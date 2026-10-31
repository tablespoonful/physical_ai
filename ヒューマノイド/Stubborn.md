---
title: "Stubborn: A Streamlined and Unified Reinforcement Learning Framework for Robust Motion Tracking and Fall Recovery for Humanoids"
date: "2026-06-11"
authors: "Xiao Ren; Yuhui Yang; Zongbiao Weng; Zhijie Liu; He Kong"
url: https://arxiv.org/abs/2606.12814
pdf: https://arxiv.org/pdf/2606.12814
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.12814)** / [論文ページ](https://arxiv.org/abs/2606.12814)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Stubborn: A Streamlined and Unified Reinforcement Learning Framework for Robust Motion Tracking and Fall Recovery for Humanoids** 

**Xiao Ren**<sup>_∗_</sup> **, Yuhui Yang**<sup>_∗_</sup> **, Zongbiao Weng, Zhijie Liu, and He Kong**<sup>_†_</sup> 

**Abstract:** Recent reinforcement learning approaches have shown great promise in improving humanoid motion tracking performance and achieving fall recovery under disturbances. However, most existing works treat motion tracking and fall recovery as different tasks and require multi-stage training with specialized recovery rewards and/or separate recovery policies. Moreover, existing reinforcement learning-based methods often terminate training episodes immediately after severe tracking failures, limiting recovery-oriented exploration in unstable or fallen states. To address the above issues, we propose Stubborn, a streamlined and unified reinforcement learning framework to achieve robust humanoid motion tracking and fall recovery. Specifically, Stubborn uses an asymmetric ActorCritic architecture and consists of three major components. First, a yaw-aligned tracking representation is adopted to reduce sensitivity to global drift and heading disturbances while preserving gravity-related balance information. Second, we introduce a Bernoulli-based probabilistic termination mechanism that enables the policy to encourage exploration of fall-recovery behaviors under varying failure modes. Third, we propose a probabilistic termination and tracking-error-driven strategy that dynamically reshapes the sampling distribution based on tracking performance, increasing the training efficiency for difficult motion segments and unstable states. Extensive comparisons with SOTA methods and ablation studies show that Stubborn achieved competitive performance, and the proposed probabilistic termination mechanism and adaptive sampling strategy contributed to the performance and robustness gains. For real-world demonstrations, please refer to https://aislab-sustech.github.io/Stubborn/. 

**Keywords:** Humanoids, reinforcement learning, motion tracking, fall recovery 

## **1 Introduction** 

Recent years have witnessed much progress in reinforcement learning-based highly dynamic motion tracking for humanoids, including dancing [1, 2, 3] and martial arts [4, 5]. There exist works that rely on global absolute pose tracking for training, which might cause the policy to exert excessive control effort to correct translation and heading deviations after perturbations [6, 7]. To address the above issue, recent works in the literature adopt a yaw-aligned tracking representation to reduce sensitivity to global drift and heading disturbances while preserving gravity-related balance information [8, 9]. 

Although existing reinforcement learning (RL) methods can achieve remarkable performance under normal conditions, maintaining tracking accuracy and robustness (e.g., recovering from falls) under strong external disturbances remains a challenging problem [10, 11, 12]. In particular, how to enhance tracking performance and robustness in an effective and unified way, rather than treating 

> _∗_ Xiao Ren and Yuhui Yang contributed equally to this work. The authors are with the Southern University of Science and Technology, Shenzhen 518055, China. E-mails: [12431359;12411024;12433032;12332642]@mail.sustech.edu.cn, kongh@sustech.edu.cn. 

> _†_ Corresponding author. 


Figure 1: **Overview of Stubborn.** The policy is trained with a yaw-aligned representation and via an asymmetric actor-critic architecture, with a Bernoulli-based soft termination mechanism, and probabilistic termination and tracking error-driven sampling strategy. 

motion tracking and fall recovery as separate tasks, has not been well explored and several design issues remain to be addressed. 

In particular, under long-horizon training, uniformly sampled training data often under-represent difficult motion segments and unstable states, limiting the exploration capability of the policy [13, 14]. In addition, for fall recovery, most existing methods employ hard termination mechanisms: once the tracking error exceeds a predefined threshold, the policy training terminates (or, during deployment, the execution terminates). Such designs would prematurely prevent the policy from exploring to learn to recover. Existing studies often address this issue through recovery-specific rewards, multi-stage training procedures, or separate recovery controllers [15, 16], thus increasing the architectural or training complexity. 

To address these challenges, we propose Stubborn, a streamlined and unified RL framework for training a single policy to achieve robust humanoid motion tracking and fall recovery. As shown in Figure 1, Stubborn uses a unified single policy for tracking highly dynamic motions while maintaining robustness under strong perturbations and achieving recovery from fallen states. Stubborn adopts an asymmetric Actor-Critic architecture [17] with yaw-aligned tracking representation, where the value network uses privileged simulation information, while the policy network relies only on proprioceptive observations. On this basis, we make the following contributions: (1) We propose a Bernoulli-based soft termination mechanism that encourages the policy to learn resilient actions in unstable and fallen states, thereby synthesizing emergent recovery behaviors without auxiliary recovery-specific reward design. (2) We develop a probabilistic termination (PT) and tracking error-driven sampling strategy that dynamically reshapes the sampling distribution based on online tracking performance, thereby improving learning efficiency in difficult tracking and recovery states. (3) Extensive simulations and real-world experiments on the 29-DoF Unitree G1 humanoid robot demonstrate that Stubborn achieves competitive performance against SOTA methods [18, 19, 20, 13]. Ablation studies have also shown that the proposed probabilistic termination mechanism and adaptive sampling strategy contribute to performance gains. 

## **2 Related Work** 

**Humanoid Motion Tracking:** In recent years, reinforcement learning has become a common paradigm for humanoid motion imitation and tracking [6, 13, 21, 22]. For example, DeepMimic [6] 

2 

learns physics-based controllers by tracking reference motion clips with imitation objectives. BeyondMimic [13] learns motion-tracking primitives for highly dynamic humanoid skills through adaptive sampling and distills the learned primitives into a guided diffusion policy for downstream humanoid control. HumanPlus [21] and OmniH2O [22] primarily target whole-body imitation, teleoperation, and autonomous behavior learning, rather than unified motion tracking in highly dynamic, long-horizon settings. ASAP [23] improves sim-to-real transfer for agile humanoid skills through real-to-sim-to-real adaptation, while GMT [14] improves general motion tracking through large-scale motion data, adaptive sampling, and a motion mixture-of-experts architecture. HoloMotion [18] explores foundation models for whole-body control to improve diverse motion generation and tracking, while BFM-Zero [20] focuses on zero-shot and few-shot robot motion transfer. 

Motion tracking is closely related to whole-body control [24], and data-driven whole-body control methods have further advanced this direction. ExBody2 [25, 26] emphasizes stable wholebody imitation under diverse reference motions. TWIST [27, 28] and CLONE [29] improve longhorizon whole-body control through real-time teleoperation and closed-loop correction, respectively. SONIC [30] further explores scaling motion tracking toward general whole-body behaviors. Although recent work continues to advance unified data-driven representations and broader generalization, challenges remain in robustness under strong perturbations, learning difficult long-horizon motion segments, and handling tracking and recovery within a unified framework. 

**Robustness and Fall Recovery:** Motion robustness and autonomous fall recovery are important capabilities for humanoid robots in practice. RL-based methods have been widely used to train standing-up and push-recovery policies for humanoids [31, 32, 33]. For example, HoST [34] improves recovery across diverse poses through a multi-critic architecture and curriculum learning, while HumanUP [35] learns standing-up policies across multiple terrains and initial fall states. HuB [36] improves humanoid balance robustness by combining reference motion refinement, balance-aware policy learning, and robustness training. Although the above-mentioned methods help to learn recovery and balance behaviors, policies are typically designed for specific recovery or balance scenarios, separately from the motion tracking policy, requiring extensive reward tuning. Unlike recovery-specific policy learning, recent studies have also improved robustness from the perspective of motion tracking. For example, Any2Track [19] adopts a two-stage tracker-adapter framework to improve motion tracking robustness under disturbances and sim-to-real variations. 

Overall, existing works often treat motion tracking and fall recovery as competing objectives with conflicting gradients [31]. To decouple these tasks, the community seeks solutions using multistage training and separate recovery policies with recovery-specific rewards. We argue that tracking failures actually provide a natural gateway to the fall state manifold. By harnessing these natural transitions rather than avoiding them, one might achieve high-fidelity motion tracking, robustness to strong perturbations, and recovery from unstable states with a unified training framework and policy. This is the objective that this paper aims to fulfill. Our framework spontaneously explores recovery behaviors alongside motion tracking, enabling highly sample-efficient, simultaneous exploration of both tasks within a single policy. 

## **3 Method** 

Stubborn, as illustrated in Figure 1, is trained using an asymmetric actor-critic architecture and consists of three core modules. Due to limited space, details of the drift-invariant yaw-aligned tracking representation are placed in the Appendix section while the Bernoulli-based PT mechanism, as well as the PT and tracking error-driven sampling strategy are described in the following. 

### **3.1 Bernoulli-based Probabilistic Termination for Fall Recovery Learning** 

**Conditional Bernoulli Termination Mechanism:** In our framework, when the tracking error exceeds a predefined threshold, the environment does not terminate the episode deterministically; instead, it triggers a termination with a user-specified probability. More specifically, we denote the height error _e_<sup>_p_</sup> _root,z_<sup>oftherobot’sfloatingbaseandtheorientationerror</sup><sup>_e_</sup> _root_<sup>_q_,computedviathe</sup> 

3 

quaternion inner product in SO(3), as follows: 


Let _τt ∈{_ 0 _,_ 1 _}_ denote the binary termination indicator at time step _t_ . We model this indicator via a conditional Bernoulli distribution: 


where _st_ represents the system state. The termination probability _pterm_ is designed to accommodate the physical time window required for fall recovery, thereby mitigating value estimation bias caused by standard time-limit truncation. In the following, we provide guidelines for selecting _pterm_ . 

**Design of the Termination Probability:** If the robot remains in a marginally stable state after exceeding the tracking error threshold, the number of additional survival steps before episode termination can be modeled as a random variable _T ∼ Geo_ ( _pterm_ ). To maintain consistent temporal difference (TD) updates, the expectation of _T_ should align with the physical recovery time: 


where _fctrl_ = 50 Hz is the control frequency. We set the physical recovery time to _trec_ = 4 s, which provides the policy with an expected exploration horizon of 200 steps (E[ _T_ ] = 200). A window that is too restrictive can degenerate the mechanism into a deterministic one, thus hindering the learning of recovery behaviors, and vice versa. Following this design guideline, we select _pterm_ = 0 _._ 005, and set the thresholds to _θpos_ = 0 _._ 25 m and _θquat_ =<sup>_<u>π</u>_</sup> 2<sup>rad in our experiments.</sup> 

Under this mechanism, after the tracking error exceeds the threshold, the episode continues at each subsequent step with probability 1 _− pterm_ . Let _k_ denote the number of additional control steps after entering the unstable region; then the probability that the episode remains active for more than _k_ steps is _P_ ( _T > k_ ) = (1 _− pterm_ )<sup>_k_</sup> . This design reduces immediate termination after disturbances or falls and provides a probabilistic recovery window for learning recovery behaviors toward postperturbation stable tracking. Furthermore, assuming a perturbation occurs early in the episode, under an ideal exploration window with a maximum episode length ( _T_ max = 1000), the cumulative probability of terminating prior to the step limit is given by _P_ ( _T ≤ T_ max) = 1 _−_ (1 _− pterm_ )<sup>_T_max</sup> _._ Substituting our selected parameters ( _pterm_ = 0 _._ 005, _T_ max = 1000), this probability evaluates to approximately 0 _._ 993. The parameter _pterm_ , derived from physical recovery constraints, ensures that the vast majority ( _>_ 99%) of unstable episodes terminate probabilistically before reaching the step limit. This substantially mitigates the TD distortion caused by truncation and promotes the stability of long-horizon optimization. 

### **3.2 Probabilistic Termination and Tracking Error Driven Sampling** 

Under hard termination, segments with tracking errors exceeding a predefined threshold are more likely to terminate the episode early [13]. However, under the PT mechanism described in Section 3.1, segments exceeding the error threshold are not terminated immediately; instead, the episode terminates only with a certain probability. As a result, episode termination is no longer a reliable proxy for segment difficulty, since it is affected by stochastic termination and external perturbations. Consequently, the correspondence between termination statistics and segment difficulty is weakened, making hard-sample mining based on termination statistics less reliable. To address this issue, we propose a probabilistic termination and tracking-error-driven adaptive sampling strategy. 

Let the total length of the reference trajectory be _N_ , and let _wt_ denote the unnormalized sampling weight associated with reference frame _t_ . At each environment reset, an initial frame _t_ 0 is sampled according to the normalized sampling distribution, and an episode of maximum length _T_ max is executed from that frame. Let _T_ denote the actual episode length, where 1 _≤ T ≤ T_ max, and let _e_ kp _, t_ denote the instantaneous keypoint tracking error at reference frame _t_ . Then, for an episode 

4 

starting at _t_ 0 and lasting _T_ steps, the average keypoint tracking error is defined as 


where ¯ _e_ represents the average keypoint tracking error over the current reference segment. For each time step _t ∈_ [ _t_ 0 _, t_ 0 + _T −_ 1] within the sampled segment, the weight increment ∆ _wt_ is defined as 


Here, _θ_ success denotes the success threshold for the average tracking error, and we set _θ_ success = 0 _._ 06 in our implementation. A segment is regarded as successfully tracked when ¯ _e < θ_ success; otherwise, it is considered to require further training. Moreover, ∆ _wi >_ 0 and ∆ _wd >_ 0 denote the step sizes for increasing and decreasing the sampling weights, respectively. In our implementation, ∆ _wi_ = 0 _._ 10 and ∆ _wd_ = 0 _._ 05. When an episode reaches the maximum length _T_ max while maintaining a low average error, the local decay operator Φatt( _t_ ) is applied. When an episode satisfies _e_ ¯ _< θ_ success but terminates before reaching the maximum length, i.e., _T < T_ max, the local redistribution operator Φdist( _t_ ) is applied. They are defined as 


Subsequently, the sampling weights of the reference frames involved in the current episode are updated as follows: where _w_ min and _w_ max denote the lower and upper bounds of the sampling weights, respectively. In our implementation, we set _w_ min = 0 _._ 05 and _w_ max = 1 _._ 0. After the update, the weights are normalized to obtain the sampling distribution for selecting the starting max( _wt,w_ min) frame of the next episode as follows _pt_ = <u>�</u> _Nj_ =0 _−_ 1<sup>max(</sup><sup>_wj,w_min).In this way, the online tracking error</sup> _e_ ¯ serves as an empirical indicator of segment difficulty, allowing the sampling distribution to adapt dynamically even under the probabilistic termination mechanism. As a result, more probability mass is assigned to high-error regions, encouraging training to focus on difficult motion segments. The overall algorithm of Stubborn is summarized in Algorithm 1 in Appendix. 

## **4 Results and Discussions** 

This section provides a systematic evaluation of Stubborn through both simulation and real experiments, with a focus on the following four questions: **Q1** : How does Stubborn compare with baseline methods on large and diverse motion datasets, and how well does it generalize to unseen motions? **Q2** : Does the PT mechanism improve disturbance recovery and fall recovery capability under strong perturbations **Q3** : Does the proposed PT and tracking error-driven sampling strategy improve tracking performance across diverse motion skills? **Q4** : How does Stubborn perform in real-world scenarios? 

### **4.1 Experiment Setup** 

Simulation experiments are conducted in IsaacLab/MuJoCo using motions from the public LAFAN1 [37] dataset. Real-robot experiments are performed on the 29-DoF Unitree G1 humanoid robot with retargeted motions from LAFAN1 [37] and AMASS [38] to evaluate the practical deployability of the learned policy. 

**Baselines.** We compare Stubborn with representative humanoid motion tracking methods, including HoloMotion [18], Any2Track [19], BFM-Zero [20], and a From-scratch multi-motion RL baseline [39]. The latter follows BeyondMimic [13] in its algorithmic framework and network architecture, while extending single-motion tracking to end-to-end multi-motion RL training. We do not 

5 

directly compare with OmniXtreme [39], as it uses substantially larger-scale motion data and targets general highly dynamic humanoid control, whereas our evaluation focuses on precise motion tracking, robustness, and fall recovery. 

**Evaluation Metrics and Training Details.** For motion tracking, we use root-relative mean per-body position error (MPBPE, mm), mean per-joint position error (MPJPE, 10<sup>_−_3</sup> rad), mean per-joint velocity error (MPJVE, 10<sup>_−_3</sup> rad/s), and acceleration deviation (∆acc, rad/s<sup>2</sup> ). For recovery, the robot is subjected to strong external perturbations that may cause unstable tracking, severe balance loss, or complete falls. A trial is successful if the robot re-establishes stable tracking within the predefined tracking-error threshold after the disturbance or fall, and unsuccessful otherwise. The main evaluation metric is the success rate (Succ, %). The reward items and key training configurations are summarized in the Appendix (see Tables 4 and 5, respectively). 

### **4.2 Results on Motion Tracking** 

To address **Q1** , this section compares the motion tracking accuracy of Stubborn with baseline methods on the full LAFAN1 dataset. All methods were evaluated on the MuJoCo simulation platform, and the results are shown in Table 1, where the results are reported as the mean _±_ one standard deviation. Stubborn achieves lower errors in MPBPE, MPJPE, and MPJVE. Compared with Fromscratch RL, MPBPE decreases from 62 _._ 68 to 48 _._ 85, MPJPE decreases from 115 _._ 43 to 113 _._ 38, and MPJVE decreases from 887 _._ 87 to 624 _._ 03. These results indicate that the proposed method improves whole-body position tracking and joint velocity tracking performance under the current test settings. Furthermore, the relatively small standard deviations of MPBPE and MPJVE suggest that the evaluation results on the full LAFAN1 dataset are relatively stable. 

Table 1: Quantitative results of motion tracking on the complete LAFAN1 dataset. Results are reported as mean _±_ standard deviation. Bold indicates the best result. 

|Method_|_Metric|MPBPE_↓_|MPJPE_↓_|MPJVE_↓_|∆acc_↓_|
|---|---|---|---|---|
|HoloMotion [18]|162_._92_±_0_._000|150_._65_±_0_._000|758_._56_±_0_._000|19_._47_±_0_._000|
|Any2Track [19]|401_._26_±_0_._000|122_._44_±_0_._000|913_._41_±_0_._000|26_._44_±_0_._000|
|BFM-Zero [20]|214_._09_±_0_._000|299_._36_±_0_._000|1100_._88_±_0_._000|**17**_._**07**_±_0_._000|
|From-scratch RL [13]|62_._68_±_0_._000|115_._43_±_0_._000|887_._87_±_0_._000|27_._75_±_0_._000|
|Ours|**48**_._**85**_±_0_._000|**113**_._**38**_±_0_._000|**624**_._**03**_±_0_._000|17_._09_±_0_._000|


For ∆acc, Stubborn achieves a score of 17 _._ 09, which is lower than HoloMotion, Any2Track, and From-scratch RL, and is close to BFM-Zero. Although BFM-Zero achieves a slightly lower ∆acc value, its MPBPE, MPJPE, and MPJVE are substantially higher than those of Stubborn. Considering these metrics together, Stubborn achieves lower tracking errors across the full LAFAN1 dataset while maintaining stable, smoother dynamic motion performance. 

### **4.3 Ablation Studies** 

To address **Q2** , we perform an ablation study on the PT mechanism under a strong external perturbation of 5 m/s, as shown in Table 2. We compare the full Stubborn framework with a variant without 

Table 2: Ablation study of the probabilistic termination strategy. Bold means better. 

|**Method**|**Threshold (m)**|**Success (%)**_↑_|
|---|---|---|
|w/o PT|0.15<br>0.25|77.5<br>85.0|
|Ours|0.15<br>0.25|**100**<br>**100**|


6 

PT (w/o PT), while keeping all other settings unchanged. We define the recovery threshold as the success criterion based on the tracking error after perturbation. Specifically, recovery is considered successful once the tracking error falls below the threshold again. Here, 0 _._ 15 m corresponds to a strict criterion, whereas 0.25 m corresponds to a more moderate one. Under both thresholds, Stubborn with PT achieves a recovery success rate of 100%, while w/o PT achieves 77 _._ 5% and 85 _._ 0%, respectively. These results indicate that PT improves recovery success under strong perturbations. 


Figure 2: Ablation results of the PT mechanism. The recovery success rate and the average number of recovery steps of Stubborn with PT (Ours) and w/o PT are compared under recovery thresholds of 0.15 m and 0.25 m. Ours achieves higher recovery success rates and requires fewer recovery steps under both recovery thresholds. 

Figure 2 shows the recovery success rate and the average number of recovery steps during training under a 5 m/s external perturbation. Ours converges faster and exhibits more stable performance under both thresholds, whereas w/o PT shows larger fluctuations, especially under the stricter threshold of 0.15 m. The box plot on the right summarizes the final-stage evaluation results: the lower and upper whiskers correspond to the 10% and 90% quantiles, respectively, and the solid line inside each box indicates the median. Ours achieves a higher median recovery success rate and requires fewer recovery steps on average than w/o PT, suggesting stronger robustness and more efficient recovery. 

Table 3: Ablation study of our proposed sampling strategy. Bold means better. 

|**Method**|**MPJPE**_↓_|**MPJVE**_↓_|∆**acc**_↓_|
|---|---|---|---|
|w/o AdpS|120.7|548.5|14.50|
|Ours|**119.4**|**541.5**|**14.42**|


To address **Q3** , we perform an ablation study on the effect of the adaptive PT and tracking errordriven sampling strategy (AdpS) by comparing the full Stubborn with a variant without this module (w/o AdpS), while keeping all other settings unchanged. As shown in Table 3, introducing AdpS reduces MPJPE, MPJVE, and ∆acc from 120.7, 548.5, and 14.50 to 119.4, 541.5, and 14.42, respectively, indicating improved tracking performance in terms of joint position, joint velocity, and acceleration. Figure 3 further illustrates the error trends during training. AdpS maintains lower joint position and velocity errors overall in the middle and late stages, while the acceleration error remains similar to that of w/o AdpS. The box plot on the right summarizes the error distribution in the final training stage, with the solid line within each box indicating the median. These results suggest that tracking-error-based adaptive sampling improves the overall tracking performance of long-horizon, highly dynamic motions by increasing the training frequency for difficult segments. 

7 


Figure 3: Ablation results of the AdpS sampling strategy. The results suggest that AdpS improves motion-tracking performance in the later training stages. 

### **4.4 Real-World Deployment** 

To address **Q4** , we evaluate the real-world deployment viability of Stubborn on the physical 29-DoF Unitree G1 humanoid platform, as shown in Figure 4. The real-robot experiments include motions from LAFAN1 [37] and AMASS [38], and demonstrate the robot’s motion tracking, disturbance robustness, and fall recovery performance in physical environments. 


Figure 4: Experimental results. Stubborn can recover from falls and precisely tracks diverse dynamic motions, including flips and acrobatic maneuvers. 

## **5 Conclusion** 

This paper presents Stubborn, a streamlined and unified RL framework that enables the learning of one policy for robust motion tracking and fall recovery for humanoids. By adopting a yaw-aligned tracking representation, we have proposed a PT mechanism, together with a PT and tracking errordriven sampling strategy. The proposed method improves tracking robustness and enables recovery from both unstable and fallen states under strong perturbations. Experimental results in simulation and on the Unitree G1 humanoid robot demonstrate that Stubborn offers effective disturbance re- 

8 

covery, fall recovery, and competitive motion tracking performance under challenging conditions, in comparison with STOA methods. Future work will focus on improving the agility and smoothness of recovery motions after severe falls, as well as extending the framework to more challenging terrains and highly dynamic humanoid behaviors. 

## **References** 

- [1] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4): 1–20, 2021. 

