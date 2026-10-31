---
title: "HOIST: Humanoid Optimization with Imitation and Sample-efficient Tuning for Manipulating Suspended Loads"
date: "2026-05-29"
authors: "Songyang Liu; Shunyu Yao; Dingyuan Huang; Shuai Li"
url: https://arxiv.org/abs/2606.00252
pdf: https://arxiv.org/pdf/2606.00252
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.00252)** / [論文ページ](https://arxiv.org/abs/2606.00252)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HOIST: Humanoid Optimization with Imitation and Sample-efficient Tuning for Manipulating Suspended Loads** 

|**Songyang Liu**<sup>_∗_</sup>|**Shunyu Yao**<sup>_∗_</sup>|
|---|---|
|Department of Civil and Coastal Engineering<br>University of Florida United States<br>`liusongyang@ufl.edu`|Department of Civil and Coastal Engineering<br>University of Florida United States<br>`shunyu.yao@ufl.edu`|
|**Dingyuan Huang**|**Shuai Li**|
|Department of Civil and Coastal Engineering<br>University of Florida United States<br>`dingyuanhuang@ufl.edu`|Department of Civil and Coastal Engineering<br>University of Florida United States<br>`shuai.li@ufl.edu`<br>_†_Corresponding author|


**Abstract:** Manipulating suspended payloads with humanoid robots is challenging because the robot can only influence an underactuated, oscillatory load through whole-body motion and intermittent contact. Imitation learning provides safe initial behavior but does not directly optimize final placement, while reinforcement learning from scratch is unsafe and sample-inefficient on real humanoids. We present HOIST– **H** umanoid **O** ptimized with **I** mitation and **S** ampleefficient **T** uning for manipulating suspended loads. HOIST first finetunes a highlevel vision-language-action (VLA) policy from virtual-reality (VR) teleoperation demonstrations and executes its commands through a whole-body controller. It then uses VLA rollouts and iterative batched RL to improve placement accuracy and stopping behavior. Experiments in simulation and on a real humanoid show that HOIST improves over imitation-only and additional-demonstration baselines; compared with pure VLA rollouts, HOIST reduces translational placement error by 19.9 _cm_ and raw angular error by 3.56<sup>_◦_</sup> , demonstrating the potential of humanoids for underactuated material-handling tasks. 

**Keywords:** Robot manipulation, Reinforcement learning for physical robot control 


> _∗_ Equal contribution. 

Figure 1: Motivation and task setup for humanoid hoisting. Left: workers manually guide a suspended payload during construction hoisting, exposing them to struck-by and caught-between hazards. Right: our lab setup studies a humanoid robot pushing an externally suspended payload toward a target region, requiring whole-body balance, contact-rich pushing, and accurate stopping. Left image adapted from online material [1]. 

## **1 Introduction** 

Material handling often involves underactuated systems: payloads are not rigidly grasped or directly actuated, but are influenced through cables, hooks, slings, cranes, carts, or intermittent human contact. Such systems are common in construction, manufacturing, shipbuilding, logistics, and warehousing, where heavy payloads are transported by lifting equipment and then manually guided into their final positions. Hoisting is a representative example. Although cranes provide the primary lifting capability, final placement often still requires workers to stand near suspended loads and guide, stabilize, or push them by hand. Because suspended payloads can swing, respond with delay, and keep moving after contact, this stage creates struck-by and caught-between hazards [2, 3, 4, 5]. Fig. 1 illustrates both real hoisting operations and our lab setup, motivating the question: can humanoid robots safely operate around underactuated material-handling systems that are currently handled by human workers? 

We study this question through _humanoid hoisting_ : using a humanoid robot to position an externally suspended payload through whole-body motion and contact-rich manipulation. Unlike standard pick-and-place or tabletop manipulation, the robot cannot directly control the payload pose or velocity; it can only influence the payload through base motion, arm motion, body posture, and contact forces. The payload therefore behaves like an underactuated pendulum, a structure widely studied in crane modeling and anti-sway control [6, 7, 8, 9]. It may continue moving after the robot stops, overshoot the target, or retain residual oscillation. We therefore position humanoid hoisting as a new whole-body loco-manipulation problem, where success depends not only on feasible humanoid motion, but also on contact timing and stopping behavior for a dynamically active payload. VR teleoperation offers a practical way to collect demonstrations for initializing humanoid hoisting behaviors [10, 11, 12]. However, imitation learning does not directly optimize final placement accuracy and may accumulate errors during closed-loop execution [13]. Conversely, training from scratch with RL on a real humanoid is unsafe and sample-inefficient in this contact-rich setting [14, 15]. 

We present HOIST– **H** umanoid **O** ptimized with **I** mitation and **S** ample-efficient **T** uning for manipulating suspended loads. HOIST first uses VR whole body teleoperation collected demonstrations to finetune a high-level vision-language-action (VLA) policy, whose planner-level commands are executed by a whole-body controller. It then collects autonomous rollouts and applies iterative batched RL refinement with hoisting-specific rewards to improve placement accuracy and stopping behavior. This combines safe imitation initialization with task-level reward optimization, avoiding unsafe tabula-rasa exploration while addressing objectives not captured by imitation alone. Our contributions are: 

- We introduce _humanoid hoisting_ , a whole-body loco-manipulation problem involving an externally suspended, indirectly driven, and oscillatory payload, opening a direction for humanoids to operate underactuated material-handling systems. 

- We present HOIST, which combines VR teleoperation, supervised VLA finetuning, fixed whole-body execution, and sample-efficient RL refinement for suspended-payload manipulation. 

- We evaluate suspended-payload positioning in simulation and on a real humanoid, comparing additional demonstrations with RL refinement and analyzing how rollout count and input modalities affect placement accuracy. 

2 

## **2 Related Work** 

**Robotic hoisting and suspended-payload control.** Robotic systems have been widely studied for construction automation and material handling [16, 17], where hoisting heavy payloads is common. Because suspended loads exhibit pendulum-like dynamics, prior work has studied modeling, trajectory planning, input shaping, and anti-sway control for crane and cable-suspended systems [6, 7, 8, 18]. These methods typically control the lifting mechanism directly, whereas humanoid hoisting can only influence an externally suspended payload through intermittent whole-body contact. Our work therefore reformulates suspended-payload positioning as humanoid-assisted local manipulation, where the robot acts as an external contact-rich agent rather than part of the crane controller. 

**Humanoid whole-body control and loco-manipulation.** Humanoid whole-body control has advanced from motion tracking to real humanoid systems with richer high-level interfaces [19, 20, 21, 22, 23, 24]. Humanoid loco-manipulation further studies coordinated locomotion, balance, and contact-rich interaction through motion priors, residual policies, and compliance regulation [25, 26, 27, 28]. However, most prior tasks involve rigid or quasi-static objects whose motion is constrained by the robot or environment. In contrast, suspended payloads remain dynamically active after contact, making success depend on contact timing, accurate placement, and stopping behavior. 

**Reinforcement learning for robot control.** Reinforcement learning can optimize robot behavior from task rewards and environment interaction, including high-dimensional contact-rich manipulation [14, 29]. However, applying RL directly to humanoid hoisting is unsafe and sample-inefficient: early exploration may cause unstable motion, hard contacts, over-pushing, or large residual swing, motivating safety-aware and demonstration-guided learning [30, 31]. Our approach avoids tabularasa exploration by starting from a teleoperation-finetuned VLA policy and using RL to refine highlevel commands from limited rollouts, optimizing placement and stopping while preserving safe demonstrated behavior [15]. 

## **3 Methodology** 

This section describes the technical formulation and implementation of HOIST. We first define the humanoid hoisting problem, then present the teleoperation data collection, high-level VLA policy, whole-body controller, and RL refinement procedure used to improve final payload placement. 

### **3.1 Problem Formulation** 

We consider _humanoid hoisting_ , where a humanoid robot assists the local positioning of an externally suspended payload. Given a task instruction and visual observations, the robot must approach the payload, establish physical interaction, push it toward a target region, and stop without inducing excessive residual swing. The robot does not actuate the crane or suspension mechanism. Instead, it can only influence the payload through whole-body motion and intermittent contact forces. Therefore, the task couples humanoid locomotion and balance, contact timing, payload displacement, and delayed pendulum-like swing. 

We model humanoid hoisting as a task-conditioned, partially observed, closed-loop control problem. At each high-level decision step _t_ , the policy receives the observation 


where **I**<sup>ego</sup> _t_<sup>_,_rgb</sup> and **D**<sup>ego</sup> _t_ are the humanoid onboard RGB and depth observations, **I**<sup>side</sup> _t_<sup>_,_rgb</sup> is an external side-view image that captures the payload-target relationship, **x**<sup>_r_</sup> _t_<sup>denotesthehumanoid</sup> proprioceptive state, _ℓ_ is the language instruction, and **c**<sup>nav</sup> _t−_ 1<sup>isthepreviousnavigationcommand.</sup> 

3 


Figure 2: Overview of humanoid hoisting. Left: in standard pick-and-place, the robot directly actuates the object and receives an immediate object response. Middle: in humanoid hoisting, the payload is externally suspended and underactuated, so the robot can only influence it through wholebody contact; this introduces delayed motion, overshoot, and residual swing near the target. Right: HOIST addresses this setting by learning high-level hoisting commands from teleoperation and refining them with iterative batched RL, improving final placement accuracy while reducing residual sway. 


Figure 3: Motivation for imitation-initialized RL. Pure imitation yields safe motions but may leave large placement errors, while pure RL from scratch is unsafe and hard to converge on real humanoids. HOIST starts from an imitation-learned policy and uses iterative batched RL refinement to improve task-level placement while preserving safe behavior. 

The proprioceptive state **x**<sup>_r_</sup> _t_<sup>include joint states and base/IMU information.We do not assume direct</sup> contact-force sensing or explicit payload-state input to the policy. 

The high-level policy does not output joint torques. Instead, it predicts the next _H_ high-level plannercommand increments: 


where _πθ_ is the learned high-level VLA policy with parameters _θ_ , _H_ is the action-chunk horizon, and ∆ **U** _t_ is the predicted command-increment chunk at time _t_ . 

Each single-step command increment ∆ **u** _τ_ updates the head target, left-hand target, right-hand target, navigation command, and desired base height: 


4 


Figure 4: Overview of the HOIST pipeline. VR teleoperation provides hoisting demonstrations to finetune a high-level VLA policy, which predicts short-horizon planner-command chunks. A fixed whole-body controller executes these commands as stable humanoid motion. Autonomous VLA rollouts are then used for iterative batched RL with hoisting-specific rewards to improve placement accuracy, residual swing, and stopping behavior. 

Here, _τ_ indexes a future high-level step within the predicted command chunk, **y** _τ_<sup>head</sup> is the head tracking target, **y** _τ_<sup>_L_and</sup><sup>**y**</sup> _τ_<sup>_R_are the left- and right-hand tracking targets,</sup><sup>**c**nav</sup> _τ_ is the navigation command, and _h_<sup>base</sup> _τ_ is the desired base-height command. The corresponding full planner command at time _t_ is **u** _t_ = � **y** _t_<sup>head</sup> _,_ **y** _t_<sup>_L,_</sup><sup>**y**</sup> _t_<sup>_R,_</sup><sup>**c**</sup> _t_<sup>nav</sup> _, h_<sup>base</sup> _t_ � _._ (4) In words, the VLA policy only decides short-horizon task-level motions, such as where the hands and body should move next; the low-level controller converts these commands into balanced wholebody motion. 

The execution stack maintains the previous full planner command **u** _t−_ 1, while the policy receives only the previous navigation command **c**<sup>nav</sup> _t−_ 1<sup>asanexplicitcommand-historyinput.Atexecution</sup> time, we apply the first increment in the chunk to update the current planner command: 


The updated command is then executed by a humanoid whole-body control stack: 


where _π_ wbc is a fixed decoupled whole-body controller [22], and **a**<sup>motor</sup> _t_ denotes the low-level motor command. This hierarchy lets the learned policy operate at the task-command level, while wholebody tracking, balance, and joint-level stabilization are handled by the fixed execution stack. 

### **3.2 Overview of HOIST** 

Our method consists of three stages: teleoperation data collection, supervised VLA finetuning, and RL refinement. First, a human operator uses a VR headset and controllers to teleoperate the humanoid robot through the hoisting task. Second, we use the collected teleoperation data to finetune A high-level VLA policy, so that the humanoid can autonomously generate hoisting-related planner commands from visual observations and task instructions. Third, we deploy the finetuned VLA policy to collect autonomous rollouts and use these rollouts for iterative batched flow-matching-steering RL [15] refinement. 

5 

**Teleoperation data collection.** We collect demonstrations using a PICO VR headset and controllers. The operator guides the humanoid through the full hoisting sequence: approach, contact, push, and stop. Each trajectory is stored as 


where **u**<sup>demo</sup> _t_ is the planner command produced during teleoperation and _yi_ denotes trajectory-level outcomes such as final placement error and residual motion. 

We construct the supervised action-chunk target as 


These demonstrations initialize the high-level policy with safe approach, pushing, and stopping behavior. 

**High-level VLA policy.** We build the high-level policy by modifying GR00T N1.6 [23] for humanoid hoisting. The policy takes multimodal observations and task instructions as input and outputs a short sequence of relative commands for both hands, the navigation command, the head pose, and the base height. To make the policy better aware of the robot’s current motion, we add the navigation command as an additional modality to the vision-language model. We also add depth images and robot ego-velocity to the flow-matching based action expert, so that the action expert can condition on both scene geometry and the humanoid’s current physical state. During supervised finetuning, most VLM layers are frozen; we finetune only the final four layers of VLM, the diffusion-transformer action expert, and the encoders for the newly introduced modalities. This design adapts the foundation policy to humanoid hoisting while preserving the general visual-language and action priors learned by the pretrained model. 

**Humanoid whole-body controller.** We use the GR00T Whole-Body Control deployment stack as a fixed execution layer. The high-level VLA policy outputs planner-level command updates, which are accumulated into inputs as target velocities, hand/head tracking targets, and base height. We do not train or finetune the planner or low-level controller for the hoisting task. This design keeps the low-level motion prior fixed and shifts task adaptation to the high-level VLA policy and RL refinement module. Thus, HOIST learns how to command hoisting-relevant motion without learning joint-level actuation or modifying the whole-body controller. 

**Reinforcement-learning refinement.** After supervised finetuning, we refine the high-level command generator using VLA rollouts. In each domain, we deploy the finetuned VLA policy together with the fixed whole-body controller to collect a small batch of autonomous hoisting rollouts. These rollouts are added to a refinement dataset and labeled with hoisting-specific rewards. In our current implementation, the reward is a simple weighted combination of translational placement errors and the raw angular error, rather than a learned or heavily shaped reward model. We then perform an offline actor-critic update on the accumulated rollout dataset. The updated refinement module is redeployed to collect the next batch of rollouts, and the same collect-train cycle is repeated. During rollouts, we record the initial noise used by the flow-matching action expert and train an actor-critic module to predict which initial-noise vector should be used for a given state. The actor outputs this steering vector deterministically rather than predicting a mean and variance and then sampling from them. Throughout RL, the VLA policy itself remains frozen; only the noise-steering actor-critic module is updated. For efficiency, we store VLM features from the frozen policy and reuse them to avoid repeated encoding of the same visual-language observations. This batched flywheel allows the refinement stage to improve placement accuracy with a small number of task rollouts while preserving the behavior learned from teleoperation. 

6 

### **3.3 Metrics** 

Let ( _xT , yT , ψT_ ) denote the final planar pose of the payload center and ( _x_<sup>_⋆_</sup> _, y_<sup>_⋆_</sup> _, ψ_<sup>_⋆_</sup> ) denote the target pose. We evaluate placement accuracy using absolute translational and yaw errors: 

**e** place = [∆ _x_ ∆ _y_ ∆ _ψ_ ] = [ _|xT − x_<sup>_⋆_</sup> _| |yT − y_<sup>_⋆_</sup> _| |_ wrap( _ψT − ψ_<sup>_⋆_</sup> ) _|_ ] _._ (9) 

Here, ∆ _x_ and ∆ _y_ measure the terminal center offset of the payload along the _x_ - and _y_ -directions, respectively, while ∆ _ψ_ measures its terminal rotational error about the vertical _z_ -axis. In the result tables, we report ∆ _x_ , ∆ _y_ , ∆ _ψ_ , and the Manhattan terminal position error ∆ _x_ + ∆ _y_ . 

## **4 Experiments and Results** 

### **4.1 Experiment Setup** 

We evaluate HOIST in simulation and on a real humanoid platform. Each trial starts with the payload away from the target; the humanoid must position it through contact without actuating the suspension mechanism. In each domain, VLA-50 is finetuned on 50 teleoperated demonstrations, VLA-80 uses 80 demonstrations, and HOIST starts from VLA-50 before applying up to 30 samedomain RL rollouts. All methods use the same frozen GR00T whole-body execution stack, isolating changes to the high-level command policy. 

### **4.2 Reinforcement-Learning Progression** 

Table 1 reports placement accuracy after each batch of RL rollouts. The resulting trend shows whether same-domain refinement steadily improves the VLA-50 initialization. A decreasing error trend indicates that rollout feedback corrects placement bias left by imitation learning. 

Table 1: Placement accuracy with increasing numbers of RL rollouts. 

|Domain|Method|∆_x_(cm)_↓_|∆_y_(cm)_↓_|∆_ψ_(deg)_↓_|_|_∆_x|_+_|_∆_y|_(cm)_↓_|
|---|---|---|---|---|---|
|Simulation|Human Expert Teleop|4.35|3.00|8.48|7.35|
|Simulation|VLA-50|21.56|0.88|3.85|22.44|
|Simulation|VLA-50 + 10 RL rollouts|15.09|1.83|4.58|16.92|
|Simulation|VLA-50 + 20 RL rollouts|**1.72**|**0.82**|**0.29**|**2.54**|
|Simulation|VLA-50 + 30 RL rollouts|5.16|1.09|2.76|6.25|
|Real platform|VLA-50|**1.60**|7.68|14.5|9.28|
|Real platform|VLA-50 + 10 RL rollouts|2.15|5.22|21.0|7.37|
|Real platform|VLA-50 + 20 RL rollouts|4.20|**2.49**|**12.1**|6.69|
|Real platform|VLA-50 + 30 RL rollouts|1.64|4.74|28.9|**6.38**|


### **4.3 Reinforcement Learning versus Additional Demonstrations** 

Table 2 compares additional demonstrations with same-domain RL rollouts after the initial 50 demonstrations. HOIST achieves better performance than VLA-80, showing that optimizing closedloop placement rewards is more effective than adding demonstrations alone. This supports using RL to correct final-position errors that remain after imitation learning. 

Table 2: Additional demonstrations versus RL refinement. 

|Domain|Method|Demos|RL rollouts|∆_x_(cm)_↓_|∆_y_(cm)_↓_|∆_ψ_(deg)|_|_∆_x|_+_|_∆_y|_(cm)_↓_|
|---|---|---|---|---|---|---|---|
|Simulation|VLA-50|50|0|21.56|**0.88**|3.85|22.44|
|Simulation|VLA-80|80|0|15.69|2.89|12.14|18.58|
|Simulation|HOIST (OURS)|50|30|**5.16**|1.09|**2.76**|**6.25**|
|Real platform|VLA-50|50|0|1.60|7.68|**14.5**|9.28|
|Real platform|VLA-80|80|0|**0.54**|8.03|27.0|8.57|
|Real platform|HOIST (OURS)|50|30|1.64|**4.74**|28.9|**6.38**|


7 

### **4.4 Observation-Modality Ablation** 

Table 3 evaluates the VLA policy before RL refinement under different input modalities. The goal is to measure whether depth and navigation-command conditioning improve the imitation-learned initialization. All rows use the same number of demonstrations and no RL rollouts. 

Table 3: Ablation of VLA input modalities before RL refinement. 

|VLA variant|Depth|Nav command|∆_x_(cm)_↓_|∆_y_(cm)_↓_|∆_ψ_(deg)_↓_|_|_∆_x|_+_|_∆_y|_(cm)_↓_|
|---|---|---|---|---|---|---|
|Base VLA|–|–|1.54|10.52|26.6|12.06|
|+ Depth|✓|–|**0.78**|8.78|14.8|9.57|
|+ Nav command|–|✓|1.30|9.90|32.5|11.20|
|+ Nav command + Depth|✓|✓|1.60|**7.68**|**14.5**|**9.28**|


Depth improves contact-geometry awareness, while navigation-command conditioning improves the use of current base motion. The combined variant performs best, supporting the use of both modalities before RL refinement. 

### **4.5 Residual Motion Analysis** 


Figure 5: Residual-motion analysis from an IMU mounted on the suspended payload. 

We further analyze payload dynamics throughout the lifting process using an IMU mounted on the suspended load. As shown in Fig. 5, compared with the imitation-only policy, HOIST yields higher accelerometer readings but reduces gyroscope responses by approximately half, suggesting reduced angular motion with more active corrective adjustments during lifting. Meanwhile, both learned policies exhibit lower accelerometer and gyroscope readings than human teleoperation demonstrations, which may reflect the more frequent closed-loop corrections performed by human operators. 

## **5 Discussion** 

The improvement from 30 RL rollouts suggests that the imitation-learned VLA policy has systematic deployment bias. Supervised finetuning matches expert actions on the demonstration distribution, but the learned policy is not executed under that same distribution: once deployed, its own prediction errors affect contact timing, pushing strength, and stopping behavior, producing a different closedloop rollout distribution. Thus, the policy may consistently under-push, over-push, or stop at a biased terminal position. 

Additional demonstrations add more expert-distribution data, but they do not directly identify this deployment-time bias. In contrast, autonomous rollouts reveal the biased trajectories generated by the current VLA policy itself. HOIST can then use task-level rewards to learn an initial-noise correction that steers the frozen policy away from these systematic errors. This makes RL rollouts more useful than extra demonstrations for correcting final placement accuracy. 

8 

## **6 Limitation** 

The primary limitation of the current system lies in the low-level whole-body controller, which has not been fine-tuned for interaction with suspended payloads. Specifically, the policy can only influence robot execution through a limited interface consisting of navigation commands, head pose, base height, and bimanual hand poses, without explicitly adapting the applied force to different payload weights. Consequently, the system struggles to generate sufficiently large and adaptive forces when manipulating heavier objects, limiting its ability to handle heavy payloads. 

## **7 Conclusion** 

We presented HOIST, which initializes humanoid hoisting from teleoperated demonstrations and improves final placement through rollout-level RL while keeping the whole-body controller fixed. The learned initial-noise correction changes command sequences, which propagate through humanoid-payload contact dynamics to reduce final placement error and residual swing. Future work will expand payload and suspension conditions, add explicit safety constraints, and study coordinated humanoid-hoist control. 

9 

### **Acknowledgments** 

If a paper is accepted, the final camera-ready version will (and probably should) include acknowledgments. All acknowledgments go at the end of the paper, including thanks to reviewers who gave useful comments, to colleagues who contributed to the ideas, and to funding agencies and corporate sponsors that provided financial support. 

## **References** 

- [1] Holy maker. The construction process for a modular concrete home takes just two weeks. Precast Concrete (PC) Factory. YouTube video, 2026. URL `https://www.youtube.com/ watch?v=GXIMQnndCVU&t=1133s` . Screenshot captured at 18:53. Accessed: 2026-05-28. 

- [2] National Institute for Occupational Safety and Health. Preventing struck-by injuries in construction: Lift zone safety. CDC/NIOSH Science Blog, 2021. Accessed 2026-05-07. 

- [3] U.S. Bureau of Labor Statistics. Fatal occupational injuries involving cranes, 2011–17. BLS Injuries, Illnesses, and Fatalities Factsheet, 2023. Accessed 2026-05-07. 

- [4] National Institute for Occupational Safety and Health. Niosh alert: Preventing worker injuries and deaths from mobile crane tip-over, boom collapse, and uncontrolled hoisted loads. Technical Report DHHS (NIOSH) Publication No. 2006-142, U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, 2006. 

- [5] Occupational Safety and Health Administration. Construction focus four: Struck-by hazards. OSHA Training Material, 2011. 

- [6] E. M. Abdel-Rahman, A. H. Nayfeh, and Z. N. Masoud. Dynamics and control of cranes: A review. _Journal of Vibration and control_ , 9(7):863–908, 2003. 

- [7] L. Ramli, Z. Mohamed, A. M. Abdullahi, H. I. Jaafar, and I. M. Lazim. Control strategies for crane systems: A comprehensive review. _Mechanical Systems and Signal Processing_ , 95: 1–23, 2017. 

- [8] H.-y. Qiang, Y.-g. Sun, J.-c. Lyu, and D.-s. Dong. Anti-sway and positioning adaptive control of a double-pendulum effect crane system with neural network compensation. _Frontiers in Robotics and AI_ , 8:639734, 2021. 

- [9] M. R. Mojallizadeh, B. Brogliato, and C. Prieur. Modeling and control of overhead cranes: A tutorial overview and perspectives. _Annual Reviews in Control_ , 56:100877, 2023. 

- [10] T. Zhang, Z. McCarthy, O. Jow, D. Lee, X. Chen, K. Goldberg, and P. Abbeel. Deep imitation learning for complex manipulation tasks from virtual reality teleoperation. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 5628–5635. Ieee, 2018. 

- [11] E. Rosen, D. Whitney, E. Phillips, D. Ullman, and S. Tellex. Testing robot teleoperation using a virtual reality interface with ros reality. In _Proceedings of the 1st International Workshop on Virtual, Augmented, and Mixed Reality for HRI (VAM-HRI)_ , pages 1–4, 2018. 

- [12] S. Han. _VR teleoperation interface for learning loco-manipulation of humanoid robots_ . PhD thesis, 2023. 

- [13] S. Ross, G. Gordon, and D. Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

- [14] A. Rajeswaran, V. Kumar, A. Gupta, G. Vezzani, J. Schulman, E. Todorov, and S. Levine. Learning complex dexterous manipulation with deep reinforcement learning and demonstrations. _arXiv preprint arXiv:1709.10087_ , 2017. 

10 

- [15] A. Wagenmaker, M. Nakamoto, Y. Zhang, S. Park, W. Yagoub, A. Nagabandi, A. Gupta, and S. Levine. Steering your diffusion policy with latent space reinforcement learning. _arXiv preprint arXiv:2506.15799_ , 2025. 

- [16] T. Bock and T. Linner. _Construction robots: Elementary technologies and single-task construction robots_ . Cambridge University Press, 2016. 

- [17] X. Xu and B. G. De Soto. On-site autonomous construction robots: A review of research areas, technologies, and suggestions for advancement. In _ISARC. Proceedings of the International Symposium on Automation and Robotics in Construction_ , volume 37, pages 385–392. IAARC Publications, 2020. 

- [18] R. Hoffman and H. H. Asada. Precision assembly of heavy objects suspended with multiple cables from a crane. _IEEE Robotics and Automation Letters_ , 5(4):6876–6883, 2020. 

- [19] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne. Deepmimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [20] X. B. Peng, A. Kanazawa, J. Malik, P. Abbeel, and S. Levine. Sfv: Reinforcement learning of physical skills from videos. _ACM Transactions On Graphics (TOG)_ , 37(6):1–14, 2018. 

- [21] A. Allshire, H. Choi, J. Zhang, D. McAllister, A. Zhang, C. M. Kim, T. Darrell, P. Abbeel, J. Malik, and A. Kanazawa. Visual imitation enables contextual humanoid control. _arXiv preprint arXiv:2505.03729_ , 2025. 

- [22] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Castaneda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, et al. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [23] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [24] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, and Y. Zhu. GR00T Whole-Body Control, 2025. URL `https://github.com/NVlabs/ GR00T-WholeBodyControl` . Software repository. 

- [25] E. Yoshida, V. Hugel, P. Blazevic, K. Yokoi, and K. Harada. Dexterous humanoid whole-body manipulation by pivoting. _Humanoid Robots, Human-like Machines_ , 2007. 

- [26] Y. Zhang, Y. Yuan, P. Gurunath, I. Gupta, S. Omidshafiei, A.-a. Agha-mohammadi, M. Vazquez-Chanlatte, L. Pedersen, T. He, and G. Shi. Falcon: Learning force-adaptive humanoid loco-manipulation. _arXiv preprint arXiv:2505.06776_ , 2025. 

- [27] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [28] S. Chen, Z.-a. Cao, Z. Luo, F. Casta˜neda, C. Li, T. Wang, Y. Yuan, L. Fan, C. K. Liu, Y. Zhu, et al. Chip: Adaptive compliance for humanoid control through hindsight perturbation. _arXiv preprint arXiv:2512.14689_ , 2025. 

- [29]<sup>´</sup> I. Elguea-Aguinaco, A. Serrano-Mu˜noz, D. Chrysostomou, I. Inziarte-Hidalgo, S. Bøgh, and N. Arana-Arexolaleiba. A review on reinforcement learning for contact-rich robotic manipulation tasks. _Robotics and Computer-Integrated Manufacturing_ , 81:102517, 2023. 

- [30] J. Garcıa and F. Fern´andez. A comprehensive survey on safe reinforcement learning. _Journal of Machine Learning Research_ , 16(1):1437–1480, 2015. 

11 

- [31] S. Gu, A. Kshirsagar, Y. Du, G. Chen, J. Peters, and A. Knoll. A human-centered safe robot reinforcement learning framework with interactive behaviors. _Frontiers in Neurorobotics_ , 17: 1280341, 2023. 

12 

