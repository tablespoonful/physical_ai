---
title: "The Dynamic Model of the UR10 Robot and its ROS2 Integration"
date: "2025-02-17"
authors: "Vincenzo Petrone; Enrico Ferrentino; Pasquale Chiacchio"
url: https://arxiv.org/abs/2502.11940
pdf: https://arxiv.org/pdf/2502.11940
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.11940)** / [論文ページ](https://arxiv.org/abs/2502.11940)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/TII.2025.3534415 – IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS 1 

# The Dynamic Model of the UR10 Robot and its ROS2 Integration 

Vincenzo Petrone, Enrico Ferrentino, and Pasquale Chiacchio 

**_Abstract_ — This paper presents the full dynamic model of the UR10 industrial robot. A triple-stage identification approach is adopted to estimate the manipulator’s dynamic coefficients. First, linear parameters are computed using a standard linear regression algorithm. Subsequently, nonlinear friction parameters are estimated according to a sigmoidal model. Lastly, motor drive gains are devised to map estimated joint currents to torques. The overall identified model can be used for both control and planning purposes, as the accompanied ROS2 software can be easily reconfigured to account for a generic payload. The estimated robot model is experimentally validated against a set of exciting trajectories and compared to the state-of-the-art model for the same manipulator, achieving higher current prediction accuracy (up to a factor of 4.43) and more precise motor gains. The related software is available at https://code ocean.com/capsule/8515919/tree/v2.** 

**_Index Terms_ — dynamic identification, nonlinear dynamical systems, parameter identification, robot model, robot operating system, system identification** 

## I. INTRODUCTION 

**M** ODELING manipulator dynamics is critical for a broadspectrum of robotic applications, ranging from highperformance model-based control [1] to trajectory planning [2] and human-robot interaction [3]–[5]. 

In industrial settings, the effectiveness of planning and control algorithms heavily relies on the accuracy of the underlying dynamic model [6]. Therefore, obtaining a reliable estimation of manipulator dynamics is essential in all the aforementioned applications [7]. 


Fig. 1: UR10 Kinematic Model 

## _A. Background_ 

Given the fundamental importance of an accurate dynamic characterization of manipulators, the identification of accurate dynamic models has been one of the major interests in robotics research for decades [8]. Traditional approaches involve modeling system dynamics using Newton-Euler equations [9] or Lagrangian methods [10], and decomposing it to linearly separate kinematic variables from dynamic coefficients [11]. 

Authors are with the Department of Information Engineering, Electrical Engineering and Applied Mathematics (DIEM), University of Salerno, 84048 Fisciano, Italy (e-mail: vipetrone@unisa.it, eferrentino@unisa.it, pchiacchio@unisa.it). 

> ©2025 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works. 

In the realm of system identification, dynamic coefficients are typically identified through online or offline techniques. Online methods, such as composite adaptation and learning algorithms [12], are often used in adaptive control to compensate for unknown dynamics and disturbances [13]. However, offline estimation remains the prevalent strategy for identifying manipulator dynamics [7], [8], which involves collecting data from specifically designed excitation trajectories [14] and applying linear estimation algorithms [15]. 

Although these procedures have been performed on various motion-controlled manipulators [16]–[18], two key challenges persist: linear models fail to fully capture the nonlinear dynamics due to friction effects, resulting in inaccuracies in torque prediction [7], [19], [20]; furthermore, unlike many commercial robots, industrial manipulators typically do not provide direct torque measurements, allowing access to joint currents only [21]. This necessitates the estimation of _motor_ 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/TII.2025.3534415 – IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS 

2 

_drive gains_ , which convert currents to torques, as part of the identification process. 

This study focuses on the dynamic identification of the UR10 industrial manipulator, shown in Fig. 1, addressing the aforementioned challenges of estimating its linear dynamic coefficients, nonlinear joint friction currents, and motor drive gains. 

## _B. Contribution_ 

This paper’s primary contribution is the comprehensive estimation of the UR10 robot dynamic coefficients, hence the provision of the complete dynamic model of this manipulator. We compare our model to the state-of-the-art model [3] against two excitation trajectories.Our model consistently achieves lower estimation errors across all joints. Unlike [3], which solely estimates the static coefficients related to gravity and extracts other dynamic coefficients from a simulated model provided by the manufacturer, our approach estimates the full set of dynamic coefficients, executing excitation trajectories on the real hardware directly. As mentioned in Section I-A, our identification process consists of three stages: (i) estimation of linear dynamic coefficients; (ii) characterization of nonlinear friction currents; (iii) computation of motor drive gains. 

As an additional contribution, in a comparison with [3], which performs a two-stage static estimation of motor drive gains, our method utilizes a one-shot algorithm based on dynamically exciting trajectories, yielding more accurate results. For this, we adopt the methodology originally proposed in [21], to map the whole set of estimated current-level dynamic parameters to the torque level, extending the identified model to include a generic payload at the manipulator’s flange, building on formulations from [17]. To the best of the authors’ knowledge, this is the first comprehensive study that includes motor drive gain estimation, dynamic identification, and payload integration for a single industrial manipulator. Our findings, supported by a consistent investigation and analysis of all these features, are crucial for a complete and effective deployment of industrial robots. 

Furthermore, we improve the practical applicability of our research providing a ROS2-ready software tool, the _inverse dynamics solver_ (IDS), that incorporates the identified dynamic model of the UR10 arm in an off-the-shelf library, providing users a simple tool to be straightforwardly integrated in control and planning applications. Besides providing the manipulator dynamic model, the IDS is also designed to be easily reconfigurable, in that it allows users to include any known payload at the end-effector (EE) to obtain accurate joint torques for the entire arm-payload system, relieving users from the burden of performing a second estimation of the composite system [15]. The solver is experimentally validated on the UR10 with a known payload, using inertial parameters from the manufacturer’s datasheet. 

## _C. Outline_ 

The rest of the article is structured as follows. Section II briefly describes the theoretical foundations on the identification problem, and introduces UR10’s kinematic model. Section III presents the identification procedure we adopt to 

identify the robot’s dynamic model. Section IV reports the results obtained employing the procedure, comparing with the state-of-the-art model. Section V concludes the paper, summarizing the main findings of the present work and suggesting potential improvements left for future developments. For convenience, the symbols and the notation adopted, as well as the dimensions of all the arrays utilized in the paper, are included in the List of Symbols in appendix. 

## II. PRELIMINARIES 

## _A. Manipulator Dynamic Model_ 

The manipulator dynamics in free-space can be modeled with the following equations of motion (EOM) [22]: 


where **_H_** ( **_q_** ) is the inertia matrix, **_C_** ( **_q_** _,_ **_q_** ˙) is the matrix accounting for Coriolis and centrifugal effects, **_f_** ( ˙ **_q_** ) is the joint friction vector, **_g_** ( **_q_** ) expresses the gravitational torques, **_τ_** is the joint torque vector, and **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨ are the joint kinematic variables, namely positions, velocities and accelerations. 

Joint torques **_τ_** are strictly related to the currents **_v_** supplied to the joint motors, according to the following linear relationship [23]: 


where **_K_** is the diagonal matrix containing the joint motor drive gains. 

According to the Lagrange formulation [10], the components **_H_** , **_C_** and **_g_** are parametrized w.r.t. the link _inertial parameters_ including, for each link _i_ , its mass _mi_ , center of mass (COM) vector **_r_** _i_ = [ _ri,x, ri,y, ri,z_ ]<sup>_⊤_</sup> relative to the _i_ -th kinematic frame, and the symmetric inertia tensor relative to the principal axes of inertia 


The inertial parameters can be grouped to constitute the robot _dynamic parameters_ 


where _mi_ **_r_** _i_ is the first moment of inertia and **_I_** _i_ ≜ **_I_**<sup>ˇ</sup> _i_ + _mi_ [ **_r_** _i_ ]<sup>_⊤_</sup> _×_<sup>[</sup><sup>**_r_**</sup><sup>_i_]</sup><sup>_×_representstheinertiatensorw.r.t.theoriginof</sup> the _i_ -th frame, in virtue of the Steiner theorem, with 


being the skew-symmetric matrix operator applied to **_r_** _i_ . 

Ignoring the **_f_** term, the EOM in (1) can be expressed in linear form, separating the dynamic parameters in (4) from kinematics-related expressions, as [11] 


where **_P_** ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨) is called _regressor_ , and **_π_** ≜ [ **_π_** 1<sup>_⊤, . . . ,_</sup><sup>**_π_**</sup><sup>_⊤_</sup> _n_<sup>]</sup><sup>_⊤_</sup> is the vector of the dynamic parameters for the whole _n_ -link chain, with _n_ being the number of degrees of freedom (DOF) of the robot. 

