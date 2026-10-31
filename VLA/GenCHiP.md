---
title: "GenCHiP: Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks"
date: "2024"
venue: "IROS 2024"
url: https://doi.org/10.1109/IROS58592.2024.10801525
pdf: https://arxiv.org/pdf/2404.06645
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2404.06645)** / [論文ページ](https://doi.org/10.1109/IROS58592.2024.10801525)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **GenCHiP: Gen** erating Robot Policy **C** ode for **Hi** gh- **P** recision and Contact-Rich Manipulation Tasks 

Kaylee Burns<sup>_∗_1</sup><sup>_,_2</sup> , Ajinkya Jain<sup>1</sup> , Keegan Go<sup>1</sup> , Fei Xia<sup>3</sup> , Michael Stark<sup>1</sup> , Stefan Schaal<sup>1</sup> , Karol Hausman<sup>2</sup><sup>_,_3</sup> 

**_Abstract_ — Large Language Models (LLMs) have been successful at generating robot policy code, but so far these results have been limited to high-level tasks that do not require precise movement. It is an open question how well such approaches work for tasks that require reasoning over contact forces and working within tight success tolerances. We find that, with the right action space, LLMs are capable of successfully generating policies for a variety of contact-rich and high-precision manipulation tasks, even under noisy conditions, such as perceptual errors or grasping inaccuracies. Specifically, we reparameterize the action space to include compliance with constraints on the interaction forces and stiffnesses involved in reaching a target pose. We validate this approach on subtasks derived from the Functional Manipulation Benchmark (FMB) and NIST Task Board Benchmarks. Exposing this action space alongside methods for estimating object poses improves policy generation with an LLM by greater than 3x and 4x when compared to non-compliant action spaces. More material is available on our project webpage: https://dex-code-gen.github.io/dex-code-gen/** 

## I. INTRODUCTION 

Many of the open problems in learning-based robotics revolve around the issue of scaling: deep-learning methods require vast datasets that are not readily available for robotics applications. One workaround for the data scarcity problem is to retrofit deep learning models that have been trained on internet-scale datasets from other modalities for robotics tasks. Recently, large language models (LLMs) have emerged as a strong candidate for this approach. LLMs are able to successfully generate code, complete numeric sequences, and solve common-sense reasoning tasks [1]–[4]. Because code is one of the most popular interfaces for specifying robotic planning and control commands, these capabilities hint at enormous potential when applied to robotics [1]. 

Past work demonstrates that generating robot policy code from LLMs is successful for high-level tasks such as navigation and open-vocabulary pick-and-place [1], [2]. For example, a language model can compose high-level action primitives like grab(chips) and move ~~t~~ o(human) to successfully generate a policy conditioned on a natural language command such as “bring me the chips” [1]. But at present, lower-level tasks and behaviors are generally considered out of reach for LLMs because, to the best of our knowledge, there are no compelling demonstrations of code generation that commands robots to perform contact-rich tasks. 

While various robot learning approaches have been able to demonstrate impressive generalization across different settings and target objects for pick-and-place tasks [5]–[10], 

*Correspondence to kayl@google.com 

> 1[Google] Intrinsic 2Stanford University 3Google DeepMind 

such generalization is arguably more difficult for dexterous tasks where a higher level of precision is required. For example, for a peg-in-hole insertion task, surfaces with more friction or tight insertion tolerances may require multiple insertion attempts or contact force tuning to reach the insertion site [11]. Similarly, pegs with different geometries may need different approach trajectories to achieve proper alignment: a peg with a star-shaped cross-section may require an initial rotation for insertion, whereas no such rotation is required for a circular peg. In practice, the parameters of contactrich insertion skills are mostly tuned by experts to handle these differences and automating this process is still an open problem. This presents a challenge for the approach taken in past work [1], which directly provides a language model with a library of high-level skills (such as insert(peg)). 

We present GenCHiP: a promising alternative for automating the parameter-tuning process within the control API by instead leveraging the world knowledge inside language models (LMs) to compose lower-level control primitives. Our goal is to understand if LLMs have the ability to reason about motions and forces acting on objects so as to enable generalization across a larger class of target objects and skills. To study this topic, we modify the action space in which an LLM operates by exposing constraints on the contact stiffness and forces observed during a high-precision task. With these modifications we can study code generation for contact-rich manipulation tasks, including industry relevant tasks such as high-precision insertion, rigid body assembly, and deformable object manipulation (see Fig. 1). 

The main contribution of this work is to demonstrate that LLMs, without any specialized training, have the ability to perform contact-rich tasks when given the appropriate action space. We develop a system for automatically generating robot policy code for dexterous tasks by allowing LLMs to specify constraints on the stiffnesses, forces, and trajectories required to perform contact-rich manipulation tasks. We show that our method, GenCHiP, is able to outperform a contact-unaware model by over 3x on average on subtasks developed from two challenging contact-rich benchmarks. Specifically, our approach is able to generate novel insertion patterns from high level descriptions of object shape and texture on insertion tasks from the Functional Manipulation Benchmark (FMB) [12], route and un-route cables in the style of the IROS 2020 Robotic Grasping and Manipulation Competition (IROS RGMC) [13], and complete a waterproof connector insertion task selected from the NIST Assembly Task Board #1 [14]. To the best of our knowledge, this is the first paper to provide a strong proof-of-concept that LLMs 


Fig. 1: (a) We prompt an LLM to generate code for high-precision tasks. By using an action space that paramterizes compliant behavior, the LLM is able to generate action sequences for contact-rich tasks like peg insertion. (b) Language models’ ability to reason about object geometry and make plans by using world knowledge about different object enables zero-shot generalization to new tasks. 

are capable of parameterizing robotic policies for precise, contact-rich manipulation tasks with code. 

<mark># You're a robot trying to insert a peg in a hole. Grab the circular peg. pick_up(circular_peg)</mark> 

## II. RELATED WORK 

**LLMs for robotics** can successfully generate robot policy code for pick-and-place style manipulation tasks [15], [16], compose mid-level plans for navigation tasks [3], and compose multiple navigation and manipulation skills for integrated household agents [17]–[19]. Many of these approaches rely on filtering LLM-generated code based on what is executable [20] or on making queries hierarchically [1], [10]. They also require a large number of prompt examples: for example, Huang, Wang, Zhang, _et al._ [21] makes use of eight different prompts with approximately nine subcommands per prompt. By contrast, in the Few-Shot example settings we describe in Sec. IV-A, we use a maximum of four examples in a given environment. Furthermore, none of these works establish whether or not LLMs can generate robot policy code for performing high-precision, contact-rich manipulation tasks, which we study in this work. 

**Contact-rich robot manipulation** tasks are those that involve a robot making controlled contact with its environment while performing them. These tasks constitute the vast majority of manipulation tasks in daily life, including household tasks such as wiping tables and sweeping dust into a dust-pan [22], and industrial tasks such as high precision insertion [11], [23], [24] and assembly [25], [26]. A robot needs to reason about the contact forces it will impart on and sense from the environment while performing such tasks to complete them successfully. Learning a general policy to perform a wide array of contact-rich manipulation tasks has been studied in great detail in robotics [23], [24], [27]–[32], yet how to find a general approach to these tasks remains an 

Fig. 2: We generate code by formatting natural language requests and instructions as comments. Generations are highlighted in blue. 

open question. Prior work directly learns policies with imitation learning [33] or reinforcement learning [25], [34], [35], but these require hundreds of human demonstrations, significant operator training, dedicated simulators, or thousands of environment interactions to achieve a performant policy. We step towards obtaining a general policy for contactrich manipulation tasks by leveraging the world knowledge inside LLMs and combining it with the appropriate task action spaces. We choose robot impedance (or equivalently, admittance) control as the action space for contact-rich manipulation tasks as it can regulate the relationship between robot position and contact forces effectively [36], [37]. 

## III. PRELIMINARIES 

Our goal is to develop a system that can translate natural language instructions into robotic actions by leveraging a sufficiently expressive API for control. Past work [1] shows that off-the-shelf language models can be adapted towards this goal with few-shot prompting. Concretely, pairs of natural language requests with corresponding robot policy code are fed into a language model. Then, the language model can output novel programs in response to new commands as shown in Fig. 2. The success of this approach can be attributed to the fact that during offline training on vast internet datasets, language models absorb world knowledge about common-sense interactions and learn mappings between natural language instructions and code. Strategies for 


Fig. 3: We present information about the task and control API via prompting. The API description is the same across all environments, the hints and examples are the same within each environment, while the task description must be modified to describe each task. 

adapting this approach towards a contact-rich setting are discussed in the next section. 

## IV. GENCHIP 

GenCHiP equips LLMs with a compliant action space. In this section, we first describe the prompting strategies that enable a language model to successfully paramterize and compose compliant move actions. Then, we discuss the different choices of action spaces that can be made available to a language model including our proposed action space. 

## _A. Prompting for contact-rich control_ 

We consider four prompting strategies when generating robot policy code from a language model: 

a. **Task descriptions** are high-level explanations of the scene and the task goal written in natural language. These can occur at both the beginning and end of a prompt and often include important information about the task setup such as the peg shape or the available objects. See Fig. 3a for an example. 

b. **Descriptions of available control APIs** are formatted doc-strings that describe code accessible to the LLM. These include lists of variables as well as the expected range of values for floating point numbers. Fig. 3b shows an example description for a simplified move function that controls endeffector pose. We also include descriptions for the full library of available methods, including a point-to-point move, a compliant move, conditions, gripper movements, and methods or variables specifying the positions of relevant objects. 


Fig. 4: Generating code with point-to-point moves limits policies to free-space-motions. For this policy to run successfully, displacement along the z-axis in the second and fifth actions must be exact. 

c. **Hints** in our setting include rules, keywords that specify relevant control primitives, and requests to have the model explain its reasoning in natural language or in pseudocode. Phrases such as “perform a pattern search” guide the model towards predicting behavior that better recovers from errors and better handles imprecision in the position of target poses. Intuitively these keywords help in reducing task ambiguity (e.g., by emphasizing that provided locations are imprecise) and guide the model towards motion patterns that are relevant to contact-rich tasks. Requests to explain in natural language can be thought of as a variant of chain-of-thought prompting [38]. The specific keywords and requests that are helpful in each task are described in the experimental section. 

d. **Examples** of the control APIs being used for basic movements, such as making contact with a surface, are useful for tasks with ambiguity or where the desired force constraints are difficult to infer from the given ranges. 

The combination of the prompt strategies described above allows us to prompt a language model with enough contextual information about the dexterous task at hand. Next, we discuss how we can design the action space of the robot to be able to perform such tasks in practice. 

## _B. Action spaces for robot manipulation tasks_ 

Past approaches assume access to a library of methods that exhaustively cover all user-requested commands [1], [2]. Building such a library is challenging for contact-rich tasks because in practice these policies are tuned by experts across different object geometries, frictions, and scene layouts. This section describes different approaches to parameterizing the control API and what the right choice of a control API can achieve. Formally, we consider a contact-rich robot manipulation task to be composed of a sequence of subtasks _τ_ = ( _t_ 1 _,...,tn_ ). The specific definition of a subtask will change based on the action space, as described below. 

**Point-to-point moves.** Past work [1], [2] makes use of an action space that directly commands the robot to move to target poses in the Cartesian space, [ **x** _target_ ] _i_ (See Fig. 4). In this setting, each sub-task _ti_ is simply defined as the next Cartesian pose (a.k.a. waypoint): _ti_ = ([ **x** _target_ ] _i_ ). 

While this approach is successful for executing motions in free-space or for simple pick-and-place tasks, it fails when the robot needs to explicitly make a purposeful contact with 


Fig. 5: Compliance prevents the robot from faulting when in contact. Conditional termination constraints enable the language model to reason about contact forces. In this example, the robot moves a cable back and forth until no more upward force is detected, which indicates that an opening has been found. 

its environment. Consider a robot trying to make contact with a surface to perform a wiping motion. Successfully parameterizing a policy in this action space would require predicting a precise Cartesian pose with very little tolerance for error. Predicting a pose that is millimeters short of the surface would fail to make a contact and predicting millimeters too deep into the surface would cause the robot to exert high forces on the surface, which can cause faults in the robot or even break it in the worst case scenario. 

**Compliant moves.** Addressing this shortcoming, we propose to parameterize the action space for performing contact-rich manipulation tasks using a robot’s compliance, realized in impedance control (or equivalently admittance control which is an adequate action space for robot learning in Mart´ınMart´ın, Lee, Gardner, _et al._ [39]). An impedance move action is parameterized by both a target Cartesian pose, [ **x** _target_ ] _i_ , and a vector that specifies stiffness along each degree of freedom, _σi_ : _ti_ = ([ **x** _target_ ] _i, σi_ ), when the robot is in contact with the environment. During execution, the stiffness vector for each subtask can be used to define the parameters for a variable impedance controller [40] of the form: 


where **x** _target_ , **x** , **x** ˙ _target_ , **x** ˙, **x** ¨ _target_ , and **x** ¨ denote the target and current pose, twist, and accelerations, respectively. _Kp_ , _Kd_ , and Λ correspond to the stiffness, damping, and taskspace inertia matrices, respectively. The impedance controller realizes that the end-effector in contact with the environment behaves like the linear spring-damper-mass system above. _Kp_ , _Kd_ , and Λ are computed as a function of our specified stiffness vector _σi_ (explained below) and robot specific parameters in order to achieve stable yet responsive behavior. 

Intuitively, the stiffness vector determines the interaction forces that the robot will impart on its environment while performing the task. Low stiffness coefficients in _σ_ regulate the robot’s compromise between contact forces and the attempt to achieve position accuracy. In the example that we 

discussed in the last paragraph, a low stiffness value would enable the robot to maintain gentle contact with a surface that prevents the robot from reaching a desired position. A higher stiffness value would create higher contact forces, equivalent to a higher priority to reduce position error. 

**Conditional compliant moves.** In addition to the impedance control specification described above, we also allow the LLM to specify conditions under which to terminate an impedance move. Specifically, these are thresholds on force or position in a specified coordinate direction. Example pseudocode is presented in Fig. 5. This is a powerful primitive as it enables the robot to construct recipes for high-precision tasks without relying on fine-grained perception. In the example of making contact with a surface, this may look like moving a peg downwards with a termination constraint on upward force. 

## V. EXPERIMENTS 

In this section, we evaluate the ability of GenCHiP to generate code for fine-grained manipulation tasks that require high precision in a series of experiments on a set of real robotic tasks. Specifically, we evaluate on a subset of highprecision contact-rich manipulation tasks from the Functional Manipulation Benchmark (FMB) [12] and a set of industrial manipulation tasks selected from the NIST Assembly Task Board #1 [14] and the IROS 2020 Robotic Grasping and Manipulation Competition (IROS RGMC) [13] (Sec. V- A). Later, we ablate prompt hints to study the utility of incorporating additional hints in generating relevant motion patterns for robot manipulation tasks (Sec. V-B). 

## _A. Contact-rich manipulation tasks_ 

Sec. V-A.1 details the task setup considered in our experiments, while baselines and ablations are discussed in Sec. V-A.3. We discuss experimental results in Sec. V-A.5. 

_1) Task description:_ The **Functional Manipulation Benchmark** [12] studies robotic manipulation, grasping, reorienting, and assembling of a set of dozens of 3D printed objects. The benchmark emphasizes generalization across different object shapes and positions. We evaluate our approach on a subset of peg insertion tasks across three different object shapes: the circle, star, and half-pipe. We use scripted motion to bring the pegs into a fixed position over the insertion point and program a randomized rotation about the z-axis. There is no rotation for the circular peg because it has a constant radius. Rotation of the star is sampled uniformly between 0 and<sup>_<u>π</u>_</sup> 2<sup>.Rotationofthehalfpipeissampleduniformlyfrom</sup> either 0 or _π_ . Inserting these peg shapes successfully requires generating search patterns contingent on object geometry. 

