---
title: "Data-driven Interpretable Hybrid Robot Dynamics"
date: "2025-12-10"
authors: "Christopher E. Mower; Rui Zong; Haitham Bou-Ammar"
url: https://arxiv.org/abs/2512.11900
pdf: https://arxiv.org/pdf/2512.11900
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.11900)** / [論文ページ](https://arxiv.org/abs/2512.11900)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Data-driven Interpretable Hybrid Robot Dynamics 

Christopher E. Mower<sup>1</sup> , Rui Zong<sup>1</sup> , Haitham Bou-Ammar<sup>1</sup><sup>_,_2</sup> 

> 1Huawei, Noah’s Ark Lab, London, UK 

> 2University College London, London, UK 

**_Abstract_ —We study data-driven identification of interpretable hybrid robot dynamics, where an analytical rigid-body dynamics model is complemented by a learned residual torque term. Using symbolic regression and sparse identification of nonlinear dynamics (SINDy), we recover compact closed-form expressions for this residual from joint-space data. In simulation on a 7- DoF Franka arm with known dynamics, these interpretable models accurately recover inertial, Coriolis, gravity, and viscous effects with very small relative error and outperform neuralnetwork baselines in both accuracy and generalization. On real data from a 7-DoF WAM arm, symbolic-regression residuals generalize substantially better than SINDy and neural networks, which tend to overfit, and suggest candidate new closed-form formulations that extend the nominal dynamics model for this robot. Overall, the results indicate that interpretable residual dynamics models provide compact, accurate, and physically meaningful alternatives to black-box function approximators for torque prediction.** 

## I. INTRODUCTION 

Accurate estimation of a robot’s dynamics (i.e., its equations of motion) is crucial for applications such as force control [1] and external torque estimation [2]. However, these dynamics depend on many interacting factors (e.g., mechanical structure, payload, contact conditions), making modeling difficult. As a result, purely model-based approaches often become impractical, requiring considerable expertise to derive the models. 

In parallel, the emergence of large-scale vision–language– action (VLA) models [3–5] is rapidly changing how we think about robot controllers: instead of hand-designed pipelines, robots are increasingly treated as black-box embodiments that map images and language instructions to low-level actions. However, current VLA datasets and policies are almost exclusively built around visual, linguistic, and proprioceptive signals; explicit force or torque measurements are rarely available at scale, and only a small number of recent works explore force- or touch-augmented foundation models [6–8]. These works suggest that explicitly treating force and touch as first-class modalities can substantially improve performance on contact-rich manipulation tasks, but they also highlight a key bottleneck: high-quality force/torque and tactile sensors are expensive, difficult to integrate across many platforms, and often produce noisy, robot-specific signals, so most robots in large datasets simply do not have them. If we could reliably infer internal and external joint torques from readily available signals (e.g. encoder-based kinematics and motor torques) using an interpretable dynamics model, we would effectively equip fleets of otherwise “blind-to-force” robots with virtual force sensors at negligible hardware cost. This would both enable scalable collection of contact-rich supervision for 

future VLA-style policies and provide physically grounded signals (estimated forces and torques) that can be used as additional targets or auxiliary tasks during training, tightening the connection between high-level foundation models and the underlying mechanics of the robot. 

From a reinforcement learning (RL) perspective, good physical priors over the robot’s dynamics are equally important. A long line of work in legged locomotion has shown that combining deep RL with accurate simulators and carefully designed structure can produce remarkably robust controllers for quadrupeds in the real world [9–12]. In these systems, the policy is typically trained in a high-fidelity rigid-body simulator with hand-engineered rewards and contact models, and then transferred to hardware via domain randomization and other robustness techniques. While this pipeline has enabled blind locomotion over challenging terrain [10] and rapid policy training in minutes [11], it remains heavily reliant on accurate but opaque simulators, and the learned policies themselves provide little direct insight into the underlying mechanics. Interpretable models of joint torques and contact forces offer a complementary route: they can serve as structured priors or residual models inside model-based or hybrid RL schemes, provide physically meaningful features and auxiliary targets for value and policy networks, and constrain exploration to behavior that remains consistent with known dynamics. In the context of contact-rich tasks surveyed by Ha et al. [12], such physically grounded priors are crucial for improving sample efficiency, safety, and out-of-distribution generalization, especially when training directly on hardware or across diverse robot morphologies. 

Together with the rapid growth of AI techniques, these challenges have motivated researchers to explore data-driven approaches based on neural networks. Although such models can outperform traditional model-based methods and adapt to new scenarios, their black-box nature raises concerns about trust and robustness. In contrast, methods that derives explicit mathematical expressions directly from data, without assuming a predefined model structure, e.g,, symbolic/sparse regression. This makes these methods particularly useful for describing physical phenomena that lack explicit mathematical formulations or are too complex to derive analytically. Moreover, they have been observed to uncover new, interpretable relationships hidden in the data, making it well suited for approximating complex behaviors such as friction torque, whose precise characterization is difficult due to its dependence on multiple interacting factors. 

A useful historical analogy is the progression from Ke- 

pler’s and Newton’s descriptions of planetary motion. Kepler’s laws provided an accurate, data-driven description of orbits, but they remained essentially empirical and system-specific. Newton’s formulation, on the other hand, introduced a simple and interpretable law of gravitation that explained Kepler’s observations, generalized far beyond the original data, and ultimately enabled engineered capabilities such as interplanetary navigation. In a similar spirit, a highly accurate but opaque neural network model of joint torques plays a role akin to Kepler’s descriptive laws, whereas an explicit, low-complexity model of the robot dynamics corresponds more closely to Newton’s formulation: it can be inspected, trusted, and reused for analysis, controller design, and extrapolation beyond the training conditions. This motivates the search for data-driven models of robot dynamics that are not only accurate, but also sparse and interpretable. 

In this paper, we focus on developing interpretable and accurate dynamic models. Concretely, we model joint-space dynamics as an analytical rigid-body model plus a datadriven residual, and investigate the affect of using symbolic regression and SINDy-style sparse regression on joint-space features to identify closed-form expressions for this residual from data. We validate the approach in simulation on a 7-DoF Franka arm with known dynamics, showing that the recovered expressions accurately reconstruct known dynamics equations and substantially outperform neural-network baselines in both accuracy and generalization. We then apply the same methodology to real data from a 7-DoF WAM arm, comparing symbolic and sparse models against neural networks, and analyzing how each class trades off in-sample fit, out-ofsample generalization, and interpretability. Throughout, we emphasize models that not only predict joint torques well but also expose physically meaningful structure that can be inspected and potentially reused for tasks such as virtual force sensing, controller design, and physically grounded robot learning. 

## II. PROBLEM FORMULATION 

For an _n_ -DoF robot, the joint-space dynamics is given by 


where _τm ∈_ R<sup>_n_</sup> are the motor joint torques, _τdyn ∈_ R<sup>_n_</sup> are the torques due to the internal robot dynamics, and _τext ∈_ R<sup>_n_</sup> are external joint torques. 

A common model used to estimate _τdyn_ is the rigid-body dynamics equations of motion 


where _M_ ( _·_ ) _∈_ R<sup>_n×n_</sup> is the inertia matrix, _C_ ( _·_ ) _∈_ R<sup>_n×n_</sup> is the Coriolis matrix, _τg_ ( _·_ ) _∈_ R<sup>_n_</sup> is the gravitational torque, and _q, q,_ ˙ ¨ _q ∈_ R<sup>_n_</sup> are the joint position, velocity, and acceleration, respectively. For sufficiently rigid/heavy robots whose dynamics are dominated by inertial effects, _τrbd_ often provides a good approximation of _τdyn_ . In general, however, unmodeled effects (e.g., friction, actuator dynamics, or flexibilities) can lead to a 

significant mismatch between the true internal dynamics _τdyn_ and the model _τrbd_ , i.e. 


where _ϵ ∈_ R<sup>_n_</sup> denotes the modeling error such that _∥ϵ∥_ is non-negligible. The error can depend on nonlinear relationship with the motion of the joints, coupling effects of the joints, manufacturing mismatches, and potentially many other effects (e.g., temperature). Deriving a model for _ϵ_ by hand is errorprone and can be tedious for researchers. On the other hand, as mentioned above, neural networks have been observed to be good predictors of _ϵ_ , however, they are not interpretable, leading to lack of trust in real world applications. The goal of this work is to discover an interpretable, data-driven model for the error term _ϵ_ in (3). 

## III. RELATED WORK 

Before studying residual dynamic models, obtaining an accurate rigid-body model is essential. As early as 1986, Atkeson [13] demonstrated that inertial parameters can be identified using linear regression and least-squares techniques, showing on the PUMA manipulator that parameters estimated from the regressor form _w_ = _A ϕ_ produce torque predictions that significantly outperform CAD-based models. Sousa [14] later introduced the notion of enforcing physical feasibility in inertial parameter identification, observing that the physically feasible inertial parameters form a convex set and that these constraints can be expressed as Linear Matrix Inequalities (LMIs). This allows the identification problem to be solved via semidefinite programming while guaranteeing that _ϕ_ corresponds to a reliable mass distribution. Their experiments on the WAM manipulator demonstrated a framework for constrained and physically feasible parameter identification. The optimization problem required to identify these dynamic parameters is often ill-conditioned; consequently, a complementary line of work has focused on generating optimal excitation trajectories [15, 16]. 

While parameter identification for robotic manipulators is now relatively mature, the same process becomes substantially more challenging for legged robots because the common assumption of zero external torques does not hold. Khorshidi [17] addresses this difficulty by projecting the robot dynamics into the null space of contact forces with the nullspace projector _P_ ( _q_ ) = _Im − Jc_ ( _q_ )<sup>_†_</sup> _Jc_ ( _q_ ), yielding torque equations that are independent of ground reaction forces. They then identify the inertial parameters by solving the constrained optimization problem _ϕ_<sup>ˆ</sup> = arg min _ϕ ∥Y ϕ − τm∥_<sup>2</sup> s.t. _ϕ ∈ P_ phys, where _P_ phys encodes mass positivity, center-of-mass bounds, and inertia LMIs. The resulting physically consistent model achieves more reliable joints torque predictions than neural-network-based estimators, maintaining low prediction error across a wide range of tasks. 

A widely adopted strategy for improving robot dynamics models is to learn the residual mismatch between the true dynamics and the nominal model, because this residual is usually much smoother than the full dynamics and can thus 

be captured effectively with Gaussian Processes (GPs). Carron [18] implement this idea by training a GP prior to approximate the model error _d_ ( _x, u_ ) in the discrete-time system dynamics _xk_ +1 = _Axk_ + _Buk_ + _Bd_ � _d_ ( _xk, uk_ ) + _d_<sup>¯</sup> �, where the constant offset noise _d_<sup>¯</sup> is estimated online via an extended Kalman Filter (EFK). In their formulation, the GP mean _µd_ ( _x, u_ ) provides a feedforward compensation to the nominal inverse-dynamics model, while the GP covariance Σ _d_ ( _x, u_ ) contributes to the predicted state covariance Σ _x_ , which is used in chance constraints within the Model Predictive Control (MPC) horizon. Experiments on a compliant 6-DoF robotic arm show substantial tracking improvements compared to both PID and nominal MPC baselines. However, given its intrinsic properties, GP-based residual modeling is fundamentally limited. Because the GP is trained offline and must be sparsified to remain computationally feasible at 1 kHz control rates, this residual model cannot adapt to changing dynamics. Moreover, GP models cannot automatically capture complex physical effects without appropriately designed kernels, which leads to a strong sensitivity to hyperparameter tuning. Its accuracy is constrained by the risk of overfitting, which ultimately highlights the strong dependence of GP-based residual models on the distribution of the training task data. 

Recently, Scholl used symbolic regression to learn an interpretable friction model for the KUKA LWR robot arm [19] where _ϵ_<sup>(</sup><sup>_j_)</sup> = _τf_<sup>(</sup><sup>_j_)( ˙</sup><sup>_q_(</sup><sup>_j_)</sup><sup>_, τ_</sup> _g_<sup>(</sup><sup>_j_))and</sup><sup>_j_indicatesthemodel</sup> is per joint. By operating the robot at low, near-constant velocities, i.e. _q,_ ˙ ¨ _q, C_ ( _q, q_ ˙) ˙ _q ≈_ 0 _n_ , and assuming zero external torques _τext_ = 0 _n_ they were able to simplify the dynamic model _τm_ = _τg_ ( _q_ ) + _ϵ_ and thus uncover a model for _ϵ_ using symbolic regression. Whilst the work by Scholl et al provides early validation that symbolic regression is useful for modeling dynamic effects, the work is limited. Their approach identifies a quasi-static, per-joint friction law only in a narrow operating regime: near-zero accelerations, low velocities, and single-joint motions. As a result, the learned model does not account for dynamic friction phenomena (e.g. hysteresis, pre-sliding) or joint–joint coupling effects, and it strongly relies on an accurate rigid-body model to remove inertial and Coriolis contributions. Moreover, the symbolic expressions are unconstrained outside the identification domain, so there is no guarantee that the inferred friction model extrapolates sensibly to higher velocities, larger accelerations, or more aggressive, multi-joint trajectories. 

## IV. METHODS FOR INTERPRETABLE DYNAMICS 

Two common approaches are considered in this work for inferring interpretable dynamics models from motion data. 

## _A. Symbolic regression_ 

Symbolic regression is a supervised learning approach in which the goal is to discover an explicit analytic expression that relates input variables to a target quantity, rather than fitting the parameters of a fixed model class. Given a dataset _D_ = _{_ ( _xi, yi_ ) _}_<sup>_N_</sup> _i_ =1<sup>,symbolicregressionsearchesovera</sup> space _F_ of candidate expressions built from basic operators 

(e.g. + _, −, ×, /,_ exp _,_ log _,_ sin _, . . ._ ), input variables, and free numerical constants to find a closed-form function _f_ : R<sup>_d_</sup> _→_ R that explains the data [20]. 

Formally, one can view symbolic regression as the problem 


where _L_ is a loss function that evaluates candidate expressions _f_ on the data. In contrast to typical regression techniques, where the functional form is fixed in advance (e.g. linear models, polynomials of fixed degree, neural networks) and only the parameters are optimized, symbolic regression treats both the structure of the expression and its numerical constants as unknowns. Thus, the loss _L_ is typically designed to reflect a trade-off between predictive accuracy and some notion of simplicity, so that the selected expressions are not only accurate on the observed data but also compact and interpretable. This is beneficial compared to models such as neural networks, which are often treated as black boxes, since the resulting expressions can be directly inspected and analyzed. Modern tools such as PySR [20] implement this paradigm using heuristic search procedures to explore the large, discrete space _F_ while maintaining this balance between fit quality and model simplicity, and have been used to derive physics models in various applications (e.g. particle physics [21]). 

## _B. Sparse identification of Nonlinear Dynamics_ 

Sparse identification of nonlinear dynamics (SINDy) is a data-driven framework for discovering governing equations of dynamical systems from time-series data [22]. Given measurements of the system state _{xi}_<sup>_N_</sup> _i_ =1<sup>andcorresponding</sup> (estimated) time derivatives _{_ ˙ _xi}_<sup>_N_</sup> _i_ =1<sup>,SINDyassumesthatthe</sup> dynamics can be expressed as a sparse linear combination of candidate nonlinear functions. To this end, one constructs a feature library Θ( _X_ ) _∈_ R<sup>_N×p_</sup> , whose columns contain nonlinear transformations of the states (and possibly inputs), such as polynomials, trigonometric functions, or other userspecified basis functions. The dynamical model is then written as _X_<sup>˙</sup> _≈_ Θ( _X_ ) Ξ where _X_<sup>˙</sup> _∈_ R<sup>_N×d_</sup> stacks the time derivatives and Ξ _∈_ R<sup>_p×d_</sup> is a matrix of coefficients. Identifying the dynamics reduces to solving a regression problem for Ξ with a sparsity-promoting procedure (e.g. sequentially thresholded least squares), so that only a small subset of candidate terms remains active in each column. The resulting models are compact and interpretable, since each retained term corresponds to a specific mechanism in the dynamics. 

In this work, we do not use SINDy to identify an explicit evolution law _x_ ˙ = _f_ ( _x_ ), but instead adapt the same sparseregression machinery to learn a general input–output mapping _y_ = _g_ ( _x_ ). Conceptually, this amounts to replacing the timederivative matrix _X_ ˙ in the standard SINDy formulation by a target matrix _Y_ collecting the quantities of interest, while keeping the construction of the nonlinear feature library and the sparsity-enforcing regression procedure unchanged. The identification step then becomes 


Fig. 1: Visualization of the simulated 7-DoF Franka Robot arm. Note, in our experiments we only use PyBullet to visualize the robot, we use our own simulator definition. 

so that one recovers a sparse combination of basis functions that best predicts the target signal from the input features. This viewpoint casts our approach as a SINDy-inspired sparse polynomial regression, reusing the standard SINDy components (feature libraries, sparsity-promoting solvers, and their implementation in PySINDy [23]) in a supervised regression setting rather than for explicit time-derivative modeling. 

## V. EXPERIMENTS 

In this section, we report our experimental findings. 

## _A. Validation of pipeline in simulation_ 

A simulator was developed using a fixed-base 7-DoF Franka Emika Panda robot arm, shown in Fig. 1. In these initial experiments, our primary objective is to validate the overall pipeline and evaluation infrastructure for the approaches considered in this study. It is important to note that PyBullet [24] is used only as a visualizer in this initial experimental setup; all robot dynamics are simulated using a known analytical rigid-body model of the Franka arm implemented in Pinocchio [25]. This design choice provides a clean benchmark in which modeling errors and low-level simulation artifacts are removed, allowing us to attribute the observed behavior directly to the algorithms under study. Note, the simulator developed in this section assumes no external torques, i.e, _τext_ = 07. This means by (1), that predicting _τdyn_ is equivalent to predicting _τm_ . 

_1) Simulator:_ The robot is modeled as a 7-DoF manipulator with joint configuration _q ∈_ R<sup>7</sup> and joint velocities _q_ ˙ _∈_ R<sup>7</sup> . The joint-space dynamics are written as 


