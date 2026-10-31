---
title: "MuGen: Multi-Skill Generative Locomotion Controller for Humanoid Robots"
date: "2026-05-23"
authors: "Yusen Feng; Xiang Wang; Heyuan Yao; Zixi Kang; Xinyu Huo; Boyang Yu"
url: https://arxiv.org/abs/2605.24592
pdf: https://arxiv.org/pdf/2605.24592
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.24592)** / [論文ページ](https://arxiv.org/abs/2605.24592)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# **MuGen: Multi-Skill Generative Locomotion Controller for Humanoid Robots** 

Yusen Feng<sup>_∗_</sup> , Xiang Wang<sup>_∗_</sup> , Heyuan Yao, Zixi Kang Xinyu Huo, Boyang Yu, Pengyun Qiu, Ruijie Zhao Baoquan Chen<sup>_†_</sup> , Libin Liu<sup>_†_</sup> 

_Peking University_ 

**_Abstract_ —This paper presents MuGen, a data-driven framework for learning and deploying multi-skill locomotion on humanoid robots. MuGen enables a robot to perform expressive motions like humans under the guidance of example motion sequences. To achieve this, we employ vector-quantized autoencoders (VQ-VAEs) trained with model-based reinforcement learning, resulting in a generative representation of locomotion that captures key patterns of human motion from hours of heterogeneous human performance data. We employ a teacherstudent learning framework and develop a new policy distillation strategy to enable a deployable student policy learning this efficient latent representation. This policy allows the robot to track and mimic unseen human motions and further enables the robot to reuse the learned latent space for other tasks. We demonstrate the effectiveness of our framework through a diverse set of motions and accurate execution.** 

## I. INTRODUCTION 

Humanoid robots have achieved significant advancements in bipedal locomotion and dynamic maneuvers (e.g., running, jumping, getting up, acrobatics) through deep reinforcement learning (RL) frameworks. However, careful task-specific reward shaping and tuning of RL algorithms are typically required for these tasks, which is often challenging and not generalizable across tasks. By leveraging the morphological similarity between humanoid robots and humans, along with the increasing availability of human motion performance datasets, imitating human performance has emerged as a promising approach for humanoid robots [1], [2], [3], [4]. This approach alleviates the burden of precise reward shaping and enables robots to leverage the control strategies embedded in human motion to produce agile and expressive behaviors. 

Existing methods for motion imitation typically train policies to take reference kinematic trajectories as part of the input and compute actions that control the robot to follow these trajectories. A kinematic motion generation module may also be employed to generate motions based on task goals, producing new reference trajectories that are then fed to the policy for tracking [3]. However, this paradigm has two main limitations. First, naive tracking policies cannot effectively capture the structure of the action space under the kinematic and dynamic constraints of the robot, and they often struggle to extract distinctive motion patterns from large-scale datasets and reuse them in downstream tasks. Second, the separation of motion generation and robot control cannot guarantee the 

dynamic reliability of the generated trajectories. Even if the trajectories are kinematically plausible, the tracking policy may be unable to reproduce them, leading to suboptimal results or even failures. 

In this paper, we address these fundamental limitations by learning a generative control system, **MuGen** , from a large human motion dataset with various locomotion performances. MuGen learns a structured latent space for motion skills and actions directly from physical simulation, ensuring that the skill embeddings are consistent with the kinematic and dynamic constraints of the robot. By projecting kinematic trajectories into this latent space or generating new trajectories from it, MuGen can achieve robust tracking on unseen motions and generation of new motions within the capabilities of the robot. 

We employ vector-quantized variational autoencoders (VQVAE) as the generative model, with the goal of reconstructing input motions from discrete latent codes. To achieve effective training, we draw inspiration from recent work in physics-based motion control [5], [6] and adopt a modelbased reinforcement learning (MBRL) approach, in which a differentiable dynamics model is trained to bridge the gap between kinematic references and the actions predicted by the policy. To further facilitate training, we adopt a two-stage training strategy. First, a teacher generative policy is learned using privileged information, and then the policy and skill embeddings are distilled into a deployable student policy. To this end, we develop a novel DAgger [7]-style distillation strategy with a progressive scheduling mechanism. 

We evaluate MuGen on a diverse set of locomotion tasks and validate its performance in robust tracking and the generation of new motions on a Unitree G1 humanoid robot. Our approach significantly outperforms baseline methods in terms of tracking accuracy and robustness when trained on a small set of human motions and generalizes to unseen motions. We also demonstrate that MuGen can generate robust control of new motions using the latent embeddings without requiring reference trajectories. 

## II. RELATED WORKS 

## _A. Legged Robot Locomotion_ 

Legged locomotion has long been a fundamental topic in robotics, with early approaches primarily centered on model-based control and trajectory optimization. Classical methods, ranging from the pioneering WABOT [8] and early 

> _∗_ Equal contribution. 

> _†_ Corresponding authors. 

2 


Fig. 1: **MuGen** enables multi-skill humanoid locomotion by learning a generative controller. (a-d): A simulated humanoid tracks (a) a long walking motion manually crafted from motion data and (b–d) dance, run, and crouching walk motions selected from the motion dataset. (e-f): A real Unitree G1 robot tracks short segments of (e) a straight walk and (f) a crouching walk from the motion dataset. Details are provided in Section IV-A. 

dynamic walking studies [9] to the landmark Honda humanoids [10] rely heavily on accurate analytic models [11], [12], [13], [14], [15]. Subsequent work introduced hybrid-zero dynamics [16], whole-body task hierarchies [17], and the 3-D LIPM for pattern generation [18]. Model-based techniques remain state-of-the-art for many humanoid and quadruped platforms, including ANYmal [19], geometric retargeting [20], multimode or tele-operated frameworks [21], [22], [23], [24], whole-body MPC [25], [26], [27], [28], and recent acrobatic or synchronized human–robot studies [29], [30]. Despite their effectiveness, these methods demand extensive expert tuning and often degrade under modeling error or unstructured terrain. 

## _B. Reinforcement Learning-based Methods for Locomotion_ 

Recent advances in reinforcement learning (RL) have shown remarkable robustness and adaptability, as policies are learned directly from interaction without an exact dynamics model. For quadrupeds, model-free RL enables agile motion imitation [31], rapid motor adaptation [32], energy-efficient gait discovery [33], vision-based blind stair climbing [34], and parkour-level versatility [35], [36], [37]. RL further supports loco-manipulation [38], [39], [40] and dynamic ball-dribbling [41]. For bipeds and humanoids, policies have progressed from simulation-only agility [42], [43], [44], [45] to real-world deployment [46], [47], [48], RL exoskeleton-cockpit teleoperation [49] , and versatile jump/stand-up controllers [50], [51]. Nevertheless, low sample efficiency and the sim-to-real gap remain key obstacles. Some works [52], [53] combine online system identification with policy learning, while extensive domain randomization is still common practice [54], [55], [56]. However, these tasks often require fine-grained reward design with respect to the goal. In this work, we address these limitations by proposing a differentiable physical simulator, transforming humanoid behaviors learning into a model-based approach. Our method reduces the need for extensive reward engineering and enables direct transfer from simulation to real robots. 

## _C. Imitation Learning-based Methods for Locomotion_ 

Imitation learning (IL) leverages motion-capture or video demonstrations to mitigate reward-design burdens. Recent 

work in physics-based motion control condenses large-scale human-motion datasets into compact skill sets via generative controllers. This began with VAE models [57], [58], followed by adversarial motion priors [59], [60], evolving toward reusable skill embeddings [44], [5], [45], [61], [6] and masked-motion inpainting [62]. As for the deployment, Quadruped IL combines trajectory optimization with policy distillation [63], [64], adversarial priors in the wild [1], [2], model-based learning with VAE [65], and multi-modal whole-body control [66]. Humanoid IL explores expressive whole-body control [67], [3], omni-directional tele-operation [68], [69], [70], instant human camera data [71], next-token transformer control [72], universal motion representations [73], generative strategy learning [74], surrogate function tuning [75], and GAN-based style distillation [4]. While these combinations greatly improve motion realism and sample efficiency, reliable transfer to hardware still hinges on accurate dynamics alignment and sensor calibration. Potential solutions include AMP-in-real adaptations [76], [70] and using delta action model that compensates for the dynamics mismatch [53]. Motivated by VAE based works [5], [65], [61], [6], our approach complements these efforts by introducing a VQVAE encoder–decoder that learns a discrete, dynamics-feasible motion latent space from heterogeneous human data, enabling zero-shot composition and real-world execution of diverse humanoid skills. 

## III. METHOD 

We propose MuGen, a data-driven framework for learning and deploying multi-skill locomotion on humanoid robots. As illustrated in Figure 2, MuGen employs a teacher-student architecture for robust motor skill acquisition. The teacher learns skills using privileged information, aided by a world model that enhances sample efficiency and enables efficient optimization via backpropagation. The student distills these skills for deployment with limited information. Skill knowledge is transferred using a shared Vector-Quantized (VQ) codebook as a skill space, combined with simultaneous behavior cloning in both this VQ space and the raw action space. We elaborate on these components in the following sections. 

3 


Fig. 2: **System overview** 1) _Motion Skill Embedding:_ states and reference motions are encoded into continuous representations, then a VQ bottleneck maps embeddings to a trainable codebook. 2) _Student policy:_ using the shared codebook, the student decodes actions from partial observations and aligns them with teacher outputs through behavior cloning. All training is performed in simulation environment. 