**Industrial Manipulation Tasks** are adapted from the NIST Assembly Task Board #1 [14] and the IROS RGMC 2020 [13]. These benchmarks are designed to evaluate proficiency in robotic assembly with an emphasis on small and medium sized parts and deformable objects. We consider the wire routing and connector insertion subtasks. Specifically, we study routing (insertion) and unrouting 


Fig. 6: Left: The Functional Manipulation Benchmark (FMB) [12] and a modified assembly board with tasks sourced from NIST Assembly Task Board #1 [14] and IROS RGMCS 2020 [13] we used for experimentation. Both environments have relatively tight tolerances. Right: Example of the rollouts produced by our method for two tasks: the waypoints from GenCHiP are able to successfully complete the tasks. 

(removal) of a wire through a plastic channel component and inserting a waterproof connector plug into a socket. Task environments are visualized in Fig. 6. Note there are multiple sources of noise across episodes. For example, in the orientation of the cable within the grasp of the gripper, the tautness of the cable, and the estimated poses of the waterproof connector. Additionally, we evaluate on each side of the routing component to verify that the pattern works across starting positions. An ideal method should result in an execution policy that is robust to such sources of noise. 

_2) Implementation details:_ We conduct our robot experiments on a Universal Robotics UR5e robot, which is a position-controlled robot with ATI Axia80 force-torque sensor at the wrist. To expose the compliant action space to the language model, we prompt it with the doc-string for a Cartesian admittance move with parameters on stiffnesses, impedances, and constraints in reaching a target pose. We add a suffix describing the details of the given task, optionally including certain keywords about relevant motion patterns when the environment setup is ambiguous (e.g., we specify that the peg in the FMB insertion tasks is not aligned, which requires the policy to search for the opening). 

