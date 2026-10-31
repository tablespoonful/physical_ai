---
title: "LiLo-VLA: Compositional Long-Horizon Manipulation via Linked Object-Centric Policies"
date: "2026-02-25"
authors: "Yue Yang; Shuo Cheng; Yu Fang; Homanga Bharadhwaj; Mingyu Ding; Gedas Bertasius"
url: https://arxiv.org/abs/2602.21531
pdf: https://arxiv.org/pdf/2602.21531
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.21531)** / [論文ページ](https://arxiv.org/abs/2602.21531)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# LiLo-VLA: Compositional Long-Horizon Manipulation via Linked Object-Centric Policies 

Yue Yang<sup>1</sup><sup>_,†_</sup> , Shuo Cheng<sup>2</sup> , Yu Fang<sup>1</sup> , Homanga Bharadhwaj<sup>3</sup> , Mingyu Ding<sup>1</sup> , Gedas Bertasius<sup>1</sup> , Daniel Szafir<sup>1</sup> 

- 1 **University of North Carolina at Chapel Hill** 2 **Georgia Institute of Technology** 3 **Carnegie Mellon University** 

   - Corresponding author: yygx@cs.unc.edu 


Fig. 1. **LiLo-VLA enables composable and robust manipulation.** LiLo-VLA solves long-horizon tasks by sequentially executing object-centric skill policies connected by robust motion planning. This enables zero-shot compositional generalization and robustness against cascading failures. 

**_Abstract_ —General-purpose robots must master long-horizon manipulation, defined as tasks involving multiple kinematic structure changes (e.g., attaching or detaching objects) in unstructured environments. While Vision-Language-Action (VLA) models offer the potential to master diverse atomic skills, they struggle with the combinatorial complexity of sequencing them and are prone to cascading failures due to environmental sensitivity. To address these challenges, we propose LiLo-VLA** **<u>(Linked Local VLA),</u> a modular framework capable of zero-shot generalization to novel long-horizon tasks without ever being trained on them. Our approach decouples transport from interaction: a Reaching Module handles global motion, while an Interaction Module employs an object-centric VLA to process isolated objects of interest, ensuring robustness against irrelevant visual features and invariance to spatial configurations. Crucially, this modularity facilitates robust failure recovery through dynamic replanning and skill reuse, effectively mitigating the cascading errors common in end-toend approaches. We introduce a 21-task simulation benchmark consisting of two challenging suites: LIBERO-Long++ and UltraLong. In these simulations, LiLo-VLA achieves a 69% average success rate, outperforming Pi0.5 by 41% and OpenVLA-OFT by 67%. Furthermore, real-world evaluations across 8 long-horizon tasks demonstrate an average success rate of 85%. Project page: https://yy-gx.github.io/LiLo-VLA/.** 

### I. INTRODUCTION 

A grand goal of general-purpose robotics is to enable complex long-horizon manipulation, such as activities involving multiple skills (e.g., picking, placing, and pouring) to achieve high-level goals like cooking or cleaning. While recent generalist policies have achieved impressive results on short-horizon, single-stage manipulation [6, 7, 42, 36], extending these capabilities to multi-stage activities remains a grand challenge. Vision-Language-Action (VLA) models have emerged as a promising solution to bridge this gap, utilizing Internet-scale pre-training to enable diverse skill execution and semantic reasoning [21, 22, 3, 18]. However, applying current VLA paradigms to long-horizon tasks reveals two fundamental limitations. First, existing methods lack compositional generalization: they struggle to adapt to novel task sequences that were not explicitly seen during training, as they fail to flexibly recombine learned atomic skills without extensive task-specific demonstrations [32, 31]. Second, long-horizon execution is prone to cascading failures: since VLA policies easily overfit to visual features or specific spatial configurations, they become brittle to minor variations, where a single failure at any 

stage jeopardizes the entire task sequence [41, 40]. 

To mitigate the data requirements for compositional generalization, recent research has explored learning modular skills. Approaches like PlanSeqLearn and local policy learning decouple tasks into atomic behaviors, employing motion planners for reaching and learned policies for interaction [8, 9]. However, these methods struggle with skill chaining, often relying on labor-intensive reward engineering or ad-hoc local goals for motion planning integration that hinder scalability. Alternatively, unified approaches like Long-VLA train a single end-to-end model to handle both transport and interaction phases via input masking [10]. Yet, these methods remain data-inefficient as they couple global transport with interaction, forcing the network to learn geometric motion planning through unstructured data. To address the second challenge of cascading failures, VLM-based recovery methods leverage the reasoning capabilities of foundation models to detect errors and trigger replanning [16, 28, 14]. However, these approaches primarily focus on task-level planning and rely on the critical assumption that underlying skills are robust. Simply reinvoking a skill policy that is sensitive to irrelevant visual features is ineffective, as it often leads to repeated failures. Moreover, execution failures frequently modify the spatial configuration of the scene, pushing the system outside the policy’s initial state distribution. 

To overcome these limitations, we introduce **LiLo-VLA** ( **Li** nked **Lo** cal **VLA** ), a framework that synergizes the strengths of classical motion planning and VLA policies to master complex long-horizon manipulation. We adopt a modular control strategy that decouples execution into two distinct phases. A Reaching Module employs classical motion planners to navigate a robot’s end-effector to a target vicinity, where control is handed over to an Interaction Module, an objectcentric VLA dedicated to fine-grained atomic manipulation. Through this modular design and the seamless integration of learned policies with classical planners, **LiLo-VLA** offers three decisive advantages. First, it achieves compositional generalization. By reusing object-centric atomic skills, the system can zero-shot generalize to novel long-horizon tasks without requiring any task-specific demonstration data. Second, it ensures robustness to environmental variations. By decomposing the scene and confining VLA observations strictly to the object of interest, the policy remains invariant to global workspace layouts and background clutter. Third, it enables inherent failure recovery. Rather than blindly retrying a failed skill, our system utilizes the Reaching Module to dynamically replan and reset the workspace, allowing for effective re-invocation of VLA skills. To comprehensively evaluate **LiLo-VLA** , we curate a challenging benchmark and provide the corresponding dataset, consisting of 21 tasks across two distinct suites. Crucially, both suites enforce randomized skill sequencing to rigorously stress-test compositional generalization. The first enhances LIBERO-Long [26] by introducing complex visual clutter to verify robustness against distractors. The second features custom ultra-long tasks chaining up to 16 atomic skills. This significantly exceeds the horizon length of 

prior benchmarks such as LIBERO-Long, which are typically limited to sequences of 3 to 4 skills, thereby challenging scalability. Our contributions in this work are four-fold: 

- **LiLo-VLA Framework:** A modular framework for longhorizon tasks that enables zero-shot compositional generalization and achieves robustness to visual clutter and execution failures. 

- **Evaluation Benchmarks:** A 21-task benchmark across two suites, “LIBERO-Long++” and “Ultra-Long”, both of which evaluate compositional generalization while respectively focusing on visual robustness and extreme temporal scalability reaching up to 16 sequential skills. 

- **Simulation Performance:** Extensive experiments show **LiLo-VLA** achieves a 69% average success rate, significantly outperforming Pi0.5 (28%) and OpenVLA-OFT (2%). 

- **Real-World Validation:** Deployment on 8 long-horizon tasks (up to 8 skills) with complex backgrounds and varied sequence, achieving an 85% average success rate. 

II. RELATED WORK 

### _A. Vision-Language-Action Models_ 

Recent robot learning has been driven by VLA models that unify perception and control via Transformer architectures. Pioneering works like RT-2 [44] and Octo [37] demonstrated the efficacy of large-scale pretraining. Building on this, OpenVLA [21] utilized LLM backbones to enhance performance, while OpenVLA-OFT [22] improved control precision. Applications have expanded to bimanual control with RDT-1b [27] and humanoid embodiments via Project GR00t [2]. Recently, Pi0 [3] and Pi0.5 [18] leveraged flow matching and extensive real-world pretraining to capture complex action distributions. Despite improving atomic skill proficiency, these methods often overfit to visual signals and lack inherent compositional generalization. 

### _B. Long-Horizon Manipulation and Skill Chaining_ 

Solving long-horizon tasks requires effectively sequencing atomic behaviors to achieve a high-level goal. Classical Task and Motion Planning (TAMP) addresses this by combining symbolic search with geometric feasibility checks and engineered low-level controllers [19, 12, 34]. However, TAMP typically assumes accurate state estimation and known object models, which limits its robustness and applicability in unstructured, real-world environments. More recently hierarchical learning approaches have integrated learned models for generating low-level motions [5, 4, 30, 29]. To reduce reliance on manually defined planning domains, researchers have explored using large language models to decompose abstract task instructions into intermediate, executable subgoals. Frameworks, such as Code as Policy [23], ProgPrompt [35], SayCan [1] and VoxPoser [17], demonstrate strong semantic planning capabilities but often assume robust low-level execution. Most recently, LEAGUE [4] and Planseq-learn [8] pioneered the integration of motion planning 

with RL trained policies for long-horizon tasks, while LongVLA [10] introduced the first VLA architecture explicitly designed for long-horizon manipulation. However, the former relies on ad-hoc integration strategies that hinder scalability, while the latter is data-inefficient by coupling global transport with local interaction. 

### III. METHODOLOGY 

We describe **LiLo-VLA** in four stages: In Section III-A, we first formalize the problem and outline the system architecture. We then detail the Reaching Module, which handles global transport via robust motion planning, in Section III-B. Subsequently, Section III-C introduces our Interaction Module, featuring the Object-Centric VLA designed for local robustness. Finally, Section III-D describes the closed-loop execution pipeline and our hierarchical failure recovery mechanism. 

### _A. Overview of_ **_LiLo-VLA_** 

Formally, we define a long-horizon manipulation task as a sequence of symbolic actions _T_ = _{a_ 1 _, a_ 2 _, . . . , aN }_ . Each action _ai_ is formulated as a parameterized predicate _αi_ ( _oi, ρi_ ), where _αi_ denotes the primitive skill category (e.g., Pick, Place), _oi_ represents the reference object that establishes the local coordinate frame for execution (e.g., the target object for a Pick action, or the receptacle for a Place action), and _ρi_ encapsulates auxiliary parameters such as constraints. Although such high-level task skeleton can be generated automatically— either by symbolic planners [33, 12, 24] or by foundation models (LLMs/VLMs) [25, 11]—our focus in this work is on generating low-level robot motions that faithfully realize a given task plan _T_ and achieve the desired goal under realistic geometric and dynamical constraints. 

As illustrated in Figure 2, **LiLo-VLA** adopts a modular architecture to ground and execute these symbolic actions sequentially. For each action _ai_ , the system executes the corresponding atomic skill through a two-phase process. First, the Reaching Module (Figure 2 Top-Left) transports the endeffector from its current configuration to a robust approach pose defined relative to _oi_ via motion planning. Subsequently, the Interaction Module (Figure 2 Top-Right) is activated to perform the contact-rich manipulation using a learned policy centered on _oi_ with visual masking. As depicted in the bottom pipeline of Figure 2, this design philosophy effectively decouples the problem space. It utilizes motion planning for collision-free transport and leverages the Object-Centric VLA for local interaction, ensuring that the expensive learning capacity is focused exclusively on mastering the diverse dynamics of atomic skills while enabling autonomous failure recovery. 

### _B. The Reaching Module: Global Transport_ 

The Reaching Module serves as the bridge between distinct atomic skills, addressing the challenge of navigating the endeffector from the termination state of the previous skill to the initial state of the next. By leveraging a motion planner, this module ensures collision avoidance over long distances 

and guides the robot to a precise approach pose suitable for the downstream object-centric VLA. This approach pose also serves as a deterministic target for the motion planner during deployment. 

_1) Relative Goal Generation with Perturbation:_ The core function of this module is to determine the robust _Approach Pose_ , _Tapproach ∈ SE_ (3), which serves as the deterministic target for the motion planner. We derive this pose via a relative transformation from the reference object’s frame: _Tapproach_ = _Toi ·Toffset_ ( _αi_ ). Here, the offset transformation _Toffset_ ( _αi_ ) is constructed to enforce a fixed face-down orientation relative to the object surface for all skills, while applying a skill-specific translation vector defined by _αi_ (e.g., a vertical clearance _hpick_ for picking tasks). 

