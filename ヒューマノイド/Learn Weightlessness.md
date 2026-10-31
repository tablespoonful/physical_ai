---
title: "Learn Weightlessness: Imitate Non-Self-Stabilizing Motions on Humanoid Robot"
date: "2026-04-23"
authors: "Yucheng Xin; Jiacheng Bao; Haoran Yang; Wenqiang Que; Dong Wang; Junbo Tan"
url: https://arxiv.org/abs/2604.21351
pdf: https://arxiv.org/pdf/2604.21351
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.21351)** / [論文ページ](https://arxiv.org/abs/2604.21351)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Learn Weightlessness: Imitate Non-Self-Stabilizing Motions on Humanoid Robot** 

Yucheng Xin<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Jiacheng Bao<sup>2</sup><sup>_∗_</sup> , Haoran Yang<sup>3</sup><sup>_,_2</sup><sup>_∗_</sup> , Wenqiang Que<sup>2</sup> , Dong Wang<sup>2</sup><sup>_†_</sup> Junbo Tan<sup>1</sup> , Xueqian Wang<sup>1</sup> , Bin Zhao<sup>2</sup> , Xuelong Li<sup>2</sup> 


Fig. 1: Our work introduces a human-inspired weightlessness mechanism that controls robot joints to selectively relax when tracking non-self-stabilizing motions, enabling passive environmental contact to complete the motion. One single pipeline, without any task-specific engineering, achieves: **a) sitting on chairs** of varying heights (0.2m, 0.25m, and 0.3m); **b) lyingdown on surfaces** with different inclinations (0°, 45°, and 90°); and **c) leaning against the wall** by shoulder or elbow with only one supporting leg, while the other leg resists external perturbations at varying heights (0.1m, 0.2m, and 0.3m). **Phase a-1, b-1** : the robot reaches a critical limit posture; **Phase a-2, b-2** : lower-limb joints relax, allowing the robot to naturally fall onto the chair or inclined surface; **Phase b-3** : Waist joints relax, allowing the robot’s upper body to naturally fall onto the inclined surface; **Phase a-3, b-4** : Recovery to a stable, natural posture. 

**_Abstract_ — The integration of imitation and reinforcement learning has enabled remarkable advances in humanoid wholebody control, facilitating diverse human-like behaviors. However, research on environment-dependent motions remains limited. Existing methods typically enforce rigid trajectory tracking while neglecting physical interactions with the environment. We observe that humans naturally exploit a ”weightless” state during non-self-stabilizing (NSS) motions—selectively relaxing specific joints to allow passive body-environment contact, thereby stabilizing the body and completing the motion. Inspired by this biological mechanism, we design a weightlessnessstate auto-labeling strategy for dataset annotation; and we propose the Weightlessness Mechanism (WM), a method that dynamically determines which joints to relax and to what level, together enabling effective environmental interaction while executing target motions. We evaluate our approach on 3** 

> 1Center for Artificial Intelligence and Robotics, Shenzhen International Graduate School, Tsinghua University, China, _{_ xin-yc23@mails., wang.xq@sz., tjblql@sz. _}_ tsinghua.edu.cn, 

> 2Shanghai AI Laboratory, 3University of Science and Technology of China 

> _†_ Corresponding author, _∗_ indicates equal contribution 

**representative NSS tasks: sitting on chairs of varying heights, lying down on beds with different inclinations, and leaning against walls via shoulder or elbow. Extensive experiments in simulation and on the Unitree G1 robot demonstrate that our WM method, trained on single-action demonstrations without any task-specific tuning, achieves strong generalization across diverse environmental configurations while maintaining motion stability. Our work bridges the gap between precise trajectory tracking and adaptive environmental interaction, offering a biologically-inspired solution for contact-rich humanoid control.** 

## I. INTRODUCTION 

Developing generalist robot policies that can interact effectively with the physical world and perform complex movements has been a central goal in robotics research. Recent advances [1], [2], [3], [4], [5], [6] have enabled robots to perform increasingly expressive and human-like motions. 

We categorize all humanoid robot motions into two major types based on whether the robot can complete the movement without assistance from the external environment or objects: the **self-stabilizing (SS) motions** and the **non-self-** 


Fig. 2: **Fake motions.** Existing imitation-learning methods typically only reproduce a single demonstrated posture and ignore any physical interaction with the environment. As a result, the robot can only ”fake-sit” or ”fake-lean” without making sustained contact with the support surface. 

**stabilizing (NSS) motions** . For **SS** motions, robots can complete the movements by adjusting their own postures even when interacting with the environment or objects like walk-and-turning [4], carrying boxes [7], fadeaway jumping [3], dancing the waltz [2], and etc. For **NSS** motions, robots must rely on the external environment or objects to achieve the desired posture. Sitting on chairs, lying down on beds and leaning against walls are the most representative motions, without chairs or beds or walls, the robot struggles to maintain postural stability. 

Mainstream algorithms for real robots—reinforcement learning (RL) and imitation learning (IL)—perform well on self-stabilizing motions but often fail on non-self-stabilizing ones. RL requires complex, task-specific reward design and tuning, limiting generalization to new tasks. Naive IL produces ”fake-sit” or ”fake-lean” behaviors (Figure 2), where the robot adopts visually correct postures without establishing functional contact with supporting objects. By conditioning solely on reproduced joint positions rather than physical support conditions, these policies fail to generalize when real support heights or geometries differ from training demonstrations. 

