---
title: "GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation"
date: "2025-12-18"
authors: "Jingjing Qian; Boyao Han; Chen Shi; Lei Xiao; Long Yang; Shaoshuai Shi"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2512.16811
pdf: https://arxiv.org/pdf/2512.16811
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.16811)** / [論文ページ](https://arxiv.org/abs/2512.16811)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **GeoPredict: Leveraging Predictive Kinematics and 3D Gaussian Geometry for Precise VLA Manipulation** 

Jingjing Qian<sup>1</sup> Boyao Han<sup>2</sup> Chen Shi<sup>1</sup> Lei Xiao<sup>1</sup> Long Yang<sup>1</sup> Shaoshuai Shi<sup>3</sup> Li Jiang<sup>1</sup><sup>_†_</sup> 1The Chinese University of Hong Kong, Shenzhen 2Hunan University 3Voyager Research, Didi Chuxing 

https://jingjingqian75.github.io/GeoPredict-Page/ 

## **Abstract** 

_Vision–Language–Action (VLA) models achieve strong generalization in robotic manipulation but remain largely reactive and 2D-centric, making them unreliable in tasks that require precise 3D reasoning. We propose_ **_GeoPredict_** _, a geometry-aware VLA framework that augments a continuous-action policy with predictive kinematic and geometric priors. GeoPredict introduces a trajectory-level module that encodes motion history and predicts multi-step 3D keypoint trajectories of robot arms, and a predictive 3D Gaussian geometry module that forecasts workspace geometry with track-guided refinement along future keypoint trajectories. These predictive modules serve exclusively as training-time supervision through depth-based rendering, while inference requires only lightweight additional query tokens without invoking any 3D decoding. Experiments on RoboCasa Human-50, LIBERO, and real-world manipulation tasks show that GeoPredict consistently outperforms strong VLA baselines, especially in geometry-intensive and spatially demanding scenarios._ 

## **1. Introduction** 

Vision–Language–Action (VLA) models have recently emerged as a powerful paradigm for robotic manipulation, leveraging large pre-trained Vision–Language Models (VLMs) to map rich visual observations and language instructions directly to actions [4, 22, 51, 54]. By inheriting semantic and visual priors from internet-scale data, these models generalize well across tasks and settings. However, they operate primarily in 2D image space, mapping the current observation reactively and lacking explicit 3D spatial modeling [53]. This 2D-centric, myopic formulation limits performance in tasks requiring precise 3D reasoning and physically consistent long-horizon control. 

To move beyond purely reactive policies, recent work has begun to incorporate predictive structure into visuomotor models [17, 23, 30]. Some approaches learn latent dynamics or temporal abstractions to better capture how states evolve over time [7, 8, 24, 50], while others predict future observations such as RGB frames, depths, or pointbased representations [6, 11, 12, 17, 36, 49]. Although these methods provide useful temporal signals, they often remain view-independent and do not strictly enforce multiview or 3D geometric consistency, making it hard to reason about object poses, clearances, and end-effector motion in workspace coordinates. Moreover, tightly coupling highcapacity predictive modules with large VLA backbones can introduce non-negligible computational overhead if complex 3D prediction is required during inference time. 

For robotic manipulation, we argue that two predictive capabilities are particularly valuable. First, the policy should exploit _predictive kinematic priors_ that summarize how the robot is likely to move over the next few steps, rather than relying solely on instantaneous joint states. Second, it should reason about _predictive 3D Gaussian geometry_ through an explicit, differentiable representation aligned with the robot’s workspace and amenable to supervision from depth and multi-view cues. Crucially, these predictive signals must seamlessly integrate with VLA architectures and keep inference-time overhead modest enough to enable practical deployment for real-time robotic control. 

In this paper, we introduce **GeoPredict** , a geometryaware VLA framework augmented with predictive priors for robotic manipulation. GeoPredict is built on top of a strong continuous-action VLA policy [3], and augments the policy with two complementary predictive modules. 

First, at the kinematic level, we introduce a _trajectorylevel prediction module_ that tracks key robot joints and endeffector points and encodes their motion history into compact tokens via a Track Encoder. A set of learnable future track queries then predicts multi-step 3D keypoint trajectories, providing explicit, differentiable kinematic priors. 

> _†_ Corresponding Author. 

13529 

These predicted trajectories not only regularize the transformer’s internal dynamics, but also serve as guidance for where high-fidelity 3D scene modeling is most needed. 

Second, at the geometric level, we introduce a _predictive 3D Gaussian geometry module_ that forecasts how workspace geometry evolves over time. A coarse 3D spatial query grid is decoded into Gaussian primitives representing the scene at future timesteps. To focus geometric capacity where precision matters most, a track-guided refinement mechanism increases Gaussian density along the predicted future keypoint trajectories of the joints, yielding higher resolution around anticipated motion and interaction regions. The resulting 3DGS representation is supervised through future depth-map rendering, providing a geometryfocused training signal without requiring color modeling. 

Both predictive modules are integrated via a block-wise causal attention hierarchy and are used only during training; inference behaves exactly like the base VLA policy. 

In summary, our main contributions are threefold: (1) We introduce **GeoPredict** , a geometry-aware VLA framework that injects future-aware kinematic and geometric priors into a continuous-action VLA policy, enhancing reasoning about long-horizon 3D dynamics. (2) We propose two complementary predictive modules: a trajectory-level kinematic predictor forecasting multi-step robot keypoint motion, and a predictive 3D Gaussian geometry module with track-guided refinement that allocates geometric capacity to task-relevant interaction regions. (3) We show that GeoPredict delivers consistent and substantial improvements over strong VLA baselines on RoboCasa Human-50, LIBERO, and real-world manipulation tasks, particularly those requiring precise spatial reasoning and geometric robustness. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

Vision-Language-Action (VLA) models have emerged as powerful robotic policies [4, 20, 22, 44, 51, 52]. Pioneering methods like OpenVLA [20] rely on discrete autoregressive tokenization, limiting inference frequency and struggling with continuous, multi-modal action distributions [53]. While subsequent architectures like _⇡_ 0 [3] utilize conditional flow matching [25] to generate continuous actions, they remain predominantly 2D-centric and reactive [3, 5, 17, 52], lacking the robust 3D geometric understanding required for complex manipulation. Furthermore, although SpatialVLA [37] and BridgeVLA [21] integrate explicit 3D information and auxiliary tasks, they still lack a predictive understanding of 3D scene dynamics. To address this gap, our GeoPredict introduces a geometry-aware predictive model that directly forecasts 3D scene evolution using 3D Gaussian Splatting [18], equipping the VLA model with predictive geometric priors. 

### **2.2. Future Prediction for Robotic Manipulation** 

Recent works explore future prediction to enhance robotic policies [6, 13–15, 31, 48]. Some directly forecast future observations like RGB images [17, 42], depths [49], or pointmaps [27], while approaches like Seer [40] condition inverse dynamics on these forecasted visual states. However, these methods face two key limitations. First, popular approaches like SuSiE [2] or UniPi [10] often rely on a single prediction step, which struggles to capture complex physical dynamics and introduces time-consuming denoising that reduces control frequency. Second, these 2Dcentric methods [42] struggle with multi-view consistency and lack the explicit 3D geometry crucial for accurate manipulation. To address this gap, we introduce GeoPredict, a geometry-aware predictive model that forecasts scene evolution over a full horizon of _H_ steps in explicit 3D space, learning a spatially coherent and predictive 3D representation to condition action generations. 

### **2.3. 3D Scene Representation** 

3D scene representation is a fundamental problem in computer vision, traditionally relying on explicit structures like meshes [28], voxels [43] and point clouds [35]. Recent research has shifted to neural representations that learn continuous models of scene geometry and appearance. Pioneered by Neural Radiance Fields (NeRF) [32], these implicit models often require subsequent acceleration [16, 33, 45] due to costly training and rendering. More recently, 3D Gaussian Splatting (3DGS) [18, 38, 41, 46] has emerged as a highly effective explicit alternative. 3DGS models scenes as a collection of 3D Gaussians with learned attributes, leveraging differentiable rasterization for high-fidelity and remarkably efficient rendering. While recent works like GWM [30] apply 3DGS to robotic world modeling, directly forecasting these massive Gaussian attributes remains computationally demanding. To circumvent this burden, we leverage 3DGS as a predictive scene geometry module solely during training, aiming to endow the VLA policy with intrinsic, foresight-driven spatial reasoning ability. 

## **3. Methodology** 

We propose **GeoPredict** , a geometry-aware VLA framework that equips continuous-control policies with predictive kinematic and geometric priors. GeoPredict jointly learns future robot keypoint trajectories and future scene geometry through a 3DGS representation, and conditions the underlying VLA on these predictions. Notably, these predictive modules are used only during training, while the action generation process remains similar to a standard VLA policy. 

First, we describe the problem setup and the base VLA model (Sec. 3.1). We then introduce our trajectory encoding and future motion prediction module (Sec. 3.2), followed 

13530 


Figure 1. **Overview of GeoPredict.** Given an instruction, multi-view images and motion history encoded by the Track Encoder, a central LLM Transformer learns two main tasks. First, it predicts multi-timestep 3D keypoint trajectories using learnable Future Track Query. Second, it forecasts future workspace geometry as a predictive 3D Gaussian by processing a 3D Spatial Query through a Voxel Decoder. A track-guided refinement mechanism leverages the predicted future tracks to allocate geometric capacity to task-relevant interaction regions. Our policy then generates the final action via an Action Expert. Crucially, these predictive modules serve exclusively as trainingtime supervision and are not invoked during inference, thus preserving efficiency. 

by the predictive 3D Gaussian geometry and its refinement mechanism (Sec. 3.3). Finally, we present the attention design, training objective and inference process (Sec. 3.4). 

### **3.1. Preliminary** 

**Problem Definition.** The VLA paradigm [3, 20] aims to learn a policy **_⇡_** that maps a language instruction **L** , the current multi-view image observation **I** _t_ , and the robot’s proprioceptive state **Q** _t_ to a continuous action chunk **A** _t_ = [ **a** _t,_ **a** _t_ +1 _, . . . ,_ **a** _t_ + _H−_ 1], where we set _H_ = 50. Each action **a** _t 2_ **R**<sup>7</sup> is a 7-DoF end-effector command **a** _t_ = _{_ ∆ **x** _,_ ∆ **_✓_** _, g}_ , where ∆ **x** _2_ R<sup>3</sup> and ∆ **_✓_** _2_ R<sup>3</sup> denote translational and rotational offsets (e.g., in axis–angle or Euler representation), and _g 2_ R is the gripper’s open-close state. 

While VLAs generate actions reactively from the current observation, many manipulation tasks require anticipating how both the robot and the surrounding scene will evolve over time. Thus, GeoPredict augments the policy by conditioning not only on past observations but also on internally predicted future robot motion and future scene geometry. 

**Base VLA model.** We adopt _⇡_ 0 [3] as the VLA base model. It comprises a VLM (PaliGemma [1] with a SigLIP vision encoder) and a robotics-specific _action expert_ that generates continuous actions via conditional flow matching [25]. Text, image, and proprioceptive tokens are projected into a shared space and processed by the transformer; 

the action expert then generates **A** _t_ by integrating a learned vector field from noise in a small, fixed number of steps. 

### **3.2. Trajectory-Level Kinematic Prediction** 

GeoPredict models robot motion at the trajectory level. This provides both a compact summary of past kinematics and an explicit prediction of future trajectories, serving as a kinematic prior for action generation and as guidance for spatial refinement in the following 3D Gaussian geometry module. **Track Encoder.** The Track Encoder compresses the motion history of all robot keypoints into compact tokens for the transformer. This historical context provides a strong kinematic prior: because joint motion exhibits inertia and action generation fundamentally involves forecasting future trajectories, encoding past dynamics enables the model to make more physically consistent motion predictions. 

As illustrated in Figure 1, we track _K_ 3D keypoints (joints and end-effector points). For each keypoint _k 2 {_ 1 _, . . . , K}_ , we collect its 3D coordinates from time 0 to _t−_ 1 into a trajectory **_T_** _k 2_ R<sup>(</sup><sup>_t−_1)</sup><sup>_⇥_3</sup> . A shared learnable history query **Q**<sup>hist</sup> performs cross-attention over the embedded trajectory to produce a single _history track token_ : 


These _K_ history tokens encode inertia, joint limits, and mo- 

13531 

tion regularities, and are appended to the transformer input. **Future Track Query.** To explicitly capture future motion, we introduce _K_ learnable future track queries _{_ **q**<sup>fut</sup> _k_<sup>_}_</sup> _k_<sup>_K_</sup> =1<sup>.</sup> These queries are processed together with the instruction **L** , current images **I** _t_ , and history tokens _{_ **Z**<sup>hist</sup> _k_<sup>_}_, producing</sup> future track embeddings **e**<sup>fut</sup> _k_<sup>that summarize the latent pre-</sup> dicted trajectory of each keypoint. 

We decode each **e**<sup>fut</sup> _k_<sup>into an explicit spatio-temporal tra-</sup> jectory by using a shared MLP to predict _H_ +1 timesteps, one for the current time _t_ and _H_ for future steps _{t_ +1 _, . . . , t_ + _H}_ . A 1D sinusoidal temporal encoding **PE**<sup>time</sup> _2_ R<sup>(</sup><sup>_H_+1)</sup><sup>_⇥C_</sup> is then adopted as follows: 


The predicted trajectories are supervised using a Mean Squared Error loss over all keypoints and timesteps as 


This encourages the shared transformer backbone to learn predictive, dynamically consistent motion representations and provides explicit future trajectories that will be used for predictive 3D Gaussian refinement. 

### **3.3. Predictive 3D Gaussian Geometry** 

We now introduce a predictive 3D Gaussian geometry module that estimates the future geometry of the robot workspace. By anticipating how the scene will evolve, this module provides the policy with stronger spatial reasoning abilities, which is essential for manipulation tasks that reply on forecasting future object configurations. The module comprises four components: a 3D spatial query for encoding the robot workspace, a voxel decoder that produces 3D Gaussian Splatting (3DGS) primitives, a track-guided refinement mechanism for increasing fidelity near interaction regions, and a depth-rendering objective for supervision. 

**3D Spatial Query.** To represent the workspace efficiently, we define a 3D volume of dimensions _H ⇥ W ⇥ D_ meters and discretize it into voxels of size _v_ , yielding a grid resolution of ( _H/v_ ) _⇥_ ( _W/v_ ) _⇥_ ( _D/v_ ). For token efficiency, this high-resolution grid is downsampled by a factor of 4 along each axis, producing a coarse grid of size _Nx ⇥ Ny ⇥ Nz_ , where _Nx_ = _H/_ (4 _v_ ), _Ny_ = _W/_ (4 _v_ ), and _Nz_ = _D/_ (4 _v_ ). 

Each coarse voxel is assigned a learnable _C_ -dimensional embedding, forming the initial spatial query tensor **Q**<sup>init</sup> _2_ R<sup>_Nx⇥Ny⇥Nz⇥C_</sup> . To incorporate geometric structure and reduce learning difficulty, we add a 3D sinusoidal positional encoding **PE**<sup>spatial</sup> _2_ R<sup>_Nx⇥Ny⇥Nz⇥C_</sup> , constructed by concatenating independent 1D sinusoidal encodings along the _x_ , _y_ , and _z_ axes: **PE**<sup>spatial</sup> [ _i, j, k_ ] = Concat� **PE**<sup>x</sup> [ _i_ ] _,_ **PE**<sup>y</sup> [ _j_ ] _,_ **PE**<sup>z</sup> [ _k_ ]� _._ Hence, the final spatial 

query is obtained by 


All spatial queries are flattened into a sequence of _NxNyNz_ tokens and provided to the transformer together with the instruction, current observations and history track tokens. **Voxel Decoder.** After multi-layer attention, we obtain spatial embeddings **E**<sup>spatial</sup> _2_ R<sup>(</sup><sup>_NxNyNz_)</sup><sup>_⇥C_</sup> that summarize the workspace representation at time _t_ . To model future geometry, we reuse the temporal positional encoding **PE**<sup>time</sup> from Eq. (2) and construct temporally shifted embeddings 


Each **E**<sup>spatial</sup> _t_ + _⌧_ is reshaped into a grid of size _Nx ⇥ Ny ⇥ Nz_ and passed through a 3D voxel decoder composed of transposed convolutions and upsampling layers, which restores the original voxel resolution ( _H/v_ ) _⇥_ ( _W/v_ ) _⇥_ ( _D/v_ ). This yields a dense voxel feature volume 


where _C_<sup>_0_</sup> is the feature dimension of the voxel feature grid. A final 3D convolution maps each voxel feature **F**<sup>voxel</sup> [ _i, j, k_ ] to a set of _NG_ Gaussian primitives. Following the 3DGS formulation [18], each primitive **g** = _{_ **_µ_** _, ↵,_ **⌃** _}_ has a 3D center **_µ_** _2_ R<sup>3</sup> , an opacity _↵ 2_ R, and a covariance matrix **⌃** _2_ R<sup>3</sup><sup>_⇥_3</sup> . Because our focus is on geometry rather than appearance, we omit color coefficients. The union of Gaussians over all voxels forms the initial 3D scene representation **G**<sup>init</sup> _t_ + _⌧_<sup>.</sup> 

**Track-based Gaussian Refinement.** While a coarse global representation is often sufficient for capturing the overall workspace, accurate manipulation requires high-fidelity geometry near regions of interaction, particularly around the end-effector, joints, and task-relevant objects. We therefore refine the Gaussian representation adaptively using the predicted future keypoint trajectories from Sec. 3.2. 

At timestep _t_ + _⌧_ , given the initial Gaussian set **G**<sup>init</sup> _t_ + _⌧_<sup>and</sup> the predicted keypoint positions **P** _t_ + _⌧_ = _{_ **p** ˆ _k,t_ + _⌧ }_<sup>_K_</sup> _k_ =1<sup>, we</sup> define a binary refinement mask for each voxel **_V_** [ _i, j, k_ ]: 


For each voxel with **M**<sup>refine</sup> [ _i, j, k_ ] = 1, a shared MLP maps **F**<sup>voxel</sup> [ _i, j, k_ ] to an additional _NG_<sup>_0_finer-grained Gaus-</sup> sian primitives ( _NG_<sup>_0>NG_),yieldingarefinedset</sup><sup>**G**refine</sup> _t_ + _⌧_<sup>.</sup> The complete Gaussian representation for timestep _t_ + _⌧_ is **G**<sup>total</sup> _t_ + _⌧_<sup>=</sup><sup>**G**init</sup> _t_ + _⌧_<sup>_[_</sup><sup>**G**refine</sup> _t_ + _⌧_<sup>_._</sup> (8) 

This track-guided refinement concentrates modeling capacity near predicted interaction regions, improving geometric accuracy along the robot’s anticipated motion path without requiring a globally high-resolution scene model. 

13532 

**Future Depth Rendering.** To supervise the predictive 3DGS model, we render depth maps from **G**<sup>total</sup> _t_ + _⌧_<sup>at all</sup><sup>_H_+1</sup> timesteps using differentiable alpha compositing, following the rendering formulation of 3D Gaussian Splatting [18]. For a given camera and timestep _t_ + _⌧_ , we consider a pixel ray **r** and collect all Gaussians whose projected ellipses intersect the ray into a set _N_ , sorted in front-to-back order. For the _i_ -th Gaussian, let _di_ denote the depth of its center **_µ_** _i_ and _↵i_ its opacity. The accumulated transmittance is 


representing the probability that the ray passes through all primitives in front of the _i_ -th one. The rendered depth for ray **r** is then 


Since we focus on geometry prediction, colors are omitted. 

To restrict supervision to regions relevant for manipulation, we apply a spatial mask over the robot’s operational workspace. For each ray **r** , we back-project the depth value to obtain a 3D point **p** 3 _d_ ( **r** ). If this point lies within the predefined workspace, we set **M**<sup>spatial</sup> ( **r** ) = 1; otherwise, **M**<sup>spatial</sup> ( **r** ) = 0. The depth loss is formulated as a masked L1 loss over all cameras and timesteps: 


This loss encourages the predicted 3D Gaussian representation to accurately capture the evolution of workspace geometry in regions relevant to downstream manipulation. 

### **3.4. Training and Inference** 

We now introduce how the kinematic and geometric prediction modules are integrated into the transformer via a blockwise causal attention mechanism, and how the full system is jointly trained and deployed efficiently. 

**Block-wise Causal Attention Mechanism.** We adopt a block-wise causal attention structure adapted from _⇡_ 0 as shown in Figure 2, in which the full token sequence is partitioned into five conceptually ordered groups: (1) 2D Token (text and image tokens), (2) 3D Token (history track tokens), (3) 3D Query tokens (future track queries and spatial queries), (4) State Token (proprioceptive token) and (5) Action Noise tokens (used by flow matching). Attention is fully bidirectional within each block, enabling rich intrablock interactions, while cross-block attention is strictly causal: tokens in a given block may attend only to tokens within the same block or to those in preceding blocks. 

This organization imposes a perceptual-to-predictive-tocontrol hierarchy. The transformer fuses 2D language and multi-view observations, incorporates 3D kinematic history, 


Figure 2. **Block-wise Causal Attention Mechanism.** For simplicity, the detailed attention pathways from the 3D Token and State Token blocks to other blocks are not fully drawn. 

forms predictive 3D representations (future trajectories and spatial fields), integrates current proprioception, and generates an action via the action-noise block. The predictive modules thus occupy an intermediate stage, shaping control by injecting structured motion and geometry priors into the transformer. 

**Training Objective.** We train the model end-to-end using a weighted sum of three loss terms: 


where _L_ action is the continuous conditional flow-matching loss from _⇡_ 0, _L_ track is the trajectory prediction loss defined in Eq. 3, and _L_ depth is the masked depth-rendering loss from Eq. 11. The coefficients _λ_ 1, _λ_ 2, and _λ_ 3 balance supervision from action, kinematic, and geometric signals. 

**Inference.** At inference time, all context tokens including text, images, history track tokens and 3D queries are processed by the transformer in a single forward pass, which computes and caches attention Key–Value pairs for subsequent use. The _action expert_ then performs its iterative denoising process for _a_ steps to generate the action chunk **A** _t_ , reusing the cached Key–Value states and invoking only its lightweight action-specific layers. 

Importantly, the predictive 3D Gaussian geometry modules (e.g., the voxel decoder and depth-rendering module) are not executed during inference. They serve purely as training-time supervision signals that shape the transformer’s internal representations with geometric and physical structure, while the action-generation pathway remains unchanged and efficient during deployment. 

## **4. Experiments** 

We first introduce our experimental setup (Sec. 4.1), followed by a benchmarking against state-of-the-art baselines (Sec. 4.2). We then dissect the contribution of our proposed modules through detailed ablation studies (Sec. 4.3) and qualitative analysis (Sec. 4.4). Finally, we assess the model’s performance in real-world scenarios (Sec. 4.5). 

13533 

### **4.1. Experimental Setup** 

**Simulation Benchmarks.** We evaluate our method on two widely recognized robotic manipulation benchmarks. 

- **RoboCasa** [34]: This benchmark features 24 complex long-horizon everyday tasks in kitchen environments. We adopt the challenging Human-50 few-shot setting, where policies are trained using only 50 human demonstrations per task. To rigorously assess generalization capabilities, we follow the standard protocol by evaluating our model over 50 trials per task across five distinct scenes. This evaluation is conducted exclusively on _unseen object instances_ , and includes scenes with _unseen styles_ that were never encountered during training. 

- **LIBERO** [26]: This benchmark is designed to evaluate knowledge transfer and policy generalization across four distinct task suites: LIBERO-Spatial, LIBEROObject, LIBERO-Goal, and LIBERO-Long. We follow the standard protocol for LIBERO, training policies on 50 human-teleoperated demonstrations for each task and evaluating over 50 trials per task (500 trials per suite). 

- **Real-world Evaluation Suite.** To evaluate GeoPredict’s efficacy on real-world tasks requiring precise 3D reasoning, we use an evaluation suite (Figure 3). This suite includes three task categories, using 50 expert trajectories per category for training. Each policy is evaluated for 20 trials per category, where success is defined as successfully grasping the target object and placing it in the correct position. 

- **Spatial Generalization:** The robot is instructed to place the green cube into a plate. We evaluate the policy with the plate located at positions _unseen_ during training, testing its ability to generalize to novel target locations. 

- **Geometry Generalization:** During the 20 evaluation trials, the model must grasp four distinct object types: a small cube, a medium cube, a large cube, and a rectangular prism. Critically, the test set includes cubes with dimensions _not seen_ during training. Furthermore, the rectangular prism is tested in its three unique stable orientations, requiring the policy to adapt its grasp approach based on the perceived object geometry. 

- **Visual Robustness:** This task evaluates the policy’s resilience to visual distractors. The robot must place the yellow cube into the plate while novel and task-irrelevant objects are introduced into the background of the scene, which were absent during training. 

- **Baselines.** Our primary baseline is our VLA backbone, _⇡_ 0 [3], trained without our proposed predictive 3D modules. This comparison directly isolates the contribution of our geometry-aware predictive method. We also compare against a range of state-of-the-art VLA and world-modeling approaches, including BC-Transformer [34], GWM [30], OpenVLA [20], SpatialVLA [37] and UniVLA [5]. 

- **Implementation Details.** A predictive horizon of _H_ = 50 


Figure 3. **Real-world Evaluation Suite.** These settings aim to evaluate the model’s spatial generalization, geometry generalization and robustness to distractors. Each column represents different trials of the same task. 

is used for all tasks. Observations include two environment and one wrist camera views. Depth supervision is applied only to the two 224 _⇥_ 224 environment cameras. For the trajectory-level prediction module (Sec. 3.2), we track _K_ = 8 keypoints (7 joints, 1 end-effector) for LIBERO [26] and RoboCasa [34], and _K_ = 7 (6 joints, 1 end-effector) for the real-world setup. For the predictive 3DGS geometry module (Sec. 3.3), the workspace is 1 _._ 6m _⇥_ 1 _._ 6m _⇥_ 1 _._ 0m with _v_ = 0 _._ 04m voxels. Token and decoder feature dimensions are _C_ = 2048 and _C_<sup>_0_</sup> = 256. We use _NG_ = 4 initial primitives per voxel, and generate _NG_<sup>_0_=64addi-</sup> tional primitives for voxels selected by the track-guided refinement mechanism. All loss weights in Eq. (12) are 1.0. We train for 40,000 iterations using AdamW [29] (LR 2.5e5) on 8 NVIDIA H20 GPUs with a total batch size of 32. The primary metric is Task Success Rate (%). 

### **4.2. Main Results** 

**RoboCasa.** Table 1 details the performance across the 24 RoboCasa sub-tasks. GeoPredict achieves an average success rate of **52.4%** , significantly outperforming all baselines. Notably, it improves upon the _⇡_ 0 baseline success rate of 42.3% by a margin of **10.1%** . This substantial gain underscores the benefit of conditioning the policy on predictive kinematic and geometric priors, especially in the Human-50 few-shot setting where generalization from limited data is critical [34]. Moreover, GeoPredict demonstrates clear advantages over other future prediction methods such as GWM [30] at 39.2% and 2D policies like BCTransformer [34] at 28.8%. Additional large-scale results on RoboCasa Generated-300 are in the Appendix. 

13534 

Table 1. **RoboCasa Simulation Benchmark Results.** Task success rates (%) across 24 sub-tasks and the Average Success Rate (%). **_⇤_** Denotes our fine-tuned experimental results. **Bold** indicates the best performing model. See Appendix for detailed sub-task definitions. 

|**Method**|**PnP**<br>**CTC1**|**PnP**<br>**CTC2**|**PnP**<br>**CTS1**|**PnP**<br>**STC1**|**PnP**<br>**CTS2**|**PnP**<br>**STC2**|**PnP**<br>**CTM**|**PnP**<br>**MTC**|**CM**<br>**SU**|**CM**<br>S**V**|**CB**<br>**PS**|**TSS**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|BC-Transformer [34]|6.0|2.0|2.0|8.0|2.0|6.0|2.0|2.0|0.0|22.0|48.0|54.0|
|GWM [30]|4.0|**18.0**|20.0|22.0|2.0|18.0|14.0|**20.0**|16.0|36.0|**76.0**|**72.0**|
|_⇡_<sup>**_⇤_**</sup><br>0 <sup>(Baseline) [3]</sup>|24.0|6.8|26.8|15.6|11.2|12.8|6.8|7.6|18.4|33.6|74.0|69.6|
|**GeoPredict (Ours)**|**32.4**|8.8|**27.6**|**31.2**|**20.4**|**28.8**|**14.4**|18.0|**28.4**|**49.2**|67.6|70.8|
|**Average Success Rate**|**OSD**|**CSD**|**ODD**|**CDD**|**OD**|**CD**|**TNSF**|**TFSF**|**TNS**|**TFS**|**TNM**|**TFM**|
|28.8|46.0|56.0|28.0|28.0|42.0|80.0|38.0|50.0|32.0|4.0|62.0|70.0|
|39.2|**58.0**|54.0|28.0|50.0|56.0|80.0|52.0|44.0|46.0|**22.0**|64.0|70.0|
|42.3|40.8|**82.0**|55.2|69.2|66.4|96.0|43.6|86.0|43.2|6.0|59.6|60.0|
|**52.4**|40.4|78.8|**87.2**|**70.0**|**77.6**|**96.8**|**72.4**|**94.8**|**60.0**|13.2|**84.8**|**82.8**|


Table 2. **LIBERO Simulation Benchmark Results.** Task success rates (%) across 4 evaluation suites and the Average Success Rate (%). **_⇤_** Denotes our reproduced experimental results. **_†_** Denotes no available standard deviation data. **Bold** indicates the **best** performing model, and underline indicates the **runner-up** model. 

|**Method**|**LIBERO-Spatial**|**LIBERO-Object**|**LIBERO-Goal**|**LIBERO-Long**|**Average**|
|---|---|---|---|---|---|
|Diffusion Policy [9]|78.3_±_1.1|92.5_±_0.7|68.3_±_1.2|50.5_±_1.3|72.4_±_0.7|
|TraceVLA [52]|84.6_±_0.2|85.2_±_0.4|75.1_±_0.3|54.1_±_1.0|74.8_±_0.5|
|Octo [39]|78.9_±_1.0|85.7_±_0.9|84.6_±_0.9|51.1_±_1.3|75.1_±_0.6|
|OpenVLA [20]|84.7_±_0.9|88.4_±_0.8|79.2_±_1.0|53.7_±_1.3|76.5_±_0.6|
|SpatialVLA [37]|88.2_±_0.5|89.9_±_0.7|78.6_±_0.6|55.5_±_1.0|78.1_±_0.7|
|WorldVLA<sup>**_†_** </sup>[6]|87.6|96.2|83.4|60.0|81.8|
|4D-VLA [47]|88.9_±_0.5|95.2_±_0.3|90.9_±_0.4|79.1_±_1.2|88.6_±_0.3|
|DreamVLA<sup>**_†_** </sup>[49]|97.5|94.0|89.5|89.5|92.6|
|_⇡_<sup>**_†_**</sup><br>0 <sup>[3]</sup>|96.8|**98.8**|**95.8**|85.2|94.2|
|OpenVLA-OFT<sup>**_†_** </sup>[19]|95.2|94.2|95.2|93.2|94.5|
|UniVLA<sup>**_†_** </sup>[5]|96.5|96.8|95.6|92.0|95.2|
|_⇡_<sup>**_⇤_**</sup><br>0 <sup>(Baseline) [3]</sup>|96.6_±_0.6|97.2_±_0.8|94.2_±_0.7|87.6_±_1.1|93.9_±_0.4|
|**GeoPredict (Ours)**|**98.0**_±_**0.7**|98.2_±_0.7|95.7_±_0.2|**94.0**_±_**1.0**|**96.5**_±_**0.6**|


**LIBERO.** In Table 2, we show results on the four LIBERO suites [26]. GeoPredict achieves an average success rate of **96.5%** , surpassing the current SOTA method UniVLA [5]. Furthermore, it significantly outperforms strong baselines such as OpenVLA [20] which attains 76.5% by a margin of 20.0%. Our model demonstrates consistently high performance across all four suites, including Spatial (98.0%), Object (98.2%), Goal (95.7%), and the challenging Long (94.0%). This indicates that our method’s geometry-aware training is highly effective and generalizes robustly across diverse tasks and environments. 

### **4.3. Ablation Study** 

**Component Ablation.** Table 3 details our ablation, building the model from the ground up. Starting from the _⇡_ 0 baseline (42.3%), adding the history Track Encoder provides a kinematic prior, improving performance to 44.8%. Adding the Future Track Query ( _Ltrack_ ) for explicit motion prediction further boosts the rate to 47.2%. 

The predictive 3D Gaussian Splatting geometry mod- 

ule yields the most substantial gains. Supervising with _Ldepth_ (using only initial **G**<sup>_init_</sup> ) elevates performance to 49.4%. Jointly training with _Ltrack_ and _Ldepth_ but without the explicit _track-guided refinement_ yields 50.5%. Critically, activating the full _track-guided refinement_ mechanism, which allocates geometric capacity along the predicted future tracks, achieves the peak 52.4%. This final 1.9% gain (50.5% _!_ 52.4%) validates our hypothesis: using kinematic predictions to refine the 3DGS representation provides a superior geometric prior for the policy. 

**Ablation on Depth Rendering.** Table 4 ablates our predictive 3DGS method. Rendering with color (49.2%) offers no benefit over depth-only (49.4%), confirming geometric information alone suffices. Increasing the global initial primitives from _NG_ = 4 to _NG_ = 8 (51.4%) significantly increases training time (12.0 to 19.1 hours/epoch). 

In contrast, our _track-guided refinement_ strategy ( _NG_ = 4 _, NG_<sup>_0_=8) is more efficient, achieving 51.1% at only 15.5</sup> hours/epoch. This highlights the efficiency of allocating geometric capacity to task-relevant interaction regions. Since 

13535 

Table 3. **Ablation Study on RoboCasa Simulation Benchmark.** Future Depth is rendered from initial global Gaussians ( **G**<sup>_init_</sup> ), while Future Depth<sup>**_⇤_**</sup> utilizes the refined total Gaussians ( **G**<sup>_total_</sup> ). Results denote the Average Success Rate (%) across all sub-tasks. 

|History Track|8|4|4|8|4|4|
|---|---|---|---|---|---|---|
|Future Track|8|8|4|8|4|4|
|Future Depth|8|8|8|4|4|8|
|Future Depth<sup>**_⇤_**</sup>|8|8|8|8|8|4|
|**Average SR**|42.3|44.8|47.2|49.4|50.5|52.4|


Table 4. **Ablation Study on Depth Rendering.** _NG_ and _NG_<sup>_0_de-</sup> note the number of Gaussian primitives per voxel for the initial and refined stages, respectively. Color indicates RGB image reconstruction. **Time / Epoch** represents the training time per epoch in hours, and **Average SR** is the Average Success Rate (%). 

|_NG_|4|4|8|4|4|
|---|---|---|---|---|---|
|_N _<sup>_0_</sup><br>_G_|8|8|8|8|64|
|Color|4|8|8|8|8|
|**Time / Epoch**|12.3|12.0|19.1|15.5|15.7|
|**Average SR**|49.2|49.4|51.4|51.1|52.4|


Table 5. **Real-World Experiment Results.** Task success rates (%) across three distinct settings: Spatial, Geometry, and Robustness. 

|**Method**|**Spatial**|**Geometry**|**Robustness**|
|---|---|---|---|
|_⇡_0 (Baseline) [3]|60.0|50.0|35.0|
|**GeoPredict (Ours)**|85.0|95.0|90.0|


these regions are a small fraction of the volume, we can increase _NG_<sup>_0_withnegligibleoverhead.Setting</sup><sup>_N 0_</sup> _G_<sup>=64</sup> yields our peak 52.4% success rate at a near-identical 15.7 hours. Therefore, we adopt _NG_ = 4 and _NG_<sup>_0_=64as our</sup> final configuration. 

### **4.4. Qualitative Analysis** 

Figure 4 provides a qualitative visualization of our predictive 3DGS geometry module, which compares the predicted future depths at various timesteps ( _t_ + 1 _, t_ + 10 _, t_ + 20). While the **initial** Gaussians ( **G**<sup>_init_</sup> ) capture only the coarse scene layout, the **refined** Gaussians ( **G**<sup>_total_</sup> ) exhibit significantly sharper geometric details, particularly surrounding the robotic arm. This visually confirms that our refinement mechanism produces a more precise and geometricallyfaithful prediction of the future, which in turn provides a superior conditional prior for the action expert. 

### **4.5. Real-World Experiments** 

We validate GeoPredict on a DISCOVER robotic arm to assess performance on tasks demanding explicit 3D reasoning. As detailed in Table 5, GeoPredict significantly outperforms the _⇡_ 0 [3] baseline across all tasks. Specifically, in the Spatial and Robustness tasks, our method achieves success rates of 85.0% and 90.0% respectively, surpassing the 


Figure 4. **Qualitative Comparisons of Future Depth Rendering.** Visualizations are shown for timesteps _t_ + 1 _, t_ + 10 _,_ and _t_ + 20. Red boxes highlight the improvements in fine-grained geometric details. Best viewed zoomed in. 

baseline scores of 60.0% and 35.0% and demonstrating superior spatial generalization and resilience to distractors. In the Geometry task, GeoPredict attains a 95.0% success rate compared to 50.0% for the baseline. This 45.0% improvement on tasks involving object sizes absent from the training set strongly indicates that our predictive 3DGS module endows the policy with a generalizable understanding of 3D geometry, enabling adaptive grasping capabilities that the 2D-centric _⇡_ 0 baseline lacks. Moreover, since our method explicitly encodes motion history via the Track Encoder, the Appendix provides a dedicated real-world experiment to validate the effectiveness of this historical context. 

## **5. Conclusion** 

We presented **GeoPredict** , a geometry-aware VLA framework enhancing continuous-action policies with predictive kinematic and geometric priors. By forecasting robot trajectories and workspace geometry via track-guided 3DGS, GeoPredict introduces future-aware structure into the transformer while keeping inference lightweight. Extensive experiments show consistent superiority over strong baselines in tasks requiring precise 3D reasoning, geometric robustness and long-horizon physical consistency. While acquiring multi-view RGB-D and camera extrinsics presents scaling challenges, the increasing availability of calibrated depth in modern datasets and commodity hardware mitigates these concerns. Ultimately, our training-time predictive supervision provides a promising direction for reliable, geometry-aware, and grounded VLA controllers. 

13536 

## **Acknowledgment** 

This work is supported by the Shenzhen Science and Technology Program (Grant No. ZDCY20250901113000001) and the 1+1+1 CUHK-CUHK(SZ)-GDSTC Joint Collaboration Fund (Grant No. 2025A0505000079). We gratefully acknowledge DISCOVER Robotics for providing hardware support. 

## **References** 

- [1] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _CoRR_ , 2024. 3 

- [2] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pre-trained imageediting diffusion models. In _NeurIPS 2023 Workshop on Goal-Conditioned Reinforcement Learning_ , 2023. 2 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _⇡_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv.2410.24164_ , 2024. 1, 2, 3, 6, 7, 8, 4 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2 

- [5] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2505.06111_ , 2025. 2, 6, 7 

- [6] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 1, 2, 7 

- [7] Xiaoyu Chen, Hangxing Wei, Pushi Zhang, Chuheng Zhang, Kaixin Wang, Yanjiang Guo, Rushuai Yang, Yucen Wang, Xinquan Xiao, Li Zhao, et al. Villa-x: enhancing latent action modeling in vision-language-action models. _arXiv preprint arXiv:2507.23682_ , 2025. 1 

- [8] Yi Chen, Yuying Ge, Weiliang Tang, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 19752– 19763, 2025. 1 

- [9] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action dif- 

fusion. _The International Journal of Robotics Research_ , 44 (10-11):1684–1704, 2025. 7 

- [10] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 2 

- [11] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18995–19012, 2022. 1 

- [12] Gunshi Gupta, Karmesh Yadav, Yarin Gal, Dhruv Batra, Zsolt Kira, Cong Lu, and Tim GJ Rudner. Pre-trained textto-image diffusion models are versatile representation learners for control. _Advances in Neural Information Processing Systems_ , 37:74182–74210, 2024. 1 

- [13] Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2020. 2 

- [14] Danijar Hafner, Kuang-Huei Lee, Ian Fischer, and Pieter Abbeel. Deep hierarchical planning from pixels. _Advances in Neural Information Processing Systems_ , 35:26091–26104, 2022. 

- [15] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. In _NeurIPS 2023 Foundation Models for Decision Making Workshop_ , 2023. 2 

- [16] Tao Hu, Shu Liu, Yilun Chen, Tiancheng Shen, and Jiaya Jia. Efficientnerf efficient neural radiance fields. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12902–12911, 2022. 2 

- [17] Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _Forty-second International Conference on Machine Learning_ , 2025. 1, 2 

- [18] Bernhard Kerbl, Georgios Kopanas, Thomas Leimkuehler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Transactions on Graphics (TOG)_ , 42(4):1–14, 2023. 2, 4, 5 

- [19] Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 7 

- [20] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _Conference on Robot Learning_ , pages 2679–2713. PMLR, 2025. 2, 3, 6, 7 

- [21] Peiyan Li, Yixiang Chen, Hongtao Wu, Xiao Ma, Xiangnan Wu, Yan Huang, Liang Wang, Tao Kong, and Tieniu Tan. Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models. _arXiv preprint arXiv:2506.07961_ , 2025. 2 

13537 

- [22] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _CoRR_ , 2024. 1, 2 

- [23] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 1 

- [24] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. In _ICLR_ , 2024. 1 

- [25] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 2, 3 

- [26] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 6, 7 

- [27] Zeyi Liu, Shuang Li, Eric Cousineau, Siyuan Feng, Benjamin Burchfiel, and Shuran Song. Geometry-aware 4d video generation for robot manipulation. _arXiv preprint arXiv:2507.01099_ , 2025. 2 

- [28] William E Lorensen and Harvey E Cline. Marching cubes: A high resolution 3d surface construction algorithm. In _Seminal graphics: pioneering efforts that shaped the field_ , pages 347–353. 1998. 2 

- [29] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _International Conference on Learning Representations_ , 2017. 6 

- [30] Guanxing Lu, Baoxiong Jia, Puhao Li, Yixin Chen, Ziwei Wang, Yansong Tang, and Siyuan Huang. Gwm: Towards scalable gaussian world models for robotic manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9263–9274, 2025. 1, 2, 6, 7, 3 

- [31] Vincent Micheli, Eloi Alonso, and Franc¸ois Fleuret. Transformers are sample-efficient world models. In _Deep Reinforcement Learning Workshop NeurIPS 2022_ , 2022. 2 

- [32] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 65(1):99–106, 2021. 2 

- [33] Thomas M¨uller, Alex Evans, Christoph Schied, and Alexander Keller. Instant neural graphics primitives with a multiresolution hash encoding. _ACM transactions on graphics (TOG)_ , 41(4):1–15, 2022. 2 

- [34] Soroush Nasiriany, Abhiram Maddukuri, Lance Zhang, Adeet Parikh, Aaron Lo, Abhishek Joshi, Ajay Mandlekar, and Yuke Zhu. Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ , 2024. 6, 7, 1, 2, 3 

- [35] Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 652–660, 2017. 2 

- [36] Zezhong Qian, Xiaowei Chi, Yuming Li, Shizun Wang, Zhiyuan Qin, Xiaozhu Ju, Sirui Han, and Shanghang Zhang. Wristworld: Generating wrist-views via 4d world models for robotic manipulation. _arXiv preprint arXiv:2510.07313_ , 2025. 1 

- [37] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2, 6, 7, 1 

- [38] Xuanchi Ren, Yifan Lu, Hanxue Liang, Zhangjie Wu, Huan Ling, Mike Chen, Sanja Fidler, Francis Williams, and Jiahui Huang. Scube: Instant large-scale scene reconstruction using voxsplats. _Advances in Neural Information Processing Systems_ , 37:97670–97698, 2024. 2 

- [39] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 7 

- [40] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. 2 

- [41] Guanjun Wu, Taoran Yi, Jiemin Fang, Lingxi Xie, Xiaopeng Zhang, Wei Wei, Wenyu Liu, Qi Tian, and Xinggang Wang. 4d gaussian splatting for real-time dynamic scene rendering. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 20310–20320, 2024. 2 

- [42] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pre-training for visual robot manipulation. In _ICLR_ , 2024. 2 

- [43] Zhirong Wu, Shuran Song, Aditya Khosla, Fisher Yu, Linguang Zhang, Xiaoou Tang, and Jianxiong Xiao. 3d shapenets: A deep representation for volumetric shapes. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 1912–1920, 2015. 2 

- [44] Lei Xiao, Jifeng Li, Juntao Gao, Feiyang Ye, Yan Jin, Jingjing Qian, Jing Zhang, Yong Wu, and Xiaoyuan Yu. Avavla: Improving vision-language-action models with active visual attention. _arXiv preprint arXiv:2511.18960_ , 2025. 2 

- [45] Qiangeng Xu, Zexiang Xu, Julien Philip, Sai Bi, Zhixin Shu, Kalyan Sunkavalli, and Ulrich Neumann. Pointnerf: Point-based neural radiance fields. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 5438–5448, 2022. 2 

- [46] Yunzhi Yan, Haotong Lin, Chenxu Zhou, Weijie Wang, Haiyang Sun, Kun Zhan, Xianpeng Lang, Xiaowei Zhou, and Sida Peng. Street gaussians: Modeling dynamic urban scenes with gaussian splatting. In _European Conference on Computer Vision_ , pages 156–173. Springer, 2024. 2 

- [47] Jiahui Zhang, Yurui Chen, Yueming Xu, Ze Huang, Yanpeng Zhou, Yu-Jie Yuan, Xinyue Cai, Guowei Huang, Xingyue Quan, Hang Xu, et al. 4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene calibration. _arXiv preprint arXiv:2506.22242_ , 2025. 7, 1 

13538 

- [48] Weipu Zhang, Gang Wang, Jian Sun, Yetian Yuan, and Gao Huang. Storm: Efficient stochastic transformer based world models for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:27147–27166, 2023. 2 

- [49] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, XinQiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, et al. Dreamvla: A vision-languageaction model dreamed with comprehensive world knowledge. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 1, 2, 7 

- [50] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 1 

- [51] Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, YaQin Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22508–22519, 2025. 1, 2 

- [52] Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 2, 7 

- [53] Yifan Zhong, Fengshuo Bai, Shaofei Cai, Xuchuan Huang, Zhang Chen, Xiaowei Zhang, Yuanfei Wang, Shaoyang Guo, Tianrui Guan, Ka Nam Lui, et al. A survey on visionlanguage-action models: An action tokenization perspective. _arXiv preprint arXiv:2507.01925_ , 2025. 1, 2 

- [54] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 1 

13539 

