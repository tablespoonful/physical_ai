---
title: "TaskNPoint: How to Teach Your Humanoid to Hit a Backhand in Minutes"
date: "2026-06-24"
authors: "Blake Werner; Ilona Demler; Pietro Perona; Aaron D. Ames"
url: https://arxiv.org/abs/2606.26215
pdf: https://arxiv.org/pdf/2606.26215
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.26215)** / [論文ページ](https://arxiv.org/abs/2606.26215)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **TaskNPoint: How to Teach Your Humanoid to Hit a Backhand in Minutes** 

**Blake Werner Ilona Demler Pietro Perona Aaron D. Ames** California Institute of Technology _{_ `bwerner, idemler, perona, ames` _}_ `@caltech.edu` 


Figure 1: **TaskNPoint** is a training protocol that teaches humanoid robots dynamic skills from a single human video demonstration per motion. We have a human “coach” specify the discrete skills and critical interaction window, from which we generate goals _G_ . Reinforcement learning in simulation with randomized targets lets a single demonstration generalize zero-shot to new target locations, trainable in under an hour on one GPU. 

**Abstract:** How do we learn to hit a tennis backhand? Not from a thousand hours of tennis tournaments on TV — we _work with a coach_ and _practice_ . We argue this is also the right recipe for teaching dynamic skills to humanoid robots. This follows from a structural property of dynamic skills: the outcome is decided by a short, crucial portion of the trajectory — for a backhand, the _∼_ 20cm of racket travel around ball contact. Getting this _interaction window_ right requires coordinating the whole motion, so that control, physics, and morphology act in concert. Learning thus reduces to mastering a handful of distinct actions and, for each, practicing until the window comes out right. To this end, we introduce TaskNPoint, a training protocol which makes the coach-learner division of labor explicit. The human coach contributes four inputs: a discrete set of skills (e.g. different shots), one demonstration per skill, identification of the interaction window, and the goal. Learning in a physically realistic simulation environment fills in each action trajectory and provides robustness to unmodeled events. Crucially, randomized target sampling during training lets a single demonstration generalize zero-shot to unseen goal locations. We test this approach on a Unitree G1 humanoid that hits forehands and backhands against balls thrown by a human, kicks incoming soccer balls, and picks and places boxes from novel locations. We find that learning is successful from short human video demonstrations and under an hour of training on a single GPU, with no per-task reward tuning. 

```
https://ilonadem.github.io/tasknpoint_website/
```

**Keywords:** Reinforcement Learning for Physical Robot Control, Humanoids 

## **1 Introduction** 

Suppose you want to learn to play tennis. Probably you will not watch a thousand professionals before you step on the court. Rather, you will work with a coach who will start by defining a shot, e.g. the backhand, demonstrate the motion once or twice, point out what matters (the moment the racket meets the ball), name the goal (get it over the net and inside the lines) and send you to practice. Over the next few sessions you will learn additional shots, each anchored by explanations and a demonstration, and refined through your own practice against varied incoming balls. This is how humans learn sports. We argue that this is also a general strategy to teach humanoid robots dynamic loco-manipulation skills. 

Dynamic sports skills have a peculiar structure that makes this kind of learning possible. Although a forehand involves coordinated motion of the entire body, its outcome is determined solely by the position and motion of the racket during contact, or about 20 cm of the racket’s trajectory: the _interaction window_ . In other words, get the racket head moving in the right direction, at the right speed and time, and the ball will go where you want it. The rest of the swing (the backswing, the footwork, the follow-through) serves the purpose of getting the interaction window right, and is shaped by the morphology of the body and the physics of running, standing, swinging, and balancing under gravity. The same is true for kicking a ball, throwing a javelin, or swinging a bat. 

This observation suggests a natural division of labor between teacher and learner. The teacher contributes expert knowledge: (1) the discrete set of skills that constitute the sport (forehand, backhand, serve, volley, overhead, footwork), (2) a demonstration of each, (3) identification, for each skill, of the interaction window: the short bit of trajectory that determines success (in striking sports, like tennis, this is the moment of contact, in throwing sports, like bocce, it is the moment of release), and (4) a specification of the goal — for tennis, placing the ball at a chosen location in the opponent’s court, though in this paper we adopt the beginner’s goal of racket-ball interaction quality. The learner, via practice in a physics-accurate simulation environment, supplies everything else: filling in the rest of the trajectory, generalizing the skill to a continuum of possible target points and velocities, and acquiring robustness to perturbation through systematic variation of the ball’s incoming trajectory. We call this the TaskNPoint paradigm. 

We test our paradigm by training dynamic humanoid motions from a handful of monocular videos of tennis, soccer, and box pick-and-place. We find that from one demonstration per skill (a few seconds of video), we can train a Unitree G1 humanoid to hit tennis forehands and backhands, kick soccer balls toward targets, and pick up boxes in new locations. This takes less than an hour on one GPU. Training in simulation achieves sufficient precision and robustness to enable successful hardware deployment with no per-task reward tuning. 

## **2 Related Work** 

Table 1: **Comparison to existing methods.** TaskNPoint is a general framework for training dynamic humanoid motions. Despite being multi-task and trained on dynamic environments, it is faster and more data efficient to learn than competing approaches: for each task it requires just 1 demonstration with seconds of data, and has a simple single-stage training setup that takes less than 1 GPU hour to train to deployable performance. For GPU training hours, we assume convergence in 30,000 iterations of RL training at 1 second per iteration, the standard in [1], for each policy in the pipeline. 

||Dynamic<br>Environment|Training Stages|GPU Training<br>Hours|Multi-Task?|Train demos per<br>task|Imitation Data<br>(min) per task|
|---|---|---|---|---|---|---|
|**VideoMimic [2]**|✗|4|33|✓|17.6|20.5|
|**HDMI [3]**|✗|1|8|✗|1.0|1.0|
|**OmniRetarget [4]**|✗|1|8|✗|1.0|0.1|
|**LATENT [5]**|✓|3|25|✗|_>_200.0|300.0|
|**HITTER [6]**|✓|1|8|✗|2.0|0.3|
|**HumanX [7]**|✓|3|_>_50|✓|1.0|500.0|
|**TaskNPoint (Ours)**|✓|1|1|✓|1.0|0.5|


2 


Figure 2: **TaskNPoint Overview.** From a small collection of videos of human demonstrations (one video per task), we provide a pipeline for learning a repertoire of goal-conditioned motions interacting with dynamic environments. We first reconstruct the human motions using SMPLX parameters (section 4), which we then kinematically retarget to the humanoid (section 4). A higher level planner conditions action selection on goal, then a policy trained to both imitate the action and accomplish the goal (section 5) performs the task conditioned on the simple abstraction, allowing for robust performance during deployment (section 7). 

**Humanoid Loco-manipulation** The humanoid form makes human demonstrations a natural prior for loco-manipulation, and the field has utilized this fact in several ways. RL for motion tracking, pioneered by works such as [8, 9], show excellent results at tracking specific trajectories robustly [10, 3, 4], however generalization outside of the imitation data proves to be difficult. Addressing this problem has largely been approached in two different ways. The first optimizes a reward through massive simulations [1, 11, 12, 13, 14, 15], while the second uses general whole-body controllers that track arbitrary trajectories [7, 16, 10, 17, 18, 19] and relies on a higher-level trajectory generator. The first is much more data efficient, using minimal numbers of human demonstrations, but often results in behaviors that are unnatural and inefficient, due to the bias of tuned rewards. The second bypasses reward engineering thanks to learning from massive human motion datasets. This scale is becoming more achievable thanks to improvements in video reconstruction [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 2] and imitation. However, these methods often require expensive ad-hoc data cleaning to ensure high-enough quality for effective training [31, 32, 33, 34, 35]. Our method differs from both of these approaches in two ways. First, we use a principled approach to human reconstruction using MLE estimates from multiple views, which removes the need for reward-engineering or task-specific fixes to imperfect reconstructions. Second, by formulating dynamic tasks as goals conditioned on points in 3D space and time, we are able to train on a small set of these demonstrations and achieve motion coverage over a 3D volume around a player. 

**Sport-playing Humanoids** Sport-playing humanoids [36, 37, 38, 39, 40, 41, 42, 6] demonstrate impressive behaviors, but these policies are often tuned to their sport, and some sidestep wholebody coordination by decoupling upper and lower body [6]. Neither matches the data efficiency of a human learner: a tennis student does not invent ”forehand” from raw experience [43, 44], because coaches have spent centuries cataloging the skills of the game and what matters about each. In TaskNPoint we propose a new paradigm for understanding dynamic tasks as spatio-temporal goals, and use this paradigm to avoid priors induced by task-specific reward tuning. In doing so, we 

3 

simplify the learning problem by considering the sport divided into clear, discrete actions that can be trained efficiently in parallel simulation, and results in multi-skill policies that train in under an hour on a single GPU. 

## **3 Task Definition** 

**Intuition.** Consider what a tennis player must do when returning an incoming ball. First, they must decide which shot to play. Is it a forehand, a backhand, a smash, or a volley? This is a discrete choice with a finite vocabulary of actions. Second, once the shot is chosen, they must shape the shot depending on the incoming ball’s speed, spin, and trajectory, and on the desired ball destination. Shaping the shot includes the footwork to reach a good position, and the preparation and followthrough that produce the desired impact quality. This is a choice within a continuum of possibilities. 

We therefore arrive at a natural hierarchy of discrete action selection and continuous action shaping needed to execute the task. The policies for shot selection and for shot shaping need to be specified – we will use RL for shot shaping (section 5) and a simple hand-made policy for shot selection (section 6) . While we use tennis as a running example, the paradigm is quite general. This decomposition similarly applies to many robot loco-manipulation tasks, including those that require multiple sequential targets. Besides tennis, we experiment with ball kicking and box pick-and-place to validate this point. 

Regarding the action (the _shot_ , in tennis), we need to distinguish between four different and interrelated entities: the control, the trajectory, the interaction, and the goal. There is a causal connection between them: the _control_ will make the robot move and describe a _trajectory_ — a time sequence _qt_ =0: _T_ , where _q_ indicates the degrees of freedom of the robot — defining both the kinematics and the dynamics of the robot during the action. The position and velocity of the end-effector at the time of _interaction_ determine the outcome which, hopefully, meets the _goal_ . E.g. in tennis the position and velocity of the racket when it impacts the ball (the interaction) determine the trajectory of the ball, and eventually the placement of the ball into the opponent’s court (the goal). Thus, the goal _G_ is a function of the interaction _J_ , which is a function of the action’s trajectory _A_ , which is a function of the control signal. To select the best control, the one that best places the ball, we must invert this chain. Thus, learning must produce a map, or policy, that computes the control from the goal. Or, in a more structured approach, three concatenated maps: from goal to interaction, from interaction to trajectory, and from trajectory to control. 

In this paper we simplify this rather complex picture for the sake of studying the overall TaskNPoint framework. First, we do not learn the map from control to trajectory since this may be obtained analytically using classical control theory, and is available as a primitive through the humanoid’s standard software. Second, like beginners in tennis, we adopt the quality of the impact as the goal, rather than having ball placement as the goal and inverting a target landing location into the impact parameters (which is left for future work). Since we identify _G_ := _J_ , only one map, _G → A_ , needs to be learned. 

**Formalization.** Given a reference action trajectory _A_ := _qt_ =0: _T_ , where _q_ is the vector indicating the degrees of freedom of the robot, the teacher identifies the crucial moment in the demonstration sequence, i.e. the time where the racket impacts the ball in tennis, the foot kicks the ball in soccer, and the hand grabs the box in box pickup. For a tennis shot the racket-ball interaction is parametrized by the time _t_<sup>_∗_</sup> _∈_ R, the 3D location _p_<sup>_∗_</sup> _∈_ R<sup>3</sup> , the velocity direction _ν_<sup>_∗_</sup> _∈_ R<sup>3</sup> and orientation _n_<sup>_∗_</sup> _∈_ S<sup>2</sup> of the racket at impact. Thus, the parameterization of the interaction in the reference demonstration is _G_<sup>_∗_</sup> := ( _p_<sup>_∗_</sup> _, ν_<sup>_∗_</sup> _, n_<sup>_∗_</sup> _, t_<sup>_∗_</sup> ) (similar parameterizations for other tasks). In this paper, this is denoted the _goal_ . The rest of the robot’s trajectory will be determined taking into account the kinematics and dynamics of the robot, as well as other terms in the loss function, such as torque minimization. 

The teacher provides one, or at most few, demonstrations, which are sufficient to provide a qualitative idea of the trajectory of the shot. It is, however, not sufficient to learn how the interaction (racket-to-ball impact) can achieve a multitude of different impact types (the goal here) and deal with a multitude of incoming ball trajectories. To train a policy that is robust to uncertainty on where the 

4 


Figure 3: **Video Demonstrations.** We collect single-view (left) and multi-view (right) demonstrations and reconstruct human poses using state-of-the-art reconstruction methods (section 4). For the multi-view demonstrations, we fuse per-view estimates into a maximum-likelihood pose estimate. 

racket will meet the ball (both are traveling at high speed, thus such uncertainty is unavoidable), we generate goals Gtrain = _{_ ( _p, ν, n, t_ ) _}_ , where the impact variables are randomized: _p ∼N_ ( _p_<sup>_∗_</sup> _,_ Σ), and similarly for _ν_ and _n_ . To average over noisy sensor measurements we average position, velocity direction, and orientation rewards in training over the interaction window, i.e. a small time-window around impact: Ω= _t_<sup>_∗_</sup> + ( _−δt, δt_ ). The set of all actions _A_ and goals _G_<sup>_∗_</sup> constitute a library of motions A, which we use to train our policy. 

In the remainder of this paper we will discuss how we can apply this dynamic task abstraction as shown in fig. 2. We first extract goals G from human demonstrations (section 4) which we then use to train a humanoid policy (section 5). We then define a simple motion-selection optimization for task space coverage and deploy our policy on hardware (section 6). Finally, we discuss our results and compare TaskNPoint to current state-of-the-art methods (section 7). 

## **4 Motion Acquisition** 

In this section we outline our method for producing a repertoire of reference motions from a small set of videos of human demonstrations (fig. 3). 

**Motion Reconstruction** We start by collecting monocular videos of human demonstrations and extracting human pose estimates using state-of-the-art off-the-shelf monocular human pose estimation and SfM methods (Appendix B.1). We recover 3D human pose estimates with PromptHMR [27], producing per-frame pose estimates of 3D SMPL-X [45] parameters: _H_ = _{_ ( _dt, ϕt, βt, θt_ ) _}_<sup>_T_</sup> _t_ =0<sup>,</sup> with translation _dt ∈_ R<sup>3</sup> , body pose _θt ∈_ R<sup>21</sup><sup>_×_3</sup> , orientation _ϕt ∈_ R<sup>3</sup> , and shape _βt ∈_ R<sup>10</sup> . To counter known failure modes such as foot skating and translation drift [46], for in-the-wild videos we use multiple concurrent views of tennis practices from [47] and form a maximum-likelihood consensus pose by fusing per-view pose estimates. Each per-camera joint estimate _Jc_<sup>(</sup><sup>_i_)</sup> is modeled as a Gaussian observation of the true joint position, with covariance Σ<sup>(</sup> _c_<sup>_i_), elongated along that</sup> camera’s depth axis to take into account monocular depth ambiguity. We lift camera-coordinate estimates into a shared world-coordinate frame _Jc → Jw_ , Σ _c →_ Σ _w_ defined relative to the court geometry (as outlined in Appendix B). To fuse multiple estimates into a consensus we compute the maximum-likelihood estimate of the joint positions: 


We provide the full derivation of the MLE pose in Appendix B. 

**Kinematic Retargeting** We next retarget human motion trajectories to the robot’s morphology and identify the goal _G_<sup>_∗_</sup> = _{_ ( _p, ν_<sup>_∗_</sup> _, n_<sup>_∗_</sup> _, t_<sup>_∗_</sup> ) _}_ that will serve as the nominal goal of the motion. First, we kinematically retarget the human motion trajectory with GMR [48] to translate the trajectory of the 

5 


Figure 4: **Policy Architecture. (Top):** We reconstruct reference single-view or multi-view human demonstrations via SMPL-X parameters (section 4). For multi-view video, we lift reconstructions into a shared coordinate space and calculate a maximum likelihood pose. **(Middle):** In training we use Asymmetric Actor Critic Policy Optimization [49] to optimize motions _Ai_ from our motion library A, from which we sample randomized goals _G_ (section 5). **(Bottom):** In deployment, policy observations are computed by a trajectory estimator and fed to the motion selection algorithm which takes care of selecting the action type, goal, and phase (section 6). 

body of the human coach demonstrating a shot, e.g. a tennis backhand, to the closest motion that the robot can execute. A crucial aspect of retargeting is identifying the moment where the interaction happens. Upon identifying the timestamp _t_<sup>_∗_</sup> of interaction, we set the position of the end effector (e.g. the hand of the tennis player) at _t_<sup>_∗_</sup> as _p_<sup>_∗_</sup> , and set the link’s velocity direction and orientation as _ν_<sup>_∗_</sup> and _n_<sup>_∗_</sup> . During training the target points _p_ will be randomized around the nominal target _p_<sup>_∗_</sup> with covariance Σ = diag( _σx, σy, σz_ ) to cover the 3D volume of possible target locations around the humanoid with sufficiently fine sampling. We denote the set of all retargeted demonstrations as an action library A. 

## **5 Policy Learning** 

Equipped with our action library A, we next learn a policy that computes a trajectory as a function of a chosen goal (fig. 4) and is robust to novel target locations and trajectories at test-time (fig. 5) . 

**Training** We use Proximal Policy Optimization [49] to train our policy in the MJlab simulator. Please refer to Appendix C for more details on our formulation and hyperparameters. 

**Observations** Our policy is conditioned on both proprioceptive and chosen goal. The proprioceptive inputs include a history of the robot’s joint positions, joint velocities, angular velocity, projected 

6 


Figure 5: **Training Rewards.** TaskNPoint learns a policy given a nominal target point and motion reference from a human demonstration (section 4). Motions and contact points are randomly sampled throughout training (section 5); position, velocity, and orientation rewards are assigned during the duration of contact. Segments in each motion tubule are color-coded by reward value. 

gravity vector, and previous action, whose history length we set to 1 sample. In addition, the policy receives the chosen goal; target positions and orientations are passed in the robot’s local (anchor) frame and target velocities are passed in the world frame, along with the reference trajectory of the chosen action _Ai_ ( _t_ ) = _{qt}i_ . Finally, the critic receives additional privileged observations: robot center of mass position and velocity as well as each of the robot links’ positions and orientations, which are detailed in Appendix C.1. 

**Actions** Our actor outputs position setpoints for each joint to be tracked by PD controllers as introduced by [12] and explored further by [50]. Details, including gains, are given in section C.2. 

**Rewards.** The robot needs to learn to accomplish the goal, and we regularize the solution by imposing that it also imitates the reference motion. Thus, the reward has two main components: trajectory tracking and goal achievement. The tracking component of the reward is taken from [9] including positions, orientations, and velocities of robot key points, penalties for self collisions and reaching joint limits, and regularization on action rate. For position and velocity achievement we use 


and for orientation, 


where _⟨·, ·⟩_ indicates the standard Euclidean inner product. By decreasing _σ{p,ν,n}_ we get a tighter position reward around the goal position if we want stricter adherence to the goal requirement. This allows us to match specific orientation axes, and generalizes to exact orientation matching by using two of these constraints to uniquely define an orientation in _SO_ (3). Notably, our approach does not require any additional reward tuning, besides optionally scaling achievement rewards according to the size of the contact window Ω; see Appendix C.5 for more details. 

**Action Goals.** Our framework accommodates weighted sampling to prioritize motions that are more complex and thus more difficult to learn — we currently sample all motion classes equally. Action selection relies on assigning heuristic difficulty weights to each motion, which proportionally dictate the exact distribution of motions in a finite pool. Sampling from this pool without replacement during training yields a deterministic motion count, thereby stabilizing the training process. Conditioned on the motion choice _i_ , we sample _pi ∼N_ ( _p_<sup>_∗_</sup> _i_<sup>_,_Σ)</sup><sup>_,_and sample</sup><sup>_νi_and</sup><sup>_ni_analogously.</sup> Each motion primitive induces a confidence region 


7 

**Algorithm 1** Action Selection and Goal/Timing Estimation (section 6). 


where _rδ_<sup>2is chosen such that</sup> 


where _δ_ = 0 _._ 26. We implicitly ablate this parameter in Appendix C.5 when we ablate _σ{x,y,z}_ and find our method is robust to even large variations in the coverage parameter. We choose the motion primitives so that these regions cover the workspace, _W ⊆_<sup>�</sup><sup>_K_</sup> _i_ =1<sup>_Ci_(</sup><sup>_δ_)</sup><sup>_,_asillustratedin</sup> fig. 6. Orientations and velocities are sampled similarly with their own desired workspaces. 

**Curriculum** We use reference state initialization similar to [10] to preferentially select more difficult motion phases to initialize to during training. However, when a motion is successfully completed, we do not immediately restart the environment, but instead pause the action at the final frame for a randomized period, then sample a new motion and goal for the robot to perform. This gives the robot an implicit curriculum; at the beginning of training when the robot is initially learning to imitate the motion, adaptive sampling allows us to focus on training the motion itself. However, once the motion is mastered to a degree that the robot no longer loses its balance, we allow the previous motion to act as the initialization for the next one. This way, training mirrors the situation in the field, allowing the policy to learn good recovery behaviors and transitions between motions. 

## **6 Motion Selection and Planning** 

The policy from section 5 executes a motion once it is handed a goal _G_ = ( _p, ν, n, t_ ). The job of the planning stack is simple: at every control step, decide _which_ action to play and supply the goal the policy expects (fig. 2). This breaks into three steps — measure the state of the object being interacted with (e.g. the ball), predict where it will go, and select the action that best deals with that predicted trajectory. 

**State estimation and prediction.** We track the dynamic object of interaction (ball, box, etc.) with an OptiTrack motion-capture system. From the noisy position measurements, a Kalman filter [51] estimates the object’s position and velocity (ˆ _xb,_ ˆ _vb_ ). We roll this state forward with a hybrid rigidbody model [52] that combines ballistic flight with bounces: 


where _g_ is gravitational acceleration, _C_ is an estimated coefficient of restitution, and _S_ = _{xb_ : _xb,z_ = 0 _}_ is the ground plane. Propagating the estimated state through _F_ yields a predicted trajectory _x_ ˆ _b_ ( _t_ ) over the next _N_ time steps. 

**Action selection.** Each candidate action _Ai ∈_ A carries a nominal contact point _p_<sup>_∗_</sup> _i_<sup>andcontact</sup> time _t_<sup>_∗_</sup> _i_<sup>, the lead time from motion start to impact (section 4).We select the action whose nominal</sup> 

8 


Figure 6: **TaskNPoint Space Coverage.** Our motion abstraction formulation allows us to cover a wide task space. Each colored sphere corresponds to a distinct reference human motion demonstration, and is centered around the point of contact. During training (section 5) we randomly sample points around each point of contact to provide the learning algorithm with a diverse set of possible ball trajectories. The radius of each sphere represents the standard deviation of the sampling. Notice that the primary actions here are a Cartesian product of the type of shot (e.g. forehand and backhand) and the number of steps needed to reach the proper position to execute the shot. 

contact point best matches the predicted trajectory: 


The inner minimization finds, for each action, the time _t_<sup>ˆ</sup> _i_ at which the ball passes closest to _p_<sup>_∗_</sup> _i_<sup>; the</sup> outer minimization picks the action _i_<sup>_∗_</sup> whose closest approach is smallest. Note that if _t_<sup>ˆ</sup> _i < t_<sup>_∗_</sup> _i_<sup>, then</sup> no action is executed. The target point sent to the policy is the predicted ball position at that time, _p_ ˆ = _x_ ˆ _b_ ( _t_<sup>ˆ</sup> _i∗_ ), while the velocity direction _ν_ and orientation _n_ are chosen heuristically. The spatial target is refreshed every step as new measurements arrive. Algorithm 1 gives the full procedure. 

**Triggering.** Because the spatial target keeps updating, the action choice could oscillate as the prediction is refined. To prevent this, once the predicted time-to-contact drops below the chosen motion’s lead time _t_<sup>_∗_</sup> _i_<sup>_∗_, we lock the action choice and initiate the motion; the spatial target continues to</sup> update until contact. 

## **7 Experimental Results** 

We implemented our method on a G1 humanoid robot and carried out experiments to assess whether our learning paradigm is successful in practice. Concretely, we wish to assess three properties of TaskNPoint: that we can cover a large task space from a few locally varied actions, that our task abstraction gives us robustness in deployment to novel ball trajectories and novel targets, and that the combination of these two ideas leads to successful hardware deployment without requiring extensive reward tuning or hyperparameter selection. 

**Task Space Coverage.** TaskNPoint abstracts dynamic motions in a way that enables us to cover a large task space with only a few actions, which we show in fig. 6. We define the task space as a 3D volume centered around the demonstration’s contact point, as opposed to previous approaches [6] in which the task space is constrained to be a heuristically defined plane. In table 3 we compare TaskNPoint to current state-of-the-art humanoid policies in simulation. The generalized success rate (GSR) over this volume is 93% for ballistic hitting (tennis) and 98% for box pick-and-place, using sizes equal to those selected for comparison in [7] and using identical metrics for success rate, generalized success rate, and target position error. Pairing variation in 3D contact location with the correct demonstration action yields a policy robust to changes in the 3D target. Notably, from less 

9 


Figure 7: **Qualitative Results.** We train TaskNPoint on a small set of reference demonstrations of tennis shots, soccer kicks, and box pick-and-place. By randomizing incoming target trajectories and positions, we are able to generalize to unseen target locations in deployment. We show successful execution of tennis shots (1st and 2nd row), soccer kicks (3rd row), and box pick-and-place (4th row). The columns show samples of the robot’s pose during task execution. 

than 10 demonstrations we are able to achieve successful actions over the same 3D motion volume, without extensive data augmentations or reward tuning as in current methods. 

**Hardware results.** We report hardware results of our policy in table 2. We deploy our controller on a 27-dof G1 humanoid robot, running the policy onboard, and feed OptiTrack data through ethernet. We use a motion capture system detailed in Appendix D.1 to estimate ball positions, get forward trajectory projections, and feed the target positions to the policy at 50hz. Figure 7 and the accompanying video showcase the robot returning balls thrown and kicked with speeds of up to 8m/s and distances up to 2m laterally from the robot. We carried out experiments involving different speed targets. For slow moving targets we have a perfect 100% hit rate which deteriorates slowly as the speed of the incoming balls increases. We measure 40-70% at ball toss speeds of 4-8 m/s. Because our task abstraction _G_<sup>_∗_</sup> = ( _p_<sup>_∗_</sup> _, ν_<sup>_∗_</sup> _, n_<sup>_∗_</sup> _, t_<sup>_∗_</sup> ) is agnostic to speed (which is handled by the higher-level action selection), all of these scenarios are ‘in distribution’, so the robot fails gracefully, remains standing, and continues to be able to return shots. 

Table 2: **Hardware Results.** Success rates over 20 trials per condition. 

||Tennis SR|Soccer SR|Box Pick-and-Place SR|
|---|---|---|---|
|**Slow (0-4 m/s)**|1.00|1.00|0.60|
|**Fast (4-8 m/s)**|0.45|0.70|n/a|


**Generalizing to Novel Tasks: Box Pick-and-Place.** How general is the abstraction of motion as a 3D conditioning point and contact time? We test this with a box pickup task, wherein we place boxes randomly in a 3m radius in front of the robot and task the robot to pick up the box and return it to its starting location, which we show in the accompanying video as well. We further discuss hardware details, limitations, and performance in Appendix D. 

10 

Table 3: **Simulation Result Comparison.** We compare TaskNPoint against the state-of-the art. We report success rate (SR); the rate at which the projectile is hit by the robot or the box is picked to a height of within 10cm of the target (waist) position with nominal ball trajectories/box positions from the original demonstration; generalized success rate (GSR); where the trajectory initial conditions/box positions are randomized either uniformly in a ball of size 0.3m in the ballistic case, or uniformly with a distance of up to 3m in the semicircular area in front of the robot in the box case; and target position error ( _eb_ ); the distance between the correct and actual interaction point (contact with box or ball). XMimic has the highest SR for ballistic hitting, but TaskNPoint has a higher GSR, suggesting that it is better able to generalize to novel trajectories. TaskNPoint performs best across all other metrics. 

|**Method**||**Ballistic Hitti**|**ng**|**Bo**|**x Pick-and Pl**|**ace**|
|---|---|---|---|---|---|---|
||SR_↑_|GSR_↑_|_eb_ (m)_↓_|SR_↑_|GSR_↑_|_eb_ (cm)_↓_|
|SkillMimic [53]|68.2%|30.9%|0.48 (0.13)|0.4%|0.0%|28.3 (2.13)|
|OmniRetarget [4]|75.8%|20.4%|0.15 (0.10)|0.0%|0.0%|13.3 (1.57)|
|HDMI [3]|90.0%|25.3%|0.07 (0.02)|95.8%|1.8%|13.1 (1.28)|
|HumanX [7]|**100%**|90.6%|0.09 (0.06)|99.3%|96.3%|8.67 (0.91)|
|TaskNPoint|99.5%|**93.0%**|**0.02 (0.01)**|**100.0%**|**98.0%**|**4.85 (3.65)**|


Figure 8: **MLE poses** . We test how well TaskNPoint scales with the number of demonstrations by training on MLE-estimated human poses from in-the-wild multi-view data of tennis practices and matches (section 4). Here we visualize the nominal point sampling volume during training. Each colored sphere is centered around the nominal point and corresponds to a distinct human demonstration, and the radius of each sphere corresponds to one standard deviation of the sampling area during training. We note that by increasing the number of demonstrations we are able to cover more shots, including volleys and overheads, and that many of the demonstration volumes overlap with each other, resulting in the ability to perform different actions on the same 3D point in space. 

**Ablations.** We run several ablations on our parameter selection and see that our policy is not only performant in the nominal setup, but robust to considerable variation in parameters from phase density, _τ_ ( _t_<sup>_∗,_+</sup> ) _− τ_ ( _t_<sup>_∗,−_</sup> ), to target nominal distance _||pi − p_<sup>_∗_</sup> _i_<sup>_||_.Weseegracefuldegradationof</sup> quality outside our best parameter choices, where failure rate remains consistently less than 10% and the average target position error falls until the robot is just performing its nominal motion. See our discussion in Appendix C.5. 

**Training On In-the-Wild Data.** We test the ability of TaskNPoint to handle additional motions by retraining the policy on up to 34 discrete motions (shown in fig. 8) and report our results in table 11. Overall success rate on 34 motions is 91%, with an average target position error of 4.9cm. The phase error remains at 0.5, unchanged from the baseline. This suggests that although we demonstrate successful deployment of a limited number of motions, our method scales well to more complex motion libraries, and does not sacrifice its quality. 

11 

## **8 Conclusion** 

We introduced TaskNPoint, an abstraction methodology and training pipeline for teaching dynamic skills to humanoid robots. We observe that the space of human motions is intrinsically discrete, composed of a suite of skills, each of which is dynamically adapted to environmental conditions and continuously varied in order to achieve a given goal. Through an intentionally simple implementation of our idea, we find that we can teach dynamic loco-manipulation skills such as tennis and soccer play and box picking and placing with only seconds of training data from a coach, and under an hour of training per task, all on a single GPU. We believe this direction offers a scalable and robust paradigm for humanoid learning of dynamic actions such as those found in sports. We expect future work in this direction to approach the problem of environmental conditioning for motion and target selection, along with targeted modeling of key interactions. 

## **9 Limitations** 

TaskNPoint’s loco-manipulation abilities are hindered by the lack of force feedback in training: we assume that the tasks we perform do not require this feedback for success. We believe that a direction more similar to [7] could be better here, in which we train with the simulated object-tobe-manipulated and therefore allow the policy to learn recovery behaviors, tactile feedback, and sensor robustness. However, this comes at a cost of complex data generation, longer training, and assumptions about the types of objects with which we will be interacting. Additionally, TaskNPoint assumes ground-truth estimator accuracy, and in practice the majority of our hardware deployment failure cases are due to imprecise estimates of ball trajectories. The relaxation of our hierarchical abstraction could provide a promising way forward at cost of generality, for instance, by modeling the estimator in the training pipeline. 

12 

### **Acknowledgments** 

Thanks to Lizhi Yang, Sergio Esteban, Nima Rahmanian, and Georgia Gkioxari for their advice. Thanks to Damiano Marsili for reviewing. This work is supported by the Technology Innovation Institute (TII) and the National Science Foundation Graduate Research Fellowship Program under Grant No. 2139433. Data of the Caltech Tennis Team was obtained through explicit IRB approved consent. 

## **References** 

- [1] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [2] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [3] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [4] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [5] Z. Zhang, H. Lu, Y. Lian, Z. Chen, Y. Liu, C. Lin, H. Xue, Z. Zeng, Z. Qi, S. Zheng, et al. Learning athletic humanoid tennis skills from imperfect human motion data. _arXiv preprint arXiv:2603.12686_ , 2026. 

- [6] Z. Su, B. Zhang, N. Rahmanian, Y. Gao, Q. Liao, C. Regan, K. Sreenath, and S. S. Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [7] Y. Wang, Q. Zhao, Y. F. Lau, R. Yu, H. W. Tsui, Q. Chen, J. Wang, J. Pang, and P. Tan. Humanx: Toward agile and generalizable humanoid interaction skills from human videos. _arXiv preprint arXiv:2602.02473_ , 2026. 

- [8] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4): 1–20, 2021. 

