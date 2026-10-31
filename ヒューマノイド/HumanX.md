---
title: "HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos"
date: "2026-02-02"
authors: "Yinhuai Wang; Qihan Zhao; Yuen Fui Lau; Runyi Yu; Hok Wai Tsui; Qifeng Chen"
url: https://arxiv.org/abs/2602.02473
pdf: https://arxiv.org/pdf/2602.02473
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.02473)** / [論文ページ](https://arxiv.org/abs/2602.02473)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HumanX: Toward Agile and Generalizable Humanoid Interaction Skills from Human Videos** 

**Yinhuai Wang**<sup>**1,2**</sup><sup>_∗_</sup> **, Qihan Zhao**<sup>**1**</sup><sup>_∗_</sup> **, Yuen Fui Lau**<sup>**1**</sup><sup>_∗_</sup> **, Runyi Yu**<sup>**1**</sup> **, Hok Wai Tsui**<sup>**1**</sup> **Qifeng Chen**<sup>**1**</sup><sup>_†_</sup> **, Jingbo Wang**<sup>**2**</sup><sup>_†_</sup> **, Jiangmiao Pang**<sup>**2**</sup> **, Ping Tan**<sup>**1**</sup><sup>_†_</sup> 

1The Hong Kong University of Science and Technology 2Shanghai AI Laboratory 

> _∗_ Equal contribution _†_ Corresponding authors **https://wyhuai.github.io/human-x/** 


Figure 1: Breaking away from task-specific engineering, we introduce a unified framework that compiles human video into generalizable, real-world humanoid interaction skills, such as basketball dribbling, jumpshots, layups, consecutive football kicks, generalizable cargo pickup, and real-time counterattacks against a human, showing generalization far beyond the original human video. 

**Abstract:** Enabling humanoid robots to perform agile and adaptive interactions has long been a core challenge in robotics. Current approaches are bottlenecked by either the scarcity of realistic interaction data or the need for meticulous, taskspecific reward engineering, which limits their scalability. To narrow this gap, we present HumanX, a unified framework that compiles human video into generalizable, real-world interaction skills for humanoids, without per-task design. HumanX integrates two co-designed components: XGen, an anchor-centric data generation pipeline that yields physically plausible robot interaction data from monocular video and augments it to create a diverse, scalable training dataset; and XMimic, an interaction-prioritized learning framework to achieve generalizable interaction skills from seconds of demonstration. Evaluated across five distinct domains—basketball, football, badminton, cargo pickup, and reactive fighting—HumanX successfully acquires 9 different skills and transfers them zero-shot to a physical Unitree G1 humanoid. The learned capabilities include complex maneuvers such as pump-fake turnaround fadeaway jumpshots without any external perception, as well as interactive tasks like sustained human-robot passing sequences over 10 consecutive cycles—learned from a single video demonstration. Our experiments show that HumanX achieves higher generalization success than prior methods, demonstrating a scalable pathway within a class of anchorable interactions for learning versatile, real-world robot interactive skills. 

**Keywords:** Humanoids, Whole-Body Control, Learning from Human Video 

10th Conference on Robot Learning (CoRL 2026), Austin TX, USA. 

## **1 Introduction** 

Humanoid robots share a morphological affinity with humans, offering the potential to operate seamlessly in human environments and interact with everyday objects. This inherent compatibility points to a vast, yet largely untapped resource: the rich diversity of skills demonstrated in human motion. However, unlocking this potential for robot learning remains a challenge. While behavior cloning (BC) offers a simple and unified training paradigm, it relies on large-scale, costly teleoperated demonstrations [1, 2, 3]. Although reinforcement learning (RL) combined with physics simulation can substantially reduce the demand for large quantities of high-quality demonstrations, it usually requires meticulously engineered, task-specific reward functions, limiting its scalability across diverse tasks [4, 5, 6, 7, 8, 9]. Together, these bottlenecks have constrained the development of a general, scalable pipeline for acquiring humanoid interaction skills from human. 

To address these limitations, we introduce HumanX, a full-stack framework that compiles human video into generalizable, real-world interaction skills for humanoids, without per-task design. HumanX integrates two synergistic components: XGen, an anchor-centered data-generation pipeline that yields diverse and physically plausible humanoid interaction data from monocular video while enabling scalable augmentation; and XMimic, a unified interaction-prioritized learning framework that enables the mastery of generalizable interaction skills with only seconds of HOI data. 

While estimating human and object motion separately from monocular video is well-studied [10, 11, 12, 13, 14], naively combining such independent estimates often yields physically implausible results due to issues like occlusion and depth ambiguity [15, 16]. XGen addresses this by fundamentally shifting the paradigm: it _synthesizes_ interaction trajectories governed by physical rules, rather than pursuing exact _reconstruction_ . This shift enables highly efficient data augmentation, allowing XGen to generate a broad distribution of physically consistent interaction trajectories from just a single video demonstration. Concretely, XGen operates in three stages: (1) extracting human motion and retargeting it to the robot; (2) interaction synthesis: anchor-object configuration, anchor-based object trajectory synthesis, and contact refinement; (3) data augmentation through object geometry scaling and trajectory variation to maximize coverage for improved generalization. Instead of pursuing task-specific solutions [17, 18, 19, 20], XMimic adopts an unified imitation paradigm for learning interaction skills. However, separately imitating body and object motions often results in weak interaction robustness and generalization [21, 22]. We identify that the core of interaction skills lies in the relative motion patterns between robot and object, which we formulated as _Interaction Vectors (IVs)_ . Thus, XMimic introduce three key designs to prioritize interaction learning: (1) _IV Imitation Rewards_ that incentivize relative body–object motion, enabling robust and generalizable interactions; (2) _IV-based Termination_ , which executes early termination [23] upon interaction failure, compelling the policy to prioritize interaction success under disturbances; and (3) _Interaction Perturbation_ , include perturbing the initialization of the robot-object state and applying random external forces to the robot and object during training, forcing the policy to adapt and generalize. Together, these components enables robust and generalizable interaction skill from a single reference demonstration. This learning capability is further strengthened by XGen’s data augmentation, achieves generalization far beyond the original video. 

We evaluate HumanX on 9 diverse loco-manipulation and interaction skills—spanning basketball, football, badminton, cargo handling, and robot-human fighting—on a Unitree G1 humanoid. The system demonstrates two practical deployment ways: (1) Without any explicit external sensing, it executes basketball skills including dribbling, layups, and complex pump-fake turnaround fadeaways, with an average success rate over 80%. (2) With object sensing from a MoCap system, it achieves sustained closed-loop interactions, including over 10 consecutive human-robot basketball passes and football kicks, along with reliable pickup of randomly placed objects. Notably, each skill is learned from a single video demonstration, highlighting the strong generalization capability of our approach. Beyond mimicry, the policies exhibit adaptive behaviors: if a human removes a carried object and sets it down, the robot autonomously walks to and regrasps it —demonstrating real-time reaction rather than fixed motion replay. Quantitatively, HumanX achieves significantly higher generalization success than existing methods, establishing a scalable pathway within a class of anchorable interactions for acquiring versatile interactive skills from human videos. 

## **2 Related Work** 

**Data Acquisition for Humanoid Loco-Manipulation** Retargeting human motion to humanoids for robot learning has shown significant promise for agile, dynamic skills [24, 25, 26, 27, 28, 29, 30, 31, 32, 19, 33, 34]. For instance, SFV [35] estimates human pose from monocular video and enables simulated humanoids to perform complex acrobatics. SkillMimic [36, 16] estimates both human and object motion from video to train diverse basketball skills in simulation. VideoMimic [37] estimates human-scene interaction data from video and enables real-world humanoid-scene interaction through imitation. Meanwhile, GMR [38] provides a general motion retargeting framework that maps human motion to various robot morphologies. Several recent methods explores retargeting human-object or human-scene interaction data to train loco-manipulation policies [22, 39, 7]. However, these methods either rely on high-quality human-object interaction (HOI) data for retargeting [22], or they are struggle to reconstruct physically plausible interactions from monocular video due to severe occlusion and depth ambiguity [39]. Furthermore, these methods suffer from limited scalability, making it difficult to collect robot interaction data that adequately covers the distribution required for learning generalizable interaction skills. In contrast, our framework overcomes these limitations by shifting the interaction data acquisition paradigm from reconstruction to synthesis. This paradigm shift not only acquires physically plausible interaction data but also supports data augmentation, enabling strong generalization when combined with our training framework. 

**Reinforcement Learning for Humanoid Robots** Reinforcement learning (RL) in physics simulation has emerged as a key paradigm for whole-body humanoid control [24, 25, 40, 28, 41, 6, 42, 43, 44, 45, 30, 46, 47]. Early RL approaches for humanoids largely focused on gait learning, typically requiring carefully designed task-specific reward functions [48, 49, 50, 51]. This reward-engineering paradigm has also proven effective for a variety of other tasks, such as getting up [6, 52], goalkeeping [53], box carrying [54, 7], and pick-and-place [17, 18]. Inspired by the success of imitation learning in character animation [23, 55, 56, 57], retargeting human motion to humanoids and applying imitation rewards has enabled robots to acquire diverse locomotion skills—such as parkour [58, 59], martial arts [32], jumping [24, 60], and even generalizable whole-body motion tracking [34, 33, 61, 62, 27, 26]—through unified imitation rewards. Extending this imitation-based paradigm to interaction has seen initial progress in simulation [16, 36, 63, 64]. Recent research has explored imitation learning to equip real humanoid robots with interaction skills [39, 22]. However, these methods typically imitate isolated object and body motions, causing the policy to easily overfit to isolated body motion patterns, which reduces interaction generalization and robustness. In contrast, our reward function and training mechanism are designed based on the interaction-first principle, achieving interaction performance far exceeding that of concurrent works. 

## **3 XGen** 

XGen is an anchor-centric data synthesis pipeline that generates physically plausible anchorable interactions from human demonstration videos. As illustrated in Fig. 2, it converts monocular human video into humanoid motion and synthesizes interaction based on anchor-object configuration and physical simulation. The pipeline further supports augmentation of object mesh, size, and trajectory to produce large-scale, diversified interaction data. 

**Extracting Humanoid Motion from Human Video** Given a monocular RGB video with _K_ frames, we first obtains an initial estimation of the 3D human pose sequence using off-the-shelf tools [11]. The estimated 3D human pose in the _i_ -th frame is defined as **h** _i_ = ( **h**<sup>root</sup> _i ,_ **h**<sup>joint</sup> _i_ ), where _i_ = 1 _, . . . , K_ . **h**<sup>root</sup> _i ∈_ R<sup>6</sup> represents the 6D pose (3D position and 3D orientation) of the human root, and **h**<sup>joint</sup> _i ∈_ R<sup>_J×_3</sup> denotes the 3D rotations of _J_ SMPL [10] joints. Subsequently, we use GMR [38] to retarget the human pose sequence into a pose sequence of the target humanoid robot, which involves three core steps: keypoint alignment, skeleton scaling, and IK-based optimization. After retargeting, the robot pose sequence is denoted as **r** _i_ = ( **r**<sup>root</sup> _i ,_ **r**<sup>joint</sup> _i_ ), where _i_ = 1 _, . . . , K_ . **r**<sup>root</sup> _i ∈_ R<sup>6</sup> is the 6D root pose, and **r**<sup>joint</sup> _i ∈_ R<sup>_N×_1</sup> represents the 1D rotations of _N_ joints. 

**Synthesizing Interaction via Anchor-Object Configuration** We segment the data into contact and non-contact phases. As illustrated in Fig. 2, taking the example of box carrying, we annotate the 


Figure 2: Overview of **XGen** . The pipeline begins by estimating SMPL-based human motion from video and retargeting it to the humanoid’s morphology. The video is segmented into **contact** and **non-contact** phases. For the contact phase, a body anchor (e.g., the midpoint between the two palms) is predefined. The object trajectory is then synthesized by transforming the object according to the anchor, followed by contact optimization to refine the robot poses. During the non-contact phases, diverse object trajectories are generated via physical simulation. Complete interaction trajectories are obtained by concatenating and smoothly interpolating the phases. 


Figure 3: Data Augmentation for The Contact Phase. 


Figure 4: Aug for Non-Contact Phases. 

video frames into: a non-contact phase before contact begins ( _t < ts_ ), a contact phase ( _ts ≤ t ≤ te_ ), and a final non-contact phase after contact ends ( _t > te_ ). 

For the contact phase, we consider the relative motion between a predefined body anchor and the object as the core of an interaction. This representation exhibits favorable cross-embodiment properties, meaning the same anchor-object relationship can be transferred across different morphologies (e.g., from human to humanoid) while preserving interaction semantics. We primarily discuss two types of anchor definitions: (1) Using the midpoint between the two palms as the anchor, suitable for contact phases where the object is stably held with both hands, such as box carrying, shooting, and layups. (2) Using a specific body part as the anchor, suitable for contact phases involving a single-point interaction, such as hitting a shuttlecock or kicking a football ball. 

Once the anchor is defined, we can estimate the object’s mesh and its rotation _ϕ_ relative to the anchor at time _ts_ from the video frame **v** _ts_ using SAM-3D [12]. Alternatively, the mesh and the initial anchor-object configuration can be manually defined, which also allows synthesizing interactions from videos where the object is not visibly present. The anchor’s trajectory is then derived from the robot motion sequence _{_ **r** _i}_ , and the corresponding object trajectory is obtained by preserving the relative transformation _ϕ_ throughout the anchor’s motion. To improve physical plausibility, the robot motion can be optimized under contact and force-closure objectives [65, 66, 67], yielding refined robot poses ˆ **r** _t_ and corresponding object poses **p** _t_ for each frame in the contact phase. 

In the non-contact phase, object trajectories are synthesized using a physics simulator [68]. Specifically: (1) After contact ends ( _t > te_ ), the object is initialized in simulation with pose **p** _te_ and a predefined initial velocity, and its trajectory is recorded under simulation. This applies to actions such as basketball shooting, football kicking, or object placement. (2) Before contact begins ( _t < ts_ ), —e.g., when catching a ball—we reverse the process: starting from **p** _ts_ , we simulate the object backward in time and then reverse the sequence to obtain the pre-contact trajectory. This allows accurate synthesis of motions such as a parabolic ball path into the hands. To ensure physical plausibility in the reversed simulation, object damping coefficients are inverted. 


Figure 5: **XMimic** is a unified framework for learning diverse interaction skills. To reinforce interaction and prevent overfitting to isolated body motions, it employs rewards that prioritize interaction and introduces interaction perturbations and interaction-vector termination during simulation. The training follows a two-stage pipeline: a privileged teacher policy first learns the skill using full state information, which then guides the training of a deployable student policy. 

**Interaction Augmentation** XGen supports data augmentation along multiple dimensions to increase the interaction diversity and data coverage: (1) We apply scaling to the object mesh or replace it with a different geometry during the mesh acquisition stage. The subsequent XGen synthesis process ensures that interactions remain physically plausible with the scaled or substituted object. This allows generating data for performing similar actions on different objects from a single demonstration video, as shown in Fig. 3. (2) The object trajectory within the contact phase can be augmented by applying simple geometric transformations—such as translation and scaling. The subsequent XGen pipeline ensures the physical plausibility of the interaction after augmentation. For example, from a single video demonstration of lifting a box, XGen can generate training data for lifting the same box from different heights, as illustrated in Fig. 3. (3) We enrich the diversity of object trajectories in the non-contact phase by introducing parametric randomization to the object’s initial velocity in the physics simulation. For instance, from one demonstration of hitting a shuttlecock, XGen can produce data for hitting with different parabolic trajectories. Similarly, a single basketball shooting video can yield training data for making shots from various distances, as shown in Fig. 4. 

## **4 XMimic** 

XMimic is a interaction-prioritized imitation learning framework that enables humanoids to acquire diverse interaction skills from humanoid-object interaction data. Fig. 5 provides an overview. 

**Teacher-Student Training Architecture** Our training process follows a two-stage teacher-student paradigm that first master individual skills with privilege information and then consolidate them into a unified deployable policy. Given the observation **_s_** _t_ as input, the policy output is parameterized as a Gaussian distribution **_π_** ( **_a_** _t |_ **_s_** _t_ ) _∼N_ ( **_ϕπ_** ( **_s_** _t_ ) _,_ **Σ** **_π_** ), where **_ϕπ_** is a MLP that predicts mean of the action distribution. The covariance matrix **Σ** **_π_** is learnable. The resulting action **_a_** _t ∈_ R<sup>_n_</sup> (where _n_ is the number of robot DoFs) is then transformed into joint torques via a PD controller. Given _n_ skill patterns and their corresponding datasets _{D_ 1 _, . . . , Dn}_ generated by XGen, we train a teacher policy _π_ tea<sup>_i_oneachdataset</sup><sup>_Di_.The training procedure for a single teacher is as follows.</sup> A trajectory clip is sampled from its dedicated dataset, and the humanoid along with objects are initialized according to the first frame of the clip. At each timestep _t_ , the policy receives a privileged state observation **_s_** _t_ = _{_ **_o_** _t,_ **_o_**<sup>_priv_</sup> _t ,_ **_s_**<sup>_ext_</sup> _t }_ , which comprises proprioception **_o_** _t_ , privileged body information **_o_**<sup>_priv_</sup> _t_ , and object state **_s_**<sup>_ext_</sup> _t_ . The policy then samples an action **_a_** _t_ , which is executed in the physics simulator. Subsequently, the reward _rt_ is computed. The network parameters **_ϕπ_** of the teacher policy are optimized using PPO [69] to maximize the expected cumulative reward. 

The student policy is trained on the combined dataset _D_ =<sup>�</sup> _i_<sup>_Di_followingsimilarprocedureto</sup> the teacher, with proprioception and optional object observations. The training objective is extended to combine the RL rewards with a behavior cloning loss that distills the pre-trained teachers. An asymmetric Actor-Critic setting [70] is applied to further provide privileged guidance for the student. 

**Interaction-Prioritized Imitation Learning** The essence of imitating an interaction skill lies not in replicating isolated body movements, but in learning relative body-object interaction patterns that are robust to perturbations. We capture this relational structure via Interaction Vectors (IVs). By imitating IVs from reference data and using IV tracking error to trigger early termination [23], our approach significantly enhances the robustness and generalization of learned interactions. Concretely, we augment the anchor body with additional tracking points—such as the fingertips or the 

Table 1: **Main Simulation Results** . SR, _Eo_ , and _Eh_ measure the success rate on the original data, the object position tracking error, and the key-body position tracking error, respectively, while GSR measures the success rate of skill generalization. 

|Method||_Basket_|_ball Catch-Sh_|_ot_||_Badm_|_inton Hitting_|||_Ca_|_rgo Pickup_|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||SR<sup>_↑_</sup>|GSR<sup>_↑_</sup>|_Eo_<br>_↓_(m)|_Eh_<br>_↓_(cm)|SR<sup>_↑_</sup>|GSR<sup>_↑_</sup>|_Eo_<br>_↓_(m)|_Eh_<br>_↓_(m)|SR<sup>_↑_</sup>|GSR<sup>_↑_</sup>|_Eo_<br>_↓_(cm)|_Eh_<br>_↓_|(cm)|
|SkillMimic [36]|0.0%|0.0%|1.25 (_±_0.26)|10.3 (_±_1.37)|68.2%|30.9%|2.94 (_±_0.91)|0.48 (_±_0.13)|0.4%|0.0%|25.1 (_±_0.06)|28.3 (|_±_2.13)|
|OmniRetarget [22]|0.0%|0.0%|1.18 (_±_0.15)|7.83 (_±_0.95)|75.8%|20.4%|1.25 (_±_1.15)|0.15 (_±_0.10)|0.0%|0.0%|10.8 (_±_0.00)|13.3 (|_±_1.57)|
|<br>HDMI [39]|53.1%|2.4%|0.70 (_±_0.11)|10.8 (_±_2.41)|90.0%|25.3%|1.64 (_±_0.66)|0.07 (_±_0.02)|95.8%|1.8%|1.79 (_±_0.22)|13.1 (|_±_1.28)|
|XMimic (Base)|93.4%|4.9%|0.69 (_±_0.14)|6.36 (_±_1.51)|97.1%|41.6%|1.32 (_±_0.44)|0.12 (_±_0.07)|100%|50.9%|1.56 (_±_0.30)|6.58 (|_±_0.76)|
|+ IP|86.8%|13.5%|0.70 (_±_0.08)|7.46 (_±_0.46)|94.0%|60.5%|1.03 (_±_0.57)|0.10 (_±_0.05)|100%|94.5%|1.62 (_±_0.03)|10.5 (|_±_1.23)|
|+ IVT|93.4%|10.9%|0.83 (_±_0.09)|6.97 (_±_0.38)|100%|67.2%|1.33 (_±_0.67)|0.10 (_±_0.06)|99.6%|94.3%|1.51 (_±_0.29)|9.62 (|_±_1.13)|
|+ Data Aug|77.6%|60.6%|0.76 (_±_0.11)|8.34 (_±_0.91)|100%|84.4%|0.98 (_±_0.65)|0.10 (_±_0.05)|/|/|/|/||
|+ Tea-Stu|86.8%|64.7%|0.85 (_±_0.10)|7.83 (_±_0.95)|100%|90.6%|0.90 (_±_0.46)|0.09 (_±_0.06)|99.3%|96.3%|1.38 (_±_0.25)|8.67 (|_±_0.91)|


Figure 6: **Simulation Results on Basketball Catch-Shot** . XMimic generalizes to novel ball-passing trajectories and target positions (green sphere) with natural interactions. 


Figure 7: **Visualization of Generalization Performance in Simulation** . With HumanX, skills learned from only **one video** generalize to unseen object positions, trajectories, and goals. 

edge points of a racket—which, together with standard body keypoints, form an extended set of body points. The vectors from these points to the object’s center are defined as the Interaction Vectors (IVs). Interaction quality is measured by the consistency between the IVs in reference data and those in simulation. Thanks to their relative nature, IVs provide dense, fine-grained guidance even under perturbation, whereas isolated object or body tracking rewards may fail in such cases. The complete reward function combines the IV imitation reward with isolated body/object tracking rewards, a contact reward, and regularization terms. We further employ IV error to detect interaction failure and trigger early termination, which we term IV-based Termination (IVT). IVT helps prevent the policy from overfitting to isolated body imitation. We apply IVT probabilistically to provide a tradeoff from strict to lenient. To further improve robustness and generalization, we introduce a set of Interaction Perturbations (IP) during training, including: (1) perturbations to the robot’s root pose, joint angles, and object pose at episode initialization, and (2) applying random external forces to the object (only during contact phases) and to the robot. Through the combined use of IV reward and IVT, the policy learns to compensate for these perturbations, achieving strong interaction performance that generalizes beyond the original demonstration. 

**Flexible Perception Schemes for Deployment** XMimic supports two deployment schemes: (1) _No External Perception (NEP) mode_ , where object observations are removed during the student training, enabling the robot to rely solely on proprioception for dynamic interaction. This mode supports skills such as shooting, layups, dribbling, and complex maneuvers like pump-fake turnaround jumpshots. (2) _MoCap mode_ , where the object observations are provided by a MoCap system. However, object tracking via MoCap often suffers from intermittent frame loss due to occlusion. To address this, we simulates frame loss of the object observations during the student training. This enables zero-shot adaptation to real-world MoCap streams with intermittent data loss. 

## **5 Experiments** 

**Experimental Settings** Video clips for XGen was captured using an iPhone 16. All training and simulation were conducted on the Isaac Gym platform [68] using a single NVIDIA RTX 4090 GPU with 16,384 parallel environments. Each policy was trained for 20,000 iterations unless otherwise specified. Deployment was performed on a Unitree G1 humanoid robot. For MoCap-based experiments, we employed a Noitom optical motion capture system within a 5×5×2.6m space, using 14 cameras. The policy and mocap systems ran at 100 Hz, while the PD controller operated at 1 kHz. 

**Simulation Evaluation and Ablation Study** We conduct simulation experiments on three representative interaction tasks: (1) _Basketball Catch-Shot_ : catching a passed basketball and shooting it into a target hoop. Success is defined as the shot landing within 20 cm of the target hoop cen- 


Figure 8: **Real Robot Experiment on Blind Basketball Skills** . The policy relies solely on proprioception to control objects, achieving diverse, highly dynamic, and complex interactions. 


Figure 9: **Real Robot Experiment on MoCap-based Interaction Skills** . When utilizing MoCap system to perceive object or human motion, our method enables sustained interaction, demonstrating high precision, agility, robustness, and generalization capability. Notably, each task shown here is learned from a single demonstration video without any task-specific reward. 

ter. (2) _Badminton Hitting_ : striking a flying shuttlecock, with success measured by the hitting rate. (3) _Cargo Pickup_ : walking to and lifting a randomly placed cargo. Success requires the lifted cargo to reach within 10 cm of the target height. We perform a series of ablation studies on our method, starting from our baseline (XMimic Base), and incrementally add: interaction perturbation (+IP), interaction-vector termination (+IVT), XGen data augmentation (+Data Aug), and the teacher-student scheme (+Tea-Stu). For comparison, we also evaluate on prior and concurrent imitation methods including SkillMimic [36], OmniRetarget [22], and HDMI [39]. For each task, a single video is processed by XGen to generate one training clip. In the “+Data Aug” and “+Tea-Stu” settings, this clip is augmented by XGen to produce 50 interaction clips for training. 

We report four metrics: object-position error ( _Eo_ ), key-body-position error ( _Eh_ ), success rate (SR) on the original demonstration, and generalization SR beyond the original demonstration (GSR). Quantitative results are summarized in Tab. 1. The multiplicative reward of SkillMimic is difficult to balance with regularization terms, leading to suboptimal performance. OmniRetarget simply sums the object and body tracking rewards, which biases the policy towards replicating isolated body motion patterns and yields weak interaction. HDMI incorporates an additional contact reward, thereby improving its ability to fit a single demonstration, but it suffers from poor generalization due to overfitting. In contrast, XMimic (Base) yields superior interaction performance over these methods, validating the effectiveness of our Interaction-Vector reward. Subsequent ablation studies highlight significant gains in GSR, with our final model exceeding 80% average GSR—approximately 8× higher than HDMI, further demonstrating the efficacy of XMimic’s overall interaction-centric de- 

Table 2: **<u>Quantitative Results on Real Robot Experiments</u>** . 

|_Basketball Catch-Pass_(MoCap)|41 / 50|_Reactive Fighting_(MoCap)|37 / 50|_Jumpshot_(NEP)|8 / 10|
|---|---|---|---|---|---|
|_Cargo Pickup_(MoCap)|43 / 50|_Dribble_(NEP)|8 / 10|_Basketball Pickup_(NEP)|10 / 10|
|_Football Kicking_(MoCap)|42 / 50|_Pump-fake_(NEP)|9 / 10|_Layup_(NEP)|7 / 10|


Figure 10: **Adaptive Behaviors** . During the execution of the Cargo Pickup skill, a researcher first kicks the robot forcefully, then takes the object from its hand and places it on the ground. The robot shows robust adaptation in response to such complex disturbances. 


Figure 11: **Sim-to-Real Analysis** . ( **_Left_** ) If the training does not include Interaction Perturbation, the robot may lose balance during highly dynamic interactions. ( **_Right_** ) Without simulating MoCap signal loss during training, the robot may collapse when the object signal is lost during deployment. 

sign. Fig. 6 illustrates simulated executions of our generalized _Basketball Catch-Shot_ skill. Fig. 7 visualizes the generalization ranges for each skill. Notably, this strong generalization capability is learned from only a single demonstration video per skill. 

**Real Robot Experiments** We evaluate real-world deployment under two perception schemes: _NEP mode_ and _MoCap mode_ . Each skill is trained based on a single human video. 

_NEP Mode._ We test five basketball skills in NEP mode: _Jumpshot_ , _Dribble_ , _Pickup_ , _Layup_ , and _Pump-fake turnaround fadeaway_ . Each skill starts with the ball in hand (or on the floor for Pickup). A trial is successful if the robot completes the entire sequence without dropping the ball and remains balanced. Over 10 trials per skill (Tab. 2), the policy achieves high success rates, demonstrating reliable proprioceptive control for diverse interaction behaviors (Fig. 8). 

_MoCap Mode._ We evaluate four interactive tasks using MoCap: _Cargo Pickup_ , sustained _Basketball Catch-and-Pass_ and _Football Kicking_ with a human partner, and _Reactive Fighting_ (blocking and countering human punches). Success rates over 50 trials per skill are reported in Tab. 2. Our method enables prolonged, closed-loop interaction. For instance, in basketball, the robot can execute over 10 consecutive successful catch-and-pass cycles with a human partner, maintaining stability even if the ball is dropped and seamlessly resuming when the ball is returned. Similarly, in football, it achieves over 14 consecutive successful return kicks despite variability in human passes. This consistent performance under human-induced uncertainty strongly evidences the policy’s generalization capability. The results visualized in Fig. 9 and Fig. 10 demonstrate that the acquired skills extend far beyond simple mimicry. They show adaptive closed-loop execution, robustness to perturbations, and the ability to generalize within interactive scenarios, validating the effectiveness of our HumanX system. Finally, Fig. 11 illustrates two key factors critical for deployment stability. 

## **6 Conclusion, Limitation, and Future Extension** 

This paper presents HumanX, a full-stack framework that compiles monocular human video into agile and generalizable humanoid interaction skills. With HumanX, we demonstrate a range of interactive capabilities that are difficult to achieve with prior methods. Nevertheless, the framework still has several limitations. First, while XGen is effective for synthesizing tasks involving stable grasps and point-contact interactions—which constitute a large portion of practical manipulation—it does not yet support in-hand reorientation motions. Second, due to limits in data reconstruction and simulation techniques, our method cannot currently handle interactions with deformable or cuttable objects, such as dumpling wrapping, apple peeling, or garment dressing. Third, our implementation does not employ dexterous hands, though integrating mature hand-object grasp synthesis techniques [71, 72] with XGen’s anchor-centered pipeline is a promising direction. Beyond data synthesis, the current motion-capture-based perception system struggles to perceive diverse objects and is costly to deploy. In the future, we plan to investigate egocentric visual perception, which will help scaling a single policy to acquire a wide range of interaction skills with cross-object generalization. 

### **Acknowledgments** 

We sincerely thank Weishuai Zeng, Tao Huang, Feiyu Jia, Huayi Wang, Xiao Chen, Junli Ren, and Wenjun Liu for their help, discussions, and support throughout the experiments. We also express our gratitude to Unitree Robotics for providing technical support on the robot, and to Noitom Robotics for their technical assistance with the motion capture equipment. This work was supported by the HKUST-BYD Joint Laboratory and Shanghai Artificial Intelligence Laboratory. 

## **References** 

- [1] Z. Fu, Q. Zhao, Q. Wu, G. Wetzstein, and C. Finn. Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ , 2024. 

- [2] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [3] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang. Open-television: Teleoperation with immersive active visual feedback. In _Conference on Robot Learning_ , pages 2729–2749. PMLR, 2025. 

- [4] T. Haarnoja, B. Moran, G. Lever, S. H. Huang, D. Tirumala, M. Wulfmeier, J. Humplik, S. Tunyasuvunakool, N. Siegel, R. Hafner, M. Bloesch, K. Hartikainen, A. Byravan, L. Hasenclever, Y. Tassa, F. Sadeghi, N. Batchelor, F. Casarini, S. Saliceti, C. Game, N. Sreendra, K. Patel, M. Gwira, A. Huber, N. Hurley, F. Nori, R. Hadsell, and N. M. O. Heess. Learning agile soccer skills for a bipedal robot with deep reinforcement learning. _Science Robotics_ , 9, 2023. 

- [5] Y. Ma, A. Cramariuc, F. Farshidian, and M. Hutter. Learning coordinated badminton skills for legged manipulators. _Science robotics_ , 10 102:eadu3922, 2025. 

- [6] X. He, R. Dong, Z. Chen, and S. Gupta. Learning getting-up policies for real-world humanoid robots. _ArXiv_ , abs/2502.12152, 2025. 

- [7] H. Wang, W. Zhang, R. Yu, T. Huang, J. Ren, F. Jia, Z. Wang, X. Niu, X. Chen, J. Chen, et al. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [8] H. Zhang, Y. Yuan, V. Makoviychuk, Y. Guo, S. Fidler, X. B. Peng, and K. Fatahalian. Learning physically simulated tennis skills from broadcast videos. _ACM Trans. Graph._ , 2023. doi: 10.1145/3592408. 

- [9] P. Xu, Z. Wu, R. Wang, V. Sarukkai, K. Fatahalian, I. Karamouzas, V. B. Zordan, and C. K. Liu. Learning to ball: Composing policies for long-horizon basketball moves. _ACM Transactions on Graphics (TOG)_ , 44:1 – 14, 2025. 

- [10] M. Loper, N. Mahmood, J. Romero, G. Pons-Moll, and M. J. Black. Smpl: A skinned multiperson linear model. _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , 2023. 

- [11] Z. Shen, H. Pi, Y. Xia, Z. Cen, S. Peng, Z. Hu, H. Bao, R. Hu, and X. Zhou. World-grounded human motion recovery via gravity-view coordinates. In _SIGGRAPH Asia Conference Proceedings_ , 2024. 

- [12] X. Chen, F.-J. Chu, P. Gleize, K. J. Liang, A. Sax, H. Tang, W. Wang, M. Guo, T. Hardin, X. Li, et al. Sam 3d: 3dfy anything in images. _arXiv preprint arXiv:2511.16624_ , 2025. 

- [13] B. Wen, W. Yang, J. Kautz, and S. T. Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 17868–17879, 2023. 

- [14] J. Sun, Z. Wang, S. Zhang, X. H. He, H. Zhao, G. Zhang, and X. Zhou. Onepose: One-shot object pose estimation without cad models. _2022 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 6815–6824, 2022. 

- [15] Y. Hasson, G. Varol, D. Tzionas, I. Kalevatykh, M. J. Black, I. Laptev, and C. Schmid. Learning joint reconstruction of hands and manipulated objects. _2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 11799–11808, 2019. 

- [16] Y. Wang, J. Lin, A. Zeng, Z. Luo, J. Zhang, and L. Zhang. Physhoi: Physics-based imitation of dynamic human-object interaction. _arXiv preprint arXiv:2312.04393_ , 2023. 

- [17] T. He, Z. Wang, H. Xue, Q. Ben, Z. Luo, W. Xiao, Y. Yuan, X. Da, F. Casta˜neda, S. Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 

- [18] D. Kalaria, S. S. Harithas, P. Katara, S. Kwak, S. Bhagat, S. Sastry, S. Sridhar, S. Vemprala, A. Kapoor, and J. C.-K. Huang. Dreamcontrol: Human-inspired whole-body humanoid control for scene interaction via guided diffusion. _arXiv preprint arXiv:2509.14353_ , 2025. 

- [19] Z. Su, B. Zhang, N. Rahmanian, Y. Gao, Q. Liao, C. Regan, K. Sreenath, and S. S. Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [20] H. Xue, T. He, Z. Wang, Q. Ben, W. Xiao, Z. Luo, X. Da, F. Casta˜neda, G. Shi, S. Sastry, et al. Opening the sim-to-real door for humanoid pixel-to-action policy transfer. _arXiv preprint arXiv:2512.01061_ , 2025. 

- [21] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [22] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [23] X. B. Peng, P. Abbeel, S. Levine, and M. van de Panne. Deepmimic. _ACM Transactions on Graphics_ , page 1–14, Aug 2018. doi:10.1145/3197517.3201311. 

- [24] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, et al. Asap: Aligning simulation and real-world physics for learning agile humanoid wholebody skills. _arXiv preprint arXiv:2502.01143_ , 2025. 

- [25] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024. 

- [26] Y. Pan, R. Qiao, L. Chen, K. Chitta, L. Pan, H. Mai, Q. Bu, H. Zhao, C. Zheng, P. Luo, et al. Agility meets stability: Versatile humanoid control with heterogeneous data. _arXiv preprint arXiv:2511.17373_ , 2025. 

- [27] Y. Li, Y. Lin, J. Cui, T. Liu, W. Liang, Y. Zhu, and S. Huang. Clone: Closed-loop whole-body humanoid teleoperation for long-horizon tasks. _arXiv preprint arXiv:2506.08931_ , 2025. 

- [28] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [29] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, et al. Track any motions under any disturbances. _arXiv preprint arXiv:2509.13833_ , 2025. 

- [30] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang. Expressive whole-body control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- [31] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- [32] W. Xie, J. Han, J. Zheng, H. Li, X. Liu, J. Shi, W. Zhang, C. Bai, and X. Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _Advances in Neural Information Processing Systems_ , 38:62406–62433, 2026. 

- [33] W. Zeng, S. Lu, K. Yin, X. Niu, M. Dai, J. Wang, and J. Pang. Behavior foundation model for humanoid robots. _arXiv preprint arXiv:2509.13780_ , 2025. 

- [34] K. Yin, W. Zeng, K. Fan, M. Dai, Z. Wang, Q. Zhang, Z. Tian, J. Wang, J. Pang, and W. Zhang. Unitracker: Learning universal whole-body motion tracker for humanoid robots. _arXiv preprint arXiv:2507.07356_ , 2025. 

- [35] X. B. Peng, A. Kanazawa, J. Malik, P. Abbeel, and S. Levine. Sfv: Reinforcement learning of physical skills from videos. _ACM Transactions On Graphics (TOG)_ , 37(6):1–14, 2018. 

- [36] Y. Wang, Q. Zhao, R. Yu, H. W. Tsui, A. Zeng, J. Lin, Z. Luo, J. Yu, X. Li, Q. Chen, et al. Skillmimic: Learning basketball interaction skills from demonstrations. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17540–17549, 2025. 

- [37] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [38] J. P. Araujo, Y. Ze, P. Xu, J. Wu, and C. K. Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [39] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [40] Y. Li, Y. Zhang, W. Xiao, C. Pan, H. Weng, G. He, T. He, and G. Shi. Hold my beer: Learning gentle humanoid locomotion and end-effector stabilization control. In _RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 

- [41] J. Li, X. Cheng, T. Huang, S. Yang, R.-Z. Qiu, and X. Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _arXiv preprint arXiv:2505.03738_ , 2025. 

- [42] Y. Shao, X. Huang, B. Zhang, Q. Liao, Y. Gao, Y. Chi, Z. Li, S. Shao, and K. Sreenath. Langwbc: Language-directed humanoid whole-body control via end-to-end learning. _ArXiv_ , abs/2504.21738, 2025. 

- [43] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang. A unified and general humanoid whole-body controller for fine-grained locomotion. _ArXiv_ , abs/2502.03206, 2025. 

- [44] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. _ArXiv_ , abs/2502.10363, 2025. 

- [45] Q. Ben, F. Jia, J. Zeng, J. Dong, D. Lin, and J. Pang. Homie: Humanoid loco-manipulation with isomorphic exoskeleton cockpit. _ArXiv_ , abs/2502.13013, 2025. 

- [46] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati, et al. Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning. _arXiv preprint arXiv:2511.04131_ , 2025. 

- [47] I. Radosavovic, B. Zhang, B. Shi, J. Rajasegaran, S. Kamat, T. Darrell, K. Sreenath, and J. Malik. Humanoid locomotion as next token prediction. _Advances in neural information processing systems_ , 37:79307–79324, 2024. 

- [48] R. Tedrake, T. W. Zhang, and H. S. Seung. Stochastic policy gradient reinforcement learning on a simple 3d biped. In _2004 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)(IEEE Cat. No. 04CH37566)_ , volume 3, pages 2849–2854. IEEE, 2004. 