## _A. Problem Formulation_ 

We target generative humanoid locomotion by training controllers using model-based reinforcement learning (MBRL). The task is framed as a partially observable Markov decision process (POMDP), represented by the tuple _M_ = _⟨S, O, G, A, P, R⟩_ . Here, _S_ , _O_ , _G_ , and _A_ denote the state, observation function, goal, and action spaces, respectively. _P_ ( _s_<sup>_′_</sup> _| s, a_ ) describes the true environment transition dynamics, and _R_ ( _s, a, g_ ) is the reward function. In our locomotion context, _R_ typically quantifies how closely the robot’s state or resulting motion aligns with reference motion capture data, as specified by the goal _g_ . The standard objective in this framework is to find a policy _π_ that maximizes the expected discounted cumulative reward E[<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtRt_].</sup> 

Instead of maximizing returns in the true environment _P_ (often requiring sample-based gradients), our MBRL approach employs a learned, differentiable world model _W_ ( _s_<sup>_′_</sup> _| s, a_ ), which approximates the true dynamics _P_ . The objective function turns to: 


where _πθ_ ( _at | st_ ) is a parameterized control policy, _γ ∈_ (0 _,_ 1] is the discount factor and _L_ is a differentiable loss with _L_ = _−R_ . The outer expectation involves sampling actions from the policy _πθ_ and predicting next states _st_ +1 using the differentiable world model _W_ . Because both _πθ_ and _W_ are differentiable, we can efficiently compute the gradients of the loss objective with respect to the policy parameters _θ_ using backpropagation through the predicted state trajectories. This avoids the need for high-variance, sample-based gradient estimators often used in model-free RL and enables stable, end-to-end gradient-based optimization of the control policy. 

## _B. Dynamics Model_ 

We adopt a world model that serves as the predictor of the next state for environment modeling. At time step _t_ , the world model takes the current robot state _st_ and the action _at_ produced by the teacher policy, and predicts the change of state between time steps. We then integrate the change with the current robot state to obtain the predicted next state _st_ +1. The world model is optimized by minimizing reconstruction loss: 


where _WW_ represents a predefined set of weights the metric. _LW_ penalizes deviations between the simulated next states _s_<sup>sim</sup> _t_ +1<sup>and the world model’s predictions</sup><sup>_s_</sup> _t_<sup>_W_</sup> +1<sup>. Notably, to build</sup> a more precise prediction, the world model has access to full privileged information as input. Therefore, we jointly optimize the teacher policy and the world model through alternating updates. During the distillation process, we freeze the world model to prevent performance degradation when we begin the distillation process. 

## _C. Skill Embeddings_ 

As shown in Figure 2, the teacher policy comprises an encoder _E_ and a decoder _D_ . The encoder _E_ maps states _s_ and reference motion _m_ to continuous embeddings _z_ = _E_ ( _s, m_ ), which are then quantized by a VQ bottleneck to the nearest codebook entry _z_ ˆ = _B_ ( _z_ ). The decoder _D_ conditions on the code and the current state to output a distribution over joint targets, _a ∼D_ ( _·|z, s_ ˆ ), encouraging reuse of motion primitives and stabilizing exploration. Since the simulation environment is not differentiable, we adopt world model to predict the resulting next state _s_<sup>_W_</sup> _t_ +1<sup>_∼W_(</sup><sup>_·|s, a_)forgradient</sup> 

4 

backpropagation. We jointly optimize the teacher policy and the codebook during the same update steps with the objective function: 


where _WT_ denotes weights of state-component which will be shown in Section B, _β_ 1 controlling the commitment weights. _L_ rec enforces consistency between reconstructed and reference states, and _L_ VQ regularizes the latent space using stop-gradient operators sg( _·_ ). Following the approach suggested in the appendix of [77], we replace the optimization stage of codebook update loss by applying the strategy of exponential moving averages (EMA) to update the dictionary items. The whole objective function _LT_ simultaneously enforces both behavioral fidelity and latent space regularity. We further apply two regularization terms _L_ reg on the decoded action to encourage smooth and normal actions. It is notable that the codebook will only be updated during this stage, and will remain frozen during the training of the student policy. 

## _D. Policy Distillation_ 

The teacher-student framework is widely used for deployable policy distillation [68], [3], [78], [79]. However, this process often encounters a capability drop due to the lack of privileged information, which is only available in simulation and significantly enhances policy performance. To bridge this gap, we propose teacher-student architecture with distinct observation space<sup>1</sup> but a shared latent skill domain. The key component of the generative policy, the VQ codebook _B_ , is shared between the teacher and student. _B_ enables the student to leverage high-quality dynamics and motion skills learned by the teacher, thereby implicitly transferring knowledge accessible only through privileged information. The behavior cloning objective function of student policy combines action-level and latent-space matching: 


where _ρπ_ S denotes the state space observed by student policy and _β_ 4 is a balancing weight. _L_ align encourages the student encoder _E_<sup>S</sup> to produce embeddings compatible with the teacher’s frozen codebook _B_ , enabling feature-level knowledge transfer while maintaining flexibility. _L_ BC is a standard behavior 

> 1Appendix B will show detailed observation space for both teacher and student policies. 

cloning loss which directly minimizes the action discrepancy between the student and teacher. 

## _E. Training Schedule_ 

The training process of MuGen is divided into three main stages: (1) _Pretraining_ : build the skill latent space within the VQ codebook by training teacher policy. (2) _Warming up_ : refine the teacher policy and codebook, and warm up the student policy. (3) _Distillation_ : allow the student policy to gradually take over control to obtain a deployable policy. 

During the _Pretraining_ stage, we optimize and roll out only the teacher policy. The teacher policy and world model are jointly trained through alternating updates using Equation (2) and Equation (3). We do not optimize the student policy at this stage because the teacher is still exploring and building the codebook, and an unstable target policy could harm early student learning. 

In the _Warming Up_ stage, we optimize all modules, include the student policy, while continuing to roll out trajectories using only the teacher policy. Once the teacher has sufficiently learned and student has warmed up, we proceed to the distillation stage, where the student policy gradually takes over robot control. 

