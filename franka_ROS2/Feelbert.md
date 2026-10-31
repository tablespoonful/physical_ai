---
title: "Feelbert: A Feedback Linearization-based Embedded Real-Time Quadrupedal Locomotion Framework"
date: "2025-04-28"
authors: "Aristide Emanuele Casucci; Federico Nesti; Mauro Marinoni; Giorgio Buttazzo"
url: https://arxiv.org/abs/2504.19965
pdf: https://arxiv.org/pdf/2504.19965
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2504.19965)** / [論文ページ](https://arxiv.org/abs/2504.19965)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# Feelbert: A Feedback Linearization-based Embedded Real-Time Quadrupedal Locomotion Framework 

Aristide Emanuele Casucci<sup>1</sup> , Federico Nesti<sup>1</sup> , Mauro Marinoni<sup>1</sup> , Giorgio Buttazzo<sup>1</sup> 

**_Abstract_ —Quadruped robots have become quite popular for their ability to adapt their locomotion to generic uneven terrains. For this reason, over time, several frameworks for quadrupedal locomotion have been proposed, but with little attention to ensuring a predictable timing behavior of the controller.** 

**To address this issue, this work presents Feelbert, a modular control framework for quadrupedal locomotion suitable for execution on an embedded system under hard real-time execution constraints. It leverages the feedback linearization control technique to obtain a closed-form control law for the body, valid for all configurations of the robot. The control law was derived after defining an appropriate rigid body model that uses the accelerations of the feet as control variables, instead of the estimated contact forces. This work also provides a novel algorithm to compute footholds and gait temporal parameters using the concept of imaginary wheels, and a heuristic algorithm to select the best gait schedule for the current velocity commands.** 

**The proposed framework is developed entirely in C++, with no dependencies on third-party libraries and no dynamic memory allocation, to ensure predictability and real-time performance. Its implementation allows Feelbert to be both compiled and executed on an embedded system for critical applications, as well as integrated into larger systems such as Robot Operating System 2 (ROS 2). For this reason, Feelbert has been tested in both scenarios, demonstrating satisfactory results both in terms of reference tracking and temporal predictability, whether integrated into ROS 2 or compiled as a standalone application on a Raspberry Pi 5.** 

## I. Introduction 

In recent years, researchers have put increasing effort in creating novel solutions for legged robots due to their ability to adapt their locomotion to generic uneven terrains. Robots with at least six legs can easily achieve a stable walk by always keeping at least three feet on the ground, but they are more expensive to build. On the other hand, the locomotion of quadrupedal and bipedal robots requires going through moments of instability, while they have less than three feet on the ground. 

> 1Department of Excellence on Robotics and AI, Sant’Anna School of Advanced Studies, Pisa, Italy 

Therefore, they are the most studied among legged robots. 

Over the years, various solutions have been proposed to address this problem, generally considering simplified kinematic models, such as spring-loaded inverted pendulum (SLIP) [1], [2], or linearized dynamic models controlled with optimal control techniques such as model predictive control (MPC) [3], [4], [5], [6], [7], [8], or whole-body control (WBC) [8], [9], [10], [11]. More recent approaches involve neural controllers such as central pattern generator (CPG) [12], [13] and reinforcement learning (RL) [13], [14]. 

Each of these publicly available solutions presents its advantages, but none of them has been designed with the intent of being deployed on an embedded system with hard real-time execution constraints. To the best of our knowledge, only a few works considered realtime execution of their framework, but only in terms of achieving relatively high execution frequencies on their platform, without providing timing guarantees [4], [6], [7], [8], [9], [10], [11]. However, respecting hard realtime execution constraints is crucial for safety-critical applications where predictability is paramount and computational resources are limited. 

## _A. Method Overview_ 

Since quadrupedal locomotion is a complex problem, it is typically addressed by dividing it into sub-problems. For this reason, many works proposed modular frameworks [4], [7], [8], [9], [11], [12], [14], [15], [16], [17], [18], in which each module solves a sub-problem. Some of such frameworks are divided into a gait planning module, a body planning module, and a body tracking module [7], [11], [12], [15], [17], [18]. 

Feelbert follows a similar modular architecture, but it is the first quadruped locomotion framework designed to ensure a predictable execution behavior suitable for implementation on embedded systems with limited resources and hard real-time execution constraints. This is achieved thanks to the adoption of simple algorithms to obtain lower execution times, improve temporal predictability, and reduce the memory footprint. The proposed implementation also avoids the use of third-party 

2 

libraries to improve timing predictability, adaptability, and maintainability. 

Figure 1 summarizes Feelbert’s architecture. The framework receives high-level velocity commands ( _vfw_<sup>_⋆_,</sup> _vlw_<sup>_⋆_,</sup><sup>_ψ_˙</sup><sup>_⋆_)andheightandinclinationcommands(</sup><sup>_z⋆_,</sup><sup>_φ⋆_,</sup> _θ_<sup>_⋆_</sup> ) from a joystick or a motion planner. The main feedback from the robot is defined by the foot contact signals _σ_ 1:4, and the joint angle values _<u>q</u>_ 1:4<sup>.Theframework</sup> outputs the joint velocity commands _<u>q</u>_ ˙ _⋆_ <u>1:4</u><sup>tomovethe</sup> legs. The framework is organized in 3 macro-blocks: _Feet Manager_ , _Body Reference_ , and _Body Manager_ . 

The _Feet Manager_ is responsible for converting the high-level velocity commands into the trajectory of each foot, by first computing the footholds, the gait schedule, and the gait period. It outputs the feet control signals, which are sent to the _Body Manager_ . 

The _Body Reference_ translates high-level commands and foot contact signals _σ_ 1:4 into online references for the body and sends them to the _Body Manager_ . Such references stabilize the body, by maintaining the Zero Moment Point (ZMP) within the Support Polygon. 

The _Body Manager_ is responsible for low-level body control. Specifically, it receives the foot control signals from the _Feet Manager_ , the body references from the _Body Reference_ , and the feedback from the robot, returning the joint velocity commands _<u>q</u>_ ˙ _⋆_ <u>1:4</u><sup>asoutput.It</sup> also computes additional model data required by the _Feet Manager_ and the _Body Reference_ that will be specified in Section IV-C. 

In the current implementation of Feelbert, the _Feet Manager_ and _Body Reference_ blocks were designed assuming locomotion on a flat horizontal terrain. In the future, these blocks will be extended to handle other types of terrain. In any case, the modular division allows straightforward replacement or modification of these blocks, if required by the application. 

## _B. Contributions_ 

The main contribution presented in this article is an efficient and predictable quadrupedal locomotion framework (Feelbert), specifically designed to be executed on embedded boards with limited computational resources. To achieve this goal, feedback linearization was applied to derive a single closed-form control law for the body, as detailed in Section IV-C5. To the best of our knowledge, this is the first work that applies a feedback linearization technique to the control of a quadruped robot, achieving satisfactory results both in terms of reference tracking and temporal predictability, as shown by the experiments in Section V. This control law holds for all the 15 cases in which the robot has at least one foot on the ground, thanks to the incorporation of the foot contact signals into the model of the robot to be controlled. Such foot contact signals are independent of 

foot positions, making the model suitable for any type of terrain and walking. 

The proposed model, detailed in Section IV-C4, adopts a new form of state space that uses foot accelerations as control inputs, while typical implementations use joint torques and estimated foot contact forces. Furthermore, such a model is obtained by solving the inverse dynamics of the robot through LDQ matrix decomposition [19], which always requires a fixed number of operations to execute, making it temporally predictable, as detailed in Section IV-C3. 

In addition, the following improvements were introduced in gait management, always focusing on predictability and efficiency: 

- The projection of the main body onto the horizontal plane was modeled as a planar vehicle with pivoting wheels. This allows (i) computing online the footholds as a function of the velocity commands, as detailed in Section IV-A1, and (ii) computing online the gait temporal parameters that maintain the final footholds within the foot workspaces, while keeping the feet off the ground for the shortest possible time, as detailed in Section IV-A2. 

- A heuristic algorithm, described in Section IV-A4, is proposed to select the correct gait schedule, among the six different possibilities. It maximizes the longitudinal stability margin in each direction of motion (forward, backward, leftward, rightward, clockwise, counterclockwise) by determining the predominant motion in case of intermediate directions. 

- Despite the common assumption that the foot remains stationary while touching the ground, other works neglected to choose a foot reference trajectory with both zero velocity and zero acceleration at the moment the foot touches the ground [9], [11], [12], [14], [20]. In this work, to fully respect the stationary foot assumption, foot reference trajectories are chosen to have both zero velocity and zero acceleration when the foot touches the ground. 

## _C. Outline_ 

The rest of the paper is organized as follows: Section II presents an overview of the existing approaches; Section III precisely formalizes the problem addressed in this work; Section IV illustrates the proposed solution; and Section V presents the results of the simulation experiments that have been carried out to show the effectiveness of the proposed approach. 

## II. Related Work 

Quadruped locomotion is a complex problem that is generally divided into two main sub-tasks: _body management_ and _foot management_ . The next two sections analyze the literature related to both tasks. 

3 


Fig. 1: Feelbert block diagram. 

## _A. Body Management_ 

This task consists of finding how to control the supporting legs in order to move the robot body in a desired direction while guaranteeing the equilibrium (i.e., without causing it to fall). This is done by first modeling the robot body and then applying a specific control strategy to that model. Therefore, body management is divided into two sub-problems: body modeling and body control. 

_1) Body Modeling:_ Over the years, several models of increasing complexity have been proposed for legged robots, each having a different degree of accuracy in representation depending on the application scope. The most well-known models proposed in the literature are presented below. Typically, for a legged robot, the instantaneous center of rotation in the vertical plane is known as the _Zero Moment Point_ (ZMP) [21]. 

Given that, the simplest model is the linear inverted pendulum (LIP) [1], which describes the body as an inverted pendulum composed of a point with a given mass at the top of a variable-length rod rotating around the ZMP. The rod changes its length to keep the mass at a constant height while this moves. This model is mainly used to compute the trajectory of the center of mass under the effect of gravity when a foot touches the ground, and therefore neglects the rotational dynamics of the robot’s body. This model was designed for biped robots [21] but was also applied to quadrupeds [1], [2], [7], [10], [15]. 

Since in many quadruped robots the masses of the leg links are negligible compared to that of the main body, the single rigid body dynamics (SRBD) model assumes that the robot’s legs are massless, so that all the dynamic properties of the robot coincide with those of the central rigid body. This is a fair approximation, thus it has been used in many works [3], [4], [5], [6], [11], [12], [22], [18], [23], [24]. This model has also been adopted in this work as presented in Section III. 