- [9] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [10] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [11] J. Hwangbo, J. Lee, and M. Hutter. Per-contact iteration method for solving contact dynamics. _IEEE Robotics and Automation Letters_ , 3(2):895–902, 2018. 

- [12] N. Rudin, D. Hoeller, P. Reist, and M. Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on robot learning_ , pages 91–100. PMLR, 2022. 

- [13] T. Haarnoja, B. Moran, G. Lever, S. H. Huang, D. Tirumala, J. Humplik, M. Wulfmeier, S. Tunyasuvunakool, N. Y. Siegel, R. Hafner, et al. Learning agile soccer skills for a bipedal robot with deep reinforcement learning. _Science Robotics_ , 9(89):eadi8022, 2024. 

13 

- [14] Y. Ma, A. Cramariuc, F. Farshidian, and M. Hutter. Learning coordinated badminton skills for legged manipulators. _Science robotics_ , 10(102):eadu3922, 2025. 

- [15] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. _arXiv preprint arXiv:2502.10363_ , 2025. 

- [16] Z. Wu, X. Huang, L. Yang, Y. Zhang, K. Sreenath, X. Chen, P. Abbeel, R. Duan, A. Kanazawa, C. Sferrazza, et al. Perceptive humanoid parkour: Chaining dynamic human skills via motion matching. _arXiv preprint arXiv:2602.15827_ , 2026. 

