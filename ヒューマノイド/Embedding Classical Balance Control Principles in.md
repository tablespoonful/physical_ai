---
title: "Embedding Classical Balance Control Principles in Reinforcement Learning for Humanoid Recovery"
date: "2026-03-09"
authors: "Nehar Poddar; Stephen McCrory; Luigi Penco; Geoffrey Clark; Hakki Erhan Svil; Robert Griffin"
url: https://arxiv.org/abs/2603.08619
pdf: https://arxiv.org/pdf/2603.08619
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.08619)** / [論文ページ](https://arxiv.org/abs/2603.08619)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Embedding Classical Balance Control Principles in Reinforcement Learning for Humanoid Recovery** 

Nehar Poddar<sup>1</sup><sup>_,_2</sup> , Stephen McCrory<sup>1</sup><sup>_,_2</sup> , Luigi Penco<sup>1</sup> , Geoffrey Clark<sup>1</sup><sup>_,_2</sup> , Hakki Erhan Sevil<sup>2</sup> , Robert Griffin<sup>1</sup><sup>_,_2</sup> 

**_Abstract_ — Humanoid robots remain vulnerable to falls and unrecoverable failure states, limiting their practical utility in unstructured environments. While reinforcement learning has demonstrated stand-up behaviors, existing approaches treat recovery as a pure task-reward problem without an explicit representation of the balance state. We present a unified RL policy that addresses this limitation by embedding classical balance metrics: capture point, center-of-mass state, and centroidal momentum, as privileged critic inputs and shaping rewards directly around these quantities during training, while the actor relies solely on proprioception for zero-shot hardware transfer. Without reference trajectories or scripted contacts, a single policy spans the full recovery spectrum: ankle and hip strategies for small disturbances, corrective stepping under large pushes, and compliant falling with multi-contact stand-up using the hands, elbows, and knees. Trained on the Unitree H1-2 in Isaac Lab, the policy achieves a** 93 _._ 4% **recovery rate across randomized initial poses and unscripted fall configurations. An ablation study shows that removing the balance-informed structure causes stand-up learning to fail entirely, confirming that these metrics provide a meaningful learning signal rather than incidental structure. Sim-to-sim transfer to MuJoCo and preliminary hardware experiments further demonstrate crossenvironment generalization. These results show that embedding interpretable balance structure into the learning framework substantially reduces time spent in failure states and broadens the envelope of autonomous recovery.** 

## I. INTRODUCTION 

Humanoid robots have demonstrated increasingly capable locomotion and manipulation in controlled environments [1– 3]. However, reliable recovery from falls and large disturbances remains an open challenge. Falls interrupt operation, risk hardware damage, and often require manual intervention, limiting deployment beyond laboratory settings. For humanoid platforms to operate autonomously in unstructured environments, fall recovery must be treated as a core capability rather than an exceptional case. 

Fall recovery is contact-rich, non-periodic, and highly state-dependent. Depending on the disturbance, a robot must decide in real time whether to resist using ankle or hip strategies, take a stabilizing step, initiate a controlled descent, or execute a multi-contact stand-up using the hands, elbows, and knees yet no existing approach addresses all of these behaviors within a single policy. Prior works tackle isolated subproblems, including predefined stand-up sequences [4, 5], 

> 1 Florida Institute for Human and Machine Cognition, Pensacola, FL, USA. 

> 2 University of West Florida, Pensacola, FL, USA. Email: npoddar@ihmc.org 


Fig. 1. Stand-up sequence on the Unitree H1-2 hardware. Frames 1–8 show recovery from a fallen configuration (1) to upright stance (8). 

scripted contact schedules [6], and reference motion tracking [7]. Although effective within their respective design envelopes, these approaches require significant engineering effort and generalize poorly to unplanned contact configurations or disturbances of unexpected magnitude. 

Reinforcement learning offers a path toward more general recovery [8–10], and recent work has produced increasingly capable whole-body controllers across a range of disturbance conditions. However, most RL-based recovery formulations treat stability as an implicit consequence of the task reward, leaving the policy without an explicit representation of how close the robot is to an unrecoverable state. Without balanceaware signals, the critic must infer recoverability from reward history alone, a representation that may suffice under narrow task conditions but leaves open the question of generalization across a broader disturbance spectrum. 

Classical humanoid balance analysis already provides this information in compact, interpretable form. Capture point [11, 12], center of mass (CoM) state, and centroidal momentum together characterize whether a given configuration is recoverable under feasible contact changes and are wellestablished tools in model-based control [13]. These quantities are readily available in simulation and can be estimated on hardware, yet they are rarely used to directly structure learned recovery policies. We argue that this represents an underexplored opportunity: embedding balance-aware structure may improve both the efficiency and generality of RL based recovery without sacrificing the adaptability of learned controllers. 

We address this by incorporating classical balance metrics: 

capture point, CoM state, and centroidal momentum, directly into both the reward structure and an asymmetric critic [14]. The critic receives these quantities as privileged inputs during training [15], while the actor relies solely on proprioception for zero-shot hardware transfer. Without reference trajectories or scripted contacts, a single policy trained in Isaac Lab [16] on the Unitree H1-2 learns ankle and hip stabilization, stepping recovery, compliant falling, and multi-contact standup from arbitrary initial configurations. 

The main contributions of this work are: 

- A balance-informed RL formulation embedding capture point, CoM state, and centroidal momentum as privileged critic inputs and reward terms, providing explicit recoverability structure without reference trajectories or scripted contacts. 

- A single unified policy on the Unitree H1-2 spanning the full recovery spectrum: ankle and hip strategies, stepping recovery, compliant falling, and multi-contact stand-up through hands, elbows, and knees [6, 17], trained via a curriculum that explicitly cycles fallinduction and stand-up to cover the complete recovery sequence. 

- An ablation study indicating that, within this formulation, balance-informed structure is critical for stand-up discovery: removing privileged critic inputs and capturepoint rewards results in failure to leave the ground, with stuck-low termination rate rising from 0.067 to 1.0. 

- Zero-shot hardware deployment on the Unitree H1-2 across 10 trials from diverse configurations, and sim-tosim transfer to MuJoCo, validating cross-environment generalization without policy modification. 

## II. RELATED WORK 

## **A) Classical Stability and Reduced-Order Models** 

Early humanoid balance research established analytical criteria linking centroidal motion to contact feasibility. The Zero Moment Point (ZMP) framework provided a practical trajectory feasibility condition under fixed-foot contacts [18], later extended to multi-contact settings through wrenchbased support region analysis [19]. The capture point and divergent component of motion (DCM) relate CoM position and velocity to stepping requirements, unifying ankle, hip, and stepping strategies within a common framework [11, 12, 17, 20]. Reaction-mass and flywheel models extend these ideas to centroidal angular momentum, capturing upperbody effects [21, 22]. Centroidal dynamics formulations then bridge reduced-order reasoning and full multi-contact wholebody behavior [23, 24]. While these methods yield interpretable stability criteria effective for structured locomotion, they rely on simplifying assumptions that become strained in the non-periodic, contact-rich scenarios characterizing postdisturbance recovery. Our work draws on these classical metrics not as controllers, but as structured signals to guide learned value estimation. 

TABLE I 

COMPARISON OF REPRESENTATIVE RL-BASED HUMANOID RECOVERY APPROACHES. 

|**Method**<br>**HoF**<br>**Fal**|**l**<br>**MP**|**MT**|**Ref**|**EB**|**AC**|
|---|---|---|---|---|---|
|FRASA [8]<br>✗<br>✓|✗|✗|✗|✗|✗|
|HumanUP [7]<br>✓<br>✗|✓|✓|✓|✗|✓|
|HoST [5]<br>✓<br>✗|✓|✓|✗|✗|✗|
|HiFAR [10]<br>✓<br>✓|✓|✓|✗|✗|✗|
|**Ours**<br>✓<br>✓|✓|✓|✗|✓|✓|
|**HoF**: high-DOF humanoid;|**Fall**: fall|recovery;|**MP**: mu|lti-pose||
|initialization; **MT**: multi-terrain; <br>balance metrics;|**Ref**: uses <br> **AC**: asy|motion r<br>mmetric cr|eference; <br>itic.|**EB**: ex|plicit|


## **B) Optimization and Multi-Contact Planning** 

Optimization-based approaches formulate balance and recovery as constrained trajectory optimization problems over contact forces, centroidal dynamics, and joint motion. Whole-body trajectory optimization enables dynamically consistent multi-contact behavior [23], while direct-contact formulations such as DirCon compute contact-consistent trajectories through hybrid dynamics optimization [25].Contactexplicit optimal control frameworks such as Crocoddyl achieve real-time feasible motion plans through efficient differential dynamic programming [26]. Model predictive control extends these ideas to online adaptation, with contactimplicit variants discovering contact transitions via complementarity constraints [27], and reduced-order MPC schemes leveraging simplified models for push recovery and bracing [28–30]. Contact-Invariant Optimization treats contact activation as a decision variable to discover feasible contact phases [31], while learning-based feasibility predictors estimate whether candidate configurations are dynamically realizable [32]. Despite their expressiveness and physical grounding, these methods remain computationally demanding and challenging to apply in real time to the non-periodic, unplanned scenarios characterizing fall and recovery. 

## **C) Reinforcement Learning for Humanoid Recovery** 

Reinforcement learning has been applied to fall detection, recovery control, and end-to-end stand-up using posetracking or task-based rewards [8, 9]. Curriculum-based frameworks address high-dynamics recovery through staged training [10], and reward-shaping strategies have been explored to improve recovery from fallen states [33]. Several getting-up methods rely on motion references, keyframes, or canonical poses [7, 34], while others train reference-free, posture-spanning policies in which multi-contact strategies emerge implicitly [5]. Beyond dedicated recovery controllers, recent RL methods have produced versatile humanoid behaviors including agile locomotion, running, and parkour [3, 35, 36], with whole-body controllers leveraging reference motions, symmetry priors, or shared architectures to generalize across behaviors [37, 33, 38, 39]. 

In most of these formulations, balance behavior arises as a consequence of task or survival objectives rather than from explicitly structured stability criteria, as summarized in Table I. Our work is reference-free and does not rely on 

motion clips, keyframes, or canonical poses; instead, it incorporates CoM state, capture point, and centroidal momentum directly into the reward structure and an asymmetric critic, connecting classical stability analysis with learned recovery without predefined contact schedules. 

## III. METHODOLOGY 

## **A) Problem Formulation** 

We formulate humanoid fall recovery as a continuousstate, continuous-action Markov Decision Process (MDP) defined by ( _S , A , P, R_ ). A stochastic policy _πθ_ ( **a** _t |_ **o** _t_ ), parameterized by learnable weights _θ_ , maps proprioceptive observations **o** _t_ to joint-level actions **a** _t_ , with the objective of maximizing the expected discounted return: 


where _rt_ = _R_ ( **s** _t ,_ **a** _t_ ) is the per-step reward, _γ ∈_ (0 _,_ 1) is the discount factor, and _T_ is the episode horizon. The full system state **s** _t_ is available during training, while the deployed policy receives only partial observations **o** _t_ corresponding to onboard proprioceptive sensing. Actions are continuous joint-level position commands. 

## **B) Learning Architecture** 

We employ an on-policy actor–critic framework based on Proximal Policy Optimization (PPO) [40]. The actor outputs relative joint position targets for all actuated degrees of freedom of the Unitree H1-2, tracked by low-level PD controllers. The critic estimates the state-value function using privileged information available only during training, following the asymmetric actor–critic design of [14]. 

Both actor and critic are multilayer perceptrons with hidden dimensions [512 _,_ 256 _,_ 128] and ELU activations. The policy is initialized with action noise _σ_ = 1 _._ 0. Training runs for 50,000 iterations with 24 rollout steps per environment per update. PPO hyperparameters are summarized in Table II. Training is conducted in Isaac Lab [37], modeling full-body dynamics, contact, joint limits, and friction. 

TABLE II 

PPO TRAINING HYPERPARAMETERS. 

|**Hyperparameter**|**Value**|
|---|---|
|Iterations|50,000|
|PPO clip _ε_<br>|0.2|
|Discount _γ_<br>|0.99|
|GAE _λ_|0.95<br>|
|Learning rate|1_×_10<sup>_−_3</sup>|
|Target KL|0.01|
|Entropy coeff.|0.005|


## **C) Observation Design** 

To support sim-to-real transfer, we decompose the full state **s** _t_ into policy observations **o** _t_ and privileged variables available only to the critic during training. 

## **1) Policy Observations** 

The actor receives only quantities measurable on hardware: 

- Base angular velocity and projected gravity, 

- Relative joint positions and joint velocities, 

- Previous action **a** _t−_ 1. 

Additive uniform noise is applied to **o** _t_ during training to model sensor uncertainty and improve robustness to realworld measurement error. 

## **2) Privileged Critic Observations** 

The critic receives the full actor observation **o** _t_ augmented with simulator-derived quantities **s** _t_<sup>priv</sup> , forming the input ( **o** _t ,_ **s** _t_<sup>priv</sup> ), where **s** _t_<sup>priv</sup> _⊂_ **s** _t_ contains quantities unavailable on hardware: 

- Center-of-mass (CoM) position, velocity, and acceleration, 

- Whole-body linear and angular momentum, 

- Capture point location. 

These quantities characterize the instantaneous balance state of the robot, enabling more accurate value estimation and more stable policy updates during training. While CoM state can in principle be estimated via IMU integration or wholebody state estimators, reliable estimation during contact-rich fall recovery is particularly challenging: drift accumulates rapidly during dynamic motion, and multi-contact estimation requires knowing which contacts to trust during uncontrolled falling. 

## **D) Action Space** 

The action space comprises relative joint position commands for all actuated joints of the H1-2. At each control step, the policy outputs actions **a** _t_ , scaled by 0.3 and executed via low-level PD controllers. To model realistic actuator and communication latencies, a randomized per-episode delay of 10–40 ms is applied to joint commands and held constant within each episode, supporting consistent sim-to-real transfer. 

## **E) Physics-Guided Reward Design** 

We decompose the total reward into three physically motivated groups: 


where _R_<sup>I</sup> enforces vertical recovery, _R_<sup>II</sup> enforces balance and capturability, and _R_<sup>III</sup> provides regularization and motion priors. This grouping mirrors the physical recovery sequence: vertical elevation _→_ dynamic balance _→_ motion refinement. Table III summarizes all symbols and Table IV provides a full decomposition. 

## **1) Group I: Vertical Recovery** 

Group I rewards drive vertical recovery toward a target CoM height _h_<sup>_∗_</sup> : 


Fig. 2. End-to-end pipeline for the Unitree H1-2 stand-up controller: diverse initial pose distribution with upright target (left); Isaac Lab training with PPO, asymmetric critic, and push curriculum; MuJoCo sim-to-sim validation; SCS2 integration with balance visualization; and zero-shot hardware deployment using proprioception only (right). 

TABLE III 

SUMMARY OF SYMBOLS USED IN THE REWARD FORMULATION. 

|**Category**|**Symbol**|**Description**|
|---|---|---|
|State|**s**_t_<br>∆_t_|Robot state at discrete time _t_<br>Control/simulation time step|
|CoM|**p**_c ∈_R<sup>3</sup><br>**p**_c,xy ∈_R<sup>2</sup><br>_hc_<br>_h_<sup>_∗_</sup><br>˙_hc_<br>_eh_|3-D CoM position<br>Horizontal CoM projection<br>Vertical CoM height (_pc,z_)<br>Target upright CoM height<br>Vertical CoM velocity<br>Height error (_hc −h_<sup>_∗_</sup>)|
||_ξ_|Capture point (LIP model)|
|Balance|_g_<br>I[_·_]|Gravitational acceleration<br>Indicator function|
||_C_|Convex hull of active contacts|
|Support|_C_feet<br>_d_CoM|Convex hull of foot contacts<br>Signed distance: CoM projection to _C_|
||_d_CP|Signed distance: CP to _C_feet|
||**p**_ℓ_|Whole-body linear momentum|
|Momentum|**L**<br>**F**net|Whole-body angular momentum<br>Net centroidal force (˙**p**_ℓ/_∆_t_)|
||_τ_net|Net centroidal torque (<sup>˙</sup>**L**_/_∆_t_)|
||_w•_|Group weighting coefficients|
|Prmtr|_α•_|Shaping coefficients|
|aaees|_σ•_<br>_δh_|Gaussian bandwidth parameters<br>Height deadband threshold|


## **a) Height tracking.** 

A dense Gaussian reward centered at _h_<sup>_∗_</sup> provides a smooth gradient throughout the elevation range: 


where _σh_ controls the reward bandwidth. 

## **b) Vertical momentum shaping.** 

_r_ rise rewards upward CoM velocity when the robot is below target height; _r_ fall quadratically penalizes downward velocity to discourage collapse: 


This asymmetric structure rewards rising proportionally to upward velocity while penalizing downward motion quadratically. Neither term activates near _h_<sup>_∗_</sup> , avoiding conflicting incentives during final convergence. 

**c) Stationary stability near target.** 

