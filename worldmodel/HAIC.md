---
title: "HAIC: Humanoid Agile Object Interaction Control via Dynamics-Aware World Model"
date: "2026-02-12"
authors: "Dongting Li; Xingyu Chen; Qianyang Wu; Bo Chen; Sikai Wu; Hanyu Wu"
url: https://arxiv.org/abs/2602.11758
pdf: https://arxiv.org/pdf/2602.11758
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.11758)** / [論文ページ](https://arxiv.org/abs/2602.11758)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# HAIC: Humanoid Agile Object Interaction Control via Dynamics-Aware World Model 

Dongting Li<sup>1,4</sup><sup>_∗_</sup> , Xingyu Chen<sup>2,4</sup><sup>_∗_</sup> , Qianyang Wu<sup>4</sup> , Bo Chen<sup>4</sup> , Sikai Wu<sup>4</sup> , Hanyu Wu<sup>3</sup> , Guoyao Zhang<sup>4</sup> Liang Li<sup>4</sup> , Mingliang Zhou<sup>4</sup> , Diyun Xiang<sup>4</sup> , Jianzhu Ma<sup>1</sup><sup>_†_</sup> , Qiang Zhang<sup>2</sup><sup>_†_</sup> , Renjing Xu<sup>2</sup><sup>_†_</sup> 1Tsinghua University 2HKUST(Guangzhou) 3ETH Zurich 4Xiaomi Robotics Lab 

> _∗_ Equal Contribution _†_ Equal Advising 

https://haic-humanoid.github.io/ 


**Fig. 1:** Our proposed framework HAIC enables a robot to perform complex interactions, including (a) **Underactuated Object Interaction.** The robot learns interaction skills such as skateboarding, cart pushing, and cart pulling. (b) **Sequential Interaction.** HAIC supports multi-object interaction, enabling a wholebody controller to pick up the box, load it onto the cart, then drive them forward in one policy. (c) **Multi-terrain Interaction.** HAIC enables robots to maintain interactions with both an object and the scene, such as carrying a box across various types of terrains, such as platforms, slopes, and stairs. 

**_Abstract_ —Humanoid robots exhibit significant potential for executing complex whole-body interaction tasks in unstructured environments. While recent advancements in Human-Object Interaction (HOI) have been substantial, prevailing methodologies predominantly address the manipulation of fully actuated objects, where the target is rigidly coupled to the robot’s end-effector and its state is strictly constrained by the robot’s kinematics. This paradigm neglects the pervasive class of underactuated objects characterized by independent dynamics and non-holonomic constraints, which pose significant control challenges due to complex coupling forces and frequent visual occlusions. To bridge this gap, we propose HAIC, a unified framework designed to enable robust interaction across a spectrum of object dynamics without reliance on external state estimation. Central to our approach is a novel dynamics predictor that infers high-order object states, specifically velocity and acceleration, solely from proprioceptive history. These predictions are explicitly projected onto static** 

**geometric priors to construct a spatially grounded representation of dynamic occupancy, allowing the policy to internalize collision boundaries and contact affordances in visual blind spots. We employ an asymmetric fine-tuning strategy where the world model continuously adapts to the student policy’s exploration, ensuring robust state estimation under distribution shifts. We evaluate our framework on a Unitree G1 humanoid robot. Empirical results demonstrate that HAIC achieves high success rates in agile object interactions, including skateboarding, cart pushing, and cart pulling under various weight load conditions, by compensating for inertial physical perturbations. Furthermore, by accurately predicting multi-object dynamics, it seamlessly masters sequential tasks and carries a box across composed terrains.** 

I. INTRODUCTION 

Humanoid robots, characterized by their anthropomorphic morphology, possess immense potential for executing complex 


**(a)** Types of interacted objects. **(b)** Success rate comparison on different tasks. 

**Fig. 2:** HAIC excels at complex interactions, particularly with underactuated objects, and significantly outperforms the baseline. 

whole-body interaction tasks in unstructured environments. From transporting payloads to interacting dynamically with tools, these tasks require not only robust locomotion stability but also the capacity to perform precise interactions with the environment. Recent data-driven approaches in Human-Object Interaction have achieved significant milestones, enabling robots to acquire diverse interaction skills [16, 6, 37, 59]. 

However, prevailing research predominantly focuses on the Interaction of **fully actuated objects** , such as carrying a rigidly grasped box [6, 37]. In these scenarios, the object’s state is strictly constrained by the robot’s end-effector, resulting in relatively simple and fully controlled dynamics. In contrast, the real world is populated with **underactuated objects** possessing independent dynamics and non-holonomic constraints, such as skateboards, carts, or luggage. Manipulating such objects presents a dual challenge. First, **visual occlusion** is frequent. Large objects often obstruct onboard sensors, depriving the robot of direct observation of both the terrain and the object itself [26]. Second, **dynamics coupling** becomes critical. Unlike static payloads, underactuated objects generate independent acceleration and inertial forces that propagate to the robot. Traditional control methods often rely on external high-precision state estimation to handle these disturbances, which is impractical for real-world deployment [51]. Meanwhile, existing reinforcement learning policies, lacking explicit modeling of high-order dynamics, often suffer from response lag, leading to instability during high-speed interactions [18, 33, 47]. 

Humans exhibit remarkable adaptability when facing similar constraints. Even when vision is obstructed by a carried object or when balancing on an accelerating skateboard, humans rely on proprioception and an internal mental model to infer the object’s state. This capability stems from a fusion of geometric reasoning (knowing the object’s boundaries) and dynamic sensing (feeling the forces to anticipate acceleration), enabling proactive center-of-mass adjustments. 

Inspired by this cognitive mechanism, we introduce HAIC, a unified learning framework designed to enable robust and agile object interaction in visual blind spots. Unlike prior 

models focused on visual prediction [10, 11, 13, 9, 39], HAIC is proprioception-centric and addresses the control of both fully actuated and underactuated objects through two key mechanisms in a dynamics-aware world model (DWM): 

- High-Order Dynamics Prediction: By analyzing proprioceptive history, HAIC explicitly predicts the object’s linear and angular accelerations. This allows the robot to capture the independent motion trends of underactuated objects, facilitating proactive inertia compensation. 

- Explicit Geometric Projection: HAIC explicitly project these predicted dynamic states onto a static geometric prior (point cloud) of the object. This constructs a spatially grounded representation of dynamic occupancy, enabling the policy to perceive collision boundaries and contact affordances even without visual feedback. 

To bridge the gap between simulation and reality, we employ an asymmetric fine-tuning strategy where the world model continuously adapts to the student policy’s exploration online, effectively mitigating distribution shifts [46, 57]. 

The main contributions of this work are summarized as follows: 

- **Dynamics-Aware World Model:** We propose a novel dynamics predictor that integrates high-order acceleration inference with explicit geometric projection, unifying state estimation for both static payloads and dynamic underactuated objects. 

- **Asymmetric Adaptive Distillation:** We design a robust two-stage training pipeline that transfers privileged geometric and dynamic reasoning into a sensor-limited student policy via continuous world model adaptation. 

- **Agile Real-World Performance:** We demonstrate SOTA performance on a Unitree G1 humanoid robot. Our framework achieves a 100% success rate in blind multiterrain box carrying and, for the first time without external sensing, enables the robot to master agile underactuated tasks, such as dynamic skateboarding. 

## II. RELATED WORK 

## _A. Humanoid Whole-Body Control and Tracking_ 

Deep reinforcement learning (RL) [49] has achieved significant milestones in tracking large-scale human motion capture (MoCap) datasets like AMASS [41]. Recent General Motion Trackers (GMT) [5, 71] and retargeting frameworks [3, 34, 16] allow humanoids to reproduce diverse kinematic behaviors. To support these data-driven approaches, scalable collection systems like TWIST [74] and TWIST2 [75] have been developed to provide high-quality whole-body demonstrations. 

Early studies demonstrated that motion imitation and adversarial motion priors enable policies to track diverse human motion data, producing natural and robust whole-body control [44, 45, 65, 34, 14, 17]. These works establish motion tracking as a scalable paradigm for acquiring rich motor skills while substantially reducing manual reward engineering. 

Building upon this foundation, subsequent research [75, 12, 73, 76] investigates generalized whole-body control through 

large-scale motion datasets and unified latent representations, enabling a single policy to compose heterogeneous skills and adapt to diverse task conditions. Policies are pretrained via large-scale data and unsupervised reinforcement learning, and conditioned on language, vision, or high-level task descriptors to enable controllable and zero-shot skill adaptation [31, 40, 22, 50]. These models demonstrate strong generalization across diverse motion patterns, highlighting the potential of foundation training for whole-body control and advanced interactions with environments, especially dynamic objects. 

## _B. Physics-Based Human-Object Interaction_ 

Humanoid-object interaction (HOI) is a longstanding challenge bridging computer vision and robotics. Large-scale HOI datasets provide diverse demonstrations to facilitate datadriven learning [29, 55, 4, 21, 77, 66]. Based on these data, advanced frameworks [60, 56, 61, 43, 67, 35] have been developed to train policies that master versatile whole-body interactions in simulation. Similarly, video-based imitation methods extract interactive skills directly from human videos [63, 2, 72]. Prior studies on loco-manipulation, which focus only on the interaction between the hand and objects, show that integrating force adaptation [78], hierarchical control [32, 23, 28], or residual action [54] enables precise manipulation behaviors with stable locomotion. And visual sim-to-real transfer methods substantially improve real-world generalization for continuous manipulation tasks [69, 15, 20]. Some specialized systems demonstrate high-speed adaptation for specific sports but lack generality [52, 68, 36, 62]. As for full-body interactions, Omniretarget [70] improves the quality of retargeted motion by constructing the interaction mesh. HDMI [63] and ResMimic [80] incorporate residual action modules to adapt policies to virtual object states. Other methods typically rely on explicit object tracking to estimate object states, such as PhysHSI (LiDAR) [58], HDMI (markers) [63], VisualMimic (depth) [72], and DemoHLM (RGB) [8]. However, all these methods are restricted to interactions with static environments or fully actuated objects. In contrast, HAIC can learn coupled humanoid-object dynamics through a specialized world model, enabling agile interactions with underactuated objects or multiterrain environments. 

## _C. World Models for Humanoids_ 

World models [10, 11] act as internal simulators that enable agents to anticipate future outcomes, and have been widely adopted in robotic manipulation to predict tactile feedback and object dynamics[7, 19, 51]. Recent work leverages world models to address high-dimensional humanoid dynamics and complex contact sequences. DWL [9] reconstructs complete physical states from noisy observations via denoising learning, enabling robust whole-body control, while RWM [27] mitigates long-horizon drift through a dual-autoregressive prediction scheme. WMR [53] decouples dynamics learning from policy gradients and enforces state reconstruction to prevent representation collapse. World models are also used as self-supervised objectives for perceptual robustness, as 


**Fig. 3: Overview of our Dynamics-aware World Model.** It predicts object dynamics from proprioception and explicitly projects them onto a static geometric prior for reconstructing the privileged information. 

demonstrated by WMP [25], and extended to active interaction in Ego-VCP [38] for ego-centric contact planning. Any2Track [79] learns dynamics-aware embeddings from observation histories, enabling implicit inference of environmental properties and robust sim-to-real transfer. However, these methods primarily model proprioceptive dynamics for wholebody control, often neglecting the coupled dynamics inherent in object interaction. 

## III. METHODOLOGY 

## _A. Problem Formulation_ 

The purpose of humanoid-object interaction is to train a whole-body control policy that simultaneously tracks the reference trajectory of both the robot and the object. We formulate this proprioception-based interaction task as a partially observable Markov decision process (POMDP) [26]. At each timestep _t_ , the full state _st ∈S_ includes the robot’s proprioception _s_<sup>_prop_</sup> _t_ , the reference motion _s_<sup>_ref_</sup> _t_ , the point cloud of objects _P_ and the privileged state _s_<sup>_priv_</sup> _t_ . 

Since the object state _s_<sup>_obj_</sup> _t_ cannot be acquired directly, we adapt the teacher-student framework [24] to distill the privileged information. In training, the teacher has access to the full state _st_ . During deployment, the student only observes: 

- Onboard proprioception _s_<sup>_prop_</sup> _t_ (joint data, IMU data). 

- Reference motion _s_<sup>_ref_</sup> _t_ . 

- Nominal geometric template _P ∈_ R<sup>_N×_3</sup> : a standard-sized point cloud acting as a semantic prior. 

The goal is to explore a policy _π_ ( _at|s_<sup>_prop_</sup> _t , s_<sup>_ref_</sup> _t , at−_ 1 _, P_ ) in the simulation that enables the humanoid robot to acquire robust interaction skills with objects in the real world. 

## _B. Dynamics-Aware World Model_ 

Our motivation is to use the robot’s state _s_<sup>_prop_</sup> _t_ to predict the inaccessible state of objects _s_<sup>_obj_</sup> _t_ [51]. Therefore, we design a predictive framework to internalize the object’s dynamics relative to the robot. And we propose a pipeline that first estimates object dynamics, explicitly projects these dynamics onto the geometric prior, and subsequently feeds them into the downstream network, as shown in Fig. 3. 

_1) Object Adapter:_ The core component of the dynamicsaware world model is the object adapter, which functions as a real-time dynamics predictor. It takes the history of predicted object state _s_ ˆ<sup>_obj_</sup> _t−_ 1<sup>,robotobservations</sup><sup>_Ht_=</sup><sup>_{s_</sup> _t_<sup>_prop_</sup> _−n_<sup>_, . . . , s_</sup> _t_<sup>_prop_</sup> _}_ and the future of reference motion _Ft_ = _{s_<sup>_ref_</sup> _t , . . . , s_<sup>_ref_</sup> _t_ + _m_<sup>_}_as</sup> input and predicts the object’s relative spatial and temporal state _s_ ˆ<sup>_obj_</sup> _t_ : 


**Fig. 4: Framework overview** . We train policies in the simulation from scratch. The framework includes a privileged teacher and a dynamics-aware student. The student policy utilizes the learned world model to perform robust interaction tasks such as skateboarding on a real humanoid robot. 

where _s_ ˆ<sup>_obj_</sup> _t_ includes the predicted relative position _p_ ˆ _t_ , orientation _R_<sup>ˆ</sup> _t_ , linear/angular velocities ( _v_ ˆ _t_<sup>_lin_</sup> _,_ ˆ _vt_<sup>_ang_</sup> ), and linear/angular accelerations ( _a_ ˆ<sup>_lin_</sup> _t_<sup>_,_ˆ</sup><sup>_a_</sup> _t_<sup>_ang_</sup> ). 

_2) Explicit Geometric Projection:_ While dynamics-aware approaches using signed distance fields (SDFs) or point clouds have been explored for stationary arms [30, 19] and HOI animation [1, 64], the application to the high-dimensional dynamics of humanoid whole-body control remains limited. By conditioning our predictor on a point-cloud-based geometric prior, the robot can mentally track an invisible object, effectively transforming a partially observable Markov decision process into a manageable control task without the need for the real-time privileged states. 

To bridge the gap between abstract state estimation and physical interaction, we introduce an explicit geometric projection step. We transform the canonical point cloud _P_ using the predicted _s_ ˆ<sup>_obj_</sup> _t_ into the robot’s root coordinate frame: 


By explicitly generating the dynamic object point cloud _Pt_<sup>_dyn_</sup> , we provide the privilege adapter with a spatially grounded representation of the object’s occupancy. Note that _P_ serves as a geometric prior rather than a ground-truth measurement. 

