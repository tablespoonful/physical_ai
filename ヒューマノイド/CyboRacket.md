---
title: "CyboRacket: A Perception-to-Action Framework for Humanoid Racket Sports"
date: "2026-03-15"
authors: "Peng Ren; Chuan Qi; Haoyang Ge; Qiyuan Su; Xuguo He; Cong Huang"
url: https://arxiv.org/abs/2603.14605
pdf: https://arxiv.org/pdf/2603.14605
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.14605)** / [論文ページ](https://arxiv.org/abs/2603.14605)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

1 

# CyboRacket: A Perception-to-Action Framework for Humanoid Racket Sports 

Peng Ren<sup>1,2,*</sup> , Chuan Qi<sup>3,2,*</sup> , Haoyang Ge<sup>4,2,*</sup> , Qiyuan Su<sup>5</sup> , Xuguo He<sup>5</sup> , Cong Huang<sup>2,6</sup> , Pei Chi<sup>1,</sup><sup>_†_</sup> , Jiang Zhao<sup>1</sup> , Kai Chen<sup>2,5,6,</sup><sup>_†_</sup> , 1BUAA 2BZA 3USTC 4TJU 5DeepCybo 6ZGCI *Equal contribution. 

> _†_ Corresponding authors: Pei Chi (peichi@buaa.edu.cn), Kai Chen (kaichen@zgci.ac.cn). 

**_Abstract_ —Dynamic ball-interaction tasks remain challenging for robots because they require tight perception-action coupling under limited reaction time. This challenge is especially pronounced in humanoid racket sports, where successful interception depends on accurate visual tracking, trajectory prediction, coordinated stepping, and stable whole-body striking. Existing robotic racket-sport systems often rely on external motion capture for state estimation or on taskspecific low-level controllers that must be retrained across tasks and platforms. We present** **_CyboRacket_ , a hierarchical perception-to-action framework for humanoid racket sports that integrates onboard visual perception, physics-based trajectory prediction, and large-scale pre-trained whole-body control. The framework uses onboard cameras to track the incoming object, predicts its future trajectory, and converts the estimated interception state into target end-effector and base-motion commands for whole-body execution by SONIC on the Unitree G1 humanoid robot. We evaluate the proposed framework in a vision-based humanoid tennis-hitting task. Experimental results demonstrate real-time visual tracking, trajectory prediction, and successful striking using purely onboard sensing.** 

**_Index Terms_ —Humanoid Robotics; Vision-Based Control; Ball Trajectory Prediction; Whole-Body Motion Control** 

## I. Introduction 

ECENT years have seen substantial progress in **R** robotic control across diverse platforms, from quadrupeds traversing challenging terrain to industrial manipulators performing precise assembly and humanoids achieving stable locomotion and whole-body coordination [1]–[3]. However, tasks involving fast-moving objects remain significantly more challenging, as they require tight perception-action coupling under limited reaction time. Robotic racket sports, including table tennis, badminton, and tennis, exemplify such dynamic visuomotor problems: the robot must track a high-speed ball, predict its future trajectory, and generate coordinated striking motions with accurate spatial and temporal alignment. 

Existing approaches to robotic racket-sport interaction can be broadly divided into two categories. End-to-end learning methods map sensory observations directly to 

Equal contribution. 

low-level actions without explicit intermediate representations. For example, Tebbe et al. showed that reinforcement learning can acquire rallying behavior from scratch in fewer than 200 trials [4], while the Gemini Robotics team demonstrated amateur human-level robotic table tennis through large-scale hierarchical reinforcement learning and sim-to-real transfer [5], [6]. In contrast, hierarchical methods separate projectile-state prediction and interception planning from low-level motion execution, typically combining model-based trajectory prediction and strike-point generation with specialized controllers such as MPC [7] or task-specific learned policies [8], [9]. While more modular and interpretable, existing hierarchical systems still face two key limitations: many depend on external motion capture or other instrumented sensing for accurate state estimation [8], and their low-level controllers are often task-specific, requiring retraining when the task or platform changes [9]. This motivates a hierarchical framework that integrates onboard closed-loop perception with a reusable pre-trained whole-body execution backbone. 

Among these dynamic racket-sport settings, humanoid platforms are particularly challenging. Unlike fixed-base manipulators, humanoid robots must coordinate perception, locomotion, balance maintenance, and arm swinging within a single whole-body control loop. The reachable striking region is not determined by the arm alone, but also depends on timely base repositioning and stable lower-body support. As a result, errors in state estimation or interception timing can propagate not only to racket contact, but also to stepping behavior and wholebody balance. These characteristics make humanoid racket sports a demanding testbed for dynamic perception-action integration. 

In this work, we present _CyboRacket_ , a hierarchical perception-to-action framework for humanoid racket sports that integrates onboard visual perception, physicsbased trajectory prediction, and large-scale pre-trained whole-body control. The system uses a YOLO-based detector running entirely on onboard cameras to track fast incoming projectiles in real time, without relying on external motion capture. A physics-based predictor estimates the future trajectory, including the landing region and arrival time, and converts these predictions into target 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

2 

end-effector states and base motion commands for interception. To realize these commands on a humanoid platform, we build the execution layer on top of SONIC [10], a recently open-sourced large-scale motion tracking foundation model for humanoid control. We instantiate the proposed framework on the Unitree G1 humanoid robot in a vision-based tennis-hitting task. By coupling closedloop perception and interception planning with pre-trained whole-body motion execution, the framework enables time-critical projectile interaction through coordinated stepping and swinging. Experimental results show that the proposed system supports real-time projectile tracking, trajectory prediction, and successful striking using purely onboard visual sensing, demonstrating the feasibility of perception-driven dynamic racket-sport interaction on a humanoid platform. 

The main contributions of this work are as follows: 

- We propose a hierarchical perception-to-action framework for humanoid racket sports that combines onboard visual trajectory prediction with a large-scale pre-trained humanoid motion executor, avoiding taskspecific retraining of the full low-level controller. 

- We develop a purely onboard visual closed-loop pipeline for fast-projectile perception and trajectory prediction, removing the dependence on external motion capture systems. 

- We demonstrate vision-based tennis hitting on the Unitree G1 humanoid robot, showing the effectiveness of integrating pre-trained whole-body motion control with closed-loop perception and planning for dynamic humanoid interaction. 

## II. Related Work 

_A. Robotic Racket Sports and Dynamic Object Interaction_ 

Robotic racket sports provide a representative benchmark for dynamic perception, prediction, and time-critical control. Early table-tennis systems established the foundations for high-speed striking through biologically inspired trajectory generation, kinesthetic teach-in, and anticipatory action selection [11]–[14]. More recent work has increasingly adopted learning-based methods. The Gemini Robotics team demonstrated amateur human-level robotic table tennis using hierarchical learning with sim-to-real transfer [5], [6], while Tebbe et al. showed that reinforcement learning can acquire rallying behavior from scratch in fewer than 200 trials [4]. 

Related developments in other racket-sport and dynamic-manipulation settings have further extended these ideas beyond fixed-base platforms. Zaidi et al. developed an athletic mobile manipulator for wheelchair tennis [15], and Ma et al. demonstrated coordinated badminton skills on legged manipulators with onboard perception and whole-body visuomotor coordination [9]. On humanoid platforms, Xiong et al. demonstrated table tennis with impedance control but were limited to static standing [16], whereas Su et al. combined model-based planning with RL-based whole-body control 

to enable dynamic humanoid table tennis [8]. Despite this progress, current systems still exhibit two recurring limitations: many depend on external motion capture or other privileged sensing setups for accurate projectilestate estimation [8], and their control policies are often specialized for a specific task or platform [9]. These limitations make it difficult to achieve deployable onboard perception together with reusable whole-body execution for humanoid racket-sport tasks. 

_B. Humanoid Whole-Body Control and Scalable Motion Tracking_ 

In parallel, humanoid control has evolved from taskspecific imitation toward scalable whole-body motion tracking. Early work focused on learning controllers for individual motions or motion families through large-scale reinforcement learning and manually designed rewards [17], [18]. Subsequent approaches improved coordination by decoupling upper- and lower-body control [19], [20], while more recent methods developed general whole-body motion trackers capable of reproducing a broad range of human movements [21], [22]. 

A growing line of work has further explored largescale pre-trained models as reusable control backbones for humanoid robots. Luo et al. showed that scaling motion tracking to 100 million frames can yield universal tracking capabilities across diverse behaviors, suggesting motion tracking as a practical foundation for humanoid control [10]. SONIC [10] and contemporaneous systems [23], [24] further demonstrated that such pre-trained controllers can support multimodal command interfaces, including teleoperation, video-driven control, and integration with higher-level vision-language-action models [25]. However, these methods mainly focus on tracking externally provided motion references and remain weakly connected to task-level closed-loop perception. As a result, although they provide strong reusable whole-body motion priors, they do not by themselves solve dynamic interactive tasks such as racket sports, where perception, prediction, and action must be tightly coupled in real time. 

## III. System Overview 

We address real-time tennis interception on the Unitree G1 humanoid as an onboard perception-to-action problem, where noisy RGB-D observations of a fast incoming projectile must be converted into dynamically feasible wholebody striking behaviors under tight latency constraints. As shown in Fig. 1, our framework closes this loop through three tightly coupled stages: projectile state estimation from a head-mounted RGB-D camera, interception target generation from short-horizon trajectory prediction, and whole-body execution through a SONIC-based control interface. The robot is equipped with a 100 Hz RGB-D camera mounted on the head, whose synchronized color and depth streams are processed together with proprioceptive robot states for visual tracking, geometric reconstruction, and frame transformation. From image-space projectile 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

3 


Fig. 1: System overview of the humanoid humanoid racket sports framework. 

observations, the system maintains temporally consistent 2D measurements, reconstructs 3D projectile positions in the robot frame, and estimates a filtered projectile state using an EKF. This state estimator further rolls out the short-horizon trajectory of the projectile and continuously provides the downstream planner with updated interception candidates. 

Given the estimated projectile trajectory, the planner selects a dynamically feasible interception target by jointly considering timing, reachability, body stability, and swing effectiveness. The planning process runs online in a receding-horizon manner and is coupled with a swing state machine, allowing the robot to revise its interception decision as new visual evidence arrives. Instead of directly producing joint-level commands, the planner outputs structured motion targets, including the desired head orientation for maintaining visual continuity, wrist targets for racket interception, body height adjustment, and navigation velocity. These targets are mapped to the low-dimensional SONIC command interface, which drives coordinated locomotion and striking behaviors at the whole-body level. This design separates fast visual updates from motion generation while preserving a tight closed loop between onboard perception, interception planning, and physically executable humanoid control. 

## IV. Onboard RGB-D projectile Perception and State Estimation 

This section presents an onboard RGB-D perception pipeline that estimates the state of the incoming racket- 

sport projectile and provides the planner with a temporally consistent 3D trajectory prediction. In the current implementation, we instantiate this module for tennisball perception. The main challenge is that the projectile appears as a small, fast-moving target under limited sensing resolution and short reaction horizons, while aggressive head and body motions can further amplify localization noise and timing error. Motivated by the closedloop requirements of dynamic interception, we formulate this perception module not as isolated detection and tracking components, but as a unified estimation process that converts synchronized RGB-D measurements into uncertainty-aware 3D projectile states and short-horizon trajectory predictions. 

## _A. Projectile Observation and 2D Tracking_ 

We first extract image-space projectile observations from synchronized RGB and depth frames captured by the head-mounted RGB-D camera. A YOLO-based detector is applied to the RGB image to produce candidate tennisball bounding boxes. To preserve geometric consistency between the network input and the original image coordinates, the RGB image is resized with aspect-ratiopreserving padding before inference, and the predicted boxes are mapped back to the original image plane afterward. Since generic `sports ball` detections are prone to false positives in real scenes, we further apply taskspecific filtering based on geometry and appearance. In particular, for the tennis instantiation used in this work, we reject candidates with implausible scale or aspect ratio 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

4 

and retain only regions whose color statistics are consistent with the typical yellow-green appearance of a tennis ball. The resulting output is a timestamped 2D observation stream containing the projectile bounding box, confidence, and image metadata. 

ment covariance matrix **R** _t_<sup>meas</sup> . We model uncertainty in the image-plane localization and depth estimate by 


where _σu,t_ and _σv,t_ denote the standard deviations of the projectile center in pixel coordinates, and _σZ,t_ denotes the standard deviation of the aggregated depth estimate. We then propagate this uncertainty through the nonlinear mapping from ( _ut, vt, Zt_ ) to the base-frame position **p** _b,t_ using first-order error propagation: 

To improve robustness against single-frame errors, missed detections, and motion blur, we maintain a lightweight single-object temporal tracker in image space. The tracker propagates the current observation with a constant-velocity model and associates new detections using center proximity, scale consistency, and motion-direction agreement. This produces a temporally smoothed 2D projectile observation and also serves as an observation manager: when detections are briefly unavailable, the tracker extrapolates the object center for a small number of frames; when the observation gap exceeds a threshold, the trajectory is reset. Compared with raw frame-wise detections, this representation provides a substantially more stable visual signal for downstream 3D reconstruction and state estimation. 


Here, **J** _t ∈_ R<sup>3</sup><sup>_×_3</sup> denotes the Jacobian of the mapping from ( _ut, vt, Zt_ ) to the reconstructed base-frame position **p** _b,t_ , and thus characterizes how image-plane and depth uncertainties are amplified in 3D space. This construction yields a range-dependent measurement covariance: as the projectile moves farther away, a given pixel or depth error induces a larger 3D localization error. The resulting covariance is used in the EKF update step to weight each observation according to its geometric reliability. 

## _B. RGB-D 3D Localization and Measurement Uncertainty_ 

The tracked 2D observation is then lifted to 3D using the aligned depth measurement from the RGB-D camera. Rather than directly querying depth at a single pixel, we estimate the projectile depth from a local region centered at the tracked image location, which is more robust for small distant objects whose depth measurements are easily corrupted by background leakage, invalid samples, and boundary noise. Invalid or out-of-range values are removed, and a foreground-biased robust statistic is used to recover the depth value. 

## _C. EKF-Based projectile State Estimation_ 

On top of these reconstructed 3D measurements, we maintain a continuous estimate of the projectile state using an extended Kalman filter (EKF). The EKF state consists of the 3D projectile position and velocity, 


where **p** _t_ = [ _px,t, py,t, pz,t_ ]<sup>_⊤_</sup> denotes the projectile position and **v** _t_ = [ _vx,t, vy,t, vz,t_ ]<sup>_⊤_</sup> denotes the projectile velocity in the robot base frame. The measurement vector contains only the reconstructed 3D position, 

Let ( _ut, vt_ ) denote the tracked projectile center in the RGB image at time _t_ , and let _Zt_ denote the aggregated depth value obtained from the aligned depth map within a local region around the projectile center. Given the RGBD camera intrinsics 


During the prediction step, the projectile state is propagated with a discrete flight model that accounts for gravity and aerodynamic drag. Starting from the current state estimate ( **p** _t,_ **v** _t_ ) and time step ∆ _t_ , we update the position and velocity as 

where ( _fx, fy_ ) are the focal lengths and ( _cx, cy_ ) is the principal point, the 3D projectile position in the camera frame is recovered by pinhole back-projection as 


where the acceleration term is defined as 

The point is then transformed into the robot base frame as 


with **g** the gravitational acceleration and _k_ 1 _, k_ 2 the coefficients of linear and quadratic drag, respectively. In compact form, the EKF process model is written as 


where **R** _b←c ∈ SO_ (3) and **t** _b←c ∈_ R<sup>3</sup> are the calibrated extrinsic rotation and translation from the camera frame to the robot base frame. 


To quantify the reliability of each 3D observation, we further associate the reconstructed point with a measure- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

5 

During the measurement update, we first validate each incoming 3D observation using a Mahalanobis-distance gate on the innovation, in order to reject outliers caused by false detections, depth corruption, or abrupt mismatches. The innovation is defined as 


where **x** ˆ _t|t−_ 1 is the predicted EKF state and **H** is the measurement matrix defined in (6). The corresponding innovation covariance is 


with **P** _t|t−_ 1 the predicted state covariance. We then compute the Mahalanobis distance 


and accept the measurement only if _d_<sup>2</sup> _t_<sup>_<τ_,where</sup><sup>_τ_</sup> is chosen according to a _χ_<sup>2</sup> threshold. Otherwise, the update is skipped and the filter continues prediction-only propagation, which allows the estimator to bridge short observation gaps without being corrupted by unreliable measurements. 

To better capture near-ground projectile motion, we additionally apply a simplified bounce update when the estimated projectile height in the robot base frame falls below a bounce threshold _zb_ and the vertical velocity is downward, i.e., _p_ ˆ _z < zb_ and _v_ ˆ _z <_ 0. In this case, the postbounce vertical velocity is approximated by 


where _vz_<sup>_−_and</sup><sup>_v_</sup> _z_<sup>+denote the pre- and post-bounce vertical</sup> velocities, respectively, and _e_ is an effective restitution coefficient. Optionally, the corresponding covariance can be inflated after the bounce event to reflect additional uncertainty introduced by ground contact. This approximation is sufficient for short-horizon interception prediction while avoiding the complexity of a more detailed contact model. 

## _D. Short-Horizon Trajectory Prediction_ 

Beyond recursive filtering, we further perform shorthorizon trajectory prediction for interception planning. Starting from the current filtered state estimate, we roll out the same projectile dynamics model forward in time by discrete integration and obtain a sequence of future trajectory samples 


where _τi_ = _i_ ∆ _t_ pred denotes the prediction horizon. From this rollout, we compute interception-relevant quantities, including the predicted hitting point **p** hit, the corresponding hitting time _t_ hit, the projectile velocity at interception **v** hit, and the predicted landing point. 

In particular, the candidate hitting point is determined as the earliest feasible intersection between the predicted trajectory and a designated hitting-height plane within the prediction horizon, 


where _z_ 0 is the desired hitting height. A candidate interception state is exported to the planner only when the EKF state covariance remains below a threshold, the predicted hitting time lies within a feasible reaction window, and the target remains inside the robot’s reachable workspace. In this way, the estimator provides the planner not only with a filtered instantaneous projectile state but also with a dynamically consistent short-horizon forecast for online interception. 

## V. Interception Planning and Pre-trained Whole-Body Control 

This section converts the estimated projectile state into executable whole-body interception commands. Rather than synthesizing joint-space trajectories directly, the planner outputs a structured interception intent, including the desired contact time and location, target base placement, swing direction, and execution phase, while locomotion realization, balance maintenance, and coordinated whole-body motion are delegated to the pre-trained SONIC execution stack. This decomposition keeps the planning problem compact and interpretable while leveraging SONIC as a scalable whole-body control backbone. 

## _A. Interception Planning_ 

At each planning cycle, the planner receives the filtered projectile state, a short-horizon trajectory prediction, and the current robot base pose. Let 


denote the predicted projectile trajectory sampled at future time instants _τi_ , where **p** ˆ( _τi_ ) _∈_ R<sup>3</sup> and **v** ˆ( _τi_ ) _∈_ R<sup>3</sup> are the predicted position and velocity, and _N_ is the number of prediction samples. The planner first identifies a candidate interception state ( **p** hit _, t_ hit) from the earliest feasible intersection between the predicted trajectory and the designated hitting-height plane, subject to predefined temporal and workspace constraints. 

Given the candidate contact point, we compute a desired base placement from a nominal racket-contact template. Let **r** hit _∈_ R<sup>3</sup> denote the preferred offset from the robot base to the racket contact point at impact, expressed in the base-heading frame. Given a desired base yaw _ψ_ des, the corresponding target base position is 


where **R** _z_ ( _ψ_ des) _∈ SO_ (3) denotes the planar rotation matrix about the vertical axis. Intuitively, the planner selects a base pose such that the nominal racket contact point aligns with the predicted projectile position at the desired contact time. 

The resulting interception plan at planning cycle _t_ is represented as 


where **d** swing _∈_ R<sup>3</sup> denotes the desired swing direction, _mt ∈{_ `APPROACH` _,_ `SWING` _,_ `RECOVER` _}_ denotes the current 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

6 

swing mode, and valid _∈{_ 0 _,_ 1 _}_ indicates whether the candidate is dynamically feasible. In practice, feasibility is checked through simple reachability and timing tests: the target is accepted only if the robot can translate and rotate its base into the desired pose within the available reaction time and if the predicted contact lies inside the arm-reachable hitting region. This formulation avoids fullbody trajectory search and instead reduces interception planning to geometric reasoning over the predicted projectile trajectory and the reachable contact manifold. 

## _B. Online Replanning and Swing Coordination_ 

To maintain responsiveness under fast projectile motion, the overall system is organized as three asynchronous loops running at different rates. The _perception loop_ continuously updates the latest projectile-state estimate and handles short observation dropouts. The _planning loop_ periodically invokes the interception planner in (17) and maintains both the current valid plan and the most recent valid fallback plan. The _command loop_ runs at the highest frequency and converts the active plan into SONIC-compatible motion targets. This multi-rate design decouples fast state refresh from more expensive replanning while preserving smooth command output to the controller. 

On top of this replanning mechanism, we maintain a swing state machine with three stages: 

## `APPROACH` _→_ `SWING` _→_ `RECOVER` _._ 

During `APPROACH` , the robot moves toward the desired base pose while keeping the racket arm in a ready configuration and the head oriented toward the incoming projectile. Once the robot is sufficiently close to the target base pose and the predicted contact time enters a narrow execution window, the planner commits to `SWING` . In this stage, the racket arm follows a staged impact template consisting of a backswing ( _cock_ ), contact, and follow-through phase. After the predicted impact window has passed, the state machine transitions to `RECOVER` , where the upper body and head are smoothly returned toward a neutral ready posture for the next interception cycle. 

This design separates _when_ to swing from _how_ the full body realizes the motion. The planner reasons over contact timing, base placement, and phase transitions, while the low-level realization of locomotion, balance, and coordinated whole-body motion is handled by SONIC. 

## _C. Task-Space Target Generation_ 

The active interception plan Π _t_ is converted into a set of structured task-space targets rather than joint-level commands. These targets define _what_ motion should be realized at the task level, while the low-level realization of locomotion, balance, and whole-body coordination is handled by SONIC. 

The head target pose, denoted by **T** head _∈ SE_ (3), is generated online to maintain visual attention on the 

incoming projectile. Specifically, the desired head orientation is chosen such that the nominal head forward axis aligns with the current projectile direction in the robot frame. This allows the robot to continuously observe the projectile during both the approach and swing phases. 

The wrist targets are generated from a phase-dependent strike template. For the non-dominant arm, we maintain a relatively stable support pose to avoid unnecessary upperbody disturbance. For the racket arm, the target wrist pose is computed from the current swing mode _mt_ , the desired contact point **p** hit, the desired base placement **p**<sup>des</sup> base<sup>,andthedesiredswingdirection</sup><sup>**d**swing.Let</sup> 


denote the nominal racket-wrist poses for the ready, backswing, contact, and follow-through phases, respectively. The commanded wrist poses for the left and right wrists are denoted by **T**<sup>_L_</sup> wrist<sup>_∈SE_(3)and</sup><sup>**T**</sup><sup>_R_</sup> wrist<sup>_∈SE_(3),</sup> respectively. In practice, the active wrist command is obtained by phase-dependent interpolation between the nominal templates, with the contact pose additionally aligned to the predicted interception geometry. This yields a smooth upper-body motion prior while still allowing the whole-body controller to compensate for balance and timing errors. 

In addition to the head and wrist targets, the planner outputs a desired base height and a navigation command. The desired base height, denoted by _h_ base, is adjusted to keep the hitting posture within a comfortable arm workspace. The navigation command, denoted by **u** nav, drives the base toward the target placement **p**<sup>des</sup> base<sup>with</sup> the desired heading _ψ_ des. Together, these quantities define a compact high-level motion intent: 


where **T** head and **T**<sup>_L/R_</sup> wrist<sup>are</sup><sup>_SE_(3)targetsforthehead</sup> and wrists, _h_ base is the desired base height, and **u** nav is the planar navigation command for root motion. 

## _D. Execution Interface to SONIC_ 

To decouple perception from execution, the visual estimation stack is exposed to the planner through a unified projectile-state interface. Internally, this module encapsulates RGB-D acquisition, 2D detection, temporal tracking, 3D localization, EKF filtering, and short-horizon trajectory prediction. Externally, however, the planner consumes only a compact projectile-state representation 


where **p** _t ∈_ R<sup>3</sup> and **v** _t ∈_ R<sup>3</sup> are the filtered projectile position and velocity estimates, and _ct ∈_ [0 _,_ 1] denotes the current confidence. This abstraction hides perceptionspecific details from the planning layer and allows the planner to operate on a clean dynamical state interface. 

Given _Bt_ , the interception planner computes the active plan Π _t_ in (17) and converts it into the task-space command **u** plan in (18). The planner output is then streamed 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

7 


Fig. 2: Representative motion sequence of humanoid badminton hitting in simulation. 


Fig. 3: Representative sequence of vision-based tennis hitting on the humanoid robot. 


Fig. 4: Representative sequence of vision-based badminton hitting on the humanoid robot. 

to SONIC as structured motion commands. These commands include the locomotion mode, planar movement and facing commands, desired speed, base height, and the _SE_ (3) targets for the head and wrists. SONIC interprets them as hybrid kinematic commands and realizes them through its whole-body tracking policy. 

Importantly, this interface does not require SONIC to reason about detection, tracking, or projectile-state estimation; it only consumes compact task-level motion targets. Conversely, the planner does not solve inverse kinematics or whole-body balance explicitly. The resulting architecture forms a clean perception–planning–control stack: the perception module produces an uncertaintyaware projectile state, the planner converts it into an interception intent, and SONIC realizes that intent as dynamically feasible whole-body motion. 

## VI. Experiments 

We evaluate _CyboRacket_ in both simulation and the real world, focusing on integrated hitting performance in simulation and transfer to Unitree G1. Representative motion sequences are shown in Fig. 2 for simulation, and in Fig. 3 and Fig. 4 for real-world tennis and badminton hitting, respectively. 

## _A. Simulation Experiments in MuJoCo_ 

We evaluate the complete _CyboRacket_ pipeline in a MuJoCo simulation environment that includes the humanoid robot, racket geometry, tennis ball dynamics, and court layout. In each rollout, the robot starts from a nominal ready stance, while the incoming object is launched under varying conditions. In each trial, the robot perceives the incoming object, predicts its future trajectory, plans an interception target, and executes the corresponding wholebody motion. A representative simulation sequence is shown in Fig. 2. The evaluation is conducted over 20 simulated trials. The proposed system achieves a hit rate of 75% and a return rate of 70%. 

## _B. Real-World Experiments_ 

We evaluate _CyboRacket_ on the Unitree G1 humanoid robot, equipped with a racket mounted on the right arm and an external Intel RealSense D455 RGB-D camera mounted on the head for onboard ball perception. The camera streams synchronized RGB-D observations at 90 Hz. In the tennis setting, incoming balls are launched by a ball machine under varying speeds and directions. The complete _CyboRacket_ pipeline is deployed in a visionbased tennis-hitting task, where the robot starts from a 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2015 

8 

ready pose, perceives the incoming tennis ball using the onboard RGB-D camera, predicts its future trajectory, plans an interception target, and executes the corresponding whole-body motion through SONIC. A representative real-world tennis-hitting sequence is shown in Fig. 3. These results demonstrate that the proposed perceptionto-action pipeline can be transferred from simulation to the real humanoid platform using purely onboard sensing. 

To further illustrate the generality of the proposed framework beyond tennis, we additionally present a visionbased badminton-hitting sequence on the humanoid robot, as shown in Fig. 4. This result further suggests that the proposed perception-to-action pipeline can be extended to broader humanoid racket-sport interaction scenarios. 

## VII. Conclusion 

In this work, we have presented _CyboRacket_ , a hierarchical perception-to-action framework for humanoid racket sports that has combined onboard visual perception, physics-based trajectory prediction, and large-scale pre-trained whole-body control. We have instantiated the framework on the Unitree G1 humanoid robot and have validated it in a vision-based tennis-hitting task using purely onboard sensing. The experimental results have shown that the proposed system has supported realtime object tracking, trajectory prediction, and successful striking through coordinated whole-body execution. These findings have demonstrated the potential of integrating closed-loop perception and planning with pretrained humanoid motion control for dynamic racket-sport interaction, and have provided a practical foundation for extending such capabilities to broader humanoid athletic skills. 

## References 

- [1] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025. 

- [2] T. Zhang, B. Zheng, R. Nair, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath _et al._ , “Hub: Learning extreme humanoid balance,” _arXiv preprint arXiv:2505.07294_ , 2025. 

- [3] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” in _20th Robotics: Science and Systems (RSS 2024)_ . MIT Press Journals, 2024. 

- [4] J. Tebbe, L. Krauch, Y. Gao, and A. Zell, “Sample-efficient reinforcement learning in robotic table tennis,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 4171–4178. 

- [5] D. B. D’Ambrosio, N. Jaitly, V. Sindhwani, K. Oslund, P. Xu, N. Lazic, A. Shankar, J. Abelian, E. Coumans _et al._ , “Robotic table tennis: A case study into a high speed learning system,” in _Proceedings of Robotics: Science and Systems (RSS)_ , Daegu, Republic of Korea, 2023. 

- [6] D. B. D’Ambrosio, S. Abeyruwan, L. Graesser, A. Iscen, H. Ben Amor, A. Bewley, B. J. Reed, K. Reymann, L. Takayama, Y. Tassa _et al._ , “Achieving human level competitive robot table tennis,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025. 

- [7] D. Nguyen, K. D. Cancio, and S. Kim, “High speed robotic table tennis swinging using lightweight hardware with model predictive control,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025. 

- [8] Z. Su, B. Zhang, N. Rahmanian, Y. Gao, Q. Liao, C. Regan, K. Sreenath, and S. S. Sastry, “Hitter: A humanoid table tennis robot via hierarchical planning and learning,” _arXiv preprint arXiv:2508.21043_ , 2025. 

- [9] Y. Ma, A. Cramariuc, F. Farshidian, and M. Hutter, “Learning coordinated badminton skills for legged manipulators,” _Science Robotics_ , vol. 10, no. 102, p. eadu3922, 2025. 

- [10] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, X. Da, R. Ding, C. Hogg, L. Song, E. Lim, E. Jeong, T. He, H. Xue, W. Xiao, Z. Wang, S. Yuen, J. Kautz, Y. Chang, U. Iqbal, L. J. Fan, and Y. Zhu, “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [11] K. Mülling, J. Kober, and J. Peters, “A biomimetic approach to robot table tennis,” in _2010 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2010, pp. 1921–1926, also published in _Adaptive Behavior_ , vol. 19, no. 5, pp. 359–376, 2011. 

- [12] K. Mülling, J. Kober, O. Kroemer, and J. Peters, “Learning to select and generalize striking movements in robot table tennis,” _The International Journal of Robotics Research (IJRR)_ , vol. 32, no. 3, pp. 263–279, 2013. 

- [13] Z. Wang, C. H. Lampert, K. Mülling, B. Schölkopf, and J. Peters, “Learning anticipation policies for robot table tennis,” in _2011 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2011, pp. 332–337. 

- [14] Z. Wang, A. Boularias, K. Mülling, B. Schölkopf, and J. Peters, “Anticipatory action selection for human–robot table tennis,” _Artificial Intelligence_ , vol. 247, pp. 399–414, 2017, special Issue on AI and Robotics. 

- [15] Z. Zaidi, D. Martin, N. Belles, V. Zakharov, A. Krishna, K. M. Lee, P. Wagstaff, S. Naik, M. Sklar, S. Choi _et al._ , “Athletic mobile manipulator system for robotic wheelchair tennis,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 8, no. 4, pp. 2245–2252, 2023. 

- [16] R. Xiong, Y. Sun, Q. Zhu, J. Wu, and J. Chu, “Impedance control and its effects on a humanoid robot playing table tennis,” _International Journal of Advanced Robotic Systems (IJARS)_ , vol. 9, no. 5, p. 178, 2012. 

- [17] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physicsbased character skills,” _ACM Transactions on Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, July 2018, proceedings of SIGGRAPH 2018. 

- [18] X. B. Peng, Z. Zhou, S. Luo, and M. van de Panne, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (TOG)_ , vol. 40, no. 4, pp. 1–20, July 2021, proceedings of SIGGRAPH 2021. 

- [19] T. He, Z. Luo, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” in _8th Annual Conference on Robot Learning (CoRL)_ . PMLR, 2024. 

- [20] Y. Zhang, Y. Yuan, P. Gurunath, T. He, S. Omidshafiei, A. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, and G. Shi, “Falcon: Learning force-adaptive humanoid locomanipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

- [21] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [22] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang, “Gmt: General motion tracking for humanoid whole-body control,” _arXiv preprint arXiv:2506.14770_ , 2025. 

- [23] Y. Ze, Z. Chen, J. P. Araujo, Z.-a. Cao, X. B. Peng, J. Wu, and K. Liu, “Twist: Teleoperated whole-body imitation system,” in _Proceedings of The 9th Conference on Robot Learning_ , vol. 305. PMLR, 2025, pp. 2143–2154. 

- [24] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, H. Liu _et al._ , “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 

- [25] J. Bjorck, F. Castañeda, N. Cherniadev, X. Da, R. Ding, L. J. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

