---
title: "GenHOI: Contact-Aware Humanoid-Object Interaction by Imitating Generated Videos without Task-Specific Training"
date: "2026-06-11"
authors: "Zhihai Bi; Qiang Zhang; Guoyang Zhao; Jiahang Cao; Xueyin Luo; Yushan Zhang"
url: https://arxiv.org/abs/2606.12995
pdf: https://arxiv.org/pdf/2606.12995
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.12995)** / [論文ページ](https://arxiv.org/abs/2606.12995)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **GenHOI: Contact-Aware Humanoid-Object Interaction by Imitating Generated Videos without Task-Specific Training** 

Zhihai Bi<sup>1</sup> , Qiang Zhang<sup>2</sup> , Guoyang Zhao<sup>1</sup> , Jiahang Cao<sup>3</sup> , Xueyin Luo<sup>1</sup> , Yushan Zhang<sup>1</sup> , Jinglan Xu<sup>1</sup> , Ruoyu Geng<sup>1</sup> , Yulin Li<sup>4</sup> , Andrew F. Luo<sup>3</sup> , and Jun Ma<sup>1</sup><sup>_,_†</sup> 

      - 1The Hong Kong University of Science and Technology (Guangzhou) 

   - 2Artificial General Intelligence Institute, University of Science and Technology of China 

- 3The University of Hong Kong 4National University of Singapore †Corresponding author 


Fig. 1. **The proposed GenHOI framework enables a humanoid robot to perform diverse object-interaction tasks.** 

**_Abstract_ —Humanoid-Object Interaction (HOI) is essential for deploying humanoid robots in human-centered environments, yet it remains challenging due to the tight coupling between dynamic balance and stable interaction with diverse objects. Existing methods often require time-consuming task-specific policy training or rely on rigid trajectory replay, which limits their ability to accommodate novel interaction scenarios. In this work, we present** **_GenHOI_ , a simple yet effective framework that enables humanoid robots to perform diverse object-interaction tasks in a zero-shot manner by directly imitating a single generated video, without task-specific training or physical demonstration data. GenHOI first reconstructs the robot-object scene in simulation and renders a first-frame image, which conditions the synthesis of a task-oriented interaction video in conjunction with the language command. The generated video is then analyzed to identify interaction-relevant contact events and estimate handobject contact regions, which are encoded as object-centric geometric constraints that convert visual interaction cues into physically grounded optimization priors. Guided by these priors, the reference motion recovered from the video is refined and smoothed to resolve the scale ambiguity inherent in 2D video generation, while adapting a single reference trajectory to unseen robot-object relative poses. The optimized trajectory is finally executed by a closed-loop tracking controller. We validate the proposed framework in extensive simulation and real-world experiments across diverse object-interaction tasks, including box grasping, asymmetric bimanual chair carrying, table lifting from below, and cylindrical-object enveloping. The project page is available at https://genhoi-humanoid.github.io/.** 

## I. INTRODUCTION 

Humanoid robots hold great promise for operating in human-centered environments [1]. Despite recent progress in locomotion, versatile Humanoid-Object Interaction (HOI) 

remains challenging because physical interaction with objects is tightly coupled with whole-body stability. The robot must simultaneously coordinate its motion, contact locations, and interaction forces across diverse objects [2]. 

Current HOI methods either directly mimic a single reference trajectory [3] or learn task policies regularized by motiondistribution priors, such as motion-prior models [4] and AMPbased discriminators [5]. Essentially, these methods largely ground interaction learning in pre-collected motion data and therefore entail task-specific demonstrations, reward design, and policy training for each new task or object category. Moreover, since the behaviors are tied to reference motions, they often fail to generalize when the robot-object relative pose, object geometry, or contact affordance shifts beyond the training distribution [6]. 

Recently, video generation models have made remarkable progress. Representative models such as Sora [7] and Seedance [8] are capable of synthesizing videos that increasingly resemble the visual appearance and motion dynamics of the real physical world. Compared with existing model-based or datadriven methods for HOI, planning future actions through video generation offers a potentially more generalizable alternative. Motivated by this observation, we explore a new paradigm for humanoid loco-manipulation: **Can a humanoid robot leverage the generalization capability of video generation models to perform loco-manipulation tasks, such as chair carrying, by imitating a single generated video?** 

Recent efforts that leverage generated videos for robot manipulation can be broadly grouped into two lines of work. The first uses video generation models as auxiliary tools for 

TABLE I COMPARISON WITH RELATED WORKS 

|**Method**<br>No|Task-Specific<br>Training|Onboard<br>Sensing|Steerable<br>Interaction|
|---|---|---|---|
|HDMI [15]|✗|✗|✗|
|Pro-HOI [6]|✗|✓|✓|
|ExoActor [13]|✓|✗|✗|
|Dream2Act [14]|✓|✗|✗|
|**Ours**|✓|✓|✓|


policy learning, such as augmenting training data [9] or learning video-based representations [10]. Although effective in improving generalization, these methods still depend on taskspecific policy training and real robot interaction data. The second line of work seeks to directly translate generated videos into robot behaviors, avoiding the need for additional policy learning [11]. However, existing demonstrations are mainly limited to fixed-base manipulators, where the workspace is constrained, and the robot-object interaction is relatively simple [12]. In contrast, extending direct video imitation to humanoid loco-manipulation is substantially more challenging, requiring the robot to coordinate whole-body locomotion with bimanual manipulation while establishing stable contacts with geometrically complex objects. In addition, spatial and metric inconsistencies between generated 2D videos and the real environment can lead to inaccurate contact localization and motion execution errors, a limitation largely overlooked by prior work [13], [14]. Moreover, existing paradigms are often tied to the scene configuration depicted in the video and therefore cannot generalize to unseen object poses. Comparisons with related approaches are presented in Table I. 

To address these limitations, we propose GenHOI, a locomanipulation framework for humanoid robots, as shown in Fig. 2. The framework consists of four key modules: real-tosim video generation, contact-aware geometric constraint extraction, geometry-guided trajectory optimization, and closedloop trajectory tracking. First, the real-to-sim video generation module reconstructs the robot and target object in simulation and uses a simulator-rendered first-frame image, together with a language command, to condition a video diffusion model for synthesizing the video without relying on external cameras. Second, to mitigate the spatial and metric inconsistencies of the motion recovered from the 2D video, we derive contactaware geometric constraints from the generated video and use them to guide trajectory optimization, thereby aligning the trajectory with the real robot workspace. Notably, this decoupled design allows a single trajectory to generalize across different robot-object relative poses by updating only the optimization constraints. Finally, the optimized trajectory is executed through closed-loop trajectory tracking with a general-purpose motion controller [16]. The main contributions are summarized as follows: 

- We propose an HOI framework that enables a humanoid robot to perform diverse object-interaction tasks in a zero-shot manner by directly imitating a single generated video, without requiring task-specific policy training or physical demonstration data. 

- We introduce a contact-aware geometric constraint extraction module that identifies contact events in generated videos and estimates hand-object contact regions to construct object-centric geometric constraints, thereby converting visual cues into physically grounded priors. 

- We develop a geometry-guided trajectory optimization pipeline that uses the extracted constraints to refine and smooth the reference motion, which mitigates metric discrepancies and enables a single reference trajectory to generalize to unseen robot-object relative poses. 

- We validate the proposed framework through extensive simulation and real-world experiments. The results show that our method enables humanoid robots to learn diverse object-interaction behaviors more efficiently than the baselines while achieving stronger generalization. 

## II. RELATED WORK 

## _A. Humanoid Loco-Manipulation_ 

In recent years, humanoid loco-manipulation has attracted increasing attention. Some studies are inspired by the success of reinforcement learning (RL) in robotic locomotion and extend RL-based approaches to humanoid loco-manipulation tasks [17]. For example, DoorMan [18] designs a multi-stage reward function to train a policy capable of performing diverse articulated-object interaction tasks using only RGB perception. Similarly, VIRAL [2] leverages reinforcement learning to achieve pick-and-place tasks. However, these approaches typically rely on task-specific reward engineering. In particular, for long-horizon, contact-rich tasks, training RL policies from scratch often requires curriculum learning, multi-stage setups, and extensive hyperparameter tuning. 

Compared with training RL policies from scratch, a more efficient paradigm leverages offline human-object interaction demonstrations. These demonstrations are typically retargeted to the humanoid robot and then used to train a tracking policy [19]. For example, HDMI [15] extracts human and object motion trajectories from videos and trains an RL-based policy for interactions. The policy performs tasks such as door traversal robustly. Similarly, OmniRetarget [3] introduces a mesh-based retargeting method that generates higher-quality interaction trajectories, enabling more challenging tasks such as fast platform climbing. Despite their effectiveness on specific tasks, they rely on carefully engineered preprocessing pipelines, including manually predefined robot-object contact points. Moreover, because they mainly learn to track fixed demonstration trajectories, they tend to generalize poorly to changes in robot-object relative pose. 

Recently, inspired by the success of LLM and VLM, researchers explore more scalable learning paradigms, aiming to improve generalization through large-scale datasets [20], [21]. Representative examples include EgoScale [22], which trains a VLA model on tens of thousands of hours of human egocentric videos, and Ψ0 [23], which pretrains a VLM backbone on large-scale egocentric videos and further adapts it using highquality real-world humanoid robot data. By combining broad pretraining on human video data with robot-specific posttraining, these methods exhibit improved potential for crosstask transfer. However, their reliance on massive datasets and 

substantial computational resources limits their practicality for follow-up research. 

In contrast to these paradigms, we explore a novel framework for humanoid loco-manipulation: directly imitating actions from generated videos, without relying on physical demonstrations or task-specific policy training. 

## _B. Video Generation for Robotics_ 

Recent advances in video generation models have enabled the synthesis of high-fidelity, controllable videos of robotic actions, offering a new technical pathway for robot learning [24]. A common use of such models is data synthesis. DexImit [25], for instance, synthesizes bimanual dexterous manipulation sequences and converts them into training data for policy learning. DreamGen [26] instead fine-tunes a video world model on a target robot, using it to generate synthetic data for downstream visuomotor policy training. Compared with manually collected demonstrations, such approaches can substantially reduce the cost of data acquisition. 

Beyond data synthesis, recent work directly uses video generation models as policy backbones, jointly modeling future video frames and action sequences conditioned on language instructions and initial observations [27]. For example, DreamZero [28] builds on a pretrained video diffusion model to learn diverse skills from heterogeneous robot data. Unlike data-synthesis methods, this paradigm offers a more direct route from generative modeling to policy learning. However, the large model size and high inference latency of existing approaches limit their evaluation primarily to fixed-base manipulation, leaving their applicability to real-time humanoid loco-manipulation largely unexplored. 

Another emerging direction seeks to recover executable control signals directly from generated videos without additional policy training. RIGVid [12] guides manipulation by estimating the target-object pose in each video frame and tracking the extracted trajectory with the end effector under an initial grasp. Dream2Act [14] instead extracts 3D robot coordinates from generated videos for tracking control. However, it assumes geometric consistency between the generated video and the real scene, leaving stable contact formation unresolved. Moreover, these methods rely on manually captured images as input and cannot be deployed in closed-loop settings using only onboard robot sensing. 

To bridge these gaps, we reconstruct the robot and target object in simulation and use a simulator-rendered image for video generation. Furthermore, we extract contact-aware geometric constraints from the generated video to guide trajectory optimization. This design reduces spatial and metric discrepancies during real-world execution while enabling generalization across varying robot-object relative poses. 

## III. METHODOLOGY 

In this work, we propose GenHOI, a humanoid locomanipulation framework that directly imitates generated videos without task-specific training, as illustrated in Fig. 2. Specifically, the proposed framework comprises four key stages: real-to-sim video generation (Sec. III-A), contact-aware 

geometric constraint extraction (Sec. III-B), geometry-guided trajectory optimization (Sec. III-C), and closed-loop trajectory tracking (Sec. III-D). 

## _A. Real-to-Sim Video Generation_ 

In contrast to prior works that rely on external cameras to capture third-person images for video generation [13], our goal is to enable the robot to generate such videos using only onboard sensors, thereby supporting autonomous operation. To this end, we adopt a simple yet effective digital-twin-based solution, as shown in Fig. 2(A). Specifically, assuming the object mesh is available, we first estimate the 6D pose of the object relative to the robot using onboard RGB-D observations based on foundationPose [29] or AprilTag. The robot and the object are then rendered in a MuJoCo simulation environment. Thanks to the flexibility of the simulator, virtual cameras can be placed arbitrarily to obtain third-person views of the robotobject interaction. Given the simulated first-frame image and the corresponding language command, we then use Seedance 2.0 to generate a video (5 s) from a fixed viewpoint (for details see Appendix A). 

Given the generated video with _N_ frames, we then recover the robot’s 3D pose sequence by following a standard pipeline widely adopted in prior work [30]. Specifically, we first use GVHMR [31] to estimate the 3D pose sequence from the input video, and then retarget it to the humanoid robot using GMR [32], yielding the raw robot 3D pose trajectory: 


where the **h**<sup>root</sup> _i ∈_ R<sup>6</sup> indicates the 6D pose of the robot root, and **h**<sup>joint</sup> _i ∈_ R<sup>29</sup> denotes the robot joint angles. 

## _B. Contact-Aware Geometric Constraint Extraction_ 

Due to depth ambiguity, occlusion, and perspective effects in monocular videos, the raw 3D pose trajectory recovered from generated videos often exhibits substantial inaccuracies in the global root motion and hand trajectories. Such errors can lead to physically inconsistent robot-object interactions during execution. To improve the feasibility of interaction, our core idea is to refine the raw 3D pose trajectory using hand-object contact poses. 

To this end, we first recover accurate 3D hand positions from monocular videos. We uniformly sample frames from the last _N_ seconds of the generated video at 0.5 s intervals and concatenate them in temporal order into a single composite image, which is fed into Doubao-Seed-2.0, a VLM model, to identify the key frame where the humanoid first establishes physical interaction with the object. Here, _N_ defines the temporal search window. We set _N_ = 3, which covers the typical contact interval while keeping the candidate set compact for efficient VLM-based key-frame selection (for details see Appendix B). This frame is referred to as the terminal interaction frame in the subsequent optimization. We then estimate its monocular depth using Depth Anything [33]. Since the predicted depth is defined only up to an unknown scale, we recover its metric scale using the digital-twin setup, where the camera parameters and object pose in the camera frame are available. 


Fig. 2. **Overview of the proposed GenHOI framework.** GenHOI first reconstructs the robot-observed scene in simulation and generates a reference video from the rendered image and text instructions (A). It then extracts contact-aware geometric constraints from the generated video via key-frame selection, metric depth recovery, hand segmentation, and contact point detection (B). These constraints are incorporated into trajectory optimization to refine the original trajectory into a physically feasible hand-object interaction trajectory (C), which is finally executed through closed-loop tracking in both simulation and real-world experiments (D). 

With the restored metric depth, we next use VitPose [34] to extract 2D keypoints for the left and right hands and lift them to coarse 3D positions in the world frame. However, due to errors in depth restoration and potential hand occlusions, these coarse hand positions may deviate from the true hand locations and therefore require further refinement. If the hand is visible and not occluded by the object, we refine the coarse hand position to the nearest point on the object mesh as the target contact position. Otherwise, we cast a ray from the camera center through the 3D hand position and use its last intersection with the object mesh as the final contact position. The hand visibility can be determined based on the color region within the hand mask. This process yields objectconsistent target hand positions **p**<sup>_⋆_</sup> _L_<sup>_,_</sup><sup>**p**</sup><sup>_⋆_</sup> _R_<sup>_∈_R3 in the world frame.</sup> Since monocular depth and 2D keypoints do not provide reliable hand orientations, we retain the hand orientations from the recovered humanoid motion at the terminal interaction frame. Let **R**<sup>_⋆_</sup> _L_<sup>_,_</sup><sup>**R**</sup><sup>_⋆_</sup> _R_<sup>_∈SO_(3)denotethecorrespondingleft</sup> and right hand orientations. Together with the target hand positions, these quantities define the contact-aware geometric constraints used in the subsequent optimization. 

## _C. Geometry-Guided Trajectory Optimization_ 

Given a raw robot 3D pose trajectory **h** _i, i_ = 1 _, ··· , N_ , together with the extracted contact-aware terminal hand pose constraints, we refine the trajectory such that the resulting motion becomes more consistent with the desired robotobject interaction. Directly optimizing the full-body humanoid motion would require jointly considering gait planning, foot contact transitions, and balance constraints, resulting in a 

highly coupled and computationally challenging problem [35]. Instead, we perform a lightweight terminal refinement over the root pose and upper-body joints. 

Specifically, we optimize a subset of the terminal full-body state: 


where ( _x, y, z_ ) denotes the root position, _ψ_ denotes the root yaw angle, _φ_ denotes the waist pitch angle, and **q** _∈_ R<sup>14</sup> contains the upper-body arm joint angles. Given **h**<sup>ˆsub</sup> _N_<sup>,theworld-frame</sup> poses of the left and right hands are computed through forward kinematics: 


where **T** root _∈ SE_ (3) is the homogeneous transformation matrix of the robot root, and **T** root _→L_ ( _·_ ) and **T** root _→R_ ( _·_ ) denote the forward kinematic mappings from the root frame to the left and right hand frames, respectively. 

For a current pose **T** = ( **R** _,_ **p** ) and a target pose **T**<sup>_⋆_</sup> = ( **R**<sup>_⋆_</sup> _,_ **p**<sup>_⋆_</sup> ), we define the 6D pose error as: 


where the first three dimensions correspond to the translational error, and the last three dimensions represent the rotational error in the tangent space of _so_ (3). 

For bimanual object-holding motions, directly aligning the hands with the estimated object surface may lead to marginal contact under position-controlled execution. To encourage a stable holding interaction, we introduce a compliance-aware 

inward bias inspired by a virtual spring model. Let **p**<sup>_⋆_</sup> _L_<sup>and</sup><sup>**p**</sup><sup>_⋆_</sup> _R_ be the translational components of **T**<sup>_⋆_</sup> _L_<sup>and</sup><sup>**T**</sup><sup>_⋆_</sup> _R_<sup>,respectively.</sup> We define the inter-hand direction as: 


The target hand positions are then slightly displaced toward each other: 


where _δ >_ 0 is a small inward displacement. This inward displacement acts as a virtual compression between the two hands and induces a nominal holding tendency proportional to the imposed displacement, following the virtual spring relation _F_ = _kδ_ . Since the video does not provide reliable force information, this term is used as a heuristic compliance prior rather than an explicit contact-force estimate. The adjusted terminal hand pose targets are defined as: 


Using these targets, we define the geometric residual as: 


## _D. Closed-Loop Trajectory Tracking_ 

Once the optimized trajectory is obtained, it is executed on the humanoid robot through a closed-loop tracking controller. Specifically, the robot first performs real-time localization using its onboard LiDAR to estimate its current global pose during execution. Based on this feedback, the lower body tracks the optimized global root trajectory in the Cartesian space, i.e., the root translation along the _x_ , _y_ , and _z_ axes, while the upper body tracks the optimized joint trajectory, including the waist pitch angle and the arm joint angles of both hands. This decoupled tracking strategy allows the lower body to realize stable locomotion while enabling the upper body to maintain the desired hand-object interaction. The tracking controller is built upon the open-source Sonic general-purpose motion controller [16]. 

## IV. EXPERIMENTS 

This section presents the experimental results to systematically evaluate the proposed method. Specifically, we organize our experiments to answer the following questions: _Q_ 1: How does GenHOI perform compared to other methods? (Sec. IV-B) _Q_ 2: What key factors influence the performance of video generation and downstream execution for HOI? (Sec. IV-C) _Q_ 3: How robust are the key modules, including the VLMbased key frame selection and hand-object contact estimation? (Sec. IV-D) _Q_ 4: Can the framework enable the humanoid to perform different loco-manipulation tasks in real-world scenarios? (Sec. IV-E) 

where the hand-specific weighting matrix is defined as: 


Here, _we_<sup>_p_and</sup><sup>_wR_</sup> _e_ denote the translational and rotational weights for hand _e_ , respectively. **h**<sup>sub</sup> _N_ is the terminal state of the raw trajectory, and _w_ reg regularizes the solution toward the terminal state recovered from the generated video. This regularization prevents unnecessary deviations from the demonstrated motion while allowing the terminal hand poses to better satisfy the contact-aware geometric constraints. 

The terminal refinement is formulated as the following constrained nonlinear least-squares problem: 


The optimized terminal state **h**<sup>opt</sup> _N_ adjusts the root pose, waist pitch, and upper-body arm joints to align both hands with the compliance-aware object interaction targets. In practice, the resulting terminal correction is smoothly propagated to the preceding frames within a short temporal window to avoid abrupt motion changes (for details see Appendix C). 

## _A. Experimental Setup_ 

We conduct both simulation and real-world experiments on the Unitree G1 humanoid robot platform. In simulation, the experiments are performed in MuJoCo, where the global poses of the robot and target objects are directly obtained from the simulator. For real-world experiments, the humanoid robot is equipped with a Mid360 LiDAR for global relocalization [36] and an Intel RealSense D435i camera for object pose estimation [29]. All algorithms run on a single workstation equipped with an Intel Core i9 3.60 GHz CPU and an NVIDIA GeForce RTX 4080 GPU. The workstation communicates with the robot over a local area network. 

For the geometry-guided trajectory optimization, we use the following hyperparameters: _we_<sup>_p_= 20,</sup><sup>_wR_</sup> _e_<sup>= 5,</sup><sup>_w_reg= 0</sup><sup>_._25, and</sup> _δ_ = 0 _._ 06 m. The bounds on the root height and waist pitch are set to _z_<sup>min</sup> = 0 _._ 3 m, _z_<sup>max</sup> = 0 _._ 8 m, _φ_<sup>min</sup> = 0 _._ 0 rad, and _φ_<sup>max</sup> = 0 _._ 58 rad, respectively. The joint limits _q_<sup>min</sup> _j_ and _q_<sup>max</sup> _j_ are specified according to the robot URDF model. 

## _B. Comparison with Baselines_ 

The most closely related works to ours are Dream2Act [14] and ExoActor [13], both of which extract body trajectories from videos and directly track them for control. We therefore adopt **ExoActor** as a representative baseline for this line of work. To assess the importance of accurate hand–object contact localization, we introduce an ablation baseline, **W/o Cont. Det.** , which removes the contact-point detection module 


Fig. 3. **Qualitative comparison of different methods on loco-manipulation tasks across four object categories.** Red crosses denote failed trials, and green check marks denote successful task completion. 

TABLE II 

QUANTITATIVE COMPARISON OF SUCCESS RATE AND HAND-CONTACT POINT ERROR ACROSS DIFFERENT OBJECTS 

||||Success R|ate _↑_||H|and–Con|tact Poin|t Error [m]|_↓_|
|---|---|---|---|---|---|---|---|---|---|---|
|Methods|Box|Chair|Table|Cylinder|Ave.|Box|Chair|Table|Cylinder|Ave.|
|ExoActor [13]|2/15|0/15|1/15|4/15|11.7%|0.54|0.79|1.12|0.53|0.75|
|W/o Traj. Smooth.|7/15|2/15|2/15|6/15|28.3%|0.32|0.27|0.48|0.41|0.37|
|W/o Cont. Det.|5/15|4/15|9/15|7/15|41.7%|0.22|0.20|0.45|0.22|0.27|
|W/o Inward Bias|4/15|2/15|10/15|10/15|43.3%|0.19|0.15|0.41|**0.18**|0.23|
|**Ours**|**11/15**|**10/15**|**13/15**|**12/15**|**76.7%**|**0.12**|**0.15**|**0.40**|0.20|**0.22**|


and instead uses the coarse 3D hand positions lifted from 2D hand masks as optimization targets. Besides, to evaluate the contributions of trajectory smoothing and the inward compressive bias, we further introduce two ablation variants, denoted as **W/o Traj. Smooth.** and **W/o Inward Bias** , respectively. For a broader comparison, we also include **HDMI** [15], a representative task-specific policy-learning method. We evaluate all methods across four tasks of varying difficulty, including box grasping, asymmetric bimanual chair carrying (i.e., holding the seat with one hand while stabilizing the backrest with the other), table lifting from below, and cylindricalobject enveloping. For quantitative evaluation, we report task success rate, hand-contact point error, skill acquisition time, and generalization to out-of-distribution (OOD) object poses. Specifically, the hand-contact point error is defined as the sum of the Euclidean distances between each hand and its corre- 

sponding target contact point. To ensure a fair comparison and decouple the impact of video generation failures, all methods are evaluated on the same set of successfully generated videos. 

_1)_ **_Comparison of Success Rate and Contact Accuracy_** _:_ Fig. 3 presents qualitative comparisons across four object categories, with all objects initialized 2.0 m away from the robot. For **ExoActor** , we observe significant spatial deviations between the generated trajectories and the target objects, particularly in the box grasping and table manipulation tasks. This is mainly caused by the scale ambiguity introduced when lifting 3D human motions from monocular videos, resulting in misalignment between the recovered trajectory and the real-world metric space. By contrast, the **w/o contact detection** baseline incorporates object pose information to refine the global trajectory, which effectively reduces rootlevel deviations and enables more accurate object approach. 