Once the robot approaches _h_<sup>_∗_</sup> , _r_ stab provides a proximity bonus within tolerance _δh_ while penalizing residual vertical velocity to suppress overshoot: 


The Gaussian in (3) provides a nonzero gradient at all heights below _h_<sup>_∗_</sup> , and _r_ rise encourages upward momentum throughout, giving the policy a continuous learning signal across the full range of initial CoM heights rather than only at discrete canonical poses. 

## **2) Group II: Balance and Capturability** 

Group II rewards enforce static and dynamic stability by embedding capture-point theory directly into the reward structure: 


Capture Point: Balance is assessed using the capture point _ξ_ , derived from the Linear Inverted Pendulum (LIP) model [11], which indicates the location where the robot must step to arrest a fall: 


The signed distances _d_ CoM and _d_ CP measure how far the CoM projection and capture point lie from the boundaries of _C_ and _C_ feet respectively (negative inside, positive outside). 

## **a) Static Stability** 

_r_ CoM rewards configurations in which the CoM projection lies within the support hull _C_ : 


The smooth Gaussian decay encourages stable base maintenance without hard threshold switching. 

**b) Dynamic Capturability** _r_ CP penalizes configurations in which the capture point falls outside the foot support hull _C_ feet, indicating that balance cannot be maintained under the LIP model without a contact change [12]: 


