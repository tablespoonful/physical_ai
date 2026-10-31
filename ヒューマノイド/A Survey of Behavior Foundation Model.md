---
title: "A Survey of Behavior Foundation Model: Next-Generation Whole-Body Control System of Humanoid Robots"
date: "2025-06-25"
authors: "Mingqi Yuan; Tao Yu; Wenqi Ge; Xiuyong Yao; Huijiang Wang; Jiayu Chen"
url: https://arxiv.org/abs/2506.20487
pdf: https://arxiv.org/pdf/2506.20487
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2506.20487)** / [論文ページ](https://arxiv.org/abs/2506.20487)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

1 

# A Survey of Behavior Foundation Model: Next-Generation Whole-Body Control System of Humanoid Robots 

Mingqi Yuan<sup>123*</sup> , Tao Yu<sup>2*</sup> , Wenqi Ge<sup>24*</sup> , Xiuyong Yao<sup>2</sup> , Dapeng Li<sup>2</sup> , Huijiang Wang<sup>5</sup> , Jiayu Chen<sup>48</sup> , Bo Li<sup>1</sup> , Wei Zhang<sup>26</sup> , _Senior Member, IEEE_ , Wenjun Zeng<sup>3</sup> , _Fellow, IEEE_ , Hua Chen<sup>27</sup><sup>_‡_</sup> , Xin Jin<sup>3</sup><sup>_†_</sup> 

**_Abstract_ —Humanoid robots are drawing significant attention as versatile platforms for complex motor control, human-robot interaction, and general-purpose physical intelligence. However, achieving efficient whole-body control (WBC) in humanoids remains a fundamental challenge due to sophisticated dynamics, underactuation, and diverse task requirements. While learningbased controllers have shown promise for complex tasks, their reliance on labor-intensive and costly retraining for new scenarios limits real-world applicability. To address these limitations, behavior(al) foundation models (BFMs) have emerged as a new paradigm that leverages large-scale pre-training to learn reusable primitive skills and broad behavioral priors, enabling zero-shot or rapid adaptation to a wide range of downstream tasks. In this paper, we present a comprehensive overview of BFMs for humanoid WBC, tracing their development across diverse pre-training pipelines. Furthermore, we discuss realworld applications, current limitations, urgent challenges, and future opportunities, positioning BFMs as a key approach toward scalable and general-purpose humanoid intelligence. Finally, we provide a curated and regularly updated collection of BFM papers and projects to facilitate further research, which is available at https://github.com/yuanmingqi/awesome-bfm-papers.** 

**_Index Terms_ —Humanoid robot, whole-body control, behavior foundation model, pre-training, adaptation.** 

the need for more general, robust, and scalable control frameworks. In the following sections, we begin by comprehensively reviewing previous humanoid WBC methods, ranging from traditional model-based to learning-based and task-specific controllers, before introducing the transformative approach— the behavior foundation model. This evolutionary trajectory not only reflects the field’s advancement toward enhanced intelligence and generalizability but also paves the way for the next-generation humanoid robot control systems. 


## I. INTRODUCTION 

**H** UMANOID robots are increasingly being developed anddeployed in a variety of real-world scenarios due to their human-like morphology and high degrees of freedom (DoF) [1]–[3]. These capabilities allow them to operate seamlessly in environments originally designed for humans, allowing them to perform locomotion, manipulation, and interaction tasks with versatility and agility. To enable such rich behaviors, whole-body control (WBC) plays a central role by coordinating numerous joints, contacts, and actuators to achieve balanced, agile, and safe full-body motions. However, designing effective WBC policies remains highly challenging due to the complex dynamics of humanoids, underactuation, frequent contact changes, and the strong coupling between locomotion, manipulation, and balance [4], [5]. These difficulties highlight 

> 1Department of Computing, The Hong Kong Polytechnic University, Hong Kong SAR, China.<sup>2</sup> LimX Dynamics, Shenzhen, China.<sup>3</sup> Ningbo Institute of Digital Twin, Eastern Institute of Technology, Ningbo, China.<sup>4</sup> Department of Data and Systems Engineering, The University of Hong Kong, Hong Kong SAR, China.<sup>5</sup> CREATE Lab, EPFL, Lausanne, Switzerland.<sup>6</sup> School of System Design and Intelligent Manufacturing, Southern University of Science and Technology, Shenzhen, China.<sup>7</sup> ZJU-UIUC Institute, Zhejiang University, Zhejiang, China.<sup>8</sup> INFIFORCE Intelligent Technology Co., Ltd., Zhejiang, China. 

> *Work done at LimX Dynamics, and these authors contributed equally. 

> _†_ Corresponding author: Xin Jin (jinxin@eitech.edu.cn). 

> _‡_ Project lead: Hua Chen (huachen@intl.zju.edu.cn). 

Fig. 1. A behavior foundation model learns broad behavior priors from largescale and diverse behavior data, which can then be conveniently adapted to a wide range of downstream tasks. 

## _A. Traditional Model-based Controller_ 

Traditional WBC methods have served as the cornerstone for locomotion and manipulation in early humanoid robots [6], [7]. These methods rely heavily on physics-based models and are typically structured into a predictive-reactive hierarchy: high-level planners like centroidal model predictive control (MPC) [8], [9] generate reference trajectories, while lowlevel task-space whole-body controllers solve optimal control problems (OCPs) [10] to track these objectives under dynamic constraints. For instance, operational space control [11] and hierarchical task control [12] establish the theoretical foundation, while [13] advances hierarchical quadratic programming (QP) solvers and enables real-time performance in multi-task scenarios such as balance, walking, and manipulation. Wholebody operational space control (WBOSC) extends these methods by integrating the control of multiple body parts, handling redundancy, and managing dynamic constraints across the entire robot body [14]–[16]. These frameworks have been widely applied in humanoids, such as Atlas [4], HRP-2 [17], and DLR’s torque-controlled robots [18], achieving robust locomotion and multi-contact interactions. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

2 


Fig. 2. Evolution map of the whole-body controller for humanoid robots. 

Despite their success, traditional WBC systems face critical limitations: (i) task design, gain tuning, and heuristic adjustments for complex behaviors ( _e.g._ , uneven terrain or dynamic transitions) remain labor-intensive and brittle, (ii) real-time MPC struggles with high-dimensional systems, often requiring simplifications that sacrifice dynamic fidelity [19], (iii) the lack of flexibility to execute highly dynamic skills ( _e.g._ , backflips or rapid contact switches) or adapt to unforeseen disturbances [20], and (iv) weak robustness, as even a little push may topple a robot with model-based walking controller. These challenges are especially significant in humanoids, where tasks often require rich coordination, contact reasoning, and situational awareness [21], [22]. As a result, recent research increasingly shifts toward data-driven approaches, aiming to learn motor skills, coordination policies, and behavioral priors from demonstrations or reinforcement learning [23], [24]. 

## _B. Learning-based and Task-specific Controller_ 

Learning-based methods, particularly reinforcement learning (RL) and imitation learning (IL), have emerged as promising alternatives to traditional WBC methods, enabling robots to acquire complex skills through environmental interaction or human demonstrations [25]–[35]. For example, the DeepMimic framework [23] combines deep RL with motion capture data, allowing physically simulated characters to learn dynamic skills while maintaining natural motion quality. This work is further extended by adversarial motion priors (AMP) [36], which enables more stylized and diverse character control while preserving physical realism. Similarly, the HoST [37] framework introduces an RL-based standingup controller that learns adaptive and stable motions across diverse laboratory and outdoor environments, highlighting the robustness and task-specific learning capability of RL. For ILbased approaches, the TRILL [38] approach combines virtual reality (VR) teleoperation with WBC for humanoid locomanipulation, demonstrating an 85% success rate in real-world bimanual tasks [39]. Further advances, such as ExBody [5], [40], develop an expressive WBC framework that decouples upper-body IL (for stylistic motions) from robust lower-body locomotion, enabling humanoid robots to dynamically adapt 

their gait while performing diverse movements. This approach overcomes the instability of full-body imitation caused by morphological mismatches between humans and robots. 

While learning-based methods have demonstrated remarkable success in diverse humanoid WBC tasks, they face fundamental challenges that limit their broader applicability. RL-based approaches suffer from sample inefficiency, often requiring millions of environment interactions to converge, while remaining highly sensitive to the reward function design— poorly shaped rewards can lead to unintended behaviors or local optima [41]. Furthermore, the simulation-to-reality (Sim2Real) gap exacerbates these limitations, as policies trained in simulation frequently degrade when confronted with real-world dynamics, sensor noise, and hardware imperfections [42]–[45]. In contrast, IL-based methods are more sampleefficient yet pose a significant challenge to data collection, and learned policies often inherit the biases and limitations of the demonstrator [46]–[50]. Moreover, both paradigms struggle with generalization, in which learned policies typically excel only at narrow tasks and fail to adapt to new scenarios without extensive retraining. These challenges collectively underscore the need for approaches that combine the flexibility of learning with structured priors for robustness and generalizability, a gap that behavior foundation models aim to bridge. 

## _C. Behavior Foundation Model_ 

The term ” **behavior(al) foundation model (BFM)** ” is first introduced in [51], which proposes a successor measurebased framework for training generalist policies capable of instantly imitating diverse behaviors from minimal demonstrations. It demonstrates that BFMs pretrained on unsupervised interaction data are promising for eliminating task-specific RL fine-tuning by solving imitation tasks through forwardbackward state feature matching, while simultaneously supporting multiple IL paradigms via a unified representation, such as behavioral cloning, reward inference, and distribution matching. Subsequent work [52]–[56] has established BFMs as a class of RL agents capable of unsupervised training on reward-free transitions while yielding approximately optimal 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

3 

policies for broad classes of reward functions at test time without additional learning or planning. 

In this paper, we extend the definition of BFMs as a specialized class of foundation models [57] designed to control agent behaviors in dynamic environments. As illustrated in Fig. 1, rooted in the principles of general foundation models ( _e.g._ , GPT-4 [58], CLIP [59], and SAM [60]) that leverage broad, self-supervised pre-training on large-scale static data, BFMs are often trained on extensive behavior data ( _e.g._ , human demonstrations, or agent-environment interactions), encoding a comprehensive spectrum of behaviors rather than specializing narrowly in single-task scenarios. This property ensures that the model can readily generalize across different tasks, contexts, or environments, demonstrating versatile and adaptive behavior generation capabilities. Recent advancements in vision-language-action (VLA) models [59], [61]–[63] have focused on integrating vision, language, and action to handle multi-modal tasks, excelling in dynamic settings where they generate context-aware responses based on visual and linguistic inputs. In contrast, BFMs are primarily designed for directly controlling agent behaviors such as locomotion, manipulation, and interaction. Moreover, most existing VLA models are applicable to relatively stable platforms, such as mechanical arms or wheeled humanoid robots [64], whereas BFMs are designed to handle the sophisticated WBC of fullsize humanoid robots. 

Inspired by the discussions above, it is worthwhile to conduct a systematic and comprehensive review of BFMs to provide a holistic perspective for subsequent research. To the best of our knowledge, this is the first study focused on the development of BFMs, particularly their applications in humanoid robots. The structure of this paper is organized as follows: Section II introduces the essential background information of this paper. Section III discusses the application of BFMs in humanoid WBC, including diverse pretraining and adaptation strategies. Section IV explores the potential applications of BFMs towards multiple industries, while summarizing the limitations of current BFMs. Section V highlights the opportunities for future advancements in BFMs, as well as the risks and ethical concerns associated with their development and deployment. Finally, Section VI summarizes the key findings and contributions of this paper. 

## II. BACKGROUND 

In this section, we introduce the basic background to support the subsequent analysis of BFM approaches. More specifically, we begin with an overview of the definition and evolution of the humanoid WBC systems. Then, we introduce the formulation of RL, which is currently widely employed to build learning-based and task-specific controllers. 

TABLE I 

MAIN NOTATIONS AND THEIR SEMANTICS USED IN THIS ARTICLE. 

|**Notation**|**Semantics**|
|---|---|
|_M_<br>_S_<br>_A_<br>_r_<sup>ext</sup>(**_s_**)<br>_r_<sup>int</sup>(**_s_**)<br>|Markov decision process<br>State space<br>Action space<br>Extrinsic/task reward function<br>Intrinsic reward function|
|_P_(d**_s_**<sup>_′_</sup>_|_**_s_**_,_**_a_**)<br>_γ_<br>_π_(d**_a_**_|_**_s_**)|Transition probability measure<br>Discount factor<br>Policy|
|_Q_<sup>_π_</sup><br>_r_ <sup>(</sup><sup>**_s_**</sup><sup>_,_</sup><sup>**_a_**)</sup>|Action-value function of policy _π_ and reward _r_|
|_M_<sup>_π_</sup>(_X|_**_s_**_,_**_a_**)<br>_F_(**_s_**_,_**_a_**)<br>_B_(**_s_**<sup>_′_</sup>)<br>_L_|Successor measure of policy _π_<br>Forward embedding<br>Backward embedding<br>Loss function|


to coordinate the motion of multiple robots’ appendages to execute multiple tasks simultaneously and reliably. It considers the entire robot body as a single and integrated system, managing locomotion, manipulation, and interaction with the environment using a unified set of control algorithms [14]. As illustrated in Fig. 2, the humanoid WBC has evolved from traditional model-based approaches to flexible learning-based approaches, moving toward a generalist that solves broad tasks in diverse scenarios [5], [64]–[68]. In line with this trend, BFMs have emerged as a promising approach to achieve general-purpose WBC through large-scale pre-training on diverse motion data, which will be comprehensively discussed in the following contents. 

## _B. Reinforcement Learning_ 

We frame the RL problem as a Markov decision pro= cess (MDP), which can be defined by a tuple _M_ ( _S, A, P, r_<sup>ext</sup> _, γ_ ) [69]. Here, _S_ is the state space, _A_ is the action space, _P_ ( **_s_**<sup>_′_</sup> _|_ **_s_** _,_ **_a_** ) is the probability measure on _S_ defining the stochastic transition to the next state **_s_**<sup>_′_</sup> obtained by taking action **_a_** in state **_s_** , _r_<sup>ext</sup> ( **_s_** ) : _S →_ R is the extrinsic/task reward function, and _γ ∈_ [0 _,_ 1] is a discount factor. A policy _π_ is defined as the probability measure _π_ ( **_a_** _|_ **_s_** ) that maps each state to a distribution over actions. Furthermore, we denote Pr( _·|_ **_s_** 0 _,_ **_a_** 0 _, π_ ) and E( _·|_ **_s_** 0 _,_ **_a_** 0 _, π_ ) as the probability and expectation operators under state-action sequences ( **_s_** _t,_ **_a_** _t_ ) _t≥_ 0 starting at ( **_s_** 0 _,_ **_a_** 0) and following the policy _π_ with **_s_** _t ∼ P_ ( **_s_** _t|_ **_s_** _t−_ 1 _,_ **_a_** _t−_ 1) and **_a_** _t ∼ π_ ( **_a_** _t|_ **_s_** _t_ ). The goal of RL is to learn a policy that maximizes the expected discounted return: 


Finally, we list all the main notations and their semantics used in this paper in Table I. 

## _A. Humanoid Whole-body Control_ 

Humanoid robots are expected to operate in unstructured environments that are dynamic and unpredictable, demanding control systems that are highly versatile, robust, reconfigurable, dexterous, and mobile compared to less agile robotic platforms [65]. To that end, the humanoid WBC is proposed 

## III. BFM FOR HUMANOID WHOLE-BODY CONTROL 

In this section, we introduce representative methods for constructing and adapting BFMs towards humanoid WBC, analyzing their main motivations, typical implementations, and empirical properties extensively. Fig. 3 offers an overview of 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

4 


Fig. 3. An overview of the pre-training pipelines and adaptation strategies for BFMs discussed in this review. The goal-conditioned learning requires an **extrinsic reward** function and large-scale human data, while intrinsic reward-driven learning uses **intrinsic rewards** generated by self-supervised tasks. In contrast, the forward-backward representation learning learns a forward embedding network (FEN) and a backward embedding network (BEN) using **rewardfree** transitions, which can then be combined with a specific reward function to infer a policy. For adaptation strategies, BFMs can be fine-tuned through common approaches, such as full fine-tuning (FFT) and low-rank adaptation (LoRA), as well as methods like latent space adaptation, which adjust the policy by modifying the latent task vector. Beyond fine-tuning, adaptation also involves strategies for hierarchical control, where high-level planners ( _e.g._ , generative models like LLMs or diffusion models) process abstract goals and generate subtasks for the BFM to execute as a low-level controller, enabling complex and long-horizon task completion. 

the pre-training pipelines and adaptation strategies that will be discussed in this review, and Table II lists the corresponding methods. **Note that some approaches might have been proposed before the emergence of the concept of BFMs, yet we still discuss them as long as they adhere to the properties of BFMs or their physical meaning is analogous to BFMs.** 

## _A. Pre-training_ 

Pre-training of BFMs seeks to learn reusable primitive skills and behavioral priors from large-scale data sources, creating a foundation for efficient downstream adaptation. Current approaches can be broadly categorized into three types: **goalconditioned learning** , **intrinsic reward-driven learning** , and the **forward-backward representation learning** . 

_1) Goal-conditioned Learning:_ As shown in Figure 4, goal-conditioned learning is a framework in RL where an agent’s behavior is conditioned on a specific goal or objective, typically provided as input. Unlike traditional RL, where the agent learns from raw state-action pairs without explicit taskspecific guidance, goal-conditioned learning integrates the goal into the agent’s policy, enabling it to adapt its actions toward achieving that specific goal. The goal can be specified in various forms, such as a target state, an objective function, or an external task description [70]–[72]. The key advantage of goal-conditioned learning lies in its ability to learn a more flexible and transferable policy that can be applied to a wide range of tasks, as it directly incorporates the task’s goal during training, rather than requiring retraining for each specific task. This makes it particularly useful in environments where the agent needs to solve multiple tasks or interact with changing environments. 