The full dynamic model (FDM) is the standard model of equations of motion for a robot, which takes into account the dynamic properties of all the robot’s links. 

It is constructed using Lagrange dynamic equations or the Recursive Newton-Euler Algorithm (RNEA). Since this model does not neglect any rigid body, it is highly accurate and it is employed in many works [3], [9], [10], [11], [25], [16], [17], [26]. On the other hand, it is also quite complex to calculate manually. Therefore, thirdparty libraries are typically used to compute the model components numerically. 

_2) Body Control:_ As reported by Chai et al. [27], the existing methods developed for motion control can be classified into two main categories: model-based methods and model-free methods. Model-based control methods encompass various techniques that depend on the body model chosen from those listed in Section II-A1. 

The stability criterion control uses the LIP model to calculate a stable trajectory for the quadruped’s center of mass or the ZMP. The method ensures that a certain stability margin is met [28], requiring detailed planning of foot and center of mass trajectories, thus sacrificing dynamic performance [27]. 

Inverse Dynamics Control employs a full dynamic model of a generic floating-base robot to compute the joint torques needed to follow the desired joint trajectories. However, this approach does not address the problem of finding the desired joint trajectories required to move the quadruped robot, which must be solved separately. This control technique has been applied to a quadruped robot by Buchli [25] and Hutter [29]. Buchli complemented it with an algorithm that plans the center of mass trajectories in advance. Hutter complemented it by defining a hierarchical least squares optimization problem, where the optimization variables are the joint torques, joint accelerations, and foot contact forces. 

Model predictive control (MPC) is an optimal control technique that uses a linear model of a system to compute the best sequence of inputs over a prediction horizon. The first input from this planned sequence is then applied. Since MPC is designed for linear systems, it has been used with linear models, such as the LIP model by Hamed et al. [7] or first-order Taylor approximation 

4 

of the SRBD model by different authors [5], [6], [8], [22], [23], [24]. Since linearization limits the applicability of MPC, some works used a non-linear MPC (NMPC) [4], [18]. 

Whole-body control (WBC) addresses the problem by defining a series of control tasks on the full dynamic model. Such tasks, each defined with different priority, are then hierarchically solved by third-party quadratic programming (QP) solvers [8], [9], [10], [11], [29]. Sometimes, WBC is used in conjunction with other controllers that generate reference trajectories for the body [8], [11]. 

Both WBC and MPC are based on optimization techniques that require solving computationally intensive non-linear optimization problems and may encounter convergence issues [11]. For instance, for NMPC it is often challenging to meet real-time requirements because the solver can get stuck in local minima [16]. Moreover, in a numerical optimization solver algorithm, each inequality constraint can activate a distinct operational branch, making the temporal evolution of the algorithm difficult to predict. Usually, these optimization algorithms rely on third-party libraries [9], [10], [18], [22], [26] that may not be able to guarantee predictable temporal behavior, due to dynamic allocation or non-optimized memory usage. These factors are particularly undesirable in hard real-time systems that must guarantee a result within predefined time bounds. 

Model-free control methods encompass several techniques, that do not depend on the choice of a model. The two most commonly used approaches of this type are described below. 

Central pattern generator (CPG) is a biomimetic control method that involves constructing multiple periodic oscillators to generate rhythmic motion by coordinating their connections. Since parameter tuning can be complex, this technique is often combined with genetic algorithms or reinforcement learning to optimize the parameters [13]. 

Reinforcement Learning (RL) is a learning technique that enables the robot to learn to walk based on its experience, by choosing an action from a set of possible actions it can perform in a given state and receiving feedback on the quality of the chosen action in terms of reward. Since the sets of possible states and actions for a quadruped robot are very large, it is necessary to use neural networks to represent value functions and policies, which could require too much memory [30] and computational power [31], [32], [33] for a generic embedded system, that is, without a dedicated hardware accelerator based on FPGA [31]. For example, in the framework presented by Tan et al. [14], the RL component is executed on a dedicated server rather than on the robot itself, since the robot’s onboard computer lacked sufficient computational power to run RL online. Therefore, although RL is a very powerful tool for high- 

level tasks that are difficult to model mathematically, we chose not to integrate it in our framework, which focuses on low-level tasks that are easily modeled, in order to be predictably and effortlessly executed on embedded systems with hard real-time constraints and limited computational resources. 

## _B. Feet Management_ 

This task consists of finding the alternation of foot movements that allows the robot to walk and run in the environment. Since it is a complex problem, it is handled by dividing it into various subproblems described below. 

_1) Gait planning:_ The gait is the pattern of limb movements during locomotion. Kajita and Espiau [21] provided definitions commonly adopted for characterizing the gait. 

Since the gait is repeated periodically, it is defined as a cycle that lasts for a given period _T_ . Being alternately lifted and lowered to walk, each foot goes through two phases during the gait cycle: a support phase, during which the foot is on the ground, and a swing phase, during which the foot is lifted. Assuming that each foot remains lifted for the same amount of time as the others, a duty factor _β ∈_ [0; 1] can be defined such that the support phase lasts _Tst_ = _βT_ and the swing phase lasts _Tsw_ = (1 _− β_ ) _T_ for each foot. 

Additionally, since feet cannot all be lifted simultaneously, they are lifted at different times, appropriately phased with each other depending on the type of gait. Consequently, each foot _i_ leaves the ground at the instant _t_ 0 _,i_ ( _lift-off time_ ) and touches the ground again at the instant _t_ 0 _,i_ + _Tsw_ ( _touch-down time_ ). In our work, we defined a policy for choosing the parameters _T_ , _Tsw_ , and _β_ based on the input commands to the framework and the constraints on the footholds, as explained in Section IV-A2. 

A common convention is to number the feet on the left with odd numbers and the feet on the right with even numbers, starting from the front feet. Therefore, in a quadruped robot, foot 1 is the front-left (FL) foot, foot 2 is the front-right (FR) foot, foot 3 is the rear-left (RL) foot, and foot 4 is the rear-right (RR) foot. 

Defining the function _γ_ : _{_ 1 : 4 _} →{_ 1 : 4 _}_ such that _i_ = _γ_ ( _j_ ) is the foot to be lifted as _j_ -th, the gait that has the maximum stability in a certain direction of motion is called the _crawl gait_ and is characterized by the lifting sequences reported in Table I. 

|**Motion**|_γ_(1)|_γ_(2)|_γ_(3)|_γ_(4)|
|---|---|---|---|---|
|Forwards|FL|RR|FR|RL|
|Backwards|FL|RL|FR|RR|
|Leftwards|FL|RR|RL|FR|
|Rightwards|FL|FR|RL|RR|
|Counterclockwise|FL|RL|RR|FR|
|Clockwise|FL|FR|RR|RL|


TABLE I: Crawl gait according to motion. 

5 

The crawl gait that maximizes the longitudinal stability margin is called the _wave gait_ and is characterized by the lift-off times pattern in the table of Equation (1). 


Such lift-off times can be visualized in the gait graph shown in Figure 2. 


Fig. 2: Gait graph of a wave gait, where dark green and dark red arrows indicate the lift-off and touch-down times respectively, with respect to the period _T_ and the swing time _Tsw_ . 

In our work, we adapted the state-of-the-art convention reported above by defining a policy that handles cases where the input commands to the framework do not correspond to a motion in a single direction, as explained in Section IV-A4. 

_2) Foothold planning:_ Foothold planning is the problem of choosing where to place the foot after it has been lifted to take a step. Terrains without holes or deformations allow much more freedom in foot landing choice. Many works [4], [8], [9], [11], [18] have chosen to refer to the Raibert heuristic defined for a onelegged robot by Raibert [34], introducing variations or corrections. 

This heuristic approach was avoided in this work, instead adopting an algorithm based on the concept of imaginary wheels, explained in Section IV-A1. 

_3) Foot trajectories:_ Each foot must follow a trajectory that lifts it and places it in the desired foothold. Therefore, after computing the footholds, it is necessary to connect them with a proper trajectory. Several trajectories have been proposed in various works. 

Tan et al. [14] used polynomial trajectories whose parameters are calculated by a neural network. Barasoul et al. [12] used elliptical trajectories inspired by the CPG, which are cut when the foot touches the ground. Li et al. [11] used second-order B´ezier curves to interpolate the initial and final footholds by raising the foot to a certain height. Raiola et al. [9] used a parametric semielliptical trajectory in a local foot frame. Shi et al. [20] 

used a cycloidal trajectory (described by a point on the border of a rolling wheel) in a global frame. 

All these solutions have a common inconsistency: despite the control techniques used for the body are based on the assumption that the feet have both zero velocity and acceleration when on the ground, they do not take this aspect into account when choosing foot trajectories. However, in the proposed framework, this assumption is taken into account, as explained in Section IV-A5. 

## III. System model 

This section describes the quadruped robot model on which Feelbert was built. Generally, a quadruped robot consists of a floating base, named _body_ , to which four serial kinematic chains, named _legs_ , are connected. Each leg comprises three revolute joints, and its endeffector is named _foot_ . The quadruped robot model consists of a kinematic part, detailed later in Section III-A, and a dynamic part, detailed later in Section III-B. 

For the comprehension of the reader, here is a summary of the notation used throughout this article: small capital letters indicate points; over right arrows indicate vectors in space; framed capital letters indicate reference systems (frames); underlines generally indicate n-tuples; underlines with a superscript lowercase letter or number indicate the coordinates of the vectors in the frame specified by the superscript; _Ra_<sup>_b_is a rotation matrix from</sup> a frame _<u>A</u>_ to a frame _<u>B</u>_ <u>; [</u> _<u>a×</u>_ ] is the skew-symmetric matrix of the vector _<u>a</u> ∈_ R<sup>3</sup> such that [ _<u>a×</u>_ ] _<u>b</u>_ = _<u>a×b</u> ∀_ _<u>b</u> ∈_ R<sup>3</sup> ; and <u>�</u> _<u>i, j, k</u>_ <u>�</u> is the canonical basis of R<sup>3</sup> . 

## _A. Kinematics_ 

This subsection defines the kinematic quantities necessary to describe the motion of the robot. Such kinematic quantities are all illustrated in Figure 3. 

To correctly model the quadruped robot, the following frames are defined a fixed frame _<u>W</u>_ named _World_ , with origin o, such that _<u>gw</u>_ = _−gk_ <u>,</u> and a frame _B_ <u>0</u> named _Body_ attached to the body, with origin in the center of mass g of the body. 