- [49] N. Heess, D. Tb, S. Sriram, J. Lemmon, J. Merel, G. Wayne, Y. Tassa, T. Erez, Z. Wang, S. Eslami, et al. Emergence of locomotion behaviours in rich environments. _arXiv preprint arXiv:1707.02286_ , 2017. 

- [50] Z. Li, X. Cheng, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath. Reinforcement learning for robust parameterized locomotion control of bipedal robots. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 2811–2817. IEEE, 2021. 

- [51] Z. Li, X. B. Peng, P. Abbeel, S. Levine, G. Berseth, and K. Sreenath. Reinforcement learning for versatile, dynamic, and robust bipedal locomotion control. _The International Journal of Robotics Research_ , 44(5):840–888, 2025. 

- [52] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang. Learning humanoid standing-up control across diverse postures. _ArXiv_ , abs/2502.08378, 2025. 

- [53] J. Ren, J. Long, T. Huang, H. Wang, Z. Wang, F. Jia, W. Zhang, J. Wang, P. Luo, and J. Pang. Humanoid goalkeeper: Learning from position conditioned task-motion constraints. _arXiv preprint arXiv:2510.18002_ , 2025. 

- [54] J. Dao, H. Duan, and A. Fern. Sim-to-real learning for humanoid box loco-manipulation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 16930– 16936. IEEE, 2024. 