We give the LLM access to methods for computing transformations on reference poses (i.e., pose ~~m~~ ultiply) and for detecting objects in the environment (i.e., estimate ~~a~~ nd ~~u~~ pdate ~~p~~ ose). To support the latter, we train pose estimators to do joint object detection and keypoint prediction using a Faster-RCNN [41] architecture. 

_3) Methods considered:_ We compare two classes of methods: a scripted baseline policy authored by an expert and different variants of LLM-generated code using the prompting strategies and control APIs outlined in Sec. IV-A and Sec. IV-B. For LLM-generated code, we compare with and without code examples. For zero-shot settings, the prompt 

includes includes Task Descriptions (Fig. 3a), Control API Descriptions (Fig. 3b), and Hints (Fig. 3c). In few-shot settings, Examples (Fig. 3d) are added to the prompt. 

**Scripted [Baseline].** We compare against a scripted pattern search insertion move that is tuned by an expert on a single task setting. This baseline reflects an alternative to our approach where a single skill is added to our control library, but is not able to be tuned by an expert across different task generalizations. On FMB tasks, we adapt a pattern search insertion skill for peg insertion. The scripted move implements fixed get-in-contact, pattern search, and insertion phases, with durations, motion patterns, and force thresholds set by an expert on the circle setting. 

**Code-as-Policies (CaP) [1] [Baseline].** We compare with a baseline approach akin to the prior work [1], [2] that uses the point-to-point action space for performing robot manipulation tasks, i.e. to directly command the robot to move to Cartesian target poses (Fig. 4). 

**GenCHiP, Fixed Compliance (FC).** For each task, we compare against a baseline where we do not expose the stiffness and impedance targets or the force constraints to the LLM planner, but instead, use predefined compliance parameters. This ablates the importance of force constraints in completing the task, making the action space similar to prior work [1], but with compliant motions. Concretely, we provide a modified prompt and access to a wrapper around the Cartesian admittance move that provides fixed stiffness and impedance targets and a fixed translation error constraint. 

**GenCHiP (Few-Shot).** We expose force constraints to the language model and add examples of calls to our control API, which includes conditional compliant moves. This is similar to the GenCHiP, Fixed Compliance baselines, but all of the force constraints and termination conditions are exposed to the language model (Fig. 5). In these experiments, each 

||Circle|Star|Half-Pipe|
|---|---|---|---|
|Scripted|**100%**|10%|0%|
|CaP [1] (Zero-Shot)|70%|0%|0%|
|GenCHiP, FC (Zero-Shot)|**100%**|70%|30%|
|**GenCHiP** (Zero-Shot)|**100%**|**80%**|**50%**|


