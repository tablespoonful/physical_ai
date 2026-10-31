---
title: "Unified Perceptive Fall Safety for Humanoids"
date: "2026-02-18"
authors: "Osher Azulay; Zhengjie Xu; Andrew Scheffer; Stella X. Yu"
url: https://arxiv.org/abs/2602.16511
pdf: https://arxiv.org/pdf/2602.16511
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.16511)** / [論文ページ](https://arxiv.org/abs/2602.16511)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED OCTOBER, 2026 

1 

# Unified Perceptive Fall Safety for Humanoids 

Osher Azulay, Zhengjie Xu, Andrew Scheffer, and Stella X. Yu 

**_Abstract_ —Reliable fall recovery is critical for humanoids operating in cluttered environments. Unlike quadrupeds or wheeled robots, humanoids undergo high-energy impacts, complex wholebody contact, and large viewpoint changes during falls, making recovery essential. Prior work treats fall safety as separate problems (avoidance, impact mitigation, stand-up) or learns endto-end policies without vision, typically on flat terrain. More fundamentally, it couples pose, dynamics, and terrain into a single data space, requiring exhaustive coverage and limiting generalization. We present a unified visually grounded fallsafety approach spanning all phases of recovery. It builds on two insights: (1) human fall-recovery poses are structured and transferable across terrains via alignment, and (2) e** **<mark>ffective</mark> r** **<mark>ecovery</mark> d** **<mark>epends</mark> on i** **<mark>nterpreting the</mark> r** **<mark>ecovery goal</mark> in rel** **<mark>ation</mark> to** **<mark>the surrounding terrain.</mark> We train a privileged teacher using sparse human demonstrations and simulated terrains, and distill it into a deployable student that relies on egocentric depth and proprioception.** **<mark>The student predicts</mark> a** **<mark>goal-</mark> in** **<mark>-context</mark> l** **<mark>atent representing the</mark> r** **<mark>ecovery target</mark> in rel** **<mark>ation</mark> to its** **<mark>surroundings, guiding</mark> coord** **<mark>inated whole-body</mark> rea** **<mark>ctions.</mark> Experiments in simulation and on a Unitree G1 demonstrate robust zero-shot fall safety across diverse terrains. Project page: vigor2026.github.io.** 

## I. INTRODUCTION 

**H** UMANOIDStered and unevenare intendedenvironmentsto operateas humans,in the sameyet clut-they 

tered and unevenare environmentsto as humans,in yet they remain vulnerable when failures occur. Minor disturbances can quickly cascade into coupled rotations, impacts, and contact transitions, unfolding faster than conventional stabilization can correct. <mark>Humanoid fall safety</mark> d <mark>emands whole-body</mark> coordina- <mark>tion</mark> u <mark>nder</mark> s <mark>evere time pressure,</mark> as <mark>early</mark> a <mark>ctions constrain later contacts and</mark> r <mark>ecovery.</mark> 

Fall safety cannot be reduced to a post-impact reflex: How a robot falls determines which supports and contacts remain feasible, and whether standing up is possible at all. These choices depend on situational and terrain awareness, since contact feasibility and momentum redirection are shaped by local geometry invisible to proprioception alone. Fall safety thus requires the integration of terrain perception and coordinated whole-body control across the fall-recovery process. Despite the intrinsic coupling between fall and recovery, existing approaches fragment fall safety along two axes and typically rely on blind, proprioceptive-only sensing. 

First, many methods decompose fall-related behaviour into isolated subproblems: <mark>fall avoidance (preventing loss</mark> of <mark>balance),</mark> i <mark>mpact miti</mark> g <mark>ation (controlling</mark> d <mark>escent and contact</mark> to re- <mark>duce</mark> i <mark>mpact),</mark> or <mark>stand-</mark> up r <mark>ecovery (restoring stable standing).</mark> 

Manuscript received May 5, 2026; revised October 2, 2026; accepted October 13, 2026. 

> This paper was recommended for publication by Editor Olivier Stasse upon evaluation of the Associate Editor and Reviewers’ comments. 

> All authors are with the University of Michigan, Ann Arbor, MI, USA. Corresponding Author: osher@umich.edu. Digital Object Identifier (DOI): see top of this page. 


Fig. 1. **Vision-enabled unified fall safety for humanoids** . Left: fallmitigation recovery after a push towards stairs demands vision-guided anticipatory arm contact to arrest the fall. Right: recovery behaviors across diverse terrain and initial conditions highlight the generality of vision-guided contact selection and whole-body rebalancing. 

Balance controllers focus on preventing loss of stability [1], [2], while stand-up controllers are typically invoked only after the robot reaches rest in a small set of predefined poses [3]. These components are designed largely in isolation and rely primarily on proprioceptive sensing, implicitly assuming flat ground and benign contact geometry. Recovery therefore cannot be separated from _how the robot falls_ , nor from _where and how contact occurs_ . 

Second, learning-based approaches that aim to address fallrelated behaviors end-to-end often treat the problem as one of monolithic data complexity, and are typically trained without access to visual terrain perception. Reinforcement learning (RL) methods usually require extensive reward engineering, frequently leading to unnatural motions [4]. Imitation learning methods rely on dense trajectory demonstrations, often sourced from internet-scale human motion data, which transfer poorly across terrain geometry and contact conditions [5]–[7]. Both families of methods often treat environmental complexity as a monolithic data problem, entangling kinematics, dynamics, and terrain and requiring exhaustive coverage of their combinations. 

In contrast, we adopt a factorized view of data complexity (Fig. 2): Our first insight is that natural human fall and recovery poses are far more constrained than they appear: Poses required on complex terrain often admit spatially aligned and physically compatible counterparts on flat terrain. This observation allows pose and terrain variation to be treated 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED OCTOBER, 2026 

2 


Fig. 2. **Factorized data generation yields sample-efficient imitation and scalable adaptation for humanoid fall safety learning.** Rather than treating pose, time, and terrain as a single monolithic data space requiring exhaustive coverage, we factorize it into a small set of human pose trajectories from real-world demonstrations on flat terrain and independently varying terrain geometry in simulation. 

as largely independent factors. As a result, a few human demonstrations collected on flat ground can serve as priors on kinematics and dynamics, while variation in terrain geometry, contact timing, and momentum redirection is handled through RL via interaction with the environment. 

<mark>Our second</mark> i <mark>nsight</mark> is <mark>that</mark> r <mark>ecovery goals must</mark> be u <mark>nderstood</mark> in rel <mark>ation</mark> to <mark>the</mark> te <mark>rrain</mark> on <mark>which they are</mark> rea <mark>lized.</mark> A <mark>motion prior provides whole-body</mark> coordin <mark>ation, while the current body state and</mark> l <mark>ocal</mark> g <mark>eometry</mark> dete <mark>rmine which contacts can support that</mark> r <mark>ecovery.</mark> 

We therefore build the policy directly on a compact visual goal-in-context latent representation, which integrates the next target pose with the local terrain and body context in a single perceptual-motor space. 

Based on these insights, we introduce VIGOR ( _<u>Visual Goal-</u> In-Context Inference_ ), a <mark>perceptive control framework that unif</mark> i <mark>es fall avoidance,</mark> i <mark>mpact miti</mark> g <mark>ation, and stand-</mark> up r <mark>ecovery.</mark> A privileged teacher policy is trained via RL using sparse human demonstrations on flat terrain together with access to local terrain geometry, yielding terrain-aware reactive behaviours. This knowledge is then distilled into a deployable student policy that operates using only egocentric depth observations and short-term proprioceptive history. L <mark>atent</mark> s <mark>upervision guides the student’s</mark> inte <mark>rpretation</mark> of its r <mark>ecovery</mark> ta <mark>rget, while</mark> a <mark>ction</mark> imit <mark>ation guides the</mark> r <mark>esulting control.</mark> 

Our contributions are threefold: 

- We formulate humanoid fall safety as a unified, _visually grounded_ control problem spanning fall mitigation, impact handling, and stand-up recovery within a single policy. To <mark>our knowledge, this</mark> is <mark>the f</mark> i <mark>rst learning-based framework for unif</mark> i <mark>ed perceptive</mark> h <mark>umanoid</mark> r <mark>ecovery.</mark> 

- We introduce a factorized data formulation that decouples human fall-recovery motion from terrain variation, enabling sample-efficient learning from a small set of flatground human demonstrations combined with large-scale terrain randomization. 

- <mark>We</mark> i <mark>ntroduce</mark> a v <mark>isual</mark> r <mark>ecovery policy trained through</mark> inte <mark>rmediate</mark> l <mark>atent</mark> s <mark>upervision alongside</mark> a <mark>ction</mark> imit <mark>ation.</mark> A <mark>privileged teacher guides the student</mark> to i <mark>nfer</mark> r <mark>ecovery</mark> ta <mark>rgets suited</mark> to <mark>the surrounding</mark> te <mark>rrain,</mark> u <mark>sing only egocentric depth and proprioceptive history.</mark> 

We evaluate VIGOR extensively in simulation and demonstrate zero-shot transfer to a real humanoid across diverse fall and recovery conditions, validating a unified vision-enabled approach to humanoid fall safety. 

## II. RELATED WORK 

## _A. Humanoid Fall Mitigation and Standing-Up Control_ 

<mark>Humanoid fall safety</mark> r <mark>equires managing</mark> i <mark>mpacts and restoring stable standing.</mark> Prior work typically decomposes recovery into two disjoint stages: fall mitigation during descent and standing up after impact. Classical fall mitigation methods focus on maintaining balance or redirecting momentum to reduce impact forces [1], [2], while learning-based approaches similarly emphasize safe landing or damage reduction without explicitly addressing subsequent recovery [8]. <mark>Stand-</mark> up <mark>controllers typically act</mark> after <mark>the robot has settled into predef</mark> i <mark>ned conf</mark> igur <mark>ations</mark> [9], a <mark>lthough</mark> r <mark>ecent learning-based methods</mark> e <mark>xtend</mark> r <mark>ecovery</mark> to <mark>more</mark> d <mark>iverse</mark> in <mark>itial poses</mark> [4], [10]. Only a few works attempt to unify fall mitigation and standing-up within a single policy [11], [12], but these approaches typically rely on limited sensing or blind operation. In contrast, we learn a _unified, visually grounded_ policy that explicitly couples fall mitigation and recovery under diverse terrain conditions. 

## _B. Visual Whole-Body Control_ 

Methods in vision-based control have recently enabled humanoids to perform complex whole-body behaviors under partial observability [13]. Visual input has been used to support loco-manipulation and contact-rich interaction [14]–[16], as well as to guide navigation and locomotion across challenging environments [17]–[19]. Visual reinforcement learning has also produced active perception during whole-body manipulation in simulated humanoids [20]. Despite this progress, fall recovery remains perceptually challenging: rapid body rotations, self-occlusion, and intermittent ground contact produce unstable visual observations. Visually grounded fall recovery is still largely unexplored, especially for policies spanning fall mitigation, impact, and stand-up recovery. 

## _C. Motion Priors and Style-Constrained RL_ 

<mark>Learning whole-body control</mark> r <mark>equires</mark> coord <mark>inating many joints through changing contacts.</mark> Prior work therefore relies on carefully shaped multi-term reward functions [13], [21] or constrains the control problem through reduced body representations or limited link actuation [18]. Human motion priors provide an alternative form of regularization, inducing behavior with minimal reward engineering. 

Reference-guided RL methods such as DeepMimic [22] and AMP [23] demonstrate strong whole-body control on 

AZULAY _et al._ : UNIFIED PERCEPTIVE FALL SAFETY FOR HUMANOIDS 

3 


Fig. 3. **Overview of VIGOR. 1)** Human fall–recovery demonstrations <mark>collected</mark> on <mark>f</mark> l <mark>at ground</mark> are kinematically retargeted to the robot. **2)** Reference poses are <mark>used</mark> d <mark>irectly</mark> on flat terrain and coarsely projected onto uneven terrain to provide sparse tracking targets. **3)** A privileged RL teacher learns a goal-in-context latent <mark>representing the</mark> i <mark>mmediate</mark> r <mark>ecovery</mark> ta <mark>rget</mark> in rel <mark>ation</mark> to l <mark>ocal</mark> te <mark>rrain.</mark> **4)** A <mark>student learns through</mark> l <mark>atent</mark> s <mark>upervision and</mark> a <mark>ction</mark> imit <mark>ation,</mark> u <mark>sing only egocentric depth and proprioceptive history</mark> at d <mark>eployment.</mark> 

