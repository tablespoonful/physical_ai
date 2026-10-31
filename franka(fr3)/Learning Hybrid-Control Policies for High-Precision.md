---
title: "Learning Hybrid-Control Policies for High-Precision In-Contact Manipulation Under Uncertainty"
date: "2026-04-21"
authors: "Hunter L. Brown; Geoffrey Hollinger; Stefan Lee"
url: https://arxiv.org/abs/2604.19677
pdf: https://arxiv.org/pdf/2604.19677
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.19677)** / [論文ページ](https://arxiv.org/abs/2604.19677)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Learning Hybrid-Control Policies for High-Precision In-Contact Manipulation Under Uncertainty** 

Hunter L. Brown<sup>1</sup> , Geoffrey Hollinger<sup>1</sup> , and Stefan Lee<sup>1</sup> 

**_Abstract_ — Reinforcement learning-based control policies have been frequently demonstrated to be more effective than analytical techniques for many manipulation tasks. Commonly, these methods learn neural control policies that predict endeffector pose changes directly from observed state information. For tasks like inserting delicate connectors which induce force constraints, pose-based policies have limited explicit control over force and rely on carefully tuned low-level controllers to avoid executing damaging actions. In this work, we present hybrid position-force control policies that learn to dynamically select when to use force or position control in each control dimension. To improve learning efficiency of these policies, we introduce Mode-Aware Training for Contact Handling (MATCH) which adjusts policy action probabilities to explicitly mirror the mode selection behavior in hybrid control. We validate MATCH’s learned policy effectiveness using fragile peg-in-hole tasks under extreme localization uncertainty. We find MATCH substantially outperforms pose-control policies – solving these tasks with up to 10% higher success rates and 5x fewer peg breaks than pose-only policies under common types of state estimation error. MATCH also demonstrates data efficiency equal to pose-control policies, despite learning in a larger and more complex action space. In over 1600 sim-to-real experiments, we find MATCH succeeds twice as often as pose policies in high noise settings (33% vs. 68%) and applies** _∼_ **30% less force on average compared to variable impedance policies on a Franka FR3 in laboratory conditions.** 

## I. INTRODUCTION 

Many real-world tasks induce strict force constraints throughout operation; e.g., excessive or inconsistent force may damage components in industrial assembly [1], lead to uneven underwater welds [2], or harm delicate tissue in medical settings [3]. The precision planning necessary to avoid violating these constraints analytically is often unachievable due to noisy sensing and uncertain state estimation. This is especially challenging when engaging and disengaging contact for which inaccurate workpiece localization can lead to unexpected collision forces or unstable jittering contact. Consequently, these tasks require methods that adapt robustly during execution and are compliant with the environment. 

Many analytical approaches have been proposed to address these issues by explicitly controlling contact forces. Researchers have hand-defined constraint frames [4], deployed constrained optimization techniques [5], or fit model parameters with data gathered from demonstrations [6]. Often, these approaches assume a model and use system identification, demonstrations, or other data to fit the parameters. These systems have been shown to be brittle, 

*This work was funded in part by Office of Naval Research grant N00014-22-1-2114 and National Science Foundation grant 2437138. 

> 1 Collaborative Robotics and Intelligent Systems Institute, Oregon State University, Corvallis, OR 


Fig. 1. a) Using hybrid position-force control allows for directional compliance. Our approach makes control policies able to specify desired mode selection, force goal _fgoal_ , and pose goal _pgoal_ . This allows better force regulation and improves policy performance. b) Three common phases of fragile Peg-In-Hole. Robots start by approaching the hole in free-space. Upon interaction with the work piece, it enters the initial contact phase. Finally, insertion begins when the peg is aligned to the hole, ready to complete the task. Each task phase requires a different control strategy. 

requiring task-specific contact state estimation and handdesigned compliance strategies that must be re-derived for each new workpiece geometry or operating condition [7]. 

Recently, reinforcement learning methods have been effective for many complex tasks without explicit models [8], [9]. Repeated interaction with the environment allows the policy to learn observation-to-action mappings that can generalize effectively [10], without requiring prior knowledge or assumptions about the system dynamics. These methods often utilize simple kinematic action spaces (e.g., pose control) [11], but there is growing interest in variable impedance control (VIC) [12]. By allowing learned policies to dynamically vary the gains in pose control, VIC methods enable indirect force regulation and have shown impressive results for in-contact manipulation tasks [13]. 

However, direct force control has long been argued as essential for contact rich problems in classic literature [4] with hybrid position-force control being a natural fit. Due to difficulties in training in a combined discrete-continuous action space, controller stability, and sim-to-real difficulty, no method has been able to fully leverage the powerful force regulation direct methods afford. Prior methods have constrained or simplified the controller-policy interaction to ease training, but this limits policy expressiveness [14], [15]. 

In this work, we develop the first framework to fully integrate hybrid position-force control in model-free reinforcement learning. As in Fig. 1 (a), our policy network produces pose and force goals at each time step and then 

selects dynamically between the two control modes for each control dimension. For the example peg insertion task shown, this action space allows our policies to learn control strategies that maintain contact with the workpiece via force control in the downward axis while maneuvering laterally via pose commands for hole-peg alignment. 

