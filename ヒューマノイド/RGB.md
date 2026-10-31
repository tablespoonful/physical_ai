---
title: "RGB: RL Guided Whole-Body MPPI for Humanoid Control"
date: "2026-06-23"
authors: "Yunsoo Seo; Sol Choi; Euncheol Im; Myo Taeg Lim; Yisoo Lee"
url: https://arxiv.org/abs/2606.25123
pdf: https://arxiv.org/pdf/2606.25123
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.25123)** / [論文ページ](https://arxiv.org/abs/2606.25123)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RGB: RL Guided Whole-Body MPPI for Humanoid Control** 

Yunsoo Seo, Sol Choi, Euncheol Im, Myo Taeg Lim, Yisoo Lee 

**_Abstract_ — Humanoid robots require whole-body controllers that are both robust and precise in contact-rich environments. While deep reinforcement learning (RL) achieves robust stability, its behavior is tightly coupled to the training objective and command interface, making it difficult to add new feedback objectives without retraining. In this study, we propose an RL guided whole-body model predictive path integral (MPPI) framework that acts as an add-on feedback controller on top of a pretrained RL policy. Instead of using RL policy as the final controller, we use it as a sampling prior that biases MPPI rollouts toward dynamically feasible behaviors. Task objectives are specified through modular MPPI cost terms, and MPPI closes the loop by continuously correcting the RL prior online to satisfy these objectives without retraining the policy. Simulations on a 29-DoF Unitree G1 humanoid in MuJoCo demonstrate stable high-rate control (average 280 Hz). The proposed method improves task-level precision over a pure RL baseline under the same command interface. This is achieved by correcting systematic drift during straight walking and tracking additional whole-body reference signals imposed through the cost.** 

## I. INTRODUCTION 

Humanoid robots are expected to perform sophisticated, complex, and human-like motions while maintaining dynamic balance and ensuring safety in uncertain, contact-rich environments. To achieve these capabilities, prior research has primarily followed two major paradigms: model-based control [1] and learning-based approaches centered on reinforcement learning (RL) [2]. Model-based methods provide interpretability and stability guarantees grounded in system dynamics, whereas learning-based approaches offer adaptability and the ability to handle high-dimensional behaviors. Nevertheless, both paradigms exhibit inherent limitations, making it difficult to develop a unified whole-body control framework that simultaneously achieves high precision, robustness, and strong generalization across diverse tasks and environments. 

In particular, deep RL has demonstrated impressive wholebody locomotion skills with strong stability and adaptability [3]–[5]. By enabling humanoid robots to experience diverse and challenging scenarios in simulation, RL facilitates the acquisition of robust behaviors. However, en- 

*This work was supported by the National Research Foundation of Korea (NRF) grant funded by the Korea government(MSIT) (RS-2024-00339632, RS-2025-25448259). 

Y. Seo, S. Choi, and Y. Lee are with the Center for Humanoid Research, Korea Institute of Science and Technology (KIST), 02792 Seoul, South Korea. Y. Seo is now with University of Texas at Austin, Austin, Texas 78712, USA. S. Choi is also with the Department of Mechanical Engineering, Yonsei University, 03722, Seoul, South Korea 

M. T. Lim is with the School of Electrical Engineering, Korea University, 02841 Seoul, South Korea 

_Corresponding author: Yisoo Lee_ yisoo.lee@kist.re.kr 

hancing robustness through extensive domain randomization and disturbance training often introduces a trade-off, where motion precision and fine-grained control performance may be compromised. 

Furthermore, while RL has achieved remarkable performance in specific tasks, deploying it as a general-purpose whole-body controller remains challenging. Learned policies are inherently shaped by their training objectives and command interfaces. For instance, incorporating additional objectives such as explicit swing foot clearnace modulation or pelvis height regulation to a locomotion policy trained for planar velocity tracking typically accept limited command inputs (e.g., base linear velocity and yaw rate) [6], requires task specific reward redesign and retraining. This results in significant development time and limited scalability across tasks. 

Recent efforts have leveraged human motion data to learn generalized whole-body motion tracking policies via RL [7], [8]. While these approaches broaden the behavioral repertoire, achieving both rapid, highly dynamic motion generation and fine-grained precision in control remains an unresolved challenge. Moreover, RL-based policies do not naturally enforce strict constraint satisfaction, such as torque limits, which is critical for reliable and safe humanoid operation. 

Model-based methods, particularly recent whole-body model predictive control (MPC), offer a structured approach by optimizing composite task objectives online while explicitly enforcing system constraints [9], [10]. Samplingbased MPC methods, such as Model Predictive Path Integral (MPPI) [11], are especially appealing for contactrich humanoid locomotion, as they can optimize non-smooth objectives through parallel rollouts without requiring analytic derivatives [12]–[15]. More recently, physics engine-based predictive control frameworks, including MuJoCo MPC (MJPC) [16], [17], have further improved the practicality of whole-body predictive control by leveraging high-fidelity forward dynamics and efficient rollout computation [18]. 

Despite these advantages, applying sampling-based MPC to high-DoF humanoids remains challenging. In particular, vanilla MPPI is highly sensitive to initialization and sampling distributions. Achieving feasible rollouts and stable performance often requires substantial manual tuning and carefully designed proposal distributions, and performance can still degrade under rapidly changing contact conditions. 

These complementary strengths and limitations motivate a hybrid approach that preserves the robustness of learned locomotion while enabling explicit objective shaping and feedback refinement through predictive control. In this study, 

we propose an RL guided whole-body predictive control framework that uses a pretrained RL policy as a sampling prior within a physics engine-based MPPI. Crucially, our method can be viewed as an add-on, plug-and-play controller, which the base RL policy remains unchanged and continues to provide robust locomotion, while MPPI adds generalized whole-body feedback objectives through modular cost terms. 

The main contributions of this work are as follows: 

- 1) We propose an RL guided whole-body MPPI framework that acts as an add-on feedback controller for a pretrained RL policy. 

