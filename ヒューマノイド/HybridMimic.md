---
title: "HybridMimic: Hybrid RL-Centroidal Control for Humanoid Motion Mimicking"
date: "2026-03-06"
authors: "Ludwig Chee-Ying Tay; I-Chia Chang; Yan Gu"
url: https://arxiv.org/abs/2603.06775
pdf: https://arxiv.org/pdf/2603.06775
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.06775)** / [論文ページ](https://arxiv.org/abs/2603.06775)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HybridMimic: Hybrid RL-Centroidal Control for Humanoid Motion Mimicking 

Ludwig Chee-Ying Tay<sup>1</sup> , I-Chia Chang<sup>2</sup> , Yan Gu<sup>2</sup><sup>_†_</sup> 

**_Abstract_ —Motion mimicking, i.e., encouraging the control policy to mimic human motion, facilitates the learning of complex tasks via reinforcement learning (RL) for humanoid robots. Although standard RL frameworks demonstrate impressive locomotion agility, they often bypass explicit reasoning about robot dynamics during deployment, which is a design choice that can lead to physically infeasible commands when the robot encounters out-of-distribution environments. By integrating model-based principles, hybrid approaches can improve performance; however, existing methods typically rely on predefined contact timing, limiting their versatility. This paper introduces HybridMimic, a framework in which a learned policy dynamically modulates a centroidal-model-based controller by predicting continuous contact states and desired centroidal velocities. This architecture exploits the physical grounding of centroidal dynamics to generate feedforward torques that remain feasible even under domain shift. Using physics-informed rewards, the policy is trained to efficiently utilize the centroidal controller’s optimization by outputting precise control targets and reference torques. Through hardware experiments on the Booster T1 humanoid, HybridMimic reduces the average base position tracking error by 13% compared to a state-of-the-art RL baseline, demonstrating the robustness of dynamics-aware deployment.** 

## I. INTRODUCTION 

In the context of Reinforcement Learning (RL) for humanoids, motion mimicking, i.e., encouraging the control policy to mimic human motion via tracking rewards, serves as a technique to improve motion naturalness and sample efficiency while achieving locomotion and loco-manipulation tasks. Motion mimicking has enabled humanoids to walk, run, and dance naturally [1], [2] and perform loco-manipulation tasks, e.g., box picking [3]. With these successes, it is promising to utilize motion mimicking to build embodied intelligence that can achieve diverse complex task for various applications. The primary objective of this work is to introduce HybridMimic, a hybrid control architecture that integrates RL with a modelbased controller to enable humanoid robots to learn diverse and physically grounded motions. This framework addresses the substantial challenge of ensuring physical feasibility in standard RL during deployment while simultaneously eliminating the dependency of traditional model-based controllers on hand-crafted, predefined contact schedules. 

> _†_ Corresponding author. 1 Ludwig Chee-Ying Tay is with Department of Computer Science, Purdue University, West Lafayette, IN 47907, USA. E- mail: tay3@purdue.edu. 2 I-Chia Chang and Yan Gu are with the School of Mechanical Engineering, Purdue University, West Lafayette, IN 47907, USA. E-mail: _{_ chang970, yangu _}_ @purdue.edu. 


Fig. 1: Snapshots of Booster T1 executing the kicking task using the proposed HybridMimic controller. (a) The robot starts standing. (b) The robot walks forward. (c) The robot kicks with its left foot. (d) The robot recovers and stabilizes from the kick and steps backwards. More motion can be found in the supplementary video. https://youtu.be/1d5vkqNtCOY 

## _A. Related Work_ 

_1) Standard RL:_ RL policies are typically trained in physics-based simulators to ensure physical feasibility, and with domain randomization [4], [5] employed to ensure robustness against various disturbances [6]. However, standard RL frameworks, especially those that use a ProportionalDerivative (PD) controller to enable joint-level torque generation, do not explicitly reason about robot dynamics during deployment. As a result, when the policy’s observations deviate from the training distribution, the policy network lacks a mechanism to generate physically feasible commands, leading to degraded sim-to-real performance. 

_2) Analytical-model-based control:_ Despite their theoretical grounding [7] and impressive success in enabling dynamic locomotion in various environments [8]–[12], model-based controllers face significant hurdles when tasked with enabling agile and robust locomotion in unstructured environments, due to the high-dimensional, hybrid, nonlinear nature of the associated robot dynamics. Classical inverted-pendulum-based methods [13]–[17] often rely on simplifying assumptions, such as constant Center-of-Mass (CoM) height, which are frequently violated during natural human-like motions such as crouching or jumping. Even more sophisticated centroidal models [18] typically require predefined, rigid contact schedules to remain computationally tractable. These hand-crafted heuristics struggle to generalize to “in-the-wild” motions where contact timing is non-periodic or difficult to specify a priori. Furthermore, the performance of these controllers is 

strictly capped by the accuracy of the underlying reducedorder model; they lack the inherent ability to learn from experience or adapt to unmodeled environmental nuances. These limitations necessitate a learning-based approach that can discover optimal control strategies while still respecting fundamental physical constraints. 

_3) Hybrid methods:_ Hybrid methods that integrate components or principles from model-based controllers into RL frameworks have been studied to improve performance. To improve the training efficiency, [19], [20] employ modelbased outputs as reference signals to guide policy training. Meanwhile, [21]–[25] adopt model-based whole-body controllers as the torque generators in their RL frameworks. These frameworks facilitate precise tracking [22], higher walking speeds [23], increased agility in quadruped jumping [24], and improved rejection of external disturbances [25], demonstrating that the inclusion of a model-based torque controller can significantly improve locomotion performance. 

While promising, existing hybrid methods rely on simplifying assumptions that limit their applicability for diverse motion mimicking. Inverted pendulum-based approaches [23], [25] assume a constant CoM height, an approximation that does not generally hold for human-like motion. Another common approach, centroidal methods [22], [24], typically require predefined footstep timings. 