where _M_ ( _q_ ) _∈_ R<sup>7</sup><sup>_×_7</sup> is the joint-space inertia matrix, _C_ ( _q, q_ ˙) ˙ _q_ collects Coriolis and centrifugal terms, and _τg_ ( _q_ ) is the generalized gravity torque. 

A diagonal viscous damping model is used, 


where _D_ = diag( _d_ 1 _, . . . , d_ 7) _∈_ R<sup>7</sup><sup>_×_7</sup> is a diagonal matrix with positive diagonal elements, i.e., _di >_ 0 for all _i_ = 1:7. Given commanded motor torques _τm ∈_ R<sup>7</sup> , the effective torques (6) are found by the residual 


where _τd_ = _τd_ ( ˙ _q_ ). By including the damping model (7) in (8), we introduce a known, structured contribution to the effective torque that can serve as additional signal for the considered methods to identify and recover from data. 

The joint accelerations are computed by solving (6) for _q_ ¨, forming the forward dynamics, given by 


We use Pinocchio’s efficient implementation of the articulatedbody algorithm to compute (9). 

Given the state ( _qs, q_ ˙ _s_ ) and the effective torque _τeff,s_ at time step _s_ , we first compute _q_ ¨ _s_ using (9) and then the state is integrated using a semi-implicit (symplectic) Euler scheme with simulation time step ∆ _tsim_ . Thus, the next state is computed using 