- 2) We establish a modular objective formulation that enables flexible task-level command augmentation without modifying or retraining the learned policy. 

- 3) We implement an asynchronous, physics-engine-based MPPI on a 29-DoF humanoid and achieve real-time operation with an average effective update rate of _∼_ 280 Hz in simulation. 

- 4) We demonstrate improved task-level precision over a pure RL baseline under identical command inputs, while preserving robust locomotion from the RL prior. 

## II. BACKGROUND 

## _A. Model predictive path integral (MPPI)_ 

MPPI [12], [19] is a sampling-based stochastic optimal control method that optimizes a control sequence by evaluating a population of perturbed rollouts over a finite prediction horizon. At each control step, the method samples control perturbations, simulates the corresponding trajectories, and aggregates them through an importance-weighted update. In this work, MPPI serves as the model-based predictive controller, which is integrated with a learned policy as a sampling prior. 

We briefly review the standard formulation of MPPI. Consider a discrete-time dynamical system 


where _xt_ denotes the system state at time _t_ , _f_ ( _·_ ) is the discrete-time system dynamics. The control input is decomposed into a nominal signal _ut_ and an gaussian exploration noise term _δu ∼N_ (0 _, νI_ ) that drives the sampling process with covariance _νI_ . The stochastic exploration around _u_ is what later allows us to bias the sampling distribution using RL. 

The control objective is expressed as the minimization of a finite-horizon cost functional 


where **x** = [ _xt, . . . , xT_ ] is the state trajectory, _ϕ_ ( _xT_ ) is a terminal cost, and _l_ ( _xt, ut_ ) is a running cost that encodes the task objective and soft constraints. 

In the path-integral derivation of MPPI, a likelihoodratio term appears when relating the controlled dynamics to an uncontrolled reference process. This change of measure 

naturally introduces a quadratic penalty on the control and leads to an augmented instantaneous cost of the form 


where _R_ is a positive-definite weighting matrix. The additional terms arise from the injected noise _δu_ and recover the usual quadratic effort penalty<sup><u>1</u></sup> 2<sup>_u_T</sup><sup>_Ru_knownfromclassical</sup> optimal control. 

Given this modified running cost, each sampled trajectory _n ∈{_ 1 _, . . . , N }_ accumulates a cost-to-go _S_<sup>˜</sup> _n_ ( **x** ). MPPI then updates the control sequence by computing an importanceweighted average of the sampled perturbations: 