To ensure the downstream VLA policy is resilient to noise stemming from motion planning and perception, we introduce a perturbation strategy. During demonstration generation, rather than always initializing from the canonical approach pose _Tapproach_ , we randomize the start pose of each training trajectory by sampling 


where _ξ ∼N_ (0 _,_ Σ) defines a zero-mean perturbation in SE(3), injecting noise in both translation and rotation. The robot is transported to this perturbed state _Tinit_ to initiate each data collection episode. Consequently, during the deployment phase, while the Reaching Module targets the canonical _Tapproach_ , the VLA policy acquires strong local generalization capabilities by training on the dispersed distribution of _Tinit_ . This allows the Interaction Module to effectively compensate for deviations caused by pose estimation errors and imperfect motion planning convergence. 

_2) Collision-Free Motion Planning:_ Given the determined target pose, _Tapproach_ , during deployment or _Tinit_ during demonstration generation, we employ MPLib [13] to generate a collision-free trajectory. This planner integrates the environmental point cloud with the robot’s kinematic chain to solve for a feasible path, ensuring safe global transport to the interaction start state without requiring any learning. 

### _C. The Interaction Module: Object-Centric VLA_ 

The reaching module brings the robot end-effector into proximity with the object. We model robot–object interaction by learning an end-to-end visuomotor policy _πθ_ that reactively predicts end-effector actions from the current observations. To ensure robustness against the spatial variability inherent in long-horizon tasks, we introduce a strictly object-centric design. 

_1) Object-Centric Observation Space:_ To ensure a strictly object-centric representation, our observation space relies exclusively on egocentric visual inputs captured by the wristmounted camera. We deliberately exclude static third-person views to mitigate the observation space shift (OSS) problem common in long-horizon manipulation [41], defined as the performance degradation caused by task-irrelevant visual changes across different stages of a long-horizon task. Since 


Fig. 2. **Architecture of LiLo-VLA.** Our framework decouples manipulation into two distinct phases. **(Top Left) The Reaching Module** handles global transport via collision-free motion planning. It employs initial state perturbation during training to ensure the policy to be robust to pose errors during deployment. **(Top Right) The Interaction Module** executes atomic skills via an object-centric VLA, strictly utilizing wrist-view observations and visual masking to eliminate environmental distractors. **(Bottom)** The system sequentially chains these modules, enabling closed-loop failure recovery where each skill’s execution errors trigger a fallback to the Reaching Module for state resetting. 

