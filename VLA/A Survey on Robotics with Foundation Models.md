---
title: "A Survey on Robotics with Foundation Models: toward Embodied AI"
date: "2024-02-04"
authors: "Zhiyuan Xu; Kun Wu; Junjie Wen; Jinming Li; Ning Liu; Zhengping Che"
url: https://arxiv.org/abs/2402.02385
pdf: https://arxiv.org/pdf/2402.02385
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2402.02385)** / [論文ページ](https://arxiv.org/abs/2402.02385)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **A Survey on Robotics with Foundation Models: toward Embodied AI** 

## **Zhiyuan Xu**<sup>_∗_</sup> , **Kun Wu**<sup>_∗_</sup> , **Junjie Wen** , **Jinming Li Ning Liu** , **Zhengping Che** , **Jian Tang**<sup>_†_</sup> 

Midea Group 

{xuzy70, wukun12, wenjj25, lijm295, liuning22, chezp, tangjian22}@midea.com<sup>_∗†_</sup> 

## **Abstract** 

While the exploration for embodied AI has spanned multiple decades, it remains a persistent challenge to endow agents with human-level intelligence, including perception, learning, reasoning, decision-making, control, and generalization capabilities, so that they can perform general-purpose tasks in open, unstructured, and dynamic environments. Recent advances in computer vision, natural language processing, and multi-modality learning have shown that the foundation models have superhuman capabilities for specific tasks. They not only provide a solid cornerstone for integrating basic modules into embodied AI systems but also shed light on how to scale up robot learning from a methodological perspective. This survey aims to provide a comprehensive and up-to-date overview of foundation models in robotics, focusing on autonomous manipulation and encompassing highlevel planning and low-level control. Moreover, we showcase their commonly used datasets, simulators, and benchmarks. Importantly, we emphasize the critical challenges intrinsic to this field and delineate potential avenues for future research, contributing to advancing the frontier of academic and industrial discourse. 

## **1 Introduction** 

Although robots are extensively used in various fields like manufacturing, logistics, and specialized operations, they have been confined to controlled environments with preprogrammed actions. The advent of machine learning and deep learning has ushered in vision-guided planning and deep reinforcement learning-based control, reducing the need for precise environment or manipulation object modeling that is impractical in dynamic real-world scenarios. Nevertheless, due to training on task-specific data with limited model capacity, these methods still struggle with generalizability and transferability, impeding the deployment of robots into everyday environments with general-purpose tasks. 

> _†_ Corresponding author 

Recently, foundation models have become pivotal in advancing embodied AI. Pre-trained on massive, internetscale datasets consisting of text, images, audio, and video, these large models, with billions of parameters, demonstrate remarkable capabilities. Examples include Large Language Models (LLMs) [OpenAI, 2023], Large Vision Models (LVMs) [Kirillov _et al._ , 2023], and large multi-modal VisionLanguage Models (VLMs) [Radford _et al._ , 2021], presenting exceptional understanding, reasoning, interaction, and generative abilities. However, these models are not yet able to interact directly with entities in the physical world, i.e., they merely provide humans and agents with auxiliary information and are not the decision-makers, so current applications are limited to the Internet. Therefore, how to integrate foundation models into decision-making models harmoniously is a key question for embodied AI. 

In this survey, we methodically review recent papers that apply foundation models to address challenges in autonomous robotic manipulation, categorizing them into two fundamental ways: 1) **High-Level Planning:** This involves processing natural language commands from users and observations from interactive environments, culminating in stepby-step decision-making. Foundation models aid in interpreting commands, perceiving environments, and reasoning through complex tasks using their underlying world knowledge; 2) **Low-Level Control:** The focus is on implementing execution commands while monitoring environmental and robotic states, ultimately determining precise execution parameters, such as the position of the robot arm end-effector or the degree of joints. The capacity of foundation models enables learning multiple tasks and making fine-grained execution decisions simultaneously. Furthermore, recent advancements merge these two aspects, training large robotic foundation models to handle both planning and control. Their synergies, like the collaboration of the cerebrum and cerebellum, significantly enhance the reasoning and execution ability to handle complex and long-horizon tasks in a few-shot or zero-shot manner. 

Despite recent demonstrations showcasing significant progress toward achieving general-purpose tasks, there remains a considerable journey ahead before robots can be widely deployed in everyday scenarios. In this survey, we also investigate the commonly used datasets, simulators, and benchmarks in this research field, enabling readers to quickly 

> _∗_ Equal contributions 


Figure 1: Taxonomy of foundation models for high-level planning and their properties. 

grasp the subject and apply their knowledge with existing resources. More importantly, we emphasize some persisting challenges and propose several potential research directions. 

## **2 Foundation Models for High-Level Planning** 

As the complexity of long-horizon tasks increases, training a single policy model to complete an entire task based on simple and concise instruction remains challenging. The model needs not only to acquire multiple skills but also to understand the sequential execution order among these skills, making the training process inherently intricate. Considering the demonstrated prowess of vision and language foundation models in intricate reasoning and contextual generalization, it is a natural progression for the robotics community to explore the application of foundation models in addressing these challenges. From the perspectives of forms (i.e., Section 2.1) and assistants (i.e., Section 2.2) of planning, we review how to apply foundation models for understanding user command and planning long-horizon tasks. The taxonomy of foundation models for high-level planning is illustrated in Fig. 1. 

### **2.1 Forms of Planning** 

Foundation models, such as LLMs and VLMs, are capable of generating a range of planning formats, spanning from highly structured forms like Planning Domain Definition Language (PDDL) to expressive programming code and even to the more flexible natural language. Stricter formats offer greater precision and are more easily interpreted by robotic controllers, yet their predefined nature restricts the expressiveness of foundation models. This limitation means the models are confined to generating only within these structures, potentially reducing their efficacy in zero-shot tasks. Conversely, a more loosely structured format, while offering increased expressiveness and better suitability for interpreting user commands in natural language, may pose execution challenges for robotics. For instance, natural language planning steps necessitate a sophisticated low-level controller for effective understanding and execution. 

