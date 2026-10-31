---
title: "X-Loco: Towards Generalist Humanoid Locomotion Control via Synergetic Policy Distillation"
date: "2026-03-04"
authors: "Dewei Wang; Xinmiao Wang; Chenyun Zhang; Jiyuan Shi; Yingnan Zhao; Chenjia Bai"
url: https://arxiv.org/abs/2603.03733
pdf: https://arxiv.org/pdf/2603.03733
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.03733)** / [論文ページ](https://arxiv.org/abs/2603.03733)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# X-Loco: Towards Generalist Humanoid Locomotion Control via Synergetic Policy Distillation 

Dewei Wang<sup>1, 2</sup> Xinmiao Wang<sup>2, 3</sup> Chenyun Zhang<sup>2</sup> Jiyuan Shi<sup>2</sup> Yingnan Zhao<sup>3</sup> Chenjia Bai<sup>2 *</sup> Xuelong Li<sup>2 *</sup> 

> 1University of Science and Technology of China 2Institute of Artificial Intelligence (TeleAI), China Telecom 

> 3Harbin Engineering University 

> _∗_ Corresponding author Website: x-loco-humanoid.github.io 


Fig. 1: X-Loco achieves vision-based generalist humanoid locomotion control. Relying solely on velocity commands without reference motions, X-Loco leverages proprioception and exteroception to traverse complex terrains, performing behaviors such as climbing up and down stairs, fall recovery, box climbing, and forward rolls. 

**_Abstract_ —While recent advances have demonstrated strong performance in individual humanoid skills such as upright locomotion, fall recovery and whole-body coordination, learning a single policy that masters all these skills remains challenging due to the diverse dynamics and conflicting control objectives involved. To address this, we introduce X-Loco, a framework for training a vision-based generalist humanoid locomotion policy. X-Loco trains multiple oracle specialist policies and adopts a synergetic policy distillation with a case-adaptive specialist selection mechanism, which dynamically leverages multiple specialist policies to guide a vision-based student policy. This design enables the student to acquire a broad spectrum of locomotion skills, ranging from fall recovery to terrain traversal and wholebody coordination skills. To the best of our knowledge, X-Loco is the first framework to demonstrate vision-based humanoid** 

**locomotion that jointly integrates upright locomotion, wholebody coordination and fall recovery, while operating solely under velocity commands without relying on reference motions. Experimental results show that X-Loco achieves superior performance, demonstrated by tasks such as fall recovery and terrain traversal. Ablation studies further highlight that our framework effectively leverages specialist expertise and enhances learning efficiency.** 

## I. INTRODUCTION 

Humanoid robots equipped with advanced algorithms have garnered significant attention due to their potential for anthropomorphic motion and versatile manipulation [52, 11, 39, 6, 47, 4, 19, 2]. As a fundamental capability, locomotion control has witnessed rapid progress facilitated by 

reinforcement learning (RL) and high-fidelity physical simulators [49, 43, 13, 36, 33, 64, 22, 19]. Recent advancements have demonstrated remarkable results, ranging from traversing challenging terrains [54, 29, 46, 14] and executing robust fall recovery [8, 20, 56] to agilely tracking highly dynamic motions [19, 28, 60, 55, 15, 68]. 

Despite these advancements, a key limitation of many existing humanoid locomotion control methods lies in their predominant focus on isolated or specific categories of locomotion skills, such as exteroception-based terrain traversal [54, 29, 46, 71] or fall recovery [22, 56, 30, 48]. This functional fragmentation renders these methods incapable of handling complex scenarios, such as autonomously resuming locomotion after a fall. Furthermore, these methods fail to achieve whole-body coordination skills, which prevents the robot from traversing challenging terrains. While motion tracking [15, 61, 66, 60, 59] and teleoperation paradigms [17, 65, 25] facilitate diverse whole-body coordination behaviors, their inference relies heavily on reference motions or human intervention via specialized devices, leaving the robot unable to autonomously perceive its surroundings and perform locomotion. Consequently, these approaches lack the necessary autonomy required for self-contained and versatile humanoid locomotion controllers. 

Developing a vision-based generalist locomotion controller capable of integrating locomotion skills ranging from terrain traversal to fall recovery, alongside contact-rich skills like box climbing, remains an open challenge in humanoid robotics. To realize such a versatile controller, several challenges must be addressed: First, reward engineering for humanoid locomotion remains inherently labor-intensive [22, 57], as formulating reward functions capable of eliciting diverse motor skills poses a significant challenge. Second, achieving wholebody coordination skills [59, 15] without reference motion introduces substantial complexity, as the absence of guidance leads to inefficient exploration within high-dimensional stateaction spaces. Third, beyond mastering diverse skills, the controller needs to leverage visual perception to understand the environment and generate appropriate, real-time responses to conditions. Lastly, while head-mounted cameras facilitate perception, camera rendering in current simulations is limited by slow or non-independent rendering across parallel environments. Achieving fast and decoupled camera rendering is essential for the efficient training of vision-based policies. 

To address these challenges, we introduce X-Loco, a framework that develops a generalist humanoid controller by distilling three privileged specialist policies, each optimized for a distinct capability: upright locomotion, fall recovery, and whole-body coordination, such as rolling and box climbing. Specifically, we implement a _Case-Adaptive Specialist Selection_ (CASS) mechanism that dynamically queries the most relevant specialist policy based on the robot’s state and the surrounding terrains giving the action guidance for the student policy. As acquiring multiple locomotion skills simultaneously is often hindered by the untrained policy inability to cover the specialists’ optimal state-action distribution, we introduce 

_Specialist Annealing Rollout_ (SAR), a dynamic ratio-based data collection strategy that incorporates a proportion of rollouts from the specialist policies for training. This mixing ratio decays as the distillation loss converges, shifting the focus toward the student policy’s own explorations while reducing noisy data in the early stages of training. To enhance robustness, _Stochastic Fall Injection_ (SFI) is implemented by applying active external disturbances during locomotion, rather than just initializing fallen states. This mechanism forces the policy to adapt to unexpected loss of balance, requiring the emergence of a transition between locomotion and emergency fall recovery. 

In summary, by distilling specialist policy expertise into a generalist policy, X-Loco expands the capabilities of existing humanoid locomotion controllers. Our primary contributions are summarized as follows: 

- We develop X-Loco, which trains three locomotion specialist policies sharing a unified action space and integrates their diverse motor skills into a generalist policy. 

- We introduce a synergetic distillation paradigm to consolidate expertise from multiple specialist policies into a single generalist policy, effectively mitigating interference between diverse locomotion skills. 

- We introduce SAR to ensure efficient expert knowledge internalization through adaptive rollout mixing, and SFI to expose the policy to failure regimes, thereby enabling transitions between locomotion and fall recovery. 

- We deploy X-Loco on the Unitree G1 robot, demonstrating its superior performance and stability across diverse terrains and challenging scenarios, thereby validating the framework’s robustness and sim-to-real transferability. 

II. RELATED WORK 

_A. Learning-based Humanoid Control_ 

_1) Upright Locomotion:_ Humanoid locomotion has evolved from blind locomotion on uneven terrains [13, 40, 67, 13], visual locomotion across complex terrains [54, 46, 29] and multiple locomotion skill learning [71, 57]. By decoupling the control of the upper and lower limbs [5, 45, 57], humanoid robots can achieve complex loco-manipulation tasks that require coordination between the entire body. However, the aforementioned methods fall short of addressing complex tasks such as fall recovery and high-difficulty whole-body coordinated movements. 

_2) Fall Recovery:_ Falling is an inevitable occurrence for legged robots. RL provides a robust and generalizable framework for fall recovery [24, 22, 8]. FIRM [56] has explored the synergy between fall-safety and fall-recovery and AHC [69] utilizes multi-task RL to simultaneously achieve both autonomous fall recovery and stable walking. Despite these advancements, integrating fall recovery with a visual locomotion controller remains an open challenge. 

_3) Motion Tracking:_ Leveraging motion retargeting [3, 63, 18] and motion imitation [37, 51, 31], humanoid robots can perform highly dynamic behaviors [19, 55, 68, 28] and universal motion tracking [15, 66, 60, 9] given reference motions. 


Fig. 2: **Overview of X-Loco** . (a) X-Loco integrates the capabilities of three specialist policies into a vision-based generalist policy via Synergetic Policy Distillation. (b) X-Loco can perform diverse locomotion skills in the real world. 

Exteroceptive information is integrated into a motion tracking framework to enable complex loco-manipulation [61] and sensorimotor locomotion [1]. Our method further eliminates the dependency on reference motions during inference, enabling the robot to autonomously perform whole-body coordination movements based on exteroceptive perception. 

## _B. Multiple Locomotion Skills Learning_ 

While developing a single policy for multiple skills is often hindered by gradient interference and task objective tradeoffs [26, 62]. Mixture-of-Experts (MoE) [7, 23] has been shown to mitigate gradient conflict in multi-skill learning and effectively facilitate the acquisition of diverse locomotion gaits [54, 21]. Methods such as MELA [58] and MTAC [44] utilize a hierarchical structure to decouple individual motor skills, which are subsequently coordinated by a high-level module. Locomotion skills with minor morphological variations can be acquired by one-stage framework leveraging reward function design [57, 35] and curriculum learning [10, 53]. 

In legged locomotion, policy distillation is widely utilized for privileged information learning [10, 17, 9] and sim-to-real transfer [61, 27]. Policy distillation enables dynamic parkour behaviors by training specialized teachers for different terrains and distilling their expertise into a single policy [70, 71]. In contrast to existing works, our framework further integrates whole-body coordination and fall recovery into a generalist policy, autonomously executed based solely on exteroceptive perception and velocity commands. 