where _δut,n_ is the perturbation applied at time index _t_ for the _n_ -th rollout, _S_<sup>˜</sup> min is the minimum cost among all sampled trajectories, and _λ_ is the inverse temperature parameter controlling how sharply the weighting focuses on low-cost trajectories. Intuitively, rollouts with smaller cumulative cost receive exponentially larger weights, so the updated control is biased toward perturbations that produced more desirable outcomes. 

This sampling-based update has several properties that are particularly relevant for high-dimensional humanoid control. First, the update relies solely on rollout evaluations and does not require derivatives of the dynamics or cost, allowing the incorporation of complex nonlinear models or physics engines. Second, rollouts are independent and can be evaluated in parallel, enabling efficient computation for realtime predictive control. These properties motivate the hybrid framework introduced in the next section, which leverages derivative-free rollouts and parallel computation for wholebody control. 

## _B. Limitations of Vanilla MPPI for Humanoids_ 

Despite its simplicity and derivative-free nature, vanilla MPPI can be brittle for high-dimensional humanoid locomotion. First, MPPI performance depends strongly on the sampling distribution, including the choice of covariance and the mean, which is often set by warm-starting from the previously optimized sequence. Poorly chosen sampling statistics can lead to inefficient exploration, large variance in rollout costs, and convergence to suboptimal local solutions [20], [21]. Second, in contact-rich tasks, dynamically feasible trajectories may occupy only a narrow subset of the state–action space. As a result, many sampled rollouts may violate implicit feasibility (e.g., unstable contact sequences), wasting samples and degrading real-time performance. This sensitivity is characteristic of nonconvex trajectory optimization in high-dimensional systems [22]. Finally, although physics engine-based rollouts enable derivative-free optimization, a large number of samples may still be required 


Fig. 1. Overview of the proposed RL guided whole-body MPPI framework. A pretrained RL policy provides a nominal motion prior for sampling, and knot based MPPI refines it using physics rollouts and modular cost terms as an add-on feedback controller. The refined command is applied immediately upon completion of planning in an asynchronous receding-horizon loop, and a low-level PD controller tracks the joint targets. 

to reliably improve the control sequence under tight realtime constraints, particularly when discontinuous contact transitions are present. 

## III. PROPOSED METHOD 

To address the sensitivity of vanilla MPPI to sampling statistics and initialization in high-dimensional humanoid control, we propose a RL guided whole-body MPPI framework that integrates a learned motion prior with physics engine-based predictive optimization. 

## _A. Overview of the RL Guided MPPI framework_ 

Fig. 1 shows overall structure of the proposed hybrid control framework. The framework combines (a) a pretrained RL policy that provides a motion prior and (b) a knotparameterized MPPI that refines the prior using physicsconsistent rollouts. 

The overall control stack operates at three different rates. First, the RL policy runs at 50 Hz and outputs a nominal joint position reference _q_ RL. Second, the MPPI refines this prior in an asynchronous receding-horizon loop. Once planning finishes, it outputs an updated desired joint command using _q_ RL as the mean of the sampling distribution, yielding an average effective update rate of _∼_ 280 Hz in simulation with CPU-based parallel rollouts. Finally, a low-level joint PD controller runs at 500 Hz, tracking the MPPI-refined desired states ( _qt_<sup>_des_</sup> ) and computing the corresponding desired joint torques Γ<sup>_des_</sup> . These update rates are implementation choices rather than fixed design constraints, and both the RL policy and MPPI modules can operate at higher frequencies depending on computational resources. Further details can be found in the following subsections and Algorithm 1. 

## _B. RL Policy-Based Sample Trajectory Generation_ 

_1) RL policy:_ An RL policy provides a nominal wholebody joint position that serves as a structured sampling prior 

for MPPI. We employ a pretrained humanoid policy, a command velocity tracking locomotion policy, as the prior for the proposed RL guided MPPI. The framework is agnostic to the specific RL algorithm, training procedure, or reward design. Any learned policy that outputs a nominal wholebody command with a compatible action interface can be used. Importantly, the RL policy is trained as a standalone controller, without considering the presence of MPPI, and is assumed to be sufficiently generalized for direct deployment in real robot control. Note that the proposed method does not require training or modification of the policy to integrate it into the predictive control framework. 