TABLE I: **Functional Manipulation Benchmark. [12]** Compared to a scripted policy, GenCHiP is better able to generalize an insertion pattern across object geometries, including the challenging half-pipe task. We show average performance across 10 evaluations. 

“shot” is an example subcommand that shows how to call the API. In the IROS RGMCS tasks, we include 3 example subcommands: moving down until contact, moving up until a snag, and moving right until a snag is detected. 

**GenCHiP (Zero-Shot).** We follow the same approach of exposing force constraints to the language model as GenCHiP (Few-Shot, Fig. 5), but do not include any examples that call the control APIs. This is the most difficult generalization setting because every command is an unseen command. _4) Evaluation Protocol:_ Similar to Yu, Gileadi, Fu, _et al._ [42], we take the best completion out of 5 calls to the underlying language model and run 10 evaluations. All of our experiments use the OpenAI ChatCompletions API [43] with the gpt-4-0613 endpoint and a temperature of 0.0. To make comparisons between different action spaces as fair as possible, we take the most successful code generated from our method and overwrite the control API to implement the relevant action space. For each environment, we tune the insertion reference pose that appears in the prompt. Concretely, this is the reference pose used in to make contact in the admittance move. This hyperparameter is essential on the Point-to-Point baseline because insertion reference poses that are too deep cause a fault. 

_5) Results:_ **Functional Manipulation Benchmark.** Our first evaluation studies how well different approaches generalize across unseen task settings, in particular, the ability to modify insertion search patterns based on different object geometries. Results on FMB are listed in Tab. I. 

We find that GenCHiP outperforms the performance of other methods across different peg shapes. The baseline scripted policy is successful on the star only when the points are already in close-enough alignment with the hole and fails on the half-pipe shape, which is the most difficult to align because there is only one valid orientation for a successful insertion. In contrast, our method is successful on half-pipe 50% of the time. Upon further analysis, we notice that this is because GenCHiP generates a successful policy in only one direction of rotation (i.e., 100% successful for one rotation and 0% successful for the other randomized rotation). 

When we inspect the code output from the LLM, we find that it generates intuitive waypoints for the search that correspond to the object specified in the prompt. For example, for the half-pipe, the output waypoints oscillate between 0 and<sup>_<u>π</u>_</sup> 2 while the star shape policy goes through multiples of<sup>_<u>π</u>_</sup> 4<sup>.We</sup> also find that the zero-shot prompting setup is sufficient for 

||Cable<br>Unroute|Cable <br> Route|Connector<br>Insertion|Connector<br>Insertion<br>(Perception)|
|---|---|---|---|---|
|CaP [1] (Few-Shot)|40%|0%|0%|0%|
|GenCHiP, FC (Few-Shot)|80%|30%|20%|0%|
|GenCHiP (Zero-Shot)|60%|0%|0%|0%|
|**GenCHiP** (Few-Shot)|**90%**|**100%**|**90%**|**60%**|


TABLE II: **RGMC [13] and NTB [14] Assembly Tasks.** On challenging manufacturing tasks, it’s critical to have compliance and conditional terminations in the action space. GenCHiP outperforms other LLM-based code-generation approaches for this reason. 


Fig. 7: We classify error types across three levels of hints. The severity of errors decreases from left to right. After combining all hints, the most common error is correct specification of force values. 

this application. Out of the box, the language model is able to parameterize the conditional compliant move. 

**Industrial Manipulation Tasks.** To validate our method on more realistic force-based manipulation environments, we turn to the IROS RGMC [13] and NIST Assembly [14] experiments, which are arguably more directly targeted towards force-based manipulation than the peg insertion task. Indeed, we find it difficult to design an analogous scripted policy baseline for cable (un-)routing that would perform well across both tasks, which is why we omit it in this experiment. From the results in Table II, we observe that GenCHiP (Few-Shot) again consistently outperforms the baselines. Fixed Compliance (Few-Shot) is second-best, while Code-asPolicies [1] (Few-Shot) performs worst, failing to complete the routing task even a single time. The Zero-Shot version of our method also fails for these tasks, and for two reasons: (1) the LLM tends to generate while loops that are incompatible with the way the API is structured and (2) the program is successful within a narrow range of force values that are difficult to infer without more information from examples. 

In the connector insertion task, we consider two cases: with and without fixed object placement. In the absence of fixed object placement, we estimate the plug and socket reference poses using pose estimators, which can reduce their accuracy by a small margin ( _ε ≤_ 4mm). Our method succeeded in maintaining a reasonable success rate in this case as well. 

## _B. Ablating prompt hints_ 

In the experiments underlying Sec. V-A.5, we observed that incorporating additional hints is critical in eliciting relevant motion patterns. To understand this phenomenon in depth, we plot the distribution over error types for increasing levels of hints on the cable un-routing task in the Zero-Shot setting. We use three hint types: specifically asking for a pattern search, adding extra rules about accessing undefined variables, and asking the model to translate from pseudocode, similar to Chain-of-Thought prompting [44]. Fig. 7 plots the distribution of failures for combinations of these hint types. We perform rejection sampling to estimate the likelihood of each error type given that the generated code fails. The errors are ordered from left to right based on the level of intervention required by a human operator to make the task succeed. For example, if the model outputs runnable code, but only moves the cable up without any wiggling motion, the operator will likely need to add new waypoints and tune the termination conditions and force values. The most common example of invalid syntax or undefined variable accesses that we observe is in attempts to access the force values directly to construct for loops over waypoints. Explicitly adding rules against for loops helps somewhat, but asking the model to translate from pseudocode is the most helpful in minimizing these types of errors. 

## VI. CONCLUSIONS 

In this work, we study the capability of Large Language Models (LLMs) to generate policies for a variety of high-precision, contact-rich manipulation tasks. By allowing LLMs to place constraints on robot impedances and interaction forces, GenCHiP improves success rates on subtasks derived from the Functional Manipulation Benchmark (FMB) and NIST Task Boards by 3x and 4x, respectively, when compared to code generation approaches that don’t allow for compliance. This is the first work to show that robotic code generation using language models can yield policies that are successful in completing contact-rich manipulation tasks. 

## REFERENCES 

- [1] J. Liang, W. Huang, F. Xia, _et al._ , “Code as policies: Language model programs for embodied control,” in _arXiv preprint arXiv:2209.07753_ , 2022. 

- [2] S. Mirchandani, F. Xia, P. Florence, _et al._ , “Large language models as general pattern machines,” _arXiv preprint_ , Jul. 2023. 

- [3] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents,” _arXiv preprint arXiv:2201.07207_ , 2022. 

- [4] S. Vemprala, R. Bonatti, A. Bucker, and A. Kapoor, “Chatgpt for robotics: Design principles and model abilities,” _arXiv preprint arXiv:2306.17582_ , 2023. 