- [17] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [18] R. Yu, H. Park, and J. Lee. Human dynamics from monocular video with dynamic camera movements. _ACM Transactions on Graphics (TOG)_ , 40(6):1–14, 2021. 

- [19] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. Kitani, and W. Xu. Universal humanoid motion representations for physics-based control. In _International Conference on Learning Representations_ , volume 2024, pages 56766–56782, 2024. 

- [20] S. Peng, Y. Zhang, Y. Xu, Q. Wang, Q. Shuai, H. Bao, and X. Zhou. Neural body: Implicit neural representations with structured latent codes for novel view synthesis of dynamic humans. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9054–9063, 2021. 

- [21] G. Moon, T. Shiratori, and S. Saito. Expressive whole-body 3d gaussian avatar. In _European Conference on Computer Vision_ , pages 19–35. Springer, 2024. 

- [22] J. Rajasegaran, G. Pavlakos, A. Kanazawa, and J. Malik. Tracking people by predicting 3d appearance, location and pose. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2740–2749, 2022. 

- [23] D. C. Luvizon, D. Picard, and H. Tabia. 2d/3d pose estimation and action recognition using multitask deep learning. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 5137–5146, 2018. 

- [24] J. Rajasegaran, G. Pavlakos, A. Kanazawa, C. Feichtenhofer, and J. Malik. On the benefits of 3d pose and tracking for human action recognition. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 640–649, 2023. 