Together, _r_ CoM and _r_ CP couple static and dynamic stability: the former penalizes instantaneous support violations while the latter penalizes momentum states that may lead to future balance loss even when the CoM projection currently lies within the support hull. 

**c) Momentum Regularization** 

_r_ mom penalizes large net centroidal forces and moments to suppress impulsive whole-body reactions: 


Quadratic penalization disproportionately discourages large impulsive reactions relative to small smooth corrections. 

**3) Group III: Regularization and Motion Shaping** Group III introduces hardware safety constraints and physically consistent motion priors: 


Safety terms penalize torque and joint limit violations and rapid action changes, protecting hardware during highforce recovery transitions. The posture term penalizes torso misalignment with gravity, encouraging upright orientation throughout recovery. The contact shaping term applies height-gated rewards for hand and elbow support, promoting appropriate multi-contact transitions during stand-up. The survival term combines an alive bonus with an early termination penalty, encouraging task completion rather than episode length maximization. 

Taken together, Group III terms encourage the detailed recovery sequence: including multi-contact transitions and compliant falling, to emerge from the physics-based objectives in _R_<sup>I</sup> and _R_<sup>II</sup> , without scripted contact schedules or reference trajectories. 

## **F) Curriculum and Training Strategy** 

Training follows a three-stage progressive curriculum designed to encourage broad exploration of recovery strategies, introduce physical realism, and constrain behavior to hardware-safe operating ranges. 