- [55] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa. Amp: Adversarial motion priors for stylized physics-based character control. _ACM Transactions on Graphics_ , page 1–20, Aug 2021. doi:10.1145/3450626.3459670. 

- [56] Z. Luo, J. Cao, K. Kitani, W. Xu, et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 10895–10904, 2023. 

- [57] P. Xu, X. Shang, V. Zordan, and I. Karamouzas. Composite motion learning with task control. _ACM Transactions on Graphics (TOG)_ , 42(4):1–16, 2023. 

- [58] Z. Zhuang, S. Yao, and H. Zhao. Humanoid parkour learning. _arXiv preprint arXiv:2406.10759_ , 2024. 

- [59] C. Zhang, W. Xiao, T. He, and G. Shi. Wococo: Learning whole-body humanoid control with sequential contacts. In _Conference on Robot Learning_ , pages 455–472. PMLR, 2025. 

- [60] T. Huang, H. Wang, J. Ren, K. Yin, Z. Wang, X. Chen, F. Jia, W. Zhang, J. Long, J. Wang, et al. Towards adaptable humanoid control via adaptive motion tracking. _arXiv preprint arXiv:2510.14454_ , 2025. 

- [61] Z. Chen, M. Ji, X. Cheng, X. Peng, X. B. Peng, and X. Wang. Gmt: General motion tracking for humanoid whole-body control. _arXiv preprint arXiv:2506.14770_ , 2025. 