In the _Distillation_ stage, the teacher policy and the codebook are frozen, and the student policy is continually trained to distill the knowledge of the teacher. We establish a smooth transition between the teacher and student: in each rollout trajectory of this stage, we randomly choose between _π_<sup>T</sup> and _π_<sup>S</sup> at every step, with the probability of selecting the teacher policy linearly annealed to zero. This strategy differs from the original DAgger [7], as the policies are mixed within a single trajectory, allowing the teacher to stabilize the robot when the student makes incorrect decisions. This linear annealing strategy mitigates abrupt distribution shifts while preserving the benefits of teacher oversight during early training stages. 

After completing the _Distillation_ stage, MuGen is ready for deployment. For more details, please refer to the pseudocode provided in Algorithm 1 in the Appendix. 

## IV. EXPERIMENTAL RESULTS 

Our training and evaluation framework is implemented using the NVIDIA IsaacGym [80] simulator. To bridge the simto-real gap, we apply domain randomization during training by varying simulation parameters, adding random noise to observations, and applying random weight loads to the robot’s torso. For more details, please refer to Appendix C. We utilize the retargeted version of the LaFAN1 motion dataset [81] provided by Unitree [82] for training and testing MuGen. Specifically, we use a selected subset of this dataset containing only locomotion, with a total duration of roughly one hour. Appendix A provides detailed statistics of this locomotion dataset. 

## _A. Simulation Results_ 

We evaluate MuGen’s performance in simulation using the one-hour selected subset of the LaFAN1 dataset. As 

5 


Fig. 3: The trajectory generated by the student policy using the learned prior encoder _E_<sup>ˆ</sup> = _E_<sup>ˆ</sup> ( _z|s_ ). 

illustrated in Figure 1, MuGen’s student policy successfully tracks various motions using only deployable observations. Specifically, Figure 1(c) and (d) show results for tracking a motion sequence from the same dataset. The reference motion in Figure 1(a) is created by repeating the kinematic trajectory of a walking cycle selected from the dataset. We find that the MuGen policy can maintain balance even when tracking unseen motions that are very different from the training data, such as a dance. However, the robot struggles to perform such motions using only the learned skills from the training set. To demonstrate that our framework is capable of robustly controlling more dynamic skills, we train a new MuGen policy using a single reference dance clip. The student policy can then perform the dance accurately, as shown in Figure 1(b). These results confirm that MuGen can generalize well to diverse locomotion tasks when trained on unstructured data and achieve precise tracking performance under targeted training. 

_1) Generation Ability:_ We further evaluate the generative ability of our deployable student policy and design an experiment in which the student autonomously produces motion by sampling latent skills from the pretrained VQ codebook. This is carried out in a post-training stage, where we introduce a new encoder called prior encoder _E_<sup>ˆ</sup> , which only accepts the state as input, while freezing all other components. The prior encoder _E_<sup>ˆ</sup> = _E_<sup>ˆ</sup> ( _z|s_ ) takes only proprioception input and outputs a probability distribution over discrete codebook indices. A corresponding latent skill embedding _z_ ˆ is then extracted from the codebook and passed into the frozen decoder _D_ . This setup allows us to generate actions directly from onboard observations using learned skills. 

To train _E_<sup>ˆ</sup> , we let the teacher policy track randomly selected reference motions and treat the resulting codebook indices as labels. The prior is trained via a standard cross-entropy loss to predict these indices. During inference, we compose a fully deployable policy by combining the trained prior encoder _E_ ˆ, the codebook _B_ , and the student decoder _D_ . Figure 3 demonstrates that the student policy, conditioned only on the proprioceptive state, can generate smooth and diverse behaviors, transitioning between different motion patterns such as walking, running, crouching, and turning around, without any reference motion. These results validate the expressiveness 

and robustness of MuGen’s learned skill space and its capacity for real-time generative control. 

## _B. Ablation Study_ 

To assess the key components of our system design, we conduct ablation studies that evaluate the performance of policies under various settings. The goal is to measure how well each policy can maintain stable tracking under random perturbations introduced by domain randomization. We compare MuGen against two baselines: (1) a vanilla MLP policy that directly maps input states and reference motions to actions, and (2) a VAE-based policy, where the latent skill space is continuous rather than discretized. Details of these baselines can be found in Appendix F. All models are trained on a small subset of the LaFAN1 dataset consisting of approximately 200 seconds of walking motions and tested on both the same motion set and an additional test subset of approximately 90 seconds of walking motions. Detailed information about the dataset used for the ablation study is provided in Appendix A. 

We evaluate the performance of these policies by tracking the same reference motions in 1,024 simulation environments, each initialized with different domain randomization parameters. To assess robustness, we report the following metrics: (1) **Survival Rate (SR)** , the proportion of environments completed without falling, (2) **Mean Joint Rotation Error (MJRE)** , the average local rotation error between each joint and its reference joint over successful rollouts, measured in radians, and (3) **Mean linear Velocity Error (MVE)** ,the average deviation of root velocity from the reference. Results are summarized in Table I. MuGen achieves strong performance, with higher SR and lower MJRE on both seen and unseen motions, demonstrating better generalization and greater resilience to disturbances compared to both baselines. The vanilla MLP policy achieves strong performance on the training dataset but shows a dramatic performance drop on unseen data, indicating overfitting to the training set. These findings highlight the effectiveness of discrete skill embeddings in enhancing policy robustness. 

We further ablate the importance of the length of temporal context in the state representation and the smooth transition strategy described in Section III-E. **Temporal Context:** We 

6 

TABLE I: Evaluation on tracking task for MuGen and baselines. 

|Model|SR_seen↑_|MJRE_seen_ (rad)_↓_|MVE_seen↓_|SR_unseen↑_|MJRE_unseen_ (rad)_↓_|MVE_unseen↓_|
|---|---|---|---|---|---|---|
|baseline w/o history|**0.9082**|**0.0759**|0.3581|0.6070|0.0996|0.4832|
|VAE-based w/o history|0.6490|0.0842|0.3519|0.5151|0.1094|0.4359|
|VQ-based w/o history|0.8072|0.0977|0.4303|0.7279|0.1108|0.4686|
|MuGen(Ours)|0.8820|0.0791|**0.3404**|**0.9535**|**0.0927**|**0.3652**|


TABLE II: Ablation of History Observation. 

|#HT|#HS|SR_seen↑_|MJRE_seen_ (rad)_↓_|MVE_seen↓_|SR_unseen↑_|MJRE_unseen_|(rad)_↓_<br>MVE_unseen↓_|
|---|---|---|---|---|---|---|---|
|0|0|0.8072|0.0977|0.4303|0.7279|0.1108|0.4686|
|0|5|**0.8820**|**0.0791**|**0.3404**|**0.9535**|**0.0927**|**0.3652**|
|2|5|0.8666|0.0907|0.3674|0.6810|0.1101|0.4230|
|5|5|0.2006|0.0925|0.4455|0.2615|0.1170|0.4888|
|2|10|0.6901|0.0824|0.3605|0.4824|0.1066|0.4156|


