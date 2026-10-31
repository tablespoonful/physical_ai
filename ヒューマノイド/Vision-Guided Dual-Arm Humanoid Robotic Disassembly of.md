---
title: "Vision-Guided Dual-Arm Humanoid Robotic Disassembly of End-of-Life 18650 Lithium-ion Battery Packs"
date: "2026-06-06"
authors: "Yile Chen; Zhihao Liu; Xi Vincent Wang; Lihui Wang"
url: https://arxiv.org/abs/2606.08152
pdf: https://arxiv.org/pdf/2606.08152
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.08152)** / [論文ページ](https://arxiv.org/abs/2606.08152)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Vision-Guided Dual-Arm Humanoid Robotic Disassembly of End-of-Life 18650 Lithium-ion Battery Packs 

Yile Chen<sup>a</sup> , Zhihao Liu<sup>a,</sup><sup>_∗_</sup> , Xi Vincent Wang<sup>a</sup> , Lihui Wang<sup>a</sup> 

> _aKTH Royal Institute of Technology, Brinellvägen 8, 114 28, Stockholm, Sweden_ 

## **Abstract** 

The growing volume of retired lithium-ion battery packs from electric vehicles and portable electronics calls for automated disassembly that is safe, flexible, and selective down to the individual cell. Existing robotic systems, however, mostly assume known pack poses, external fixtures, or specialised tooling, leaving fixture-free cell-level disassembly under pose uncertainty largely unsolved. This paper presents a vision-guided dual-arm pipeline that disassembles a 21-cell 18650 pack from an arbitrary initial pose using only general-purpose parallel-jaw grippers, RGB-D sensing, and a pre-trained grasp detector. Pose uncertainty is absorbed by a learn-and-filter perception stack with discrete look-and-move wrist-camera corrections, while a mid-task support transfer between the two arms extends the effective workspace without any external clamp. The pipeline achieves an 8/10 end-to-end success rate, a cell-localisation root-mean-square error of 2 _._ 4 mm, and a mean cycle time of 6.0 minutes per pack, providing a practical, fixture-free building block for industrial battery recycling. 

_Keywords:_ robotic disassembly, battery recycling, dual-arm manipulation, 18650 lithium-ion battery, RGB-D perception, look-and-move correction 

## **1. Introduction** 

The accelerating electrification of transport and consumer electronics has established lithium-ion batteries as one of the most strategically important industrial commodities of the past decade. Worldwide sales of passenger electric vehicles (EVs) exceeded ten million units in 2022 and are projected to roughly double within the next several years [1]. Given a typical service life of 8–15 years, the annual volume of retired EV battery packs requiring safe and cost-effective processing is expected to reach the order of several million units by 2030, in addition to a continuous inflow of retired packs from power tools, e-bikes, and portable electronics [2]. End-of-life battery packs are not a uniform waste stream: they contain valuable cathode metals (lithium, cobalt, nickel, and manganese) whose primary 

> _∗_ Corresponding author. 

> _Email address:_ `zhihaoliu@ieee.org` (Zhihao Liu) 

supply is geographically concentrated, and they pose substantial safety risks arising from residual charge, flammable electrolytes, and the potential for thermal runaway [3]. Effective recycling therefore requires accurate, repeatable, and safe disassembly to at least the module level, and ideally to the individual cell, so that subsequent sorting and material recovery can be carried out at high purity. 

The prevailing solution is still manual disassembly. Human operators accommodate the wide diversity of pack geometries that has emerged across vehicle manufacturers, but they are also exposed to toxic and flammable gases, high-voltage terminals, and residual electrical charge throughout the process [3, 4]. Manual throughput is poorly matched to the projected scale of end-of-life inflows and is fundamentally constrained by the safety procedures that the task imposes. These factors have motivated a growing body of research on robotic battery disassembly as a complement to, or a partial replacement of, manual production lines [5, 2, 6]. 

Robotic disassembly has been demonstrated at the pack, module, and individual-cell levels of the product hierarchy, and a substantial literature has accumulated on grasp pose estimation, visual servoing, and dual-arm coordination directly relevant to the problem [7, 8, 9, 10, 11, 12]. Across these prior systems, the majority of demonstrations rely on one or more of three simplifying assumptions. First, the pack is presented in a known, fixtured pose, removing the need for vision-based localisation. Second, the disassembly procedure terminates at the module level rather than at individual cylindrical cells, circumventing the sub-centimetre localisation accuracy that cell-level extraction demands. Third, cell extraction relies on specialised tooling, such as vacuum suction or custom jigs, which restricts deployment flexibility. 

This paper addresses the gap identified above. The objective is to disassemble, to the level of individual cylindrical cells, a battery pack of unknown initial position and orientation, using a dual-arm robotic system equipped only with general-purpose parallel-jaw grippers, commodity RGB-D sensors, and a pre-trained grasp detector, and without recourse to any external fixture or custom tooling. 

The proposed solution is a vision-guided, multi-stage pipeline that decomposes the disassembly task into four sequential stages: pack acquisition, lid removal and cell dump, cell-assembly relocation, and sequential cell extraction. Each stage is implemented by a stage-specific policy that maps RGB-D observations to robot motion commands, drawing on a pre-trained GraspNet-Baseline [11] detector for grasp proposals, on look-and-move wrist-camera corrections in place of continuous visual servoing, and on a mid-task support transfer between the two arms that extends the effective workspace without any external clamp. 

The pipeline is implemented on a Realman RM75 dual-arm platform with DH Robotics AG95 grippers and three Intel RealSense D435 RGB-D cameras (one head-mounted, two wristmounted), running ROS Noetic and MoveIt 1. It is validated on a non-functional mock-up dimensionally identical to a commercial 18650 module (21 cells in a 3 _×_ 7 layout). The main contributions of this paper are as follows: 

(i) Cell-level 18650 extraction from a pack at an unknown initial pose is formulated as 

2 

a perception-driven dual-arm manipulation task, and an end-to-end implementation is reported that relies only on standard parallel-jaw grippers and commodity RGB-D sensing, without dedicated fixtures or specialised tooling. 

- (ii) A discrete-correction look-and-move perception scheme is developed that couples learned grasp proposals with a single-shot wrist-camera refinement step, offering a practical compromise between the accuracy of continuous visual servoing and the latency of open-loop planning, and extending the perception scope to the enclosure-opening and cell-localisation stages. 

- (iii) A fixture-free dual-arm support-transfer strategy is introduced, in which the two arms exchange stabilising and extracting roles to substitute kinematic coordination for dedicated mechanical fixtures. The complete pipeline is evaluated on a physical platform, and the role of each perception component is examined through ablation studies. 

The remainder of the paper is organised as follows. Section 2 reviews related work and positions the contribution. Section 3 presents the system architecture, problem formulation, motion-planning framework, and hand-eye calibration. Section 4 details the four-stage perception-and-manipulation pipeline. Section 5 reports the experimental platform, perstage and end-to-end results, ablations, and a comparison with related work. Section 6 discusses key findings, limitations, and future directions, and Section 7 concludes. 

## **2. Related Work** 

## _2.1. Robotic disassembly for battery recycling_ 

The growing scale of end-of-life battery flows has driven a sharp increase in research on robotised disassembly over the past five years. A recent systematic review by Kaarlela et al. [4] covers 63 publications and concludes that the diversity of pack designs and the safety risks of handling energised cells make fully automated disassembly difficult. The review identifies human-robot collaboration as the most practical route to combine robotic repeatability with human flexibility. Complementary reviews by Villagrossi and Dinon [5], Meng et al. [2], and Zang et al. [6] reach a similar conclusion and consistently identify perception-guided operation and flexible manipulation under pose uncertainty as the two central enabling capabilities for further automation. 

Existing disassembly demonstrations span all levels of the product hierarchy. At the pack level, the Fraunhofer DeMoBat [7] project uses industrial robots to remove bolts and cables from full automotive packs whose geometry is known a priori, demonstrating that high-payload automation is feasible when geometric uncertainty is removed. At the module level, Kay et al. [8] combine force-controlled insertion with safety interlocks for cylindricalcell extraction in a human-robot cell. Qu et al. [9] use four arms (two KUKA iiwa 14 and two Techman 14) with two-step visual localisation to disassemble plug-in-hybrid battery modules, while Liang et al. [10] report a techno-economic analysis of a robotic prismaticmodule cell whose productivity is comparable to 5.5 human workers, and Erdogan et al. [13] verify RRT-based collision-free planning for a simulated four-robot disassembly cell. At the 

3 

cell level, prior work is sparse. To the best of our knowledge, cell-level extraction of 18650 cylindrical cells without fixtures has not been demonstrated in the literature 

These works show that perception-guided robotic operation is feasible, but they also illustrate the three simplifying assumptions noted in the Introduction. Cell-level extraction of cylindrical 18650 cells without external fixtures remains under-explored: the tight packing of an 18650 array (1 mm edge-to-edge gap, 18 mm cell diameter) demands sub-centimetre localisation accuracy, which exceeds what fixed-camera setups typically deliver. 

## _2.2. Perception for grasping and disassembly_ 

Estimating feasible 6-DoF (six degrees of freedom) grasp poses from raw sensor data is a prerequisite for manipulating objects whose position and orientation are not known a priori, and the past decade has seen rapid progress on data-driven solutions to this problem. Mousavian et al. [14] were among the first to formalise grasp prediction as a sampling-andscoring problem, using a variational autoencoder to generate candidate 6-DoF grasps and a separate evaluator to score them. GraspNet-1Billion [11] scales this paradigm to a largescale benchmark with a dense point-cloud network that predicts grasp candidates directly on visible surfaces. Contact-GraspNet [15] improves efficiency in cluttered scenes by predicting contact surfaces, and AnyGrasp [16] extends the approach to robust grasp prediction across a wide range of unseen objects and viewpoints. A consistent practical limitation of these networks is the domain gap between the training distribution (diverse household objects, predominantly textured and matte) and industrial targets such as textureless, highly reflective battery enclosures. Ma et al. [17] address this through physical constraint regularisation and contact-score joint optimisation, while fine-tuning for each new pack geometry remains impractical at recycling scale due to annotation cost and the non-stationary distribution of retired EV models. 

A complementary line of work refines coarse perception with visual feedback during execution. Classical visual servoing distinguishes image-based (IBVS) and position-based (PBVS) formulations. The latter reconstructs 3-D targets from depth data and is better suited to metric manipulation tasks. Both classically run as tight feedback loops at sensor frame rate, which is incompatible with the per-call planning latency of sampling-based motion planners. A pragmatic alternative is the look-and-move variant, in which a single correction is computed from a fresh wrist-camera observation and the motion is executed open-loop to the corrected target. Zhou et al. [18] apply a coarse-to-fine vision pipeline to screw disassembly, demonstrating the practical benefit of an additional close-range correction step between coarse detection and tool engagement. 

For sub-tasks with a strong geometric prior, classical parametric detectors remain attractive. The circular end-caps of 18650 cells, for example, have a known diameter, which makes a parametric detector such as HoughCircles a natural match: it requires no training data, its parameters can be derived analytically from camera intrinsics and scene depth, and its noise characteristics admit straightforward multi-frame averaging. This suggests that, in industrial pipelines whose components have known geometry, a hybrid learn-and-filter perception stack can trade favourably against a uniformly learned alternative in terms of deployment cost and maintainability. 

4 

## _2.3. Dual-arm manipulation and coordination_ 

Dual-arm systems extend the kinematic reach and dexterity of a single robot, but introduce significant planning complexity from the higher dimensionality of the joint space and the need for mutual collision avoidance. Recent work has addressed both ends of this tradeoff. Fabrica [12] combines hierarchical task planning with learned manipulation policies to demonstrate multi-part assembly across diverse object geometries. Assembly and disassembly differ structurally: assembly proceeds toward a known target state against which progress can be verified, whereas disassembly starts from an uncertain initial state and must react to observations at each stage. Grannen et al. [19] demonstrate a bimanual stabiliseand-act coordination scheme in which one arm holds an object while the other performs precise manipulation, illustrating how role specialisation can simplify bimanual planning. 

Earlier dual-arm disassembly systems typically assume known, fixture-aligned parts. Huang et al. [20] present a human-robot collaborative cell for press-fitted components but rely on a human to position the parts precisely. 

Fixture-free coordination strategies that extend the effective workspace through interarm role exchange remain comparatively under-explored in the disassembly setting. 

Taken together, the three lines of work above leave a consistent gap. Cell-level cylindrical disassembly without fixtures is rare, learned grasp detectors are not by themselves accurate enough for the tight clearances of 18650 arrays, and dual-arm coordination has mostly been studied in assembly or fixtured settings rather than as a substitute for external clamping. The pipeline introduced in the remainder of this paper targets precisely this combination. 

## **3. System Overview and Preliminaries** 

This section introduces the system architecture and overall data flow on which the pipeline is built (Section 3.1), formalises the disassembly task as a staged decision problem (Section 3.2), and describes the motion-planning (Section 3.3), and eye-in-hand calibration with depth-to-base-frame projection (Section 3.4) components that the four-stage perception-and-manipulation pipeline of Section 4 relies on. 

## _3.1. System architecture_ 

The proposed system follows a sensing, perception, planning, and actuation pipeline distributed across two cooperating seven degrees-of-freedom (7-DoF) arms, each fitted with a parallel-jaw electric gripper, and three RGB-D cameras with complementary viewpoints (Figure 1). A head-mounted camera provides a wide, fixed-baseline view of the workspace and supplies the point clouds consumed by a learned 6-DoF grasp detector, which produces coarse grasp candidates for the arbitrarily posed pack. Each arm additionally carries a wrist-mounted camera that delivers close-range, viewpoint-independent observations of the active target. These feed classical perception modules (a depth-and-colour fused lid detector and a Hough-circle cell localiser) whose outputs serve as discrete look-and-move corrections immediately before each precision action. All perception outputs converge on a shared motion-planning layer that maintains a single transform (TF) tree, performs collision-aware trajectory generation, and issues joint and gripper commands to the two arms. 

5 


Figure 1: Overall system architecture. Three RGB-D streams feed a learned 6-DoF grasp detector and classical depth/colour perception modules. The resulting targets are consumed by a shared motion-planning layer that drives the two arms and their grippers through a common TF tree. 

This three-camera configuration reflects a deliberate division of perceptual labour. The head camera supplies the wide context required to bootstrap learned grasp detection from an unknown initial pack pose, but its viewing geometry and depth noise at table distance are inadequate for the sub-centimetre alignment required for cell extraction. The wrist cameras absorb the residual error by approaching each target before action. On the actuation side, the dual-arm layout enables a fixture-free support-transfer strategy in which the two arms exchange stabilising and extracting roles to extend the effective workspace, supported by three motion-planning modes (single-arm, parallel, and simultaneous dual-arm planning) that are invoked selectively at each stage (Section 3.3). 

## _3.2. Problem formulation_ 

We consider a tabletop disassembly task in which an intact, arbitrarily posed 18650 pack must be processed into its constituent cylindrical cells and deposited into output bins. Let _W ⊂_ R<sup>3</sup> be the visible workspace, and let _B_ 0 denote the initial pack configuration (position, orientation, internal assembly state). The combined joint configuration of the two 7-DoF arms is **q** ¯ = [ **q**<sup>_L⊤_</sup> _,_ **q**<sup>_R⊤_</sup> ]<sup>_⊤_</sup> _∈_ R<sup>14</sup> . An observation at time _t_ aggregates the active cameras _At_ as 


Table 1: Overview of the four-stage disassembly pipeline. 

|**Stage**|**Name**|**Arm(s)**|**Completion condition**|
|---|---|---|---|
|1|Battery pack acquisition|Left (+ Right parallel)|Pack held at fixed position|
|2|Lid removal & cell dump|Right + Left|Cells deposited on workspace|
|3|Cell assembly relocation|Left|Holder seated at disassembly position|
|4|Sequential cell extraction|Both|All cells in output bins|


where **I**<sup>rgb</sup> , **I**<sup>d</sup> , and **K** are the RGB image, aligned depth image, and intrinsic matrix of camera _c_ . An action is a pair of end-effector targets together with gripper commands, 


Single-arm steps set the idle arm’s target to its current pose. 

The task is decomposed into four sequential stages, and the corresponding stage policies _πk_ map observations to actions, 


where _θk_ collects the (frozen) GraspNet weights and the hand-tuned thresholds. GraspNet is the only learned component, and all remaining perception and control logic are rule-based. Table 1 summarises the stages. 

Between Stages 2 and 3, the operator removes the thin upper holder bracket (5–10 s). This part is friction-fit and cannot be reliably grasped by a parallel-jaw gripper. This is the only manual step in the pipeline. 

## _3.3. Motion planning and control_ 

MoveIt 1 on ROS Noetic exposes the dual-arm robot through three move groups: `l_arm` and `r_arm` for independent single-arm planning, and `dual_arms` for simultaneous 14-DoF planning. The primary planner is RRT-Connect [21], chosen for its bidirectional growth and proven performance on 7-DoF arms operating close to the tabletop. Path optimality is secondary to planning speed in this setting, because trajectories are generated at runtime from the current state and the workspace is relatively open. On top of this baseline, three modifications are introduced to improve reliability for the present task. 

The first modification addresses inverse-kinematics selection. For a kinematically redundant 7-DoF arm, the KDL inverse-kinematics solver [22] can return very different joint configurations across calls for the same target pose, occasionally producing unnecessarily large joint displacements. To stabilise this behaviour, multiple solutions are requested (up to _N_ = 8 attempts) and the one closest in joint space to the current configuration is selected, with an early-stop threshold _d_ stop = 0 _._ 5 rad (Algorithm 1). The selected **q**<sup>_∗_</sup> is then used as the seed for a second joint-space planning query, decoupling the kinematic solve from trajectory planning so that each can use its own parameter set. 

7 

## **Algorithm 1:** Nearest-IK multi-solution selection. 

**Input:** Move group `arm` ; target pose **T** des; attempts _N_ =8; early-stop _d_ stop=0 _._ 5 rad **Output:** Nearest joint configuration **q**<sup>_∗_</sup> and distance _d_<sup>_∗_</sup> **1 q** cur _←_ current joints; **2 q**<sup>_∗_</sup> _←_ None; _d_<sup>_∗_</sup> _←∞_ **3 for** _i_ = 1 _, . . . , N_ **do 4** (ok _, τi_ ) _←_ `arm.plan` ( **T** des) `// random IK seed` **5 if** _ok_ **_and_** _τi has waypoints_ **then 6 q** _i ←_ final waypoint of _τi_ ; **7** _di ←∥_ **q** _i −_ **q** cur _∥_ 2; **8 if** _di < d_<sup>_∗_</sup> **then 9** _d_<sup>_∗_</sup> _← di_ ; **q**<sup>_∗_</sup> _←_ **q** _i_ ; **10 if** _d_<sup>_∗_</sup> _< dstop_ **then break 11 return** ( **q**<sup>_∗_</sup> _, d_<sup>_∗_</sup> ) 

The second modification is a joint-space fallback for Cartesian planning. Approach, lift, and press-down operations use MoveIt’s Cartesian interpolation, with a small step size ( _δ_ = 5 mm) near the object and a larger one ( _δ_ = 10 mm) for transport. The planner returns the fraction _f ∈_ [0 _,_ 1] of the requested path that is feasible. When _f < f_ accept = 0 _._ 8, the Cartesian path is abandoned and the system falls back to a joint-space plan to the same target. Straight-line accuracy is sacrificed, but the trajectory remains collision-free and the task can complete. This fallback is the dominant source of robustness against the Cartesian-planning anomalies that would otherwise abort a stage. 

The third modification concerns dual-arm coordination, for which the pipeline uses three modes that trade off planning cost against safety. Separate planning moves a single arm at a time using either `l_arm` or `r_arm` , and is the default. Parallel execution plans the two arms independently and executes the resulting trajectories simultaneously. This overlaps singlearm motions but does not guarantee mutual collision avoidance, and is therefore restricted to phases in which the two motions are known to be spatially disjoint. Simultaneous planning operates in the 14-DoF `dual_arms` group and guarantees mutual avoidance at the cost of longer planning times and occasional planning failures. It is therefore reserved for steps in which the two arms must coordinate closely, such as the final dual-arm release in Stage 4. 

## _3.4. Hand-eye calibration and depth projection_ 

Each wrist camera requires a constant transform **X** = **T**<sup>_E_</sup> _C_<sup>_∈SE_(3),obtainedbysolving</sup> the standard eye-in-hand equation **A** _i_ **X** = **XB** _i_ . An ArUco marker (DICT_5X5_50, ID 2, 50 mm) is observed from _n ≥_ 10 diverse arm poses. The marker pose is recovered with `cv2.solvePnP` , and the end-effector pose comes from the MoveIt TF tree. OpenCV’s five closed-form solvers are run in parallel. Candidates with _|_ det( **R** ) _−_ 1 _| ≥_ 0 _._ 1 or _∥_ **t** _∥≥_ 0 _._ 5 m are rejected, and the result with the largest median translation norm is selected, because the median is more robust than the mean to the degenerate failure modes observed empirically. The chosen **X** is accepted when the per-axis standard deviation of the back-projected marker 

8 

Table 2: Hand-eye calibration results for the three D435 cameras. _n_ : number of calibration samples; method: winning closed-form solver among {TSAI, PARK, HORAUD, ANDREFF, DANIILIDIS}; _∥_ **t** _∥_ : translation norm; _σxy, σz_ : per-axis back-projection std. dev. on held-out poses. 

|**Camera**|_n_|**Method**|_∥_**t**_∥_(mm)|_σxy_ (mm)|_σz_ (mm)|
|---|---|---|---|---|---|
|Head (eye-to-hand)|18|TSAI|412.8|3.5|2.8|
|Left wrist|15|PARK|63.2|2.1|1.8|
|Right wrist|12|HORAUD|67.5|2.4|2.0|


is below 5 mm across all _n_ samples, otherwise additional samples are collected. 

Table 2 reports the calibration results. All three cameras pass the 5 mm threshold. Wristcamera translation norms (60–70 mm) are consistent with the physical mounting offset, and the head-camera value of approximately 413 mm reflects the overhead mounting distance. 

With **X** in hand, a point ( _u, v_ ) in a depth map projects into the camera frame through the pinhole model and into the base frame through the kinematic chain: 


where _d_ = **I**<sup>d</sup> ( _u, v_ ) and **p** ˜ is the homogeneous form. For the fixed head camera, **T**<sup>_E_</sup> _C_<sup>is replaced</sup> by the static extrinsic **T**<sup>_B_</sup> _C_<sup>.Equation(4)isinvokedbyeveryperceptionmoduleinSection4</sup> with the appropriate pixel set and camera. 

## **4. Disassembly Pipeline** 

## _4.1. Pipeline overview_ 

This section describes the four stages of the pipeline in detail. Algorithm 2 gives the toplevel control flow that the rest of the section unfolds; Figure 2 shows representative platform snapshots from each stage. For readability, all symbolic parameters ( _N_ warm, _ϵk_ , _h_ lift, _N_ avg, _δz_ , _D_ max, etc.) are introduced in context here and their numerical values, together with the rationale behind each value, are consolidated in Section 5. 

9 

- **Algorithm 2:** Top-level disassembly <u>pipeline.</u> **Input:** Pack _B_ 0 at unknown pose in workspace _W_ **Output:** All _M_ cells in output bins _D_ 

- **1** Initialise both arms to home; open grippers; warm up cameras (discard _N_ warm frames) 

- `// Stage 1: Pack acquisition` 

- **2** _g_<sup>_∗_</sup> _←_ GraspSelect( _O_ head _, W_ 1 _, ϵ_ 1) `// Algorithm 3` **3** Apply lateral correction ∆ _xB_ from left wrist camera **4** Approach _→_ grasp _→_ pitch-up _→_ lift _h_ lift _→_ transport to **p** fix _→_ open _→_ press-down _→_ re-grip (full force) 

- **5** [parallel] right arm _→_ overhead observation pose `// Stage 2: Lid removal and cell dump` 

- **6** [ _z_ lid _,_ **c** lid _, ψ_ lid] _←_ LidDetect( _O_ wrist-R _, N_ avg) `// depth+HSV+PCA` **7** Right: _Y_ -align _→_ rotate _ψ_ lid _→_ descend to _z_ lid _→_ grasp _→_ lift _→_ bin **8** Left: pitch-up _→_ flip +180<sup>_◦_</sup> _→_ tilt _→_ release cell assembly `// Manual step: operator removes upper holder bracket // Stage 3: Assembly relocation` 

- **9** _g_<sup>_∗_</sup> _←_ GraspSelect( _O_ head _, W_ 3 _, ϵ_ 3) 

- **10** Grasp (reduced force) _→_ lift _→_ transport to **p** fix _→_ position-controlled press-down ( _δz_ , max _D_ max) 

- `// Stage 4: Sequential cell extraction` 

- **11** ExtractCells(right arm) `// Phase B` **12** Support transfer: right clamps holder; left releases **13** ExtractCells(left arm) `// Phase C` **14** Dual-arm simultaneous final release 

## _4.2. Stage 1: Pack acquisition_ 

Stage 1 begins with GraspNet inference and feasibility filtering. Both arms move to home, the grippers open, and the cameras warm up by discarding their first _N_ warm frames so that auto-exposure and white balance settle. A point cloud is then constructed from the head-camera RGB-D stream, masked by the Stage 1 workspace bounding box _W_ 1, and randomly subsampled to _N_ pts = 20 000 points before being passed to GraspNet-Baseline [11], which is built on the PointNet [23] architecture. The network returns a ranked set of 6-DoF proposals _G_ = _{gi}_<sup>_N_</sup> _i_ =1<sup>withconfidencescores</sup><sup>_si∈_[0</sup><sup>_,_1],fromwhichthehighest-scoring</sup> feasible candidate is selected as 


subject to workspace, approach-angle, and quality constraints, 


where **p** _g_ is the grasp centre in the base frame, _az_ ( _g_ ) the _z_ -component of the approach direction, _ϵk_ the approach-angle tolerance, and _τ_ the minimum score. A front-surface bias 

10 


Figure 2: Snapshots of the four pipeline stages. 

further restricts the candidate set to those grasps within a distance _d_ front of the maximum- _y_ point of the cloud, targeting the accessible front face of the pack. 

A PCA-based yaw refinement then sharpens the orientation. The selected _g_<sup>_∗_</sup> inherits its yaw from the network’s prediction, which on textureless enclosures is often noisy. To improve it, principal component analysis is applied to the _xy_ -projection of the points within a radius _r_ pca = 100 mm of the grasp centre, yielding eigenvectors **v** 1 (major axis) and **v** 2 (minor axis) of the local front surface. The gripper yaw is then set to align the closing direction with the short-side direction of the enclosure, 


with a sign disambiguation against the approach vector. Algorithm 3 summarises the full selection procedure. 

11 


(a) Workspace-filtered GraspNet candidates. 


(b) PCA eigenvectors: green **v** 1 (major), blue **v** 2 (minor, used for yaw). 

Figure 3: Stage 1 perception. (a) GraspNet candidates after workspace/approach-angle filtering. (b) PCAbased yaw alignment on the pack front face. 

**Algorithm 3:** GraspNet-based <u>grasp</u> selection with PCA <u>yaw</u> alignment. 

**Input:** RGB-D observation _O_ ; workspace _Wk_ ; approach threshold _ϵk_ ; score threshold _τ_ 

**Output:** Grasp _g_<sup>_∗_</sup> with refined yaw _ψ_<sup>_∗_</sup> ; or Failure 

**1** _P ←_ point cloud from _O_ masked to _Wk_ ; 

- **2** _P ←_ subsample to _N_ pts points; **3** _G ←_ GraspNet( _P_ ) `// ranked candidates` **4** _G_ valid _←{g ∈G |_ **p** _g ∈Wk, |az_ ( _g_ ) _| ≤ ϵk,_ score( _g_ ) _≥ τ }_ 

- **5** _G_ front _←{g ∈G_ valid _|_ ( _pg_ ) _y ≥_ max _P y − d_ front _}_ **6 if** _Gfront_ = _∅_ **then** 

```
//front-surfacebias
```

- **7** retry up to 3 times; if still empty **return** Failure 

- **8** _g_<sup>_∗_</sup> _←_ arg max _g∈G_ front score( _g_ ); 

**9** _P_ loc _←{p ∈P | ∥pxy − pg∗,xy∥≤ r_ pca _}_ ; **10** [ **v** 1 _,_ **v** 2] _←_ PCA( _P_ loc projected to _xy_ ); **11** _ψ_<sup>_∗_</sup> _←_ atan2( _v_ 2 _,y, v_ 2 _,x_ ); 

**12** Disambiguate sign of _ψ_<sup>_∗_</sup> against the approach vector **a** _g∗_ ; **13 return** ( _g_<sup>_∗_</sup> _, ψ_<sup>_∗_</sup> ); 

A wrist-camera lateral correction then compensates for residual head-camera error. The grasp _g_<sup>_∗_</sup> recovered from the head camera is precise enough in depth and yaw but tends to drift laterally by several millimetres. Three error sources contribute to this drift: range-dependent D435 depth noise propagated through the head-camera standoff of approximately 400 mm, residual reprojection error from the head-camera hand-eye calibration itself ( _σxy_ = 3 _._ 5 mm, Table 2), and specular reflections on the smooth plastic enclosure that degrade the front-face point-cloud quality. The combined offset can exceed the parallel-jaw capture range, and the ablation in Section 5.4 confirms the effect: without correction, the Stage 1 success rate drops 

12 


Figure 4: Left-wrist lateral correction. Depth gating isolates the pack front surface, and the orange arrow shows the measured offset ∆ _xB_ between the column centroid _u_ cen and the calibrated reference _u_ ref. 

## from 10/10 to 7/10. 

To absorb this residual error, a single-shot look-and-move update is performed once the left arm has reached the pre-grasp pose. Its wrist camera captures one depth frame. The front surface of the pack is then extracted by depth gating, and the lateral column centroid _u_ cen of the resulting mask is compared against a pre-calibrated reference column 


in which _δu_ accounts for the lateral mounting offset of the wrist camera relative to the tool centre point (TCP). This offset is measured once by a one-time calibration experiment, in which a marked object is grasped at its centre and the wrist image is examined to read the pixel column on which the mark appears. The offset is empirically stable across the arm configurations used in the experiments (108 px on this platform). The induced lateral correction in the base frame is 


where _d_<sup>¯</sup> is the mean depth of the masked pixels and _fx_ the horizontal focal length. A symmetric _±_ 10 mm deadband suppresses sensor noise. Whenever the magnitude of the correction exceeds the deadband, the grasp target is updated by ∆ _xB_ and the arm reexecutes the pre-grasp approach to the corrected position. Transport and stabilisation conclude the stage. With the corrected target in hand, the left arm closes its gripper, pitches up to clear the worktable, transports the pack to the fixed disassembly position **p** fix, opens the gripper to let the pack settle under gravity, descends a 

13 

short distance, and finally re-grasps at full force. The descend-and-re-grasp step removes any residual error introduced during transport, so that the pack starts Stage 2 from a repeatable position and orientation. In parallel, the right arm moves to the overhead observation pose required by Stage 2. Because the two trajectories are spatially disjoint, this overlap is handled by the parallel-execution mode described in Section 3.3. 

## _4.3. Stage 2: Lid removal and cell dump_ 

Lid detection in Stage 2 uses a fused depth and colour pipeline. With the pack secured at **p** fix, the right wrist camera acquires _N_ avg = 30 frames from the overhead pose and runs a per-frame detection routine. Each frame produces a binary mask by joint depth and HSV gating, 


with the depth range [ _d_ min _, d_ max] chosen to match the wrist-to-lid standoff at the topdown pose, and the HSV region _H_ lid matched to the lid colour. Frames with too few mask pixels are discarded. For each valid frame, PCA on the mask pixels yields the image-plane short axis. Two points along this axis are back-projected with Eq. (4) to obtain the corresponding base-frame direction, from which the lid yaw is 


After rejecting frames whose height estimate deviates from the running median by more than _δz_<sup>gate</sup> = 2 mm, the yaw is aggregated by circular averaging, 


which avoids _±π_ discontinuities. The lid centre and height are the inlier means. The output triple (ˆ _z_ lid _,_ ˆ **c** lid _, ψ_<sup>ˆ</sup> lid) fully parameterises the lid-removal grasp. 

Lid removal and a gravity-assisted cell dump then follow. Given the detection result, the right arm aligns to **c** ˆlid, rotates its wrist by _ψ_<sup>ˆ</sup> lid _− ψ_ 0 to align the closing direction with the lid’s short axis, descends to _z_ ˆlid, grips at maximum force, lifts vertically, and deposits the lid in a bin. The left arm then pitches up, lifts, and flips the pack by +180<sup>_◦_</sup> to invert the cell assembly. The flip-and-tilt motion is shaped by two physical considerations. First, before the flip, the pitch is adjusted so that the contact centroid moves from the fingertips towards the gripper base. This increases the normal force and prevents the inverted pack from slipping out of the gripper during the rotation. Second, after the flip, a small additional pitch combined with a 10 % grip-force reduction allows the cell assembly to slide out under gravity while residual friction continues to hold the outer shell. This exploits the weight distribution and friction of the assembly, so that no tilt mechanism or auxiliary tool is required. The operator then removes the thin upper holder bracket (5–10 s), the only manual intervention in the pipeline. 

14 


Figure 5: Right-wrist lid detection: depth-gated and HSV-filtered mask isolates the yellow lid, and the cross-hair marks the centroid while the overlaid axes the PCA short axis used for yaw alignment. 

## _4.4. Stage 3: Cell assembly relocation_ 

After the manual bracket-removal step, the remaining cell assembly (the lower holder together with its mounted cells) lies on the workspace surface in an arbitrary pose. A new grasp candidate is recovered with Algorithm 3, this time using a workspace box _W_ 3 tuned to the post-dump region. The left arm then executes the same approach, grasp, lift, and transport sequence as in Stage 1, but with reduced grip force. Full force would squeeze the now-unsupported holder and risk shifting or detaching individual cells. 

The stage concludes with an incremental press-down that seats the holder against the workspace surface, 


with _δz_ = 5 mm and _D_ max = 80 mm. The step size is small enough for the arm’s stalldetection mechanism to register holder contact before the holder can deform, and the maximum descent exceeds the worst-case transport height error while remaining safely below the depth at which the holder would fracture. 

## _4.5. Stage 4: Sequential cell extraction_ 

Stage 4 starts with multi-frame HoughCircles cell localisation. The right wrist camera moves to the overhead observation pose and runs a five-step localisation per frame. First, depth gating removes background, worktable, and holder walls by retaining only depths inside the expected cell-top range. Second, CLAHE contrast enhancement sharpens edge contrast on the cell-top surfaces. Third, a Gaussian blur attenuates high-frequency noise prior to circle detection. Fourth, OpenCV’s `HOUGH_GRADIENT` detector searches for circles 

15 


Figure 6: Stage 2: lid detection, lid removal, and cell dump. 

whose radius lies inside bounds derived analytically from the cell radius _r_ = 9 mm and the measured scene depth _d_ , 


Fifth, a final depth filter discards detections whose centre depth falls outside the gated range. For each accepted centre ( _ui, vi_ ) with median patch depth _di_ , the 3-D cell position in the base frame is recovered through Eq. (4). 

Per-frame depth noise is reduced by accumulating _N_ avg = 100 frames and averaging, 


where _Fi_ collects the frames in which cell _i_ was detected. Frames whose total detection count deviates from the running median are excluded. This averaging step is the single most important determinant of extraction accuracy and is examined in detail in Section 5.4. 

The extraction order is then planned and a dual-arm support transfer is scheduled midstage. Cells are sorted in ascending _yB_ , so that the active arm always reaches the most 

16 

accessible remaining cell first, 


The right arm executes Algorithm 4 (Phase B) until its workspace boundary is reached. A support transfer then occurs. The right arm clamps the holder base at 80 % grip force, the left arm releases and returns to home, and the same algorithm runs again from the opposite side (Phase C). The transfer effectively doubles the workspace covered by a single arm and eliminates the need for an external clamp. For the final cell, the dual-arm group plans a coordinated simultaneous release in which the left arm transfers the cell to the bin while the right arm releases the holder. 

**Algorithm 4:** Cell extraction loop <u>(Phase</u> B or Phase C). **Input:** Wrist observation _O_ wrist; arm _a ∈{_ left _,_ right _}_ ; output bin _Da_ **Output:** Cells in _Da_ ; remaining unextracted set **1** Move arm _a_ to overhead observation pose; **2** _C_<sup>ˆ</sup> _←_ HoughAvg( _O_ wrist _, N_ avg) `// Eq.` (15) **3** Sort _C_<sup>ˆ</sup> by ascending _yB_ ; **4 foreach** _cell_ **c** ˆ _i (sorted)_ **do** 

- **5** Move arm _a_ to pre-grasp pose (table collision active); **6** Open gripper to extraction width; deactivate table collision; **7** Cartesian approach to **c** ˆ _i_ + **_δ_** offset; 

- **8** Close gripper (100 %); Cartesian vertical lift; 

- **9** Transport to _Da_ ; open gripper; 

- **10 if** _arm a at workspace limit_ **then break** 

## **11 return** _C \ {_<sup>ˆ</sup> extracted _}_ ; 

Lightweight error-recovery logic is built into each stage. If GraspNet returns no valid candidate, the system captures a fresh frame and retries up to three times before requesting manual intervention. If the Cartesian feasibility fraction _f_ drops below _f_ accept = 0 _._ 8, the system falls back to joint-space planning to the same target, sacrificing straight-line accuracy for robustness. HoughCircles outliers are absorbed by the multi-frame averaging in Eq. (15). After each vertical lift in Stage 4, a gripper-closure-distance check determines whether a cell has actually been grasped. A zero closure distance indicates a missed grasp, in which case the cell is marked as undetected and skipped. 

## **5. Experiments** 

## _5.1. Setup and protocol_ 

All experiments were carried out on a dual-arm platform realising the architecture of Section 3.1. The two manipulators are Realman RM75 7-DoF arms (5 kg payload, 610 mm reach, 0.05 mm repeatability) mounted on a shared base, each equipped with a DH Robotics AG160-95 parallel-jaw electric gripper (95 mm stroke, 45–160 N grip force, 0.05 mm repeatability, 0.9 s open/close time). Three Intel RealSense D435 RGB-D cameras (one head-mounted 

17 


(a) Right wrist (Phase B): detection on partially extracted assembly. 


Figure 7: Multi-frame averaged HoughCircles detection. Green circles mark detected cell tops, and yellow numbers indicate the planned extraction order (near-to-far in _yB_ ). 


(a) Support transfer: right arm clamps (b) Phase C: left wrist re-detects remain(c) Final dual-arm coordinated release. holder. ing cells. 

Figure 8: Stage 4: support transfer between arms and Phase C extraction. 

and one on each wrist) stream at 640 _×_ 480 px and 15–30 fps, with colour-to-depth alignment enabled through `rs.align` . In the present implementation, the left wrist camera handles lateral correction during pack acquisition and cell localisation in Phase C of Stage 4, while the right wrist camera handles lid detection in Stage 2 and cell localisation in Phase B of Stage 4. The compute unit runs Ubuntu 20.04 with ROS Noetic and MoveIt 1. Each camera is served by a dedicated daemon thread that maintains a lock-protected latest-frame buffer so that perception latency does not block the main planning thread. The work table measures approximately 1 _._ 2 _×_ 0 _._ 8 m, with constant laboratory illumination free of strong reflections. A single 18650 battery-pack mock-up was used throughout. Its external dimensions and internal cell layout match a commercial 18650 module (Table 3), and the pack was reassembled (cells reinserted, lid re-attached) between runs. 

For safety, the mock-up is intentionally non-functional. Its geometry matches a commercial product, but the cells store no electrical energy and the terminals are not live, which eliminates thermal-runaway and electrical hazards during robotic handling. Voltage and 

18 

Table 3: Battery-pack mock-up specifications. 

|**Parameter**|**Value**|**Notes**|
|---|---|---|
|Enclosure length|150 mm|long axis|
|Enclosure width|64 mm|short axis|
|Enclosure height|96 mm||
|Lid thickness|15 mm|snap-fit, no clasps|
|Cell type|18650|cylindrical|
|Cell diameter|18 mm||
|Cell height|65 mm||
|Cell count|21|3 rows _×_ 7 columns|
|Cell spacing|1 mm|edge-to-edge gap|


Table 4: MoveIt planning parameters used in all stages. 

|**Parameter**|**Value**|**Description**|
|---|---|---|
|Planning time|15 s|Maximum time per planning query|
|Planning attempts|5|Parallel attempts|
|Position tolerance|10 mm|Goal position tolerance|
|Orientation tolerance|0.10 rad|Goal orientation tolerance|
|Velocity scaling|1.0|Fraction of max joint velocity|
|Acceleration scaling|1.0|Fraction of max joint acceleration|
|Nearest-IK _d_stop|0.5 rad|Early-stop threshold|
|Cartesian step _δ_ (precision)|5 mm|Near object|
|Cartesian step _δ_ (transport)|10 mm|Long moves|
|Cartesian acceptance _f_accept|0.8|Fallback threshold|


temperature monitoring would be required for industrial deployment on packs that retain residual charge [3], and the present platform does not include this safety layer. 

The trial protocol was the same across all evaluations. At the start of each trial, the pack was placed within a _±_ 5 cm region around a nominal location reachable by the left arm, with the yaw randomly varied within _±_ 30<sup>_◦_</sup> of the nominal orientation. Placements outside this range would require a manipulator with greater payload and reach and are left to future work. Following standard practice in robotic manipulation research [16, 8], 10 trials per condition were performed for the component evaluations and 10 end-to-end trials for the full pipeline. A trial is counted as a success if the pipeline completes without unplanned manual intervention. The designated manual bracket-removal step between Stages 2 and 3 is not counted. Timings are measured from the first GraspNet inference call (or HoughCircles loop start) to the final gripper release. The 5–10 s manual bracket-removal and pack-return time is excluded from all reported timings. 

Table 4 lists the MoveIt parameters used throughout, and Table 5 consolidates the key stage-specific parameters. 

19 

Table 5: Key stage-specific parameters and their rationale. 

|**Parameter**|**Value**|**Rationale**|
|---|---|---|
|_Stage 1: Pack acquisitio_|_n_||
|GraspNet<br>sample|20 000|Default of GraspNet-Baseline.|
|count _N_pts|||
|Front-surface<br>bias|50 mm|Targets the accessible front face.|
|_d_front|||
|Approach threshold _ϵ_1|0.3|Allows approximately 17<sup>_◦_</sup>deviation from horizontal.|
|Score threshold _τ_|0.1|Lowest value rejecting boundary spurious proposals.|
|PCA radius _r_pca|100 mm|Covers the 64 mm short axis with margin.|
|Wrist offset _δu_|108 px|One-time calibration; consistent with camera-to-TCP off-<br>set.|
|Lateral deadband|_±_10mm|Suppresses depth-sensor noise.|
|_Stage 2: Lid removal & _|_cell dump_||
|Lid frames _N_avg|30|Brings _z_-std below 1 mm.|
|Depth gate[_d_min_, d_max]|[0_._214_,_0_._232]m|Matches wrist-to-lid standoff.|
|HSV gate _H_lid|_H ∈_[26<sup>_◦_</sup>_,_83<sup>_◦_</sup>],<br>_S ∈_[18_,_86],<br>_V ∈_[95_,_255]|Isolates the yellow lid under lab lighting.|
|Outlier gate _δ_<sup>gate</sup><br>_z_|2 mm|Rejects frames deviating from running median.|
|Cell-dump pitch|_−_30<sup>_◦_</sup>|Shifts contact centroid to proximal gripper face.|
|Force reduction|10 %|Lets cells slide out while shell stays held.|
|_Stage 3: Assembly reloca_|_tion_||
|Pre-grasp distance|130 mm|Clearance above 96 mm enclosure with 30 mm margin.|
|Press-down step _δz_|5 mm|Triggers stall detection without damaging holder.|
|Max depth _D_max|80 mm|Below the depth that would fracture the holder.|
|_Stage 4: Cell extraction_|||
|Averaging frames _N_avg|100|1_/_<br>_~~√~~_<br>100 = 10_×_ noise reduction.|
|Gripper opening|30 mm|6 mm clearance per side around 18 mm cell.|
|Wall offset **_δ_**offset|(_−_18_,_+18_, −_25)mm|Compensates slanted holder walls.|
|Support-transfer force|80 %|Stabilises holder without crushing it.|
|Vertical lift|80 mm|Clears holder walls; used for slip detection.|


## _5.2. Per-stage results_ 

Tables 6–9 summarise the per-stage results. With the wrist-camera lateral correction enabled, Stage 1 reaches 10/10 success at a mean cycle time of 28.0 s (Table 6). The rare failures observed without the correction occur at extreme yaw ( _|ψ| >_ 25<sup>_◦_</sup> from nominal), where the PCA alignment becomes unreliable. Stage 2 succeeded in every sub-step on every trial, including lid detection, lid removal, and cell dump (Table 7), which confirms that the fused depth and colour signal is sufficient for a coloured snap-fit lid and that the flip-and-tilt motion reliably overcomes the static friction between the cell assembly and its case. Stage 3 was likewise uniformly successful (Table 8), with the incremental press-down reaching its depth limit in all trials. In Stage 4, all 21 cells were detected in every trial and on average 20 _._ 7 _/_ 21 cells were extracted (Table 9). The rare misses correspond to extraction slips during the vertical lift rather than to detection failures. 

20 

Table 6: Stage 1 pack-acquisition evaluation ( _N_ = 10 trials per condition). 

|**Condition**|**Success**|**Mean time (s)**|
|---|---|---|
|With lateral correction|10/10|28.0|
|Without lateral correction|7/10|26.6|


Table 7: Stage 2 lid removal & cell dump ( _N_ = 10). 

|**Sub-step**|**Success**|**Mean time (s)**|
|---|---|---|
|Lid detection (30-frame)|10/10|5.5|
|Lid removal|10/10|16.5|
|Cell dump (flip+tilt)|10/10|17.7|
|**Stage 2 overall**|10/10|39.7|


Table 8: Stage 3 assembly relocation ( _N_ = 10). 

|**Metric**|**Va**|**lue**|**Notes**|
|---|---|---|---|
|Grasp + relocation success|10/|10||
|Press-down completed|10/|10|reached depth limit|
|Mean Stage 3 time|20.|9 s||


Table 9: Stage 4 cell localisation and extraction ( _N_ = 10 replicates, 100-frame averaging per detection). 

|**Metric**|**Value**|**Notes**|
|---|---|---|
|Full-count detection (21/|21)<br>10/10||
|Mean extraction success|20.7/21|cells per trial|


## _5.3. End-to-end results_ 

Table 10 summarises the ten end-to-end trials. The pipeline reached full success (all 21 cells extracted) in 8 out of 10 trials, extracting on average 20 _._ 6 _/_ 21 cells per trial with a mean cycle time of 6 _._ 0 minutes (excluding the manual bracket-removal step). Stage 4 dominates the cycle at approximately 75 % of the total time, driven by the 100-frame averaging window and the cell-by-cell extraction loop. Both are explicit accuracy and throughput trade-offs that the system designer can retune for higher throughput at the cost of reduced robustness (Section 5.4). The observed failure modes (Table 11) both occur in Stage 4. The first is a single incomplete cell detection caused by corner cells occluded by the holder, and the second is a single extraction slip during the vertical lift. No Stage 1–3 failures were observed in the ten end-to-end trials. 

## _5.4. Ablation studies_ 

Two targeted ablations isolate the contribution of the perception choices to overall reliability. 

21 

Table 10: End-to-end disassembly results ( _N_ = 10). Manual bracket-removal time is excluded from all timings. 

|**Metric**|**Value**|**Notes**|
|---|---|---|
|Full success (21/21 cells)|8/10||
|Mean cells extracted per trial|20.6/21||
|Mean Stage 1 time|28.0 s|pack acquisition|
|Mean Stage 2 time|39.7 s|lid removal & cell dump|
|Mean Stage 3 time|20.9 s|assembly relocation|
|Mean Stage 4 time|271.2 s|all cell extractions|
|**Mean total time**|6.0 min|excl. manual step|


Table 11: Failure mode summary across all end-to-end trials. 

|**Stage**|**Failure mode**<br>|**Count**|**Root cause**|
|---|---|---|---|
|1|Grasp miss (closed<br>on air)|0|Lateral offset above dead-band or extreme yaw|
|1|GraspNet:<br>no valid<br>candidate|0|Point cloud too sparse / occluded|
|2|Lid slip during re-<br>moval|0|Grasp centre near lid edge|
|2|Incomplete<br>cell<br>dump|0|Cells stuck to enclosure wall|
|4|Incomplete cell de-<br>tection|1|Corner cells occluded by holder|
|4|Cell extraction slip|1|Cell fell during lift|


The first ablation isolates the effect of the wrist-camera lateral correction in Stage 1. Table 6 compares the stage with and without the single-shot correction described in Section 4.2. Disabling the correction reduces the Stage 1 success rate from 10 _/_ 10 to 7 _/_ 10. With no compensation, the gripper systematically misses the pack whenever the residual head-camera lateral error exceeds the parallel-jaw capture range, confirming the analysis in Section 4.2. The cost of enabling the correction (a single depth frame and a re-execution of the pre-grasp approach) is negligible relative to the 30-percentage-point improvement in success rate. 

The second ablation examines multi-frame averaging in Stage 4. Ten repeated measurements were performed on the same fixed cell layout, with and without the 100-frame averaging from Eq. (15). Under the assumption of independent per-frame noise, averaging _N_ avg = 100 frames should reduce position noise by a factor of 1 _/_ _~~√~~_ 100 = 10. The empirical root-mean-square (RMS) standard deviation drops from 18 _._ 7 mm under the single-frame condition to 2 _._ 4 mm under 100-frame averaging (Table 12), a factor of approximately 7 _._ 8 that is close to the theoretical upper bound and brings the residual error well within the _±_ 6 mm per-side clearance around an 18 mm cell inside the 30 mm gripper opening. Increasing _N_ avg beyond 100 yields diminishing accuracy gains while linearly increasing the per-cell 

22 

Table 12: Ablation: multi-frame averaging effect on cell-position repeatability ( _N_ = 10 repeated measurements of the same layout). 

|**Condition**|_σ_RMS (mm)|Full det.|
|---|---|---|
|Single frame (_N_avg = 1)|18.7|6/10|
|100-frame avg (_N_avg = 100)|2.4|9/10|


Table 13: Comparison with related robotic battery-disassembly systems. Level: P = pack, M = module, C = cell. Cycle times marked “n/r” were not reported. 

|**Work**|**Level**|**Pose unc.**<sup>**a**</sup>|**Arms**|**Sensors**|**Cycle**|
|---|---|---|---|---|---|
|Kay et al. [8]|M|No|1|F/T sensor|n/r|
|_Force-controlled extraction_||||||
|Contreras et al. [13]<br>_RRT multi-robot planning_|M|Partial|4 (sim)|Cam end-eff.|n/r|
|Qu et al. [9]|M|Partial|4|2 cameras|n/r|
|_Two-step visual localisation_||||||
|Liang et al. [10]|M|No|1|Camera + F/T|32.7 min<sup>b</sup>|
|_Structured disassembly_||||||
|**Ours**|**C**|**Yes**|**2**|3 RGB-D|**6.0 min**|
|_GraspNet + wrist-cam correction +_<br>_HoughCircles_||||||


> a System handles unknown initial pose without fixtures. b 32.7 min per module (8 prismatic cells); direct comparison with the present cylindrical-cell pipeline is approximate. 

sensing time, so 100 frames is chosen as the operating point for the end-to-end evaluation. 

## _5.5. Comparison with related work_ 

Table 13 positions the present pipeline against representative robotic battery-disassembly systems. The works differ in decomposition level (pack, module, or cell), hardware and software configuration, and operating environment (simulation or real-world), so the comparison is meant for context rather than as a strict benchmark. To the best of our knowledge, ours is the first system to use a dual-arm robot and parallel-jaw grippers to perform 18650 cell-level extraction without fixed fixtures, on a pack at an unknown initial pose, while combining data-driven 6-DoF grasp estimation with rule-based perception and discrete visual correction. 

## **6. Discussion** 

Three findings emerge from the per-stage and end-to-end results. First, the wrist-camera lateral correction is essential at Stage 1. Without it, three of ten trials fail at the initial grasp because the residual head-camera lateral error exceeds the parallel-jaw capture range (Table 6). A single depth frame and a re-execution of the pre-grasp approach is sufficient to 

23 

absorb this error, suggesting that, on platforms constrained by per-call planning latency, a look-and-move correction placed at the right moment recovers most of the practical benefit of continuous visual servoing. Second, the 100-frame averaging brings cell-position noise from 18 _._ 7 mm down to 2 _._ 4 mm RMS (Table 12), a factor close to the 1 _/_ ~~�~~ _N_ avg theoretical bound, which places the residual error inside the _±_ 6 mm per-side clearance around an 18 mm cell. This noise reduction is what makes a classical detector with a known geometric prior competitive with learned alternatives at this scale. Third, the flip-and-tilt cell-dump primitive is empirically robust for this pack. A +180<sup>_◦_</sup> wrist flip combined with a small additional pitch (approximately 20<sup>_◦_</sup> ) reliably overcomes the static friction between the cell assembly and its case, eliminating the need for a dedicated tilting mechanism or auxiliary tool. 

The role of GraspNet in the proposed pipeline deserves explicit comment. The network is used as a frozen, pre-trained candidate generator followed by domain-specific filtering (workspace boundaries, approach angle, front-surface bias, and score threshold), rather than as a black-box grasp predictor. The proposal stage benefits from the network’s ability to produce geometrically reasonable 6-DoF candidates on reflective enclosures without any task-specific training data, while the filtering stage enforces the predictability and safety constraints required for industrial execution. For structured disassembly tasks with known target geometries, this learn-and-filter strategy currently yields more reliable execution than either pure learning or pure rule-based perception in isolation, and the same principle is expected to apply to other end-of-life processing pipelines whose components are geometrically constrained but spatially uncertain. 

The scope and limitations of the present evaluation also merit discussion. The pipeline is designed and validated for one commercial 18650 pack geometry. Other pack sizes or cell layouts can in principle be supported through parameter rescaling, but they require revalidation. All experiments were carried out on a non-functional mock-up, and deployment on energised packs would require an additional safety layer with voltage and temperature monitoring. Beyond this general scope, several specific limitations apply. Only a single mock-up was used, so inter-sample differences are not captured, and repeated assembly may gradually weaken the lid-retention force in ways that systematically affect Stage 2. The initial pose range was set conservatively to _±_ 5 cm and _±_ 30<sup>_◦_</sup> around the nominal placement, matched to the RM75’s 610 mm reach, and performance outside this range is untested. Filter parameters and gripper opening widths are tuned to the specific 18650 geometry, while the HSV lid filter and HoughCircles parameters are tuned to constant laboratory illumination. Both would have to be revisited for substantially different working conditions. Cell extraction is currently open-loop. A slip during the lift cannot be corrected in real time, and success is only detected post-hoc through the gripper-distance check. The upper holder bracket still requires a 5–10 s manual removal step. Finally, the ten end-to-end trials follow common practice in robotic manipulation research [8, 16] but yield wide confidence intervals. An observed 8 _/_ 10 success rate corresponds to a Wilson 95 % confidence interval of approximately [49 % _,_ 96 %], so the precise numerical success rate should be interpreted with caution, and larger-scale trials would be needed for narrower bounds. 

24 

## **7. Conclusions** 

This paper presented an end-to-end dual-arm robotic pipeline that disassembles an 18650 battery pack from an unknown initial pose using only parallel-jaw grippers, commodity RGBD sensing, and a pre-trained grasp detector, without any external fixture or custom tooling. A hybrid learn-and-filter perception stack, consisting of GraspNet candidates refined by workspace filtering, PCA yaw alignment, and a single-shot wrist-camera lateral correction, together with a fused depth and colour lid detector, and a multi-frame HoughCircles cell localiser, is combined with an in-task dual-arm support transfer to cover the full 3 _×_ 7 cell array. On a Realman RM75 platform equipped with three RealSense D435 cameras, the pipeline reached an end-to-end success rate of 8 _/_ 10, a cell-localisation accuracy of _±_ 2 _._ 4 mm (RMS), and a mean cycle time of 6.0 minutes per pack, with ablation studies confirming the necessity of both the lateral correction and the multi-frame averaging. Future work will focus on closed-loop cell extraction with force sensing, automation of the remaining manual bracket-removal step, and extension to other pack geometries. 

## **Acknowledgements** 

This work was supported by Centre of Excellence in Production Research (XPRES). 

## **Declaration of competing interest** 

The authors declare no competing interests. 

## **Declaration of generative AI and AI-assisted technologies in the manuscript preparation process** 

During the preparation of this work the author(s) used Anthropic Opus 4.7 in order to help preparing the initial draft of this manuscript, designing code for experiments, and polishing writing. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the published article. 

## **References** 

- [1] International Energy Agency, Global EV outlook 2023, Tech. rep., IEA (2023). URL `https://www.iea.org/reports/global-ev-outlook-2023` 

- [2] K. Meng, G. Xu, X. Peng, K. Youcef-Toumi, J. Li, Intelligent disassembly of electricvehicle batteries: A forward-looking overview, Resources, Conservation and Recycling 182 (2022) 106207. `doi:10.1016/j.resconrec.2022.106207` . 

- [3] G. Harper, R. Sommerville, E. Kendrick, L. Driscoll, P. Slater, R. Stolkin, A. Walton, P. Christensen, O. Heidrich, S. Lambert, A. Abbott, K. Ryder, L. Gaines, P. Anderson, Recycling lithium-ion batteries from electric vehicles, Nature 575 (2019) 75–86. `doi: 10.1038/s41586-019-1682-5` . 

25 

- [4] T. Kaarlela, E. Villagrossi, A. Rastegarpanah, A. San-Miguel-Tello, T. Pitkäaho, Robotised disassembly of electric vehicle batteries: A systematic literature review, Journal of Manufacturing Systems 74 (2024) 901–921. `doi:10.1016/j.jmsy.2024.05.013` . 

- [5] E. Villagrossi, T. Dinon, Robotics for electric vehicles battery packs disassembly towards sustainable remanufacturing, Journal of Remanufacturing 13 (2023) 355–379. `doi: 10.1007/s13243-023-00134-z` . 

- [6] Y. Zang, M. Qu, D. T. Pham, R. Dixon, F. Goli, Y. Zhang, Y. Wang, Robotic disassembly of electric vehicle batteries: Technologies and opportunities, Computers & Industrial Engineering 198 (2024) 110727. `doi:10.1016/j.cie.2024.110727` . 

- [7] KUKA AG, DeMoBat: Battery disassembly for electric cars using KUKA robots, `https://www.kuka.com/en-us/industries/solutions-database/2024/02/ fraunhofer-ipa-battery-disassembly-electric-car` (2024). 

- [8] I. Kay, S. Farhad, A. Mahajan, R. Esmaeeli, S. R. Hashemi, Robotic disassembly of electric vehicles’ battery modules for recycling, Energies 15 (13) (2022) 4856. `doi: 10.3390/en15134856` . 

- [9] M. Qu, D. T. Pham, F. Altumi, A. Gbadebo, N. Hartono, K. Jiang, M. Kerin, F. Lan, M. Micheli, S. Xu, Y. Wang, Robotic disassembly platform for disassembly of a plug-in hybrid electric vehicle battery: A case study, Automation 5 (2) (2024) 50–67. `doi: 10.3390/automation5020005` . 

- [10] C. Liang, A. Parnada, A. Gbadebo, F. Altumi, M. Qu, L. Li, A. D. Gomes, X. Lin, D. T. Pham, Y. Wang, An experimental robotic cell for the disassembly of electric vehicle battery modules, Journal of Remanufacturing 15 (2025) 381–410. `doi:10. 1007/s13243-025-00156-9` . 

- [11] H.-S. Fang, C. Wang, M. Gou, C. Lu, GraspNet-1Billion: A large-scale benchmark for general object grasping, in: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020, pp. 11441–11450. `doi: 10.1109/CVPR42600.2020.01146` . 

- [12] Y. Tian, J. Jacob, Y. Huang, J. Zhao, E. L. Gu, P. Ma, A. Zhang, F. Javid, B. Romero, S. Chitta, S. Sueda, H. Li, W. Matusik, Fabrica: Dual-arm assembly of general multipart objects via integrated planning and learning, in: 9th Annual Conference on Robot Learning, 2025. `arXiv:2506.05168` . 

- [13] C. Erdogan, C. A. Contreras, R. Stolkin, A. Rastegarpanah, Multi-robot task planning for efficient battery disassembly in electric vehicles, Robotics 13 (5) (2024) 75. `doi: 10.3390/robotics13050075` . 

- [14] A. Mousavian, C. Eppner, D. Fox, 6-DOF GraspNet: Variational grasp generation for object manipulation, in: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2019, pp. 2901–2910. `doi:10.1109/70.34770` . 

26 

- [15] M. Sundermeyer, A. Mousavian, R. Triebel, D. Fox, Contact-GraspNet: Efficient 6-DoF grasp generation in cluttered scenes, in: IEEE International Conference on Robotics and Automation (ICRA), 2021, pp. 13438–13444. `doi:10.1109/ICRA48506.2021.9561877` . 

- [16] H.-S. Fang, C. Wang, H. Fang, M. Gou, T. Liu, J. Yan, W. Liu, Y. Xie, C. Lu, AnyGrasp: Robust and efficient grasp perception in spatial and temporal domains, IEEE Transactions on Robotics 39 (5) (2023) 3929–3945. `doi:10.1109/TRO.2023.3281153` . 

- [17] H. Ma, M. Shi, B. Gao, D. Huang, Generalizing 6-DoF grasp detection via domain prior knowledge, in: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024, pp. 18102–18111. `doi:10.1109/CVPR52733.2024.01714` . 

- [18] C. Zhou, Y. Wu, W. Sterkens, M. Piessens, P. Vandewalle, J. R. Peeters, Towards robotic disassembly: A comparison of coarse-to-fine and multimodal fusion screw detection methods, Journal of Manufacturing Systems 74 (2024) 633–646. `doi:10.1016/ j.jmsy.2024.04.024` . 

- [19] J. Grannen, Y. Wu, B. Vu, D. Sadigh, Stabilize to act: Learning to coordinate for bimanual manipulation, in: Conference on robot learning, PMLR, 2023, pp. 563–576. `arXiv:2309.01087` . 

- [20] J. Huang, D. T. Pham, R. Li, M. Qu, Y. Wang, C. Ji, S. Su, W. Xu, An experimental human-robot collaborative disassembly cell, Computers & Industrial Engineering 155 (2021) 107189. `doi:10.1016/j.cie.2021.107189` . 

- [21] J. J. Kuffner, S. M. LaValle, RRT-Connect: An efficient approach to single-query path planning, in: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), 2000, pp. 995–1001. `doi:10.1109/ROBOT.2000.844730` . 

- [22] R. Smits, KDL: Kinematics and Dynamics Library, `https://www.orocos.org/kdl` (2011). 

- [23] C. R. Qi, H. Su, K. Mo, L. J. Guibas, PointNet: Deep learning on point sets for 3D classification and segmentation, in: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2017, pp. 77–85. `doi:10.1109/CVPR.2017.16` . 

27 