This yields a deterministic simulator with known dynamics and full access to the true joint state. By substituting (8) into (6) and rearranging for _τm_ , provides us the model that we hope to uncover from motion data. The model we hope to discover is thus given by 


where _τi_ = _M_ ( _q_ )¨ _q_ , _τc_ = _C_ ( _q, q_ ˙) ˙ _q_ , and _τg_ = _τg_ ( _q_ ). 

_2) Controller:_ The low-level controller, used to compute the motor torques _τm_ is a joint-space PID law with gravity compensation. Given the desired joint positions _q_<sup>_⋆_</sup> _∈_ R<sup>7</sup> and velocities _q_ ˙<sup>_⋆_</sup> _∈_ R<sup>7</sup> , the motor torques are given by 


where _τg_ ( _q_ ) is the generalized gravity torque computed by Pinocchio, and _Kp, Ki, Kd ∈_ R<sup>7</sup> are diagonal matrices representing the PID gains. The integral term is updated at the controller (environment) sampling period ∆ _tenv_ and is clipped component-wise to prevent windup. 

This setup provides a clean testbed in which both the plant and the controller share the same perfect model of the robot, isolating the behavior of the proposed methods from modeling errors and sensor noise. 

_3) Data generation:_ In order to test our proposed datadriven approach, we require data collected from the simulator. This section describes the data generation and simulation steps. 

_a) Trajectory generation:_ To excite the dynamics of all joints, we generate joint-space reference trajectories as sums of sinusoidal signals. For each rollout, we first sample a random initial configuration _q_ 0 _∈_ R<sup>7</sup> inside the joint limits of the Franka arm, with a fixed margin subtracted from each bound to avoid saturating the joints. Formally, if _q_ min _, q_ max _∈_ R<sup>7</sup> denote the lower and upper joint limits respectively and 0 _< ρ ∈_ R is a fixed margin, we sample 


where _U_ ( _a, b_ ) represents a uniform distribution with lower and upper bounds _a, b ∈_ R<sup>7</sup> such that _aj < bj_ for all _j_ = 1:7, and _e_ = [1 _, . . . ,_ 1]<sup>_T_</sup> _∈_ R<sup>7</sup> is the vector of ones. We then construct a time grid _{tk}_<sup>_N_</sup> _k_ =0<sup>overahorizon</sup><sup>_T_withsamplingperiod</sup> ∆ _tenv_ . For each joint _j_ = 1:7, we form a multi-sine signal 


where _nm_ is the number of sinusoidal modes per joint and the amplitudes _ajℓ_ , frequencies _fjℓ_ , and phases _ϕjℓ_ are drawn independently from uniform distributions over prescribed ranges. The corresponding velocity signal is obtained analytically as 


Each pair � _qraw,j, q_ ˙ _raw,j_ � is then scaled by a single factor such that the resulting joint positions and velocities remain within the (shrunken) position limits and the nominal velocity limits of joint _j_ . Formally, for each joint _j_ we define the available position margin around the initial configuration _q_ 0 _,j_ as 


where _q_ min _,j_ and _q_ max _,j_ denote the _j_ th components of _q_ min and _q_ max, respectively. Let _q_ ˙max _∈_ R<sup>7</sup> denote the jointvelocity limits and define 


with a small 0 _< ε ∈_ R such that _|ε| ≪_ 1 to avoid division by zero. The final scaling factor is then 


and the discrete desired trajectories are obtained as 


This yields discrete desired trajectories _q_<sup>_⋆_</sup> ( _tk_ ) and _q_ ˙<sup>_⋆_</sup> ( _tk_ ). Using the above procedure and 

_b) Simulation:_ Given desired trajectories _q_<sup>_⋆_</sup> ( _tk_ ) _, q_ ˙<sup>_⋆_</sup> ( _tk_ ) for _k_ = 0: _N_ , we simulate the closed-loop system consisting of the Franka simulator and the joint-space PID controller described in the previous sections. The initial state is set to 


At each environment step _k_ = 0: _N −_ 1, the controller computes a motor torque command _τm_ using (12), which is held constant while the plant is integrated for a fixed number of smaller integration sub-steps using the semi-implicit Euler scheme (10). The resulting joint states _qk_ +1 and _q_ ˙ _k_ +1 are recorded at the environment rate ∆ _tenv_ . 

For each rollout we thus obtain sequences _{qk}_<sup>_N_</sup> _k_ =0<sup>_, {_˙</sup><sup>_qk}N_</sup> _k_ =0<sup>_, {τm,k}N_</sup> _k_ =0<sup>_−_1,</sup> representing the joint positions, joint velocities, and motor torque commands over the horizon, respectively, together with the reference signals _q_<sup>_⋆_</sup> ( _tk_ ), _q_ ˙<sup>_⋆_</sup> ( _tk_ ) and the time stamps _{tk}_<sup>_N_</sup> _k_ =0<sup>.Each</sup> rollout is stored on disk as a separate trajectory, and a dataset is obtained by repeating this procedure for multiple independently sampled reference trajectories. 

We used the above procedure to generate 10 training trajectories and 10 test trajectories. An example of a trajectory generated by the above procedure and resulting rollout in the simulator are shown in Figure 2. 

_4) Training and evaluation:_ The trajectories collected are split into disjoint training and test sets. Each candidate data-driven dynamics approach takes as input the features _q, q,_ ˙ ¨ _q,_<sup>...</sup> _q , τi, τc, τg_ (i.e, the joint position, velocity, acceleration, jerk, inertia torques, Coriolis/centrifugal torques, and gravity torques respectively), and learns a mapping, such that _f_ : R<sup>49</sup> _→_ R<sup>7</sup> , which estimates the motor torques _τm_ , 


Note, the joint accelerations _q_ ¨ and jerk<sup>...</sup> _q_ are estimated using finite-differencing method. 

The models _f_ are fit on the training set only, and after training, we evaluate each model on both the training and test sets. For each set, we reconstruct the feature matrices and compute the corresponding torque predictions _τ_ � _m_ . Performance is quantified by a relative root-mean-square error (RMSE) per joint across each dataset. 

_5) Methods compared:_ As mentioned above, in the simulated setting, we have _τext_ = 0 in (1), so that _τm_ = _τdyn_ . Using the decomposition in (3), each method either approximates _τdyn_ directly from data, or explicitly uses the rigid-body model (2) and learns an approximation of the error term _ϵ_ . 

All models take as input the same feature vector 


constructed from the joint signals and the analytically computed inertia, Coriolis/centrifugal, and gravity torques. For the 7-DoF Franka arm used in the experiments, this corresponds to 7 variables of each type. Given _x_ , each model returns an estimate _τ_ � _m_ ( _x_ ). Symbolic-regression and SINDy-based models provide explicit closed-form expressions, whereas neuralnetwork models are treated as black-box baselines. 


Fig. 2: Example of a trajectory collected from our idealized simulator based on the 7-DoF Franka robot arm used in our validation experiments. Motor torques were computed using a controller implementing PID with gravity compensation. 

_a) Symbolic Regression (SR):_ The SR baseline directly learns a mapping _τsr_ : R<sup>49</sup> _→_ R<sup>7</sup> to approximate _τdyn_ (and hence _τm_ ) in (3), without explicitly using (2). We stack all training samples into matrices _X ∈_ R<sup>_N×_49</sup> and _Y ∈_ R<sup>_N×_7</sup> , where each row of _X_ is a feature vector _x_ and each row of _Y_ is the corresponding torque measurement _τm_ . For each joint _j_ = 1:7 we fit an independent scalar model 


using PySR [20], with a search space of algebraic expressions built from the input variables and the binary operators _{_ + _, −, ∗}_ (division is excluded). PySR is run in batching mode with batch size 10<sup>4</sup> , and the internal selection criterion balances mean-squared error on _Y_ and expression complexity. The result is a set of joint-wise, closed-form expressions _τsr,j_ that approximate _τdyn,j_ . 

_b) Sparse Identification of Nonlinear Dynamics (SINDy):_ The SINDy baseline, based on the work of Brunton et al [22], also approximates _τdyn_ directly, but constrains the model to be a sparse multivariate polynomial in the features. Starting from _X_ and _Y_ as above, we construct a polynomial feature library Θ( _X_ ) _∈_ R<sup>_N×p_</sup> using a basis of total degree up to 2, including all pairwise interactions and a bias term. We then learn a linear model 


with _W ∈_ R<sup>7</sup><sup>_×p_</sup> and _b ∈_ R<sup>7</sup> fitted jointly for all seven outputs using sequentially thresholded least-squares (STLSQ) with a sparsity threshold of 0 _._ 01, regularization parameter _α_ = 10<sup>_−_4</sup> , and at most 100 iterations. The resulting _τsindy_ is an explicit sparse polynomial approximation of _τdyn_ in (3). To implement this approach we utilized the PySINDy library [23]. 

_c) Hybrid RBD and SR (r-SR):_ The r-SR model uses the decomposition in (3) explicitly. For each training sample, we compute _τrbd_ ( _q, q,_ ˙ ¨ _q_ ) from the known Franka model and form the residual target _y_ = _τm − τrbd._ (27) 

We then train seven independent PySR models on ( _x, yj_ ), exactly as in the SR baseline, obtaining a residual estimate 