vary the number of historical frames observed by the teacher (#HT) and student (#HS) policies to assess the role of temporal information. Results in Table II indicate that incorporating a moderate history horizon improves tracking accuracy and survival rate by providing better motion continuity and contextual cues. However, using excessive history introduces noise and may exceed the representational capacity of the policy networks, leading to reduced performance. **Smooth Transition:** As illustrated in Figure 4, disabling the smooth transition mechanism, i.e., switching control from the teacher to the student at the beginning of the _Distillation_ stage, leads to a significant performance drop. The training becomes unstable during the stage-switching period, which in turn degrades the final performance. This demonstrates the importance of our scheduling strategy in policy distillation. 

## _C. Real-World Deployment_ 

Our experiments are conducted on the Unitree G1 humanoid robot (35 kg, 1.32 m height) equipped with 23 actuated degrees of freedom (legs: 6 _×_ 2, arms: 5 _×_ 2, waist: 1). The policy is executed at 30 Hz to generate target joint position and a lowlevel PD controller is actuated at 500 Hz to follow desired joint position. We carefully select motions that are safe for deployment, using this subset for training and deployment of MuGen. Our deployment codebase builds upon unitree <u>rl gym[83].</u> Since the default standing pose of the robot differs significantly from the first frame of the reference motion, we perform linear interpolation at the beginning to prevent large impulsive forces that could destabilize or damage the hardware. Results of realworld deployments are illustrated in Fig. 1 (e-f). 


Fig. 4: Training Curves of different model designs. We calculate weighted tracking error and map it into reward matrix with _e_<sup>_−wx_</sup> , where _w_ is a weight factor and _x_ is the tracking error in global space. 

## V. CONCLUSION 

## VI. LIMITATIONS 

In this paper, we present a generative locomotion framework for humanoid robots based on a VQ-VAE skill embedding architecture. Our method distills a diverse skillset of locomotion skills from unstructured human motion data and produces a deployable student policy capable of real-time motion generation. The resulting controller can robustly track unseen motions and generate human-like behaviors without the need for handcrafted reward design. 

While our framework demonstrates the potential of generative models for humanoid locomotion and successfully builds what is, to the best of our knowledge, one of the first generative controllers for humanoid robots, several real-world constraints currently limit its scalability: 

- **Difficulty with Standing Still.** We observe that our generative policy struggles to maintain a stable standing 

7 

pose. This behavior arises because the VQ codebook was primarily trained on motion-rich sequences, and the quantized embeddings corresponding to static or quasistatic poses are underrepresented or ambiguous. As a result, the policy tends to alternate between similar but distinct embeddings, resulting in oscillatory motions like shuffling or pacing. 

- **Inaccurate World Model.** Our learned dynamics model is a simple MLP and does not explicitly account for environmental interactions. While we observe that optimization is effective as long as gradients from the world model are directionally informative, its limited accuracy ultimately caps the performance of the teacher policy, especially for precise tracking. 

- **Limited Sim-to-Real Adaptation.** Our deployment relies solely on domain randomization to bridge the sim-toreal gap and stable deployment remains a challenge. A more robust approach would involve fine-tuning the world model using real-world rollouts and re-distilling a student policy accordingly. 

**Future Work.** Potential directions include replacing MoCap with vision-based or onboard pose estimation, enhancing the world model with structure or uncertainty modeling, and scaling the skill codebook to encompass more diverse behaviors and terrains. Additionally, we envision integrating natural language interfaces—e.g., a GPT-style model mapping text prompts to skill sequences—for building a prompt-driven humanoid motion generation system. 

## ACKNOWLEDGMENT 

We thank Ruoyu Lin, Shiyi Xu, Yutong Liang, Liyuan Wang, Xurong Lu, Kunqi Xu, for help with deploying on G1 hardware. We thank Tao Huang for always being there to help with any problem and answer any question. We thank Yulong Zhang for invaluable feedback and for helping us use precise terminology throughout this work. We thank Unitree Robotics for help with G1 support. 

## REFERENCES 

- [1] A. Escontrela, X. B. Peng, W. Yu, T. Zhang, A. Iscen, K. Goldberg, and P. Abbeel, “Adversarial motion priors make good substitutes for complex reward functions. 2022 ieee,” in _International Conference on Intelligent Robots and Systems (IROS)_ , vol. 2, 2022. 

- [2] Y. Wang, Z. Jiang, and J. Chen, “Amp in the wild: Learning robust, agile, natural legged locomotion skills,” _arXiv preprint arXiv:2304.10888_ , 2023. 

- [3] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [4] L. Ma, Z. Meng, T. Liu, Y. Li, R. Song, W. Zhang, and S. Huang, “Styleloco: Generative adversarial distillation for natural humanoid robot locomotion,” _arXiv preprint arXiv:2503.15082_ , 2025. 

- [5] H. Yao, Z. Song, B. Chen, and L. Liu, “Controlvae: Model-based learning of generative controllers for physics-based characters,” _ACM Transactions on Graphics (TOG)_ , vol. 41, no. 6, pp. 1–16, 2022. 

- [6] H. Yao, Z. Song, Y. Zhou, T. Ao, B. Chen, and L. Liu, “Moconvq: Unified physics-based motion control via scalable discrete representations,” _ACM Transactions on Graphics (TOG)_ , vol. 43, no. 4, pp. 1–21, 2024. 

- [7] S. Ross, G. Gordon, and D. Bagnell, “A reduction of imitation learning and structured prediction to no-regret online learning,” in _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , 2011. 

- [8] I. Kato, “Development of wabot 1,” _Biomechanism_ , vol. 2, pp. 173–214, 1973. 

- [9] H. Miura and I. Shimoyama, “Dynamic walk of a biped,” _IJRR_ , 1984. 

- [10] K. Hirai, M. Hirose, Y. Haikawa, and T. Takenaka, “The development of honda humanoid robot,” in _Proceedings. 1998 IEEE international conference on robotics and automation (Cat. No. 98CH36146)_ , vol. 2. IEEE, 1998, pp. 1321–1326. 

- [11] Y. Ishiguro, K. Kojima, F. Sugai, S. Nozawa, Y. Kakiuchi, K. Okada, and M. Inaba, “High speed whole body dynamic motion experiment with real time master-slave humanoid robot system,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , 2018, pp. 5835–5841. 

- [12] J. Ramos and S. Kim, “Dynamic locomotion synchronization of bipedal robot and human operator via bilateral feedback teleoperation,” _Science Robotics_ , vol. 4, no. 35, p. eaav4282, 2019. 

- [13] F.-J. Montecillo-Puente, M. N. Sreenivasa, and J.-P. Laumond, “On realtime whole-body human to humanoid motion transfer,” in _International Conference on Informatics in Control, Automation and Robotics_ , 2010. [Online]. Available: https://api.semanticscholar.org/CorpusID:20676844 

- [14] J. Koenemann, F. Burget, and M. Bennewitz, “Real-time imitation of human whole-body motions by humanoids,” in _2014 IEEE International Conference on Robotics and Automation (ICRA)_ , 2014, pp. 2806–2812. 

- [15] O. E. Ramos, N. Mansard, O. Stasse, C. Benazeth, S. Hak, and L. Saab, “Dancing humanoid robots: Systematic use of osid to compute dynamically consistent movements following a motion capture pattern,” _IEEE Robotics and Automation Magazine_ , vol. 22, no. 4, pp. 16–26, 2015. 

- [16] E. R. Westervelt, J. W. Grizzle, and D. E. Koditschek, “Hybrid zero dynamics of planar biped walkers,” _IEEE transactions on automatic control_ , vol. 48, no. 1, pp. 42–56, 2003. 

- [17] B. Dariush, M. Gienger, B. Jian, C. Goerick, and K. Fujimura, “Whole body humanoid control from human motion descriptors,” in _2008 IEEE International Conference on Robotics and Automation_ . IEEE, 2008, pp. 2677–2684. 

- [18] S. Kajita, F. Kanehiro, K. Kaneko, K. Yokoi, and H. Hirukawa, “The 3d linear inverted pendulum mode: A simple modeling for a biped walking pattern generation,” in _Proceedings 2001 IEEE/RSJ International Conference on Intelligent Robots and Systems. Expanding the Societal Role of Robotics in the the Next Millennium (Cat. No. 01CH37180)_ , vol. 1. IEEE, 2001, pp. 239–246. 

- [19] M. Hutter, C. Gehring, D. Jud, A. Lauber, C. D. Bellicoso, V. Tsounis, J. Hwangbo, K. Bodie, P. Fankhauser, M. Bloesch, _et al._ , “Anymal-a highly mobile and dynamic quadrupedal robot,” in _IROS_ , 2016. 

- [20] K. Darvish, Y. Tirupachuri, G. Romualdi, L. Rapetti, D. Ferigo, F. J. A. Chavez, and D. Pucci, “Whole-body geometric retargeting for humanoid robots,” in _2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids)_ , 2019, pp. 679–686. 