- [25] H. Choi, G. Moon, J. Y. Chang, and K. M. Lee. Beyond static features for temporally consistent 3d human pose and shape from a video, 2021. URL `https://arxiv.org/abs/2011.08627` . 

- [26] A. Kanazawa, J. Y. Zhang, P. Felsen, and J. Malik. Learning 3d human dynamics from video, 2019. URL `https://arxiv.org/abs/1812.01601` . 

- [27] Y. Wang, Y. Sun, P. Patel, K. Daniilidis, M. J. Black, and M. Kocabas. Prompthmr: Promptable human mesh recovery, 2025. URL `https://arxiv.org/abs/2504.06397` . 

- [28] Y. Wang, Z. Wang, L. Liu, and K. Daniilidis. Tram: Global trajectory and motion of 3d humans from in-the-wild videos, 2024. URL `https://arxiv.org/abs/2403.17346` . 

- [29] Z. Shen, H. Pi, Y. Xia, Z. Cen, S. Peng, Z. Hu, H. Bao, R. Hu, and X. Zhou. World-grounded human motion recovery via gravity-view coordinates. In _SIGGRAPH Asia 2024 Conference Papers_ , SA ’24, page 1–11. ACM, Dec. 2024. doi:10.1145/3680528.3687565. URL `http: //dx.doi.org/10.1145/3680528.3687565` . 