At test time, the prediction is 


so that r-SR can be interpreted as a symbolic model of the error term _ϵ_ in (3). 

_d) Hybrid RBD and SINDy (r-SINDy):_ The r-SINDy model follows the same residual-learning strategy, but represents _ϵ_ via a SINDy model. After computing _τrbd_ , we form residual targets _Yres_ = _τm − τrbd_ (30) 

and reuse the same polynomial library Θ( _X_ ) as in the SINDy baseline. We then fit 


using STLSQ with identical hyperparameters. The hybrid prediction is 


yielding an interpretable sparse polynomial approximation of the error term in (3). 

_e) Hybrid RBD, SINDy, and SR (r-SINDy-SR):_ The r- SINDy-SR model refines the r-SINDy approximation of _ϵ_ by adding a second, symbolic residual layer. First, a hybrid RBD–SINDy model 


is trained as above and kept fixed. We then define a second residual 


which can be viewed as a two-layer approximation of the error term _ϵ_ in (3). 

_f) Neural Network (NN):_ The NN baseline directly parametrizes _τdyn_ by a fully connected neural network. We use a multilayer perceptron 


with two hidden layers of width 128 and rectified-linear (ReLU) activations. The network is trained on the concatenated dataset using mean-squared error loss between _τnn_ ( _x_ ) and _τm_ , the Adam optimizer with learning rate 10<sup>_−_4</sup> , batch size 1024, and 100 training epochs. In the notation of (3), this model implicitly learns _τdyn_ (and hence _ϵ_ ) without imposing an explicit structure. 

_g) Hybrid RBD and NN (r-NN):_ Finally, the r-NN model combines the rigid-body model with a neural approximation of the error term _ϵ_ in (3). As in the other hybrid methods, we first compute _τrbd_ and form residual targets 


We then train an “error network” _ferr_ , with the same architecture as the NN baseline, to map _x_ to an estimate 


During training, the loss is evaluated on 


against the measured _τm_ , so that the network explicitly learns to correct the analytical model. At test time the hybrid prediction is 


which matches the decomposition in (3) with � _ϵ_ represented by a neural network. 

TABLE I: Training set RMSE per joint for the Franka simulation. 

|Joint|SR|SINDy|r-SR|r-SINDy|r-SINDy-SR|NN|r-NN|
|---|---|---|---|---|---|---|---|
|1|0.002|**0.002**|0.002|0.002|**0.002**|0.072|0.041|
|2|**0.001**|**0.001**|**0.001**|**0.001**|**0.001**|0.092|0.025|
|3|0.002|**0.002**|0.002|0.002|**0.002**|0.084|0.062|
|4|0.002|0.002|0.002|0.002|**0.002**|0.065|0.041|
|5|**0.002**|0.003|0.003|0.003|0.003|0.138|0.071|
|6|**0.002**|0.003|0.003|0.003|0.003|0.163|0.087|
|7|0.003|0.003|0.003|0.003|**0.003**|0.168|0.111|


TABLE II: Test set RMSE per joint for the Franka simulation. 

|Joint|SR|SINDy|r-SR|r-SINDy|r-SINDy-SR|NN|r-NN|
|---|---|---|---|---|---|---|---|
|1|0.002|**0.002**|0.002|0.002|**0.002**|0.687|0.994|
|2|0.001|0.001|0.001|0.001|**0.001**|0.267|0.244|
|3|0.002|**0.002**|0.002|0.002|**0.002**|0.388|0.628|
|4|0.002|0.002|0.002|0.002|**0.002**|0.300|0.251|
|5|**0.003**|0.003|0.003|0.003|0.003|0.679|0.624|
|6|**0.003**|0.003|0.003|0.003|0.003|1.111|0.424|
|7|**0.004**|**0.004**|**0.004**|**0.004**|**0.004**|1.356|0.986|


_6) Results:_ Table I reports the per-joint relative RMSE on the training set, while Table II shows the corresponding errors on the test set. Across both sets, the SR, SINDy, r-SR, r- SINDy, and r-SINDy-SR models achieve virtually identical performance, with relative RMSEs on the order of 10<sup>_−_3</sup> –10<sup>_−_2</sup> for all seven joints. In particular, the best-performing method for each joint (shown in bold) is always one of these interpretable models, and the numerical differences between them are negligible at the scale of the metric. This indicates that, in the simulated setting where _τrbd_ is computed from the same analytical model used to generate the data, both the purely data-driven (SR, SINDy) and hybrid variants are able to recover the internal dynamics _τdyn_ essentially perfectly. 

Comparing training and test performance, we observe that the SR, SINDy and all hybrid models generalize very well: their test RMSEs closely match the training RMSEs for every joint. This is consistent with the fact that the simulator defines a smooth, low-noise mapping from the feature vector _x_ to _τm_ , which can be represented accurately either as a sparse polynomial or as a compact symbolic expression. The hybrid models do not exhibit a clear systematic advantage over their non-hybrid counterparts in this setting, which is expected since _τrbd_ already matches the true rigid-body component of the dynamics and the remaining error term _ϵ_ is relatively small and structured. 

In contrast, the neural-network baselines perform significantly worse. On the training set, the NN and r-NN models exhibit relative RMSEs between roughly 0 _._ 02 and 0 _._ 17 depending on the joint, already one to two orders of magnitude larger than those of the interpretable models. On the test set, the degradation is much more pronounced: test RMSEs for the NN and r-NN models reach values between 0 _._ 24 and 1 _._ 36 across the seven joints, indicating poor generalization despite having access to the same feature vector _x_ . The hybrid r-NN model slightly improves training errors over the pure NN but does not consistently reduce test errors, suggesting that, in this idealized setting, simply adding a neural residual on top of _τrbd_ does not overcome the optimization and generalization 

challenges of the black-box model. 

Table III reports the closed-form expressions identified by the interpretable methods and enables a direct comparison with the target structure in (11) and the error decomposition in (3). For the purely data-driven SR and SINDy models, the learned expressions closely match the desired superposition of inertial, Coriolis/centrifugal, gravity, and viscous contributions. Across all joints, the coefficients multiplying _τi,j_ , _τc,j_ , and _τg,j_ are essentially equal to one (up to small _O_ (10<sup>_−_3</sup> ) deviations), indicating that both methods correctly recover the known rigidbody components from data. Moreover, the estimated viscous coefficients _ξ_<sup>(</sup><sup>_j_)</sup> on _q_ ˙ _j_ agree very well with the nominal damping coefficients _dj_ , with relative discrepancies below 1% for all joints. For joints 5 and 6, SR additionally introduces jerk terms<sup>...</sup> _q j_ with very small magnitude (on the order of 10<sup>_−_5</sup> –10<sup>_−_4</sup> ), consistent with the negligible higher-order corrections suggested by the low RMSE values in Tables I and II. 

The hybrid models further confirm that the dominant unmodeled dynamics in this setup are well captured by a simple viscous term. Both r-SR and r-SINDy recover _ϵj_ as a scalar multiple of _q_ ˙ _j_ that is numerically indistinguishable from _dj_ , with only very small jerk corrections for joints 5 and 6 in the r- SR case. In contrast, the r-SINDy-SR model, which refines the hybrid RBD–SINDy estimate, learns only very small residual structures in terms of accelerations _q_ ¨ _j_ (and a single tiny cross term involving _q_ ˙1 for joint 3), with coefficients on the order of 10<sup>_−_3</sup> or smaller. Taken together, these results show that once the rigid-body model and a joint-wise viscous damping term are accounted for, there is little systematic structure remaining in the residual, and the interpretable methods converge to compact, physically meaningful expressions that are consistent with the known simulated dynamics. 

_7) Discussion:_ Overall, these results show that in a noisefree environment with a known rigid-body model, interpretable sparsity-promoting methods (SR, SINDy and their hybrid variants) can recover a highly accurate model of _τdyn_ and the error term _ϵ_ in (3), whereas standard neural-network baselines struggle to match their accuracy and generalization. The symbolic models not only achieve low training and test RMSE across all joints, but also recover coefficients that are numerically consistent with the known viscous damping and rigid-body terms, and expose any remaining structure in the residual as small, easily interpretable corrections (e.g., weak jerk or acceleration terms). 

By contrast, the pure NN and hybrid RBD–NN baselines exhibit clear signs of overfitting in this setting, attaining low training error but substantially worse test performance and offering no direct insight into the underlying physical structure of the dynamics. Taken together, the simulation study validates that, when a reasonable mechanistic model is available and the data are sufficiently informative, interpretable sparse regression can serve as a powerful tool to identify both _τdyn_ and _ϵ_ in (3), combining prediction accuracy with physically meaningful, human-readable models that can be inspected, validated, and potentially modified by a designer. 

## _B. Analysis on real world data from WAM robot arm_ 

The previous section provided evidence that interpretable methods can be used to discover dynamics models from data. Also, the experimental pipeline developed was validated. In this section, we wish to apply and analyze these interpretable methods on real world data collected from the 7-DoF WAM robot arm. 

_1) Dataset:_ The dataset for the experiments in this section was sourced from the work of Sousa and Cortes˜ao [14], available at github.com/cdsousa/wam7 <u>dyn ident.</u> 

Estimating time derivatives from noisy joint trajectories is delicate, since standard finite-difference schemes tend to amplify measurement noise and can severely degrade the quality of learned models. For the WAM data, we therefore computed joint velocity, acceleration, and jerk using a smoothed finite-difference method based on the total-variationregularized differentiation framework of Chartrand [26]. In this approach, the derivative signal is obtained as the minimizer of a small variational problem that balances a least-squares fit to the noisy measurements with a total-variation penalty on the derivative, effectively enforcing a piecewise-smooth derivative that suppresses high-frequency noise while still allowing sharp changes. We apply this procedure independently to each joint trajectory before constructing the feature matrices. 