- [21] L. Penco, N. Scianca, V. Modugno, L. Lanari, G. Oriolo, and S. Ivaldi, “A multimode teleoperation framework for humanoid loco-manipulation: An application for the icub robot,” _IEEE Robotics and Automation Magazine_ , vol. 26, no. 4, pp. 73–82, 2019. 

- [22] J. Ramos and S. Kim, “Dynamic locomotion synchronization of bipedal robot and human operator via bilateral feedback teleoperation,” _Science Robotics_ , vol. 4, no. 35, p. eaav4282, 2019. [Online]. Available: https://www.science.org/doi/abs/10.1126/scirobotics.aav4282 

- [23] Y. Ishiguro, T. Makabe, Y. Nagamatsu, Y. Kojio, K. Kojima, F. Sugai, Y. Kakiuchi, K. Okada, and M. Inaba, “Bilateral humanoid teleoperation system using whole-body exoskeleton cockpit tablis,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6419–6426, 2020. 

- [24] L. Penco, K. Momose, S. McCrory, D. Anderson, N. Kitchel, D. Calvert, and R. J. Griffin, “Mixed reality teleoperation assistance for direct control of humanoids,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 2, pp. 1937–1944, 2024. 

- [25] F. L. Moro and L. Sentis, “Whole-body control of humanoid robots,” _Humanoid Robotics: A reference, Springer, Dordrecht_ , 2019. 

- [26] G. Romualdi, S. Dafarra, G. L’Erario, I. Sorrentino, S. Traversaro, and D. Pucci, “Online non-linear centroidal mpc for humanoid robot locomotion with step adjustment,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022, pp. 10 412–10 419. 

- [27] J. Englsberger, A. Dietrich, G.-A. Mesesan, G. Garofalo, C. Ott, and A. O. Albu-Sch¨affer, “Mptc-modular passive tracking controller for stack of tasks based control frameworks,” _16th Robotics: Science and Systems, RSS 2020_ , 2020. 

- [28] M. Elobaid, G. Romualdi, G. Nava, L. Rapetti, H. A. O. Mohamed, and D. Pucci, “Online non-linear centroidal mpc for humanoid robots payload carrying with contact-stable force parametrization,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 12 233–12 239. 

8 

- [29] M. Chignoli, D. Kim, E. Stanger-Jones, and S. Kim, “The mit humanoid robot: Design, motion planning, and control for acrobatic behaviors,” in _2020 IEEE-RAS 20th International Conference on Humanoid Robots (Humanoids)_ . IEEE, 2021, pp. 1–8. 

- [30] A. Dallard, M. Benallegue, F. Kanehiro, and A. Kheddar, “Synchronized human-humanoid motion imitation,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 7, pp. 4155–4162, 2023. 

- [31] X. B. Peng, E. Coumans, T. Zhang, T.-W. Lee, J. Tan, and S. Levine, “Learning agile robotic locomotion skills by imitating animals,” Apr. 2020. 

- [32] A. Kumar, Z. Fu, D. Pathak, and J. Malik, “Rma: Rapid motor adaptation for legged robots,” _arXiv preprint arXiv:2107.04034_ , 2021. 

- [33] Z. Fu, A. Kumar, J. Malik, and D. Pathak, “Minimizing energy consumption leads to the emergence of gaits in legged robots,” _Conference on Robot Learning (CoRL)_ , 2021. 

- [34] J. Siekmann, K. Green, J. Warila, A. Fern, and J. Hurst, “Blind bipedal stair traversal via sim-to-real reinforcement learning,” _arXiv preprint arXiv:2105.08328_ , 2021. 

- [35] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” in _Conference on Robot Learning (CoRL)_ , 2023. 

- [36] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” _arXiv preprint arXiv:2309.14341_ , 2023. 

- [37] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv preprint arXiv:2502.10363_ , 2025. 

- [38] X. Cheng, A. Kumar, and D. Pathak, “Legs as manipulator: Pushing quadrupedal agility beyond locomotion,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [39] S. Jeon, M. Jung, S. Choi, B. Kim, and J. Hwangbo, “Learning whole-body manipulation for quadrupedal robot,” _arXiv preprint arXiv:2308.16820_ , 2023. 

- [40] C. Schwarke, V. Klemm, M. Van der Boon, M. Bjelonic, and M. Hutter, “Curiosity-driven learning of joint locomotion and manipulation tasks,” in _Proceedings of The 7th Conference on Robot Learning_ , vol. 229. PMLR, 2023, pp. 2594–2610. 

- [41] Y. Ji, G. B. Margolis, and P. Agrawal, “Dribblebot: Dynamic legged manipulation in the wild,” _arXiv preprint arXiv:2304.01159_ , 2023. 

- [42] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , pp. 1–14, 2018. 

- [43] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Trans. Graph._ , vol. 40, no. 4, July 2021. [Online]. Available: http://doi.acm.org/10.1145/3450626.3459670 

- [44] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Largescale reusable adversarial skill embeddings for physically simulated characters,” _ACM Trans. Graph._ , vol. 41, no. 4, July 2022. 

- [45] C. Tessler, Y. Kasten, Y. Guo, S. Mannor, G. Chechik, and X. B. Peng, “Calm: Conditional adversarial latent models for directable virtual characters,” in _ACM SIGGRAPH 2023 Conference Proceedings_ , ser. SIGGRAPH ’23. New York, NY, USA: Association for Computing Machinery, 2023. [Online]. Available: https://doi.org/10.1145/3588432. 3591541 

- [46] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for robust parameterized locomotion control of bipedal robots,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2021, pp. 2811–2817. 

- [47] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control,” _arXiv preprint arXiv:2401.16889_ , 2024. 

- [48] I. Radosavovic, T. Xiao, B. Zhang, T. Darrell, J. Malik, and K. Sreenath, “Real-world humanoid locomotion with reinforcement learning,” _arXiv:2303.03381_ , 2023. 

- [49] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [50] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath, “Robust and versatile bipedal jumping control through multi-task reinforcement learning,” _arXiv preprint arXiv:2302.09450_ , 2023. 

- [51] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” _arXiv preprint arXiv:2502.08378_ , 2025. 

- [52] Y. Jiang, T. Zhang, D. Ho, Y. Bai, C. K. Liu, S. Levine, and J. Tan, “Simgan: Hybrid simulator identification for domain adaptation via adversarial reinforcement learning,” in _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , 2021, pp. 2884–2890. 

- [53] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [54] A. Agarwal, A. Kumar, J. Malik, and D. Pathak, “Legged locomotion in challenging terrains using egocentric vision,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 403–415. 

- [55] R. Yang, G. Yang, and X. Wang, “Neural volumetric memory for visual locomotion control,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 1430–1440. 

- [56] H. Duan, B. Pandit, M. S. Gadde, B. J. van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” _arXiv preprint arXiv:2309.14594_ , 2023. 

- [57] H. Y. Ling, F. Zinno, G. Cheng, and M. Van De Panne, “Character controllers using motion vaes,” _ACM Transactions on Graphics (TOG)_ , vol. 39, no. 4, pp. 40–1, 2020. 

- [58] J. Won, D. Gopinath, and J. Hodgins, “Physics-based character controllers using conditional vaes,” _ACM Trans. Graph._ , vol. 41, no. 4, July 2022. [Online]. Available: https://doi.org/10.1145/3528223. 3530067 

- [59] J. Ho and S. Ermon, “Generative adversarial imitation learning,” _Advances in neural information processing systems_ , vol. 29, 2016. 

- [60] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [61] Q. Zhu, H. Zhang, M. Lan, and L. Han, “Neural categorical priors for physics-based character control,” 2023. [Online]. Available: https://arxiv.org/abs/2308.07200 

- [62] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “Maskedmimic: Unified physics-based character control through masked motion inpainting,” _ACM Transactions on Graphics (TOG)_ , 2024. 