TABLE III 

QUANTITATIVE COMPARISON OF LEARNING TIME 

|Metric|HDMI [15]<br>ExoActor|[13]|**Ours**|
|---|---|---|---|
|Ave. Learning Time|_∼_70 min<br>1 min 33|s<br>|1 min 51 s|
||TABLE IV|||
|COMPARISON OFSU|CCESSRATES UNDEROOD<br>DISTANCE|ROBOT|-OBJECT|
||Robot-Object Dist|ance [m|]|
|Methods|-1.0<br>-0.5<br>+0.5|+1.0|+1.5|
|HDMI [15]|3/10<br>8/10<br>8/10|4/10|0/10|
|ExoActor [13]|0/10<br>0/10<br>0/10|0/10|0/10|
|**Ours**|**8/10**<br>**10/10**<br>**8/10**|**7/10**|**8/10**|


However, without explicit hand-object contact optimization, the recovered hand trajectories still suffer from geometric inaccuracies, leading to unreliable contact formation and failures such as object collision or unstable grasping due to excessive hand separation. The **w/o trajectory smoothing** baseline considers terminal contact optimization but does not enforce temporal smoothness on the optimized trajectory. As illustrated by the red trajectory in Fig. 3, the optimized terminal pose introduces abrupt changes with respect to the preceding motion, resulting in discontinuities in the reference trajectory. These discontinuities increase tracking errors during execution and consequently degrade task success rates. This issue is particularly evident in the box grasping task, where the large terminal correction leads to significant tracking deviations. The **w/o inward bias** baseline highlights the importance of incorporating interaction-specific physical priors. Although it considers contact optimization and trajectory smoothing, stable bimanual holding still requires sufficient compressive interaction between the hands and the object. Without the inward compressive bias, the robot can achieve geometric alignment with the object but lacks the additional force-inducing prior necessary for maintaining stable contacts. In comparison, **our method** jointly addresses global trajectory alignment, contact detection, and trajectory smoothing. It achieves more precise and physically consistent object interactions. 

