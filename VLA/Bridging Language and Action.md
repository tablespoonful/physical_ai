---
title: "Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation"
date: "2023-12-17"
authors: "Xiangtong Yao; Hongkuan Zhou; Oier Mees; Yuan Meng; Ted Xiao; Yonatan Bisk"
url: https://arxiv.org/abs/2312.10807
pdf: https://arxiv.org/pdf/2312.10807
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2312.10807)** / [論文ページ](https://arxiv.org/abs/2312.10807)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation** 

<u>Journal Title</u> XX(X):1–70 ©The Author(s) 2024 Reprints and permission: sagepub.co.uk/journalsPermissions.nav DOI: 10.1177/ToBeAssigned www.sagepub.com/ 

<u>SAGE</u> 

**Xiangtong Yao**<sup>**1**</sup> ***, Hongkuan Zhou**<sup>**2,12**</sup> ***, Oier Mees**<sup>**3,4**</sup> ***, Yuan Meng**<sup>**1**</sup> ***, Ted Xiao**<sup>**5**</sup> **, Yonatan Bisk**<sup>**6**</sup> **, Jean Oh**<sup>**6**</sup> **, Edward Johns**<sup>**7**</sup> **, Mohit Shridhar**<sup>**5**</sup> **, Dhruv Shah**<sup>**5,8**</sup> **, Jesse Thomason**<sup>**9**</sup> **, Kai Huang**<sup>**10**</sup> **, Joyce Chai**<sup>**11**</sup> **, Zhenshan Bing**<sup>**1,13**</sup> **, Alois Knoll**<sup>**1**</sup> 

### **Abstract** 

Language-conditioned robot manipulation is an emerging field aimed at enabling seamless communication and cooperation between humans and robotic agents by teaching robots to comprehend and execute instructions conveyed in natural language. This interdisciplinary area integrates scene understanding, language processing, and policy learning to bridge the gap between human instructions and robot actions. In this comprehensive survey, we systematically explore recent advancements in language-conditioned robot manipulation. We categorize existing methods based on the primary ways language is integrated into the robot system, namely language for state evaluation, language as a policy condition, language for cognitive planning and reasoning, and language in unified vision-languageaction models. Specifically, we further analyze state-of-the-art techniques from five axes of action granularity, data and supervision regimes, system cost and latency, environments and evaluations, and task specification. Additionally, we highlight the key debates in the field. Finally, we discuss open challenges and future research directions, focusing on potentially enhancing generalization capabilities and addressing safety issues in language-conditioned robot manipulators. 

### **Keywords** 

language-conditioned learning, robot manipulation, diffusion models, large language models, vision language models, vision-language-action models, neuro-symbolic models, and foundation models. 

# **1 Introduction** 

Robot manipulation, the ability of robots to physically interact with and manipulate objects in their environment (Billard and Kragic 2019), is an important component of autonomous systems. It has been widely adopted in structured environments, such as factory floors (Sanchez et al. 2018), where robots perform repetitive tasks with high precision and efficiency. One vision of robotics is to integrate intelligent systems into the fabric of everyday life, moving them from the environment with controlled settings to unstructured scenarios in homes, hospitals, and warehouses, where high levels of interaction between humans and robots are required (SilveraTawil 2024; Zhang and Xue 2025). A fundamental barrier, however, has long hindered this vision: the complexity of instructing robots in unstructured environments, particularly for non-expert users. Traditional methods for instructing robots are non-generalizable, such as specialized programming of control rules (Takeshita et al. 2025), teleoperation (Wu et al. 2019), or reward functions engineering (Ibarz et al. 2021). These methods demand expert efforts, which are inaccessible to the general public without extensive training. This limitation has impeded the broader deployment of general-purpose robots. 

voice lowers the barrier for non-expert users and unlocks the potential for robots to function as general-purpose assistants, making robotics more accessible to a broader audience and increasing its importance. This motivation is shared by a broader family of intuitive task-specification paradigms. Image- and video-conditioned manipulation methods, for instance, aim to reduce the burden of robot instruction by enabling users to specify tasks through target visual states, 

- 1 Technical University of Munich, Munich, Germany 

> 2 Corporate Research, Robert Bosch GmbH, Renningen, Germany 

- 3 University of California Berkeley, USA 

- 4 Microsoft, Switzerland 

- 5 Google DeepMind, USA & UK 

- 6 Carnegie Mellon University, USA 

- 7 Imperial College London, UK 

- 8 Princeton University, USA 

- 9 University of Southern California, USA 

- 10 Sun Yat-sen University, Guangzhou, China 

- 11 University of Michigan, USA 

> 12 Institute for Artificial Intelligence, University of Stuttgart, Stuttgart, Germany 

> 13 The State Key Laboratory for Novel Software Technology, Nanjing University, Suzhou, China 

- Equal contribution 

Language-conditioned robotic manipulation is emerging as a transformative solution to this challenge. It leverages natural language as an intuitive interface for humans to specify tasks, enabling robots to translate these high-level commands into physical actions. Enabling control via simple text or 

This version is accepted by _The International Journal of Robotics Research_ (IJRR). 

#### **Corresponding author:** 

Zhenshan Bing 

Email: zhenshan.bing@tum.de, bing@nju.edu.cn 

_Prepared using sagej.cls [Version: 2017/01/17 v1.20]_ 

_Journal Title XX(X)_ 

2 

demonstrations, or perceptual references instead of low-level programming. However, different conditioning modalities provide different forms of task information. 

Image-conditioned methods are well-suited for specifying desired object configurations or goal states (Alakuijala et al. 2023; Wang et al. 2023b), while video-conditioned methods convey motion patterns, temporal evolution, and demonstration trajectories (Yang et al. 2023; Eze and Crick 2025). Compared with these visual modalities, language provides a more compact and editable interface for expressing abstract task intent, relational constraints, safety requirements, preferences, and corrections. Beyond external task specification, language can also serve as an internal cognitive medium for robot reasoning, enabling systems to decompose long-horizon tasks into subgoals, reason about affordances and causality, and generate plans or executable code. Therefore, while language-, image-, and videoconditioned manipulation are complementary paradigms for intuitive robot instruction. The broader functional role of language motivates a dedicated survey on how it is grounded in perception, planning, and control. The advantages of language conditioning can be summarized as follows. 

- **Accessibility and usability** : Language conditioning allows people who are not experts to use robots. As noted by Tellex et al. (2020): “ _most future robot users will not be programmers_ ”. Natural language provides a “zero-learning” interface that allows anyone to specify complex and high-level goals without needing to understand the underlying code or control logic. Instead of navigating complex graphical user interfaces (GUIs) or writing scripts, a user can simply state their intent, such as “ _bring me the red cup from the kitchen counter_ ”, lowering the barrier to entry for a wide range of applications. 

- **Trust through bidirectional communication:** Trust is essential for human-robot collaboration, especially in sensitive environments, such as assistive care (Jenamani et al. 2025). Language-conditioned systems offer a natural pathway to building that trust. The same channel used to command a robot can be used for on-the-fly correction and explanation. A user asks, “ _I have a trach and have to eat slowly_ ” (Jenamani et al. 2025), and the robot can provide a rationale for its actions. These transparent feedback loops enable more intuitive and safer interactions, a key theme in humanrobot interaction research focused on closing the loop between robot learning and communication (Habibian et al. 2025). 

- **Transferring textual knowledge to robotics:** Realworld environments like homes and factories are unpredictable, with many unique situations that preprogrammed robots cannot handle. Language provides a compact interface for importing the world’s common sense knowledge, such as properties, procedures, and safety rules, into the control system. By grounding natural-language commands to perception and action primitives, a system can parse goals like “ _stack the two lightest boxes_ ” into perceptual queries, relational reasoning, and sequences of controllable skills. Leveraging broad linguistic priors reduces per-task 

engineering and enables zero/few-shot generalization to unseen tasks (Zitkovich et al. 2023; Zhang et al. 2025b), improving robustness when operating in dynamic environments. 


**Figure 1.** Language-conditioned manipulation sits at the intersection of computer vision, natural language processing, and robotics. Scene understanding, language understanding/grounding, policy learning/design, and action execution are widely studied in this realm. This field leverages a variety of techniques, such as Vision-Language Models, Large Language Models, Vision-Language-Action Models, Imitation Learning, Reinforcement Learning, or Planning, to achieve behavior. 

Driven by these advantages, recent research goals in the emerging field of language-conditioned robot manipulation aim to enable natural language commands, instructions, and queries to robot systems that are translated into motor actions and behaviors conditioned on visual observations of the physical environment. Remarkable success has been seen in robotic arm control (Knoll et al. 1997; Zhang et al. 1999; Lynch and Sermanet 2021; Silva et al. 2021; Mees et al. 2022a; O’Neill et al. 2024; Bing et al. 2023a; Octo Model Team et al. 2024) ,cross-embodiment learning (Yang et al. 2024b; Doshi et al. 2025), and robot navigation tasks (Hermann et al. 2017; Fu et al. 2019; Hirose et al. 2025) such as autonomous driving (Sriram et al. 2019; Roh et al. 2020). Figure 1 demonstrates fundamental disciplines and research in language-conditioned robot manipulation. Success in this field requires tackling challenges across three key axes: language understanding, visual perception, and action generation. From a system perspective, it is useful to factor a language-conditioned manipulation pipeline into three interacting modules: Language, Perception, and Control. This decomposition is architectural rather than conventional robotics taxonomy: here, the language module includes instruction understanding, task representation, and often high-level semantic planning/reasoning; the perception module grounds language in observations and estimates the environment state; and the control module converts the resulting task specification into executable robot actions through learned policies or classical planners/controllers, as shown in Figure 2. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

3 


**Figure 2.** This architectural framework provides a high-level overview of language-conditioned robot manipulation. The agent comprises three key modules: the language module, the perception module, and the control module. These modules serve the functions of understanding instructions, perceiving the environment’s state, and acquiring skills, respectively. The vision-language module establishes connections between instructions and the surrounding environment to achieve a deeper understanding of both aspects. The control module can acquire low-level policies by learning from rewards (reinforcement learning) and demonstrations (imitation learning), both engineered by experts. At times, these low-level policies can also be directly designed or hard-coded, making use of path and motion planning algorithms. There are two key loops to highlight. The interactive loop, located on the left, facilitates human-robot language interaction. The control loop, positioned on the right, signifies the interaction between the agent and its surrounding environment. This paper focuses on the role language plays in the system, namely ➊ language for state evaluation (language _→_ perception), ➋ language as a policy condition (language _→_ control), and ➌ language for cognitive planning and reasoning (among language). ➍ Language in unified vision-language-action models (unify all the modules) 

To extract semantics from natural language, early research works (Kress-Gazit et al. 2009; Raman et al. 2012) leverage formal specification languages such as temporal logic, which support formal verification of provided commands. Nevertheless, specifying instructions in these languages can be challenging, complex, and time-consuming. Large-scale pretraining approaches in natural language processing have led to text embedding models, like GloVe (Pennington et al. 2014), RoBERTa (Liu et al. 2019), and BERT (Devlin et al. 2019). In particular, large language models (LLMs) have shown impressive abilities in extracting semantic information and performing high-level planning and reasoning tasks. 

To ground language commands in the physical scene, robots must perceive their environments, a challenge addressed by advances in computer vision. Foundational technologies include convolutional neural networks (e.g., ResNet (He et al. 2016)) for feature extraction, object detectors (e.g., Faster-RCNN (Girshick 2015), YOLO (Redmon et al. 2016)), and more recent transformer-based architectures like Vision Transformers (ViT) (Dosovitskiy et al. 2021). To connect visual perception with linguistic instructions, vision-language models (VLMs) such as CLIP (Radford et al. 2021) and Flamingo (Alayrac et al. 2022) have been developed. These models learn joint embeddings that align 

visual and textual data, enabling robots to perform tasks like language-conditioned object detection (Zang et al. 2025) and segmentation (Li et al. 2022), which are critical for identifying and localizing objects mentioned in a command. 

To translate high-level linguistic goals into low-level robot actions, researchers explore several paradigms. One major approach is to learn a language-conditioned policy using methods like reinforcement learning (RL) (Sutton et al. 1998) or imitation learning (IL) (Argall et al. 2009). In this paradigm, the language command is provided as an input to the policy, which then directly outputs low-level actions (e.g., joint torques or end-effector velocities). For instance, in language-conditioned IL, the model learns to map from images and text commands to expert actions from a dataset of language-annotated demonstrations. A second popular approach decouples high-level reasoning from low-level control. In these methods, a large language model or visionlanguage model is used to parse the instruction and predict an intermediate goal, such as a target end-effector pose or a grasp point. This high-level prediction is then passed to a classical motion planner that uses inverse kinematics to compute the required joint movements (Habekost et al. 2024; Yang et al. 2025h). This modular design leverages the strong open-vocabulary and instruction-following priors 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

4 

of foundation models (FMs) for goal specification while relying on robust non-learning-based controllers for precise manipulation (Yang et al. 2025h). 

While this “Language-Perception-Control” framework provides a useful high-level overview, a deeper analysis reveals that the central research questions are not just about these components, but about the _specific functional role language plays in bridging them_ . Different approaches leverage language in fundamentally distinct ways to solve the manipulation problem. This survey will focus on this perspective, categorizing recent methods based on how language enters the manipulation control loop. 

# _1.1 Contributions_ 

**A New Taxonomy and Comprehensive Review:** We introduce a new taxonomy that organizes the field by the functional role language plays in the manipulation control loop. This taxonomy categorizes methods into four primary themes: language for state evaluation (using language to define goals and assess task-relevant states for high-level planning, such as task decomposition and subgoal sequencing, or for learning, such as reward design, value estimation, and policy optimization), language as a direct policy condition (using language to specify desired behavior), language for cognitive planning and reasoning, and language-driven end-to-end policy (visionlanguage-action models). Based on this framework, we provide a comprehensive review of state-of-the-art methods, from traditional language-conditioned policies to the latest approaches driven by FMs, including LLMs, VLMs, VLAs, and neuro-symbolic integrations. This structured review highlights how different methods leverage language to bridge perception (grounding language in sensory observations and extracting task-relevant state information), planning/reasoning (inferring task structure, constraints, and subgoals), and control (generating executable actions or policy outputs). Moreover, to provide a multifaceted understanding, we conduct a systematic comparative analysis from an orthogonal perspective. We evaluate the surveyed methods across several key dimensions: action granularity, data and supervision requirements, system cost and latency, the environments and benchmarks used for validation, and cross-modal task specification. This analysis offers practical insights into the trade-offs and applicability of different approaches. 

**Discussion and Future Directions:** Additionally, we delve into the key debates, such as whether scaling up VLA models is the most effective path forward compared to incorporating structured world models or other hybrid approaches. We also discuss open challenges currently shaping the field. Building on this discussion, we outline the primary limitations and future directions, focusing on two critical areas: enhancing generalization capability and ensuring real-world safety. To improve generalization, we propose focusing on the development of large-scale, diverse datasets, integrating lifelong learning frameworks to enable continuous adaptation, and establishing methods for crossembodiment alignment. To address safety, we highlight the need for mechanisms to handle language ambiguity, improve 

failure recovery, and guarantee the real-time performance required for unstructured environments. 

# _1.2 Relation to existing surveys_ 

Before the emergence of LLMs, Tellex et al. (2020) provided a foundational review of language grounding in robotics, categorizing approaches by their technical underpinnings (e.g., “lexically grounded” vs. “learning methods”). Recent surveys, prompted by the rise of FMs, have offered broad perspectives. Surveys by Hu et al. (2023); Li et al. (2024a); Xiao et al. (2025) discuss the application of FMs in robotics, organizing their findings by model type and the specific robotic module they enhance, such as perception and planning. Similarly, Firoozi et al. (2025) structures its analysis around general robotics capabilities like “Perception”, “Decision-making”, and “Control”. 

While these surveys provide essential overviews, our work offers a distinct and orthogonal perspective. Rather than categorizing by model type or the robotic module it replaces, our survey organizes the field by the functional role language plays within the manipulation control loop. This taxonomy allows for a finer-grained analysis that spans multiple models and algorithms. We categorize approaches into four types: language for state evaluation, language as a policy condition, language for cognitive planning and reasoning, and language in unified vision-language-action models (VLAs). This taxonomy allows us to systematically cover a wide range of techniques, including language-conditioned policy learning/planning, neuro-symbolic methods, and emerging paradigms based on LLMs, VLMs, and VLAs. By focusing on the role of language, our survey provides a new perspective for understanding the diverse ways we can bridge language and action in robotic manipulation. 

# _1.3 Organization_ 

The rest of this paper is organized as follows. Section 2 presents foundational concepts relevant to languageconditioned robot manipulation. In Section 3, we elaborate on the taxonomy of the recent approaches that they can be categorized into _language for state evaluation_ (Section 4), _language as policy condition_ (Section 5), _language for cognitive planning and reasoning_ (Section 6), and _Language in unified vision-language-action models_ (Section 7). Additionally, in Section 8, we conduct a comprehensive comparative analysis of various approaches from a different perspective, focusing on the dimensions of _action granularity_ , _data and supervision regime_ , _system cost and latency_ , _environment and evaluation_ , as well as _manipulation task spectrum_ . Finally, we present the key debates in this field in Section 9, outline the challenges and future directions in Section 10, and provide conclusions in Section 11. 

# **2 Background** 

We present fundamental terms and concepts in this section. An understanding of these principles is crucial, as they serve as the cornerstone for the more advanced methods discussed throughout this article. Table 1 provides an overview of important abbreviations used in this article. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

5 

**Table 1.** Abbreviations 

|Abbreviations|Meaning|
|---|---|
|MDP|Markov Decision Process|
|IL|Imitation Learning|
|RL|Reinforcement Learning|
|BC|Behavior Cloning|
|IRL|Inverse Reinforcement Learning|
|GCIL|Goal-conditioned Imitation Learning|
|KB|Knowledge Base|
|KG|Knowledge Graph|
|KGE|Knowledge Graph Embedding|
|PDDL|Planning Domain Definition Language|
|NLMs|Neural Language Models|
|PLMs|Pre-trained Language Models|
|LLMs|Large Language Models|
|VLMs|Vision-Language Models|
|VLAs|Vision-Language-Action Models|
|FMs|Foundation Models|


# _2.1 Markov decision process_ 

A Markov decision process (MDP) is a discrete-time stochastic control model for sequential decision making under uncertainty (Sutton and Barto 1998). Formally, an MDP is a tuple _M_ = ( _S, A, P, R, γ_ ), where _S_ is the state space and _A_ is the action space. _P_ : _S × A × S →_ [0 _,_ 1] is the transition probability, where _P_ ( _s_<sup>_′_</sup> _| s, a_ ) = Pr _{St_ +1 = _s_<sup>_′_</sup> _| St_ = _s, At_ = _a}_ . The reward function _R_ : _S × A →_ R gives the expected immediate reward _R_ ( _s, a_ ) = E[ _Rt_ +1 _| St_ = _s, At_ = _a_ ]. The discount factor _γ ∈_ [0 _,_ 1] encodes the trade-off between near-term and long-term rewards and, in continuing tasks, ensures that the (potentially infinitehorizon) return<sup>�</sup><sup>_∞_</sup> _t_ =0<sup>_γtRt_+1 is finite.</sup> 

# _2.2 Reinforcement learning_ 

RL (Sutton and Barto 1998) studies how an agent interacts with an environment modeled as an MDP to learn a policy that maximizes expected return _when the environment’s dynamics are not available to the agent_ . Concretely, the transition probability _P_ and reward function _R_ are typically _unknown_ in RL and the agent must improve its behavior from trial-and-error experience. A (stochastic) policy is a mapping _π_ : _S →A_ with _π_ ( _a | s_ ) denoting the probability of taking action _a_ in state _s_ . 

The goal of RL is to select a policy _π_<sup>_∗_</sup> which maximizes expected return _J_ ( _π_ ) when the agent acts according to it. The expected return can be written as 


The central optimization problem in RL can be expressed by 


with _π_<sup>_∗_</sup> being the optimal policy. RL algorithms typically define value functions 


and action-value functions 


to guide the search for an optimal policy. 

# _2.3 Imitation learning_ 

Imitation Learning (IL) aims to learn a policy _π_ by mimicking expert demonstrations, which are sequences of state-action pairs _τ_ = _{s_ 0 _, a_ 0 _, s_ 1 _, a_ 1 _, . . . }_ , without relying on explicit reward signals. The main IL methodologies include behavioral cloning (BC), goal-conditioned imitation learning (GCIL), and inverse reinforcement learning (IRL). 

### _2.3.1 Behavioral cloning_ 

In BC (Bain and Sammut 1995), the trajectory executed by expert agents is treated as the reference or ground truth trajectory. Through supervised learning, an imitation policy is acquired by minimizing the disparity between the anticipated actions and the actual actions observed in the ground-truth trajectory. Considering a set of trajectories are collected from experts _τ ∈T_ , the optimization problem can be defined as: 


where _L_ is the cost function, _π_<sup>_∗_</sup> ( _s_ ) and _π_ ( _s_ ) are the expert’s and predicted actions at the state _s_ , respectively. 

### _2.3.2 Goal-conditioned imitation learning_ 

GCIL extends standard imitation learning by conditioning the policy not only on the state but also on a desired goal, enabling agents to generalize across multiple tasks and achieve diverse outcomes from demonstrations (Ding et al. 2019). This extension is essential in robotics, where demonstrations often target different configurations, and a goal-conditioned policy _πθ_ ( _a|s, g_ ) can leverage these demonstrations to reach any goal _g ∈S_ . In the goal-conditioned setting, the reward function is defined as an indicator of goal achievement, _r_ ( _st, at, st_ +1 _, g_ ) = 1 [ _st_ +1 == _g_ ], meaning that the agent succeeds if its next state matches the goal. To learn from demonstrations without explicitly engineering rewards, the most direct approach is goal-conditioned behavioral cloning (Ding et al. 2019), which minimizes the error between the expert’s action _a_<sup>_j_</sup> _t_ and the agent’s predicted action _πθ_ ( _s_<sup>_j_</sup> _t_<sup>_, gj_)givenstate–goal</sup> pairs. Here, We assume access to _D_ expert demonstration trajectories _{_ ( _s_<sup>_j_</sup> 0<sup>_, aj_</sup> 0<sup>_, s_</sup> 1<sup>_j, . . ._)</sup><sup>_}D_</sup> _j_ =1<sup>_∼τ_expert,eachproduced</sup> by an expert policy pursuing a goal _g_<sup>_j_</sup> , with _{g_<sup>_j_</sup> _}_<sup>_D_</sup> _j_ =1 uniformly sampled from the feasible goal space (Ding et al. 2019). The supervised loss is: 


This formulation directly adapts standard BC to the goalconditioned case by embedding goals into the input space of the policy. Beyond simple cloning, GCIL leverages the insight that trajectories labeled with a particular goal _g_<sup>_j_</sup> can also serve as valid demonstrations for any intermediate state along the trajectory, effectively enabling goal relabeling. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

6 

For example, a transition tuple ( _s_<sup>_j_</sup> _t_<sup>_, aj_</sup> _t_<sup>_, sj_</sup> _t_ +1<sup>_, gj_)</sup> can equivalently be relabeled as ( _s_<sup>_j_</sup> _t_<sup>_, a_</sup> _t_<sup>_j, sj_</sup> _t_ +1<sup>_, g′_=</sup><sup>_sj_</sup> _t_ + _k_<sup>)since</sup> reaching _s_<sup>_j_</sup> _t_ + _k_ is also a valid goal achieved by the expert. This relabeling principle, analogous to hindsight experience replay (HER) (Andrychowicz et al. 2017) in RL, substantially improves sample efficiency and generalization in sparse reward settings. 

### _2.3.3 Inverse reinforcement learning_ 

An alternative to direct BC in IL is to reason about and recover the hidden reward function that drives expert behavior. This approach, known as IRL (Arora and Doshi 2021), seeks to infer a reward function _R_ ( _s, a_ ) from demonstrations rather than directly copying actions, thereby capturing the intent behind behavior and enabling agents to generalize or even surpass the expert. Formally, given demonstrations represented as trajectories _τ_ = _{_ ( _s_ 0 _, a_ 0) _,_ ( _s_ 1 _, a_ 1) _, . . . }_ , the objective of IRL is to find a reward function under which the expert’s policy is (approximately) optimal: 


To address the ill-posed nature of IRL, two representative techniques are widely used. Apprenticeship Learning (Abbeel and Ng 2004) avoids recovering a unique reward and instead matches the expert’s and learner’s feature expectations. Assuming a linear reward form _R_ ( _s, a_ ) = _w_<sup>_⊤_</sup> _ϕ_ ( _s, a_ ), where _w_ is a weight vector and _ϕ_ ( _s, a_ ) is a feature representation of state–action pairs, it seeks a policy _π_ such that 


In contrast, Maximum Entropy IRL (Ziebart et al. 2008) resolves ambiguity by modeling expert demonstrations as samples from a maximum entropy trajectory distribution 


where _Z_ is a normalization term. These two approaches capture the main routes in IRL: feature-matching to approximate expert performance and probabilistic modeling to handle reward uncertainty, both of which extend imitation learning beyond BC. 

Here, _µθ_ ( _xt, t_ ) and Σ _θ_ ( _xt, t_ ) are the mean and variance predicted by a neural network parameterized by _θ_ , which attempt to approximate the true posterior of the forward process. The forward diffusion process is defined as 


where _βt ∈_ (0 _,_ 1) is a variance schedule that determines the amount of Gaussian noise injected at step _t_ . This process admits a closed-form expression for sampling at step _t_ : 


Here, _αt_ = 1 _− βt_ represents the retained signal at each step, and the cumulative product _α_ ¯ _t_ measures how much of the original data signal _x_ 0 remains after _t_ steps of noise addition. 

Building on this foundation, recent works in robotics propose Diffusion Policy (DP) (Chi et al. 2023), which represents visuomotor control as a conditional denoising diffusion process in action space. Instead of directly regressing robot actions, the policy refines Gaussian noise into an action sequence by learning the score function of the conditional distribution _p_ ( **_A_** _t|_ **_O_** _t_ ), where **_O_** _t_ are observations and **_A_** _t_ are action trajectories. This formulation leverages the advantages of diffusion, such as naturally modeling multimodal distributions, scaling to high-dimensional action sequences, and exhibiting stable training. These properties make it highly effective for robot manipulation tasks. The action generation in diffusion policy follows an iterative denoising process akin to Langevin dynamics (Welling and Teh 2011). At inference, starting from a noisy action sequence **_A_**<sup>_K_</sup> _t_<sup>, the denoising step is given by</sup> 


where _εθ_ is a neural network that predicts noise conditioned on **_O_** _t_ , _γ_ is the learning rate, _k_ is the iteration step, and _α_ and _σ_ follow a noise schedule. Training minimizes the meansquared error between predicted and true noise: 


# _2.4 Diffusion model-based policy learning_ 

Denoising Diffusion Probabilistic Models (DDPMs) (Ho et al. 2020) are a class of generative models that define a latent-variable Markov chain to progressively denoise a sample drawn from Gaussian noise into a data sample. The model learns to reverse a fixed forward process that gradually adds Gaussian noise to data according to a variance schedule. Formally, the reverse (generative) process is defined as 


This process allows the model to iteratively refine noise into structured action sequences that are both temporally consistent and reactive. As a result, diffusion-based approaches have emerged as a powerful paradigm for trajectory generation and visuomotor policy learning in robotics, bridging generative modeling and control. 

# _2.5 Knowledge base & Knowledge graph_ 

A knowledge base (KB) serves as a foundational repository of structured knowledge, encapsulating facts, rules, and relationships pertinent to a given domain. Information is organized in a structured format in a knowledge base, facilitating efficient retrieval and inference. Formally, 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

7 

knowledge bases often employ languages such as Resource Description Framework (RDF) or Web Ontology Language (OWL) to encode knowledge in a machine-readable form. 

A Knowledge Graph (KG) can be considered as a specialized form of KB with a graph structure. Formally, a Knowledge Graph (KG) is defined as _G ⊆E × R × E_ over a set _E_ of entities and a set _R_ of predicates. In the field of robot manipulation, entities often contain real-world objects, actions, skills, and other abstract concepts; relations represent the relations between these entities, such as _isComponentOf_ , _withForce_ , and _hasPose_ . Several wellknown knowledge graphs (KGs) have been developed in this field, as highlighted in various works (Waibel et al. 2011; Diab et al. 2019; Beetz et al. 2018; Kwak et al. 2022). 

Knowledge Graph Embedding (KGE) methods represent the information from a KG as dense embeddings. Entities and predicates in the KG are mapped into a _d_ -dimensional vector _Mθ_ : _E ∪R →_ R<sup>_d_</sup> . These methods can be either score function based (Bordes et al. 2013; Wang et al. 2014; Lin et al. 2015) or graph neural network based (Schlichtkrull et al. 2018; Nathani et al. 2019). 

# _2.6 Language and Multimodal Fusion_ 

Language-conditioned robot manipulation inherently requires integrating linguistic instructions with perceptual observations and robot states (Belkhale et al. 2024). This process relies on multimodal fusion, aiming to learn joint representations that align and combine information from heterogeneous modalities such as vision and language. In general multimodal learning, fusion strategies are often categorized according to how interactions between modalities are modeled during representation learning (Baltruˇsaitis et al. 2018). Three representative paradigms have emerged in recent visionlanguage multimodal frameworks. The first paradigm adopts _dual-stream architectures_ in which visual and textual features are encoded by separate networks and interact through cross-modal attention mechanisms, enabling finegrained alignment between modalities, as demonstrated in models such as ViLBERT (Lu et al. 2019). The second paradigm employs _single-stream architectures_ , where tokens from different modalities are projected into a shared embedding space and processed by a unified transformer encoder, allowing deeper cross-modal interactions and joint reasoning (Chen et al. 2020b). The third paradigm focuses on _contrastive alignment_ , which learns a shared embedding space by maximizing the similarity between paired vision and language representations, a strategy popularized by models such as CLIP (Radford et al. 2021). These multimodal fusion mechanisms provide the foundation for modern vision–language models and vision–language–action models, which ground language instructions in visual observations and enable robots to translate high-level semantic commands into executable manipulation behaviors. 

# _2.7 Language model_ 

Language models are designed to estimate the likelihood of sequences of words in human language. They learn patterns, structures, and semantics from vast amounts of textual data, enabling them to understand and predict language usage. In recent years, neural language models have advanced significantly, allowing for generating coherent and contextually relevant text. We provide a brief history of neural language models. 

**Neural Language/Lexical Models (NLMs):** NLMs (Bengio et al. 2003; Mikolov et al. 2010; Kombrink et al. 2011) leverage neural networks to estimate the probability of word sequences, e.g., recurrent neural networks (RNNs), offering a more powerful alternative to traditional statistical methods. Collobert et al. (2011) make a remarkable contribution by developing a unified neural network approach capable of handling various Natural Language Processing (NLP) tasks within a single framework, demonstrating the versatility of neural models in language understanding. Furthermore, word2vec (Mikolov et al. 2013b,a) revolutionizes word representations employing a simple yet efficient shallow neural network to learn distributed word embeddings. These embeddings have proven to be highly effective across a wide range of NLP tasks and have been instrumental in advancing applications like language-conditioned robot manipulation by enhancing semantic understanding. 

**Pre-trained Language Models (PLMs):** PLMs are an early attempt to extract semantic meaning from natural language. ELMo (Peters et al. 2018) aims to capture context-aware word representations by first pre-training a bidirectional LSTM (biLSTM) network and then fine-tuning the biLSTM network according to specific downstream tasks. Moreover, drawing inspiration from the Transformer architecture (Vaswani et al. 2017) and incorporating selfattention mechanisms, BERT (Devlin et al. 2019) takes language model pre-training a step further. It accomplishes this by conducting bidirectional pre-training exercises on extensive unlabeled text corpora. These specially crafted pretraining tasks imbue BERT with contextual understanding. 

**Large Language Models:** LLMs become popular as scaling of PLMs leads to improved performance on downstream tasks. Many researchers (Hoffmann et al. 2022) attempt to study the performance limit of PLMs by scaling the size of models and datasets, e.g., the comparatively small 1.5B parameter GPT-2 (Radford et al. 2019) versus larger 175B GPT-3 (Brown et al. 2020) and 540B PaLM (Chowdhery et al. 2023). Although these models share similar architectures, larger models exhibit enhanced capabilities such as few-shot learning, in-context learning, and improved performance on language understanding and generation benchmarks. Additionally, models like ChatGPT have adapted the GPT family for dialogue by incorporating techniques such as instruction tuning and reinforcement learning from human feedback (Ouyang et al. 2022). This results in more coherent and contextually appropriate conversational abilities, which are crucial for interactive robot manipulation tasks where ongoing dialogue between the human and robot can enhance task execution and adaptability. By integrating LLMs into robotic systems, 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

8 

researchers (Ding et al. 2022; Kant et al. 2022) aim to leverage their advanced language understanding to enable robots to handle challenging tasks by reasoning and inferring missing information. This contributes to developing more robust and flexible manipulators that can operate effectively in unstructured real-world environments (Lin et al. 2023; Ren et al. 2023a; Wu et al. 2023a). 

**Vision-Language Models:** VLMs play a key role in extracting and combining visual and textual content from large-scale web data. This paradigm equips the agent with an expansive understanding of the world. Seminal models in this domain, such as CLIP (Radford et al. 2021), Flamingo (Alayrac et al. 2022), PaLM-E (Driess et al. 2023), and PaLI-X (Chen et al. 2023d) underscore the potential of VLMs. Integrating these pre-trained VLMs into robotic systems makes it feasible for robots to tackle diverse tasks in real-world scenarios. 

**Vision-Language-Action Models** : In this work, we define vision-language-action (VLA) models as unified embodied policy models that integrate the three modalities of language, visual observations, and robot actions within a shared or tightly coupled architecture. In such models, language, images, and actions are represented in a common modeling framework, for example, as text tokens, visual tokens, and action tokens (Gato (Reed et al. 2022), RT-1 (Brohan et al. 2023a), and RT-2 (Zitkovich et al. 2023)). More recent VLAs generalize this idea from discrete action tokens to continuous action-token embeddings or diffusion-/flow-based action representations, enabling trajectory-level or low-level control generation (Kim et al. 2025c; Black et al. 2025b; Wen et al. 2025c). 

# **3 Taxonomy of language-conditioned methods for robotic manipulation** 

Over the past few years, there has been a growing interest in leveraging natural language to enhance robotic manipulation tasks, particularly in making these systems more intuitive and accessible during interactions. To facilitate a clear review of these approaches, this section outlines the taxonomy employed in the narration. While robotic learning in bridging language instructions and robot actions is often categorized by the algorithmic paradigm, such as RL, IL, or planning, this can obscure the specific and varied roles that language plays. For instance, an RL agent might use language to shape its reward function or, in a completely different manner, to directly condition its policy learning. Although both involve RL methods, the function of language is fundamentally different. To provide a clearer, more orthogonal taxonomy, we structure this survey around the primary ways language is integrated into robot systems. 

As illustrated in the fine-grained taxonomy tree in Figure 3, our classification logic progresses from macro-level functional roles down to specific algorithmic implementations and evolutionary process. The four primary categories and their underlying classification logic are detailed below: 

- **Language for state evaluation (Section 4):** Language is used to define goals and quantify task progress, by converting text into numerical feedback signals 

(reward or cost). The policy is then optimized against these signals. The core question is: How can language specify whether a state or outcome is desirable (feedback _how the progress_ )? This category is subdivided based on the type of algorithm receiving the signal and the technological evolution of the signal generation: 

   - **Reward Functions** : For learning-based agents (RL), language is translated into rewards. We trace the logical evolution of this process from manual Reward Designing (sparse vs. dense), to data-driven Reward Learning (like Inverse RL), and finally to modern Foundation Model (FM)driven automated reward generation. 

   - **Cost Functions** : For optimization-based motion planners, language is translated into cost maps. The narrative trajectory moves from specific linguistic-to-cost mappings to automated 3D cost map generation empowered by FMs. 

- **Language as a policy condition (Section 5):** Language is used as an explicit conditioning signal for a policy that maps observations to actions. The primary learning target is a control policy, and language specifies the desired behavior for the current episode or timestep. Although such methods may use multimodal encoders, language remains an external task condition rather than the organizing principle of the whole architecture. The core question is: How can language condition a policy to produce the correct behavior? This category is subdivided by the underlying algorithmic paradigms used to learn this language-conditioned mapping: 

   - **Reinforcement Learning** : Integrates language to solve trial-and-error exploration, evolving from simple goal-conditioning to lifelong multitask learning. 

   - **Behavioral Cloning** : Learns directly from expert demonstrations to bypass the sample inefficiency and complex reward engineering inherent in RL. 

   - **Diffusion-based Policy** : Represents the latest generative evolution to address BC’s limitation in handling multi-modal action distributions (traditional BC averages out expert behaviors). 

- **Language for cognitive planning and reasoning (Section 6):** Language serves as an internal reasoning medium for decomposing complex tasks and forming strategies. Core question: How a robot “ _thinks_ ” in the language space to structure its own behavior, i.e., utilizing language to reason about its goals and plan its actions. This branch is subdivided based on the type of cognitive system used to bridge abstract reasoning and perceptual reality: 

   - **Classic Neuro-symbolic approaches** : The foundational methods that use language to bridge explicit symbolic logic (like Knowledge Graphs) with neural perception. 

   - **Empowered by Large Language Models** : Approaches that replace rigid symbolic systems with LLMs for open-vocabulary text reasoning 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

9 


**Figure 3.** Overview list of representative language-conditioned robotic manipulation methods. 

and code generation, often without task-specific retraining for the planning module. 

   - **Empowered by Vision-Language Models** : Methods that resolve the “blindness” of pure LLMs by directly grounding textual reasoning in visual observations. 

- **Language in unified vision-language-action models (Section 7):** Language is not used merely as an external condition; instead, it is jointly modeled with visual observations, language and robot actions within an embodied policy architecture which unifies the modalities of images, text, and actions. In such a system, perception, semantic grounding, and action generation are increasingly learned within one embodied foundation model, often by extending pretrained VLMs/LLMs with robot action representations. The core question is: How can vision (perception), language (semantic grounding), and action be unified into a single scalable model for embodied decision-making? This branch is subdivided based on different optimization directions for bridging language and action: 

   - **Perception** : Methods that focus on optimizing how VLAs perceive and understand their environment. 

   - **Reasoning** : Approaches that enhance the model’s internal “thought process”, that is, how it forms plans, leverages prior knowledge, and predicts outcomes to solve complex tasks. 

   - **Action** : Methods that focus on the optimization regarding the “output” stage of the policy, concerning the form and mechanism of the robot’s actions. This bridges the gap between 

the model’s internal plan and its physical embodiment. 

- **Adaptation** : Techniques that adapt pretrained VLAs to new tasks, objects, or scenes while preserving or improving the grounding between language instructions and executable actions. 

Each subsequent section explores the advanced techniques developed within these sub-branches, highlighting their unique contributions, chronological evolution, and the specific challenges they aim to resolve. 

# **4 Language for state evaluation** 

Traditionally, specifying a robot’s objective has required significant expert engineering, such as hand-crafting dense reward functions (Eschmann 2021) or defining precise goal coordinates in the state space (La Valle 2011). This process is not only labor-intensive but also rigid, and the robot cannot easily generalize to new goals without being reprogrammed. Natural language provides a powerful solution to this limitation. It offers a flexible, intuitive, and generalizable interface, enabling non-experts to communicate a vast range of complex, abstract, or compositional goals in multi-task scenarios without programming efforts (Tellex et al. 2020), such as from “ _pick up the red block_ ” to “ _tidy up the table_ ”. This shifts the paradigm from low-level programming to high-level human-centric goal specification. This brings us to the first key research question: How can we use language to quantify task progress? The core idea is to translate a language instruction into a quantitative scoring function that evaluates how well a robot’s state or action aligns with the desired outcome, guiding the robot towards desired 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

10 


**Figure 4.** An illustration of different reward schemes. (a) Dense reward: The agent receives a gradually increasing reward as it approaches the goal, providing continuous guidance. (b) Sparse reward: The agent only receives a large reward upon reaching the final goal state. (c) Reward function learning: A function is learned to map state-goal pairs to a continuous reward value, creating a smooth reward gradient. ✩ the starting position. 

behaviors efficiently. This numerical signal, which can serve as a reward for RL agents or a cost for planners, provides the essential feedback for the robot to learn or plan effectively. Grounding language in state-space valuations is a central challenge and can be implemented in two primary ways. 

- Language-conditioned reward functions: In RL, the language-derived score serves as a reward function. It guides the agent’s trial-and-error learning, reinforcing behaviors that bring it closer to fulfilling the instruction. These methods can be further categorized by the numerical properties of the reward signal, such as dense rewards, sparse rewards, or fully learned reward functions, as illustrated in Figure 4. 

- Language-conditioned cost functions: In task and motion planning, the score serves as a cost function. It guides a search algorithm to find an optimal sequence of actions that minimizes the cost, thereby achieving the goal specified in the language command. For example, for command “ _Pick up the apple, but stay away from the vase_ ”, the cost function would assign a high penalty to any trajectory that nears the vase. A motion planner would then search for a path that minimizes this total cost, resulting in a trajectory that safely navigates around the vase to reach the apple. 

This section reviews the methods developed to address this problem, including Language-conditioned reward designing/learning in Sec. 4.1 and Language-conditioned cost functions in Sec. 4.2. The taxonomy illustrated in Figure 5. In addition, to provide a clearer overview of how language is utilized to quantify task progress, Table 2 summarizes representative state-of-the-art methods discussed in this section. These approaches are categorized by the type of algorithmic signal they generate, such as rewards for reinforcement learning or cost functions for motion planning. Furthermore, the table traces the technological evolution of these signals, moving from manual reward design and data-driven learning to the recent integration of foundation models that automate signal generation. This comparison explicitly highlights the core mechanisms, key advantages, and inherent limitations of each state-evaluation paradigm. 

# _4.1 Language-conditioned reward designing/learning_ 

In many RL scenarios, particularly for complex manipulation tasks, agents often learn from sparse rewards, which provide 


**Figure 5.** Taxonomy of Sec. 4 Language for state evaluation. 

a positive signal only upon task completion (Andrychowicz et al. 2017; Riedmiller et al. 2018; Bing et al. 2023b). This is because defining a continuous measure of progress for abstract or contact-rich tasks like “folding a shirt” (Jangir et al. 2020) or “inserting a key” (Ocana et al. 2023) is difficult, as their success is often binary and depends on a complex combination of factors that are hard to quantify. This approach is sample-inefficient, as the agent may struggle to discover the goal through random exploration, resulting in long learning time. On the contrary, dense rewards, such as the distance to a target, provide stronger learning signals but are difficult to specify, and often require intensive manual engineering and domain expertise for each new task (Sutton and Barto 1998). A common technique to accelerate learning is reward shaping (Ng et al. 1999), which provides the agent with additional, intermediate rewards to guide it toward the goal. However, designing these shaping functions can also be a challenging and time-consuming process in multitask scenarios (Yu et al. 2020). Using natural language instructions offers a more intuitive solution, instead of requiring an expert to engineer a complex function, anyone can provide simple instructions, like “ _Jump over the skull while going to the left_ ”, to specify desired behaviors (Goyal et al. 2019). These instructions can then be translated into intermediate language-based rewards by a pre-trained language-action matching model, guiding the agent’s exploration and accelerate learning. Languageconditioned reward designing/learning approaches make it convenient for non-experts to teach new skills for RL agents. 

### _4.1.1 Language-based reward signal designing_ 

Language provides a natural and expressive medium for designing reward signals that guide robot learning. Instead of manually engineering complex reward functions, language allows users to specify desired behaviors, goals, or preferences intuitively. These signals can be broadly categorized into two types: _sparse reward_ and _dense reward_ , as illustrated in Figure 4. Each type presents a distinct trade-off between design simplicity and learning efficiency. A _sparse reward_ provides a meaningful signal only upon task completion (e.g., a single positive reward for success), which is simple to define but often leads to sample-inefficient learning. In contrast, a _dense reward_ offers continuous 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

11 

**Table 2.** Comparison of representative state-of-the-art methods for **Section 4 Language for state evaluation** . The table highlights how different algorithms translate language into quantitative signals (rewards for reinforcement learning or costs for motion planning) , tracing the evolution from manual design and data-driven learning to automated foundation model-driven generation. 

|**Method**|**Signal**<br>**Category**|**Core Mechanism**|**Key Advantages**|**Key Disadvantages**|
|---|---|---|---|---|
|ZSRM<br>(Mahmoudieh<br>et al. 2022)|Sparse<br>Reward<br>Design|Design reward by calculating<br>similarity between a camera<br>image and goal text using<br>CLIP.|Enables reward specification<br>for some new goals with-<br>out additional reward-model<br>training.|Performance<br>is<br>fundamentally<br>limited<br>by the CLIP model’s spatial<br>reasoning abilities.|
|PixL2R<br>(Goyal<br>et<br>al.<br>2021)|Dense<br>Reward<br>Design|Learns a relatedness model<br>from paired data (language<br>and trajectory) to generate a<br>dense shaping reward.|Significantly improves pol-<br>icy learning efficiency by<br>providing continuous guid-<br>ance.|Relies on absolute scores as<br>ground truth and requires<br>diverse language datasets.|
|LOREL<br>(Nair<br>et<br>al.<br>2022)|Reward<br>Learning|Implements a binary classi-<br>fier trained on offline expert<br>demonstrations.|Automates<br>the<br>translation<br>of visual observations and<br>instructions into reward sig-<br>nals.|Struggles<br>with<br>complex<br>manipulation tasks involving<br>fine-grained<br>behaviors<br>or<br>multiple objects.|
|Text2Reward<br>(Xie et al. 2024)|FM-driven<br>Reward<br>Generation|Uses LLMs to write dense<br>Pythonic reward functions<br>directly from natural lan-<br>guage goals.|Enables autonomous reward<br>generation<br>and<br>matches<br>expert rewards on simulated<br>tasks.|Relies heavily on the correct-<br>ness of generated code and<br>requires a privileged simula-<br>tor state.|
|ReWiND<br>(Zhang<br>et<br>al.<br>2025b)|VLM-driven<br>Reward<br>Learning|Learns a progress-predicting<br>reward<br>from<br>language-<br>annotated<br>demonstrations<br>and generated failures.|Improves success rates sig-<br>nificantly in both simulation<br>and real bi-manual setups.|Requires<br>a<br>handful<br>of<br>demonstrations to learn a<br>general reward.|


feedback at each step, guiding the agent more effectively but typically requiring significant manual engineering. 

For the former one, language can be used to generate a _sparse_ reward signal to indicate whether the agent’s current state successfully fulfills the language instruction, providing a flexible way to specify complex goals or human preferences. For example, ZSRM (Mahmoudieh et al. 2022) derives the entire reinforcement learning reward from a natural language goal description. At each step, it generates a reward by calculating the similarity between a camera image and the goal text using CLIP encoders. This text-vision matching method enables reward specification for some newly described goals without retraining the reward model, although transfer degrades on tasks that require stronger spatial reasoning from the CLIP model. An alternative approach is to design a reward function by interpreting human preferences expressed through comparative language. Yang et al. (2025i) designs a reward learning scheme with comparative language feedback, e.g., “ _move farther from the stove_ ”. The system aligns trajectory data with language feedback in a shared latent space, turning each piece of comparative language into a learning signal to train an episodic reward model that captures the user’s underlying preferences. However, the model’s ability to generalize is limited by the objects and concepts seen during its pretraining phase. Despite the convenience of language-based sparse reward design, such methods may still face challenges with low sample efficiency, requiring extended training periods or even failing to converge (Ladosz et al. 2022). 

To address the sample inefficiency of sparse rewards, another line of work uses language to create _dense_ , _intermediate_ reward signals that provide more continuous guidance. These approaches typically learn a model that scores how well an ongoing trajectory aligns with a language command, 

using this score to shape the reward at every timestep. An example is PixL2R (Goyal et al. 2021), which maps natural language and pixels directly to a continuous reward signal. It first learns a relatedness model from paired trajectory and language data. During policy training, this model evaluates the agent’s trajectory and turns the language command into a potential function (Ng et al. 1999). This potential generates a dense shaping reward that is added to the environment’s original reward at every step, significantly improving policy learning efficiency. This suggests a powerful paradigm where language can be used to refine and improve upon existing hand-designed reward functions. However, this method relies on classification and regression training objectives with absolute scores as ground truth, which can be rigid and may not fully capture the task progress. Furthermore, a limited language dataset may not showcase the diversity of language descriptions needed to guide robot learning effectively. 

### _4.1.2 Language-based reward function learning_ 

The above reward designing approaches highlight the importance of designing effective reward signals with language instructions, while requiring extensive manual effort and are often challenging in real-world scenarios, limiting real-world manipulation performance (Deshpande et al. 2025). Reward function learning aims to learn a reward function from data (e.g., demonstrations or human video (Das et al. 2021; Zakka et al. 2022a)), rather than manually designing it. This flexible and scalable manner enables the reward models can adapt to multi-task (Dimitrakakis and Rothkopf 2011) or crossembodiments (Zakka et al. 2022a; Kumar et al. 2023) scenarios without requiring expert knowledge. In languageconditioned manipulation, reward learning methods typically learn a function that maps observations and a language instruction to a scalar reward value, which can then be used 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

12 

to guide a standard RL agent. Some studies directly pre-train a reward mapping model using offline expert demonstrations. For example, LOReL (Nair et al. 2022) implements a binary classifier _R_ ( _s_ 0 _, s, l_ ) that receives the initial state _s_ 0, current state _s_ , and language instruction _l_ , predicting whether a trajectory segment satisfies a given language instruction. This model translates visual observations and language instructions into reward signals. Besides direct learning, a classic alternative for learning the reward function from demonstrations is IRL (Arora and Doshi 2021). 

IRL is utilized to deduce the underlying reward structure, alleviating the challenge of manual reward design. It infers the rewards that could explain the observed actions of an expert. Rather than simply learning from experts, IRL has the potential to achieve better performance than the expert by optimizing the inferred reward function (Finn et al. 2016). Integrating language instructions into IRL learn reward functions that are not only consistent with the expert’s actions but also grounded in the specific textual command, showcasing promising performance in various tasks, such as navigation (Zhou and Small 2021) and mobile manipulation tasks (Fu et al. 2019). In mobile pick-and-place manipulation tasks, MacGlashan et al. (2015) present a system that grounds natural language commands to reward functions through IRL, using demonstrations of different natural language commands being carried out in the environment. Fu et al. (2019) propose language-conditioned reward learning based on MaxEnt IRL, which grounds language commands as a reward function represented by a deep neural network, incorporating generic, differentiable function approximators that can handle arbitrary observations (such as raw images). Learning the reward functions, combining language instructions and IRL, empowers the robot to solve novel tasks and transfer to realistic environments (Fu et al. 2019), or the learned reward functions can be transferred to new robots (MacGlashan et al. 2015). However, these methods struggle with complex manipulation tasks that involve finegrained behaviors or interactions of multiple objects (Das et al. 2021; Zhang et al. 2025b). A primary reason is that the ambiguity of the expert’s intent grows exponentially with the complexity of the task (Adams et al. 2022). 

In the simple pick-and-place tasks, most demonstrations follow a simple and optimal path, making it easy for traditional IRL agents to infer the reward with the language instruction like “ _move X object to Y position_ ” (Fu et al. 2019). However, for complex manipulation tasks like “ _sort out the kitchen table and wiping a stain_ ”, expert demonstrations can vary significantly in terms of manipulating trajectory for different types of objects. This variability makes it difficult for traditional IRL methods to learn the powerful reward functions that can distinguish the true underlying goal from spurious correlations in the limited demonstration data. Consequently, these methods often require a large number of demonstrations to learn a robust reward function (Hwang et al. 2025) and struggle to generalize beyond the specific conditions they were trained on. This highlights a bottleneck, that is, the need for a reward model that possesses a general, common-sense understanding of the world, rather than one learned from scratch for each new task (Glazer et al. 2024). 

### _4.1.3 Foundation model-driven reward designing and learning_ 

The limitations of aforementioned traditional reward models, particularly their reliance on task-specific datasets and rigid training objectives, have motivated a shift towards more flexible and generalizable solutions. Foundation models (such as LLMs and VLMs), with their broad pretrained knowledge and powerful open-vocabulary inference abilities (Hurst et al. 2024; Yang et al. 2025a), provide a powerful alternative. Instead of learning a reward function from scratch on a limited dataset, these models can leverage their inherent understanding of language and vision in foundation models to directly infer task progress, thereby automating the reward design process and overcoming the need for extensive manual engineering or data collection. 

### **LLM-driven reward code generation** 

Early works leveraging FMs for reward generation explored several distinct strategies. One initial approach repurposed LLMs into reward functions. For example, Kwon et al. (2023) reframe GPT-3 (Brown et al. 2020) itself as a proxy reward function, prompting it with a trajectory transcript and asking whether the behavior satisfied a textual objective. This prompting-based ‘language reward’ can align agents with minimal or no task-specific demonstrations, but the setting remains confined to symbolic domains and incurs high query costs. To overcome the latency and domain-shift limits of such on-the-fly calls of LLMs, LAMP (Adeniji et al. 2024) proposes a two-stage strategy: first, use a frozen vision-language model combination (R3M (Nair et al. 2023) + DistilBERT (Sanh et al. 2019)) to score image-language alignment and treat that score as a dense learning signal during pre-training, then fine-tune with conventional task rewards. The approach warm-starts manipulation policies, yet its intrinsic rewards are noisy, and VLM inference during pre-training remains expensive. 

Language2Reward (Yu et al. 2023c) pushes further by asking an LLM to write executable reward code from naturallanguage instructions, enabling real-time user corrections and covering both quadruped locomotion and dexterous manipulation tasks. However, the method relies on the correctness of the generated code and presumes an accurate simulator. Recognizing that even task design and scene layout constrain scalability, RoboGen (Wang et al. 2024d) wraps foundation models in a proposegenerate-learn loop: the system autonomously proposes tasks, builds 3-D scenes, selects between RL, motion planning, or trajectory optimisation, and writes its own reward functions, producing an endless stream of diverse skills. Its current limitation is that everything still happens in simulation, with no guarantee of real-world transfer. Parallel work tackles reward generalization itself: Vision-Language Success Detectors (Du et al. 2023a) fine-tune Flamingo on human-labelled “success/failure” clips and cast success detection as a VQA problem, achieving stronger out-ofdistribution robustness than traditional detectors. However, they still require labelled videos, and their binary output leaves temporal credit assignment open. 

### **Reward code generation with self-improving** 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

13 

Building on the above insights, some research focused on creating fully autonomous and sensor-grounded reward systems. The initial problem was that “ _LLM-generated code was often fragile and required human oversight_ ” (Kwon et al. 2023; Guo et al. 2024). Driven by the need for self-improving signals, Text2Reward (Xie et al. 2024) lets GPT-4 and Codex (Chen et al. 2021) write dense reward functions directly from a natural-language goal with a Pythonic environment sketch, even refining the code through self-execution and optional human feedback. Policies trained on the generated code match or beat expert rewards on simulating manipulation tasks. To improve the robustness of LLM-driven reward code generation, EUREKA (Ma et al. 2024) generates a high-performance reward function in an evolutionary manner. It uses RL policy performance as a fitness score to guide the LLM in iteratively improving a population of reward programs. Such a loop is iterated until it meets the termination condition. 

A key limitation remained: the generated code used static numeric weights for different reward components (like “Reward=0.8 _×_ grasp ~~s~~ uccess-0.2 _×_ dist ~~t~~ o ~~c~~ ube”), which may be suboptimal. If the first draft of the generated reward code selects fragile features, the RL agent can not learn effectively. This motivated a new focus on learning these parameters automatically. Methods like Reward-Self-Align (Zeng et al. 2024) and R* (Li et al. 2025a) move beyond just code generation to parameter optimization. Reward-Self-Align (Zeng et al. 2024) first lets an LLM write feature templates, then iteratively aligns their parameters with the LLM’s pair-wise ranking of real rollouts. R* (Li et al. 2025a) learns dense reward weights from LLM preferences, but it disentangles the two challenges altogether: evolving reward structure while a critic ensemble aligned the reward function weights. The learned rewards outperform both human and EUREKA (Ma et al. 2024). 

In addition to developing methods for self-aligning critics and searching for both reward structure and weights, some methods turn to the twin bottlenecks of sample efficiency and latent-preference mis-specification. RLingua (Chen et al. 2024a) provides a solution by addressing the millions of interactions required by RL agents. The core idea is to prompt an LLM to generate an imperfect, rulebased controller that seeds the replay buffer and guides policy exploration, thereby reducing sample complexity. However, because this controller is bound to hand-coded state variables, it underperforms on more complex tasks. To mitigate this limitation, ELEMENTAL (Chen et al. 2025c) fuses VLM reasoning with IRL. In this interactive pipeline, a VLM drafts executable reward features from a text prompt and a key-frame demonstration, while MaxEnt-IRL learns the weights that best match the demonstration, iteratively refining the features through a self-reflection loop. This improves generalization and success rates by narrowing the gap between a generated reward and human preferences. 

### **VLM-driven reward learning** 

However, a drawback of these LLM-driven code-centric methods is their dependence on privileged simulator state information. To operate in the real world using visual input, the focus shifted to VLMs. Video-Language 

Critic (Alakuijala et al. 2025) trains a temporal contrastive VLM with ranking loss on large “Open X-Embodiment” videos (O’Neill et al. 2024). The critic assigns a dense and monotonically increasing reward based on pixelinstruction pairs only and transfers across robots, thereby doubling sample efficiency over sparse rewards on unseen manipulation tasks. While this method needs thousands of good trajectories to learn a general reward. RealBEF (Wang et al. 2025c) fine-tunes the smaller VLM ALBEF (Li et al. 2021) backbone with pair-wise image comparisons, so only a few task videos are needed. Rewards guide RL on MetaWorld benchmarks (Yu et al. 2020) better than previous image-based methods and alleviate data hunger. To further improve data efficiency, ReWiND (Zhang et al. 2025b) learns a progress-predicting reward from a handful of languageannotated demonstrations combined with “video-rewind” generated failures, then fine-tunes policies on unseen tasks with that reward. Its success rate beats baselines 2 _×_ in the Meta-World simulation and 5 _×_ on a real bi-manual setup. Systems like ARCHIE (Turcato et al. 2025) demonstrate a path toward real-world deployment by using an LLM to generate both the reward code and a success classifier, enabling autonomous training in simulation and successful transfer to a physical robot. However, this method relies on an assumption that the generated success detector is correct. 

In summary, the integration of foundation models into reward designing and learning represents an advancement in language-conditioned robot manipulation. Early FMdriven methods (e.g., LAMP (Adeniji et al. 2024), Text2Reward (Xie et al. 2024), and EUREKA (Ma et al. 2024)) showed that LLMs can replace manual reward engineering, but exposed the weight-tuning fragility of the generated reward code. Reflection and preferencealignment methods (like Reward-Self-Align (Zeng et al. 2024), R* (Li et al. 2025a)) improve robustness by learning parameters, whereas evolutionary search overcame local optima. Methods like Rlingua (Chen et al. 2024a) and ELEMENTAL (Chen et al. 2025c) enhance sample efficiency and preference alignment. But these codecentric methods still required privileged simulator state information. The VLM-based methods (Video-Language Critic (Alakuijala et al. 2025), RealBEF (Wang et al. 2025c)) bypass this limitation by learning dense rewards directly from pixels and language, but they introduce datascale issues. Hybrid approaches, such as ReWiND (Zhang et al. 2025b) and ARCHIE (Turcato et al. 2025), decrease demonstration cost and mitigate the sim-to-real gap, thereby showcasing a fully autonomous reward design. 

# _4.2 Language-conditioned cost functions_ 

While reward functions guide learning-based agents, cost functions are essential for optimization-based motion planners. Translating language into a cost function enables a robot to understand not only a goal, but also the constraints and preferences that indicate how to achieve it, turning natural language into a formal optimization objective. 

### _4.2.1 Specific linguistic-text cost mapping_ 

Early motion-planning pipelines couldn’t directly interpret a human’s verbal goals, requiring hand-coded cost terms or 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

14 

exact goal configurations (Yamashita et al. 2003; Cambon et al. 2009). This rigidity made them unsuitable for openended environments like households. The initial problem was “ _how to extract a task-relevant cost map from text_ ”. Some research focuses on creating a tighter loop between specific linguistic text and the planner’s cost function. Park et al. (2019) introduce dynamic constraint mapping, where a Conditional Random Field (Sutton et al. 2012) grounds each _noun phrase_ or _adverb_ (“upright” and “slowly”) into the continuous parameters of a trajectory optimizer. This allows the same natural-language template to generate different cost functions on the fly. However, the limitation is that it relies on attribute-level annotations and requires retraining to handle new linguistic structures. Sharma et al. (2022) shift the supervision burden to the user. Their planner executes a trajectory and then incorporates spoken _corrections_ like “ _stay away from the yellow bottle_ ” by learning a residual cost function that modifies the optimizer’s objective. They sidestep the need for a fully annotated dataset but are limited to generating 2D cost maps, which struggle in 3D scenes. 

of “acceptable contact”. It feeds multi-view RGBD images to GPT-4o, rating each object’s “contact tolerance” on a 0-10 scale and is then used to create a 3D cost map that integrates directly with standard planners ( e.g., RRT* (Karaman and Frazzoli 2011)). The robot can make incidental contact with a soft object while strictly avoiding a fragile one, without explicit instructions to do so. IMPACT unifies high-level semantic reasoning with continuous optimization, but is limited by its assumption of a static scene and perfect object segmentation, opening up a challenge: online cost refinement as the environment changes. 

# _4.3 Summary_ 

In its role as a tool for state evaluation, language provides a flexible and intuitive interface for specifying a robot’s objectives, translating high-level instructions into quantitative scoring functions that guide robot behavior. This paradigm addresses our first core question by grounding language into reward functions for reinforcement learning or cost functions for motion planning. 

### _4.2.2 FM-driven cost mapping_ 

To tackle 3D complexity, VoxPoser (Huang et al. 2023b) harnesses foundation models. It uses GPT-4 to write Python code that queries a VLM (OWL-ViT (Minderer et al. 2022)) to compose dense 3D value maps. These maps assign high values (rewards) to affordances and low values (costs) near constraints (like “ _watch out for the vase_ ”), enabling a standard motion planner to synthesize trajectories from novel language instructions without planner retraining. The primary limitation is its heavy reliance on the perception module, which integrates OWL-ViT (Minderer et al. 2022), Segment Anything (Kirillov et al. 2023), and XMEM (Cheng and Schwing 2022). If the object detector fails, the resulting cost map is incorrect. To capture complex spatio-temporal relationships, ReKep (Huang et al. 2025b) alternatively uses a VLM to write Python code defining symbolic constraints instead of creating a value map (Huang et al. 2023b). ReKep first uses a vision model (DINOv2 (Oquab et al. 2024)) to automatically propose semantically meaningful 3D keypoints on objects. An image with these keypoints and user language is then fed to a VLM, which generates a sequence of cost functions defining arithmetic relationships between the keypoints (like _minimizing the distance between a teapot spout and a cup_ ). These code-based constraints are passed to a real-time optimization solver that plans the robot’s trajectory. A key advantage is its ability to implicitly specify complex 6-DoF motions by having the VLM reason only about simple 3D point relationships, offloading the difficult geometric calculations to the numerical solver. 

Instead of composing value maps, LACO (Xie et al. 2023a) learns a collision function directly. It uses a transformer to fuse a single RGB image, the robot’s joint state, and a language prompt (such as “ _can collide with toy_ ”) to predict a language-conditioned collision score. This score is then used as a cost by the planner. By avoiding the need for depth data or 3D meshes, it generalizes well. However, its reliance on a single camera view means it ignores risks posed by occluded objects. IMPACT (Ling et al. 2025) leverages the advanced semantic and spatial reasoning capabilities of VLMs (GPT-4o (Hurst et al. 2024)) to automate the inference 

Initial methods focused on manually designing languagebased rewards, which could be sparse (Mahmoudieh et al. 2022) or dense (Goyal et al. 2021). While more intuitive than traditional reward engineering, these approaches often struggled with sample inefficiency or required significant expert effort. Reward function learning, particularly through IRL, offered a data-driven alternative by inferring rewards from expert demonstrations. However, these methods face challenges in complex multi-object manipulation tasks where expert intent is ambiguous, often requiring an impractically large number of demonstrations to generalize effectively. The development of FMs accelerates this shift, automating reward design by leveraging their vast pretrained knowledge. Early approaches used LLMs to generate reward code (Yu et al. 2023c) or act as proxy reward functions (Kwon et al. 2023). More advanced methods have created fully autonomous systems that can write, refine, and optimize reward functions through self-reflection, evolutionary algorithms (Ma et al. 2024), or alignment with human preferences (Zeng et al. 2024; Li et al. 2025a). VLMbased methods further bridge the sim-to-real gap by learning dense rewards directly from pixels and language (Alakuijala et al. 2025; Zhang et al. 2025b). Similarly, in motion planning, FMs are used to generate dense 3D cost maps from language, enabling planners to handle previously unseen language constraints and affordances without taskspecific retraining of the planner, although success remains conditional on perception quality and scene coverage (Huang et al. 2023b, 2025b; Ling et al. 2025). The overarching insight is that the role of language in state evaluation has evolved from a tool for manual reward/cost specification to a medium for automated, knowledge-driven reward and cost generation, powered by FMs’ reasoning capabilities. This progression has enhanced the scalability, flexibility, and data efficiency of teaching robots complex manipulation tasks. 

# **5 Language as a policy condition** 

While the previous section focused on using language to quantify the task progress for implicitly directing the robot’s 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

15 


**Figure 6.** Taxonomy of Sec. 5 Language as policy condition. The arrow (“addresses limitations of”) head is commonly used to introduce a family that alleviates key practical limitations of the preceding family (not a strict hierarchy or a complete replacement). For instance, language-conditioned behavioral cloning can reduce reliance on reward engineering and exploration in RL by learning directly from demonstrations, while diffusion-based policies can further alleviate BC’s tendency to imitate suboptimal or averaged behaviors, albeit sometimes at the cost of higher inference latency. 

behaviors. This section shifts to an alternative paradigm for clarifying the role of the language in robotic manipulation: using language as an explicit condition for policy learning to specify _how_ a robot should act. Instead of translating language into a reward or cost function that indirectly guides a learning or planning algorithm, the methods discussed here integrate language into the policy itself. This approach addresses our second key research question: How can language condition a policy to produce the correct behavior? Here, the policy _πθ_ , parameterized by the neural network _θ_ , learns a direct mapping from the current observation _st_ and the language instruction _l_ to an action _at_ , i.e., _πθ_ ( _at|st, l_ ). This changes the role of language from a goal specifier to a behavior specifier. We will explore how this concept is realized through different families of algorithms, including reinforcement learning, imitation learning, and emerging diffusion-based policy learning. Figure 6 presents the taxonomy of this section. 

Table 3 presents a comprehensive comparison of the stateof-the-art methods that shift the role of language from a goal specifier to a behavior specifier, mapping observations and instructions directly to actions. The table categorizes these approaches by their underlying algorithmic paradigms: reinforcement learning, behavioral cloning, and diffusionbased policy learning. By analyzing these methods sideby-side, we can observe the progression of techniques designed to address distinct learning bottlenecks, such as addressing sample inefficiency and exploration challenges in RL, or overcoming the averaging of multi-modal behaviors in standard BC through generative diffusion models. 

# _5.1 Language in reinforcement learning_ 

RL algorithms can be applied to tasks based on languageconditioned rewards. Early attempts at language-conditioned RL concentrated on games (Fu et al. 2019; MacGlashan 

et al. 2015; Bahdanau et al. 2018; Kaplan et al. 2017; Goyal et al. 2019), since games often have well-defined rules and objectives, and also easy to reproduce experiments and compare the performance. These studies train an agent capable of comprehending natural language instructions given by humans. In these games, human languages are given to control the agent to solve navigation tasks (Chaplot et al. 2018; Misra et al. 2017; Andreas et al. 2017; MacGlashan et al. 2015; Janner et al. 2018), scoring games (Kaplan et al. 2017; Goyal et al. 2019), and object manipulations (Bahdanau et al. 2018). However, this does not explain how language can guide robots to perform complex manipulation tasks with high-dimensional actions. 

An early solution was to decouple language from control. LCGG (Colas et al. 2020) uses language to condition a goal generator, which then provides a language-agnostic goal to a pre-trained goal-conditioned policy. This modularity allows any off-the-shelf RL controller to be used, enabling a single instruction to generate a diverse range of behaviors. However, because language never directly touches the policy network, the robot cannot adapt its low-level behavior to linguistic intent and is limited to simple pick-and-place tasks involving different colors. To address this limitation, subsequent research aims to integrate language more tightly into the policy loop. For example, LanCon-Learn (Silva et al. 2021) achieves this by directly feeding a language embedding into an attention router that gates multiple skill modules inside a shared actor-critic network. By allowing language to re-weight reusable skills at every timestep, a single network could master dozens of tasks and recombine them for limited task recomposition on held-out instructions or task combinations. The drawback is that learning the router and control policies simultaneously proved to be fragile and sample-hungry. To improve sample efficiency, MILLION (Bing et al. 2023a) introduces a memorybased meta-learning approach using a Gated TransformerXL (Parisotto et al. 2020). It separates the process into a brief instruction phase, where the model reads the language command into its memory, and a trial phase, where it acts based on that stored context. This decoupling of “reading” from “acting” accelerates exploration and enables rapid adaptation to unseen manipulation tasks. Building on this, Yao et al. (2023) observes that many manipulation tasks come in symmetric pairs (“open left drawer” vs. “open right drawer”). It automatically generates symmetric language instructions using antonym rules and co-trains the MILLION backbone on both the original and symmetric tasks, leading to faster convergence and improved performance. Yet handcrafted symmetry rules are not always applicable. 

Free-form language instructions exhibit expression diversity, where the same task can be described with varied expressions. Thus, directly learning from language instructions can be sample-inefficient. Some works explore whether a more structured language representation could improve efficiency. For example, TALAR (Pang et al. 2023) proposes translating free-form text into a compact and discrete set of TaskLanguage (TL) predicates using a VAE-based translator. The RL policy is then trained only on this simplified TL, making the learning process more data-efficient and the resulting task codes more interpretable. Similarly, LOVM (Ye et al. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

16 

**Table 3.** Comparison of representative state-of-the-art methods of **Section 5 Language as a policy condition** . These selected approaches illustrate the progression across reinforcement learning, behavioral cloning, and diffusion-based paradigms , demonstrating how language acts as a behavior specifier to solve distinct learning bottlenecks like sample inefficiency and multi-modal behavior averaging. 

|**Method**|**Learning**<br>**Paradigm**|**Addressed Bottleneck**|**Key Advantages**|**Key Disadvantages**|
|---|---|---|---|---|
|MILLION<br>(Bing<br>et<br>al.<br>2023a)|Reinforcement<br>Learning|Sample inefficiency during<br>exploration.|Achieves rapid adaptation on<br>unseen tasks via memory-<br>based meta-learning.|Requires<br>decoupling<br>the<br>reading<br>phase<br>from<br>the<br>acting phase.|
|FLaRe<br>(Hu<br>et al. 2025a)|Reinforcement<br>Learning|Inefficient learning of multi-<br>task behaviors from scratch.|Achieves 15x faster learning<br>than dense-reward baselines<br>via fine-tuning.|Inherits the limitations of<br>the pre-trained BC model’s<br>training data distribution.|
|PerAct<br>(Shridhar<br>et al. 2023)|Behavioral<br>Cloning|Learning 3D spatial relation-<br>ships from 2D projections.|Provides a strong 3D struc-<br>tural<br>prior<br>by<br>voxelizing<br>both observations and action<br>spaces.|Introduces<br>high<br>computa-<br>tional overhead due to dense,<br>high-resolution voxelization<br>requirements.|
|HULC<br>(Mees<br>et<br>al.<br>2022a)|Behavioral<br>Cloning|Long-horizon task learning<br>and generalization.|Creates<br>robust<br>language-<br>conditioned representations<br>using<br>a<br>transformer-based<br>architecture.|Standard BC methods inher-<br>ently suffer from compound-<br>ing execution errors over<br>long horizons.|
|StructDiffusion<br>(Liu<br>et<br>al.<br>2023c)|Diffusion-<br>based Policy|Grounding<br>language<br>in<br>physically<br>plausible<br>scene<br>arrangements.|Samples diverse, collision-<br>free goal poses for multiple<br>unseen objects.|Performance is heavily lim-<br>ited by the capabilities of<br>subsequent low-level poli-<br>cies.|
|ChainedDiffuser<br>(Xian<br>et<br>al.<br>2023)|Diffusion-<br>based Policy|Long-horizon<br>continuous<br>trajectory generation.|Unifies discrete keypose pre-<br>diction with local trajectory<br>diffusion for smooth motion.|Inherits the high inference<br>latency typical of iterative<br>denoising processes.|


2024) grounds language at the pixel level by using FiLM layers to modulate image features based on the instruction that is encoded by BiGRU or DistilBERT, which in turn predicts object masks for training a downstream DQN. Both approaches demonstrate high success rates in pick-place tasks but come with their own trade-offs: TALAR (Pang et al. 2023) requires a curated dataset to pre-train its translator, while LOVM (Ye et al. 2024) needs pixel-level mask supervision. InstructRobot (Cleveston et al. 2025) shows that a small transformer can directly map raw language combined with RGB-D observations to a 26-DoF robot’s joint commands without requiring curated language-action pairs or handcrafted task predicates. The approach is modular and lightweight, but it handles only short-horizon simple tabletop tasks and relies on customized sparse rewards. 

Learning multiple complex manipulation tasks with a single RL policy remains an open challenge, which may bring the issue of catastrophic forgetting. LEGION (Meng et al. 2025a) clusters language embeddings online and uses the resulting cluster ID to gate reusable skills, demonstrating that language helps disambiguate tasks during lifelong learning and enables recombining mastered subtasks to solve unseen long-horizon goals. Furthermore, FLaRe (Hu et al. 2025a) mitigates this limitation by fine-tuning a large pre-trained behavioral cloning policy (vision-language transformer) with PPO under sparse linguistic rewards, achieving 15 times faster learning than dense-reward baselines and supporting rapid embodiment transfer. However, the reliance on a pre-trained BC model means it inherits the limitations of its training data and may struggle with tasks outside that distribution. To avoid fine-tuning or even accessing the weights of the pre-trained policy, V-GPS (Nakamoto 

et al. 2025) learns a language-conditioned value function via offline RL, and the learned value function can re-rank the actions of the pre-trained policy, steering the agent’s behavior at deployment time. Recent work pushes further by injecting additional structure into the multi-task learner: LIMT (Aljalbout et al. 2025) combines language with worldmodel imagination. A Sentence-BERT vector conditions both a VQ-VAE tokenizer and a transformer dynamics model inside a Dreamer pipeline, and the latent actor-critic agent (model-based RL) then plans in imagination before acting. Therefore, when the agent predicts the future during training and execution, the language itself can provide information to it, thereby improving sampling efficiency and generalization. 

In summary, using language as a direct policy condition in RL transforms it from a goal specifier to a behavior specifier, but this shift introduces challenges, primarily sample inefficiency and inability to generalize in multitask settings. Early approaches that decoupled language from control were modular but could not capture fine behaviors (Colas et al. 2020). This leads to end-to-end methods that integrate language directly into the policy loop, which is more expressive, while suffering from poor sample efficiency (Silva et al. 2021). To address this, researchers develop techniques such as memory-based meta-learning (MILLION (Bing et al. 2023a)), exploiting task symmetries for data augmentation (Yao et al. 2023), and translating free-form text into structured predicates (TALAR (Pang et al. 2023)). To achieve richer conditioning, recent works have moved beyond simple feature concatenation, instead using FiLM layers to modulate visual features based on the instruction (LOVM (Ye et al. 2024)), clustering language embeddings to gate reusable skills for lifelong learning 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

17 


**Figure 7.** Typical representations of goals in goal-conditioned learning: vectors, images, and languages (illustration adapted from Liu et al. (2022)). 

(LEGION (Meng et al. 2025a)), and even conditioning the latent dynamics of a world model to shape an agent’s “imagined” futures (LIMT (Aljalbout et al. 2025)). For scaling to hundreds of complex manipulation tasks, a powerful paradigm has emerged: fine-tuning large pretrained behavioral cloning policies with sparse linguistic rewards (FLaRe (Hu et al. 2025a)), and steering the agent’s behavior through a learned language-conditioned value function (V-GPS (Nakamoto et al. 2025)). Although these advances show a clear path toward deeply integrating language into different levels of the RL decision-making process, open challenges remain. These include the reliance on curated reward functions, the high computational and data cost of large-scale pre-training, the inefficient learning of multi-task, and the limited ability to ground nuanced or stylistic language beyond direct commands. 

# _5.2 Language in behavioral cloning_ 

Given the challenges of sample inefficiency and complex reward engineering in RL, an alternative paradigm is to learn policies directly from expert demonstrations. This approach, known as imitation learning, circumvents the difficult exploration problem by training an agent to mimic expert behavior. The most direct form of IL is BC, which frames policy learning as a supervised learning problem: given a dataset of expert trajectories, the goal is to learn a policy _πθ_ ( _at|st_ ) that maps an observation _st_ to the expert’s action _at_ . To address our initial question of _how language can specify robot behavior_ in this field, a direct approach is to treat language instruction _l_ as a conditional input to the imitation learning policy, such that _πθ_ ( _at|st, l_ ). A mainstream strategy for implementing this is to adapt goalconditioned imitation learning frameworks, where language instructions serve as the goal. 

### **Language as goals in goal-conditioned IL** 

Goal-conditioned IL (GCIL) provides a natural foundation for language-conditioned IL. GCIL provides various types of goal conditions for policy learning, including visual and spatial goals, or linguistic goals, as shown in Figure 7. In language-conditioned IL, by replacing abstract goal representations (e.g., state vectors or images) with language instructions, the policy learns to map observations and text to actions. This paradigm shift empowers robots to understand and execute a wide range of commands specified in natural language. A key challenge in this domain is effectively grounding language instructions in visual observations to guide manipulation. Early approaches tackled this by using task-focused visual attention (TFA) 

mechanisms (Abolghasemi et al. 2019; Stepputtis et al. 2020), which directed the vision system to task-relevant regions of an image based on the command, thereby improving manipulation precision. CLIPORT (Shridhar et al. 2022) combines the broad semantic understanding of CLIP with the spatial precision of Transporter (Zeng et al. 2021), solving a variety of language-specified tabletop tasks from packing unseen objects to folding cloths. However, these methods are often constrained by the limited availability of paired action-language data and architectural bottlenecks, which hinder their ability to learn complex multi-step tasks. To overcome the data scarcity problem, some research focus on data-efficient learning and leveraging diverse data sources, such as unstructured data (or play data). Multicontext imitation learning (MCIL) (Lynch and Sermanet 2021) demonstrates that an agent could learn effectively even when less than 1% of the demonstration data is languageannotated, by co-training on multiple goal modalities (task IDs, images, and language). Similarly, BC-Z (Jang et al. 2022) improves data efficiency by learning from a mix of expert demonstrations and cheaper, imperfect interventions. Other works explore alternative data sources entirely, such as MimicPlay (Wang et al. 2023a), which enables robots to learn from videos of humans freely interacting with objects, bypassing the need for costly teleoperated demonstrations. 

Motivated by the architectural bottlenecks of convolutional and recurrent backbones, a second wave of work replaces task-specific backbones with fully-attentional transformers (Vaswani et al. 2017). These works share the intuition that: _if language is inherently sequential and relational, then the action policy should process tokens of words, images and robot proprioception with the same permutation-invariant mechanism_ . HiveFormer (Guhur et al. 2023) asks _“How can a robot remember what it has already done?”_ . To overcome the challenge of _partial observability in multistep tasks_ , HiveFormer concatenates language tokens with all past visual-proprioceptive tokens into a single sequence and processes them with a multimodal Transformer. The resulting history-aware policy improves long-horizon success on 74 RLBench (James et al. 2020) tasks, demonstrating that transformers can scale beyond single images. While in multitask scenarios, learning 3D spatial relationships and 6-DoF actions directly from 2D image projections is challenging. PerAct (Shridhar et al. 2023) mitigates this by framing the problem as “ _detecting the next best voxel action_ ”. It contrastes with earlier image-to-action methods (Shridhar et al. 2022; Jang et al. 2022) by voxelizing both the RGB-D observations and the 6-DoF action space, providing a strong 3D structural prior that proved more data-efficient for complex language-conditioned manipulation. PerAct enables the agent to learn dozens of diverse tasks from only a few demonstrations each. While voxelization provides a powerful 3D inductive bias, it introduces computational challenges, particularly for high-resolution grids needed for precision manipulation tasks. 

To address the computational overhead of dense voxelization, subsequent research explored two main directions. The first path aimed to improve the efficiency and semantic richness of 3D representations. Act3D (Gervet et al. 2023) tackles the computational cost by representing the workspace 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

18 

as a 3D feature field, using a coarse-to-fine attention mechanism to adaptively sample and focus on relevant 3D points rather than processing a dense grid. This allows for highresolution action prediction with a fraction of the compute. In parallel, GNFactor (Ze et al. 2023) argues that existing 3D fields (Driess et al. 2022) lack semantics. It distilled pretrained 2D vision-language models’ features into a generalizable neural feature field, thereby grounding the 3D representation with a deeper understanding of object semantics and functionality. GNFactor transferred to language-conditioned real kitchen tasks with only 100 demonstrations, whereas geometry-only fields struggled with novel objects. 

Concurrent to the development of 3D policies, other research questioned the necessity of explicit voxelization, seeking to inherit the scalability and efficiency of view-based methods while achieving high performance in 3D tasks. Instead of voxelizing space, RVT (Goyal et al. 2023) re-renders the point cloud from 8-16 virtual cameras and applies a multiview ViT (Dosovitskiy et al. 2021) with cross-view attention. This approach trained 36x faster than PerAct (Shridhar et al. 2023) for achieving the same performance in languageconditioned RLBench tasks, showing that clever view selection can replace heavy 3-D convolutions. Building on this multi-view paradigm, Σ-agent (Ma et al. 2025) revisits data efficiency by introducing Contrastive Imitation Learning, adding an auxiliary contrastive loss to the standard BC objective. It pulls together embeddings of visionlanguage pairs from the same task and pushs apart others in the feature space, outperforming RVT (Goyal et al. 2023) in multi-task settings. While these methods advanced the stateof-the-art for rigid object manipulation, they still struggled with deformable objects. To address this, Deng et al. (2024) propose a model that encodes cloth as a graph and uses a transformer to reason jointly over pixels, graph nodes, and language instructions, improving performance on complex cloth manipulation tasks. 

Pushing the boundaries of what language-conditioned IL could achieve, some work explores long-horizon manipulations. In a long-horizon task setting, the robot needs to solve complex manipulation tasks by understanding a series of unconstrained language expressions in a row, for example, “ _open the drawer → pick up the blue block → push the block into the drawer → open the sliding door_ ” (Mees et al. 2022b). Integrating the advantages of data-source improvements and architectural innovations. Some work empowers the language-conditioned policy to solve long-horizon manipulations. For example, HULC (Mees et al. 2022a) introduces a transformer-based architecture with contrastive learning to create more robust language-conditioned representations. This is later extended by HULC++ (Mees et al. 2023), which integrates visual affordance models and leverages LLMs for long-horizon planning. Moreover, to enhance generalization to novel scenarios, SPIL (Zhou et al. 2024a) builds upon the HULC framework by incorporating pre-trained skill priors, allowing the agent to better adapt to unfamiliar environments. 

However, an inherent issue in BC is compounding error, hindering learning language-conditioned policies to solve long-horizon manipulation tasks. To mitigate the issue of 

compounding error, ACT (Zhao et al. 2023a) introduces _action chunking_ , which predicts sequences of actions at a time, and uses temporal ensembling to improve robustness. Building on this idea, MT-ACT (Bharadhwaj et al. 2024) trains a language-conditioned policy using a multitask action-chunking transformer architecture, leveraging efficient action representations for ingesting multi-modal multitask data into a single policy. Some researchers believe that for long-horizon high-precision tasks like autonomous surgery, a simple end-to-end policy is insufficient. SRTH (Kim et al. 2025a) introduces a hierarchical framework where a high-level Transformer policy generates language instructions (e.g., corrective ones) to guide a low-level policy, enabling robust multi-step execution and linguistic error correction in realistic surgical settings. 

In summary, using language as a direct policy condition in BC has evolved, addressing challenges like data scarcity and long-horizon task execution. Early methods focused on grounding language in visual observations using task-focused attention mechanisms (Abolghasemi et al. 2019; Stepputtis et al. 2020) and combining pre-trained vision-language models with spatial reasoning (Shridhar et al. 2022). To overcome data scarcity, approaches like MCIL (Lynch and Sermanet 2021) and BC-Z (Jang et al. 2022) demonstrate effective learning from limited languageannotated data and imperfect interventions, while MimicPlay (Wang et al. 2023a) leverages unstructured human interaction videos. The adoption of transformer architectures (Vaswani et al. 2017) enables models like HiveFormer (Guhur et al. 2023) to handle partial observability in multi-step tasks by attending over entire action histories, and PerAct (Shridhar et al. 2023) to learn 6-DoF actions from voxelized 3D spaces. To address the computational challenges of dense voxelization, subsequent works pursued more efficient 3D representations (Act3D (Gervet et al. 2023), GNFactor (Ze et al. 2023)) and multi-view approaches (RVT (Goyal et al. 2023), Σ-agent (Ma et al. 2025)). For long-horizon tasks, innovations like HULC (Mees et al. 2022a), SPIL (Zhou et al. 2024a) introduce latentrepresentation and skill-prior mechanisms for maintaining long-term context. Hierarchical frameworks like SRTH (Kim et al. 2025a) further enhance robustness by combining high-level language planning with low-level execution. These works demonstrate that deeply integrating language into BC policies can enable robots to perform complex multistep tasks specified in natural language. However, challenges remain in scaling to more diverse tasks, improving data efficiency, and enhancing the robustness of learned policies. 

# _5.3 Language in diffusion-based policy learning_ 

While traditional imitation learning methods like BC have been successful, they may struggle with tasks that exhibit multi-modal action distributions, where multiple valid action sequences can achieve the same goal. Methods that rely on direct regression, mixtures of Gaussian (Mandlekar et al. 2022), or discretization (Shafiullah et al. 2022) perform poorly on this problem, as illustrated in Figure 8(a). 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

19 


**Figure 8.** (a) Explicit policy in imitation learning. (b) Diffusion process (modified from Diffusion Policy (Chi et al. 2023)). 

For example, the regression methods, such as using a Mean Squared Error (MSE) loss (Torabi et al. 2018), tend to average these diverse expert behaviors, resulting in conservative or even invalid actions (Chi et al. 2023). To overcome this limitation, generative models have been introduced into this field, which are adept at learning complex high-dimensional data distributions. Among these, diffusion models have emerged as a powerful and stable alternative to Generative Adversarial Networks (Srivastava et al. 2017) and energy-based models (Florence et al. 2022), offering a robust framework for modeling expressive and multi-modal robot behavior (Urain et al. 2024). 

The core of a diffusion-based policy is a two-stage process, as illustrated in Figure 8(b). In the forward (diffusion) phase, Gaussian noise is incrementally added to expert action data over a series of timesteps, gradually corrupting it into pure noise. The model, typically a noise-prediction network, is then trained to reverse this process. In the reverse (denoising) phase at inference time, the model starts with random noise and iteratively refines it over a sequence of steps, conditioned on the current state observation, to generate a clean, executable action sequence (Chi et al. 2023; Ho et al. 2020). This generative paradigm has proven highly effective and has been applied to a wide array of robotic manipulation applications, including visual-motor control (Pearce et al. 2022; Chi et al. 2023; Scheikl et al. 2024; Octo Model Team et al. 2024; Di Palo and Johns 2024; Dasari et al. 2025), tasks in 3D scenes (Xian et al. 2023; Yan et al. 2024; Vosylius et al. 2024; Ze et al. 2024; Lu et al. 2024), human-robot interactions(Ng et al. 2023; Wang et al. 2025d), cross-embodiment transfer (Yao et al. 2025b,c), contact-rich manipulation (Xue et al. 2025), longhorizon planning (Mishra et al. 2023), and robust control (Hu et al. 2026). 

To direct the generation process toward specific goals, the denoising network can be conditioned on additional information not just observations (robot states and scene context). By incorporating language instructions as a condition, these models become language-conditioned diffusion policies. This allows a single policy to generate behaviors for a wide range of tasks specified by text. The language instruction, along with the visual observation, guides the denoising process, ensuring the generated action sequence is not only physically plausible but also semantically aligned with the command. This approach has been successfully used to learn goal-and-state-conditioned distributions, enabling policies to capture multiple valid 

solutions from demonstration data and solve complex tasks specified by image or language goals (Xian et al. 2023; Reuss et al. 2023; Chen et al. 2023b; Ha et al. 2023; Reuss et al. 2024; Hao et al. 2025; Ke et al. 2025), even for unseen objects (Liu et al. 2023c). In the following, we will discuss the integration and role of language instructions in this field. 

A challenge in this area was bridging high-level abstract language commands with low-level physically-valid robot actions. To overcome the challenge of grounding language in physically plausible scene arrangements, StructDiffusion (Liu et al. 2023c) introduced language as a high-level constraint, such as “ _Set the table in the center left, relative to you_ ”, to guide an object-centric language-conditioned diffusion model to sample diverse and collision-free goal poses for multiple objects, even those unseen during training. The method’s performance is limited by subsequent lowlevel goal-conditioned policies. This highlights the need for policies that could produce complete trajectories with numerous high-quality expert demonstrations, while bringing a new bottleneck: such demonstrations are expensive to collect, and unstructured data (“play” data) is plentiful but noisy. A key line of research is the need for greater data efficiency and scalability. For example, Scaling&Distilling (Ha et al. 2023) leverages an LLM to propose textual subtasks, executes them in simulation, and _distils_ the successful trajectories into a compact language-conditioned diffusion policy. ChainedDiffuser (Xian et al. 2023) utilizes language guides a global transformer to predict a sequence of discrete keyposes, and a local trajectory diffuser then generates smooth motion segments to connect them, unifying keypose prediction with trajectory diffusion to solve long-horizon tasks. 

Alternatively, LCD (Zhang et al. 2024a) tackles longhorizon tasks by employing a diffusion model as a highlevel planner that operates in a learned low-dimensional latent space. Language instructions guide this planner to generate a sequence of abstract goal states for execution. Chen et al. (2023b); Ju et al. (2024); Wu et al. (2025a) explore to learn policies in a more generalizable and reusable manner, aiming to discover and disentangle fundamental skills. PlayFusion (Chen et al. 2023b) introduces a skill discovery scheme, which treats language-annotated play as weak supervision. A conditional diffusion model segments free-play trajectories into latent _skills_ that are managed via a discrete codebook. These skills can later be recombined when given a new language instruction. Similarly, Ju et al. (2024) and Wu et al. (2025a) propose leveraging vector quantization (VQ) to map continuous action sequences into a discrete latent skill space, guided by language instructions. Whereas StructDiffusion (Liu et al. 2023c) focuses on singlestep goal sampling, sequential works expand language’s role to _self-supervised data curation_ (Ha et al. 2023), _skill composition_ (Chen et al. 2023b; Ju et al. 2024; Wu et al. 2025a), and _long-term plan decomposing_ (Xian et al. 2023; Zhang et al. 2024a), improving data and computational efficiency. 

For language-conditioned diffusion policies to be practical in the real world, they must overcome several challenges related to data heterogeneity and deployment constraints. A primary issue is handling diverse data sources, such as 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

20 

simulations, different robot platforms, and human videos. To address this, PoCo (Wang et al. 2024c) formulates policy composition as a conditional diffusion problem, allowing it to combine multiple pre-trained policies with language guidance, thus avoiding the difficulty of training a single model on disparate data distributions. Another challenge is cross-embodiment transfer. RoLD (Tan et al. 2024) tackles this by first pre-training a task-agnostic autoencoder to create a unified latent action space. A language-conditioned diffusion policy is then trained within this compact space, enabling effective knowledge transfer across different robot platforms. Furthermore, real-world datasets often have sparse or missing language annotations. To handle this, methods like MDT (Reuss et al. 2024) and GR-MG (Li et al. 2025b) are designed to accept multimodal goals (e.g., language or images). GR-MG, for instance, uses the language instruction to generate a corresponding goal image with a diffusion model, then conditions its policy on both modalities for increased robustness. While these methods improve data efficiency and generalization, a fundamental architectural bottleneck remains: the high inference latency of the iterative denoising process, which is often prohibitive for real-time control. Although not language-conditioned, other works offer potential solutions; for example, some methods (Lu et al. 2024; Prasad et al. 2024) impose consistency constraints on the diffusion process to enable low-latency decision-making, suggesting a promising direction for future language-conditioned models. 

In summary, the integration of language into diffusionbased policy learning transforms the generative process from simply modeling multi-modal action distributions to directing it toward specific, semantically meaningful goals. This addresses a core limitation of regressionbased methods, which tend to average out diverse expert behaviors. Early works using language as a high-level constraint for single-step goal sampling (Liu et al. 2023c), while relying on separate low-level controllers for execution. Researchers leveraged language for more sophisticated, structured learning paradigms, including selfsupervised data curation (Ha et al. 2023), hierarchical plan decomposition (Xian et al. 2023; Zhang et al. 2024a), and skill discovery and composition (Chen et al. 2023b; Ju et al. 2024; Wu et al. 2025a). To enhance the practicality of diffusion model-based policies for real-world applications, recent work has used language to tackle challenges of data heterogeneity and sparse annotation. This includes using language to guide the composition of multiple pre-trained policies (Wang et al. 2024c), enabling cross-embodiment transfer via shared latent spaces (Tan et al. 2024), and designing multimodal goal representations (Reuss et al. 2024; Li et al. 2025b) that can handle missing or imperfect language inputs (Li et al. 2025b). Although these advancements demonstrate a clear trajectory toward using language for structured and efficient learning, an open challenge remains: the inherent inference latency of the iterative denoising process of the diffusion models, which is a bottleneck for real-time robot control. 

# _5.4 Summary_ 

When used as a policy condition, language shifts from quantifying “ _task progress_ ” to dictating “ _how to do it_ ”. In this paradigm, language serves as a direct input to policy, mapping observations and instructions to actions. This approach has been explored across RL, BC, and DP, each offering distinct advantages and challenges. In RL, conditioning the policy on language helps address sample inefficiency and multi-task generalization by enabling more structured learning, such as through memory-based meta-learning (Bing et al. 2023a) or by shaping the latent dynamics of a world model (Aljalbout et al. 2025). In BC, language-conditioned policies learn directly from expert demonstrations, circumventing the need for reward engineering and enabling complex long-horizon manipulations (Mees et al. 2022a; Zhou et al. 2024a; Kim et al. 2025a). However, standard regression-based BC methods struggle with multi-modal behaviors, often averaging diverse expert actions into a single, suboptimal output. Diffusion-based policies mitigate this by using generative models to capture the full distribution of expert behaviors, with language guiding the generation process toward the intended goal. Across all three learning paradigms, there is a clear progression from simple feature conditioning toward more deeply integrated roles for language. This includes using language to modulate visual features (Ye et al. 2024), guide hierarchical planning (Mees et al. 2022a; Zhou et al. 2024a; Kim et al. 2025a), and structure the learning process itself (Zhang et al. 2024a; Wang et al. 2024c; Tan et al. 2024), leading to more data-efficient, generalizable, and expressive robotic manipulation. A key remaining challenge, particularly for diffusion policies, is their inference latency, which can be a bottleneck for real-time control. 

# **6 Language for cognitive planning and reasoning** 


**Figure 9.** Taxonomy of Sec. 6 Language for cognitive planning and reasoning. 

The previous sections explore how language can quantify _task progress_ (state evaluation in Sec. 4) or _how_ to do it (policy conditioning in Sec. 5). In both paradigms, language serves as an external instruction that guides the 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

21 

robot’s low-level behavior. This section explores a more cognitive role for language, utilizing it as an internal tool for reasoning and planning. We now turn to our third key research question: _How can a robot “think” in language to structure its own behavior?_ This involves leveraging language not just to follow commands, but to reason about the world, decompose complex problems reasonably, and formulate strategies, enabling more autonomous and intelligent manipulation in real-world environments. This perspective is inspired by cognitive science, which posits that human language comprehension is dually embodied and symbolic (Louwerse and Jeuniaux 2008). While embodied approaches connect language to human’s perceptual and motor experiences (Goldin-Meadow 2005) (much like a robot policy grounds “grasp the cup” in sensorimotor control), symbolic approaches highlight that language also derives meaning from the abstract interdependencies between words (Kintsch 1998). This symbolic structure allows humans to reason efficiently, providing a “shortcut” to meaning without needing to constantly simulate every physical detail (Louwerse and Jeuniaux 2008). 

This cognitive duality mirrors a fundamental challenge and a corresponding solution in artificial intelligence. On one hand, neural systems excel at perceptual intelligence, learning directly from unstructured data (e.g., images, videos, or texts). Their information processing units are typically vectors, inherently lacking explicit reasoning capabilities. On the other hand, symbolic systems offer powerful, interpretable reasoning but are brittle when faced with noisy, real-world sensory input (Yu et al. 2023a). An ideal solution is a hybrid approach that combines the strengths of both: neural-symbolic learning systems (Besold et al. 2021; Yu et al. 2023a). Following the idea of these frameworks, in the field of language-conditioned robotic manipulation, language serves as the bridge that connects the neural and symbolic components, grounding abstract symbols in perceptual reality, enhancing both interpretability and robustness of the robot policies. This section will delve into approaches that leverage this paradigm, exploring both classic neural-symbolic methods and the recent emergence of Foundation Models (LLMs, VLMs, VLAs) as powerful engines for task planning and reasoning in robotics. 

Figure 9 displays the taxonomy of this section. Moreover, to synthesize the diverse approaches that enable robots to use language as an internal tool to reason, decompose problems, and structure their behavior, Table 4 provides a detailed comparison of the cognitive planning and reasoning methods reviewed in this section. These methods are categorized based on the type of cognitive system employed to bridge _abstract textual reasoning_ with _perceptual reality_ . The table spans classic neuro-symbolic frameworks to modern paradigms empowered by the broad openvocabulary reasoning priors of Large Language Models and the grounded perception of Vision-Language Models. This side-by-side comparison emphasizes how each reasoning mechanism balances interpretability and structural rigor against scalability constraints and hallucination risks. 

# _6.1 Classic neuro-symbolic approaches_ 

Neuro-symbolic artificial intelligence (Besold et al. 2021), combining both neural and symbolic traditions to solve tasks, continually develops alongside popular data-driven machine-learning approaches. In this context, “neuro” refers to neural networks, while “symbolic” refers to high-level (human-readable) representations like logic or graphs. In the field of robot manipulation, integrating neural and symbolic approaches can enhance the robot’s reasoning capabilities and the interpretability of its decisions by grounding abstract knowledge in the robot’s perceptual world. This section discusses key neuro-symbolic methods in language-conditioned manipulation, categorized according to the framework by Yu et al. (2023a), namely _Learning for reasoning_ , _Reasoning for learning_ , and _Learning-reasoning_ . 

### _6.1.1 Learning for reasoning_ 

In this category, neural networks serve as perception and feature extraction modules, converting unstructured data (e.g., images, language) into symbolic representations. A separate symbolic system then uses these symbols to perform high-level reasoning and planning. An early system proposed by Tenorth et al. (2010) sourced task knowledge from websites like wikiHow. It parsed natural language and used knowledge bases like WordNet (Fellbaum 1998) and Cyc ontology (Matuszek et al. 2006) to resolve word senses and map them to a formal logic representation, generating a symbolic plan. This plan was then translated into an executable language for the robot’s planner for further optimization. She et al. (2014) present a framework where a robotic arm learns new highlevel actions through natural language. Their system first processes human instructions into a symbolic “Grounded Action Frame” by parsing the language and grounding it to objects perceived in the environment. This symbolic representation allows a classic STRIPS (Fikes and Nilsson 1971) planner to dynamically generate new sequences of primitive movements to accomplish the learned action in novel and more complex situations, demonstrating flexible application of the acquired knowledge. 

HiTUT (Zhang and Chai 2021) uses a unified transformer architecture to learn a hierarchical task structure from language and vision. Language is provided at two levels of granularity: high-level goal instructions guide subgoal planning, while low-level step-by-step instructions inform navigation and manipulation actions. The neural model extracts task components from these inputs, enabling hierarchical planning. DANLI (Zhang et al. 2022) operates on a task-oriented dialogue history between a human commander and the robot. Its neural component, a “task monitor”, processes the dialogue and action history to extract symbolic sub-goals, representing both completed and future steps. A traditional symbolic planner then uses these sub-goals and a dynamically built semantic map of the environment to generate low-level action plans, allowing the agent to reason about its progress and recover from errors. Bartoli et al. (2022) focuses on long-term, incremental knowledge acquisition through human-robot interaction. Here, language serves as a verification and correction tool. The robot makes a prediction about a perceived object and 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

22 

**Table 4.** Comparison of representative state-of-the-art methods for **Section 6 Language for cognitive planning and reasoning** . By contrasting classic neuro-symbolic systems with modern LLM- and VLM-empowered approaches , this table summarizes the key mechanisms, advantages, and limitations of using language to internally structure robot behavior and bridge abstract reasoning with perceptual reality. 

|**Method**|**Cognitive**<br>**System**|**Reasoning Mechanism**|**Key Advantages**|**Key Disadvantages**|
|---|---|---|---|---|
|DANLI<br>(Zhang<br>et<br>al.<br>2022)|Classic<br>Neuro-<br>symbolic|Learning for reasoning via<br>dialogue history and sym-<br>bolic sub-goals.|Allows the agent to reason<br>about progress and dynami-<br>cally recover from errors.|Relies<br>on<br>labor-intensive,<br>task-specific<br>Knowledge<br>Graph construction.|
|SayCan<br>(Brohan<br>et<br>al.<br>2023b)|LLM-<br>Empowered|Open-loop<br>planning<br>integrated with affordance<br>functions.|Translates natural language<br>into<br>semantically<br>relevant<br>and<br>physically<br>feasible<br>action sequences.|Assumes faultless skill exe-<br>cution and lacks real-time<br>feedback for replanning.|
|SayPlan<br>(Rana<br>et<br>al.<br>2023)|LLM-<br>Empowered|Closed-loop planning via 3D<br>scene graphs and semantic<br>simulators.|Operates<br>successfully<br>in<br>large-scale environments by<br>providing continuous textual<br>feedback.|Performance remains capped<br>by the underlying LLM’s<br>reasoning<br>capabilities<br>and<br>potential latency.|
|Code as Policies<br>(Liang<br>et<br>al.<br>2023)|LLM-<br>Empowered|Auto-regressive code gener-<br>ation for orchestrating policy<br>logic.|Flexibly<br>recomposes<br>API<br>calls to generalize better to<br>unseen objects.|Code-generation<br>LLMs<br>struggle<br>with<br>complex<br>commands<br>and<br>may<br>call<br>nonexistent functions.|
|PaLM-E<br>(Driess<br>et<br>al.<br>2023)|VLM-<br>Empowered|Text generation via a mas-<br>sive, single embodied rea-<br>soning model.|Translates high-level com-<br>mands into robot-executable<br>plans with little or no robot-<br>task-specific<br>finetuning<br>in<br>some evaluated settings.|Highly resource-intensive to<br>deploy and run.|
|SuSIE<br>(Black<br>et<br>al.<br>2024)|VLM-<br>Empowered|Image generation for visual-<br>izing sequential subgoals.|Decouples high-level seman-<br>tic understanding from low-<br>level control optimization.|Generated images can con-<br>tain physically implausible<br>details, creating unreliable<br>control signals.|
|LEMMo-Plan<br>(Chen<br>et<br>al.<br>2025b)|LLMs-driven<br>structured<br>planning<br>(Symbolic)|Incorporates<br>multi-modal<br>demonstrations<br>(tactile<br>and force-torque data) into<br>PDDL symbolic planning.|Allows the LLM to rea-<br>son about “invisible” events<br>like cable tension, defining<br>robust force-based skill con-<br>ditions.|Integrating<br>LLMs<br>with<br>PDDL can introduce slow<br>symbolic<br>search<br>speeds,<br>delaying robot action.|
|BETR-<br>XP-LLM<br>(Styrud<br>et<br>al.<br>2025)|LLMs-driven<br>structured<br>planning<br>(Behavior<br>Trees)|Casts the LLM as a “repair<br>agent” to propose minimal<br>preconditions and matching<br>subtrees for execution fail-<br>ures|Permanently integrates ver-<br>ifiable fixes into the pol-<br>icy, making the robot more<br>robust with every failure.|Relying on LLMs for run-<br>time feedback and replan-<br>ning<br>increases<br>token<br>and<br>latency costs.|


asks the human a direct question (e.g., “ _Is it true that this bottle has material metal?_ ”). The human’s verbal response (“ _Yes_ ”, “ _No_ ”, or a correction like “ _Plastic_ ”) is used to directly update the robot’s knowledge graph. This approach uses Knowledge Graph Embeddings and Continual Learning to generalize from human-provided feedback and prevent catastrophic forgetting over long interaction periods. 

### _6.1.2 Reasoning for learning_ 

_Reasoning for Learning_ indicates that the symbolic system provides structure, rules, or knowledge that constrains and guides a neural network’s learning process or decisionmaking. The final output is typically generated by the neural component, but its behavior is shaped by symbolic reasoning. Misra et al. (2016) propose a model that grounds free-form natural language instructions in a robot’s environment. The language is first parsed into an intermediate symbolic representation of “verb clauses”. Symbolic domain knowledge, encoded in the STRIPS formal language (Fikes and Nilsson 1971), provides preconditions and effects for robot actions. This symbolic knowledge 

is integrated into a trainable energy function, modeled as a Conditional Random Field (Sutton et al. 2012), which learns to map the verb clauses to a valid sequence of executable controller instructions that respects both the language command and the physical constraints of the world. Nguyen et al. (2019) integrate the prior knowledge in KG, capturing spatial relationships between target objects, with the visual and textual information of observation and language instructions to enhance the agent’s generalization ability in unseen environments. Silver et al. (2023) learn neuro-symbolic skills from demonstrations without direct language commands during training. Instead, the symbolic system provides a predefined “language” of symbolic predicates (e.g., Grasped, Pressed) that structure the learning process. The system learns symbolic operators alongside neural policies and subgoal samplers from demonstrated trajectories. At test time, a bilevel planner uses these learned skills to solve new tasks specified by a formal symbolic goal, demonstrating how symbolic reasoning structures both learning and planning. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

23 

### _6.1.3 Learning-reasoning approaches_ 

This category includes integrated systems where neural and symbolic components work in a tight loop, mutually informing and enhancing each other to produce the final results. Both neural and symbolic components are critical to the reasoning process. Chai et al. (2018) introduce an Interactive Task Learning framework that incorporates language into a rich, interactive dialogue between a human and a robot, complemented by physical demonstrations. A key concept is learning the physical causality of action verbs (e.g., the action “slice” results in the state “in pieces”) to bridge symbolic actions and their perceptual outcomes (Gao et al. 2016). A hypothesis space of such verb representations can be acquired incrementally through continuous interaction with the environment (She and Chai 2016). As the world is full of uncertainties, a dialogue policy can be learned to better capture the connection between symbolic representations and the perception from the world (She and Chai 2017). Through this interaction, the agent simultaneously learns a grounded symbolic task structure and improves its perceptual understanding of causeand-effect of actions, showing how neural and symbolic representations can _co-develop_ (Gao et al. 2018). 

K et al. (2023) propose a system that translates natural language instructions into executable programs. First, a symbolic Language Reasoner parses the instruction into a hierarchical program using a Domain-Specific Language. This symbolic program is then executed by a neural Visual Reasoner, which operates on neural object-centric representations of the scene to ground the program’s symbols (e.g., “the red block”) to specific objects. Finally, a neural Action Simulator predicts the physical outcome of the grounded actions. This architecture creates a tight loop where symbolic parsing guides neural grounding, which in turn informs neural prediction. Miao et al. (2023) use a vision module, which takes the RGB images of the scene as input and predicts the labels, bounding boxes, and relation predicate labels of all entities to generate a scene graph. Then, the generated scene graph is utilized as the input of the regression planning network (Xu et al. 2019) and the task instructions to output intermediate goals (plan). 

In summary, language instructions in the above parallels serve different roles. In _learning-for-reasoning_ , language specifies task structure and entities that the symbolic layer reasons over. In _reasoning-for-learning_ , language instantiates symbolic predicates or constraints that steer neural learning toward logically valid behaviors. In _learningreasoning_ , language facilitates an interplay between symbolic and neural components, enhancing both learning and reasoning capabilities of the robot policy. While these classic neuro-symbolic frameworks provide interpretable and structured reasoning for robotic manipulation, they also face several limitations that can hinder their application in complex real-world environments, mainly including: 

- **Labor-intensive KG construction:** Approaches like DANLI (Zhang et al. 2022) or KGE-based continual learning (Bartoli et al. 2022) presuppose a task-specific KG. Populating and maintaining these graphs quickly 

becomes a bottleneck in dynamic open-world settings where new objects and relations may appear frequently. 

- **Manual symbol engineering and ontology drift:** The above systems rely on a hand-crafted inventory of symbols (such as object types (Bartoli et al. 2022; Kwak et al. 2022), predicates (Misra et al. 2016; Silver et al. 2023), operators (Chai et al. 2018)). Extending the ontology to new domains requires human curation, ontology alignment, and often re-training of perception modules. 

- **Limited coverage of commonsense and real-world knowledge:** Symbolic rules capture only what has been explicitly encoded. They lack the broad background knowledge, such as object materials, physical affordance, social conventions, and other contextual factors needed for robust behavior in unstructured environments. 

- **Scaling issues in long-horizon tasks:** As plan length grows, search over discrete operators and grounding choices explodes combinatorially, leading to slow inference or heavy reliance on humans’ sub-goal supervision (Zhang et al. 2022). 

# _6.2 Empowered by large language models_ 


**Figure 10.** Illustration of approaches empowered by LLMs. 

The limitations of classic neuro-symbolic methods listed above stem from the fact that classic pipelines rely on _explicitly engineered_ symbolic knowledge. Recent _foundation models_ , particularly LLMs, offer a complementary path. Trained on trillions of tokens of numerous unstructured data (such as internet text) (Naveed et al. 2025), LLMs encode broad textual priors and often exhibit useful instructionfollowing, commonsense understanding, and contextual reasoning without domain-specific retraining. Famous LLMs like GPT-families (Brown et al. 2020; Achiam et al. 2023; Hurst et al. 2024), Claude (Bai et al. 2022), LLaMA-2 (Touvron et al. 2023), Gemini (Team et al. 2023), DeepSeekR1 (Guo et al. 2025), and Qwen3 (Yang et al. 2025a). Instead of extending a hand-written ontology, one can _prompt_ the model in natural language (or provide a few demonstrations (Gao et al. 2023)) to obtain a structured plan, a piece of executable code, or a step-by-step chain-of-thought reasoning (Wei et al. 2022). 

This capability allows LLMs to serve as a powerful tool that combines planner and reasoner for language-conditioned 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

24 

robots, bridging the gap between high-level human intent and a plausible sequence of executable steps. Early work in this area demonstrated this potential by using LLMs as task planners. For example, Saycan (Brohan et al. 2023b) translates natural language instructions into intermediate action sequences. When combined with affordance functions that ground these actions in the robot’s current environment, LLMs can generate behaviors that are both semantically relevant and physically feasible. Subsequent research has expanded on this, leveraging LLMs to solve a diverse set of long-horizon manipulation tasks in large-scale (Rana et al. 2023) or open-ended environments like Minecraft (Wang et al. 2023c). More generally, the pattern recognition abilities of LLMs can be exploited beyond just language-based reasoning by converting robot observations and actions to numerical text (Di Palo and Johns 2024). 

While LLMs address many of the scalability issues of classic methods for robotic manipulation, they introduce their own potential and non-negligible issues. 

- **The grounding problem** : LLMs are prone to confidently hallucinate predictions (Rana et al. 2023), and generate a plausible but not feasible plan (Brohan et al. 2023b; Singh et al. 2023), because LLMs will plan an action involving objects unavailable in the real environment (Huang et al. 2022). 

- **Ambiguity in language** : Natural language is highly ambiguous, especially in expressing spatial and geometrical relationships such as “ _moving faster_ ” or “ _placing objects slightly left_ ” (Liang et al. 2023; Mees and Burgard 2021; Mees et al. 2020, 2017). 

- **Lack of feedback and reactivity** : When operating as open-loop planners, LLMs are not inherently aware of the outcomes of their proposed actions. They can generate unsafe plans (e.g., putting metal in a microwave) and cannot dynamically replan when an action fails without a corrective mechanism to provide real-time feedback (Ren et al. 2023a). 

The following sections will review how recent works in robot manipulation are addressing these challenges, categorizing methods based on how they leverage LLMs for planning and reasoning, as illustrated in Figure 10. Furthermore, we explore the methods that combine LLMs with symbolic systems to achieve interpretable task planning and reasoning. 

### _6.2.1 Planning_ 

Planning refers to a process wherein an agent decomposes a high-level task into subgoals or sequences, which are a set of learned actions to accomplish a specific objective (Rana et al. 2023). Recent research has highlighted the remarkable capabilities of LLMs in planning tasks, including semantic classification, common-sense reasoning, and contextual understanding. These capabilities can potentially be harnessed by embodied agents for task planning. Huang et al. (2022) posit that LLMs inherently possess the knowledge required to achieve goals without further training. Specifically, pre-trained autoregressive LLMs necessitate only minimal prompts (Wang et al. 2023c; Singh et al. 2023; Ren et al. 2023a; Ding et al. 2023) or 


**Figure 11.** (a) Open-loop models guide planning with auxiliary information. (b) Closed loop update planning with state feedback. 

no prompts at all (Brohan et al. 2023b; Huang et al. 2022) to generate coherent plans expressed in natural language. In contrast, traditional learning-based planning methods rely on intricate heuristics (Vallati et al. 2015) and extensive training datasets (Ceola et al. 2019). Collecting such vast data is often prohibitive, especially for diverse tasks and unpredictable real-world scenarios. 

However, pre-trained LLMs encode a large amount of task-agnostic knowledge and lack state feedback from the environment, which leads to task planning with LLMs often struggling with the hallucination issue. LLMs tend to generate plausible but infeasible plans, such as an action involving an unavailable object in the environment (Brohan et al. 2023b; Singh et al. 2023). Ding et al. (2022) mention that grounding domain-independent knowledge into a specific domain with many domain-relevant constraints is challenging for task planning with LLMs. Therefore, we ask: _how to ground planning into the environment?_ i.e., _how to enable LLMs to generate more feasible plans and executable actions?_ Recent works integrate LLM with external components or leverage the code generation capability of LLM to remedy these problems. Here, we discuss _open-loop_ and _closed-loop_ planning. Figure 11 demonstrates the overall process of both approaches. 

## **Open-loop planning** 

In recent years, many researchers have designed LLMbased planners that integrate LLMs with different external components. These external components can provide LLMs with additional input information or embodied feedback from the environment, thus ensuring the output actions adhere to the constraints and achieve the goal. Brohan et al. (2023b) leverage the affordance function to quantify the success rate of each action in the current state, and LLMs reorder the set of predicted actions and output the most accessible action. Ren et al. (2023a) combine LLMs with conformal prediction to measure and align uncertainty. LLM planning can be formulated as multiple-choice Q&A. It generates a series of candidate actions in the next step. Then, LLMs choose the correct options by a conformal prediction threshold calculated based on a user-specified success rate. If the robot cannot select the only correct option, it will ask humans for help, thus aligning the uncertainty, e.g., “ _Put a plastic bowl in the microwave_ ” and “ _Put a metal bowl in the microwave_ ” for the task “ _Heating_ 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

25 

_up the food_ ”. Moreover, Huang et al. (2022) let two pretrained LLMs play different roles in task planning. A pretrained causal LLM decomposes the high-level task into a sensible mid-level action plan. The other pre-trained masked LLMs leverage semantic similarity to translate these midlevel actions into admissible learned actions, e.g., translating the action “ _squeeze out a glob of lotion_ ” into “ _pour the lotion into right hand_ ”. Wu et al. (2023c) utilize CLIP (Radford et al. 2021) and a masked RCNN as an open-vocabulary object detector to collect multiple RGB images and predict a list of objects existing in the scene, showcasing the openloop model guide planning with auxiliary information and mitigating the issues of LLMs to generate multi-step actions involving unavailable objects in the specific environment. 

Nevertheless, these prior approaches still cannot solve the long-horizon tasks successfully, which is caused by two major issues. Firstly, the prior approaches adopt shortterm or open-loop execution strategies, trusting LLMs to generate the correct strategies without accounting for the geometric dependence over a skill sequence (Lin et al. 2023), which is an essential factor in solving long-horizon tasks. Open-loop approaches, like Saycan (Brohan et al. 2023b; Huang et al. 2022; Ren et al. 2023a; Wu et al. 2023c), have distinct planning and control components that are implemented separately. LLMs, as offline planners, never received embodied feedback to reflect on previous executions. Therefore, most open-loop approaches must assume faultless skill execution in solving long-horizon tasks (Brohan et al. 2023b; Huang et al. 2022), or utilizing user cases to constrain the LLM’s planning in specific domains (Singh et al. 2025). These assumptions or constraints limit their scalability and the success rate of solving tasks in a new environment. Secondly, some approaches output a plan that can be viewed as a oneshot plan (Wang et al. 2023c), i.e., the approaches have no replanning function. LLMs lacking state feedback do not replan the generated skill but only focus on reasoning over more accessible skills in the next step. Obviously, it is challenging for these open-loop approaches to generate a flawless one-shot plan that can directly solve long-horizon tasks. On the one hand, various complex preconditions and unforeseen accidents can occur in the real world, making the one-shot plan non-executable easily. On the other hand, many challenging long-horizon tasks, such as household tasks or rearrangement tasks, involve multiple objects and a series of chronologically linked subgoals, making it difficult to cover all of them in a one-shot plan. 

## **Closed-loop planning** 

To address the aforementioned issues, more recent studies (Lin et al. 2023; Zhao et al. 2023b; Jin et al. 2023; Chalvatzaki et al. 2023) integrate LLMs with external components in a closed loop, where these external components can provide embodied state feedback to LLMs. Then, LLMs can constantly replan more executable skills until the plan succeeds completely. This iterative replanning leverages the strong contextual reasoning of LLMs and continuous feedback through the closed loop to improve the scalability and generalizability (Rana et al. 2023; Ha et al. 2023). For example, compared to Saycan (Brohan et al. 2023b), which only accomplishes tasks in kitchen 

scenarios, Sayplan (Rana et al. 2023) operates in a largerscale environment that covers almost all daily office scenarios. Specifically, Sayplan leverages a hierarchical 3D scene graph to represent the environment, while a scene graph simulator generates textual feedback to LLMs, combining the scene graph’s predicates, current states, and affordances to enhance the planning process. Lin et al. (2023) propose Text2Motion to leverage Sequencing Task-Agnostic Policies (STAP) (Agia et al. 2023) as geometric feasibility approaches. LLMs will plan a new skill if STAP finds the previous plan failing to adhere to geometric dependence. Jin et al. (2023) and Huang et al. (2023c) utilize a pretrained visual transformer as a scene descriptor, which can translate visual observations into real-time textual feedback for LLMs. Kwon et al. (2024) show that a single taskagnostic prompt could predict dense robot end-effector trajectories with closed-loop feedback to check performance and correct trajectories where necessary. With an innerfeedback mechanism, Wu et al. (2025b) propose SELP to mitigate hallucination issues of LLMs for long-horizon tasks (i.g. producing unfeasible or unsafe plans), which incorporates Linear Temporal Logic (LTL) formulation to prune out LLM’s unsafe plans, adhere the plan to follow the temporal constraint of natural language commands, and allow replanning when no valid plan exists. However, this method relies on a predefined LTL specification for specific environments, which limits its flexibility. Moreover, Asuzu et al. (2025) incorporate continuous human user feedback into the LLM planning process, which forms a closed-loop corrective mechanism to refine the LLM plans. 

### _6.2.2 Reasoning_ 

In general, reasoning refers to the ability of a policy to mimic human-like thinking and make inferences using observation embedding or external information. In robot manipulation, planning and reasoning are two crucial capabilities that embodied agents use to solve multi-step and long-horizon tasks. They are distinct but highly interconnected. Feasible reasoning at each step ensures the generation of an executable action plan, i.e., the reasoning is a prerequisite for planning. Some prior surveys do not make a clear distinction between planning and reasoning (Tellex et al. 2020; Cohen et al. 2024). In our work, we categorize them into two different sections. In section _Planning_ (§6.2.1), many works are developed for a closed world, assuming that complete knowledge of the world is provided and the agent can enumerate all possible states (Ding et al. 2022). LLM-based models utilizing auxiliary information (Brohan et al. 2023b; Ding et al. 2023) or feedback (Wang et al. 2023c; Lin et al. 2023; Jin et al. 2023) to solve spatial and geometric dependencies in action sequences. For unseen objects, LLM-based planners are trained to avoid them rather than to generalize them. Meanwhile, many other researchers (Ding et al. 2022; Kant et al. 2022) operate their agents in an open world, leveraging different types of reasoning to improve the generalizability of unseen objects or instructions. They improve the agent’s performance by making it robust to unforeseen situations. We categorize these works into summarization, prompt engineering, and code generation in this section. 

## **Summarization** 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

26 


**Figure 12.** An example of summarization from Tidybot (Wu et al. 2023a). LLM can summarize a strategy with few-shot prompting. 

Summarization, also called inductive reasoning, is a cognitive ability to draw logical conclusions or provide a general strategy from limited information (Funke 2010). Summarization of LLMs shows the potential of embodied agents in the household scenario. The rearrangement task of tidying up a room is challenging for classical methods (Batra et al. 2020; Gan et al. 2022). On the one hand, where objects are placed is highly personal, depending on different people’s preferences and habits. On the other hand, it is impractical to enumerate all the objects that exist in the task-specific domain and to specify the goal state for every novel object. Thus, prior models of rearrangement tasks that specify target locations manually struggle to execute effectively in large-scale or real-world environments (Rasch et al. 2019; Yan et al. 2021). To solve this issue, Housekeep utilizes a large-scale dataset of human preferences instead of learning from a small set of tidying samples (Kant et al. 2022). Consequently, the Housekeeper assesses the capability to reason the target location and rearrange unseen objects. Wu et al. (2023a) argue that such a rearrangement preference is still generic rather than personal. They have constructed a mobile manipulator, Tidybot, which reasons individual preference by few-shot prompting and summarizes a general strategy, e.g., through textual prompts “ _yellow shirts go in the drawer_ ” and “ _white socks go in the drawer_ ”. Tidybot outputs “ _lighter-colored clothes go in the drawer_ ”, as shown in Figure 12. Tidybot can decide where to place the unseen object in the test by executing a corresponding preference strategy. While an agent with inductive reasoning can enhance their performance for unseen objects, a significant drawback is that the LLMs encode much task-agnostic knowledge, resulting in the failure to generate an entirely correct summary. For example, a rearrangement category may be too specific and not generalize well to unseen objects (Wu et al. 2023a). 

## **Eliciting reasoning via prompt engineering** 

LLMs are sensitive to prompting, so prompt engineering 


**Figure 13.** Chain-of-Thought with few-shot prompting. 

can elicit better reasoning from LLMs. The chain-of-thought (CoT) is one of the most well-known promptings (Wei et al. 2022). CoT decomposes a problem into a set of subproblems and then solves the sub-problems sequentially, where the answer to the next subproblem depends on the previous one. Consequently, CoT encourages LLMs to perform more intermediate reasoning steps before generating the final output. Figure 13 illustrates an example of CoT for better understanding. As a follow-up work, Zhang et al. (2024b) input LLMs with additional communication information from other agents to generate high-level plans that involve multi-agent cooperation. In addition, Socratic models employ multimodal-informed prompting (Zeng et al. 2023), such as utilizing visual language models and audio language models to incorporate perceptual information into the textual language input, thereby generating plans (Liang et al. 2023). Socratic-model-based systems thus have access to open-ended reasoning, such as video Q&A and forecasting, making these systems more robust to unseen objects. ECoT incorporates CoT into VLAs and performs multiple steps of reasoning about plans, sub-tasks, motions, and many others (Zawalski et al. 2025; Chen et al. 2025d). 

Question Objects: blue bowl, red block, red bowl, blue block. Command: move the red block a bit to the right. Agent Pythonic Code from utils import get ~~p~~ os, put ~~f~~ irst ~~o~~ n ~~s~~ econd objs = [’blue bowl’, ’red block’, ’red bowl’, ’blue block’] target ~~p~~ os = get ~~p~~ os(’red block’) + [0.1, 0] LLMs put ~~f~~ irst ~~o~~ n ~~s~~ econd(’red block’, target ~~p~~ os) 

**Figure 14.** Code generation with few-shot prompting (adapted from Code as policies (Liang et al. 2023)). 

## **Code-generation** 

Beyond leveraging LLMs for planning, those trained on code completion have demonstrated the capability to synthesize policy code, orchestrating planning, policy logic, and control (Chen et al. 2021; Chowdhery et al. 2023; Liang et al. 2023). An example is shown in Figure 14, where LLMs generate Pythonic code for an agent to perform a pick-andplace task. Wang et al. (2024a) mention that programs can represent temporally extended and compositional actions. Otherwise, Liang et al. (2023) also argue that policy code generated by LLMs can run on the controller directly, avoiding the requirement of the language-conditioned plan 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

27 

to map every textual instruction into the executable action in the pre-trained skill library. Liang et al. (2023) utilize the prompting hierarchical code-gen approach to re-compose the original API calls, defining a more complex function flexibly, which can generalize better to unseen objects. Similar works, such as VOYAGER (Wang et al. 2024a), can code a new skill using skill retrieval and memorize it in the skill library, then refine learned skills to deal with unseen objects. However, LLMs for code generation struggle to interpret much longer and more complex commands than the sample and still may call functions that do not exist in the control primitive APIs. Ha et al. (2023) prompt LLMs to output a success function code snippet as a labeler. The LLMs can verify unlabeled trajectories through this success function and label them with success or failure. Singh et al. (2023) design a Pythonic program prompt structure that ensures the generated plan has code formulation. This Pythonic plan inherits features from the code, such as obtaining state feedback via _assert_ and error collection via _else_ . 

However, these early Code-as-Policies methods (Liang et al. 2023; Mu et al. 2023; Karli et al. 2024; Mu et al. 2024) rely on open-loop control, meaning they cannot recover from execution errors or handle environmental uncertainties. To address this limitation, recent research incorporates closed-loop feedback and structured learning into code generation frameworks (Meng et al. 2025c,b). For example, DAHLIA (Meng et al. 2025c) introduces a dual-tunnel “planner + reporter” loop. The LLM first writes a multiprimitive code plan, guided by a CoT example curriculum that improves its reasoning. After robot execution, a visionlanguage reporter inspects before-and-after RGB-D frames and returns structured feedback (object, current pose, target pose, required action). The planner then patches only the failing parts and re-executes, iterating until success. While this LLM-based feedback improves robustness, it can be unreliable in extremely long-horizon tasks, as the LLM verifier may lack the understanding to identify subtle errors that are obvious to a human. Furthermore, this feedback is transient and does not contribute to the robot’s longterm capability growth (Meng et al. 2025b). The LYRA framework (Meng et al. 2025b) addresses this by integrating a human-in-the-loop for lifelong skill acquisition. It places a human verifier in the loop and stores every approved correction as a reusable skill function, indexed in an external vector memory. During future tasks, the agent retrieves the minimal skill set and few-shot plans, allowing the user to provide one-line hints that steer retrieval when ambiguity remains. This approach enables the robot to continually learn from its experiences and improve its performance over time. 

In summary, early code-generation agents with LLMs (Liang et al. 2023; Mu et al. 2023; Karli et al. 2024; Mu et al. 2024) revealed the promise of “from language to robot code” for developing flexible and generalizable robot policies, but they were hindered by open-loop execution, shallow prompts, and forgetfulness. DAHLIA (Meng et al. 2025c) addresses the first two issues with structured inter-loop feedback and CoT-guided example curricula, while LYRA (Meng et al. 2025b) complements it by turning corrections into persistent, retrievable skills under light human supervision. Together, these methods demonstrate a potential path for achieving 

reliable and scalable reasoning in language-conditioned manipulation. However, a fundamental limitation remains: the performance of these systems is ultimately capped by the reasoning and code-generation capabilities of the underlying LLM. Mialon et al. (2023) demonstrate that different LLMs, and even different versions of the same model, possess varying inference capabilities, which directly impacts the quality of the generated code and, consequently, the robot’s task success. For instance, on the GSM8K reasoning benchmark (Cobbe et al. 2021), the code-optimized “code-davinci-002” model outperforms the text-optimized “text-davinci-002”, highlighting that the choice of the foundation model is a critical factor for the success of code-as-policy approaches. 

## **Iterative reasoning** 

LLMs for planning or single-cycle reasoning often generate plans that are brittle to execution errors or environmental uncertainties, as they may call nonexistent functions or rely on flawed assumptions about the environment state. Iterative reasoning mitigates this issue by creating a closed loop where the model refines its output based on feedback from previous attempts iteratively. This process allows the agent to correct its course, circumventing hallucinations, and adapt to unexpected outcomes, as shown in Figure 15. Early examples of this paradigm focused on incorporating feedback. For instance, Inner Monologue (Huang et al. 2023c) uses feedback from a dedicated success detector and a scene descriptor to inform the LLM’s next reasoning step, enhancing task completion. A more cognitive form of iterative reasoning is _self-reflection or self-correction_ , where the LLM is prompted to analyze its own performance and generate corrective feedback for itself. This moves beyond simple error signals to a more cognitive process of introspection. For example, REFLECT (Liu et al. 2023d) attempts at this, where an LLM summarizes hierarchical sensor data into a textual form to obtain explanations for high-level task failures. However, it corrects errors only after an entire long-horizon task is completed, making it inefficient for real-time adjustments. 

To address this, HiCRISP (Ming et al. 2024) introduces a hierarchical closed-loop system that enables error correction within individual steps of a task. It distinguishes between high-level planning failures and low-level action failures. When a low-level failure occurs, it first tries to correct using a predefined structure. If that fails, or if a high-level plan failure is detected, it generates a language prompt describing the error and the current state, which is fed back to the LLM to generate a corrected action or plan. While these methods correct high-level plans or skill choices, they often struggle to refine the low-level motor control parameters, like SE(3) pose for grasping. AIC MMLM (Xiong et al. 2025) specifically targets this gap for articulated object manipulation. When a manipulation attempt fails, a Feedback Information Extraction module analyzes the failed interaction to infer its geometric cause. Similarly, the Self-Corrected (SC)-MLLM (Liu et al. 2024) also detects low-level pose errors and adaptively seeks feedback from “experts” (e.g., affordance models, grasp planners). Based on the expert’s structured feedback (e.g., potential contact 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

28 


**Figure 15.** LLM could also iteratively replan based on the observations and feedback given from environments. 

points or orientations), SC-MLLM re-evaluates the failure and generates a corrected action. Though these iterative reasoning methods enhance robustness, they still rely on the underlying LLM’s reasoning capabilities and may require extensive computational resources or inference time due to multiple inference cycles. Moreover, this issue is exacerbated in long-horizon tasks, where multiple iterations may be needed at each step, leading to significant latency. 

### _6.2.3 LLMs-driven structured planning_ 

LLMs face challenges with long-horizon planning and reasoning, mainly due to their lack of interpretability and difficulty in handling complex constraints. To mitigate these issues, recent work has explored integrating LLMs with formal planning methods, such as symbolic systems and behavior trees, to leverage the strengths of both approaches. 

## **Combining LLMs with symbolic systems** 

Symbolic systems offer structured and interpretable planning but require extensive manual engineering. LLMs, on the other hand, posses vast commonsense knowledge but lack formal guarantees and can hallucinate. Combining them provides a promising solution for robust and grounded reasoning. One approach is to integrate LLMs with KGs, which provides a structured representation of entities and their relationships. For instance, PLANner (Lu et al. 2022) leverages an external KG (ConceptNet (Speer et al. 2017)) to construct commonsense-infused prompts, guiding the LLM to generate more plausible plans. Going a step further, LLMs can be used to autonomously build or augment these KGs. Miao et al. (2024) use an LLM to create SkillKG, a taskcentric manipulation KG, from which a robot can infer new task plans. Similarly, RoboEXP (Jiang et al. 2025a) 

interactively explores its environment to build an actionconditioned scene graph (a KG variant), which is then used for planning and reasoning. Another powerful symbolic formalism is the PDDL. 

PDDL models define structured symbolic blueprints that enable off-the-shelf external planners (symbolic solvers) to generate robust and optimized solutions. Integrating LLMs with PDDL models enhances their capabilities by automating the difficult process of creating PDDL domain and problem files from natural language. Early works used LLMs to translate natural language goals into PDDL representations for constraint checking and goal verification (Ding et al. 2022; Xie et al. 2023b). However, this integration introduces several key challenges: (i) the slow speed of symbolic search, (ii) the symbol grounding problem, and (iii) the difficulty of representing complex realworld interactions. First, the **slow speed of symbolic search** may cause long delays before the robot can act. To overcome this, Capitanelli and Mastrogiovanni (2024) fine-tune GPT-3 on a domain-specific dataset of PDDL problem-plan pairs. This allowed the LLM to generate a plan action by action, enabling concurrent planning and execution and reducing the robot’s perceived waiting time. 

The second challenge of **symbol grounding problem** is _how to connect abstract PDDL predicates to the robot’s physical reality_ . To address this, IALP (Wang et al. 2025a) develops a closed-loop system that augments user instructions with feasibility information derived from real-time sensor feedback. By using “grounding mechanisms” to check predicates, the PDDL problem itself is enriched with grounded, physically-aware knowledge before planning, ensuring the generated actions are viable. A specific but critical aspect of grounding arises in contact-rich manipulation, where visual perception alone is insufficient. LEMMo-Plan (Chen et al. 2025b) tackles this by incorporating multi-modal demonstrations, including tactile and force-torque data. This allows the LLM to reason about “invisible” events like cable tension or insertion forces, enabling it to define robust force-based skill conditions and segment demonstrations more accurately. Further refining the interface between language and symbolic systems, subsequent research explore different _levels of abstraction_ . Task-level PDDL may not be the most natural representation for an LLM to reason about. Paulius et al. (2025) propose bootstrapping task planning with a higher Object-Level Plan. It uses an LLM to generate a plan schema describing object interactions, which is then systematically grounded into a set of PDDL subgoals for a traditional planner. This creates a cleaner separation of concerns, allowing the LLM to operate at a commonsense level while the symbolic planner handles the formal task-level constraints. The third challenge of **complex interaction representation** remains open, while behavior trees offer an alternative. 

## **Combining LLMs with behavior trees** 

While symbolic planners like PDDL may struggle with scalability, Behavior Trees (BTs) offer a more modular, reactive, and reusable alternative for specifying complex tasks (Iovino et al. 2022). However, manually designing BTs is a laborintensive process that limits their scalability. To address this, 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

29 

recent work has focused on leveraging LLMs to automatically generate BTs from natural language instructions. This approach combines the structured, verifiable execution of BTs with the commonsense reasoning of LLMs, tackling key challenges in _data inefficiency_ (learn BTs from scratch) and _runtime adaptability_ (on-the-fly modifications). Early methods explored using LLMs for runtime plan adaptation. For example, LLM-bt (Zhou et al. 2024b) uses an LLM to generate high-level descriptive steps that are parsed into an initial BT. A dedicated algorithm then dynamically expands this tree at runtime if a failure is detected, allowing the robot to incorporate new actions to adapt to environmental changes. However, this approach still required hand-written parsing rules for each new task. To ensure optimality and correctness, LLM-OBTEA (Chen et al. 2024b) introduces a two-stage framework where the LLM’s role is limited to translating high-level instructions into a formal first-order logic goal. This goal is then fed to an Optimal BT Expansion Algorithm, which constructs a BT that is theoretically guaranteed to achieve the goal with minimal cost. A key limitation remained: the resulting BT could not autonomously debug missing preconditions discovered only during deployment. Subsequent work addressed this by casting the LLM as a “common-sense repair agent”. BETR-XP-LLM (Styrud et al. 2025) uses the LLM to propose the minimal precondition and matching subtree required to resolve an execution failure, permanently integrating the fix into the policy. Because these patches are verifiable BT fragments, the robot’s policy becomes more robust with every failure. Other research focuses on improving the initial generation process itself. Ao et al. (2025) effectively exploite LLMs to directly generate BTs and explored four distinct in-context learning strategies for BT generation (one-step, iterative, human-in-the-loop, and recursive), enabling runtime feedback and replanning. They find that while richer interaction yields higher success rates, it also increases LLMs token and latency costs, highlighting a trade-off between performance and efficiency. 

# _6.3 Empowered by vision-language models_ 

In robotic manipulations, while LLMs excel at high-level reasoning and planning, they suffer from a fundamental limitation: they are disembodied. Operating purely on text, they lack direct perceptual access to the robot’s environment. This leads to the classic “grounding problem”, where the model’s plans might involve objects that are not present or fail to account for the current observation of the world, resulting in hallucinations and infeasible actions. To bridge this gap, many approaches require intermediate modules, such as object detectors (like YOLO (Redmon et al. 2016), MDETR (Kamath et al. 2021)), to translate visual information into text that the LLM can comprehend. This process may lose critical information. VLMs offer a more direct and powerful solution. By being pre-trained on vast datasets of paired images and text, VLMs can inherently process and reason about visual information. This allows them to directly ground high-level language instructions in the images, connecting abstract concepts like “the red block” to specific image pixels. This section explores how the tight fusion of vision and language in VLMs enables more robust and capable robotic manipulation systems, focusing on contrastive learning and generative methods. 

### _6.3.1 Contrastive learning approaches_ 

Contrastive learning is widely used in VLMs to align the text and vision modalities. It learns representations where similar samples are brought closer together in the learned latent space, while dissimilar samples are pushed farther apart. The well-known approach CLIP (Radford et al. 2021) aligns the image embedding and the text embedding of its corresponding caption in the latent space. In the field of robot manipulation, CLIP-based approaches are extensively applied. CLIPORT (Shridhar et al. 2022), a method that combines the broad semantic understanding of CLIP with the spatial precision of Transporter (Zeng et al. 2021), is capable of solving a variety of language-specified tabletop tasks. In Dream2Real (Kapelyukh et al. 2024), 6-DoF languagebased rearrangement tasks are achieved by enabling robots to “imagine” virtual goal states and then evaluate them using CLIP. CLIP-Fields (Shafiullah et al. 2023) is capable of mapping spatial locations to semantic embedding vectors trained using CLIP-based approaches, enabling the agent to conduct navigation and localization. 

EmbCLIP (Khandelwal et al. 2022) investigates the effectiveness of CLIP visual backbones for Embodied AI tasks. Instruction2Act (Huang et al. 2023a) leverages CLIP model to accurately locate and classify objects in the environments. LAMP (Adeniji et al. 2024) leverages R3M (Nair et al. 2023), a reusable representation for robot manipulation, to calculate the rewards for RL. MOO (Stone et al. 2023) queries an OWL-ViT (Minderer et al. 2022) to produce a bounding box of the object of interest with the prompt “An image of an X”. Xiao et al. (2023) enhance instructions using CLIP by fine-tuning it with robot manipulation data and natural language annotations, and then label a larger dataset with this CLIP model for further training. LATTE utilizes CLIP encoders to better align visual and textual information (Bucker et al. 2023), grounding the instructions in the specific objects that need manipulation. Moving beyond image-level approaches, R+X (Papagiannis et al. 2025) demonstrates how Gemini can be utilized to retrieve relevant videos of human demonstrations for a given language-based task, which is then used to condition a policy. 

### _6.3.2 Generative approaches_ 

Generative approaches model data distributions to synthesize textual and visual content, conditioned on text, images, or both simultaneously. They are important for languageconditioned robot manipulation, since the generated content can be used for planning, reasoning, data augmentation, and future state estimation. 

## **Text generation** 

Auto-regressive text generation approaches (Cho et al. 2021; Wang et al. 2022) typically merge visual and textual information through a Transformer-based method and perform a sequence-to-sequence structure to generate text. A growing line of work uses such VLMs as planning and evaluation scaffolds. For example, Patel et al. (2023) demonstrate that a pre-trained planner can convert textual task descriptions and execution videos into explicit plans. Complementing planning, languageaugmented evaluators provide reward signals: Du et al. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

30 

(2023a) fine-tune Flamingo (Alayrac et al. 2022) as a success detector via VQA, using its judgments for reward design. Beyond planning and evaluation, VLMs supply promptable perceptual priors and enable data-centric scaling. For instance, PR2L (Chen et al. 2025e) demonstrates that VLMs can generate superior visual embeddings when prompted with task-relevant context, outperforming generic, non-promptable representations. Similarly, RoboPoint (Yuan et al. 2025b) addresses the VLM’s struggle with precise action articulation by using a synthetic data pipeline to instruction-tune a VLM to predict keypoint affordances from language instructions, grounding abstract commands in concrete visual features without requiring real-world data. In parallel, NILS (Blank et al. 2025) leverages VLMs for data-centric scaling by automatically generating descriptive labels for unlabeled robot datasets, which are then used to train more capable language-conditioned policies. 

Some works focus on leveraging the generalist reasoning capabilities of large-scale VLMs. PaLM-E (Driess et al. 2023), a 562B parameter VLM, demonstrates that a single massive model could perform embodied reasoning, translating high-level commands into robot-executable plans with little or no robot-task-specific finetuning. This shows that scaling could directly yield more powerful robotic planners. An alternative to a single model is a modular approach. Socratic Models (Zeng et al. 2023) proposes a framework where multiple specialized models (e.g., for vision, audio, and language) communicate through multimodal prompts, collaboratively solving problems that no single model could handle alone. This enables more flexible and extensible reasoning. PIVOT (Nasiriany et al. 2024) reframes manipulation as an iterative visual dialogue, where the VLM repeatedly answers questions about the scene to refine its proposed actions. This turns the VLM into an active reasoning partner that grounds its decisions through a continuous feedback loop. 

## **Image generation** 

The ability of generative models to generate realistic images or videos over a long horizon brings new opportunities for robotic manipulation. Such models commonly include textto-image models like Make-A-Video (Singer et al. 2023), DALL-E 2 (Ramesh et al. 2022), Stable Diffusion (Rombach et al. 2022), and Imagen (Saharia et al. 2022). Instead of just aligning or describing existing content, these models can synthesize novel visual data from language, serving several key roles in robotics. One primary application is _goal visualization_ , where a text-to-image model translates a language instruction into a concrete goal image. This visual goal can then guide a low-level, goal-conditioned policy. For example, Dall-E-Bot (Kapelyukh et al. 2023) utilizes a text-conditioned diffusion model to generate goal images for tabletop object rearrangement tasks. SuSIE (Black et al. 2024) leverages pre-trained text-conditional image-editing models to generate a sequence of subgoals, which are then executed by a low-level controller. This approach decouples high-level semantic understanding from low-level control, allowing each component to be optimized independently. 

Another powerful use is _data augmentation_ . Given the high cost of collecting real-world robot data, generative models 

can create diverse, synthetic training examples. Chen et al. (2024d) take a small offline dataset of expert demonstrations and use a text-to-image model to semantically bootstrap it into a much larger and more varied dataset. This augmented data can then be used to train a robot policy that generalizes better to unseen environments and tasks. Generative models can also function as _world models_ by predicting future video frames conditioned on language and current actions. These video prediction models can be used for planning or to learn an inverse dynamics model that maps desired outcomes back to the actions required to achieve them (Gu et al. 2024b; Ko et al. 2024; Du et al. 2023b). This allows the robot to “imagine” the consequences of its actions before executing them (Nematollahi et al. 2020). Moreover, generative models can enhance policies through _multi-modal conditioning_ , especially when dealing with partially annotated datasets. GR-MG (Li et al. 2025b) first trains a policy that accepts both language and image goals. During inference, when only a text instruction is available, it uses an image-editing model (Brooks et al. 2023) to generate a corresponding goal image. The policy is then conditioned on both the original text and the generated image, making it more robust. These approaches are powerful but resource-intensive. The generated images and videos can contain noise, artifacts, or physically implausible details, making it challenging to extract reliable signals for robot control (Yuan et al. 2025a; McCarthy et al. 2025). 

# **7 Language in unified vision-language-action models** 

As the field has evolved, increasing attention has shifted from hierarchical language-conditioned systems to end-to-end vision-language-action models (VLAs). In the hierarchical approaches discussed in Section 6, large models such as LLMs and VLMs typically serve as planners, reasoners, or perceptual modules, while action execution is handled by separate low-level controllers, policy modules, or motion planners. By contrast, VLAs aim to learn a policy model that jointly represents visual observations, language instructions, and robot actions within a unified embodied policy architecture. In this paradigm, language is no longer limited to high-level reasoning or external task specification. Instead, it is coupled with visual perception and action in the model’s core representation and training process. 

The term VLA, however, is not used uniformly across the literature. Under a broad input-output definition, a system may be called a VLA if it receives visual observations and language instructions and produces robot actions (Kawaharazuka et al. 2025). This broad view is useful for tracing the historical development of observationlanguage-action systems. In this survey, however, the VLA category is used in a narrower analytical sense to preserve the distinction between the functional roles of language introduced in Sections 5–6. Specifically, this section focuses on embodied policy models in which action generation is learned in close coupling with visuallinguistic representations through the model architecture and training objective. This coupling may be realized through discrete action tokens that are detokenized into 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

31 


**Figure 16.** Hierachical taxonomy of Vision-Language-Action models according to optimization directions, which f **l** ows Perception _→_ Reasoning _→_ Action _→_ Adaptation: (I) Perception and state representation. (II) Reasoning, planning, and knowledge preserving. (III) Action generation and execution. (IV) Model learning and adaptation. 

executable robot commands (Brohan et al. 2023a; Zitkovich et al. 2023), continuous action heads, diffusion-based action generation (Wen et al. 2025c), flow-matching-based controllers (Black et al. 2025b), or action-expert modules attached to a VLM backbone. 

attribute (Kawaharazuka et al. 2025), but to maintain a finergrained distinction between VLM-empowered languageconditioned policies and recent unified VLA policy models in our taxonomy. 

# _7.1 Overview_ 

This distinction is particularly relevant to the boundary between Section 5 and the present section. Both languageconditioned policies and VLAs may receive visual observations and language instructions as inputs and output robot actions. The difference lies in the role played by language and in how the action-generation mechanism is integrated with the vision-language model. In language-conditioned policies, language primarily acts as an external task or behavior condition for a policy. In VLM-empowered methods, a pretrained VLM may provide semantic grounding, perception, affordance estimation, or reasoning, while a taskspecific policy or controller generates executable actions. In contrast, the VLA models emphasized in this section integrate action generation more directly into the embodied vision-language policy, so that robot actions are learned as a central component of the model rather than only as the output of a downstream task-specific controller. 

CLIPORT (Shridhar et al. 2022) provides an example. From a broad observation-language-action perspective, CLIPORT can be viewed as an early VLA-like system, as it integrates CLIP-based vision-language grounding with a manipulation policy that outputs robot actions (Kawaharazuka et al. 2025). In our taxonomy, however, CLIPORT is discussed primarily as a VLM-empowered language-conditioned visuomotor policy. The reason is that CLIP (Radford et al. 2021) serves as a frozen semantic grounding module, while action generation is performed by a Transporter-style policy (Zeng et al. 2021). Specifically, CLIPORT predicts dense pick and place affordance maps and selects executable actions through spatial maximization, followed by a placement prediction conditioned on the selected pick location. Thus, language in CLIPORT conditions the policy and improves semantic grounding, but the robot action is generated through a task-specific pick-and-place affordance mechanism, rather than through an action representation integrated into a large VLM-based embodied policy. This placement is not meant to deny CLIPORT’s observation-language-action 

Gato (Reed et al. 2022) represents a pioneering effort in this direction as a general-purpose agent. The authors tokenize text, images, discrete values, and continuous values, then train the model from scratch by predicting the masked tokens within sequences. RT-1 (Brohan et al. 2023a), RT2 (Zitkovich et al. 2023), Gemini Robotics (Team et al. 2025; Abdolmaleki et al. 2025), and PI VLAs (Black et al. 2025b,a) utilize pre-trained vision-language models, which are cofine-tuned on both large-scale vision-language datasets and low-level robot actions, to enhance generalization to novel objects and commands. RT-X (O’Neill et al. 2024) is trained on an assembled dataset collected from 22 different robots, encompassing 527 skills across 160,266 tasks. It demonstrates positive transfer effects, where shared experiences from other platforms enhanced the capabilities of individual robots, suggesting that VLAs could benefit from cross-embodiment learning. In contrast, OpenVLA (Kim et al. 2025c) utilizes the pre-trained open-source Llama 2 (7B) along with features from DINOv2 (Oquab et al. 2024) and SigLIP (Zhai et al. 2023), and is fine-tuned on a robot manipulation dataset, demonstrating that data diversity and new model components allow a small-scale model (7B) outperform the large-scale model RT-X (55B) in some tasks. Instead of relying on 2D inputs, 3D-VLA (Zhen et al. 2024) is built on a 3D-based LLM and introduces a set of interaction tokens to engage with the embodied environment. 

As the field of VLAs continues to rapidly evolve with the advancement of foundation models, we present a systematic taxonomy to organize recent developments. Our taxonomy follows the flow: Perception _→_ Reasoning _→_ Action _→_ Adaptation<sup>*</sup> , as illustrated in Figure 16: 

> _∗_ In this taxonomy, we focus on delineating the primary contribution of each method (like reasoning aspect), even though most methods involve multiple aspects (such as perception, action). 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

32 

- **Perception** : Methods that focus on optimizing how VLAs perceive and understand their environment, including: _Data Sources and Augmentation_ , _3D Scene Representation and Grounding_ , and _Multimodal Sensing and Fusion_ . 

- **Reasoning** : Approaches that enhance the model’s internal “thought process”, that is, how it forms plans, leverages prior knowledge, and predicts outcomes to solve complex tasks, including: _Internal World Models and Reasoning_ , _Preserving Foundational VLM Capabilities_ , and _Long-Horizon Planning_ . 

- **Action** : Methods that focus on the optimization regarding the “output” stage of the policy, concerning the form and mechanism of the robot’s actions. This bridges the gap between the model’s internal plan and its physical embodiment, primarily including: _Action Generation and Execution_ . 

- **Adaptation** : Techniques for efficiently training, finetuning VLA models to enhance their adaptability to new situations and downstream tasks, including: _Efficient Adaptation and Fine-Tuning_ . 

To synthesize the rapid progress in VLAs, Table 5 summarizes the comparison of representative state-of-the-art methods across these four dimensions. 

# _7.2 Optimization for perception_ 

A VLA model’s ability to act intelligently is fundamentally rooted in its capacity to perceive and interpret the world accurately. The methods in this section focus on optimizing the “input” stage of the policy, addressing how VLAs can be trained on richer, more diverse, and more robust data sources to build a better understanding of their environment. 

### _7.2.1 Data sources and augmentation_ 

A foundational challenge in training a generalist VLA has been the scarcity and high cost of collecting large-scale, high-quality robot demonstration data. The requirement for physical robots and expert teleoperators fundamentally limits the scale, diversity, and complexity of tasks that can be captured, creating a data bottleneck for training powerful generalist policies. To overcome this challenge, a significant line of research has explored alternative data sources, moving beyond robot-specific demonstrations to leverage the vast and rich data generated by human activities. For example, EgoVLA (Yang et al. 2025d) proposed a paradigm of learning from egocentric human videos in a two-stage process. First, a VLA model is pre-trained on a curated dataset of egocentric human videos to predict human wrist and hand actions. Then, this model is fine-tuned with a small number of robot-specific demonstrations to bridge the “embodiment gap” between humans and robots, using inverse kinematics and action retargeting methods. This approach dramatically reduces the reliance on large-scale robot data collection for learning complex skills. H-RDT (Bi et al. 2026) seeks to scale up this two-stage paradigm and addresses the challenges of transferring knowledge from a single embodiment (human) to multiple robot embodiments. It first pre-trains a 2B-parameter diffusion transformer on a human manipulation dataset, which provides a more 

consistent and powerful behavioral prior. Then, it applies modular action encoders/decoders that are re-initialized and fine-tuned for each target robot, preserving the rich manipulation knowledge learned during pre-training. This design turns rich but embodiment-mismatched human motion into a transferable visual-linguistic prior, yielding obvious improvements over training-from-scratch models ( _π_ 0 (Black et al. 2025b), RDT (Liu et al. 2025a)). 

However, simply increasing the volume of data does not guarantee generalization. A critical line of inquiry investigates why policies trained on large, aggregated datasets often exhibit “shortcut learning”, relying on spurious correlations instead of causal features, which leads to poor out-of-distribution performance. Xing et al. (2025b) provide a comprehensive analysis of this problem, identifying two primary causes: (1) limited diversity within individual sub-datasets and (2) dataset fragmentation, where significant distributional gaps exist between different subdatasets (e.g., data from different labs or robots). The model learns to associate task-irrelevant features (like camera viewpoint or background) with specific tasks. Because those features are predictive within a fragmented dataset. To mitigate this, the work proposes not only principles for better data collection but also a practical solution for existing offline datasets: robotic data augmentation. By synthetically generating novel viewpoints or swapping objects between scenes, these augmentation strategies can increase intradataset diversity and bridge the gaps between fragmented sub-datasets, effectively breaking the spurious correlations that lead to shortcut learning. 

### _7.2.2 3D scene representation and grounding_ 

Many VLAs utilize 2D vision as their primary input modality, which lacks 3D spatial awareness (e.g., depth, scale, and spatial relationships). This “spatial awareness” gap hinders a robot’s ability to perform precise manipulation. To overcome the limitations of 2D vision, research has focused on integrating 3D information into VLA frameworks, grounding the model’s understanding in the geometric reality of the physical world. A direct approach is to augment 2D features with explicit spatial data. For instance, SpatialVLA (Qu et al. 2025) introduces Ego3D Position Encoding, which utilizes a depth model to calculate the 3D coordinates of each pixel and incorporates this information into the VLM’s 2D visual features. This method enriches the model’s input with spatial context without requiring complex architectural changes and extends this spatial reasoning to the action space via Adaptive Action Grids, making action tokens spatially meaningful. However, directly modifying the visual input stream risks disrupting the VLM’s pre-trained vision-language alignment. To mitigate this, PointVLA (Li et al. 2026a) proposes a modular framework that injects 3D information with minimal disruption. It uses a separate lightweight encoder to process a 3D point cloud and injects the resulting geometric features into a frozen action expert module, thereby preserving the core VLM’s integrity. 

An alternative to injecting 3D data is to reformat it into a 2D representation that the VLM can natively understand. BridgeVLA (Li et al. 2026b) implements this by projecting a 3D point cloud into multiple 2D orthographic images (e.g., 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

33 

**Table 5.** Comparison of representative state-of-the-art methods for **Section 7 Vision-language-action models** . This table categorizes large model-driven end-to-end policies based on their primary optimization directions: Perception, Reasoning, Action, and Learning & Adapting. By tokenizing reasoning and low-level actions within a unified framework, these representative methods illustrate the cutting-edge strategies for overcoming embodiment gaps, enhancing internal planning, physical execution, and achieving efficient fine-tuning. 

|**Method**|**Optimization**<br>**Direction**|**Core Mechanism**|**Key Advantages**|**Key Disadvantages**|
|---|---|---|---|---|
|EgoVLA<br>(Yang<br>et<br>al.<br>2025d)|Perception|Pre-trains<br>on<br>egocentric<br>human<br>videos<br>to<br>predict<br>actions, then fine-tunes with<br>robot data.|Dramatically<br>reduces<br>reliance<br>on<br>large-scale,<br>costly robot data collection<br>for learning complex skills.|Inherently<br>requires<br>robust<br>action retargeting methods<br>to bridge the “embodiment<br>gap” between humans and<br>robots.|
|BridgeVLA<br>(Li et al. 2026b)|Perception|Projects<br>3D<br>point<br>clouds<br>into multi-view 2D images<br>and predicts 2D heatmaps to<br>seamlessly align 3D inputs<br>and actions within a pre-<br>trained 2D VLM.|Highly<br>sample-efficient<br>(3<br>trajectories<br>per<br>task)<br>and<br>generalizes<br>robustly<br>to visual disturbances and<br>novel instructions.|Target<br>keypoints<br>can<br>be<br>occluded<br>during<br>the<br>2D<br>orthographic<br>projection,<br>and performance drops on<br>complex,<br>multi-step<br>long-<br>horizon tasks.|
|CoT-VLA<br>(Zhao<br>et<br>al.<br>2025)|Reasoning|Autoregressively<br>generates<br>intermediate subgoal images<br>as<br>a<br>visual<br>“chain-of-<br>thought” before predicting<br>the final actions.|Improves multi-step reason-<br>ing and complex instruction<br>following by explicitly visu-<br>alizing the goal state first<br>(reason before acting).|High<br>computational<br>overhead due to image token<br>generation,<br>and<br>struggles<br>with<br>out-of-distribution<br>subgoal synthesis.|
|MemoryVLA<br>(Shi et al. 2026)|Reasoning|Incorporates explicit mem-<br>ory mechanisms to retain<br>task context and visual his-<br>tory over extended interac-<br>tions.|Mitigates<br>context-loss<br>in<br>long-horizon<br>tasks,<br>allowing<br>the<br>robot<br>to<br>execute sequences that span<br>extended timeframes.|Managing<br>and<br>retrieving<br>from<br>an<br>expanding<br>memory<br>buffer<br>adds<br>architectural<br>complexity<br>and computational cost.|
|_π_0<br>(Black<br>et al. 2025b)|Action|Adds an action expert using<br>flow-matching<br>to<br>a<br>pre-<br>trained<br>VLM,<br>outputting<br>high-frequency,<br>continuous<br>actions.|Bridges semantic reasoning<br>with<br>precise<br>continuous<br>motor<br>control,<br>enabling<br>highly<br>dexterous,<br>multi-<br>stage tasks.|Requires<br>massive<br>and<br>diverse<br>training<br>datasets<br>( 10,000 hours).|
|ControlVLA<br>(Li et al. 2025c)|Adaptationg|Integrates<br>object-centric<br>representations<br>into<br>VLA<br>models,<br>using<br>zero-initialized<br>layers<br>to<br>adapt without losing prior<br>knowledge.|Highly<br>data-efficient<br>(requires<br>only<br>10-20<br>demonstrations) and robust<br>to<br>unseen<br>objects<br>and<br>backgrounds.|Relies<br>on<br>external<br>visual<br>models<br>(GroundingDINO,<br>SAM2)<br>for<br>tracking,<br>and<br>evaluations<br>are<br>currently<br>limited to single-arm indoor<br>manipulation.|
|OpenVLA-OFT<br>(Kim<br>et<br>al.<br>2025b)|Adaptationg|Replaces<br>autoregressive<br>discrete<br>prediction<br>with<br>an Optimized Fine-Tuning<br>(OFT)<br>recipe,<br>integrating<br>parallel<br>decoding,<br>action<br>chunking,<br>and<br>continuous<br>L1 regression.|Improves<br>inference<br>speed<br>(25-50×) and reduces latency<br>for real-time control, while<br>boosting task success rates.|Struggles<br>with<br>complex,<br>memory-dependent<br>tasks<br>and may lack the capacity<br>to model highly multimodal<br>action distributions.|


top, front, and side views). These 2D images are then fed into the standard VLM backbone, and the model predicts actions as 2D heatmaps over these same projections. This approach unifies the input and output within a consistent 2D space, leveraging the VLM’s powerful 2D understanding while grounding actions in a 3D-derived representation. After exploring methods that either enhance features with 3D data (Qu et al. 2025), inject (Li et al. 2026a), or reformat (Li et al. 2026b), a more holistic approach emerged that seeks to process both 2D and 3D modalities in parallel and fuse them at the decision-making stage. GeoVLA (Sun et al. 2025) processes 2D and 3D modalities in parallel. a standard VLM processes the 2D image and language to produce a fused vision-language embedding, while a separate network processes the point cloud to generate a separate 3D geometric 

embedding. The resulting embeddings are then concatenated and fed into a novel 3D-enhanced Action Expert, which uses a Mixture-of-Experts architecture (Jacobs et al. 1991; Mees et al. 2016) to fuse the information before generating the final action. This parallel design preserves the integrity of the pretrained VLM while enabling a more expressive combination of 2D semantic and 3D geometric cues. 

The integration of 3D scene representation is a critical and rapidly evolving frontier for VLA models. A primary insight is that simply adding a 3D sensor is not enough, the core scientific challenge lies in bridging the “modality gap” between the 2D-centric perception of existing VLMs and the 3D geometry of the real world (Mees et al. 2019; Kerr et al. 2023). The field is moving from straightforward feature augmentation (Qu et al. 2025) toward more sophisticated 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

34 

and principled architectures that are modular (Li et al. 2026a), aligned (Li et al. 2026b), or parallelized (Sun et al. 2025). These advanced strategies aim to harness the semantic richness of 2D vision and the geometric precision of 3D data simultaneously, paving the way for robot policies with superior spatial awareness, precision, and adaptability to real-world complexities. 

(OmniVTLA (Cheng et al. 2025), FuSe-VLA Jones et al. (2025)), and dynamic fusion (ForceVLA (Yu et al. 2026)). This progression underscores that the future of generalist robots lies not just in seeing and hearing, but in feeling and physically reasoning about their physical interactions with the world. This requires architectures can intelligently and adaptively fuse multiple sensing modalities. 

### _7.2.3 Multimodal sensing and fusion_ 

While vision provides rich global context, it is insufficient for contact-rich tasks like assembly or insertion, where a sense of touch is crucial. To overcome this limitation, a key area of research focuses on integrating non-visual sensory data, such as tactile and force feedback, into VLA models. This introduces challenges in representing diverse sensory signals, fusing them with vision-language features, and grounding abstract commands in physical forces. Early work focused on integrating tactile data and refining the learning process. VTLA (Zhang et al. 2026a) is proposed to fuse vision, tactile, and language by tokenizing tactile image sequences alongside other modalities. It addresses the mismatch between the VLM’s classification objective and continuous robot control by using a two-stage training process with Direct Preference Optimization (DPO) to refine the policy. While integrating tactile data as another perceptual channel is a crucial first step, a deeper challenge lies in grounding the VLM’s abstract knowledge directly into physical force control. To better ground language in physical interaction, Tactile-VLA (Huang et al. 2025a) augments the policy’s output to predict both target force and target position, enabling it to understand force-related adverbs like “gently” or “hard”. It also introduces a CoT mechanism to interpret tactile feedback upon failure and generate corrective actions. 

A practical barrier is the heterogeneity of tactile sensors, where some are vision-based (e.g., GelSight), while others are force-based, each with different data structures and characteristics. To address this, OmniVTLA (Cheng et al. 2025) creates a unified tactile representation by using a dualpath encoder for different sensor types ( vision-based tactile sensors and force-based sensors), and uses cross-modal contrastive learning to align the tactile representations with their linguistic and visual counterparts. This pre-alignment ensures that tactile information is processed within a shared semantic space before being fused into the main VLA model. As models begin incorporating multiple modalities, the focus shifts to how to fuse them most effectively. Simple concatenation or early fusion can disrupt the VLM’s powerful pre-trained representations. ForceVLA (Yu et al. 2026) introduces a dynamic “late fusion” mechanism using a force-aware Mixture-of-Experts (MoE) module. This allows the model to adaptively route sensory inputs to specialized expert networks, enabling a more effective integration of real-time force feedback. 

In summary, incorporating a “sense of touch” is essential for enabling robust manipulation in contact-rich environments. Research has progressed from simple data fusion to more principled approaches that address learning objectives (VTLA (Zhang et al. 2026a)), semantic grounding (Tactile-VLA (Huang et al. 2025a)), sensor heterogeneity 

# _7.3 Optimization for reasoning_ 

Approaches that enhance the model’s internal “thought process”, that is, how it forms plans, leverages prior knowledge, and predicts outcomes to solve complex tasks. 

### _7.3.1 Long-horizon planning_ 

While VLAs excel at short-horizon skills, they often struggle with long-horizon tasks due to their reactive, step-by-step characteristics, which leads to compounding errors over time. To address this, a key area of research has focused on endowing VLAs with planning capabilities, enabling them to reason about multi-step sequences. This has led to three primary strategies: hierarchical decomposition, phaseaware control, and memory-augmented reasoning. The first strategy, **hierarchical decomposition** , trains the VLA to function as its own high-level planner. LoHoVLA (Yang et al. 2025f) and DexVLA (Wen et al. 2025a) explore this by training a unified model to first generate a linguistic sub-task (e.g., “ _pick up the green block_ ”) and then use that self-generated instruction to predict the corresponding action. This “think before you act” process is enhanced in LoHoVLA (Yang et al. 2025f) with a closed-loop control mechanism that efficiently replans at the sub-task level when execution fails, making error correction more robust. While DexVLA (Wen et al. 2025a) trains the model on demonstrations annotated with fine-grained sub-step reasoning, compelling the VLM backbone to function as an implicit high-level policy that decomposes direct prompts into a sequence of executable steps. 

While hierarchical decomposition provides a plan, it does not solve the **skill chaining challenge** , where dynamic coupling and error propagation between sub-tasks degrade performance. To address this, Long-VLA (Fan et al. 2025) introduces a more fine-grained and **phase-aware control** strategy. It segments each sub-task into a “moving phase” and an “interaction phase” and uses a novel phase-aware input masking to force the model to attend to the most relevant camera view for each phase (e.g., a wide view for navigation, a gripper view for manipulation). This allows a single model to smoothly transition between different stages of a sub-task, improving robustness. An alternative to explicit planning is to use **memory-augmented reasoning** to handle the non-Markovian properties of long-horizon tasks, where action history is crucial. Mainstream VLAs are effectively “memoryless”, which can cause failures when an action produces little visual change. MemoryVLA (Shi et al. 2026) solves this by incorporating an explicit memory system (Perceptual-Cognitive Memory Bank) that stores both lowlevel perceptual details and high-level semantic summaries from past steps. By retrieving and fusing relevant memories with the current observation, the model obtains a continuous 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

35 

stream of historical context, allowing it to handle temporal dependencies without relying on a predefined task hierarchy. 

In summary, long-horizon planning approaches range from integrating explicit hierarchical reasoning within unified models to developing complex mechanisms for temporal consistency. LoHoVLA (Yang et al. 2025f) and DexVLA (Wen et al. 2025a) represent a “planning-asreasoning” paradigm, where the VLM is trained to generate its own textual sub-goals to guide behavior. While LongVLA (Fan et al. 2025) focuses on the execution dynamics within and between these sub-goals, proposing a phase-based perceptual adaptation to improve skill chaining. Moreover, MemoryVLA (Shi et al. 2026) offers a more generalized solution by introducing an explicit memory module, tackling the core non-Markovian property of long-horizon tasks. 

### **Preserving foundational VLM capabilities** 

A central motivation for building VLA models is to leverage the vast semantic knowledge and reasoning skills embedded in pre-trained VLMs. However, a fundamental challenge emerged: fine-tuning these powerful, generalist models on narrower, domain-specific robotics data often leads to catastrophic forgetting. This phenomenon causes the VLA to lose the very conversational and reasoning capabilities that motivated its creation in the first place, degrading the model’s ability to understand novel instructions and generalize. To overcome this, some works have focused on developing architectural and training strategies to preserve, reactivate, and effectively transfer these foundational VLM capabilities into the embodied domain. Early efforts focused on creating a synergy between the reasoning of autoregressive models and the precision of diffusion-based policies. DiffusionVLA (Wen et al. 2025c) proposes a unified framework that integrates an autoregressive component for reasoning with a diffusion model for control. It introduces a “reasoning injection module” to embed self-generated textual reasoning into the diffusion policy, enriching the learning process with explicit reasoning signals. 

Subsequent research identifies that performance degradation stems from direct conflicts within the model’s parameter space. ChatVLA (Zhou et al. 2025b) identifies two key challenges: “spurious forgetting”, where robot-centric training overwrites crucial visual-text alignments, and “task interference”, where the competing objectives of control and understanding degrade performance. To address this, ChatVLA introduces a MoE architecture to isolate taskspecific parameters, minimizing interference. Building on this, ChatVLA-2 (Zhou et al. 2026b) refines this approach by using a dynamic MoE and a two-stage training pipeline to ensure the model’s actions reliably follow its internal reasoning. Taking a different perspective, some work focuses on the training dynamics as the root cause of knowledge degradation. Driess et al. (2026) propose knowledge insulation, which stops the gradient flow from the action expert back into the VLM backbone. This technique insulates the VLM’s knowledge from disruptive gradients while the VLM is simultaneously fine-tuned using a safer parallel learning signal: an autoregressive next-token prediction loss on discretized actions. Contrasted to MoE-based methods, this approach modifies the training graph rather than the core 

model architecture, allowing the VLM and action expert to be trained in parallel without interference. 

Another line of research recognized that preserving VLM capabilities is fundamentally tied to the training data. InstructVLA (Yang et al. 2025e) argues that “catastrophic forgetting” is exacerbated by the lack of instructional diversity in robotics datasets. It introduces Vision-LanguageAction Instruction Tuning, a paradigm centered on a curated dataset rich with diverse instructions, captions, and questionanswer pairs. This data-centric scheme ensures the model is continuously exposed to VLM-style tasks during training. Similarly, GR-3 (Cheang et al. 2025) demonstrates the power of this data-centric approach at scale by employing extensive co-training with web-scale vision-language data alongside robot and human trajectories. This shows that large-scale co-training is an effective method for producing a generalist policy that retains its foundational reasoning capabilities. 

In summary, preserving VLM knowledge can mitigate the catastrophic forgetting issue of VLAs. The path evolved from simply using reasoning outputs (DiffusionVLA (Wen et al. 2025c)) to architecturally isolating task-specific parameters (ChatVLA (Zhou et al. 2025b), ChatVLA-2 (Zhou et al. 2026b)), modifying training dynamics to protect the VLM backbone (Knowledge Insulation (Driess et al. 2026)), and enriching the training data to prevent skill atrophy (InstructVLA (Yang et al. 2025e), GR-3 (Cheang et al. 2025)). While architectural solutions like MoE and trainingdynamic solutions like gradient stopping both effectively tackle task interference, they represent different strategies: MoE creates separate “specialists” within one model, while insulation shields the generalist “brain” (reasoning) from the specialist “limb” (action). The data-centric co-training approach is complementary and has become a cornerstone of recent state-of-the-art models, suggesting a growing consensus that to keep a VLM’s abilities, one must continue to train it on VLM-style data. 

### _7.3.2 Internal world models and reasoning_ 

A key limitation of standard VLAs that utilize a behavioral cloning training scheme is their reactive and “black box” attribute, where they map observations directly to actions without explicit intermediate reasoning or planning. This approach struggles with long-horizon tasks that require anticipating future outcomes. To address this, recent research integrates predictive world models into VLAs, enabling them to reason about the future and ground their actions in an understanding of environmental dynamics. 

One line of work focuses on using visual foresight to guide action generation. Tian et al. (2025) first predicts a future visual state based on the current observation and language goal, and then use an inverse dynamics model to determine the actions needed to reach that state. By training both the visual prediction and action generation modules jointly in an end-to-end manner, the model learns a synergistic relationship where visual prediction informs action planning, and the need to generate plausible actions refines the model’s understanding of world dynamics. CoT-VLA (Zhao et al. 2025) introduces a Visual Chain-of-Thought. The model generates a subgoal image as an explicit reasoning step, which is used in conjunction with the current observation and 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

36 

language instruction to condition the final action prediction. This strategy allows the model to “think visually” about how to accomplish a task before taking action. 

WorldVLA (Cen et al. 2025) unifies the action model and world model into a single autoregressive framework, which is trained to perform two complementary tasks: (i) as an action model, it predicts actions given the current state and a goal, and (ii) as a world model, it predicts the next visual state given the current state and an action, creating a synergistic learning process that mutually enhances each other. The world model’s need to understand actions for accurate future prediction improves the action model’s grounding, while the action model’s interaction with the environment provides rich data for learning world dynamics. However, predicting entire future images is computationally expensive and can include irrelevant information (like static backgrounds). To improve efficiency, DreamVLA (Zhang et al. 2026b) proposes forecasting a compact latent “world embedding” instead of raw pixels. This embedding captures critical aspects of the future, such as object dynamics, depth, and high-level semantics, providing the policy with a concise and relevant representation for planning. To prevent interference between these different knowledge types, the model employs a block-wise structured attention mechanism, disentangling the representations and ensuring that the final action is conditioned on a clean understanding of the predicted future. 

In summary, the integration of internal world models into VLAs marks a shift from reactive to predictive control. Early methods like Seer (Tian et al. 2025) and CoTVLA (Zhao et al. 2025) established the paradigm of using pixel-level future predictions to guide actions, framing it respectively as a control problem and a cognitive reasoning step. WorldVLA (Cen et al. 2025) advances this by creating a bidirectional link, where the model learns to predict future states from actions and, conversely, actions from future states, thereby building a more complete understanding of environmental dynamics. The most recent evolution, represented by DreamVLA (Zhang et al. 2026b), addresses the computational inefficiency of pixel-level prediction by forecasting a compact representation of the future. This trajectory reflects a move from concrete visual prediction towards more abstract and efficient future reasoning. 

# _7.4 Optimization for action_ 

The representation and generation of robot actions are critical bottlenecks in VLA performance. A primary challenge with early VLA models was their reliance on discrete representations of continuous actions (like OpenVLA (Kim et al. 2025c)), which limited the fidelity and smoothness of robot movements for dexterous manipulations. To mitigate this issue, _π_ 0 (Black et al. 2025b) is proposed to shift away from discrete action tokens toward a continuous generative process, which models the distribution of entire action sequences using _flow matching_ . By adding a dedicated “action expert” module to a standard VLM backbone, _π_ 0 could generate precise and fluent continuous action chunks (50 Hz trajectories), enabling it to master highly dexterous tasks. While the flow matching approach effectively solves the action precision problem, it introduces computational overhead during training. 

Pertsch et al. (2025) observe that the poor performance of autoregressive VLA results from redundancy, as consecutive action tokens are highly correlated, which provides a weak learning signal for the next-token prediction objective. Their Frequency-space Action Sequence Tokeniser (FAST) compresses the action sequence by converting it into the frequency domain using the Discrete Cosine Transform, thereby removing temporal redundancy before tokenization. Their results demonstrate that a VLA trained with FAST could match the performance of the _π_ 0 flow-matching VLA while reducing training time by up to 5x. With precision and efficiency addressed separately, a broader question remains: “ _how can a single model generalize its actions to unseen scenarios_ ”. The answer requires a method that can efficiently train a single model on massive heterogeneous data sources while still enabling fine-grained and real-time control at deployment. _π_ 0 _._ 5 (Black et al. 2025a) answers this by _jointly_ learning discrete and continuous action heads. In the pre-training stage, it uses the FAST tokenizer (Pertsch et al. 2025) to handle diverse robotic action data at a large scale. During the post-training stage, a flow-matching action expert (as in _π_ 0) is employed for high-fidelity continuous control and efficient real-time inference. At run-time _π_ 0 _._ 5 first predicts a _high-level sub-task_ (text) and then refines it into continuous motor commands, achieving open-world manipulation such as cleaning an unseen kitchen. 

Some works explore the action generation problem from the model architectural perspective. Both autoregressive decoders and the external continuous diffusion heads used in many state-of-the-art models created an architectural disconnect between the VLM backbone and the action generation module. To create a more cohesive and scalable architecture, Discrete Diffusion VLA (Liang et al. 2025) introduces a framework to model discretized action chunks using a discrete diffusion process within a single unified transformer. This approach trains the entire model with the same cross-entropy objective used by the VLM backbone, thereby preserving pre-trained priors while enabling parallel and iterative refinement of the action chunk. This contrasted with all previous methods by treating action decoding not as a separate task for an external module, but as a native capability of the core transformer, paving the way for better scaling and architectural consistency. These approaches provide a perspective for action generation in VLAs: _control precision_ demands continuous action decoders, _scalability_ requires smarter tokenization to reduce redundancy in action sequences, and _generalization_ needs a hybrid that combines large-scale pre-training with fine-grained control. 

# _7.5 Optimization for Adaptation_ 

Although VLAs unify vision, language, and action within a single policy, the grounding between language instructions and executable actions remains sensitive to deployment conditions. When applied to new scenes, tasks, embodiments, or object distributions, a VLA must adapt to downstream settings while preserving the semantic and instruction-following priors inherited from largescale vision-language pretraining. This section focuses on adaptation methods that improve or preserve language-action 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

37 

grounding in manipulation, especially under limited data, real-time control requirements, and interactive deployment. 

A practical requirement for adaptation is the improvement of the deployability of VLA policies, ensuring responsive enough for real robot control. For example, OpenVLAOFT (Kim et al. 2025b) revisits the fine-tuning design of OpenVLA (Kim et al. 2025c) and shows that parallel decoding, action chunking, and continuous action prediction can substantially improve the responsiveness of language-conditioned control, which improves success rate by 20% on LIBERO and boosting control frequency 26x against OpenVLA. By reducing inference latency and producing temporally coherent action sequences, such designs help language-specified commands remain executable under the timing constraints of real robot control. However, improving control efficiency alone does not guarantee robust language grounding under new objects, scenes, or referring expressions. When only limited downstream demonstrations are available, adaptation should improve task-specific behavior without overwriting the semantic knowledge that supports openvocabulary instruction following. ControlVLA (Li et al. 2025c) mitigates this issue by injecting object-centric visual information into a largely frozen VLA backbone, enabling adaptation to new task-relevant objects and language references while preserving pretrained language priors. 

Nevertheless, supervised fine-tuning is constrained by the quality of the demonstrations it imitates, which may be suboptimal, incomplete, or unsafe in downstream manipulation settings. To mitigate this, some works use post-training or interaction to align language-specified goals with successful manipulation behavior. post-training methods such as ConRFT (Chen et al. 2025g) and RIPTVLA (Tan et al. 2025) refine pretrained VLAs through task rewards, online interaction, or human intervention. By incorporating downstream feedback, these methods correct failures in alignment with language goals, improve instruction-following, and strengthen the mapping from linguistic intent to physical action. Overall, languagegrounded adaptation mitigates a central challenge for VLAs, e.g., transferring broad linguistic and visual priors to new manipulation settings while maintaining reliable languageaction alignment. 

Additionally, Appendix A (Table 10) provides a consolidated classification of representative VLA models discussed in this section. It summarizes the models according to the optimization dimensions introduced in this section: perception, reasoning, action generation, and learning/adaptation, while also comparing their observation modalities, actiongeneration paradigms, policy mechanisms, pretraining settings, and evaluation scenarios. 

# **8 Comparative analysis** 

The preceding sections systematically categorized languageconditioned methodologies based on the functional role of language within the control loop. While this taxonomy clarifies _how_ language is integrated, it is equally important to analyze the structural design choices and practical tradeoffs that determine a system’s real-world feasibility. Critical 

dimensions often affect the success of a method beyond its theoretical formulation, such as the granularity of action spaces, the cost of data acquisition, system latency, and the validity of evaluation setups. Furthermore, to fully contextualize the utility of language, it is necessary to compare it with alternative task-specification modalities, such as goal images or videos. In this section, we conduct a detailed comparative analysis of representative approaches, evaluating them along five cross-cutting axes designed to highlight the fundamental engineering decisions in the field. 

- **Action granularity:** We analyze whether methods output high-level skills (a sequence of actions) or low-level torques/poses (fundamental commands that directly control a robot’s motors/limbs). This is a critical design choice that determines a system’s precision, ability to handle contact-rich tasks, and realtime feasibility. It reveals the trade-off between longhorizon planning (coarse actions) and fine-grained control (fine actions, e.g., joint torques). 

- **Data and supervision regimes:** We compare methods based on their data sources (e.g., expert demos, play data, web data) and supervision signals (e.g., human labels, learned rewards, FM-generated code). This axis is crucial as it directly impacts annotation cost, scalability, and a method’s ability to generalize to outof-distribution scenarios. 

- **System cost and latency:** We now explicitly compare the computational and memory costs of different approaches, both at training and inference time. This is a vital organizing principle because real-world robots must operate under strict hardware and latency constraints. This axis highlights the practical gap between theoretically powerful models and deployable systems. 

- **Environments and evaluations:** We compare the benchmarks, tasks, and hardware used for evaluation. We further discuss the manipulation task categories to characterize task difficulty. This axis aims to understand the external validity of a method’s claims, highlighting the critical distinction between results achieved in controlled simulations versus the complexities of the real world. 

- **Task Specification:** We compare methods based on whether they condition on language instructions or other modality specifications (e.g., goal images/videos). This axis reveals the trade-offs between the expressiveness and flexibility of language versus the directness and precision of visual goals. 

To support this cross-sectional comparison, Appendix A (Tables 11-12) provides a unified tabular summary of representative language-conditioned robotic manipulation approaches discussed across Sections 4-6. The tables consolidate key implementation and evaluation dimensions, including benchmarks or simulation engines, language and perception modules, real-world validation, and whether a method relies on foundation models, reinforcement learning, imitation learning, or motion planning. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

38 

# _8.1 Action granularity_ 

Action granularity denotes the resolution of the control signal produced by the learned component, defining the end-to-end coverage of the learning method. We consider three levels: skill-level (selects pre-defined skills such as “open drawer”), trajectory-level action (predicts waypoints/poses), and low-level control (outputs high-rate joint torques/velocities). 

### _8.1.1 Skill-level actions_ 

Skill-level actions represent the nature composition of the language instruction. Representative approaches issue highlevel skills or API calls rather than time-parameterized waypoints/poses of the motion planner or torques of the robot’s joints. The planner-level LLMs such as SayCan (Brohan et al. 2023b), Code as Policies (Liang et al. 2023), Inner Monologue (Huang et al. 2023c), ReKep (Huang et al. 2025b) follows this design. Additionally, task and motion planning (TAMP) approaches, such as PDDLStream (Garrett et al. 2020), provide the backbone that binds these symbolic steps to geometric feasibility. This granularity matches language well, where skills are “natural language units”, showing strong constitutionality and interpretability. The main failure mode is skill library uncoverage, which means the policy-asked skill primitive is missing in the library. In practice, systems address these failures with affordance or value filters (Brohan et al. 2023b; Huang et al. 2025b), schema validation for generated code (Liang et al. 2023; Singh et al. 2023), and scene-aware success checks with replaning (Brohan et al. 2023b; Liang et al. 2023; Huang et al. 2023c). 

### _8.1.2 Trajectory-level actions_ 

Trajectory-level actions involve outputting end-effector waypoints or trajectories, rather than skills. Many languageconditioned IL approaches (Lynch and Sermanet 2021; Jang et al. 2022; Wang et al. 2023a; Mees et al. 2023; Zhou et al. 2024a) fall here: they map an image observation and language instruction to either a next waypoint or an entire trajectory to achieve the described goal. Similarly, some language-conditioned RL methods (Bing et al. 2023a; Pang et al. 2023; Aljalbout et al. 2025) optimize a trajectory that satisfies a language-specified reward or success condition. Diffusion models have also emerged as powerful trajectory generators, learning a distribution over motion sequences that can be sampled by iterative refinement. For instance, Diffusion Policy (Chi et al. 2023) and subsequent variants (Ze et al. 2024; Lu et al. 2024) generate multi-step actions by denoising random trajectories, guided by language or goal images. This granularity lies between skill and low-level control, which is expressive enough for contact and geometry while still amenable to language conditioning via goals, keyframes, or affordance hints. The main failure modes are covariate shift that yields trajectory drift and compounding error over long horizons. Common mitigations include receding-horizon replanning (Nair et al. 2022; Huang et al. 2023b), which optimizes a short-horizon trajectory, executes only the first slice, resenses, and replans; and intervention-based dataset aggregation (Jang et al. 2022), which logs brief human 

corrections during rollouts and incorporates them into the training set to mitigate distribution (covariate) shift. 

### _8.1.3 Low-level control_ 

A challenge of many language-conditioned manipulation tasks, such as dexterous manipulations (Ma et al. 2024), or handing fragile/deformable objects (Kobayashi et al. 2025), which are defined by physical contact and force dynamics, rather than just spatial positions. This motivates the need for integrating language with low-level torque/force control, which directly commands the robot’s joint torques at high control frequency (e.g., 100Hz+) that allows robots to perform contact-rich tasks with greater precision and compliance. Current methods integrate this capability in different ways, including reinforcement learning, imitation learning, and foundation models, which present unique challenges and opportunities. A primary bottleneck for reinforcement learning is the difficulty of manual reward design. Crafting reward functions that guide a policy to learn a complex, dynamic, and contact-rich skill (e.g., pen spinning) is extremely hard. EUREKA (Ma et al. 2024) mitigates this issue by using the LLM’s coding and zero-shot generation capabilities to perform evolutionary optimization over the reward function code itself. EUREKA successfully generates reward functions that enabled a simulated robot hand to learn complex low-level manipulation skills (like spinning a pen). While RL is powerful, imitation learning from human demonstrations is often more data-efficient. The core problem for IL in this domain is that standard kinesthetic teleoperation only captures position data, failing to record the demonstrator’s force intent. To solve this, BiLAT (Kobayashi et al. 2025) introduces a framework based on bilateral control, a teleoperation setup that records not only joint position and velocity but also joint torque data. The key insight is then to condition this multimodal policy on natural language instructions (like “softly/strongly twist the sponge”), explicitly modulating its force output. 

The rise of foundation models introduces new challenges, such as creating a unified model for contact physics. ManiFoundation Model (Xu et al. 2024) addresses this by framing manipulation as a problem of “contact synthesis”. It takes object and robot point clouds as input and predicts the optimal contact points and contact forces required to achieve a desired target motion, offering a general solution that bypasses direct torque prediction. Another challenge is integrating low-level torque control into large pretrained VLA models (which are typically pose-based). TAVLA (Zhang et al. 2025d) explores this by elucidating the design space for creating “torque-aware” VLAs, providing several insights. They find that (i) torque signals are best integrated into the action decoder, as they align better with other proprioceptive signals like joint angles, (ii) torque history can be summarized into a single token for temporal context, and (iii) performance improves by adding an auxiliary task of predicting future torque, which helps the model build a physically grounded internal representation. 

Despite these advances, many language-conditioned policies still operate one step higher, predicting the trajectory of the end-effector poses and delegating torques to the execution layer. We identify two primary reasons for this: data labeling 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

39 

and the sim-to-real gap. Collecting clean, time-aligned torque labels with accurate force sensing and per-joint calibration is expensive, whereas trajectory data can be easily obtained via teleoperation and is less noisy. Additionally, simulating friction, compliance, and actuator dynamics can be challenging. Torque-level policies trained in simulation often overfit to the simulator’s specific physics, whereas trajectory outputs tracked by a robust low-level controller can result in a more seamless transfer. 

# _8.2 Data and supervision regime_ 

The data and supervision regime specifies where training signals come from and how they are provided. We use it to compare annotation cost, reachable-state coverage, and outof-distribution (OOD) behavior across methods. 

### _8.2.1 Data sources_ 

Language-conditioned manipulation relies on two broad categories of data: (i) Robotic interaction data (direct experience) and (ii) Web-scale data (human-curated content). Robotic data is often further split by how structured it is: 

**Expert demonstrations:** Demonstrations of tasks (via teleoperation (Mandlekar et al. 2018), kinesthetic teaching (Calinon and Billard 2007), or VR control (Zhang et al. 2018)) paired with language instructions labeled by experts (Jang et al. 2022; Brohan et al. 2023a). They are high-quality and task-directed, making them effective for imitation learning. However, they are costly to collect and scale. Each demonstration must be carefully performed and often manually labeled with a description. Despite the cost, several works have compiled demonstration datasets for dozens of manipulation tasks (e.g., RT-1 (Brohan et al. 2023a)’s dataset with 130k demos), enabling supervised policies to learn a range of skills from “open drawer” to “flip light switch”. 

**Unstructured play data:** This refers to large collections of robot experience without strict task labels – e.g., a robot or a human teleoperator freely interacts with objects, producing a wide variety of behaviors. Such play or onrobot logs are much easier to gather at scale since they don’t require labeling each sequence with a specific instruction. Despite the convenience of collecting these data, making use of them conditioned on language becomes a challenge. Recent techniques address this by relabeling play data with language post-hoc. For instance, Learning from Play (Lynch et al. 2020) introduces relabeling unlabeled trajectories with goal images. Lynch and Sermanet (2021); Lynch et al. (2023) combine these play data with goal images and 1% language-labeled data with language instruction to train a language-conditioned policy, similar to HULC and HULC++ (Mees et al. 2022a, 2023). Such play+language strategies significantly expand state coverage and diversity compared to limited expert demos and have therefore also been explored for extracting affordances (Borja-Diaz et al. 2022) and learning goal-conditioned policies via offline reinforcement learning (Rosete-Beas et al. 2022). 

**Web-scale data:** Internet data provides broad priors that cut robot data needs. Image–text pretraining (Radford et al. 2021; Alayrac et al. 2022) combines visual and textual modalities and is helpful for language grounding in current 

perception. Text-only pretraining (Chowdhery et al. 2023; Brown et al. 2020) offers a rich source of common-sense knowledge and reasoning abilities. 

### _8.2.2 Supervision_ 

Supervision indicates how robots learn from data. We classify supervision by the form of the learning signal it provides to the learner entity. This yields three types of supervision paradigms for language-conditioned manipulation systems. Some approaches utilize a combination of these supervision paradigms. 

**Targets labels** The targets here are the per-sample values (actions, subgoals, success/value labels) the learner is asked to match or predict during training. For example, recent generalist policies learn from these labels via imitation learning. RT-2 (Zitkovich et al. 2023) co-finetunes a webscale VLM jointly with robot trajectories and then supervises action outputs, improving zero-shot instruction following in the real world. OpenVLA (Kim et al. 2025c), Octo (Octo Model Team et al. 2024) follow the same supervised recipe, leveraging strong pretrained vision backbones and more training data. 

**Outcome evaluations:** In outcome-driven supervision, the learner optimizes a scalar evaluation from execution (rewards, success, preferences, penalties). The scalar evaluation rates the quality of a state, action, or trajectory. It is used to drive learning without prescribing an exact target action. The learner then maximizes (or minimizes) this number via RL/MPC or on-policy updates. The evaluation can be manually defined (Silva et al. 2021) or realized by VLMs as success detectors (Du et al. 2023a), LLMs for reward generation (Yu et al. 2023c; Ma et al. 2024). 

**Auxiliary supervision** Auxiliary self-supervision shapes the learner without supervising the primary task directly. These additional learning objectives have two main advantages: (i) Ensuring important information flows in the neural networks, which is critical for decision-making. (ii) Guiding the direction of gradient descent during training can potentially lead the neural network to a more optimal location in the parameter space. We classify them into three categories: **(i) visual attention** , which learns what/where to act via language-conditioned affordances and attention (e.g., region–text alignment (Shridhar et al. 2022; Mees et al. 2023), handle/keypoint and graspability maps (Sundaresan et al. 2023; Mo et al. 2021; Sundermeyer et al. 2021)); **(ii) reconstruction** , which learns how to represent robust scenario representation through reconstruct image/video (Shridhar et al. 2023; Nair et al. 2020; Rahmatizadeh et al. 2018; Ebert et al. 2018), and **(iii) future prediction** , which learns what will happen next via nextstates prediction (Paxton et al. 2019; Ebert et al. 2018; Bu et al. 2024) in pixel or latent space and keyframe prediction (Xian et al. 2023) to stabilize long-horizon behavior and expose subgoals for planning. 

Many systems blend supervision paradigms across training phases. We write the objective as 

_L_ final = _λ_ 1 _L_ targets + _λ_ 2 _L_ evaluations + _λ_ 3 _L_ auxiliary, (18) 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

40 

where _L_ targets, _L_ evaluations, and _L_ auxiliary correspond to fixed targets, outcome evaluations, and auxiliary losses, respectively. _λ_ 1 _, λ_ 2, and _λ_ 3 are time-dependent curriculum weights. A common schedule is to warm-start with fixed targets (imitation) for stability ( _λ_ 1 _↑_ ), anneal in outcome evaluations (rewards/preferences/validators) for robustness and long-horizon credit assignment ( _λ_ 2 _↑_ as _λ_ 1 _↓_ ), and cotrain with auxiliaries to improve grounding and invariances ( _λ_ 3 small but nonzero throughout). 

# _8.3 System cost and latency_ 

### _8.3.1 Training cost_ 

Scaling models and data improve capability and generalization, as shown by LLMs. Recent robotics systems increasingly ride these trends. However, scaling significantly raises the training cost. More GPU hours are needed to leverage foundation models in the robotic domain. Three training strategies are identified: (i) Training from scratch, (ii) Finetuning, and (iii) Prompt engineering. 

**Training from scratch:** This approach builds languageconditioned manipulation models from the ground up, without leveraging any prior pre-training on external data. Large models are initialized with random weights and trained end-to-end on robot-specific datasets. The training cost is enormous because the model must learning vision, language, and control solely from task data. For example, the Gato (Reed et al. 2022) agent is a pioneering visionlanguage-action model trained from scratch on tokenized images, text, and actions, achieving multi-task skills entirely from its training set. Such scratch-trained models demonstrate that it is possible to integrate language and control without foundations, while they also show the requirements for large training datasets and GPU resources (Brohan et al. 2023a; O’Neill et al. 2024) to achieve downstream generalization ability. 

**Fine-tuning:** Rather than start from scratch, this strategy adapts pre-trained foundation models to the robot manipulation domain. A model that has already learned broad visual and linguistic patterns is used as a backbone, then fine-tuned on robot-specific data (possibly with additional new layers or using LoRA (Hu et al. 2022) strategy). The key advantage is leveraging prior knowledge: the foundation model’s understanding of semantics and vision greatly reduces the needed robot data and improves generalization to new conditions. For instance, Google’s RT-2 (Zitkovich et al. 2023) policy builds on pre-trained vision-language representations (PaLIX (Chen et al. 2023d) and PaLM-E (Driess et al. 2023)) and fine-tunes them with robotic data, resulting in substantially better performance on novel objects and instructions compared to a scratch-trained policy, especially when those examples remain close to the pre-training distribution. The trade-offs include overfitting and forgetting that the model can lose some of its prior knowledge if the domain is narrow and the fine-tuning data is limited. 

**Prompt engineering :** In this strategy, the FMs remain frozen and is invoked at inference via prompting. An LLM proposes a sequence of subtasks that a robot executes 

**Table 6.** The inference cost and latency for sampled approaches. _Cloud_ denotes inference on remote compute; ‘–’ indicates not reported; ‘*’ marks values inferred from architectural details. 

|System|Model|Params|Hardware|Latency|Cloud|
|---|---|---|---|---|---|
|RT-1Brohan et al.|VLA policy|35M|-|_∼_3Hz|✗|
|RT-2-55BZitkovich et al.|VLA policy|55B|TPU|1-3Hz|✓|
|RT-2-5BZitkovich et al.|VLA policy|5B|-|1-3Hz|✗|
|OpenVLAKim et al.|VLA policy|7B|RTX4090|3-6Hz|✗|
|CLIP-RTKang et al.|VLA policy|1B|-|8-16Hz|✗|
|PaLM-SayCanBrohan et al.|LLM planner|540B|TPU|-|✓|
|PaLM-EDriess et al.|Embodied VLM|562B|TPU|-|✓|
|Diffusion PolicyChi et al.|Diffusion policy|_∼_200M<sup>_∗_</sup>|-|_∼_1Hz|✗|
|DP3Ze et al.|Diffusion policy|_∼_150M<sup>_∗_</sup>|-|5-6Hz|✗|
|ManiCMLu et al.|Diffusion policy|_∼_200M<sup>_∗_</sup>|RTX4090|_∼_50-60Hz|✗|


using a library of skill primitives (e.g., SayCan (Brohan et al. 2023b) or Code-as-Policies (Liang et al. 2023)). Because the FM is not fine-tuned, no additional training on robot data is required. The planner simply queries a pretrained LLM, which can generate coherent plans with prompts. The prompted, frozen-FM planners can call very large LLMs/VLMs and inherit broad open-ended knowledge so that they show strong generalization across instructions and scenes. However, since the model is decoupled from the embodiment, the planning is typically open-loop and prone to hallucinated or infeasible steps, struggling on longhorizon tasks. 

### _8.3.2 Inference cost_ 

At deployment time, the inference time largely depends on the model scale and the computation resources. Systems that prompt a frozen LLM/VLM inherit the reasoning breadth of very large FMs but typically run open-loop, so plan proposals arrive on a seconds-scale and must be grounded with affordance/validation or closed-loop replanning. For end-toend VLA policies, fine-tuning larger backbones improves generalization but increases per-step compute and memory, making multi-Hz closed-loop control harder unless the model is compressed or carefully engineered, as shown in Table 6. Diffusion policy may incur additional runtime tax, since actions are sampled with multiple denoising steps, which can be mitigated by utilizing fast samplers (Chi et al. 2023; Ze et al. 2024) (e.g., DDIM/DPMSolver) or consistency distillation (Lu et al. 2024). We flag realtime performance as a core hurdle for large LLM/VLMbased systems. Although cloud computation can be used for inference to address on-board hardware limits, it makes performance contingent on network reliability, introducing latency jitter and drop-out failure modes. 

# _8.4 Environments and evaluations_ 

### _8.4.1 Simulations and benchmarks_ 

A variety of task domains and benchmarks are developed to assess the novel methodologies’ performance. In this section, we delve into the environmental settings and benchmarks within the realm of language-conditioned robot manipulation. Simulation plays a pivotal role in accelerating advancements in robot manipulation by enabling rapid prototyping, thorough testing, and exploring complex scenarios that might be challenging to replicate in the real world. We introduce several simulators widely used 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

41 

**Table 7.** Comparison of Simulation Engines. 

|Simulator|Description|Use Cases|
|---|---|---|
|PyBullet (Coumans and Bai<br>2016–2021)|With its origins rooted in the Bullet physics engine, PyBullet transcends the<br>boundaries of conventional simulation platforms, offering a wealth of tools<br>and resources for tasks ranging from robot manipulation and locomotion to<br>computer-aided design analysis.|Shao et al. (2021) and Mees et al.<br>(2023, 2022a) leverage PyBullet to<br>build a table-top environment to<br>conduct object manipulation tasks.|
|MuJoCo<br>(Todorov<br>et<br>al.<br>2012)|MuJoCo, short for “Multi-Joint dynamics with Contact”, originates from<br>the vision of creating a physics engine tailored for simulating articulated<br>and deformable bodies. It has evolved into an essential tool for exploring<br>diverse domains, from robot locomotion and manipulation to human<br>movement and control.|Lynch and Sermanet(2021);Lynch<br>et al. (2020) build a table-top<br>environment based on MuJoCo.<br>The famous benchmark Meta-world<br>also builds on this simulator.|
|CoppeliaSim (Rohmer et al.<br>2013)|CoppeliaSim offers a comprehensive environment for simulating and<br>prototyping robotic systems, enabling users to create, analyze, and optimize<br>a wide spectrum of robotic applications. Its origins as an educational tool<br>have evolved into a full-fledged simulation framework, revered for its<br>versatility and user-friendly interface.|Stepputtis<br>et<br>al.<br>(2020)<br>lever-<br>age CoppeliaSim to construct an<br>environment where the agent can<br>manipulate cups and bowls with<br>different sizes and colors.|
|NVIDIA Omniverse|NVIDIA Omniverse offers real-time physics simulation and lifelike<br>rendering, creating a virtual environment for comprehensive testing and<br>fine-tuning of robot manipulation algorithms and control strategies, all prior<br>to their actual deployment in the physical realm.|e.g., LEMMA benchmark (Gong<br>et al. 2023a) builds a multi-robot<br>environment based on NVIDIA<br>Omniverse.|
|Unity|Unity is a cross-platform game engine developed by Unity Technologies.<br>Renowned for its user-friendly interface and powerful capabilities, Unity<br>has become a cornerstone in the worlds of video games, augmented reality<br>(AR), virtual reality (VR), and simulations.|Alfred (Shridhar et al. 2020), which<br>is based on Ai2-thor (Kolve et al.<br>2017) hausehold environment, use<br>Unity game engine.|
|UniSim (Yang et al. 2024c)|Different from physical simulators, UniSim is learned by real-world<br>interactions through generative modeling. It leverages diverse, naturally<br>rich datasets such as abundant objects in image data, densely sampled<br>actions in robotics data, and varied movements in navigation data to<br>simulate both high-level instructions and low-level controls.|UniSim represents the pioneering<br>attempt to build a simulator based<br>on generative models.|


in the field of robot manipulations, as shown in Table 7. Benchmarks are important for assessing and advancing the capabilities of robotic systems. We explore the fundamental significance of benchmarks in the domain of robot manipulation based on the above simulation engine or a real-world setting. A comparison is shown in Table 8, and illustrations of these benckmarks as shown in Figure 17. Benchmarks in both simulation and real-world environments are listed as follows. 

**CALVIN** (Mees et al. 2022b): Composing Actions from Language and Vision (CALVIN) is an open-source simulated benchmark to learn long-horizon language-conditioned tasks constructed on PyBullet. It has four different yet structurally related environments so that it can be used for general playing and evaluating specific tasks. 34 different tasks can be performed under such environments. It has two different evaluation metrics, namely Multi-Task Language Control (MTLC) and Long-Horizon MTLC (LH-MTLC). MTLC aims to verify how well the learned multi-task languageconditioned policy generalizes to 34 manipulation tasks; LH-MTLC aims to verify how well the learned multitask language-conditioned policy can accomplish several instructions in a row. Mees et al. (2022a, 2023) and Zhou et al. (2024a) evaluate their models on this benchmark. 

**Meta-World** (Yu et al. 2020): Meta-World is a collection of 50 diverse robot manipulation tasks built on the MuJoCo physics simulator. It contains two widely used benchmarks, namely, ML10 and ML45. The ML10 contains a subset of the ML45 training tasks, which are split into 10 training tasks and 5 test tasks, and the ML45 consists of 45 training tasks and 5 test tasks. It used to be a platform to evaluate 

the performance of meta-reinforcement learning. Bing et al. (2023a); Silva et al. (2021); Goyal et al. (2021); Nair et al. (2022) use Meta-world to test the performance of their language-conditioned models. 

**RLBench** (James et al. 2020): This benchmark includes 100 completely unique, hand-designed tasks ranging in difficulty, which share a common Franka Emika Panda robot arm, featuring a range of sensor modalities, including joint angles, velocities, and forces, an eye-in-hand camera, and an over-the-shoulder stereo camera setup. RLBench is built around a CoppeliaSim/V-REP, allowing for drag-and-drop style scene building and a whole host of robotic tools, such as inverse/forward kinematics, motion planning, and visualizations. Shridhar et al. (2023) use RLbenchmark to evaluate their models’ performance on 18 tasks. 

**VIMAbench** (Jiang et al. 2023): VIMAbench is a simulation benchmark built on the Ravens simulator (Zeng et al. 2021) that supports multimodal prompts (text + images) for 17 tabletop manipulation task templates. It provides nearly 650,000 expert trajectories along with a four-level hierarchical evaluation protocol that progresses from randomized object placements to entirely novel tasks, enabling a systematic assessment of an agent’s generalization capability. The benchmark aims to support the development of generalist robot learning agents that can handle a wide variety of tasks specified via intuitive multimodal interfaces. For example, Li et al. (2024b) applies VIMAbench to assess a new policy for multimodal language-conditioned robot control and reports meaningful performance gains. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

42 

**Table 8.** Comparison of existing language-conditioned robot manipulation benchmarks. 

|Benchmark|Simulation Engine or|Embodiment|Data Size|Observations|Tool u|sed<br>Multi-agents<br>Long-horizon|
|---|---|---|---|---|---|---|
||Real-world Dataset|||RGB<br>Depth<br>Masks|||
|CALVIN (Mees et al. 2022b)|PyBullet|Franka Panda|2400k|✓<br>✓<br>✗|✗|✗<br>✓|
|Meta-world (Yu et al. 2020)|MuJoCo|Sawyer|-|✓<br>✗<br>✗|✗|✗<br>✗|
|RLBench (James et al. 2020)|CoppeliaSim|Franka Panda|-|✓<br>✓<br>✓|✗|✗<br>✓|
|VIMAbench (Jiang et al. 2023)|PyBullet|UR5|650K|✓<br>✗<br>✗|✗|✗<br>✓|
|LoHoRavens (Zhang et al. 2023)|PyBullet|UR5|15k|✓<br>✓<br>✗|✗|✗<br>✓|
|ARNOLD (Gong et al. 2023b)|NVIDIA Omniverse|Framka Panda|10k|✓<br>✓<br>✓|✗|✗<br>✓|
|RoboGen (Wang et al. 2024d)|PyBullet|Multiple|-|✓<br>✗<br>✗|✓|✓<br>✓|
|LIBEROLiu et al.(2023a)|MuJoCo|Franka Panda|6.5k|✓<br>✗<br>✗|✗|✗<br>✓|
|Open X-Embodiment (O’Neill et|al. 2024)<br>Real-world Dataset|Multiple|2419k|✓<br>✓<br>✗|✗|✗<br>✓|
|DROID (Khazatsky et al. 2024)|Real-world Dataset|Franka Panda|76k|✓<br>✓<br>✗|✗|✗<br>✓|
|Galaxea Open-world (Jiang et al.|2025b)<br>Real-world Dataset|Galaxea R1 Lite|100k|✓<br>✓<br>✗|✗|✗<br>✓|
|CALVIN(Mees et al. 2022b)|Meta-world(Yu et al. 2020)|RLbench(James e|t al. 2020)|VIMAbench(Jiang et al.|2023)|LoHoRavens(Zhang et al. 2023)|
|ARNOLD(Gong et al. 2023b)|RoboGen(Wang et al. 2024d)<br>Op|en X-Embodiment(O’|Neill et al. 202|4)<br>DROID(Khazatsky et al.|2024)<br>G|alaxea Open-world(Jiang et al. 2025b)|


**Figure 17.** The illustration of various benchmarks. 

**LoHoRavens** (Zhang et al. 2023): LoHoRavens is built upon the Ravens simulator (Zeng et al. 2021) and contains ten long-horizon language-conditioned tasks in total. The tasks are split into seen tasks and unseen tasks to evaluate the robot’s generalization performance. Unlike VIMAbench, which primarily focuses on short-horizon tasks, this benchmark emphasizes long-horizon scenarios where the robot must perform at least five sequential pickand-place actions to accomplish a high-level instruction. Meng et al. (2025c) build upon this benchmark to validate their code generation framework. 

**ARNOLD** (Gong et al. 2023b): ARNOLD is built on NVIDIA Omniverse, equipped with photo-realistic and physically accurate simulation, covering 40 distinctive objects and 20 scenes. It comprises 8 language-conditioned tasks that involve understanding object states and learning policies for continuous goals, and provides 10,000 expert demonstrations with diverse template-generated language instructions based on thousands of human annotations. Its main strength lies in its high visual realism and detailed annotations, which enable richer language-grounded manipulation studies. However, its limited scale and task diversity make it less suitable for developing broadly generalizable policies across varied robots and environments. For example, Lee et al. (2025) use ARNOLD to train and evaluate their framework in dynamic scenes. 

**RoboGen** (Wang et al. 2024d): RoboGen is an automated pipeline that utilizes the embedded common sense and generative capabilities of the foundation models (ChatGPT, Alpaca (Taori et al. 2023)) for automatic task, scene, and training supervision generation, leading to diverse robotic skill learning at scale. RoboGen considers tasks including rigid object manipulation, soft body manipulation, and 

legged locomotion. In addition, RoboGen integrates several functions, including Task Proposal, Scene Generation, Training Supervision Generation, and Skill Learning. 

**LIBERO** (Liu et al. 2023a): LIBERO is a simulation benchmark originally for lifelong language-conditioned robot manipulation. It introduces a procedural task generation pipeline that automatically creates infinite manipulation scenarios with natural language instructions, enabling studies of knowledge transfer under distribution shifts in objects, spatial layouts, and task goals. The benchmark consists of four curated task suites based on Franka Panda (LIBERO-SPATIAL/-OBJECT/-GOAL/-100), totaling 130 high-quality, language-conditioned tasks with human-teleoperated demonstrations. Although LIBERO was originally designed for lifelong imitation learning, it has now become a widely used simulation benchmark for evaluating the reasoning and task generalization capabilities of VLA models (Kim et al. 2025b; Zhao et al. 2025; Cen et al. 2025). 

**Open X-Embodiment** (O’Neill et al. 2024): Open X- Embodiment is a real-world large-scale dataset, which is assembled from 22 different robots collected through a collaboration between 21 institutions, demonstrating 527 skills and 160266 tasks. Over 2M+ robot trajectories are stored in RLDS data format, which stores data in serialized TFRecord files and supports diverse action spaces and input modalities across different robot setups, including varying configurations of RGB cameras, depth sensors, and point clouds. Open X-Embodiment is currently one of the few realworld datasets offering large-scale, language-conditioned robot manipulation data with broad diversity in both robot embodiments and task distributions. Recent VLA models have widely adopted it for large-scale pretraining (Kim et al. 2025c; Black et al. 2025b,a). 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

43 

**DROID** (Khazatsky et al. 2024): Distributed Robot Interaction Dataset (DROID) is a real-world, large-scale, in-the-wild robot manipulation dataset comprising 76k teleoperated trajectories ( _≈_ 350 hours) collected across 564 scenes, 52 buildings, and 86 tasks. Each episode records synchronized observations from three RGB stereo camera streams (two external ZED 2 cameras and one wristmounted ZED Mini), depth maps, camera calibration, lowlevel robot states, and crowd-sourced natural language instructions. DROID is collected with a standardized Franka Panda platform with a Robotiq 2F-85 gripper via VR-based teleoperation, providing diverse scenes and viewpoints that support reproducibility, 3D reasoning, and robust policy generalization. _π_ 0 _._ 5 (Black et al. 2025a) utilize this dataset for fine-tuning and real-world evaluation. 

**Galaxea Open-World Dataset** (Jiang et al. 2025b): This dataset is a real-world open-world manipulation dataset containing 100k teleoperated trajectories ( _≈_ 500 hours) across 150 tasks and 50 diverse scenes with over 1,600 unique objects. Data is collected using the Galaxea R1 Lite, a mobile bimanual robot with 23 DoF, equipped with a head stereo camera and dual wrist cameras. All demonstrations are recorded through isomorphic teleoperation and annotated with fine-grained subtask-level language labels, ensuring consistent embodiment, multimodal alignment, and highquality data for policy learning. This real-world dataset provides a valuable foundation for fine-tuning humanoidbased, bi-manual VLA models. 

While recent progress in language-conditioned robot manipulation has produced a growing number of simulators, benchmarks, and real-world datasets, the field still lacks a unified evaluation protocol that can fairly quantify how accurate language grounding and contextual understanding contribute to task performance (Liu et al. 2023a). Current benchmarks often focus on task success rates (Yu et al. 2020; James et al. 2020; Jiang et al. 2023) but overlook semantic comprehension and context knowledge transfer between tasks (Black et al. 2025a; Meng et al. 2025a). Furthermore, there remains a pressing need for large-scale, real-world datasets that encompass a wider variety of embodiments, environments, and task distributions to support robust and generalizable language-conditioned robotic manipulation learning (O’Neill et al. 2024; Black et al. 2025a). 

### _8.4.2 Manipulation Task Families_ 

Language-conditioned manipulation methods are evaluated on diverse task families with substantially different sources of difficulty. Therefore, direct comparison based only on reported task success can be misleading, as performance may reflect not only algorithmic capability but also the complexity of the underlying benchmark. For example, benchmarks dominated by object recognition and shorthorizon pick-and-place primarily evaluate semantic grounding and visuomotor control, whereas tasks involving contactrich interaction, deformable objects, or extended action sequences impose additional requirements on physical interaction modeling, temporal reasoning, and error recovery. To avoid conflating algorithmic capability with task difficulty, we group the manipulation tasks considered in this survey 

into three broad families, namely, _Object-centric manipulation_ , _Interaction-centric manipulation_ , and _Long-horizon manipulation_ (Table 9). This grouping is evaluation-oriented rather than a strict taxonomy of robot motions. The three task families correspond to different dominant sources of difficulty in language-conditioned manipulation. 

**Object-centric manipulation** refers to tasks in which the main objective is to identify, grasp, move, arrange, or reorient one object. Typical examples include object relocation, object sorting, stacking, and tabletop rearrangement. These tasks usually require grounding language instructions to object identities, attributes, spatial relations, grasp points, and target poses. Representative instructions include “move the red block into the bowl”, “Stack the red block on the blue one”. This category is widely used to evaluate visual-language grounding. Some early benchmarks, such as Meta-World (Yu et al. 2020) and RLBench (James et al. 2020), mainly focus on this category to evaluate whether an agent can identify the target object, ground the language instruction, and determine how to approach, grasp, and place the object. In these settings, the physical interaction between the robot end-effector and the object is often simplified. The manipulated objects are often rigid and geometrically simple, reducing the complexity of contact dynamics and allowing the evaluation to focus primarily on object grounding, spatial reasoning, and short-horizon visuomotor control. 

**Interaction-centric manipulation** focuses on the interaction of the agent with the physical world. It includes articulated-object manipulation, deformable-object manipulation, and tool-mediated Manipulation. Representative instructions include “insert the plug”, “fold the cloth”, “use the spatula to flip the object”, and “twist the sponge gently”. Compared with object-centric manipulation, these tasks require stronger physical grounding, including 3D spatial reasoning, force control, tactile feedback, deformation modeling, and tool-object affordance reasoning. Representative benchmarks include ARNOLD (Gong et al. 2023b), with language-guided manipulation of articulated household objects such as drawers, cabinets, doors, ovens, and refrigerators; and RoboGen (Wang et al. 2024d), with automatically generated tasks involving articulated objects, tool use, and deformable or soft-object interactions. Large-scale realworld datasets such as Open X-Embodiment (O’Neill et al. 2024), DROID (Khazatsky et al. 2024), and Galaxea OpenWorld (Jiang et al. 2025b) also contain these tasks across diverse scenes and robot embodiments. 

**Long-horizon manipulation** focuses on tasks that require the robot to complete a sequence of interdependent manipulation steps to satisfy a high-level instruction. It includes multi-step object rearrangement, sequential household manipulation, and mobile manipulation. Representative instructions include “tidy up the table”, “prepare a cup of coffee”, “bring me the red cup from the kitchen”, and “open the drawer, pick up the blue block, place it inside, and then close the drawer”. These tasks require task decomposition, subgoal sequencing, memory, semantic reasoning, navigation-manipulation coupling, closed-loop replanning, and failure recovery. Representative benchmarks include CALVIN (Mees et al. 2022b), LoHoRavens (Zhang et al. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

44 

**Table 9.** Three main categories of manipulation tasks in language-conditioned robot manipulation. Some benchmarks span multiple task families. 

|**Task category**|**Task Examples**|**Representative Benchmarks**|**Illustration**|
|---|---|---|---|
|**Object-centric**|Object relocation,<br>Stacking,<br>Pose Manipulation|Meta-World (Yu et al. 2020),<br>RLBench (James et al. 2020),<br>VIMAbench (Jiang et al. 2023)||
|**Interaction-centric**|Articulated-object Manipulation,<br>Deformable-object Manipulation,<br>Tool-mediated Manipulation|ARNOLD (Gong et al. 2023b),<br>RoboGen (Wang et al. 2024d),<br>Open X-Embodiment (O’Neill<br>et al. 2024)||
|**Long-horizon**|Multi-step Object Rearrangement,<br>Household Manipulation,<br>Mobile Manipulation|CALVIN (Mees et al. 2022b),<br>LoHoRavens (Zhang et al. 2023),<br>LIBERO (Liu et al. 2023a),<br>Open X-Embodiment (O’Neill<br>et al. 2024), DROID (Khazatsky<br>et al. 2024), Galaxea Open-<br>World (Jiang et al. 2025b)||


2023), and LIBERO (Liu et al. 2023a), which focus on long-horizon tabletop tasks, requiring to complete multiple sequential tasks and evaluate the completeness. Open X- Embodiment (O’Neill et al. 2024), DROID (Khazatsky et al. 2024) and Galaxea Open-World (Jiang et al. 2025b) provide diverse long-horizon manipulation demonstrations across different scenes, objects, and embodiments in the real world. This category is therefore particularly useful for evaluating whether a trained agent can maintain robust execution under long-horizon error accumulation and decompose complex high-level instructions into feasible subtask sequences. 

In summary, these categories correspond to increasingly rich requirements in semantic grounding, physical interaction, and temporal reasoning; however, they are not mutually exclusive and should not be interpreted as a strict linear difficulty hierarchy. For instance, an articulated-object task may also require long-horizon planning, and deformableobject manipulation may be more challenging than a short multi-step rigid-object task. Nevertheless, this taxonomy provides a useful lens for interpreting reported performance, i.e., strong results on object-centric benchmarks primarily indicate effective visual-language grounding and shorthorizon visuomotor control, whereas interaction-centric and long-horizon benchmarks further evaluate physical interaction modeling, planning, memory, and closed-loop robustness. 

# _8.5 Task Specification_ 

While this survey primarily focuses on _language-conditioned_ manipulation, it is important to position language as one task-specification modality within a broader multi-modal landscape. In parallel to language, a substantial body of work specifies tasks using _goal images_ or _demonstration videos_ (e.g., image/video-conditioned manipulation). These visual modalities occupy analogous functional roles in the manipulation control loop, directly aligning with our established taxonomy: (i) defining _state evaluation_ signals (rewards/costs) to quantify task progress (Section 4), (ii) serving as a _policy condition_ that directly shapes action generation (Section 5), and (iii) providing structural priors for _cognitive planning_ in long-horizon tasks (Section 6). 

In this subsection, we compare language and image/video conditioning through the lens of these three functional roles, highlighting the inherent strengths, limitations, and synergistic potential of each modality. 

### _8.5.1 State evaluation: Language-derived objectives_ vs. _video-derived progress signals_ 

In our taxonomy (Section 4), language for state evaluation refers to converting instructions into numerical feedback signals to define goals and quantify task progress. A fundamental challenge here is defining these signals when explicit reward engineering is intractable. Image and videobased approaches excel at providing **implicit and dense** progress signals in such scenarios. By learning state evaluation functions directly from visual demonstrations, these methods can map physical state changes to rewardlike metrics without manual specification. For instance, XIRL (Zakka et al. 2022b) learns a visual representation and a temporal progress measure from videos that transfer across different embodiments. Such visual-derived evaluations are particularly effective when success is defined by perceivable physical changes (e.g., whether a peg is fully inserted or gears are aligned (Chen et al. 2023c)) and when geometric precision is paramount. 

Conversely, language-conditioned state evaluation specifies objectives through **explicit compositional semantics** (e.g., _“place the red mug into the left drawer and close it”_ ). A central advantage of language is its ability to enforce abstract constraints that are difficult to infer solely from a visual goal or demonstration. Specifically, language seamlessly encodes **negative constraints** (e.g., _“stay away from the yellow bottle”_ (Sharma et al. 2022) or _“watch out for the vase”_ (Huang et al. 2023b)) and **safety protocols** (e.g., grounding modifiers like “ _slowly_ ” and “ _upright_ ” into trajectory optimizer parameters (Park et al. 2019)). Furthermore, instructions capture **relational preferences** , such as explicit keypoint constraints (Huang et al. 2025b) or comparative directives like “ _move farther from the stove_ ” (Yang et al. 2025i), by mapping linguistic descriptions into quantitative rewards or costs. While visual evaluation excels at verifying _physical configurations_ , 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

45 

language provides an editable and human-readable interface for defining _behavioral boundaries_ . However, language inherently under-specifies exact geometric details (e.g., precise insertion angles), necessitating visual grounding for fine-grained verification. 

### _8.5.2 Policy conditioning: Language instructions_ vs. _Perceptual grounding_ 

As a condition for policy execution, language instructions serve as high-level behavior specifiers, whereas goal images and videos offer direct **perceptual grounding** . Imageconditioned policies are optimal for tasks where the objective is strictly defined by a target spatial configuration, effectively resolving geometric ambiguity. Video-conditioned imitation extends this capability by implicitly conveying complex spatio-temporal dynamics (Chen et al. 2026), such as approach trajectories, contact timing, and velocity profiles, which are difficult for language to communicate precisely. For instance, BC-Z (Jang et al. 2022) demonstrates transfer to holdout tasks by conditioning on diverse task specifications, including human videos and language, showing that multimodal conditioning can improve generalization within the evaluated task family. 

Language-conditioned policies abstract away these low-level physical details to offer three distinct practical advantages: 

- **Low-bandwidth specification:** Language delivers human intent compactly, eliminating the need to record or render new visual demonstrations for every task variation. 

- **Compositional generalization:** Language supports the systematic recombination of skills, objects, and spatial relations, a critical requirement for scaling to open-world environments (Wang et al. 2024c; Zhou et al. 2024a). 

- **Interactive editability:** Language allows for realtime goal refinement and corrective interaction during execution, allowing human operators to steer the policy through verbal corrections (Liu et al. 2023b), or dialogue-based clarification (Zhang et al. 2022), rather than re-collecting demonstrations or re-specifying visual goals. 

These properties make language the ideal modality for userfriendly interfaces and scalable deployment. Nonetheless, because language frequently under-specifies spatial realities, hybrid conditioning (fusing language embeddings with goal images or visual keyframes) often yields the most robust policies (Jang et al. 2022; Mees et al. 2022a). 

### _8.5.3 Planning: Language-based decomposition_ vs. _Visual imitation_ 

In Section 6, we discussed how language serves as an “internal reasoning medium” for planning, enabling task decomposition (Wei et al. 2022), strategy formulation (Silver et al. 2023), and open-loop planning with LLMs (Wang et al. 2023c; Rana et al. 2023). In contrast, video-conditioned methods utilize visual demonstrations as dense **kinematic and structural priors** . A continuous video implicitly contains the necessary subgoals and physical transitions required for long-horizon tasks. One-shot visual imitation 

methods (Lu et al. 2025b) capitalize on this by extracting multi-stage operational plans directly from demonstrations, bypassing the need for explicit symbolic planners. This is particularly effective for tasks requiring complex physical manipulation that is difficult to articulate linguistically (e.g., folding cloth). 

Language-conditioned planning, however, excels in scenarios that are **branching, constraint-rich, or highly interactive** . While video demonstrations typically show a single successful path, language naturally encodes causal logic and conditional behaviors (e.g., _“if the drawer is stuck, pull harder; otherwise, close it gently”_ ). Furthermore, language acts as a bridge to high-level reasoning modules, allowing systems to decompose tasks logically, propose alternative plans, and query users for clarification (Bartoli et al. 2022). The key distinction lies in the abstraction level: visual demonstrations define the specific _physical path_ , while language organizes the _logical structure_ . To bridge the gap between high-level logic and low-level execution, effective systems often anchor linguistic subgoals to visual keyframes. 

### _8.5.4 Summary_ 

Overall, image and video-conditioned manipulation provide stronger **perceptual grounding** , effectively conveying precise **geometric configurations** and **implicit manipulation skills** . Conversely, language-conditioned manipulation offers unmatched **text semantic expressiveness** for constraints, **compositionality** for open-vocabulary generalization, and **interactive editability** for non-expert human collaboration. 

Rather than viewing these as competing paradigms, the contemporary consensus points toward a unified multimodal task-specification framework: utilize language as the primary interface to dictate _what_ to do (e.g., high-level goals, logical constraints, and user preferences), while using image/video conditioning to specify _how precisely_ to execute it (e.g., spatial geometry, kinematics, and contact-rich dynamics). This distinction motivates the development of hybrid VLA architectures that fuse semantic linguistic instructions with visual demonstrations, enabling robust and adaptable manipulation in unstructured environments (Black et al. 2025a; Li et al. 2026d; Torne et al. 2026). 

# **9 Discussion** 

This section discusses three heat debates in the community: Are large-scale vision-language-action models the most direct path to generalization? Can learned world models provide the necessary foresight for robust planning? And what are the trade-offs between model scaling and the strict real-time constraints of physical control? While these topics are relevant across robotics, they are particularly critical in language-conditioned robot manipulation. Here, language must be grounded in perception to inform physical interaction, creating a tightly coupled system where a failure in one domain may cascade and cause total task failure. Therefore, these advanced techniques bring new capabilities but also introduce challenges that should be addressed to achieve reliable and generalizable robot manipulation. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

46 

# _9.1 Are VLAs the right path forward?_ 

The question of whether VLA models represent the right direction for robotics ultimately depends on whether the scaling principles that have succeeded in language and vision domains can also extend to embodied AI. In pure language modeling, the assumptions of effectively unlimited, homogeneous data and strong structural regularities make scaling laws viable: larger models and more data yield consistent improvements (Achiam et al. 2023; Hurst et al. 2024). However, this assumption becomes questionable when extended to robotic learning, where vision, language, and action must be tightly fused to enable embodied understanding and control. 

On the one hand, current VLA models are still smaller and less data-rich than modern foundation models in computer vision or natural language processing. While today’s LLMs usually contain over 100B parameters and are trained on trillions of tokens, most existing VLAs remain under 7B parameters and rely on only a few million robot trajectories (Kim et al. 2025c; O’Neill et al. 2024). As a result, it is still uncertain whether scaling up model size or dataset volume alone will yield meaningful improvements in robotic manipulation performance. On the other hand, robotic learning is different from pure language or vision tasks because perception, reasoning, and control are all tightly linked to the physical world. Even a small error in the physical world can lead to task failure, whereas minor ambiguities in vision or language tasks rarely have catastrophic consequences. Moreover, robotic data arises from physical interactions that are highly diverse, costly to collect, and difficult to reproduce, thus biases in data cannot be compensated for simply by collecting more samples. 

Consequently, an alternative direction for current VLA approaches is to operate under the paradigm of finite data with strong structural dependencies rather than relying purely on scale (Wagenmaker et al. 2025; Kerr et al. 2025; Parimi and Williams 2025). In this setting, structure should guide scaling, ensuring that model capacity is grounded in physical and causal understanding. Historically, advances in VLA have emerged from the expansion of task complexity rather than from model growth (O’Neill et al. 2024; Yang et al. 2025f). Moving from single-arm to dualarm manipulation (Gbagbe et al. 2024; Li et al. 2026c), from fixed-base to mobile platforms (Wu et al. 2025c), from rigid to deformable object handling (Gao et al. 2026), or from standalone manipulation to human-robot collaboration (Xia et al. 2025), each introduces new structural dimensions and coordination mechanisms. In this sense, genuine scaling in robotics lies in expanding the task manifold, namely the complexity, diversity, and structure of interactions, rather than merely increasing model parameters. Empirical findings show that enlarging model scale alone does not yield consistent generalization improvements, as perception and control remain tightly coupled to embodiment and environment dynamics (Lin et al. 2025). Looking forward, VLA frameworks should evolve beyond pure scaling toward task-driven structural induction, hybrid learning that integrates symbolic reasoning with physical priors, and modular architectures where perception, language, and action modules co-adapt coherently. Whether such 

hybrid and structure-aware scaling can ultimately achieve the robustness and versatility of human-like embodied intelligence remains an open question. 

# _9.2 Are world models the right path forward?_ 

A world model is a learned predictor of environmental dynamics that enables a robot to “imagine” how states will evolve under candidate actions. The Dreamer family, e.g., DreamerV3 (Hafner et al. 2025), shows that such imagination-based learning can yield strong sample efficiency and long-horizon behavior across diverse control domains (from visual game to continuous-control benchmarks) by optimizing policies in latent rollouts. Extending this idea to language, conditioning imagined rollouts on instructions turns free-form text into goal-aware futures that support compositional generalization, recombining known skills to follow new commands (Aljalbout et al. 2025). 

Beyond these, world models contribute to improved safety and generalization in language-conditioned robotics. Because candidate action sequences can be evaluated offline in the model’s “imagination”, the robot gains a capacity for what-if reasoning and safety filtering before execution. The system can proactively reject plans that appear risky or infeasible under the learned dynamics (Wu et al. 2023b; Huang et al. 2024b), thereby avoiding hazardous trials in the real world. This ability to trial plans in simulation provides a measure of safety through imagination that purely reactive policies lack. Moreover, a world model encapsulates shared dynamics priors that aid generalization across tasks and contexts (Ai et al. 2025). Knowledge of physical cause-andeffect learned in one scenario can be carried over to new objects (Xie et al. 2019), tasks, or even robotic embodiments, reducing the amount of task-specific experience needed for each new instruction. 

However, there are notable drawbacks and challenges associated with world-model-based approaches. A primary concern is model bias and distributional brittleness. Because the world model is only an approximate dynamics model, small errors in contact, friction, or object properties can accumulate during imagined rollouts (Hoque et al. 2022). When the system encounters out-of-distribution scenarios, it may propose semantically plausible plans (they satisfy the instruction) yet physically inconsistent (violating kinematics, stability, or contact constraints). In practice, this means a plan that looks sound in simulation can fail when executed on the real robot. For example, due to subtle unmodeled dynamics or unseen environmental factors, such out-of-distribution errors show an inherent fragility: the world model’s predictions are reliable within its training data’s distribution. Ensuring the model’s validity in the real world, especially given the open-ended attribute of language instructions, remains an open problem. Robustness techniques and online adaptation may be required to mitigate these issues, but they add extra complexity to the system (Chen et al. 2025a). Another downside of world models is the computational overhead and the difficulty of grounding imagined rollouts in real perception (Xing et al. 2025a). Training and deploying high-capacity generative 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

47 

models for dynamics prediction can be resource-intensive, straining real-time control loops. 

In summary, rather than definitive drawbacks, current limitations reflect an early methodological stage. Open problems include: (i) injecting structured priors (physics, geometry, task constraints, and commonsense) into the learned dynamics, (ii) quantifying and propagating model uncertainty to mitigate bias and rollout drift, and (iii) meeting real-time control deadlines with compute-efficient models. 

# _9.3 Does scaling help under real-time constraints?_ 

While scaling up models clearly improves representation quality and broadens the range of instructions they can handle, controlling physical robots is constrained by strict real-time deadlines. Each control cycle has a fixed time budget within which sensing, policy inference, and actuation must be completed. If a larger model increases inference time beyond this budget, the control loop can miss its deadline, leading to jitter and degraded stability, especially during contact-rich interactions. Using planner-based LLMs or VLMs for decision-making often adds noticeable latency (on the order of seconds) unless results are aggressively cached. Similarly, fully end-to-end VLA models tend to demand more computation time and memory per step on embedded hardware. Diffusion-based controllers also incur additional “denoising tax” due to iterative sampling, unless faster samplers or model distillation techniques are applied (Lu et al. 2024). Offloading computation to the cloud can provide greater processing capacity, but it introduces unpredictable network delays and potential failure modes that are difficult to bound in safety-critical settings. 

Consequently, simply using a “bigger” model is only helpful if its benefits can be realized within the strict timing deadlines of the control loop. In practice, robotics stacks often mitigate latency by compressing or distilling large neural network backbones and by pruning input tokens or model memory caches to reduce inference time. Many systems also favor multi-view 2D encoders (processing information from multiple camera views) over heavy 3D volumetric perception to keep the feedback loop fast. A split architecture is frequently effective: a lightweight onboard controller handles immediate feedback control and safety interlocks, while more computationally intensive deliberation (e.g., high-level planning or sub-goal generation) runs asynchronously or off-board when possible. We note that latency is not consistently treated as a firstclass evaluation metric in the literature, and often it is mentioned only in footnotes. To assess real-world feasibility, we strongly encourage authors to report latency prominently as a primary performance metric. 

# **10 Limitations and future directions** 

While vision and language models provide a strong foundation for language-conditioned robotic manipulation, several limitations remain for future research, such as _generalization capability_ and _real-world safety_ . 

# _10.1 Generalization capability_ 

The generalization capability of language-conditioned robot manipulation systems remains a central challenge for developing agents that can operate robustly across diverse, real-world scenarios (Mon-Williams et al. 2025). Although current systems exhibit impressive performance within specific training domains (Wu et al. 2023a; Driess et al. 2023; Black et al. 2025b), their performance often degrades when faced with unseen language instructions, novel objects, unfamiliar task compositions, dynamic environments, or new robot embodiments. This challenge reflects the tightly coupled but uneven generalization properties of language, perception, and control: language is compositional and ambiguous, while physical environments are diverse and nonstationary. As a result, the mapping from language to action may overfit to limited data distributions, leading to unexpected behaviors when the robot encounters new situations, object configurations, or embodimentspecific dynamics. More fundamentally, such failures stem from insufficient semantic grounding, data sparsity, weak mechanisms for the continual adaptation of knowledge, and the lack of aligned representations that transfer across tasks, spatial and temporal contexts, and varying robot dynamics. 

To achieve robust generalization in language-conditioned robot manipulation, we argue that future research could focus on the following key aspects: (i) **Data** : Developing large-scale, diverse, and better multimodally aligned robot manipulation datasets across language, perception, and action so as to enhance semantic grounding and coverage. (ii) **Lifelong learning** : Integrating lifelong learning frameworks that enable continual adaptation and knowledge retention across evolving tasks and linguistic contexts. (iii) **Crossembodiment alignment** : Establishing cross-embodiment alignment mechanisms to bridge semantic and control representations across heterogeneous robot morphologies and dynamics. Finally, these three aspects jointly affect the practical effectiveness of zero-shot capability. 

_10.1.1 Language-conditioned datasets and evaluation_ The generalization of language-conditioned robot manipulation heavily depends on the availability of diverse, languageannotated datasets and standardized benchmarks. 

**Data availability** : Training large-scale languageconditioned manipulation models inherently demands extensive datasets (O’Neill et al. 2024; Khazatsky et al. 2024; Jiang et al. 2025b). While VLMs and LLMs benefit from web-scale data, collecting comparable volumes in the domain of robotic manipulation remains infeasible and highly labor-intensive. Some approaches (Lynch et al. 2020; Lynch and Sermanet 2021; Mees et al. 2022a; Zhou et al. 2024a; Wang et al. 2023a) leverage play data instead of expert-labeled data to reduce labeling costs. Unlabeled play data is often readily available in large quantities and can be acquired at a lower cost. It is also possible to gather play data by integrating computer gaming platforms, potentially providing access to data from millions of users. Xiao et al. (2023) utilize VLMs to augment the scenarios or instructions of video demonstration data. Nevertheless, relying solely on 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

48 

play data and generative VLMs may not be sufficient to train a robust FM for robot manipulation. We foresee the need for alternative techniques to gather large-scale demonstration data to enhance robot manipulation capabilities. 

**Beyond web-scale data** : Do we really need vast amounts of data to excel at manipulation and language understanding? While web-scale datasets have fueled progress in FMs, human proficiency in manipulation arises from much smaller, context-rich experiences. Deep learning models are highly data-hungry, requiring massive amounts of information to generalize well. When there is limited data, deep learning models are more likely to overfit to spurious correlation patterns (short-cuts) that exist in the training set but do not generalize to real-world scenarios. This highlights a key limitation: relying solely on data-driven approaches may not be sufficient to solve manipulation and other complex tasks. Neuro-symbolic approaches (Besold et al. 2021), which combine neural networks with symbolic reasoning, offer a promising alternative. These models can enhance data efficiency and reduce the need for massive datasets by integrating predefined human-readable knowledge, such as knowledge graphs or knowledge bases. This suggests that FMs trained on enormous data are not the only path to achieving intelligence. Exploring how to leverage limited data to train models with better generalization capabilities is an important direction. 

**Benchmarking** : Quantifying generalization in real-world settings is challenging, as model performance strongly depends on the underlying hardware specifications and physical constraints of the robotic platform. For this reason, most of the approaches evaluate their results in simulators and lack a unified, standardized real-world evaluation benchmark. However, strong performance in simulation does not necessarily translate to real-world success, as the sim-to-real gap arises from discrepancies in visual appearance, sensor noise, physical dynamics, and the interpretation of linguistic context between virtual and physical environments. To reduce the gap, a promising approach is the _real-to-sim-to-real_ (Torne et al. 2024), where real-world interaction data are used to calibrate simulators that closely replicate physical environments. Policies trained in these aligned simulations are then redeployed in the real world, forming a feedback loop that enhances transfer robustness and consistency across domains. In parallel, establishing a standardized, language-conditioned real-world benchmark is essential for fair and reproducible evaluation. Such a benchmark should integrate natural-language instructions, multimodal observations, and diverse robot embodiments to assess both task success, semantic understanding, and real-time performance, ultimately advancing grounded languageconditioned manipulation. 

### _10.1.2 Lifelong learning_ 

Lifelong learning represents a transformative direction for adaptive, continuously improving robotic agents. Unlike recent episodic learning, which assumes fixed datasets and tasks, lifelong learning allows agents to incrementally acquire new skills while avoiding catastrophic forgetting 

of prior ones. In language-conditioned contexts, this means not only adapting to new tasks but also maintaining semantic consistency across evolving linguistic instructions. Integrating replay buffers (Chaudhry et al. 2019), modular architectures (Mallya and Lazebnik 2018), and progressive neural expansion strategies (Kirkpatrick et al. 2017) enables robots to preserve earlier knowledge while incorporating new behaviors, leading to more scalable, context-aware generalization. Future work should explore how lifelong learning can interface with FMs and policy distillation in language-conditioned robotic manipulation, forming persistent, adaptive intelligence capable of reasoning over both new language goals and prior embodied experiences. 

### _10.1.3 Cross-embodiment alignment_ 

Language is inherently embodiment-agnostic (Wang et al. 2024b), as the same instruction, such as “ _pick up the block_ ”, can be given to robots with very different kinematic structures and sensing configurations. However, robots differ significantly in perception systems, actuation mechanisms, and control dynamics. As a result, policies trained on one robot platform (e.g., Franka Panda) may fail when transferred to another robot (e.g., KUKA iiwa) even when the same language instruction is provided. 

From the perspective of the taxonomy introduced in Section 3, the embodiment gap affects multiple stages of language-conditioned manipulation systems. First, **at the perception level** , language instructions must be grounded in observations collected by different sensor configurations. Robots may rely on different camera placements, sensing modalities, or workspace geometries, which can lead to inconsistent visual grounding of the same language command (Khazatsky et al. 2024). Consequently, perception modules must learn representations that can align semantic language descriptions with heterogeneous sensory inputs. 

Second, **at the control level** , policies conditioned on language instructions must adapt to different kinematic structures and action spaces. A manipulation policy learned on one robot often implicitly encodes embodimentspecific dynamics. When transferred to another robot with different degrees of freedom, joint limits, or end-effector configurations, the learned policy may no longer produce valid actions (Black et al. 2025b). Cross-embodiment alignment, therefore, requires mechanisms that map shared semantic goals to embodiment-specific control strategies. Third, **at the planning and reasoning level** , robots must maintain consistent semantic interpretation of language instructions while executing tasks using different embodiments. High-level reasoning modules may generate task plans such as object rearrangement or multi-step manipulation sequences (Kim et al. 2025c). Ensuring that such plans remain executable across robots with different capabilities requires bridging the gap between abstract language reasoning and embodiment-specific constraints. 

To address these challenges, cross-embodiment learning aims to align shared semantic representations across heterogeneous robot morphologies. Recent work, such as HPT (Wang et al. 2024b) and embodiment-aware dynamics modeling (Schaldenbrand et al. 2023, 2024) 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

49 

demonstrates that learning shared latent spaces across robots can significantly reduce the adaptation effort required when transferring policies to new embodiments. Developing such unified representations will be essential for enabling language-conditioned manipulation systems to generalize across diverse robotic platforms and environments. 

rather than universal: strongest for semantic specification and high-level planning, promising but still fragile for policy transfer, and still limited for reliable real-world manipulation under substantial novelty. 

# _10.2 Real-world safety_ 

### _10.1.4 Effectiveness of zero-shot capability_ 

In language-conditioned robot manipulation, zero-shot capability is not a uniform property but depends on what is being generalized. Current methods show the strongest zero-shot behavior at the semantic and planning levels, where pre-trained language or vision-language models can interpret unseen instructions, retrieve relevant skills, propose subgoals, or construct reward/cost signals without taskspecific retraining. For example, ZSRM (Mahmoudieh et al. 2022) derives rewards by matching goal text with images through CLIP, thereby enabling zero-shot instruction-toreward transfer, although its performance is fundamentally limited by CLIP’s weak spatial reasoning (Radford et al. 2021). At the planning level, SayCan (Brohan et al. 2023b) translates natural-language commands into semantically relevant and physically feasible skill sequences by combining LLM reasoning with affordance scores, while Code as Policies (Liang et al. 2023) can flexibly recompose API calls for previously unseen objects. However, such zero-shot planning remains fragile, since SayCan assumes faultless skill execution and Code-as-Policies may generate infeasible steps or even call nonexistent functions. 

At the policy level, zero-shot generalization is more limited and usually depends on recombining previously learned skills or leveraging broad pre-trained representations. For instance, Lancon-learn (Silva et al. 2021) uses language to reweight reusable skill modules and can recombine them for zero-shot task generalization, but the joint learning of routing and control is fragile and sample-hungry. Similarly, RT-2 (Zitkovich et al. 2023) fine-tunes pretrained vision-language representations for robot control and achieves better zero-shot performance on novel objects and instructions than scratch-trained policies. Nevertheless, these gains remain strongly tied to the coverage of the pre-training distribution and the availability of embodied robot data. 

As the problem moves closer to physical execution, zeroshot capability weakens further. Robust zero-shot execution remains difficult for long-horizon, contact-rich, dynamic, or cross-embodiment tasks, where errors in grounding, perception, dynamics, and feedback accumulation become dominant. Open-loop planners such as SayCan (Brohan et al. 2023b) often struggle in new environments because they lack embodied feedback, whereas closed-loop systems such as SayPlan (Rana et al. 2023) improve robustness through replanning and textual scene feedback, but their performance is still limited by the reasoning ability and latency of the underlying LLM. More fundamentally, as discussed in our section on cross-embodiment alignment, even the same instruction can fail to transfer across robots with different sensors, kinematics, and control dynamics. Therefore, the practical effectiveness of zero-shot capability in current systems should be understood as _partial and conditional_ 

Ensuring real-world safety in language-conditioned robot manipulation is critical, especially as robots increasingly interact with humans in dynamic and unstructured environments. We summarize three major concerns, namely ambiguity in language (Sec. 10.2.1), failure recovery (Sec. 10.2.2), and real-time performance (Sec. 10.2.3). 

### _10.2.1 Ambiguity in language_ 

One of the main safety concerns arises from language grounding and language use. Natural language instructions alone can be ambiguous. They are often underspecified and depend on rich context for a correct interpretation (Clark 1996). For instance, given the instruction “ _Remove the chemicals from the table._ ”, the user may intend for the robot to carefully relocate the containers of chemicals from the table to a designated storage area, ensuring safety by avoiding spills or accidents. However, this instruction might be interpreted as physically removing chemicals by tipping over or mishandling the containers, resulting in a hazardous situation with chemical spills and potential harm. To mitigate this risk, robots need to understand the intent of human users and interpret the instructions based on shared experience and context. This often requires robots to take extra effort to proactively engage in clarification dialogue with humans to establish a common ground (Chai et al. 2014). For instance, if instructed to “ _Remove the chemicals from the table_ ”, the robot could respond with “ _Do you want me to move the chemicals to storage, or should I dispose of them_ ?” Furthermore, implementing feedback loops to confirm its interpretation before acting is essential. For example, the robot might state, “ _I understood that I should carefully move the containers to the storage area. Is this correct?_ ” This ensures clarity and prevents potential errors. 

Despite recent progress, language grounding to 3D world still faces significant challenges (Hong et al. 2023; Huang et al. 2024a). Vision-language models are prone to hallucination (Zhou et al. 2024c; Chen et al. 2024c) and incapable of taking spatial perspectives when interpreting spatial expressions (Zhang et al. 2025c). Future work will need to find ways to improve language grounding, for example, through an agentic architecture that orchestrates various reasoning and perception modules (Yang et al. 2024a), or through large-scale data synthesis (Yang et al. 2025b) for training better 3D-LLMs or VLMs. 

### _10.2.2 Recovering from failures_ 

Safety issues also emerge when robots fail during task execution due to software and hardware limitations. On the software side, LLM hallucinations can lead to serious task failures, such as referencing nonexistent objects, producing logically inconsistent plans, or generating unsafe control code Rana et al. (2023); Liang et al. (2023); Mu et al. (2023). On the hardware side, edge-device inference limitations can 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

50 

delay actions (Brohan et al. 2023a); motor overheating may trigger shutdowns in high-dynamic motions; depth sensors are prone to interference from lighting or reflective surfaces; and limited battery capacity restricts operating time in the wild. To address these challenges, future research should focus on two complementary directions: (1) At the software level, establishing closed-loop feedback mechanisms such as self-verification for LLM outputs and human-in-the-loop supervision (Dai et al. 2025; Bucker et al. 2024; Liu et al. 2023b; Shi et al. 2024; Meng et al. 2025b) to detect and correct reasoning or planning errors in real time; and (2) At the hardware level, advancing computational efficiency, thermal management, and sensor fusion to improve stability and reliability during continuous real-world operation. 

# **11 Conclusion** 

In summary, this survey presents an overview of the current language-conditioned robot manipulation approaches. Our analysis focuses on the primary ways language is integrated into the robotic systems, namely _language for state evaluation_ , _language as a policy condition_ , _language for cognitive planning and reasoning_ , and _language in unified vision-language-action models_ . Furthermore, our comparative analysis offers a multifaceted perspective along five axes: _action granularity_ , _data and supervision regimes_ , _system cost and latency_ , _environment and evaluation_ and _task representations_ . We also examine the central debates in language-conditioned robot manipulation concerning VLAs, world models, and scaling. Finally, we articulate the key challenges and delineate future directions, with particular emphasis on _generalization capability_ and _real-world safety_ . 

### _10.2.3 Real-time performance_ 

Real-time responsiveness is another essential aspect of safe manipulation. Large-scale models such as LLMs, VLMs, and VLAs often incur long inference times, which extend the control loop latency and hinder a robot’s ability to adapt to fast-changing environments. Model compression methods, including pruning, quantization (Liang et al. 2021), and knowledge distillation (Gou et al. 2021), can accelerate inference while preserving accuracy. Hybrid frameworks that delegate time-critical decisions to lightweight local models while offloading complex reasoning to larger models can balance responsiveness and intelligence. 

Beyond on-device optimization, cloud-based inference offers a scalable path forward, where computationally intensive reasoning is performed remotely and distributed to multiple robots (Brohan et al. 2023a; Zitkovich et al. 2023; Belkhale et al. 2024). However, this introduces new latency and safety challenges. For instance, in industrial settings, hundreds of robots may simultaneously query a shared cloud model, placing enormous pressure on network infrastructure. Each agent typically requires control updates at frequencies exceeding 50 Hz (Belkhale et al. 2024), demanding not only high inference throughput on the cloud side but also ultra-fast data transmission and bus communication speeds to ensure timely feedback. Even minor network delays or bandwidth bottlenecks can propagate through the control loop, resulting in unsafe behavior or degraded task performance. Moreover, communication security risks present another critical safety concern in cloud-connected language-conditioned robotic systems. Risks include hijacking or maliciously tampering with user commands, altering the model’s output action patterns, or even infiltrating and corrupting the internal weights of large-scale models. Such attacks could lead to unsafe or unpredictable robot behaviors, jeopardizing both human safety and system integrity. Therefore, ensuring secure, encrypted communication protocols, robust authentication mechanisms, and integrity verification of transmitted data and model parameters is essential. These measures not only protect robots from external interference but also help maintain the reliability, traceability, and realtime performance required for safe deployment of languageconditioned policy in unstructured environments. 

# **12 Acknowledgement** 

The authors thank the International Max Planck Research School for Intelligent Systems (IMPRS-IS) for supporting Hongkuan Zhou. The authors also thank Yufei Duan for helpful insights with the design of Figure 2. 

# **Appendix** 

# _A. Tabular comparison of vision-language-action models_ 

Table 10 provides a comprehensive comparison and classification of various Vision-Language-Action (VLA) models discussed in Section 7. The table organizes these models based on their primary _Optimization Direction_ , which includes improvements in Group I for Perception (Data Source and Augmentation, Spatial Understanding, Multimodal Fusion), Group II for Reasoning (Long-horizon Task Solving, Knowledge Preservation, Reasoning with World Models), Group III for Action Generation, and Group IV for Learning & Adaptation. For each model, the table details several key design dimensions: 

- **Observation** : The input modalities used by the model, such as RGB images (RGB), depth information (D), including point clouds or other types, robot proprioception (ROB), and text instructions (TX). 

- **Action generation** : The methodology for producing actions, categorized into Flow Matching (FM), Diffusion Models (DM), Autoregressive (AR) decoding, or Direct Prediction (DP). 

- **VLM policy** : The internal mechanisms of the policy, highlighting the use of advanced reasoning like Chainof-Thought (CoT), Future Prediction (FP), or explicit Memory (MEM). 

- **Pretraining** : The type of the training data, specifying whether it involves Multiple Datasets (MD) or Crossembodiment (CE) data. 

- **Scenarios** : The evaluation context, indicating if the model was tested across Multi-scenario (MS) setups, deployed in the Real World (RW), or demonstrated Cross-embodiment Execution (CE). 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

51 

**Table 10.** Classification of VLA models and design dimensions in Section 7. 

|Optimization|Article|Time|Observation|Action|V|LM po|licy|Pretr|aining|S|cenario|s|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Direction||||Generation|CoT|FP|MEM|MD|CE|MS|RW|CE|
|I: Data Source &|EgoVLA (Yang et al.)|2025-07|RGB, ROB, TX|DP|✗|✗|✓|✓|✓|✓|✗|✓|
|Augmentation|H-RDT (Bi et al.)|2025-08|RGB, ROB, TX|FM|✗|✗|✗|✓|✓|✓|✓|✓|
||Shortcut (Xing et al.)|2025-08|RGB, TX|-|✗|✗|✗|✓|✓|✓|✓|✗|
|I: Spatial|SpatialVLA (Qu et al.)|2025-01|RGB, ROB, TX|AR|✗|✗|✗|✓|✓|✓|✓|✓|
|Understanding|PointVLA (Li et al.)|2025-05|RGBD, ROB, TX|DM|✗|✗|✗|✓|✓|✓|✓|✓|
||BridgeVLA (Li et al.)|2025-06|RGB, ROB, TX|DP|✗|✗|✗|✗|✗|✓|✓|✗|
||GeoVLA (Sun et al.)|2025-08|RGBD, ROB, TX|DM|✗|✗|✗|✗|✗|✓|✓|✗|
|I: Multimodal|VTLA (Zhang et al.)|2025-05|RGB, TX|AR|✗|✗|✓|✗|✗|✗|✓|✗|
|Sensing &|Tactile-VLA (Huang et al.)|2025-07|RGB, ROB, TX|FM|✓|✗|✗|✗|✗|✓|✗|✗|
|<br>Fusion|<br>OmniVTLA (Cheng et al.)|2025-08|RGB, ROB, TX|FM|✗|✗|✓|✗|✗|✗|✓|✗|
||ForceVLA (Yu et al.)|2025-09|RGBD, ROB, TX|FM|✓|✗|✗|✗|✗|✓|✓|✗|
||FuSe VLA (Jones et al.)|2025-01|RGBD, ROB, TX|AR|✗|✗|✗|✗|✗|✓|✓|✗|
|II: Long-horizon|LoHoVLA (Yang et al.)|2025-05|RGB, ROB, TX|AR|✓|✗|✗|✗|✗|✓|✗|✗|
|task solving|Long-VLA (Fan et al.)|2025-08|RGB, TX|DM|✗|✗|✗|✓|✗|✓|✓|✗|
||DexVLA (Wen et al.)|2025-08|RGB, ROB, TX|DM|✓|✗|✗|✓|✓|✓|✓|✓|
||MemoryVLA (Shi et al.)|2025-08|RGB, TX|DM|✓|✗|✓|✓|✓|✓|✓|✓|
|II: Knowledge|DiffusionVLA (Wen et al.)|2024-12|RGBD, TX|DM + AR|✓|✗|✗|✓|✗|✓|✓|✓|
|Preserving|ChatVLA (Zhou et al.)|2025-02|RGB, TX|DM|✗|✗|✗|✓|✗|✓|✓|✗|
||ChatVLA-2 (Zhou et al.)|2025-05|RGB, TX|DM|✓|✗|✗|✓|✗|✓|✓|✗|
||Insulating (Driess et al.)|2025-05|RGB, ROB, TX|FM + AR|✗|✗|✗|✓|✓|✓|✓|✓|
||<br>InstructVLA (Yang et al.)|2025-07|RGB, ROB, TX|FM|✓|✗|✓|✓|✗|✓|✓|✓|
||GR-3 (Cheang et al.)|2025-07|RGB, ROB, TX|FM|✗|✗|✓|✓|✗|✓|✓|✗|
|II: Reasoning &|Seer (Tian et al.)|2024-12|RGB, ROB, TX|DP|✗|✓|✗|✓|✓|✓|✓|✓|
|World Models|CoT-VLA (Zhao et al.)|2025-05|RGB, ROB, TX|AR|✓|✓|✗|✓|✓|✓|✓|✓|
||WorldVLA (Cen et al.)|2025-06|RGB, ROB, TX|AR|✗|✓|✗|✗|✗|✗|✗|✗|
||DreamVLA (Zhang et al.)|2025-08|RGB, ROB, TX|DM|✗|✓|✗|✗|✗|✓|✓|✗|
||ECoT VLA (Zawalski et al.)|2024-07|RGB, TX|AR|✓|✓|✗|✓|✗|✓|✓|✗|
|III: Policy|PI-0 (Black et al.)|2024-10|RGB, ROB, TX|FM|✗|✗|✗|✓|✓|✓|✓|✓|
|Execution|PI-Fast (Pertsch et al.)|2025-01|RGB, ROB, TX|FM|✗|✗|✗|✓|✓|✓|✓|✓|
||PI-0.5 (Black et al.)|2025-04|RGB, ROB, TX|FM|✓|✗|✗|✓|✓|✓|✓|✓|
||DisDiffVLA (Liang et al.)|2025-08|RGB, ROB, TX|DM|✗|✗|✗|✓|✓|✓|✗|✓|
|IV: Adaptation &|OpenVLA-OFT (Kim et al.)|2025-02|RGB, ROB, TX|DP|✗|✗|✗|✓|✓|✓|✓|✓|
|Fine-Tuning|ConRFT (Chen et al.)|2025-04|RGB, ROB, TX|DM|✗|✗|✗|✗|✗|✗|✓|✗|
||RIPT-VLA (Tan et al.)|2025-05|RGB, ROB, TX|AR|✗|✗|✗|✗|✓|✓|✗|✗|
||ControlVLA (Li et al.)|2025-06|RGB, ROB, TX|DM|✗|✗|✗|✗|✗|✗|✓|✗|


Observation: RGB images, D: depth information (e.g., point clouds), ROB: Robot Proprioception, TX: text (e.g., prompt, language goal). Action generation: (FM) Flow Matching, (DM) Diffusion Model, (AR) Autoregressive, (DP) Direct Prediction, (-) Not Applicable; (CoT) Chain-of-Thought, (FP) Future Prediction, (MEM) Memory Mechanisms, (MD) Multiple Datasets, (CE) Cross-embodiment Data, (MS) Multi-scenario, (RW) Real-world Deployment, (CE) Cross-embodiment Execution. 

This classification highlights the key features, capabilities, and architectural choices of recent VLA models, offering a structured overview of the current research landscape. 

# _B. Tabular comparison of language-conditioned robotic manipulations_ 

Table 11 and Table 12 present a tabular comparison of various language-conditioned robot manipulation approaches discussed in Sections 4 - 8. The tables summarize key aspects such as the year of publication, benchmarks or simulation engines used, language and perception modules, real-world experiment status, and the utilization of foundational models (FMs), reinforcement learning (RL), imitation learning (IL), and motion planning (MP). 

### **References** 

- Abbeel P and Ng AY (2004) Apprenticeship learning via inverse reinforcement learning. In: _Proceedings of the twenty-first international conference on Machine learning_ . p. 1. 

- Abdolmaleki A, Abeyruwan S, Ainslie J, Alayrac JB, Arenas MG, Balakrishna A, Batchelor N, Bewley A, Bingham J, Bloesch M et al. (2025) Gemini robotics 1.5: Pushing the frontier of generalist robots with advanced embodied reasoning, thinking, and motion transfer. _arXiv preprint arXiv:2510.03342_ . 

- Abolghasemi P, Mazaheri A, Shah M and Boloni L (2019) Pay attention!-robustifying a deep visuomotor policy through taskfocused visual attention. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 4254–4262. 

- Achiam J, Adler S, Agarwal S, Ahmad L, Akkaya I, Aleman FL, Almeida D, Altenschmidt J, Altman S, Anadkat S et al. (2023) Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ . 

- Adams S, Cody T and Beling PA (2022) A survey of inverse reinforcement learning. _Artificial Intelligence Review_ 55(6): 4307–4346. 

- Adeniji A, Xie A, Sferrazza C, Seo Y, James S and Abbeel P (2024) Language reward modulation for pretraining reinforcement learning. In: _Workshop on Training Agents with Foundation Models at RLC 2024_ . 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

52 

**Table 11.** Comparison of language-conditioned robot manipulation approaches I in Section 8. 

|Models|Years|Benchmark|Simulation Engine|Language<br>Module|Perception<br>Module|Real world<br>experiments|FM|s<br>R|L<br>IL|MP|
|---|---|---|---|---|---|---|---|---|---|---|
|IPRO (Hatori et al.)|2018|#|-|LSTM|CNN|✓|✗|✗|✗|✓|
|MaestROB (Munawar et al.)<br>exePlan (Liu and Zhang)<br>|2018<br>2018<br>|#<br>#<br>|-<br>-|IBM Watson<br>coreNLP<br>|Artoolkit<br>*<br>|✓<br>✓<br>|✗<br>✗<br>|✗<br>✗<br>|✗<br><br>✗<br><br>|✓<br>✓<br>|
|TLC (Wang et al.)<br>IMNLU (Wang et al.)|2018<br>2018|#<br>#|-<br>-|CCG<br>WordNet, FrameNet|*<br>Stereo Vision|✓<br>✓|✗<br>✗|✗|✓<br><br>✗|✗<br>✓|
|Cut&recombine (Tamosiunaite et al.<br>DREAMCELL (Paxton et al.)|)<br>2019<br>2019|#<br>#|-<br>-|Parser<br>LSTM|*<br>*|✓<br>✗|✗<br>✗|✗<br>✗|✗<br><br>✓|✓<br>✗|
|<br>ICR (Patki et al.)<br>GroundedDA (Thomason et al.)|2019<br>2019|#<br>#|-<br>-|Parser, DCG<br>CCG|YOLO9000<br>RANSAC|✓<br>✓|✗<br>✗|✗<br>✗|✗<br><br>✗|✓<br>✓|
|MEC (Arkin et al.)<br>|2020<br>|#<br>|-|Parser, ADCG<br>|Mask RCNN<br>|✓<br>|✗<br>|✗<br>|✗<br><br>|✓<br>|
|LMCR (Chen et al.)<br>|2020<br>|#<br>|-<br>|RNN<br>|Mask RCNN<br>|✓<br>|✗<br>||✗<br><br>|✓<br>|
|PixL2R (Goyal et al.)<br>Concept2Robot (Shao et al.)|2020<br>2020|Meta-World<br>#|MuJoCo<br>PyBullet|LSTM<br>BERT|CNN<br>ResNet-18|✗<br>✗|✗<br>✗||✗<br><br>✓|✗<br>✗|
|<br>LanguagePolicy(Stepputtis et al.)|2020|#|CoppeliaSim|GLoVe|Faster RCNN|✗|✗|✗|✓|✗|
|LOReL (Nair et al.)<br> hi  l|2021<br>221|Meta-World<br>l|MuJoCo<br>|distillBERT<br>|CNN<br>*|✓<br>|✗<br>✓|✓<br>|✗<br><br>|✗<br>|
|CARE (Sodan et a.)<br>MCIL (Lynch and Sermanet)|0<br>2021|Meta-Word<br>#|MuJoCo<br>MuJoCo|RoBERTa<br>MUSE|CNN|✗<br>✗|✗|✗|✗<br><br>✓|✗<br>✗|
|BC-Z (Jang et al.)|2021|#|-|MUSE|ResNet18|✓|✗|✗|✓|✗|
|CLIPort (Shridhar et al.)|2021|#|PyBullet|CLIP|CLIP|✓|✗|✗|✓|✗|
|LanCon-Learn (Silva et al.)|2022|Meta-World|MuJoCo|GLoVe|*|✗|✗|✓|✓|✗|
|MILLION (Bing et al.)<br>PLMSCBh  l|2022<br>2022|Meta-World<br>#|MuJoCo|GLoVe<br>PLM|*<br>ViLD|✓<br>✓|✗<br>✓|✓<br>|✗<br><br>✓|✗<br>|
|a-ayan (roan et a.)<br>|||-<br>|a<br>||||||✗<br>|
|ATLA (Ren et al.)|2022|#|PyBullet|BERT-Tiny|CNN|✗|✓||✗|✗|
|HULC (Mees et al.)|2022|CALVIN|PyBullet|MiniLM-L3-v2|CNN|✗|✗|✗|✓|✗|
|<br>PerAct (Shridhar et al)|2022|RLbench|CoppelaSim|CLIP|ViT|✓|✗||✓|✗|
|.<br>RT-1 (Brohan et al.)<br>|2022<br>|#<br>|-<br>|USE<br>|EfficientNet-B3<br>|✓<br>|✓<br>|✗<br>|✓<br><br>|✗<br>|
|LATTE (Bucker et al.)<br>DIAL (Xiao et al.)|2023<br>2022|#<br>#|CoppeliaSim<br>-|distillBERT, CLIP<br>CLIP|CLIP<br>CLIP|✓<br>✓|✗<br>✓|✗<br>✗|✗<br><br>✓|✓<br>✗|
|<br>R3M (Nair et al)|2022|#|-|distillBERT|ResNet183450|✓|✗||✓|✗|
|.<br>Inner Monologue (Huang et al.)|2022|#|-|CLIP|,,<br>CLIP|✓|✓|✗|✗|✓|
|NLMap (Chen et al.)<br>|2023<br>|#<br>|-|CLIP<br>|ViLD<br>|✓<br>|✓<br>|✗<br>|✓<br><br>|✗<br>|
|Code as Policies (Liang et al.)<br>Progprompt (Singh et al.)|2023<br>2023|#<br>Virtualhome|-<br>Unity3D|GPT3, Codex<br>GPT-3|ViLD<br>*|✓<br>✓|✓<br>✓|✗|✗<br><br>✗|✓<br>✓|
|Language2Reward (Yu et al.)|2023|#|MuJoCo MPC|GPT-4|*|✓|✓|✓|✗|✗|
|<br>LfS (Y t l)|2023|MtWrld|MJC|Cn Prr|*|✓|✗||✗|✗|
|ao e a.<br>HULC++ (Mees et al.)|2023|ea-o<br>CALVIN|uoo<br>PyBullet|os. ase<br>MiniLM-L3-v2|CNN|✓|✗|✗|✓|✗|
|ALOHA (Zhao et al.)<br>LEMMA (Gong et al.)|2023<br>2023|#<br>LEMMA|-<br>NVIDIA Omniverse|Transformer<br>CLIP|CNN<br>CLIP|✓<br>✗|✗<br>✗|✗<br>|✓<br><br>✓|✗<br>✗|
|<br>SPIL (Zhou et al.)<br>|2023<br>|CALVIN<br>|<br>PyBullet<br>|MiniLM-L3-v2<br>|CNN<br>|✓<br>|✗<br>|✗<br>|✓<br><br>|✗<br>|
|PaLM-E (Driess et al.)<br>LAMP (Adeniji et al.)<br>MOO (Stone et al)|2023<br>2023<br>2023|#<br>RLbench<br>#|PyBullet<br>CoppelaSim<br>-|PaLM<br>ChatGPT<br>OWL-ViT|ViT<br>R3M<br>OWL-ViT|✓<br>✗<br>✓|✓<br>✓<br>✗|✓<br>|✓<br><br>✗<br><br>✓|✗<br>✗<br>✗|
|.<br>Instruction2Act (Huang et al.)<br>|2023<br>|VIMAbench<br>|PyBullet<br>|ChatGPT<br>|CLIP<br>|✗<br>|✓<br>|✗<br>|✗<br><br>|✓<br>|
|VoxPoser (Huang et al.)|2023|#|SAPIEN|GPT-4|OWL-ViT|✓|✓||✗|✓|
|SuccessVQA (Du et al.)|2023|#|IA Playroom|Flamingo|Flamingo|✓|✓|✗|✓|✗|
|<br>VIMA (Jiang et al.)<br>|2023<br>|VIMAbench<br>|<br>PyBullet|T5<br>|ViT<br>|✓<br>|✓<br>|✗<br>|✓<br><br>|✗<br>|
|TidyBot (Wu et al.)<br>|2023<br>|#<br>|-|GPT-3<br>|CLIP<br>|✓<br>|✓<br>||✗<br><br>|✓<br>|
|Text2Motion (Lin et al.)<br>LLM-GROP (Ding et al.)|2023<br>2023|#<br>#|-<br>Gazebo|GPT-3, Codex<br>GPT-3|*<br>*|✓<br>✓|✓<br>✓|✗|✗<br><br>✗|✗<br>✓|
|<br>Scaling Up (Ha et al)|2023|#|MuJoCo|CLIP GPT-3|ResNet-18|✓|✓||✓|✗|
|.<br>Socratic Models (Zeng et al.)<br>SayPlan (Rana et al.)|2023<br>2023|#<br>#|-<br>-|,<br>RoBERTa, GPT-3<br>GPT-4|CLIP<br>*|✓<br>✓|✓<br>✓|✗<br>✗|✗<br><br>✗|✓<br>✓|
|RT-2 (Zitkovich et al.)<br>KNOWNO (R t l)|2023<br>2023|#<br>#|-<br>PBllt|PaLI-X, PaLM-E<br>PLM2L|PaLI-X, PaLM-E<br>*|✓<br>✓|✓<br>✓|✗<br>|✓<br><br>✗|✗<br>✓|
|en e a.<br>MDT(Reuss et al.)<br>|2023|CALVIN|yue<br>PyBullet|a-<br>CLIP|CLIP<br>i|✗<br>|✗<br>|✗|✓<br>|✗|
|RT-Trajectory (Gu et al.)<br>SuSIE(Black et al.)|2023<br>2023|#<br>CALVIN|-<br>PyBullet|PaLM-E<br>InstructPix2Pix(GPT3)|EfficientNet-B3<br>InstructPix2Pix|✓<br>✓|✓<br>✓|✗<br>✗|✓<br><br>✓|✗<br>✗|
|Playfusion(Chen et al.)<br>|2023<br>|CALVIN<br>|PyBullet<br>|Sentence-bert<br>|ResNet-18<br>|✓<br>|✗<br>|✗<br>|✓<br><br>|✗<br>|
|ChainedDiffuser(Xian et al.)<br>GNFactor(Ze et al.)|2023<br>2023|RLbench<br>RLbench|CoppelaSim<br>CoppelaSim|CLIP<br>CLIP|CLIP<br>NeRF|✓<br>✓|✗<br>✗|✗|✓<br><br>✓|✗<br>✗|
|StructDiffusion(Liu et al.)|2023|#|PyBullet|Sentence-bert|PCT|✓|✗|✗|✗|✓|
|PoCo(Wang et al.)<br>DNAct(Yan et al)|2024<br>2024|Fleet-Tools<br>RLbench|Drake<br>CoppelaSim|T5<br>CLIP|ResNet-18<br>NeRF PointNext|✓<br>✓|✗<br>✗|✗<br>|✓<br><br>✓|✗<br>✗|
|.<br>3D Diff AK  l|2024|CALVIN|PBll|CLIP|,<br>CLIP|✓|||✓||
|user ctor(e et a.)<br>|||yuet<br>||||✗<br>|||✗<br>|
|RoboFlamingo (Li et al.)<br>OpenVLA (Kim et al.)|2024<br>2024|CALVIN<br>Open X-Embodiment|Pybullet<br>-|OpenFlamingo<br>Llama 2 7B|OpenFlamingo<br>DINOv2 & SigLIP|✗<br>✓|✓<br>✓|✗|✓<br><br>✓|✗<br>✗|
|<br>RT-X (O’Neill et al.)<br>|2024<br>|<br>Open X-Embodiment<br>|-|PaLI-X,PaLM-E<br>|<br>PaLI-X,PaLM-E<br>|✓<br>|✓<br>|✗<br>|✓<br><br>|✗<br>|
|PIVOT (Nasiriany et al.)<br>|2024<br>|Open X-Embodiment<br>|-|GPT-4, Gemini<br>|GPT-4, Gemini<br>|✓<br>|✓<br>||✗<br><br>|✓<br>|
|RT-Hierarchy (Belkhale et al.)<br>3D-VLA (Zhen et al.)|2024<br>2024|#<br>RL-Bench & CALVIN|-<br>CoppeliaSim & PyBullet|PaLI-X<br>3D-LLM|PaLI-X<br>3D-LLM|✓<br>✗|✓<br>✓|✗|✓<br><br>✓|✗<br>✗|
|<br>Octo (Octo Model Team et al.)<br>ECoT (Zawalski et al.)<br>|2024<br>2024<br>|Open X-Embodiment<br>BridgeData V2<br>|<br>-<br>-<br>|T5<br>Llama 2 7B<br>|CNN<br>DinoV2 & SigLIP<br>|✓<br>✓<br>|✓<br>✓<br>|✗<br>✗<br>|✓<br><br>✓<br><br>|✗<br>✗<br>|
|LEGION(Meng et al.)<br>RACER (Dai et al.)|2024<br>2024|Meta-World<br>RLbench|MuJoCo<br>CoppelaSim|RoBERTa<br>Llama3-llava-next-8B|*<br>LLaVA|✓<br>✓|✗<br>✓|✗|✗<br><br>✓|✗<br>✗|


# Their own benchmark; * Directly get environment states; FMs: use foundational models or not; RL: reinforcement learning; IL: imitation learning; MP: motion planning. 

- Agia C, Migimatsu T, Wu J and Bohg J (2023) Stap: Sequencing task-agnostic policies. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 7951–7958. 

- Agia C, Sinha R, Yang J, Cao Z, Antonova R, Pavone M and Bohg J (2025) Unpacking failure modes of generative policies: 

Runtime monitoring of consistency and progress. In: _2025 Conference on Robot Learning_ . PMLR, pp. 689–723. 

Ai B, Tian S, Shi H, Wang Y, Pfaff T, Tan C, Christensen HI, Su H, Wu J and Li Y (2025) A review of learning-based dynamics models for robotic manipulation. _Science Robotics_ 10(106): 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

53 

**Table 12.** Comparison of language-conditioned robot manipulation approaches II in Section 8. 

|Models|Years|Benchmark or<br>_Simulation Engine_|Language<br>Module|Perception<br>Module|Real world<br>experiments|FMs|RL|IL<br>MP|
|---|---|---|---|---|---|---|---|---|
|Ground4Act (Yang et al.)|2024|Gazebo|Transformer|ResNet101, BERT|✓|✗|✓|✗<br>✗|
|LOVM (Ye et al.)|2024|#|BiGRU|LOVM|✗|✗|✓|✗<br>✓|
|ECLAIR (Tarakli et al.)|2024|#|GPT-3-turbo|*|✓|✓|✓|✗<br>✗|
|PR2L (Chen et al.)|2024|MineDojo, HM3D|InstructBLIP|InstructBLIP|✓|✓|✓|✗<br>✗|
|AHA (Duan et al.)|2024|RLBench, ManiSkill, RoboFail|LLaMA-2-13B|CLIP|✗|✓|✓|✗<br>✓|
|KOI (Lu et al.)|2024|Meta-World, LIBERO|GPT-4v|KOI|✓|✓|✗|✓<br>✓|
|GPT-4V(ISION) (Wake et al.)|2024|#|GPT-4|GPT-4|✓|✓|✗|✓<br>✗|
|<br>HiRT (Zhang et al.)|2024|Meta-World, Franka-Kitchen|InstructBLIP|CNN|✓|✓|✗|✓<br>✗|
|Sentinel (Agia et al.)|2024|#|GPT-4o|PointNet++|✓|✓|✗|✗<br>✓|
|<br>RoLD (Tan et al.)|2024|Open X-E, Robomimic, Meta-World|DistilBERT|DistilBERT|✗|✗|✗|✗<br>✓|
|ITS (Jin et al.)|2025|*|LLaMA|A2C|✗|✓|✓|✗<br>✓|
|SIAMS (Hatanaka et al.)|2025|Miniworld|LTL|CNN|✗|✓|✓|✗<br>✗|
|<br>CRTO (Dong et al.)|2025|Continual World|ChatGPT|*|✗|✓|✓|✗<br>✓|
|LAMARL (Zhu et al.)|2025|✗|OpenAI|MADDPG|✓|✓|✓|✗<br>✓|
|ARCHIE (Turcato et al.)|2025|#|GPT-4|*|✓|✓|✓|✗<br>✓|
|RealBEF (Wang et al.)|2025|Meta-World|ALBEF|CNN|✗|✓|✓|✗<br>✗|
|<br>LLMRewardShaping (Guo et al.)|2025|Meta-World|GPT-4|*|✓|✓|✓|✗<br>✗|
|BOSS (Yang et al.)|2025|LIBERO|OpenVLA|ResNet|✗|✓|✗|✓<br>✓|
|LAV-ACT (Tripathi et al.)|2025|MuJuCo|Voltron|Voltron|✓|✗|✗|✓<br>✗|
|<br>TPM (Yang et al.)|2025|MuJuCo|GPT-4|ResNet|✓|✓|✗|✓<br>✓|
|Mamba (Tsuji)|2025|#|Mamba|Mamba|✓|✓|✗|✓<br>✓|
|TransformerPolicy (Yao et al.)|2025|CALVIN|Transformer|Sentence-BERT|✓|✗|✗|✓<br>✓|
|HierarchicalLCL (Tang et al.)|2025|CALVIN|OpenFlamingoM-3B|ViT|✗|✓|✗|✓<br>✓|
|BLADE (Liu et al.)|2025|CALVIN|GPT-4|PCT|✓|✓|✗|✓<br>✓|
|LES6DPose (Tu et al.)|2025|Isaac Gym|GPT-4|PointNet++|✓|✓|✗|✗<br>✓|
|SafetyFilter (Brunke et al.)|2025|#|GPT-4o|CLIP|✓|✓|✗|✗<br>✓|
|<br>TARAD (Hu et al.)|2025|RLBench|GPT-4o|CLIP|✓|✓|✗|✓<br>✓|
|DISCO (Hao et al.)|2025|CALVIN|GPT-4o|*|✓|✓|✗|✗<br>✓|
|<br>TinyVLA (Wen et al.)|2025|Meta-World|Pythia|MLP|✓|✓|✗|✗<br>✓|
|ASD-QR (Wang et al.)|2025|ScalingUp|GPT3|CLIP|✗|✓|✓|✗<br>✓|
|<br>RDT-1B (Liu et al.)|2025|#|GPT-4-Turbo|T5-XXL|✓|✓|✗|✓<br>✗|
|GRAVMAD (Chen et al.)|2025|RLBench|GPT-4o|CLIP|✓|✓|✗|✓<br>✓|
|<br>GR-MG (Li et al.)|2025|CALVIN|Transformer|T5-Base|✓|✗|✗|✗<br>✓|
|LEMMo-Plan (Chen et al.)|2025|✗|GPT-4o|*|✓|✓|✗|✗<br>✓|
|LGGD (Jiang et al.)|2025|✗|CLIP|CLIP, ResNet50|✓|✗|✗|✗<br>✓|
|<br>AffordanceGrasp-R1 (Zhou et al.)|2026|HANDAL|Qwen2.5-VL-72B-Instruct|SAM2|✓|✓|✓|✗<br>✓|


# Their own benchmark; * Directly get environment states; FMs: use foundational models or not; RL: Reinforcement Learning; IL: Imitation Learning; MP: Motion Planning. 

eadt1497. 

- Alakuijala M, Dulac-Arnold G, Mairal J, Ponce J and Schmid C (2023) Learning reward functions for robotic manipulation by observing humans. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . pp. 5006–5012. 

- Alakuijala M, McLean R, Woungang I, Farsad N, Kaski S, Marttinen P and Yuan K (2025) Video-language critic: Transferable reward functions for language-conditioned robotics. _Transactions on Machine Learning Research_ . 

- Alayrac JB, Donahue J, Luc P, Miech A, Barr I, Hasson Y, Lenc K, Mensch A, Millican K, Reynolds M et al. (2022) Flamingo: a visual language model for few-shot learning. _Advances in Neural Information Processing Systems_ 35: 23716–23736. 

- Aljalbout E, Sotirakis N, van der Smagt P, Karl M and Chen N (2025) Limt: Language-informed multi-task visual world models. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 8226–8233. 

- Andreas J, Klein D and Levine S (2017) Modular multitask reinforcement learning with policy sketches. _International conference on machine learning_ : 166–175. 

- Andrychowicz M, Wolski F, Ray A, Schneider J, Fong R, Welinder P, McGrew B, Tobin J, Pieter Abbeel O and Zaremba W (2017) Hindsight experience replay. In: _Advances in Neural Information Processing Systems_ , volume 30. Curran Associates, Inc., pp. 5055–5065. 

- Ao J, Wu F, Wu Y, Swiki A and Haddadin S (2025) Llm-as-btplanner: Leveraging llms for behavior tree generation in robot task planning. In: _2025 IEEE International Conference on_ 

_Robotics and Automation (ICRA)_ . IEEE, pp. 1233–1239. 

- Argall BD, Chernova S, Veloso M and Browning B (2009) A survey of robot learning from demonstration. _Robotics and Autonomous Systems_ 57(5): 469–483. 

- Arkin J, Park D, Roy S, Walter MR, Roy N, Howard TM and Paul R (2020) Multimodal estimation and communication of latent semantic knowledge for robust execution of robot instructions. _The International Journal of Robotics Research_ 39(10-11): 1279–1304. 

- Arora S and Doshi P (2021) A survey of inverse reinforcement learning: Challenges, methods and progress. _Artificial Intelligence_ 297: 103500. 

- Asuzu K, Singh H and Idrissi M (2025) Human–robot interaction through joint robot planning with large language models. _Intelligent Service Robotics_ 18(2): 261–277. 

- Bahdanau D, Hill F, Leike J, Hughes E, Hosseini A, Kohli P and Grefenstette E (2018) Learning to understand goal specifications by modelling reward. _International Conference on Learning Representations_ . 

- Bai Y, Kadavath S, Kundu S, Askell A, Kernion J, Jones A, Chen A, Goldie A, Mirhoseini A, McKinnon C et al. (2022) Constitutional ai: Harmlessness from ai feedback. _arXiv preprint arXiv:2212.08073_ . 

- Bain M and Sammut C (1995) A framework for behavioural cloning. In: _Machine Intelligence 15_ . pp. 103–129. 

- Baltruˇsaitis T, Ahuja C and Morency LP (2018) Multimodal machine learning: A survey and taxonomy. _IEEE transactions on pattern analysis and machine intelligence_ 41(2): 423–443. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

54 

- Bartoli E, Argenziano F, Suriani V and Nardi D (2022) Knowledge acquisition and completion for long-term humanrobot interactions using knowledge graph embedding. In: _2022 International Conference of the Italian Association for Artificial Intelligence_ . Springer, pp. 241–253. 

- Batra D, Chang AX, Chernova S, Davison AJ, Deng J, Koltun V, Levine S, Malik J, Mordatch I, Mottaghi R et al. (2020) Rearrangement: A challenge for embodied ai. _arXiv preprint arXiv:2011.01975_ . 

- Beetz M, Beßler D, Haidu A, Pomarlan M, Bozcuo˘glu AK and Bartels G (2018) Know rob 2.0—a 2nd generation knowledge processing framework for cognition-enabled robotic agents. In: _2018 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 512–519. 

- Belkhale S, Ding T, Xiao T, Sermanet P, Vuong Q, Tompson J, Chebotar Y, Dwibedi D and Sadigh D (2024) Rt-h: Action hierarchies using language. _Robotics: Science and Systems_ . 

- Bengio Y, Ducharme R, Vincent P and Jauvin C (2003) A neural probabilistic language model. _Journal of machine learning research_ 3(Feb): 1137–1155. 

- Besold TR, d’Avila Garcez AS, Bader S, Bowman H, Domingos PM, Hitzler P, K¨uhnberger K, Lamb LC, Lima PMV, de Penning L, Pinkas G, Poon H and Zaverucha G (2021) Neural-symbolic learning and reasoning: A survey and interpretation. In: _Neuro-Symbolic Artificial Intelligence: The State of the Art_ , volume 342. IOS Press, pp. 1–51. 

- Bharadhwaj H, Vakil J, Sharma M, Gupta A, Tulsiani S and Kumar V (2024) Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 4788–4795. 

- Bi H, Wu L, Lin T, Tan H, Su Z, Su H and Zhu J (2026) H-rdt: Human manipulation enhanced bimanual robotic manipulation. In: _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40. pp. 18135–18143. 

- Billard A and Kragic D (2019) Trends and challenges in robot manipulation. _Science_ 364(6446): eaat8414. 

- Bing Z, Koch A, Yao X, Huang K and Knoll A (2023a) Metareinforcement learning via language instructions. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 5985–5991. 

- Bing Z, Zhou H, Li R, Su X, Morin FO, Huang K and Knoll A (2023b) Solving robotic manipulation with sparse reward reinforcement learning via graph-based diversity and proximity. _IEEE Transactions on Industrial Electronics_ 70(3): 2759–2769. 

- Black K, Brown N, Darpinian J, Dhabalia K, Driess D, Esmail A et al. (2025a) _π_ 0 _._ 5: a vision-language-action model with openworld generalization. In: _Proceedings of The 8th Conference on Robot Learning_ , volume 305. PMLR, pp. 17–40. 

- Black K, Brown N, Driess D, Esmail A, Equi MR, Finn C, Fusai N, Groom L, Hausman K, Ichter B, Jakubczak S, Jones T, Ke L, Levine S, Li-Bell A, Mothukuri M, Nair S, Pertsch K, Shi LX, Smith L, Tanner J, Vuong Q, Walling A, Wang H and Zhilinsky U (2025b) _π_ 0: A Vision-Language-Action Flow Model for General Robot Control. In: _Proceedings of Robotics: Science and Systems_ . LosAngeles, CA, USA. DOI: 10.15607/RSS.2025.XXI.010. 

- Black K, Nakamoto M, Atreya P, Walke HR, Finn C, Kumar A and Levine S (2024) Zero-shot robotic manipulation with 

pre-trained image-editing diffusion models. _The Twelfth International Conference on Learning Representations_ . 

- Blank N, Reuss M, R¨uhle M, Ya˘gmurlu OE,<sup>¨</sup> Wenzel F, Mees O and Lioutikov R (2025) Scaling robot policy learning via zeroshot labeling with foundation models. In: _2025 Conference on Robot Learning_ . PMLR, pp. 4158–4187. 

- Bordes A, Usunier N, Garcia-Duran A, Weston J and Yakhnenko O (2013) Translating embeddings for modeling multi-relational data. _Advances in neural information processing systems_ 26. 

- Borja-Diaz J, Mees O, Kalweit G, Hermann L, Boedecker J and Burgard W (2022) Affordance learning from play for sampleefficient policy learning. In: _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6372–6378. 

- Brohan A, Brown N, Carbajal J, Chebotar Y, Dabis J, Finn C, Gopalakrishnan K, Hausman K, Herzog A, Hsu J et al. (2023a) Rt-1: Robotics transformer for real-world control at scale. _Robotics: Science and Systems XIX_ . 

- Brohan A, Chebotar Y, Finn C, Hausman K, Herzog A, Ho D, Ibarz J, Irpan A, Jang E, Julian R et al. (2023b) Do as i can, not as i say: Grounding language in robotic affordances. In: _Conference on robot learning_ . PMLR, pp. 287–318. 

- Brooks T, Holynski A and Efros AA (2023) Instructpix2pix: Learning to follow image editing instructions. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 18392–18402. 

- Brown T, Mann B, Ryder N, Subbiah M, Kaplan JD, Dhariwal P, Neelakantan A, Shyam P, Sastry G, Askell A et al. (2020) Language models are few-shot learners. _Advances in neural information processing systems_ 33: 1877–1901. 

- Brunke L, Zhang Y, R¨omer R, Naimer J, Staykov N, Zhou S and Schoellig AP (2025) Semantically safe robot manipulation: From semantic scene understanding to motion safeguards. _IEEE Robotics and Automation Letters_ 10(5): 4810–4817. 

- Bu Q, Zeng J, Chen L, Yang Y, Zhou G, Yan J, Luo P, Cui H, Ma Y and Li H (2024) Closed-loop visuomotor control with generative expectation for robotic manipulation. _Advances in Neural Information Processing Systems_ 37: 139002–139029. 

- Bucker A, Figueredo L, Haddadin S, Kapoor A, Ma S, Vemprala S and Bonatti R (2023) Latte: Language trajectory transformer. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 7287–7294. 

- Bucker A, Ortega-Kral P, Francis J and Oh J (2024) Grounding robot policies with visuomotor language guidance. 

- Calinon S and Billard A (2007) Active teaching in robot programming by demonstration. In: _RO-MAN 2007-The 16th IEEE International Symposium on Robot and Human Interactive Communication_ . IEEE, pp. 702–707. 

- Cambon S, Alami R and Gravot F (2009) A hybrid approach to intricate motion, manipulation and task planning. _The International Journal of Robotics Research_ 28(1): 104–126. 

- Capitanelli A and Mastrogiovanni F (2024) A framework for neurosymbolic robot action planning using large language models. _Frontiers in Neurorobotics_ 18: 1342786. 

- Cen J, Yu C, Yuan H, Jiang Y, Huang S, Guo J, Li X, Song Y, Luo H, Wang F et al. (2025) Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ . 

- Ceola F, Tosello E, Tagliapietra L, Nicola G and Ghidoni S (2019) Robot task planning via deep reinforcement learning: a tabletop object sorting application. In: _2019 IEEE International Conference on Systems, Man and Cybernetics (SMC)_ . IEEE, 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

55 

pp. 486–492. 

- Chai J, Gao Q, She L, Yang S, Saba-Sadiya S and Xu G (2018) Language to action: Towards interactive task learning with physical agents. In: Lang J (ed.) _Proceedings of the Twenty-Seventh International Joint Conference on Artificial Intelligence, IJCAI 2018, July 13-19, 2018, Stockholm, Sweden_ . ijcai.org, pp. 2–9. 

- Chai JY, She L, Fang R, Ottarson S, Littley C, Liu C and Hanson K (2014) Collaborative effort towards common ground in situated human-robot dialogue. In: _Proceedings of the 2014 ACM/IEEE international conference on Human-robot interaction_ . pp. 33– 40. 

- Chalvatzaki G, Younes A, Nandha D, Le AT, Ribeiro LF and Gurevych I (2023) Learning to reason over scene graphs: a case study of finetuning gpt-2 into a robot language model for grounded task planning. _Frontiers in Robotics and AI_ 10: 1221739. 

- Chaplot DS, Sathyendra KM, Pasumarthi RK, Rajagopal D and Salakhutdinov R (2018) Gated-attention architectures for taskoriented language grounding. In: _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 32. pp. 2819– 2826. 

- Chaudhry A, Marc’Aurelio R, Rohrbach M and Elhoseiny M (2019) Efficient lifelong learning with a-gem. _7th International Conference on Learning Representations_ . 

- Cheang C, Chen S, Cui Z, Hu Y, Huang L, Kong T, Li H, Li Y, Liu Y, Ma X et al. (2025) Gr-3 technical report. _arXiv preprint arXiv:2507.15493_ . 

- Chen B, Xia F, Ichter B, Rao K, Gopalakrishnan K, Ryoo MS, Stone A and Kappler D (2023a) Open-vocabulary queryable scene representations for real world planning. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 11509–11522. 

- Chen G, Wang M, Cui T, Yang C, Hu M, Lu H, Peng Z, Zhou T, Jiang X, Yang Y and Yue Y (2026) Learning from videos through graph-to-graphs generative modeling for robotic manipulation. _IEEE Transactions on Robotics_ 42: 1158–1177. 

- Chen H, Tan H, Kuntz A, Bansal M and Alterovitz R (2020a) Enabling robots to understand incomplete natural language instructions using commonsense reasoning. In: _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 1963–1969. 

- Chen J, Zhao W, Meng Z, Mao D, Song R, Pan W and Zhang W (2025a) Vision-language model predictive control for manipulation planning and trajectory generation. _arXiv preprint arXiv:2504.05225_ . 

- Chen K, Shen Z, Zhang Y, Chen L, Wu F, Bing Z, Haddadin S and Knoll A (2025b) Lemmo-plan: Llm-enhanced learning from multi-modal demonstration for planning sequential contactrich manipulation tasks. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 11972–11978. 

- Chen L, Bahl S and Pathak D (2023b) Playfusion: Skill acquisition via diffusion from language-annotated play. In: _Conference on Robot Learning_ . PMLR, pp. 2012–2029. 

- Chen L, Lei Y, Jin S, Zhang Y and Zhang L (2024a) Rlingua: Improving reinforcement learning sample efficiency in robotic manipulations with large language models. _IEEE Robotics and Automation Letters_ 9(7): 6075–6082. 

- Chen L, Moorman NM and Gombolay MC (2025c) ELEMENTAL: Interactive learning from demonstrations and vision-language models for reward design in robotics. In: _Proceedings of the 42nd International Conference on Machine Learning_ . PMLR, pp. 8700–8725. 

- Chen M, Tworek J, Jun H, Yuan Q, Pinto HPdO, Kaplan J, Edwards H, Burda Y, Joseph N, Brockman G et al. (2021) Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ . 

- Chen W, Belkhale S, Mirchandani S, Pertsch K, Driess D, Mees O and Levine S (2025d) Training Strategies for Efficient Embodied Reasoning. In: _Proceedings of The 9th Conference on Robot Learning_ , volume 305. PMLR, pp. 365–391. 

- Chen W, Mees O, Kumar A and Levine S (2025e) Vision-language models provide promptable representations for reinforcement learning. _Transactions on Machine Learning Research_ . 

- Chen W, Zeng C, Liang H, Sun F and Zhang J (2023c) Multimodality driven impedance-based sim2real transfer learning for robotic multiple peg-in-hole assembly. _IEEE Transactions on Cybernetics_ 54(5): 2784–2797. 

- Chen X, Cai Y, Mao Y, Li M, Yang W, Xu W and Wang J (2024b) Integrating intent understanding and optimal behavior planning for behavior tree generation from human instructions. In: _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ . pp. 6832–6840. 

- Chen X, Djolonga J, Padlewski P, Mustafa B, Changpinyo S, Wu J, Ruiz CR, Goodman S, Wang X, Tay Y et al. (2023d) Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ . 

- Chen X, Ma Z, Zhang X, Xu S, Qian S, Yang J, Fouhey D and Chai J (2024c) Multi-object hallucination in vision language models. _Advances in Neural Information Processing Systems_ 37: 44393–44418. 

- Chen Y, Chen Z, Yin J, Huo J, Tian P, Shi J and Gao Y (2025f) GravMAD: Grounded spatial value maps guided action diffusion for generalized 3d manipulation. _The Thirteenth International Conference on Learning Representations_ . 

- Chen Y, Tian S, Zhou Y, Liu S, Li H and Zhao D (2025g) Conrft: A reinforced fine-tuning method for vla models via consistency policy. _arXiv preprint arXiv:2502.05450_ . 

- Chen YC, Li L, Yu L, El Kholy A, Ahmed F, Gan Z, Cheng Y and Liu J (2020b) Uniter: Universal image-text representation learning. In: _European conference on computer vision_ . Springer, pp. 104–120. 

- Chen Z, Mandi Z, Bharadhwaj H, Sharma M, Song S, Gupta A and Kumar V (2024d) Semantically controllable augmentations for generalizable robot learning. _The International Journal of Robotics Research_ : 02783649241273686. 

- Cheng HK and Schwing AG (2022) Xmem: Long-term video object segmentation with an atkinson-shiffrin memory model. In: _European conference on computer vision_ . Springer, pp. 640– 658. 

- Cheng Z, Zhang Y, Zhang W, Li H, Wang K, Song L and Zhang H (2025) Omnivtla: Vision-tactile-language-action model with semantic-aligned tactile sensing. _arXiv preprint arXiv:2508.08706_ . 

- Chi C, Feng S, Du Y, Xu Z, Cousineau E, Burchfiel B and Song S (2023) Diffusion policy: Visuomotor policy learning via action diffusion. _Robotics: Science and Systems_ . 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

56 

- Cho J, Lei J, Tan H and Bansal M (2021) Unifying visionand-language tasks via text generation. In: _International Conference on Machine Learning_ . PMLR, pp. 1931–1942. 

- Chowdhery A, Narang S, Devlin J, Bosma M, Mishra G, Roberts A, Barham P, Chung HW, Sutton C, Gehrmann S et al. (2023) Palm: Scaling language modeling with pathways. _Journal of Machine Learning Research_ 24(240): 1–113. 

- Clark HH (1996) _Using language_ . Cambridge university press. 

- Cleveston I, Santana AC, Costa PD, Gudwin RR, Sim˜oes AS and Colombini EL (2025) Instructrobot: A model-free framework for mapping natural language instructions into robot motion. _arXiv preprint arXiv:2502.12861_ . 

- Cobbe K, Kosaraju V, Bavarian M, Chen M, Jun H, Kaiser L, Plappert M, Tworek J, Hilton J, Nakano R et al. (2021) Training verifiers to solve math word problems. _arXiv preprint arXiv:2110.14168_ . 

- Cohen V, Liu JX, Mooney R, Tellex S and Watkins D (2024) A survey of robotic language grounding: tradeoffs between symbols and embeddings. In: _Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence_ . pp. 7999–8009. 

- Colas C, Akakzia A, Oudeyer PY, Chetouani M and Sigaud O (2020) Language-conditioned goal generation: a new approach to language grounding for rl. _preprint arXiv:2006.07043_ . 

- Collobert R, Weston J, Bottou L, Karlen M, Kavukcuoglu K and Kuksa P (2011) Natural language processing (almost) from scratch. _Journal of machine learning research_ 12(ARTICLE): 2493–2537. 

- Coumans E and Bai Y (2016–2021) Pybullet, a python module for physics simulation for games, robotics and machine learning. http://pybullet.org. 

- Dai Y, Lee J, Fazeli N and Chai J (2025) Racer: Rich languageguided failure recovery policies for imitation learning. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 15657–15664. 

- Das N, Bechtle S, Davchev T, Jayaraman D, Rai A and Meier F (2021) Model-based inverse reinforcement learning from visual demonstrations. _Conference on Robot Learning_ : 1930– 1942. 

- Dasari S, Mees O, Zhao S, Srirama MK and Levine S (2025) The ingredients for robotic diffusion transformers. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 15617–15625. 

- Deng Y, Mo K, Xia C and Wang X (2024) Learning languageconditioned deformable object manipulation with graph dynamics. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 7508–7514. 

- Deshpande S, Walambe R, Kotecha K, Selvachandran G and Abraham A (2025) Advances and applications in inverse reinforcement learning: a comprehensive review. _Neural Computing and Applications_ : 1–53. 

- Devlin J, Chang MW, Lee K and Toutanova K (2019) Bert: Pre-training of deep bidirectional transformers for language understanding. In: _Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics: human language technologies, volume 1 (long and short papers)_ . pp. 4171–4186. 

- Di Palo N and Johns E (2024) Keypoint action tokens enable incontext imitation learning in robotics. _Proceedings of Robotics: Science and Systems (RSS)_ . 

- Diab M, Akbari A, Ud Din M and Rosell J (2019) Pmk—a knowledge processing framework for autonomous robotics perception and manipulation. _Sensors_ 19(5): 1166. 

- Dimitrakakis C and Rothkopf CA (2011) Bayesian multitask inverse reinforcement learning. In: _European workshop on reinforcement learning_ . Springer, pp. 273–284. 

- Ding Y, Florensa C, Abbeel P and Phielipp M (2019) Goalconditioned imitation learning. _Advances in neural information processing systems_ 32. 

- Ding Y, Zhang X, Amiri S, Cao N, Yang H, Esselink C and Zhang S (2022) Robot task planning and situation handling in open worlds. _arXiv preprint arXiv:2210.01287_ . 

- Ding Y, Zhang X, Paxton C and Zhang S (2023) Task and motion planning with large language models for object rearrangement. In: _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 2086–2092. 

- Dong Q, Wu T, Zeng P, zang C, Wan G and Cui S (2025) Enhancing robot learning through cognitive reasoning trajectory optimization under unknown dynamics. _IEEE Robotics and Automation Letters_ 10(6): 5401–5408. 

- Doshi R, Walke HR, Mees O, Dasari S and Levine S (2025) Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. In: _2025 Conference on Robot Learning_ . PMLR, pp. 496–512. 

- Dosovitskiy A, Beyer L, Kolesnikov A, Weissenborn D, Zhai X, Unterthiner T, Dehghani M, Minderer M, Heigold G, Gelly S, Uszkoreit J and Houlsby N (2021) An image is worth 16x16 words: Transformers for image recognition at scale. _International Conference on Learning Representations_ . 

- Driess D, Schubert I, Florence P, Li Y and Toussaint M (2022) Reinforcement learning with neural radiance fields. _Advances in Neural Information Processing Systems_ 35: 16931–16945. 

- Driess D, Springenberg J, Ichter B, Yu L, Li-Bell A, Pertsch K, Ren A, Walke H, Vuong Q, Shi LX et al. (2026) Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. _Advances in Neural Information Processing Systems_ 38: 102867–102888. 

- Driess D, Xia F, Sajjadi MS, Lynch C, Chowdhery A, Ichter B, Wahid A, Tompson J, Vuong Q, Yu T et al. (2023) Palm-e: an embodied multimodal language model. In: _Proceedings of the 40th International Conference on Machine Learning_ . pp. 8469–8488. 

- Du Y, Konyushkova K, Denil M, Raju A, Landon J, Hill F, de Freitas N and Cabi S (2023a) Vision-language models as success detectors. In: Chandar S, Pascanu R, Sedghi H and Precup D (eds.) _Proceedings of The 2nd Conference on Lifelong Learning Agents_ , _Proceedings of Machine Learning Research_ , volume 232. PMLR, pp. 120–136. 

- Du Y, Yang S, Dai B, Dai H, Nachum O, Tenenbaum J, Schuurmans D and Abbeel P (2023b) Learning universal policies via textguided video generation. _Advances in neural information processing systems_ 36: 9156–9172. 

- Duan J, Pumacay W, Kumar N, Wang YR, Tian S, Yuan W, Krishna R, Fox D, Mandlekar A and Guo Y (2024) Aha: A visionlanguage-model for detecting and reasoning over failures in robotic manipulation. _arXiv preprint arXiv:2410.00371_ . 

- Ebert F, Finn C, Dasari S, Xie A, Lee A and Levine S (2018) Visual foresight: Model-based deep reinforcement learning for visionbased robotic control. _arXiv preprint arXiv:1812.00568_ . 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

57 

- Eschmann J (2021) Reward function design in reinforcement learning. _Reinforcement learning algorithms: Analysis and Applications_ : 25–33. 

- Eze C and Crick C (2025) Learning by watching: A review of video-based learning approaches for robot manipulation. _IEEE Access_ 13: 184071–184109. 

- Fan Y, Bai S, Tong X, Ding P, Zhu Y, Lu H, Dai F, Zhao W, Liu Y, Huang S, Fan Z, Chen B and Wang D (2025) Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation. In: _Proceedings of The 9th Conference on Robot Learning_ , volume 305. pp. 2018–2037. 

- Fellbaum C (1998) Wordnet: An electronic lexical database. _MIT Press google schola_ 2: 678–686. 

- Fikes RE and Nilsson NJ (1971) Strips: A new approach to the application of theorem proving to problem solving. _Artificial intelligence_ 2(3-4): 189–208. 

- Finn C, Levine S and Abbeel P (2016) Guided cost learning: Deep inverse optimal control via policy optimization. In: _International conference on machine learning_ . PMLR, pp. 49– 58. 

- Firoozi R, Tucker J, Tian S, Majumdar A et al. (2025) Foundation models in robotics: Applications, challenges, and the future. _The International Journal of Robotics Research_ 44(5): 701– 739. 

- Florence P, Lynch C, Zeng A, Ramirez OA, Wahid A, Downs L, Wong A, Lee J, Mordatch I and Tompson J (2022) Implicit behavioral cloning. In: _Conference on Robot Learning_ . PMLR, pp. 158–168. 

- Fu J, Korattikara A, Levine S and Guadarrama S (2019) From language to goals: Inverse reinforcement learning for visionbased instruction following. _International Conference on Learning Representations_ . 

- Funke J (2010) Complex problem solving: A case for complex cognition? _Cognitive processing_ 11: 133–142. 

- Gan C, Zhou S, Schwartz J, Alter S, Bhandwaldar A, Gutfreund D, Yamins DL, DiCarlo JJ, McDermott J, Torralba A and Tenenbaum JB (2022) The threedworld transport challenge: A visually guided task-and-motion planning benchmark towards physically realistic embodied ai. In: _2022 International Conference on Robotics and Automation_ . pp. 8847–8854. 

- Gao C, Liu Z, Chi Z, Huang J, Fei X, Hou Y, Zhang Y, Lin Y, Fang Z, Jiang Z and Lin S (2026) Vla-os: Structuring and dissecting planning representations and paradigms in vision-languageaction models. _Advances in Neural Information Processing Systems_ 38: 136705–136736. 

- Gao Q, Doering M, Yang S and Chai J (2016) Physical causality of action verbs in grounded language understanding. In: _Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . pp. 1814– 1824. 

- Gao Q, Yang S, Chai J and Vanderwende L (2018) What action causes this? towards naive physical action-effect prediction. In: _Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1)_ . pp. 934–945. 

- Gao S, Wen XC, Gao C, Wang W, Zhang H and Lyu MR (2023) What makes good in-context demonstrations for code intelligence tasks with llms? In: _2023 38th IEEE/ACM International Conference on Automated Software Engineering (ASE)_ . IEEE, pp. 761–773. 

- Garrett CR, Lozano-P´erez T and Kaelbling LP (2020) Pddlstream: Integrating symbolic planners and blackbox samplers via optimistic adaptive planning. In: _Proceedings of the international conference on automated planning and scheduling_ , volume 30. pp. 440–448. 

- Gbagbe KF, Cabrera MA, Alabbas A, Alyunes O, Lykov A and Tsetserukou D (2024) Bi-vla: Vision-language-action modelbased system for bimanual robotic dexterous manipulations. In: _2024 IEEE International Conference on Systems, Man, and Cybernetics (SMC)_ . IEEE, pp. 2864–2869. 

- Gervet T, Xian Z, Gkanatsios N and Fragkiadaki K (2023) Act3d: 3d feature field transformers for multi-task robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 3949–3965. 

- Girshick R (2015) Fast r-cnn. In: _Proceedings of the IEEE international conference on computer vision_ . pp. 1440–1448. 

- Glazer N, Navon A, Shamsian A and Fetaya E (2024) Multi task inverse reinforcement learning for common sense reward. _arXiv preprint arXiv:2402.11367_ . 

- Goldin-Meadow S (2005) _Hearing gesture: How our hands help us think_ . Harvard University Press. 

- Gong R, Gao X, Gao Q, Shakiah S, Thattai G and Sukhatme GS (2023a) Lemma: Learning language-conditioned multi-robot manipulation. _IEEE Robotics and Automation Letters_ 8(10): 6835–6842. 

- Gong R et al. (2023b) ARNOLD: A benchmark for languagegrounded task learning with continuous states in realistic 3d scenes. In: _ICCV_ . IEEE, pp. 20426–20438. 

- Gou J, Yu B, Maybank SJ and Tao D (2021) Knowledge distillation: A survey. _International Journal of Computer Vision_ 129(6): 1789–1819. 

- Goyal A, Xu J, Guo Y, Blukis V, Chao YW and Fox D (2023) Rvt: Robotic view transformer for 3d object manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 694–710. 

- Goyal P, Niekum S and Mooney R (2021) Pixl2r: Guiding reinforcement learning using natural language by mapping pixels to rewards. In: _Conference on Robot Learning_ . PMLR, pp. 485–497. 

- Goyal P, Niekum S and Mooney RJ (2019) Using natural language for reward shaping in reinforcement learning. In: _Proceedings of the 28th International Joint Conference on Artificial Intelligence_ . pp. 2385–2391. 

- Gu J, Kirmani S, Wohlhart P, Lu Y, Arenas MG, Rao K, Yu W, Fu C, Gopalakrishnan K, Xu Z, Sundaresan P, Xu P, Su H, Hausman K, Finn C, Vuong Q and Xiao T (2024a) Rt-trajectory: Robotic task generalization via hindsight trajectory sketches. _International Conference on Learning Representations_ . 

- Gu X, Wen C, Ye W, Song J and Gao Y (2024b) Seer: Language instructed video prediction with latent diffusion models. _The Twelfth International Conference on Learning Representations_ 

- Guhur PL, Chen S, Pinel RG, Tapaswi M, Laptev I and Schmid C (2023) Instruction-driven history-aware policies for robotic manipulations. In: _Conference on Robot Learning_ . PMLR, pp. 175–187. 

- Guo D, Yang D, Zhang H, Song J, Wang P, Zhu Q, Xu R, Zhang R, Ma S, Bi X et al. (2025) Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. _Nature_ 645(8081): 633– 638. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

58 

- Guo Q, Liu X, Hui J, Liu Z and Huang P (2024) Utilizing large language models for robot skill reward shaping in reinforcement learning. In: _International Conference on Intelligent Robotics and Applications_ . Springer, pp. 3–17. 

- Ha H, Florence P and Song S (2023) Scaling up and distilling down: Language-guided robot skill acquisition. _Conference on Robot Learning_ : 3766–3777. 

- Habekost JG, G¨ade C, Allgeuer P and Wermter S (2024) Inverse kinematics for neuro-robotic grasping with humanoid embodied agents. In: _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 7315– 7322. 

- Habibian S, Alvarez Valdivia A, Blumenschein LH and Losey DP (2025) A survey of communicating robot learning during human-robot interaction. _The International Journal of Robotics Research_ 44(4): 665–698. 

- Hafner D, Pasukonis J, Ba J and Lillicrap T (2025) Mastering diverse control tasks through world models. _Nature_ : 1–7. 

- Hao C, Lin K, Xue Z, Luo S and Soh H (2025) Disco: Languageguided manipulation with diffusion policies and constrained inpainting. _IEEE Robotics and Automation Letters_ 10(10): 9726–9733. 

- Hatanaka W, Yamashina R and Matsubara T (2025) Reinforcement learning of flexible policies for symbolic instructions with adjustable mapping specifications. _IEEE Robotics and Automation Letters_ 10(3): 2614–2621. 

- Hatori J, Kikuchi Y, Kobayashi S, Takahashi K, Tsuboi Y, Unno Y, Ko W and Tan J (2018) Interactively picking real-world objects with unconstrained spoken language instructions. In: _2018 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 3774–3781. 

- He K, Zhang X, Ren S and Sun J (2016) Deep residual learning for image recognition. In: _Proceedings of the IEEE conference on computer vision and pattern recognition_ . pp. 770–778. 

- Hermann KM, Hill F, Green S, Wang F, Faulkner R, Soyer H, Szepesvari D, Czarnecki WM, Jaderberg M, Teplyashin D et al. (2017) Grounded language learning in a simulated 3d world. _arXiv preprint arXiv:1706.06551_ . 

- Hirose N, Glossop C, Sridhar A, Mees O and Levine S (2025) Lelan: Learning a language-conditioned navigation policy from in-the-wild video. In: _Conference on Robot Learning_ . PMLR, pp. 666–688. 

- Ho J, Jain A and Abbeel P (2020) Denoising diffusion probabilistic models. _Advances in neural information processing systems_ 33: 6840–6851. 

- Hoffmann J, Borgeaud S et al. (2022) Training compute-optimal large language models. _International Conference on Neural Information Processing Systems_ : 30016–30030. 

- Hong Y, Zhen H, Chen P, Zheng S, Du Y, Chen Z and Gan C (2023) 3d-llm: Injecting the 3d world into large language models. _Advances in Neural Information Processing Systems_ 36: 20482–20494. 

- Hoque R, Seita D et al. (2022) Visuospatial foresight for physical sequential fabric manipulation. _Autonomous Robots_ 46(1): 175–199. 

- Hu EJ, Shen Y, Wallis P, Allen-Zhu Z, Li Y, Wang S, Wang L and Chen W (2022) Lora: Low-rank adaptation of large language models. In: _ICLR_ . OpenReview.net. 

- Hu J, Hendrix R, Farhadi A, Kembhavi A, Mart´ın-Mart´ın R, Stone P, Zeng KH and Ehsani K (2025a) Flare: Achieving masterful 

and adaptive robot policies with large-scale reinforcement learning fine-tuning. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 3617–3624. 

- Hu S, Nagai T and Horii T (2025b) Tarad: Task-aware robot affordance-centric diffusion policy learned from llm-generated demonstrations. _IEEE Robotics and Automation Letters_ 10(10): 10122–10129. 

- Hu Y et al. (2023) Toward general-purpose robots via foundation models: A survey and meta-analysis. _CoRR_ abs/2312.08782. 

- Hu Z, Yao X, Meng Y, Bing Z and Knoll A (2026) Dreaming the unseen: World model-regularized diffusion policy for out-ofdistribution robustness. URL https://arxiv.org/abs/ 2603.21017. 

- Huang J, Wang S, Lin F, Hu Y, Wen C and Gao Y (2025a) Tactile-vla: Unlocking vision-language-action model’s physical knowledge for tactile generalization. _arXiv preprint arXiv:2507.09160_ . 

- Huang J, Yong S, Ma X, Linghu X, Li P, Wang Y, Li Q, Zhu SC, Jia B and Huang S (2024a) An embodied generalist agent in 3d world. In: _Proceedings of the 41st International Conference on Machine Learning_ . pp. 20413–20451. 

- Huang S, Jiang Z, Dong H, Qiao Y, Gao P and Li H (2023a) Instruct2act: Mapping multi-modality instructions to robotic actions with large language model. _arXiv preprint arXiv:2305.11176_ . 

- Huang W, Abbeel P, Pathak D and Mordatch I (2022) Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In: _International Conference on Machine Learning_ . PMLR, pp. 9118–9147. 

- Huang W, Ji J, Xia C, Zhang B and Yang Y (2024b) Safedreamer: Safe reinforcement learning with world models. In: _The Twelfth International Conference on Learning Representations_ . 

- Huang W, Wang C, Li Y, Zhang R and Fei-Fei L (2025b) Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. In: _2025 Conference on Robot Learning_ . PMLR, pp. 4573–4602. 

- Huang W, Wang C, Zhang R, Li Y, Wu J and Fei-Fei L (2023b) Voxposer: Composable 3d value maps for robotic manipulation with language models. In: _Conference on Robot Learning_ . PMLR, pp. 540–562. 

- Huang W, Xia F, Xiao T, Chan H, Liang J, Florence P, Zeng A, Tompson J, Mordatch I, Chebotar Y et al. (2023c) Inner monologue: Embodied reasoning through planning with language models. In: _Conference on Robot Learning_ . PMLR, pp. 1769–1782. 

- Hurst A, Lerer A, Goucher AP, Perelman A, Ramesh A, Clark A, Ostrow A, Welihinda A, Hayes A, Radford A et al. (2024) Gpt4o system card. _arXiv preprint arXiv:2410.21276_ . 

- Hwang M, Forsey-Smerek A and Bobu A (2025) Masked Inverse Reinforcement Learning for Language Conditioned Reward Learning. In: _Human-to-Robot (H2R) Workshop at the 9th Conference on Robot Learning (CoRL 2025)_ . 

- Ibarz J, Tan J, Finn C, Kalakrishnan M, Pastor P and Levine S (2021) How to train your robot with deep reinforcement learning: lessons we have learned. _The International Journal of Robotics Research_ 40(4-5): 698–721. 

- Iovino M, Scukins E, Styrud J, Ogren<sup>¨</sup> P and Smith C (2022) A survey of behavior trees in robotics and ai. _Robotics and Autonomous Systems_ 154: 104096. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

59 

- Jacobs RA, Jordan MI, Nowlan SJ and Hinton GE (1991) Adaptive mixtures of local experts. _Neural computation_ 3(1): 79–87. 

- James S, Ma Z, Arrojo DR and Davison AJ (2020) Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ 5(2): 3019–3026. 

- Jang E, Irpan A, Khansari M, Kappler D, Ebert F, Lynch C, Levine S and Finn C (2022) Bc-z: Zero-shot task generalization with robotic imitation learning. In: _Conference on Robot Learning_ . PMLR, pp. 991–1002. 

- Jangir R, Alenya G and Torras C (2020) Dynamic cloth manipulation with deep reinforcement learning. In: _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 4630–4636. 

- Janner M, Narasimhan K and Barzilay R (2018) Representation learning for grounded spatial reasoning. _Transactions of the Association for Computational Linguistics_ 6: 49–61. 

- Jenamani RK, Silver T, Dodson B, Tong S, Song A, Yang Y, Liu Z, Howe B, Whitneck A and Bhattacharjee T (2025) Feast: A flexible mealtime-assistance system towards in-thewild personalization. _Robotics: Science and Systems (RSS)_ . 

- Jiang H, Huang B, Wu R, Li Z, Garg S, Nayyeri H, Wang S and Li Y (2025a) Roboexp: Action-conditioned scene graph via interactive exploration for robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 3027–3052. 

- Jiang T, Yuan T, Liu Y, Lu C, Cui J, Liu X, Cheng S, Gao J, Xu H and Zhao H (2025b) Galaxea open-world dataset and g0 dualsystem vla model. _arXiv preprint arXiv:2509.00576_ . 

- Jiang Y, Gupta A, Zhang Z, Wang G, Dou Y, Chen Y, Li F, Anandkumar A, Zhu Y and Fan L (2023) VIMA: Robot Manipulation with Multimodal Prompts. In: _Proceedings of the 40th International Conference on Machine Learning_ , volume 202. PMLR, pp. 14975–15022. 

- Jiang Z, Jin T, Yao X, Knoll A and Cao H (2025c) Languageguided grasp detection with coarse-to-fine learning for robotic manipulation. _arXiv preprint arXiv:2512.21065_ . 

- Jin C, Tan W, Yang J, Liu B, Song R, Wang L and Fu J (2023) Alphablock: Embodied finetuning for visionlanguage reasoning in robot manipulation. _arXiv preprint arXiv:2305.18898_ . 

- Jin K, Tian G, Huang B, Cui Y and Zheng X (2025) Task-oriented adaptive learning of robot manipulation skills. _Artificial Life and Robotics_ : 1–10. 

- Jones J, Mees O, Sferrazza C, Stachowicz K, Abbeel P and Levine S (2025) Beyond sight: Finetuning generalist robot policies with heterogeneous sensors via language grounding. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . pp. 5961–5968. DOI:10.1109/ICRA55743.2025.11127987. 

- Ju Z, Yang C, Sun F, Wang H and Qiao Y (2024) Rethinking mutual information for language conditioned skill discovery on imitation learning. In: _Proceedings of the International Conference on Automated Planning and Scheduling_ , volume 34. pp. 301– 309. 

- K N, Singh H, Bindal V, Tuli A, Agrawal V, Jain R, Singla P and Paul R (2023) Learning neuro-symbolic programs for language guided robot manipulation. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . pp. 7973– 7980. 

- Kamath A, Singh M, LeCun Y, Synnaeve G, Misra I and Carion N (2021) Mdetr-modulated detection for end-to-end multi-modal understanding. In: _Proceedings of the IEEE/CVF international_ 

_conference on computer vision_ . pp. 1780–1790. 

- Kang G, Kim J, Shim K, Lee JK and Zhang B (2024) CLIP-RT: learning language-conditioned robotic policies from natural language supervision. _CoRR_ abs/2411.00508. 

- Kant Y, Ramachandran A, Yenamandra S, Gilitschenski I, Batra D, Szot A and Agrawal H (2022) Housekeep: Tidying virtual households using commonsense reasoning. In: _European Conference on Computer Vision_ . Springer, pp. 355–373. 

- Kapelyukh I, Ren Y, Alzugaray I and Johns E (2024) Dream2real: Zero-shot 3d object rearrangement with vision-language models. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 4796–4803. 

- Kapelyukh I, Vosylius V and Johns E (2023) Dall-e-bot: Introducing web-scale diffusion models to robotics. _IEEE Robotics and Automation Letters_ 8(7): 3956–3963. 

- Kaplan R, Sauer C and Sosa A (2017) Beating atari with natural language guided reinforcement learning. _arXiv preprint arXiv:1704.05539_ . 

- Karaman S and Frazzoli E (2011) Sampling-based algorithms for optimal motion planning. _The international journal of robotics research_ 30(7): 846–894. 

- Karli UB, Chen JT, Antony VN and Huang CM (2024) Alchemist: Llm-aided end-user development of robot applications. In: _Proceedings of the 2024 ACM/IEEE International Conference on Human-Robot Interaction_ . pp. 361–370. 

- Kawaharazuka K, Oh J, Yamada J, Posner I and Zhu Y (2025) Vision-language-action models for robotics: A review towards real-world applications. _IEEE Access_ 13: 162467–162504. 

- Ke TW, Gkanatsios N and Fragkiadaki K (2025) 3d diffuser actor: Policy diffusion with 3d scene representations. _Conference on Robot Learning_ : 1949–1974. 

- Kerr J, Hari K, Weber E, Kim CM, Yi B, Goldberg K, Kanazawa A et al. (2025) Eye, robot: Learning to look to act with a bcrl perception-action loop. In: _Conference on Robot Learning_ . PMLR, pp. 3647–3664. 

- Kerr J, Kim CM, Goldberg K, Kanazawa A and Tancik M (2023) Lerf: Language embedded radiance fields. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 19729–19739. 

- Khandelwal A, Weihs L, Mottaghi R and Kembhavi A (2022) Simple but effective: CLIP embeddings for embodied AI. In: _CVPR_ . IEEE, pp. 14809–14818. 

- Khazatsky A, Pertsch K, Nair S, Balakrishna A, Dasari S, Karamcheti S, Nasiriany S, Srirama MK, Chen LY, Ellis K et al. (2024) Droid: A large-scale in-the-wild robot manipulation dataset. _Robotics: Science and Systems_ . 

- Kim JW, Chen JT, Hansen P, Shi LX, Goldenberg A, Schmidgall S, Scheikl PM, Deguet A, White BM, Tsai DR et al. (2025a) Srt-h: A hierarchical framework for autonomous surgery via language-conditioned imitation learning. _Science robotics_ 10(104): eadt5254. 

- Kim MJ, Finn C and Liang P (2025b) Fine-Tuning VisionLanguage-Action Models: Optimizing Speed and Success. In: _Proceedings of Robotics: Science and Systems_ . LosAngeles, CA, USA. DOI:10.15607/RSS.2025.XXI.017. 

- Kim MJ, Pertsch K, Karamcheti S, Xiao T, Balakrishna A, Nair S, Rafailov R, Foster EP, Sanketi PR, Vuong Q et al. (2025c) Openvla: An open-source vision-language-action model. In: _Conference on Robot Learning_ . PMLR, pp. 2679–2713. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

60 

- Kintsch W (1998) _Comprehension: A paradigm for cognition_ . Cambridge university press. 

- Kirillov A, Mintun E, Ravi N, Mao H, Rolland C, Gustafson L, Xiao T, Whitehead S, Berg AC, Lo WY et al. (2023) Segment anything. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 4015–4026. 

- Kirkpatrick J, Pascanu R, Rabinowitz N, Veness J, Desjardins G, Rusu AA, Milan K, Quan J, Ramalho T, Grabska-Barwinska A et al. (2017) Overcoming catastrophic forgetting in neural networks. _Proceedings of the national academy of sciences_ 114(13): 3521–3526. 

- Knoll A, Hildenbrandt B and Zhang J (1997) Instructing cooperating assembly robots through situated dialogues in natural language. In: _Proceedings of International Conference on Robotics and Automation_ , volume 1. pp. 888–894 vol.1. 

- Ko PC, Mao J, Du Y, Sun SH and Tenenbaum JB (2024) Learning to act from actionless videos through dense correspondences. In: _2024 The Twelfth International Conference on Learning Representations_ . 

- Kobayashi T, Kobayashi M, Buamanee T and Uranishi Y (2025) Bi-lat: Bilateral control-based imitation learning via natural language and action chunking with transformers. In: _2025 34th IEEE International Conference on Robot and Human Interactive Communication (RO-MAN)_ . pp. 1609–1616. 

- Kolve E, Mottaghi R, Han W, VanderBilt E, Weihs L, Herrasti A, Deitke M, Ehsani K, Gordon D, Zhu Y et al. (2017) Ai2-thor: An interactive 3d environment for visual ai. _arXiv preprint arXiv:1712.05474_ . 

- Kombrink S, Mikolov T, Karafi´at M and Burget L (2011) Recurrent neural network based language modeling in meeting recognition. In: _Interspeech_ , volume 11. pp. 2877–2880. 

- Kress-Gazit H, Fainekos GE and Pappas GJ (2009) Temporal-logicbased reactive mission and motion planning. _IEEE transactions on robotics_ 25(6): 1370–1381. 

- Kumar S, Zamora J, Hansen N, Jangir R and Wang X (2023) Graph inverse reinforcement learning from diverse videos. In: _Proceedings of The 6th Conference on Robot Learning_ , _Proceedings of Machine Learning Research_ , volume 205. PMLR, pp. 55–66. 

- Kwak JH, Lee J, Whang JJ and Jo S (2022) Semantic grasping via a knowledge graph of robotic manipulation: A graph representation learning approach. _IEEE Robotics and Automation Letters_ 7(4): 9397–9404. 

- Kwon M, Xie SM, Bullard K and Sadigh D (2023) Reward design with language models. In: _The Eleventh International Conference on Learning Representations_ . 

- Kwon T, Di Palo N and johns E (2024) Language models as zeroshot trajectory generators. _IEEE Robotics and Automation Letters_ 9(7). 

- La Valle SM (2011) Motion planning. _IEEE Robotics & Automation Magazine_ 18(2): 108–118. 

- Ladosz P, Weng L, Kim M and Oh H (2022) Exploration in deep reinforcement learning: A survey. _Inf. Fusion_ 85: 1–22. 

- Lee S, Park S and Kim H (2025) Dynscene: Scalable generation of dynamic robotic manipulation scenes for embodied ai. In: _Proceedings of the Computer Vision and Pattern Recognition Conference_ . pp. 12166–12175. 

- Li B, Weinberger KQ, Belongie S, Koltun V and Ranftl R (2022) Language-driven semantic segmentation. _International Conference on Learning Representations_ . 

- Li C, Wen J, Peng Y, Peng Y and Zhu Y (2026a) Pointvla: Injecting the 3d world into vision-language-action models. _IEEE Robotics and Automation Letters_ 11(3): 2506–2513. 

- Li D, Jin Y, Sun Y, Yu H, Shi J, Hao X, Hao P, Liu H, Sun F, Zhang J et al. (2024a) What foundation models can bring for robot learning in manipulation: A survey. _The International Journal of Robotics Research_ . 

- Li J, Gao Q, Johnston M, Gao X, He X, Shi H, Shakiah S, Ghanadan R and Wang WY (2024b) Mastering robot manipulation with multimodal prompts through pretraining and multi-task finetuning. In: _International Conference on Machine Learning_ . PMLR, pp. 27822–27845. 

- Li J, Selvaraju R, Gotmare A, Joty S, Xiong C and Hoi SCH (2021) Align before fuse: Vision and language representation learning with momentum distillation. _Advances in neural information processing systems_ 34: 9694–9705. 

- Li P, Chen Y, Wu H, Ma X, Wu X, Huang Y, Wang L, Kong T and Tan T (2026b) Bridgevla: Input-output alignment for efficient 3d manipulation learning with vision-language models. _Advances in Neural Information Processing Systems_ 38: 63635–63673. 

- Li P, Hao J, Tang H, Yuan Y, Qiao J, Dong Z and Zheng Y (2025a) R*: Efficient reward design via reward structure evolution and parameter alignment optimization with large language models. In: _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267. PMLR, pp. 34509–34527. 

- Li P, Wu H, Huang Y, Cheang C, Wang L and Kong T (2025b) Grmg: Leveraging partially-annotated data via multi-modal goalconditioned policy. _IEEE Robotics and Automation Letters_ 10(2): 1912–1919. 

- Li P, Wu Y, Xi Z, Li W, Huang Y, Zhang Z, Chen Y, Wang J, Zhu SC, Liu T and Huang S (2025c) Controlvla: Fewshot object-centric adaptation for pre-trained vision-languageaction models. In: _Proceedings of The 9th Conference on Robot Learning_ , _Proceedings of Machine Learning Research_ , volume 305. PMLR, pp. 1898–1913. 

- Li S, Gao L, Wang J, Che C, Xiao X, Cao J, Hu Y and Karimi HR (2026c) Information-theoretic graph fusion with visionlanguage-action model for policy reasoning and dual robotic control. _Information Fusion_ : 104193. 

- Li X, Li P, Qian L, Liu M, Wang D, Liu J, Kang B, Ma X, Wang X, Guo D et al. (2026d) What matters in building vision– language–action models for generalist robots. _Nature Machine Intelligence_ 8: 158–172. 

- Li X, Liu M, Zhang H, Yu C, Xu J, Wu H, Cheang C, Jing Y, Zhang W, Liu H et al. (2024c) Vision-language foundation models as effective robot imitators. In: _The Twelfth International Conference on Learning Representations_ . 

- Liang J, Huang W, Xia F, Xu P, Hausman K, Ichter B, Florence P and Zeng A (2023) Code as policies: Language model programs for embodied control. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 9493–9500. 

- Liang T, Glossner J, Wang L, Shi S and Zhang X (2021) Pruning and quantization for deep neural network acceleration: A survey. _Neurocomputing_ 461: 370–403. 

- Liang Z, Li Y, Yang T, Wu C, Mao S, Pei L, Yang X, Pang J, Mu Y and Luo P (2025) Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ . 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

61 

- Lin F, Hu Y, Sheng P, Wen C, You J and Gao Y (2025) Data scaling laws in imitation learning for robotic manipulation. In: _The Thirteenth International Conference on Learning Representations_ . 

- Lin K, Agia C, Migimatsu T, Pavone M and Bohg J (2023) Text2motion: From natural language instructions to feasible plans. _arXiv preprint arXiv:2303.12153_ . 

- Lin Y, Liu Z, Sun M, Liu Y and Zhu X (2015) Learning entity and relation embeddings for knowledge graph completion. _Proceedings of the AAAI Conference on Artificial Intelligence_ 29(1). 

- Ling Y, Owalekar K, Adesanya O, Biyik E and Seita D (2025) IMPACT: intelligent motion planning with acceptable contact trajectories via vision-language models. _CoRR_ abs/2503.10110. 

- Liu B, Zhu Y, Gao C, Feng Y, Liu Q, Zhu Y and Stone P (2023a) Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ 36: 44776–44791. 

- Liu H, Chen A, Zhu Y, Swaminathan A, Kolobov A and Cheng CA (2023b) Interactive robot learning from verbal correction. In: _The 2nd Workshop on Language and Robot Learning: Language as Grounding_ . 

- Liu J, Li C, Wang G, Lee L, Zhou K, Chen S, Xiong C, Ge J, Zhang R and Zhang S (2024) Self-corrected multimodal large language model for end-to-end robot manipulation. _arXiv e- prints_ : arXiv–2405. 

- Liu M, Zhu M and Zhang W (2022) Goal-conditioned reinforcement learning: Problems and solutions. _CoRR_ abs/2201.08299. 

- Liu R and Zhang X (2018) Generating machine-executable plans from end-user’s natural-language instructions. _KnowledgeBased Systems_ 140: 15–26. 

- Liu S, Wu L, Li B, Tan H, Chen H, Wang Z, Xu K, Su H and Zhu J (2025a) RDT-1b: a diffusion foundation model for bimanual manipulation. In: _The Thirteenth International Conference on Learning Representations_ . 

- Liu W, Du Y, Hermans T, Chernova S and Paxton C (2023c) Structdiffusion: Language-guided creation of physically-valid structures using unseen objects. _Robotics: Science and Systems_ 

- Liu W, Nie N, Zhang R, Mao J and Wu J (2025b) Learning compositional behaviors from demonstration and language. In: _2025 Conference on Robot Learning_ . PMLR, pp. 1992–2028. 

- Liu Y, Ott M, Goyal N, Du J, Joshi M, Chen D, Levy O, Lewis M, Zettlemoyer L and Stoyanov V (2019) Roberta: A robustly optimized bert pretraining approach. _arXiv preprint arXiv:1907.11692_ . 

- Liu Z, Bahety A and Song S (2023d) Reflect: Summarizing robot experiences for failure explanation and correction. In: _2023 Conference on Robot Learning_ . PMLR, pp. 3468–3484. 

- Louwerse MM and Jeuniaux P (2008) Language comprehension is both embodied and symbolic. _Symbols and embodiment: Debates on meaning and cognition_ : 309–326. 

- Lu G, Gao Z, Chen T, Dai W, Wang Z and Tang Y (2024) Manicm: Real-time 3d diffusion policy via consistency model for robotic manipulation. _arXiv preprint arXiv:2406.01586_ . 

- Lu J, Batra D, Parikh D and Lee S (2019) Vilbert: Pretraining task-agnostic visiolinguistic representations for vision-andlanguage tasks. _Advances in neural information processing systems_ 32. 

- Lu J, Xia W, Wang D, Wang Z, Zhao B, Hu D and Li X (2025a) Koi: Accelerating online imitation learning via hybrid keystate guidance. In: _Conference on Robot Learning_ . PMLR, pp. 3847–3865. 

- Lu S, H¨ardtlein C and Schilp J (2025b) Visual imitation learning from one-shot demonstration for multi-step robot pick and place tasks. _Scientific Reports_ 15: 43265. 

- Lu Y, Feng W, Zhu W, Xu W, Wang XE, Eckstein M and Wang WY (2022) Neuro-symbolic procedural planning with commonsense prompting. _arXiv preprint arXiv:2206.02928_ . 

- Lynch C, Khansari M, Xiao T, Kumar V, Tompson J, Levine S and Sermanet P (2020) Learning latent plans from play. In: _Conference on robot learning_ . PMLR, pp. 1113–1132. 

- Lynch C and Sermanet P (2021) Language conditioned imitation learning over unstructured data. In: Shell DA, Toussaint M and Hsieh MA (eds.) _Robotics: Science and Systems XVII_ . 

- Lynch C, Wahid A, Tompson J, Ding T, Betker J, Baruch R, Armstrong T and Florence P (2023) Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ : 1–8. 

- Ma T, Zhou J, Wang Z, Qiu R and Liang J (2025) Contrastive imitation learning for language-guided multi-task robotic manipulation. _Conference on Robot Learning_ : 4651–4669. 

- Ma YJ, Liang W, Wang G, Huang DA, Bastani O, Jayaraman D, Zhu Y, Fan L and Anandkumar A (2024) Eureka: Humanlevel reward design via coding large language models. In: _The Twelfth International Conference on Learning Representations_ . 

- MacGlashan J, Babes-Vroman M, desJardins M, Littman ML, Muresan S, Squire S, Tellex S, Arumugam D and Yang L (2015) Grounding english commands to reward functions. In: _Robotics: Science and Systems_ . 

- Mahmoudieh P, Pathak D and Darrell T (2022) Zero-shot reward specification via grounded natural language. _International Conference on Machine Learning_ : 14743–14752. 

- Mallya A and Lazebnik S (2018) Packnet: Adding multiple tasks to a single network by iterative pruning. In: _Proceedings of the IEEE conference on Computer Vision and Pattern Recognition_ . pp. 7765–7773. 

- Mandlekar A, Xu D, Wong J, Nasiriany S, Wang C, Kulkarni R, Fei-Fei L, Savarese S, Zhu Y and Mart´ın-Mart´ın R (2022) What matters in learning from offline human demonstrations for robot manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 1678–1690. 

- Mandlekar A, Zhu Y, Garg A, Booher J, Spero M, Tung A, Gao J, Emmons J, Gupta A, Orbay E et al. (2018) Roboturk: A crowdsourcing platform for robotic skill learning through imitation. In: _Conference on Robot Learning_ . PMLR, pp. 879– 893. 

- Matuszek C, Cabral J, Witbrock M and DeOliveira J (2006) An introduction to the syntax and content of cyc. In: _AAAI Spring Symposium: Formalizing and Compiling Background Knowledge and Its Applications to Knowledge Representation and Question Answering_ . AAAI, pp. 44–49. 

- McCarthy R, Tan DC, Schmidt D, Acero F, Herr N, Du Y, Thuruthel TG and Li Z (2025) Towards generalist robot learning from internet video: A survey. _Journal of Artificial Intelligence Research_ 83. 

- Mees O, Abdo N, Mazuran M and Burgard W (2017) Metric learning for generalizing spatial relations to new objects. In: _2017 IEEE/RSJ International Conference on Intelligent Robots_ 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

62 

_and Systems (IROS)_ . IEEE, pp. 3175–3182. 

- Mees O, Borja-Diaz J and Burgard W (2023) Grounding language with visual affordances over unstructured data. In: _ICRA_ . IEEE, pp. 11576–11582. 

- Mees O and Burgard W (2021) Composing pick-and-place tasks by grounding language. In: _Experimental Robotics: The 17th International Symposium_ . Springer, pp. 491–501. 

- Mees O, Eitel A and Burgard W (2016) Choosing smartly: Adaptive multimodal fusion for object detection in changing environments. In: _2016 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, pp. 151–156. 

- Mees O, Emek A, Vertens J and Burgard W (2020) Learning object placements for relational instructions by hallucinating scene representations. In: _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 94–100. 

- Mees O, Hermann L and Burgard W (2022a) What matters in language conditioned robotic imitation learning over unstructured data. _IEEE Robotics and Automation Letters_ 7(4): 11205–11212. 

- Mees O, Hermann L, Rosete-Beas E and Burgard W (2022b) Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ 7(3): 7327–7334. 

- Mees O, Tatarchenko M, Brox T and Burgard W (2019) Selfsupervised 3d shape and viewpoint estimation from single images for robotics. In: _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 6083–6089. 

- Meng Y, Bing Z, Yao X, Chen K, Huang K, Gao Y, Sun F and Knoll A (2025a) Preserving and combining knowledge in robotic lifelong reinforcement learning. _Nature Machine Intelligence_ : 1–14. 

- Meng Y, Sun Z, Fest M, Li X, Bing Z and Knoll A (2025b) Growing with your embodied agent: A human-in-the-loop lifelong code generation framework for long-horizon manipulation skills. _arXiv preprint arXiv:2509.18597_ . 

- Meng Y, Yao X, Ye H, Zhou Y, Zhang S, Bing Z and Knoll A (2025c) Data-agnostic robotic long-horizon manipulation with vision-language-guided closed-loop feedback. _arXiv preprint arXiv:2503.21969_ . 

- Mialon G, Dess`ı R, Lomeli M, Nalmpantis C, Pasunuru R, Raileanu R, Rozi`ere B, Schick T, Dwivedi-Yu J, Celikyilmaz A et al. (2023) Augmented language models: a survey. _arXiv preprint arXiv:2302.07842_ . 

- Miao R, Jia Q and Sun F (2023) Long-term robot manipulation task planning with scene graph and semantic knowledge. _Robotic Intelligence and Automation_ 43(1): 12–22. 

- Miao R, Jia Q, Sun F, Chen G and Huang H (2024) Hierarchical understanding in robotic manipulation: A knowledge-based framework. _Actuators_ 13(1). 

- Mikolov T, Chen K, Corrado G and Dean J (2013a) Efficient estimation of word representations in vector space. _arXiv preprint arXiv:1301.3781_ . 

- Mikolov T, Karafi´at M, Burget L, Cernock`y J and Khudanpur S (2010) Recurrent neural network based language model. _Interspeech_ 2(3): 1045–1048. 

- Mikolov T, Sutskever I, Chen K, Corrado GS and Dean J (2013b) Distributed representations of words and phrases and their compositionality. _Advances in neural information processing systems_ 26. 

- Minderer M, Gritsenko A, Stone A, Neumann M, Weissenborn D, Dosovitskiy A, Mahendran A, Arnab A, Dehghani M, Shen Z et al. (2022) Simple open-vocabulary object detection. In: _European conference on computer vision_ . Springer, pp. 728– 755. 

- Ming C, Lin J, Fong P, Wang H, Duan X and He J (2024) Hicrisp: An llm-based hierarchical closed-loop robotic intelligent selfcorrection planner. In: _2024 China Automation Congress (CAC)_ . IEEE, pp. 4310–4315. 

- Mishra UA, Xue S, Chen Y and Xu D (2023) Generative skill chaining: Long-horizon skill planning with diffusion models. In: _Conference on Robot Learning_ . PMLR, pp. 2905–2925. 

- Misra D, Langford J and Artzi Y (2017) Mapping instructions and visual observations to actions with reinforcement learning. In: _Proceedings of the 2017 conference on empirical methods in natural language processing_ . pp. 1004–1015. 

- Misra DK, Sung J, Lee K and Saxena A (2016) Tell me dave: Context-sensitive grounding of natural language to manipulation instructions. _The International Journal of Robotics Research_ 35(1-3): 281–300. 

- Mo K, Guibas LJ, Mukadam M, Gupta A and Tulsiani S (2021) Where2act: From pixels to actions for articulated 3d objects. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ . pp. 6813–6823. 

- Mon-Williams R, Li G, Long R, Du W and Lucas CG (2025) Embodied large language models enable robots to complete complex tasks in unpredictable environments. _Nature Machine Intelligence_ : 1–10. 

- Mu Y, Chen J, Zhang QL, Chen S, Yu Q, Ge C, Chen R, Liang Z, Hu M, Tao C et al. (2024) Robocodex: Multimodal code generation for robotic behavior synthesis. In: _International Conference on Machine Learning_ . PMLR, pp. 36434–36454. 

- Mu Y, Zhang Q, Hu M, Wang W, Ding M, Jin J, Wang B, Dai J, Qiao Y and Luo P (2023) Embodiedgpt: Vision-language pretraining via embodied chain of thought. _Advances in Neural Information Processing Systems_ 36: 25081–25094. 

- Munawar A, De Magistris G, Pham TH, Kimura D, Tatsubori M, Moriyama T, Tachibana R and Booch G (2018) Maestrob: A robotics framework for integrated orchestration of low-level control and high-level reasoning. In: _2018 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 527–534. 

- Nair A, Bahl S, Khazatsky A, Pong V, Berseth G and Levine S (2020) Contextual imagined goals for self-supervised robotic learning. In: _Conference on Robot Learning_ . PMLR, pp. 530– 539. 

- Nair S, Mitchell E, Chen K, Savarese S, Finn C et al. (2022) Learning language-conditioned robot behavior from offline data and crowd-sourced annotation. In: _Conference on Robot Learning_ . PMLR, pp. 1303–1315. 

- Nair S, Rajeswaran A, Kumar V, Finn C and Gupta A (2023) R3m: A universal visual representation for robot manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 892–909. 

- Nakamoto M, Mees O, Kumar A and Levine S (2025) Steering your generalists: Improving robotic foundation models via value guidance. In: _Conference on Robot Learning_ . PMLR, pp. 4996–5013. 

- Nasiriany S, Xia F, Yu W, Xiao T, Liang J, Dasgupta I, Xie A, Driess D, Wahid A, Xu Z et al. (2024) Pivot: iterative visual prompting elicits actionable knowledge for vlms. In: _2024 Proceedings of_ 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

63 

   - _the 41st International Conference on Machine Learning_ . pp. 37321–37341. 

- Nathani D, Chauhan J, Sharma C and Kaul M (2019) Learning attention-based embeddings for relation prediction in knowledge graphs. In: _Proceedings of the 57th annual meeting of the association for computational linguistics_ . pp. 4710–4723. 

- Naveed H, Khan AU, Qiu S, Saqib M, Anwar S, Usman M, Akhtar N, Barnes N and Mian A (2025) A comprehensive overview of large language models. _ACM Transactions on Intelligent Systems and Technology_ 16(5): 1–72. 

- Nematollahi I, Mees O, Hermann L and Burgard W (2020) Hindsight for foresight: Unsupervised structured dynamics models from physical interaction. In: _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 5319–5326. 

- Ng AY, Harada D and Russell S (1999) Policy invariance under reward transformations: Theory and application to reward shaping. In: _Icml_ , volume 99. Citeseer, pp. 278–287. 

- Ng E, Liu Z and Kennedy M (2023) Diffusion co-policy for synergistic human-robot collaborative tasks. _IEEE Robotics and Automation Letters_ . 

- Nguyen TL, Nguyen DV and Le TH (2019) Reinforcement learning based navigation with semantic knowledge of indoor environments. In: _2019 11th International Conference on Knowledge and Systems Engineering (KSE)_ . IEEE, pp. 1–7. 

- Ocana JMC, Capobianco R and Nardi D (2023) An overview of environmental features that impact deep reinforcement learning in sparse-reward domains. _Journal of Artificial Intelligence Research_ 76: 1181–1218. 

- Octo Model Team, Ghosh D, Walke H, Pertsch K, Black K, Mees O et al. (2024) Octo: An open-source generalist robot policy. In: _Proceedings of Robotics: Science and Systems_ . Delft, Netherlands. 

- O’Neill A et al. (2024) Open x-embodiment: Robotic learning datasets and RT-X models : Open x-embodiment collaboration. In: _ICRA_ . IEEE, pp. 6892–6903. 

- Oquab M, Darcet T, Moutakanni T, Vo HV, Szafraniec M et al. (2024) DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research_ . 

- Ouyang L, Wu J, Jiang X, Almeida D, Wainwright C et al. (2022) Training language models to follow instructions with human feedback. _Advances in Neural Information Processing Systems_ 35: 27730–27744. 

- Pang JC, Yang XY, Yang SH and Yu Y (2023) Natural language-conditioned reinforcement learning with inside-out task language development and translation. _arXiv preprint arXiv:2302.09368_ . 

- Papagiannis G, Di Palo N, Vitiello P and Johns E (2025) R+ x: Retrieval and execution from everyday human videos. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 8284–8290. 

- Parimi V and Williams BC (2025) Diffusion-guided multi-arm motion planning. In: _Conference on Robot Learning_ . PMLR, pp. 4684–4696. 

- Parisotto E, Song F, Rae J, Pascanu R, Gulcehre C, Jayakumar S, Jaderberg M, Kaufman RL, Clark A, Noury S et al. (2020) Stabilizing transformers for reinforcement learning. In: _International conference on machine learning_ . PMLR, pp. 7487–7498. 

- Park JS, Jia B, Bansal M and Manocha D (2019) Efficient generation of motion plans from attribute-based natural language instructions using dynamic constraint mapping. In: _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6964–6971. 

- Patel D, Eghbalzadeh H, Kamra N, Iuzzolino ML, Jain U and Desai R (2023) Pretrained language models as visual planners for human assistance. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 15302– 15314. 

- Patki S, Daniele AF, Walter MR and Howard TM (2019) Inferring compact representations for efficient natural language understanding of robot instructions. In: _2019 International Conference on Robotics and Automation (ICRA)_ . pp. 6926– 6933. 

- Paulius D, Agostini A, Quartey B and Konidaris G (2025) Bootstrapping object-level planning with large language models. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 16233–16239. 

- Paxton C, Bisk Y, Thomason J, Byravan A and Foxl D (2019) Prospection: Interpretable plans from language by predicting the future. In: _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6942–6948. 

- Pearce T, Rashid T, Kanervisto A, Bignell D, Sun M et al. (2022) Imitating human behaviour with diffusion models. In: _The Eleventh International Conference on Learning Representations_ . 

- Pennington J, Socher R and Manning CD (2014) Glove: Global vectors for word representation. In: _Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP)_ . pp. 1532–1543. 

- Pertsch K, Stachowicz K, Ichter B, Driess D, Nair S, Vuong Q, Mees O, Finn C and Levine S (2025) Fast: Efficient action tokenization for vision-language-action models. In: _Proceedings of Robotics: Science and Systems_ . 

- Peters ME, Neumann M, Iyyer M, Gardner M, Clark C, Lee K and Zettlemoyer L (2018) Deep contextualized word representations. In: _Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers)_ . pp. 2227–2237. 

- Prasad A, Lin K, Wu J, Zhou L and Bohg J (2024) Consistency policy: Accelerated visuomotor policies via consistency distillation. In: _Robotics: Science and Systems_ . 

- Qu D, Song H, Chen Q, Yao Y, Ye X, Ding Y, Wang Z, Gu J, Zhao B, Wang D et al. (2025) Spatialvla: Exploring spatial representations for visual-language-action model. _Robotics: Science and Systems_ . 

- Radford A, Kim JW, Hallacy C, Ramesh A, Goh G, Agarwal S, Sastry G, Askell A, Mishkin P, Clark J et al. (2021) Learning transferable visual models from natural language supervision. In: _International conference on machine learning_ . PMLR, pp. 8748–8763. 

- Radford A, Wu J, Child R, Luan D, Amodei D, Sutskever I et al. (2019) Language models are unsupervised multitask learners. _OpenAI blog_ 1(8): 9. 

- Rahmatizadeh R, Abolghasemi P, B¨ol¨oni L and Levine S (2018) Vision-based multi-task manipulation for inexpensive robots using end-to-end learning from demonstration. In: _2018 IEEE international conference on robotics and automation (ICRA)_ . 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

64 

IEEE, pp. 3758–3765. 

- Raman V, Finucane C and Kress-Gazit H (2012) Temporal logic robot mission planning for slow and fast actions. In: _2012 IEEE/RSJ International Conference on Intelligent Robots and Systems_ . IEEE, pp. 251–256. 

- Ramesh A, Dhariwal P, Nichol A, Chu C and Chen M (2022) Hierarchical text-conditional image generation with clip latents. _arXiv preprint arXiv:2204.06125_ . 

- Rana K, Haviland J, Garg S, Abou-Chakra J, Reid I and Suenderhauf N (2023) Sayplan: Grounding large language models using 3d scene graphs for scalable robot task planning. In: _7th Annual Conference on Robot Learning_ . 

- Rasch R, Sprute D, P¨ortner A, Battermann S and K¨onig M (2019) Tidy up my room: Multi-agent cooperation for service tasks in smart environments. _Journal of Ambient Intelligence and Smart Environments_ 11(3): 261–275. 

- Redmon J, Divvala S, Girshick R and Farhadi A (2016) You only look once: Unified, real-time object detection. In: _Proceedings of the IEEE conference on computer vision and pattern recognition_ . pp. 779–788. 

- Reed S, Zolna K, Parisotto E, Colmenarejo SG, Novikov A et al. (2022) A generalist agent. _Transactions on Machine Learning Research_ Featured Certification, Outstanding Certification. 

- Ren AZ, Dixit A, Bodrova A, Singh S, Tu S, Brown N, Xu P, Takayama L, Xia F, Varley J et al. (2023a) Robots that ask for help: Uncertainty alignment for large language model planners. In: _Conference on Robot Learning_ . PMLR, pp. 661–682. 

- Ren AZ, Govil B, Yang TY, Narasimhan KR and Majumdar A (2023b) Leveraging language for accelerated learning of tool manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 1531–1541. 

- Reuss M, Li M, Jia X and Lioutikov R (2023) Goalconditioned imitation learning using score-based diffusion policies. _Robotics: Science and Systems_ . 

- Reuss M, Ya˘gmurlu ¨OE, Wenzel F and Lioutikov R (2024) Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. In: _Robotics: Science and Systems_ . 

- Riedmiller M, Hafner R, Lampe T, Neunert M, Degrave J, Wiele T, Mnih V, Heess N and Springenberg JT (2018) Learning by playing solving sparse reward tasks from scratch. In: _International conference on machine learning_ . PMLR, pp. 4344–4353. 

- Roh J, Paxton C, Pronobis A, Farhadi A and Fox D (2020) Conditional driving from natural language instructions. In: _Conference on Robot Learning_ . PMLR, pp. 540–551. 

- Rohmer E, Singh SP and Freese M (2013) V-rep: A versatile and scalable robot simulation framework. In: _2013 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, pp. 1321–1326. 

- Rombach R, Blattmann A, Lorenz D, Esser P and Ommer B (2022) High-resolution image synthesis with latent diffusion models. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 10684–10695. 

- Rosete-Beas E, Mees O, Kalweit G, Boedecker J and Burgard W (2022) Latent plans for task-agnostic offline reinforcement learning. In: _CoRL_ , _Proceedings of Machine Learning Research_ , volume 205. PMLR, pp. 1838–1849. 

- Saharia C, Chan W, Saxena S, Li L, Whang J, Denton EL, Ghasemipour K, Gontijo Lopes R, Karagol Ayan B, Salimans T et al. (2022) Photorealistic text-to-image diffusion models with 

deep language understanding. _Advances in neural information processing systems_ 35: 36479–36494. 

- Sanchez J, Corrales JA, Bouzgarrou BC and Mezouar Y (2018) Robotic manipulation and sensing of deformable objects in domestic and industrial applications: a survey. _The International Journal of Robotics Research_ 37(7): 688–716. 

- Sanh V, Debut L, Chaumond J and Wolf T (2019) Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter. In: _Proceedings of Thirty-third Conference on Neural Information Processing Systems (NIPS2019)_ . 

- Schaldenbrand P, McCann J and Oh J (2023) Frida: A collaborative robot painter with a differentiable, real2sim2real planning environment. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 11712–11718. 

- Schaldenbrand P, Parmar G, Zhu JY, McCann J and Oh J (2024) Cofrida: Self-supervised fine-tuning for human-robot co-painting. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 2296–2302. 

- Scheikl PM, Schreiber N, Haas C, Freymuth N, Neumann G, Lioutikov R and Mathis-Ullrich F (2024) Movement primitive diffusion: Learning gentle robotic manipulation of deformable objects. _IEEE Robotics and Automation Letters_ . 

- Schlichtkrull M, Kipf TN, Bloem P, Van Den Berg R, Titov I and Welling M (2018) Modeling relational data with graph convolutional networks. In: _European semantic web conference_ . Springer, pp. 593–607. 

- Shafiullah NM, Cui Z, Altanzaya AA and Pinto L (2022) Behavior transformers: Cloning _k_ modes with one stone. _Advances in neural information processing systems_ 35: 22955–22968. 

- Shafiullah NMM, Paxton C, Pinto L, Chintala S and Szlam A (2023) Clip-fields: Weakly supervised semantic fields for robotic memory. In: _Robotics: Science and Systems_ . 

- Shao L, Migimatsu T, Zhang Q, Yang K and Bohg J (2021) Concept2robot: Learning manipulation concepts from instructions and human demonstrations. _The International Journal of Robotics Research_ 40(12-14): 1419–1434. 

- Sharma P, Sundaralingam B, Blukis V, Paxton C, Hermans T, Torralba A, Andreas J and Fox D (2022) Correcting robot plans with natural language feedback. _arXiv preprint arXiv:2204.05186_ . 

- She L and Chai J (2016) Incremental acquisition of verb hypothesis space towards physical world interaction. In: _Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . pp. 108–117. 

- She L and Chai J (2017) Interactive learning of grounded verb semantics towards human-robot communication. In: _Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . pp. 1634– 1644. 

- She L, Cheng Y, Chai JY, Jia Y, Yang S and Xi N (2014) Teaching robots new actions through natural language instructions. In: _The 23rd IEEE International Symposium on Robot and Human Interactive Communication_ . IEEE, pp. 868–873. 

- Shi H, Xie B, Liu Y, Sun L, Liu F, Wang T, Zhou E, Fan H, Zhang X and Huang G (2026) MemoryVLA: Perceptualcognitive memory in vision-language-action models for robotic manipulation. In: _The Fourteenth International Conference on Learning Representations_ . URL https://openreview. net/forum?id=54U3XHf7qq. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

65 

- Shi LX, Hu Z, Zhao TZ, Sharma A, Pertsch K, Luo J, Levine S and Finn C (2024) Yell at your robot: Improving on-the-fly from language corrections. _Robotics: Science and Systems_ . 

- Shridhar M, Manuelli L and Fox D (2022) Cliport: What and where pathways for robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 894–906. 

- Shridhar M, Manuelli L and Fox D (2023) Perceiver-actor: A multitask transformer for robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 785–799. 

- Shridhar M, Thomason J, Gordon D, Bisk Y, Han W, Mottaghi R, Zettlemoyer L and Fox D (2020) Alfred: A benchmark for interpreting grounded instructions for everyday tasks. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 10740–10749. 

- Silva A, Moorman N, Silva W, Zaidi Z, Gopalan N and Gombolay M (2021) Lancon-learn: Learning with language to enable generalization in multi-task manipulation. _IEEE Robotics and Automation Letters_ 7(2): 1635–1642. 

- Silver T, Athalye A, Tenenbaum JB, Lozano-P´erez T and Kaelbling LP (2023) Learning neuro-symbolic skills for bilevel planning. In: _Conference on Robot Learning_ . PMLR, pp. 701–714. 

- Silvera-Tawil D (2024) Robotics in healthcare: a survey. _SN Computer Science_ 5(1): 189. 

- Singer U, Polyak A, Hayes T, Yin X, An J, Zhang S, Hu Q, Yang H, Ashual O, Gafni O, Parikh D, Gupta S and Taigman Y (2023) Make-a-video: Text-to-video generation without textvideo data. _The Eleventh International Conference on Learning Representations_ . 

- Singh CK, Kumar D, Sanap V and Sinha R (2025) Llm-rspf: Large language model-based robotic system planning framework for domain specific use-cases. In: _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ . IEEE, pp. 7277–7286. 

- Singh I, Blukis V, Mousavian A, Goyal A, Xu D, Tremblay J, Fox D, Thomason J and Garg A (2023) ProgPrompt: Program generation for situated robot task planning using large language models. _Autonomous Robots (AURO)_ . 

- Sodhani S, Zhang A and Pineau J (2021) Multi-task reinforcement learning with context-based representations. In: Meila M and Zhang T (eds.) _Proceedings of the 38th International Conference on Machine Learning_ , _Proceedings of Machine Learning Research_ , volume 139. PMLR, pp. 9767–9779. 

- Speer R, Chin J and Havasi C (2017) Conceptnet 5.5: An open multilingual graph of general knowledge. _the Thirty-First AAAI Conference on Artificial Intelligence_ : 4444–4451. 

- Sriram N, Maniar T, Kalyanasundaram J, Gandhi V, Bhowmick B and Krishna KM (2019) Talk to the vehicle: Language conditioned autonomous navigation of self driving cars. In: _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 5284–5290. 

- Srivastava A, Valkov L, Russell C, Gutmann MU and Sutton C (2017) Veegan: Reducing mode collapse in gans using implicit variational learning. _Advances in neural information processing systems_ 30. 

- Stepputtis S, Campbell J, Phielipp M, Lee S, Baral C and Ben Amor H (2020) Language-conditioned imitation learning for robot manipulation tasks. _Advances in Neural Information Processing Systems_ 33: 13139–13150. 

- Stone A, Xiao T, Lu Y, Gopalakrishnan K, Lee KH, Vuong Q, Wohlhart P, Kirmani S, Zitkovich B, Xia F et al. (2023) Openworld object manipulation using pre-trained vision-language models. _Conference on Robot Learning_ : 3397–3417. 

- Styrud J, Iovino M, Norrl¨of M, Bj¨orkman M and Smith C (2025) Automatic behavior tree expansion with llms for robotic manipulation. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 1225–1232. 

- Sun L, Xie B, Liu Y, Shi H, Wang T and Cao J (2025) Geovla: Empowering 3d representations in vision-languageaction models. _arXiv preprint arXiv:2508.09071_ . 

- Sundaresan P, Belkhale S, Sadigh D and Bohg J (2023) KITE: keypoint-conditioned policies for semantic manipulation. In: _CoRL_ , _Proceedings of Machine Learning Research_ , volume 229. PMLR, pp. 1006–1021. 

- Sundermeyer M, Mousavian A, Triebel R and Fox D (2021) Contact-graspnet: Efficient 6-dof grasp generation in cluttered scenes. In: _ICRA_ . IEEE, pp. 13438–13444. 

- Sutton C, McCallum A et al. (2012) An introduction to conditional random fields. _Foundations and Trends® in Machine Learning_ 4(4): 267–373. 

- Sutton R and Barto A (1998) Reinforcement learning: An introduction. _IEEE Transactions on Neural Networks_ 9(5): 1054–1054. 

- Sutton RS, Barto AG et al. (1998) _Introduction to reinforcement learning_ , volume 135. MIT press Cambridge. 

- Takeshita K, Yamazaki T, Ono T and Yamamoto T (2025) Robot local planner: A periodic sampling-based motion planner with minimal waypoints for home environments. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 10772–10778. 

- Tamosiunaite M, Aein MJ, Braun JM et al. (2019) Cut & recombine: reuse of robot action components based on simple language instructions. _The International Journal of Robotics Research_ 38(10-11): 1179–1207. 

- Tan S, Dou K, Zhao Y and Kraehenbuehl P (2025) Interactive posttraining for vision-language-action models. In: _Workshop on Foundation Models Meet Embodied Agents at CVPR 2025_ . 

- Tan W, Liu B, Zhang J, Song R and Fu J (2024) Rold: Robot latent diffusion for multi-task policy modeling. _International Conference on Multimedia Modeling_ : 340–353. 

- Tang J, Cheng B and Wen M (2025) Hierarchical languageconditioned robot learning with vision-language models. In: _Intelligent Robotics: 5th China Annual Conference, CIRAC 2024, Dalian, China, September 20–22, 2024, Proceedings_ , volume 2355. Springer Nature, p. 167. 

- Taori R, Gulrajani I, Zhang T, Dubois Y, Li X, Guestrin C, Liang P and Hashimoto TB (2023) Alpaca: A strong, replicable instruction-following model. _Stanford Center for Research on Foundation Models._ 3(6): 7. 

- Tarakli I, Vinanzi S and Nuovo AD (2024) Interactive reinforcement learning from natural language feedback. In: _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . pp. 11478–11484. 

- Team G, Anil R, Borgeaud S, Alayrac JB, Yu J, Soricut R, Schalkwyk J, Dai AM, Hauth A, Millican K et al. (2023) Gemini: a family of highly capable multimodal models. _arXiv preprint arXiv:2312.11805_ . 

- Team GR, Abeyruwan S, Ainslie J, Alayrac JB, Arenas MG, Armstrong T, Balakrishna A, Baruch R, Bauza M, Blokzijl 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

66 

M et al. (2025) Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ . 

- Tellex S, Gopalan N, Kress-Gazit H and Matuszek C (2020) Robots that use language. _Annual Review of Control, Robotics, and Autonomous Systems_ 3(1): 25–55. 

- Tenorth M, Nyga D and Beetz M (2010) Understanding and executing instructions for everyday manipulation tasks from the world wide web. In: _2010 ieee international conference on robotics and automation_ . IEEE, pp. 1486–1491. 

- Thomason J, Padmakumar A, Sinapov J, Walker N, Jiang Y, Yedidsion H, Hart J, Stone P and Mooney RJ (2019) Improving grounded natural language understanding through human-robot dialog. In: _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6934–6941. 

- Tian Y, Yang S, Zeng J, Wang P, Lin D, Dong H and Pang J (2025) Predictive inverse dynamics models are scalable learners for robotic manipulation. In: _The Thirteenth International Conference on Learning Representations_ . 

- Todorov E, Erez T and Tassa Y (2012) Mujoco: A physics engine for model-based control. In: _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, pp. 5026– 5033. 

- Torabi F, Warnell G and Stone P (2018) Behavioral cloning from observation. In: _Proceedings of the 27th International Joint Conference on Artificial Intelligence_ . pp. 4950–4957. 

- Torne M, Pertsch K, Walke H, Vedder K, Nair S, Ichter B, Ren AZ, Wang H, Tang J, Stachowicz K et al. (2026) Mem: Multi-scale embodied memory for vision language action models. _arXiv preprint arXiv:2603.03596_ . 

- Torne M, Simeonov A, Li Z, Chan A, Chen T, Gupta A and Agrawal P (2024) Reconciling reality through simulation: A real-to-simto-real approach for robust manipulation. _CoRR_ . 

- Touvron H, Martin L, Stone K, Albert P, Almahairi A, Babaei Y, Bashlykov N, Batra S, Bhargava P, Bhosale S et al. (2023) Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ . 

- Tripathi D, Liu C, Pudasaini N, Hao Y, Tzes A and Fang Y (2025) Lav-act: Language-augmented visual action chunking with transformers for bimanual robotic manipulation. In: _2025 11th International Conference on Automation, Robotics, and Applications (ICARA)_ . pp. 18–22. 

- Tsuji T (2025) Mamba as a motion encoder for robotic imitation learning. _IEEE Access_ 13: 69941–69949. 

- Tu Y, Wang Y, Zhang H, Chen W and Zhang J (2025) Languageembedded 6d pose estimation for tool manipulation. _IEEE Robotics and Automation Letters_ 10(9): 8618–8625. 

- Turcato N, Iovino M, Synodinos A, Dalla Libera A, Carli R and Falco P (2025) Towards autonomous reinforcement learning for real-world robotic manipulation with large language models. _IEEE Robotics and Automation Letters_ 10(9): 8850– 8857. 

- Urain J, Mandlekar A, Du Y, Shafiullah M, Xu D, Fragkiadaki K, Chalvatzaki G and Peters J (2024) Deep generative models in robotics: A survey on learning from multimodal demonstrations. _arXiv preprint arXiv:2408.04380_ . 

- Vallati M, Chrpa L, Grze´s M, McCluskey TL, Roberts M, Sanner S et al. (2015) The 2014 international planning competition: Progress and trends. _Ai Magazine_ 36(3): 90–98. 

- Vaswani A, Shazeer N, Parmar N, Uszkoreit J, Jones L, Gomez AN, Kaiser Ł and Polosukhin I (2017) Attention is all you need. 

_Advances in neural information processing systems_ 30. 

- Vosylius V, Seo Y, Uruc¸ J and James S (2024) Render and diffuse: Aligning image and action spaces for diffusion-based behaviour cloning. In: _Robotics: Science and Systems_ . 

- Wagenmaker A, Zhang Y, Nakamoto M, Park S, Yagoub W, Nagabandi A, Gupta A and Levine S (2025) Steering your diffusion policy with latent space reinforcement learning. In: _Conference on Robot Learning_ . PMLR, pp. 258–282. 

- Waibel M, Beetz M, Civera J, D’Andrea R, Elfring J, G´alvez-L´opez D, H¨aussermann K, Janssen R, Montiel J, Perzylo A, Schießle B, Tenorth M, Zweigle O and Molengraft M (2011) Roboearth - a world wide web for robots. _Robotics and Automation Magazine, IEEE_ 18: 69 – 82. 

- Wake N, Kanehira A, Sasabuchi K, Takamatsu J and Ikeuchi K (2024) Gpt-4v(ision) for robotics: Multimodal task planning from human demonstration. _IEEE Robotics and Automation Letters_ 9(11): 10567–10574. 

- Wang C, Fan L, Sun J, Zhang R, Fei-Fei L, Xu D, Zhu Y and Anandkumar A (2023a) Mimicplay: Long-horizon imitation learning by watching human play. _Conference on Robot Learning_ : 201–221. 

- Wang F, Lyu S, Zhou P, Duan A, Guo G and Navarro-Alarcon D (2025a) Instruction-augmented long-horizon planning: Embedding grounding mechanisms in embodied mobile manipulation. _Proceedings of the AAAI Conference on Artificial Intelligence_ 39(14): 14690–14698. 

- Wang G, Xie Y, Jiang Y, Mandlekar A, Xiao C, Zhu Y, Fan L and Anandkumar A (2024a) Voyager: An open-ended embodied agent with large language models. _Transactions on Machine Learning Research_ . 

- Wang H, Qi L and Sun Y (2025b) Integrating failures in robot skill acquisition with offline action-sequence diffusion rl. In: _ICASSP 2025 - 2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ . pp. 1–5. 

- Wang J, Dasari S, Srirama MK, Tulsiani S and Gupta A (2023b) Manipulate by seeing: Creating manipulation controllers from pre-trained representations. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 3859–3868. 

- Wang K, Zhao Y, He Y, Dai S, Zhang N and Yang M (2025c) Guiding reinforcement learning with shaping rewards provided by the vision–language model. _Engineering Applications of Artificial Intelligence_ 155: 111004. 

- Wang L, Chen X, Zhao J and He K (2024b) Scaling proprioceptivevisual learning with heterogeneous pre-trained transformers. _Advances in neural information processing systems_ 37: 124420–124450. 

- Wang L, Zhao J, Du Y, Adelson EH and Tedrake R (2024c) Poco: Policy composition from and for heterogeneous robot learning. _Robotics: Science and Systems_ . 

- Wang P, Yang A, Men R, Lin J, Bai S, Li Z, Ma J, Zhou C, Zhou J and Yang H (2022) Ofa: Unifying architectures, tasks, and modalities through a simple sequence-to-sequence learning framework. In: _International Conference on Machine Learning_ . PMLR, pp. 23318–23340. 

- Wang W, Li R, Chen Y, Diekel ZM and Jia Y (2018) Facilitating human–robot collaborative tasks by teachinglearning-collaboration from human demonstrations. _IEEE Transactions on Automation Science and Engineering_ 16(2): 640–653. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

67 

- Wang Y, Wang L, Du Y, Sundaralingam B, Yang X, Chao YW, P´erez-D’Arpino C, Fox D and Shah J (2025d) Inference-time policy steering through human interactions. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 15626–15633. 

- Wang Y, Xian Z, Chen F, Wang TH, Wang Y, Fragkiadaki K, Erickson Z, Held D and Gan C (2024d) Robogen: Towards unleashing infinite data for automated robot learning via generative simulation. In: _2024 International Conference on Machine Learning_ . PMLR, pp. 51936–51983. 

- Wang Z, Cai S, Chen G, Liu A, Ma X, Liang Y and CraftJarvis T (2023c) Describe, explain, plan and select: interactive planning with large language models enables open-world multi-task agents. In: _Proceedings of the 37th International Conference on Neural Information Processing Systems_ . pp. 34153–34189. 

- Wang Z, Zhang J, Feng J and Chen Z (2014) Knowledge graph embedding by translating on hyperplanes. _Proceedings of the AAAI Conference on Artificial Intelligence_ 28(1). 

- Wei J, Wang X, Schuurmans D, Bosma M, Xia F, Chi E, Le QV, Zhou D et al. (2022) Chain-of-thought prompting elicits reasoning in large language models. _Advances in Neural Information Processing Systems_ 35: 24824–24837. 

- Welling M and Teh YW (2011) Bayesian learning via stochastic gradient langevin dynamics. In: _Proceedings of the 28th international conference on machine learning (ICML-11)_ . pp. 681–688. 

- Wen J, Zhu Y, Li J, Tang Z, Shen C and Feng F (2025a) Dexvla: Vision-language model with plug-in diffusion expert for general robot control. In: _Conference on Robot Learning_ . PMLR, pp. 3094–3114. 

- Wen J, Zhu Y, Li J, Zhu M, Tang Z et al. (2025b) Tinyvla: Toward fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ 10(4): 3988–3995. 

- Wen J, Zhu Y, Zhu M, Tang Z, Li J, Zhou Z, Liu X, Shen C, Peng Y and Feng F (2025c) DiffusionVLA: Scaling robot foundation models via unified diffusion and autoregression. In: _Proceedings of the 42nd International Conference on Machine Learning_ , volume 267. PMLR, pp. 66558–66574. 

- Wu J, Antonova R, Kan A, Lepert M, Zeng A, Song S, Bohg J, Rusinkiewicz S and Funkhouser T (2023a) Tidybot: Personalized robot assistance with large language models. _Autonomous Robots_ 47(8): 1087–1102. 

- Wu K, Zhu Y, Li J, Wen J, Liu N, Xu Z and Tang J (2025a) Discrete policy: Learning disentangled action space for multitask robotic manipulation. In: _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 8811–8818. 

- Wu P, Escontrela A, Hafner D, Abbeel P and Goldberg K (2023b) Daydreamer: World models for physical robot learning. In: _Conference on robot learning_ . PMLR, pp. 2226–2240. 

- Wu Y, Balatti P, Lorenzini M, Zhao F, Kim W and Ajoudani A (2019) A teleoperation interface for loco-manipulation control of mobile collaborative robotic assistant. _IEEE Robotics and Automation Letters_ 4(4): 3593–3600. 

- Wu Y, Xiong Z, Hu Y, Iyengar SS, Jiang N, Bera A, Tan L and Jagannathan S (2025b) Selp: Generating safe and efficient task plans for robot agents with large language models. In: _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 2599–2605. 

- Wu Z, Wang Z, Xu X, Lu J and Yan H (2023c) Embodied task planning with large language models. _arXiv preprint arXiv:2307.01848_ . 

- Wu Z, Zhou Y, Xu X, Wang Z and Yan H (2025c) Momanipvla: Transferring vision-language-action models for general mobile manipulation. In: _Proceedings of the Computer Vision and Pattern Recognition Conference_ . pp. 1714–1723. 

- Xia W, Yang Y, Wu H, Ma X, Kong T and Hu D (2025) Robotic policy learning via human-assisted action preference optimization. _arXiv preprint arXiv:2506.07127_ . 

- Xian Z, Gkanatsios N, Gervet T, Ke TW and Fragkiadaki K (2023) Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 2323–2339. 

- Xiao T et al. (2023) Robotic skill acquisition via instruction augmentation with vision-language models. In: _Robotics: Science and Systems_ . 

- Xiao X, Liu J, Wang Z, Zhou Y, Qi Y, Jiang S, He B and Cheng Q (2025) Robot learning in the era of foundation models: A survey. _Neurocomputing_ : 129963. 

- Xie A, Ebert F, Levine S and Finn C (2019) Improvisation through physical understanding: Using novel objects as tools with visual foresight. _Robotics: Science and Systems_ . 

- Xie A, Lee Y, Abbeel P and James S (2023a) Language-conditioned path planning. In: _Conference on Robot Learning_ . PMLR, pp. 3384–3396. 

- Xie T, Zhao S, Wu CH, Liu Y, Luo Q, Zhong V, Yang Y and Yu T (2024) Text2reward: Reward shaping with language models for reinforcement learning. In: _The Twelfth International Conference on Learning Representations_ . 

- Xie Y, Yu C, Zhu T, Bai J, Gong Z and Soh H (2023b) Translating natural language to planning goals with large-language models. _arXiv preprint arXiv:2302.05128_ . 

- Xing E, Deng M, Hou J and Hu Z (2025a) Critiques of world models. _CoRR_ abs/2507.05169. 

- Xing Y, Luo X, Xie J, Gao L, Shen HT and Song J (2025b) Shortcut learning in generalist robot policies: The role of dataset diversity and fragmentation. In: _Conference on Robot Learning_ . PMLR, pp. 3239–3266. 

- Xiong C, Shen C, Li X, Zhou K, Liu J, Wang R and Dong H (2025) Autonomous interactive correction mllm for robust robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 3139–3156. 

- Xu D, Mart´ın-Mart´ın R, Huang DA, Zhu Y, Savarese S and Fei-Fei LF (2019) Regression planning networks. _Advances in neural information processing systems_ 32: 1319–1329. 

- Xu Z, Gao C, Liu Z, Yang G, Tie C et al. (2024) Manifoundation model for general-purpose robotic manipulation of contact synthesis with arbitrary objects and robots. In: _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 10905–10912. 

- Xue H, Ren J, Chen W, Zhang G, Fang Y, Gu G, Xu H and Lu C (2025) Reactive diffusion policy: Slow-fast visual-tactile policy learning for contact-rich manipulation. In: _Proceedings of Robotics: Science and Systems (RSS)_ . 

- Yamashita A, Arai T, Ota J and Asama H (2003) Motion planning of multiple mobile robots for cooperative manipulation and transportation. _IEEE Transactions on Robotics and Automation_ 19(2): 223–237. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

68 

- Yan G, Wu YH and Wang X (2024) Dnact: Diffusion guided multitask 3d policy learning. _arXiv preprint arXiv:2403.04115_ . 

- Yan Z, Crombez N, Buisson J, Ruichck Y, Krajnik T and Sun L (2021) A quantifiable stratification strategy for tidy-up in service robotics. In: _2021 IEEE International Conference on Advanced Robotics and Its Social Impacts (ARSO)_ . IEEE, pp. 182–187. 

- Yang A, Li A, Yang B, Zhang B, Hui B, Zheng B, Yu B, Gao C, Huang C, Lv C et al. (2025a) Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ . 

- Yang J, Chen X, Madaan N, Iyengar M, Qian S, Fouhey DF and Chai J (2025b) 3d-grand: A million-scale dataset for 3d-llms with better grounding and less hallucination. In: _Proceedings of the Computer Vision and Pattern Recognition Conference_ . pp. 29501–29512. 

- Yang J, Chen X, Qian S, Madaan N, Iyengar M, Fouhey DF and Chai J (2024a) Llm-grounder: Open-vocabulary 3d visual grounding with large language model as an agent. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 7694–7701. 

- Yang J, Glossop C, Bhorkar A, Shah D, Vuong Q, Finn C, Sadigh D and Levine S (2024b) Pushing the limits of cross-embodiment learning for manipulation and navigation. _arXiv preprint arXiv:2402.19432_ . 

- Yang J, Tan W, Jin C, Yao K, Liu B, Fu J, Song R, Wu G and Wang L (2025c) Transferring foundation models for generalizable robotic manipulation. In: _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ . pp. 1999–2010. 

- Yang R, Yu Q, Wu Y, Yan R, Li B, Cheng AC, Zou X, Fang Y, Cheng X, Qiu RZ et al. (2025d) Egovla: Learning visionlanguage-action models from egocentric human videos. _arXiv preprint arXiv:2507.12440_ . 

- Yang S, Du Y, Ghasemipour SKS, Tompson J, Kaelbling LP, Schuurmans D and Abbeel P (2024c) Learning interactive realworld simulators. In: _The Twelfth International Conference on Learning Representations_ . 

- Yang S, Li H, Chen Y, Wang B, Tian Y, Wang T, Wang H, Zhao F, Liao Y and Pang J (2025e) Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ . 

- Yang S, Zhang W, Song R, Cheng J, Wang H and Li Y (2023) Watch and act: Learning robotic manipulation from visual demonstration. _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ 53(7): 4404–4416. 

- Yang Y, Guo J, Li Z, He Z and Zhang J (2024d) Ground4act: Leveraging visual-language model for collaborative pushing and grasping in clutter. _Image and Vision Computing_ 151: 105280. 

- Yang Y, Sun J, Kou S, Wang Y and Deng Z (2025f) Lohovla: A unified vision-language-action model for long-horizon embodied tasks. _arXiv preprint arXiv:2506.00411_ . 

- Yang Y, Zhao L, Ding M, Bertasius G and Szafir D (2025g) Boss: Benchmark for observation space shift in long-horizon task. _IEEE Robotics and Automation Letters_ 10(9): 8882–8889. 

- Yang Z, Garrett C, Fox D, Lozano-P´erez T and Kaelbling LP (2025h) Guiding long-horizon task and motion planning with vision language models. In: _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 16847–16853. 

- Yang Z, Jun M, Tien J, Russell S, Dragan A and Biyik E (2025i) Trajectory improvement and reward learning from comparative 

   - language feedback. In: _Conference on Robot Learning_ . PMLR, pp. 5389–5404. 

- Yao X, Bing Z, Zhuang G, Chen K, Zhou H, Huang K and Knoll A (2023) Learning from symmetry: Meta-reinforcement learning with symmetrical behaviors and language instructions. In: _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 5574–5581. 

- Yao X, Blei T, Meng Y, Zhang Y, Zhou H, Bing Z, Huang K, Sun F and Knoll A (2025a) Long-horizon language-conditioned imitation learning for robotic manipulation. _IEEE/ASME Transactions on Mechatronics_ : 1–12. 

- Yao X, Zhou Y, Meng Y, Dong L, Hong L, Zhang Z, Bing Z, Huang K, Sun F and Knoll A (2025b) Pick-and-place manipulation across grippers without retraining: A learning-optimization diffusion policy approach. _preprint arXiv:2502.15613_ . 

- Yao X, Zhou Y, Meng Y, Liu Y, Dong L, Zhang Z, Bing Z, Huang K, Sun F and Knoll A (2025c) Inference-stage adaptation-projection strategy adapts diffusion policy to crossmanipulators scenarios. _arXiv preprint arXiv:2509.11621_ . 

- Ye F, Lin Y, Lai Y and Huang Q (2024) Task-oriented language grounding for robot via learning object mask. In: _6th International Conference on Robotics, Intelligent Control and Artificial Intelligence (RICAI)_ . pp. 16–22. 

- Yu D, Yang B, Liu D, Wang H and Pan S (2023a) A survey on neural-symbolic learning systems. _Neural Networks_ 166: 105– 126. 

- Yu J, Liu H, Yu Q, Ren J, Hao C, Ding H, Huang G, Huang G, Song Y, Cai P et al. (2026) Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation. _Advances in Neural Information Processing Systems_ 38: 93409–93439. 

- Yu T, Quillen D, He Z, Julian R, Hausman K, Finn C and Levine S (2020) Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. _Conference on robot learning_ : 1094–1100. 

- Yu T et al. (2023b) Scaling robot learning with semantically imagined experience. In: _Robotics: Science and Systems_ . 

- Yu W, Gileadi N, Fu C, Kirmani S, Lee KH, Arenas MG, Chiang HTL, Erez T, Hasenclever L, Humplik J et al. (2023c) Language to rewards for robotic skill synthesis. In: _Conference on Robot Learning_ . PMLR, pp. 374–404. 

- Yuan C, Wen C, Zhang T and Gao Y (2025a) General flow as foundation affordance for scalable robot learning. In: _Conference on Robot Learning_ . PMLR, pp. 1541–1566. 

- Yuan W, Duan J, Blukis V, Pumacay W, Krishna R, Murali A, Mousavian A and Fox D (2025b) Robopoint: A visionlanguage model for spatial affordance prediction in robotics. In: _Conference on Robot Learning_ . PMLR, pp. 4005–4020. 

- Zakka K, Zeng A, Florence P, Tompson J, Bohg J and Dwibedi D (2022a) Xirl: Cross-embodiment inverse reinforcement learning. In: Faust A, Hsu D and Neumann G (eds.) _Proceedings of the 5th Conference on Robot Learning_ , _Proceedings of Machine Learning Research_ , volume 164. PMLR, pp. 537–546. 

- Zakka K, Zeng A, Florence P, Tompson J, Bohg J and Dwibedi D (2022b) Xirl: Cross-embodiment inverse reinforcement learning. In: _Conference on Robot Learning_ . PMLR, pp. 537– 546. 

- Zang Y, Li W, Han J, Zhou K and Loy CC (2025) Contextual object detection with multimodal large language models. _International Journal of Computer Vision_ 133(2): 825–843. 

_Prepared using sagej.cls_ 

_Bridging Language and Action: A Survey of Language-Conditioned Robot Manipulation_ 

69 

- Zawalski M, Chen W, Pertsch K, Mees O, Finn C and Levine S (2025) Robotic control via embodied chain-of-thought reasoning. In: _Conference on Robot Learning_ . PMLR, pp. 3157–3181. 

- Ze Y, Yan G, Wu YH, Macaluso A, Ge Y, Ye J, Hansen N, Li LE and Wang X (2023) Gnfactor: Multi-task real robot learning with generalizable neural feature fields. In: _Conference on Robot Learning_ . PMLR, pp. 284–301. 

- Ze Y, Zhang G, Zhang K, Hu C, Wang M and Xu H (2024) 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. _Robotics: Science and Systems_ . 

- Zeng A, Attarian M, brian ichter, Choromanski KM, Wong A et al. (2023) Socratic models: Composing zero-shot multimodal reasoning with language. In: _The Eleventh International Conference on Learning Representations_ . 

- Zeng A, Florence P, Tompson J, Welker S, Chien J, Attarian M, Armstrong T, Krasin I, Duong D, Sindhwani V et al. (2021) Transporter networks: Rearranging the visual world for robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 726–747. 

- Zeng Y, Mu Y and Shao L (2024) Learning reward for robot skills using large language models via self-alignment. In: _International Conference on Machine Learning_ . PMLR, pp. 58366–58386. 

- Zhai X, Mustafa B, Kolesnikov A and Beyer L (2023) Sigmoid loss for language image pre-training. In: _2023 Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ . pp. 11975–11986. 

- Zhang C, Hao P, Cao X, Hao X, Cui S and Wang S (2026a) Vtla: Vision-tactile-language-action model with preference learning for insertion manipulation. _Biomimetic Intelligence and Robotics_ : 100333. 

- Zhang E, Lu Y, Huang S, Wang WY and Zhang A (2024a) Language control diffusion: Efficiently scaling through space, time, and tasks. In: _The Twelfth International Conference on Learning Representations_ . 

- Zhang H, Du W, Shan J, Zhou Q, Du Y, Tenenbaum JB, Shu T and Gan C (2024b) Building cooperative embodied agents modularly with large language models. In: _The Twelfth International Conference on Learning Representations_ . 

- Zhang J, Guo Y, Chen X, Wang YJ, Hu Y, Shi C and Chen J (2025a) Hirt: Enhancing robotic control with hierarchical robot transformers. In: _2025 Conference on Robot Learning_ . PMLR, pp. 933–946. 

- Zhang J, Luo Y, Anwar A, Sontakke SA, Lim JJ, Thomason J, Biyik E and Zhang J (2025b) Rewind: Language-guided rewards teach robot policies without new demonstrations. In: _Proceedings of The 9th Conference on Robot Learning_ , volume 305. PMLR, pp. 460–488. 

- Zhang J, von Collani Y and Knoll A (1999) Interactive assembly by a two-arm robot agent. _Robotics and Autonomous Systems_ 29(1): 91–100. 

- Zhang S, Wicke P, S¸enel LK, Figueredo L, Naceri A, Haddadin S, Plank B and Sch¨utze H (2023) Lohoravens: A longhorizon language-conditioned benchmark for robotic tabletop manipulation. _arXiv preprint arXiv:2310.12020_ . 

- Zhang T, McCarthy Z, Jow O, Lee D, Chen X, Goldberg K and Abbeel P (2018) Deep imitation learning for complex manipulation tasks from virtual reality teleoperation. In: _2018 IEEE International Conference on Robotics and Automation_ 

_(ICRA)_ . IEEE, pp. 5628–5635. 

- Zhang W, Liu H, Qi Z, Wang Y, Yu X, Zhang J, Dong R, He J, Wang H, Zhang Z et al. (2026b) Dreamvla: a visionlanguage-action model dreamed with comprehensive world knowledge. _Advances in Neural Information Processing Systems_ 38: 24195–24228. 

- Zhang Y and Chai J (2021) Hierarchical task learning from language instructions with unified transformers and selfmonitoring. In: _Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021_ . Online: Association for Computational Linguistics, pp. 4202–4213. 

- Zhang Y and Xue S (2025) A new trend in the warehousing: A review of human robot collaboration. _IEEE Access_ 13: 161194–161205. 

- Zhang Y, Yang J, Pan J, Storks S, Devraj N et al. (2022) DANLI: Deliberative agent for following natural language instructions. In: _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ . Association for Computational Linguistics, pp. 1280–1298. 

- Zhang Z, Hu F, Lee J, Shi F, Kordjamshidi P, Chai J and Ma Z (2025c) Do vision-language models represent space and how? evaluating spatial frame of reference under ambiguities. In: _The Thirteenth International Conference on Learning Representations_ . 

- Zhang Z, Xu H, Yang Z, Yue C, Lin Z, Gao Ha, Wang Z and Zhao H (2025d) Elucidating the design space of torque-aware visionlanguage-action models. In: _Conference on Robot Learning_ . PMLR, pp. 4019–4037. 

- Zhao Q, Lu Y, Kim MJ, Fu Z, Zhang Z, Wu Y, Li Z, Ma Q, Han S, Finn C et al. (2025) Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In: _Proceedings of the Computer Vision and Pattern Recognition Conference_ . pp. 1702–1713. 

- Zhao TZ, Kumar V, Levine S and Finn C (2023a) Learning finegrained bimanual manipulation with low-cost hardware. In: Bekris KE, Hauser K, Herbert SL and Yu J (eds.) _Robotics: Science and Systems XIX_ . 

- Zhao Z, Lee WS and Hsu D (2023b) Large language models as commonsense knowledge for large-scale task planning. _Advances in neural information processing systems_ 36: 31967– 31987. 

- Zhen H, Qiu X, Chen P, Yang J, Yan X, Du Y, Hong Y and Gan C (2024) 3d-vla: A 3d vision-language-action generative world model. In: _2024 International Conference on Machine Learning_ . PMLR, pp. 61229–61245. 

- Zhou D, He M, Fang Z, Yao X, Liu Y, Knoll A and Cao H (2026a) Affordancegrasp-r1: Leveraging reasoning-based affordance segmentation with reinforcement learning for robotic grasping. _arXiv preprint arXiv:2602.03547_ . 

- Zhou H, Bing Z, Yao X, Su X, Yang C, Huang K and Knoll A (2024a) Language-conditioned imitation learning with base skill priors under unstructured data. _IEEE Robotics and Automation Letters_ 9(11): 9805–9812. 

- Zhou H, Lin Y, Yan L, Zhu J and Min H (2024b) Llm-bt: Performing robotic adaptive tasks based on large language models and behavior trees. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 16655–16661. 

- Zhou L and Small K (2021) Inverse reinforcement learning with natural language goals. _Proceedings of the AAAI Conference on Artificial Intelligence_ 35(12): 11116–11124. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

70 

- Zhou Y, Cui C, Yoon J, Zhang L, Deng Z, Finn C, Bansal M and Yao H (2024c) Analyzing and mitigating object hallucination in large vision-language models. In: _12th International Conference on Learning Representations, ICLR 2024_ . 

- Zhou Z, Atreya P, Lee A, Walke HR, Mees O and Levine S (2025a) Autonomous improvement of instruction following skills via foundation models. In: _Conference on Robot Learning_ . PMLR, pp. 4805–4825. 

- Zhou Z, Zhu Y, Liu X, Tang Z, Wen J, Peng Y, Shen C and Xu Y (2026b) Chatvla-2: Vision-language-action model with openworld reasoning. _Advances in Neural Information Processing Systems_ 38: 45537–45559. 

- Zhou Z, Zhu Y, Zhu M, Wen J, Liu N, Xu Z, Meng W, Peng Y, Shen C, Feng F et al. (2025b) Chatvla: Unified multimodal understanding and robot control with vision-language-action model. In: _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ . pp. 5377–5395. 

- Zhu G, Zhou R, Ji W and Zhao S (2025a) Lamarl: Llm-aided multiagent reinforcement learning for cooperative policy generation. _IEEE Robotics and Automation Letters_ 10(7): 7476–7483. 

- Zhu W, Chai M, Singh I, Jia R and Thomason J (2025b) PSALM-V: Automating symbolic planning in interactive visual environments with large language models. _arXiv_ . 

- Ziebart BD, Maas AL, Bagnell JA, Dey AK et al. (2008) Maximum entropy inverse reinforcement learning. In: _Aaai_ , volume 8. Chicago, IL, USA, pp. 1433–1438. 

- Zitkovich B, Yu T, Xu S, Xu P, Xiao T et al. (2023) Rt-2: Visionlanguage-action models transfer web knowledge to robotic control. In: _Conference on Robot Learning_ . PMLR, pp. 2165– 2183. 

_Prepared using sagej.cls_ 