_2) RL policy as a sampling prior:_ At each control step, the controller observes the current RL observation _ot_ and the RL policy _π_ RL( _·_ ) outputs a nominal joint position reference _qRL_ . This reference is utilized as the mean of the sample generator in MPPI, around which Gaussian perturbations are applied. 

Note that the command inputs used by the RL policy are shared with MPPI. The same command vector contained in the RL observation _ot_ is used to generate the nominal prior **z** ¯ = _π_ RL( _ot_ ) and is also used consistently during MPPI rollouts so that refinement is performed around the intended commanded behavior of the prior. Additional task objectives are introduced only through MPPI cost terms as task-space references, enabling closed-loop refinement without modifying the RL command interface. 

_3) Knot-based interpolation:_ Directly optimizing a full control sequence over the horizon leads to a high dimensional search space. Thus, we employ knot-based sampling approach [23] which parameterize the MPPI control sequence using _H_ knots. Knot-based interpolation enables the evaluation of continuous and extended trajectories using only a small number of sampled control sequences, thereby improving computational efficiency and exploration effectiveness. 

Specifically, we treat the knot vector **z** = [ _z_ 1<sup>_⊤, . . . , z_</sup> _H_<sup>_⊤_]</sup><sup>_⊤∈_</sup> R<sup>_H×J_</sup> as the optimization variable, where _J_ is the number of actuated joint DoFs and each _zt ∈_ R<sup>_J_</sup> corresponds to a joint-position target at a knot time. At each MPPI update, we sample _H_ knot sequences around the RL mean. Then, we can compose the following equation. 


where policy input _ot_ denotes the observation used during RL training, _ϵ_ represents the sampled joint position target increments at knot nodes, and _ν_ controls the exploration variance around the policy prior. The above equation reconstructs a high-resolution control sequence from the knot representation using cubic interpolation, _U_<sup>(</sup><sup>_k_)</sup> = InterpolateKnots( **z**<sup>(</sup><sup>_k_)</sup> ). This reduces the effective sampling dimension from _T ×N ×J_ to _H×N ×J_ and yields temporally smooth commands, since the full rate time sequence control input is reconstructed by interpolating between knots. The resulting control sequence is then evaluated through rollouts to compute the corresponding trajectory and cost. 

## _C. Physics Engine-based Optimal Solution_ 

_1) Physics Engine-based Rollout:_ MPPI injects Gaussian perturbations according to (5) around the nominal sequence and samples _N_ candidate trajectories in a low-dimensional knot space with _H_ knots. Each candidate is evaluated through forward simulation in the physics engine, and an importanceweighted update is computed based on the resulting task costs. Generated perturbed control propagate rollouts through the forward dynamics 


In our framework, the physics engine acts as a rollout oracle. Given the current state and a candidate control sequence, it performs forward simulation—including contact dynamics—and returns the resulting trajectory and cost. This process does not require analytic Jacobians, explicit dynamics derivations, or backward sensitivity propagation. The derivative-free nature of this approach is particularly advantageous for contact-rich humanoid locomotion, where intermittent contacts and non-smooth transitions make local linearization and gradient-based methods unreliable. 

MPPI naturally supports parallel computation, as each rollout is independent. Accordingly, physics engine-based predictive control frameworks including MJPC evaluate large batches of candidates trajectories in parallel. By combining learning-guided sampling with physics engine-supported parallel rollouts, the proposed framework enables fast and scalable predictive optimization for contact-rich humanoid control. 

_2) Cost-based Optimal Solution Computation:_ For each rollout _n_ , we compute the finite-horizon trajectory cost _S_<sup>(</sup><sup>_n_)</sup> with equations (2) and (6). 


**Algorithm 1** RL-Guided Knot-Based MPPI Overview 


23: **end while** 

The terminal and running costs _ϕ_ and _ℓ_ together constitute a multi-objective cost function, allowing task objectives and constraints to be composed and weighted according to the control requirements. Then the normalized importance weights are described as follows: 