- 1) **Exploration phase.** Joint torque limits are initially set to 10 _×_ hardware specifications, providing sufficient 

TABLE IV 

PHYSICS-GUIDED REWARD DECOMPOSITION. 

|**Group**|**Component**|**Symbol**|**Objective**|
|---|---|---|---|
|_R_<sup>I</sup>|Height tracking<br>Rise shaping|_r_height<br>_r_rise|Reach _h_<sup>_∗_</sup><br>Encourage upward motion|
||Fall penalty<br>Stability band|_r_fall<br>_r_stab|Suppress downward velocity<br>Prevent oscillation|
||CoM support|_r_CoM|Static stability|
|_R_<sup>II</sup>|Capture point|_r_CP|Dynamic capturability|
||Momentum reg.|_r_mom|Smooth centroidal dynamics|
||Safety|_r_torque|Hardware protection|
|_R_<sup>III</sup>|Posture|_r_orient|Upright torso alignment|
||Contact shaping|_r_contact|Multi-contact transitions|
||Survival|_r_alive|Task completion|


actuation authority for the policy to discover diverse recovery strategies, including multi-contact behaviors such as hand-assisted push-ups from the ground. 

- 2) **Difficulty expansion.** External disturbances, randomized initial configurations (standing, squatting, kneeling, sitting, and supine), and domain randomization over physical parameters (mass distribution, friction, inertia, and joint armature) are progressively introduced. Once the robot reaches upright stance, large destabilizing impulses are applied to induce a fall and trigger a full fall-and-recovery cycle, ensuring the policy trains on the complete recovery sequence. 