**Skill learning from motion tracking** . Among the diverse approaches to goal-conditioned learning, tracking-based learning represents a specialized form where the target behavior is explicitly defined by dense reference supervision or guidance, typically derived from motion capture data or expert demonstrations. At each time step, the agent is often trained to track the given reference motion’s joint angle or kinematic pose of the next time step [23]. The primary motivation behind tracking-based learning is that learning to track a single pose is more achievable and general than directly imitating a whole motion, especially a complex motion. 

For example, the TeamPlay [73] framework trains an agent to imitate a large amount of football motion capture data via a DeepMimic-like [23] approach, aiming to learn a complete behavior set required for the football game. Then the agent is leveraged to sample substantial state-action pairs to train a neural probabilistic motor primitive (NPMP) model [105] and derive a low-level latent-conditioned controller. Finally, the controller is applied for further drill learning by conducting RL with a drill-specific ( _e.g._ , follow, dribble, shoot, and kick-totarget) reward function. Here, the learned low-level controller can be viewed as a BFM as it learns realistic human-like movements based on motion capture data and can be rapidly adapted to diverse higher-level drill learning. 

Similarly, the adversarial skill embeddings (ASE) framework [74] learns a reusable latent space of motor skills by combining adversarial IL with unsupervised RL. Trained on unstructured motion data, ASE produces a latent-conditioned low-level controller capable of generating diverse and physically plausible behaviors, serving as a general-purpose motor prior to downstream tasks. Building on ASE, the conditional adversarial latent models (CALM) framework [75] incorporates a conditional discriminator to enable fine-grained control 

5 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

TABLE II 

TAXONOMY OF THE PRE-TRAINING AND ADAPTATION APPROACHES OF THE BFMS. THE ”*” SYMBOL INDICATES THAT THIS WORK HAS BEEN SUCCESSFULLY DEPLOYED IN REAL-WORLD HUMANOID ROBOTS. 

|**Item**|**Category**|**Algorithm**|
|---|---|---|
||Goal-Conditioned<br>Learning|TeamPlay [73], ASE [74], PHC [70], CALM [75], MTM [71],<br>CASE [76], InterMimic [77], MoConVQ [78], H-GAP [72],<br>MaskedMimic [79], HugWBC<sup>_∗_</sup>[66], HOVER<sup>_∗_</sup>[67], ModSkill [80],<br>CLONE<sup>_∗_</sup>[81], TWIST<sup>_∗_</sup>[82], TWIST2<sup>_∗_</sup>[83], AMS<sup>_∗_</sup>[84],<br>Any2Track<sup>_∗_</sup>[85], BFM4Humanoid<sup>_∗_</sup>[86], SONIC<sup>_∗_</sup>[87]|
|**Pre-training**|Intrinsic Reward-Driven<br>Learning|ICM [88], DIAYN [89], RND [90], APS [91],<br>ProtoRL [92], RE3 [93], ODPP [94]|
||Forward-Backward<br>Representation Learning|FB [95], FB-IL [51], FB-AW [52], FB-ARE [52],<br>FB-AWARE [52], Motivo [53], BFM-Zero<sup>_∗_</sup>[96]|
|**Adtti**|Fine-tuning|TokenHSI [97], Belief-FB [56], Rotation-FB [56],|
|**apaon**<br>**Adaptation**|Techniques|TaskTokens [55], ReLA [54], LoLA [54]|
||Towards Hierarchical<br>Control|UniHSI [98], TokenHSI [97], UniPhys [99], CLoSD [100],<br>LangWBC<sup>_∗_</sup>[101], LeVERB<sup>_∗_</sup>[102], BeyondMimic<sup>_∗_</sup>[103], SENTINEL<sup>_∗_</sup>[104]|


over generated motions through latent manipulation. This line of work is further extended by CASE [76], which introduces skill-conditioned IL with training techniques such as focal skill sampling and skeletal residual forces to enhance agility and motion diversity. 


Fig. 4. Workflow of the goal-conditioned learning, which enables versatile skill acquisition by training policies to achieve diverse target states specified through goal embeddings. 

While the methods above achieve efficient skill acquisition from large behavior datasets, the HugWBC [66] method explores learning versatile locomotion skills without relying on pre-collected motion data. The framework automatically generates adaptive behaviors through a structured RL process, where a general command space dynamically produces feasible velocity, gait, and posture targets during training. By reformulating WBC as a self-supervised command-tracking problem, the work establishes a new direction for developing general-purpose humanoid controllers that learn robust skills through environmental interaction rather than data imitation. 

Moving beyond body-level skill learning, ModSkill [80] introduces a modular framework that decouples full-body 

motion into part-specific skills for individual body parts. This modularization allows for efficient and scalable learning, as each body part is controlled independently by a low-level controller driven by part-specific skill embeddings. ModSkill’s ability to focus on body-part-level skills makes it a powerful system for controlling complex motions and adapting learned behaviors across different tasks. By utilizing a skill modularization attention layer, ModSkill enhances the generalization of motor skills across various tasks, such as reaching or striking, thereby further improving task-specific adaptation. 

**From primitive skills to high-level goal execution** . The success of BFMs in learning diverse primitive skills has propelled the development of more advanced BFMs capable of interpreting and executing high-level goals, including language instructions and multi-task objectives. A notable example is MoConVQ [78], which introduces a unified motion control framework based on discrete latent codes learned via vector quantized variational autoencoder (VQ-VAE). The model supports a wide range of downstream tasks, including motion tracking, interactive control, and text-to-motion generation, by offering a compact and modular representation. MoConVQ also integrates with large language models (LLMs) and enables the simulated agents to be directed via in-context language prompts, thereby bridging symbolic reasoning and physical control. 

Meanwhile, MaskedMimic [79] addresses physics-based character control as a general motion inpainting problem, producing full-body motions from partial descriptio, such as masked keyframes, objects, or text instructions. MaskedMimic involves a two-phase training process. First, a fully-constrained motion tracking controller is trained to imitate diverse reference motions. Then, a partially-constrained VAE-based policy distills this knowledge through masked goal conditioning. As a result, MaskedMimic can dynamically adapt to complex scenes and support applications ranging from VR control to complex human-object interaction (HOI), as illustrated in 

6 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 


Fig. 5. MaskedMimic [79] is a representative BFM trained via goalconditioned learning, which supports diverse control modalities and achieves seamless transitions between distinct tasks. 

Fig. 5. In addition, InterMimic [77] focuses on the HOI scenario and designs a two-stage teacher-student framework that distills imperfect motion capture interaction data into robust and physics-based controllers. Teacher policies are trained on subsets of noisy data and refined through simulation, then distilled into a student policy with RL-based fine-tuning. This curriculum strategy enables generalization across diverse interactions with high physical fidelity. 

For real-world robotic applications, HOVER [67] introduces a multi-mode policy distillation framework that enables humanoid robots to switch seamlessly between tasks ( _e.g._ , locomotion, manipulation, and navigation) using a single unified policy distilled from an oracle. This eliminates the need for task-specific controllers, demonstrating general-purpose control in real-world environments, akin to the versatility seen in MaskedMimic for virtual characters. 

All the above methods follow the idea of BFM, which is revealed from two aspects: (i) their ability to learn broad behavioral priors from diverse data sources, and (ii) their fast adaptation ability to downstream tasks. Trained on largescale data, these models generalize across a wide range of behaviors without being limited to a single domain. For example, InterMimic handles various HOI tasks, while MoConVQ adapts to tasks like goal-reaching and text-conditioned motion generation. Critically, they exhibit rapid adaptation to new scenarios with minimal retraining. Thus, the learned broad behavioral priors, along with the swift adaptation capability, characterize these methods as BFMs. 

_2) Intrinsic Reward-driven Learning:_ In tracking-based learning, the agent is consistently provided with an explicit objective ( _e.g._ , joint angles or velocities) and trained via a well-specified reward function to achieve targeted skill acquisition. In contrast, intrinsic reward-driven learning presents a distinct approach, where the agent is motivated to explore the environment without relying on explicit task-specific rewards. Instead, as illustrated in Fig. 6, the agent is guided by intrinsic rewards, which are self-generated signals that encourage exploration, skill acquisition, or novelty detection. 


Fig. 6. Workflow of the intrinsic reward-driven learning. The agent is trained to explore and comprehend the environment via self-supervised reward signals, thereby achieving non-directional skill acquisition. 

Extensive strategies for intrinsic reward-driven learning have been developed, including curiosity-driven exploration [88], [90], [106], [107], skill discovery [89], [91], [108], [109], and maximizing data coverage [92], [93], [110], [111], each encouraging the agent to explore different aspects of the environment. Denote by _r_<sup>int</sup> : _S →_ R the intrinsic reward function, the optimization objective in Eq. (1) is reformulated as 


For example, the intrinsic curiosity module (ICM) [88] encourages the agent to explore unfamiliar states by providing an intrinsic reward based on the prediction error between the current and predicted next state. The intrinsic reward is proportional to the discrepancy between the predicted state and the actual state, motivating the agent to interact with environments that it cannot predict, thereby driving exploration and learning. ICM has been shown to significantly improve the agent’s ability to explore complex environments with sparse or no external rewards. In contrast, DIAYN [89] utilizes latent variable discovery to guide the agent’s exploration, encouraging it to maximize the diversity of behaviors exhibited. DIAYN introduces an intrinsic reward based on the mutual information between the agent’s latent skill variable and its environment state, encouraging the agent to discover and explore a wide range of distinct behaviors. By learning a set of diverse, reusable skills, DIAYN enables agents to tackle complex tasks without requiring domain-specific rewards, making it a valuable approach for unsupervised skill discovery. 

In addition, RE3 [93] focuses on state coverage maximization, where the intrinsic reward is driven by the state visitation frequency. The goal is to encourage the agent to explore states that are infrequent or underrepresented in its past experience. By learning from these underexplored regions, RE3 enhances the agent’s understanding of the environment and helps prevent the agent from getting stuck in local optima. RE3 allows the agent to explore a broader range of states, improving the diversity of the learned representations 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

7 


and making it suitable for environments with sparse external rewards. Following DIAYN and RE3, ODPP [94] is proposed as a unified framework to discover skills that are both diverse and have superior state coverage, based on a novel use of the determinant point process. Specifically, the unsupervised objective is to maximize (i) the number of modes covered within each trajectory to enhance state coverage, and (ii) the number of modes across the trajectory space to promote skill diversity. 