## _B. Contributions_ 

In this paper, we propose HybridMimic, a hybrid control architecture that combines RL with a centroidal-modelbased controller to generate feasible torque commands through centroid dynamics. Our HybridMimic formulation enables contact state estimation using policy observation, removing the requirement of hand-crafted contact schedules [22], [24]. The proposed controller offers a general framework for learning diverse motions by training it to mimic human reference motions [1], [2] (see Fig.1). The specific contributions of this work are as follows: 

- (a) **Contact-schedule-free formulation** : Unlike existing hybrid centroidal methods [22], [24], HybridMimic estimates continuous contact states based on observations, eliminating the need for predefined contact schedules and providing smooth contact transitions. Additionally, HybridMimic optimizes the ground reaction forces by considering the reference torque output by the policy network. This allows diverse ground reaction force profiles to emerge naturally, making it well-suited to complex contact transitions inherent in motion mimicking. 

- (b) **Physics-based rewards** : We introduce novel reward terms that are functions of the inputs and outputs of the centroidal controller, e.g., commanded accelerations, estimated contact states, and ground reaction forces. These rewards encourage consistent and physically grounded use of the centroidal controller by the policy, resulting in an interpretable and transparent model-based controller that can streamline physical deployment. 

- (c) **Real-world deployment** : Through extensive sim-to-sim and sim-to-real experiments, we demonstrate that HybridMimic successfully learns to perform diverse human motions while maintaining performance comparable to a state-of-the-art baseline [1]. We further highlight the benefits of integrating model-based control by showing a reduced sim-to-real gap in robot base position tracking during locomotion, achieving a 13% reduction in base position error compared to the baseline. 

## II. PRELIMINARIES 

We first review the robot dynamics models and the associated nomenclature for HybridMimic. We focus on full-order dynamics to relate feedforward torque and ground reaction force, and centroidal dynamics to relate ground reaction force and centroidal acceleration. These models bridge the highlevel centroidal acceleration command to the low-level joint torque using physics-based models. 

## _A. Full-order Dynamics_ 

Using multi-rigid-body dynamics, the dynamics equation of a humanoid robot can be expressed as 


where _q_ ˜ _∈_ R<sup>6+</sup><sup>_n_</sup> is the generalized coordinates of the floatingbase humanoid robot with _n_ the total number of joints, _M_ (˜ _q_ ) _∈_ R<sup>(6+</sup><sup>_n_)</sup><sup>_×_(6+</sup><sup>_n_)</sup> is the inertial matrix, _H_ (˜ _q, q_ ˜<sup>˙</sup> ) _∈_ R<sup>6+</sup><sup>_n_</sup> is the sum of Coriolis, centrifugal, and gravitational terms, _u ∈_ R<sup>_n_</sup> is the joint motor torque, _B ∈_ R<sup>(</sup><sup>_n_+6)</sup><sup>_×n_</sup> is the input matrix, and _Fi ∈_ R<sup>6</sup> and _Ji ∈_ R<sup>6</sup><sup>_×_(</sup><sup>_n_+6)</sup> are the ground reaction wrench and the corresponding Jacobian for the contact indexed by _i ∈E_ . The set _E_ represents the set of all possible contact surfaces on the robot. In this work, a limited set _E_ = _{_ left foot _,_ right foot _}_ is considered. However, given feasible motion clips, the proposed framework could be readily extended to consider more possible contacting surfaces, e.g., hands, knees, and elbows. 

## _B. Centroidal Dynamics_ 

To enable high-frequency control and avoid complex computations during RL training, we use a single rigid body (SRB) model to capture the centroidal dynamics of the humanoid robot. A SRB model assumes the mass of the robot is concentrated at the CoM, the angular inertia is constant, and the motion can be controlled by the ground reaction wrench _Fi_ with lever arms _ri ∈_ R<sup>3</sup> for all _i ∈E_ [18]. The linear acceleration _x_ ¨lin _∈_ R<sup>3</sup> and the angular acceleration _x_ ¨ang _∈_ R<sup>3</sup> of the centroid can be expressed as 


where _m ∈_ R is the total mass of the robot, _g ∈_ R<sup>3</sup> is the gravitational acceleration vector, _Fi,_ lin _∈_ R<sup>3</sup> is the linear 

2 


Fig. 2: Diagram illustrating HybridMimic controller formulation in both training and deployment. The dashed items represent training specific elements that are unused during deployment. 

portion of _Fi_ , _Ic ∈_ R<sup>3</sup><sup>_×_3</sup> is the rotational inertial matrix of the robot about the CoM, _Fi,_ ang _∈_ R<sup>3</sup> is the angular portion of _Fi_ , and [ _ri_ ] _×_ is the skew-symmetric matrix of _ri_ . Stacking the two equations above gives: 


where _x_ ¨ = [¨ _x_<sup>_⊤_</sup> lin<sup>_,_¨</sup><sup>_x⊤_</sup> ang<sup>]</sup><sup>_⊤_,</sup><sup>_A_horizontallystacksall</sup><sup>_Ai∀i∈E_,</sup> and _F_ vertically stacks all _Fi ∀i ∈E_ . 

## III. METHODOLOGY 

To mimic a motion reference _q_ ˜ref( _t_ ) retargeted from a human demonstration [26], a controller needs to generate motor torque _u_ ( _t_ ) to minimize the difference between the motion reference _q_ ˜ref( _t_ ) and the actual motion _q_ ˜( _t_ ) performed by the robot. For simplicity, we omit the explicit dependence on time in the rest of the paper. Inspired by model-based control [27], [28], our HybridMimic controller (Fig. 2) computes motor torque as the sum of a feedforward torque _u_ FF and a PD torque _u_ PD: 


Similar to standard RL [1], [2], the PD term is designed by 