- [2] Z. Luo, J. Cao, A. Winkler, K. Kitani, and W. Xu. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [3] Z. Sun, Y. Peng, Y. Meng, X. Li, B.-S. Huang, Z. Bing, X. Wang, and A. Knoll. Robotdancing: Residual-action reinforcement learning enables robust long-horizon humanoid motion tracking. _arXiv:2509.20717_ , 2025. 

- [4] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _arXiv:2506.12851_ , 2025. 

- [5] J. Han, W. Xie, J. Zheng, J. Shi, W. Zhang, T. Xiao, and C. Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv:2509.16638_ , 2025. 

- [6] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [7] T. Zhu, G. Cai, Z. Yang, G. Ren, H. Xie, Z. Wang, J. Wu, J. Wang, X. Yang, Y. Mu, and Y. Yan. Clot: Closed-loop global motion tracking for whole-body humanoid teleoperation. _arXiv:2602.15060_ , 2026. 

- [8] J. Cheng, D. Kang, G. Fadini, G. Shi, and S. Coros. Rambo: Rl-augmented model-based whole-body control for loco-manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [9] H. J. Lee, S. H. Jeon, and S. Kim. Learning humanoid arm motion via centroidal momentum regularized multi-agent reinforcement learning. _IEEE Robotics and Automation Letters_ , 2025. 

