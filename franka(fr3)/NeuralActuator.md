---
title: "NeuralActuator: Neural Actuation Modeling for Robot Dynamics and External Force Perception"
date: "2026-07-13"
authors: "Zhiyang Dou; John U. Onyemelukwe; Hangxing Zhang; Heng Zhang; Minghao Guo; Yunsheng Tian"
url: https://arxiv.org/abs/2607.11734
pdf: https://arxiv.org/pdf/2607.11734
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2607.11734)** / [論文ページ](https://arxiv.org/abs/2607.11734)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# NeuralActuator: Neural Actuation Modeling for Robot Dynamics and External Force Perception 

Zhiyang Dou<sup>1</sup> , John U. Onyemelukwe<sup>1*</sup> , Hangxing Zhang<sup>1*</sup> , Heng Zhang<sup>1</sup> , Minghao Guo<sup>1</sup> , Yunsheng Tian<sup>1</sup> , Michal Piotr Lipiec<sup>1</sup> , Joshua Jacob<sup>1</sup> , Chao Liu<sup>1</sup> , Peter Yichen Chen<sup>1</sup> , Yuri Ivanov<sup>2,</sup><sup>_†_</sup> and Wojciech Matusik<sup>1</sup> 

1MIT 2Amazon Robotics 

**_Abstract_ —Differentiable simulators have advanced policy learning and model-based control across diverse robotic tasks. To date, actuator dynamics remain underexplored and can be a major source of sim-to-real error, especially on low-cost platforms where the linear current-to-joint-torque approximation** _τ_ = _KtI_ **becomes unreliable under commanded-target tracking because of friction, hysteresis, backlash, and thermal effects. Beyond forward dynamics, accurate actuator models also support force perception and integrated force/position control in manipulation tasks. We present NeuralActuator, a neural actuator model that jointly predicts (i) a torque surrogate for trajectory propagation on low-cost servo platforms, (ii) external forces together with a contact-probability gate for sensorless force perception, and (iii) a motor-condition score for the supervised joint, distinguishing normal from mechanically restricted operation. We introduce a twin-arm teleoperation system that collects robot states and actuator telemetry alongside external-force labels, yielding the Neural Actuation Dataset (NAD). The torque-surrogate head is trained through differentiable simulation from pose trajectories without ground-truth joint-torque measurements. A Transformer-based architecture captures temporal dependencies while enabling efficient real-time inference. We validate NeuralActuator across three platforms—a 5-DoF OpenManipulator-X, a 6-DoF SO-101 from LeRobot, and a 7-DoF Franka Emika Panda—spanning three actuator families and costs from approximately $500 to more than $30,000. The low-cost platforms support physically plausible dynamics and enable force evaluation, while the offline Franka experiment provides an additional payload-forceestimation benchmark. We also demonstrate motor-condition estimation and improved behavior-cloning performance when NeuralActuator is used as a pretrained module. We release the dataset, code, and hardware configurations on the project page.** 

## I. INTRODUCTION 

Differentiable simulators [24, 36, 13, 22, 15] enable efficient gradient-based optimization for robot control and robot learning, with substantial advances in modeling rigid-body dynamics and recent extensions to soft bodies and fluids. However, actuator dynamics remain comparatively underexplored. A common control approximation assumes that joint torque scales linearly with current, e.g., _τ_ = _KtI_ . Although reasonable for well-calibrated industrial actuators, this approximation becomes unreliable on cost-effective, servo-driven platforms [4, 40, 35, 41]. These platforms often use mechanically commutated actuators (e.g., coreless brushed DC servo modules) whose hardware simplicity is accompanied by significant non-idealities: gearbox friction, hysteresis, backlash, current saturation, and thermal drift affect joint-side effort. 

> _∗_ These authors contributed equally. Both were research assistants at MIT CDFG. 

> _†_ This work is unrelated to the author’s position at Amazon. 


Fig. 1: **(a) Push–force gauge validation at three end-effector heights.** We show NeuralActuator pushing a force gauge at _low_ , _middle_ , and _high_ end-effector heights (top to bottom). Left: real-robot execution; middle: corresponding simulated rollout; right: contact-axis force-magnitude profiles. The tracelevel mean absolute errors (MAEs) are 0.037 N, 0.015 N, and 0.028 N, respectively. These values correspond to the three representative front-push sequences shown; Tab. VI reports aggregate componentwise force errors across positions, front/top contact directions, and rollout horizons. The shows the predicted magnitude, and the shows the force-gauge ground truth. **(b) Estimated forces for downstream tasks.** NeuralActuator provides online force feedback to behaviorcloning controllers for real-robot object lifting and holding (top) and pick-and-place (bottom) tasks. 

Because the relevant internal friction and transmission states are inaccessible, these time-varying effects resist analytical modeling, resulting in poor effort tracking, unstable impedance behavior, and degraded sim-to-real transfer. 

Beyond accurate modeling, a reliable actuator model also supports _force perception without dedicated force/torque sensors at inference time_ . Recent studies demonstrate torquebased sensing for e-skin–like contact perception [26], proprioceptive estimation in legged robots [14], and force estimation and control in manipulation [29, 19, 9, 52]. Such torque-based methods, however, generally rely on high-quality effort feedback; when it is unavailable on low-cost platforms, an unreliable current–torque mapping undermines analogous force inference. Because physical interaction is fundamentally mediated by force, contact-force prediction can support manipulation without precise geometric models of arbitrary or deformable objects. 

We introduce **NeuralActuator** , a data-driven actuation modeling method for low-cost robot platforms that captures actuator behavior and its coupling with robot dynamics. NeuralActuator is integrated with a differentiable simulator, enabling end-to-end training via gradient-based supervision from real-robot rollouts. NeuralActuator learns a history-dependent mapping from command and state histories together with actuator-side telemetry, including the platform-specific effort signal, voltage, and temperature where available, to torque surrogates, external forces, contact probabilities, and a motorcondition score that distinguishes normal from mechanically restricted operation on the supervised joint. Prior actuator models use torque targets obtained either from joint-torque sensing [25] or from calibrated motor-current estimates [42]; both forms of supervision are difficult to obtain reliably on many low-cost servos. Instead, we supervise the torquesurrogate head using pose trajectories: forward integration through our differentiable dynamics maps the predicted generalized inputs to future configurations, making pose an effective surrogate signal. To capture nonlinear, time-varying actuator effects, NeuralActuator adopts a Transformer architecture that processes recent state-and-command sequences through multihead self-attention, modeling temporal dependencies and interjoint coupling. It outputs per-actuator torque surrogates, external forces, contact probabilities, and motor-condition scores in a multi-task manner. 

To train and benchmark NeuralActuator, we introduce a real-robot dataset capturing actuation, motion, and force signals. We build a twin-arm leader–follower teleoperation system where an operator kinesthetically drives a leader arm to generate diverse trajectories, while the follower executes joint-space commands under closed-loop control. For each trajectory, we log (i) robot states (joint positions, velocities, commanded targets), (ii) actuator telemetry (motor currents, temperature, supply voltage), and (iii) external-force labels. The dataset spans free-space motions and contact-rich manipulation (pushing, pulling, lifting, known-weight loads), covering actuator effects induced by friction, load changes, and intermittent contacts. We release it as the **Neural Actuation Dataset (NAD)** , providing synchronized supervision data for model training and benchmarking. 

We conduct several experiments across three platforms—a cost-effective, servo-driven 5-DoF OpenManipulator-X (four 

revolute joints and a 1-DoF gripper) 1, a 6-DoF SO-101 low-cost arm built on the LeRobot stack [4], and a 7-DoF Franka Emika Panda industrial arm (Sec. IV-F)—spanning three actuator families and costs from approximately $500 to more than $30,000. We evaluate modeling fidelity on the low-cost arms, cross-platform external-force estimation including an offline Franka benchmark, online adaptation, throughput, and downstream real-robot control. On held-out rollouts, NeuralActuator yields low rollout errors (Sec. IV-A), accurate external-force estimates (Sec. IV-B), and accurate motor-condition classification (Sec. IV-G). The evaluated implementation provides sub-millisecond GPU inference at the 60 Hz control rate with a modest parameter footprint (Sec. IV-H). We also evaluate online adaptation using 12 newly collected trajectories (Sec. IV-E). For downstream realrobot control, NeuralActuator provides online force feedback to behavior-cloning policies for object manipulation. We show that learning actuator behavior together with external force perception improves task success rates (Sec. IV-I). Finally, we demonstrate that combining differentiable simulation with silhouette-based image-space supervision provides a visual training signal for NeuralActuator (Sec. IV-J). We summarize our contributions below: 

- A data-driven, differentiable actuator model named **NeuralActuator** that captures actuator behavior and its coupling with robot dynamics via neural torquesurrogate prediction, with additional outputs for external force prediction, contact detection, and motor-condition estimation—enabling force perception without dedicated force/torque sensors at inference time—and a training scheme that leverages differentiable physics without ground-truth joint-torque measurements. 

- A twin-arm teleoperation system for efficient data collection on low-cost arms, time-synchronizing robot proprioception, commanded targets, and actuator-side telemetry. 

- **Neural Actuation Dataset (NAD)** : a real-robot dataset with time-aligned robot states, actuator telemetry, and end-effector external-force labels, enabling training and benchmarking for low-cost actuator modeling. 

- Experiments across three platforms evaluate actuatordynamics modeling, sensorless force estimation, motorcondition estimation, downstream manipulation, and computational efficiency. 

II. RELATED WORK 

## _A. Learning Neural-Augmented Simulation_ 

To close the sim-to-real gap, prior work has augmented analytical simulators with learned residual models; for example, the approach in [1] uses a stochastic RNN to capture residual dynamics and align simulation with reality. Jiang et al. [27] augment a rigid-body simulator with a data-driven contact model that predicts aggregate 3D contact impulses while retaining analytical contact constraints. TossingBot [51] further 

> 1https://emanual.robotis.com/docs/en/platform/openmanipulator <u>x/</u> overview/ 

combines an analytic ballistic prior with a neural residual learned from visual features. NeuralSim [20] embeds neural modules in differentiable simulators to capture unmodeled dynamics and jointly optimizes them with physical parameters on real data; at the component level, Serifi et al. [43] use a Transformer to predict residual state corrections for actuators and rigid bodies from simulated states and interaction forces. Recently, Xu et al. [49] present NeRD, which learns robotspecific dynamics models for predicting future states for articulated rigid bodies under contact constraints. Hwangbo et al. [25] train a supervised actuator network from physicalsystem data and use it in the simulation loop to model each joint of ANYmal; the network maps state histories and position targets to joint torques for simulation. Schwendeman et al. [42] introduce a system identification method that combines a physics model with a neural network to learn residual dynamics, enabling domain-consistent dynamics modeling. In their setting, joint torques are estimated from motor-current measurements. Accordingly, these approaches use torque targets obtained either from joint-torque sensing [25] or from a calibrated current–torque estimate [42]; both forms of supervision are difficult to obtain reliably on many low-cost servo platforms. In contrast, the torque-surrogate head in NeuralActuator requires no direct generalized-effort labels: it is supervised through differentiable simulation using pose trajectories, without assuming reliable current–torque calibration. Concurrently, Fey et al. [12] learn residual corrective torques via reinforcement learning from tracking errors; NeuralActuator instead predicts torque surrogates without assuming a fixed current–torque conversion. 

_a) Learning Actuator Models:_ Existing work mostly targets permanent-magnet electrical machines, using neural models to estimate, control, or emulate electromagnetic torque from electrical states or simulation-derived features [50, 32, 47, 44]. These approaches concern electronically commutated machine models rather than the low-cost integrated coreless DC servo dynamics studied here. Prior work also covers hydraulic actuators [28] and twisted-string actuators [30]. Unlike these efforts, NeuralActuator targets low-cost _coreless DC_ servo actuators, where friction, backlash, saturation, and thermal drift can make the effective current–torque relationship nonlinear and history-dependent. 

## _B. Force Estimation and Proprioceptive Sensing_ 

_a) Torque- and effort-based contact inference:_ A longstanding line of work reconstructs external joint torques from model discrepancies and uses them for collision detection and safe reaction [10, 11, 17]. Building on reliable effort feedback, recent systems further elevate this idea to richer “intrinsic” contact perception (e.g., e-skin–like touch without tactile skins) [26], whole-robot touch sensing without dedicated tactile sensors [14], and learning-based controllers that couple force and motion in manipulation and locomanipulation [29, 52]. These approaches highlight the growing role of actuation as an implicit sensing channel, but they often rely on high-quality torque measurements or well-calibrated 


Fig. 2: **Neural Actuation Dataset (NAD) data collection.** (a) Overview of the twin-arm leader–follower system with an external camera. (b) An operator kinesthetically drives the leader to generate diverse motions; the follower mirrors these motions while manipulating a payload and recording synchronized actuator currents, robot states, and end-effector forces. 

current–torque mappings. 

_b) External force estimation on robot arms:_ For manipulators, a complementary body of work estimates external forces and contacts by explicitly modeling the robot dynamics and attributing residual terms to interaction wrenches. Representative examples include virtual force sensing and contact localization along the robot structure [37, 38], as well as observer and filtering formulations that improve robustness under friction and model uncertainty [23, 33, 18, 31]. Recently, learning has also been used to directly map joint-level proprioception and measured joint torques from sensors to endeffector wrenches in static or quasi-static regimes [39]. Chen et al. [7] leverage differentiable simulation to infer external object properties solely from proprioceptive signals. Despite this progress, most proprioceptive force-estimation methods assume accurate torque feedback, while the setting of low-cost, servo-driven arms remains largely unexplored. A summary is provided in Tab. A21 in the Appendix. 

## III. METHOD 

## _A. Problem Formulation_ 

Consider a robotic manipulator with _na_ arm joints and _nm_ modeled actuator channels, including a gripper channel when applicable. For OpenManipulator-X, _na_ = 4 and _nm_ = 5. Let _τj_<sup>real</sup> denote the physical joint-side effort for actuator channel _j_ (torque for a revolute joint). It depends on the commanded position, effort-related actuator telemetry, state, and operating history: 


where _qj_<sup>cmd</sup> ( _t_ ) is the commanded (goal) position, _qj_ ( _t_ ) and _q_ ˙ _j_ ( _t_ ) are joint position and velocity, and _Vj_ ( _t_ ) and _Tj_ ( _t_ ) denote the supply voltage and thermal state, respectively. The platform-specific signal _uj_ is motor current on OpenManipulator-X, the signed load register on SO-101, and commanded joint torque on Franka. Let **x** _t_ collect the command, proprioceptive state, and actuator telemetry at time _t_ . 


Fig. 3: **NeuralActuator pipeline.** At each time step _t_ , NeuralActuator takes the commanded pose _q_<sup>cmd</sup> ( _t_ ), an effort-related actuator signal _u_ ( _t_ ), actuator-side telemetry, and tracking feedback _e_ ( _t_ ), together with a history buffer _Ht_ that summarizes recent commands, states, and telemetry (e.g., joint poses and velocities). A Transformer encoder ( _×N_ blocks) maps the sequence to four task heads: (i) a torque surrogate **_τ_** , (ii) a raw external-force estimate<sup>ˆ</sup> **f** raw, (iii) a contact-probability gate _g_ , and (iv) a per-motor condition vector **c** . The gated force is<sup>ˆ</sup> **f** = _g_<sup>ˆ</sup> **f** raw. The torque surrogate supplies the simulator’s generalized control input; the simulator then advances the state to time _t_ +1 and updates the history buffer. See Sec. III-B for a discussion of the torque-surrogate and external-force outputs. The torque-surrogate head is trained through _Diff Sim_ from real-robot state transitions. **Right:** High-level schematic of the Transformer and output heads. The implementation uses the pre-normalized gated-attention and GELU encoder blocks specified in the text; the condition branch represents per-motor condition scores, and the separately implemented contact gate is omitted for visual clarity. 