- [63] Y. Fuchioka, Z. Xie, and M. Van de Panne, “Opt-mimic: Imitation of optimized trajectories for dynamic quadruped behaviors,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 5092–5098. 

- [64] X. Huang, Y. Chi, R. Wang, Z. Li, X. B. Peng, S. Shao, B. Nikolic, and K. Sreenath, “Diffuseloco: Real-time legged locomotion control with diffusion from offline datasets,” 2024. [Online]. Available: https://arxiv.org/abs/2404.19264 

- [65] H. Shi, T. Li, Q. Zhu, J. Sheng, L. Han, and M. Q. H. Meng, “An efficient model-based approach on learning agile motor skills without reinforcement,” 2024. [Online]. Available: https: //arxiv.org/abs/2403.01962 

- [66] P. Dugar, A. Shrestha, F. Yu, B. van Marum, and A. Fern, “Learning multi-modal whole-body control for real-world humanoid robots,” 2024. [Online]. Available: https://arxiv.org/abs/2408.07295 

- [67] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” 2024. [Online]. Available: https://arxiv.org/abs/2402.16796 

- [68] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning,” 2024. [Online]. Available: https://arxiv.org/abs/2406.08858 

- [69] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” in _arXiv_ , 2024. 

- [70] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, C. Liu, G. Shi, X. Wang, L. Fan, and Y. Zhu, “Hover: Versatile neural whole-body controller for humanoid robots,” _arXiv preprint arXiv:2410.21229_ , 2024. 

- [71] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” 2024. [Online]. Available: https://arxiv.org/abs/2406.10454 

- [72] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik, “Humanoid locomotion as next token prediction,” _arXiv:2402.19469_ , 2024. 

- [73] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. M. Kitani, and W. Xu, “Universal humanoid motion representations for physicsbased control,” in _The Twelfth International Conference on Learning Representations_ , 2024. [Online]. Available: https://openreview.net/ forum?id=OrOd8PxOO2 

- [74] J. Wang, J. Hodgins, and J. Won, “Strategy and skill learning for physicsbased table tennis animation,” in _ACM SIGGRAPH 2024 Conference Papers_ , 2024, pp. 1–11. 

- [75] A. Serifi, R. Grandia, E. Knoop, M. Gross, and M. B¨acher, “Robot motion diffusion model: Motion generation for robotic characters,” in _SIGGRAPH Asia 2024 Conference Papers_ , ser. SA ’24. New York, 

9 

NY, USA: Association for Computing Machinery, 2024. [Online]. Available: https://doi.org/10.1145/3680528.3687626 

- [76] X. B. Peng, E. Coumans, T. Zhang, T.-W. E. Lee, J. Tan, and S. Levine, “Learning agile robotic locomotion skills by imitating animals,” in _Robotics: Science and Systems_ , 07 2020. 

- [77] A. van den Oord, O. Vinyals, and K. Kavukcuoglu, “Neural discrete representation learning,” in _Proceedings of the 31st International Conference on Neural Information Processing Systems_ , ser. NIPS’17. Red Hook, NY, USA: Curran Associates Inc., 2017, p. 6309–6318. 

- [78] F. Wu, X. Nal, J. Jang, W. Zhu, Z. Gu, A. Wu, and Y. Zhao, “Learn to teach: Sample-efficient privileged learning for humanoid locomotion over diverse terrains,” 2025. [Online]. Available: https: //arxiv.org/abs/2402.06783 

- [79] H. Wang, H. Luo, W. Zhang, and H. Chen, “Cts: Concurrent teacher-student reinforcement learning for legged locomotion,” 2024. [Online]. Available: https://arxiv.org/abs/2405.10830 

- [80] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [81] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal, “Robust motion in-betweening,” _ACM Trans. Graph._ , vol. 39, no. 4, Jul 2020. 

- [82] Unitree Robotics, “Unitree robotics: Open-source embodied intelligence datasets and models from unitree robotics,” https://huggingface.co/ unitreerobotics, 2025, accessed: 2025-04-28. 

- [83] unitreerobotics, “Unitree RL GYM,” https://github.com/unitreerobotics/ unitree <u>rl gym, 2025, a repository for reinforcement learning implemen-</u> tation based on Unitree Go2, H1, H1 <u>2, and G1. Accessed: 2025-04-30.</u> 

- [84] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li, “On the continuity of rotation representations in neural networks,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2019, pp. 5745–5753. 

## APPENDIX A DATASET 

We provide here additional details on our locomotion data usage. We source our reference motions from the LaFAN1 [81], using its version retargeted to the G1 robot’s kinematic model as provided by Unitree [82]. Table III details the composition of our dataset, which comprises walking and running sequences as well as the transitions between these two gaits. Figure 5 demonstrates the data distribution of our selected subset: here “data distribution” refers to the histograms of joint-angle values counted across all frames. A striking feature is that several key joints (notably the ankle, elbow, and knee) exhibit strongly non-Gaussian, often multimodal distributions rather than the unimodal, symmetric shapes one would expect under a normal assumption. This observation motivated our decision to forgo a VAE-based latent model, which typically assumes Gaussian priors in favor of a more flexible representation capable of capturing arbitrary, multimodal density profiles. We further selected some motions that do not involve self-collision and use this small set to conduct ablation study, including walking, crouching, turning around, and pacing. Table IV details the composition of our dataset for ablation study. We manually designed two reference motion sequences: one for walking straight forward and one for crouching walk straight forward. Both sequences were created by looping a single gait cycle and have been deployed on the real robot, with the walking-straight-forward sequence also used in an ablation study. 

## APPENDIX B 

TABLE III: Composition of Used LaFAN1 Dataset 

|Name|Frames|Seconds|
|---|---|---|
|walk2<br>subject4|7146|238.2|
|walk2<br>subject3|7146|238.2|
|walk3<br>subject2|7399|246.63|
|walk1<br>subject5|7840|261.33|
|walk2<br>subject1|7146|238.2|
|walk1<br>subject1|7840|261.33|
|walk3<br>subject5|7399|246.63|
|walk4<br>subject1|4918|163.93|
|walk1<br>subject2|7840|261.33|
|walk3<br>subject3|7399|246.63|
|Sum Walk|72073|2402.43|
|run2<br>subject4|7345|244.83|
|run1<br>subject5|7135|237.83|
|run2<br>subject1|7345|244.83|
|run1<br>subject2|7135|237.83|
|Sum Run|28960|965.33|


## TABLE IV: Composition of Ablation Dataset 

|Name|Frames|Seconds|
|---|---|---|
|walk1<br>subject1<br>100<br>1170|1070|35.67|
|walk1<br>subject5<br>5740<br>6830|1090|36.3|
|walk1<br>subject5<br>80<br>1715|1635|54.5|
|walk1<br>subject1<br>2460<br>3680|1220|40.67|
|walk3<br>subject5<br>320<br>1410|1090|36.3|
|Sum Train|6105|203.5|
|walk1<br>subject1<br>2480<br>2591|111|3.7|
|walk1<br>subject1<br>2657<br>3117|460|15.33|
|walk1<br>subject1<br>5344<br>5772|428|14.27|
|walk<br>straight(hand crafted)|1590|53|
|Sum Test|2589|86.3|


to represent information: global space and local space. For world model training, skill embedding learning, and teacher policy training, all calculations are performed in the global space. In contrast, student policy learning operates entirely in the local space. We maintain two separate state history buffers to store information in different spaces, and teacher and student policies can observe different numbers of history frames. Notably, we only feed the goal of the current frame to the policy, as providing goal history may degrade generative capability. Generally, observation at timestep _t_ is given by 


where _H_ means number of observed history frames, _gt_ means tracking target _mt_ in tracking policy while None in random sample mode. 

_a) Global Space:_ The humanoid is modeled as articulated rigid bodies with a floating root. A global state is defined as 


where _B_ denotes the set of links including the floating root. We express it in the root heading frame as 


## OBSERVATION SPACE 