- [10] K. Yin, W. Zeng, K. Fan, M. Dai, Z. Wang, Q. Zhang, Z. Tian, J. Wang, J. Pang, and W. Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv:2507.07356_ , 2025. 

- [11] F. Wu, X. Nal, J. Jang, W. Zhu, Z. Gu, A. Wu, and Y. Zhao. Learn to teach: Sample-efficient privileged learning for humanoid locomotion over real-world uneven terrain. _IEEE Robotics and Automation Letters_ , 2025. 

- [12] H. Jung, Z. Gu, Y. Zhao, H.-W. Park, and S. Ha. Ppf: Pre-training and preservative finetuning of humanoid locomotion via model-assumption-based regularization. _IEEE Robotics and Automation Letters_ , 2025. 

- [13] Q. Liao, T. E. Truong, X. Huang, Y. Gao, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv:2508.08241_ , 2025. 

- [14] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv:2506.14770_ , 2025. 

9 

- [15] A. Duburcq, F. Schramm, G. Bo´eris, N. Bredeche, and Y. Chevaleyre. Reactive stepping for humanoid robots using reinforcement learning: Application to standing push recovery on the exoskeleton atalante. In _2022 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 9302–9309. IEEE, 2022. 

- [16] L. Yang, B. Werner, A. B. Ghansah, and A. D. Ames. Bracing for impact: Robust humanoid push recovery and locomotion with reduced order models. In _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pages 728–735. IEEE, 2025. 