To quantitatively evaluate performance, we report task success rate and hand-contact point error across four object categories, as shown in Table II. For each category, objects are initialized at five positions in front of the robot, ranging from 1.0 m to 2.0 m with 0.25 m intervals, and one video is generated per position. Each trial is repeated three times, resulting in 15 evaluations per category. A trial is considered successful if the object is lifted above the supporting surface for at least 1 s. The results show that our method consistently outperforms both baselines, achieving the highest average success rate of 76.7% and the lowest average hand–contact point error of 0.22 m. Similar to the analysis above, most failure cases can be attributed to root-position tracking errors. These errors propagate to the hand trajectories, increasing the hand–contact point error and occasionally causing unintended collisions with the object. ExoActor suffers from global geo- 


Fig. 4. **Task success rates under OOD box positions.** 

metric inconsistencies inherited from direct video-to-trajectory extraction, leading to systematic directional deviations and unreliable contact formation. The baseline without contact-point detection performs better than ExoActor, as its object-aware refinement partially alleviates root-trajectory errors; however, the lack of explicit contact localization still limits stable object interaction due to inaccurate hand-object alignment. The w/o trajectory smoothing baseline shows that abrupt trajectory corrections degrade tracking accuracy, which further increases the hand-contact point error and leads to lower task success rates. In addition, although the w/o inward bias baseline uses the smoothed trajectory, it still relies on purely geometrybased tracking and lacks an explicit prior for inducing objectholding forces. As a result, the robot may achieve accurate geometric alignment but fail to establish sufficiently stable contacts for holding the object. As a result, all these variants achieve success rates below 50%, accompanied by the average hand-contact point errors of up to 0.75 m. 

