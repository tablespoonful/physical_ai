---
title: "MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation"
date: "2026-06-04"
authors: "Ilyass Taouil; Michal Ciebelski; Shafeef Omar; Haizhou Zhao; Angela Dai; Aaron M. Johnson"
url: https://arxiv.org/abs/2606.06139
pdf: https://arxiv.org/pdf/2606.06139
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.06139)** / [論文ページ](https://arxiv.org/abs/2606.06139)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation** 

**Ilyass Taouil**<sup>1</sup><sup>_,∗_</sup> **Michal Ciebielski**<sup>1</sup><sup>_,∗_</sup> **Shafeef Omar**<sup>1</sup><sup>_,∗_</sup> **Haizhou Zhao**<sup>1</sup><sup>_,_2</sup> 

**Angela Dai**<sup>1</sup> **Aaron M. Johnson**<sup>3</sup> **Majid Khadiv**<sup>1</sup> 

1Technical University of Munich, Germany 2New York University, USA 3Carnegie Mellon University, USA 

> _∗_ Equal contribution 


Figure 1: **Real-world humanoid motion from MotionDisco.** Snapshots of a real-world experiment executing a trajectory discovered by our evolutionary tree search, deployed zero-shot on the robot. 

**Abstract:** We present _MotionDisco_ , a framework that discovers contact-rich, long-horizon humanoid loco-manipulation motions from scratch, without relying on teleoperation or motion retargeting from human demonstrations. This is challenging because the space of possible contact interactions grows combinatorially with the task horizon and the number of objects in the scene. MotionDisco enables rapid discovery of novel motions by coupling a large language model (LLM) guided evolutionary search over sequences of interactions with an efficient sequential kinodynamic trajectory optimizer and pruning strategy, enabling the rapid discovery of novel skills. Through extensive ablation studies, we show that our LLM-guided search discovers successful whole-body trajectories across several challenging long-horizon tasks. Finally, by training reinforcement learning tracking policies on the discovered trajectories, we transfer the motions to a real humanoid robot. This is the first work to discover and deploy long-horizon humanoid loco-manipulation skills entirely through automated evolutionary search. Supplementary videos of the experiments are available at: `https://youtu.be/DHiVz34QYlw` . 

**Keywords:** Motion Discovery, Humanoid Loco-Manipulation, Program Search 

## **1 Introduction** 

For humanoid robots to operate effectively in the real world, they must be capable of executing longhorizon loco-manipulation behaviors in novel and unstructured environments. However, exploration in such high-dimensional, contact-rich settings remains extremely challenging [1, 2, 3]. As a result, most state-of-the-art approaches rely either on retargeting human motion to humanoids to make exploration tractable or on teleoperation to bypass the exploration problem altogether. Despite their success, motion-retargeting approaches have inherent limitations, most notably the impracticality of generating demonstrations for every possible scenario a robot may encounter. 

In this work, we move beyond pure imitation and propose a motion discovery framework that enables humanoid robots to reason about their environment and synthesize novel long-horizon behaviors. Specifically, we combine the reasoning capabilities of large language models (LLMs) with evolutionary algorithms to efficiently explore the space of contact interactions via program search, in which an LLM iteratively mutates code that generates candidate contact plans. Our framework is built around a layered kinodynamic trajectory optimization formulation that takes candidate contact sequences as input and progressively solves increasingly complex optimization problems. The resulting optimization feedback is used as numerical and language-based guidance for the program search process. Through extensive ablation studies and experimental evaluations, we demonstrate that the proposed framework can unlock highly complex humanoid loco-manipulation behaviors. 

The main contributions of this work are as follows: 

- A framework that couples LLM-guided evolutionary search over contact plans with a kinodynamic trajectory optimizer that returns numerical and structured language feedback, enabling time-efficient discovery of complex long-horizon loco-manipulation behaviors. 

- Extensive analysis showing that our search-based approach outperforms a non-iterative approach, indicating that search with structured feedback is essential for successful motion discovery. Moreover, the evolutionary nature of the search yields diverse motions for the same task in a single run, providing an efficient source of data generation for humanoid loco-manipulation. 

- Real-world results on a wide range of long-horizon loco-manipulation behaviors. This is the first work to autonomously discover and execute long-horizon loco-manipulation behaviors on real hardware, without any motion retargeting from human data or teleoperation. 

## **2 Related Work** 

### **2.1 Human to humanoid retargeting** 

Retargeting human motion to humanoid robots has recently received significant attention. Humanto-humanoid motion transfer remains challenging due to morphological differences in degrees of freedom, limb lengths, and mass distributions. Existing methods [4, 5] address this problem through keypoint-based inverse kinematics followed by unconstrained optimization to improve physical consistency. More recent approaches [6, 7] formulate constrained trajectory optimization problems to improve the geometric consistency of the generated motions. To track these retargeted trajectories, several works employ reinforcement learning (RL) with reward formulations inspired by DeepMimic [8], producing robust policies around reference motions and demonstrating successful tracking of retargeted human behaviors on humanoid hardware [9]. More recent approaches extend this paradigm to loco-manipulation using proprioceptive observations, data augmentation, and contact-aware rewards [6, 10]. 

While RL-based tracking can generate robust and dynamically feasible behaviors, it typically requires extensive training and high-quality demonstrations. In loco-manipulation settings, performance further depends on accurate contact information [11, 10], which is difficult to recover reliably from kinematic retargeting alone. Consequently, recent methods [12, 13] perform dynamic refinement of retargeted trajectories before RL tracking, leading to significant improvements. Despite recent progress in retargeting-based pipelines, they remain limited in complex or novel scenarios 

2 


Figure 2: **MotionDisco** couples LLM-guided evolutionary discovery of contact plans (left) with contact-explicit trajectory optimization (right). Each search node proposes a mutation of its parent program, conditioned on the goal prompt and the parent’s feasibility feedback; executing the mutated program yields a discrete contact plan (denoted by the blue dots). Plans that pass a kinematic feasibility check are sent to the trajectory optimizer, which assesses dynamic feasibility and returns the feedback that guides subsequent mutations. 

where relevant demonstrations are unavailable. Even when such data exists, tying motions to human demonstrations constrains the robot to human-like behaviors, preventing it from unlocking its full physical capability. 

### **2.2 LLMs for Motion Synthesis** 

The common-sense reasoning capabilities of LLMs have recently sparked significant interest in their application to robotic motion planning. Early work by [14] demonstrated how low-level robotic skills can be combined with LLMs that provide high-level procedural knowledge for executing complex, temporally extended instructions. Subsequently, [15] leveraged the code-generation capabilities of LLMs to translate natural language commands into robot policy code that processes perception outputs and parametrizes control primitives for tabletop manipulation tasks. 

More recent approaches further integrate LLMs with planning and optimization. For example, [16] uses LLM-generated programs together with sampling or optimization methods to identify skill sequences that achieve task goals while satisfying constraints. Similarly, [17] demonstrates the effectiveness of this strategy in a variety of long-horizon manipulation settings. In parallel, [18] employs LLMs within an evolutionary optimization loop over reward code, while [19] shows that hierarchical planning with LLMs enables more complex human behaviors that can subsequently be tracked using RL in simulation. 

The work most closely related to ours is [20], which uses LLMs to perform program search in order to assist trajectory optimization for long-horizon tasks. In contrast to [20], which operates at the level of manipulation predicates, our approach directly generates programs over contact plans, enabling the treatment of both locomotion and manipulation behaviors. Furthermore, we introduce a trajectory optimization framework with progressively increasing structural complexity that provides 

3 

informative feedback to the program search process. In particular, we build on recent advances in program evolution and scientific discovery [21, 22, 23, 24] to generate candidate contact plans, which we evaluate with an efficient kinodynamic trajectory optimization tool to drive a sampleefficient evolutionary search over contact sequences. 

## **3 Method** 

This section presents MotionDisco, a framework for discovering long-horizon humanoid locomanipulation behaviors through the interaction of discrete contact-plan search and continuous motion planning. The framework alternates between proposing candidate contact sequences, which explore the combinatorial space of possible interactions, and evaluating whether each candidate can be realized as a feasible robot–object motion consistent with the scene geometry and dynamics. We first describe the contact-explicit motion-planning formulation used to evaluate candidates and generate feasible trajectories, and then the LLM-guided evolutionary search, which represents contact plans as programs, mutates them through language-model-guided edits, and uses motion-planner feedback to improve subsequent proposals. Figure 2 illustrates the overall framework. 

### **3.1 Motion Planning** 

The motion planning module evaluates the contact plans produced by the LLM-guided search and is used in two ways. First, it acts as an evaluator for contact-mode discovery: a sequential kinematic optimization, similar to [25], rejects contact sequences that fail to satisfy collision avoidance, configuration limits, and transition consistency, returning text feedback that identifies where the proposed interaction sequence fails. This stage ignores dynamics and serves as a fast geometric feasibility filter. Second, when a sequence is feasible, the planner solves for the robot–object state trajectory, controls, contact wrenches, and stage durations while enforcing dynamics, contact constraints, collision avoidance, and state/control limits; the resulting trajectory is used for downstream policy training and execution. 

Let _I_ be the set of contact interfaces. For each _a ∈I_ , define its contact state as a pair ( _a, b_ ) where _b ∈I_ denotes unilateral contact with interface _b_ , or ( _a,_ ∅) if free. The interfaces _a_ represent the contact interfaces that can change their state, such as end effectors and movable objects. A contact mode is the complete assignment over all interfaces: 


with a consistency constraint that if _b̸_ = ∅ then ( _a, b_ ) _∈ c ⇒_ ( _b, a_ ) _∈ c_ . For a contact mode _c_ , let _M_ ( _c_ ) denote the feasible constraint manifold associated with it: 


The set _M_ ( _c_ ) contains all state _x, x_ ˙ , and control _u_ tuples that satisfy the dynamics and contact conditions induced by _c_ , remain within hardware limits, and avoid unintended collisions. The latter requirement is particularly important, since any additional collision would create an unmodeled contact and thus imply a departure from the contact mode _c_ . 

Given a fixed contact-mode sequence _C_ = ( _c_ 0 _, . . . , cK−_ 1), the continuous optimization problem finds the state trajectory _x_ ( _·_ ), control trajectory _u_ ( _·_ ), and stage durations _T_<sup>¯</sup> 0: _K−_ 1, where each _T_<sup>¯</sup> _k_ is the duration of mode _ck_ . These durations induce switching times _t_ 0 = 0, _tk_ +1 = _tk_ + _T_<sup>¯</sup> _k_ , and final time _T_ = _tK_ , with _c_ ( _t_ ) = _ck_ for _t ∈_ [ _tk, tk_ +1). The continuous trajectory optimization problem 

4 

induced by a fixed contact-mode sequence is defined as follows: 


Where, _ϕ_ is the running cost, _ϕT_ is the terminal cost, _wT_ weights the final-time penalty, and _X_ goal is the desired goal set. 

Both the sequential kinematic optimization and the trajectory optimization are implemented using a direct multiple shooting transcription and solved with temporal structure exploiting solvers, [26] and [27], respectively. 

### **3.2 Motion Discovery via LLM-guided Evolutionary Search** 

Given a scene representation _S_ and a goal _G_ , our objective is to discover a contact-mode sequence _C_ = ( _c_ 0 _, . . . , cK−_ 1) that reaches the goal and respects all constraints. The scene representation _S_ is a text-based description of the world containing the label, position, and dimensions of every object in the scene. The goal _G_ may contain both discrete and continuous components: the discrete component specifies desired contacts between robot or object interfaces, while the continuous component specifies target states such as robot or object poses. 

The remainder of this section describes the full search loop. We first define the tree search representation, in which each node stores an executable contact-plan program together with its score and feedback. We then describe the parent-selection policy used to choose nodes for expansion, the LLM-based mutation operators used to generate new contact-mode sequences, and the automatic scoring and feedback procedure that evaluates each candidate through kinematic feasibility and trajectory optimization. All LLM-based components in this work use _Claude Opus 4.7_ [28]. 

### **3.2.1 LLM-guided Tree Search** 

We search over contact-mode sequences using an LLM-guided evolutionary tree _T_ = ( _N, E_ ). Each node _n ∈ N_ is a self-contained candidate contact plan represented by a program _pn_ whose execution returns a sequence _Cn_ . The node also stores a scalar score _Fn_ , optional text feedback _τn_ , and an offspring count _on_ recording how many children have already been generated from that node. Each edge _e ∈ E_ corresponds to a mutation from a parent program to a child program. Starting from a root node encoding the initial contact state, the search iteratively selects a parent node, mutates its contact-plan program with an LLM, evaluates the resulting sequence, and adds the evaluated candidate back to the tree. The search terminates when the allocated search budget is exhausted. 

### **3.2.2 Tree Expansion** 

LLM-guided program evolution methods [21, 22, 23, 24] rely on several mechanisms for effectively expanding the tree search. First, _expansion sampling_ determines which existing nodes are selected for further expansion. Second, _diversity maintenance_ prevents premature convergence by encouraging the search to preserve multiple promising directions. Third, _inspiration sampling_ selects additional nodes from the tree to include in the prompt, allowing new candidates to build on diverse prior solutions. In this work, we adopt the tree expansion strategy of ShinkaEvolve [22], which additionally uses novelty-based rejection sampling to filter candidates too similar to existing ones. 

In ShinkaEvolve, these mechanisms are realized through a hierarchical population model. Expansion sampling is island-conditioned: candidate parents are sampled from structured subpopulations, which distributes search effort across different regions of the tree. The same island structure provides diversity maintenance by preserving multiple subpopulations and preventing the search from 

5 

collapsing around a small set of high-scoring nodes. For prompt construction, ShinkaEvolve samples additional tree nodes as inspirations, allowing the LLM to condition candidate generation on diverse prior solutions. The details of each of these steps can be found in Appendix A.2. 

### **3.2.3 Contact Plan Mutation** 

After selecting a parent node, MotionDisco constructs an LLM mutation prompt from the scene _S_ , goal _G_ , parent program _pn_ , parent score _Fn_ , and parent feedback _τn_ . The prompt also specifies the valid interfaces _I_ , so that mutations are restricted to meaningful contact assignments in the current scene. Details about the prompt can be found in Appendix A.1 

The LLM returns a modified program _p_<sup>_′_</sup> , whose execution produces a new contact-mode sequence: 


Thus, the LLM mutates only the discrete contact plan: each stage must assign exactly one target _b ∈I ∪{_ ∅ _}_ to every active interface _a_ , while the continuous motion between contact switches is recovered later by kinematic feasibility and trajectory optimization. 

The prompt conditions each mutation on the current tree state through the selected parent and, optionally, other nodes sampled from the tree. After parsing, the proposed program’s contact plan is checked for syntactic validity and consistency with the contact-mode definition in Sec. 3.1. Valid proposals are evaluated by the motion planner and inserted into the tree as children of the selected parent. 

### **3.2.4 Contact Plan Scoring and Feedback** 

Given a candidate sequence, we first run the sequential kinematic feasibility check; if the full sequence is kinematically feasible, we then solve the trajectory optimization problem. In this case, the cost assigned to the plan is computed from the resulting trajectory as the sum of the constraint residuals and a jerk regularization term: 


where _r_ ( _xi, ui, cs_ ( _i_ )) collects the equality and inequality constraint residuals at knot point _i_ , and _wj_ weights the jerk penalty. The text feedback reports if the full contact sequence is kinematically feasible together with the resulting residual and jerk costs. 

If the full kinematic sequence is infeasible, trajectory optimization is not run and a score of zero is given to the respective node. Instead, we identify the failure point by iteratively shortening the sequence until the longest feasible prefix is found: 

_K_ ˆ = max � _k ∈{_ 0 _, . . . , K_<sup>_′_</sup> _}_ : ( _c_<sup>_′_</sup> 0<sup>_, . . . , c_</sup> _k_<sup>_′_</sup> _−_ 1<sup>) is kinematically feasible</sup> � _._ (6) ˆ ˆ ˆ The first failing mode or transition, namely _cK_<sup>_′_or</sup><sup>_c′_</sup> _K−_ 1<sup>_→c′_</sup> _K_<sup>, is returned as text feedback to the</sup> LLM. This feedback describes which contact assignment caused the kinematic optimization to fail, allowing future mutations to repair the contact plan locally rather than discard the entire sequence. 

## **4 Evaluation** 

We evaluate MotionDisco on eight tasks spanning a range of difficulty levels, from simple pickand-place to complex whole-body behaviors that require integrating locomotion, manipulation, and reasoning about the environment as a source of support. Detailed task descriptions and scene illustrations are provided in Appendix B.1. We organize our evaluation in three parts. First, we quantitatively analyze motion discovery across different expansion and feedback strategies, reporting the best trajectory optimization cost achieved, the percentage of valid contact plans found, and the time required to find the first valid solution for the best strategy. Second, we qualitatively analyze the diversity of motions discovered by the search on a representative scene, showing that it finds a variety of contact plans that all satisfy the goal in a single search. Finally, we carry out extensive real-world experiments showing that the discovered motions transfer successfully to the real humanoid robot. 

6 

Table 1: Comparison across different expansion and feedback strategies. We additionally report the time required to find the first valid solution for the best strategy <u>(MotionDisco, MD).</u> 

|||**SC**|**MD**|**w/o TF**||**MD**||
|---|---|---|---|---|---|---|---|
|**# **|**Task**|**Cost**_↓_|**Cost**_↓_|**Valid %**_↑_|<br>**Cost**_↓_|**Valid %**_↑_|**Time**[min]_↓_|
|1|Banana|/|21.17|48.14|**20.08**|**70.30**|7.49|
|2|Box Stacking|398.05|398.05|45.45|**10.53**|**63.63**|4.58|
|3|Climb Table w/ Box|16.16|16.47|46.15|**15.97**|**53.84**|2.15|
|4|Long-Dist. Pick & Place|13.61|10.70|65.00|**10.42**|**70.00**|2.50|
|5|Move Through Clutter|/|11.96|**73.33**|**11.67**|**73.33**|3.11|
|6|Parkour Pick & Place 1|/|15.97|33.33|**15.47**|**38.88**|6.05|
|7|Parkour Pick & Place 2|/|15.90|58.82|**15.51**|**67.64**|4.40|
|8|Under-Table Pick & Place|115.64|18.87|64.28|**17.84**|**71.42**|1.34|


### **4.1 LLM-guided Search Enables Motion Discovery** 

Table 1 reports the cost of the recovered motions under three regimes, namely a single LLM call (SC), MotionDisco without text feedback (MD w/o TF), and our evolutionary search framework MotionDisco with text feedback (MD). The text feedback consists of a textual description informing the LLM at which node the contact plan becomes kinematically infeasible, (6). Unlike SC, both MD w/o TF and MD successfully solve all scenarios, highlighting that a single LLM query is insufficient and that iterative search is essential to refine the initial proposals and discover feasible, lower-cost contact plans. Moreover, given the same search budget, MD finds a higher percentage of valid contact plans at a lower TO cost, demonstrating the benefit of text feedback in guiding the search. Importantly, MD finds a first valid solution within a few minutes across all scenarios, making the approach practical despite the combinatorial size of the contact-plan space. Here, we consider a contact plan valid if it first passes the sequential kinematic feasibility check and the TO converges. 

### **4.2 LLM-guided Search Produces Diverse Motions** 

Beyond cost reduction, the evolutionary search naturally produces multiple distinct solutions for the same task. Because the population preserves diversity across generations and duplicate plans are penalized, the search returns qualitatively different contact plans that all satisfy the goal—for example, alternative assignments of end-effectors to environment features. These variations emerge without re-prompting or restarting the pipeline, providing a source of motion diversity that a single LLM call—which tends to collapse onto a single mode—cannot offer. Figure 3 illustrates the motion diversity for the _Parkour Pick & Place 2_ task. 

### **4.3 Real-World Deployment** 

To validate MotionDisco on hardware, we train motion tracking policies for the discovered trajectories using RL with DeepMimic-style rewards [8] and domain randomization, and execute them zero-shot on a real humanoid robot. The resulting controllers robustly reproduce the discovered motions, achieving multiple consecutive successful executions across all attempted tasks. Figure 1 shows snapshots of one such execution, with additional snapshots in Appendix B.2. We refer the reader to the supplementary video for further results. 

## **5 Conclusion** 

This paper presents MotionDisco, a framework for discovering long-horizon whole-body humanoid motions. MotionDisco couples an LLM-guided evolutionary search over discrete contact plans with a layered kinodynamic motion-planning module, in which a sequential kinematic feasibility stage rapidly prunes geometrically inconsistent plans and a full trajectory optimization stage produces dynamically feasible robot–object motions for the surviving candidates. The structured failure feed- 

7 


Figure 3: **Motion diversity discovered by the search on Parkour Pick & Place 2.** _Top: xyz_ hand and foot trajectories across all valid contact plans found by MD. _Bottom:_ whole-body trajectory snapshots of two distinct solutions. The variation in both panels arises from the diversity of the underlying contact plans found in a single run. 

back returned by the motion planner is translated into language and used to guide subsequent LLM mutations, closing the loop between high-level reasoning and low-level optimization. Across eight long-horizon loco-manipulation tasks, our search consistently outperforms a single-call state-of-theart LLM in both success and trajectory cost, and naturally produces qualitatively different solutions to the same task. Finally, through real-world experiments, we demonstrate the first humanoid locomanipulation behaviors of this complexity generated without motion retargeting or teleoperation. 

## **6 Limitations & Future Work** 

While MotionDisco enables the discovery of complex loco-manipulation behaviors, several limitations remain. First, the sequential kinematic and trajectory optimization used in MotionDisco currently supports only unilateral sticking contacts on rectangular patches, and the manipulated objects are restricted to rigid box-like geometries. Extending the contact model to sliding and non-unilateral contacts, and the object set to articulated and free-form shapes, would significantly broaden the range of behaviors and environments the framework can address. Second, MotionDisco assumes a known scene and does not currently incorporate perception; coupling the search with a vision module that builds the scene representation directly from sensor observations would be an important step toward deployment in unstructured environments. Finally, another important next step to improve MotionDisco is to integrate the recent advances in simulation-ready scene construction for on-the-fly motion discovery [29, 30, 31]. 

8 

## **References** 

- [1] S. Tonneau, A. Del Prete, J. Pettr´e, C. Park, D. Manocha, and N. Mansard. An efficient acyclic contact planner for multiped robots. _IEEE Transactions on Robotics_ , 34(3):586–601, 2018. 

- [2] M. A. Toussaint, K. R. Allen, K. A. Smith, and J. B. Tenenbaum. Differentiable physics and stable modes for tool-use and manipulation planning. In _Robotics: Science and Systems Foundation_ , 2018. 

- [3] M. Ciebielski, V. Dh´edin, and M. Khadiv. Task and motion planning for humanoid locomanipulation. In _IEEE-RAS International Conference on Humanoid Robots (Humanoids)_ , pages 1179–1186, 2025. 

- [4] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, Z. Yi, G. Qu, K. Kitani, J. Hodgins, L. J. Fan, Y. Zhu, C. Liu, and G. Shi. ASAP: Aligning simulation and real-world physics for learning agile humanoid whole-body skills. In _Robotics: Science and Systems_ , 2025. 

- [5] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. Kitani, C. Liu, and G. Shi. OmniH2O: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. In _Conference on Robot Learning_ , 2024. 

- [6] L. Yang, X. Huang, Z. Wu, A. Kanazawa, P. Abbeel, C. Sferrazza, C. K. Liu, R. Duan, and G. Shi. OmniRetarget: Interaction-preserving data generation for humanoid whole-body locomanipulation and scene interaction. _arXiv preprint arXiv:2509.26633_ , 2025. 

- [7] I. Taouil, H. Zhao, A. Dai, and M. Khadiv. Physically consistent humanoid loco-manipulation using latent diffusion models. In _IEEE-RAS International Conference on Humanoid Robots (Humanoids)_ , pages 1179–1186, 2025. 

- [8] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne. DeepMimic: Example-guided deep reinforcement learning of physics-based character skills. _ACM Transactions On Graphics (TOG)_ , 37(4):1–14, 2018. 

- [9] T. E. Truong, Q. Liao, X. Huang, G. Tevet, C. K. Liu, and K. Sreenath. BeyondMimic: From motion tracking to versatile humanoid control via guided diffusion. _arXiv preprint arXiv:2508.08241_ , 2025. 

- [10] H. Weng, Y. Li, N. Sobanbabu, Z. Wang, Z. Luo, T. He, D. Ramanan, and G. Shi. HDMI: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [11] S. Zhao, Y. Ze, Y. Wang, C. K. Liu, P. Abbeel, G. Shi, and R. Duan. ResMimic: From general motion tracking to humanoid whole-body loco-manipulation via residual learning. _arXiv preprint arXiv:2510.05070_ , 2025. 

- [12] C. Pan, C. Wang, H. Qi, Z. Liu, H. Bharadhwaj, A. Sharma, T. Wu, G. Shi, J. Malik, and F. Hogan. SPIDER: Scalable physics-informed dexterous retargeting. _arXiv preprint arXiv:2511.09484_ , 2025. 

- [13] V. Dhedin, I. Taouil, S. Omar, D. Yu, K. Tao, A. Dai, and M. Khadiv. DynaRetarget: Dynamically-feasible retargeting using sampling-based trajectory optimization. _arXiv preprint arXiv:2602.06827_ , 2026. 

- [14] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman, et al. Do as I can, not as I say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 

9 

- [15] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng. Code as policies: Language model programs for embodied control. In _IEEE International conference on robotics and automation (ICRA)_ , pages 9493–9500, 2023. 

- [16] A. Curtis, N. Kumar, J. Cao, T. Lozano-P´erez, and L. P. Kaelbling. Trust the PRoC3S: Solving long-horizon robotics problems with LLMs and constraint satisfaction. In _Conference on Robot Learning_ , 2024. 

- [17] H. Chi, Z. Feng, Y. Lyu, C. Zheng, L. Luo, Y. S. Ong, I. Tsang, H. Chen, Y. Chang, and H. Yin. InstructFlow: Adaptive symbolic constraint-guided code generation for long-horizon planning. _Advances in Neural Information Processing Systems_ , 38:2602–2632, 2026. 

- [18] Y. J. Ma, W. Liang, G. Wang, D.-A. Huang, O. Bastani, D. Jayaraman, Y. Zhu, J. Fan, et al. Eureka: Human-level reward design via coding large language models. In _International conference on learning Representations_ , volume 2024, pages 26516–26560, 2024. 

- [19] Z. Wu, J. Li, P. Xu, and C. K. Liu. Human-object interaction from human-level instructions. In _IEEE/CVF International Conference on Computer Vision_ , pages 11176–11186, 2025. 

- [20] D. Shcherba, E. Cobo-Briesewitz, C. V. Braun, and M. Toussaint. Meta-optimization and program search using language models for task and motion planning. In _Conference on Robot Learning_ , 2025. 

- [21] A. Novikov, N. V˜u, M. Eisenberger, E. Dupont, P.-S. Huang, A. Z. Wagner, S. Shirobokov, B. Kozlovskii, F. J. Ruiz, A. Mehrabian, et al. AlphaEvolve: A coding agent for scientific and algorithmic discovery. _arXiv preprint arXiv:2506.13131_ , 2025. 

- [22] R. T. Lange, Y. Imajuku, and E. Cetin. ShinkaEvolve: Towards open-ended and sampleefficient program evolution. In _International Conference on Learning Representations_ , 2026. 

- [23] M. Cemri, S. Agrawal, A. Gupta, S. Liu, A. Cheng, Q. Mang, A. Naren, L. E. Erdogan, K. Sen, M. Zaharia, et al. AdaEvolve: Adaptive LLM driven zeroth-order optimization. _arXiv preprint arXiv:2602.20133_ , 2026. 

- [24] S. Liu, S. Agarwal, M. Maheswaran, M. Cemri, Z. Li, Q. Mang, A. Naren, E. Boneh, A. Cheng, M. Z. Pan, et al. EvoX: Meta-evolution for automated discovery. _arXiv preprint arXiv:2602.23413_ , 2026. 

- [25] M. Ciebielski, H. Zhao, A. M. Johnson, and M. Khadiv. Discovery of dynamic locomanipulation behaviors. In _ICRA Workshop on Contact-Rich Control and Representation_ , 2026. 

- [26] R. Verschueren, G. Frison, D. Kouzoupis, J. Frey, N. van Duijkeren, A. Zanelli, B. Novoselnik, T. Albin, R. Quirynen, and M. Diehl. acados – a modular open-source framework for fast embedded optimal control. _Mathematical Programming Computation_ , 2021. 

- [27] H. Zhao, L. Righetti, and M. Khadiv. Hippo: High-performance interior-point and projectionbased solver for generic constrained trajectory optimization. _IEEE Robotics and Automation Letters_ , 11(6):6752–6759, 2026. 

- [28] Anthropic. Claude opus 4.7, 2026. URL `https://www.anthropic.com/news/ claude-opus-4-7` . Large language model. 

- [29] C. Xia, K. Zhu, Z. Wang, F. Liu, Z. Zhang, and Y. Duan. SimRecon: SimReady compositional scene reconstruction from real videos. In _Computer Vision and Pattern Recognition_ , 2026. 

- [30] H. Xia, C.-H. Lin, H.-Y. Hsu, Q. Leboutet, K. Gao, M. Paulitsch, B. Ummenhofer, and S. Wang. HoloScene: Simulation-ready interactive 3D worlds from a single video. _Advances in Neural Information Processing Systems_ , 38:32501–32524, 2026. 

10 

- [31] M. Dong, C. Xia, M. Jia, W. Lyu, L. Xu, Z. Zhu, and Y. Duan. ReplicateAnyScene: Zero-shot video-to-3D composition via textual-visual-spatial alignment. _arXiv preprint arXiv:2604.10789_ , 2026. 

11 

## **A LLM-guided Search Implementation** 

### **A.1 Prompt Details** 

The prompt provides the LLM with task-specific scene information, contact-surface identifiers, planning rules, helper functions, and evaluator feedback, then asks it to generate a contact mode sequence given a goal description. It also includes examples of useful contact-transition patterns, such as twohand grasps, lifts, placements, releases, and step-ups. These patterns are intended as illustrative guidance rather than required templates: the model may use, combine, or depart from them as needed, provided the resulting contact plan satisfies the task constraints and contact validity rules. 

```
============================================================
```

```
Youareacontactplannerforahumanoidrobot.Givenatask
andascenewithlabeledsurfaceIDs,yououtputPythoncodethatbuildsa
contact_mode_seq|adictionarydescribinghowtherobot’send-effectors,soles,
andmanipulatedobjectsmakeandbreakcontactacrossasequenceofmodes.
```

```
YourjobistoreasonabouttheINTERESTINGsubgoalsonly:grasps,releases,
lifts,placements,andstep-upsontoelevatedsurfaces.Ordinarywalking
betweensubgoalsisdelegatedtoastandardlocomotionhelper,walk(),soyou
justdecidehowmanystepstotakeandneverhavetohand-craftplainstepping
modes.
```

```
#Notation
#EEsandsoles:(env_id,contact_type)or()forfree
#Objects:(self_id,env_id,contact_type)or()forfree
#
#env_id:IDofthesurfaceinthescenebeingcontacted
#self_id:IDofthesurfaceontheobjectitself
#contact_type:1=unilateral(onlysupportedvalue)
#
```

```
#Amodeisafullsnapshotofallactivecontacts.Eachmodelasts1second.
```

```
#Onlyemitanewmodewhenatleastonecontactactuallychanges.
```

#### `# Rules` 

- `At least one sole must be in contact at all times.` 

- `Object channels are passive: env contact breaks when lifted, and only reappears when the object is explicitly placed or lands on a new surface. When placed on another object, env_id becomes that object’s surface ID.` 

- `Concurrent make/break events in one transition are intentional and encouraged.` 

- `The robot has flat palms with no finger closure. To hold an object against gravity, BOTH EEs must be in contact with it | a single EE cannot grip an object alone. Both EEs must be in contact before the lift transition (object channel -> ()), and must remain in contact until the object is placed back on a support surface. The two EEs may make contact in different modes (sequential grasp), but both must be on the object before the object becomes free.` 

- `Be efficient: combine concurrent events into a single mode, no noop repeats, no modes that change nothing. Shorter plans solve faster and rarely score worse than padded ones.` 

- `# Helpers available in scope` 

```
get_initial_mode()->Dict[str,List[Tuple]]
Returnsthescene’scompiledstartingmodeasalength-1
contact_mode_seqdict.Useitasmode0ofyourplan,then
groweachchannelbycallingwalk()andappend_mode():
plan={ch:list(seq)forch,seqinget_initial_mode().items()}
Thelist(seq)copyisrequiredsoeachchannelisamutable
listthehelperscanappendto.
```

```
walk(plan,n_steps)->None
Appendsastandardlocomotionpatternofn_stepsstepsto‘plan‘.
```

12 

```
Onestep=onefootliftsandplantsagain(alternatingfeet,right
footfirst).Thefeetstayonthesupportsurfacetheywerealready
on.Allnon-solechannelsareheldattheircurrentvalues
throughoutthewalk,soanyactiveEEgraspandattachedobject
persistthroughit.
```

```
walkproducesaSTRAIGHT-LINEbasetranslationtowardthenext
contact-impliedtarget|itdoesNOTplanaroundobstacles.Ifany
movableorfixedobject’sxyfootprintintersectsthelinesegment
fromthecurrentbasexytothenextrequiredbasexy,thewalk
willcollide.Youmustclearmovableobstacles(grasp,lift,walk
aside,place)BEFOREthewalkthatwouldpassthroughthem.Fixed
obstaclesmustberoutedaroundexplicitly|typicallywithan
intermediatewalktoawaypointthatgivesaclearline.
```

```
AfterwalkreturnstheplanisinDOUBLESUPPORT:bothsolesare
plantedontheiroriginalsupportenv_ids(onlythebasexyhas
moved).Thisholdsforanyn_steps.Astep-up,step-down,orany
otherfoottransitionchainedimmediatelyafterwalktherefore
stillbeginswithafoot-lift(sole->())mode.
```

```
walkdoesNOTstepontoelevatedsurfaces(boxlids,platforms)or
changesupportsurfaces.Useappend_modeforthosetransitions.
```

```
append_mode(plan,**channel_updates)->None
Appendsexactlyonenewmodeto‘plan‘.Anychannelnotmentioned
keepsitspreviousvalue.Usethistoexpressinterestingtransitions.
```

#### `# When to use walk vs append_mode` 

```
Usewalkwhenevertheonlythingchangingbetweentwosubgoalsisthebase’s
xypositiononflatground.Don’tenumeratethesteppingmodesyourself|
justdecidehowmanystepstherobotneedsandletIK/TOplacethem.
```

```
Useappend_modeforeverythingthatactuallymattersforthetask:
```

- `grasping: EE goes from () -> (env_id, 1)` 

- `- releasing: EE goes from (env_id, 1) -> () - lifting: object goes from (self_id, env_id, 1) - placing: object goes from () -> (self_id, env_id, 1) - stepping up / down onto a different support surface` 

```
#Interestingpatterns
```

```
Inthepatternsbelow,env_id_1,env_id_2,...areplaceholdersfordistinct
env_idsdrawnfromtheactivescene’sIDtable(similarlyself_id_1for
self_ids).Withinasinglepatternthesamenamereferstothesameid;
acrosspatternsthenamesareindependent.Substitutetheactualintegers
fromtheIDtablewhenemittingyourplan.
```

```
Thepatternsareillustrative,notexhaustive.Channelsareindependent
andanycombinationoftransitionsconsistentwiththerulesaboveis
valid|forinstance,EEsmaypressagainstenvironmentsurfaces(not
justobjectsurfaces)toprovidesupportduringastep-uporstep-down.
```

```
##Two-EEgrasp+lift,concurrent
append_mode(plan,left_ee=(env_id_1,1),right_ee=(env_id_2,1))
append_mode(plan,box1=())
```

```
##Two-EEgrasp+lift,sequential(stabilize,thensecure)
append_mode(plan,left_ee=(env_id_1,1))
append_mode(plan,right_ee=(env_id_2,1))
append_mode(plan,box1=())
```

```
##Placeandrelease
```

```
append_mode(plan,box1=(self_id_1,env_id_1,1))
```

13 

```
append_mode(plan,left_ee=(),right_ee=())
```

```
##Stepupontoanelevatedsurface
append_mode(plan,right_sole=())
append_mode(plan,right_sole=(env_id_1,1))
append_mode(plan,left_sole=())
append_mode(plan,left_sole=(env_id_1,1))
##Stepupontoanelevatedsurface,assistedbyoneEE
#OneEEpressesagainstthedestinationsurfaceforsupport;theEEis
#establishedbeforethefeetmoveandreleasedoncebothfeetareplanted.
append_mode(plan,left_ee=(env_id_1,1))
append_mode(plan,right_sole=())
append_mode(plan,right_sole=(env_id_1,1))
append_mode(plan,left_sole=())
append_mode(plan,left_sole=(env_id_1,1))
append_mode(plan,left_ee=())
##Stepupwhilecarryinganobject
#Sameasabove|EEandobjectchannelsinherit,sothegrasppersists.
append_mode(plan,right_sole=())
append_mode(plan,right_sole=(env_id_1,1))
append_mode(plan,left_sole=())
append_mode(plan,left_sole=(env_id_1,1))
##Stepdownfromanelevatedsurfacebacktothefloor
#Currentlybothfeetonanelevatedsurface,steppingbacktothefloor.
append_mode(plan,right_sole=())
append_mode(plan,right_sole=(env_id_1,1))
append_mode(plan,left_sole=())
append_mode(plan,left_sole=(env_id_1,1))
##Stepdownfromanelevatedsurface,assistedbyoneEE
#Currentlybothfeetonenv_id_1(elevated).Descendingtoenv_id_2(lower).
#OneEEpressesagainstthesurfacebeingleftforsupportduringdescent.
append_mode(plan,left_ee=(env_id_1,1))
append_mode(plan,right_sole=())
append_mode(plan,right_sole=(env_id_2,1))
append_mode(plan,left_sole=())
append_mode(plan,left_sole=(env_id_2,1))
append_mode(plan,left_ee=())
```

```
#Geometricreasoning
```

- `Before writing a grasp, place, or step-up, check the target’s xyz in the scene geometry block and compare it to where the base will be at that point in the plan. The G1 can reach ~0.8 m from the base; anything beyond could require walking or climbing to be within reach.` 

- `Before EVERY walk, mentally trace the straight line from the current base xy to the next required base xy (implied by the next subgoal). If that line passes through any object’s xy footprint | movable OR fixed | the walk will collide and IK will fail at that mode. Movable objects in the way MUST be relocated before the walk; fixed objects (walls, pillars) MUST be routed around. There is no other way through; "just walk past it" is not an option the solver can rescue.` 

- `The robot body has non-zero width (~0.4 m). Treat any object whose footprint comes within roughly 0.2 m of the straight-line path as in the way, not just objects exactly on the line.` 

- `Estimate step count from distance: one G1 step covers ~0.4 m, so a 1 m approach is ~3 steps, a 2 m approach is ~5 steps, a 3 m approach is ~8 steps. Don’t over-step | extra steps inflate the expanded plan length and burn the mode budget. Round to the nearest integer; only round up if you’d otherwise end the walk out of arm’s reach for the next subgoal.` 

- `Track the base mode-by-mode. Soles move the base: xy follows the feet, z` _≈_ `sole-surface z + ~0.8 m. Stepping onto a box (via append_mode)` 

14 

```
raisesthebasebyroughlythebox’ssize_z.EEandobjectoperations
doNOTmovethebase.
```

- `Step-up height limit: the robot can only step onto a surface that is at most 0.8 m above its current support surface. Compute the height difference as (target_surface_z) - (current_support_surface_z); if it exceeds 0.8 m the step-up is infeasible and IK will fail. To reach a higher surface, stage the climb via an intermediate surface or hand assistend climbing.` 

```
Thesamelimitappliessymmetricallytostep-downs.
```

- `walk does not change which surface the feet are on. To get onto an elevated surface, emit explicit step-up modes via append_mode.` 

- `Re-read your plan before emitting it: at every append_mode, verify that the new contact is reachable from the base position implied by everything before it. If not, insert a walk (or step-up sequence) first.` 

#### `# Planning order` 

```
Beforewritinganycode,dothisauditinorder:
```

`1. Identify the final subgoal(s) the task requires.` 

`2. List every movable object whose xy footprint lies between the robot’s start position and any point the base must visit. These are obstacles and need to be relocated first, even if the task description doesn’t mention them.` 

`3. Write the plan: clearing subgoals first, then task subgoals.` 

#### `# Output format` 

```
Firststatethehigh-levelplaninoneline,e.g.:
```

```
"walktobox,two-EEgrasp,lift,walktotable,placeontable,release"
ThenemitthePythonbodyofgenerate_contact_plan(scene).Itmuststartfrom
get_initial_mode()andreturntheresultingdict.
```

#### `# Feedback` 

```
IftheIKsolverfindstheexpandedplaninfeasible,theevaluatorwillreport
atwhichmodefeasibilitybroke.Modeindicesstartat0,wheremode0isthe
scene’sinitialstate,andrefertotheFULLYEXPANDEDplan.Forexample:
```

```
"IKinfeasibleatmode5(of8);mode0isthescene’sinitialstate."
```

```
Afailureinsideawalkexpansionusuallymeansthesurroundinggrasp/
objectstateisincompatiblewithlocomotion(e.g.carryinganoversized
object),orthattherequestedstepcountiswrongforthegeometry|too
fewstepsleavesyououtofreachforthenextsubgoal,toomanyrunsyou
intosomething.Adjustn_stepsorrethinkthesubgoalorder.
```

```
#----Activetask:parkour_pick_place_2/default/place_box_on_table----
```

```
Pickthewhiteboxandplaceitontheelevatedtable.
```

```
#Discretecontactgoal
```

```
TheFINALmodeofyourcontact_mode_seqmustsatisfy:
"white_box":finalentrymustbe(6,8,1)(self_id=6,env_id=8,contact_type=1)
```

```
Partialmatchesarerewardedinsidethediscrete-goalband|matchingkofN
channelsgivesgoalprogressk/N|but
IKfeasibilityandTOcostareonlyevaluated
whenALLchannelsmatch(afullpassisrequiredtoadvancetothenextband).
```

#### `# Continuous cost term` 

```
Thesetargetsshapethetrajectory:whenIKpassesandTOruns,
planswhosefinalstateisclosertothetargetsconvergewith
lowerTOcost(lowerconstraintviolations+controljerk),
placingthemhigherinsidetheTObandofthescore.
```

```
(goal:box_on_table)
```

- `object ’white_box’ final xyz should be near (0.700, 0.000, 1.265)` 

15 

```
#----Scenegeometry----
```

```
Thescene’sinitialgeometry(xyzinmeters,sizeinmeters):
robotbase:xyz=[-1.00,0.00,0.77]
floor(fixed):xyz=[0.00,0.00,0.00]size=[1.5,0.7]
table_short(fixed):xyz=[0.00,0.00,0.36]size=[0.35,0.7,0.365]
table_tall(fixed):xyz=[0.80,0.00,0.56]size=[0.395,0.395,0.565]
white_box(movable):xyz=[-0.70,0.00,0.14]size=[0.1325,0.1275,0.135]
```

```
#----ActivescenesurfaceIDs----
```

```
ThereareTWOdistinctIDspacesineverycontacttuple:
```

```
env_id(globalfeatureindex,usedinEVERYtupleastheenv_id)
self_id(per-objectfeatureindex,usedonlyinobjectchannels)
```

```
Fortheactivescene,theIDsintrospectedfromthecompiled
contact_tampsceneare:
```

```
floor:
env_id1=floor_feat1(self_id1)[top]
table_short:
env_id2=table_short_feat1(self_id1)[top]
env_id3=table_short_feat2(self_id2)[left]
env_id4=table_short_feat3(self_id3)[front]
env_id5=table_short_feat4(self_id4)[right]
env_id6=table_short_feat5(self_id5)[back]
env_id7=table_short_feat6(self_id6)[bottom]
table_tall:
env_id8=table_tall_feat1(self_id1)[top]
env_id9=table_tall_feat2(self_id2)[left]
env_id10=table_tall_feat3(self_id3)[front]
env_id11=table_tall_feat4(self_id4)[right]
env_id12=table_tall_feat5(self_id5)[back]
env_id13=table_tall_feat6(self_id6)[bottom]
white_box:
env_id14=white_box_feat1(self_id1)[top]
env_id15=white_box_feat2(self_id2)[left]
env_id16=white_box_feat3(self_id3)[front]
env_id17=white_box_feat4(self_id4)[right]
env_id18=white_box_feat5(self_id5)[back]
env_id19=white_box_feat6(self_id6)[bottom]
```

```
Eachrowistaggedwiththefeature’sfacedirectionintheobject’s
bodyframe(‘top‘/‘bottom‘/‘front‘/‘back‘/‘left‘/‘right‘).
Useittopicktherightself_id:‘bottom‘iswhatrestsonahorizontal
surface,‘top‘iswhatreceivesastack,opposingpairs(‘front‘/‘back‘
or‘left‘/‘right‘)arethenaturaltwo-EEgrasppair.
```

```
Requiredchannels:"left_ee","right_ee","left_sole","right_sole","white_box"
```

```
EE/soleentriesare(env_id,contact_type);objectentriesare
(self_id,env_id,contact_type);()alwaysmeans"free".
contact_type=1(unilateral)istheonlysupportedvaluefornow.
```

```
Thescene’scompiledinitialmode(usethisasmode0):
```

```
contact_mode_seq={
’left_sole’:[(1,1)],
’right_sole’:[(1,1)],
’left_ee’:[()],
’right_ee’:[()],
’white_box’:[(6,1,1)],
}
```

16 

```
Movableobjects(eachneedsitsownchannel):"white_box"
```

```
============================================================
```

### **A.2 Tree Expansion and Sampling Details** 

- **Expansion sampling (population model):** We use the hierarchical sampling policy from ShinkaEvolve [22]. The evaluated nodes are partitioned into island subpopulations. At each expansion step, an island is first sampled uniformly, and the parent node is then sampled from the evaluated nodes in that island. This separates global exploration across islands from local exploitation within an island. 

Let _I_ denote the set of islands and let _N_ eval<sup>(</sup><sup>_k_)betheevaluatednodesinisland</sup><sup>_k∈I_.We</sup> first sample 

_k ∼_ Uniform( _I_ ) _._ 

Within the selected island, each node _i ∈ N_ eval<sup>(</sup><sup>_k_)isassignedaweightbasedonitsscore</sup> and offspring count. Let _Fi_ denote the node score and _oi_ the number of times node _i_ has already been expanded. We compute 


This favors high-scoring nodes while reducing the probability of repeatedly expanding nodes that have already produced many children. The island sampling promotes diversity across search directions, while the weighted parent sampling balances exploration and exploitation within each island. 

- **Island-based diversity maintenance.** Diversity is maintained by evolving separate island subpopulations in parallel. This prevents all expansions from concentrating around a single high-performing branch. To share useful discoveries across the tree, nodes may occasionally migrate between islands, while island elites are protected from migration so that each island preserves its own best search direction. 

- **Novelty-based rejection sampling.** After a new candidate is generated, novelty-based rejection sampling is applied before adding it to the tree. The mutable portion of the candidate is embedded and compared against existing nodes in the selected island using cosine similarity. If the maximum similarity exceeds a threshold _η_ , the candidate is considered potentially redundant. In this case, an LLM novelty judge is queried to determine whether the candidate is meaningfully different; candidates judged insufficiently novel are rejected and resampled. 

- **Inspiration sampling.** In addition to the main parent, the prompt includes inspiration nodes sampled from the tree. Following ShinkaEvolve [22], these inspirations are drawn from a mixture of high-performing nodes and randomly sampled nodes, using the selected island as the local sampling context. The high-performing inspirations expose the LLM to successful strategies, while the random inspirations encourage recombination with more diverse parts of the tree search. 

- **Mutation-type sampling.** Each expansion samples one of three mutation types: targeted diff edits, full rewrites, or crossover. We use probabilities 

_p_ diff = 0 _._ 6 _, p_ full = 0 _._ 3 _, p_ cross = 0 _._ 1 _._ 

Diff edits make localized changes to the parent node, full rewrites allow larger structural changes while preserving immutable code regions, and crossover samples an additional node and asks the LLM to combine ideas from both nodes. 

17 

## **B Evaluation** 

### **B.1 Task Descriptions** 

We describe below the eight loco-manipulation evaluation tasks. Figure 4 shows the corresponding scenes. 

- **(1) Banana.** The robot must grasp a banana placed out of reach, which requires reasoning about stacking the object in the scene on top of the table and climbing on top of the object placed on the table to gain height. 

- **(2) Box Stacking.** The robot must stack three boxes on top of each other to build the tallest possible stack, testing sequential manipulation and stability reasoning. 

- **(3) Climb Table w/ Box.** This task tightly couples locomotion and manipulation: the robot must climb onto a table while moving a box with it throughout the maneuver. 

- **(4) Long-Distance Pick & Place.** The robot must transport a box and place it on a distant table, evaluating the ability to combine extended locomotion with manipulation. 

- **(5) Move Through Clutter.** The robot must traverse a corridor obstructed by two boxes, probing obstacle-aware planning and interaction to reach the other side. 

- **(6, 7) Parkour Pick & Place 1 and 2.** These two variants pose increasingly difficult challenges. In the first, the robot must climb onto a table in order to place a box on an otherwise obstructed surface. In the second, more challenging variant, the robot must climb onto and back down from an intermediate table while carrying the box before placing it on the floor. 

- **(8) Under-Table Pick & Place.** The robot must reach into a confined space beneath a table, demanding low-clearance whole-body postures that go beyond standard standing manipulation. 


Figure 4: **Experiment scenes.** The eight loco-manipulation evaluation tasks, numbered as referenced in the text: (1) Banana, (2) Box Stacking, (3) Climb Table w/ Box, (4) Long-Dist. Pick & Place, (5) Move Through Clutter, (6) Parkour Pick & Place 1, (7) Parkour Pick & Place 2, and (8) Under-Table Pick & Place. 

18 

### **B.2 Real-World Deployment Snapshots** 


Figure 5: **Under-Table Pick & Place.** Real-world snapshots of the humanoid robot reaching into a confined space beneath a table to retrieve the box, demonstrating the low-clearance whole-body posture discovered by MotionDisco. 


Figure 6: **Move Through Clutter.** Real-world snapshots of the humanoid robot traversing a corridor obstructed by two boxes, interacting with the obstacles along the path to make way for passage. 


Figure 7: **Parkour Pick & Place 2.** Real-world snapshots of the humanoid robot climbing onto the table using its feet, while carrying the box, before placing it on a distant table after taking some steps. 


Figure 8: **Long-Distance Pick & Place.** Real-world snapshots of the humanoid robot transporting a box and placing it on a distant table, combining extended locomotion with manipulation. 

19 


Figure 9: **Climb Table w/ Box.** Real-world snapshots of the humanoid robot climbing onto a table while moving a box, using its hands as support on the table, and lifting up the box. 

20 