where _KP_ and _KD_ are the stiffness and damping matrices of motors, _q ∈_ R<sup>_n_</sup> is the actual joint position, and _q_ cmd _∈_ R<sup>_n_</sup> is the commanded joint position generated by the policy network. Using the PD term alone has been shown to be empirically effective for locomotion tasks and can implicitly 

handle both feedforward and feedback terms [29]. However, the PD formulation encodes all the control command into a single channel _q_ cmd governed by the policy. Xiong et al. [30] suggest that the standard PD formulation may cause latency without feedforward velocity command. 

Thus, in addition to the PD term, a centroidal controller is used to generate a feedforward torque _u_ FF for HybridMimic. 

## _A. Feedforward torque generation_ 

To compensate for the effect of contact wrench and the bias force _H_ , the feedforward torque is generated by the following: 


where _B_<sup>_†_</sup> is the pseudo-inverse of _B_ and _Fi_<sup>_∗_isthefeasible</sup> ground reaction wrench estimate for the contact _i ∈E_ . 

A feasible estimate of contacting wrenches _Fi_<sup>_∗_</sup> _∀i ∈E_ is obtained by solving the following constrained quadratic programming (QP) problem to respect the centroidal dynamics and the estimated contact states: 


where the commanded centroidal acceleration _x_ ¨cmd is determined by 


Here, _K_ vel _∈_ R<sup>6</sup><sup>_×_6</sup> is the gain for centroidal velocity tracking, _x_ ˙ cmd = [ ˙ _x_<sup>_⊤_</sup> cmd,lin<sup>_,x_˙</sup><sup>_⊤_</sup> cmd,ang<sup>]</sup><sup>_⊤∈_R6isthecommandedcentroidal</sup> 

3 

TABLE I: Actor and critic observations. Actor has access to the baseline observation while the critic has both the baseline and privileged observation. An observation history of four policy timesteps are stacked together. 

|Term|Observation|Dimension|
|---|---|---|
||Baseline Observation<br>Rfiii||
|_q_ref<br>˙_q_ref<br>˙_PB_<br>_ωB_<br>_q_<br>˙_q_|eerence jont poston<br>Reference joint velocity<br>Base frame linear velocity<br>Base frame angular velocity<br>Current joint position<br>Current joint velocity|_n_<br>_n_<br>3<br>3<br>_n_<br>_n_|
||Privileged Observation<br>||
|_p_ref<br>_p_|Reference base position in world frame<br>Current base position in world frame|3<br>3|
|_RW B,_ref|Reference base frame orientation relative to<br>world frame (the 6 elements of the first two<br>columns of a 3_×_3 Rotation matrix)|6|
|_RW B_|Current base frame orientation relative to<br>world frame|6|


velocity output by the policy network, and _x_ ˙ _∈_ R<sup>6</sup> is the actual centroidal velocity. The cost function _L_ ( _F_ ) is defined as 


where _u_ ref _∈_ R<sup>_n_</sup> is the reference torque generated by the policy, _Kτ_ is the nominal weight of reference torque cost and is scaled by the motor torque limit _τ_ limit _∈_ R<sup>_n_</sup> where _τ_ limit<sup>_−_2</sup> represents the element-wise inverse square of _τ_ limit. _wi ∈_ R is the contact state for the _i_<sup>th</sup> contact surface in _E_ and is generated by the policy. _K_ lin and _K_ ang are the nominal weights of the end-effector contacting cost and are scaled by the contact state _wi_ . A larger _wi_ implies that the _i_<sup>th</sup> surface is more likely to be in contact with the environment. We adopt a continuous description of contact state to ensure a continuous mapping from policy actions to joint torque, thereby avoiding sudden jumps in torque that may hinder RL training. 

The cost function can be expressed as a quadratic form _L_ ( _F_ ) = 21<sup>_F ⊤QF_+</sup><sup>_c⊤F_wherethedetaileddefinitionsof</sup> _Q_ and _c_ are omitted. This allows the optimal solution to (9) to be expressed in a closed form as shown below, which facilitates the efficient computation during training and realworld deployment: 


Finally, the feedforward torque is clipped to respect the motor torque limit _τ_ limit to ensure safety and feasibility. 

In our HybridMimic formulation, the policy network generates outputs to adjust the reference torque _u_ ref, the contact state _wi_ for the _i_<sup>th</sup> contact, and the commanded centroidal velocity _x_ ˙ cmd. These outputs enable the policy network to exploit the structure of the QP problem and the SRB dynamic model 

TABLE II: Values of reward terms. Reward terms are split into tracking, regularization, and HybridMimic categories. Tracking terms are taken directly from [1] with adjusted parameters. The HybridMimic terms are described in Secs. III-B1 _σ_ , the, rewardIII-B2, isIII-B3defined, andasIII-B4 _r_ = _e_ . _σ_ For _<u>ϵ</u>_<sup><u>2</u></sup> whereterms _ϵ_ withrepresentssensitivitythe error between the desired and measured values. 

|Type|Reward|Weight|Sensitivity|
|---|---|---|---|
||Global anchor position<br>Global anchor orientation|0.7<br>0.7|0.3<br>0.4|
|Tracking|Body position<br>Body orientation<br>Body linear velocity<br>Body angular velocity|1<br>1<br>1<br>1.25|0.2<br>0.3<br>0.5<br>2.09|
|Regularization|L2 action rate<br>Undesired contacts|-0.08<br>-0.5|-<br>-|
||GRF reward|0.15|100|
|HybridMimic|Contact state reward<br>Torque limit reward|0.5<br>0.1|-<br>-|
||Centroidal acceleration (lin)|0.1|6|
||Centroidal acceleration (ang)|0.1|12|


to generate feedforward torque without prior knowledge of the contact schedule. By scaling the end-effector contact cost weights using _wi_ , the formulation produces significant ground reaction wrenches only for contact surfaces with a high contact state value. Through the reference torque cost term, the policy network gains greater control over _F_<sup>_∗_</sup> , particularly when the equality constraint in (9) has infinitely many solutions (e.g., during the double-support phase), and implicitly prevents violations of the friction cone and actuation limit. 