The model used in our experiments takes the eight preceding feature vectors _Ht_ = _{_ **x** _t−_ 8 _, . . . ,_ **x** _t−_ 1 _}_ and appends the current vector **x** _t_ , yielding the nine-token sequence **X** _t_ = ( **x** _t−_ 8 _, . . . ,_ **x** _t_ ). 

In parallel with the learned torque-surrogate output, we predict external forces and motor-condition scores from the same input features: 


where<sup>ˆ</sup> **f**<sup>ext</sup> ( _t_ ) is the predicted end-effector external force. The architecture emits one condition score _cj_ ( _t_ ) per actuator channel. In the OpenManipulator-X condition benchmark, only the Joint 3 component is supervised and evaluated: _c_ 3 estimates the probability of normal operation, and _c_ 3 = 0 denotes the mechanically restricted condition. We do not assign a calibrated probabilistic interpretation to the unsupervised components in this experiment. 

_B. Physical Interpretation through Manipulator Dynamics_ 

We define **f**<sup>ext</sup> as the force exerted by the environment on the robot, matching the sign of the recorded force labels, and write 


Here, _q ∈_ R<sup>_na_</sup> contains the arm coordinates. The quantities _M_ ( _q_ ), _C_ ( _q, q_ ˙) ˙ _q_ , and **g** ( _q_ ) denote the joint-space inertia matrix, 

Coriolis and centrifugal generalized forces, and gravity generalized forces encoded by the simulator, respectively; **_τ_** act denotes the physical joint-side actuator torque. The translational Jacobian _Jv_ ( _q_ ) is evaluated at the force-reference point; using a three-dimensional force rather than a six-dimensional wrench assumes that the residual moment about that point is negligible. The gripper geometry is described separately in Sec. III-E. This convention gives **_τ_** ext = **_τ_** ID _−_ **_τ_** act, which is the residual used by the classical force-estimation baselines. Those methods approximate the actuator term by a linear current–torque model, **_τ_** act = **K** _t_ **i** + **b** , where **K** _t_ = diag( _Kt,_ 1 _, . . . , Kt,na_ ), and map the resulting residual to Cartesian force. On geared low-cost servos, however, friction, backlash, saturation, and thermal drift make this linear map unreliable; its errors therefore contaminate the inferred contact force. 

NeuralActuator predicts a torque surrogate **_τ_**<sup>pred</sup> and an external-force estimate<sup>ˆ</sup> **f**<sup>ext</sup> with dedicated heads. We consider two ways to couple the force prediction to the differentiable rollout. Under _implicit coupling_ , **_τ_**<sup>pred</sup> alone drives the simulated body, while<sup>ˆ</sup> **f**<sup>ext</sup> is directly supervised but is not applied to the differentiable simulator. The torque surrogate may therefore absorb interaction effects needed to reproduce the observed motion. Under _explicit coupling_ ,<sup>ˆ</sup> **f**<sup>ext</sup> is applied at the force-reference point and contributes _Jv_ ( _q_ )<sup>_⊤_ˆ</sup> **f**<sup>ext</sup> alongside **_τ_**<sup>pred</sup> , so the predicted interaction load also enters the state update. The rollout loss accordingly backpropagates through the applied force. Sec. IV-L compares the two coupling choices. 

Independently of force coupling, we consider direct and 

residual parameterizations of the torque surrogate: 


For instance, for the OpenManipulator-X arm joints, **_τ_** base = **K** _t_ **i** _t_ with _Kt_ = 1 _._ 3 N m _/_ A. We use the direct form because it avoids imposing a fixed linear telemetry-to-torque prior, whereas the residual form retains that prior as a nominal anchor. Sec. IV-K compares the two parameterizations. 

## _C. Neural Actuation Dataset (NAD)_ 

To learn the actuator model, we first collect synchronized robot-state, actuator-telemetry, and force data using a twin-arm teleoperation system built on two identical OpenManipulatorX robots [41]. The system consists of a _leader_ arm kinesthetically operated by a human demonstrator and a _follower_ arm that mirrors the leader’s motion while interacting with the environment (Fig. 2). 

The _commanded target joint positions_ sent to the follower’s actuators are set to the leader’s instantaneous joint states. Both arms are equipped with DYNAMIXEL XM430-W350 servos, which provide synchronized actuator-level measurements, including: 

- Joint positions _qj_ ( _t_ ) and velocities _q_ ˙ _j_ ( _t_ ) 

- Motor currents _ij_ ( _t_ ), PWM signals, and bus voltages 

- Coil temperatures _Tj_ ( _t_ ) 

For a subset of interaction trajectories, interaction force is measured with a fixture-mounted six-axis force/torque sensor. We use its three force channels as ground-truth end-effector contact-force measurements **f**<sup>gt</sup> ( _t_ ) _∈_ R<sup>3</sup> ; the three moment channels are not used for supervision. Before training, force labels are transformed into the robot base frame and retain the environment-on-robot sign convention used in Eq. 4. 

All data streams are temporally synchronized and logged per trajectory. For each trajectory of length _T_ , we record timealigned tuples containing (i) robot states (e.g., joint positions, velocities, and commanded targets), (ii) motor currents and actuator-side telemetry, and (iii) end-effector external forces. Together, these streams support pose-based surrogate learning and force estimation. The OpenManipulator-X modeldevelopment and evaluation subset used in our experiments comprises the following three components: 

**Free motion (no external force).** This subset characterizes intrinsic actuator dynamics and provides force-free baselines. We record a diverse set of trajectories (119,933 frames, avg. 20.49 s), including (a) clockwise and counterclockwise circular end-effector motions, (b) individual joint sweeps covering approximately 90% of feasible ranges, and (c) whole-arm primitives such as _lean and extend_ . These trajectories contain no intentional external contact. 

**Force-labeled interactions.** This subset provides force labels via two modalities. _(a) Known-weight loads._ The experimental subset uses payloads with _m ∈{_ 200 _,_ 300 _,_ 400 _,_ 500 _}_ g; the full NAD dataset additionally contains 100 g payload trajectories. During _loaded/grasped_ intervals, we assign the nominal baseframe load **f** grav<sup>gt=</sup><sup>_m_</sup><sup>**g**</sup> base<sup>=[0</sup><sup>_,_0</sup><sup>_, −mg_]</sup><sup>_⊤_.Thisreference</sup> 


Fig. 4: **Data verification in NAD.** We time-synchronize the real-robot video (left) with the logged trajectory and verify alignment in a GUI (right), where the red arrow visualizes the estimated external force. 

is exact for static or quasi-static holding; during motion, it provides nominal supervision that does not account for object inertia or gripping friction. Tasks include _go up and stay still_ (persistent load) and _pick and place_ (intermittent load during grasping), totaling 88,611 frames with an average duration of 21.63 s. _(b) Axis-aligned sensor interactions._ Operators apply controlled push and pull forces along the force sensor’s principal axes ( _±X, ±Y, ±Z_ ). For each force direction, we also record matched no-interaction trajectories that follow the same motion patterns but are executed without physical contact. The measured wrench is transformed into the robot base frame to capture full 3D force components arising from both dominantaxis interactions and kinematic coupling (74,020 frames, avg. 10.50 s). 

We also collect data for the cross-platform evaluation in Sec. IV-F, using an SO-101 arm logged via the LeRobot stack [4] and a 7-DoF Franka Emika Panda industrial arm. Franka provides an additional offline payload-force-estimation benchmark. 


## **Mechanically restricted motor** 

**operation.** In this task, we constrain Joint 3 with rubber bands to introduce additional mechanical 

resistance; see the inset. Under this asymmetric restriction, we collect _pick and place_ trajectories with and without a 200 g payload (49,898 frames, avg. 21.20 s), enabling disentanglement of contact-induced and condition-induced deviations. 

We split the dataset into training, validation, and test sets in an 8:1:1 ratio. All data in NAD are calibrated and humanverified as shown in Fig. 4. See Appendix A for additional details. 

## _D. NeuralActuator_ 

To capture temporal dependencies and nonlinear actuator dynamics, we employ a Transformer encoder that processes recent commands, states, and telemetry to produce multi-task actuator and interaction estimates. In NeuralActuator, the input sequence **X** _t ∈_ R<sup>_L×nf_</sup> stacks per-time-step feature vectors **x** _t ∈_ R<sup>_nf_</sup> . It comprises _H_ hist = 8 historical frames followed by the current frame, so _L_ = _H_ hist + 1 = 9. In the primary low-cost configurations, each **x** _t_ aggregates three families of 


Fig. 5: **Robot arm simulation with external force estimation on the test set.** (a) NeuralActuator estimates end-effector external forces along six directions ( _±X, ±Y, ±Z_ ); red arrows visualize the estimated force vectors in simulation (paired with corresponding real-robot executions). (b) Force estimation during force-aware manipulation: lifting and holding 200 g and 300 g payloads (top) and pick-and-place with 200 g and 300 g payloads (bottom). Additional examples are shown in the accompanying video. 

TABLE I: **OpenManipulator-X model-development and evaluation subset.** The 94.52 minutes sum the taskassignment durations used in the experiments; nominal trajectories reused for motor-condition comparison also appear in the free-motion and force-labeled categories. See Appendix A for a detailed task-level breakdown. 

|**Component**|**Description**|**Duration (min)**|
|---|---|---|
|Free motion|No external force|_∼_34_._15|
|Force-labeled|Known payloads or measured force|_∼_46_._24|
|Motor condition|Mechanically restricted|_∼_14_._13|
|**Total**||_∼_94_._52|


signals—(i) commanded targets ( _q_<sup>cmd</sup> _, qg_<sup>cmd</sup> ), (ii) proprioception ( _q, q, q_ ˙ _g_ ), and (iii) actuator telemetry ( _u_ , _V_ , _T_ )—together with tracking-error features ( _e_ = _q_<sup>cmd</sup> _−q, eg_ = _qg_<sup>cmd</sup> _−qg_ ). All features are normalized before being fed to the network. The Franka experiment uses the platform-specific feature vector described in Appendix B. In simulation, the gripper feature _qg_ is the single-finger prismatic-joint coordinate; it is distinct from the total physical jaw opening _a_ ( _α_ ) in Sec. III-E. 

An input projection and learned positional embeddings initialize **H**<sup>(0)</sup> enc<sup>=</sup><sup>**X**</sup> _t_<sup>**W**</sup> in<sup>+</sup><sup>**P**,where</sup><sup>**W**</sup> in<sup>_∈_R</sup><sup>_nf ×d_and</sup> **P** _∈_ R<sup>_L×d_</sup> . 

We use pre-normalized residual blocks with a querydependent elementwise gate on the attention output. For layer _l_ , 


Here, **W** _g_<sup>(</sup><sup>_l_)</sup><sup>_,_</sup><sup>**W**</sup> _o_<sup>(</sup><sup>_l_)</sup> _∈_ R<sup>_d×d_</sup> , **U**<sup>(</sup><sup>_l_)</sup> **W** _g_<sup>(</sup><sup>_l_)</sup> is produced alongside the query projection, MHA denotes the concatenated perhead attention values before the output projection, and _⊙_ denotes elementwise multiplication. After the final encoder layer and layer normalization, temporal mean pooling yields **h** pool _∈_ R<sup>_d_</sup> . The configuration uses four encoder layers, 

hidden dimension _d_ = 192, four attention heads, and feedforward dimension _d_ ff = 384. Four output heads with SiLU hidden activations predict a torque surrogate, raw force, contact probability, and per-motor condition scores. 

**1. Torque-Surrogate Prediction.** NeuralActuator predicts a torque surrogate as 


where **_τ_**<sup>pred</sup> ( _t_ ) _∈_ R<sup>_nm_</sup> denotes the torque-surrogate output and **X** _t_ = ( **x** _t−_ 8 _, . . . ,_ **x** _t_ ) contains proprioception, commands, and actuator telemetry. For the primary torque-actuated simulators, we use _torque surrogate_ as shorthand for this generalized effort: it is torque-valued on revolute channels and force-valued on a prismatic gripper channel. The Franka configuration instead retains the robot model’s stock affine PD position actuators; on that platform, the corresponding head supplies a simulator-control surrogate rather than a directly torque-valued input. This design accommodates a nonlinear, history-dependent relationship between actuator telemetry and the effective generalized input required by the simulator. The surrogate therefore avoids relying on a fixed linear current– torque prior. 

A single MLP head jointly predicts the surrogate values for all _nm_ actuator channels: **_τ_**<sup>pred</sup> = MLP _τ_ ( **h** pool) _∈_ R<sup>_nm_</sup> , where MLP _τ_ uses SiLU hidden activations. 

**2. External Force Prediction.** We predict end-effector external forces using a two-stage approach that decouples force regression from contact detection. A force-specific hidden feature is first computed from the shared Transformer representation. Separate linear readouts from this feature predict the raw 3D force<sup>ˆ</sup> **f** raw _∈_ R<sup>3</sup> and the contact gate _g ∈_ [0 _,_ 1]. No dedicated force sensor is required at inference time. The gate represents the probability of physical contact, and the final force output is<sup>ˆ</sup> **f** = _g_<sup>ˆ</sup> **f** raw. During training, the gate target is _g_ gt = I[ _∥_ **f** gt _∥_ 2 _> ϵ_ ]. We set _ϵ_ = 0 _._ 01 N solely to distinguish zero from nonzero supervision labels. 

**3. Motor Condition Estimation.** A separate head predicts the per-motor condition vector **c** = _σ_ (MLPcond( **h** pool)) _∈_ [0 _,_ 1]<sup>_nm_</sup> . The OpenManipulator-X benchmark supervises and evaluates only the Joint 3 component from the shared com- 

mand, state, and telemetry history: a value near one indicates normal operation, whereas a value near zero indicates the mechanically restricted condition. The remaining output components are not interpreted as calibrated condition probabilities in this experiment. 

**Differentiable Simulation Integration.** NeuralActuator is integrated with differentiable physics simulators. We embed the model within the simulation loop to enable gradient-based optimization through the system dynamics. When differentiable rendering is enabled, image-space supervision follows the same computational path: the silhouette loss is backpropagated through the renderer, simulated configurations, and differentiable dynamics to the parameters of NeuralActuator. _Forward Dynamics._ At time step _t_ , the torque-surrogate head for the torque-actuated OpenManipulator-X and SO-101 simulators produces **_τ_**<sup>pred</sup> _t_ = _gθ_ ( **X** _t_ ). 

Under implicit force coupling, the simulator advances the state using the predicted surrogate: 


Here, **s** _t_ = [ _qt, q_ ˙ _t_ ] is the simulated joint state. The Franka configuration instead supplies the simulator-control surrogate to its affine PD position actuators, as described above. Offline training and evaluation use the complete time-aligned efforttelemetry sequence recorded with each trajectory; the resulting multi-step evaluations are therefore recorded-telemetryconditioned rollouts rather than forecasts of the actuator response to counterfactual future commands. For online OpenManipulator-X deployment, prediction is strictly causal. At each control cycle, the robot reads the current state and available actuator telemetry, including the live measured current **i** _t_ ; NeuralActuator then estimates the current surrogate, force, and condition scores, and a feedback controller can use<sup>ˆ</sup> **f** _t_ to generate the next command. After inference, **x** _t_ is appended to the history used at the next control cycle; **x** _t_ +1 enters only after the next telemetry packet arrives. Online predictions therefore use no future current measurements. Planning over counterfactual future commands would additionally require a model of the corresponding effort signal. _Gradient Computation._ For _L_ =<sup>�</sup><sup>_T_</sup> _k_ =1<sup>_ℓk_(</sup><sup>**s**</sup><sup>_k_),automatic</sup> differentiation accounts for the effect of **_τ_**<sup>pred</sup> _t_ on **s** _t_ +1 and performs backpropagation through time according to 