- [30] J. Li, J. Cao, H. Zhang, D. Rempe, J. Kautz, U. Iqbal, and Y. Yuan. Genmo: A generalist model for human motion, 2025. URL `https://arxiv.org/abs/2505.01425` . 

14 

- [31] Y. Yuan, S.-E. Wei, T. Simon, K. Kitani, and J. Saragih. Simpoe: Simulated character control for 3d human pose estimation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 7159–7169, 2021. 

- [32] Y. Yuan, V. Makoviychuk, Y. Guo, S. Fidler, X. Peng, and K. Fatahalian. Learning physically simulated tennis skills from broadcast videos. _ACM Trans. Graph_ , 42(4):66, 2023. 

- [33] N. Ugrinovic, B. Pan, G. Pavlakos, D. Paschalidou, B. Shen, J. Sanchez-Riera, F. MorenoNoguer, and L. Guibas. Multiphys: Multi-person physics-aware 3d motion estimation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 2331–2340, 2024. 

- [34] S. Zhang, Y. Zhang, F. Bogo, M. Pollefeys, and S. Tang. Learning motion priors for 4d human body capture in 3d scenes. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11343–11353, 2021. 

- [35] J. Li, S. Bian, C. Xu, G. Liu, G. Yu, and C. Lu. D &d: Learning human dynamics from dynamic camera. In _European Conference on Computer Vision_ , pages 479–496. Springer, 2022. 

- [36] Q. Wang, M. Zhu, R. Hou, K. Gillespie, A. Zhu, S. Wang, Y. Wang, G. I. Fernandez, Y. Liu, C. Togashi, et al. A hierarchical, model-based system for high-performance humanoid soccer. _arXiv preprint arXiv:2512.09431_ , 2025. 

- [37] J. Ren, J. Long, T. Huang, H. Wang, Z. Wang, F. Jia, W. Zhang, J. Wang, P. Luo, and J. Pang. Humanoid goalkeeper: Learning from position conditioned task-motion constraints. _arXiv preprint arXiv:2510.18002_ , 2025. 

- [38] Z. Luo, J. Wang, K. Liu, H. Zhang, C. Tessler, J. Wang, Y. Yuan, J. Cao, Z. Lin, F. Wang, et al. Smplolympics: Sports environments for physically simulated humanoids. _arXiv preprint arXiv:2407.00187_ , 2024. 

- [39] L. Liu and J. Hodgins. Learning basketball dribbling skills using trajectory optimization and deep reinforcement learning. _Acm transactions on graphics (tog)_ , 37(4):1–14, 2018. 

- [40] C. Liu, L. Jiang, Y. Wang, K. Yao, J. Fu, and X. Ren. Humanoid whole-body badminton via multi-stage reinforcement learning. _arXiv preprint arXiv:2511.11218_ , 2025. 

- [41] M. Kim, E. Jung, and Y. Lee. Physicsfc: Learning user-controlled skills for a physics-based football player controller. _ACM Transactions on Graphics (TOG)_ , 44(4):1–21, 2025. 

- [42] Y. Chen, S. Dong, X. Ji, J. Sun, Z. Luo, L. Zhao, J. Zhang, W. Li, J. Ma, B. Xu, et al. Learning human-like badminton skills for humanoid robots. _arXiv preprint arXiv:2602.08370_ , 2026. 

- [43] S. Calinon and A. G. Billard. What is the teacher’s role in robot programming by demonstration? – toward benchmarks for improved learning. _Interaction Studies_ , 8(3):441–464, 2007. doi:10.1075/is.8.3.08cal. 

- [44] C. L. Nehaniv and K. Dautenhahn. The correspondence problem. In K. Dautenhahn and C. L. Nehaniv, editors, _Imitation in Animals and Artifacts_ , pages 41–61. MIT Press, Cambridge, MA, 2002. ISBN 9780262042031. 

- [45] G. Pavlakos, V. Choutas, N. Ghorbani, T. Bolkart, A. A. A. Osman, D. Tzionas, and M. J. Black. Expressive body capture: 3d hands, face, and body from a single image, 2019. URL `https://arxiv.org/abs/1904.05866` . 

- [46] C. Yeung, T. Suzuki, R. Tanaka, Z. Yin, and K. Fujii. Athletepose3d: A benchmark dataset for 3d human pose estimation and kinematic validation in athletic movements, 2025. URL `https://arxiv.org/abs/2503.07499` . 

15 