Using the importance weights _w_<sup>(</sup><sup>_n_)</sup> , we compute the refined knot vector **z**<sup>_⋆_</sup> = ¯ **z** +<sup>�</sup><sup>_N_</sup> _n_ =1<sup>_w_(</sup><sup>_n_)</sup><sup>_ϵ_(</sup><sup>_n_). We then interpolate</sup><sup>**z**</sup><sup>_⋆_</sup> to a dense desired joint-position sequence and set _qt_<sup>_des_</sup> to its first element. Only _qt_<sup>_des_</sup> is executed, and the optimization is repeated at the next time step during the receding-horizon. 

_3) Control Input:_ Finally, the desired joint torques are computed using a joint-space PD controller and applied to the robot actuators: 


where _q_ and _q_ ˙ are the measured joint state vectors. The PD gain matrices _Kp_ and _Kd_ are constant diagonal matrices and are identical to those used during policy training. 

“‘latex “‘ 

## _D. Design Rationale_ 

_1) Decoupling Learning from Task Specification:_ The RL policy is trained with a reward function that may not be fully 

aligned with the objectives required at deployment time. Our framework explicitly decouples policy learning from task specification. The RL policy is used solely to shape the sampling distribution and does not act as the control law itself. Task objectives and constraints are instead imposed through modular MPPI cost terms. 

As a result, new tasks can be introduced by modifying the MPPI cost function without retraining or fine-tuning the RL policy. This separation enables flexible task composition while preserving the structured motion prior provided by the learned policy. 

_2) RL Guided Sampling and Sample Efficiency:_ Centering the MPPI sampling distribution on the learned policy _πRL_ biases rollouts toward dynamically feasible whole-body behaviors. This significantly improves sample efficiency in high-dimensional humanoid control, where naive exploration can result in a large number of infeasible or unstable trajectories. 

By leveraging a policy that has already learned stabilizing locomotion or motion patterns, MPPI exploration is concentrated in a structured region of the state–action space, reducing sensitivity to initialization and improving convergence. 

_3) Implicit Contact Handling via Physics Rollouts:_ Contact-rich feasibility is enforced implicitly through physics engine rollouts during MPPI evaluation. In our implementation, contact handling and constraint-consistent state propagation are provided by the simulator during forward simulation. We do not introduce additional hand-crafted contact constraint penalties in the cost function. 

Instead, infeasible contact behaviors naturally incur higher rollout costs due to unstable state evolution, allowing MPPI to reject them through importance weighting. 

## IV. SIMULATION RESULTS 

## _A. System Setup_ 

We evaluate the proposed RL guided whole body MPPI in MuJoCo using a 29 DoF Unitree G1 humanoid model. Rollout evaluation was performed using MJPC, leveraging CPUbased parallel computation. All validations were conducted on a workstation equipped with an Intel Core i9-14900KF CPU, 32 GB RAM, and an NVIDIA GeForce RTX 4070 Ti GPU. 

For the evaluation of the proposed method, a humanoid walking policy that can track command velocity is trained and utilized. While our framework is agnostic to the specific RL algorithm and policy architecture, we employ a policy trained independently in IsaacLab using proximal policy optimization (PPO) [24]. The policy was trained as a standalone controller for direct deployment, without considering integration with the proposed MPPI framework. The reward consisted of command-tracking terms (linear and yaw velocity), regularization terms encouraging smooth actions and joint motions, stability/uprightness and joint-limit penalties, and gait-related terms (e.g., foot air-time and symmetry gait phase). The policy outputs desired joint positions for the 12 lower-body DoFs. Observation includes base angular 

velocity, projected gravity vector, velocity command, joint positions, joint velocities, previous action, and gait phase. 

For the knot-based MPPI, we use _N_ = 128 rollouts with a horizon of 0 _._ 02 s, a control timestep of _dt_ = 0 _._ 002 s (500 Hz), _H_ = 2 spline knot points, and Gaussian exploration noise with standard deviation _σ_ = 0 _._ 2. In all experiments, task objectives are specified by augmenting the MPPI stage cost in equation (7) with task-specific terms, while keeping the pretrained RL policy unchanged. 