flat terrain, but often rely on dense trajectory tracking or periodic motion assumptions, which become limiting in highly non-periodic, contact-rich behaviors such as fall recovery. Recent work relaxes dense tracking through higher-level structural guidance, including keyframe-based objectives [5], styleconstrained learning [6], or hybrid formulations that combine flat-terrain imitation with residual adaptation on uneven terrain [7]. These methods allow deviation from demonstrations when needed, but still depend on sufficient motion–terrain coverage. We therefore treat human fall-recovery demonstrations as _sparse structural priors_ rather than dense trajectory targets. 

## III. METHOD 

We propose VIGOR, a unified framework for humanoid stand-up, fall mitigation, and recovery in unstructured environments, as illustrated in Fig. 3. Unlike pipelines that treat falling, impact mitigation, and standing as separate modules, VIGOR learns the full process with a single control policy conditioned on onboard egocentric sensing. 

Following a destabilizing disturbance, the robot may enter arbitrary configurations involving high-energy impacts, whole-body contact, and large changes in body orientation. At each timestep _t_ , the robot receives proprioception **o** _t_ = [ **_ω_** _t,_ **g** _t,_ **q** _t,_ **q** ˙ _t,_ **a** _t−_ 1] _,_ where **_ω_** _t_ is the base angular velocity, **g** _t_ is projected gravity, **q** _t_ and **q** ˙ _t_ are joint positions and velocities, and **a** _t−_ 1 is the previous action. The policy outputs joint-space PD targets **a** _t_ for the 23-DoF humanoid. 