The total derivative includes the dependence of the simulatedstate components in **X** _t_ on earlier predictions; consequently, losses at later steps backpropagate to preceding torquesurrogate predictions wherever the simulator sensitivity is nonzero. Equivalently, the Markov state for this recurrence is the augmented state ( **s** _t, Ht_ ); Eq. 13 suppresses the explicit history-buffer component for readability. 

_Model Training._ Since direct generalized-effort labels are unavailable on the low-cost platforms, the torque-surrogate head is supervised through pose trajectories: forward integration converts the predicted generalized inputs into future configurations, making measured poses effective surrogate targets. We use Smooth L1 (Huber) regression losses. The following equations describe the primary OpenManipulatorX configuration. Let Huber _β_ denote the elementwise Huber penalty with transition parameter _β_ , and let _vt,k ∈{_ 0 _,_ 1 _}_ be the optional validity mask for force channel _k_ . The sets _Tf_ and _Tc_ index the input–label pairs used by the force, gate, and condition losses. The regression terms are 


For the OpenManipulator-X prismatic gripper, _κg_ = 1000 converts the single-finger slide-coordinate residual from meters to millimeters before applying the loss. The force loss = uses _βf_ 0 _._ 15 for the force-sensor run and the final known-weight fine-tuning stage, and _βf_ = 1 otherwise. Franka instead supervises only the vertical component with _L_<sup>Franka</sup> force = _|Tf |_<sup>_−_1 �</sup> _t∈Tf_<sup>_wt_Huber0</sup><sup>_._15( ˆ</sup><sup>_ft,z−f_</sup> _t,z_<sup>gt),where</sup> _ft,z_<sup>gt=</sup><sup>_−mg_istheknown-payloadlabel.Thesampleweight</sup> _wt_ implements fixed nonzero-force-sample reweighting. We set _vt,k_ = 1, including for missing-value sentinels converted to zero; configurations that enable invalid-channel masking set the corresponding _vt,k_ = 0. The classification terms are 


where _mt,_ 3 = 1 denotes normal operation of Joint 3 and _mt,_ 3 = 0 denotes the mechanically restricted condition. For selected SO-101 and Franka runs, finite-difference velocities computed from logged poses provide an auxiliary Smooth L1 rollout loss _L_ vel. The complete objective is 


We use _λ_ vel = 5 for the velocity-supervised SO-101 runs and 5 or 10 across the Franka training stages; it is zero otherwise. Unavailable task losses are likewise assigned zero weight. For visual-supervision experiments, the silhouette objective is added to Eq. 19 and backpropagated through the path described above. We train with AdamW [34] for up to 100000 epochs; in practice the best checkpoints emerge within 30000 epochs. Unless otherwise specified, experiments are conducted 


Fig. 6: **Kinematics and force transmission of the symmetric gripper.** Top (a) and side (b) views show the rotary motor driving two symmetric prismatic jaws. Each link transmits an axial force _T_ , whose component along the closing direction gives the per-jaw force _F_ = _T_ cos _β_ . 

on a standard workstation with an Intel Core Ultra 7 265K processor (20 cores, 5.0 GHz), 32 GB of memory, and an NVIDIA GeForce RTX 5080 GPU with 16 GB of VRAM; the no-load benchmark in Appendix B uses an RTX 4090, and the handeye calibration measurements in Appendix C use an A6000. Network training and inference were implemented in JAX with JIT compilation [3] and GPU acceleration, and differentiable simulation for rigid-body dynamics was based on the MuJoCo engine and its MJX JAX implementation [45, 16]. Additional implementation details are provided in the Appendix. 

Because the gripper is driven by a rotary motor while its fingers translate along prismatic joints, relating motor commands to jaw position requires a kinematic mapping. We describe this mechanism next. 

## _E. Gripper Kinematics_ 

Fig. 6 defines the physical gripper geometry. Let _B_ and _B_<sup>_′_</sup> denote the two crank pins, _r_ = _|OB|_ = _|OB_<sup>_′_</sup> _|_ the crank radius, _l_ = _|AB|_ = _|A_<sup>_′_</sup> _B_<sup>_′_</sup> _|_ the link length, _α_ the acute angle between either crank radius and the slider axis, and _δ_ the offset from each slider pin ( _A_ or _A_<sup>_′_</sup> ) to the corresponding inner jaw face. The symmetric jaw aperture is 


Eq. 20 provides the ideal motor-angle-to-jaw-aperture relation for the physical mechanism; the simulator represents the gripper with a calibrated single-finger prismatic coordinate. For a quasistatic symmetric grasp, the links act as two-force members carrying axial force _T_ . If _β_ is the angle between a link and the slider axis, each jaw applies the closing force _F_ = _T_ cos _β_ ; torque balance about the motor axis gives _τ_ = 2 _Tr_ sin _γ_ , where _γ_ = ∠ _OBA_ = ∠ _OB_<sup>_′_</sup> _A_<sup>_′_</sup> . Thus, the gripper’s force transmission depends on both motor torque and mechanism configuration. 

TABLE II: **Gradient behavior across rollout horizons** _H_ **.** Here, input-grad denotes the norm of the loss gradient at the simulator’s generalized-effort input; cos is the parametergradient cosine similarity relative to _H_ = 128. 

|_H_|input-grad|_∥∇θL∥_|cos|
|---|---|---|---|
|64|2_._73_×_10<sup>_−_2</sup>|8.77|0.96|
|128|2_._59_×_10<sup>_−_2</sup>|17.33|1.00|
|256|1_._72_×_10<sup>_−_2</sup>|22.35|0.99|
|320|1_._45_×_10<sup>_−_2</sup>|22.91|0.99|
|500|9_._37_×_10<sup>_−_3</sup>|20.29|0.98|


## IV. EXPERIMENTS 

## _A. Rollout Accuracy_ 

We evaluate the fidelity of our differentiable simulator by comparing predicted trajectories against ground truth on a held-out test dataset. For each joint _j_ at horizon _T_ , we compute the mean absolute error (MAE) across _N_ test trajectories: = <u>1 1</u> MAE _j_ ( _T_ ) _N_ � _Nn_ =1 _T_ � _Tt_ =1�� _qj,t_ ( _n_ )<sup>_−q_ˆ</sup> _j,t_<sup>(</sup><sup>_n_)</sup> ��, where _qj,t_ ( _n_ ) and _q_ ˆ _j,t_<sup>(</sup><sup>_n_)</sup> denote the ground-truth and predicted positions, respectively. Tab. III reports rollout errors across horizons. The model remains accurate over short horizons for both revolute and prismatic joints, and the errors remain moderate over the evaluated longer horizons. Because these experiments replay the recorded current sequence, they evaluate recorded-currentconditioned trajectory propagation rather than counterfactual planning; model-predictive control would additionally require a model of the current response to candidate commands. The consistent trend across joints indicates that physics-inthe-loop learning captures effective history-dependent input– output behavior while retaining the structure of differentiable rigid-body dynamics. Force MAE is the componentwise mean over the evaluated trajectories, time steps, and three Cartesian output channels: MAE _F_ ( _T_ ) = (3 _NT_ )<sup>_−_1 �</sup> _n,t,k_<sup>_|f_</sup> _t,k_<sup>(</sup><sup>_n_)</sup><sup>_−f_ˆ</sup> _t,k_<sup>(</sup><sup>_n_)</sup><sup>_|_.</sup> For payload-based benchmarks, the nominal reference is **f**<sup>gt</sup> = [0 _,_ 0 _, −mg_ ]<sup>_⊤_</sup> , so the metric compares lateral predictions with zero and the vertical prediction with _−mg_ . The directional force-sensor benchmark provides measured three-axis force references. For gauge pushing, the scalar gauge reading is assigned to the known contact axis and the orthogonal reference components are zero; the tabulated F values retain the same three-channel convention, whereas the trace-level values in Fig. 1 use the contact-axis force magnitude. For OpenManipulator-X, Grip denotes single-finger slide-coordinate MAE in millimeters, rather than the total jaw aperture _a_ ( _α_ ). 

Across the rollout horizons _H ∈{_ 64 _,_ 128 _,_ 256 _,_ 320 _,_ 500 _}_ (Tab. II), simulator-input gradient norms remain _O_ (10<sup>_−_2</sup> ), and parameter-gradient cosine similarity remains at least 0.96 relative to _H_ =128; _∥∇θL∥_ plateaus around _H_ =256–320, motivating the curriculum used in training. 

## _B. Force Estimation Accuracy_ 

We evaluate force prediction on three complementary benchmarks: (i) directional contact measured by a calibrated 

TABLE III: **Simulation accuracy on the test set.** J1–J4: jointangle MAE (deg). Grip: single-finger slide-coordinate MAE (mm). Rollouts of 600 steps span approximately 10 seconds at the platform sampling rate. 

|||**@1**|**00 s**|**teps**|||**@3**|**00 s**|**teps**|||**@6**|**00 s**|**teps**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|J1|J2|J3|J4|Grip|J1|J2|J3|J4|Grip|J1|J2|J3|J4|Grip|
|backward<br>forward|2.4|4.3|4.4|4.2|0|2.3|5.9|3.9|4.2|0|3.1|4.8|4.9|4.5|0|
|circular<br>ccw|1.7|5.2|2.2|2.6|0|1.5|3.1|2.0|3.4|0|2.5|2.3|2.1|2.8|0|
|circular<br>cw|3.6|3.2|1.4|2.2|0|3.1|1.9|1.2|2.6|0|2.6|1.7|2.0|2.8|0|
|go<br>up<br>stay<br>still|2.5|1.8|2.3|1.2|0|3.1|2.1|3.1|2.5|0|3.1|1.5|3.5|2.7|0|
|joint<br>sweep<br>1|2.3|2.5|1.8|1.4|0|1.9|1.0|2.6|1.8|0|2.9|1.9|2.0|1.6|0|
|joint<br>sweep<br>2|2.1|4.3|4.6|1.2|0|1.8|6.7|8.4|1.1|0|2.4|4.6|5.2|1.7|0|
|joint<br>sweep<br>3|3.7|4.5|3.1|1.9|0|3.4|2.6|2.8|2.8|0|3.1|2.6|2.5|3.4|0|
|joint<br>sweep<br>4|2.6|4.8|2.5|3.4|0|2.9|3.3|2.4|3.2|0|2.4|2.9|2.2|4.6|0|
|joint<br>sweep<br>5|1.7|3.0|1.7|3.1|0.4|2.6|3.9|2.3|2.7|0.5|5.5|3.3|5.1|3.0|0.7|
|pick<br>place<br>empty|2.6|2.5|2.2|3.5|1.1|1.9|3.6|2.7|3.2|1.1|3.1|2.7|2.0|3.9|1.0|
|Average|2.5|3.6|2.6|2.5|0.2|2.5|3.4|3.1|2.8|0.2|3.1|2.8|3.2|3.1|0.2|


TABLE IV: **Simulation and force prediction accuracy on the force-sensor test set.** J1–J4: joint-angle MAE (deg). Grip: single-finger slide-coordinate MAE (mm). F: force MAE (N). 

||||**@100 **|**step**|**s**||||**@300 **|**step**|**s**||||**@500**|**step**|**s**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|J1|J2|J3|J4|Grip|F|J1|J2|J3|J4|Grip|F|J1|J2|J3|J4|Grip|F|
|||||||_With _|_Exte_|_rnal _|_Force_|_Con_|_tact_||||||||
|force<br>X+|0.9|2.3|0.9|1.6|1.0|0.36|1.1|1.8|2.4|1.3|1.0|0.46|0.9|1.9|2.7|1.7|1.0|0.50|
|force<br>X_−_|1.4|1.1|0.8|1.1|1.0|0.39|1.6|2.3|1.3|2.3|1.0|0.42|2.0|2.9|1.5|3.0|1.0|0.44|
|force<br>Y+|2.3|5.7|2.8|0.6|0.1|0.36|2.1|4.5|2.6|0.9|0.2|0.38|2.7|4.8|2.1|0.9|0.3|0.44|
|force<br>Y_−_|1.4|1.6|3.1|0.5|0.1|0.38|1.5|3.0|3.1|1.3|0.1|0.36|1.4|3.6|3.1|1.5|0.2|0.38|
|force<br>Z+|3.3|6.2|3.3|0.8|0.1|0.39|2.3|5.6|2.5|1.9|0.2|0.43|2.5|4.4|2.2|2.3|0.3|0.46|
|force<br>Z_−_|1.0|5.9|0.6|0.6|1.0|0.36|2.9|6.6|2.8|2.5|1.0|0.64|3.8|6.4|3.5|2.0|1.0|0.57|
|||||||_Refer_|_ence _|_(No _|_Extern_|_al F_|_orce)_||||||||
|force<br>X+|0.6|2.0|1.5|1.2|1.0|0.01|0.8|1.8|1.0|1.1|1.0|0.02|1.0|1.6|1.1|1.1|1.0|0.01|
|force<br>X_−_|2.0|2.5|0.5|1.1|1.0|0.00|1.4|2.3|0.5|1.0|1.0|0.00|1.5|2.2|0.8|1.3|1.0|0.00|
|force<br>Y+|2.0|1.0|2.0|0.6|0.1|0.00|2.1|3.3|2.1|1.1|0.2|0.00|1.9|3.7|1.7|1.1|0.4|0.00|
|force<br>Y_−_|1.0|1.8|1.2|1.3|0.1|0.00|1.6|4.5|2.0|2.2|0.1|0.00|1.2|4.0|2.4|1.6|0.3|0.00|
|force<br>Z+|1.2|1.7|2.1|0.5|0.1|0.00|1.6|3.8|2.2|1.2|0.2|0.00|1.5|2.9|2.0|1.3|0.3|0.00|
|force<br>Z_−_|0.6|2.3|0.9|0.9|1.0|0.02|0.7|1.6|1.1|1.1|1.0|0.01|0.9|1.3|1.0|1.1|1.0|0.01|
|Avg|1.48|2.84|1.64|0.90|0.55|0.19|1.64|3.43|1.97|1.49|0.58|0.23|1.78|3.31|2.01|1.58|0.65|0.23|


six-axis force/torque sensor, (ii) known payloads whose gravitational loads define force labels, and (iii) contact with a force gauge across multiple directions and heights. The experimental setup is shown in Fig. 5. 

**External Force Sensing.** Tab. IV reports 3D external force prediction across six directions ( _±X, ±Y, ±Z_ ), with forces up to 9 N applied at the end-effector. On contact trajectories, the force MAE is 0.36–0.39 N at 100 steps and 0.38–0.57 N at 500 steps. On reference trajectories without contact, NeuralActuator predicts near-zero forces (0.00–0.02 N). Payloads at or below _∼_ 50 g ( _∼_ 0.5 N) lie close to the noise floor of this low-cost platform; reliable detection in this regime remains future work. 

**Payload Benchmark.** Tab. V summarizes force prediction accuracy across payloads and rollout horizons. NeuralActuator achieves an average force MAE of 0.08–0.12 N across tasks and horizons, with single-task errors at most 0.24 N. The goup-and-stay task exhibits relatively larger per-row errors (up to 0.20 N) under sustained static loading. 

