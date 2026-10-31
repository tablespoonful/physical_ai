---
title: "Task-Specified Compliance Bounds for Humanoids via Lipschitz-Constrained Policies"
date: "2026-03-17"
authors: "Zewen He; Yoshihiko Nakamura"
url: https://arxiv.org/abs/2603.16180
pdf: https://arxiv.org/pdf/2603.16180
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.16180)** / [論文ページ](https://arxiv.org/abs/2603.16180)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Task-Specified Compliance Bounds for Humanoids via Lipschitz-Constrained Policies 

Zewen He and Yoshihiko Nakamura 

**_Abstract_ —Reinforcement learning (RL) has demonstrated substantial potential for humanoid bipedal locomotion and the control of complex motions. To cope with oscillations and impacts induced by environmental interactions, compliant control is widely regarded as an effective remedy. However, the modelfree nature of RL makes it difficult to impose** **_task-specified_ and quantitatively verifiable compliance objectives, and classical model-based stiffness designs are not directly applicable. Lipschitz-Constrained Policies (LCP), which regularize the local sensitivity of a policy via gradient penalties, have recently been used to smooth humanoid motions. Nevertheless, existing LCP-based methods typically employ a single scalar Lipschitz budget and lack an explicit connection to physically meaningful compliance specifications in real-world systems. In this study, we propose an anisotropic Lipschitz-constrained policy (ALCP) that maps a task-space stiffness upper bound to a state-dependent Lipschitz-style constraint on the policy Jacobian. The resulting constraint is enforced during RL training via a hinge-squared spectral-norm penalty, preserving physical interpretability while enabling direction-dependent compliance. Experiments on humanoid robots show that ALCP improves locomotion stability and impact robustness, while reducing oscillations and energy usage.** 

## I. INTRODUCTION 

Humanoid robots, owing to their human-like morphology, have long been regarded as a general-purpose form factor for enabling robots to truly integrate into human society. Since their inception, a core challenge for humanoid robots has been maintaining stability during interactions with the environment. On the one hand, humanoids inherently rely on bipedal locomotion, which is intrinsically less stable than fixed-base mechanisms; on the other hand, in practical applications, robots must physically interact with the environment and, potentially, with humans. Research efforts—from early simplified models [1], through whole-body model-based control (e.g., model predictive control) [2], to reinforcement learning (RL) policies [3]—have consistently revolved around this fundamental challenge. 

Although current RL-based control policies can satisfy the basic requirements of bipedal locomotion, their black-box nature makes it difficult to reliably enforce many specific and quantifiable objectives beyond “walk without falling” [3]. A representative example is task-specified compliant control, which is crucial for task performance and safety when humanoid robots execute practical manipulation or physical-interaction tasks. Using foot impact during stepping 

The authors are with the Department of Robotics, Mohamed bin Zayed University of Artificial Intelligence, Masdar City, Abu Dhabi, United Arab Emirates. _{_ zewen.he, yoshihiko.nakamura _}_ @mbzuai.ac.ae 


Fig. 1: Task-specific compliance. (a) Hand-pulling experiment under the SILC method. (b) Hand impact experiment. A 2.5 kg weight is attached to the robot’s right hand via a rope and released from a certain height to generate an impact. (c) Stepping motion experiment. The robot’s one foot intermittently steps onto a foam pad placed on the ground, thereby introducing disturbances from uneven terrain. 

as an example, many RL locomotion pipelines mitigate undesired transients by adding shaping penalties (e.g., on joint torques, accelerations, or action-rate changes), which can reduce impact-related behaviors [4]. While often effective, this reward-engineering strategy does not naturally yield an interpretable, analyzable compliance specification, and it can introduce objective coupling: the same penalty weights that improve smoothness or reduce impacts may also hinder task performance, requiring tedious retuning across domains [5]. 

To address the same issue, a broad range of approaches has been developed in classical model-based robot control [6], [7]. However, most of these methods rely purely on modelbased theory and require sufficient hardware support (e.g., force sensors). For a long time, these methods and learningbased approaches progressed largely in parallel, with little connection between them, and thus cannot simultaneously benefit from the advantages offered by RL-based approaches. Motivated by this observation, recent studies have attempted to achieve compliant control within RL-based control frameworks. Section II-B of this paper reviews these efforts. Overall, however, most existing studies effectively wrap modelbased controllers around the RL framework, without explicitly observing the equivalent stiffness or analyzing the internal control behavior induced by the policy itself. 

Meanwhile, in RL-based methods, the use of simplified dynamics and actuation models often biases the policy toward jittery behaviors, which can severely compromise stability in real-world experiments [5]. To mitigate this phenomenon, in addition to directly adding smoothness rewards [8] or a 

low-pass filter [9], introducing Lipschitz constraints to the policy training is considered a more effective approach, which is referred to as Lipschitz-constrained policies (LCP) [5], [10]. However, in existing LCP methods applied to humanoid robots, the Lipschitz constant is typically set as a scalar. Moreover, in practical training, it is relaxed into a soft constraint or enforced only implicitly, which undermines its physical interpretability. 

Based on the above state of the art, this paper aims to start from quantitatively specified task compliance and, based on Lipschitz-constraint theory, enforce an equivalent stiffness constraint within an RL framework on humanoids. We propose a **Stiffness-Induced Lipschitz Constrained (SILC)** policy, which maps a prescribed stiffness upper-bound (in task or joint space) to an anisotropic Lipschitz budget on the policy Jacobian, and enforces it via a LCP-style regularization. In this study, we use _Lipschitz-style regularization_ to denote Jacobiannorm penalties that cap a policy’s local sensitivity. Specifically, we first use kinematic relations to map the task-space stiffness constraint to a corresponding joint-space stiffness budget. We then combine this budget with the low-level control law to express it as a target Lipschitz-style constraint, which is incorporated into the loss function during RL training. Finally, in experiments (as shown in Fig. 1), by specifying different target task-space stiffness values, we achieve tunable compliance during whole-body learning-based control on a humanoid robot. 

The main contributions of this study are as follows: 

- 1) By leveraging the Jacobian of the RL policy, we propose **policy-induced equivalent joint stiffness** , which enables explicit observation of the system’s equivalent joint stiffness under an RL-based control framework; 