## _B. Results_ 

Training a robust whole-body RL policy typically requires substantial reward tuning, and the resulting command interface is often limited. Consequently, incorporating additional objectives outside the original interface usually requires reward redesign and retraining. 

To address this limitation, we evaluate task augmentation with the proposed method.The pretrained locomotion policy is kept unchanged and used as a robust motion prior, while MPPI augments the behavior by adding task objectives through cost terms and refining the prior in closed loop. This closed-loop refinement compensates systematic tracking errors online, improving task-level precision while preserving the robust locomotion behavior of the learned policy. 

As representative tasks, we consider straight-walk drift suppression and base-height regulation for a squat motion. The straight-walk task regulates lateral position and heading to mitigate drift induced by symmetry-breaking bias under a zero yaw command. The squat task evaluates whether an explicit whole-body posture objective can be imposed through cost augmentation alone. 

_a) Straight-walk drift suppression:_ We first evaluate walking velocity tracking under the same command interface used for RL training, commanded _x_ and _y_ velocity and angular velocity around _z_ -axis. In practice, learning a symmetry consistent locomotion policy is often challenging even when trained with symmetric observations and rewards, the resulting policy can exhibit a persistent left-right bias due to stochastic optimization, contact discontinuities. As a consequence, a pure RL baseline may fail to straight walk under a zero angular velocity command, drifting or gradually turning despite, the yaw reference is zero ( _ψ_ des = 0). To isolate the benefit of the proposed controller, we use a pretrained RL policy that exhibits this straight-line tracking deficiency and verify whether MPPI refinement can suppress the bias without retraining. In this experiment, the same locomotion command ( _vx_<sup>_des_</sup> _, vy_<sup>_des_</sup> _, ψ_<sup>_des_</sup> ) = (1 _,_ 0 _,_ 0) is provided to both the RL policy and the MPPI rollouts, so the nominal behavior remains that of the original velocitytracking policy. MPPI then augments this behavior by adding an extra task objective through the cost term _ℓ_ , forming a task-space feedback loop that reduces drift while preserving robust locomotion. 

Specifically, we add a straight-walk objective that penalizes both lateral drift and heading drift: 


Fig. 2. Straight walking performance comparison between pure RL and RL guided MPPI. 

Where _y_ des is set to the initial base lateral position and _βy, βψ_ is a scalar weight used as 25. Here, we only use the running cost _ℓ_ accumulated over the finite-horizon, and we do not include an explicit terminal cost, _ϕ x_<sup>(</sup> _H_<sup>_n_)</sup> . No additional � � cost terms are used beyond those defined in _ℓ_ . When _ℓ_ is not evaluated for planning, the system reverts to the pretrained RL policy alone. 

Fig. 2 summarizes straight-walking performance over a 11.265 s trial. The proposed RL guided MPPI significantly suppresses drift accumulation, reducing the RMSE of the base lateral position error from 0.339 m for the pure RL policy to 0.022 m. This indicates that the added straight-walk objective introduces a task-space closed-loop refinement that compensates systematic left–right bias in the pretrained policy, enabling near-straight locomotion while retaining the robust walking behavior provided by the RL prior. Fig. 2(c) further shows that the forward velocity tracking accuracy is comparable between the two methods, with RMSE values of 0.773 for RL guided MPPI and 0.806 for pure RL. In contrast, the lateral velocity tracking in Fig. 2(d) improves noticeably, where RL guided MPPI achieves an RMSE of 


Fig. 3. Squat task performance via base height cost augmentation. (a) Left view snapshots of the simulated Humanoid G1. (b) Base-height tracking with a piecewise-linear reference _z_<sup>des</sup> (0.71–0.78 m). The RL baseline remains near its nominal height since _z_ is not a part of the policy command interface. 

0.021 m/s compared to 0.046 m/s for pure RL. These results support that incorporating task-space feedback through MPPI improves motion precision, particularly in drift-related components, without degrading the nominal velocity-tracking performance of the learned policy. 

_b) Squat task:_ To demonstrate task augmentation beyond the RL command interface, we add a base-height objective for a squat motion through cost composition. Specifically, we augment the MPPI stage cost with a baseheight tracking term, 