The dataset provided by Sousa and Cortes˜ao [14] contains four robot trajectories, all containing about one minute of robot motion collected at a sampling frequency of 1 kHz. We used three trajectories as part of the training dataset and one as test dataset. An example of the joint positions provided in the dataset, along with the estimated velocities, accelerations and jerk (estimated using the smoothed finite differencing method described above) is shown in Figure 3. 

_2) Results:_ Table IV reports the per-joint relative RMSE on the WAM training set, and Table V shows the corresponding errors on the test set. On the training data, the SINDy-based models (SINDy, r-SINDy, r-SINDy-SR) achieve the lowest RMSE for every joint, with values between roughly 0 _._ 03 and 0 _._ 18, i.e., substantially smaller than those of SR and r-SR (about 0 _._ 14–0 _._ 65) and somewhat better than the NN and r-NN baselines (about 0 _._ 03–0 _._ 33). Thus, in terms of in-sample fit, the sparse-regression models remain very effective at capturing the observed joint torques on this system. 

The generalization behavior on the WAM test set, however, is dramatically different across model classes. The SINDy and SINDy-based hybrid models suffer from severe overfitting: their test RMSEs increase by two to three orders of magnitude compared to training, reaching values between approximately 4 and 60 depending on the joint. In contrast, the SR and r-SR models exhibit much more stable behaviour, with test RMSEs in the range 0 _._ 18–0 _._ 58 that remain close to their training errors. For most joints, the best-performing method on the WAM test set (highlighted in bold in Table V) is therefore SR or r-SR, indicating that the symbolic-regression models provide the most robust out-of-sample performance in this setting. 

TABLE III: Closed-form models identified by the interpretable methods on a known dynamics model. We used [6 _._ 75 _,_ 6 _._ 00 _,_ 5 _._ 25 _,_ 4 _._ 50 _,_ 3 _._ 75 _,_ 3 _._ 00 _,_ 2 _._ 25]<sup>_⊤_</sup> for the nominal viscous damping coefficients. 