When modeled as a general mixed discrete-continuous action space without considering the controller [16], we find that this basic formulation reduces sample efficiency during training, compared to VIC and pose control policies. To overcome this, we introduce Mode Aware Training for Contact Handling (MATCH). To better encode how the controller actually utilizes the model outputs during training, MATCH structures the action probabilities to include only the selected pose or force distributions. We find hybrid control policies trained with MATCH achieve comparable sample efficiency to VIC and pose while retaining the benefits of hybrid control. Further, we also encourage realistic and safe action selection with a supervised selection loss based on contact. 

Taken together in simulated fragile peg-in-hole (fPiH) tasks with significant estimation noise, we find both our basic hybrid and MATCH trained policies improve successful insertion rates while breaking fewer pegs compared to posebased policies. Specifically for MATCH, we observe as much as a 10% increase in success rate under extreme noise and 5x fewer peg breaks. We find that MATCH’s performance matches VIC and represents a viable alternative that offers direct force control. Next, we analyze the control strategy learned by MATCH and find that it is similar to humandesigned approaches and semantically meaningful. Finally, across 1600 sim-to-real insertions across noise levels on a Franka FR3 in laboratory conditions, we find MATCH substantially improves success rate compared to pose-based policies (up to +35%). Compared to VIC-based methods, MATCH achieves similar success while exerting up to _∼_ 30% less force. 

**Contributions.** To summarize our contributions, we: 

- Introduce hybrid position-control learned with reinforcement learning for in-contact tasks and show its effectiveness in simulated fragile peg-in-hole experiments. 

- Identify a shortcoming of applying uninformed reinforcement learning techniques to hybrid control and present Mode Aware Training for Contact Handling (MATCH), which improves learning efficiency. 

- Provide detailed analysis that characterizes the learned behaviors of the MATCH trained policies, as well as the effects of state estimation noise and peg geometry. 

- Demonstrate direct sim-to-real transfer of our learned policies on 1600 fragile peg-in-hole insertions, on a Franka FR3 in laboratory conditions. 

## II. RELATED WORK 

**Analytical Approaches.** Analytical approaches to in-contact manipulation make extensive use of direct force control. Hybrid position-force control allows for positional control in some directions and force control in the others [4]. This 

requires careful definition of constraint frames, such as in Bruyninckx et al. [17]. These type of approaches have been shown to make brittle systems [7], [18] motivating attempts to find robust approaches. 

Commonly, this involves developing search strategies that, combined with hybrid control, increase robustness. Chhatpar et al. define several types of search strategies for peg-inhole (PiH), but most commonly employed is the spiral search [5]. Canonical spiral search for PIH typically defines a force constraint parallel to the hole and position control in the plane above the hole, a strategy which our learning-based method also converges towards. Under this constraint, the spiral search pattern ensures the peg will align and complete the insertion. Extensions to this include Kang et al. that use estimates of uncertainty to scale the spiral [19]. While these methods show the importance of direct force control, they require task-specific engineering and do not generalize across geometries or operating conditions [7], [18]. This motivates our use of learning-based approaches that can discover forceaware policies directly from interaction. 

**Force in Reinforcement Learning (RL).** Recent work has shown that force observations improve effectiveness of policies trained for in-contact manipulation [20], [10], [21]. However, incorporating force into RL has been shown to complicate learning. For instance, Huang et al. find that including force targets in the reward can lead to overly conservative behavior [22]. We mitigate this risk in MATCH by designing a loss that encourages safe controller behaviors, without any task specific safety rewards. This contactbased loss makes it easier for the policy to learn the force constraints, without providing negative feedback. Lee at al. introduced a similar contact prediction loss as an auxiliary objective [23]; however, our supervision is tied explicitly to force selection to directly guide policy learning . 

**Force in Action Spaces.** Manipulating the gains of lowlevel controllers provides an indirect way of regulating force. Bogdanovic et al. shows that allowing the policy to control impedance improves task performance, while making the policy more interpretable. Buchli et al. introduced variable impedance control (VIC) for use in joint space, and use a model-based approach [12]. Mart´ın-Mart´ın et al. expanded this concept to VIC in end-effector space (VICES), and compared against common action spaces using model-free RL. They showed increased sample efficiency, safety, and used less energy [13]. We position our work as an alternative to VICES with the critical distinction being that our method regulates force directly via hybrid position-force control. 

Most similar to our work, Anand et al. used a model-based method to perform VIC with hybrid position-force control. To simplify training, they define the control mode in each direction a priori [15]. This limits policies to manually fixed position-force control strategies that cannot adapt to differing task phases. For example in fPiH, during search it may be ideal to control position in xy to find the hole and force in z to prevent breaks. Then during insertion having position control in the z-direction provides a smoother 

decent while force control in the xy-directions can ensure compliance with hole walls. Strategies our method discovers during training (see Sec. VI-D). 

An alternative indirect force control relationship is admittance control which defines how the robot will respond to external force. Zhang et al. trained policies with admittance control action spaces in simulation and refined them online [24]. Beltran-Hernandez et al. focus on comparing admittance control with parallel position-force control for robots incapable of joint torque control [14]. This differs from MATCH as admittance control simply defines the compliance to force. The parallel controller is more similar to our approach, but uses continuous selection weights that blend position and force commands simultaneously, potentially allowing conflicting objectives on the same axis. A discrete selection, like we use, prevents conflicting objectives but increases learning difficulty. MATCH deals with this learning difficulty directly, by defining action probabilities based on how the controller actually uses policy outputs. 

## III. PRELIMINARIES 