the robot base or global position may vary between skill executions, relying on fixed global cameras can introduce inconsistent visual features. In contrast, the wrist view maintains a consistent perspective relative to the workspace during interaction. This observation locality helps the robot focus on task-relevant objects, reducing the negative impact of visual distractors. We provide empirical validation for this design choice in Section IV-C2, demonstrating that a wrist-only policy outperforms multi-view configurations in atomic skill success rates. 

_2) Visual Clutter Augmentation:_ VLA policies frequently overfit to environmental distractors, such as objects relevant to other skills [40]. To eliminate this interference during deployment, we apply a heuristic masking strategy that covers non-target objects with black rectangles derived from their bounding boxes. However, these artificial occlusions constitute a significant visual domain shift, potentially leading to out-ofdistribution (OOD) failures for a standard policy. 

To ensure robustness against these artifacts, we introduce a mask-aware data augmentation strategy during training, inspired by [43]. We utilize segmentation to partition each training frame into foreground (the gripper, the reference object, and any grasped object) and background (all other pixels). We then apply a random erasing augmentation that overlays black rectangles exclusively onto the background regions. The number of rectangles and their total area ratio are sampled uniformly from a predefined range. This training procedure effectively simulates the visual artifacts introduced by our deployment masking, ensuring that the masked infer- 

**Algorithm 1** Compositional Inference with Closed-Loop Recovery 


ence observations remain within the learned distribution of the policy. 

### _D. Compositional Execution and Failure Recovery_ 

The complete inference pipeline integrates the proposed modules into a cohesive control loop, as summarized in Algorithm 1. 

_1) Sequential Execution Pipeline:_ For each atomic skill _ai_ in the plan, the system orchestrates the execution through a standardized pipeline (Alg. 1, Lines 3-6). First, the system estimates the 6D pose of the target object relevant to the current skill. This pose is ingested by the Reaching Module ( _M_ reach), which plans and executes a collision-free trajectory to navigate the end-effector to the approach pose, denoted as _T_ approach. This alignment ensures a consistent geometric initialization for the subsequent manipulation. Subsequently, the Interaction Module ( _M_ int) takes control to perform the fine-grained manipulation task using the VLA policy. Finally, the execution concludes with a geometric verification function _V_ ( _ai_ ), which evaluates the spatial configuration of the object of interest to determine if the skill’s effect has been satisfied. 

_2) Closed-Loop Recovery Mechanism:_ The modular architecture enables robust recovery from execution failures by adapting the control flow based on the semantic state of the robot (Alg. 1, Lines 8-12). When a failure is detected by _V_ ( _ai_ ) for a skill that does not involve holding an object (e.g., a _Pick_ attempt), the system triggers a local retry. By maintaining the current skill index _i_ and re-initiating the loop, the system forces a re-evaluation of the spatial state. Specifically, this updates the object pose and resets the endeffector to _T_ approach, correcting any transient errors caused by the failed interaction and ensuring the policy is conditioned on the latest observation. In contrast, if a failure occurs during a skill that requires object retention (e.g., a _Place_ operation), we conservatively assume that the object has been dropped or lost during transport. Operating under this assumption, a local retry is deemed risky. Therefore, the system backtracks the index _i_ to the most recent _Pick_ skill, ensuring the robot re-acquires the object before attempting the transport task again. 

### IV. SIMULATION EXPERIMENTS 

### _A. Experimental Setup_ 

_1) Benchmarks:_ To evaluate zero-shot compositional generalization and robustness to cascading failures, we curate a 21task benchmark across two distinct suites within the LIBERO environment [26], derived from 9 core scenarios. 

**Suite 1: LIBERO-Long++.** We select 6 tasks from LIBERO-Long that are amenable to sequence re-ordering and augment them with randomized visual distractors (e.g., mugs, cans). As shown in Fig. 3, this setup increases visual complexity to test robustness, forcing the policy to filter background clutter and attend strictly to task-relevant objects. 

**Suite 2: Ultra-Long.** We design 3 tasks with increasing complexity: Kitchen Organization (9 steps), Cooking Preparation (10 steps), and Living Room Organization (16 steps). As illustrated in Fig. 3, the 16-step task presents a extreme challenge in workspace saturation; here, the high density of objects and receptacles pushes the kinematic reachability limits of a fixed-base tabletop robot. This suite systematically evaluates the system’s ability to maintain coherent execution and temporal scalability over extended horizons. 

**Evaluation Protocol.** To assess true compositionality rather than trajectory memorization, we evaluate multiple skill per- 

mutations for each scenario: 2 permutations for each of the 6 “Suite 1” scenarios and 3 for the 3 “Suite 2” scenarios (21 tasks in total). This protocol rigorously tests the system’s ability to ground novel skill execution orders in zero-shot way. 

_2) Baselines:_ We compare **LiLo-VLA** against two stateof-the-art generalist policies: **Pi 0.5** [18], a flow-matching VLA, and **OpenVLA-OFT** [22], a highly optimized version of OpenVLA [21]. 

**Setup for Suite 1.** For standard sequences, baselines are LoRA fine-tuned [15] on the original continuous long-horizon demonstrations to learn skill transitions in a fixed order. For variant sequences with novel orders, we evaluate zeroshot performance by prompting the models with re-ordered language instructions. 

**Setup for Suite 2.** Since collecting continuous demonstrations for every possible sequence permutation is combinatorially intractable, we train baselines on the aggregate dataset of constituent atomic skills to evaluate their inherent compositionality. During inference, we employ language chaining, sequentially prompting the model with sub-task descriptions to execute skills one-by-one. This evaluates whether VLAs can compose learned behaviors into novel long-horizon chains without requiring task-specific trajectory data. 

_3) Evaluation Metrics:_ We evaluate each task configuration over 10 trials and report performance using two standard metrics. **Success Rate (SR)** measures the percentage of episodes that reach the final goal state. Crucially, we enforce a strict standard: we count an episode as a success only if the robot executes the entire sequence of skills in the exact required order. **Average Progress (AP)** calculates the ratio of completed skills starting from the first step. We count only the continuous sequence of correct actions; if a skill is performed out of order, we stop counting immediately. 

_4) Implementation Details:_ To isolate manipulation capability from perception noise, we utilize simulator-provided ground-truth poses and segmentation masks. This oracle assumption ensures reported failures are attributable solely to the manipulation policy or motion planning rather than upstream estimation errors. 

**Data Generation.** We segment LIBERO-90 demonstrations into atomic skills and augment them via MPLib to bridge the planner-policy domain gap. By generating perturbed initial states around the approach pose and planning trajectories back to the original demonstrations, we create a dataset of skills initialized from diverse starting configurations. 

**Policy Architecture.** We adopt OpenVLA-OFT [22] as our backbone, retaining original hyperparameters for controlled comparison. To enforce object-centricity, we utilize the wrist camera view and apply random erasing to background pixels, mitigating visual overfitting to distractors. 

**Deployment.** During inference, the system executes the symbolic plan sequentially. For each skill, the Reaching Module plans a collision-free path to an approach pose defined by a fixed offset; the Interaction Module then takes control using language instructions. We implement the failure detector _V_ ( _Si_ ) via geometric heuristics to trigger closed-loop recovery. 


Fig. 3. **Overview of Evaluation Benchmarks.** We introduce two suites to evaluate long-horizon manipulation: Suite 1 (LIBERO-Long++) focuses on visual robustness by introducing more complex backgrounds with multiple distractors (highlighted in red), while Suite 2 (Ultra-Long) tests temporal scalability with task sequences extending up to 16 steps. Both suites incorporate multiple variant configurations with permuted skill orders to rigorously assess zero-shot compositional generalization. 