The center of mass g can translate freely, then it has three degrees of freedom, and its coordinates are <u>og</u> _w_ = � _x y z_<sup>�</sup><sup>_⊤_</sup> . The body can rotate freely, so its orientation _R_ 0<sup>_w_</sup> <u>�</u> _<u>ϕ</u>_ <u>�</u> = _Rz_ ( _ψ_ ) _Ry_ ( _θ_ ) _Rx_ ( _φ_ ) has three degrees of freedom _<u>ϕ</u>_ = � _φ θ ψ_ � _⊤_ , corresponding to roll _φ_ , pitch _θ_ , and yaw _ψ_ . Therefore, the body has six _w_ degrees of freedom, represented by _<u>q</u>_ <u>0</u><sup>=</sup> _∈_ R<sup>6</sup> . <u>�og</u> _<u>ϕ</u>_ � 

In addition, each leg _i_ is made up of three revolute joints, each of which rotates by an angle _qij_ , therefore it has three degrees of freedom represented by _<u>qi</u>_<sup>=</sup> � _qi_ 1 _qi_ 2 _qi_ 3� _⊤_ . Since the robot has four legs, the robot has a total of 18 degrees of freedom. 

The coordinates in _B_ <u>0</u> of the linear velocity of the center of mass _⃗v_ g are given by _<u>v</u>_ 0 ~~g~~<sup>=</sup> � _R_ 0<sup>_w_</sup> <u>�</u> _<u>ϕ</u>_ <u>��</u> _⊤_ <u>og˙</u> _w_ , and 

6 


Fig. 3: The orange arrows are the _world_ and _body_ frames. The purple arrows are the position vectors of the center of mass and foot 4. The blue arrows are linear and angular velocities of the body. The red arrows are the joint angles of leg 2. The red points are the feet centers e _i_ . The purple points are the feet contact points f _i_ . The green line is the trajectory followed by foot contact point f2 lifted to make a step. 

By differentiating Equation (9), we obtain 

gf˙ _<u>i</u>_ 0 = _J_ ge0 _i_ <u>�</u> _<u>qi</u>_ � _<u>q</u>_ ˙ _i_<sup>+</sup><sup>_<u>ω</u>_</sup> 0 _~~w~~_ 0<sup>_× ζ_[</sup><sup>_R_</sup> 0<sup>_w_]</sup><sup>_⊤_</sup><sup>_<u>k</u>_</sup> _<u>,</u>_ (10) _∂_ ge _i_ 0 where we have defined _J_ ge<sup>0</sup> _i_ <u>�</u> _<u>qi</u>_ � := _∂qi_<sup>.</sup> The moment that foot _i_ touches the ground, its posi˙ ¨ tion of _<u>iw</u>_ stays constant, then of _<u>iw</u>_ = 0 and of _<u>iw</u>_ = 0. If we define 


for each foot _i_ , it always holds _σi_ of˙ _<u>iw</u>_ = 0 and _σi_ of¨ _<u>iw</u>_ = <u>0,</u> thus, for Equations (5) and (7), we have 


and 


_1) Uncontrollable motions:_ Let’s analyze how the relative motion of the feet on the ground influences the motion of the body: by applying Equation (12) to all the feet, we obtain 


those of the angular velocity of the body _⃗ωw_ 0 are given by _<u>ω</u>_ 0 _~~w~~_ 0<sup>=</sup><sup>_<u>φi</u>_˙</sup> + _θR_<sup>˙</sup> _x_<sup>_⊤_(</sup><sup>_φ_)</sup><sup>_<u>j</u>_</sup> + _ψR_<sup>˙</sup> _x_<sup>_⊤_(</sup><sup>_φ_)</sup><sup>_R_</sup> _y_<sup>_⊤_(</sup><sup>_θ_)</sup><sup>_<u>k</u>_</sup> = Ω<sup>0</sup> _w_ 0� _<u>ϕ</u>_ <u>�</u> _<u>ϕ</u>_ ˙. Together, they form the twist, whose coordinates in _B_ <u>0</u> are given by 


Each foot _i_ is assumed to be a sphere with center e _i_ and radius _ζ_ , that touches the ground at the contact point f _i_ . Therefore, the center e _i_ has coordinates 


where ge _<u>i</u>_ 0<sup><u>�</u></sup> _<u>qi</u>_ � depends on the chosen robot, and the contact point f _i_ has coordinates 


By differentiating Equation (4), we obtain 


where we have set 


By differentiating Equation (5), we obtain 


where we have defined 


From Equation (4) we derive 

where we defined 


and 


Equation (14) represents a system of 12 equations with 6 variables, because we want to find _<u>V</u>_ 0 _~~w~~_ 0<sup>_∈_R6asa</sup> function of <u>gf˙</u> 0 ~~1~~ :4<sup>_∈_R12.Equation(14)doesnothavea</sup> solution if _<u>V</u>_ 0 _~~w~~_ 0<sup>_∈N_[</sup><sup>_A_],thereforethenullspace</sup><sup>_N_[</sup><sup>_A_]</sup> can be considered the space of uncontrollable motions. If _r_ denotes the rank of matrix _A_ , then the body has only _r ≤_ 6 controllable degrees of freedom, because only _r_ equations are actually linearly independent. Since matrix _A_ changes depending on the contact flags _σ_ 1:4, the null space _N_ [ _A_ ] has been calculated for each possible number of grounded feet _N_ , thus deriving the corresponding value of its rank as _r_ = 6 _−_ dim _N_ [ _A_ ]. For brevity, the computation procedure is not reported here, but the resulting values of _r_ for each value of _N_ are shown in Table II. Knowing a priori the values of _r_ as a function of _N_ will allow us to make the LDQ decomposition robust to numerical approximations, as explained later in Section IV-C3. 


TABLE II: Values of _r_ = rank _A_ corresponding to the number of grounded feet _N_ computed offline. 


7 

## _B. Dynamics_ 

This subsection defines the dynamic quantities necessary to describe the causes of the motion of the robot. Such dynamic quantities are all illustrated in Figure 4. 


Fig. 4: The red arrows are the external forces acting on the robot. The magenta polygon is the Support Polygon. The magenta point z is the Zero Moment Point. 

The weight force _<u>F</u> w_ _~~g~~_<sup>=</sup><sup>_mg_</sup> _w_ = _−mgk_ acts on the center of mass g. A contact force _<u>F</u> w_ _~~⊥~~ ,i_<sup>=</sup><sup>_F w_</sup> _⊥,i_<sup>_<u>k</u>_</sup> such that _F⊥_<sup>_w_</sup> _,i_<sup>_≥_0,perpendiculartotheground,andafriction</sup> force _<u>F</u> w_ _~~∥~~ ,i_<sup>suchthat</sup><sup>_<u>k</u>_</sup> _⊤F w_ _~~∥~~ ,i_<sup>=0and</sup> <u>��</u> _<u>F</u> w_ _~~∥~~ ,i_ �� _≤ µsF w⊥,i_<sup>,</sup> parallel to the ground, act on the contact point f _i_ of each foot _i_ . For simplicity, in this work we assume _µs ≃∞_ . We define _<u>F</u> w_ _~~i~~_<sup>:=</sup><sup>_<u>F</u>_</sup> _w_ _~~⊥~~ ,i_<sup>+</sup><sup>_<u>F</u>_</sup> _w_ _~~∥~~ ,i_<sup>astheresultingforceon</sup> each contact point f _i_ . Since the forces on foot _i_ exist only if it touches the ground, it holds _<u>F</u> w_ _~~i~~_<sup>=</sup><sup>_σiF_</sup> _w_ _~~i~~_<sup>.</sup> 

According to the Newton-Euler equations of dynamics, the dynamic equilibrium of the forces acting on the quadruped robot is given by 


_1) Zero Moment Point (ZMP):_ As reported by Kajita and Espiau [21], the convex hull of the contact points of the feet that touch the ground is named _Support Polygon_ , and it can be defined mathematically by 


Defining the inertial wrench as 


Equation (18) can be rewritten as 


where the inertial wrench _<u>W</u>_ 0 _~~V~~_<sup>isdecomposedintoits</sup> components, i.e., the inertial force _<u>F</u>_ 0 _~~V~~_<sup>andtheinertial</sup> moment _<u>M</u>_ 0 _~~V~~_<sup>.StartingfromEquation(22),itcanbe</sup> proved [21] that there exists a point z named _Zero Moment Point_ (ZMP) such that 


where _<u>F</u> w_ _~~V~~ g_<sup>=</sup><sup>_R_</sup> 0<sup>_w_</sup> <u>�</u> _<u>F</u>_ 0 _~~V~~_<sup>_−_</sup><sup>_<u>F</u>_</sup> 0 _~~g~~_ � and _<u>M</u> w_ _~~V~~_<sup>=</sup><sup>_R_</sup> 0<sup>_wM_</sup> 0 _~~V~~_<sup>.Inthe</sup> case where <u>oz</u> _w ∈/_ P _sup_ , the dynamic equilibrium would not be maintained and the robot would become unstable. Therefore, the stability of the robot is guaranteed as long as <u>oz</u> _w ∈_ P _sup_ . 

## IV. Proposed framework 

This section presents in detail the components of Feelbert, by describing its internal sub-modules. 

As shown in Figure 1, the framework receives highlevel input commands, which can be sent either by a user through a joystick or by a high-level planner, and produces the joint velocities _<u>q</u>_ ˙ _⋆_ <u>1:4</u><sup>tomovethequadruped</sup> robot as required. The robot feeds back to the framework the actual joint positions _<u>q</u>_ 1:4<sup>andthecontactsignals</sup> _σ_ 1:4. 

Internally, the framework is divided into three main blocks: the _Feet Manager_ , the _Body Reference_ , and the _Body Manager_ , which are described below. 

## _A. Feet Manager_ 

This module receives high-level velocity commands (longitudinal velocity _vfw_<sup>_⋆_,lateralvelocity</sup><sup>_v_</sup> _lw_<sup>_⋆_,andyaw</sup> rate _ψ_<sup>˙</sup><sup>_⋆_</sup> ) and converts them into foot acceleration commands <u>of¨</u> _w_ ~~1~~ :4<sup>, forwarded to the</sup><sup>_Body Manager_. The block</sup> diagram of the _Feet Manager_ is illustrated in Figure 5 and consists of six modules described in the following subsubsections. 

_1) Wheels Commands:_ To compute footholds, we assume that the projection of the body on the ground (named _shadow_ ) has 4 imaginary wheels at points w _i ∀ i ∈{_ 1 : 4 _}_ , as shown in Figure 6. 