Our work is motivated by non-prehensile, in-contact manipulation task settings – i.e., tasks like cable insertion, scraping, or welding [25] that require sustained contact between the robot and the environment. These tasks typically induce direct or indirect force constraints, such as maintaining a specific pressure on a welding arc to ensure a consistent bead or limiting sheer forces to avoid breaking delicate cables during insertion. Tight tolerances, complex contact dynamics, and uncertainty in state estimation make managing these constraints challenging in real deployments. In this work, we take fragile peg-in-hole (fPiH) as an appropriate case study for reinforcement learning of hybrid positionforce control policies that can address these challenges by explicitly regulating desired forces while in contact. 

## _A. Fragile Peg-in-Hole (fPiH)_ 

The fPiH task requires a manipulator to insert a held peg into a hole without breaking it. If exposed to a force greater than some threshold, _Fth_ , the peg breaks and the policy fails the task. We selected this task as it is a canonical incontact manipulation problem, requires satisfying strict force constraints, and can be easily modulated to increase difficulty by adjusting state estimation noise or _Fth_ . 

To formalize fPiH in a reinforcement learning setting, we cast it as a Partially Observable Markov Decision Process (POMDP) [26]. Following standard conventions, the POMDP is defined by a state space _S_ , an observation function Ω: _S →O_ that maps states to policy observations, actions _A_ which the policy can perform, a transition function _T_ : _S × A →S_ that describes how actions affect the environment, a reward function _R_ : _S →_ R which assigns scalar values to states, and a discount factor _γ_ which we describe below. 

_States._ A state _st ∈S_ captures the true physical configuration of the environment at time step _t_ , including poses, velocities, and experienced forces of the manipulator, peg, and goal. We 

also include contact forces and a directional binary contact indicator for each axis. 

_Transitions._ During simulation-based training, we use the Factory simulation environment [27] implemented in IsaacLab to update the state given an action as a proxy for the outcome of physical interaction in the real environment. 

_Observations._ The robot observation _ot_ consists of noisy estimates of the relative position between the end-effector and hole, hole orientation, end-effector velocity, and endeffector forces at time _t_ . 

_Rewards._ We leverage the dense reward from [18] which provides increasingly fine-grained rewards for moving towards insertion, engagement with the hole, and task completion. 

_Actions._ Action spaces will vary depending on the underlying robot controller and are detailed in the following sections. These include goal end-effector poses (Sec. III-B) or forces, or both for our proposed method (Sec. IV-B). 

_Policy._ The objective of a learned policy _πθ_ : _O → P_ ( _A_ ) parameterized by _θ_ is to map observations to a distribution over actions such that the expected discounted cumulative reward is maximized under that action distribution, i.e., 


Notably, policy actions are interpreted by a low-level control law which typically executes at a much higher frequency and is treated as part of the transition function during learning. 

## _B. Learning-Based Pose Control Policies_ 

A common choice in prior work is for the policy to output end-effector poses that are passed to a standard pose controller. Following standard conventions, rigid articulated robotic system dynamics are described by 


where _q_ are the joint angles, _M_ ( _q_ ) is the inertia matrix, _C_ ( _q, q_ ˙) is the Coriolis matrix, _g_ ( _q_ ) are the gravity terms and _u_ is the joint torque control [28]. 

To control pose, the following control law can be used: 


where _kp_ and _kd_ are the proportional and derivative gains, _x_ is the robot’s 6-dimensional end-effector pose (xyz,RPY), _xd_ is the desired end-effector pose, _J_ is the robot’s Jacobian and _Mx_ is the task-space mass matrix [28]. 

To drive this controller, we consider pose control policies that represent the action distribution, _p_ ( _a_ ), as a product of per-control dimension scaled tanh-transformed Gaussians with observation-dependent means and standard deviations such that the _i_ th dimension’s target _xdi_ is produced as 


where _kth_<sup>_p_scalestothemin/maxactionlimits.Thedesired</sup> pose _xd_ is sampled in this way at each timestep and used in Eq. 3. While conceptually simple and commonly applied, this formulation can result in unbounded forces if the desired pose causes collision with the environment. 

## IV. LEARNING HYBRID POSITION-FORCE CONTROL 

In this work, we examine an alternative to this standard pose-control paradigm – hybrid position-force control. Hybrid control allows the policy to directly regulate forces in any direction, enabling more complex manipulation strategies. However, optimizing for hybrid control in a reinforcement learning framework introduces challenges. Hybrid action spaces create a credit assignment problem, where a discrete mode selection changes which continuous commands (pose or force) are actually applied. We address these challenges with a controller-informed RL formulation. 

## _A. Hybrid Force-Position Control_ 

A hybrid position-force controller selects between position and force control on each dimension, allowing regulation of the applied force in some directions and pose in the others. For end-effector control, this choice is represented with the selection matrix Λ, a 6-dimensional diagonal binary matrix, where a 1 indicates pose control and 0 represents force control in that dimension [4]. 

The force controller adjusts the robot’s motion to maintain a desired contact force, _fd_ , enabling compliant behavior during contact. The desired force is compared against the robot’s current end-effector force, _fee_ , and generates control commands with a proportional controller with gain _kf_ . The overall control law is written as 


which combines pose and force control terms. 

To design a corresponding policy, we can output an observation-dependent probability of selecting force control as _ϕ_ ( _ot_ ), parameterizing a Bernoulli distribution for each control dimension. The selection matrix Λ is sampled as 