### _B. Main Results: Zero-Shot Compositionality and Scalability_ 

The quantitative results in Table I demonstrate that **LiLo-VLA** significantly outperforms state-of-the-art baselines across all metrics achieving an average success rate of 69% compared to 28% for Pi0.5 [18] and 2% for OpenVLAOFT [22]. This substantial performance gap highlights the limitations of monolithic policies in handling the complexity of long-horizon manipulation. In the LIBERO-Long++ suite the results reveal a critical weakness in current VLAs where Pi0.5 achieves a high success rate on Original sequences (83%) which is statistically comparable to **LiLo-VLA** (78%, _p >_ 0 _._ 05) yet collapses to 0% on Variant sequences. We observe that Pi0.5 frequently ignores the altered language instructions in these variant tasks and persists in executing the sequence order seen during training which confirms that the model overfits to the demonstrated trajectories rather than grounding the current language command. In contrast **LiLo-VLA** maintains robust performance (85%) by effectively isolating atomic skills. Furthermore in the ultra-long tasks of Suite 2 both baselines fail completely with a 0% success rate while **LiLo-VLA** maintains a 44% success rate. We attribute this failure to the coupling of global transport and local interaction in baseline models. Long-horizon tasks inherently involve evolving geometric configurations and spatial distribution shifts. Consequently baselines struggle to generalize to these changing layouts without intractable amounts of transition data. By explicitly decoupling global transport via a motion planner **LiLo-VLA** renders the interaction policy invariant to these global spatial shifts and effectively addresses the scalability bottleneck. 

### _C. Ablation Studies: Dissecting the_ **_LiLo-VLA_** _Framework_ 

_1) Necessity and Robustness of the Reaching Module:_ We first investigate the fundamental necessity of decoupling transport from interaction by removing the Reaching Module as shown in Table I. To address potential concerns regarding fair comparison and strictly isolate the impact of the modular architecture, we provided this ablation baseline with the same privileged ground-truth object poses used by our full method. Despite having access to this oracle geometric information, the policy fails completely with a 0% success rate across all 


Fig. 4. **Impact of State Perturbation.** Average success rates across 27 unique skills demonstrate that our interaction policy remains robust to initial pose noise due to state perturbation, whereas the unperturbed policy degrades significantly. 

tasks. This failure confirms that standard VLA architectures cannot implicitly learn long-horizon transport dynamics from atomic skill demonstrations alone even when the target location is known. Consequently, an explicit motion planner is not merely an auxiliary component but a structural prerequisite for bridging spatially distributed skills. 

Beyond necessity, we analyze the robustness of the interface between the motion planner and the policy. In real-world deployment, the system must contend with inevitable inaccuracies stemming from perception noise and imperfect motion planning convergence. To evaluate resilience to these factors, we conduct a comprehensive evaluation aggregating all 36 atomic skills from both Suite 1 and Suite 2, introducing execution noise to the initial poses of evaluation episodes as shown in Fig. 4. A baseline policy trained solely on canonical trajectory endpoints performs adequately under perfect initialization but degrades significantly under this noisy execution setting. In contrast, our full model which incorporates initial state perturbation during training maintains robust performance with no statistically significant drop in success rate ( _p >_ 0 _._ 05). This stability confirms that our data generation strategy effectively bridges the domain gap between the precision of the motion planner and the local generalization required by the policy. 

_2) Visual Robustness via Object-Centric Design:_ Next, we validate the design choices of our interaction module, focusing 

TABLE I 

**EVALUATION ON LIBERO-LONG++ AND ULTRA-LONG.** WE REPORT SUCCESS RATE (SR, %) AND AVERAGE PROGRESS (AP). **SUITE 1** TESTS ROBUSTNESS TO VISUAL CLUTTER. **SUITE 2** TESTS SCALABILITY (UP TO 16 SKILLS). <mark>G</mark> RAY COLUMNS INDICATE AVERAGE PERFORMANCE. 

||**Sui**|**te 1: Vis**|**ual Clutte**|**r (LIBE**|**RO-Long**|**++)**|||**Suite 2**|**: Scalabil**|**ity (Ultra**|**-Long)**|||**Ove**|**rall**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|_Orig_|_inal_|_Vari_|_ant_|_Av_|_g._|_Orig_|_inal_|_Varia_|_nt 1_|_Vari_|_ant 2_|_A_|_vg._|**Av**|**g.**|
||**SR**|**AP**|**SR**|**AP**|**SR**|**AP**|**SR**|**AP**|**SR**|**AP**|**SR**|**AP**|**SR**|**AP**|**SR**|**AP**|
|_Baselines_|||||||||||||||||
|Pi0.5|**83%**|**93%**|0%|0%|42%|46%|0%|1%|0%|0%|0%|0%|0%|0.3%|28%|31%|
|OpenVLA-OFT|7%|11%|0%|0%|3%|5%|0%|0%|0%|0%|0%|0%|0%|0%|2%|4%|
|_Ablations_|||||||||||||||||
|w/o Reaching|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|0%|
|w/o Masking|67%|80%|77%|87%|72%|83%|0%|16%|0%|32%|0%|10%|0%|20%|48%|64%|
|w/o Recovery|2%|25%|23%|59%|13%|42%|0%|16%|0%|16%|0%|21%|0%|18%|8%|33%|
|**LiLo-VLA (ours)**|78%|88%|**85%**|**89%**|**82%**|**89%**|**53%**|**79%**|**37%**|**84%**|**43%**|**74%**|**44%**|**79%**|**69%**|**86%**|


on viewpoint selection and visual augmentation. To evaluate resilience to visual disturbances, we conduct experiments on the BOSS-C1 benchmark [41], which stress-tests policies against Observation Space Shift, defined as the phenomenon where changes in task-irrelevant visual predicates within the observation space disrupt the performance of a learned policy. As shown in Fig. 5, the “Wrist Only” configuration achieves the highest absolute success rate on original tasks (0.88). We attribute this to the wrist-mounted perspective, where the target object occupies a larger portion of the field of view, facilitating feature extraction compared to global views. Crucially, under OSS conditions, the “Wrist Only” configuration also exhibits the lowest Ratio Performance Delta (15.9%) compared to “Both Views” (18.8%) and “3rd Person” (29.8%). This confirms that the wrist view is inherently more robust to background clutter and task-irrelevant changes in the environment. 


Fig. 5. **Comparison across different camera configurations.** Our wrist-only design achieves the highest success rate with the minimal performance drop under OSS. 

Complementing the viewpoint choice, the “w/o Masking” row in Table I highlights the necessity of our visual augmentation. Removing the random erasing strategy leads to a sharp decline in the overall success rate from 69% to 48%. This significant drop indicates that even with a wrist camera, the policy’s receptive field inevitably includes environmental distractors. Explicitly masking these irrelevant regions during training is therefore essential to strictly enforce objectcentricity and prevent the policy from overfitting to spurious visual features. 

_3) Efficacy of Closed-Loop Recovery:_ Finally, we examine the role of our closed-loop recovery mechanism. The “w/o Recovery” row in Table I reveals that removing this module leads to a catastrophic performance drop, with the overall average success rate plummeting from 69% to 8%. This failure is particularly absolute in the ultra-long tasks of Suite 2, where the success rate collapses to 0% without recovery compared to 44% with the full system. This dramatic difference demonstrates that closed-loop recovery is not merely an optimization but a structural prerequisite for scaling to extended horizons, where open-loop execution inevitably fails due to cumulative errors. 