- [62] Y. Ze, Z. Chen, J. P. Ara´ujo, Z.-a. Cao, X. B. Peng, J. Wu, and C. K. Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

- [63] S. Xu, H. Y. Ling, Y.-X. Wang, and L.-Y. Gui. Intermimic: Towards universal whole-body control for physics-based human-object interactions. _arXiv preprint arXiv:2502.20390_ , 2025. 

- [64] C. Tessler, Y. Jiang, E. Coumans, Z. Luo, G. Chechik, and X. B. Peng. Maskedmanipulator: Versatile whole-body control for loco-manipulation. _arXiv preprint arXiv:2505.19086_ , 2025. 

- [65] T. Liu, Z. Liu, Z. Jiao, Y. Zhu, and S.-C. Zhu. Synthesizing diverse and physically stable grasps with arbitrary hand structures using differentiable force closure estimator. _IEEE Robotics and Automation Letters_ , 7(1):470–477, 2021. 

- [66] R. Wang, J. Zhang, J. Chen, Y. Xu, P. Li, T. Liu, and H. Wang. Dexgraspnet: A largescale robotic dexterous grasp dataset for general objects based on simulation. _arXiv preprint arXiv:2210.02697_ , 2022. 

- [67] Y. Wang, R. Yu, H. W. Tsui, X. Lin, H. Zhang, Q. Zhao, K. Fan, M. Li, J. Song, J. Wang, Q. Chen, and P. Tan. Learning generalizable hand-object tracking from synthetic demonstrations. _arXiv preprint arXiv:2512.19583_ , 2025. 