## _B. RL policy_ 

To train a policy network to utilize the proposed hybrid controller in (6), an RL problem is formulated as a Partially Observable Markov Decision Process (POMDP), represented by a tuple _⟨S, O, A, P, r, γ⟩_ . Here, _S_ is the state space, _O_ is the observation space (Tab. I), _A_ is the action space (including _u_ ref, _wi ∀i ∈E_ , _x_ ˙ cmd, and _q_ cmd), _PS′|S,A_ is the state transition probability, _r_ : _O×A →_ R is the reward function (Tab. II), and _γ_ is the discount factor. The policy _πθ_ : _O →A_ , parameterized by _θ_ , is trained to maximize the expected discounted return over trajectories initialized from an initial state drawn from the initial distribution _s_ 0 _∼ p_ 0, where actions _at_ are selected given the observations _ot_ at time step _t_ : 


We utilize Proximal Policy Optimization [31] with an asymmetric actor-critic [32] for efficient learning to train one policy for each motion clip. To improve robustness, domain randomization is used as summarized in Tab. III. 

A key novelty of this work is the introduction of reward functions that ensure feasible utilization of the centroidal controller. We encourage feasible utilization of the controller by minimizing the error between simulated values, such as ground reaction wrench _F_ sim, and the predicted value, _F_<sup>_∗_</sup> , through reward design. Our rewards facilitate the derivation 

4 

TABLE III: Settings of domain randomization applied to improve policy robustness. Terms with + have a uniformly distributed random noise added to the true value. Terms with * have a uniformly distributed random factor multiplied to the true value. We add random noise to HybridMimic inputs to prevent the policy from learning behaviors that exploit using the centroidal controller for noise-free observation. 

|Type|Randomization Term|Range|
|---|---|---|
|Observations|Base linear velocity noise (m/s)<br>Base angular velocity noise (rad/s)<br>Joint position noise (rad)<br>Joint velocity noise (rad/s)|+(-0.5, 0.5)<br>+(-0.2, 0.2)<br>+(-0.02, 0.02)<br>+(-0.5, 0.5)|
||Mass randomization _M_ (kg)|*(0.98, 1.02)|
|HybridMimic<br>input|Inertia matrix _Ic_<br>Jacobian _J_<br>End-effector position _r_ (m)|*(0.98, 1.02)<br>*(0.98, 1.02)<br>+(-0.02, 0.02)|
||Initial joint position (rad)|+(-0.1, 0.1)|
|Environment|Body CoM position offset (m)<br>Base velocity push (m/s)|+(-0.025, 0.025)<br>+(1.0, 3.0)|


of accurate, interpretable outputs, including ground reaction wrenches, contact states, and centroidal acceleration. 

The following sections describe the specific rewards implemented for HybridMimic. 

_1) Ground reaction force (GRF) reward:_ The policy network should, when utilizing the centroidal controller correctly, generate an estimate of ground reaction wrench _Fi_<sup>_∗_closeto</sup> the value _Fi,_ sim from the simulator for the _i_<sup>th</sup> contact. Thus, a reward is given for minimizing the error between the two values. 


The sensitivity constant _σgrf ∈_ R can be chosen based on the magnitude of the expected contacting wrench of the humanoid robot. 

_2) Contact state reward:_ The contact state _wi_ generated by the policy network should match the contact state _wi,_ sim obtained through the simulator. A penalty is given for the predicted contact state of the policy network deviating from the true contact state 


_3) Torque limit reward:_ For computational efficiency, the centroidal controller does not consider torque limits. The policy network is intended to implicitly learn to utilize _u_ ref to avoid exceeding torque limits. A torque limit penalty is applied when _u_ FF exceeds a soft torque limit. 


where _α ≈_ 0 _._ 9 and the subscript [ _·_ ] _j_ indicates the _j_<sup>th</sup> joint. 

_4) Centroidal acceleration reward:_ The robot’s acceleration in simulation should match the commanded acceleration computed by equation (10). To encourage this behavior, a centroidal acceleration reward is implemented for minimizing 

the error between the simulated acceleration _x_ ¨sim and the commanded centroidal acceleration _x_ ¨cmd. 


where _σacc ∈_ R is the sensitivity constant detailed in Table II. 

IV. RESULTS AND ANALYSIS 

To validate the effectiveness of the proposed HybridMimic framework to mimic human motion, we conduct an extensive study of both sim-to-sim and sim-to-real transfer. In the study, several variations of the controller are compared to show that the proposed design is crucial to achieving the improved motion mimicking performance. The controllers include: 

- (i) **BeyondMimic** [1]: This produces an RL policy using only a PD controller (7) as the torque generator, and serves as our baseline to highlight the performance gains introduced by the centroidal controller. 

- (ii) **HybridMimic** : The proposed controller from Sec. III. 

- (iii) **HybridMimic with fixed contact schedule (FCS) (termed as “HybridMimic+FCS”)** : This is HybridMimic but with the contact state _wi_ derived from the reference motion. We set _wi_ = 1 if the distance between the _i_<sup>th</sup> contact surface and the environment is below a threshold and _wi_ = 0 otherwise. This ablation is used to demonstrate that the policy-estimated contact states _wi_ are necessary for robust motion mimicking. 

- (iv) **HybridMimic+FCS without Reference Torque Cost (RTC) (termed as “HybridMimic+FCS-RTC”)** : This is the HybridMimic+FCS formulation with the reference torque cost removed from the cost function _L_ ( _F_ ). As our most complete ablation, this setup closely mirrors previous hybrid centroidal controllers [22], [24]. We use it to show that policy-generated contact states _wi_ and reference torques _u_ ref are essential for robust performance. 

