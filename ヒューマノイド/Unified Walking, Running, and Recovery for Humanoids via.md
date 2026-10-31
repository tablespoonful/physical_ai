---
title: "Unified Walking, Running, and Recovery for Humanoids via State-Dependent Adversarial Motion Priors"
date: "2026-05-18"
authors: "Yidan Lu; Yichao Zhong; Liu Zhao; Wanyue Li; Peng Lu"
url: https://arxiv.org/abs/2605.18611
pdf: https://arxiv.org/pdf/2605.18611
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.18611)** / [論文ページ](https://arxiv.org/abs/2605.18611)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Unified** 

# **Walking, Running, and Recovery for Humanoids via State-Dependent Adversarial Motion Priors** 

Yidan Lu, Yichao Zhong, Liu Zhao, Wanyue Li, Peng Lu<sup>_†_</sup> 

**_Abstract_ — We propose a unified reinforcement learning framework that enables a single policy to perform walking, running, and fall recovery on the Unitree G1 humanoid robot, validated on physical hardware without any explicit modeswitching command at deployment. The framework extends Adversarial Motion Priors (AMP) by replacing the conventional global reference distribution with a state-dependent gate that routes each training transition to one of two discriminators: a dedicated recovery discriminator and a velocity-conditioned locomotion discriminator that jointly covers walking and running. The gate is defined by a single fixed threshold on projected gravity: the recovery discriminator is activated when body tilt exceeds approximately** 37<sup>_◦_</sup> **from vertical (** _|gz_ +1 _| >_ 0 _._ 6 **); otherwise the locomotion discriminator is used, with the normalized commanded velocity serving as a condition that selects the appropriate reference trajectory between walk and run clips. Only three LAFAN1 reference clips are required to regularize the complete behavior set. At deployment, a single frozen ONNX policy executes at 50 Hz with no runtime mode logic; hardware experiments demonstrate successful recovery from both prone and supine falls and smooth walk-to-run transitions under the same controller.** 

## I. INTRODUCTION 

Humanoid robots deployed in unstructured environments must seamlessly execute agile locomotion and robustly recover from falls. Conventional approaches address these demands through modular architectures in which walking, running, and recovery are implemented as separate controllers coordinated by a hand-crafted finite state machine [1]. While this decomposition simplifies individual controller design, it entails significant practical limitations: transition logic requires manual tuning, behavioral boundaries can be brittle near mode boundaries, and motion quality may degrade during inter-module handoffs. 

Recent advances in reinforcement learning have demonstrated that humanoid standing-up and fall recovery can be acquired end-to-end without handcrafted motion scripts [2], [3], [4], [5], [6], [7]. In parallel, motion-prior-based methods such as DeepMimic and Adversarial Motion Priors (AMP) have established that reference motions significantly improve the physical plausibility and style consistency of learned behaviors [8], [9]. However, AMP is most naturally formulated for a single behavioral mode or a shared motion distribution, whereas humanoid operation in practice spans qualitatively distinct regimes—steady locomotion, high-speed running, 

> _†_ Corresponding author: Peng Lu (lupeng@hku.hk). The University of Hong Kong, Hong Kong SAR, China. 

> _E-mail:_ ydlu@connect.hku.hk, yichao.zhong@connect.hku.hk, zhaol@connect.hku.hk, liwy1024@connect.hku.hk. 


Fig. 1. Overview of the proposed framework. A shared actor policy _πθ_ is trained with a composite reward comprising task terms and a modespecific AMP reward. At each training step, the state-dependent gate _g_ ( _st,_ ˆ _vt_ ) routes each transition to one of two discriminators: the recovery discriminator (activated when body tilt exceeds _∼_ 37<sup>_◦_</sup> ) or the velocityconditioned locomotion discriminator, which selects between walk and run reference trajectories based on the normalized commanded velocity _v_ ˆ _t_ . At deployment, only the frozen policy is used; no runtime mode logic is required. 

and recovery from failure—each with different kinematic characteristics. 

This work proposes a targeted extension: maintaining a single shared actor policy while switching the adversarial motion prior in response to the current robot state and command. Two discriminators are trained in parallel—a recovery discriminator regularized by a fall-recovery reference clip, and a velocity-conditioned locomotion discriminator that jointly covers walking and running by conditioning on the commanded velocity to select the appropriate reference trajectory. A lightweight, interpretable gating function selects the active discriminator at each training step based on body orientation, ensuring that the AMP reward signal is always mode-consistent. The resulting policy requires no runtime mode selector and is deployed as a single frozen model, yet produces behaviorally appropriate motion across all three regimes. 

## II. PROBLEM FORMULATION 

We consider the problem of learning a single humanoid controller _πθ_ ( _at | ot_ ) that spans three qualitatively distinct behavioral regimes: walking, running, and fall recovery. The observation _ot_ comprises body angular velocity, projected gravity, commanded velocity, relative joint positions, joint velocities, and previous actions. Each observation frame is 96-dimensional; a history of four consecutive frames is concatenated before policy inference, yielding a 384dimensional input. The action _at ∈_ R<sup>29</sup> specifies target joint positions, which are tracked by low-level PD controllers. 


Fig. 2. Hardware demonstration of the unified policy on Unitree G1. **Top:** supine recovery _→_ walk _→_ run. **Bottom:** prone recovery _→_ walk _→_ run. Both sequences are executed by a single deployed controller with no mode-switch command; the active motion prior is selected automatically by the statedependent gate (Eq. 5). 

The central challenge is maintaining coherent behavioral regularization across regimes with fundamentally different kinematics: walking and running are cyclic velocity-tracking behaviors, whereas recovery requires rapid posture reorientation through multi-contact support phases. A single shared motion prior is poorly suited to this envelope—a global reference distribution either fails to capture high-speed running statistics or conflates locomotion with recovery dynamics, degrading motion quality in both regimes. 

## III. METHOD 

## _A. Policy and Task Reward_ 

The actor policy _πθ_ ( _at | ot_ ) is trained end-to-end and deployed as a single ONNX model without any runtime mode logic. The primary task reward combines velocity tracking, motion smoothness, postural stability, and safety penalties: 


## _B. State-Dependent Motion Prior_ 

We employ two discriminators. A recovery discriminator _Dϕ_<sup>rec</sup> is trained exclusively on fall-recovery transitions. A velocity-conditioned locomotion discriminator _Dϕ_<sup>loco</sup> accepts the normalized commanded velocity _v_ ˆ _t ∈_ [0 _,_ 1] as an additional input and is trained jointly on walk and run reference transitions, using _v_ ˆ _t_ to interpolate between the two reference distributions—providing style-consistent rewards across the full speed range without separate walk and run networks. 

For each state transition ( _st, st_ +1) encountered during training, a binary gating function _g_ ( _st_ ) selects the active discriminator: 


The AMP style reward is then computed as 


and the total training reward is 


## _C. Gating Function_ 

The gate _g_ is defined by a single fixed threshold rather than a learned classifier: 


where _gz_ is the _z_ -component of the projected gravity vector ( _gz ≈−_ 1 when upright, near zero or positive when fallen). A fixed threshold is justified because the gravity signal is bimodal by construction—the _|gz_ + 1 _| >_ 0 _._ 6 boundary corresponds to _≈_ 37<sup>_◦_</sup> tilt and lies in a low-occupancy region of the signal’s empirical distribution, making it accurate and robust to noise without a learned gating mechanism. When the locomotion branch is active, _v_ ˆ _t_ = min( _vx_<sup>cmd</sup> _/v_ max _,_ 1) is passed as a condition to _Dϕ_<sup>loco</sup> , selecting reference transitions from the walk clip at low _v_ ˆ _t_ and from the run clip at high _v_ ˆ _t_ . This gate is active only during training; at inference time, the deployed policy is a monolithic network with no explicit mode variable. 

## _D. Reference Motion Retargeting_ 

Three reference clips are drawn from the LAFAN1 dataset [10] and retargeted to the G1 joint space via inverse kinematics: walk1 ~~s~~ ubject1, run1 ~~s~~ ubject2, 

and fallAndGetUp2 ~~s~~ ubject2. The recovery clip exclusively trains _Dϕ_<sup>rec.Bothlocomotionclipstrain</sup><sup>_D_</sup> _ϕ_<sup>loco</sup> : at each discriminator update, a reference transition is sampled from the walk clip with probability (1 _−v_ ˆ _t_ ) and from the run clip with probability _v_ ˆ _t_ , so the condition consistently indexes the intended reference distribution. 

## IV. EXPERIMENTS 

## _A. Setup_ 

The policy is trained in Isaac Lab [11] simulation using Proximal Policy Optimization (PPO) [12] with AMP auxiliary reward weighted at _λ_ amp = 0 _._ 5. The network is a three-layer MLP operating on a 384-dimensional stacked observation. Upon convergence, the policy is exported as an ONNX model and deployed at 50 Hz on the physical Unitree G1 via a C++ finite state machine that reads joint states and issues PD position targets. No sim-to-real adaptation or domain randomization fine-tuning is applied beyond standard simulation parameter randomization during training. 

## _B. Locomotion_ 

The deployed policy successfully tracks forward velocity commands over [ _−_ 0 _._ 5 _,_ 1 _._ 0] m/s in normal operating mode and [ _−_ 1 _._ 5 _,_ 3 _._ 0] m/s in fast mode. Fast mode is engaged via an explicit operator command, reflecting a deliberate safety constraint. Across this speed range, the velocity-conditioned locomotion discriminator _Dϕ_<sup>loco</sup> continuously interpolates between walk and run reference distributions via _v_ ˆ _t_ , producing a smooth style-consistent reward signal without any discrete mode switch. Observed gait characteristics are consistent with the respective reference clips: walking exhibits a regular heel-toe contact cycle, while running displays elongated stride length and reduced double-support phase duration. 

## _C. Fall Recovery_ 

Recovery is evaluated from two hardware configurations: prone (face-down) and supine (face-up). Because the projected gravity condition in Eq. (5) continuously routes fallenstate transitions to _Dϕ_<sup>rec</sup> throughout training, the policy acquires recovery behavior without any dedicated recovery module or separate training phase. As shown in Fig. 2, the robot successfully regains a stable upright stance from both configurations without manual intervention. 

## _D. Unified Behavioral Continuity_ 

Fig. 2 presents complete hardware rollouts demonstrating the unified nature of the controller. Starting from a fallen configuration, the robot executes the full recovery _→_ walk _→_ run sequence under a single deployed policy in both the supine and prone conditions. These results confirm that the three behavioral regimes are stably encoded within a single policy and that the mode transitions induced by the training-time gating rule produce coherent, continuous motion at deployment. 

## V. CONCLUSION 

We have presented a unified humanoid control framework in which a single reinforcement learning policy covers walking, running, and fall recovery through state-dependent adversarial motion priors. The key design choice is a twodiscriminator structure: a dedicated recovery discriminator and a velocity-conditioned locomotion discriminator that jointly handles walking and running within a single network. A single fixed threshold on projected gravity routes training transitions between the two discriminators, ensuring modeconsistent style regularization without learned gating complexity. The minimality of the reference set—three LAFAN1 clips—demonstrates that structural separation of recovery and locomotion priors can be more important than reference diversity for achieving qualitatively distinct and physically plausible behaviors within a shared policy. Hardware validation on the Unitree G1 confirms that the learned controller generalizes from simulation to real-world conditions and supports seamless behavioral transitions across locomotion and recovery regimes without runtime mode management. 

## REFERENCES 

- [1] J. Pratt, J. Carff, S. Drakunov, and A. Goswami, “Capture point: A step toward humanoid push recovery,” in _2006 6th IEEE-RAS International Conference on Humanoid Robots_ . IEEE, 2006, pp. 200–207. 

- [2] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [3] X. He, R. Dong, Z. Chen, and S. Gupta, “Learning getting-up policies for real-world humanoid robots,” _arXiv preprint arXiv:2502.12152_ , 2025. 

- [4] P. Chen, Y. Wang, C. Luo, W. Cai, and M. Zhao, “Hifar: Multi-stage curriculum learning for high-dynamics humanoid fall recovery,” _arXiv preprint arXiv:2502.20061_ , 2025. 

- [5] C. Gaspard, M. Duclusaud, G. Passault, M. Daniel, and O. Ly, “Frasa: An end-to-end reinforcement learning agent for fall recovery and stand up of humanoid robots,” _arXiv preprint arXiv:2410.08655_ , 2024. 

- [6] Z. Meng, T. Liu, L. Ma, Y. Wu, R. Song, W. Zhang, and S. Huang, “Safefall: Learning protective control for humanoid robots,” _arXiv preprint arXiv:2511.18509_ , 2025. 

- [7] Z. Xu, S. Bahl, and D. Pathak, “Unified humanoid fall-safety policy from a few demonstrations,” _arXiv preprint arXiv:2511.07407_ , 2025. 

- [8] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions on Graphics_ , vol. 37, no. 4, 2018. 

- [9] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics_ , vol. 40, no. 4, 2021. 

- [10] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal, “Robust motion in-betweening,” _ACM Transactions on Graphics_ , vol. 39, no. 4, pp. 60:1–60:12, 2020. 

- [11] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mukopadhyay, G. Bhatt, R. Burgess-Limerick, A. Mandlekar, M. Hutter, and A. Garg, “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 6, pp. 3740–3747, 2023. 

- [12] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