- [68] V. Makoviychuk, L. Wawrzyniak, Y. Guo, M. Lu, K. Storey, M. Macklin, D. Hoeller, N. Rudin, A. Allshire, A. Handa, and G. State. Isaac gym: High performance GPU based physics simulation for robot learning. In _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ , 2021. 

- [69] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [70] L. Pinto, M. Andrychowicz, P. Welinder, W. Zaremba, and P. Abbeel. Asymmetric actor critic for image-based robot learning. _Robotics: Science and Systems XIV_ , 2018. 

- [71] R. Wang, J. Zhang, J. Chen, Y. Xu, P. Li, T. Liu, and H. Wang. Dexgraspnet: A large-scale robotic dexterous grasp dataset for general objects based on simulation. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11359–11366. IEEE, 2023. 

- [72] J. Chen, Y. Ke, L. Peng, and H. Wang. Dexonomy: Synthesizing all dexterous grasp types in a grasp taxonomy. _arXiv preprint arXiv:2504.18829_ , 2025. 

- [73] R. Yu, Y. Wang, Q. Zhao, H. W. Tsui, J. Wang, P. Tan, and Q. Chen. Skillmimic-v2: Learning robust and generalizable interaction skills from sparse and noisy demonstrations. In _Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers_ , pages 1–11, 2025. 