where _z_ base is the robot base height, _z_<sup>des</sup> is a piecewise-linear height reference, and _βz_ = 100. 

Fig. 3(b) shows that RL guided MPPI tracks the prescribed base-height reference over the entire motion, including the transition regions between descent and ascent. 

Unlike the straight-walk scenario where the command is expressed in planar task coordinates ( _vx_<sup>_des_</sup> _, vy_<sup>_des_</sup> _, ψ_<sup>_des_</sup> ), the squat task introduces an additional vertical objective that the pretrained RL policy cannot directly command or regulate. Consistent with this, the RL only curve in Fig. 3(b) remains near its nominal base height instead of following _z_<sup>des</sup> ( _t_ ). In contrast, our proposed method closes a task-space feedback loop in the _z_ direction and achieves accurate base-height regulation without retraining. 

Representative snapshots are shown in Fig. 3(a). Starting from the nominal upright posture produced by the pretrained locomotion policy, RL guided MPPI adjusts the lower-body joint targets to drive the base height toward the time-varying reference while maintaining balance. The snapshots illustrate 

the descent phase, where the controller increases knee and hip flexion to lower the pelvis, and the ascent phase, where it reverses this coordination to recover the original height. Importantly, these posture changes emerge from cost-based refinement around the RL prior rather than from any explicit squat command in the RL interface, demonstrating that the proposed add-on controller can synthesize a whole-body posture adaptation to satisfy a vertical task objective. 

## V. CONCLUSION 

We presented an RL guided whole-body MPPI framework for humanoid control, where a pretrained RL policy is used as a sampling prior and task objectives are specified through a modular MPPI cost evaluated by physics engine rollouts. By refining the policy prior online using knot-parameterized MPPI, the proposed add-on controller improves task-level precision in real-time while maintaining the robust locomotion provided by the pretrained policy. Furthermore, despite relying on CPU-based parallelism, our asynchronous implementation achieves an average effective update rate of 280 Hz in simulation, which GPU-based rollouts could further increase the update rate. In simulation on a 29DoF Unitree G1 model in MuJoCo, the method corrected a common RL failure mode in straight walking under the same command interface by reducing lateral drift, and it enabled task augmentation without retraining by incorporating additional objectives such as base-height controlling shaping via cost composition. 

This work highlights the benefits of decoupling learning from task specification. Viewed as an add-on feedback controller, our MPPI module can be attached to a pretrained RL policy to retain its robust locomotion prior while injecting precise, whole-body objective shaping through modular cost design. This plug-and-play structure allows the same learned controller to be reused across tasks: new objectives can be introduced by composing or reweighting cost terms, without modifying the RL policy or its command interface. 

While the proposed framework provides a strong plugand-play way to add precise whole-body objectives on top of robust RL locomotion, its behavior is naturally anchored to the pretrained policy prior used for sampling. Extending the framework to support larger behavioral changes will be an exciting direction, for example by incorporating multiple priors (skill libraries), adaptive proposal distributions, or switching/blending mechanisms. Future work will also focus on real-hardware deployment, improving robustness to modeling and contact-estimation errors, and establishing reliable synchronization and state-estimation pipelines. 

## REFERENCES 

- [1] J. Z. Zhang, T. A. Howell, Z. Yi, C. Pan, G. Shi, G. Qu, T. Erez, Y. Tassa, and Z. Manchester, “Whole-body model-predictive control of legged robots with mujoco,” _arXiv preprint arXiv:2503.04613_ , 2025. 