Inspired by the weightlessness mechanism in these nonself-stabilizing human motions shown in Figure 3 and Figure 4, we propose a method incorporating a weightlessness mechanism (WM). This mechanism modulates joint activation by determining both which joints to relax and the specific degree of relaxation, thereby enhancing control performance during the execution of non-self-stabilizing robot movements. 

To generate training data for weightless state determination, we design a weightlessness-state auto-labeling strategy to automatically determine which joints to relax and annotate their weightlessness states from motion sequences. These annotations are used to train a WM network. The trained WM network predicts the current state and appropriate joint relaxation levels, enabling the robot to execute sitting, lyingdown, and leaning motions naturally through controlled freefall. An imitation learning policy is then trained to track these motions, and fine-tuned with the WM network for more natural behaviors. The approach allows the Unitree G1 robot to sit stably on chairs of varying heights, lie down on beds with different inclinations, and lean against walls by shoulder 

or elbow while resisting external disturbances, as shown in Figure 1. 

In conclusion, our contributions are as follows: leftmargin=12pt, parsep=0pt 

- 1) We propose a pipeline that integrates a weightlessness mechanism (WM) into humanoid whole-body motion tracking, enabling physically plausible and human-like execution of non-self-stabilizing motions. 

- 2) We design a weightlessness-state auto-labeling strategy that automatically annotates which joints to relax, and the weightlessness states from NSS motion sequence data. 

- 3) We validate the approach achieves robust generalization to varied environment configurations across arbitrary NSS tasks without any task-specific engineering. 

- 4) We validate our approach on the Unitree G1 humanoid robot, demonstrating robust sitting on chairs of different heights, lying down onto beds with various inclinations, and leaning against walls with either the shoulder or elbow, across both simulation and realworld environments. 


Fig. 3: **WM in Sitting and Lying-down.** During typical human sitting and lying-down motions, the body often relaxes after reaching a certain critical point. For example, after attaining a specific extreme position during sitting **b)** , the lower limbs become fully relaxed, allowing the upper body to free-fall onto the chair to complete the sitting motion. Similarly, when leaning back to a certain limit **c)** , the upper body relaxes and free-falls onto the bed to accomplish the lying-down motion. 

## II. RELATED WORKS 

**Human-Object Interaction.** Early datasets such as GRAB [8] provided detailed captures of human-object interactions. More recently, a number of datasets have been proposed to further enrich this area [9], [10], [11], [12], [13], [14], [15], [16], [17]. The CHAIRS [18] and COUCH [19] datasets provide realistic full-body interactions with sittable furniture, offering high-quality annotations for human–object interaction research. 

Physics simulators such as Isaac Gym [20] and MuJoCo [21] are widely used for synthesizing realistic humanobject interactions. Early methods largely rely on tracking 


Fig. 4: **WM in leaning against the wall.** During the action of leaning against a wall, humans typically relax and undergo a controlled free-fall toward the wall after tilting to a certain critical angle in **b)** . Only the arm and leg in contact with the wall remain actively engaged to provide support, while the remaining arm and leg are free to move in **c)** . 

reference motions [22], [23], [24], [25], [13], but often suffer from limited generalization. To overcome this, approaches introduce Visual-Language-Action (VLA) [26] and adversarial priors such as AMP [27], which have been applied to various tasks [28], [29], [30], [31], [32]. Recent work also explores HOI using humanoid robots to bridge simulation and reality [33], [13], [34]. 

**Imitation Learning on Humanoid.** Recent advances in humanoid control have shifted from model-based methods to perception- and imitation-driven approaches. Early work relied on IK, ZMP, and LIP models for teleoperation [35], [36],later extended by motion capture [37], [38], Exoskeleton [39], and VR-based systems [40], [41], [42], [43], [44]. 

Deep learning enables large-scale motion imitation. Humanoid Transformer [45] predicts motions from mocap and video data, and Exbody [46] enhances expressiveness via body-part separation. HumanPlus [1] and Okami [47] extend video imitation with transformer models. BeyondMimic [48] achieves real-world dynamic skills with guided diffusion, and GBC [49] introduces a robust DAgger-MMPPO based MMTransformer. Real-time control methods such as Exbody2 [2], H2O [50], OmniH2O [4], and HOVER [51] use teacher-student frameworks for teleoperation and imitation. To address motion diversity loss, UniTracker [52] integrates a CVAE to model latent motion diversity. For expressive motions, Humanoid-VLA [7] adds scene perception for wholebody control, while ASAP [3], Embrace Collisions [5], and PBHC [6] enhance expressiveness via delta-action pretraining, contact recovery, and dynamic skill imitation. 

## III. METHODS 

## _A. Framework_ 

The proposed framework, incorporating a human-inspired weightlessness mechanism (WM), is shown in Figure 5. We collected 50 video demonstrations each of sitting, lying down, and leaning with shoulder/elbow motions, retargeted them to the Unitree G1 robot. Environmental supports (e.g., 

chairs, beds, walls) were reconstructed into height map, and joint weightlessness states were annotated across the dataset. 

We adopt a two-stage training for non–self-stabilizing motions. First, an asymmetric Proximal Policy Optimization (PPO) algorithm performs imitation learning on the processed data. Second, an LSTM-based WM network predicts continuous joint relax levels, simulating controlled free-fall. The imitation policy is fine-tuned under these signals to improve naturalness and robustness. 

The final policy was validated in MuJoCo and deployed on the Unitree G1, successfully executing non–self-stabilizing motions. Training details are provided in later sections. 

## _B. Data Process_ 