- 3) **Hardware constraint annealing.** Joint torque and position limits are gradually reduced toward hardwaresafe values (1 _×_ torque, 0 _._ 9 _×_ position limit factor), transitioning the policy from exploratory to deployable behavior. 

Episodes were terminated upon timeout or when unsafe torso–ground contact occurred under high contact force conditions, encouraging recovery while discouraging catastrophic collapse. 

## **G) Domain Randomization and Noise Injection** 

To improve sim-to-real robustness, domain randomization is applied across dynamics, contacts, initialization, observations, and disturbances: 

- **Actuation and joint dynamics:** Stiffness and damping gains scaled by [0 _._ 75 _,_ 1 _._ 25]; joint friction sampled from [0 _._ 5 _,_ 4 _._ 0]; armature scaled by [0 _._ 5 _,_ 1 _._ 6]. 

- **Contact properties:** Static friction _µs ∼_ [0 _._ 3 _,_ 1 _._ 6], dynamic friction _µd ∼_ [0 _._ 3 _,_ 1 _._ 2], restitution _e ∼_ [0 _,_ 0 _._ 2]. 

- **Initialization noise:** Base pose perturbations ∆ _p ∈_ [ _−_ 0 _._ 05 _,_ 0 _._ 05] m, ∆ _r ∈_ [ _−_ 0 _._ 2 _,_ 0 _._ 2] rad; joint offsets ∆ _q ∈_ [ _−_ 0 _._ 1 _,_ 0 _._ 1] rad. 

- **Observation noise:** Additive uniform noise on policy inputs: base angular velocity _ωb ±_ 0 _._ 5 rad/s, projected gravity _±_ 0 _._ 15, joint positions _q±_ 0 _._ 1 rad, joint velocities _q_ ˙ _±_ 0 _._ 5 rad/s. 

- **External disturbances:** Random torso impulses of 50– 300 N over 0.1–0.2 s for push recovery training. Once upright stance is reached, large destabilizing impulses 


Fig. 3. Capture-point evolution during push recovery. The blue marker denotes _ξ_ and polygons represent active foot support regions. The policy progressively drives _ξ_ back inside the support hull through ankle, hip, and stepping responses. 