- [17] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [18] M. Chen, K. Wang, B. Zhang, Y. Ren, Z. Zhu, X. Ma, Q. Huang, Z. Yang, Y. Wang, and Z. Su. Holomotion: A foundation model for whole-body humanoid control, 2026. URL `https://github.com/HorizonRobotics/HoloMotion` . 

- [19] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, et al. Track any motions under any disturbances. _arXiv:2509.13833_ , 2025. 

- [20] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati, et al. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. _arXiv:2511.04131_ , 2025. 

- [21] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv:2406.10454_ , 2024. 

- [22] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv:2406.08858_ , 2024. 

- [23] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid wholebody skills. _arXiv:2502.01143_ , 2025. 

- [24] F. Liu, Z. Gu, Y. Cai, Z. Zhou, H. Jung, J. Jang, S. Zhao, S. Ha, Y. Chen, D. Xu, et al. Opt2skill: Imitating dynamically-feasible whole-body trajectories for versatile humanoid locomanipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [25] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots. _arXiv:2402.16796_ , 2024. 

- [26] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv:2412.13196_ , 2024. 

- [27] Y. Ze, Z. Chen, J. P. Ara´ujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu. Twist: Teleoperated whole-body imitation system. _arXiv:2505.02833_ , 2025. 

- [28] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv:2511.02832_ , 2025. 