- [5] Y. Jiang, A. Gupta, Z. Zhang, _et al._ , “Vima: General robot manipulation with multimodal prompts,” _arXiv preprint arXiv:2210.03094_ , 2022. 

- [6] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” in _Conference on Robot Learning_ , 2022. 

- [7] A. Brohan, N. Brown, J. Carbajal, _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [8] A. Brohan, N. Brown, J. Carbajal, _et al._ , “Rt-2: Visionlanguage-action models transfer web knowledge to robotic control,” _arXiv preprint arXiv:2307.15818_ , 2023. 

- [9] M. Shridhar, L. Manuelli, and D. Fox, “Perceiveractor: A multi-task transformer for robotic manipulation,” in _Conference on Robot Learning_ , 2023. 

- [10] S. Belkhale, T. Ding, T. Xiao, _et al._ , _Rt-h: Action hierarchies using language_ , 2024. arXiv: 2403.01823 [cs.RO]. 

- [11] K. Tracy, Z. Manchester, A. Jain, _et al._ , “Efficient online learning of contact force models for connector insertion,” _arXiv preprint arXiv:2312.09190_ , 2023. 

- [12] J. Luo, C. Xu, L. Tan, L. Lin, J. Wu, and S. Levine, _Fmb: A functional manipulation benchmark for generalizable robotic learning_ , 2023. 

- [13] Y. Sun, J. Falco, M. A. Roa, and B. C¸ alli, “Research challenges and progress in robotic grasping and manipulation competitions,” _IEEE Robotics and Automation Letters_ , vol. 7, pp. 874–881, 2021. 

- [14] K. Kimble, K. V. Wyk, J. Falco, _et al._ , “Benchmarking protocols for evaluating small parts robotic assembly systems,” _IEEE Robotics and Automation Letters_ , vol. 5, pp. 883–889, 2020. 

- [15] W. Huang, F. Xia, T. Xiao, _et al._ , “Inner monologue: Embodied reasoning through planning with language models,” in _arXiv preprint arXiv:2207.05608_ , 2022. 

- [16] K. Lin, C. Agia, T. Migimatsu, M. Pavone, and J. Bohg, “Text2motion: From natural language instructions to feasible plans,” _Autonomous Robots_ , 2023. 

- [17] I. Singh, V. Blukis, A. Mousavian, _et al._ , “Progprompt: Generating situated robot task plans using large language models,” in _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [18] J. Wu, R. Antonova, A. Kan, _et al._ , “Tidybot: Personalized robot assistance with large language models,” _Autonomous Robots_ , 2023. 

- [19] A. Xie, Y. Lee, P. Abbeel, and S. James, “Languageconditioned path planning,” in _Conference on Robot Learning_ , PMLR, 2023, pp. 3384–3396. 

- [20] Y. Gai, P. Jain, W. Zhang, J. Gonzalez, D. X. Song, and I. Stoica, “Grounded graph decoding improves compositional generalization in question answering,” _ArXiv_ , vol. abs/2111.03642, 2021. 

- [21] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” _arXiv preprint arXiv:2307.05973_ , 2023. 

- [22] Y. Wi, M. V. der Merwe, P. Florence, A. Zeng, and N. Fazeli, “CALAMARI: Contact-aware and language conditioned spatial action MApping for contact-RIch 

manipulation,” in _7th Annual Conference on Robot_ trol for robotic peg-in-hole assembly: A deep- _Learning_ , 2023. reinforcement-learning approach,” _Applied Sciences_ , J. Luo, E. Solowjow, C. Wen, _et al._ , “Reinforcement vol. 10, no. 19, p. 6923, 2020. 

- [23] J. Luo, E. Solowjow, C. Wen, _et al._ , “Reinforcement learning on variable impedance controller for highprecision robotic assembly,” in _2019 International Conference on Robotics and Automation (ICRA)_ , 2019. DOI: 10.1109/ICRA.2019.8793506. 

   - [37] F. J. Abu-Dakka and M. Saveriano, “Variable impedance control and learning—a review,” _Frontiers in Robotics and AI_ , vol. 7, p. 590 681, 2020. 

   - [38] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large language models are zero-shot reasoners,” _ArXiv_ , vol. abs/2205.11916, 2022. 

- [24] T. Z. Zhao, J. Luo, O. Sushkov, _et al._ , “Offline meta-reinforcement learning for industrial insertion,” in _2022 International Conference on Robotics and Automation (ICRA)_ , 2022. 

   - [39] R. Mart´ın-Mart´ın, M. A. Lee, R. Gardner, S. Savarese, J. Bohg, and A. Garg, “Variable impedance control in end-effector space: An action space for reinforcement learning in contact-rich tasks,” _International Conference on Intelligent Robots and Systems (IROS)_ , 2019. 

   - [40] J. Buchli, F. Stulp, E. Theodorou, and S. Schaal, “Learning variable impedance control,” _The International Journal of Robotics Research_ , 2011. 

- [25] Y. Narang, K. Storey, I. Akinola, _et al._ , “Factory: Fast contact for robotic assembly,” _arXiv preprint arXiv:2205.03532_ , 2022. 

- [26] Z. Liu, Q. Liu, W. Xu, L. Wang, and Z. Zhou, “Robot learning towards smart robotic manufacturing: A review,” _Robotics and Computer-Integrated Manufacturing_ , vol. 77, p. 102 360, 2022. 

   - [41] S. Ren, K. He, R. Girshick, and J. Sun, “Faster R- CNN: Towards real-time object detection with region proposal networks,” in _Advances in Neural Information Processing Systems (NIPS)_ , 2015. 

- [27] O. Kroemer, S. Niekum, and G. Konidaris, “A review of robot learning for manipulation: Challenges, representations, and algorithms,” _J. Mach. Learn. Res._ , vol. 22, no. 1, Jan. 2021, ISSN: 1532-4435. 

   - [42] W. Yu, N. Gileadi, C. Fu, _et al._ , “Language to rewards for robotic skill synthesis,” _Arxiv preprint arXiv:2306.08647_ , 2023. 

- [28] M. Suomalainen, Y. Karayiannidis, and V. Kyrki, “A survey of robot manipulation in contact,” _Robotics and Autonomous Systems_ , vol. 156, p. 104 224, 2022. 

   - [43] OpenAI, “Gpt-4 technical report,” 2023. 

- [29] ´I. Elguea-Aguinaco, A. Serrano-Mu˜noz, D. Chrysostomou, I. Inziarte-Hidalgo, S. Bøgh, and N. AranaArexolaleiba, “A review on reinforcement learning for contact-rich robotic manipulation tasks,” _Robotics and Computer-Integrated Manufacturing_ , 2023. 

   - [44] J. Wei, X. Wang, D. Schuurmans, _et al._ , “Chain of thought prompting elicits reasoning in large language models,” _ArXiv_ , vol. abs/2201.11903, 2022. 

   - [45] T.-Y. Lin, P. Doll´ar, R. B. Girshick, K. He, B. Hariharan, and S. J. Belongie, “Feature pyramid networks for object detection,” _2017 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2016. 