PETRONE _et al._ : THE DYNAMIC MODEL OF THE UR10 ROBOT AND ITS ROS2 INTEGRATION 

3 

## _B. Joint Friction Model_ 


where **_f_** _o,_ **_f_** _v,_ **_f_** _c_ are parameters representing the Coulomb friction offset, viscous friction and Coulomb friction coefficients, respectively, and multiplications are element-wise. Since (7) is linear w.r.t. **_f_** _o_ , **_f_** _v_ and **_f_** _c_ , these parameters can be included in **_π_** , thus being consistent with the linear model in (6). Nevertheless, friction is notably a complex nonlinear phenomenon [19], especially during motion reversal [20], hence a sigmoidal model is more appropriate [3]: 


with element-wise multiplications and exponentials. Differently from (7), it is worth stressing that (8) presents a nonlinear dependency on the parameters parameters **_δ_** and **_ν_** . 

More specifically, friction exhibits a nonlinear behavior in a particular region (called _nonlinearity region_ ) of the joint velocity domain, denoted with 


Henceforth, the short notation on the left-hand side will be used for convenience. In this work we aim at comparing with [3], thus we adopt the sigmoidal model (8). However, other formulations can be chosen in general: for instance, some models include the Stribeck effect [24] or the degressive friction [25], [26], whereas other approaches approximate the friction contribution with neural networks based on sigmoidjump activation functions [27]. 

## _C. Modified Dynamic Coefficients Due to a Payload_ 

When a rigid payload is attached at the robot’s EE, it introduces new dynamics that affect **_π_** _n_ , according to the following modifications [17]: 


where _mL_ , **_r_** _L_ and **_I_** _L_ are the payload’s mass, COM and inertia tensor w.r.t. _n_ -th link frame, with 


The linear transformations (11)–(12) are necessary to compute (10b)–(10c), since the payload’s COM **_r_** _l_ and inertia tensor **_I_** _l_ are typically expressed in frame _l_ , i.e. the payload origin frame, where the transform matrix **_T_** _n_<sup>_l_,definedas</sup> 


expresses the rotation **_R_** _n_<sup>_l_andthetranslation</sup><sup>**_t_**</sup><sup>_l_</sup> _n_<sup>of</sup><sup>_l_w.r.t.the</sup> _n_ -th link frame. 

TABLE I: UR10 DH parameters 

|**Joint**|**_a_** [mm]|**_α_** [rad]|**_d_** [mm]|**_θ_**|
|---|---|---|---|---|
|Base|0|_−_<sup>_π_</sup>_/_2|127.3|_q_1|
|Shoulder|612|0|0|_q_2|
|Elbow|572.3|0|0|_q_3|
|Wrist 1|0|_−_<sup>_π_</sup>_/_2|163.941|_q_4|
|Wrist 2|0|_π/_2|115.7|_q_5|
|Wrist 3|0|0|92.2|_q_6|


Because of (10a)–(10b), the first moment of inertia of the last link becomes [17] 


hence preserving the linearity property in (6), with 


where **_π_** _L_ indicates the payload’s dynamic parameters, composed of _mL_ , **_r_** _L_ and **_I_** _L_ in (4). 

## _D. UR10 Kinematic Model_ 

Computing **_P_** ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨) requires the knowledge of the manipulator kinematics, usually devised applying the DenavitHartenberg (DH) convention on the dimensional properties given by the robot manufacturer [8]. However, since they can be subject to inaccuracies, one can mitigate the parameter uncertainty by performing a separate kinematic calibration procedure as a preliminary step [28]. Nevertheless, in the context of dynamic model identification, these parameters are typically assumed to be known [3], [8], [9], [16]–[18], [21], and used as input to the estimation algorithm; therefore, the kinematic calibration problem falls outside the scope of this article. As regards the UR10 robot, Fig. 1 shows its kinematic model, also highlighting its joints and the relative frames, from which the DH parameters reported in Table I are extracted<sup>1</sup> . 

## III. DYNAMIC MODEL IDENTIFICATION 

This section describes the procedure we exercise to devise UR10’s dynamic model, schematized in Figure 2. As preliminary steps, we construct the robot’s dynamic model (hence building the regressor) starting from its geometrical properties, and define the excitation trajectories to command in order to collect data used to identify the robot dynamics. The actual estimation follows a three-stage approach, consisting in the following phases: (i) identification of linear dynamic parameters in (6), described in Section III-B; (ii) computation of nonlinear friction parameters in (8), detailed in Section III-C; (iii) estimation of motor drive gains in (2), reported in Section III-D. Lastly, in Section III-E we describe how to extend the identified model to include the payload dynamics. 

## _A. Excitation Trajectories_ 

As a preliminary step, a complete identification procedure requires collecting data to estimate and validate the dynamic 

> 1Link lengths available at the manufacturer website: https://rb.gy/ xxb5k5 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/TII.2025.3534415 – IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS 

4 


Fig. 2: Estimation procedure 

parameters, which is typically done by commanding sinusoidal _excitation trajectories_ , parametrized as finite Fourier series [7] 


where **_q_** 0, **_a_** _k_ and **_b_** _k_ are Fourier coefficients, and _Tf_ is chosen to be a multiple of the robot’s sampling period. 

Once the trajectories are commanded, input/output data can be collected. Let _M_ be the number of recorded samples, and denote with _<u>•</u>_ the column-stack of a sequence of _M_ data points. Therefore, inputs **_<u>q</u>_** _<u>,</u>_ **_<u>q</u>_** ˙ _<u>,</u>_ **_<u>q</u>_** ¨ include measured kinematic states. As regards the outputs, one can measure either joint torques **_<u>τ</u>_** or, as in the case of UR10, joint currents **_<u>v</u>_** <u>.</u> 

The reader is invited to consider that designing excitation trajectories is paramount for accurate model estimation [8]. Therefore, it is worth stressing that a correct identification requires meeting the persistent excitation (PE) condition, i.e. the reference signal (16) must include sufficiently rich spectral information to properly excite the robot dynamics [7], [12]. In practice, this typically requires trajectories of units to tens of thousands of samples [3], [8], [9], [16], [18], [21], corresponding to execution times of, at most, units of minutes, assuming control frequencies in the hundreds to thousands of Hz. To this purpose, optimization of Fourier parameters has also been explored [14]. 

## _B. Linear Dynamic Parameters_ 

As known, a subset of dynamic parameters in **_π_** can be estimated only in linear combinations [15], called _dynamic coefficients_ . Hence, (6) changes to 


where **_ξ_** contains the dynamic coefficients, and **_Y_** ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨) indicates the _minimal regressor_ , computed using Singular Value Decomposition (SVD) [8], [15]. 

Retrieving **_π_** from **_ξ_** requires a further optimization approach [16], [18], and goes beyond the scope of this article, since the computation of **_τ_** from **_ξ_** in (17), in place of **_π_** in (6), can equivalently be used to compute the EOM in (1). 

Dropping the dependencies on joint variables for the sake of brevity, **_ξ_** can be estimated using either the Linear Least Square Estimation (LLSE) method [15] 


or the Weighted Least Square Estimation (WLSE) to be robust against inaccurate data [7] 


where **_W_** = diag _{_<sup>1</sup> _/_ **_σ_** _k_<sup>2</sup><sup>_}M_</sup> _k_ =1<sup>isadiagonalmatrixofweights,</sup> and **_σ_** _k_<sup>2isthevarianceofthe</sup><sup>_k_-thsamplein</sup><sup>**_<u>τ</u>_**</sup> <u>,</u> with ( _•_ )<sup>2</sup> indicating the element-wise square. Plugging (18) or (19) into (17), estimated joint torques can be retrieved for a given input state with 