- 2) We extend scalar Lipschitz-constrained policies to **anisotropic Lipschitz-constrained policies (ALCP)** for RL training, and derive target ALCP budgets from taskspace stiffness constraints, thereby endowing ALCP with a clear physical interpretation for the robotic system; 

- 3) Experimental results demonstrate that the proposed ALCP enables both task-specified compliance and stable humanoid locomotion. 

## II. BACKGROUND 

## _A. Learning-based Humanoid Control_ 

In recent years, RL-based motion control for legged robots—particularly humanoid robots—has largely converged toward a well-established paradigm. Through appropriate reward design in RL, a humanoid robot’s basic stable gait can generally be ensured [11]. Furthermore, researchers have employed imitation-learning approaches (e.g., AMP [12]) to enable robots to mimic human motions while still maintaining their own stability. Meanwhile, research on humanoid robots has shifted from pure locomotion control toward locomanipulation [13]. Whether in conventional locomotion control or more complex loco-manipulation, the central challenges for humanoid robots remain unchanged: ensuring balance 

under a floating-base formulation and handling physically reasonable contacts with the environment. To address these issues within learning-based control, many classical modelbased control components have been integrated into the framework, such as compliance control. 

## _B. Compliant Control_ 

Classical model-based compliant control has been studied for many years, and it has also achieved substantial progress in the humanoid robotics community [6]. Recently, there has been a growing interest in integrating classical compliance control into RL-based humanoid robot control. A key challenge in this integration is how to preserve the physical interpretability of compliance while retaining the distinctive advantages of RL-based methods. In early work such as deep compliant control [14], compliance objectives were recast as admittance-like tracking targets and learned via imitation. This “admittance-to-reference” paradigm was later extended in [15], [16], where desired compliance is mapped to a target displacement (in task or joint space) and the policy is trained to track the resulting reference. In parallel, other studies embed model-based compliant control directly into RL, producing behavior closer to classical impedance control [17], [18]. The former integrates cleanly with RL but can blur the intended physical meaning of compliance under learningbased tracking, whereas the latter is physically intuitive yet may conflict with the learned policy (e.g., overly stiff low-level loops can induce oscillations). Finally, neither of the above two categories provides a way to observe the system’s overall compliance characteristics, which makes targeted compliance control considerably inconvenient. 

## _C. Lipschitz Contunuity and Lipschitz-constrained Policies_ 

_1) Lipschitz continuity:_ Let ( _X , ∥· ∥X_ ) and ( _Y, ∥· ∥Y_ ) be normed spaces and _f_ : _X →Y_ be a function. We say that _f_ is _Lipschitz continuous_ if there exists a constant _L ≥_ 0 such that, for all **x** 1 _,_ **x** 2 _∈X_ , 


The smallest such _L_ is called the _Lipschitz constant_ of _f_ , denoted by Lip( _f_ ). If _f_ is differentiable, a common sufficient bound is 


where _∥· ∥_ 2 denotes the spectral (operator) norm. 

_2) Lipschitz-Constrained policies (LCP):_ In reinforcement learning, a (deterministic) policy _π_ **_θ_** : _O →A_ maps an observation **o** _∈O_ to an action **a** _∈A_ . A policy is called _Lipschitz-constrained_ if its input–output sensitivity is bounded, i.e., there exists _K_ LCP _≥_ 0 such that 


Equivalently, for differentiable policies, one can enforce a local Jacobian bound, 


Fig. 2: Control framework in reinforcement learning pipeline. 

or relax it using sample-based penalties during training. For stochastic policies _π_ **_θ_** ( **a** _|_ **o** ), Lipschitz constraints are often imposed via regularizing the norm of the input-gradient of the log-likelihood, _∥∇_ **o** log _π_ **_θ_** ( **a** _|_ **o** ) _∥_ . In several prior studies, LCP-based methods have been incorporated into RL training for humanoid robots; however, their primary objective is to mitigate motion oscillations, and they typically consider only an isotropic Lipschitz constraint [5], [10]. 