- [30] A. S. Morgan, B. Wen, J. Liang, A. Boularias, A. M. Dollar, and K. Bekris, “Vision-driven compliant manipulation for reliable, high-precision assembly tasks,” _arXiv preprint arXiv:2106.14070_ , 2021. 

   - [46] S. Garg, D. Tsipras, P. Liang, and G. Valiant, “What can transformers learn in-context? a case study of simple function classes,” in _arXiv preprint_ , 2022. 

- [31] T. Davchev, K. S. Luck, M. Burke, F. Meier, S. Schaal, and S. Ramamoorthy, “Residual learning from demonstration: Adapting dmps for contact-rich manipulation,” _IEEE Robotics and Automation Letters_ , 2022. 

   - [47] A. Vaswani, N. Shazeer, N. Parmar, _et al._ , “Attention is all you need,” in _Advances in Neural Information Processing Systems_ , I. Guyon, U. V. Luxburg, S. Bengio, _et al._ , Eds., vol. 30, Curran Associates, Inc., 2017. [Online]. Available: https : / / proceedings . neurips . cc / paper _ files / paper / 2017 / file / 3f5ee243547dee91fbd053c1c4a845aa - Paper.pdf. 

- [32] T. Migimatsu, W. Lian, J. Bohg, and S. Schaal, “Symbolic state estimation with predicates for contact-rich manipulation tasks,” in _2022 International Conference on Robotics and Automation (ICRA)_ , 2022. 

- [33] C. Chi, S. Feng, Y. Du, _et al._ , “Diffusion policy: Visuomotor policy learning via action diffusion,” in _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

   - [48] R. Gal, Y. Alaluf, Y. Atzmon, _et al._ , “An image is worth one word: Personalizing text-to-image generation using textual inversion,” in _The Eleventh International Conference on Learning Representations_ , 2023. [Online]. Available: https : / / openreview . net/forum?id=NAQvF08TcyG. 

- [34] G. Schoettler, A. Nair, J. Luo, _et al._ , “Deep reinforcement learning for industrial insertion tasks with visual inputs and natural rewards,” _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 5548–5555, 2019. 

   - [49] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” in _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. [Online]. Available: https : / / openreview . net / forum ? id = w0H2xGHlkw. 

- [35] S. Brahmbhatt, A. Deka, A. Spielberg, and M. M¨uller, “Zero-shot transfer of haptics-based object insertion policies,” in _International Conference on Robotics and Automation (ICRA)_ , Jun. 2023. 

- [36] C. C. Beltran-Hernandez, D. Petit, I. G. RamirezAlpizar, and K. Harada, “Variable compliance con- 

## APPENDIX 

We discuss implementation details in Sec. VII. We explore the fitness of language models for high-precision prediction in Sec. VIII. Robustness evaluations are in Sec. IX. Rollout visualizations are in Sec. X and example prompts are in Sec. XI. 

## VII. IMPLEMENTATION DETAILS 

## _A. Pose estimators_ 

We use a Faster-RCNN [41] model that does joint object detection and keypoint prediction with a ResNet-50 Feature Pyramid Network (FPN) [45] backbone. We train with a bounding box and keypoint regression loss mixture. 

## _B. Prompt Ablation Details_ 

To generate Fig. 7, we take the first 15 prompts that generate an error (skipping any successful prompts) and classify them based on failure type with a human operator. Table II uses the best of five samples from the complete prompt. 

## _C. Compliant action space parameterizations_ 

It is worth noting that different robotic platforms offer different interfaces for control. Torque controlled robots, such as Franka-Emika Panda and Kuka LBR iiwa robots, readily lend themselves to the impedance control law described in Equation 1. On the other hand, position controlled robots, such as the UR5e, require a target position. This will affect how the compliant action space is parameterized. 

To achieve soft interaction with the environment, we can implement an admittance controller that makes use of a force-torque sensor attached to our robot end-effector: 


where _fd_ is a desired force value, and _fs_ is the current sensed force value. The use of admittance control enables us to parameterize our action space as _ti_ = ([ **x** _target_ ] _i, σi_ ), where [ **x** _target_ ] _i_ denote target pose and _σi_ denote the stiffness vector. 

Even though the admittance controller differs from the impedance controller described in Equation 1, the parameters, namely _Kp_ , _Kd_ , and _M_ , play a conceptually similar role to their corresponding variables in the impedance control law, which implies that our method can generalize across different robotic platforms. 

## VIII. PROBING LANGUAGE MODEL FITNESS FOR PRECISION TASKS 

## _A. Reasoning Over Continuous Spaces_ 

The goal of the main paper is to demonstrate that language models trained on vast, offline, internet datasets can still be useful in generalizing robotic policies. In Sec. V-A.5, we show that this is because LLMs encode world knowledge about contact forces and information about object geometry that can be translated into motion patterns, such as the pattern search examples in Tab. I. One reason this question is so pertinent is because of recent interest in amortizing the cost 

of robot policy learning by adapting language models to predict action tokens [8]. Code prediction is one way of using language models out of the box to yield generalizable robotic policies. However, for language models to be aqequate at action prediction for high-precision tasks, they also need to be able to extrapolate floating point sequences with high precision because contact-rich settings require millimeterlevel precision. 

While prior work demonstrates that LLMs are capable of serving as general pattern machines [2], they have not been shown to be able to reason over floating point numbers specifically. In this section, we thus examine two arithmetic tasks that we believe to be precursors to reasoning successfully in continuous action spaces: (1) a linear regression task, and (2) a continuous sequence extrapolation task. In both cases, and in contrast to prior work [2], we let the LLM operate on floating point numbers directly. 

_1) Background:_ **Arithmetic reasoning and pattern extrapolation abilities of LLMs** Mirchandani, Xia, Florence, _et al._ [2] demonstrated that models trained on internet-scale data are capable of doing general spatial and sequential reasoning tasks. Similar to our work, their analysis is inspired by robot control-relevant reasoning problems. However, unlike them, we produce a proof of concept on real hardware and on a challenging contact rich manipulation task. Our arithmetic reasoning tasks are inspired by work from Garg, Tsipras, Liang, _et al._ [46], which shows that the Transformers [47] can learn simple function classes in-context after training on regression problems. Unlike them, we show that this capability emerges in models trained only on text generation. 