PDDL is a typical family of structured languages that defines a robotic planning problem. Its standardization has the benefit of making research more reusable and easily comparable, though at the cost of some expressive power, compared to domain-specific systems. LLMs, like GPT-4 [OpenAI, 2023], first translate planning problems into PDDL descriptions, then are parsed by a standard PDDL planner. Finally, parsing results will be further translated to finite state automata [Yang _et al._ , 2023b], executable programming code [Zhou _et al._ , 2023], or natural lanugage [Liu _et al._ , 2023a]. 

#### **Policy Code Planning** 

Policy code planning decouples natural language instructions into several steps in code form. Notably, the planning form is a well-organized and order-sensitive program that involves intricate planning. Code excels at providing an accurate description of the spatial position and exclusive reference of objects. Moreover, employing code as a high-level plan offers the advantage of expressing functions or feedback loops, processing perception outputs, and parameterizing control primitive APIs. Code as Policies (CaP) [Liang _et al._ , 2023] first presents a robotic-centric formulation of language model generated programs (LMPs) executed on real systems. With sophisticated prompt engineering, CaP could establish a target program according to the natural language instruction and recursively define new functions to generalize to novel tasks. Furthermore, ProgPrompt [Singh _et al._ , 2023] encodes the world state into natural language and then embeds it in prompts for LLMs to generate policy code. Instruct2Act [Huang _et al._ , 2023b] utilizes LLMs to map multimodal instructions to sequential code for robotic manipulation tasks. OEIEA [Sarch _et al._ , 2023] generates policy code by human-robot dialogue that offers more detailed information and utilizes the VLMs to get scene descriptions. 

#### **Natural Language Planning** 

Natural language generation is the inherent ability of foundation models, which possess good interpretability. However, natural language may lack clear expression that misleads agents and aborts tasks. To mitigate this, CAPEAM [Kim 

_et al._ , 2023] utilizes a sub-goal planner to extract sub-goals and concrete objects from task instruction, thereby reducing expressive ambiguity through the composition of these subgoals and objects. Moreover, it leverages external models to evaluate sub-goals to verify their feasibility, correctness, and clarity. ViLA [Hu _et al._ , 2023] directly applies the most advanced multi-modal foundation models, GPT4-V, to generate nature language planning for long-horizon tasks through chain-of-thought reasoning and rich web-scale knowledge. Furthermore, RSFT [Zhu _et al._ , 2024a] proposes to identify fast and slow thinking for more precise planning and execution, which refers to straightforward actions like picking and multi-step reasoning tasks like rearranging, respectively. 

### **2.2 Assistants of Planning** 

The complexity of robot planning extends beyond mere language input or output. Consequently, researchers are exploring diverse methods to augment foundation models, like LLMs, with additional tools for more effective planning. This includes integrating vision models into LLMs to assist in target identification and incorporating external feedback to guide the robotic manipulation. What’s more, combining extra common sense knowledge with foundation models is beneficial for reasoning and planning as well. These enhancements aim to bridge the gap between linguistic processing and practical perceptual information in robotics. 

E [Driess _et al._ , 2023] jointly trains an embodied multi-modal vision-language model by blending the robotic data and routine vision-language data, which performs well both at embodied reasoning tasks and vision-language tasks. Though VLMs significantly improve the grounding capability, they fall short in fine-grained semantic understanding, which is essential for tiny object manipulation and dexterous operation. OCI-Robotics [Wen _et al._ , 2024] fine-tunes VLMs to predict the precise position of target objects, alleviating this deficiency to some extent. 

#### **Plan with Extra Knowledge** 

Foundation models typically lacks domain-specific knowledge, hence it may cause errors in task planning in some scenarios e.g. make a cup of coffee with coffee machine. This extra knowledge can be acquired from self-planning, i.e., “inside”, and other models, i.e., “outside”. ClIN [Majumder _et al._ , 2023] learns from its planning failures, recursively using these insights for subsequent planning until success. CAPEAM [Kim _et al._ , 2023] introduces an environment-aware memory system that records the historical locations of objects to enhance agent interactions. LMZSP [Huang _et al._ , 2022a] translates each step of the origin task plan from LLMs to precise admissible actions through another pre-trained foundation model. PLAN [Lu _et al._ , 2022] constructs commonsenseinfused prompts from external knowledge, which serves as an external prompt for enhanced task planning. 

#### **Visual-Assisted Plan** 

Language-based Foundation models, such as LLMs [Touvron _et al._ , 2023], often require the support of conventional deep learning models (e.g., 2D/3D detection models) or other large vision-language models [Liu _et al._ , 2023b; Zhu _et al._ , 2024b] to process image data for task planning. Inner Monologue [Huang _et al._ , 2022b] directly integrates detection results of vision foundation models into the prompt of LLM for planning or re-planning. PHYSOBJECTS [Gao _et al._ , 2023] utilizes LLMs to generate initial plans and grounds them with the help of VLMs by querying physical concepts (e.g., material, fragility) of everyday objects. Vision foundation models can also serve as value or affordance functions to assist LLMs in next-step planning. Specifically, SayCan [Brohan _et al._ , 2023b] introduces a vision model to predict the probability of successfully executing said skills in a plan. This model collaborates with the LLMs, which evaluates the probability of selecting each skill, to jointly determine the next step in the process. However, the skills are predefined in SayCan, which lacks task generalizability. To mitigate this, GD [Huang _et al._ , 2023c] directly predicts the probability of each token for the next step, aided by a vision model. The selection of the next token then involves a joint decoding process, which combines the probabilities estimated by both the LLMs and the vision model. 