## III. PROBLEM STATEMENT 

We consider a legged humanoid robot controlled by a hierarchical architecture. The low-level controller is a fixed joint-space PD position servo, while a high-level RL policy outputs joint position targets. Let **_q_** _∈_ R<sup>_n_</sup> and **_q_** ˙ _∈_ R<sup>_n_</sup> denote joint positions and velocities, and let **_o_** _∈O_ be the policy observation (e.g., full proprioception). The policy **_q_** des = _πθ_ ( **_o_** ) produces desired joint positions, and the PD controller applies joint torques 


where **_K_** _p ≻_ **0** and **_K_** _d ⪰_ **0** are constant gain matrices (typically diagonal). This RL-based control framework can be schematically illustrated in Fig. 2. 

Let **_x_** _∈_ R<sup>_m_</sup> denote a task-space coordinate of interest (e.g., center of mass (CoM) position), with Jacobian **_J_** _x_ ( **_q_** ) ≜ _∂_ **_x_** _/∂_ **_q_** . In the neighborhood of a nominal motion, a task-space impedance law is commonly written as 


where **_f_** _x ∈_ R<sup>_m_</sup> is the task-space force, and **_K_** _x ⪰_ **0** , **_D_** _x ⪰_ **0** denote the task-space stiffness and damping, respectively. Here we consider that **_K_** _x_ and **_D_** _x_ are always symmetric positive semidefinite (SPD). The task-space stiffness matrix **_K_** _x_ defines a _stiffness ellipsoid_ with a positive constant _c_ through the quadratic form 


We are given a task-level SPD stiffness budget **_K_**<sup>max</sup> _x_ and require _Ex_ ( **_K_** _x, c_ ) _⊆ Ex_ ( **_K_**<sup>max</sup> _x , c_ ), which means that the ellipsoid induced by **_K_**<sup>max</sup> _x_ upper-bounds the allowable stiffness in every direction. In this work, **_K_**<sup>max</sup> _x_ is set as a diagonal matrix. For a position task, **_K_**<sup>max</sup> _x_ can be visualized as a spatial ellipsoid. 


Fig. 3: Stiffness upper-bound derivation diagram.upper-bound ellipsoid, illustrated as the pink ellipsoid; **_K_**<sup>max</sup> _x_ **_K_** denotes the task-space stiffness<sup>max</sup> _q_ denotes the joint-space stiffness upper-bound super-ellipsoid, where individual joint stiffnesses are depicted as torsional springs; **_K_** _LCP_ represents the Lipschitz upper-bound constraint. 


where **_a_** _t_ = _πθ_ ( **_o_** _t_ ) and the constraint may be enforced either as a hard constraint or via a soft penalty during training. 

**Proposition 1** ( **Policy-induced equivalent joint stiffness** ) **.** _Assume that the observation_ **_o_** _contains the joint positions_ **_q_** _and that πθ is differentiable with respect to_ **_q_** _in a neighborhood of interest. Then, for small perturbations around a nominal state, the incremental torque response to jointposition perturbations satisfies_ 


_where α is the action scale of the policy. The derivation of_ **_K_** eq _is given by_ (5) _and_ **_q_** des = _α_ **_a_** _t._ 

Based on the above derivations, since it accounts for both the prescribed low-level stiffness and the policy’s intrinsic sensitivity, **_K_** eq provides a more comprehensive measure for observing compliance. 

Given a desired task-space stiffness upper bound **_K_**<sup>max</sup> _x_ , our goal is to train a policy whose LCP-regularized local sensitivity induces an effective joint stiffness **_K_** eq( **_o_** ) consistent with the task-level specification. Formally, letting **_K_** _x_ ( **_o_** ) denote the task-space stiffness induced by **_K_** eq( **_o_** ), we seek a training procedure such that 


by appropriately choosing anisotropic Lipschitz budgets in the policy regularization. Following the above derivations, the procedure used in this paper to infer the target upper-bound 

of the LCP from the task-space stiffness is illustrated in Fig. 3. 

## IV. METHODOLOGY 

_A. Anisotropic Lipschitz-Constrained Policies_ 

_1) Anisotropic LCP upper-bound:_ Building on the scalar upper-bound LCP introduced in Section II-C, we extend it to the anisotropic setting in this study. Accordingly, we define the following. 

**Definition 1** ( **Anisotropic Lipschitz constraint** ) **.** Let _πθ_ : _O →_ R<sup>_n_</sup> be differentiable in **_o_** , with policy Jacobian **_J_** _π_ ( **_o_** ). Given a non-singular matrix **_K_** LCP _∈_ R<sup>_n×n_</sup> , we say that _πθ_ satisfies an _anisotropic Lipschitz constraint_ with budget **_K_** LCP on _O_ if 


Definition 1 specifies a _matrix_ (anisotropic) generalization of the standard scalar Lipschitz bound in (4). Geometrically, **_K_** LCP **_K_**<sup>_⊤_</sup> LCP<sup>definesanoutputellipsoid.Hence,</sup><sup>**_K_**LCPacts</sup> as an anisotropic “Lipschitz budget” that shapes the directiondependent sensitivity of the policy. When **_K_** LCP is chosen SPD, this can be written as 