When torques cannot be directly measured, but currents are available instead, (18) and (19) cannot be computed. Hence, one can rewrite (1) in terms of joint currents using (2), obtaining the following _n_ scalar equations: 


_∀j ∈{_ 1 _, . . . , n}_ . Exploiting the same linearity property as in (17), (21) becomes 


where **_χ_** ≜ [ **_χ_** 1<sup>_⊤, . . . ,_</sup><sup>**_χ_**</sup><sup>_⊤_</sup> _n_<sup>]</sup><sup>_⊤_arethecurrent-leveldynamic</sup> coefficients. Denoting the current-level minimal regressor as **_U_** ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨) ≜ blockdiag _{_ **_y_** _j_ ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨) _}_<sup>_n_</sup> _j_ =1<sup>,(19)becomes</sup> 


and (20) translates into 


To summarize, the first step of the identification procedure consists in computing the current-level minimal regressor **_U_** from the torque-level equivalent **_Y_** , and estimating currentlevel dynamic coefficients **_χ_** after collecting data ( **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨ _,_ **_v_** ): estimated currents **_v_** ˆ are finally computed with (25). In the light of the discussion in Section II-B, one should consider that (25) holds if and only if the complement of (9) is satisfied, i.e. _|_ **_q_** ˙ _| > q_ ˙<sup>+</sup> , i.e. where the joint friction currents behave linearly according to (7). 

PETRONE _et al._ : THE DYNAMIC MODEL OF THE UR10 ROBOT AND ITS ROS2 INTEGRATION 

5 

## _C. Nonlinear Friction Parameters_ 

In the second stage of our estimation procedure, we estimate the set of nonlinear friction parameters, denoted with **_ψ_** ≜<sup>�</sup><sup>_n_</sup> _j_ =1<sup>**_ψ_**</sup> _j_<sup>,where</sup><sup>**_ψ_**</sup> _j_<sup>≜</sup><sup>_{fo,j, fv,j, fc,j, δj, νj}_.Given</sup> the dynamic coefficients identified in (24), we compute the estimated friction currents as 


where **_U_** _f_ (resp. **_χ_** ˆ _f_ ) includes the columns (resp. rows) of **_U_** (resp. **_χ_** ˆ ), excluding the linear friction parameters **_f_** _o,_ **_f_** _v,_ **_f_** _c_ . 

Given a set of parameters **_ψ_** , we denote with **_f ψ_** ( ˙ **_q_** ) the joint friction torques in (8) evaluated with **_ψ_** ; hence, we define the corresponding joint friction currents as **_vψ_** ( ˙ **_q_** ) ≜ **_K_**<sup>_−_1</sup> **_f ψ_** ( ˙ **_q_** ). Finally, we estimate the friction parameters by solving the following nonlinear optimization problem: 


with **_<u>v</u>_** ˆ _~~f~~_<sup>( ˙</sup><sup>**_q_**)and</sup><sup>**_<u>v</u>_**</sup> **_~~ψ~~_**<sup>( ˙</sup><sup>**_q_**)representing,inthiscase,thecolumn-</sup> stack of **_v_** ˆ _f_ and **_vψ_** evaluated on the samples s.t. _|_ **_q_** ˙ _| < q_ ˙<sup>+</sup> holds, thus exhibiting the sigmoidal characteristics in (8). 

Notably, (27) replaces the linear friction parameters estimated in (24), fitting them to the nonlinear formulation. Finally, the estimated currents are 


Readers should be aware that joint friction estimation for industrial robots is currently an active research topic [25]. Indeed, solving the nonlinear problem (27) with a seeddependent algorithm does not guarantee a globally optimal solution: this well-known issue is typical of gradient-based solvers (also adopted by, e.g., [3], [21]). Exploring the most suitable friction model and resolution algorithm falls outside the scope of this article, since this particular sub-problem requires further specific investigation. 

## _D. Motor Drive Gains_ 

Once the currents are estimated with (28), the third and final stage of our estimation procedure is performed, i.e., **_v_** ˆ are converted into **_τ_** ˆ. According to (2), once the motor drive gains **_K_**<sup>ˆ</sup> are estimated, the following relationship holds: 


In this work, we replicate the procedure performed by [21] on our manipulator to compute **_K_**<sup>ˆ</sup> . This section reports and clarifies its steps, for the sake of completeness. 

First, the algorithm requires the execution of a set of trajectories run with the manipulator arm only (let us denote this scenario with _a_ ), and a set of trajectories run with the robot holding a payload (scenario _b_ ). After the trajectories are executed, _M_ samples are collected, with _M_ ≜ _M_<sup>_a_</sup> + _M_<sup>_b_</sup> . As regards the payload dynamic parameters **_π_** _L_ , it is assumed that only a certain number _c_ of them are unknown. This is a reasonable assumption since, for instance, one can simply use a scale to obtain the payload mass _mL_ at least, thus _c ≤_ 9 is assumed to hold in general. Hence, **_π_** _L_ can be partitioned into **_π_** _uL_ and **_π_** _kL_ , i.e., the sets of unknown and known payload dynamic parameters, respectively. 

Consider the following equation, holding for the _j_ -th joint: 


simplified as 

where **_<u>v</u>_** _~~j~~_<sup>_−_</sup><sup>**_<u>v</u>_**</sup> **_~~ψ~~_** ˆ _,j_<sup>≜[(</sup><sup>**_<u>v</u>_**</sup> _a_ _~~j~~_<sup>_−_</sup><sup>**_<u>v</u>_**</sup> _a_ **_~~ψ~~_** ˆ _,j_<sup>)</sup><sup>_⊤,_</sup><sup><u>(</u></sup><sup>**_<u>v</u>_**</sup> _b_ _~~j~~_<sup>_−_</sup><sup>**_<u>v</u>_**</sup> _b_ **_~~ψ~~_** ˆ _,j_<sup>)</sup><sup>_⊤_]</sup><sup>_⊤_stacks</sup> the _linear_ current samples collected in scenarios _a_ and _b_ respectively, **_χ_** _f,j_ are the rows of **_χ_** _j_ excluding linear friction parameters, **_<u>u</u>_** _a_ _~~f~~ ,j_<sup>and</sup><sup>**_<u>u</u>_**</sup> _b_ _~~f~~ ,j_<sup>arethecolumn-stacksof</sup><sup>**_u_**</sup><sup>_f,j_(i.e.,</sup> the _j_ -th row of **_U_** _f_ ) evaluated on kinematic states measured in scenarios _a_ and _b_ respectively, and **_<u>p</u>_** _~~u~~ L,j_<sup>(resp.</sup><sup>**_<u>p</u>_**</sup> _~~k~~ L,j_<sup>)</sup> is a column-stack of **_p_** _uL,j_ (resp. **_p_** _kL,j_ ), namely the _j_ -th row of **_P_** _uL_ (resp. **_P_** _kL_ ), i.e. the regressor w.r.t. **_π_** _uL_ (resp. **_π_** _kL_ ), evaluated on input samples retrieved in scenario _b_ . Since (30) uses a linear model, for the sake of clarity we highlight that henceforth all the kinematics-dependent variables are considered to be evaluated on samples in the linearity region only. 

Similarly to (19), _∀j ∈{_ 1 _, . . . , n}_ , **_S_** _j_ is used to estimate **_ζ_** _j_ with WLSE: 


Then, _K_<sup>ˆ</sup> _j_ can be simply extracted from **_ζ_**<sup>ˆ</sup> _j_ with 


However, there might exist a joint _j_<sup>_∗_</sup> for which the matrices _{_ **_S_** _j}_<sup>_n_</sup> _j_<sup>_∗_arerank-deficient;thus,</sup><sup>_{Kj}n_</sup> _j_<sup>_∗_cannotbedirectly</sup> estimated, as **_ζ_** _j_ combines linearly with other parameters. In these cases, **_ζ_** _j_ must be partitioned into two parts: 


where **_ϕ_** _j_ and **_φ_** _j_ represent the identifiable and unidentifiable parameters, respectively. Denoting the size of **_φ_** _j_ with _|_ **_φ_** _j|_ , the following equation holds, according to the QR decomposition of **_S_** _j_ : 