VLMs can directly integrate LLMs and visual information for task planning, which excels at grounding language into the environments and understanding tasks. A simple and efficient way to utilize VLMs is to substitute LLMs with VLMs in the origin framework. ViLA [Hu _et al._ , 2023] utilizes the novel GPT4-V model to generate plans showcasing strong zero-shot reasoning and generalization capability. PaLM- 

#### **Plan with Feedback** 

The aforementioned methods, like PaLM-E or ViLA, employ preliminary, one-time planning, whereas interactive planning dynamically evolves throughout task execution. Precisely, the foundation models predict subsequent actions, assisted by instructions and real-time feedback, continually updating their plans following each step. Typical feedback consists of: 1) feedback from the environment, indicating the signals from task completion or the success of actions. Inner Monologue [Huang _et al._ , 2022b] incorporates closed-loop language feedback based on the success signals of actions into robot planning, significantly enhancing the completion of high-level instructions; 2) feedback from humans, involving direct human-robot interaction and serving as an intuitive signal to enhance planning capability. IRAP [Hori _et al._ , 2023] uses a question-and-answer format to obtain essential taskrelevant knowledge, like the specific location of a target, facilitating precise robot instructions generation. 

## **3 Foundation Models for Low-Level Control** 

In addition to using the decomposition and planning capabilities of large foundation models to help robots do high-level planning for complex long-horizon tasks, numerous studies also propose leveraging the recognition, reasoning, and generalization capabilities of the language and vision foundation models for generating accurate low-level control. Moreover, employing internet-scale data for training the foundation models also paves a promising way for training robotic foundation models. In this section, we focus on the works dedicated to the robotic low-level control, i.e., the ultimate 

Table 1: Taxonomy of foundation models for low-level control and their properties. 

|**Directions**|**Category**|**Reward**|**Minimum Requirements**<br>**Optimal Data**<br>**Suboptimal Data**|**Causality**|**Prope**<br>**Sample Efficiency**|**rties**<br>**End-to-End**|**Generalization**|
|---|---|---|---|---|---|---|---|
|Policy|RL|✓||✓|Low|✓|Low|
|Learning|IL||✓|✓|High|✓|Low|
|Environment<br>Modeling|Forward Dynamic<br>Inverse Dynamic||✓<br>✓|✓|Low<br>High||Improve<br>Improve|
|Representation|Frozen Models||✓||High||Improve|
|Learning|Learned Models||✓<br>✓|✓|Low|✓|Improve|


goal is to learn a policy to output actions like target joint position, target 6 DoF poses, and so on. We categorized these methods into three classes from the perspective of different focused components in the learning process: 1) Policy learning. 2) Environment modeling. 3) Representation learning. As shown in Table 1, we provide a taxonomy of foundation models for low-level control and their properties. 

### **3.1 Policy Learning** 

#### **Reinforcement Learning** 

RL problems are typically formulated using the Markov Decision Process (MDP). The goal is to maximize the total reward of the tasks by interacting with the environments and learning in a trial-and-error manner. One of the major barriers preventing RL from being used in real-world applications is reward shaping [Ng _et al._ , 1999] that RL requires carefully designed reward functions to learn. Therefore, many recent studies have turned their attention to utilizing the knowledge and understanding of various tasks contained in large foundation models to provide rewards and reduce laborious human involvement. After observing that textual task instructions typically express the outcome of robot behavior rather than the details of the low-level actions, L2R [Yu _et al._ , 2023b] proposes the use of reward functions as a bridge between language instructions and low-level actions and explores the use of the code generation capability of LLMs to convert task descriptions into reward functions. Using the generated reward, the trajectory optimization and reinforcement learning algorithms can learn a good policy. Eventually, L2R performs well on robotic arms for dexterous manipulation tasks. 

Another important challenge lies in the low sample efficiency of RL methods. Recently, many studies have argued that the foundation models can greatly accelerate the development of the above techniques by infusing the learning process with more prior knowledge learned from internet-scale data. Specifically, FRL [Ye _et al._ , 2023] presents a foundation reinforcement learning framework and instantiates an actorcritic method, FAC, which leverages the value, reward, and policy prior knowledge from foundation models to achieve sample-efficient learning, robustness to noisy priors, and minimal human intervention. Moreover, the success of using ballooned internet-scale data with transformer architecture in the vision and language domain has fueled the imagination about how embodied intelligence can evolve. For instance, Q-Transformer [Chebotar _et al._ , 2023] discusses design decisions for using transformer architecture to learn Q-function and multi-task policy given large-scale offline datasets. 

#### **Imitation Learning** 

Considering the MDP setting, where the difference from RL is that the expert demonstrations are given and the reward function is unknown, the goal of imitation learning is to recover the expert policy and thus achieve higher rewards or task success rates. Since the distribution of expert demonstrations is typically narrow, the major problem is that the compounding error exists and the generalization ability of learned policy is poor. Inspired by the fact that LLMs and VLMs can achieve strong zero-shot performance in the openset world via training with the overwhelming amount of data, an intuitive and straightforward way is to extend this mode into embodied AI and use large-scale robotic data to train a policy with high capability. Many studies have put the above idea into practice, the best known of which would be RT-1 [Brohan _et al._ , 2023a]. In RT-1, the authors spent 17 months collecting massive amounts of data on robot manipulation from 13 robots, including 130k trajectories for 700 tasks. Equipped with a high-capacity transformer-based architecture and pre-trained vision and language models, RT-1 can not only achieve high success rates on the training tasks but also perform better than baseline methods in new test tasks and scenarios, showing better generalization ability. 

### **3.2 Environment Modeling** 

Besides learning a policy directly from demonstrations or interactions with environments, it is also important to learn the environment (world) model, which can be used in conjunction with other algorithms, such as reinforcement learning and trajectory optimization, to generate better policies. 