**Data Acquisition and Processing.** We collected 200 video demonstrations across four action categories—sitting, lying, and leaning via shoulder and elbow (50 per category). SMPL motion data were obtained using GVHMR [53], world point clouds extracted with MegaSaM [54], and meshes generated via NKSR [55]. SMPL motions were aligned with the reconstructed scene geometry using the MegaHunter module from VideoMimic [34], after which we approximated the key contact objects and environment using simple shape of boxes. 

**Retargeting with Smoothing.** We adopt GMR [56] retargeting [57] to transfer reconstructed SMPL motions onto target skeletons of Unitree G1. To alleviate jitter in static poses, we apply a smoothing pipeline that first downsamples the sequence to reduce redundancy, then applies a causal moving average to suppress high-frequency oscillations, and finally uses a median filter to remove spike-like artifacts while preserving salient motion features. Interpolation restores the original frame rate, producing temporally consistent and stable motions for downstream optimization. 

## _C. Weightlessness-State Auto-Labeling Strategy_ 

To accurately annotate weightless states in motion sequences, we identify two key aspects: (i) the time interval of weightlessness, and (ii) the set of joints entering the weightless state. 

**Time Interval of Weightlessness.** Let _P_ ( _t_ ) denote the gravity projection of the robot’s center of mass at time _t_ , and _S_ ( _t_ ) the support polygon formed by the feet. A weightless interval should be satisfied whenever 

## _P_ ( _t_ ) _∈S/_ ( _t_ ) _,_ 

and the robot makes external contact through body parts other than the feet. Let _C_ ( _t_ ) denote the set of environmental contacts at time _t_ , which is confirmed in reconstructed simulator. Then the annotated weightless interval _I_ is 

## _I_ = _{t | P_ ( _t_ ) _∈S/_ ( _t_ ) _, C_ ( _t_ ) _̸_ = _∅}._ 

To enhance robustness, the start and end times of _I_ are perturbed by a random temporal shift of _±_ ∆ _t_ , with ∆ _t_ = 20 timesteps. The interval is also defined as shown in Figure 6. 

**Joint Weightless States.** The set of active joints _A_ ( _t_ ) is determined using a limb-node hierarchy inspired by human 


Fig. 5: **Framework.** The method consist of 4 components: **(a)** We collected videos of sitting, lying, and leaning (shoulder and elbow) motions, from which SMPL motions and terrains were extracted, followed by motion retargeting and terrain reconstructed. **(b)** Label the robot’s joint weightlessness states and weightless time interval via annotation method, and train a WM network using LSTM. **(c)** Train the action policy using imitation learning. **(d)** Integrate the WM network to fine-tune the learned policy. 


Fig. 6: **Confirmation of Weightless Time Interval.** The weightless interval _I_ is related to contacting-time _C_ ( _t_ ), CoM offset time _{P_ ( _t_ ) _∈S/_ ( _t_ ) _}_ , and random temporal shift ∆ _t_ . 

motor control. Let _C_ ( _t_ ) again denote the set of environmentcontact frames at time _t_ . Then 


where ParentPath( _c_ ) denotes all ancestor nodes from contact joint _c_ up to the waist joint _c_ waist. The weightless joints are then 


The method and example were shown in Figure 7, when leaning against a wall supported by the left elbow and left foot, we have _C_ ( _t_ ) = _{c_ left elbow _, c_ left foot _}_ , hence _A_ ( _t_ ) includes all ancestors of these contacts plus the waist (painted blue), while the remaining joints _W_ ( _t_ ) are annotated as weightless (painted red). 

Through the aforementioned approach, we can achieve automated annotation of weightless time interval and weightless joints directly from video stream data, eliminating the need for manual intervention. 

## _D. WM Network Training_ 

The weightlessness mechanism (WM) computes jointspecific relaxation levels _wt,i_ for the corresponding joints 

_qi_ , enabling the robot to transition into a weightless state and execute non-self-stabilizing tasks. 

Formally, let the robot have _K_ = 23 actuated joints with joint states _q_ = [ _q_ 1 _, q_ 2 _, . . . , qK_ ]<sup>_⊤_</sup> _∈_ R<sup>_K_</sup> , where _qi_ represents the angle or position of the _i_ -th joint. The WM aims to learn a continuous control policy 


that maps observed features **x** _t ∈X_ , consisting of current posture, motion history, and future motion trend, to a target relaxation vector 


where _wt,i ∈_ [0 _,_ 1] denotes the relaxation level of joint _i_ at time _t_ . A value _wt,i ≈_ 0 indicates full relaxation (weightless), while _wt,i ≈_ 1 indicates full activation. 

To determine the weightlessness state, it is necessary to utilize the current posture, motion history, and future motion trend. In particular, future motion information is crucial. Let _qt_<sup>_r∈_R23denotethereferencejointpositionsattime</sup> _t_ , and let 


denote the historical sequence of length _h_ = 4. The future motion trend is obtained by sampling a reference sequence with a randomized temporal offset. Specifically, for maximum offset _t_<sup>˜</sup> and horizon _l_ = 5, we define 


where _δ ∼U_ ( _−t,_<sup>˜</sup> _t_<sup>˜</sup> ) is uniformly sampled.Thus, the network input at time _t_ is 


corresponding to 4 + 1 + 5 = 10 frames of _K_ -dimensional joint positions. 

The LSTM-based weightlessness mechanism network _Wθ_ maps this input to a continuous relaxation vector: 


To enforce temporal consistency and avoid abrupt changes in relaxation levels, we add a smoothness regularization term across consecutive frames. Specifically, for each training sequence, we define 