|_j_<br>1|Expected m|odel||Identified model<br>Coefficients<br>_ξ_<sup>(1)</sup><br>_τ_+_ξ_<sup>(1)</sup><br>_τ_+_ξ_<sup>(1)</sup><br>˙<br>_ξ_<sup>(1)</sup><br>=1_ξ_<sup>(1)</sup><br>=1_ξ_<sup>(1)</sup><br>=6721|
|---|---|---|---|---|
|||||1<br>_i,_1  <br>2<br>_c,_1  <br>3<br>_q_1<br><br>1<br> _, _<br>2<br> _, _<br>3<br> _._<br><br><br><br><br><br><br><br>|
|2||||_ξ_<sup>(2)</sup><br>1<br>_τi_2 + _ξ_<sup>(2)</sup><br>2<br>_τc_2 + _ξ_<sup>(2)</sup><br>3<br>_τ_2 + _ξ_<sup>(2)</sup><br>4<br>˙_q_2<br>_ξ_<sup>(2)</sup><br>1<br>= 1_, ξ_<sup>(2)</sup><br>2<br>= 1_, ξ_<sup>(2)</sup><br>3<br>= 1_, ξ_<sup>(2)</sup><br>4<br>= 5_._962|
|SR<br>3|(11)|||_,_ <br><br>_,_ <br><br>_g,_ <br><br><br><br><br><br><br><br><br><br><br>_ξ_<sup>(3)</sup><br>1<br>_τi,_3 + _ξ_<sup>(3)</sup><br>2<br>_τc,_3 + _ξ_<sup>(3)</sup><br>3<br>_τg,_3 + _ξ_<sup>(3)</sup><br>4<br>˙_q_3<br>_ξ_<sup>(3)</sup><br>1<br>= 1_, ξ_<sup>(3)</sup><br>2<br>= 1_, ξ_<sup>(3)</sup><br>3<br>= 1_, ξ_<sup>(3)</sup><br>4<br>= 5_._235<br><br><br><br><br><br><br><br>|
|4||||_ξ_<sup>(4)</sup><br>1<br>_τi,_4 + _ξ_<sup>(4)</sup><br>2<br>_τc,_4 + _ξ_<sup>(4)</sup><br>3<br>_τg,_4 + _ξ_<sup>(4)</sup><br>4<br>˙_q_4<br>_ξ_<sup>(4)</sup><br>1<br>= 1_, ξ_<sup>(4)</sup><br>2<br>= 1_, ξ_<sup>(4)</sup><br>3<br>= 1_, ξ_<sup>(4)</sup><br>4<br>= 4_._486<br><br><br><br><br><br><br><br>|
|5||||_ξ_<sup>(5)</sup><br><br>_τi_5 + _ξ_<sup>(5)</sup><br><br>_τ_5 + _ξ_<sup>(5)</sup><br><br>_τ_5 + _ξ_<sup>(5)</sup><br><br>˙_q_5 + _ξ_<sup>(5)</sup><br><br>...<br>_q_5<br>_ξ_<sup>(5)</sup><br><br>_≈_1_._001_, ξ_<sup>(5)</sup><br><br>= 1_, ξ_<sup>(5)</sup><br><br>= 1_,_|
|||||1<br>_,_ <br>2<br>_c,_ <br>3<br>_g,_ <br>4<br> <br>5<br><br><br>1<br><br>2<br><br>3<br><br>_ξ_<sup>(5)</sup><br>4<br>_≈_3_._741_, ξ_<sup>(5)</sup><br>5<br>_≈_5_._2 _×_ 10<sup>_−_5</sup>|
|6||||_ξ_<sup>(6)</sup><br>1<br>_τi,_6 + _ξ_<sup>(6)</sup><br>2<br>_τc,_6 + _ξ_<sup>(6)</sup><br>3<br>_τg,_6 + _ξ_<sup>(6)</sup><br>4<br>˙_q_6 + _ξ_<sup>(6)</sup><br>5<br>...<br>_q_6<br>_ξ_<sup>(6)</sup><br>1<br>_≈_1_._001_, ξ_<sup>(6)</sup><br>2<br>= 1_, ξ_<sup>(6)</sup><br>3<br>= 1_,_<br>_ξ_<sup>(6)</sup><br><br>_≈_2_._993_, ξ_<sup>(6)</sup><br><br>_≈_1_._0 _×_ 10<sup>_−_4</sup>|
|7||||4<br><br>5<br>_ξ_<sup>(7)</sup><br>1<br>_τi,_7 + _ξ_<sup>(7)</sup><br>2<br>_τc,_7 + _ξ_<sup>(7)</sup><br>3<br>˙_q_7<br>_ξ_<sup>(7)</sup><br>1<br>= 1_, ξ_<sup>(7)</sup><br>2<br>= 1_, ξ_<sup>(7)</sup><br>3<br>= 2_._244|
|1||||_ξ_<sup>(1)</sup><br>1<br>_τi,_1 + _ξ_<sup>(1)</sup><br>2<br>_τc,_1 + _ξ_<sup>(1)</sup><br>3<br>˙_q_1<br>_ξ_<sup>(1)</sup><br>1<br>= 1_._001_, ξ_<sup>(1)</sup><br>2<br>= 1_._001_, ξ_<sup>(1)</sup><br>3<br>= 6_._721<br><br><br><br><br><br><br><br>|
|2||||_ξ_<sup>(2)</sup><br><br>_τi_2 + _ξ_<sup>(2)</sup><br><br>_τ_2 + _ξ_<sup>(2)</sup><br><br>_τ_2 + _ξ_<sup>(2)</sup><br><br>˙_q_2<br>_ξ_<sup>(2)</sup><br><br>= 1_, ξ_<sup>(2)</sup><br><br>= 1_._001_, ξ_<sup>(2)</sup><br><br>= 1_, ξ_<sup>(2)</sup><br><br>= 5_._962|
|INDy<br>3|(11)|||1<br>_,_ <br>2<br>_c,_ <br>3<br>_g,_ <br>4<br><br><br>1<br><br>2<br><br>3<br><br>4<br>_ξ_<sup>(3)</sup><br>1<br>_τi,_3 + _ξ_<sup>(3)</sup><br>2<br>_τc,_3 + _ξ_<sup>(3)</sup><br>3<br>_τg,_3 + _ξ_<sup>(3)</sup><br>4<br>˙_q_3<br>_ξ_<sup>(3)</sup><br>1<br>= 1_._001_, ξ_<sup>(3)</sup><br>2<br>= 1_._002_, ξ_<sup>(3)</sup><br>3<br>= 1_, ξ_<sup>(3)</sup><br>4<br>= 5_._234|
|S<br>4||||_ξ_<sup>(4)</sup><br>1<br>_τi,_4 + _ξ_<sup>(4)</sup><br>2<br>_τc,_4 + _ξ_<sup>(4)</sup><br>3<br>_τg,_4 + _ξ_<sup>(4)</sup><br>4<br>˙_q_4<br>_ξ_<sup>(4)</sup><br>1<br>= 1_, ξ_<sup>(4)</sup><br>2<br>= 1_._001_, ξ_<sup>(4)</sup><br>3<br>= 1_, ξ_<sup>(4)</sup><br>4<br>= 4_._486<br><br><br><br><br><br><br><br>|
|5||||_ξ_<sup>(5)</sup><br>1<br>_τi,_5 + _ξ_<sup>(5)</sup><br>2<br>_τc,_5 + _ξ_<sup>(5)</sup><br>3<br>_τg,_5 + _ξ_<sup>(5)</sup><br>4<br>˙_q_5<br>_ξ_<sup>(5)</sup><br>1<br>= 1_._001_, ξ_<sup>(5)</sup><br>2<br>= 1_, ξ_<sup>(5)</sup><br>3<br>_≈_0_._9997_, ξ_<sup>(5)</sup><br>4<br>= 3_._741<br><sup>6</sup><br><sup>6</sup><br><sup>6</sup><br><sup>6</sup><br><sup>6</sup><br><sup>6</sup><br><sup>6</sup><br><sup>6</sup>|
|6||||_ξ_<sup>()</sup><br>1<br>_τi,_6 + _ξ_<sup>()</sup><br>2<br>_τc,_6 + _ξ_<sup>()</sup><br>3<br>_τg,_6 + _ξ_<sup>()</sup><br>4<br>˙_q_6<br>_ξ_<sup>()</sup><br>1<br>= 1_._001_, ξ_<sup>()</sup><br>2<br>= 1_._001_, ξ_<sup>()</sup><br>3<br>= 1_, ξ_<sup>()</sup><br>4<br>= 2_._991|
|7||||_ξ_<sup>(7)</sup><br>1<br>_τi,_7 + _ξ_<sup>(7)</sup><br>2<br>_τc,_7 + _ξ_<sup>(7)</sup><br>3<br>˙_q_7<br>_ξ_<sup>(7)</sup><br>1<br>= 1_._001_, ξ_<sup>(7)</sup><br>2<br>= 1_._001_, ξ_<sup>(7)</sup><br>3<br>= 2_._244<br><br>|
|1||||_ξ_<sup>(1)</sup><br>1<br>˙_q_1<br>_ξ_<sup>(1)</sup><br>1<br>= 6_._721<br><sup>2</sup><br><sup>2</sup>|
|2||||_ξ_<sup>()</sup><br>1<br>˙_q_2<br>_ξ_<sup>()</sup><br>1<br>= 5_._962|
|r-SR<br>3|_ϵj_ = _dj_|˙_qj_||_ξ_<sup>(3)</sup><br>1<br>˙_q_3<br>_ξ_<sup>(3)</sup><br>1<br>= 5_._235<br><br>|
|4||||_ξ_<sup>(4)</sup><br>1<br>˙_q_4<br>_ξ_<sup>(4)</sup><br>1<br>= 4_._486<br><br><br><br><br>|
|5||||_ξ_<sup>(5)</sup><br>1<br>˙_q_5 + _ξ_<sup>(5)</sup><br>2<br>...<br>_q_5<br>_ξ_<sup>(5)</sup><br>1<br>= 3_._742_, ξ_<sup>(5)</sup><br>2<br>_≈_5_._2 _×_ 10<sup>_−_5</sup>|
|6||||_ξ_<sup>(6)</sup><br>1<br>˙_q_6 + _ξ_<sup>(6)</sup><br>2<br>...<br>_q_6<br>_ξ_<sup>(6)</sup><br>1<br>= 2_._994_, ξ_<sup>(6)</sup><br>2<br>_≈_1_._0 _×_ 10<sup>_−_4</sup><br><br>|
|7||||_ξ_<sup>(7)</sup><br>1<br>˙_q_7<br>_ξ_<sup>(7)</sup><br>1<br>= 2_._244<br><br>|
|1||||_ξ_<sup>(1)</sup><br>1<br>˙_q_1<br>_ξ_<sup>(1)</sup><br>1<br>= 6_._721|
|Dy<br>2||||_ξ_<sup>(2)</sup><br>1<br>˙_q_2<br>_ξ_<sup>(2)</sup><br>1<br>= 5_._962<br><br>|
|N<br>3|_ϵ_ = _d_|˙_q_||_ξ_<sup>(3)</sup><br><br>˙_q_<br>_ξ_<sup>(3)</sup><br><br>=5235|
|r-SI<br><br>4<br>|_j_ _j_|_j_||1<br>3<br><br>1<br> _._<br>_ξ_<sup>(4)</sup><br>1<br>˙_q_4<br>_ξ_<sup>(4)</sup><br>1<br>= 4_._486<br><sup>(5)</sup><br>˙<br><sup>(5)</sup><br>|
|5||||_ξ_<br>1<br>_q_5<br>_ξ_<br>1<br>= 3_._741<br><br>|
|6||||_ξ_<sup>(6)</sup><br><br>˙_q_6<br>_ξ_<sup>(6)</sup><br><br>= 2_._991|
|7||||1<br><br><br>1<br><br>_ξ_<sup>(7)</sup><br>1<br>˙_q_7<br>_ξ_<sup>(7)</sup><br>1<br>= 2_._244|
|1||||_ξ_<sup>(1)</sup><br>1<br>¨_q_1<br>_ξ_<sup>(1)</sup><br>1<br>_≈_2_._92 _×_ 10<sup>_−_3</sup><br><br>|
|SR<br>2||||_ξ_<sup>(2)</sup><br><br>¨_q_2<br>_ξ_<sup>(2)</sup><br><br>_≈_2_._38 _×_ 10<sup>_−_3</sup>|
|NDy-<br>3|_ϵ_<sup>(2)</sup><br>_j_<br>= 0|||1<br><br><br>1<br><br>_ξ_<sup>(3)</sup><br>1<br>¨_q_3 + _ξ_<sup>(3)</sup><br>2<br>˙_q_1<br>_ξ_<sup>(3)</sup><br>1<br>_≈_2_._74 _×_ 10<sup>_−_3</sup>_, ξ_<sup>(3)</sup><br>2<br>_≈−_2_._74 _×_ 10<sup>_−_3</sup>|
|r-SI<br>4||||_ξ_<sup>(4)</sup><br>1<br>...<br>_q_4<br>_ξ_<sup>(4)</sup><br>1<br>_≈_9_._62 _×_ 10<sup>_−_5</sup><br><br>|
|5||||_ξ_<sup>(5)</sup><br>1<br>¨_q_5<br>_ξ_<sup>(5)</sup><br>1<br>_≈_2_._04 _×_ 10<sup>_−_3</sup><br><sup>(6)</sup><br><sup>(6)</sup><br>|
|6||||_ξ_<br>1<br>¨_q_6<br>_ξ_<br>1<br>_≈_1_._53 _×_ 10<sup>_−_3</sup>|
|7||||_ξ_<sup>(7)</sup><br>1<br>¨_q_7<br>_ξ_<sup>(7)</sup><br>1<br>_≈_1_._03 _×_ 10<sup>_−_3</sup>|
||TABL|E IV:|WAM t|raining set RMSE per joint.<br>consistently worse than SR and r-SR across|
|Joint|SR|SINDy|r-SR|r-SINDy r-SINDy-SR<br>NN<br>r-NN<br>hybrid r-NN slightly improves over the pure|
|1|0.410|**0.103**|0.477|**0.103**<br>**0.103**<br>0.121 0.132<br>joints (e.g., joint 1) but degrades performance|
|2|0.143|**0.027**<br>|0.182<br>|**0.027**<br>**0.027**<br>0.030 0.030<br><br><br>does not close the gap to the best SR-based m|
|3|0.437|0.057|0.570|**0.057**<br>**0.057**<br>0.0810.081<br><br>|
|4|0.423|**0.039**|0.422|<br>**0.039**<br>**0.039**<br>0.056 0.058<br>The SR approach produced the following eq|
|5|0.621|**0.177**|0.645|0.177<br>0.177<br>0.329 0.330<br>�_τ _<sup>_SR_</sup><br><sup>=¨</sup><sup>_q_1+˙</sup><sup>_q_1(</sup><sup>_ξ_(1)</sup><br><br>_−_˙_q_<sup>2</sup><br><sup>)</sup>|
|6|0.487|**0.076**|0.556|**0.076**<br>**0.076**<br>0.213 0.213<br> <br>_m,_1    <br>1<br><br>1<br><br><br>|
|7|0403|**0090**|0558|0090<br>0090<br>03220324<br>�_τ _<sup>_SR_</sup><br><sup>=¨</sup><sup>_q_2</sup><sup>_−_¨</sup><sup>_q_+˙</sup><sup>_q_2( ˙</sup><sup>_q_+</sup><sup>_ξ_(1)</sup><br><sup>)</sup><sup>_−_˙</sup><sup>_q_2</sup><br>|
||.<br>TA|**.**<br>BLE V|.<br>: WAM|.<br>.<br>. .<br> test set RMSE per joint.<br> <br>_m,_2   <sup>3</sup>   <sup>5</sup>  <br>2  <br>3<br>_−_((_ξ_<sup>(2)</sup><br>2<br>_−q_4)_q_2_ξ_<sup>(3)</sup><br>2<br>_−q_6+_τg,_3)|
|Joint|SR<br>|SINDy|r-SR|r-SINDy r-SINDy-SR<br>NN<br>r-NN<br><br>� <sup>_SR_</sup><br><sup>˙ ¨</sup> <sup>(1)</sup><br><sup>¨ </sup> <sup>(2)</sup><br>|
|1|**0410**|18566|0441|18566<br>18566<br>07330681<br>_τ _<br>_m,_3 <sup>= </sup><sup>_q_3</sup> <sup>+ (</sup><sup>_q_1</sup> <sup>+</sup><sup>_q_3</sup><sup>_q_4(</sup><sup>_ξ_</sup><br>3 <sup>_q_1 +</sup><sup>_ξ_</sup><br>3 <sup>))(</sup><sup>_q_2 </sup>|
|2|**.** <br>**0.183**|. <br>4.106|.<br>0.230|.<br>.<br>. .<br>4.106<br>4.106<br>0.470 0.472<br>� <sup>_SR_</sup><br><sup>= (</sup><sup>_−_(1)</sup><br><sup>)(2)</sup><br><sup>+˙ +</sup> <sup>(3)</sup>|
|3|**0.483**|7.782|0.540|7.463<br>7.463<br>0.876 0.773<br>_τ _<br>_m,_4  <sup>_q_4</sup> <sup>_ξ_</sup><br>4 <sup>_ξ_</sup><br>4 <sup>_q_4  </sup><sup>_q_4 </sup><sup>_ξ_</sup><br>4<br><br>|
|4|**0.453**|9.423|0.458|9.423<br>9.423<br>0.805 0.854<br>�_τ _<sup>_SR_</sup><br>_m_5 <sup>=</sup><sup>_ξ_(1)</sup><br>5<br>˙_q_5|
|5|0.476|60.189|**0.475**|59.389<br>59.388<br>0.942 1.243<br>_,_<br><br>�<sup>_SR_</sup><br> <sup>(1)</sup><br>˙¨ ˙<sup>(2)</sup><br>|
|6|0548|13280|**0547**|13160<br>13160<br>08220967<br>_τ _<br>_m_6 <sup>= (</sup><sup>_ξ_</sup><br>6<br>_−τg_6)(_q_6+ (_q_6+ _q_3)_ξ_<br>6 <sup>)</sup>|
|7|. <br>**0.437**|. <br> 27.754|**.**<br> 0.580|.<br>.<br>. .<br>27.905<br>27.905<br>1.246 1.282<br>_,_  <br><br>_,_   <br> <br>�<sup>_SR_</sup><br><sup>˙ ˙2</sup><br><sup>(1)</sup><br>˙<sup>2</sup><br><sup>(2)</sup><br>  <sup>(3)</sup><br>|


consistently worse than SR and r-SR across all joints. The hybrid r-NN slightly improves over the pure NN for some joints (e.g., joint 1) but degrades performance on others, and does not close the gap to the best SR-based models. 

The SR approach produced the following equations. 


The neural-network baselines occupy an intermediate regime. On the training set, NN and r-NN attain errors comparable to or slightly larger than the SINDy family, but substantially lower than SR and r-SR. On the test set, their RMSEs increase to roughly 0 _._ 47–1 _._ 28, which is still an order of magnitude smaller than the SINDy-based models but 


Fig. 3: An example of one of the trajectories provided by Sousa and Cortes˜ao [14], along with estimated velocities, accelerations, and jerk. Estimates of the various time derivatives were found using the method proposed by Chartrand [26]. 

The r-SR approach produced the following equations. 


= where _ξ_ 1<sup>(1)</sup> = 3 _._ 2723246, _ξ_ 2<sup>(1)</sup> = 0 _._ 016012268, _ξ_ 2<sup>(2)</sup> = _−_ 1 _._ 023108, _ξ_ 2<sup>(3)</sup> = _−_ 8 _._ 626232, _ξ_ 2<sup>(4)</sup> = 0 _._ 50142884, _ξ_ 2<sup>(5)</sup> = = = 3 _._ 391348, _ξ_ 3<sup>(1)</sup> 2 _._ 58501, _ξ_ 4<sup>(1)</sup> 3 _._ 1465542, _ξ_ 4<sup>(2)</sup> = 1 _._ 9603553, _ξ_ 4<sup>(3)</sup> = 0 _._ 58640337, _ξ_ 5<sup>(1)</sup> = 0 _._ 14822637, _ξ_ 6<sup>(1)</sup> 0 _._ 24277882, _ξ_ 7<sup>(1)</sup> = 0 _._ 07425557. 

The methods using SINDy produced models that are too long to write in the page. 

Beyond the quantitative comparison in Tables IV and V, the closed-form SR and r-SR expressions for the WAM arm provide additional qualitative insight into the structure of the learned dynamics. For several joints, the models recover familiar physical motifs: joints 1, 5, 6, and 7 are dominated by velocity-dependent terms that resemble viscous or nonlinear friction laws (linear in _q_ ˙ _j_ for joints 5–7 in the r-SR residuals, and cubic/quintic in _q_ ˙1 and _q_ ˙7 in the full SR model), while joint 4 features a clear spring-like dependence on _q_ 4 of the form ( _q_ 4 _−_ offset) _q_ 4 combined with a viscous term in _q_ ˙4 and a constant bias torque. These patterns are consistent with the intuition that the nominal rigid-body model accounts for the 

bulk of the inertial and gravitational effects, whereas the residuals capture joint-local friction, compliance, and offset torques that arise from the WAM’s cable transmissions and hardwarespecific characteristics. The presence of explicit _τg,j_ terms in several SR and r-SR equations—for instance, _τg,_ 3 appearing in the models for joints 2 and 3, or _τg,_ 5 and _τg,_ 6 modulating the residuals of joints 5 and 6—further indicates that the symbolic learner makes systematic use of the available gravity regressor, effectively re-weighting or partially “undoing” it where the analytical model and the real robot diverge. 

At the same time, the WAM expressions also expose more complex structures that go beyond the canonical RBD-plusviscous-friction picture and would be difficult to anticipate a priori, yet remain compact and interpretable. In particular, the SR model for joints 2 and 3 contains configuration- and coupling-dependent factors such as ( _ξ_ 2<sup>(2)</sup> _− q_ 4) _q_ 2, and mixed dependencies on _q_ 4, _q_ 6, and _τg,_ 3, while the r-SR residual for joint 2 exhibits a product ( ˙ _q_ 2 + ( _ξ_ 2<sup>(1)</sup> _− q_ 2)( _ξ_ 2<sup>(2)</sup><sup>_q_4</sup><sup>_−_</sup> _ξ_ 2<sup>(3))</sup><sup>_−ξ_</sup> 2<sup>(4))</sup><sup>_ξ_</sup> 2<sup>(5).Thesetermssuggestnontrivialcross-joint</sup> couplings and configuration-dependent biases that are not explicitly encoded in the nominal RBD model, and may be absorbing effects of cable routing, structural compliance, or sensor/actuator nonlinearities. Similarly, the SR expression for _−_ joint 6 includes a gravity-modulated friction term ( _ξ_ 6<sup>(1)</sup> _τg,_ 6)( ˙ _q_ 6 +(¨ _q_ 6 + _q_ ˙3) _ξ_ 6<sup>(2)), indicating that the effective damping</sup> on joint 6 depends on both posture (through _τg,_ 6) and motion of another joint (via _q_ ˙3), which goes beyond standard jointwise viscous friction models. While some of these couplings may reflect identification artifacts or dataset-specific correlations rather than entirely new physical effects, the fact that they arise as low-complexity terms and still generalize better than both 

SINDy and neural networks on held-out trajectories makes them valuable hypotheses for further mechanical analysis and model refinement. 

Finally, we note that all SR and r-SR models on the WAM dataset were learned with a deliberately simple PySR setup: the operator set was restricted to the binary operators _{_ + _, −, ×}_ , and all remaining options (evolutionary strategy, complexity–accuracy trade-off, population sizes, etc.) were left at their default values, with no task-specific hyperparameter tuning. In other words, the discovered spring-like terms, crossjoint couplings, and gravity-modulated friction laws emerge under a generic, off-the-shelf configuration. It is plausible that a more targeted search—for example, adjusting the complexity penalty, enriching the operator set with piecewise or nonsmooth functions, or biasing the search toward cross-joint features—could either simplify some of the more intricate couplings found here or uncover additional, more physically structured components (such as clearer Coulomb-like friction terms or smoother approximations of stick–slip effects) while retaining or further improving generalization on held-out trajectories. 

_3) Discussion:_ Overall, the WAM results highlight a clear gap between in-sample fit and out-of-sample reliability. SINDy and its hybrid variants achieve the lowest training errors but fail to generalize, with test RMSEs increasing by several orders of magnitude and yielding very long expressions that appear to track trajectory-specific artefacts rather than underlying mechanics. In contrast, SR and r-SR trade some training accuracy for substantially better generalization, attaining the lowest test errors across most joints. 