where **_β_** _j_ ≜ **_ϕ_** _j_ + **_R_**<sup>_†_</sup> _j,ϕ_<sup>**_R_**</sup><sup>_j,φ_</sup><sup>**_φ_**</sup><sup>_j_istheregroupingvector</sup> of **_ζ_** _j_ ; **_S_** _j,ϕ_ and **_S_** _j,φ_ contain the linearly independent and dependent columns of **_S_** _j_ , respectively, and **_Q_** _j,ϕ_ , **_Q_** _j,φ_ , **_R_** _j,ϕ_ and **_R_** _j,φ_ are, respectively, the orthogonal and upper triangular matrices of **_S_** _j,ϕ_ and **_S_** _j,φ_ , with _•_<sup>_†_</sup> indicating the MoorePenrose pseudo-inverse. 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/TII.2025.3534415 – IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS 

6 

After the QR factorization of **_S_** _j_ , the following optimization problem must be solved to extract _K_<sup>ˆ</sup> _j_ : 


where _K_<sup>_−_</sup> and _K_<sup>+</sup> are minimum and maximum bounds to _j j_ impose on _Kj_ . 


(a) Schunk Gripper (b) Franka Hand 

Fig. 3: Payloads 

TABLE II: Franka Hand inertial parameters 

## _E. Payload Integration_ 

Rewriting (6) to separate the _n_ -th link, one has: 

|**Mass [**kg**]**|**COM **|**[**mm**]**|**Inertia matrix **|**[**gm<sup>2</sup>**]**|
|---|---|---|---|---|
|_m_|_cx_<br>_cy_|_cz_|_Ixx_<br>_Iyy_|_Izz_|
|0.73|0<br>10|30|1<br>2.5|1.7|


where **_P_** 1: _n−_ 1 represents the columns of the regressor matrix related to the dynamic parameters of links from 1 to _n −_ 1, **_P_** _n_ contains the columns related to link _n_ only, and **_π_** 1: _n−_ 1 ≜ [ **_π_** 1<sup>_⊤, . . . ,_</sup><sup>**_π_**</sup><sup>_⊤_</sup> _n−_ 1<sup>]</sup><sup>_⊤_.</sup> 

In virtue of (15), in the presence of a payload, (37) changes to 


where **_τ_** _arm_ are the torques due to the arm motion only and **_τ_** _L_ are those due to the payload. Therefore, once **_τ_** _arm_ is estimated and **_π_** _L_ is known, one can obtain the joint torques of the composed arm-payload system **_τ_** simply using the regressor **_P_** _n_ (which only contains kinematic information) and **_π_** _L_ . The latter is typically known from the datasheet, as the one that will be used in Section IV-C, or can be estimated separately, as in [17]. 

## IV. EXPERIMENTAL RESULTS 

In this section, we report the results of the estimation of the dynamic coefficients of the UR10 robot, shown in Fig. 1. 

## _A. Task Setup & Materials_ 

_1) Manipulator:_ To acquire input/output data from the 6- DOF UR10 manipulator, we use a Python library provided by the manufacturer<sup>2</sup> , from which we can measure **_q_** , **_q_** ˙ and **_v_** , whereas **_q_** ¨ can be computed using the backward Euler approximation from **_q_** ˙. To cope with the inherent noise of **_q_** ¨ [29], due to the inescapable measurement noise of **_q_** ˙ further deteriorated by discrete differentiation, the time history of the acquired samples is filtered out of high-frequency noise with a low-pass filter, implemented in MATLAB using the designfilt function. Excitation trajectories in the shape of (16) are commanded using a ros ~~c~~ ontrol [30] positionbased joint trajectory controller, through the ROS driver developed by UR<sup>3</sup> . Two of the excitation trajectories we defined are used as validation set: henceforth, they will be referred to as Trajectory A and Trajectory B. 

_2) Payload:_ In our experiments we use two different payloads (Fig. 3): a Schunk PSH-32/1 gripper (Fig. 3a) to estimate the motor gains according to the procedure defined in Section III-D, and the Franka Hand (Fig. 3b) to validate our configurable IDS. As regards the former, we only know its mass (hence _c_ = 9) by weighing, i.e. _mL_ = 4 _._ 823 kg, while the inertial parameters of the latter are known from the datasheet<sup>4</sup> and reported in Table II. 

_3) Software:_ Our UR10 IDS exposes interfaces, written in C++, to extract **_H_** ( **_q_** ), **_C_** ( **_q_** _,_ **_q_** ˙) ˙ **_q_** , **_f_** ( ˙ **_q_** ), **_g_** ( **_q_** ) or **_τ_** . The payload inertial parameters can be added in a separate configuration file, without any change to the software itself, thanks to the implementation of (38) separating **_τ_** _arm_ and **_τ_** _L_ . Readers are invited to visit our public repository<sup>5</sup> and consult the related documentation to easily get acquainted with the solver and perform demos and unit tests. Further details on the IDS are given in Section IV-D. The estimations (24), (32) are implemented using the robustfit function, which automatically computes **_W_** and applies WLSE. The optimization problem (27) is solved with fminunc setting _q_ ˙<sup>+</sup> := 0 _._ 17 rad _/_ s, whereas (36) is solved with lsqlin, as it is a LLSE problem, choosing _Kj_<sup>_−_</sup> := 10 N m _/_ A and _Kj_<sup>+:= max</sup><sup>_i∈{_1</sup><sup>_,...,j−_1</sup><sup>_}Ki_.</sup> _4) Performance indices:_ With 


we denote the Mean Squared Error (MSE) between two generic vectors **_x_** _,_ **_y_** _∈_ R<sup>_ς_</sup> , and with 


we define the Mean Normalized Absolute Error (MNAE) between **_x_** and **_y_** , i.e. the percentage of how much **_y_** deviates from **_x_** , normalized against the range of the samples in **_x_** . The index (40) is particularly useful in fairly assessing our estimated currents accuracy, e.g. with MNAE( **_v_** _j,_ ˆ **_v_** _j_ ), in that 

> 2https://rb.gy/dnuvs9 

> 3https://rb.gy/nhd821 

> 4https://rb.gy/l8wb9y 

> 5https://codeocean.com/capsule/8515919/tree/v2 

PETRONE _et al._ : THE DYNAMIC MODEL OF THE UR10 ROBOT AND ITS ROS2 INTEGRATION 

7 

TABLE III: MNAE( **_v_** _j,_ ˆ **_v_** _j_ ) in validation trajectories 

|**Joint**|**T**<br>[3]|**rajectory A**<br>ours|_η_|**T**<br>[3]|**rajectory B**<br>ours|_η_|
|---|---|---|---|---|---|---|
|Joint 1|23.2838|10.0031|2.3277|15.6990|6.0429|2.5979|
|Joint 2|5.4332|3.6834|1.4751|4.8266|4.4326|1.0889|
|Joint 3|5.6983|2.1738|2.6214|5.0099|1.5387|3.2559|
|Joint 4|10.3336|5.9348|1.7412|9.8104|5.6306|1.7423|
|Joint 5|35.7345|8.0699|4.4281|32.7093|11.1431|2.9354|
|Joint 6|28.3407|8.3120|3.4096|23.5660|5.4544|4.3205|


TABLE VI: MNAE( **_τ_** _j,_ ˆ **_τ_** _j_ ) obtained by validating the dynamics solver against different payload configurations 

|**Joint**|**Scenario 1**|**Scenario 2**|**Scenario 3**|
|---|---|---|---|
|Joint 1|4.3672|4.0876|4.1121|
|Joint 2|3.3818|3.8360|3.1968|
|Joint 3|3.0961|4.6370|1.5898|
|Joint 4|9.1918|8.3397|8.5546|
|Joint 5|10.1428|13.7379|11.2278|
|Joint 6|8.8053|8.2813|8.2736|
|**Average**|6.4975|7.1533|6.1591|


TABLE IV: Estimated nonlinear friction parameters 