### V. REAL ROBOT EXPERIMENTS 

### _A. Real-World System Implementation_ 

We implement **LiLo-VLA** on a Franka Emika Panda robot equipped with a Robotiq 2F-85 parallel gripper. Following the standardized hardware protocol of DROID [20] we utilize a dual-camera setup where a static third-person ZED 2 stereo camera provides global context for the Reaching Module and a wrist-mounted ZED Mini camera captures egocentric data for the Interaction Module. 

To transition from the oracle perception used in simulation to the unstructured real world we deploy a modular perception stack. We utilize YOLOE [38] for open-vocabulary object detection and segmentation coupled with FoundationPose [39] to estimate the 6D pose of target objects. This geometric information is ingested by the Reaching Module to generate collision-free motion plans to the target vicinity. 

Complementing our simulation experiments which utilized OpenVLA-OFT [22], we deploy **LiLo-VLA** with the Pi0.5 [18] backbone in the real world. This architectural switch empirically validates the model-agnostic nature of our framework demonstrating that the modular benefits of **LiLo-VLA** can enhance diverse VLA architectures without modification. 


Fig. 6. **Real-World Experimental Evaluation.** We evaluate LiLo-VLA on 8 tasks ranging from 4 to 8 steps. To test generalization, we introduce: “Standard” configurations (Task 1-3), “Diverse Layouts” with more complex background and large layout variation (Task 4-5), and “Change Sequence” with permuted skill orders. The quantitative results (top right) demonstrate that LiLo-VLA maintains robust performance across all variations. 

To train this policy we collect a minimal set of teleoperated demonstrations covering only atomic skills without any longhorizon sequence data. Finally due to the severe occlusions and visual clutter inherent in our evaluation tasks, we employ a human-in-the-loop protocol for success verification of each skill. 

### _B. Evaluation Tasks: Stress-Testing Generalization_ 

To evaluate the zero-shot generalization capabilities of **LiLo-VLA** in the physical world, we design three longhorizon tasks of increasing complexity as illustrated in Fig. 6. Task 1 and Task 2 each consist of 4 atomic skills, while Task 3 represents an ultra-long sequence chaining 8 atomic skills to push the limits of temporal scalability. 

Beyond the Standard evaluation where tasks are executed in canonical configurations, we introduce two variant protocols to stress-test specific generalization axes. The first protocol, _Diverse Layout_ (Variant 1), is applied to Tasks 1 and 2. Here we drastically alter the initial workspace layout and introduce previously unseen visual distractors. This setting evaluates the robustness of the Object-Centric VLA against visual clutter. The second protocol, _Change Sequence_ (Variant 2), is applied across all three tasks. We permute the execution order of the atomic skills forcing the system to generate novel long-horizon behaviors that were never seen during data collection. This protocol strictly tests compositional generalization distinguishing true skill understanding from trajectory memorization. 

### _C. Results Analysis_ 

We report the quantitative results in Fig. 6 based on 5 evaluation trials per configuration. Under Standard conditions **LiLo-VLA** achieves a 100% success rate across all three tasks demonstrating effective sim-to-real transfer. When introduced to the “Diverse Layout” protocol the system exhibits strong resilience to spatial shifts and visual distractors maintaining a 100% success rate on Task 1 and 80% on Task 2. This stability validates the robustness of our object-centric Interaction Module against environmental noise. Furthermore under the “Change Sequence” protocol performance remains robust even when atomic skills are permuted into different orders. In the 8-step ultra-long Task 3 the system maintains a 60% success rate with 85% average progress. Collectively these results confirm that **LiLo-VLA** enables robust real-world manipulation capable of handling severe visual clutter and flexible skill composition. 

### VI. CONCLUSION AND LIMITATIONS 

In this work, we introduced **LiLo-VLA** , a modular framework that integrates a Reaching Module for global transport with an Interaction Module for local manipulation. By incorporating a closed-loop recovery mechanism our system effectively addresses observation space shifts and achieves robust performance in both simulation benchmarks and realworld deployments. 

Despite these advancements, our reliance on external perception models introduces limitations where accurate detection 

of transparent or severely occluded objects remains challenging. Additionally, the overall system performance is bounded by the atomic proficiency of the underlying VLA backbone. Future work will investigate active perception strategies that autonomously navigate to the most favorable viewpoints for execution, thereby mitigating visual occlusions and maximizing the performance of the VLA policy. 

### REFERENCES 

- [1] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 

- [2] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ . 

- [4] Shuo Cheng and Danfei Xu. League: Guided skill learning and abstraction for long-horizon manipulation. _IEEE Robotics and Automation Letters_ , 8(10):6451– 6458, 2023. 

- [5] Shuo Cheng, Caelan Reed Garrett, Ajay Mandlekar, and Danfei Xu. NOD-TAMP: Generalizable long-horizon planning with neural object descriptors. In _8th Annual Conference on Robot Learning_ , 2024. URL https:// openreview.net/forum?id=rThtgkXuvZ. 

- [6] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- [7] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 2024. 

- [8] Murtaza Dalal, Tarun Chiruvolu, Devendra Chaplot, and Ruslan Salakhutdinov. Plan-seq-learn: Language model guided rl for solving long horizon robotics tasks. _arXiv preprint arXiv:2405.01534_ , 2024. 

- [9] Murtaza Dalal, Min Liu, Walter Talbott, Chen Chen, Deepak Pathak, Jian Zhang, and Ruslan Salakhutdinov. Local policies enable zero-shot long-horizon manipulation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13875–13882. IEEE, 2025. 

- [10] Yiguo Fan, Pengxiang Ding, Shuanghao Bai, Xinyang Tong, Yuyang Zhu, Hongchao Lu, Fengqi Dai, Wei Zhao, Yang Liu, Siteng Huang, et al. Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation. _arXiv preprint arXiv:2508.19958_ , 2025. 

- [11] Yunhai Feng, Jiaming Han, Zhuoran Yang, Xiangyu Yue, Sergey Levine, and Jianlan Luo. Reflective planning: Vision-language models for multi-stage long-horizon robotic manipulation. _arXiv preprint arXiv:2502.16707_ , 2025. 

- [12] Caelan Reed Garrett, Rohan Chitnis, Rachel Holladay, Beomjoon Kim, Tom Silver, Leslie Pack Kaelbling, and Tom´as Lozano-P´erez. Integrated task and motion planning. _Annual review of control, robotics, and autonomous systems_ , 4(1):265–293, 2021. 

- [13] RK Guo, Xinsong Lin, Minghua Liu, Jiayuan Gu, and Hao Su. Mplib: a lightweight motion planning library. 

- [14] Yanjiang Guo, Yen-Jen Wang, Lihan Zha, and Jianyu Chen. Doremi: Grounding language model by detecting and recovering from plan-execution misalignment. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 12124–12131. IEEE, 2024. 

- [15] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- [16] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv:2207.05608_ , 2022. 

- [17] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 

- [18] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0. 5: a vision-language-action model with open-world generalization, 2025. _URL https://arxiv. org/abs/2504.16054_ , 1(2):3. 

- [19] Leslie Pack Kaelbling and Tom´as Lozano-P´erez. Hierarchical task and motion planning in the now. In _2011 IEEE international conference on robotics and automation_ , pages 1470–1477. IEEE, 2011. 