- [47] I. Demler, X. Xie, B. Werner, A. Szczuka, and P. Perona. Caltennis: Large multi-view tennis video dataset and benchmark of monocular-to-3d pose estimation, 2026. URL `https:// arxiv.org/abs/2606.20542` . 

- [48] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [49] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [50] A. Bronars, Y. Park, and P. Agrawal. Tune to learn: How controller gains shape robot policy learning. _arXiv preprint arXiv:2604.02523_ , 2026. 

- [51] G. Welch, G. Bishop, et al. An introduction to the kalman filter. 1995. 

- [52] D. Nguyen, K. D. Cancio, and S. Kim. High speed robotic table tennis swinging using lightweight hardware with model predictive control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15278–15284. IEEE, 2025. 

- [53] Y. Wang, Q. Zhao, R. Yu, H. W. Tsui, A. Zeng, J. Lin, Z. Luo, J. Yu, X. Li, Q. Chen, et al. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17540–17549, 2025. 

- [54] Y. Xu, J. Zhang, Q. Zhang, and D. Tao. Vitpose: Simple vision transformer baselines for human pose estimation, 2022. URL `https://arxiv.org/abs/2204.12484` . 

- [55] N. Ravi, V. Gabeur, Y.-T. Hu, R. Hu, C. Ryali, T. Ma, H. Khedr, R. R¨adle, C. Rolland, L. Gustafson, E. Mintun, J. Pan, K. V. Alwala, N. Carion, C.-Y. Wu, R. Girshick, P. Doll´ar, and C. Feichtenhofer. Sam 2: Segment anything in images and videos, 2024. URL `https: //arxiv.org/abs/2408.00714` . 

- [56] Z. Teed and J. Deng. Droid-slam: Deep visual slam for monocular, stereo, and rgb-d cameras, 2022. URL `https://arxiv.org/abs/2108.10869` . 

- [57] S. F. Bhat, R. Birkl, D. Wofk, P. Wonka, and M. M¨uller. Zoedepth: Zero-shot transfer by combining relative and metric depth, 2023. URL `https://arxiv.org/abs/2302.12288` . 

- [58] K. Zakka, Q. Liao, B. Yi, L. L. Lay, K. Sreenath, and P. Abbeel. mjlab: A lightweight framework for gpu-accelerated robot learning. _arXiv preprint arXiv:2601.22074_ , 2026. 

16 

## **A Notation Table** 

Table 4: Notation and Definitions 

|**Variable**|**Definition**|
|---|---|
|_Video capture and camera calib_|_ration_|
|_N_|Number of cameras capturing the scene|
|_c_<sup>_i_</sup>|The_i_-th camera|
|_V _<sup>_i_</sup><br>|Video collected by camera_c_<sup>_i_</sup>, containing RGB frames_I_<sup>_i_</sup><br>_t_<br>|
|_t_<sup>_i_</sup><br>_k_|Length (total frames or duration) of video_V _<sup>_i_</sup>|
|_K_<sup>_i_</sup><br>|<br>Intrinsic matrix of camera_c_<sup>_i_ </sup>(R<sup>3</sup><sup>_×_4</sup>)<br>|
|_R_<sup>_i_</sup>_, T _<sup>_i_</sup>|Extrinsic rotation (_SO_(3)) and translation (R<sup>3</sup>) of camera_c_<sup>_i_</sup>|
|_Human pose reconstruction_||
|_p_|Number of people in the scene|
|_M_|Pre-trained monocular 3D human pose estimation model|
|_H_<sup>_i_</sup>|SMPL-X pose estimates for_p_people from video_V _<sup>_i_</sup>|
|_d_<sup>_i_</sup><br>_t_|Translation of all_p_people at time_t_(R<sup>_p×_3</sup>)|
|_ϕ_<sup>_i_</sup><br>_t_|Global orientation of all_p_people at time_t_(R<sup>_p×_3</sup>)|
|_θ_<sup>_i_</sup><br>_t_<br>|<br>Body pose (joint angles) of all_p_people at time_t_(R<sup>_p×_21</sup><sup>_×_3</sup>)<br>|
|_β_<sup>_i_</sup><br>_t_|Body shape parameters of all_p_people at time_t_(R<sup>_p×_10</sup>)|
|_Multi-view fusion_||
|_J_<sup>(</sup><sup>_i_)</sup><br>_c _<sup>_, J_(</sup><sup>_i_)</sup><br>_w_|Joint position estimate from camera_i_in camera / world frame (R<sup>3</sup>)|
|Σ<sup>(</sup><sup>_i_)</sup><br>_c _<sup>_,_ Σ(</sup><sup>_i_)</sup><br>_w_|Per-camera joint observation covariance, camera / world frame (R<sup>3</sup><sup>_×_3</sup>)|
|_P_MLE|Maximum-likelihood consensus joint position (R<sup>3</sup>)|
|_Reference motion and task_||
|A:=_{A_1_, A_2_, . . . }_|Set of reference actions(R<sup>_n×T ×K_</sup>)|
|<br>_K_|<br>Number of discrete actions from which the policy selects|
|_T_|Number of frames in a reference motion|
|_n_|Number of tracked key points on the robot|
|G|<br>A TaskNPoint goal defined as the tuple_{_(_p_<sup>_∗_</sup>_, ν_<sup>_∗_</sup>_, n_<sup>_∗_</sup>_, t_<sup>_∗_</sup>)_}_|
|_q_<sup>_∗_</sup><br>1:_T_<br>_τ_(_t_)_∈_[0_,_1]<br>|i    <br>Reference key-point positions (R<sup>_n×T_ </sup>)<br>Speed-agnostic motion phase, with_τ_(0) = 0and_τ_(_T_) = 1<br>|
|(_t_<sup>_∗,−_</sup>_, t_<sup>_∗,_+</sup>)|Time window of the crucial interaction (e.g., racket–ball contact)|
|Ω:= (_τ_(_t_<sup>_∗,−_</sup>)_, τ_(_t_<sup>_∗,_+</sup>))|Phase window in which target rewards are active|
|_p_<sup>_∗_</sup>|Target interaction point in the world|
|_ν_<sup>_∗_</sup>|Target interaction velocity|
|_n_<sup>_∗_</sup>|Target interaction orientation axis|
|_Training and target sampling_||
|_i_|Action / motion class index|
|_Ci_(_δ_)|Confidence region around a target for motion_i_|
|Σ_p,ν,n_ = diag(_σx, σy, σz_)_p,ν,n_|Covariance of target sampling around_p_<sup>_∗_</sup>_, ν_<sup>_∗_</sup>_, n_<sup>_∗_</sup>|
|_W_|Covered workspace,_W ⊆_<sup>�</sup><sup>_K_</sup><br>_i_1 <sup>_Ci_(</sup><sup>_δ_)</sup><sup>_,_</sup>|
|_δ_|<br>= <br>Coverage probability parameter|
|_r{p,ν}, rn_|Target position/velocity and orientation reward terms|
|_w{p,ν}, wn_|Target reward weights|
|_σ{p,ν}, σn_|Target reward bandwidths|


## **B Maximum-likelihood consensus pose** 

To establish a single robust 3D joint estimate per timestep from _N_ overlapping views, we form an MLE-weighted consensus pose. Let _Jc_<sup>(</sup><sup>_i_)</sup> _∈_ R<sup>3</sup> represent a joint position estimated by the monocular model from camera _i_ in its local coordinate frame. We model the per-camera measurement noise as 

17 

a Gaussian distribution centered at the true camera-frame joint position. To account for the fact that depth is the dominant error mode in monocular reconstruction, the covariance matrix Σ _c_<sup>(</sup><sup>_i_)</sup> _∈_ R<sup>3</sup><sup>_×_3</sup> is elongated along that camera’s depth axis. 

Before fusing the estimates, we must lift each camera’s prediction into the shared world coordinate system (the tennis court frame). Given the camera-to-world calibration parameters _R_ calib<sup>(</sup><sup>_i_)</sup> ~~c~~ 2w<sup>_∈_R3</sup><sup>_×_3</sup> and _T_ calib<sup>(</sup><sup>_i_)</sup> ~~c~~ 2w<sup>_∈_R3, the lifted world-frame joint observation is:</sup> 


To ensure correct coordinate transformation, the noise covariance matrix must also be transformed into the world frame. The world-frame covariance Σ<sup>(</sup> _w_<sup>_i_)is computed as:</sup> 


Let the true consensus world-frame joint position be _P_ . Assuming the measurement errors across the _N_ cameras are independent, the joint likelihood of observing the set of lifted estimates _D_ = _{Jw_<sup>(1)</sup><sup>_, . . . , J_</sup> _w_<sup>(</sup><sup>_N_)</sup> _}_ is the product of the individual Gaussian likelihoods: 