_2)_ **_Comparison of Learning Time_** _:_ In addition, taskspecific training methods such as HDMI tend to overfit a single trajectory, achieving near 100% success rates [15]. However, these methods require object-specific policy training and are computationally expensive, while exhibiting limited generalization to novel object configurations. Table III reports the average learning time on the box carrying task over three runs for each method. To ensure a fair comparison, all methods are evaluated under identical robot-object relative poses and on the same hardware platform, namely a single workstation equipped with an Intel Core i9 3.60 GHz CPU and an NVIDIA GeForce RTX 4080 GPU. The results show that HDMI requires substantially longer training time than other methods, taking more than one hour to complete a single task. In contrast, our method requires less than 2 minutes while still achieving a relatively high success rate, demonstrating significantly improved efficiency. 

_3)_ **_Comparison of Generalization Performance_** _:_ We evaluate the generalization ability of different methods under OOD object poses using the box-carrying task. The reference trajectory is generated with the box initialized 1.5 m from the robot, while evaluation is conducted at unseen distances of 0.5 m, 1.0 m, 2.0 m, 2.5 m, and 3.0 m. Each distance is 


Fig. 5. **Success rates of video generation models across four manipulation tasks.** Each bar reports the generation success rate over 10 generated videos. 


Fig. 6. **Effect of first-frame camera azimuth on task success rates.** Success rates for the box and chair tasks are evaluated at azimuth angles from 0<sup>_◦_</sup> to 180<sup>_◦_</sup> , with representative generated frames shown for selected viewpoints. 