**Unseen Contact Geometries.** The force head predicts baseframe end-effector force from the shared telemetry representation and does not take explicit object geometry as input. We therefore 


TABLE V: **Simulation and force prediction accuracy on the payload-based test set.** J1–J4: joint-angle MAE (deg). Grip: single-finger slide-coordinate MAE (mm). F: force MAE (N). 

||||**@**<br>|**100 **<br>|**step**<br>|**s**<br>||||**@300 **<br>|**step**<br>|**s**<br>||||**@600 **<br>|**step**<br>|**s**<br>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**<br>|**Weight**|J1|J2|J3|J4|Grip|F|J1|J2|J3|J4|Grip|F|J1|J2|J3|J4|Grip|F|
|ou|200 g|1.3|5.0|2.6|2.4|0.1|0.12|3.4|3.9|4.2|2.3|0.1|0.10|3.1|3.3|4.3|2.9|0.1|0.16|
|g p<br>andsta|300 g|2.6|5.3|5.7|3.7|0.1|0.20|1.8|3.4|5.7|5.4|0.0|0.17|3.5|2.5|3.4|4.6|0.0|0.20|
||400 g|2.2|4.1|1.4|5.0|0.1|0.07|2.9|2.1|2.1|6.1|0.1|0.12|2.0|1.4|3.0|7.1|0.2|0.11|
||200 g|0.7|3.1|4.3|3.4|1.1|0.24|2.7|3.9|4.0|4.0|1.1|0.08|2.9|5.1|2.9|3.0|1.0|0.11|
|pick an|d<br>300 g|0.5|4.5|3.7|0.9|0.3|0.00|1.2|5.1|4.8|1.5|0.2|0.00|2.7|7.8|4.9|3.2|0.3|0.09|
|place|400 g|0.8|2.1|2.8|2.9|1.1|0.19|2.8|1.4|3.4|3.6|1.1|0.06|2.4|2.0|3.8|3.3|1.0|0.03|
||500 g|2.7|1.8|1.7|3.3|1.1|0.05|4.8|2.8|1.7|2.3|1.1|0.02|4.2|6.3|2.3|2.3|0.9|0.04|
|Avg||1.54|3.70|3.17|3.09|0.56|0.12<br>|2.80|3.23|3.70|3.60|0.53|0.08<br>|2.97|4.06|3.51|3.77|0.50|0.11|


TABLE VI: **Simulation and force prediction accuracy on gauge pushing.** The end-effector contacts the gauge from the front or top at three positions. J1–J4: joint-angle MAE (deg). Grip: single-finger slide-coordinate MAE (mm). F: force MAE (N). 

|**Task**|J1<br>J2|**@100**<br>J3|**steps**<br>J4<br>Grip<br>F|J1<br>J2|**@300**<br>J3|**step**<br>J4|**s**<br>Grip|F|J1|J2|**@600 **<br>J3|**step**<br>J4|**s**<br>Grip|F|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|high<br>push<br>front|0.91 1.68|1.18|0.62 0.00 0.07|1.62 1.29|0.53|0.32|0.00|0.08|1.48|1.16|1.44|1.09|0.00|0.09|
|high<br>push<br>top|0.73 1.01|0.78|1.61 0.01 0.10|1.38 1.35|1.97|1.92|0.01|0.11|1.62|1.57|2.72|2.01|0.01|0.12|
|mid<br>push<br>front|0.66 0.52|0.96|0.61 0.30 0.06|0.85 0.51|0.60|0.99|0.31|0.07|0.95|0.56|0.48|0.98|0.31|0.08|
|mid<br>push<br>top|0.49 0.54|0.87|0.74 0.30 0.09|0.64 0.43|0.73|1.07|0.31|0.10|0.89|0.52|0.75|0.78|0.31|0.11|
|low<br>push<br>front|0.61 0.75|1.83|0.23 0.32 0.08|0.87 0.56|1.65|0.33|0.32|0.09|1.29|0.88|1.12|0.98|0.33|0.10|
|low<br>push<br>top|1.00 0.36|1.05|0.29 0.31 0.08|1.17 0.84|2.11|0.74|0.32|0.09|1.35|0.76|2.27|1.04|0.32|0.10|
|Avg|0.73 0.81|1.11|0.68 0.21 0.08|1.09 0.83|1.27|0.90|0.21|0.09|1.26|0.91|1.46|1.15|0.21|0.10|


evaluate the pretrained model on two unseen objects (inset) whose shapes and surface properties are not represented in training: a 261 g payload and a 226 g payload. We measure the force during the stationary holding phase. Predicted forces are 2.80 N (GT: 2.56 N) and 2.40 N (GT: 2.21 N), indicating some generalization to unseen contact geometries in this setting. **Qualitative Payload Rollouts.** Figs. 7 and 8 show paired hardware executions and simulated rollouts for the two payloadbased manipulation tasks. The force overlays capture contact transitions during pick-and-place and sustained loading during lift-and-hold, complementing the aggregate errors in Tab. V. **Gauge Pushing.** We further test contact with a force gauge from the front (horizontal pushing) and top (vertical pressing) at low, middle, and high end-effector positions. Tab. VI reports state and force errors over 100-, 300-, and 600-step rollouts. Average force MAE increases from 0.08 N at 100 steps to 0.10 N at 600 steps and remains at most 0.12 N for every setting. Joint errors grow moderately with horizon, whereas single-finger slide-coordinate MAE remains approximately 0.21 mm. Fig. 9 shows that the predicted force also tracks contact onset, sustained loading, and release for representative front pushes. 

## _C. Learned Torque Surrogates_ 

Fig. 10 compares torque-surrogate responses with measured motor currents over time for the four revolute joints of OpenManipulator-X. Because the platform lacks joint-torque sensing, the comparison provides a qualitative view of the nonlinear, history-dependent association learned from actuator telemetry; it does not establish a calibrated current–torque relation. 


Fig. 7: **Force-aware pick-and-place rollouts.** From top to bottom: 200 g, 300 g, 400 g, and 500 g payloads. Each row pairs the real execution with the simulated rollout and overlays the predicted end-effector external force. 

## _D. Comparison with Baselines_ 

To compare NeuralActuator with model-based alternatives under a common low-cost-servo input protocol, we implement three adapted baselines on the payload benchmark: (i) _ID-Linear_ , the acceleration-based inverse-dynamics residual **_τ_** ˆ ext = **_τ_** ID( _q, q,_ ˙ ¨ _q_ ) _−_ ( **K** _t_ **_i_** + **b** ) with per-joint _Kt,j_ calibrated on free motion; (ii) _ID-Friction_ , which augments (i) with Stribeck friction and backlash terms; and (iii) the Generalized Momentum Observer ( _GMO_ ) [10], which avoids _q_ ¨ through momentum integration with an auto-tuned gain. The first two are simplified benchmark adaptations and differ from the camera-assisted contact-localization method of Magrini et al. [37] and the measured-motor-torque-based convex friction-uncertainty estimator of Linderoth et al. [31]. All three baselines convert motor current to torque through the linear current–torque map and recover end-effector force as<sup>ˆ</sup> **f** = ( _Jv_<sup>_⊤_)</sup><sup>_†_</sup><sup>**_τ_**ˆ ext;theyconsume</sup><sup>_ground-truth_robotstatesatevery</sup> step, whereas NeuralActuator predicts forces from its own simulated rollout. First, fitting _Kt_ per joint on OpenManipulatorX reveals the limits of the linear assumption: two joints yield negative unconstrained slopes, consistent with high-ratio gearboxes masking the underlying current–torque relation. Second, even after Stribeck and backlash compensation, the mean force MAE of the best adapted classical baseline (GMO) is 5 _._ 5 times that of NeuralActuator (0.66 N vs. 0.12 N). In the no-contact regime, classical methods produce 33–59% false- 

TABLE VII: **Force MAE (N) against model-based sensorless baselines** on the payload benchmark at a 100-step horizon (lower is better). Baselines consume ground-truth states at every step; NeuralActuator uses simulated rollout states. 

|**Method**|**Go **<br>200 g|**Up & S**<br>300 g|**tay**<br>400 g|200 g|**Pick &**<br>300 g|**Place**<br>400 g|500 g|**Avg**|
|---|---|---|---|---|---|---|---|---|
|ID-Linear|1.37|1.81|2.30|0.72|0.95|1.22|1.47|1.41|
|ID-Friction|1.06|1.59|2.15|0.62|0.82|1.10|1.31|1.23|
|GMO [10]|0.58|0.66|1.23|0.33|0.47|0.63|0.75|0.66|
|**NeuralActuator**|**0.12**|**0.20**|**0.07**|**0.24**|**0.00**|**0.19**|**0.05**|**0.12**|


positive contact rates, whereas NeuralActuator remains near zero. Adding Stribeck friction over the linear baseline provides only modest improvement (1.23 versus 1.41 N), indicating that these fixed parametric models do not capture the dominant nonlinearities of the geared servos on this platform. 

## _E. Online Adaptation_ 

When actuator characteristics change across hardware instances or operating conditions, a pretrained model may require local recalibration. Starting from the pretrained checkpoint, we therefore fine-tune NeuralActuator in situ on 12 newly collected trajectories (7,810 frames). The adaptation runs for 70 epochs and takes 356 seconds end-to-end, corresponding to approximately 5.1 seconds per epoch. 

Tab. VIII reports per-joint position, single-finger slide- 


Fig. 8: **Force-aware lift-and-hold rollouts.** From top to bottom: 200 g, 300 g, and 400 g payloads. Each row pairs the real execution with the simulated rollout and overlays the predicted end-effector external force. 


Fig. 9: **Force prediction for front-direction gauge pushing.** For high, middle, and low contact positions, we show the physical setup and simulated scene together with the measured and predicted signed contact-axis force. The bottom panels show the corresponding binary contact interval. 

coordinate, and force errors before (B) and after (A) adaptation on the force-sensor benchmark. Adaptation reduces aggregate position-tracking error across all three rollout horizons, while force MAE remains comparable and improves slightly at the longer horizons. Fig. 11 reports approximately 44% average tracking-error reduction after 70 epochs under the curve-level aggregation used for that progress plot; this statistic is distinct from the horizon-wise Avg rows in Tab. VIII. In this setting, recalibration required 12 trajectories and 356 seconds rather than full retraining. 

## _F. Cross-Platform Validation_ 

For clarity, OpenManipulator-X has four arm joints plus one gripper actuator, SO-101 has five arm joints plus one gripper actuator, and Franka has seven arm joints. The Franka results below report external force only; the SO-101 table reports its arm joints and treats gripper actuation separately. 

## **7-DoF Franka Emika Panda: external-force estimation.** 

The Franka model is command-conditioned: its input contains a target joint pose together with the current state, commanded joint torque, motor-side state, and gripper features. Because the logged commanded-position signal is a sparse sequence of setpoints, the offline feature construction replaces that channel with the smooth proxy **q** ˜<sup>cmd</sup> _t_ = 1 _._ 03 **q**<sup>rec</sup> _t_ +5<sup>, constructed</sup> from the recorded joint positions. Because this proxy depends on a future recorded state, the Franka force results constitute a future-state-conditioned offline benchmark rather than an online evaluation. For causal hardware deployment, this channel must instead be populated by the commanded pose already available at time _t_ from the controller, teleoperation interface, or inverse-kinematics module; no future measured state is then required. Accordingly, the Franka analysis focuses on external-force estimation. The force head is supervised 

TABLE VIII: **Simulation and force prediction accuracy before (B) and after (A) online adaptation.** J1–J4: joint-angle MAE (deg). Grip: single-finger slide-coordinate MAE (mm). F: force MAE (N). 

|||||||**@100 s**|**teps**|||||||||**@3**|**00 step**|**s**||||||||**@**|**50**|**0 step**|**s**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||J1||J|2||J3|J4|Grip|F|J1|||J2|||J3|J|4|Gri|p<br>F<br>J1|||J|2||J3||J|4|Grip|F|
|**Task**|B<br>|A|B||A|B<br>A|B<br>A|B<br>A|B<br>A|B|A<br>|B||A|B||A<br>B|A|B|A<br>B<br>A<br>B|A|B||A|B||A|B|A|B<br>A|B<br>A|
||||||||||||_W_|_it_|_h _|_Exte_|_rna_|_l Fo_|_rce Con_|_tact_||||||||||||||
|force<br>X+|0.9<br>0|.3|2.1||0.7|1.0<br>0.8<br>0|.8<br>0.8|1.0<br>1.0|0.36<br>0.37|2.1<br>|1.2<br>2|.3||1.0|0.|7<br>1|.5<br>0.9|0.8|1.0<br>|1.0<br>0.46<br>0.41<br>2.7|1.6<br>|4.0||1.3<br>|0.|6<br>1|.9|0.9|0.|8<br>1.0<br>1.|0<br>0.52<br>0.41|
|force<br>X_−_|0.2<br>0|.5|1.1||1.7|0.9<br>1.2<br>0|.7<br>1.3|1.0<br>1.0|0.39<br>0.39|1.7<br>|0.7<br>1|.6||1.6|1.|4<br>0|.7<br>0.8|1.2|1.0<br>|1.0<br>0.41<br>0.40<br>2.5|0.9<br>|1.9||1.6<br>|2.|0<br>0|.8|0.9|1.|2<br>1.0<br>1.|0<br>0.42<br>0.41|
|force<br>Y+|2.1<br>1|.8|5.4||3.4|0.8<br>1.1<br>1|.2<br>1.3|0.0<br>0.1|0.37<br>0.37|2.3<br>|1.5<br>4|.5||3.2|1.|1<br>1|.1<br>1.6|1.0|0.1<br>|0.1<br>0.39<br>0.37<br>3.0|1.2<br>|3.7||2.3<br>|2.|5<br>1|.2|3.1|1.|7<br>0.3<br>0.|3<br>0.45<br>0.39|
|force<br>Y_−_|1.1<br>1|.2|0.6||1.3|1.1<br>1.8<br>1|.8<br>1.8|0.1<br>0.1|0.38<br>0.38|1.6<br>|1.0<br>3|.1||2.6|1.|2<br>1|.4<br>2.1|2.0|0.1<br>|0.1<br>0.36<br>0.36<br>1.7|1.0<br>|2.3||2.0<br>|2.|5<br>1|.1|2.1|1.|6<br>0.2<br>0.|2<br>0.38<br>0.37|
|force<br>Z+|2.9<br>4|.0|5.2||3.6|1.3<br>3.1<br>0|.6<br>0.5|0.1<br>0.1|0.39<br>0.39|2.7<br>|2.1<br>4|.0||2.7|1.|4<br>1|.5<br>0.7|0.9|0.2<br>|0.1<br>0.44<br>0.42<br>5.0|1.8<br>|3.2||2.0<br>|1.|7<br>1|.5|1.4|1.|5<br>0.3<br>0.|2<br>0.46<br>0.45|
|force<br>Z_−_|0.7<br>0|.9|6.2||3.5|2.0<br>0.6<br>1|.0<br>0.7|1.0<br>1.0|0.36<br>0.36|2.0<br>|0.7<br>7|.1||2.3|1.|8<br>0|.8<br>3.3|1.2|1.0<br>|1.0<br>0.61<br>0.38<br>2.6|1.0<br>|7.2||1.6<br>|2.|0<br>0|.8|3.0|1.|1<br>1.0<br>1.|0<br>0.54<br>0.40|
||||||||||||_Re_|_fe_|_re_|_nce _|_(No_|_Ext_|_ernal F_|_orce_|_)_|||||||||||||
|force<br>X+|1.4<br>0|.4|1.6||0.4|1.0<br>1.0<br>0|.8<br>0.8|1.0<br>1.0|0.01<br>0.08|1.5<br>|0.5<br>1|.3||0.6|0.|8<br>0|.8<br>1.0|1.2|1.0<br>|1.0<br>0.02<br>0.08<br>1.3|0.5<br>|1.1||0.6<br>|0.|6<br>1|.0|1.4|1.|9<br>1.0<br>1.|0<br>0.01<br>0.05|
|force<br>X_−_|0.4<br>0|.7|3.2||0.6|2.4<br>0.5<br>0|.7<br>1.0|1.0<br>1.0|0.00<br>0.00|0.7<br>|0.6<br>2|.4||1.2|1.|9<br>0|.5<br>0.9|0.9|1.0<br>|1.0<br>0.00<br>0.04<br>0.8|0.6<br>|2.2||1.0<br>|2.|2<br>0|.7|1.1|0.|8<br>1.0<br>1.|0<br>0.00<br>0.05|
|force<br>Y+|1.4<br>1|.8|1.0||2.8|1.4<br>1.4<br>1|.3<br>1.9|0.1<br>0.1|0.00<br>0.00|2.2<br>|1.7<br>3|.3||3.3|1.|0<br>1|.2<br>1.8|1.4|0.2<br>|0.2<br>0.00<br>0.01<br>2.2|1.2<br>|4.4||2.4<br>|1.|0<br>1|.1|1.3|1.|3<br>0.4<br>0.|3<br>0.00<br>0.01|
|force<br>Y_−_|2.0<br>1|.2|2.2||1.9|0.8<br>0.4<br>2|.7<br>1.3|0.0<br>0.1|0.00<br>0.01|2.5<br>|1.5<br>4|.8||2.7|0.|7<br>0|.8<br>3.2|1.8|0.1<br>|0.1<br>0.00<br>0.01<br>2.0|1.2<br>|4.9||2.1<br>|0.|7<br>1|.3|2.7|2.|0<br>0.3<br>0.|2<br>0.00<br>0.01|
|force<br>Z+|0.6<br>0|.9|1.3||0.8|0.4<br>1.3<br>1|.4<br>1.3|0.1<br>0.1|0.00<br>0.00|1.3<br>|1.2<br>3|.4||1.6|0.|4<br>1|.0<br>1.2|1.0|0.2<br>|0.2<br>0.00<br>0.00<br>1.0|1.1<br>|3.4||1.5<br>|0.|5<br>1|.2|0.9|1.|3<br>0.3<br>0.|3<br>0.00<br>0.00|
|force<br>Z_−_|1.8<br>0|.5|1.9||0.8|1.1<br>0.9<br>0|.5<br>0.7|1.0<br>1.0|0.03<br>0.14|1.7<br>|0.6<br>0|.9||0.7|1.|1<br>0|.8<br>0.8|0.8|1.0<br>|1.0<br>0.02<br>0.11<br>1.6|0.5<br>|0.8||0.7<br>|1.|0<br>0|.7|0.8|1.|1<br>1.0<br>1.|0<br>0.01<br>0.08|
|Avg|1.28<br>1|.1|9<br>2.65|1|.81|1.19<br>1.17<br>1|.13<br>1.12|0.55<br>0.55|0.19<br>0.21<br>|1.86<br>1|.09<br>3.|2|2<br>1|.96|1.1|1<br>1.|02<br>1.53|1.1|8<br>0.59<br>0|.58<br>0.23<br>0.22<br>2.20<br>|1.04<br>3|.2|5<br>|1.58<br>1|.4|4<br>1|.1|0<br>1.64|1.3|5<br>0.66<br>0.6|5<br>0.23<br>0.22|