To learn recovery under these conditions, we adopt a privileged teacher–student design. During training, the teacher _πθ_ observes the current proprioception **o** _t_ , sparse keyframe targets **k** _t_ , and local terrain samples **h** _t_ , which provide structured recovery intent and terrain context. The deployable student _πϕ_ does not access these privileged inputs. Instead, it receives proprioceptive history **o** _t−T_ : _t_ and stacked egocentric depth **I** _t−k_ : _t_ from a head-mounted camera, and learns to reconstruct the teacher’s _visual goal-in-context_ latent. This enables unified vision-based fall mitigation and recovery from onboard sensing. 

## _A._ _<mark>Motion–Terrain Factorization</mark>_ 

<mark>Motion–</mark> te <mark>rrain factorization</mark> r <mark>emoves the need for</mark> te <mark>rrainmatched demonstrations: f</mark> l <mark>at-ground motions supply</mark> r <mark>ecovery structure, while RL learns</mark> te <mark>rrain-specif</mark> i <mark>c contacts and</mark> dy- <mark>namics.</mark> We obtain fall–recovery demonstrations from monocular human videos recorded on flat ground, covering prone, forward, sideways, and backward recoveries. We process the videos with VideoMimic [24] and retarget the reconstructed motions to the Unitree G1 using kinematics-aware mapping with conservative pelvis and hip constraints to reduce artifacts. We retain nine high-quality recovery sequences from three body sizes. Rather than tracking full trajectories, we uniformly subsample sparse keyframes at _∼_ 5 Hz. These keyframes provide coarse structural priors for the privileged teacher while allowing RL to adapt contact timing, momentum redirection, and terrain-dependent recovery. During training, keyframes are coarsely aligned to terrain by a vertical shift: 


where _h_ ( _·_ ) is the terrain height at link position **p**<sup>ref</sup> _i_<sup>.All</sup> reference poses are shifted by ∆ _z_ to maintain terrain clearance and are initialized near the terrain center with small _x_ – _y_ perturbations. To increase coverage, we randomize the reference trajectory, temporal phase, global transformations, and occasionally add a short free-fall interval by suppressing a random subset of joint torques before control begins. 

## _B. Privileged Goal-in-Context Teacher_ 

We train a privileged fall-mitigation and recovery teacher policy _πθ_ using PPO [25]. Training proceeds in two stages: first on flat terrain to acquire basic fall mitigation and stand-up behaviors, and then on randomized non-flat terrains to handle diverse contact geometry and perturbations. The teacher receives proprioception **o** _t_ , sparse keyframe targets **k** _t_ , and privileged terrain samples **h** _t_ . The reference and terrain signals are fused into a single _goal-in-context_ latent **z** _g_ = _F_ � **k** _t,_ **h** _t_ � _,_ which encodes the immediate recovery target conditioned on local terrain context. <mark>We normalize the projected</mark> l <mark>atent</mark> as **z** _g_ = _~~√~~ d_ ¯ **z** _g/∥_ **z** ¯ _g∥_ 2 to <mark>maintain</mark> a <mark>cons</mark> i <mark>stent scale for policy</mark> 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED OCTOBER, 2026 

4 

<mark>conditioning and dist</mark> ill <mark>ation.</mark> The teacher actor conditions on this latent and proprioception to produce joint targets: **a** _t_ = _πθ_ � **z** _g,_ **o** _t_ � _._ While the teacher is trained in a trackingbased manner similar to prior motion imitation policies [22], the reference signals are intentionally sparse and enforced only at a coarse, relative level. Together with privileged terrain observations, this under-specification allows RL to resolve contact timing, body placement, and terrain-dependent execution details beyond what is prescribed by the demonstrations. 

## _C. Reward Design_ 

We design a composite reward function to support fall mitigation, stabilization, and recovery within a single policy: _rt_ = _rt_<sup>imit</sup> + _rt_<sup>reg</sup> + _rt_<sup>post</sup> 

where _rt_<sup>imit</sup> is a DeepMimic-style tracking term [22] _, rt_<sup>reg</sup> aggregates standard motion-regularization penalties, and _rt_<sup>post</sup> provides post-recovery stabilization by rewarding upright hold and suppressing residual motion once standing. All reward terms are summarized in Table I. 