evaluated over 10 trials, with the results summarized in Table IV. Our method consistently outperforms the baselines across OOD object distances. This is mainly because our approach refines the robot trajectory conditioned on the current object pose, rather than simply tracking a fixed reference trajectory. In contrast, HDMI learns to track a fixed trajectory and remains effective when test poses are close to the training distribution. However, its performance degrades significantly once the object is placed outside the randomized range used during training, reaching 0% success at 3.0 m. Similarly, ExoActor achieves lower success rates, as it directly tracks an open-loop trajectory recovered from video and cannot steer the robot toward unseen object poses. 

To further evaluate the generalization capability of the proposed method, we conduct the box-carrying task under OOD box positions using a single reference trajectory. As shown in Fig. 4, each point reports the success rate averaged over 10 repeated trials at a specific box position. Some positions do not have recorded results because they fall outside the field of view (FOV) of the robot-mounted camera. The results show that the proposed method consistently achieves high success rates across a wide range of OOD positions (greater than 65%), owing to its decoupled design that enables online trajectory refinement conditioned on the observed object pose. 

deployment, we study two controllable factors in the generation process: the video generation model and the camera azimuth used to capture the first-frame image. 

_1)_ **_Video Generation Model_** _:_ To evaluate the impact of different video generation models on the quality of generated task-oriented videos, we compare Wan 2.2, Seedance 1.0, Seedance 1.5, and Seedance 2.0 across four loco-manipulation tasks involving a box, chair, table, and cylinder. For each model-task pair, we generate 10 videos and evaluate whether each video satisfies the generation criteria, including faithful instruction following, consistent object geometry, and fixed camera viewpoint. The results are summarized in Fig. 5. Overall, stronger video generation models, such as Seedance 2.0, achieve higher video generation success rates by producing videos with better prompt adherence, more consistent object geometry, and more physically plausible interactions. In contrast, Wan 2.2 and Seedance 1.0 frequently suffer from object deformation and camera-viewpoint drift, resulting in invalid task-oriented videos. For table and cylinder manipulation, video generation is particularly challenging due to more complex hand-object interactions, where physically inconsistent behaviors, such as object deformation, are more likely to occur. 