Fig. 10: **Measured motor current and torque-surrogate response for the arm joints.** Two representative rollouts illustrate the learned temporal association; the responses serve as diagnostic outputs rather than direct measurements of motor torque. 

by the known-payload vertical load and operates in parallel with the simulator-control head on the shared Transformer representation. Across 200–600 g lift-and-hold trajectories, the three-component force MAE ranges from 0.26 to 0.42 N. Tab. IX reports the payload-wise results at 100- and 500-step horizons. 

**6-DoF low-cost arm (SO-101).** SO-101 uses STS3215 serialbus servos, extending the cross-platform evaluation beyond the DYNAMIXEL family used in the primary NAD experiments. Its model uses the servos’ signed load registers as the effortrelated input; the raw current registers are not used. The complete SO-101 corpus contains 65,916 frames (1,037.7 s at an aggregate rate of approximately 63.5 Hz) across ten combinations of two tasks and five payload conditions. For a controlled comparison across nonzero payloads, the evaluation subset contains 40,426 frames (649 s, approximately 62.3 Hz) across six combinations: go-up-and-stay and pick-and-place with 300 g, 400 g, and 500 g payloads. At a 500-step horizon, 


Fig. 11: **Online adaptation progress.** The curve-level aggregate shows approximately 44% average tracking-error reduction after 70 epochs with 12 trajectories (7,810 frames). Finetuning takes 356 seconds in total (approximately 29.7 seconds per trajectory and 5.1 seconds per epoch). 


Fig. 12: **Cross-platform validation.** We train NeuralActuator from scratch on a 7-DoF Franka Emika Panda and a 6-DoF SO-101 low-cost arm with STS3215 servos. Franka provides an offline payload-force-estimation benchmark, whereas SO101 provides both rollout and force evaluation. Together with OpenManipulator-X, these robots span three actuator families and costs from approximately $500 to more than $30,000. 

force MAE is 0.47–0.73 N, and the largest joint error is approximately 9 _._ 8<sup>_◦_</sup> on Joint 3 (Tab. X). The larger joint errors relative to OpenManipulator-X may reflect differences in actuator and platform dynamics together with the finite per-platform training set; the short calibration procedure in 

TABLE IX: **Franka Panda external-force output MAE (N)** at 100- and 500-step future-state-conditioned offline rollouts. F averages the three output components against the nominal payload reference [0 _,_ 0 _, −mg_ ]<sup>_⊤_</sup> . Consistent with the verticalloading protocol, training supervision is applied to _fz_ , while the lateral outputs enter the metric through their zero references. 

|**Payload**|**F @100**|**F @500**|
|---|---|---|
|200 g|0.42|0.31|
|300 g|0.35|0.28|
|400 g|0.36|0.27|
|500 g|0.27|0.26|
|600 g|0.30|0.28|
|Avg|0.34|0.28|


TABLE X: **SO-101 per-joint and force MAE** at a 500-step rollout. Joint errors are in degrees and force error (F) is in N. 

|**Task**|J1|**G**<br>J2|**o Up **<br>J3|**& St**<br>J4|**ay**<br>J5|F|J1|**P**<br>J2|**ick &**<br>J3|**Plac**<br>J4|**e**<br>J5|F|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|300 g|2.27|8.20|6.40|5.40|2.37|0.64|3.73|5.63|4.17|6.17|2.47|0.73|
|400 g|2.83|9.30|9.63|4.00|5.73|0.57|3.53|6.83|2.43|5.23|5.13|0.63|
|500 g|2.27|7.63|9.77|7.13|2.67|0.47|3.80|5.60|1.53|6.73|3.33|0.54|


Sec. IV-E provides a practical mechanism for platform-specific refinement. 

## _G. Motor Condition Estimation_ 

Next, we create a controlled mechanical restriction by wrapping rubber bands around Joint 3 to introduce additional resistance (Fig. 13(a)). Under identical position commands, the restricted joint draws more current while following a similar trajectory (Fig. 13(b)). This current deviation enables sensorless classification of the restricted condition. For evaluation, the restricted-class score is 1 _− c_ 3. Under the native decision granularity of each method, NeuralActuator achieves 91.0% accuracy, 96.2% recall, and 0.95 AUC-ROC on a pick-andplace task with a 200 g object (Tab. XI), with higher values than the threshold, SVM, and Random Forest baselines. The task distinguishes unrestricted from mechanically restricted operation and does not address motor-damage diagnosis or general motor-health assessment. 

TABLE XI: **Motor-condition classification under controlled mechanical restriction.** Precision and recall treat the mechanically restricted condition as the positive class. The handcrafted baselines classify overlapping 64-step windows, whereas NeuralActuator uses a nine-frame context and produces framewise predictions. All methods are evaluated on the same four held-out trajectories. 

|**Metric**|Thres.|SVM|RF|**Ours**|
|---|---|---|---|---|
|Accuracy|58.6%|59.9%|67.1%|**91.0%**|
|Precision|0.0%|52.6%|62.3%|**84.5%**|
|Recall|0.0%|31.7%|52.4%|**96.2%**|
|AUC-ROC|0.45|0.62|0.72|**0.95**|


**Baseline Protocols.** The threshold baseline classifies a win- 

Fig. 13: **Motor-condition experiment.** (a) Rubber bands mechanically restrict Joint 3. (b) Under matched commands, the unrestricted and restricted trials follow similar position trajectories (top), but the restricted joint draws more current (middle), producing a measurable difference (bottom). 

dow using the mean absolute Joint 3 current, with the threshold selected on the training set. The SVM uses an RBF kernel, and the Random Forest uses 200 trees with maximum depth 15. Both operate on the same 20 handcrafted features: six current statistics (mean, standard deviation, maximum, minimum, skewness, and kurtosis); three tracking-error statistics (mean, maximum, and standard deviation); four temporal features (mean and maximum current derivative, mean acceleration, and current trend); three spectral features (dominantfrequency power, low-to-high-frequency power ratio, and spectral entropy); three physics-inspired features (current during motion, current-to-velocity ratio, and power estimate); and one first-half-versus-second-half current-asymmetry feature. NeuralActuator is trained on 32 trajectories (eight from each task–condition combination), whereas the three handcrafted baselines are fitted on 16 trajectories (four from each combination). All methods are evaluated on the same four held-out trajectories (two per condition). They classify 64-step windows with 50% overlap, yielding 601 training and 152 test windows; the SVM and Random Forest features are standardized using training-set statistics only. NeuralActuator instead produces a prediction at each time step from its native nine-frame input (eight historical frames plus the current frame) and is evaluated on the same four held-out test trajectories. We therefore compute the metrics at each method’s native decision granularity, with the same four held-out trajectories providing the common evaluation set. 

## _H. Runtime Performance_ 

Tab. XII shows that JAX with JIT compilation yields submillisecond GPU inference latency and throughput above the 60 Hz control rate. Batch processing further improves throughput, and the parameter footprint remains modest. 

TABLE XII: **Model parameters and runtime performance.** 

|_Model Sizes_||_Inf_|_erence_||
|---|---|---|---|---|
|Metric<br>Value|Unit|Metric|Value|Unit|
|Parameters<br>1.44M|–|Mean time|0.25|ms|
|FLOPs (fwd)<br>5.46M|–|P95 time|0.31|ms|
|FP32t<br>550|MiB|Thru. (b=1)|4,019|Hz|
|parameer memory<br>.||Thru. (b=32)|10,992|Hz|


TABLE XIII: **Behavior cloning success rates with NeuralActuator.** Results are averaged over 40 trials. 

|**Task**|**w/o NeuralActuator**|**w/ NeuralActuator**|
|---|---|---|
|Pick-and-Place|80%|**92.5%**|
|Go Up-and-Stay|85%|**95%**|


## _I. Force-Aware Imitation Learning for Real-Robot Control_ 

To evaluate the utility of NeuralActuator as a pretrained force-perception module for downstream control, we train a behavior-cloning (BC) controller using a frozen NeuralActuator module. Following [29], we collect expert demonstrations via teleoperation and train a policy network to predict commanded joint positions (see details in Appendix F). We train the policy using demonstrations with 100 g, 200 g, 300 g, and 500 g payloads, and evaluate on 400 g for object lift-and-hold and 500 g for pick-and-place. The pretrained NeuralActuator module is trained on the full 100–500 g payload set, while the BC demonstrations include the 500 g condition used in the pick-and-place evaluation. The downstream protocol therefore evaluates task-level transfer within the payload range represented during pretraining. **Force-aware policy input.** The BC policy receives a history of joint positions and gripper aperture augmented with the **external force signal** predicted by the frozen NeuralActuator module,<sup>ˆ</sup> **f** ext. This augments position-only control with force feedback under varying payloads and intermittent contacts. The NeuralActuator module remains frozen throughout policy training; it is pretrained on teleoperated NAD trajectories and is not optimized jointly with the downstream policy. **Position-only baseline.** The baseline trains the same policy architecture from the position-andaperture history without the predicted-force input. Tab. XIII shows higher success rates for the force-aware variant than for the position-only baseline in the evaluated manipulation trials (Fig. 1). 

## _J. Visual Supervision_ 

We evaluate an image-space refinement pipeline that composes the neural actuator, differentiable dynamics, forward kinematics, and a differentiable renderer. A geometric threepoint initialization provides the camera-from-base transform _Tcb_ , after which the silhouette objective refines the camera extrinsics and NeuralActuator parameters for the evaluated sequence. Camera intrinsics are estimated with VGGT [46] and held fixed; SAM3 produces the observed robot masks [5]. Following the EasyHeC formulation [6], gradients propagate from mask alignment through the renderer and simulated states 


Fig. 14: **Image-space refinement.** The evaluated pipeline refines the hand–eye transform and NeuralActuator parameters through the simulated robot state; the visualization reports silhouette alignment. 

to NeuralActuator. The resulting silhouette alignment reaches a mean IoU of 0.8515 (Fig. 14); this experiment evaluates alignment quality and does not by itself quantify improvements in actuator or rollout accuracy. Appendix C gives the complete objective and optimization details. 

## _K. Ablation on Torque Parameterization_ 

We compare direct prediction with the residual form in Eq. 5 over full trajectories. On the OpenManipulator-X nogripper tasks, direct prediction reduces the average/worst perjoint MAE from 0 _._ 49<sup>_◦_</sup> _/_ 0 _._ 64<sup>_◦_</sup> to 0 _._ 30<sup>_◦_</sup> _/_ 0 _._ 39<sup>_◦_</sup> . On the SO-101 six-task protocol, the worst per-joint MAE is nearly unchanged (1 _._ 53<sup>_◦_</sup> versus 1 _._ 52<sup>_◦_</sup> ), while force MAE decreases from 0 _._ 38 to 0 _._ 22 N. The residual form offers a nominal effort anchor, but its fixed linear prior appears less well matched to the nonlinear, history-dependent behavior of low-cost servos; we therefore use direct prediction (Tab. XIV). 

## _L. Ablation on Force Coupling_ 

We next compare the implicit and explicit variants on the combined payload benchmarks. Implicit coupling is more accurate on both platforms (Tab. XIV), with a modest difference on OpenManipulator-X and a larger gap on SO-101. Explicit coupling introduces the predicted force as an additional generalized load, as illustrated in Fig. 15. Its sensitivity to calibration mismatch in the simulator—including the forcereference frame, kinematics, and inertial parameters—may leave a load that the torque-surrogate head must counteract, particularly during sustained payload holds. In this paper, we use implicit coupling. 

## _M. Ablation on Network Architecture_ 

To isolate the effect of network architecture, we compare our Transformer against three alternatives with approximately matched parameter counts ( _∼_ 1 _._ 4 M). Let **_x_** _t ∈_ R<sup>_F_</sup> denote the feature vector containing joint states, motor currents, and goals. We consider: (i) an MLP with LayerNorm that predicts the torque surrogate from a flattened history, **_τ_** _t_ = _fθ_ ( **_x_** _t−L_ +1: _t_ ); (ii) a GRU [8], **_h_** _t_ = GRU _θ_ ( **_x_** _t,_ **_h_** _t−_ 1), with a learnable initial state; and (iii) an LSTM [21], ( **_h_** _t,_ **_c_** _t_ ) = 