The observation space of MuGen consists of two components: state and goal. We adopt two distinct coordinate spaces 

with the transformation 


10 


Fig. 5: Data Distribution 

Rotations are represented using the 6D continuous format from [84]. After this transformation, at each timestep, the state (¯ _xi,_ ¯ _qi,_ ¯ _vi,_ ¯ _ωi_ ) has shape ( _N_ body _,_ 3 + 6 + 3 + 3), corresponding to body position, body orientation (6D), linear velocity, and angular velocity. States and reference motions in global space encompass privileged information that is typically inaccessible to onboard sensing. 

_b) Local Space:_ The local observation space reflects the sensing limitations of real robots, where privileged information such as root height and global velocity is inaccessible. A local state is defined as 

## _s_<sup>proprioception</sup> = _{g, w} ∪{qj, dqj}j∈J ,_ 

where _J_ denotes the set of activated joints. Available observations include projected gravity _g_ , body angular velocity _w_ , and per-joint positions _q_ and velocities _dq_ relative to their parent joints. Combining these components, the local state for a single frame has shape (3 + 3 + _N_ joint _×_ 2 _,_ ). States and reference motions represented in local space contain only information realistically obtainable by onboard sensors. 

## APPENDIX C 

epoch _< ms_ 2), both teacher and student policies are trained, but only the teacher is used to generate rollouts. This helps the student gain a stable imitation target. Third, in the _distillation_ phase ( _ms_ 2 _<_ epoch _< ms_ 3), control is gradually handed over to the student policy using a linear annealing strategy that mixes teacher and student actions within each trajectory, enabling smooth policy transition without full dependence on DAgger-style aggregation. An optional _post-training_ phase (epoch _> ms_ 3) further adapts the student policy to selected reference motions for improved real-world robustness. The full procedure is detailed in Algorithm 1. In each training step, we update the modules (world model, teacher policy, and student policy) by sampling trajectory clips and computing the corresponding objective functions as described in Section III. Since we operate in two distinct information spaces—global and local, we store trajectory data for both spaces separately. During the joint training of the world model, codebook, and teacher policy, we sample only global space trajectories from the replay buffer. In contrast, during the distillation phase, we sample both global and local trajectories, as the student policy requires demonstrations from the teacher, which operates in the global space. 

## DOMAIN RANDOMIZATION 

To improve the robustness of the trained policy, we employ domain randomization to simulate several kinds of random noises that may occur while deploying in the real world. The terms used for randomization, along with their descriptions and ranges, are listed in TableV. 

## APPENDIX D PSEUDO CODE 