_3) Privilege Adapter:_ Finally, the estimated dynamic geometry is fused with proprioception via the privilege adapter. This module takes the dynamic point cloud _Pt_<sup>_dyn_</sup> , current proprioception _s_<sup>_prop_</sup> _t_ , and the reference motion _s_<sup>_ref_</sup> _t_ to produce a predicted privileged feature _z_ ˆ _t_<sup>_priv_</sup> . This feature serves as the input to the student actor, effectively mimicking the information flow of a privileged actor. 

_C. Two-Stage Training Framework_ 

Fig. 4 illustrates the overall architecture of HAIC. To streamline our formulation, we define the unified world model loss ( _LW M_ ) as the weighted sum of dynamics prediction error and latent feature alignment: 


where _λ_ obj and _λ_ priv balance the supervision strength of physical state regression and latent space distillation, respectively. We denote the standard PPO [49] objective (including policy gradient, value loss, and entropy) as _LP P O_ ( _π, V_ ). 

_1) Stage 1: Feature Alignment & Warm-up:_ In the first stage, we train the privileged Teacher actor _πT_ via reinforcement learning. Simultaneously, we train the world model and the student actor _πS_ to mirror the teacher’s behavior and internal representation [48]. This “warm-up” phase ensures that the student starts Stage 2 with a learned sensorimotor primitive closer to the expert distribution. The objective is: 

_LStage_ 1 = _LP P O_ ( _πT , VT_ )+ _LW M_ + _λ_ distill _DKL_ ( _πS||πT_ ) (4) Here, the action distillation term _λ_ distill forces the student to produce actions consistent with the teacher. 

_2) Stage 2: Asymmetric Fine-tuning:_ In the second stage, we fine-tune the student actor _πS_ using an asymmetric actorcritic setup [46]. The critic _VT_ retains access to privileged states for variance reduction. 

To address the distribution shift caused by the student’s independent exploration, we continue to optimize the world model alongside the policy. The total objective is: 


By consistently minimizing _LW M_ in both stages, we ensure the world model continuously adapts to the evolving trajectory distribution of the student policy, preventing the “blind” policy from collapsing due to inaccurate state estimation. **Stabilization via EMA:** To further mitigate instability arising from the coupled training of the policy and the world model, we maintain an exponential moving average (EMA) [42] of the world model weights for the rollout policy. The policy interacts with the environment using the EMA-smoothed predictions, while gradients are backpropagated through the online network. 


**Fig. 5:** Multiple Objects Contact Guidance Strategy. 


**Fig. 6:** Real-world performance comparison with the baseline across various tasks. With the specifically designed dynamics-aware world model, HAIC maintains robust stability throughout the interaction, whereas the baseline suffers from balance failures and trajectory drift. 

## _D. Multiple Objects Contact Reward_ 

To enable robust manipulation of multiple objects, we introduce a contact reward _r_ contact that unifies geometric alignment and force regulation. As illustrated in Fig. 5, this reward dynamically guides the robot through two phases: 

- Guidance (Fig. 5a): Before contact, the reward minimizes the distance between end-effectors and semantic targets. 

- Execution (Fig. 5b-c): Upon contact, it applies force appropriately while maintaining geometric constraints. 

The contact reward is calculated as the average reward across all active objects _o ∈O_ and their corresponding endeffectors _e ∈Eo_ : 


Here, I _o,e_ is a binary mask from the reference motion indicating if contact is active. The individual terms account for physical tolerances to prevent optimization instability. Position term _r_ pos<sup>_o,e_encourages the end-effector position</sup><sup>**_p_**</sup> _e_<sup>to match the</sup> target **_p_** tgt within a tolerance _ϵ_ tol: 


Force term _r_ force<sup>_o,e_ensuresthecontactforce</sup><sup>**_F_**</sup><sup>_e_reachesa</sup> required threshold _F_ thr. We penalize the force deficit only when it falls below this threshold: 


More detailed reward definitions and parameters are provided in Appendix C2. 

IV. EXPERIMENTS 

_A. Experimenrt Setup_ 

_1) Task Description:_ To validate our method, we designed three types of interaction tasks: 

**Underactuated Object Interaction.** This task requires the robot to interact with underactuated wheeled objects, which introduces unstructured, time-varying external physical disturbances upon contact. Unlike interactions with fully actuated objects, the motion of underactuated objects actively affects the robot’s balance, requiring the controller to predict and compensate for these disturbances in real time. 

**Sequential interaction.** In addition to interacting with a single object, we also design composite sequential tasks involving multiple objects, such as loading a payload onto a mobile cart and then manipulating the cart. These scenarios challenge the policy’s capacity to handle discrete mode switching and maintain stable control over extended horizons while coordinating interactions with multiple dynamic bodies. 

**Multi-terrain interaction.** The final task requires the robot to carry a box across composite terrains, including platforms, slopes, and stairs. This task places high demands on state estimation because the box obscures the robot’s view of the ground. As a result, the policy relies solely on self-perception and predictions from the world model. The controller must simultaneously handle the dynamic load on the arms and the complex interactions with the terrain. 

_2) Implementation Details:_ We describe the specific configurations for data processing, training infrastructure, and deployment setups below. 

**Data Collection and Processing.** To capture high-fidelity interaction behaviors, we utilized an optical motion capture system tracking both the human motion and interactive objects via synchronized markers. The raw kinematic data were retargeted to the Unitree G1 and refined through a physicsbased simulation pipeline to generate physically valid states with contact information (see Appendix B for details). **Training Setup.** We trained the base policy and world model using PPO in the Isaac Sim simulator. The two-stage training of a model was conducted on a single NVIDIA RTX 4090 GPU and took approximately 8 hours. 

**Sim-to-Real Transfer.** We employed extensive domain randomization to bridge the reality gap. For real-world deployment, the policy ran on an external PC, transmitting joint position targets to the robot’s onboard control board via Ethernet. The PD controller operated at 200 Hz in simulation and 500 Hz on the real robot to ensure accurate tracking of the PD targets, while the control policies ran at 50 Hz. 

_3) Evaluation Metrics:_ To rigorously quantify the robot’s kinematic tracking performance, we define the following metrics based on onboard proprioception. We report the Mean and Standard Deviation for error metrics, and the Success Rate (SR) for task completion. 

## **Robot State Metrics:** 

- _E_ mpbpe **/** _E_ mpboe **:** Root-relative Mean Per Body Position (mm) and Orientation (10<sup>_−_3</sup> rad) Error. 

- _E_ g **-** mpbpe **:** Global Mean Per Body Position Error (mm). 

- _E_ mpjpe **/** _E_ mpjve **:** Mean Per Joint Position (10<sup>_−_3</sup> rad) and Velocity (10<sup>_−_3</sup> rad/frame) Error. 

- _E_ mpbve **/** _E_ mpbae **:** Mean Per Body Velocity (mm/frame) and Acceleration (mm/frame<sup>2</sup> ) Error. 

## **Object State Metrics:** 

- _E_ mpope **/** _E_ mpooe **:** Mean Per Object Position (mm) and Orientation (10<sup>_−_3</sup> rad) Error. 