are applied to induce a fall and trigger a full fall-andrecovery cycle. 

Rigid-body inertias are randomized without recomputing a dynamically consistent model, requiring the policy to infer balance-relevant structure directly from observed state trajectories rather than relying on accurate internal dynamics. 

## IV. EXPERIMENTS AND RESULTS 

## **A) Simulation** 

All policies were trained and evaluated in Isaac Lab using the Unitree H1-2 model, with additional validation in MuJoCo to assess cross-simulator generalization. Under nominal conditions, the policy maintained stable standing for the full episode horizon in both environments. 

## **1) Recovery from Diverse Configurations** 

The policy successfully recovered to upright stance from a variety of initial poses, including squatting, kneeling, sitting, and supine, without relying on predefined trajectories. Across 10,000 trials, it achieved a 93.4% recovery success rate with a mean recovery time of 5 s. Failures primarily occurred when the robot became trapped in local contact configurations from which upright recovery could not be completed within the episode horizon. 

## **2) Disturbance Rejection** 

External perturbations of increasing magnitude were applied during standing. Small pushes (50–100 N) were absorbed through ankle strategies; moderate pushes (100– 200 N) induced hip-based adjustments; and larger pushes (200–300 N) triggered stepping responses. This graduated hierarchy is consistent with the balance structure embedded in the reward and with classical push-recovery analysis [17]. For disturbances _≥_ 300 N, the robot transitioned to multicontact recovery, bracing with the hands before returning to upright stance. Fig. 3 shows the capture point evolution during a representative push recovery trial. The policy drives _ξ_ back inside the foot support hull through the ankle, hip, and 

stepping sequence, consistent with the capturability reward structure in Eqs. (9)–(10). 

## **3) Sim-to-Sim Validation** 

To assess cross-simulator generalization, we evaluated the policy in MuJoCo across five initial configurations (standing, squatting, kneeling, supine, and sitting) under applied forces from 0–500 N in four lateral directions. MuJoCo’s more conservative contact model, with stricter friction and damping defaults than Isaac Lab, we observe, more closely approximates physical hardware dynamics, providing a stronger test of transferability than in-distribution Isaac Lab evaluation alone. 

A trial is counted as successful only if the CoM exceeds 0.85 m and remains there for at least 1 s with vertical velocity below 0.1 m/s and torso tilt within 72<sup>_◦_</sup> of vertical, ruling out momentary bounces or transient uprighting. Without perturbation, the policy achieves 100% recovery from all poses. Under perturbation, robustness degrades gracefully: standing and squatting maintain recovery rates above 50% at 200 N, while supine and sitting drop below 25% beyond 100 N, consistent with the greater centroidal momentum that must be regulated from near-floor orientations. Recovery time increases with force magnitude, reaching up to 9 s for supine trials at high forces. 

Push application height has a consistent effect: low pushes ( _−_ 0.2 m) yield the highest recovery rates while high pushes (0.6 m) yield the lowest. A force applied above the CoM induces larger whole-body angular momentum, driving greater displacement of _ξ_ outside the support polygon, the precise failure mode penalised by Eq. (10). Results are summarized in Fig. 4. 

## **B) Ablation Study** 

To evaluate the contribution of our key design choices, we trained a reduced policy without privileged critic inputs (CoM dynamics, capture point, centroidal momentum), capture-point reward terms, or progressive curriculum, with all other hyperparameters and reward terms held identical. 

Results are shown in Table V. The reduced policy failed to learn stand-up behavior: episodes terminated exclusively via the stuck-low condition (triggered when CoM height shows no increase for 2 consecutive seconds) at a rate of 1.0, compared to 0.067 in the full policy, indicating the robot never left the ground. Mean reward fell from +379.2 to _−_ 115.3 and all recovery metrics collapsed. These results suggest that, within this training setup, balance-informed structure is necessary for the policy to discover multi-contact stand-up behavior. We note that this is a single combined ablation; disentangling the individual contributions of privileged critic inputs, capture-point rewards, and curriculum is left for future work. 

## **C) Hardware Deployment** 

Policies trained in simulation were exported as ONNX networks and deployed on the physical Unitree H1-2 using our software stack, integrated via the OpenCV DNN Java 


Fig. 4. MuJoCo sim-to-sim recovery analysis across five initial poses and forces 0–500 N. Success requires the CoM to exceed 0.85 m and remain stable for _≥_ 1 s. (A) Baseline recovery without push. (B–C) Recovery rate degrades gracefully with force; standing and squatting are most robust. (D) Recovery time increases with perturbation magnitude. (E–F) Directional and height sensitivity show consistent trends across poses. 

TABLE V 

ABLATION AT CONVERGENCE: FULL POLICY VS. REDUCED VARIANT (NO PRIVILEGED CRITIC, NO CAPTURE-POINT REWARDS, NO CURRICULUM). 