which penalizes sudden jumps in predicted relaxation levels between adjacent frames. 

The final training objective is a weighted sum of the Binary Cross-Entropy (BCE) loss and the smoothness loss: 


where _λ >_ 0 controls the strength of temporal smoothing. This ensures that the predicted relaxation vector **w** _t_ evolves continuously over time, preventing unrealistic sudden transitions of relaxation level. 

Details of the network architecture and training configurations are included in Table I. 


Fig. 7: **Confirmation of Joint Weightless States.** The left image illustrates the limb-node relationship. The right image presents a case study. 

TABLE I: LSTM Network Configurations 

|**Component**|**Specification**|
|---|---|
|Input Dimension|230-dims each frame<br>including 4 historical steps, 1 current step,<br>and 5 future steps of joint positions _q ∈_R<sup>23</sup>,<br>resulting in a total input dimension of 23_×_10 = 230|
|Hidden Size|[256, 256, 64] units for hidden layers|
|Output|Continuous deactivation levels **w**_t ∈_[0_,_1]<sup>_K_</sup>|
|Activation Function|Sigmoid|
|Dropout|0.1|
|Optimizer|Adam|
|Loss Function|Binary Cross-Entropy (BCE) + Smoothness penalty|
|Batch Size|64|
|Learning Rate|1e-4|
|Regularization|Temporal smoothness: _λ_ <sup>�</sup>(_wt,i −wt−_1_,i_)<sup>2</sup>|


## _E. Action Policy Training_ 

In this work, imitation learning is primarily used to train an action policy for the robot’s whole-body motion. We employ 

the policy network that maps from the robot’s proprioception and reference motions to whole-body motion control signals. **Observation space.** The policy observation _ot_ consists of joint positions _qt ∈_ R<sup>23</sup> , joint velocities _q_ ˙ _t ∈_ R<sup>23</sup> , root angular velocity _ωt_<sup>root</sup> _∈_ R<sup>3</sup> , projected gravity _gt ∈_ R<sup>3</sup> and previous action _at−_ 1 _∈_ R<sup>23</sup> . To enhance the tracking performance, we incorporate the reference joint positions _qt_<sup>_r∈_R23andjointvelocities</sup><sup>_q_˙</sup> _t_<sup>_r∈_R23extractedfromthe</sup> dataset into the observations. Additionally, we introduce an n - step observation history _ot−n_ : _t−_ 1 for more precise future state estimation. To improve terrain adaptation, we further include sampled terrain height measurements _ht ∈_ R<sup>32</sup> around the robot’s base. We sample 32 points within a region of 0.5×0.5 meters from the robot’s base position, rotated according to the robot’s orientation. 

Thus, the complete observation at time _t_ is: 


We adopt an asymmetric PPO framework, where the actor and critic use distinct observation spaces. The actor receives only partial observations **o** _t_ available at deployment, while the critic has access to additional privileged information, including root linear velocity _vt_<sup>root</sup> _∈_ R<sup>3</sup> , ground friction _µ ∈_ R<sup>1</sup> , and external force _f ∈_ R<sup>3</sup> . This enables more accurate value estimation, improving overall policy optimization. 

**Action Space.** The policy outputs an action _at ∈_ R<sup>_K_</sup> , corresponding to the Unitree G1’s 23 degrees of freedom. Each element of _at_ represents the deviation between the desired joint position and the default joint position. The desired joint positions are subsequently tracked using a low-level Proportional-Derivative (PD) controller, which generates the torque commands to actuate. 

TABLE II: Reward Terms for Training 

|**Term**|**Expression**|**Weight**|
|---|---|---|
|**Task Rewards**|||
|Keypoint position|exp(_−_0_._1_∥pt −_ˆ_pt∥_<sup>2</sup><br>2<sup>)</sup><br>|3_._00|
|Root rotation|exp(_−_1_._0_∥θ_<sup>_root_</sup><br>_t_<br>_⊕_<sup>ˆ</sup>_θ_<sup>_root_</sup><br>_t_<br>_∥_)<br><br>|0_._5|
|Root velocity|exp(_−_1_._0_∥v_<sup>_root_</sup><br>_t_<br>_−_ˆ_v_<sup>_root_</sup><br>_t_<br>_∥_2)<br><sup>ˆ</sup>|0_._75|
|Joint position without feet|exp(_−_1_._0_∥dt −dt∥_<sup>2</sup><br>2<sup>)</sup><br><sup>ˆ</sup>|32|
|Joint velocity without feet|exp(_−_1_._0_∥_<sup>˙</sup>_dt −_<sup>˙</sup>_dt∥_<sup>2</sup><br>2<sup>)</sup>|0_._5|
|Termination|**1**termination|_−_200|
|**Regularization Rewards**|||
|Joint acceleration|_∥_¨_qt∥_2|_−_2_._5_×_10<sup>_−_8</sup>|
|Joint velocity|_∥_˙_qt∥_2|_−_0_._001|
|Action rate|_∥at −at−_1_∥_2|_−_0_._5<br>|
|Torque|_∥τt∥_|_−_1_×_10<sup>_−_6</sup>|
|Feet orientation|_∥_**g**_xy∥_2<br>|_−_62_._5|
|Feet heading|_∥θ_<sup>_feet_</sup><br>_t_<br>_−θ_<sup>_root_</sup><br>_t_<br>_∥_2|_−_1_×_10<sup>_−_5</sup>|