#### **Forward Dynamic Learning** 

Forward dynamic learning predicts the next state based on the current or historical observations and actions. This learning objective incorporates the nature of causality because the next state is the result of an action made at the current state. Thus, it can effectively model the environment, containing the physical rules. The trade-off is that it is difficult and requires a large amount of data to build an accurate dynamic model. As a seminal work, SWIM [Mendonca _et al._ , 2023] learns world models with forward dynamics from internet-scale human play videos. In order to overcome the morphological differences between humans and robots, the method learns in a high-level abstract and structured action space, i.e., predicting the target poses and waypoints. Subsequently, the model can be fine-tuned using a small portion of the robotic data in an unsupervised way, which does not require a reward function as well as task-related supervision. 

#### **Inverse Dynamic Learning** 

Inverse dynamic learning aims to predict the action given the current and next states as input. It is non-causal since it leverages information from the future to recover past behaviors. Thus, this learning method reduces the difficulty of training and is not as data-hungry as forward dynamic learning. [Brandfonbrener _et al._ , 2023] builds extensive experiments on robot manipulation tasks over various domains. The empirical results show that 1) learning inverse dynamic can perform better than other per-training objectives when learning from scratch, and 2) it can extract smoother and more discriminative representations with higher sample efficiency compared to forward dynamic objective. 

### **3.3 Representation Learning** 

Representation, one of the most fundamental concepts in the era of deep learning, has a pivotal impact on the final performance of various tasks. Currently, vision and language foundation models trained with large internet-scale data can extract beneficial representations for images and text instructions, providing a solid cornerstone for downstream embodied AI tasks. Also, they are able to align with the features of the text. For example, the foundation models can recognize areas of apples in an image based on the word "apples" in the instructions. Following this spirit, many studies take LLMs and VLMs as fixed representation extractors and establish a harmonious composition and pipeline. 

#### **Frozen Foundation Models** 

One of the most straightforward approaches is to use the large model as a read-standing component for some specific functions, such as object detection [Liu _et al._ , 2023c], semantic segmentation [Kirillov _et al._ , 2023], and object tracking [Yang _et al._ , 2023a]. For instance, SMS [Sharma _et al._ , 2023] presents a plug-and-play semantic module that provides more detailed and comprehensive semantic information for downstream embodied AI tasks. Through the use of an open vocabulary object detection model, it is able to recognize objects in the current scene and, in conjunction with the LLMs, explicitly builds a semantic occupancy distribution as the feature of the scene. 

#### **Learned Control Models** 

To extract descriptive and intelligible representations from robotic data, many works propose to use the techniques in different fields like unsupervised learning [Alloghani _et al._ , 2020], self-supervised learning [Balestriero _et al._ , 2023], and transfer learning [Zhuang _et al._ , 2020]. More specifically, Motivated by the pattern of human acting and learning in the real world, DualMind [Wei _et al._ , 2023] proposes a similar two-stage learning strategy for learning a generalist policy that can handle multiple decision-making tasks. In the first phase, the policy is trained in a self-supervised manner to learn the underlying common knowledge in the world. Subsequently, in the second phase, a small part of the parameters is used to train a conditional policy based on multimodal prompts. The method uses an Encoder-Decoder Transformer architecture combined with Token-Leaner and a crossattention mechanism for enhancing feature extraction ability. 

## **4 Datasets, Simulators, and Benchmarks** 

### **4.1 Datasets** 

The development of foundation models in the domains of CV and NLP over recent years owes much of its success to the utilization of large-scale datasets. Analogously, for the substantial improvement of embodied AI capabilities, the imperative lies in scaling up the robotic datasets, which serves as a requisite pathway to facilitate significant advancement in embodied AI. Compared to the vision and language dataset that emphasizes abstract, 2D, and web-based information, the datasets for embodied AI focus more on 3D information in real-world environments, the affordance of objects, and the interactions between the robots and objects, which are based on the constraints of real-world physical laws. We divide the datasets for embodied AI into three categories, including object, human, and robotic datasets. 

#### **Object Datasets** 

Object datasets usually contain a large number of synthesized or real scanned items and their corresponding labels, including categories, meshes, point clouds, etc. These datasets can be used for various downstream tasks, including robotic environment building, perception, novel view synthesis, object reconstruction, object generation, and robotic manipulation tasks. For example, OmniObject3D [Wu _et al._ , 2023] scans from the real world to collect a total of 6,000 everyday objects of 190 types and aligns the category with commonly used 2D datasets like ImageNet. It also provides rich object annotations, including multi-view images and even videos. Moreover, all objects are scanned using professional scanners and thus have accurate shapes and high-fidelity appearance, providing high-quality environments and scenes. 

#### **Human Datasets** 

Human datasets are usually in the form of videos and contain people performing activities from the first- or third-person view in different environments and scenarios, from doing chores in the kitchen to biking outdoors. These data are very broad and relatively easy to collect, e.g., downloading human activity videos from YouTube. They contain real-world information about the appearance of the objects and environments, the human-object interactions, and physical rules embedded in the movement and dynamics, which are beneficial to the embodied AI if this knowledge can be successfully transferred to the agents. In the latest work Ego-Exo4D [Grauman _et al._ , 2023], the authors build a massive multi-view human video dataset containing a total of 1,422 hours of video divided into 5,625 instances, each between 1 and 42 minutes, with more than 800 participants from 13 different cities around the world. 

#### **Robotic Datasets** 

Robotic datasets contain demonstrations of directly controlling robots to perform tasks in the real world or a simulator, with various collection methods like teleoperation devices, pre-trained agents, and so on. However, these collection processes are time-consuming and labor-intensive, e.g., setting up the environment in which the robots perform the tasks and teaching operators to use the relevant equipment. This leads 