- [29] Y. Li, Y. Lin, J. Cui, T. Liu, W. Liang, Y. Zhu, and S. Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. In _9th Annual Conference on Robot Learning_ , 2025. 

- [30] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv:2511.07820_ , 2025. 

10 

- [31] P. Chen, Y. Wang, C. Luo, W. Cai, and M. Zhao. Hifar: Multi-stage curriculum learning for high-dynamics humanoid fall recovery. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2908–2915. IEEE, 2025. 

- [32] C. Gaspard, M. Duclusaud, G. Passault, M. Daniel, and O. Ly. Frasa: An end-to-end reinforcement learning agent for fall recovery and stand up of humanoid robots. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15994–16000. IEEE, 2025. 

- [33] T. Egle, Y. Yan, D. Lee, and C. Ott. Enhancing model-based step adaptation for push recovery through reinforcement learning of step timing and region. In _2024 IEEE-RAS 23rd International Conference on Humanoid Robots (Humanoids)_ , pages 165–172. IEEE, 2024. 

- [34] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang. Learning humanoid standing-up control across diverse postures. _arXiv:2502.08378_ , 2025. 

- [35] X. He, R. Dong, Z. Chen, and S. Gupta. Learning getting-up policies for real-world humanoid robots. _arXiv:2502.12152_ , 2025. 