- _E_ mpove **/** _E_ mpoae **:** Mean Per Object Velocity (mm/frame) and Acceleration (mm/frame<sup>2</sup> ) Error. 

We evaluate the performance of our proposed framework on the Unitree G1 humanoid robot in real-world scenarios. The robot operates autonomously using onboard computation, without external motion capture systems, relying solely on proprioceptive feedback and our dynamics-aware World Model. 

_4) Baseline:_ We compare our method with HDMI in simulation and the real world. We utilize **HDMI**<sup>_∗_</sup> , a proprioceptiononly variant of the original HDMI framework [63] as its lower bound. As illustrated in Fig. 2b, we also present the sim-to-sim upper bound performance of HDMI for comparison with the real-world success rates of HAIC and HDMI<sup>_∗_</sup> . To ensure a fair comparison, this baseline was retrained from scratch using the same setup as our method. Instead of privileged object states, HDMI<sup>_∗_</sup> receives a history of proprioceptive observations to implicitly infer the environmental context. 

## _B. Real-world Deployment and Comparison_ 

In real-world experiments, our dynamics-aware world model functions as a core estimator across three distinct scenarios: 

(a) **Underactuated Object Interaction.** For underactuated objects like skateboards and carts, the world model infers the object’s full dynamics, including translation, rotation, linear/angular velocity, and acceleration. These high-order predictions are explicitly applied to the object’s canonical point cloud. (b) **Sequential Interaction.** In sequential tasks involving multiple objects, HAIC predicts the dynamics for both the box and the cart. It applies the respective predicted rotations and translations to align each object’s geometric prior independently. (c) **Multi-terrain Interaction.** HAIC extends its prediction to environmental features. It estimates the dynamics of the carried box while simultaneously predicting the translation and orientation of terrain structures. By projecting these estimates onto the geometry and feeding the aligned features into the downstream network, the robot successfully navigates uneven ground. We compared HAIC with the baseline in these scenarios. HAIC exhibits superior robustness due to its structured representation incorporating both geometric and dynamic information. The original HDMI performed well with fully-driven objects, but its performance declined on underactuated objects, since it does not account for geometry and higher-order physical quantities. As demonstrated by the case study results below, HAIC shows significant advantages in both success rate and motion quality. 

**TABLE I:** Real-world results for **Skateboarding** . We report the success rate for both Gliding and Completing. HAIC achieves stable gliding and significantly higher completion rates compared to the baseline. 

||**Succes**|**s Rate**|||**Robot State**|**Metrics**|||
|---|---|---|---|---|---|---|---|---|
|**Method**|**Glide**|**Comp.**|_E_mpbpe|_E_mpboe|_E_mpjpe|_E_mpbve|_E_mpbae|_E_mpjve|
|HDMI<sup>_∗_</sup>|20%|0%|132.1<sup>_±_35</sup><sup>_._7</sup><br>|666.7<sup>_±_213</sup><sup>_._6</sup><br>|188.7<sup>_±_12</sup><sup>_._6</sup><br>|5.39<sup>_±_0</sup><sup>_._62</sup><br>|**4.06**<sup>_±_0</sup><sup>_._04</sup><br>|**10.40**<sup>_±_0</sup><sup>_._19</sup><br>|
|**HAIC**|**100%**|**60%**|**81.5**<sup>_±_15</sup><sup>_._4</sup>|**453.5**<sup>_±_88</sup><sup>_._2</sup>|**127.1**<sup>_±_11</sup><sup>_._5</sup>|**4.72**<sup>_±_0</sup><sup>_._75</sup>|4.48<sup>_±_0</sup><sup>_._50</sup>|12.15<sup>_±_1</sup><sup>_._87</sup>|


**TABLE II:** Real-world results for **Cart Manipulation** . HAIC achieves 100% success in both tasks, whereas the baseline fails in “Push”. 

|**Task**|**Method**|**SR** _↑_|_E_mpbpe _↓_|_E_mpboe _↓_|_E_mpjpe _↓_|_E_mpbve _↓_|_E_mpbae _↓_|_E_mpjve _↓_|
|---|---|---|---|---|---|---|---|---|
|Pull|HDMI<sup>_∗_</sup>|40%|118.0<sup>_±_5</sup><sup>_._8</sup><br>|556.7<sup>_±_43</sup><sup>_._0</sup><br>|165.0<sup>_±_2</sup><sup>_._3</sup><br>|6.11<sup>_±_0</sup><sup>_._13</sup><br>|3.73<sup>_±_0</sup><sup>_._14</sup><br>|10.32<sup>_±_1</sup><sup>_._00</sup><br>|
|Cart|**HAIC**|**100%**|**76.2**<sup>_±_6</sup><sup>_._8</sup>|**425.0**<sup>_±_41</sup><sup>_._7</sup>|**132.3**<sup>_±_6</sup><sup>_._4</sup>|**5.08**<sup>_±_0</sup><sup>_._53</sup>|**3.66**<sup>_±_0</sup><sup>_._21</sup>|**9.50**<sup>_±_1</sup><sup>_._10</sup>|
|Push|HDMI<sup>_∗_</sup>|0%|136.2<sup>_±_23</sup><sup>_._3</sup><br>|778.5<sup>_±_218</sup><sup>_._6</sup><br>|158.9<sup>_±_4</sup><sup>_._7</sup><br>|7.36<sup>_±_0</sup><sup>_._48</sup><br>|5.32<sup>_±_0</sup><sup>_._21</sup><br>|15.62<sup>_±_0</sup><sup>_._74</sup><br>|
|Cart|**HAIC**|**100%**|**82.0**<sup>_±_6</sup><sup>_._3</sup>|**418.7**<sup>_±_36</sup><sup>_._6</sup>|**150.0**<sup>_±_9</sup><sup>_._3</sup>|**5.29**<sup>_±_0</sup><sup>_._17</sup>|**4.47**<sup>_±_0</sup><sup>_._09</sup>|**11.61**<sup>_±_0</sup><sup>_._80</sup>|


**TABLE III:** Real-world results for **Sequential Interaction** . The baseline is omitted as it failed to complete the prerequisite cart tasks. HAIC demonstrates capability in sequential object transport. 

|**Task**|**Method**|**SR** _↑_|_E_mpbpe _↓_|_E_mpboe _↓_|_E_mpjpe _↓_|_E_mpbve _↓_|_E_mpbae _↓_|_E_mpjve _↓_|
|---|---|---|---|---|---|---|---|---|
|Pull Cart|HDMI<sup>_∗_</sup>|0%|-<br>|-<br>|-<br>|-<br>|-<br>|-<br>|
|w/ Box|**HAIC**|**40%**|**88.2**<sup>_±_8</sup><sup>_._2</sup>|**420.7**<sup>_±_16</sup><sup>_._7</sup>|**157.2**<sup>_±_8</sup><sup>_._2</sup>|**5.91**<sup>_±_0</sup><sup>_._07</sup>|**5.02**<sup>_±_0</sup><sup>_._09</sup>|**12.20**<sup>_±_0</sup><sup>_._31</sup>|
|Push Cart|HDMI<sup>_∗_</sup>|0%|-|-|-|-|-|-|
|w/ Box|**HAIC**|**100%**|**70.5**<sup>_±_5</sup><sup>_._7</sup>|**381.7**<sup>_±_24</sup><sup>_._7</sup>|**143.6**<sup>_±_4</sup><sup>_._1</sup>|**5.27**<sup>_±_0</sup><sup>_._26</sup>|**3.92**<sup>_±_0</sup><sup>_._18</sup>|**11.10**<sup>_±_0</sup><sup>_._85</sup>|


**TABLE IV:** Real-world results for **Multi-terrain Interaction** . HAIC succeeds on the complex slope-stair terrain where baseline fails. 

|**Task**|**Method**|**SR** _↑_|_E_mpbpe _↓_|_E_mpboe _↓_|_E_mpjpe _↓_|_E_mpbve _↓_|_E_mpbae _↓_|_E_mpjve _↓_|
|---|---|---|---|---|---|---|---|---|
|Carry|HDMI<sup>_∗_</sup>|100%|66.6<sup>_±_2</sup><sup>_._0</sup><br>|344.0<sup>_±_19</sup><sup>_._8</sup><br>|171.7<sup>_±_1</sup><sup>_._7</sup><br>|4.69<sup>_±_0</sup><sup>_._10</sup><br>|3.14<sup>_±_0</sup><sup>_._01</sup><br>|8.10<sup>_±_0</sup><sup>_._13</sup><br>|
|Box|**HAIC**|100%|**58.8**<sup>_±_6</sup><sup>_._1</sup>|**305.6**<sup>_±_20</sup><sup>_._8</sup>|**162.0**<sup>_±_6</sup><sup>_._8</sup>|**4.21**<sup>_±_0</sup><sup>_._13</sup>|**3.03**<sup>_±_0</sup><sup>_._05</sup>|**7.75**<sup>_±_0</sup><sup>_._18</sup>|
|/Stair|HDMI<sup>_∗_</sup>|100%|66.2<sup>_±_4</sup><sup>_._1</sup><br>|**316.2**<sup>_±_2</sup><sup>_._8</sup><br>|158.9<sup>_±_13</sup><sup>_._8</sup><br>|4.79<sup>_±_0</sup><sup>_._36</sup><br>|4.35<sup>_±_0</sup><sup>_._24</sup><br>|10.10<sup>_±_0</sup><sup>_._98</sup><br>|
|w|**HAIC**|100%|**55.5**<sup>_±_3</sup><sup>_._9</sup>|331.2<sup>_±_23</sup><sup>_._1</sup>|**118.4**<sup>_±_0</sup><sup>_._6</sup>|**4.06**<sup>_±_0</sup><sup>_._02</sup>|**4.05**<sup>_±_0</sup><sup>_._01</sup>|**8.66**<sup>_±_0</sup><sup>_._01</sup>|
|/Sl|HDMI<sup>_∗_</sup>|100%|**53.5**<sup>_±_0</sup><sup>_._7</sup><br>|**289.0**<sup>_±_1</sup><sup>_._7</sup><br>|130.6<sup>_±_1</sup><sup>_._9</sup><br>|**3.68**<sup>_±_0</sup><sup>_._03</sup><br>|**3.39**<sup>_±_0</sup><sup>_._01</sup><br>|7.41<sup>_±_0</sup><sup>_._02</sup><br>|
|w ope|**HAIC**|100%|60.5<sup>_±_4</sup><sup>_._3</sup>|324.7<sup>_±_28</sup><sup>_._0</sup>|**120.2**<sup>_±_1</sup><sup>_._6</sup>|8.77<sup>_±_0</sup><sup>_._11</sup>|4.60<sup>_±_0</sup><sup>_._13</sup>|**3.66**<sup>_±_0</sup><sup>_._05</sup>|
|w/ Stair|HDMI<sup>_∗_</sup>|0%|126.8<sup>_±_4</sup><sup>_._4</sup><br>|701.0<sup>_±_32</sup><sup>_._1</sup><br>|162.3<sup>_±_2</sup><sup>_._0</sup><br>|5.98<sup>_±_0</sup><sup>_._07</sup><br>|**4.03**<sup>_±_0</sup><sup>_._10</sup><br>|10.87<sup>_±_0</sup><sup>_._27</sup><br>|
|+ Slope|**HAIC**|**100%**|**60.6**<sup>_±_13</sup><sup>_._4</sup>|**286.5**<sup>_±_59</sup><sup>_._8</sup>|**128.5**<sup>_±_16</sup><sup>_._2</sup>|**4.74**<sup>_±_0</sup><sup>_._17</sup>|4.05<sup>_±_0</sup><sup>_._04</sup>|**10.67**<sup>_±_0</sup><sup>_._52</sup>|


_1) Underactuated Object Interaction:_ This task involves high-dynamic interactions, where object interactions significantly affect the robot’s balance: skateboarding and manipulating wheeled carts. Fig. 6 demonstrates that HAIC maintains 

**TABLE V:** Ablation results for **Skateboarding** . Vec-Pose can balance but fails to dismount due to a lack of acceleration prediction. HAIC achieves a high completion rate with the lowest robot tracking errors and the most stable object acceleration control. 

||**SR**|_↑_|||**Robo**|**t State Metr**|**ics**||||**Object Sta**|**te Metrics**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Glide**|**Comp.**|_E_mpbpe_↓_|_E_g**-**mpbpe_↓_|_E_mpboe_↓_|_E_mpjpe_↓_|_E_mpbve_↓_|_E_mpbae_↓_|_E_mpjve_↓_|_E_mpope_↓_|_E_mpooe_↓_|_E_mpove_↓_|_E_mpoae_↓_|
|Proprio|40%|0%|91.1<sup>_±_9</sup><sup>_._6</sup><br>|548.1<sup>_±_186</sup><sup>_._4</sup><br>|490.6<sup>_±_58</sup><sup>_._0</sup><br>|163.3<sup>_±_3</sup><sup>_._4</sup><br>|5.08<sup>_±_0</sup><sup>_._28</sup><br>|4.18<sup>_±_0</sup><sup>_._10</sup><br>|12.45<sup>_±_0</sup><sup>_._55</sup><br>|549.9<sup>_±_167</sup><sup>_._5</sup><br>|1219<sup>_±_179</sup><br>|9.63<sup>_±_0</sup><sup>_._64</sup><br>|11.02<sup>_±_0</sup><sup>_._25</sup><br>|
|Vec-Pose|100%|0%|77.1<sup>_±_12</sup><sup>_._7</sup><br>|430.3<sup>_±_248</sup><sup>_._2</sup><br>|394.0<sup>_±_55</sup><sup>_._0</sup><br>|167.0<sup>_±_4</sup><sup>_._7</sup><br>|**4.25**<sup>_±_0</sup><sup>_._20</sup><br>|**3.94**<sup>_±_0</sup><sup>_._09</sup><br>|**10.14**<sup>_±_0</sup><sup>_._10</sup><br>|434.8<sup>_±_259</sup><sup>_._9</sup><br>|1192<sup>_±_147</sup><br>|8.78<sup>_±_1</sup><sup>_._25</sup><br>|10.75<sup>_±_0</sup><sup>_._10</sup><br>|
|Vec-Dyn|100%|100%|74.6<sup>_±_0</sup><sup>_._8</sup>|444.7<sup>_±_13</sup><sup>_._3</sup>|416.7<sup>_±_6</sup><sup>_._8</sup>|147.7<sup>_±_2</sup><sup>_._3</sup>|4.87<sup>_±_0</sup><sup>_._16</sup>|4.11<sup>_±_0</sup><sup>_._16</sup>|12.20<sup>_±_0</sup><sup>_._56</sup>|**432.1**<sup>_±_9</sup><sup>_._1</sup>|1038<sup>_±_137</sup>|8.64<sup>_±_0</sup><sup>_._36</sup>|10.90<sup>_±_0</sup><sup>_._28</sup>|
|Geo-Pose|100%|100%|60.2<sup>_±_2</sup><sup>_._5</sup><br>|513.0<sup>_±_86</sup><sup>_._2</sup><br>|354.5<sup>_±_18</sup><sup>_._3</sup><br>|121.6<sup>_±_1</sup><sup>_._8</sup><br>|4.55<sup>_±_0</sup><sup>_._08</sup><br>|4.01<sup>_±_0</sup><sup>_._04</sup><br>|12.42<sup>_±_0</sup><sup>_._22</sup><br>|565.8<sup>_±_83</sup><sup>_._2</sup><br>|1071<sup>_±_72</sup><br>|8.77<sup>_±_0</sup><sup>_._98</sup><br>|10.74<sup>_±_0</sup><sup>_._11</sup><br>|
|**HAIC**|100%|100%|**57.8**<sup>_±_2</sup><sup>_._8</sup>|**417.8**<sup>_±_36</sup><sup>_._4</sup>|**335.5**<sup>_±_19</sup><sup>_._7</sup>|**117.6**<sup>_±_0</sup><sup>_._7</sup>|4.54<sup>_±_0</sup><sup>_._11</sup>|4.04<sup>_±_0</sup><sup>_._05</sup>|12.30<sup>_±_0</sup><sup>_._31</sup>|473.8<sup>_±_43</sup><sup>_._1</sup>|**1035**<sup>_±_57</sup>|**8.08**<sup>_±_0</sup><sup>_._32</sup>|**10.66**<sup>_±_0</sup><sup>_._01</sup>|


**TABLE VI:** Ablation results for **Cart Manipulation** . HAIC shows consistently high performance, achieving either the best or second-best results across most metrics. 

||||||**Robo**|**t State Metric**|**s**||||**Object Stat**|**e Metrics**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|**Method**|**SR** _↑_|_E_mpbpe_↓_|_E_g**-**mpbpe_↓_|_E_mpboe_↓_|_E_mpjpe_↓_|_E_mpbve_↓_|_E_mpbae_↓_|_E_mpjve_↓_|_E_mpope_↓_|_E_mpooe_↓_|_E_mpove_↓_|_E_mpoae_↓_|
||Proprio|60%|97.9<sup>_±_34</sup><sup>_._7</sup>|341.9<sup>_±_114</sup><sup>_._6</sup>|575.4<sup>_±_188</sup>|137.4<sup>_±_6</sup><sup>_._5</sup>|5.58<sup>_±_0</sup><sup>_._73</sup>|3.75<sup>_±_0</sup><sup>_._22</sup>|11.39<sup>_±_1</sup><sup>_._69</sup>|448.8<sup>_±_190</sup>|1551<sup>_±_149</sup>|5.90<sup>_±_2</sup><sup>_._41</sup>|3.59<sup>_±_0</sup><sup>_._06</sup>|
|Pll|Vec-Pose|60%|100.0<sup>_±_26</sup><sup>_._6</sup>|388.0<sup>_±_221</sup><sup>_._0</sup>|589.6<sup>_±_141</sup>|145.3<sup>_±_13</sup><sup>_._5</sup>|5.86<sup>_±_0</sup><sup>_._74</sup>|3.83<sup>_±_0</sup><sup>_._31</sup>|11.96<sup>_±_2</sup><sup>_._06</sup>|437.7<sup>_±_223</sup>|1530<sup>_±_212</sup>|5.78<sup>_±_1</sup><sup>_._96</sup>|3.55<sup>_±_0</sup><sup>_._03</sup>|
|u<br>Cart|Vec-Dyn<br>Geo-Pose|100%<br>100%|71.3<sup>_±_0</sup><sup>_._5</sup><br>66.1<sup>_±_0</sup><sup>_._3</sup>|244.1<sup>_±_22</sup><sup>_._3</sup><br>261.5<sup>_±_32</sup><sup>_._7</sup>|406.9<sup>_±_9</sup><sup>_._3</sup><br>384.1<sup>_±_21</sup><sup>_._7</sup>|133.7<sup>_±_1</sup><sup>_._0</sup><br>127.3<sup>_±_4</sup><sup>_._4</sup>|5.12<sup>_±_0</sup><sup>_._04</sup><br>5.29<sup>_±_0</sup><sup>_._66</sup>|3.54<sup>_±_0</sup><sup>_._01</sup><br>3.65<sup>_±_0</sup><sup>_._19</sup>|9.88<sup>_±_0</sup><sup>_._18</sup><br>10.85<sup>_±_1</sup><sup>_._52</sup>|230.1<sup>_±_16</sup><sup>_._0</sup><br>320.3<sup>_±_89</sup><sup>_._5</sup>|1640<sup>_±_108</sup><br>**1210**<sup>_±_11</sup><sup>_._6</sup>|**4.05**<sup>_±_0</sup><sup>_._02</sup><br>4.09<sup>_±_0</sup><sup>_._11</sup>|**3.52**<sup>_±_0</sup><sup>_._01</sup><br>3.57<sup>_±_0</sup><sup>_._04</sup>|
||**HAIC**|100%|**64.8**<sup>_±_2</sup><sup>_._8</sup>|**225.7**<sup>_±_3</sup><sup>_._4</sup>|**372.7**<sup>_±_34</sup><sup>_._1</sup>|**123.1**<sup>_±_0</sup><sup>_._3</sup>|**4.75**<sup>_±_0</sup><sup>_._01</sup>|**3.48**<sup>_±_0</sup><sup>_._01</sup>|**9.39**<sup>_±_0</sup><sup>_._09</sup>|**219.5**<sup>_±_6</sup><sup>_._6</sup>|1241<sup>_±_247</sup>|4.19<sup>_±_0</sup><sup>_._02</sup>|3.55<sup>_±_0</sup><sup>_._01</sup>|
||Proprio|0%|112.9<sup>_±_9</sup><sup>_._2</sup>|276.6<sup>_±_80</sup><sup>_._5</sup>|538.4<sup>_±_129</sup><sup>_._2</sup>|172.1<sup>_±_14</sup><sup>_._2</sup>|6.50<sup>_±_0</sup><sup>_._41</sup>|4.78<sup>_±_0</sup><sup>_._14</sup>|15.38<sup>_±_0</sup><sup>_._85</sup>|460.7<sup>_±_286</sup><sup>_._2</sup>|1406<sup>_±_16</sup>|4.61<sup>_±_0</sup><sup>_._91</sup>|3.75<sup>_±_0</sup><sup>_._04</sup>|
|Push<br>Cart|Vec-Pose<br>Vec-Dyn|100%<br>100%|61.5<sup>_±_1</sup><sup>_._8</sup><br>62.3<sup>_±_2</sup><sup>_._5</sup>|451.8<sup>_±_82</sup><sup>_._9</sup><br>439.0<sup>_±_75</sup><sup>_._7</sup>|**287.7**<sup>_±_3</sup><sup>_._1</sup><br>299.9<sup>_±_16</sup><sup>_._3</sup>|**125.3**<sup>_±_2</sup><sup>_._0</sup><br>126.4<sup>_±_2</sup><sup>_._2</sup>|4.65<sup>_±_0</sup><sup>_._17</sup><br>**4.58**<sup>_±_0</sup><sup>_._05</sup>|4.16<sup>_±_0</sup><sup>_._10</sup><br>**4.12**<sup>_±_0</sup><sup>_._04</sup>|11.20<sup>_±_0</sup><sup>_._91</sup><br>**10.86**<sup>_±_0</sup><sup>_._39</sup>|338.7<sup>_±_63</sup><sup>_._9</sup><br>358.4<sup>_±_73</sup><sup>_._1</sup>|**1152**<sup>_±_58</sup><br>1172<sup>_±_26</sup>|4.25<sup>_±_0</sup><sup>_._43</sup><br>4.63<sup>_±_1</sup><sup>_._03</sup>|3.71<sup>_±_0</sup><sup>_._01</sup><br>**3.70**<sup>_±_0</sup><sup>_._01</sup>|
||Geo-Pose<br>**HAIC**|100%<br>100%|64.0<sup>_±_4</sup><sup>_._8</sup><br>**61.3**<sup>_±_2</sup><sup>_._1</sup>|249.1<sup>_±_43</sup><sup>_._3</sup><br>**221.0**<sup>_±_74</sup><sup>_._3</sup>|346.8<sup>_±_28</sup><sup>_._5</sup><br>319.9<sup>_±_13</sup><sup>_._0</sup>|141.0<sup>_±_3</sup><sup>_._1</sup><br>145.9<sup>_±_5</sup><sup>_._5</sup>|4.93<sup>_±_0</sup><sup>_._06</sup><br>5.00<sup>_±_0</sup><sup>_._10</sup>|4.28<sup>_±_0</sup><sup>_._03</sup><br>4.23<sup>_±_0</sup><sup>_._08</sup>|12.70<sup>_±_0</sup><sup>_._16</sup><br>12.36<sup>_±_0</sup><sup>_._39</sup>|**259.8**<sup>_±_66</sup><sup>_._8</sup><br>267.9<sup>_±_85</sup><sup>_._6</sup>|1153<sup>_±_107</sup><br>1262<sup>_±_96</sup>|**3.65**<sup>_±_0</sup><sup>_._41</sup><br>4.04<sup>_±_1</sup><sup>_._07</sup>|**3.70**<sup>_±_0</sup><sup>_._01</sup><br>**3.70**<sup>_±_0</sup><sup>_._01</sup>|


robust stability in skateboarding and cart tasks, whereas the baseline suffers from frequent failures and trajectory drift. **Skateboarding:** Table I reports two success metrics: glide success rate (maintaining balance on the skateboard _>_ 1s) and complete success rate. While the baseline struggles to maintain basic balance, HAIC achieves a high glide success rate, demonstrating robust balance control. Although the complex dismount phase remains challenging, our method significantly outperforms the baseline, which fails to complete the task. **Cart Manipulation:** Table II highlights the robustness of HAIC. Notably, in the “Push Cart” task, the baseline fails as it cannot account for the cart’s external dynamics and nonholonomic constraints. HAIC predicts the object’s forward velocity and acceleration, allowing the robot to proactively lean into the motion, resulting in a high success rate for both “Pull” and “Push” tasks. 

_2) Sequential Interaction:_ We evaluate sequential tasks requiring mode switching: “Pull Cart w/ Box” (load the box, then pull the cart) and “Push Cart w/ Box” (load the box, then push the cart). The baseline was unable to attempt these sequential composite tasks, as it cannot reliably complete a single cart manipulation task. Therefore, Table III reports only the performance of HAIC. Despite the compounded complexity and error accumulation over a longer horizon, our framework enables the robot to transition smoothly, achieving a high success rate in the “Push Cart w/ Box” task. 

_3) Multi-terrain Interaction:_ We evaluate the robot’s ability to carry a box across varying terrains, including flat ground, 15-degree slopes, stairs, and mixed slope-stair terrains. In these scenarios, HAIC successfully picks and places a box across various types of terrains, where the policy completely occludes the robot’s visual sensors. As shown in Table IV, HAIC demonstrates superior robustness on complex terrains. While the baseline handles simple slopes, it suffers catastrophic failures on the “w/ Slope + Stair” task due to error accumulation 

in state estimation. In contrast, HAIC maintains a high success rate with lower orientation errors, validating that our geometric prior effectively compensates for the lack of visual feedback on uneven terrain. 

## _C. Ablation Study on_ HAIC 

To rigorously analyze the contribution of each component in our framework—specifically, the benefits of higher-order dynamics prediction and explicit geometric projection—we define five model variants for our ablation study: 

- **Proprio:** A standard proprioception-only policy that observes only the robot’s joint states and reference motion, without any explicit object representation. 

- **Vec-Pose:** Extends the Proprio by adding an auxiliary module that predicts the object’s position and orientation ( _p,_ ˆ _R_<sup>ˆ</sup> ). These are fed into the privilege adapter together. 

- **Vec-Dyn:** Extends Vec-Pose by predicting the comprehensive dynamics, including velocity and acceleration ( _v,_ ˆ ˆ _a_ ), which are also fed as flattened vector inputs. 

- **Geo-Pose:** Predicts the same state ( _p,_ ˆ _R_<sup>ˆ</sup> ) as Vec-Pose. The predicted pose is used to transform the canonical point cloud into the robot frame. The explicit geometric feature and predicted pose are fed to the privilege adapter. 

- **HAIC:** The proposed full method. It predicts the comprehensive dynamics ( _p,_ ˆ _R,_<sup>ˆ</sup> ˆ _v,_ ˆ _a_ ), projects the pose onto the geometric feature, and then feeds all the object’s representations into the privilege adapter. 

_1) Analysis of Training Efficiency:_ Fig. 8 illustrates the learning curves of all methods on the challenging “Push Cart w/ Box” task over 3,800 training steps. HAIC demonstrates superior sample efficiency and achieves the highest asymptotic return compared to all baselines. We further evaluate the variants in the MuJoCo simulator within the same setup for quantitative comparison. 


**Fig. 7:** Sim-to-real performance across various HOI tasks, including pushing, carrying, and terrain traversal. HAIC achieves robust interactions with diverse terrains and underactuated objects, and demonstrates strong generalization across object size, terrain orientation, and load weight. 


**Fig. 8:** Learning curves on the “Push Cart w/ Box” task. 

_2) Skateboarding:_ Table V presents the results for the dynamic skateboarding task, where Proprio struggles to maintain balance even during the glide phase, confirming the insufficiency of proprioception alone. Interestingly, while Vec-Pose achieves perfect gliding success, it fails during the dismount phase, indicating that position perception aids balance but lacks the foresight to handle impulsive forces upon stepping off. Comparing this with dynamics-aware methods highlights that predicting object acceleration is critical for managing transient disturbances. Consequently, HAIC achieves high success rates across both phases with the lowest tracking errors, indicating that our world model generates necessary feedforward compensation for stability. 

_3) Cart Manipulation:_ Table VI presents the results for cart manipulation. Proprio fails to resolve object states, while VecPose and Vec-Dyn suffer from severe trajectory drift despite completing the task. In contrast, methods utilizing geometric projection (Geo-Pose and HAIC) achieve significantly tighter global tracking by strictly aligning with the cart’s steering axis. Ultimately, HAIC delivers the best overall performance by combining this geometric alignment with dynamics prediction for precise and stable manipulation. 

_4) Other Complex Scenarios:_ We further extend the evaluation to sequential and multi-terrain tasks. Detailed metrics are provided in Appendix Table XIV and Table XV. Experimental results highlight two key advantages of HAIC: 

- Sequential Stability: In sequential tasks like “Pull Cart w/ Box”, baselines fail completely due to error accumulation. HAIC leverages its world model to mitigate drift, thereby ensuring high success rates and precise object steering across extended interaction sequences. 

- Terrain Adaptability: On the challenging “Slope + Stair” terrain, Proprio and Vec-Pose suffer from stability issues. HAIC maintains a high success rate by predicting dynamic disturbances caused by uneven ground. 

## _D. Robust interaction and Generalization_ 

To evaluate the policy’s robustness and generalization capabilities when encountering unseen object attributes and environmental changes, we designed a series of rigorous variations, including object size, terrain rotation, and loaded weight. The results are summarized in Fig. 7. 

_1) Object Size and Weight Generalization:_ We tested beyond the training range (0 _._ 1m–0 _._ 2m, 1kg–2kg). The input geometric prior _P_ remained fixed as the original standard template. The policy successfully transported a large box with a side length of 0 _._ 25m and a heavy box weighing 3kg. For heavy objects, the policy exhibited a lower center of gravity and a slower movement speed. For large-sized objects, the policy adjusted the grasping position and arm posture to avoid selfcollisions. This indicates that the world model learned general relationships between mass, inertia, and motion dynamics. 

_2) Terrain Orientation Perturbations:_ We randomly rotated slopes and stairs. The policy successfully adapted to these changes, maintaining stable walking by adjusting foot landing angles and body orientation. This demonstrates that the policy does not memorize specific terrain geometries but understands general equilibrium principles on inclined support surfaces. 

_3) External Perturbations:_ We applied instantaneous lateral thrusts during robot carrying tasks. The strategy rapidly estimated changes in object and self-momentum caused by the disturbance using the world model, swiftly restoring balance through stepping and arm swinging, demonstrating the ability to adapt online to unknown perturbations. 

_4) Extend experiment.:_ We also extend the experiment to more underactuated interaction tasks on everyday furniture in Fig. 9, and HAIC achieves a 100% success rate on all tasks, including pushing a table, a suitcase, and chairs with an extra yaw freedom on the shaft. 

These experiments demonstrate that by combining geometric priors and predictions of dynamics in end-to-end training, HAIC can acquire an understanding of the essence of physical interactions, and exhibit zero-shot generalization capabilities. 


**Fig. 9:** Real-world extend deployment experiment on everyday furniture. HAIC perform 100% SR on table, suitcase and chairs. 


**Fig. 10:** Comparison of the relative object states in robot’s local frame from dynamics-aware world model, MuJoCo and reference motion. 

## _E. Analysis and Explanation of world model_ 

_1) Comparison on world model:_ To evaluate the effectiveness of our explicit world modeling approach, we compare HAIC against Rapid Motor Adaptation (RMA) [24]. While RMA relies on an implicit environmental latent to adapt to dynamics, our DWM explicitly models the object’s physical behaviors. As summarized in Table VII, HAIC achieves superior or competitive success rates and significantly lower tracking errors across most kinematic metrics in both cart manipulation tasks. These results validate that for handling complex underactuated interactions, explicit dynamics prediction is more robust and effective than implicit adaptation. 

**TABLE VII:** Compared to the RMA baseline, HAIC achieves superior or competitive success rates and significantly lower tracking errors. 

|**Task**|**Method**|**SR** _↑_|_E_mpbpe _↓_|_E_g**-**mpbpe_↓_|_E_mpboe _↓_|_E_mpjpe _↓_|_E_mpope _↓_|_E_mpooe _↓_|
|---|---|---|---|---|---|---|---|---|
|PullCart|RMA|70%|99.1<sup>_±_38</sup><sup>_._2</sup><br>|323.1<sup>_±_110</sup><sup>_._8</sup><br>|530.6<sup>_±_168</sup><sup>_._6</sup><br>|139.9<sup>_±_5</sup><sup>_._6</sup><br>|530.6<sup>_±_168</sup><sup>_._6</sup><br>|1474<sup>_±_178</sup><sup>_._5</sup><br>|
||**HAIC**|**100%**|**64.8**<sup>_±_2</sup><sup>_._8</sup>|**225.7**<sup>_±_3</sup><sup>_._4</sup>|**372.7**<sup>_±_34</sup><sup>_._1</sup>|**123.1**<sup>_±_0</sup><sup>_._3</sup>|**219.5**<sup>_±_6</sup><sup>_._6</sup>|**1241**<sup>_±_246</sup><sup>_._5</sup>|
|PhCt|RMA|**100%**|74.1<sup>_±_6</sup><sup>_._3</sup><br>|267.0<sup>_±_52</sup><sup>_._8</sup><br>|340.8<sup>_±_30</sup><sup>_._2</sup><br>|**140.1**<sup>_±_6</sup><sup>_._0</sup><br>|519.9<sup>_±_92</sup><sup>_._9</sup><br>|**1120**<sup>_±_31</sup><sup>_._0</sup><br>|
|us ar|**HAIC**|**100%**|**61.3**<sup>_±_2</sup><sup>_._1</sup>|**221.0**<sup>_±_74</sup><sup>_._3</sup>|**319.9**<sup>_±_13</sup><sup>_._0</sup>|145.9<sup>_±_5</sup><sup>_._5</sup>|**267.9**<sup>_±_85</sup><sup>_._6</sup>|1262<sup>_±_96</sup><sup>_._2</sup>|


_2) DWM and Failure case analysis:_ We visualize the robot frame object state from DWM prediction, MuJoCo, and reference motion in Fig. 10. We select several highly salient object state components, namely translation along x or y-axis, and rotation on z-axis. For box state, the prediction closely match the simulated results. However, for challenging tasks like pushing or pulling cart and skateboarding, the predicted 

states exhibit drift from the simulated trajectories, tending to revert toward the reference motion state. This error eventually leads to an observation mismatch, preventing it from adapting effectively. When its prediction of the object state converges within a error threshold, it can ensure the policy success. When skateboard decelerates and lands, divergence from the actual state will lead to failure (60% SR). As illustrated in Fig. 10, transforming the static terrain into the robot’s local frame equips the DWM with crucial spatial awareness. This enables the system to actively alleviate heading drifts and maintain the intended path, even under terrain rotations. 

_3) Robustness to Hyperparameters and Annotations:_ As shown in Table VIII, even with imprecise thresholds, HAIC maintains a high success rate with only minor kinematic degradation. Furthermore, our binary contact masks are automatically computed via a standardized script rather than manually annotated. This algorithmic approach is generalizable across tasks and avoids human annotation noise. 

**TABLE VIII:** Ablation study on contact reward thresholds. We varied the tolerance ( _ϵ_ tol) and force threshold ( _F_ thr) parameters (Eq. 7 and 8). 


## V. CONCLUSION 

This paper introduced HAIC, a novel framework that enables humanoid robots to perform robust whole-body interactions with underactuated objects under visual occlusion by integrating a dynamic-aware world model. By fusing static geometric priors with dynamic proprioceptive feedback, our approach effectively tracks unobserved object states and anticipates environmental changes through higher-order dynamics prediction. This capability was validated in various scenarios, including climbing stairs, dynamic skateboarding, and cart manipulation, demonstrating proactive gait adjustment and balance recovery. Real-world experiments on the Unitree G1 humanoid confirm that our distilled policy achieves high performance, successfully bridging the sim-to-real gap for deployment in sensor-limited environments. 

## VI. ACKNOWLEDGMENT 

We would like to thank Xiaomi Robotics for providing the experimental site and equipment, Qingfang Li for processing the teaser material, and Shimin Li and Dongfang Li for assisting with the optical motion capture. 

REFERENCES 

- [1] Rami Ali Al-Asqhar, Taku Komura, and Myung Geol Choi. Relationship descriptors for interactive motion adaptation. In _Proceedings of the 12th ACM SIGGRAPH/Eurographics Symposium on Computer Animation_ , pages 45–53, 2013. 

- [2] Arthur Allshire, Hongsuk Choi, Junyi Zhang, David McAllister, Anthony Zhang, Chung Min Kim, Trevor Darrell, Pieter Abbeel, Jitendra Malik, and Angjoo Kanazawa. Visual imitation enables contextual humanoid control. In _Proceedings of the Conference on Robot Learning (CoRL)_ , 2025. 

- [3] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [4] Bharat Lal Bhatnagar, Xianghui Xie, Ilya Petrov, Cristian Sminchisescu, Christian Theobalt, and Gerard PonsMoll. BEHAVE: Dataset and method for tracking human object interactions. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2022. 

- [5] Zixuan Chen, Mazeyu Ji, Xuxin Cheng, Xuanbin Peng, Xue Bin Peng, and Xiaolong Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [6] Jeremy Dao, Helei Duan, and Alan Fern. Sim-toreal learning for humanoid box loco-manipulation. In _International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [7] Fan Feng, Phillip Lippe, and Sara Magliacane. Learning interactive world model for object-centric reinforcement learning. In _2511.02225_ , Thirty-ninth Conference on Neural Information Processing Systems (NeurIPS). 

- [8] Yuhui Fu, Feiyang Xie, Chaoyi Xu, Jing Xiong, Haoqi Yuan, and Zongqing Lu. Demohlm: From one demonstration to generalizable humanoid loco-manipulation. _arXiv preprint arXiv:2510.11258_ , 2025. 

- [9] Xinyang Gu, Yen-Jen Wang, Xiang Zhu, Chengming Shi, Yanjiang Guo, Yichen Liu, and Jianyu Chen. Advancing humanoid locomotion: Mastering challenging terrains with denoising world model learning. _arXiv preprint arXiv:2408.14472_ , 2024. 

- [10] David Ha and J¨urgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2(3), 2018. 

- [11] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 

- [12] Jinrui Han, Weiji Xie, Jiakun Zheng, Jiyuan Shi, Weinan Zhang, Ting Xiao, and Chenjia Bai. Kungfubot2: Learning versatile motion skills for humanoid whole-body control. _arXiv preprint arXiv:2509.16638_ , 2025. 

- [13] Nicklas Hansen, Jyothir SV, Vlad Sobal, Yann LeCun, Xiaolong Wang, and Hao Su. Hierarchical world models as visual whole-body humanoid controllers. _arXiv preprint arXiv:2405.18418_ , 2024. 

- [14] Tairan He, Jiawei Gao, Wenli Xiao, Yuanhang Zhang, Zi Wang, Jiashun Wang, Zhengyi Luo, Guanqi He, Nikhil Sobanbabu, Chaoyi Pan, Zeji Yi, Guannan Qu, Kris Kitani, Jessica Hodgins, Linxi ”Jim” Fan, Yuke Zhu, Changliu Liu, and Guanya Shi. Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [15] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Casta˜neda, Shankar Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 

- [16] Tairan He, Wenli Xiao, Toru Lin, Zhengyi Luo, Zhenjia Xu, Zhenyu Jiang, Jan Kautz, Changliu Liu, Guanya Shi, Xiaolong Wang, et al. Hover: Versatile neural wholebody controller for humanoid robots. In _International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [17] Tao Huang, Junli Ren, Huayi Wang, Zirui Wang, Qingwei Ben, Muning Wen, Xiao Chen, Jianan Li, and Jiangmiao Pang. Learning humanoid standingup control across diverse postures. _arXiv preprint arXiv:2502.08378_ , 2025. 

- [18] Jemin Hwangbo, Joonho Lee, Alexey Dosovitskiy, Dario Bellicoso, Vassilios Tsounis, Vladlen Koltun, and Marco Hutter. Learning agile and dynamic motor skills for legged robots. _Science Robotics_ , 2019. 

- [19] Youngjoon Jeong, Junha Chun, Soonwoo Cha, and Taesup Kim. Object-centric world model for languageguided manipulation. _arXiv preprint arXiv:2503.06170_ , 2025. 

- [20] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, et al. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- [21] Nan Jiang, Tengyu Liu, Zhexuan Cao, Jieming Cui, Zhiyuan Zhang, Yixin Chen, He Wang, Yixin Zhu, and Siyuan Huang. Full-body articulated human-object interaction. In _International Conference on Computer Vision (ICCV)_ , 2023. 

- [22] Nan Jiang, Zimo He, Wanhe Yu, Lexi Pang, Yunhao Li, Hongjie Li, Jieming Cui, Yuhan Li, Yizhou Wang, Yixin Zhu, et al. Uniact: Unified motion generation and action streaming for humanoid robots. _arXiv preprint arXiv:2512.24321_ , 2025. 

- [23] Dvij Kalaria, Sudarshan S Harithas, Pushkal Katara, Sangkyung Kwak, Sarthak Bhagat, Shankar Sastry, Srinath Sridhar, Sai Vemprala, Ashish Kapoor, and Jonathan Chung-Kuan Huang. Dreamcontrol: Human-inspired whole-body humanoid control for scene interaction via guided diffusion. _arXiv preprint arXiv:2509.14353_ , 2025. 

- [24] Ashish Kumar, Zipeng Fu, Deepak Pathak, and Jitendra Malik. Rma: Rapid motor adaptation for legged robots. In _Robotics: Science and Systems (RSS)_ , 2021. 

- [25] Hang Lai, Jiahang Cao, Jiafeng Xu, Hongtao Wu, Yun- 

feng Lin, Tao Kong, Yong Yu, and Weinan Zhang. World model-based perception for visual legged locomotion. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11531–11537. IEEE, 2025. 

- [26] Mikko Lauri, David Hsu, and Joni Pajarinen. Partially observable markov decision processes in robotics: A survey. _IEEE Transactions on Robotics_ , 39(1):21–40, 2023. 

- [27] Chenhao Li, Andreas Krause, and Marco Hutter. Robotic world model: A neural network simulator for robust policy optimization in robotics. _arXiv preprint arXiv:2501.10100_ , 2025. 

- [28] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, Ri-Zhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid wholebody control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [29] Jiaman Li, Jiajun Wu, and C Karen Liu. Object motion guided human motion synthesis. _ACM Trans. Graph._ , 42 (6), 2023. 

- [30] Jinhan Li, Yifeng Zhu, Yuqi Xie, Zhenyu Jiang, Mingyo Seo, Georgios Pavlakos, and Yuke Zhu. Okami: Teaching humanoid robots manipulation skills through single video imitation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [31] Yitang Li, Zhengyi Luo, Tonghe Zhang, Cunxi Dai, Anssi Kanervisto, Andrea Tirinzoni, Haoyang Weng, Kris Kitani, Mateusz Guzek, Ahmed Touati, et al. Bfmzero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. _arXiv preprint arXiv:2511.04131_ , 2025. 

- [32] Yitang Li, Yuanhang Zhang, Wenli Xiao, Chaoyi Pan, Haoyang Weng, Guanqi He, Tairan He, and Guanya Shi. Learning gentle humanoid locomotion and end-effector stabilization control. _arXiv preprint arXiv:2505.24198_ , 2025. 

- [33] Zhongyu Li, Xue Bin Peng, Pieter Abbeel, Sergey Levine, Glen Berseth, and Koushil Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _The International Journal of Robotics Research (IJRR)_ , 2024. 

- [34] Qiayuan Liao, Takara E Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [35] Yuhang Lin, Yijia Xie, Jiahong Xie, Yuehao Huang, Ruoyu Wang, Jiajun Lv, Yukai Ma, and Xingxing Zuo. Simgenhoi: Physically realistic whole-body humanoidobject interaction via generative modeling and reinforcement learning. _arXiv preprint arXiv:2508.14120_ , 2025. 

- [36] Chenhao Liu, Leyun Jiang, Yibo Wang, Kairan Yao, Jinchen Fu, and Xiaoyu Ren. Humanoid whole-body badminton via multi-stage reinforcement learning. _arXiv preprint arXiv:2511.11218_ , 2025. 

- [37] Fukang Liu, Zhaoyuan Gu, Yilin Cai, Ziyi Zhou, Shijie Zhao, Hyunyoung Jung, Sehoon Ha, Yue Chen, Danfei 

Xu, and Ye Zhao. Opt2skill: Imitating dynamicallyfeasible whole-body trajectories for versatile humanoid loco-manipulation. _arXiv preprint arXiv:2409.20514_ , 2024. 

- [38] Hang Liu, Yuman Gao, Sangli Teng, Yufeng Chi, Yakun Sophia Shao, Zhongyu Li, Maani Ghaffari, and Koushil Sreenath. Ego-vision world model for humanoid contact planning. _arXiv preprint arXiv:2510.11682_ , 2025. 

- [39] Junfeng Long, Junli Ren, Moji Shi, Zirui Wang, Tao Huang, Ping Luo, and Jiangmiao Pang. Learning humanoid locomotion with perceptive internal model. _arXiv preprint arXiv:2411.14386_ , 2024. 

- [40] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Casta˜neda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [41] Naureen Mahmood, Nima Ghorbani, Nikolaus F Troje, Gerard Pons-Moll, and Michael J Black. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 5442–5451, 2019. 

- [42] Daniel Morales-Brotons, Thijs Vogels, and Hadrien Hendrikx. Exponential moving average of weights in deep learning: Dynamics and benefits. _Trans. Mach. Learn. Res._ , 2024. 

- [43] Liang Pan, Zeshi Yang, Zhiyang Dou, Wenjia Wang, Buzhen Huang, Bo Dai, Taku Komura, and Jingbo Wang. Tokenhsi: Unified synthesis of physical human-scene interactions through task tokenization. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2025. 

- [44] Xue Bin Peng, Pieter Abbeel, Sergey Levine, and Michiel Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [45] Xue Bin Peng, Ze Ma, Pieter Abbeel, Sergey Levine, and Angjoo Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics (ToG)_ , 40(4):1–20, 2021. 

- [46] Lerrel Pinto, Marcin Andrychowicz, Peter Welinder, Wojciech Zaremba, and Pieter Abbeel. Asymmetric actor critic for image-based robot learning. _arXiv preprint arXiv:1710.06542_ , 2017. 

- [47] Ilija Radosavovic, Tete Xiao, Bike Zhang, Trevor Darrell, Jitendra Malik, and Koushil Sreenath. Real-world humanoid locomotion with reinforcement learning. _Science Robotics_ , 2024. 

- [48] Stephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics_ , 2011. 

- [49] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec 

Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [50] Yiyang Shao, Xiaoyu Huang, Bike Zhang, Qiayuan Liao, Yuman Gao, Yufeng Chi, Zhongyu Li, Sophia Shao, and Koushil Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _arXiv preprint arXiv:2504.21738_ , 2025. 

- [51] Andrea Sipos and Nima Fazeli. Simultaneous contact location and object pose estimation using proprioception and tactile feedback. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2022. 

- [52] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [53] Wandong Sun, Long Chen, Yongbo Su, Baoshi Cao, Yang Liu, and Zongwu Xie. Learning humanoid locomotion with world model reconstruction. _arXiv preprint arXiv:2502.16230_ , 2025. 

- [54] Wandong Sun, Luying Feng, Baoshi Cao, Yang Liu, Yaochu Jin, and Zongwu Xie. Ulc: A unified and fine-grained controller for humanoid loco-manipulation. _arXiv preprint arXiv:2507.06905_ , 2025. 

- [55] Omid Taheri, Nima Ghorbani, Michael J. Black, and Dimitrios Tzionas. GRAB: A dataset of whole-body human grasping of objects. In _European Conference on Computer Vision (ECCV)_ , 2020. 

- [56] Chen Tessler, Yunrong Guo, Ofir Nabati, Gal Chechik, and Xue Bin Peng. Maskedmimic: Unified physicsbased character control through masked motion inpainting. _ACM Transactions on Graphics (TOG)_ , 43(6):1–21, 2024. 

- [57] Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, and Pieter Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2017. 

- [58] Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, Qifeng Chen, Jingbo Wang, and Jiangmiao Pang. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [59] Jin Wang, Rui Dai, Weijie Wang, Luca Rossini, Francesco Ruscelli, and Nikos Tsagarakis. Hypermotion: Learning hybrid behavior planning for autonomous locomanipulation. In _Conference on Robot Learning (CoRL)_ , 2024. 

- [60] Yinhuai Wang, Jing Lin, Ailing Zeng, Zhengyi Luo, Jian Zhang, and Lei Zhang. Physhoi: Physics-based imitation of dynamic human-object interaction. _arXiv preprint arXiv:2312.04393_ , 2023. 

- [61] Yinhuai Wang, Qihan Zhao, Runyi Yu, Hok Wai Tsui, 

Ailing Zeng, Jing Lin, Zhengyi Luo, Jiwen Yu, Xiu Li, Qifeng Chen, Jian Zhang, Lei Zhang, and Ping Tan. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , pages 17540–17549, June 2025. 

- [62] Yushi Wang, Changsheng Luo, Penghui Chen, Jianran Liu, Weijian Sun, Tong Guo, Kechang Yang, Biao Hu, Yangang Zhang, and Mingguo Zhao. Learning visiondriven reactive soccer skills for humanoid robots. _arXiv preprint arXiv:2511.03996_ , 2025. 

- [63] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [64] Qianyang Wu, Ye Shi, Xiaoshui Huang, Jingyi Yu, Lan Xu, and Jingya Wang. Thor: Text to human-object interaction diffusion via relation intervention. _arXiv preprint arXiv:2403.11208_ , 2024. 

- [65] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid wholebody control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- [66] Sirui Xu, Dongting Li, Yucheng Zhang, Xiyan Xu, Qi Long, Ziyin Wang, Yunzhi Lu, Shuchang Dong, Hezi Jiang, Akshat Gupta, Yu-Xiong Wang, and Liang-Yan Gui. Interact: Advancing large-scale versatile 3d humanobject interaction generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2025. 

- [67] Sirui Xu, Hung Yu Ling, Yu-Xiong Wang, and Liangyan Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2025. 

- [68] Zifan Xu, Myoungkyu Seo, Dongmyeong Lee, Hao Fu, Jiaheng Hu, Jiaxun Cui, Yuqian Jiang, Zhihan Wang, Anastasiia Brund, Joydeep Biswas, et al. Learning agile striker skills for humanoid soccer robots from noisy sensory input. _arXiv preprint arXiv:2512.06571_ , 2025. 

- [69] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. Leverb: Humanoid whole-body control with latent visionlanguage instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [70] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interactionpreserving data generation for humanoid whole-body loco-manipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [71] Kangning Yin, Weishuai Zeng, Ke Fan, Minyue Dai, Zirui Wang, Qiang Zhang, Zheng Tian, Jingbo Wang, 

Jiangmiao Pang, and Weinan Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- [72] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C. Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid locomanipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [73] Mingqi Yuan, Tao Yu, Wenqi Ge, Xiuyong Yao, Dapeng Li, Huijiang Wang, Jiayu Chen, Xin Jin, Bo Li, Hua Chen, et al. Behavior foundation model: Towards next-generation whole-body control system of humanoid robots. _arXiv preprint arXiv:2506.20487_ , 2025. 

- [74] Yanjie Ze, Zixuan Chen, Jo˜ao Pedro Ara´ujo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [75] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [76] Weishuai Zeng, Shunlin Lu, Kangning Yin, Xiaojie Niu, Minyue Dai, Jingbo Wang, and Jiangmiao Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

- [77] Juze Zhang, Haimin Luo, Hongdi Yang, Xinru Xu, Qianyang Wu, Ye Shi, Jingyi Yu, Lan Xu, and Jingya Wang. NeuralDome: A neural modeling pipeline on multi-view human-object interactions. In _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2023. 

- [78] Yuanhang Zhang, Yifu Yuan, Prajwal Gurunath, Ishita Gupta, Shayegan Omidshafiei, Ali-akbar Agha-mohammadi, Marcell Vazquez-Chanlatte, Liam Pedersen, Tairan He, and Guanya Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [79] Zhikai Zhang, Jun Guo, Chao Chen, Jilong Wang, Chenghuai Lin, Yunrui Lian, Han Xue, Zhenrong Wang, Maoqi Liu, Jiangran Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [80] Siheng Zhao, Yanjie Ze, Yue Wang, C Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

## APPENDIX 

## _A. Dynamics-Aware World Model_ 

We select the term “world model” for our dynamics-aware world model (DWM), as our approach aligns with its fundamental definition in reinforcement learning and control: learning the environment’s transition dynamics. DWM explicitly learns the forward transition function by predicting the full state of the object from the previous state _st−_ 1 to the current state _st_ , conditioned on the robot’s action and state history. By modeling how the environment responds to robot actions, it serves as a true world model for the interaction system. 

## _B. Dataset Description_ 

To achieve robust humanoid-object interaction learning, we constructed a high-fidelity dataset covering diverse interaction scenarios. The data pipeline consists of three main stages: optical motion capture, kinematic retargeting, and physicsbased state generation. 

_1) Assets Description:_ In our experiments, we employ two primary categories of objects for interaction: fully actuated and underactuated objects. 

- Box: A standard cube with a mass of 1.3 kg. Its external dimensions are 0.36 m (length) × 0.28 m (width) × 0.35 m (height) 

- Cart: The cart has a mass of 13 kg. Its base platform measures 60 cm (width) × 90 cm (length) with a ground clearance of 17 cm, and its handle is 85 cm high. 

- Skateboard: The skateboard has a mass of 3.269 kg, equipped with four wheels (diameter 6.85 cm, thickness 5 cm). Its deck is 24 cm wide with upturned edges, and its ground clearance varies from 12 to 14 cm under load. 

The composed terrains consist of three fundamental parts: 

   - Stair: The stair has a step height of 10 cm, a tread depth of 30 cm, and a total run length of 90 cm. 

   - Slope: The slope has a vertical rise of 30 cm, a slope length of 110 cm, and an inclination angle of approximately 15°. 

   - Platform: The platform is a flat, square surface measuring 80 cm × 80 cm. This configuration is designed to replicate common geometric encountered in daily locomotion tasks. 

- _2) Data Acquisition:_ We used an optical motion capture 

- system to record the human demonstration. 

   - Volunteers: Participants wore a specialized motion capture suit (equipped with optical markers on key body landmarks) to record whole-body kinematics. 

   - Interactive Objects: Markers were affixed to the surface of interactive objects to track their 6-DoF pose (position and orientation) synchronously with the human operator. 

   - Scenarios: This dataset covers complex behaviors such as skateboarding, pulling carts, and pushing carts, as well as performing complex operations on multiple objects. 

_3) Kinematic Retargeting:_ The raw marker data was processed to drive the target humanoid robot (G1) using the PoseLib framework. 

- Humanoid Motion: The human skeleton motion was retargeted to the G1 robot’s 29-DoF kinematic structure. This process generated reference trajectories for the robot’s root position, root orientation, and 29 joint positions **_q_** . 

- Motion of Objects: The tracked object marker data were cleaned via interpolation of missing frames and transformed into canonical coordinate frames relative to the recording origin, yielding smooth 6-DoF trajectories for the object’s root link. 

- Alignment: Coordinate system transformations and spatial offsets were applied to align the human-object interaction workspace with the robot’s physical dimensions and the simulation environment. 

_4) Physics-Based Motion Representation:_ To address the discrepancy between valid interaction and purely kinematic data (lacking physical contact information), we employed a physical simulation method based on the Isaac Gym. 

- Digital Twin Simulation: We reconstructed the scene in simulation by importing the G1 robot and dynamic assets. The robot is driven kinematically by the retargeted reference motion. 

- Dynamic Objects: The objects are driven kinematically for trajectory reference. 

- Full-State Extraction: 

- _Merged Body State:_ We compute a unified state representation that concatenates the robot’s _n_ rigid bodies with the interactive _m_ objects into a single ( _n_ + _m_ )- body array. This provides global positions, linear velocities, quaternions, and angular velocities for the entire system at 50 Hz. 

- _Expanded Joint State:_ The kinematic joint state is expanded to include object articulations, resulting in a (29+ _k_ )-DoF vector (29 robot joints + _k_ object joints). 

- Contact Annotation: 

- _Body Contact:_ We heuristically compute contact binary masks by checking geometric proximity between robot links and object meshes. 

- _Foot Contact:_ Ground contact labels are generated based on foot height ( _h <_ 0 _._ 14 m) and velocity thresholds ( _v <_ 1 _._ 0 m/s), incorporating temporal hysteresis for stability. 

- Recovery Transitions: To aid reinforcement learning reset mechanisms, we procedurally generated “recovery” transition frames that interpolate between the interaction termination state and a standard “T-pose” or standing stance, ensuring valid cycle consistency during training. 

## _C. Algorithm Design_ 

_1) Observation Space Design:_ We adopt an asymmetric observation design, where the student operates under partial observability constraints to ensure deployability, while the 

**TABLE IX:** Details of the Observation Space and Privileged Information. 

|**Category**|**Observation Term**|**Noise (**_σ_**)**|**Description**|
|---|---|---|---|
||Base Angular Velocity<br>Projected Gravity<br>Joint Positions|0.05<br>0.05<br>0.015|History of base angular velocity in base frame (steps: [0]).<br>History of gravity vector projected to base frame (steps: [0]).<br>History of joint positions (steps: [0, 1, 2, 3, 4, 8]).|
|**Proprioception**|Previous Actions<br>Ref. Motion Phase<br>Ref. Joint Positions|-<br>-<br>-|Joint target history from previous 3 steps.<br>Phase variable _ϕ_ of the reference motion.<br>Future reference joint positions.|
||Ref. Body Pos (Local)<br>Ref. Contact 1 Pos<br>Ref. Contact 2 Pos<br>Objects Point Cloud|-<br>0.01<br>0.01<br>-|Future reference body positions in robot local frame.<br>Reference contact positions on Object 1.<br>Reference contact positions on Object 2 (if enabled).<br>Canonical point clouds of Object 1 & Object 2 (if enabled).|
||_Clean Proprioception_<br>Root Linear Velocity<br>Body Velocity|0.0<br>0.0<br>0.0|Noise-free history (steps: 0-8) of all proprioceptive states.<br>Linear velocity of the robot base in local frame.<br>Linear velocity of key bodies (e.g., ankles).|
||Body Height|0.0|Height of pelvis, torso, and feet relative to ground.|
||Ref. Root State (Global)|0.0|Future reference root position/orientation in global frame.|
||Ref. Diff (Local)|0.0|Difference between current and ref (pos, ori, ...) in local frame.|
||Obj. 1 State|0.01|Relative state (pos, ori, ...) of Object 1 in local frame.|
||Obj. 2 State|0.01|Relative state (pos, ori, ...) of Object 2 (if enabled) in local frame.|
|**Privileged**|Applied Forces<br>_Dynamics Randomization _<br>Body/Object Mass, Fric|-<br>_Parameters (I_<br>tion, Restituti|Real applied actions and torques.<br>_mplicitly observed by Critic):_<br>on, Object Scale, Joint Armature/Damping.|


teacher leverages privileged simulation information to facilitate training. 

**Actor Observation (Student)** The student policy _π_ relies solely on onboard sensors and reference information to ensure real-world deployability. The observation vector _ot ∈O_ primarily consists of: 

- Proprioceptive State ( _s_<sup>_prop_</sup> _t_ ): This includes a 5-step history of joint positions, joint velocities, root angular velocity, and the projected gravity vector. 

- Reference Motion ( _s_<sup>_ref_</sup> _t_ ): To guide the tracking task, the actor receives the reference motion phase _ϕt_ and a sequence of future reference joint positions. 

- Object Point Cloud ( _P_ ): To perceive the interaction target, a canonical point cloud of the objects is provided. 

**Critic Observation (Teacher)** During training, the teacher has access to the privileged state _s_<sup>_priv_</sup> _t_ to facilitate the learning of complex interaction behaviors. The details are given in Table IX. 

_2) Reward Design:_ The training objective is defined as a weighted sum of individual reward terms, maximizing the cumulative return _R_ =<sup>�</sup> _t_ � _i_<sup>_wiri,t_.Wecategorizethe</sup> rewards into four groups, detailed in Table X: _•_ Motion Tracking: Encourages the policy to mimic the reference human motion kinematics, including joint angles, body velocities, and root pose. 

- Object Interaction: Critical for task success, this group ensures the object tracks its target trajectory and enforces precise multiple objects contact. 

- Foot Constraints: specific terms designed to ensure physical realism, such as penalizing foot sliding and encour- 

aging stable swing/stance phases. 

- Regularization: Penalizes high-frequency control noise, joint limit violations, and excessive energy consumption to produce smooth and feasible motions. 

_3) Domain Randomization:_ To ensure the transferability of our policy to the physical world, we employ extensive domain randomization during training. This technique mitigates the discrepancies between the simulation and reality by modeling physical uncertainties as probabilistic distributions. We randomize a comprehensive set of parameters, ranging from the robot’s inertial and actuation properties to the physical characteristics of the interactive objects. Additionally, external perturbations are introduced to enhance stability against unforeseen disturbances. The specific randomization terms and their corresponding sampling ranges are summarized in Table XI. 

_4) PPO Hyperparameters and Network Architecture:_ We optimize the policy using PPO with the Adam optimizer, utilizing generalized advantage estimation (GAE) and a clipped surrogate objective to ensure stable training. Entropy regularization is applied to encourage exploration. Regarding the architecture, we employ an asymmetric Actor-Critic design implemented as multi-layer perceptrons (MLPs) with ELU activations. The total objective functions as a weighted sum of policy, value, and auxiliary losses. Detailed configurations and network dimensions are listed in Table XII. 

_5) Action Space and Low-level Control:_ The policy outputs actions _at ∈_ R<sup>23</sup> representing target joint positions _qtarget_ = _qt_ +∆ _q_ . Note that this dimension covers the wholebody joints excluding the 6 wrist degrees of freedom (3 per 

**TABLE X:** Reward Functions for the Humanoid-Object Interaction Task. 

|**Term**|**Expression**|**Weight**|**Description**|
|---|---|---|---|
|_(a) Motion Tracking Rewa_|_rd_|||
|Joint Position|exp(_−∥_**_q_**_−_**_q_**<sup>ref</sup>_∥_<sup>2</sup>_/σq_)|0.5|Tracks reference joint positions.|
|Joint Velocity|exp(_−∥_˙**_q_**_−_˙**_q_**<sup>ref</sup>_∥_<sup>2</sup>_/σ_˙_q_)|0.5|Tracks reference joint velocities.|
|Upper Body Pos.|exp(_−∥_**_p_**up_−_**_p_**<sup>ref</sup><br>up<sup>_∥_2</sup><sup>_/σp_)</sup>|0.5|Tracks pos. of shoulder, elbow, wrist.|
|Upper Body Ori.|exp(_−∥_**_θ_**up_⊖_**_θ_**<sup>ref</sup><br>up <sup>_∥_2</sup><sup>_/σ_</sup>_θ_<sup>)</sup>|0.5|Tracks ori. of upper body links.|
|Lower Body Pos.|exp(_−∥_**_p_**low_−_**_p_**<sup>ref</sup><br>low<sup>_∥_2</sup><sup>_/σp_)</sup>|0.5|Tracks pos. of hip, knee, ankle links.|
|Lower Body Ori.|exp(_−∥_**_θ_**low_⊖_**_θ_**<sup>ref</sup><br>low<sup>_∥_2</sup><sup>_/σθ_)</sup>|0.5|Tracks ori. of lower body links.|
|Root Position|exp(_−∥_**_p_**root_−_**_p_**<sup>ref</sup><br>root<sup>_∥_2</sup><sup>_/σp_)</sup>|0.5|Tracks pelvis position in world frame.|
|Root Orientation|exp(_−∥_**_θ_**root_⊖_**_θ_**<sup>ref</sup><br>root<sup>_∥_2</sup><sup>_/σθ_)</sup>|0.5|Tracks pelvis orientation.|
|Body Lin/Ang Vel.|exp(_−∥_**_v_**_−_**_v_**<sup>ref</sup>_∥_<sup>2</sup>_/σv_)|0.5|Tracks lin/ang velocities of bodies.|
|_(b) Object Interaction Rew_|_ard_|||
|Object Position|exp(_−∥_**_p_**obj_−_**_p_**<sup>ref</sup><br>obj<sup>_∥_2</sup><sup>_/σp_)</sup>|1.0|Tracks global position of object(s).|
|Object Orientation|exp(_−∥_**_θ_**obj_⊖_**_θ_**<sup>ref</sup><br>obj<sup>_∥_2</sup><sup>_/σθ_)</sup>|1.0|Tracks global orientation of object(s).|
|Multiple Objects Contact|1<br>_|O|_<br>�<br>_o∈O_<br>�<br>1<br>_|Eo|_<br>�<br>_e∈Eo_ <sup>I</sup><sup>_o,e · ro,e_</sup><br>pos <sup>_· ro,e_</sup><br>force<br>�|1.0|Align active body-object pairs & forces.|
|_(c) Foot Constraints_||||
|Feet Air Time|exp(clip(_t_air_−t_thr)_/σ_)_·_Istep|0.5|Encourages longer swing phases.|
|Feet Slip|_−∥_**_v_**<sup>_xy_</sup><br>foot<sup>_∥·_ Iground</sup>|0.5|Penalizes sliding velocity when grounded.|
|Feet Contact Match|exp(_−∥_I<sup>real</sup><br>con <sup>_−_Iref</sup><br>con<sup>_∥_2</sup><sup>_/σ_)</sup>|0.5|Matches reference contact states.|
|Feet Air Lift|_−_<sup>�</sup>(**_h_**foot _< h_min)_·_Iswing|0.5|Penalizes tripping during swing.|
|Impact Force|_−∥_**_F_**impact_∥_<sup>2</sup>|1.0|Penalizes large impact forces.|
|_(d) Regularization_||||
|Action Rate|_−∥_**_a_**_t −_**_a_**_t−_1_∥_<sup>2</sup>|0.1|Penalizes rapid action changes.|
|Joint Velocity L2|_−∥_˙**_q_**_∥_<sup>2</sup>|5e-4|Penalizes high velocity (energy).|
|Joint Limits|_−_<sup>�</sup>clip(**_q_**_−_**_q_**limit)|10.0|Penalizes exceeding physical limits.|
|Torque Limits|_−_<sup>�</sup>clip(**_τ_** _−_**_τ_**limit)|0.01|Penalizes torque saturation.|
|Survival|1_._0|1.0|Reward for not terminating early.|


hand), as they are not involved in the interaction tasks. These targets are processed by a low-level proportional-derivative (PD) controller to compute joint torques _τ_ : 


where _kp_ and _kd_ are the stiffness and damping gains. This residual-style control maintains compliant interaction. 

The specific PD gains used for the G1 humanoid robot are detailed in Table XIII. 

## _D. Experimental Details_ 

- _1) Experiment Setup:_ 

- Compute platform: Each experiment is conducted on a machine with a 24-core Intel i9-13900 CPU running at 5.4GHz, 64 GB of RAM, and a single NVIDIA GeForce RTX 4090 GPU, with Ubuntu 22.04. Each of our models is trained for 8 hours. 

- Real robot setup: We deploy our policies on a Unitree G1 robot. The system consists of an onboard motion control board and an external PC, connected via Ethernet. The control board collects sensor data (IMU and joint states) and transmits it to the PC using the DDS protocol. The PC, running a control loop, estimates the robot’s state, maintains observation history, and executes a Finite State 

- Machine (FSM). Inside the FSM, a dedicated RL process performs policy inference in parallel and sends target joint angles (with PD gains) back to the control board, which then issues torque commands to the motors at 500 Hz. 

- _2) Evaluation Metrics:_ 

- Global Mean Per Body Position Error ( _E_ g-mpbpe, mm): The average position error of body parts in global coordinates. 

      - _E_ g-mpbpe = E ��� **_p_** _t −_ **_p_** _t_ ref ��2� _._ (10) 

- Root-Relative Mean Per Body Position Error ( _E_ mpbpe, mm): The average position error of body parts relative to the root position. 

- _E_ mpbpe = E ���( **_p_** _t −_ **_p_** root _,_ t) _−_ ( **_p_** _t_ ref _−_ **_p_**<sup>ref</sup> root _,_ t<sup>)</sup> ��2� _._ (11) 

- _•_ Mean Per Body Orientation Error ( _E_ mpboe, 10<sup>_−_3</sup> rad): The average angular error of body part orientations using quaternion distance. 

   - _E_ mpboe = E �2 arccos � _|⟨_ **_q_** _t,_ **_q_** _t_<sup>ref</sup><sup>_⟩|_</sup> �� _._ (12) 


**TABLE XI:** Domain Randomization Parameters for Robot and Objects. 

|**Category**|**Parameter**|**Range / Distribution**|
|---|---|---|
|**_Robot Dynam_**|**_ics_**||
||Link Mass Scale|_U_(0_._9_,_1_._1)_×_default|
|Properties|Center of Mass Offset|_U_(_−_0_._02_,_0_._02) m|
||Static Friction|_U_(0_._3_,_1_._6)|
||Dynamic Friction|_U_(0_._3_,_1_._2)|
||Joint Position Offset|_U_(_−_0_._01_,_0_._01) rad|
|Actuation|Motor Stiffness Scale|_U_(0_._9_,_1_._1)|
||Motor Damping Scale|_U_(0_._9_,_1_._1)|
||Action Delay|_U_[40_,_120] ms|
|**_Object Interac_**|**_tion_**||
||Dynamic Friction|_U_(0_._3_,_0_._8)|
|Surface|Static-to-Dynamic Ratio|_U_(1_._0_,_2_._0)|
||Restitution|_U_(0_._0_,_0_._2)|
|Box|Mass<br>Scale|_U_(1_._0_,_2_._0) kg<br>_U_(0_._9_,_1_._1)|
||Body Mass<br>Wheel Mass|_U_(11_._0_,_13_._0) kg<br>_U_(0_._2_,_0_._4) kg|
|Cart|Wheel Joint Friction|_U_(0_._01_,_0_._1) N_·_m|
||Wheel Joint Damping|_U_(0_._01_,_0_._1) N_·_m_·_s/rad|
||Scale|_U_(0_._9_,_1_._1)|
||Body Mass|_U_(2_._0_,_5_._0) kg|
||Wheel Mass|_U_(0_._1_,_0_._2) kg|
|Skateboard|Wheel Armature<br>Wheel Joint Damping|_U_(0_._0_,_1e-4) kg_·_m<sup>2</sup><br>_U_(0_._0_,_1e-3) N_·_m_·_s/rad|
||Scale|_U_(0_._9_,_1_._1)|
|Slope / Stair|Scale|_U_(0_._98_,_1_._02)|
|**_External Pert_**|**_urbation_**||
|Push|Push Force<br>Push Min Interval|_U_(0_._2_,_0_._5)_×_weight<br>2s|


- Mean Per Joint Velocity Error ( _E_ mpjve, 10<sup>_−_3</sup> rad/frame): The average error of joint angular velocities. 

_E_ mpjve = E ���∆ **_θ_** _t −_ ∆ **_θ_** _t_ ref ��1� _,_ (14) 

where ∆ **_θ_** _t_ = **_θ_** _t −_ **_θ_** _t−_ 1. 

_•_ Mean Per Body Velocity Error ( _E_ mpbve, mm/frame): The average error in the linear velocities of body parts. 

- _E_ mpbve = E ���∆ **_p_** _t −_ ∆ **_p_** _t_ ref ��2� _,_ (15) 

- where ∆ **_p_** _t_ = **_p_** _t −_ **_p_** _t−_ 1. 

- Mean Per Body Acceleration Error ( _E_ mpbae, mm/frame<sup>2</sup> ): The average error in the linear accelerations of body parts. 

   - _E_ mpbae = E ���∆2 **_p_** _t −_ ∆2 **_p_** _t_ ref ��2� _,_ (16) 

where ∆<sup>2</sup> **_p_** _t_ = ∆ **_p_** _t −_ ∆ **_p_** _t−_ 1. 

- Mean Per Object Position Error ( _E_ mpope, mm): The average position error in the global coordinates of object 

**TABLE XII:** Hyperparameters related to PPO and Network Architecture. 

|**Hyperparameter**|**Value**|
|---|---|
|Optimizer|Adam|
|Number of Environments|4096|
|Rollout Steps (Horizon)|32|
|Mini-batches|8|
|Learning Epochs|3|
|Discount Factor (_γ_)|0.99|
|GAE Parameter (_λ_)|0.95|
|Clip Parameter (_ϵ_)|0.2|
|Entropy Coefficient|0.001|
|Max Gradient Norm|1.0|
|Desired KL|0.01|
|Learning Rate|3_×_10<sup>_−_4</sup>|
|Initial Noise Std|1.0|
|_Loss Coefficients_||
|Value Loss Coefficient (_λ_value)|1.0|
|Object Loss Coefficient (_λ_obj)|1.0|
|Privileged Loss Coefficient (_λ_priv)|1.0|
|Distillation Loss Coefficient (_λ_distill)|1.0|
|_Network Architecture_||
|Actor MLP Size|[512_,_256_,_256]|
|Critic MLP Size|[512_,_256_,_128]|
|Adapter MLP Size|[256_,_256]|
|Activation Function|ELU|


### **TABLE XIII:** PD controller gains for the G1 Humanoid. 

|**Joint Name**|**Stiffness (**_kp_**)**|**Damping (**_kd_**)**|
|---|---|---|
|_Legs_|||
|Left/Right Hip Pitch/Yaw|40.18|2.558|
|Left/Right Hip Roll|99.10|6.309|
|Left/Right Knee|99.10|6.309|
|Left/Right Ankle Pitch/Roll|28.50|1.814|
|_Waist_<br>Waist Yaw|40.18|2.558|
|Waist Roll/Pitch|28.50|1.814|
|_Arms_|||
|Left/Right Shoulder Pitch/Roll/Yaw|14.25|0.9072|
|Left/Right Elbow Pitch/Roll|14.25|0.9072|
|Left/Right Wrist Roll/Pitch|16.78|1.068|


- _E_ mpooe = E 2 arccos _|⟨_ **_q_** _t_<sup>obj</sup> _,_ **_q_** _t_<sup>obj</sup><sup>_,_ref</sup> _⟩| ._ (18) � � �� 

- Mean Per Object Velocity Error ( _E_ mpove, mm/frame): The average error in object linear velocities. 


**TABLE XIV:** Ablation results for **Sequential Interaction** . The complexity of sequentially loading and manipulating objects causes error accumulation in Proprio. Proprio and Vec-Pose fail completely on “Pull Cart w/ Box”. **HAIC** maintains a high success rate across both tasks and achieves the lowest object orientation error in the “Push” phase, confirming that the dynamic-aware world model effectively mitigates drift over long horizons. 

||||||**Rob**|**ot State Metri**|**cs**||||**Object Stat**|**e Metrics**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|**Method**|**SR** _↑_|_E_mpbpe_↓_|_E_g**-**mpbpe_↓_|_E_mpboe_↓_|_E_mpjpe_↓_|_E_mpbve_↓_|_E_mpbae_↓_|_E_mpjve_↓_|_E_mpope_↓_|_E_mpooe_↓_|_E_mpove_↓_|_E_mpoae_↓_|
|Pull Cart<br>w/ Box|Proprio<br>Vec-Pose<br>Vec-Dyn<br>Geo-Pose|0%<br>0%<br>100%<br>100%|117.9<sup>_±_31</sup><sup>_._3</sup><br>138.7<sup>_±_2</sup><sup>_._5</sup><br>**59.7**<sup>_±_2</sup><sup>_._7</sup><br>69.8<sup>_±_2</sup><sup>_._0</sup>|354.7<sup>_±_93</sup><sup>_._0</sup><br>444.8<sup>_±_118</sup><br>204.7<sup>_±_21</sup><sup>_._2</sup><br>302.2<sup>_±_65</sup><sup>_._9</sup>|590.8<sup>_±_124</sup><br>780.9<sup>_±_75</sup><sup>_._7</sup><br>**333.5**<sup>_±_15</sup><sup>_._0</sup><br>376.6<sup>_±_14</sup><sup>_._5</sup>|162.7<sup>_±_14</sup><sup>_._1</sup><br>155.8<sup>_±_1</sup><sup>_._4</sup><br>**130.0**<sup>_±_2</sup><sup>_._0</sup><br>138.4<sup>_±_0</sup><sup>_._9</sup>|5.67<sup>_±_0</sup><sup>_._24</sup><br>5.25<sup>_±_0</sup><sup>_._09</sup><br>**5.18**<sup>_±_0</sup><sup>_._14</sup><br>5.63<sup>_±_0</sup><sup>_._13</sup>|4.64<sup>_±_0</sup><sup>_._04</sup><br>**4.55**<sup>_±_0</sup><sup>_._02</sup><br>4.64<sup>_±_0</sup><sup>_._10</sup><br>4.75<sup>_±_0</sup><sup>_._02</sup>|12.21<sup>_±_0</sup><sup>_._15</sup><br>**10.57**<sup>_±_0</sup><sup>_._25</sup><br>11.88<sup>_±_0</sup><sup>_._42</sup><br>12.45<sup>_±_0</sup><sup>_._19</sup>|501.6<sup>_±_47</sup><sup>_._3</sup><br>550.6<sup>_±_218</sup><br>**300.6**<sup>_±_26</sup><sup>_._1</sup><br>414.7<sup>_±_64</sup><sup>_._7</sup>|454.4<sup>_±_13</sup><sup>_._5</sup><br>**438.7**<sup>_±_77</sup><sup>_._6</sup><br>499.3<sup>_±_66</sup><sup>_._3</sup><br>635.5<sup>_±_68</sup><sup>_._1</sup>|4.63<sup>_±_1</sup><sup>_._04</sup><br>4.83<sup>_±_0</sup><sup>_._92</sup><br>**4.06**<sup>_±_0</sup><sup>_._39</sup><br>4.47<sup>_±_0</sup><sup>_._37</sup>|2.87<sup>_±_0</sup><sup>_._01</sup><br>2.87<sup>_±_0</sup><sup>_._01</sup><br>2.88<sup>_±_0</sup><sup>_._01</sup><br>2.88<sup>_±_0</sup><sup>_._01</sup>|
||**HAIC**|100%|64.4<sup>_±_2</sup><sup>_._1</sup>|**196.5**<sup>_±_29</sup><sup>_._5</sup>|343.7<sup>_±_20</sup><sup>_._3</sup>|135.8<sup>_±_5</sup><sup>_._2</sup>|5.24<sup>_±_0</sup><sup>_._14</sup>|4.65<sup>_±_0</sup><sup>_._06</sup>|12.17<sup>_±_0</sup><sup>_._46</sup>|332.9<sup>_±_30</sup><sup>_._0</sup>|561.3<sup>_±_22</sup><sup>_._6</sup>|4.35<sup>_±_0</sup><sup>_._26</sup>|**2.86**<sup>_±_0</sup><sup>_._01</sup>|
|Push Cart<br>w/ Box|Proprio<br>Vec-Pose<br>Vec-Dyn<br>Geo-Pose<br>**HAIC**|0%<br>80%<br>100%<br>100%<br>100%|99.7<sup>_±_39</sup><sup>_._2</sup><br>66.2<sup>_±_2</sup><sup>_._0</sup><br>68.3<sup>_±_5</sup><sup>_._0</sup><br>**58.2**<sup>_±_1</sup><sup>_._0</sup><br>60.2<sup>_±_3</sup><sup>_._2</sup>|520.7<sup>_±_240</sup><br>451.9<sup>_±_69</sup><sup>_._3</sup><br>490.2<sup>_±_46</sup><sup>_._3</sup><br>360.2<sup>_±_9</sup><sup>_._1</sup><br>**326.5**<sup>_±_11</sup><sup>_._3</sup>|605.0<sup>_±_263</sup><br>393.6<sup>_±_13</sup><sup>_._4</sup><br>407.7<sup>_±_21</sup><sup>_._9</sup><br>**324.8**<sup>_±_6</sup><sup>_._0</sup><br>327.7<sup>_±_4</sup><sup>_._3</sup>|167.0<sup>_±_9</sup><sup>_._6</sup><br>175.2<sup>_±_3</sup><sup>_._5</sup><br>156.2<sup>_±_6</sup><sup>_._1</sup><br>141.6<sup>_±_2</sup><sup>_._0</sup><br>**140.8**<sup>_±_0</sup><sup>_._8</sup>|5.67<sup>_±_0</sup><sup>_._64</sup><br>4.97<sup>_±_0</sup><sup>_._15</sup><br>5.00<sup>_±_0</sup><sup>_._24</sup><br>4.95<sup>_±_0</sup><sup>_._13</sup><br>**4.75**<sup>_±_0</sup><sup>_._03</sup>|3.84<sup>_±_0</sup><sup>_._27</sup><br>3.52<sup>_±_0</sup><sup>_._11</sup><br>3.48<sup>_±_0</sup><sup>_._09</sup><br>3.54<sup>_±_0</sup><sup>_._08</sup><br>**3.42**<sup>_±_0</sup><sup>_._02</sup>|12.23<sup>_±_1</sup><sup>_._42</sup><br>11.42<sup>_±_0</sup><sup>_._52</sup><br>11.68<sup>_±_0</sup><sup>_._51</sup><br>11.39<sup>_±_0</sup><sup>_._42</sup><br>**10.73**<sup>_±_0</sup><sup>_._05</sup>|536.7<sup>_±_171</sup><br>499.3<sup>_±_79</sup><sup>_._4</sup><br>519.0<sup>_±_47</sup><sup>_._1</sup><br>491.3<sup>_±_68</sup><sup>_._1</sup><br>**386.7**<sup>_±_18</sup><sup>_._0</sup>|362.2<sup>_±_78</sup><sup>_._5</sup><br>422.3<sup>_±_41</sup><sup>_._9</sup><br>386.3<sup>_±_72</sup><sup>_._6</sup><br>419.1<sup>_±_63</sup><sup>_._7</sup><br>**326.9**<sup>_±_7</sup><sup>_._3</sup>|4.43<sup>_±_1</sup><sup>_._01</sup><br>4.22<sup>_±_0</sup><sup>_._28</sup><br>4.06<sup>_±_0</sup><sup>_._22</sup><br>4.11<sup>_±_0</sup><sup>_._12</sup><br>**4.00**<sup>_±_0</sup><sup>_._13</sup>|3.03<sup>_±_0</sup><sup>_._03</sup><br>3.02<sup>_±_0</sup><sup>_._01</sup><br>3.01<sup>_±_0</sup><sup>_._01</sup><br>3.02<sup>_±_0</sup><sup>_._02</sup><br>**3.00**<sup>_±_0</sup><sup>_._01</sup>|


**TABLE XV:** Ablation results for **Multi-terrain Interaction** . **HAIC** achieves the most consistent success rate across all terrains, while Geo-Pose demonstrates superior stability in velocity and acceleration metrics on complex stair terrains due to the explicit geometric projection. 

||||||**Rob**|**ot State Metri**|**cs**||||**Object Stat**|**e Metrics**||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Task**|**Method**|**SR** _↑_|_E_mpbpe|_E_g**-**mpbpe_↓_|_E_mpboe_↓_|_E_mpjpe_↓_|_E_mpbve_↓_|_E_mpbae_↓_|_E_mpjve_↓_|_E_mpope_↓_|_E_mpooe_↓_|_E_mpove_↓_|_E_mpoae_↓_|
|Carry<br>Box|Proprio<br>Vec-Pose<br>Vec-Dyn<br>Geo-Pose<br>**HAIC**|100%<br>100%<br>100%<br>100%<br>100%|61.8<sup>_±_4</sup><sup>_._8</sup><br>**59.3**<sup>_±_4</sup><sup>_._4</sup><br>73.2<sup>_±_5</sup><sup>_._3</sup><br>69.4<sup>_±_1</sup><sup>_._6</sup><br>64.3<sup>_±_2</sup><sup>_._9</sup>|166.3<sup>_±_10</sup><sup>_._3</sup><br>**155.7**<sup>_±_17</sup><sup>_._6</sup><br>220.2<sup>_±_52</sup><sup>_._1</sup><br>221.8<sup>_±_13</sup><sup>_._8</sup><br>173.2<sup>_±_34</sup><sup>_._4</sup>|323.6<sup>_±_16</sup><sup>_._7</sup><br>**315.9**<sup>_±_19</sup><sup>_._3</sup><br>340.2<sup>_±_24</sup><sup>_._1</sup><br>318.7<sup>_±_6</sup><sup>_._9</sup><br>320.4<sup>_±_18</sup><sup>_._7</sup>|**181.6**<sup>_±_5</sup><sup>_._0</sup><br>194.5<sup>_±_1</sup><sup>_._4</sup><br>198.2<sup>_±_2</sup><sup>_._9</sup><br>209.3<sup>_±_1</sup><sup>_._2</sup><br>182.5<sup>_±_0</sup><sup>_._8</sup>|5.34<sup>_±_0</sup><sup>_._23</sup><br>5.78<sup>_±_0</sup><sup>_._12</sup><br>5.19<sup>_±_0</sup><sup>_._06</sup><br>**4.82**<sup>_±_0</sup><sup>_._12</sup><br>5.17<sup>_±_0</sup><sup>_._05</sup>|3.34<sup>_±_0</sup><sup>_._07</sup><br>3.72<sup>_±_0</sup><sup>_._08</sup><br>3.32<sup>_±_0</sup><sup>_._06</sup><br>**3.18**<sup>_±_0</sup><sup>_._07</sup><br>3.23<sup>_±_0</sup><sup>_._04</sup>|11.08<sup>_±_0</sup><sup>_._50</sup><br>13.49<sup>_±_0</sup><sup>_._28</sup><br>11.20<sup>_±_0</sup><sup>_._28</sup><br>**10.20**<sup>_±_0</sup><sup>_._18</sup><br>10.29<sup>_±_0</sup><sup>_._15</sup>|180.1<sup>_±_12</sup><sup>_._0</sup><br>**161.8**<sup>_±_24</sup><sup>_._6</sup><br>197.5<sup>_±_50</sup><sup>_._4</sup><br>184.6<sup>_±_22</sup><sup>_._5</sup><br>176.0<sup>_±_30</sup><sup>_._9</sup>|**129.0**<sup>_±_7</sup><sup>_._3</sup><br>149.9<sup>_±_22</sup><sup>_._6</sup><br>517.4<sup>_±_45</sup><sup>_._8</sup><br>258.3<sup>_±_8</sup><sup>_._7</sup><br>169.2<sup>_±_5</sup><sup>_._5</sup>|7.23<sup>_±_0</sup><sup>_._09</sup><br>6.92<sup>_±_0</sup><sup>_._22</sup><br>7.24<sup>_±_0</sup><sup>_._35</sup><br>**6.26**<sup>_±_0</sup><sup>_._25</sup><br>6.42<sup>_±_0</sup><sup>_._23</sup>|1.84<sup>_±_0</sup><sup>_._05</sup><br>2.23<sup>_±_0</sup><sup>_._11</sup><br>1.99<sup>_±_0</sup><sup>_._08</sup><br>1.71<sup>_±_0</sup><sup>_._04</sup><br>**1.62**<sup>_±_0</sup><sup>_._02</sup>|
||Proprio<br>Vec-Pose|100%<br>100%|66.1<sup>_±_4</sup><sup>_._6</sup><br>55.3<sup>_±_1</sup><sup>_._3</sup>|234.7<sup>_±_28</sup><sup>_._8</sup><br>218.0<sup>_±_11</sup><sup>_._4</sup>|351.5<sup>_±_15</sup><sup>_._5</sup><br>300.6<sup>_±_9</sup><sup>_._8</sup>|166.5<sup>_±_10</sup><sup>_._8</sup><br>132.3<sup>_±_1</sup><sup>_._5</sup>|4.95<sup>_±_0</sup><sup>_._20</sup><br>4.34<sup>_±_0</sup><sup>_._05</sup>|4.14<sup>_±_0</sup><sup>_._06</sup><br>3.95<sup>_±_0</sup><sup>_._02</sup>|12.02<sup>_±_0</sup><sup>_._36</sup><br>9.41<sup>_±_0</sup><sup>_._17</sup>|148.2<sup>_±_20</sup><sup>_._9</sup><br>**138.4**<sup>_±_35</sup><sup>_._5</sup>|193.9<sup>_±_100</sup><sup>_._8</sup><br>390.9<sup>_±_101</sup><sup>_._2</sup>|3.88<sup>_±_0</sup><sup>_._40</sup><br>3.79<sup>_±_0</sup><sup>_._23</sup>|2.57<sup>_±_0</sup><sup>_._09</sup><br>2.40<sup>_±_0</sup><sup>_._06</sup>|
|w/ Stair|Vec-Dyn|100%|57.8<sup>_±_4</sup><sup>_._4</sup><br>|**216.4**<sup>_±_9</sup><sup>_._9</sup><br>|317.3<sup>_±_30</sup><sup>_._3</sup><br>|132.1<sup>_±_0</sup><sup>_._5</sup><br>|4.39<sup>_±_0</sup><sup>_._02</sup><br>|3.97<sup>_±_0</sup><sup>_._03</sup><br>|9.61<sup>_±_0</sup><sup>_._01</sup><br>|149.5<sup>_±_29</sup><sup>_._0</sup><br>|294.8<sup>_±_145</sup><sup>_._7</sup><br>|3.73<sup>_±_0</sup><sup>_._06</sup><br>|2.38<sup>_±_0</sup><sup>_._02</sup><br>|
||Geo-Pose<br>**HAIC**|100%<br>100%|53.7<sup>_±_1</sup><sup>_._0</sup><br>**53.5**<sup>_±_0</sup><sup>_._9</sup>|283.0<sup>_±_30</sup><sup>_._8</sup><br>281.5<sup>_±_72</sup><sup>_._9</sup>|302.9<sup>_±_1</sup><sup>_._7</sup><br>**290.5**<sup>_±_0</sup><sup>_._8</sup>|132.6<sup>_±_1</sup><sup>_._3</sup><br>**127.5**<sup>_±_2</sup><sup>_._5</sup>|**3.91**<sup>_±_0</sup><sup>_._01</sup><br>4.34<sup>_±_0</sup><sup>_._04</sup>|**3.84**<sup>_±_0</sup><sup>_._03</sup><br>3.95<sup>_±_0</sup><sup>_._03</sup>|**8.91**<sup>_±_0</sup><sup>_._11</sup><br>9.67<sup>_±_0</sup><sup>_._08</sup>|168.9<sup>_±_7</sup><sup>_._9</sup><br>154.5<sup>_±_29</sup><sup>_._8</sup>|82.0<sup>_±_2</sup><sup>_._6</sup><br>**71.0**<sup>_±_7</sup><sup>_._4</sup>|**3.17**<sup>_±_0</sup><sup>_._05</sup><br>3.41<sup>_±_0</sup><sup>_._03</sup>|**2.32**<sup>_±_0</sup><sup>_._04</sup><br>2.40<sup>_±_0</sup><sup>_._02</sup>|
||Proprio<br>Vec-Pose|100%<br>100%|**54.6**<sup>_±_1</sup><sup>_._1</sup><br>60.7<sup>_±_2</sup><sup>_._5</sup>|186.6<sup>_±_14</sup><sup>_._4</sup><br>235.6<sup>_±_16</sup><sup>_._5</sup>|317.7<sup>_±_3</sup><sup>_._6</sup><br>340.8<sup>_±_9</sup><sup>_._8</sup>|138.4<sup>_±_2</sup><sup>_._4</sup><br>150.4<sup>_±_2</sup><sup>_._0</sup>|**3.72**<sup>_±_0</sup><sup>_._04</sup><br>3.91<sup>_±_0</sup><sup>_._03</sup>|**3.30**<sup>_±_0</sup><sup>_._03</sup><br>3.35<sup>_±_0</sup><sup>_._04</sup>|**8.78**<sup>_±_0</sup><sup>_._08</sup><br>9.20<sup>_±_0</sup><sup>_._09</sup>|105.4<sup>_±_5</sup><sup>_._1</sup><br>130.5<sup>_±_9</sup><sup>_._5</sup>|108.4<sup>_±_17</sup><sup>_._0</sup><br>109.5<sup>_±_18</sup><sup>_._6</sup>|3.06<sup>_±_0</sup><sup>_._06</sup><br>3.29<sup>_±_0</sup><sup>_._09</sup>|**1.71**<sup>_±_0</sup><sup>_._02</sup><br>1.74<sup>_±_0</sup><sup>_._01</sup>|
|w/ Slope|Vec-Dyn|100%|59.4<sup>_±_1</sup><sup>_._2</sup>|229.4<sup>_±_12</sup><sup>_._1</sup>|322.9<sup>_±_7</sup><sup>_._0</sup>|**129.7**<sup>_±_0</sup><sup>_._5</sup>|3.93<sup>_±_0</sup><sup>_._04</sup>|3.33<sup>_±_0</sup><sup>_._02</sup>|9.30<sup>_±_0</sup><sup>_._13</sup>|134.4<sup>_±_3</sup><sup>_._0</sup>|**75.7**<sup>_±_5</sup><sup>_._1</sup>|3.37<sup>_±_0</sup><sup>_._14</sup>|1.74<sup>_±_0</sup><sup>_._01</sup>|
||Geo-Pose|100%|70.3<sup>_±_1</sup><sup>_._9</sup>|198.9<sup>_±_28</sup><sup>_._8</sup>|404.3<sup>_±_3</sup><sup>_._4</sup>|175.9<sup>_±_3</sup><sup>_._1</sup>|4.39<sup>_±_0</sup><sup>_._04</sup>|3.43<sup>_±_0</sup><sup>_._03</sup>|9.96<sup>_±_0</sup><sup>_._10</sup>|198.9<sup>_±_28</sup><sup>_._8</sup>|145.1<sup>_±_24</sup><sup>_._1</sup>|3.31<sup>_±_0</sup><sup>_._16</sup>|1.84<sup>_±_0</sup><sup>_._02</sup>|
||**HAIC**|100%|58.5<sup>_±_1</sup><sup>_._2</sup>|**163.1**<sup>_±_31</sup><sup>_._0</sup>|**314.4**<sup>_±_8</sup><sup>_._0</sup>|131.8<sup>_±_4</sup><sup>_._0</sup>|3.90<sup>_±_0</sup><sup>_._08</sup>|3.32<sup>_±_0</sup><sup>_._02</sup>|8.94<sup>_±_0</sup><sup>_._26</sup>|**99.0**<sup>_±_11</sup><sup>_._3</sup>|80.4<sup>_±_9</sup><sup>_._4</sup>|**2.93**<sup>_±_0</sup><sup>_._08</sup>|1.73<sup>_±_0</sup><sup>_._03</sup>|
||Proprio|60%|91.0<sup>_±_36</sup><sup>_._9</sup>|702.9<sup>_±_203</sup><sup>_._9</sup>|462.4<sup>_±_192</sup><sup>_._2</sup>|185.3<sup>_±_16</sup><sup>_._5</sup>|5.22<sup>_±_0</sup><sup>_._53</sup>|3.86<sup>_±_0</sup><sup>_._21</sup>|13.01<sup>_±_1</sup><sup>_._17</sup>|358.9<sup>_±_72</sup><sup>_._4</sup>|337.1<sup>_±_117</sup><sup>_._8</sup>|4.33<sup>_±_0</sup><sup>_._45</sup>|2.30<sup>_±_0</sup><sup>_._05</sup>|
|/Sl|Vec-Pose|60%|93.2<sup>_±_52</sup><sup>_._6</sup>|448.1<sup>_±_122</sup><sup>_._3</sup>|503.2<sup>_±_312</sup><sup>_._7</sup>|165.5<sup>_±_26</sup><sup>_._4</sup>|4.84<sup>_±_0</sup><sup>_._32</sup>|3.66<sup>_±_0</sup><sup>_._14</sup>|11.87<sup>_±_0</sup><sup>_._84</sup>|222.1<sup>_±_37</sup><sup>_._6</sup>|183.7<sup>_±_88</sup><sup>_._7</sup>|4.49<sup>_±_0</sup><sup>_._17</sup>|2.30<sup>_±_0</sup><sup>_._04</sup>|
|w ope<br>+Sti|Vec-Dyn|100%|65.3<sup>_±_6</sup><sup>_._0</sup>|336.2<sup>_±_69</sup><sup>_._8</sup>|367.8<sup>_±_44</sup><sup>_._9</sup>|151.5<sup>_±_1</sup><sup>_._1</sup>|**4.29**<sup>_±_0</sup><sup>_._12</sup>|**3.47**<sup>_±_0</sup><sup>_._03</sup>|**10.75**<sup>_±_0</sup><sup>_._28</sup>|202.8<sup>_±_30</sup><sup>_._6</sup>|130.1<sup>_±_27</sup><sup>_._2</sup>|3.92<sup>_±_0</sup><sup>_._26</sup>|2.26<sup>_±_0</sup><sup>_._02</sup>|
|ar|Geo-Pose<br>**HAIC**|100%<br>100%|**62.3**<sup>_±_6</sup><sup>_._9</sup><br>67.7<sup>_±_1</sup><sup>_._9</sup>|320.3<sup>_±_129</sup><sup>_._0</sup><br>**250.1**<sup>_±_29</sup><sup>_._4</sup>|**321.0**<sup>_±_61</sup><sup>_._0</sup><br>327.8<sup>_±_7</sup><sup>_._5</sup>|**144.1**<sup>_±_8</sup><sup>_._2</sup><br>154.2<sup>_±_4</sup><sup>_._2</sup>|4.63<sup>_±_0</sup><sup>_._44</sup><br>4.75<sup>_±_0</sup><sup>_._16</sup>|3.83<sup>_±_0</sup><sup>_._05</sup><br>3.56<sup>_±_0</sup><sup>_._07</sup>|11.92<sup>_±_1</sup><sup>_._25</sup><br>11.98<sup>_±_0</sup><sup>_._61</sup>|**149.7**<sup>_±_5</sup><sup>_._6</sup><br>157.2<sup>_±_3</sup><sup>_._8</sup>|179.1<sup>_±_173</sup><sup>_._9</sup><br>**121.4**<sup>_±_7</sup><sup>_._8</sup>|**3.53**<sup>_±_0</sup><sup>_._63</sup><br>4.01<sup>_±_0</sup><sup>_._02</sup>|**1.72**<sup>_±_0</sup><sup>_._47</sup><br>2.29<sup>_±_0</sup><sup>_._01</sup>|


- where ∆ **_p_**<sup>obj</sup> _t_ = **_p_**<sup>obj</sup> _t −_ **_p_**<sup>obj</sup> _t−_ 1<sup>.</sup> 

- _•_ Mean Per Object Acceleration Error ( _E_ mpoae, mm/frame<sup>2</sup> ): The average error of object linear accelerations. 


## _E. Additional Experimental Results_ 

_1) Inference Latency:_ Real-time feasibility is paramount for agile interaction. By utilizing a sparse canonical template instead of dense raw scans, the explicit geometric projection (Eq. 2) is simplified to efficient vectorized matrix operations. The benchmarks on Unitree G1 confirm that the total inference latency averages 0.17 ms, consuming less than 1% of the control period of 20 ms (50 Hz). This negligible overhead guarantees an instantaneous response capability for high-speed tasks such as skateboarding. 

_2) Ablation Study for Sequential Interaction:_ Table XIV evaluates the performance in sequential tasks. 

**Failure of Baselines in Sequential Tasks:** The complexity of these tasks causes a severe accumulation of errors in baseline methods. Proprio and Vec-Pose fail completely on the “Pull 

Cart w/ Box” task, dropping to a 0% success rate. This indicates that standard policies without explicit future prediction struggle to coordinate the transition between manipulating the box and controlling the cart. 

**Mitigating Sequential Drift:** In contrast, HAIC maintains a high success rate across both “Pull” and “Push” tasks. Our dynamics-aware world model effectively mitigates the drift that typically accumulates over long horizons. This is evidenced by the significantly lower global body position error in the “Pull” task. 

**Precision in Complex Interaction:** In the “Push Cart w/ Box” task, HAIC achieves the best performance across almost all metrics. Notably, it records the lowest object orientation error, demonstrating that our method can stably steer the cartbox system, whereas other methods struggle to maintain the heading of the coupled objects. 

_3) Ablation Study for Multi-terrain Interaction:_ Table XV compares the performance across different terrains. **Robustness Comparison:** On simple terrains, all methods achieve a high success rate. However, on the most challenging slope-stair terrain, Proprio and Vec-Pose fail to adapt to rapid height changes. In contrast, HAIC maintains a high success rate across all scenarios, showing superior robustness against environmental complexity. 

**Tracking Accuracy:** HAIC consistently achieves lower tracking errors than the baselines. On the slope-stair terrain, our method outperforms Geo-Pose significantly in global body position error and object orientation error. This indicates that our policy generates more stable whole-body motions and precise object manipulation. 

