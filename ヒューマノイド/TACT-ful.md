---
title: "TACT-ful: Multi-Channel Terrain Affordance and Compliance Training for Payload-Robust Perceptive Humanoid Locomotion"
date: "2026-06-06"
authors: "Thanh Ly; Truong-Duy Dang; Chien Le; Tan-Dzung Do; Phuong Tuan Dat; Cuc T. Trinh"
url: https://arxiv.org/abs/2606.20645
pdf: https://arxiv.org/pdf/2606.20645
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.20645)** / [論文ページ](https://arxiv.org/abs/2606.20645)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TACT-ful: Multi-Channel Terrain Affordance and** **<u>Compliance Training for Payload-Robust Perceptive</u> Humanoid Locomotion** 

- Thanh Ly<sup>1</sup><sup>_∗_</sup> Truong-Duy Dang<sup>1</sup><sup>_∗_</sup> Chien Le<sup>1</sup> Tan-Dzung Do<sup>1</sup> Phuong Tuan Dat<sup>1</sup> Cuc T. Trinh<sup>1</sup> Vien Anh Ngo<sup>1</sup><sup>_,_2</sup> An T. Le<sup>1</sup><sup>_,_2</sup><sup>_,_3</sup> 

   - 1VinRobotics, Vietnam 2Center for AI Research, VinUniversity, Vietnam 3Intelligent Autonomous Systems, TU Darmstadt, Germany 


Figure 1: A service humanoid, trained on TACT-ful, traverses structured terrain while carrying heavy payload. 

**Abstract:** Foothold selection on structured terrain requires explicit reasoning about contact planarity, surface steepness, and kinematic reachability, properties not captured by a single height-based terrain signal. We propose a multichannel terrain cost combining flatness, steepness, and velocity-aware height feasibility, plus a forward climb reward, that simultaneously drives a GPU-parallel divergent component of motion (DCM) foothold planner and shapes a dense per-step affordance reward for an asymmetric actor-critic policy trained with proximal policy optimization (PPO) from depth images. A Bézier swing trajectory with adaptive apex bias extends foothold tracking to joint position-andorientation, using the arc tangent to guide sole orientation through riser crossings and tread landings. To support payload tasks, we introduce a lower-body compliance training procedure in which a virtual wrench is injected at a sampled load attachment point, generating physically consistent force and moment; wrench-aware compliance targets replace rigid pose penalties, and the policy learns to yield to load-induced perturbations without force sensing. The full system trains end-to-end with standard PPO, no distillation, and no teacher-student staging, and is deployed on a humanoid directly from simulation with configuration changes only. In simulation, the policy reaches 1 _._ 0 m _/_ s on stairs with risers up to 0 _._ 20 m and improves payload robustness up to _∼_ 15 kg centered load and for moment-dominated wrist loads without fine-tuning. We also provide a qualitative hardware demonstration on structured terrain. Project website: `https://fai-rl-tech.github.io/tact-locomotion.github.io/` 

**Keywords:** Humanoid locomotion, terrain affordance, payload compliance 

> _∗_ Equal contribution. Corresponding author: An T. Le, `an@robot-learning.de` . 

## **1 Introduction** 

Service humanoids operating in human environments must traverse structured non-flat terrain, including staircases, stepped platforms, and ramps, while carrying tools or cargo. Foothold placement on such terrain is consequential: a sole that straddles a step edge bears load on a line contact, narrowing the friction cone and generating lateral impulses that scale with robot mass. The capture-point [1] divergence rate is independent of mass, but the ground reaction force needed to intercept a divergent trajectory scales with total weight, so that early, terrain-quality-aware foothold selection [2] becomes more consequential as platform mass grows. Payload carrying adds a second challenge: a carried load shifts the effective neutral pelvis pose and imposes a time-varying tug on the torso, requiring the locomotion controller to absorb these perturbations without loss of balance. 

Existing approaches address subsets of this problem. Model-based foothold planners select discrete landing targets subject to stability and reachability constraints [3, 4, 5], but their outputs are not used to shape the reinforcement-learning (RL) policy reward. Perceptive RL methods for humanoids consume elevation maps or depth images to adapt gait on rough terrain [6, 7, 8], but typically encode terrain through a single height channel and do not reason explicitly about contact planarity or kinematic overreach. Compliance under payload is largely treated separately, either through dedicated force controllers, online payload estimators, or manual gait re-tuning, rather than as a behavior the locomotion policy acquires within a single terrain-aware training run. 

The contributions of this paper are: 

1. **Multi-channel terrain cost with terrain-adaptive swing and tangent-guided foot orientation.** Flatness, steepness, velocity-aware height feasibility, and a climb bonus jointly drive a GPU-parallel DCM foothold planner and serve as a dense terrain-affordance learning signal for the RL policy. A Bézier swing trajectory with adaptive apex bias and clearance extends foothold tracking to joint position-and-orientation references, using the arc tangent to guide sole orientation through riser crossings and tread landings. Unlike the closest predecessor, which couples a single-channel DCM planner to a position-only foothold reward under a multi-stage curriculum [7], our cost adds explicit flatness, velocity-aware feasibility, and speed-gated climb channels, and the tangent schedule extends the swing reference to sole _orientation_ . 

2. **Lower-body compliance training for payload-robust locomotion.** A virtual wrench injected at a sampled load attachment point generates physically consistent force and moment; together with wrench-aware compliance targets for pelvis height and trunk orientation, it teaches the policy to yield to payload-induced perturbations without force sensing, improving robustness up to _∼_ 15 kg centered load and for moment-dominated wrist loads without payload-specific fine-tuning. 

3. **An integrated end-to-end pipeline with a qualitative hardware demonstration.** The system trains with standard PPO in a single run (no distillation, no teacher-student staging) and combines terrain-aware foothold selection with payload compliance, and is deployed zero-shot from simulation on a service humanoid traversing structured terrain while carrying payload. 

## **2 Related Work** 

**Foothold planning and terrain-conditioned reinforcement learning.** Model-based foothold planners select discrete landing targets under LIPM capturability constraints: Acosta and Posa [3] formulate MIQP over convex foothold regions, while Xiang et al. [4] jointly optimize step timing and placement under DCM bounds. Kim et al. [5] replace the MIQP with an RL-trained footstep policy mapping elevation maps to 3D targets, decoupled from end-to-end training. Lee et al. [9] use LIP-derived footstep targets as a partial RL reward, and Liu et al. [7] reformulate DCM foothold search as GPU-parallel discrete optimization used as an explicit RL reward with a multi-stage curriculum, the most direct predecessor to our approach. Wang et al. [10] show that a purely learned dense foothold reward with a double-critic curriculum can traverse sparse footholds without an explicit planner. 

2 


Figure 2: **Overview of the proposed framework.** Two parallel modules feed into the training reward buffer. _(i) DCM foothold planner:_ at every control step, a pelvis-mounted elevation map is consumed by the GPU-parallel DCM foothold planner, which selects terrain-optimal landing targets and produces a Bézier swing trajectory reference; these targets define the foothold-tracking and terrain-specific reward terms and are provided as privileged observations to the critic. _(ii) Wrench compliance scheduler:_ a virtual wrench is injected at a sampled load attachment point, generating force that shifts the pelvis and moment that tilts the trunk; wrench-aware compliance targets replace rigid pelvis-height and orientation penalties, training the policy to absorb payloadinduced perturbations without explicit force sensing. 

**Perceptive humanoid locomotion and terrain representation.** Agarwal et al. [11], Miki et al. [12] pioneered the privileged-training-to-depth-distillation paradigm, decoupling policy and perception learning for zero-shot real-world deployment, which has become standard for perceptive legged locomotion. Building on this, Song et al. [6] reconstruct a dense egocentric height map from depth and jointly output joint targets and adaptive gait frequency; Radosavovic et al. [13] train a Transformer policy on diverse outdoor terrain without perceptive reward shaping; Long et al. [14] achieve stair climbing via LiDAR elevation maps; Ben et al. [8] extend perception to full 3D structure via a voxel-grid representation; Zhang et al. [15] distil terrain-specific experts into a unified transformer policy with multi-view depth fusion and velocity-scaled features; and Sun et al. [16] train end-to-end from raw stereo depth images using terrain-specific multi-critic shaping. Vision-based whole-body policies demonstrate perceptive parkour, stair climbing, gap crossing, and platform jumping, on humanoids and quadrupeds [17, 18, 19]. Standard terrain representations include probabilistic elevation maps [20], traversability scoring [21], and multi-layer grid maps [22]. 

**Payload-carrying and compliant loco-manipulation.** Large-scale domain randomization yields implicit payload tolerance [23]; Kumar et al. [24] achieve payload and terrain robustness on quadrupeds through rapid online system identification; Zhang et al. [25] demonstrate balance recovery under large external perturbations via a multi-phase curriculum; Fu et al. [26] make payload awareness explicit on the Tiangong humanoid via a history-based estimator in a decoupled lowerbody RL architecture, evaluated on flat terrain. Pasricha et al. [27] extend payload limits to 3 _×_ nominal via compliant trajectory diffusion. For force-adaptive compliance without force sensors, Xu et al. [28] train legged robots to absorb collision impulses and sustain payload pulls up to<sup><u>2</u></sup> 3<sup>body</sup> weight by tracking a virtual impedance reference; Zhi et al. [29] unify position and force control for contact-rich loco-manipulation. Terrain property estimation from vision [30] and friction identification [31] connect perception to contact mechanics. None of these works couple terrain-quality-aware foothold selection with compliance training in a single end-to-end RL formulation, leaving the interaction between payload mass, step-height feasibility, and terrain planarity unaddressed. 

## **3 Terrain Affordance and Compliance Training** 

Figure 2 Overview the framework: a DCM foothold planner and a wrench compliance scheduler feed a shared reward for an asymmetric actor-critic policy. All hyperparameters and implementation details are located in the Appendices. 

3 

### **3.1 Capture-Point Stability** 

We use the divergent component of motion (DCM) / capture-point framework [1, 32] with a constant natural frequency _ω_ 0 = ~~�~~ _g/z_ 0, where _g_ is gravitational acceleration and _z_ 0 is the nominal center of mass (CoM) height [33]. The DCM is defined as _ξ_ = _x_ CoM + _x_ ˙ CoM _/ω_ 0 and propagates as _ξ_ ( _T_ ) = _ξ_ 0 _e_<sup>_ω_0</sup><sup>_T_</sup> over a swing of duration _T_ (step time); applied component-wise in the horizontal plane this gives the 2D DCM **_ξ_** _T ∈_ R<sup>2</sup> . The nominal step offset **b** nom = ( _bx, by_ ) keeps the divergent mode in steady state [34]; we adopt the linear-CoM-height reduction of Liu et al. [7] and set _ω_ = _ω_ 0 throughout. 

### **3.2 Multi-Channel Terrain Cost** 

The planner selects the cell _i_ that minimizes the total cost 


where _d_ pos _,i_ = ( _xi − vxT_ )<sup>2</sup> + _β_ ( _yi −_ ( _vyT_ + sign( _f_ ) _lp_ ))<sup>2</sup> is an asymmetric position residual from the nominal stride target ( _β >_ 1 penalizes lateral deviation more than sagittal to limit foot spread; **p** _i_ = ( _xi, yi_ )<sup>_⊤_</sup> is the 2D candidate foothold, ( _vx, vy_ ) the commanded planar velocity, _lp_ the nominal lateral inter-foot distance, and sign( _f_ ) _∈{_ +1 _, −_ 1 _}_ selects the swinging leg), and _d_ dcm _,i_ = _∥_ **_ξ_** _T −_ **p** _i −_ **b** nom _∥_<sup>2</sup> is the capture-point stability residual. These are computed from the elevation map _H_ in one GPU-batched forward pass. 

**Flatness cost** _Q_ **.** A sole straddling a height discontinuity tilts by _θi ≈_ arctan( _Qi/L_ foot), reducing admissible friction to _µ_ eff _,i ≤ µ_ 0 cos _θi −_ sin _θi_ , which collapses to zero at _Qi/L_ foot = _µ_ 0 _≈_ 0 _._ 6, precisely the failure regime on standard stairs. We use the elevation range over a footprint-sized kernel as a GPU-efficient continuous proxy: 


Sampling-based foothold rewards [10] evaluate _contact support coverage_ , suited to surface voids but blind to planarity loss. On structured terrain, a tread-edge landing scores zero under that criterion yet incurs _Qi >_ 0; the two costs target distinct failure modes and are complementary. 

**Steepness cost** _E_ **.** An edge contact on a vertical riser produces a lateral impulse. Sobel-filtered gradients _gx,j_ , _gy,j_ are max-pooled, deliberately propagating the worst gradient within the footprint: 


**Height-feasibility cost** _M_ **.** A step too tall to reach kinematically or dynamically is worse than a sub-optimal flat placement. The quadratic penalty 


where ∆ _zi_ is the stance foot height difference, uses a _velocity-aware effective maximum step height_ : 


where _h_<sup>_∗_</sup> min<sup>and</sup><sup>_h_</sup> max<sup>_∗_boundthereachablestepheightatstandstillandratedforwardspeed</sup><sup>_v∗_,</sup> respectively. At low speed the robot lacks the leg momentum needed to assist a step-up, so the effective kinematic reach is reduced; at high speed the dynamic leg drive can clear the full height. Below a minimum speed threshold a hard override replaces the planned target with the current foot position, and _h_<sup>_∗_</sup> eff<sup>_→h_</sup> min<sup>_∗_ensures the cost still disfavors high steps in the transition region.</sup> 

**Forward climb bonus** _b_ **.** To encourage the robot to step _up_ onto reachable treads, a speed-gated capped bonus _bi_ = min�max(∆ _zi,_ 0) _, h_<sup>_∗_</sup> eff � _·_ **1** [ _vx > v_ min] rewards upward steps proportionally to their height, capped at _h_<sup>_∗_</sup> eff<sup>.</sup> 

4 


Figure 3: **Bézier swing arcs with adaptive apex bias.** (a) Step-up: apex biased toward the landing target, keeping the peak over the riser face. (b) Step-down: apex biased toward lift-off, extending horizontal travel before descent. (c) Gap: behave analogously, with clearance scaled by _|_ ∆ _z|_ . 

### **3.3 Bézier Swing Trajectory and Tangent-Guided Foot Orientation** 

After selecting per-foot landing target **p**<sup>_∗_</sup> _f_<sup>, the swing foot tracks a quadratic Bézier arc whose tangent</sup> simultaneously determines foot orientation: 


where **p** _ℓ_ is the lift-off position and **p** ˙ ( _u_ ) points in the direction of instantaneous foot travel. The apex _xy_ is biased toward whichever endpoint is higher: 


For step-up (∆ _z >_ 0), bias _>_ 0 _._ 5 places the trajectory peak over the riser face, preventing premature descent onto the vertical surface; for step-down (∆ _z <_ 0), bias _<_ 0 _._ 5 extends horizontal travel before descent, reducing the landing impact angle (fig. 3a-b). A phase-conditional schedule derived from **p** ˙ ( _u_ ) guides sole orientation through riser crossings. Both position proximity and foot heading are jointly optimized during swing via an exponential proximity kernel: 


where **d**<sup>ˆ</sup> _f_ = _Rf_ **e** ˆ _x_ is the foot forward axis and _σd_ = 0 recovers the position-only form when orientation is not used. 

The apex height adapts to terrain relief: 


where _s_ is a clearance scale factor and _c_ max caps the swing peak. The tangent is vertical at 


equal to 0 _._ 5 for level steps and shifting toward the higher endpoint on transitions. Two windows around _u_ peak define the reference unit vector<sup>ˆ</sup> **t** _f_ ( _u_ ): in the _pre-apex_ window [ _u_ peak _−δℓ_<sup>_−,u_peak</sup><sup>_−δ_</sup> _ℓ_<sup>+),</sup><sup>**p**˙is rotated 90</sup><sup>_◦_in the sagittal plane ((</sup><sup>_tx, ty, tz_)</sup><sup>_�→_(</sup><sup>_tz, ty, −tx_)) and nor-</sup> malized, yielding a forward-downward direction that guides the sole through the riser and reduces toe-strike risk; in the _post-apex_ window ( _u_ peak+ _δr_<sup>_−,u_peak+</sup><sup>_δ_</sup> _r_<sup>+], ˆ</sup><sup>**t**</sup><sup>_f_=</sup><sup>**p**˙</sup><sup>_/∥_</sup><sup>**p**˙</sup><sup>_∥_aligns the foot with</sup> the forward travel direction for tread landing; elsewhere<sup>ˆ</sup> **t** _f_ = **0** (no orientation constraint). 

### **3.4 Lower Body Compliance Training** 

A payload exerts a wrench **W** = ( **F** _,_ **_τ_** ) on the robot, where the moment **_τ_** = **r** load _×_ **F** scales with the CoM-to-load arm **r** load independently of mass. **_τ_** ext tilts the trunk by _φ_ , displacing the CoM by ∆ _x_ CoM _≈ d_ CoM _φ_ ; under LIPM this offset grows by _e_<sup>_ω_0</sup><sup>_T_step</sup> _>_ 2 over a typical step, so 

5 

moment-induced tilt perturbs the capture point more than an equivalent translational offset, and both components of **W** require explicit coverage in the disturbance distribution. We emulate the wrench by applying a spring-damper at the _virtual load attachment point_ **p** load = **p** CoM + **r** load: 


where **p** _a_ is a fixed world-frame anchor drawn once per episode, with stiffness _k_ and damping _c_ set so the spring force at maximum displacement _Ra_ reaches a fixed fraction of nominal weight. Applying the force at **p** load rather than the CoM generates **_τ_** ext = **r** load _×_ **F** ext automatically. At each reset, **r** load is drawn from a two-component mixture ( **r** load = **r** body with prob. _ρ_ body, else **r** arm) that jointly covers both carry scenarios: _Body-attached_ with **r** body _∼_ Ball( _R_ close), direction biased toward _−_ **z** ˆ; and _Arm-extended_ with **r** arm from a shoulder-frame half-ellipsoid, biased forward. Both components use cosine-power lobes to concentrate sampling: 


where **d**<sup>ˆ</sup> is the unit direction of **r** body and _θ_ its polar angle from _−_ **z** ˆ. A weight- _ϵ_ isotropic component blends in lateral and overhead samples. We replace the height and orientation penalties with wrenchaware compliance targets. For the height, 


where _h_<sup>_∗_</sup> is the commanded base height, _za_ ( _t_ ) = [ **p** load( _t_ )] _z_ is the world-frame z-coordinate of the virtual attachment point, and _αz ∈_ [0 _,_ 1] is the height compliance gain. For the trunk orientation, the virtual target is derived from the induced moment: 


where _τx, τy_ are the roll and pitch components of **_τ_** ext, _k_ rot [N _·_ m _/_ rad] is a rotational stiffness converting induced moment to a tilt angle, and _αφ, αψ ∈_ [0 _,_ 1] are orientation compliance gains. The combined compliance reward is 


where _φB, ψB_ are pelvis pitch and roll from the projected gravity vector. When _αz_ = _αφ_ = _αψ_ = 0 the reward collapses to the original rigid height and orientation penalties; at nonzero gains the policy learns to yield to the full wrench, acquiring wrench-aware compliance in both translation and rotation as a learned behavior without explicit force or torque sensing. 

### **3.5 Policy and Training** 

An asymmetric Actor-Critic Encoder is used. The actor concatenates a convolutional embedding of a temporally stacked depth image with proprioceptive state and passes the result through a feedforward multilayer perceptron (MLP). The critic shares the same encoder but also receives privileged training-only signals. Actions are joint position targets relative to the default pose, converted to torques via proportional-derivative (PD) control and clipped to mechanical limits. Following the gait-adaptive extension [6], the policy also outputs a scalar gait frequency _ft_ that advances an internal phase clock via an exponential-moving-average (EMA) smoothed update: 


with ( _f_<sup>ˆ</sup> _t,_ sin 2 _πϕt,_ cos 2 _πϕt_ ) appended to the actor observation. Training uses standard PPO [35] with adaptive Kullback–Leibler (KL) scheduling, generalized advantage estimation (GAE), and massively-parallel joint-velocity and terrain-difficulty curricula [36]. 

6 


Figure 4: Terrain traversal ablation on **standard terrain** (top) and **hard terrain** (out-of-distribution). 

## **4 Results** 

**Experimental setup.** Four variants are compared: _TACT + Adaptive Gait (Ours)_ , _TACT-only_ , _Adaptive Gait only_ , and _Baseline_ (a standard depth-map perceptive policy with no terrain-cost channels and no privileged elevation-map input to the critic). Each variant is evaluated at iteration 20 k across 4096 environments in MuJoCo [37] on stairs, slopes, and rough terrain; a second, unseen hard-terrain sweep covers risers 0 _._ 20–0 _._ 30 m, over which we report the success rate SRhard computed on the strict interior [0 _._ 22 _,_ 0 _._ 28] m. 

### **4.1 Terrain Traversal Ablation** 

Ours (TACT + Adaptive Gait) leads on both standard and hard terrain (70 % standard SR and 30 % SRhard), outperforming TACT-only by 13 and 9 percentage points (pp) and Adaptive Gait only by 17 and 12 pp (Fig. 4); Adaptive Gait only falls below the Baseline on hard terrain (18 % vs. 19 %), confirming that frequency re-timing without terrain-quality guidance is actively harmful when risers approach kinematic limits. The Baseline’s 52 % and 19 % SR coincide with the highest 95th-percentile ground reaction force (GRF) ( _≈_ 6 _._ 7 _×_ and 8 _._ 0 _× mg/_ 2), consistent with edge-biased contacts from blind foothold placement. On efficiency, Ours achieves lower velocity-tracking root-mean-square error (RMSE) (0 _._ 22 vs. 0 _._ 23 m _/_ s) and mechanical power (229 vs. 241 W) than TACT-only on hard terrain; _Q_ c is identical between the two (0 _._ 023), isolating terrain cost channels as the mechanism for tread-centered landings. Fig. 5a shows that the SR gap relative to the Baseline is speed-invariant (71 _/_ 68 _/_ 69 % vs. _≈_ 20 pp lower at 0 _._ 3 _/_ 0 _._ 6 _/_ 1 _._ 0 m _/_ s), confirming foothold quality, not speed, drives the difference; Fig. 5b shows that removing all TACT channel weights raises foot-target distance 2 _._ 8 _×_ (0 _._ 088 _→_ 0 _._ 251 m). 

### **4.2 Payload Generalization** 

Fig. 5c evaluates payload generalization across three conditions (pelvis +15 kg, pelvis +20 kg, wrist +10 kg) on terrain and compares Ours against the Baseline. At moderate centered load (pelvis +15 kg), Ours achieves 50 % SR versus the Baseline’s 38 % at lower power (247 W vs. 277 W), consistent with compliance training absorbing the downward wrench and suppressing impulsive GRF recovery. At high centered load (pelvis +20 kg), both policies degrade substantially to _≈_ 37 % and _≈_ 35 % SR respectively, nearly indistinguishable, indicating the load magnitude approaches the boundary of the training distribution; power rises for both, with Ours remaining 27 W below the Baseline (293 vs. 320 W), confirming that partial compliance is retained even as balance recovery deteriorates. Wrist-mounted mass (+10 kg), which generates a large moment rather than a direct CoM shift, yields the largest margin across all three conditions: Ours achieves 65 % SR versus the 

7 


Figure 5: (a) Speed-conditioned SR; (b) foot-target distance; (c) SR (%) and mean power (W). (d–f) Qualitative hardware payload demonstrations, separate from the simulated ablations (d–e: 20 kg backpack; f: 7 kg tray). 

Baseline’s 50 % at 223 W versus 259 W, consistent with the arm-extended wrench samples in the disturbance force-field explicitly targeting moment-dominated loads. 

## **5 Limitations** 

**Simulation-only evaluation.** All quantitative ablations are conducted in MuJoCo; hardware results are qualitative demonstrations, with domain randomization as the sole sim-to-real bridge, so absolute success rates on real structured terrain remain uncharacterized and unmodeled contact phenomena will shift them. Even in simulation, the best variant reaches only 30 % SRhard on hard terrain (interior risers 0 _._ 22–0 _._ 28 m), a ceiling insufficient for reliable deployment on tall staircases. 

**Compliance and perception scope.** The compliance benefit vanishes near 20 kg of centered load (Ours _≈_ 37 % vs. Baseline _≈_ 35 % SR at pelvis +20 kg): the sampled wrench distribution and legonly actuation set an effective payload ceiling, and lateral or distributed loads fall outside the sampled space. The DCM planner depends on accurate elevation-map registration with no fallback under localization drift, and the forward-facing depth camera gives no lateral coverage. Finally, the terrain cost channels are collectively necessary but individually non-critical, removing any one keeps foot-target distance within 5 %, and their weights are hand-tuned rather than derived. Extended analysis of each limitation (adaptive-gait fragility, channel redundancy, upper-body coupling, and deformable/low-friction terrain) is given in Appendix. 

## **6 Conclusion** 

We presented a physics-informed terrain affordance learning system for payload-robust perceptive humanoid locomotion. A multi-channel terrain cost drives a GPU-parallel DCM foothold planner and provides a dense terrain-affordance learning signal to the RL policy; a terrain-adaptive Bézier swing with tangent-guided foot orientation extends foothold tracking to joint position-andorientation references. Because the cost is defined from sole geometry rather than learned per embodiment [12], it is platform-agnostic by construction. Lower-body compliance training via a cosine-power-weighted virtual spring-damper yields a learned wrench-dependent impedance (conceptually related to virtual impedance tracking [28] but without a separate impedance reference, and avoiding the online payload estimation of Kumar et al. [24]), improving payload robustness up to _∼_ 15 kg centered load and for moment-dominated wrist loads without retraining. The full system trains with standard PPO in a single run (no teacher-student distillation [11, 15]) and is deployed zero-shot from simulation on a humanoid; quantitative real-world evaluation and a terrain _×_ payload coupling study are the main remaining steps toward reliable deployment. 

8 

## **References** 

- [1] J. Pratt, J. Carff, S. Drakunov, and A. Goswami. Capture point: A step toward humanoid push recovery. In _2006 6th IEEE-RAS International Conference on Humanoid Robots (Humanoids)_ , pages 200–207, 2006. doi:10.1109/ICHR.2006.321385. 

- [2] E. Whitman and G. C. Fay. Terrain aware step planning system. U.S. Patent Application Publication US20200117198A1, assigned to Boston Dynamics, Inc., Apr. 2020. URL `https://patents.google.com/patent/US20200117198A1/en` . Published Apr. 16, 2020; granted as US11287826B2. 

- [3] B. Acosta and M. Posa. Perceptive mixed-integer footstep control for underactuated bipedal walking on rough terrain. _IEEE Transactions on Robotics_ , 41:4518–4537, 2025. doi:10.1109/ TRO.2025.3587998. 

- [4] Z. Xiang, U. Pant, and A. Hereid. Perceptive variable-timing footstep planning for humanoid locomotion on disconnected footholds, 2026. URL `https://arxiv.org/abs/2603.07400` . 

- [5] M. Kim, B. Acosta, P. Chaudhari, and M. Posa. Learning a vision-based footstep planner for hierarchical walking control. _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 1–8, 2025. URL `https://arxiv.org/abs/2508.06779` . 

- [6] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li. Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction. _IEEE Robotics and Automation Letters_ , 11(4):4969–4976, 2026. doi:10.1109/LRA.2026.3664167. 

- [7] Y. Liu, T. Yu, H. Song, H. Zhu, N. Hu, Y. Hao, X. Yao, X. Zang, H. Chen, and J. Zhao. FastStair: Learning to run up stairs with humanoid robots, 2026. URL `https://arxiv.org/ abs/2601.10365` . 

- [8] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3D constrained terrains, 2025. URL `https://arxiv.org/abs/2511.14625` . 

- [9] H. J. Lee, S. Hong, and S. Kim. Integrating model-based footstep planning with modelfree reinforcement learning for dynamic legged locomotion. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11248–11255, 2024. doi: 10.1109/IROS58592.2024.10801468. 

- [10] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. BeamDojo: Learning agile humanoid locomotion on sparse footholds. In _Proceedings of Robotics: Science and Systems_ , Los Angeles, CA, USA, June 2025. doi:10.15607/RSS.2025.XXI.068. URL `https: //www.roboticsproceedings.org/rss21/p068.html` . 

- [11] A. Agarwal, A. Kumar, J. Malik, and D. Pathak. Legged locomotion in challenging terrains using egocentric vision, 2022. URL `https://arxiv.org/abs/2211.07638` . 

- [12] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science Robotics_ , 7(62):eabk2822, 2022. doi:10.1126/scirobotics.abk2822. URL `https://doi.org/10.1126/scirobotics. abk2822` . 

- [13] I. Radosavovic, S. Kamat, T. Darrell, and J. Malik. Learning humanoid locomotion over challenging terrain, 2024. URL `https://arxiv.org/abs/2410.03654` . 

- [14] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang. Learning humanoid locomotion with perceptive internal model, 2024. URL `https://arxiv.org/abs/2411.14386` . 

9 

- [15] Y. Zhang, Y. Seo, J. Chen, Y. Yuan, K. Sreenath, P. Abbeel, C. Sferrazza, K. Liu, R. Duan, and G. Shi. RPL: Learning robust humanoid perceptive locomotion on challenging terrains, 2026. URL `https://arxiv.org/abs/2602.03002` . 

- [16] W. Sun, Y. Su, L. Huang, A. Zhang, D. Wei, M. San, D. Tian, E. Cao, B. Cao, Y. Liu, F. Yan, E. Xie, and Z. Xie. Now You See That: Learning end-to-end humanoid locomotion from raw pixels, 2026. URL `https://arxiv.org/abs/2602.06382` . 

- [17] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning, 2024. URL `https://arxiv. org/abs/2406.10759` . 

- [18] Z. Wu, X. Huang, L. Yang, Y. Zhang, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza, G. Shi, and C. K. Liu. Perceptive Humanoid Parkour: Chaining dynamic human skills via motion matching, 2026. URL `https://arxiv.org/abs/2602.15827` . 

- [19] D. Hoeller, N. Rudin, D. Sako, and M. Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots, 2023. URL `https://arxiv.org/abs/2306.14874` . 

- [20] P. Fankhauser, M. Bloesch, and M. Hutter. Probabilistic terrain mapping for mobile robots with uncertain localization. _IEEE Robotics and Automation Letters_ , 3(4):3019–3026, 2018. doi:10.1109/LRA.2018.2849506. URL `https://doi.org/10.1109/LRA.2018.2849506` . 

- [21] D. D. Fan, K. Otsu, Y. Kubo, A. Dixit, J. Burdick, and A.-a. Agha-mohammadi. STEP: Stochastic traversability evaluation and planning for risk-aware off-road navigation. In _Proceedings of Robotics: Science and Systems_ , Virtual, July 2021. doi:10.15607/RSS.2021.XVII. 021. URL `https://www.roboticsproceedings.org/rss17/p021.html` . 

- [22] P. Fankhauser and M. Hutter. A universal grid map library: Implementation and use case for rough terrain navigation. In A. Koubaa, editor, _Robot Operating System (ROS): The Complete Reference (Volume 1)_ , volume 625 of _Studies in Computational Intelligence_ , chapter 5, pages 99–120. Springer, Cham, 2016. doi:10.1007/978-3-319-26054-9_5. URL `https://doi. org/10.1007/978-3-319-26054-9_5` . 

- [23] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath. Real-world humanoid locomotion with reinforcement learning, 2023. URL `https://arxiv.org/abs/ 2303.03381` . 

- [24] A. Kumar, Z. Fu, D. Pathak, and J. Malik. RMA: Rapid motor adaptation for legged robots. In _Proceedings of Robotics: Science and Systems_ , Virtual, July 2021. doi:10.15607/RSS.2021. XVII.011. URL `https://www.roboticsproceedings.org/rss17/p011.html` . 

- [25] T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath, and Y. Gao. HuB: Learning extreme humanoid balance, 2025. URL `https://arxiv.org/ abs/2505.07294` . 

- [26] L. Fu, Y. Zhong, X. Li, Y. Liu, Z. Xu, J. Tang, and S. Li. Load-aware locomotion control for humanoid robots in industrial transportation tasks, 2026. URL `https://arxiv.org/abs/ 2603.14308` . 

- [27] A. Pasricha, J. Koh, J. Vakil, and A. Roncone. Dynamics-compliant trajectory diffusion for super-nominal payload manipulation, 2025. URL `https://arxiv.org/abs/2508.21375` . 

- [28] B. Xu, H. Weng, Q. Lu, Y. Gao, and H. Xu. Facet: Force-adaptive control via impedance reference tracking for legged robots, 2025. URL `https://arxiv.org/abs/2505.06883` . 

- [29] P. Zhi, P. Li, J. Yin, B. Jia, and S. Huang. Learning a unified policy for position and force control in legged loco-manipulation, 2025. URL `https://arxiv.org/abs/2505.20829` . 

10 

- [30] J. Chen, J. Frey, R. Zhou, T. Miki, G. Martius, and M. Hutter. Identifying terrain physical parameters from vision - towards physical-parameter-aware locomotion and navigation. _IEEE Robotics and Automation Letters_ , 9(11):9279–9286, 2024. doi:10.1109/LRA.2024.3455788. URL `https://doi.org/10.1109/LRA.2024.3455788` . 

- [31] H. Kim, D. Kang, M. G. Kim, G. Kim, and H. W. Park. Online friction coefficient identification for legged robots on slippery terrain using smoothed contact gradients. _IEEE Robotics and Automation Letters_ , 10(4):3150–3157, 2025. doi:10.1109/LRA.2025.3541428. URL `https: //doi.org/10.1109/LRA.2025.3541428` . 

- [32] J. Englsberger, C. Ott, and A. Albu-Schäffer. Three-dimensional bipedal walking control based on divergent component of motion. _IEEE Transactions on Robotics_ , 31(2):355–368, 2015. doi: 10.1109/TRO.2015.2405592. 

- [33] M. Khadiv, A. Herzog, S. A. A. Moosavian, and L. Righetti. Walking control based on step timing adaptation. _IEEE Transactions on Robotics_ , 36(3):629–643, 2020. doi:10.1109/TRO. 2020.2982584. 

- [34] T. Koolen, T. De Boer, J. Rebula, A. Goswami, and J. Pratt. Capturability-based analysis and control of legged locomotion, part 1: Theory and application to three simple gait models. _The International Journal of Robotics Research_ , 31:1094–1113, 07 2012. doi: 10.1177/0278364912452673. 

- [35] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347, 2017. URL `https://arxiv.org/abs/1707. 06347` . 

- [36] N. Rudin, D. Hoeller, P. Reist, and M. Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In A. Faust, D. Hsu, and G. Neumann, editors, _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pages 91–100. PMLR, 08–11 Nov 2022. URL `https: //proceedings.mlr.press/v164/rudin22a.html` . 

- [37] E. Todorov, T. Erez, and Y. Tassa. MuJoCo: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5026–5033, 2012. doi:10.1109/IROS.2012.6386109. 

11 

## **Appendix** 

### **A Implementation Details** 

**DCM derivation (§3.1).** Liu et al. [7] show that for a linear CoM height profile _z_ ( _t_ ) = _kzt_ + _z_ 0 during swing, the Variable-Height Inverted Pendulum dynamics reduce to _ξ_<sup>˙</sup> _≈ ω_ ( _t_ ) _ξ_ when _a_ = 1 + _kz/_ (2<sup>_~~√~~_</sup> _<u>gz</u>_ 0) _≈_ 1; we adopt this result and set _ω_ = _ω_ 0. The steady-state nominal step offset that keeps the divergent mode bounded [34] is _bx_ = _vxT/_ ( _e_<sup>_ω_0</sup><sup>_T_</sup> _−_ 1) and _by_ = sign( _f_ ) _lp/_ (1 + _e_<sup>_ω_0</sup><sup>_T_</sup> ), where _lp_ is the nominal lateral inter-foot distance and sign( _f_ ) _∈{_ +1 _, −_ 1 _}_ selects the swinging leg. 

Table 1: DCM foothold planner configuration. 

|Parameter|Value|Notes|
|---|---|---|
|_z_0|0_._90 m|Nominal CoM height|
|_T_swing (=_T_ in §3.1)|0_._45 s|Half gait period|
|_lp_|0_._20 m|Lateral inter-foot distance|
|_κ_|0_._4|Bézier apex bias gain|
|_b_min_, b_max|0_._25_,_ 0_._75|Bézier bias clamp bounds|
|_c_min|0_._05 m|Base swing clearance|
|_s_|0_._5|Clearance scale (m per m step height)|
|_c_max|0_._20 m|Maximum swing clearance|
|_δ_<sup>_−_</sup><br>_ℓ_<sup>_, δ_+</sup><br>_ℓ_|0_._30_,_ 0_._05|Lift phase: swing fractions before/after apex where<br>tangent orientation is blended|
|_δ_<sup>_−_</sup><br>_r _<sup>_, δ_+</sup><br>_r_|0_._05_,_ 0_._25|Reach phase:<br>swing fractions before/after apex<br>where landing orientation is blended|
|Elevation map|37_×_25,0_._05 m|1_._80_×_1_._20 mat pelvis|
|Foot footprint kernel|0_._25_×_0_._10 m|For_Qi_,_Ei_ pooling|
|Search window|_±_0_._30 m(x and y)|Around nominal stride; fallback to nominal at<br>mean valid height if empty|
|_h_<sup>_∗_</sup><br>min|0_._05 m|Effective step height at standstill|
|_h_<sup>_∗_</sup><br>max|0_._28 m|Effective step height at rated speed|
|_v_<sup>_∗_</sup>|0_._5 m_/_s|Rated forward speed for_h_<sup>_∗_</sup><br>eff <sup>scaling (Eq. (5))</sup>|
|_v_min|0_._05 m_/_s|Standing override: planned target replaced by cur-<br>rent foot position|
|Lateral penalty|_β_ = 2_._5|Lateral vs. sagittal asymmetry|
|_α_pos_, α_dcm|1_._0_,_ 0_._5|Position and capture-point stability|
|_αE, αQ, αM, α_climb|0_._6_,_ 4_._0_,_ 6_._0_,_ 1_._5|Terrain channels (Eq. (1))|
|_Gait-adaptive extension_|||
|_f_min_, f_max|1_._0_,_ 1_._5 Hz|Gait frequency bounds|
|_α_EMA|0_._2|Frequency smoothing weight|


### **B Policy Learning Details** 

**Observation space (actor).** Base angular velocity, projected gravity vector, velocity command, joint positions and velocities relative to default, last action, binary foot contacts, gait phase (sin _ϕ_ , cos _ϕ_ ), and a stacked depth image (four temporally delayed frames at 30 Hz, blurred, range-clipped, and normalized). Proprioceptive signals are maintained as a 5-frame history at the 50 Hz control frequency; the depth image stack is updated at the camera pipeline rate (30 Hz). **Observation space (critic, training only).** Actor observations plus: true CoM velocity, noiseless elevation map (ray misses filled with a sentinel value), ground-truth foot contact forces and heights, foot air times, and planner landing targets **p**<sup>_∗_</sup> _f_<sup>for each foot.</sup> 

**Training hyperparameters.** PPO with clip parameter _ϵ_ = 0 _._ 2, learning rate 10<sup>_−_3</sup> with adaptive KL-based scheduling, GAE _λ_ = 0 _._ 95, discount _γ_ = 0 _._ 99, 5 learning epochs per rollout, 4 minibatches, 24 steps per environment per rollout. 

12 

Table 2: Lower-body compliance training <u>parameters (§3.4).</u> 

|Parameter|Value|Notes|
|---|---|---|
|_Spring-damper_|||
|_Ra_|0_._40 m|Anchor ball radius|
|_k_|200 N_/_m|Virtual spring stiffness|
|_c_|20 N_·_s_/_m|Virtual damping|
|_Wrench sampling_|||
|_ρ_body|0_._6|Body-attached component probability|
|_R_close|0_._10 m|Body-attached ball radius|
|_n_|2|Cosine-power exponent (bias toward_−_ˆ**z**)|
|_nr_|3|Cosine-power exponent (arm-extended forward bias)|
|(_a_fwd_, a_lat_, a_vert)|(0_._50_,_ 0_._40_,_ 0_._30) m|Arm-extended half-ellipsoid semi-axes|
|_ϵ_|0_._1|Isotropic mixture weight|
|_Compliance targets_|_(Eq._(13)_,_(14)_)_||
|_k_leg|300 N_/_m|Effective leg stiffness; gives_αz_ =_k/_(_k_+_k_leg) = 0_._40|
|_αz_|_k/_(_k_+_k_leg) = 0_._40|Height compliance gain|
|_k_rot|50 N_·_m_/_rad|Rotational stiffness (moment-to-tilt conversion)|
|_αφ, αψ_|0_._5|Orientation compliance gains (pitch, roll)|


Table 3: Reward terms. Terrain-specific terms are highlighted; all other terms are standard locomotion rewards. _If_ denotes foot contact, _Ff_ contact force, _Lc_ centroidal angular momentum. 

Term _w_ Definition _Velocity tracking r_ vel _,xy_ +3 _._ 5 exp( _−∥exy∥_<sup>2</sup> _/_ 0 _._ 25) _r_ vel _,z_ +3 _._ 0 exp( _−e_<sup>2</sup> _z_<sup>_/_0</sup><sup>_._5)</sup> _Gait quality r_ gait +2 _._ 0 Phase match: stance/swing vs. gait clock _r_ airtime +2 _._ 0 Single-stance duration reward _r_ orient _−_ 7 _._ 0 _∥_ **g** _xy∥_<sup>2</sup> (base tilt) _r_ pelvis _−_ 3 _._ 0 _∥_ **g** _xy∥_<sup>2</sup> (pelvis) _r_ action _−_ 0 _._ 8 _∥at − at−_ 1 _∥_<sup>2</sup> _r_ collision _−_ 2 _._ 0 Self-collision force _>_ 10 N _r_ limits _−_ 1 _._ 0 Joint-limit violation _r_ slip _−_ 0 _._ 4 Tangential contact velocity _rL −_ 0 _._ 001 _∥Lc∥_<sup>2</sup> angular momentum **_Terrain-specific (contribution)_** _r_ foothold + **2** _._ **1** Eq. (8); _σp_ = 10, _σd ∈{_ 0 _,_ 5 _._ 0 _} r_ clearance _−_ **0** _._ **5** � _f_<sup>_|h_</sup> _f_<sup>foot</sup> _− h_<sup>terrain</sup> _f − d_<sup>_∗_</sup> _| · ∥vf,xy∥_ , _d_<sup>_∗_</sup> = 0 _._ 06 m _r_ stumble _−_ **0** _._ **5 1** [ _∥Ff_<sup>_xy∥>_4</sup><sup>_|F_</sup> _f_<sup>_z|∧∥v_</sup> _f_<sup>_xy∥>_0</sup><sup>_._15 m</sup><sup>_/_s]</sup> _r_ comply _−_ **1** _._ **5** Eq. (15); _h_<sup>_∗_</sup> = 0 _._ 90 m, _αz_ = _k/_ ( _k_ + _k_ leg) 

Table 4: Domain randomization ranges applied at episode startup. 

|Parameter|Range|Mode|
|---|---|---|
|Waist-link mass offset|[_−_2_,_+2] kg|add|
|Other body masses|_×_[0_._95_,_1_._05]|scale|
|Foot friction|[0_._3_,_1_._6]|absolute|
|PD gains (_Kp_,_Kd_)|_×_[0_._7_,_1_._1]|scale|
|Joint stiffness / damping|_×_[0_._7_,_1_._3]|scale|
|Joint armature|_×_[0_._2_,_5_._0]|scale|
|CoM offset (pelvis)|_±_0_._05 m|add|
|Encoder bias|_±_0_._015 radper joint|add|
|Depth camera pose|<br>pos_x, y ±_0_._01m,_z_ (_−_0_._03_,_+0_._01)m; rot roll/yaw_±_2<sup>_◦_</sup>, pitch_±_10<sup>_◦_</sup>|add|


**Curriculum.** A two-stage velocity curriculum starts at [0 _,_ 0 _._ 5] m _/_ s and expands to [0 _,_ 1 _._ 0] m _/_ s after 120,000 steps. The terrain curriculum uses stairs with 0.05–0.20 m risers and 0.30–0.60 m treads, open-width stairs, and flat sections. 

13 

Table 5: Actor network specification. 

|Component|Specification|
|---|---|
|Depth encoder|Conv2d: channels[32_,_32], kernel3_×_3, max-pool<br>FC:[128_,_64], output embedding_∈_R<sup>64</sup>|
|Actor MLP|Input: embed (64)_⊕_proprioception; hidden(1024_,_512_,_256_,_128), ELU activation|
|Action|Joint position increments, clipped to limits|
|History|5-frame obs history at 50 Hz|


**Gait-adaptive frequency action.** The policy outputs a scalar gait frequency _ft ∈_ [ _f_ min _, f_ max] as an additional action dimension appended after joint targets. Each physics step the gait phase advances as _ϕt_ = ( _ϕt−_ 1 + ∆ _t_ phys _· ft_ ) mod 1 _._ 0. The raw policy output is clipped to [ _f_ min _, f_ max] and smoothed by an EMA before use: _ft_ = (1 _−α_ EMA) _ft−_ 1 + _α_ EMA clip( _ft_<sup>raw</sup> _, f_ min _, f_ max). The phase and its sinusoidal encoding (sin _ϕt,_ cos _ϕt_ ) are included in the actor observation; _f_ min, _f_ max, and _α_ EMA are listed in the DCM planner table (§A). 

**Auxiliary reward terms.** _Clearance_ :<sup>�</sup> _f_<sup>_|h_</sup> _f_<sup>foot</sup> _−h_<sup>terrain</sup> _f −d_<sup>_∗_</sup> _|·∥vf,xy∥_ penalizes swing proximity to the terrain, velocity-weighted so edge collisions at high swing speed incur proportionally larger cost. _Stumble_ : fires when _∥Ff_<sup>_xy∥>_4</sup><sup>_|F_</sup> _f_<sup>_z|_and</sup><sup>_∥v_</sup> _f_<sup>_xy∥>_0</sup><sup>_._15 m</sup><sup>_/_s;thecriterion</sup><sup>_µ_eff</sup><sup>_>_4reliably</sup> distinguishes riser edge-strikes from high-force landings. _Compliant base height_ : ( _z_ pelvis _− z_ virt<sup>_∗_)2</sup> tracks a virtual compliant target (eq. (13)); at zero compliance gain it reduces to the standard terrainrelative penalty, preserving the LIPM eigenfrequency _ω_ 0 = ~~�~~ _g/z_ 0 through elevation changes. 

### **C Experimental Details** 

**Training setup.** All policies are trained on a single NVIDIA H100 SXM5 80 GB GPU with 8192 parallel MuJoCo environments. Each iteration collects 24 simulation steps per environment. The PPO rollout and network update run on the same GPU; physics simulation is CPU-parallelized across the host node’s available cores. All training uses the `mjlab` framework with MuJoCo 3.8.0 as the physics backend. Total wall-clock training time per variant is approximately 10–12 h. 

**Training terrain configurations.** Figure 6 shows the eight terrain types used during curriculum training. Stair variants (a–d) are the primary training signal for the multi-channel terrain cost and foothold reward; slope and rough terrain (e–h) provide gradient and contact-stability diversity. The policy is never trained with riser heights above 0 _._ 20 m; the hard-terrain evaluation extends risers to 0 _._ 30 m and is fully out-of-distribution. 

**Evaluation setup.** All ablation variants are evaluated at iteration 20 k with 4096 environments using different random seeds in MuJoCo on stairs, slopes, and rough terrain. Standard evaluation terrain spans the same riser range as training: stair flights with risers 0 _._ 05 m to 0 _._ 20 m and treads 0 _._ 25 m to 0 _._ 55 m, including 3-step and 5-step flights, open-width stairs (no side walls), slopes up to 23<sup>_◦_</sup> , and random rough height fields 0–0 _._ 15 m. Hard-terrain evaluation uses riser heights 0 _._ 20–0 _._ 30 m with configurations unseen during training. An episode succeeds if the robot traverses _D_ target = 10 m without triggering fall termination (base tilt _>_ 70<sup>_◦_</sup> , self-collision, or joint-limit violation). SRhard is computed over the strict interior riser range [0 _._ 22 _,_ 0 _._ 28] m, excluding the boundary cases at the edges of the hard sweep. 

**Ablation variants.** All variants share the base training setup; only cost weights, reward terms, and observation inputs differ. Each is evaluated at iteration 20 k with 4096 environments over different random seeds. 

_TACT + Adaptive Gait (Ours)_ : full system with all four terrain-cost channels ( _αE, αQ, αM , α_ climb _>_ 0; _β >_ 1 controls lateral asymmetry in _d_ pos), foothold tracking reward, and gait-adaptive frequency head [6]. 

14 


Figure 6: **Training terrain configurations.** (a) Pyramid stairs, ascending. (b) Pyramid stairs, descending. (c) Open-width stairs, ascending (no side walls). (d) Open-width stairs, descending. (e) Pyramid slope, ascending. (f) Pyramid slope, descending. (g) Stepping stones. (h) Gravel (random rough height field). Stair risers span 0 _._ 05 m to 0 _._ 20 m with treads 0 _._ 25 m to 0 _._ 55 m; slopes up to 23<sup>_◦_</sup> ; rough field height 0–0 _._ 15 m. Hardterrain evaluation extends risers to 0 _._ 30 m (out-of-distribution). 

_TACT-only_ : all terrain-cost channels and foothold tracking reward active; gait-adaptive frequency head removed. 

_Adaptive Gait only_ : gait-adaptive frequency head added; all terrain-cost channel weights and foothold tracking reward set to zero ( _αQ_ = _αE_ = _αM_ = _α_ climb=0, _w_ foothold=0); no privileged heightmap input to the critic. 

_Baseline_ : standard depth-map perceptive policy; neither TACT channels nor gait adaptation; no privileged critic input. 

**Payload generalization (terrain).** Three attachment conditions are evaluated: pelvis-mounted +15 kg and +20 kg (CoM offset; tests balance under downward wrench) and wrist-mounted +10 kg (large moment arm; tests trunk-tilt compliance). Mass is added at test time with no policy modification. A no-mass-DR baseline is trained identically to the full policy but without waist-link mass offset randomization. Each condition uses 100 episodes at _vx_ = 0 _._ 5 m s<sup>_−_1</sup> on a 5-step staircase with 0 _._ 20 m risers. 

**Planned evaluations (future work).** The following targeted protocols are specified for completeness; their quantitative results are deferred to future work and not claimed here: non-nominal pelvisheight tracking ( _h_<sup>_∗_</sup> _∈{h_ 0 _−_ 6 _, h_ 0 _−_ 3 _, h_ 0+3 _}_ cm, recording _h_<sup>_∗_</sup> -RMSE), and a maximum sustained downward pull sweep ( _F_ max at SR _>_ 90 %). 

### **Metric definitions.** 

- SR: success rate (%), fraction of episodes that traverse _D_ target. 

- SRhard: SR restricted to riser heights ∆ _z ∈_ [0 _._ 22 _,_ 0 _._ 28] m; isolates performance on the most demanding subset of the hard sweep (strict interior, excluding boundary cases at 0.20 and 0.30 m). 

- _Q_ c: mean flatness cost _Qi_ (Eq. (2)) at the elevation-map cell under each foot at touchdown, averaged over all touchdown events. 

- _F_<sup>95</sup> : pct95( _∥Ff ∥/_ ( _mg/_ 2)), 95th-percentile normalized ground reaction force at touchdown events. 

- _Ev_ : velocity-tracking RMSE, ~~�~~ _N_<sup>_−_1�</sup><sup>_N_</sup> _t_ =1<sup>_∥vxy,t −v_cmd</sup><sup>_,t∥_2 (m/s).</sup> 

15 

- _P_ : mean absolute mechanical power, _N_<sup>_−_1�</sup><sup>_N_</sup> _t_ =1<sup>_∥_</sup><sup>**_τ_**</sup><sup>_t ⊙_</sup><sup>**q**˙</sup><sup>_t∥_1 (W);lowervaluesindicatemore</sup> efficient gait [16]. 

- **Foot-target distance** : mean planar Euclidean distance between the executed touchdown centroid and the nearest DCM-planned foothold at swing initiation, averaged over all touchdown events in the episode (the “foot-target distance” reported in §4.1). 

### **D Hardware and Deployment** 

**Sensor architecture.** The actor policy receives a single perceptual stream at runtime: a noisy depth image from a forward-facing RGB-D (color-and-depth) camera. A raycaster-based elevation map mounted at the pelvis is available during training only and is used exclusively by the privileged critic; it is not available at deployment. Additional per-foot proximity rays and a pelvis height sensor supply scalar terrain signals used exclusively in reward computation and privileged critic observations. The simulation models each sensor with geometry-matched raycasters; the depth camera adopts the intrinsics of a RealSense D435 and injects pose domain randomization to bridge the sim-to-real gap. 

**Depth camera processing pipeline.** Raw depth frames are captured at 30 Hz, cropped to remove border artifacts, resized to 30 _×_ 30 px, Gaussian-blurred to suppress raycaster aliasing, and normalized to [0 _,_ 1]. Four temporally spaced frames are stacked into a history buffer and fed to the depth encoder at each 50 Hz control step. Camera intrinsics are matched to a RealSense D435; extrinsic pose domain randomization (table 4) covers mounting uncertainty. The identical pipeline runs at deployment with no modification. 

**Deployment.** The trained actor (depth encoder + policy MLP) is exported to ONNX and executed at 50 Hz on the robot’s onboard computer via a joint-position PD interface. No real-world finetuning is performed; the sim-to-real gap is closed entirely by domain randomization during training. 

### **E Additional Results** 

### **Flat-Terrain Payload Generalization** 

Fig. 7 evaluates payload generalization across three conditions (pelvis +15 kg, pelvis +25 kg, wrist +15 kg) on flat terrain and compares Ours against the Baseline, isolating compliance behavior from terrain traversal difficulty. At moderate load (pelvis +15 kg, wrist +15 kg), Ours maintains 76–79 % SR against the Baseline’s 67–76 % while consuming 9–20 % less power, consistent with compliance training suppressing impulsive GRF recovery. At high centered load (pelvis +25 kg), Ours drops to 47.5 % (below the Baseline’s 60.0 %), indicating that a large CoM shift exceeds the compliance training distribution and causes over-compensation; power remains lower (257 vs. 283 W), confirming the policy still reduces impulsive contacts but can no longer maintain balance. Wrist-mounted mass, which generates a large moment rather than a direct CoM offset, is handled comparably in SR but with a clear power advantage for Ours (186 vs. 231 W), consistent with the arm-extended wrench samples in the disturbance force-field. 


Figure 7: SR (%) and mean power (W) vs. payload mass on flat terrain. 

16 

### **Cross-Embodiment Generalization** 

Fig. 8 shows the ablation evaluated on two platforms (Platform-A (H1-2 class) and Unitree G1) using identical reward weights and hyperparameters, with only the robot asset and joint configuration changed. The relative ordering of variants is preserved across embodiments, supporting the platform-agnostic claim in §6. 


Figure 8: Cross-embodiment ablation on Platform-A (H1-2 class) and Unitree G1: **standard terrain** (top) and **hard terrain, out-of-distribution** (bottom). Identical reward weights and hyperparameters; only robot asset and joint configuration differ. 

### **F Extended Limitations** 

**Adaptive-gait fragility under kinematic stress.** The _Adaptive Gait only_ variant falls _below_ the Baseline on hard terrain (18 % vs. 19 % SR): EMA-smoothed frequency re-timing without terrainquality guidance modifies stance-to-swing departure timing with no corresponding adjustment to the landing target, producing foot-target mismatches that the foothold reward would otherwise suppress. Adaptive gait frequency is therefore an auxiliary capability contingent on accurate foothold guidance, not an independent locomotion primitive, and its benefit is confined to regimes where kinematic margins are non-trivial. A natural remedy is to co-condition the frequency head on the terrain-cost signal so that re-timing decisions are aware of contact quality, or to gate frequency updates on a kinematic feasibility check before committing to the new landing target. 

**Terrain-cost channel redundancy.** Removing any single terrain cost channel leaves foot-target distance within 5 % of the full system (0 _._ 085–0 _._ 093 m vs. 0 _._ 088 m), while removing all three raises it 2 _._ 8 _×_ to 0 _._ 251 m. The channels are thus collectively necessary but individually non-critical, and the manually tuned weighting ( _αQ_ =4 _._ 0, _αE_ =0 _._ 6, _αM_ =6 _._ 0) does not follow from principled minimality. A compressed two-channel formulation and a weight-sensitivity sweep across platforms are left to future work. More broadly, replacing hand-tuned weights with a differentiable meta-learning or Bayesian optimization pass over the cost coefficients could yield principled, platform-adaptive weightings without requiring per-robot re-tuning. 

**Compliance distribution and upper-body coupling.** Near 20 kg of centered CoM shift, two factors compound. First, the spring-damper sampling concentrates on body-attached downward-biased and arm-extended forward-biased scenarios; lateral carry, two-point distributed loads, and dynamically swinging payloads produce wrenches outside this sampled space. Second, the policy controls leg joints only: at high payload masses, upper-body inertia shifts the effective CoM in ways the lower-body policy cannot observe, as the pelvis inertial measurement unit (IMU) and joint encoders provide no direct signal of trunk angular momentum. Together these set the effective payload ceiling. Both failure modes have tractable remedies: broadening the wrench distribution to include lateral 

17 

and multi-point loads during training, and extending the controlled joints to include the torso or arm would directly address the sampling gap and the observability gap respectively. An online payload estimator feeding a residual compliance target could further extend the effective range without requiring a larger wrench training distribution. 

**Tangent-guided orientation failure on slopes.** The Bézier swing reference orients the sole using the arc tangent of the trajectory at the landing point, which on discrete stair steps closely approximates the riser-face normal and drives the foot to land with the sole parallel to the tread. On smooth slopes this mechanism fails: the swing trajectory approaches the inclined surface from above along a path whose touchdown tangent is approximately horizontal, independent of terrain slope angle. The resulting orientation reference does not rotate the sole to match the surface normal, so the foot arrives level on a tilted surface. On ascending grades the surface rises toward the direction of travel, placing the toe geometrically closer to the ground than the heel at the moment of touchdown; the foot therefore contacts toe-first, concentrating GRF on the toe edge. On descending grades the inverse holds, producing heel-first contact with the toe elevated. Both deviate from the designed flat-sole landing, narrow the friction cone, and raise _F_<sup>95</sup> ; on grades above roughly 15<sup>_◦_</sup> the resulting ankle-roll moment is frequently sufficient to trigger fall termination. 

A complementary failure arises in the foothold planner. The flatness cost _Qi_ measures height variance within a local neighbourhood around each candidate cell: a uniformly inclined surface produces near-zero inter-cell variance, so _Qi ≈_ 0 regardless of slope angle, and the planner assigns high contact quality to steep cells. The steepness cost _Ei_ is intended to compensate, but with the current weighting ( _αE_ = 0 _._ 6 vs. _αM_ = 6 _._ 0) it is the weakest channel and is insufficient to steer footholds away from high-gradient cells when flatness and reachability are simultaneously satisfied. The combination of incorrect sole orientation and inadequate slope-avoidance pressure jointly accounts for the observed degradation on slope terrain relative to stairs of comparable height gain per step. A corrected planner would supplement _Qi_ with a surface-normal tilt term and extend the swing orientation reference from the trajectory tangent to the estimated surface normal at the target cell, analogous to normal-aligned foot placement used in model-based planners. 

Additional Bézier-specific failures emerge on slopes. The apex height is set relative to the takeoff elevation; on ascending grades the landing point is higher than take-off by ∆ _z_ = _l_ stride sin _θ_ , reducing effective clearance over the landing surface by the same amount. At steep grades and long strides the foot can contact the slope during mid-swing before the apex is reached, a form of early collision absent on flat terrain and stairs. On descending grades the inverse produces excess apex clearance, which extends swing duration and can desynchronize foot arrival with the DCMtimed stance transition. Addressing both the orientation and clearance failures requires replacing the trajectory-tangent reference with a surface-normal estimate at the target cell (available from the elevation map) and setting the apex height relative to the landing elevation rather than the take-off elevation, a straightforward modification to the existing Bézier parameterization. 

**Elevation-map dependency and terrain scope.** The DCM planner consumes a pelvis-mounted elevation map requiring accurate extrinsic odometry; localization drift degrades foothold selection monotonically with no fallback planner, and the forward-facing depth camera provides no lateral or rearward coverage. Highly deformable surfaces (sand, gravel, foam) violate the rigid-terrain assumption underlying both the Bézier clearance computation and the flatness cost _Qi_ , causing systematic under-clearance, and wet or icy contacts fall outside the domain-randomization friction range ( _µ ∈_ [0 _._ 3 _,_ 1 _._ 6]). Terrain with moving obstacles is not modeled. Robustness to localization drift could be improved by incorporating a fallback stance-hold controller that activates when odometry confidence is low, and by fusing the depth camera into a local elevation map that does not depend on global pose. Extending the friction domain randomization range and adding deformable-terrain simulation (e.g., via compliant contact models in MuJoCo) are the most direct paths to covering low-friction and soft-surface deployments. Handling dynamic obstacles would require integrating a short-horizon obstacle prediction model into the foothold search window. 

18 