The Maximum Likelihood Estimate (MLE) for the true pose, _P_ MLE, is found by minimizing the negative log-likelihood: 


Taking the derivative with respect to _P_ and setting it to zero yields: 


Solving for _P_ yields the closed-form solution, which is a precision-weighted average of the lifted per-view estimates: 


This formulation ensures that the highly uncertain depth axes from individual monocular cameras are appropriately down-weighted during spatial fusion. We use the MLE pose for training on in-thewild videos of tennis practices and matches, as shown in fig. 8. 

### **B.1 Human pose reconstruction from video** 

Following PromptHMR[27], we first detect people and 2D joint poses using ViTPose [54], and associate people between frames by propagating masks and bounding boxes with SAM2 [55]. We estimate camera intrinsics and extrinsics using Droid-SLAM [56] and ZoeDepth [57]. Next, we recover 3D human pose estimates with PromptHMR [27], producing per-frame pose estimates of all _p_ detected people in the scene with 3D SMPL-X [45] parameters: _H_ = _{_ ( _dt, ϕt, βt, θt_ ) _}_<sup>_T_</sup> _t_ =0<sup>, with</sup> translation _dt ∈_ R<sup>_p×_3</sup> , body pose _θt ∈_ R<sup>_p×_21</sup><sup>_×_3</sup> , orientation _ϕt ∈_ R<sup>_p×_3</sup> , and shape _βt ∈_ R<sup>_p×_10</sup> . 

18 

## **C RL Training Details** 

We set our training hyperparameters according to the standard of the field for ease of reproducibility. We train using the Asymmetric Actor Critic PPO algorithm [49]. We use a discount factor of _γ_ = 0 _._ 99, a GAE of _λ_ = 0 _._ 95, learning rate of 1 _e −_ 3 and desired KL of 0 _._ 01. We set the max gradient norm to 1 _._ 0 and the entropy coefficient to 0 _._ 005, use 5 learning epochs per rollout, and each rollout is of length 24. We train on a single NVIDIA 4090 GPU with 4096 environments. Finally, both our actor and critic networks have three hidden layers of [512 _,_ 256 _,_ 128]. 

### **C.1 Observation Details** 

Table 5: **Observation space.** Observations used by the actor (policy) and critic (value function). Noise is injected only for actor observations during training. All positions and orientations in the robot base frame are denoted with subscript _b_ . 

|**Observation**|**Description**|Actor<br>(policy)|Critic<br>(value fn.)|Noise<br>_U_(_± ·_)|
|---|---|---|---|---|
|Motion command|Reference Body Positions, target positions, velocities, orientations|✓|✓|—|
|Anchor orientation_R_<sup>anc</sup><br>_b_|Rotation of anchor body in robot frame|✓|✓|0_._05|
|Base angular velocity_ω_|IMU angular velocity|✓|✓|0_._20|
|Joint positions_q_|Joint angles relative to default pose|✓|✓|0_._01|
|Joint velocities ˙_q_|Joint velocities relative to default|✓|✓|0_._50|
|Last action_at−_1|Previous joint-position targets|✓|✓|—|
|Anchor position_p_<sup>anc</sup><br>_b_<br>|Position of anchor body in robot frame|✗|✓|—|
|Body positions_p_<sup>body</sup><br>_b_|Positions of all tracked bodies in robot frame|✗|✓|—|
|Body orientations_R_<sup>body</sup><br>_b_|Rotations of all tracked bodies in robot frame|✗|✓|—|
|Base linear velocity_v_|IMU linear velocity|✗|✓|—|


### **C.2 Action Details** 

We use unbounded actions without activations on the actor output following the style of [12]. We do not clip our actions, instead taking the output of the actor, sending it through an action scaling to allow the network outputs to live in [ _−_ 1 _,_ 1], add this value to a default joint position, then send these as desired joint positions. PD controllers at each joint track the positions sent by the actor network at 200hz, with gains from [10]. 

### **C.3 Reward Details** 

Table 6: **Reward terms.** ˆ _·_ denotes quantities from the reference motion clip. Subscript _b_ denotes the robot base frame. _N_ is the number of tracked bodies. Log : SO(3) _→_ R<sup>3</sup> is the rotation-vector logarithm. Target rewards are gated to the configured phase window. 

|**Reward**|**Formula**|**Description**|**Weight**_w_|_σ_|
|---|---|---|---|---|
|_Motion imitation_|||||
|Anchor position|exp<sup>�</sup><br>_−∥p_<sup>anc</sup> _−_ˆ_p_<sup>anc</sup>_∥_<sup>2</sup>_/σ_<sup>2�</sup><br><br><sup>ˆ</sup><br>|Global anchor body position error|0_._0|0_._30|
|Anchor orientation|exp<sup>�</sup><br>_−∥_Log(<br>_R_<sup>anc</sup><sup>_⊤_</sup>_R_<sup>anc</sup>)_∥_<sup>2</sup>_/σ_<sup>2�</sup><br><br><br><br>|Global anchor body orientation error|0_._5|0_._40|
|Body positions|exp<sup>�</sup><br>_−_<sup>1</sup><br>_N_<br>�<br>_i _<sup>_∥pi_</sup><br>_b _<sup>_−_ˆ</sup><sup>_pi_</sup><br>_b_<sup>_∥_2</sup><sup>_/σ_2�</sup><br><br><br><sup>ˆ</sup><br><br><br>|Mean relative body position error in base frame|1_._0|0_._30|
|Body orientations|exp<sup>�</sup><br>_−_<sup>1</sup><br>_N_<br>�<br>_i _<sup>_∥_Log(</sup><br>_R_<sup>_i⊤_</sup><br>_b _<sup>_Ri_</sup><br>_b_<sup>)</sup><sup>_∥_2</sup><sup>_/σ_2�</sup><br><br><br>|Mean relative body orientation error in base frame|1_._0|0_._40|
|Body linear velocities|exp<sup>�</sup><br>_−_<sup>1</sup><br>_N_<br>�<br>_i _<sup>_∥vi −_ˆ</sup><sup>_vi∥_2</sup><sup>_/σ_2�</sup><br><br><br>|Mean global body linear velocity error|1_._0|1_._00|
|Body angular velocities|exp<sup>�</sup><br>_−_<sup>1</sup><br>_N_<br>�<br>_i _<sup>_∥ωi −_ˆ</sup><sup>_ωi∥_2</sup><sup>_/σ_2�</sup>|Mean global body angular velocity error|1_._0|_π_|
|_Target achievement_|||||
|Target position|exp(_−||p_<sup>_∗_</sup>_−p||_<sup>2</sup>_/σ_<sup>2</sup>)1_τ∈_Ω<br>|End-effector position error at target phase|1_._0|0_._30|
|Target orientation|exp(_−_(1_−⟨n_<sup>_∗_</sup>_, n⟩_)_/σ_<sup>2</sup>)1_τ∈_Ω<br>|End-effector primary-axis alignment error at target phase|1_._0|1_._00|
|Target velocity|exp(_−||ν_<sup>_∗_</sup>_−ν||_<sup>2</sup>_/σ_<sup>2</sup>)1_τ∈_Ω|End-effector velocity error at target phase|1_._0|1_._00|
|_Regularization_|||||
|Action rate|_−∥at −at−_1_∥_<sup>2</sup><br>|Penalizes high-input actions|_−_0_._10|—|
|Joint limits|_−_<sup>�</sup><br>_i_ <sup>max(</sup><sup>_qi −q_max</sup><br>_i_<br>_,_ 0) + max(_q_<sup>min</sup><br>_i_<br>_−qi,_ 0)|Penalizes joint position limit violations|_−_10_._0|—|
|Self-collisions|_−_<sup>�</sup><br>_c _<sup>_Fc_ 1[</sup><sup>_Fc > F_thr]</sup>|Penalizes self-contact forces above_F_thr=10 N|_−_10_._0|—|


19 

### **C.4 Termination Details** 

Our training environments terminate early as per the recommendation of [9] if any of the following criteria are met. We track the error of many of the robot’s bodies Z coordinate, terminating if any fall below 0.25m below the reference. We do not track any of the other directions, as for imperfect translations in the motion or if we want to move to a slightly different target, deviation from the anchor position in the lateral directions is desired. We terminate if the anchor body’s orientation exceeds 0.8 radians, ensuring the robot stays upright. Finally we use an episode length of 10s, so at this point the episode times out. 

### **C.5 Ablations** 