**Reward Design.** During the first stage, we employed a reward structure inspired by [3]. However, for non-selfstabilizing motions, we observed noticeable inconsistencies in the feet’ placement after retargeting. To address this issue, we opted to relax the tracking constraints on the feet joints during training and introduced additional rewards for feet orientation and feet heading. This approach enhances the stability and improves its tracking performance for key points. The detailed reward design is summarized in Table II. 

## _F. Weightless-Action Policy Fine-tune._ 

At the second-stage training, we integrate the weightlessness mechanism to fine-tune the action policy. The WM network predicts the degree of deactivation for each target lower-limb joint at each step. The output torque of the robot’s joints can be expressed as: 

## _τt_ = _τ_ ( _at_ ) _·_ **w** _t_ 

where is, _τt ∈_ R<sup>23</sup> represents the joint output torque at the current moment, _τ_ ( _·_ ) represents the torque mapping of the PD controller. _at ∈_ R<sup>23</sup> represents the action policy output for the whole-body joints. 

TABLE III: Ablation Study: Weightlessness Mechanism Effectiveness (Tracking Metrics) 

|Experiments|||Error M|etrics|||
|---|---|---|---|---|---|---|
||_Empjpe _|_Empjae _|_Empjve _|_Eroot,p_|_Eroot,r_|_Eroot,v_|
|baseline-Sit|**0.1642**|**0.0357**|1.7802|**0.1468**|**1.4936**|0.3350|
|WM w/o ft|0.2047|0.0421|1.9171|0.1734|1.2011|0.5302|
|WM+ft (ours)|0.1707|0.0398|**1.7484**|0.1521|1.4550|**0.3099**|
|baseline-LieDown|**0.2512**|**0.0483**|2.1504|**0.2317**|1.8901|**0.4103**|
|WM w/o ft|0.2953|0.0556|2.4505|0.2651|**1.7523**|0.6226|
|WM+ft (ours)|0.2605|0.0505|**2.1054**|0.2380|1.8329|0.4357|
|baseline-Lean Shoulder|0.1378|**0.0281**|1.2546|**0.0957**|0.8758|0.1832|
|WM w/o ft|0.1158|0.0332|1.4891|0.1176|0.7926|0.2783|
|WM+ft (ours)|**0.1103**|0.0291|**1.2054**|0.0987|**0.8552**|**0.1959**|
|baseline-Lean Elbow|**0.1084**|**0.0275**|1.2203|**0.0927**|**0.8487**|0.1884|
|WM w/o ft|0.1328|0.0327|1.4592|0.1114|0.7339|0.2920|
|WM+ft (ours)|0.1127|0.0283|**1.1809**|0.0949|0.8554|**0.1839**|


TABLE IV: Ablation Study: Weightlessness Mechanism Effectiveness (Success Rates) 

|Experiments|S|uccess Ra|tes|
|---|---|---|---|
||_E_<sup>1</sup><br>_succ_|_E_<sup>2</sup><br>_succ_|_E_<sup>3</sup><br>_succ_|
|baseline-Sit|0.72|0.20|0.08|
|WM w/o ft|0.76|0.86|0.82|
|WM+ft (ours)|0.78|0.92|0.84|
|baseline-LieDown|0.58|0.56|0.64|
|WM w/o ft|0.72|0.72|0.74|
|WM+ft (ours)|**0.92**|**0.88**|**0.90**|
|baseline-Lean Shoulder|0.48|0.30|0.22|
|WM w/o ft|0.70|0.62|0.62|
|WM+ft (ours)|**0.94**|**0.88**|**0.82**|
|baseline-Lean Elbow|0.42|0.24|0.14|
|WM w/o ft|0.86|0.84|0.68|
|WM+ft (ours)|**0.92**|**0.92**|**0.86**|


The input to the WM network while fine-tuning can be expressed as: 


where _qt_ and _qh_ represent the current and historical joint positions of the robot, respectively, while _qf_<sup>_r_correspondsto</sup> the future reference motion initialized from the current time phase. Meanwhile, the incorporation of the weightlessness mechanism alters the observation space and may impair the performance of the original policy, thus making fine-tuning of the policy essential. 

## IV. EXPERIMENTS 

## _A. Experiment Setup_ 

**Software and Hardware.** To verify the effectiveness of the algorithm, we deployed it in both simulation and realworld environments. We used Isaac Gym as the training environment and validated our policy in the MuJoCo simulator. Both the simulation and real-world experiments were conducted using the Unitree G1 robot. We utilize the builtin LiDAR on the Unitree G1 robot to obtain terrain height observations. The control frequency on the real robot is 50 Hz. 

**Baselines.** We use the imitation learning policy without the WM as our baseline and perform ablation experiments on this baseline to evaluate the effectiveness of the proposed mechanisms. 

**Metrics.** We evaluate our method using a set of metrics that assess kinematic accuracy, physical realism, and task success in simulation. _E_ mpjpe, _E_ mpjae, _E_ mpjve: These metrics evaluate the accuracy of joint-level predictions. _E_ mpjpe measures the mean per-joint global position error, _E_ mpjae measures the mean per-joint angles error, and _E_ mpjve measures the mean per-joint velocity error. _E_ root,p, _E_ root,r, _E_ root,v: These metrics quantify the root tracking performance in terms of position, rotation, and velocity error, respectively. _E_ succ<sup>1,</sup><sup>_E_</sup> succ<sup>2, and</sup><sup>_E_</sup> succ<sup>3denote the task success rates measured</sup> in four different experimental motions: 