## III. PROBLEM FORMULATION 

We formulate the humanoid locomotion control as a Markov Decision Process (MDP), defined by a tuple _M_ = ( _S, A, P, R, γ_ ) where _S_ and _A_ denote the state and action spaces, respectively. _P_ ( **_s_** _t_ +1 _|_ **_s_** _t,_ **_a_** _t_ ) represents the state transition probability, _R_ ( **_s_** _t,_ **_a_** _t_ ) : _S×A →_ R is the reward function, and _γ ∈_ [0 _,_ 1) is the discount factor. We employ proximal 

policy optimization (PPO) [43] and Generalized Advantage Estimation (GAE) [42] to train specialist policies, each optimized to maximize the expected discounted cumulative return _J_ ( _π_ ) = E _τ ∼π_ [<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtR_(</sup><sup>**_s_**</sup><sup>_t,_</sup><sup>**_a_**</sup><sup>_t_)].</sup> 

_1) State Space:_ We partition the state space _S_ into three components: the privileged state **_s_**<sup>priv</sup> _t_ , which contains information available only in simulation, proprioceptive information **_s_**<sup>prop</sup> _t_ and exteroceptive information which in our setting consists of depth images **_d_** _t ∈_ R<sup>64</sup><sup>_×_64</sup> . The proprioceptive information **_s_**<sup>prop</sup> _t_ primarily comprises: 


where **_ω_** _t ∈_ R<sup>3</sup> is the base angular velocity, **_g_** _t ∈_ R<sup>3</sup> is the gravity vector in the base frame, **_q_** _t ∈_ R<sup>23</sup> and **_q_ ˙** **_t_** _∈_ R<sup>23</sup> represent joint position and joint velocity, and **_a_** _t−_ 1 _∈_ R<sup>23</sup> is the last action. The privileged state **_s_**<sup>priv</sup> _t_ is defined as: 


where **_v_** _t ∈_ R<sup>3</sup> is the base linear velocity, _bt_ denotes the head height, and **_e_** _t ∈_ R<sup>6</sup> , **_f_** _t ∈_ R<sup>6</sup> represent the positions and velocities of the hands and feet relative to the base frame, respectively. **_h_** _t ∈_ R<sup>143</sup> denotes the local terrain height samples, while **_m_** _t ∈_ R<sup>52</sup> indicates the motion command. 

_2) Action Space:_ To ensure knowledge transfer during distillation, all policies share a consistent action space _A ∈_ R<sup>23</sup> and employ the same Proportional Derivative (PD) parameters to map the action to joint target positions: **_q_** _t_<sup>target</sup> = **_q_**<sup>default</sup> + **_α_** _·_ **_a_** _t_ , where **_q_**<sup>default</sup> represents the pre-defined default pose and **_α_** is a scaling factor following Liao et al. [28]. The joint torques **_τ_** _t_ are then computed as: 


where _Kp_ and _Kd_ denote the stiffness and damping coefficients, respectively. 

## IV. METHOD 

In this section, we introduce the pipeline of the X-Loco framework as shown in Fig 2. We first train three specialist policies: upright locomotion _πl_ , fall recovery _πr_ , and wholebody coordination _πw_ . Subsequently, we propose a synergetic policy distillation to effectively consolidate these specialized capabilities into a single generalist policy _πg_ . 

## _A. Specialist Policies Training_ 

All specialists share a unified action space and consistent DoFs. While these specialists are undeployable in real world due to their dependency on privileged state, they achieve peak performance in their respective domains. 

_1) Upright Locomotion Specialist:_ The upright locomotion specialist _πl_ is designed to establish the robot’s basic mobility, enabling navigation of diverse terrains, such as stairs, pits, and gaps, while following velocity commands **_c_** _t_ = [ _vx, vy, ωz_ ]<sup>_⊤_</sup> . We employ two encoders to process observations, alongside an actor network to predict actions. Specifically, the policy incorporates a history encoder to compress historical states comprising _{_ **_s_**<sup>prop</sup> _i ,_ **_v_** _i,_ **_e_** _i,_ **_f_** _i}_<sup>_t_</sup> _i_ = _t−_ 9<sup>overtenconsecutivetime</sup> steps into a latent representation. Simultaneously, an elevation map encoder processes **_h_** _t_ to provide a compact geometric understanding of the surrounding terrain. To ensure behavioral naturalness and enhance exploration efficiency, we incorporate the Adversarial Motion Prior (AMP) [38, 50] as a style reward to guide the policy. Consequently, _πl_ learns to track velocity commands with a natural gait across diverse terrains, providing upright locomotion guidance for the student policy. 

_2) Fall Recovery Specialist:_ The fall recovery specialist _πr_ is optimized for robot posture restoration from diverse fallen situations. Given that the objective of _πr_ is postural stabilization rather than velocity-tracking, the policy is designed to be agnostic to terrain information, i.e. **_h_** _t_ . We adopt an architecture comprising only a history encoder compressing historical state similar as _πl_ and an actor network for _πr_ . To ensure the policy can recover from arbitrary failure cases, the robot is initialized in both supine and prone postures during training, with large joint position noise added to the initial states to simulate diverse falling conditions. Furthermore, an AMP-based style reward is integrated into the training of _πr_ for avoiding jerk motions and guide the policy’s exploration. As a result, _πr_ is capable of executing recovery maneuvers, enabling the robot to regain its footing from any fallen state. 

_3) Whole-Body Coordination Specialist:_ While existing locomotion policies often lack whole-body coordination ability, we develop the whole-body coordination specialist _πw_ focusing on these skills following a motion tracking paradigm. The _πw_ consists of an elevation map encoder and an actor network. The former processes **_h_** _t_ into a latent representation, which together with **_s_**<sup>prop</sup> _t_ and **_m_** _t_ is fed into the actor network to predict actions. We employ the elevation map encoder for local terrain perception, thereby enhancing the policy’s generalization capability when tracking motions that involve terrain interaction. _πw_ is specialized in tracking motions that necessitate whole-body coordination motion like box climbing 

and rolling, rather than aiming for universal motion imitation. The subsequent distillation phase transfers these skills into a generalist policy _πg_ and eliminate its dependence on reference motions during inference. 

## _B. Synergetic Policy Distillation_ 

In the distillation process, we employ a student policy using MoE architecture that maps **_s_**<sup>prop</sup> _t_ , **_c_** _t_ and **_d_** _t_ to target joint positions, acquiring the capabilities from various specialist policies. To consolidate skills from these specialists into a generalist policy, our synergetic policy distillation employs CASS to dynamically switch specialists based on the robot’s state and terrain, while SFI and SAR collectively enhance robustness and training efficiency. 

_1) Case-Adaptive Specialist Selection:_ CASS defines three cases according to the robot state and local terrain: recovery, upright locomotion, and coordinated maneuvers. Each = case is associated with a specific specialist. Let _C {_ ( _c_ rec _, πr_ ) _,_ ( _c_ loco _, πl_ ) _,_ ( _c_ coor _, πw_ ) _}_ denotes the set of all cases and their corresponding specialist. The specific case assigned to the robot is determined by the mapping function _f_ ( _bt, It_ ), which evaluates the robot’s head height _bt_ and the current terrain context _It_ and outputs a specific case index from _C_ . A detailed definition for the mapping function is provided in Appendix C. During distillation, the target action _a_<sup>_∗_</sup> _t_<sup>is selected</sup> as: 


where **_s_** _i,t_ represents the input of the specialist policy and I is the indicator function. The termination criteria are consistent with the selected specialist policy to ensure that the collected trajectories remain within state-space manifold explored during specialist training. Notably, each specialist leverages clean privileged observations **_s_** _i,t_ for maximum performance, the student policy is trained using a noised non-privileged observation _ou,t_ . The distillation objective minimizes the mean squared error between the student’s action and the selected target action: 


Within the case _c_ coor, CASS adaptively modulates the motion commands fed into _πw_ , thereby providing the student policy with appropriate whole-body coordination skill guidance across different scenarios. Consequently, CASS provides the student policy with appropriate target action, enabling the generalist humanoid control learning including whole-body coordination, terrain traversal, and fall recovery based on proprioception and depth without requiring reference motions. 

_2) Specialist Annealing Rollout:_ Only with the CASS mechanism, training a single policy to master multiple specialist domains simultaneously is challenging. This difficulty stems from two primary issues: First, an untrained policy frequently generates trajectories that are out-of-distribution (OOD) relative to the specialists, which are difficult to filter via early termination. Second, contact-rich and whole-body 

coordination skills are hard to acquire because errors in the early stages of a maneuver prevent the agent from experiencing subsequent parts of the skill. To mitigate these challenges, we introduce SAR, which samples actions applied for the environment during data collection by switching between the student and specialist policies according to a mixing ratio _ρ_ : 


where _bt ∼_ Bernoulli( _ρ_ ) is a binary random variable governed by _ρ_ . This mixed rollout strategy reduces the occurrence of low-quality state manifolds, allowing the student policy to observe and learn from the successful behaviors of complex motion sequences before it can execute them independently. The mixing ratio _ρ_ follows an annealing schedule tied to the training progress. Specifically, we decrease _ρ_ when the distillation loss _Ldistill_ falls below a predefined threshold _ϵ_ : 


By gradually shifting from expert-driven rollouts to autonomous exploration, SAR provides a scaffold for distillation, ensuring the student policy transitions to self-exploration only after attaining a foundational mastery of the specialist’s knowledge. 