<u>owThis</u> _w_ ~~1~~ :4<sup>and</sup> block<sup>desired</sup> transforms<sup>velocities</sup> _vfw_<sup>_⋆_,</sup> <u>ow</u><sup>_v_</sup> ˙ _lw_<sup>_⋆_</sup> _w⋆_ ~~1~~<sup>,</sup> :4<sup>andin</sup><sup>_ψ_the˙</sup><sup>_⋆_into</sup><sup>_<u>W</u>_positions</sup> frame of such imaginary wheels. This data will then be used by the _Period_ block (see Section IV-A2), the _Gait Scheduler_ block (see Section IV-A4), and the _Trajectories Generator_ block (see Section IV-A5). 

For convenience, an intermediate frame _<u>S</u>_ ( _shadow_ ) is attached to the projection of the body on the ground (assumed flat), as shown in Figure 6. Therefore, for the origin k of _<u>S</u>_ we have <u>ok</u> _w_ = _<u>xi</u>_ + _yj_ <u>,</u> _Rs_<sup>_w_=</sup><sup>_Rz_(</sup><sup>_ψ_),</sup> 

8 


Fig. 5: Feet manager block diagram. 


Fig. 6: Shadow of the body (blue rectangle) delimited by imaginary wheels (blue dots w _i_ ). The _world_ , _shadow_ and _body_ frames are denoted in orange. The red dotted rectangles denote the feet workspaces _Wi_ . 

<u>kg</u> _s_ = _zk_ <u>,</u> _R_ 0<sup>_s_=</sup><sup>_Ry_(</sup><sup>_θ_)</sup><sup>_Rx_(</sup><sup>_φ_),anditscommanded</sup> velocity in _<u>W</u>_ is <u>ok˙</u> _w_ _~~⋆~~_<sup>=</sup><sup>_Rz_(</sup><sup>_ψ_)</sup> � _vfw_<sup>_⋆_</sup><sup>_<u>i</u>_</sup> + _vlw_<sup>_⋆_</sup><sup>_<u>j</u>_</sup> <u>�.</u> Hence, the position of wheel _i_ is given by 

ow _<u>iw</u>_ = ok _w_ + _Rsw_<sup>kw</sup><sup>_<u>i</u>_</sup> _s_ = _<u>xi</u>_ + _yj_ + _Rz_ ( _ψ_ ) kw _<u>is</u>_ (24) 

and its commanded velocity is given by 


where kw _<u>is</u>_ is provided by the _Body Manager_ as 


because it depends on current roll and pitch angles and the internal parameter gw _<u>i</u>_ 0. 

Since the feet are required to move as much as the imaginary wheels during a period, their positions and desired velocities are used to compute the initial and final footholds: it is desired that foot _i_ starts from the initial position ow _<u>iw</u>_ (0) and reaches the final position ow _<u>iw</u>_ ( _T_ ) of wheel _i_ . After updating the values of ow _<u>iw</u>_ and ow˙ _<u>iw⋆</u>_<sup>onlineusingEquations(24)and(25),the</sup> initial foothold is obtained as 


and the final foothold as 


where _t_ is the current time step _t_ marked by the clock (see Section IV-A3), and it is assumed that the desired velocity of the wheel remains constant throughout the gait period _T_ . This assumption holds as long as the highlevel velocity commands remain constant, but it has been experimentally proven effective also when the commands change, thanks to the fact that ow _<u>iw</u>_ , ow˙ _<u>iw⋆</u>_<sup>,and</sup><sup>_T_are</sup> updated at each execution of Feelbert. 

_2) Period:_ This block computes the gait period _T_ , the duty factor _β_ , and the swing time _Tsw_ (see Section II-B1 for definitions) as a function of the current positions and desired velocities of the imaginary wheels received from the _Wheels Commands_ block. 

In order for the step to be physically feasible, the foot position must be contained within the _workspace_ region (shown in Figure 6), defined for each foot _i_ as 


such that ow _<u>iw</u>_ ( _τ_ ) _∈Wi ∀ τ ∈_ [0; _T_ ]. Currently, the workspaces are defined to ensure that the feet do not cross each other during the gait, but they can be modified to handle other situations. 

For a feasible step, it must hold _Tsw ∈_ � _Tsw_<sup>_min_;</sup><sup>_T max_</sup> _sw_ � and _β ∈_ [ _βmin_ ; _βmax_ ] _⊂_ [0; 1]. As a consequence, it must also hold _T ∈_ [ _Tmin_ ; _Tmid_ ] _∪_ [ _Tmid_ ; _Tmax_ ], where _Tmin_ = 1 _−Tswβ_<sup>_min_</sup> _min_<sup>,</sup><sup>_Tmid_=</sup> 1 _−Tswβ_<sup>_min_</sup> _max_<sup>,and</sup><sup>_Tmax_=</sup> 1 _−Tswβ_<sup>_max_</sup> _max_<sup>.</sup> 

For a given period _T_ , a stable gait can be achieved by maximizing the support time _Tst_ = _βT_ = _T − Tsw_ , which means maximizing _β_ and minimizing _Tsw_ . On the other hand, an efficient gait (i.e., with the fewest steps) is achieved by maximizing the period _T_ . Since for Equation (28) it must hold that 


the maximum period _T_ that satisfies ow _<u>iw</u>_ ( _T_ ) _∈Wi_ is computed using the following procedure: initialize _T_ with _Tmax_ and, for each foot _i_ , compute (i) the position ow _<u>iw</u>_ ( _T_ ); (ii) the position ow _<u>iw∈</u>_<sup>(</sup><sup>_Ti_)</sup><sup>_∈Wi_closestto</sup> 

9 

ow _<u>iw</u>_ ( _T_ ), and (iii) the period candidate _Ti_ that would make the foot _i_ reach the boundaries of its workspace _Wi_ , using Equation (30). Then, _T_ is set to the minimum of all _Ti_ , and the maximum _β_ and the minimum _Tsw_ is computed to be compatible with their bounds. Such a procedure is detailed in Algorithm 1. 

**Algorithm 1** Period Computation 

- 1: _T_ := _Tmax_ 


10: **end for** 

11: _T_ := min _{Ti | i ∈{_ 1 : 4 _}}_ 


16: **end if** 

_3) Clock:_ This module provides the current time _t_ , elapsed from the beginning of the current period. It is incremented by the sampling time _Ts_ at each iteration and it is reset when _t ≥ T_ . 

_4) Gait Scheduler:_ This block decides the sequence for lifting the feet according to the commands _vfw_<sup>_⋆_,</sup> _vlw_<sup>_⋆_,and</sup><sup>_ψ_˙</sup><sup>_⋆_,thatis,itdecidesthegaitschedule</sup><sup>_γ_,as</sup> defined in Section II-B1. The schedule is then used by the _Trajectories Generator_ to compute the lift-off times according to Equation (1) (see Section IV-A5). 

The gait schedules shown in Table I are provided only for motions in a single direction, that is, for velocity commands where only one of _vfw_<sup>_⋆_,</sup><sup>_v_</sup> _lw_<sup>_⋆_, and</sup><sup>_ψ_˙</sup><sup>_⋆_is different</sup> from zero (see Table III). 

|**Motion**|_v_<sup>_⋆_</sup><br>_fw_|_v_<sup>_⋆_</sup><br>_lw_|˙_ψ_<sup>_⋆_</sup>|
|---|---|---|---|
|Forwards|_>_0|0|0|
|Backwards|_<_0|0|0|
|Leftwards|0|_>_0|0|
|Rightwards|0|_<_0|0|
|Counterclockwise|0|0|_>_0|
|Clockwise|0|0|_<_0|


TABLE III: Correspondence between motion and velocity commands. 

Therefore, it is necessary to define a criterion that generalizes the choice of the gait schedule to all possible velocity commands. The idea is to choose the gait schedule corresponding to the motion that is predominant compared to the others. 


Fig. 7: Illustration of the selection of the predominant motion: the red arrows are the velocities of the wheels, the purple angle _α_ is formed by the commanded velocity _v_<sup>_⋆_</sup> = _vfw_<sup>_⋆_</sup> _⃗_<sup>_ıs_+</sup><sup>_v_</sup> _lw_<sup>_⋆_</sup> _⃗_<sup>_ȷs_withthe</sup><sup>_x_axisofthe</sup><sup>_shadow_</sup> frame, the blue dashed lines split the sectors when gait scheduling changes. 

Referring to Figure 7, the predominant motion is determined heuristically as follows. The desired average velocity of the front imaginary wheels is compared with that of the rear wheels: if the angle between them is larger than 90 degrees, then rotation is predominant over translation, and the gait schedule for clockwise or counterclockwise motion is selected. When translation is predominant over rotation, the half-lines that start from the origin and pass through the imaginary wheels divide the plane into four sectors: a front one, one on the right, one on the back, and one on the left. The selected gait schedule is the one corresponding to that sector in which the commanded velocity vector lies. This procedure is formalized in Algorithm 2. 

Since the gait schedule always starts with _γ_ (1) = 1, the gait schedule is updated only when _t_ = 0 to avoid inconsistencies that could make the robot fall. 

_5) Trajectories Generator:_ This block computes the position <u>of</u> _w⋆_ ~~1~~ :4<sup>,velocity</sup> <u>of˙</u> _w⋆_ ~~1~~ :4<sup>,andacceleration</sup> <u>of¨</u> _w⋆_ ~~1~~ :4 references for the feet, using all the data computed by the previous blocks. Specifically, the gait schedule _γ_ is used to compute the lift-off times _t_ 0 _,_ 1:4 by Equation (1), the period _T_ , the current positions <u>ow</u> _w_ ~~1~~ :4<sup>,andthedesired</sup> velocities <u>ow</u> _w⋆_ ~~1~~ :4<sup>oftheimaginarywheels(neededto</sup> compute the footholds). 

As already mentioned in Section II-B3, after computing the footholds, it is necessary to connect them with a trajectory that lifts each foot _i_ from the ground at time _t_ 0 _,i_ , raises it to the height _h_ , and places it back on the ground at time _t_ 0 _,i_ + _Tsw_ . During the rest of the period, the foot must remain stationary. This means that, as seen in Section III-A, since each foot _i_ at time _t_ 0 _,i_ and 

10 