Compared to BFMs trained on large-scale and diverse behavior datasets, intrinsic reward-driven models are typically trained on a single environment/task, which limits their ability to provide strong and intuitive behavioral priors. However, these models exhibit several key properties desirable for BFM pre-training. Specifically, they can (i) effectively explore the environment and action space and discover generalizable and latent behavioral priors under the motivation of intrinsic rewards, and (ii) demonstrate the capability to learn and adapt to various downstream tasks, as shown in [92], [112]. Therefore, we consider these methods as influential and conceptually related prototypes, whose unsupervised behavioral prior acquisition mechanisms can inspire the development of more effective BFMs. Future work may combine the exploratory advantages of intrinsic rewards with the task-specific utility of goal-conditioned learning, leading to a more comprehensive approach to behavioral prior learning. 

Fig. 7. Workflow of the forward-backward representation Learning, where a forward embedding network (FEN) and backward embedding network (BEN) are employed to learn the approximation of the successor measure, thereby achieving the universal policy representation. 

Eq. (5) decouples the action-value function as two separate terms: (i) the successor measure that models the evolution of the policy in the environment, and (ii) the reward function that captures task-relevant information. This factorization suggests that learning the successor measure for _π_ allows for the zeroshot evaluation of _Q_<sup>_π_</sup> _r_<sup>onanyrewardwithoutfurthertraining.</sup> Notably, the success measure can be estimated as [95] 


_3) Forward-backward Representation Learning:_ Recent advances in BFM are propelled by a novel framework entitled forward-backward (FB) representation learning [113]. As illustrated in Fig. 7, it disentangles policy learning from task-specific objectives, which is fundamentally different from goal-conditioned learning and intrinsic reward-driven learning. By learning a universal policy representation, it can be rapidly adapted to new tasks through reward inference or demonstration alignment, without additional environment interaction or policy optimization. 

where _ρ_ is an arbitrary distribution over states, _F_ : _S × A →_ R<sup>_d_</sup> is the forward embedding and _B_ : _S →_ R<sup>_d_</sup> is the backward embedding, respectively. Denote by **_z_** = E **_s_** _∼ρ_ [ _B_ ( **_s_** ) _r_ ( **_s_** )], the action-value function is rewritten as 


To learn a family of polices, both the forward embedding _F_ and policy _π_ can be parameterized by the same task encoding vector **_z_** [95], such that 

At its core, the FB representation learning seeks to learn a finite-rank approximation of the successor measure, which is an extension of the successor representation [114], [115]. It depicts the discounted future state visitation distribution as a measure over states. For each policy _π_ , its successor measure is defined as 


where **_z_** _⊆_ R<sup>_d_</sup> , and the policy _π_ **_z_** is defined as 


Then, the forward-backward embedding network is trained to minimize the temporal difference (TD) loss derived as the Bellman residual: 


The successor measure satisfies a measure-valued Bellman equation [113]: 


Equipped with the successor measure, the action-value function _Q_<sup>_π_</sup> _r_<sup>(</sup><sup>**_s_**</sup><sup>_,_</sup><sup>**_a_**)of</sup><sup>_π_foranyrewardfunction</sup><sup>_r_satisfies</sup> 

where **_s_**<sup>+</sup> denotes a future state and sg( _·_ ) denote the stopgradient operation. Consider continuous action spaces, the policies can be obtained by training an actor network to minimize 


IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

8 


Fig. 8. Motivo [53] learns broad behavior priors and demonstrates outstanding zero-shot adaptation capability to diverse downstream tasks, including complex motion imitation, pose reaching, and composite reward optimization. Moreover, Motivo achieves real-time motor control while ensuring motion naturalness. 

Once the FB model is trained, it can be utilized to solve diverse tasks in a zero-shot manner without performing additional task-specific learning, planning, or fine-tuning. For example, given a task reward function _r_ , the policy can be inferred by computing 


where _{_ **_s_** _i}_<sup>_n_</sup> _i_ =1<sup>isasetofsamplestates.Similarly,foragoal-</sup> reaching problem, it suffices to compute the encoder vector by **_zs_** = _B_ ( **_s_** ) _,_ **_s_** _∈S_ . 

As introduced in Section I-C, the term ”BFM” is first literally introduced in the FB-IL framework [51], which supports multiple IL principles without needing separate RL routines for each new task. FB-AW [52] enhances the FB framework by incorporating the advantage-weighted (AW) regression loss in offline RL algorithms, achieving stable performance on complex datasets ( _e.g._ , DMC Humanoid [116]) composed of near-optimal trajectories. The subsequent FB-AWARE [52] method further employs an auto-regressive encoding (ARE) mechanism to let fine-grained task features depend on coarsergrained task information. While the standard FB method employs a linear task projection that can blur rewards and reduce spatial precision, this mechanism can significantly enhance the expressivity and performance of the FB framework, particularly for tasks that require spatial accuracy or generalization. Notably, the AW and ARE mechanisms can be flexibly combined based on the task requirements. For example, the ARE mechanism can be used independently in the FB-ARE variant for environments where the AW component is not required for satisfactory performance. 

The FB framework provides a general and flexible approach for training BFMs by learning successor measure representations and applying pre-trained policies to new tasks. However, it suffers from several limitations: (i) when the latent dimension _d_ is finite, it relies on the assumption of a low- 

rank dynamic, leading to a limited inductive bias for policy selection; (ii) poor coverage in the training dataset causes offline learning to fail in reliably optimizing policies, often collapsing to a few suboptimal behaviors with weak performance on downstream tasks. These limitations greatly hinder the application of the FB framework for humanoid robots. To address these limitations, the Motivo framework [53] combines the FB framework with a conditional policy regularization (FB-CPR) term. As illustrated in Fig. 8, Motivo solves diverse humanoid WBC tasks in a zero-shot manner, including motion tracking, goal reaching, and reward optimization. 

Specifically, FB-CPR learns the FB representations with a discriminator-based regularization scheme, whose loss function is defined as 


where _D_ online is the associated replay buffer of unsupervised transitions, _pπ_ ( **_s_** _,_ **_z_** ) is the joint distribution of ( **_s_** _,_ **_z_** ) induced by FB, and _pE_ is the joint distribution of the dataset. However, it is intractable to optimize the divergence term directly via a RL procedure. To tackle the problem, FB-CPR interprets the divergence as an expected return under the policies and defines a divergence-based reward _r_<sup>div</sup> as 


Then, a discriminator network _D_ : _S × A →_ [0 _,_ 1] is trained to estimate the _r_<sup>div</sup> : 


The estimation holds due to the optimal discriminator satisfies _D_<sup>_∗_</sup> = _pEp_ + _<u>Epπ</u>_<sup>[117].Finally,thedivergencetermcanbe</sup> estimated by training another critic network via off-policy TD learning, and the actor loss for FB-CPR is rewritten as 


It is natural to find that FB-CPR is not a rigorous unsupervised method, as it leverages unlabeled demo data to assist motion prior learning. By aligning unsupervised RL with human-like behavioral priors from unlabeled data, FBCPR enhances policy diversity and dataset coverage, enabling the agent to learn a rich latent space of behaviors ( _e.g._ , walking, jumping, handstands) and achieve robust zero-shot performance across diverse tasks. Experimental results demonstrate that Motivo achieves an 83% success rate in motion tracking tasks, and performs 61% of the top-line performance in reward optimization tasks, surpassing DIFFUSER [118] in computational efficiency by requiring only 12 seconds per 300step episode. Additionally, it outperforms ASE and CALM in motion diversity, achieving a score of 4.70 ( _±_ 0.66), reflecting its ability to capture a broader range of behaviors. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

9 

Moving beyond simulated environments, BFM-Zero [96] first successfully deploys BFMs derived from the FB framework in real-world humanoid robots by introducing key architectural innovations that enhance sim-to-real robustness. Building upon the FB-CPR foundation, BFM-Zero incorporates a dual-critic architecture that augments the adversarial imitation objective with a separate critic network explicitly trained to maximize auxiliary stability rewards, such as action smoothness and joint limit avoidance. Meanwhile, BFM-zero integrates extensive domain randomization, history-based policies, and a scaled-up transformer-inspired residual network. These efforts collectively enable the learned policies to exhibit real-time, stable, and naturalistic WBC directly transferred from simulation to hardware, such as the Unitree G1 and Booster T1 robots, without any fine-tuning. 

## _B. Adaptation_ 

Equipped with the derived BFMs through the aforementioned pre-training frameworks, we next introduce recent advancements in the adaptation techniques of BFMs. These approaches can be broadly categorized into two types: **finetuning** and **towards hierarchical control** . It is worthwhile to highlight the distinction between the adaptation capabilities arising directly from pre-training and the fine-tuning approaches presented in this section. Pre-trained BFMs often exhibit representation-level generalization, allowing them to solve downstream tasks directly through task conditioning, such as providing goal states, latent vectors, or reward embeddings, without updating model parameters. For example, Motivo [53] can generate desirable locomotion simply by constructing a reward function that specifies the intended behavior. In contrast, the adaptation techniques reviewed below often involve refining parameters or introducing additional modules to further enhance performance in specific tasks or environments. 

_1) Fine-tuning:_ Fine-tuning of BFMs seeks to bridge the gap between general-purpose behavioral priors and taskspecific requirements. While pre-trained BFMs capture broad behavioral priors, they often lack precision for specialized tasks or novel environments. To address this, fast adaptation techniques such as residual latent adaptation (ReLA) and lookahead latent adaptation (LoLA) [54] enable BFMs to achieve zero-shot adaptation with minimal online interactions after pre-training. These methods improve task performance by up to 40%, demonstrating the effectiveness of fast adaptation strategies that enable efficient task switching without requiring extensive retraining. In contrast, methods like TaskTokens [55] enhance goal-conditioned BFMs by generating task-specific tokens through a task encoder, achieving high success rates across complex tasks such as motion tracking and goalreaching. TaskTokens shows up to 99.75% success in tasks such as the long jump. Furthermore, the belief-FB method [56] extends forward–backward representations by incorporating a transformer-based dynamics inference module, substantially improving robustness to unseen environmental variations and achieving a performance improvement of up to 2 _×_ . Future work could investigate additional post-training techniques, 

such as test-time scaling [119] or RL from human feedback [120], to further improve the adaptability and efficiency of BFMs and ensure alignment with human preferences in realworld applications. 

_2) Towards Hierarchical Control:_ While fine-tuning techniques enhance the performance of BFMs for specific tasks through minimal modifications during test time, several pioneering works have attempted to establish a hierarchical control architecture based on BFM, which decouples highlevel planning from low-level motion execution to achieve more scalable and flexible control [101], [102]. For example, UniHSI [98] introduces a unified framework for human-scene interaction by using language commands to guide a chainof-contacts, which represents the sequence of human-object contact pairs. The system translates language inputs into structured task plans, which are then executed by a unified controller based on the AMP architecture. This framework achieves semantic alignment between language commands and physical motions, supporting diverse interactions with single or multiple objects. TokenHSI [97] further extends this line by proposing a transformer-based unified policy that tokenizes human proprioception and task states. By separating shared motor knowledge (proprioception token) from taskspecific parameters (task tokens), it enables seamless multiskill unification and flexible adaptation to novel tasks, such as skill composition ( _e.g._ , carrying while sitting), variations in object or terrain shape, and long-horizon task completion. 

In contrast, CLoSD [100] introduces a text-driven RL controller that combines motion diffusion models with physicsbased simulations for robust multi-task control of human characters. By utilizing a real-time diffusion planner and a motion tracking controller in a closed-loop feedback system, CLoSD can handle complex tasks, such as goal-reaching, striking, and human-object interactions, all of which are controlled through text prompts and target locations. Similarly, UniPhys [99] introduces a diffusion-based behavior cloning framework that unifies planning and control with diffusion forcing to handle prediction errors, enabling flexible control via text, velocity, and goal guidance for applications, such as dynamic obstacle avoidance and long-horizon planning. These applications demonstrate that BFMs serve as a pivotal bridge between high-level semantic instructions and low-level physical execution, leveraging pre-trained behavioral priors to enable zero-shot adaptation, multi-task generalization, and physics-aware motion synthesis. By integrating various control paradigms ( _e.g._ , transformer-based tokenization and closedloop diffusion planning), these highlight the potential of BFMs to democratize humanoid control across complex, real-world scenarios, ranging from interactive robotics to dynamic environment adaptation. 

## IV. APPLICATIONS AND LIMITATIONS 

BFMs are foreseen to significantly enhance humanoid robotics by providing a universal pre-trained controller capable of generalizing across diverse tasks. In this section, we explore the potential applications of BFMs in various industries, including healthcare robotics and gaming. Furthermore, we 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

10 

identify the key limitations of current BFMs, including the Sim2Real gap, data bottleneck, and generalization to embodiment. An overview of the applications and limitations is illustrated in Fig. 9. Our analysis is inspired by the current development and applications of other foundation models, such as LLMs [121] and large vision models [122], [123]. 


Fig. 9. An overview of the practical applications and current limitations of BFMs. 

## _A. Applications_ 

_1) General Accelerator for Humanoid Robotics:_ BFMs will act as a transformative general accelerator for humanoid robotics, accelerating the development and deployment of advanced WBC systems. Unlike the previous pipelines that require resource-intensive and task-specific training, BFMs eliminate the need for training from scratch by pre-training on vast and diverse behavior datasets, thereby embedding a rich behavioral prior that accelerates downstream adaptation exponentially [54]. Moreover, advanced BFMs with zero-shot adaptation capabilities, such as Motivo [53], can directly map high-level task specifications ( _e.g._ , goal states and reward functions) to low-level control actions, bypassing traditional RL loops entirely. This capability efficiently solves basic control tasks but also facilitates rapid prototyping, allowing developers to evaluate robot behaviors in both simulation and real-world environments within minutes, dramatically shortening the development cycle. 

_2) Virtual Agents and Gaming:_ Virtual agents play a crucial role in advancing the development of BFMs for humanoid robots. Many foundational BFM techniques ( _e.g._ , large-scale motion pre-training and latent skill learning) are first developed and validated in simulation environments for virtual agents before being adapted for real-world humanoids. On the other hand, the strong growth of the game industry and metaverse platforms creates an increasing demand for natural, physically grounded avatar motions, which align closely with the objectives of humanoid BFMs [124]–[126]. BFMs offer a groundbreaking solution by enabling lifelike, context-aware non-player characters (NPCs) behaviors without extensive manual scripting. Pre-trained on diverse human behavior datasets, BFMs generate adaptive actions, such as 