- [36] T. Zhang, B. Zheng, R. Nai, Y. Hu, Y.-J. Wang, G. Chen, F. Lin, J. Li, C. Hong, K. Sreenath, et al. Hub: Learning extreme humanoid balance. _arXiv:2505.07294_ , 2025. 

- [37] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [38] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [39] Y. Wang, S. Zhu, P. Zhi, Y. Li, J. Li, Y.-L. Li, Y. Xiao, X. Wang, B. Jia, and S. Huang. Omnixtreme: Breaking the generality barrier in high-dynamic humanoid control. _arXiv:2602.23843_ , 2026. 

## **6 Appendix** 

### **6.1 Drift-Invariant Yaw-Aligned Tracking Representation** 

To decouple global drift from the desired motion style, similar to [8, 9], our framework adopts a yaw-invariant tracking representation based on a yaw-angle-aligned root coordinate system. Let _W_ denote the world frame and _B_ the robot base frame. The global pose of the robot base remains defined in the world frame, where _TB_<sup>_W_</sup> _∈ SE_ (3) consists of the rotation _RB_<sup>_W∈SO_(3)andthe</sup> position _p_<sup>_W_</sup> _B_<sup>_∈_R3.Using the Z-Y-X Euler-angle convention,</sup><sup>_R_</sup> _B_<sup>_W_is decomposed into the product</sup> of the yaw angle _ψ_ , pitch angle _θ_ , and roll angle _ϕ_ as _RB_<sup>_W_=</sup><sup>_RZ_(</sup><sup>_ψ_)</sup><sup>_RY_(</sup><sup>_θ_)</sup><sup>_RX_(</sup><sup>_ϕ_)</sup><sup>_._Accordingly, we</sup> define the yaw-aligned frame Ψ, whose homogeneous transformation with respect to _W_ is given by _T_ Ψ<sup>_W_=</sup> � _R_ 0 _Z_ 1 _×_ ( _ψ_ 3 ) _p_ 1<sup>_W_</sup> _B_ � _._ For any rigid body _i ∈B_ , with world-frame pose ( _Ri_<sup>_W, pW_</sup> _i_<sup>), its pose in Ψ</sup> is obtained via 