|**Al**|**gorithm 2** Predominant Motion|
|---|---|
||˙<br>1<br><br>˙<br><br>˙<br>|
|1:|ow_F_<br>_w_ := <br>2<br>�<br>ow1<br>_w_+<br>ow2<br>_w_<sup>�</sup><br><br><br>|
|2:|˙<br>ow_R_<br>_w_ := 1<br>2<br>�<br>˙<br>ow3<br>_w_+<br>˙<br>ow4<br>_w_<sup>�</sup><br><br>|
|3:|**if**<br>˙<br>ow_F_<br>_w ·_<br>˙<br>ow_R_<br>_w_ _≤_0 **then**|
|4:|rotation is predominant<br><sup>˙</sup>|
|5:|**if** _ψ_<sup>_⋆_</sup>_>_0 **then**|
|6:|counterclockwise motion is predominant|
|7:|**else**|
|8:|clockwise motion is predominant|
|9:|**end if**|
|10:|**else**|
|11:|translation is predominant<br><br>|
|12:|_α_:= atan2<br>�<br>_v_<sup>_⋆_</sup><br>_lw_<sup>_, v⋆_</sup><br>_fw_<br>�|
|13:|_αi_ := atan2<br>�<br>_j_<br>_⊤_kw_i_<br>_s, i_<br>_⊤_kw_i_<br>_s_<sup>�</sup><br>_∀i ∈_[1 : 4]|
|14:|**if** _α ∈_[_α_2;_α_1] **then**|
|15:|forward motion is predominant|
|16:|**else if** _α ∈_[_α_1;_α_3] **then**|
|17:|leftward motion is predominant|
|18:|**else if** _α ∈_[_α_4;_α_2] **then**|
|19:|rightward motion is predominant|
|20:|**else if** _α ∈_[_−π_;_α_4]_∪_[_α_3;_π_] **then**|
|21:|backward motion is predominant|
|22:|**end if**|
|23:|**end if**|


It can be proved that the choice of _ηi_ ( _t_ ) that satisfies Equation (37) is 


_6) Feet Controller:_ This block computes the feet accelerations <u>of¨</u> _w_ ~~1~~ :4<sup>suchthatthefeetfollowthereferences</sup> computed by the _Trajectories Generator_ block. Defining the error on the outputs of foot _i_ as of� _<u>iw</u>_ := of _<u>iw⋆</u>_<sup>_−_of</sup><sup>_<u>i</u>_</sup> _w_ , the feet are controlled to follow the desired trajectory, by imposing the following control law: 

of¨ _<u>iw</u>_ = of¨ _<u>iw⋆</u>_<sup>+</sup><sup>_kp,i_</sup> of<sup>�</sup> _<u>iw</u>_ + _kd,i_ of�˙ _<u>iw</u> ∀ i ∈{_ 1 : 4 _} ,_ (39) andwhereof˙ _kiwp,i_ are _, kd,i_ provided _∈_ R arebytunedthe _Body_ as PID _Manager_ gains,. and of _<u>iw</u>_ 

## _B. Body Reference_ 

**if** _α ∈_ [ _α_ 1; _α_ 3] **then** This block receives the high-level velocity commands leftward motion is predominant (longitudinal velocity _vfw_<sup>_⋆_,lateralvelocity</sup><sup>_v_</sup> _lw_<sup>_⋆_,yawrate</sup> **if** _α ∈_ [ _α_ 4; _α_ 2] **then** _ψ_ ˙<sup>_⋆_</sup> , height _z_<sup>_⋆_</sup> , roll _φ_<sup>_⋆_</sup> , pitch _θ_<sup>_⋆_</sup> ), and converts them rightward motion is predominant into references for the body _<u>q⋆</u>_ <u>0</u><sup>and</sup><sup>_<u>q</u>_˙</sup> _⋆_ <u>0</u><sup>,whichwillbe</sup> **if** _α ∈_ [ _−π_ ; _α_ 4] _∪_ [ _α_ 3; _π_ ] **then** forwarded to the _Body Manager_ . backward motion is predominant Since the robot oscillates while walking, the velocity **if** references are numerically integrated to obtain a position **if** reference robust to oscillations. In this way, the robot returns to the desired trajectory even if its position drifts because of the oscillations. More specifically, _ψ_<sup>_⋆_</sup> is 0 _,i_ + _Tswsw_ touches the ground, it must hold obtained by integrating _ψ_<sup>˙</sup><sup>_⋆_</sup> and og _w_ _~~⋆~~_<sup>is obtained by inte-</sup> ˙ _w_ ˙ _w_ grating <u>og˙</u> _w_ _~~⋆~~_<sup>=</sup><sup>_Rz_(</sup><sup>_ψ⋆_)</sup> � _vfw_<sup>_⋆_</sup><sup>_<u>i</u>_</sup> + _vlw_<sup>_⋆_</sup><sup>_<u>j</u>_</sup> <u>�. At this point, oz</u> _w_ _~~⋆~~_ of _<u>i⋆</u>_<sup>(</sup><sup>_t_0</sup><sup>_,i_) =</sup> of _<u>i⋆</u>_<sup>(</sup><sup>_t_0</sup><sup>_,i_+</sup><sup>_Tsw_) = 0</sup> ¨ _w w ._ (31) can be computed as a function of _<u>ϕ⋆</u>_ = � _φ⋆ θ_<sup>_⋆_</sup> _ψ_<sup>_⋆_</sup><sup><u>�</u></sup><sup>_⊤_</sup> , <u>�of</u> _<u>i⋆</u>_<sup>(</sup><sup>_t_0</sup><sup>_,i_) =</sup> of<sup>¨</sup> _<u>i⋆</u>_<sup>(</sup><sup>_t_0</sup><sup>_,i_+</sup><sup>_Tsw_) = 0</sup> _<u>ϕ</u>_ ˙ _⋆_ = �0 0 _ψ_ ˙<sup>_⋆_�</sup><sup>_⊤_</sup> and <u>og</u> _w_ _~~⋆~~_<sup>byapplyingEquation(23).</sup> normalized cycloid trajectory is chosen for foot _i_ , Since it is not certain that the computed <u>oz</u> _w_ _~~⋆~~_<sup>belongs</sup> to the Support Polygon, we compute 

at time _t_ 0 _,i_ + _Tswsw_ touches the ground, it must hold 

A normalized cycloid trajectory is chosen for foot _i_ , such that 

<u>oz</u> _w_ ~~▲~~<sup>= arg min</sup><sup>_{∥_</sup><sup><u>op</u></sup> _w −_ <u>oz</u> _w_ _~~⋆~~_<sup>_∥|_</sup><sup><u>op</u></sup> _w ∈_ P _sup}_ (40) that is the point belonging to the Support Polygon closest to <u>oz</u> _w_ _~~⋆~~_<sup>(seeFigure8).</sup> Inverting Equation (23), we compute 


which is the position of the center of mass closest to the desired <u>og</u> _w_ _~~⋆~~_<sup>thatensuresthattheZMPbelongstothe</sup> Support Polygon, i.e., that the robot is stable. Finally, _w w ⋆_ ~~▲~~ _⋆_ _~~⋆~~_ _<u>q</u>_ <u>0</u><sup>=</sup> <u>�og</u> _<u>ϕ⋆</u>_ � and _<u>q</u>_ ˙0<sup>=</sup> <u>�og</u> _<u>ϕ</u>_ ˙˙ _⋆_ � are forwarded to the _Body Manager_ . 

where 


and 


## _C. Body Manager_ 

This block receives the feet accelerations <u>of¨</u> _w_ ~~1~~ :4<sup>from</sup> the _Feet Manager_ , the body references from the _Body Reference_ , the joint positions _<u>q</u>_ 1:4<sup>and the contact signals</sup> _σ_ 1:4 from the robot’s sensors, and derives the joint velocity commands _<u>q</u>_ ˙ _⋆_ <u>1:4</u><sup>thatwillbeforwardedtothe</sup> robot’s actuators. As illustrated in Figure 9, the Body Manager comprises five blocks described below. 

For Equations (32), (33), and (34) to satisfy the constraints of Equation (31), it can be proved that it must hold 


11 


Fig. 8: Choice of z▲ when z _⋆_ is inside or outside the Support Polygon, with 4 feet on the ground. 


Fig. 9: Body manager block diagram. 

_1) Feet Kinematics:_ This block computes: the positions <u>of</u> _w_ ~~<u>1</u>~~ <u>:4</u><sup>andvelocities</sup> <u>of˙</u> _w_ ~~1~~ :4<sup>ofthefootcontact</sup> points in _<u>W</u>_ <u>,</u> needed by the _Feet Controller_ (see Section IV-A6), applying Equations (4) and (5); the positions kw _s_ ~~1~~ :4<sup>of the imaginary wheels in</sup><sup>_<u>S</u>_</sup> <u>, needed by the</u> _Wheels Commands_ block (see Section IV-A1); and the positions <u>gf0</u> ~~1~~ :4<sup>ofthefootcontactpointsin</sup><sup>_B_</sup><sup><u>0</u></sup> <u>,</u> needed by the _Constraints Matrix_ block (see Section IV-C2), applying Equation (9). 

_2) Constraints Matrix:_ This block uses the contact signals _σ_ 1:4 and the positions of the contact points gf0 ~~1~~ :4 in the frame _B_ <u>0</u> to compute the matrix _A_ , applying Equation (15), and its rank _r_ , according to Table II. This data is then forwarded to the _Thin LDQ Decomposition_ block (see Section IV-C3). 

_3) Thin LDQ Decomposition:_ This block decomposes matrix _A_<sup>_⊤_</sup> into the matrices _P_ , _L_ , _D_ , _Q_ such that _A_<sup>_⊤_</sup> = _PLDQ_ . These data are necessary for the _Body Dynamical Model_ (see Section IV-C4) and the _Body Controller_ (see Section IV-C5) to work. 

As proved by Golub and Van Loan [19, Theorem 3.2.1], for any square matrix _S ∈_ R<sup>_n×n_</sup> with rank _r_ , there exists a unique permutation matrix _P ∈{_ 0 _,_ 1 _}_<sup>_n×n_</sup> , a unique unit lower triangular matrix _L ∈_ R<sup>_n×r_</sup> , a unique unit upper triangular matrix _U ∈_ R<sup>_r×n_</sup> , and a unique diagonal matrix _D ∈_ R<sup>_r×r_</sup> such that _S_ = _PLDUP_<sup>_⊤_</sup> . This is known as _LDU Decomposition_ . Assuming that row and column indices start from 0, the matrices _P_ , _L_ , _D_ , and _U_ are computed as follows: 


for each _k_ from 0 to _r −_ 1, where _<u>{i</u>_ ~~0~~<sup>_, ..., i_</sup> _~~n~~ −_ 1<sup>_}_isthe</sup> canonical basis of R<sup>_n_</sup> . To make the decomposition robust to numerical errors, _<u>pk</u>_<sup>ischosentomaximize</sup><sup>_|d_</sup> _k_<sup>_|_.This</sup> is implemented with a nested for loop that always takes _nr −_<sup>_r_</sup><sup><u>(</u></sup><sup>_r_</sup> 2<sup>_−_1)</sup> iterations to derive _P_ , _L_ , _U_ and _D_ . This aspect is important when it comes to characterizing the predictability of the system during a real-time analysis. 