This is a key difference between our contribution and prior work. Anand et al. manually defined Λ before deployment [15], limiting the control strategies available to the policy. Beltran-Hernandez et al. used a parallel position-force controller [14], treating Λ as a continuous variable that blends force and position components. This allows contradictory commands but simplifies learning since each output contributes to every action. This work treats selection as a _discrete_ action, so only a force or pose component can contribute to the robot’s behavior in each direction preventing contradictions while learning a dynamic control selection strategy. 

In addition to target pose distributions as in Eq. 4, we also produce force target distributions as scaled, tanh-transformed 

Gaussians with observation-dependent means and variances such that per-control dimension force _fdi_ goals are given as 


where _kth_<sup>_f_scales to the min / max action. In practice, we im-</sup> plement selection probabilities ( _ϕi_ ) and target distribution parameters ( _µxi_ , _σxi_ , _µfi_ , _σfi_ ) as outputs from a neural policy. In the standard RL settings, where the underlying robot controller is considered an unknown part of the transition function, the overall action distribution would be written as _p_ ( _a_ )= � _p_ ( _xdi | µxi, σxi_ ) _p_ ( _fdi | µfi, σfi_ ) _p_ (Λ _ii | ϕi_ ) _,_ (8) _i_ 

where each policy output is independent – mirroring common formulations for mixed discrete-continuous action RL [16]. We denote this configuration as Hybrid-Basic. As far as the authors are aware, this is the first time hybrid control with discrete selection has been used in on-policy model-free RL. 

## _B. Mode-Aware Action Distribution_ 

While straightforward, the formulation in Eq. 8 offers a poor reflection of each action components’ contribution to the hybrid controller. For instance, the _predicted force goal_ in a dimension for which _pose control was selected_ plainly has no effect on the overall action. When coupled with policy gradient methods, that adjust model parameters to increase or decrease _p_ ( _a_ ) based on observed rewards, this formulation propagates gradients through outputs unused by the controller, resulting in potentially uninformative updates [29]. 

To account for this, we define _p_ ( _a_ ) as a product over each control dimension, _p_ ( _a_ ) =<sup>�</sup> _i_<sup>_c_(</sup><sup>_ai_),wherewedefinethe</sup> per-control dimension distribution _c_ ( _ai_ ) piecewise as 


such that each control dimension considers only the selection variable and corresponding force or pose action. In this way, we clearly assign credit and apply gradients to only the component actually used. We denote this novel action distribution Mode Aware Training for Contact Handling (MATCH). 

## _C. Supervised Selection Loss_ 

Free-space force control is risky due to the possibility of unbounded acceleration, destabilizing the controller and damaging the environment. Early in training when the robot is not consistently engaging the work piece, this creates a stern penalty for selecting force. Consequently, the policy is unlikely to explore force control when it does start engaging the work piece. Moreover, our experiments showed that only 20%-40% of steps involve contact, further reducing the likelihood of sampling useful force control actions. 

To combat this, we add a supervised selection loss defined as the binary cross-entropy between the selection probability _p_ (Λ _ii_ ) and the true contact state _ψi_ in control dimension _i_ : 


TABLE I 

NOMINAL PERFORMANCE ON FPIH IN TRAINING CONDITION. RESULTS AVERAGED OVER 5 SEEDS. BEST PERFORMANCE PER METRIC IN **BOLD** . 

||Method|Success (%) _↑_|Break (%) _↓_|Time (s) _↓_|Force (N) _↓_|
|---|---|---|---|---|---|
|1|Pose|95.4 _±_ 1.6|1.6 _±_ 1.5|2.5 _±_ 0.4|1.9 _±_ 0.3|
|2|VICES [13]|95.2 _±_ 2.4|1.4 _±_ 2.3|2.7 _±_ 0.2|2.0 _±_ 0.2|
|3|Hybrid-Basic|**98.2** _±_ **0.7**|0.4 _±_ 0.5|**2.4** _±_ **0.1**|3.0 _±_ 0.4|
|4|Hybrid-MATCH|97.0 _±_ 1.5|**0.0** _±_ **0.0**|2.5 _±_ 0.2|2.7 _±_ 0.2|
||Hybrid-MATCH|||||
|5|(no-SSL)|82.0 _±_ 5.1|8.2 _±_ 3.8|2.4 _±_ 0.2|**1.7** _±_ **0.2**|
||Hybrid-Basic|||||
|6|(no-SSL)|87.0 _±_ 1.4|2.6 _±_ 1.9|2.6 _±_ 0.2|1.8 _±_ 0.2|


This loss is added to a standard policy gradient objective and is weighted by _βSSL_ . This ensures that there is always a gradient signal to use force control when in contact. 

## V. EXPERIMENTAL SETUP 

We test our approach in a tabletop fragile peg-in-hole (fPiH) setting with break force threshold _Fth_ =10 N, except where noted. In most of our experiments, the peg has a circular cross-section with a peg-hole clearance of _∼_ 0 _._ 5 mm, representing a realistic tolerance seen in industrial applications [18]. For all methods, we train asymmetric actor-critic policies [10], [18], [30] using PPO [31]. 

**Observation.** During training policies observe noisy estimates of relative position between end-effector and hole location, hole orientation, end-effector velocities and forces, and the previous action. The noise is normally distributed with a standard deviation of 1 N for force and 1 mm for hole pose observations. The critic receives noiseless variants of these as well as ground truth contact states and poses for the peg, hole and end-effector. This privileged information is not available to the policy. 