tactical combat, social engagement, or exploration, seamlessly responding to dynamic player inputs. By integrating BFMs with LLMs, NPCs can interpret complex player instructions ( _e.g._ , dialogue-driven commands in role-playing games) and foster immersive and responsive interactions. This capability positions BFMs as a pivotal technology for revolutionizing virtual agents, enabling next-generation gaming experiences with unprecedented behavioral realism and interactivity. 

_3) Towards Industry 5.0:_ While Industry 4.0 introduced smart factories with cyber-physical systems, IoT, and AIdriven automation, Industry 5.0 shifts toward human-centric, resilient, and sustainable manufacturing, emphasizing collaborative robotics, adaptive intelligence, and personalized production [127]–[131]. To that end, robots must move beyond rigid automation and instead exhibit generalizable, adaptive, and explainable behaviors [132]–[136]. BFMs are expected to empower this landscape by enabling humanoid robots to seamlessly blend pre-trained motor skills with real-time adaptability, effortlessly switching between tasks like precision welding and adaptive part handling. By integrating large multimodal models with BFMs, robots can process diverse inputs like gestures, voice commands ( _e.g._ , ”handle gently”), or environmental cues, fostering intuitive human-robot collaboration in shared workspaces. BFMs also ensure resilience, autonomously recovering from disturbances like unbalanced loads in logistics, and support personalized production through zero-shot or few-shot learning. 

_4) Healthcare and Assistive Robotics:_ The global population aging presents unprecedented challenges for healthcare systems [137]–[140], resulting in an increased demand for assistive technologies that support independent living and rehabilitation. Extensive and diverse robots have been developed for robot-assisted dressing, rehabilitation therapy, medical treatment, and caregiving for the elderly and children [141]– [149]. Humanoid robots are ideally suited for these tasks due to their anthropomorphic design, navigating human-centric environments and perform precise, natural, and intuitive interactions. BFMs offer a promising solution by enabling robots to adapt to diverse user needs and unstructured environments. For instance, BFMs can empower assistive robots to perform tasks like mobility support ( _e.g._ , fall prevention, gait assistance) or daily tasks ( _e.g._ , object retrieval, meal preparation) with minimal user-specific tuning. In rehabilitation, BFMs trained on clinician-guided demonstrations can personalize therapy protocols by dynamically adjusting task difficulty or providing real-time feedback based on patient progress. 

## _B. Limitations_ 

_1) Sim2Real Gap:_ The Sim2Real gap is a persistent challenge in robotics, representing the performance discrepancy between the policies trained in simulators and their real-world deployment [42]–[45]. Traditional model-based controllers address this through explicit physics modeling and robust optimization, while data-driven approaches employ domain randomization and system identification [150]–[153]. Recent advancements like ASAP [154] mitigate dynamics mismatch via residual action learning yet face policy-specific limitations, 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

11 

as their residuals are trained on trajectories from a single pre-trained policy, thereby restricting generalization. BFMs exacerbate this challenge by encoding a vast spectrum of behaviors, ranging from locomotion to multi-contact interactions, which introduces high-dimensional transfer risks. For example, a BFM trained for diverse humanoid motions may fail to adapt to real-world actuator delays, friction variations, or sensor noise, resulting in unstable or unsafe execution. The integration of visual signals into control systems further compounds the challenge, and perceptual domain shifts ( _e.g._ , lighting, texture, or camera calibration mismatches) and generalization gaps in visual features can destabilize motion policies based on simulated visual inputs. Current BFMs remain largely confined to simulation, with no documented large-scale realworld deployments. While several pioneering works have been devoted to developing BFM-like controllers in real humanoid robots, such as HugWBC [66] and CLONE [81], their motion skills remain limited, highlighting a significant challenge to Sim2Real feasibility in maintaining behavior richness. This gap stems from behavioral overgeneralization, dynamics mismatches, and latent space instability, which hinder scaling targeted Sim2Real successes ( _e.g._ , quadruped locomotion or grasping) to BFM’s complexity. 

_2) Computational and System Integration Challenges:_ While the Sim2Real gap presents deployment challenges at the data and policy levels, another significant challenge in deploying BFMs arises from computational and system integration issues. To ensure responsive motion execution and effective disturbance rejection, the humanoid control policy typically requires real-time command updates at frequencies ranging from 50Hz to 100Hz [96], [155]. Unlike simulation environments, where computing resources are plentiful, realworld humanoids operate under strict constraints related to latency, power consumption, and thermal management. Although BFMs can excel with increased model size, as demonstrated by Motivo [53], these constraints limit the feasibility of using larger models. For instance, the BFM-Zero [96] only has a maximum parameter count of 44.5M, while SONIC [87] has 42M parameters. 

On the other hand, incorporating perceptual input ( _e.g._ , RGB or depth images) into BFMs further exacerbates the computational challenge, often requiring additional hardware acceleration to meet real-time processing demands. Devices like the NVIDIA Jetson computing board [156], [157] are commonly employed to offload the heavy computational burden of vision-based inference, enabling the robot to process complex multimodal data. However, integrating such hardware introduces significant complexity, particularly in synchronizing the robot’s control system with the inference hardware, managing data communication, and minimizing latency. The increased complexity can complicate overall system coordination, making it difficult to achieve seamless integration between perception, decision-making, and action execution. Future research could address these issues by exploring more efficient sensor fusion methods [158], model compression techniques [159], and hybrid inference architectures [160], etc. 

_3) Data Bottleneck:_ The data bottleneck poses a fundamental constraint in developing BFMs for humanoid robots. While 

the datasets listed in Table III have been successfully employed to train the current BFMs, their scale remains significantly smaller than the datasets used to train LLMs or large vision models. This scarcity is exacerbated when retargeting motions to specific robotic platforms [161], where subtle morphological differences can incur severe policy performance loss. Realworld robot data is even more constrained due to hardware limitations and safety concerns. The challenge compounds when considering multimodal data requirements. 

TABLE III 

AVAILABLE HUMANOID MOTION DATASETS FOR TRAINING BFMS. 

|**Dataset**|**Clip**|**Hour**|**Date**|
|---|---|---|---|
|KIT-ML [162]|3911|11.2|2016|
|AMASS [163]|11265|40.0|2019|
|LAFAN [164]|77|4.6|2020|
|BABEL [165]|13220|43.5|2021|
|Posescript [166]|-|-|2022|
|HumanML3D [167]|14616|28.6|2022|
|Motion-X [168]|81084|144.2|2023|
|Motion-X++ [169]|120462|180.9|2025|
|PHUMA [170]|76000|73.0|2025|
|Humanoid-X [171]|163800|240.0|2025|


Current BFMs predominantly rely on proprioceptive inputs, and integrating exteroceptive sensing for real-world deployment introduces new bottlenecks. Pioneering work, such as OmniH2O [172] explores multimodal data collection through teleoperation, pairing head-mounted RGBD cameras with whole-body proprioception and motor commands. While this enables tasks like vision-based autonomy and imitation learning, its 40-minute dataset (OmniH2O-6) remains limited to lab environments and lacks diverse contact dynamics. Currently, there is no existing dataset that provides largescale and temporally aligned recordings of proprioception, vision, and contact dynamics across diverse environments. Therefore, larger-scale, high-quality, and more curated datasets are urgently needed to enhance the effectiveness of current BFMs and to aid in the development of future models. 

_4) Embodiment Generalization:_ Despite the use of the term ”BFM”, current BFMs are typically trained on specific humanoid robot embodiments with fixed morphology, actuator dynamics, and sensor configurations. While they excel at controlling the robot they were trained on, it is currently intractable for them to generalize to novel embodiments with different body shapes, actuator types, or degrees of freedom. This limitation stems from several key challenges in embodiment generalization. One major issue is morphological mismatch, where policies designed for a specific kinematic or dynamic structure struggle to adapt to robots with differing link lengths, joint types, or mass distributions. Additionally, differences in actuator dynamics, such as variations in torque, latency, or control modes ( _e.g._ , position vs. torque control), can destabilize policies when transferred between systems. Sensor diversity introduces another layer of complexity, as BFMs often assume consistent sensor inputs and struggle to manage situations involving missing or additional sensing modalities. Furthermore, reward functions created for one type of embodiment ( _e.g._ , humanoid walking) may not effectively 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

12 

translate to others ( _e.g._ , hexapod gait patterns), resulting in confusion during task adaptation. These challenges underscore the necessity for more adaptable BFM architectures that can abstract skills across various robotic platforms. 

## V. OPPORTUNITIES AND RISKS 

In this section, we explore key research opportunities that could enhance the broader adoption of BFMs, including their integration into high-level ML systems, scaling laws, post-training techniques, and multi-agent coordination. We also critically examine the risks associated with BFMs, such as ethical concerns in human-robot interaction and safety mechanisms for real-world deployment. An overview of the opportunities and risks is illustrated in Fig. 10. By addressing these opportunities and risks, the robotics community can ensure that BFMs evolve into robust, adaptable, and socially responsible controllers for next-generation humanoid systems. 


Fig. 10. An overview of the future research opportunities and potential risks of BFMs. 

## _A. Opportunities_ 

_1) Multimodal BFMs:_ A promising direction for BFMs lies in expanding beyond proprioceptive inputs to multimodal sensory integration, incorporating exteroceptive signals such as vision, acoustic signals, and tactile feedback [173]–[175]. While current BFMs primarily rely on proprioceptive information, richer perceptual inputs could enable more robust and adaptive behaviors in unstructured environments. For example, integrating real-time visual perception could enable humanoids to dynamically adjust their movements based on object positions, terrain conditions, or human interactions, enhancing both safety and task performance. However, achieving multimodal BFMs requires the advancement of both large-scale datasets and scalable training paradigms, which are key challenges for the field. 

_2) High-level ML System:_ Recent advances in foundation models like LLMs and VLAs have demonstrated their potential as controllers for coordinating specialized AI systems [41], [176]–[181]. For example, HuggingGPT [176] leverages LLMs to orchestrate task planning across diverse models, while Eureka [41] employs LLMs to automate reward function 

design in RL. These projects present a natural pathway for integrating BFMs into high-level ML systems, where they could serve as universal low-level controllers for humanoid robots. By combining the reasoning capabilities of LLMs (for task planning and adaptation) with the motor priors encoded in BFMs (for real-time execution), such systems could achieve unprecedented flexibility in handling complex and multi-step physical tasks, while minimizing task-specific engineering. The ultimate vision is to create a unified cognitive-physical architecture based on LLMs and BFMs, mirroring the seamless integration of human cognition and physical control. 

_3) Scaling Law:_ The concept of scaling laws describes how the performance of neural language models improves with increases in model size, data, and compute resources. While these laws are well-established in domains like language and vision, their applicability to BFMs remains an open problem [182]–[186]. Preliminary evidence suggests that scaling BFMs through larger architectures, diverse training datasets, and expanded computational resources can enhance their generalization and zero-shot adaptation capabilities. For instance, FB-CPR [53] demonstrated improved performance in humanoid control tasks with more parameters (from 25M to 288M), achieving more robust zero-shot motion tracking and reward optimization. On the other hand, data scaling appears more critical for BFMs, as it directly determines the quality and physical plausibility of the learned behavior priors, the foundational requirements that model scaling alone cannot address. However, the effect of data scaling remains underexplored, with open questions as discussed in Section IV-B3. Furthermore, unlike LLMs, BFM scaling must strike an appropriate balance between behavior coverage (diverse motor skills) and control efficiency (precision and real-time stability). Future work should rigorously quantify these scaling dynamics to unlock the full potential of BFMs as general-purpose controllers. 

_4) Post-training:_ Post-training techniques have emerged as critical tools for the continued success and refinement of foundation models, especially for LLMs [187], which refine models to improve reasoning, address limitations, and better align with user intents and ethical considerations. Among these methods, fine-tuning [188]–[194], integration of RL [120], [195]–[201], and test-time scaling [119], [202], [203], [203], [204] have been the most prominent strategies for optimizing LLMs’ performance. Integrating these post-training strategies presents unique research opportunities for BFMs. For instance, leveraging RL techniques like RLHF and RLAIF for BFMs can be crucial for refining the alignment between the agent’s behavior and real-world human expectations, especially in human-centric task environments. This opens avenues for developing more robust models that can adapt dynamically to user feedback. Additionally, test-time scaling for BFMs can enhance computational efficiency during deployment, particularly for real-time robot control or decision-making systems. Research could focus on improving the scalability of BFMs while ensuring that model outputs remain accurate and contextually appropriate across varying operational conditions. 

_5) Multi-agent System:_ A multi-agent system (MAS) consists of multiple interacting agents that can be either coopera- 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

13 

tive, competitive, or a mix of both, aiming to address complex tasks that require collaboration, decision-making, and behavior coordination among agents [205]–[210]. BFMs can fundamentally accelerate the construction of MAS consists of humanoid robots, eliminating the need to effortlessly teach each robot basic survival skills like balance and locomotion before they can collaborate. Instead, researchers can focus directly on higher-level coordination challenges, such as role allocation and team strategy. However, current BFMs trained on singlerobot data lack the specialized interaction capabilities needed for optimal collaboration. This presents a promising research direction: developing next-generation BFMs trained explicitly on multi-robot interaction scenarios. Such models could better handle physical coordination challenges, such as object handovers, formation maintenance, and collision avoidance, while preserving their generalizability. 

_6) Evaluation Mechanism:_ While foundation models like LLMs benefit from well-established benchmarks ( _e.g._ , GPQA [211] for broad knowledge recall, MATH [212] for mathematical problem solving, or MUSR [213] for multi-step reasoning), there is no specific and comprehensive evaluation mechanism for evaluating BFM’s capability and guiding the evolution direction [214], [215]. A robust assessment of BFMs must consider multiple interdependent factors, including task generalization across unseen scenarios, adaptability to new skills with minimal data, robustness against physical perturbations, and alignment with human safety and interpretability standards. For example, Motivo [53] combines quantitative metrics, such as task success rates, with qualitative human evaluations of motion naturalness; yet, critical gaps remain in assessing compositional skill combinations, hardware-specific constraints, and long-term behavioral stability. Future benchmarks should focus on progressive difficulty levels and cross-domain transfer tests to effectively assess the potential of BFMs as generalpurpose physical controllers in both simulated and real-world scenarios. This approach will ultimately guide the field toward developing more capable and reliable humanoid systems. 