to the fact that it is very difficult to scale the robotic datasets to very large sizes, which is one of the challenges embodied AI faces. RT-X [Padalkar _et al._ , 2023] is leading the way and taking an important step forward in this regard. It assemble a dataset from 22 different robots collected through a collaboration between 21 institutions, demonstrating 527 skills (160,266 tasks). Based on such large-scale data, the trained agent shows positive performance in zero-shot generalization and cross-morphology transfer learning. 

### **4.2 Simulators** 

In the field of embodied AI, high-fidelity simulators are crucial for efficient training and reducing the gap between simulation and real-world application. Key challenges in simulator development include 1) Real-time soft-body material simulation, where advanced simulators like ManiSkill2 use the material point method (MPM) for more realistic and complex interactions compared to traditional methods like finite element method (FEM); 2) Support for multiple controllers to accommodate various tasks and control methods, with simulators like ManiSkill2 [Gu _et al._ , 2023] and Nvidia Isaac Sim offering versatility in action spaces for tasks ranging from obstacle avoidance to pick-and-place; 3) The ability to handle the parallel computation of multiple environments, essential for large-scale data collection and training in reinforcement learning, where simulators like ManiSkill2 and Isaac Gym demonstrate superior computational efficiency and functionality in managing numerous simultaneous environments. 

quickly with steps. Therefore, it is important to learn highlevel planning and low-level control simultaneously and make them collaborate seamlessly. Recently, RT-2 [Zitkovich _et al._ , 2023] and RT-X [Padalkar _et al._ , 2023] present significant advancements for this objective. As a milestone in robotics work, RT-X absorbs its predecessors, RT-1 and RT-2, including the use of VLMs, LLMs, and transformer-based policy networks for learning. More importantly, authors from 21 institutions have collected massive amounts of data on robot manipulation, including 527 skills and 160,266 tasks from 22 robots with different morphologies. Using these data, RT-X demonstrates a strong ability to transfer among different morphologies and generalize to new tasks and scenarios. 

Compared to integrating planning and control in a single large policy network, many previous works study how to decompose complex tasks rationally and learn skills effectively. Nevertheless, they use only pre-defined primitive tasks (skills) and can not generalize to new tasks, which is a prerequisite for robots to be successfully deployed in real-world applications. At present, the development of vision and language foundation models also provides a strong boost to this direction, for example, using LLMs for more rational planning and expanding the skill library. More specifically, given the high-dimensional visual observation history as the input, Skill Transformer [Huang _et al._ , 2023d] predicts both highlevel skills and low-level actions concurrently. It consists of a skill prediction module and a transformer-based policy that can model the long-horizon sequences and dependencies without making every subtask completely isolated. 

### **4.3 Benchmarks** 

In embodied AI, benchmarks are crucial for assessing diverse systems and algorithms to ensure fair comparisons. However, the vast scope of embodied AI, encompassing a wide range of tasks, systems, and environments, poses a challenge in creating a universal benchmark. Two notable benchmarks are FMB [Luo _et al._ , 2024], which offers a benchmark for testing and improving robotic manipulation skills with tasks like grabbing, moving, and assembling objects using 3D-printed items for easy replication and study, and ManiSkill2 [Gu _et al._ , 2023], presenting a collection of 20 targeted operational tasks designed to address common challenges in operational skill benchmarks. Both provide comprehensive platforms for developing and evaluating embodied AI agents, catering to the field’s complex and varied requirements. 

## **5 Discussions and Future Directions** 

The exploration of robotics integrated with foundation models is currently in its nascent phase. Despite significant advancements, numerous challenges impede the practical application of robots in real-world environments. In this section, we highlight some existing challenges and potential future avenues of research in this area. 

### **5.2 Hallucination of Foundation Model** 

Foundation models have achieved remarkable success due to their ability to learn from massive datasets and generalize to domains beyond their training scope. However, significant concerns have been raised regarding the safety and reliability of these models, particularly in relation to their tendency to ’hallucinate’ or generate misleading information [Ouyang _et al._ , 2022]. A case in point is GPT-4V, which can sometimes interpret images by including objects that do not actually exist. This issue becomes critically important in fields like robotics, where inaccurate interpretations or instructions provided by foundation models can lead to serious malfunctions or failures. Additionally, the aspect of model safety is vital in the development of embodied agents [Liu _et al._ , 2023d; Perez _et al._ , 2022], where the model is integrated with a physical entity. Misuse of these models can lead to catastrophic outcomes, reminiscent of scenarios depicted in science fiction novels. In these applications, the physical capabilities of the agents, combined with potentially flawed decision-making processes, underscore the need for rigorous safety protocols and reliable operational frameworks to prevent adverse outcomes [Brunke _et al._ , 2022]. 

### **5.3 Efficient Data Collection** 

### **5.1 Synergies of Planning and Control** 

Current embodied AI has achieved unprecedented success on simple tasks such as grasping and placing objects. However, for long-horizon tasks, such as object rearrangement, learning a single policy is very difficult because errors accumulate 

A key observation gained from the fact that large vision and language foundation models show super generalization ability as well as emergent abilities [Wei _et al._ , 2022] is that scaling the size of datasets is perhaps one of the most important things to do. The current scale of the robotic dataset is 

nowhere near the magnitude used for the vision and language foundation models. For example, the vision and language dataset LAION-5B [Schuhmann _et al._ , 2022] contains 5.75 billion text-image pairs, while the dataset in VIMA [Jiang _et al._ , 2023] only collects 650k successful demonstrations. The collection of robotics data poses an even more formidable challenge compared to acquiring purely visual and language data. A fraught example is that RT-1 [Brohan _et al._ , 2023a] spends 17 months to collect 130k episodes. With this collecting speed, it is essentially impossible to collect robotic data of a magnitude comparable to the vision and language internetscale dataset. How to collect robotic data more efficiently remains a key and open question. 