- [74] R. Featherstone. _Rigid body dynamics algorithms_ . Springer, 2008. 

- [75] R. M. Murray, Z. Li, and S. S. Sastry. _A mathematical introduction to robotic manipulation_ . CRC press, 2017. 

- [76] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 

- [77] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

Table 3: **Evaluation on Multi-Pattern Interaction Skills in Simulation** . Each skill contains three distinct interaction patterns from three human video. 

|**Method**|_Football Kicking_|_Badminton Hitting_|
|---|---|---|
|w/o Tea-Stu|74.2% GSR|52.4% GSR|
|w/ Tea-Stu|93.1% GSR|84.3% GSR|


Figure 12: **Diverse Skill Patterns** . XMimic supports learning multiple interaction patterns for a single skill, allowing the policy to autonomously select the most suitable pattern in response to object state. ( **_Left_** ): football-kicking patterns. ( **_Right_** ): badminton-hitting patterns. 

## **7 Appendix** 

### **7.1 Evaluation on Multi-Pattern Interaction Skills** 

To assess whether a single student policy can learn diverse skill patterns, we test on two representative tasks: _Football Kicking_ and _Badminton Hitting_ . For each task, three distinct human demonstration videos are processed by XGen and augmented for training. An ablation study confirms the critical role of the teacher-student scheme in this setting. Quantitative and qualitative results (Tab. 3 and Fig. 12) show that XMimic successfully learns multiple patterns, with the teacher-student framework yielding greater benefits in multi-pattern learning than in single-pattern scenarios. 