_2) Results:_ **Zero-Shot Regression In-Context:** In Fig. 8a, we show the result of prompting a model with _x, y_ = _f_ ( _x_ ) from a 2-dimensional linear function _f_ . We quantify the ability of the model to implicitly learn the linear function by measuring the _y_ ˆ output by the model for a given _x_ , and plotting the resulting error for different floating point number resolutions. The x-axis denotes the number of x, y pairs provided to the LLM and the y-axis is the average prediction error of _y_ ˆ for a given value _x_ . We compare two different formatting strategies. In the first, the _x, y_ pairs are written out as f(x)=y. The second formatting strategy adds spaces between each digit so that each digit is treated as a separate token. For example, f(1.393)=4.107 is formatted as f(1.3 9 3)=4.1 0 7. As can be seen in Fig. 8a, spaceformating with GPT-4 is able to successfully regress to the targets within an error of 0 _._ 01 when using at least 3 decimal places. 

**Sequence Extrapolation:** In Fig. 8b, we illustrate the ability of an LLM to extrapolate sequences of two-dimensional series of numbers (concretely, sinusoids of different frequencies), as this might transfer to path-following behaviors required in the robotic context. To generate these plots, 


Fig. 8: (a) Reconstruction error across different floating point number resolutions and formatting styles. (b) Reconstructions of exemplary sinusoidal sequences for different floating point number resolutions. 

we feed samples of the sinusoidal function up to a certain value and then auto-regressively sample from the LLM. The sampled points are shown in orange. For visualization purposes, the true function is shown in blue. Qualitatively, we see in the figure that the LLM is indeed capable of extrapolating the chosen sinusoids. Unlike Mirchandani, Xia, Florence, _et al._ [2], we find that this ability also works for floating point numbers. To realize these results, we modify the tokenization strategy by placing a space in between each digit. The extrapolation ability begins to break down as the precision and frequency of the sinusoid increase, which can be seen on the right-most side of Fig. 8b. 

The takeaway from this set of experiments is that LLMs trained entirely on offline language data can indeed achieve reasonable performance on arithmetic tasks on continuous spaces. This result shows that large language models are capable of performing least squares up to a small degree of error with in-context learning. 

## _B. Reasoning over spatial patterns_ 

To protoype alternative ways of providing the language model with perceptual information for contact rich tasks, we provide schematics of an assembly board in natural language. In Sec. V-A.1, we allow the language model to reason over object poses via calls to estimate ~~a~~ nd ~~u~~ pdate ~~p~~ ose. Alternatively, we could pass tokenized versions of the scene into the language model [48], [49]. We explore this by prompting with spatial patterns. 


Fig. 9: We prototype an alternative way of passing perceptual information into the language model on the cable unraveling task from IROS RGMC [13]. This is a typical rollout. 

**Spatial patterns** are symbolic summaries of a given scene and act as a character-based representation of what is visible to the agent. An example of a symbolic representation of an IROS RGMCS [13] board is summarized in Figure VIII-B. The c symbol refers to the path of the cable, S refers to a screw, and B refers to a plastic channel component through which the cable is routed. These would also be defined in the prompt. Although these are specified by the prompt designer in our examples, they could also be generated by a visionlanguage model or other perception APIs [22]. 

In addition to adding the spatial pattern to the prompt, we append the following task command: Explain how to unravel the cable from the screws and then generate the code to unravel the cable if the robot is currently holding the cable at position 1.Using GenCHiP, the best code generation is successful in removing the cable from the first screw in 8 out of 10 evaluation runs but only successful in removing the cable from both screws in 2 out of 10 cases. We expect that these numbers could be further improved by allowing for regrasps or by implementing more advanced and iterative scene tokenization strategies, which we believe is a strong area for future work. 

## IX. ROBUSTNESS 

## _A. Cable un-routing_ 

We study the robustness to initial position on the cable unrouting task. The starting position on this task is parameterized by a script that localizes and picks up the cable, which is assumed to be threaded through one of the RGMC plastic 

Spatial Patterns 


Fig. 10: Example rollouts on all tasks. 

||Left-side tunnel|Right-side tunnel|
|---|---|---|
|CaP [1] (Few-Shot)|60%|20%|
|GenCHiP, FC (Few-Shot)|60%|**100%**|
|**GenCHiP** (Few-Shot)|**100%**|80%|


TABLE III: Cable unrouting [13] from different starting positions. 

components. To make the task challenging, the gripper starting position is offset in the positive or negative x direction, which corresponds to the left and right side of the tunnel. In Tab. III we show that GenCHiP is able to successfully un-route the cable regardless of the displacement direction. 

## XI. PROMPT AND OUTPUT CODE EXAMPLE 

In this section, we provide a complete prompt example for the cable un-routing task (Listing 1) and the GPT-4-generated output (Listing 2). Importantly, this example demonstrates how that the language model is capable of generating novel combinations of moves and constraint conditions. In the prompt, there is no constraint on right-ward snags for poses moving to the left in the prompt, but the language model is able to synthesize these constraints for the task. Please see our paper website for the remaining prompts. 

## X. ROLLOUT VISUALIZATION 

We visualize rollouts from our method in Fig. 10. 

## Example 1: Complete <u>prompt</u> example for the cable un-routing task 

|prompt = """<br>|
|---|
|You're a robot holding a cable that's threaded through a tunnel with a small opening at the top.|
|You need to unroute the cable by removing it from the tunnel.|
|You will have access to the following methods, which are imported directly:|
|- cartesian_admittance_move: This moves the robot to a target_pose until a termination condition is reached.|
|Args:|
|max_cartesian_stiffness:|
|The maximum allowed stiffness along each cartesian dof (6d), expressed in|
|the robot base frame.<br>|
|target_impedance:<br>|
|(0,1] 6d-vector specifying the target impedance along each cartesian dof.|
|target_pose:|
|Target pose for the robot flange frame in the base frame.|
|termination_condition:|
|Termination condition.|
|virtual_cartesian_inertia:|
|The diagonal representation of the desired virtual Cartesian inertia|
|matrix, expressed in the robot base frame [kg, kg mˆ2]|
|execution_timeout_seconds:|
|Timeout for execution. Defaults to 30s if not specified<br>|
|Default value: 10.0|
|tare_ft_sensor: False when in contact, True otherwise.|
|- types_pb2.Comparison: this specifies the termination condition above. It can't be accessed directly, it can only be|
|passed as an argument to the cartesian_admittance_move method.|
|Args:|
|operation: types_pb2.Comparison type. One of GREATER_THAN_OR_EQUAL, LESS_THAN_OR_EQUAL, APPROX_EQUAL, or|
|APPROX_NOT_EQUAL.|
|statevariablename:Variablewhereconditionisapplied.Oneofpolicy.status.{xforceyforcezforce|
|__        _, _, _,<br>translation_error, rotation_error}.<br>|
|double_value: [-0.4, 0.4] value of state variable on which operation is applied|
|- types_pb2.Condition: Can't be accessed directly, can only be passed as an argument to the cartesian_admittance_move|
|method.|
|Args:|
|comparison: types_pb2.Comparison type.|
|- types_pb2.ConjunctionCondition: Wrapper to compose multiple conditions together.|
|Args:<br>operation: types_pb2.ConjunctionCondition type. One of ALL_OF or ANY_OF .|
|conditions: A list of Conditions over which the operation is applied<br>|
|- pose3rpy: returns a pose object that specifies a pose. Note: Poses can be composed using the multiply method. E.g.,|
|_<br>pose1.multiply(pose2) applies pose2 on top of pose1.<br>|
|Args:|
|translation: x, y, z translation.|
|rotation: rotation along x, y, and z.|
|- move_gripper: opens and closes the gripper.|
|Args:|
|percent_open: Controls how open gripper is. 0 is fully closed, 100 is fully open.|
|- grasp_cable: grab the free edge of the routed cable|
|You will also have access to the following fields:|
|- pose(number): the robot pose just above number. You can build more poses by using this as a reference with the<br>|
|multiply method.<br>"""|