_3) Stochastic Fall Injection:_ Instead of solely initialize a subset of environments in fallen states, we propose SFI which introduces random external forces while the robot is walk or climbing, forcing the robot to enter the _crec_ regime from normal states. To ensure realism, these external force injections are not entirely stochastic, they are conditioned on specific vulnerable scenarios, such as high-speed turns or rolling motions, to simulate unpredictable real-world accidents. To prevent the student policy from being compromised by corrupted data when external forces drive the robot into OOD states relative to _πr_ , we implement an additional termination criterion when SFI is triggered. We maintain a buffer of the robot’s head height _H_ over consecutive timesteps, the episode is terminated if the variance of the buffer falls below a predefined threshold indicating that the robot has become stuck during the stand-up process: 


where _δ_ is a stability threshold. This criterion ensures that the distillation process remains focused on recoverable states by pruning trajectories where the _πr_ fails to progress. 

## _C. Training Details_ 

This section details implementation techniques used to optimize the training process. Refer to Appendix A for the complete configurations regarding the simulation environment and hardware setup, as well as reward formulations and domain randomization. 

_1) Expert Ratio Scheduling:_ We implement a hysteresisbased annealing mechanism for the expert ratio _ρ_ . Specifically, _ρ_ decays by a step size of 1e _−_ 4 per iteration only when the MSE loss falls below a lower threshold _τlow_ = 0 _._ 005. Conversely, if the loss exceeds an upper threshold _τhigh_ = 0 _._ 010, 


Fig. 3: Terrains used for training and evaluation. 

the decay process is suspended until the performance recovers (i.e., loss _< τlow_ ). This adaptive scheduling dynamically modulates the intensity of expert assistance based on the student’s real-time proficiency. The introduction of the hysteresis zone enhances the stability of _ρ_ updates and prevents premature reduction of expert support. 

_2) Stabilizing Whole-Body Specialist Distillation:_ During the pre-training of _πw_ , we incorporate elevation maps into the observation space to facilitate the perception of local terrain geometry. To mitigate overfitting to specific terrain configurations, we randomize the robot’s start position with _x_ - _y_ offsets sampled from [ _−_ 0 _._ 15m _,_ 0 _._ 15m] on box terrains. For the distillation phase, we preserve data quality by adopting the specialist’s termination criteria to exclude failed samples. 

_3) Camera Rendering:_ Current sensor rendering in simulations [33, 36] suffers from low throughput and a lack of visual isolation, where robots inadvertently perceive instances from parallel environments. Furthermore, acceleration frameworks such as NVIDIA Warp [32] often struggle to concurrently handle both dynamic and static meshes. We implement a highperformance depth rendering pipeline utilizing NVIDIA Warp to execute parallelized ray-casting. Our approach decouples the environment into static meshes representing the terrain and dynamic meshes representing the robot mesh. To optimize computational throughput, each agent’s ray-caster selectively queries the global static mesh and its own local dynamic mesh. 

## V. EXPERIMENTS 

## _A. Experiment Setup_ 

We perform training and evaluation in the IsaacLab [36] simulator. The trained policy is deployed on a Unitree G1 humanoid robot, operating at 50Hz predicting target joint positions. These targets are subsequently tracked by a 500Hz PD controller, which translates them into torques to drive the motors. 

In the simulation evaluation, we categorize the test task into three categories: **Upright Locomotion** , **Whole-Body Coordination** ( **WBC** ), and **Recovery** . The full suite of evaluation terrains is visualized in Fig. 3 and the detailed physical specifications for each terrain type are summarized in Table II. 

_1) Baselines:_ To validate the locomotion performance of the proposed framework, we compare our framework with the following baselines: 

TABLE I: Quantitative comparison of X-Loco against baselines and specialist policies. Bold numbers indicates the best performance other than the specialists, and - denotes that the method failed to complete the corresponding task. 

|||||**Locomo**|**tion**|||**Wh**|**ole-Body Coordin**|**ation**|**Recovery**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|Sl<br>_R_succ|ope<br>_D_trav|P<br>_R_succ|it<br>_D_tra|v|Stairs<br>_R_succ<br>_D_trav|¯_R_succ|Hanging Bar<br>_R_succ|Box<br>_R_succ|¯_R_succ|Flat<br>_R_succ|
|BeyondMimic [28]|-|-|-|-||-<br>-|-|**1.000** _±_ .000|**0.916** _±_ .008|**0.958** _±_ .004|-|
|MoRE [54]|**0.992** _±_ .008|7.863 _±_ .018|0.844 _±_ .009|6.833 _±_|.114|0.926 _±_ .009<br>7.387 _±_ .013|0.921 _±_ .009|-|-|-|-|
|PPO [43]|0.823 _±_ .021|6.674 _±_ .152|0.793 _±_ .018|6.396 _±_|.184|0.781 _±_ .025<br>6.565 _±_ .141|0.799 _±_ .021|-|-|-|-|
|AHC [69]|0.968 _±_ .005|7.871 _±_ .022|0.403 _±_ .031|3.179 _±_|.254|0.278 _±_ .042<br>2.524 _±_ .311|0.550 _±_ .026|-|-|-|**1.000** _±_ .000|
|Locomotion Specialist|0.995 _±_ .002|7.989 _±_ .011|0.984 _±_ .010|7.914 _±_|.135|0.991 _±_ .011<br>7.963 _±_ .004|0.990 _±_ .008|-|-|-|-|
|Whole-Body Specialist|-|-|-|-||-<br>-|-|1.000 _±_ .000|1.000 _±_ .000|1.000 _±_ .000|-|
|Recovery Specialist|-|-|-|-||-<br>-|-|-|-|-|1.000 _±_ .000|
|**Ours (X-Loco)**|0.982 _±_ .010|**7.984** _±_ .033|**0.878** _±_ .015|**7.592** _±_|.084|**0.958** _±_ .007<br>**7.853** _±_ .011|**0.939** _±_ .011|0.873 _±_ .014|0.868 _±_ .018|0.871 _±_ .016|**1.000** _±_ .000|
|TABLE II: <br>Skill|Terrain Ci<br>Obstacle Pr|onfigurati<br>operties|ions for E<br>Ran|valuati<br>ges|on<br>Uni|t<br>**right **<br>postur<br>_•_ **Trave**|**Locomoti**<br>e and bala<br>**rsal Dista**|**on** and <br>ncing fo<br>**nce (**_D_**tr**|**WBC** task; <br>r 5s for th<br>**av):** The a|regaining<br>e **Recove**<br>verage di|a standi<br>**ry** task.<br>stance tr|
||slope incline||[15_,_|20]|_◦_|eled a|long the|_x_-axis|prior to f|ailure or|timeout|
|Locomotion|pit obstacle|height|[0_._30_,_|0_._40]|m|assess|ed in the|**Upright **|**Locomotio**|**n** tasks.||
||stair step he|ight|[0_._10_,_|0_._15]|m|||||||
|Whole-Body|obstacle ver|tical clearanc|e<br>[0_._87_,_|0_._95]|m|_B. Simulati_|_on Result_|_s_||||
|Coordination|obstacle hei|ght|[0_._50_,_|0_._65]|m|_1) Comp_<br>|_arative A_<br>|_nalysis:_ <br>|We cond<br>|uct a co<br>|mprehensi<br>|
|Recovery|flat ground||-||-|quantitative<br>ilid|comparis<br>ilit|on betw<br>d|een our pr<br>lbli|oposed X<br>Th|-Loco, s<br>lt|


   - **right Locomotion** and **WBC** task; regaining a standing posture and balancing for 5 s for the **Recovery** task. 

- **Traversal Distance (** _D_ **trav):** The average distance traveled along the _x_ -axis prior to failure or timeout is assessed in the **Upright Locomotion** tasks. 

_1) Comparative Analysis:_ We conduct a comprehensive quantitative comparison between our proposed X-Loco, specialized specialists, and several baselines. The results are summarized in Table I. 

_a) Specialist vs. Baselines:_ As expected, the specialist policies consistently achieve the highest performance in their respective domains. For instance, the locomotion specialist achieves a near-perfect average success rate _R_<sup>¯</sup> succ of 0 _._ 990 and the whole-body specialist achieves perfect performance with _R_ ¯succ at 1 _._ 000. The superior performance over the baseline in the box climbing task stems from to the utilization of the information in **_h_** _t_ . This results is primarily attributed to the use of privileged information and a focused training objective on a single category of tasks which allows these policies to establish the performance upper bound for each skill. 

- **BeyondMimic [28]:** A baseline focuses on whole-body coordination motion tracking relying solely on proprioception. We compare against it to highlight the necessity of exteroception for interacting with environments. 

- **MoRE [54]:** This baseline employs a two-stage pipeline training a vision-based policy to achieve robust locomotion across complex terrains. 

- **AHC [69]:** This baseline implements an adaptive blind control policy that unifies locomotion with autonomous fall recovery behaviors. 

- **PPO [43]:** The baseline trains a policy using PPO with depth inputs to traverse across all terrains. 

_b) X-Loco vs. Baselines:_ Our generalist policy demonstrates significant versatility compared to the baselines. While BeyondMimic excels in **WBC** tasks with an average _R_<sup>¯</sup> succ of 0 _._ 958 but lacks locomotion and recovery capabilities, and MoRE and AHC show competitive results in locomotion but fail completely in **WBC** task, X-Loco successfully masters all three tasks. In the **Upright Locomotion** task, X-Loco achieves an average success rate of 0 _._ 939. This performance outperforms the PPO baseline at 0 _._ 799 and AHC at 0 _._ 550 by a large margin, while remaining highly competitive with MoRE. In the **WBC** task, X-Loco maintains a success rate of 0 _._ 871 without relying on reference motions, whereas other baselines lacking such references fail to execute these tasks. 