_2)_ **_First-Frame Camera Azimuth_** _:_ To analyze the effect of the first-frame camera viewpoint, we vary the camera azimuth around the robot–object scene for both the box and chair tasks, while keeping other camera parameters fixed, including the camera height, pitch angle, and so on. Due to the bilateral symmetry of the robot-object setup, we only evaluate azimuth angles from 0<sup>_◦_</sup> to 180<sup>_◦_</sup> at 30<sup>_◦_</sup> intervals. For each angle, we render one first-frame image and generate five valid videos using Seedance 2.0. Each generated video is processed through GenHOI twice to execute the task. The task success rates are reported in Fig. 6. The results indicate a noticeable drop in success rate at azimuth angles of 150<sup>_◦_</sup> and 180<sup>_◦_</sup> . This is because, from these viewpoints, the robot substantially occludes the target object in the generated videos, leading to unreliable hand detection and contact-point estimation. In contrast, for viewpoints where both the robot and the target object are clearly visible, the proposed method maintains consistent performance across different camera azimuths. 

## _C. Key Factors of Video Generation for Loco-Manipulation_ 

To understand how video generation influences the downstream performance of GenHOI in simulation and real-world 

## _D. Key Modules Evaluation_ 

_1)_ **_Evaluation of Key Frame Selection_** _:_ To evaluate the accuracy of VLM-based key frame selection, we test two 

TABLE V 

EVALUATION OF VLM-BASED KEY FRAME SELECTION 

|Models|Box|Chair|Table|Cylinder|Ave.|
|---|---|---|---|---|---|
|Doubao-Seed-2.0|15/15|15/15|12/15|15/15|95.0%|
|GPT-5.5|15/15|15/15|13/15|15/15|96.7%|


vision-language models, Doubao-Seed-2.0 and GPT-5.5, on four object manipulation tasks: box, chair, table, and cylinder. For each object, we generate five videos and query the VLM three times for each video. A selection is counted as successful if the predicted frame correctly captures the initial hand-object contact. The results are reported in Table V. 

Both models achieve high selection accuracy across different objects, with average accuracies of at least **95%** , indicating that VLMs can reliably localize the critical interaction moment from generated videos. The only noticeable performance drop occurs in the table task, where the larger object geometry and partial hand-object occlusions make the first contact moment more ambiguous. Nevertheless, the consistently high accuracy demonstrates that the proposed key frame selection module provides reliable temporal anchors for subsequent contact estimation and motion extraction. 

_2)_ **_Evaluation of Contact Point Detection_** _:_ Fig. 7 illustrates contact point detection on different object manipulation tasks. For each task, the first column shows the selected key frame with detected hand masks. The second column visualizes the coarse contact points, which are obtained by back-projecting the depth pixels within the hand masks into 3D using the estimated depth map and camera intrinsics. The refined contact points are shown in the third column. The results show that, even when the hands are partially occluded or only weakly visible in the key frame, the proposed refinement step effectively recovers reliable hand-object contact locations. 

## _E. Real-World Experiments_ 

We conduct real-world experiments to evaluate the proposed GenHOI framework. The experiments include box grasping, asymmetric bimanual chair carrying, table lifting from below, and cylindrical-object enveloping, as well as continuous box grasping at varying positions. These experiments aim to: (1) demonstrate the ability of our method to rapidly acquire object-interaction skills across diverse objects; (2) highlight the steerable interaction capability, where a single reference trajectory can generalize to objects at different positions. 

_1)_ **_Interaction with Different Objects_** _:_ As illustrated in Fig. 8, we first present qualitative demonstrations to evaluate whether GenHOI can achieve loco-manipulation across different objects. In each task, the target object is placed 1.0–3.0 m away from the robot, ensuring that its initial pose remains within the camera FOV. Starting from the perceived object pose, the robot reconstructs the scene in simulation, generates a video conditioned on the rendered first-frame image and a language command, extracts geometric constraints, and executes the optimized trajectory with a closed-loop tracking controller. Specifically, we evaluate four representative objects with different geometries and contact configurations: a box 


Fig. 7. **Visualization of contact point detection.** Each row corresponds to one manipulation task, and the three columns show the selected key frame, coarse contact points, and refined contact points, respectively. 

(0 _._ 23m _×_ 0 _._ 26m _×_ 0 _._ 42m), a chair (0 _._ 37m _×_ 0 _._ 37m _×_ 0 _._ 85m), a table (0 _._ 80m _×_ 0 _._ 36m _×_ 0 _._ 60m), and a cylinder (Φ 0 _._ 40m _×_ 0 _._ 70m). The box is initialized 1.8 m in front of the robot with its centroid 0.3 m above the ground. The chair is placed on the ground at 1.6 m, the table is placed on the ground at 1.5 m, and the cylinder is initialized at 1.5 m with its centroid 0.9 m above the ground. GenHOI generates distinct interaction strategies for these objects: the robot establishes symmetric bimanual contacts to lift the box, forms asymmetric contacts on the chair backrest and seat, bends down to lift the table from underneath, and adopts an enveloping motion around the cylinder. These results show that our method can adapt the generated motion to diverse object geometries and contact configurations. 

