---
title: "Dexterous Manipulation through Imitation Learning: A Survey"
date: "2025-04-04"
authors: "Shan An; Ziyu Meng; Chao Tang; Yuning Zhou; Tengyu Liu; Fangqiang Ding"
url: https://arxiv.org/abs/2504.03515
pdf: https://arxiv.org/pdf/2504.03515
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2504.03515)** / [論文ページ](https://arxiv.org/abs/2504.03515)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

1 

# Dexterous Manipulation through Imitation Learning: A Survey 

Shan An, _Senior Member, IEEE,_ Ziyu Meng, Chao Tang, Yuning Zhou, Tengyu Liu, Fangqiang Ding, Shufang Zhang, Yao Mu, _Member, IEEE,_ Ran Song, _Senior Member, IEEE,_ Wei Zhang, _Senior Member, IEEE,_ Zeng-Guang Hou, _Fellow, IEEE_ , and Hong Zhang, _Fellow, IEEE_ 

**_Abstract_ —Dexterous manipulation, which refers to the ability of a robotic hand or multi-fingered end-effector to skillfully control, reorient, and manipulate objects through precise, coordinated finger movements and adaptive force modulation, enables complex interactions similar to human hand dexterity. With recent advances in robotics and machine learning, there is a growing demand for these systems to operate in complex and unstructured environments. Traditional model-based approaches struggle to generalize across tasks and object variations due to the high dimensionality and complex contact dynamics of dexterous manipulation. Although model-free methods such as reinforcement learning (RL) show promise, they require extensive training, large-scale interaction data, and carefully designed rewards for stability and effectiveness. Imitation learning (IL) offers an alternative by allowing robots to acquire dexterous manipulation skills directly from expert demonstrations, capturing fine-grained coordination and contact dynamics while bypassing the need for explicit modeling and large-scale trial-and-error. This survey provides an overview of dexterous manipulation methods based on imitation learning, details recent advances, and addresses key challenges in the field. Additionally, it explores potential research directions to enhance IL-driven dexterous manipulation. Our** 

The authors gratefully acknowledge the support of the National Key Research and Development Program of China (Grant No. 2023YFC3603601), and the National Natural Science Foundation of China (Grant No. U22A2057). (Corresponding author: Ran Song) 

Shan An is with the Tianjin Key Laboratory of Intelligent Unmanned Swarm Technology and System, the School of Electrical and Information Engineering, Tianjin University, Tianjin 300072, China. 

Ziyu Meng is with the School of Control Science and Engineering, Shandong University, Jinan 250061, China, also with the State Key Laboratory of General Artificial Intelligence, Beijing 100086, China. 

Chao Tang is with the Division of Robotics, Perception and Learning at KTH Royal Institute of Technology, Stockholm 11428, Sweden. 

Ran Song and Wei Zhang are with the School of Control Science and Engineering, Shandong University, Jinan 250061, China. (e-mail: ransong@sdu.edu.cn). 

Yuning Zhou is with the Department of Mechanical and Process Engineering, ETH Zurich, 8092 Zurich, Switzerland. 

Tengyu Liu is with the State Key Laboratory of General Artificial Intelligence, Beijing 100086, China. 

Fangqiang Ding is with the Department of Mechanical Engineering at the Massachusetts Institute of Technology (MIT), MA 02118, USA. 

Shufang Zhang is with the School of Electrical and Information Engineering, Tianjin University, Tianjin 300072, China. 

Yao Mu is with the School of Computer Science, Shanghai Jiao Tong University, Shanghai 200240, China. 

Zeng-Guang Hou is with the State Key Laboratory of Multimodal Artificial Intelligence Systems, Institute of Automation, Chinese Academy of Sciences, Beijing 100190, China, also with the School of Artificial Intelligence, University of Chinese Academy of Sciences, Beijing 100049, China, and also with CASIA-MUST Joint Laboratory of Intelligence Science and Technology, Institute of Systems Engineering, Macau University of Science and Technology, Macao 999078, China. 

Hong Zhang is with the Department of Electronic and Electrical Engineering, Southern University of Science and Technology, Shenzhen 518055, China. 

**goal is to offer researchers and practitioners a comprehensive introduction to this rapidly evolving domain.** 

**_Note to Practitioners_ —This work explores the intersection of IL and dexterous manipulation. With promising applications in manufacturing, healthcare, and home robotics, IL-based approaches allow robots to handle delicate objects, execute precise tasks, and operate in diverse, unstructured environments. However, key challenges remain—particularly in collecting highquality demonstrations and enabling generalization from limited data, both of which are critical for real-world deployment. This survey aims to serve as a practical and accessible guide for practitioners seeking to apply IL-based methods to develop more capable and adaptable robotic systems in real-world scenarios.** 

**_Index Terms_ —Dexterous Manipulation, Imitation Learning, End Effector, Teleoperation** 

## I. INTRODUCTION 

**O** VERtensivetheresearchpast fewinterests,decades,withroboticsdexteroushas manipulationattracted inemerging as a particularly popular focus. Dexterous manipulation aims to perform complex, precise, and flexible tasks (such as grasping an object, opening a drawer, and rotating a pencil) in various scenes with human-level dexterity using robotic hands or other end-effectors, as illustrated in Fig. 1. This high-precision manipulation capability supports a broad spectrum of applications, including industrial manufacturing [1]–[4], space or underwater exploration, [5]–[8], and medical care [9]–[12]. Recently, the rapid development of imitation learning (IL) [13], [14], which seeks to acquire knowledge by observing and mimicking behaviors of humans or other agents, has led to notable advancements in computer graphics and robotics. As an intuitive approach to equip robots with human prior knowledge, especially in the ability to interact with objects and understand scenes, IL has shown exceptional performance in enabling robots to perform tasks with humanlike dexterity. 

Research on dexterous manipulation has received significant attention even before reinforcement learning (RL) was adopted to optimize behavior strategies through iterative interactions with the environment and reward-based feedback mechanisms. Traditional approaches encourage robots to acquire dexterous manipulation skills by modeling domain dynamics and applying optimal control methods. These approaches are theoretically sound but rely heavily on the fidelity of the world model. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

2 


Fig. 1. Examples of dexterous manipulation in the real world. Row 1: Customized dexterous manipulation platform, Dextreme [15], DexCap [16], Row 2: Robotic telekinesis [17], Dexpilot [18], Row 3: Anyteleop [19]. 

However, when it comes to dexterous operations, such as assembling precision components or performing complex surgical procedures, a high degree of flexibility and multidegree-of-freedom movement capabilities are required to execute complex, human-like tasks. The successful execution of dexterous manipulation hinges upon intricate and highly precise mechanical design, such as multi-fingered robotic hand [20] or anthropomorphic arms [21], as well as sophisticated control algorithms required to handle high-dimensional spaces [21] and multi-contact dynamics [22]. 

Recently, the exploration of employing IL in the field of robotics has garnered significant attention from researchers. Without the need to craft complex world models and carefully designed reward functions, IL enables robots to learn tasks by observing and imitating expert demonstrations. This approach is intuitive, as the goal is for robots to substitute human labor by performing tasks like human experts. Specifically, the initial step involves collecting a dataset of expert demonstrations, which contains trajectories of manipulation tasks conducted by humans or well-trained agents. Robots use such trajectories as a reference to learn task behaviors. To ensure consistency, it is preferable to use identical robots during both the data collection and execution phases. However, this implementation does not facilitate data sharing among heterogeneous robotic systems. One solution is to map the trajectory of the original manipulator to the target robots, a process known as retargeting. Nonetheless, the process of humans operating robots for data collection remains time-consuming and laborintensive in constructing large-scale datasets. To address this issue, researchers [17], [23], [24] have adopted pose estimation techniques from computer vision to develop mappings from human hands to robotic hands, effectively lowering the barriers of collecting demonstration data. Additionally, dataset augmentation enhances the ability to generalize to new objects and scenes, contributing to the expansion of the dataset. 

IL mimics expert behaviors analogous to supervised learning (SL) and often integrates with RL to address complex 

decision-making tasks. Both IL and SL share similarities in learning from demonstrations or ground truth data. However, their objectives differ: SL aims to produce outputs identical to the ground truth in static scenarios, while IL focuses on task completion in dynamic environments, such as changes in target object position and environmental disturbances in manipulation tasks. Such tasks usually involve sequential decision-making, where errors can accumulate over steps, leading to compounding errors and overall task failure. IL emphasizes task completion by adjusting and compensating for initial errors in subsequent decisions, thereby reducing their overall impact. In dexterous manipulation tasks, RL and IL are often combined. This combination addresses the inefficiencies caused by the agent’s large and complex action space, has a high degree of freedom, and makes pure RL exploration less effective. IL leverages expert demonstrations to offer straight guidance, thereby reducing exploration time and increasing efficiency. Additionally, reward functions for manipulation tasks are often challenging to design. Different tasks typically necessitate distinct reward functions. However, IL benefits from a relatively universal reward function to fit demonstration trajectories, necessitating only the provision of varied demonstration data, which ultimately improves learning efficiency and task success rates. 

IL is particularly advantageous for dexterous manipulation tasks. This is because objects involved in dexterous manipulation are typically designed for human use, and thus, robots subject to these tasks are likely to have structures similar to humans or parts of the human body, such as humanoid robots, dual-arm manipulators, or dexterous hands. They usually require precise control, coordination, and adaptability, attributes that are challenging to achieve through traditional methods. Specifically, this learning paradigm includes various branches such as behavior cloning [25], [26], hybrid approaches (the combination of RL and IL) [27], [28], hierarchical IL [29], [30], and others, each contributing unique advantages to the learning process. 

Since the intersection of IL and dexterous manipulation represents a frontier in robotics research. In the past decade, several works including DAPG [27], which combined deep reinforcement learning(DRL) with human demonstrations to solve high-dimensional dexterous manipulation tasks; Implicit Behavioral Cloning [26] which focused on improving robot policy learning from a mathematical perspective; Hiveformer [31], which explored creating multimodal interactive agents; Diffusion Policy [32] leveraged recent advancement in generative models to achieve better performance in manipulation tasks, have been proposed and significantly expanded the boundaries of what is achievable in robotic dexterous manipulation. However, despite the recent considerable progress in this field, numerous challenges remain. Data collection for IL is labor-intensive and time-consuming [33], [16]. The acquisition of generalization ability from learned behaviors to new tasks and varying environments is also non-trivial [34]. Additionally, real-time control and sim-to-real transfer, where robots trained in the simulation must perform effectively in the real world, both hinder the application [35]. Addressing these challenges requires a concerted effort to develop more 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

3 


Fig. 2. Overview of imitation learning-based dexterous manipulation methods in this survey. 

efficient data collection methods, improve learning algorithms, and enhance the physical capabilities of robotic systems. 

Building on significant advancements in the intersection of IL and dexterous manipulation, several recent surveys have explored key aspects of this rapidly evolving field. Zare et al. [36] provided an extensive overview of the applications, progress, and challenges of imitation learning in both robotics and artificial intelligence. Arora and Doshi [37] focused on inverse reinforcement learning (IRL), particularly the process of inferring reward functions from observed behavior. Han et al. [38] delved into deep reinforcement learning (DRL), reviewing recent methods designed to optimize DRL algorithms for real-world applications. Li et al. [39] offered a comprehensive review of data collection methods and skill learning frameworks for robotic dexterous manipulation, emphasizing the key challenges in this area. Pitkevich and Makarov [40] addressed the Sim-to-Real transfer problem in DRL, discussing the deployment of robots trained in simulation to real-world environments. Welte and Rayyes [41] examined the potential of interactive imitation learning for humanoid robots, with a focus on how these methods can be transplanted for dexterous tasks. Finally, Tsuji et al. [42] provided a systematic review of imitation learning techniques for contact-rich tasks, discussing the unique challenges and emerging trends in this field. In contrast to these existing works, which primarily focus on specific aspects of imitation learning or dexterous manipulation, this survey aims to provide a comprehensive overview of IL-based dexterous manipulation approaches. 

The rest of this article is organized as follows: Section II 

presents an introduction to dexterous manipulation and IL in detail. Subsequently, we discuss the state-of-the-art ILbased dexterous manipulation techniques and highlight notable achievements in this field in Section III. Section IV discusses end-effectors for dexterous manipulation. Moreover, we discuss teleoperation systems and datasets in Section V. We summarize existing challenges and propose future directions for research in this rapidly evolving field in Section VI. Finally, conclusions are made in Section VII. An overview of this survey is shown in Fig. 2. By synthesizing the existing body of knowledge, this survey aspires to serve as a valuable resource for researchers and practitioners seeking to advance the capabilities of robotic systems through the synergy of IL and dexterous manipulation. 

## II. OVERVIEW OF IMITATION LEARNING BASED DEXTEROUS MANIPULATION 

## _A. Dexterous Manipulation_ 

In the field of robotics, dexterous manipulation [43]–[46] refers to the capability of robotic systems to execute intricate and precise tasks. These tasks often employ grippers or dexterous hands to grasp, maneuver, and manipulate objects [47]. Characterized by high degrees of freedom and fine motor skills, dexterous manipulation extends beyond simple pickand-place operations to include activities such as tool use, object reorientation, and complex assembly tasks. Achieving such manipulation commonly involves using sophisticated end-effectors designed to emulate the versatility and finesse 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

4 

of human hands, such as multi-fingered hands or anthropomorphic robotic arms. 

Dexterous manipulation poses several significant challenges, including precise control, high-dimensional motion planning, and real-time adaptability to dynamic environments [48]. The intricacies of these tasks demand robust mechanical design and advanced control algorithms capable of handling the complexities of multi-contact interactions and the variability inherent in real-world scenarios. Traditional model-based methods [49], [50] have become inadequate for robots performing complex tasks due to the increasing complexity of manipulation tasks. Consequently, extensive research has been dedicated to learning-based approaches, with RL emerging as an effective method. Various works have exploited RL for robots to learn dexterous policies [51]–[56]. However, pure RL has several inherent drawbacks. RL algorithms often struggle with exploring high-dimensional action spaces efficiently in dexterous manipulation tasks [57]. Additionally, designing reasonable reward functions is challenging; flawed reward functions can affect exploration and learning speed, leading to inferior performance. Recently, advancements in IL have opened new avenues for addressing these challenges. 

## _B. Imitation Learning_ 

The main purpose of IL is to enable agents to learn and perform behaviors by imitating expert demonstrations [35]. In contrast, pure RL requires carefully designed reward functions and is particularly effective in scenarios where the desired behavior is difficult to describe in algorithms but can be easily demonstrated. IL employs these expert demonstrations to guide the learning process of agents by establishing the correlation between observed states and corresponding actions. Through IL, agents can transcend merely replicating basic and predefined behaviors within controlled and constrained environments, enabling them to autonomously execute optimal actions in complex, unstructured environments [58]. Consequently, IL significantly alleviates the burden on experts, facilitating efficient skill transfer. 

Methodologies of IL can be broadly categorized into several sub-classes, including behavior cloning [59], inverse reinforcement learning (IRL) [60], and generative adversarial imitation learning (GAIL) [61]. Behavior cloning directly maps observed actions to the agent’s actions through SL techniques. Conversely, IRL aims to deduce the underlying reward structure that motivates the demonstrator’s behavior, allowing the agent to optimize its actions accordingly. GAIL employs adversarial training techniques to improve the imitation policy by distinguishing between expert and agent actions, thus refining the agent’s ability to replicate the desired behavior accurately. 

## _C. Connections to Human Motor Learning_ 

IL is fundamentally motivated by the way humans acquire motor skills through observation, demonstration, and practice. From a cognitive perspective, Bandura’s social learning theory [62] emphasized that behavior can be learned by observing others, rather than solely through reinforcement 

or trial-and-error. This insight has inspired IL paradigms that rely on demonstration-based policy generation instead of environment-driven exploration. 

At the neural level, the discovery of mirror neurons in primates provides biological evidence that action observation and execution may share overlapping representations [63]. These findings suggest that learning by watching others perform a task can activate internal motor plans, a mechanism analogous to behavioral cloning in robotics. Furthermore, models of human motor control, such as the internal model theory [64] and optimal feedback control [65], offer insights into how the brain predicts, plans, and corrects motor behaviors. These principles have influenced the design of IL algorithms that incorporate predictive models or closed-loop feedback refinement. For example, Nah et al. [66] presented a modular robot control framework using Dynamic Movement Primitives (DMP) and Elementary Dynamic Actions (EDA), employing dynamical systems to predict and correct motor behaviors in a manner similar to internal models in the brain. 

In summary, the foundations of IL are deeply rooted in cognitive and neuroscientific principles, from observational learning and mirror neuron systems to predictive motor control and hierarchical skill organization. These biological insights continue to shape IL algorithms, guiding the development of methods that mimic the way humans learn and adapt motor behaviors. 

## _D. Long-horizon Dexterous Manipulation_ 

Long-horizon dexterous manipulation involves executing complex tasks that require both fine-grained control and longterm planning. These tasks typically span long time horizons and require coherent, efficient execution of sequential actions. Without an appropriate structure, such tasks can overwhelm agents, complicating both planning and execution. Task decomposition addresses this challenge by enabling agents to focus on different task components at various levels of abstraction, thereby facilitating the management of long-horizon manipulation [67]. In the context of IL, task decomposition is commonly realized through temporal abstraction, often implemented via techniques such as option discovery [68] or hierarchical policy structures [69], [70]. 

Temporal abstraction enables an agent to make decisions through temporally extended action sequences, thereby accelerating learning and simplifying complex tasks. Option discovery refers to the automated process of identifying and constructing these temporal abstractions, known as options, that comprise an internal low-level policy, an initiation set, and a termination condition. The options framework [71], [72] generalizes the traditional action concept by treating options as temporally extended actions, allowing planning over multiple time scales. The option-critic architecture [73] and its variants are widely adopted to automatically extract options from demonstration data, which are then scheduled by highlevel policies to effectively organize the temporal structure of tasks. For example, DDCO [74] autonomously discovers and learns hierarchical options within continuous action spaces from expert demonstrations, enabling unsupervised task decomposition and hierarchical IL for robotic control. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

5 

Hierarchical RL is often integrated with IL to tackle longhorizon tasks and complex policy learning [75]. The fundamental principle involves leveraging human demonstrations to decompose tasks along temporal or functional dimensions, which reduces the policy search space and enhances both learning efficiency and generalization. For example, SRTH [76] proposed a hierarchical language-conditioned IL framework that integrates high-level instruction parsing with lowlevel dexterous control to allow the execution of end-to-end autonomous surgical tasks. 

## _E. Multi-agent or Collaborative Dexterous Manipulation_ 

Multi-agent or collaborative dexterous manipulation refers to the system-level problem in which two or more agents endowed with multi-fingered dexterous manipulation capabilities, such as robot arms, dexterous hands, or mobile manipulators, jointly accomplish a high-dimensional, long-horizon, contact-rich task. The scenario emphasizes: 

- heterogeneous or homogeneous agents sharing workspace and task objectives; 

- explicit or implicit communication (force, vision, language instructions) for action synchronization and load distribution; 

- leveraging the redundant degrees of freedom of multiple arms/hands to realize complex operations unattainable by a single arm (e.g., bimanual valve turning, multi-human cooperative suturing). 

To enable collaborative dexterous manipulation, Kim et al. [76] introduced the SRT-H framework, which employs a hierarchical policy integrating high-level language instructions with low-level trajectory imitation. In a dual-arm da Vinci suturing task, the framework achieves precise bimanual coordination over long horizons, relying solely on human demonstrations without any reward supervision. Building on this line of research, BUDS [21] introduced a “stabilize-thenact” role decomposition with a visual keypoint stabilization mechanism, attaining 76.9% task success on complex bimanual dexterous tasks without reward signals or RL finetuning. Extending further, Bi-DexHands [77] framed bimanual dexterous manipulation as a comprehensive suite of over 20 cooperative sub-tasks, providing the first large-scale benchmark for evaluating the scalability of multi-agent RL in physically coordinated manipulation. More recently, BiDexHD [78] advanced collaborative dexterous manipulation by integrating multi-task human demonstration data with teacher–student policy learning. This framework enables robots to efficiently acquire a wide range of cooperative bimanual skills across numerous auto-constructed tasks, substantially improving task completion rates and zero-shot generalization. 

While task-level coordination addresses high-level planning, physical-level coordination must handle coupled, contact-rich dynamics inherent to dexterous manipulation. This challenge is addressed through unified model-based control. For example, Sleiman et al. [79] proposed a whole-body MPC framework that jointly optimizes contact forces and centroidal dynamics in real time, enabling coherent coordination of locomotion and manipulation. Likewise, Yu et al. [80] integrated global 

planning with adaptive MPC for dual-arm manipulation of deformable objects, capturing coupling through predictive dynamics. Beyond conventional hands, Zhong et al. [81] demonstrated that even micro-scale multi-agent coordination requires explicit handling of coupling dynamics, modeling nonlinear magnetic interactions between paired millirobots via data-driven inversion control and active disturbance rejection. These approaches collectively demonstrate that real-time compensation of coupled dynamics is essential for safe, responsive, and generalizable multi-agent IL policies. 

In general, the core challenge of multi-agent or collaborative dexterous manipulation lies in learning generalizable cooperative policies within large-scale continuous control spaces while satisfying safety, real-time responsiveness, and consistency with human demonstrations, particularly under the imitationlearning paradigm. 

## III. IMITATION LEARNING BASED DEXTEROUS MANIPULATION APPROACHES 

We categorize IL-based dexterous manipulation approaches into four categories: (1) Behavioral Cloning, (2) Inverse Reinforcement Learning, (3) Generative Adversarial Imitation Learning, and other extended frameworks, including (4) Hierarchical Imitation Learning and (5) Continual Imitation Learning. In the following subsections, we provide an overview of each category, followed by a detailed description and a summary of key research progress. Tab. I presents a comparison between different IL approaches. 

## _A. Behavioral Cloning_ 

_1) Description:_ Behavioral Cloning (BC) refers to replicating expert behavior by learning directly from demonstrated state-action pairs. Specifically, BC is characterized by (1) a supervised learning paradigm and (2) a direct mapping from states to actions without relying on reward signals or exploration, as is typical in RL. 

To formally define BC, we consider a set of _n_ demonstrations _D_ = _{τ_ 1 _, . . . , τn}_ , where each demonstration _τi_ is a sequence of state-action pairs of length _Ni_ . Specifically, _τi_ = _{_ ( _s_ 1 _, a_ 1) _, . . . ,_ ( _sNi, aNi_ ) _}_ , with states _s ∈S_ and actions _a ∈A_ . _S_ and _A_ denote the state and action spaces, respectively. The objective of BC is to learn a policy _π_ : _S →A_ that imitates the expert behavior by minimizing the negative loglikelihood of the demonstrated actions. Formally, the objective function is: 


_2) Research Progress:_ BC has achieved significant progress in dexterous manipulation [20], [82], [83], [126], [127] and has demonstrated effective performance in relatively simple tasks, such as pushing [84] and grasping [14]. However, its applicability in dynamic environments and long-horizon tasks remains an active area of research. 

The training data for BC models are usually collected from expert demonstrations tailored to specific tasks. Consequently, when the agent encounters states that are unseen during training, it may produce actions that deviate from the expert’s 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

6 

TABLE I 

COMPARISON OF DIFFERENT IMITATION LEARNING APPROACHES 

|**Approach**|**Key Characteristics**|**Pros**|**Cons**|**Key Applications**|
|---|---|---|---|---|
|**Behavioral**<br>**Cloning**<br>[14],<br>[20], [26], [29], [32], [82],<br>[82]–[91]|_•_ Supervised learning paradigm.<br>_•_ Mapping from states to actions.<br>_•_ No reward signals or exploration.|_•_ Simple and easy to imple-<br>ment.<br>_•_ Data-efficient with large<br>demonstrations.|_•_ Prone to distribution shift.<br>_•_ Poor generalization to<br>unseen states.|_•_ Grasping<br>and<br>pick-and-<br>place tasks.<br>_•_ Short-horizon,<br>structured<br>tasks with sufficient data.|
|**Inverse Reinforcement**<br>**Learning**<br>[37],<br>[38],<br>[53],<br>[92]–[99]|_•_ Inferring expert’s reward function.<br>_•_ Deriving policy by maximizing the<br>inferred reward.|_•_ Generalization to new situ-<br>ations.<br>_•_ Suitable for tasks with un-<br>known<br>rewards.|_•_ Computationally intensive.<br>_•_ Non-unique reward solu-<br>tions.|_•_ Complex tool-use tasks.<br>_•_ Assembly tasks with im-<br>plicit objectives.|
|**Generative Adversarial**<br>**Imitation**<br>**Learning**<br>[23],<br>[100]–[113]|_•_ Adversarial training between genera-<br>tor and discriminator.<br>_•_ No explicit reward function.|_•_ Good sample efficiency.<br>_•_ Improved robustness.|_•_ Training instability.<br>_•_ Mode collapse and sensi-<br>tivity<br>to hyperparameters.|_•_ Long-horizon<br>dexterous<br>tasks.<br>_•_ In-hand manipulation with<br>sparse demonstrations.|
|**Hierarchical Imitation**<br>**Learning** [114]–[120]|_•_ Two-level hierarchical policy.<br>_•_ Decomposing tasks into sub-tasks<br>and primitives.|_•_ Scalable to complex tasks.<br>_•_ Modular and reusable<br>sub-policies.|_•_ Requiring<br>hierarchy<br>de-<br>sign.<br>_•_ Requiring training coordi-<br>nation.|_•_ Multi-step<br>assembly<br>and<br>contact-rich tasks.<br>_•_ Skill chaining and long-<br>horizon manipulation.|
|**Continual Imitation**<br>**Learning** [118], [121]–[125]|_•_ Continual skill acquisition.<br>_•_ Adapting previously learned behav-<br>iors.|_•_ Flexible to evolving tasks.<br>_•_ Reducing forgetting of old<br>skills.|_•_ Risk of catastrophic forget-<br>ting.<br>_•_ Requiring ongoing expert<br>input.|_•_ Lifelong<br>learning<br>for<br>multi-task manipulation.<br>_•_ Adapting to changing tools<br>or objects.|