- **Our Specialists:** We evaluate the individual specialist policies ( _πl_ , _πr_ and _πw_ ) separately. 

To assess the specific contributions of our proposed components, we also evaluate several ablation baselines: 

- **Ours w/o CASS:** An ablation to evaluate whether CASS facilitates the acquisition diverse locomotion skills. 

- **Ours w/o SFI:** An ablation to evaluate whether SFI helps to enhance the policy’s robustness. 

- **Ours w/o SAR:** An ablation to analyze SAR’s contribution to the policy distillation process. 

- **Ours w/o MoE:** Ablation of policy network with the MoE replaced by a Multi-Layer Perceptron (MLP). 

_c) Specialist vs. X-Loco:_ The performance gap between X-Loco and the specialist policies is remarkably narrow. In the **Upright Locomotion** task, X-Loco recovers approximately 94 _._ 8% of the specialist’s success rate. In the **Recovery** task, X-Loco matches the specialist with a perfect 1 _._ 000 success rate. While X-Loco exhibits the most pronounced performance degradation in the **WBC** tasks, this underscores the difficulty of mastering vision-based whole-body coordination skills without reliance on reference motions. These results indicate 

- **MoE-** _N_ : Variants of our framework with _N ∈{_ 2 _,_ 3 _}_ experts to investigate the sensitivity of performance to _N_ , where **MoE-2** serves as our adopted architecture. 

- _2) Metrics:_ We quantify performance using two primary 

- metrics: 

- **Success Rate (** _R_ **succ):** The percentage of episodes where the task objective is fully met. Success is defined as: traversing the entire 8 m track without falling for the **Up-** 


Fig. 4: **Top** : Testing the generalist policy on hybrid, challenging terrains. **Bottom** : Extensibility of the X-Loco to include vision-guided (a) lateral sidling and (b) kneeling crawling. 

TABLE III: Quantitative results of ablation analysis on CASS and MoE architectures. 

|**Method**|**Locomotion**<br>¯_R_succ|**Whole-Body**<br>**Coordination**<br>¯_R_succ|**Recovery**<br>_R_succ|**Average**<br>¯_R_succ|
|---|---|---|---|---|
|Ours w/o CASS|0.903|0.446|**1.000**|0.783|
|Ours w/o MoE|0.692|0.561|0.996|0.749|
|MoE-3|0.628|0.709|**1.000**|0.779|
|**MoE-2 (Ours)**|**0.939**|**0.845**|**1.000**|**0.928**|


that X-Loco can effectively distill and integrate diverse expert knowledge into a single policy without significant performance degradation, despite the inherent challenges of multi-task learning and potential gradient interference between different skills. 

_2) Ablation Analysis:_ We conduct a comprehensive ablation study on CASS, MoE architecture, SAR and SFI. 

_a) Effectiveness of CASS:_ To evaluate the contribution of CASS, we compare our method against the variant **Ours w/o CASS** . As reported in Table III, the absence of CASS leads to a drastic performance collapse in both **WBC** and **Upright Locomotion** tasks. The primary driver of this degradation is that without the selection mechanism, the distillation process lacks critical training samples representing the transition phases between heterogeneous motor patterns. Specifically, the student policy is not exposed to the specific state-action pairs required to bridge disparate skills. In summary, CASS is essential for providing the guidance to synthesize specialized specialist into a generalist policy, ensuring the emergent generalist policy maintains high fidelity to specialist capabilities while mastering the connective dynamics between them. 

_b) Ablations on MoE Architecture:_ We evaluate **Our w/o MoE** and **MoE-3** across all test tasks and report the average success rate. As shown in Table III, the **Ours w/o MoE** variant struggles to maintain high success rates across all tasks, with performance dropping significantly in **WBC** 


tasks. This confirms that the MLP backbone lacks the capacity to reconcile state-action distributions from multiple specialists into a shared parameter space. While the **MoE-2** significantly recovers performance, further increasing the number of experts ( **MoE-3** ) leads to a regression, particularly in **Upright Locomotion** tasks. We attribute this to the fact that an excessive number of experts can lead to sparse updates and sub-optimal expert utilization during the distillation process. 

_c) Ablations on SAR & SFI:_ As shown in Fig. 5, our method demonstrates a clear advantage in distillation loss over the **Ours w/o SAR** baseline. In the early training phase, the loss decreases rapidly as the policy focuses on high-quality samples from the specialists. As _ρ_ decays, the student policy begins to utilize its own rollout data including non-optimal or failed trajectories to learn to adapt complex situations, leading to a rise in loss. Ultimately, X-Loco achieves faster convergence to a lower terminal loss. This confirms that SAR effectively bridges specialist guidance and self-exploration, ensuring more efficient policy distillation. To evaluate the role of SFI, we assess the policy’s performance in **Upright Locomotion** and **WBC** tasks under large external disturbances that lead to falls. We measure the success rate after falling to quantify the recovery capability. As shown in Table IV, the variant with SFI achieves a higher success rate, demonstrating that SFI significantly enhances the policy’s ability to regain balance in unpredictable environments. 

## _C. More Analysis_ 

_1) Hybrid Terrain:_ We further evaluated the robustness and skill integration of the generalist policy by constructing a challenging hybrid terrain sequence that requires continuous navigation across diverse obstacles. In this experiment, the robot is initialized in a fallen state and must sequentially perform fall recovery, climb up and down stairs, roll under a hanging bar, and finally climb a box. This is a longhorizon task using depth information, as shown in Fig 4. It can even recover after being pushed off a high platform and subsequently resume the climbing task. This successful traversal across such a challenging terrain proves that our framework effectively consolidates diverse skills into a single policy, enabling the robot to execute multifaceted movements while maintaining inherent adaptability. 

_2) Framework Extensibility:_ X-Loco enables the capability expansion of the generalist policy by expanding motions learned by the whole-body coordination specialist and sub- 


Fig. 6: **Left** : (a) fall recovery and platform traversal; (b) resilience to external disturbances; (c) a continuous sequence of recovery, stair climbing, and rolling under an overhead bar. **Right** : (Top) a failure case where the robot trips due to lack of camera randomization. (Bottom, from left to right) original depth in simulation, noisy depth, and processed real-world depth. 

sequently adjusting CASS and terrains during the distillation process. Fig. 4 illustrates two examples of capability expansion: lateral movement through narrow gaps and crawling under low-overhanging obstacles. The results demonstrate that the distilled generalist policy _πg_ successfully mastered these skills: when encountering narrow gaps, the robot autonomously transitions to a sidling posture to traverse the terrain; when faced with low-clearance obstacles, the robot spontaneously adopts a crawling gait to pass under the obstacles. This capability underscores the versatility and extensibility of our framework. By simply enriching the specialist’s training set, the generalist policy can effectively integrate new wholebody coordination skills, proving that X-Loco is a scalable solution for humanoid locomotion control. 

with obstacles followed by falls or continuous foot scuffing against the ground during locomotion. To bridge the depth sim-to-real gap, we implement a multi-stage pipeline that synthesizes realistic depth data by injecting additive Gaussian noise and blurring to emulate real-world sensor. Furthermore, we employ domain randomization over the camera’s extrinsic and intrinsic parameters, including random perturbations of its orientation, position, and field of view (FOV). For real-world depth images, we apply hole-filling and Gaussian filtering to mitigate sensor noise and data sparsity. As illustrated in Fig. 6, this preprocessing ensures consistent image alignment between simulation and reality, enabling the policy to achieve successful sim-to-real transfer. 

## VI. CONCLUSION 

## _D. Real-World Deployment_ 

_a) Performance on Hybird Terrains:_ To validate the robustness and versatility of X-Loco in the real world, we deployed the generalist policy on a Unitree G1 robot. Fig. 1 illustrates the performance of X-Loco across diverse challenging terrains, including a 90cm-high hanging bar and a 60cm-tall box. In a series of comprehensive tests, the robot successfully manifested a seamless transition between the three core locomotion abilities. Fig. 6 demonstrates X-Loco’s performance across various composite terrains under disturbances. The policy successfully executes a series of continuous maneuvers, including recovering from a fall, traversing high platforms, climbing stairs, and performing a rolling motion to pass under a hanging bar. Furthermore, the experimental results confirm the policy’s exceptional resilience. When subjected to severe external disturbances or manual pushes that result in a fall, the policy autonomously regains an upright posture and resumes locomotion. The experiment results demonstrate that the capabilities integrated via our distillation pipeline generalize effectively to physical hardware. 

_b) Depth Sim-to-Real Analysis:_ Transitioning the policy from simulation to the real world reveals a large depth sim-toreal gap, which significantly degrades the policy’s performance as shown in Fig. 6. The policy suffers from perception-action mismatches caused by depth disparities, resulting in collisions 

We present X-Loco, a framework that enables a single vision-based policy to achieve generalist humanoid control via velocity commands. By employing synergetic policy distillation, X-Loco consolidates three specialist policies into a unified agent. SAR and SFI are introduced to bridge the gap between expert guidance and autonomous exploration, and to enhance the policy’s recovery resilience, respectively. Experimental results demonstrate that X-Loco achieves successful integration of diverse locomotion skills with performance comparable to that of the specialists, offering a scalable solution for generalist humanoid locomotion. Real-world deployments further confirm its capability to manage complex environments, pushing the boundaries of humanoid locomotion. 

## VII. LIMITATIONS AND FUTURE WORK 

Despite its advancements, X-Loco has limitations. Its performance is primarily constrained by a limited sensory horizon due to the narrow-FOV camera, and the difficulty of perfectly modeling real-world sensor noise. Additionally, since the distillation relies on behavior cloning, the policy is inherently bounded by the specialists’ performance, making X-Loco less effective in edge cases lacking expert coverage. 