TABLE XIV: **Torque-parameterization and force-coupling ablations.** Torque-parameterization results use full trajectories: the OpenManipulator-X (OMX) columns give average/worst per-joint MAE on the no-gripper tasks, whereas the SO-101 columns give worst per-joint MAE and mean force MAE over six tasks. For force coupling, the columns give the worst task– joint cell and all-task mean force MAE on the combined payload benchmarks. OMX coupling entries summarize three-seed results as mean (range); for SO-101, the implicit entry uses the released checkpoint, whereas the explicit entry summarizes three from-scratch seeds. 

|**Design choice**|**Variant**|**OMX joint MAE (**<sup>_◦_</sup>**)**|**OMX force MAE (N)**|**SO-101 joint MAE (**<sup>_◦_</sup>**)**|**SO-101 force MAE (N)**|
|---|---|---|---|---|---|
|Torque parameterization|Direct|**0.30 / 0.39**|–|**1.52**|**0.22**|
||Residual|0.49 / 0.64|–|1.53|0.38|
|Force coupling|Implicit|**0.88 (0.84–0.90)**|**0.06**|**2.50**|**0.22**|
||Explicit|1.33 (1.00–1.53)|0.08|6.9 (6.35–7.34)|0.33|


Fig. 15: **Illustration of explicit external-force coupling.** Predicted external forces are applied at the grasp point to illustrate their injection into the differentiable simulation. From left to right, each panel shows no applied force, a downward force, and an upward force; the red arrows indicate the injection direction. The resulting arm motion illustrates the action of the injected generalized load. 

TABLE XV: **Comparison of neural architectures for actuation modeling.** We report rollout and force prediction accuracy at a 500-step prediction horizon. Bold marks the best result per column; ties are bolded jointly. 

|**Model**|J1|J2|J3|J4|Grip|F|
|---|---|---|---|---|---|---|
|MLP|4.55|5.81|3.48|2.16|0.91|0.47|
|GRU|1.83|**2.08**|**1.68**|1.70|**0.65**|0.49|
|LSTM|2.91|7.66|3.21|3.08|0.71|0.41|
|**Ours**|**1.78**|3.31|2.01|**1.58**|**0.65**|**0.23**|


LSTM _θ_ ( **_x_** _t,_ **_h_** _t−_ 1 _,_ **_c_** _t−_ 1). At a 500-step horizon, the Transformer is best or tied for best on four of the six metrics, including force MAE (Tab. XV). 

## _N. Additional Physics Backend_ 

The learned actuator can also be coupled to differentiable rigid-body simulators other than MuJoCo. We integrate NeuralActuator with NVIDIA Warp [36] through a lightweight adapter that maps generalized joint states and control signals between the actuator model and Warp’s articulatedbody simulator. The implementation advances the robot with wp.sim.FeatherstoneIntegrator and records each rollout with wp.Tape() for reverse-mode differentiation. We use a gravitational acceleration of _−_ 9 _._ 81 m _/_ s<sup>2</sup> , an environment rate of 60 Hz, five simulation substeps per frame (300 Hz internally), and a per-joint armature value of 0.01. Fig. 16 shows representative differentiated rollouts under multiple initial configurations and external pushes. 

## V. CONCLUSION 

We presented NeuralActuator, a differentiable neural actuator model for low-cost robots that supports torque-surrogate prediction and contact-gated force perception without dedicated force/torque sensors at inference time. Instead of assuming a fixed linear current–torque relation, NeuralActuator learns a history-dependent mapping from command, state, and telemetry histories to a torque surrogate, while jointly estimating external forces and contact. We provide a twin-arm teleoperation pipeline for collecting force-labeled data and a multi-task Transformer that predicts torque surrogates, forces, contact probabilities, and motor-condition scores; its torquesurrogate head is trained through differentiable simulation without ground-truth joint-torque measurements. Experiments across three platforms spanning three actuator families and costs from approximately $500 to more than $30,000 show accurate motion prediction, force estimation on payload benchmarks, motor-condition estimation, and improved behaviorcloning performance with NeuralActuator. _Limitations and Future Work._ Long-horizon recorded-telemetry-conditioned trajectory propagation accumulates error and eventually degrades tracking accuracy; the few-trajectory online adaptation routine in Sec. IV-E mitigates this drift. 

Online inference also requires live effort-related actuator telemetry. Although causal closed-loop deployment is supported as new telemetry arrives, the current model does not 


Fig. 16: **NeuralActuator with NVIDIA Warp.** Representative articulated-arm rollouts under different initial configurations and external push directions (red arrows), simulated with wp.sim.FeatherstoneIntegrator. 

predict the effort response to unexecuted commands and therefore cannot perform counterfactual rollouts over candidate future command sequences without an additional effort-response model. The force head estimates a single 3D resultant force at the end effector; it neither localizes distributed or multipoint contacts nor estimates a full wrench, and it requires force labels for training. Future work could explore multipoint force prediction and more scalable ways to learn force estimation from visual cues. 

## VI. ACKNOWLEDGMENTS 

This work was conducted as part of the MIT–Amazon Science Hub. We thank Yuxiang Ma and Yuxin Song for assistance with the hardware experiments. We thank the anonymous reviewers for their constructive feedback. 

## REFERENCES 

- [1] Anurag Ajay, Jiajun Wu, Nima Fazeli, Maria Bauza, Leslie P Kaelbling, Joshua B Tenenbaum, and Alberto Rodriguez. Augmenting physical simulators with stochastic neural networks: Case study of planar pushing and bouncing. In _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3066–3073. IEEE, 2018. 

- [2] Seyed Ali Baradaran Birjandi, Johannes K¨uhn, and Sami Haddadin. Observer-extended direct method for collision monitoring in robot manipulators using proprioception and IMU sensing. _IEEE Robotics and Automation Letters_ , 5(2):954–961, 2020. 

- [3] James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula, Adam Paszke, Jake VanderPlas, Skye 

Wanderman-Milne, and Qiao Zhang. JAX: composable transformations of Python+NumPy programs, 2018. URL http://github.com/jax-ml/jax. 

- [4] Remi Cadene, Simon Alibert, Alexander Soare, Quentin Gallouedec, Adil Zouitine, Steven Palma, Pepijn Kooijmans, Michel Aractingi, Mustafa Shukor, Dana Aubakirova, Martino Russi, Francesco Capuano, Caroline Pascal, Jade Choghari, Jess Moss, and Thomas Wolf. LeRobot: State-of-the-art machine learning for real-world robotics in PyTorch. https://github.com/huggingface/ lerobot, 2024. 

- [5] Nicolas Carion, Laura Gustafson, Yuan-Ting Hu, Shoubhik Debnath, Ronghang Hu, Didac Suris, Chaitanya Ryali, Kalyan Vasudev Alwala, Haitham Khedr, Andrew Huang, Jie Lei, Tengyu Ma, Baishan Guo, Arpit Kalla, Markus Marks, Joseph Greer, Meng Wang, Peize Sun, Roman R¨adle, Triantafyllos Afouras, Effrosyni Mavroudi, Katherine Xu, Tsung-Han Wu, Yu Zhou, Liliane Momeni, Rishi Hazra, Shuangrui Ding, Sagar Vaze, Francois Porcher, Feng Li, Siyuan Li, Aishwarya Kamath, Ho Kei Cheng, Piotr Doll´ar, Nikhila Ravi, Kate Saenko, Pengchuan Zhang, and Christoph Feichtenhofer. SAM 3: Segment anything with concepts, 2025. URL https://arxiv.org/abs/2511.16719. 

- [6] Linghao Chen, Yuzhe Qin, Xiaowei Zhou, and Hao Su. EasyHeC: Accurate and automatic hand-eye calibration via differentiable rendering and space exploration. _IEEE Robotics and Automation Letters_ , 8(11): 7234–7241, November 2023. ISSN 2377-3774. doi: 10. 1109/lra.2023.3315551. URL http://dx.doi.org/10.1109/ LRA.2023.3315551. 

- [7] Peter Yichen Chen, Chao Liu, Pingchuan Ma, John Eastman, Daniela Rus, Dylan Randle, Yuri Ivanov, and Wojciech Matusik. Learning object properties using robot proprioception via differentiable robot-object interaction. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5997–6004. IEEE, 2025. 

- [8] Junyoung Chung, Caglar Gulcehre, KyungHyun Cho, and Yoshua Bengio. Empirical evaluation of gated recurrent neural networks on sequence modeling. _arXiv preprint arXiv:1412.3555_ , 2014. 

- [9] Jeremy A Collins, Cody Houff, Patrick Grady, and Charles C Kemp. Visual contact pressure estimation for grippers in the wild. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 10947–10954. IEEE, 2023. 

- [10] Alessandro De Luca and Raffaella Mattone. Sensorless robot collision detection and hybrid force/motion control. In _Proceedings of the 2005 IEEE international conference on robotics and automation_ , pages 999–1004. IEEE, 2005. 

- [11] Alessandro De Luca, Alin Albu-Schaffer, Sami Haddadin, and Gerd Hirzinger. Collision detection and safe reaction with the DLR-III lightweight manipulator arm. In _2006 IEEE/RSJ international conference on intelligent robots and systems_ , pages 1623–1630. IEEE, 2006. 

- [12] Nolan Fey, Gabriel B Margolis, Martin Peticco, and Pulkit Agrawal. Bridging the sim-to-real gap for athletic loco-manipulation. _arXiv preprint arXiv:2502.10894_ , 2025. 

- [13] C. Daniel Freeman, Erik Frey, Anton Raichuk, Sertan Girgin, Igor Mordatch, and Olivier Bachem. Brax - a differentiable physics engine for large scale rigid body simulation, 2021. URL http://github.com/google/brax. 

- [14] Wanjia Fu, Hongyu Li, Ivy X He, Stefanie Tellex, and Srinath Sridhar. UniTac: Whole-robot touch sensing without tactile sensors. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops_ , pages 3976–3985, June 2026. 

- [15] Genesis Authors. Genesis: A generative and universal physics engine for robotics and beyond, December 2024. URL https://github.com/Genesis-Embodied-AI/Genesis. 

- [16] Google DeepMind. MuJoCo XLA (MJX). https:// mujoco.readthedocs.io/en/stable/mjx.html, 2026. Official software documentation, accessed July 13, 2026. 

- [17] Sami Haddadin, Alin Albu-Schaffer, Alessandro De Luca, and Gerd Hirzinger. Collision detection and reaction: A contribution to safe physical human-robot interaction. In _2008 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 3356–3363. IEEE, 2008. 

- [18] Linyan Han, Jianliang Mao, Pengfei Cao, Yahui Gan, and Shihua Li. Toward sensorless interaction force estimation for industrial robots using high-order finite-time observers. _IEEE Transactions on Industrial Electronics_ , 69 (7):7275–7284, 2022. doi: 10.1109/TIE.2021.3095820. 

- [19] Ryo Hanai, Yukiyasu Domae, Ixchel G Ramirez-Alpizar, 

Bruno Leme, and Tetsuya Ogata. Force map: Learning to predict contact force distribution from vision. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3129–3136. IEEE, 2023. 

- [20] Eric Heiden, David Millard, Erwin Coumans, Yizhou Sheng, and Gaurav S Sukhatme. NeuralSim: Augmenting differentiable simulators with neural networks. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9474–9481. IEEE, 2021. 

- [21] Sepp Hochreiter and J¨urgen Schmidhuber. Long shortterm memory. _Neural computation_ , 9(8):1735–1780, 1997. 

- [22] Taylor A Howell, Simon Le Cleac’h, Jan Br¨udigam, J Zico Kolter, Mac Schwager, and Zachary Manchester. Dojo: A differentiable physics engine for robotics. _arXiv preprint arXiv:2203.00806_ , 2022. 

- [23] Jin Hu and Rong Xiong. Contact force estimation for robot manipulator using semiparametric model and disturbance Kalman filter. _IEEE Transactions on Industrial Electronics_ , 65(4):3365–3375, 2018. doi: 10.1109/TIE. 2017.2748056. 

- [24] Yuanming Hu, Luke Anderson, Tzu-Mao Li, Qi Sun, Nathan Carr, Jonathan Ragan-Kelley, and Fr´edo Durand. DiffTaichi: Differentiable programming for physical simulation. _ICLR_ , 2020. 

- [25] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [26] Maged Iskandar, Alin Albu-Sch¨affer, and Alexander Dietrich. Intrinsic sense of touch for intuitive physical human-robot interaction. _Science Robotics_ , 9(93): eadn4008, 2024. 

- [27] Yifeng Jiang, Jiazheng Sun, and C Karen Liu. Dataaugmented contact model for rigid body simulation. In _Learning for dynamics and control conference_ , pages 378–390. PMLR, 2022. 

- [28] Sung-Woo Kim, Buyoun Cho, Seunghoon Shin, Jun-Ho Oh, Jemin Hwangbo, and Hae-Won Park. Force control of a hydraulic actuator with a neural network inverse model. _IEEE Robotics and Automation Letters_ , 6(2): 2814–2821, 2021. 

- [29] Masato Kobayashi, Thanpimon Buamanee, Yuki Uranishi, and Haruo Takemura. ILBiT: Imitation learning for robot using position and torque information based on bilateral control with transformer. _IEEJ Journal of Industry Applications_ , 14(2):161–168, 2025. 

- [30] Hyeokjun Kwon, Sung-Woo Kim, and Hyun-Min Joe. Learning-based force control of twisted string actuators using a neural network-based inverse model. _IEEE Robotics and Automation Letters_ , 9(9):8170–8177, 2024. doi: 10.1109/LRA.2024.3428909. 

- [31] Magnus Linderoth, Andreas Stolt, Anders Robertsson, and Rolf Johansson. Robotic force estimation using motor torques and modeling of low velocity friction disturbances. In _2013 IEEE/RSJ International Conference_ 

_on Intelligent Robots and Systems_ , pages 3550–3556. IEEE, 2013. 

- [32] Hongda Liu, Wentie Niu, and Yonghao Guo. Direct torque control for PMSM based on the RBFNN surrogate model of electromagnetic torque and stator flux linkage. _Control Engineering Practice_ , 148:105943, 2024. doi: 10.1016/j.conengprac.2024.105943. 

- [33] Sichao Liu, Lihui Wang, and Xi Vincent Wang. Sensorless force estimation for industrial robots using disturbance observer and neural learning of friction approximation. _Robotics and Computer-Integrated Manufacturing_ , 71:102168, 2021. 

- [34] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _International Conference on Learning Representations_ , 2019. 

- [35] Tribotix Pty Ltd. PincherX 150 5DOF robot arm. https://tribotix.com/product/pincherx-150-robot-arm/, 2020. Accessed: 2025-08-12. 

- [36] Miles Macklin. Warp: A high-performance Python framework for GPU simulation and graphics. https: //github.com/nvidia/warp, March 2022. NVIDIA GPU Technology Conference (GTC). 

- [37] Emanuele Magrini, Fabrizio Flacco, and Alessandro De Luca. Estimation of contact forces using a virtual force sensor. In _2014 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 2126–2133. IEEE, 2014. 

- [38] Lucas Manuelli and Russ Tedrake. Localizing external contact using proprioceptive sensors: The contact particle filter. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 5062–5069. IEEE, 2016. 

- [39] Jonas Osburg, Ivo Kuhlemann, Jannis Hagenah, and Floris Ernst. Using deep neural networks to improve contact wrench estimation of serial robotic manipulators in static tasks. _Frontiers in Robotics and AI_ , 9:892916, 2022. 