**Simulation.** We leverage the Factory simulation environment in IsaacSim using IsaacLab [27] to train control policies for a Franka FR3 (Franka Robotics) robot. End-effector force is estimated as the force acting on the wrist of the robot. The simulation physics and low-level controller update at 120 Hz to keep training computationally feasible. The policy acts at 15 Hz. For each episode, the end-effector is spawned approximately 5 cm above hole with Gaussian noise with standard deviations of 2 cm in xy and 1 cm in z. 

**Architecture and Training.** All methods are trained with PPO with data collection across 256 parallel environments. Policies are updated after 150 steps in each environment. Episodes terminate after 150 steps or on peg break. Policy and critic networks use the Simba architecture [32] with the policy having 2 residual blocks with latent size 256, and the critic using 3 residual blocks and latent size of 1024. We train 5 seeds in each condition for 3 million steps per seed and retain the policy checkpoint with highest training success rate in evaluation for each. For hybrid policies (Hybrid-Basic and MATCH), we introduced a initial bias to the selection term so the probability of position control is _∼_ 93% at network initialization. This was to match the 


Fig. 2. Learning Efficiency. Each method was trained for 3M steps using PPO. Success rate with 95% confidence intervals over 5 random seeds is shown. We see that MATCH, VICES and Pose converge at similar rates, while Hybrid-Basic requires more data. Further, we see ablations lacking selection supervision (no-SSL) learn slower than their counterparts. 

expected initial mode and stabilize training but was not found to have impact in practice. Both hybrid policies include the supervised selection loss during training. 

**Methods.** We compare pose-control (Pose), VICES [13] (VICES), and hybrid-control policies (Hybrid-Basic and MATCH). For Pose, the action space is a change in endeffector position and wrist rotation (yaw). Gains for the pose controller were selected to allow compliance with the environment, a common approach to ensure safety. VICES differs from Pose only in that the controller gains are also controlled by the policy. Both Hybrid-Basic and MATCH use hybrid action spaces (selection / pose / force) for position but we use only pose control for orientation due to unreliability of torque sensors. All methods share the same training conditions and model architecture. 

## VI. RESULTS 

To explore the effectiveness of RL-based hybrid control, we divide the analysis of our results into the following empirical questions, presenting claims and evidence for each. 

## _A. How effective are hybrid control policies?_ 

We evaluate success rate (peg reaches within 1 mm of the bottom of the hole), peg break rate, average time to success, and average force across 100 evaluation episodes for each method in Tab. I. Episodes are sampled according to the training distribution described above. Results are reported as mean and standard error across seeds. 

We find hybrid-control methods (rows 3 and 4) to increase success rate and lower break rate compared to Pose (row 1) and VICES (row 2). Notably, MATCH produced _zero_ peg breaks across all 500 trials (100 episodes _×_ 5 policy seeds) while maintaining a high success rate. Interestingly, hybrid methods also have higher average applied force. We speculate these higher-but-still-safe forces help maintain consistent contact with the top of the hole while aligning the peg. Behavior observed during sim-to-real trials (see Sec. VII). 

## _B. Does MATCH improve learning efficiency?_ 

Hybrid control introduces a more complex action space compared to Pose which, for a standard approach, is slower 


Fig. 3. Force control selection probability for MATCH. Each trajectory, across 500 evaluations, are segmented by phases, time normalized, and aggregated. MATCH learns a force selection policy that uses position while in free space, regulates force during contact, then returns to pose for insertion, consistent with common analytical approaches [5], [17], [19] 

to learn. In Fig. 2, we show success rate as a function of training iterations (steps) with mean and 95% confidence intervals over 5 seeds. We find our uninformed Hybrid-Basic formulation takes considerably longer to begin learning, likely due to uninformative gradients. In contrast, our MATCH formulation, which explicitly models the underlying hybrid controller, trains comparably to the simpler Pose method while retaining the benefits of hybrid control. 

## _C. What effect does the supervised selection loss have?_ 

We ablate the supervised selection loss (SSL) from both Hybrid-Basic and MATCH, finding it contributes substantially to learning efficiency and performance. Hybrid-Basic (no-SSL) converges to a success rate 11.2% lower and MATCH (no-SSL) 15% lower. The largest gap is MATCH to MATCH (no-SSL), likely because MATCH conditions the action distribution on the selection which makes it easier for early force failures to alter overall strategy. By introducing the SSL, we can compensate while encouraging safe behavior. We see a similar pattern in break rates, with Hybrid-Basic 2.2% and MATCH 8.2% better. 

Both ablations produce the lowest average forces. We also noted that during training, no-SSL policies made 3x less contact than hybrid methods (similar to Pose) and the force selection probability was less than 0.1%. Early in training, policies are primarily in free-space, where pose control is ideal. The policy is biased to pose control and stops exploring force control without SSL – demonstrating SSL usefulness for force control exploration throughout training. 

## _D. Does MATCH learn a meaningful selection policy?_ 

While our supervised selection loss (Sec. IV-C) encourages hybrid policies to select force while in contact, this is not a hard constraint on policy behavior. Policies can exhibit different strategies if detecting contact is too difficult or task reward is maximized in other ways. We describe the learned strategies for our hybrid MATCH policies in two ways. 