The corresponding local position _p_ ˜ _i_ and orientation _R_<sup>˜</sup> _i_ in the aligned frame are then _p_ ˜ _i_ = _RZ_<sup>_T_(</sup><sup>_ψ_)(</sup><sup>_p_</sup> _i_<sup>_W−pW_</sup> _B_<sup>)</sup><sup>_,_</sup> _R_ ˜ _i_ = _RZ_<sup>_T_(</sup><sup>_ψ_)</sup><sup>_R_</sup> _i_<sup>_W._This representation reduces sensitivity to global drift while</sup> preserving key physical cues for motion control. The relative displacement term ( _p_<sup>_W_</sup> _i − p_<sup>_W_</sup> _B_<sup>)re-</sup> moves global translation, while the inverse yaw rotation _RZ_<sup>_⊤_(</sup><sup>_ψ_) removes the global heading compo-</sup> nent from the body pose representation. Therefore, the resulting tracking errors mainly reflect local whole-body coordination rather than global translation or yaw drift, reducing unnecessary global correction under strong perturbations. The yaw-aligned transformation is applied to the body tracking representation, while the root pose remains defined in the world frame, enabling the policy to reduce sensitivity to global drift while preserving gravity-related pitch and roll information. 

11 

### **6.2 The Overall Algorithm Pipeline and Training Details of Stubborn** 

### **Algorithm 1:** The Overall Algorithm Pipeline of Stubborn 