**Motion imitation.** We project reference poses, recorded on flat ground, onto the simulated terrain before computing tracking errors, as described in Sec. III-A. This preserves the demonstrated motion structure but is not physically exact on uneven terrain, leaving small residual offsets. Tracking full world-frame positions _∥_ **p**<sup>ref</sup> _i,t_<sup>_−_</sup><sup>**p**</sup><sup>_i,t∥_wouldthereforepenalize</sup> projection residuals and terrain-dependent deviations needed for recovery. Instead, we define imitation targets in a rootrelative canonical frame by comparing ( **p**<sup>ref</sup> _i,t_<sup>_−_</sup><sup>**p**</sup> 0<sup>ref</sup> _,t_<sup>)</sup><sup>_−_(</sup><sup>**p**</sup><sup>_i,t −_</sup> **p** 0 _,t_ ), preserving relative body configuration while remaining insensitive to projection artifacts, allowing demonstrations to act as structural priors rather than exact pose targets. 

**Regularization and safety.** The term _rt_<sup>reg</sup> aggregates standard regularization penalties, including joint limit violations, joint velocities, accelerations, momentum change, action smoothness, undesired contacts, and contacts near terrain edges. These terms stabilize learning and reduce unsafe behaviors without prescribing a specific recovery strategy. 

**Post-recovery stabilization.** Once the robot reaches an upright configuration, _rt_<sup>post</sup> encourages stable upright posture by suppressing residual base motion and joint velocities. 

## _D. Egocentric Student Policy_ 

At deployment time, the robot relies only on onboard sensing. The student therefore learns to infer the teacher’s goal-in-context latent from egocentric depth and short-term proprioceptive history. The same sparse demonstrations used to train the teacher define the space of recovery behaviors available to the student, which infers an appropriate recovery target without explicit reference signals. 

The student receives egocentric depth **I** _t−k_ : _t_ and proprioceptive history **o** _t−T_ : _t_ . These inputs are fused into a predicted _visual_ goal-in-context latent **z** ˜ _g_ = _G_ � **I** _t−k_ : _t,_ **o** _t−T_ : _t_ � _,_ which is designed to capture the terrain-conditioned recovery objective. To i <mark>nfer this</mark> l <mark>atent, the student</mark> e <mark>ncodes depth with</mark> a <mark>CNN and proprioceptive history with</mark> a <mark>temp</mark> oral e <mark>ncoder. The</mark> r <mark>esulting features are concatenated and projected through</mark> an <mark>MLP, then</mark> 

TABLE I 

**REWARD TERMS USED FOR FALL-RECOVERY LEARNING** . 

|**Reward**|**Definition**|**Weight**|
|---|---|---|
||_Motion imitation_<br><sup>2</sup>||
|Pos. track.|exp(_−∥_∆_x∥/σ_)<br>|1_._25|
|Rot. track.|exp(_−∥_∆_θ∥_<sup>2</sup>_/σ_)<br>|0_._5|
|Lin. vel. track.|exp(_−∥_∆_v∥_<sup>2</sup>_/σ_)<br>|0_._125|
|Ang. vel. track.|exp(_−∥_∆_ω∥_<sup>2</sup>_/σ_)<br>|0_._125|
|Joint pos. track.|exp(_−∥_∆_q∥_<sup>2</sup>_/σ_)|0_._5|
|Joint vel. track.|exp(_−∥_∆˙_q∥_<sup>2</sup>_/σ_)|0_._125|
||_Regularization & safety_||
|Torque penalty|_∥τ∥_<sup>2</sup>|_−_10<sup>_−_6</sup>|
|Torque limit|max(0_, |τ| −τ_max)|_−_0_._1|
|Joint pos. limit|max(0_, q −q_max) + max(0_, q_min _−q_)|_−_10|
|Joint vel. limit|max(0_, |_˙_q| −_˙_q_max)<br>|_−_5|
|Joint acc.|_∥_¨_q∥_<sup>2</sup>|_−_2_._5_·_10<sup>_−_7</sup>|
|Momentum change|_∥_∆_p∥_<br>|_−_5_·_10<sup>_−_3</sup>|
|Body yank|_∥_∆_F ∥_<sup>2</sup>|_−_2_·_10<sup>_−_6</sup>|
|Joint vel. penalty|_∥_˙_q∥_<sup>2</sup><br>|_−_10<sup>_−_4</sup>|
|Action rate|_∥at −at−_1_∥_<sup>2</sup>|_−_0_._1|
|Undesired contacts|_r_contacts [26]|_−_0_._1|
|Foothold|_r_foothold [21]|_−_1|
||_Post-recovery stabilization_<br><sup>2</sup>||
|Head height|exp(_−∥_∆_h∥/σ_)<br>|0_._25|
|Base lin. vel.|_∥_**v**base_∥_<sup>2</sup><br>|_−_0_._01|
|Base ang. vel.|_∥_**_ω_**base_∥_<sup>2</sup>|_−_0_._05|


<mark>normalized</mark> as in <mark>the teacher.</mark> The student actor conditions on this latent and current proprioception to produce joint targets: **a** ˜ _t_ = _πϕ_ � **z** ˜ _g,_ **o** _t_ � _._ 

We train the student by distilling from the privileged teacher using a hybrid of behavioral cloning and DAgger-style [27], [28] rollouts. Supervision is applied over a mixture of teacherand student-induced state distributions, 


where _ρπθ_ and _ρπϕ_ denote the distributions induced by teacher and student rollouts, respectively. The mixing coefficient _α_ is annealed from 1 toward 0 during training, gradually shifting rollouts from teacher-driven supervision to student-induced states. The student is trained using weighted behavior-cloning and goal-in-context reconstruction losses: 


Teacher rollouts provide stable demonstrations that rapidly imprint recovery behavior, while student rollouts expose the policy to off-distribution states and improve adaptability. 

Although the teacher is trained with motion-tracking signals that include intentional falls, the student is distilled from unstable initial states, which biases it toward stabilization rather than deliberate falling. Therefore, without disturbance the policy maintains a stable posture; under disturbance, it mitigates fall severity and recovers. 

## _E. Domain Randomization_ 