Future work will follow two directions. First, we will integrate multi-modal sensing (e.g., RGB-D and LiDAR) to broaden the perceptual field and rectify misjudgments through 

cross-modal calibration. Second, we aim to develop a hybrid learning framework that combines distillation with RL-based fine-tuning, allowing the policy to explore and generalize beyond specialist demonstrations. 

## REFERENCES 

- [1] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [2] Hongjun An, Wenhan Hu, Sida Huang, Siqi Huang, Ruanjun Li, Yuanzhi Liang, Jiawei Shao, Yiliang Song, Zihan Wang, Cheng Yuan, et al. Ai flow: Perspectives, scenarios, and approaches. _Vicinagearth_ , 3(1):1, 2026. 

- [3] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] Tamim Asfour, Pedram Azad, Nikolaus Vahrenkamp, Kristian Regenstein, Alexander Bierbaum, Kai Welke, Joachim Schroeder, and Ruediger Dillmann. Toward humanoid manipulation in human-centred environments. _Robotics and Autonomous Systems_ , 56(1):54–65, 2008. 

- [5] Qingwei Ben, Feiyu Jia, Jia Zeng, Junting Dong, Dahua Lin, and Jiangmiao Pang. Homie: Humanoid locomanipulation with isomorphic exoskeleton cockpit. _arXiv preprint arXiv:2502.13013_ , 2025. 

- [6] Aude Billard and Danica Kragic. Trends and challenges in robot manipulation. _Science_ , 364(6446):eaat8414, 2019. 

- [7] Onur Celik, Aleksandar Taranovic, and Gerhard Neumann. Acquiring diverse skills using curriculum reinforcement learning with mixture of experts. In _International Conference on Machine Learning_ , pages 5907– 5933. PMLR, 2024. 

- [8] Penghui Chen, Yushi Wang, Changsheng Luo, Wenhan Cai, and Mingguo Zhao. Hifar: Multi-stage curriculum learning for high-dynamics humanoid fall recovery. _arXiv preprint arXiv:2502.20061_ , 2025. 

- [9] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv:2506.14770_ , 2025. 

- [10] Xuxin Cheng, Kexin Shi, Ananye Agarwal, and Deepak Pathak. Extreme parkour with legged robots. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11443–11450. IEEE, 2024. 

- [11] Kourosh Darvish, Luigi Penco, Joao Ramos, Rafael Cisneros, Jerry Pratt, Eiichi Yoshida, Serena Ivaldi, and Daniele Pucci. Teleoperation of humanoid robots: A survey. _IEEE Transactions on Robotics_ , 39(3):1706– 1727, 2023. 

- [12] Alejandro Escontrela, Xue Bin Peng, Wenhao Yu, Tingnan Zhang, Atil Iscen, Ken Goldberg, and Pieter Abbeel. Adversarial motion priors make good substitutes 

for complex reward functions. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 25–32. IEEE, 2022. 

- [13] Xinyang Gu, Yen-Jen Wang, and Jianyu Chen. Humanoid-gym: Reinforcement learning for humanoid robot with zero-shot sim2real transfer. _arXiv preprint arXiv:2404.05695_ , 2024. 

- [14] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. _arXiv preprint arXiv:2408.14472_ , 2024. 

- [15] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [16] F´elix G Harvey, Mike Yurick, Derek Nowrouzezahrai, and Christopher Pal. Robust motion in-betweening. _ACM Transactions on Graphics (TOG)_ , 39(4):60–1, 2020. 

- [17] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [18] Tairan He, Zhengyi Luo, Wenli Xiao, Chong Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Learning humanto-humanoid real-time whole-body teleoperation. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8944–8951. IEEE, 2024. 

- [19] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbab, Chaoyi Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [20] Xialin He, Runpei Dong, Zixuan Chen, and Saurabh Gupta. Learning getting-up policies for real-world humanoid robots. _arXiv preprint arXiv:2502.12152_ , 2025. 

- [21] Runhan Huang, Shaoting Zhu, Yilun Du, and Hang Zhao. Moe-loco: Mixture of experts for multitask locomotion. _arXiv preprint arXiv:2503.08564_ , 2025. 

- [22] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standingup control across diverse postures. _arXiv preprint arXiv:2502.08378_ , 2025. 

- [23] Robert A Jacobs, Michael I Jordan, Steven J Nowlan, and Geoffrey E Hinton. Adaptive mixtures of local experts. _Neural computation_ , 3(1):79–87, 1991. 

- [24] Heejin Jeong and Daniel D Lee. Efficient learning of stand-up motion for humanoid robots with bilateral symmetry. In _2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1544– 1549. IEEE, 2016. 

- [25] Mazeyu Ji, Xuanbin Peng, Fangchen Liu, Jialong Li, Ge Yang, Xuxin Cheng, and Xiaolong Wang. Ex- 

body2: Advanced expressive humanoid whole-body control, 2025. URL https://arxiv.org/abs/2412.13196. 

- [26] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. Mt-opt: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ , 2021. 

- [27] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. _arXiv preprint arXiv:2107.04034_ , 2021. 

- [28] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [29] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9997–10003. IEEE, 2025. 

- [30] Dingsheng Luo, Yaoxiang Ding, Zidong Cao, and Xihong Wu. A multi-stage approach for efficiently learning humanoid robot stand-up behavior. In _2014 IEEE international conference on mechatronics and automation_ , pages 884–889. IEEE, 2014. 

- [31] Zhengyi Luo, Jinkun Cao, Kris Kitani, Weipeng Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [32] Miles Macklin. Warp: A high-performance python framework for gpu simulation and graphics. https://github.com/ nvidia/warp, March 2022. NVIDIA GPU Technology Conference (GTC). 

- [33] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [34] Xudong Mao, Qing Li, Haoran Xie, Raymond YK Lau, Zhen Wang, and Stephen Paul Smolley. Least squares generative adversarial networks. In _Proceedings of the IEEE international conference on computer vision_ , pages 2794–2802, 2017. 

- [35] Gabriel B Margolis and Pulkit Agrawal. Walk these ways: Tuning robot control for generalization with multiplicity of behavior. In _Conference on Robot Learning_ , pages 22–31. PMLR, 2023. 

- [36] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Mu˜noz, Xinjie Yao, Ren´e Zurbr¨ugg, Nikita Rudin, et al. Isaac lab: A gpu-accelerated simulation framework for multimodal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [37] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel 

Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [38] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [39] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [40] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 9(89):eadi9579, 2024. 

- [41] Nikita Rudin, David Hoeller, Philipp Reist, and Marco Hutter. Learning to walk in minutes using massively parallel deep reinforcement learning. In _Conference on robot learning_ , pages 91–100. PMLR, 2022. 

- [42] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous control using generalized advantage estimation. _arXiv preprint arXiv:1506.02438_ , 2015. 

- [43] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [44] Nishaant Shah, Kshitij Tiwari, and Aniket Bera. Mtac: Hierarchical reinforcement learning-based multi-gait terrain-adaptive quadruped controller. _arXiv preprint arXiv:2401.03337_ , 2023. 

- [45] Jiyuan Shi, Xinzhe Liu, Dewei Wang, Ouyang Lu, S¨oren Schwertfeger, Chi Zhang, Fuchun Sun, Chenjia Bai, and Xuelong Li. Adversarial locomotion and motion imitation for humanoid policy learning. _arXiv preprint arXiv:2504.14305_ , 2025. 

- [46] Haolin Song, Hongbo Zhu, Tao Yu, Yan Liu, Mingqi Yuan, Wengang Zhou, Hua Chen, and Houqiang Li. Gait-adaptive perceptive humanoid locomotion with realtime under-base terrain reconstruction. _arXiv preprint arXiv:2512.07464_ , 2025. 

- [47] Haoming Song, Delin Qu, Yuanqi Yao, Qizhi Chen, Qi Lv, Yiwen Tang, Modi Shi, Guanghui Ren, Maoqing Yao, Bin Zhao, et al. Hume: Introducing system-2 thinking in visual-language-action model. _arXiv preprint arXiv:2505.21432_ , 2025. 

- [48] J¨org St¨uckler, Johannes Schwenk, and Sven Behnke. Getting back on two feet: Reliable standing-up routines for a humanoid robot. In _IAS_ , pages 676–685, 2006. 

- [49] Richard S Sutton, Andrew G Barto, et al. _Introduction to reinforcement learning_ , volume 135. MIT press Cambridge, 1998. 

- [50] Annan Tang, Takuma Hiraoka, Naoki Hiraoka, Fan Shi, Kento Kawaharazuka, Kunio Kojima, Kei Okada, and Masayuki Inaba. Humanmimic: Learning natural loco- 

motion and transitions for humanoid robot via wasserstein adversarial imitation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13107–13114. IEEE, 2024. 

- [51] Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physicsbased character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 43(6):1–21, 2024. 

- [52] Yuchuang Tong, Haotian Liu, and Zhengtao Zhang. Advancements in humanoid robots: A comprehensive review and future prospects. _IEEE/CAA Journal of Automatica Sinica_ , 11(2):301–328, 2024. 

- [53] Dewei Wang, Chenjia Bai, Chenhui Li, Jiyuan Shi, Yan Ding, Chi Zhang, and Bin Zhao. Skill-nav: enhanced navigation with versatile quadrupedal locomotion via waypoint interface. _Vicinagearth_ , 2(1):7, 2025. 

- [54] Dewei Wang, Xinmiao Wang, Xinzhe Liu, Jiyuan Shi, Yingnan Zhao, Chenjia Bai, and Xuelong Li. More: Mixture of residual experts for humanoid lifelike gaits learning on complex terrains. _arXiv preprint arXiv:2506.08840_ , 2025. 