- **Sit action:** The success rates _E_ succ<sup>1,</sup><sup>_E_</sup> succ<sup>2,and</sup><sup>_E_</sup> succ<sup>3</sup> correspond to the agent successfully sitting on chairs of three different heights: 0.2 m, 0.25 m, and 0.3 m. A trial is considered successful if the agent achieves the sitting posture and contact with chairs without falling. 

- **Lying down action:** The success rates _E_ succ<sup>1,</sup><sup>_E_</sup> succ<sup>2,</sup> and _E_ succ<sup>3forthelying-downactionaremeasuredat</sup> three tilt angles: 0<sup>_◦_</sup> , 45<sup>_◦_</sup> , and 90<sup>_◦_</sup> . A trial is considered successful if the agent completes the lying-down motion as intended, maintaining stability without any abnormal oscillations or jittering. 

- **Leaning action (by shoulder/elbow)** : The leaning task is designed to test whether the agent can maintain stability while one side of the body bears weight against a support via the shoulder or elbow. The success rates _E_ succ<sup>1,</sup><sup>_E_</sup> succ<sup>2,and</sup><sup>_E_</sup> succ<sup>3aredefinedbythefreeswing</sup> and disturbance resistance of the non-weight-bearing leg, tested at raised heights of 0.1m, 0.2m, and 0.3m. 

For each condition, the reported success rates are computed based on 50 trials. 

## _B. Main Results_ 

In this work, our main contribution is the introduction of a WM. To evaluate its effectiveness, we focus on these core questions: 

## **Q1: Does the WM benefit?** 

To evaluate the benefits of the WM in training, we introduce it as an experimental variable. As shown in Table III, the inclusion of WM leads to a slight degradation in motion tracking performance, as expected, since it permits controlled 


Fig. 8: For different motions, the weightlessness network demonstrates a clear capability to identify distinct temporal intervals of weightlessness. 

deviation from the reference trajectory to achieve more natural motion. However, the baseline method, which learns a fixed motion trajectory, fails to adapt to environmental variations such as chair height or surface inclination. In contrast, as shown in Table IV, the WM-based approach significantly improves success rates across all tasks. These results indicate that although WM slightly affects tracking accuracy, it substantially enhances the robot’s ability to complete sitting, lying, and leaning motions successfully. 

## **Q2: Why is the WM used only for fine-tuning rather than during initial policy training?** 

Integrating the independently trained WM into imitation learning poses a challenge. We designed an ablation experiment where the way WM involves in training differ: applying WM from the start (WM w/o ft) or applying WM to fine-tune the action policy after initial convergence (WM+ft). 

As results shown in Table III and Table IV, fine-tuning 5000 iterations of imitation learning followed by 2000 iterations with the WM (WM+ft) achieves better tracking and success rates than synchronous training (WM w/o ft). This is likely because early random exploration triggers premature weightless states, leading to overly conservative behavior. Fine-tuning avoids this, allowing better overall performance. 

TABLE V: Domain Randomization Parameters 

|**Parameter**|**Range [Min, Max]**|**Unit**|
|---|---|---|
|Link Mass|[0_._8_,_1_._2]|kg|
|CoM offset|[_−_0_._1_,_0_._1]|m|
|Ground Friction|[0_._5_,_1_._5]<br>|-|
|Motor Strength|[0_._8_,_1_._2]|Nm|
|Joint _Kp_|[0_._75_,_1_._25]|-|
|Joint _Kd_|[0_._75_,_1_._25]|-|
|Action Delay|[5_,_25]|ms|


## **Q3: How does WM network perform?** 

To evaluate the performance intuitively, we output the weightless values for four different motions, as shown in the Figure 8. It can be observed that during the motion, the weightlessness network successfully identifies reasonable temporal intervals of weightlessness. 

## _C. Deployment_ 

To bridge the gap between simulation and reality (simto-real), domain randomization was introduced during training. By introducing variability in key physical parameters, the learned policy becomes more robust, enabling seamless transfer to the real world. The specific parameters used for domain randomization are listed in Table V. 

As shown in Figure 1, the proposed algorithm was deployed on the real robot. For sitting, the robot was tested under different chair heights and achieved the intended posture reliably. For lying-down, trials under varying surface inclinations were all completed stably without abnormal oscillations. For leaning, both shoulder- and elbow-based cases were evaluated against a wall, with stability confirmed by perturbing the non-supporting leg. Overall, the robot demonstrated consistent, natural, and stable motion performance across all conditions. 

## V. CONCLUSION 

In this work, we introduce a human-inspired weightlessness mechanism (WM) designed to enable humanoid robots to perform physically plausible non-self-stabilizing (NSS) motions—including sitting on chairs of varying heights, lying down on bed with different inclinations, and leaning against walls by shoulder or elbow. A auto-labeling strategy based on limb-node relationship is proposed, which enables automatic annotation of joint weightless states and weightless time interval. The proposed WM network employs an LSTMbased network to predict adaptive, joint-specific relaxation levels in real time, allowing the robot to enter a state of controlled free-fall while preserving body stability. Extensive experiments conducted on the Unitree G1 humanoid robot show significantly improved task success rates and more natural NSS motion adaptation across diverse environmental geometries without any task-specific engineering. This approach enhances the robot’s ability to imitate humanlike weight transfer and whole-body control in interactive scenarios. 

## REFERENCES 

- [1] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn, “Humanplus: Humanoid shadowing and imitation from humans,” _arXiv preprint arXiv:2406.10454_ , 2024. 

- [2] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” _arXiv preprint arXiv:2412.13196_ , 2024. 

- [3] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” _arXiv preprint arXiv:2502.01143_ , 2025. 