First, we analyze trajectory-level behavior in key task phases – approach, contact, and insertion. These are divided by first contact (approach _→_ contact) and when the peg is first centered and partially inserted (contact _→_ insertion). On average, these correspond to roughly 20%, 30%, and 50% 


Fig. 4. Success rate (top) and break rate (bottom) under uniform hole localization noise in observations. All methods were trained with normal noise ( _σ_ =1 mm), except Pose(2.5mm) which had _σ_ =2.5 mm. The figures show average success and break rates with 95% CI over 5 seeds. Notably hybrid methods have greater success rates and lower break rates. 

of the episode length respectively. Each evaluation trajectory is segmented into these phases then time normalized perphase before being aggregated. Fig. 3, shows the average probability of selecting force control across phases. 

We find MATCH learns a physically meaningful control strategy. During the approach phase, the robot is in free space, where force control may be dangerous, MATCH consistently predicts near 0 probability of force control. After contact, we see a spike in force control probability that is most pronounced in the z direction that persists until insertion and then declines. Meanwhile, xy control is largely posebased. This pattern suggests a hybrid control strategy that keeps the peg in firm contact with the top rim of the hole while searching for the correct alignment. During insertion, z-axis force control decreases as position control affords better regulation of the peg’s descent. This is similar to common manually-designed analytical approaches [5], [17], [19]. 

Second, we consider per-time-step correspondence between ground truth contact states and force selection. During evaluation, we find MATCH uses force control in 84 _±_ 10.8% of in-contact steps across all directions and only 2.9 _±_ 2.1% of free space steps. This suggests contact detection was learned effectively as part of the behavior policy. 

## _E. How robust are hybrid control policies to noise?_ 

In practical deployments, state estimation errors can lead to reduced performance or increase the risk of damaging work pieces. In Fig. 4, we deploy policies with increasing noise on hole location – adding uniform noise at scales of plus or minus 1mm, 2.5mm, 5mm, and 7.5mm. For context, the hole diameter is 8mm such that later conditions 


Fig. 5. Real robot results. Five simulation trained policies were evaluated with 30 noiseless trials and the highest success rate policy was kept. The policy was then evaluated on increasing noise conditions (50 trials per condition). Plots show success (left), average force (middle), and average energy use (right) with 95% CIs. MATCH substantially outperforms Pose, achieving performance comparable to VICES while exerting up to _∼_ 30% less force. 

represent significant error. Recall that policies were trained with Gaussian noise on hole position ( _σ_ =1mm). For these experiments each policy was evaluated across 500 episodes. 

In Fig. 4 (top), we see that while, all methods deteriorate with larger noise, pose is most affected, with a widening gap in success rate. At the most extreme, hybrid policies maintain near 40% success rates, outperforming pose by _∼_ 10%. We also find no significant difference between VICES and hybrid methods in either success or break rate. This suggests that force regulation improves robustness for in-contact manipulation. To examine whether higher noise training might improve Pose, we also report Pose(2.5mm) which was trained with a wider noise distribution. However, consistently training policies proved difficult in this setting with some policy seeds learning overly-conservative behaviors with poor performance. Uncertainty leading to poor local minima like this in fragile tasks has been reported in prior work as well [22]. 

Fig. 4 (bottom) shows the break rate across the same conditions. For all methods, break rate is fairly constant across noise levels, but the hybrid policies again show break rates less than half of pose control. Qualitatively, Pose policies exhibit a jerky search strategy that regularly makes and breaks contact. This more aggressive approach takes actions that are more likely to break the peg. In contrast, MATCH and Hybrid-Basic learned a search strategy that maintains a consistent force on the hole and then slides the peg tip around until reaching the hole. 

## _F. How are hybrid control policies on unconstrained tasks?_ 

Our results so far have been in a setting with a relatively strict 10 N break threshold where hybrid control policies may have a natural advantage. To study the impact of force constraints on Pose, VICES, and hybrid methods performance, we consider models trained and evaluated with unbreakable pegs. We repeat our hole localization noise experiments for this setting in Fig. 6. In this setting, both MATCH and VICES demonstrate significant robustness, with improved success rates of 17.1% and 21.1% better. This indicates that force regulation provides generally useful behaviors. 

## VII. SIM-TO-REAL EXPERIMENTS 

We evaluate sim-to-real deployment of our polices to a real Franka FR3 in laboratory conditions. 


Fig. 6. Success rate as hole localization noise increases with an unbreakable peg. For each method, 5 policies were trained with random seeds. During evaluation the observation of the hole location was noised with increasing magnitude, mean success rate and 95% CI are shown. Notably, MATCH and VICES perform best, demonstrating that even without force constraints force regulation has a positive effect under noisy observations. 

_Setup._ The peg and hole were 3D printed with approximately 0.5mm of clearance to mimic training conditions. Break threshold was set to 20 N and enforced by force estimates derived from joint torques. Force samples were taken at 1 kHz, and filtered with an exponential moving average ( _α_ = 0 _._ 08). Force control was implemented on filtered force estimates, assumed to be at the end-effector frame and estimated with joint torques. This setup is shown in Fig. 5. 

Five seeds of each policy were trained with additional dynamics randomization and noise, then deployed without fine-tuning. Dynamics randomization ranges were selected based on common practices [18], [27]. Real robot gains were tuned to maximize tracking performance, while staying as close as possible to the randomization ranges. For Pose and Hybrid-Basic we found it necessary to scale predicted standard deviations to 5% of the predicted values to achieve high performance. Each policy was evaluated across 30 trials with no hole position noise and the most successful seed for each method was then evaluated across 100 trials for each higher noise level. 

