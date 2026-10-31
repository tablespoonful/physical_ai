---
title: "HumanoidArena: Benchmarking Egocentric Hierarchical Whole-body Learning"
date: "2026-06-16"
authors: "Taowen Wang; Zikang Xie; Bin Yang; Yunheng Wang; Zizhao Yuan; Yuetong Fang"
url: https://arxiv.org/abs/2606.17833
pdf: https://arxiv.org/pdf/2606.17833
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.17833)** / [論文ページ](https://arxiv.org/abs/2606.17833)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **HUMANOIDARENA: Benchmarking Egocentric Hierarchical Whole-body Learning** 

**Taowen Wang**<sup>**1,***</sup> **, Zikang Xie**<sup>**1,***</sup> **, Bin Yang**<sup>**1,***</sup> **, Yunheng Wang**<sup>**1**</sup> **, Zizhao Yuan**<sup>**1**</sup> **, Yuetong Fang**<sup>1</sup> , **Yixiao Feng**<sup>1</sup> , **Yichi Wang**<sup>2</sup> , **Xingyu Chen**<sup>1</sup> , **Haodong Chen**<sup>3</sup> , **Qiwei Wu**<sup>1</sup> , **Weisheng Xu**<sup>1</sup> , **Lihan Chen**<sup>4</sup> , **Lusong Li**<sup>5</sup> , **Zecui Zeng**<sup>5</sup> , **Renjing Xu**<sup>1,†</sup> 

1The Hong Kong University of Science and Technology (Guangzhou), 

2Beijing University of Technology, 3Harbin Institute of Technology, Shenzhen, 

4Shenzhen MSU-BIT University, 5JD Explore Academy 

## **Abstract** 

Humanoid robots promise whole-body interaction in human-centered environments, but scalable policy learning remains difficult because task-level decision-making and whole-body dynamic execution are tightly coupled. A practical solution is hierarchical control, where a high-level policy predicts intermediate whole-body actions and low-level general motion trackers (GMTs) execute them as stable humanoid motion. However, existing benchmarks rarely evaluate the policy–tracker interface itself, leaving open whether intermediate whole-body actions are executable, robust under task distribution shifts, and transferable across different GMT backends. We introduce HUMANOIDARENA, a simulation-first benchmark for egocentric hierarchical whole-body learning. The benchmark formulates policy learning as a hierarchical decision making problem: a high-level policy converts egocentric vision, proprioception, and instructions into a compact whole-body action, which is subsequently executed by a low-level GMT. Instead of treating the legs as planar transport tools, HUMANOIDARENA emphasizes interactions where lower-body coordination is structurally necessary in task completion. We therefore design 7 leg-critical HOI/HSI tasks in which success requires foot placement, balance maintenance, posture adjustment, and whole-body reorientation. To further diagnose the hierarchical system, we evaluate policies from two complementary perspectives: perturbation-conditioned generalization and GMT-conditioned transfer. We benchmark representative imitation-learning and VLA-style policies under this shared interface. Experiments show that hierarchical control enables learned policies to solve diverse leg-critical interactions, but performance is strongly tracker-conditioned and _cross-GMT_ transfer remains fragile. These results position HUMANOIDARENA as a benchmark for studying transferable intermediate action representations and scalable egocentric whole-body policy learning. Code and data are available at: `https://humanoidarena.github.io` . 

## **1 Introduction** 

_“The body is our general medium for having a world.”_ 

_— Maurice Merleau-Ponty [1]_ 

A central goal of embodied intelligence is to build agents that can perceive, reason, and act in the physical world through their bodies [2]. Humanoid robots are a natural embodiment for human- 

> * Equal contribution. 

> † Corresponding author. 

Preprint. 

centered environments because their morphology aligns with spaces, objects, tools, and affordances designed around the human body. This alignment is most consequential in interaction tasks where the lower body is not merely a locomotion module that transports the hands to a workspace. Foot placement, support transitions, balance-aware posture, and whole-body reorientation can directly determine whether an object or scene interaction is feasible [3, 4, 5]. In such _leg-critical_ interaction settings, lower-body coordination is structurally involved in task completion rather than reducible to planar base motion. Evaluating humanoid intelligence under this setting requires policies that act through an integrated body under egocentric perception, rather than treating locomotion and manipulation as separable subproblems. 

This whole-body requirement exposes a central tension at the interface between task intent and dynamic realization. A high-level policy must produce actions that preserve task-relevant intent, such as which object or scene affordance to approach and what interaction to attempt, while the execution layer must realize these intentions as stable, coordinated motion on a high-DoF legged body under contact and viewpoint changes. This division suggests different learning regimes: visual and semantic policy learning benefits from scalable imitation learning [6, 7], whereas dynamics-level execution benefits from fast reactive controllers trained with dense physical feedback [8, 9, 10]. Recent hierarchical humanoid systems [11, 12] make this division operational by letting high-level egocentric policies specify task-directed whole-body intent and low-level trackers realize that intent as dynamically feasible motion. This hierarchy provides a powerful abstraction for scalable humanoid control, decoupling visual-semantic decision making from high-frequency whole-body stabilization while retaining an executable intermediate representation for coordinated behavior. 

Despite this progress, existing benchmarks do not yet provide a controlled setting for studying hierarchical humanoid whole-body learning. First, according to _interface_ , most systems evaluate an end-to-end control stack [13, 14] or a fixed action representation [11, 12], making it difficult to separate high-level policy learning from low-level execution behavior. Without an explicit policyfacing whole-body action space and GMT-conditioned execution layer, comparisons are easily confounded by controller design, tracker dynamics, and backend-specific failure modes. Second, for _task_ , many embodied and humanoid benchmarks emphasize locomotion [13], manipulation [15, 16], or specific task diversity [17], but do not center leg-critical interactions where lower-body coordination is structurally required for success. Third, for _evaluation_ , existing protocols rarely disentangle visual perception, semantic grounding, spatial execution, and tracker-induced deployment shifts within the same benchmark. As a result, task success under one controller and one distribution can obscure whether a policy has learned robust hierarchical whole-body behavior. 

To address this gap, we introduce HUMANOIDARENA, a simulation-first benchmark for egocentric hierarchical whole-body learning. For the _interface_ , HUMANOIDARENA makes the hierarchical decomposition explicit: high-level policies predict compact intermediate whole-body actions from egocentric observations, proprioception, and task instructions, while low-level GMTs execute these actions as dynamically feasible humanoid motions. For the _task_ design, the benchmark instantiates seven leg-critical Human-Object Interaction (HOI) / Human-Scene Interaction (HSI) tasks that require lower-limb participation as an essential part of interaction, rather than treating the legs merely as a navigation module. For _evaluation_ , HUMANOIDARENA defines controlled perturbation-conditioned evaluation protocols across visual, semantic, and execution shifts and further supports _in/crossGMT_ deployment to assess both policy robustness and policy–tracker compatibility. Together, these design choices establish HUMANOIDARENA as a principled benchmark for egocentric hierarchical whole-body humanoid learning. Specifically, we make the following contributions. 

❶ **Hierarchical benchmark formulation.** We introduce a shared hierarchical interface for egocentric humanoid whole-body learning, where high-level policies predict intermediate whole-body actions and low-level general motion trackers execute them as dynamically feasible motions. 

❷ **Leg-critical egocentric task suite and data pipeline.** We design seven leg-critical HOI/HSI tasks in which successful execution requires lower-body participation, balance maintenance, posture adjustment, and whole-body coordination. Built in simulation, our GMT-based teleoperation pipeline collects closed-loop egocentric demonstrations while supporting scalable task and scene variation, failure-rich exploration, and synchronized first-person and third-person observations. 

❸ **Controlled hierarchical evaluation protocols.** We introduce perturbation-conditioned evaluation protocols across visual, semantic, and execution shifts. Together with _in/cross-GMT_ deployment, 

2 


Figure 1: **Overview of HUMANOIDARENA.** The benchmark studies leg-critical HOI/HSI tasks where success requires coordinated perception, foot placement, balance, and whole-body motion. Within this hierarchical formulation, high-level policies predict intermediate whole-body actions from egocentric visual observations, task instructions, and proprioception, while low-level GMTs stabilize and track them into feasible humanoid motions. To evaluate this interface, perturbation-conditioned evaluation and GMT-conditioned evaluation diagnose task generalization, tracker-induced distribution shifts, and policy–tracker compatibility. 

these protocols make policy robustness and policy–tracker compatibility measurable under a shared intermediate whole-body action interface. 

❹ **Baselines and findings.** We benchmark representative imitation-learning and VLA-style policies across tasks, trackers, and perturbations. Our results show that GMT-based hierarchy enables learned policies to complete diverse leg-critical interactions, while performance remains sensitive to the choice of execution backend. This sensitivity highlights _cross-GMT_ transfer and transferable intermediate action representations as important open challenges for hierarchical whole-body learning. 

## **2 Related Work** 

**Egocentric Humanoid Whole-Body Interaction.** Recent advances in humanoid whole-body control have gradually transitioned from proprioceptive motion tracking toward perception-driven interaction. Prior arts [5, 18, 19] achieved significant milestones by reinforcement learning, and recent work has expanded into the field of underactuated object interaction [20]. To ensure perception accuracy, several approaches rely on external sensors [21, 22, 23], while egocentric perception has increasingly emerged for HOI [24, 25, 26, 27, 28, 29, 30]. In parallel, egocentric vision has also proven crucial for HSI, empowering humanoids to navigate various terrains [31, 32, 33, 34, 35, 36]. These works demonstrate impressive interaction capabilities, since they inherently couple visual perception, decision-making, and whole-body execution within one stack, making it difficult to evaluate the generalization of the learned intent across different execution backends. 

A second line of work makes the hierarchy explicit. TWIST2 [11] uses a general motion tracker as the execution layer for egocentric whole-body teleoperation and visuomotor policy learning, while SONIC [12] scales motion tracking into a general low-level controller that can interface with multiple input modalities. Other humanoid VLA and whole-body policy systems instantiate the high-level/low-level split through different intermediate abstractions: motion generation followed by tracking [37, 38], latent vision-language verbs with RL whole-body skills [14], or VLA/action experts paired with specialized lower-body or whole-body controllers [39, 40, 41]. Together, these works mark a clear shift toward hierarchical whole-body learning, where high-level models handle 

3 

egocentric perception, language, and task intent, while low-level controllers maintain dynamic feasibility. However, hierarchical whole-body learning still lacks a dedicated benchmark. Existing systems vary in tasks, data, action spaces, and GMT backends, making it difficult to evaluate highlevel policies under a shared policy–tracker interface. HUMANOIDARENA fills this gap by turning egocentric hierarchical whole-body learning into a controlled benchmark. 

**Humanoid Benchmarks and Platforms.** Broader robot-learning benchmarks have greatly expanded task diversity and standardized evaluation. LIBERO [16] studies knowledge transfer in languageconditioned manipulation with 130 procedurally generated tasks, while BEHAVIOR-1K [15] scales household activity evaluation to 1,000 tasks in realistic simulation. However, they either rely on fixed-arm manipulation setups or abstract mobility into simplified navigation actions, leaving hierarchical whole-body control with humanoid full-body execution largely unstudied. A related line of work studies whole-body mobile manipulation beyond fixed-arm settings. BEHAVIOR Robot Suite [42] targets real-world household whole-body manipulation with a bimanual wheeled robot and a 4-DoF torso, emphasizing bimanual coordination, stable navigation, and end-effector reachability. AgentWorld [43] supports scalable scene construction and mobile manipulation data collection with both wheeled bases and humanoid locomotion policies. These platforms expand the scope of mobile manipulation, but their lower-body control is either wheeled or abstracted through locomotion/navigation interfaces, rather than evaluated through leg-critical humanoid execution under a GMT-based hierarchical interface. 

Furthermore, HumanoidBench [13] provides a high-dimensional simulated benchmark for humanoid locomotion and manipulation. LeVERB [14] introduces a sim-to-real-ready vision-language closedloop benchmark for humanoid whole-body control and a latent hierarchical policy, directly motivating the need for expressive high-level action interfaces. HumanoidVerse [17] studies egocentric languageguided multi-object rearrangement across 350 tasks, while Humanoid Everyday [44] contributes a large real-world humanoid manipulation dataset with multimodal sensing and cloud-based evaluation. Although these resources substantially advance humanoid whole-body learning, they do not explicitly benchmark GMT-based hierarchical control. HUMANOIDARENA complements them by making the policy–tracker interface itself a benchmark axis, enabling systematic evaluation of high-level policies across task-relevant perception, grounding, spatial execution, and tracker-induced deployment shifts. 

## **3 HUMANOIDARENA** 

This section introduces HUMANOIDARENA by first outlining the research topics that motivate its design (Sec. 3.1). We then instantiate these topics through four benchmark components: a hierarchical whole-body protocol that couples high-level policies with low-level general motion trackers (Sec. 3.2), a closed-loop egocentric data collection pipeline for multi-GMT demonstrations (Sec. 3.3), leg-critical HOI/HSI task suites (Sec. 3.4), and evaluation protocols for perturbation-conditioned and GMTconditioned generalization (Sec. 3.5). 

### **3.1 Research Topics in HumanoidArena** 

**(T1) Goal-directed hierarchical humanoid interaction.** Humanoid robots are expected to accomplish goals through coordinated whole-body interaction rather than isolated locomotion or manipulation. In leg-critical HOI/HSI tasks, success may depend on foot placement, balance-aware posture adjustment, whole-body reorientation, and coordinated arm–leg motion. HUMANOIDARENA provides a hierarchical setting in which a high-level policy predicts intermediate whole-body actions from egocentric observations and task instructions, while a low-level general motion tracker executes them into dynamically feasible motion. 

**(T2) Robust policy learning with egocentric perception.** A key question is how robust policies remain when task execution depends on egocentric visual observations. HUMANOIDARENA enables this study through three controlled generalization dimensions, visual, semantic, and execution, which test robustness to lighting changes, similar distractors, and various object initializations. 

**(T3)** **_Cross-GMT_ generalization in hierarchical control.** Hierarchical control raises the question of how policy outputs change when executed by different low-level general motion trackers. Through a shared intermediate whole-body action interface, HUMANOIDARENA offers a _cross-GMT_ testbed where policies can be trained with one tracker and deployed with another, directly evaluating whether intermediate actions remain valid across different GMTs. 

4 

**(T4) Multimodal coordination under whole-body motion.** Humanoid perception is tightly coupled with body motion. Unlike stationary-arm manipulation, humanoid egocentric and wrist cameras can undergo drastic viewpoint changes due to walking, arm swing, torso rotation, squatting, balance recovery, and contact-rich interaction. HUMANOIDARENA enables research on multimodal fusion and visual–proprioceptive alignment under rapidly changing egocentric viewpoints. 

### **3.2 Hierarchical Whole-Body Protocol** 

HUMANOIDARENA adopts a hierarchical whole-body control protocol that separates perceptionconditioned decision making from low-level dynamic execution. At time step _t_ , a high-level policy receives an egocentric observation _It_<sup>ego</sup> , proprioception _pt_ , and a task instruction _ℓ_ . The proprioception _pt_ consists of the root orientation in 6D rotation representation, the 29D G1 joint positions, and their corresponding joint velocities. Then the high-level policy predicts a 40D intermediate whole-body action _ut ∈_ R<sup>40</sup> . This action specifies root movement in the horizontal plane, root height, root orientation, 29D body joint targets, and binary open/close commands for both hands. This action serves as a tracker-compatible interface that specifies the intended whole-body motion to be executed. A low-level GMT then tracks this action and converts it into dynamically feasible humanoid motion. This separation allows HUMANOIDARENA to evaluate not only task success, but also the tracker robustness of intermediate whole-body actions under different GMT backends. 

**High-level policy baselines.** The high-level policy _πθ_ is the main learning component evaluated in HUMANOIDARENA. At each policy step, it receives egocentric visual observations, task instructions, and a 64D canonical proprioceptive state, and predicts a 40D intermediate whole-body action: 


We benchmark _πθ_ with four representative visuomotor policy families: ACT [45], Diffusion Policy [46], Flow Matching [47], and _π_ 0 _._ 5 [7], covering chunked action prediction, diffusion-based modeling, multi-step action prediction, and VLA-style instruction-conditioned policy learning. Since high-dimensional action spaces substantially increase learning complexity, we adopt a compact 40D canonical action interface instead of an SMPL-based action representation. This interface still requires policies to predict coordinated whole-body actions over the root, torso, arms, legs, and hands under egocentric perception, while keeping the action space tractable for systematic baseline evaluation. All baselines share the same observation space, action interface, and GMT backends, so performance differences primarily reflect policy design rather than changes in the execution interface. 

**Low-level general motion tracker bank.** The low-level layer contains a bank of GMTs that execute the canonical whole-body action predicted by the high-level policy. Since each GMT follows its own input protocol, _ut_ is first mapped by a GMT-specific adapter _ψm_ before being passed to GMT _G_<sup>(</sup><sup>_m_)</sup> : 


where _qt_<sup>(</sup> +1<sup>_m_)is the G1 joint-position target produced by the</sup><sup>_m_-th GMT. The adapter</sup><sup>_ψm_implements</sup> the required conversion from the canonical action space to the tracker-specific reference format. After this conversion, each GMT applies its own tracking policy to produce executable joint targets. Since trackers differ in motion priors, stabilization strategies, and failure modes, this bank enables evaluation of tracker robustness under a shared high-level interface. 

### **3.3 Data Collection Pipeline** 

HUMANOIDARENA collects data in Isaac Lab [48] through a VR-based egocentric teleoperation pipeline, where the operator receives the humanoid’s egocentric visual stream and controls the robot in closed loop via GMR [49, 50]. The retargeted robot reference motion is canonicalized into the policyfacing action form defined in Section 3.2, and then executed by a selected GMT. Under the same teleoperation and action interface, switching the GMT backend yields multi-GMT data with shared policy-facing action semantics but different low-level tracking dynamics. In our implementation, to reduce retargeting errors caused by height variation across operators, both backends are conditioned on robot reference motions: TWIST2 [11] adopts a mimic-style tracking command, while SONIC [12], which supports multiple conditioning interfaces, is used in its robot motion encoder mode rather than its human motion encoder mode. The full data specification is provided in Appendix B. 

5 

### **3.4 Leg-Critical Egocentric Task Suites** 

HUMANOIDARENA focuses on leg-critical egocentric tasks, by which we refer to HOI/HSI settings where lower-body coordination is directly involved in task completion rather than serving only as planar transport for the upper body. In contrast to mobile-base manipulation settings, these tasks require the policy to predict intermediate whole-body actions that jointly coordinate root motion, body posture, legs, arms, and hands. Detailed task design, including layouts, initialization ranges, success conditions, and the lower-body requirements of each task, is provided in Appendix A. 

The **HOI** tasks test how legged motion changes object interaction. HOI-DOUBLEDESK couples crosssurface object transfer with terrain-aware stepping across a height discontinuity. HOI-FOOTBALL evaluates coordinated leg-object interaction, where success depends on visual localization, balance, and kicking motion. HOI-P&PBOX tests leg-assisted high placement, requiring the robot to bend its legs and adjust whole-body posture to reach the target shelf height. 

The **HSI** tasks test how to interact with scenes. HSI-VISNAVI evaluates obstacle-aware egocentric navigation in constrained space. HSI-OPENDOOR couples handle manipulation with body turning and doorway traversal. HSI-SITSOFA requires obstacle avoidance, body alignment, and a stable sitting transition. HSI-BOXING evaluates height-adaptive striking, where low targets require crouching and whole-body adjustment. Together, these HOI and HSI tasks probe complementary forms of leg-critical interaction, from terrain-aware object transfer to posture-dependent scene interaction. 

### **3.5 Evaluation Protocols** 

**Perturbation-conditioned evaluation.** HUMANOIDARENA defines three perturbation axes for diagnosing policy generalization: _visual_ , _semantic_ , and _execution_ . These axes are designed to isolate failures in scene perception, target grounding, and whole-body execution, respectively. _Visual generalization_ changes the lighting direction while preserving the goal and object identity, testing robustness to egocentric appearance shifts. _Semantic generalization_ introduces semantically similar distractors under the same instruction, testing whether the policy grounds the commanded target. _Execution generalization_ expands the initialization range of task-relevant objects, requiring policies to adapt foot placement, body pose, and whole-body motion to new spatial conditions. Full perturbation configurations and rollout seeds are detailed in Appendix D. 

**GMT-conditioned evaluation.** Enabled by the shared whole-body action interface defined in Section 3.2, HUMANOIDARENA introduces GMT-conditioned protocols for evaluating policy–tracker compatibility. This design allows the same policy-facing action space to be executed by different low-level GMT backends, making _cross-GMT_ transfer a measurable property rather than an implementation detail. In the _in-GMT_ protocol, training and inference use the same GMT, measuring performance under matched tracking dynamics. In the _cross-GMT_ protocol, policies are trained with one GMT and deployed with another, testing whether the learned intermediate actions encode tracker-transferable whole-body intent or overfit to the motion priors, behavior, and failure modes of a single GMT. Together, these protocols assess _cross-GMT_ transfer of intermediate whole-body actions and reveal compatibility failures that are hidden under standard matched-backend evaluation. 

## **4 Experiments** 

In this section, we conduct experiments as an initial study of the proposed benchmark setting and hierarchical control formulation. We first introduce the evaluation protocols and then analyse empirical results across tasks, trackers, and generalization settings. Our experiments focus on the following research questions: 

- **Q1:** How well do existing imitation-learning and VLA-style policy baselines perform on legcritical egocentric HOI/HSI tasks? 

- **Q2:** How robust are different policy models under visual, semantic, and execution perturbations? 

- **Q3:** How do high-level policies trained on demonstrations collected with a single GMT perform when deployed with different GMT backends? 

### **4.1 Experimental Setup** 

**Evaluation matrix.** We evaluate policies across task categories, GMT backends, policy architectures, and perturbations. The task suite contains leg-critical HOI and HSI tasks introduced in Section 3.4; 

6 


Figure 2: **Qualitative rollouts.** We visualize four representative successful episodes generated by Diffusion Policy with SONIC as the low-level GMT. The examples cover both HOI and HSI tasks, showing that the high-level policy can coordinate egocentric perception, task interaction, foot placement, and whole-body motion through the shared GMT-based execution interface. 

we report both category-level performance and the overall average. For each task, all methods use the same demonstration split and are evaluated on the same held-out initializations. Each experimental configuration is evaluated with 3 random seeds and 20 rollout trials per seed, resulting in 60 rollouts per configuration. To study robustness beyond the in-distribution setting, we evaluate on the visual, semantic, and execution generalization splits defined in Section 3.5. 

**Policy instantiations and training.** We instantiate the high-level policy with four representative policy families: ACT [45], Diffusion Policy (DP, [46]), Flow Matching (FM, [47]), and _π_ 0 _._ 5 [7]. All policies receive the same egocentric RGB observation, proprioceptive state, and task instruction, and predict the same 40D intermediate whole-body action. This keeps the observation space, action interface, and GMT execution layer fixed, so that performance differences primarily reflect policy design rather than changes in the control interface. For fair comparison, all policies are trained with the same number of demonstrations per task and the same total training budget of 100k gradient steps. Model-specific training details are provided in Appendix F. 

**GMT deployment protocols.** We evaluate each policy under multiple GMT deployment settings. In the _in-GMT_ protocol, training and inference use the same GMT, measuring standard task performance under a matched data-collection and GMT backend. In the _cross-GMT_ protocol, policies are trained on demonstrations collected with one GMT and deployed with another, measuring whether the learned high-level policy and intermediate action representation transfer across GMT backends. 

**Metrics.** We utilize success rate (SR) as the primary metric across all tasks and evaluation protocols. For cross-GMT evaluation, we report the absolute cross-GMT drop ∆cross = SRin _−_ SRcross and relative transfer retention Ret = SRcross _/_ SRin, where SRin is the matched in-GMT success rate and SRcross is the success rate after replacing the deployment GMT. For visual, semantic, and execution generalization, we report success rate on each held-out split together with the relative performance drop from the in-distribution split. In addition to task completion, we report average fall rate (AFR) as a key stability metric, since successful humanoid interaction requires not only reaching task goals but also maintaining balance and dynamically feasible whole-body motion throughout execution. 

**Implementation and reproducibility.** To ensure that comparisons reflect policy design rather than evaluation artifacts, all methods are evaluated with identical rollout seeds, held-out object configurations, and initial robot states. All policies share the same visual preprocessing, canonical proprioceptive input, and intermediate whole-body action interface. Detailed training and deployment settings, including policy frequency, GMT control frequency, action chunking, optimization hyperparameters, and compute resources, are provided in Appendix F. 

7 

Table 1: **_In-GMT_ evaluation.** We evaluate high-level policy baselines with matched training and inference GMTs, using TWIST2 or SONIC as the low-level execution backend. Results are reported as success rate (SR, _↑_ ; mean _±_ standard deviation). AVG denotes the average SR within each HOI or HSI task suite. The best and second-best AVG are highlighted in **bold** and underlined, respectively. 

|i||||H|OI||||HSI|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Difficulty|Method|AFR (_↓_)|FOOTBALL|DOUBLEDESK|P&PBOX|AVG(_↑_)|OPENDOOR|SITSOFA|BOXING|VISNAVI|AVG (_↑_)|
||ACT [45]|6.43%|26.7_±_6.2%|15.0_±_8.2%|43.3_±_8.5%|28.33_±_13.94%|50.0_±_4.1%|66.7_±_10.3%|58.3_±_10.3%|13.3_±_4.7%|47.08_±_21.84%|
|TWIST2|DP [46]<br>FM [47]|10.48%<br>7.38%|46.7_±_6.2%<br>53.3_±_8.5%|10.0_±_4.1%<br>16.7_±_8.5%|50.0_±_0.0%<br>38.3_±_8.5%|35.56_±_18.63%<br>**36.11**_±_**17.28%**|68.3_±_6.2%<br>76.7_±_2.4%|73.3_±_6.2%<br>68.3_±_6.2%|51.7_±_11.8%<br>63.3_±_9.4%|30.0_±_4.1%<br>26.7_±_20.9%|55.83_±_18.58%<br>**58.75**_±_**22.56%**|
||_π_0_._5[7]|3.33%|26.7_±_4.7%|1.7_±_2.4%|46.7_±_8.5%|25.00_±_19.29%|28.3_±_9.4%|60.0_±_4.1%|51.7_±_8.5%|13.3_±_8.5%|38.33_±_20.14%|
||ACT [45]|8.57%|16.7_±_6.2%|18.3_±_4.7%|56.7_±_6.2%|30.56_±_19.36%|78.3_±_9.4%|73.3_±_8.5%|56.7_±_6.2%|33.3_±_2.4%|60.42_±_18.98%|
|SONIC|DP [46]|8.33%|45.0_±_10.8%|36.7_±_4.7%|75.0_±_4.1%|**52.22**_±_**17.97%**|85.0_±_10.8%|78.3_±_14.3%|76.7_±_2.4%|23.3_±_6.2%|**65.83**_±_**26.52%**|
||FM [47]|5.71%|13.3_±_2.4%|38.3_±_4.7%|73.3_±_6.2%|41.67_±_25.06%|70.0_±_4.1%|15.0_±_7.1%|70.0_±_8.2%|38.3_±_14.3%|48.33_±_24.94%|
||_π_0_._5[7]|5.24%|10.0_±_4.1%|43.3_±_6.2%|71.7_±_11.8%|41.67_±_26.46%|66.7_±_6.2%|73.3_±_2.4%|70.0_±_0.0%|23.3_±_6.2%|58.33_±_20.85%|


### **4.2 Main Results** 

**_In-GMT_ evaluation.** Table 1 evaluates high-level policy baselines under matched training and inference GMTs. Overall, the results show that existing egocentric policies can complete leg-critical HOI/HSI tasks with GMT-based execution, while performance varies substantially across policy architectures and tracker backends. Under TWIST2, FM [47] achieves the best suite averages on both HOI and HSI, reaching 36.11% and 58.75%, respectively. Under SONIC, DP [46] becomes the strongest baseline on both suites, reaching 52.22% on HOI and 65.83% on HSI. Notably, _π_ 0 _._ 5 achieves the best result on DoubleDesk under SONIC, reaching 43.3% SR. This may benefit from its manipulation-oriented pretraining, since DoubleDesk involves hand-centric grasping, carrying, and placing. However, this advantage is less evident on tasks dominated by whole-body motion, where success depends on foot placement, balance, and coordinated body execution. Comparing the best results under each tracker, SONIC outperforms TWIST2 on both HOI and HSI, improving the best average SR by 16.11% and 7.08%, respectively. These results suggest that performance should be interpreted as a property of the policy–tracker pair rather than the high-level policy alone. Beyond SR, AFR provides an important safety-oriented view: _π_ 0 _._ 5 [7] achieves the lowest AFR under both TWIST2 and SONIC in the in-GMT setting, making it the most stable baseline. This highlights the need to evaluate both interaction success and physical stability in humanoid benchmarks. 

**_Finding 1: In-GMT_ performance is feasible but tracker-conditioned.** The same policy family can behave differently when paired with different GMTs, and the best policy under one tracker is not always the best under another. This supports the benchmark design choice of treating the general motion tracker as a first-class evaluation axis rather than a hidden low-level controller. 


Figure 3: **Perturbation-conditioned evaluation.** We report suite-level average success rates under the in-distribution, visual, semantic, and execution settings. Each curve denotes one high-level policy, characterizing how different policy architectures degrade under the three benchmark-defined sources of perturbation with matched GMT execution. 

**Perturbation-conditioned evaluation.** Figure 3 summarizes _in-GMT_ robustness using average SR under the visual, semantic, and execution settings. Overall, SR often decreases under perturbation, especially under visual shifts, but the degradation patterns are not uniform across policies and tracker backends. Visual perturbations produce the most consistent drop, especially on HOI; for example, under TWIST2-HOI, ACT [45] drops from 28.33% to 14.44% and FM from 36.11% to 18.33%. DP [46] shows the most consistent profile in SONIC settings, remaining strongest on HSI across all perturbation splits and on HOI except the semantic split, where _π_ 0 _._ 5 achieves the highest HOI average. These results show that visual, semantic, and execution perturbations expose different failure modes rather than a single notion of robustness, motivating evaluation of egocentric appearance robustness, 

8 

Table 2: **_Cross-GMT_ evaluation.** T _→_ S denotes policies trained on TWIST2 demonstrations and deployed with the SONIC backend, while S _→_ T denotes the reverse direction. Each policy entry reports absolute _cross-GMT_ drop ∆cross ( _↓_ ) / relative transfer retention Ret ( _↑_ ), computed with respect to the corresponding matched in-GMT performance. AFR ( _↓_ ) denotes the task-level average fall rate under each _cross-GMT_ deployment direction, measuring tracker-induced stability failures. 

|Task Type|Task||TWI|ST2_→_SONIC||||SONI|C_→_TWIST2|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||ACT [45]|DP [46]|FM [47]|_π_0_._5 [7]|AFR (_↓_)|ACT [45]|DP [46]|FM [47]|_π_0_._5 [7]|AFR (_↓_)|
||FOOTBALL|26.70 / 0.00%|25.00 / 46.47%|46.60 / 12.57%|26.70 / 0.00%|1.25%|16.70 / 0.00%|43.30 / 3.78%|11.60 / 12.78%|10.00 / 0.00%|7.08%|
|HOI|DOUBLEDESK|15.00 / 0.00%|10.00 / 0.00%|16.70 / 0.00%|1.70 / 0.00%|2.90%|18.30 / 0.00%|36.70 / 0.00%|38.30 / 0.00%|41.60 / 3.93%|32.08%|
||P&PBOX|43.30 / 0.00%|50.00 / 0.00%|38.30 / 0.00%|46.70 / 0.00%|0.00%|31.70 / 44.09%|48.30 / 35.60%|45.00 / 38.61%|21.70 / 69.74%|0.40%|
||OPENDOOR|50.00 / 0.00%|68.30 / 0.00%|75.00 / 2.22%|28.30 / 0.00%|0.00%|78.30 / 0.00%|81.70 / 3.88%|63.30 / 9.57%|51.70 / 22.49%|0.00%|
|HSI|SITSOFA|66.70 / 0.00%|73.30 / 0.00%|68.30 / 0.00%|60.00 / 0.00%|0.40%|45.00 / 38.61%|60.00 / 23.37%|1.00 / 93.33%|68.30 / 6.82%|1.65%|
||BOXING|58.30 / 0.00%|50.00 / 3.29%|55.00 / 13.11%|51.70 / 0.00%|2.50%|23.40 / 58.73%|31.70 / 58.67%|11.70 / 83.29%|15.00 / 78.57%|0.00%|
||VISNAVI|13.30 / 0.00%|13.30 / 55.67%|26.70 / 0.00%|13.30 / 0.00%|2.48%|33.30 / 0.00%|23.30 / 0.00%|35.00 / 8.62%|23.30 / 0.00%|11.68%|


target grounding, and spatial adaptation of whole-body actions. Full per-task results are provided in Appendix I. 

**_Cross-GMT_ evaluation.** Table 2 evaluates whether intermediate whole-body actions remain transferable when replacing the deployment GMT. Each policy entry reports ∆cross ( _↓_ ) / Ret ( _↑_ ), so the two metrics should be interpreted jointly. Overall, tracker replacement causes substantial degradation in both directions: TWIST2 _→_ SONIC has a slightly larger average drop than SONIC _→_ TWIST2 (39.9% vs. 36.0%), and it produces more zero-retention entries. For example, on Football, TWIST2 _→_ SONIC yields drops ranging from 25.0% to 46.6%, whereas SONIC _→_ TWIST2 ranges from 10.0% to 43.3% with low retention values of 0.0%–12.78%. This shows that smaller ∆cross does not necessarily indicate better transfer when matched-GMT performance is already low. Furthermore, AFR provides a complementary view of tracker-induced stability. SONIC _→_ TWIST2 has a higher average AFR than TWIST2 _→_ SONIC (7.56% vs. 1.36%), driven by instability on DoubleDesk (32.08%) and VisNavi (11.68%). In contrast, TWIST2 _→_ SONIC remains stable, with its highest AFR values on DoubleDesk (2.90%), Boxing (2.50%), and VisNavi (2.48%). However, the lower AFR of TWIST2 _→_ SONIC does not translate into improved task transfer, as retention remains low across tasks. 

**_Finding 2: Cross-GMT_ transfer is asymmetric and metric-dependent.** Replacing the deployment GMT causes substantial performance drops and low retention, but the two transfer directions differ in absolute drop, retention, and fall rate. This indicates that current high-level policies do not learn fully tracker-invariant intermediate intent by default; instead, they partially specialize to the dynamics and correction behavior of the demonstration tracker. 

**Qualitative Results.** Figure 2 presents successful Diffusion Policy [46] rollouts on Football, DoubleDesk, SitSofa, and VisNavi. The examples show that the learned policy can generate temporally coherent intermediate whole-body actions that are executable by the low-level general motion tracker. In Football, the robot coordinates approach, stance adjustment, and leg swing to kick the ball; in DoubleDesk, it moves through constrained scene geometry while maintaining stable body orientation; in SitSofa, it aligns with the sofa and lowers its body into a seated posture; and in VisNavi, it uses egocentric observations to guide stepping and turning toward the goal region. Together, these cases illustrate that HUMANOIDARENA evaluates integrated perception, foot placement, balance, and whole-body interaction, rather than isolated manipulation or base navigation. We further provide failure case analysis in Appendix G. 

## **5 Conclusion** 

We presented HUMANOIDARENA, a simulation-first benchmark for egocentric hierarchical wholebody humanoid learning. Built around a shared policy–tracker interface, HUMANOIDARENA provides leg-critical HOI/HSI tasks, closed-loop multi-GMT demonstrations, and controlled evaluation protocols across visual, semantic, execution, _in-GMT_ , and _cross-GMT_ settings. Our experiments show that current policies can learn diverse whole-body interactions through GMT-based execution, but also reveal that performance depends strongly on the paired general motion tracker. In particular, cross-GMT evaluation exposes substantial and asymmetric transfer failures that are hidden under matched-backend evaluation. These findings highlight the need for intermediate whole-body action representations that are robust, tracker-transferable, and physically compatible with dynamic execution. We hope HUMANOIDARENA provides a common testbed for advancing egocentric humanoid policies that coordinate perception, task interaction, balance, and whole-body motion. 

9 

## **References** 

- [1] M. Merleau-Ponty and C. Smith. _Phenomenology of Perception_ . Motilal Banarsidass Publishers (Pvt. Limited), 1996. 

- [2] Rodney A. Brooks. Intelligence without representation. _Artificial Intelligence_ , 1991. 

- [3] Mike Stilman, Koichi Nishiwaki, and Satoshi Kagami. Humanoid teleoperation for whole body manipulation. In _ICRA_ , 2008. 

- [4] Júlia Borràs and Tamim Asfour. A whole-body pose taxonomy for loco-manipulation tasks. In _IROS_ , 2015. 

- [5] Lujie Yang, Xiaoyu Huang, Zhen Wu, Angjoo Kanazawa, Pieter Abbeel, Carmelo Sferrazza, C. Karen Liu, Rocky Duan, and Guanya Shi. Omniretarget: Interaction-preserving data generation for humanoid whole-body loco-manipulation and scene interaction. In _ICRA_ , 2026. 

- [6] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [7] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- [8] Qiayuan Liao, Takara E. Truong, Xiaoyu Huang, Yuman Gao, Guy Tevet, Koushil Sreenath, and C. Karen Liu. Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [9] Weiji Xie, Jinrui Han, Jiakun Zheng, Huanyu Li, Xinzhe Liu, Jiyuan Shi, Weinan Zhang, Chenjia Bai, and Xuelong Li. Kungfubot: Physics-based humanoid whole-body control for learning highly-dynamic skills. _arXiv preprint arXiv:2506.12851_ , 2025. 

- [10] Yunshen Wang, Shaohang Zhu, Peiyuan Zhi, Yuhan Li, Jiaxin Li, Yong-Lu Li, Yuchen Xiao, Xingxing Wang, Baoxiong Jia, and Siyuan Huang. Omnixtreme: Breaking the generality barrier in high-dynamic humanoid control. _arXiv preprint arXiv:2602.23843_ , 2026. 

- [11] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C. Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 

- [12] Zhengyi Luo, Ye Yuan, Tingwu Wang, Chenran Li, Sirui Chen, Fernando Castañeda, Zi-Ang Cao, Jiefeng Li, David Minor, Qingwei Ben, Xingye Da, Runyu Ding, Cyrus Hogg, Lina Song, Edy Lim, Eugene Jeong, Tairan He, Haoru Xue, Wenli Xiao, Zi Wang, Simon Yuen, Jan Kautz, Yan Chang, Umar Iqbal, Linxi Fan, and Yuke Zhu. Sonic: Supersizing motion tracking for natural humanoid whole-body control. _arXiv preprint arXiv:2511.07820_ , 2025. 

- [13] Carmelo Sferrazza, Dun-Ming Huang, Xingyu Lin, Youngwoon Lee, and Pieter Abbeel. Humanoidbench: Simulated humanoid benchmark for whole-body locomotion and manipulation. _arXiv preprint arXiv:2403.10506_ , 2024. 

- [14] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, and Shankar Sastry. Leverb: Humanoid whole-body control with latent vision-language instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

10 

- [15] Chengshu Li, Ruohan Zhang, Josiah Wong, Cem Gokmen, Sanjana Srivastava, Roberto MartínMartín, Chen Wang, Gabrael Levine, Michael Lingelbach, Jiankai Sun, Mona Anvari, Minjune Hwang, Manasi Sharma, Arman Aydin, Dhruva Bansal, Samuel Hunter, Kyu-Young Kim, Alan Lou, Caleb R Matthews, Ivan Villa-Renteria, Jerry Huayang Tang, Claire Tang, Fei Xia, Silvio Savarese, Hyowon Gweon, Karen Liu, Jiajun Wu, and Li Fei-Fei. BEHAVIOR-1k: A benchmark for embodied AI with 1,000 everyday activities and realistic simulation. In _CoRL_ , 2022. 

- [16] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- [17] Haozhuo Zhang, Jingkai Sun, Michele Caprio, Jian Tang, Shanghang Zhang, Qiang Zhang, and Wei Pan. Humanoidverse: A versatile humanoid for vision-language guided multi-object rearrangement. _arXiv preprint arXiv:2508.16943v1_ , 2025. 

- [18] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [19] Siheng Zhao, Yanjie Ze, Yue Wang, C. Karen Liu, Pieter Abbeel, Guanya Shi, and Rocky Duan. Resmimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [20] Dongting Li, Xingyu Chen, Qianyang Wu, Bo Chen, Sikai Wu, Hanyu Wu, Guoyao Zhang, Liang Li, Mingliang Zhou, Diyun Xiang, et al. Haic: Humanoid agile object interaction control via dynamics-aware world model. _arXiv preprint arXiv:2602.11758_ , 2026. 

- [21] Yinhuai Wang, Qihan Zhao, Yuen Fui Lau, Runyi Yu, Hok Wai Tsui, Qifeng Chen, Jingbo Wang, Jiangmiao Pang, and Ping Tan. Humanx: Toward agile and generalizable humanoid interaction skills from human videos. _arXiv preprint arXiv:2602.02473_ , 2026. 

- [22] Zhi Su, Bike Zhang, Nima Rahmanian, Yuman Gao, Qiayuan Liao, Caitlin Regan, Koushil Sreenath, and S Shankar Sastry. Hitter: A humanoid table tennis robot via hierarchical planning and learning. _arXiv preprint arXiv:2508.21043_ , 2025. 

- [23] Zhikai Zhang, Haofei Lu, Yunrui Lian, Ziqing Chen, Yun Liu, Chenghuai Lin, Han Xue, Zicheng Zeng, Zekun Qi, Shaolin Zheng, et al. Learning athletic humanoid tennis skills from imperfect human motion data. _arXiv preprint arXiv:2603.12686_ , 2026. 

- [24] Huayi Wang, Wentao Zhang, Runyi Yu, Tao Huang, Junli Ren, Feiyu Jia, Zirui Wang, Xiaojie Niu, Xiao Chen, Jiahe Chen, et al. Physhsi: Towards a real-world generalizable and natural humanoid-scene interaction system. _arXiv preprint arXiv:2510.11072_ , 2025. 

- [25] Shaofeng Yin, Yanjie Ze, Hong-Xing Yu, C Karen Liu, and Jiajun Wu. Visualmimic: Visual humanoid loco-manipulation via motion tracking and generation. _arXiv preprint arXiv:2509.20322_ , 2025. 

- [26] Tairan He, Zi Wang, Haoru Xue, Qingwei Ben, Zhengyi Luo, Wenli Xiao, Ye Yuan, Xingye Da, Fernando Castañeda, Shankar Sastry, et al. Viral: Visual sim-to-real at scale for humanoid loco-manipulation. _arXiv preprint arXiv:2511.15200_ , 2025. 

- [27] Yuhang Lin, Jiyuan Shi, Dewei Wang, Jipeng Kong, Yong Liu, Chenjia Bai, and Xuelong Li. Pro-hoi: Perceptive root-guided humanoid-object interaction. _arXiv preprint arXiv:2603.01126_ , 2026. 

- [28] Yutang Lin, Jieming Cui, Yixuan Li, Baoxiong Jia, Yixin Zhu, and Siyuan Huang. Lessmimic: Long-horizon humanoid interaction with unified distance field representations. _arXiv preprint arXiv:2602.21723_ , 2026. 

- [29] Xialin He, Sirui Xu, Xinyao Li, Runpei Dong, Liuyu Bian, Yu-Xiong Wang, and Liang-Yan Gui. Ultra: Unified multimodal control for autonomous humanoid whole-body loco-manipulation. _arXiv preprint arXiv:2603.03279_ , 2026. 

11 

- [30] Junli Ren, Yinghui Li, Kai Zhang, Penglin Fu, Haoran Jiang, Yixuan Pan, Guangjun Zeng, Tao Huang, Weizhong Guo, Peng Lu, et al. Smash: Mastering scalable whole-body skills for humanoid ping-pong with egocentric vision. _arXiv preprint arXiv:2604.01158_ , 2026. 

- [31] Nikita Rudin, Junzhe He, Joshua Aurand, and Marco Hutter. Parkour in the wild: Learning a general and extensible agile locomotion policy using multi-expert distillation and rl fine-tuning. _arXiv preprint arXiv:2505.11164_ , 2025. 

- [32] Hang Liu, Yuman Gao, Sangli Teng, Yufeng Chi, Yakun Sophia Shao, Zhongyu Li, Maani Ghaffari, and Koushil Sreenath. Ego-vision world model for humanoid contact planning. _arXiv preprint arXiv:2510.11682_ , 2025. 

- [33] Qingwei Ben, Botian Xu, Kailin Li, Feiyu Jia, Wentao Zhang, Jingping Wang, Jingbo Wang, Dahua Lin, and Jiangmiao Pang. Gallant: Voxel grid-based humanoid locomotion and localnavigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [34] Shaoting Zhu, Ziwen Zhuang, Mengjie Zhao, Kun-Ying Lee, and Hang Zhao. Hiking in the wild: A scalable perceptive parkour framework for humanoids. _arXiv preprint arXiv:2601.07718_ , 2026. 

- [35] Ziwen Zhuang, Shaoting Zhu, Mengjie Zhao, and Hang Zhao. Deep whole-body parkour. _arXiv preprint arXiv:2601.07701_ , 2026. 

- [36] Zhen Wu, Xiaoyu Huang, Lujie Yang, Yuanhang Zhang, Koushil Sreenath, Xi Chen, Pieter Abbeel, Rocky Duan, Angjoo Kanazawa, Carmelo Sferrazza, et al. Perceptive humanoid parkour: Chaining dynamic human skills via motion matching. _arXiv preprint arXiv:2602.15827_ , 2026. 

- [37] Haoran Yang, Jiacheng Bao, Yucheng Xin, Haoming Song, Yuyang Tian, Bin Zhao, Dong Wang, and Xuelong Li. Zerowbc: Learning natural visuomotor humanoid control directly from human egocentric video. _arXiv preprint arXiv:2603.09170_ , 2026. 

- [38] Weikai Qin, Sichen Wu, Ci Chen, Mengfan Liu, Linxi Feng, Xinru Cui, Haoqi Han, and Hesheng Wang. Physiflow: Physics-aware humanoid whole-body vla via multi-brain latent flow matching and robust tracking. _arXiv preprint arXiv:2603.05410_ , 2026. 

- [39] Pengxiang Ding, Jianfei Ma, Xinyang Tong, Binghong Zou, Xinxin Luo, Yiguo Fan, Ting Wang, Hongchao Lu, Panzhong Mo, Jinxin Liu, Yuefan Wang, Huaicheng Zhou, Wenshuo Feng, Jiacheng Liu, Siteng Huang, and Donglin Wang. Humanoid-vla: Towards universal humanoid control with visual integration. _arXiv preprint arXiv:2502.14795_ , 2025. 

- [40] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, and Hongyang Li. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- [41] Songlin Wei, Hongyi Jing, Boqian Li, Zhenyu Zhao, Jiageng Mao, Zhenhao Ni, Sicheng He, Jie Liu, Xiawei Liu, Kaidi Kang, Sheng Zang, Weiduo Yuan, Marco Pavone, Di Huang, and Yue Wang. _ψ_ 0: An open foundation model towards universal humanoid loco-manipulation. _arXiv preprint arXiv:2603.12263_ , 2026. 

- [42] Yunfan Jiang, Ruohan Zhang, Josiah Wong, Chen Wang, Yanjie Ze, Hang Yin, Cem Gokmen, Shuran Song, Jiajun Wu, and Li Fei-Fei. BEHAVIOR robot suite: Streamlining real-world whole-body manipulation for everyday household activities. In _CoRL_ , 2025. 

- [43] Yizheng Zhang, Zhenjun Yu, Jiaxin Lai, Cewu Lu, and Lei Han. Agentworld: An interactive simulation platform for scene construction and mobile robotic manipulation. In _CoRL_ , 2025. 

- [44] Zhenyu Zhao, Hongyi Jing, Xiawei Liu, Jiageng Mao, Abha Jha, Hanwen Yang, Rong Xue, Sergey Zakharov, Vitor Guizilini, and Yue Wang. Humanoid everyday: A comprehensive robotic dataset for open-world humanoid manipulation. _arXiv preprint arXiv:2510.08807_ , 2025. 

- [45] Tony Z. Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. In _RSS_ , 2023. 

12 

- [46] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _RSS_ , 2023. 

- [47] Boston Dynamics and TRI Research Team. Large behavior models and atlas find new footing, 2025. Blog post. 

- [48] Mayank Mittal, Pascal Roth, James Tigue, Antoine Richard, Octi Zhang, Peter Du, Antonio Serrano-Muñoz, Xinjie Yao, René Zurbrügg, Nikita Rudin, Lukasz Wawrzyniak, Milad Rakhsha, Alain Denzler, Eric Heiden, Ales Borovicka, Ossama Ahmed, Iretiayo Akinola, Abrar Anwar, Mark T. Carlson, Ji Yuan Feng, Animesh Garg, Renato Gasoto, Lionel Gulich, Yijie Guo, M. Gussert, Alex Hansen, Mihir Kulkarni, Chenran Li, Wei Liu, Viktor Makoviychuk, Grzegorz Malczyk, Hammad Mazhar, Masoud Moghani, Adithyavairavan Murali, Michael Noseworthy, Alexander Poddubny, Nathan Ratliff, Welf Rehberg, Clemens Schwarke, Ritvik Singh, James Latham Smith, Bingjie Tang, Ruchik Thaker, Matthew Trepte, Karl Van Wyk, Fangzhou Yu, Alex Millane, Vikram Ramasamy, Remo Steiner, Sangeeta Subramanian, Clemens Volk, CY Chen, Neel Jawale, Ashwin Varghese Kuruttukulam, Michael A. Lin, Ajay Mandlekar, Karsten Patzwaldt, John Welsh, Huihua Zhao, Fatima Anes, Jean-Francois Lafleche, Nicolas Moënne-Loccoz, Soowan Park, Rob Stepinski, Dirk Van Gelder, Chris Amevor, Jan Carius, Jumyung Chang, Anka He Chen, Pablo de Heras Ciechomski, Gilles Daviet, Mohammad Mohajerani, Julia von Muralt, Viktor Reutskyy, Michael Sauter, Simon Schirm, Eric L. Shi, Pierre Terdiman, Kenny Vilella, Tobias Widmer, Gordon Yeoman, Tiffany Chen, Sergey Grizan, Cathy Li, Lotus Li, Connor Smith, Rafael Wiltz, Kostas Alexis, Yan Chang, David Chu, Linxi "Jim" Fan, Farbod Farshidian, Ankur Handa, Spencer Huang, Marco Hutter, Yashraj Narang, Soha Pouya, Shiwei Sheng, Yuke Zhu, Miles Macklin, Adam Moravanszky, Philipp Reist, Yunrong Guo, David Hoeller, and Gavriel State. Isaac lab: A gpu-accelerated simulation framework for multi-modal robot learning. _arXiv preprint arXiv:2511.04831_ , 2025. 

- [49] Joao Pedro Araujo, Yanjie Ze, Pei Xu, Jiajun Wu, and C. Karen Liu. Retargeting matters: General motion retargeting for humanoid motion tracking. _arXiv preprint arXiv:2510.02252_ , 2025. 

- [50] Yanjie Ze, Zixuan Chen, João Pedro Araújo, Zi ang Cao, Xue Bin Peng, Jiajun Wu, and C. Karen Liu. Twist: Teleoperated whole-body imitation system. _arXiv preprint arXiv:2505.02833_ , 2025. 

13 

### **SUMMARY OF THE APPENDIX** 

This appendix contains additional experimental results and discussions of our work, organized as: 

- §A details the **leg-critical HOI/HSI task suite** , including task layouts, initialization ranges, success conditions, termination criteria, and why each task requires lower-body participation. 

- §B describes the **data collection pipeline and dataset specification** , including VR teleoperation, GMR retargeting, synchronized observations, episode format, data fields, train/test splits, and multi-GMT demonstration statistics. 

- §C explains the **intermediate whole-body action interface and GMT adapters** , covering the 40D canonical action, 64D proprioceptive state, tracker-specific mappings, and the SONIC/TWIST2 execution interfaces. 

- §D outlines the **evaluation protocol details** , including visual, semantic, and execution perturbation configurations, held-out splits, rollout seeds, _in/cross-GMT_ settings, and metric definitions. 

- §E provides **additional experimental analysis** , examining representative rollout behaviors across diverse HOI/HSI tasks. 

- §F provides **policy implementation and training details** , including ACT, Diffusion Policy, Flow Matching, and _π_ 0 _._ 5 hyperparameters, learning rates, batch sizes, action chunk lengths, inference horizons, preprocessing, training steps, and compute resources. 

- §G analyses **failure cases** , separating perception failures, semantic grounding failures, execution instability, fall cases, tracker incompatibility, and compounding errors under long-horizon wholebody interaction. 

- §H provides **reproducibility and release details** , including code structure, dataset format, environment setup, asset dependencies, random seeds, license information, and expected compute requirements. 

- §I presents **additional results** , including full per-task perturbation results for in-GMT evaluation and merge-all training analysis across TWIST2, SONIC, and combined GMT datasets. 

- §J discusses **limitations and future directions** . 

## **A Task Suite Specification** 

This section specifies the seven leg-critical egocentric tasks in HUMANOIDARENA, designed to evaluate whole-body robotic capabilities that require tight coordination between locomotion, perception, balance control, and task-oriented interaction. The task suite consists of three Human-Object Interaction (HOI) tasks and four Human-Scene Interaction (HSI) tasks. The HOI tasks include **Football** , where the robot kicks a soccer ball into a goal net; **DoubleDesk** , where it transfers a hammer from one desk to a basket on another desk; and **P&PBox** , where it picks up a box from a table and places it onto a shelf. The HSI tasks include **OpenDoor** , which requires opening an articulated door and passing through the doorway; **SitSofa** , which requires navigating to and sitting on a sofa; **Boxing** , which requires striking a randomized target mounted on a punching bag; and **VisNavi** , which requires visually navigating through obstacles and stepping into a target sign zone. Together, these tasks cover a diverse set of lower-body-dependent skills, including approach-and-kick motion, object transport during walking, articulated contact interaction, obstacle-aware navigation, precise foot placement, whole-body posture adjustment, and controlled sitting or striking behaviors. The task-specific success criteria, failure/termination conditions, and maximum episode lengths are summarized in Table S1. Each task is evaluated under a consistent protocol with 3 random seeds and 20 repeated trials per seed, resulting in 60 episodes for each model configuration. 

Table S1: Task-specific success and termination conditions. Fall detection uses a 60° torso tilt threshold, confirmed over 5 consecutive steps; an additional 75° hard-tilt condition or 50N body contact force with tilt triggers immediate termination. All tasks share a standing criterion of root height _≥_ 0.45m and torso up-axis alignment _≥_ 0.60. 

1 

|**Task**<br>|**Max Step**|**s**<br>||**Termin**<br>|**ation**<br>|**Success Condition**|
|---|---|---|---|---|---|---|
|||**Fall**|**Timeou**|**t**|**Note**||
|FOOTBALL|1300|✓|✓|Ball le  i|aves the field|Ball center crosses the goal<br>plane and remains within the<br>net bounds|
|DOUBLEDESK|2000|✓|✓|–||Hammer center of mass lies<br>inside the basket bounding box|
|P&PBOX|2000|✓|✓|Non-te|rminal box drop|Box rests on the shelf support<br>surface, with its center within<br>the support span|
|OPENDOOR|1800|✓|✓|–||Robot root passes through the<br>door-frame plane while<br>remaining upright|
|SITSOFA|1050|✓|✓|–||Pelvis or hip bodies maintain<br>stable contact with the sofa seat<br>surface|
|BOXING|1500|✓|✓|–||Hand reaches the dynamic hit<br>radius of the target|
|VISNAVI|1800|✓|✓|–||Both feet are inside the target<br>bounding box while the robot<br>remains upright|


Figure S1: Football successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 


Figure S2: DoubleDesk successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 


2 


Figure S3: P&PBox successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 


Figure S4: OpenDoor successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 


Figure S5: SitSofa successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 


Figure S6: Boxing successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 


3 


Figure S7: VisNavi successful rollout with 10 uniformly sampled frames shown in temporal order from left to right, top to bottom. 

**Football (HOI).** The robot must kick a soccer ball into a single goal net. The ball position is randomized within [ _−_ 1 _._ 2 _,_ 1 _._ 2] _×_ [ _−_ 1 _._ 2 _,_ 1 _._ 2]. The scene includes four backdrop walls and a kinematic goal net at 3.0m distance. The ball has physics properties (0.43kg mass, restitution 0.1). **Why leg-critical** : Kicking requires the robot to (i) visually locate the ball, (ii) approach and adjust its stance, (iii) balance on the support leg, and (iv) execute a coordinated leg swing with precise impact timing. Each sub-step depends on lower-body dynamics; a stationary-base policy cannot perform the approach-kick sequence. 

**DoubleDesk (HOI).** The robot operates between two desks, tasked with picking up a hammer and placing it into a basket. Both the hammer and basket positions are randomized: hammer within [ _−_ 3 _._ 2 _, −_ 2 _._ 4] _×_ [ _−_ 3 _._ 15 _, −_ 3 _._ 0] and basket within [ _−_ 3 _._ 6 _, −_ 2 _._ 0] _×_ [ _−_ 0 _._ 3 _, −_ 0 _._ 005] with yaw randomization. If the hammer falls to the ground, it is unrecoverable (training data does not contain ground-pickup demonstrations, and teleoperation-based ground retrieval exceeds current GMT capability boundaries), resulting in eventual timeout. **Why leg-critical** : The desktops are at standing height and spaced far enough apart that the robot must walk between the pickup and drop-off locations while carrying a grasped object. Whole-body coordination of locomotion, grasp stability, and target placement is essential; a fixed-station manipulator cannot cover the inter-desk distance. 

**P&PBox (HOI).** The robot picks up a box from a table and places it onto a shelving unit. Both the box and shelf positions are randomized. A dropped box does not cause immediate termination; the robot may attempt to recover if the box remains within reach. Success requires the box center to rest on a detected shelf support surface. **Why leg-critical** : The box pickup point (table) and placement target (shelf) are separated horizontally, requiring the robot to walk while holding the box. The shelf’s varied heights require the robot to adjust its stance and arm reach, combining locomotion with vertical manipulation. 

**OpenDoor (HSI).** The robot must approach and open an articulated door. The door position is randomized within a [ _−_ 0 _._ 754 _,_ 0 _._ 55] _×_ [ _−_ 0 _._ 8 _,_ 0 _._ 1] XY range. The door uses articulation physics with configured joint friction properties. Success requires the robot’s root to pass through the door frame plane ( _|x_ local _| ≤_ 0 _._ 55m, _y_ local _>_ 0 _._ 02m past the door) while maintaining an upright standing posture. **Why leg-critical** : Unlike fixed-base manipulation, successful door opening requires coordinated base placement, torso orientation, arm contact, and balance recovery under articulated contact forces. The robot must walk through the door while pushing, which demands lower-body locomotion integrated with upper-body manipulation. 

**SitSofa (HSI).** The robot navigates a living room environment and must sit on a sofa. Two carton obstacles are randomized in position as distractors. Success is determined when the robot’s pelvis or hip joint bodies make stable contact with the sofa seat surface. **Why leg-critical** : Success requires obstacle-aware navigation (lower body steers around cartons), precise body-to-sofa alignment (foot placement determines final seating position), and a controlled sitting transition that depends on coordinated leg flexion and torso rotation. A wheeled base cannot execute the sitting motion. 

**Boxing (HSI).** The robot stands before a punching bag and must strike a green spherical target mounted on the bag. The target’s position is randomized within a 0.15m radius cylinder around two predefined bag centers. Success is determined by the distance between the robot’s hand proxy links and the target center falling below a dynamic threshold computed from the asset’s bounding radius plus a hand-radius offset (0.08m). **Why leg-critical** : The target’s randomized height requires the robot to crouch for lower targets and reach high for elevated ones; arm-only motion is insufficient. The dynamic hit-distance threshold depends on the target’s world-space bounding box, meaning the 

4 

robot must coordinate whole-body posture to bring the hand near the target while maintaining balance on two feet. 

**VisNavi (HSI).** The robot must locate and walk into a target sign zone within a warehouse environment containing randomized obstacles. The target sign position is randomized with XY pose ranges, and six obstacles (two sets of three) are placed with configurable layout ranges. Success requires both feet to be within the target bounding box while the robot remains upright. **Why leg-critical** : The task demands egocentric visual navigation with lower-body steering through cluttered obstacle fields; foot placement accuracy directly determines whether both feet land inside the target zone. Static arm manipulation or a mobile-base abstraction cannot satisfy the dual-foot zone constraint. 

**Implementation Note.** To ensure reproducibility and maintain a consistent evaluation interface across tasks, HUMANOIDARENA adopts a modular task implementation. Task scenes and object layouts are specified under `tasks/common_scene/` , and environment configurations, including initialization ranges and task-level randomization settings, are defined under `tasks/common_env_config/` . The reward predicates and success/termination checks for each task are implemented in its corresponding `mdp/rewards.py` file. During evaluation, fall detection is handled uniformly in `script/eval_scripts/*/sim_eval_vla.py` , where a 60° torso-tilt threshold is treated as a soft fall condition after 5-frame confirmation, while a 75° hard-tilt threshold or a 50N body-contact force under tilt triggers immediate termination. 

## **B Data Collection Pipeline and Dataset Specification** 

This section describes the data collection pipeline and the resulting dataset specification. A core design principle of HUMANOIDARENA is that all demonstrations share a unified _policy-facing canonical action space_ (the 40D intermediate whole-body action defined in §C), while the low-level execution dynamics differ depending on which GMT executes the action. This separation allows the benchmark to study whether high-level policies learn reusable whole-body intent (via the shared action interface) or overfit to tracker-specific dynamics (via _cross-GMT_ evaluation). Switching the GMT backend under the same teleoperation interface yields multi-GMT datasets with identical policy-facing semantics but different tracking characteristics. 

### **B.1 Collection Pipeline** 

Human demonstrations are collected through a shared upstream teleoperation pipeline, followed by backend-specific action interpretation inside Isaac Lab: 

- **Shared capture and retargeting (both backends):** The operator receives the humanoid’s egocentric video stream via PICO headset. Human motion is captured and retargeted through GMR to produce a 35D robot-space reference signal ( `mimic_obs` ), which is published to Redis for real-time consumption. 

- **Backend-specific action interpretation:** Inside Isaac Lab, the 35D `mimic_obs` is consumed by a backend-specific action provider — `action_provider_wh_twist2` for the TWIST2 tracker, and `action_provider_sonic` for the SONIC tracker. Each provider interprets the shared 35D signal into executable G1 joint targets using its own policy (TWIST2: ONNX inference; SONIC: GEAR-SONIC encoder/decoder). The GMT then executes these targets in simulation. 

Within Isaac Lab, the action provider consumes poses from Redis, runs a pretrained policy, and drives the G1 humanoid robot. A `RecordingManager` buffers per-frame state and action data, serializing episodes into NPZ archives along with multi-camera RGB video. Teleoperation and data collection use a single egocentric front camera at 640 _×_ 480 resolution; the multi-camera and camera depth recordings are generated during data re-recording and are available for training and inference. The high-level policy outputs at 50Hz for both backends; GMT-specific decimation aligns both to the same 50Hz control frequency for fair _cross-GMT_ comparison. Data collection and teleoperation consistently operate at 50Hz. 

5 

### **B.2 Canonical State and Action Schema** 

All recorded demonstrations are normalized into the shared policy-facing interface defined in Appendix C. Specifically, each episode stores synchronized egocentric observations, a 64D canonical proprioceptive state, and a 40D intermediate whole-body action. The detailed state/action schema, coordinate conventions, canonical conversion procedure, and GMT-specific adapter mappings are described in Appendix C. 

### **B.3 Dataset Statistics** 

Each task provides 100 successful demonstration episodes per GMT backend (TWIST2 and SONIC), totaling 200 episodes per task and 1,400 episodes across all tasks. Although the total demonstration duration may be modest relative to large-scale video pretraining corpora, each episode contains dense 50Hz whole-body state-action supervision, synchronized egocentric observations, and closedloop GMT-executed humanoid behavior. The dataset is therefore intended primarily for controlled evaluation of hierarchical whole-body policies rather than large-scale pretraining. 

### **B.4 Dataset Format** 

Each recorded episode is stored as an NPZ archive containing per-frame arrays: front-camera RGB images (640 _×_ 480, with additional multi-camera views available from re-recording), 64D canonical state, and 40D canonical action. Unless otherwise specified, all reported benchmark results use the front egocentric camera as the policy visual input. The NPZ archives are converted to LeRobotcompatible format using the conversion pipeline described below. Training, validation, and test splits are held constant across all evaluated policies and GMT backends. Only successful demonstrations are included in the training set. 

### **B.5 Conversion Pipeline** 

Raw NPZ recordings are converted into LeRobot-compatible datasets using dedicated conversion tools. The canonical extraction helpers read existing canonical fields when available or reconstruct 64D state and 40D action from recorded joint arrays and root orientation. Cleaning tools filter invalid frames due to time discontinuities or held-action motion mismatches. A verification script cross-checks converted dataset rows against canonical arrays reconstructed from source recordings to detect conversion drift. 

For multi-camera datasets, re-recording tools replay NPZ episodes through Isaac Lab to generate additional viewpoint images. 

## **C Intermediate Whole-Body Action Interface and GMT Adapters** 

This appendix defines the policy-facing canonical interface used throughout HUMANOIDARENA. All high-level policies observe the same 64D proprioceptive state and predict the same 40D intermediate whole-body action, irrespective of which GMT executes the motion. 

Table S2: Canonical 64D state and 40D intermediate whole-body action representation. 

|COMPONENT|DIMS|DESCRIPTION|
|---|---|---|
|**Observation State**|**(64D)**||
|ROOT_ROT6D|6|ROOT ORIENTATION IN6D CONTINUOUS ROTATION|
|DOF_POS|29|JOINT POSITIONS FOR29-DOF WHOLE-BODYG1|
|DOF_VEL|29|JOINT VELOCITIES|
|**Intermediate Whol**|**e-Body**|**Action (40D)**|
|ROOT_XY_DELTA|2|ROOT TRANSLATION IN XY AXIS|
|ROOT_Z|1|ROOT-HEIGHT TARGET|
|ROOT_ROT6D|6|TARGET ROOT ORIENTATION IN6D CONTINUOUS ROTATION|
|JOINT_POS|29|TARGET JOINT POSITIONS|
|HAND_BINARY|2|LEFT/RIGHT HAND OPEN-CLOSE COMMANDS|


6 

The 40D action is intentionally structured: it encodes coordinated whole-body intent (root motion, joint targets, hands) while remaining compact enough for visuomotor policy learning. It delegates dynamic feasibility and fast stabilization to the low-level GMT rather than requiring the policy to predict torque-level commands. 

**Canonical conversion.** During demonstration collection and policy rollout, the reference signal from the teleoperation pipeline is normalized into the canonical interface. The conversion runs through `action_provider/vla_smpl_runtime.py` : • `build_vla_observation_state()` constructs the 64D proprioceptive state from root orientation, joint positions, and joint velocities. 

- `build_vla_action()` constructs the 40D intermediate action from root motion, orientation, joint targets, and hand commands. 

- `UnifiedSMPLActionRuntime` lifts tracker-specific or teleoperation-specific references into the shared canonical space when needed. 

With this conversion, policies trained on demonstrations collected with different GMTs observe and produce identical state and action formats. 

**GMT adapters.** Each GMT exposes a different execution interface. A GMT-specific adapter _ψm_ maps the canonical 40D action _ut_ into the reference format required by GMT _G_<sup>(</sup><sup>_m_)</sup> , producing executable G1 joint-position targets _qt_<sup>(</sup> +1<sup>_m_)=</sup><sup>_G_(</sup><sup>_m_)(</sup><sup>_ψm_(</sup><sup>_ut_)).The adapter changes only the action-</sup> to-tracker mapping; the high-level policy, observation space, and canonical action space remain unchanged across GMT backends. This design makes _in-GMT_ and _cross-GMT_ evaluation welldefined: _cross-GMT_ deployment replaces only the adapter and low-level tracker, while keeping the trained policy and its output space fixed. 

HUMANOIDARENA currently instantiates two GMT backends. The TWIST2 adapter maps the canonical 40D action into a mimic-style tracking command for TWIST2’s ONNX policy. The SONIC adapter maps the same 40D action into the reference format required by the SONIC execution stack, which uses a GEAR-SONIC encoder/decoder pair for tracking. Both backends consume the same upstream 35D `mimic_obs` signal produced by the shared GMR retargeting pipeline (§B), ensuring consistent canonical conversion and enabling fair _cross-GMT_ comparison. 

**Implementation Note.** The canonical runtime is implemented in `action_provider/vla_smpl_runtime.py` . The dataset-level conversion pipeline lives under `tools/data_tools/` , including `twist2lerobot_64_40.py` , `sonic2lerobot_64_40.py` , and shared helpers in `smpl_lerobot_common.py` . 

## **D Evaluation Protocols and Perturbation Design** 

This section specifies the evaluation protocol, the three perturbation axes used for robustness testing, the _in-GMT_ and _cross-GMT_ deployment protocols, and the complete evaluation coverage matrix. All protocols ensure that different policies and backends are compared under identical rollout seeds, held-out object configurations, and initial robot states. 

### **D.1 Evaluation Protocol** 

All models are evaluated under a consistent protocol: each model is tested with _N_ seeds = 3 random seeds, each seed running _N_ repeats = 20 repeated trials, totaling 60 episodes per configuration. The simulation uses persistent mode ( `persistent_sim = true` ) where the Isaac Lab environment is created once and reset between episodes. Episode seeds are derived deterministically as sha256(task_name _|_ group_seed _|_ repeat_idx). Success is defined as a binary reward: 1 if the taskspecific success condition is met (as defined in §A, Table S1), 0 otherwise. In addition to success rate, we report average fall rate (AFR) as a stability metric. 

7 

### **D.2** **_In-GMT_ and** **_Cross-GMT_ Evaluation** 

HUMANOIDARENA supports two GMT deployment protocols that test the generalization of learned high-level policies across execution backends: 

- **_In-GMT_ (matched)** : The high-level policy is trained on demonstrations collected and executed with GMT- _A_ and evaluated with the same GMT- _A_ . This measures standard task performance under a matched data-collection and execution backend. 

- **_Cross-GMT_ (transferred)** : The high-level policy is trained on GMT- _A_ demonstrations but deployed with GMT- _B_ . This measures whether the intermediate whole-body action representation transfers across execution backends. 

### **D.3 Test Modes** 

We define four test modes that systematically vary different axes of perturbation while keeping the evaluation protocol identical. Each perturbation axis is designed to change the target test variable without altering the task’s underlying semantics: 

Table S3: Four test settings and their perturbation dimensions 

|MODE|OBJECTPOSERANGE|ASSET|LIGHTING|
|---|---|---|---|
|BASETEST|TRAINING RANGE|ORIGINAL|DOMELIGHT(UNIFORM)|
|EXECUTIONTEST|**Expanded**|ORIGINAL|DOMELIGHT(UNIFORM)|
|SEMANTICTEST|TRAINING RANGE|**Replaced USD**|DOMELIGHT(UNIFORM)|
|VISUAL TEST|TRAINING RANGE|ORIGINAL|**DistantLight + random rotation**|


### **D.4 Execution Test: Expanded Pose Randomization** 

The execution test increases the randomization range of object positions beyond the training distribution. For each task, the `deterministic_object_resets[].pose_range` is widened in the execution YAML config relative to the base test. For example, the football task’s ball XY range expands from [ _−_ 1 _._ 2 _,_ 1 _._ 2] to [ _−_ 1 _._ 45 _,_ 1 _._ 45], and the door position expands from _x ∈_ [ _−_ 0 _._ 754 _,_ 0 _._ 55] to [ _−_ 0 _._ 9 _,_ 0 _._ 66]. All other parameters (control frequency, decimation, physics properties) remain identical to base test. 

### **D.5 Semantic Test: Asset Replacement** 

We use “semantic” in the benchmark sense of _semantics-preserving asset substitution_ : the task goal and affordance remain unchanged while the visual instance, shape, or distractor configuration varies. The test evaluates robustness to appearance, geometry, and scene-clutter variations by substituting specific scene assets with pre-built variant USD files. 

The semantic variants fall into three categories: (i) _geometry-preserving appearance variants_ where textures or colors are modified while geometry remains unchanged (OpenDoor door, Football goal net, SitSofa/DoubleDesk room walls); (ii) _affordance-preserving geometry variants_ where the object shape changes but the functional affordance and comparable physical extent are preserved (Boxing: green sphere _→_ green cube of equal bounding extent); (iii) _scene-clutter distractor variants_ where additional non-target objects are introduced to test robustness under scene clutter while preserving the target goal (P&PBox: distractor objects on the desk surface). 

Asset overrides are specified in YAML test configurations using the environment configuration loader. The loader traverses the config object hierarchy and sets the asset’s `usd_path` attribute. No code changes are required in the evaluation pipeline — semantic testing is purely configuration-driven. All YAML configs reside under `tasks/common_test_config/semantic/` . 

8 

Table S4: Semantic asset substitutions across the 7 tasks. 

|TASK|SCENEATTRIBUTE|SEMANTICVARIANT|
|---|---|---|
|FOOTBALL|`goal_net`|ORIGINAL GOAL_→_TEXTURE-MODIFIED GOAL|
|DOUBLEDESK|`room_walls`|ORIGINAL ROOM_→_TEXTURE-MODIFIED ROOM|
|P&PBOX|`room_walls`|ORIGINAL ROOM_→_ROOM WITH DISTRACTOR OBJECTS|
|OPENDOOR|`door`|ORIGINAL DOOR_→_TEXTURED VARIANT|
|SITSOFA|`room_walls`|ORIGINAL ROOM_→_TEXTURE-MODIFIED ROOM|
|BOXING|`boxing_target`|GREEN SPHERE_→_GREEN CUBE|
|VISNAVI|`target_sign`|WET FLOOR SIGN_→_SEMANTIC VARIANT|


### **D.6 Visual Test: Lighting Randomization** 

The visual test evaluates robustness to illumination variations. The default DomeLight (uniform ambient illumination) is replaced at runtime with a DistantLight (directional light source) whose pose and intensity are randomized per episode. 

- **Light Replacement** : After simulator initialization, the existing DomeLight prim at `/World/light` is deleted and a DistantLight is created with default parameters: position ( _−_ 4 _, −_ 1 _,_ 18), intensity 5000, angle 15<sup>_◦_</sup> , color (0 _._ 75 _,_ 0 _._ 75 _,_ 0 _._ 75). 

- **Per-Episode Randomization** : Before each episode reset, the DistantLight parameters are deterministically randomized using the episode seed: 

   - Rotation: pitch _∼U_ ( _−_ 20<sup>_◦_</sup> _,_ +20<sup>_◦_</sup> ), roll _∼U_ ( _−_ 20<sup>_◦_</sup> _,_ +20<sup>_◦_</sup> ), yaw fixed at 0<sup>_◦_</sup> . 

   - Intensity: _∼U_ (3000 _,_ 7000). 

   - Color: RGB each channel _∼U_ (0 _._ 65 _,_ 0 _._ 85). 

The DistantLight’s directional nature means that rotating the light changes shadow directions, highlight positions, and overall scene contrast, testing the model’s robustness to lighting variations without changing the physical task configuration. Implementation resides in `tools/augmentation_utils.py` (light replacement and randomization) and `tasks/common_runtime/env_runtime_hooks.py` (per-episode integration). 

Table S5: Evaluation matrix. ✓ = completed, N.E. = not evaluated for the listed mode. 

|CONFIGURATION|BASETEST|EXECUTION|SEMANTIC|VISUAL|
|---|---|---|---|---|
|IN-GMT TWIST2|✓(7 tasks)|✓(7)|✓(7)|✓(7)|
|IN-GMT SONIC|✓(7 tasks)|✓(7)|✓(7)|✓(7)|
|CROSS-GMT (TWIST2_→_SONIC)|✓(7 tasks)|N.E.|N.E.|N.E.|
|CROSS-GMT (SONIC_→_TWIST2)|✓(7 tasks)|N.E.|N.E.|N.E.|


### **D.7 Evaluation Matrix** 

Table S5 summarizes the complete evaluation coverage. All results use 3 seeds _×_ 20 repeats = 60 episodes per entry. In-GMT denotes matched training and evaluation with the same backend; Cross-GMT denotes training on one backend’s demonstrations and deployment on the other. 

## **E Additional Experiments and Rollout Analysis** 

### **E.1 Predicted Action Distributions under** **_Cross-GMT_ Observations** 

This section provides a qualitative analysis of why _cross-GMT_ deployment is challenging. We ask whether a fixed policy produces similar whole-body actions when conditioned on observations collected with different general motion trackers (GMTs). Instead of visualizing ground-truth dataset actions, we visualize _policy-predicted_ actions: each point corresponds to a 40D action predicted by a task-specific diffusion policy from one sampled egocentric observation. The policy input contains the 

9 

front RGB image and the 64D proprioceptive state, while the t-SNE embedding is computed only from the predicted 40D action after policy post-processing. 

For each task and each diffusion policy, we sample 1,000 SONIC observations and 1,000 TWIST2 observations, using 10 uniformly spaced frames from each of the 100 episodes per source. We run the same inference pipeline as the HTTP policy server, including image preprocessing, policy normalization, post-processing, and action unnormalization. For diffusion policies, we use the first action from the predicted action chunk as the immediate policy output, avoiding the stateful action queue used during online `select_action` inference. 

Figures S8 and S9 show the predicted-action distributions of SONIC-trained and TWIST2-trained diffusion policies, respectively. Each subplot fixes one task-specific policy and compares actions induced by SONIC versus TWIST2 observations. Overlapping colors indicate that the policy maps both observation sources to similar regions of the action space, whereas separated clusters indicate a GMT-dependent shift in the predicted whole-body action distribution. Since t-SNE is fitted independently per subplot, the coordinates should only be interpreted within each subplot; absolute positions are not comparable across tasks or policies. 


Figure S8: **SONIC-trained diffusion policies.** t-SNE visualization of predicted 40D actions on the seven benchmark tasks. Blue and orange points denote actions induced by SONIC and TWIST2 observations, respectively, using 1,000 samples per source. Larger color separation indicates a stronger GMT-dependent shift in the immediate action distribution. 

The visualized distributions show that SONIC and TWIST2 observations often form source-specific regions in the predicted action space, especially in tasks involving locomotion, contact, and wholebody coordination. This pattern is consistent with the cross-GMT rollout degradation reported in the benchmark: observations collected through different GMTs are not interchangeable inputs for a fixed policy. Instead, changing the GMT shifts the coupled image–proprioception distribution and leads the same policy to produce different immediate control outputs. These t-SNE results therefore provide qualitative evidence that the SONIC–TWIST2 gap appears not only at the execution-interface level, but also in the policy-predicted action distribution. 

## **F Policy Implementations and Training Details** 

All policy baselines are implemented and trained on the LeRobot platform under a unified experimental pipeline. As summarized in Table S6, we report the main implementation and training configurations for ACT, Diffusion Policy, Flow Matching, and _π_ 0 _._ 5, covering model initialization, optimization settings, temporal prediction design, image preprocessing, training schedule, and numerical precision. To ensure a fair comparison, these baselines are trained with consistent settings whenever applicable, including the same observation length, action chunk length, inference action length, batch size, training steps, and random seed. Meanwhile, we retain the model-specific configurations required by each policy architecture, such as backbone initialization, learning rate, 

10 


Figure S9: **TWIST2-trained diffusion policies.** t-SNE visualization of predicted 40D actions on the seven benchmark tasks. Blue and orange points denote actions induced by SONIC and TWIST2 observations, respectively, using 1,000 samples per source. Stronger separation provides qualitative evidence of a larger GMT-dependent shift in the policy-predicted action distribution. 

policy horizon, optimization objective, preprocessing pipeline, and precision format. This unified yet architecture-aware setup allows different policy baselines to be compared under controlled training conditions while preserving their standard implementation characteristics. 

Table S6: **Training configurations of policy baselines.** We summarize the key implementation and training settings used for ACT, Diffusion Policy, Flow Matching, and _π_ 0 _._ 5. 

|**Configuration**|**ACT**|**Diffusion Policy**|**Flow Matching**|**_π_0****_._5**|
|---|---|---|---|---|
|Initialization<br>Objective|ResNet-18<br>–|ResNet-18<br>–|CLIP ViT-B/16<br>Flow matching|_π_0_._5base checkpoint<br>–|
|Observation steps|1|1|1|1|
|Action chunk length|20|20|20|20|
|Policy horizon|–|24|40|–|
|Inference action steps|20|20|20|20|
|Image preprocessing|Resize + padding|Resize + padding|Resize + padding|Image transform enabled|
|Input image size|224_×_224<br>|224_×_224<br>|224_×_224<br>|–<br>|
|Learning rate|1_._0_×_10<sup>_−_5</sup>|1_._0_×_10<sup>_−_4</sup>|2_._0_×_10<sup>_−_5</sup>|2_._5_×_10<sup>_−_5</sup>|
|Batch size|64|64|64|64|
|Training steps|100K|100K|100K|100K|
|Random seed|42|42|42|42|
|Precision|float32|float32|float32|bfloat16|


## **G Failure Mode Analysis** 

This section analyses representative failure modes in HUMANOIDARENA. While the main text reports task success rate and average fall rate, these aggregate metrics do not fully explain where a hierarchical humanoid policy succeeds or fails. In HUMANOIDARENA, a rollout may fail because the high-level policy misinterprets the egocentric scene, fails to align the body with the task-relevant object, predicts an intermediate whole-body action that is difficult for the selected GMT to execute, or makes contact with the environment in a physically ineffective way. We therefore analyse failures at the level of rollout phases: perception and target localization, approach and body alignment, pre-contact posture preparation, contact execution, post-contact recovery, and final task completion. 

11 

### **G.1 Failure Taxonomy** 

We organize failures according to the stage of the hierarchical whole-body interaction pipeline at which task progress breaks down. 

**Perception and target-localization failure.** The policy fails to localize the task-relevant object or scene region from egocentric observations. For Football, this may appear as walking toward an incorrect direction, losing the ball after body rotation, or failing to maintain both the ball and goal in the effective field of view. 

**Approach and body-alignment failure.** The policy identifies the correct target but fails to bring the humanoid body into a useful interaction pose. For kicking, this includes incorrect root position relative to the ball, poor support-foot placement, or torso orientation that prevents a directed swing-leg trajectory. 

**Pre-contact posture failure.** The robot approaches the object but does not form a stable pre-contact posture. In Football, the robot must coordinate root displacement, support-leg balance, and swing-leg preparation. A rollout may remain upright but still fail to produce a posture from which a strong and well-directed kick is feasible. 

**Contact-execution failure.** The robot reaches the object but the physical contact does not produce the desired task effect. For Football, this includes weak impact, off-center foot–ball contact, incorrect kick direction, or insufficient momentum transfer. This failure mode is particularly important for leg-critical tasks because task success depends not only on reaching the object, but also on generating a physically meaningful contact event. 

**Post-contact recovery failure.** After an imperfect contact, the robot may need to re-localize the object, recover balance, and continue task execution. A policy that can recover from a partial contact failure demonstrates stronger closed-loop competence than one that becomes stuck after the first unsuccessful attempt. 

**Tracker-induced execution failure.** In cross-GMT settings, the same 40D canonical action may be realized differently by different GMT-specific adapters and low-level trackers. The resulting motion can differ in root displacement, swing-leg timing, torso stabilization, or egocentric camera motion, leading to task failure even when the high-level action encodes a plausible task intent. 

### **G.2 Football Case Study: Recoverable Contact-Execution Failure** 

Figure S10 shows a representative Football rollout. The sequence illustrates a recoverable contactexecution failure: the robot initially approaches the ball and attempts a kick, but the first contact does not send the ball far enough to enter the goal. Instead of terminating, falling, or remaining idle, the policy continues to track the updated ball position, moves closer, re-aligns its body and feet, and performs a second kick that completes the task. 

**Stage 1: target localization.** At the beginning of the rollout, the ball and goal are visible from the robot’s egocentric view. The policy initiates forward movement toward the task-relevant object, indicating that the rollout does not fail at the initial perception or target-grounding stage. 

**Stage 2: first approach and kick attempt.** The robot walks toward the ball and forms a kicking posture. This phase requires coordinated root displacement, support-foot placement, torso stabilization, and swing-leg preparation. The behavior demonstrates that the high-level policy has learned a plausible approach-and-kick pattern from the demonstration data. 

**Stage 3: partial contact failure.** The first kick contacts the ball but does not complete the task. The ball moves forward but stops between the robot and the goal. This is not a pure perception failure, because the robot has reached the correct object and produced meaningful task progress. Instead, it is better categorized as a contact-execution failure: the contact direction, impact strength, or swing timing is insufficient for the ball to satisfy the goal predicate. 

12 


Figure S10: Football failure-and-recovery rollout. The robot first observes the ball and goal, approaches the ball, and attempts an initial kick. The first contact is physically ineffective: the ball moves forward but does not travel far enough to enter the goal. The policy then continues the task by re-localizing the updated ball position, reducing the distance to the ball, aligning its body and feet before contact, and executing a second kick that sends the ball into the goal. This example shows that some HUMANOIDARENA failures are phase-level and recoverable, rather than immediately terminal. 

**Stage 4: recovery and re-approach.** After the unsuccessful kick, the robot does not remain fixed at the old ball location. It continues to move toward the new ball position. This behavior suggests that the high-level policy has learned a closed-loop recovery pattern from the demonstration distribution: when the first interaction does not finish the task, the robot can re-localize the object and continue acting on the updated scene state. 

**Stage 5: pre-contact re-alignment.** Before the second kick, the robot reduces its distance to the ball and re-aligns its body. This stage is important because leg-object interaction depends strongly on the relative pose between the root, support foot, swing leg, ball, and goal. The policy does not simply repeat the previous action; it adjusts the approach based on the changed ball position. 

**Stage 6: successful second contact.** The second kick sends the ball into the goal. This final stage indicates that the rollout contains a recoverable failure rather than an unrecoverable collapse. The policy preserves task intent after the first imperfect contact, while the GMT maintains sufficient balance and whole-body feasibility to support another attempt. 

### **G.3 Implications for Hierarchical Whole-Body Learning** 

The failure taxonomy reveals that leg-critical HOI/HSI tasks expose diagnostic signals beyond binary success. A policy may demonstrate competent target localization and approach behavior while still failing at contact execution (e.g., Football’s timing-critical kick). Binary success hides this intermediate competence, which is valuable for understanding where a hierarchical policy breaks down. Recoverable failures — where the robot re-approaches after an imperfect contact — further indicate that the policy is not replaying a fixed trajectory but conditioning on updated observations. 

### **G.4 Relation to Other Failure Modes** 

The same rollout can transition between failure categories. A perception error (losing the ball) may lead to an approach failure (incorrect foot placement), which then produces a contact failure (weak 

13 

kick). HUMANOIDARENA’s perturbation axes help isolate these: visual perturbations primarily stress perception; execution perturbations stress alignment and contact; semantic perturbations stress target grounding. The behavior-level taxonomy above provides a consistent framework for mapping quantitative signals (timeout/fall/visual-decline) to the underlying failure stage. 

## **H Reproducibility and Release Details** 

**Data collection.** All demonstration data are collected in Isaac Lab through teleoperated control. During collection, the operator receives the humanoid’s egocentric visual stream and controls the robot in closed loop; the resulting trajectories are recorded with synchronized observations, proprioceptive states, intermediate whole-body actions, task metadata, and GMT backend information. 

**Compute resources.** All policy models are trained on an 8-GPU NVIDIA H200 server. Validation and benchmark evaluation are performed on a 16-GPU NVIDIA RTX 4090 server. We use the RTX 4090 server for evaluation because our Isaac Lab evaluation pipeline requires graphical rendering, which is not available on the H-series training nodes in our compute environment. 

**Assets and licenses.** The paper cites and credits existing assets, including Isaac Lab (BSD-3-Clause, with Isaac Sim subject to NVIDIA Isaac Sim terms), Unitree simulation/G1-related resources (Apache2.0 where derived from `unitree_sim_isaaclab` ), GMR (MIT), TWIST2 (MIT), SONIC/GR00TWholeBodyControl (Apache-2.0), LeRobot and Unitree-LeRobot components (Apache-2.0), ACT and Diffusion Policy baselines (MIT), Flow Matching implementations based on LeRobot or related open implementations (Apache-2.0 where applicable), _π_ 0 _._ 5/OpenPI code (Apache-2.0), XRoboToolkit teleoperation components used in the data stream (MIT), and Synthesis/Extwin scene assets, which are tracked through an asset manifest and redistributed only when permitted by the corresponding asset license or terms of use. 

## **I More Results** 

Table S7 reports the full perturbation results for in-GMT evaluation, including per-task success rates under the in-distribution, visual, semantic, and execution settings. These results complement the suite-level robustness profiles in Figure 3 and provide detailed task-level evidence for the analysis in Section 4.2. 

Table S8 further studies whether the shared intermediate whole-body action interface enables dataset transfer across tasks and GMT backends. Compared with the base in-GMT results in Table S7, merged training brings clear gains in several settings. Under TWIST2 _×_ 7, DP improves from 35.56 _±_ 18.63% to 38.89 _±_ 20.25% on HOI, and more substantially from 55.83 _±_ 18.58% to 73.33 _±_ 23.48% on HSI. _π_ 0 _._ 5 also improves on TWIST2 HSI from 38.33 _±_ 20.14% to 55.00 _±_ 25.50%. Under SONIC _×_ 7, _π_ 0 _._ 5 improves its HSI average from 58.33 _±_ 20.85% to 65.42 _±_ 21.06%. These results suggest that the canonical action interface can reuse task-level whole-body intent across tasks, supporting effective dataset transfer beyond isolated task training. 

However, the gains are not uniform. For example, SONIC _×_ 7 reduces DP on HOI from 52.22 _±_ 17.97% to 29.44 _±_ 23.27%, and TWIST2+SONIC _×_ 14 improves DP on HSI to 68.12 _±_ 23.00% but leaves HOI at 31.67 _±_ 26.11%. We attribute these drops to GMT-conditioned action distribution mismatch. Although different GMT datasets share the same 40D action space, TWIST2 [11] and SONIC [12] differ in tracking capability, motion priors, stabilization behavior, and contact response. During closed-loop teleoperation, operators therefore rely on different corrective motions, foot placements, body postures, and contact timings to complete the same task. Such GMT-specific realizations have a stronger effect on contact-rich HOI tasks, where small execution differences can affect grasp stability, kicking timing, and object-contact effectiveness. Overall, merge-all training demonstrates that the shared intermediate action interface provides a practical basis for dataset transfer, while revealing how GMT-conditioned execution diversity shapes the effectiveness of multi-GMT policy learning. 

14 

Table S7: **In-GMT evaluation.** We evaluate high-level policy baselines with matched training and deployment GMTs, using either TWIST2 or SONIC as the low-level execution backend. Results are reported as success rate (SR, _↑_ ; mean _±_ standard deviation) on the in-distribution setting and the visual, semantic, and execution generalization splits. AVG denotes the average performance within each HOI or HSI task suite. The best and second-best SRs for each task and suite average under the same GMT and evaluation split are highlighted in **bold** and underlined, respectively. 

|Difficulty|Method|AFR(_↓_)|FOOTBALL|H<br>DOUBLEDESK|OI<br>P&PBOX|AVG|OPENDOOR|SITSOFA|HSI<br>BOXING|VISNAVI|AVG|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||**TWIST2**||||||
||ACT [45]|6.43%|26.7_±_6.2%|15.0_±_8.2%|43.3_±_8.5%|28.33_±_13.94%|50.0_±_4.1%|66.7_±_10.3%|58.3_±_10.3%|13.3_±_4.7%|47.08_±_21.84%|
|B|DP [46]|10.48%|46.7_±_6.2%|10.0_±_4.1%|**50.0**_±_**0.0%**|35.56_±_18.63%|68.3_±_6.2%|**73.3**_±_**6.2%**|51.7_±_11.8%|**30.0**_±_**4.1%**|55.83_±_18.58%|
|ase|FM [47]|7.38%|**53.3**_±_**8.5%**|**16.7**_±_**8.5%**|38.3_±_8.5%|**36.11**_±_**17.28%**|**76.7**_±_**2.4%**|68.3_±_6.2%|**63.3**_±_**9.4%**|26.7_±_20.9%|**58.75**_±_**22.56%**|
||_π_0_._5[7]|3.33%|26.7_±_4.7%|1.7_±_2.4%|46.7_±_8.5%|25.00_±_19.29%|28.3_±_9.4%|60.0_±_4.1%|51.7_±_8.5%|13.3_±_8.5%|38.33_±_20.14%|
||ACT [45]|6.67%|15.0_±_8.2%|0.0_±_0.0%|28.3_±_2.4%|14.44_±_12.57%|43.3_±_2.4%|51.7_±_8.5%|**63.3**_±_**6.2%**|23.3_±_12.5%|45.42_±_16.77%|
||DP [46]|12.38%|**40.0**_±_**7.1%**|**8.3**_±_**8.5%**|**41.7**_±_**6.2%**|**30.00**_±_**17.00%**|**68.3**_±_**4.7%**|**78.3**_±_**2.4%**|51.7_±_8.5%|25.0_±_4.1%|**55.83**_±_**20.90%**|
|Visual|<br>FM [47]|9.05%|26.7_±_4.7%|5.0_±_4.1%|23.3_±_6.2%|18.33_±_10.80%|65.0_±_10.8%|53.3_±_6.2%|56.7_±_18.9%|**30.0**_±_**10.8%**|51.25_±_18.04%|
||_π_0_._5[7]|1.67%|25.0_±_4.1%|1.7_±_2.4%|33.3_±_11.8%|20.00_±_15.28%|31.7_±_2.4%|43.3_±_10.3%|43.3_±_13.1%|5.0_±_4.1%|30.83_±_17.89%|
||ACT [45]|4.29%|20.0_±_4.1%|6.7_±_2.4%|35.0_±_8.2%|20.56_±_12.79%|46.7_±_8.5%|51.7_±_17.0%|**61.7**_±_**11.8%**|33.3_±_15.5%|48.33_±_17.00%|
||DP [46]|6.43%|50.0_±_0.0%|**16.7**_±_**4.7%**|46.7_±_6.2%|**37.78**_±_**15.65%**|**56.7**_±_**9.4%**|**75.0**_±_**10.8%**|60.0_±_4.1%|**40.0**_±_**8.2%**|**57.92**_±_**15.06%**|
|Semantic|FM [47]|7.14%|**58.3**_±_**6.2%**|8.3_±_2.4%|43.3_±_4.7%|36.67_±_21.47%|23.3_±_13.1%|66.7_±_8.5%|60.0_±_10.8%|20.0_±_14.1%|42.50_±_24.11%|
||_π_0_._5[7]|1.43%|13.3_±_9.4%|0.0_±_0.0%|**61.7**_±_**12.5%**|25.00_±_27.99%|6.7_±_2.4%|50.0_±_4.1%|55.0_±_4.1%|16.7_±_9.4%|32.08_±_21.55%|
||ACT [45]|5.71%|26.7_±_13.1%|**13.3**_±_**2.4%**|33.3_±_13.1%|24.44_±_13.63%|48.3_±_15.5%|65.0_±_4.1%|55.0_±_12.2%|35.0_±_10.8%|50.83_±_15.79%|
||DP [46]|8.33%|**43.3**_±_**4.7%**|8.3_±_4.7%|**45.0**_±_**4.1%**|**32.22**_±_**17.50%**|63.3_±_6.2%|60.0_±_10.8%|48.3_±_10.3%|**36.7**_±_**13.1%**|52.08_±_14.78%|
|Execution|FM [47]|6.67%|41.7_±_6.2%|13.3_±_4.7%|33.3_±_6.2%|29.44_±_13.22%|**80.0**_±_**8.2%**|**76.7**_±_**8.5%**|**58.3**_±_**13.1%**|23.3_±_9.4%|**59.58**_±_**24.62%**|
||_π_0_._5[7]|2.62%|21.7_±_2.4%|0.0_±_0.0%|33.3_±_8.5%|18.33_±_14.72%|31.7_±_13.1%|51.7_±_8.5%|50.0_±_7.1%|16.7_±_8.5%|37.50_±_17.26%|
|||||||**SONIC**||||||
||ACT [45]|8.57%|16.7_±_6.2%|18.3_±_4.7%|56.7_±_6.2%|30.56_±_19.36%|78.3_±_9.4%|73.3_±_8.5%|56.7_±_6.2%|33.3_±_2.4%|60.42_±_18.98%|
||DP [46]|8.33%|**45.0**_±_**10.8%**|36.7_±_4.7%|**75.0**_±_**4.1%**|**52.22**_±_**17.97%**|**85.0**_±_**10.8%**|**78.3**_±_**14.3%**|**76.7**_±_**2.4%**|23.3_±_6.2%|**65.83**_±_**26.52%**|
|Base|FM [47]|5.71%|13.3_±_2.4%|38.3_±_4.7%|73.3_±_6.2%|41.67_±_25.06%|70.0_±_4.1%|15.0_±_7.1%|70.0_±_8.2%|**38.3**_±_**14.3%**|48.33_±_24.94%|
||_π_0_._5[7]|5.24%|10.0_±_4.1%|**43.3**_±_**6.2%**|71.7_±_11.8%|41.67_±_26.46%|66.7_±_6.2%|73.3_±_2.4%|70.0_±_0.0%|23.3_±_6.2%|58.33_±_20.85%|
||ACT [45]|9.76%|18.3_±_2.4%|6.7_±_2.4%|50.0_±_10.8%|25.00_±_19.44%|63.3_±_2.4%|35.0_±_8.2%|53.3_±_10.3%|38.3_±_2.4%|47.50_±_13.31%|
||DP [46]|8.33%|**30.0**_±_**4.1%**|**28.3**_±_**2.4%**|55.0_±_4.1%|**37.78**_±_**12.72%**|**71.7**_±_**8.5%**|**46.7**_±_**22.5%**|**75.0**_±_**14.1%**|35.0_±_4.1%|**57.08**_±_**21.93%**|
|Visual|<br>FM [47]|8.10%|6.7_±_6.2%|13.3_±_6.2%|46.7_±_20.9%|22.22_±_21.87%|31.7_±_4.7%|8.3_±_2.4%|73.3_±_2.4%|**41.7**_±_**8.5%**|38.75_±_23.90%|
||_π_0_._5[7]|5.00%|15.0_±_0.0%|13.3_±_2.4%|**73.3**_±_**10.3%**|33.89_±_28.56%|63.3_±_2.4%|35.0_±_10.8%|63.3_±_13.1%|18.3_±_6.2%|45.00_±_21.31%|
||ACT [45]|6.43%|8.3_±_6.2%|15.0_±_4.1%|63.3_±_2.4%|28.89_±_24.92%|56.7_±_6.2%|21.7_±_6.2%|46.7_±_10.3%|30.0_±_8.2%|38.75_±_15.83%|
||DP [46]|6.67%|**33.3**_±_**14.3%**|13.3_±_2.4%|56.7_±_6.2%|34.44_±_19.92%|**78.3**_±_**2.4%**|**60.0**_±_**7.1%**|**71.7**_±_**8.5%**|26.7_±_8.5%|**59.17**_±_**21.10%**|
|Semantic|<br>FM [47]|5.71%|8.3_±_8.5%|8.3_±_4.7%|60.0_±_4.1%|25.56_±_25.10%|3.3_±_4.7%|28.3_±_2.4%|68.3_±_13.1%|**35.0**_±_**7.1%**|33.75_±_24.51%|
||_π_0_._5[7]|2.38%|16.7_±_8.5%|**25.0**_±_**0.0%**|**75.0**_±_**7.1%**|**38.89**_±_**26.54%**|8.3_±_4.7%|41.7_±_13.1%|65.0_±_4.1%|16.7_±_2.4%|32.92_±_23.40%|
||ACT [45]|6.90%|23.3_±_6.2%|11.7_±_8.5%|65.0_±_4.1%|33.33_±_23.80%|68.3_±_13.1%|50.0_±_4.1%|46.7_±_6.2%|36.7_±_6.2%|50.42_±_14.06%|
|Eti|<br>DP [46]|5.00%|**45.0**_±_**4.1%**|30.0_±_14.7%|**78.3**_±_**6.2%**|**51.11**_±_**22.33%**|81.7_±_6.2%|**80.0**_±_**4.1%**|**80.0**_±_**7.1%**|33.3_±_11.8%|**68.75**_±_**21.90%**|
|xecuon|FM [47]|5.24%|20.0_±_8.2%|**31.7**_±_**8.5%**|63.3_±_8.5%|38.33_±_20.14%|**83.3**_±_**4.7%**|6.7_±_4.7%|66.7_±_11.8%|**45.0**_±_**4.1%**|50.42_±_29.54%|
||_π_0_._5[7]|5.48%|15.0_±_4.1%|26.7_±_2.4%|78.3_±_6.2%|40.00_±_27.89%|63.3_±_6.2%|41.7_±_9.4%|68.3_±_6.2%|18.3_±_2.4%|47.92_±_20.86%|


Table S8: **Merge-All evaluation.** We evaluate high-level policy baselines trained with merged demonstrations from TWIST2-only seven task-GMT settings, SONIC-only seven task-GMT settings, or the combined TWIST2+SONIC fourteen task-GMT settings. Results are reported as success rate (SR, _↑_ ; mean _±_ standard deviation). AVG denotes the average SR within each HOI or HSI task suite. The best and second-best distinct AVG are highlighted in **bold** and underlined, respectively. 

|||||H|OI||||HSI|||
|---|---|---|---|---|---|---|---|---|---|---|---|
|Setting|Method|AFR (_↓_)|FOOTBALL|DOUBLEDESK|P&PBOX|AVG(_↑_)|OPENDOOR|SITSOFA|BOXING|VISNAVI|AVG (_↑_)|
|TWIST2_×_7|ACT [45]<br>DP [46]<br>FM [47]|7.75%<br>7.62%<br>6.90%|48.3_±_2.4%<br>61.7_±_9.4%<br>35.0_±_4.1%|3.3_±_2.4%<br>18.3_±_12.5%<br>18.3_±_2.4%|17.5_±_2.5%<br>36.7_±_6.2%<br>30.0_±_4.1%|23.75_±_19.96%<br>**38.89**_±_**20.25%**<br>27.78_±_7.86%|21.7_±_4.7%<br>93.3_±_6.2%<br>68.3_±_6.2%|78.3_±_6.2%<br>91.7_±_2.4%<br>68.3_±_6.2%|8.3_±_6.2%<br>61.7_±_8.5%<br>55.0_±_8.2%|18.3_±_16.5%<br>46.7_±_22.5%<br>25.0_±_7.1%|31.67_±_29.04%<br>**73.33**_±_**23.48%**<br>54.17_±_19.02%|
||_π_0_._5[7]|4.52%|33.3_±_8.5%|0.0_±_0.0%|43.3_±_6.2%|25.56_±_19.50%|73.3_±_6.2%|81.7_±_4.7%|46.7_±_6.2%|18.3_±_6.2%|55.00_±_25.50%|
||ACT [45]|7.38%|20.0_±_4.1%|30.0_±_4.1%|60.0_±_12.2%|36.67_±_18.71%|58.3_±_2.4%|21.7_±_2.4%|58.3_±_10.3%|28.3_±_4.7%|41.67_±_17.83%|
|SONIC_×_7|DP [46]|7.14%|53.3_±_6.2%|35.0_±_10.8%|0.0_±_0.0%|29.44_±_23.27%|83.3_±_6.2%|83.3_±_4.7%|21.7_±_30.6%|50.0_±_14.7%|59.58_±_31.12%|
||FM [47]|7.14%|21.7_±_8.5%|20.0_±_7.1%|0.0_±_0.0%|13.89_±_11.73%|76.7_±_2.4%|48.3_±_6.2%|18.3_±_25.9%|38.3_±_6.2%|45.42_±_25.12%|
||_π_0_._5[7]|6.43%|10.0_±_7.1%|30.0_±_7.1%|75.0_±_4.1%|**38.33**_±_**27.89%**|85.0_±_4.1%|70.0_±_14.7%|71.7_±_12.5%|35.0_±_4.1%|**65.42**_±_**21.06%**|
||ACT [45]|6.95%|32.5_±_18.4%|9.2_±_10.2%|36.0_±_12.8%|25.29_±_18.67%|10.0_±_2.9%|34.2_±_6.7%|53.3_±_16.7%|13.3_±_9.0%|27.71_±_20.21%|
|TWIST2SONIC14|DP [46]|9.40%|33.3_±_5.5%|17.5_±_12.8%|44.2_±_30.2%|31.67_±_26.11%|82.5_±_4.8%|89.2_±_9.8%|63.3_±_9.0%|37.5_±_17.5%|**68.12**_±_**23.00%**|
|+_×_|FM [47]|9.88%|26.7_±_12.1%|18.3_±_13.4%|28.3_±_26.9%|24.44_±_19.21%|13.3_±_13.1%|40.8_±_24.7%|36.7_±_15.5%|10.0_±_7.6%|25.21_±_21.38%|
||_π_0_._5[7]|8.69%|35.0_±_23.8%|15.0_±_15.8%|45.0_±_25.3%|**31.67**_±_**25.33%**|51.7_±_21.5%|58.3_±_21.5%|55.8_±_11.7%|23.3_±_10.3%|47.29_±_22.13%|


## **J Limitations and Future Directions** 

**Limited task and scene coverage.** The current benchmark contains seven leg-critical HOI/HSI tasks covering object interaction, scene interaction, navigation, kicking, sitting, door opening, and target striking. Although these tasks expose important whole-body behaviors such as foot placement, balance maintenance, posture adjustment, and contact-rich execution, they still represent only a subset of everyday humanoid interaction. Future versions can expand the benchmark with richer household activities, multi-object rearrangement, human-robot interaction, tool use, outdoor locomotion-interaction tasks, and longer-horizon task sequences. 

15 