To evaluate the performance of a controller, we compare the difference between the trajectory rollout in the training environment _q_ train (which is a good approximation of _q_ ref after sufficient training) and the rollout during evaluation _q_ eval either in the MuJoCo simulation or in the real experiment. We use _q_ train as a baseline instead of the motion reference _q_ ref since the latter may not be dynamically feasible to be tracked by the robot due to retargeting issues [26]. The difference between _q_ eval and _q_ train also characterizes the capability of the controller under domain shift caused by sim-to-sim or sim-toreal transfer. In this study, the following performance metrics are used: 

- (a) **Base final position error (m)** : The L2 norm of the base position error at the end of the motion clip. 

- (b) **Base mean position error (m)** : The averaged L2 norm of the base position error across the entire motion clip. 

- (c) **Base mean orientation error (rad)** : The averaged L2 norm of orientation error across the entire motion clip. 

- (d) **Base velocity root-mean-square (RMS) error (m/s)** : The RMS value of the L2 norm of linear velocity error for the entire motion clip. 

5 

TABLE IV: Training and HybridMimic parameters. 

||Training Param<br>|eters<br>||
|---|---|---|---|
|Term|Value|Term|Value|
|# of environments|8192|# of iterations|15000|
|Episode length|10s|Learning rate|10<sup>_−_3</sup>|
|Desired KL|0.01|Value loss coeff.|1.0|
|Entropy coeff.|0.005|Clip ratio|0.2|
|Actor size|[1024,512,256,256]|_γ_ (Discount factor)|0.99|
|Critic size|[1024,512,256,256]|_λ_ (GAE decay)|0.95|
||HybridMimic Par|ameters||
|Term|Value|Term|Value|
|_K_vel,lin<br>_Kτ_<br>_K_ang|5_I_3<br>100_In_<br>0_._02_I_3|_K_vel,ang<br>_K_lin|10_I_3<br>10<sup>_−_3</sup>_I_3|


space in full HybridMimic. However, the fragility of fixed contact schedules becomes evident in running, where complex contact patterns and disturbances require adaptable scheduling. 

## _C. Hardware Experiments_ 

We train the HybridMimic and BeyondMimic policies on a series of motion clips involving dynamic locomotion tasks: 

   - (1) **Forward walking** : Starting from standing, the robot walks forward [38]. The task has duration 7 _s_ . 

   - (2) **Side-stepping** : Sidestep to the right [36]. The task has duration 6 _._ 5 _s_ . 

   - (3) **Backwards stepping** : Stepping backwards [36]. The task has duration 6 _s_ . 

- (e) **Base angular velocity RMS Error (rad/s)** : The RMS value of the L2 norm of angular velocity error for the entire motion clip. 

## _A. Training_ 

We implemented HybridMimic in IsaacLab [33] and trained our policies on a Booster T1 humanoid robot for various motion clips. The parameters used in the training environment are described in Tab. IV. The policy network is operated at 50 Hz and the centroidal controller runs at 500 Hz. The stiffness matrix _KP_ for HybridMimic is 0.75 times that suggested in [1]. When training the policy on a walking task using a partial A100 GPU instance provided by [34], we measured the wall clock time to be 15.4 hours for BeyondMimic and 22.3 hours for HybridMimic, representing a computational overhead of 31% in training time. 

## _B. Sim-to-Sim Results_ 

We train all four policies on three 10- _s_ motion clips: 

- (1) **Walking to kneeling** : Robot walks forward then high kneels on the right leg [35]. 

- (2) **Running in Circle** : Robot runs in a circle [36]. 

- (3) **Jumping** : Robot jumps forward using both legs [37]. 

We evaluated the trained policies in the IsaacLab training environment without domain randomization to obtain datasets of 256 trained trajectories _q_ train, with a large count to mitigate the nondeterministic effects of the IsaacLab environments. We then evaluate the policies in MuJoCo to obtain _q_ eval. The simto-sim tracking results are shown in Tab. V, and the video can be found in the supplementary video. 

For all three motion clips, HybridMimic and BeyondMimic are able to mimic the reference motion, while HybridMimic demonstrates lower tracking error in linear position, linear velocity, and angular velocity, showing the proposed framework improves the motion mimicking performance through the feedforward torque. By comparing the HybridMimic with its variants, it can be found that the HybridMimic+FCS and HybridMimic+FCS-RTC have higher tracking error than full HybridMimic for the first two motion clips, where the contact timing is more complex than the jumping motion. The strong performance of HybridMimic+FCS-RTC in the jumping task likely stems from the motion’s simple contact schedule, which allows for easier learning due to the lack of redundant action 

- (4) **Kicking** : Robot steps forward then kicks with the left leg before stepping backwards to original location [38]. The task has duration 8 _s_ . 

The trained policies are deployed on the real robot. VICON motion-capture cameras are used both to capture tracking data and to provide linear velocity information for policy observation at 100 Hz. On the real robot, the centroidal controller was run at 350 Hz due to hardware limitations. Each policy was executed to obtain three successful trials per motion clip. HybridMimic performs complex dynamic tasks in the real world (Fig. 1, supplementary video), with tracking statistics shown in Tab. V. 

As shown in Tab. V, HybridMimic achieves an about 13% reduction in base position tracking error across all four realworld motions compared to the BeyondMimic baseline. This demonstrates that the proposed HybridMimic improves the sim-to-real tracking performance compared to a state-of-theart baseline. For the sidestepping motion, Fig. 3 shows the robot’s base position trajectory in the direction of travel. As shown in Fig. 3, the proposed HybridMimic performs a smoother motion and stays closer to the trajectory shown in training environments, while the motion controlled by BeyondMimic is more jittery and has a larger base position tracking error and can be illustrated in the experiment video. 

During sim-to-real deployment, we noted that tuning HybridMimic parameters was comparatively straightforward due to the transparent and explainable nature of the proposed design. One example involves adjusting the gain _K_ vel for centroidal velocity tracking to balance the sensor noise level and the velocity tracking performance. 

## _D. Results Analysis_ 