_Results._ Fig. 5 (left) shows the success rate of these best performing policies with increasing hole localization noise. All policies transfer well in low noise settings and then degrade as noise increases, similar to simulation results in Fig. 4. We find MATCH consistently outperforms Pose and Hybrid-Basic methods in success rate, with more 

substantial gaps as noise increases (e.g., an improvement of +35% over Pose in the 7.5mm setting). MATCH achieves similar success rates as VICES but applies up to _∼_ 30% reduced force on average as shown in Fig. 5 (middle). As in simulation, we find Pose frequently makes and breaks contact in a more chaotic search, resulting in the only break recorded in our trials (1 of 100 trials) and higher average force (Fig. 5 (middle)). In contrast, hybrid methods (Hybrid-Basic and MATCH) keep sustained contact while aligning the peg. While VICES has a similar average force as Pose, we find substantially higher max forces compared to all policies as shown in Fig. 5 (right). Taken together, these results suggest MATCH outperforms Pose control and is an effective alternative to VICES with the advantage of explicit force control allowing for finer interactions. 

## VIII. CONCLUSION 

In this work, we show the effectiveness of policies trained with hybrid position-force action spaces. In simulation, we show that hybrid policies are more robust and break the peg 5x less frequently than Pose. We then directly address the data inefficiency that comes with a more complex action space by introducing MATCH. MATCH is able to maintain all of the advantages of Hybrid-Basic while learning with the efficiency of Pose. We compare this to VICES and demonstrate it as a viable alternative as performance was identical in simulation. Finally, we evaluate sim-to-real policies with no additional training and show that MATCH substantially outperforms Pose, achieving performance comparable to VICES while exerting up to _∼_ 30% less force. 

## REFERENCES 

- [1] Y. Jiang, Z. Huang, B. Yang, and W. Yang, “A review of robotic assembly strategies for the full operation procedure: planning, execution and evaluation,” _Robotics and Computer-Integrated Manufacturing_ , vol. 78, p. 102366, Dec. 2022. 

- [2] F. Nauert and P. Kampmann, “Inspection and maintenance of industrial infrastructure with autonomous underwater robots,” _Frontiers in Robotics and AI_ , vol. 10, Aug. 2023. 

- [3] B. S. Peters, P. R. Armijo, C. Krause, S. A. Choudhury, and D. Oleynikov, “Review of emerging surgical robotic technology,” _Surgical Endoscopy_ , vol. 32, no. 4, pp. 1636–1655, Apr. 2018. 

- [4] M. H. Raibert and J. J. Craig, “Hybrid Position/Force Control of Manipulators,” _Journal of Dynamic Systems, Measurement, and Control_ , vol. 103, no. 2, pp. 126–133, June 1981. 

- [5] S. Chhatpar and M. Branicky, _Search strategies for peg-in-hole assemblies with position uncertainty_ , Feb. 2001, vol. 3, iEEE International Conference on Intelligent Robots and Systems. 

- [6] F. J. Abu-Dakka, B. Nemec, A. Kramberger, A. G. Buch, N. Kr¨uger, and A. Ude, “Solving peg-in-hole tasks by human demonstration and exception strategies,” _Industrial Robot: An International Journal_ , vol. 41, no. 6, pp. 575–584, Oct. 2014. 

- [7] J. Xu, Z. Hou, Z. Liu, and H. Qiao, “Compare Contact Model-based Control and Contact Model-free Learning: A Survey of Robotic Pegin-hole Assembly Strategies,” Apr. 2019, arXiv:1904.05240 [cs]. 

- [8] J. Kober and J. Peters, “Policy Search for Motor Primitives in Robotics,” in _Advances in Neural Information Processing Systems_ , vol. 21. Curran Associates, Inc., 2008. 

- [9] L. Yang, Z. Huang, F. Lei, Y. Zhong, Y. Yang, C. Fang, S. Wen, B. Zhou, and Z. Lin, “Policy Representation via Diffusion Probability Model for Reinforcement Learning,” May 2023, arXiv:2305.13122. 

- [10] M. Noseworthy, B. Tang, B. Wen, A. Handa, C. Kessens, N. Roy, D. Fox, F. Ramos, Y. Narang, and I. Akinola, “FORGE: Force-Guided Exploration for Robust Contact-Rich Manipulation under Uncertainty,” Jan. 2025, arXiv:2408.04587 [cs]. 

- [11] J. Luo, Z. Hu, C. Xu, Y. L. Tan, J. Berg, A. Sharma, S. Schaal, C. Finn, A. Gupta, and S. Levine, “SERL: A Software Suite for Sample-Efficient Robotic Reinforcement Learning,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , May 2024, pp. 16 961–16 969. 

- [12] J. Buchli, F. Stulp, E. Theodorou, and S. Schaal, “Learning variable impedance control,” _The International Journal of Robotics Research_ , vol. 30, no. 7, pp. 820–833, June 2011. 

- [13] R. Mart´ın-Mart´ın, M. A. Lee, R. Gardner, S. Savarese, J. Bohg, and A. Garg, “Variable impedance control in end-effector space: An action space for reinforcement learning in contact-rich tasks,” in _2019 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, 2019, pp. 1010–1017. 