To improve robustness and sim-to-real transfer, following prior works [16], [28], we randomize both dynamics and perception at the start of each episode and throughout rollout. On the dynamics side, we randomize friction and restitution, and further vary the episode initialization described in Sec. III-A, including the reference motion clip and phase, planar position, yaw, initial pose, and joint states. We additionally apply stochastic external pushes and occasional joint torque dropouts to mimic disturbances and partial actuator failures. On the perception side, we perturb depth observations using 

5 

AZULAY _et al._ : UNIFIED PERCEPTIVE FALL SAFETY FOR HUMANOIDS 


Fig. 4. <mark>Training</mark> te <mark>rrains, from left</mark> to <mark>right: f</mark> l <mark>at, wave, rough, slope, stairs, and</mark> i <mark>nverted stairs.</mark> One representative difficulty is shown. 

depth clipping and non-linear remapping, multiplicative noise, spatial and temporal dropout, synthetic occlusions, and small camera pose jitter. These perturbations encourage the policy to rely on stable geometric structure. 

TABLE II 

<mark>EVALUATION METRICS.</mark> 

|**Metric**|**Definition**|
|---|---|
|SR _↑_(%)|Success with upright stabilization within 7_._5 s.|
|SSR _↑_(%)|Stable Success without re-fall.|
|Time _↓_(s)|Time to recovery.|
|PIF _↓_|Peak internal-force magnitude.|
|_F_c _↓_(kN)|Peak contact force across all links.|
|FR _↓_(%)|Subsequent re-fall rate.|
|Drift _↓_(m)|Horizontal pelvis displacement.|
|MPJPE _↓_(cm)|Pelvis-relative joint tracking error.|


## IV. EXPERIMENTS 

## _A. Implementation Details_ 

We summarize the main components of our simulation, training, and deployment setup below. For more visual results, see the supplementary multimedia. 

**Simulation Setup.** We use a 23-DoF Unitree G1 with a head-mounted depth camera in IsaacGym and IsaacSim, controlled at 50 Hz with a 7.5 s recovery horizon. Training proceeds in two phases. The policy is first trained on flat terrain to acquire core stand-up and impact-mitigation behaviors, and is then continued on randomized non-flat terrains, as shown in Fig. 4. We train the teacher with PPO using 4,096 parallel environments, then distill it into the visual student using 512 environments. 

**Real-World Setup:** Hardware experiments are performed on a Unitree G1 equipped with an Intel RealSense head mounted depth camera. Proprioception streams at 500 Hz and depth at 30 Hz. The student policy runs at 50 Hz and outputs joint-space position targets to the low-level PD controller. Depth preprocessing mirrors simulation, and deployment is _fully zero-shot_ without any real-world fine-tuning. 

## _B. Simulated Experiments_ 

We evaluate policies under two initialization regimes on terrains sampled from the families shown in Fig. 4. In both cases, initial planar position and yaw are randomized. 

In _Stand-Up_ , episodes start from low-body configurations sampled around the lowest keyframe of each demonstration, with pose noise. In _Fall-Recovery_ , episodes start earlier in the motion, near the onset of falling, with random perturbations and nonzero base velocity, requiring the policy to handle impact mitigation and recovery on varying terrain geometry. Unless otherwise stated, results are reported in IsaacGym. 

**Metrics.** <mark>Simu</mark> l <mark>ation</mark> r <mark>esults</mark> in <mark>this section use 500</mark> tr <mark>ials per seed across three different evaluation seeds.</mark> T <mark>able</mark> II d <mark>ef</mark> i <mark>nes the evaluation metrics.</mark> 

## _C. Simulated Results_ 

**Teacher Ablations.** We evaluate teacher-side ablations to isolate the contribution of privileged structure and supervision. NoKeypoints removes keypoint-based observations. DofKeypoints replaces spatial keypoint positions with joint angle targets. AbsTrack trains the teacher using absolute pose tracking objectives instead of relative tracking. NoScandots removes access to privileged terrain information, while Teacher denotes the full privileged teacher. 

TABLE III 

TEACHER ABLATIONS UNDER STAND-UP AND FALL-RECOVERY. 

|**Method**||**Stand-Up**||**Fa**|**ll-Recover**|**y**|
|---|---|---|---|---|---|---|
||SR_↑_|SSR_↑_|Time_↓_|SR_↑_|SSR_↑_|Time_↓_|
|NoKeypoints|57.4(_±_4.1)|53.2(_±_3.0)|6.9(_±_1.3)|76.1(_±_3.1)|73.2(_±_3.4)|6.3(_±_1.5)|
|DofKeypoints|86.6(_±_3.1)|80.5(_±_3.4)|5.8(_±_1.0)|84.1(_±_2.9)|80.1(_±_2.4)|5.5(_±_0.9)|
|AbsTrack|73.1(_±_3.0)|70.0(_±_3.5)|5.7(_±_2.0)|70.4(_±_3.5)|67.3(_±_3.8)|5.6(_±_2.1)|
|NoScandots|84.4(_±_3.8)|70.0(_±_3.4)|5.6(_±_1.7)|88.3(_±_3.7)|77.6(_±_4.6)|6.4(_±_1.6)|
|Teacher|**98.0 (**_±_**0.3)**|**97.6 (**_±_**0.2)**|**4.2 (**_±_**1.0)**|**96.3 (**_±_**0.8)**|**95.7 (**_±_**1.2)**|**5.3 (**_±_**0.9)**|


Table III highlights the role of structural priors in the teacher. <mark>Removing keypoint guidance causes the largest degra-</mark> d <mark>ation</mark> in <mark>Stand-Up, while</mark> r <mark>eplacing</mark> rel <mark>ative tracking with</mark> abs <mark>olute tracking causes the largest degradation</mark> in <mark>Fall-Recovery.</mark> Similarly, replacing spatial keypoints with joint-angle targets (DofKeypoints) partially recovers performance but remains below the full model, suggesting that geometric body configuration provides stronger guidance than joints alone. Removing privileged terrain samples (NoScandots) limits the teacher’s scene awareness. The full privileged Teacher achieves the best overall performance. 