|**Metric**|**Full**|**Reduced**|
|---|---|---|
|**Performance**|||
|Mean reward|+**379**_._**2**|_−_115_._3|
|Episode length (steps)|**975**|219|
|**Recovery**|||
|CoM height maintenance|**13**_._**23**|0_._17|
|Progressive recovery|**3**_._**78**|0_._41|
|Hand-support recovery|**1**_._**80**|0_._11|
|Feet under CoM|**1**_._**58**|0_._00|
|**Termination**|||
|Timeout|**0**_._**934**|0_._000|
|Stuck low|0_._067|**1**_._**000**|


API at 50 Hz. The joint-level control law was 

## _τ_ = _kp_ ( _q_ ref _− q_ ) _− kd_ ˙ _q,_ 

where _q_ ref is the policy output and _q_ , _q_ ˙ are measured joint position and velocity. No modifications were made to the policy or control structure at deployment. 

Across 10 trials initialized from supine, seated, kneeling, and crouched configurations, the robot successfully achieved upright recovery in all 10 attempts with no parameter tuning between simulation and hardware. In 3 trials, transient high- 

frequency joint oscillations were observed following recovery, prompting conservative safety intervention. We attribute this behavior to residual sim-to-real mismatch in damping characteristics and are addressing it through improved actionsmoothing during training. 

During disturbance trials, the robot successfully rejected manual pushes and recovered balance. Observable increases in ankle and hip motor torques following perturbations were consistent with the ankle and hip stabilization strategies learned in simulation, providing qualitative evidence that the balance hierarchy transfers to hardware. 

## V. CONCLUSION AND FUTURE WORK 

We presented a balance-informed reinforcement learning framework for humanoid fall recovery that incorporates classical stability metrics: capture point, CoM state, and wholebody momentum, as privileged critic inputs and reward terms. Rather than enforcing predefined contact sequences, this structure gives the critic an explicit representation of recoverability, enabling the actor to decide when to resist a disturbance, when to step, and when to engage multi-contact support. 

Simulation results demonstrate a 93 _._ 4% recovery rate across diverse initial configurations, while an ablation without balance-informed structure fails entirely to learn standup behavior. These results suggest that the embedded metrics 

provide a meaningful learning signal rather than an incidental cue. A single policy spans the full recovery spectrum: ankle and hip strategies, stepping recovery, compliant falling, and hand-assisted stand-up, all achieved without reference trajectories or scripted contact schedules. Zero-shot hardware deployment on the Unitree H1-2 successfully recovers from diverse configurations across 10 trials, providing initial validation that the learned balance structure transfers to real hardware. 

These findings highlight a broader insight: classical balance metrics offer a compact, transferable representation for contact-rich humanoid control that complements purely task-driven reward design. Whether this structure generalizes beyond fall recovery: to manipulation under external loads or locomotion over complex terrain, remains an open question. In particular, maintaining capturability and regulating momentum may serve as prerequisites for robust manipulation, allowing a robot to respond to externally applied loads without explicit payload estimation, potentially simplifying downstream control. 

Future work will explore perception-driven contact selection in cluttered environments, multi-surface recovery, integration with long-horizon locomotion and manipulation tasks, and tighter coupling between balance-aware control and task-level planning. Extending to non-planar surfaces is a natural next step; however, the convex hull support polygon metric assumes coplanar contacts, and replacing it with a more general criterion, such as wrench-space feasibility over non-coplanar contact sets, would be necessary. By using a planar segmentation representation of the environment, the policy could infer contact normals and select contacts within a continuous action space. 

## REFERENCES 

- [1] I. Radosavovic, _et al._ , “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, 2024. 

- [2] T. Haarnoja, _et al._ , “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, 2024. 

- [3] Z. Li, _et al._ , “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _International Journal of Robotics Research_ , vol. 44, 2025. 

- [4] J. Stückler, J. Schwenk, and S. Behnke, “Getting back on two feet: Reliable standing-up routines for a humanoid robot,” in _International Conference on Intelligent Autonomous Systems_ , 2006. 

- [5] T. Huang, _et al._ , “Learning humanoid standing-up control across diverse postures,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [6] C. Zhang, _et al._ , “WoCoCo: Learning whole-body humanoid control with sequential contacts,” in _Conference on Robot Learning (CoRL)_ , 2024. 

- [7] X. He, _et al._ , “Learning getting-up policies for real-world humanoid robots,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [8] C. Gaspard, _et al._ , “Frasa: An end-to-end reinforcement learning agent for fall recovery and stand up of humanoid robots,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [9] C. Yang, _et al._ , “Learning complex motor skills for legged robot fall recovery,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, 2023. 