- [55] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- [56] Zhengjie Xu, Ye Li, Kwan-yee Lin, and Stella X Yu. Unified humanoid fall-safety policy from a few demonstrations. _arXiv preprint arXiv:2511.07407_ , 2025. 

- [57] Yufei Xue, Wentao Dong, Minghuan Liu, Weinan Zhang, and Jiangmiao Pang. A unified and general humanoid whole-body controller for fine-grained locomotion. _arXiv e-prints_ , pages arXiv–2502, 2025. 

- [58] Chuanyu Yang, Kai Yuan, Qiuguo Zhu, Wanming Yu, and Zhibin Li. Multi-expert learning of adaptive legged locomotion. _Science Robotics_ , 5(49):eabb2174, 2020. 

- [59] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

   - [63] Kevin Zakka. Mink: Python inverse kinematics based on MuJoCo, December 2025. URL https://github.com/ kevinzakka/mink. 

   - [64] Kevin Zakka, Baruch Tabanpour, Qiayuan Liao, Mustafa Haiderbhai, Samuel Holt, Jing Yuan Luo, Arthur Allshire, Erik Frey, Koushil Sreenath, Lueder A Kahrs, et al. Mujoco playground. _arXiv preprint arXiv:2502.08844_ , 2025. 

   - [65] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

   - [66] Weishuai Zeng, Shunlin Lu, Kangning Yin, Xiaojie Niu, Minyue Dai, Jingbo Wang, and Jiangmiao Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

   - [67] Qiang Zhang, Peter Cui, David Yan, Jingkai Sun, Yiqun Duan, Gang Han, Wen Zhao, Weining Zhang, Yijie Guo, Arthur Zhang, et al. Whole-body humanoid robot locomotion with human reference. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 11225–11231. IEEE, 2024. 

   - [68] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

   - [69] Yingnan Zhao, Xinmiao Wang, Dewei Wang, Xinzhe Liu, Dan Lu, Qilong Han, Peng Liu, and Chenjia Bai. Towards adaptive humanoid control via multi-behavior distillation and reinforced fine-tuning. _arXiv preprint arXiv:2511.06371_ , 2025. 

   - [70] Ziwen Zhuang, Zipeng Fu, Jianren Wang, Christopher Atkeson, S¨oren Schwertfeger, Chelsea Finn, and Hang Zhao. Robot parkour learning. In _Conference on Robot Learning (CoRL)_ , 2023. 

   - [71] Ziwen Zhuang, Shenzhe Yao, and Hang Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 

- [60] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- [61] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [62] Tianhe Yu, Saurabh Kumar, Abhishek Gupta, Sergey Levine, Karol Hausman, and Chelsea Finn. Gradient surgery for multi-task learning. _Advances in neural information processing systems_ , 33:5824–5836, 2020. 

## APPENDIX 

## _A. Experimental Setup Details_ 

_1) Simulation Environment and Robot Configuration:_ We conduct training and evaluation in the Isaac Lab simulator [36]. The physics simulation operates at 200 Hz, while the policy runs at 50 Hz, with a decimation factor of 4. For real-world evaluation, we use the Unitree G1 humanoid robot, which is equipped with an Intel RealSense D435i and has 23 actuated degrees of freedom (6 per leg, 4 per arm, and 3 in the waist). The robot is equipped with a Jetson Orin NX for onboard computation. We assign different _Kp, Kd_ parameters and action scales for each joint as shown in Table V, following the setup in [28]. 

TABLE V: PD Controller Parameters and Action Scaling 

|Joint Names|_Kp_ (N_·_m/rad)|_Kd_ (N_·_m_·_s/rad)|Action Scale|
|---|---|---|---|
|Hip Roll, Knee|99_._10|6_._31|0_._35|
|Hip Pitch, Hip Yaw, Waist Yaw|40_._18|2_._56|0_._55|
|Ankle (P/R), Waist (R/P)|28_._50|1_._81|0_._44|
|Shoulder (P/R/Y), Elbow|14_._25|0_._91|0_._44|


_2) Reward Formulation:_ The formulation of reward functions and their respective weights for the three specialist policies ( _π_ l _, π_ r _, π_ w) are detailed in Table IX–XI. To facilitate the emergence of naturalistic motion patterns, we incorporate an Adversarial Motion Prior (AMP) reward into the training of the upright locomotion ( _π_ l) and fall recovery ( _π_ r) specialists. The mathematical formalization of the AMP reward and its optimization objectives are provided in Appendix B. 

_3) Domain Randomization:_ We implement a consistent Domain Randomization (DR) configuration during the specialist policy training and generalist policy distillation to facilitate robust sim-to-real transfer. Our DR mainly involves randomizing physical parameters, initial states, and actuator dynamics. Specifically, we vary ground friction and inertial properties to handle environmental diversity, while applying external force perturbations to simulate real-world uncertainties. The full randomization configuration is listed in Table VI. 

TABLE VI: Domain Randomization Parameters. ( _U_ [ _·_ ]: uniform distribution) 

|Domain Randomization|Sampling Distribution|Unit|
|---|---|---|
|Static friction|_µ_static _∼U_[0_._6_,_1_._0]|-|
|Dynamic friction|_µ_dynamic _∼U_[0_._4_,_0_._8]|-|
|Torso payload mass|_m_payload _∼U_[_−_1_._0_,_5_._0]|kg|
|Initial joint positions|_θ_init _∼U_[0_._8_,_1_._2]_× θ_nominal|-|
|External push interval|∆_t_push _∼U_[5_._0_,_8_._0]|s|
|Push linear velocity|_vx, vy ∼U_[_−_0_._5_,_0_._5]_, vz ∼U_[_−_0_._2_,_0_._2]|m/s|
|Push angular velocity|_ωr, ωp ∼U_[_−_0_._52_,_0_._52]_, ωy ∼U_[_−_0_._78_,_0_._78]|rad/s|
|Actuator stiffness _Kp_|_kp ∼U_[0_._8_,_1_._2]_× Kp,_nominal|-|
|Actuator damping _Kd_|_kd ∼U_[0_._8_,_1_._2]_× Kd,_nominal|-|


_4) Terrain Curriculum:_ We adopt an adaptive terrain curriculum inspired by [41] for the training of _πl_ and _πg_ , which automatically modulates terrain difficulty based on agent performance. The environment is structured as a 10 _×_ 20 grid 

of 8m _×_ 8m patches, encompassing five distinct terrain types: slopes, pits, hanging bars, stairs, and boxes. The difficulty is scaled by adjusting geometric parameters: slopes range from 0<sup>_◦_</sup> to 20<sup>_◦_</sup> ; pits vary in height from 0 _._ 05m to 0 _._ 3m; hanging bars enforce vertical clearance constraints of 0 _._ 67m to 0 _._ 72m; stair step heights range from 0m to 0 _._ 15m; and climbing boxes vary in height from 0 _._ 45m to 0 _._ 65m. 

_5) Training Implementation Details:_ In this section, we detail the neural network architectures and the training parameters for both the specialist and generalist policies. 

_a) Specialist Policy Architecture:_ The specialist policies ( _π_ l _, π_ r _, π_ w) are trained using the Actor-Critic framework and comprise some or all of the following modules: 

- **History Encoder:** An MLP with hidden units [1024 _,_ 512 _,_ 128], utilized by _π_ l _, π_ r. 

- **Elevation Map Encoder:** A 3-layer MLP [128 _,_ 64 _,_ 32] employed by _π_ l and _π_ w to process local terrain geometry. 

- **Privileged Proprioception Encoder:** A 3-layer MLP [128 _,_ 64 _,_ 32] for _π_ l to encode privileged states. 

- **Actor Head and Critic:** Both networks are modeled as 3-layer MLPs with dimensions [512 _,_ 256 _,_ 128]. For the fall recovery specialist _π_ r, we adopt a multi-critic structure [22] comprising four independent critics. 

_b) Generalist Policy Architecture:_ The generalist policy _πg_ leverages a Mixture-of-Experts (MoE) architecture, where a gating network modulates the contributions of experts. The experts and the gating network are instantiated as 3-layer MLPs [512 _,_ 256 _,_ 128]. To incorporate exteroception, a CNNbased depth encoder is employed to compress sequential depth images into a 128-dimensional latent representation. In parallel, a history encoder is utilized to process proprioceptive sequences over a 10-step horizon. This temporal context, combined with the latent representation from the depth encoder, is subsequently fed into the MoE to predict the actions. 

_c) Training Hyperparameters:_ Specialist policies are trained via PPO [43], while the generalist policy is distilled using supervised behavior cloning. Detailed training hyperparameters are provided in Table VII. 

TABLE VII: Optimization Hyperparameters for Specialists and Generalist Policies 

|**Hyperparameter**|**Specialist Training **|**(PPO)**|**Generalist Distillation**|
|---|---|---|---|
|Number of environments|4096||4096|
|Learning rate|1_._0_×_10<sup>_−_3 </sup>(Ada|ptive)|1_._0_×_10<sup>_−_3 </sup>(Fixed)|
|Num. epochs per iteration|5||8|
|Num. mini-batches|4||12|
|Steps per training batch|24||12|
|Discount factor (_γ_)|0.99||-|
|GAE parameter (_λ_)|0.95||-|
|PPO clip parameter (_ϵ_)|0.2||-|
|Entropy coefficient|0.005||-|
|Desired KL divergence|0.01||-|
|**Total Training Iterations**||||
|Upright Locomotion (_π_l)||30,000||
|Recovery (_π_r)||10,000||
|Whole-Body Coordination (_π_w)||50,000||
|Generalist Policy (_π_g)||30,000||