|**Joint**|**_f_**_v_|**_f_**_o_|**_f_**_c_|**_α_**|**_ν_**|
|---|---|---|---|---|---|
|Joint 1|1.0640|-1.0066|2.0506|7.9467|-0.0185|
|Joint 2|0.9944|0.9563|-2.4017|-59.9536|-0.0019|
|Joint 3|0.6796|-0.8120|1.6478|19.8251|-0.0053|
|Joint 4|0.3159|-0.1767|0.4688|134.8982|-0.0186|
|Joint 5|0.2244|-0.1924|0.4760|331.4421|-0.0118|
|Joint 6|0.2358|-0.2453|0.5980|459.1933|-0.0130|


the estimation error is weighted differently depending on the actual current domain. 

## _B. Dynamic Model Estimation_ 

_1) Joint Currents:_ Fig. 4 shows the comparison between the joint currents estimated by [3] and the currents estimated with our method, defined in Section III-B and III-C. Table III presents the numerical evaluation: as confirmed by the plots, we achieve a lower prediction error across all joints against both the validation trajectories, manifesting the superior performance of our model and demonstrating the efficacy of a dynamic estimation of **_v_** against a static retrieval of **_g_** ( **_q_** ) only. Remarkably, we achieve a maximum improvement factor of _η_ = 4 _._ 4281 and _η_ = 4 _._ 3205 in trajectories A and B respectively, with _η >_ 1 for all the joints in both trajectories. 

We point out that larger prediction errors are due to nonlinear effects: consider, for instance, the nonlinear regions in _t ∈_ [7 _._ 5 _,_ 10]s for Joint 6 in Trajectory A, or in _t ∈_ [12 _._ 5 _,_ 15]s for Joint 6 in Trajectory B. Indeed, for _|q_ ˙6 _| < q_ ˙, we attained an MNAE index of 25 _._ 8714 and 26 _._ 8361, respectively, which is considerably higher than the same index computed for all samples. Notably, this phenomenon is more evident for the last joints, for which the friction contribution plays a substantial role on the overall dynamics, compared to other effects. 

_2) Nonlinear Friction Parameters:_ After estimating the linear parameters, the nonlinear friction parameters are estimated by using the procedure described in Section III-C and reported in Table IV. The friction currents are illustrated in Fig. 5. It is evident from the plots that **_<u>v</u>_** ˆ _~~f~~_<sup>( ˙</sup><sup>**_q_**)behavesnonlinearlyfor</sup> _|_ **_q_** ˙ _| < q_ ˙<sup>+</sup> , hence a sigmoidal model (8) is fitted on them, while they tend to follow the linear model in (7) for _|_ **_q_** ˙ _| > q_ ˙<sup>+</sup> . 

_3) Motor Drive Gains:_ To estimate the motor drive gains **_K_** , we exercise the procedure described in Section III-D, 

TABLE V: Estimated joint motor drive gains [N m _/_ A] 

|**Joint**|**GT**|**[3]**|**[21]**|**ours**|
|---|---|---|---|---|
|Joint 1|13.9557|14.87|14.7336|13.5841|
|Joint 2|13.8669|13.26|14.3300|14.2959|
|Joint 3|11.5049|11.13|11.5476|11.3716|
|Joint 4|11.5438|10.62|11.2487|11.2408|
|Joint 5|11.6143|11.03|11.5000|11.7682|
|Joint 6|11.4149|11.47|11.5000|11.7681|
|**MSE w.r.t. GT**|0|1.5946|0.9637|0.7617|


originally developed in [21], by attaching an eccentrically mounted payload, according to the EE frame shown in Fig. 3a. More specifically, _j_<sup>_∗_</sup> = _n −_ 1, i.e., **_S_** _n−_ 1 and **_S_** _n_ are rankdeficient for the UR10 kinematic structure, hence (36) is solved for gains _Kn−_ 1 and _Kn_ . 

Table V reports the joint motor drive gains estimated in [3] and [21], as well as our estimation. On the one hand, [3] uses a procedure foreseeing a sequence of 500 static configurations as data samples to estimate the motor gains, based on the difference between the measured currents with and without holding an eccentric payload; this requires _K_ 1 to be estimated separately. On the other hand, we make use of a dynamic procedure, as in [21], i.e. we collect data from the execution of a set of trajectories, allowing a one-shot estimation of **_K_** . 

We compare our estimated gains with those obtained by the aforementioned baselines. As ground-truth (GT), we measure a certain number _N ∈_ N of samples in different static configurations, and compute the motor gains as 


where _τd,j_<sup>(</sup><sup>_k_)and</sup><sup>_v_</sup> _d,j_<sup>(</sup><sup>_k_)indicatethe</sup><sup>_k_-thsampleof,respectively,</sup> the target torques and currents commanded to the joints, both acquired through the software provided by the manufacturer. The results collected in Table V show that, although a significant improvement is already achieved by [21] compared to [3], an additional increase of accuracy is attained by replicating [21] on our robot. This suggests the necessity of performing the motor drive gains estimation from scratch for each industrial manipulator, as **_K_** might differ because of unavoidable manufacturing inaccuracies in the motors production. 

## _C. Payload Integration_ 

The integration of a payload attached to the EE flange is assessed with 3 experimental scenarios: 

Scenario 1) a trajectory is run without the robot holding a payload, **_Kv_** ˆ are comparedthe torqueswithcomputedthe estimationsfrom measuredof the IDScurrentsconfigured **_τ_** = without a payload; 

Scenario 2) the trajectory is run with the robot holding a payload (i.e., the hand in Fig. 3b), the torques computed from measured currents are compared with the estimations of the IDS configured without a payload; 

Scenario 3) the trajectory is run with the robot holding the payload, the torques computed from measured currents are compared with the estimations of the IDS configured with the payload inertial parameters in Table II. 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/TII.2025.3534415 – IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS 

8 


Fig. 4: Measured and estimated joint currents in Trajectory A (first two rows) and Trajectory B (last two rows) 


Fig. 5: Measured and estimated joint friction currents 

Equation (38) is implemented in our IDS with 


i.e. Franka Hand is concentrically mounted with a 45<sup>_◦_</sup> rotation around _z_ 6, attached without any translational offset. 

Table VI shows that, compared to Scenario 1, the estimation error increases in Scenario 2, demonstrating the decrease of performance when the IDS ignores the actual presence of the payload. In contrast, when the solver is properly configured in Scenario 3, an improvement is attained. Fig. 6 shows the measured and estimated joint torques in scenarios 2 and 3. It is worth pointing out that differences in the performance between the scenarios might be more evident with a more dynamically exciting payload. In fact, Franka Hand’s mass ( _<_ 1 kg) is rather limited compared to the manipulator capacity (10 kg). 

## _D. Software Implementation_ 

Our UR10 dynamics solver is a C++ software library developed according to the ROS2 framework. Once the modeling and identification procedure described in Section III is performed on the UR10 robot, the estimated model implementing equations (28)–(29) is converted from MATLAB symbolic equations to C++ functions using the matlabFunction method and the MATLAB Coder Toolbox. 

_1) Functionalities:_ The IDS library exposes functions to allow the user to extract **_H_** ( **_q_** ), **_C_** ( **_q_** _,_ **_q_** ˙) ˙ **_q_** , **_f_** ( ˙ **_q_** ), **_g_** ( **_q_** ) or **_τ_** . In particular, while **_τ_** is computed according to (29), with **_v_** calculated as (28), all the dynamics terms are retrieved using “partial” regressors and dynamic coefficients, constructed considering only the portions of the EOM in (1) describing each particular term. Mathematical details on how to implement the EOM can be found in [22]. Moreover, it is possible to configure the solver with the payload parameters by reading a YAML file, a common format used by the ROS2 community. A _launch file_ is responsible for both loading the configuration file and instantiating and configuring the IDS, which reads the payload parameters at instantiation time. 

_2) Architecture:_ The software architecture is composed by an abstract class, named InverseDynamicsSolver, providing the functionalities mentioned in Section IV-D.1: this class represents a generic solver, and the particular implementation of the methods returning dynamic components is a responsibility of the concrete classes. The actual UR10’s IDS, named InverseDynamicsSolverUR10, is one of the two concrete implementations of the abstract class we provide: this class returns the torques for the specific manipulator under study, according to the estimated model. Additionally, the abstract class is inherited by InverseDynamicsSolverKDL, which computes the dynamic components through the KDL library, after reading the robot description from URDF files: 