We show our pseudo-code for training MuGen in Algorithm 1 and Algorithm 2. MuGen is trained through a staged pipeline comprising three core phases and one optional refinement step. First, during _pretraining_ (epoch _< ms_ 1), the teacher policy explores the motion space and builds the latent skillset in the VQ codebook, jointly optimized with the world model. Second, in the _warming-up_ phase ( _ms_ 1 _<_ 

## APPENDIX E NETWORK STRUCTURE 

Our architecture consists of four main components: a shared vector-quantised (VQ) bottleneck _B_ , an encoder _E_ to process embedded information, a policy decoder _D_ that outputs actions from the discrete quantized latent code, and a world model _W_ serving as a differentiable simulator. Together, Emb and _E_ form the latent extractor, as illustrated in Figure 2. The teacher and student policies share almost identical network architectures, differing only slightly in input dimensionality. 

We first flatten the input states and pass them through an embedding layer Emb _s_ . The target goal for a single frame is separately embedded via Emb _g_ . These two embeddings are concatenated and then fed into the encoder _E_ to produce a latent representation in a continuous latent space. The decoder _D_ then processes the vector-quantized skill embedding searched 

11 

TABLE V: Randomization Terms, Description, and Ranges 

|Term|Description|Ranges|
|---|---|---|
|Friction coefficient (_−_)|Random friction coefficients applied to robot’s links|[0_._60_,_1_._00]|
|Torso payload mass (_Kg_)|Additional random mass attached to the torso links|[_−_2_._00_,_2_._00]|
|_Kp_ (_−_)|Random scaling factors applied to the proportional gain (_Kp_) of the robot’s joints|[0_._90_,_1_._10]|
|_Kd_ (_−_)|Random scaling factors applied to the derivative gain (_Kd_) of the robot’s joints|[0_._90_,_1_._10]|
|Dof pos obs (_rad_)|Random dof velocity added to the observation of joint positions|[_−_0_._05_,_0_._05]|
|Dof vel obs (_rad/s_)|Random dof velocity added to the observation of joint velocities|[_−_0_._50_,_0_._50]|
|Ang vel obs (_rad/s_)<br>|Random dof velocity added to the observation of body angular velocities|[_−_0_._50_,_0_._50]|
|Gravity obs (_m/s_<sup>2</sup>)|Random dof velocity added to the observation of gravities projected to robot’s body frame|[_−_0_._05_,_0_._05]|


TABLE VI: Hyperparameters, Description, and Value 

|Term|Description|Value|
|---|---|---|
|num<br>envs|number of parallel environment|1024|
|_T_|maximum episode length in single rollout trajectory|1500|
|_Tm_|length of sampled reference motion clip|120|
|FPS|Frames Per Second of simulation, reference motion, and control signal|30|
|Substep|substep of simulation within each control step|6|
|buff<br>len|maximum length of replay buffer|256|
|_h_0<br>|height threshold for termination: episode terminates when any non-foot link’s vertical position falls below this value|0.2 m|
|_BS_<sup>_W_</sup><br>|Batch Size for training world model|512|
|_BS_<sup>_T_</sup><br>|Batch Size for training teacher policy|1024|
|_BS_<sup>_S_</sup>|Batch Size for training student policy|1024|
|_l_<sup>_W_</sup><br>|replay clip length for training world model|24|
|_l_<sup>_T_</sup><br>|replay clip length for training teacher policy|24|
|_l_<sup>_S_</sup>|replay clip length for training student policy|32|
|lr|learning rate|2e-4|
|_γ_|discount factor|1|
|_WW_|weight of state component(position, rotation, velocity, angular) loss for training world model|[2,1,10,5]|
|_WT_|weight of state component(position, rotation, velocity, angular) loss for training teacher policy|[2,1,0.5/3,0.5/3]*0.1|
|_β_1|weight of commitment loss|0.05|
|_β_2|weight of smooth action loss|0.01|
|_β_3|weight of action L2-norm penalty loss|0.001|
|_β_4|weight of align loss|1|


from codebook _B_ to produce a latent action, which is further passed through two small linear layers to predict the mean ( _µ_ ) and standard deviation ( _σ_ ) of the action distribution. 

## APPENDIX F 

## ABLATION BASELINES 

Here we give more detailed information of our baselines in Table I. 

**VQ-based w/o history:** This model shares the exact architecture with our full MuGen model, except that it does not use historical states in the observation (i.e., #HT = #HS = 0). This ablation helps evaluate the impact of temporal context in the input representation. 

**VAE-based w/o history:** In this variant, we remove the vector quantization codebook and instead apply a KullbackLeibler (KL) divergence loss to the continuous latent variable _z_ , encouraging it to follow a standard normal distribution. All other components remain identical to the ’VQ-based w/o history’ model. 

4.4. The pipeline consists of three main stages: (1) _Motion export_ : the simulated trajectory, including link positions and orientations, is exported from Isaac Gym at 30 Hz and saved in .npy format; (2) _Scene construction_ : the robot’s 3D geometry in .stl format is imported into Blender, where the scene is assembled based on XML descriptors. Materials, lighting, and camera parameters are configured for photorealism; (3) _Animation scripting_ : the exported motion is mapped onto Blender’s rigged model via Python scripts, where transformation matrices are applied frame-by-frame and converted into animation keyframes. This pipeline allows us to generate consistent visualizations for simulated trajectories, enabling direct qualitative comparison and clearer demonstration of motion quality. 

**MLP baseline:** As a baseline, we use a standard MLPbased model with the same architecture as the ’VAE-based w/o history’ variant, but without any KL regularization. 

## APPENDIX G 

## VISUALIZATION 

To visualize the kinematic behavior of our system, we construct a high-fidelity rendering pipeline based on Blender 

12 

## **Algorithm 1:** Train MuGen 

**Function Train** ( ) **:** Hyperparameters: milestones _ms_ = [ _ms_ 1 _, ms_ 2 _, ms_ 3], max expisode length _T_ , reference motion clip length _Tm_ , trajectory clip length _lW_ , _lT_ , _lS_ Initialize: teacher policy _π_<sup>T</sup> = _E_<sup>T</sup> _, B, D_<sup>T</sup> , student policy _π_<sup>S</sup> = _E_<sup>S</sup> _, D_<sup>S</sup> , shared codebook _B_ , world model _W_ , trajectory buffer Buff _←_ ∅, epoch counter _e ←_ 0 **while** training **do** // collect simulation trajectories Remove the oldest _NB_<sup>_′_simulationtuplesfrom</sup> Buff **while** _|Buff| < NB_ **do** Select _τ_ ˜ = _{_ ˜ _m_ 0 _, m_ ˜ 1 _, . . . , m_ ˜ _T }_ from D _τ ←_ **TakeOver** ( _τ_ ˜, _m_ ˜ 0, _T_ , _π_<sup>T</sup> , _π_<sup>S</sup> , _B_ ) Store _τ_ and _τ_ ˜ in Buff **end if** _e < ms_ 2 **then TrainWorldModel** ( _W_ , _l_ , Buff) **TrainTeacher** ( _W_ , _π_<sup>T</sup> , _B_ , _l_ , Buff) **end if** _e > ms_ 1 **then TrainStudent** ( _π_<sup>T</sup> , _π_<sup>S</sup> , _B_ , _l_ , Buff) **end end end Function TakeOver** ( _τ_ ˜, _s_ 0, _T_ , _π_<sup>T</sup> , _π_<sup>S</sup> , _B_ ) **:** _t ←_ 0 **while** not terminated _and t < T_ **do if** _e < ms_ 2 **then** _P ←_ 1 **else if** _e > ms_ 3 **then** _P ←_ 0 **else** _P ←_ 1 _−_ ( _e − ms_ 2) _/_ ( _ms_ 3 _− ms_ 2) **end** Randomly select policy _π_ with probability _p_ ( _π_<sup>T</sup> ) = _P_ and _p_ ( _π_<sup>S</sup> ) = 1 _− P_ Extract _m_ ˜<sup>_t_</sup> from _τ_ ˜ Sample _at ∼ π_ ( _at|st, m_ ˜ _t, B_ ) by **Policy** ( _at|st, m_ ˜ _t, B_ ) _st_ +1 _←_ Simulate( _st_ , _at_ ) _t ← t_ + 1 **if** _run out of reference motion clip_ **then** Resample _τ_ ˜ = _{_ ˜ _m_ 0 _, m_ ˜ 1 _, . . . , m_ ˜<sup>_T_</sup> _m_<sup>_}_fromD</sup> **end end** Return _τ_ = _{s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, . . . , }_ 

**Algorithm 2:** Train Step for world model, teacher <u>policy,</u> and student <u>policy</u> 

**Function TrainWorldModel** ( _W_ , _T_ , Buff ) **:** Sample _τ_<sup>_∗_</sup> = _{s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, . . . , , sT , aT }_ from Buff, ignore _τ_ ˜<sup>_∗_</sup> _s_ ¯0 _← s_ 0 **for** _t ←_ 0 **to** _T_ **do** _s_ ¯ _t_ +1 _←W_ (¯ _st, at_ ) **end** Cache _τ_ = _{s_ 0 _, s_ 1 _, . . . , sT }_ Cache _τ_ ¯ = _{s_ ¯0 _,_ ¯ _s_ 1 _, . . . ,_ ¯ _sT } L ←L_ w(¯ _τ, τ_<sup>_∗_</sup> ) Update _W_ with _L_ w 

**end** 

**Function TrainTeacher** ( _W_ , _π_ , _B_ , _T_ , Buff) **:** Sample _τ_<sup>_∗_</sup> = _{s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, . . . , , sT , aT }_ and _τ_ ˜<sup>_∗_</sup> = _{_ ˜ _m_ 0 _, m_ ˜ 1 _, . . . , m_ ˜ _T }_ from Buff _s_ ¯0 _← s_ 0 **for** _t ←_ 0 **to** _T_ **do** Sample _a_ ¯ _t ∼ π_ ( _at|s_ ¯ _t, m_ ˜ _t, B_ ) _s_ ¯ _t_ +1 _←W_ (¯ _st,_ ¯ _at_ ) **end** Cache _τ_ ¯ = _{s_ ¯0 _,_ ¯ _a_ 0 _,_ ¯ _s_ 1 _,_ ¯ _a_ 1 _, . . . ,_ ¯ _sT ,_ ¯ _aT } L ←L_ rec(¯ _τ,_ ˜ _τ_<sup>_∗_</sup> ) + _βLkl_ (¯ _τ_ ) + _L_ act(¯ _τ_ ) Update _π_<sup>T</sup> _, B_ with _L_ **end Function TrainStudent** ( _π_<sup>T</sup> , _π_<sup>S</sup> , _B_ , _T_ , Buff) **:** Sample _τ_<sup>_∗_</sup> = _{s_<sup>0</sup> _, a_<sup>0</sup> _, s_<sup>1</sup> _, a_<sup>1</sup> _, . . . , , s_<sup>_T_</sup> _, a_<sup>_T_</sup> _}_ and _τ_ ˜<sup>_∗_</sup> = _{_ ˜ _m_<sup>0</sup> _, m_ ˜<sup>1</sup> _, . . . , m_ ˜<sup>_T_</sup> _}_ from Buff **for** _t ←_ 0 **to** _T_ **do** Sample _a_ ¯<sup>T</sup> _t_<sup>_∼π_T(</sup><sup>_at|s_T</sup> _t_<sup>_,m_˜</sup><sup>_t, B_)</sup> Sample _a_ ¯<sup>S</sup> _t_<sup>_∼π_S(</sup><sup>_at|s_S</sup> _t_<sup>_,m_˜</sup><sup>_t, B_)</sup> **end** Cache _τ_ ¯<sup>T</sup> = _{z_ ¯0<sup>T</sup><sup>_,_¯</sup><sup>_a_</sup> 0<sup>T</sup><sup>_,_¯</sup><sup>_z_</sup> 1<sup>T</sup><sup>_,_¯</sup><sup>_a_T</sup> 1<sup>_, . . . ,_¯</sup><sup>_z_</sup> _T_<sup>T</sup><sup>_,_¯</sup><sup>_a_T</sup> _T_<sup>_}_</sup> Cache _τ_ ¯<sup>S</sup> = _{z_ ¯0<sup>S</sup><sup>_,_¯</sup><sup>_a_S</sup> 0<sup>_,_¯</sup><sup>_z_</sup> 1<sup>S</sup><sup>_,_¯</sup><sup>_a_S</sup> 1<sup>_, . . . ,_¯</sup><sup>_z_</sup> _T_<sup>S</sup><sup>_,_¯</sup><sup>_a_S</sup> _T_<sup>_}_</sup> _L ←L_ rec(¯ _τ_<sup>S</sup> _,_ ¯ _τ_<sup>T</sup> ) Update _π_<sup>S</sup> with _L_ **end** 

**end Function Policy** ( _at|st, m_ ˜ _t, B_ ) **:** Sample _zt ∼E_ ( _zt|st, m_ ˜ T) Quantize _z_ ˆ _t ∼B_ ( _zt_ ) Sample _at ∼D_ ( _at|st,_ ˆ _zt_ ) **end** 

