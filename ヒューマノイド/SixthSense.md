---
title: "SixthSense: Task-Agnostic Proprioception-Only Whole-Body Wrench Estimation for Humanoids"
date: "2026-05-02"
authors: "Xingzhou Chen; Xiayan Xu; Yan Ning; Jiyu Yu; Yizheng Zhang; Siyi Qian"
url: https://arxiv.org/abs/2605.01427
pdf: https://arxiv.org/pdf/2605.01427
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.01427)** / [論文ページ](https://arxiv.org/abs/2605.01427)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# SixthSense: Task-Agnostic Proprioception-Only Whole-Body Wrench Estimation for Humanoids 

Xingzhou Chen<sup>1</sup><sup>_,∗_</sup> , Xiayan Xu<sup>1</sup><sup>_,∗_</sup> , Yan Ning<sup>1</sup> , Ling Shi<sup>1</sup> , Jiyu Yu<sup>2</sup> , Yizheng Zhang<sup>3</sup> , Siyi Qian<sup>3</sup> , Lingzhu Xiang<sup>3</sup> , Jiahao Chen<sup>3</sup> , Yuquan Wang<sup>3</sup><sup>_,†_</sup> , and Haodong Zhang<sup>3</sup><sup>_,†_</sup> 

**_Abstract_ —Humanoid robots are entering our physical world at scale, yet as oversized toys—good at singing and dancing, but short on force-interaction capabilities for practical tasks. Bridging this gap necessitates prioritizing reliable contact perception as a fundamental requirement. Estimating external wrenches in humanoids is complicated by floating-base dynamics and indeterminate contact locations. Existing analytical frameworks require idealistic assumptions and hard-to-obtain measurements, which are often unavailable in practice. To bridge this gap, we propose SixthSense, a task-agnostic approach that infers whole-body contact timing, location, and wrenches from proprioception and IMU data alone. To capture the multi-modal dynamics between unstructured contact inputs and the uncertain motion outputs, we employ conditional flow matching to tokenize proprioceptive histories and estimate a spatiotemporally sparse contact-event flow. SixthSense serves as a plug-and-play perception module for applications including collision detection, physical human– robot interaction, and force-feedback teleoperation. Experiments across standing, walking, and whole-body motion-tracking policies showcased unprecedented performance in diverse behaviors.** 

**_Index Terms_ —humanoid robots, whole-body wrench estimation, proprioception, conditional generative model** 

## I. INTRODUCTION 

Humanoid robots are increasingly capable of executing complex motions in the wild, from agile locomotion to expressive whole-body tracking [16, 22, 29, 24, 37]. In these examples, robots treat physical contact—collisions, pushes and pulls, or carried loads—as disturbances to be rejected, rather than phenomena to be perceived and understood. As a result, robots remain unaware of when, where, and how forces are applied to their bodies. This lack of force-level interaction understanding limits their ability to engage in realistic physical contact [31], fueling skepticism about the practical utility of humanoids beyond polished demonstrations. 

This limitation stems from the fact that current reinforcement learning-based controllers [16, 20, 39] do not explicitly estimate contacts. Rather, contact information is entangled with specific objectives, limiting generality across tasks and interaction regimes [39]. A few recent learning-based approaches begin to explicitly estimate contact forces, but primarily focus on end-effector control with known contact interfaces [41]. 

> _∗_ Equal contribution. 

> _†_ Corresponding authors. 

> 1Xingzhou Chen, Xiayan Xu, Yan Ning, and Ling Shi are with The Hong Kong University of Science and Technology, Hong Kong SAR, China. 

> 2Jiyu Yu is with Zhejiang University, Hangzhou, China. 

> 3Yizheng Zhang, Siyi Qian, Lingzhu Xiang, Jiahao Chen, Yuquan Wang, and Haodong Zhang are with Tencent Robotics X, Shenzhen, China. 


Fig. 1: **SixthSense** : Inferring whole-body contact wrench fields via proprioception. This task-agnostic, plug-and-play module provides a robust perception foundation for diverse downstream control and decision-making applications. 

While external wrench estimation for fixed-base manipulators is largely a solved problem, extending these methods to whole-body humanoid interaction is fundamentally different. The presence of a floating base and numerous potential contact locations renders the problem physically under-determined and nearly unobservable [8]. Consequently, analytical solutions often adopt oversimplified dynamics or highly restricted contact assumptions [6, 11, 10, 30], making them impractical for general purposes. To the best of our knowledge, achieving robust analytical estimation of whole-body external wrenches from proprioception remains an open challenge. 

Alternative to previous work, we formulate whole-body contact perception as an inference problem over a spatiotemporal distribution of external wrenches. Inspired by human sensorimotor experience, we refer to this form of bodily awareness of interaction phenomena as SixthSense, beyond classical visual or tactile sensing. 

Building on this perspective and without requiring force, vision, or tactile sensors, we propose SixthSense, a taskagnostic approach that enables humanoid robots to perceive whole-body external wrenches, including (i) whether non-foot 

contact occurs, (ii) where it happens, (iii) when it happens, and (iv) what impulse is applied. 

SixthSense adopts a generative inference framework that models external contact wrenches as a stochastic spatiotemporal process conditioned on closed-loop proprioceptive signals [19, 32]. It combines a unified whole-body contact representation for joint contact-likelihood and wrench estimation, temporally aligned proprioceptive inputs from contact-resilient controllers, and probabilistic contact inference via conditional flow matching [25] to predict sparse contact impulses. 

We evaluate SixthSense across different tasks, demonstrating consistent and accurate wrench inference under diverse behaviors. By providing explicit, reusable whole-body wrench estimates without additional sensors, SixthSense enables forceaware reasoning beyond contactless shows, supporting forceful and diverse interactions. 

To summarize, the main contributions are twofold: 

- Formulating contact perception as a flow matching-based generative problem, modeling external wrenches as a sparse spatiotemporal field and enabling distributional inference under ambiguity. 

- A task-agnostic plug-and-play perception module for whole-body external contact that can infer contact timing, location, and wrenches directly from proprioception and IMU signals. 

## II. RELATED WORK 

## _A. Implicit Contact-Aware Humanoid Motion Control_ 

Conventionally, accurate and timely contact information is essential for balancing humanoid robots for locomotion or multi-contact manipulation [4, 14, 9], enabling locomotion in uneven terrain [27, 9] or contact-rich industrial workshop [18]. 

The emerging deep reinforcement learning-based controllers embed the floating-base state estimation in a learned network, significantly improving the locomotion policy’s robustness [17]. Merely employing IMU and joint motor feedback, locomotion policies achieve stable foothold behaviors and disturbance recovery without explicit contact-force handling. 

In humanoid motion tracking, imitation-based approaches induce physically consistent contacts and recovery behaviors through dense tracking objectives, while more recent systems scale interaction diversity via diffusion-based motion synthesis or large-scale whole-body teleoperation [29, 24, 37, 13]. In parallel, disturbance-aware tracking methods treat external interactions as latent disturbances to be compensated online, using history-conditioned representations for adaptation [20, 39]. Related ideas also appear in end-effector manipulation, where joint torque feedback is incorporated into Vision-LanguageAction models to improve performance in contact-rich tasks without dedicated force sensing [40]. 

Despite promising task performance, contact information in these approaches remains tightly coupled to specific tasks and controllers, limiting reusability and generalization when control objectives or interaction regimes change. 

## _B. Sensor-Based Contact-Rich Control_ 

Direct force and tactile sensing provides explicit access to contact information and has been extensively studied in dexterous manipulation. High-resolution tactile and force sensors enable accurate estimation of contact location, geometry, and force, supporting grasp stability and fine interaction control in robotic hands [36, 35, 21]. However, scaling dense force sensing to whole-body humanoids remains challenging due to hardware cost and calibration complexity. Similar in spirit to visuotactile perception in manipulation [2, 33, 23], some humanoid control pipelines exploit visual cues to anticipate contact geometry in task space [22, 38], but such cues do not capture body-level force interaction during execution. 

## _C. Sensorless Contact Force Estimation_ 

When force-torque or tactile sensors are absent, modelbased observers can infer external wrenches from dynamics residuals for fixed-base manipulators [5, 6, 10, 8, 11, 26]. A representative family is the generalized momentum observer (GMO), which avoids direct acceleration measurements and detects external generalized forces through momentum residuals [11]. Probabilistic extensions like the contact particle filter (CPF) further represent multi-contact as probabilistic hypotheses and infer their likelihood with a particle filter [26]. 

However, these model-based methods rest on idealized assumptions that limit humanoid deployment. GMO requires accurate rigid-body models and well-conditioned Jacobians, yet the floating base’s unactuated degrees of freedom corrupt momentum residuals and multiple contact configurations produce ambiguous proprioceptive signatures [11]. CPF elegantly frames multi-contact as probabilistic inference, but still depends on precise foot-force models and accurate whole-body Jacobians. 

Adjacent model-based work—e.g., multi-momentum footcontact observers [28], probabilistic foot-contact estimation [15, 3], and Kalman-filter-based legged state estimation [1, 12]—improves locomotion or base state estimation but outputs foot contact modes or odometry rather than wholebody external wrenches. 

Meanwhile, learning-based sensorless approaches remain scarce; among them, [41] estimates contact forces from historical states but is limited to pre-defined end-effector contact. As a result, task-agnostic whole-body contact perception from proprioception—explicitly estimating contact timing, location, and wrenches—remains largely underexplored. 

## III. PROBLEM STATEMENT 

We introduce the mathematical preliminaries, explain issues associated with the well-established analytical approaches, and motivate the problem of interest. 

## _A. Dynamics of Humanoid Robots_ 

A floating-base robot has generalized coordinates **_q_** = [ **_q_** b<sup>_⊤_</sup> **_q_** j<sup>_⊤_]</sup><sup>_⊤_,where</sup><sup>**_q_**b</sup><sup>_∈SE_(3)denotesthebaseposeand</sup> 

**_q_** j _∈_ R<sup>_n_</sup> collects the _n_ joint angles. Neglecting joint friction, the rigid-body dynamics writes 

- When multi-point contacts occur across the entire body, how should such spatiotemporally sparse and uncertain external wrenches be represented? 


- When external contacts are only indirectly observed through proprioceptive signals, and different contacts can produce nearly identical proprioceptive responses, how should external wrenches be inferred under this fundamentally non-identifiable mapping? 

where _H_ ( **_q_** ) is the inertia matrix, _C_ ( **_q_** _,_ **_q_ ˙** ) **˙** **_q_** and _g_ ( **_q_** ) collect Coriolis/centrifugal and gravity terms, respectively. The selection matrix _S_ = [ **0** _n×_ 6 **I** _n_ ] maps joint torques **_τ_** m to generalized forces. Each contact wrench **_f_** _e ∈_ R<sup>6</sup> contributes linearly through the corresponding contact Jacobian _Je_ ( **_q_** ). 

- When dominant dynamics change across tasks and motion phases, including variations in foot support and contact regimes, how can whole-body external wrench estimation remain task-agnostic and generalizable? 

Adopting the base–joint block form [7], we partition the base and joint accelerations **_q_ ¨** = [ **_a_**<sup>_⊤_</sup> b **_q_ ¨** j<sup>_⊤_]</sup><sup>_⊤_,thecontact</sup> Jacobian: _Je_ = [ _Je,_ b _Je,_ j ], and re-write (1) as: 

In this work, we answer these questions by casting whole-body wrench perception as a distributional conditional inference problem and learning a generative model over spatiotemporal wrench fields. 


## IV. METHOD 

We formulate the whole-body contact detection as a probabilistic problem in Sec. IV-A, detail the learning objectives in Sec. IV-B, and explain contact inference via conditional flow matching in Sec. IV-C. 

where _H_ bb _∈_ R<sup>6</sup><sup>_×_6</sup> , _H_ bj _∈_ R<sup>6</sup><sup>_×n_</sup> , and _H_ jj _∈_ R<sup>_n×n_</sup> are the base–joint blocks of _H_ ( **_q_** ). The vectors **_h_** b and **_h_** j denote the corresponding blocks of _C_ ( **_q_** _,_ **_q_ ˙** ) **˙** **_q_** + _g_ ( **_q_** ). 

## _B. Problem of Interest_ 

## _A. Contact Representation and Learning Objective_ 

Let **o** _t_ denote the proprioceptive observation at time _t_ , and _Ot_ : _t_ + _T −_ 1 = _{_ **o** _t}_<sup>_t_</sup> _t_<sup>+</sup><sup>_T −_1</sup> denote an observation window of length _T_ . In (2), the left-hand side is fully determined by _Ot_ : _t_ + _T −_ 1 and a known rigid-body model, whereas the righthand side depends on a latent contact configuration through the unknown external wrenches. 

Existing analytical contact estimation [11] typically applies a sequential three-step pipeline: (1) detecting a binary contact state, (2) identifying the contact location, and (3) computing the corresponding external wrench. While this modularity simplifies the estimation process, its reliance on heuristicbased logic often fails to account for real-world physical complexities and lacks robustness in multi-contact scenarios. 

Analytical approaches typically localize contacts to construct _Je_ ( **_q_** ) and then solve for **_f_** _e_ via inverse dynamics or residual-based formulations. When contact information is uncertain, the mapping from contact wrenches to joint- and base-level dynamics residuals becomes non-injective, admitting multiple solutions in the nullspace and rendering wrench recovery structurally non-identifiable under contact uncertainty [8]. Moreover, even when inertia inversion is avoided, modeling errors and sensor noise can be significantly amplified through ill-conditioned contact _Je_ ( **_q_** ). Existing analytical formulations have been demonstrated primarily in simulation, highlighting the fragility of idealized assumptions for realworld whole-body contact interpretation. 

Alternatively, we represent the entire robot surface as a single interaction entity, allowing us to simultaneously estimate contact likelihood and external wrenches at any potential contact region. We divide the robot surface into _N_ sub-regions. At each time step _t_ , we predict (i) a probabilistic contact mask **M** _t ∈_ [0 _,_ 1]<sup>_N_</sup> and (ii) a per-subregion 6-D wrench field **F** _t ∈_ R<sup>_N×_6</sup> . Under this representation, we leverage the contact mask to detect contacts and corroborate the wrench in the following way: 


Motivated by these limitations, rather than selecting an explicit contact set, we lift contacts to _N_ potential sites distributed over the body surface and approximate the generalized contact wrench as 

where _⊙_ denotes the Hadamard product with row-wise broadcasting, and _δ_ is the threshold. **F**<sup>(</sup> _t_<sup>_i_)</sup> and **M**<sup>(</sup> _t_<sup>_i_)</sup> denote the wrench (with the application point at the center of mass of the sub-region) and contact probability associated with region _i_ , respectively. 


where **J**<sup>_⊤_</sup> ext<sup>=[</sup><sup>_J_(1)</sup><sup>_⊤, . . . , J, . . . , J_(</sup><sup>_N_)</sup><sup>_⊤_]</sup><sup>_∈_R(6+(6+</sup><sup>_n_)</sup><sup>_×_6</sup><sup>_N_and</sup><sup>**f**ext</sup><sup>_∈_</sup> R<sup>6</sup><sup>_N_</sup> stacks the corresponding candidate wrenches. 


Removing explicit contact-set selection reframes wholebody wrench perception as a set of open questions rather than a closed-form estimation problem: 

_where_ **c**<sup>(</sup><sup>_i_)</sup> _denotes the center of mass of the sub-region._ 

**Example 1.** _The discretization of the robot’s surface is adaptable to specific application requirements; specifically, the number of candidate contact regions, N in_ (4) _, is configured per robot and use case. Employing the Unitree G1 as an example (Fig. 2), its official URDF defines 30 distinct links. We can intuitively choose N_ = 30 _, which maps the robot surface for a per-link wrench field_ **F** _∈_ R<sup>30</sup><sup>_×_6</sup> _and a contact mask_ **M** _∈_ [0 _,_ 1]<sup>30</sup> _, as illustrated in Fig. 3._ 


Fig. 2: Mapping whole-body surface contact force to wrench at sub-region’s center of mass 

## _B. Proprioceptive Signal Construction and Alignment_ 

In practice, contacts are inherently sparse in both time and space, leading to highly imbalanced data distributions. To learn whole-body contact under severe spatio-temporal sparsity, we minimize a composite loss that couples contact presence prediction with wrench estimation: 


Here, _L_ mask is a binary cross-entropy loss for the predicted contact mask. _L_ wrench is a mask-aware regression loss for wrench estimation, prioritizing errors on contact regions while lightly regularizing non-contact regions. In addition, we use two lightweight priors: _L_ consistency suppresses spurious forces when no contact is predicted, and _L_ sparsity encourages sparsity in the predicted contact. 

The proprioceptive observation at time _t_ includes: 


where joint positions **q** _t_ , velocities **q** ˙ _t_ , and torques **_τ_** _t_ are read from the actuators, base orientation **R** base _,t_ and angular velocity **_ω_** base _,t_ are obtained from the IMU. To capture temporal dynamics, we tokenize each proprioceptive observation **o** _t_ and stack _H_ consecutive tokens to form an observation window **c** = _{_ **o** _t, . . . ,_ **o** _t_ + _H−_ 1 _}_ . During training, we pair **c** with a corresponding contact chunk **x** = _{_ **F** _t, . . . ,_ **F** _t_ + _H−_ 1 _}_ , where ground truth labels are acquired via simulation or high-fidelity force-torque sensors. This sequence-to-sequence 

formulation leverages temporal correlations within the proprioceptive stream, yielding more consistent predictions and improved data efficiency for sparse or ambiguous contact events. 

We argue that the observation window **c** not only encodes rich information about the robot’s motion, but also implicitly carries sufficient information about external contacts. This intuition is further supported by evidence from proprioceptiononly controllers: 

- **Proprioception-only control.** Beyond high-level commands, many RL-based controllers can operate reliably using proprioceptive observations alone. 

- **Implicit foot-contact sensing.** Stable walking across diverse terrains suggests that the controller implicitly infers and regulates foot–ground contacts. 

- **Implicit body-contact awareness.** When the robot is pushed during motion, it can recover balance smoothly, indicating that the controller implicitly detects and reacts to external disturbances applied to body parts. 

- Motivated by this empirical evidence, we posit the following 

- working hypotheses: 

**_Hypothesis 1:_ If a humanoid remains stable under external contacts, the contact information is (at least) weakly observable to the controller.** _It can be interpreted through the lens of system theory. External contacts induce distinct subsequent observations, which a stable controller must exploit in closed loop to compensate for the disturbance._ 

**_Hypothesis 2:_ Greater robustness to external contacts makes contact cues more readily observable to the controller.** _It can be understood through information theory using entropy. A more robust controller tends to yield a more consistent proprioceptive response to external disturbances. Therefore, it reduces the uncertainty of the latent contact variable given the observations._ 

Building on the above hypotheses, we obtain aligned proprioceptive signals by first training a contact-resilient controller (Fig. 3). To improve the controller’s robustness to external contacts, we adopt domain randomization and curriculum learning. By training a policy to stabilize smoothly under contacts, we obtain an aligned proprioceptive stream from the controller’s input, in which contacts leave strong and informative temporal signatures that are easy to decode. 

## _C. CFM-Based Contact Inference_ 

Conditional flow matching (CFM) [34] learns a timedependent velocity field that transports a noisy sample toward a target conditional data distribution. We employ CFM to recover the multi-modal nature of contact events. 

We initialize a contact chunk **x** _∈_ R<sup>_H×N×_6</sup> with Gaussian noise **x** 0 _∼N_ ( **0** _,_ **I** ), and discretize the entire training procedure as _t ∈_ [0 _,_ 1]. At a training step _k_ , the contact chunk evolves as: 


where **x** = **x** ˆ _K_ is a sampled contact estimate conditioned on proprioceptive observation **c** , and **v** _θ_ ( _·_ ) is a time-dependent 


Fig. 3: Overview: Given a contact-resilient control policy, we use its rollouts to train a conditional flow-matching model that outputs a whole-body external contact wrench field over the discretized robot surface. 

velocity field parameterized by _θ_ to be learned from the data. 

**Remark 2.** _The discrete evolution_ (8) _can be interpreted as an iterative solver for the Euler–Lagrange equation, which can infer_ **x** ˆ _from the proprioceptive observation window_ **c** _. In this view,_ ∆ _t corresponds to a step size and_ **v** _θ_ ( **x** _k, tk_ ; **c** ) _is a learned gradient surrogate that updates_ **x** ˆ _k to satisfy the physical constraint implied by_ **c** _. Intuitively,_ **v** _θ measures the inconsistency of the current_ ( **x** _k,_ **c** ) _pair and provides a correction direction to reduce it. At convergence, the update magnitude diminishes and_ **v** _θ_ ( **x** _k, tk_ ; **c** ) _→_ **0** _, indicating that_ **x** ˆ _k becomes locally compatible with the condition._ 

We adopt a shared-backbone, dual-head design for joint 

mask and wrench prediction. Specifically, a single CFM backbone encodes the conditioning context and captures shared contact semantics, while two lightweight attention heads separately decode per-link contact probabilities (mask) and perlink wrenches. This structure maximizes feature reuse with minimal overhead, improves generalization, and promotes coherent mask–wrench outputs by learning both tasks from a common latent representation. 

## V. EXPERIMENT 

We validate SixthSense with the Unitree G1, utilizing the surface discretization illustrated in Fig. 2. Evaluations in both simulation and real-world environments demonstrate 


Fig. 4: Overview of information flow: Tokenized proprioceptive observations are streamed into iterative CFM refinement modules to progressively infer whole-body contact masks and external wrench fields 

the framework’s robustness and its effectiveness in enabling downstream interactive tasks. 

## _A. Results on the Simulation Contact Dataset_ 

In simulation, we construct contact datasets for training with three representative controllers and settings: 

- **Balancing:** the controller (our customized static-standing policy) balances the robot with sustained non-coplanar contacts. 

- **Locomotion:** an RL policy<sup>1</sup> guides the robot according to a base command. 

- **Motion tracking:** a whole-body tracker<sup>2</sup> follows diverse reference trajectories. 

In all the situations, the robot balances itself against nonfoot impacts. These external disturbances manifest as transient deviations from the nominal dynamics, requiring the estimator to isolate subtle contact signatures during motion. This is particularly challenging during motion tracking, where diverse reference trajectories induce large, non-stationary proprioceptive variations. 

Hence, we collect 10,000 contact rollouts for static-standing and walking settings, and construct a larger dataset for tracking by injecting contacts into 31,961 TWIST2 reference trajectories, resulting in a total of 1,000,000 contact rollouts. The successful recovery of contact events across these regimes demonstrates the robustness and generalization of our approach. 


Fig. 5: Contact dataset collection across behaviors in MuJoCo 

We actively apply and log impulsive interactions that cause noticeable state deviations in real-world operation. Specifically, we sample a contact force with magnitude in [30 _,_ 100] N, with a random direction, and a duration within [0 _._ 1 _,_ 0 _._ 4] s. Both proprioceptive signals and contact labels are recorded at 50 Hz. We convert contacts applied at surfaces into equivalent wrenches at a link’s CoM according to (5) in the robot base frame. 

The estimator consumes a 50-frame proprioceptive window and predicts the corresponding 50-step contact sequence over the same horizon. During training, we enforce a 1:4 positiveto-negative ratio over the clips, where a clip is labeled positive if it contains any non-zero contact within the horizon. 

> 1Unitree’s official walking policy (https://github.com/unitreerobotics/ unitree <u>rl lab)</u> with randomized speed commands. 

> 2The open-source TWIST2 [38] motion-tracking policy with diverse reference trajectories (https://github.com/amazon-far/TWIST2). 

We report contact awareness success rates based on the predicted contact masks across three dimensions in Table I: (i) **whether any non-foot contact occurs** , (ii) **where the contact occurs** , and (iii) **when the contact happens** . Since small temporal or spatial errors are often tolerable in practice, we compute both strict success rates and tolerant success rates. 

TABLE I: Contact awareness performance across tasks 

|**Task**|**Metric (%)**|**Standing**|**Walking**|**Tracking**|
|---|---|---|---|---|
|**(i)hether**|detection rate|84.2|85.5|78.1|
|**w**|false alarm rate|0.4|1.9|15.2|
|**(ii)here**|target link|61.7|58.0|36.9|
|**w**|tolerant ±1 link|76.4|72.8|70.7|
|**iiih**|target timestamp|77.3|33.6|75.9|
|**()wen**|tolerant ± 0.1s|98.1|85.5|93.3|


We care about an additional dimension (iv) **what wrench is applied** , and decompose it into force and torque in both magnitude and direction. 

Table II summarizes the mean estimation errors for contact timing, location, and wrench magnitude, conditioned on the predicted contact mask and estimated wrench. While classification accuracy and estimation precision naturally decrease with increased task complexity, our framework maintains performance comparable to low-cost force-torque sensors. To the best of our knowledge, this work is the first to quantitatively characterize the ’joint-torque-to-contact’ mapping for humanoid robots across diverse, whole-body interactions. 

TABLE II: Mean contact estimation errors across tasks 

|**Task**|**Errors**|**Standing**|**Walking**|**Tracking**|
|---|---|---|---|---|
|**(ii) where**|distance (links)|0.9|0.6|1.2|
|**(iii) when**|interval (ms)|10|24|35|
||force mag (N)|2.1|1.9|1.7|
|**(iv)what**|force direction(deg)|28.7|17.0|25|
||torque mag(N_·_m)|0.4|0.7|0.3|
||torque direction(deg)|33.2|24.2|35|


## _B. Cross-Task Generalization_ 

Different controllers take unique observations; naively collecting controller-specific inputs for training would result in fragmented datasets and task-specific estimators. We define a unified proprioceptive representation that decouples the perception layer from the underlying control logic, enabling a cross-task contact estimator. 

For a humanoid robot, the available proprioceptive observation typically includes **o** = _{_ **q** _,_ **q** ˙ _,_ **_τ_** _,_ **R** base _,_ **_ω_** base _}._ In contrast, the policy input used by many controllers is often _{_ cmd _,_ **q** _,_ **q** ˙ _,_ action _,_ **R** base _,_ **_ω_** base _},_ which differs in three aspects: 

- **High-level commands:** Controllers consume commands in different formats (e.g., walking velocity vs. trajectory segments). Since closed-loop proprioception implicitly 

reflects the command over time, we omit explicit command inputs to the estimator. 

- **Previous action:** The action-to-torque mapping is controller-dependent and varies with stiffness and damping, so actions are not comparable across tasks. Following BeyondMimic [24], we use normalized torques as a taskconsistent surrogate for actions. 

- **Per-signal weights:** While controllers may use different weighting schemes, the raw signal scales are largely consistent; thus we fix a single set of weights across tasks. 

- We standardize the estimator input using only proprio- 

- ceptive signals shared across controllers, forming a unified observation vector 

**o** _t_ = � _wq_ **q** ˜ _t, wq_ ˙ ˙ **q** _t, wω_ **_ω_** base _,t, wg g_ ( **R** base _,t_ ) _, wτ_ **_τ_** ˆ _t_ � _,_ (9) 

where **q** ˜ _t_ = **q** _t −_ **q** default denotes the joint position offset from the default posture, and _g_ ( **R** base) maps the base rotation to the gravity direction expressed in the robot frame. The normalization weights rescale observations for stable training ( _wq,g,τ_ = 1 _, wq_ ˙ = 0 _._ 05 _, wω_ = 0 _._ 2). For torques, we adopt an impedance-aware normalization: for each joint _i_ , 


where _ki_ and _di_ are the joint stiffness (position gain) and damping (velocity gain), and the denominator provides an impedance-motivated torque scale. 


Fig. 6: Comparison of success rates across tasks: task-agnostic vs. task-specific vs. baseline estimators 

As shown in Fig. 6, we compare the task-specific estimator, the task-agnostic estimator, and a baseline estimator that uses cross-task data but is trained on a single task. The results indicate that the performance gap is mainly due to removing controller command/reference information, which makes 

contact inference harder—especially for tracking where the reference provides strong disambiguating context. Meanwhile, multi-task training is beneficial: compared to the single-task baseline, the task-agnostic model’s higher data diversity partially mitigates the absence of command inputs. 

## _C. Zero-Shot Generalization to Multi-Contact Estimation_ 

This test evaluates the scalability of the proposed pipeline when extending from single-contact to multi-contact wrench estimation. In particular, our experiments show that an estimator trained solely on single-contact data can zero-shot generalize to scenarios with simultaneous contacts at multiple locations. 

We further clarify why the estimator is not trained directly on a multi-contact dataset: 

- First, constructing and covering multi-contact configurations is prohibitively expensive: the dataset size grows exponentially with the number of concurrent contact points. 

- Second, multi-contact interactions can be viewed as compositions of single-contact events; hence, the key challenge is to learn contact-relevant proprioceptive features at the level of individual contacts, rather than enumerating all combinations. 

- Third, CFM is well-suited for modeling highly nonuniform distributions, which makes it a natural choice for extrapolating beyond the training support and enables generalization to multi-contact cases. 

In our evaluation, we apply two simultaneous external forces to the left and right wrists of the robot (link indices 21 and 28), as shown in Fig. 7a. Each contact lasts 0.2 s with around 50 N and an arbitrary direction, and we visualize the groundtruth contact by taking the per-link norm of the corresponding 6D wrench, yielding the contact intensity map in Fig. 7b. 


Fig. 7: An example multi-point contact scenario 

We then test a contact estimator trained on the singlecontact dataset only, which has never observed any multicontact sample during training. Fig. 8 shows the predicted contact mask and corresponding wrench estimated purely from proprioceptive signals. The results indicate that, in a subset of challenging scenes, the estimator can perform zero-shot multicontact inference, highlighting a key advantage of the CFMbased formulation: it learns transferable contact signatures 

from sparse supervision and remains robust as contact patterns become more complex than those seen during training. 


(a) Contact mask prediction (b) Contact wrench estimation 

Fig. 8: Zero-shot multi-contact inference 

To verify that this zero-shot generalization stems from CFM’s distributional modeling rather than network capacity alone, we compare against an MLP baseline with hidden size [512 _,_ 512 _,_ 512] trained on the same single-contact locomotion data. The MLP achieves 99 _._ 69% detection on single-contact testing—comparable to CFM—but is evaluated on three simultaneous contacts that induce overlapping proprioceptive effects. We report Top-1 (dominant contact) and Top-3 (multicontact ambiguity) metrics: 

TABLE III: Contact detection metrics under Top-1 and Top-3 settings 

||||**CFM**|**MLP**|
|---|---|---|---|---|
||(i)whether|detection rate|89.31|17.24|
|To-1||false alarm rate|3.06|0.15|
|p<br>Metrics|(ii)where|target link|24.86|9.40|
|(%)||tolerant _±_1 link|50.00|11.29|
||(iii)when|target timestamp|30.06|0.00|
|||tolerant _±_0.1 s|89.02|17.24|
|To-3|(i) whether|any exact hit@3|7.80|0.40|
|p<br>Mti|(ii)where|target link@3|26.80|21.50|
|ercs<br>(%)||tolerant _±_1 link@3|33.80|29.90|
||(iii) when|tolerant _±_0.1 s@3|31.70|9.00|


As shown in Table III, CFM dominates across all metrics. The MLP, despite near-perfect single-contact accuracy, collapses under multi-contact ambiguity—its deterministic mapping cannot represent the multi-modal posterior over overlapping contacts. CFM’s flow-based sampling naturally maintains diverse hypotheses, confirming that distributional modeling is essential for zero-shot multi-contact generalization. 

## _D. Comparison with Model-based Approaches_ 

Despite using carefully grid-searched parameters and being provided with noise-free foot contact measurements in simulation, GMO [11] and CPF [26] remain less robust to sensor noise and less accurate in multi-contact and challenging scenarios. In contrast, SixthSense relies only on proprioceptive and IMU inputs. 

**Case 1: Sensitivity to observation noise in single-contact** 

**localization** . As shown in Fig. 9, when noise assumptions become less accurate and Gaussian noise increases, baselines degrade significantly, while SixthSense maintains localization accuracy. 


Fig. 9: Sensitivity to observation noise under single-contact localization 

**Case 2: Contact disambiguation under multi-contact uncertainty** (GMO not applicable). CPF assumes known contact cardinality, while SixthSense generalizes zero-shot from single-contact training without such prior. Although slower than CPF, SixthSense achieves higher detection and lower false alarm rates. Its performance also degrades more gracefully as contact number increases, indicating better scalability. 

TABLE IV: Performance comparison under multi-contact points 

|Metric||N|umber|of Con|tact Poi|nts|
|---|---|---|---|---|---|---|
|||1|2|3|4|5|
|Time (ms)|CPF<br>SixthSense|56.9<br>370|85.5<br>367|111.4<br>365|133.3<br>373|151.7<br>368|
|DetRate(%)|CPF|45.3|22.7|17.1|13.2|16.9|
|.|SixthSense|60.0|35.2|21.3|19.5|17.9|
|FARt(%)|CPF|12.6|38.7|65.1|79.8|85.8|
|ae|SixthSense|1.9|26.6|23.5|37.5|17.0|


**Case 3: Robustness to challenging cases** . SixthSense (blue) better matches the ground truth (red) than GMO (orange) and CPF (green) in selected cases (a)-(c). The reasons are three-fold: (1) leveraging pre- and post-contact context; 

(2) learning implicit dynamics from data; and (3) capturing complex posterior distributions via CFM. 


## _E. Ablation Study on Controllers with Different Robustness Levels_ 

This ablation study provides empirical evidence for the hypotheses in Sec. IV-B by evaluating how controller robustness affects the observability and estimation performance of external contacts. 

We quantify the controller’s robustness by running 10,000 randomized rollouts across both standing and walking tasks, and use the following metrics to describe their robustness: 

- **Success Rate (SR).** Fraction of rollouts that do _not_ fall: 


- **Integral of Time-weighted Absolute Error (ITAE** mean **).** Time-weighted tracking error (discrete): 


- **Constraint Violation Magnitude (VioMag** mean **).** Mean violation magnitude over time and rollouts: 


As shown in Tab. V, across different tasks, our experiments show that robot motions generated by more robust controllers make contact information easier to infer, consistent with the hypotheses in Sec. IV-B. With stronger controller robustness, we observe only minor changes in detection rate and contact timing (i.e., when contact occurs), but marked improvements in the false-alarm rate, contact location accuracy, and contact force estimation. These findings also provide an indirect explanation for the inferior performance on the tracking task: the tracking controller used in our paper is less robust, which likely degrades the quality and informativeness of the collected data compared to other tasks. 

TABLE V: Effect of controller robustness on contact estimation 

|||||Walking||Tracking|
|---|---|---|---|---|---|---|
||Controller Rob|ustness|**good**|fair|poor|**fair**|
|||SR(%)|99.1|97.4|58.8|80.0|
|Robus|tness|ITAEmean|10.8|14.5|21.3|25.3|
|Me|tric|VioMagmean|0.02|0.21|0.87|0.37|
|||RVR|0.1|0.07|0.06|0.03|
||(i)whether|detection rate|85.5|86.3|89.3|78.1|
|Contact||false alarm rate|1.9|11.0|14.1|15.2|
|Detection|iih|target link|58.0|54.3|52.1|36.9|
|Rate<br>|()were|tolerant ±1 link|72.8|72.6|71.2|70.7|
|(%)|(iii)when|target timestamp|73.6|67.4|66.9|75.9|
|||tolerant ± 0.1s|85.5|89.1|89.0|93.3|
||(ii)where|distance (links)|0.6|0.67|0.70|1.2|
||(iii)when|interval (ms)|24|16|17|35|
|Contact<br>Estimation||force mag (N)|1.9|2.1|2.4|1.7|
|Errors|(iv)what|force dir(deg)|17.0|29.4|32.7|25|
|||torque mag(N·m)|0.7|0.7|0.85|0.3|
|||torque dir(deg)|24.2|29.9|37.1|35|


## _F. Real-World Validation and Sim-to-Real Transfer_ 

We validate the contact estimator on real hardware and demonstrate its plug-and-play and real-time performance. 


Fig. 11: Contact data collection on real Unitree G1 

Before deployment, we improve sim-to-real robustness in two complementary ways. During data collection, we apply domain randomization by varying link mass and inertia, joint damping and friction, actuator strength, and ground friction. During training, we further augment proprioceptive inputs with injected noise to account for sensor noise and residual modeling errors. 

Our real-robot estimator contains _∼_ 100M parameters and performs CFM with 10 refinement steps, resulting in an inference time of 0.5 s per forward pass. As shown in Fig. 11, we attach force sensors to the robot surface to obtain groundtruth contact measurements, which are converted into linklevel CoM-equivalent wrenches. We then apply instrumented 


Fig. 12: Spatiotemporally sparse contact wrench field estimation 

pushes and stream proprioceptive signals to the estimator in real time. 

The estimator outputs two physical quantities over the discretized body surface: a probabilistic contact mask chunk **M** _∈_ [0 _,_ 1]<sup>50</sup><sup>_×_30</sup> and a wrench field chunk **W** _∈_ R<sup>50</sup><sup>_×_30</sup><sup>_×_6</sup> . For visualization in Fig. 12, we report the wrench magnitude by taking the _ℓ_ 2 norm of the 6-D wrench at each cell; note that each grid cell still represents a full 6-D wrench vector in the underlying prediction. Given the predicted mask in Fig. 12a and wrench field in Fig. 12b, we then apply Eq. (4) to select the most likely contact location(s) and the corresponding contact force magnitude(s) in Fig. 12c. Realtime contact estimates capture the applied forces on the target link, with correlated responses on neighboring links that reflect the robot’s kinematic connectivity. 

## _G. Applications: Physical Human–Robot Interaction_ 

Whole-body contact perception is a key enabler for physical human–robot interaction (pHRI). Because physical contacts convey immediate and meaningful information about interactions, inferring contacts from proprioception adds a new interaction channel beyond vision, language, and teleoperation. Fig. 13 highlights three practical benefits. 

**Safety.** Improved whole-body contact perception enables earlier identification of hazardous situations, reducing both self-damage and risk to humans, as shown in Case 4. This addresses the limited contact awareness of many humanoids over the torso and other non-manipulating regions. 

**Contact as command.** When contact is reliably estimated and interpreted, it can serve as a direct and intuitive command channel. As shown in Case 1, a user can pull the robot’s arm 


Fig. 13: Physical human–robot interaction cases with SixthSense contact estimation 

to convey the intention to stand up, and the robot responds naturally without relying on speech or handheld controllers. 

**Feedback for planning.** Our per-step output (a per-region contact mask with a wrench field) forms a structured, highdimensional feedback signal that can be consumed by highlevel planners to support environment-aware decision-making in pHRI. All the cases serve as simple examples of statemachine triggering. 

## VI. CONCLUSION 

We propose a task-agnostic approach that infers humanoid whole-body external contact wrenches from proprioception using conditional flow matching. By casting contact estimation as a spatiotemporal sequence inference problem, we lift fixedpoint contacts to a whole-body contact wrench field over the discretized robot surface, and infer sparse, time-varying contact events as a distribution rather than point estimates. Simulations and real-robot experiments across diverse tasks demonstrate its practical value as a plug-and-play, taskagnostic module that can be readily integrated into existing controllers. 

As one of the first works to study whole-body external wrench perception on real humanoid robots, our approach demonstrates promising results but still faces several limitations: 

- The real-robot data collection in this work remains limited. Acquiring dense, whole-body contact wrench measurements on real humanoids is a major open challenge. 

- The current framework relies exclusively on proprioception. Extending the observation to multiple modalities, 

   - e.g., vision, language, and high-level context, is a necessary step toward general contact-aware humanoid control. 

- We discretize the robot surface at a relatively coarse spatial resolution. While sufficient for locomotion and tracking, finer-grained wrench estimation will be required to support dexterous manipulation and physical human– robot interaction. 

Future research will target these limitations, providing the next-generation humanoid robot with a sixth sense of contact. 

REFERENCES 

- [1] Michael Bloesch, Marco Hutter, Mark A Hoepflinger, Stefan Leutenegger, Christian Gehring, C David Remy, and Roland Siegwart. State estimation for legged robots—consistent fusion of leg kinematics and IMU. _Robotics_ , 17:17–24, 2013. 

- [2] Roberto Calandra, Andrew Owens, Dinesh Jayaraman, Justin Lin, Wenzhen Yuan, Jitendra Malik, Edward H Adelson, and Sergey Levine. More than a feeling: Learning to grasp and regrasp using vision and touch. _IEEE Robotics and Automation Letters_ , 3(4):3300–3307, 2018. 

- [3] Marco Camurri, Maurice Fallon, St´ephane Bazeille, Andreea Radulescu, Victor Barasuol, Darwin G. Caldwell, and Claudio Semini. Probabilistic contact estimation and impact detection for state estimation of quadruped robots. _IEEE Robotics and Automation Letters_ , 2(2):1023–1030, 2017. 

- [4] St´ephane Caron, Adrien Escande, Leonardo Lanari, and Bastien Mallein. Capturability-based pattern generation for walking with variable height. _IEEE Transactions on Robotics_ , 36(2):517–536, 2019. 

- [5] Alessandro De Luca and Raffaella Mattone. Sensorless robot collision detection and hybrid force/motion control. In _Proceedings of the IEEE International Conference on Robotics and Automation_ , pages 999–1004. IEEE, 2005. 

- [6] Alessandro De Luca, Alin Albu-Schaffer, Sami Haddadin, and Gerd Hirzinger. Collision detection and safe reaction with the DLR-III lightweight manipulator arm. In _IEEE/RSJ international conference on intelligent robots and systems_ , pages 1623–1630. IEEE, 2006. 

- [7] Roy Featherstone. _Rigid body dynamics algorithms_ . Springer, 2008. 

- [8] Fabrizio Flacco, Antonio Paolillo, and Abderrahmane Kheddar. Residual-based contacts estimation for humanoid robots. In _IEEE-RAS International Conference on Humanoid Robots_ , pages 409–415, 2016. 

- [9] Yukai Gong, Ross Hartley, Xingye Da, Ayonga Hereid, Omar Harib, Jiunn-Kai Huang, and Jessy Grizzle. Feedback control of a Cassie bipedal robot: Walking, standing, and riding a Segway. In _2019 American control conference_ , pages 4559–4566. IEEE, 2019. 

- [10] Sami Haddadin, Alin Albu-Schaffer, Alessandro De Luca, and Gerd Hirzinger. Collision detection and reaction: A contribution to safe physical human-robot interaction. In _IEEE/RSJ International Conference on_ 

_Intelligent Robots and Systems_ , pages 3356–3363. IEEE, 2008. 

- [11] Sami Haddadin, Alessandro De Luca, and Alin AlbuSch¨affer. Robot collisions: A survey on detection, isolation, and identification. _IEEE Transactions on Robotics_ , 33(6):1292–1312, 2017. 

- [12] Ross Hartley, Maani Ghaffari, Ryan M. Eustice, and Jessy W. Grizzle. Contact-aided invariant extended Kalman filtering for robot state estimation. _The International Journal of Robotics Research_ , 39(4):402–430, 2020. 

- [13] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 8944–8951. IEEE, 2024. 

- [14] Ayonga Hereid, Omar Harib, Ross Hartley, Yukai Gong, and Jessy W Grizzle. Rapid trajectory optimization using C-FROST with illustration on a Cassie-series dynamic walking biped. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 4722–4729, 2019. 

- [15] Jemin Hwangbo, Carmine Dario Bellicoso, P´eter Fankhauser, and Marco Hutter. Probabilistic foot contact estimation by fusing information from dynamics and differentialforward kinematics. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 3872–3878. IEEE, 2016. 

- [16] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 4(26):eaau5872, 2019. 

- [17] Gwanghyeon Ji, Juhyeok Mun, Hyeongjun Kim, and Jemin Hwangbo. Concurrent training of a control policy and a state estimator for dynamic and robust legged locomotion. _IEEE Robotics and Automation Letters_ , 7 (2):4630–4637, 2022. 

- [18] Abderrahmane Kheddar, St´ephane Caron, Pierre Gergondet, Andrew Comport, Arnaud Tanguy, Christian Ott, Bernd Henze, George Mesesan, Johannes Englsberger, M´aximo A Roa, et al. Humanoid robots in aircraft manufacturing: The airbus use cases. _IEEE Robotics & Automation Magazine_ , 26(4):30–45, 2019. 

- [19] Diederik P Kingma and Max Welling. Auto-encoding variational Bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- [20] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. RMA: Rapid motor adaptation for legged robots. _arXiv preprint arXiv:2107.04034_ , 2021. 

- [21] Mike Lambeta, Po-Wei Chou, Stephen Tian, Brian Yang, Benjamin Maloon, Victoria Rose Most, Dave Stroud, Raymond Santos, Ahmad Byagowi, Gregg Kammerer, et al. DIGIT: A novel design for a low-cost compact high-resolution tactile sensor with application to in-hand manipulation. _IEEE Robotics and Automation Letters_ , 5 (3):3838–3845, 2020. 

- [22] Joonho Lee, Jemin Hwangbo, Lorenz Wellhausen, Vladlen Koltun, and Marco Hutter. Learning quadrupedal 

locomotion over challenging terrain. _Science Robotics_ , 5 (47):eabc5986, 2020. 

- [23] Michelle A Lee, Yuke Zhu, Peter Zachares, Matthew Tan, Krishnan Srinivasan, Silvio Savarese, Li Fei-Fei, Animesh Garg, and Jeannette Bohg. Making sense of vision and touch: Learning multimodal representations for contact-rich tasks. _IEEE Transactions on Robotics_ , 36(3):582–596, 2020. 

- [24] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [25] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [26] Lucas Manuelli and Russ Tedrake. Localizing external contact using proprioceptive sensors: The contact particle filter. In _IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5062–5069. IEEE, 2016. 

- [27] George Mesesan, Johannes Englsberger, Gianluca Garofalo, Christian Ott, and Alin Albu-Sch¨affer. Dynamic walking on compliant and uneven terrain using dcm and passivity-based whole-body control. In _2019 IEEERAS 19th International Conference on Humanoid Robots_ , pages 25–32, 2019. 

- [28] J. Joe Payne, Daniel A. Hagen, Denis Garagi´c, and Aaron M. Johnson. Multi-momentum observer contact estimation for bipedal robots. _arXiv preprint arXiv:2412.03462_ , 2024. 

   - [35] Youcan Yan, Zhe Hu, Zhengbao Yang, Wenzhen Yuan, Chaoyang Song, Jia Pan, and Yajing Shen. Soft magnetic skin for super-resolution tactile sensing with force selfdecoupling. _Science Robotics_ , 6(51):eabc8801, 2021. 

   - [36] Wenxuan Yuan, Siyuan Dong, and Edward H Adelson. GelSight: High-resolution robot tactile sensors for estimating geometry and force. _Sensors_ , 17(12):2762, 2017. 

   - [37] Yanjie Ze, Zixuan Chen, Joao Pedro Ara´ujo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C Karen Liu. TWIST: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

   - [38] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. TWIST2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

   - [39] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Huaping Liu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

   - [40] Zongzheng Zhang, Haobo Xu, Zhuo Yang, Chenghao Yue, Zehao Lin, Huan-ang Gao, Ziwei Wang, and Hao Zhao. Elucidating the design space of torque-aware vision-language-action models. In _9th Annual Conference on Robot Learning_ , 2025. 

   - [41] Peiyuan Zhi, Peiyang Li, Jianqin Yin, Baoxiong Jia, and Siyuan Huang. Learning unified force and position control for legged loco-manipulation. _arXiv preprint arXiv:2505.20829_ , 2025. 

- [29] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. DeepMimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics_ , 37(4):1–14, 2018. 

- [30] C David Remy. Ambiguous collision outcomes and sliding with infinite friction in models of legged systems. _The International Journal of Robotics Research_ , 36(12): 1252–1267, 2017. 

- [31] Bruno Siciliano, Oussama Khatib, and Torsten Kr¨oger. _Springer handbook of robotics_ , volume 200. Springer, 2008. 

- [32] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Scorebased generative modeling through stochastic differential equations. _arXiv preprint arXiv:2011.13456_ , 2020. 

- [33] Sudharshan Suresh, Haozhi Qi, Tingfan Wu, Taosha Fan, Luis Pineda, Mike Lambeta, Jitendra Malik, Mrinal Kalakrishnan, Roberto Calandra, Michael Kaess, et al. NeuralFeels with neural fields: Visuotactile perception for in-hand manipulation. _Science Robotics_ , 9(96): eadl0628, 2024. 

- [34] Alexander Tong, Kilian Fatras, Nikolay Malkin, Guillaume Huguet, Yanlei Zhang, Jarrid Rector-Brooks, Guy Wolf, and Yoshua Bengio. Improving and generalizing flow-based generative models with minibatch optimal transport. _arXiv preprint arXiv:2302.00482_ , 2023. 