_2) Spectral (max-eigenvalue) violation:_ Define the violation as 


where _λ_ max( _·_ ) represents the maximum eigenvalue; and penalize only positive violations: 


where we define the positive-part operator as _x_ + ≜ max( _x,_ 0) for any scalar _x ∈_ R. Based on (13), **_J_** _π_ ( **_o_** ) **_J_** _π_ ( **_o_** )<sup>_⊤_</sup> _−_ **_K_**<sup>2</sup> LCP<sup>shouldalwaysbenegativesemidefinite.Accordingly,</sup> ( _v_ max( **_o_** ))<sup>2</sup> +<sup>penalizesonlyconstraintviolations(</sup><sup>_v_max(</sup><sup>**_o_**)</sup><sup>_>_</sup> 0) and is zero otherwise. This yields the unconstrained objective in the loss function 


where _λlip_ is a weight of LCP loss. 

## _B. Joint-space Stiffness Upper-bound Ellipsoid_ 

Let **_x_** = _f_ ( **_q_** ) be a task-space variable with Jacobian **_J_** _x_ ( **_q_** ) = _∂_ **_x_** _/∂_ **_q_** _∈_ R<sup>_m×n_</sup> . For clarity, we consider _anisotropic_ (matrix-valued) stiffness budgets specified by symmetric positive-definite matrices **_K_**<sup>max</sup> _x ≻_ **0** . 

According to [19], the contact conditions of a humanoid robot can be categorized into single-support and doublesupport. In each contact mode, the support foot is assumed to be a fixed base (i.e., no relative slipping). In the singlesupport case, the relationship between task-space compliance **_C_** _x_ and joint-space compliance **_C_** _q_ is 


A general symmetric solution of (17) is 

**_C_** _q_ = **_J_** _x_<sup>_♯_</sup><sup>**_C_**</sup><sup>_x_</sup><sup>**_J_**</sup><sup>_⊤_</sup> _x_<sup>_♯_+ (</sup><sup>**_Y_**</sup><sup>_−_</sup><sup>**_J_**</sup><sup>_♯_</sup> _x_<sup>**_J_**</sup><sup>_x_</sup><sup>**_Y J_**</sup><sup>_⊤_</sup> _x_<sup>**_J_**</sup><sup>_⊤_</sup> _x_<sup>_♯_)</sup><sup>_,_</sup> (18) where **_J_**<sup>_♯_</sup> _x_<sup>isthepseudo-inverseof</sup><sup>**_J_**</sup><sup>_x_,and</sup><sup>**_Y_**isanarbitrary</sup> symmetric matrix for null-space compliance. Given a task-space stiffness upper bound **_K_**<sup>max</sup> _x_ , (11) is equivalently expressed as the compliance lower-bound 


Using (17), a sufficient condition for (20) is to choose a jointspace compliance budget **_C_**<sup>max</sup> _q_ such that 


Finally, defining **_K_**<sup>max</sup> _q_ ≜ ( **_C_**<sup>max</sup> _q_ )<sup>_−_1</sup> , and **_K_** q ≜ **_C_**<sup>_−_</sup> _q_<sup>1</sup> as the joint stiffness matrix, we obtain the following sufficient joint-space condition: 


which guarantees the task-space bound (11). In this study, we consider the joint-space stiffness **_K_** q to be physically equivalent to **_K_** eq in (10): **_K_** q = **_K_** eq. 

_C. Anisotropic Lipschitz-Constrained Policies Based on Target Stiffness_ 

_1) Anisotropic upper-bound via an ellipsoidal metric induced by_ **_K_**<sup>max</sup> _q :_ Let **_K_**<sup>max</sup> _q ∈_ R<sup>_n×n_</sup> be an arbitrary symmetric PSD matrix encoding an anisotropic closed-loop stiffness upper-bound. Assuming **_K_**<sup>max</sup> _q ≻_ **0** , we define the weighted norm induced by compliance **_C_**<sup>max</sup> _q_ = ( **_K_**<sup>max</sup> _q_ )<sup>_−_1</sup> : 


We impose the following _anisotropic gain constraint_ on torque perturbations: 


Here enforcing (24) for all _δ_ **_q_** ensures the closed-loop incremental torque response is bounded in every joint-space direction. Substituting (9) into (24) yields 


_2) Reduction to a Lipschitz-style (spectral-norm) constraint:_ Let **_K_**<sup>max</sup> _q_ = **_LL_**<sup>_⊤_</sup> be a Cholesky factorization with **_L_** invertible. Then 


Using (26), the constraint (25) is equivalent to 


In this study, we define the constraint in (27) as StiffnessInduced Lipschitz Constrained (SILC). Up to this point, we can observe that although SILC also imposes a Lipschitz-type constraint on the policy Jacobian, scalar LCP essentially constrains the Jacobian matrix itself, whereas the SILC constrains 

the equivalent stiffness directly. Therefore, tightening scalar LCP can only drive the effective stiffness to asymptotically approach the underlying PD stiffness, whereas SILC can constrain the joint stiffness to lie below an arbitrary target upper bound—even lower than the stiffness of the low-level PD controller. 