**Baselines.** We compare VIGOR with pretrained HOST [4] and FIRM [12] policies, using HOST’s official checkpoints and a FIRM checkpoint provided by its authors. HOST learns separate RL stand-up policies for different initial configurations, while FIRM r <mark>etrieves keyframe goal features</mark> to <mark>cond</mark> i- <mark>tion</mark> a <mark>diffusion policy.</mark> As no prior visual baseline exists for humanoid fall recovery, we analyze perception through student ablations. 

Table IV reports average recovery performance across all simulated terrains for both Stand-Up and Fall-Recovery. 

<mark>VIGOR achieves substantially higher</mark> r <mark>ecovery and stable success than the pretrained baselines</mark> in <mark>the evaluated settings.</mark> 

**Student Ablations.** We ablate student-side components of VIGOR while keeping training conditions fixed. w.o Shared removes intermediate latent supervision, retaining action imitation. w.o Vision removes egocentric depth input, yielding a proprioception-only student. w.o History removes temporal observation history, restricting the student to single-step observations. VIGOR includes egocentric depth, temporal history, and intermediate latent supervision. <mark>Separate</mark> r <mark>etains</mark> l <mark>atent</mark> s <mark>upervision but</mark> r <mark>eplaces the shared goal–</mark> te <mark>rrain projection with separate</mark> e <mark>ncodings, whose concatenation the student predicts.</mark> 

Table V <mark>shows that</mark> v <mark>ision and</mark> inte <mark>rmediate</mark> l <mark>atent</mark> s <mark>uperv</mark> i- <mark>sion both contribute substantially</mark> to r <mark>ecovery. Removing</mark> v <mark>ision</mark> 

6 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED OCTOBER, 2026 


TABLE IV 

AVERAGE SIMULATED RECOVERY PERFORMANCE. 


Fig. 6. <mark>Demonstration scaling. Recovery success (SR) and stable success (SSR) for</mark> v <mark>isual students</mark> s <mark>upervised</mark> by <mark>teachers trained with one, four,</mark> or <mark>nine</mark> h <mark>uman demonstrations,</mark> u <mark>nder Stand-Up and Fall-Recovery.</mark> 

<mark>causes the largest</mark> r <mark>eduction</mark> in <mark>stable success</mark> in <mark>both tasks, while</mark> r <mark>emoving</mark> inte <mark>rmediate</mark> l <mark>atent</mark> s <mark>upervision also substantially</mark> d <mark>egrades</mark> r <mark>ecovery, supporting</mark> r <mark>ecovery-level guidance</mark> b <mark>eyond</mark> a <mark>ction</mark> imit <mark>ation. The blind student</mark> i <mark>nheri</mark> ts <mark>strong</mark> re- <mark>covery skills from the teacher and can f</mark> i <mark>nd support and</mark> r <mark>egain</mark> a <mark>stable posture even</mark> after te <mark>rrain collisions. Separate achieves comp</mark> ar <mark>able</mark> r <mark>ecovery success but lower stable success. An</mark> add <mark>itional evaluation also f</mark> i <mark>nds higher peak contact forces for Separate than VIGOR (2.4 versus 2.0 kN). Temp</mark> oral <mark>history provides</mark> a <mark>clearer bene</mark> fit in <mark>Stand-Up, where successive contacts must</mark> be coord <mark>inated.</mark> Its <mark>smaller bene</mark> fit in <mark>Fall-Recovery</mark> is <mark>cons</mark> i <mark>stent with greater</mark> r <mark>eliance</mark> on i <mark>mmediate feedback during rapid</mark> d <mark>escent.</mark> 

**<mark>Recovery Across Terrain Conditions.</mark>** <mark>Factorization lets f</mark> l <mark>at-ground demonstrations guide</mark> r <mark>ecovery across varied</mark> ter- <mark>rain contacts. We evaluate the teacher and students</mark> on <mark>steps, slopes, waves, and</mark> u <mark>nseen rubble (Fig.</mark> 5 ), <mark>without new demonstrations</mark> or <mark>f</mark> i <mark>ne-tuning.</mark> _<mark>Nominal</mark>_ <mark>uses random starts</mark> on <mark>standard</mark> te <mark>rrain;</mark> _<mark>Placement</mark>_ <mark>varies starts and headings around</mark> te <mark>rrain features;</mark> _<mark>Geometry</mark>_ i <mark>ncreases</mark> te <mark>rrain severi</mark> ty by <mark>doubling heights and gradients.</mark> 

<mark>Placement changes have</mark> rel <mark>atively</mark> little e <mark>ffect, whereas</mark> in- <mark>creased</mark> g <mark>eometry</mark> r <mark>educes</mark> r <mark>ecovery,</mark> esp <mark>ecially</mark> on <mark>rubble. The teacher’s performance</mark> on u <mark>nseen rubble supports transfer</mark> of <mark>f</mark> l <mark>at-ground motion priors. On</mark> u <mark>nseen rubble, VIGOR and Separate reach standing</mark> at <mark>simi</mark> lar <mark>rates, but VIGOR more</mark> o <mark>ften maintains stable</mark> r <mark>ecovery; the blind policy performs worse</mark> on 

### TABLE V 

STUDENT ABLATIONS UNDER STAND-UP AND FALL-RECOVERY. 


Fig. 7. <mark>Stair</mark> r <mark>ecovery</mark> i <mark>llust</mark> r <mark>ation: w.o</mark> V <mark>ision (top) and VIGOR (bottom), progressing from left</mark> to <mark>right.</mark> 

<mark>both metrics. We</mark> h <mark>ypothesize that avoiding</mark> r <mark>econstruction</mark> of a <mark>separate</mark> te <mark>rrain</mark> l <mark>atent helps VIGOR maintain</mark> r <mark>ecovery</mark> on unf <mark>amili</mark> ar te <mark>rrain.</mark> 

**<mark>Demonstration Scaling.</mark>** <mark>We compare</mark> v <mark>isual students</mark> s <mark>upervised</mark> by <mark>teachers trained with one, four,</mark> or <mark>the full demonstration set. Evaluation uses identical held-out starts across four fall</mark> d <mark>irections and the tested</mark> te <mark>rrains. The gain from one</mark> to <mark>four demonstrations (Fig.</mark> 6) <mark>suggests that complementary</mark> r <mark>ecovery patterns broaden the student’s coverage.</mark> 