PETRONE _et al._ : THE DYNAMIC MODEL OF THE UR10 ROBOT AND ITS ROS2 INTEGRATION 

9 


Fig. 6: Estimated joint torques compared to torques computed from measured currents 

this class is useful when a complete kinematic and dynamic description is available, e.g. in the case both the DH and dynamic parameters are provided by the manufacturer. Lastly, it is worth remarking that users in the ROS2 community are allowed to inherit the base class with their own implementations, possibly including the estimated models of other manipulators. 

_3) Implementation details:_ The IDS defines the input/output types of the implemented methods using Eigen, a popular C++ linear algebra library. This way, users can easily manipulate the computed matrices for model based applications, such as writing control schemes or evaluating planning algorithms [2]. For further details, interested readers are referred to the supplementary code capsule. 

## V. CONCLUSIONS 

This paper introduced the dynamic model of the UR10 industrial robot, and presented the identification procedure performed to estimate the manipulator’s dynamic coefficients. The complete identification process is composed of three subsequent stages, to face several issues due to the structural nature of the robot. 

The first step consists in devising linear dynamic coefficients to retrieve the estimated joint currents, according to a well-known linear least square solution, hence obtaining a linear current-level dynamic model, as joint torques are not directly measurable. Since the joint currents exhibit a nonlinear behavior due to joint friction, the second phase requires establishing a nonlinear optimization problem, to fit a set of friction parameters to a sigmoidal model. The third and last stage finally outputs joint torques: indeed, it concerns the estimation of motor drive gains, to convert the current-level dynamic model to the joint torque level. 

Compared to the current-level model identified in [3], we consistently achieved a lower estimation error on all the joints, validated against 2 exciting trajectories; however, the adopted procedure still presents the major flaw of lacking a global solution for the nonlinear optimization problem to devise friction parameters. The estimated torque-level dynamic model has been implemented in a ROS2 software module we developed and released, that can be used off-the-shelf in a variety of control, planning, and simulation applications. The IDS is validated in various scenarios, also foreseeing the inclusion of a payload, demonstrating that the software can be reconfigured to account for a generic known payload. 

In future research, we aim to refine excitation trajectory design. Currently, reference joint sinusoid parameters are chosen heuristically to explore the robot’s workspace. In this sense, investigating the impact of optimal excitation trajectory computation [14] on parameter estimation accuracy during validation would be a valuable improvement. Alternatively, adopting online identification approaches could prove particularly beneficial by eliminating the need for designing trajectories tailored to meet the PE condition [27], thereby simplifying the process and potentially enhancing efficiency. 

Additionally, we intend to explore alternative friction models, such as those incorporating the Stribeck effect [24] or degressive friction [26]. To address the challenge of globally optimizing nonlinear friction parameter estimation, we might employ resolution techniques like evolutionary algorithms [25] or neural networks [27]. 

Finally, training the model on data averaged across multiple identical trajectories, rather than relying on single trajectories with low-pass filtering, could enhance current prediction accuracy by mitigating measurement noise without distorting high-frequency motion signals. 

## ACKNOWLEDGMENT 

The authors would like to thank Giovanni Mignone and Antonio Annunziata for refining the implementation of the identification procedure, making this work possible. 

LIST OF SYMBOLS 

_n ∈_ N number of degrees of freedom **_q_** _,_ **_q_** ˙ _,_ **_q_** ¨ _∈_ R<sup>_n_</sup> joint positions, velocities, accelerations **_H_** _∈_ R<sup>_n×n_</sup> inertia matrix **_h_** _j ∈_ R<sup>1</sup><sup>_×n_</sup> _j_ -th row of **_H C_** _∈_ R<sup>_n×n_</sup> centrifugal and Coriolis matrix **_c_** _j ∈_ R<sup>1</sup><sup>_×n_</sup> _j_ -th row of **_C f_** _∈_ R<sup>_n_</sup> friction torques **_g_** _∈_ R<sup>_n_</sup> gravity torques **_τ_** _,_ **_v_** _∈_ R<sup>_n_</sup> joint torques, currents **_K_** _∈_ R<sup>_n×n_</sup> diagonal matrix of joint motor drive gains _•j_ quantity ( _•_ ) for the _j_ -th joint _m ∈_ R+ mass **_r_** _∈_ R<sup>3</sup> center of mass **_I_** ˇ _∈_ R<sup>3</sup><sup>_×_3</sup> inertia tensor relative to the principal axes of inertia **_I_** _∈_ R<sup>3</sup><sup>_×_3</sup> inertia tensor relative to the kinematic frame **_π_** _∈_ R<sup>10</sup><sup>_n_</sup> dynamic parameters _•i_ quantity ( _•_ ) for the _i_ -th link 

ACCEPTED VERSION, PUBLISHED AT HTTPS://DOI.ORG/10.1109/TII.2025.3534415 – IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS 

10 

**_π_** 1: _n−_ 1 _∈_ R<sup>10(</sup><sup>_n−_1)</sup> dynamic parameters of links 1 _, . . . , n p ∈_ N number of dynamic coefficients **_ξ_** _∈_ R<sup>_p_</sup> dynamic coefficients 

**_χ_** _∈_ R<sup>_pn_</sup> current-level dynamic coefficients **_P_** _∈_ R<sup>_n×_10</sup><sup>_n_</sup> regressor 

- **_P_** 1: _n−_ 1 _∈_ R<sup>_n×_10(</sup><sup>_n−_1)</sup> columns of **_P_** related to **_π_** 1 _, . . . ,_ **_π_** _n−_ 1 

- **_P_** _n ∈_ R<sup>_n×_10</sup> columns of **_P_** related to **_π_** _n_ **_Y_** _∈_ R<sup>_n×p_</sup> minimal regressor **_y_** _j ∈_ R<sup>1</sup><sup>_×p_</sup> _j_ -th row of **_Y_** 

**_U_** _∈_ R<sup>_n×pn_</sup> current-level minimal regressor 

**_u_** _j ∈_ R<sup>1</sup><sup>_×pn_</sup> _j_ -th row of **_U_** 

- **_W_** diagonal matrix of weights for WLSE **_σ_** _k_<sup>2</sup><sup>_∈_R</sup><sup>_n_varianceofthe</sup><sup>_k_-thsamplein</sup><sup>**_<u>τ</u>_**</sup> or **_<u>v</u> v_** _f ∈_ R<sup>_n_</sup> joint currents due to friction 

**_f_** _o ∈_ R<sup>_n_</sup> Coulomb friction offset 

**_f_** _v ∈_ R<sup>_n_</sup> viscous friction 

**_f_** _c ∈_ R<sup>_n_</sup> Coulomb friction coefficient 

**_δ_** _∈_ R<sup>_n_</sup> nonlinear friction multiplicative factor 

**_ν_** _∈_ R<sup>_n_</sup> nonlinear friction additive factor 

**_ψ_** set of friction parameters 

**_f ψ_** _∈_ R<sup>_n_</sup> nonlinear friction torques **_f_** evaluated on **_ψ_** 

- **_vψ_** _∈_ R<sup>_n_</sup> nonlinear friction currents evaluated on **_ψ χ_** _f ∈_ R<sup>(</sup><sup>_p−_3)</sup><sup>_n_</sup> **_χ_** excluding **_f_** _o_ , **_f_** _v_ , **_f_** _c_ 

- **_U_** _f ∈_ R<sup>_n×_(</sup><sup>_p−_3)</sup><sup>_n_</sup> **_U_** excluding columns related to **_f_** _o_ , **_f_** _v_ , **_f_** _c_ **_u_** _f,j ∈_ R<sup>1</sup><sup>_×_(</sup><sup>_p−_3)</sup><sup>_n_</sup> _j_ -th row of **_U_** _f_ 

_c ∈_ N number of unknown payload dynamic parameters 

- _•l_ quantity ( _•_ ) for payload w.r.t. payload origin frame 

- _•L_ quantity ( _•_ ) for payload w.r.t. _n_ -th link frame **_R_** _n_<sup>_l∈SO_(3)rotationofframe</sup><sup>_l_w.r.t.</sup><sup>_n_-thlinkframe</sup> **_t_**<sup>_l_</sup> _n_<sup>_∈_R3translationofframe</sup><sup>_l_w.r.t.</sup><sup>_n_-thlinkframe</sup> **_T_** _n_<sup>_l∈SE_(3)transformationofframe</sup><sup>_l_w.r.t.</sup><sup>_n_-thlinkframe</sup> 