_3) Training objective:_ Define the whitened Jacobian-like quantity 


A hinge-squared penalty that softly enforces (27) is 


where _∥· ∥_ 2 denotes the spectral norm (largest singular value), which can be approximated efficiently (e.g., via power iteration). Note that the stiffness upper-bound ellipsoid is not absolutely inviolable, we therefore still adopt a soft-constraint formulation. In addition, the spectral-norm penalty used in this context is still a form of gradient penalty rather than an SNLCP [10]. 

The total training loss can be written as 


where _λ_ aniso is the weights of anisotropic Lipschitz loss. 

V. REINFORCEMENT LEARNING SETUP 

## _A. Baseline_ 

This section describes the configuration of the RL training in Isaac Gym environment used in this work. For upper-body motion priors, we employ the AMASS dataset [20]. In the baseline, the network architecture and hyperparameter settings are kept consistent with those of FALCON [21]. Moreover, to enable a more direct comparison with the proposed method, we modify the baseline from the original work as follows. First, we augment the observation space with the contact phase and upper-body torque. Second, we reduce the weight of the regularization (joint velocity, acceleration, and torque) reward term by scaling it by a factor of 0.1. 

## _B. Training Details_ 

In this work, all training is conducted on a workstation running Ubuntu 22.04, equipped with an Intel Core i9-14900K CPU and an NVIDIA RTX 4080 GPU. The frequency of the policy output is 50 Hz. The action scale _α_ is 0.25. The policy parameter **_θ_** are updated via proximal policy optimization (PPO) [22]. As in the baseline, the observation is constructed by stacking the states from the previous five time steps. However, when computing the equivalent stiffness, we use only the state from the previous time step to evaluate the policy Jacobian. For the introduced SILC loss term, its weight _λ_ aniso is set to 0.5. To select the appropriate kinematic chain for computing the equivalent joint stiffness, we employ a finitestate machine (FSM) during training to determine whether the robot is in double-support, single-support, or a flight phase based on foot-contact detection. Because the foot contact force is privileged information that is required only during 

TABLE I: CoM task and null-space stiffness setting in SILC method. 

|**Mode**|**CoM Stiffness**|**Null-space Stiffness**|
|---|---|---|
|**High-stiff**|[1000_,_1000_,_20000]|100_._0|
|**Compliance**|[200_,_200_,_20000]|50_._0|
|**Hard-nullspace**|[200_,_200_,_20000]|500_._0|


training, it does not pose a concern for deployment, where such measurements may be unavailable. 

## VI. EXPERIMENT 

## _A. Experiment Setting_ 

This section primarily evaluates the effect of SILC in both simulation and hardware experiments and compares it against the baseline and scalar LCP. We mainly compare the following approaches: 

- **Baseline (without LCP)** : similar as in FALCON [21], but without action jitter penalty. 

- **Scalar LCP** : set Lipschitz upper-bound as a scalar [10]: 


We set the Lipschitz constant _KLCP_ values to 2 _._ 0 and weight _λ_ = 0 _._ 5. Empirically, this Lipschitz constant is already close to the minimum critical threshold; reducing _KLCP_ further would directly lead to control instability. 

- **Task stiffness-induced anisotropic LCP** : in this case, we set a task stiffness-induced Lipschitz upper-bound in the policy. We configured three modes, namely _high-stiff_ , _compliance_ , and _hard-nullspace_ . The specific stiffness settings are provided in Table I. _λ_ aniso is set to 0.5. 

To evaluate the performance of each approach, several metrics are used as follows. Beyond several commonly used evaluation criteria (e.g., joint torque, joint velocity), this paper follows [5] and introduces the following metric definitions: 

- 1) _Jitter_ (action, DoF velocity, torque): Let **_a_** _t ∈_ R<sup>_n_</sup> be the action vector at discrete time _t_ , sampled with constant timestep ∆ _t_ : 


To compute other jitters, one can simply replace _a⋆_ in (32) with _q_ ˙ _⋆_ or _τ⋆_ , respectively. 

2) _Energy_ (absolute-mean): 


- 3) _Directional Quadratic-form Budget_ : We enforce the stiffness upper bound of (11) in a directional (quadratic-form) sense for any joint perturbation _δ_ **_q_** _∈_ R<sup>_n_</sup> : 


That is, the incremental elastic energy induced by **_K_** eq( **_o_** ) is upper bounded by the budget ellipsoid defined by **_K_**<sup>max</sup> q in every direction _δ_ **_q_** . 

4) _High-frequency energy_ : 


where _Sxixi_ ( _f_ ) is the power spectral density of _i_ -th task position component, _f_ 0 is 5 Hz, and _fN_ is 100 Hz. 5) _Peak-to-peak (P95-P5)_ : 


where _s_ ( _t_ ) denote a scalar trajectory signal of interest, and P _p_ ( _·_ ) denotes the _p_ -th percentile over the evaluation interval. 

## _B. Simulation Results_ 

In this subsection, all simulations are conducted on robot Unitree G1 in the Isaac Gym environment. 