**<mark>Safety and Recovery Quality.</mark>** <mark>We compare the teacher, VIGOR, and the blind student from matched</mark> in <mark>itial states</mark> un- <mark>der both tasks.</mark> T <mark>able VI suggests that</mark> v <mark>ision supports more controlled</mark> r <mark>ecovery:</mark> i <mark>mproved</mark> reliability is a <mark>ccompanied</mark> by <mark>lower contact forces, less drift, and closer motion tracking. The</mark> r <mark>eduction</mark> in <mark>contact peaks</mark> is <mark>more pronounced than the change</mark> in <mark>PIF, highlighting the bene</mark> fit of v <mark>ision for controlling robot–</mark> te <mark>rrain loading. The teacher’s stronger</mark> reliability <mark>and tracking</mark> ind <mark>icate further room for</mark> i <mark>mprovement</mark> in <mark>dist</mark> ill <mark>ation. Fig.</mark> 7 <mark>shows recorded</mark> r <mark>ecovery</mark> s <mark>equences for the</mark> v <mark>isual and blind students.</mark> 

AZULAY _et al._ : UNIFIED PERCEPTIVE FALL SAFETY FOR HUMANOIDS 

7 


Fig. 8. <mark>Real-world</mark> r <mark>ecovery</mark> s <mark>equences from the project teaser: (A)</mark> diag <mark>onal stairs fall, (B) fall</mark> t <mark>oward stairs, (C) stand-</mark> up <mark>with raised legs, and stand-</mark> up <mark>across</mark> a <mark>gap from (D) face-down and (E) face-</mark> up <mark>conf</mark> igur <mark>ations. Four</mark> s <mark>elected frames per</mark> e <mark>xample show the starting pose</mark> or <mark>fall, contact transitions, and</mark> r <mark>ecovery from left</mark> to <mark>right;</mark> i <mark>nsets show synchronized depth.</mark> 

||SAFETY<br>|TAB<br>AND<br>RE<br>C|LE VI<br>OV<br>ERY<br>QU|AL<br>ITY.||
|---|---|---|---|---|---|
|**Method**|PIF_↓_|_F_c_↓_<br>(kN)|FR_↓_<br>(%)|Drift_↓_<br>(m)|MPJPE_↓_<br>(cm)|
|w.o Vision|44.4(_±_7.7)|3.3(_±_1.1|) 22.1(_±_3.0)|0.9(_±_0.6)|21.5(_±_6.6)|
|VIGOR|40.6(_±_7.6)|2.0(_±_1.0|) 7.3(_±_1.6)|0.5(_±_0.5)|17.3(_±_5.9)|
|Teacher|39.3(_±_6.0)|1.8(_±_1.1|) 3.1(_±_2.5)|0.5(_±_0.4)|11.5(_±_4.8)|


Fig. 9. Real-world recovery performance across surfaces and initial configurations. Top: stand-up. Bottom: fall recovery. Bars show success over 5 trials; denotes successful recoveries with unsafe upper-body contact. 

## _D. Real-World Experiments_ 

We evaluate VIGOR on a Unitree G1 without task-specific tuning or parameter changes. Each setting is tested for 5 trials under the _Stand-Up_ and _Fall-Recovery_ regimes, <mark>with represen-</mark> t <mark>ative</mark> s <mark>equences shown</mark> in <mark>Fig.</mark> 8. <mark>See the supplementary video for the</mark> s <mark>etups.</mark> 

**Stand-Up.** We test stand-up on flat ground, stones, and a box obstacle. Flat-ground trials include prone, supine, and sideways initializations; stones include prone and supine initializations; and box trials include seated and torso-on-box configurations. In all cases, joint configurations are _randomized_ , and the policy must recover to an upright stance. 

**Fall-Recovery.** We test fall recovery on flat ground, a raised platform, and stairs. Flat-ground trials use backward, forward, and sideways pushes; platform trials push the robot forward off the edge; and stair trials use direct and diagonal pushes toward the stairs. To ensure a genuine dynamic fall, the policy is initially disabled and activated only after the projected gravity vector indicates that the robot has reached a predefined fall angle (20<sup>_◦_</sup> ). <mark>This</mark> d <mark>elayed</mark> activ <mark>ation evaluates miti</mark> g <mark>ation and</mark> r <mark>ecovery</mark> after <mark>destabilization.</mark> 

**Results.** Fig. 9 reports real-world performance on a Unitree G1 under _Stand-Up_ and _Fall-Recovery_ , grouped by terrain and initialization or disturbance type. <mark>Fig.</mark> 8 <mark>shows corr</mark> e- <mark>sponding</mark> r <mark>ecovery</mark> b <mark>ehaviors.</mark> _Unitree_ controller only succeeds for face-up flat-ground stand-up, so we omit it from further evaluation. <mark>For stand-up, both policies achieve high</mark> r <mark>ecovery rates across</mark> in <mark>itial poses</mark> on <mark>f</mark> l <mark>at</mark> te <mark>rrain.</mark> As terrain complexity increases, especially on stones and box obstacles, the benefit of visual grounding becomes clearer: VIGOR maintains higher success under uneven contacts, indicating more reliable terrain-aware stabilization. <mark>During fall</mark> r <mark>ecovery, both policies</mark> r <mark>ecover</mark> rel <mark>iably from forward and backward pushes</mark> on <mark>f</mark> l <mark>at</mark> te <mark>rrain.</mark> Under more challenging disturbances, including sideways pushes and stair interactions, VIGOR 

IEEE ROBOTICS AND AUTOMATION LETTERS. PREPRINT VERSION. ACCEPTED OCTOBER, 2026 

8 