When _S_ is nonsingular, i.e., when _r_ = _n_ , the matrices _P_ , _L_ , _D_ , and _U_ are fully computed by the algorithm in Equation (42), and it holds that _S_<sup>_−_1</sup> = _PU_<sup>_−_1</sup> _D_<sup>_−_1</sup> _L_<sup>_−_1</sup> _P_<sup>_⊤_</sup> . This is useful because _U_<sup>_−_1</sup> , _L_<sup>_−_1</sup> , and _D_<sup>_−_1</sup> are much easier to compute than _S_<sup>_−_1</sup> . 

When _S_ is singular, i.e., when _r < n_ , it results in _P_ = � _Pr−_ 1 _P_ +�, _L_ = , and _U_ = � _Ur−_ 1 _U_ +�, � _LLr−_ +1� where _Pr−_ 1, _Lr−_ 1, _D_ , and _Ur−_ 1 are computed by the algorithm in Equation (42), while the columns of _P_ + are _<u>{i</u>_ ~~0~~<sup>_, ..., i_</sup> _~~n~~ −_ 1<sup>_}_∖</sup> <u>�</u> _<u>p</u>_ <u>0</u><sup>_, ..., p_</sup> _r−_ 1�, _L_ + = _P_ +<sup>_⊤SPr−_1</sup><sup>_U_</sup> _r_<sup>_−_</sup> _−_<sup>1</sup> 1<sup>_D−_1,</sup> and _U_ + = _D_<sup>_−_1</sup> _L_<sup>_<u>−</u>_</sup> _r−_<sup>1</sup> 1<sup>_P_</sup> _r_<sup>_⊤_</sup> _−_ 1<sup>_SP_+.</sup> 

As proved by Golub and Van Loan [19, Theorem 4.1.3], as a consequence of the previous result, if _S_ is symmetric, that is, _S_ = _S_<sup>_⊤_</sup> , then _U_ = _L_<sup>_⊤_</sup> and the LDU decomposition can be simplified to _S_ = _PLDL_<sup>_⊤_</sup> _P_<sup>_⊤_</sup> . This is known as _LDLT Decomposition_ . 

Let _X ∈_ R<sup>_m×n_</sup> be a matrix with rank _r ≤_ min _{m, n}_ . For the _LDLT Decomposition_ , since matrix _S_ = _XX_<sup>_⊤_</sup> is symmetric and positive definite by construction, then _XX_<sup>_⊤_</sup> = _PLDSL_<sup>_⊤_</sup> _P_<sup>_⊤_</sup> , where _P ∈{_ 0 _,_ 1 _}_<sup>_m×m_</sup> is a permutation matrix, _L ∈_ R<sup>_m×r_</sup> is a unit lower triangular matrix, and _DS ∈_ R<sup>_r×r_</sup> is a diagonal matrix. 

As proved by Golub and Van Loan [19, Theorem 5.2.3], there exists a matrix _Q ∈_ R<sup>_r×n_</sup> such that _QQ_<sup>_⊤_</sup> = _Ir_ and a matrix _D_ such that _D_<sup>2</sup> = _DS_ , for which _X_ = _PLDQ_ , in such a way that _XX_<sup>_⊤_</sup> = 

12 

_PLDQQ_<sup>_⊤_</sup> _DL_<sup>_⊤_</sup> _P_<sup>_⊤_</sup> = _PLDSL_<sup>_⊤_</sup> _P_<sup>_⊤_</sup> . It can be proved that _Q_ = _D_<sup>_−_1</sup> _L_<sup>_−_</sup> _r−_<sup>1</sup> 1<sup>_P_</sup> _r_<sup>_⊤_</sup> _−_ 1<sup>_X_.</sup> 

If we apply this results with _X_ = _A_<sup>_⊤_</sup> , we obtain the matrices _P ∈{_ 0 _,_ 1 _}_<sup>6</sup><sup>_×_6</sup> , _L ∈_ R<sup>6</sup><sup>_×r_</sup> , _D ∈_ R<sup>_r×r_</sup> , and _Q ∈_ R<sup>_r×_12</sup> such that 


This result is crucial, as it will be employed to find a solution to Equation (46). 

_4) Body Dynamical Model:_ This block internally simulates the dynamic system to be controlled, using the matrix decomposition of Equation (43) and integrating the feet acceleration commands <u>of¨</u> _w_ ~~1~~ :4<sup>incomingfrom</sup> the _Feet Manager_ block. The internal simulation allows the computation of the data necessary for the _Body Controller_ (see Section IV-C5) and _Body Reference_ (see Section IV-B) blocks to operate, and the joint velocity commands _<u>q</u>_ ˙ _⋆_ <u>1:4</u><sup>thatmaketherobotmove.Theinternal</sup> simulation is based on the internal model explained in the following paragraphs. 

From Equation (18) we derive 


From Equation (13) we derive 


Combining such results together we obtain 


where we have defined _<u>h</u>_ _~~V~~_<sup>:=</sup><sup>_<u>W</u>_</sup> 0 _~~g~~_<sup>_−_</sup> �ad<sup>_∗_</sup> _<u>V</u>_ 0 _~~w~~_ 0� _M_ g<sup>0</sup><sup>_<u>V</u>_</sup> 0 _~~w~~_ 0<sup>.</sup> We observe that ∆ _∈_ R<sup>18</sup><sup>_×_18</sup> is not invertible because rank _A_ = _r ≤_ 6 _⇒_ rank ∆= _r_ + 6 _≤_ 12 _<_ 18. However, after substituting Equation (43) into Equation (46), we derive the first derivative of the twist 


where 

Let’s combine the previously seen equations to derive a state form to be controlled: from Equation (2) we get 


From Equation (10) we get 

From Equation (7) we get 

Since the robot’s body has only _r_ controllable degrees of freedom, as explained in Section III-A1, the control inputs for the body are chosen as _<u>u</u>_ _~~V~~_<sup>:=</sup><sup>_<u>Q</u>_</sup> <u>gf</u><sup>¨</sup> 0 ~~1~~ :4<sup>_∈_R</sup><sup>_r_</sup><sup><u>,</u></sup> which are the projections of the foot accelerations in _B_ <u>0</u> into the controllable motions space. 

Hence, from Equation (47) we get 


where _<u>f V</u>_<sup>:= Λ</sup><sup>_<u>h</u>_</sup> _~~V~~_<sup>+Ψ</sup><sup>_D−_1</sup><sup>_<u>Qh</u>_</sup> ~~1~~ :4<sup>is defined. Consequently,</sup> combining Equations (51), (52), (53), and (54), we obtain the following state form 


for every _i ∈{_ 1 : 4 _}_ . Thus the vectors _<u>q</u>_ <u>0</u><sup>_∈_R6,</sup><sup>_<u>q</u>_</sup> 1:4<sup>_∈_</sup> R<sup>12</sup> , _<u>V</u>_ 0 _~~w~~_ 0<sup>_∈_R6, and</sup><sup><u>gf˙</u></sup> 0 ~~1~~ :4<sup>_∈_R12constitute the state</sup><sup>_<u>x</u>_</sup> _∈_ R<sup>36</sup> of the system, while the vectors _<u>u</u>_ _~~V~~_<sup>_∈_R</sup><sup>_r_and</sup> <u>of</u><sup>¨</sup> _w_ ~~1~~ :4<sup>_∈_</sup> R<sup>12</sup> constitute the inputs _<u>u</u> ∈_ R<sup>_r_+12</sup> of the system. _5) Body Controller:_ This block computes the control inputs _<u>u</u>_ _~~V~~_<sup>(seeEquation(54))thatmakethebodystate</sup> _<u>q</u>_ <u>0</u><sup>and</sup><sup>_<u>q</u>_˙</sup> <u>0</u><sup>(see Section IV-C4) follow the body references</sup> _<u>q⋆</u>_ <u>0</u><sup>and</sup><sup>_<u>q</u>_˙</sup> _⋆_ <u>0</u><sup>(seeSectionIV-B),i.e.,theinputsthatbring</sup> the errors � _<u>q</u>_ <u>0</u><sup>:=</sup><sup>_<u>q</u>_</sup> _⋆_ <u>0</u><sup>_−_</sup><sup>_<u>q</u>_</sup> <u>0</u><sup>and�</sup><sup>_<u>q</u>_˙</sup> <u>0</u><sup>:=</sup><sup>_<u>q</u>_˙</sup> _⋆_ <u>0</u><sup>_−_</sup><sup>_<u>q</u>_˙</sup> <u>0</u><sup>tozero.</sup> By differentiating Equation (2), we obtain 


from which, combining it with Equation (54), we derive 


Now, applying the _Feedback Linearization_ technique, we find a single control law valid for any value of _r_ : 


where _kp,_ 0 _, kd,_ 0 _∈_ R are tuned as PID gains. 

The advantages resulting from this control law make this formulation one of the key contributions of this work: (i) it is a closed-form solution, (ii) it is valid for any combination of feet contacts, (iii) it linearizes exactly a complex system like a quadruped robot, and (iv) it projects the linear control law for the pose into the controllable degrees of freedom granted by the foot contacts. 

## V. Experimental results 

This section describes the results of some experiments carried out to test the effectiveness of the proposed approach. 

13 

## _A. Implementation_ 

The framework is implemented in C++, following the architecture presented in Section IV. It does not rely on any third-party libraries to keep the implementation of Feelbert as predictable and maintainable as possible. 

To make this possible, a custom matrix calculation library called Laerte ( _Linear Algebra for Embedded Real-Time systEms_ ) has been implemented. Laerte uses only static allocation and avoids dynamic memory allocation, which is one of the main causes of temporal unpredictability in real-time systems. It optimizes the performance of Feelbert by implementing only the operations necessary for the framework to run, such as matrix addition, multiplication, inversion, and the LDU and LDQ decompositions explained in Section IV-C3. 

The proposed solution has been tested in simulation, but to obtain more significant results, the positions of the foot center points ge _<u>i</u>_ 0 (see Equation (3)), the radius of the spherical foot of Equation (4) and the dynamic parameters of Equation (18) are derived from an actual robot. The reference platform is a Unitree Go2<sup>1</sup> whose parameters are derived from the Unified Robot Description Format (URDF) file made available by the manufacturer<sup>2</sup> . 

