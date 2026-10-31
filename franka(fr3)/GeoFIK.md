---
title: "GeoFIK: A Fast and Reliable Geometric Solver for the IK of the Franka Arm based on Screw Theory Enabling Multiple Redundancy Parameters"
date: "2025-03-06"
authors: "Pablo C. Lopez-Custodio; Yuhe Gong; Luis F. C. Figueredo"
url: https://arxiv.org/abs/2503.03992
pdf: https://arxiv.org/pdf/2503.03992
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.03992)** / [論文ページ](https://arxiv.org/abs/2503.03992)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM BASED ON SCREW THEORY ENABLING MULTIPLE REDUNDANCY PARAMETERS 

PREPRINT 

**Pablo C. Lopez-Custodio**<sup>1</sup><sup>_∗_</sup> **, Yuhe Gong**<sup>2</sup><sup>_†_</sup> **, and Luis F.C. Figueredo**<sup>2,3</sup><sup>_‡_</sup> 

1Department of Computer Science, Nottingham Trent University 

2School of Computer Science, University of Nottingham 

3Munich Institute of Robotics and Machine Intelligence (MIRMI), Technical University of Munich (TUM) 

> 1* `custodio825@gmail.com` , † `yuhe.gong@nottingham.ac.uk` , ‡ `figueredo@ieee.org` 

## **ABSTRACT** 

Modern robotics applications require an inverse kinematics (IK) solver that is fast, robust and consistent, and that provides all possible solutions. Currently, the Franka robot arm is the most widely used manipulator in robotics research. With 7 DOFs, the IK of this robot is not only complex due to its redundancy, but also due to the link offsets at the wrist and elbow. Due to this complexity, none of the Franka IK solvers available in the literature provide satisfactory results when used in real-world applications. Therefore, in this paper we introduce GeoFIK (Geometric Franka IK), an analytical IK solver that allows the use of different joint variables to resolve the redundancy. The approach uses screw theory to describe the entire geometry of the robot, computing the Jacobian matrix prior to the joint angles. All singularities are handled. As an example of how the geometric elements obtained by the IK can be exploited, a solver with the swivel angle as the free variable is provided. Several experiments are carried out to validate the speed, robustness, and reliability of GeoFIK against three state-of-the-art solvers. The C++ code for GeoFIK is available at `https://github.com/ PabloLopezCustodio/GeoFIK` 

## 1 INTRODUCTION 

Inverse kinematics (IK) plays a pivotal role in robotics, bridging task-space goals with joint-space feasibility, execution, and performance. It is the core element of a wide range of tasks, from simple pick-and-place, grasping, and collision avoidance [5, 27] to highly dynamic task-and-motion planning, high-DoF planning, safety [21, 14] and even biomechanics [12]. Unlike forward kinematics, finding IK solutions is challenging due to the non-linearity of the equations and the branching of its solutions. While the IK of 6-DOF manipulators can have up to 16 solutions [26], the problem is more complex for redundant robots, such as 7-DOF arms, as they have infinitely many solutions organized along a continuous one-parameter manifold (self-motion) [4]. 

Standard 7-DOF manipulators designed with spherical wrist and shoulder, offer trivial kinematics which allows for simple redundancy resolution. This is however not the case for the most widely used manipulator in robotics research of today [15, 13, 6, 24, 10, 11, 22], the Franka Research Robot. This manipulator features an unconventional topology with joint offsets at the wrist and elbow that break the symmetry exploited by traditional solvers. Indeed, despite the excellent work within the robotics community (e.g. tailored tools including [31, 13, 6, 24, 10]) a fundamental piece is missing: a fast, robust and reliable multi-parametrization analytical IK solver. 

In this context, this work presents the first IK solution for the Franka Robot based on screw theory. To address the challenges and the wide range of applications required to improve stateof-the-art methods and systems, [21, 14, 12], our design choice 

aimed to satisfy the following conditions: The IK solver should **(i)** be _faster and more robust_ than any other solution, leading to solutions overlooked by other analytical methods; **(ii)** be _more reliable_ , ensuring always finding a solution if one exists; **(iii)** return solutions even in _extreme singular poses_ where other approaches fail; **(iv)** _return Jacobians_ at no extra cost; **(v)** explore _multiple free parameters_ (beyond standard _q_ 7), thus revealing more valid configurations than existing alternatives, including **(vi)** using the _swivel-angle_ [20]. Obtaining the Jacobian from the IK without committing to joint angles is useful for lazyplanning strategies, dynamic and static trajectory optimization, and geometric pullbacks. 

The Franka robot arm has firmly established itself as a reference in robotics research, with a breadth of studies showing its versatility in both industrial and academic settings. Recent surveys have shown that more than 4700 papers from leading venues such as IEEE ICRA, RA-L, T-RO, IROS, CoRL, and RSS have been using the system with a majority of the work (33 %) focused on AI and ML.<sup>4</sup> It is also estimated that 90 % and 100 % of the top 10 US and EU institutions in Computer Science have the system in their labs [15]. The success of the Franka is mostly due to its tactile and compliance capabilities as well as increased safety capabilities, including a lower effective mass at its end-effector. See [19] for a comparison with other systems. As highlighted in [15, 19], achieving a safer design came with a cost, an offset at the wrist and at the elbow, which makes its IK more complex than existing systems, e.g., 7-DOF KUKA arm whose wrist, elbow and shoulder are spherical. 

> 4Manually verified papers containing keywords _Franka robot, Emika, Panda {arm, gripper, manipulator, cobot, robot}, or 7 DoF Panda_ , 2017–23 [15]. 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

2 


Figure 1: Home configuration of the Franka arm with _qi_ = 0, _i_ = 1 _, . . . ,_ 7, and detail of the end-effector frames. Note that both frames 8 and _E_ are rigidly attached to the gripper. 

This complex topology (Fig. 1) reduces the effective mass, critical for safety [21, 19], but introduces additional challenges for analytical and geometric analysis. This challenge is reflected in the scarce number of analytical solvers for the IK of the Franka.<sup>5</sup> Indeed, up to today, only four methods were capable to derive an analytical IK, [30, 32, 18, 16]. Among these, the exceptional work by He and Liu [16] is the only complete and functional one. It is available as a C++ application [17]. However, all these publications limit the free parameter to the last joint, _q_ 7, which leads to an easier yet less robust analysis. To the best of our knowledge, no geometric solvers with other joint variables as free variable have been presented for the specific case of the Franka. Analytical solutions can be obtained from IKFast [7], which precomputes algebraic expressions to automatically generate a solver. The method is general, but this comes at the cost of lacking geometric insight, being slower than geometric methods, and instability in singularity handling. The lack of geometric insight prevents the user from extracting geometric information needed in certain applications. Another option to obtain analytical solutions is to use a solver for general 6-DOF robots (e.g. [25, 9]) after one of the joints has been locked. However, this involves the definition of a new kinematic structure every time the value of the locked joint is fixed which results in additional computational time. These changes in the topology of the 6-DOF robot can also lead to unexpected behavior as we show in Sec. 8. Finally, being able to use a 6- DOF solver for the Franka involves the development of a considerable amount of code and requires non-trivial knowledge of the robot’s kinematics. 

### _1.1 Contributions_ 

Motivated by these gaps, this paper introduces **GeoFIK** ( **Geo** metric **F** ranka **IK** ), a novel solver that allows exploring 

> 5The IK can always be computed numerically by means of the _differential IK_ using gradient-descent [29]. However, this strategy is hundred-to-thousand-fold slower and leads to a single solution. 

free parameters (rather than only locking _q_ 7) while robustly handling singularities, maximizing available solutions, and offering explicit Jacobian computation at no extra cost. 

In contrast to existing methods, including [16, 30, 7], which find individual expressions for the joint angles, our method explores the whole geometry of the robot, finding first all the screw axes. Hence, the Jacobian matrix can be returned as a byproduct. Then, the joint angles are systematically computed using the exponential and logarithmic maps of the special orthogonal group, SO(3). Due to the use of screw theory, singularities are easily identified and handled. To our knowledge, no other IK solver for redundant manipulators works on finding the screw axes, although this is often done for mechanisms and parallel robots [23]. 

As an example of the extraction of geometric information before joint angle calculation, a fast numerical IK solver with the swivel angle as a free variable is presented. The _swivel angle_ is roughly defined as an angle between the arm plane and a reference plane, providing a sense of posture [20]. We demonstrate how such solver allows to preserve flexibility, guaranteeing solutions even for poses that break joint-lock-based strategies, improving robustness. 

We thoroughly compare the performance of our method against an analytical solver specifically designed for the Franka, the HeLiu solver [16]; a general analytical solver, IKFast [7]; and a 6-DOF state-of-the-art solver, IKGeo [9]. HeLiu is the goto solver for the analytical IK of the Franka, e.g. it is currently used in the MuJoCo Playground [34]. Due to its effectiveness and generality, IKFast remains one of the most used solvers. It is, for example, the analytical solver for the popular framework MoveIt! [2]. Hence, both solvers represent valuable baselines. We illustrate that GeoFIK outperforms existing methods in terms of reliability, robustness, and speed (particularly, when computing the Jacobian and joints). Furthermore, we show scenarios at singular configurations where other solvers fail. With real-world experiments, we also show that joint-lock-based techniques inevitably falter in discovering valid poses even for predictably easier scenarios in the middle of the robot’s workspac, whereas our solver with swivel-angle as free variable consistently finds solutions and remains computationally efficient. 

This paper is organized as follows: Sec. 2 introduces the problem statement and general method; Secs. 3 to 6 present the solutions locking _q_ 7, _q_ 6, _q_ 4 and swivel angle, respectively; Sec. 7 discusses singularity handling; Sec. 8 provides comparisons with baselines; Sec. 9 shows a real-world experiment; and conclusions are drawn in Sec. 10. 

## 2 PROBLEM FORMULATION AND METHOD DESCRIPTION 

This section defines our IK problem, and outlines our screwtheory-based approach.<sup>6</sup> 

> 6Fig. 1 shows the frames and DH parameters of the Franka arm. We use the frame _E_ as end-effector frame. When the gripper is connected, _E_ matches the frame `panda_hand_tcp` in Franka Description [1]. We rename the centre of the shoulder as _S_ . 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

3 

**Problem Definition** : Given a desired pose of the end-effector frame<sup>7</sup> _E_ w.r.t. the base frame _O_ defined by<sup>_O_</sup> **r** _E/O∈_ R<sup>3</sup> and _OE_<sup>**R**</sup><sup>_∈_SO(3) the goal is to find a set of joint-angles</sup><sup>_qi∈_S,with</sup> _i_ =1 _, . . .,_ 7 that leads to the desired pose of frame _E_ . 

**Algorithm 1:** Calculating the joint angles _qi_ from the directions of the joint axes<sup>_O_</sup> ˆ **s** _i_ , _i_ = 1 _, . . . ,_ 7 **Input:**<sup>_O_</sup> ˆ **s** _i,_ 0,<sup>_O_</sup> ˆ **s** _i_ , _i_ = 1 _, . . . ,_ 7 _,_<sup>_O_</sup> ˆ **ı** _E_ **Output:** _q_ 1 _, . . . , q_ 7 **1 u** ˆ _i ←_<sup>_O_</sup> ˆ **s** _i,_ 0, _i_ = 1 _, . . . ,_ 7, **u** ˆ8 _←_ ( _~~√~~_ 2 _/_ 2 _,_ _~~√~~_ 2 _/_ 2 _,_ 0)<sup>_⊤_</sup> **2 g** ˆ _i ←_<sup>_O_</sup> ˆ **s** _i_ , _i_ = 1 _, . . . ,_ 7, **g** ˆ8 _←_<sup>_O_</sup> ˆ **ı** _E_ **3 for** _j ←_ 1 to 7 **do 4** _qj ←_ atan2�(ˆ **u** _j_ +1 _×_ ˆ **g** _j_ +1) _·_ ˆ **u** _j,_ **u** ˆ _j_ +1 _·_ ˆ **g** _j_ +1� **5** <u>�</u> **u** ˆ _j_ +1 _, . . ._ ˆ **u** 8� _←_ exp <u>�</u> _qj_ ˆ **u** _j_ <u>��</u> **u** ˆ _j_ +1 _, . . ._ ˆ **u** 8� 

Given the 1-DOF redundancy, one additional constraint must be **1** provided. We provide solutions that use _q_ 4 _, q_ 6 _, q_ 7, or the swivel **2** angle to resolve this redundancy. No _q_ 5 solver is provided since **3** it is geometrically the most complex and will be researched in **4** future work. **5** 

**Screw Theory-based IK Solution:** Unlike traditional IK solvers that rely on purely algebraic formulations, our approach uses screw theory, offering a geometric perspective on the solution. The method is based on determining the screw axes of the manipulator<sup>_O_</sup> **S** _i_ = (<sup>_O_</sup> ˆ **s** _i_ ;<sup>_O_</sup> **r** _i ×_<sup>_O_</sup> ˆ **s** _i_ ) _, i_ = 1 _, . . . ,_ 7, where _O_ ˆ **s** _i_ is the direction of the axis, and _O_ **r** _i_ is the position of _any_ point along the axis. By using this formulation, the **Jacobian** can be computed = even without prior knowledge of joint angles as **J** Adj( **I** 3 _, −_<sup>_O_</sup> **r** _E/O_ )� _O_ **S** 1 _, . . . , O_ **S** 7�, where Adj( _·, ·_ ) is the adjoint representation of an element of SE(3) defined by a pair in SO(3) _×_ R<sup>3</sup> , see [28, Sec. 4.2]. 

## 3 SOLUTION LOCKING JOINT 7 

It can be seen that<sup>_O_</sup> ˆ **s** 6 = exp �(<sup><u>3</u></sup> 4<sup>_π −q_7</sup> � _O_ ˆ **s** 7) _O_ ˆ **ı** _E_ and _O_ **r** 6 = _O_ **r** _O_ 6 _/O_ = _O_ **r** _O_ 7 _/O − a_ 7 _O_ ˆ **s** 6 _× O_ ˆ **s** 7. 

Consider<sup>_O_</sup> **r** _O_ 6 _<u>/S</u>_ =<sup>_O_</sup> **r** _O_ 6 _<u>/S</u> −_<sup>_O_</sup> **r** _S/O_ and let _l_ := _|_<sup>_O_</sup> **r** _O_ 6 _/S|_ , _b_ 1 := ~~�~~ _d_<sup>2</sup> 3<sup>+</sup><sup>_a_</sup> 4<sup>2,</sup><sup>_b_2:=</sup> ~~�~~ _d_<sup>2</sup> 5<sup>+</sup><sup>_a_</sup> 5<sup>2,</sup><sup>_ρ_1:=arctan(</sup><sup>_a_4</sup><sup>_/d_3) and</sup> _ρ_ 2 := arctan( _a_ 5 _/d_ 5) in Fig. 2, then: 


We first exploit the spherical shoulder joint structure of the Franka, and hence we first find screw-axes<sup>_O_</sup> **S** 4,<sup>_O_</sup> **S** 5, and<sup>_O_</sup> **S** 6. The axis of the last joint,<sup>_O_</sup> **S** 7, is fully determined by the input, i.e.,<sup>_O_</sup> ˆ **s** 7 =<sup>_O_</sup> **k**<sup>ˆ</sup> _E_ and<sup>_O_</sup> **r** 7 =<sup>_O_</sup> r _E/O_ . 

These two solutions correspond to the elbow-up and elbowdown assemblies of triangle _SO_ 4 _O_ 6. However, as noted in [16], due to link interference, solution 2 only happens when _SO_ 4 _O_ 6 is almost flat and _d_ 3 + _d_ 5 _< l < b_ 1 + _b_ 2, Fig. 8 shows one of such scenarios. 

Once those are known, the spherical shoulder is solved as 


Define a frame _C_ with<sup>_O_</sup> **k**<sup>ˆ</sup> _C∥_<sup>_O_</sup> **r** _S/O_ 6 and<sup>_O_</sup> ˆ **ı** _C∥_<sup>_O_</sup> **k**<sup>ˆ</sup> _C ×_<sup>_O_</sup> ˆ **s** 6. This allows us to easily write<sup>_C_</sup> ˆ **s** 5 = _−_ (sin _α_ 2 cos _γ,_ sin _α_ 2 sin _γ,_ cos _α_ 2)<sup>_⊤_</sup> , where, if<sup>_C_</sup> ˆ **s** 6 =<sup>_C_</sup> _O_<sup>**R**</sup><sup>_O_ˆ</sup><sup>**s**6=(0</sup><sup>_, s_6</sup><sup>_,y, s_6</sup><sup>_,z_), imposing</sup> the constraint<sup>_C_</sup> ˆ **s** 5 _·_<sup>_C_</sup> ˆ **s** 6=0 results in 


Once the screw axes are known, we compute the **joint angles** by comparing how these axes rotate away from a known home configuration ( _qi_ =0). Let<sup>_O_</sup> ˆ **s** _i,_ 0 be the directions of the axes at home configuration, then, from Fig. 1: 

where, _Aγ_ := _−_ ( _s_ 6 _,z/s_ 6 _,y_ ) cot _α_ 2. If _Aγ >_ 1, the kinematic chain cannot be assembled, and if _Aγ_ = 1 the two solutions for _γ_ are repeated. Finally,<sup>_O_</sup> ˆ **s** 5 =<sup>_O_</sup> _C_<sup>**R**</sup><sup>_C_ˆ</sup><sup>**s**5and</sup><sup>_O_</sup><sup>**r**5=</sup><sup>_O_</sup><sup>**r**6.The</sup> remaining parameters are easily found as follows: 


Since _α_ 2, _γ_ and<sup>_O_</sup> ˆ **s** 2 can have up to two solutions each, the maximum number of solutions is 2<sup>3</sup> = 8. 

With this information, we can compute the exponential map in SO(3) to align each axis step by step. This process is shown in Algorithm 1. Note that line 4 is a simplification of _qj ←_ �� log � _Oj_ +1<sup>**R**</sup><sup>_⊤O_</sup> _j_<sup>**R**</sup> ���. 


In the Secs. 3, 4, 5 and 6 we present solvers that have, respectively, _q_ 7, _q_ 6, _q_ 4 and swivel angle as free variable. Each solver has as input the value of the free variable, and<sup>_O_</sup> ˆ **ı** _E_ , _O_ ˆ **s** 7 = _O_ **k** ˆ _E_ , and _O_ **r** _O_ 7 _/O_ = _O_ **r** _E/O − dEO_ **k** ˆ _E_ (and _O_ **r** _O_ 7 _/S_ ). The goal is to find<sup>_O_</sup> **S** 4,<sup>_O_</sup> **S** 5 and<sup>_O_</sup> **S** 6. 

> 7Notation: _O_ **r** _P/Q ∈_ R3 is the position vector of point _P_ with respect to point _Q_ measured in frame _O_ .<sup>_O_</sup> _E_<sup>**R**</sup><sup>_∈_SO(3) is the rotation</sup> matrix defining the orientation of frame _E_ with respect to frame _O_ . Unit vectors wear a hat, **u** ˆ _∈S_<sup>2</sup> . We use the parallel symbol “ _∥_ " to avoid normalising the right-hand side when the left-hand side is a unit vector, e.i. **u** ˆ _∥_ **r** means **u** ˆ = **r** _/|_ **r** _|_ . 

Figure 2: Franka Robot Geometry for the IK solution fixing _q_ 7. 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

4 


Figure 3: Geometry of the Franka for the IK fixing _q_ 6 _/∈{_ 0 _, π}_ . 


Figure 4: Geometry of the Franka for the IK fixing _q_ 6 _∈{_ 0 _, π}_ . 

## 4 SOLUTION LOCKING JOINT 6 

Define _γ_ 1 := _π − q_ 6 as the angle between **S** 5 and **S** 7, and let _P_ be their intersection point as shown in Fig. 3. The following two cases are analysed separately. 

**S** 5 **and S** 7 **are not parallel:** It can be seen that<sup>_O_</sup> **r** _P/S_ = _O_ **r** _O_ 7 _/S_ + ( _a_ 7 _/_ tan _γ_ 1) _O_ **k** ˆ _E_ . Let _γ_ 2 be the angle from **r** _S/P_ to _−_ **S** 5 measured about _−_ ˆ **s** 4 as shown in Fig. 3. The goal is to first find _γ_ 2 using the polygon _SO_ 4 _O_ 6 _P_ and then use the result to find ˆ **s** 5. 

Let _lC_ be the projection of **r** _P/O_ 6 on **S** 5, so _lC_ = _a_ 7 _/_ sin _γ_ 1. The angle _τ_ , defined as ∠ _SPO_ 4 can be easily found by solving first the triangle _PO_ 6 _O_ 4 followed by triangle _SPO_ 4. It can be seen that 


The extreme case when _SPO_ 4 is almost flat, i.e. _d_ 3 + _d_ 5 + _lC < |_<sup>_O_</sup> **r** _S/P |< b_ 1 +( _a_ 5<sup>2+(</sup><sup>_lC_+</sup><sup>_d_5)2)1</sup><sup>_/_2, provides a second solution</sup> _γ_ 2<sup>(2)</sup> in which _τ_ appears with negative sign. 

Now we can write an equation to constrain the angle between **r** _S/P_ and **S** 5 to _γ_ 2. In frame _E_ it is easy to write<sup>_E_</sup> ˆ **s** 5 = ( _−_ sin _γ_ 1 cos _u, −_ sin _γ_ 1 sin _u,_ cos _γ_ 1)<sup>_⊤_</sup> , where _u_ := 5 _π/_ 4 _−q_ 7. Then, the following equation in _u_ is to be solved: 


Figure 5: Geometry of the Franka for the IK solution fixing _q_ 4. 

which has the two solutions _u_<sup>(1)</sup> = _u_ 1 _− u_ 2 and _u_<sup>(2)</sup> = _π − u_ 1 _− u_ 2, where, if<sup>_E_</sup> **r** _S/P_ = ( _C_ 1 _, C_ 2 _, C_ 3)<sup>_⊤_</sup> : 


With<sup>_O_</sup> **r** _P/O_ =<sup>_O_</sup> **r** _P/S_ +<sup>_O_</sup> **r** _S/O_ , the remaining parameters are found easily: 


Since _γ_ 2, _u_ and<sup>_O_</sup> ˆ **s** 2 have up to two solutions, the maximum number of solutions is (2)<sup>3</sup> = 8. 

**S** 5 **and S** 7 **are parallel:** Since _q_ 6 _∈{_ 0 _, π}_ , we define _σ_ = cos _q_ 6 _∈{_ 1 _, −_ 1 _}_ . Consider the plane Π which is perpendicular to **S** 5 and **S** 7 and contains **S** 4, see Fig. 4. Let _E_<sup>_′_</sup> , _O_ 6<sup>_′_and</sup><sup>_S′_</sup> be the respective projections of _E_ , _O_ 6 and _S_ onto Π. Note that _E_ **r** _E′/E_ = (0 _,_ 0 _, −dE_ + _σd_ 5) _⊤_ . Since _E′_ is known, the problem is reduced to solving the equivalent kinematic chain shown in Fig. 4 by working on plane Π and in frame _E_ . 

It can be seen that<sup>_E_</sup> **r** _S′/E′_ =<sup>_E_</sup> **r** _S/E′ −_ (<sup>_E_</sup> **r** _S/E′ ·_<sup>_E_</sup> **k**<sup>ˆ</sup> _E_ )<sup>_E_</sup> **k**<sup>ˆ</sup> _E_ , where<sup>_E_</sup> **r** _S/E′_ =<sup>_E_</sup> **r** _S/E −_<sup>_E_</sup> **r** _E′/E_ . Due to the two possible ways of reaching _S_ from Π, the distance from _O_ 6<sup>_′_to</sup><sup>_S′_along</sup> _x_ 4 is _lO_<sup>(</sup><sup>_i_</sup> 6<sup>)</sup><sup>_′S′_=</sup><sup>_a_5+ (</sup><sup>_−_1)</sup><sup>_i_�</sup> _d_<sup>2</sup> 3<sup>+</sup><sup>_a_</sup> 4<sup>2</sup><sup>_−_</sup> � _E_ **r** _S/E′ · E_ **k** ˆ _E_ �2�1 _/_ 2, _i_ = 1 _,_ 2. This leads to two solutions for _ψ_ , the angle ∠ _S_<sup>_′_</sup> _E_<sup>_′_</sup> _O_ 6<sup>_′_:</sup> 


Similarly, due to the two different ways of assembling the triangle _S_<sup>_′_</sup> _E_<sup>_′_</sup> _O_ 6<sup>_′_, two solutions for the position of</sup><sup>_O_</sup> 6<sup>_′_appear for</sup> each solution of _ψ_ : 

> _E_ **r**<sup>(</sup> _O_<sup>_i_)</sup> 6<sup>_′/E′_=</sup><sup>_a_7 exp</sup> �( _−_ 1)<sup>_i_</sup> _ψ_<sup>_E_</sup> **k**<sup>ˆ</sup> _E_ � _E_ **r** _S′/E′/|E_ **r** _S′/E′|, i_ = 1 _,_ 2 _._ It follows that _E_ **r** 6 = _E_ **r** _E′/E_ + _E_ **r** _O_ 6 _′_<sup>_/E′−σd_5</sup><sup>_E_</sup><sup>**k**ˆ</sup><sup>_E_</sup> and<sup>_E_</sup> ˆ **s** 6 _∥_<sup>_E_</sup> **r** _O_ 6<sup>_′/E′×E_</sup><sup>**k**ˆ</sup><sup>_E_.</sup> For<sup>_E_</sup> **S** 5, it can be seen that 

5 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 


Figure 6: Geometry of the Franka arm for the IK solution fixing the swivel angle _θ_ . 

> _E_ ˆ **s** 5 = _−σE_ **k** ˆ _E_ and _E_ **r** 5 = _E_ **r** 6. To find<sup>_E_</sup> **S** 4, consider 

> _E_ ˆ **ı** 4 _∥_ sign( _lO_ 6 _′_<sup>_S′_)</sup> � _E_ **r** _S′/E′ − E_ **r** _O_ 6 _′_<sup>_/E′_�</sup> , then<sup>_E_</sup> **r** 4 =<sup>_E_</sup> **r** _E′/E_ + 

> _E_ **r** _O_ 6 _′_<sup>_/E′_+</sup><sup>_a_5</sup><sup>_E_ˆ</sup><sup>**ı**4,and</sup><sup>_E_ˆ</sup><sup>**s**4=</sup><sup>_E_ˆ</sup><sup>**ı**4</sup><sup>_×E_ˆ</sup><sup>**s**5.Allthescrewaxes</sup> are then transformed back to frame _O_ . Since _ψ_ ,<sup>_E_</sup> **r** _O_ 6<sup>_′/E′_and</sup><sup>_O_ˆ</sup><sup>**s**2can have up to two solutions each,</sup> the maximum number of solutions is 2<sup>3</sup> = 8. 

## 5 SOLUTION LOCKING JOINT 4 

Since in this case _q_ 4 is given, the triangle _SO_ 4 _O_ 6 can be easily solved to obtain _l_ := _|_ **r** _S/O_ 6 _|_ and _α_ 2, see Fig. 5. We can then locate _O_ 6 on a sphere of radius _l_ and centre at _S_ . From the pose of frame _E_ , we can also constrain _O_ 6 to a known circle of radius _a_ 7 and centre at _O_ 7. Hence, the problem is solved by finding the intersection of this circle with the sphere. This is reduced to the intersection of two circles on the _XEYE−_ plane. 

As shown in Fig. 5, let _S_<sup>_′_</sup> and _O_ 6<sup>_′_be the respective projections</sup> of points _S_ and _O_ 6 onto the _XEYE−_ plane, then define _lS′O_ 6<sup>_′_:=</sup> _|_ **r** _S′/O_ 6<sup>_′|_= (</sup><sup>_l_2</sup><sup>_−_(</sup><sup>_E_</sup><sup>**r**</sup><sup>_O_7</sup><sup>_/S·E_</sup><sup>**k**ˆ</sup><sup>_E_)2)1</sup><sup>_/_2and</sup><sup>_lS′E_:=</sup><sup>_|_</sup><sup>**r**</sup><sup>_S′/E|_=</sup> ((<sup>_E_</sup> **r** _O_ 7 _/S ·_<sup>_E_</sup> ˆ **ı** _E_ )<sup>2</sup> + (<sup>_E_</sup> **r** _O_ 7 _/S ·_<sup>_E_ˆ</sup> **j** _E_ )<sup>2</sup> )<sup>1</sup><sup>_/_2</sup> . To find _O_ 6<sup>_′_,consider</sup><sup>_ϕ_,theanglefrom</sup><sup>_xE_to</sup><sup>**r**</sup> _S_<sup>_′_</sup> _/E_<sup>about</sup> _zE_ , and _ψ_ , the angle ∠ _S_<sup>_′_</sup> _EO_ 6<sup>_′_,asshowninFig.5.Itcan</sup> be seen that _ϕ_ = atan2(<sup>_E_</sup> **r** _S/O_ 7 _·_<sup>_E_ˆ</sup> **j** _E,_<sup>_E_</sup> **r** _S/O_ 7 _·_<sup>_E_</sup> ˆ **ı** _E_ ) and _ψ_ = arccos �( _lS_<sup>2</sup><sup>_′_</sup> _E_<sup>+</sup><sup>_a_</sup> 7<sup>2</sup><sup>_−l_</sup> _S_<sup>2</sup><sup>_′_</sup> _O_ 6<sup>_′_)</sup><sup>_/_(2</sup><sup>_a_7</sup><sup>_lS′E_)</sup> �, leading to the two solutions _q_ 7<sup>(</sup><sup>_i_)</sup> = ( _−_ 1)<sup>_i_</sup> _ψ − ϕ −_ 3 _π/_ 4, _i_ = 1 _,_ 2. 

With _O_ 6<sup>_′_</sup> in hand, it is easy to find _O_ **S** 6 with _O_ ˆ **s** 6 = _OE_<sup>**R**exp</sup> �( _−q_ 7 + 3 _π/_ 4)<sup>_E_</sup> **k**<sup>ˆ</sup> _E_ � _E_ ˆ **ı** _E_ and _O_ **r** _O_ 6 _/O_ = _OE_<sup>**R**</sup><sup>_E_</sup><sup>**r**</sup><sup>_O_</sup> 6<sup>_/O_</sup> 7<sup>+</sup><sup>_O_</sup><sup>**r**</sup><sup>_O_</sup> 7<sup>_/O_, where</sup><sup>_E_</sup><sup>**r**</sup><sup>_O_</sup> 6<sup>_/O_</sup> 7<sup>=</sup><sup>_−a_7 exp</sup> �( _−q_ 7 + _π/_ 4)<sup>_E_</sup> **k**<sup>ˆ</sup> _E_ � _E_ ˆ **ı** _E_ . 

Since _q_ 7,<sup>_O_</sup> **S** 6 and _α_ 2 are known now, we can proceed as we did in Sec. 3, where _q_ 7 was a free parameter. Following the same procedure, we find two solutions of<sup>_O_</sup> ˆ **s** 5 per each value of _q_ 7. Since _q_ 7,<sup>_O_</sup> ˆ **s** 5 and<sup>_O_</sup> ˆ **s** 2 can have up to two solutions each, the total number of solutions is 2<sup>3</sup> = 8. 


Figure 7: An example of flat shoulder singularity. 


Figure 8: Elbow-up and elbow-down solutions in a Shoulderon- **S** 7 singularity. Note that these are _not_ work-space boundary singularities as the arm is not fully stretched. 

## 6 SOLUTION FOR SWIVEL ANGLE 

Due to the lack of a spherical wrist, the swivel angle _θ_ can be defined using either _O_ 6 or _O_ 7 as “wrist centre". Let this be _O_ 7, like in [33]. Then the swivel angle is defined between the plane containing _zO_ and _O_ 7, and the plane containing _O_ 4, _S_ and _O_ 7 as shown in Fig. 6. Hence, if: 


then _θ_ is the angle from<sup>_O_</sup> **n** ˆ1 to<sup>_O_</sup> **n** ˆ2 measured about<sup>_O_</sup> **r** _O_ 7 _/S_ . 

In order to find all the solutions that have the desired value of _θ_ , we discretise the range of _q_ 7, calculate _θ_ for each point, pick the ones that are close enough to the desired value, and finally we interpolate to find the optimal values of _q_ 7. _q_ 7 is used as free variable since, by doing so, the first singularity discussed in Sec. 7 is avoided. 

We do not need to solve the entire IK with _q_ 7 as input, we only obtain the strictly necessary geometric elements that allow us to calculate _θ_ . That means proceeding as done in Sec. 3 until<sup>_O_</sup> **r** 7, _O_ **r** 6 and _O_ ˆ **s** 4 are found. To speed up the process, we ignore the elbow-down solution with _α_ 2<sup>(2)</sup> in Eq. (1), which appears in the unlikely cases where _d_ 3 + _d_ 5 _< l < b_ 1 + _b_ 2. 

## 7 SINGULARITY ANALYSIS 

Singularities in 7-DOF robots can be classified as kinematic and algorithmic singularities [3]. _Kinematic singularities_ are configurations in which rank( **J** ( **q** )) _<_ 6. This rank-deficiency are the result of special geometric conditions between the screw axes. For our IK solvers, these conditions will appear as extreme cases of triangles becoming flat or axes becoming parallel. To provide numerical stability in those cases, GeoFIK includes a constant `SING_TOL` which defines how close to the 

6 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

extreme value a variable can be to still attempt a solution, e.g. if _x >_ 1 but _x −_ 1 _<_ `SING_TOL` , arccos _x_ = 0 is considered. An example occurs when **S** 4 and **S** 6 are parallel and coplanar with _S_ . As a consequence, **S** 5, **S** 6 and _S_ are coplanar too, resulting in rank( **J** ( **q** )) = 5 and the triangle _SO_ 4 _O_ 6 becoming flat. It can be seen that work-space boundary configurations are kinematic singularities. In general, since the Franka has 7 joints, two special geometric conditions are needed to take rank( **J** ) below 6. 

In _algorithmic singularities_ the self-motion no longer affects the variable we want to fix to resolve the redundancy. If _qi_ is being fixed, rank( **J** ( **q** )) = 6 can hold, but if **S** _i_ is linearly independent from the other screw axes, then it is not possible to have _qi_ as free variable. In the Franka arm with the redundant variables considered in this paper, such cases can only occur in the following scenario: 

**Shoulder-on-S** 7 **singularity** : If **S** 7 intersects the spherical shoulder at _S_ , the robot experiences self-motion with the polygon _SO_ 4 _O_ 6 _O_ 7 spinning around **S** 7 without affecting _q_ 4, _q_ 5 and _q_ 6. Hence, only _q_ 7 can be used as free variable with the resulting 6-DOF robot being in regular configuration. If GeoFIK detects that _S ∈_ **S** 7, the solver with _q_ 7 as free variable is called with an emergency value of _q_ 7 provided by the user. Fig. 8 shows an example of this singularity. 

Theoretically, other algorithmic singularities can appear whenever a pair of joint axes become collinear or a joint axis intersects _S_ . However, due to the link-lengths and joint limits of the Franka, this will only occur in the two scenarios described above. As noted in [6], the home configuration (Fig. 1) is a kinematic singularity with rank( **J** ( **q** )) = 5, but it is also algorithmic-singular as **S** 5 intersects _S_ . This case is not implemented in GeoFIK since it violates joint limits. 

As reported in [16, 30], if _q_ 2 = 0 the self-motion is reduced to **S** 2 spinning about **S** 1 = **S** 3 (Fig. 7). However, this configuration is not a kinematic singularity since, in general, rank( **J** ) = 6. The robot is neither in an algorithmic singularity as we ignore the first 3 joints to obtain the rest of the joint axes. However, the shoulder is in a singularity since rank([ **S** 1 _,_ **S** 2 _,_ **S** 3]) = 2. Hence, we refer to this configuration as **flat shoulder singularity** . Only the definition of **S** 2 is affected, with _q_ 1 becoming a free choice. The user can provide an emergency value of _q_ 1 to be used in this situation. 

Another kind of singularity occurs in the swivel angle definition (2). Clearly, _θ_ is not defined if **r** _O_ 7 _/S_ is parallel to _zO_ . This is the unavoidable singularity of any swivel angle definition [8]. GeoFIK prints an error message in those cases. Note that the sign _σ_ prevents the sudden change of direction of the plane containing _S_ , _O_ 7 and _O_ 4. In addition, if these three points are collinear, **n** ˆ2 = ˆ **s** 4 is chosen. 

## 8 COMPARISON WITH BASELINE SOLVERS 

This section presents an analytical comparison against the stateof-the-art solvers from He and Liu [16] (referred to here as HeLiu), IKFast [7], and the 6-DOF solver IKGeo [9]. HeLiu is only compared fixing _q_ 7 since it is the only solver they provide. For IKGeo, we coded the necessary functions to solve the IK of the Franka using the general 6-DOF solver. The dif- 

Table 1: Solver Comparison for Singular Configurations (angles in degrees). Solutions in orange indicate larger errors (EE <u>position)</u> _≥_ 1 cm, and in red, violations of joint limits. 

|||**Case 1**|**(Flat sho**|**ulder, solver**|**s withq7 a**|**s free var**|**iable)**||
|---|---|---|---|---|---|---|---|---|
||sol|_q_1|_q_2|_q_3|_q_4|_q_5|_q_6|_q_7|
||1|-30.06|86.09|123.97|-106.86|48.58|nan|-21.32|
||2|149.94|-86.09|-56.03|-106.86|48.58|nan|-21.32|
|GeoFIK<br>|3|-90|0|115.96|-106.86|131.42|150.52|-21.32|
|(ours)|4|90|0|-64.04|-106.86|131.42|150.52|-21.32|
||1|90|0|-64.04|-106.86|131.42|150.52|-21.32|
|HLi|2|90|0|-64.04|-106.86|131.42|150.52|-21.32|
|eu|3|-30.06|86.09|123.97|nan|nan|nan|nan|
||4|149.94|-86.09|-56.03|nan|nan|nan|nan|
||1|-30.06|86.09|123.97|-106.86|48.58|-137.3|-21.32|
|IKFast|2|149.94|-86.09|-56.03|-106.86|48.58|-137.3|-21.32|
||1|149.93|-86.09|-56.03|-106.9|48.58|-137.3|-21.32|
||2|-30.06|86.09|123.97|-106.9|48.58|-137.3|-21.32|
||3|-27.9|-0.02|61.7559|-106.9|131.4|150.5|-21.32|
|IKGeo|4|152.1|0.02|-118.2|-106.9|131.42|150.5|-21.32|
||5|-174.8|-48.83|65.06|53.35|-90|-173.4|-21.32|
||6|5.17|48.83|-114.9|53.35|-90|-173.4|-21.32|
||**Ca**<br>|**se 2(algo **<br>|**rithmic si**<br>|**ngularity, s**<br>|**olvers with**<br>|**q6 as fre**<br>|**e variab**<br>|**le)**<br>|
||sol|_q_1|_q_2|_q_3|_q_4|_q_5|_q_6|_q_7|
||1|-18.99|78.13|28.75|-39.33|0|204.90|0|
||2|161.01|-78.13|-151.25|-39.33|0|204.90|0|
||3|2.37|nan|-148.49|-39.33|nan|169.24|0|
||4|nan|nan|31.51|-39.33|nan|169.24|0|
|GeoFIK<br>|5|-12.43|90.22|28.08|-14.19|0|193.44|0|
|(ours)|6|nan|-90.22|-151.92|-14.19|0|193.44|0|
||7|-4.97|nan|-151|-14.19|nan|180.65|0|
||8|nan|nan|29|-14.19|nan|180.65|0|
|IKFast||||no|solution||||
|IKGeo||||no|solution||||


ferent solvers provided by IKGeo were tested and it was decided to use `IK_spherical_2_intersect` when locking _q_ 7, and `IK_spherical` for _q_ 6 and _q_ 4. 

### _8.1 Number of solutions attempted_ 

As discussed in Sections 3-5, each case of GeoFIK solver attempts 8 solutions which constitute all geometrically valid solutions. In contrast, HeLiu attempts only 4 solutions, explicitly omitting a secondary elbow-down (solution 2 in Eq. (1)), as acknowledged in [16]. Due to its general algebraic approach, IKFast attempts the 16 solutions that the system of equations can have. However, since only 8 solutions are geometrically possible, the other 8 must be complex or repeated. Among those, IKFast will return elbow-down solutions with link interference which have to be discarded by subsequent joint-limits checks. The number of solutions attempted by IKGeo depends on each subproblem it solves. 

### _8.2 Handling of singularities_ 

We examine the behavior of the solvers in the flat shoulder and wrist-on- **S** 7 configurations described in Sec. 7. 

**flat shoulder singularity:** Consider the following IK problem that leads to a flat shoulder: 


PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

7 

Table 2: IK Solver Quantitative Comparison in terms of computation time, number of solutions, and errors. 

|Min/Max||Lock|ing q7|||Locking q6|||Locking q4||Locking S. Angle|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Mean_±_Std|**GeoFIK**|HeLiu|IKFast|IKGeo|**GeoFIK**|IKFast|IKGeo|**GeoFIK**|IKFast|IKGeo|**GeoFIK**|
|Joint angles|1.7/4.8|0.3/16.6|3.2/14.6|4.5/25.0|2.5/6.3|33.7/129.3|7.7/30.1|5.1/7.4|16.6/71.7|5.5/23.4|41.7/1429.2|
|computation time (_µ_s)|2.1_±_0.6|1.0_±_0.6|4.8_±_1.7|6.0_±_2.3|3.1_±_0.9|39.1_±_7.8|8.3_±_1.3|5.4_±_0.2|18.7_±_5.6|6.1_±_2.2|198_±_123|
|Jacobian only|0.2/1.9|_−_|_−_|_−_|0.4/2.3|_−_|_−_|0.9/7.7|_−_|_−_|30.8/1405.5|
|computation time (_µ_s)|0.3_±_0.07|_−_|_−_|_−_|0.8_±_0.3|_−_|_−_|1.4_±_0.5|_−_|_−_|192.1_±_125|
|Jacobian + joint angles|1.8/11.3|6/20|8.6/41|11.5/55.4|2.6/11.1|39.5/132.6|18/73.5|5.2/21|17/65.5|10.5/31.6|41.6/1322.8|
|computation time (_µ_s)|2.7_±_1.5|7_±_1.2|12.8_±_5|14.4_±_4.6|3.5_±_1.3|46.7_±_7.8|19.7_±_3|5.6_±_0.6|19_±_4.6|11.4_±_2.7|204.2_±_135.3|
|Num. valid sols.|1/8|0/4|1/8|1/8|1/8|1/8|0/8|1/8|1/8|0/4|0/8|
|per call|3.2_±_1.5|2.6_±_1.1|3.2_±_1.5|3.2_±_1.5|3.6_±_1.5|3.6_±_1.5|2.9_±_1.6|4.9_±_2.0|4.9_±_2.0|2.6_±_1.5|2.0_±_1.0|
|Total num. of valid sols.|6352|5272|6346|6350|7119|7119|5856|9742|9742|5137|4042|
|Total num. of wrong sols.|0|72|0|328|0|0|0|0|0|0|0|
|EE pos. error mean (m)|2x10<sup>_−_6</sup>|3x10<sup>_−_4</sup>|7x10<sup>_−_10</sup>|5x10<sup>_−_3</sup>|9x10<sup>_−_14</sup>|7x10<sup>_−_10</sup>|9x10<sup>_−_8</sup>|6x10<sup>_−_14</sup>|6x10<sup>_−_10</sup>|5x10<sup>_−_10</sup>|1x10<sup>_−_5</sup>|
|EE rot. error mean (rads)|1x10<sup>_−_5</sup>|4x10<sup>_−_4</sup>|1x10<sup>_−_9</sup>|3x10<sup>_−_13</sup>|3x10<sup>_−_13</sup>|1x10<sup>_−_9</sup>|3x10<sup>_−_13</sup>|3x10<sup>_−_13</sup>|1x10<sup>_−_9</sup>|3x10<sup>_−_13</sup>|2x10<sup>_−_13</sup>|


The problem is sent to the solvers with _q_ 7 as a free parameter. The results are shown as Case 1 in Table 1. 

In GeoFIK, the user can provide a value of _q_ 1 to resolve the redundancy. The default value is _π/_ 2. Solutions for the two ways of assembling the spherical shoulder are still returned with _±q_ 1. One such solution is shown in Fig. 7. Other two solutions that are not singular are returned, however, in those _q_ 6 violates joint limits. In HeLiu, the user provides a vector of joint angles from which it takes _q_ 1 and uses it to resolve the redundancy induced by the singularity. Then, it returns two repeated solutions with _q_ 1, rather than two different ones with _±q_ 1, which can lead to discontinuity in the real-world applications, and the other two regular solutions that violate joint limits. IKFast fails in this singularity and only returns the two regular configurations that violate joint limits. IKGeo returns these same two regular configurations but also returns 4 invalid solutions for which the end-effector position is more than 1cm away from that of the requested pose. 

**shoulder-on-S** 7 **:** Consider the following IK problem that leads to an algorithmic singularity: 


The problem is sent to the solvers with _q_ 6 as a free parameter. The results are shown as Case 2 in Table 1. In the algorithmic singularities, _q_ 6 stops being a free variable as there are only two values of _q_ 6 that satisfy the pose. One of them is the value used in this IK problem. 

GeoFIK is able to automatically detect that _q_ 6 can no longer be freely chosen and transfers the problem to the solver with _q_ 7 as a free variable. 8 solutions are found, indicating that triangle _SO_ 4 _O_ 6 is almost flat, allowing elbow-up and elbow-down solutions as shown in Fig. 8. Among those, two solutions are within the locked value for _q_ 6. 

Both IKFast and IKGeo fail to generate any solution. It is worth highlighting that this behaviour is inconsistent in IKFast as it is able to find solutions to some shoulder-on- **S** 7 singularities (yet, it is highly sensitive to numerical precision to work). This is not an issue with GeoFIK, since once it detects the singularity, it no 

longer requires the value of _q_ 6. Hence, it returns consistently valid solutions. 

### _8.3 Quantitative Analysis_ 

While Sec. 8.2 provided a comparison in singular configurations, here we quantitatively evaluate the performance in regular and near-singular configurations. We generated 2000 random valid joint configurations to produce EE poses, which in turn were sent as input to the solvers<sup>8</sup> . 

We evaluated all the solvers against 4 parameters. The results are shown in Table 2. 

**(i) Computational time** for a single call for only joint angles, only Jacobians, and both joint angles and Jacobians. For only joint angles, GeoFIK outperformed the other solvers when locking _q_ 6 and _q_ 4. HeLiu is the fastest in the case of _q_ 7, this is due to the lack of calculation of elbow-down solutions. 

When comparing the Jacobian computation time, GeoFIK outperformed all other solvers. This is mostly due to our screwaxis-based design that returns the Jacobian as a byproduct of the IK. In fact, GeoFIK outputs Jacobians even faster than the joint-configurations. 

**(ii) Number of distinct valid solutions (total and per call):** We consider a solution valid if it is within joint-limits and has an EE error smaller than 5mm in position and 3<sup>_◦_</sup> in rotation. Repeated solutions are not counted. It can be seen that GeoFIK outperforms all the solvers in total number of solutions with IKFast almost providing the same number. 

**(iii) Total number of incorrect solutions:** Incorrect solutions are defined here as being within joint-limits but having an EE error as described in (ii). HeLiu and IKGeo returned incorrect solutions in the _q_ 7 case. 

**(iv) EE error:** GeoFIK outperforms all the solvers in EE error with exception of the _q_ 7 case. 

> 8Laptop used: 11th Gen Intel Core i7-11370H (3.30 GHz), 32GB running Windows 11. Compiler: gcc 13.2.0 and optimization flag `-O3` for all solvers. For the case of locking _q_ 7, clang was used instead for all solvers as it gave better results, except for IKFast which was compiled with gcc. 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

8 


Figure 9: Trajectory tracking using IK solvers: The obtained joints (dashed-green lines) compared to the real-robot (blue lines). HeLiu and GeoFIK (with _q_ 7 as a free-var) both fail to find a feasible solution around 10 s. (shaded area) and the robot stops (real-robot on the top strip) only to continue with an aggressive motion at the end of the trajectory. GeoFIK with the swivel-angle as free-var always finds a solution—as expected from Table 2—enabling smooth joint-trajectory. 

## 9 REAL-WORLD EXPERIMENT 

We evaluated our GeoFIK approach on a real Franka Robot to investigate (i) feasibility and joint-space tracking of a desired task-space trajectory (herein obtained through vector fields) within the robot’s central workspace, and (ii) whole-body tasks that require both the end-effector pose and the manipulability ellipsoid to match a human-demonstrated reference (i.e., sweeping and pushing). 

**Feasibility and Trajectory Tracking:** This first scenario tested the ability to compute real-time IK solutions and maintain a continuous joint-space trajectory over a basic trajectory in the central region of the workspace, a domain expected to be straightforward. Despite this assumption, the IK solver by HeLiu failed after approximately 10 s, providing no valid solutions and forcing the robot to halt. Our GeoFIK solver, when using _q_ 7 as the free parameter, also reached a point where it could not find a solution. Both failures led to abrupt reconfiguration once a valid solution was found again (Fig. 9 top-images with a red border). 

Allowing the standard _q_ 7-locking solvers to sample a small range _±_ 10<sup>_o_</sup> around the current _q_ 7 mitigated total failure, but induced frequent chattering in joint angles (Fig. 11). Meanwhile, IKFast remained unable to find even a valid initial solution, all valid IKs demand an instantaneous flip of the base joints, generating torque reflexes and halting progress altogether, as shown in Fig. 12(a). In contrast, the swivel-angle-based GeoFIK solution never lost feasibility and preserved a smooth trajectory as shown in Fig 9. 

**Whole-Body (Manipulability) Tracking:** The second set of experiments required each solver to produce both joint angles and Jacobian, which was used to compute the manipulability ellipsoid. The solver then aimed to match a reference ellipsoid provided by a user demonstration (e.g. sweeping or pushing motions). We sampled 250 configurations every 30ms, akin to a lightweight model-predictive control loop. 

As shown in Fig. 10, GeoFIK achieves lower computational times thanks to its screw-transformation design, where the Jacobian emerges naturally from the IK solution. Although HeLiu managed to complete the sweeping task, it proved slower in delivering joint–Jacobian pairs. IKFast again frequently produced no valid solutions (or an out-of-reach configuration), leading to task failure in the sweeping experiments, Figs. 12(bc). GeoFIK, in contrast, consistently offered feasible joint trajectories while preserving the desired manipulability profile, underscoring the benefits of its geometry-aware method and multi-parameter redundancy resolution. 


Figure 10: Computation time in tracking manipulability for sweeping (dashed) and pushing (solid) tasks. 

## 10 CONCLUSIONS 

We introduced a fully geometric, screw-theory-based IK solver for the Franka Robot, accommodating multiple free parameters and automatically providing the Jacobian even faster than the joint configuration. By systematically capturing all geometrically valid solutions, our method, GeoFIK, overcomes the limitations of existing solvers that either fix only _q_ 7 or neglect key geometric insights. Extensive quantitative benchmarks showed that our approach consistently outperforms baseline solvers in terms of reliability, completeness, and efficiency. Real-world experiments confirmed its resilience, enabling the 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

9 


Figure 11: Trajectory tracking using IK solvers and sampling _q_ 7 _±_ 10<sup>_o_</sup> . Sampling allows _q_ 7-locking IKs to complete the task, but the resulting trajectory includes chattering due to discontinuities (the overlapped green areas). 


Figure 12: (a) IKFast traj. tracking, and (b)c IKFast and (c) GeoFIK sweeping tasks. IKFast often provides invalid solutions. In (a), the lack of solutions near the **q** (0) results in abrupt arm rotations exceeding torque reflexes. Similarly, in sweeping tasks, IKFast causes the arm to flip over lacking proper solutions. GeoFIK success in all tasks. 

robot to smoothly execute tasks and even when controlling less conventional variables, such as the swivel angle. We believe that the flexibility and robustness of GeoFIK can facilitate more advanced planning, control, and learning algorithms, thereby fulfilling the growing demand for speed and reliability in modern robotics. 

## REFERENCES 

- [1] Franka Control Interface (FCI) - Panda description. `https://frankaemika.github.io/docs/franka_ ros.html#franka-description` . Accessed: 28-Feb2025. 

- [2] MoveIt! Tutorials - IKFast kinematics solver. `http://docs.ros.org/en/kinetic/api/moveit_ tutorials/html/doc/ikfast/ikfast_tutorial. html` . Accessed: Sep-2025. 

- [3] M. Asgari, I. A. Bonev, and C. Gosselin. Singularities of ABB’s YuMi 7-DOF robot arm. _Mechanism and Machine Theory_ , 2025. 

- [4] J. Burdick and H. Seraji. Characterization and control of self-motions in redundant manipulators. In _Proceedings of the NASA Conference on Space Telerobotics, Volume 2_ , 1989. 

- [5] S. Chiaverini. Singularity-robust task-priority redundancy resolution for real-time kinematic control of robotic manipulators. _IEEE Trans. on Robotics and Automation_ , 13(3):398–410, 1997. 

- [6] P. Corke. Matlab Robotics Toolbox: Franka Emika Panda Kinematics & Singularities. https://petercorke.com/robotics/franka-emika-pandakinematics-and-singularities/. Accessed: 29-08-24. 

- [7] R. Diankov. _Automated construction of robotic manipulation programs_ . PhD thesis, Carnegie Mellon University, USA, 2010. 

- [8] A. J. Elias and J. T. Wen. Redundancy parameterization and inverse kinematics of 7-DOF revolute manipulators. _Mechanism and Machine Theory_ , 204:105824, 2024. 

- [9] A. J. Elias and J. T. Wen. IK-Geo: Unified robot inverse kinematics using subproblem decomposition. _Mechanism and Machine Theory_ , 209:105971, 2025. 

- [10] J. Elsner. Taming the Panda with Python: A powerful duo for seamless robotics programming and integration. _SoftwareX_ , 24, 2023. 

- [11] S. Feng, B. Burchfiel, and R. Tedrake. TRI’s Robots Learn New Manipulation Skills in an Afternoon. Here’s How. Medium (Toyota Research Institute), https://medium.com/toyotaresearch/tris-robots-learnnew-skills-in-an-afternoon-here-s-how-2c30b1a8c573. Accessed: 29-Aug-2024. 

- [12] L. F. Figueredo, R. D. C. Aguiar, L. Chen, T. C. Richards, S. Chakrabarty, and M. Dogar. Planning to minimize the human muscular effort during forceful human-robot collaboration. _ACM Trans. on Human-Robot Interaction (THRI)_ , 11(1):1–27, 2021. 

- [13] Q. Gallouédec, N. Cazin, E. Dellandréa, and L. Chen. panda-gym: Open-Source Goal-Conditioned Environments for Robotic Learning. In _Proc. of the 4th Robot Learning Workshop: Self-Supervised and Lifelong Learning (NeurIPS)_ , 2021. 

- [14] C. R. Garrett, R. Chitnis, R. Holladay, B. Kim, T. Silver, L. P. Kaelbling, and T. Lozano-Pérez. Integrated task and motion planning. _Annual Review of Control, Robotics, and Autonomous Systems_ , 2021. 

- [15] S. Haddadin. The Franka Emika robot: A standard platform in robotics research [survey]. _IEEE Robotics and Automation Magazine_ , 2024. 

- [16] Y. He and S. Liu. Analytical inverse kinematics for Franka Emika panda–a geometrical solver for 7-DOF manipulators with unconventional design. In _IEEE Int Conf Ctr, Mech & Autom (ICCMA)_ , 2021. 

- [17] Y. He and S. Liu. Franka analytical IK. `https: //github.com/ffall007/franka_analytical_ik` , 2024. Accessed: 28-Feb-2025. 

- [18] L. Jiang, X. Huo, Y. Liu, and H. Liu. An integrated inverse kinematic approach for the 7-DOF humanoid arm with offset wrist. In _IEEE int. conf. on robotics & biomimetics (ROBIO)_ , pages 2737–2742, 2013. 

- [19] R. Kirschner, K. Karacan, A. Melone, et al. Categorizing robots by performance fitness into the tree of robots. _Nature Machine Intelligence_ , 2025. 

- [20] K. Kreutz-Delgado, M. Long, and H. Seraji. Kinematic analysis of 7 DOF anthropomorphic arms. In _Proceedings., IEEE International Conference on Robotics and Automation_ , pages 824–830. IEEE, 1990. 

PREPRINT – GEOFIK: A FAST AND RELIABLE GEOMETRIC SOLVER FOR THE IK OF THE FRANKA ARM 

10 

- [21] R. Laha, W. Wu, R. Sun, N. Mansfeld, L. F. Figueredo, and S. Haddadin. S*: On safe and time efficient robot motion planning. In _IEEE Int. Conf. on Robotics & Autom. (ICRA)_ , pages 12758–12764, 2023. 

- [22] C. Lenz, M. Schwarz, A. Rochow, B. Pätzold, R. Memmesheimer, M. Schreiber, and S. Behnke. NimbRo wins ANA Avatar XPRIZE Immersive Telepresence Competition: Human-Centric Evaluation and Lessons Learned. _International Journal of Social Robotics_ , 2023. Published online Oct. 2023. 

- [23] P. López-Custodio, R. Fu, J. Dai, and Y. Jin. Compliance model of Exechon manipulators with an offset wrist. _Mechanism and Machine Theory_ , 167:104558, 2022. 

- [24] A. A. Oliva, F. Spindler, P. R. Giordano, and F. Chaumette. FrankaSim: A dynamic simulator for the Franka Emika robot with visual-servoing enabled capabilities. In _17th International Conference on Control, Automation, Robotics and Vision (ICARCV)_ , pages 868–874, 2022. 

- [25] D. L. Pieper. _The kinematics of manipulators under computer control_ . Stanford University, 1969. 

- [26] M. Raghavan and B. Roth. Inverse kinematics of the general 6R manipulator and related linkages. _Journal of Mechanical Design_ , 115(3):502–508, 09 1993. 

- [27] D. Rakita, H. Shi, B. Mutlu, and M. Gleicher. Collisionik: A per-instant pose optimization method for generating robot motions with environment collision avoidance. In _IEEE International Conf. on Robotics and Automation (ICRA)_ , pages 9995–10001, 2021. 

- [28] J. M. Selig. _Geometric fundamentals of robotics_ . Springer Science & Business Media, 2007. 

- [29] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo. _Robotics: Modelling, Planning and Control_ . Springer Publishing Company, Incorporated, 2010. 

- [30] S. Tittel. Analytical solution for the inverse kinematics problem of the Franka Rmika panda seven-DOF lightweight robot arm. In _20th Intern. Conference on Advanced Robotics (ICAR)_ , pages 1042–1047, 2021. 

- [31] M. Tröbinger, A. Naceri, X. Chen, H. Sadeghian, and S. Haddadin. Identification of a generalized base inertial parameter set of robotic manipulators considering mounting configurations. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [32] Y. Wang, L. Li, and G. Li. An analytical solution for inverse kinematics of 7-DOF redundant manipulators with offsets at elbow and wrist. In _2022 IEEE 6th Information Technology and Mechatronics Engineering Conference (ITOEC)_ , volume 6, pages 1096–1103. IEEE, 2022. 

- [33] X. Yang, Z. Zhao, Z. Xu, Y. Li, J. Zhao, and H. Liu. General inverse kinematics method for 7-DOF offset manipulators based on arm angle parameterization. _Acta Astronautica_ , 202:263–277, 2023. 

- [34] K. Zakka, B. Tabanpour, Q. Liao, M. Haiderbhai, S. Holt, J. Y. Luo, A. Allshire, E. Frey, K. Sreenath, L. A. Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 