For our ablations, we measure four metrics. Training stability is measured in iterations to convergence, defined as the point at which the target position reward hits 95% of its final value consistently, rounded to the nearest 500 iterations (n/a indicates that it never converged). Note that each iteration, run on a single RTX4090 GPU, takes about an average of 1.15 seconds. Success rate is measured as rate at which the robot succeeds at the task without falling or self collision, average targeting error is the minimum distance between the target point and the interfacing link over the motion, and average phase error is the average time in seconds between the desired and actual contact with the target point. Each of the evaluations are run on 4096 parallel environments with randomized targets within 2m laterally, 0.5m vertically, and 0.2m longitudinally of the robot’s anchor point. Averages and standard deviations are taken across environments. 

Table 7: **Target Phase Length + Reward Density** 

|# Frames<br>Of Contact|Convergence Iterate|Success Rate|Target Position Error (m)|Target Phase Error (s)|
|---|---|---|---|---|
|1|3000|0.9939|0.0205 (0.0108)|0.1665 (0.2191)|
|3|3000|0.9768|0.0499 (0.0537)|0.1346 (0.2462)|
|5|4000|0.9846|0.0522 (0.0548)|0.1343 (0.2149)|
|7|5500|0.9854|0.0486 (0.0552)|0.1429 (0.2467)|
|15|n/a|0.9895|0.0927 (0.0961)|0.2338 (0.3822)|
|30|n/a|1.0000|0.3338 (0.1780)|0.4508 (0.7283)|
|200|n/a|0.9985|0.3253 (0.1771)|0.5057 (0.8225)|


We first ablate the phase density. Our nominal setup concentrates the entire goal reward at the impact frame; spreading the same reward over a longer phase window monotonically degrades targeting, and at the limit (200 frames) the policy collapses to pure imitation without hitting the target. Despite the sparsity of the single-frame reward, Figure 9 shows dense behavior around the target phase — a favorable indicator of robustness in hit time. 

Table 8: **Target Mean Variation** 

|_||_¯_p −p_<sup>_∗_</sup>_||_|Convergence Iterate|Success Rate|Target Position Error (m)|Target Phase Error (s)|
|---|---|---|---|---|
|**0.0**|3000|0.9939|0.0205 (0.0108)|0.1665 (0.2191)|
|**0.374**|13000|0.9907|0.0523 (0.0553)|0.1302 (0.2334)|
|**0.412**|17000|0.9824|0.0537 (0.0524)|0.1278 (0.2147)|
|**0.469**|22000|0.9819|0.0754 (0.0890)|0.1500 (0.3325)|
|**0.538**|n/a|0.9841|0.0925 (0.1024)|0.1643 (0.3645)|


We ablate the command formulation along three axes. Varying the mean offset from the nominal target, the policy tracks reliably out to roughly 0.6m on tennis tasks, beyond which training stability degrades as the policy takes longer to discover that hitting the target — not just imitating the motion — earns reward. Varying the target standard deviation leaves average targeting error roughly 

20 

Table 9: **Target Standard Deviation Variation** 

|Co|nvergence Iterate|Success Rate|Target Position Error (m)|Target Phase Error (s)|
|---|---|---|---|---|
|_σ_<sup>2</sup><br>_y_<sup>_, σ_2</sup><br>_z_ <sup>(</sup>|<sup>within hitting p</sup>|<sup>lane)</sup>|||
|**0.20**|3000|0.9939|0.0205 (0.0108)|0.1665 (0.2191)|
|**0.25**|6500|0.9731|0.0465 (0.0489)|0.1376 (0.2402)|
|**0.30**|7000|0.9893|0.044 (0.048)|0.1299 (0.1948)|
|**0.35**|9500|0.9946|0.0428 (0.0517)|0.137 (0.2373)|
|**0.40**|9000|0.9988|0.0406 (0.0503)|0.1321 (0.2169)|
|**1.0**|n/a|1.0000|0.3569 (0.1831)|0.467 (0.7425)|
|_σ_<sup>2</sup><br>_x_ <sup>(out</sup>|<sup>of hitting plane</sup>|<sup>)</sup>|||
|**0.05**|5000|0.9507|0.0465 (0.052)|0.1317 (0.2194)|
|**0.10**|3000|0.9939|0.0205 (0.0108)|0.1665 (0.2191)|
|**0.15**|4000|0.958|0.0458 (0.0539)|0.1307 (0.2278)|
|**0.20**|5000|0.9722|0.0474 (0.0533)|0.1343 (0.2330)|
|**0.25**|6000|0.9768|0.0495 (0.0515)|0.1318 (0.2059)|
|**1.0**|18000|0.9727|0.0536 (0.0561)|0.1333 (0.2352)|


Table 10: **Motion Retiming** 

|Convergence Iterate|Success Rate|Target Position Error (m)|Target Phase Error (s)|
|---|---|---|---|
|Eval Hz = Train Hz||||
|**0.33**<br>7000|0.9971|0.1820 (0.1714)|0.4739 (1.2329)|
|**0.66**<br>6000|0.9988|0.0383 (0.0485)|0.1853 (0.3047)|
|**1.0**<br>3000|0.9939|0.0205 (0.0108)|0.1665 (0.2191)|
|**1.33**<br>8500|0.9963|0.0344 (0.0253)|0.1054 (0.1485)|
|**1.66**<br>9000|0.9968|0.0346 (0.0261)|0.0902 (0.1203)|
|Eval Hz = 1.0||||
|**0.33**<br>7000|0.7793|0.2384 (0.1227)|0.3069 (0.5924)|
|**0.66**<br>6000|0.8582|0.0754 (0.0518)|0.1383 (0.2321)|
|**1.0**<br>3000|0.9939|0.0205 (0.0108)|0.1665 (0.2191)|
|**1.33**<br>8500|0.9634|0.0661 (0.0486)|0.1326 (0.2238)|
|**1.66**<br>9000|0.8318|0.1023 (0.0541)|0.1757 (0.2924)|


constant until the variance becomes very large, at which point the policy reverts to pure imitation. Finally, varying motion speed in training and deployment shows that kinematic retargeting combined with our phase observation yields robustness to retiming: the policy is best when training and deployment speeds match, but remains reasonably performant when they do not. 

### **C.6 Simulation Parameters and Domain Randomization** 

We run Mjlab [58] at 200hz with a control decimation of 4, giving a policy a frequency of 50hz. We perform identical domain randomization to the Mjlab imitation policy setup, randomizing pushes on our robot, our base COM offset, encoder bias, and foot friction. 

21 

Table 11: **Motion Count** 

||Training Stability|Success Rate|Target Position Error (m)|Target Phase Error (s)|
|---|---|---|---|---|
|**10**|7000|0.9878|0.0319 (0.0158)|0.5750 (0.2834)|
|**15**|4700|0.9944|0.0346 (0.0265)|0.5579 (0.8532)|
|**20**|19800|0.9277|0.0413 (0.0331)|0.7102 (1.0616)|
|**23**|9500|0.9265|0.0422 (0.0327)|0.7189 (1.0247)|
|**28**|17900|0.969|0.0453 (0.0332)|0.5153 (0.8635)|
|**34**|7200|0.9082|0.0495 (0.0386)|0.5077 (0.8005)|


Figure 9: **TaskNPoint Phase Histogram.** We get density of target hit time even with very sparse rewards. We define the goal window as the phase range that we emperically determine is sufficient to get a solid hit. 

## **D Hardware Results** 

We evaluate on three hardware tasks. Tennis success is a racket–ball contact; soccer success is a foot–ball contact; box pick-and-place success requires lifting a 0.3m x 0.3m x 0.5m box and dropping it within 1m of the goal. Each task has a slow variant (stationary, gently tossed, or swung on a rope) and a fast variant (balls thrown or kicked at 4–8 m/s), with objects placed up to 3m laterally for sports and within a 3m semicircle in front of the robot for boxes. We run 20 trials per condition. The robot achieves a perfect hit rate on slow sports targets, with box pickup somewhat lower: every box failure was an imperfect grasp, unsurprising given that we do not train recovery behaviors. Performance on fast targets degrades gracefully with ball speed, and every failure traced to the perception stack; the tennis–soccer gap reflects the difficulty of tracking a bouncing tennis ball on uneven floor. Notably, the robot tolerated pushes and varied room and lighting conditions, and never fell even on missed hits, which are properties we attribute to the abstraction. Training with the estimator in the loop, or with motion-capture failures in domain randomization, should close the remaining gap; we leave this to future work. 

### **D.1 Estimation Details** 

We find the target and the robot using an OptiTrack Motion Capture setup running at 120hz composed of 8 cameras capturing an effective 4.5m by 7.5m by 3m volume. 

22 