One promising solution is to utilize a high-fidelity simulator for large-scale trajectory collection or training and then deploy the agent to real-world applications via Sim2Real methods [Huang _et al._ , 2023a]. However, there is still a distribution shift between simulators and the real world, both in terms of external appearance and internal dynamic, which can significantly degrade the performance, and the Sim2Real approach cannot fully compensate for this part of the gap. 

Another solution is to utilize the extra human activity datasets [Grauman _et al._ , 2022], as we discuss in Section 4.1. These data are relatively easy to collect by downloading them from the internet, and they contain real-world observations and dynamic information. Experimental results from the work [Huo _et al._ , 2023] demonstrate that incorporating extra data can enhance performance. However, it is difficult to align this information with the inputs and outputs of robots since robots and humans have very different morphologies. 

### **5.4 Augmenting Existing Datasets** 

Compared to vision and language tasks, collecting large-scale training data for embodied AI tasks is much more difficult and costly. People need time-consuming training to become proficient in the use of teleoperation equipment and are susceptible to a variety of interfering factors that can lead to mistakes, such as fatigue and distracting events. Therefore, how to effectively augment the existing robotic datasets is an unavoidable question. 

The straightforward approach is to enhance the image data from the perspective of computer vision, which uses commonly used data augmentation techniques [Xu _et al._ , 2023], such as modifying brightness, flipping, cropping, noise injection, etc. However, these methods may destroy the semantic information in the images, which degrades the final performance. Recently, data augmentation methods without destroying the semantic information have been proposed to enhance the generalization performance of the policy further by utilizing VLMs and LLMs. One of these encouraging works, ROSIE [Yu _et al._ , 2023a], reformulates the data augmentation problem as an image inpainting problem. It uses the VLMs to delineate the task-relevant region of the images and uses the Imagen Editor, a state-of-the-art diffusion model, to augment the region based on textual instructions. Finally, the robot manipulation policy trained on the augmented data shows enhanced generalization capabilities on hundreds of tasks. However, these methods essentially do not increase the number of robotic trajectories, meaning that when the agent 

enters a dangerous or out-of-distribution (OOD) state, it still does not know how to recover from the error. 

### **5.5 Efficiency on Computation and Deployment** 

The effective integration of foundation models significantly enhances robot learning, such as PaLM-E-562B [Driess _et al._ , 2023] and RT-1 [Brohan _et al._ , 2023a]. However, both the training and inference phases demand substantial computational resources. Training the huge models on largescale datasets necessitates a bunch of high-end GPUs. Therefore, efficient pre-training and fine-tuning techniques like LoRA [Hu _et al._ , 2021] and MiniGPT-4 [Zhu _et al._ , 2023] are essential to mitigate training costs. Moreover, deploying these large models on resource-constrained edge devices presents challenges because of concerns over user data privacy and the need for real-time performance in robotic applications, which makes cloud deployment impractical. Consequently, optimizing the computation efficiency of large models through model compression techniques and designing lightweight models is vital for enabling deployment on edge devices [Dey _et al._ , 2023]. 

### **5.6 Safety and Interpretation of Robot** 

In the deployment of robotic systems within real-world scenarios, particularly in areas with a high concentration of people and objects, such as human-robot collaborations or indoor environments, ensuring running safety is imperative. This involves mitigating the risk of collisions and preventing injuries to people and property damage to objects. While certain approaches [Zhao _et al._ , 2021] offer theoretical guarantees for robot systems through the utilization of Lyapunov functions, they only consider ideal and simple experimental environments with only low-dimensional inputs and necessitate precise modeling of the environment. However, these real-world applications with high-dimensional inputs like images are more intricate, e.g., many assumptions will not hold anymore, so how to ensure security in real-world environments poses a formidable challenge. In contrast, alternative methods [Farid _et al._ , 2022] focus on using out-of-distribution (OOD) detection to facilitate real-time identification of errors made by the robot. However, these methods grapple with the challenge of generalization in novel scenarios and the formulation of recovery strategies following errors, constituting a crucial area for ongoing research. 

## **6 Conclusion** 

In this paper, we offer an in-depth overview of the latest applications of foundation models in embodied AI, with a special emphasis on autonomous robotic manipulation. We methodically categorize existing literature based on high-level planning strategies and low-level control mechanisms. Furthermore, this review includes an extensive survey of the robots, simulators, and benchmarks that are most commonly utilized in experimental research in this area. It concludes with a discussion of the key challenges and outlines promising research directions. Through this survey, we hope to advocate for a concerted effort from both academic and industrial spheres to advance foundation models in robotics toward a new era of generalized, embodied AI. 

## **References** 

- [Alloghani _et al._ , 2020] Mohamed Alloghani, Dhiya AlJumeily, Jamila Mustafina, et al. A systematic review on supervised and unsupervised machine learning algorithms for data science. _Supervised and unsupervised learning for data science_ , 2020. 

- [Balestriero _et al._ , 2023] Randall Balestriero, Mark Ibrahim, Vlad Sobal, et al. A cookbook of self-supervised learning. _arXiv preprint arXiv:2304.12210_ , 2023. 

- [Brandfonbrener _et al._ , 2023] David Brandfonbrener, Ofir Nachum, and Joan Bruna. Inverse dynamics pretraining learns good representations for multitask imitation. _NeurIPS_ , 2023. 

- [Brohan _et al._ , 2023a] Anthony Brohan, Noah Brown, Justice Carbajal, et al. Rt-1: Robotics transformer for realworld control at scale. _RSS_ , 2023. 

- [Brohan _et al._ , 2023b] Anthony Brohan, Yevgen Chebotar, Chelsea Finn, et al. Do as i can, not as i say: Grounding language in robotic affordances. _CoRL_ , 2023. 