_2)_ **_Generalization to Out-of-Distribution Object Positions_** _:_ As shown in Fig. 9, the box is placed at three different planar positions with distances of 1.5 m, 2.5 m, and 3.5 m. Using only a single box-grasping trajectory extracted from the generated video, the robot continuously performs grasping tasks across these varying object configurations. During _t_ 1– _t_ 4, the robot approaches and grasps a box placed at a height of 0.3 m above the ground while adopting a single-knee posture. The box is then relocated to a platform at a height of 0.6 m. During _t_ 5– _t_ 8, the robot re-estimates the box pose, optimizes the reference trajectory based on the current object configuration, and grasps the box in a semi-squatting posture. Finally, the box is placed on a table at a height of 0.8 m. From _t_ 9 to _t_ 12, the robot again adapts the trajectory according to the real-time box pose and successfully completes the grasping task. Notably, all three sequential tasks are completed using only a single generated video and the corresponding reference trajectory 


Fig. 8. **Real-world experiments across four object-interaction tasks.** Including box grasping (a), asymmetric bimanual chair carrying (b), table lifting from below (c), and cylindrical-object enveloping (d). 


Fig. 9. **Continuous real-world box-grasping demonstrations across OOD object poses.** 

extracted from it, with online trajectory optimization enabling adaptation to different OOD object heights and positions. 

## _F. Analysis of Failure Cases_ 

Since GenHOI consists of multiple sequential modules, failures may originate from different stages and propagate through the pipeline. To better understand the contribution of each module to the final task outcome, we conduct 50 repeated trials on the box-grasping task and categorize the failure cases, as shown in Fig. 10. Overall, 34 out of 50 trials successfully complete the full pipeline. The main failures occur during video generation, including camera-viewpoint drift, object deformation, and hallucination, followed by errors in keyframe extraction and contact detection. In addition, five trials fail during robot trajectory tracking, mainly due to the limited tracking accuracy of the current low-level humanoid controller. Overall, directly imitating generated videos for HOI is primarily limited by the quality of the generated videos and the tracking accuracy of the humanoid locomotion controller. 

## V. CONCLUSION 

In this paper, we presented GenHOI, a framework that enables humanoid robots to perform object-interaction tasks by 


Fig. 10. **Failure-case analysis of the framework.** Across video generation, key frame extraction, contact detection, and trajectory tracking. 

imitating a single generated video. Given an onboard observation and a language command, GenHOI reconstructs the robot– object scene in simulation, generates a task video, extracts contact-aware geometric constraints, and refines the recovered motion through geometry-guided trajectory optimization. 

The optimized trajectory is then executed by a closed-loop whole-body controller, enabling real-world loco-manipulation without task-specific policy training or physical demonstration data. Simulation and real-world experiments on a Unitree G1 robot demonstrate diverse interaction skills, including box grasping, table lifting, chair carrying, and cylindrical-object enveloping. The results further show that GenHOI enables steerable interactions and generalizes to OOD object poses. Overall, this work represents a step toward using generative video models as scalable action priors for HOI. 

The current framework has several limitations. First, the real-to-sim reconstruction assumes access to an accurate object mesh, which may limit its scalability to previously unseen objects. Future work could incorporate online 3D reconstruction or shape completion from onboard RGB-D observations. Second, the current platform lacks dexterous hands, restricting the system to relatively coarse interactions. Future work incorporates dexterous end-effectors to support more precise and versatile humanoid–object interaction. 

## REFERENCES 

- [1] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _IEEE/ASME Transactions on Mechatronics_ , vol. 31, no. 2, pp. 2300–2330, 2026. 

- [2] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Casta˜neda, S. Sastry _et al._ , “Viral: Visual sim-to-real at scale for humanoid loco-manipulation,” _arXiv preprint arXiv:2511.15200_ , 2025. 

- [3] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi, “Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction,” _arXiv preprint arXiv:2509.26633_ , 2025. 

- [4] C. Zheng, K. Chen, Z. Bi, Y. Li, L. Pan, J. Zhou, H. Li, and J. Ma, “Embracing bulky objects with humanoid robots: Whole-body manipulation with reinforcement learning,” _arXiv preprint arXiv:2509.13534_ , 2025. 

- [5] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [6] Y. Lin, J. Shi, D. Wang, J. Kong, Y. Liu, C. Bai, and X. Li, “Prohoi: Perceptive root-guided humanoid-object interaction,” _arXiv preprint arXiv:2603.01126_ , 2026. 

- [7] T. B. OpenAI, “Video generation models as world simulators,” _https://openai. com/sora/_ , 2024. 

- [8] T. Seedance, D. Chen, L. Chen, X. Chen, Y. Chen, Z. Chen, Z. Chen, F. Cheng, T. Cheng, Y. Cheng _et al._ , “Seedance 2.0: Advancing video generation for world complexity,” _arXiv preprint arXiv:2604.14148_ , 2026. 

- [9] T. Xie, H. Zhang, J. Park, Z. Wang, B. Wen, J. Li, X. Li, Q. Ben, H. Weng, Y. Ye _et al._ , “Grail: Generating humanoid loco-manipulation from 3d assets and video priors,” _arXiv preprint arXiv:2606.05160_ , 2026. 

- [10] J. Liang, P. Tokmakov, R. Liu, S. Sudhakar, P. Shah, R. Ambrus, and C. Vondrick, “Video generators are robot policies,” _arXiv preprint arXiv:2508.00795_ , 2025. 

- [11] K. Dharmarajan, W. Huang, J. Wu, L. Fei-Fei, and R. Zhang, “Dream2flow: Bridging video generation and open-world manipulation with 3d object flow,” _arXiv preprint arXiv:2512.24766_ , 2025. 

- [12] S. Patel, S. Mohan, H. Mai, U. Jain, S. Lazebnik, and Y. Li, “Robotic manipulation by imitating generated videos without physical demonstrations,” _arXiv preprint arXiv:2507.00990_ , 2025. 

- [13] Y. Zhou, J. Ma, Y. Peng, Z. Sun, Y. Bai, and B. F. Karlsson, “Exoactor: Exocentric video generation as generalizable interactive humanoid control,” _arXiv preprint arXiv:2604.27711_ , 2026. 

- [14] W. Xu, J. Li, Y. Gu, B. Yang, H. Chen, S. Lin, M. Zhou, J. Tan, Q. Wu, X. Jiang _et al._ , “Morphology-consistent humanoid interaction through robot-centric video synthesis,” _arXiv preprint arXiv:2603.19709_ , 2026. 

- [15] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi, “Hdmi: Learning interactive humanoid whole-body control from human videos,” _arXiv preprint arXiv:2509.16757_ , 2025. 