## _B. Risks_ 

_1) Ethical Issues:_ Ethical issues consistently accompany the development of diverse foundation models [216]–[218], which involve biased or unlicensed data, racial discrimination, and uncontrollable behaviors, etc. For BFMs, training on nondiverse motion datasets may encode demographic biases such as favoring movements natural to specific age groups or body types, which then propagate into robotic behaviors and create embodied forms of discrimination. Meanwhile, privacy risks escalate beyond data memorization to movement analytics, where rehabilitation or performance data could leak sensitive health information through generated motions. The physical instantiation of BFMs introduces unprecedented risks: unlike purely digital models, misaligned BFMs might reproduce unsafe or socially harmful behaviors ( _e.g._ , aggressive gestures, or exclusionary motions) with real-world consequences. While techniques like differential privacy and federated learning offer partial solutions, they struggle with the temporal nature of continuous motion data. In summary, BFMs demand novel 

governance frameworks that address both data provenance and normativity of real-time behavior. 

_2) Safety Mechanism:_ As BFMs will be increasingly deployed in real-world robotic systems, they introduce critical safety requirements beyond those of digital foundation models [219]–[221]. A key issue is maintaining model behavior integrity, particularly in safety-critical scenarios such as humanrobot interaction and autonomous navigation. When trained on large-scale yet weakly curated motion datasets, BFMs may unintentionally learn unsafe or undesirable behaviors. Even minor changes in sensory input, caused by adversarial attacks or sensor noise, can lead to control failures. This highlights the need for robustness against shifts in data distribution and protection against malicious input manipulation. 

While most current BFMs focus primarily on proprioceptive inputs, integrating multimodal information ( _e.g._ , visual, linguistic, and auditory cues) has emerged as a promising direction for more generalizable and situationally aware control. However, multimodality introduces new vulnerabilities. Adversaries can exploit inconsistencies across modalities, as seen in the well-known CLIP case where an apple image was misclassified as an ”iPod” due to an overlaid label [222]. Such cross-modal confusion can be especially dangerous when a BFM is adapted for an unimodal task but retains sensitivity to irrelevant signals from other modalities. These challenges underscore the need to develop robust safety mechanisms for BFMs. Future work could prioritize adversarial robustness, cross-modal consistency checks, and disentangling modalityspecific information to ensure predictable, trustworthy robot behavior in open-world environments. 

## VI. CONCLUSION 

In this paper, we present a systematic review of the behavior foundation model, an emerging and transformative paradigm of humanoid whole-body control systems. By pre-training on large-scale and diverse humanoid behavior data, BFMs learn broad behavior priors that enable few-shot or zeroshot adaptation to diverse downstream tasks, eliminating the need for resource-intensive and task-specific retraining. We establish a comprehensive taxonomy that categorizes BFM approaches into pre-training pipelines and adaptation strategies, demonstrating their real-world applicability across industrial, gaming, and healthcare domains. Furthermore, we highlight future research opportunities in multimodal BFMs, high-level ML system integration, post-training optimization, and standardized evaluation mechanisms that could accelerate BFM development. 

Despite their unprecedented capabilities, BFMs face significant challenges, including the Sim2Real gap, embodiment dependence, and data scarcity. The physical instantiation of BFMs introduces unique safety risks that require robust verification mechanisms, while their training on human motion data likely raises ethical concerns regarding privacy and bias mitigation. Addressing these limitations in future work will lead to more reliable and generalizable BFMs. Our work is expected to inspire more subsequent research on BFMs. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

14 

## ACKNOWLEDGMENTS 

This work is supported, in part, by the Hong Kong SAR Research Grants Council under Grant No. PolyU 15224823, the Guangdong Basic and Applied Basic Research Foundation under Grant No. 2024A1515011524, the NSFC under Grant No. 62302246, the ZJNSFC under Grant No. LQ23F010008, the Ningbo under Grants No. 2023Z237 & 2023CX050011 & 2024Z284 & 2024Z289 & 2025Z038, and the Ningbo Institute of Digital Twin (IDT) under Grant No. S203.2.01.32.002. This work is also supported by the High Performance Computing Center at the IDT and the Eastern Institute of Technology, Ningbo. 

## REFERENCES 

- [1] K. Darvish, L. Penco, J. Ramos, R. Cisneros, J. Pratt, E. Yoshida, S. Ivaldi, and D. Pucci, “Teleoperation of humanoid robots: A survey,” _IEEE Transactions on Robotics_ , vol. 39, no. 3, pp. 1706–1727, 2023. 

- [2] K. L. Valenzuela, S. I. Roxas, and Y.-H. Wong, “Embodying intelligence: humanoid robot advancements and future prospects,” in _International Conference on Human-Computer Interaction_ , pp. 295– 303, Springer, 2024. 

- [3] Y. Tong, H. Liu, and Z. Zhang, “Advancements in humanoid robots: A comprehensive review and future prospects,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 11, no. 2, pp. 301–328, 2024. 

- [4] S. Kuindersma, R. Deits, M. Fallon, A. Valenzuela, H. Dai, F. Permenter, T. Koolen, P. Marion, and R. Tedrake, “Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot,” _Autonomous Robots_ , vol. 40, pp. 429–455, 2016. 

- [5] X. Cheng, Y. Ji, J. Chen, R. Yang, G. Yang, and X. Wang, “Expressive whole-body control for humanoid robots,” in _Robotics: Science and Systems (RSS)_ , 2024. 

- [6] D. Kuli´c, G. Venture, K. Yamane, E. Demircan, I. Mizuuchi, and K. Mombaur, “Anthropomorphic movement analysis and synthesis: A survey of methods and applications,” _IEEE Transactions on Robotics_ , vol. 32, no. 4, pp. 776–795, 2016. 

- [7] A. Goswami and P. Vadakkepat, _Humanoid robotics: a reference_ . Springer Dordrecht, 2019. 

- [8] M. Schwenzer, M. Ay, T. Bergs, and D. Abel, “Review on model predictive control: An engineering perspective,” _The International Journal of Advanced Manufacturing Technology_ , vol. 117, no. 5, pp. 1327–1349, 2021. 

- [9] G. Romualdi, S. Dafarra, G. L’Erario, I. Sorrentino, S. Traversaro, and D. Pucci, “Online non-linear centroidal mpc for humanoid robot locomotion with step adjustment,” in _2022 International Conference on Robotics and Automation (ICRA)_ , pp. 10412–10419, IEEE, 2022. 

- [10] S. P. Sethi and S. P. Sethi, _What is optimal control theory?_ Springer, 2021. 

- [11] O. Khatib, “A unified approach for motion and force control of robot manipulators: The operational space formulation,” _IEEE Journal on Robotics and Automation_ , vol. 3, no. 1, pp. 43–53, 2003. 

- [12] L. Sentis and O. Khatib, “Synthesis of whole-body behaviors through hierarchical control of behavioral primitives,” _International Journal of Humanoid Robotics_ , vol. 2, no. 04, pp. 505–518, 2005. 

- [13] A. Escande, N. Mansard, and P.-B. Wieber, “Hierarchical quadratic programming: Fast online humanoid-robot motion generation,” _The International Journal of Robotics Research_ , vol. 33, no. 7, pp. 1006– 1028, 2014. 

- [14] L. Sentis and O. Khatib, “A whole-body control framework for humanoids operating in human environments,” in _2006 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 2641–2648, IEEE, 2006. 

- [15] D. Kim, Y. Zhao, G. Thomas, B. R. Fernandez, and L. Sentis, “Stabilizing series-elastic point-foot bipeds using whole-body operational space control,” _IEEE Transactions on Robotics_ , vol. 32, no. 6, pp. 1362–1379, 2016. 

- [16] C.-L. Fok, G. Johnson, J. D. Yamokoski, A. Mok, and L. Sentis, “Controlit!—a software framework for whole-body operational space control,” _International Journal of Humanoid Robotics_ , vol. 13, no. 01, p. 1550040, 2016. 

- [17] E. Dantec, M. Naveau, P. Fernbach, N. Villa, G. Saurel, O. Stasse, M. Taix, and N. Mansard, “Whole-body model predictive control for biped locomotion on a torque-controlled humanoid robot,” in _2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids)_ , pp. 638–644, 2022. 

- [18] B. Henze, A. Dietrich, and C. Ott, “An approach to combine balancing with hierarchical whole-body control for legged humanoid robots,” _IEEE Robotics and Automation Letters_ , vol. 1, no. 2, pp. 700–707, 2015. 

- [19] S. Sovukluk, J. Englsberger, and C. Ott, “Whole body control formulation for humanoid robots with closed/parallel kinematic chains: Kangaroo case study,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 10390–10396, IEEE, 2023. 

- [20] K. Ishihara, T. D. Itoh, and J. Morimoto, “Full-body optimal control toward versatile and agile behaviors in a humanoid robot,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 1, pp. 119–126, 2019. 

- [21] Y. Hao, G. C. R. Bethala, N. Pudasaini, H. Huang, S. Yuan, C. Wen, B. Huang, A. Nguyen, and Y. Fang, “Embodied chain of action reasoning with multi-modal foundation model for humanoid locomanipulation,” _arXiv preprint arXiv:2504.09532_ , 2025. 

- [22] M. Murooka, K. Fukumitsu, M. Hamze, M. Morisawa, H. Kaminaga, F. Kanehiro, and E. Yoshida, “Whole-body multi-contact motion control for humanoid robots based on distributed tactile sensors,” _IEEE Robotics and Automation Letters_ , 2024. 

- [23] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “Deepmimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Transactions On Graphics (TOG)_ , vol. 37, no. 4, pp. 1–14, 2018. 

- [24] A. Singh, H. Liu, G. Zhou, A. Yu, N. Rhinehart, and S. Levine, “Parrot: Data-driven behavioral priors for reinforcement learning,” in _International Conference on Learning Representations_ , 2021. 

- [25] J. Kober, J. A. Bagnell, and J. Peters, “Reinforcement learning in robotics: A survey,” _The International Journal of Robotics Research_ , vol. 32, no. 11, pp. 1238–1274, 2013. 

- [26] N. S¨underhauf, O. Brock, W. Scheirer, R. Hadsell, D. Fox, J. Leitner, B. Upcroft, P. Abbeel, W. Burgard, M. Milford, _et al._ , “The limits and potentials of deep learning for robotics,” _The International Journal of Robotics Research_ , vol. 37, no. 4-5, pp. 405–420, 2018. 

- [27] H. Nguyen and H. La, “Review of deep reinforcement learning for robot manipulation,” in _2019 Third IEEE International Conference on Robotic Computing (IRC)_ , pp. 590–595, IEEE, 2019. 

- [28] A. I. K´aroly, P. Galambos, J. Kuti, and I. J. Rudas, “Deep learning in robotics: Survey on model structures and training strategies,” _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ , vol. 51, no. 1, pp. 266–279, 2020. 

- [29] R. Liu, F. Nageotte, P. Zanne, M. de Mathelin, and B. Dresp-Langley, “Deep reinforcement learning for the control of robotic manipulation: a focussed mini-review,” _Robotics_ , vol. 10, no. 1, p. 22, 2021. 

- [30] C. Huang, G. Wang, Z. Zhou, R. Zhang, and L. Lin, “Rewardadaptive reinforcement learning: Dynamic policy gradient optimization for bipedal locomotion,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 6, pp. 7686–7695, 2022. 

- [31] T. Zhang, S. Guo, T. Tan, X. Hu, and F. Chen, “Adjacency constraint for efficient hierarchical reinforcement learning,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 4, pp. 4152– 4166, 2022. 

- [32] J. Wu, Y. Zhou, H. Yang, Z. Huang, and C. Lv, “Human-guided reinforcement learning with sim-to-real transfer for autonomous navigation,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 12, pp. 14745–14759, 2023. 

- [33] J. Chen, D. Tamboli, T. Lan, and V. Aggarwal, “Multi-task hierarchical adversarial inverse reinforcement learning,” in _International Conference on Machine Learning_ , vol. 202 of _Proceedings of Machine Learning Research_ , pp. 4895–4920, PMLR, 2023. 

- [34] Z. Zhu, K. Lin, A. K. Jain, and J. Zhou, “Transfer learning in deep reinforcement learning: A survey,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , vol. 45, no. 11, pp. 13344–13362, 2023. 

- [35] G. Luo, Y. Zhou, M. Huang, T. Ren, X. Sun, and R. Ji, “Moil: Momentum imitation learning for efficient vision-language adaptation,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [36] X. B. Peng, Z. Ma, P. Abbeel, S. Levine, and A. Kanazawa, “Amp: Adversarial motion priors for stylized physics-based character control,” _ACM Transactions on Graphics (ToG)_ , vol. 40, no. 4, pp. 1–20, 2021. 

- [37] T. Huang, J. Ren, H. Wang, Z. Wang, Q. Ben, M. Wen, X. Chen, J. Li, and J. Pang, “Learning humanoid standing-up control across diverse postures,” in _Robotics: Science and Systems (RSS)_ , 2025. 

15 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

- [38] M. Seo, S. Han, K. Sim, S. H. Bang, C. Gonzalez, L. Sentis, and Y. Zhu, “Deep imitation learning for humanoid loco-manipulation through human teleoperation,” in _2023 IEEE-RAS 22nd International Conference on Humanoid Robots (Humanoids)_ , pp. 1–8, IEEE, 2023. 

- [39] S. H. Bang, C. Gonzalez, J. Ahn, N. Paine, and L. Sentis, “Control and evaluation of a humanoid robot with rolling contact joints on its lower body,” _Frontiers in Robotics and AI_ , vol. 10, p. 1164660, 2023. 

- [40] M. Ji, X. Peng, F. Liu, J. Li, G. Yang, X. Cheng, and X. Wang, “Exbody2: Advanced expressive humanoid whole-body control,” in _RSS 2025 Workshop on Whole-body Control and Bimanual Manipulation: Applications in Humanoids and Beyond_ , 2025. 