As discussed above, the closed-form SR and r-SR models remain compact and physically interpretable, capturing friction-like, spring-like, and gravity-modulated effects as well as nontrivial cross-joint couplings. Importantly, all of these SR and r-SR models were obtained with a simple, off-the-shelf PySR configuration restricted to the operators _{_ + _, −, ×}_ and default evolutionary settings, with no task-specific hyperparameter tuning. This suggests that even a modest symbolicregression setup can already uncover meaningful structure in realistic robot data. The limited benefit of hybridizing neural networks with _τrbd_ and the poor robustness of the SINDy variants together underline that, in this more realistic setting where the analytical model and function libraries are only approximate, the choice of model class and regularization is at least as important as raw approximation power. 

## VI. CONCLUSION 

We proposed interpretable, data-driven residual models of robot dynamics that augment an analytical rigid-body dynamics (RBD) model with a learned error term _ϵ_ . Using symbolic regression (SR) and SINDy-style sparse regression on joint-space features, we obtained compact expressions that, in simulation on a Franka arm with known dynamics, recover inertial, Coriolis, gravity, and viscous terms with relative errors of order 10<sup>_−_3</sup> . In this setting, SR/SINDy and their 

RBD hybrids match the true dynamics with strong train– test generalization and outperform neural-network baselines while remaining fully interpretable. On real data from a 7- DoF WAM arm, SR models generalize best and consistently outperform both SINDy and neural networks on held-out data, revealing physically meaningful structure such as viscous and nonlinear friction, spring-like terms, gravity reweightings, and low-dimensional cross-joint couplings. 