- [2] Y. Chen, “Walking problem of bipedal humanoid robot: comparison between model-based and learning-based method,” in _2023 IEEE 3rd International Conference on Power, Electronics and Computer Applications (ICPECA)_ , 2023, pp. 1629–1633. 

   - [4] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, p. eadi9579, 2024. 

   - [5] G. Li and R. Gomez, “Realizing full-body control of humanoid robots,” _Nature Machine Intelligence_ , vol. 6, pp. 990–991, 2024. 

   - [6] G. B. Margolis, G. Yang, K. Paigwar, T. Chen, and P. Agrawal, “Rapid locomotion via reinforcement learning,” _The International Journal of Robotics Research_ , vol. 43, no. 4, pp. 572–587, 2024. 

   - [7] Y. Ze _et al._ , “Twist2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint arXiv:2511.02832_ , 2025. 

   - [8] Z. Luo _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

   - [9] A. L. Bishop, J. Alvarez-Padilla, S. Schoedel, I. S. Sow, J. Chandrachud, S. Sharma, W. Kraus, B. Park, R. J. Griffin, J. M. Dolan _et al._ , “The surprising effectiveness of linear models for whole-body modelpredictive control,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2025, pp. 1–7. 

   - [10] L. Molnar, J. Cheng, G. Fadini, D. Kang, F. Zargarbashi, and S. Coros, “Whole-body inverse dynamics mpc for legged loco-manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

   - [11] G. Williams, P. Drews, B. Goldfain, J. M. Rehg, and E. A. Theodorou, “Aggressive driving with model predictive path integral control,” in _2016 IEEE International Conference on Robotics and Automation (ICRA)_ , 2016, pp. 1433–1440. 

   - [12] G. Williams, A. Aldrich, and E. A. Theodorou, “Model predictive path integral control: From theory to parallel computation,” _Journal of Guidance, Control, and Dynamics_ , vol. 40, no. 2, pp. 344–357, 2017. 

   - [13] J. Alvarez-Padilla, J. Z. Zhang, S. Kwok, J. M. Dolan, and Z. Manchester, “Real-time whole-body control of legged robots with model-predictive path integral control,” 2024. [Online]. Available: https://arxiv.org/abs/2409.10469 

   - [14] D. Kim, E. Im, Y. Kim, M. Lim, and Y. Lee, “Single-instance sampling for computationally efficient and accurate real-time task space mppi control,” _IEEE Transactions on Robotics_ , vol. 41, pp. 6327–6344, 2025. 

   - [15] Y. Seo, D. Kim, J. Bak, Y. Oh, and Y. Lee, “Extremely fast computation of com trajectory generation for walking leveraging mppi algorithm,” in _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , 2023, pp. 1–7. 

   - [16] T. Howell, N. Gileadi, S. Tunyasuvunakool, K. Zakka, T. Erez, and Y. Tassa, “Predictive sampling: Real-time behaviour synthesis with mujoco,” _arXiv preprint arXiv:2212.00541_ , 2022. 

   - [17] J. Alvarez-Padilla, J. Z. Zhang, S. Kwok, J. M. Dolan, and Z. Manchester, “Real-time whole-body control of legged robots with modelpredictive path integral control,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 14 721– 14 727. 

   - [18] H. Xue, C. Pan, Z. Yi, G. Qu, and G. Shi, “Full-order sampling-based mpc for torque-level locomotion control via diffusion-style annealing,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 4974–4981. 

   - [19] G. Williams, P. Drews, B. Goldfain, J. M. Rehg, and E. A. Theodorou, “Information-theoretic model predictive control: Theory and applications to autonomous driving,” _IEEE Transactions on Robotics_ , vol. 34, no. 6, pp. 1603–1622, 2018. 

   - [20] R. Tedrake, _Underactuated Robotics_ , 2023. [Online]. Available: https://underactuated.csail.mit.edu 

   - [21] I. S. Mohamed, J. Xu, G. S. Sukhatme, and L. Liu, “Toward efficient mppi trajectory generation with unscented guidance: U-mppi control strategy,” _IEEE Transactions on Robotics_ , vol. 41, pp. 1172–1192, 2025. 

   - [22] M. Kelly, “An introduction to trajectory optimization: How to do your own direct collocation,” _SIAM Review_ , vol. 59, no. 4, pp. 849–904, 2017. 

   - [23] C. Tao, F. Wang, H. Jiang, J. He, Y. Chen, and Q. Bu, “Sampling strategy design for model predictive path integral control on legged robot locomotion,” _arXiv preprint arXiv:2601.01409_ , 2026. 

   - [24] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [3] T. Haarnoja _et al._ , “Learning agile soccer skills for a bipedal robot with deep reinforcement learning,” _Science Robotics_ , vol. 9, p. eadi8022, 2024. 