- [4] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” _arXiv preprint arXiv:2406.08858_ , 2024. 

- [5] Z. Zhuang and H. Zhao, “Embrace collisions: Humanoid shadowing for deployable contact-agnostics motions,” _arXiv preprint arXiv:2502.01465_ , 2025. 

- [6] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li, “KungfuBot: Physics-Based Humanoid Whole-Body Control for Learning Highly-Dynamic Skills,” Jun. 2025. 

- [7] P. Ding, J. Ma, X. Tong, B. Zou, X. Luo, Y. Fan, T. Wang, H. Lu, P. Mo, J. Liu _et al._ , “Humanoid-vla: Towards universal humanoid control with visual integration,” _arXiv preprint arXiv:2502.14795_ , 2025. 

- [8] O. Taheri, N. Ghorbani, M. J. Black, and D. Tzionas, “Grab: A dataset of whole-body human grasping of objects,” in _Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part IV 16_ . Springer, 2020, pp. 581–600. 

- [9] B. L. Bhatnagar, X. Xie, I. A. Petrov, C. Sminchisescu, C. Theobalt, and G. Pons-Moll, “Behave: Dataset and method for tracking human object interactions,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022, pp. 15 935–15 946. 

- [10] Y. Huang, O. Taheri, M. J. Black, and D. Tzionas, “Intercap: Joint markerless 3d tracking of humans and objects in interaction,” in _DAGM German Conference on Pattern Recognition_ . Springer, 2022, pp. 281– 299. 

- [11] J. Li, J. Wu, and C. K. Liu, “Object motion guided human motion synthesis,” _ACM Transactions on Graphics (TOG)_ , vol. 42, no. 6, pp. 1–11, 2023. 

- [12] J. Kim, J. Kim, J. Na, and H. Joo, “Parahome: Parameterizing everyday home activities towards 3d generative modeling of human-object interactions,” _arXiv preprint arXiv:2401.10232_ , 2024. 

- [13] Y. Liu, B. Yang, L. Zhong, H. Wang, and L. Yi, “Mimicking-bench: A benchmark for generalizable humanoid-scene interaction learning via human mimicking,” _arXiv preprint arXiv:2412.17730_ , 2024. 

- [14] Y. Liu, H. Yang, X. Si, L. Liu, Z. Li, Y. Zhang, Y. Liu, and L. Yi, “Taco: Benchmarking generalizable bimanual tool-action-object understanding,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 21 740–21 751. 

- [15] X. Lv, L. Xu, Y. Yan, X. Jin, C. Xu, S. Wu, Y. Liu, L. Li, M. Bi, W. Zeng _et al._ , “Himo: A new benchmark for full-body human interacting with multiple objects,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 300–318. 

- [16] X. Xie, J. E. Lenssen, and G. Pons-Moll, “Intertrack: Tracking human object interaction without object templates,” _arXiv preprint arXiv:2408.13953_ , 2024. 

- [17] Y. Liu, C. Zhang, R. Xing, B. Tang, B. Yang, and L. Yi, “Core4d: A 4d human-object-human interaction dataset for collaborative object rearrangement,” _arXiv preprint arXiv:2406.19353_ , 2024. 

- [18] N. Jiang, T. Liu, Z. Cao, J. Cui, Z. Zhang, Y. Chen, H. Wang, Y. Zhu, and S. Huang, “Full-body articulated human-object interaction,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2023, pp. 9365–9376. 

- [19] X. Zhang, B. L. Bhatnagar, S. Starke, V. Guzov, and G. Pons-Moll, “Couch: Towards controllable human-chair interactions,” in _European Conference on Computer Vision_ . Springer, 2022, pp. 518–535. 

- [20] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa _et al._ , “Isaac gym: High performance gpu-based physics simulation for robot learning,” _arXiv preprint arXiv:2108.10470_ , 2021. 

- [21] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [22] L. Liu, K. Yin, and B. Guo, “Improving sampling-based motion control,” in _Computer Graphics Forum_ , vol. 34, no. 2. Wiley Online Library, 2015, pp. 415–423. 

- [23] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [24] Y.-W. Chao, J. Yang, W. Chen, and J. Deng, “Learning to sit: Synthesizing human-chair interactions via hierarchical control,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 35, no. 7, 2021, pp. 5887–5895. 

- [25] Z. Xie, J. Tseng, S. Starke, M. van de Panne, and C. K. Liu, “Hierarchical planning and control for box loco-manipulation,” _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , vol. 6, no. 3, pp. 1–18, 2023. 

- [26] X. Xu, Y. Zhang, Y.-L. Li, L. Han, and C. Lu, “Humanvla: Towards vision-language directed object rearrangement by physical humanoid,” _arXiv preprint arXiv:2406.19972_ , 2024. 

- [27] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [28] J. Juravsky, Y. Guo, S. Fidler, and X. B. Peng, “Padl: Languagedirected physics-based character control,” in _SIGGRAPH Asia 2022 Conference Papers_ , 2022, pp. 1–9. 

- [29] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Largescale reusable adversarial skill embeddings for physically simulated characters,” _ACM Transactions On Graphics (TOG)_ , vol. 41, no. 4, pp. 1–17, 2022. 

- [30] M. Hassan, Y. Guo, T. Wang, M. Black, S. Fidler, and X. B. Peng, “Synthesizing physical character-scene interactions,” in _ACM SIGGRAPH 2023 Conference Proceedings_ , 2023, pp. 1–9. 