## _A. Limitations_ 

Our method assumes an accurate RBD model and sufficiently clean joint-level measurements. Models are trained offline on pre-collected data and evaluated via one-step torque prediction, so their closed-loop impact on performance and safety is unknown. We restrict the feature libraries and function classes to hand-designed polynomials, a basic operator set _{_ + _, −, ×}_ , and per-joint models, which may miss richer friction effects and higher-order couplings. Derivative-based features (velocities, accelerations, jerk) rely on numerical differentiation; although we use smoothed, total-variationregularized finite differences [26], derivative quality and some learned terms may still be affected by noise, sampling rates, and sensor biases. 

## _B. Future Work_ 

Future work will embed interpretable residual models into control and learning pipelines, e.g., as components in impedance or model-predictive controllers, as structured priors in model-based or hybrid reinforcement learning, and as virtual force/torque sensors for contact-rich tasks. We also aim to relax reliance on a fixed RBD model by jointly identifying rigidbody parameters and residuals, and by enriching SR/SINDy libraries with more physics-informed, possibly non-smooth operators while preserving sparsity. Finally, we plan to study transfer across robots and data regimes, leveraging shared interpretable structure to generalize dynamics models and support scalable, force-aware extensions of vision–language– action frameworks. 

## REFERENCES 

- [1] Maged Iskandar, Christian Ott, Alin Albu-Sch¨affer, Bruno Siciliano, and Alexander Dietrich. Hybrid forceimpedance control for fast end-effector motions. _IEEE Robotics and Automation Letters_ , 8(7):3931–3938, 2023. doi: 10.1109/LRA.2023.3270036. 

- [2] Sichao Liu, Lihui Wang, and Xi Vincent Wang. Sensorless force estimation for industrial robots using disturbance observer and neural learning of friction approximation. _Robotics and Computer-Integrated Manufacturing_ , 71:102168, 2021. 

- [3] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag R. Sanketi, Grecia Salazar, Michael S. Ryoo, Krista Reymann, Kanishka 


Fig. 4: Evaluations of our trained model using SR on the real world data collected from the 7-DoF WAM robot arm [14]. 

Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Lisa Lee, Tsang-Wei Edward Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil J. Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Keerthana Gopalakrishnan, Chuyuan Fu, Pete Florence, Chelsea Finn, Kumar Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Marcin Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, Anthony Brohan, Montserrat Gonzalez Arenas, and Kehang Han. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of The 7th Conference on Robot Learning_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 2023. URL https://proceedings.mlr.press/v229/ zitkovich23a.html. 

- [4] Open X.-Embodiment Collaboration, Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alexander Herzog, Alex Irpan, Alexander Khazatsky, Anant Raj, Anikait Singh, Anthony Brohan, Antonin Raffin, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Sch¨olkopf, Brian Ichter, Cewu Lu, Charles Xu, 

Chelsea Finn, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Chuer Pan, Chuyuan Fu, Coline Devin, Danny Driess, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Federico Ceola, Fei Xia, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Giulio Schiavi, Gregory Kahn, Hao Su, Haoshu Fang, Haochen Shi, Heni Ben Amor, Henrik I. Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Igor Mordatch, Ilija Radosavovic, et al. Open x-embodiment: Robotic learning datasets and RT-X models. _CoRR_ , abs/2310.08864, 2023. doi: 10.48550/arXiv.2310.08864. URL https://arxiv.org/abs/2310.08864. 

- [5] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P. Foster, Grace Lam, Pannag R. Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source visionlanguage-action model. _CoRR_ , abs/2406.09246, 2024. doi: 10.48550/arXiv.2406.09246. URL https://arxiv.org/ abs/2406.09246. 

- [6] William Xie and Nikolaus Correll. Towards forceful robotic foundation models: a literature survey. _CoRR_ , abs/2504.11827, 2025. doi: 10.48550/arXiv.2504.11827. URL https://arxiv.org/abs/2504.11827. 

- [7] Jialei Huang, Shuo Wang, Fanqi Lin, Yihang Hu, Chuan Wen, and Yang Gao. Tactile-VLA: Unlocking visionlanguage-action model’s physical knowledge for tactile generalization. _CoRR_ , abs/2507.09160, 2025. doi: 10.48550/arXiv.2507.09160. URL https://arxiv.org/abs/ 2507.09160. 

- [8] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, Cewu Lu, and Wenqiang Zhang. Forcevla: Enhancing VLA models with a force-aware MoE for contact-rich manipulation. _arXiv preprint arXiv:2505.22159_ , 2025. doi: 10.48550/arXiv.2505. 22159. URL https://arxiv.org/abs/2505.22159. NeurIPS 2025. 

- [9] P. Fankhauser, M. Hutter, C. Gehring, M. Bloesch, M. A. Hoepflinger, and R. Siegwart. Reinforcement learning of single legged locomotion. In _2013 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 188–193. IEEE, 2013. doi: 10.1109/IROS. 2013.6696363. 

- [10] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal locomotion over challenging terrain. _Science Robotics_ , 5 (47):eabc5986, 2020. doi: 10.1126/scirobotics.abc5986. 

- [11] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Proceedings of the 5th Conference on Robot Learning_ , volume 164 of _Proceedings of Machine Learning Research_ , pages 91– 100. PMLR, 2022. 

- [12] Sehoon Ha, Joonho Lee, Michiel van de Panne, Zhaoming Xie, Wenhao Yu, and Majid Khadiv. Learning-based legged locomotion: State of the art and future perspectives. _International Journal of Robotics Research_ , 44(8): 1396–1427, 2025. doi: 10.1177/02783649241312698. 

- [13] Christopher G Atkeson, Chae H An, and John M Hollerbach. Estimation of inertial parameters of manipulator loads and links. _The International Journal of Robotics Research_ , 5(3):101–119, 1986. 

- [14] Crist´ovao D Sousa and Rui Cortesao. Physical feasibility of robot base inertial parameter identification: A linear matrix inequality approach. _The International Journal of Robotics Research_ , 33(6):931–944, 2014. 

- [15] J. Swevers, C. Ganseman, D.B. Tukel, J. de Schutter, and H. Van Brussel. Optimal robot excitation and identification. _IEEE Transactions on Robotics and Automation_ , 13 (5):730–740, 1997. doi: 10.1109/70.631234. 

- [16] Huanyu Tian, Martin Huber, Christopher E Mower, Zhe Han, Changsheng Li, Xingguang Duan, and Christos Bergeles. Excitation trajectory optimization for dynamic parameter identification using virtual constraints in hands-on robotic system. In _2024 IEEE International_ 

_Conference on Robotics and Automation (ICRA)_ , pages 11605–11611. IEEE, 2024. 

- [17] Shahram Khorshidi, Murad Dawood, Benno Nederkorn, Maren Bennewitz, and Majid Khadiv. Physicallyconsistent parameter identification of robots in contact. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 677–683, 2025. doi: 10.1109/ICRA55743.2025.11128710. 

- [18] Andrea Carron, Elena Arcari, Martin Wermelinger, Lukas Hewing, Marco Hutter, and Melanie N. Zeilinger. Datadriven model predictive control for trajectory tracking with a robotic arm. _IEEE Robotics and Automation Letters_ , 4(4):3758–3765, 2019. doi: 10.1109/LRA.2019. 2929987. 

- [19] Philipp Scholl, Alexander Dietrich, Sebastian Wolf, Jinoh Lee, Alin-Albu Sch¨affer, Gitta Kutyniok, and Maged Iskandar. Interpretable robotic friction learning via symbolic regression, 2025. URL https://arxiv.org/abs/2505. 13186. 

- [20] Miles Cranmer. Interpretable machine learning for science with pysr and symbolicregression. jl. _arXiv preprint arXiv:2305.01582_ , 2023. 

- [21] Manuel Morales-Alvarado, Daniel Conde, Josh Bendavid, Veronica Sanz, and Maria Ubiali. Symbolic regression for precision lhc physics, 2024. URL https: //arxiv.org/abs/2412.07839. 

- [22] Steven L. Brunton, Joshua L. Proctor, and J. Nathan Kutz. Discovering governing equations from data by sparse identification of nonlinear dynamical systems. _Proceedings of the National Academy of Sciences_ , 113(15): 3932–3937, 2016. doi: 10.1073/pnas.1517384113. URL https://www.pnas.org/doi/abs/10.1073/pnas.1517384113. 

- [23] Alan A. Kaptanoglu, Brian M. de Silva, Urban Fasel, Kadierdan Kaheman, Andy J. Goldschmidt, Jared Callaham, Charles B. Delahunt, Zachary G. Nicolaou, Kathleen Champion, Jean-Christophe Loiseau, J. Nathan Kutz, and Steven L. Brunton. Pysindy: A comprehensive python package for robust sparse system identification. _Journal of Open Source Software_ , 7(69):3994, 2022. doi: 10.21105/joss.03994. URL https://doi.org/10.21105/joss. 03994. 

- [24] Erwin Coumans and Yunfei Bai. Pybullet, a python module for physics simulation for games, robotics and machine learning, 2016. 

- [25] Justin Carpentier, Guilhem Saurel, Gabriele Buondonno, Joseph Mirabel, Florent Lamiraux, Olivier Stasse, and Nicolas Mansard. The pinocchio c++ library : A fast and flexible implementation of rigid body dynamics algorithms and their analytical derivatives. In _2019 IEEE/SICE International Symposium on System Integration (SII)_ , pages 614–619, 2019. doi: 10.1109/SII.2019. 8700380. 

- [26] Rick Chartrand. Numerical differentiation of noisy, nonsmooth data. _International Scholarly Research Notices_ , 2011(1):164564, 2011. 

