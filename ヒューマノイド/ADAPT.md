---
title: "ADAPT: Analytical Disturbance-Aware Policy Training for Humanoid Locomotion"
date: "2026-06-15"
authors: "Bofan Lyu; Jindou Jia; Kuangji Zuo; Yanshuo Lu; Shijia Han; Gen Li"
url: https://arxiv.org/abs/2606.16542
pdf: https://arxiv.org/pdf/2606.16542
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.16542)** / [論文ページ](https://arxiv.org/abs/2606.16542)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**ADAPT: Analytical Disturbance-Aware Policy Training for Humanoid Locomotion** 

**Bofan Lyu**<sup>1</sup><sup>_,∗_</sup> , **Jindou Jia**<sup>1</sup><sup>_,∗_</sup> , **Kuangji Zuo**<sup>1</sup> , **Yanshuo Lu**<sup>1</sup> , **Shijia Han**<sup>1</sup> , **Gen Li**<sup>1</sup> , **Boyu Ma**<sup>1</sup> , **Jingliang Li**<sup>1</sup> , **Geng Li**<sup>1</sup> , **Jianfei Yang**<sup>1</sup><sup>_,†_</sup> 

> 1MARS Lab, Nanyang Technological University 

- _∗_ Equal contribution, _†_ Corresponding authors 

Humanoids deployed in human-centered environments must handle force-interactive tasks, where external contacts introduce unexpected disturbances that disrupt locomotion accuracy and stability. Existing learning-based approaches rely on broad domain randomization, task-specific force objectives, or learning-based force estimators from motion history, each of which compromises accuracy, task transferability, or out-of-distribution (OOD) robustness. We present **A** nalytical **D** isturbance- **A** ware **P** olicy **T** raining ( **ADAPT** ), a framework that equips humanoid policies with a physically grounded disturbance observer. The core of ADAPT is an analytical whole-body disturbance observer that estimates residual force/torque online with the accessible robot dynamics, without requiring force/torque sensors. Fed directly into the policy, the estimated disturbances give the humanoid an explicit, physics-derived sense of external force/torque that can generalize across diverse unseen scenes. Experiments on a Unitree G1 humanoid show that ADAPT achieves accurate disturbance prediction and stronger robustness than a proprioception-only baseline under torso perturbations, standing pushes, and asymmetric hand payloads, with improved velocity tracking even on OOD disturbances. Moreover, ADAPT enables penalizing inferred disturbances at lower-body joints to encourage lighter locomotion. 


**Correspondence:** Jianfei Yang: jianfei.yang@ntu.edu.sg, Bofan Lyu: lyub0002@e.ntu.edu.sg. **Project:** https://blyu413.github.io/adapt-locomotion/. 

# **1 Introduction** 

Recent progress in learning-based control has greatly advanced humanoid locomotion in the real world (Radosavovic et al., 2024; Liao et al., 2025; Luo et al., 2025; Yuan et al., 2026). As humanoids move toward deployment in human-centered environments, they inevitably encounter force-interactive tasks, in which robots must exert forces while adapting to the resulting reaction forces from the environment. Examples include transporting payloads (Zhang et al., 2025b; Du et al., 2025), pushing loaded carts (Li et al., 2026), opening doors (Xue et al., 2025), and interacting compliantly with humans (Chen et al., 2025; Lu et al., 2025). These physically interactive tasks inevitably introduce a wide range of unseen uncertainties that disrupt the accuracy and stability of the robot’s locomotion. How to clearly characterize these uncertainties and effectively overcome them becomes increasingly critical for reliable humanoid deployment. 

Existing learning-based methods have explored several ways to handle contact-rich interactive tasks. One line of work aims to improve sim-to-real robustness by exposing the policy to randomized external forces and internal dynamics variations during training (Radosavovic et al., 2024; Long et al., 2024; Zhang et al., 2025c). Another line of work explicitly incorporates force perception into loco-manipulation training for task-specific objectives such as exerting desired forces (Portela et al., 2024), producing compliant responses (Chen et al., 2025; Lu et al., 2025), or enabling force-adaptive control (Zhang et al., 2025b; Xu et al., 2025). A third direction uses learning-based force estimators that infer interaction forces from proprioceptive histories, and then feed the predicted force-related signal to the controller to form force-conditioned policies without additional force/torque sensors (Zhi et al., 2025). However, these methods either rely on broad randomization that sacrifices tracking accuracy, require task-specific design, or generalize poorly to out-of-distribution (OOD) disturbances. 

This motivates us to seek a more general and minimally policy-invasive disturbance-aware strategy for 

1 


**Figure 1 Overview of ADAPT.** ADAPT augments RL-based humanoid control with an analytical disturbance observer that infers whole-body disturbance torques from accessible robot dynamics, proprioception, and expected motor torques. The estimated disturbances are fed into the policy as an explicit observation and used for reward shaping. This enables emergent force-aware behaviors, including push resistance, payload compensation, and light-footed locomotion. 

improving the robustness and generalization of humanoid policies. Physics-informed learning has been increasingly shown to be an effective path toward more robust and generalizable policies (Lutter et al., 2019; Jia et al., 2026b). Following this line of thought, we ask whether prior physical knowledge of the humanoid itself can serve as a source of disturbance awareness, one that informs policy learning and, being grounded in physics rather than data, generalizes beyond the training distribution. Analytical disturbance estimation has been extensively explored in classical robot control, exemplified by nonlinear disturbance observers (Chen et al., 2000; Jia et al., 2025) and _L_ 1 adaptive estimation (Han, 2009). Yet, integrating such analytical estimates into Reinforcement Learning (RL)-based humanoid policies to improve robustness and generalization remains an open question (Lim et al., 2025). 

In this work, we introduce the **A** nalytical **D** isturbance- **A** ware **P** olicy **T** raining ( **ADAPT** ) framework for humanoid locomotion, which augments prevailing RL-based policy with explicit whole-body disturbance prediction during training. Specifically, instead of requiring the policy to infer external forces/torques only from motion histories (Portela et al., 2024; Zhi et al., 2025), we estimate unexpected forces/torques online with accessible physical knowledge and feed them directly into the policy. This gives the policy a structured and physically grounded force-related perception channel for disturbance-aware humanoid control. Notably, the analytical disturbance estimation also enables task-specific reward shaping, such as penalizing foot-joint disturbances to encourage lighter locomotion. On the technical side, we further integrate a Fast-LIO (Xu et al., 2022) based odometry module for accurate root linear velocity, which, to our knowledge, is among the earliest uses of LIO-based root velocity estimation as policy inputs in learning-based humanoid whole-body control. 

We validate ADAPT in both simulation and real-world experiments on a Unitree G1 humanoid. The results show that the proposed whole-body disturbance observer provides a consistent and reliable disturbance signal. With this prediction as policy input, ADAPT improves robustness against external forces, achieving better velocity tracking and smaller directional drift than a proprioception-only baseline. More importantly, the policy also shows an emergent force-aware response. Under asymmetric hand payloads never encountered during training, it actively adjusts the whole-body posture to compensate for the load. Beyond direct policy feedback, the same disturbance prediction can also support contact-aware reward shaping and behavior analysis. 

# **2 Related works** 

**Force-aware policy learning.** Handling interaction forces is central to contact-rich humanoid and legged control, where robots must apply, resist, or yield to external contacts while remaining stable. Existing learning-based methods address this challenge in several ways. Some methods improve robustness by training 

2 

policies with randomization of internal dynamics (Radosavovic et al., 2024; Zhang et al., 2025c) and external disturbances (Zhang et al., 2025c; Long et al., 2024). Other methods introduce force interaction through task-specific objectives and rewards, enabling tasks such as payload transport (Zhang et al., 2025b), door opening (Xue et al., 2025), high-intensity pulling (Li et al., 2025), compliant interaction (Chen et al., 2025; Lu et al., 2025; Hou et al., 2025), and collaborative carrying (Du et al., 2025). Another line of work estimates or predicts force-related quantities from proprioceptive histories for direct force control (Portela et al., 2024), unified position and force control (Zhi et al., 2025), or disturbance compensation (Zhang et al., 2025a). These approaches handle external forces by broadening the training distribution, embedding interaction requirements into task objectives, or learning force-related representations from proprioceptive histories. In contrast, ADAPT leverages a physics-derived disturbance prediction with built-in generalization. 

**Sensorless disturbance estimation.** Some methods infer object physical properties or task feasibility from internal robot measurements and a priori physical knowledge, without relying on joint force/torque sensors (Lao et al., 2023; Han et al., 2020). They have been used for disturbance rejection, sensorless torque reasoning, fault detection, and collision monitoring for various robots (Chen et al., 2000; Chen, 2004; De Luca and Mattone, 2003; Haddadin et al., 2017). For humanoids, external torque estimation is more challenging due to high-dimensional, strongly nonlinear dynamics. MOB-Net (Lim et al., 2025) uses a momentum observer to estimate external contact wrenches, primarily for wrench feedback, collision detection, and collision reaction. BeyondMimic (Liao et al., 2025) combines the momentum observer with a Kalman filter for onboard fullstate estimation during humanoid deployment. These estimated forces are commonly used for monitoring, identification, or model-based feedback. However, directly incorporating such analytical disturbance estimates into the learned policy as an explicit observation modality remains largely unexplored. 

# **3 Methodology** 

## **3.1 Overview of ADAPT** 

**Problem formulation.** The whole-body dynamics of a humanoid (Nenchev et al., 2018) can be formalized as 


where _q ∈_ R<sup>_nj_+7</sup> and _v ∈_ R<sup>_nj_+6</sup> are the generalized coordinate and velocity, and _nj_ denote the number of actuated joints in the humanoid. The dimension mismatch comes from the floating-base representation: _q_ includes a 3D base position and a 4D unit quaternion, whereas _v_ includes 3D base linear and 3D angular velocities. _M_ ( _q_ ) is the nominal inertia matrix, _C_ ( _q, v_ ) _v_ is the nominal _Coriolis_ and centrifugal term, _g_ ( _q_ ) is the nominal gravity term, _τm_ is the generalized actuation force induced by joint motors, and _τe_ denotes the generalized disturbance. In practice, _τe_ captures the combined effect of external contacts (e.g., payloads, environmental reactions, human interaction) and internal model mismatch (e.g., friction, inertial uncertainty) on the robot’s generalized motion. 

Direct access to _τe_ , however, is difficult in practice. Humanoid robots are rarely equipped with a whole-body force/torque sensor. Meanwhile, directly computing _τe_ through Eq. (1) requires the generalized acceleration _v_ ˙, whose estimation is highly susceptible to sensor noise and numerical differentiation errors. Existing force-aware policies often obtain disturbance cues through task-specific curricula (Chen et al., 2025) or learned force estimators from motion history (Zhi et al., 2025), which makes the resulting force representation dependent on the disturbance distribution specified during training and inevitably degrades under out-of-distribution forces. 

**Oursolution.** Our ADAPT framework addresses this problem by closing the loop between analytical disturbance estimation and policy control. As illustrated in Fig. 1, ADAPT consists of two main modules: an analytical disturbance estimator and an RL-based whole-body controller. The disturbance estimator, detailed in Sec. 3.2, evaluates the nominal robot dynamics from the current robot state and actuator command, and estimates the whole-body disturbance. The learning-based controller, detailed in Sec. 3.3, takes this estimation as a force-aware proprioceptive signal and feeds it back to the policy as part of its observation or even the upper-level reward. With this feedback channel, the learned controller can condition its whole-body response on the inferred disturbance, enabling disturbance-aware humanoid adaptation. 

3 

## **3.2 Whole-body disturbance observer** 

Derived from Eq. (1), we can easily get a representation of whole-body disturbance through _τe_ = _M_ ( _q_ ) _v_ ˙ + _C_ ( _q, v_ ) _v_ + _g_ ( _q_ ) _− τm_ . However, directly calculating _v_ ˙ is impractical, as it is usually unavailable from the sensory system and noisy under numerical differentiation. The disturbance observer avoids this noisy acceleration term by using the generalized momentum, i.e., _p_ = _M_ ( _q_ ) _v_ . Differentiating the generalized momentum and using the standard _Christoffel_ convention, _M_ ˙ ( _q_ ) = _C_ ( _q, v_ ) + _C_<sup>_⊤_</sup> ( _q, v_ ) (De Luca and Mattone, 2003), gives 


Substitute Eq. (1) into Eq. (2) gives _τe_ = _p_ ˙ _− β_ ( _q, v_ ) _− τm_ , where _β_ ( _q, v_ ) = _C_<sup>_⊤_</sup> ( _q, v_ ) _v − g_ ( _q_ ) for simplicity. Now, we can estimate _τe_ using a first-order observer with positive-definite diagonal observer gain _Ko_ , i.e., _τ_ ˙ˆ _e_ = _Ko_ ( _τe − τ_ ˆ _e_ ). To avoid the use of the inaccessible _p_ ˙, we introduce the auxiliary state _z_ = _τ_ ˆ _e − Kop_ and obtain 


Note that the observer established in Eqs.(3)-(4) only requires accessible signals including current proprioceptive state, control command, and nominal dynamics terms. 

As for the nominal dynamics, instead of hand-deriving, we obtain _M_ ( _q_ ) and _β_ directly from a synchronized MuJoCo model, which is fast enough for large-scale parallel training and deployment. And _τm_ is derived from an ideal motor controller. For efficiency, we approximate _β_ ( _q, v_ ) = _C_<sup>_⊤_</sup> ( _q, v_ ) _v − g_ ( _q_ ) using the negative MuJoCo bias force _−q_ bias, where _q_ bias = _C_ ( _q, v_ ) _v_ + _g_ ( _q_ ). This approximation introduces a velocity-dependent error _M_ ˙ ( _q_ ) _v_ in _β_ , whose effect is shown to be negligible in practice (see Appx. A). 

The observer gain _Ko_ governs a fundamental trade-off. A larger _Ko_ accelerates convergence and improves estimation accuracy, but also amplifies high-frequency noise from measurement, especially critical on real hardware. To balance responsiveness and noise robustness, we apply a low-pass filter to the raw estimate _τ_ ˆ _e_ before passing it to downstream modules. Moreover, the linear floating-base residual contains a constant gravity bias in the inertial vertical direction. We remove this constant gravity bias and then rotate the floating-base residual into the root frame before feeding it to the policy. We denote the final resulting filtered residual as 


where _τ_ ¯ _e_<sup>lin</sup> _∈_ R<sup>3</sup> and _τ_ ¯ _e_<sup>ang</sup> _∈_ R<sup>3</sup> are the linear and angular residuals of the floating base, expressed in the root frame of the humanoid. The term _τ_ ¯ _e_<sup>jnt</sup> _∈_ R<sup>29</sup> denotes the residual in the joint coordinates. 

## **3.3 Disturbance-aware policy** 

With the analytical disturbance estimation, we next endeavor to design the RL policy. We use a multi-layer perceptron (MLP) as the whole-body controller. The policy is trained with Proximal Policy Optimization (PPO) (Schulman et al., 2017) and outputs target joint positions, which are tracked by a low-level motor PD controller. The key modification in ADAPT is to augment the actor input with the analytical disturbance estimated by the dynamics-driven observer in Sec. 3.2. This analytical disturbance provides a structured forcerelated observation channel, enabling the policy to condition its response on explicit whole-body disturbance. See Fig. 1 for the policy structure. 

**Actor-critic architecture.** We use an asymmetric _actor-critic_ architecture trained with PPO (Schulman et al., 2017). Both the actor and critic are three-layer MLPs with hidden dimensions (512 _,_ 256 _,_ 128) and ELU activations. At timestep _k_ , the actor observation _o_<sup>_π_</sup> _k_<sup>consistsofafive-stephistoryfrom</sup><sup>_k −_4to</sup><sup>_k_ofbase</sup> linear velocity _vk_<sup>_b∈_R3,baseangularvelocity</sup><sup>_ω_</sup> _k_<sup>_b∈_R3,projectedgravity</sup><sup>_g_</sup> _k_<sup>_b∈_R3,jointpositionandvelocity</sup> _qk_<sup>_j,q_˙</sup> _k_<sup>_j∈_R</sup><sup>_nj_,velocitycommand</sup><sup>_ck∈_R3,andeffort-scaleddisturbanceestimation</sup><sup>_ρk∈_R6+</sup><sup>_nj_,togetherwith</sup> the previous action _ak−_ 1 _∈_ R<sup>_nj_</sup> , resulting in a 554-dimensional actor observation. Moreover, the critic receives the actor observation and additional privileged foot-contact information, including foot height _hf_ , foot air time _t_<sup>air</sup> _f_<sup>,contactstate</sup><sup>_sf_,andcontactforce</sup><sup>_Ff_.Theseprivilegedobservationsareusedonlyduringtraining</sup> for value estimation. 

4 

**Trainingpipeline.** To allow the policy to gradually adapt to external disturbance and incorporate the disturbance observation, we train it with a two-stage curriculum. Stage 1 trains the policy to acquire basic locomotion in a disturbance-free setting, while still consuming the disturbance observation as input. Stage 2 introduces a disturbance curriculum with external forces applied to selected bodies, requiring the same policy to track velocity commands under increasing disturbance levels. 

**Disturbance normalization.** For the disturbance observation, standard normalization is not well-suited to our two-stage force curriculum, as the disturbance magnitudes encountered in the two stages differ significantly in scale. We therefore use unified scales for the disturbance observation channels in two stages, i.e., _ρ_ = � _τ_ ¯ _e_<sup>lin</sup><sup>_/_(</sup><sup>_mg_)</sup><sup>_,_¯</sup><sup>_τ_</sup> _e_<sup>ang</sup> _/_ ( _mgl_ ref ) _,_ ¯ _τe_<sup>jnt</sup><sup>_/τ_max</sup> _j_ �, where _m_ is the nominal robot mass, _g_ is the gravity magnitude, _l_ ref is a user-defined normalization constant, and _τ_<sup>max</sup> is the actuator effort limit of each joint. This representation incorporates joint-dependent actuation capacity by expressing each joint’s residual relative to its corresponding effort limit. We apply this unified normalization to the disturbance channels and standard observation normalization to the remaining policy inputs. Appx. E shows the effectiveness of this scaling strategy. **Training reward.** Within the ADAPT framework, in addition to the standard rewards for command tracking (Zakka et al., 2026), ADAPT supports task-specific reward terms defined on the estimated disturbance. Here, we penalize the leg-joint disturbance estimates to encourage lighter, lower-impact locomotion. Let _ρ_<sup>_s_</sup> _i_ denote the scaled leg disturbance residuals of the _i_ -th <u>joint</u> of leg _s ∈{L, R}_ at a single timestep. For each leg, we define the residual envelope as _e_<sup>_s_</sup> = ~~�~~ <u>16 �6</u> _i_ =1<sup>(</sup><sup>_ρ_</sup> _i_<sup>_s_)2.</sup> 

During training, this value is computed at each timestep, and we use _ek_ = max( _e_<sup>_L_</sup> _k_<sup>_, eR_</sup> _k_<sup>)asthelower-body</sup> residual envelope at timestep _k_ . Let _Hk_ = _{ek−H_ +1 _, . . . , ek}_ denote a rolling window of length _H_ . We compute the high-tail average _ηk_ = mean (Top10%( _Hk_ )) as the mean of the largest 10% values in _Hk_ , and the peak _<u>k</u> −θ_ <u>peak</u> value _e_<sup>peak</sup> _k_ = max _e∈Hk_ . We define two penalty as _ϕη,k_ = max�0 _,_<sup>_<u>ηk</u>_</sup> _δ_<sup>_−_</sup> _η_<sup>_θη_</sup> � and _ϕ_ peak _,k_ = max�0 _,_<sup>_e_peak</sup> _δ_ peak �. The light-step reward is 


where _χk ∈{_ 0 _,_ 1 _}_ is a command mask that enables the penalty for locomotion commands and disables it for zero commands, _λη_ and _λ_ peak are penalty weights, _θη_ and _θ_ peak are activation thresholds, and _δη_ and _δ_ peak are margin parameters that scale the excess above the thresholds. These terms penalize high-impact lower-body residual peaks, while preserving the support forces needed for walking. Other instantiations, such as penalizing hand-joint disturbances to encourage compliant pushing or pulling, are left for future exploration. 

## **3.4 Practical consideration** 

**FAST-LIO usage.** The root linear velocity is an important observation for the disturbance observer, but it is not directly available in the current humanoid community. Directly integrating IMU acceleration is unreliable due to drift. We here employ FAST-LIO (Xu et al., 2022) to obtain the robot motion during real-world deployment. Since the LiDAR is mounted on the torso, we convert the raw observation to the root frame before using it in the disturbance observer and policy. Let _vL_<sup>_L∈_R3betherawLiDARlinearvelocityfrom</sup> FAST-LIO expressed in the LiDAR local frame. Given the current joint position _q_ jnt and the rotation matrix _RRL_ ( _q_ jnt) _∈ SO_ (3) that maps vectors from the LiDAR frame to the root frame, the LiDAR velocity expressed in the root frame is _vL_<sup>_R_=</sup><sup>_RRL_(</sup><sup>_q_jnt)</sup><sup>_v_</sup> _L_<sup>_L_.Wethencomputetherootlinearvelocityas</sup><sup>_v_</sup> root<sup>_R_=</sup><sup>_v_</sup> _L_<sup>_R−JL_(</sup><sup>_q_jnt) ˙</sup><sup>_q_jnt,</sup> where _v_ root<sup>_R_istherootlinearvelocityexpressedintherootframe,</sup><sup>_JL_(</sup><sup>_q_jnt)</sup><sup>_∈_R3</sup><sup>_×nj_istheLiDARlinear</sup> Jacobian with respect to the actuated joints, expressed in the root frame, and _q_ ˙jnt is the measured joint velocity. The term _JL_ ( _q_ jnt) ˙ _q_ jnt represents the relative linear velocity between the LiDAR and the root. 

# **4 Experimental Results** 

We evaluate ADAPT in both simulation and real-world experiments on a Unitree G1 humanoid. The experiments are designed to answer three questions: (1) Does the disturbance observer provide accurate disturbance estimation during humanoid locomotion? (2) Does conditioning the policy on the analytical 

5 


**Figure 2 Performance of the disturbance observer on the Unitree G1** . The robot walks forward while known disturbance torques (dashed lines) are injected into the left shoulder pitch, left elbow, right shoulder pitch, and waist pitch joints. Solid lines show the observer estimation in simulation ( _left_ ) and real-world ( _middle_ ). 

disturbance improve robustness and generalization to external perturbations? (3) Does using the analytical disturbance for reward reshaping bring additional benefits? The experimental setup and parameter setting are detailed in Appx.B. 

## **4.1 Estimation performance of disturbance observer** 

The observer for estimating whole-body disturbance is the core component of our ADAPT framework, as it provides the policy with an explicit force-aware signal for physical interaction. Its performance directly affects the reliability of the learning-based controller built upon it. In both simulation and real test, the robot is commanded to walk forward with a fixed velocity command, _vx_ = 0 _._ 8 m _/_ s. The observer output is not provided to the policy observation and does not affect the control action. Therefore, the measured residuals reflect the standalone estimation behavior of the observer. During the rollout, known disturbance torques are directly injected into selected joints: left shoulder pitch, left elbow, right shoulder pitch, and waist pitch, as shown in the right of Fig. 2. The goal of this experiment is to validate whether the observer remains stable and reliable during locomotion. 

The test results are shown in Fig. 2. In simulation, the observer closely tracks the injected disturbance profiles across multiple joints, and the estimated residuals remain well isolated among different joint channels. In the real-world test, the observer still captures the onset and relative magnitude of the applied disturbance in each channel, indicating consistent observer behavior between simulation and hardware. Compared with simulation, the observer shows a larger estimation error in the real world. This degradation reflects additional unknown real-world disturbances beyond the injected joint torque, such as joint friction and motor modeling error. 

## **4.2 Control performance of disturbance-aware policy** 

The observer evaluation above shows that the disturbance observer provides a reliable estimation of joint-space disturbances. We next ask whether this estimated signal can be effectively used by a learned policy. To answer this question, we evaluate ADAPT under diverse velocity commands and external force perturbations. Perturbations vary in location and magnitude. We compare ADAPT with a baseline that uses the same policy architecture and training setup but does not receive the explicit disturbance feedback. The comparison is made in both simulation and real-world experiments. We adopt several evaluation metrics, including velocity tracking error _evx_ , lateral drift _dy_ , and yaw drift _dψ_ . Detailed definitions are provided in Appx. D. 

**Torso pulling test.** We first evaluate ADAPT in simulation by applying torso forces in the sagittal plane. The magnitude of forces ranges from 0 N to 60 N, where the maximum force magnitude used during training is 40 N. Fig. 3 shows the results under sagittal torso forces across different walking speeds. Compared with the baseline, ADAPT achieves lower forward velocity tracking error, lateral drift, and heading drift, especially under stronger perturbations. This shows that the explicit disturbance feedback helps the policy compensate for external forces while maintaining the commanded locomotion behavior. 

We further evaluate the velocity tracking task under torso perturbations applied from different horizontal directions. The radar maps in Fig. 3 present two force magnitudes, 40 N, which lies within the training range, and 60 N, which exceeds it. ADAPT outperforms the baseline, achieving better locomotion under 

6 


**Figure 3 Torso pulling test in simulation.** _Left:_ Velocity tracking error, lateral drift, and yaw drift under sagittal torso forces across three command velocities. _Right:_ Radar plots summarize results across disturbance directions. 


**Figure 4 Stance pulling test.** The policy trained under the ADAPT framework exhibits whole-body posture adjustment to resist external force applied on torso. 

both in-distribution and OOD disturbance magnitudes. These results indicate that the explicit disturbance estimation serves as an effective feedback for the policy, improving its robustness and generalization. 

**Stance pulling test.** On the real robot, we conduct a standing perturbation test to evaluate the policy response to external forces. The robot receives a zero-velocity command, while an operator applies external forces to its torso and shoulder. As presented by snapshots in Fig. 4, compared with the baseline, the ADAPT-trained policy shows stronger resistance to the applied forces and adjusts its whole-body posture to counteract the perturbation. This indicates that the explicit disturbance estimation provides useful feedback for improving whole-body robustness during physical interaction. 

**Asymmetric hand loading test.** We then evaluate ADAPT under asymmetric hand loading. In simulation, we apply a constant downward force of 10–40 _,_ N to one hand. On the real robot, we reproduce this condition by attaching weights of 1 to 4 kg to the same hand, 


**Figure 5 Asymmetric hand loading test.** _Upper_ : postural response with an OOD 4 kg payload on the right hand. _Lower_ : lateral drift versus forward distance under one-sided hand loads, in both simulation and real tests. 

7 


**Figure 6 Light-step Reward Shaping.** Disturbance residual envelope over time in simulation ( _left_ ) and on the real robot ( _middle_ ). _Right:_ Snapshots of the touchdown phase, showing that ADAPT produces a _tiptoeing_ gait while the baseline exhibits a _stomping_ gait. 

where the 4 kg payload lies outside the training distribution. The added payloads create downward loads comparable to the simulated setting. Under these asymmetric loads, ADAPT and the baseline exhibit markedly different postural responses. As shown in Fig. 5, the proprioception-only baseline is pulled toward the loaded side, resulting in a visibly unbalanced upper-body posture. In contrast, ADAPT tilts the torso away from the loaded side to compensate for the moment caused by the load. We further examine walking robustness under asymmetric loading. The curves in Fig. 5 show that the baseline exhibits increasing lateral drift as the hand load becomes larger. In contrast, ADAPT maintains a straighter walking trajectory across all load magnitudes, indicating better compensation. 

## **4.3 Reward shaping for lighter locomotion** 

Beyond using the disturbance estimation as a direct policy input, we also examine whether it can be used for reward shaping. We focus on foot touchdown as an illustrative test case, considering that abrupt touchdown often produces short disturbance peaks in the lower-body residuals. This allows us to test whether rewards derived from joint-space disturbance estimation can encourage lighter locomotion behavior. The reward shaping strategy is formalized in Eq. (6). 

We evaluate the light-step reward in both simulation and real-world deployment using the scaled leg disturbance residual envelope, where lower values indicate lighter leg loading and smaller foot-ground impact. As shown in Fig. 6, the light-step policy maintains a consistently lower envelope than the baseline and reduces the periodic loading peaks. This indicates lighter foot contacts during walking. This phenomenon can also be revealed in snapshots of the touchdown phase. Overall, the simulation and real-robot results show that ADAPT-derived envelopes can serve as effective reward-shaping signals for improving contact transitions during locomotion. 

# **5 Conclusion** 

We present ADAPT, a framework that augments RL-based humanoid control with an analytical whole-body disturbance observer. The observer provides a physics-grounded, sensorless force-related observation that can be directly fed into the policy as observation or used for reward shaping. Experiments on a Unitree G1 show that ADAPT improves robustness and velocity tracking under external forces, generalizes to OOD perturbations such as asymmetric hand loads, and enables emergent behaviors including light-footed locomotion through disturbance-derived reward shaping. 

# **6 Limitations** 

The disturbance observer in ADAPT has a finite convergence time and thus responds with some delay to fast-varying disturbances such as impulsive pushes and foot-ground impacts. Currently, we absorb these fast transients into a single lumped disturbance, and ADAPT still exhibits robust performance in our experiments. However, this lumped treatment can make the learned policy somewhat conservative. Separating fast-varying components from the lumped signal, or designing observers for fast disturbances, could further improve 

8 

responsiveness, which we leave for future work. ADAPT could also be combined with multimodal robot policy backbones (Jia et al., 2026a) to enable more expressive humanoid behaviors under disturbance-aware control. 

9 

# **References** 

- Sirui Chen, Zi-ang Cao, Zhengyi Luo, Fernando Castañeda, Chenran Li, Tingwu Wang, Ye Yuan, Linxi Fan, C Karen Liu, and Yuke Zhu. CHIP: Learning adaptive compliance for humanoid control through hindsight perturbation. _arXiv preprint arXiv:2512.14689_ , 2025. 

- Wen-Hua Chen. Disturbance observer based control for nonlinear systems. _IEEE/ASME Transactions on Mechatronics_ , 9(4):706–710, 2004. 

- Wen-Hua Chen, Donald J. Ballance, Peter J. Gawthrop, and John O’Reilly. A nonlinear disturbance observer for robotic manipulators. _IEEE Transactions on Industrial Electronics_ , 47(4):932–938, 2000. 

- A. De Luca and R. Mattone. Actuator failure detection and isolation using generalized momenta. In _2003 IEEE International Conference on Robotics and Automation_ , volume 1, pages 634–639, 2003. 

- Yushi Du, Yixuan Li, Baoxiong Jia, Yutang Lin, Pei Zhou, Wei Liang, Yanchao Yang, and Siyuan Huang. Learning human-humanoid coordination for collaborative object carrying. _arXiv preprint arXiv:2510.14293_ , 2025. 

- Sami Haddadin, Alessandro De Luca, and Alin Albu-Schäffer. Robot collisions: A survey on detection, isolation, and identification. _IEEE Transactions on Robotics_ , 33(6):1292–1312, 2017. 

- Jingqing Han. From PID to active disturbance rejection control. _IEEE Transactions on Industrial Electronics_ , 56(3): 900–906, March 2009. 

- Yuanfeng Han, Ruixin Li, and Gregory S. Chirikjian. Can i lift it? humanoid robot reasoning about the feasibility of lifting a heavy box with unknown physical properties. In _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 3877–3883, 2020. 

- Yifan Hou, Zeyi Liu, Cheng Chi, Eric Cousineau, Naveen Kuppuswamy, Siyuan Feng, Benjamin Burchfiel, and Shuran Song. Adaptive compliance policy: Learning approximate compliance for diffusion guided control. In _2025 IEEE International Conference on Robotics and Automation_ , pages 4829–4836, 2025. 

- Jindou Jia, Kexin Guo, Yuyang Wang, Sicheng Zhou, Jiayi Zhang, Yuhang Liu, Xiang Yu, Yang Shi, and Lei Guo. FORESEER: Recognize and utilize uncertainties by integrating data-based learning and symbolic feedback. _The International Journal of Robotics Research_ , 2025. 

- Jindou Jia, Tuo An, Yuxuan Hu, Gen Li, Jingliang Li, Bohan Hou, Xiangyu Chen, Jiaqi Bai, Bofan Lyu, and Jianfei Yang. Mars policy: Multimodality only when it matters. _arXiv preprint arXiv:2605.29766_ , 2026a. 

- Jindou Jia, Shixuan Han, Meng Wang, Gen Li, Zihan Yang, Sicheng Zhou, Kexin Guo, Jianfei Yang, Xiang Yu, Wei Wang, and Lei Guo. Physics filtering favors the generalization of robot learning. _Research Square preprint_ , 2026b. 

- Zizhou Lao, Yuanfeng Han, Yunshan Ma, and Gregory S. Chirikjian. A learning-based approach for estimating inertial properties of unknown objects from encoder discrepancies. _IEEE Robotics and Automation Letters_ , 8(9):5283–5290, 2023. 

- Dongting Li, Xingyu Chen, Qianyang Wu, Bo Chen, Sikai Wu, Hanyu Wu, Guoyao Zhang, Liang Li, Mingliang Zhou, Diyun Xiang, et al. HAIC: Humanoid agile object interaction control via dynamics-aware world model. _arXiv preprint arXiv:2602.11758_ , 2026. 

- Gangyang Li, Qing Shi, Youhao Hu, Jincheng Hu, Zhongyuan Wang, Xinlong Wang, and Shaqi Luo. Thor: Towards human-level whole-body reactions for intense contact-rich environments. _arXiv preprint arXiv:2510.26280_ , 2025. 

- Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- Daegyu Lim, Myeong-Ju Kim, Junhyeok Cha, and Jaeheung Park. MOB-Net: Limb-modularized uncertainty torque learning of humanoids for sensorless external torque estimation. _The International Journal of Robotics Research_ , 44 (1):96–128, 2025. 

- Junfeng Long, Wenye Yu, Quanyi Li, ZiRui Wang, Dahua Lin, and Jiangmiao Pang. Learning H-Infinity locomotion control. In _8th Annual Conference on Robot Learning_ , 2024. 

- Qingzhou Lu, Yao Feng, Baiyu Shi, Michael Piseno, Zhenan Bao, and C Karen Liu. GentleHumanoid: Learning upper-body compliance for contact-rich human and object interaction. _arXiv preprint arXiv:2511.04679_ , 2025. 

10 

- Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castaneda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- M Lutter, C Ritter, and Jan Peters. Deep lagrangian networks: Using physics as model prior for deep learning. In _International Conference on Learning Representations_ , 2019. 

- Dragomir N Nenchev, Atsushi Konno, and Teppei Tsujita. _Humanoid robots: Modeling and control_ . ButterworthHeinemann, 2018. 

- Tifanny Portela, Gabriel B Margolis, Yandong Ji, and Pulkit Agrawal. Learning force control for legged manipulation. In _2024 IEEE International Conference on Robotics and Automation_ , pages 15366–15372, 2024. 

- Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Botian Xu, Haoyang Weng, Qingzhou Lu, Yang Gao, and Huazhe Xu. FACET: Force-adaptive control via impedance reference tracking for legged robots. In _9th Annual Conference on Robot Learning_ , 2025. 

- Wei Xu, Yixi Cai, Dongjiao He, Jiarong Lin, and Fu Zhang. FAST-LIO2: Fast direct LiDAR-inertial odometry. _IEEE Transactions on Robotics_ , 38(4):2053–2073, 2022. 

- Haoru Xue, Tairan He, Zi Wang, Qingwei Ben, Wenli Xiao, Zhengyi Luo, Xingye Da, Fernando Castañeda, Guanya Shi, Shankar Sastry, et al. Opening the sim-to-real door for humanoid pixel-to-action policy transfer. _arXiv preprint arXiv:2512.01061_ , 2025. 

- Xichen Yuan, Zhe Li, Bofan Lyu, Kuangji Zuo, Yanshuo Lu, Gen Li, and Jianfei Yang. Roboforge: Physically optimized text-guided whole-body locomotion for humanoids. _arXiv preprint arXiv:2603.17927_ , 2026. 

- Kevin Zakka, Qiayuan Liao, Brent Yi, Louis Le Lay, Koushil Sreenath, and Pieter Abbeel. mjlab: A lightweight framework for GPU-accelerated robot learning. _arXiv preprint arXiv:2601.22074_ , 2026. 

- Yang Zhang, Buqing Nie, Zhanxiang Cao, Yangqing Fu, and Yue Gao. Disturbance-aware adaptive compensation in hybrid force-position locomotion policy for legged robots, 2025a. 

- Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025b. 

- Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, Huaping Liu, He Wang, and Li Yi. Track any motions under any disturbances, 2025c. 

- Peiyuan Zhi, Peiyang Li, Jianqin Yin, Baoxiong Jia, and Siyuan Huang. Learning a unified policy for position and force control in legged loco-manipulation. In _Proceedings of the 9th Conference on Robot Learning_ , volume 305 of _Proceedings of Machine Learning Research_ , pages 652–669. PMLR, 2025. 

11 

# **A Implementation details of disturbance observer** 

**Parameters.** The theoretical formulation of the disturbance observer is given in Sec. 3.2. Here, we report the parameters used for hardware deployment. The observer runs at 50 Hz, using the same update rate as the policy. The observer timestep is therefore ∆ _t_ obs = 0 _._ 02 s. We use a uniform diagonal observer gain for all generalized velocity coordinates, 


where the first six dimensions correspond to the floating base and the remaining _nj_ dimensions correspond to the actuated joints. All residual channels use the same observer gain in hardware experiments. 

The raw residual estimation is smoothed before being used by the policy. We apply an online second-order Butterworth low-pass filter independently to each residual channel. The cutoff frequency is _fc_ = 1 _._ 0 Hz. The filtered residual is denoted by _τ_ ¯ _e_ , consistent with Eq. (5). It is then normalized and used as the disturbance observation for the policy. 

**Approximation.** The momentum observer requires the bias term _β_ ( _q, v_ ) = _C_<sup>_⊤_</sup> ( _q, v_ ) _v − g_ ( _q_ ). In the main implementation, we compute the observer with MuJoCo dynamics quantities for efficiency. MuJoCo provides the bias force 


We therefore approximate _β_ ( _q, v_ ) with the negative MuJoCo bias force, 


Under the same convention used in Sec. 3.2, _M_ ˙ ( _q_ ) = _C_ ( _q, v_ ) + _C_<sup>_⊤_</sup> ( _q, v_ ). The approximation error in _β_ is then 


Thus, the MuJoCo approximation introduces only a velocity-dependent error in the observer bias term. This error is zero when _v_ = 0. 

We test the effect of this approximation with an independent Pinocchio-based observer. Pinocchio computes the exact term _β_ ( _q, v_ ) = _C_<sup>_⊤_</sup> ( _q, v_ ) _v − g_ ( _q_ ) from the full Coriolis matrix and the generalized gravity vector. The MuJoCo-based and Pinocchio-based observers use the same robot states, commanded torques, observer parameters, and filters. They differ only in the computation of _β_ ( _q, v_ ). 

During walking, we inject known joint-space torques into the left shoulder pitch, left elbow, right shoulder pitch, and waist pitch joints. These injected torques are used as ground truth. We then compare the residuals estimated by the two observers. 

As shown in Fig. S1, the two observers produce almost identical residuals on all tested joints. Both estimates match the sign, magnitude, and timing of the injected torques. The small differences near the rising and falling edges mainly come from the observer bandwidth and the output filter. This result shows that the velocity-dependent error in _β_ has little effect on the final disturbance estimate. 

We use the MuJoCo-based observer in the main experiments to keep the computation consistent between policy training and deployment. We also implement the Pinocchio-based observer as an alternative backend for real-robot deployment. 

# **B Experiment setup** 

**Training setup.** All policies are trained in mjlab (Zakka et al., 2026) with the Unitree G1 model. Training is performed on an NVIDIA RTX 5090 GPU with 4096 parallel environments. The simulator uses a physics timestep of 0 _._ 005 s and a control decimation of 4, resulting in a 200 Hz simulation rate and a 50 Hz policy update rate. The policy action is a joint-position offset added to the default pose and tracked by the low-level 

12 


**Figure S1 Effect of approximation in observer.** Comparison between MuJoCo-based and Pinocchio-based observer residuals under known joint-space torque perturbations. The two observers produce nearly identical estimates and both match the injected torques, showing that the MuJoCo bias approximation has little practical effect. 

PD controller. We train ADAPT in two stages. Stage 1 trains the nominal walking policy for 15 _,_ 000 iterations. Stage 2 resumes from the Stage-1 checkpoint and trains the disturbance-aware policy for another 20 _,_ 000 iterations with external wrench perturbations applied on torso and end-effectors. 

**Reward.** The base reward is shared by ADAPT and the corresponding baselines. It consists of velocity tracking terms and regularization terms for posture, smoothness, contact quality, and safety. We denote the commanded velocity by _c_ = [ _vx_<sup>cmd</sup> _, vy_<sup>cmd</sup> _, ωz_<sup>cmd</sup> ], where _vx_<sup>cmd</sup> and _vy_<sup>cmd</sup> are the commanded base linear velocities and _ωz_<sup>cmd</sup> is the commanded yaw rate. We use _v_<sup>_b_</sup> and _ω_<sup>_b_</sup> for the base linear and angular velocities in the root frame, _q_ jnt for actuated joint positions, _q_ ˙jnt for actuated joint velocities, _a_ for policy actions, and _hf_ for foot height. The reward terms are summarized in Table S1. The light-step reward is only used in the reward-shaping experiment. 

The total reward is computed as a weighted sum, 


where _ri_ is the raw reward or penalty term and _wi_ is its weight. For compact notation, let _F_ denote the set of feet, _sf ∈_ 0 _,_ 1 denote the contact state of foot _f_ , _vf_ denote the foot velocity, and _h_<sup>_⋆_</sup> _f_<sup>= 0</sup><sup>_._1mdenote</sup> the target foot height. We use _χ_ cmd = I( _|_ [ _vx_<sup>cmd</sup> _, vy_<sup>cmd</sup> ] _| >_ 0 _._ 05 or _|ωz_<sup>cmd</sup> _| >_ 0 _._ 05) to mask foot-related rewards when the robot is commanded to stand. _h_<sup>peak</sup> _f_ denotes the maximum foot height reached during the preceding swing phase, and I<sup>fc</sup> _f_<sup>indicatesthefirst-contacteventoffoot</sup><sup>_f_.</sup> 

**Domain randomization.** We apply domain randomization to improve sim-to-real transfer. The randomized quantities are listed in Table S2. Here, _µ_ denotes the ground friction coefficient, _bq_ denotes encoder bias, ∆ _p_ com denotes the torso center-of-mass offset, _α_ pi denotes the pseudo-inertia scaling factor, _τ_ fric<sup>rand</sup> denotes the randomized joint friction term, and _sd_ denotes the joint damping multiplier. The pseudo-inertia randomization 

13 

**Table S1 Reward terms.** 

|Term|Raw term _ri_<br>_wi_|
|---|---|
|Linear velocity tracking|exp<br>�<br>_−_<br>_∥v_<sup>_b_</sup><br>_xy_<sup>_−_[</sup><sup>_v_cmd</sup><br>_x_<br>_,v_<sup>cmd</sup><br>_y_<br>]_∥_<sup>2</sup><br>0_._25<br>�<br>2_._0|
|Yaw-rate tracking|exp<br>�<br>_−_<br>(_ω_<sup>_b_</sup><br>_z_<sup>_−ω_cmd</sup><br>_z_<br>)<sup>2</sup><br>0_._25<br>�<br>3_._0|
|Vertical velocity|(_v_<sup>_b_</sup><br>_z_<sup>)2</sup><br>_−_2_._0<br><br>|
|Upright torso|exp<br>�<br>_−_<br>_∥g_<sup>_b_</sup><br>_xy_<sup>_∥_2</sup><br>0_._2<br>�<br>1_._0|
|Joint posture|exp<br>�<br>_−_<br>����<br>_q_jnt_−q_<sup>def</sup><br>jnt<br>_σq_<br>����<br>2<sup>�</sup><br>1_._0|
|Joint position limits|�_nj_<br>_i_=1<br>�<br>max(_q_jnt_,i −q_<sup>max</sup><br>jnt_,i_<sup>_,_ 0)2 + max(</sup><sup>_q_min</sup><br>jnt_,i _<sup>_−q_jnt</sup><sup>_,i,_ 0)2�</sup><br>_−_1_._0<br>|
|Action rate|_∥a −a_prev_∥_<sup>2</sup><br>_−_0_._1|
|Foot clearance|_χ_cmd<br>�<br>_f∈F _<sup>_∥vf,xy∥_2</sup><sup>_|hf −h⋆_</sup><br>_f_<sup>_|_</sup><br>_−_2_._0<br>|
|Swing-foot height|_χ_cmd<br>�<br>_f∈F_ <sup>Ifc</sup><br>_f_<br>�<br>_h_<sup>peak</sup><br>_f_<br>_h_<sup>_⋆_</sup><br>_f_<br>_−_1<br>�2<br>_−_0_._25|
|Foot slip|_χ_cmd<br>�<br>_f∈F _<sup>_sf∥vf,xy∥_2</sup><br>_−_0_._1|
|Soft landing|_χ_cmd<br>�<br>_f∈F_ <sup>I(</sup><sup>_sf_ = 1)</sup><sup>_∥vf,z∥_2</sup><br>_−_1_._0_×_10<sup>_−_5</sup>|
|Torso angular velocity|_∥ω_<sup>_b_</sup><br>_xy_<sup>_∥_2</sup><br>_−_0_._05|
|Angular momentum|_∥L_root_∥_<sup>2</sup><br>_−_0_._02|
|Self-collision|Iself<br>_−_1_._0|
|Light-step reward|Eq. (6)<br>experiment-specific|


scales mass and inertia consistently for the leg, torso, and arm links. For joint friction and damping, the ranges in the table denote the final values reached by the curriculum during Stage 2. 

**Deployment setup.** All real-world experiments are conducted on the Unitree G1 humanoid. The high-level controller runs on an external laptop with an NVIDIA RTX 5070 Ti Laptop GPU. The laptop is connected to the robot through wired Ethernet. It receives joint positions, joint velocities, IMU measurements, and motor command information from the robot. It sends joint-position targets back to the robot. The onboard low-level controller tracks these targets with PD control. 

FAST-LIO (Xu et al., 2022) runs on the onboard computer of the G1. It publishes odometry at 100 Hz. The odometry provides velocity estimation and global localization. The laptop uses the latest FAST-LIO message to compute the root linear velocity, following _v_ root<sup>_R_=</sup><sup>_v_</sup> _L_<sup>_R−JL_(</sup><sup>_q_jnt) ˙</sup><sup>_q_jnt.Thisvelocityisusedbyboththe</sup> policy observation and the disturbance observer. 

The policy and the disturbance observer run on the laptop at 50 Hz, matching the policy update rate used during training. At each control step, the laptop first builds the current robot state from proprioception and FAST-LIO odometry. It then writes this state and the latest motor command into a local MuJoCo model. MuJoCo is not used to simulate future robot motion during deployment. Instead, it serves as a synchronized nominal dynamics model. After state synchronization, we call MuJoCo forward dynamics to compute the nominal dynamics terms required by the momentum observer. The observer updates the filtered residual using these nominal dynamics terms and the measured robot state. The filtered residual is normalized and concatenated with the policy observation. The policy then outputs the next joint-position target for onboard PD tracking. 

# **C Task descriptions.** 

**Torso pulling test.** We evaluate torso-level disturbance rejection in simulation by applying constant horizontal forces to the robot torso while it tracks a fixed forward velocity command. Each rollout starts from the reset state, followed by a 1 _._ 0 s settling phase with zero command and zero external force. The robot is then 

14 

**Table S2 Domain randomization.** 

|Term|Description|Range / setting|
|---|---|---|
|_µ_|Ground friction coefficient|[0_._3_,_1_._2]<br>|
|_bq_|Encoder bias|[_−_0_._015_,_0_._015] rad<br>|
|∆_p_com_,x_|Torso COM offset along _x_|[_−_0_._025_,_0_._025] m<br>|
|∆_p_com_,y_|Torso COM offset along _y_|[_−_0_._025_,_0_._025] m|
|∆_p_com_,z_|Torso COM offset along _z_|[_−_0_._03_,_0_._03] m|
|_α_pi<br>|Pseudo-inertia scaling factor|[_−_0_._05_,_0_._05]|
|_τ_ <sup>rand</sup><br>fric_,_leg<br>|Leg joint friction|[0_._05_,_1_._5]|
|_τ_ <sup>rand</sup><br>fric_,_waist<br>|Waist joint friction|[0_._05_,_1_._0]|
|_τ_ <sup>rand</sup><br>fric_,_arm|Arm joint friction|[0_._05_,_0_._8]|
|_sd,_leg|Leg joint damping scale|[0_._5_,_1_._5]<br>|
|_sd,_waist|Waist joint damping scale|[0_._7_,_1_._3]<br>|
|_sd,_arm|Arm joint damping scale|[0_._7_,_1_._3]<br>|
|_ϵvb_|Base linear velocity noise|[_−_0_._5_,_0_._5] m_/_s<br>|
|_ϵωb_|Base angular velocity noise|[_−_0_._2_,_0_._2] rad_/_s|
|_ϵgb_|Projected gravity noise|[_−_0_._05_,_0_._05]|
|_ϵq_jnt|Joint position noise|[_−_10<sup>_−_4</sup>_,_10<sup>_−_4</sup>] rad<br>|
|_ϵ_˙_q_jnt|Joint velocity noise|[_−_0_._03_,_0_._03] rad_/_s|


commanded with **v**<sup>cmd</sup> = [ _vx_<sup>cmd</sup> _,_ 0 _,_ 0] for 10 _._ 0 s, while a constant world-frame force is applied to torso_link. The applied wrench has zero moment and zero vertical-force component. For the sagittal-force evaluation, we set _vx_<sup>cmd</sup> _∈{_ 0 _._ 5 _,_ 0 _._ 8 _,_ 1 _._ 1 _}_ m _/_ s and apply _Fx ∈{−_ 60 _, −_ 40 _, −_ 20 _,_ 0 _,_ 20 _,_ 40 _,_ 60 _}_ N with _Fy_ = 0. For the directional evaluation, we fix _vx_<sup>cmd</sup> = 1 _._ 1 m _/_ s and apply forces with magnitudes of 40 N and 60 N along eight horizontal directions. Each simulated condition is evaluated with ten random seeds, and rollouts are recorded at the policy control rate. 

**Asymmetric hand loading test.** We evaluate asymmetric loading by applying a unilateral downward load to the right hand. In simulation, the load is modeled as a constant force applied to right_wrist_yaw_link. The commanded velocity is **v**<sup>cmd</sup> = [ _vx_<sup>cmd</sup> _,_ 0 _,_ 0], where _vx_<sup>cmd</sup> _∈{_ 0 _._ 5 _,_ 0 _._ 8 _,_ 1 _._ 1 _}_ m _/_ s, and the downward force magnitude is varied over _{_ 10 _,_ 20 _,_ 40 _}_ N. Each condition is evaluated with ten random seeds for both the baseline policy and ADAPT. For the real-robot test, the load is physically attached to the right hand. We use payloads of 1 kg, 2 kg, and 4 kg with forward commands of 0 _._ 8 m _/_ s and 1 _._ 1 m _/_ s. The reported real-world comparison uses three repeated trials per policy for each command-load condition. 

**Light-step reward shaping.** We evaluate light-step reward shaping during forward walking, without external payloads or applied disturbances. The robot tracks a fixed command **v**<sup>cmd</sup> = [0 _._ 8 _,_ 0 _,_ 0]. In simulation, we compare the baseline policy and the policy trained with the light-step reward over 20 random seeds per policy. For each trajectory, the observer is already running before the walking command starts. We then collect command-following data to compute the reported curves. For the real-robot evaluation, we use the same forward command and compare the baseline policy with the reward-shaped policy. Since the real robot does not provide ground-truth foot contact forces, we report the observer-based leg disturbance envelope instead of measured contact force. The envelope is computed from the normalized residuals of the 12 leg joints. We first compute the envelope for each leg and then take the maximum over the left and right leg envelopes. The reported real-world comparison uses seven completed trials per policy. 

# **D Evaluation criterion** 

We report three metrics for fixed-command locomotion. The forward **velocity tracking error** is computed as the root-mean-square error between the commanded forward velocity _vx_<sup>cmd</sup> and the forward velocity _vx,k_<sup>_b_ofroot</sup> in over the evaluation window _T_ 


In forward-velocity tracking tasks, the robot is expected not only to maintain the commanded speed but also to preserve its walking direction. We therefore evaluate directional stability using two metrics: **lateral drift** 

15 


**FigureS2 Unified-scalenormalizationablation.** The baseline here denotes a variant of ADAPT using standard-normalization instead of our unified normalization. _Left:_ Velocity tracking error, lateral drift, and yaw drift under sagittal torso forces across three command velocities. _Right:_ Radar plots summarize results across disturbance directions. 

and **yaw drift** 


where the position is measured in the world frame, and _k_ start and _k_ end denote the first and last timesteps of the evaluation window. The yaw drift is computed as the wrapped heading change, 


For policy comparison, we report the magnitudes _|dy|_ and _|dψ|_ , where lower values indicate better rejection of lateral and rotational deviations under external disturbances or asymmetric payloads. 

# **E Unified-scale ablation** 

We evaluate unified-scaled normalization for two stages in velocity tracking under external force perturbations as the baseline. We compare ADAPT with a standard-normalization variant, where the estimated disturbances are normalized by standard statistics instead of a unified normalization. As shown in Fig. S2, ADAPT tracks the velocity more robustly under perturbations with lower drift. This result shows that joint effort provides a useful scale for representing disturbance estimates. 

# **F Supplementary experiment results** 

**Asymmetric hand loading test.** Fig. S3 provides additional results for the asymmetric hand loading test. In simulation, we apply one-sided downward forces on the robot hand with magnitudes of 10 N, 20 N, and 40 N. In the real-world experiment, we attach asymmetric payloads to one hand, including 1 kg, 2 kg and 4 kg loads. For both simulation and real-world tests, we evaluate fixed-forward-velocity walking under two commands, _vx_<sup>cmd</sup> = 0 _._ 8 m _/_ s and _vx_<sup>cmd</sup> = 1 _._ 1 m _/_ s, the supplementary comparison reports the matching simulation results under the same two forward velocity commands. 

The plots show the lateral drift with respect to the forward walking distance. Across both simulation and realworld experiments, ADAPT produces smaller lateral drift than the baseline under asymmetric loading. This indicates that ADAPT can better maintain the commanded walking direction under unbalanced disturbances. 

16 


**Figure S3 Supplementary results for the asymmetric hand loading test.** We report lateral drift trajectories under one-sided hand loads in simulation and on the real robot. ADAPT maintains a straighter walking direction than the baseline under asymmetric disturbances. 

17 