- [16] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [17] H. Wang, W. Zhang, R. Yu, T. Huang, J. Ren, F. Jia, Z. Wang, X. Niu, X. Chen, J. Chen, Q. Chen, J. Wang, and J. Pang, “Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system,” _arXiv preprint arXiv:2510.11072_ , 2025. 

- [18] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Casta˜neda, G. Shi, S. Sastry _et al._ , “Opening the sim-to-real door for humanoid pixel-to-action policy transfer,” _arXiv preprint arXiv:2512.01061_ , 2025. 

- [19] M. Shi, S. Peng, J. Chen, H. Jiang, Y. Li, D. Huang, P. Luo, H. Li, and L. Chen, “Egohumanoid: Unlocking in-the-wild loco-manipulation with robot-free egocentric demonstration,” _arXiv preprint arXiv:2602.10106_ , 2026. 

- [20] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [21] A. O’Neill, A. Rehman, A. Gupta, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar _et al._ , “Open x- embodiment: Robotic learning datasets and rt-x models,” _arXiv preprint arXiv:2310.08864_ , 2023. 

- [22] R. Zheng, D. Niu, Y. Xie, J. Wang, M. Xu, Y. Jiang, F. Casta˜neda, F. Hu, Y. L. Tan, L. Fu _et al._ , “Egoscale: Scaling dexterous manipulation with diverse egocentric human data,” _arXiv preprint arXiv:2602.16710_ , 2026. 

- [23] S. Wei, H. Jing, B. Li, Z. Zhao, J. Mao, Z. Ni, S. He, J. Liu, X. Liu, K. Kang _et al._ , “Ψ0: An open foundation model towards universal humanoid loco-manipulation,” _arXiv preprint arXiv:2603.12263_ , 2026. 

- [24] S. Zhou, Y. Du, J. Chen, Y. Li, D.-Y. Yeung, and C. Gan, “Robodreamer: Learning compositional world models for robot imagination,” _arXiv preprint arXiv:2404.12377_ , 2024. 

- [25] J. Mu, S. Yang, Y. Bao, H. Bae, T. Wei, L. Xu, B. Li, H. Xu, and J. Pang, “Deximit: Learning bimanual dexterous manipulation from monocular human videos,” _arXiv preprint arXiv:2602.10105_ , 2026. 

- [26] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin _et al._ , “Dreamgen: Unlocking generalization in robot learning through video world models,” _arXiv preprint arXiv:2505.12705_ , 2025. 

- [27] T. Ma, J. Zheng, Z. Wang, C. Jiang, A. Cui, J. Liang, and S. Yang, “Dit4dit: Jointly modeling video dynamics and actions for generalizable robot control,” _arXiv preprint arXiv:2603.10448_ , 2026. 

- [28] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang _et al._ , “World action models are zero-shot policies,” _arXiv preprint arXiv:2602.15922_ , 2026. 

- [29] B. Wen, W. Yang, J. Kautz, and S. Birchfield, “Foundationpose: Unified 6d pose estimation and tracking of novel objects,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2024, pp. 17 868–17 879. 

- [30] Y. Wang, Q. Zhao, Y. F. Lau, R. Yu, H. W. Tsui, Q. Chen, J. Wang, J. Pang, and P. Tan, “Humanx: Toward agile and generalizable humanoid interaction skills from human videos,” _arXiv preprint arXiv:2602.02473_ , 2026. 

- [31] Z. Shen, H. Pi, Y. Xia, Z. Cen, S. Peng, Z. Hu, H. Bao, R. Hu, and X. Zhou, “World-grounded human motion recovery via gravity-view coordinates,” in _SIGGRAPH Asia 2024 Conference Papers_ , 2024, pp. 1–11. 

- [32] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [33] L. Yang, B. Kang, Z. Huang, Z. Zhao, X. Xu, J. Feng, and H. Zhao, “Depth anything v2,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 21 875–21 911, 2024. 

- [34] Y. Xu, J. Zhang, Q. Zhang, and D. Tao, “Vitpose: Simple vision transformer baselines for human pose estimation,” _Advances in neural information processing systems_ , vol. 35, pp. 38 571–38 584, 2022. 

- [35] S. Dafarra, G. Romualdi, and D. Pucci, “Dynamic complementarity conditions and whole-body trajectory optimization for humanoid robot locomotion,” _IEEE Transactions on Robotics_ , vol. 38, no. 6, pp. 3414– 3433, 2022. 

- [36] Z. Bi, Y. Zhang, K. Chen, G. Zhao, Y. Li, and J. Ma, “Alore: Autonomous large-object rearrangement with a legged manipulator,” _arXiv preprint arXiv:2602.04214_ , 2026. 


Fig. 11. Object-specific prompts and representative key frames from the generated videos. 

## APPENDIX A 

## VIDEO GENERATION PROMPTS 

To guide the video diffusion model toward physically plausible and task-consistent outputs, we design object-specific text prompts for each loco-manipulation task. Fig. 11 shows the prompts used for four representative objects, including a box, chair, table, and cylinder, together with four selected key frames from the generated videos. 


Fig. 12. Prompt of the key frame selection. 

## APPENDIX C 

## TRAJECTORY SMOOTHING 

After obtaining the optimized terminal state **h**<sup>opt</sup> _N_<sup>,wecom-</sup> pute the terminal correction relative to the reference trajectory as: 


Rather than re-optimizing the entire trajectory, we smoothly propagate this terminal correction over the last _K_ frames of the reduced-state trajectory, where _K_ = 90, corresponding to the final 3 s of motion. Specifically, for each frame _i ∈{N − K_ + 1 _,..., N}_ , we define a normalized tail coordinate 


and compute a quintic smoothstep weight: 


The refined reduced state is then updated as: 


Each updated state is subsequently projected onto the same box constraints used in (10) to ensure kinematic feasibility. In this way, the terminal correction is distributed smoothly over the final 3 s of the trajectory, leading to a gradual transition to the optimized terminal configuration while avoiding abrupt motion changes. 

## APPENDIX B 

## KEY FRAME SELECTION 

Fig. 12 illustrates the procedure for selecting the key frame from a generated video. We first sample a set of candidate frames from the video and concatenate them into a single composite image in chronological order. The composite image is then fed into Doubao-Seed-2.0, together with a prompt asking the model to identify the earliest frame in which both hands are fully in contact with the object. The model is required to return only the index of the selected frame, which is used as the key frame for subsequent contact-point detection and object-aware constraint extraction. In the example shown in Fig. 12, the second frame is selected as the key frame. 