- [20] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- [21] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: 

An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [22] Moo Jin Kim, Chelsea Finn, and Percy Liang. Finetuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- [23] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. _arXiv preprint arXiv:2209.07753_ , 2022. 

- [24] Jacky Liang, Mohit Sharma, Alex LaGrassa, Shivam Vats, Saumya Saxena, and Oliver Kroemer. Search-based task planning with learned skill effect models for lifelong robotic manipulation. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 6351–6357. IEEE, 2022. 

- [25] Kevin Lin, Christopher Agia, Toki Migimatsu, Marco Pavone, and Jeannette Bohg. Text2motion: From natural language instructions to feasible plans. _Autonomous Robots_ , 47(8):1345–1365, 2023. 

- [26] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776– 44791, 2023. 

- [27] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [28] Zeyi Liu, Arpit Bahety, and Shuran Song. Reflect: Summarizing robot experiences for failure explanation and correction. _arXiv preprint arXiv:2306.15724_ , 2023. 

- [29] Ajay Mandlekar, Caelan Reed Garrett, Danfei Xu, and Dieter Fox. Human-in-the-loop task and motion planning for imitation learning. In _Conference on Robot Learning_ , pages 3030–3060. PMLR, 2023. 

- [30] Utkarsh Aashu Mishra, Shangjie Xue, Yongxin Chen, and Danfei Xu. Generative skill chaining: Long-horizon skill planning with diffusion models. In _Conference on Robot Learning_ , pages 2905–2925. PMLR, 2023. 

- [31] Nived Rajaraman, Lin Yang, Jiantao Jiao, and Kannan Ramchandran. Toward the fundamental limits of imitation learning. _Advances in Neural Information Processing Systems_ , 33:2914–2924, 2020. 

- [32] St´ephane Ross, Geoffrey Gordon, and Drew Bagnell. A reduction of imitation learning and structured prediction to no-regret online learning. In _Proceedings of the fourteenth international conference on artificial intelligence and statistics_ , pages 627–635. JMLR Workshop and Conference Proceedings, 2011. 

Lozano-P´erez, and Leslie Pack Kaelbling. Learning neuro-symbolic skills for bilevel planning. _arXiv preprint arXiv:2206.10680_ , 2022. 

   - [35] Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. Progprompt: Generating situated robot task plans using large language models. _arXiv preprint arXiv:2209.11302_ , 2022. 

   - [36] Generalist AI Team. Gen-0: Embodied foundation models that scale with physical interaction. _Generalist AI Blog_ , 2025. https://generalistai.com/blog/nov-04-2025GEN-0. 

   - [37] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

   - [38] Ao Wang, Lihao Liu, Hui Chen, Zijia Lin, Jungong Han, and Guiguang Ding. Yoloe: Real-time seeing anything, 2025. URL https://arxiv.org/abs/2503.07465. 

   - [39] Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17868–17879, 2024. 

   - [40] Kechun Xu, Zhenjie Zhu, Anzhe Chen, Shuqi Zhao, Qing Huang, Yifei Yang, Haojian Lu, Rong Xiong, Masayoshi Tomizuka, and Yue Wang. Seeing to act, prompting to specify: A bayesian factorization of vision language action policy. _arXiv preprint arXiv:2512.11218_ , 2025. 

   - [41] Yue Yang, Linfeng Zhao, Mingyu Ding, Gedas Bertasius, and Daniel Szafir. Boss: Benchmark for observation space shift in long-horizon task. _IEEE Robotics and Automation Letters_ , 2025. 

   - [42] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

   - [43] Zhun Zhong, Liang Zheng, Guoliang Kang, Shaozi Li, and Yi Yang. Random erasing data augmentation. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 34, pages 13001–13008, 2020. 

   - [44] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [33] Tom Silver, Rohan Chitnis, Joshua Tenenbaum, Leslie Pack Kaelbling, and Tom´as Lozano-P´erez. Learning symbolic operators for task and motion planning. In _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3182–3189. IEEE, 2021. 

- [34] Tom Silver, Ashay Athalye, Joshua B Tenenbaum, Tom´as 

## **Appendix for LiLo-VLA** 

### OVERVIEW 

This supplementary material provides comprehensive details supporting the main paper. Section VII presents qualitative visualizations of our real-world experiments, highlighting specific mechanisms for robustness and failure recovery. Section VIII defines the full atomic skill library and details the exact task sequences for the LIBERO-Long++ and UltraLong benchmarks. Section IX elaborates on the relative pose representation designed to ensure zero-shot generalization to novel workspace configurations. Section X offers a theoretical analysis of the combinatorial complexity involved in longhorizon tasks, demonstrating the data efficiency of our modular approach. Section XI outlines the training objectives, hyperparameters, and the success checker heuristics utilized in our implementation. Finally, Section XII describes the hardware specifications and perception models utilized in our real-world system. 

### _B. Real-World Rollout Visualizations_ 

We provide comprehensive visualizations of our real-world experiments in Fig. S1. The top panel displays successful execution rollouts for all 8 evaluation tasks, where we explicitly mark the active object of interest in green and all distractors in red. Note that for any specific atomic skill, there is only one target object; consequently, all other objects in the scene, including targets for other skills, are treated as distractors, highlighting the robustness of our object-centric policy against clutter. 

To explain LiLo-VLA’s robustness, we visualize two core mechanisms. First, for perception, Fig. S2 shows the wrist camera inputs. We apply random black masks to these images, which forces the policy to ignore background clutter and focus only on the target object. Second, for execution, Fig. S3 shows the recovery process. After grasp failures in Frames 1 and 4, the system re-estimates the object’s new pose and uses the Reaching Module to reset the arm to the approach pose (Frames 3 and 6). This allows the Interaction Module to retry the skill, eventually leading to a success (Frame 7). 

### VIII. BENCHMARK DETAILS 

### VII. ADDITIONAL EXPERIMENTAL RESULTS 

### _A. Real-World Task Specifications_ 

To evaluate the compositional generalization of LiLo-VLA, we define a library of 8 unique atomic skills across three distinct scenes. Table S1 defines these primitives, while Table S2 details the exact execution sequences for all 8 evaluation tasks. 

### _A. Atomic Skill Library_ 

We define a comprehensive library of 22 atomic skills used across LIBERO-Long++ and Ultra-Long suites. To facilitate concise task specification, we assign a unique label to each skill in Table S3. 

TABLE S3 

SIMULATION ATOMIC SKILL LIBRARY (LIBERO-LONG++ AND ULTRA-LONG) 

TABLE S1 

REAL-WORLD ATOMIC SKILL LIBRARY 

|**Label**|**Object-Centric Instruction**|
|---|---|
|_S_1|“pick the tape”|
|_S_2|“hang the tape”|
|_S_3|“pick the red cup”|
|_S_4|“place the red cup on the plate”|
|_S_5|“pick the yellow mustard”|
|_S_6|“place the yellow mustard in the basket”|
|_S_7|“pick the corn”|
|_S_8|“place the corn in the basket”|