- **_π_** _uL ∈_ R<sup>_c_</sup> unknown payload dynamic parameters **_π_** _kL ∈_ R<sup>10</sup><sup>_−c_</sup> known payload dynamic parameters 

- **_P_** _uL ∈_ R<sup>_n×c_</sup> regressor w.r.t. **_π_** _uL_ **_P_** _kL ∈_ R<sup>_n×_(10</sup><sup>_−c_)</sup> regressor w.r.t. **_π_** _kL_ 

- **_p_** _uL,j ∈_ R<sup>1</sup><sup>_×c_</sup> _j_ -th row of **_P_** _uL_ 

- **_p_** _kL,j ∈_ R<sup>1</sup><sup>_×_(10</sup><sup>_−c_)</sup> _j_ -th row of **_P_** _kL_ 

- **_τ_** _arm ∈_ R<sup>_n_</sup> joint torques due to arm motion only **_τ_** _L ∈_ R<sup>_n_</sup> joint torques due to payload 

- _F ∈_ N number of Fourier components in exciting trajectories _M ∈_ N number of samples acquired with exciting trajectories _N ∈_ N number of samples acquired in static conditions **_q_** 0 _,_ **_a_** _k,_ **_b_** _k ∈_ R<sup>_n_</sup> excitation trajectory parameters 

- <sup>_a_</sup> quantity ( _•_ ) for trajectories executed without payload 

- <sup>_b_</sup> quantity ( _•_ ) for trajectories executed with payload 

- **_S_** _j ∈_ R<sup>_M×_(</sup><sup>_p_+</sup><sup>_c−_2)</sup> regressor to estimate _Kj_ **_ζ_** _j ∈_ R<sup>_p_+</sup><sup>_c−_2</sup> vector including arm coefficients and _Kj_ **_µ_** _j ∈_ R<sup>1</sup><sup>_×_(</sup><sup>_p_+</sup><sup>_c−_2)</sup> decision vector to extract _Kj_ from **_ζ_** _j dj ∈_ N number of identifiable parameters in **_ζ_** _j_ **_ϕ_** _j ∈_ R<sup>_dj_</sup> identifiable parameters in **_ζ_** _j_ **_φ_** _j ∈_ R<sup>_p_+</sup><sup>_c−_2</sup><sup>_−dj_</sup> unidentifiable parameters in **_ζ_** _j_ 

- **_S_** _j,ϕ ∈_ R<sup>_M×dj_</sup> linearly independent columns of **_S_** _j_ 

- **_S_** _j,φ ∈_ R<sup>_M×_(</sup><sup>_p_+</sup><sup>_c−_2</sup><sup>_−dj_)</sup> linearly dependent columns of **_S_** _j_ **_Q_** _j,ϕ,_ **_Q_** _j,φ ∈_ R<sup>_M×M_</sup> orthogonal matrix of **_S_** _j,ϕ_ , **_S_** _j,φ_ **_R_** _j,ϕ ∈_ R<sup>_M×dj_</sup> upper triangular matrix of **_S_** _j,ϕ_ **_R_** _j,φ ∈_ R<sup>_M×_(</sup><sup>_p_+</sup><sup>_c−_2</sup><sup>_−dj_)</sup> upper triangular matrix of **_S_** _j,φ_ **_β_** _j ∈_ R<sup>_dj_</sup> regrouping vector of **_ζ_** _j_ 

- [ _•_ ] _× ∈_ R<sup>3</sup><sup>_×_3</sup> skew-symmetric operator applied to vector ( _•_ ) ˆ _•_ estimation of quantity ( _•_ ) 

- _∈_ R<sup>_Mx×y_</sup> column-stack of quantity ( _•_ ) _∈_ R<sup>_x×y_</sup> 

- <sup>_−_</sup> _, •_<sup>+</sup> lower/upper bounds on quantity ( _•_ ) 

- _η ∈_ R+ improvement factor of MSE( **_v_** _j,_ ˆ **_v_** _j_ ) w.r.t. [3] 

## REFERENCES 

- [1] K. Lu, H. Yu, Z. Liu, S. Han, and J. Yang, “Inverse Optimal Adaptive Control of Canonical Nonlinear Systems With Dynamic Uncertainties and Its Application to Industrial Robots,” _IEEE Trans. Ind. Inform._ , vol. 20, no. 4, pp. 5318–5327, Apr. 2024. 

- [2] V. Petrone, E. Ferrentino, and P. Chiacchio, “Time-Optimal Trajectory Planning With Interaction With the Environment,” _IEEE Robot. Automat. Lett._ , vol. 7, no. 4, pp. 10 399–10 405, Oct. 2022. 

- [3] C. Gaz, E. Magrini, and A. De Luca, “A model-based residual approach for human-robot collaboration during manual polishing operations,” _Mechatronics_ , vol. 55, pp. 234–247, Nov. 2018. 

- [4] S. Zhang, S. Wang, F. Jing, and M. Tan, “A Sensorless Hand Guiding Scheme Based on Model Identification and Control for Industrial Robot,” _IEEE Trans. Ind. Inform._ , vol. 15, no. 9, pp. 5204–5213, Sept. 2019. 

- [5] X. Xing, K. Maqsood, C. Zeng, C. Yang, S. Yuan, and Y. Li, “Dynamic Motion Primitives-Based Trajectory Learning for Physical Human–Robot Interaction Force Control,” _IEEE Trans. Ind. Inform._ , vol. 20, no. 2, pp. 1675–1686, Feb. 2024. 

- [6] W. Yang, S. Li, Z. Li, and X. Luo, “Highly Accurate Manipulator Calibration via Extended Kalman Filter-Incorporated Residual Neural Network,” _IEEE Trans. Ind. Inform._ , vol. 19, no. 11, pp. 10 831–10 841, Nov. 2023. 

- [7] J. Swevers, W. Verdonck, and J. De Schutter, “Dynamic Model Identification for Industrial Robots,” _IEEE Contr. Syst. Mag._ , vol. 27, no. 5, pp. 58–71, Oct. 2007. 

- [8] G. Antonelli, F. Caccavale, and P. Chiacchio, “A systematic procedure for the identification of dynamic parameters of robot manipulators,” _Robotica_ , vol. 17, no. 4, pp. 427–435, July 1999. 

- [9] C. Gaz, F. Flacco, and A. De Luca, “Identifying the dynamic model used by the KUKA LWR: A reverse engineering approach,” in _Proc. IEEE Int. Conf. Robot. Automat._ , Hong Kong, China, May 2014, pp. 1386–1392. 

- [10] J. M. Hollerbach, “A Recursive Lagrangian Formulation of Maniputator Dynamics and a Comparative Study of Dynamics Formulation Complexity,” _IEEE Trans. Syst., Man, Cybern._ , vol. 10, no. 11, pp. 730–736, Nov. 1980. 

- [11] J.-J. E. Slotine, “Putting physics in control - the example of robotics,” _IEEE Contr. Syst. Mag._ , vol. 8, no. 6, pp. 12–18, Dec. 1988. 

- [12] K. Guo and Y. Pan, “Composite adaptation and learning for robot control: A survey,” _Annu. Rev. Contr._ , vol. 55, pp. 279–290, 2023. 

- [13] D. Huang, C. Yang, Y. Pan, and L. Cheng, “Composite Learning Enhanced Neural Control for Robot Manipulator With Output Error Constraints,” _IEEE Trans. Ind. Inform._ , vol. 17, no. 1, pp. 209–218, Jan. 2021. 

- [14] R. Luo, S. Bao, L. Du, Z. Hu, Y. Liu, and J. Yuan, “Optimal Exciting Trajectories for Identifying Dynamic Parameters of Serial Robots,” in _Proc. IEEE. Int. Conf. Mechatron. Automat._ , Aug. 2023. 

- [15] C. G. Atkeson, C. H. An, and J. M. Hollerbach, “Estimation of Inertial Parameters of Manipulator Loads and Links,” _Int. J. Robot. Res._ , vol. 5, no. 3, pp. 101–119, Sept. 1986. 