Alongside demonstrating the reduced tracking error, another feature of HybridMimic is the transparent and interpretable behavior of the centroidal controller. In this section, we discuss the ground reaction force solved from the QP problem (9) and the feedforward torque generated by HybridMimic and its variant during the walking then kneeling motion task in a sim-to-sim study. 

The estimated ground reaction forces of HybridMimic and HybridMimic+FCS are shown in Fig. 4. HybridMimic learns to accurately estimate ground reaction forces, with a small error between the simulated and estimated ground reaction 

6 

TABLE V: Sim-to-sim and sim-to-real tracking errors across motion clips and controller variants. The bolded figures represent the **lowest** tracking error in the category. The underlined figures represent the <u>second best</u> in the category. The text with background color is the <mark>proposed method</mark> . 

||||Sim-to-Sim Results||||
|---|---|---|---|---|---|---|
|Task|Model|Base Final Position<br>Error (m)|Base Mean Posi-<br>tion Error (m)|Base Mean Orien-<br>tation Error (rad)|Base Velocity Er-<br>ror (m/s)|Base Angular Ve-<br>locity Error (rad/s)|
||BeyondMimic|0.4739 _±_ 0.031|0.3344 _±_ 0.021|0.1577 _±_ 0.012|0.1331 _±_ 0.004|0.2881 _±_ 0.007|
|Walking|HybridMimic+FCS|0.6824 _±_ 0.021|0.4768 _±_ 0.014|0.2356 _±_ 0.007|0.1291 _±_ 0.002|0.3021 _±_ 0.004|
|to Kneeling|HybridMimic+FCS-RTC|0.3641 _±_ 0.015|0.2633 _±_ 0.013|**0.1513** _±_ **0.006**|0.1202 _±_ 0.004|0.2679 _±_ 0.007|
||HybridMimic|**0.3455** _±_ **0.011**|**0.2366** _±_ **0.008**|0.1576 _±_ 0.003|**0.1105** _±_ **0.001**|**0.2285** _±_ **0.002**|
||BeyondMimic|0.3435 _±_ 0.008|0.2653 _±_ 0.007|0.1597 _±_ 0.005|0.1985 _±_ 0.002|0.3961 _±_ 0.002|
|Running|HybridMimic+FCS|0.5626 _±_ 0.042|0.2930 _±_ 0.031|0.1757 _±_ 0.013|0.2066 _±_ 0.003|0.5064 _±_ 0.004|
|in Circle|HybridMimic+FCS-RTC|1.8963 _±_ 0.009|0.7606 _±_ 0.009|0.4071 _±_ 0.005|0.4894 _±_ 0.000|0.8870 _±_ 0.001|
||HybridMimic|**0.3289** _±_ **0.012**|**0.2622** _±_ **0.010**|**0.1413** _±_ **0.009**|**0.1497** _±_ **0.001**|**0.3711** _±_ **0.004**|
||BeyondMimic|0.4670 _±_ 0.018|0.2794 _±_ 0.010|0.2827 _±_ 0.006|0.5346 _±_ 0.001|1.4305 _±_ 0.002|
|Ji|HybridMimic+FCS|0.3771 _±_ 0.012|0.2225 _±_ 0.007|0.1518 _±_ 0.004|0.2168 _±_ 0.001|0.5657 _±_ 0.002|
|umpng|HybridMimic+FCS-RTC|**0.3571** _±_ **0.009**|**0.1929** _±_ **0.006**|**0.1253** _±_ **0.004**|**0.1957** _±_ **0.000**|**0.4566** _±_ **0.002**|
||HybridMimic|0.3926 _±_ 0.017|0.2217 _±_ 0.009|0.1521 _±_ 0.005|0.2306 _±_ 0.002|0.5548 _±_ 0.003|
||||Sim-to-Real Results||||
|Sidestein|BeyondMimic|0.0942 _±_ 0.042|0.0471 _±_ 0.003|**0.0614** _±_ **0.004**|0.2767 _±_ 0.092|**0.7708** _±_ **0.006**|
|ppg|HybridMimic|**0.0694** _±_ **0.008**|**0.0401** _±_ **0.002**|0.0962 _±_ 0.001|**0.2676** _±_ **0.078**|0.7810 _±_ 0.001|
|Backwards|BeyondMimic|0.1849 _±_ 0.002|0.0500 _±_ 0.001|0.0912 _±_ 0.002|0.1994 _±_ 0.001|0.9044 _±_ 0.003|
|Stepping|HybridMimic|**0.1079** _±_ **0.011**|**0.0405** _±_ **0.002**|**0.0834** _±_ **0.004**|**0.1947** _±_ **0.005**|**0.8978** _±_ **0.003**|
|Forwards|BeyondMimic|0.2275 _±_ 0.067|0.0592 _±_ 0.006|**0.0808** _±_ **0.011**|0.3293 _±_ 0.036|0.8762 _±_ 0.078|
|Walking|HybridMimic|**0.1377** _±_ **0.025**|**0.0496** _±_ **0.001**|0.0912 _±_ 0.006|**0.1856** _±_ **0.004**|**0.7581** _±_ **0.001**|
|Kickin|BeyondMimic|0.1564 _±_ 0.051|0.0580 _±_ 0.001|**0.1338** _±_ **0.007**|0.9608 _±_ 0.016|0.6388 _±_ 0.014|
|g|HybridMimic|**0.1131** _±_ **0.009**|**0.0567** _±_ **0.002**|0.1826 _±_ 0.005|**0.9402** _±_ **0.008**|**0.6360** _±_ **0.006**|


Fig. 3: The left two images illustrate the robot displacement after two sidesteps for (a) BeyondMimic and (b) HybridMimic controllers. (c) The projected base position _p_ ˆ is the base position projected onto the line from the starting to ending position in the reference motion clip. While the real HybridMimic trajectory oscillates around the trained motion, the real BeyondMimic trajectory consistently undershoots it and induces trunk wobbling as shown in the experiment video. 