- [31] L. Pan, J. Wang, B. Huang, J. Zhang, H. Wang, X. Tang, and Y. Wang, “Synthesizing physically plausible human motions in 3d scenes,” in _2024 International Conference on 3D Vision (3DV)_ . IEEE, 2024, pp. 1498–1507. 

- [32] Z. Xiao, T. Wang, J. Wang, J. Cao, W. Zhang, B. Dai, D. Lin, and J. Pang, “Unified human-scene interaction via prompted chain-ofcontacts,” _arXiv preprint arXiv:2309.07918_ , 2023. 

- [33] C. Sferrazza, D.-M. Huang, X. Lin, Y. Lee, and P. Abbeel, “Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation,” _arXiv preprint arXiv:2403.10506_ , 2024. 

- [34] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa, “Visual Imitation Enables Contextual Humanoid Control,” May 2025. 

- [35] F.-J. Montecillo-Puente, M. Narsipura Sreenivasa, and J.-P. Laumond, “On real-time whole-body human to humanoid motion transfer,” 2010. 

- [36] K. Hu, C. Ott, and D. Lee, “Online human walking imitation in task and joint space based on quadratic programming,” in _2014 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2014, pp. 3458–3464. 

- [37] C. Stanton, A. Bogdanovych, and E. Ratanasena, “Teleoperation of a humanoid robot using full-body motion capture, example movements, and machine learning,” in _Proc. Australasian Conference on Robotics and Automation_ , vol. 8, 2012, p. 51. 

- [38] D. Dajles, F. Siles _et al._ , “Teleoperation of a humanoid robot using an optical motion capture system,” in _2018 IEEE International Work Conference on Bioinspired Intelligence (IWOBI)_ . IEEE, 2018, pp. 1–8. 

- [39] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang, “Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit,” _arXiv preprint arXiv:2502.13013_ , 2025. 

- [40] A. Winkler, J. Won, and Y. Ye, “Questsim: Human motion tracking from sparse sensors with simulated avatars,” in _SIGGRAPH Asia 2022 Conference Papers_ , 2022, pp. 1–8. 

- [41] S. Lee, S. Starke, Y. Ye, J. Won, and A. Winkler, “Questenvsim: Environment-aware simulated motion tracking from sparse sensors,” in _ACM SIGGRAPH 2023 Conference Proceedings_ , 2023, pp. 1–9. 

- [42] Y. Ye, L. Liu, L. Hu, and S. Xia, “Neural3points: Learning to generate physically realistic full-body motion for virtual reality users,” in _Computer Graphics Forum_ , vol. 41, no. 8. Wiley Online Library, 2022, pp. 183–194. 

- [43] Z. Luo, J. Cao, J. Merel, A. Winkler, J. Huang, K. Kitani, and W. Xu, “Universal humanoid motion representations for physics-based control,” _arXiv preprint arXiv:2310.04582_ , 2023. 

- [44] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-television: Teleoperation with immersive active visual feedback,” _arXiv preprint arXiv:2407.01512_ , 2024. 

- [45] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik, “Humanoid locomotion as next token prediction,” in _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. 

- [46] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” _arXiv preprint arXiv:2402.16796_ , 2024. 

- [47] J. Li, Y. Zhu, Y. Xie, Z. Jiang, M. Seo, G. Pavlakos, and Y. Zhu, “Okami: Teaching humanoid robots manipulation skills through single video imitation,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [48] T. E. Truong, Q. Liao, X. Huang, G. Tevet, C. K. Liu, and K. Sreenath, “BeyondMimic: From Motion Tracking to Versatile Humanoid Control via Guided Diffusion,” Aug. 2025. 

- [49] Y. Yao, C. Luo, J. Du, W. He, and J.-G. Lu, “GBC: Generalized Behavior-Cloning Framework for Whole-Body Humanoid Imitation,” Aug. 2025. 

- [50] T. He, Z. Luo, W. Xiao, C. Zhang, K. Kitani, C. Liu, and G. Shi, “Learning human-to-humanoid real-time whole-body teleoperation,” 

in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2024, pp. 8944–8951. 

- [51] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang _et al._ , “Hover: Versatile neural whole-body controller for humanoid robots,” _arXiv preprint arXiv:2410.21229_ , 2024. 

- [52] K. Yin, W. Zeng, K. Fan, Z. Wang, Q. Zhang, Z. Tian, J. Wang, J. Pang, and W. Zhang, “UniTracker: Learning Universal Whole-Body Motion Tracker for Humanoid Robots,” Jul. 2025. 

- [53] Z. Shen, H. Pi, Y. Xia, Z. Cen, S. Peng, Z. Hu, H. Bao, R. Hu, and X. Zhou, “World-Grounded Human Motion Recovery via GravityView Coordinates,” in _SIGGRAPH Asia 2024 Conference Papers_ , Dec. 2024, pp. 1–11. 

- [54] Z. Li, R. Tucker, F. Cole, Q. Wang, L. Jin, V. Ye, A. Kanazawa, A. Holynski, and N. Snavely, “MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos,” Dec. 2024. 

- [55] J. Huang, Z. Gojcic, M. Atzmon, O. Litany, S. Fidler, and F. Williams, “Neural kernel surface reconstruction,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023, pp. 4369–4379. 

- [56] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu, “Retargeting matters: General motion retargeting for humanoid motion tracking,” _arXiv preprint arXiv:2510.02252_ , 2025. 

- [57] Z. Luo, J. Cao, A. Winkler, K. Kitani, and W. Xu, “Perpetual Humanoid Control for Real-time Simulated Avatars,” Sep. 2023. 

