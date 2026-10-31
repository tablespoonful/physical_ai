---
title: "General Humanoid Whole-Body Control via Pretraining and Fast Adaptation"
date: "2026-02-12"
authors: "Zepeng Wang; Jiangxing Wang; Shiqing Yao; Yu Zhang; Ziluo Ding; Ming Yang"
url: https://arxiv.org/abs/2602.11929
pdf: https://arxiv.org/pdf/2602.11929
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11929)** / [論文ページ](https://arxiv.org/abs/2602.11929)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

<u>∝</u> BeingBeyond 

# **General Humanoid Whole-Body Control via Pretraining and Fast Adaptation** 

**Zepeng Wang**<sup>1</sup><sup>_,_2</sup> **Jiangxing Wang**<sup>2</sup> **Shiqing Yao**<sup>2</sup> **Yu Zhang**<sup>2</sup> **Ziluo Ding**<sup>2</sup> **Ming Yang**<sup>2</sup><sup>_,_3</sup> **Yuxuan Wang**<sup>2</sup><sup>_,_3</sup> **Haobin Jiang**<sup>2</sup><sup>_,_3</sup> **Chao Ma**<sup>1</sup> **Xiaochuan Shi**<sup>1</sup><sup>_,†_</sup> **Zongqing Lu**<sup>2</sup><sup>_,_3</sup><sup>_,‡_</sup> 1Wuhan University 2BeingBeyond 3Peking University 

```
https://research.beingbeyond.com/fast
```


Figure 1: **FAST** is a **general** and **fast-adaptation** framework for humanoid whole-body control. It enables zero-shot high-dynamic motion tracking and real-time teleoperation with strong robustness and balance beyond simulation. For low-quality or out-of-distribution motion references, FAST further supports lightweight residual adaptation for rapid and stable specialization. 

## **Abstract** 

Learning a general whole-body controller for humanoid robots remains challenging due to the diversity of motion distributions, the difficulty of fast adaptation, and the need for robust balance in high-dynamic scenarios. Existing approaches often require task-specific training or suffer from performance degradation when adapting to new motions. In this paper, we present **FAST** , a general humanoid whole-body control framework that enables <u>Fast Adaptation</u> and <u>Stable</u> Motion <u>Tracking.</u> FAST introduces Parseval-Guided Residual Policy Adaptation, which learns a lightweight delta action policy under orthogonality and KL constraints, enabling efficient adaptation to out-of-distribution motions while mitigating catastrophic forgetting. To further improve physical robustness, we propose Center-of-Mass-Aware Control, which incorporates CoM-related observations and objectives to enhance balance when tracking challenging reference motions. Extensive experiments in simulation and real-world deployment demonstrate that FAST consistently outperforms state-of-the-art baselines in robustness, adaptation efficiency, and generalization. 

**Date:** February 12, 2026 

## **1 Introduction** 

In robotics, achieving <u>general</u> whole-body control (WBC) is a critical step toward advancing humanoid intelligence. Rather than mastering isolated skills [1, 2], general WBC aims to extend the boundary of controllable motions and coordination patterns, enabling a single controller to execute diverse whole-body behaviors [3]. Such capability is essential for deploying humanoid robots in realistic settings, including teleoperation for both hazardous operations and large-scale data collection in real-world settings [4], reliable execution of complex whole-body motions [5], and serving as the low-level motor foundation for embodied intelligence systems [6]. 

Despite recent progress in learning-based whole-body control, existing methods remain far from achieving truly <u>general</u> motion tracking. Most approaches are trained on curated motion datasets such as AMASS [7], OMOMO [8], and LaFan1 [9], which are collected under controlled settings and exhibit relatively clean and consistent kinematics. In contrast, real-world motion references often originate from heterogeneous sources, including offline motion capture, real-time teleoperation, text-to-motion generation, and monocular video-based estimation. These sources vary substantially in motion quality, noise, temporal consistency, and physical plausibility, inducing significant distribution shifts [10]. 

Under such shifts, existing controllers frequently struggle to robustly track motions that deviate from the training distribution. This issue is particularly pronounced for highly dynamic or stylistically complex motions [11, 12], where limited policy expressiveness and stability constraints lead to tracking failures even for motions nominally similar to training data. Such motions effectively act as outliers that are difficult to cover with finite datasets [13]. These limitations motivate the need for whole-body controllers that combine strong zero-shot robustness with the ability to rapidly adapt to novel and low-quality motion inputs. 

A direct solution is to scale up motion datasets, model capacity, and computational resources to cover a broader range of motions and embodiments [3, 14]. In theory, large-scale pretraining can improve generalization. In practice, however, this paradigm is constrained by real-world control requirements. Whole-body control 

> †Correspondence to Xiaochuan Shi _<_ shixiaochuan@whu.edu.cn _>_ . 

> ‡Project led by Zongqing Lu _<_ lu@beingbeyond.com _>_ . 

2 

demands low-latency, high-frequency inference to maintain closed-loop stability [6]. Humanoid robots typically operate under limited onboard compute and power budgets, making large-scale models difficult to deploy at control frequencies [15]. Moreover, increased model size introduces additional inference latency, which can directly degrade balance and stability. Under these constraints, a more practical direction is fast adaptation. Rather than relying solely on exhaustive pretraining, policies should rapidly specialize to new motion distributions through efficient fine-tuning or lightweight adaptation, complementing large-scale training while satisfying deployment and control constraints. 

To address robust humanoid whole-body control under distribution shifts, we propose **FAST** , a general framework that combines a pretrained Center-of-Mass-Aware controller with lightweight residual learning for fast adaptation to unseen and out-of-distribution motions. This design preserves robust zero-shot performance while maintaining physical stability under relatively low-quality reference motions. 

Our main contributions are summarized as follows: 

- We propose **FAST** , a general and fast-adaptation framework for humanoid whole-body control that enables efficient adaptation to out-of-distribution motions while maintaining strong zero-shot robustness. 

- We introduce **Center-of-Mass-Aware Control** , which explicitly incorporates CoM-related observations and objectives to improve balance and stability when tracking challenging or physically inconsistent motion references. 

- We demonstrate that FAST supports a wide range of whole-body control scenarios, including zero-shot high-dynamic motion tracking, fast adaptation to relatively low quality motions from text and video, and real-time whole-body teleoperation, with consistent gains in robustness and generalization in both simulation and real-world experiments. 

## **2 Related Work** 

### **2.1 Learning-based Humanoid Whole-Body Control** 

Learning-based approaches have achieved significant progress in humanoid whole-body control, enabling a wide range of skills such as locomotion [16, 17], agile motions [2], and recovery behaviors [18]. However, most methods typically rely on task-specific reward design, which limits scalability and generality. In contrast, whole-body motion tracking leverages retargeted human motion as reference trajectories through kinematic retargeting, eliminating manual reward engineering while promoting coordinated and more generalizable humanoid control. 

For learning diverse humanoid motions within a general policy, prior work has explored improvements along several complementary directions [19–21]. Architectural approaches improve scalability by decoupling upperand lower-body control [22] or adopting expert-based paradigms to reduce cross-motion interference [23]. Data-centric methods emphasize curated large-scale datasets [24] or augment training with extreme balance recovery to enhance robustness [11]. From the perspective of tracking objectives, GMT [13] prioritizes local pose and velocity consistency for stable long-horizon tracking, while KungfuBot2 [12] enforces consistency via local style and global stability constraints. More recently, SONIC [3] demonstrates that scaling model capacity and data volume enables foundation-style policies to generalize across broad motion distributions. 

In contrast, FAST emphasizes fast and stable adaptation under distribution shift, rather than scaling model size or retraining task-specific policies, enabling robust whole-body control for high-dynamic and out-of-distribution motions. 

### **2.2 Fast Adaptation for Humanoid Control** 

Fast adaptation in humanoid control has been widely studied to bridge distribution gaps between reference motions and physical execution. A common paradigm is residual reinforcement learning, where a posttrained residual policy compensates for mismatches between kinematic references and robot dynamics [25]. Representative methods such as ResMimic [26] and ASAP [1] apply residual learning to refine motion tracking 

3 


Figure 2: **An overview of FAST.** Our framework consists of three stages. (1) We construct a curated humanoid motion dataset via human-to-humanoid retargeting with auxiliary physical signals. (2) We train a general whole-body controller with a Mixture-of-Experts architecture and Center-of-Mass-Aware control. (3) We perform fast adaptation via Parseval-guided residual policy learning. 

under physical constraints. However, these approaches mainly target sim-to-real dynamics correction and are not designed for rapid adaptation to novel or long-tailed motion distributions. 

Another line of work improves adaptation efficiency by leveraging pre-trained priors or skill representations [27, 28]. Hierarchical frameworks such as SPiRL [29] constrain downstream policy updates via KL regularization to remain close to learned skill priors, while large-scale pre-training approaches like Octo [30] demonstrate that fine-tuning pre-trained models significantly outperforms training from scratch. Nevertheless, these methods rely on the transferability and expressiveness of the learned priors, which can limit adaptation when target motions deviate substantially from pre-training distributions. 

To address highly diverse and challenging motion datasets, more targeted adaptation mechanisms have been proposed. PHC [31] incrementally extends policy capacity by adding new motion-specific modules while freezing existing ones to mitigate forgetting. UniTracker [32] adopts a lightweight residual decoder on top of a frozen universal policy to capture extreme out-of-distribution motions efficiently. 

Distinct from these directions, FAST combines residual adaptation with explicit stability regularization, enabling fast adaptation to novel motion distributions while preserving robustness and prior tracking capabilities. 

## **3 Method** 

We present a unified framework, FAST, for general humanoid whole-body control that combines large-scale motion pretraining with stable and efficient policy adaptation, as illustrated in Figure 2. A motion tracking policy is trained to follow diverse reference motions while explicitly regulating balance and stability through Center-of-Mass–Aware objectives and observations. To enable fast specialization to new motion distributions, we introduce a residual adaptation scheme with Parseval regularization and KL-constrained updates, allowing efficient adaptation without degrading previously learned behaviors. 

### **3.1 Motion Dataset Curation** 

**Human-to-Humanoid Retargeting** . We construct a large-scale humanoid motion dataset by retargeting publicly available human motion capture datasets, including AMASS [7] and OMOMO [8], represented in the SMPL format. Additionally, we also collect a small in-house dataset using our own MoCap system. The retargeting and PHC-filtering process follows the previous work [23]. These datasets are used mainly for the 

4 

large-scale pretraining of the general whole-body controller. To evaluate fast adaptation and cross-distribution generalization, we additionally incorporate in-house motion data collected via Inertial Motion Capture, together with LaFan1 [9] and MotionX [33], which contain more dynamic and device-specific motion patterns. 

**Data Augmentation for Motion Diversity** . To enhance motion diversity and robustness to distribution shifts, we augment retargeted humanoid motions by adjusting global translational velocity and perturbing lower-limb joint configurations. This produces a broader range of motion speeds and kinematic variations while preserving physically coherent dynamics. More details are in Appendix C.2. 

**Auxiliary Physical Signals** . In addition to kinematic data, we augment each motion with contact masks derived from foot–ground interactions, and include the center of mass (CoM) and center of pressure (CoP) computed following prior work [2]. These physically grounded signals provide explicit balance and support cues, enabling more stable and physically plausible motion tracking. 

### **3.2 General Whole-Body Controller** 

A general motion tracking policy is trained on the motion dataset via Reinforcement Learning. At each timestep, the policy observation contains the proprioceptive information. In addition, the observation also includes command information from the reference motion at that timestep, consisting of both joint angles and selected keypoint positions, as well as the corresponding velocities. The policy is trained using Proximal Policy Optimization (PPO) [34] and outputs actions as whole-body target joint positions for joint-level proportional-derivative (PD) controllers. More details about the observation design of our framework are provided in the Appendix A.1. 

**Policy Architecture** . Following prior work [13, 23], we adopt a mixture-of-experts (MoE) policy architecture to handle diverse motion dynamics. The policy consists of multiple expert networks, each implemented as a three-layer MLP, and a gating network that outputs state-dependent mixture weights. At each timestep, the final action is a weighted sum of the expert outputs. 

This design is motivated by the fact that different motions exhibit distinct dynamic properties. Training a single policy on highly diverse motions often leads to mutual interference during learning. The MoE structure allows different experts to specialize in different motion dynamics, while the gating network learns to combine them based on the current state and reference command. 

**Center-of-Mass-Aware Control** . In the general whole-body control, especially for teleoperation, prior methods [2] rely on curated training pipelines that filter out aggressive or unstable motions, while in real-world deployment, the policy inevitably encounters aggressive and unseen references that cannot be filtered in advance. Instead of enforcing strict tracking, we explicitly design the policy to conservatively follow such motions to ensure safe execution. 

Concretely, we augment the observation with reference Center-of-Mass (CoM) and Center-of-Pressure (CoP) signals, and guide conservative behavior through two reward mechanisms. First, when the reference CoM–CoP distance exceeds a threshold, all tracking-related reward coefficients are progressively down-weighted, allowing the policy to relax tracking under aggressive references. Second, we introduce an explicit stability reward that encourages minimizing the distance between the humanoid’s actual CoM and CoP, promoting balance maintenance (See A.2 for details). These CoM-aware designs enable a dynamic trade-off between tracking accuracy and physical stability, improving robustness under challenging motions. 

### **3.3 Parseval-Guided Residual Policy Adaptation** 

**Delta Policy Parameterization** . To enable efficient adaptation to new motion distributions while preserving the generality of the pretrained controller, we adopt a residual policy on top of a fixed base model. The base policy _πb_ is a pretrained whole-body controller introduced earlier, for which direct end-to-end fine-tuning is computationally expensive and often inefficient in the low-data adaptation setting. 

We therefore introduce a lightweight residual policy _πr_ , implemented as a three-layer MLP, which predicts additive action corrections conditioned on the same observations as _πb_ . During adaptation, the base policy is 

5 

fully frozen and only the residual policy is optimized, while the critic is initialized from the pretrained model and further fine-tuned. The final action is given by _at_ = _a_<sup>_b_</sup> _t_<sup>+</sup><sup>_ar_</sup> _t_<sup>.</sup> 

**Parseval Regularization for Stable Adaptation** . While the residual policy reduces the parameter space for adaptation, unconstrained fine-tuning can still be unstable and prone to suboptimal convergence when adapting to new motion distributions that differ substantially from the pretraining domain. To address these challenges, we incorporate Parseval regularization, which both **_stabilizes optimization and encourages the network to learn diverse, approximately orthogonal feature directions_** . This allows the residual policy to explore beyond the base policy’s original behavior, facilitating escape from local optima in the new domain. 

Specifically, we apply Parseval regularization [35] to all linear layers of the residual policy except the final output layer. For a weight matrix _W ∈_ R<sup>_m×n_</sup> , the regularization term is defined as 


where _s >_ 0 is a scaling factor, _I_ denotes the identity matrix of appropriate dimension, and _∥· ∥F_ is the Frobenius norm. This regularizer encourages the columns of _W_ to be approximately orthonormal, thereby implicitly constraining the layer’s spectral norm and limiting extreme scaling along any single feature direction. As a result, it promotes smoother gradient propagation and better-conditioned feature representations, enabling both stable training and effective exploration of new feature directions during adaptation. 

The residual policy is trained with the combined objective 


where _L_ RL is the standard reinforcement learning loss, _Wl_ are the weight matrices of all layers except the last, and _λp >_ 0 controls the regularization strength. Empirically, Parseval-regularized residual adaptation leads to more stable optimization and improved sample-efficient learning across new motion distributions, successfully escaping local optima that unconstrained updates may get trapped in. 

**KL-Constrained Policy Update** . While residual parameterization and Parseval regularization constrain adaptation in parameter and representation spaces, they do not by themselves prevent the adapted model from deviating excessively from the pretrained model. This is particularly important in our setting, where adaptation is performed after pretraining and relies only on newly encountered motions, without revisiting the source-domain dataset. As a result, the residual policy receives no supervision on previously learned motions, making explicit constraints on policy drift essential. To mitigate catastrophic drift and preserve general motion tracking capabilities, we introduce a KL-divergence constraint that anchors the adapted model to the base model. 

Specifically, we regularize the combined policy _π_ , defined by _at_ = _a_<sup>_b_</sup> _t_<sup>+</sup><sup>_ar_</sup> _t_<sup>,toremainclosetothebasepolicy</sup> _πb_ in terms of action distributions: 


where _D_ is the state distribution induced by the adapted policy. The KL constraint encourages small, task-specific corrections by implicitly limiting residual action magnitude. As a result, the combined model remains close to the base policy’s output, allowing the residual policy to generalize to states from the original distribution even though it is trained solely on new motion data. Empirically, KL-constrained adaptation preserves performance across both original and new motion distributions. 

The KL term is incorporated into the overall objective as a soft constraint: 


where _λk_ controls the strength of the KL constraint. 

6 

**Stability Analysis of Residual Policy Adaptation** . To support the stability and effectiveness of the proposed fast adaptation framework, we provide a theoretical analysis of the residual policy adaptation scheme. In particular, we show that Parseval regularization and KL-constrained updates provide complementary constraints on the residual policy: Parseval regularization bounds its functional sensitivity via Lipschitz continuity, while the KL constraint limits its deviation from the base policy. Together, they ensure smooth and stable fast adaptation under limited data. 

**Proposition 3.1.** _Consider a residual policy πr_ : R<sup>_d_</sup> _→_ R<sup>_m_</sup> _parameterized by an L-layer feed-forward MLP with 1-Lipschitz activation functions ϕ_ ( _·_ ) _. Suppose Parseval regularization is applied such that for each layer l_ = 1 _, . . . , L −_ 1 _, the weight matrix satisfies ∥Wl_<sup>_⊤Wl −sI∥_2</sup><sup>_≤εl,wheres >_0</sup><sup>_isascalingfactorandεl≥_0</sup> _denotes the approximation error. Then the residual policy πr is Lipschitz continuous, with Lipschitz constant bounded as_ Lip( _πr_ ) _≤_<sup>�</sup><sup>_L_</sup> _l_ =1<sup>_−_1</sup> _~~√~~_ _<u>s</u>_ <u>+</u> _<u>εl</u> ∥WL∥_ 2 _._ 

**Proposition 3.2.** _Let the adapted policy be defined as π_ ( _·|s_ ) = _N_ ( _µb_ ( _s_ ) + _µr_ ( _s_ ) _,_ Σ) _, where µb_ ( _s_ ) _is the mean of the base policy ,µr_ ( _s_ ) _is the residual mean, and_ Σ _is a state-independent covariance matrix shared by both policies. If the KL divergence satisfies DKL_ ( _π_ ( _·|s_ ) _∥πb_ ( _·|s_ )) _≤ ϵ, ∀s, then the residual policy output is bounded as ∥µr_ ( _s_ ) _∥_ 2 _≤_ ~~�~~ 2 _ϵλmax_ (Σ) _, where λ_ max(Σ) _denotes the largest eigenvalue of the covariance matrix._ 

_Proof._ Full proof details of Proposition 3.1 and Proposition 3.2 are provided in Appendix B. 

Taken together, Proposition 3.1 and Proposition 3.2 provide complementary guarantees for residual policy adaptation. Parseval regularization bounds the sensitivity of the residual policy with respect to state perturbations (functional smoothness). KL constraint bounds the magnitude of the residual policy relative to the base policy (distributional proximity). 

As a result, the adapted policy remains **_locally smooth_** and **_statistically stable_** , enabling efficient adaptation to out-of-distribution motions while preserving prior knowledge. 

## **4 Experiments** 

In the experimental section, we aim to answer the following key research questions: 

- **Q1** : How does FAST compare with state-of-the-art humanoid whole-body controllers? 

- **Q2** : Can FAST adapt efficiently to new motion distributions while retaining prior capabilities? 

- **Q3** : Does CoM-Aware Control improve balance and stability in high-dynamic motions? 

- **Q4** : How effectively does FAST transfer to real-world whole-body control from diverse motion sources? 

### **4.1 Experiment Setup** 

**Baselines** . To evaluate the effectiveness of our approach, we compare against two state-of-the-art universal humanoid motion tracker, GMT [13] and TWIST2 [4]. We employ the officially released models for both baselines and conduct all evaluations in the MuJoCo simulator, which is supported by all methods. 

**Metrics** . We use a set of metrics [23, 36] to comprehensively evaluate the performance of motion tracking. (1) **Success Rate** ( _Succ_ , %): in all experiments, a task is considered a failure when the root height of the humanoid deviates from the reference motion by more than 0.25 m. Additionally, for the objectives of different experiments, we design and apply stricter task failure conditions to better reflect the specific requirements of each task (see Appendix D.1). (2) **Global Mean Per Keypoint Position Error** ( _E_ mpkpe, _m_ ) measures global keypoint position tracking accuracy. (3) **Mean Per Joint Position Error** ( _E_ mpjpe, _rad_ ) measures local joint position tracking performance. (4) **Global Mean Root Linear Velocity Error** ( _E_ vel, _m_ ) measures global root linear velocity tracking accuracy. To evaluate the policy’s performance on high-dynamic balance motions, we further include (5) **Slippage** ( _Slip_ , _m/s_ ), measuring the velocity of the support foot relative to the ground, with higher values indicating greater instability, and (6) **Mean Center-of-Mass and Center-of-Pressure Distance** ( _E_ mpd, _m_ ), which measures the absolute difference between the robot’s CoM and CoP, reflecting the current balance state of the humanoid. 

7 

### **4.2 Comparison with Existing Methods** 

To address **Q1** , Table 1 compares our base model with GMT and TWIST2 on both the training dataset (AMASS) and an out-of-distribution (OOD) dataset (a leg-dominant subset of MotionX [33]). 

Table 1: Main results on training dataset (AMASS) and test dataset (MotionX). Results are reported as mean _±_ one standard deviation. 

|||**AMASS (**|**training dat**|**aset)**||**MotionX **|**(test datase**|**t)**|
|---|---|---|---|---|---|---|---|---|
|**Method**|_Succ ↑_|_E_mpjpe _↓_|_E_mpkpe _↓_|_E_vel _↓_|_Succ ↑_|_E_mpjpe _↓_|_E_mpkpe _↓_|_E_vel _↓_|
|GMT|77.55|0.100_±_0.020|0.319_±_0.257|0.226_±_0.162|38.91|0.124_±_0.033|0.232_±_0.173|**0.273**_±_0.157|
|TWIST2|72.61|**0.084**_±_0.022|0.388_±_0.258|0.269_±_0.163|31.82|**0.102**_±_0.031|0.229_±_0.182|0.311_±_0.191|
|**FAST (ours)**|**87.14**|0.132_±_0.040|**0.123**_±_0.079|**0.206**_±_0.157|**51.46**|0.143_±_0.035|**0.212**_±_0.136|0.359_±_0.198|


Across both datasets, FAST consistently achieves the highest success rate, highlighting improved long-horizon robustness and generalization. Although not always optimal in local joint-angle errors, FAST substantially improves the tracking accuracy of global keypoints, which is more directly correlated with physically consistent and stable motions. This reflects a trade-off between optimizing local accuracy and maintaining globally coherent, long-horizon behavior. 

On the OOD dataset, baseline methods report lower MPJPE and velocity errors. However, these metrics are computed over significantly shorter successful segments, as frequent early terminations occur during highly dynamic motions. As a result, per-frame error metrics alone can be misleading when evaluating long-horizon tracking performance. 

### **4.3 Evaluation of Fast Adaptation with Performance Preservation** 

To address **Q2** , we evaluate the fast adaptation capability of FAST on two target datasets, LaFan1 and MotionX, while assessing performance preservation on the source training dataset (AMASS). We compare against several adaptation strategies, including a frozen base model, training from scratch, full fine-tuning, and a residual policy without regularization. For a fair comparison, all methods utilize the same training setup and optimization steps. All simulation evaluations are conducted in the IsaacLab simulator. Quantitative results on LaFan1 and MotionX, alongside performance preservation on AMASS, are visualized in Figure 3. 

On the target adaptation datasets, FAST consistently achieves the best overall performance across tracking accuracy and task completion metrics. Compared to training from scratch and full fine-tuning, FAST converges more rapidly and reaches higher success rates, demonstrating its effectiveness for fast adaptation to new motion distributions. Although the unregularized residual model also improves target-domain performance, it consistently underperforms FAST, indicating that structured regularization plays an important role in guiding stable and effective adaptation. 

Importantly, FAST better preserves performance on the source dataset. As shown in Figure 3, the residual-only model exhibits a clear performance degradation on AMASS, reflecting substantial distribution drift caused by the lack of source-domain constraints. In contrast, FAST significantly alleviates this degradation, achieving the lowest MPJPE and MPKPE among all adapted models while maintaining competitive success rates. Although its success rate is slightly lower than that of the frozen base model and full fine-tuning, FAST provides a more favorable balance between adaptation to new data and robustness on the original distribution. 

### **4.4 Ablation Studies** 

#### **4.4.1 Ablations on CoM-Aware Control** 

To address **Q3** , we evaluate the impact of CoM-Aware Control on a curated set of high-dynamic motions, where maintaining balance is a primary source of failure. Table 2 reports quantitative results on both in-distribution and out-of-distribution (OOD) subsets, while Figure 4 presents representative qualitative examples. 

8 


Figure 3: Fast adaptation on LaFan1 and MotionX (target) with performance retention on AMASS (source). 

Table 2: Quantitative ablation results on CoM-Aware Control for high-dynamic motions. 

||**In-di**|**stribution data**|**set**|**Out-of**|**-distribution d**|**ataset**|
|---|---|---|---|---|---|---|
|**Method**|Stab|ility|Completion|Sta|bility|Completion|
||_E_mpd _↓_|_Slip ↓_|_Succ ↑_|_E_mpd _↓_|_Slip ↓_|_Succ ↑_|
|FAST w.o. CoM|0.171_±_0.075|1.472_±_0.848|84.15|0.122_±_0.052|1.298_±_0.752|79.07|
|**FAST (Ours)**|**0.156**_±_**0.079**|**0.909**_±_**0.483**|**97.56**|**0.110**_±_**0.040**|**0.995**_±_**0.787**|**86.63**|


As shown in Table 2, incorporating explicit CoM awareness consistently improves stability and task completion across both motion distributions. Compared to the variant without CoM-related objectives, the full model achieves lower mean positional deviation ( _E_ mpd) and reduced _Slip_ , indicating more stable contact and improved balance maintenance. 

Figure 4 further illustrates the benefits of CoM-Aware Control in representative high-dynamic scenarios. By explicitly accounting for the CoM, the controller suppresses excessive root drift and mitigates balance loss during large-amplitude motions, enabling successful execution where the baseline fails. 

Overall, these results demonstrate that explicit consideration of CoM-related physical signals significantly enhances balance robustness in high-dynamic motion tracking and improves generalization to unseen motion distributions. 

#### **4.4.2 Ablations on Fast Adaptation** 

We conduct ablation studies by selectively removing Parseval and KL regularization from FAST, resulting in three variants: FAST w.o. Parseval & KL, FAST w.o. KL, and FAST w.o. Parseval. 

As shown in Table 3, on the target adaptation dataset, the FAST consistently achieves the best performance across all metrics. This indicates that Parseval and KL regularization provide complementary benefits for stable and efficient adaptation. Variants using only a single regularization term improve over the unregularized baseline but remain inferior to the full model. 

On the source dataset, FAST and variant with KL regularization consistently achieve higher success rates than 

9 


Figure 4: Visualizations of representative motions comparing CoM-Aware Control with the baseline. (a) Forward bending. (b) High knee lift. (c) High leg lift. (d) Side-to-side swaying gait with turning. CoM-Aware Control consistently maintains balance and reduces instability, while the baseline exhibits drift or falls. 

Table 3: Abaltions on fast adaptation results on target adaptation dataset (LaFan1) and source dataset (AMASS). 

||**La**|**Fan1 (target **|**adaptation **|**dataset)**||**AMASS (**|**source datas**|**et)**|
|---|---|---|---|---|---|---|---|---|
|**Method**|_Succ ↑_|_E_mpjpe _↓_|_E_mpkpe _↓_|_E_vel _↓_|_Succ ↑_|_E_mpjpe _↓_|_E_mpkpe _↓_|_E_vel _↓_|
|FAST w.o. Parseval & KL|86.19|0.113_±_0.055|0.067_±_0.055|0.335_±_0.136|94.67|0.133_±_0.031|0.050_±_0.026|0.314_±_0.130|
|FAST w.o. KL|88.40|0.090_±_0.052|0.062_±_0.045|0.318_±_0.121|96.81|0.099_±_0.027|0.048_±_0.027|0.297_±_0.130|
|FAST w.o. Parseval|87.82|0.091_±_0.055|0.064_±_0.068|0.323_±_0.124|**97.36**|0.101_±_0.029|0.048_±_0.027|**0.295**_±_0.129|
|**FAST (ours)**|**90.60**|**0.084**_±_0.050|**0.058**_±_0.041|**0.317**_±_0.123|96.92|**0.092**_±_0.028|**0.047**_±_0.028|0.306_±_0.137|


those without KL, indicating that KL regularization effectively helps preserve previously learned behaviors by constraining policy deviation from the base model. In particular, the KL-only variant attains the highest success rate, while FAST achieves the second-highest success rate together with the lowest MPJPE and MPKPE, reflecting a favorable balance between preservation and adaptation. 

Overall, these results demonstrate that combining Parseval and KL regularization enables fast adaptation with a favorable balance between target-domain performance and source-domain preservation. 

### **4.5 Real-world Deployment** 

To answer **Q4** , we deploy FAST on a Unitree G1 humanoid robot [37] to evaluate its real-world performance across diverse motion sources and control scenarios, as shown in Figure 1. High-dynamic motion tracking and whole-body teleoperation are performed in a zero-shot manner using the pretrained general policy, demonstrating strong robustness and balance beyond simulation. For more challenging scenarios with lowquality motion references, we further leverage FAST’s lightweight residual adaptation to enable rapid and stable specialization. 

#### **4.5.1 High-dynamic Motion Tracking** 

We first evaluate FAST on high-dynamic single-motion tracking tasks using offline motion capture data. Without adaptation, the robot successfully executes challenging motions such as single-leg squats and side kicks [2], which require precise balance control and rapid weight shifts. FAST maintains stable CoM behavior and accurately follows the reference motions, demonstrating strong zero-shot robustness to high-dynamic motions. 

#### **4.5.2 Teleoperation** 

We further assess FAST in real-time whole-body teleoperation scenarios, where human motions are streamed online as reference trajectories. The robot performs diverse behaviors, including walking, jumping, martial 

10 

arts movements, and object manipulation (e.g., grabbing toys, and moving chairs). Despite the variability and latency inherent in teleoperation, FAST remains responsive and stable, illustrating that the pretrained general policy provides a strong foundation for whole-body teleoperation without additional adaptation. 

#### **4.5.3 Adaptation to Low-Quality Motions** 

While the pretrained base policy demonstrates strong zeroshot robustness, motion references derived from text generation or monocular video estimation often contain significant kinematic noise, temporal inconsistencies, and physical implausibilities that exceed the coverage of the training distribution. To handle such challenging scenarios, we leverage FAST’s residual adaptation mechanism to quickly specialize the base policy to these low quality motion sources. 

We integrate a text-to-motion generation pipeline [38] and a video-to-motion estimation pipeline [39, 40] to produce reference motions. After fast adaptation, the robot robustly tracks synthesized motions, including single-leg jumping, 360degree hopping, and complex dance sequences reconstructed from monocular videos. These results demonstrate that FAST enables efficient and stable adaptation to low-quality motions. 

## **5 Conclusion** 


In this work, we present FAST, a general humanoid wholeFigure 5: Zero-shot generalization to highbody control framework that emphasizes fast adaptation and dynamic motions on a Unitree G1. stable motion tracking. FAST combines Parseval-Guided Residual Policy Adaptation to efficiently specialize a pretrained policy to new motion distributions while constraining policy drift, with Center-of-Mass-Aware Control to enhance stability when tracking high-dynamic or low-quality reference motions. Extensive simulation and real-world experiments demonstrate that FAST consistently outperforms state-of-the-art methods in robustness, adaptability, and generalization across diverse scenarios, including motion capture tracking, textand video-derived motions, and real-time teleoperation. Future work will explore fully online and continual adaptation, as well as more adaptive regularization strategies to further balance stability and flexibility. 

11 

## **References** 

- [1] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. arXiv <u>preprint</u> arXiv:2502.01143, 2025. 

- [2] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. arXiv <u>preprint</u> arXiv:2506.12851, 2025. 

- [3] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. arXiv <u>preprint</u> arXiv:2511.07820, 2025. 

- [4] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. arXiv <u>preprint</u> arXiv:2511.02832, 2025. 

- [5] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. arXiv <u>preprint</u> arXiv:2508.21043, 2025. 

- [6] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. arXiv <u>preprint</u> arXiv:2508.08241, 2025. 

- [7] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In Proceedings of the IEEE/CVF international conference on computer vision, pages 5442–5451, 2019. 

- [8] Jiaman Li, Jiajun Wu, and C Karen Liu. Object motion guided human motion synthesis. ACM Transactions on Graphics <u>(TOG),</u> 42(6):1–11, 2023. 

- [9] Félix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. ACM Transactions on Graphics <u>(TOG),</u> 39(4):60–1, 2020. 

- [10] Haozhuo Li, Yuchen Cui, and Dorsa Sadigh. How to train your robots? the impact of demonstration modality on imitation learning. arXiv <u>preprint</u> arXiv:2503.07017, 2025. 

- [11] Yixuan Pan, Ruoyi Qiao, Li Chen, Kashyap Chitta, Liang Pan, Haoguang Mai, Qingwen Bu, Hao Zhao, Cunyuan Zheng, Ping Luo, et al. Agility meets stability: Versatile humanoid control with heterogeneous data. arXiv <u>preprint</u> arXiv:2511.17373, 2025. 

- [12] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. arXiv <u>preprint</u> arXiv:2509.16638, 2025. 

- [13] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. arXiv <u>preprint</u> arXiv:2506.14770, 2025. 

- [14] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Castañeda, Shankar Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. arXiv <u>preprint</u> arXiv:2511.15200, 2025. 

- [15] Sarat Ahmad, Maryam Hafeez, and Syed Ali Raza Zaidi. Vision-language models on the edge for real-time robotic perception. arXiv <u>preprint</u> arXiv:2601.14921, 2026. 

- [16] Zepeng Wang, Xiaochuan Shi, Ziluo Ding, Yuxuan Wang, Zhenguo Sun, Chao Ma, and Zongqing Lu. Crosser: Learning generalizable humanoid locomotion through inverse dynamics-guided cross-simulator adaptation. IEEE Robotics and Automation Letters, 10(12):13336–13343, 2025. 

- [17] Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, and Jiangmiao Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. arXiv <u>preprint</u> arXiv:2502.10363, 2025. 

- [18] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standing-up control across diverse postures. arXiv <u>preprint</u> arXiv:2502.08378, 2025. 

- [19] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. arXiv <u>preprint</u> arXiv:2509.13833, 2025. 

12 

- [20] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris M Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In Conference on Robot Learning, pages 1516–1540. PMLR, 2025. 

- [21] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural whole-body controller for humanoid robots. In 2025 IEEE International Conference on Robotics and Automation <u>(ICRA),</u> pages 9989–9996. IEEE, 2025. 

- [22] Ziluo Ding, Haobin Jiang, Yuxuan Wang, Zhenguo Sun, Yu Zhang, Xiaojie Niu, Ming Yang, Weishuai Zeng, Xinrun Xu, and Zongqing Lu. Jaeger: Dual-level humanoid whole-body controller. arXiv <u>preprint</u> arXiv:2505.06584, 2025. 

- [23] Yuxuan Wang, Ming Yang, Ziluo Ding, Yu Zhang, Weishuai Zeng, Xinrun Xu, Haobin Jiang, and Zongqing Lu. From experts to a generalist: Toward general whole-body control for humanoid robots. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025. 

- [24] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Exbody2: Advanced expressive humanoid whole-body control. arXiv <u>preprint</u> arXiv:2412.13196, 2024. 

- [25] Tobias Johannink, Shikhar Bahl, Ashvin Nair, Jianlan Luo, Avinash Kumar, Matthias Loskyll, Juan Aparicio Ojea, Eugen Solowjow, and Sergey Levine. Residual reinforcement learning for robot control. In 2019 international conference on robotics and automation <u>(ICRA),</u> pages 6023–6029. IEEE, 2019. 

- [26] Siheng Zhao, Yanjie Ze, Yue Wang, C Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. arXiv <u>preprint</u> arXiv:2510.05070, 2025. 

- [27] Xue Bin Peng, Yunrong Guo, Lina Halper, Sergey Levine, and Sanja Fidler. Ase: Large-scale reusable adversarial skill embeddings for physically simulated characters. ACM Transactions On Graphics <u>(TOG),</u> 41(4):1–17, 2022. 

- [28] Chen Tessler, Yoni Kasten, Yunrong Guo, Shie Mannor, Gal Chechik, and Xue Bin Peng. Calm: Conditional adversarial latent models for directable virtual characters. In ACM SIGGRAPH 2023 Conference Proceedings, pages 1–9, 2023. 

- [29] Karl Pertsch, Youngwoon Lee, and Joseph Lim. Accelerating reinforcement learning with learned skill priors. In Conference on robot learning, pages 188–204. PMLR, 2021. 

- [30] Oier Mees, Dibya Ghosh, Karl Pertsch, Kevin Black, Homer Rich Walke, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, Jianlan Luo, et al. Octo: An open-source generalist robot policy. In First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024, 2024. 

- [31] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 10895–10904, 2023. 

- [32] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. arXiv <u>preprint</u> arXiv:2507.07356, 2025. 

- [33] Jing Lin, Ailing Zeng, Shunlin Lu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x: A large-scale 3d expressive whole-body human motion dataset. Advances in Neural Information Processing Systems, 36:25268–25280, 2023. 

- [34] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. arXiv <u>preprint</u> arXiv:1707.06347, 2017. 

- [35] Wesley Chung, Lynn Cherif, David Meger, and Doina Precup. Parseval regularization for continual reinforcement learning. Advances in Neural Information Processing Systems, 37:127937–127967, 2024. 

- [36] Tong Zhang, Boyuan Zheng, Ruiqian Nai, Yingdong Hu, Yen-Jen Wang, Geng Chen, Fanqi Lin, Jiongye Li, Chuye Hong, Koushil Sreenath, et al. Hub: Learning extreme humanoid balance. In RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond. 

- [37] Unitree Robotics. Humanoid robot G1_Humanoid Robot Functions_Humanoid Robot Price | Unitree Robotics, 2025. `https://www.unitree.com/g1/` . 

13 

- [38] Junpeng Yue, Zepeng Wang, Yuxuan Wang, Weishuai Zeng, Jiangxing Wang, Xinrun Xu, Yu Zhang, Sipeng Zheng, Ziluo Ding, and Zongqing Lu. Rl from physical feedback: Aligning large motion models with humanoid control. arXiv <u>preprint</u> arXiv:2506.12769, 2025. 

- [39] Zehong Shen, Huaijin Pi, Yan Xia, Zhi Cen, Sida Peng, Zechen Hu, Hujun Bao, Ruizhen Hu, and Xiaowei Zhou. World-grounded human motion recovery via gravity-view coordinates. In SIGGRAPH Asia 2024 Conference Papers, pages 1–11, 2024. 

- [40] Yanjie Ze, João Pedro Araújo, Jiajun Wu, and C. Karen Liu. Gmr: General motion retargeting, 2025. GitHub repository. 

- [41] Yanjie Ze, Zixuan Chen, Joao Pedro Araújo, Zi-ang Cao, Xue Bin Peng, Jiajun Wu, and C Karen Liu. Twist: Teleoperated whole-body imitation system. arXiv <u>preprint</u> arXiv:2505.02833, 2025. 

- [42] Yuhong Zhang, Jing Lin, Ailing Zeng, Guanlin Wu, Shunlin Lu, Yurong Fu, Yuanhao Cai, Ruimao Zhang, Haoqian Wang, and Lei Zhang. Motion-x++: A large-scale multimodal 3d whole-body human motion dataset. arXiv <u>preprint</u> arXiv:2501.05098, 2025. 

- [43] Albert S Huang, Edwin Olson, and David C Moore. Lcm: Lightweight communications and marshalling. In 2010 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 4057–4062. IEEE, 2010. 

14 

# **Appendix** 

## **A RL training details** 

We provide a detailed training environment setting in this section. 

### **A.1 Observation** 

We adopt a single-stage reinforcement learning framework and do not employ a teacher–student architecture [13, 20, 41]. 

**Critic Observations** (Privileged Information). The critic is provided with privileged observations to facilitate stable value estimation. These include proprioception information: linear and angular velocities, joint positions and velocities, keypoint positions and rotations, root position and orientation (expressed in the local coordinate frame), and the last action. In addition, we augment the critic with physical signals, including contact masks, center-of-mass (CoM), and center-of-pressure (CoP). Task-related reference information is also included, consisting of target joint positions and velocities, target keypoint position differences relative to the root, target linear and angular velocities (all in the local coordinate frame), as well as target contact masks, CoM, and CoP signals. 

**Actor Observations** . The actor receives a restricted set of observations without privileged physical signals. Specifically, it observes linear and angular velocities, root position and orientation, joint positions and velocities, and the previous action. Task-related reference observations further include target joint positions and velocities, target selected keypoint (including wrists and ankles) position differences relative to the root, target linear and angular velocities, as well as reference CoM and CoP signals. 

**Residual Policy Observations** . The residual action policy uses the same observation space as the actor network to ensure consistency during fast adaptation. 

### **A.2 Reward** 

We summarize the reward terms used for training both the base policy and the residual policy in Table 4. To ensure consistency and generality, the same reward formulation is applied to both training stages. 

**CoM–Aware Adaptive Tracking Weight.** In addition to the explicit stability reward, we further modulate all motion-tracking rewards using an adaptive weight derived from the reference motion stability. Let _d_<sup>ref</sup> CoM-CoP denote the horizontal distance between the reference CoM and CoP. When this distance exceeds a critical threshold _τ_ , the reference motion is considered physically aggressive or unstable. In such cases, we progressively down-weight tracking-related rewards to grant the controller more freedom to maintain balance. 

Concretely, we define an adaptive tracking weight 


where _τ_ is the stability threshold, _κ_ controls the decay rate, and _w_ min is a small lower bound to preserve minimal tracking awareness. When _d_<sup>ref</sup> CoM-CoP<sup>_≤τ_theweightremainscloseto1,correspondingtofulltracking.</sup> As the reference becomes increasingly unbalanced, the weight decays smoothly toward _w_ min. 

This adaptive factor is multiplicatively applied to key tracking rewards, including body position, anchor position, and joint position terms: 


Such modulation enables a continuous trade-off between motion fidelity and physical stability, preventing the policy from over-committing to physically implausible references while retaining accurate tracking for stable motions. 

15 

Table 4: Unified reward formulation using Gaussian-shaped tracking scores. 

|**Reward Terms**|**Expression**|**Weight**|
|---|---|---|
|**Task reward**|||
|Joint position|exp<br>�<br>_−_<br>�<br>1<br>_|J_target_|_<br>�<br><br>_∥_**q**<sup>des</sup><br>_b_<br>_−_**q**_b∥_<sup>2�</sup><br>_/_0_._4<sup>2�</sup>|1_._0|
||_b∈J_target<br><br>||
|Body position|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_<br>_∥_**p**<sup>des</sup><br>_b_<br>_−_**p**_b∥_<sup>2�</sup><br>_/_0_._3<sup>2�</sup>|1_._0|
||target||
|Body orientation|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_target<br>_∥_log(_R_<sup>des</sup><br>_b_<br>_R_<sup>_⊤_</sup><br>_b_ <sup>)</sup><sup>_∥_2�</sup><br>_/_0_._4<sup>2�</sup><br><br>|1_._0|
|Body linear velocity|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br><br>_∥_**v**<sup>des</sup><br>_b_<br>_−_**v**_b∥_<sup>2�</sup><br>_/_1_._0<sup>2�</sup>|1_._0|
||_b∈B_target<br><br>||
|Body angular velocity|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_target<br>_∥_**_ω_**<sup>des</sup><br>_b_<br>_−_**_ω_**_b∥_<sup>2�</sup><br>_/_3_._14<sup>2�</sup><br><br>|1_._0|
|Anchor position|exp<br>�<br>_−∥_**p**<sup>des</sup><br>anchor <sup>_−_</sup><sup>**p**anchor</sup><sup>_∥_2</sup><sup>_/_0</sup><sup>_._32�</sup>|0_._5|
|Anchor orientation|exp<br>�<br>_−∥_log(_R_<sup>des</sup><br>anchor<sup>_R⊤_</sup><br>anchor<sup>)</sup><sup>_∥_2</sup><sup>_/_0</sup><sup>_._42�</sup>|0_._5|
|Contact mask|1_−∥_**c**robot_−_**c**ref_∥_1_/_2|1_._0|
|**Regularization**|||
|Action smoothness|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|_−_0_._1|
|Undesired self-contacts|�<br>_b/∈B_ee <sup>**1**</sup><br>�<br>_∥f_ <sup>self</sup><br>_b_<br>_∥>_1N<br>�|_−_0_._1|
|Robot balance|exp<br>�<br>_−_max(_∥_**CoM**<sup>xy</sup><br>robot <sup>_−_</sup><sup>**CoP**</sup><sup>_xy_</sup><br>xy<sup>_∥_2</sup> <sup>_−_0</sup><sup>_._12</sup><sup>_,_ 0)</sup><sup>_/_0</sup><sup>_._082�</sup>|_−_2_._0|
|**Penalty**|||
|Termination|**1**[**termination**]|_−_1_._0|
|Joint position limit|�_N_<br>_j_=1<br>�<br>max(_lj −θj,_0) + max(_θj −uj,_0)<br>�|_−_10_._0|


### **A.3 Action** 

We control the 29 degrees of freedom (DoF) of the Unitree G1 humanoid [37] using a proportional–derivative (PD) controller. The policy outputs target joint position offsets that are tracked by the PD controller. 

Specifically, for each joint _j_ , the target joint position at time step _t_ is computed as 


where _q_ ˆ _j_ denotes a fixed default joint configuration, _aj,t_ is the policy output, and _αj_ is a joint-specific scaling factor. 

The scaling factor _αj_ is defined as 


where _τj,_ max is the maximum allowable torque for joint _j_ , and _kp,j_ is the proportional gain (stiffness) of the PD controller. This formulation ensures that the resulting joint position commands respect actuator torque limits. 

The stiffness and damping parameters of the PD controller are set following prior work [6], and are kept fixed throughout training and evaluation. 

16 

### **A.4 Termination** 

An episode is terminated and reset under one of the following three conditions: 

**Fall Detection** . The episode is terminated if the humanoid is considered to have fallen. Specifically, a fall is detected if either (i) the height of the robot root deviates from the reference motion by more than 0.25 m, or (ii) the difference in the vertical gravity component between the reference motion’s anchor orientation and the robot’s anchor orientation exceeds 0.8 rad. 

**Tracking Failure** . The episode is terminated if tracking fails, defined as any end-effector body (left or right ankle, or left or right hand), having a height deviation greater than 0.25 m from the corresponding reference motion. 

**Task Completion** . If the humanoid successfully tracks the reference motion until the final frame without triggering any termination condition, the episode is considered successful and ends naturally. 

### **A.5 Domain randomization** 

Detailed domain randomization setups are summarized in Table 5, following [6]. 

Table 5: **Domain randomization parameters.** ( _U_ [ _·_ ]: uniform distribution) 

|**Domain Randomization**|**Sampling Distribution**|
|---|---|
|**Physical parameters**||
|Static friction coefficients|_µ_static _∼U_[0_._3_,_ 1_._6]|
|Dynamic friction coefficients|_µ_dynamic _∼U_[0_._3_,_ 1_._2]|
|Restitution coefficient|_e_rest _∼U_[0_,_ 0_._5]|
|Default joint positions [rad]|∆_θ_<sup>0</sup><br>_j _<sup>_∼U_[</sup><sup>_−_0</sup><sup>_._01</sup><sup>_,_ 0</sup><sup>_._01]</sup>|
|Torso’s CoM offset [m]|∆_x∼U_[_−_0_._025_,_0_._025], ∆_y∼U_[_−_0_._05_,_0_._05], ∆_z ∼U_[_−_0_._05_,_0_._05]|
|**Root velocity perturbatio**|**ns**|
|Root linear vel [m/s]|_vx ∼U_[_−_0_._5_,_0_._5]_, vy ∼U_[_−_0_._5_,_0_._5]_, vz ∼U_[_−_0_._2_,_0_._2]|
|Push duration [s]|∆_t ∼U_[1_._0_,_ 3_._0]|
|Root angular vel [rad/s]|_ωx, ωy ∼U_[_−_0_._52_,_0_._52]_, ωz ∼U_[_−_0_._78_,_0_._78]|


### **A.6 Adpative sampling** 

To improve learning efficiency on complex and long-horizon motions, we introduce a two-stage adaptive sampling strategy that dynamically resamples training motions based on failure statistics collected during policy learning. The first stage operates at the clip level, where each target motion assigned to an environment is uniformly segmented into fixed-length clips. During training, we record the clip index corresponding to each episode termination or failure. At regular intervals, we estimate a failure rate for each clip and update a per-motion clip sampling distribution accordingly. Environments are then reinitialized by resampling the starting clip based on this distribution, biasing training toward temporally localized motion segments that are more difficult to track. This clip-level resampling mechanism enables the policy to focus on challenging sub-sequences within long motions, significantly improving sample efficiency for learning complex transitions, following a strategy similar to [6]. 

The second stage operates at the motion level, targeting difficulty imbalance across the entire motion dataset. We aggregate failure statistics for each motion across all environments and periodically update a global motion sampling distribution proportional to their observed failure rates. At resampling steps, all environments are reassigned new target motions drawn from this distribution, increasing the training frequency of motions that are globally harder to execute. By jointly applying clip-level and motion-level adaptive resampling, the 

17 

proposed two-stage strategy balances fine-grained temporal difficulty with coarse-grained motion complexity, enabling more effective learning of diverse and high-difficulty whole-body behaviors. 

### **A.7 Model details** 

As described in the main paper, following prior work [13, 23], we adopt a mixture-of-experts (MoE) architecture to model diverse humanoid motion dynamics. Both the policy (actor) and value (critic) networks consist of multiple expert networks and a shared gating network. 

Table 6: **Hyperparameters for policy training.** 

|**Term**|**Value**|
|---|---|
|Num parallel envs|4096|
|Num steps per env|24|
|Learning epochs|5|
|Num mini_batches|4|
|Discount _γ_|0.99|
|GAE _λ_|0.95|
|PPO clip ratio|0.2|
|Value loss coefficient|1.0|
|Entropy coefficient|1e-2|
|Initial learning rate|1e-3|
|Max learning rate|1e-2|
|Min learning rate|1e-5|
|Desired KL|0.01|
|Max grad norm|1.0|
|MLP hidden layers|[512, 256, 128]|
|Num experts|12|
|Parseval scaling factor|2.0|
|Parseval loss coefficient|1e-7|
|KL regularization coefficient|1e-4|


Each expert network is implemented as a three-layer multilayer perceptron (MLP) with hidden layer sizes of 512, 256, and 128, respectively. The gating network takes the same observation as input and outputs state-dependent mixture weights over experts. The hidden layer dimension of gating network is set to half of the corresponding input dimension for both the actor and critic. At each timestep, the final policy action (or value estimate) is computed as a weighted sum of the outputs from all experts. 

For fast adaptation, the residual (delta) policy is parameterized by a lightweight three-layer MLP with the same hidden layer sizes (512, 256, 128), but without an MoE structure. This design reduces optimization complexity while retaining sufficient expressivity for adaptation. All networks use the ELU activation function. 

Other hyperparameters related to policy training are shown in Table 6. 

## **B Proofs of Stability Analysis of Residual Policy Adaptation** 

_Proof of Proposition 3.1 (Lipschitz Continuity with Scaled Orthogonality)._ The residual policy _πr_ is a composition of affine transformations and activation functions: 


18 

Since the activation function _ϕ_ ( _·_ ) is assumed to be 1-Lipschitz, it satisfies 


Each affine transformation _fl_ is Lipschitz continuous with constant _∥Wl∥_ 2: 


where the bias terms cancel out and thus do not affect the Lipschitz constant. By the composition property of Lipschitz functions, 


Under Parseval regularization, we assume that for each layer _l_ = 1 _, . . . , L −_ 1, 


Since _∥Wl∥_<sup>2</sup> 2<sup>=</sup><sup>_λ_max(</sup><sup>_W ⊤_</sup> _l_<sup>_Wl_),itfollowsthat</sup> _∥Wl∥_ 2<sup>2=</sup><sup>_λ_max(</sup><sup>_W ⊤_</sup> _l_<sup>_Wl_)</sup><sup>_≤λ_max(</sup><sup>_sI_) +</sup><sup>_∥W_</sup> _l_<sup>_⊤Wl−sI∥_2</sup><sup>_≤s_+</sup><sup>_εl,_</sup> (14) 

and hence 


Substituting this bound yields 


Thus, the residual policy _πr_ is Lipschitz continuous with a bounded Lipschitz constant. 


_Proof of Proposition 3.2 (Distributional Stability under KL Constraint)._ For Gaussian policies with identical covariance Σ, the KL divergence reduces to 


Applying the KL constraint yields 


By the Rayleigh quotient bound, 


Combining the above inequalities gives 


Recalling that _µ_ = _µb_ + _µr_ holds pointwise for each state, we have _µr_ = _µ − µb_ , and thus 


which directly bounds the magnitude of the residual policy output. 


19 

## **C Dataset description** 

### **C.1 Dataset composition** 

As described in the 4.1, we employ multiple datasets for training and evaluation to comprehensively assess the generality, robustness, and scalability of FAST. In addition to commonly used motion datasets such as AMASS, OMOMO, and LaFan1, we further incorporate Motion-X and an in-house motion capture dataset. These datasets differ in motion quality, diversity, and acquisition modality, and are used for complementary training and evaluation purposes, as detailed below. 

**Motion-X Dataset.** Motion-X is a large-scale 3D expressive full-body motion dataset constructed from a combination of large amounts of online videos and eight existing motion datasets. Compared to optically captured datasets such as AMASS, motions in Motion-X, especially those extracted from videos, exhibit lower geometric accuracy, but offer substantially greater diversity in motion types and scene coverage [42]. 

We use a leg-dominant subset of the Motion-X dataset for both base model evaluation and fast adaptation. Motion-X is selected due to its relatively low-quality and noisy motion signals, which provide a challenging benchmark for assessing robustness to imperfect reference motions. All Motion-X data are processed using the same retargeting pipeline described in Section 3.1. 

To emphasize high-dynamic behaviors, we cluster the Motion-X dataset based on text annotations and extract motion clips dominated by leg-intensive actions. The resulting subset contains 6,009 clips (approximately 15.24 hours of motion data) and is consistently used as both the test set for base model comparison and the target dataset for fast adaptation experiments. 

**In-House Motion Capture Dataset.** In addition to public datasets, we collect an in-house indoor motion capture dataset covering a broad range of full-body motions. This dataset includes both common locomotion and manipulation behaviors, as well as high-dynamic motions, and serves as an additional source of real-world motion data. 

From this dataset, we further identify and curate a subset of high-dynamic motions specifically for evaluating the effectiveness of Center-of-Mass-Aware Control. This subset includes actions such as single-leg balancing, kicking, and punching, with each motion sequence lasting at least 5 seconds. From the curated high-dynamic subset, we randomly select 12.6 minutes of data as high-dynamic motions included in the training set, and reserve 51.7 minutes as an out-of-distribution (OOD) zero-shot evaluation set. The composition of the OOD high-dynamic dataset is illustrated in Figure. 6. 


Figure 6: The composition of the OOD high-dynamic dataset. 

20 

### **C.2 Dataset preprocessing** 

The retargeted motions are further processed through a series of steps before being used for policy training. These steps aim to improve motion diversity, physical consistency, and the availability of auxiliary training signals. 

**Motion Augmentation via Physical Attribute Perturbation.** To increase motion diversity and improve robustness to distribution shifts, we apply targeted data augmentation directly to the retargeted humanoid motions by modifying selected physical attributes. Specifically, we adjust the global root translation and velocity to generate motions with different execution speeds. 

In addition, we perturb knee joint angles to synthesize varied walking postures while preserving overall motion coherence. To compensate for these knee modifications, the pitch angles of the hip and ankle joints are adjusted by half of the knee angle change. This heuristic maintains kinematic consistency and avoids introducing unrealistic poses. These controlled perturbations effectively expand the motion distribution without violating basic physical plausibility, encouraging the policy to generalize across a wider range of motion styles and speeds. 

**Global Height Adjustment for Physical Consistency.** Due to retargeting and the aforementioned pose perturbations, the global vertical translation of the motion may no longer satisfy basic physical constraints, such as maintaining foot contact above the ground plane. To address this issue, we perform a global height correction on each motion sequence. 

Specifically, we estimate a reasonable minimum foot height using the lower quartile (25th percentile) of foot heights over the entire motion sequence. Based on this estimate, a vertical offset is applied uniformly to all frames in the sequence to ensure that the feet remain physically plausible with respect to the ground. This procedure preserves relative motion structure while restoring global consistency. 

**Contact Mask Estimation.** Following height adjustment, we compute contact masks based on the distance between the feet and the ground. The contact threshold is determined empirically using MuJoCo visualization, where foot–ground contact can be visually inspected through rendered contact indicators. 

We note that different motion batches may require different contact thresholds due to variations in retargeting quality, physical constraint satisfaction, and motion capture accuracy. Therefore, the threshold is adjusted on a per-batch basis to ensure reliable contact estimation. 

**Motion Replay and Auxiliary Signal Extraction.** Finally, we use IsaacLab as a forward dynamics engine to replay the processed motion sequences. By combining motion replay with finite-difference approximations, we extract additional auxiliary signals required for training, including body positions, body orientations, linear velocities, angular velocities, center-of-mass (CoM), center-of-pressure (CoP), joint positions and joint velocities. 

The resulting motion data thus contains rich kinematic and physical annotations, which are used to support stable and effective training of the general whole-body controller. 

## **D Experiment details** 

### **D.1 Task Failure conditions** 

The task failure conditions vary across experiments to reflect different evaluation objectives. 

For **fast adaptation experiments** , the failure conditions are identical to those described in Appendix A.4, ensuring consistency with the base training setup. 

For **base model comparison** , to better highlight differences in global position tracking accuracy, we introduce an additional failure criterion: an episode is terminated if the robot’s root position deviates from the reference motion by more than 2.0 m. This criterion emphasizes long-horizon global tracking performance. 

For **CoM-Aware Control experiments on high-dynamic motions** , we further tighten the global root position deviation threshold to 1.5 m. This stricter criterion more sensitively captures failures caused by 

21 

balance loss that lead to excessive global drift. At the same time, we relax the height deviation constraints on end-effectors, so that the success metric better reflects balance-related performance rather than strict limb-level tracking accuracy. 

Moreover, in the latter two experimental settings, we do not introduce an explicit orientation-based termination criterion. This is because large orientation instabilities are already implicitly captured by the global root position deviation condition, which reflects physically meaningful failures such as loss of balance or unrecoverable drift. Moreover, for the CoM-aware control evaluation, introducing additional rotation-based termination may prematurely terminate relatively conservative but stable behaviors that involve transient torso tilting, thereby shifting the focus away from the core objective of balance robustness. By relying on global position drift as the primary failure signal, we better assess the controller’s ability to maintain physically stable and recoverable motion under challenging dynamics. 

### **D.2 Deployment** 

The control policy is executed at an inference frequency of 50 Hz, while the low-level control interface operates at 500 Hz to ensure smooth and responsive actuation. Communication between the high-level policy and the low-level controller is handled via Lightweight Communications and Marshalling (LCM) [43], enabling efficient real-time data exchange. 

State estimation, including linear velocity and position estimation, is implemented using the legged_control2 library [6]. To support fast and stable inference during real-world deployment, the trained policy is exported to the ONNX format and executed using an optimized runtime. 

All policy-related modules, including the neural policy and the state estimator, are deployed directly on the robot computer. Motion capture acquisition and retargeting are executed on an external workstation (Inter Core Ultra 7 255HX, 20 cores). The two machines communicate wirelessly via Wi-Fi using ZeroMQ, maintaining a stable bidirectional motion streaming rate of 50 Hz for reference transmission and feedback synchronization. 

22 