- [40] Interbotix (Trossen Robotics). PhantomX reactor robot arm (AX-12A). https://www.interbotix.com/p/ phantomx-ax-12-reactor-robot-arm.aspx, 2025. Accessed: 2025-08-12. 

- [41] ROBOTIS Co., Ltd. OpenMANIPULATOR-X: Overview (RM-X52-TNM). https://emanual.robotis.com/docs/en/ platform/openmanipulator <u>x/overview/,</u> 2017. Accessed: 2025-07-12. 

   - [44] Mikko Tahkola, Janne Ker¨anen, Denis Sedov, Mehrnaz Farzam Far, and Juha Kortelainen. Surrogate modeling of electrical machine torque using artificial neural networks. _IEEE Access_ , 8:220027–220045, 2020. doi: 10.1109/ACCESS.2020.3042834. 

   - [45] Emanuel Todorov, Tom Erez, and Yuval Tassa. MuJoCo: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026–5033. IEEE, 2012. doi: 10.1109/IROS.2012.6386109. 

   - [46] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. VGGT: Visual geometry grounded transformer. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 5294–5306, 2025. 

   - [47] Songyi Wang and Xinjian Wang. A PINN-based nonlinear PMSM electromagnetic model using differential inductance theory. _Applied Sciences_ , 15(13):7162, 2025. doi: 10.3390/app15137162. 

   - [48] Yufei Wang, David Held, and Zackory Erickson. Visual haptic reasoning: Estimating contact forces by observing deformable object interactions. _IEEE Robotics and Automation Letters_ , 7(4):11426–11433, 2022. 

   - [49] Jie Xu, Eric Heiden, Iretiayo Akinola, Dieter Fox, Miles Macklin, and Yashraj Narang. Neural robot dynamics. In _Proceedings of the 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 3915–3935. PMLR, 2025. URL https: //proceedings.mlr.press/v305/xu25g.html. 

   - [50] Yu-Bai Yan, Jia-Ning Liang, Tian-Fu Sun, Jian-Ping Geng, Gang Xie, and Dong-Jia Pan. Torque estimation and control of PMSM based on deep learning. In _2019 22nd International Conference on Electrical Machines and Systems (ICEMS)_ . IEEE, 2019. doi: 10.1109/ICEMS. 2019.8921886. 

   - [51] Andy Zeng, Shuran Song, Johnny Lee, Alberto Rodriguez, and Thomas Funkhouser. TossingBot: Learning to throw arbitrary objects with residual physics. _IEEE Transactions on Robotics_ , 36(4):1307–1319, 2020. 

   - [52] Peiyuan Zhi, Peiyang Li, Jianqin Yin, Baoxiong Jia, and Siyuan Huang. Learning a unified policy for position and force control in legged loco-manipulation. In _Proceedings of the 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 652–669. PMLR, 2025. 

- [42] Laura Schwendeman, Andrew SaLoutos, Elijah StangerJones, and Sangbae Kim. Improving domain transfer of robot dynamics models with geometric system identification and learned friction compensation. In _2023 IEEERAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pages 1–8. IEEE, 2023. 

- [43] Agon Serifi, Espen Knoop, Christian Schumacher, Naveen Kumar, Markus Gross, and Moritz B¨acher. Transformer-based neural augmentation of robot simulation representations. _IEEE Robotics and Automation Letters_ , 8(6):3748–3755, 2023. 

APPENDIX 

This appendix provides dataset details (Sec. A), implementation details (Sec. B), the visual-supervision formulation (Sec. C), an architecture comparison (Sec. D), a force-sensing taxonomy (Sec. E), and the imitation-learning setup (Sec. F). 

_A. Additional Details of the Neural Actuation Dataset (NAD)_ 

_a) Task Design:_ We collect the Neural Actuation Dataset (NAD) with a twin-arm leader–follower teleoperation system to capture actuator behavior across a broad range of motions, loads, and contact wrenches. Tab. A16 summarizes the task suite, which is organized into three categories. **(i) Free motion** tasks contain no external contact and are used to characterize nominal actuation dynamics under representative workspace motions, including end-effector circular trajectories (clockwise/counterclockwise), per-channel sweeps (actuator channels 1–5), and scripted motion primitives (lean-back/extendforward, pick-and-place without payload, and go-up/holdstill). **(ii) Force-labeled** tasks introduce controlled external wrenches in two ways: (a) _payload_ variants of go-up/hold-still and pick-and-place with task-specific payloads spanning 100– 500 g to induce repeatable gravity loading, and (b) _directional interaction_ trials in _±X_ , _±Y_ , and _±Z_ using an external fixture instrumented with a six-axis F/T sensor. For each directional trial, we additionally record a matched _no-interaction_ counterpart that executes the same commanded motion but without physical contact, enabling paired characterization of contact-induced effects. **(iii) Motor-condition** tasks replicate pick-and-place sequences under nominal and mechanically restricted operation. We randomly split the 10 trajectories for each task instance into training, validation, and test sets in an 8:1:1 ratio. 


Fig. A17: **Data collection hardware.** (a) Twin-arm leader– follower teleoperation setup with a fixed external RGB camera and a fixture-mounted six-axis force/torque (F/T) sensor. (b) Close-up of the F/T sensor mounted on the rigid fixture. (c) Force gauge with a stand. (d) Payload set (100 g, 200 g, 300 g, 400 g, 500 g) used to induce controlled loading during data collection. 


Fig. A18: **Representative data-collection configurations.** Free motion, payload supervision, mechanically restricted operation, and fixture-based force sensing are shown from top to bottom. 

_b) Data Capture Setup:_ Fig. A17 illustrates the collection apparatus. We perform teleoperation in a leader–follower manner: a human operator drives the leader arm, while the follower arm tracks the leader’s motion to execute the corresponding interaction in the physical scene (Fig. A17(a)). To obtain force labels, the target object is mounted on a rigid fixture instrumented with a calibrated six-axis F/T sensor (Fig. A17(b)), which measures the interaction wrench ( _Fx, Fy, Fz, τx, τy, τz_ ). We use only the three translational force channels as learning targets and express them in the robot base frame. For payload-based trials, we additionally attach standardized weights (100–500 g; Fig. A17(d)) to induce repeatable gravity loading. A fixed external RGB camera observes the workspace and records synchronized visual observations. All streams (robot proprioception, F/T readings, and camera frames) are timestamped and time-aligned per trajectory. For reproducibility, we (i) zero the F/T sensor prior to each recording session and after any re-mounting, (ii) keep the camera pose and the sensor–object fixture unchanged throughout a session, and (iii) use a consistent coordinate convention across trials, defining the _±X/±Y/±Z_ interaction directions in the F/T sensor frame. 

_c) Robotic Arm:_ We use two OpenManipulator-X arms with identical kinematic structures to form the leader and follower. Each arm is a 5-DoF platform (4 revolute joints + a 1-DoF parallel gripper) driven by DYNAMIXEL XM430-W350-T motors<sup>2</sup> . The gear ratio of this motor is 353 _._ 5 : 1. The system is powered at 12 V and communicates over a TTL-level multidrop bus; the arms are controlled from a PC via an OpenCR interface. Each arm has a reach of 380 mm, a payload capacity of 500 g, repeatability below 0.2 mm, a maximum joint speed of 46 RPM, and a gripper stroke of 20–75 mm. Using two identical arms reduces kinematic mismatch between demonstration and execution and improves the repeatability of the collected trajectories. 

**Payload-labeled manipulation (SO-101).** Tab. A17 summarizes the SO-101 collection. Following the same protocol as the OpenManipulator-X setup described in the main paper, we collect teleoperated trajectories under known payload conditions ( _m ∈{_ 0 _,_ 200 _,_ 300 _,_ 400 _,_ 500 _}_ g) with two tasks: _go up and stay still_ and _pick and place_ . For each of the 10 task– payload combinations, we record 10 trajectories: eight for training, one for validation, and one for testing. The LeRobot logs contain 65 _,_ 916 frames over 1 _,_ 037 _._ 7 s, corresponding to an aggregate rate of approximately 63 _._ 5 Hz. 

The task breakdown in Tab. A16 contains 350 OpenManipulator-X trajectory assignments across 35 rows. The two nominal motor-condition rows reuse 20 trajectories already listed under free motion and forcelabeled interaction, yielding 330 distinct OpenManipulator-X trajectories. Together with 100 trajectories spanning ten SO- 

101 task–payload combinations, the complete NAD contains 430 distinct trajectories. Individual training and evaluation protocols use task-specific subsets of this broader collection, and collection videos are available for all 430 trajectories. 

_B. Implementation Details_ 

_a) Loss Functions:_ We use robust regression losses for continuous targets and binary cross-entropy for classification targets. Using implementation-specific weights, Eq. 19 can be written as 


For the primary OpenManipulator-X configuration, _L_ pos = _L_ arm + _w_ grip _L_ grip combines Smooth L1 losses on arm joint positions (radians) and the single-finger slide coordinate (millimeters). _L_ force is a Huber loss on the predicted base-frame 3D force. It uses _β_ = 0 _._ 15 for the force-sensor run and the final known-weight fine-tuning stage; _β_ = 1 otherwise. Franka uses a scalar Huber loss with _β_ = 0 _._ 15 on _fz_ alone, supervised by the known-payload label _−mg_ . Nonzeroforce samples receive _w_ focal times the weight of zero-force samples. For the final known-weight fine-tuning stage and the SO-101 runs, the force loss is masked per channel so that only valid labels contribute; other runs supervise all three channels after missing-value sentinels are converted to zero. _L_ gate is a binary cross-entropy loss for contact gating. For the OpenManipulator-X motor-condition task, _L_ cond is binary cross-entropy on the Joint 3 component of the per-motor output. The condition term is used only for motor-condition tasks, where _w_ cond = 100; otherwise _w_ cond = 0. Selected SO101 and Franka runs use finite-difference joint velocities for auxiliary supervision, with _w_ vel = 5 on SO-101 and 5 or 10 across the Franka training stages; it is zero otherwise. The OpenManipulator-X weights are _w_ pos = 100, _w_ grip = 0 _._ 02, _w_ force = 30, _w_ gate = 1, and _w_ focal = 5 (3 for the forcesensor run). SO-101 instead uses one equally weighted sixchannel pose loss over its five arm joints and rotary jaw. Franka uses seven arm-joint weights [1 _,_ 1 _,_ 1 _,_ 1 _,_ 1 _._ 5 _,_ 2 _,_ 1 _._ 5] and replays the recorded position-controlled gripper, so the gripper does not contribute to learning the simulator-control surrogate. Each training step uses the features at time _t_ to advance the simulated state toward _qt_ +1; force, gate, and condition labels are aligned at _t_ +1. The offline force evaluators instead compare the output computed from the time- _t_ features with the force label time-stamped at _t_ , resulting in a one-sample difference in label alignment between training and evaluation. The condition label is constant within each motor-condition trajectory. 

_b) Differentiable Simulation:_ Training uses task-specific truncated rollouts of up to 320 steps. For the primary OpenManipulator-X and SO-101 320-step runs, we begin with 128-step supervision and increase the horizon to 256 and then 320. The no-load runs instead use 128, 192, and 256 steps, motor-condition training remains at 128 steps, and the Franka runs use a fixed 128-step horizon. The simulator uses 

2https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/ 

TABLE A16: **Task Composition of the Dataset.** The dataset consists of free-motion, force-labeled, and motor-condition data. Each task instance contains 10 trajectories, which are randomly split into 8 training, 1 validation, and 1 test trajectory. The two nominal motor-condition rows reuse trajectories listed in the free-motion and force-labeled categories. 

|**Category**|**T**|**ask**|**#Frames**|**Duration (s)**|
|---|---|---|---|---|
||Circular trajectory|Clockwise<br>Counterclockwise|8615<br>8428|147.06<br>143.90|
|||Motor 1|22935|392.04|
|||Motor 2|8688|148.47|
|Free motion<br>|Joint sweep|Motor 3|11357|193.95|
|(No external force)||Motor 4|15012|256.57|
|||Motor 5|7338|125.21|
||Lean back and|extend forward|12261|209.35|
||Pick & pl|ace (empty)|15288|261.08|
||Go up an|d stay still|10011|171.14|
|||100 g|10976|187.61|
||Go up and stay still<br>|200 g|10606|181.26|
||(with weight)|300 g|11259|192.40|
|||400g|11291|192.89|
|||100 g|12483|213.35|
||Pikdl|200 g|13245|226.15|
||c an pace<br>(with weight)|300 g|13129|224.31|
|||400 g|15124|258.54|
|||500g|13957|238.49|
|||+_X_|5005|85.17|
|Force-labeled||+_X_ w/o interaction|5005|85.21|
|||_−X_|5169|87.94|
|||_−X_ w/o interaction|5169|88.00|
|||+_Y_|7444|126.74|
||Forcesensor|+_Y_ w/o interaction|7444|126.78|
|||_−Y_|6921|117.88|
|||_−Y_ w/o interaction|6921|117.91|
|||+_Z_|6906|117.59|
|||+_Z_ w/o interaction|6906|117.63|
|||_−Z_|5565|94.69|
|||_−Z_ w/o interaction|5565|94.73|
||Pick & place|Motor restricted|10113|168.26|
|Motorcondition|w/ weight (200 g)|Nominal motor|13245|226.15|
||Pick & place|Motor restricted|11252|192.41|
||(empty)|Nominal motor|15288|261.08|


|**Category**|**Tas**|**k**|**#Frames**|**Duration (s)**|
|---|---|---|---|---|
||Go up and<br>stay still|Empty<br>200 g<br>300 g<br>400 g|6753<br>7312<br>7227<br>7659|87.5<br>117.4<br>116.1<br>123.0|
|Paload-labeled||500g|7630|122.5|
|y||Empty|6125|98.4|
||Pikd|200 g|5300|85.1|
||c an<br>l|300 g|5553|89.2|
||pace|400 g|5725|92.0|
|||500 g|6632|106.5|


TABLE A17: **SO-101 dataset overview.** 

4 substeps for OpenManipulator-X, 5 for SO-101, and 8 for Franka. For the torque-actuated OpenManipulator-X and 

SO-101 simulators, we use direct torque-surrogate prediction, **_τ_** = _gθ_ ( **X** _t_ ). Under implicit coupling, the torque surrogate alone advances the simulator. Secs. IV-K and IV-L evaluate the residual and explicit alternatives, respectively. The Franka simulator instead retains the stock affine PD position actuators, and the dynamics head supplies their control channels; its raw output is therefore treated as a simulator-control surrogate rather than a direct torque estimate in N m. 

_c) Optimization Schedule:_ The learning rate follows a cosine-annealing schedule from a base rate of 10<sup>_−_4</sup> (5 _×_ 10<sup>_−_5</sup> on SO-101) whose decay horizon is set independently of the 

epoch budget, so extended runs continue at a small floor rate instead of restarting the decay. The known-weight configuration uses staged warm-starts for the no-gripper and forcerefinement stages at 5 _×_ 10<sup>_−_5</sup> and then 5 _×_ 10<sup>_−_6</sup> ; the SO-101 extended configuration is likewise fine-tuned from its scratch run. The three Franka stages use 4 _×_ 10<sup>_−_5</sup> , 1 _._ 2 _×_ 10<sup>_−_5</sup> , and 10<sup>_−_5</sup> , respectively. The training code maintains both raw and exponential-moving-average parameter tracks. 