behavior, leading to task failure. In sequential decision-making processes, even small deviations from expert actions at each step can accumulate over time, resulting in what is known as the “compounding error” problem. This issue is particularly pronounced in dexterous manipulation tasks [85], [86], due to the high dimensionality of the action space and the strong dependency between task success and the consistency of the predicted action trajectory. To mitigate compounding errors in dexterous manipulation, Mandlekar et al. [29] proposed a hierarchical framework that segments demonstration trajectories at intersection points across different tasks and recombines them to synthesize trajectories for unseen tasks. Similarly, Zhao et al. [82] addressed the problem by considering the compatibility with high-dimensional visual observations. Instead of predicting actions step by step, they propose to predict entire action sequences, thereby reducing the effective decision horizon and alleviating compounding errors. 

Another challenge in BC is its limited ability to model multimodal data, which is prevalent in human demonstrations collected from real-world environments. To overcome this limitation, several approaches have been proposed to model multi-modal action distributions. Florence et al. [26] formulated BC as a conditional energy-based modeling problem for capturing multi-modal data distribution, albeit at the cost of increased computational overhead. Similarly, Shafiullah et al. [87] proposed to model the action distribution as a mixture of Gaussians. Their method leverages the Transformer architecture to efficiently utilize the history of previous observations and enables multi-modal action prediction through token-based outputs. Another promising direction is leveraging generative models to capture the inherent diversity of expert behaviors. Mandlekar et al. [88] proposed using generative models for trajectory prediction, enabling selective imitation, though this approach relies on carefully curated, task-specific datasets. 

More recently, diffusion models have shown great potential in enhancing the robustness and generalization of BC methods. Chen et al. [89] proposed a diffusion-augmented BC 

framework that models both conditional and joint probability distributions over expert demonstrations. Building on this idea, Chi et al. [32] employed diffusion models as decision models to directly generate sequential actions conditioned on visual input and the robot’s current state. Additionally, the 3D Diffusion Policy [90] leveraged 3D input representations to better capture scene spatial configurations. Similarly, the 3D Diffuser Actor [91] utilized full 3D scene representations by integrating RGB and depth information, along with language instructions, robot proprioception, and noise trajectories, through a 3D Relative Transformer framework. 

Compared to variational autoencoders (VAEs) [128] and generative adversarial networks (GANs) [129], diffusion models offer several advantages for imitation learning, particularly in modeling complex, multimodal action distributions [32], [130]. Chen et al. [89] proposed using diffusion models to augment BC and conducted a comprehensive comparison with other generative models, including VAEs, GANs, and EBMs (energy-based models)/implicit models, across different implementations in terms of model architecture, sampling/inference cost, and performance on various continuous control and manipulation tasks. Experimental results demonstrated that diffusion-augmented BC outperformed standard BC and several other generative model variants on multiple tasks. 

_3) Discussion:_ In general, BC-based methods struggle with generalization and modeling multi-modal action distributions. To overcome these limitations, diffusion models have recently attracted increasing attention. They can be employed either as decision models that directly generate action sequences [32] or as high-level strategy models that guide the action generation process [89]. In both settings, diffusion models have shown promising performance and improved flexibility over conventional BC methods. 

## _B. Inverse Reinforcement Learning_ 

_1) Description:_ Inverse Reinforcement Learning (IRL) inverts the conventional RL framework, which focuses on learn- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

7 

ing a policy to maximize a predefined reward function. Instead, IRL aims to infer the underlying reward function that best explains a set of expert demonstrations. 

Formally, IRL estimates a reward function _R_ ( _s, a_ ) that best aligns with the demonstrated state-action pairs _D_ = _{τ_ 1 _, τ_ 2 _, . . . , τN }_ , where _τi_ = _{_ ( _s_ 0 _, a_ 0) _,_ ( _s_ 1 _, a_ 1) _, . . . ,_ ( _st, at_ ) _}_ . It is assumed that these demonstrations are generated by an expert following an optimal or near-optimal policy. The IRL problem is typically formulated within a finite Markov Decision Process, defined as _M_ = _⟨S, A, T, R, γ⟩_ , where _S_ and _A_ are the state and action spaces, _T_ ( _s_<sup>_′_</sup> _|s, a_ ) is the state transition probability, _R_ ( _s, a_ ) is the reward function, and _γ ∈_ [0 _,_ 1] is the discount factor. IRL often represents the reward function as a linear combination of feature functions: 


where _ϕ_ ( _s, a_ ) is a feature vector and _w_ is a learnable weight vector. The expected feature counts under a policy _π_ are defined as: 


where _ψ_<sup>_π_</sup> ( _s_ ) denotes the state-action visitation frequency: 


IRL is particularly advantageous in dexterous manipulation scenarios, where manually defining a reward function is often challenging or impractical. IRL has demonstrated effectiveness in various dexterous manipulation tasks, including dexterous grasping, assembly, and manipulation in dynamic and uncertain environments. 

_2) Research Progress:_ Recent studies have leveraged IRL frameworks to tackle complex dexterous manipulation tasks. Orbik et al. [92] first advanced IRL for dexterous manipulation by introducing reward normalization, task-specific feature masking, and random sample generation. These techniques effectively mitigate reward bias toward demonstrated actions and enhance learning stability in high-dimensional state-action spaces, leading to better generalization across unseen scenarios. Building upon the need for efficient learning in such high-dimensional settings, Generative Causal Imitation Learning [93] improved the sample efficiency of IRL by integrating maximum entropy modeling with adaptive sampling strategies. By leveraging nonlinear function approximation through neural networks, the proposed method enables expressive cost function learning while handling unknown system dynamics. To further incorporate user feedback into the learning process, ErrP-IRL [94] integrated error-related potentials [95] with IRL. This approach assigns trajectory weights based on users’ cognitive responses, which are then used to iteratively refine a reward function represented as a sum of radial basis functions. 

Beyond human feedback, recent works have explored learning reward functions from large-scale, unstructured demonstrations. GraphIRL [96] extracted task-specific embeddings from diverse video demonstrations. By modeling object interactions as graphs and performing temporal alignment, GraphIRL learns transferable reward functions without requiring explicit 

reward design or environment correspondence, enabling crossdomain manipulation capabilities. To further improve policy precision, Naranjo-Campos et al. [97] proposed to integrate IRL with Proximal Policy Optimization [53]. Their method incorporates expert-trajectory-based features and a reverse discount factor to address feature vanishing issues near goal states, thereby improving the robustness of the learned policies. More recently, Visual IRL [98] extended the scope of IRL to human-robot collaboration tasks. It employs adversarial IRL to infer reward functions from human demonstration videos and introduces a neuro-symbolic mapping that translates human kinematics into robot joint configurations. This approach not only ensures accurate end-effector placement but also preserves human-like motion dynamics, facilitating natural and effective robot behavior in dexterous manipulation tasks. 

_3) Discussion:_ In summary, IRL has demonstrated significant potential for dexterous manipulation tasks. By inferring the underlying reward function from expert demonstrations, IRL enables robots to generalize complex behaviors and adapt to diverse environments without the need for manually designed reward functions. This capability is particularly valuable in dexterous manipulation scenarios where reward specification is challenging or impractical [37], [38]. Despite these promising developments, state-of-the-art IRL methods still face several limitations. One of the primary challenges lies in accurately estimating reward functions, particularly in environments with high-dimensional action spaces or sparse feedback signals. Furthermore, IRL methods often rely on large amounts of expert demonstration data, which poses practical constraints due to the high cost and time required for data collection [37], [99]. 

## _C. Generative Adversarial Imitation Learning_ 

_1) Description:_ Generative Adversarial Imitation Learning (GAIL) extends the Generative Adversarial Network (GAN) framework [131] to the domain of IL. It formulates the imitation process as a two-player adversarial game between a generator and a discriminator. The generator corresponds to a policy _π_ that aims to produce behavior that closely resembles expert demonstrations, while the discriminator _D_ ( _s, a_ ) evaluates whether a state-action pair ( _s, a_ ) originates from the expert data _M_ or is generated by _π_ . 

Specifically, GAIL minimizes the Jensen-Shannon divergence between the state-action distributions of the expert and the generator. The discriminator is trained to maximize the following objective: 


where _d_<sup>_M_</sup> ( _s, a_ ) and _d_<sup>_π_</sup> ( _s, a_ ) denote the state-action distributions of the expert and the generator, respectively. The generator’s policy _π_ is optimized using RL with a reward signal derived from the discriminator: 


Through this adversarial training process, GAIL effectively learns complex behaviors from expert demonstrations without explicitly recovering the reward function. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

8 

_2) Research Progress:_ GAIL has been widely adopted in dexterous manipulation. However, its effectiveness heavily relies on the quality and availability of expert demonstrations, which are often labor-intensive to collect and prone to inconsistencies [100], [101]. Such discrepancies arise from factors like collector biases [102], expert errors, noisy data, non-convex solution spaces, and suboptimal strategies [103]. Additionally, data scarcity further limits learning efficiency and policy robustness. 

To address these challenges, various GAIL extensions have been proposed. HGAIL [104] employed hindsight experience replay to synthesize expert-like demonstrations without requiring real expert data. AIL-TAC [103] introduced a semisupervised correction network to refine noisy demonstrations. GAIL has also been used in sim-to-real transfer [105], reducing the dependence on real-world expert data. Nevertheless, GAIL still suffers from mode collapse, where learned policies capture only a narrow range of behaviors, and gradient vanishing issues when the discriminator overpowers the generator. To mitigate these problems, RIDB [106] incorporated variational autoencoders to learn semantic policy embeddings and enable smooth interpolation across behaviors. WAIL [107] leveraged the Wasserstein GAN framework [108] to improve training stability and reduce mode collapse. DIL-SOGM [109] further introduced a self-organizing generative model to capture multiple behavioral patterns without requiring encoders. In parallel, several works improve GAIL’s robustness under imperfect demonstrations. GA-GAIL [110] employed a second discriminator to identify goal states, enhancing policy learning from suboptimal data. RB-GAIL [111] integrated ranking mechanisms and multiple discriminators to model diverse behavior modes while leveraging generated experiences. 

In addition to addressing the quality and availability of expert demonstrations, recent studies have sought to improve the performance of GAIL-based dexterous manipulation methods in other aspects. For instance, TRAIL [112] introduced constrained discriminator optimization to prevent the discriminator from focusing on spurious, task-irrelevant features such as visual distractors, thereby preserving meaningful reward signals and enhancing task performance. In the context of human imitation, Antotsiou et al. [23] combined inverse kinematics and particle swarm optimization with GAIL to mitigate sensor noise and domain discrepancies, enabling robots to autonomously grasp objects in simulation environments. Furthermore, P-GAIL [113] incorporated entropy-maximizing deep P-networks into GAIL to improve policy learning in deformable object manipulation tasks. 

_3) Discussion:_ Although several extensions have addressed specific challenges of GAIL in dexterous manipulation, it still inherits the fundamental limitations of adversarial training. In particular, GAIL often suffers from training instability and faces difficulties in scaling to high-dimensional action spaces. 

## _D. Hierarchical Imitation learning_ 

_1) Description:_ Hierarchical Imitation Learning (HIL) is an IL framework designed to address complex tasks by decomposing them into a hierarchical structure. HIL typically adopts 

a two-level hierarchy, where the high-level policy is responsible for generating a sequence of sub-tasks or primitives based on the current state and task requirements, and the low-level policy executes sub-tasks to achieve the overall objective. This hierarchical decomposition enables handling long-horizon and complex tasks more effectively by separating decision-making and control. 

Mathematically, the high-level policy _πh_ selects a primitive _pi_ from a predefined set of primitives _{p_ 1 _, p_ 2 _, . . . , pK}_ : 


where _i ∈{_ 1 _,_ 2 _, . . . , K}_ . The corresponding low-level policy _πpi_ then generates the action to execute the selected primitive: 


The overall objective of HIL is to minimize the cumulative loss function _L_ ( _π_ ), which explicitly reflects the hierarchical structure of the policy by jointly optimizing both the highlevel decision-making and the low-level control execution to achieve effective task decomposition and coordination: 


where _ℓ_ ( _st, at_ ) represents the immediate loss at time step _t_ . 

The parameters of the high-level and low-level policies in HIL are typically determined through three approaches: (1) Learning from demonstrations, which utilizes expert demonstrations to train both levels of policies; (2) Optimization, which applies RL or other optimization methods to refine the policies; and (3) Manual tuning, which manually adjusts policies during the initial stages or for specific task requirements. A key advantage of HIL is its ability to reduce the complexity of direct action-space search by decomposing tasks into hierarchical structures. This decomposition not only improves learning efficiency, particularly in long-horizon tasks, but also enhances generalization and task success rates by enabling optimization at multiple levels. 

_2) Research Progress:_ In recent years, HIL has made significant progress in task decomposition and skill generalization. CompILE [114] enhanced generalization in complex environments by decomposing tasks into independent subtasks, laying the foundation for subsequent work, particularly for tasks with long temporal dependencies. In dexterous manipulation, ARCH [116] integrated a low-level library of predefined skills with a high-level IL policy, enabling efficient skill composition and adaptation for complex, high-precision tasks. Meanwhile, Wan et al. [118] emphasized maintaining skill continuity and stability in dynamic environments by decomposing tasks into continuous sub-tasks and enabling adaptive policy transitions under varying conditions. 

To enhance scalability, recent research has increasingly explored automatic hierarchy discovery to reduce reliance on manually designed skill structures. Unsupervised skill segmentation methods have shown strong potential for identifying reusable sub-skills and task boundaries directly from raw data. For example, Gehring et al. [132] proposed hierarchical exploration strategies that use unsupervised clustering to learn 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

9 

multi-level reusable sub-policies. More recently, Jansonnie et al. [133] presented a skill discovery framework that leverages automatic task generation and asymmetric self-play to produce diverse manipulatory behaviors, which are then embedded into reusable primitives suitable for hierarchical policies. Similarly, contrastive learning approaches [134] discovered skills by maximizing mutual information across trajectory embeddings, resulting in more robust and generalizable skill representations. 

From a data-centric perspective, play data has been used to train both high-level and low-level policies. Wang et al. [119] proposed MimicPlay, which exploits unstructured human play interactions to learn high-level latent plans and trains a low-level visuomotor controller using only a small number of demonstrations. Lin et al. [120] introduced H2RIL, which extracts interaction-aware skill embeddings from task-agnostic play data and aligns them with human videos via temporal contrastive learning, enabling generalization to novel, composable tasks and adaptation to out-of-distribution scenarios. 

_3) Discussion:_ In summary, HIL has demonstrated significant advantages in task decomposition, skill generalization, and handling long-horizon tasks. By introducing hierarchical structures and multi-level control strategies, substantial progress has been made across various dexterous manipulation tasks. However, most current approaches still depend on manually designed hierarchies, which limit autonomy in unstructured or dynamic environments. Automatic hierarchy discovery methods, such as unsupervised skill segmentation or contrastive learning-based sub-task discovery, are essential for enabling robots to autonomously identify reusable skills and adapt their hierarchy to new tasks. Furthermore, ensuring robustness and continuity when skill libraries need to be updated or extended, particularly under changing task conditions, remains an open problem. 

## _E. Continual Imitation Learning_ 

_1) Description:_ Continual Imitation Learning (CIL) combines continual learning with IL to enable robots to continuously acquire and adapt new skills from expert demonstrations while avoiding the forgetting of previously learned knowledge when adapting to new tasks in dynamic environments. Specifically, in the initial phase, the agent learns fundamental skills from expert demonstrations. In subsequent phases, the agent incrementally accumulates knowledge, adapts to new tasks or environments, and mitigates the risk of forgetting previously acquired skills. 

In CIL, the policy _π_ is optimized by minimizing the cumulative imitation loss across all previously encountered tasks. The objective function is defined as: 


where _λ_ ( _i_ ) assigns a weight to each of the _t_ tasks, and _ρ_<sup>(</sup> exp<sup>_i_)denotesthedistributionofexpertstate-actionpairs.The</sup> core objective of CIL is to continuously refine the policy _π_ using new demonstrations while preserving performance on previously learned tasks. This is particularly challenging, as 

it requires balancing the acquisition of new skills without compromising the proficiency of previously acquired ones. 

_2) Research Progress:_ Various CIL approaches have been developed for dexterous manipulation, each aiming to balance memory retention and adaptation. Early studies [121] relied on storing large amounts of task data, leading to high storage and computational costs. To address this, task-specific adapter structures introduced lightweight, modular components for seamless task switching [122], though their performance declined when task variations are substantial. 

To address catastrophic forgetting more systematically, regularization-based methods [135] have gained prominence. For instance, Elastic Weight Consolidation (EWC) [136] penalized large updates to parameters critical for previously learned tasks by incorporating Fisher information into the loss function. Similarly, knowledge distillation-based approaches [137] preserved prior skills by encouraging new policies to mimic outputs from older policies. Rehearsal-based strategies offered another solution, such as experience replay, where past experiences or generated trajectories are interleaved with new task data to reduce forgetting [138]. Generative models, such as Deep Generative Replay (DGR), further alleviated storage constraints by synthesizing realistic task trajectories instead of storing raw data [124], although ensuring trajectory fidelity remains challenging. 

Beyond these, unsupervised skill discovery has been explored to improve adaptability and generalization [118]. It dynamically generated new skills and integrated them into the robot’s repertoire, but had yet to demonstrate robust realworld generalization. Unified policy learning via behavior distillation [123] provided an alternative by employing a single shared policy across tasks, eliminating the need for task-specific modules, though at the cost of increased task interference. Lastly, self-supervised learning techniques have shown promise in acquiring transferable skill abstractions without explicit demonstrations [125]. 

_3) Discussion:_ In summary, CIL for dexterous manipulation has explored a range of techniques, such as adapter-based methods, regularization approaches, knowledge distillation, rehearsal strategies, and generative models. These approaches collectively aim to mitigate catastrophic forgetting and enhance task-switching efficiency, but significant challenges remain. The effectiveness of regularization and knowledge distillation often depends on carefully balancing new and old task performance, which becomes difficult when tasks differ substantially. Similarly, the stability and performance of rehearsal or generative replay methods are highly sensitive to the quality and diversity of stored or synthesized data. Although modular adapters and regularization techniques have reduced memory demands, computational overhead and scalability continue to pose barriers for real-world deployment. 

## _F. Comparative Analysis of Imitation Learning Approaches_ 

While Table I outlines the general pros and cons of different IL approaches, the challenges inherent to dexterous manipulation amplify these limitations and deserve deeper 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

10 

TABLE II 

A COMPARISON OF IL METHODS IN COST, FEASIBILITY, EFFICIENCY, AND COMPLEXITY 

|**Category**|**Training Cost**|**Inference Latency**|**Sample Efficiency**|**Computational**<br>**Complexity**|**Real-Time Feasibility Notes**|
|---|---|---|---|---|---|
|**BC**|Low|Very Low (_<_1<br>ms)|Low–Moderate (requires<br>many demos; improves<br>with online correction)|Low|Highly suitable for high-DOF real-<br>time control; the main bottleneck is<br>data quality and covariate shift.|
|**IRL**|High|Low–Moderate<br>(1–5 ms)|Moderate–Low|High|Training is computationally expen-<br>sive; inference is feasible but may<br>require reward computation if de-<br>ployed online.|
|**GAIL**|High|Low–Moderate<br>(2–5 ms)|Moderate|High|Inference<br>is<br>lightweight<br>once<br>trained; training is unsuitable for<br>strict real-time constraints.|
|**HIL**|Moderate–High|Moderate (2–10<br>ms)|High (can reuse<br>sub-policies)|Moderate–High|Two-tier policy execution increases<br>latency; optimization is needed for<br>tight loops.|
|**CIL**|High|Moderate (2–8 ms)|Moderate–High|Moderate–High|Online adaptation may break hard<br>real-time constraints; feasible if<br>adaptation is offloaded.|


analysis. Table II summarizes the trade-offs between efficacy and computational complexity across imitation learning paradigms. BC offers a simple, data-efficient solution but is highly vulnerable to distribution shifts, where small deviations can rapidly compound into task failure. IRL addresses this by inferring expert reward functions to improve generalization, though designing meaningful rewards for complex tasks remains difficult and computationally intensive. GAIL combines the strengths of BC and IRL by adversarially matching expert behavior without explicit reward design, yet it often suffers from instability and mode collapse in multi-modal tasks. Structurally, Hierarchical IL builds on these methods by decomposing tasks into modular skill primitives, improving scalability and reusability; however, reliance on hand-crafted hierarchies limits adaptability to novel scenarios. Continual IL addresses the evolving nature of manipulation tasks by supporting incremental skill acquisition, but dynamic contact interactions increase the risk of catastrophic forgetting. In summary, BC is well-suited for short-horizon, data-rich settings, while IRL and GAIL provide more robust generalization when expert intent must be inferred. Hierarchical and continual strategies extend these foundations to support long-term skill composition and adaptation. As detailed in Table III, the optimization specifics and convergence behavior of imitation learning methods are analyzed. 

greater scalability by eliminating the need for explicit reward functions, but it is prone to instability and mode collapse, particularly in high-DoF or multi-modal tasks. (2) Another ongoing discussion centers on the trade-off between end-toend learning from raw observations and using intermediate representations. End-to-end learning simplifies the pipeline by directly mapping raw inputs to outputs, but it often requires large amounts of data and struggles with generalization, especially in complex tasks. In contrast, using intermediate representations, such as semantic keypoints, can improve efficiency and generalization by focusing on task-relevant abstractions. However, this approach introduces added complexity in terms of feature extraction and domain-specific design, increasing the computational burden. (3) A further debate concerns the trade-off between learning from expert demonstrations versus self-exploration. Learning from expert demonstrations (e.g., via BC or GAIL) can offer highly effective solutions by mimicking human-like actions, but it relies heavily on highquality expert data, which may be scarce or difficult to obtain. Self-exploration, however, allows the model to learn through trial and error, leading to greater flexibility in task environments. Yet, this approach often suffers from inefficiencies and a longer learning time, as it requires the agent to explore numerous states to achieve a sufficient understanding of taskspecific behaviors. 

In addition to these strengths and weaknesses, ongoing debates highlight critical trade-offs that influence their application in complex dexterous manipulation tasks. (1) A central debate revolves around the balance between simplicity and scalability. BC is simple and data-efficient, making it effective for tasks with lower complexity or shorter horizons, but it struggles with generalization in high-DoF dexterous manipulation tasks. In contrast, IRL and GAIL offer better generalization, with IRL excelling at capturing expert behavior for unseen states but facing scalability issues due to the challenge of reward design. GAIL, on the other hand, provides 

Hybrid strategies hold promise for achieving both robustness and scalability in complex, long-horizon tasks by integrating complementary strengths of different paradigms. A key direction involves integrating hierarchical planning with adversarial imitation by employing a high-level policy that generates symbolic or language-conditioned subgoals, while the low-level policy is optimized through adversarial learning to match expert trajectories under complex contact dynamics. This coupling allows the high-level controller to focus on long-horizon task composition while the low-level controller benefits from the sample efficiency and robustness 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

11 

TABLE III 

A COMPARISON OF IL METHODS BY OPTIMIZATION AND CONVERGENCE 

|**Method**|**Key Hyperparameters**|**Common Optimizers**|**Regularization Strategies**|**Convergence Behavior Notes**|
|---|---|---|---|---|
|**BC**|Learning rate, batch size, net-<br>work depth|Adam, RMSprop|L2 weight decay, dropout|Converges quickly; risk of overfitting<br>on small datasets; performance lim-<br>ited by covariate shift.|
|**IRL**|Reward<br>learning<br>rate,<br>policy<br>learning rate, discriminator up-<br>dates|Adam for policy & reward<br>networks|Entropy regularization, reward<br>clipping|Slower convergence due to reward<br>inference; reward shaping essential<br>for stability.|
|**GAIL**|Policy<br>LR,<br>discriminator<br>LR,<br>batch size, rollout length|Adam (policy & discrimina-<br>tor)|Gradient<br>penalty,<br>spectral<br>norm|Sensitive to discriminator–policy up-<br>date ratio; prone to oscillation with-<br>out tuning.|
|**HIL**|Subpolicy<br>LR,<br>meta-controller<br>LR, option horizon|Adam (separate for high- &<br>low-level)|Option<br>dropout,<br>inter-option<br>regularization|Convergence<br>depends<br>on<br>option<br>discovery quality; mitigates long-<br>horizon credit assignment.|
|**CIL**|Base LR, regularization strength<br>for knowledge retention, replay<br>buffer size|Adam, SGD with momen-<br>tum|Elastic Weight Consolidation<br>(EWC), replay-based regular-<br>ization|Trains<br>indefinitely<br>with<br>periodic<br>adaptation; stability–plasticity trade-<br>off crucial.|


of adversarial training in modeling fine-grained manipulation primitives. Another approach is embedding continual learning mechanisms into hierarchical architectures, enabling incremental skill acquisition while preserving previously learned behaviors through replay-based regularization or generative memory. Reward shaping derived from IRL can be combined with supervised BC objectives to improve generalization and reduce compounding errors in data-limited settings. Furthermore, hybrid systems can integrate meta-learning for rapid skill adaptation, while lightweight model-based modules, such as MPC for local corrections, complement model-free IL for enhanced stability and precision. 

An increasingly important aspect of hybrid IL strategies is the integration of model-based control with imitation learning, which is often underexplored. Model-based components, such as dynamics models or physics priors, can provide structured guidance for low-level policy optimization, reducing reliance on dense supervision or large datasets. For instance, MPC can be used to plan feasible trajectories or correct drift during execution, while the IL policy handles task-level reasoning and adaptation. Conversely, IL can help bootstrap model-based controllers in regions where dynamic models are inaccurate or data is sparse. This synergistic integration allows systems to exploit the strengths of both paradigms: the interpretability, adaptability, and safety of model-based control with the expressiveness and flexibility of data-driven IL. In real-world manipulation, where uncertainties and contact-rich dynamics are prevalent, such hybrid control strategies have shown promise in improving generalization, robustness, and sample efficiency. 