<mark>achieves more</mark> r <mark>ecoveries without</mark> u <mark>nsafe</mark> u <mark>pper-body contact,</mark> with the strongest gains in settings that require terrain-aware reactions such as diagonal stair pushes. <mark>These</mark> r <mark>esults show why</mark> r <mark>ecovery success alone</mark> is i <mark>nsuffcient</mark> to <mark>chara</mark> cte <mark>rize fall safety.</mark> In <mark>sideways falls and</mark> diag <mark>onal stair pushes, the blind policy sometimes reaches standing</mark> d <mark>espite</mark> u <mark>nsafe</mark> u <mark>pper-body contacts, whereas VIGOR achieves more</mark> r <mark>ecoveries without these contacts. The</mark> r <mark>ecovery</mark> s <mark>equences</mark> in <mark>Fig.</mark> 8 i <mark>llustrate how depth helps the policy identify nearby support and</mark> o <mark>bstacles</mark> b <mark>efore</mark> i <mark>mpact and</mark> coord <mark>inate contacts during</mark> r <mark>ecovery.</mark> 

## V. CONCLUSION 

We present VIGOR, a unified framework for humanoid fall safety that integrates fall mitigation and recovery in a single vision-conditioned policy. By factorizing data into sparse human motion priors and independently varying terrain, and by representing recovery goals through a compact goal-incontext latent, VIGOR enables RL to resolve contact timing and terrain-dependent execution without dense demonstrations. A privileged teacher learns terrain-aware recovery from sparse keyframes and terrain access, and is distilled into a deployable student operating from egocentric perception. Simulation and real-world results demonstrate robust recovery across diverse terrains and initial conditions, validating structured teacherstudent learning as a practical path to zero-shot sim-to-real humanoid fall safety. F <mark>uture work will</mark> e <mark>xplore</mark> int <mark>egration with</mark> ong <mark>oing tasks, such</mark> as loc <mark>omotion,</mark> to <mark>support task cont</mark> inu <mark>ation</mark> after r <mark>ecovery.</mark> 

## REFERENCES 

- [1] J. Englsberger, T. Koolen, S. Bertrand, J. Pratt, C. Ott, and A. AlbuSch¨affer, “Trajectory generation for continuous leg forces during double support and heel-to-toe shift based on divergent component of motion,” in _2014 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, 2014, pp. 4022–4029. 

- [2] D. Ferigo, R. Camoriano, P. M. Viceconte, D. Calandriello, S. Traversaro, L. Rosasco, and D. Pucci, “On the emergence of whole-body strategies from humanoid robot push-recovery learning,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 4, pp. 8561–8568, 2021. 

- [3] D. Luo, Y. Ding, Z. Cao, and X. Wu, “A multi-stage approach for efficiently learning humanoid robot stand-up behavior,” in _2014 IEEE international conference on mechatronics and automation_ . IEEE, 2014, pp. 884–889. 

- [4] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning Humanoid Standing-up Control across Diverse Postures,” in _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

- [5] F. Zargarbashi, J. Cheng, D. Kang, R. Sumner, and S. Coros, “RobotKeyframing: Learning Locomotion with High-Level Objectives via Mixture of Dense and Sparse Rewards,” in _8th Annual Conference on Robot Learning_ , 2024. 

   - [11] C. Gaspard, M. Duclusaud, G. Passault, M. Daniel, and O. Ly, “Frasa: An end-to-end reinforcement learning agent for fall recovery and stand up of humanoid robots,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 15 994–16 000. 

   - [12] Z. Xu, Y. Li, K.-y. Lin, and S. X. Yu, “Unified humanoid fall-safety policy from a few demonstrations,” _arXiv preprint arXiv:2511.07407_ , 2025. 

   - [13] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid Parkour Learning,” in _8th Annual Conference on Robot Learning_ , 2024. 

   - [14] Z. Fu, X. Cheng, and D. Pathak, “Deep Whole-Body Control: Learning a Unified Policy for Manipulation and Locomotion,” in _6th Annual Conference on Robot Learning_ , 2022. 

   - [15] M. Liu, Z. Chen, X. Cheng, Y. Ji, R.-Z. Qiu, R. Yang, and X. Wang, “Visual Whole-Body Control for Legged Loco-Manipulation,” in _8th Annual Conference on Robot Learning_ , 2024. 

   - [16] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu, “Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation,” _arXiv preprint arXiv:2509.20322_ , 2025. 

   - [17] A. Loquercio, A. Kumar, and J. Malik, “Learning visual locomotion with cross-modal supervision,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 7295–7302. 

   - [18] K.-Y. Lin and S. X. Yu, “Let humanoids hike! integrative skill development on complex trails,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 22 498–22 507. 

   - [19] H. Duan, B. Pandit, M. S. Gadde, B. J. van Marum, J. Dao, C. Kim, and A. Fern, “Learning Vision-Based Bipedal Locomotion for Challenging Terrain,” _arXiv preprint arXiv:2309.14594_ , 2023. 

   - [20] Z. Luo, C. Tessler, T. Lin, Y. Yuan, T. He, W. Xiao, Y. Guo, G. Chechik, K. Kitani, L. Fan _et al._ , “Emergent active perception and dexterity of simulated humanoids from visual reinforcement learning,” _arXiv preprint arXiv:2505.12278_ , 2025. 

   - [21] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

   - [22] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

   - [23] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

   - [24] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual imitation enables contextual humanoid control,” in _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

   - [25] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

   - [26] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

   - [27] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ . JMLR Workshop and Conference Proceedings, 2011, pp. 627–635. 

   - [28] O. Azulay, D. M. Ramesh, N. Curtis, and A. Sintov, “Visuotactilebased learning for insertion with compliant hands,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 4, pp. 4053–4060, 2025. 

- [6] K. Wen, C. Li, J. He, and M. Hutter, “Constrained Style Learning from Imperfect Demonstrations under Task Optimality,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [7] Z. Zhang, C. Li, T. Miki, and M. Hutter, “Motion Priors Reimagined: Adapting Flat-Terrain Skills for Complex Quadruped Mobility,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [8] V. C. Kumar, S. Ha, and C. K. Liu, “Learning a unified control policy for safe falling,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2017, pp. 3940–3947. 

- [9] J. St¨uckler, J. Schwenk, and S. Behnke, “Getting back on two feet: Reliable standing-up routines for a humanoid robot.” in _IAS_ , 2006, pp. 676–685. 

- [10] X. He, R. Dong, Z. Chen, and S. Gupta, “Learning Getting-Up Policies for Real-World Humanoid Robots,” in _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. 