**Algorithm 1** Synergetic Policy Distillation 

- **Require:** Set _C_ = _{_ ( _crec, πr_ ) _,_ ( _cloco, πl_ ) _,_ ( _ccoor, πw_ ) _}_ , ratio _ρ_ , decay ∆ _ρ_ , threshold _ϵ_ 

- 1: Initialize storage buffer _D_ and student policy _πθ_ 2: **for** iteration = 1 _,_ 2 _, . . ._ **do** 3: Clear storage _D_ 4: // **Data Collection with SAR and SFI** 5: **for** step _t_ = 1 to _T_ in _N_ parallel environments **do** 6: Get student state _ou,t_ and privileged states _si,t_ . 7: **SFI:** Inject external forces based on context. 8: Determine case index _i ← f_ ( _bt, It_ ) and select corresponding specialist _πi_ . 

- 9: Get expert action: _a_<sup>_∗_</sup> _t_<sup>_←πi_(</sup><sup>_si,t_).</sup> 

- 10: Get student action: _a_<sup>_u_</sup> _t_<sup>_←πu_(</sup><sup>_ou,t_).</sup> 11: **SAR:** Sample _bt ∼_ Bernoulli( _ρ_ ): 12: _aenv ← bta_<sup>_∗_</sup> _t_<sup>+ (1</sup><sup>_−bt_)</sup><sup>_au_</sup> _t_ 13: Execute _aenv_ , and store ( _ou,t, at_<sup>_∗_)in</sup><sup>_D_.</sup> 14: **Termination: if** specialist _πi_ termination criteria met **or** SFI-specific failure (Eq. 5) **then** reset env 

- 15: **end for** 16: // **Policy Optimization** 17: **for** epoch = 1 to _K_ **do** 18: Sample minibatches from _D_ . 19: _Ldistill ←_ MSE( _πu_ ( _ou,t_ ) _, at_<sup>_∗_).</sup> 20: Update _θ_ via gradient descent to minimize _Ldistill_ . 21: **end for** 22: // **Specialist Annealing Schedule** 23: **if** _Ldistill < ϵ_ **then** 24: _ρ ←_ max(0 _, ρ −_ ∆ _ρ_ ) 25: **end if** 26: **end for** 

_6) Training Pseudocode:_ We present the training procedure for the generalist policy _π_ g in Algorithm 1. 

TABLE VIII: Depth Augmentation and Camera Randomization Parameters. ( _U_ [ _·_ ]: uniform distribution) 

|**Camera Randomization**|**Value / Range**|**Unit**|
|---|---|---|
|Gaussian noise|_σ_noise = 0_._02|m|
|Gaussian filter kernel|_k ∈{_3_×_3_}_|pixel|
|Gaussian filter sigma|_σ_filter = 1_._0|-|
|Camera position|∆_x,_∆_y,_∆_z ∼U_[_−_0_._05_,_0_._05]|m|
|Camera rotation|_θ_pitch _∼U_[_−_10_,_5], _θ_roll_, θ_yaw _∼U_[_−_1_,_1]|_◦_|
|Camera horizontal FOV|∆FOVh _∼U_[_−_10_,_10]|_◦_|


## _B. Adversarial Motion Prior (AMP) Formulation_ 

To facilitate naturalistic motion patterns, we incorporate the Adversarial Motion Prior (AMP) framework [38, 12] into the training of the locomotion ( _π_ l) and recovery ( _π_ r) specialists. The AMP module produces a style-dependent reward _rt_<sup>style</sup> , by training a discriminator _Dϕ_ to differentiate between reference trajectories and policy-generated ones. 

The discriminator operates on a compact input representation _τt_ = ( _s_<sup>amp</sup> _t−_ 3: _t_ +1<sup>),whichcomprisesa5-stepsequenceof</sup> 

AMP states. Each individual AMP state _s_<sup>amp</sup> _t ∈_ R<sup>23</sup> consists of the robot’s joint positions. Following the Least Squares GAN (LSGAN) [34] formulation, the discriminator is optimized by maximizing the following objective function: 


where _M_ and _P_ denote the reference dataset and the on-policy rollout buffer, respectively. Training stability is maintained via a gradient penalty with coefficient _α_<sup>_d_</sup> applied to the reference data. 

The discriminator’s output _d_ = _Dϕ_ ( _τt_ ) is subsequently mapped to a surrogate reward _rt_<sup>style</sup> to guide the policy: 


where _w_ style is a scaling coefficient. The composite reward used for policy optimization is the summation of task-specific and style-dependent components: _rt_ = _rt_<sup>task</sup> + _rt_<sup>style</sup> . 

Reference motions for the locomotion specialist ( _π_ l) are source from the LAFAN1 dataset [16], retargeted by Unitree. For the recovery specialist ( _π_ r), reference motions are sourced from motion capture (MoCap) data and retargeted to the Unitree G1 platform. 

## _C. Case-Adaptive Specialist Selection Details_ 

The Case-Adaptive Specialist Selection (CASS) mechanism selects an appropriate specialist to guide the student policy based on the robot’s head height _bt_ and the environmental context _It_ . This mechanism incorporates a mapping function _f_ ( _bt, It_ ) that identifies the robot’s specific case, alongside a set _C_ = _{_ ( _c_ rec _, πr_ ) _,_ ( _c_ loco _, πl_ ) _,_ ( _c_ coor _, πw_ ) _}_ that maps these cases to their respective specialists. Specifically, if the robot’s head height _bt_ is below 1 _._ 1 _m_ , it is categorized as case _c_ rec, where the fall recovery policy _πr_ provides guidance. If _bt_ exceeds 1 _._ 1 _m_ , the classification depends on the local environmental context _It_ . In scenarios where the robot is in proximity to a hanging bar or a high platform, it is assigned to case _c_ coor and guided by _πw_ ; otherwise, it is classified as _c_ loco and supervised by _πl_ . Once _πw_ is selected, CASS provides reference motions tailored to different terrains, enabling _πw_ to generate the appropriate guidance actions. Consequently, _c_ coor includes into several sub-cases _c_<sup>_i_</sup> coor<sup>basedonthespecificreferencemotion</sup> requirements. The definition of _It_ is illustrated in Figure 7. Accordingly, _f_ ( _bt, It_ ) can be expressed as: 


where _It_ = 1 signifies that the robot is facing a high platform requiring a climbing maneuver, while _It_ = 2 represents the presence of a hanging obstacle approximately 0 _._ 7 _m_ above the ground that can be navigated by forward rolling. 


Fig. 7: Illustration of the case-adaptive specialist selection process based on _bt_ and _It_ . 

## _D. Whole-Body Coordination Specialists πw Details_ 

To facilitate local terrain awareness, the whole-body coordination specialists _πw_ utilizes a terrain height-scanner centered on the robot’s pelvis to get the local terrain height samples (i.e., an elevation map). The sensor captures the local terrain geometry as a grid of 1 _._ 6 _m ×_ 1 _._ 0 _m_ with a spatial resolution of 0 _._ 1 _m_ . Furthermore, we employ a random initialization strategy. In Box terrain, the robot is initialized at a longitudinal distance sampled from _U_ [0 _,_ 0 _._ 55] _m_ ralative to the box. For Hanging Bar terrain, the robot is initialized at a distance sampled from _U_ [3 _,_ 3 _._ 5] _m_ from the bar. This initialization strategy ensures that _π_ w encounters a diverse set of relative distances to obstacles, thereby improving the ability to handle environmental variability. 

## _E. Depth Alignment for Sim-to-Real Transfer_ 

To bridge the visual sim-to-real gap, we implement a process that matches simulated depth distributions to realworld sensor characteristics. By injecting Gaussian noise, blur, and randomizing camera intrinsic and extrinsic parameters, we approximate the sensor observations of the actual hardware. The specific noise and randomization parameter ranges are detailed in Table VIII. 

TABLE IX: Reward Function Definitions for the Whole-Body Coordination Specialist ( _πw_ ). 

|**Reward Terms**|**Equation**|**Weight**|
|---|---|---|
|Body position|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_target <sup>_∥_</sup><sup>**p**des</sup><br>_b_<br>_−_**p**_b∥_<sup>2�</sup><br>_/_0_._3<sup>2�</sup>|1.0|
|Body orientation|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_target <sup>_∥_log(</sup><sup>_R_des</sup><br>_b _<sup>_R⊤_</sup><br>_b_ <sup>)</sup><sup>_∥_2�</sup><br>_/_0_._4<sup>2�</sup>|1.0|
|Body linear velocity|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_target <sup>_∥_</sup><sup>**v**des</sup><br>_b_<br>_−_**v**_b∥_<sup>2�</sup><br>_/_1_._0<sup>2�</sup>|1.0|
|Body angular velocity|exp<br>�<br>_−_<br>�<br>1<br>_|B_target_|_<br>�<br>_b∈B_target <sup>_∥_</sup><sup>**_ω_**des</sup><br>_b_<br>_−_**_ω_**_b∥_<sup>2�</sup><br>_/_3_._14<sup>2�</sup>|1.0|
|Anchor position|exp<br>�<br>_−∥_**p**<sup>des</sup><br>anchor <sup>_−_</sup><sup>**p**anchor</sup><sup>_∥_2</sup><sup>_/_0</sup><sup>_._32�</sup>|0.5|
|Anchor orientation|exp<br>�<br>_−∥_log(_R_<sup>des</sup><br>anchor<sup>_R⊤_</sup><br>anchor<sup>)</sup><sup>_∥_2</sup><sup>_/_0</sup><sup>_._42�</sup>|0.5|
|Action smoothness|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup>|_−_0_._1|
|Joint position limit|�_N_<br>_j_=1 <sup>[max(</sup><sup>_lj −θj,_ 0) + max(</sup><sup>_θj −uj,_ 0)]</sup>|_−_10_._0|
|Undesired self-contacts|�<br>_b/∈B_ee <sup>**1**[</sup><sup>_∥f_self</sup><br>_b_<br>_∥>_1N]|_−_0_._1|


