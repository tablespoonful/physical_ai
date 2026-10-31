---
title: "SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation"
date: "2026-06-02"
authors: "Jeonguk Kang; Hanbyel Cho; Sanghyun Kang; Donghan Koo"
url: https://arxiv.org/abs/2606.03297
pdf: https://arxiv.org/pdf/2606.03297
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.03297)** / [論文ページ](https://arxiv.org/abs/2606.03297)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation** 

**Jeonguk Kang Hanbyel Cho Sanghyun Kang Donghan Koo** Future Robot AI Group, Samsung Electronics Page: https://splitadapter.github.io/ 


Figure 1: Real-world humanoid loco-manipulation experiments with the proposed method under diverse payload, pickup/placement-height, and object-interaction conditions. (a) Transport under different payload masses, including a 6 kg condition outside the training mass range. (b) Heavy-load (6 kg) transport under different pickup/placement heights (30 cm and 60 cm). (c) Generalization to varied object properties, including large boxes and acrylic boxes. (d) Human-object handover. 

**Abstract:** Humanoid loco-manipulation requires stable whole-body control under varying object masses and pickup/placement heights. This becomes particularly challenging in sim-to-real transfer, where object-induced load variation and robot-side dynamics mismatch interact during physical contact. Existing history-based adapters often compress these factors into a single latent representation, which can weaken robustness under heavy-load manipulation. We propose **SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation** , which freezes a pretrained box manipulation policy and extends it with object/load and dynamics-aware context encoders trained with split world-model objectives, GRL-based cross-adversarial regularization, and hierarchical Feature-wise Linear Modulation (FiLM). In sim-to-sim experiments and real-world deployment, SplitAdapter improves Full-task success over the base policy and world-model FiLM baselines across object masses of 2, 4, and 6 kg and pickup/placement heights of 0, 30, and 60 cm, with the largest improvements under heavy-load conditions. 

**Keywords:** Humanoid Loco-Manipulation, Sim-to-Real, Online Adaptation 

## **1 Introduction** 

Recent learning-based systems have demonstrated strong humanoid loco-manipulation capabilities [1, 2, 3, 4, 5, 6, 7, 8], but sim-to-real transfer remains difficult under payload variation and robot/environment dynamics mismatch. A heavier box or lower pickup height changes the required whole-body coordination, while actuator or dynamics mismatch can cause policies to behave differently on real hardware. 

Existing adaptation methods often encode recent observation history into a single latent representation through supervised extrinsics estimation [9], privileged-state reconstruction [10], or worldmodel prediction [11, 12, 13]. While effective for locomotion and disturbance adaptation, these approaches can mix load-related information with residual dynamics mismatch, limiting robustness under heavy-load transfer. 

We propose **SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation** , a factorized adaptation framework for humanoid box lifting, transport, and placement. Instead of retraining the full controller, SplitAdapter freezes a pretrained AMP [2]-style manipulation policy and learns factorized adaptation modules on top of it. The framework uses two context branches: an object/load branch that estimates object mass and loaded state while extracting object-related context, and a dynamics-aware branch that learns a dynamics-aware latent through robot-transition prediction. The two branches are trained with split world-model objectives and GRL [14]-based cross-adversarial regularization to reduce overlap between load-related and dynamics-related signals. The resulting context representations modulate the frozen policy through hierarchical Featurewise Linear Modulation (FiLM [15]). 

We validate SplitAdapter in MuJoCo [16] sim-to-sim experiments and real-world humanoid deployment under diverse object masses and pickup/placement heights. Compared with the base policy and world-model FiLM baselines, SplitAdapter improves Lift-up success and Full-task success, particularly under heavy-load conditions. 

In summary, our main contributions are: 

- We introduce SplitAdapter, a frozen-policy adaptation framework for humanoid box locomanipulation under payload and dynamics variations. 

- We propose a factorized adaptation structure that decomposes adaptation into object/load and dynamics-aware context using split world-model and GRL-based cross-adversarial separation. 

- We validate SplitAdapter in MuJoCo sim-to-sim transfer and real-world humanoid deployment, demonstrating improved heavy-load loco-manipulation across diverse object masses, pickup/placement heights, and interaction scenarios. 

## **2 Related Work** 

**Humanoid loco-manipulation and object interaction.** Early model-based approaches studied humanoid walking, multi-contact motion planning, and whole-body physical interaction using preview control, trajectory optimization, and hierarchical control [17, 18, 19]. More recent work has explored humanoid box loco-manipulation and heavy-object interaction through sim-to-real learning and optimization-based whole-body control [20, 21]. Learning-based humanoid-object interaction methods have further improved generalization and real-world performance. Wang et al. proposed PhysHSI for real-world humanoid-scene interaction with AMP-based policy learning and coarse-tofine perception [3]; He et al. introduced ULTRA, a unified multimodal controller for autonomous humanoid whole-body loco-manipulation [4]; Lin et al. proposed Pro-HOI with root-guided commands and persistent object estimation for long-horizon box carrying [5]; Zhao et al. introduced ResMimic, which adapts a pretrained general motion tracker with residual policies for object-aware loco-manipulation [6]; and Zhang et al. proposed FALCON for force-adaptive humanoid loco- 

2 

manipulation through upper- and lower-body decomposition [7]. Other recent systems study videobased interaction learning and demonstration-based generalization [22, 23, 24, 25, 26]. In contrast, SplitAdapter focuses on load-aware adaptation for heavy humanoid box manipulation through a frozen-policy adapter structure. 

**Sim-to-real transfer and world-model-based adaptation.** Online adaptation for legged robots often estimates latent environment parameters from recent history. Kumar et al. proposed RMA for rapid motor adaptation using estimated extrinsics [9], and later extended this idea to bipedal robots through A-RMA [27]. Li et al. further showed that history-based reinforcement learning can produce versatile and robust bipedal locomotion controllers that adapt to dynamics changes through input-output history [28]. Dynamics randomization and asymmetric actor–critic training are also widely used tools for deployable policies [29, 30]. World-model-based methods use prediction or reconstruction as auxiliary objectives for learning adaptation embeddings. Gu et al. proposed DWL to learn robust humanoid locomotion with denoising world-model learning [10], and Sun et al. proposed WMR to reconstruct privileged states for humanoid locomotion [11]. Li et al. studied neural dynamics models for robot policy optimization in RWM [12]. Zhang et al. used world-model prediction to learn adaptation embeddings for motion tracking under disturbances in Any2Track/AnyAdapter [13]. SplitAdapter follows this predictive-adaptation direction but separates object/load and robot-transition targets instead of compressing all adaptation factors into a single latent. We also use GRL-based adversarial regularization [14] to reduce information leakage between the two adaptation latents. 

## **3 Methodology** 

SplitAdapter is a load-aware factorized adaptation framework built on top of a frozen PhysHSI-style AMP-based humanoid box manipulation policy [3]. It estimates object/load and dynamics-aware contexts from recent interaction history and injects them into the frozen policy through hierarchical Feature-wise Linear Modulation (FiLM) [15]. 

### **3.1 Frozen Base Policy** 

We train the base policy with an AMP-based reinforcement learning framework for humanoid box manipulation, where target joint positions are executed by a low-level PD controller. After pretraining, the policy is frozen and only the adaptation modules are optimized. 

### **3.2 Dual-Context History Encoding** 

To avoid compressing object/load and robot-side dynamics effects into a single latent, SplitAdapter factorizes adaptation into object/load and dynamics-aware context branches. 

At time _t_ , the adapter observes a recent observation-action history 


where _H_ is the history length, and _ot_ and _at_ denote the policy observation and action. A shared history encoder first extracts a compact representation: 


SplitAdapter factorizes the history representation into two context branches. The object/load branch _f_ obj, implemented as the Task Head in Fig. 2, maps the shared history feature to an object/load latent, a mass estimate, and a loaded-state estimate, while the dynamics branch _f_ dyn maps the same feature to a dynamics-aware latent: 


Here, _z_ obj _,t_ and _z_ dyn _,t_ denote the object/load and dynamics-aware latents, and the effective payload estimate is defined as _m_ eff _,t_ = _ℓ_<sup>ˆ</sup> _t_ ˆ _mt_ . 

3 


Figure 2: SplitAdapter overview. A frozen humanoid manipulation policy is adapted with object/load and dynamics-aware context encoders. The resulting factorized latents are trained with split world-model objectives, regularized with GRL-based separation, and injected through hierarchical FiLM modulation. 

**Object/load context encoder.** The object/load branch produces _z_ obj _,t_ while explicitly estimating object mass and loaded state. Its supervised loss is 


An optional sparse regularizer is applied as 


**Dynamics-aware context encoder.** The dynamics-aware branch produces _z_ dyn _,t_ . We also apply an _L_ 1 regularizer: 


### **3.3 Split World Models** 

SplitAdapter uses world-model prediction as a proxy task for learning informative history embeddings, following the general idea of dynamics-aware adaptation in AnyAdapter [13]. Instead of using a single transition predictor, we split the prediction target into object transition and robot transition. 

**Object/load world model.** The object/load world model predicts the object delta transition: 


where _ot_ denotes the robot state used for transition prediction, and ∆ _p_<sup>obj</sup> _t_ and ∆ _Rt_<sup>obj</sup> denote the object position and orientation changes: 


The object/load world-model loss is 


4 

**Dynamics-aware world model.** The dynamics-aware world model predicts the next robot state: _o_ ˆ _t_ +1 = _W_ dyn( _ot, at, z_ dyn _,t, mt_ ) _._ (10) 

The corresponding loss is 


Both world models are conditioned on the estimated payload _m_ est _,t_ , which reduces the need for the latent variables to redundantly encode payload mass. As a result, _z_ obj _,t_ is encouraged to emphasize object/load-related interaction context, while _z_ dyn _,t_ is encouraged to emphasize residual dynamics/environment mismatch. 

### **3.4 GRL-Based Cross-Adversarial Separation** 

Although split world-model objectives encourage specialization, both context encoders share the same history feature _et_ . To further reduce information leakage, we introduce a GRL-based crossadversarial objective. We use _A_ obj _←_ dyn and _A_ robot _←_ obj to denote adversarial predictors from the dynamics-aware latent to the object target and from the object/load latent to the robot target, respectively. 

The first adversary predicts object transition from the dynamics-aware latent: 


Through the gradient reversal layer, _z_ dyn _,t_ is discouraged from encoding object/load transition information. The second adversary predicts robot transition from the object/load latent: 


This discourages _z_ obj _,t_ from encoding robot dynamics and environment mismatch, and together with the split world models promotes branch specialization. 

### **3.5 Hierarchical FiLM-Based Feature Modulation** 

SplitAdapter adapts the frozen base policy by modulating intermediate feature representations rather than directly perturbing the final action. For a hidden activation _h_ , Feature-wise Linear Modulation (FiLM) [15] applies 


where _γ_ ( _z_ ) and _β_ ( _z_ ) are feature-wise scale and bias terms generated from context latents. We apply hierarchical FiLM modulation across different layers of the frozen policy. As shown in the lower part of Fig. 2, object/load FiLM, generated from ( _z_ obj _,t, m_ est _,t_ ), modulates earlier layers to shape coarse task-level behavior, such as payload-conditioned lifting posture and whole-body coordination. In contrast, dynamics-aware FiLM, generated from _z_ dyn _,t_ , modulates later layers closer to the action head to compensate for dynamics and environment mismatch. This layer-dependent modulation allows the two adaptation factors to influence different levels of the frozen policy representation. The modulation layers are initialized to preserve the original frozen-policy behavior at the beginning of training, and adapter training uses the same reinforcement-learning objective and reward as the base policy. 

## **4 Experimental Results** 

We design experiments to answer three questions. **Q1** : Does factorized adaptation improve humanoid loco-manipulation performance under payload and pickup/placement-height variations? **Q2** : Does factorizing adaptation into object/load and dynamics-aware contexts outperform unified latent adaptation? **Q3** : Can the proposed method improve sim-to-real transfer under heavy-load conditions? 

5 

### **4.1 Simulation Evaluation** 

We use a frozen PhysHSI-style AMP-based box manipulation policy as the base policy. Training is performed in Isaac Gym [31], and all results are verified through MuJoCo-based sim-to-sim transfer. 

We compare the following methods: 

- **Base (PhysHSI [3])** : frozen base policy. 

- **AnyAdapter-style WM-FiLM** : world-model FiLM adapter following the AnyAdapter formulation [13] 

- **Ours w/o split latent** : proposed model without latent splitting. 

- **Ours w/o hierarchical FiLM** : proposed model without hierarchical FiLM. 

- **Ours w/o GRL** : proposed model without GRL. 

- **SplitAdapter** : full proposed method. 

We evaluate three object masses (2, 4, and 6 kg) and three pickup/placement heights (0, 30, and 60 cm). Each condition is evaluated over ten trials. We report **Lift-up success** and **Full-task success** counts. Here, **Full-task success** denotes successful completion of the entire sequence of approach, lift, transport, and placement. 

### **Performance Evaluation** 

Table 1: MuJoCo sim-to-sim Full-task success counts under object mass and pickup/placementheight variations. Each condition is evaluated over ten trials. Aggregate Full-task success and Lift-up success are summarized in the two rightmost columns. Cell colors indicate higher-ranked results within each column. The 6 kg, 0 cm setting is the most challenging case. 

|Method||2 kg|||4 kg|||6 kg||Full-task|Lift-up|
|---|---|---|---|---|---|---|---|---|---|---|---|
||0 cm|30 cm|60 cm|0 cm|30 cm|60 cm|0 cm|30 cm|60 cm|||
|_Baselines_||||||||||||
|Base (PhysHSI [3])|**10**|8|9|9|**10**|**10**|5|5|5|71/90|86/90|
|AnyAdapter-style WM-FiLM|**10**|**10**|9|9|9|**10**|4|6|8|75/90|86/90|
|_SplitAdapter variants_||||||||||||
|w/o split latent|**10**|9|**10**|9|**10**|9|6|**9**|**9**|81/90|88/90|
|w/o hierarchical FiLM|**10**|**10**|**10**|9|**10**|9|7|8|8|81/90|**90/90**|
|w/o GRL|**10**|8|**10**|**10**|**10**|**10**|8|**9**|**9**|84/90|**90/90**|
|**SplitAdapter**|**10**|**10**|**10**|9|**10**|**10**|**10**|**9**|**9**|**86/90**|**90/90**|


Table 1 shows that SplitAdapter improves overall task performance, with higher success rates not only across the in-distribution mass settings but also on the 6 kg condition beyond the training range. The advantage becomes clearer in the heavy load 6 kg regime, where stable transport and placement become substantially more difficult after lifting. In particular, although Lift-up success often remains high, the base policy and the AnyAdapter-style WM-FiLM baseline frequently lose postural stability during transport and fail before completing placement. In contrast, SplitAdapter maintains high success rates across all 6 kg pickup/placement-height variations, including the most challenging 6 kg, 0 cm condition. 

The performance gap between SplitAdapter and the baselines becomes more pronounced as object mass increases, indicating that the proposed adaptation is particularly effective under stronger loadinduced dynamics changes. Compared with the AnyAdapter-style WM-FiLM baseline, which uses a unified latent, SplitAdapter exhibits clearer mass-dependent organization in the latent space, as shown in Fig. 3 (a). This suggests that the factorized branch structure preserves load-related variation more distinctly. In addition, SplitAdapter directly uses the estimated mass and loaded state as adaptation signals, as shown in Fig. 4, which further helps the policy respond to changes in object weight. As illustrated in Fig. 3 (b), the proposed method generalizes across diverse goal directions, while the base policy often deviates from direct paths or fails due to load-induced disturbances. 

6 


Figure 3: Qualitative comparisons of the proposed and baseline methods. (a) t-SNE visualization of adaptation representations across object masses for the proposed split latent [ _z_ obj; _z_ dyn] and the unified latent baseline. (b) Box-transport trajectories for a 6 kg, 0 cm floor-lift task under multiple goal directions. The base policy (PhysHSI [3]) exhibits unstable transport, including failure cases and less direct paths to the target due to load-induced balance disturbances. 


Figure 4: Online mass and loaded-state estimation across two payload conditions. Both the estimated mass and loaded probability quickly converge to the ground truth after lifting. Soft and hard labels denote probabilistic and binary loaded-state targets, respectively. 

### **Effect of Latent Splitting and GRL** 

Among the SplitAdapter variants, removing latent splitting yields the lowest Full-task performance, especially in the 6 kg regime. This suggests that, even when mass and loaded-state information are provided, a unified latent tends to mix load-related information and dynamics-related signals, making it harder for the adapter to emphasize their different predictive roles. This interpretation is supported by Fig. 5 (a), where the factorized design yields lower world-model transition losses for both the object/load and robot-transition targets. 

Removing GRL causes a smaller but still consistent drop compared with the full model, suggesting that cross-adversarial regularization helps the two branches remain sufficiently specialized to better exploit the factorized adaptation structure. As shown in Fig. 5 (b), the predictability gap between matched-target and cross-target prediction becomes larger when GRL is used. Here, the predictability gap is defined as the difference in probe regression _R_<sup>2</sup> between the matched branch-target pair and the cross-branch pair for each transition target. Larger gaps indicate that the intended branch explains its assigned transition more strongly than the opposite branch. 

Removing hierarchical FiLM also reduces Full-task success relative to the full model, while preserving high Lift-up success. This pattern suggests that hierarchical FiLM is not critical for initiating the 

7 


Figure 5: (a) World-model transition losses with and without split designs. (b) Predictability gaps with and without GRL for object/load and robot/dynamics transitions. 

lift itself, but is beneficial for subsequent whole-body coordination during transport and placement under changing load conditions. 

### **4.2 Real-World Evaluation** 

We evaluate the Base policy and SplitAdapter on the Unitree G1 [32] under zero-shot real-world deployment. Each method is tested on 9 conditions with three trials per condition, without additional fine-tuning. 

Table 2: Real-world deployment results under object mass and pickup/placement-height variations. Each entry reports Full-task success over three trials, with Lift-up success shown in parentheses. 

|Method|0 cm|2 kg<br>30 cm|60 cm|0 cm|4 kg<br>30 cm|60 cm|0 cm|6 kg<br>30 cm|60 cm|Full-task|Lift-up|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Base (PhysHSI [3])|3 (3)|3 (3)|3 (3)|1 (2)|2 (3)|2 (2)|1 (2)|1 (3)|0 (1)|16/27 (59.3%)|22/27 (81.5%)|
|**SplitAdapter**|**3 (3)**|**3 (3)**|**3 (3)**|**3 (3)**|**3 (3)**|**3 (3)**|**2 (3)**|**3 (3)**|**3 (3)**|**26/27 (96.3%)**|**27/27 (100.0%)**|


Table 2 shows that the performance improvement observed in simulation transfers to the real robot under zero-shot deployment. The Base policy succeeds reliably in the lighter 2 kg conditions, but its performance deteriorates as object mass increases, yielding 16/27 Full-task successes and 22/27 Lift-up successes overall. In particular, the failure gap becomes more pronounced in the 6 kg settings, where the policy can still initiate lifting in several trials but frequently loses grasp stability, torso alignment, or whole-body balance before completing transport and placement. In contrast, SplitAdapter achieves 26/27 Full-task successes and 27/27 Lift-up successes, while remaining robust across all 4 kg conditions and nearly all 6 kg conditions. These results indicate that the proposed factorized adaptation improves not only Lift-up success but, more importantly, the stability of the subsequent transport and placement phases in real-world heavy-load deployment. 

## **5 Conclusion** 

We presented **SplitAdapter: Load-Aware Humanoid Loco-Manipulation via Factorized Adaptation** , a factorized adaptation framework for heavy-load humanoid box manipulation. SplitAdapter augments a frozen manipulation policy with object/load-aware and dynamics-aware context encoders, split world-model objectives, GRL-based regularization, and hierarchical FiLM modulation. Experimental results show improved robustness under mass and pickup/placement-height variations in both simulation and real-world deployment, particularly in the heaviest 6 kg setting. 

## **6 Limitations** 

While the proposed framework shows strong performance in simulation and real-world evaluation, several limitations remain. The current study focuses on rigid box lifting, transport, and placement, and does not address deformable objects or broader contact-rich manipulation scenarios. In addition, the scale of the real-world evaluation remains limited due to hardware cost and durability constraints under repeated heavy-load testing, since the Unitree G1 [32] arm payload is specified at approximately 3 kg per arm. 

8 

## **References** 

- [1] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne. DeepMimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions on Graphics, 37(4):1–14_ , 2018. 

- [2] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. AMP: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics, 40(4):1–20_ , 2021. 

- [3] H. Wang, W. Zhang, R. Yu, T. Huang, J. Ren, F. Jia, Z. Wang, X. Niu, X. Chen, J. Chen, Q. Chen, J. Wang, and J. Pang. PhysHSI: Towards a real-world generalizable and natural humanoid-scene interaction system. arXiv preprint arXiv:2510.11072, 2025. 

- [4] X. He, S. Xu, X. Li, R. Dong, L. Bian, Y.-X. Wang, and L.-Y. Gui. ULTRA: Unified multimodal control for autonomous humanoid whole-body loco-manipulation. arXiv preprint arXiv:2603.03279, 2026. 

- [5] Y. Lin, J. Shi, D. Wang, J. Kong, Y. Liu, C. Bai, and X. Li. Pro-HOI: Perceptive root-guided humanoid-object interaction. arXiv preprint arXiv:2603.01126, 2026. 

- [6] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning, 2025. URL `https://arxiv.org/abs/2510.05070` . 

- [7] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A. akbar Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. FALCON: Learning force-adaptive humanoid loco-manipulation. arXiv preprint arXiv:2505.06776, 2025. 

- [8] D. Li, X. Chen, Q. Wu, B. Chen, S. Wu, H. Wu, G. Zhang, L. Li, M. Zhou, D. Xiang, J. Ma, Q. Zhang, and R. Xu. HAIC: Humanoid agile object interaction control via dynamics-aware world model. arXiv preprint arXiv:2602.11758, 2026. 

- [9] A. Kumar, Z. Fu, D. Pathak, and J. Malik. RMA: Rapid motor adaptation for legged robots. In _Robotics: Science and Systems (RSS)_ , 2021. 

- [10] X. Gu, Y.-J. Wang, X. Zhu, C. Shi, Y. Guo, Y. Liu, and J. Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. arXiv preprint arXiv:2408.14472, 2024. 

- [11] W. Sun, L. Chen, Y. Su, B. Cao, Y. Liu, and Z. Xie. Learning humanoid locomotion with world model reconstruction. arXiv preprint arXiv:2502.16230, 2025. 

- [12] C. Li, A. Krause, and M. Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics. arXiv preprint arXiv:2501.10100, 2025. 

- [13] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, H. Liu, H. Wang, and L. Yi. Track any motions under any disturbances. arXiv preprint arXiv:2509.13833, 2025. 

- [14] Y. Ganin and V. Lempitsky. Unsupervised domain adaptation by backpropagation. In _Proceedings of the International Conference on Machine Learning (ICML)_ , 2015. 

- [15] E. Perez, F. Strub, H. de Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 32, 2018. 

- [16] E. Todorov, T. Erez, and Y. Tassa. MuJoCo: A physics engine for model-based control. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2012. 

9 

- [17] S. Kajita, F. Kanehiro, K. Kaneko, K. Fujiwara, K. Harada, K. Yokoi, and H. Hirukawa. Biped walking pattern generation by using preview control of zero-moment point. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2003. 

- [18] M. Murooka, K. Chappellet, A. Tanguy, M. Benallegue, I. Kumagai, M. Morisawa, F. Kanehiro, and A. Kheddar. Humanoid loco-manipulations pattern generation and stabilization control. _IEEE Robotics and Automation Letters, 6(3):5597–5604_ , 2021. 

- [19] F. Ruscelli, M. P. Polverini, A. Laurenzi, E. M. Hoffman, and N. G. Tsagarakis. A multicontact motion planning and control strategy for physical interaction tasks using a humanoid robot. In IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2020. 

- [20] J. Dao, H. Duan, and A. Fern. Sim-to-real learning for humanoid box loco-manipulation. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16930–16936, 2024. 

- [21] A. Rigo, M. Hu, S. K. Gupta, and Q. Nguyen. Hierarchical optimization-based control for whole-body loco-manipulation of heavy objects. In _IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15322–15328, 2024. 

- [22] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [23] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [24] S. Yin, Y. Ze, H.-X. Yu, C. K. Liu, and J. Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [25] S. Xu, H. Y. Ling, Y.-X. Wang, and L.-Y. Gui. InterMimic: Towards universal whole-body control for physics-based human-object interactions. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [26] Y. Fu, F. Xie, C. Xu, J. Xiong, H. Yuan, and Z. Lu. DemoHLM: From one demonstration to generalizable humanoid loco-manipulation. arXiv preprint arXiv:2510.11258, 2025. 

- [27] A. Kumar, Z. Li, J. Zeng, D. Pathak, K. Sreenath, and J. Malik. Adapting rapid motor adaptation for bipedal robots. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1161–1168, 2022. 

- [28] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _The International Journal of Robotics Research_ , 2024. 

- [29] X. B. Peng, M. Andrychowicz, W. Zaremba, and P. Abbeel. Sim-to-real transfer of robotic control with dynamics randomization. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2018. 

- [30] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel. Asymmetric actor critic for image-based robot learning. In _Robotics: Science and Systems (RSS)_ , 2018. 

- [31] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, et al. Isaac Gym: High performance GPU-based physics simulation for robot learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2021. 

- [32] Unitree. Humanoid agent AI avatar, 2024. URL `https://www.unitree.com/g1` . Accessed: 2026-05-22. 

10 

## **A Appendix** 

### **A.1 Observation and Reward Details** 

The frozen base policy follows the AMP-based locomotion framework of PhysHSI [3]. The policy outputs 29-D joint-position targets executed through low-level PD control. Here, we only summarize the task-specific observations and rewards used in our scenario. Entries marked with ‘*’ denote additions beyond PhysHSI [3]. 

**Task Observations.** The task-specific observation _o_<sup>_G_</sup> _t_<sup>_∈_R15comprises the following properties</sup> of the target box: 

- local box position _p_<sup>_o_</sup> _t_<sup>_∈_R3,</sup> 

- local box rotation _Rt_<sup>_o∈_R6,</sup> 

- box size _bt ∈_ R<sup>3</sup> , 

- local goal position _p_<sup>_g_</sup> _t_<sup>_∈_R3.</sup> 

The one-step policy observation has 123 dimensions, consisting of 108 proprioceptive dimensions and the 15-D task observation. The privileged critic observation has 126 dimensions, obtained by augmenting the actor-side observation with the 3-D base linear velocity. SplitAdapter additionally consumes a 50-step adaptation history<sup>_∗_</sup> of 123-D observations. 

**Task Rewards.** Following PhysHSI [3], the task reward is decomposed into approach, lift, relocation, and stabilization stages. We report only the active task-specific terms used in our experiments. The total task reward is 


Here, _dro_ , _dog_ , and _vro, vrg_ denote planar distances and projected velocities, and _ψro_<sup>_⋆, ψ_</sup> _rg_<sup>_⋆_denote</sup> desired yaw directions. As in PhysHSI [3], _rro,_ vel = exp( _−_ 5(0 _._ 85 _− vro_ )<sup>2</sup> ) and _rro,_ heading is the average pelvis/torso heading-alignment term. Likewise, _rt_<sup>carryup</sup> combines hand-position, handcontact, lift-height, and pelvis-alignment terms, while _rt_<sup>relocation</sup> combines commanded transport velocity, heading alignment, object-goal distance, and vertical placement. 


Our implementation further adds a hold-phase stabilization reward and a post-success stabilization reward: 


11 


Here, _rt_<sup>hand</sup> ~~f~~ ree rewards release after placement: it takes value 1 when neither hand remains in contact with the box, 0 _._ 5 when only one hand remains in contact, and 0 when both hands are still in contact. The only additional nonzero regularizers beyond PhysHSI [3] are `ankle` ~~`r`~~ `oll` ~~`c`~~ `lose`<sup>_∗_</sup> and `low` ~~`b`~~ `ox` ~~`t`~~ `ime` ~~`p`~~ `enalty`<sup>_∗_</sup> : 


where _T_ grace = 2 _._ 0 s. The first term penalizes small lateral ankle spacing, and the second penalizes prolonged failure cases in which the robot remains near the object while keeping the box too low. 

### **A.2 Domain Randomization** 

**Task Setup Randomization.** We randomize the carry-box task setup along the following dimensions: 

- the 2D positions of the box and target are sampled relative to the initial base position, 

- the pickup and placement heights are sampled within [0 _._ 0 _,_ 0 _._ 6] m above the ground, 

- the box size is randomized with axis-wise ranges _x ∈_ [0 _._ 25 _,_ 0 _._ 45] m, _y ∈_ [0 _._ 25 _,_ 0 _._ 45] m, and _z ∈_ [0 _._ 25 _,_ 0 _._ 35] m, 

- the box mass is randomized within the training range of [0 _._ 5 _,_ 5 _._ 0] kg. 

Table 3: Parameters of domain randomization. 

|Category|Term|Value|
|---|---|---|
|_Physical Properties_|actuator offset<br>motor strength<br>center of mass<br>link mass<br>_Kp_,_Kd_<br>external disturbance|_U_(_−_0_._05_,_0_._05)rad<br>_U_(0_._9_,_1_._1)<br>_U_(_−_0_._1_,_0_._1)m<br>_U_(0_._8_,_1_._2)<br>_U_(0_._9_,_1_._1)<br>every 8 steps,<br>magnitude in[_−_50_,_50]|
|_Observation Noise_|angular velocity<br>projected gravity<br>joint position<br>joint velocity|0.3<br>0.05<br>0.02<br>2.0|
|_Task Observation Noise_|box/goal position<br>box rotation|_±_0_._05m<br>_±_5<sup>_◦_</sup>|
|_Object Dynamics_|box friction<br>box restitution<br>platform friction|_U_(0_._5_,_1_._0)<br>_U_(0_._05_,_0_._2)<br>_U_(0_._5_,_2_._0)|


12 

### **A.3 Training Hyperparameters and Network Architecture** 

Table 4: Hyperparameters for training. 

|Category|Hyperparameter|Value|
|---|---|---|
|_General_|num of envs|4096|
||num of steps per iteration|100|
||num of epochs|5|
||clip range|0.2|
||discount factor_γ_|0.99|
||GAE balancing factor_λ_|0.95|
||desired KL-divergence|0.003|
||actor and critic NN|MLP, hidden units[512_,_256_,_256]|
|_Adaptation module_|adapter history length|50|
||auxiliary learning rate|1_×_10<sup>_−_3</sup>|
||FiLM hidden dimension|128|
||object / dynamics latent size|16 / 16<br>|
||GRL coefficient / weight|0.1 /1_×_10<sup>_−_3</sup>|
||GRL warmup steps|10000|


Table 5: Network architecture of the base policy and adaptation modules. 

|Module|Component|Configuration|
|---|---|---|
|Base policy|Actor / critic|MLP[512_,_256_,_256]/<br>MLP[512_,_256_,_256]|
|Adaptation module|Adapter history<br>Shared temporal encoder<br>Shared feature dimension<br>Object/load branch<br>Dynamics branch<br>FiLM generator|50 steps of 123-D observations<br>Conv1d(123_,_64_, k_ = 6_, s_ = 2)+ ELU<br>Conv1d(64_,_32_, k_ = 4_, s_ = 2)+ ELU<br>320<br>Linear(320_,_64)+ ELU<br>Linear(64_,_64)+ ELU<br>Linear(320_,_64)+ ELU<br>Linear(64_,_16)<br>hidden size 128,<br>soft-split routing|
|Latents / predictors|Object latent<br>Dynamics latent<br>Object world model<br>Robot world model|_z_obj _∈_R<sup>16</sup><br>_z_dyn _∈_R<sup>16</sup><br>MLP[64_,_64],<br>object delta target<br>MLP[128_,_128],<br>79-D robot transition target|


Table 6: Training losses and regularizers for the adaptation modules. 

|Objective|Weight|Description|
|---|---|---|
|Mass regression_L_mass|2.0|box-mass estimation|
|Loaded-state BCE_L_loaded|1.0|loaded-state prediction|
|Object world model_L_objWM|1.0|object delta prediction|
|Robot world model_L_dynWM|1.0|robot transition prediction|
|GRL adversarial loss_L_GRL|1_×_10<sup>_−_3</sup><br>|cross-branch disentanglement|
|KL regularization_L_KL|1_×_10<sup>_−_3</sup><br>|latent regularization|
|Object-latent_L_1 norm_∥z_obj_∥_1|1_×_10<sup>_−_3</sup><br>|sparsity on object latent|
|Dynamics-latent_L_1 norm_∥z_dyn_∥_1|5_×_10<sup>_−_3</sup>|sparsity on dynamics latent|
|GRL coefficient|0.1|gradient-reversal scale|
|GRL warmup steps|10000|delayed adversarial activation|


13 

### **A.4 Experiment Details** 

### **Simulation Protocol** 

Simulation evaluation is conducted under object masses of 2, 4, and 6 kg and pickup/placement heights of 0, 30, and 60 cm, as summarized in Table 1. The success condition follows the same **Liftup success** and **Full-task success** criteria as in the main text. Since training randomizes box mass only within [0 _._ 5 _,_ 5 _._ 0] kg, the 6 kg condition is treated as an out-of-distribution evaluation setting. During training, the success condition requires both a limited box tilt, measured by the norm of the box projected-gravity vector in the horizontal plane, _∥_ **g** box<sup>_xy∥<_0</sup><sup>_._1,andafinalobject-to-goal</sup> distance below 0 _._ 1 m. 

### **Real-World Protocol** 

The real-world evaluation focuses on zero-shot deployment of the learned controller on the Unitree G1 platform [32]. We evaluate the 9 condition combinations reported in Table 2, using a validation box with fixed geometry 0 _._ 30 _×_ 0 _._ 43 _×_ 0 _._ 30 m to isolate the effects of object mass and pickup/placement-height variations. 

In each trial, the robot approaches a box placed approximately 2 m in front of its initial position, lifts the box, and transports it to a goal pose located 4 m behind the pickup location. 

To improve contact reliability during grasping and transport, the robot uses high-friction gloves, as shown in Fig. 6(a). We use an external motion-capture system to obtain the robot and box poses required by the policy observation; motion-capture markers are attached to the robot pelvis and the top of the box, as illustrated in Fig. 6. Additional qualitative evaluations are conducted using the box family shown in Fig. 6(b), including the large-box and acrylic-box examples presented in Fig. 1(c). 


Figure 6: Real-world experiment setup. (a) High-friction gloves attached to the Unitree G1 hands to improve grasp contact reliability during box lifting and transport. (b) Validation boxes and payload configurations used for real-world evaluation. The box geometry is fixed while the payload mass and pickup/placement height are varied. 

14 

### **A.5 Additional Simulation Results** 


Figure 7: Supplementary visualization of the simulation results in Table 1. The left plot summarizes overall Lift-up and Full-task success across all evaluation conditions, while the right plot focuses on the OOD 6 kg setting. 


Figure 8: Additional online mass and loaded-state estimation results across four payload conditions (0.5 kg, 1 kg, 2 kg, and 4 kg). Consistent with the main results, the predicted mass _m_ ˆ , weighted by the loaded probability, converges toward the corresponding ground-truth payload after lifting and remains stable during transport. The loaded probability _p_ ˆ reliably captures the transition from unloaded to loaded states and closely follows both the soft and hard ground-truth labels across all payload conditions. 

15 


Figure 9: Box-transport trajectories under 9 object mass and pickup/placement-height conditions, evaluated with multiple goal directions. Blue and orange curves denote the base policy and SplitAdapter, respectively. Green stars indicate target locations, and red crosses indicate failed trials of the base policy. The proposed method maintains stable transport trajectories across diverse goals, whereas the base policy exhibits larger path deviations and more frequent failures under heavier payloads. 

16 