|**ID**|**Skill Description**|**ID**|**Skill Description**|
|---|---|---|---|
|_S_1|Pick Alphabet Soup|_S_12|Pick Moka Pot|
|_S_2|Place Alphabet Soup in Basket|_S_13|Place Moka Pot on Stove|
|_S_3|Pick Cream Cheese|_S_14|Turn On Stove|
|_S_4|Place Cream Cheese in Basket|_S_15|Pick Butter|
|_S_5|Pick Tomato Sauce|_S_16|Place Butter in Basket|
|_S_6|Place Tomato Sauce in Basket|_S_17|Pick Chocolate Pudding|
|_S_7|Pick Black Bowl|_S_18|Place Chocolate Pudding Right<br>of Plate|
|_S_8|Place Black Bowl on Plate|_S_19|Pick White Mug|
|_S_9|Stack Black Bowl on Black<br>Bowl|_S_20|Place White Mug on Plate|
|_S_10|Place Black Bowl in Bottom<br>Drawer|_S_21|Pick Yellow and White Mug|
|_S_11|Close Bottom Drawer|_S_22|Place Yellow and White Mug<br>on Right Plate|


TABLE S2 

DETAILED TASK SPECIFICATIONS FOR REAL-WORLD 

|**Task ID**|**Type**|**Steps**|**Skill Sequence**|
|---|---|---|---|
|Task 1|Standard|4|_S_1 _→S_2 _→S_3 _→S_4|
|Task 2|Standard|4|_S_3 _→S_4 _→S_5 _→S_6|
|Task 3|Standard|8|_S_7 _→S_8 _→S_5 _→S_6 _→_<br>_S_3 _→S_4 _→S_1 _→S_2|
|Task 4|Clutter|4|_S_1 _→S_2 _→S_3 _→S_4|
|Task 5|Clutter|4|_S_3 _→S_4 _→S_5 _→S_6|
|Task 6|Permuted|4|_S_3 _→S_4 _→S_1 _→S_2|
|Task 7|Permuted|4|_S_5 _→S_6 _→S_3 _→S_4|
|Task 8|Permuted|8|_S_3 _→S_4 _→S_1 _→S_2 _→_<br>_S_7 _→S_8 _→S_5 _→S_6|


### _B. Detailed Task Specifications_ 

We provide the exact atomic skill sequences for all evaluation tasks in Table S4. All skill IDs (e.g., _S_ 1 _, S_ 12) correspond to the definitions in the Atomic Skill Library (Table S3). 

For Suite 1 (LIBERO-Long++), we define 6 core tasks focused on robustness and reordering. Each task consists of a Standard sequence and a corresponding Variant, where the latter permutes the execution order of atomic skills to evaluate the policy’s zero-shot compositional generalization. 

For Suite 2 (Ultra-Long), we define 3 complex long-horizon scenarios to evaluate extreme temporal scalability. Each scenario includes one Standard sequence and two additional 


Fig. S1. **Qualitative Real-World Experimental Results.** 

Variant sequences. Notably, the “Table Organization” task extends up to 16 steps, serving as a rigorous stress test for the system’s ability to maintain coherent execution over extended horizons. 

### IX. EXTENDED METHODOLOGY DETAILS 

While the main text details our object-centric visual processing, the handling of proprioception is equally critical for generalization. To further enforce an object-centric inductive bias in our simulation backbone (OpenVLA-OFT), we transform the standard absolute end-effector pose into a relative frame. Specifically, the policy input is computed as _Tobj_<sup>_ee_=(</sup><sup>_T obj_</sup> _world_<sup>)</sup><sup>_−_1</sup><sup>_T ee_</sup> _world_<sup>,where</sup><sup>_T ee_</sup> _world_<sup>and</sup><sup>_T obj_</sup> _world_<sup>repre-</sup> sent the global poses of the end-effector and target object, respectively. This formulation renders the interaction policy invariant to global workspace shifts. In contrast, our realworld Pi0.5 policy operates directly in joint space and thus does not utilize this Cartesian transformation. We empirically 

validate the robustness of this design by introducing random spatial perturbations of up to 20cm (where the object’s position is randomly placed within this range); the system maintains strong performance with no statistically significant degradation (overall success rate over all 22 atomic skills in S3 dropped only slightly from 0.80 to 0.75, _p >_ 0 _._ 05). 

### X. DATA EFFICIENCY AND COMBINATORIAL COMPLEXITY 

To rigorously feature the data efficiency advantage of LiLo-VLA over end-to-end baselines, we analyze the sample complexity required to generalize to novel long-horizon task sequences. Let a long-horizon task _T_ be composed of a set of atomic skills _S_ = _{s_ 1 _, s_ 2 _, . . . , sN }_ . In a Task and Motion Planning (TAMP) formulation, the valid execution orders are governed by causal dependencies, where the effect of a skill _si_ serves as a precondition for a subsequent skill _sj_ . These dependencies induce a partial ordering over _S_ , denoted as _≺_ . 


Fig. S2. **Visual Robustness.** Random masking on wrist camera inputs forces the policy to focus strictly on the target object effectively ignoring background clutter. 


Fig. S3. **Recovery Mechanism.** Upon detecting a grasp failure, the system autonomously re-estimates the object pose and resets the arm to retry the execution. 

**End-to-End Complexity.** An end-to-end policy _πe_ 2 _e_ must implicitly internalize these valid orderings from demonstration data. To achieve robust compositional generalization, the policy must observe sufficient coverage of the set of all valid linearizations (i.e., topological sorts) consistent with the partial order _≺_ . For a task involving _M_ independent objects, each requiring a pick-place sequence, the number of valid <u>(2</u> _M_ <u>)!</u> linearizations can be as large as Θ � 2<sup>_M_</sup> � when objects have no inter-dependencies. For our ultra-long tasks ( _N_ = 16, _M_ = 8), this combinatorial explosion renders it intractable to cover the distribution of valid trajectories via demonstrations alone. 

**Modular Complexity (LiLo-VLA).** In contrast, LiLo-VLA decouples the task into independent atomic execution units. Since our Interaction Module _πint_ is strictly object-centric and conditioned only on the immediate target, the learning problem reduces to mastering the set of unique atomic skills _U ⊆S_ . Consequently, the data requirement scales linearly, _O_ ( _|U|_ ), independent of the total horizon length _N_ or the combinatorial complexity of the task structure. For the 16-step “Table Organization” task, this reduces the learning problem from covering millions of potential trajectory variations to simply mastering the 9 unique atomic primitives listed in Table S1. 

XI. TRAINING AND IMPLEMENTATION DETAILS 

### _A. Training Objectives_ 

We employ two distinct training objectives corresponding to the different backbones used in our simulation and real-world 

experiments. 

**OpenVLA-OFT (Simulation).** For our simulation benchmarks, we utilize OpenVLA-OFT [22], which departs from the standard discrete tokenization used in original VLA models. Instead, it adopts a _continuous action representation_ and employs an Optimized Fine-Tuning (OFT) recipe that integrates parallel decoding and action chunking. Consequently, the model is trained via a regression objective rather than classification. We minimize the L1 loss between the predicted action chunk **a** ˆ _t_ : _t_ + _H_ and the ground-truth action sequence **a** _t_ : _t_ + _H_ : 


where _H_ is the action chunk size, and the model predicts the entire chunk in parallel conditioned on the observation _ot_ and instruction _l_ . 

**Pi0.5 (Real-World).** For real-world validation, we adopt the Pi0.5 backbone [18], which models the continuous action distribution using Conditional Flow Matching (CFM). The model learns a vector field _vθ_ that transports a Gaussian noise distribution _x_ 0 _∼N_ (0 _, I_ ) to the data distribution _x_ 1 (ground-truth actions) over a virtual time _τ ∈_ [0 _,_ 1]. The training objective minimizes the mean squared error between the predicted vector field and the target flow: 