TABLE X: Reward Function Definitions for the Locomotion Specialist ( _πl_ ). 

|**Reward Terms**|**Equation**|**Weight**|
|---|---|---|
|Track lin. vel.|exp_{−_<sup>_∥_</sup><sup>**_v_**cmd</sup><br>lin <sup>_−_</sup><sup>**_v_**lin</sup><sup>_∥_2</sup><br>2<br>0_._5<br>_}_<br><sup>cmd</sup><br><sup>2</sup>|5_._0|
|Track ang. vel.|exp_{−_<br>(**_ω_**<br>yaw <sup>_−_</sup><sup>**_ω_**yaw)</sup><br>0_._5<br>_}_<br>|5_._0|
|Joint acc.|_∥_<sup>¨</sup>_θ∥_<sup>2</sup><br>2|_−_5_×_10<sup>_−_7</sup>|
|Joint vel.|_∥_<sup>˙</sup>_θ∥_<sup>2</sup><br>2|_−_1_×_10<sup>_−_3</sup>|
|Action rate|_∥_**_a_**_t −_**_a_**_t−_1_∥_<sup>2</sup><br>2|_−_0_._03|
|Action smoothness|_∥_**_a_**_t −_2**_a_**_t−_1+**_a_**_t−_2_∥_<sup>2</sup><br>2|_−_0_._05|
|Angular vel. (_x, y_)|_∥_**_ω_**_xy∥_<sup>2</sup><br>2|_−_0_._05|
|Orientation|_∥_**_g_**<sup>torso</sup><br>_xy _<sup>_∥_2</sup><br>2<br>|_−_1_._5|
|Joint power|_|τ||_ <sup>˙</sup>_θ|_<sup>_⊤_</sup>|_−_2_._5_×_10<sup>_−_5</sup>|
|Feet stumble|I(_∃i, |_**_F_** <sup>_xy_</sup><br>_i_<br>_| ≥_3_|F _<sup>_z_</sup><br>_i _<sup>_|_)</sup>|_−_1_._0|
|Torques|�<br>all joints <sup>_τ_ 2</sup><br>_i_|_−_1_×_10<sup>_−_5</sup>|
|Joint deviation|�<br>_k∈{_arm, waist, hip_} _<sup>_wk_</sup><br>�<br>_j∈Jk _<sup>_|θj −θ_def</sup><br>_j _<sup>_|_</sup>|_−_0_._5|
|Joint pos. limits|�<br>all joints <sup>**_out_**</sup><sup>_i_</sup>|_−_2_._0|
|Joint vel. limits|ReLU(<sup>˙</sup>_θ −_<sup>˙</sup>_θ_<sup>max</sup>)|_−_1_._0|
|Torque limits|ReLU(_τ −τ_ <sup>max</sup>)|_−_1_._0|
|Feet lateral distance|_|_(_y_<sup>_b_</sup><br>left feet <sup>_−yb_</sup><br>right feet<sup>)</sup><sup>_−_0</sup><sup>_._2</sup><sup>_|_</sup>|0_._5|
|Feet slippage|�<br>feet <sup>_∥_</sup><sup>**_v_**foot</sup><br>_i_<br>_∥·_Icontact|_−_0_._25|
|Collision|_n_collision|_−_15_._0|
|Feet air time|�<br>foot<sup>(</sup><sup>_t_air</sup><br>_i _<sup>_−_0</sup><sup>_._5)</sup><sup>_·_ I(first contact</sup><sup>_i_)</sup>|1_._0|
|Stuck|(_∥_**_v_**_∥_2 _≤_0_._1)_·_(_∥_**_c_**<sup>_v_</sup>_∥_2 _≥_0_._2)|_−_1_._0|
|Feet clearance|�<br>foot<sup>((</sup><sup>_zi −h_target)2</sup><sup>_· ∥_</sup><sup>**_v_**</sup><sup>_i_</sup><br>_xy_<sup>_∥_)</sup>|2_._0|
|Alive|1<br><br>|2|
|AMP reward|max<br>�<br>0_,_1_−_<sup>1</sup><br>4 <sup>(</sup><sup>_Dϕ_(</sup><sup>_τ_)</sup><sup>_−_1)2</sup><br>�|3_._0|


TABLE XI: Reward Function Definitions for the Recovery Specialist ( _πr_ ). The _f_ tol adopts a Gaussian-style formulation, as detailed in [20]. 

|**Reward Terms**|**Equation**|**Weight**|
|---|---|---|
|_Task Rewards_||_w_<sup>task </sup>= 1_._0|
|Orientation|_f_tol(_−θ_<sup>_z_</sup><br>base<sup>_,_ [0</sup><sup>_._99</sup><sup>_, ∞_]</sup><sup>_,_ 1</sup><sup>_,_ 0</sup><sup>_._05)</sup>|1_._0|
|Head height|_f_tol(_h_head_,_[1_, ∞_]_,_1_,_0_._1)|1_._0|
|_Style Rewards_||_w_<sup>style </sup>= 1_._0|
|Hip joint deviation|�<br>hips <sup>I(max</sup><sup>_|θi| >_ 0</sup><sup>_._9</sup><sup>_∨_min</sup><sup>_|θi| <_ 0</sup><sup>_._8)</sup>|_−_10_._0|
|Knee deviation|�<br>knees <sup>I(max</sup><sup>_|θi| >_ 2</sup><sup>_._85</sup><sup>_∨_min</sup><sup>_|θi| < −_0</sup><sup>_._06)</sup>|_−_0_._25|
|Shoulder roll dev.|I(_θ_left _< −_0_._02_∨θ_right _>_0_._02)<br>|_−_2_._5|
|Thigh orientation|_f_tol( <sup>1</sup><br>2<br>�<br>thighs<sup>(</sup><sup>_θ_z</sup><br>thigh<sup>)</sup><sup>_,_ [0</sup><sup>_._8</sup><sup>_, ∞_]</sup><sup>_,_ 1</sup><sup>_,_ 0</sup><sup>_._1)</sup>|10_._0|
|Feet distance|I(_∥_**p**<sup>_xy_</sup><br>left<br>f <sup>_−_</sup><sup>**p**</sup><sup>_xy_</sup><br>right<br>f<sup>_∥_2</sup> <sup>_>_ 0</sup><sup>_._9)</sup>|_−_10_._0|
|Angular vel. (_x, y_)|exp(_−_2_∥_**_ω_**_xy∥_<sup>2</sup><br>2<sup>)</sup><sup>_·_ I(</sup><sup>_h_base</sup> <sup>_> h_stage1)</sup>|25_._0|
|Foot displacement|exp(clip(_−_2_∥_**q**<sup>_xy_</sup><br>base <sup>_−_</sup><sup>**q**</sup><sup>_xy_</sup><br>foot<sup>_∥_2</sup><sup>_,_ 0</sup><sup>_._3</sup><sup>_, ∞_))</sup><br>|2_._5|
|AMP reward|max<br>�<br>0_,_1_−_<sup>1</sup><br>4 <sup>(</sup><sup>_Dϕ_(</sup><sup>_τ_)</sup><sup>_−_1)2�</sup>|80_._0|
|_Regularization Rewa_|_rds_|_w_<sup>regu </sup>= 1_._0|
|Joint acc.|_∥_<sup>¨</sup>_θ∥_<sup>2</sup><br>2<br>|_−_2_._5e-7|
|Joint vel.|_∥_<sup>˙</sup>_θ∥_<sup>2</sup><br>2|_−_1e-3|
|Action rate|_∥_**a**_t −_**a**_t−_1_∥_<sup>2</sup><br>2|_−_0_._01|
|Action smoothness|_∥_**a**_t −_2**a**_t−_1+**a**_t−_2_∥_<sup>2</sup><br>2|_−_0_._05|
|Torques|�_τ_2<br>_i_|_−_1_×_10<sup>_−_5</sup>|
|Joint power|_|τ||_ <sup>˙</sup>_θ|_<sup>_⊤_</sup>|_−_2_._5_×_10<sup>_−_5</sup>|
|Joint pos. limits|�ReLU(_|θi| −θ_max<br>_i_<br>)<br>|_−_2_._0|
|Joint vel. limits|ReLU(<sup>˙</sup>_θ −_<sup>˙</sup>_θ_<sup>max</sup>)|_−_1_._0|
|_Post-Task Rewards (_|_Conditioned on hbase > hstage3)_|_w_<sup>task </sup>= 1_._0|
|Tracking errors|exp(_−_2_∥_**_ω_**_xy∥_<sup>2</sup><br>2<sup>)</sup><sup>_,_ exp(</sup><sup>_−_5</sup><sup>_∥_</sup><sup>**v**</sup><sup>_xy∥_2</sup><br>2<sup>)</sup><sup>_,_ exp(</sup><sup>_−_5</sup><sup>_∥_</sup><sup>**g**</sup><sup>_xy∥_2</sup><br>2<sup>)</sup>|10_._0|
|Base height|exp(_−_20_|h_base_−_0_._75_|_)|10_._0|
|Target joint dev.|exp(_−_0_._1 <sup>�</sup>(_θi −θ_<sup>def</sup><br>_i_ <sup>)2)</sup>|10_._0|
|Target feet dist.|_f_tol(_y_L_−y_R_,_[0_._3_,_0_._4]_,_0_._1_,_0_._05)|_−_5_._0|