- [14] C. C. Beltran-Hernandez, D. Petit, I. G. Ramirez-Alpizar, T. Nishi, S. Kikuchi, T. Matsubara, and K. Harada, “Learning Force Control for Contact-Rich Manipulation Tasks With Rigid Position-Controlled Robots,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 5709–5716, Oct. 2020. 

- [15] A. S. Anand, M. Hagen Myrestrand, and J. T. Gravdahl, “Evaluation of Variable Impedance- and Hybrid Force/MotionControllers for Learning Force Tracking Skills,” in _2022 IEEE/SICE International Symposium on System Integration (SII)_ , Jan. 2022, pp. 83–89. 

- [16] M. Neunert, A. Abdolmaleki, M. Wulfmeier, T. Lampe, T. Springenberg, R. Hafner, F. Romano, J. Buchli, N. Heess, and M. Riedmiller, “Continuous-Discrete Reinforcement Learning for Hybrid Control in Robotics,” in _Proceedings of the Conference on Robot Learning_ . PMLR, May 2020, pp. 735–751, iSSN: 2640-3498. 

- [17] H. Bruyninckx and J. De Schutter, “Specification of force-controlled actions in the ”task frame formalism”-a synthesis,” _IEEE Transactions on Robotics and Automation_ , vol. 12, no. 4, pp. 581–589, Aug. 1996. 

- [18] B. Tang, M. A. Lin, I. Akinola, A. Handa, G. S. Sukhatme, F. Ramos, D. Fox, and Y. Narang, “IndustReal: Transferring ContactRich Assembly Tasks from Simulation to Reality,” May 2023, arXiv:2305.17110 [cs]. 

- [19] H. Kang, Y. Zang, X. Wang, and Y. Chen, “Uncertainty-Driven Spiral Trajectory for Robotic Peg-in-Hole Assembly,” _IEEE Robotics and Automation Letters_ , vol. 7, no. 3, pp. 6661–6668, July 2022. 

- [20] R. Diaz, A. Imdieke, V. Veeriah, and K. Desingh, “AugInsert: Learning Robust Visual-Force Policies via Data Augmentation for Object Assembly Tasks,” in _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , Oct. 2025, pp. 18 504–18 511. 

- [21] J. Luo, O. Sushkov, R. Pevceviciute, W. Lian, C. Su, M. Vecerik, N. Ye, S. Schaal, and J. Scholz, “Robust Multi-Modal Policies for Industrial Assembly via Reinforcement Learning and Demonstrations: A Large-Scale Study,” July 2021, arXiv:2103.11512 [cs]. 

- [22] S. H. Huang, M. Zambelli, J. Kay, M. F. Martins, Y. Tassa, P. M. Pilarski, and R. Hadsell, “Learning Gentle Object Manipulation with Curiosity-Driven Deep Reinforcement Learning,” Mar. 2019, arXiv:1903.08542 [cs]. 

- [23] M. A. Lee, Y. Zhu, K. Srinivasan, P. Shah, S. Savarese, L. Fei-Fei, A. Garg, and J. Bohg, “Making Sense of Vision and Touch: SelfSupervised Learning of Multimodal Representations for Contact-Rich Tasks,” in _2019 International Conference on Robotics and Automation (ICRA)_ , May 2019, pp. 8943–8950, iSSN: 2577-087X. 

- [24] X. Zhang, C. Wang, L. Sun, Z. Wu, X. Zhu, and M. Tomizuka, “Efficient Sim-to-real Transfer of Contact-Rich Manipulation Skills with Online Admittance Residual Learning,” in _Proceedings of The 7th Conference on Robot Learning_ , Dec. 2023, pp. 1621–1639. 

- [25] M. Suomalainen, Y. Karayiannidis, and V. Kyrki, “A survey of robot manipulation in contact,” _Robotics and Autonomous Systems_ , vol. 156, p. 104224, Oct. 2022. 

- [26] R. S. Sutton and A. G. Barto, _Reinforcement Learning: An Introduction_ , 2nd ed., ser. Adaptive Computation and Machine Learning Series. Cambridge, Massachusetts: The MIT Press, 2018. 

- [27] Y. Narang, K. Storey, I. Akinola, M. Macklin, P. Reist, L. Wawrzyniak, Y. Guo, A. Moravanszky, G. State, M. Lu, A. Handa, and D. Fox, “Factory: Fast Contact for Robotic Assembly,” May 2022, arXiv:2205.03532 [cs]. 

- [28] B. Siciliano, O. Khatib, and T. Kr¨oger, _Springer handbook of robotics_ . Springer, 2008, vol. 200. 

- [29] C. J. Bester, S. D. James, and G. D. Konidaris, “Multi-Pass Q- Networks for Deep Reinforcement Learning with Parameterised Action Spaces,” May 2019, arXiv:1905.04388 [cs]. 

- [30] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel, 

   - “Asymmetric Actor Critic for Image-Based Robot Learning,” Oct. 2017, arXiv:1710.06542 [cs]. 

- [31] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal Policy Optimization Algorithms,” Aug. 2017, arXiv:1707.06347 [cs]. 

- [32] H. Lee, D. Hwang, D. Kim, H. Kim, J. J. Tai, K. Subramanian, P. R. Wurman, J. Choo, P. Stone, and T. Seno, “Simba: Simplicity bias for scaling up parameters in deep reinforcement learning,” in _International Conference on Learning Representations (ICLR)_ , 2025. 