_d) Franka Feature Configuration:_ The offline Franka force-estimation experiment uses a 52-D input per frame: a seven-joint target pose; current arm positions and velocities; normalized gripper width and goal width; seven commanded torques; motor-side positions and velocities; and seven arm tracking errors plus one gripper error. The recorded commanded-position signal contains only a sparse sequence of stepwise setpoints, so the offline feature construction = substitutes the smooth commanded-pose proxy **q** ˜<sup>cmd</sup> _t_ 1 _._ 03 **q**<sup>rec</sup> _t_ +5 for the target-position channel. The recorded position-controlled gripper is replayed in simulation. Because this offline proxy is constructed from a future recorded position, the Franka force results constitute a future-stateconditioned offline benchmark rather than an online evaluation. In causal deployment, the commanded-pose channel must instead receive the command available at time _t_ from the external controller, teleoperation interface, or inversekinematics module. 

_e) Data and Runtime:_ For the no-load free-motion benchmark, we train on 80 trajectories (8 per task _×_ 10 tasks), split across the no-gripper (8-task) and with-gripper (2-task) runs, with a batch size of 16 (12 for the no-gripper fine-tuning stage). Training converges in approximately 1.5 hours on a single NVIDIA RTX 4090 GPU. 

## _C. Visual Supervision through Differentiable Rendering_ 

We use differentiable silhouette rendering to train NeuralActuator together with the hand–eye transform from image-space alignment. Hand–eye calibration estimates the rigid camerafrom-base transform **T** _cb ∈ SE_ (3) that projects base-frame robot geometry consistently into the image. Following EasyHeC, the visual objective compares rendered and observed robot silhouettes and backpropagates through rendering, kinematics, differentiable dynamics, and the actuator model. The IoU reflects the joint image-space refinement; it does not, by itself, isolate the contribution of the actuator update or establish an improvement in rollout accuracy. 

_a) Supervision signals:_ For each selected frame _i ∈I_ , the following quantities are available. 

**Segmentation mask.** A binary robot silhouette _Mi ∈ {_ 0 _,_ 1 _}_<sup>_H_img</sup><sup>_×W_img</sup> is obtained using SAM3 [5]. This mask provides pixel-level silhouette supervision in the image plane. 

**Camera intrinsics.** A camera intrinsic matrix **K** _i ∈_ R<sup>3</sup><sup>_×_3</sup> is estimated using VGGT and analytically transformed back to the original image coordinate system. Camera intrinsics are treated as fixed during optimization. 

**Camera pose initialization.** An initial estimate of the camera-from-base transformation **T**<sup>(0)</sup> _cb ∈ SE_ (3) is obtained 

via a geometric three-point initialization. This initialization aligns depth-lifted image keypoints with corresponding robot keypoints computed from forward kinematics, and serves as the starting point for differentiable refinement. 

_b) Pose parameterization:_ We parameterize the camera extrinsic transformation in the Lie algebra. Let 


where<sup>�</sup> **_ξ_** _∈_ se(3) is the matrix representation of the twist coordinates and exp( _·_ ) is the matrix exponential. The optimization variable **_ξ_** is initialized by applying the logarithm map to **T**<sup>(0)</sup> _cb_<sup>.</sup> _c) Differentiable actuator rollout and silhouette rendering:_ For a selected frame _i_ at control step _ti_ , NeuralActuator predicts the torque surrogate from the input sequence **X** _ti_ , and differentiable simulation produces **s**<sup>sim</sup> _i_ ( _θ_ ). The offline visual experiment uses the synchronized current sequence recorded with the trajectory, so it is recorded-current-conditioned in the same sense as Sec. III. We use the simulated joint configuration and optionally add a small, regularized per-frame correction ∆ **q** _i_ : 


Forward kinematics then yields each link pose: 


Each link mesh is transformed into the camera frame by **T** _cb_ ( **_ξ_** ) **T**<sup>(</sup> _bl,i_<sup>_l_)andrenderedwithadifferentiablerasterizer,pro-</sup> ducing a soft silhouette **s**<sup>(</sup> _i_<sup>_l_)</sup> _∈_ [0 _,_ 1]<sup>_H_img</sup><sup>_×W_img</sup> . Following EasyHeC, individual link silhouettes are aggregated using saturation: 


yielding the rendered soft robot mask _M_<sup>ˆ</sup> _i ∈_ [0 _,_ 1]<sup>_H_img</sup><sup>_×W_img</sup> . _d) Silhouette alignment objective:_ We minimizeˆ the discrepancy between the rendered soft silhouette _Mi ∈_ [0 _,_ 1]<sup>_H_img</sup><sup>_×W_img</sup> and the observed binary mask _Mi ∈ {_ 0 _,_ 1 _}_<sup>_H_img</sup><sup>_×W_img</sup> : 


_e) Joint visual optimization of camera and NeuralActuator:_ In the visual-training experiment, we jointly optimize the NeuralActuator parameters, camera extrinsics, and optional per-frame state corrections. Small per-frame state corrections absorb residual synchronization, sensing, and geometry errors, and are quadratically regularized: 


Fig. A19: **Visual refinement through differentiable rendering.** Rows show two robot configurations. Columns show the initial alignment, representative optimization snapshots through iteration 239, and the observed segmentation mask. Red denotes the rendered robot silhouette; blue denotes the observed mask. The complete optimization contains 1,845 gradient steps (Tab. A19). 

The visual term is 


Combining the visual term with the trajectory losses in Sec. III, we solve 


We select the positive weights _λq_ and _λ_ visual on the training sequence to balance trajectory fidelity, silhouette alignment, and the magnitude of the state corrections, and then hold them fixed for all frames. Consequently,ˆ gradients from _L_ mask propagate to _θ_ through the chain _Mi →_ FK _→_ **q**<sup>sim</sup> _i →_ DiffSim _→ gθ_ . Because the camera extrinsics and ∆ **q** _i_ are optimized jointly, the silhouette IoU measures the combined refinement and is not an isolated ablation of the actuator update. 

_f) Optimization details:_ We optimize _θ_ , **_ξ_** , and the optional state corrections with first-order gradients and retain the lowest-loss solution. 

_g) Accuracy metrics:_ We evaluate calibration quality with soft intersection-over-union (IoU) between the rendered soft mask _M_<sup>ˆ</sup> _i_ and the observed binary mask _Mi_ : 


_h) Quantitative and qualitative results:_ We report both silhouette alignment accuracy and runtime statistics for joint camera–actuator refinement on a single real-world video sequence. All measurements are conducted on a single NVIDIA A6000 GPU. The evaluation uses six images sampled from a single video; these frames are intentionally non-consecutive and correspond to substantially different robot configurations, providing diverse geometric constraints for calibration. In 

TABLE A18: Silhouette alignment accuracy (IoU) on realworld data. 

|Method|Mean IoU|Std IoU|
|---|---|---|
|Initialization (InitCam + InitRobot)|0.2589|0.0441|
|Robot refinement (InitCam + OptRobot)|0.2974|0.0754|
|Joint refinement (OptCam + OptRobot)|0.8515|0.0065|


TABLE A19: Runtime statistics per sequence on real-world data. 

|Method|Iterations|Total time (s)|
|---|---|---|
|Joint refinement|1,845|180.23|


Tab. A18, _OptRobot_ denotes the optimized robot-side variables: the NeuralActuator parameters _θ_ and, when enabled, the regularized state corrections _{_ ∆ **q** _i}_ . The _Robot refinement_ row keeps the camera fixed, whereas _Joint refinement_ also optimizes the camera extrinsics **_ξ_** . Tab. A18 summarizes silhouette alignment accuracy, while Tab. A19 reports the corresponding runtime statistics. Qualitative visualizations of the joint refinement process at different optimization stages are provided in Fig. A19. 

## _D. Network Architecture Comparison_ 

To isolate the effect of architecture while controlling for capacity, we compare models with a budget of approximately 1.4 million parameters. Hidden widths and layer counts are adjusted to keep the MLP, GRU, LSTM, and Transformer variants within 25% of the Transformer parameter count (Tab. A20). All models use the same training data, target definitions, loss weights, augmentation, and evaluation protocol. Unless noted below, they also use a batch size of 16, AdamW with a weight decay of 10<sup>_−_4</sup> , and a dropout rate of 0.1. Each input contains eight historical samples and the current sample, all sampled at approximately 58.8 Hz. The MLP uses a lower learning rate (3 _×_ 10<sup>_−_5</sup> ) because the larger rate was unstable 

TABLE A20: **Neural architecture configurations for ablation study.** All models are trained with identical loss weights, data augmentation, and early stopping criteria. Parameter counts are matched within 25% of the Transformer baseline. 

|**Model**|**Hidden**|**Latent**|**Params**|**LR**|
|---|---|---|---|---|
|MLP|416|208|1.14M|3_×_10<sup>_−_5</sup>|
|GRU|325|162|1.43M|1_×_10<sup>_−_4</sup>|
|LSTM|275|137|1.44M|1_×_10<sup>_−_4</sup>|
|**Ours**|192|96|1.44M|1_×_10<sup>_−_4</sup>|


Fig. A20: **Payloads used in the high-level control tasks.** 

during differentiable rollouts. NeuralActuator uses four selfattention layers, four heads, hidden dimension 192, feedforward dimension 384, mean pooling, and query-dependent gated attention. Its encoder feed-forward blocks use GELU, while the output heads use SiLU, matching the implementation used in our experiments. 

## _E. Taxonomy of Robotic Force-Sensing Methods_ 

Tab. A21 summarizes representative approaches for robotic force sensing and contact inference, grouped by sensing signals and whether they explicitly estimate force magnitude. Classic sensorless collision monitoring infers external torques from residuals/momentum observers and mainly supports contact detection [10, 11, 17]. Recent intrinsic and wholebody touch methods exploit joint-torque and position sensing, whereas learning-based force-aware policies span lowcost bilateral-control arms and force-sensor-free whole-body robots [26, 14, 29, 52]. For manipulators, virtual force sensing, contact localization, and observer/filter-based methods can estimate interaction forces or localize contacts, generally using torque feedback, commanded torque, or calibrated dynamics [37, 38, 23, 33, 18, 31, 39]. Visual cues can estimate contact-force location and magnitude, whereas inertial-aided proprioceptive methods improve collision monitoring [48, 2]. In contrast, NeuralActuator enables force-magnitude estimation on low-cost servos by learning a torque surrogate from actuation telemetry and jointly predicting external forces without dedicated torque sensors. 

## _F. Imitation Learning_ 

We compare two approaches for training the high-level controller via behavior cloning. For the **position-only baseline** , the per-step observation is **o**<sup>pos</sup> _t_ = [ **q** 1:4 _,t, at_ ]<sup>_⊤_</sup> _∈_ R<sup>5</sup> . The policy receives the eight-step history **O**<sup>pos</sup> _t_ = ( **o**<sup>pos</sup> _t−_ 7<sup>_, . . . ,_</sup><sup>**o**</sup> _t_<sup>pos</sup> ) _∈_ R<sup>40</sup> and minimizes _L_ BC = _∥πψ_ ( **O** _t_<sup>pos</sup> ) _−_ **g** _t_<sup>_∗∥_</sup> 2<sup>2,where</sup> **g** _t_<sup>_∗∈_R5isthedemonstratedcommandforthefourarm</sup> joints and gripper aperture. **Our force-aware controller** augments the input with the estimated end-effector external 


Fig. A21: **Current overload in position-only behavior cloning.** Representative motor-current traces during high-level execution. The position-only baseline exhibits over-current spikes beyond the 1200 mA safety limit, which triggers the onboard protection and terminates the rollout. 

force<sup>ˆ</sup> **f** _t_ predicted by a _pretrained_ NeuralActuator, giving **o**<sup>force</sup> _t_ = [ **q** 1:4 _,t, at,_<sup>ˆ</sup> **f** _t_ ]<sup>_⊤_</sup> _∈_ R<sup>8</sup> and the corresponding eight-step history **O**<sup>force</sup> _t ∈_ R<sup>64</sup> , which replaces **O**<sup>pos</sup> _t_ in the same BC objective. NeuralActuator is trained once on the full payload set _{_ 100 _,_ 200 _,_ 300 _,_ 400 _,_ 500 _}_ g and is kept _frozen_ during policy learning. The BC-policy demonstrations also include the 500 g condition used in the pick-and-place evaluation. The downstream protocol therefore evaluates task-level transfer within the payload range represented during pretraining. For offline force analysis, we compute a trajectory-level statistic on each demonstration-aligned rollout: 


Here, _Tr_ is the rollout length. These offline rollouts replay the synchronized current measured in the corresponding demonstration at every step. Because NeuralActuator does not 

|**Direction**|**Works**|**Signals**|**Force mag.**|**Typical regime**|
|---|---|---|---|---|
|Residual/momentum collision monitoring|[10, 11, 17]|_q,_ ˙_q, τc_ / TS|Partial|Simulation /<br>torque-sensed robots|
|Intrinsic/whole-body touch from proprioception|[26, 14]|TS +_q_|Partial|High-end (torque-capable)|
|Learning-based force-aware policies|[29, 52]|ILBiT: _q,_ ˙_q,_ˆ_τ_;<br>Zhi: state<br>history|Partial / Yes|Low-cost arm / legged robots|
|Arm contact localization / virtual force sensing|[37, 38]|Magrini:<br>RGB-D<br>+_q,_ ˙_q, τ_;<br>Manuelli:<br>_q,_ ˙_q, τ_|Yes / Partial|Torque-capable /<br>calibrated dynamics|
|Observer/filter for sensorless force estimation|[23, 33, 18, 31, 39]|_q,_ ˙_q_ + TS /<br>I_→τ_|Yes|Industrial / Mixed|
|Vision- and inertial-aided force/contact infer-<br>ence|Vision: [48]<br>IMU: [2]|Wang: Vision<br>+_q,_ ˙_q_;<br>Birjandi: IMU<br>+_q_|Yes / Partial|Mixed<br>(observability-dependent)|
|NeuralActuator (ours)|This paper|Telemetry<br>+_q,_ ˙_q_|Yes|Low-cost (servo-driven)|


TABLE A21: **Taxonomy of robotic force sensing and contact inference. Signals:** TS = torque sensing; I _→ τ_ = torque inferred from current/effort; _τ_ ˜ = torque surrogate; _q, q_ ˙ = kinematics; _τc_ = commanded torque; _τ_ ˆ = estimated torque; Vision = exteroception; IMU = inertial sensing. **Force mag.:** _Yes_ = explicit force/wrench magnitude; _Partial_ = mainly detection/localization or residual signals. NeuralActuator predicts _τ_ ˜ from actuation telemetry and estimates external forces on low-cost servos without dedicated torque sensors. 


Fig. A22: **Qualitative results on high-level pick-and-place.** Time-lapse snapshots (left to right) of the robot grasping, lifting, transporting, and placing objects under different payloads. From top to bottom, we evaluate 400 g, 500 g, and a differently shaped 500 g weight. 

predict the current that would result from a counterfactual policy action, _Rf_ is a diagnostic rather than an additional policy-training loss; the policy is optimized with _L_ BC. During hardware execution,<sup>ˆ</sup> **f** _t_ is recomputed causally from telemetry available through time _t_ , including the live current **i** _t_ . Both methods use identical Transformer policies (4 layers, hidden dimension 128, and 4 heads) and are trained for 5,000 epochs on the same demonstrations. For policy training, we use payloads _{_ 100 _,_ 200 _,_ 300 _,_ 500 _}_ g with gripper contact points at approximately matched heights, and evaluate on 400 g and 500 g loads. The position-only baseline can produce current spikes above the 1200 mA safety threshold, triggering onboard protection and terminating the execution early (Fig. A21). 