_1) CoM Compliance in Stance Mode:_ In the double-support standing mode, we first enable only the CoM compliance task. In this experiment, we apply an external impulse (-150 N in 0.05 s) to G1’s pelvis link in _x_ -direction while it is standing. Fig. 4 illustrates the CoM fluctuation trajectories under the compliance SILC and high-stiff SILC settings. It can be clearly seen from the figure that, under the same-magnitude impact, the CoM in the compliance case deviates and then returns to the initial equilibrium state. In contrast, in the highstiff case, the CoM exhibits a larger deviation and does not return to its original position. We attribute this to the larger CoM compliance in the compliance case: the external impact induces a larger displacement, and subsequently, the policy prioritizing balance recovery sacrifices CoM tracking accuracy. This result indicates that, under the proposed SILC method, specifying different task-space stiffness constraints can induce distinct compliance behaviors in the robot. We also observe that the response behavior of scalar LCP is similar to that of high-stiff case. As discussed earlier, this Lipschitz constant is already the smallest value that preserves stability; however, it still cannot satisfy the requirement of high CoM compliance. This is mainly because the two kind of LCP are fundamentally different in essence as mentioned in Section IV-C2. 

_2) End-effector Compliance Under Constant Load:_ In this subsection, the G1 robot stands in double-support while its arms are set to maintain a default L-shape. A constant vertical external force (-40 N in _z_ -axis) is applied to the robot’s left hand. We compared two cases both applying SILC but using different parameter settings. In both cases, CoM and null-space stiffness are the same as in the compliance case in Table I. While in the _hard_ case, the hand task stiffness is [1000 _,_ 1000 _,_ 1000]; in the _soft_ case, hand stiffness is [200 _,_ 200 _,_ 200]. Fig. 5 illustrates the _z_ -direction displacement of the left hand during the application of the external force. By combining the displacement between the quasi-steady-state position and the initial position with the known external force, we estimate the measured equivalent task-space stiffness under the two control policies to be approximately 400 (compliance) and 1000 N/m (high-stiff), respectively. Compared with the 


Fig. 4: The _x_ -direction CoM trajectory receiving an _−x_ -direction impact (150 N in 0.05 s) on pelvis link. The red triangle indicates the time instant at which the impact is applied. Compared with the _high-stiff_ mode—in which the CoM returns to its original state via a damped oscillatory response—the _compliance_ mode exhibits more pronounced compliance, as evidenced by larger oscillation amplitudes and the lack of convergence back to the original state. Meanwhile, _scalar LCP_ also exhibits similarly high stiffness to high-stiff mode. 


Fig. 5: Hand displacement under different task-space compliance settings of SILC when a constant load (-40 N) is applied to the left hand. It can be observed that, in both cases, the hand displacement responds within a very short time ( _<_ 0.1 s). After the response settles, we compare the steady-state position with the initial position and, together with the applied external force, approximately estimate the equivalent task-space stiffness to be 400 (soft) and 1000 N/m (hard), respectively. 

setting compliance, this result demonstrates that the proposed SILC not only enforces stiffness constraints in fast transient responses, but also enables controllable compliance under quasi-static deformations induced by external forces. 

_3) Walking Motion:_ In this subsection, the robot switches between different supporting-cases by the FSM. We first evaluate the violations of the directional PSD budget as in Section VI-A during a stepping-in-place motion while the upper limbs track a random trajectory. In this evaluation, we randomly sample unit _δ_ **_q_** vectors along different DoFs to compute the PSD values as in (34). Fig. 6 illustrates the lefthand side and right-hand side values of (34). We can find that the measured value under SILC is strictly bounded by the budget; while under scalar LCP and baseline, the measured quadratic form periodically exceeds the calculated budget. 

We then sample random velocity commands for the robot across 1,024 environments. First, after training for a given number of iterations (14,000), the basic tracking rewards are very similar across all settings; we therefore treat this as a fair baseline for comparison. Then we measure the corresponding metrics over an episode, as summarized in Table II. The comparison of all LCP variants with the baseline shows that the LCP methods yield noticeably smaller energy values and jitter 


Fig. 6: According to the definition of the Directional Quadratic-form Budget, at each control step we plot the left-hand side (LHS) and right-hand side (RHS) of (34), respectively (unit of quadratic form: N _·_ m _·_ rad). The yellow curve corresponds to the RHS of the equation, i.e., the quadratic form under the target **_K_**<sup>max</sup> _q_ , whereas the blue curve corresponds to the LHS, i.e., the current quadratic form measured **_K_** _q_ ( **_o_** ). The red markers indicate instances where the measured value exceeds the target. As shown, under the SILC method, the measured value is strictly bounded by the target constraint; in contrast, under scalar LCP and baseline, the measured quadratic form periodically exceeds the target during the stepping gait. 

