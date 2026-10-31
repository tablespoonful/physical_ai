---
title: "PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation"
date: "2026-01-07"
authors: "Wenlong Huang; Yu-Wei Chao; Arsalan Mousavian; Ming-Yu Liu; Dieter Fox; Kaichun Mo"
venue: "ICLR 2026 Conference Withdrawn Submission"
url: https://arxiv.org/abs/2601.03782
pdf: https://arxiv.org/pdf/2601.03782
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.03782)** / [論文ページ](https://arxiv.org/abs/2601.03782)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**PointWorld: Scaling 3D World Models for In-The-Wild Robotic Manipulation** 

**Wenlong Huang**<sup>1</sup><sup>_,†_</sup> **, Yu-Wei Chao**<sup>2</sup> **, Arsalan Mousavian**<sup>2</sup> **, Ming-Yu Liu**<sup>2</sup> **Dieter Fox**<sup>2</sup> **, Kaichun Mo**<sup>2</sup><sup>_,∗_</sup> **, Li Fei-Fei**<sup>1</sup><sup>_,∗_</sup> 

1Stanford University 2NVIDIA 

> _∗_ Equal advising _†_ Work done partly at NVIDIA 

point-world.github.io 


Figure 1. **POINTWORLD** is a large pre-trained 3D world model that predicts full-scene 3D point flows from a static point cloud and an embodiment-agnostic description of robot actions, represented also as 3D point flows. We curate a large-scale 3D dynamics modeling dataset, spanning single-arm, bimanual, whole-body, mobile manipulation interactions in real and simulated domains. Through careful evaluations, we rigorously study the recipe for scaling up 3D world models. Pretrained on diverse data, a single model enables diverse manipulation behaviors on physical hardware, given only a single RGB-D image captured in the wild, without additional data or finetuning. 

# **Abstract** 

_Humans anticipate, from a glance and a contemplated action of their bodies, how the 3D world will respond, a capability that is equally vital for robotic manipulation. We introduce_ **POINTWORLD** _, a large pre-trained 3D world model that unifies state and action in a shared 3D space as 3D point flows: given one or few RGB-D images and a sequence of low-level robot action commands,_ POINTWORLD _forecasts per-pixel displacements in 3D that respond to the given actions. By representing actions as 3D point flows instead of embodiment-specific action spaces (e.g., joint positions), this formulation directly conditions on physical geometries of robots, while seamlessly integrating learning across embodiments. To train our 3D world model, we curate a large-scale dataset spanning real and simulated robotic manipulation in_ 

_open-world environments, enabled by recent advances in 3D vision and simulated environments, totaling about 2M trajectories and 500 hours across a single-arm Franka and a bimanual humanoid. Through rigorous, large-scale empirical studies of backbones, action representations, learning objectives, partial observability, data mixtures, domain transfers, and scaling, we distill design principles for large-scale 3D world modeling. With a real-time (0.1s) inference speed,_ POINTWORLD _can be efficiently integrated in the modelpredictive control (MPC) framework for manipulation. We demonstrate that a_ **_single pre-trained checkpoint_** _enables a real-world Franka robot to perform rigid-body pushing, deformable and articulated object manipulation, and tool use, without requiring any demonstrations or post-training and all from a single image captured in-the-wild. Code, dataset, and pre-trained checkpoints will be open-sourced._ 

1 

# **1. Introduction** 

World modeling in unstructured environments is imperative for general-purpose robots: predicting how the world evolves from what the robot sees and intends to do with its body. Humans do this from a glance and a grasp, forecasting deformation, articulation, stability, and contact, revealing how much a world-modeling objective captures when conditioned on a contemplated action in 3D (Figure 3). Actions unfold where physics lives, in space and time: our aim is a predictive model that makes such spatially grounded, actionconditioned predictions from only perceptual inputs in openworld settings, a pinnacle goal of spatial intelligence [1]. 

A large body of work has studied world modeling from complementary angles. Physics-based models [2], while capable of highly accurate predictions, face sim-to-real gaps and require curated, environment-specific modeling. Learning-based dynamics models [3] address this by learning from observed interaction, yet often depend on domainspecific inductive bias (e.g., full observability, objectness priors, or material specification). In parallel, large video generative models trained at scale [4] are capable of producing photorealistic predictions but lack explicit action conditioning and often fall short on physical consistency. See Ai et al. [5] for a recent survey. Despite progress, a gap remains between what current models predict and what humans can foresee from visual observations in the wild and a contemplated action. 

Our philosophy is unification for scaling: represent _state_ and _action_ in the same modality of 3D physical space. State is represented by a full-scene 3D point cloud built from RGB-D captures; actions are dense 3D point trajectories instantiated from the agent’s own embodiment, typically known a priori (e.g., a robot description file), and thus forecastable over time. Under this representation, 3D world modeling equates to modeling _full-scene 3D point flow_ under perturbations from a temporal sequence of robot points: given partially observed 3D scene points and those action points, predict per-point scene displacements over a horizon. While conceptually simple, this formulation ties raw sensory observation and an _embodiment-agnostic_ action space in a shared representation through dynamics (what moves, how, and where) and implicitly captures objectness, articulation, and material properties, all through interaction between the robot’s specific geometry (e.g., grippers, fingers) and the partially-observed scene. By modeling the _geometries of interaction_ independent of goals, POINTWORLD aims to capture the single source of truth of the physical world, while naturally learning from heterogeneous embodiments, tasks, and trajectories (regardless of success or failure), akin to “next-token prediction” [6] but for interaction over 3D space and time. We term our approach **POINTWORLD** . 

To provide supervision, we curate a large-scale dataset for 3D dynamics modeling, spanning hundreds of in-the- 

wild scenes with single-arm, bimanual, and whole-body interactions across both real and simulated domains. The dataset was built from existing robotic manipulation datasets, DROID [7] and BEHAVIOR-1K [8]. Since accurate 3D annotations are crucial for capturing precise contact in physical interactions, significant efforts were spent to build a custom pipeline to extract 3D point flows from the real-world dataset, enabled by recent advances in metric depth estimation [9], camera pose estimation [10], and point tracking [11]. Leveraging the dataset, we distill important design decisions for large-scale 3D dynamics learning through rigorous investigations of backbone architectures, action representations, objectives, partial observability, data mixtures, scaling laws, and domain transfers under zero-shot and finetuned settings. 

To demonstrate POINTWORLD’s potential for manipulation, we integrate it with a model-predictive controller (MPC) for action inference on a real robot. As POINTWORLD predicts scene dynamics jointly over short action chunks in a single forward pass at a real-time latency (0.1s), it provides a natural and efficient integration with sampling-based MPC (e.g., MPPI [12]). We show that a **single pre-trained checkpoint** enables a real-world robot to perform rigid-body pushing, deformable and articulated object manipulation, and tool use, without requiring any demonstrations or posttraining and all from a single image captured in-the-wild. **Contributions. (i)** We introduce a large pre-trained 3D world model, POINTWORLD, that unifies state and action in a shared representation of 3D point flows, and present rigorous studies of its modeling recipe. **(ii)** We curate and open-source a large-scale high-quality 3D interaction dataset used for training POINTWORLD, totaling _∼_ 2M trajectories or _∼_ 500 hours. **(iii)** We demonstrate a single pre-trained POINTWORLD enables a real robot to perform diverse manipulation tasks from a single in-the-wild RGB-D capture, without requiring additional demonstrations or training. 

# **2. Related Work** 

**World Modeling.** World models [13] are predictive models that simulate future states given current state and action, categorized often by their state-action representations. Video models use pixel-space state, trained either with photometric reconstruction [4, 14–29] or joint-embedding predictions [30, 31]. 3D world models instead operate on meshes or explicit surfaces [32–38], radiance fields or Gaussians [39–48], or particles [3, 49–56]. Hybrid approaches additionally reason over hierarchical structures in world modeling [57–63]. Action parameterizations range from low-level joint-space commands [14, 64–70], to camera and navigation motions [71–78], textual prompts [4, 79–83], and 2D cues [84–94]. Robot actions can then be produced by online planning [3, 12, 64, 95–97], offline policy synthesis [64–67, 98–100], or inverse-dynamics models [101–103]. POINTWORLD uses 3D point flow as shared state-action rep- 

2 


Figure 2. **Overview of POINTWORLD** . Given calibrated RGB-D, robot joint-space actions, and a robot description file (URDF), we convert actions to robot flows and concatenate with scene to form a single point cloud serving as an _embodiment-agnostic interaction geometry_ . Scene points are featurized with a frozen DINOv3 encoder, robot points with temporal embeddings, and a point cloud backbone predicts _full-scene_ 3D point flows. 

resentation, emphasizing contact and geometry rather than appearance, conditions on 3D actions with specific geometry of given robot/gripper, interaction beyond only visible regions compared to 2D cues, and doing so with one (or sparse) input images (with estimated depth) in a single, real-time forward pass of a large pre-trained model (Figure 3). 

**Dynamics Models in Robotics.** Dynamics models in robotics instantiate world models with robot action spaces. They include physics-based simulators [2, 104–108] and learning-based models [3, 5, 33, 49–54, 69, 109]. Crucial for robotics, they support policy learning [110–112], planning [58, 113–116], model-based RL [64–67, 98–100], exploration and online guidance [117–120], safety filtering [121, 122], model-based design and verification [105, 123, 124], and policy evaluation [46, 125–127]. While existing dynamics models often require curated, scene-specific modeling [5], our aim is to pre-train a single dynamics model that generalizes across diverse in-the-wild environments. Using 3D flows as state-action space, it naturally encapsulates many action parameterizations used in prior works in an embodiment-agnostic manner: joint-space commands [69, 109, 128], end-effector actions [53], and motion primitives [3, 129], while operating on partially observable RGB-D image(s) in the wild without scene reconstruction [35], priors on objectness [53] or materials [130]. 

**2D and 3D Flows for Manipulation.** Flows (or point tracks), which address correspondences across space and time, provide a powerful interface between perception and control. With advances in point tracking [11, 131, 132], recent works explored them as structured representations for policy learning [133–140], reward modeling [141–144], (sub-)goal specification [145], or as visual servoing targets [103, 146–150]. In this work, we leverage recent advances in 3D vision (depth [9], camera pose estimation [10], and point tracking [11]) to label 3D scene flows from largescale real-world manipulation dataset [7] (with robot flows obtained from known robot geometry, kinematics, and proprioception), which enables training of a large 3D world models via stable regression losses to capture robotic interactions with diverse objects in open-world environments. 

# **3. Method** 

We formulate 3D world modeling as action-conditioned fullscene 3D point flow prediction (Section 3.1; Figure 2). We then describe how POINTWORLD may be used for action inference and discuss its use case in the framework of model predictive control that we explore in this work (Section 3.2). 

## **3.1. 3D World Modeling with POINTWORLD** 

We model environment dynamics as a neural network _Fθ_ : **S** _×_ **A** _→_ **S** parametrized by _θ_ that predicts next state given current state and robot action, where **S** and **A** denote state and action spaces. Existing approaches [5] typically formulate this as a single-step update **s** _t_ +1 = _Fθ_ � **s** _t,_ **a** _t_ �. In contrast, we adopt a multi-step (chunked) formulation for datadriven modeling [151]: the model predicts future states over a horizon _H_ in a single forward pass _Fθ_<sup>_H_: (</sup><sup>**s**</sup><sup>_t,_</sup><sup>**a**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_H−_1)</sup><sup>_→_</sup> **s** _t_ +1: _t_ + _H_ , which improves temporal consistency and amortizes computation. We use _H_ = 10 steps and 0.1s per step. 

**State Representation.** Building a world model requires a deliberate choice of a state space **S** , with state at time _t_ denoted by **s** _t ∈_ **S** . In this work, we use _point flows_ (referred also as particles [3, 53]) as the environment state. Formally, let **s** _t_ = _{_ ( **p** _t,i,_ **f** _i_<sup>_S_)</sup><sup>_}N_</sup> _i_ =1<sup>_S_denotethepointflowsattime</sup><sup>_t_,</sup> consisting of _NS_ points with positions **p** _t,i ∈_ R<sup>3</sup> and timeconstant features **f** _i_<sup>_S∈_R</sup><sup>_DS_of dimension</sup><sup>_DS_for each point.</sup> Compared to alternative representations, point flows offer the following advantages for world modeling in manipulation: (i) emphasis on physical interactions between 3D geometries instead of appearance, akin to the role of physics simulators rather than renderers; (ii) accessibility from any RGB-D captures in partially observable environments [114] while not assuming objectness or material priors; (iii) simple and stable training via L2 losses on displacements, without permutation matching; (iv) expressiveness to capture diverse fine-grained contact dynamics. To obtain the point flows, 

3 


Figure 3. **Rich Supervision of 3D World Modeling for Physical Interactions** , when conditioned on 3D robot point flows and partial observable RGB-D. The 3D world modeling objective enjoys dense pixel-level supervision while encoding a wide range of capabilities central to robotic manipulation. To predict full-scene evolution, the model needs to implicitly segment objects of interest, identify material property and/or articulation structure, perform implicit shape completion for contact reasoning, propagate robot-object interaction for object-object dynamics, and simultaneously considering the effects of gravity, encapsulated all in a single forward pass of the learned model. 

from one or a few calibrated RGB-D views, we mask robot pixels via forward kinematics (using the URDF and joint configuration) and back-project the remaining pixels to obtain **p** _t,i_ . Note that since the model takes in a static point set from the environment as input, and correspondence is preserved only within the model’s forward pass (i.e., its “imagination”), no separate point tracker is required for inference, and point count may vary between forward passes. 

**Action Representation.** To learn from heterogeneous embodiments (different kinematics, gripper geometries, and even different numbers of grippers), we again use 3D point flows. However, unlike scene point flows which are obtained from RGB-D captures, robot point flows are generated by forecasting the robot’s own geometry via forward kinematics using its URDF (known a priori). This is an intentional design for ensuring “imagined actions” are _fully_ , rather than partially, observable while being represented in an _embodiment-agnostic_ way–crucial in cases where contact occurs in occluded regions (e.g., holding and transporting a large box with egocentric view). Specifically, given a sequence of joint configurations _{_ **q** _t_ + _k}_<sup>_H_</sup> _k_ =0<sup>, we sample robot</sup> surface points once at time _t_ , attach each to its corresponding link, and propagate them with forward kinematics to obtain an ordered set of _NR_ robot points _{_ ( **r** _t_ + _k,j,_ **f** _t_<sup>_R_</sup> + _k,j_<sup>)</sup><sup>_}_</sup> _j_<sup>_N_</sup> =1<sup>_R_at</sup> each time step _t_ + _k_ , where **r** _t_ + _k,j ∈_ R<sup>3</sup> denotes the position of point _j_ at time _t_ + _k_ and **f** _t_<sup>_R_</sup> + _k,j_<sup>_∈_R</sup><sup>_DR_is its time-varying</sup> feature vector of dimension _DR_ . We treat this collection as the action at time _t_ + _k_ and denote it by **a** _t_ + _k_ . This yields an embodiment-agnostic description of _interaction geometry_ over the horizon. In practice, most robot surface points never contact the scene; for efficiency, we sample robot point flows from only the grippers (a few hundred points per gripper depending on its geometry). See Section 5.2 for experiments. 

**Dynamics Prediction.** Given the above state-action representations, we now have a static full-scene point cloud **s** _t_ and a temporal sequence of robot point-flow actions **a** _t_ : _t_ + _H−_ 1 as inputs to the model. Instead of designing custom architectures, we deliberately build on top of state-of-the-art point cloud backbones [152] to distill the core principles that enable scalable, large-scale 3D world modeling. Towards this goal, we concatenate the initial scene points with the time-stacked robot points to form a single point cloud processed by the backbone. Scene points are featurized with frozen DINOv3 [153, 154] by projecting them to 2D views, while robot points are featurized with temporal embedding. The point cloud backbone processes the concatenated point cloud and outputs features for all points. A shared MLP head then predicts per-point displacements of the scene points at each step within a chunk of length _H_ in a single forward pass. This chunked formulation delivers extremely efficient inference capable of evaluating many candidate trajectories with a real-time latency (0 _._ 1 s per batched forward pass), which stands in contrast to pixel-based approaches that typically require seconds-long inference [31, 80] due to the use of diffusion objectives. 

**Training Objective.** While the formulation lends itself to standard regression objectives, 3D world modeling introduces two distinctive challenges that require careful design: (i) due to full-scene prediction, the robot often manipulates only a small subset of the scene, so most points are static and standard L2 loss leads to very sparse training signal; (ii) real-world data is noisy, so we need to regularize the model to be robust to this noise. To address challenge (i), we adopt a weighted regression objective, reweighting each point at each timestep by a soft movement likelihood _mk,i ∈_ [0 _,_ 1] computed from ground-truth motion so as to focus the loss 

4 


Figure 4. **Movement Weighting and Uncertainty Regularization** , where the robot releases and drops a yellow cloth. ( **Bottom Left** ) The movement weighting, used in the training objective, effectively biases the training towards scene points that are moving at each timestep, computed with the ground-truth flows. ( **Bottom Right** ) The uncertainty value, predicted by the model without any ground-truth, regularizes training to prevent overfitting to points that have unreliable ground-truth. Intriguingly, we observe that it also emerges to capture action-conditioned uncertainty arising from the object’s physical properties (e.g., larger variability along the edge of the cloth). 

on moving points. Letting _δk,i ≥_ 0 denote the norm of the ground-truth displacement vector for point _i_ at step _k_ , we set _mk,i_ = _σ_ � _κ_ ( _δk,i − τ_ )�, where _σ_ is the logistic sigmoid, and _τ_ and _κ_ are non-negative displacement-threshold and temperature parameters, respectively. We then normalize these likelihoods to obtain weights _wk,i_ = _mk,i/_<sup>�</sup> _k,i_<sup>_mk,i_</sup> for each point _i_ at step _k_ . To address challenge (ii), we adopt aleatoric uncertainty regularization [10, 155, 156] by predicting a scalar log-variance _sk,i_ for each point _i_ at step _k_ and further using a Huber loss on the residual. Formally, the full training objective becomes: 


where _ρδ_ is the elementwise Huber loss, and **P**<sup>**ˆ**</sup> _t_ + _k,i_ and **P** _t_ + _k,i_ are the predicted and ground-truth positions of point _i_ at step _k_ , respectively. In practice, we also ignore the points that are deemed not visible by the 2D tracker used to provide the pseudo ground-truth (more details in Section 4). 

## **3.2. POINTWORLD for Robotic Manipulation** 

A pre-trained POINTWORLD enables diverse use cases in robotics, as discussed in Section 2. In this work, we specifically investigate whether a single pre-trained POINTWORLD can enable action inference in unseen, in-the-wild real-world environments from only a single RGB-D capture, **without any additional demonstrations or post-training at deployment time** . To this end, we integrate POINTWORLD in an MPC framework with a sampling-based planner MPPI [12] that plans a sequence of _T_ end-effector pose targets in SE(3) given a cost function defined in the model’s state space. 

Specifically, given a calibrated RGB-D capture, we first form a scene point set as described in Section 3.1, yielding an initial state **s** 0. We then sample _K_ action perturbations _ℓ_ 1: _K_ using a time-correlated (cubic-spline) noise distribution, which are added to a nominal end-effector trajectory. For each sampled trajectory **E**<sup>(</sup> 1:<sup>_ℓ_</sup> _T_<sup>), the corresponding</sup> robot point-flow actions **a**<sup>(</sup> 1:<sup>_ℓ_</sup> _T_<sup>)are constructed, scene flows</sup> are rolled out by POINTWORLD conditioned on **a**<sup>(</sup> 1:<sup>_ℓ_</sup> _T_<sup>), and a</sup> trajectory cost _J_<sup>(</sup><sup>_ℓ_)</sup> is accumulated. The nominal trajectory is iteratively refined by computing exponentiated weights _ωℓ ∝_ exp( _−J_<sup>(</sup><sup>_ℓ_)</sup> _/β_ ) over samples and updating the nominal as a weighted average of sampled trajectories, where _β_ is non-negative temperature. 


where _c_ ctrl subsumes path length and reachability regularization, **E** _k_ denotes end-effector pose at step _k_ , and **E** measured is the current end-effector pose. Further details in Appendix. 

5 


Figure 5. **3D Annotation Quality and Comparisons.** FS denotes FoundationStereo [9]; Dataset Extrinsics V1 and V2 are the two DROID extrinsics releases. **(Top)** Compared to DROID releases, our pipeline yields substantially higher-quality depth and camera pose calibration, resulting in more accurate robot mask overlays and better aligned point clouds (readers are encouraged to zoom in or check out the interactive visualization on the project website for details). **(Bottom)** We further compute depth reprojection loss (differences between analytical and observed depth of robot surface), and F1 scores of point cloud alignment. We observe purely leveraging existing models (FS, VGGT) are insufficient, and V2 extrinsics improve over V1 by filtering out scenes with poor point cloud alignment but result in significantly lower scene counts. In contrast, our annotation pipeline retains substantially more scenes below 0 _._ 10 depth-loss criterion and dominates all metrics. 

# **4. Dataset Curation and Evaluation Protocol** 

dynamics modeling dataset, which we fully open-source. 

Accurate, large-scale 3D data is essential for the world model in Section 3 to generalize in the wild. Apart from requiring action labels, the dataset needs to also have accurate spatial perception (i.e., high-fidelity depth), hand-eye calibration (i.e., camera extrinsics in robot base frame), and per-pixel correspondence matching amid occlusions (i.e., point tracking). While large efforts have been made for collecting diverse real-world manipulation datasets [7, 158], obtaining their 3D annotations has previously been challenging. Our key observation is that recent advances in 3D vision—metric depth estimation, camera pose estimation, and dense point tracking—are maturing to provide a markerless offline pipeline that operates purely on recorded data to produce such a dataset of interest (Figure 5 top-left). Photorealistic simulation complements this with ground-truth supervision. Combining both, we curate a dataset of about 2M trajectories (500 hours) spanning single-arm, bimanual, and whole-body teleoperated interactions across in-the-wild real scenes and simulated home-scale environments. To the best of our knowledge, this constitutes the largest 3D 

**3D Annotation for Real-World Data.** We leverage DROID [7], a robot manipulation dataset with diverse inthe-wild interactions recorded by two external cameras and a wrist-mounted camera. Although DROID provides sensor depth and camera extrinsics, the depth often degrades in open-world environments and camera poses are inaccurate due to imperfect calibration. Frontier 3D reconstruction models such as VGGT [10] jointly estimate depth and camera parameters from RGB images and often look visually plausible, but yield overly smoothed depth maps and camera poses that can deviate from ground-truth by tens of centimeters. 

After extensive experimentation, we adopt a three-stage annotation pipeline that combines several learned models with a dedicated optimization procedure. First, we replace sensor depth with stereo-estimated depth from FoundationStereo [9], which is particularly effective at the close working distances typical of manipulation. Second, we compute camera extrinsics by refining VGGT-initialized camera poses with an optimization procedure that aligns robot depth observations to the known robot mesh. Third, given accurate depth 

6 


Figure 6. **Unseen rollouts from a single pre-trained POINTWORLD across diverse domains** , visualized with Viser [157]. Given RGB-D captures, POINTWORLD predicts 10-step point flows conditioned on robot flows. We show first prediction, last prediction, and last ground-truth. Green points in GT mark regions occluded during 2D point tracking, for which we observe model predictions are often more accurate because these points are not being supervised in model training. Due to grid downsampling (1 _._ 5cm) we apply to all point clouds, all 3D visualization is upsampled to image resolution for visual clarity via nearest neighbors. Interactive visualization at project website. 

7 


Figure 7. **Roadmap for Scaling 3D World Models** , measured by _ℓ_ 2 error on moving scene points on DROID test set. Starting from an existing baseline [5], we progressively modernize the backbone, stabilize training objectives, leverage pre-trained features, and scale model size, yielding consistent gains in accuracy. Hatched bars indicate settings that are not adopted in the final model. 

and extrinsics, we perform per-pixel point tracking using CoTracker3 [11]. CoTracker3 is a 2D point tracker that outputs image-space correspondences and a visibility map; we lift these tracks to 3D using the refined depth and camera poses and carry over the visibility labels so that occluded points are excluded from supervision during model training. With this pipeline, we recover reliable tracked 3D point flows for over 60% of DROID (nearly 200 hours of raw human teleoperation) and obtain reconstructed point clouds that both qualitatively and quantitatively improve over both original dataset and alternative annotation methods (Figure 5). To further assess extrinsics accuracy in the absence of ground truth in the real world, we treat the best 1% of scenes under the original dataset extrinsics (as measured by depth reprojection loss) as a proxy for the true extrinsics. Relative to this reference, our optimized extrinsics achieve a median translation and rotation error of 1.8 cm and 1.9 degrees. 

**Simulation (BEHAVIOR-1K).** To complement realworld data, we use BEHAVIOR-1K [8] (B1K), which provides about 1100 hours of teleoperated (pre-filtering) interaction in photorealistic home-scale environments with bimanual, whole-body, and mobile manipulation. We obtain ground-truth 3D point flows by leveraging known simulation state. Because the dataset focuses on long-horizon activities 

while POINTWORLD focuses on short-horizon interaction dynamics, we filter trajectories using privileged information accessible in simulation. We retain only trajectories with active contacts between robot and objects and those with nonzero object motion. More details are in Appendix. 

**Model Evaluation Protocol.** We evaluate predicted point flow from POINTWORLD and other baselines using a perpoint, per-timestep _ℓ_ 2 distance over the prediction horizon. Because most scene points remain static during robot interaction, we focus on the metric on moving points ( _ℓ_ 2 mover), as measured by ground-truth data and filter the full set of points using the movement likelihood introduced in Section 3. For real-world domains, we further denoise the evaluation data by training a separate expert model only on the held-out test split to flag unreliable flows via the uncertainty objective from Section 3, retaining only the top 80% of points measured by model confidence. All evaluated models are trained exclusively on the imperfect training set and are evaluated on the expert-filtered test set. Details in Appendix. 

**Interpretation of the Metric.** This dense per-point _ℓ_ 2 metric is highly discriminative when comparing methods and reveals systematic differences in rollout fidelity that tasklevel success rates often fail to expose [125]. Because all errors are measured over one-second horizons, absolute metric differences can appear modest, since even large motions move points by only a few centimeters, yet we empirically observe that small numerical differences often correspond to pronounced qualitative gains in rollout fidelity. Given the scale of the evaluation set (approx. 40 _,_ 000 robot trajectories with 10 _,_ 000 point flows each), standard errors for the _ℓ_ 2 metrics are negligible ( _≤_ 10<sup>_−_5</sup> m), so we report means only. 

# **5. Experiments** 

Focusing on real-world data, we chart a roadmap of empirical lessons we learned for scaling 3D world models (Section 5.1, Figure 7) [159, 160]. We then discuss targeted ablations along complementary design axes for POINTWORLD (Section 5.2). Using real and simulated data, we quantify in-domain, cross-domain, and held-out generalization under zero-shot and finetuned settings (Section 5.3). Finally, we study POINTWORLD for MPC-based action inference on a physical robot in the wild without extra demonstrations or finetuning (Section 5.4). All experiments are constructed to isolate a single modeling choice under controlled setups compared to baselines unless otherwise stated. 

## **5.1. Scaling 3D World Models: A Roadmap** 

**Modern point cloud backbone (PTv3 [152]) is effective, efficient, and scalable for 3D world modeling.** Graphbased neural dynamics (GBND) models are widely used for 

8 


Figure 8. **Real-World Action Inference** . POINTWORLD runs zero-shot with MPC for rigid, deformable, articulated, and tool-use tasks in the wild. Success rates are on top. 


Figure 9. **Scaling Study** . Scaling POINTWORLD in either data or model size yields roughly log-linear gains in prediction accuracy. 

|**Backbone**|**Params**|**Mem.**|**FLOPs**|**Latency**|_ℓ_2 **mov.**|_ℓ_2 **stat.**|
|---|---|---|---|---|---|---|
|❍GBND|1_._00x|1_._00x|1_._00x|13_._46|0.0390|0.0066|
|❍PointNet|1_._03x|0_._34x|0_._04x|5_._93|0.0369|0.0084|
|❍PointNet++|1_._07x|0_._67x|0_._06x|327_._08|0.0368|0.0073|
|❍SparseConv|33_._31x|7_._18x|1_._32x|17_._70|0.0396|0.0076|
|❍Transformer|41_._06x|0_._31x|3_._38x|30_._43|0.0339|0.0071|
|●PTv3-50M|49_._14x|0_._30x|0_._34x|59_._60|0.0331|0.0067|
|●PTv3-132M|127_._22x|0_._69x|1_._04x|69_._60|0.0324|0.0061|
|●PTv3-411M|398_._67x|1_._89x|1_._90x|102_._47|0.0315|0.0059|
|●PTv3-1B|**957**_._**71**x|4_._30x|3_._57x|123_._65|**0.0312**|**0.0056**|


Table 1. **Backbone Comparisons.** PTv3 [152] enables massive parameter scaling while retaining similar memory and efficient inference (latency in milliseconds, PTv3-1B _≈_ 0 _._ 12 s). 

dynamics modeling due to their relational inductive bias [5]. Scaling a GBND baseline to our dataset reveals two challenges (Table 1). Memory consumption grows rapidly because maintaining high-dim features for all points in a scene is expensive. Purely local message passing struggles under partial observability, since long-range effects must traverse noisy hops. Motivated by these limitations, we study alternative point cloud architectures, moving from PointNet [161], PointNet++ [162], sparse convolutional nets [163] to transformers [164]. Among these, PointTransformerV3 [152] (PTv3) delivers the strongest modeling power. Its point serialization mirrors GBND’s local grouping, while U-net hierarchy enables attention over progressively coarser point sets for long-range modeling and substantial parameter growth. Table 1 shows that it scales to 957 _×_ GBND while keeping modest memory and runtime increases. These results motivate PTv3 as the default backbone. 

**Movement weighting, uncertainty regularization, Huber loss stabilize 3D world model learning on real-world data.** Discussed in Section 3, na¨ıve _ℓ_ 2 loss is hard to optimize because only a fraction of points move (1–5%). Noisy real-world data exacerbates this. We therefore adopt movement weighting, uncertainty regularization, and a Huber loss on 3D residuals. Movement weighting alone over- 

emphasizes noisy signals, but the uncertainty head and robust loss temper the weights and reduce overfitting. Together, these changes stabilize training and improve accuracy relative to an unweighted _ℓ_ 2 baseline. 

**Pre-trained 2D features offer critical priors and substantial gains.** High-quality pretrained 3D representations remain scarce despite compelling 3D geometry. Methods such as Sonata [160] make encouraging progress but often lag behind in fine-grained scenes. Following [9, 10], we hypothesize that dense features from DINOv3 [153] provide objectness priors without explicit segmentation. We therefore project points into calibrated cameras and attach features from multiple layers from a frozen DINOv3. This simple addition substantially boosts accuracy over the baseline. 

**Model size scaling is necessary to ingest large-scale world modeling data.** With architecture, objective, and features in place, we expand depth and width within the same PTv3 blueprint. Aligned with scaling-law observations in vision and language modeling [165], scaling model size from 50M to 1B parameters yields smooth, log-linear gains (Figure 9) similarly for 3D world modeling. 

**Taken together** , all these levers—backbone, training objective, pre-trained feature, and model scaling—yield substantial gains over the original GBND baseline [5]. 

## **5.2. Ablations** 

**Representing actions as point flows on grippers balances effective, efficient contact reasoning and enables positive transfer across heterogeneous embodiments.** In POINTWORLD, robot actions are dense point flows over grippers with 300–500 points per gripper. We compare against four baselines: (i) whole-body point flows with the same number of points (sparser coverage), (ii) whole-body point clouds with 2000 points (similar density as ours), (iii) 6-DoF endeffector pose and gripper openness, and (iv) joint positions and gripper openness. The last two low-dim variants omit robot points, which the flow-based models concatenate with 

9 


Figure 10. **Zero-Shot and Finetuned Generalization to Held-Out Real-World Scenes** , where the robot transports a reflective glass bottle. POINTWORLD pre-trained on DROID or jointly on DROID and BEHAVIOR (D+B) are capable of zero-shot generalizing to unseen environment and motion from a held-out DROID lab’s scene, closing the gap to the specialist variant trained on that lab’s data. POINTWORLD pre-trained on only simulation data fail to generalize zero-shot. Further finetuning yields more accurate object trajectories of grasped objects. 


|||In-Do|main|Cross-|Domain|H|eld-Out|Real|From|
|---|---|---|---|---|---|---|---|---|---|
|||D_→_D|B_→_B|D_→_B|B_→_D|D_→_H|B_→_H|D+B_→_H|Scratch|
|**Zero-Shot**|<sup>_ℓ_2 mover</sup><sup>_↓_</sup>|0.0315|0.0087|0.1460|0.0558|0.0305|0.0531|0.0300|0.0293|
||<br>_ℓ_2 static_↓_|0.0059|0.0010|0.0050|0.0058|0.0049|0.0057|0.0063|0.0043|
|**Finetuned**|<sup>_ℓ_2 mover</sup><sup>_↓_</sup>|–|–|0.0107|0.0378|0.0271|0.0299|0.0272|0.0293|
||<br>_ℓ_2 static_↓_|–|–|0.0003|0.0086|0.0040|0.0046|0.0040|0.0043|


Table 2. **Generalization of POINTWORLD across in-domain, cross-domain, heldout real environments under zero-shot and finetuned settings.** D denotes DROID, B denotes B1K, H denotes held-out real-world scenes. “From Scratch” denotes specialist trained on the held-out lab’s data. Evaluations are done on unseen samples from the corresponding dataset. POINTWORLD generalizes within domains, zero-shot transfers to unseen real-world environments, surpasses specialists if finetuned with 20x fewer updates, and benefits from real-sim co-training. 

Figure 11. **Action representations.** Representing actions as point flows on grippers balances effective, efficient contact reasoning and enables positive transfer across heterogeneous embodiments. 

scene features. We train all models jointly on both DROID and B1K data, where DROID uses a single-arm Franka and B1K uses a bimanual humanoid. Results are in Figure 11. On B1K, representing contact spatially lets point-flow actions outperform low-dim alternatives (end-effector poses and joint positions). Sparse whole-body flows underperform gripper-only flows, likely due to insufficient resolution to capture precise contact. Dense whole-body flows help but still lag behind, as gradients must pass through inactive points and incur compute overhead. On real-world DROID, both whole-body point-flow baselines underperform low-dim baselines. A plausible explanation is that extensive robot points obscure already-sparse learning signals from noisy real-world data. Gripper-only flows address this issue and attain the best performance, underscoring their effectiveness on real-world data and their ability to obtain positive transfer across heterogeneous embodiments in both domains. 

(equivalent to 1 second). We ablate this design choice against two autoregressive baselines: (i) teacher-forcing (GT input each step) and (ii) self-feeding with 10k warmup steps, plus sliding-window inference ( _W_ =1 _,_ 5) using the same chunked model. Results are shown in Figure 12. Teacher-forcing outperforms self-feeding when training and inference strategies are aligned. Evaluating a chunk-trained model with _W_ =1 (equivalent to self-feeding) incurs the strongest performance degradation; _W_ =5 recovers some accuracy but degrades after the trained window. Matching chunked prediction in training and testing over the full horizon minimizes drift while amortizing compute with only a single forward pass (vs. 2–10 for autoregressive), highlighting chunking as both more accurate and more compute-efficient design choice. 

**POINTWORLD is robust to different levels of partial observability and benefits from additional cameras in both training and inference.** We train four variants that differ only in camera count for RGB-D observations: one, two, three, or a random draw of up to three cameras. We then evaluate all models on three settings with up to three 

**Using chunked prediction in both training and inference reduces rollout drift while improving compute efficiency.** POINTWORLD performs 10-step chunked prediction 

10 

cameras. Results are in Figure 13. Error on moving points stays sub-centimeter with negligible standard errors, but using more cameras at train time consistently reduces error at test time. Interestingly, models trained with fixed camera count perform better when more cameras are available at inference. The random-view model is most robust across all test camera counts, suggesting that exposure to varied observability helps the model infer objectness and physical properties under partial observability at inference time. 

**Prediction error decreases roughly log-linearly with both model size and data.** Inspired by scaling laws from language and vision [165–167], we test whether POINTWORLD follows similar trends. On DROID, we vary model capacity (50M–1B) and data fraction (5%–100%). Each curve sweeps one axis only. In log space we observe approximately linear behavior for both axes (Figure 9), suggesting predictable gains from extra data and capacity. 

## **5.3. Generalization and Transfer** 

We study POINTWORLD’s generalization across in-domain, cross-domain, and to held-out real-world environments under zero-shot and finetuned settings. Each finetuning uses 1 _/_ 20 of the original training iterations. Results are in Table 2. 

**POINTWORLD generalizes within domains.** We study in-domain transfer on held-out splits of DROID and B1K that are unseen during training. On B1K the model achieves sub-centimeter mover error on held-out trajectories, while DROID performance on held-out remains similar to training despite real-world variations. This indicates that POINTWORLD does not simply memorize training samples. 

**Pre-trained POINTWORLD can be efficiently finetuned (20x fewer updates) for both real-to-sim and sim-to-real transfer.** We study cross-domain transfer by evaluating how a model pre-trained on DROID generalizes to B1K, and vice versa. Zero-shot transfer between simulation and real domains remains challenging. Yet, finetuning with only 5% of the original training steps rapidly narrows the gap to domainspecific models trained from scratch using 20 _×_ more updates. The effect is symmetric: real-to-sim and sim-to-real transfers both benefit. Empirically, we observe training on real-world data provide better transfer than reverse, plausibly due to the higher scene diversity of the real-world data. 

**POINTWORLD zero-shot generalizes to unseen realworld environments, surpasses specialists if finetuned with 20x fewer updates, and benefits from real-sim cotraining.** To study held-out real generalization, we hold out data from the CLVR lab within DROID and evaluate how well a model pre-trained on the remaining DROID data generalizes to that lab. The held-out set is split into 90% train and 10% test. Zero-shot models never see these frames, while finetuned variants access only the 90% subset. POINTWORLD pre-trained on the remaining DROID data achieves on-par performance with specialists trained on the 


Figure 12. **Ablation on Chunked Prediction** , where we study different rollout strategies in training and testing. Chunked rollouts at both training and inference time lead to significantly less drift than other baselines while amortizing compute with only a single forward pass of the model. 


Figure 13. **Ablation on Partial Observability** , where we train variants of POINTWORLD with varying number of cameras and evaluate them on all settings at test time. POINTWORLD is robust to different levels of partial observability and benefits from additional cameras in both training and inference. Training with randomized camera counts yields the best performance across all test settings. 

held-out lab despite changes in background, lighting, object, and possibly motion distribution. With finetuning, it quickly surpasses the specialist. We observe simulation-pretrained models do not outperform scratch baselines yet reach comparable accuracy with finetuning. Finally, a model pre-trained on combined DROID and B1K mix delivers mildly stronger zero-shot performance than DROID-only. 

## **5.4. Model-Based Planning with POINTWORLD** 

Pre-trained on diverse interactions, we test whether POINTWORLD can be zero-shot deployed for manipulation on a physical robot in the wild. For evaluation, we use a Franka setup similar to DROID, mounted on a wheeled base and equipped with one RealSense D435 camera. Depth is estimated using FoundationStereo [9]. For each task, we manually draw an object mask and specify target positions through a GUI tool. Each optimization rolls out 30 steps (3 autoregressive forward passes). With only the pre-trained model and a shared MPC framework, POINTWORLD optimizes actions for real-world tasks: non-prehensile pushing of rigid 

11 

objects (tissue box, book), deformable manipulation (folding a scarf, placing a pillow), articulated manipulation (opening a microwave and closing a drawer, with revolute and prismatic joints), and tool use (sweeping with a duster or broom). Tasks and success rates are shown in Figure 8, indicating the pre-trained POINTWORLD captures transferable interaction dynamics, including contact reasoning under partial observability (rigid pushing), implicitly inferring articulation and deformation of objects (articulated and deformable manipulation), and object-object interactions (tool use). 

# **6. Conclusion** 

We introduced POINTWORLD, a large pre-trained 3D world model, that predicts 3D environment dynamics given in-thewild RGB-D capture(s) and robot actions under a shared representation of 3D point flows. To train the model, we leveraged recent advances in 3D vision and curated a largescale dataset for action-conditioned 3D world modeling, with high-quality depth maps, camera poses, and 3D tracks. Through empirical evaluations, we rigorously studied the recipe for scaling 3D world model training, including backbone designs, action representations, learning objectives, partial observability, data mixtures, domain transfers, and scaling laws. Pre-trained on diverse data, a single POINTWORLD model enabled practical manipulation behaviors in the real world, including non-prehensile pushing, deformable and articulated object manipulation, and tool use. 

# **Acknowledgments** 

This work is in part supported by the Stanford Institute for Human-Centered AI (HAI), the Schmidt Futures Senior Fellows grant, ONR MURI N00014-21-1-2801, ONR MURI N00014-22-1-2740. We would like to thank Leslie Kaelbling, Tomas Lozano-P´ erez, Yunzhu Li, Jiajun Wu, Ruohan´ Zhang, Jiayuan Mao, Abhishek Gupta, Pieter Abbeel, Pulkit Agrawal, Shenlong Wang, Anirudha Majumdar, Chuang Gan, David Held, Karen Liu, Jeannette Bohg, Balakumar Sundaralingam, Anqi Li, Bowen Wen, Xiaoyang Wu, Hang Gao, Chelsea Ye, Mijiu Mili, the BEHAVIOR team, members of the Stanford Vision and Learning Lab, and members of the Learning & Intelligent Systems Group for fruitful discussions, feedback, and support. 

# **References** 

- [1] Li Fei-Fei. From words to worlds: Spatial intelligence is ai’s next frontier. https://drfeifei. substack . com / p / from - words - to - worlds - spatial-intelligence, 2025. Substack. 2 

- [2] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5026–5033, 2012. 2, 3 

- [3] Yunzhu Li, Jiajun Wu, Russ Tedrake, Joshua B Tenenbaum, and Antonio Torralba. Learning particle dynamics for manipulating rigid bodies, deformable objects, and fluids. _arXiv preprint arXiv:1810.01566_ , 2018. 2, 3 

- [4] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, Clarence Ng, Ricky Wang, and Aditya Ramesh. Video generation models as world simulators. 2024. 2 

- [5] Bo Ai, Stephen Tian, Haochen Shi, Yixuan Wang, Tobias Pfaff, Cheston Tan, Henrik I. Christensen, Hao Su, Jiajun Wu, and Yunzhu Li. A review of learning-based dynamics models for robotic manipulation. _Science Robotics_ , 10(106), 2025. 2, 3, 8, 9 

- [6] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. _arXiv preprint arXiv:2005.14165_ , 2020. 2 

- [7] Alex Khazatsky, Karl Pertsch, Ashvin Nair, Ajay Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Madhav Srirama, Annie Chen, Benjamin Ellis, Patrick Fagan, Joseph Hejna, Maria Itkina, Lucille Lepert, Henry Ma, Alex Miller, Guanzhi Wu, Suneel Belkhale, Anish Dass, Jeongseok Ha, Ayush Jain, Angelica Lee, Youngwoon Lee, Nicole Memmel, Jeongho Park, Ilya Radosavovic, Rose Wang, Xuchen Zhan, Michael Black, Chi Chi, Landon Hatch, Jinqiang Lin, Zhenjia Lu, Jean Mercat, Ali Rehman, Pratyusha Sanketi, Akshara Sharma, Stacey Simpson, Quan Vuong, Pranav Walke, Blake Wulfe, Chih-Yuan Xiao, Brian Yang, Arman Yavary, Tony Zhao, Cem Agia, Parv Baijal, Alec Castro, Huan Chen, Tao Chen, Jen Jen Chung, Joshua Drake, Matthew Foster, Zhe Gao, Andres Herrera, Jeongwon Heo, Andy Hsu, Siyan Hu, Gabriel Jackson, Brian Le, Canyu Li, Hugo Lin, Donghun Ma, Avinash Maddukuri, Mihir Mirchandani, John Morton, Duc Nguyen, Brian O’Neill, Vincent Scalise, Jacob Seale, Doyeon Son, Yeming Tian, Quang Tran, Henry Wang, Andy Wu, Ho Chit Billy Xie, Juncheng Yang, Xiaolong Yin, Wenlong Zhang, Osbert Bastani, Glen Berseth, Jeannette Bohg, Ken Goldberg, Abhinav Gupta, Anchit Gupta, Dinesh Jayaraman, Joseph J. Lim, Jitendra Malik, Roberto Mart´ın-Mart´ın, Subramanian Ramamoorthy, Dorsa Sadigh, Shuran Song, Kuan-Ting Wu, Michael C. Yip, Yuke Zhu, Thomas Kollar, Sergey Levine, and Chelsea Finn. Droid: A large-scale in-the-wild robot manipulation dataset. In _Robotics: Science and Systems XX_ , 2024. 2, 3, 6, 22 

- [8] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto Mart´ın-Mart´ın, Chen Wang, Gabrael Levine, Wensi Ai, Benjamin Martinez, Hang Yin, Michael Lingelbach, Minjune Hwang, Ayano Hiranaka, Sujay Garlanka, Arman Aydin, Sharon Lee, Jiankai Sun, Mona Anvari, Manasi Sharma, Dhruva Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou, Caleb R Matthews, Ivan VillaRenteria, Jerry Huayang Tang, Claire Tang, Fei Xia, Yunzhu Li, Silvio Savarese, Hyowon Gweon, C. Karen Liu, Jiajun Wu, and Li Fei-Fei. Behavior-1k: A human-centered, embodied ai benchmark with 1,000 everyday activities and 

12 

realistic simulation. _arXiv preprint arXiv:2403.09227_ , 2024. 2, 8, 24 

- [9] Bowen Wen, Matthew Trepte, Joseph Aribido, Jan Kautz, Orazio Gallo, and Stan Birchfield. Foundationstereo: Zeroshot stereo matching. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 5249–5260, 2025. 2, 3, 6, 9, 11, 22, 30 

- [10] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: Visual geometry grounded transformer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 2, 3, 5, 6, 9, 22 

- [11] Nikita Karaev, Yuri Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudolabelling real videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6013–6022, 2025. 2, 3, 8, 23, 26 

- [12] Grady Williams, Andrew Aldrich, and Evangelos A. Theodorou. Model predictive path integral control: From theory to parallel computation. _Journal of Guidance, Control, and Dynamics_ , 40(2):344–357, 2017. 2, 5, 21 

- [13] David Ha and J”urgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 2 

- [14] Chelsea Finn, Ian Goodfellow, and Sergey Levine. Unsupervised learning for physical interaction through video prediction. _Advances in neural information processing systems_ , 29, 2016. 2 

- [15] Alex X. Lee, Richard Zhang, Frederik Ebert, Pieter Abbeel, Chelsea Finn, and Sergey Levine. Stochastic adversarial video prediction. _arXiv preprint arXiv:1804.01523_ , 2018. 

- [16] Junhyuk Oh, Xiaoxiao Guo, Honglak Lee, Richard L. Lewis, and Satinder Singh. Action-conditional video prediction using deep networks in atari games. In _Advances in Neural Information Processing Systems_ , 2015. 

- [17] William Lotter, Gabriel Kreiman, and David Cox. Deep predictive coding networks for video prediction and unsupervised learning. _arXiv preprint arXiv:1605.08104_ , 2016. 

- [18] Emily Denton and Rob Fergus. Stochastic video generation with a learned prior. In _Proceedings of the 35th International Conference on Machine Learning_ , 2018. 

- [19] Wilson Yan, Yunzhi Zhang, Pieter Abbeel, and Aravind Srinivas. Videogpt: Video generation using vq-vae and transformers. _arXiv preprint arXiv:2104.10157_ , 2021. 

- [20] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J. Fleet. Video diffusion models. _arXiv preprint arXiv:2204.03458_ , 2022. 

- [21] Uriel Singer, Adam Polyak, Timothy Hayes, Sagie Benaim, Oron Gafni, Oron Ashual, Yuval Atzmon, Tomer Shalev, Devi Parikh, Yaniv Taigman, Ronen Banner, and Eliya Nachmani. Make-a-video: Text-to-video generation without textvideo data. _arXiv preprint arXiv:2209.14792_ , 2022. 

- [22] Jonathan Ho, William Chan, Carl Doersch, Suman Ravuri, David J. Fleet, Mohammad Norouzi, and Tim Salimans. Imagen video: High definition video generation with diffusion models. _arXiv preprint arXiv:2210.02303_ , 2022. 

- [23] Yuwei Guo, Zhiyu Chen, Chenyang Lei, Chengyue Gao, Fang Lu, and Yi Zhang. Animatediff: Animate your personalized text-to-image diffusion models without specific tuning. _arXiv preprint arXiv:2307.04725_ , 2023. 

- [24] Yichao Yin, Lei Qi, Hong Zhu, Jiakai Qin, Salman Khan, Luc Van Gool, Li Liu, and Philip Torr. Dynamicrafter: Animating open-domain images with video diffusion priors. _arXiv preprint arXiv:2310.12190_ , 2023. 

- [25] Jiajun Chen, Yu Li, Zhaohui Fan, Fan Zhang, Yu Qiao, and Bo Dai. Videocrafter2: Overcoming data limitations for high-quality video diffusion models. _arXiv preprint arXiv:2303.19712_ , 2023. 

- [26] Danila Kondratyuk, Uriel Singer, Willi Menapace, Reza Mahjourian, Xiaohua Zhai Sun, et al., and Agrim Gupta. Videopoet: A large language model for zero-shot video generation. _arXiv preprint arXiv:2312.14125_ , 2023. 

- [27] Andreas Blattmann, Willi Menapace, Yiyi He, Arash Vahdat, Robin Rombach, et al., and Agrim Gupta. Photorealistic video generation with diffusion models. _arXiv preprint arXiv:2312.06662_ , 2023. 

- [28] Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. Tesseract: learning 4d embodied world models. _arXiv preprint arXiv:2504.20995_ , 2025. 

- [29] Klemen Kotar, Wanhee Lee, Rahul Venkatesh, Honglin Chen, Daniel Bear, Jared Watrous, Simon Kim, Khai Loong Aw, Lilian Naing Chen, Stefan Stojanov, et al. World modeling with probabilistic structure integration. _arXiv preprint arXiv:2509.09737_ , 2025. 2 

- [30] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video. _arXiv preprint arXiv:2404.08471_ , 2024. 2 

- [31] Mahmoud Assran, Adrien Bardes, Xinlei Chen, Yann LeCun, et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 2, 4 

- [32] Peng Wang, Lingjie Liu, Yuan Liu, Christian Theobalt, Taku Komura, and Wenping Wang. Neus: Learning neural implicit surfaces by volume rendering for multi-view reconstruction. _arXiv preprint arXiv:2106.10689_ , 2021. 2 

- [33] Tobias Pfaff, Meire Fortunato, Alvaro Sanchez-Gonzalez, and Peter W. Battaglia. Learning mesh-based simulation with graph networks. _arXiv preprint arXiv:2010.03409_ , 2020. 3 

- [34] Alberta Longhini et al. Edo-net: Learning elastic properties of deformable objects from graph dynamics. _arXiv preprint arXiv:2209.08996_ , 2022. 

- [35] Hanxiao Jiang, Hao-Yu Hsu, Kaifeng Zhang, Hsin-Ni Yu, Shenlong Wang, and Yunzhu Li. Phystwin: Physicsinformed reconstruction and simulation of deformable objects from videos. _arXiv preprint arXiv:2503.17973_ , 2025. 3, 21 

- [36] Hongchi Xia, Entong Su, Marius Memmel, Arhan Jain, Raymond Yu, Numfor Mbiziwo-Tiapo, Ali Farhadi, Abhishek Gupta, Shenlong Wang, and Wei-Chiu Ma. Drawer: Digital 

13 

   - reconstruction and articulation with environment realism. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 21771–21782, 2025. 

- [37] Hongchi Xia, Zhi-Hao Lin, Wei-Chiu Ma, and Shenlong Wang. Video2game: Real-time interactive realistic and browser-compatible environment from a single video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 4578–4588, 2024. 

- [38] Haitao Qiu, Xiaoyu Zhou, Liyang Zhang, Jiaqi Yang, Kailun Zhou, et al. Physgen3d: Crafting a miniature interactive world from a single image. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 2 

- [39] Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _arXiv preprint arXiv:2003.08934_ , 2020. 2, 21 

- [40] Bernhard Kerbl, Georgios Kopanas, Thomas LeGendre, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Transactions on Graphics_ , 42(4), 2023. 21 

- [41] Danny Driess, Zhiao Huang, Yunzhu Li, Russ Tedrake, and Marc Toussaint. Learning multi-object dynamics with compositional neural radiance fields. In _Conference on robot learning_ , pages 1755–1768. PMLR, 2023. 

- [42] Jad Abou-Chakra et al. Physically embodied gaussian splatting: A realtime correctable world model for robotics. _arXiv preprint arXiv:2406.10788_ , 2024. 

- [43] Jad Abou-Chakra et al. Real-is-sim: Bridging the simto-real gap with a dynamic digital twin. _arXiv preprint arXiv:2504.03597_ , 2025. 

- [44] Tianyuan Zhang, Hong-Xing Yu, Rundi Wu, Brandon Y. Feng, Changxi Zheng, Noah Snavely, Jiajun Wu, and William T. Freeman. Physdreamer: Physics-based interaction with 3d objects via video generation. _arXiv preprint arXiv:2404.13026_ , 2024. 

- [45] Guanxing Lu, Baoxiong Jia, Puhao Li, et al. Gwm: Towards scalable gaussian world models for robotic manipulation. _arXiv preprint arXiv:2508.17600_ , 2025. 

- [46] Kaifeng Zhang, Shuo Sha, Hanxiao Jiang, Matthew Loper, Hyunjong Song, Guangyan Cai, Zhuo Xu, Xiaochen Hu, Changxi Zheng, and Yunzhu Li. Real-to-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. _arXiv preprint arXiv:2511.04665_ , 2025. 3 

- [47] Guangyuan Xiang, Juntong Wang, Linhan Qiu, Jing Yang, Zhihao Liu, Jiahui Zhang, Zhen Li, et al. Physgaussian: Physics-integrated 3d gaussians for generative dynamics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 

- [48] Zizhang Li, Hong-Xing Yu, Wei Liu, Yin Yang, Charles Herrmann, Gordon Wetzstein, and Jiajun Wu. Wonderplay: Dynamic 3d scene generation from a single image and actions. _arXiv preprint arXiv:2505.18151_ , 2025. 2 

- [49] Peter W. Battaglia, Razvan Pascanu, Matthew Lai, Danilo Rezende, and Koray Kavukcuoglu. Interaction networks for learning about objects, relations and physics. _arXiv preprint arXiv:1612.00222_ , 2016. 2, 3 

- [50] Alvaro Sanchez-Gonzalez, Jonathan Godwin, Tobias Pfaff, Rex Ying, Jure Leskovec, and Peter W. Battaglia. Learning to simulate complex physics with graph networks. _arXiv preprint arXiv:2002.09405_ , 2020. 

- [51] Jad Abou-Chakra et al. Particlenerf: A particle-based encoding for online neural radiance fields. _arXiv preprint arXiv:2211.04041_ , 2022. 

- [52] Suning Huang, Qianzhong Chen, Xiaohan Zhang, Jiankai Sun, and Mac Schwager. Particleformer: A 3d point cloud world model for multi-object, multi-material robotic manipulation. _arXiv preprint arXiv:2506.23126_ , 2025. 

- [53] Kaifeng Zhang, Baoyu Li, Kris Hauser, and Yunzhu Li. Particle-grid neural dynamics for learning deformable object models from rgb-d videos. _arXiv preprint arXiv:2506.15680_ , 2025. 3 

- [54] Kaifeng Zhang, Baoyu Li, Kris Hauser, and Yunzhu Li. Adaptigraph: Material-adaptive graph-based neural dynamics for robotic manipulation. _arXiv preprint arXiv:2407.07889_ , 2024. 3 

- [55] Zihao He, Bo Ai, Tongzhou Mu, Yulin Liu, Weikang Wan, Jiawei Fu, Yilun Du, Henrik I Christensen, and Hao Su. Scaling cross-embodiment world models for dexterous manipulation. _arXiv preprint arXiv:2511.01177_ , 2025. 

- [56] William F Whitney, Jacob Varley, Deepali Jain, Krzysztof Choromanski, Sumeet Singh, and Vikas Sindhwani. Modeling the real world with high-density visual particle dynamics. _arXiv preprint arXiv:2406.19800_ , 2024. 2 

- [57] Constructions Aeronautiques, Adele Howe, Craig Knoblock, ISI Drew McDermott, Ashwin Ram, Manuela Veloso, Daniel Weld, David Wilkins Sri, Anthony Barrett, Dave Christianson, et al. Pddl—the planning domain definition language. _Technical Report, Tech. Rep._ , 1998. 2 

- [58] Leslie Pack Kaelbling and Tomas´ Lozano-Perez.´ Hierarchical task and motion planning in the now. In _2011 IEEE international conference on robotics and automation_ , pages 1470–1477. IEEE, 2011. 3 

- [59] Jiayuan Mao, Chuang Gan, Pushmeet Kohli, Joshua B Tenenbaum, and Jiajun Wu. The neuro-symbolic concept learner: Interpreting scenes, words, and sentences from natural supervision. _arXiv preprint arXiv:1904.12584_ , 2019. 

- [60] Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 62(1):1–62, 2022. 

- [61] Eric Xing, Mingkai Deng, Jinyu Hou, and Zhiting Hu. Critiques of world models. _arXiv preprint arXiv:2507.05169_ , 2025. 

- [62] Hao Liu, Wilson Yan, Matei Zaharia, and Pieter Abbeel. World model on million-length video and language with blockwise ringattention. _arXiv preprint arXiv:2402.08268_ , 2024. 

- [63] Qineng Wang, Wenlong Huang, Yu Zhou, Hang Yin, Tianwei Bao, Jianwen Lyu, Weiyu Liu, Ruohan Zhang, Jiajun Wu, Li Fei-Fei, et al. Enact: Evaluating embodied cognition with world modeling of egocentric interaction. _arXiv preprint arXiv:2511.20937_ , 2025. 2 

- [64] Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning 

14 

latent dynamics for planning from pixels. _arXiv preprint arXiv:1811.04551_ , 2018. 2, 3 

- [65] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 21 

- [66] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 

- [67] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 2, 3 

- [68] Han Qi, Haocheng Yin, Aris Zhu, Yilun Du, and Heng Yang. Strengthening generative robot policies through predictive world modeling. _arXiv preprint arXiv:2502.00622_ , 2025. 

- [69] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 3 

- [70] Chenhao Li, Andreas Krause, and Marco Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics. _arXiv preprint arXiv:2501.10100_ , 2025. 2 

- [71] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 2 

- [72] Jensen Zhou, Hang Gao, Vikram Voleti, Aaryaman Vasishta, Chun-Han Yao, Mark Boss, Philip Torr, Christian Rupprecht, and Varun Jampani. Stable virtual camera: Generative view synthesis with diffusion models. _arXiv preprint arXiv:2503.14489_ , 2025. 

- [73] Hao He, Yinghao Xu, Yuwei Guo, Gordon Wetzstein, Bo Dai, Hongsheng Li, and Ceyuan Yang. Cameractrl: Enabling camera control for text-to-video generation. _arXiv preprint arXiv:2404.02101_ , 2024. 

- [74] Xianglong He, Chunli Peng, Zexiang Liu, Boyang Wang, Yifan Zhang, Qi Cui, Fei Kang, Biao Jiang, Mengyin An, Yangyang Ren, et al. Matrix-game 2.0: An open-source, real-time, and streaming interactive world model. _arXiv preprint arXiv:2508.13009_ , 2025. 

- [75] Jiaqi Li, Junshu Tang, Zhiyong Xu, Longhuang Wu, Yuan Zhou, Shuai Shao, Tianbao Yu, Zhiguo Cao, and Qinglin Lu. Hunyuan-gamecraft: High-dynamic interactive game video generation with hybrid history condition. _arXiv preprint_ , 2025. arXiv preprint. 

- [76] Guangcong Zheng, Teng Li, Rui Jiang, Yehao Lu, Tao Wu, and Xi Li. Cami2v: Camera-controlled image-to-video diffusion model. _arXiv preprint arXiv:2410.15957_ , 2024. 

- [77] Chonghyuk Song, Michal Stary, Boyuan Chen, George Kopanas, and Vincent Sitzmann. Generative view stitching. _arXiv preprint arXiv:2510.24718_ , 2025. 

- [78] Siyuan Zhou, Yilun Du, Yuncong Yang, Lei Han, Peihao Chen, Dit-Yan Yeung, and Chuang Gan. Learning 3d persistent embodied world models. _arXiv preprint arXiv:2505.05495_ , 2025. 2 

- [79] Sherry Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Leslie Kaelbling, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 2 

- [80] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 4 

- [81] Hassan Abu Alhaija, Jose Alvarez, Maciej Bala, Tiffany Cai, Tianshi Cao, Liz Cha, Joshua Chen, Mike Chen, Francesco Ferroni, Sanja Fidler, et al. Cosmos-transfer1: Conditional world generation with adaptive multimodal control. _arXiv preprint arXiv:2503.14492_ , 2025. 

- [82] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia, Zongyu Lin, Loic Magne, Avnish Narayan, You Liang Tan, Guanzhi Wang, Qi Wang, Jiannan Xiang, Yinzhen Xu, Seonghyeon Ye, Jan Kautz, Furong Huang, Yuke Zhu, and Linxi Fan. Flare: Robot learning with implicit world modeling. _arXiv preprint arXiv:2505.15659_ , 2025. 

- [83] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, Loic Magne, Ajay Mandlekar, Avnish Narayan, You Liang Tan, Guanzhi Wang, Jing Wang, Qi Wang, Yinzhen Xu, Xiaohui Zeng, Kaiyuan Zheng, Ruijie Zheng, Ming-Yu Liu, Luke Zettlemoyer, Dieter Fox, Jan Kautz, Scott Reed, Yuke Zhu, and Linxi Fan. Dreamgen: Unlocking generalization in robot learning through video world models. _arXiv preprint arXiv:2505.12705_ , 2025. 2 

- [84] Ryan Burgert, Yuancheng Xu, Wenqi Xian, Oliver Pilarski, Pascal Clausen, Mingming He, Li Ma, Yitong Deng, Lingxiao Li, Mohsen Mousavi, et al. Go-with-the-flow: Motioncontrollable video diffusion models using real-time warped noise. _arXiv preprint arXiv:2501.08331_ , 2025. 2 

- [85] Muyao Niu, Xiaodong Cun, Xintao Wang, Yong Zhang, Ying Shan, and Yinqiang Zheng. Mofa-video: Controllable image animation via generative motion field adaptions in frozen image-to-video diffusion model. _arXiv preprint arXiv:2405.20222_ , 2024. 

- [86] Daniel Geng, Charles Herrmann, Junhwa Hur, Forrester Cole, Serena Zhang, Tobias Pfaff, Tatiana Lopez-Guevara, Carl Doersch, Yusuf Aytar, Michael Rubinstein, et al. Motion prompting: Controlling video generation with motion trajectories. _arXiv preprint arXiv:2412.02700_ , 2024. 

- [87] Nate Gillman, Charles Herrmann, Michael Freeman, Daksh Aggarwal, Evan Luo, Deqing Sun, and Chen Sun. Force prompting: Video generation models can learn and generalize physics-based control signals. _arXiv preprint_ , 2025. arXiv preprint. 

- [88] Li Hu, Xin Gao, Peng Zhang, Ke Sun, Bang Zhang, and Liefeng Bo. Animate anyone: Consistent and controllable image-to-video synthesis for character animation. _arXiv preprint arXiv:2311.17117_ , 2023. 

- [89] Xiaoyu Shi, Zhaoyang Huang, Fu-Yun Wang, Weikang Bian, Dasong Li, Yi Zhang, Manyuan Zhang, Ka Chun Cheung, Simon See, Hongwei Qin, et al. Motion-i2v: Consistent and 

15 

   - controllable image-to-video generation with explicit motion modeling. In _ACM SIGGRAPH Conference Papers_ , 2024. 

- [90] Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li, Tianshui Chen, Menghan Xia, Ping Li, Ping Luo, and Ying Shan. Motionctrl: A unified and flexible motion controller for video generation. In _ACM SIGGRAPH Conference Papers_ , 2024. 

- [91] Weijia Wu, Zhuang Li, Yuchao Gu, Rui Zhao, Yefei He, David Junhao Zhang, Mike Zheng Shou, Yan Li, Tingting Gao, and Di Zhang. Draganything: Motion control for anything using entity representation. In _European Conference on Computer Vision_ , 2024. 

- [92] Shengming Yin, Chenfei Wu, Jian Liang, Jie Shi, Houqiang Li, Gong Ming, and Nan Duan. Dragnuwa: Fine-grained control in video generation by integrating text, image, and trajectory. _arXiv preprint arXiv:2308.08089_ , 2023. 

- [93] Zhenghao Zhang, Junchao Liao, Menghao Li, Zuozhuo Dai, Bingxue Qiu, Siyu Zhu, Long Qin, and Weizhi Wang. Tora: Trajectory-oriented diffusion transformer for video generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 

- [94] Jinbo Xing, Hanyuan Liu, Menghan Xia, Yong Zhang, Xintao Wang, Ying Shan, and Tien-Tsin Wong. Tooncrafter: Generative cartoon interpolation. _ACM Transactions on Graphics_ , 2024. 2 

- [95] Pieter-Tjerk de Boer, Dirk P. Kroese, Shie Mannor, and Reuven Y. Rubinstein. A tutorial on the cross-entropy method. _Annals of Operations Research_ , 134(1):19–67, 2005. 2 

- [96] Matthew Kelly. An introduction to trajectory optimization: How to do your own direct collocation. _SIAM Review_ , 59 (4):849–904, 2017. 

- [97] Joelle Pineau, Geoffrey Gordon, and Sebastian Thrun. Pointbased value iteration: An anytime algorithm for pomdps. In _Proceedings of the 18th International Joint Conference on Artificial Intelligence (IJCAI)_ , 2003. 2 

- [98] Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. _arXiv preprint arXiv:1906.08253_ , 2019. 2, 3 

- [99] Kurtland Chua, Roberto Calandra, Rowan McAllister, and Sergey Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. _arXiv preprint arXiv:1805.12114_ , 2018. 

- [100] Danijar Hafner, Wilson Yan, and Timothy Lillicrap. Training agents inside of scalable world models. _arXiv preprint arXiv:2509.24527_ , 2025. 2, 3 

- [101] Pulkit Agrawal, Ashvin V Nair, Pieter Abbeel, Jitendra Malik, and Sergey Levine. Learning to poke by poking: Experiential learning of intuitive physics. _Advances in neural information processing systems_ , 29, 2016. 2 

- [102] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 

- [103] Jie Zhang, Yilun Du, et al. Learning to act from actionless videos through dense correspondences. _arXiv preprint arXiv:2310.08576_ , 2023. 2, 3 

- [104] Erwin Coumans. Bullet physics simulation. In _ACM SIGGRAPH 2015 Courses_ , 2015. 3 

- [105] Russ Tedrake and the Drake Development Team. Drake: A planning, control, and analysis toolbox for nonlinear systems. Technical Report, MIT CSAIL, https://drake. mit.edu, 2019. 3 

- [106] Viktor Makoviychuk, Ilya Wawrzyniak, Sergii Gupta, Anurag Narang, Maciej Kayastha, Yashraj Henry, Guanyang Li, Igor Ling, Andreas Merentitis, Alexey Makoviychuk, Kaichun Tsai, Gabe State, Dieter Fox, and Ankur Handa. Isaac gym: High performance gpu based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [107] Nathan Koenig and Andrew Howard. Design and use paradigms for gazebo, an open-source multi-robot simulator. In _2004 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2149–2154, 2004. 

- [108] Yuanming Hu, Luke Anderson, Tzu-Mao Li, Qi Sun, Nathan Carr, Jonathan Ragan-Kelley, and Fredo Durand.´ Difftaichi: Differentiable programming for physical simulation. _arXiv preprint arXiv:1910.00935_ , 2020. 3 

- [109] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ , pages 2226–2240. PMLR, 2023. 3 

- [110] Xue Bin Peng, Marcin Andrychowicz, Wojciech Zaremba, and Pieter Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3803– 3810. IEEE, 2018. 3 

- [111] OpenAI: Marcin Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew, Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, et al. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research_ , 39(1):3–20, 2020. 

- [112] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. _arXiv preprint arXiv:2107.04034_ , 2021. 3 

- [113] Tomas Lozano-Perez. Spatial planning: A configuration space approach. _IEEE transactions on computers_ , 32(02): 108–120, 1983. 3 

- [114] Leslie Pack Kaelbling, Michael L Littman, and Anthony R Cassandra. Planning and acting in partially observable stochastic domains. _Artificial intelligence_ , 101(1-2):99–134, 1998. 3 

- [115] Marc Toussaint. Logic-geometric programming: An optimization-based approach to combined task and motion planning. In _IJCAI_ , pages 1930–1936, 2015. 

- [116] Tobia Marcucci, Jack Umenberger, Pablo Parrilo, and Russ Tedrake. Shortest paths in graphs of convex sets. _SIAM Journal on Optimization_ , 34(1):507–532, 2024. 3 

- [117] Deepak Pathak, Pulkit Agrawal, Alexei A Efros, and Trevor Darrell. Curiosity-driven exploration by self-supervised prediction. In _International conference on machine learning_ , pages 2778–2787. PMLR, 2017. 3 

- [118] Ramanan Sekar, Oleh Rybkin, Kostas Daniilidis, Pieter Abbeel, Danijar Hafner, and Deepak Pathak. Planning to explore via self-supervised world models. In _International_ 

16 

_conference on machine learning_ , pages 8583–8592. PMLR, 2020. 

- [119] Igor Mordatch and Emo Todorov. Combining the benefits of function approximation and trajectory optimization. In _Robotics: Science and Systems_ , page 23, 2014. 

- [120] Maximilian Du and Shuran Song. Dynaguide: Steering diffusion polices with active dynamic guidance. _arXiv preprint arXiv:2506.13922_ , 2025. 3 

- [121] Aaron D Ames, Samuel Coogan, Magnus Egerstedt, Gennaro Notomista, Koushil Sreenath, and Paulo Tabuada. Control barrier functions: Theory and applications. In _2019 18th European control conference (ECC)_ , pages 3420–3431. Ieee, 2019. 3 

- [122] Zhanyi Sun and Shuran Song. Latent policy barrier: Learning robust visuomotor policies by staying in-distribution. _arXiv preprint arXiv:2508.05941_ , 2025. 3 

- [123] Alexandre Donze. Breach, a toolbox for verification and parameter synthesis of hybrid systems. In _Computer Aided Verification_ , pages 167–170. Springer, 2010. 3 

- [124] Xiaomeng Xu, Huy Ha, and Shuran Song. Dynamics-guided diffusion model for robot manipulator design. _CoRR_ , 2024. 3 

- [125] Jose Barreiros, Andrew Beaulieu, Aditya Bhat, Rick Cory, Eric Cousineau, Hongkai Dai, Ching-Hsin Fang, Kunimatsu Hashimoto, Muhammad Zubair Irshad, Masha Itkina, et al. A careful examination of large behavior models for multitask dexterous manipulation. _arXiv preprint arXiv:2507.05331_ , 2025. 3, 8 

- [126] Sherry Yang et al. Evaluating robot policies in a world model. _arXiv preprint arXiv:2506.00613_ , 2025. 

- [127] Gemini Robotics Team, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, Abhishek Jindal, Thomas Kipf, Sean Kirmani, Fangchen Liu, Anirudha Majumdar, et al. Evaluating gemini robotics policies in a veo world simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 3 

- [128] Yuang Wang, Chao Wen, Haoyu Guo, Sida Peng, Minghan Qin, Hujun Bao, Xiaowei Zhou, and Ruizhen Hu. Precise action-to-video generation through visual action prompts. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 12713–12724, 2025. 3 

- [129] Haonan Chen, Yilong Niu, Kaiwen Hong, Shuijing Liu, Yixuan Wang, Yunzhu Li, and Katherine Rose Driggs-Campbell. Predicting object interactions with behavior primitives: An application in stowing tasks. In _7th Annual Conference on Robot Learning_ , 2023. 3 

- [130] D. Sulsky, Z. Chen, and H. L. Schreyer. A particle method for history-dependent materials. Technical report, U.S. Department of Energy, OSTI, 1993. 3 

- [131] Carl Doersch, Pauline Luc, Yi Yang, Dilara Gokay, Skanda Koppula, Ankush Gupta, Joseph Heyward, Ignacio Rocco, Ross Goroshin, Joao Carreira, et al. Bootstap: Bootstrapped training for tracking-any-point. In _Proceedings of the Asian Conference on Computer Vision_ , pages 3257–3274, 2024. 3 

- [132] Yuxi Xiao, Qianqian Wang, Shangzhan Zhang, Nan Xue, Sida Peng, Yujun Shen, and Xiaowei Zhou. Spatialtracker: Tracking any 2d pixels in 3d space. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 20406–20417, 2024. 3 

- [133] Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2023. 3 

- [134] Siddhant Haldar and Lerrel Pinto. Point policy: Unifying observations and actions with key points for robot manipulation. _arXiv preprint arXiv:2502.20391_ , 2025. 

- [135] Thomas Weng, Sujay Bajracharya, Yufei Wang, Khush Agrawal, and David Held. Fabricflownet: Bimanual cloth manipulation with a flow-based policy. _arXiv preprint arXiv:2111.05623_ , 2021. 

- [136] Daniel Seita, Yufei Wang, Sarthak J Shetty, Edward Yao Li, Zackory Erickson, and David Held. Toolflownet: Robotic manipulation with tools via predicting tool flow from point clouds. _arXiv preprint arXiv:2211.09006_ , 2022. 

- [137] Shengjie Wang, Jiacheng You, Yihang Hu, Jiongye Li, and Yang Gao. Skil: Semantic keypoint imitation learning for generalizable data-efficient manipulation. In _Robotics: Science and Systems (RSS)_ , 2025. 

- [138] Jun Guo, Xiaojian Ma, Yikai Wang, Min Yang, Huaping Liu, and Qing Li. Flowdreamer: A rgb-d world model with flow-based motion representations for robot manipulation. _arXiv preprint arXiv:2505.10075_ , 2025. 

- [139] Bardienus P. Duisterhof, Zhao Mandi, Yunchao Yao, JiaWei Liu, Jenny Seidenschwarz, Mike Zheng Shou, Deva Ramanan, Shuran Song, Stan Birchfield, Bowen Wen, and Jeffrey Ichnowski. Deformgs: Scene flow in highly deformable scenes for deformable object manipulation. _arXiv preprint arXiv:2312.00583_ , 2024. 

- [140] Zhao-Heng Yin, Sherry Yang, and Pieter Abbeel. Objectcentric 3d motion field for robot learning from human videos. _arXiv preprint arXiv:2506.04227_ , 2025. 3 

- [141] Mengda Xu, Zhenjia Xu, Yinghao Xu, Cheng Chi, Gordon Wetzstein, Manuela Veloso, and Shuran Song. Flow as the cross-domain manipulation interface. _arXiv preprint arXiv:2407.15208_ , 2024. 3 

- [142] Shivansh Patel, Xinchen Yin, Wenlong Huang, Shubham Garg, Hooshang Nayyeri, Li Fei-Fei, Svetlana Lazebnik, and Yunzhu Li. A real-to-sim-to-real approach to robotic manipulation with vlm-generated iterative keypoint rewards. _arXiv preprint arXiv:2502.08643_ , 2025. 

- [143] Irmak Guzey, Yinlong Dai, Georgy Savva, Raunaq Bhirangi, and Lerrel Pinto. Bridging the human to robot dexterity gap through object-oriented rewards. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3344–3351. IEEE, 2025. 

- [144] Junyao Shi, Joshua Smith, Jianing Qian, and Dinesh Jayaraman. Points2reward: Robotic manipulation rewards from just one video. 2025. 3 

- [145] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. _arXiv preprint arXiv:2409.01652_ , 2024. 3, 5, 21 

- [146] Ben Eisner, Harry Zhang, and David Held. Flowbot3d: Learning 3d articulation flow to manipulate articulated objects. In _Robotics: Science and Systems (RSS)_ , 2022. 3 

- [147] Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2act: Predicting point tracks 

17 

from internet videos enables generalizable robot manipulation. In _European Conference on Computer Vision_ , pages 306–324. Springer, 2024. 

- [148] Shivansh Patel, Shraddhaa Mohan, Hanlin Mai, Unnat Jain, Svetlana Lazebnik, and Yunzhu Li. Robotic manipulation by imitating generated videos without physical demonstrations. _arXiv preprint arXiv:2507.00990_ , 2025. 

- [149] Hongyu Li, Lingfeng Sun, Yafei Hu, Duy Ta, Jennifer Barry, George Konidaris, and Jiahui Fu. Novaflow: Zero-shot manipulation via actionable flow from generated videos. _arXiv preprint arXiv:2510.08568_ , 2025. 

- [150] Karthik Dharmarajan, Wenlong Huang, Ruohan Zhang, Jiajun Wu, and Li Fei-Fei. Dream2flow: Bridging video generation and open-world manipulation with 3d object flow, 2025. Preprint. 3 

- [151] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 3 

- [152] Xiaoyang Wu, Li Jiang, Peng-Shuai Wang, Zhijian Liu, Xihui Liu, Yu Qiao, Wanli Ouyang, Tong He, and Hengshuang Zhao. Point transformer v3: Simpler, faster, stronger. _arXiv preprint arXiv:2312.10035_ , 2023. 4, 8, 9 

- [153] Oriane Simeoni, Huy V. Vo, Maximilian Seitzer, Federico´ Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michael¨ Ramamonjisoa, Francisco Massa, Daniel Haziza, Luca Wehrstedt, Jianyuan Wang, Timothee Darcet, Th´ eo Moutakanni, Leonel Sentana,´ Claire Roberts, Andrea Vedaldi, Jamie Tolan, John Brandt, Camille Couprie, Julien Mairal, Herve´ Jegou,´ Patrick Labatut, and Piotr Bojanowski. Dinov3. _arXiv preprint arXiv:2508.10104_ , 2025. 4, 9 

- [154] Bardienus P. Duisterhof, Jan Oberst, Bowen Wen, Stan Birchfield, Deva Ramanan, and Jeffrey Ichnowski. Rayst3r: Predicting novel depth maps for zero-shot object completion. _arXiv preprint arXiv:2506.05285_ , 2025. 4 

- [155] Alex Kendall and Yarin Gal. What uncertainties do we need in bayesian deep learning for computer vision? _Advances in neural information processing systems_ , 30, 2017. 5 

- [156] David Novotny, Diane Larlus, and Andrea Vedaldi. Learning 3d object categories by looking around them. In _Proceedings of the IEEE international conference on computer vision_ , pages 5218–5227, 2017. 5 

- [157] Brent Yi, Chung Min Kim, Justin Kerr, Gina Wu, Rebecca Feng, Anthony Zhang, Jonas Kulhanek, Hongsuk Choi, Yi Ma, Matthew Tancik, and Angjoo Kanazawa. Viser: Imperative, web-based 3d visualization in python, 2025. 7 

- [158] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 6 

- [159] Zhuang Liu, Hanzi Mao, Chao-Yuan Wu, Christoph Feichtenhofer, Trevor Darrell, and Saining Xie. A convnet for the 2020s. In _Proceedings of the IEEE/CVF conference on com-_ 

_puter vision and pattern recognition_ , pages 11976–11986, 2022. 8 

- [160] Xiaoyang Wu, Daniel DeTone, Duncan Frost, Tianwei Shen, Chris Xie, Nan Yang, Jakob Engel, Richard Newcombe, Hengshuang Zhao, and Julian Straub. Sonata: Selfsupervised learning of reliable point representations. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2025. 8, 9 

- [161] Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 652–660, 2017. 9 

- [162] Charles Ruizhongtai Qi, Li Yi, Hao Su, and Leonidas J Guibas. Pointnet++: Deep hierarchical feature learning on point sets in a metric space. _Advances in neural information processing systems_ , 30, 2017. 9 

- [163] Spconv Contributors. Spconv: Spatially sparse convolution library. https://github.com/traveller59/ spconv, 2022. 9 

- [164] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 9 

- [165] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeff Wu, and Dario Amodei. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ , 2020. 9, 11 

- [166] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. Palm: Scaling language modeling with pathways. In _International Conference on Machine Learning_ , 2022. 

- [167] Jean-Baptiste Alayrac, Dustin Donato, Antoine Ortega, Jacob Menick, Aidan Clark, et al. Flamingo: a visual language model for few-shot learning. _arXiv preprint arXiv:2204.14198_ , 2022. 11 

- [168] Pieter Abbeel and Andrew Y Ng. Apprenticeship learning via inverse reinforcement learning. In _Proceedings of the twenty-first international conference on Machine learning_ , page 1, 2004. 21 

- [169] Sizhe Lester Li, Annan Zhang, Boyuan Chen, Hanna Matusik, Chao Liu, Daniela Rus, and Vincent Sitzmann. Controlling diverse robots by inferring jacobian fields with deep networks. _Nature_ , pages 1–7, 2025. 21 

- [170] Martin Ester, Hans-Peter Kriegel, Jorg Sander, and Xiaowei¨ Xu. A density-based algorithm for discovering clusters in large spatial databases with noise. In _Proceedings of the Second International Conference on Knowledge Discovery and Data Mining_ , pages 226–231, 1996. 23 

- [171] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 30 

18 

- [172] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. _arXiv preprint arXiv:2402.10329_ , 2024. 30 

- [173] Yifeng Zhu, Abhishek Joshi, Peter Stone, and Yuke Zhu. Viola: Imitation learning for vision-based manipulation with object proposal priors. _arXiv preprint arXiv:2210.11339_ , 2022. 30 

- [174] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Radle, Chloe Rolland, Laura Gustafson, Eric Mintun, Junt-¨ ing Pan, Kalyan Vasudev Alwala, Nicolas Carion, ChaoYuan Wu, Ross Girshick, Piotr Dollar, and Christoph Feicht-´ enhofer. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ , 2024. 30 

- [175] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 30 

19 

# **A. Appendix** 

# **Appendix Contents** 

|A.1. Extended Discussions on Limitations . .|.|.|21|
|---|---|---|---|
|A.2. DROID 3D Annotation Pipeline . . . . .|.|.|22|
|A.2.1. Depth Estimation<br>. . . . . . . .|.|.|22|
|A.2.2. Camera Pose Estimation . . . . .|.|.|22|
|A.2.3. Benchmark Metrics for 3D Annota|ti|on|23|
|A.2.4. Occlusion-Aware Tracking in 3D|.|.|23|
|A.3. BEHAVIOR-1K Data Generation . . . .|.|.|24|
|A.3.1. Dataset Replay . . . . . . . . . .|.|.|24|
|A.3.2. Clip Filtering . . . . . . . . . . .|.|.|24|
|A.3.3. 3D Point Flows from Simulation|.|.|24|
|A.4. Model Training Details . . . . . . . . . .|.|.|26|
|A.5. DROID Evaluation Protocol . . . . . . .|.|.|29|
|A.6. Real-Robot Experiment Details<br>. . . . .|.|.|30|
|A.6.1. Model-Based Planning . . . . . .|.|.|30|
|A.6.2. Task Specification . . . . . . . .|.|.|30|
|A.6.3. Evaluation Protocol<br>. . . . . . .|.|.|30|
|A.6.4. Effect of Training Mixture . . . .|.|.|30|
|A.7. Additional 3D Annotation Examples. . .|.|.|31|
|A.8. Additional Model Rollouts . . . . . . . .|.|.|33|


20 

## **A.1. Extended Discussions on Limitations** 

**Static Initial State.** The model takes as input RGB-D point cloud together with a finite-horizon sequence of robot actions and predicts how points will move in response. Because no prior frames or velocities are provided, this formulation assumes that the world is static at the observation instant. Supporting fully dynamic initial conditions would require augmenting the input with externally tracked trajectories or recurrent state, which we leave as future work. 

**Reward/Cost Specification for Action Inference.** In this work, we explore POINTWORLD’s use case for action inference in manipulation by integrating it with a sampling-based planner, MPPI [12], which requires an explicit specification of reward/cost functions in the same state-action space of 3D point flows. For the scope of this work, we restrict ourselves to manual specification (e.g., moving a subset of points to target locations). Future work may consider automatically specifying (single or multi-stage) reward via vision-language models [145], or inferring reward from demonstrations using inverse reinforcement learning [168], while keeping POINTWORLD as the dynamics function. In addition to planning, action inference can also be alternatively performed by learning a parameterized policy by interacting with the model as the environment via reinforcement learning [65]. 

**Fine-Scale Objects and Calibration Noise.** Thin or very small objects (e.g., pens or cables) are challenging to annotate accurately in 3D: modest depth or extrinsic errors can be comparable to the object thickness and lead to ambiguous separation between robot and scene points during groundtruth annotation. In such scenarios, mis-registrations in the ground-truth flows propagate into training and can cause the model to confuse overlapping motions between the gripper and nearby scene points. Improved calibration and depth estimation could strengthen supervision for these fine-grained interactions. 

**Correlation vs. Causation.** Given an observed context frame and a sequence of robot actions, POINTWORLD is trained to predict the subsequent sequence of scene states. As such, it primarily captures correlations present in the training distribution between robot actions, robot motion, and observed scene evolution. In settings where exogenous factors (such as other agents or environment changes not controlled by the robot) also influence the future, these influences are entangled with the robot-induced effects in the data and are not disentangled as separate causal mechanisms. Our experiments therefore evaluate predictive fidelity and planning performance under the observed action-conditioned distribution, rather than claiming to recover the underlying causal structure of the environment. 

**Lack of Photometric Dynamics.** POINTWORLD only outputs displacements of 3D points captured from RGB-D inputs, which focus on geometry and physical interactions rather than appearance. While often visually plausible when rendered as point clouds, it is insufficient if one desires to reason about photometric changes of the environment caused by the robot actions, such as lights or screens turning on and off. Combining POINTWORLD with appearance models that predict emitted radiance, such as those from Gaussian Splatting [40] or Neural Radiance Fields [39], may be necessary for tasks where such photometric dynamics are critical. 

**Rigid-Body Robot Assumption.** Robot embodiment is represented as a kinematic tree of rigid links, and we propagate a fixed set of robot surface points by forward kinematics. This ignores deformations of soft, tendon-driven, or compliant structures (e.g., fin-ray grippers) and non-rigid effects of the robot body. As a result, POINTWORLD reasons only about how the scene moves in response to a forecasted robot geometry, rather than how contact may reshape the robot itself. Extending the representation to include deformable links [169] would enable reasoning about how contact deforms the robot body and how those deformations, in turn, affect contact geometry. 

**Actuation and Tracking Assumptions.** Our formulation treats the robot trajectory as a known, _fully realized_ sequence of joint configurations and uses forward kinematics to construct robot flows. As a result, POINTWORLD effectively models “what the environment does if the robot body follows this path,” rather than “whether and how the robot will actually realize this path” under a particular controller, actuation limits, or contact-induced tracking errors. This quasi-static, kinematic view of the robot action representation can break down for underactuated or compliant joints (e.g., tendondriven or compliant hand fingers), or when strong contacts, payloads, or controller changes induce large tracking errors. Extending the method to jointly reason about robot and scene dynamics is an important avenue for future work. 

**Lack of Explicit Physics Priors.** The current formulation is purely data-driven and does not incorporate explicit physics priors such as Newtonian mechanics or conservationlaw constraints, to provide a focused study on scaling 3D world models without priors of objectness and of their material and physical properties. Despite this, we observe that POINTWORLD captures many aspects of rigid, articulated, and deformable behavior from data alone. Incorporating physics-informed regularization or hybrid simulators [35] could further improve generalization and extrapolation, particularly in regimes that in-domain interaction data can be collected for accurate scene/object reconstruction, not only for their geometries but also for their physics parameters. 

21 

## **A.2. DROID 3D Annotation Pipeline** 

DROID [7] is a large-scale robot manipulation dataset with human-teleoperated interactions collected with a wristmounted camera and two externally-mounted cameras (randomized over the left and right sides of the workspace). We use all DROID episodes for which raw camera streams are available, irrespective of task success or failure, since 3D world modeling depends only on the observed interactions rather than the task-specific outcomes of the manipulation. Each episode provides stereo RGB streams with groundtruth camera intrinsics for all three cameras, plus robot joint states and a known kinematic model of the robot. In this work, we use the recovered 3D scene flows from the two externally-mounted cameras. All data share a synchronized timestamp. We augment the robot model to include the Robotiq 2F-85 gripper and the custom camera mount used in the standardized DROID setup. For each scene, the pipeline aligns timestamps to a reference stream (binary search to nearest), downsamples by 2, then runs: (i) dense metric depth; (ii) external-camera extrinsic refinement by aligning rendered robot mesh to observed depth; (iii) 2D tracking under workspace and robot masks; (iv) 3D trajectory reconstruction, slicing, and postprocessing. Note that we do not store robot point flows because those can be reconstructed efficiently at training/inference time given known robot URDF and the given joint actions. 

### **A.2.1. Depth Estimation** 

Per-view metric depth is obtained using a high-quality stereo estimator, FoundationStereo [9]. Note that unlike typical sensor depth, the estimated depth from FoundationStereo does not have a minimum depth threshold for valid depth perception. However, it is still observed that its estimated depth can be inaccurate for distant, especially texture-less, regions (such as walls). Therefore, depth values are sanitized by clamping to a trusted range [0 _,_ 4] m and producing a perpixel validity mask, which is also propagated to 3D points as a per-point depth-valid flag. 

### **A.2.2. Camera Pose Estimation** 

We do not use dataset-provided extrinsics. Instead, we compute camera extrinsics using a two-stage procedure that leverages the accurate metric depth obtained from FoundationStereo discussed previously. First, we initialize the camera pose estimates using VGGT [10]. Second, we refine all camera poses of the two external cameras from all timesteps jointly by aligning rendered robot geometry to observed depth using the recorded robot joint states. 

**Camera Pose Initialization.** Our goal is to estimate, for each externally mounted camera _Ci_ , a single rigid transform _TCi←B ∈_ SE(3) that maps 3D points from the robot base frame _B_ into the camera frame and is fixed throughout a 

DROID episode. We denote the robot base frame by _B_ , the wrist camera frame at time _t_ by _Wt_ , and the external cameras by _Ci_ . A multi-view pose estimator (VGGT [10]) is applied to time-aligned images from the two external cameras and the wrist camera; it treats the first external camera at an initial timestep as the reference frame, and returns rigid transforms _TE_ 0 _←Ci_ and _TE_ 0 _←Wt_ that map points from each camera _Ci_ or _Wt_ into this reference frame _E_ 0. Independently, forward kinematics applied to the robot joint states provide the pose of the gripper in the base frame, _TGt←B_ . For each physical robot (given by the recorded robot serial), we assume that the wrist camera is rigidly mounted relative to the end effector and reused across all episodes. We empirically found that this assumption is largely valid for robots used in DROID as the averaged transforms exhibit sub-millimeter alignment error with each other. Under this assumption, we can obtain a known gripper-to-wrist transform _TW ←G_ for each robot. Using this transform and the forward-kinematics model, we obtain a time-varying wrist pose in the base frame, 


Combining this with the estimator’s transform between the wrist and the reference external camera yields per-frame estimates of the reference camera pose in the base frame, 


which we average over all valid wrist frames to obtain a single _TE_ 0 _←B_ . For any other external camera _Ci_ , the estimator provides a relative transform _TE_ 0 _←Ci_ . We convert this to a base-frame extrinsic 


so that all external cameras are expressed in the same robot base frame before the refinement stage. 

**Camera Pose Refinement.** Starting from the initialized base-frame extrinsics _TCi←B_ , we jointly refine the poses of all external cameras using robot-depth reprojection. Let external cameras be indexed by _i_ , timesteps by _t_ , and let _k_ index valid robot pixels after filtering (in front of the camera, within image bounds, deduplicated in the image plane, and with observed depth in the trusted range). For each camera _i_ we optimize a small 6-DoF update on top of the initialization, parameterized by translation and rotation and scaled such that optimization can be done within a good numerical range. Given an observed depth value _d_<sup>obs</sup> _i,t,k_<sup>at a valid robot pixel</sup> and the corresponding predicted depth _d_<sup>pred</sup> _i,t,k_<sup>obtainedby</sup> projecting robot surface points from the base frame through the current extrinsics _TCi←B_ , we define the robot-depth reprojection loss 


22 

where the sum runs over all valid robot pixels across cameras and frames and _K_ is their total count. We optimize the 6- DoF updates for all external cameras jointly using a firstorder optimizer (100 iterations, learning rate 10<sup>_−_3</sup> ), and restrict supervision to robot pixels whose observed depth lies in a trusted range of [0 _._ 3 _,_ 2 _._ 0] m. To ensure reliable gradients, we further require that each camera–frame pair contributes at least 2 _,_ 000 valid robot points; frames that fail this criterion for any external camera are discarded before refinement. With these procedures, we can accurately label camera poses for around 60% of all episodes recorded in DROID. Quantitative metrics are reported in the main text. 

### **A.2.3. Benchmark Metrics for 3D Annotation** 

**Depth Reprojection.** For each scene and calibration variant, we render the robot mesh into each external camera using the candidate extrinsics and recorded joint states, discard depth outside [0 _._ 3 _,_ 2 _._ 0] m or out-of-bounds robot pixels, and compute an L1 depth reprojection loss over valid robot pixels. The per-frame losses are averaged over valid pixels and frames to produce a point-weighted value reported per scene and then aggregated into cumulative curves. 

**Two-view F1 @ 5/20 mm.** For each external camera, we back-project valid depth into 3D using corresponding intrinsics/extrinsics, remove robot pixels, and crop to workspace. Given the resulting paired point clouds, we compute precision, recall, and F1 via symmetric nearest-neighbor matching: a point in cloud A (resp. B) is a true positive if its nearest neighbor in B (resp. A) lies within the threshold (5 mm or 20 mm); otherwise it contributes to the false-positive/falsenegative count. Metrics are accumulated over frames, normalized by the number of valid points per view, and then aggregated per scene into the cumulative counts shown in Figure 5. Scenes with missing depth/extrinsics for a given combo are omitted from evaluation for that combo. 

### **A.2.4. Occlusion-Aware Tracking in 3D** 

Given depth and camera poses, we herein describe how we can obtain 3D point flows. We describe the following in order: (i) filtering clips based on robot motion, (ii) tracking visible points within each retained clip, and (iii) postprocessing the resulting 3D trajectories. 

**Clip Filtering.** We slice each episode into overlapping clips of length _F_ =16 frames with stride _s_ =1. Each clip covers approximately one second of the episode. Clips are retained if either the gripper changes state within the clip or end-effector motion exceeds thresholds. Thresholds depend on whether the gripper is predominantly open or closed within the clip: position/rotation thresholds are (0 _._ 005 m _,_ 0 _._ 10 rad) when open and (0 _._ 002 m _,_ 0 _._ 05 rad) when closed; either exceeding suffices to keep a clip, and any change in gripper state also keeps the clip. 

**Tracking.** After obtaining depth and camera poses and slicing episodes into short clips, we perform dense tracking to obtain 3D scene flows on a per-clip basis. Clips cover roughly one-second windows and, depending on where they fall within a longer episode, may observe quite different regions of the workspace; tracking after clip selection ensures that each clip has its own consistent set of tracked regions and avoids mixing trajectories across widely separated time intervals. To improve efficiency and robustness, we perform tracking restricted to workspace and non-robot regions. To construct the workspace mask, we project a fixed 3D workspace volume to the image. To construct the non-robot mask, we render the robot’s URDF and project the mesh to the image plane. We then track 2D points using 2D point trackers (CoTracker3 [11]) on the masked regions only, producing dense 2D trajectories. The tracker also outputs a per-point visibility mask over time; we store this visibility for each 2D trajectory so that occluded points can later be excluded from supervision after lifting to 3D. Because POINTWORLD is trained on 3D point flows rather than image-plane trajectories, we lift each tracked 2D point to a 3D world-space trajectory by back-projecting it with the corresponding depth, intrinsics, and extrinsics at each timestep. We next reconstruct 3D trajectories and apply cliplevel postprocessing. For each frame, valid depth, intrinsics, and extrinsics back-project tracked pixels to world-frame 3D points with RGB. Tracks across time yield temporally consistent per-point trajectories. We store per-camera trajectories to avoid mixing viewpoints prematurely and keep per-point visibility and depth-valid flags that are later used to mask supervision. 

**Postprocessing.** To further improve the quality of the obtained 3D point flows, we apply two postprocessing steps: DBSCAN-based outlier removal and per-frame normal estimation. For each clip we first remove spatial outliers using multi-scale DBSCAN clustering [170] across all external cameras: at each timestep, we run DBSCAN with radii _ε ∈{_ 0 _._ 02 _,_ 0 _._ 05 _}_ m and minimum core size 5, and mark point flows that are classified as outliers in more than 20% of frames as outliers to be discarded. From the remaining trajectories, we estimate normals per frame using local neighborhoods (up to _k_ =30 neighbors within radius 0 _._ 1 m) and orient them toward the camera, followed by a temporal consistency step that flips back-facing normals so that normal directions remain coherent over time. 

23 

## **A.3. BEHAVIOR-1K Data Generation** 

BEHAVIOR-1K (B1K) [8] is a large-scale benchmark of everyday household activities in photorealistic simulation built on NVIDIA Isaac Sim. As part of the 2025 BEHAVIOR Challenge, it provides approximately 10 _,_ 000 humanteleoperated episodes (average length _≈_ 6 _._ 6 minutes) across 50 tasks executed by a bimanual mobile robot (Galexea R1 Pro). We replay these episodes in the original simulator and attach three virtual cameras (left shoulder, right shoulder, and head) to extract short clips with meaningful interactions and dense 3D point flows, as detailed below. 

### **A.3.1. Dataset Replay** 

For each BEHAVIOR-1K episode, we replay it in the simulator using the recorded sequence of environment states and actions. To prevent physics leakage and adhere to the original demonstrations, we iterate over the stored trajectory and, at every recorded step, load the corresponding simulator state and advance the simulator once with the recorded action. At every such step, we also render three external RGB-D cameras mounted on the robot: a left and right shoulder camera attached near the base, and a head-mounted camera. All three cameras have ground-truth intrinsics and extrinsics, and produce per-pixel depth, surface normals, and per-link segmentation in addition to RGB. All extrinsics are recorded in the robot base frame in the first timestep of each clip. 

### **A.3.2. Clip Filtering** 

We aim to extract short clips of fixed length _F_ =11 frames that contain meaningful interaction between the robot and the scene while discarding static or uninteresting intervals. To generate candidates, we slide an overlapping window of length _F_ over each replayed episode at a fixed temporal stride; any window for which _all_ external cameras have no visible, in-workspace scene objects—that is, no non-robot, non-ground meshes with valid depth inside the workspace bounds—is immediately discarded. 

For each remaining candidate window, we maintain a set of _motion indicators_ and _contact indicators_ that are updated over the clip. Let _Mg_ denote the event that at least one arm’s end-effector exhibits sufficient translational or rotational motion over the clip or undergoes a change in gripper open/closed state, with thresholds that depend on whether the gripper is predominantly open or closed. Let _Mj_ denote the event that any non-base robot joint moves more than a fixed threshold over the clip. Using the object trajectories described in Section A.3.3, we define _Mo_ as the event that at least one object moves more than an object-movement threshold in position or orientation relative to its pose at the first frame of the clip. 

during the clip, and let _Cf_ denote the event that any gripper finger link experiences contact. Clips that contain large simulator-induced discontinuities (such as scene resets) are filtered internally before applying the following logical criterion. 


The term _¬Ct_ discards clips that contain trunk or arm collisions. The first disjunct in equation 3 retains clips where object motion is causally associated with non-base joint motion. The second disjunct retains clips where object motion primarily arises through gripper-finger contacts, which covers behaviors such as pushing an object with only base motion rather than arm motion (e.g., pushing a door by moving the base). The third disjunct retains “negative” clips in which the robot moves but no objects move, providing supervision on background dynamics and free-space motions. 

### **A.3.3. 3D Point Flows from Simulation** 

For each accepted clip and each external camera, we construct a compact representation of 3D point flows that exploits three properties of the simulation setting: (i) the environment is composed of rigid objects decomposed into rigid links; (ii) we have access to ground-truth link-level instance segmentation in rendered images; and (iii) we can query the exact rigid trajectory of every link throughout the clip. At the first frame of the clip, we back-project depth for each visible link to obtain a set of surface points in that link’s local frame, together with associated colors and normals, after filtering out background and robot meshes and enforcing workspace bounds in the robot base frame at the clip start. We then record the time-varying poses of all visible links and cameras in this same clip-start robot base frame. This factorized representation, local link points plus per-link trajectories, allows us to reconstruct exact per-point 3D trajectories for any clip while remaining far more storage-efficient than storing dense point clouds at every frame. Note that while we access ground-truth simulator state for obtaining ground-truth 3D point flows, the simulator state is never exposed to the model. 

From the ground-truth simulation state, we further construct contact indicators. Let _Ct_ denote the event that any trunk or arm link experiences a nonzero contact impulse 

24 

|**Operation**|**Description**|
|---|---|
|Camera subsampling|Sample randomized calibrated RGB-D views per timestep and concatenate their 3D points into a<br>single scene cloud.<br>|
|Bounds filtering|Retain only scene points that stay within a workspace cube (approx.[_−_3_,_3]<sup>3 </sup>m) for the entire<br>clip, dropping particles that ever exit the bounds.|
|Centering|Mean-center first-frame scene and robot points.|
|Image resize|Downscale RGB-D images to320_×_180.|
|Voxel downsampling|Voxel-grid sampling at1_._5cm; select one point per occupied voxel at_t_=0, and apply the same<br>indices to all timesteps.|
|Multi-sphere cropping|Iteratively remove spheres of points far from the robot (up to three spheres, radii in[0_._10_,_0_._80]m<br>with buffer0_._25m) until the scene falls below the target budget.|
|Max scene / robot points|Randomly subsample scene points if more than12 000remain after cropping; robot points are<br>capped at500by construction.|
|Random yaw|Uniform rotation about the vertical axis over[_−π, π_].|
|Uniform scaling|Isotropic scaling with factor sampled uniformly from[0_._9_,_1_._1].|
|Random reflection|With probability0_._5, reflect the scene and robot across either the_x_- or_y_-axis.|
|Chromatic auto-contrast|Apply chromatic auto-contrast to RGB channels with probability0_._2and blend factor up to0_._2.|
|Chromatic translation|Add a global RGB offset with magnitude 2% with probability0_._95.|
|Chromatic jitter|Add per-point RGB noise with standard deviation 2% with probability0_._95.|


Table 3. **Data Preprocessing and Augmentations.** 

|**Point set**|**Feature**|**Definition**|
|---|---|---|
|Robot|Position_p_<sup>robot</sup><br>_t,j_<br>|3D coordinates of robot points over time.|
|Robot|Color_c_<sup>robot</sup><br>_j_|Constant magenta color(1_,_0_,_1)indicating robot identity, shared across<br>timesteps.|
|Robot|Normal_n_<sup>robot</sup><br>_t,j_|Surface normals of robot points from the known robot URDF.|
|Robot|Gripper openness˜_gt_|Scalar gripper open value per timestep, broadcast to all robot points.|
|Robot|Velocity_v_<sup>robot</sup><br>_t,j_|Per-point velocity from mid-point finite differences over_p_<sup>robot</sup><br>_t,j_<br>across time.|
|Robot|Acceleration_a_<sup>robot</sup><br>_t,j_|Per-point acceleration from mid-point finite differences over_v_<sup>robot</sup><br>_t,j_<br>across<br>time.|
|Scene|Position_x_0_,i_|3D coordinates of scene points at the first frame after preprocessing.|
|Scene|Color_c_<sup>scene</sup><br>0_,i_|RGB color of scene points at the first frame.|
|Scene|Normal_n_<sup>scene</sup><br>0_,i_|(Estimated) surface normals of scene points at the first frame.|
|Scene|Gripper openness sequence_g_0:_T −_1|Sequence of gripper openness values over the context and prediction hori-<br>zon, broadcast to every scene point.|
|Scene|Distance-to-robot_d_0:_T −_1_,i_|For each timestep, distance from the first-frame position of scene point_i_to<br>the closest robot point, stacked across time.|


Table 4. **Per-Point Input Features.** 

25 

## **A.4. Model Training Details** 

**Data Preprocessing and Augmentations.** Here we describe the data preprocessing and augmentations used in our experiments. Each training sample fuses calibrated RGB-D views before passing through workspace filtering, centering, and deterministic voxel sampling with multi-sphere cropping so that the fused cloud respects fixed budgets for scene and robot points. Geometric augmentations consist of random yaw rotations, isotropic scaling, and reflections; photometric augmentations apply auto-contrast, global color shifts, and per-point jitter to the RGB channels. For evaluation, we ensure the pipeline to be fully deterministic and disable all augmentations. 

**Per-Point Input Features.** Here we describe the per-point features produced as part of the data pipeline, prior to their consumption by the model. Details are listed in Table 4. Robot features stack positions, surface normals, a gripper scalar, and velocity and acceleration terms: 


where _p_<sup>robot</sup> _t,j_ and _n_<sup>robot</sup> _t,j_ are position and normal, _c_<sup>robot</sup> _j_ is a fixed color tag, ˜ _gt_ is the normalized gripper openness, and ( _vt,j_<sup>robot</sup><sup>_, a_robot</sup> _t,j_<sup>) come from mid-point finite differences across</sup> the horizon with zero-velocity boundary conditions at the first and last timestep, i.e., we assume the robot is stationary at the boundaries of each model window. Scene features are computed for only the first frame _t_ =0 and combine positions, colors, estimated normals, gripper openness sequence, and distances to the nearest robot point: 


where _c_<sup>scene</sup> and _n_<sup>scene</sup> are the RGB color and normal at the 0 _,i_ 0 _,i_ first frame, _g_ 0: _T −_ 1 _∈_ R<sup>_T_</sup> is the sequence of gripper openness values over the context-plus-prediction horizon broadcast to every scene point, and _dt,i_ is the distance from scene point _i_ to the closest robot point at timestep _t_ , 


The distance field _d_ 0: _T −_ 1 _,i_ is obtained from nearest-neighbor queries between first-frame scene points and robot points at every timestep. 

**3D Scene Featurization with DINOv3.** Prior to the point cloud backbone, POINTWORLD uses a 2D scene encoder based on DINOv3 ViT-L/16 by aggregating its multi-layer features. To featurize the 3D scene points with the imagebased encoder, the first-frame scene coordinates _x_ 0 _,i ∈_ R<sup>3</sup> are projected into each chosen camera. For camera _c_ 

with intrinsics _Kc_ and extrinsics ( _Rc, tc_ ) we form _u_ ˜ _c,i_ = _Kc_ ( _Rcx_ 0 _,i_ + _tc_ ) and obtain the pixel coordinate as 


The same intrinsics and extrinsics support a depthconsistency mask that compares the projected depth of each point with the given depth image, so only views whose discrepancy is below a few millimeters contribute features. 

For each visible point-camera pair ( _i, c_ ), DINOv3 patch tokens are sampled at _uc,i_ by bilinear interpolation on the patch-token grid, using a coordinate mapping that aligns token centers with pixel centers. Let _fc,i ∈_ R<sup>_D_patch</sup> denote the concatenated multi-layer patch feature for point _i_ in camera _c_ , and let _mc,i ∈{_ 0 _,_ 1 _}_ indicate visibility and depth consistency. Features are aggregated across cameras by averaging over the contributing views, 


The averaged token is mapped to the backbone width (256 channels) by a learned projection and fused with a separately projected version of the raw scene features from Table 4; layer normalization is applied to each stream before concatenation, and a final linear layer produces the per-point embedding supplied to the dynamics backbone. The 2D encoder is kept frozen during training and evaluation. 

**Visibility-Aware Supervision.** For real-world domains, we restrict training on 3D point trajectories to correspondences that are both geometrically and photometrically reliable. The annotation pipeline supplies per-point visibility (from 2D trackers [11] on real data and from ground-truth simulator state on synthetic data) together with per-pixel depth-validity; both signals are propagated to the lifted 3D trajectories and stored as binary flags per scene point and timestep. During training, we construct a per-timestep mask that selects scene points that are visible in the camera view and have valid depth support. The weighted dynamics objective from Section 3 is then evaluated only over this subset of correspondences (points filtered out receive zero loss weight), so that gradients are driven by non-occluded, depthvalid 3D flows. For simulation domains, where trajectories and depth are noise-free and occlusions are explicitly modeled, all scene points contribute to the loss. 

**Training Configuration.** We train the 1B-parameter version of POINTWORLD on both BEHAVIOR-1K and DROID, with configuration and PointTransformerV3 (PTv3) design summarized in Table 5 and Table 6, respectively. For the main experiments in the paper, training configuration and PTv3 design are summarized in Table 7 and Table 8. 

26 

**Aleatoric Uncertainty on Simulation Data.** When training on mixtures of real and simulated domains, directly learning per-point uncertainty everywhere can collapse the model because simulated trajectories are noise-free. In the objective from Section 3 the residual term for point _i_ at step _k_ is weighted as _wk,i ρδ_ ( **P**<sup>**ˆ**</sup> _t_ + _k,i −_ **P** _t_ + _k,i_ ) e<sup>_−sk,i_</sup> + _wk,i sk,i_ . For vanishing residuals (typical in simulation), minimizing the loss drives _sk,i_ toward log _ρδ_ ( _·_ ). Since _ρδ_ ( _·_ ) approaches zero, the optimal _sk,i_ becomes a large negative number, i.e., the predicted variance _σk,i_<sup>2=exp(</sup><sup>_sk,i_)collapsestoward</sup> zero. As a consequence, e<sup>_−sk,i_</sup> explodes, so any small numerical discrepancy in simulated residuals produces excessively large gradients that overwhelm the real-data contributions and destabilize joint training. To stabilize training, we treat aleatoric variance on simulation domains as a constant: the uncertainty head is trained normally on real data, but for simulated domains its log-variance is replaced by a batchwise constant that matches the average variance observed on real samples (or a small fixed value when only simulation is present). This preserves heteroscedastic weighting where it is most useful (real, noisy supervision) while preventing the model from exploiting the uncertainty head to down-weight clean simulated gradients. 

27 

|**Setting**|**Value**|
|---|---|
|Optimizer|AdamW|
|Learning rate|1_×_10<sup>_−_4</sup>|
|Epochs|300|
|Weight decay|10<sup>_−_2</sup>|
|Global batch size|1920 sequences|
|Gradient clipping|Global_ℓ_2 norm capped at5|
|Loss|Huber loss with_δ_ = 5_._0with movement weighting and aleatoric uncertainty|
|Prediction horizon|10 steps|
|Training GPUs|128 NVIDIA H100 GPUs|
|Training time|20 days|


Table 5. **Training Configuration for POINTWORLD-1B.** 

**Component Values** Grid size 1 _._ 5 cm Encoder depth (4 _,_ 4 _,_ 8 _,_ 8 _,_ 12 _,_ 12 _,_ 4) Encoder channels (256 _,_ 384 _,_ 384 _,_ 512 _,_ 512 _,_ 768 _,_ 1024) Encoder heads (8 _,_ 12 _,_ 12 _,_ 16 _,_ 16 _,_ 24 _,_ 32) Encoder stride (1 _,_ 2 _,_ 2 _,_ 2 _,_ 2 _,_ 2 _,_ 2) Encoder patch size (256 _,_ 256 _,_ 256 _,_ 256 _,_ 256 _,_ 256 _,_ 256) Decoder depth (4 _,_ 4 _,_ 4 _,_ 4 _,_ 4 _,_ 4) Decoder channels (256 _,_ 384 _,_ 384 _,_ 512 _,_ 512 _,_ 768) Decoder heads (8 _,_ 12 _,_ 12 _,_ 16 _,_ 16 _,_ 24) Decoder patch size (256 _,_ 256 _,_ 256 _,_ 256 _,_ 256 _,_ 256) 

Table 6. **PointTransformerV3 (PTv3) Architecture for POINTWORLD-1B. Encoder and decoder configurations are ordered by stage.** 

**Setting Value** Optimizer AdamW Learning rate 1 _×_ 10<sup>_−_4</sup> Epochs 200 Weight decay 10<sup>_−_2</sup> Global batch size 176 sequences Gradient clipping Global _ℓ_ 2 norm capped at 5 Loss Huber loss with _δ_ = 5 _._ 0 with movement weighting and aleatoric uncertainty Prediction horizon 10 steps Training GPUs 8 NVIDIA H100 GPUs Training time 7 days 

Table 7. **Training Configuration for POINTWORLD-411M.** 

**Component Values** Grid size 1 _._ 5 cm Encoder depth (4 _,_ 4 _,_ 4 _,_ 8 _,_ 8 _,_ 12 _,_ 4) Encoder channels (256 _,_ 256 _,_ 256 _,_ 384 _,_ 384 _,_ 512 _,_ 768) Encoder heads (4 _,_ 4 _,_ 4 _,_ 8 _,_ 8 _,_ 16 _,_ 24) Encoder stride (1 _,_ 2 _,_ 2 _,_ 2 _,_ 2 _,_ 2 _,_ 2) Encoder patch size (256 _,_ 256 _,_ 256 _,_ 256 _,_ 256 _,_ 256 _,_ 256) Decoder depth (2 _,_ 2 _,_ 2 _,_ 2 _,_ 2 _,_ 2) Decoder channels (256 _,_ 256 _,_ 256 _,_ 384 _,_ 384 _,_ 512) Decoder heads (4 _,_ 4 _,_ 4 _,_ 8 _,_ 8 _,_ 16) Decoder patch size (256 _,_ 256 _,_ 256 _,_ 256 _,_ 256 _,_ 256) 

Table 8. **PointTransformerV3 (PTv3) Architecture for POINTWORLD-411M. Encoder and decoder configurations are ordered by stage.** 

28 

## **A.5. DROID Evaluation Protocol** 

Following the protocol in Section 5, we measure persequence losses and aggregate them into dataset-level summaries. Alongside the overall per-point, per-timestep _ℓ_ 2 distance, we report the same metric separately on moved and static points, since movers form a minority of the points but dominate perceived quality. We use these metrics directly for simulation data (BEHAVIOR-1K) since they are noiseless. However, for real-world data (DROID), we further apply expert confidence filtering to obtain filtered metrics. Details are described below. 

static points identified from the ground-truth trajectories via a small displacement threshold. 

**Expert Confidence Filtering.** Although the mover- _ℓ_ 2 score highlights the behavior we care about most, imperfect real-world annotations mean that a noticeable fraction of mover points correspond to outliers or background clutter, because those points tend to have large movement magnitudes due to unstable depth estimation. During training, the aleatoric uncertainty regularization down-weights those points, but at evaluation time different models produce their own uncertainty predictions, making comparisons challenging. To obtain a model-agnostic notion of trustworthy ground-truth, we train an expert model only on the evaluation split with uncertainty predictions, convert the predicted variance into a per-point confidence in [0 _,_ 1], and threshold this per-timestep per-point confidence at the 0 _._ 8 quantile over all points. Points below this confidence are treated as lowconfidence outliers. We voxelize these low-confidence sets in world coordinates using the training grid size _g_ and cache the resulting voxel grids for each evaluation sample so that the same filtering masks can be reused across subsequent evaluation runs and model variants. Note that the expert model is only used to compute the low-confidence voxel grids and does not share any training data or parameters with any evaluated models. 

**Filtered Evaluation.** To evaluate a model, for each sample, we first reconstruct world-coordinate voxel indices of scene points and then determine whether each point lies inside a precomputed low-confidence voxel. This yields a binary filter mask so that only high-confidence points at highconfidence timesteps (deemed by the shared expert model) contribute to the filtered metrics. 

**Mover/Static Splits.** Let _P_<sup>ˆ</sup> _t,i_ and _Pt,i_ denote predicted and ground-truth 3D positions. We compute per-point error _et,i_ = _∥P_<sup>ˆ</sup> _t,i − Pt,i∥_ 2 and report 


where _Vt_ denotes valid points at timestep _t_ . Mover- _ℓ_ 2 and static- _ℓ_ 2 use the same definition but restrict _Vt_ to moved or 

29 

## **A.6. Real-Robot Experiment Details** 

Real-robot experiments use a 7-DoF Franka arm equipped with a 3D-printed fin ray gripper [171, 172]. The robot is mounted on a wheeled, non-motorized base for in-thewild deployments. Since POINTWORLD is trained on data containing Robotiq 2F-85 and Galexea R1 Pro grippers, the fin ray gripper geometry remains fully unseen by the model, illustrating cross-gripper geometry generalization. Since the pipeline predicts 6-DoF end-effector poses, we run position control at 20 Hz: each predicted target pose is clipped to a predefined workspace, then linearly interpolated from the current pose with steps of 5 mm in translation and 1<sup>_◦_</sup> in rotation. For every interpolated pose, inverse kinematics (PyBullet solver) produces target joint positions that are tracked with the Deoxys joint-impedance controller [173]. We use one RealSense D435 mounted on the left shoulder of the robot to capture RGB and the stereo IR images. The stereo IR images are used to estimate the metric depth using FoundationStereo [9], given known baseline and camera intrinsics. 

### **A.6.1. Model-Based Planning** 

In this work, we use a single pre-trained POINTWORLD as the dynamics model. The model is pre-trained jointly on both real-world and simulated data. We use a samplingbased model-predictive path integral (MPPI) controller that samples action sequences around a zero-initialized nominal using cubic splines with _n_ knots=4 and degree 3. Noise scales are scheduled between _σ_ min=0 _._ 05 and _σ_ max=0 _._ 50 (in normalized action units). Each refinement iteration draws 256 samples; importance weights use temperature _β_ =0 _._ 05, and the nominal is updated with an exponential moving average (EMA = 0 _._ 9). We perform planning for 30 steps into the future, and the horizon is chunked to match the prediction window of the dynamics model. We perform 20 refinement iterations. The planning time is typically around a few seconds depending on task complexity and specific model size variant used. While we do not perform replanning in this work, replanning can be done at a real-time frequency by warm-starting from the previous nominal trajectory. 

share same control regularization comprising SE(3) pathlength penalties and IK-based reachability residual. 

### **A.6.3. Evaluation Protocol** 

We conduct evaluations on the following tasks: rigid pushing (tissue box, book), deformable manipulation (scarf fold, pillow place), articulated manipulation (microwave open, drawer close), and tool use (duster sweep, broom sweep). Each task is evaluated with ten randomly sampled initial configurations. The configurations are sampled prior to evaluation and verified to be kinematically feasible for the robot. For each trial, a human operator restores the scene to the designated configuration and triggers execution. We consider the trial successful if the task objective is met. Otherwise we declare failure. If the optimization produces a solution that is considered unsafe for execution, the trial is considered failure too. The success rates are reported in the main paper. 

### **A.6.4. Effect of Training Mixture** 

Beyond the quantitative success rates for real-world deployment, we observe interesting qualitative traits when using different variants of POINTWORLD pre-trained on different data mixtures. We empirically observe that models trained only on real data tend to be conservative: a common failure mode is for scene points to remain static even when the robot establishes contact, which we attribute to heavy regularization coping with annotation noise. On the other hand, models trained only on simulation data excel on rigid objects but frequently mis-segment cluttered real scenes implicitly, causing background points to move together with the target. Models trained on both real and simulated domains yield the most balanced behavior in practice, combining realistic contact handling with the ability to generalize to novel realworld scenes. A systematic study of how training-mixture design shapes deployment-time behavior, e.g., by varying real/sim proportions or task/domain coverage under controlled conditions, remains an important direction for future work. 

### **A.6.2. Task Specification** 

We specify tasks through a GUI tool that allows users to select object masks using SAM2 [174] and specify target positions in the world frame. We find this simple objective as a unified interface for specifying diverse real-world tasks including rigid pushing, deformable manipulation, articulatedobject interaction, and tool use. Following common practices in reward design [175], we add a mild end-effector proximity term to encourage exploration in the object’s neighborhood without prescribing a particular contact pattern. For deformable and tool-use tasks we begin from a pre-grasped configuration so that subsequent motion primarily probes deformable dynamics and object-object contacts. All tasks 

30 

## **A.7. Additional 3D Annotation Examples** 

Interactive visualizations available at project website. 


Figure 14. **DROID 3D annotations** , including robot-overlaid RGBs, depths, point clouds, and comparisons to original dataset. 

31 


Figure 15. **DROID 3D annotations** , including robot-overlaid RGBs, depths, point clouds, and comparisons to original dataset. 

32 

## **A.8. Additional Model Rollouts** 

Interactive visualizations available at project website. 


Figure 16. **DROID Unseen Rollouts** , including deformable manipulation, robot-object interactions, and object-object interactions. 

33 


Figure 17. **DROID Unseen Rollouts** , including deformable manipulation, and grasping behaviors. 

34 


Figure 18. **DROID Unseen Rollouts** , including grasping behaviors, gravity effects, and glass objects. 

35 


Figure 19. **BEHAVIOR-1K Unseen Rollouts** , including constrained bimanual lifting, gravity effects (dropped laptop), object-object interactions (laptop v.s. table), and articulated manipulation (fridge). 

36 


Figure 20. **BEHAVIOR-1K Unseen Rollouts** , including object-object interactions (within basket), gravity effects (within basket), and whole-body behaviors. 

37 


Figure 21. **BEHAVIOR-1K Unseen Rollouts** , including bimanual manipulation, whole-body behaviors, and implicit shape completion. 

38 