- [41] Y. J. Ma, W. Liang, G. Wang, D.-A. Huang, O. Bastani, D. Jayaraman, Y. Zhu, L. Fan, and A. Anandkumar, “Eureka: Human-level reward design via coding large language models,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [42] A. Kadian, J. Truong, A. Gokaslan, A. Clegg, E. Wijmans, S. Lee, M. Savva, S. Chernova, and D. Batra, “Sim2real predictivity: Does evaluation in simulation predict real-world performance?,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 4, pp. 6670–6677, 2020. 

- [43] S. H¨ofer, K. Bekris, A. Handa, J. C. Gamboa, M. Mozifian, F. Golemo, C. Atkeson, D. Fox, K. Goldberg, J. Leonard, _et al._ , “Sim2real in robotics and automation: Applications and challenges,” _IEEE Transactions on Automation Science and Engineering_ , vol. 18, no. 2, pp. 398– 400, 2021. 

- [44] K. Iyengar, S. H. Sadati, C. Bergeles, S. Spurgeon, and D. Stoyanov, “Sim2real transfer of reinforcement learning for concentric tube robots,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 10, pp. 6147–6154, 2023. 

- [45] E. Su, C. Jia, Y. Qin, W. Zhou, A. Macaluso, B. Huang, and X. Wang, “Sim2real manipulation on unknown objects with tactilebased reinforcement learning,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 9234–9241, IEEE, 2024. 

- [46] S. Schaal, “Is imitation learning the route to humanoid robots?,” _Trends in Cognitive Sciences_ , vol. 3, no. 6, pp. 233–242, 1999. 

- [47] A. Hussein, M. M. Gaber, E. Elyan, and C. Jayne, “Imitation learning: A survey of learning methods,” _ACM Computing Surveys (CSUR)_ , vol. 50, no. 2, pp. 1–35, 2017. 

- [48] M. Laskey, J. Lee, R. Fox, A. Dragan, and K. Goldberg, “Dart: Noise injection for robust imitation learning,” in _Conference on Robot Learning_ , pp. 143–156, PMLR, 2017. 

- [49] B. Fang, S. Jia, D. Guo, M. Xu, S. Wen, and F. Sun, “Survey of imitation learning for robotic manipulation,” _International Journal of Intelligent Robotics and Applications_ , vol. 3, no. 4, pp. 362–369, 2019. 

- [50] J. Hua, L. Zeng, G. Li, and Z. Ju, “Learning for a robot: Deep reinforcement learning, imitation learning, transfer learning,” _Sensors_ , vol. 21, no. 4, 2021. 

- [51] M. Pirotta, A. Tirinzoni, A. Touati, A. Lazaric, and Y. Ollivier, “Fast imitation via behavior foundation models,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [52] E. Cetin, A. Touati, and Y. Ollivier, “Finer behavioral foundation models via auto-regressive features and advantage weighting,” in _Reinforcement Learning Conference_ , 2025. 

- [53] A. Tirinzoni, A. Touati, J. Farebrother, M. Guzek, A. Kanervisto, Y. Xu, A. Lazaric, and M. Pirotta, “Zero-shot whole-body humanoid control via behavioral foundation models,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [54] H. Sikchi, A. Tirinzoni, A. Touati, Y. Xu, A. Kanervisto, S. Niekum, A. Zhang, A. Lazaric, and M. Pirotta, “Fast adaptation with behavioral foundation models,” in _Reinforcement Learning Conference_ , 2025. 

- [55] R. Vainshtein, Z. Rimon, S. Mannor, and C. Tessler, “Task tokens: A flexible approach to adapting behavior foundation models,” _arXiv preprint arXiv:2503.22886_ , 2025. 

- [56] M. Bobrin, I. Zisman, A. Nikulin, V. Kurenkov, and D. Dylov, “Zeroshot adaptation of behavioral foundation models to unseen dynamics,” _arXiv preprint arXiv:2505.13150_ , 2025. 

- [57] R. Bommasani, D. A. Hudson, E. Adeli, R. Altman, S. Arora, S. von Arx, M. S. Bernstein, J. Bohg, A. Bosselut, E. Brunskill, _et al._ , “On the opportunities and risks of foundation models,” _arXiv preprint arXiv:2108.07258_ , 2021. 

- [58] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [59] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, _et al._ , “Learning transferable visual models from natural language supervision,” in _International Conference on Machine Learning_ , pp. 8748–8763, PMLR, 2021. 

- [60] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo, _et al._ , “Segment anything,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 4015–4026, 2023. 

- [61] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ , pp. 2165–2183, PMLR, 2023. 

- [62] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ , PMLR, 2024. 

- [63] J. Wen, Y. Zhu, J. Li, M. Zhu, Z. Tang, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, _et al._ , “Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [64] G. Zambella, G. Lentini, M. Garabini, G. Grioli, M. G. Catalano, A. Palleschi, L. Pallottino, A. Bicchi, A. Settimi, and D. Caporale, “Dynamic whole-body control of unstable wheeled humanoid robots,” _IEEE Robotics and Automation Letters_ , vol. 4, no. 4, pp. 3489–3496, 2019. 

- [65] F. L. Moro and L. Sentis, “Whole-body control of humanoid robots,” _Humanoid Robotics: A Reference_ , pp. 1161–1183, 2019. 

- [66] Y. Xue, W. Dong, M. Liu, W. Zhang, and J. Pang, “A unified and general humanoid whole-body controller for versatile locomotion,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [67] T. He, W. Xiao, T. Lin, Z. Luo, Z. Xu, Z. Jiang, J. Kautz, C. Liu, G. Shi, X. Wang, _et al._ , “Hover: Versatile neural whole-body controller for humanoid robots,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , IEEE, 2025. 

- [68] Y. Wang, M. Yang, Z. Ding, Y. Zhang, W. Zeng, X. Xu, H. Jiang, and Z. Lu, “From experts to a generalist: Toward general whole-body control for humanoid robots,” in _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 

- [69] R. S. Sutton, A. G. Barto, _et al._ , _Reinforcement learning: An introduction_ , vol. 1. MIT press Cambridge, 1998. 

- [70] Z. Luo, J. Cao, K. Kitani, W. Xu, _et al._ , “Perpetual humanoid control for real-time simulated avatars,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 10895–10904, 2023. 

- [71] P. Wu, A. Majumdar, K. Stone, Y. Lin, I. Mordatch, P. Abbeel, and A. Rajeswaran, “Masked trajectory models for prediction, representation, and control,” in _International Conference on Machine Learning_ , pp. 37607–37623, PMLR, 2023. 

- [72] Z. Jiang, Y. Xu, N. Wagener, Y. Luo, M. Janner, E. Grefenstette, T. Rockt¨aschel, and Y. Tian, “H-GAP: Humanoid control with a generalist planner,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [73] S. Liu, G. Lever, Z. Wang, J. Merel, S. A. Eslami, D. Hennes, W. M. Czarnecki, Y. Tassa, S. Omidshafiei, A. Abdolmaleki, _et al._ , “From motor control to team play in simulated humanoid football,” _Science Robotics_ , vol. 7, no. 69, 2022. 

- [74] X. B. Peng, Y. Guo, L. Halper, S. Levine, and S. Fidler, “Ase: Largescale reusable adversarial skill embeddings for physically simulated characters,” _ACM Transactions On Graphics (TOG)_ , vol. 41, no. 4, pp. 1–17, 2022. 

- [75] C. Tessler, Y. Kasten, Y. Guo, S. Mannor, G. Chechik, and X. B. Peng, “Calm: Conditional adversarial latent models for directable virtual characters,” in _ACM SIGGRAPH 2023 Conference_ , pp. 1–9, 2023. 

- [76] Z. Dou, X. Chen, Q. Fan, T. Komura, and W. Wang, “C· ase: Learning conditional adversarial skill embeddings for physics-based characters,” in _SIGGRAPH Asia 2023 Conference_ , pp. 1–11, 2023. 

- [77] S. Xu, H. Y. Ling, Y.-X. Wang, and L.-Y. Gui, “Intermimic: Towards universal whole-body control for physics-based human-object interactions,” in _Proceedings of the IEEE/CVF Computer Vision and Pattern Recognition Conference_ , 2025. 

- [78] H. Yao, Z. Song, Y. Zhou, T. Ao, B. Chen, and L. Liu, “Moconvq: Unified physics-based motion control via scalable discrete representations,” _ACM Transactions on Graphics (TOG)_ , vol. 43, no. 4, pp. 1–21, 2024. 

- [79] C. Tessler, Y. Guo, O. Nabati, G. Chechik, and X. B. Peng, “Maskedmimic: Unified physics-based character control through masked motion inpainting,” _ACM Transactions on Graphics (TOG)_ , vol. 43, no. 6, pp. 1–21, 2024. 

- [80] Y. Huang, Z. Dou, and L. Liu, “Modskill: Physical character skill modularization,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 12394–12404, 2025. 

16 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

- [81] Y. Li, Y. Lin, J. Cui, T. Liu, W. Liang, Y. Zhu, and S. Huang, “CLONE: Closed-loop whole-body humanoid teleoperation for longhorizon tasks,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [82] Y. Ze, Z. Chen, J. P. Araujo, Z. ang Cao, X. B. Peng, J. Wu, and K. Liu, “TWIST: Teleoperated whole-body imitation system,” in _9th Annual Conference on Robot Learning_ , 2025. 

- [83] Y. Ze, S. Zhao, W. Wang, A. Kanazawa, R. Duan, P. Abbeel, G. Shi, J. Wu, and C. K. Liu, “Twist2: Scalable, portable, and holistic humanoid data collection system,” _arXiv preprint arXiv:2511.02832_ , 2025. 

- [84] Y. Pan, R. Qiao, L. Chen, K. Chitta, L. Pan, H. Mai, Q. Bu, H. Zhao, C. Zheng, P. Luo, _et al._ , “Agility meets stability: Versatile humanoid control with heterogeneous data,” _arXiv preprint arXiv:2511.17373_ , 2025. 

- [85] Z. Zhang, J. Guo, C. Chen, J. Wang, C. Lin, Y. Lian, H. Xue, Z. Wang, M. Liu, J. Lyu, _et al._ , “Track any motions under any disturbances,” _arXiv preprint arXiv:2509.13833_ , 2025. 

- [86] W. Zeng, S. Lu, K. Yin, X. Niu, M. Dai, J. Wang, and J. Pang, “Behavior foundation model for humanoid robots,” _arXiv preprint arXiv:2509.13780_ , 2025. 

- [87] Z. Luo, Y. Yuan, T. Wang, C. Li, S. Chen, F. Casta˜neda, Z.-A. Cao, J. Li, D. Minor, Q. Ben, _et al._ , “Sonic: Supersizing motion tracking for natural humanoid whole-body control,” _arXiv preprint arXiv:2511.07820_ , 2025. 

- [88] D. Pathak, P. Agrawal, A. A. Efros, and T. Darrell, “Curiosity-driven exploration by self-supervised prediction,” in _International Conference on Machine Learning_ , pp. 2778–2787, PMLR, 2017. 

- [89] B. Eysenbach, A. Gupta, J. Ibarz, and S. Levine, “Diversity is all you need: Learning skills without a reward function,” in _International Conference on Learning Representations_ , 2019. 

- [90] Y. Burda, H. Edwards, A. Storkey, and O. Klimov, “Exploration by random network distillation,” in _International Conference on Learning Representations_ , 2019. 

- [91] H. Liu and P. Abbeel, “Aps: Active pretraining with successor features,” in _International Conference on Machine Learning_ , pp. 6736–6747, PMLR, 2021. 

- [92] D. Yarats, R. Fergus, A. Lazaric, and L. Pinto, “Reinforcement learning with prototypical representations,” in _International Conference on Machine Learning_ , pp. 11920–11931, PMLR, 2021. 

- [93] Y. Seo, L. Chen, J. Shin, H. Lee, P. Abbeel, and K. Lee, “State entropy maximization with random encoders for efficient exploration,” in _International Conference on Machine Learning_ , pp. 9443–9454, PMLR, 2021. 

- [94] J. Chen, V. Aggarwal, and T. Lan, “A unified algorithm framework for unsupervised discovery of skills based on determinantal point process,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 67925–67947, 2023. 

- [95] A. Touati and Y. Ollivier, “Learning one representation to optimize all rewards,” _Advances in Neural Information Processing Systems_ , vol. 34, pp. 13–23, 2021. 

- [96] Y. Li, Z. Luo, T. Zhang, C. Dai, A. Kanervisto, A. Tirinzoni, H. Weng, K. Kitani, M. Guzek, A. Touati, _et al._ , “Bfm-zero: A promptable behavioral foundation model for humanoid control using unsupervised reinforcement learning,” _arXiv preprint arXiv:2511.04131_ , 2025. 

- [97] L. Pan, Z. Yang, Z. Dou, W. Wang, B. Huang, B. Dai, T. Komura, and J. Wang, “Tokenhsi: Unified synthesis of physical human-scene interactions through task tokenization,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 5379–5391, 2025. 

- [98] Z. Xiao, T. Wang, J. Wang, J. Cao, W. Zhang, B. Dai, D. Lin, and J. Pang, “Unified human-scene interaction via prompted chainof-contacts,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [99] Y. Wu, K. Karunratanakul, Z. Luo, and S. Tang, “Uniphys: Unified planner and controller with diffusion for flexible physics-based character control,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 13214–13224, October 2025. 

- [100] G. Tevet, S. Raab, S. Cohan, D. Reda, Z. Luo, X. B. Peng, A. H. Bermano, and M. van de Panne, “Closd: Closing the loop between simulation and diffusion for multi-task character control,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [101] Y. Shao, X. Huang, B. Zhang, Q. Liao, Y. Gao, Y. Chi, Z. Li, S. Shao, and K. Sreenath, “Langwbc: Language-directed humanoid whole-body control via end-to-end learning,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [102] H. Xue, X. Huang, D. Niu, Q. Liao, T. Kragerud, J. T. Gravdahl, X. B. Peng, G. Shi, T. Darrell, K. Screenath, _et al._ , “Leverb: Humanoid 

   - whole-body control with latent vision-language instruction,” _arXiv preprint arXiv:2506.13751_ , 2025. 