### **7.2 GSR Evaluation Setting** 

For evaluating the Generalization Success Rate (GSR), the test cases are sampled from a distribution beyond the original data. For Basketball Catch-and-Shot, the ball’s initial position is perturbed by ±0.3m (uniform distribution). This creates novel passing trajectories and requires shooting to a new target hoop location simultaneously. For Badminton Hitting, the shuttlecock’s initial position is perturbed by ±0.3m (uniform distribution). For Cargo Pickup, the object is randomly placed within a semicircular area of 3m radius in front of the robot’s initial orientation. 

### **7.3 Unified Reward for Natural, Robust, and Generalizable Interaction Imitation** 

We employ the following composite reward function across all experiments: 


where _rt_<sup>body</sup> is the body imitation reward, _rt_<sup>obj</sup> is the object imitation reward, _rt_<sup>ivencouragescor-</sup> rect relative motion between the body and the object, _rt_<sup>_c_isthecontactimitationreward,and</sup><sup>_r_</sup> _t_<sup>reg</sup> comprises several regularization terms to improve motion stability. Tab. 13 provides a summary. 


Figure 13: Observation and Reward Settings. _⋆_ denotes optional. 

|**Observati**|**ons**||**Reward**|**s**|
|---|---|---|---|---|
|**Curr Terms**|_π_tea|_π_stu|**Mimic Terms**|_π_tea&_π_stu|
|Base Ang Vel|✓|✓|Body Pos|✓|
|Gravity|✓|✓|Body Rot|✓|
|DoF Pos|✓|✓|Body Vel|✓|
|DoF Vel|✓|✓|Body Ang Vel|✓|
|Action|✓|✓|Body AMP|✓|
|PD Error|✓|✓|DoF Pos|✓|
|Ref Body Pos|✓||DoF Vel|✓|
|Delta Body Pos|✓||Interaction Vector|✓|
|Object Pos|✓|_⋆_|Object Pos|✓|
|Object Rot|_⋆_|_⋆_|Object Rot|_⋆_|
|Target Object Pos|_⋆_|_⋆_|Contact Graph|✓|
|Target Object Rot|_⋆_|_⋆_|**Reg Terms**||
|Skill Label||✓|Torque|✓|
|History|✓|✓|Action Rate|✓|
|**History Terms**|||Waist DoF|✓|
|Base Ang Vel|✓|✓|Feet Orientation|✓|
|Gravity|✓|✓|Feet Slippage|✓|
|DoF Pos|✓|✓|DoF Limit|✓|
|DoF Vel|✓|✓|Torque Limit|✓|
|Action|✓|✓|Termination|✓|


Figure 14: Domain Randomization Settings. 

|**Sustained External Force**||
|---|---|
|Interval Range|_U_(1_._0_,_2_._0)|
|Body Force Magnitude Range|_U_(_−_50_,_50)|
|Object Force Magnitude Range|_U_(_−_2_,_2)|
|**Velocity Perturbation**||
|Interval Range|_U_(1_._0_,_3_._0)|
|Velocity Magnitude Range|_U_(_−_0_._5_,_0_._5)|
|Angular Velocity Magnitude Range|_U_(_−_0_._5_,_0_._5)|
|**Physical Properties**||
|DoF Friction|_U_(0_._5_,_1_._25)|
|Base CoM Position|_U_(_−_0_._05_,_0_._05)|
|Default Joint DoF Offset|_U_(_−_0_._01_,_0_._01)|
|Link Mass|_U_(0_._9_,_1_._1)|
|P Gain|_U_(0_._9_,_1_._1)|
|D Gain|_U_(0_._9_,_1_._1)|
|Torque RFI|0_._1_×_Torque Limit|


These terms correspond to body position, body rotation, joint position (DoF), body linear velocity, body angular velocity, and joint velocity, respectively. The adversarial motion prior (AMP) reward [55] is effective in enhancing the smoothness and naturalness of the body motion. Each sub-reward except _rt_<sup>amp</sup> follows the general form: 


where _e_<sup>_α_</sup> _t_<sup>denotes the imitation error for modality</sup><sup>_α_at time</sup><sup>_t_,</sup><sup>_λα_and</sup><sup>_γα_are hyperparameter.</sup> 

**Object Motion Imitation Reward** The object reward ensures accurate tracking of the object’s state: 


where _rt_<sup>_op_</sup> and _rt_<sup>_or_</sup> (optional) are the object position and rotation imitation rewards, respectively. Both are computed using the formulation in Eq. (3). 