Fig. 4: The vertical ground reaction force of left foot during walking in simulation for (a) HybridMimic and (b) HybridMimic+FCS. The highlighted regions indicate periods of time during which the contact state indicates the left foot is contacting the ground. For HybridMimic, the highlighting occurs when _w_ left foot _>_ 0 and for HybridMimic+FCS , the highlighting occurs when the reference motion has a foot height below 0.007m. 

force. Visual illustration can be found in the supplementary video. Additionally, we compare it to HybridMimic+FCS and show that learning contact states is crucial because errors in the contact schedule derived from the motion reference lead to brittle and inaccurate ground reaction force computation. This downgrades the tracking performance through inaccurate feedforward torque generation in (8) and requires the policy to generate additional PD torque to compensate for it. 

Figure 5 shows the feedforward torque _u_ FF, reference torque _u_ ref, and simulated torque for the left and right knee joints under HybridMimic. When a foot contacts the ground, the 

actual and feedforward torques are similar, indicating that most motor torque is generated by the centroidal-controller-driven feedforward term. During swing phase, the feedforward torque remains small but nonzero due to the _H_ term in (8). The reference torque roughly follows the feedforward torque but is not expected to match it, as it is an additional control channel for the policy. 

## V. CONCLUSION AND FUTURE WORK 

This paper has introduced HybridMimic, a hybrid framework integrating centroidal-model-based control with reinforcement learning (RL) to track diverse, dynamic motion ref- 

7 


Fig. 5: Feedforward, actual, and reference torque during walking for the left and right knee pitch joints. The highlighted region corresponds to contact on the corresponding leg determined by when _wi >_ 0. 

erences. Through physics-informed reward design, the policy network learns to modulate commanded centroidal velocities and continuous contact states. This allows the centroidal controller to generate feedforward torques that effectively counteract ground reaction wrenches. Experimental results on the Booster T1 humanoid demonstrated that HybridMimic achieved a 13% reduction in base position tracking error compared to a state-of-the-art RL baseline during sim-toreal transfer. The synergy between centroidal control and RL facilitates deterministic parameter tuning, such as adjusting velocity tracking gains, which streamlines the deployment process. Finally, HybridMimic permits reduced joint stiffness, yielding compliant behavior for safer hardware operation. 

Although HybridMimic effectively regulates ground reaction forces for stability and performance, the current feedforward formulation does not explicitly optimize swing-leg trajectories, which are critical for precise foot placement. Future work will explore integrating model-based swing-leg control, such as task-space control, into the existing architecture to enhance the tracking accuracy during leg-swing phases of highly dynamic maneuvers. 

## ACKNOWLEDGMENT 

The authors would like to thank Muqun Hu and Zijian He for insightful discussion and thank Zenan Zhu for experimental support. Hardware support from Booster Robotics is gratefully acknowledged. This work used Jetstream2 GPU at Indiana University through allocation MCH250079 from the Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support (ACCESS) program, which is supported by U.S. National Science Foundation grants #2138259, #2138286, #2138307, #2137603, and #2138296. The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217. 

## REFERENCES 

- [1] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu, “BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [2] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “DeepMimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Trans. Graph._ , vol. 37, no. 4, pp. 1–14, 2018. 

- [3] G. B. Margolis, M. Wang, N. Fey, and P. Agrawal, “SoftMimic: Learning compliant whole-body control from examples,” _arXiv preprint arXiv:2510.17792_ , 2025. 

- [4] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel, “Sim-toreal transfer of robotic control with dynamics randomization,” in _Proc. IEEE Int. Conf. Rob. Autom._ , May 2018, p. 3803–3810. 

- [5] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _Proc. IEEE/RSJ Int. Conf. Intell. Rob. Syst._ , 2017, pp. 23–30. 

- [6] Y. Gu, G. Shi, F. Shi, I.-C. Chang, Y.-J. Wang, Q. Cheng, Z. Olkin, I. Lopez-Sanchez, Y. Feng, J. Zhang, H. Su, and K. Sreenath, “Evolution of humanoid locomotion control,” 2025, under review. 

- [7] E. R. Westervelt, J. W. Grizzle, C. Chevallereau, J. H. Choi, and B. Morris, _Feedback Control of Dynamic Bipedal Robot Locomotion_ . CRC Press, 2007. 

- [8] O. Dosunmu-Ogunbi, A. Shrivastava, G. Gibson, and J. W. Grizzle, “Stair climbing using the angular momentum linear inverted pendulum model and model predictive control,” in _Proc. IEEE Int. Conf. Intel. Rob. Syst._ , 2023, pp. 8558–8565. 

- [9] Y. Gao, V. Paredes, Y. Gong, Z. He, A. Hereid, and Y. Gu, “Timevarying foot placement control for humanoid walking on swaying rigid surface,” _IEEE Trans. Rob._ , 2025. 

- [10] A. Iqbal, Y. Gao, and Y. Gu, “Provably Stabilizing Controllers for Quadrupedal Robot Locomotion on Dynamic Rigid Platforms,” _IEEE Trans. Mechatron._ , vol. 25, no. 4, pp. 2035–2044, Aug. 2020. 

- [11] M. Dai, X. Xiong, J. Lee, and A. D. Ames, “Data-driven adaptation for robust bipedal locomotion with step-to-step dynamics,” in _Proc. IEEE Int. Conf. Intel. Rob. Syst._ , 2023, pp. 8574–8581. 

- [12] S. Kuindersma, R. Deits, M. Fallon, A. Valenzuela, H. Dai, F. Permenter, T. Koolen, P. Marion, and R. Tedrake, “Optimization-based locomotion planning, estimation, and control design for the ATLAS humanoid robot,” _Auton. Rob._ , vol. 40, no. 3, pp. 429–455, 2016. 