The following values were chosen for the other parameters: for the feet workspaces, �� _xsi,min_ �� := 0 _._ 05 m, �� _yi,mins_ �� := 0 _._ 05 m, �� _xsi,max_ �� := 0 _._ 5 m, and �� _yi,maxs_ �� := 0 _._ 5 m (see Equation (29)); for the gait parameters, _Tsw_<sup>_min_</sup> := 0 _._ 2 s, _Tsw_<sup>_max_</sup> := 0 _._ 2 s, _βmin_ := 0 _._ 5, and _βmax_ := 0 _._ 8 (see Section IV-A2); for the step height, _h_ := 0 _._ 05 m (see Section IV-A5); for the feet controllers, _kp,i_ := 1000 and _kd,i_ := 110 _∀ i ∈{_ 1 : 4 _}_ (see Equation (39)); for the body controller, _kp,_ 0 := 100 and _kd,_ 0 := 21 (see Equation (58)). To validate the control framework, Feelbert is tested on a quadruped robot modeled by the kinematic and dynamic equations described in Section III, simulating the signals from the robot: joint angles _<u>q</u>_ 1:4<sup>areobtained</sup> by numerically integrating the joint velocity commands _<u>q</u>_ ˙ _⋆_ <u>1:4</u><sup>;thefootcontactsignalsareobtainedbyassuming</sup> that each foot _i_ is in contact with the ground when the foot contact point f _i_ is below a certain height, that is, _σi_ := <u>�</u> _<u>k⊤</u>_ of _<u>iw</u> ≤_ 5 _·_ 10 _−_ 3<sup>�</sup> . 

## _B. Controller performance test_ 

To test Feelbert’s ability to follow a general reference, the robot was commanded to follow the reference trajectory illustrated in Figure 10, which was designed to cover all possible command combinations. 

Initially, starting from the center, the robot must raise and lower itself on the spot (control of _z_ ), also raising and lowering the nose (control of _θ_ ) and the 

> 1https://www.unitree.com/go2 

> 2https://github.com/unitreerobotics/unitree ros/blob/master/robots/go2 description/urdf/go2 description.urdf 

sides (control of _φ_ ); then, it must move to the front-left vertex of the rectangle and traverse the entire perimeter without rotating on itself (control of _vfw_ and _vlw_ ); then, it must rotate on the spot (control of _ψ_<sup>˙</sup> ); then, traverse a semicircular section while rotating on itself without lowering or inclining (control of _vfw_ , _vlw_ and _ψ_<sup>˙</sup> ); after that, it must traverse two diagonal sections while raising, lowering, and rotating on itself (control of _vfw_ , _vlw_ , _ψ_<sup>˙</sup> and _z_ ), a semicircular section in which it lowers while inclining nose and sides, and finally it must return to the starting position and orientation (control of _vfw_ , _vlw_ , _ψ_<sup>˙</sup> , _z_ , _φ_ and _θ_ ). 

To test the behavior of the controller at different speeds, the trajectory is traversed slowly (0.2 m/s) in a first experiment and quickly (1 m/s) in a second experiment. The reference trajectory described above is translated into a sequence of commands, that is, _z_<sup>_⋆_</sup> , _φ_<sup>_⋆_</sup> , _θ_<sup>_⋆_</sup> , _vfw_<sup>_⋆_,</sup><sup>_v_</sup> _lw_<sup>_⋆_,and</sup><sup>_ψ_˙</sup><sup>_⋆_,thataresenttoFeelbertbyan</sup> external test module that mimics the behavior of a user or a high-level planner. 

Feelbert was integrated into a ROS 2 node, to prove its compatibility with the most common robotic frameworks, and also to visualize the data computed internally during the experiments. The node includes two ROS timers: one at a frequency of 100 Hz that runs the framework, and one at a frequency of 20 Hz that publishes the data necessary to animate the robot. The published data are then displayed in RViz, the 3D visualization tool for ROS 2. 

To easily monitor the progress on RViz, these experiments were conducted on a desktop computer with an Intel® Core™i9-9900 CPU @ 3.10GHz (16 cores), 32 GB of RAM, and an NVIDIA GeForce RTX 2080 SUPER GPU, running Ubuntu 22.04 LTS and ROS 2 Humble. 

Figures 11, 12, and 13 show the results of the first experiment in which the trajectory is traversed slowly, i.e., with a maximum linear speed of 0.2 m/s and a maximum angular speed of 0.15 _π_ rad/s. The plots in Figures 11 and 12 show how the values of _x_ , _y_ , _z_ , _φ_ , _θ_ , and _ψ_ closely follow their references, except for some oscillation on _z_ , _φ_ and _θ_ , which is probably due to the gait schedule chosen for that particular combination of commands. From the experimental data, it can be observed that: the planar position errors _x_ � and _y_ � are below 2 cm; the height error _z_ � is generally below 1 cm, with two peaks of around 4 cm; the orientation errors _φ_ �, _θ_<sup>�</sup> and _ψ_<sup>�</sup> are generally below 0.005 _π_ rad, apart from some peaks of less than 0.1 _π_ rad on _θ_<sup>�</sup> . The plots in Figure 13 show how the values of _vfw_ , _vlw_ , and _ψ_<sup>˙</sup> oscillate around the references _vfw_<sup>_⋆_,</sup><sup>_v_</sup> _lw_<sup>_⋆_,</sup> and _ψ_<sup>˙</sup><sup>_⋆_</sup> . The oscillations around the reference values in this case are due to the fact that the robot, in lifting and landing its feet, creates discontinuities in the model (see Section IV-C4) and periodically shifts the Support Polygon and then the position of the safe reference for the center of mass og _w_ ~~▲~~<sup>(see Section IV-B). These values</sup> 

14 


Fig. 10: Trajectories used for the two experiments executed at low speed (a) and high speed (b), respectively. The green curve indicates the reference path, while the red curve indicates the <u>path</u> actually traversed by the robot. The arrows indicate the projections of the unit vector of axis _x_ 0 of frame _B_ <u>0</u> onto the plane, to show _ψ_ values. 


Fig. 11: Time plots of the actual coordinates of the center of mass (red) tracking their corresponding references (green), during the first experiment where the trajectory is traversed slowly. 


Fig. 12: Time plots of the actual Euler angles of the body (red) tracking their corresponding references (green), during the first experiment where the trajectory is traversed slowly. 

influence the computation of _vfw_ and _vlw_ . Furthermore, from the experimental data it can be observed that, since the velocity references are step inputs, every time the reference changes, there is an impulsive peak in the error due to the reference change and the tracking delay, with a magnitude equal to the step height. In 

fact, where the references vary continuously, no error impulses are observed. Therefore, it can be concluded that for low speeds, the performances of Feelbert are satisfactory in the control of all six degrees of freedom of the quadruped’s body. 

15 


Fig. 13: Time plots of the actual velocities of the body (red) tracking their corresponding references (green), during the first experiment where the trajectory is traversed slowly. 

Figures 14, 15, and 16 show the results of the second experiment in which the trajectory is traversed more quickly, that is, with linear speeds up to 1 m/s and angular speeds up to 0.75 _π_ rad/s. The plots in Figures 14 


Fig. 14: Time plots of the actual coordinates of the center of mass (red) tracking their corresponding references (green), during the second experiment where the trajectory is traversed quickly. 

and 15 show how the values of _x_ , _y_ and _ψ_ still follow the references _x_<sup>_⋆_</sup> , _y_<sup>_⋆_</sup> and _ψ_<sup>_⋆_</sup> quite closely, while the values of _φ_ and _θ_ oscillate considerably around their references _φ_<sup>_⋆_</sup> and _θ_<sup>_⋆_</sup> . Also, the value of _z_ struggles in following its reference _z_<sup>_⋆_</sup> . This is due to the fact that, to increase speed, the _Period_ block decreases the duty factor _β_ , as explained in Section IV-A2. When _β ≤_ 0 _._ 75, there are moments in which the robot has less than 3 grounded feet and becomes unstable due to gravity, as explained in Section III-A1. From the experimental data, it can be observed that: the planar position errors _x_ � and _y_ � are below 5 cm, while the height error � _z_ can reach peaks of 10 


Fig. 15: Time plots of the actual Euler angles of the body (red) tracking their corresponding references (green), during the second experiment where the trajectory is traversed quickly. 


Fig. 16: Time plots of the actual velocities of the body (red) tracking their corresponding references (green), during the second experiment where the trajectory is traversed quickly. 

cm, and the inclination errors _φ_ � and _θ_<sup>�</sup> can reach peaks of 0.1 _π_ rad. Regarding the velocities, from Figure 16 it can be observed that the situation is not very different from the one of the first experiment, for the same reasons. 

Overall, this second experiment demonstrates that, when the robot is running, Feelbert manages to make the robot always follow the high-level velocity commands, sacrificing the performance of the other commands, that is, the height and inclination of the body. This is possible because the LDQ decomposition naturally filters out uncontrollable motions, which, due to gravity, coincide with those involving height and inclination of the body. Hence, it can be concluded that, for high speeds, the performance of Feelbert is satisfactory in controlling the three main planar degrees of freedom of the quadruped’s body, namely _x_ , _y_ , and 

16 

## _ψ_ . 

## _C. Execution times test_ 

To verify the timing predictability of Feelbert on an embedded system, timing experiments were conducted on a Raspberry Pi 5, including a quad-core ARM CortexA76 64-bit processor, clocked at 2.4 GHz, and 16 GB of RAM, running Ubuntu 24.04 LTS. To perform these experiments, Feelbert was compiled into a separate C++ program, outside ROS 2. To measure execution times as precisely as possible, the program was executed as an isolated task on a single core of the computer with maximum priority for the Linux scheduler, to prevent operating system tasks from interfering with the task executing Feelbert. To collect a significant number of measurements of the execution times for a single job, both experiments from Section V-B were repeated, for a total of 23085 samples. 

Figure 17 shows the distribution of the execution times of the task that executes Feelbert. In particular, the upper plot reports the overall distribution, while the other plots show the distribution when a different number _N_ of feet are in contact with the ground. 


Fig. 17: Execution times distributions of the task that implements Feelbert when a different number _N_ of feet are in contact with the ground. 

Most execution times are concentrated between 950 _µ_ s and 970 _µ_ s, when the robot has 3 or 4 grounded feet, and between 780 _µ_ s and 800 _µ_ s, when the robot has 2 grounded feet. When the robot has 2 grounded feet, the rank _r_ of the matrix _A_ is lower compared to when the robot has 3 or 4 grounded feet, and therefore the LDQ decomposition requires fewer iterations to terminate (see Section IV-C3). Additionally, when the robot has 2 grounded feet, the Support Polygon reduces to a segment, making it much faster to find the safe reference for the center of mass compared to when the robot has 3 or 4 grounded feet, where the Support Polygon is a triangle or a quadrilateral (see Section IV-B). Moreover, 

the algorithm that solves Equation (40), in the case of 3 or 4 grounded feet, is implemented with a for loop containing a break, and this can influence the execution times, which are maximal when the desired ZMP is inside the Support Polygon. 