- [103] Q. Liao, T. E. Truong, X. Huang, G. Tevet, K. Sreenath, and C. K. Liu, “Beyondmimic: From motion tracking to versatile humanoid control via guided diffusion,” _arXiv preprint arXiv:2508.08241_ , 2025. 

- [104] Y. Wang, H. Jiang, S. Yao, Z. Ding, and Z. Lu, “Sentinel: A fully end-to-end language-action model for humanoid whole body control,” _arXiv preprint arXiv:2511.19236_ , 2025. 

- [105] J. Merel, L. Hasenclever, A. Galashov, A. Ahuja, V. Pham, G. Wayne, Y. W. Teh, and N. Heess, “Neural probabilistic motor primitives for humanoid control,” in _International Conference on Learning Representations_ , 2019. 

- [106] D. Pathak, D. Gandhi, and A. Gupta, “Self-supervised exploration via disagreement,” in _International Conference on Machine Learning_ , pp. 5062–5071, PMLR, 2019. 

- [107] R. Sekar, O. Rybkin, K. Daniilidis, P. Abbeel, D. Hafner, and D. Pathak, “Planning to explore via self-supervised world models,” in _International Conference on Machine Learning_ , pp. 8583–8592, PMLR, 2020. 

- [108] K. Gregor, D. J. Rezende, and D. Wierstra, “Variational intrinsic control,” in _International Conference on Learning Representations_ , 2017. 

- [109] S. Hansen, W. Dabney, A. Barreto, D. Warde-Farley, T. Van de Wiele, and V. Mnih, “Fast task inference with variational intrinsic successor features,” in _International Conference on Learning Representations_ , 2020. 

- [110] M. Bellemare, S. Srinivasan, G. Ostrovski, T. Schaul, D. Saxton, and R. Munos, “Unifying count-based exploration and intrinsic motivation,” _Advances in Neural Information Processing Systems_ , vol. 29, 2016. 

- [111] G. Ostrovski, M. G. Bellemare, A. Oord, and R. Munos, “Count-based exploration with neural density models,” in _International Conference on Machine Learning_ , pp. 2721–2730, PMLR, 2017. 

- [112] M. Laskin, D. Yarats, H. Liu, K. Lee, A. Zhan, K. Lu, C. Cang, L. Pinto, and P. Abbeel, “Urlb: Unsupervised reinforcement learning benchmark,” in _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ . 

- [113] L. Blier, C. Tallec, and Y. Ollivier, “Learning successor states and goal-dependent values: A mathematical viewpoint,” _arXiv preprint arXiv:2101.07123_ , 2021. 

- [114] P. Dayan, “Improving generalization for temporal difference learning: The successor representation,” _Neural Computation_ , vol. 5, no. 4, pp. 613–624, 1993. 

- [115] T. D. Kulkarni, A. Saeedi, S. Gautam, and S. J. Gershman, “Deep successor reinforcement learning,” _arXiv preprint arXiv:1606.02396_ , 2016. 

- [116] Y. Tassa, Y. Doron, A. Muldal, T. Erez, Y. Li, D. d. L. Casas, D. Budden, A. Abdolmaleki, J. Merel, A. Lefrancq, _et al._ , “Deepmind control suite,” _arXiv preprint arXiv:1801.00690_ , 2018. 

- [117] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial nets,” in _Advances in Neural Information Processing Systems_ , vol. 27, Curran Associates, Inc., 2014. 

- [118] M. Janner, Y. Du, J. Tenenbaum, and S. Levine, “Planning with diffusion for flexible behavior synthesis,” in _International Conference on Machine Learning_ , pp. 9902–9915, PMLR, 2022. 

- [119] K. Gandhi, D. H. J. Lee, G. Grand, M. Liu, W. Cheng, A. Sharma, and N. Goodman, “Stream of search (sos): Learning to search in language,” in _First Conference on Language Modeling_ , 2024. 

- [120] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, _et al._ , “Training language models to follow instructions with human feedback,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 27730–27744, 2022. 

- [121] H. Naveed, A. U. Khan, S. Qiu, M. Saqib, S. Anwar, M. Usman, N. Akhtar, N. Barnes, and A. Mian, “A comprehensive overview of large language models,” _ACM Transactions on Intelligent Systems and Technology_ , vol. 16, no. 5, pp. 1–72, 2025. 

- [122] Y. Liu, K. Zhang, Y. Li, Z. Yan, C. Gao, R. Chen, Z. Yuan, Y. Huang, H. Sun, J. Gao, _et al._ , “Sora: A review on background, technology, limitations, and opportunities of large vision models,” _arXiv preprint arXiv:2402.17177_ , 2024. 

- [123] M. Awais, M. Naseer, S. Khan, R. M. Anwer, H. Cholakkal, M. Shah, M.-H. Yang, and F. S. Khan, “Foundation models defining a new era in vision: a survey and outlook,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [124] M. Kopel and T. Hajas, “Implementing ai for non-player characters in 3d video games,” in _Intelligent Information and Database Systems:_ 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

17 

   - _10th Asian Conference, ACIIDS 2018, Dong Hoi City, Vietnam, March 19-21, 2018, Proceedings, Part I 10_ , pp. 610–619, Springer, 2018. 

- [125] A. Mehta, Y. Kunjadiya, A. Kulkarni, and M. Nagar, “Exploring the viability of conversational ai for non-playable characters: A comprehensive survey,” in _2021 4th International Conference on Recent Trends in Computer Science and Technology (ICRTCST)_ , pp. 96–102, IEEE, 2022. 

- [126] M. C¸ . Uluda˘glı and K. O˘guz, “Non-player character decision-making in computer games,” _Artificial Intelligence Review_ , vol. 56, no. 12, pp. 14159–14191, 2023. 

- [127] X. Xu, Y. Lu, B. Vogel-Heuser, and L. Wang, “Industry 4.0 and industry 5.0—inception, conception and perception,” _Journal of Manufacturing Systems_ , vol. 61, pp. 530–535, 2021. 

- [128] J. Leng, W. Sha, B. Wang, P. Zheng, C. Zhuang, Q. Liu, T. Wuest, D. Mourtzis, and L. Wang, “Industry 5.0: Prospect and retrospect,” _Journal of Manufacturing Systems_ , vol. 65, pp. 279–295, 2022. 

- [129] S. Huang, B. Wang, X. Li, P. Zheng, D. Mourtzis, and L. Wang, “Industry 5.0 and society 5.0—comparison, complementation and coevolution,” _Journal of Manufacturing Systems_ , vol. 64, pp. 424–428, 2022. 

- [130] A. Akundi, D. Euresti, S. Luna, W. Ankobiah, A. Lopes, and I. Edinbarough, “State of industry 5.0—analysis and identification of current research trends,” _Applied System Innovation_ , vol. 5, no. 1, p. 27, 2022. 

- [131] M. A. Hassan, S. Zardari, M. U. Farooq, M. M. Alansari, and S. A. Nagro, “Systematic analysis of risks in industry 5.0 architecture,” _Applied Sciences_ , vol. 14, no. 4, p. 1466, 2024. 

- [132] A. Dzedzickis, J. Subaˇci¯ut˙e-Zemaitien˙e,<sup>ˇ</sup> E. Sutinys,<sup>ˇ</sup> U. Samukait˙eBubnien˙e, and V. Buˇcinskas, “Advanced applications of industrial robotics: New trends and possibilities,” _Applied Sciences_ , vol. 12, no. 1, p. 135, 2021. 

- [133] M. Bartoˇs, V. Bulej, M. Bohuˇs´ık, J. Stanˇcek, V. Ivanov, and P. Macek, “An overview of robot applications in automotive industry,” _Transportation Research Procedia_ , vol. 55, pp. 837–844, 2021. 

- [134] J. Arents and M. Greitans, “Smart industrial robot control trends, challenges and opportunities within manufacturing,” _Applied Sciences_ , vol. 12, no. 2, p. 937, 2022. 

- [135] M. Soori, R. Dastres, B. Arezoo, and F. K. G. Jough, “Intelligent robotic systems in industry 4.0: A review,” _Journal of Advanced Manufacturing Science and Technology_ , pp. 2024007–0, 2024. 

- [136] C.-C. Lee, S. Qin, and Y. Li, “Does industrial robot application promote green technology innovation in the manufacturing industry?,” _Technological Forecasting and Social Change_ , vol. 183, p. 121893, 2022. 

- [137] D. T. Rowland, “Global population aging: History and prospects,” in _International handbook of population aging_ , pp. 37–65, Springer, 2009. 

- [138] D. E. Bloom, D. Canning, and A. Lubet, “Global population aging: Facts, challenges, solutions & perspectives,” _Daedalus_ , vol. 144, no. 2, pp. 80–92, 2015. 

- [139] K. Navaneetham and D. Arunachalam, “Global population aging, 1950–2050,” in _Handbook of Aging, Health and Public Policy: Perspectives from Asia_ , pp. 1–18, Springer, 2023. 

- [140] P. Zhang, H. Yang, C. Chen, T. Wang, and X. Jia, “The impact of population aging on corporate digital transformation: Evidence from china,” _Technological Forecasting and Social Change_ , vol. 214, p. 124070, 2025. 

- [141] D. Feil-Seifer and M. J. Mataric, “Defining socially assistive robotics,” in _9th International Conference on Rehabilitation Robotics, 2005. ICORR 2005._ , pp. 465–468, IEEE, 2005. 

- [142] D. P. Miller, “Assistive robotics: an overview,” _Assistive Technology and Artificial Intelligence: Applications in Robotics, User Interfaces and Natural Language Processing_ , pp. 126–136, 2006. 

- [143] A. M. Okamura, M. J. Matari´c, and H. I. Christensen, “Medical and health-care robotics,” _IEEE Robotics & Automation Magazine_ , vol. 17, no. 3, pp. 26–37, 2010. 

- [144] L. D. Riek, “Healthcare robotics,” _Communications of the ACM_ , vol. 60, no. 11, pp. 68–78, 2017. 

- [145] J. Holland, L. Kingston, C. McCarthy, E. Armstrong, P. O’Dwyer, F. Merz, and M. McConnell, “Service robots in the healthcare sector,” _Robotics_ , vol. 10, no. 1, p. 47, 2021. 

- [146] M. Kyrarini, F. Lygerakis, A. Rajavenkatanarayanan, C. Sevastopoulos, H. R. Nambiappan, K. K. Chaitanya, A. R. Babu, J. Mathew, and F. Makedon, “A survey of robots in healthcare,” _Technologies_ , vol. 9, no. 1, p. 8, 2021. 

- [147] V. Sanchez, C. J. Walsh, and R. J. Wood, “Textile technology for soft robotic and autonomous garments,” _Advanced functional materials_ , vol. 31, no. 6, p. 2008278, 2021. 

- [148] F. Zhang and Y. Demiris, “Learning garment manipulation policies toward robot-assisted dressing,” _Science Robotics_ , vol. 7, no. 65, p. eabm6010, 2022. 

- [149] M. Javaid, A. Haleem, R. Pratap Singh, S. Rab, R. Suman, and L. Kumar, “Utilization of robotics for healthcare: a scoping review,” _Journal of Industrial Integration and Management_ , vol. 10, no. 01, pp. 43–65, 2025. 

- [150] M. Kaspar, J. D. M. Osorio, and J. Bock, “Sim2real transfer for reinforcement learning without dynamics randomization,” in _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 4383–4388, IEEE, 2020. 

- [151] D. Horv´ath, G. Erd˝os, Z. Istenes, T. Horv´ath, and S. F¨oldi, “Object detection using sim2real domain randomization for robotic applications,” _IEEE Transactions on Robotics_ , vol. 39, no. 2, pp. 1225–1243, 2022. 

- [152] J. Huber, F. H´el´enon, H. Watrelot, F. B. Amar, and S. Doncieux, “Domain randomization for sim2real transfer of automatically generated grasping datasets,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 4112–4118, IEEE, 2024. 

- [153] T. Yao, H. Wang, B. Lu, J. Ge, Z. Pei, M. Kowarschik, L. Sun, L. Seneviratne, and P. Qi, “Sim2real learning with domain randomization for autonomous guidewire navigation in robotic-assisted endovascular procedures,” _IEEE Transactions on Automation Science and Engineering_ , 2025. 

- [154] T. He, J. Gao, W. Xiao, Y. Zhang, Z. Wang, J. Wang, Z. Luo, G. He, N. Sobanbab, C. Pan, _et al._ , “Asap: Aligning simulation and real-world physics for learning agile humanoid whole-body skills,” in _Robotics: Science and Systems (RSS)_ , 2025. 

- [155] J. Hwangbo, I. Sa, R. Siegwart, and M. Hutter, “Control of a quadrotor with reinforcement learning,” _IEEE Robotics and Automation Letters_ , vol. 2, no. 4, pp. 2096–2103, 2017. 

- [156] A. Biddulph, T. Houliston, A. Mendes, and S. K. Chalup, “Comparing computing platforms for deep learning on a humanoid robot,” in _International Conference on Neural Information Processing_ , pp. 120– 131, Springer, 2018. 

- [157] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li, “Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction,” _arXiv preprint arXiv:2512.07464_ , 2025. 

- [158] M. B. Alatise and G. P. Hancke, “A review on challenges of autonomous mobile robot and sensor fusion methods,” _IEEE Access_ , vol. 8, pp. 39830–39846, 2020. 

- [159] T. Choudhary, V. Mishra, A. Goswami, and J. Sarangapani, “A comprehensive survey on model compression and acceleration,” _Artificial Intelligence Review_ , vol. 53, no. 7, pp. 5113–5155, 2020. 

- [160] V. C. Pujol and S. Dustdar, “Fog robotics—understanding the research challenges,” _IEEE Internet Computing_ , vol. 25, no. 5, pp. 10–17, 2021. 

- [161] M. Gleicher, “Retargetting motion to new characters,” in _Proceedings of the 25th Annual Conference on Computer Graphics and Interactive Techniques_ , pp. 33–42, 1998. 

- [162] M. Plappert, C. Mandery, and T. Asfour, “The kit motion-language dataset,” _arXiv preprint arXiv:1607.03827_ , 2016. 

- [163] N. Mahmood, N. Ghorbani, N. F. Troje, G. Pons-Moll, and M. J. Black, “Amass: Archive of motion capture as surface shapes,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 5442–5451, 2019. 