where _ϕτ_ ( _x_ 0 _, x_ 1) = (1 _− τ_ ) _x_ 0 + _τx_ 1 represents the linear interpolation path. 

TABLE S4 

DETAILED TASK SPECIFICATIONS FOR SIMULATION BENCHMARKS 

|**Suite**|**Task Name**|**Steps**|**Skill Sequence (IDs from Table S3)**|
|---|---|---|---|
|**Suite 1: L**|**IBERO-Long++ (Robustness a**|**nd Reor**|**dering)**|
|Standard|T1: Stove and Moka|3|_S_14 _→S_12 _→S_13|
|Variant|T2: Stove and Moka|3|_S_12 _→S_13 _→S_14|
|Standard|T3: Soup and Cheese|4|_S_1 _→S_2 _→S_3 _→S_4|
|Variant|T4: Soup and Cheese|4|_S_3 _→S_4 _→S_1 _→S_2|
|Standard|T5: Soup and Tomato|4|_S_1 _→S_2 _→S_5 _→S_6|
|Variant|T6: Soup and Tomato|4|_S_5 _→S_6 _→S_1 _→S_2|
|Standard|T7: Cheese and Butter|4|_S_3 _→S_4 _→S_15 _→S_16|
|Variant|T8: Cheese and Butter|4|_S_15 _→S_16 _→S_3 _→S_4|
|Standard|T9: Two Mugs|4|_S_19 _→S_20 _→S_21 _→S_22|
|Variant|T10: Two Mugs|4|_S_21 _→S_22 _→S_19 _→S_20|
|Standard|T11: Mug and Pudding|4|_S_19 _→S_20 _→S_17 _→S_18|
|Variant|T12: Mug and Pudding|4|_S_17 _→S_18 _→S_19 _→S_20|
|**Suite 2: U**<br>|**ltra-Long (Scalability and Co**<br>|**mpositio**<br>|**nality)**<br>|
|Standard|T13: Kitchen Organization|9|_S_7 _→S_8 _→S_7 _→S_8 _→S_7 _→S_9 _→S_3 _→S_4 _→S_11|
|Variant 1|T14: Kitchen Org. (V2)|9|_S_3 _→S_4 _→S_7 _→S_8 _→S_7 _→S_9 _→S_7 _→S_8 _→S_11|
|Variant 2|T15: Kitchen Org. (V3)|9|_S_7 _→S_8 _→S_7 _→S_9 _→S_3 _→S_4 _→S_7 _→S_8 _→S_11|
|Standard|T16: Cooking Preparation|10|_S_14 _→S_12 _→S_13 _→S_14 _→S_12 _→S_13 _→S_7 _→S_8 _→S_7 _→S_8|
|Variant 1|T17: Cooking Prep. (V2)|10|_S_7 _→S_8 _→S_7 _→S_8 _→S_14 _→S_12 _→S_13 _→S_14 _→S_12 _→S_13|
|Variant 2|T18: Cooking Prep. (V3)|10|_S_7 _→S_8 _→S_14 _→S_12 _→S_13 _→S_7 _→S_8 _→S_14 _→S_12 _→S_13|
|Standard|T19: Table Organization|16|_S_5 _→S_6 _→S_5 _→S_6 _→S_1 _→S_2 _→S_1 _→S_2 _→S_3 _→S_4 _→S_3 _→S_4 _→S_7 _→S_10 _→S_7 _→S_8|
|Variant 1|T20: Table Org. (V2)|16|_S_1 _→S_2 _→S_5 _→S_6 _→S_1 _→S_2 _→S_5 _→S_6 _→S_3 _→S_4 _→S_3 _→S_4 _→S_7 _→S_10 _→S_7 _→S_8|
|Variant 2|T21: Table Org. (V3)|16|_S_1 _→S_2 _→S_1 _→S_2 _→S_5 _→S_6 _→S_5 _→S_6 _→S_3 _→S_4 _→S_3 _→S_4 _→S_7 _→S_10 _→S_7 _→S_8|


Fig. S4. **Real-world hardware setup** . Our system consists of a Franka Emika Panda arm, a wrist-mounted ZED mini camera for fine-grained interaction, and a fixed ZED 2i camera for global reaching. Compute is distributed between a local workstation (Perception/Control) and a remote cluster (VLA Inference). 

### _B. Training Hyperparameters_ 

We train a single multi-task policy for each domain: one OpenVLA-OFT model across the simulation atomic skill library and one Pi0.5 model across the real-world atomic skill library. Table S5 provides a comprehensive overview of the hyperparameters used for these trainings. 

### _C. Success Checker Heuristic Functions_ 

In our simulation experiments, the verification function _V_ ( _ai_ ) leverages ground-truth state information to evaluate skill execution. We primarily adopt the standard success predicates provided by the LIBERO benchmark. We create one success condition for the Pick skill: the skill is deemed successful only if the target object’s vertical position ( _z_ -axis) increases by at least 3 cm relative to its pre-execution state. For all other atomic skills, we retain the default LIBERO success conditions without modification. 

XII. HARDWARE AND SYSTEM SETUP 

### _A. Hardware Specifications_ 

Our real-world experimental setup follows the DROID hardware configuration standards. We use a 7-DoF Franka Emika Panda robotic arm equipped with a standard parallel jaw gripper (Robotiq 2F-85). The robot is operated using a joint impedance controller at a control frequency of 15 Hz. The vision system comprises two stereo cameras: a wrist-mounted Stereolabs ZED Mini for local object-centric observations and a single fixed third-person Stereolabs ZED 2 camera for global reaching. The VLA policy inference runs on a remote cluster node equipped with NVIDIA RTX A6000 GPUs, while all perception modules and real-time control loops operate on a local workstation equipped with a single NVIDIA RTX 4080 GPU. We visualize the complete physical setup in Fig. S4. 

TABLE S5 

HYPERPARAMETERS AND TRAINING CONFIGURATION. 

|**Hyperparameter**|**Simulation**<br>**(OpenVLA-**<br>**OFT)**|**Real-World**<br>**(Pi0.5)**|
|---|---|---|
|Base Model|OpenVLA-7B|Pi0.5 (DROID)|
|Action Representation|Continuous<br>(OFT)|Continuous<br>(Flow Matching)|
|Finetuning Method|LoRA|Full|
|Action Chunk Size (_H_)|8|16|
|Input Observation|Wrist<br>RGB<br>+|Wrist<br>RGB<br>+|
||Proprioception|Proprioception|
|Training Objective|L1 Regression|Flow Matching|
|Optimizer|AdamW<br>|AdamW<br>|
|Learning Rate|5_×_10<sup>_−_4</sup>|5_×_10<sup>_−_5</sup>|
|LR Schedule|Cosine Decay|Cosine Decay|
|Batch Size|64|32|
|Training Steps|100,000|30,000|
|Random Erasing|Enabled|Enabled|


### _B. Perception Models_ 

We utilize FoundationPose [39] for 6D pose estimation and YOLOE [38] for 2D object detection and segmentation. Both models operate in real-time to enable closed-loop feedback. FoundationPose tracks the target object pose using an RGB image, an instance segmentation mask, and a 3D CAD model. We obtain the necessary 3D meshes by scanning the physical objects with the AR Code mobile application. For object detection, we employ YOLOE with visual prompting. Instead of conditioning detection on natural language text descriptions, we provide a reference image with a bounding box of the target object. We find this visual prompting approach offers higher robustness against background clutter compared to open-vocabulary text prompts. 