of action and torque, but a larger velocity jitter. We attribute this primarily to the fact that the LCP constrains the output stiffness at the policy-Jacobian level, thereby substantially suppressing the baseline’s tendency to achieve task tracking via high-frequency oscillations. Next, relative to the scalar LCP baseline, SILC methods reduce action jitter but increase energy consumption. By decomposing the metrics into upperand lower-body, we find that this energy increase is driven primarily by the lower body, which also exhibits higher jitter under SILC. These results suggest that SILC attains compliance by reallocating effort to the lower body, partially trading motion smoothness for compliance—contrary to the common assumption that greater compliance lowers energy. Notably, SILC compliance is task-conditioned on simultaneously maintaining balance and tracking upper-body motion, making this trade-off reasonable. Consistently, a higher stiffness setting (high-stiff) can even reduce energy consumption. 

## _C. Experiment Validation_ 

In this subsection, we deploy the previously trained policy on the physical G1 robot. At first, we evaluate the hand 

compliance while the robot is standing, as shown in Fig. 1a. We then evaluate the control performance under a hand load. Specifically, we attach a 2.5 kg weight to the robot’s right hand using a rope and release it from a certain height (as shown Fig. 1b). The robot’s right hand is displaced by the external force and oscillates, and then converges to an equilibrium position. Table III summarizes the hand oscillation behavior under different policies. In the SILC situation, we applied the policy trained by SILC with the _soft_ hand task setting as introduced in Section VI-B2. As shown in the table, the settling time under SILC is about half that of the baseline, and the high-frequency energy along the _z_ -axis is nearly an order of magnitude lower. This indicates that the proposed SILC method effectively attenuates the oscillations induced by external impacts by increasing hand compliance. 

We also similarly set up a stepping motion and placed soft pads on the ground to emulate uneven terrain (as shown in Fig. 1c). During stepping, we recorded the IMU measurements, as shown in Table IV. As shown in the table, the SILC method (compliance setting) outperforms the baseline across all metrics, for both the RMS (root mean square) and peakto-peak values. In particular, the gyroscope fluctuations under SILC are roughly half of those observed with the baseline. This result indicates that, compared with the baseline, the proposed SILC method reduces body-link oscillations during locomotion by increasing compliance. 

## _D. Discussion_ 

Combining the above theoretical derivations and the experimental results, imposing an ALCP on the state-dependent equivalent joint stiffness is typically considered to yield the following effects: 

- 1) **Equivalent compliance observer in RL framework.** Through the proposed policy-induced equivalent joint stiffness, the stiffness under a RL controller can be explicitly observed. This equivalent stiffness is neither simply the stiffness of the low-level controller nor the stiffness estimated from a task-space displacement–torque relationship; rather, it is the true effective stiffness derived from the policy’s inherent characteristics. 

- 2) **Adjustable compliance and impact robustness.** In the proposed SILC method, the equivalent joint-stiffness constraint is derived directly from the task-space specification. Therefore, task compliance budget can be tuned via the LCP formulation. Moreover, the experimental results confirm that both the transient and steady-state responses can be modulated using this approach, thereby enabling different robustness under external disturbances. 

- 3) **Smoother and more stable motion.** Since the Lipschitz constraint limits the equivalent stiffness gain, the policy cannot react to small observation perturbations with arbitrarily large changes in action. In practical control, this property can mitigate the high-frequency jitter induced by the policy, improve motion stability, and also contribute to energy efficiency. 

TABLE II: Comparison of walking motion under random velocity command. (environment number: 1,024) 

||**Action Jitter** (_×_10<sup>4</sup>) _↓_|**DoF Velocity Jitter [rad/s]** (_×_10<sup>5</sup>) _↓_|**Torque Jitter [Nm]** (_×_10<sup>5</sup>) _↓_|**Energy [J]** _↓_|
|---|---|---|---|---|
|**High-stiff SILC**|3_._08_±_0_._19|1_._97_±_0_._17|4_._89_±_0_._34|**4****_._77****_±_ 3****_._07**|
|**Compliance SILC**|3_._19_±_0_._28|2_._03_±_0_._28|5_._04_±_0_._38|4_._99_±_5_._17|
|**Hard-nullspace SILC**|**3****_._03****_±_ 0****_._17**|1_._84_±_0_._16|4_._80_±_0_._22|4_._86_±_4_._47|
|**Scalar LCP (**_λ_= 0_._5**)**|3_._52_±_7_._00|1_._74_±_1_._96|**4****_._47****_±_ 5****_._01**|5_._09_±_4_._76|
|**Baseline**|4_._13_±_1_._94|**1****_._68****_±_ 0****_._51**|5_._35_±_1_._13|7_._58_±_10_._74|


TABLE III: Metrics of the right hand _z_ -direction trajectory oscillations under external impacts. 

||**Settling time [s]** _↓_|**High-frequency energy [J]** _↓_|
|---|---|---|
|**SILC (soft)**|1_._2|1_._01_×_10<sup>_−_8</sup>|
|**Baseline**|2_._4|10_._0_×_10<sup>_−_8</sup>|


TABLE IV: IMU measurement in the stepping experiment. 

|||**RMS** _↓_|**Peak-to-Peak (P95-P5)** _↓_|
|---|---|---|---|
|**Compliance**|Gyro.|0_._247|0_._726|
|**SILC**|Acc. (_x_ and _y_)|3_._885|12_._66|
|**Baseline**|Gyro.|0_._472|1_._433|
||Acc. (_x_ and _y_)|4_._859|13_._80|