- [16] C. Gaz, F. Flacco, and A. De Luca, “Extracting feasible robot parameters from dynamic coefficients using nonlinear optimization methods,” in _Proc. IEEE Int. Conf. Robot. Automat._ , Stockholm, Sweden, May 2016, pp. 2075–2081. 

- [17] C. Gaz and A. De Luca, “Payload estimation based on identified coefficients of robot dynamics — With an application to collision detection,” in _Proc. IEEE Int. Conf. Intell. Robots Syst._ , Vancouver, BC, Canada, Sept. 2017, pp. 3033–3040. 

- [18] C. Gaz, M. Cognetti, A. Oliva, P. Robuffo Giordano, and A. De Luca, “Dynamic Identification of the Franka Emika Panda Robot With Retrieval of Feasible Parameters Using Penalty-Based Optimization,” _IEEE Robot. Automat. Lett._ , vol. 4, no. 4, pp. 4147–4154, Oct. 2019. 

- [19] J. Swevers, F. Al-Bender, C. Ganseman, and T. Projogo, “An integrated friction model structure with improved presliding behavior for accurate friction compensation,” _IEEE Trans. Automat. Contr._ , vol. 45, no. 4, pp. 675–686, Apr. 2000. 

- [20] F. Al-Bender, V. Lampaert, and J. Swevers, “The generalized Maxwellslip model: a novel model for friction Simulation and compensation,” _IEEE Trans. Automat. Contr._ , vol. 50, no. 11, pp. 1883–1887, Nov. 2005. 

- [21] T. Xu, J. Fan, Q. Fang, Y. Zhu, and J. Zhao, “Robot dynamic calibration on current level: modeling, identification and applications,” _Nonlinear Dyn._ , vol. 109, no. 4, pp. 2595–2613, June 2022. 

PETRONE _et al._ : THE DYNAMIC MODEL OF THE UR10 ROBOT AND ITS ROS2 INTEGRATION 

11 

- [22] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, “Dynamics,” in _Robotics_ , 2nd ed., ser. Advanced Textbooks in Control and Signal Processing, M. J. Grimble and M. A. Johnson, Eds. Springer London, 2009, pp. 247–302. 

- [23] J. M. Hollerbach, W. Khalil, and M. Gautier, “Model Identification,” in _Springer Handbook of Robotics_ , 2nd ed., ser. Springer Handbooks, B. Siciliano, O. Khatib, B. Roth, G. Giralt, and H. Inoue, Eds. Springer International Publishing, 2016, pp. 113–138. 

- [24] M. A. Tadese, F. Yumbla, J.-S. Yi, W. Lee, J. Park, and H. Moon, “Passivity Guaranteed Dynamic Friction Model With Temperature and Load Correction: Modeling and Compensation for Collaborative Industrial Robot,” _IEEE Access_ , vol. 9, pp. 71 210–71 221, Apr. 2021. 

- [25] L. Ding, X. Li, Q. Li, and Y. Chao, “Nonlinear Friction and Dynamical Identification for a Robot Manipulator with Improved Cuckoo Search Algorithm,” _J. Robot._ , vol. 2018, 2018, Art. no.: 8219123. 

- [26] J. Weigand, J. G¨otz, J. Ulmen, and M. Ruskowski, “Dataset and Baseline for an Industrial Robot Identification Benchmark,” 2023. [Online]. Available: https://doi.org/10.26204/data/5 

- [27] K. Guo, Y. Pan, and H. Yu, “Composite Learning Robot Control With Friction Compensation: A Neural Network-Based Approach,” _IEEE Trans. Ind. Electron._ , vol. 66, no. 10, pp. 7841–7851, Oct. 2019. 

- [28] T. Sun, B. Lian, S. Yang, and Y. Song, “Kinematic Calibration of Serial and Parallel Robots Based on Finite and Instantaneous Screw Theory,” _IEEE Trans. Robot._ , vol. 36, no. 3, pp. 816–834, June 2020. 

- [29] K. Guo, Y. Liu, B. Xu, Y. Xu, and Y. Pan, “Locally Weighted Learning Robot Control With Improved Parameter Convergence,” _IEEE Trans. Ind. Electron._ , vol. 69, no. 12, pp. 13 236–13 244, Dec. 2022. 

- [30] S. Chitta, E. Marder-Eppstein, W. Meeussen, V. Pradeep, A. Rodr´ıguez Tsouroukdissian, J. Bohren, D. Coleman, B. Magyar, G. Raiola, M. L¨udtke, and E. Fern´andez Perdomo, “ros ~~c~~ ontrol: A generic and simple control framework for ROS,” _J. Open Source Softw._ , vol. 2, no. 20, 2017. 

**Enrico Ferrentino** (Member, IEEE) received the M.Sc. degree in computer and automation engineering from the Polytechnic University of Turin, Turin, Italy, in 2014, and the Ph.D. degree in robotics from the University of Salerno, Fisciano, Italy, in 2020. From 2013 to 2014, he was a Visiting Scholar with NASA’s Jet Propulsion Laboratory, Pasadena, CA, USA, where he contributed to the Axel tethered robot project within the Robotic Mobility group, led by Dr. Issa Nesnas. Between 2014 and 2017, he was a Ground Segment Engineer with ALTEC S.p.A., Turin, Italy, working on the ESA robotic mission ExoMars. In 2019, he was a Visiting Scholar with LAAS-CNRS, Toulouse, France, where he participated in the H2020 PRO-ACT project as part of the team led by Prof. Antonio Franchi. Since 2020, he has been a Lecturer in Robotics and Medical Robotics with the Department of Information Engineering, Electrical Engineering and Applied Mathematics, University of Salerno, where he is currently an Assistant Professor and technical advisor of the Robotics Laboratory, led by Prof. Pasquale Chiacchio. In 2024, he was appointed Associate Editor for the IEEE Transactions on Automation Science and Engineering. His research interests include optimal planning and control of robotic manipulators, force control, haptic teleoperations, human–robot collaboration, and software architectures for robot control, with applications spanning industrial, medical, and aerospace robotics. 

**Pasquale Chiacchio** (Senior Member, IEEE) received the M.Sc. degree in electronic engineering and the Ph.D. degree in electronic and information engineering from University of Naples Federico II, Naples, Italy, in 1987 and 1992, respectively. He is currently a Professor in Automatic Control and Robotics with the Department of Information Engineering, Electrical Engineering and Applied Mathematics, University of Salerno, Fisciano, Italy. His main research interests include robotics and modeling and control of discrete event systems. In the robotics field, he has been working on robot control and identification, inverse kinematics problem, interaction control, control of redundant manipulators, and control of cooperative manipulators. In the discrete event systems field, he has been working on supervisory control based on monitors, optimal supervisory control, and formal specification for supervisory systems. The results have been published in the main journals of the sector and have been accompanied by an intense experimental activity. He has been a Coordinator of two Research Projects of National Interest (PRIN) and has been involved in research projects funded by the European Union (ECHORD, AIRobots, EuRoC, LOCOMACHS, and LABOR). In December 2011, he was nominated Knight and then in July 2014, he was promoted to an Officer of the Order of Merit of the Italian Republic. Since 2016, he has been the Director of the Ph.D. Program in Information Engineering. Prof. Chiacchio is a member of the Italian Society of Control Researchers. 

**Vincenzo Petrone** (Student Member, IEEE) received the M.Sc. degree in computer engineering with honors from the University of Salerno, Fisciano, Italy, in 2021. He is currently working toward the Ph.D. degree in information engineering with the University of Salerno, Fisciano, Italy. Between 2023 and 2024, he was a Visiting Ph.D. Student with the Dalle Molle Institute for Artificial Intelligence (IDSIA), Lugano, Switzerland, University of Applied Sciences and Arts of Southern Switzerland (SUPSI), Manno, Switzerland, Universit`a della Svizzera italiana (USI), Manno, Switzerland, for six months, focusing on reinforcement learning techniques applied to robotic interaction tasks. His research interests cover optimal trajectory planning and interaction control of robotic tasks, parametric identification of dynamics models, and intelligent control. 