- [Brunke _et al._ , 2022] Lukas Brunke, Melissa Greeff, Adam W Hall, et al. Safe learning in robotics: From learning-based control to safe reinforcement learning. _Annu. rev. control robot. auton. syst._ , 5:411–444, 2022. 

- [Chebotar _et al._ , 2023] Yevgen Chebotar, Quan Vuong, et al. Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions. _CoRL_ , 2023. 

- [Dey _et al._ , 2023] Nolan Dey, Gurpreet Gosal, Hemant Khachane, et al. Cerebras-gpt: Open compute-optimal language models trained on the cerebras wafer-scale cluster. _arXiv preprint arXiv:2304.03208_ , 2023. 

- [Driess _et al._ , 2023] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, et al. Palm-e: an embodied multimodal language model. _ICML_ , 2023. 

- [Farid _et al._ , 2022] Alec Farid, Sushant Veer, and Anirudha Majumdar. Task-driven out-of-distribution detection with statistical guarantees for robot learning. _CoRL_ , 2022. 

- [Gao _et al._ , 2023] Jensen Gao, Bidipta Sarkar, Fei Xia, et al. Physically grounded vision-language models for robotic manipulation. _arXiv preprint arXiv:2309.02561_ , 2023. 

- [Grauman _et al._ , 2022] Kristen Grauman, Andrew Westbury, Eugene Byrne, et al. Ego4d: Around the world in 3,000 hours of egocentric video. _CVPR_ , 2022. 

- [Grauman _et al._ , 2023] Kristen Grauman, Andrew Westbury, Lorenzo Torresani, et al. Ego-exo4d: Understanding skilled human activity from first-and third-person perspectives. _arXiv preprint arXiv:2311.18259_ , 2023. 

- [Gu _et al._ , 2023] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. _ICLR_ , 2023. 

- [Hori _et al._ , 2023] Kazuki Hori, Kanata Suzuki, and Tetsuya Ogata. Interactively robot action planning with uncertainty analysis and active questioning by large language model. _arXiv preprint arXiv:2308.15684_ , 2023. 

- [Hu _et al._ , 2021] Edward J Hu, Yelong Shen, Phillip Wallis, et al. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 

- [Hu _et al._ , 2023] Yingdong Hu, Fanqi Lin, Tong Zhang, et al. Look before you leap: Unveiling the power of gpt4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ , 2023. 

- [Huang _et al._ , 2022a] Wenlong Huang, Pieter Abbeel, et al. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. _ICML_ , 2022. 

- [Huang _et al._ , 2022b] Wenlong Huang, Fei Xia, Ted Xiao, et al. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv:2207.05608_ , 2022. 

- [Huang _et al._ , 2023a] Peide Huang, Xilun Zhang, Ziang Cao, et al. What went wrong? closing the sim-to-real gap via differentiable causal discovery. _CoRL_ , 2023. 

- [Huang _et al._ , 2023b] Siyuan Huang, Zhengkai Jiang, Hao Dong, Yu Qiao, Peng Gao, and Hongsheng Li. Instruct2act: Mapping multi-modality instructions to robotic actions with large language model. _arXiv preprint arXiv:2305.11176_ , 2023. 

- [Huang _et al._ , 2023c] Wenlong Huang, Fei Xia, Dhruv Shah, et al. Grounded decoding: Guiding text generation with grounded models for robot control. _arXiv preprint arXiv:2303.00855_ , 2023. 

- [Huang _et al._ , 2023d] Xiaoyu Huang, Dhruv Batra, Akshara Rai, et al. Skill transformer: A monolithic policy for mobile manipulation. _ICCV_ , 2023. 

- [Huo _et al._ , 2023] Mingxiao Huo, Mingyu Ding, et al. Human-oriented representation learning for robotic manipulation. _arXiv preprint arXiv:2310.03023_ , 2023. 

- [Jiang _et al._ , 2023] Yunfan Jiang, Agrim Gupta, Zichen Zhang, et al. Vima: General robot manipulation with multimodal prompts. _ICML_ , 2023. 

- [Kim _et al._ , 2023] Byeonghwi Kim, Jinyeon Kim, Yuyeong Kim, et al. Context-aware planning and environmentaware memory for instruction following embodied agents. _ICCV_ , 2023. 

- [Kirillov _et al._ , 2023] Alexander Kirillov, Eric Mintun, Nikhila Ravi, et al. Segment anything. _ICCV_ , 2023. 

- [Liang _et al._ , 2023] Jacky Liang, Wenlong Huang, Fei Xia, et al. Code as policies: Language model programs for embodied control. _ICRA_ , 2023. 

- [Liu _et al._ , 2023a] Bo Liu, Yuqian Jiang, Xiaohan Zhang, et al. Llm+ p: Empowering large language models with optimal planning proficiency. _arXiv preprint arXiv:2304.11477_ , 2023. 

- [Liu _et al._ , 2023b] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _arXiv preprint arXiv:2304.08485_ , 2023. 

- [Liu _et al._ , 2023c] Shilong Liu, Zhaoyang Zeng, Tianhe Ren, et al. Grounding dino: Marrying dino with grounded 

pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ , 2023. 

- [Liu _et al._ , 2023d] Xin Liu, Yichen Zhu, Yunshi Lan, et al. Query-relevant images jailbreak large multi-modal models. _arXiv preprint arXiv:2311.17600_ , 2023. 

- [Lu _et al._ , 2022] Yujie Lu, Weixi Feng, Wanrong Zhu, et al. Neuro-symbolic procedural planning with commonsense prompting. _arXiv preprint arXiv:2206.02928_ , 2022. 

- [Luo _et al._ , 2024] Jianlan Luo, Charles Xu, Fangchen Liu, Liam Tan, Zipeng Lin, Jeffrey Wu, Pieter Abbeel, and Sergey Levine. Fmb: a functional manipulation benchmark for generalizable robotic learning. _arXiv preprint arXiv:2401.08553_ , 2024. 

