---
title: "MARCH: Model-Assisted Reinforcement Learning for the Perceptive Control of Humanoids over Sparse Footholds"
date: "2026-06-09"
authors: "Codrin Crismariu; Ryan K. Cosner"
url: https://arxiv.org/abs/2606.10288
pdf: https://arxiv.org/pdf/2606.10288
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.10288)** / [論文ページ](https://arxiv.org/abs/2606.10288)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **MARCH:** **<u>Model-Assisted Reinforcement Learning for the</u> Perceptive** **<u>Control of Humanoids over Sparse Footholds</u>** 

**Codrin Crismariu and Ryan K. Cosner** 

Department of Mechanical Engineering Tufts University, Medford, MA, United States `codrin.crismariu@tufts.edu, ryan.cosner@tufts.edu` 


Figure 1: Unitree G1 humanoid traversing sparse footholds with a vision-based, model-assisted reinforcement learning (RL) control policy. **(Left)** Physical experiment snapshots; **(Right)** depth images for control-policy feedback. Experiment video: youtube.com/watch?v=pXjy-zPCRPA. 

**Abstract:** Perceptive bipedal locomotion over sparse terrain remains a difficult challenge: model-based methods are precise but brittle to uncertainty, while model-free methods are robust but struggle to discover the precise, constrained motions required for precise locomotion where small errors can cause catastrophic failures. We propose a model-assisted reinforcement learning (RL) framework that combines both perspectives in three steps: (1) generate a reference trajectory using simplified models; (2) train a privileged teacher policy with Lyapunovguided heuristic reward shaping around that reference; and (3) distill the teacher into a vision-based student policy. We show that this model-assistance procedure produces physically grounded locomotion, improving sample efficiency, reducing the need for a complex learning curriculum, and achieving smoother locomotion behavior alongside stepping stone performance comparable to a model-free baseline. We validate our approach in simulation and demonstrate a deployment on a Unitree G1 humanoid robot navigating sparse footholds with lateral constraints. 

**Keywords:** Reinforcement learning for physical robot control, Model-based and model-free learning for robotic control, Bipedal locomotion 

## **1 Introduction** 

The promise of bipedal robotics is to _enable robots to go wherever humans can go_ . However, while current methods have successfully created robust locomotion policies that enable walking on nominal terrain, they struggle to generalize to scenarios like sparse footholds with lateral constraints. Developing policies to navigate these environments currently demands complex training curricula and sampling-intensive training. 

Existing methods for achieving safe locomotion over sparse terrain range from model-based to model-free. Traditional model-based methods typically rely on _a priori_ known system dynamics models and known environment maps [1, 2, 3]. The assumptions of a known dynamics model and safe foot placement map allow them to generate rigorous safety guarantees, but these assumptions struggle to generalize to real-world deployment and new scenarios, especially when the robot must rely on high dimensional visual measurements to identify sparse footholds. Model-free approaches 

10th Conference on Robot Learning (CoRL 2026), Austin, Texas, USA. 

typically involve either (1) developing a map from sensor feedback and learning a locomotion policy that enables safe traversal over that map [4, 5] or (2) directly learning a locomotion policy that incorporates visual information as an input [6]. Recent work explored a middle ground between model-based and data-driven methods by using models to guide reinforcement learning (RL) in the form of control Lyapunov function RL (CLF-RL) where an approximate model is used in a CLF reward function [7]. CLF-RL shows promise in improving performance and RL sample efficiency, with demonstrations on safe locomotion involving forward foothold constraints [8], but has yet to be demonstrated in scenarios with lateral foothold constraints; this work provides that extension. 

To achieve vision-based locomotion over sparse footholds with lateral constraints, we extend [8] by incorporating a receding-horizon safe footstep planner and adding a transformer and mixture density network (MDN) [9] to the locomotion policy in order to plan multiple steps, increase the utility of the proprioception measurements, and allow the policy to select between modes representing different foot placements. An overview of this framework can be seen in Figure 2. 

The core contributions of this work are: (1) a model-assisted RL framework that extends [8] to incorporate lateral foot placement requirements by introducing a receding horizon planner, a transformer, and an MDN output, (2) simulation comparisons to model-free methods that demonstrate our method’s improved sample efficiency and smooth locomotion with an ablation study showing the utility of our policy architecture, and (3) an experimental demonstration of our framework on a Unitree G1 humanoid robot walking over terrain with variable gaps and stepping stone placement, demonstrating locomotion over sparse terrain with lateral constraints on hardware. 

## **2 Related Work** 

Model-based methods have tackled the problem of locomotion over sparse footholds and provided rigorous guarantees of safety using hybrid system models. Notably, [10] presented a control barrier function (CBF [11])-based safe foot placement method for a planar biped which was later extended to a three dimensional biped in [1], with both works limited to simulation. Later hardware deployment of these methods [2] required data-driven model refinements, removing their theoretical guarantees. Similar model-based methods for quadrupedal robots leverage state-constrained model predictive control (MPC) to achieve safe foot placement when the environment height map is known [3] and when it is constructed from perception data [12]. Generally, model-based methods for safe locomotion over sparse footholds enable rigorous theoretical guarantees, but rely on conservative modeling and perception assumptions that are difficult to satisfy on hardware. 

Meanwhile, model-free, learning-based methods have enabled robust locomotion over nominal terrains [13]. While prior work shows the efficacy of RL for quadrupedal locomotion over a diverse set of terrains [14, 15, 16], similar deployment for humanoids presents a more difficult problem due to the increased instability of bipeds. Recent solutions for humanoids either avoid perception and rely on commanded foot placement [17], incorporate perception information by constructing maps [18], or operate directly on perception measurements [19, 13, 20]. The complexity of these learning problems generally limit their results to obstacles that can be overcome with general flat-terrain robustness or obstacles that do not impose a lateral constraint (e.g., stairs) and have prevented these methods from being deployed on stepping stones that are placed far apart where a poorly-placed step might result in catastrophic behavior. Only recent results have been able to achieve this behavior, but require large amounts of compute and highly structured curricula to find a viable solution in the poorly-conditioned reward landscape [6]. 

To improve the computational efficiency of this RL problem, [7] proposed the CLF-RL method that incorporates a model-guided reward function based on control Lyapunov functions (CLFs) [21] into a traditional RL framework. This method uses model-based reference trajectories to guide policy learning by rewarding policies that produce motions similar to a safe model-based reference trajectory. CLF-RL alongside teacher-student distillation [16] has been shown to improve computational efficiency in learning complex behaviors like running [22] and forward-constrained locomotion over sparse footholds in [8]. Similarly, [23] incorporates a model-based gait library which is used to guide RL to develop more general locomotion policies. Despite the success of these model-assisted results, 

they have yet to be applied to a stepping stone problem involving lateral constraints. This paper uses Lyapunov-guided heuristic reward shaping to learn walking on sparse footholds that induce both forward and lateral constraints. 

## **3 Preliminaries** 

Next, we introduce our various system models and student-teacher reinforcement learning paradigm. 

### **3.1 System Models** 

**General Walking as a Hybrid System:** We model general bipedal walking as a hybrid system that incorporates both continuous motion and the discrete changes resulting from the impacts. We denote this system as Σ = ( _D, U , G,_ ∆ _,_ **f** _,_ **g** ) where _D_ is the set of continuous domains, _U ⊂_ R<sup>_nu_</sup> is the control input space, _G ⊂D_ represents the guards corresponding to impact events, ∆: _G →D_ defines the discrete reset map, and **f** and **g** define the continuous dynamics of the system. We denote the state as **x** ≜ [ **q**<sup>_⊤_</sup> _,_ **q** ˙<sup>_⊤_</sup> ]<sup>_⊤_</sup> _∈T Q_ where **q** is the generalized system coordinate and the system input as **u** _∈U_ . In general, we assume that we do not have access to these precise dynamics: 


**Discrete-Time Single Integrator:** While the hybrid system (1) describes the general motion of the bipedal robot, its complexity makes it difficult to use for planning foot placement over sparse terrain. Alternatively, we consider a simplified discrete-time single integrator model of the stance foot location, **p** f _∈_ R<sup>2</sup> : **p** f _,k_ +1 = **p** f _,k_ + **_ℓ_** _k_ , where **_ℓ_** _k_ is the change in stance foot location that occurs between steps. This dramatically simplified model cannot be used directly for control and overlooks important system complexity, but its simplicity enables rapid planning and constraint checking to ensure that the planned stance foot locations are safe ( **p** f _,k ∈L_ step feas.) and that the planned step length is feasible ( **_ℓ_** _k ∈L_ step bound). 

**Hybrid Linear Inverted Pendulum Model [24]:** To capture the hybrid, underactuated nature of walking and characterize the swing phase motion, we model the bipedal robot as a hybrid linear inverted pendulum (HLIP) with discrete transitions at each impact [24]. This model simplifies the hybrid dynamics in (1) by assuming that the system has point-feet, massless legs, no ankle torque, a constant center of mass (CoM) _z_ -height, and all mass concentrated at the CoM, resulting in an underactuated system where the horizontal CoM position relative to the stance foot, [ _rx, ry_ ], cannot be directly regulated and must instead be controlled via the step-to-step dynamics. This HLIP model is linear and characterizes both the discrete step-to-step motion and continuous flow of the CoM between steps which can be decoupled into two orthogonal planes (i.e., _x_ and _y_ ). 

To describe the HLIP model, let **_ξ_** _x_ = [ _rx, vx_ ]<sup>_⊤_</sup> be the state vector where _vx ∈_ R is _x_ -direction CoM velocity. The continuous dynamics of the HLIP model are: 


where _g_ is gravitational acceleration, _z_ 0 is the _z_ -height of the CoM, _τ_ is the time within the current swing phase, and _T_ is the step period. The reset map accounts for the step length _ℓx_ , resulting in: 


We then identically define **_ξ_** _y_ for the CoM in the _y_ -direction and use this model to plan, predict, and control CoM motion in the ( _x, y_ ) plane. 


Figure 2: **Framework Overview** . Our framework involves three core components: **(red)** generation of model-based safe reference trajectories, **(blue)** training of a privileged teacher control policy that uses control Lyapunov function (CLF)-inspired rewards in a CLF-RL [7] framework, and **(green)** distillation of the teacher policy into a student policy that only relies on the visual and proprioceptive data accessible during hardware deployment. 

### **3.2 Reinforcement Learning and Teacher-Student Distillation** 

We formulate the task of sparse foothold traversal as a partially observable Markov decision process (POMDP), defined by the tuple _M_ = ( _S, A, O, T , Z, R, γ_ ) where _S_ is the set of states, _A_ is the set of actions, _O_ is the set of observations, _T_ ( **s**<sup>_′_</sup> _|_ **s** _,_ **a** ) is the state transition probability of moving from state **s** to state **s**<sup>_′_</sup> by taking action **a** , _Z_ ( **o** _|_ **s** ) is the probability of observing **o** given that the system is at state **s** , _R_ ( **s** _,_ **a** ) is the instantaneous reward function, and _γ ∈_ [0 _,_ 1] is the discount factor. The agent seeks to maximize the expected discounted cumulative reward: 


where **_π_** _T,θ_ ( **a** _k|_ **o** _k,_ **o**<sup>priv.</sup> _k_ ) is the stochastic policy parameterized by _θ_ and the expectation is taken over trajectories generated by this policy. We optimize the parameters _θ_ to maximize _J_ ( **_π_** _T,θ_ ) using proximal policy optimization (PPO) [25]. 

To improve learning under partial observability, we leverage a teacher-student framework. The teacher policy **_π_** _T,θ_ ( **a** _k|_ **o** _k,_ **o**<sup>priv.</sup> _k_ ) is given access to privileged observation information **o**<sup>priv.</sup> _k_ while the student policy **_π_** _S,ϕ_ ( **a** _k|_ **o** _k_ ) has limited sensing information. Once the teacher policy is trained, the student policy is trained to match the teacher under the supervised distillation loss: 


where **a** _T,k ∼_ **_π_** _T,θ_ ( _·|_ **o** _k,_ **o**<sup>priv.</sup> _k_ ) is the action sampled from the teacher distribution. 

## **4 Methodology** 

Building on the models and student-teacher RL framework in Section 3, our approach develops a control policy via a three-step process which can be seen in Figure 2. First, we develop a modelbased reference trajectory to identify a region of local optimality for teacher policy. Next, we leverage privileged information in simulation to train a teacher policy using Lyapunov-based reward shaping as in [7, 8]. Finally, we distill this teacher policy into a student that operates exclusively on visual feedback and proprioception to enable deployment on hardware. 

### **4.1 Reference Generation** 

Here we introduce the methodologies used to generate the safe model-based reference trajectories that are used to guide the RL reward. Overall, the reference trajectories include the outputs: 


where ( **p** f _,_ **v** f) is the swing foot position and velocity, ( **p** com _,_ **v** com) is the CoM position and velocity, ( **_ε_** pelv _,_ **_ε_** ˙ pelv) are the pelvis orientation and derivatives, ( **_ε_** foot _,_ **_ε_** ˙ foot) are the swing foot orientation and derivatives, and ( **q** upper _,_ **q** ˙ upper) are the joint positions for the robot’s upper body. The time argument, _t_ , is suppressed for each value on the right-hand side for brevity. 

**Swing Foot Position Reference,** ( **pf** _,_ **vf** ) **:** We first plan safe two-dimensional foot placements and step timing based on a single integrator system in order to safely track a desired velocity, **v** _D_ . Specifically, this plan attempts to solve the finite, discrete-time optimal control problem: 


where the cost _c_ edge( _·_ ) penalizes the system for stepping near an edge, the first constraint enforces single integrator dynamics, the second constraint determines the average velocity needed to complete the step, the third constraint enforces foot placement in the safe region _L_ step feas., the fourth constraint enforces the step length bound _L_ step bound, and the final constraint assigns the initial condition. 

The edge costs and stepping-stone constraints are highly non-convex making this problem difficult to solve analytically. However, over a short horizon ( _N_ = 4 steps in our case), a solution can be quickly approximated via random shooting (with 16 greedy rollouts) over discretized time and safe foot placements. Once we have generated a foot-placement and step-timing plan, we construct Bezier curves defining the desired three-dimensional trajectory for the swing foot. 

**CoM Reference,** ( **pcom** _,_ **vcom** ) **:** After generating a reference trajectory for the swing foot, we create a reference trajectory for the CoM based on the HLIP model in (3) and the step length and period found by the planner (7). We interpolate between the pre-impact CoM states using the continuous portion of the HLIP dynamics (2), **_ξ_** ( _τ_ ). 

**Pelvis Orientation Reference,** ( **_ε_ pelv** _,_ **_ε_** ˙ **pelv** ) **:** The yaw reference trajectory includes small heuristic oscillations at the step frequency in roll and pitch, and tracks the commanded yaw rate, **_ω_** _D_ . 

**Swing Foot Orientation Reference,** ( **_ε_ foot** _,_ **_ε_** ˙ **foot** ) **:** The swing foot orientation reference trajectory is chosen to keep the base of the swing foot parallel with the ground to enable flat-foot stepping while aligning the swing foot’s yaw with the pelvis. 

**Upper Body Reference,** ( **qupper** _,_ **q** ˙ **upper** ) **:** The upper body reference trajectory maintains nominal relative positions and orientations with respect to the CoM. 

### **4.2 Reward Shaping and Training the Teacher Policy** 

Next, we train the teacher policy using PPO [25] with a model-guided CLF-RL reward [7]. 

**Teacher Architecture and Observations:** The teacher’s actor and critic are both multi-layer perceptrons (MLPs). The teacher has access to a 5-step history of proprioception data and has privileged access to the reference trajectory (6) giving it indirect access to ground-truth safe foot placement. 

**Reward Shaping:** In simulation, we collect trajectory information to find the error **_η_** ( _t_ ) = **y** sim( _t_ ) _−_ **y** ref( _t_ ) which represents the difference between the true values in simulation, **y** sim( _t_ ), and the reference values that the system is tracking, **y** ref( _t_ ). To incentivize convergence to this reference trajectory, we follow the CLF-RL paradigm [7] and construct rewards inspired by control Lyapunov functions (CLFs) [21]. To do this, we define the Lyapunov-like function _V_ ( **_η_** ) ≜ 2<sup><u>1</u></sup><sup>**_η_**</sup><sup>_⊤_</sup><sup>**P**</sup><sup>**_η_**, where</sup><sup>**P**</sup> is a positive definite matrix that solves the continuous time algebraic Riccati equation [26], assuming, as in [8], that **_η_** has second-order feedback-linearizable dynamics. 

**Remark 4.1.** _While it is unlikely that V is a true control Lyapunov function or that the assumption of feedback linearizability holds, this function V can still be used to identify useful local minima in_ 

_training. Appendix 9.3 provides the conditions for which V is a valid CLF for the single-support swing phase of a fully-actuated bipedal robot._ 

Prior work implemented the CLF constraint,<sup>_<u>dV</u>_</sup> _dt_<sup>(</sup><sup>**_η_**)</sup><sup>_≤−cV_(</sup><sup>**_η_**), as part of state-feedback controller</sup> to ensure that **_η_** converges exponentially [27]. However, the reliance of these methods on their assumed model introduced fragility to model uncertainty and disturbances [28]. To overcome this, the CLF-RL paradigm instead uses _V_ ( **_η_** ) to shape the RL reward function (4) by adding two CLFinspired rewards to the standard locomotion rewards discussed in Sec. 5: 


These reward small _V_ ( **_η_** ) values (i.e., accurate reference tracking) and decreasing _V_ ( **_η_** ) values (i.e., convergence to the reference) respectively, with the normalization parameters _V_ max _, V_ dmax _>_ 0. 

### **4.3 Distillation of the Student Policy** 

Finally, we distill a student policy, **_π_** _S,ϕ_ , by minimizing the negative log likelihood loss (5). 

**Student Observations:** The student policy receives a 5-step history of the proprioception data and the desired velocity command as well as the current image from a body-mounted depth camera. The student does not have access to the reference trajectory and is only reliant on measurements that the robot has access to during hardware deployment. 

**Student Architecture:** To process the observations, the student policy has the form of a convolutional neural network (CNN) to process the depth image, a transformer that fuses the CNN embeddings and proprioception history data, and finally a mixture density network (MDN) that outputs a bi-modal action distribution. The use of the CNN and transformer was inspired by [6], while the MDN output was added to enable the student policy to disambiguate and choose between different stepping modes (e.g., one foothold instead of another or stepping with the left or right foot). 

**Remark 4.2.** _The function V is a control Lyapunov function only under the conditions stated in Appendix 9.3 for a fully actuated, flat-footed single-support phase. Our reference-guided rewards are heuristic for the full walking task: the single-support result does not cover impacts, contact changes, or the complete hybrid locomotion cycle. The finite-difference estimate of V_<sup>˙</sup> _also introduces noise into the reward, in addition to the Monte Carlo estimation noise in PPO. Thus, the reward construction does not establish a stability or safety guarantee for the learned policy._ 

## **5 Training Setup** 

Next we provide important information regarding our training setup. Please see the appendix for additional information regarding compute, hyperparameters and domain randomization distributions. 

**Teacher Training:** The teacher policy operates with privileged access to the reference commands, **y** ref, which are recomputed at every new step contact. The reference commands and true system states, **y** sim( _t_ ), are used to construct _V_ ( **_η_** ) as in (8) from a pre-computed positive definite matrix **P** . The derivative<sup>_<u>dV</u>_</sup> _dt_<sup>(</sup><sup>**_η_**</sup><sup>_,_</sup><sup>**a**) is approximated using three-point backward difference during training.</sup> These are used to evaluate the Lyapunov-guided heuristic rewards (8) which are added to the general RL rewards (4). 

The other rewards include holonomic stance-foot rewards penalizing displacement and velocity of the stance foot from its contact location, torque minimization reward, joint limits reward, and action smoothness. The holonomic stance-foot reward is included to incentivize the learned policy to satisfy the underlying assumptions of the HLIP model. The termination conditions are: timeout, fall over (i.e., _>_ 50<sup>_◦_</sup> tilt), pelvis too low, foot height too low, and MPC infeasibility. The domain randomization parameters can be found in Table 4 in the Appendix. 

The teacher is trained on a procedurally generated terrain consisting of two end platforms connected by a sequence of stepping stones, as seen in Fig. 3. A curriculum is designed where stone dimen- 


Figure 3: **Simulation Environment. (Left)** Unitree G1 in `mjlab` : the model-based planner uses the true height map (red/yellow) for a safe foothold plan (yellow arrows); the white camera view near the torso is used for student training. **(Right)** Fixed teacher **_π_** _T,θ_ , 1000 student-training episodes: ours **_π_** _S,ϕ_ (green) consistently outperforms transformer (blue) and MDN (orange) ablations. Training uses distillation loss; student rollouts are evaluated with the full teacher training reward _R_ ( **s** _k,_ **a** _k_ ). 

sions, gaps, and height variations vary with increasing difficulty. Additionally, random side-by-side stone pairs are also generated to create left/right foot-placement decisions. 

**Student Distillation:** After training the teacher policy, we distill it into the student policy that no longer has access to privileged reference trajectories or ground-truth height map information and instead only has access to a body-mounted depth camera that is facing forwards and down. The student policy input consists of both this 32 _×_ 24 pixel depth image and a 5-step history of proprioception data. Our student policy is trained using the distillation loss (5) specific to the MDN output. The depth observations used to train the student policy are corrupted with noise, pixel dropout, and a delay to approximate real sensor values. 

## **6 Experimental Results** 

We evaluate our model-assisted reinforcement learning framework through simulation validation trials on the Unitree G1 humanoid robot. When compared to standard model-free approaches exemplified by [6]<sup>1</sup> , our evaluation demonstrates that model guidance improves both sample efficiency in training and locomotion smoothness at deployment. The distilled student policy succeeded in 66 _._ 70% of 1024 trials on a randomized four-stone corridor. 

### **6.1 Simulations** 

**Ablation Study:** We first perform an ablation study to test the utility of the transformer network and the MDN output. Specifically, we compare our method against two ablations: one with the transformer replaced with an MLP and another with the MDN replaced with an MLP trained to perform regression (so that the output is deterministic). We use a fixed teacher policy, **_π_** _T,θ_ to train each student. The models with MDN layers are trained using a negative log-likelihood loss as in (5) and the model with the deterministic MLP output is trained with a Huber loss as in [8]. The results are presented in Fig. 3 and show that the transformer and MDN both improve student performance as represented by their ability to generate reward after distillation. 

**Reference-reward ablation:** We compare the Lyapunov-guided heuristic reward with quadratic reference tracking (“Quadratic”) and no reference tracking (“No Ref.”). Across 1024 episodes per policy, our method travels farther and survives longer. Quadratic tracking has lower pelvis motion variance, but terminates after approximately one third of the distance traveled by our method. No Ref. has no privileged foothold information because that information is contained in the reference. 

**MDN multi-modality:** In simulation, we swept the initial CoM lateral offset across 321 values spanning _±_ 0 _._ 3 m and recorded foot touchdown locations. The policy deterministically selects the highest-probability component of its two-component MDN. Fig. 4 shows the resulting spatially distinct touchdown modes. 

> 1We are unable to perform a direct comparison with [6] since no code has been published. The included results are our best approximation of their method according to the details in the preprint. 

|||Table1.A||T|able 1.B|
|---|---|---|---|---|---|
||Our method|Quadratic|No Ref.|Our method|Single integrator only|
|**(a)**<br>|**3****_._43****_±_ 0****_._04**<br>|1_._02_±_0_._01<br>|0_._747_±_0_._003<br>|**3****_._43****_±_ 0****_._04**<br>|0_._933_±_0_._013<br>|
|**(b)**<br>|**6****_._88****_±_ 0****_._07**<br>|2_._79_±_0_._03<br>|1_._50_±_0_._01<br>|**6****_._88****_±_ 0****_._07**<br>|1_._992_±_0_._022<br>|
|**(c)**<br>|**1****_._40****_±_ 0****_._07**<br>|1_._94_±_0_._03|6_._20_±_0_._07|**1****_._40****_±_ 0****_._07**|1_._819_±_0_._026<br>|
|**(d)**|**0****_._440****_±_ 0****_._022**|0_._460_±_0_._010|2_._125_±_0_._030|0_._440_±_0_._022|**0****_._409****_±_ 0****_._011**|
|**(e)**|0_._341_±_0_._008|**0****_._296****_±_ 0****_._005**|2_._914_±_0_._026|0_._341_±_0_._008|**0****_._281****_±_ 0****_._004**|
|**(f)**|0_._173_±_0_._005|**0****_._102****_±_ 0****_._002**<br>|1_._437_±_0_._019|0_._173_±_0_._005|**0****_._048****_±_ 0****_._001**<br>|
|**(g)**|0_._243_±_0_._006|**0****_._182****_±_ 0****_._009**|0_._384_±_0_._008|0_._243_±_0_._006|**0****_._060****_±_ 0****_._004**|


Table 1: **A (Left)** Three policies, 1024 episodes/policy; means _±_ 1 SEM, all episodes terminated. **(a,b)** Distance [m] and time [s] before termination; **(c)** contact-force variance [10<sup>4</sup> _×_ N<sup>2</sup> ]; **(d)** meansquared contact-force rate [10<sup>8</sup> _×_ N<sup>2</sup> _/_ s<sup>2</sup> ]; **(e–g)** pelvis roll/pitch/yaw variance [10<sup>_−_2</sup> _×_ rad<sup>2</sup> ]. **B (Right)** Single-integrator ablation (ours: single-integrator + HLIP reference). Means _±_ 1 SEM; **(a)** forward displacement [m], **(b)** time to episode end [s]; **(c–g)** Table 1 metrics/units. **Best in bold.** 

||_N_ = 1|_N_ = 2|_N_ = 3|_N_ = 4|_N_ = 8|
|---|---|---|---|---|---|
|**(a)**|3_._153_±_0_._066|3_._256_±_0_._071|**3****_._575****_±_ 0****_._082**<br>|3_._388_±_0_._082|2_._698_±_0_._056|
|**(b)**|7_._057_±_0_._138|7_._200_±_0_._134|**7****_._990****_±_ 0****_._165**|7_._935_±_0_._178<br>|6_._611_±_0_._109|
|**(c)**|1_._609_±_0_._038|1_._506_±_0_._027|1_._459_±_0_._031|**1****_._386****_±_ 0****_._029**<br>|1_._489_±_0_._027|
|**(d)**|0_._450_±_0_._010|0_._429_±_0_._008|0_._412_±_0_._009<br>|**0****_._387****_±_ 0****_._008**|0_._409_±_0_._007|
|**(e)**|0_._349_±_0_._007|0_._353_±_0_._007|**0****_._302****_±_ 0****_._006**|0_._317_±_0_._006|0_._352_±_0_._006<br>|
|**(f)**|0_._267_±_0_._015|0_._192_±_0_._007|0_._189_±_0_._007<br>|0_._165_±_0_._007|**0****_._160****_±_ 0****_._006**|
|**(g)**|0_._435_±_0_._018|0_._359_±_0_._019|**0****_._324****_±_ 0****_._010**|0_._328_±_0_._012|0_._427_±_0_._019|


Table 2: Planning-horizon ablation. Means _±_ 1 SEM, rounded to three decimals; metrics and units as in Table 1. **Best mean in bold.** 


Figure 4: **(Left)** Stepping-stone/initial CoM conditions (red); blue/yellow touchdowns identify the dominant mixture component (argmax for a median 75% of each step). Conditioned on successful touchdown, components dominate 69%/31% of the runs, respectively. **(Center/Right)** Forward/lateral touchdown location versus CoM offset for each mode. 

**Baseline Comparison:** We compare our method to a model-free PPO baseline similar to [6], sharing our teacher-student distillation framework and privileged environmental information but omitting Lyapunov-guided heuristic rewards. Both reach similar mean distances over stepping stones, but our teacher converges in 10,000 episodes versus 20,000 for the baseline. The method in [6] also used a more structured curriculum from flat ground to stepping stones. On one RTX 5090, teacher training and student distillation each took 12 GPU hours (24 GPU hours total) for both our method and the model-free comparison. Reference-trajectory computation raises per-episode cost, making total wall-clock training time comparable despite improved sample efficiency; caching references or reducing height-map density could reduce this primary overhead. Across 2048 rollouts of distilled student policies, our method achieves at least 12% lower mean absolute joint torque and 39% lower mean absolute angular jerk after 500 distillation iterations (Fig. 5), yielding smoother locomotion (video: youtube.com/watch?v=pXjy-zPCRPA). 

### **6.2 Hardware Experiments** 

While our primary results are in simulation, we additionally provide a single proof-of-concept hardware demonstration; we do not claim a success rate for these hardware experiments. On hardware, we iterated deployment until achieving a successful crossing and did not run a fixed- _N_ success-rate protocol. The experimental setup consists of a starting platform, an ending platform, and a sequence of 4 stepping stones arranged in a pseudo-random, alternating left-and-right configuration. This 


Figure 5: Smoothness comparisons: our model-informed method (blue) reduces or matches variances and has contact-force spectral power more concentrated at lower frequencies than the modelfree baseline (red); shown to 20 Hz. **(a)–(h)** : 64 episodes/checkpoint, logged at 50 Hz; **(a)–(g)** : _±_ 1 SEM error bars; **(h)** : dotted mean. Other _x_ -axes show distillation training iterations. Teachers: 10,000 model-informed/20,000 model-free episodes. **(i)–(k)** : 2048 rollouts/iteration; **(i)** : 20-episode moving average, slightly faster model-free convergence and similar final mean distances. 

layout forces the robot to tightly control both its forward and lateral foot placements. The stepping stones are all the same height and covered with a rigid wood board to replicate the flat contact surfaces used in simulation. The distilled student policy runs entirely on the Unitree G1’s Jetson Orin Nx onboard computer and utilizes a chest-mounted Intel Realsense D435i for depth image measurements. The full vision-proprioception pipeline, including the CNN feature extractor and transformer, executes at approximately 50Hz, matching the control loop frequency in simulation. 

## **7 Limitations** 

Firstly, our approach is limited by the sensory modes of the system. The camera is pointed forwards and down, preventing the ability to learn safe backwards or sideways locomotion. The angle of the camera also limits the ability of the robot to achieve highly dynamic, long-horizon maneuvers that might require planning motions over several ( _>_ 4) steps. Future work will involve actively directing the camera to enable these behaviors. Additionally, the HLIP model does not include a flight phase which means that our reference trajectories could not include jumping. Future work will develop and incorporate alternative reduced-order models to enable this behavior. Furthermore, while the proposed method improved sampling efficiency, the overall training time was similar. Future work will involve improving per-sample computational efficiency. Finally, while the policy achieved a successful demonstration on hardware, the proof-of-concept physical deployment was significantly less repeatable than simulation; we attribute this to camera latency and accuracy and seek to achieve improved robustness in the future. 

## **8 Conclusion** 

We propose a model-guided reinforcement learning framework to enable vision-based sparse foothold navigation with lateral constraints for a bipedal robot. Our three-step method involves first using simplified dynamics models (discrete-time single integrator and HLIP) to plan a reference trajectory, then using this reference trajectory to guide the training of a privileged teacher control policy, and finally distilling that teacher policy into a vision-based student. We deploy this method on hardware and show that this model-guided learning framework demonstrates improved sample efficiency and yields smoother locomotion compared to model-free alternatives. 

## **References** 

- [1] Q. Nguyen, A. Hereid, J. W. Grizzle, A. D. Ames, and K. Sreenath. 3d dynamic walking on stepping stones with control barrier functions. In _2016 IEEE 55th Conference on Decision and Control (CDC)_ , pages 827–834. IEEE, 2016. 

- [2] N. Csomay-Shanklin, R. K. Cosner, M. Dai, A. J. Taylor, and A. D. Ames. Episodic learning for safe bipedal locomotion with control barrier functions and projection-to-state safety. In _Proceedings of the 3rd Conference on Learning for Dynamics and Control_ , volume 144 of _Proceedings of Machine Learning Research_ , pages 1041–1053. PMLR, 07 – 08 June 2021. URL `https://proceedings.mlr.press/v144/csomay-shanklin21a.html` . 

- [3] R. Grandia, A. J. Taylor, A. D. Ames, and M. Hutter. Multi-layered safety for legged robots via control barrier functions and model predictive control. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8352–8358. IEEE, 2021. 

- [4] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning robust perceptive locomotion for quadrupedal robots in the wild. _Science Robotics_ , 7(62), 2022. 

- [5] Q. Ben, B. Xu, K. Li, F. Jia, W. Zhang, J. Wang, J. Wang, D. Lin, and J. Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains, 2025. URL `https://arxiv.org/abs/2511.14625` . 

- [6] Y. Zhang, Y. Seo, J. Chen, Y. Yuan, K. Sreenath, P. Abbeel, C. Sferrazza, K. Liu, R. Duan, and G. Shi. Rpl: Learning robust humanoid perceptive locomotion on challenging terrains. _arXiv preprint arXiv:2602.03002_ , 2026. 

- [7] K. Li, Z. Olkin, Y. Yue, and A. D. Ames. Clf-rl: Control lyapunov function guided reinforcement learning. _IEEE Robotics and Automation Letters_ , 11(3):3230–3237, 2026. doi: 10.1109/LRA.2026.3653329. 

- [8] M. Dai, W. D. Compton, J. Li, L. Yang, and A. D. Ames. Walk the planc: Physics-guided rl for agile humanoid locomotion on constrained footholds. _arXiv preprint arXiv:2601.06286_ , 2026. 

- [9] C. M. Bishop. Mixture density networks. Copyright © 1994, Christopher M. Bishop. This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (https://creativecommons.org/licenses/by-nc-nd/4.0/)., 1994. URL `https://publications.aston.ac.uk/id/eprint/373/` . 

- [10] Q. Nguyen and K. Sreenath. Safety-critical control for dynamical bipedal walking with precise footstep placement. _IFAC-PapersOnLine_ , 48(27):147–154, 2015. ISSN 2405-8963. doi:https: //doi.org/10.1016/j.ifacol.2015.11.167. Analysis and Design of Hybrid Systems ADHS. 

- [11] A. D. Ames, S. Coogan, M. Egerstedt, G. Notomista, K. Sreenath, and P. Tabuada. Control barrier functions: theory and applications. In _2019 18th European Control Conference (ECC)_ , pages 3420–3431, 2019. doi:10.23919/ECC.2019.8796030. 

- [12] R. Grandia, F. Jenelten, S. Yang, F. Farshidian, and M. Hutter. Perceptive locomotion through nonlinear model-predictive control. _IEEE Transactions on Robotics_ , 39(5):3402–3421, 2023. 

- [13] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. In P. Agrawal, O. Kroemer, and W. Burgard, editors, _Proceedings of The 8th Conference on Robot Learning_ , volume 270 of _Proceedings of Machine Learning Research_ , pages 1975–1991. PMLR, 06–09 Nov 2025. URL `https://proceedings.mlr.press/v270/zhuang25a.html` . 

- [14] X. Cheng, K. Shi, A. Agarwal, and D. Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450, 2024. doi:10.1109/ICRA57147.2024.10610200. 

- [15] A. Agarwal, A. Kumar, J. Malik, and D. Pathak. Legged locomotion in challenging terrains using egocentric vision. In _Conference on robot learning_ , pages 403–415. PMLR, 2023. 

- [16] J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter. Learning quadrupedal locomotion over challenging terrain. _Science Robotics_ , 5(47), 2020. 

- [17] H. Duan, A. Malik, J. Dao, A. Saxena, K. Green, J. Siekmann, A. Fern, and J. Hurst. Sim-toreal learning of footstep-constrained bipedal dynamic walking. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 10428–10434. IEEE, 2022. 

- [18] J. Sun, G. Han, P. Sun, W. Zhao, J. Cao, J. Wang, Y. Guo, and Q. Zhang. Dpl: Depthonly perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction, 2025. URL `https://arxiv.org/abs/2510.07152` . 

- [19] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu. Learning perceptive humanoid locomotion over challenging terrain. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 6571–6578, 2025. doi:10.1109/IROS60139.2025. 11247685. 

- [20] S. Zhu, Z. Zhuang, M. Zhao, K.-Y. Lee, and H. Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids, 2026. URL `https://arxiv.org/abs/2601.07718` . 

- [21] Z. Artstein. Stabilization with relaxed controls. _Nonlinear Analysis: Theory, Methods & Applications_ , 7(11):1163–1173, 1983. 

- [22] Z. Olkin, W. D. Compton, R. M. Bena, and A. D. Ames. Chasing autonomy: Dynamic retargeting and control guided rl for performant and controllable humanoid running, 2026. URL `https://arxiv.org/abs/2603.25902` . 

- [23] N. Janwani, V. Madabushi, and M. Tucker. Navigait: Navigating dynamically feasible gait libraries using deep reinforcement learning, 2026. URL `https://arxiv.org/abs/2510. 11542` . 

- [24] X. Xiong and A. Ames. 3-d underactuated bipedal walking via h-lip based gait synthesis and stepping stabilization. _IEEE Transactions on Robotics_ , 38(4):2405–2425, 2022. doi: 10.1109/TRO.2022.3150219. 

- [25] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [26] K. J. Astr¨om and R. Murray.<sup>˚</sup> _Feedback systems: An introduction for scientists and engineers_ . Princeton University Press, 2021. 

- [27] A. D. Ames, K. Galloway, K. Sreenath, and J. W. Grizzle. Rapidly exponentially stabilizing control lyapunov functions and hybrid zero dynamics. _IEEE Transactions on Automatic Control_ , 59(4):876–891, 2014. 

- [28] E. D. Sontag and Y. Wang. On characterizations of the input-to-state stability property. _Systems & Control Letters_ , 24(5):351–359, 1995. 

- [29] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel. mjlab: A lightweight framework for gpu-accelerated robot learning, 2026. URL `https://arxiv.org/abs/2601. 22074` . 

- [30] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 5026– 5033, 2012. doi:10.1109/IROS.2012.6386109. 

- [31] C. Schwarke, M. Mittal, N. Rudin, D. Hoeller, and M. Hutter. Rsl-rl: A learning library for robotics research, 2025. URL `https://arxiv.org/abs/2509.10771` . 

## **9 Appendix** 

### **9.1 Artificial Intelligence Acknowledgement** 

The authors acknowledge the use of artificial intelligence (AI) technologies in the preparation of this paper. Specifically, large language models were utilized for the following purposes: 

- **Code Generation:** AI tools assisted in writing the software, including the simulation setup, training scripts, plot generators, and experimental evaluation. 

- **Writing Assistance:** AI was used as a supportive tool to improve the clarity, grammar, and phrasing of the text during the writing and editing process. 

All AI-generated outputs were thoroughly reviewed, verified, and edited by the authors, who take full responsibility for the contents of this paper. 

### **9.2 Experimental Parameters and Reproducibility** 

To ensure reproducibility, this section provides comprehensive details regarding the simulation parameters, RL hyperparameters, and hardware configurations utilized across our pipeline. Specifically, Table 3 summarizes the simulation framework, the scale of our parallelized environment setup, and the specific hardware infrastructure used to execute the training. Table 4 outlines the complete suite of domain randomization ranges applied during the training process. These perturbations include rigid-body variations, sensor noise models, and push forces designed to bridge the sim-to-real gap. These are the same as in [6]. Finally, Table 5 provides the exact training hyperparameters used for both components of our learning pipeline: the reinforcement learning teacher policy (trained via PPO) and the subsequent vision-based student policy (distilled from the teacher policy). 

|**Configuration / Metric**|**Details & Infrastructure Specifications**|
|---|---|
|**Simulation Environment**|`mjlab` framework [29] via MuJoCo simulation environment<br>[30]|
|**Learning Library**|GPU-accelerated`rsl-rl`library [31]|
|**Parallelization**|4,096 parallelized simulated environments|
|**Hardware Infrastructure**|Single NVIDIA RTX 5090 GPU|
|**Pipeline Training Time**|24 GPU hours on an RTX 5090: 12 hours for teacher training<br>and 12 hours for student distillation|


Table 3: Simulation environment, training efficiency, and computational infrastructure details. 

### **9.3 Conditions for a Control Lyapunov Function** 

Consider the dynamics of the single-support phase for a bipedal robot as given in [7]: 

**D** ( **q** )¨ _q_ + **H** ( **q** _,_ **q** ˙ ) = **Bu** + **J** _h_ ( **q** )<sup>_⊤_</sup> **F** (9) 

**J** _h_ ( **q** )¨ _q_ + **J**<sup>˙</sup> _h_ ( **q** _,_ **q** ˙ ) ˙ **q** = 0 (10) 

where **D** ( **q** ) : _Q →_ R<sup>_nq×nq_</sup> is the mass-intertia matrix, **H** : _Q × T Q →_ R<sup>_nq_</sup> contains the Coriolis and gravity terms, and **B** _∈_ R<sup>_nq,nu_</sup> is the actuation matrix. The Jacobian of the holonomic contact constraint is **J** _h_ ( _q_ ) _∈_ R<sup>_h×nq_</sup> and the associated constraint wrench is **F** _∈_ R<sup>_h_</sup> 

**Proposition 9.1** ([7, Prop. 1]) **.** _Consider a fully actuated humanoid in flat-footed single support whose dynamics satisfy_ (9) _, the holonomic contact constraint_ (10) _, and friction-cone constraints. If the CARE uses_ **Q** _≻_ 0 _and the virtual-constraint Jacobian ∂y/∂q is invertible, then V_ ( **_η_** ) = **_η_**<sup>_⊤_</sup> **P** **_η_** _, with_ **P** _≻_ 0 _given by the CARE for the feedback-linearized error dynamics, is a control Lyapunov function for the full nonlinear dynamics during single support._ 

This conditional result applies to the continuous, flat-footed single-support phase. It does not establish Lyapunov decrease across impacts or other contact changes, nor a guarantee for the complete hybrid walking motion used here. 

|**Parameter**|**Value**|
|---|---|
|Friction Coefficients|_U_(0_._5_,_1_._25)|
|Link Mass|_U_(0_._9_,_1_._2)_×_default mass|
|Base Additional Mass|_U_(_−_1_._0_,_3_._0)kg|
|Encoder Bias|_U_(_−_0_._015_,_0_._015)rad|
|Base CoM Offset|∆_x ∼U_(_−_0_._025_,_0_._025)m|
||∆_y ∼U_(_−_0_._05_,_0_._05)m<br>∆_z ∼U_(_−_0_._05_,_0_._05)m|
|Motor Effort Limits|_U_(0_._85_,_1_._1)_×_default|
|Joint Damping|_U_(0_._75_,_1_._25)_×_default|
|Joint Friction|_U_(0_._0_,_0_._04)|
|Push Perturbation:|_x ∼U_(_−_1_,_1) <sup>m</sup><br>s|
|random velocity<br>added every 10-15s|_y ∼U_(_−_1_,_1) <sup>m</sup><br>s<br>(_ϕ, θ, ψ_)_∼U_<sup>3</sup>(_−_0_._4_,_0_._4) <sup>rad</sup><br>sec|
|Control Delay|_U_(0_,_20)ms|
|Depth Camera Translation|_x ∼U_(_−_0_._025_,_0_._025)m|
||_y ∼U_(_−_0_._025_,_0_._025)m|
||_z ∼U_(_−_0_._025_,_0_._025)m|
|Depth Camera Rotation (Euler)|_ϕ ∼U_(_−_2_._5_,_2_._5)<sup>_◦_</sup>|
||_θ ∼U_(_−_3_._0_,_3_._0)<sup>_◦_</sup><br>_ψ ∼U_(_−_2_._5_,_2_._5)<sup>_◦_</sup>|
|Depth Camera FOV|∆FOV_∼U_(_−_2_._0_,_2_._0)<sup>_◦_</sup>|
|Pixel Dropout|5%|
|Depth Noise|_σd_ = 0_._1_·_depth|


Table 4: Domain Randomization. The values were chosen to align with the values in [6]. 

|**Lyapunov-guided teacher PPO**|**MDN Distillation**|
|---|---|
|**Network:** MLP actor-critic, (512_,_256_,_128) hid-|**Student**<br>**network:**<br>CNN–Transformer–MDN,|
|den units, ELU activation|ELU activation|
|**Observation normalization:** enabled|**Teacher network:** Lyapunov-guided PPO policy|
|**Actor initial std:** 1_._0<br>|**Observation normalization:** enabled|
|**Learning rate:** 5_×_10<sup>_−_5</sup>|**MDN modes:** 2<br>|
|**LR schedule:** adaptive|**Minimum std:** 10<sup>_−_3</sup><br>|
|**PPO epochs:** 5<br>|**Log-std range:** [_−_3_,_2]<br>|
|**Mini-batches:** 4|**Inference mode:** `top`<br>~~`m`~~`ode`<br>~~`m`~~`ean`|
|**Clip parameter:** 0_._2|**Optimizer:** Adam<br>|
|**Value loss coefficient:** 1_._0|**Learning rate:** 5_×_10<sup>_−_4</sup>|
|**Entropy coefficient:** 0_._008|**Distillation epochs:** 10|
|**Discount factor:** _γ_ = 0_._99|**Gradient length:** 2|
|**GAE parameter:** _λ_= 0_._95|**Teacher samples:** 8|
|**Target KL:**0_._01|**Teacher std scale:** 0_._1|
|**Max gradient norm:** 1_._0|**Max gradient norm:** 2_._0|
|**Rollout length:** 24steps/env|**Rollout length:** 120steps/env|
|**Training iterations:** 10000|**Training iterations:** 1500|


Table 5: Training hyperparameters for the Lyapunov-guided PPO teacher and the MDN distillation student. 