design principles, advantages, and trade-offs. Table IV provides a comparative analysis of the performance characteristics of these three end-effector types in dexterous manipulation. 

## _A. Two-fingered Traditional Gripper_ 

Two-fingered grippers are widely used for their reliability, simplicity, and ease of control. Typically driven by a single actuator with one DoF, they are cost-effective and suitable for repetitive tasks requiring consistency [139]. For example, [140] demonstrated a Franka robot with such a gripper performing tasks like setting a breakfast table. Similarly, Kim et al. [141] used a two-fingered gripper for behavior cloning with gaze prediction, and a tendon-driven variant in [142] showed the ability to grasp diverse household objects. 

Recent works have further extended gripper capabilities through large-scale imitation datasets such as MIME [143], RH20T [144], Bridge Data [145], and Droid [146]. Dualarm systems also enhanced manipulation by coordinating two grippers. For instance, [147] achieved banana peeling through dual-action IL. More complex tasks such as shrimp cooking, cloth folding, and dishwashing were demonstrated in Mobile ALOHA [148] and UMI [149]. 

Despite these advances, two-fingered grippers remain fundamentally limited in dexterous manipulation, which requires within-hand object reconfiguration [150]. Their simple structure and lack of internal DoFs restrict post-grasp adjustments [139]. Furthermore, morphological differences from the human hand hinder learning from demonstrations and prevent replication of human-like in-hand movements [151]. 

## _B. Multi-fingered Anthropomorphic Hand_ 

## IV. END-EFFECTORS FOR DEXTEROUS MANIPULATION 

An end-effector is a component at the tip of a robotic manipulator that directly interacts with the environment to perform tasks. In dexterous manipulation, end-effectors are typically categorized into two-fingered grippers, multi-fingered anthropomorphic hands, and three-fingered robotic claws. This section introduces these three types in order, highlighting their 

To overcome the dexterity limitations of two-fingered grippers, robotic hands with human-like morphology have been widely developed. These anthropomorphic hands are better suited for interacting with objects and environments designed for humans [152]. They can be typically classified by transmission mechanisms—tendon-driven, linkage-driven, directdrive, and hybrid systems—which fundamentally affect their performance characteristics [153], [154]. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

12 

TABLE IV 

COMPARATIVE PERFORMANCE OF THREE END-EFFECTOR TYPES IN DEXTEROUS MANIPULATION 

|**End-Effector**<br>**Type**|**DoF**|**Dexterity & Design**<br>**Notes**|**Actuation Prin-**<br>**ciple**|**Control**<br>**Precision**|**Adaptability**|**Cost**|**Typical Appli-**<br>**cations**|**Suitability for IL**|
|---|---|---|---|---|---|---|---|---|
|**Two-Fingered**<br>**Gripper**|1–2|Simple parallel jaws;<br>limited<br>in-hand<br>re-<br>configuration|Single-motor,<br>linkage or direct-<br>drive|Medium|Low|Low|Pick-and-place,<br>repetitive tasks|Low data demand,<br>easy to train, strong<br>generalization|
|**Three-Fingered**<br>**Robotic Claw**|6–9|Three opposed fingers<br>(Fig.4); hybrid under-<br>actuation<br>yields<br>cylindrical/spherical<br>grasps<br>with<br>modest<br>dexterity|Tendon-driven or<br>linkage + spring<br>coupling|Medium–<br>High|Medium|Medium|General grasp-<br>ing, limited in-<br>hand manipula-<br>tion|Moderate<br>data<br>demand,<br>balances<br>flexibility<br>and<br>training cost|
|**Multi-Fingered**<br>**Anthropomorphic**<br>**Hand**|15–25|Full five-finger layout<br>(Fig. 3); high DoF en-<br>ables human-like pre-<br>cision<br>and<br>fingertip<br>control|Remote<br>tendon,<br>direct-drive,<br>or<br>hybrid<br>transmissions|High|High|High|Medical proce-<br>dures, precision<br>assembly, com-<br>plex tasks|High data demand,<br>expensive<br>training,<br>limited<br>generaliza-<br>tion|


Fig. 3. Examples of multi-fingered anthropomorphic hands: (a) Shadow Dexterous Hand [155]; (b) Awiwi Hand [156]; (c) Biomimetic Hand [157]; (d) ILDA Hand [153]; (e) Hu et al.’s robotic hand [154]; (f) INSPIRE-ROBOTS RH56 Dexterous Hand [158]; (g) Linker Hand L20 [159]; (h) PUT-Hand [160]; (i) Allegro Hand [161]; (j) Faive Hand [162]; (k) Tesla Optimus Hand [163]; (l) Utah/MIT Dexterous Hand [164]. 

_1) Tendon-driven Approach:_ Tendon-driven hands use cable transmissions to actuate joints, mimicking human tendons. This design allows for compact structure, multiple DoFs, and high dexterity, making it a common choice in anthropomorphic hand development. To accommodate high DoFs, actuators are often remotely located in the forearm. 

Representative examples include the Utah/MIT Hand [164] 

(see Fig. 3(l)), the Shadow Dexterous Hand [165] (see Fig. 3(a)), and the Awiwi Hand [166]–[169] (see Fig. 3(b)), all of which adopt antagonistic tendon routing for biomimetic motion. The FLLEX Hand [170], [171] and Faive Hand [172] (see Fig. 3(j)) with rolling contact joints demonstrate robustness and ball-rolling manipulation, respectively. Other typical tendon-driven hands include the Robonaut R2 Hand [173], Valkyrie Hand [174], [175], UB Hand [176]–[178], DEXMART Hand [179], [180], iCub Hand [181], and Biomimetic Hand [182] (see Fig. 3(c)). 

While remote actuation reduces hand weight, it introduces friction and tendon wear due to long transmission paths. To address this, some designs embed all actuators within the palm. Examples include the DEXHand [183], SpaceHand [184], CEA Hand [185], and OLYMPIC Hand [186], which prioritize modularity and compact integration. Commercial designs like DexHand 021 [187], Tesla Optimus Hand [188] (see Fig. 3(k)) and PUDU DH11 Hand [189] also follow this approach. 

Despite their advantages in dexterity and anthropomorphism, tendon-driven hands face challenges such as friction loss [190], [191], end termination [168], [192], [193], tendon creep and wear [194]–[196], which impact durability and reliability. As a result, most remain within research settings, with limited deployment in real-world industrial applications. 

_2) Linkage-driven Approach:_ Linkage-driven hands use rigid mechanical linkages to control joint motion, offering high precision, repeatability, and robustness. Compared to tendondriven designs, they generally provide fewer DoFs but benefit from simpler, more reliable actuation. As a result, most commercial prosthetic and robotic hands adopt this mechanism. Due to space constraints and the demand for compactness, most linkage-driven fingers are actuated by a single motor and fall into two main categories: one-DoF coupled and multi-DoF underactuated types [197]. 

In the one-DoF type, joints are mechanically coupled, so preshaping remains fixed during flexion. Typical designs include the S-finger with inverse four-bar coupling [198] and the humanoid hand by Liu et al. using two four-bar linkages per finger [199]. Similar configurations appear in hands like the INSPIRE-ROBOTS RH56 [158] (see Fig. 3(f)), Bebionic Hand [200], [201], BrainRobotics Hand [202] and OYMotion 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

13 

OHand [203]. 

In contrast, underactuated fingers can adapt to contact forces, enhancing grasp adaptability. Examples include the Southampton Hand with a Whiffle tree mechanism [204], the LISA Hand using linkage-based self-adaptation [205]; MORA HAP-2 Hand [206], AR Hand III [207], and Cheng et al.’s prosthetic hand [208] with multi-bar or four-bar adaptive linkages. 

While most designs use one motor per finger, a few incorporate multiple actuators for higher dexterity. The ILDA Hand [153] (see Fig. 3(d)) employs three motors per finger with combined PSS/PSU chains and four-bar linkages, achieving workspace and fingertip force comparable to human hands. Similar high-DoF linkage designs appear in the Linker Hand L20 [159](see Fig. 3(g)), AIDIN ROBOTICS Hand [209] and the RY-H1 Hand [210]. 

_3) Direct-driven Approach:_ Direct-drive hands eliminate intermediate transmission by connecting actuators directly to joints. This simplifies the mechanical structure while still allowing for high actuatable DoFs, similar to tendon-driven designs. 

Representative examples include the OCU-Hand [211] with 19 DoFs, where most joints are individually driven by embedded DC motors, and the TWENDY-ONE hand [212], which achieves 13 DoFs via joint-level motor placement. The KITECH-Hand [213], Allegro Hand [161] (see Fig. 3(i)) and LEAP Hand [214] adopt modular finger designs, integrating motors directly into the phalanges. The LEAP Hand also introduces a novel universal abduction-adduction motor configuration for enhanced MCP joint flexibility. 

While direct drive offers high control precision and responsiveness, it introduces potential drawbacks such as increased mass, rotational inertia, and finger bulkiness, which may hinder agility in fine manipulation tasks. These limitations partly explain why most direct-drive hands adopt a four-finger configuration. 

_4) Hybrid-transmission Approach:_ In addition to the transmission types introduced above, many anthropomorphic hands adopt hybrid schemes to integrate the advantages of different approaches. 

For example, the DLR/HIT Hand II [215] and NAIST Hand [216] use modular fingers with a combination of motors, belts, gears, tendons, or linkage systems. The MCR-Hand series [217], [218] utilizes a linkage-tendon mixed transmission system to achieve compactness and high functionality. Adab Mora Hand [219], LEAP Hand V2 (DLA Hand) [220], and Hu et al.’s hand [154] (see Fig. 3(e)) also integrate multiple transmission elements within fingers to enhance overall performance and adaptability. 

Other hybrid designs explicitly differentiate mechanisms across fingers to match specific functional needs. The PUTHand [160] (see Fig. 3(h)), for instance, combines a directdrive thumb, linkage-driven index/middle fingers, and tendondriven ring/little fingers. Similarly, the MPL v2.0 Hand [221], Tact Hand [222], and Six-DoF Open Source Hand [223] adopt direct or geared actuation for the thumb while using tendons, linkages or timing belts for other fingers. Hands developed by Owen et al. [224], Ryu et al. [225], and Ke et al. 

[226] follow a similar approach, implementing thumb-specific hybrid strategies to enhance opposability and dexterity. 

## _C. Three-fingered Robotic Claw: A Trade-off Solution_ 

The diversity of anthropomorphic hand designs largely stems from a fundamental trade-off between mechanical simplicity and dexterous capability [229]. While the human hand has over 20 DoFs [230]–[236], replicating this complexity mechanically remains impractical. Higher dexterity often increases structural and control complexity, cost, and susceptibility to failure [228], [237], [238], limiting the feasibility of high-DoF hands in real-world applications [239], [240]. 

To mitigate these issues, several simplification strategies are adopted: underactuation with elastic components [155], [163], [204], [205], [237], [238], reducing non-essential DoFs or phalanges [158], [163], [200], [203], or even omitting a finger entirely [161], [164], [174], [183], [212], [214]. These approaches highlight the challenge of maximizing functionality within practical constraints. 


Fig. 4. Examples of three-fingered robotic claws: (a) DEX-EE [241]; (b) BarrettHand [227]; (c) i-HY Hand [228]; (d) DoraHand [242]. 

As a compromise between the minimalist two-fingered gripper and complex multi-fingered anthropomorphic hands, the three-fingered robotic claw offers a functional middle ground. Though not anatomically human-like, three fingers are sufficient for executing common grasp types such as cylindrical and spherical power grasps [228], and can support a subset of in-hand manipulation tasks. 

Numerous three-fingered claws have demonstrated impressive capabilities. For example, Shadow’s DEX-EE [241] (see Fig. 4(a)) and the TRX Hand [243] exhibited high robustness and dexterity. The BarrettHand [244] (see Fig. 4(b)) achieved adaptive grasping through underactuation. Tendondriven designs like the i-HY Hand [228] (see Fig. 4(c)) and Model O [245] enabled actions such as pivoting and precision transitions. Systems such as DClaw [246] and TriFinger [247] were capable of performing fine manipulation tasks via RL. Other novel architectures include linkage-based [248], motormultiplexed [249], and link-belt-integrated claws [250], each offering different characteristics. 

Three-fingered claws such as the DoraHand [240] (see Fig. 4(d)), SARAH [251], D’Manus [252], and Kinova Jaco’s claw [253] further demonstrated the practicality and versatility of this design choice in both research and assistive applications.Based on the foregoing analysis, the key characteristics of representative robotic hands across the three end-effector categories are summarized in Table V. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

14 

TABLE V KEY CHARACTERISTICS OF REPRESENTATIVE ROBOTIC HANDS 