**Input :** _Tref ∈ SE_ (3)<sup>_N×|B|_</sup> : Reference trajectory _πθ, Vϕ_ : Policy and Value networks _Nenv, Krollout_ : Env count & rollout length _θsuccess, θpos, θquat, pterm_ : Threshold parameters **Output:** _θ, ϕ_ : Optimized network parameters Init _wt ←_ 1 _._ 0 _, ∀t_ ; Sample states _s_<sup>(</sup><sup>_e_)</sup> _∼ pt ∝ wt_ ; **for** _iter_ = 1 _,_ 2 _, . . ._ **do for** _k_ = 1 **to** _K_ **do** _a_<sup>(</sup> _k_<sup>_e_)</sup> _∼ πθ_ ( _·|s_<sup>(</sup> _k_<sup>_e_))</sup><sup>_,s_(</sup> _k_<sup>_e_</sup> +1<sup>)</sup><sup>_←_EnvStep(</sup><sup>_sk, ak_);</sup> `// Drift-Invariant Yaw-Aligned Tracking Representation` _T_ Ψ<sup>_W←_YawAlign(</sup><sup>_T_</sup> _B_<sup>_W_) ;</sup> (˜ _pi, R_<sup>˜</sup> _i_ )<sup>(</sup><sup>_e_)</sup> _←_ ( _T_ Ψ<sup>_W_)</sup><sup>_−_1</sup><sup>_T_</sup> _i_<sup>_W,∀i ∈B_;</sup> _rk_<sup>(</sup><sup>_e_)</sup> _←_ Reward( _{p_ ˜ _i, R_<sup>˜</sup> _i}_ ); `// Bernoulli-based Probabilistic Termination for Fall Recovery Learning` **for** _env e ∈{_ 1 _, . . . , Nenv}_ **do** _ρk ←_ I� _|e_<sup>_p_</sup> _root,z_<sup>_|>θpos ∨e_</sup> _root_<sup>_q>θquat_</sup> �; _τk ∼_ Bernoulli( _ρk · pterm_ ); **if** _T ≥ T_ max _∨ τk_ == 1 **then** `// Probabilistic Termination and Tracking Error-driven Sampling` _e_ ¯ _←_ MeanErr( _t_<sup>(</sup> 0<sup>_e_)</sup><sup>_, T_);</sup> **for** _t ∈_ [ _t_<sup>(</sup> 0<sup>_e_)</sup><sup>_, t_</sup> 0<sup>(</sup><sup>_e_)</sup> + _T −_ 1] **do if** ¯ _e ≥ θsuccess_ **then** ∆ _wt ←_ +∆ _wi_ ; **else if** _T ≥ T_ max **then** ∆ _wt ←_ Φ _att_ ( _t_ ); **else** ∆ _wt ←_ Φ _dist_ ( _t_ ); _wt ←_ max(min( _wt_ +∆ _wt, wmax_ ) _, wmin_ ); _pt ← wt/_<sup>�</sup> _wj, t_<sup>(</sup> 0<sup>_e_)</sup> _∼_ Cat( _pt_ ); Reset _s_<sup>(</sup><sup>_e_)</sup> to ref. pose _t_<sup>(</sup> 0<sup>_e_)</sup> + perturbs; 

`// Policy Optimization` Estimate GAE _A_<sup>ˆ</sup> using _{s, a, r}_ 1:<sup>(1:</sup> _K_<sup>_Nenv_)</sup> ; _θ, ϕ ←_ arg max _θ,ϕ_ E� _Lclip − cvLV F_ �; **return** _θ, ϕ_ ; 

Table 4: Reward terms for motion tracking. 

|**Term**|**Formulation**|**Weight**|
|---|---|---|
|Joint Position|exp<br>�<br>_−∥p_j_∥_<sup>2</sup>_/_0_._1<br>�<br><br>|1.00|
|Joint Velocity|exp<br>�<br>_−∥v_j_∥_<sup>2</sup>_/_5<br>�<br><br>|0.50|
|Body Linear Velocity|exp<br>�<br>_−∥v_b_∥_<sup>2</sup>_/_0_._5<sup>2�</sup><br><br><br>|0.50|
|Body Angular Velocity|exp<br>�<br>_−∥ω_b_∥_<sup>2</sup>_/_0_._5<br>�<br><br>|0.50|
|Relative Body Position|exp<br>�<br>_−∥p_rel_∥_<sup>2</sup>_/_0_._1<sup>2�</sup><br>|1.00|
|Action Rate|_∥at −at−_1_∥_<sup>2</sup><br>|_−_0_._01|
|Undesired Contacts|�I(_Fc >_1_._0)|_−_1_._00|


Table 5: Domain Randomization parameters. 

|**Category**|**Parameter**|**Type**|**Range**|
|---|---|---|---|
|Env.|Static Friction<br>Dynamic Friction|Uniform<br>Uniform|[0.6, 1.0]<br>[0.4, 0.8]|
|Delays|Action Delay|Uniform|[0.0, 0.02] s|
|Motor|Kp/Kd Factor|Scaling|[0.8, 1.2]|
||Joint Armature|Scaling|[0.8, 1.2]|
||Link Mass|Scaling|[0.8, 1.2]|
|Body|Base Mass|Additive|[-5.0, 5.0]|
||Base CoM|Additive|[-0.05, 0.05] m|


12 

