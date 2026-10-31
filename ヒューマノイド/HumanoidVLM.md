---
title: "HumanoidVLM: Vision-Language-Guided Impedance Control for Contact-Rich Humanoid Manipulation"
date: "2026-01-21"
authors: "Yara Mahmoud; Yasheerah Yaqoot; Miguel Altamirano Cabrera; Dzmitry Tsetserukou"
url: https://arxiv.org/abs/2601.14874
pdf: https://arxiv.org/pdf/2601.14874
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.14874)** / [論文ページ](https://arxiv.org/abs/2601.14874)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HumanoidVLM: Vision–Language–Guided Impedance Control for Contact-Rich Humanoid Manipulation** 

Yara Mahmoud 

Skolkovo Institute of Science and Technology Moscow, Russia yara.mahmoud@skoltech.ru 

Miguel Altamirano Cabrera Skolkovo Institute of Science and Technology Moscow, Russia m.altamirano@skoltech.ru 

Yasheerah Yaqoot Skolkovo Institute of Science and Technology Moscow, Russia yasheerah.yaqoot@skoltech.ru 

Dzmitry Tsetserukou 

Skolkovo Institute of Science and Technology Moscow, Russia d.tsetserukou@skoltech.ru 


**Figure 1: Overall architecture of the proposed HumanoidVLM framework.** 

## **Abstract** 

Humanoid robots must adapt their contact behavior to diverse objects and tasks, yet most controllers rely on fixed, hand-tuned impedance gains and gripper settings. This paper introduces HumanoidVLM, a vision–language driven retrieval framework that enables the Unitree G1 humanoid to select task-appropriate cartesian impedance parameters and gripper configurations directly from an ego-centric RGB image. The system couples a vision–language model for semantic task inference with a FAISS-based RetrievalAugmented Generation (RAG) module that retrieves experimentally validated stiffness–damping pairs and object-specific grasp angles from two custom databases, and executes them through a task-space impedance controller for compliant manipulation. We evaluate HumanoidVLM on 14 visual scenarios and achieve a retrieval accuracy of 93%. Real-world experiments show stable interaction dynamics, with _𝑧_ -axis tracking errors typically within 1–3 _._ 5 cm and virtual forces consistent with task-dependent impedance settings. These results demonstrate the feasibility of linking semantic perception with retrieval-based control as an interpretable path toward adaptive humanoid manipulation. 

## **CCS Concepts** 

• **Human-centered computing** → **Collaborative interaction** ; • **Computing methodologies** → _Vision for robotics_ ; • **Computer systems organization** → Robotic control. 

## **Keywords** 

Human-Robot Interaction, Vision Language Model, Retrieval-Augmented System, Task-Space compliance, impedance control 

## **1 Introduction** 

Humanoid robots are increasingly expected to operate in unstructured human environments, where tasks such as placing objects, applying force on surfaces, grasping diverse items, or manipulating tools require a combination of semantic understanding and compliant physical interaction [8]. Conventional control pipelines for such systems typically rely on fixed, hand-tuned impedance gains [12] and manually specified gripper configurations, which restrict the robot’s ability to adapt to changes in scene geometry, object properties, or task intent. 

Yara Mahmoud, Yasheerah Yaqoot, Miguel Altamirano Cabrera, and Dzmitry Tsetserukou 

In parallel, recent advances in Vision–Language Models (VLMs) have demonstrated impressive capabilities in open-world perception, contextual reasoning, and grounded language understanding [6], making them promising candidates for high-level task inference in robotics [9]. However, despite their strong semantic understanding, these models remain largely disconnected from the low-level control parameters that determine how a robot physically interacts with its environment. As a result, current humanoid systems lack the capacity to autonomously translate visual semantics into actionable, task-appropriate interaction behaviors—a limitation that is especially pronounced in contact-rich manipulation tasks, where selecting correct stiffness, damping, and grasping configurations is essential for safe and stable execution. 

To bridge this gap, we introduce HumanoidVLM, a retrievalaugmented vision–language framework that connects high-level visual reasoning with low-level manipulation parameters for the Unitree G1 humanoid robot. Given a single egocentric image, HumanoidVLM infers the ongoing manipulation task through structured visual queries and retrieves the corresponding cartesian impedance parameters and object-specific gripper angle from custom, experimentally validated databases. This approach enables the robot to autonomously determine task-appropriate compliance settings for a given scene. 

## **2 Related Works** 

**Foundation models and semantic manipulation.** Recent advances in foundation models have accelerated progress in semantic manipulation and scene-aware task execution. OmniVIC [18] and ImpedanceGPT [7] are most closely related to our approach, combining a vision–language model with a variable impedance controller through retrieval. However, OmniVIC focuses on industrial arms and does not address humanoid embodiment, shared workspaces, or HRI-oriented safety. Vision–language–action systems such as PG-VLM [10], SayCan [4], RT-2 [19],Bi-VLA [11], and SwarmVLM [17] show that multimodal models can generalize manipulation behavior, but these frameworks operate at the policy or pose level and rely on fixed impedance gains. Broader surveys on foundation models for manipulation and robot intelligence [15], [13] highlight the role of semantic reasoning but do not consider continuous impedance modulation in humanoid settings. Work on foundation models for collaborative assembly [14] emphasizes contextual reasoning in shared autonomy, yet compliant control remains largely unaddressed. 

**Impedance and variable impedance control.** Classical impedance control, introduced by Hogan [12], provides a structured formulation for regulating robot–environment interaction through stiffness and damping shaping. Surveys by Abu-Dakka and Saveriano [3] document advances in variable impedance strategies, including learning-based adaptation and physical interaction applications. In human–robot collaboration, Ajoudani _et al._ [5] stress the importance of compliance modulation for safety and ergonomics, following earlier studies on tactile and impedance-based interaction in humanoid systems [16]. Building on this foundation, our work links semantic scene understanding to impedance and gripper selection through retrieval-augmented reasoning, enabling task-aware compliant control on a humanoid. 

## **3 System Architecture** 

The proposed system enables the Unitree G1 humanoid to adapt its end-effector impedance and grasping behavior using visual scene understanding and retrieval-based reasoning. An ego-centric RGB image from the robot’s head camera is processed by a vision– language model (VLM), which infers the high-level manipulation task through structured visual queries. The resulting semantic task label is embedded and passed to a Retrieval-Augmented Generation (RAG) module that performs FAISS-based similarity search over two custom databases: (i) a cartesian impedance database storing task-specific stiffness and damping coefficients for the end-effector, and (ii) a gripper-angle database specifying the optimal grasp configuration for the object category. 

The retrieved control parameters ( _𝐾_ , _𝐷_ , and gripper angle _𝛾_ ) are transmitted to the onboard G1 computer, where a task-space cartesian impedance controller generates compliant end-effector trajectories. These desired virtual poses are then converted into joint targets through inverse kinematics and executed using the robot’s built-in position controllers. Fig. 1 provides an overview of the perception, reasoning, and control pipeline. 

## **3.1 VLM–RAG System** 

The VLM–RAG system processes the ego-centric view using the Molmo-7B-O BnB 4-bit model [1] to identify the task-relevant objects and scene context. The visual output is converted into a multimodal representation and embedded using the all-MiniLM-L6-v2 sentence-transformer [2], enabling semantically meaningful retrieval within a shared vector space. Given an input image, the VLM determines the task through sequential yes/no queries. The RAG system then retrieves the corresponding impedance and gripper parameters, providing the controller with context-dependent gains for safe and adaptive manipulation. 

_3.1.1 Custom Database for Environmental Scenarios._ The database contains nine manipulation tasks, each associated with experimentally validated cartesian impedance parameters and an optimal gripper configuration. Impedance parameters include stiffness coefficients _𝐾_ = [ _𝐾𝑥, 𝐾𝑦, 𝐾𝑧_ ] and damping coefficients _𝐷_ = [ _𝐷𝑥, 𝐷𝑦, 𝐷𝑧_ ], which determine how the end-effector regulates contact forces and compliance along the cartesian axes. Each entry also specifies a preferred gripper angle _𝛾𝑎_ for secure manipulation of the corresponding object type. 

The retrieval system relies on two JSON databases. The impedance database stores task-specific cartesian impedance parameters collected from real-world experiments on the G1 humanoid. Multiple settings were tested per task, and the most stable and compliant configuration was recorded as the canonical entry. The gripper database contains experimentally determined optimal closing angles for manipulating rigid, soft, deformable, or fragile objects. These angles were obtained through repeated trials and represent secure yet compliant grasp strategies. 

Together, these two databases map a semantic task label to its corresponding control variables, namely the cartesian impedance parameters and the gripper configuration, forming the knowledge base of the RAG module. 

HumanoidVLM: Vision–Language–Guided Impedance Control for Contact-Rich Humanoid Manipulation 

## **3.2 Robot Control** 

_3.2.1 End-effector Impedance Control._ The Unitree G1 does not provide wrist force–torque sensing, and its two-finger grippers lack reaction wrench feedback. To enable compliant interaction without force sensors, we adopt a homogeneous cartesian mass–spring– damper model in task space. Each end-effector is regulated as a 6-DoF point following a desired pose trajectory, which acts as a virtual reference for the impedance dynamics. 

The translational impedance parameters K and D are selected by the VLM–RAG system, while the virtual mass M and rotational impedance remain fixed for stability. For each arm _𝑎_ ∈{ _𝐿, 𝑅_ }, let x _𝑎_ ∈ R<sup>3</sup> and R _𝑎_ ∈ _𝑆𝑂_ (3) denote the current end-effector position and orientation, and let x _𝑎,_ ref _,_ R _𝑎,_ ref denote the desired reference pose. We define diagonal virtual mass, damping, and stiffness matrices: 


For each arm _𝑎_ , the translational error is defined as in (2), the impedance dynamics follow the second order ODE (3), and the resulting virtual force is given by (4). 


captures the interaction response, acting as a quantitative proxy for physical contact forces. If no disturbance exists, both pose error and the corresponding virtual forces converge to zero. 

_3.2.2 Gripper Configuration._ Each hand uses a single-DoF gripper. The controller receives a discrete action: _𝛾𝑎_ ∈{open _,_ close}, where each action corresponds to a predefined joint angle target retrieved from the database. Gripper angles are retrieved from the VLM–RAG database based on the inferred task and object type, complementing the impedance parameters selected for the scenario. 

## **4 System Evaluation** 

Experiments were conducted on the Unitree G1 humanoid robot equipped with two 1-DoF grippers and an Intel RealSense RGB-D camera mounted in the head for ego-centric perception. The taskspace impedance controller ran on the on-board PC at 50 Hz, while the VLM–RAG pipeline was executed on an external workstation with an RTX 4090 GPU and Intel i9-13900K CPU to ensure real-time inference. 

## **4.1 Experimental Setup** 

Evaluation focused on tabletop tasks dominated by normal-direction interaction along the _𝑧_ -axis. Five representative task groups were considered: (1) Following an irregular surface by maintaining smooth right-hand contact, (2) Applying controlled _𝑧_ -direction forces while holding a massage ball, (3) Bimanual placement of two objects: a sauce bottle (left) and an egg (right), (4) Tool interaction using a fork to poke a fruit or vegetable, and (5) Grasping and lifting various tabletop objects. 

Each scenario was executed with multiple impedance and gripper settings to empirically determine the optimal parameters stored in the database. Fig. 2 shows examples from successful trials. 


**Figure 2: Images from successful trials of the representative manipulation scenarios.** 

_4.1.1 VLM–RAG Retrieval Evaluation._ The evaluation tests the discrete retrieval correctness of impedance and gripper parameters from a single ego-centric image. A retrieval is considered correct for evaluation purposes when the system: (1) classifies the task correctly via sequential visual yes/no queries, (2) retrieves the correct impedance entry based on the VLM output, and (3) retrieves the correct gripper configuration conditioned on both the VLM task label and the impedance scenario. 

_4.1.2 Retrieval Process._ To assess semantic generalization across tasks, 14 ego-centric test images were collected. These depict the nine task types but vary in camera viewpoint, object placement, and arm pose, ensuring robustness evaluation rather than memorization. For each image, the VLM infers the task through hierarchical visual queries. The resulting task label is used as a FAISS query to retrieve the impedance scenario. The scenario description is then concatenated with the VLM label to form a second query for retrieving the appropriate gripper configuration. This two-stage retrieval disambiguates visually similar tasks differing in object type or interaction mode. 

_4.1.3 Impedance Control Evaluation._ To confirm that retrieved parameters yield stable and bounded interaction behavior, we analyze _𝑧_ -axis tracking errors and virtual force magnitudes during execution. Single-object tasks use the right arm; dual-object placement uses both arms. The evaluation checks whether the selected _𝐾𝑧_ and _𝐷𝑧_ values achieve the expected compliance and whether position errors and virtual forces remain bounded and task-appropriate. 

## **4.2 Results** 

_4.2.1 VLM–RAG System._ The VLM–RAG pipeline was evaluated on 14 ego-centric test images representing variations of the nine tasks stored in the database (Sec. 4.1.1). The system retrieved the correct impedance and gripper parameters in 13 out of 14 cases, resulting in an accuracy of 93% as can be seen in Fig. 3. The single failure occurred when the primary object was partially occluded, highlighting a limitation of the current vision-based task inference. 

_4.2.2 Control Evaluation Results._ Table 1 summarizes the retrieved parameters and corresponding performance metrics. For each scenario, we report the selected normal-direction gains _𝐾𝑧, 𝐷𝑧_ , the 

Yara Mahmoud, Yasheerah Yaqoot, Miguel Altamirano Cabrera, and Dzmitry Tsetserukou 


**Figure 3: Retrieval accuracy of the VLM–RAG system across 14 scenarios.** 

mean and maximum absolute position error in _𝑧_ , and the maximum virtual normal force magnitude. Across all scenarios, _𝑧_ -axis tracking errors remained small, and the computed virtual force magnitudes scaled consistently with the selected impedance gains. This confirms that the retrieved parameters produce stable and task-appropriate interaction behavior. 

**Table 1: Task-space impedance evaluation for representative tabletop tasks.** 


**Figure 4: Translational errors in the surface-following task, showing desired and measured end-effector positions using forward kinematics.** 

## **5 Conclusion and Future Work** 

|Task|_𝐾𝑧_|_𝐷𝑧_||_𝑒𝑧_||max|_𝑒𝑧_||max|_𝐹_<sup>virt</sup><br>_𝑧_<br>||
|---|---|---|---|---|---|
||[N/m]|[Ns/m]|[m]|[m]|[arb.]|
|Follow surface (R)|3.0|2.0|0.016|0.024|0.103|
|apply pressure (R)|5.0|3.0|0.017|0.035|0.334|
|Dual placement (R)|2.0|1.0|0.013|0.034|0.089|
|Dual placement (L)|6.0|1.5|0.009|0.013|0.176|
|Tool interaction (R)|2.0|1.5|0.006|0.016|0.183|
|Grasp from table (R)|4.0|1.5|0.013|0.022|0.153|


**Surface following** Soft stiffness enabled compliant tracking of curved geometry, with low virtual forces and small errors. As seen in Fig. 4, the robot tracks the curved object with compliant contact. Fig. 4 shows that _𝑧_ error follow the surface profile, while _𝑥_ deviations stem from orientation adjustments of the arm. **Massage and pressure application:** Higher stiffness and damping resulted in larger virtual forces while maintaining similar tracking accuracy, demonstrating effective modulation of contact intensity. **Dual-object placement:** Asymmetric stiffness values reflected object fragility. The egg-handling arm used soft settings, while the bottle-handling arm used stiffer gains, producing correspondingly higher force responses. **Tool interaction:** Moderate stiffness and damping supported controlled poking motions with low tracking error and transient force peaks appropriate for brief contact events. **Grasp-and-lift:** Intermediate stiffness ensured stable lifting without excessive pressure, with tracking errors remaining below 2.5 cm. 

The controller behaved consistently, with low stiffness enabling compliant contact, high stiffness supporting forceful interaction, and asymmetric bimanual settings matching object-specific needs. The clear link between impedance parameters and virtual force responses indicates that these virtual forces may serve as effective proxies for real contact forces. 

This paper presented HumanoidVLM, a vision–language–driven retrieval framework that links semantic scene understanding with task-specific cartesian impedance and gripper control for the Unitree G1 humanoid. By combining VLM-based task inference with a FAISS-based RAG module, the system autonomously selects stiffness, damping, and grasp configurations directly from an egocentric image using two small human-validated databases containing nine manipulation tasks and nine object-specific grasp entries. Experiments across manipulation tasks showed that the framework retrieves correct parameters in 93% of the evaluated scenarios and enables stable, compliant execution in real-world trials. 

Given the limited evaluation scale and task diversity, the current results should be interpreted as a proof of feasibility rather than a comprehensive robustness assessment. In future work, we aim to incorporate task-dependent _rotational_ impedance to enable orientation-sensitive behaviors. Second, substituting the discrete database with a learned continuous mapping could allow interpolation across unseen tasks and object types. Finally, integrating force or visuotactile feedback would allow closed-loop impedance adaptation, improving safety and robustness. 

## **Acknowledgements** 

Research reported in this publication was financially supported by the RSF grant No. 24-41-02039. 

## **References** 

- [1] 2025. _Molmo-7B-O BnB 4bit quantized 7GB_ . https://huggingface.co/cyan2k/ molmo-7B-O-bnb-4bit 

- [2] 2025. _Sentence Transformer: all-MiniLM-L6-v2_ . https://huggingface.co/sentencetransformers/all-MiniLM-L6-v2 

- [3] Fares J. Abu-Dakka and Matteo Saveriano. 2020. Variable Impedance Control and Learning—A Review. _Frontiers in Robotics and AI_ 7 (2020), 590681. doi:10. 3389/frobt.2020.590681 

HumanoidVLM: Vision–Language–Guided Impedance Control for Contact-Rich Humanoid Manipulation 

- [4] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. 2023. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. _Proc. of the Conf. on Robot Learning_ 205 (2023). 

- [5] Arash Ajoudani, Andrea Maria Zanchettin, Serena Ivaldi, Alin Albu-Schäffer, Kazuhiro Kosuge, and Oussama Khatib. 2018. Progress and Prospects of the Human–Robot Collaboration. _Autonomous Robots_ 42, 5 (2018), 957–975. doi:10. 1007/s10514-017-9677-2 

- [6] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. 2022. Flamingo: a Visual Language Model for Few-Shot Learning. In _Advances in Neural Information Processing Systems_ , S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (Eds.), Vol. 35. Curran Associates, Inc., 23716– 23736. 

- [7] Fatima Batool, Muhammad Zafar, Yasheerah Yaqoot, R. A. Khan, M. H. Khan, Alexey Fedoseev, and Dzmitry Tsetserukou. 2025. ImpedanceGPT: VLM-driven Impedance Control of Swarm of Mini-drones for Intelligent Navigation in Dynamic Environment. In _Proc. of the IEEE/RSJ Int. Conf. on Intelligent Robots and Systems (IROS)_ . Hangzhou, China, 2592–2597. 

- [8] A. Bicchi and V. Kumar. 2000. Robotic grasping and contact: a review. In _Proc. IEEE Int. Conf. on Robotics and Automation. Symposia Proceedings (Cat. No.00CH37065)_ , Vol. 1. 348–353 vol.1. doi:10.1109/ROBOT.2000.844081 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, et al. 2023. _RT-1: Robotics Transformer for Real-World Control at Scale_ . arXiv:2212.06817 Retrieved from https://arxiv.org/abs/2212.06817. 

- [10] Jensen Gao, Bidipta Sarkar, Fei Xia, Ted Xiao, Jiajun Wu, Brian Ichter, Anirudha Majumdar, and Dorsa Sadigh. 2024. Physically Grounded Vision–Language Models for Robotic Manipulation. _Proc. of the IEEE Int. Conf. on Robotics and Automation (ICRA)_ 2024 (2024), 12462–12469. doi:10.1109/ICRA57147.2024.10610090 

- [11] K. Fidele Gbagbe, Miguel Altamirano Cabrera, Ahmed Alabbas, Omar Alyounes, Alexey Lykov, and Dzmitry Tsetserukou. 2024. Bi-VLA: Vision-Language-Action Model-Based System for Bimanual Robotic Dexterous Manipulations. In _Proc. of_ 

_the IEEE Int. Conf. on Systems, Man, and Cybernetics (SMC)_ . Sarawak, Malaysia, 2864–2869. 

- [12] Neville Hogan. 1985. Impedance Control: An Approach to Manipulation: Part I—Theory. _Journal of Dynamic Systems, Measurement, and Control_ 107, 1 (1985), 1–7. doi:10.1115/1.3140702 

- [13] Hyeongyo Jeong, Haechan Lee, Changwon Kim, and Sungtae Shin. 2024. A Survey of Robot Intelligence with Large Language Models. _Applied Sciences_ 14, 19 (2024), 8868. doi:10.3390/app14198868 

- [14] Yuchen Ji, Zequn Zhang, Dunbing Tang, Yi Zheng, Changchun Liu, Zhen Zhao, and Xinghui Li. 2024. Foundation Models Assist in Human–Robot Collaboration Assembly. _Scientific Reports_ 14 (2024), 24828. doi:10.1038/s41598-024-75715-4 

- [15] Dingzhe Li, Yixiang Jin, Yuhao Sun, Yong A, Hongze Yu, Jun Shi, Xiaoshuai Hao, Peng Hao, Huaping Liu, Fuchun Sun, Jianwei Zhang, and Bin Fang. 2025. What Foundation Models Can Bring for Robot Learning in Manipulation: A Survey. _The International Journal of Robotics Research_ 36 (2025), 261–268. doi:10.1177/ 02783649251390579 

- [16] Dzmitry Tsetserukou, Naoki Kawakami, and Susumu Tachi. 2008. Obstacle avoidance control of humanoid robot arm through tactile interaction. In _Proc. of the IEEE-RAS Int. Conf. on Humanoid Robots_ . Daejeon, Korea, 379–384. 

- [17] Muhammad Zafar, R. A. Khan, Fatima Batool, Yasheerah Yaqoot, Zhi Guo, Mikhail Litvinov, Alexey Fedoseev, and Dzmitry Tsetserukou. 2025. SwarmVLM: VLMGuided Impedance Control for Autonomous Navigation of Heterogeneous Robots in Dynamic Warehousing. In _Proc. of the IEEE Int. Conf. on Robotics and Biomimetics (ROBIO)_ . Chengdu, China, 770–775. 

- [18] Heng Zhang, Wei-Hsing Huang, Gokhan Solak, and Arash Ajoudani. 2025. _OmniVIC: A Self-Improving Variable Impedance Controller with Vision–Language In-Context Learning for Safe Robotic Manipulation_ . doi:10.48550/arXiv.2510.17150 Retrieved from https://arxiv.org/abs/2510.17150. 

- [19] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. 2023. RT-2: Vision– Language–Action Models Transfer Web Knowledge to Robotic Control. _Proc. of the 7th Conf.on Robot Learning_ 229 (2023), 2165–2183. 