Figure 17 shows also that the execution times for each number of legs are distributed with a seemingly unimodal probability density and a very low standard deviation. In fact, the tails in the histograms are essentially invisible. This makes the execution time measurements highly reliable and predictable, and therefore suitable for a real-time system. Furthermore, the worstcase execution time (WCET) is approximately 1030 _µ_ s when there are 3 or 4 grounded feet, and approximately 820 _µ_ s when there are 2 grounded feet. These data are crucial when scheduling tasks in a real-time system, as they allow the analysis to be performed with a low pessimism, hence, allowing to enforce timing guarantees without wasting computational resources. 

## VI. Conclusions 

This paper presented Feelbert, a predictable framework for quadruped locomotion designed for embedded systems with hard real-time execution constraints. 

Feelbert’s predictability comes from the utilization of a novel closed-form control law for the body, that leverages feedback linearization, which is applied for the first time to control a quadruped robot. 

Applying feedback linearization required the definition of an appropriate model for the body, enabling the system to be linearized in closed loop and inequality constraints to be transformed into references. The model utilizes the LDQ matrix decomposition, which overcomes the under-actuation problem of quadruped robots and the loss of stability during walking, reflected in the loss of rank of the constraint matrix. The LDQ matrix decomposition employs an algorithm that requires a fixed known number of iterations to complete, making the framework suitable for real-time execution. Additional improvements have also been introduced in foot motion planning to make Feelbert responsive to sudden variations in high-level input commands while maintaining accuracy and predictability. 

The experiments presented in Section V demonstrate that Feelbert is capable of following high-level commands regardless of speed, adapting the gait to the situation. Furthermore, it can be executed on an embedded system with bounded computation times. 

As a future work, we aim to extend the _Feet Manager_ and the _Body Reference_ blocks to enable the quadruped robot to handle generic uneven terrains, while always maintaining predictability. In addition, we intend to use Feelbert on one or more physical quadruped robots to demonstrate the validity of the framework in a real-world context. 

17 

## References 

- [1] C. Tang, F. Xu, and F. Zou, “A stable trot strategy of quadruped robot based on capture point,” in _2017 IEEE 7th Annual International Conference on CYBER Technology in Automation, Control, and Intelligent Systems (CYBER)_ , pp. 427–431, IEEE, 2017. 

- [2] T. Akbas, S. E. Eskimez, S. Ozel, O. K. Adak, K. C. Fidan, and K. Erbatur, “Zero moment point based pace reference generation for quadruped robots via preview control,” in _2012 12th IEEE International Workshop on Advanced Motion Control (AMC)_ , pp. 1–7, IEEE, 2012. 

- [3] F. Farshidian, M. Neunert, A. W. Winkler, G. Rey, and J. Buchli, “An efficient optimal planning and control framework for quadrupedal locomotion,” in _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 93–100, IEEE, 2017. 

- [4] J. Norby, Y. Yang, A. Tajbakhsh, J. Ren, J. K. Yim, A. Stutt, Q. Yu, N. Flowers, and A. M. Johnson, “Quad-sdk: Full stack software framework for agile quadrupedal locomotion,” in _ICRA Workshop on Legged Robots_ , 2022. 

- [5] Y. Ding, A. Pandala, C. Li, Y.-H. Shin, and H.-W. Park, “Representation-free model predictive control for dynamic motions in quadrupeds,” _IEEE Transactions on Robotics_ , vol. 37, no. 4, pp. 1154–1171, 2021. 

- [6] Y. Ding, A. Pandala, and H.-W. Park, “Real-time model predictive control for versatile dynamic motions in quadrupedal robots,” in _2019 International Conference on Robotics and Automation (ICRA)_ , pp. 8484–8490, IEEE, 2019. 

- [7] K. A. Hamed, J. Kim, and A. Pandala, “Quadrupedal locomotion via event-based predictive control and qp-based virtual constraints,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 3, pp. 4463–4470, 2020. 

- [8] F. Risbourg, T. Corb`eres, P.-A. L´eziart, T. Flayols, N. Mansard, and S. Tonneau, “Real-time footstep planning and control of the solo quadruped robot in 3d environments,” in _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 12950–12956, IEEE, 2022. 

- [9] G. Raiola, E. Mingo Hoffman, M. Focchi, N. Tsagarakis, and C. Semini, “A simple yet effective whole-body locomotion framework for quadruped robots,” _Frontiers in Robotics and AI_ , vol. 7, p. 528473, 2020. 

- [10] C. D. Bellicoso, F. Jenelten, P. Fankhauser, C. Gehring, J. Hwangbo, and M. Hutter, “Dynamic locomotion and wholebody control for quadrupedal robots,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 3359–3365, IEEE, 2017. 

- [11] J. Li, H. Gao, Y. Wan, H. Yu, and C. Zhou, “A real-time planning and control framework for robust and dynamic quadrupedal locomotion,” _Journal of Bionic Engineering_ , vol. 20, no. 4, pp. 1449–1466, 2023. 

- [12] V. Barasuol, J. Buchli, C. Semini, M. Frigerio, E. R. De Pieri, and D. G. Caldwell, “A reactive controller framework for quadrupedal locomotion on challenging terrain,” in _2013 IEEE International Conference on Robotics and Automation_ , pp. 2554–2561, IEEE, 2013. 

- [13] X. Zhang, Z. Xiao, Q. Zhang, and W. Pan, “Synloco: Synthesizing central pattern generator and reinforcement learning for quadruped locomotion,” _arXiv preprint arXiv:2310.06606_ , 2023. 

- [14] W. Tan, X. Fang, W. Zhang, R. Song, T. Chen, Y. Zheng, and Y. Li, “A hierarchical framework for quadruped locomotion based on reinforcement learning,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 8462–8468, IEEE, 2021. 

- [15] R. T. Fawcett, A. Pandala, J. Kim, and K. Akbari Hamed, “Real-time planning and nonlinear control for quadrupedal locomotion with articulated tails,” _Journal of Dynamic Systems, Measurement, and Control_ , vol. 143, no. 7, p. 071004, 2021. 

- [16] S. Fahmi, C. Mastalli, M. Focchi, and C. Semini, “Passive whole-body control for quadruped robots: Experimental validation over challenging terrain,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 3, pp. 2553–2560, 2019. 

- [17] C. Mastalli, I. Havoutis, M. Focchi, D. G. Caldwell, and C. Semini, “Motion planning for quadrupedal locomotion: Coupled planning, terrain mapping, and whole-body control,” _IEEE Transactions on Robotics_ , vol. 36, no. 6, pp. 1635–1648, 2020. 

- [18] N. Rathod, A. Bratta, M. Focchi, M. Zanon, O. Villarreal, C. Semini, and A. Bemporad, “Model predictive control with environment adaptation for legged locomotion,” _IEEE Access_ , vol. 9, pp. 145710–145727, 2021. 

- [19] G. H. Golub and C. F. Van Loan, _Matrix computations_ . JHU press, 2013. 

- [20] Y. Shi, S. Li, M. Guo, Y. Yang, D. Xia, and X. Luo, “Structural design, simulation and experiment of quadruped robot,” _Applied Sciences_ , vol. 11, no. 22, p. 10705, 2021. 

- [21] S. Kajita and B. Espiau, “Legged robot,” in _Springer handbook of robotics_ , pp. 361–389, Springer Berlin/Heidelberg, Germany, 2008. 

- [22] J. Di Carlo, P. M. Wensing, B. Katz, G. Bledt, and S. Kim, “Dynamic locomotion in the mit cheetah 3 through convex model-predictive control,” in _2018 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pp. 1–9, IEEE, 2018. 

- [23] W. Chi, X. Jiang, and Y. Zheng, “A linearization of centroidal dynamics for the model-predictive control of quadruped robots,” in _2022 International Conference on Robotics and Automation (ICRA)_ , pp. 4656–4663, IEEE, 2022. 

- [24] F. Farshidian, E. Jelavic, A. Satapathy, M. Giftthaler, and J. Buchli, “Real-time motion planning of legged robots: A model predictive control approach,” in _2017 IEEE-RAS 17th International Conference on Humanoid Robotics (Humanoids)_ , pp. 577–584, IEEE, 2017. 

- [25] J. Buchli, M. Kalakrishnan, M. Mistry, P. Pastor, and S. Schaal, “Compliant quadruped locomotion over rough terrain,” in _2009 IEEE/RSJ international conference on Intelligent robots and systems_ , pp. 814–820, IEEE, 2009. 

- [26] F. Farshidian, E. Jelavi´c, A. W. Winkler, and J. Buchli, “Robust whole-body motion control of legged robots,” in _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 4589–4596, IEEE, 2017. 

- [27] H. Chai, Y. Li, R. Song, G. Zhang, Q. Zhang, S. Liu, J. Hou, Y. Xin, M. Yuan, G. Zhang, _et al._ , “A survey of the development of quadruped robots: Joint configuration, dynamic locomotion control method and mobile manipulation approach,” _Biomimetic Intelligence and Robotics_ , vol. 2, no. 1, p. 100029, 2022. 

- [28] H. Igarashi, T. Machida, F. Harashima, and M. Kakikura, “Free gait for quadruped robots with posture control,” in _9th IEEE International Workshop on Advanced Motion Control, 2006._ , pp. 433–438, IEEE, 2006. 

- [29] M. Hutter, H. Sommer, C. Gehring, M. Hoepflinger, M. Bloesch, and R. Siegwart, “Quadrupedal locomotion using hierarchical operational space control,” _The International Journal of Robotics Research_ , vol. 33, no. 8, pp. 1047–1062, 2014. 

- [30] K. Gogineni, S. S. Dayapule, J. G´omez-Luna, K. Gogineni, P. Wei, T.-S. Lan, M. Sadrosadati, O. Mutlu, and G. Venkataramani, “Swiftrl: Towards efficient reinforcement learning on real processing-in-memory systems,” _2024 IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS)_ , pp. 217–229, 2024. 

- [31] S. S. Sahoo, A. R. Baranwal, S. Ullah, and A. Kumar, “Memorel: A memory-oriented optimization approach to reinforcement learning on fpga-based embedded systems,” _Proceedings of the 2021 Great Lakes Symposium on VLSI_ , 2021. 

- [32] M. Li, A. Li, Y.-J. Huang, and S. Chu, “Implementation of deep reinforcement learning,” _Proceedings of the 2nd International Conference on Information Science and Systems_ , 2019. 

- [33] A. R. Baranwal, S. Ullah, S. S. Sahoo, and A. Kumar, “Relaccs: A multilevel approach to accelerator design for reinforcement learning on fpga-based systems,” _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , vol. 40, pp. 1754–1767, 2021. 

- [34] M. H. Raibert, _Legged robots that balance_ . MIT press, 1986. 