**Interaction-Vector Imitation Reward** The IV reward _rt_<sup>ivencourages correct relative interaction</sup> between robot and object. The IV error is computed as 


where **u** ˆ _t_ is the reference IVs, and **u** _t_ is the corresponding IVs from the simulation. Each vector in **u** _t_ is defined as **u**<sup>(</sup> _t_<sup>_k_)</sup> = **u**<sup>_k_</sup> _t_<sup>_−_</sup><sup>**u**</sup><sup>_o_</sup> _t_<sup>,with</sup><sup>**u**</sup><sup>_k_</sup> _t_<sup>being the 3D position of a body keypoint and</sup><sup>**u**</sup><sup>_o_</sup> _t_<sup>the</sup> object position. IV rewards deliver consistent interaction guidance even when the robot or the object deviates from the reference motion. For example, when learning from only a single ball-pickup demonstration, we wish the robot still succeed if the ball is deviated from the reference position. In such cases, global tracking rewards like _rt_<sup>body</sup> and _rt_<sup>obj</sup> offer limited guidance, while _rt_<sup>ivprovides</sup> a dense and effective learning signal. This capability is crucial for generalizing interactive skills beyond the training data. 

**Contact Imitation Reward** To enhance contact stability, we introduce a contact imitation reward. Our XGen pipeline annotates each frame with a contact label, indicating whether the object and key-bodies are in contact status. Inspired by prior works [16, 36, 73], we formulate the contact state as binary vectors **_s_**<sup>_cg_</sup> _t ∈{_ 0 _,_ 1 _}_<sup>_J_</sup> , where _J_ is the number of contact bodies (including objects), and a value of 1 indicates active contact. 

The contact reward is computed based on the discrepancy between the simulated contact state **_s_**<sup>_cg_</sup> _t_ and the reference contact state ˆ **_s_**<sup>_cg_</sup> _t_<sup>from the reference data.The contact error vector is defined as the</sup> element-wise absolute difference: 


The contact imitation reward is then given by an exponential of the weighted error: 


where _λ_<sup>_cg_</sup> _j_<sup>is a sensitivity weight for the</sup><sup>_j_-th contact edge.This formulation penalizes mismatches</sup> in the contact graph, ensuring the policy learns precise contact timing and location. 

### **7.4 Perceiving External Force from Proprioception** 

Even in the absence of visual input, humans can still effectively perform stable grasping, basketball shooting, and other interactive behaviors. This ability relies on the implicit perception of interaction states through tactile and force feedback. In the following, we conduct a theoretical analysis to demonstrate that a similar mechanism is also feasible for humanoid robots, identify the key variables that influence such perception, and accordingly guide the observation design. 

The equation of motion for a floating-base humanoid robot can be formulated as [74, 75]: 


where **_τ_** denotes the vector of commanded joint torques; **q** , **q** ˙ , and **q** ¨ are the joint positions, velocities, and accelerations, respectively; **M** is the mass matrix; **C** captures Coriolis and centrifugal terms; **G** is the gravity vector; **_τ_** _f_ accounts for joint friction; and **J** ext<sup>_⊤_</sup><sup>**F**extrepresents the joint-space</sup> projection of external contact forces **F** ext. Rearranging Eq. 8 yields 


which shows that the external forces on each joint can be estimated if corresponding parameters are available. In the context of training a whole-body control policy with RL, this implies that, in principle, a policy can possibly learn to implicitly perceive external forces—provided it is given access to the relevant observations—and thus achieve a better dynamic interaction with objects. Taking the Unitree G1 as an example, **q** and **q** ˙ are directly measurable, and **_τ_** is well approximated by the commanded torque **_τ_** cmd from the PD controller. Although the joint acceleration **q** ¨ is not directly available, we can implicitly provide coarse acceleration information by including a history of multiple frames of **q** ˙ in the observations. The remaining terms in Eq. 9 are approximately constant and therefore do not need to be provided to the policy. 

Based on these insights, the final observation components used in our policy are listed in Tab. 13; they account (either explicitly or implicitly) for all variables appearing in Eq. 9. 

### **7.5 Domain Randomization** 

As summarized in Fig. 14, we apply domain randomization (DR) to various physical properties [76], including object size, mass, and coefficient of restitution, as well as robot friction coefficients, center of mass offsets, and perception noise. Additionally, we apply sustained random external forces to the robot during training. These DR terms are particularly important for achieving robust deployment. 

### **7.6 Probabilistic Early Termination** 

To improve training efficiency, we employ early termination [77] when the simulation enters an undesirable state. In addition to the **Interaction Termination (IT)** described in the main text, we consider the following types of termination: Root Orientation Tracking Termination, Body Tracking Termination, Object Tracking Termination, and Motion End Termination. 

Similar to IT, all the above terminations (except for Motion End Termination) are implemented _probabilistically_ . This design ensures that the policy can, with a certain probability, continue training even when a termination condition is met. The purpose is to enhance deployment stability: because real-world execution cannot be terminated as in simulation, the agent may encounter states that would otherwise trigger termination. Allowing the policy to occasionally experience and learn from such states improves its robustness when deployed on physical hardware. 

### **7.7 PD Controller** 

The low-level joint motor control is realized by a PD controller that computes the desired joint torque _τj_ for each joint _j_ at each time step, formulated as: 


where _qj_<sup>ref</sup> and _qj_ are the target and measured joint positions for joint _j_ , respectively, and _q_ ˙ _j_ is the measured joint velocity. The proportional and derivative gains, _kp,j_ and _kd,j_ , are derived following previous work [28], formulated as: 


where _ω_ denotes the natural frequency, _ζ_ is the damping ratio, and _Ij_ = _kg,j_<sup>2</sup><sup>_I_rotor</sup><sup>_,j_representsthe</sup> reflected inertia of the joint. Here, _I_ rotor _,j_ is the rotor inertia and _kg,j_ is the gear ratio. We set _ζ_ = 2 and _ω_ = 10 Hz. 

The PD controller’s target position _qj_<sup>refis formulated as:</sup> 


where _qj_<sup>0and</sup><sup>_aj,t_represents the joint position offset and policy action for joint</sup><sup>_j_.The action scale</sup> _α_ is defined as: 


where _τj,_ max is the torque limit for joint _j_ . 

### **7.8 Simulating MoCap Signal Loss** 

In real-world motion capture systems, tracking object states during interactive tasks frequently suffers from packet loss. This loss manifests primarily in two modes: 

- A: the signal loss occur intermittently even under good exposure and favorable conditions 

- B: the signal loss becomes severe as the object moves close to the robot (e.g., near the hands or torso), significantly raising the missing rate. 

To improve deployment robustness, we simulate both packet-loss modes during training. At the start of each episode, a distance threshold is sampled uniformly from a predefined range. During execution, the distance between the object and the anchor (e.g., the robot’s hand center) is computed at every simulation step. If this distance falls below the sampled threshold, the episode operates under B mode; otherwise, it follows A mode. 

Each mode is parameterized by a distinct packet-loss probability and loss-duration window (i.e., the maximum number of consecutive frames that can be lost). Mode A uses a relatively low loss probability and a short loss window, while mode B adopts substantially higher values for both parameters. When a loss event is active, the object-related observation vector is masked (set to zero); other observations remain unchanged. Parameters are manually tuned so that the statistics of the simulated object-perception signal approximate those of a physical MoCap system in real operation. 