- [10] P. Chen, _et al._ , “Hifar: Multi-stage curriculum learning for highdynamics humanoid fall recovery,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2025. 

- [11] J. Pratt, _et al._ , “Capture point: A step toward humanoid push recovery,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2006. 

- [12] T. Koolen, _et al._ , “Capturability-based analysis and control of legged locomotion, part 1: Theory and application to three simple gait 

models,” _International Journal of Robotics Research_ , vol. 31, no. 9, 2012. 

- [13] J. Pratt, _et al._ , “Capturability-based analysis and control of legged locomotion, part 2: Application to m2v2, a lower-body humanoid,” _International Journal of Robotics Research_ , vol. 31, no. 10, 2012. 

- [14] L. Pinto, _et al._ , “Asymmetric actor critic for image-based robot learning,” in _Robotics: Science and Systems (RSS)_ , 2018. 

- [15] A. Kumar, _et al._ , “RMA: Rapid motor adaptation for legged robots,” in _Robotics: Science and Systems (RSS)_ , 2021. 

- [16] M. Mittal, _et al._ , “Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning,” _arXiv preprint arXiv:2511.04831_ , 2025. 

- [17] A. Herzog, _et al._ , “Momentum control with hierarchical inverse dynamics on a torque-controlled humanoid,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2016. 

- [18] M. Vukobratovic and B. Stepanenko, “Contribution to the synthesis of biped gait,” _RAIRO Automatique_ , 1972. 

- [19] T. Bretl and S. Lall, “Testing static equilibrium for legged robots,” _IEEE Transactions on Robotics_ , 2008. 

- [20] A. L. Hof, “Condition for dynamic stability,” _Journal of Biomechanics_ , vol. 38, no. 1, 2005. 

- [21] S.-H. Lee and A. Goswami, “A momentum-based balance controller for humanoid robots on non-level and non-stationary ground,” _Autonomous Robots_ , vol. 33, no. 4, 2012. 

- [22] Y. Gong and J. Grizzle, “Angular momentum about the contact point for control of bipedal locomotion: Validation in a lip-based controller,” _arXiv preprint arXiv:2008.10763_ , 2020. 

- [23] H. Dai, A. Valenzuela, and R. Tedrake, “Whole-body motion planning with centroidal dynamics and full kinematics,” in _IEEE-RAS International Conference on Humanoid Robots_ , 2014. 

- [24] L. Sentis, J. Park, and O. Khatib, “Compliant control of multicontact and center-of-mass behaviors in humanoid robots,” _IEEE Transactions on Robotics_ , vol. 26, no. 3, 2010. 

- [25] M. Posa, M. Tobenkin, and R. Tedrake, “Optimization and stabilization of trajectories for constrained dynamical systems,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2016. 

- [26] C. Mastalli, _et al._ , “Crocoddyl: An efficient and versatile framework for multi-contact optimal control,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2020. 

- [27] S. Le Cleac’h _et al._ , “Fast contact-implicit model-predictive control,” in _IEEE Robotics and Automation Letters_ , 2020. 

- [28] L. Yang, _et al._ , “Bracing for impact: Robust humanoid push recovery with reduced order models,” _IEEE Transactions on Robotics_ , 2020. 

- [29] M.-J. Kim, _et al._ , “A model predictive capture point control framework for robust humanoid balancing via ankle, hip, and stepping strategies,” _IEEE Transactions on Robotics_ , 2025. 

- [30] W. Zuo, _et al._ , “Whole-body dynamics for humanoid robot fall protection trajectory generation with wall support,” _Biomimetics_ , vol. 9, no. 4, 2024. 

- [31] I. Mordatch, E. Todorov, and Z. Popovic, “Discovery of complex behaviors through contact-invariant optimization,” _ACM Transactions on Graphics_ , vol. 31, no. 4, 2012. 

- [32] J. Carpentier, R. Budhiraja, and N. Mansard, “Learning feasibility constraints for multicontact locomotion of legged robots,” in _Robotics: Science and Systems (RSS)_ , 2017. 

- [33] B. Deng, _et al._ , “Learning to recover: Dynamic reward shaping with wheel-leg coordination for fallen robots,” _arXiv preprint arXiv:2506.05516_ , 2025. 

- [34] Z. Xu, _et al._ , “Unified humanoid fall-safety policy from a few demonstrations,” _arXiv preprint arXiv:2511.07407_ , 2025. 

- [35] B. van Marum, _et al._ , “Revisiting reward design and evaluation for robust humanoid standing and walking,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024. 

- [36] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” 2024. [37] M. Mittal, _et al._ , “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 6, 2023. 

- [38] T. He, _et al._ , “Hover: Versatile neural whole-body controller for humanoid robots,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025. 

- [39] M. Mittal, _et al._ , “Symmetry considerations for learning task symmetric robot policies,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [40] J. Schulman, _et al._ , “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