- [164] F. G. Harvey, M. Yurick, D. Nowrouzezahrai, and C. Pal, “Robust motion in-betweening,” _ACM Transactions on Graphics (TOG)_ , vol. 39, no. 4, pp. 60–1, 2020. 

- [165] A. R. Punnakkal, A. Chandrasekaran, N. Athanasiou, A. QuirosRamirez, and M. J. Black, “Babel: Bodies, action and behavior with english labels,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 722–731, 2021. 

- [166] G. Delmas, P. Weinzaepfel, T. Lucas, F. Moreno-Noguer, and G. Rogez, “Posescript: 3d human poses from natural language,” in _European Conference on Computer Vision_ , pp. 346–362, Springer, 2022. 

- [167] C. Guo, S. Zou, X. Zuo, S. Wang, W. Ji, X. Li, and L. Cheng, “Generating diverse and natural 3d human motions from text,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 5152–5161, June 2022. 

- [168] J. Lin, A. Zeng, S. Lu, Y. Cai, R. Zhang, H. Wang, and L. Zhang, “Motion-x: A large-scale 3d expressive whole-body human motion dataset,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 25268–25280, 2023. 

- [169] Y. Zhang, J. Lin, A. Zeng, G. Wu, S. Lu, Y. Fu, Y. Cai, R. Zhang, H. Wang, and L. Zhang, “Motion-x++: A large-scale multimodal 3d whole-body human motion dataset,” _arXiv preprint arXiv:2501.05098_ , 2025. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

18 

- [170] K. Lee, S. Kim, M. Park, H. Kim, D. Hwang, H. Lee, and J. Choo, “Phuma: Physically-grounded humanoid locomotion dataset,” _arXiv preprint arXiv:2510.26236_ , 2025. 

- [171] J. Mao, S. Zhao, S. Song, C. Hong, T. Shi, J. Ye, M. Zhang, H. Geng, J. Malik, V. Guizilini, _et al._ , “Universal humanoid robot pose learning from internet human videos,” in _2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids)_ , pp. 1–8, IEEE, 2025. 

- [172] T. He, Z. Luo, X. He, W. Xiao, C. Zhang, W. Zhang, K. M. Kitani, C. Liu, and G. Shi, “Omnih2o: Universal and dexterous humanto-humanoid whole-body teleoperation and learning,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [173] S. Liu, L. Wang, and X. Vincent Wang, “Multimodal data-driven robot control for human–robot collaborative assembly,” _Journal of Manufacturing Science and Engineering_ , vol. 144, no. 5, p. 051012, 2022. 

- [174] D. R. Yao, I. Kim, S. Yin, and W. Gao, “Multimodal soft robotic actuation and locomotion,” _Advanced Materials_ , vol. 36, no. 19, p. 2308829, 2024. 

- [175] T. Wang, P. Zheng, S. Li, and L. Wang, “Multimodal human–robot interaction for human-centric smart manufacturing: a survey,” _Advanced Intelligent Systems_ , vol. 6, no. 3, p. 2300359, 2024. 

- [176] Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang, “Hugginggpt: Solving ai tasks with chatgpt and its friends in hugging face,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 38154–38180, 2023. 

- [177] S.-C. Dai, A. Xiong, and L.-W. Ku, “LLM-in-the-loop: Leveraging large language model for thematic analysis,” in _The 2023 Conference on Empirical Methods in Natural Language Processing_ , 2023. 

- [178] C.-M. Chan, W. Chen, Y. Su, J. Yu, W. Xue, S. Zhang, J. Fu, and Z. Liu, “Chateval: Towards better LLM-based evaluators through multiagent debate,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [179] F. Liu, X. Wu, J. Huang, B. Yang, K. Branson, P. Schwab, L. Clifton, P. Zhang, J. Luo, Y. Zheng, _et al._ , “Aligning, autoencoding and prompting large language models for novel disease reporting,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [180] Z. Yu, X. Ouyang, Z. Shao, M. Wang, and J. Yu, “Prophet: Prompting large language models with complementary answer heuristics for knowledge-based visual question answering,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [181] H. Du, R. Zhang, D. Niyato, J. Kang, Z. Xiong, S. Cui, X. Shen, and D. I. Kim, “Reinforcement learning with llms interaction for distributed diffusion model services,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [182] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws for neural language models,” _arXiv preprint arXiv:2001.08361_ , 2020. 

- [183] A. Clark, D. de Las Casas, A. Guy, A. Mensch, M. Paganini, J. Hoffmann, B. Damoc, B. Hechtman, T. Cai, S. Borgeaud, _et al._ , “Unified scaling laws for routed language models,” in _International Conference on Machine Learning_ , pp. 4057–4086, PMLR, 2022. 

- [184] A. Aghajanyan, L. Yu, A. Conneau, W.-N. Hsu, K. Hambardzumyan, S. Zhang, S. Roller, N. Goyal, O. Levy, and L. Zettlemoyer, “Scaling laws for generative mixed-modal language models,” in _International Conference on Machine Learning_ , pp. 265–279, PMLR, 2023. 

- [185] B. Isik, N. Ponomareva, H. Hazimeh, D. Paparas, S. Vassilvitskii, and S. Koyejo, “Scaling laws for downstream task performance of large language models,” in _ICLR 2024 Workshop on Mathematical and Empirical Understanding of Foundation Models_ , 2024. 

- [186] H. Que, J. Liu, G. Zhang, C. Zhang, X. Qu, Y. Ma, F. Duan, Z. Bai, J. Wang, Y. Zhang, _et al._ , “D-cpt law: Domain-specific continual pretraining scaling law for large language models,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 90318–90354, 2024. 

- [187] K. Kumar, T. Ashraf, O. Thawakar, R. M. Anwer, H. Cholakkal, M. Shah, M.-H. Yang, P. H. Torr, F. S. Khan, and S. Khan, “Llm posttraining: A deep dive into reasoning large language models,” _arXiv preprint arXiv:2502.21321_ , 2025. 

- [188] S. Yue, W. Chen, S. Wang, B. Li, C. Shen, S. Liu, Y. Zhou, Y. Xiao, S. Yun, X. Huang, _et al._ , “Disc-lawllm: Fine-tuning large language models for intelligent legal services,” _arXiv preprint arXiv:2309.11325_ , 2023. 

- [189] Y. Chen, S. Qian, H. Tang, X. Lai, Z. Liu, S. Han, and J. Jia, “Longlora: Efficient fine-tuning of long-context large language models,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [190] L. Trung, X. Zhang, Z. Jie, P. Sun, X. Jin, and H. Li, “Reft: Reasoning with reinforced fine-tuning,” in _Proceedings of the 62nd Annual Meet-_ 

_ing of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pp. 7601–7614, 2024. 

- [191] N. Ding, Y. Qin, G. Yang, F. Wei, Z. Yang, Y. Su, S. Hu, Y. Chen, C.-M. Chan, W. Chen, _et al._ , “Parameter-efficient fine-tuning of large-scale pre-trained language models,” _Nature Machine Intelligence_ , vol. 5, no. 3, pp. 220–235, 2023. 

- [192] S. Malladi, T. Gao, E. Nichani, A. Damian, J. D. Lee, D. Chen, and S. Arora, “Fine-tuning language models with just forward passes,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 53038– 53075, 2023. 

- [193] L. Xu, H. Xie, S.-Z. J. Qin, X. Tao, and F. L. Wang, “Parameterefficient fine-tuning methods for pretrained language models: A critical review and assessment,” _arXiv preprint arXiv:2312.12148_ , 2023. 

- [194] M.-H. Guo, Y. Zhang, T.-J. Mu, S. X. Huang, and S.-M. Hu, “Tuning vision-language models with multiple prototypes clustering,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [195] H. Yuan, Z. Yuan, C. Tan, W. Wang, S. Huang, and F. Huang, “Rrhf: Rank responses to align language models with human feedback,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 10935– 10950, 2023. 

- [196] C. Y. Liu, L. Zeng, J. Liu, R. Yan, J. He, C. Wang, S. Yan, Y. Liu, and Y. Zhou, “Skywork-reward: Bag of tricks for reward modeling in llms,” _arXiv preprint arXiv:2410.18451_ , 2024. 

- [197] H. Dong, W. Xiong, B. Pang, H. Wang, H. Zhao, Y. Zhou, N. Jiang, D. Sahoo, C. Xiong, and T. Zhang, “Rlhf workflow: From reward modeling to online rlhf,” _Transactions on Machine Learning Research_ , 2024. 

- [198] G. Cui, L. Yuan, N. Ding, G. Yao, W. Zhu, Y. Ni, G. Xie, Z. Liu, and M. Sun, “Ultrafeedback: Boosting language models with high-quality feedback,” 2023. 

- [199] Y. Du, O. Watkins, Z. Wang, C. Colas, T. Darrell, P. Abbeel, A. Gupta, and J. Andreas, “Guiding pretraining in reinforcement learning with large language models,” in _International Conference on Machine Learning_ , pp. 8657–8677, PMLR, 2023. 

- [200] J. Song, Z. Zhou, J. Liu, C. Fang, Z. Shu, and L. Ma, “Self-refined large language model as automated reward function designer for deep reinforcement learning in robotics,” _arXiv preprint arXiv:2309.06687_ , 2023. 

- [201] Z. Xu, F. Jiang, L. Niu, Y. Deng, R. Poovendran, Y. Choi, and B. Y. Lin, “Magpie: Alignment data synthesis from scratch by prompting aligned LLMs with nothing,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [202] J. Jiang, D. He, and J. Allan, “Searching, browsing, and clicking in a search session: changes in user behavior by task and over time,” in _Proceedings of the 37th international ACM SIGIR Conference on Research & Development in Information Retrieval_ , pp. 607–616, 2014. 

- [203] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan, “Tree of thoughts: Deliberate problem solving with large language models,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 11809–11822, 2023. 

- [204] Y. Tian, B. Peng, L. Song, L. Jin, D. Yu, L. Han, H. Mi, and D. Yu, “Toward self-improvement of llms via imagination, searching, and criticizing,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 52723–52748, 2024. 

- [205] T. Arai, E. Pagello, L. E. Parker, _et al._ , “Advances in multi-robot systems,” _IEEE Transactions on Robotics and Automation_ , vol. 18, no. 5, pp. 655–661, 2002. 

- [206] A. Gautam and S. Mohan, “A review of research in multi-robot systems,” in _2012 IEEE 7th International Conference on Industrial and Information Systems (ICIIS)_ , pp. 1–5, IEEE, 2012. 

- [207] A. Dorri, S. S. Kanhere, and R. Jurdak, “Multi-agent systems: A survey,” _Ieee Access_ , vol. 6, pp. 28573–28593, 2018. 

- [208] ´A. Madridano, A. Al-Kaff, D. Mart´ın, and A. De La Escalera, “Trajectory planning for multi-robot systems: Methods and applications,” _Expert Systems with Applications_ , vol. 173, p. 114660, 2021. 

- [209] Z. Zhou, J. Liu, and J. Yu, “A survey of underwater multi-robot systems,” _IEEE/CAA Journal of Automatica Sinica_ , vol. 9, no. 1, pp. 1– 18, 2021. 

- [210] C. Ju, J. Kim, J. Seol, and H. I. Son, “A review on multirobot systems in agriculture,” _Computers and Electronics in Agriculture_ , vol. 202, p. 107336, 2022. 

- [211] D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman, “Gpqa: A graduate-level google-proof q&a benchmark,” in _First Conference on Language Modeling_ , 2024. 

- [212] D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt, “Measuring mathematical problem solving 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE 

19 

with the math dataset,” in _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ . 

- [213] Z. R. Sprague, X. Ye, K. Bostrom, S. Chaudhuri, and G. Durrett, “Musr: Testing the limits of chain-of-thought with multistep soft reasoning,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [214] P. Xu, W. Shao, K. Zhang, P. Gao, S. Liu, M. Lei, F. Meng, S. Huang, Y. Qiao, and P. Luo, “Lvlm-ehub: A comprehensive evaluation benchmark for large vision-language models,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024. 

- [215] Z. Huang, S. Zhong, P. Zhou, S. Gao, M. Zitnik, and L. Lin, “A causality-aware paradigm for evaluating creativity of multimodal large language models,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2025. 

- [216] L. Weidinger, J. Mellor, M. Rauh, C. Griffin, J. Uesato, P.-S. Huang, M. Cheng, M. Glaese, B. Balle, A. Kasirzadeh, _et al._ , “Ethical and social risks of harm from language models,” _arXiv preprint arXiv:2112.04359_ , 2021. 

- [217] L. Yan, L. Sha, L. Zhao, Y. Li, R. Martinez-Maldonado, G. Chen, X. Li, Y. Jin, and D. Gaˇsevi´c, “Practical and ethical challenges of large language models in education: A systematic scoping review,” _British Journal of Educational Technology_ , vol. 55, no. 1, pp. 90–112, 2024. 

- [218] R. Bommasani, S. Kapoor, K. Klyman, S. Longpre, A. Ramaswami, D. Zhang, M. Schaake, D. E. Ho, A. Narayanan, and P. Liang, “Considerations for governing open foundation models,” _Science_ , vol. 386, no. 6718, pp. 151–153, 2024. 

- [219] M. Vasic and A. Billard, “Safety issues in human-robot interactions,” in _2013 IEEE International Conference on Robotics and Automation_ , pp. 197–204, IEEE, 2013. 

- [220] P. A. Lasota, T. Fong, J. A. Shah, _et al._ , “A survey of methods for safe human-robot interaction,” _Foundations and Trends in Robotics_ , vol. 5, no. 4, pp. 261–349, 2017. 

- [221] I. Kumagai, M. Morisawa, T. Sakaguchi, S. Nakaoka, K. Kaneko, H. Kaminaga, S. Kajita, M. Benallegue, R. Cisneros, and F. Kanehiro, “Toward industrialization of humanoid robots: Autonomous plasterboard installation to improve safety and efficiency,” _IEEE Robotics & Automation Magazine_ , vol. 26, no. 4, pp. 20–29, 2019. 

- [222] G. Goh, N. Cammarata, C. Voss, S. Carter, M. Petrov, L. Schubert, A. Radford, and C. Olah, “Multimodal neurons in artificial neural networks,” _Distill_ , vol. 6, no. 3, p. e30, 2021. 