- [13] S. Kajita, F. Kanehiro, K. Kaneko, K. Yokoi, and H. Hirukawa, “The 3D linear inverted pendulum mode: a simple modeling for a biped walking pattern generation,” in _Proc. IEEE Int. Conf. Intell. Rob. Syst._ , vol. 1, 2001, pp. 239–246 vol.1. 

- [14] Y. Gao, Y. Gong, V. Paredes, A. Hereid, and Y. Gu, “Time-varying ALIP model and robust foot-placement control for underactuated bipedal robotic walking on a swaying rigid surface,” in _Proc. Amer. Contr. Conf._ , 2023, pp. 3282–3287. 

- [15] X. Xiong and A. Ames, “3-D underactuated bipedal walking via H- LIP based gait synthesis and stepping stabilization,” _IEEE Trans. Rob._ , vol. 38, no. 4, pp. 2405–2425, 2022. 

- [16] J. Stewart, I.-C. Chang, Y. Gu, and P. A. Ioannou, “Adaptive ankle torque control for bipedal humanoid walking on surfaces with unknown horizontal and vertical motion,” in _Proc. Amer. Contr. Conf._ , 2025, pp. 4647–4652. 

- [17] A. Iqbal, S. Veer, and Y. Gu, “Analytical solution to a time-varying lip model for quadrupedal walking on a vertically oscillating surface,” _Mechatron._ , vol. 96, p. 103073, 10 2023. 

- [18] J. Di Carlo, P. M. Wensing, B. Katz, G. Bledt, and S. Kim, “Dynamic locomotion in the MIT Cheetah 3 through convex model-predictive control,” in _Proc. IEEE/RSJ Int.Conf.Intell. Rob. Syst._ , 2018, pp. 1–9. 

- [19] D. Kang, J. Cheng, M. Zamora, F. Zargarbashi, and S. Coros, “Rl + model-based control: Using on-demand optimal control to learn versatile legged locomotion,” _IEEE Rob. Autom. L._ , pp. 1–8, 2023, early Access. 

- [20] Y. Yan, T. Egle, C. Ott, and D. Lee, “Efficiently learning robust torquebased locomotion through reinforcement with model-based supervision,” _arXiv preprint arXiv:2601.16109_ , 2026. 

- [21] Z. Xie, X. Da, B. Babich, A. Garg, and M. v. de Panne, “GLiDE: Generalizable quadrupedal locomotion in diverse environments with a centroidal model,” in _Int. Workshop Algorith. Found. Rob._ , 2022, pp. 523–539. 

- [22] J. Cheng, D. Kang, G. Fadini, G. Shi, and S. Coros, “RAMBO: RLaugmented model-based whole-body control for loco-manipulation,” _arXiv preprint arXiv:2504.06662_ , 2025. 

- [23] G. A. Castillo, B. Weng, S. Yang, W. Zhang, and A. Hereid, “Template model inspired task space learning for robust bipedal locomotion,” in _IEEE/RSJ Int. Conf. Intell. Rob. Syst._ , 2023, pp. 8582–8589. 

8 

- [24] Y. Yang, G. Shi, X. Meng, W. Yu, T. Zhang, J. Tan, and B. Boots, “CAJun: Continuous adaptive jumping using a learned centroidal controller,” in _Conf. Rob. learn._ , 2023, pp. 2791–2806. 

- [25] T. Egle, Y. Yan, D. Lee, and C. Ott, “Enhancing model-based step adaptation for push recovery through reinforcement learning of step timing and region,” in _IEEE-RAS Int. Conf. Humanoid Rob._ , 2024, pp. 165–172. 

- [26] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [27] H. Sadeghian, C. Ott, G. Garofalo, and G. Cheng, “Passivity-based control of underactuated biped robots within hybrid zero dynamics approach,” in _Proc. IEEE Int. Conf.Rob.Autom._ , 2017, pp. 4096–4101. 

- [28] J. Reher and A. D. Ames, “Inverse dynamics control of compliant hybrid zero dynamic walking,” in _Proc. IEEE Int. Conf.Rob.Autom._ , 2021, pp. 2040–2047. 

- [29] S. Lyu, X. Lang, H. Zhao, H. Zhang, P. Ding, and D. Wang, “RL2AC: Reinforcement learning-based rapid online adaptive control for legged robot robust locomotion,” in _Proc. Rob.: Sc Syst._ , July 2020. 

- [30] Z. Xiong, L. Fang, J. Huang, K. Yamazaki, H. Zhang, and C. Gan, “ExtremControl: Low-latency humanoid teleoperation with direct extremity control,” _arXiv preprint arXiv:2602.11321_ , 2026. 

- [31] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Prox- 

imal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [32] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, “Asymmetric actor critic for image-based robot learning,” in _Proc. Robot.: Sci. Syst._ , 2018. 

- [33] “NVIDIA Isaac lab,” https://developer.nvidia.com/isaac/lab, retrieved 2025. 

- [34] T. J. Boerner, S. Deems, T. R. Furlani, S. L. Knuth, and J. Towns, “Access: Advancing innovation: NSF’s advanced cyberinfrastructure coordination ecosystem: Services & support,” in _Practice and experience in advanced research computing 2023: Computing for the common good_ , 2023, pp. 173–176. 

- [35] A. C. C. for the Arts and T. O. S. U. Design, “MoCap system and data,” n.d., online. Available: https://accad.osu.edu/research/motion-lab/mocapsystem-and-data; Accessed: Feb. 19, 2026. 

- [36] Carnegie Mellon University Graphics Lab, “CMU graphics lab motion capture database,” http://mocap.cs.cmu.edu/, 2003, accessed: Feb. 19, 2026. 

- [37] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal, “Robust motion in-betweening,” vol. 39, no. 4, 2020. 

- [38] M. M¨uller, T. R¨oder, M. Clausen, B. Eberhardt, B. Kr¨uger, and A. Weber, “Documentation Mocap database HDM05,” Universit¨at Bonn, Tech. Rep. CG-2007-2, June 2007. 

9 