|"""<br>Args:<br>number: the pose number for the layout below.<br>- grasp(pose): go to grasp pose and grasp the cable.<br>Args:<br>pose: the robot pose above the grasp position<br>Rules:<br>- Don't define any new methods<br>- Don't call any undefined methods<br>- Don't add any if statements or while loops<br>Here are some examples using the cartesian_admittance_move method while holding the cable:<br>`````python<br>position_condition = types_pb2.Comparison(<br>operation=types_pb2.Comparison.LESS_THAN_OR_EQUAL,<br>state_variable_name="policy.status.translation_error",<br>double_value=0.001,<br>)|
|---|
|# move down until contact is reached<br>upward_force_threshold = 0.4<br>contact_condition = types_pb2.Condition(<br>comparison=types_pb2.Comparison(<br>operation=types_pb2.Comparison.GREATER_THAN_OR_EQUAL,<br>state_variable_name="policy.status.z_force",<br>double_value=upward_force_threshold,<br>)<br>)<br>down_pose = pose(1).multiply(pose3_rpy(translation=[0, 0, -.01]))<br>cartesian_admittance_move(<br>target_pose=down_pose,<br>termination_condition=termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[contact_condition, position_condition]<br>))|
|# move up unless snag is detected<br>downward_force_threshold = -0.4<br>snag_condition = types_pb2.Condition(<br>comparison=types_pb2.Comparison(<br>operation=types_pb2.Comparison.LESS_THAN_OR_EQUAL,<br>state_variable_name="policy.status.z_force",<br>double_value=downward_force_threshold,<br>)|
|)<br>up_pose = pose(1).multiply(pose3_rpy(translation=[0, 0, .01]))<br>cartesian_admittance_move(<br>target_pose=up_pose,<br>termination_condition=termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[snag_condition, position_condition]<br>))|
|# move the cable to the right unless snag is detected<br>leftward_force_threshold = 0.4<br>leftwardsnag_condition = types_pb2.Condition(<br>comparison=types_pb2.Comparison(<br>operation=types_pb2.Comparison.GREATER_THAN_OR_EQUAL,<br>state_variable_name="policy.status.x_force",<br>double_value=leftward_force_threshold,<br>)<br>|
|)<br>right_pose = pose(1).multiply(pose3_rpy(translation=[-0.01, 0, 0]))<br>cartesian_admittance_move(<br>target_pose=up_pose,<br>termination_condition=termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[leftwardsnag_condition, position_condition],<br>))<br>`````<br>Currently the robot is holding the cable at pose(1), but the cable is stuck in a tunnel with a small opening at the<br>top. Describe a strategy for unrouting the cable using force information to search for the opening and then write a<br>program using the APIs above to unroute the cable and lift it out of the tunnel."""<br>messages = [{"role": "user", "content":prompt}]<br>response = openai.ChatCompletion.create(<br>model="gpt-4",<br>messages = messages,<br>temperature=0.0,<br>max_tokens=512*3,<br>frequency_penalty=0.0<br>)<br>print(response["choices"][0]["message"]["content"])|


|Strategy:<br>1. First, we will move the cable upwards until we detect a snag. This will help us to find the top of the tunnel.<br>2. Once we detect a snag, we will move the cable to the right until we detect another snag. This will help us to find<br>the right wall of the tunnel.<br>3. After finding the right wall, we will move the cable to the left until we no longer detect a snag. This will help us<br>to find the opening of the tunnel.<br>4. Finally, we will move the cable upwards again to lift it out of the tunnel.<br>Program:<br>`````python<br># Step 1: Move up until snag is detected<br>downward_force_threshold = -0.4<br>snag_condition = types_pb2.Condition(<br>comparison=types_pb2.Comparison(<br>operation=types_pb2.Comparison.LESS_THAN_OR_EQUAL,<br>state_variable_name="policy.status.z_force",<br>double_value=downward_force_threshold,<br>)|
|---|
|)<br>up_pose = pose(1).multiply(pose3_rpy(translation=[0, 0, .01]))<br>cartesian_admittance_move(<br>target_pose=up_pose,<br>termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[snag_condition, position_condition]<br>))|
|# Step 2: Move right until snag is detected<br>leftward_force_threshold = 0.4<br>leftwardsnag_condition = types_pb2.Condition(<br>comparison=types_pb2.Comparison(<br>operation=types_pb2.Comparison.GREATER_THAN_OR_EQUAL,<br>state_variable_name="policy.status.x_force",<br>double_value=leftward_force_threshold,<br>)|
|)<br>right_pose = pose(1).multiply(pose3_rpy(translation=[-0.01, 0, 0]))<br>cartesian_admittance_move(<br>target_pose=right_pose,<br>termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[leftwardsnag_condition, position_condition],<br>))|
|# Step 3: Move left until no snag is detected<br>rightward_force_threshold = -0.4<br>rightwardsnag_condition = types_pb2.Condition(<br>comparison=types_pb2.Comparison(<br>operation=types_pb2.Comparison.LESS_THAN_OR_EQUAL,<br>state_variable_name="policy.status.x_force",<br>double_value=rightward_force_threshold,<br>)|
|)<br>left_pose = pose(1).multiply(pose3_rpy(translation=[0.01, 0, 0]))<br>cartesian_admittance_move(<br>target_pose=left_pose,<br>termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[rightwardsnag_condition, position_condition],<br>))|
|# Step 4: Move up to lift the cable out of the tunnel<br>cartesian_admittance_move(<br>target_pose=up_pose,<br>termination_condition=types_pb2.ConjunctionCondition(<br>operation=types_pb2.ConjunctionCondition.ANY_OF,<br>conditions=[snag_condition, position_condition]<br>))<br>`````|


Example 2: GPT-4-generated output for the cable-unrouting task 