|**Robotic Hand**|**DoF (actuated /**<br>**total)**|**Actuation Type**|**Key Feature**|**Typical Applications**|
|---|---|---|---|---|
|**Shadow Dexterous**<br>**Hand [155]**|20 / 24|Remote tendon-driven (20<br>Smart Motors in forearm)|Fully biomimetic; 129 sensors;<br>_±_1° joint precision|High-dexterity<br>research,<br>tele-<br>operation, AI/ML benchmarking|
|**Allegro Hand [161]**|16 / 16|Direct-driven (Maxon DC<br>motors in each phalanx)|Modular finger units; ROS-<br>native; low backlash|Academic RL/IL experiments, sim-<br>to-real transfer|
|**Linker Hand (L20)**<br>**[159]**|16 / 21|Linkage-driven<br>(4<br>motors<br>per finger)|ROS-native;<br>piezoresistive<br>sensors; optional visual-tactile<br>perception|High-dexterity<br>research,<br>Industrial<br>applications|
|**BarrettHand (BH8-280)**<br>**[227]**|4 / 7|Linkage-driven (1 motor per<br>finger + spread)|Under-actuated adaptive fin-<br>gers; rugged mechanics|Industrial grasping, pick-and-place,<br>educational labs|
|**LEAP Hand [214]**|16 / 16|Direct-driven (compact joint<br>motors)|Low-cost,<br>open-source,<br>anthropomorphic<br>yet<br>lightweight|Learning-focused<br>projects,<br>mobile<br>manipulation|
|**i-HY Hand (3-finger)**<br>**[228]**|9 / 9|Tendon-driven (elastic ten-<br>dons + capstan)|Compliant,<br>under-actuated;<br>high-impact robustness|Robust in-hand manipulation, field<br>robotics|


## _D. Tactile Sensors on Dexterous End-effectors_ 

Tactile sensing is important for enhancing the perception and control capabilities of robotic end-effectors, particularly in dexterous manipulation tasks that require fine contact interaction, compliance, and force regulation. Although previous endeffectors such as two-finger grippers and parallel jaw mechanisms often rely solely on vision or position feedback, modern multi-fingered dexterous hands [254], [255] are increasingly incorporating high-resolution tactile sensors to achieve more stable and versatile manipulation in unstructured or dynamic environments. 

In general, tactile sensors provide direct measurements of contact force, pressure distribution, slip, surface texture, and sometimes even temperature or material properties. They are typically mounted on the fingertips, phalanges, or palm surfaces of robotic hands, allowing feedback-rich control policies such as force modulation, slip prevention, and adaptive grasping. In recent years, tactile sensors have become essential for learning-based approaches, where tactile data are used for contact state estimation, affordance recognition, and policy refinement [256]–[259]. 

Tactile sensors can be broadly categorized into several types based on sensing principles: 

- Resistive and Capacitive Tactile Sensors: These are thin, flexible, and cost-effective, and detect pressure changes through variations in electrical resistance or capacitance. They are widely used in fingertip arrays and robotic skin [260]–[262]. 

- Piezoelectric Sensors: These generate voltage in response to applied stress and are suitable for dynamic contact detection, such as impact and slip sensing [263], [264]. 

- Optical and Vision-Based Tactile Sensors: Examples such as GelSight [265], TacTip [266], and GelStereo tip [267] use internal cameras and deformable gel surfaces to reconstruct high-resolution 3D contact geometry. These sensors offer rich, interpretable data and are increasingly used in learning-based manipulation [268]. 

- Magnetic and Hall Effect Sensors: Often embedded 

within soft materials or joints, these detect local deformations or forces via magnetic field changes [269]–[272]. 

- Bio-inspired Sensors: Inspired by human skin or mechanoreceptors, these sensors aim to capture multimodal tactile features (e.g., pressure + vibration + shear) in compact designs. Examples include BioTac [273], NeuTouch [274], and GTac [275]. 

The integration of tactile sensing into robotic hands offers significant advantages. First, it enables robust manipulation under conditions of visual occlusion or low illumination by relying solely on contact feedback. Second, tactile sensors facilitate adaptive grasping strategies such as regrasping, forcelimited lifting, and slip compensation. Third, tactile data contribute to improved grasp quality estimation, object property inference, and planning for in-hand manipulation. However, tactile sensing also faces several challenges. Calibration and drift over time, especially in soft or flexible sensors, can reduce measurement fidelity. High-resolution sensors (e.g. GelSight [265]) are relatively bulky and have limited durability under repeated contact. Furthermore, real-time integration of tactile data into control pipelines demands efficient signal processing, accurate contact modeling, and often machine learning-based interpretation. 

In the context of IL for dexterous manipulation, tactile sensing provides a rich stream of contact information that complements visual and proprioceptive cues. Demonstrations collected from expert teleoperation or kinesthetic teaching can include synchronized tactile signals, allowing the learning agent to capture subtle contact events, such as incipient slip, rolling, or micro-adjustments of finger force, that are often invisible to vision alone. By incorporating tactile feedback into the policy representation, IL systems can better generalize to novel objects and adapt to variations in shape, compliance, or surface texture. Recent work [257], [276]–[278] showed that tactile-informed IL can substantially improve grasp stability, reduce failure rates under visual occlusion, and enable fine in-hand reorientation without explicit object models. 

Overall, tactile sensors are becoming an indispensable com- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

15 

ponent of dexterous robotic end-effectors, bridging the gap between perception and control. Future research is expected to focus on developing scalable, durable, and multimodal tactile arrays, as well as fusing tactile signals with vision and proprioception to support generalizable manipulation policies in open-world environments. 

## _E. Impact of End-effector Design on Imitation Learning Performance_ 

While prior research has primarily focused on algorithmic innovations, the influence of end-effector morphology, actuation, and sensor configuration on IL performance has received comparatively limited attention. These factors can significantly affect data efficiency, policy generalization, and task success rate through the following mechanisms. 

_1) Morphology: Redundant Degrees of Freedom and Ergonomic Alignment._ High-DoF hands (e.g., Shadow Hand, 20+ DoF) can replicate fine human manipulations such as fingertip control, but they increase the dimensionality of the action space, leading to severe sparsity issues in IL. The RH20T dataset [144] showed that the demonstration data requirement for high-DoF hands grows exponentially. In contrast, threefingered grippers (e.g., DoraHand [240]) traded off some dexterity for reduced policy learning complexity, achieving better zero-shot generalization in cross-domain tasks such as those in BridgeData V2 [279]. Anthropomorphic hands (e.g., ILDA Hand [153]) with geometric consistency to the human demonstrator’s workspace reduced cross-domain mapping errors. Antotsiou et al. [23] highlighted that differences in morphology, degrees of freedom, and joint constraints between the human hand and the robot hand can amplify retargeting errors and consequently raise the likelihood of task failure. 

_2) Actuation: Trade-Offs Between Transmission Dynamics and Controllability._ Hands such as the Shadow Hand use tendon-driven actuation, where compliance introduces nonlinear friction and hysteresis, increasing noise in the action–state mapping of demonstration data. Tendon-driven systems introduce nonlinearities such as friction and hysteresis in the transmission chain, which degrades control fidelity in dexterous manipulators [192]. Rigid linkage actuation (e.g. BarrettHand [227]) reduces dynamic errors, but underactuated designs (e.g. adaptive grasping) limit the reproduction of fine finger motions. Direct-drive hands (e.g. LEAP Hand [214]) achieve millimeter-level control precision through joint-level motors but suffer from increased inertia due to motor mass, requiring IL policies to learn dynamic feedforward compensation. 

_3) Sensor Configuration: Complementarity in Multimodal Perception._ High-resolution tactile sensing (e.g., GelSight [265]) can capture micro-force adjustments and slip signals in human demonstrations, significantly improving IL’s understanding of contact dynamics. Huang et al. [257] reported that removing tactile input causes task success rates to plummet to near-random levels, underscoring the critical importance of tactile information for successful multi-object in-hand manipulation. Differences in sampling frequency (e.g., vision at 30 Hz vs. tactile sensing at 1 kHz) introduce synchronization challenges. Lin et al. [285] addressed this via a cross-modal 

alignment network, reducing motion consistency error by 25% in bimanual coordination tasks. NeuralFeels [280] aligned vision with tactile streams via global timestamps and fuses both modalities in a joint neural implicit field, cutting trajectoryconsistency error by 25% for precise in-hand manipulation. 

Future end-effector designs should follow a “task–morphology–algorithm” co-optimization paradigm. High-dexterity tasks (e.g., surgical suturing) favor fully actuated hands with dense tactile arrays (e.g., Shadow Dexterous Hand [155]) and employ hierarchical IL frameworks [76] to mitigate the curse of dimensionality. Low-cost generalization tasks (e.g., household tidying) use three-fingered grippers with vision-dominant sensing, combined with domain randomization [281] to improve cross-object robustness. Real-time collaboration tasks (e.g., human–robot co-manipulation) balance actuation latency and control precision. For instance, RAPID Hand [282] achieved _<_ 7 ms response delay through a lightweight design. 

## V. DEXTEROUS MANIPULATION WITH TELEOPERATION AND VIDEO DEMONSTRATION 

This section discusses two main approaches to dexterous manipulation: acquiring demonstration data through teleoperation and learning directly from demonstration videos. Teleoperation facilitates direct human control over robotic systems, leveraging human expertise for learning complex manipulation tasks, while video-based learning harnesses rich visual data to enable autonomous skill acquisition from natural human demonstrations. Together, these approaches address challenges in teaching robots fine-grained manipulation behaviors across diverse scenarios. The section further discusses datasets and benchmarks in supporting imitation learning frameworks that underpin these methodologies. 

Teleoperation systems provide a robust interface for humanrobot collaboration, benefiting from directly making robot behaviors comply with human-level intelligence, which refers to _human-in-the-loop_ . This approach is highly intuitive since humans’ extensive knowledge and experience empower them to make informed judgments on diverse tasks across complex scenes and to promptly adjust strategies in response to feedback. Due to this usability, teleoperation is widely applied in various fields. Additionally, by collecting data on the robot’s states and corresponding actions during teleoperation, datasets can be constructed to perform end-to-end IL. 

Learning dexterous manipulation skills from demonstration videos offers a promising alternative to teleoperation by leveraging abundant visual data to teach robots complex behaviors. Unlike direct control, video-based learning enables robots to observe human experts performing tasks in diverse and unstructured environments, capturing rich contextual and temporal information. Advances in computer vision and representation learning facilitate extracting meaningful features from raw videos, which can be mapped to robot actions through imitation learning frameworks. This approach not only reduces the reliance on specialized teleoperation hardware but also broadens the scalability of training data, ultimately enabling robots to acquire fine-grained manipulation capabilities from natural human demonstrations. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

16 

TABLE VI 

COMPARISON OF TELEOPERATION-BASED DATA COLLECTION APPROACHES 

|**Approach**|**Key Characteristics**|**Advantages**|**Limitations**|
|---|---|---|---|
|**Vision-Based Systems**<br>[17]–[20], [83], [119],<br>[283]–[286]|_•_ Non-contact image-based motion<br>capture<br>_•_ Single or multi-camera configura-<br>tions<br>_•_ RGB or RGB-D inputs, frequently<br>accompanied by hand pose esti-<br>mation|_•_ Low-cost hardware (especially<br>single camera)<br>_•_ Easy to deploy and user-friendly<br>_•_ No wearables required|_•_ Susceptible to occlusion and lighting con-<br>ditions<br>_•_ Limited 3D precision and depth estima-<br>tion<br>_•_ Latency due to vision processing|
|**Mocap Gloves** [16],<br>[287], [288]|_•_ Wearable gloves with IMUs, flex<br>sensors, or magnetic sensors<br>_•_ Real-time hand joint tracking<br>_•_ Often used with external cameras<br>or LiDAR|_•_ High<br>joint-level<br>accuracy<br>(millimeter-level)<br>_•_ Fast response time<br>_•_ Robust under varied visual con-<br>ditions|_•_ High equipment cost<br>_•_ Requires calibration and setup<br>_•_ Potential discomfort for extended use|
|**VR/AR Controllers** [14],<br>[288]–[293]|_•_ Head-mounted display with spa-<br>tial tracking<br>_•_ Hand-held controllers with 6-DoF<br>input<br>_•_ Immersive virtual environments|_•_ Intuitive and interactive control<br>_•_ Multimodal feedback (e.g., vi-<br>sual and occasional haptic)<br>_•_ Consumer-grade accessibility|_•_ Dependence on virtual environments<br>_•_ Challenging<br>deployment<br>and<br>non-<br>negligible control latency<br>_•_ Limited haptic realism and force feed-<br>back|
|**Exoskeleton and**<br>**Bilateral Systems** [82],<br>[148], [149], [294]–[298]|_•_ Direct joint-space mapping<br>_•_ Includes bilateral force and torque<br>feedback<br>_•_ Leader-follower robot configura-<br>tions|_•_ High-fidelity control suitable for<br>precision tasks<br>_•_ Enables tactile interaction and<br>real-time feedback|_•_ Complex and bulky setups<br>_•_ Expensive hardware and maintenance<br>_•_ Restricted operator mobility|


## _A. Teleoperation Systems for Dexterous Manipulation_ 

A typical teleoperation system consists of two main components: the local site and the remote site, as demonstrated in Fig. 5. The local site includes a human operator and a suite of interactive I/O devices. The output devices provide real-time status about the remote robot and its surrounding environment, while the input devices allow the operator to issue commands in diverse forms, thereby controlling the remote robot’s actions. The remote site primarily contains the robot itself, which is equipped with various sensors to gather perceptions of its state and the surrounding environment. Upon receiving teleoperation commands from humans, the robots can perform the corresponding actions and complete tasks. 

To accurately convey human operators’ intentions to robotic systems, previous works have employed a wide range of human-robot interaction devices. Human operators with work experience can easily identify the current state of a robot through the image; however, accurately translating human instructions to robot actions remains a challenge. Some traditional controllers act on this: 1) joysticks [299] 2) haptic devices [300]; However, manipulation tasks often involve delicate movements and complex interactions, such as grasping, moving, and positioning small or irregularly shaped objects. These tasks necessitate devices that can offer dexterous interfaces to ensure the safety and efficacy of the robot’s actions. Precision and real-time feedback are crucial. Commonly used devices include: 1) cameras [17]–[20], [83], [283]–[285], [301]; 2) mocap gloves [287], [302]–[306]; 3) VR/AR controllers [14], [27], [83], [289], [291], [307]–[313]; 4) exoskeletons and bilateral systems [82], [148], [294], [296]– [298]. A comparative summary of representative teleoperation approaches is presented in Table VI, highlighting their key characteristics, advantages, and limitations to facilitate effective human-robot interaction. 

_1) Vision-based Teleoperation Systems:_ Recently, advancements in computer vision have led to the development of vision-based teleoperation systems. However, their accuracy in capturing hand movements is often compromised by factors such as occlusion, lighting, resolution, background, and inaccurate 3D estimation issues. Several methods have been proposed for robust hand pose estimation and reliable mapping to the robot end-effector. Li et al. [283] developed a visionbased teleoperation system by training TeachNet on pairs of images of human hands and simulated robots to form mappings between a human hand and a robotic Shadow Hand in the latent space. Dexpilot [18] utilized a calibrated multicamera system to estimate hand poses to teleoperate an Allegro Hand. Riemannian Motion Policies (RMPs) are employed to compute the Cartesian pose of the hand, facilitating handarm motion control. Subsequent approaches, such as Robotic Telekinesis [17] and DIME [83], simplified requirements to a single RGB camera, thus reducing the need for calibration. This is achieved through a general mapping method between humans and robots that have different kinematic structures. Additionally, Robotic telekinesis [17] adjusted the position and orientation of the end-effector relative to its base using the relative position and direction of the human wrist to the torso, enabling the teleoperation of both arm and hand. However, these methods still suffer from occlusion issues due to the single fixed camera setting. To solve this problem, Transteleop [284] introduced a system that utilizes real-time active vision with a depth camera mounted on the end-effector of the remote UR5 robot arm. During teleoperation, this robot arm can reposition the camera to enhance its field of view and improve hand pose estimation accuracy. 

The morphology discrepancy between the human hand and the robot hand might impede the operator from intuitively controlling the robot. To address this, Qin et al. [20] devel- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

17 


Fig. 5. Teleoperation frameworks and commonly used devices: (a) mocap gloves, (b) VR controllers, (c) joystick, (d) RGB-D camera, (e) exoskeleton, (f) dexterous hand, (g) dual-arm robot, (h) single-arm robot. 

oped a user-friendly interface by constructing a customized robotic hand modeled after the specific shape of a human hand. Demonstrations performed with this customized robot hand can be directly transferred to any dexterous robot hand. AnyTeleop [19] proposed a solution to the self-occlusion problem by integrating images from multiple cameras, each offering different perspectives. To further enhance precision in observation, ACE [285] mounted the camera under the endeffector of the exoskeleton to maintain a clear view of the hands and wrists. MimicPlay [119] employed two calibrated cameras in different viewpoints to reconstruct 3D hand locations. The teleoperation data for the robot was collected using the RoboTurk system [286], which operated via an IMUequipped smartphone. 

_2) Mocap Gloves:_ Motion capture systems typically utilize stable hardware devices such as multi-camera setups with markers, IMU sensors, and RGB-D cameras. These devices are robust against changes in lighting, occlusion, and complex backgrounds. Mocap gloves collect human hand motion data directly via sensors, enabling ideal real-time performance and significantly improving data collection efficiency in teleoperation. Although motion capture gloves are expensive, they provide precise hand tracking [287]. Wang et al. [16] introduced DexCap, a portable motion capture system. It includes a mocap glove for accurate finger joint tracking, a single-view camera for 6-DoF wrist pose tracking, and an RGB-D LiDAR camera for observing the surrounding 3D environment. With this precise 3D hand motion data, the proposed DexIL system can effectively learn bimanual dexterous manipulation skills. The remote system features two Franka Emika robotic arms, each with a LEAP dexterous robotic hand. Similarly, Mosbach et al. [288] used the SenseGlove DK1, a force-feedback glove, to capture hand joint movements, with hand tracking facilitated by a camera mounted on a headset. 

_3) VR/AR Controllers:_ VR devices typically include a headmounted display, a tracking system, and input devices. The head-mounted display provides an immersive visual experience with high-resolution screens and head motion tracking. The tracking system captures the user’s movements to ensure that interactions in the virtual environment correspond to realworld actions. Input devices, such as controllers or gloves, facilitate user interaction within the virtual space. Zhang et al. [14] developed a teleoperation system using consumergrade VR devices to control a PR2 robot. Following this, 

methods utilizing low-cost equipment [289], [290] demonstrated high-quality teleoperation through mixed reality. To streamline scene construction, Mosbach et al. [288] explored VR teleoperation in simulated environments for manipulation tasks. Recently, Bunny-VisionPro [291] equipped the Apple VisionPro with a haptic module to provide tactile feedback. Similarly, Open-television [292] used an active camera mounted on a humanoid robot to capture first-person stereo videos. This approach enhances the robot’s ability to perform precise and context-aware actions by providing a dynamic, real-time visual perspective similar to human vision. Lin et al. [293] introduced a low-cost teleoperation system, HATO, combining two Psionic Ability Hands for prosthetic use with UR5e robot arms. The system utilizes two Meta Quest 2 VR controllers with IMU sensors to capture hand spatial positions and orientations, translating controller inputs into multi-fingered hand poses. 

_4) Exoskeleton and Bilateral Systems:_ The majority of the aforementioned methods focus on manipulating the robot’s end-effector in task space in Cartesian coordinates. While setting the robot’s end-effector position is convenient, it has drawbacks. For robots with multiple DoF, computationally demanding inverse kinematics (IK) calculations are required, which can be problematic in real-time control scenarios. These complexities may cause response delays and compromise operational precision. Furthermore, singularities in the motion trajectory may lead to indeterminate or nonexistent IK solutions, resulting in control failures. In the following sections, we discuss studies that aim to synchronize human and robot movements in the joint space. 

Exoskeletons are wearable devices that gather and analyze user motion data. Fabian [294] developed a lightweight exoskeleton, DE VITO, for measuring human arm movements to teleoperate the mobile robot DE NIRO [295]. AirExo [296] presented a framework for whole-arm dexterous manipulation adaptable to different robot arms using interchangeable 3Dprinted components for robots divergent in morphology. 

Another approach involves a bilateral framework, where the movements of the leader robot are mirrored by the follower robot. Any resistance or force encountered by the follower is communicated back to the leader, enabling precision and tactile sensation tasks. Kim et al. [297] developed a controller with Denavit-Hartenberg parameters matching the teleoperated dual-arm robot alongside a calibration method to reduce grav- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

18 

TABLE VII 

COMPARISON OF VIDEO-BASED IMITATION LEARNING APPROACHES 

|**Method Category**|**Representative Method**|**Data Source**|**Key Characteristics**|
|---|---|---|---|
|**Motion-centric Imitation**<br>**Learning**|_•_ DexMV [314]<br>_•_ Robotic Telekinesis [17]<br>_•_ Track2Act [315]|_•_ Unlabeled<br>third-person<br>real-world<br>videos<br>_•_ Unlabeled<br>third-person<br>unpaired<br>videos<br>_•_ Unlabeled videos, limited real-world<br>data|_•_ Reconstructs 3D hand-object trajectories<br>or end-effector trajectories from videos<br>and maps them to robot actions, en-<br>abling cross-domain imitation and im-<br>proved generalization.|
|**Synthetic Video for Policy**<br>**Learning**|_•_ Gen2Act [316]<br>_•_ NIL [317]|_•_ Text-generated unlabeled synthetic<br>videos<br>_•_ Diffusion-generated unlabeled visual<br>videos|_•_ Uses language-conditioned video gener-<br>ation to synthesize training demonstra-<br>tions, removing the need for expert data.<br>_•_ Learns policies via perceptual similarity<br>in generated videos, supporting large-<br>scale training and generalization.|
|**Representation Learning for**<br>**Generalization**|_•_ Ag2Manip [318]|_•_ Unlabeled human action videos|_•_ Learns agent-agnostic action embeddings<br>to support imitation across different robot<br>embodiments and improve generaliza-<br>tion.|
|**Task-specific Architectures and**<br>**Learning Objectives**|_•_ Bi-KVIL [319]<br>_•_ Rank2Reward [320]<br>_•_ ViViDex [321]|_•_ Unlabeled<br>third-person<br>dual-hand<br>videos<br>_•_ Unlabeled videos<br>_•_ Unlabeled<br>noisy<br>videos<br>with<br>no<br>ground-truth state|_•_ Specialized frameworks modeling biman-<br>ual coordination, reward learning without<br>labels, and hierarchical learning architec-<br>tures for robust imitation.|


itational errors. For demonstrations without real robots, the controller uses force/torque sensors identical to those in real robots to provide force feedback. Recently, employing costeffective arms with comparable size as leaders and followers, ALOHA [82] utilized structurally analogous robotic arms with identical joint spaces for teleoperation. Expanding upon this concept, Mobile ALOHA [148] integrated the system with an automated guided vehicle to establish a whole-body teleoperation system. GELLO [298] reduced costs by replacing the real robotic arms at the local site with scaled kinematically equivalent 3D-printed parts, achieving one-to-one joint mapping. After that, UMI [149] further eliminated the need for physical robot arms by using hand-held grippers, providing a more portable interface for in-the-wild data collection. 

Differing from specific robot methods, AnyTeleop [19] introduced a unified system supporting multiple robot arms and dexterous hands through a general human-robot hand retargeting method. This system supports different arms by generating trajectories based on the estimated Cartesian end-effector pose. ACE [285] developed a cross-platform visual-exoskeleton teleoperation system compatible with diverse robot hardware, including various end-effectors such as grippers and multifinger hands, offering flexibility. Its exoskeleton arm features high-resolution encoders for precise joint position readings, ensuring accurate end-effector tracking. 

Assessing teleoperation interfaces requires considering both interface fidelity and the quality of collected demonstrations. Key evaluation criteria include spatial and temporal tracking precision, the consistency between operator commands and robot execution under communication latency, control bandwidth, and the resolution of feedback. Demonstration quality is typically reflected in task success rate, trajectory smoothness, and the frequency of effective error recovery during operation. An important downstream measure is the interface- 

to-policy transfer efficiency, which captures how interface characteristics influence the performance and generalization of imitation learning policies. Interfaces with high fidelity and low latency generally enable richer demonstrations and yield superior policy performance in fine-grained manipulation tasks, while lower-bandwidth and less complex interfaces may be sufficient for coarse and high-level motion primitives. Incorporating these metrics together with empirical evidence provides a principled basis for interface comparison, supporting data collection strategies that balance hardware complexity, operator skill, and final policy effectiveness. 

_B. Learning from Video Demonstrations for Dexterous Manipulation_ 

Video-based demonstration learning offers a promising solution to the challenge of acquiring robotic manipulation skills in the absence of expensive expert demonstrations. Table VII presents a summary of representative methods in this paradigm. By extracting structured behavioral cues from a range of human videos including recorded, synthetic, and websourced data, these methods transform raw visual observations into robot-interpretable representations, facilitating robust generalization across diverse tasks, objects, and embodiments. 

_1) Motion-centric Imitation Learning:_ A major line of work adopt motion-centric imitation, where human hand–object interactions were converted into robot-executable trajectories. Qin et al. [314] proposed a method that reconstructed 3D hand–object poses from third-person human videos and re-targeted them to dexterous robot hardware, enabling high-fidelity policy learning without the need for direct teleoperation or egocentric demonstrations. Building upon this approach, Bharadhwaj et al. [315] predicted objectrelative end-effector trajectories from unstructured videos and fine-tune residual policies on robots, thereby achieving 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

19 

TABLE VIII 

CATEGORIZATION OF BENCHMARK DATASETS FOR ROBOTIC IMITATION LEARNING 

|**Method Category**|**Representative Datasets**|**Scale**|**Sensory Modalities**|
|---|---|---|---|
|**Human-teleoperated Datasets**|_•_ MIME [143]<br>_•_ RH20T [144]<br>_•_ BridgeData [145]<br>_•_ BridgeData V2 [279]|_•_ 8,260 demos, 20 tasks<br>_•_ 110K+ multimodal sequences<br>_•_ 7,200 demos, 71 tasks, 10 domains<br>_•_ 60,096 trajectories, 24 environments|_•_ RGB-D, Kinesthetic trajectories<br>_•_ RGB-D, Audio, Tactile, Proprioception<br>_•_ Egocentric vision, Action sequences<br>_•_ Vision, Language embeddings|
|**Augmented Datasets**|_•_ RoboAgent [322]|_•_ 7,500 →98K* augmented trajectories|_•_ RGB, Semantic masks|
|**Synthetic Datasets**|_•_ MimicGen [323]|_•_ 200 →50K synthesized demos, 18 tasks|_•_ Object poses, Motion primitives|
|**Dexterous and Bimanual**<br>**Manipulation Datasets**|_•_ ARCTIC [324]<br>_•_ DexGraspNet [325]<br>_•_ OAKINK2 [326]|_•_ 2.1M frames (3D meshes)<br>_•_ 1.32M grasps, 5,355 objects<br>_•_ 627 sequences, 4.01M frames|_•_ Multi-view RGB, Contact dynamics<br>_•_ Tactile sensing, Physics simulation<br>_•_ Multi-view capture, 3D pose annotations|


*RoboAgent employs semantic-preserving augmentation techniques to scale demonstrations 

generalization across novel scenes and object configurations with minimal real-world training. Complementary to these approaches, Sivakumar et al. [17] directly mapped unstructured human hand motions from third-person videos to dexterous robotic hands, supporting real-time teleoperation without paired demonstrations. 

_2) Synthetic Video-driven Imitation Learning:_ Another direction leverage synthetic video as training signals for policy learning. Bharadhwaj et al. [316] proposed a method that generated realistic manipulation videos from textual prompts and internet instructions, which were then employed to train robot policies capable of generalizing to unseen categories and actions. Building upon this approach, Albaba et al. [317] introduced a diffusion-based video generation framework that replaced explicit action labels with perceptual similarity, providing a scalable pathway for training robots with diverse morphologies. By eliminating the reliance on real or expert demonstrations, these approaches significantly expanded the scalability of video-based demonstration learning. 

_3) Representation Learning for Generalization:_ A third stream of research focuses on representation learning for generalization, aiming to decouple policy learning from specific tasks and embodiments. Singh et al. [327] proposed a method that spatially aligned human hands and objects in 3D, producing consistent motion patterns that could pretrain generalpurpose manipulation policies and enable task-agnostic skill acquisition. Building upon this idea, Li et al. [318] learned shared agent-agnostic visual–action embeddings from diverse human operation videos, achieving robust sim-to-real transfer even on previously unseen tasks and object configurations. These approaches highlighted the potential of abstracting beyond raw trajectory reconstruction to acquire transferable skills across domains. 

_4) Task-specific Architectures and Objectives:_ Finally, several task-specific architectures and learning objectives have been designed to address unique challenges in video-based imitation. Gao et al. [319] introduced a hybrid master–slave modeling strategy with low-level geometric constraints for dualhand coordination, enabling robust reproduction of bimanual manipulation in cluttered environments. Building upon this idea, Shaw et al. [328] extracted vision–action–force relations from human demonstrations to provide physical and semantic 

priors for dexterous robot learning, reducing the dependence on paired demonstrations. Extending this approach, Chen et al. [321] presented a three-stage framework that combined video demonstrations, reinforcement learning-based trajectory optimization, and vision-only policy learning without privileged object information, thus enabling physically executable policies from noisy demonstrations. Yang et al. [320] addressed the reward specification bottleneck by constructing progress-based rewards from temporal rankings of video frames, supporting both reinforcement and adversarial imitation without access to action annotations. Collectively, these approaches advanced the practicality of video-based demonstration learning by tackling challenges such as bimanual coordination, noisy inputs, reward learning, and task-specific constraints. 

## _C. Datasets and Benchmarks_ 

_1) Human-teleoperated Datasets:_ A straightforward approach to collecting data for IL is through human teleoperation, where operators directly control robots to perform tasks. MIME [143] represented an early large-scale effort in this direction, providing 8,260 human–robot demonstrations across 20 diverse tasks, along with both human demonstration videos and kinesthetic robot trajectories. RH20T [144] extended this paradigm by scaling up to over 110,000 multimodal manipulation sequences and incorporating richer sensing modalities—visual, tactile, audio, and proprioceptive—captured through teleoperation interfaces with force–torque sensors and haptic feedback. This multimodal design enabled one-shot IL across a wider range of tasks, robots, and environments. Building on the same teleoperation foundation, BridgeData [145] focused on cross-environment generalization, offering 7,200 demonstrations across 71 tasks in 10 environments, primarily in kitchen settings. Its successor, BridgeData V2 [279] expanded the dataset to 60,096 trajectories in 24 environments, covering tasks from pick-and-place to complex manipulations, and supporting scalable robot learning with multi-task and language-conditioned objectives. 

_2) Augmented Datasets:_ To overcome the time-consuming and labor-intensive process of collecting many human demonstration data for IL, some datasets leverage data augmentation to expand existing demonstrations. RoboAgent [322] began with 7,500 teleoperated trajectories and scaled them up to 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

20 

TABLE IX 

RUBRIC FOR IMITATION LEARNING DATASET QUALITY ASSESSMENT 

|**Criterion**|**Description**|**Example Indicators**|
|---|---|---|
|Sensor Modality Richness|Extent and variety of sensing channels provided.|RGB, depth, tactile, proprioception, force–torque, audio|
|Annotation Quality|Accuracy, and consistency of labels across<br>modalities and tasks.|Object pose precision, end-effector position, task boundary<br>clarity|
|Task & Scene Diversity|Breadth of tasks, objects, and environmental<br>variations covered.|Number of object categories, scene layouts, lighting conditions|
|Physical Realism|Degree to which simulated/augmented data ap-<br>proximates real-world physics and appearance.|Visual fidelity, dynamics accuracy, sim-to-real transfer success|


roughly 98,000 using semantic augmentations, eliminating the need for additional human or robot effort. CyberDemo [329] adopted a similar strategy, collecting demonstrations in both simulated and real environments before applying extensive augmentations that introduced visual and physical variations, improving policy robustness and generalization. 

_3) Synthetic Datasets:_ Some datasets employ simulated or synthetic demonstration generation systems to expand the amount of training data from a small set of human demonstrations. MimicGen [323] generated over 50,000 demonstrations across 18 tasks from roughly 200 human examples by adapting object-centric manipulation behaviors to new contexts via trajectory transformations. IntervenGen [330] built on this idea by autonomously producing large sets of corrective interventions from minimal human input, thereby improving policy robustness to distribution shifts. DiffGen [331] adopted a similar strategy but incorporated differentiable physics simulation, photorealistic rendering, and vision–language models to create realistic robot demonstrations directly from text instructions. 

_4) Dexterous and Bimanual Manipulation Datasets:_ Focusing on dexterous manipulation and hand–object interactions, ARCTIC [324] offered 2.1 million videos with precise 3D hand–object meshes and dynamic contact data, enabling the study of bimanual manipulation of articulated objects. DexGraspNet [325] provided 1.32 million grasps for 5,355 objects using ShadowHand, with each grasp physically validated in simulation to ensure stability. OAKINK2 [326] extended the scope to real-world bimanual object manipulation, comprising 627 sequences and 4.01 million frames from multi-view captures with detailed pose annotations for human bodies, hands, and objects. Table VIII presents a concise summary of the representative benchmarks and datasets discussed above. 

From the perspective of dataset usability, several interdependent factors critically shape the practical value of an imitation learning dataset (as shown in Table IX). Foremost among these is sensor modality richness: datasets offering more comprehensive multi-modal signals (e.g., depth image, tactile feedback, proprioceptive states, force–torque readings, audio) generally deliver superior informational content and flexibility compared to RGB-only collections. Such multimodal data facilitates more accurate perception, reasoning over physical contacts, and cross-modal policy learning. Annotation quality is another decisive factor; precise labels for object poses, manipulator or end effector positions, and task boundaries directly constrain the attainable performance of learned models. Task and scene diversity further influences 

generalization: datasets encompassing a wide spectrum of object categories, environmental configurations, and illumination conditions are better poised to support robust and transferable policies than those restricted to narrow, repetitive settings. For simulated or augmented datasets, physical realism is especially critical, as greater realism narrows the sim-to-real gap and boosts the likelihood that policies trained virtually will operate successfully on physical robots. 

## VI. CHALLENGES AND FUTURE DIRECTIONS IN IMITATION LEARNING-BASED DEXTEROUS MANIPULATION 

IL-based dexterous manipulation poses unique challenges due to the inherent complexities of both IL and dexterous control. Despite significant advancements over the past decade, several challenges hinder its human-level dexterity and realworld applicability. Fig. 6 summarizes the challenges based on research impact and technical difficulty, highlighting immediate priorities further discussed in this section. 

## _A. Data Collection and Generation_ 

Data collection and generation for imitation learning-based dexterous manipulation pose several challenges, including heterogeneous data fusion, data diversity, high-dimensional data sparsity, and data collection costs. 

_1) Heterogeneous Data Fusion:_ Dexterous manipulation relies on multi-modal sensory inputs (e.g., visual, tactile, proprioceptive, and force), each with varying sampling rates, noise characteristics, and spatial-temporal resolutions, making data integration and synchronization challenging. Moreover, differences in embodiments and gripper designs introduce additional complexities. For example, demonstrations collected with one robotic hand may not directly generalize well to another due to variations in kinematics, actuation mechanisms, and sensor placements. Addressing these challenges requires (1) multi-modal alignment techniques to improve sensor fusion and (2) cross-embodiment learning frameworks for better transferability across robotic platforms and embodiments. 

_2) Data Quantity, Quality, and Diversity:_ Ensuring sufficient data quantity, quality, and diversity is challenging because collecting expert demonstrations for dexterous tasks at scale is labor-intensive and expensive. Even small variations in object properties, task conditions, or environmental factors can significantly affect manipulation policies, making it difficult for IL models to generalize. Future research should 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

21 

explore synthetic data augmentation, domain randomization, and generative models to efficiently generate diverse training datasets. Scalable and automated data collection methods, such as crowdsourced teleoperation, where multiple users remotely control robots to provide varied demonstrations, and self-supervised learning, where robots autonomously collect and label data through interaction and feedback, can further mitigate data collection bottlenecks. Additionally, establishing standardized data collection protocols and defining robust evaluation metrics for data quality and diversity will be essential to ensure consistency and reliability. 

_3) High-Dimensional Data Sparsity:_ Data sparsity in highdimensional action spaces limits the effectiveness of learned policies, as dexterous manipulation requires precise finger coordination, force regulation, and contact-rich interactions that demonstrations alone struggle to capture comprehensively. Hierarchical representation learning can potentially mitigate this challenge by structuring high-dimensional action spaces into more learnable subspaces. In dexterous manipulation, decomposing control policies into hierarchical levels—such as low-level motor commands, mid-level grasp strategies, and high-level task affordances—allows models to extract structured representations, improving learning efficiency and reducing dependence on large-scale demonstrations. 

RL fine-tuning further complements IL by refining dexterous manipulation policies beyond demonstrated behaviors. Fine-tuning in simulation enables robots to explore variations in object properties, task conditions, and environmental dynamics that may not be covered in the demonstration data. However, effective sim-to-real transfer techniques and highfidelity physics engines are crucial to bridging the gap between simulated training and real-world execution. 

_4) Data Collection Costs:_ The high cost and complexity of data collection pose barriers to scaling IL for dexterous manipulation. Traditional methods often require specialized motion capture systems, high-precision force sensors, and complex teleoperation setups, which are expensive, laborintensive, and impractical for large-scale data acquisition. Reducing these barriers requires the development of low-cost, scalable data collection methods, such as wearable sensor systems for capturing human demonstrations and shared autonomy techniques to minimize operator effort. Additionally, establishing standardized data collection protocols and collaborative data-sharing platforms can improve data accessibility and consistency across datasets. 

While simulation provides a scalable solution for generating synthetic data in dexterous manipulation, several challenges limit its real-world effectiveness. First, achieving real-world fidelity remains difficult, as physics engines struggle to model contact dynamics, deformable objects, and high-resolution tactile feedback, leading to discrepancies between simulation and reality. Second, ensuring sufficient data diversity is another challenge, as models trained in static or overly idealized environments often fail to generalize to unstructured real-world conditions, and while domain randomization can enhance robustness, excessive variation may reduce learning efficiency or introduce unrealistic artifacts. Third, the sim-toreal gap further complicates deployment, as policies trained 


Fig. 6. Prioritization matrix of key challenges in imitation learning-based dexterous manipulation. 

in simulation often fail in real-world settings due to sensor noise, unexpected disturbances, and actuation discrepancies. While techniques such as domain adaptation, sim-to-real finetuning, and physics-based calibration can help mitigate these challenges, they require substantial computational resources and real-world validation, increasing deployment complexity. 

## _B. Benchmarking and Reproducibility_ 

The dependence on real-world hardware experiments and the variability in simulation environments pose significant challenges for benchmarking and reproducibility in imitation learning-based dexterous manipulation. Unlike computer vision or natural language processing, where large-scale datasets enable standardized evaluations, dexterous manipulation involves physical interactions, making consistent replication across research efforts difficult. Hardware dependency is a major obstacle, as reproducing results requires access to the same robotic platform, gripper design, sensor setup, and control software, which is often impractical in real-world experiments due to cost, availability, and proprietary constraints. 

Simulation-based benchmarks offer a scalable alternative, but the lack of standardized simulation settings, computing environments, and evaluation protocols in physics-based simulators limits fair comparisons across studies. Variability in physics engine configurations, actuator models, contact dynamics, and material properties further exacerbates inconsistencies, making it difficult to establish reliable performance benchmarks and universally comparable evaluation metrics in dexterous manipulation research. Some studies rely on non-physics-based or simplified simulators, which focus on high-level task planning but neglect low-level contact physics modeling. While these environments provide visual realism and scalable training, they introduce a significant sim-to-real gap, failing to capture key aspects of dexterous manipulation, such as precise force interactions and object deformations. 

Addressing these challenges requires standardized benchmarking frameworks and open-source datasets for both simulation and real-world experiments. In simulation, standardization should focus on consistent physics parameterization (e.g., contact dynamics, actuator models, material properties) and com- 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

22 

mon environment representations to minimize discrepancies across different physics engines. For real-world experiments, benchmarks should incorporate multi-modal sensory recordings (e.g., RGB-D, tactile, proprioceptive data) and diverse task demonstrations across various robotic embodiments to ensure broader comparability. Additionally, establishing standard evaluation protocols across hardware platforms and physicsbased simulators would enable more reliable performance comparisons across studies. 

## _C. Generalization to Novel Setups_ 

Generalizing IL-based dexterous manipulation policies is challenging due to task and environment variability, adaptive learning limitations, and cross-embodiment adaptability: 

_1) Task and Environment Variability:_ Learning-based policies often struggle to extend beyond the specific demonstrations to new conditions. Variations in object shapes, sizes, weights, textures, and dynamic interactions, as well as unforeseen obstacles and workspace changes, can significantly degrade performance. Also, these policies may fail when faced with unseen task configurations that require adaptive behavior beyond the demonstrated distribution. 

_2) Adaptive and Continual Learning Frameworks:_ Traditional IL models do not adapt to new tasks or environmental changes after training. This limitation leads to rigid behaviors that fail to improve with experience. Continual learning frameworks allow robots to learn incrementally from new data without catastrophic forgetting, while adaptive learning methods such as meta-learning and RL fine-tuning enable policies to generalize to new conditions by leveraging prior experience. Additionally, uncertainty-aware models can dynamically adjust decision-making strategies based on real-time feedback, improving generalization in unstructured settings. 

_3) Cross-Embodiment Adaptability:_ Variability in robot embodiments, gripper designs, sensor configurations, and actuation dynamics poses significant challenges for generalization. A policy trained on one robotic hand may struggle to transfer to another due to differences in degrees of freedom, joint limits, contact dynamics, and control strategies. Even within the same robotic platform, inconsistencies arise from sensor noise, latency, and mechanical tolerances. To address this, morphology-agnostic policy learning can be explored, where models are trained across diverse robotic embodiments to develop transferable representations. Graph-based and latentspace embeddings of robot kinematics could help policies reason about different embodiments more effectively. Additionally, modular policy architectures, where separate components (e.g., perception, control, and adaptation modules) are fine-tuned independently, may enhance transferability. Another promising direction is meta-learning and few-shot adaptation, enabling robots to quickly adjust to new embodiments with minimal data, reducing the need for extensive retraining. 

## _D. Sim-to-Real Transfer_ 

Simulation provides a scalable and controlled environment for training dexterous manipulation policies. However, the sim-to-real gap remains a major obstacle to deploying IL 

models on real-world robotic systems. This gap arises from discrepancies in factors such as contact dynamics, sensor noise, actuation delays, and material properties, which are often inadequately modeled in simulation. The following subsection discusses key techniques and ongoing challenges related to sim-to-real transfer. 

_1) Domain Randomization:_ One widely adopted strategy for bridging the sim-to-real gap is domain randomization. Instead of replicating real-world conditions exactly, domain randomization introduces variability in simulation parameters. This exposure helps policies generalize to unseen real-world scenarios [281]. However, domain randomization requires manual tuning of parameter distributions, which demands expert knowledge to balance realism and variability. It also struggles to address unmodeled dynamics, such as non-linear material deformations or high-frequency contact interactions, which are crucial for dexterous manipulation. Therefore, future research could focus on combining domain randomization with complementary sim-to-real techniques, such as real-world fine-tuning or adversarial domain adaptation, to achieve more robust and reliable transfer. 

_2) Feature Alignment:_ Another promising line of work focuses on feature alignment, where the objective is to map simulated and real-world sensory inputs into a shared latent feature space. This can be achieved through representation learning techniques such as autoencoders or contrastive learning, which minimize the distributional discrepancy between the domains. Similarly, cross-modal embeddings can be learned to align tactile or proprioceptive features from both domains, which is particularly valuable for dexterous tasks involving high-dimensional state observations. These approaches can complement domain randomization by providing a structured way to reduce domain shift. 

_3) Adversarial Domain Adaptation:_ Adversarial techniques have also emerged as a powerful way to minimize sim-to-real discrepancies. This approach has been applied to tasks where direct collection of real-world demonstrations is expensive [332]. In robotic manipulation, adversarial adaptation can be used in combination with IL by first imitating expert demonstrations in simulation and then fine-tuning the learned policy to fool a domain discriminator, ensuring smoother deployment in real-world settings. Future research could explore integrating adversarial adaptation with generative models or selfsupervised representation learning to improve robustness and scalability, particularly for high-dimensional sensory inputs such as vision and tactile feedback. 

_4) Hybrid Training and Online Adaptation:_ Beyond domain adaptation, hybrid training paradigms are gaining significant traction. In these approaches, policies are first pre-trained in simulation for rapid skill acquisition and subsequently finetuned on real-world data using IL, RL, or offline corrections [27]. This strategy combines the efficiency and scalability of simulation with the precision of real-world adaptation, thereby reducing the need for extensive real-world data collection. Additionally, self-supervised real-to-sim refinement, where real-world rollouts are used to iteratively adjust simulation parameters, can improve the fidelity of simulated environments and facilitate bi-directional transfer. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

23 

## _E. Real-Time Control_ 

Dexterous manipulation presents significant computational challenges due to its high-dimensional action spaces and complex dynamics. Achieving real-time execution demands a delicate balance between accuracy and efficiency in terms of both software and hardware. 

Efficient real-time control relies on algorithms capable of handling nonlinearities, contact dynamics, and feedback loops while maintaining stability and responsiveness. Model-based approaches, such as optimal control and Model Predictive Control (MPC), leverage system dynamics to generate control policies but often struggle with the complexities of dexterous manipulation. MPC, in particular, provides real-time adaptability through continuous optimization but imposes high computational demands, often requiring specialized hardware acceleration or dedicated edge computing to meet real-time constraints. In contrast, model-free RL learns policies directly from data, bypassing the need for explicit system modeling. While RL offers greater adaptability in high-dimensional, unstructured environments, it remains sample inefficient, prone to slow convergence, and challenging to stabilize, especially for real-time execution. A potential solution is designing hybrid control strategies that combine model-based control for stability with model-free learning for adaptability, improving efficiency without sacrificing robustness. Meanwhile, accelerated learning techniques, such as parallelized RL training and meta-learning, could address sample inefficiency, enabling faster policy convergence. 

Hardware architecture is also a key enabler of real-time dexterous manipulation, balancing computational power, latency, and energy efficiency. High-performance computing hardware (e.g., GPUs, TPUs, and FPGAs) is essential for complex model-based and learning-based control strategies but is often constrained by high power consumption and deployment costs. Edge computing and custom ASICs offer low-latency processing but may lack the computational capacity required for large-scale dexterous manipulation policy inference. Cloud computing facilitates large-scale training and high-fidelity simulations; however, real-time reliance on remote processing is limited by communication delays and network instability. Recent advancements in low-power AI accelerators, neuromorphic computing, and distributed edgecloud architectures have the potential to enhance real-time processing while reducing latency and energy constraints. 

## _F. Safety, Robustness, and Social Compliance_ 

Ensuring safety, robustness, and social compliance is crucial for real-world dexterous robotics, requiring risk prevention, adaptive error recovery, and human-aware behavior for seamless integration. Real-world dexterous manipulation demands reliable error detection, recovery, and adaptability in dynamic environments. Detecting failures is challenging due to sensor noise, occlusions, and unpredictable interactions, while recovery strategies like re-grasping or trajectory replanning must be executed in real time to maintain stability and task continuity. Future research should address two key aspects. First, largescale failure datasets and standardized benchmarks are essen- 

tial for improving data-driven recovery policies. Establishing comprehensive datasets and evaluation protocols for failure detection, uncertainty estimation, and recovery effectiveness would provide a foundation for training and benchmarking robust policies. Second, self-supervised learning for multi-modal anomaly detection could enable robots to autonomously refine their error detection capabilities. By leveraging visual, tactile, and proprioceptive feedback, robots could learn to recognize and anticipate failures in real time, improving adaptability and robustness in dynamic environments. 

Safety is equally critical, particularly in real-world deployments where unpredictable interactions and dynamic conditions pose significant risks. In dexterous manipulation, safety considerations involve collision avoidance, force regulation, and compliance control, particularly when interacting with fragile objects or operating near humans. However, achieving these safety measures requires handling varying contact conditions, but sensor noise, occlusions, and data processing delays can reduce reliability. Additionally, while compliant actuators and soft robotic designs help mitigate impact forces, integrating these hardware safety mechanisms involves tradeoffs between control precision, responsiveness, and durability. Different paradigms also entail distinct safety concerns. Endto-end learning directly maps perception to control, but its black-box nature complicates safety verification and error tracing. Motion module learning decomposes the pipeline into structured stages, improving generalization and safety at the cost of intermediate complexity. 

To address safety constraints in IL for real-world dexterous manipulation, recent studies have investigated constrained policy optimization [333] and Lyapunov-based safe learning [334]. Constrained policy optimization integrates hard limits on torque, contact force, or joint velocity directly into the training objective, often via Lagrangian relaxation or primal-dual methods. For instance, Constrained Trust Region Policy Optimization (C-TRPO) [335] augmented the trustregion update rule by incorporating actuator and contact-force limits, ensuring that each policy update remains close to expert demonstrations while strictly respecting physical safety bounds. In parallel, Lyapunov-based approaches synthesized control policies that provably satisfy safety specifications, constructing Lyapunov functions as certificates of stability [336]– [338]. In dexterous manipulation, Neural Lyapunov Control (NLC) [339] has been adapted to learn neural network policies that maintain force closure and avoid excessive contact forces. Recent work combined these paradigms. SafeDiffuser [340] augmented diffusion-policy-based planning with control barrier functions to enforce real-time safety constraints. By conditioning the diffusion model on expert demonstrations and integrating CBF-based corrections at every denoising step, the method achieves robust generalization to unseen scenarios while guaranteeing safety-critical bounds. 

Beyond technical safety, social compliance is essential for real-world deployment yet remains underexplored, particularly in HRI settings. In the context of dexterous manipulation, prior research has investigated various approaches, such as RLbased methods (e.g. preference-based RL [341] and inverse RL [342]), MPC frameworks (e.g. socially aware Model Predictive 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

24 

Path Integral control [343]), and game-theoretic models (e.g. Nash equilibrium formulations [344]). However, achieving social compliance remains challenging due to the inherent ambiguity of human comfort, spatial preferences, and social norms, which are often context-dependent and difficult to model explicitly. Additionally, soft social constraints, such as maintaining legibility of motion, avoiding intrusive actions, or signaling intent, are subjective and require learning from diverse human feedback, which is costly and time-consuming. Another challenge lies in the lack of standardized evaluation metrics and benchmarking protocols to assess social compliance. Existing metrics, such as trajectory smoothness, proximity compliance, or motion legibility, are often evaluated qualitatively or through small-scale user studies without a consistent framework. Moreover, there is a lack of publicly available datasets and simulation environments specifically designed for evaluating social compliance in dexterous manipulation, unlike traditional benchmarks for grasping or motion planning (e.g., RLBench [345] or ManiSkill3 [346]). Without well-defined metrics, datasets, and test scenarios, progress in this area remains fragmented and difficult to measure systematically. 

## _G. High-Precision and Micro-Scale Manipulation_ 

While the above discussion focuses on macro-scale object manipulation (e.g., bottles, tools), scaling down to the millimeter or micrometer level (e.g., electronic components, micromachines) introduces fundamentally different challenges. At these scales, perception limitations, such as low sensor resolution, visual noise, and occlusion, become critical. Actuation requirements also rise sharply, demanding ultra-precise force and motion control within micrometer tolerances to prevent damage to delicate objects. Conventional actuators frequently suffer from backlash, hysteresis, and limited resolution, while achieving high control precision becomes a bottleneck. These challenges have driven the development of advanced control methods [347]–[349], including force-feedback, adaptive impedance, and hybrid position-force strategies designed specifically for micro-scale tasks. 

Moreover, data collection at micro-scales remains a significant challenge. Acquiring large, diverse, and high-quality demonstrations is both costly and time-intensive, given the specialized equipment and delicate experimental setups required. Synthetic data generation through high-fidelity physics-based simulation is a promising direction, but it requires accurate modeling of micro-scale physical effects, such as adhesion forces, surface roughness, or fluid dynamics, which are often negligible in macro-scale tasks. From an algorithmic perspective, recent research [76] underscored the potential of hierarchical IL frameworks in addressing dexterous manipulation in micro-scale tasks. These techniques, together with advances in small-scale robots [350], presented a promising pathway for enabling autonomous micro-manipulation tasks, such as precision assembly and surgical procedures. 

## _H. Roadmap for IL-based Dexterous Manipulation_ 

To summarize, we propose a potential roadmap to address these issues, distinguishing between low-hanging fruits and grand, long-term challenges. 

_1) Low-Hanging Fruits:_ Data collection and benchmarking are high-impact areas that require relatively low research difficulty. Efforts focused on synthetic data generation, domain randomization, and crowdsourced teleoperation can quickly scale up the diversity of training datasets, which is essential for improving the generalization capabilities of models. Furthermore, establishing standardized benchmarking frameworks and evaluation protocols will streamline the process of comparing performance across different studies. These actions will enable faster progress in dexterous manipulation and contribute to broader adoption of the proposed techniques. 

_2) Grand, Long-Term Challenges:_ Sim-to-real transfer and real-time control are high-impact challenges that involve significant research difficulty. Bridging the sim-to-real gap will require breakthroughs in domain adaptation, hybrid training paradigms, and better computational resources. These advances are crucial for ensuring the successful deployment of models trained in simulation into real-world environments. Real-time control, particularly for high-dimensional tasks like dexterous manipulation, presents a need for more efficient algorithms, better control strategies, and seamless hardware integration. Solving these challenges will be essential for creating practical, high-performance systems capable of operating in dynamic, unstructured environments. 

_3) Safety and High-Precision Manipulation:_ While safety and high-precision manipulation are specialized concerns, they remain essential for real-world applications. These areas are high-difficulty but relatively lower in impact compared to simto-real transfer and real-time control. However, safety remains critical for human-robot interaction, especially in unstructured environments, and high-precision control is crucial for tasks like micro-manipulation. Future research should continue to address these challenges for real-world deployment. 

## VII. CONCLUSION 

Imitation learning has shown significant promise in enabling robots to perform dexterous manipulation tasks with humanlike skill and precision. By learning from human demonstrations, robots can acquire complex manipulation capabilities that are difficult to achieve through traditional programming methods. This survey has provided an overview of the current state-of-the-art in IL-based dexterous manipulation, highlighting key techniques, applications, and challenges. 

Despite the progress that has been made, several challenges remain that hinder the practical deployment of these systems. Addressing issues related to data collection, generalization, real-time control, safety, and sim-to-real transfer is essential for advancing the field. Future research should focus on developing optimized IL algorithms, enhancing human-robot collaboration, and integrating advanced sensory systems. 

The future of dexterous manipulation holds great potential, with applications ranging from industrial automation to healthcare and service robotics. By continuing to push the boundaries of IL and robotic manipulation, researchers and practitioners can pave the way for more capable, adaptable, and intelligent robots. These advances will not only improve the efficiency and safety of robotic tasks but also open up new possibilities for human-robot collaboration and interaction. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

25 

## ACKNOWLEDGMENT 

We would like to thank Huapeng Li, Qianyi Wang, Mingwu Liu, Shouzheng Wang and Zijing Yang for their contributions to the completion of this survey. 

## REFERENCES 

- [1] C. Gonz´alez, J. E. Solanes, A. Mu˜noz, L. Gracia, V. Girb´es-Juan, and J. Tornero, “Advanced teleoperation and control system for industrial robots based on augmented virtuality and haptic feedback,” _J. Manuf. Syst._ , vol. 59, pp. 283–298, 2021. 

- [2] I. Rodrıguez, K. Nottensteiner, D. Leidner, M. Kaßecker, F. Stulp, and A. Albu-Sch¨affer, “Iteratively refined feasibility checks in robotic assembly sequence planning,” _IEEE Robot. Autom. Lett_ , vol. 4, no. 2, pp. 1416–1423, 2019. 

- [3] J. Liang, J. Mahler, M. Laskey, P. Li, and K. Goldberg, “Using dVRK teleoperation to facilitate deep learning of automation tasks for an industrial robot,” in _CASE_ , 2017, pp. 1–8. 

- [4] J. Rebelo, T. Sednaoui, E. B. Den Exter, T. Krueger, and A. Schiele, “Bilateral robot teleoperation: A wearable arm exoskeleton featuring an intuitive user interface,” _IEEE Robot. Autom. Mag._ , vol. 21, no. 4, pp. 62–69, 2014. 

- [5] M. Diftler, T. Ahlstrom, R. Ambrose, N. Radford, C. Joyce, N. De La Pena, A. Parsons, and A. Noblitt, “Robonaut 2—initial activities on-board the iss,” in _IEEE AeroConf_ , 2012, pp. 1–12. 

- [6] G. Brantner and O. Khatib, “Controlling ocean one: Human–robot collaboration for deep-sea manipulation,” _J. Field Robot._ , vol. 38, no. 1, pp. 28–51, 2021. 

- [7] L. Barbieri, F. Bruno, A. Gallo, M. Muzzupappa, and M. L. Russo, “Design, prototyping and testing of a modular small-sized underwater robotic arm controlled through a master-slave approach,” _Ocean Eng._ , vol. 158, pp. 253–262, 2018. 

- [8] Z. Gharaybeh, H. Chizeck, and A. Stewart, “Telerobotic control in virtual reality,” in _OCEANS_ , 2019, pp. 1–8. 

- [9] D. Zhang, J. Chen, W. Li, D. Bautista Salinas, and G.-Z. Yang, “A microsurgical robot research platform for robot-assisted microsurgery research and training,” _Int. J. Comput. Assist. Radiol. Surg._ , vol. 15, pp. 15–25, 2020. 

- [10] J. Guo, C. Liu, and P. Poignet, “A scaled bilateral teleoperation system for robotic-assisted surgery with time delay,” _J. Intell. Robot. Syst._ , vol. 95, pp. 165–192, 2019. 

- [11] F. Pugin, P. Bucher, and P. Morel, “History of robotic surgery: from aesop® and zeus® to da vinci®,” _J. Visc. Surg._ , vol. 148, no. 5, pp. e3–e8, 2011. 

- [12] M. Talamini, K. Campbell, and C. Stanfield, “Robotic gastrointestinal surgery: early experience and system description,” _J. Laparoendosc. Adv. Surg. Tech._ , vol. 12, no. 4, pp. 225–232, 2002. 

- [13] X. B. Peng, P. Abbeel, S. Levine, and M. Van de Panne, “DeepMimic: Example-guided deep reinforcement learning of physics-based character skills,” _ACM Trans. Graph._ , vol. 37, no. 4, pp. 1–14, 2018. 

- [14] T. Zhang, Z. McCarthy, O. Jow, D. Lee, X. Chen, K. Goldberg, and P. Abbeel, “Deep imitation learning for complex manipulation tasks from virtual reality teleoperation,” in _ICRA_ , 2018, pp. 5628–5635. 

- [15] A. Handa, A. Allshire, V. Makoviychuk, A. Petrenko, R. Singh, J. Liu, D. Makoviichuk, K. Van Wyk, A. Zhurkevich, B. Sundaralingam _et al._ , “DeXtreme: Transfer of agile in-hand manipulation from simulation to reality,” in _ICRA_ , 2023, pp. 5977–5984. 

- [16] C. Wang, H. Shi, W. Wang, R. Zhang, L. Fei-Fei, and K. Liu, “DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation,” in _RSS_ , 2024. 

- [17] A. Sivakumar, K. Shaw, and D. Pathak, “Robotic telekinesis: Learning a robotic hand imitator by watching humans on youtube,” in _RSS_ , 2022. 

- [18] A. Handa, K. Van Wyk, W. Yang, J. Liang, Y.-W. Chao, Q. Wan, S. Birchfield, N. Ratliff, and D. Fox, “DexPilot: Vision-based teleoperation of dexterous robotic hand-arm system,” in _ICRA_ , 2020, pp. 9164–9170. 

- [19] Y. Qin, W. Yang, B. Huang, K. Van Wyk, H. Su, X. Wang, Y.-W. Chao, and D. Fox, “AnyTeleop: A general vision-based dexterous robot armhand teleoperation system,” in _RSS_ , 2023. 

- [20] Y. Qin, H. Su, and X. Wang, “From one hand to multiple hands: Imitation learning for dexterous manipulation from single-camera teleoperation,” _IEEE Robot. Autom. Lett_ , vol. 7, no. 4, pp. 10 873–10 881, 2022. 

- [21] J. Grannen, Y. Wu, B. Vu, and D. Sadigh, “Stabilize to act: Learning to coordinate for bimanual manipulation,” in _CoRL_ , 2023, pp. 563–576. 

- [22] X. Zhu, J. Ke, Z. Xu, Z. Sun, B. Bai, J. Lv, Q. Liu, Y. Zeng, Q. Ye, C. Lu, M. Tomizuka, and L. Shao, “Diff-LfD: Contact-aware modelbased learning from visual demonstration for robotic manipulation via differentiable physics-based simulation and rendering,” in _CoRL_ , 2023. 

- [23] D. Antotsiou, G. Garcia-Hernando, and T.-K. Kim, “Task-oriented hand motion retargeting for dexterous manipulation imitation,” in _ECCV_ , 2018. 

- [24] S. Li, X. Ma, H. Liang, M. G¨orner, P. Ruppel, B. Fang, F. Sun, and J. Zhang, “Vision-based teleoperation of shadow dexterous hand using end-to-end deep neural network,” in _ICRA_ , 2019, pp. 416–422. 

- [25] L. X. Shi, A. Sharma, T. Z. Zhao, and C. Finn, “Waypoint-based imitation learning for robotic manipulation,” in _CoRL_ , 2023, pp. 2195– 2209. 

- [26] P. Florence, C. Lynch, A. Zeng, O. A. Ramirez, A. Wahid, L. Downs, A. Wong, J. Lee, I. Mordatch, and J. Tompson, “Implicit behavioral cloning,” in _CoRL_ , 2022, pp. 158–168. 

- [27] A. Rajeswaran, V. Kumar, A. Gupta, G. Vezzani, J. Schulman, E. Todorov, and S. Levine, “Learning complex dexterous manipulation with deep reinforcement learning and demonstrations,” in _RSS_ , 2018. 

- [28] Y. Ding, C. Florensa, P. Abbeel, and M. Phielipp, “Goal-conditioned imitation learning,” in _NeurIPS_ , vol. 32, 2019. 

- [29] A. Mandlekar, D. Xu, R. Mart´ın-Mart´ın, S. Savarese, and L. Fei-Fei, “GTI: Learning to Generalize across Long-Horizon Tasks from Human Demonstrations,” in _RSS_ , 2020. 

- [30] S. Belkhale, Y. Cui, and D. Sadigh, “HYDRA: Hybrid robot actions for imitation learning,” in _CoRL_ , 2023, pp. 2113–2133. 

- [31] P.-L. Guhur, S. Chen, R. G. Pinel, M. Tapaswi, I. Laptev, and C. Schmid, “Instruction-driven history-aware policies for robotic manipulations,” in _CoRL_ , 2023, pp. 175–187. 

- [32] C. Chi, Z. Xu, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _Int. J. Robot. Res._ , 2023. 

- [33] A. Zeng, P. Florence, J. Tompson, S. Welker, J. Chien, M. Attarian, T. Armstrong, I. Krasin, D. Duong, V. Sindhwani _et al._ , “Transporter networks: Rearranging the visual world for robotic manipulation,” in _CoRL_ , 2021, pp. 726–747. 

- [34] S. Haldar, J. Pari, A. Rai, and L. Pinto, “Teach a robot to fish: Versatile imitation from one minute of demonstrations,” in _RSS_ , 2023. 

- [35] M. Zare, P. M. Kebria, A. Khosravi, and S. Nahavandi, “A survey of imitation learning: Algorithms, recent developments, and challenges,” _IEEE Trans. Cybern._ , 2024. 

- [36] ——, “A survey of imitation learning: Algorithms, recent developments, and challenges,” _IEEE Trans. Cybern._ , 2024. 

- [37] S. Arora and P. Doshi, “A survey of inverse reinforcement learning: Challenges, methods and progress,” _Artif. Intell._ , vol. 297, 2021. 

- [38] D. Han, B. Mulyana, V. Stankovic, and S. Cheng, “A survey on deep reinforcement learning algorithms for robotic manipulation,” _Sensors_ , vol. 23, no. 7, 2023. 

- [39] G. Li, R. Wang, P. Xu, Q. Ye, and J. Chen, “The developments and challenges towards dexterous and embodied robotic manipulation: A survey,” _arXiv preprint arXiv:2507.11840_ , 2025. 

- [40] A. Pitkevich and I. Makarov, “A survey on sim-to-real transfer methods for robotic manipulation,” in _SISY_ , 2024, pp. 000 259–000 266. 

- [41] E. Welte and R. Rayyes, “Interactive imitation learning for dexterous robotic manipulation: Challenges and perspectives–a survey,” _arXiv preprint arXiv:2506.00098_ , 2025. 

- [42] T. Tsuji, Y. Kato, G. Solak, H. Zhang, T. Petriˇc, F. Nori, and A. Ajoudani, “A survey on imitation learning for contact-rich tasks in robotics,” _arXiv preprint arXiv:2506.13498_ , 2025. 

- [43] J. K. Salisbury and J. J. Craig, “Articulated hands: Force control and kinematic issues,” _Int. J. Robot. Res._ , vol. 1, no. 1, pp. 4–17, 1982. 

- [44] M. T. Mason and J. K. Salisbury, “Robot hands and the mechanics of manipulation,” _IEEE Trans. Autom. Control_ , vol. 31, pp. 879–880, 1986. 

- [45] Y. Bai and C. K. Liu, “Dexterous manipulation using both palm and fingers,” in _ICRA_ , 2014, pp. 1560–1565. 

- [46] Y. Liu, S. Liu, B. Chen, Z.-X. Yang, and S. Xu, “Fusion-perceptionto-action transformer: Enhancing robotic manipulation with 3d visual fusion attention and proprioception,” _IEEE Trans. Robot._ , vol. 41, pp. 1553–1567, 2025. 

- [47] A. Okamura, N. Smaby, and M. Cutkosky, “An overview of dexterous manipulation,” in _ICRA_ , vol. 1, 2000, pp. 255–262. 

- [48] C. Yu and P. Wang, “Dexterous manipulation for multi-fingered robotic hands with reinforcement learning: A review,” _Front. Neurorobot._ , vol. 16, p. 861825, 2022. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

26 

- [49] M. Buss, H. Hashimoto, and J. Moore, “Dextrous hand grasping force optimization,” _IEEE Trans. Robot. Automat._ , vol. 12, no. 3, pp. 406– 418, 1996. 

- [50] I. Mordatch, Z. Popovi´c, and E. Todorov, “Contact-invariant optimization for hand manipulation,” in _SCA_ , 2012, pp. 137–144. 

- [51] I. Popov, N. Heess, T. Lillicrap, R. Hafner, G. Barth-Maron, M. Vecerik, T. Lampe, Y. Tassa, T. Erez, and M. Riedmiller, “Dataefficient deep reinforcement learning for dexterous manipulation,” _arXiv preprint arXiv:1704.03073_ , 2017. 

- [52] R. J. Williams, “Simple statistical gradient-following algorithms for connectionist reinforcement learning,” _Machine Learning_ , vol. 8, pp. 229–256, 1992. 

- [53] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv preprint arXiv:1707.06347_ , 2017. 

- [54] T. Dai, K. Arulkumaran, T. Gerbert, S. Tukra, F. Behbahani, and A. A. Bharath, “Analysing deep reinforcement learning agents trained with domain randomisation,” _Neurocomputing_ , vol. 493, pp. 143–165, 2022. 

- [55] K. Xu, Z. Hu, R. Doshi, A. Rovinsky, V. Kumar, A. Gupta, and S. Levine, “Dexterous manipulation from images: Autonomous realworld rl via substep guidance,” in _ICRA_ , 2023, pp. 5938–5945. 

- [56] Z.-H. Yin, B. Huang, Y. Qin, Q. Chen, and X. Wang, “Rotating without seeing: Towards in-hand dexterity through touch,” in _RSS_ , 2023. 

- [57] T. Lillicrap, “Continuous control with deep reinforcement learning,” in _ICLR_ , 2016. 

- [58] H. Ravichandar, A. S. Polydoros, S. Chernova, and A. Billard, “Recent advances in robot learning from demonstration,” _Annu. Rev. Control Robot. Auton. Syst._ , vol. 3, no. 1, pp. 297–330, 2020. 

- [59] M. BAIN, “A framework for behavioral cloning,” _Mach. Intell._ , 1995. [60] A. Y. Ng and S. J. Russell, “Algorithms for inverse reinforcement learning,” in _ICML_ , 2000, pp. 663–670. 

- [61] J. Ho and S. Ermon, “Generative adversarial imitation learning,” in _NeurIPS_ , vol. 29, 2016. 

- [62] A. Bandura and R. H. Walters, _Social Learning Theory_ . Prentice hall Englewood Cliffs, NJ, 1977, vol. 1. 

- [63] G. Rizzolatti and L. Craighero, “The mirror-neuron system,” _Annu. Rev. Neurosci._ , vol. 27, no. 1, pp. 169–192, 2004. 

- [64] D. M. Wolpert, Z. Ghahramani, and M. I. Jordan, “An internal model for sensorimotor integration,” _Science_ , vol. 269, no. 5232, pp. 1880– 1882, 1995. 

- [65] E. Todorov and M. I. Jordan, “Optimal feedback control as a theory of motor coordination,” _Nat. Neurosci._ , vol. 5, no. 11, pp. 1226–1235, 2002. 

- [66] M. C. Nah, J. Lachner, and N. Hogan, “Modular robot control with motor primitives,” _arXiv preprint arXiv:2505.10694_ , 2025. 

- [67] Z. Chen, J. Yin, Y. Chen, J. Huo, P. Tian, J. Shi, Y. Hou, Y. Li, and Y. Gao, “DeCo: Task decomposition and skill composition for zeroshot generalization in long-horizon 3d manipulation,” _arXiv preprint arXiv:2505.00527_ , 2025. 

- [68] J. Achiam, H. Edwards, D. Amodei, and P. Abbeel, “Variational option discovery algorithms,” _arXiv preprint arXiv:1807.10299_ , 2018. 

- [69] J. Sun, A. Curtis, Y. You, Y. Xu, M. Koehle, L. Guibas, S. Chitta, M. Schwager, and H. Li, “Hierarchical hybrid learning for long-horizon contact-rich robotic assembly,” _arXiv preprint arXiv:2409.16451_ , 2024. 

- [70] H. Wang, L. Qi, Z. Wang, J. Ren, W. Li, and Y. Sun, “Hierarchical visual policy learning for long-horizon robot manipulation in densely cluttered scenes,” in _ICRA_ , 2025, pp. 1149–1155. 

- [71] R. S. Sutton, D. Precup, and S. Singh, “Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning,” _Artif. Intell._ , vol. 112, no. 1-2, pp. 181–211, 1999. 

- [72] D. Precup, _Temporal abstraction in reinforcement learning_ . University of Massachusetts Amherst, 2000. 

- [73] P.-L. Bacon, J. Harb, and D. Precup, “The option-critic architecture,” in _AAAI_ , vol. 31, no. 1, 2017. 

- [74] S. Krishnan, R. Fox, I. Stoica, and K. Goldberg, “DDCO: Deep discovery of continuous options for robot learning from demonstrations,” in _CoRL_ , 2017, pp. 418–437. 

- [75] B. Li, J. Li, T. Lu, Y. Cai, and S. Wang, “Hierarchical learning from demonstrations for long-horizon tasks,” in _ICRA_ , 2021, pp. 4545–4551. 

- [76] J. W. Kim, J.-T. Chen, P. Hansen, L. X. Shi, A. Goldenberg, S. Schmidgall, P. M. Scheikl, A. Deguet, B. M. White, D. R. Tsai _et al._ , “SRT-H: A hierarchical framework for autonomous surgery via language-conditioned imitation learning,” _Sci. Robot._ , vol. 10, no. 104, p. eadt5254, 2025. 

- [77] Y. Chen, Y. Geng, F. Zhong, J. Ji, J. Jiang, Z. Lu, H. Dong, and Y. Yang, “Bi-DexHands: Towards human-level bimanual dexterous 

   - manipulation,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 46, no. 5, pp. 2804–2818, 2023. 

- [78] B. Zhou, H. Yuan, Y. Fu, and Z. Lu, “Learning diverse bimanual dexterous manipulation skills from human demonstrations,” _arXiv preprint arXiv:2410.02477_ , 2024. 

- [79] J.-P. Sleiman, F. Farshidian, M. V. Minniti, and M. Hutter, “A unified mpc framework for whole-body dynamic locomotion and manipulation,” _IEEE Robot. Autom. Lett_ , vol. 6, no. 3, pp. 4688–4695, 2021. 

- [80] M. Yu, K. Lv, C. Wang, Y. Jiang, M. Tomizuka, and X. Li, “Generalizable whole-body global manipulation of deformable linear objects by dual-arm robot in 3-d constrained environments,” _Int. J. Robot. Res._ , vol. 44, no. 4, pp. 607–639, 2025. 

- [81] S. Zhong, S. Guo, T. Sun, H.-W. Huang, Q. Shi, Q. Huang, T. Fukuda, and H. Wang, “Paired interactions of magnetic millirobots in confined spaces through data-driven disturbance rejection control under global input,” _IEEE/ASME Trans. Mechatron._ , 2025. 

- [82] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _ICML_ , 2023. 

- [83] S. P. Arunachalam, S. Silwal, B. Evans, and L. Pinto, “Dexterous imitation made easy: A learning-based framework for efficient dexterous manipulation,” in _ICRA_ , 2023, pp. 5954–5961. 

- [84] Y. Liu, A. Gupta, P. Abbeel, and S. Levine, “Imitation from observation: Learning to imitate behaviors from raw video via context translation,” in _ICRA_ , 2018, pp. 1118–1125. 

- [85] T. Osa, J. Pajarinen, G. Neumann, J. A. Bagnell, P. Abbeel, J. Peters _et al._ , “An algorithmic perspective on imitation learning,” _Found. Trends Robot._ , vol. 7, no. 1-2, pp. 1–179, 2018. 

- [86] L. Ke, J. Wang, T. Bhattacharjee, B. Boots, and S. Srinivasa, “Grasping with chopsticks: Combating covariate shift in model-free imitation learning for fine manipulation,” in _ICRA_ , 2021, pp. 6185–6191. 

- [87] N. M. Shafiullah, Z. J. Cui, A. Altanzaya, and L. Pinto, “Behavior transformers: Cloning k modes with one stone,” in _NeurIPS_ , 2022. 

- [88] A. Mandlekar, F. Ramos, B. Boots, S. Savarese, L. Fei-Fei, and A. Garg, “IRIS: Implicit reinforcement without interaction at scale for learning control from offline robot manipulation data,” in _ICRA_ , 2020, pp. 4414–4420. 

- [89] S.-F. Chen, H.-C. Wang, M.-H. Hsu, C.-M. Lai, and S.-H. Sun, “Diffusion model-augmented behavioral cloning,” in _ICML_ , 2024. 

- [90] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3D Diffusion Policy: Generalizable visuomotor policy learning via simple 3d representations,” in _RSS_ , 2024. 

- [91] T.-W. Ke, N. Gkanatsios, and K. Fragkiadaki, “3D Diffuser Actor: Policy diffusion with 3d scene representations,” in _CoRL_ , 2024. 

- [92] J. Orbik, A. Agostini, and D. Lee, “Inverse reinforcement learning for dexterous hand manipulation,” in _ICDL_ , 2021, pp. 1–7. 

- [93] C. Finn, S. Levine, and P. Abbeel, “Guided cost learning: Deep inverse optimal control via policy optimization,” in _ICML_ , 2016. 

- [94] I. Batzianoulis, F. Iwane, S. Wei, C. Correia, R. Chavarriaga, J. d. R. Millan, and A. Billard, “Customizing skills for assistive robotic manipulators, an inverse reinforcement learning approach with error-related potentials,” _Commun. Biol._ , vol. 4, 2021. 

- [95] J. d. R. Millan, “Error-related eeg potentials generated during simulated brain–computer interaction,” _IEEE Trans. Biomed. Eng._ , vol. 55, pp. 923–9, 04 2008. 

- [96] S. Kumar, J. Zamora, N. Hansen, R. Jangir, and X. Wang, “Graph inverse reinforcement learning from diverse videos,” in _CoRL_ , 2022. 

- [97] F. J. Naranjo-Campos, J. G. Victores, and C. Balaguer, “Experttrajectory-based features for apprenticeship learning via inverse reinforcement learning for robotic manipulation,” _Appl. Sci._ , vol. 14, no. 23, 2024. 

- [98] E. Asali and P. Doshi, “Visual IRL for human-like robotic manipulation,” _arXiv preprint arXiv:2412.11360_ , 2024. 

- [99] R. Ozalp, A. Ucar, and C. Guzelis, “Advancements in deep reinforcement learning and inverse reinforcement learning for robotic manipulation: Toward trustworthy, interpretable, and explainable artificial intelligence,” _IEEE Access_ , vol. 12, pp. 51 840–51 858, 2024. 

- [100] V. Tangkaratt, B. Han, M. E. Khan, and M. Sugiyama, “Variational imitation learning with diverse-quality demonstrations,” in _ICML_ , 2019. 

- [101] Y. Wang, C. Xu, B. Du, and H. Lee, “Learning to weight imperfect demonstrations,” in _ICML_ , 2021, pp. 10 961–10 970. 

- [102] G. Zuo, Q. Zhao, S. Huang, J. Li, and D. Gong, “Adversarial imitation learning with mixed demonstrations from multiple demonstrators,” _Neurocomputing_ , vol. 457, pp. 365–376, 2021. 

- [103] D. Antotsiou, C. Ciliberto, and T.-K. Kim, “Adversarial imitation learning with trajectorial augmentation and correction,” in _ICRA_ , 2021, pp. 4724–4730. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

27 

- [104] N. Liu, T. Lu, Y. Cai, B. Li, and S. Wang, “Hindsight generative adversarial imitation learning,” _arXiv preprint arXiv:1903.07854_ , 2019. 

- [105] D. Jiang, H. Wang, and Y. Lu, “Mastering the complex assembly task with a dual-arm robot: A novel reinforcement learning method,” _IEEE Robot. Autom. Mag._ , vol. 30, no. 2, pp. 57–66, 2023. 

- [106] Z. Wang, J. S. Merel, S. E. Reed, N. de Freitas, G. Wayne, and N. Heess, “Robust imitation of diverse behaviors,” in _NeurIPS_ , 2017. 

- [107] H. Xiao, M. Herman, J. Wagner, S. Ziesche, J. Etesami, and T. H. Linh, “Wasserstein adversarial imitation learning,” _arXiv preprint arXiv:1906.08113_ , 2019. 

- [108] M. Arjovsky, S. Chintala, and L. Bottou, “Wasserstein generative adversarial networks,” in _ICML_ , 2017, pp. 214–223. 

- [109] A. Vahabpour, T. Wang, Q. Lu, O. Pooladzandi, and V. Roychowdhury, “Diverse imitation learning via self-organizing generative models,” _IEEE Trans. Neural Netw. Learn. Syst._ , 2024. 

- [110] Y. Tsurumine and T. Matsubara, “Goal-aware generative adversarial imitation learning from imperfect demonstration for robotic cloth manipulation,” _Robot. Auton. Syst._ , vol. 158, p. 104264, 2022. 

- [111] Z. Shi, X. Zhang, Y. Fang, C. Li, G. Liu, and J. Zhao, “Ranking-based generative adversarial imitation learning,” _IEEE Robot. Autom. Lett_ , 2024. 

- [112] K. Zolna, S. Reed, A. Novikov, S. G. Colmenarejo, D. Budden, S. Cabi, M. Denil, N. de Freitas, and Z. Wang, “Task-relevant adversarial imitation learning,” in _CoRL_ , 2021, pp. 247–263. 

- [113] Y. Tsurumine, Y. Cui, K. Yamazaki, and T. Matsubara, “Generative adversarial imitation learning with deep p-network for robotic cloth manipulation,” in _Humanoids_ , 2019, pp. 274–280. 

- [114] T. Kipf, Y. Li, H. Dai, V. Zambaldi, E. Grefenstette, P. Kohli, and P. Battaglia, “Compositional imitation learning: Explaining and executing one task at a time,” _arXiv preprint arXiv:1812.01483_ , 2018. 

- [115] F. Xie, A. Chowdhury, M. De Paolis Kaluza, L. Zhao, L. Wong, and R. Yu, “Deep imitation learning for bimanual robotic manipulation,” in _NeurIPS_ , 2020, pp. 2327–2337. 

- [116] J. Sun, A. Curtis, Y. You, Y. Xu, M. Koehle, L. Guibas, S. Chitta, M. Schwager, and H. Li, “Hierarchical hybrid learning for long-horizon contact-rich robotic assembly,” _arXiv preprint arXiv:2409.16451_ , 2024. 

- [117] M. Xu, Z. Xu, C. Chi, M. M. Veloso, and S. Song, “Xskill: Cross embodiment skill discovery,” in _CoRL_ , 2023. 

- [118] W. Wan, Y. Zhu, R. Shah, and Y. Zhu, “LOTUS: Continual imitation learning for robot manipulation through unsupervised skill discovery,” in _ICRA_ , 2023, pp. 537–544. 

- [119] C. Wang, L. Fan, J. Sun, R. Zhang, L. Fei-Fei, D. Xu, Y. Zhu, and A. Anandkumar, “MimicPlay: Long-horizon imitation learning by watching human play,” in _CoRL_ , 2023, pp. 201–221. 

- [120] Z. Lin, Y. Chen, and Z. Liu, “Hierarchical human-to-robot imitation learning for long-horizon tasks via cross-domain skill alignment,” in _ICRA_ , 2024, pp. 2783–2790. 

- [121] W. Liang, G. Sun, Q. He, Y. Ren, J. Dong, and Y. Cong, “Neverending behavior-cloning agent for robotic manipulation,” _arXiv preprint arXiv:2403.00336_ , 2024. 

- [122] Z. Liu, J. Zhang, K. Asadi, Y. Liu, D. Zhao, S. Sabach, and R. Fakoor, “TAIL: Task-specific adapters for imitation learning with large pretrained models,” in _ICLR_ , 2024. 

- [123] S. Haldar and L. Pinto, “PolyTask: Learning unified policies through behavior distillation,” _arXiv preprint arXiv:2310.08573_ , 2023. 

- [124] C. Gao, H. Gao, S. Guo, T. Zhang, and F. Chen, “CRIL: Continual robot imitation learning via generative and prediction model,” in _IROS_ , 2021, pp. 6747–5754. 

- [125] A. Mete, H. Xue, A. Wilcox, Y. Chen, and A. Garg, “QueST: Self-supervised skill abstractions for learning continuous control,” in _NeurIPS_ , 2024. 

- [126] S. Yang, W. Zhang, R. Song, J. Cheng, H. Wang, and Y. Li, “Watch and act: Learning robotic manipulation from visual demonstration,” _IEEE Trans. Syst., Man, Cybern., Syst_ , vol. 53, no. 7, pp. 4404–4416, 2023. 

- [127] D. Li, C. Zhao, S. Yang, R. Song, X. Li, and W. Zhang, “MPGNet: Learning move-push-grasping synergy for target-oriented grasping in occluded scenes,” in _IROS_ , 2024, pp. 5064–5071. 

- [128] D. P. Kingma, M. Welling _et al._ , “An introduction to variational autoencoders,” _Found. Trends Mach. Learn._ , vol. 12, no. 4, pp. 307– 392, 2019. 

- [129] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial networks,” _Commun. ACM_ , vol. 63, no. 11, pp. 139–144, 2020. 

- [130] S. Yan, Z. Zhang, M. Han, Z. Wang, Q. Xie, Z. Li, Z. Li, H. Liu, X. Wang, and S.-C. Zhu, “ _M_<sup>2</sup> diffuser: Diffusion-based trajectory optimization for mobile manipulation in 3d scenes,” _IEEE Trans. Pattern Anal. Mach. Intell._ , 2025. 

- [131] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial nets,” in _NeurIPS_ , 2014. 

- [132] J. Gehring, G. Synnaeve, A. Krause, and N. Usunier, “Hierarchical skills for efficient exploration,” in _NeurIPS_ , 2021, pp. 11 553–11 564. 

- [133] P. Jansonnie, B. Wu, J. Perez, and J. Peters, “Unsupervised skill discovery for robotic manipulation through automatic task generation,” in _Humanoids_ , 2024, pp. 926–933. 

- [134] R. Yang, C. Bai, H. Guo, S. Li, B. Zhao, Z. Wang, P. Liu, and X. Li, “Behavior contrastive learning for unsupervised skill discovery,” in _ICML_ , 2023, pp. 39 183–39 204. 

- [135] X. Zhao, H. Wang, W. Huang, and W. Lin, “A statistical theory of regularization-based continual learning,” in _ICML_ , 2024. 

- [136] J. Kirkpatrick, R. Pascanu, N. Rabinowitz, J. Veness, G. Desjardins, A. A. Rusu, K. Milan, J. Quan, T. Ramalho, A. Grabska-Barwinska _et al._ , “Overcoming catastrophic forgetting in neural networks,” _PNAS_ , vol. 114, no. 13, pp. 3521–3526, 2017. 

- [137] S. Li, T. Su, X. Zhang, and Z. Wang, “Continual learning with knowledge distillation: A survey,” _IEEE Trans. Neural Netw. Learn. Syst._ , 2024. 

- [138] D. Rolnick, A. Ahuja, J. Schwarz, T. Lillicrap, and G. Wayne, “Experience replay for continual learning,” in _NeurIPS_ , vol. 32, 2019. 

- [139] C. Yu and P. Wang, “Dexterous manipulation for multi-fingered robotic hands with reinforcement learning: A review,” _Front. Neurorobot._ , vol. 16, p. 861825, 2022. 

- [140] S. Nasiriany, T. Gao, A. Mandlekar, and Y. Zhu, “Learning and retrieval from prior data for skill-based imitation learning,” in _CoRL_ , 2023. 

- [141] H. Kim, Y. Ohmura, and Y. Kuniyoshi, “Using human gaze to improve robustness against irrelevant objects in robot manipulation tasks,” _IEEE Robot. Autom. Lett_ , vol. 5, no. 3, pp. 4415–4422, 2020. 

- [142] M. Ciocarlie, F. M. Hicks, and S. Stanford, “Kinetic and dimensional optimization for a tendon-driven gripper,” in _ICRA_ , 2013, pp. 2751– 2758. 

- [143] P. Sharma, L. Mohan, L. Pinto, and A. Gupta, “Multiple interactions made easy (MIME): Large scale demonstrations data for imitation,” in _CoRL_ , 2018, pp. 906–915. 

- [144] H.-S. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, and C. Lu, “RH20T: A comprehensive robotic dataset for learning diverse skills in one-shot,” in _ICRA_ , 2024, pp. 653–660. 

- [145] F. Ebert, Y. Yang, K. Schmeckpeper, B. Bucher, G. Georgakis, K. Daniilidis, C. Finn, and S. Levine, “Bridge data: Boosting generalization of robotic skills with cross-domain datasets,” in _RSS_ , 2022. 

- [146] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “DROID: A large-scale in-the-wild robot manipulation dataset,” in _RSS_ , 2024. 

- [147] H. Kim, Y. Ohmura, and Y. Kuniyoshi, “Goal-conditioned dual-action imitation learning for dexterous dual-arm robot manipulation,” _IEEE Trans. Robot._ , vol. 40, pp. 2287–2305, 2024. 

- [148] Z. Fu, T. Z. Zhao, and C. Finn, “Mobile ALOHA: Learning bimanual mobile manipulation with low-cost whole-body teleoperation,” in _CoRL_ , 2024. 

- [149] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song, “Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots,” in _RSS_ , 2024. 

- [150] R. R. Ma and A. M. Dollar, “On dexterity and dexterous manipulation,” in _ICAR_ , 2011, pp. 1–7. 

- [151] S. K. Sampath, N. Wang, H. Wu, and C. Yang, “Review on humanlike robot manipulation using dexterous hands.” _Cogn. Comput. Syst._ , vol. 5, no. 1, pp. 14–29, 2023. 

- [152] L. Vianello, L. Penco, W. Gomes, Y. You, S. M. Anzalone, P. Maurice, V. Thomas, and S. Ivaldi, “Human-humanoid interaction and cooperation: a review,” _Curr. Robot. Rep._ , vol. 2, no. 4, pp. 441–454, 2021. 

- [153] U. Kim, D. Jung, H. Jeong, J. Park, H.-M. Jung, J. Cheong, H. R. Choi, H. Do, and C. Park, “Integrated linkage-driven dexterous anthropomorphic robotic hand,” _Nat. Commun._ , vol. 12, no. 1, 2021. 

- [154] Z. Hu, C. Zhou, J. Li, and Q. Hu, “Design of a compact anthropomorphic robotic hand with hybrid linkage and direct actuation,” in _ICIRA_ , 2023, pp. 322–332. 

- [155] S. Robot, “Dexterous hand documentation,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://shadowrobot.com/ dexterous-hand-series/ 

- [156] M. Grebenstein, “The awiwi hand: An artificial hand for the dlr hand arm system,” in _Approaching Human Performance: The FunctionalityDriven Awiwi Robot Hand_ . Springer, 2014, pp. 65–130. 

- [157] E. Ackerman, “This is the most amazing biomimetic anthropomorphic robot hand we’ve ever seen,” 2025, accessed: 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

28 

- Dec. 15, 2025. [Online]. Available: https://spectrum.ieee.org/ biomimetic-anthropomorphic-robot-hand 

- [158] INSPIRE-ROBOTS, “The dexterous hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://en.inspire-robots.com/ product-category/the-dexterous-hands 

- [159] LinkerBot, “Linker hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://linkerbot.cn/data/view 

- [160] T. Ma´nkowski, J. Tomczy´nski, K. Walas, and D. Belter, “Puthand—hybrid industrial and biomimetic gripper for elastic object manipulation,” _Electronics_ , vol. 9, no. 7, p. 1147, 2020. 

- [161] W. Robotics, “Allegro hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.allegrohand.com/v4 

- [162] E. Z. S. R. Lab, “Biomimetic tendon-driven hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.mimicrobotics.com/ 

- [163] Tesla, “Tesla optimus,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://tesla.rocks/2025/06/01/optimus-hand-design/ 

- [164] S. Jacobsen, E. Iversen, D. Knutti, R. Johnson, and K. Biggers, “Design of the Utah/MIT dextrous hand,” in _ICRA_ , vol. 3, 1986, pp. 1520–1532. 

- [165] S. Robot, “Dexterous hand series,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://shadowrobot.com/dexterous-hand-series/ 

- [166] M. Grebenstein, A. Albu-Sch¨affer, T. Bahls, M. Chalon, O. Eiberger, W. Friedl, R. Gruber, S. Haddadin, U. Hagn, R. Haslinger _et al._ , “The DLR hand arm system,” in _ICRA_ , 2011, pp. 3175–3182. 

- [167] M. Grebenstein, M. Chalon, W. Friedl, S. Haddadin, T. Wimb¨ock, G. Hirzinger, and R. Siegwart, “The hand of the dlr hand arm system: Designed for interaction,” _Int. J. Robot. Res._ , vol. 31, no. 13, pp. 1531– 1555, 2012. 

- [168] M. Grebenstein, M. Chalon, G. Hirzinger, and R. Siegwart, “Antagonistically driven finger design for the anthropomorphic dlr hand arm system,” in _Humanoids_ , 2010, pp. 609–616. 

- [169] M. Grebenstein and P. Van der Smagt, “Antagonism for a highly anthropomorphic hand–arm system,” _Adv. Robot._ , vol. 22, no. 1, pp. 39–55, 2008. 

- [170] Y.-J. Kim, J. Yoon, and Y.-W. Sim, “Fluid lubricated dexterous finger mechanism for human-like impact absorbing capability,” _IEEE Robot. Autom. Lett._ , vol. 4, no. 4, pp. 3971–3978, 2019. 

- [171] I. L. KOREATECH, “Fllex hand ver. 2 : Robustness and payload test,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.roboticgizmos.com/f **l** ex-robotic-hand-version-2/ 

- [172] Y. Toshimitsu, B. Forrai, B. G. Cangan, U. Steger, M. Knecht, S. Weirich, and R. K. Katzschmann, “Getting the ball rolling: Learning a dexterous policy for a biomimetic tendon-driven hand with rolling contact joints,” in _Humanoids_ , 2023, pp. 1–7. 

- [173] L. B. Bridgwater, C. Ihrke, M. A. Diftler, M. E. Abdallah, N. A. Radford, J. Rogers, S. Yayathi, R. S. Askew, and D. M. Linn, “The robonaut 2 hand-designed to do work with tools,” in _ICRA_ , 2012, pp. 3425–3430. 

- [174] N. A. Radford, P. Strawser, K. Hambuchen, J. S. Mehling, W. K. Verdeyen, A. S. Donnan, J. Holley, J. Sanchez, V. Nguyen, L. Bridgwater _et al._ , “Valkyrie: Nasa’s first bipedal humanoid robot,” _J. Field Robot._ , vol. 32, no. 3, pp. 397–419, 2015. 

- [175] R. Guo, V. Nguyen, L. Niu, and L. Bridgwater, “Design and analysis of a tendon-driven, under-actuated robotic hand,” in _IDETC-CIE_ , 2014. 

- [176] F. Lotti, P. Tiezzi, G. Vassura, L. Biagiotti, G. Palli, and C. Melchiorri, “Development of UB hand 3: Early results,” in _ICRA_ , 2005. 

- [177] G. Palli, U. Scarcia, C. Melchiorri, and G. Vassura, “Development of robotic hands: The ub hand evolution,” in _IROS_ , 2012, pp. 5456–5457. 

- [178] C. Melchiorri, G. Palli, G. Berselli, and G. Vassura, “Development of the UB Hand IV: Overview of design solutions and enabling technologies,” _IEEE Robot. Autom. Mag._ , vol. 20, no. 3, pp. 72–81, 2013. 

- [179] G. Palli, C. Melchiorri, G. Vassura, U. Scarcia, L. Moriello, G. Berselli, A. Cavallo, G. De Maria, C. Natale, S. Pirozzi _et al._ , “The DEXMART hand: Mechatronic design and experimental evaluation of synergybased control for human-like grasping,” _Int. J. Robot. Res._ , vol. 33, no. 5, pp. 799–824, 2014. 

- [180] B. Siciliano, _Advanced bimanual manipulation: Results from the DEXMART project_ . Springer Science & Business Media, 2012, vol. 80. 

- [181] A. V. Sureshbabu, G. Metta, and A. Parmiggiani, “A new cost effective robot hand for the icub humanoid,” in _Humanoids_ , 2015, pp. 750–757. 

- [182] Z. Xu and E. Todorov, “Design of a highly biomimetic anthropomorphic robotic hand towards artificial limb regeneration,” in _ICRA_ , 2016, pp. 3485–3492. 

- [183] M. Chalon, A. Wedler, A. Baumann, W. Bertleff, A. Beyer, J. Butterfaß, M. Grebenstein, R. Gruber, F. Hacker, E. Kraemer _et al._ , “DEXhand: a space qualified multi-fingered robotic hand,” in _ICRA_ , 2011. 

- [184] M. Maier and M. Chalon, “Spacehand: a multi-fingered robotic hand for space,” _Space_ , 2015. 

- [185] J. Martin and M. Grossard, “Design of a fully modular and backdrivable dexterous hand,” _Int. J. Robot. Res._ , vol. 33, no. 5, pp. 783–798, 2014. 

- [186] L. Liow, A. B. Clark, and N. Rojas, “OLYMPIC: A modular, tendondriven prosthetic hand with novel finger and wrist coupling mechanisms,” _IEEE Robot. Autom. Lett._ , vol. 5, no. 2, pp. 299–306, 2019. 

- [187] DexRobot, “Dexhand 021 mass production,” 2025, accessed: November 27, 2024. [Online]. Available: https://www.dex-robot. com/en/dexhand021Pro 

- [188] M. Leddy, “Underactuated hand with cable-driven fingers,” WO Patent WO2 024 073 138A1, Apr., 2024. 

- [189] P. Technology, “Pudu robotics unveils the PUDU DH11: An 11dof 5-fingered dexterous hand to empower robotic performance,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www. pudurobotics.com/zh-HK/news/956 

- [190] J. Reinecke, M. Chalon, W. Friedl, and M. Grebenstein, “Guiding effects and friction modeling for tendon driven systems,” in _ICRA_ , 2014, pp. 6726–6732. 

- [191] S. Uchiyama, J. Coert, L. Berglund, P. Amadio, and K.-N. An, “Method for the measurement of friction between tendon and pulley,” _J. Orthop. Res._ , vol. 13, no. 1, pp. 83–89, 1995. 

- [192] M. Grebenstein, “Approaching human performance,” Ph.D. dissertation, Springer, 2012. 

- [193] L. Gerez and M. Liarokapis, “A compact ratchet clutch mechanism for fine tendon termination and adjustment,” in _AIM_ , 2018, pp. 1390–1395. 

- [194] G. Palli, G. Borghesan, and C. Melchiorri, “Modeling, identification, and control of tendon-based actuation systems,” _IEEE Trans. Robot._ , vol. 28, no. 2, pp. 277–290, 2011. 

- [195] W. Friedl, M. Chalon, J. Reinecke, and M. Grebenstein, “FRCEF: The new friction reduced and coupling enhanced finger for the awiwi hand,” in _Humanoids_ , 2015, pp. 140–147. 

- [196] M. Grebenstein, M. Chalon, M. A. Roa, and C. Borst, “DLR multifingered hands,” in _Humanoid Robotics: A Reference_ . Springer, 2017, pp. 1–41. 

- [197] S. R. Kashef, S. Amini, and A. Akbarzadeh, “Robotic hand: A review on linkage-driven finger mechanisms of prosthetic hands and evaluation of the performance criteria,” _Mech. Mach. Theory_ , vol. 145, p. 103677, 2020. 

- [198] I. Imbinto, F. Montagnani, M. Bacchereti, C. Cipriani, A. Davalli, R. Sacchetti, E. Gruppioni, S. Castellano, and M. Controzzi, “The S- Finger: a synergetic externally powered digit with tactile sensing and feedback,” _IEEE Trans. Neural Syst. Rehabil. Eng._ , vol. 26, no. 6, pp. 1264–1271, 2018. 

- [199] H. Liu, D. Yang, S. Fan, and H. Cai, “On the development of intrinsically-actuated, multisensory dexterous robotic hands,” _ROBOMECH J._ , vol. 3, no. 1, p. 4, 2016. 

- [200] Ottobock, “Bebionic hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.ottobock.com/en-us/product/8E7----61161 

- [201] C. Medynski and B. Rattray, “Bebionic prosthetic design,” in _MEC Symposium_ , 2011. 

- [202] BrainRobotics, “Brainrobotics hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.brainrobotics.com/ 

- [203] O. Technologies, “Ohand smart prosthesis,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.oymotion.com/product61 

- [204] P. J. Kyberd, C. Light, P. H. Chappell, J. M. Nightingale, D. Whatley, and M. Evans, “The design of anthropomorphic prosthetic hands: A study of the southampton hand,” _Robotica_ , vol. 19, no. 6, pp. 593– 600, 2001. 

- [205] J. Jin, W. Zhang, Z. Sun, and Q. Chen, “LISA Hand: Indirect selfadaptive robotic hand for robust grasping and simplicity,” in _ROBIO_ , 2012, pp. 2393–2398. 

- [206] R. Gopura, D. Bandara, N. Gunasekera, V. Hapuarachchi, and B. Ariyarathna, “A prosthetic hand with self-adaptive fingers,” in _ICCAR_ , 2017, pp. 269–274. 

- [207] D.-p. Yang, J.-d. Zhao, Y.-k. Gu, X.-q. Wang, N. Li, L. Jiang, H. Liu, H. Huang, and D.-w. Zhao, “An anthropomorphic robot hand developed based on underactuated mechanism and controlled by EMG signals,” _J. Bionic Eng._ , vol. 6, no. 3, pp. 255–263, 2009. 

- [208] M. Cheng, L. Jiang, F. Ni, S. Fan, Y. Liu, and H. Liu, “Design of a highly integrated underactuated finger towards prosthetic hand,” in _AIM_ , 2017, pp. 1035–1040. 

- [209] A. ROBOTICS, “Robotic hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.aidinrobotics.co.kr/en/robotic-hand 

- [210] R. Robot, “Dexterous hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: http://ruirobot.cn/acp <u>view.asp?id=269</u> 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

29 

- [211] R. Mahmoud, A. Ueno, and S. Tatsumi, “Dexterous mechanism design for an anthropomorphic artificial hand: Osaka city university hand i,” in _Humanoids_ , 2010, pp. 180–185. 

- [212] H. Iwata and S. Sugano, “Design of anthropomorphic dexterous hand with passive joints and sensitive soft skins,” in _SII_ , 2009, pp. 129–134. 

- [213] D.-H. Lee, J.-H. Park, S.-W. Park, M.-H. Baeg, and J.-H. Bae, “KITECH-hand: A highly dexterous and modularized robotic hand,” _IEEE/ASME Trans. Mechatron._ , vol. 22, no. 2, pp. 876–887, 2016. 

- [214] K. Shaw, A. Agarwal, and D. Pathak, “LEAP hand: Low-cost, efficient, and anthropomorphic hand for robot learning,” in _RSS_ , 2023. 

- [215] H. Liu, K. Wu, P. Meusel, N. Seitz, G. Hirzinger, M. Jin, Y. Liu, S. Fan, T. Lan, and Z. Chen, “Multisensory five-finger dexterous hand: The DLR/HIT Hand II,” in _IROS_ , 2008, pp. 3692–3697. 

- [216] J. Ueda, Y. Ishida, M. Kondo, and T. Ogasawara, “Development of the NAIST-Hand with vision-based tactile fingertip sensor,” in _ICRA_ , 2005, pp. 2332–2337. 

- [217] H. Yang, G. Wei, L. Ren, Z. Qian, K. Wang, H. Xiu, and W. Liang, “An affordable linkage-and-tendon hybrid-driven anthropomorphic robotic hand—mcr-hand ii,” _J. Mech. Robot._ , vol. 13, no. 2, p. 024502, 2021. 

- [218] ——, “A low-cost linkage-spring-tendon-integrated compliant anthropomorphic robotic hand: MCR-Hand III,” _Mech. Mach. Theory_ , vol. 158, p. 104210, 2021. 

- [219] R. Abayasiri, R. Abayasiri, R. Gunawardhana, R. Premakumara, S. Mallikarachchi, R. Gopura, T. D. Lalitharatne, and D. Madusanka, “An under-actuated hand prosthesis with finger abduction and adduction for human like grasps,” in _ICCAR_ , 2020, pp. 574–580. 

- [220] K. Shaw and D. Pathak, “LEAP hand v2: Dexterous, low-cost anthropomorphic hybrid rigid soft hand for robot learning,” in _RSS_ , 2024. 

- [221] M. S. Johannes, J. D. Bigelow, J. M. Burck, S. D. Harshbarger, M. V. Kozlowski, and T. Van Doren, “An overview of the developmental process for the modular prosthetic limb,” _Johns Hopkins APL Tech. Dig._ , vol. 30, no. 3, pp. 207–216, 2011. 

- [222] P. Slade, A. Akhtar, M. Nguyen, and T. Bretl, “Tact: Design and performance of an open-source, affordable, myoelectric prosthetic hand,” in _ICRA_ , 2015, pp. 6451–6456. 

- [223] N. E. Krausz, R. A. Rorrer _et al._ , “Design and fabrication of a six degree-of-freedom open source hand,” _IEEE Trans. Neural Syst. Rehabil. Eng._ , vol. 24, no. 5, pp. 562–572, 2015. 

- [224] M. Owen, C. Au, and A. Fowke, “Development of a dexterous prosthetic hand,” _J. Comput. Inf. Sci. Eng._ , vol. 18, no. 1, 2018. 

- [225] W. Ryu, Y. Choi, Y. J. Choi, Y. G. Lee, and S. Lee, “Development of an anthropomorphic prosthetic hand with underactuated mechanism,” _Appl. Sci._ , vol. 10, no. 12, p. 4384, 2020. 

- [226] A. Ke, J. Huang, and J. He, “A new anthropomorphic thumb configuration with passive finger torsion,” in _ICMA_ . IEEE, 2021, pp. 890–896. 

- [227] R. Robots, “Barrett hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://barrett.com/barretthand 

- [228] L. U. Odhner, L. P. Jentoft, M. R. Claffee, N. Corson, Y. Tenzer, R. R. Ma, M. Buehler, R. Kohout, R. D. Howe, and A. M. Dollar, “A compliant, underactuated hand for robust manipulation,” _Int. J. Robot. Res._ , vol. 33, no. 5, pp. 736–752, 2014. 

- [229] A. Bicchi, “Hands for dexterous manipulation and robust grasping: A difficult road toward simplicity,” _IEEE Trans. Robot. Autom._ , vol. 16, no. 6, pp. 652–662, 2002. 

- [230] E. Pe˜na Pitarch, “Virtual human hand: Grasping strategy and simulation,” Ph.D. dissertation, 2008. 

- [231] X. Yang, J. Park, K. Jung, and H. You, “Development and evaluation of a 25-degree of freedom hand kinematic model,” _J. Ergon. Soc. Korea_ , pp. 517–520, 2008. 

- [232] A.-A. Samadani, D. Kuli´c, and R. Gorbet, “Multi-constrained inverse kinematics for the human hand,” in _EMBC_ , 2012, pp. 6780–6784. 

- [233] J. Lenarcic, T. Bajd, and M. M. Staniˇsi´c, _Robot Mechanisms_ . Springer Netherlands, 2013, vol. 60. 

- [234] N. M. Thalmann, L. Tian, and F. Yao, “Nadine: A social robot that can localize objects and grasp them in a human way,” in _Front. Electron. Technol._ Springer, 2017, pp. 1–23. 

- [235] J. Zhou, J. Yi, X. Chen, Z. Liu, and Z. Wang, “BCL-13: A 13-dof soft robotic hand for dexterous grasping and in-hand manipulation,” _IEEE Robot. Autom. Lett._ , vol. 3, no. 4, pp. 3379–3386, 2018. 

- [236] M. Zarzoura, P. Del Moral, M. I. Awad, and F. A. Tolbah, “Investigation into reducing anthropomorphic hand degrees of freedom while maintaining human hand grasping functions,” _Proc. Inst. Mech. Eng. H_ , vol. 233, no. 2, pp. 279–292, 2019. 

- [237] L.-A. A. Demers and C. Gosselin, “Kinematic design of a planar and spherical mechanism for the abduction of the fingers of an anthropomorphic robotic hand,” in _ICRA_ , 2011, pp. 5350–5356. 

- [238] H. Mnyusiwalla, P. Vulliez, J.-P. Gazeau, and S. Zeghloul, “A new dexterous hand based on bio-inspired finger design for inside-hand manipulation,” _IEEE Trans. Syst., Man, Cybern., Syst._ , vol. 46, no. 6, pp. 809–817, 2015. 

- [239] T. Feix, J. Romero, C. H. Ek, H.-B. Schmiedmayer, and D. Kragic, “A metric for comparing the anthropomorphic motion capability of artificial hands,” _IEEE Trans. Robot._ , vol. 29, no. 1, pp. 82–93, 2012. 

- [240] T. Wang, Z. Xie, Y. Li, Y. Zhang, H. Zhang, and F. Kirchner, “DoraHand: a novel dexterous hand with tactile sensing finger module,” _Ind. Robot_ , vol. 49, no. 4, pp. 658–666, 2022. 

- [241] S. Robot, “DEX-EE,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://shadowrobot.com/dex-ee/ 

- [242] iF Design, “Dorahand-3f robot hand,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://ifdesign.com/en/winner-ranking/ project/dorahand-3f/336442 

- [243] W. Hu, B. Huang, W. W. Lee, S. Yang, Y. Zheng, and Z. Li, “Dexterous in-hand manipulation of slender cylindrical objects through deep reinforcement learning with tactile sensing,” _Robot. Auton. Syst._ , vol. 186, p. 104904, 2025. 

- [244] W. Townsend, “The BarrettHand grasper–programmably flexible part handling and assembly,” _Ind. Robot_ , vol. 27, no. 3, pp. 181–188, 2000. 

- [245] R. Ma and A. Dollar, “Yale openhand project: Optimizing open-source hand designs for ease of fabrication and adoption,” _IEEE Robot. Autom. Mag._ , vol. 24, no. 1, pp. 32–40, 2017. 

- [246] H. Zhu, A. Gupta, A. Rajeswaran, S. Levine, and V. Kumar, “Dexterous manipulation with deep reinforcement learning: Efficient, general, and low-cost,” in _ICRA_ , 2019, pp. 3651–3657. 

- [247] M. Wuthrich, F. Widmaier, F. Grimminger, S. Joshi, V. Agrawal, B. Hammoud, M. Khadiv, M. Bogdanovic, V. Berenz, J. Viereck _et al._ , “TriFinger: An open-source robot for learning dexterity,” in _CoRL_ , 2021, pp. 1871–1882. 

- [248] G. Li, X. Liang, Y. Gao, T. Su, Z. Liu, and Z.-G. Hou, “A linkagedriven underactuated robotic hand for adaptive grasping and in-hand manipulation,” _IEEE Trans. Autom. Sci. Eng._ , vol. 21, no. 3, pp. 3039– 3051, 2023. 

- [249] J. Xu, S. Li, H. Luo, H. Liu, X. Wang, W. Ding, and C. Xia, “MuxHand: A cable-driven dexterous robotic hand using time-division multiplexing motors,” _arXiv preprint arXiv:2409.12455_ , 2024. 

- [250] Y.-J. Kim, H. Song, and C.-Y. Maeng, “BLT gripper: An adaptive gripper with active transition capability between precise pinch and compliant grasp,” _IEEE Robot. Autom. Lett._ , vol. 5, no. 4, pp. 5518– 5525, 2020. 

- [251] T. Lalibert´e and C. M. Gosselin, “Underactuation in space robotic hands,” in _ISAIRAS_ , 2001. 

- [252] R. Bhirangi, A. DeFranco, J. Adkins, C. Majidi, A. Gupta, T. Hellebrekers, and V. Kumar, “All the feels: A dexterous hand with large-area tactile sensing,” _IEEE Robot. Autom. Lett._ , vol. 8, no. 12, pp. 8311– 8318, 2023. 

- [253] Kinova, “Robotic arm,” 2025, accessed: Dec. 15, 2025. [Online]. Available: https://www.kinovarobotics.com 

- [254] T. Ueno, S. Funabashi, H. Ito, A. Schmitz, S. Kulkarni, T. Ogata, and S. Sugano, “Multi-fingered dragging of unknown objects and orientations using distributed tactile information through vision-transformer and lstm,” in _IROS_ , 2024, pp. 7445–7452. 

- [255] P. Lin, Y. Huang, W. Li, J. Ma, C. Xiao, and Z. Jiao, “PP-Tac: Paper picking using tactile feedback in dexterous robotic hands,” in _RSS_ , 2025. 

- [256] K.-W. Lee, Y. Qin, X. Wang, and S.-C. Lim, “Dextouch: Learning to seek and manipulate objects with tactile dexterity,” _IEEE Robot. Autom. Lett_ , 2024. 

- [257] J. Huang, K. Chen, J. Zhou, X. Lin, P. Abbeel, Q. Dou, and Y. Liu, “DiH-Tele: Dexterous in-hand teleoperation framework for learning multiobjects manipulation with tactile sensing,” _IEEE/ASME Trans. Mechatron._ , 2025. 

- [258] L. Heng, H. Geng, K. Zhang, P. Abbeel, and J. Malik, “ViTacFormer: Learning cross-modal representation for visuo-tactile dexterous manipulation,” _arXiv preprint arXiv:2506.15953_ , 2025. 

- [259] D. Zhang, C. Yuan, C. Wen, H. Zhang, J. Zhao, and Y. Gao, “KineDex: Learning tactile-informed visuomotor policies via kinesthetic teaching for dexterous manipulation,” _arXiv preprint arXiv:2505.01974_ , 2025. 

- [260] M. Hailiang, S. Yixiao, P. Junjie, and B. Guanjun, “Flexible tactile sensor arrays with capacitive and resistive dual-mode transduction,” _IEEE Sens. J._ , vol. 24, no. 10, pp. 15 892–15 899, 2024. 

- [261] X. Liu, W. Yang, F. Meng, and T. Sun, “Material recognition using robotic hand with capacitive tactile sensor array and machine learning,” _IEEE Trans. Instrum. Meas._ , vol. 73, pp. 1–9, 2024. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

30 

- [262] Y. Chen, J. Cao, J. Qiu, D. Yang, M. Liu, M. Zhang, C. Li, Z. Wu, J. Yu, X. Zhang _et al._ , “Capacitive in-sensor tactile computing,” _Nat. Commun._ , vol. 16, no. 1, p. 5691, 2025. 

- [263] X. Wang, C. Lin, C. Yang, Z. Liu, Y. Sheng, K. Li, L. Huang, and H. Liu, “PiezoTac: Fingerprint-inspired piezoelectric tactile sensing for enhanced texture discrimination,” in _ICACI_ , 2025, pp. 211–218. 

- [264] J. Tang, Y. Li, Y. Yu, Q. Hu, W. Du, and D. Lin, “Recent progress in flexible piezoelectric tactile sensors: Materials, structures, fabrication, and application,” _Sensors (Basel)_ , vol. 25, no. 3, p. 964, 2025. 

- [265] W. Yuan, S. Dong, and E. H. Adelson, “GelSight: High-resolution robot tactile sensors for estimating geometry and force,” _Sensors_ , vol. 17, no. 12, p. 2762, 2017. 

- [266] B. Ward-Cherrier, N. Pestell, L. Cramphorn, B. Winstone, M. E. Giannaccini, J. Rossiter, and N. F. Lepora, “The TacTip family: Soft optical tactile sensors with 3d-printed biomimetic morphologies,” _Soft Robot._ , vol. 5, no. 2, pp. 216–227, 2018. 

- [267] B. Zhang, S. Cui, C. Zhang, J. Hu, R. Wang, and S. Wang, “GelStereo Tip: A spherical fingertip visuotactile sensor for multi-finger screwing manipulation,” _IEEE Trans. Autom. Sci. Eng._ , 2025. 

- [268] Y. Sun, N. Cheng, S. Zhang, W. Li, L. Yang, S. Cui, H. Liu, F. Sun, J. Zhang, D. Guo _et al._ , “Tactile data generation and applications based on visuo-tactile sensors: A review,” _Inf. Fusion_ , vol. 121, 2025. 

- [269] Y. Yan, Z. Hu, Z. Yang, W. Yuan, C. Song, J. Pan, and Y. Shen, “Soft magnetic skin for super-resolution tactile sensing with force selfdecoupling,” _Sci. Robot._ , vol. 6, no. 51, p. eabc8801, 2021. 

- [270] Y. Yan, Y. Shen, C. Song, and J. Pan, “Tactile super-resolution model for soft magnetic skin,” _IEEE Robot. Autom. Lett_ , vol. 7, no. 2, pp. 2589–2596, 2022. 

- [271] S. Park, S.-R. Oh, and D. Hwang, “MagTac: Magnetic six-axis force/torque fingertip tactile sensor for robotic hand applications,” in _ICRA_ , 2023, pp. 10 367–10 372. 

- [272] X. Ding, X. Wang, Y. Zhang, S. Yao, Y. Zheng, F. Sun, J. Shan, and B. Fang, “Soft magnetic skin with motion and contact sensing for anthropomorphic robotic finger,” _IEEE Robot. Autom. Lett_ , 2024. 

- [273] N. Wettels, J. A. Fishel, and G. E. Loeb, “Multimodal tactile sensor,” in _The human hand as an inspiration for robot hand development_ . Springer, 2014, pp. 405–429. 

- [274] T. Taunyazov, W. Sng, H. H. See, B. Lim, J. Kuan, A. F. Ansari, B. C. Tee, and H. Soh, “Event-driven visual-tactile sensing and learning for robots,” in _RSS_ , 2020. 

- [275] Z. Lu, X. Gao, and H. Yu, “GTac: A biomimetic tactile sensor with skin-like heterogeneous force feedback for robots,” _IEEE Sens. J._ , vol. 22, no. 14, pp. 14 491–14 500, 2022. 

- [276] T. Ablett, O. Limoyo, A. Sigal, A. Jilani, J. Kelly, K. Siddiqi, F. Hogan, and G. Dudek, “Multimodal and force-matched imitation learning with a see-through visuotactile sensor,” _IEEE Trans. Robot._ , 2024. 

- [277] I. Guzey, Y. Dai, B. Evans, S. Chintala, and L. Pinto, “See to touch: Learning tactile dexterity through visual incentives,” in _ICRA_ , 2024, pp. 13 825–13 832. 

- [278] M. Murooka, T. Hoshi, K. Fukumitsu, S. Masuda, M. Hamze, T. Sasaki, M. Morisawa, and E. Yoshida, “TACT: Humanoid whole-body contact manipulation through deep imitation learning with tactile modality,” _IEEE Robot. Autom. Lett_ , 2025. 

- [279] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. HansenEstruch, A. W. He, V. Myers, M. J. Kim, M. Du _et al._ , “BridgeData V2: A dataset for robot learning at scale,” in _CoRL_ , 2023, pp. 1723–1736. 

- [280] S. Suresh, H. Qi, T. Wu, T. Fan, L. Pineda, M. Lambeta, J. Malik, M. Kalakrishnan, R. Calandra, M. Kaess _et al._ , “Neuralfeels with neural fields: Visuotactile perception for in-hand manipulation,” _Sci. Robot._ , vol. 9, no. 96, p. eadl0628, 2024. 

- [281] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel, “Domain randomization for transferring deep neural networks from simulation to the real world,” in _IROS_ , 2017, pp. 23–30. 

- [282] Z. Wan, Z. Bi, Z. Zhou, H. Ren, Y. Zeng, Y. Li, L. Qi, X. Yang, M.-H. Yang, and H. Cheng, “Rapid hand: A robust, affordable, perceptionintegrated, dexterous manipulation platform for generalist robot autonomy,” _arXiv preprint arXiv:2506.07490_ , 2025. 

- [283] S. Li, X. Ma, H. Liang, M. G¨orner, P. Ruppel, B. Fang, F. Sun, and J. Zhang, “Vision-based teleoperation of shadow dexterous hand using end-to-end deep neural network,” in _ICRA_ , 2019, pp. 416–422. 

- [284] S. Li, N. Hendrich, H. Liang, P. Ruppel, C. Zhang, and J. Zhang, “A dexterous hand-arm teleoperation system based on hand pose estimation and active vision,” _IEEE Trans. Cybern._ , vol. 54, no. 3, pp. 1417–1428, 2022. 

- [285] S. Yang, M. Liu, Y. Qin, R. Ding, J. Li, X. Cheng, R. Yang, S. Yi, and X. Wang, “ACE: A cross-platform visual-exoskeletons system for low-cost dexterous teleoperation,” in _CoRL_ , 2024. 

- [286] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, J. Gao, J. Emmons, A. Gupta, E. Orbay _et al._ , “RoboTurk: A crowdsourcing platform for robotic skill learning through imitation,” in _CoRL_ , 2018, pp. 879–893. 

- [287] M. Caeiro-Rodr´ıguez, I. Otero-Gonz´alez, F. A. Mikic-Fonte, and M. Llamas-Nistal, “A systematic review of commercial smart gloves: Current status and applications,” _Sensors_ , vol. 21, no. 8, p. 2667, 2021. 

- [288] M. Mosbach, K. Moraw, and S. Behnke, “Accelerating interactive human-like manipulation learning with gpu-based simulation and highquality demonstrations,” in _Humanoids_ , 2022, pp. 435–441. 

- [289] S. P. Arunachalam, I. G¨uzey, S. Chintala, and L. Pinto, “Holo-Dex: Teaching dexterity with immersive mixed reality,” in _ICRA_ , 2023, pp. 5962–5969. 

- [290] I. Radosavovic, T. Xiao, S. James, P. Abbeel, J. Malik, and T. Darrell, “Real-world robot learning with masked visual pre-training,” in _CoRL_ , 2023, pp. 416–426. 

- [291] R. Ding, Y. Qin, J. Zhu, C. Jia, S. Yang, R. Yang, X. Qi, and X. Wang, “Bunny-VisionPro: Real-time bimanual dexterous teleoperation for imitation learning,” in _IROS_ , 2024. 

- [292] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang, “Open-TeleVision: teleoperation with immersive active visual feedback,” in _CoRL_ , 2024. 

- [293] T. Lin, Y. Zhang, Q. Li, H. Qi, B. Yi, S. Levine, and J. Malik, “Learning visuotactile skills with two multifingered hands,” in _ICRA_ , 2025. 

- [294] F. Falck, K. Larppichet, and P. Kormushev, “DE VITO: A dual-arm, high degree-of-freedom, lightweight, inexpensive, passive upper-limb exoskeleton for robot teleoperation,” in _TAROS_ , 2019, pp. 78–89. 

- [295] F. Falck, S. Doshi, N. Smuts, J. Lingi, K. Rants, and P. Kormushev, “Human-centered manipulation and navigation with Robot DE NIRO,” in _IROS_ , 2018. 

- [296] H. Fang, H.-S. Fang, Y. Wang, J. Ren, J. Chen, R. Zhang, W. Wang, and C. Lu, “AirExo: low-cost exoskeletons for learning whole-arm manipulation in the wild,” in _ICRA_ , 2024, pp. 15 031–15 038. 

- [297] H. Kim, Y. Ohmura, A. Nagakubo, and Y. Kuniyoshi, “Training robots without robots: deep imitation learning for master-to-robot policy transfer,” _IEEE Robot. Autom. Lett_ , vol. 8, no. 5, pp. 2906–2913, 2023. 

- [298] P. Wu, Y. Shentu, Z. Yi, X. Lin, and P. Abbeel, “GELLO: A general, low-cost, and intuitive teleoperation framework for robot manipulators,” in _IROS_ , 2024. 

- [299] N. Sian, K. Yokoi, S. Kajita, F. Kanehiro, and K. Tanie, “Whole body teleoperation of a humanoid robot - development of a simple master device using joysticks,” in _IROS_ , vol. 3, 2002, pp. 2569–2574 vol.3. 

- [300] A. Toedtheide, X. Chen, H. Sadeghian, A. Naceri, and S. Haddadin, “A force-sensitive exoskeleton for teleoperation: An application in elderly care robotics,” in _ICRA_ , 2023, pp. 12 624–12 630. 

- [301] S. Song, A. Zeng, J. Lee, and T. Funkhouser, “Grasping in the wild: Learning 6dof closed-loop grasping from low-cost demonstrations,” _IEEE Robot. Autom. Lett_ , vol. 5, no. 3, pp. 4978–4985, 2020. 

- [302] M. V. Liarokapis, P. K. Artemiadis, and K. J. Kyriakopoulos, “Mapping human to robot motion with functional anthropomorphism for teleoperation and telemanipulation with robot arm hand systems,” in _IROS_ , 2013, pp. 2075–2075. 

- [303] S. Han, B. Liu, R. Wang, Y. Ye, C. D. Twigg, and K. Kin, “Online optical marker-based hand tracking with deep labels,” _ACM Trans. Graph._ , vol. 37, no. 4, pp. 1–10, 2018. 

- [304] V. Kumar and E. Todorov, “MuJoCo HAPTIX: A virtual reality system for hand manipulation,” in _Humanoids_ , 2015, pp. 657–663. 

- [305] S. Li, J. Jiang, P. Ruppel, H. Liang, X. Ma, N. Hendrich, F. Sun, and J. Zhang, “A mobile robot hand-arm teleoperation system by vision and imu,” in _IROS_ , 2020, pp. 10 900–10 906. 

- [306] O. Taheri, N. Ghorbani, M. J. Black, and D. Tzionas, “GRAB: A dataset of whole-body human grasping of objects,” in _ECCV_ , 2020, pp. 581– 600. 

- [307] H. Hedayati, M. Walker, and D. Szafir, “Improving collocated robot teleoperation with augmented reality,” in _HRI_ , 2018, pp. 78–86. 

- [308] M. Seo, S. Han, K. Sim, S. H. Bang, C. Gonzalez, L. Sentis, and Y. Zhu, “Deep imitation learning for humanoid loco-manipulation through human teleoperation,” in _Humanoids_ , 2023, pp. 1–8. 

- [309] J. Duan, Y. R. Wang, M. Shridhar, D. Fox, and R. Krishna, “AR2D2:training a robot without a robot,” in _CoRL_ , 2023. 

- [310] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn, “BC-Z: Zero-shot task generalization with robotic imitation learning,” in _CoRL_ , 2022, pp. 991–1002. 

- [311] J. I. Lipton, A. J. Fay, and D. Rus, “Baxter’s homunculus: Virtual reality spaces for teleoperation in manufacturing,” _IEEE Robot. Autom. Lett_ , vol. 3, no. 1, pp. 179–186, 2018. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

31 

- [312] D. Krupke, F. Steinicke, P. Lubos, Y. Jonetzko, M. G¨orner, and J. Zhang, “Comparison of multimodal heading and pointing gestures for co-located mixed reality human-robot interaction,” in _IROS_ , 2018. 

- [313] E. Rosen, D. Whitney, M. Fishman, D. Ullman, and S. Tellex, “Mixed reality as a bidirectional communication interface for human-robot interaction,” in _IROS_ , 2020, pp. 11 431–11 438. 

- [314] Y. Qin, Y.-H. Wu, S. Liu, H. Jiang, R. Yang, Y. Fu, and X. Wang, “DexMV: Imitation learning for dexterous manipulation from human videos,” in _ECCV_ , 2022, pp. 570–587. 

- [315] H. Bharadhwaj, R. Mottaghi, A. Gupta, and S. Tulsiani, “Track2Act: Predicting point tracks from internet videos enables generalizable robot manipulation,” in _ECCV_ , 2024, pp. 306–324. 

- [316] H. Bharadhwaj, D. Dwibedi, A. Gupta, S. Tulsiani, C. Doersch, T. Xiao, D. Shah, F. Xia, D. Sadigh, and S. Kirmani, “Gen2Act: Human video generation in novel scenarios enables generalizable robot manipulation,” in _CoRL_ , 2025. 

- [317] M. Albaba, C. Li, M. Diomataris, O. Taheri, A. Krause, and M. Black, “NIL: No-data imitation learning by leveraging pre-trained video diffusion models,” _arXiv preprint arXiv:2503.10626_ , 2025. 

- [318] P. Li, T. Liu, Y. Li, M. Han, H. Geng, S. Wang, Y. Zhu, S.-C. Zhu, and S. Huang, “Ag2Manip: Learning novel manipulation skills with agent-agnostic visual and action representations,” in _IROS_ , 2024, pp. 573–580. 

- [319] J. Gao, X. Jin, F. Krebs, N. Jaquier, and T. Asfour, “Bi-KVIL: Keypoints-based visual imitation learning of bimanual manipulation tasks,” in _ICRA_ , 2024, pp. 16 850–16 857. 

- [320] D. Yang, D. Tjia, J. Berg, D. Damen, P. Agrawal, and A. Gupta, “Rank2Reward: Learning shaped reward functions from passive video,” in _ICRA_ , 2024, pp. 2806–2813. 

- [321] Z. Chen, S. Chen, E. Arlaud, I. Laptev, and C. Schmid, “ViViDex: Learning vision-based dexterous manipulation from human videos,” in _ICRA_ , 2025. 

- [322] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar, “RoboAgent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking,” in _ICRA_ , 2024, pp. 4788–4795. 

- [323] A. Mandlekar, S. Nasiriany, B. Wen, I. Akinola, Y. Narang, L. Fan, Y. Zhu, and D. Fox, “MimicGen: A data generation system for scalable robot learning using human demonstrations,” in _CoRL_ , 2023, pp. 1820– 1864. 

- [324] Z. Fan, O. Taheri, D. Tzionas, M. Kocabas, M. Kaufmann, M. J. Black, and O. Hilliges, “ARCTIC: A dataset for dexterous bimanual handobject manipulation,” in _CVPR_ , 2023, pp. 12 943–12 954. 

- [325] R. Wang, J. Zhang, J. Chen, Y. Xu, P. Li, T. Liu, and H. Wang, “DexGraspNet: A large-scale robotic dexterous grasp dataset for general objects based on simulation,” in _ICRA_ , 2023, pp. 11 359–11 366. 

- [326] X. Zhan, L. Yang, Y. Zhao, K. Mao, H. Xu, Z. Lin, K. Li, and C. Lu, “OAKINK2: A dataset of bimanual hands-object manipulation in complex task completion,” in _CVPR_ , 2024, pp. 445–456. 

- [327] H. G. Singh, A. Loquercio, C. Sferrazza, J. Wu, H. Qi, P. Abbeel, and J. Malik, “Hand-object interaction pretraining from videos,” in _ICRA_ , 2025. 

- [328] K. Shaw, S. Bahl, and D. Pathak, “VideoDex: Learning dexterity from internet videos,” in _CoRL_ , 2023, pp. 654–665. 

- [329] J. Wang, Y. Qin, K. Kuang, Y. Korkmaz, A. Gurumoorthy, H. Su, and X. Wang, “CyberDemo: Augmenting simulated human demonstration for real-world dexterous manipulation,” in _CVPR_ , 2024. 

- [330] R. Hoque, A. Mandlekar, C. Garrett, K. Goldberg, and D. Fox, “IntervenGen: Interventional data generation for robust and data-efficient robot imitation learning,” in _IROS_ , 2024. 

- [331] Y. Jin, J. Lv, S. Jiang, and C. Lu, “DiffGen: Robot demonstration generation via differentiable physics simulation, differentiable rendering, and vision-language model,” _arXiv preprint arXiv:2405.07309_ , 2024. 

- [332] E. Tzeng, J. Hoffman, K. Saenko, and T. Darrell, “Adversarial discriminative domain adaptation,” in _CVPR_ , 2017, pp. 7167–7176. 

- [333] J. Achiam, D. Held, A. Tamar, and P. Abbeel, “Constrained policy optimization,” in _ICML_ , 2017, pp. 22–31. 

- [334] Y. Chow, O. Nachum, E. Duenez-Guzman, and M. Ghavamzadeh, “A lyapunov-based approach to safe reinforcement learning,” in _NeurIPS_ , vol. 31, 2018. 

- [335] N. Milosevic, J. M¨uller, and N. Scherf, “Embedding safety into rl: A new take on trust region methods,” in _ICML_ , 2025. 

- [336] S. M. Khansari-Zadeh and A. Billard, “Learning stable nonlinear dynamical systems with gaussian mixture models,” _IEEE Trans. Robot._ , vol. 27, no. 5, pp. 943–957, 2011. 

- [337] S. Xu, Y. Ou, Z. Wang, J. Duan, and H. Li, “Learning-based kinematic control using position and velocity errors for robot trajectory tracking,” _IEEE Trans. Syst., Man, Cybern.: Syst_ , vol. 52, no. 2, pp. 1100–1110, 2020. 

- [338] S. Xu, J. Liu, C. Yang, X. Wu, and T. Xu, “A learning-based stable servo control strategy using broad learning system applied for microrobotic control,” _IEEE Trans. Cybern._ , vol. 52, no. 12, pp. 13 727– 13 737, 2021. 

- [339] Y.-C. Chang, N. Roohi, and S. Gao, “Neural lyapunov control,” in _NeurIPS_ , vol. 32, 2019. 

- [340] W. Xiao, T.-H. Wang, C. Gan, R. Hasani, M. Lechner, and D. Rus, “SafeDiffuser: Safe planning with diffusion probabilistic models,” in _ICLR_ , 2023. 

- [341] G. An, J. Lee, X. Zuo, N. Kosaka, K.-M. Kim, and H. O. Song, “Direct preference-based policy optimization without reward modeling,” in _NeurIPS_ , vol. 36, 2023, pp. 70 247–70 266. 

- [342] N. Das, S. Bechtle, T. Davchev, D. Jayaraman, A. Rai, and F. Meier, “Model-based inverse reinforcement learning from visual demonstrations,” in _CoRL_ , 2021, pp. 1930–1942. 

- [343] E. Trevisan and J. Alonso-Mora, “Biased-mppi: Informing samplingbased model predictive control by fusing ancillary controllers,” _IEEE Robot. Autom. Lett_ , vol. 9, no. 6, pp. 5871–5878, 2024. 

- [344] S. Bansal, J. Xu, A. Howard, and C. Isbell, “A bayesian framework for nash equilibrium inference in human-robot parallel play,” in _RSS_ , 2020. 

- [345] S. James, Z. Ma, D. Rovick Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robot. Autom. Lett_ , 2020. 

- [346] S. Tao _et al._ , “ManiSkill3: GPU Parallelized Robotics Simulation and Rendering for Generalizable Embodied AI,” in _RSS_ , 2025. 

- [347] S. Zhong, Y. Hou, Q. Shi, Y. Li, H.-W. Huang, Q. Huang, T. Fukuda, and H. Wang, “Spatial constraint-based navigation and emergency replanning adaptive control for magnetic helical microrobots in dynamic environments,” _IEEE Trans. Autom. Sci. Eng._ , vol. 21, no. 4, pp. 7180– 7189, 2023. 

- [348] Z. Xin, S. Zhong, A. Wu, Z. Zheng, Q. Shi, Q. Huang, T. Fukuda, and H. Wang, “Dynamic control of multimodal motion for bistable soft millirobots in complex environments,” _IEEE Trans. Robot._ , 2025. 

- [349] H. Wang, S. Zhong, Z. Zheng, Q. Shi, T. Sun, Q. Huang, and T. Fukuda, “Data-driven parallel adaptive control for magnetic helical microrobots with derivative structure in uncertain environments,” _IEEE Trans. Syst., Man, Cybern.: Syst_ , vol. 54, no. 7, pp. 4139–4150, 2024. 

- [350] Y. Dong, L. Wang, N. Xia, Z. Yang, C. Zhang, C. Pan, D. Jin, J. Zhang, C. Majidi, and L. Zhang, “Untethered small-scale magnetic soft robot with programmable magnetization and integrated multifunctional modules,” _Sci. Adv._ , vol. 8, no. 25, p. eabn8932, 2022. 

**Shan An (Senior Member, IEEE)** received the B.E. degree from Tianjin University in 2007, the M.E. degree from Shandong University in 2010, and the Ph.D. degree in computer science and engineering from Beihang University in 2022. He is currently an Associate Professor with the School of Electrical and Information Engineering, Tianjin University. His research interests include dexterous manipulation, extended reality for robotics, and robotic vision. Prior to his academic career, he accumulated 14 years of extensive industrial experience at the China Academy of Space Technology, Alibaba, and JD Group. He was elected Fellow of the Institution of Engineering and Technology (IET) in 2023 and Fellow of the British Computer Society (BCS) in 2024. 

**Ziyu Meng** received the B.S. degree from Shandong University, Jinan, China, in 2022. He is currently pursuing the Ph.D. degree in pattern recognition and intelligent systems at Shandong University, Jinan, China. His current research interests include wholebody control for humanoid robots. 


JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 14, NO. 8, DEC. 2025 

32 


**Chao Tang** is currently a postdoctoral researcher at the Division of Robotics, Perception and Learning, KTH Royal Institute of Technology. He received his Ph.D. degree from Southern University of Science and Technology in 2025 and his M.S. degree from the Georgia Institute of Technology in 2020. His research interests include robotic manipulation and grasping, mobile manipulation, human–robot interaction, and semantic reasoning for robots. 

**Yuning Zhou** received the B.E. degree in Mechanical Engineering from the University of Leeds and Southwest Jiaotong University (dual-degree program) in 2022, and the M.Sc. degree in Robotics, Systems and Control from ETH Zurich in 2025. His research interests include the design, simulation, and benchmarking of anthropomorphic robotic hands. 


**Shufang Zhang** is currently an associate professor in the School of Electrical and Information Engineering, Tianjin University, Tianjin, China. She received her M.S. and Ph.D. degrees from Tianjin University in 2004 and 2007, respectively. Her research interests include Robot and SLAM, Artificial Intelligence, and Embodied Intelligence. 

**Ran Song (Senior Member, IEEE)** is a Professor with the School of Control Science and Engineering, Shandong University, China since 2020. Before his current post, he was a senior lecturer at the University of Brighton, UK. He received his Ph.D. degree in electronic engineering from the University of York, UK in 2009 and his first degree from Shandong University in 2005. He has published more than 100 papers in peer-reviewed international conference proceedings and journals. His research interests lie in 3D visual perception, 3D vision for 

robotics, and robot learning. 

**Tengyu Liu** received the B.S. degree in computer science from the University of Illinois UrbanaChampaign (UIUC), Champaign, IL, USA, and the M.S. and Ph.D. degrees in computer science from the University of California, Los Angeles (UCLA), Los Angeles, CA, USA, in 2021. He is currently a Senior Research Scientist at Beijing Institute of General Artificial Intelligence (BIGAI), Beijing, China. His research interests lie at the intersection of 3D computer vision, computer graphics, and robotics, specifically focusing on generalizable 


dexterous grasping, manipulation, and whole-body control of humanoid and quadruped robots. 

**Fangqiang Ding** is a Postdoctoral Associate with the Department of Mechanical Engineering at the Massachusetts Institute of Technology (MIT), Cambridge, MA, USA, working with Dr. Hermano Igo Krebs in The 77 Lab. He was previously a Postdoctoral Fellow at Technion – Israel Institute of Technology, working with Dr. Or Litany. He received the Ph.D. degree in Robotics and Autonomous Systems from the School of Informatics, University of Edinburgh, U.K., and the B.E. degree from Tongji University, Shanghai, China. He was selected as an RSS Pioneer in 2025 for his work on robust spatial perception with 4D radar for mobile autonomy. My research centers on reliable and affordable Physical AI, enabling AI-integrated physical systems (e.g., autonomous vehicles, robots, and IoT) to operate responsibly around humans and deliver societal benefits at scale in the physical world. 

**Yao Mu** is an Assistant Professor at the Institute of Artificial Intelligence, Shanghai Jiao Tong University. He received his Ph.D. from the University of Hong Kong in 2025 and his Master’s from Tsinghua University in 2021. His research in embodied intelligence, reinforcement learning, robot control, and autonomous driving has produced over 40 papers in top venues including RSS, NeurIPS, ICML, ICLR, and CVPR, accumulating more than 2500 citations. Dr. Yao’s work has earned notable recognition including the ECCV Embodied Intelligence Workshop Best Paper Award, IEEE ICCAS 2020 Best Student Paper Award, and IEEE IV2021 Best Student Paper Nomination. He is a recipient of the Hong Kong Ph.D. Fellowship, University of Hong Kong Presidential Scholarship, and the National Scholarship of China. His research advances AI systems capable of effectively interacting with the physical world. 

**Wei Zhang (Senior Member, IEEE)** received the Ph.D. degree in electronic engineering from the Chinese University of Hong Kong in 2010. He is currently a Professor with the School of Control Science and Engineering, Shandong University, Jinan, China. His research interests include computer vision and robotics. He has served as a program committee member and a reviewer for various international conferences and journals. 


**Zeng-Guang Hou (Fellow, IEEE)** received the B.E. and M.E. degrees in electrical engineering from Yanshan University (formerly Northeast Heavy Machinery Institute), Qinhuangdao, China, in 1991 and 1993, respectively, and the Ph.D. degree in electrical engineering from the Beijing Institute of Technology, Beijing, China, in 1997. He is currently a Professor with the State Key Laboratory of Multimodal Artificial Intelligence Systems, Institute of Automation, Chinese Academy of Sciences. His research interests include neural networks, robotics, and intelligent systems. He is serving as a VP of the Asia Pacific Neural Network Society (APNNS) and Chinese Association of Automation (CAA). He is an associate editor of IEEE Transactions on Neural Networks and Learning Systems, IEEE Transactions on Cognitive and Developmental Systems, and Neural Networks, etc. He is on the Board of Governors of International Neural Network Society (INNS). He was the Chair of Neural Network Technical Committee (NNTC) of Computational Intelligence Society (CIS), IEEE. Dr. Hou was a recipient of Neural Networks Best Paper Award in 2022, IEEE Transactions on Neural Networks Outstanding Paper Award in 2013. 

**Hong Zhang (Life Fellow, IEEE)** received his Ph.D. in Electrical Engineering from Purdue University in 1986. He was a Professor in the Department of Computing Science, University of Alberta, Canada, for over 30 years before he joined the Southern University of Science and Technology (SUSTech), China, in 2020, where he is currently a Chair Professor. Dr. Zhang served as the Editorin-Chief of IROS Conference Paper Review Board (2020-2022) and as a member of the IEEE Robotics and Automation Society Administrative Committee (2023-25). He is a Life Fellow of IEEE and a Fellow of the Canadian Academy of Engineering. His research interests include robotics, computer vision, and image processing. 