This work has three main limitations. First, although SILC updates its kinematic terms online, the task-space stiffness budget is not yet adjustable at runtime. Second, the current formulation constrains only the policy sensitivity to joint positions, so the induced equivalent stiffness is defined on a limited subspace and ignores other relevant state components (e.g., joint velocities, task-space states, or latent variables). Finally, we regulate stiffness only; the associated damping design and constraints are left for future work. 

## VII. CONCLUSION 

This study proposes a Stiffness-Induced Lipschitz Constrained (SILC) policy that transfers a task-specified stiffness upper-bound to an anisotropic Lipschitz budget on the policy Jacobian and enforces it via a Lipschitz constraint during training. Our method builds upon Lipschitz-constrained policies (LCP), but extends the original scalar constraint to an anisotropic form and links it to task-specified compliance. With the proposed theoretical formulation, compliance during policy execution can be achieved by directly specifying an upper-bound on the task-space stiffness during RL training. 

## REFERENCES 

- [1] S. Kajita, F. Kanehiro, K. Kaneko, K. Fujiwara, K. Harada, K. Yokoi, and H. Hirukawa, “Biped walking pattern generation by using preview control of zero-moment point,” in _2003 IEEE international conference on robotics and automation (Cat. No. 03CH37422)_ , vol. 2. IEEE, 2003, pp. 1620–1626. 

- [2] A. Escande, N. Mansard, and P.-B. Wieber, “Hierarchical quadratic programming: Fast online humanoid-robot motion generation,” _The International Journal of Robotics Research_ , vol. 33, no. 7, pp. 1006– 1028, 2014. 

- [3] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _Science Robotics_ , vol. 9, no. 89, p. eadi9579, 2024. 

- [4] N. Rudin, D. Hoeller, P. Reist, and M. Hutter, “Learning to walk in minutes using massively parallel deep reinforcement learning,” in _Conference on robot learning_ . PMLR, 2022, pp. 91–100. 

- [5] Z. Chen, X. He, Y.-J. Wang, Q. Liao, Y. Ze, Z. Li, S. S. Sastry, J. Wu, K. Sreenath, S. Gupta, _et al._ , “Learning smooth humanoid locomotion through lipschitz-constrained policies,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 4743–4750. 

- [6] B. Henze, A. Dietrich, and C. Ott, “An approach to combine balancing with hierarchical whole-body control for legged humanoid robots,” _IEEE Robotics and Automation Letters_ , vol. 1, no. 2, pp. 700–707, 2015. 

- [7] K. Yamamoto, T. Ishigaki, and Y. Nakamura, “Humanoid motion control by compliance optimization explicitly considering its positive definiteness,” _IEEE Transactions on Robotics_ , 2021. 

- [8] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8944–8951. 

- [9] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 2811–2817. 

- [10] J. Shin, W. Cha, D. Kim, J. Cha, and J. Park, “Spectral normalization for lipschitz-constrained policies on learning humanoid locomotion,” _arXiv preprint arXiv:2504.08246_ , 2025. 

- [11] Y. Gu, G. Shi, F. Shi, I.-C. Chang, Y.-J. Wang, Q. Cheng, Z. Olkin, I. Lopez-Sanchez, Y. Feng, J. Zhang, _et al._ , “Evolution of humanoid locomotion control.” 

- [12] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [13] Z. Gu, J. Li, W. Shen, W. Yu, Z. Xie, S. McCrory, X. Cheng, A. Shamsah, R. Griffin, C. K. Liu, _et al._ , “Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning,” _arXiv preprint arXiv:2501.02116_ , 2025. 

- [14] S. Lee, P. S. Chang, and J. Lee, “Deep compliant control,” in _ACM SIGGRAPH 2022 conference proceedings_ , 2022, pp. 1–9. 

- [15] B. Xu, H. Weng, Q. Lu, Y. Gao, and H. Xu, “Facet: Force-adaptive control via impedance reference tracking for legged robots,” _arXiv preprint arXiv:2505.06883_ , 2025. 

- [16] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan, “Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning,” _arXiv preprint arXiv:2510.05070_ , 2025. 

- [17] L. Wei, X. Peng, R.-Z. Qiu, X. Cheng, and X. Wang, “Hmc: Learning heterogeneous meta-control for contact-rich loco-manipulation,” in _RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 

- [18] Z. He, C. Chen, D. Azizov, and Y. Nakamura, “Cotap: Compliant task pipeline and reinforcement learning of its controller with compliance modulation,” _arXiv preprint arXiv:2509.25443_ , 2025. 

- [19] K. Yamamoto, “Robust Walking by Resolved Viscoelasticity Control Explicitly Considering Structure-Variability of a Humanoid,” in _Proc. of IEEE ICRA_ , 2017, pp. 3461–3468. 

- [20] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 5442–5451. 

- [21] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Aghamohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi, “Falcon: Learning force-adaptive humanoid loco-manipulation,” _arXiv preprint arXiv:2505.06776_ , 2025. 

- [22] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