- [Majumder _et al._ , 2023] Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra, et al. Clin: A continually learning language agent for rapid task adaptation and generalization. _arXiv preprint arXiv:2310.10134_ , 2023. 

- [Mendonca _et al._ , 2023] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. _RSS_ , 2023. 

- [Ng _et al._ , 1999] Andrew Y Ng, Daishi Harada, and Stuart Russell. Policy invariance under reward transformations: Theory and application to reward shaping. _ICML_ , 1999. 

- [OpenAI, 2023] OpenAI. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [Ouyang _et al._ , 2022] Long Ouyang, Jeffrey Wu, et al. Training language models to follow instructions with human feedback. _NeurIPS_ , 35:27730–27744, 2022. 

- [Padalkar _et al._ , 2023] Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, et al. Open X-Embodiment: Robotic learning datasets and RT-X models. _CoRL Workshop_ , 2023. 

- [Perez _et al._ , 2022] Ethan Perez, Saffron Huang, Francis Song, et al. Red teaming language models with language models. _arXiv preprint arXiv:2202.03286_ , 2022. 

- [Radford _et al._ , 2021] Alec Radford, Jong Wook Kim, Chris Hallacy, et al. Learning transferable visual models from natural language supervision. _ICML_ , 2021. 

- [Sarch _et al._ , 2023] Gabriel Sarch, Yue Wu, Michael J Tarr, and Katerina Fragkiadaki. Open-ended instructable embodied agents with memory-augmented large language models. _arXiv preprint arXiv:2310.15127_ , 2023. 

- [Schuhmann _et al._ , 2022] Christoph Schuhmann, Romain Beaumont, Richard Vencu, et al. Laion-5b: An open largescale dataset for training next generation image-text models. _NeurIPS_ , 2022. 

- [Sharma _et al._ , 2023] Satvik Sharma, Huang Huang, Kaushik Shivakumar, et al. Semantic mechanical search with large vision and language models. _CoRL_ , 2023. 

- [Singh _et al._ , 2023] Ishika Singh, Valts Blukis, Arsalan Mousavian, et al. Progprompt: Generating situated robot task plans using large language models. _ICRA_ , 2023. 

- [Touvron _et al._ , 2023] Hugo Touvron, Thibaut Lavril, Gautier Izacard, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

- [Wei _et al._ , 2022] Jason Wei, Yi Tay, Rishi Bommasani, et al. Emergent abilities of large language models. _TMLR_ , 2022. 

- [Wei _et al._ , 2023] Yao Wei, Yanchao Sun, Ruijie Zheng, et al. Is imitation all you need? generalized decisionmaking with dual-phase training. _ICCV_ , 2023. 

- [Wen _et al._ , 2024] Junjie Wen, Yichen Zhu, Minjie Zhu, et al. Object-centric instruction augmentation for robotic manipulation. _ICRA_ , 2024. 

- [Wu _et al._ , 2023] Tong Wu, Jiarui Zhang, et al. Omniobject3d: Large-vocabulary 3d object dataset for realistic perception, reconstruction and generation. _CVPR_ , 2023. 

- [Xu _et al._ , 2023] Mingle Xu, Sook Yoon, Alvaro Fuentes, et al. A comprehensive survey of image augmentation techniques for deep learning. _Pattern Recognition_ , 2023. 

- [Yang _et al._ , 2023a] Jinyu Yang, Mingqi Gao, Zhe Li, et al. Track anything: Segment anything meets videos. _arXiv preprint arXiv:2304.11968_ , 2023. 

- [Yang _et al._ , 2023b] Yunhao Yang, Cyrus Neary, and Ufuk Topcu. Multimodal pretrained models for sequential decision-making: Synthesis, verification, grounding, and perception. _arXiv preprint arXiv:2308.05295_ , 2023. 

- [Ye _et al._ , 2023] Weirui Ye, Yunsheng Zhang, Mengchen Wang, et al. Foundation reinforcement learning: towards embodied generalist agents with foundation prior assistance. _arXiv preprint arXiv:2310.02635_ , 2023. 

- [Yu _et al._ , 2023a] Tianhe Yu, Ted Xiao, Austin Stone, et al. Scaling robot learning with semantically imagined experience. _arXiv preprint arXiv:2302.11550_ , 2023. 

- [Yu _et al._ , 2023b] Wenhao Yu, Nimrod Gileadi, et al. Language to rewards for robotic skill synthesis. _CoRL_ , 2023. 

- [Zhao _et al._ , 2021] Weiye Zhao, Tairan He, and Changliu Liu. Model-free safe control for zero-violation reinforcement learning. _CoRL_ , 2021. 

- [Zhou _et al._ , 2023] Zhehua Zhou, Jiayang Song, Kunpeng Yao, Zhan Shu, and Lei Ma. Isr-llm: Iterative selfrefined large language model for long-horizon sequential task planning. _arXiv preprint arXiv:2308.13724_ , 2023. 

- [Zhu _et al._ , 2023] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 

- [Zhu _et al._ , 2024a] Minjie Zhu, Yichen Zhu, et al. Languageconditioned robotic manipulation with fast and slow thinking. _ICRA_ , 2024. 

- [Zhu _et al._ , 2024b] Yichen Zhu, Minjie Zhu, Ning Liu, et al. Llava- _ϕ_ : Efficient multi-modal assistant with small language model. _arXiv preprint arXiv:2401.02330_ , 2024. 

- [Zhuang _et al._ , 2020] Fuzhen Zhuang, Zhiyuan Qi, Keyu Duan, et al. A comprehensive survey on transfer learning. _Proceedings of the IEEE_ , 2020. 

- [Zitkovich _et al._ , 2023] Brianna Zitkovich, Tianhe Yu, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _CoRL_ , 2023. 

