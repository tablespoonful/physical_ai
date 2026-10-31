---
title: "What Foundation Models can Bring for Robot Learning in Manipulation : A Survey"
date: "2024-04-28"
authors: "Dingzhe Li; Yixiang Jin; Yuhao Sun; Yong A; Hongze Yu; Jun Shi"
url: https://arxiv.org/abs/2404.18201
pdf: https://arxiv.org/pdf/2404.18201
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2404.18201)** / [論文ページ](https://arxiv.org/abs/2404.18201)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**What Foundation Models can Bring for Robot Learning in Manipulation : A Survey** 

<u>SAGE</u> 

Journal Title XX(X):1–47 ©The Author(s) 2016 Reprints and permission: sagepub.co.uk/journalsPermissions.nav DOI: 10.1177/ToBeAssigned www.sagepub.com/ 

## **Dingzhe Li**<sup>**1**</sup> **, Yixiang Jin**<sup>**1**</sup> **, YuHao Sun**<sup>**2**</sup> **, Yong A**<sup>**1**</sup> **, Hongze Yu**<sup>**1**</sup> **, Jun Shi**<sup>**1**</sup> **, Xiaoshuai Hao**<sup>**1**</sup> **, Peng Hao**<sup>**1**</sup> **, Huaping Liu**<sup>**3**</sup> **, Xiang Li**<sup>**3**</sup> **, Xinde Li**<sup>**4**</sup> **, Fuchun Sun**<sup>**3**</sup> **, Jianwei Zhang**<sup>**5**</sup> **, Bin Fang**<sup>**2**</sup> 

#### **Abstract** 

The realization of universal robots is an ultimate goal of researchers. However, a key hurdle in achieving this goal lies in the robots’ ability to manipulate objects in their unstructured environments according to different tasks. The learning-based approach is considered an effective way to address generalization. The impressive performance of foundation models in the fields of computer vision and natural language suggests the potential of embedding foundation models into manipulation tasks as a viable path toward achieving general manipulation capability. However, we believe achieving general manipulation capability requires an overarching framework akin to auto driving. This framework should encompass multiple functional modules, with different foundation models assuming distinct roles in facilitating general manipulation capability. This survey focuses on the contributions of foundation models to robot learning for manipulation. We propose a comprehensive framework and detail how foundation models can address challenges in each module of the framework. What’s more, we examine current approaches, outline challenges, suggest future research directions, and identify potential risks associated with integrating foundation models into this domain. 

#### **Keywords** 

Robot learning, general manipulation, foundation model, survey, universal robot 

## **1 Introduction** 

Researchers aim to create universal robots that can seamlessly integrate into human life to boost productivity, much like those depicted in the movie ‘I, Robot’. However, a key hurdle in achieving this lies in the robots’ ability to manipulate objects in their unstructured environments according to different tasks. There is abundant literature available for improving the general manipulation capability of robots, which can be roughly categorized into modelbased and learning-based approaches (Zarrin et al. (2023)). The real world is too diverse for universal robots and they must adapt to unstructured environments and arbitrary objects to manipulate effectively. Therefore, learning-based methods are crucial for manipulation tasks (Kleeberger et al. (2020)). 

The predominant methodologies in learning-based approaches are deep learning, reinforcement learning and imitation learning. Learning-based methods have spanned from acquiring specific manipulation skills through labeled datasets like human demonstration, to acquiring abstract representations of manipulation tasks conducive to highlevel planning, to exploring an object’s functionalities through interaction and encompassing various objectives in between (Kroemer et al. (2021)). However, challenges persist, including 1) unnatural interaction with humans; 2) high-cost data collection; 3) limited perceptual capability; 4) non-intelligent hierarchy of skills; 5) inaccurate pre- and post-conditions & post-hoc correction; 6) unreliable skill learning; 7) poor environment transition (Hu et al. (2023b)). 

Foundation models are primarily pretrained on vast internet-scale datasets, enabling them to be fine-tuned for diverse tasks. Their significant advancements in vision and language processing contribute to mitigating the aforementioned challenges. Based on Firoozi et al. (2023) and considering the different input modalities and functionalities of the models, we categorize foundation models into the following six types. 

1. **Large Language Models (LLMs)** like BERT (Devlin et al. (2018)), GPT-3 (Brown et al. (2020)) demonstrate the capability to generate coherent chains of thought. 

2. **Visual Foundation Models (VFMs)** like SAM (Kirillov et al. (2023)) demonstrate strong segmentation capability for open-set objects. 

3. **Visual Generative Models (VGMs)** like DALL-E (Ramesh et al. (2021)), Zero-1-to-3 (Liu et al. (2023e)) and Sora (Brooks et al. (2024)), demonstrate the 

> 1Samsung R&D Institute China-Beijing, China 

> 2Beijing University of Posts and Telecommunications, China 

> 3Tsinghua University, China 

> 4Southeast University, China 

> 5Universit¨at Hamburg, Germany 

##### **Corresponding author:** 

Bin Fang, Beijing University of Posts and Telecommunications, China. Email: _{_ fangbin1120 _}_ @bupt.edu.cn 

_Prepared using sagej.cls [Version: 2017/01/17 v1.20]_ 

_Journal Title XX(X)_ 

2 

capability to generate 2D images, videos or 3D meshes through text or images. 

4. **Visual-Language Models (VLMs)** like GPT-4V (Achiam et al. (2023)), CLIP (Radford et al. (2021)) showcase robust comprehension of both vision and language, such as open-set image classification and visual question answering. 

5. **Large Multimodal Models (LMMs)** expand their scope beyond vision and language to create novel categories of foundation models incorporating additional modalities, such as ULIP (Xue et al. (2023a)) aligns point cloud representation to the pre-aligned imagetext feature space. VLMs are a type of LMMs (Firoozi et al. (2023)). However, due to the current literature focusing more on VLMs, this paper will treat VLMs as a separate category. To avoid confusion, LMMs in this paper refer to those that include images, language, and more modalities. 

6. **Robotic-specific Foundation Models (RFMs)** , like RT-X (Padalkar et al. (2023a)). Internet-scale dataset, such as images and text data, are suitable for pretraining visual and language models, but lack task level manipulation data. Therefore, researchers aim to train end-to-end RFMs by collecting task-level manipulation datasets to enable observations-to-action mapping. 

In this survey, we investigate how foundation models are utilized in robot learning for manipulation, like Fig. 1: 

1. **LLMs** enable the direct generation of policy codes or action sequences and facilitate natural interaction with the environment. 

2. **VFMs** enhance open-world perception. 

3. **VLMs** serve as the cornerstone for alignment between vision and language, facilitating understanding of multimodality. 

4. **LMMs** expand their modalities to include 3D point cloud and haptic data, among others. 

5. **VGMs** generate 2D images or 3D meshes based on prompting, aiding in scene generation within simulation environments. 

6. **RFMs** serve as an end-to-end policy model, directly outputting actions based on input observations. 

These findings underscore the potential of embedding foundation models into manipulation tasks as a viable path toward achieving general manipulation capability. However, we do not believe that a single foundation model alone can achieve general manipulation capability. Although RFMs currently represent a single-model end-to-end training approach, ensuring safety and stability, particularly in achieving an over 99% success rate in manipulation tasks, remains a challenge. Achieving over a 99% success rate in manipulation tasks is crucial, as human manipulation success rates are around 99%. Without this level of accuracy, robots can’t replace humans (Kumar (2023)). 


**Figure 1.** LLMs help address challenges in Interaction, Manipulation Data Generation, Hierarchy of Skills, Skill Policy Learning, and Environment Transition Model. VLMs assist in tackling challenges in Interaction, Manipulation Data Generation, Hierarchy of Skills, Pre- and Post-conditions Detection, Skill Policy Learning, and Perception. LMMs aid in addressing challenges in Interaction and Perception. VGMs tackle the challenge of Manipulation Data Generation and Environment Transition. VFMs help address challenges in Manipulation Data Generation, Hierarchy of Skills, Pre- and Post-conditions Detection, Skill Policy Learning, and Perception. RFMs assist in addressing the challenge of Skill Policy Learning. 

Therefore, drawing inspiration from the development of autonomous driving systems (Hu et al. (2023c)), achieving general manipulation capability necessitates an overarching framework that encompasses multiple functional modules, with different foundation models assuming distinct roles in facilitating general manipulation capability. 

The ultimate general manipulation framework should be able to interact with human or other agent and control whole-body to manipulate arbitrary objects in openworld scenarios and achieve diverse manipulation tasks (McCarthy et al. (2024)). Drawing from Kroemer et al. (2021) and this general manipulation definition, we propose a comprehensive framework for general manipulation. However, the interaction between robot and human involves not only recognizing intentions but also learning new skills or improving old skills from human experts in the external world. Open-world scenarios may be static or dynamic. Objects can be either rigid or deformable. Task objectives can vary from short-term to long-term. Furthermore, tasks may necessitate different degrees of precision with respect to contact points and applied forces/torques. Although there are many challenges, achieving general manipulation can be accomplished through multiple stages. We designate the restriction of the robot’s learning capability to improving old skills and to manipulating rigid objects in static scenes in order to achieve short-horizon task objectives with low precision requirements for contact points and forces/torques as Level 0 (L0). At the same time, we believe that improving 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

3 

the algorithm performance of different modules in the framework can support the transition from the L0 stage to the final general manipulation. Hence, we aim to use this survey not only to enlighten scholars on the issues that foundation models can address in robot learning for manipulation but also to stimulate their exploration of the general manipulation framework and the role various foundation models can play in the general manipulation framework. 

Di Palo et al. (2023) and Firoozi et al. (2023) provide detailed descriptions of the application of foundation models in navigation and manipulation, but these lack thoughtful consideration of the relationship between foundation models across different applications. The survey most closely related to this paper is Xiao et al. (2023). Compared to this survey, our survey focuses on the contributions of foundation models to robot learning for manipulation, proposing a comprehensive framework and detailing how foundation models can address challenges in each module of the framework. 

This paper is structured as follows: In Sec. 2, we present a comprehensive framework of robot learning for general manipulation, based on the developmental history of robot learning for manipulation and general manipulation definition. We elaborate on the impact of foundation models on each module in the framework in the following sections. Sec. 3 is Human/Agent Interaction module, Sec. 4 is Preand Post-conditions Detection module, Sec. 5 is Hierarchy of Skills module, Sec. 6 is State Perception module, Sec. 7 is Policy module, Sec. 8 is Manipulation Data Generation module. In Sec. 9, we discuss several issues of particular concern to us. In Sec. 10, we summarize the contributions of this survey and identify the limitations of the current framework as well as the challenges in each module. 

## **2 Framework of Robot Learning for General Manipulation** 

Over the past decade, there has been a significant expansion in research concerning robot manipulation, with a focus on leveraging the growing accessibility of costeffective robot arms and grippers to enable robots to interact directly with the environment in pursuit of their objectives. As the real world encompasses extensive variation, a robot cannot expect to possess an accurate model of its unstructured environment, the objects within it, or the skills necessary for manipulation in advance (Kroemer et al. (2021)). 

Early stage, robot manipulation is defined as learning a policy Π through deep learning, reinforcement learning, or imitation learning, etc. This policy controls the robot’s joint movements and executes tasks based on observations of the environment and the robot’s state _S_ , mapping to actions _α_ . such as Rlafford (Geng et al. (2023b)) and Graspnet (Fang et al. (2020b)) take point cloud as input and output the target pose. This process is represented by the Skill Execution module, as shown in Fig. 2. 

In the mid-term, many tasks in robotics require a series of correct actions, which are often long-horizon tasks. For example, making a cup of tea with a robot involves multiple sequential steps such as boiling water, adding a 

tea bag, pouring hot water, etc. Learning to plan for longhorizon tasks is a central challenge in episodic learning problems (Wang et al. (2020b)). Decomposing tasks has several advantages. It makes learning individual skills more efficient by breaking them into shorter-horizon, thus aiding exploration. Reusing skills in multiple settings can speed up learning by avoiding the need to relearn elements from scratch each time. Researchers train a hierarchy model to decompose the task into a sequence of subgoals (Ahn et al. (2022)), and observe pre- and post-conditions to ensure that the prerequisites and outcomes of each subgoals are met (Cui et al. (2022)). These three processes are represented as the Hierarchy of Skills module _H_ , the Pre-conditions Detection module _P_ , and the Post-conditions Detection module _P_ in Fig. 2. However, detecting only task success with postconditions detection is insufficient. It should also identify the reasons for task failure to help the robot self-correct and improve success rates. Therefore, we add a Post-hoc Correction module, as shown in Fig. 2. 

Recently, researchers have realized that training policies require real-world interaction between the robot and environments, which inevitably increases the probability of unforeseen hazardous situations. Therefore, researchers aim to train the environment’s transition model _T_ . Once the model is fitted, robot can generate samples based on it, significantly reducing the frequency of direct interaction between the robot and environments (Liu et al. (2024e)). This process is represented as the Transition module _T_ in Fig. 2. 

The modules described above are summarized from the development of robot learning for manipulation. However, they are still insufficient for a comprehensive framework for general manipulation. The ultimate general manipulation framework should be able to interact with human or other agent and control whole-body to manipulate arbitrary objects in open-world scenarios, achieving diverse manipulation tasks. When interacting with human or other agent to understand task objectives, the transmitted instruction may sometimes be unclear, such as when there are two cups in the environment, it needs to determine which cup to pour water. Therefore, we add the Interaction module _I_ in Fig. 2 to understand the precise task objective. 

The aforementioned modules all require datasets for learning. The data collection process for the Hierarchy of skills _H_ and Pre- and Post-conditions detection modules _P_ is similar to that in the fields of CV and NLP. Compared to data collection in CV and NLP domains, gathering datasets for manipulation tasks requires the robot’s trajectory to train the policy. Therefore, we include the Manipulation Data Generation module in Fig. 2. 

We organize the framework of robot learning for general manipulation according to its development history and definition, as shown in Fig. 2. In the caption of Fig. 2, we outline the flow of the entire framework. To better illustrate the role of each module, we list the inputs and outputs of each module below, along with their specific functions. 

1. **Pre-conditions Detection.** This module takes raw information observed by the robot as input. It outputs perception information about objects in the environment and affordances of those object. Perception information helps ensures that requirements are met 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

4 


**Figure 2.** Framework of Robot Learning for General Manipulation. The Pre-conditions Detection module _P_ perceives the environment to identify objects and the affordances objects support. The Interaction module _I_ receives instruction from a human or other agent. It uses perception information from the Pre-conditions Detection module _P_ to check for ambiguities in the instruction. If there are any ambiguities, it generates a question to clarify the instruction by asking the human or other agent. The Hierarchy of Skills module _H_ generates subgoals by using precise instruction from the Interaction module _I_ and perception information from the Pre-conditions Detection module _P_ . Each subgoal is then passed to the Skill Execution module. In the Skill Execution module, Policy module Π generates Action _α_ based on the State _S_ . To obtain the next state after executing the current action, State _S_ can either perceive it from the environment or use the Transition module _T_ . To train the Skill Execution module, including the State module _S_ , the Policy module Π and the Transition module _T_ , the Manipulation Data Generation module is required. This module provides a task-level manipulation dataset. When issues arise during execution, corrective instruction is sent to the Policy module Π for manual adjustment. Policy module Π modifies the current action to corrective action and saves corrective demonstration to the dataset for self-improvement of Policy module Π. After skill execution, Post-conditions Detection module _P_ determines the success of execution. If successful, proceed to the next subgoal; if not, the failure reason is conveyed to Post-hoc Correction module for self-correction. 

and helps select the execution method based on object affordances. For instance, when placing a tea bag in a teacup, perception information can help determine whether there are tea bags and teacups and chooses between pick-place or pushing based on their affordances, such as, a tea bag is spherical, and it has the affordance of rolling when pushed. 

2. **Human/Agent Interaction.** The input to the Human/Agent Interaction module _I_ consists of an instruction or answer from the collaborating agent or human, and perception information from the Preconditions Detection module _P_ . The output includes a question if the instruction or answer has ambiguities and provides a precise instruction to the Hierarchy of Skills module _H_ . The main function of this module is to understand the exact task objectives. 

3. **Hierarchy of skills.** This module takes as input the perception information about objects in the environment and their affordances for the task from the Pre-conditions Detection module _P_ , as well as the precise instruction from the Interaction module _I_ . It then produces a sequence of subgoals as output. The concept of ‘Hierarchy of skills’ often involves creating a sequence of subgoals (Song et al. (2023)). Each subgoal necessitates a skill, which may consist of one or multiple primitive actions (Zhang et al. (2023c)). For instance, tasks like filling the kettle with water, heating the water, and getting the tea leaves are examples of subgoals that robot needs to achieve in a specific order to fulfill the final goal as instructed. 

4. **State.** The input to the State module is the current environment, objects and robot observation. States require the use of multiple sensors for perception. The 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

5 

   - output is the features of states. The states consists of robot proprioception _Srobot_ , environment state _Se_ , and objects states _So_ . The difference between _Se_ and _So_ is analogous to the foreground and background of an image. _Srobot_ generally relates to the mechanical structure of the robot. Currently, there are limited studies focusing on the improvement of robot mechanical structure using foundation models, with Stella et al. (2023) being one of them. However, researches in this direction are scarce and still in their initial stages. 

5. **Policy.** The Policy module takes as input features from the State module _S_ and subgoals generated by the Hierarchy of Skills module _H_ . The policy outputs action to accomplish task goals based on the input states. We categorize action into three types: Code, Key Pose, and Dense Pose. Code refers to the direct control code of the robot. Key Pose refers to the desired poses of the end-effector, which is input to motion planning to generate the trajectory. Dense Pose refers to the next waypoint the end-effector moves to, with continuously outputted dense pose forming the trajectory. At present, the methods for generating actions using foundation models include LLMs directly generating code for robot execution, VLMs directly generating or VLMs combined with LLMs generating corresponding key poses, RFMs directly outputting key poses or dense poses through end-to-end training, and foundation models assisting reinforcement learning in generating various actions. 

6. **Post-conditions Detection.** This module takes as input the environment, objects and robot states observed after the robot performs a task, along with the subgoals generated by the Hierarchy of Skills module H. It outputs whether the current subgoal is successful. If not, it provides the reason for failure to Post-hoc Correction module. The Post-hoc Correction module generates a sequence of actions for self-correction based on the failure reason. For example, if a teacup is knocked over during pick-and-place, inform post-hoc correction and use pick-and-place to upright the cup and reinsert the tea bag. 

7. **Transition.** The Transition module _T_ takes an action generated by the Policy module _P_ as input. It outputs the next state after executing this action, thus helping to reduce the interaction between the robot and the real environment. UniSim (Yang et al. (2023b)) introduces the action-in-video-out framework as an observation prediction model. It takes the current action as input and produces the subsequent observation as output. 

8. **Manipulation Data Generation.** This module functions as a database. It takes in existing manipulation data and correction data generated from robot tasks. The output is to provide task-level manipulation datasets for offline training. 

Current research on foundation models for manipulation primarily focuses on several key modules: the Interaction module in Sec. 3, the Pre- and Post-conditions Detection 

module in Sec. 4, the Hierarchy of Skills module in Sec. 5, the State module in Sec. 6, the Policy module in Sec.7, and the Manipulation Data Generation module in Sec. 8. The following section will provide an overview of these modules. 

## **3 Human/Agent Interaction** 

There are two ways for human or other agent to interact with robot: 1) Providing task instruction to the robot to help it understand the task objective and complete the task independently (Khan et al. (2023)). 2) Collaborating with the human or other agent to complete tasks, sharing workspace information, and conveying corrective instruction when useful or error-correcting information is identified to optimize the robot’s current action (Lynch et al. (2023)). 

When conveying task instruction to the robot, there may contain language ambiguity in the task goal, such as having both red and green cups in the scene, and the task instruction is ‘grasp the cup’. This ambiguity may confuse the robot regarding which color cup to grasp. To address this issue, the robot needs to inquire about and confirm the final task objective from the human or other agent, thus requiring enhancement of their capability in text generation and comprehension. When conveying corrective instruction to a robot, it needs to comprehend the meaning of the corrective instruction and translate corrective instruction into appropriate actions. For instance, if a robot is picking up a book from a shelf filled with books, lifting too quickly may cause other books to fall. Human or collaborating agent need to alert the robot that the current lifting action is dangerous and advise it to lift slowly. If necessary, the robot should also report its current execution state, such as its grasping speed, and inquire whether this speed is considered high. However, corrective instruction are diverse; thus, understanding them is essential. 

In addressing instruction ambiguity and text generation and comprehension challenges, SeeAsk (Mo et al. (2023)) utilizes CLIP’s perceptual module to identify objects in the scene and employs a fixed questioning template to organize language to ask about which object will be manipulated. Although the use of CLIP enhances the generalization ability for object recognition, it can’t generate text for asking questions and to comprehend answers from the outside world and SeeAsk (Mo et al. (2023)) focuses solely on addressing ambiguities concerning object color and spatial relationship due to a fixed questioning template. KNOWNO (Ren et al. (2023a)) utilizes LLM to score the next action to be taken. If the score difference between the top two actions is less than a threshold, it’s considered ambiguity, prompting a confirmation for the final action. This approach improves efficiency and autonomy. Matcha (Zhao et al. (2023c)) not only employs vision but also utilizes haptic and sound senses to perceive object properties, such as material. When encountering ambiguity in object attribute recognition, it leverages LLM to generate inquiry content. CoELA (Zhang et al. (2023b)) utilizes LLM as both a communication module and a planning module to enhance interaction text generation and comprehension, as well as task scheduling, with collaborative agent. LLM-GROP (Ding et al. (2023)) utilizes LLM to extract latent commonsense knowledge embedded within task instruction. For example, 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

6 

a task instruction might be ”set dinner table with plate and fork,” while the latent commonsense knowledge could be ”fork is on the left of a bread plate.” 

As for corrective instruction, LILAC (Cui et al. (2023)) utilizes GPT-3 to distinguish between task instruction and corrective instruction. It then employs Distil-RoBERTa to extract text features and input them into the network to modify the robot’s original trajectory. LATTE (Bucker et al. (2023)), on the other hand, employs BERT and CLIP to extract features from corrective instruction and observation images and input them into the network to modify the robot’s original trajectory. RT-H (Belkhale et al. (2024)) employs VLMs in a two-step operation, initially outputting abstract delta-pose representations like ”move left,” which are then converted into delta poses and human intervention can enable robots to adjust trajectories based on human language instruction. 

## _Summary_ 

Following Fig. 3, LLMs using chain of thought efficiently identifies ambiguity, surpassing the limitations of enumerating ambiguity. LLMs’ comprehension of text effectively understands corrective instruction and transforms the original trajectory into a corrective trajectory. 

## **4 Pre- and Post-conditions Detection** 

In pre- and post-conditions detection, it is necessary to identify the initial and termination conditions. In preconditions detection, recognize objects and observe the affordances of objects. In post-conditions detection, identify whether a task has been successfully executed and provide reasons for task failure after skill execution. Currently, there are few papers focusing on identifying termination conditions. Cui et al. (2022) utilizes CLIP to compare the target’s text or image with the termination environment to determine the success of task execution. Few articles are found in this study that address the output of task failure reasons after skill execution. RobotGPT (Jin et al. (2024)) analysis task failure utilizes the positions of manipulated objects after execution, but task failure should be determined during execution. AHA (Duan et al. (2024)) uses a large number of robotic failure trajectories to fine-tune the VLM. The fine-tuned VLM leverages keyframe trajectory images and task descriptions from the robot’s current task execution process to detect failures and provide detailed, adaptable failure explanations. Therefore, this section focuses on literature discussing foundation models in pre-conditions detection including object affordance and object recognition. 

## _4.1 Object Affordance_ 

The affordances associated with an object represent the range of manipulations that the object affords the robot (Gibson (2014)). Early approaches addressed the issue by treating it as a supervised task (Kokic et al. (2017)). However, the process of annotating datasets is laborious and time-consuming, making it impractical to exhaustively cover all geometric information present in realworld environments. Consequently, researchers are exploring the application of reinforcement learning, enabling robots to 


**Figure 3.** Foundation Models for Interaction Module. Interaction mainly involves the exchange between task instruction and corrective instruction. Ambiguity often arises in task instruction interaction, hence robot needs to detect ambiguities. 1) One approach is to perceive objects in a multi-modal environment and enumerate possible ambiguities based on perception information (Mo et al. (2023)). 2) Another approach involves using LLM to be the next step prediction module, which predicts and scores the next step; if the scores of the top 2 steps are less than _δ_ , it is considered that the task goal is ambiguous (Ren et al. (2023a)). 3) Strong comprehension skills are required during the transmission of corrective instruction, and the current mainstream approach involves using the encoder of LLM to extract tokens and input them into the policy to modify the original trajectory (Bucker et al. (2023)). 

collect data and train affordance perception modules through continuous exploration (Wu et al. (2021)). Nevertheless, current reinforcement learning methods are trained in simulated environments, leading to a significant sim-toreal gap. To address these challenges, researchers propose training the affordance perception module using videos of human interactions in real-world scenarios (Ye et al. (2023b); Bahl et al. (2023)). 

For supervised learning methods, GraspGPT (Tang et al. (2023)) utilizes LLM outputs for object class descriptions and task descriptions. Object class descriptions detail the geometric shapes of each part of an object, while task descriptions outline the desired affordances for task execution, such as the types of manipulation actions to be taken. Integrating both components into the task-oriented grasp evaluator enhances the quality of the generated grasp pose. 3DAP (Nguyen et al. (2023)) utilizes the text encoder of LLM for feature extraction. The extracted features from desired affordances text are inputted into both the affordance detection module and pose generation module. 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

7 

This enhances the quality of the predicted affordance map and the generated pose. 

In reinforcement learning, ATLA (Ren et al. (2023b)) utilizes GPT-3 to generate language descriptions of tools. These descriptions are then inputted into a pre-trained BERT model to obtain representations. The extracted features are finally fed into the SAC network module. Meta-learning techniques are employed to enhance the learning efficiency for the use of new tools. Xu et al. (2023a) employ CLIP’s text and image encoders to extract features from language instruction and scene image, improving the quality of grasp pose generation in the SAC module. 

The methods mentioned above utilize foundation models to assist other learning methods in improving affordance maps or grasp poses. There are also direct approaches using foundation models to generate affordance maps and grasp poses. PartSLIP (Liu et al. (2023d)) converts 3D point clouds into 2D rendering images and inputs multi-view 2D images and textual descriptions of object parts into GLIP for object parts detection, ultimately fusing 2D bounding boxes into 3D segmentation to generate affordance maps. However, PartSLIP requires manual definition text prompts and additional algorithms to convert 2D boxes back to 3D regions. UAD (Tang et al. (2025)) clusters object points into fine-grained semantic regions based on pixel-wise features extracted from multi-view rendered images using DINOv2. It then queries the VLM to generate a set of task instructions and associates these instructions with the most relevant clustered region to construct the affordance map. LAN-grasp (Mirjalili et al. (2023)) inputs human instruction into LLM, utilizing its prior knowledge to output the shape of part to be grasped. These shapes, along with the object’s 2D image, are then inputted into VLM to detect the bounding box for the grasping part. Finally, the bounding box and the point cloud from object 3D reconstruction are inputted into the grasp planner to generate grasp poses. 

## _4.2 Object Recognition_ 

Object recognition can be categorized into two types: passive perception and active perception. Compared to passive perception, active perception adjusts the perspective to the areas of interest (Kroemer et al. (2021)). Then, modeling manipulation tasks and generalizing manipulation skills necessitate representations of both the robot’s environment and the manipulated objects. These representations form the foundation for skill hierarchies, pre- and post-condition detection, skill learning, and transition model learning. 

The Vision Transformers (ViTs) and similar attentionbased neural networks have recently achieved state-of-theart performance on numerous computer vision benchmarks (Han et al. (2022); Khan et al. (2022); Zhai et al. (2022)) and the scaling of ViTs has driven breakthrough capability for vision models (Dehghani et al. (2023)). The development of visual backbones not only advances pre-trained visual representations but also accelerates the progress of open-set perception tasks, such as segmentation and detection. 

As for pre-trained visual representations, the algorithms mentioned have various training objectives: for instance, contrastive methods like Vi-PRoM (Caron et al. (2021)), R3M (Nair et al. (2022)), VIP (Ma et al. (2022)), CLIP 

(Radford et al. (2021)), LIV (Ma et al. (2023a)); distillationbased methods such as DINO (Caron et al. (2021)); or masked autoencoder methods like MAP (Radosavovic et al. (2023)), MAE (He et al. (2022)). The primary datasets utilized comprise the CLIP dataset (Radford et al. (2021)), consisting of 400 million (image, text) pairs sourced from the internet, along with ImageNet (Deng et al. (2009)), Ego4D (Grauman et al. (2022)), and EgoNet (Jing et al. (2023)). 

Pre-trained visual representations have high transfer ability to policy learning (Xiao et al. (2022b); Yang et al. (2023c)), but visual representation involves not just recognizing spatial features but also understanding semantic features. Masked autoencoding methods prioritize low-level spatial aspects, sacrificing high-level semantics, whereas contrastive learning methods focus on the inverse (Karamcheti et al. (2023)). The fusion of masked autoencoder and contrastive learning is employed in both Voltron (Karamcheti et al. (2023)) and iBOT (Zhou et al. (2021)). The loss function achieves a balanced trade-off between these two aspects. To compare different pretrained visual representations, benchmarks are established by CORTEXBENCH (Majumdar et al. (2023)) and EmbCLIP (Khandelwal et al. (2022)) to assess which model could provide a better ”artificial visual cortex” for manipulation tasks. However, the models included in these benchmarks are still not comprehensive enough. 

The aforementioned pre-trained visual representations mainly involve the extraction of features from 2D images. The experience of learning representations on 2D images can also be extended to other modalities. For the object point cloud modality, ULIP (Xue et al. (2023a)) and ULIP2 (Xue et al. (2023b)) employ contrastive learning to align features between point clouds and text-images. PointBERT (Yu et al. (2022)) uses the masked autoencoding method to learn point cloud features by reconstructing point clouds. GeDi (Poiesi and Boscaini (2022)) uses a contrastive learning approach to extract general and distinctive 3D local geometric information. In the haptic modality, MOSAIC (Tatiya et al. (2023)) utilizes contrastive learning to train the haptic encoder. 

As for segmentation, SAM (Kirillov et al. (2023)) develops a transformer-based architecture and creates the largest segmentation dataset, with over 1 billion masks from 11 million images. The model is adaptable and enables zeroshot transfer to new tasks and image distributions. FastSAM (Zhao et al. (2023b)) and Faster-SAM (Zhang et al. (2023a)) aim to improve the training and inference speed of the network by enhancing its network structure. TAM (Yang et al. (2023a)) merges SAM (Yang et al. (2023a)) and XMem (Cheng and Schwing (2022)) for high-performance interactive tracking and segmentation in videos. 

As for detection, traditional detection models are usually confined to a narrow range of semantic categories because of the cost and time involved in gathering localized training data within extensive or open-label domains. However, advancements in language encoders and contrastive imagetext training enable open-set detection. Researchers integrate language into a closed-set detector to generalize openset concepts, detecting various classes through language generalization despite being trained solely on existing bounding box annotations, such as OWL-ViT (Minderer 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

8 


**Figure 4.** Foundation Models for Pre-conditions Detection. As for object affordance, the main approaches of task-oriented grasp are supervised learning and reinforcement learning. Both methods utilize LLM to generate object part-level description and desired affordance description in task instruction, then fuse tokens and features into the original network through language encoder and image encoder to output task-oriented grasp pose (Tang et al. (2023); Ren et al. (2023b)). In reinforcement learning, it is possible to choose between a LLM language encoder with a custom-designed image encoder, or a VLM language encoder with a VLM image encoder. When selecting the LLM language encoder with a custom image encoder, the LLM language encoder should be frozen, and the custom image encoder should be trained (Ren et al. (2023b)). When using the VLM language encoder with the VLM image encoder, both encoders are typically frozen (Xu et al. (2023a)). Direct using foundation method utilizes LLM to generate object part-level description and desired affordance description according to task instruction. VLM marks out the part of the object to grasp in the image based on the description (Liu et al. (2023d)). As for object recognition, the representation learning methods in state perception mainly include contrastive learning (Radford et al. (2021)), distillation-based learning (Caron et al. (2021)), and masked autoencoder learning (Radosavovic et al. (2023)). Masked autoencoding methods prioritize low-level spatial aspects, sacrificing high-level semantics, whereas contrastive learning methods focus on the inverse, the fusion of masked autoencoder and contrastive learning is employed in both Voltron (Karamcheti et al. (2023)) and iBOT (Zhou et al. (2021)). Multimodal representation learning focuses primarily on multimodal alignment (Xue et al. (2023b); Tatiya et al. (2023)). Training the encoder with large-scale data and parameters has facilitated open-set perception, including tasks such as open-set detection, open-set segmentation. For instance, SAM (Kirillov et al. (2023)) utilizes the MAE (He et al. (2022)), ViLD (Gu et al. (2021)) employs the CLIP (Radford et al. (2021)). 

et al. (2022)), Grounding-DINO (Liu et al. (2023f)), OVD (Zareian et al. (2021)), ViLD (Gu et al. (2021)), DetCLIP (Yao et al. (2022a)). 

Deploying such models in open-set detection presents a significant challenge, primarily because even slight alterations in prompting can greatly impact performance. Fine-tuning can enhance a foundation model’s understanding of prompting. However, foundation models are often overparameterized, leading to slow training processes. COOP (Zhou et al. (2022)) maps prompting to a set of learnable vectors, which can be optimized through network training. In CLIP-Adapter (Gao et al. (2024)), two extra linear layers are appended after the final layer of either the vision or language backbone to enable efficient few-shot transfer learning through fine-tuning. 

The method for open-set detection on 2D images can be extended to the research direction of open-set detection on 3D point clouds. PointCLIP (Zhang et al. (2022b)) utilizes 

pre-trained CLIP to extract multi-view depth image features of point cloud, then compares the extracted features with textual features to identify the point cloud category. 

## _Summary_ 

As shown in Fig. 4, LLM provides object part-level knowledge via text, aiding in affordance map or grasp pose generation. Reinforcement learning can make robotic systems perform better though interaction than supervised learning trained on datasets. Direct use of foundation models avoids training. However, stability remains a concern. In object recognition, representation learning aligns multimodal features with text, improving model cognition, similar to human think with words. It also supports open-set perception tasks, like detection and segmentation. 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

9 

## **5 Hierarchy of skills** 

The skill hierarchy is closely related to the field of task and motion planning (TAMP). TAMP aims to address high-level instructions by organizing tasks in a sequence that ensures dynamic feasibility (Guo et al. (2023)). There are three main types of classical TAMP methods: constraint-based TAMP, sampling-based TAMP, and optimization-based TAMP (Zhao et al. (2024)). Constraint-based and samplingbased TAMP define the problem with goal conditions. Unlike optimization-based TAMP, these approaches often cannot assess or compare the quality of the generated plan or final state due to the lack of objective functions, such as when the goal is to pour as much water as possible into the cup (Zhao et al. (2024); Zhang et al. (2022a)). However, optimizationbased TAMP is sensitive to the initial conditions and goal setup of the problem (Zhao et al. (2024)). 

The scalability of classical TAMP methods is often constrained by the tree search problem size for complex tasks and the computational cost of evaluating heuristics and optimal trajectories (Zhao et al. (2024)). Integrating learning-based approaches into TAMP enables informed decision-making based on prior examples and experiences and improves flexibility and generalizability (Guo et al. (2023)). Models for skill hierarchy can be trained using text or videos, similar to how humans learn assembly procedures from instructional manuals or tutorial videos. As for tutorial videos, VLaMP (Patel et al. (2023) and SeeDo (Wang et al. (2024a)) use trained models to understand human video operations and HourVideo (Chandrasegaran et al. (2024)) proposes a benchmark dataset specifically designed for hourlong video-language understanding. 

Traditional TAMP’s domain representations are usually manually specified by expert users such as PDDL (Silver et al. (2022)). However, LLMs have been explored for processing and interpreting natural language inputs (Huang et al. (2022)). They offer a novel approach to encoding the planning domain in a more intuitive and accessible way. Furthermore, LLMs’ acquisition of world knowledge and commonsense reasoning has the potential to improve the scalability and generalizability of skill hierarchy tasks (Vemprala et al. (2023); Jansen (2020); Driess et al. (2023)). Various benchmarks such as PlanBench (Valmeekam et al. (2023)) can assess the planning and reasoning capability of LLMs. 

LLMs possess a notable limitation: they lack practical experience, hindering their utility for decision-making within a specific context, so the output of LLMs often cannot be translated into executable actions for the robot. Huang et al. (2022) first use pre-trained causal LLM to break down highlevel tasks into logical mid-level action plans. Then, a pretrained masked LLM is employed to convert mid-level action plans into admissible actions. However, prompts usually require the context of the robot’s capability, its current state, and the environment. At the same time, LLMs are considered ‘forgetful’ and don’t treat information in the system prompt as absolute. Despite efforts to reinforce task constraints in the objective prompt and extract numerical task contexts from the system prompt, storing them in data structures, errors caused by LLM forgetfulness remain unresolved (Chen and Huang (2023)). 

To address the aforementioned issues, SayCan (Ahn et al. (2022)) scores pre-trained tasks based on prompting and observation images, generating the task sequence with the highest score. Saycan provides a paradigm for generating action sequences using LLM, but there are still some drawbacks: 1) The generated action sequences do not incorporate user preferences. 2) Safety regulations are not adequately addressed. 3) The limitation of the skill library. 4) LLM focuses solely on reasoning when generating action sequences, neglecting feedback on action execution. 5) The limitation of scene grounding. GD (Huang et al. (2023d)) proposes a paradigm to address the aforementioned issues by not only scoring the generated action sequence using LLM but also introducing a grounded function model for scoring the generated action sequence. The grounded function model encompasses token-conditioned robotic functions, such as affordance functions that capture the abilities of a robot based on its embodiment, safety functions, and more. This approach tackles drawbacks by designing grounded functions, avoiding fine-tuning in LLM. 

Regarding user preferences, TidyBot (Wu et al. (2023b)) trains LLM by collecting users’ preference data, enabling the trained LLM to choose behaviors that better align with user preferences. As for safety regulations, Yang et al. (2023d) incorporate ISO 61508, a global standard for safely deploying robots in industrial factory settings, into the constraints of the action sequence generation. As for the skill library, BOSS (Zhang et al. (2023c)) suggests using LLMs’ rich knowledge to guide skills chaining in the skill library, aiming to create new skills through combinations. RoboGen (Wang et al. (2023e)) employs generative models to create new skill task scenarios, then utilizes either reinforcement learning or gradient optimization methods to automatically learn new skills based on the reward function generated by the LLM. As for action execution feedback, REACT (Yao et al. (2022b)), COWP (Ding et al. (2022)), LLMPlanner (Song et al. (2023)), CoPAL (Joublin et al. (2023)) and PROGPROMPT (Singh et al. (2023)) provide feedback on robot action execution to LLMs. This allows LLMs to adjust action sequences based on execution status, creating a closed-loop process for generating action sequences. 

As for the limitation of scene grounding, LLMs need to inquire about the scene representation to determine the availability, relationship and location of objects. NLMap (Chen et al. (2023a)) proposes an open-vocabulary, queryable semantic representation map built on ViLD and CLIP. This map outputs the pose of related objects based on task instruction, which are then handed over to the LLM for planning. Text2Motion (Lin et al. (2023)) incorporates a geometric value function on top of the value function, enabling the robot to select actions that adhere to geometric constraints based on scene descriptions. Xu et al. (2023b) explore the possibility of teaching robots to creatively utilize tools within scenarios, which involve implicit physical limitations and require long-term planning. VILA (Hu et al. (2023a)) seamlessly incorporates perceptual data into ChatGPT-4V for its reasoning and planning processes, facilitating a deep comprehension of common sense knowledge within the visual domain, encompassing spatial arrangements and object characteristics. PHYSOBJECTS (Gao et al. (2023)) fine-tunes a VLM to enhance its 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

10 


**Figure 5.** Foundation Models for Hierarchy of Skills. 1) Utilize human operation video to learn the skill sequence for task execution, decompose the video of the user’s progress so far into observations and human actions through segmentation, and input them along with task instruction into a pre-trained language model to predict the next step (Patel et al. (2023)). 2) LLM scores the skills in the skill library based on task instruction and the skills already executed, and the value function also scores the skills in the skill library based on observation images. The highest-scoring skill, obtained by multiplying the two scores, is selected as the next step (Ahn et al. (2022)). The value function can consider multiple factors such as affordance, safety, user preference, and more (Huang et al. (2023d)), and these considerations can also be fine-tuning LLM (Wu et al. (2023b)). 3) LLM assists the classical planner by translating task instruction into PDDL descriptions, sending them to the classical planner to generate a PDDL plan, and then translating the PDDL plan into a natural language plan using LLM (Liu et al. (2023a)). 

understanding of physical object attributes, such as material. This integration of a physically informed VLM into an interactive framework with a LLM enhances task planning performance in tasks incorporating instruction related to physical object attributes. SpatialVLM (Chen et al. (2024b)) and 3D-LLM (Hong et al. (2023a)) utilizes a 2D pretrained VLM to train on collected 3D datasets, enhancing capabilities related to 3D tasks while maintaining the abilities of previous tasks. 

The hierarchy of skills possessed by LLMs or VLMs can be applied not only to single agent but also to multiple agents. SMART-LLM (Kannan et al. (2023)) utilizes LLM for the hierarchy of skills and allocates each task to every agent through the task assignment module. 

Regardless of whether the prompting input to LLMs is in natural language or PDDL format, the hierarchy of skills possessed by LLMs still exhibits instability (Silver et al. (2022)). Hence, researchers are exploring approaches that integrate LLMs with classical PDDL-based planning methods for the hierarchy of skills. LLM+P (Liu et al. (2023a)) utilize LLMs to translate natural language into PDDL and input into a classical planner for the hierarchy of 

skills. Xie et al. (2023b) indicate that LLMs exhibit greater efficacy in translation tasks as opposed to planning. 

## _Summary_ 

According to Fig. 5, the hierarchy of skills is mainly divided into video instruction and language instruction. VFM and LLM play roles in perception and reasoning. Language instruction is further divided into methods based on foundation models and methods combining foundation models with classical TAMP. As shown in Appendix.C Tab. 6, there is currently no significant research comparing video instruction and language instruction. However, from the modality perspective, video provides more temporal or spatial dependencies regarding tasks compared to language. This also means that video instruction requires a higher level of hierarchy of skills, not only needing to output task plans but also understanding the task and scene constraints from the video. Language instruction is more suitable for interaction and reasoning for LLMs/VLMs. However, the two share some similarities. Current research on the hierarchy of skills in language and video instruction tends to focus on SOTA VLMs, and both have similar failure modes, indicating that both face challenges in perception and reasoning. In the language instruction methods, the combination of foundation models and classical TAMP is more reliable than foundation models alone, but it also faces limitations in generalization. Therefore, how to better integrate foundation models with classical TAMP requires further research. 

## **6 State** 

The State module focuses on perceiving the environment, objects, and robot states. Section. 4 introduces lowlevel perception methods. This section explains high-level approaches for 3D reconstruction and pose estimation. 

## _6.1 3D Reconstruction_ 

3D reconstruction involves capturing both the shape and appearance of an object or scene (Wikipedia Contributors (2025)). 3D reconstruction methods are divided into passive and active types (Butime et al. (2006)). Active methods involve contact or project some form of energy onto the object, such as Laser Scanning (Butime et al. (2006)), X- ray (Maken and Gupta (2023)). These devices have high accuracy, but they are usually expensive. Therefore, various studies focus on 3D reconstruction using consumer RGBD cameras, such as Microsoft Kinect, Intel RealSense, Google Tango, and ORBBEC Gemini (Li et al. (2022)). 

These consumer cameras typically use principles such as structured light, time of flight, and traditional photometric stereo for depth estimation (Zhou et al. (2024a)) and 3D representation can be generated by registering them using camera poses (Huang et al. (2024b)). However, when surfaces are shiny, bright, transparent, textureless or distant from the camera, depth images produced by consumer cameras are often noisy and incomplete. Several studies have addressed this challenging problem by learning to restore depth images (Dai et al. (2022); Fang et al. (2022); Sajjan et al. (2020)). However, the correct depth information may 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

11 

already be lost in the original depth. ASGrasp (Shi et al. (2024)) demonstrates that 3D reconstruction using raw multiview images from consumer cameras is better than restoring the original depth. Many studies use a single image for 3D reconstruction (Fu et al. (2021)). However, a single image loses a significant amount of information, resulting in lower accuracy. Despite this, the zero-shot capability of current single image 3D reconstruction has led to its widespread application in simulation scene generation (in Sec. 8.3). 

The 3D representation for 3D reconstruction can be expressed as explicit and implicit expressions (Zhou et al. (2024a)). Explicit expressions include point clouds (Shi et al. (2024)), voxels (Jiang et al. (2021)), and meshes (Wen et al. (2019)). The three representations can be converted into each other (Jiang et al. (2021)), but each has its own advantages. A point cloud is made up of discrete points in space, providing flexibility in processing. A voxel can store spatial information inside an object but comes with high space complexity. A mesh uses triangle meshes to represent complex shapes and details accurately, such as deformation (Wen et al. (2019)). It ensures the projection is always convex, making it easier to rasterize (Zhou et al. (2024a)). Implicit expressions represent 3D geometry using a function, such as signed distance function (SDF) (Chabra et al. (2020)), occupancy field (Jiang et al. (2021)), and radiance field (Mildenhall et al. (2021)). They offer differentiability and efficient storage, making them a powerful tool. In contrast, explicit expressions tend to be more intuitive. 

GIGA (Jiang et al. (2021)) points out that manipulation requires a fine-grained understanding of local geometry details. Implicit representations, due to their continuous and differentiable nature, can represent smooth surfaces at high resolution. As a result, there is a growing research using implicit representations for manipulation tasks (Dai et al. (2023); Lu et al. (2024)). Current state-of-the-art methods for representing scenes using implicit representations are mainly divided into Nerf-based (Wang et al. (2023b)) and 3DGSbased approaches (Kulhanek and Sattler (2024)). Compared to Nerf (Mildenhall et al. (2021)), 3DGS offers better realtime performance (Kerbl et al. (2023)). However, these implicit 3D representations currently lack scene semantics and not easily editable for 3D modifications (Bai et al. (2024)). 

As for scene semantics, semantic-NeRF (Zhi et al. (2021)) employs manually annotated semantic labels to jointly encode semantics, appearance, and geometry using NeRF. Manual annotation is time-consuming and labor-intensive. Due to the foundation model’s robust open-set capability for objects, DFF (Shen et al. (2023)), CLIP-Fields (Shafiullah et al. (2022)) and LERF (Kerr et al. (2023)) employ CLIP image encoder to extract features from multi-view 2D images for NeRF (Mildenhall et al. (2021)) reconstruction. These features are integrated as part of the output of the NeRF network, enriching the semantic information of the reconstructed 3D scenes. When a text prompt is provided, the features output by the CLIP text encoder can be compared with the CLIP image features output by NeRF to form a relevancy map. This relevancy map can support downstream tasks, such as semantic scene completion and object localization (Ha and Song (2022)). Since CLIP can only provide image-level features, the relevancy map lacks precise 

pixel-level object boundary information. 3DOVS (Liu et al. (2023c)) incorporates DINO features into the NeRF output to distill object boundary information. OV-NeRF (Liao et al. (2024)) addresses the issues of coarse relevancy maps and view-inconsistent relevancy maps through SAM and cross-view self-enhancement. FMGS (Zuo et al. (2025)) transfers this concept from NeRF to 3DGS, achieving 851X faster inference. Although foundation models, such as CLIP and DINO, enable 3D open-set semantic scene understanding, the performance is limited by the foundation models themselves. For example, CLIP is constrained by the bag-of-words limitation (Kerr et al. (2023)). 

The image features output by NeRF can be used to build a relevancy map. They can also be lifted into 3D space through multi-view images, serving as 3D features for downstream tasks (Ze et al. (2023)). 3D-LLM (Hong et al. (2023b)) extracts 2D features from multi-view rendered images using the CLIP image encoder. These features are then fused into 3D features through Direct Reconstruct, gradSLAM (Jatavallabhula et al. (2023)), or Neural Field methods (Hong et al. (2023b)), endowing 3D features with semantic information. 

For implicit 3D editing, some methods use human scribbles to edit 3D shape and appearance (Zhang et al. (2023d); Schwarz et al. (2020); Li and Pan (2024); Liu et al. (2021)). However, this approach is not intuitive enough. With the development of foundation models, many methods for implicit 3D editing using text prompts have emerged. CLIPNeRF (Wang et al. (2022a)) integrates semantic features extracted by CLIP into NeRF reconstruction to change object shape and appearance during rendering. However, CLIPbased approaches cannot precisely modify specific local regions. Instruct-NeRF2NeRF (Haque et al. (2023)) utilizes InstructPix2Pix (Brooks et al. (2023)) to iteratively edit multiview input images and optimize the underlying scene in NeRF. This process produces a refined 3D scene that adheres to the edit instruction. However, InstructPix2Pix modifies the entire image. As a result, regions that are not desired may also be altered. DreamEditor (Zhuang et al. (2023)) uses Dreambooth (Ruiz et al. (2023)) to generate 2D editing masks. These masks are then converted into 3D editing regions through back projection. This approach enables precise local editing. 

## _6.2 Pose Estimation_ 

Object pose estimation can be divided into marker-based and markerless methods (Karashchuk et al. (2021)). Markerbased methods require attaching passive or active markers (Cassinis and Tampalini (2007)) to the object. These methods achieve high accuracy in pose estimation. For example, the NDI Polaris Vega XT, commonly used in medical robotics, can achieve an accuracy of 0.12 mm RMS (NDI (2024)). However, in unstructured environments, it is not feasible to attach specific markers to every object. Therefore, achieving object pose estimation in unstructured markerless environment is necessary. 

From the perspective of generalization, pose estimation methods can be classified into instance-level, category-level, and unseen object approaches (Liu et al. (2024c)). Instancelevel methods can estimate pose accurately for specific object instances on which they are trained. However, they struggle 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

12 

with novel objects. To improve the model’s adaptation for pose estimation of novel objects, category-level approaches use geometric priors from objects of the same category to estimate the pose of the novel object without requiring its 3D model (Wang et al. (2019)). Unseen object approaches typically rely on the 3D model of the novel object to estimate its pose (Caraffa et al. (2024)). 

Category-level and unseen object approaches can also be primarily classified into model-free and model-based approaches (Liu et al. (2024c)). Model-free methods do not require prior knowledge of the object’s 3D model. These methods typically regress the object pose using neural network (Guan et al. (2024)). However, these methods require large amounts of data for the neural network to learn the geometric priors of the object. In contrast, model-based methods use a known 3D model of the object and usually lead the BOP benchmark for object pose estimation (Burde et al. (2024)). However, obtaining accurate object 3D models in the real world is not easy. The advancement of multi-view image 3D reconstruction technology bridges the gap between model-based and model-free real-world applications (Burde et al. (2024)). 

The input modalities for the model-based approach include RGB, depth, and RGBD. Currently, the RGBD modality leads the BOP benchmark for object pose estimation. The optimization goals are primarily divided into three parts: 2D-2D correspondences followed by regression (Nguyen et al. (2024)), 2D-3D correspondences followed by PnP (Li et al. (2023b); Ausserlechner et al. (2024)), and 3D-3D correspondences followed by least squares fitting (Lin et al. (2024b); Caraffa et al. (2024)). However, pose estimation accuracy remains a challenge when dealing with occlusion, specularity, symmetry and textureless objects (Guan et al. (2024)). Many methods use the predicted pose as a coarse result and refine it to obtain a fine result (Labb´e et al. (2022); Wen et al. (2024a); Moon et al. (2024)). 

The pose estimation of moving objects mainly involves two methods. 1) Some single-image 6D pose estimation methods are fast and re-estimate poses from scratch for each frame. However, this approach is inefficient and results in less coherent estimations (Wen and Bekris (2021)). 2) Pose tracking utilizes temporal cues to improve pose prediction. It enhances efficiency, smoothness, and accuracy in video sequences. Current pose-tracking methods are mainly divided into probabilistic tracking (Deng et al. (2021); Issac et al. (2016); Stoiber et al. (2022)) and optimization-based tracking (Li et al. (2018); Wen et al. (2020); Lin et al. (2022); Wang et al. (2020a)). Pose tracking faces challenges mainly from motion blur, incremental error drift, and occlusion. To address these issues, BundleSDF (Wen et al. (2023a)) and BundleTrack (Wen and Bekris (2021)) use an online pose graph optimization process. 

There are some research integrating foundation models into pose estimation. As for category-level, OV9D (Cai et al. (2024)) utilizes DINO and VQVAE to extract visual features from images, while CLIP is used to extract text features from category prompts. These features are then fed into the Stable Diffusion UNet (Rombach et al. (2022)) to generate a normalized object coordinate space (NOCS) map. This method achieves generalizability to unseen categories and enables open-set pose estimation. In unseen object 


**Figure 6.** Foundation Models for State. The foundation models have three main applications in 3D reconstruction: 3D openset semantic scene understanding, lifting 2D features to 3D space, and implicit 3D editing. In 3D open-set semantic scene understanding, the main pipeline is to use image features extracted by the VFM encoder and VLM image encoder as input for NeRF. Then, semantic text features extracted by the VLM language encoder are used in conjunction with the image features from NeRF to generate a relevancy map through a relevancy extractor (Kerr et al. (2023)). This relevancy map can support downstream tasks, such as semantic scene completion and object localization (Ha and Song (2022)). As for lifting, using the VLM image encoder to extract features from 3D data multi-view images and lift them into 3D features can incorporate semantic information into the 3D features. The lifting methods include direct reconstruction, gradSLAM, and Neural Field (Hong et al. (2023b)). For implicit 3D editing, the current mainstream pipeline is to input the image rendered by NeRF and the editing prompt into the VGM to generate the updated image. The updated image is then fed back into NeRF for training, modifying NeRF’s radiance field representation of the 3D scene (Haque et al. (2023)). Pose estimation with foundation models achieves state-of-the-art results (Caraffa et al. (2024)). The main method is 2D-lifting-3D. It extracts texture features from the object model and observation RGBD image. LMM extracts geometric features from the object model and observation RGBD image. The fused features are then used to estimate the 6D pose through 3D-3D correspondences. 

pose estimation with foundation models, FoundationPose (Wen et al. (2024a)) utilizes LLM-aided synthetic data generation at scale to ensure strong generalizability for novel object pose estimation & tracking. SAM-6D (Lin et al. (2024b)) and ZS6D (Ausserlechner et al. (2024)) leverage SAM to generate valid proposals, enabling zeroshot 6D pose estimation. FreeZe (Caraffa et al. (2024)) employs frozen GeDi (Poiesi and Boscaini (2022)) and DINO (Caron et al. (2021)) to extract both geometric and visual features from the query object model and the target object’s RGBD observation image. It then uses 3D-3D fused feature correspondences to obtain the 6D pose. Due to the foundation models’ robust capability in discriminative feature extraction, FreeZe achieves state-of-the-art results without the need for any data or training. Overall, foundation models primarily improve generalization for novel object 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

13 

pose estimation in three areas: data , object recognition, and feature extraction. However, the performance is limited by the foundation models themselves. For example, foundation models are large in size (Caraffa et al. (2024)) and SAM may hallucinate in object segmentation (Kirillov et al. (2023)). 

## _Summary_ 

Following Fig. 6, VLM and VFM assist implicit 3D reconstruction by generating relevancy maps that include semantic information (Kerr et al. (2023)). They can also be employed in 2D-to-3D lifting to extract 3D features, encompassing texture, semantic, and spatial information (Hong et al. (2023b)). VGM aids in generating edited images and modifying 3D scenes based on these edited images (Haque et al. (2023)). FreeZe (Caraffa et al. (2024)) achieves state-of-the-art result in pose estimation by extracting discriminative features through 2D-to-3D lifting and LMM. 

## **7 Policy** 

The policy is divided into two categories: object/actioncentric methods and end-to-end methods. Object/actioncentric methods extract attributes from observations, such as bounding boxes, masks (Sajjan et al. (2020)), or 3D spatial action-value map (Shi et al. (2024)). These extracted attributes are then transformed into either a sequence of key poses or a single key pose, which is used in motion planning to guide robot motion. End-to-end methods directly map observation to robot action (Chi et al. (2023)). They eliminate the need for attribute extraction. 

End-to-end methods are mainly divided into reinforcement learning (Herzog et al. (2023)) and imitation learning (Dasari et al. (2019)). Recent end-to-end methods have made significant progress. ACT (Zhao et al. (2023a)) uses action chunks to reduce compounding errors. Diffusion policy (Chi et al. (2023)) applies the idea of diffusion to visuo-motor control, tackling challenges such as action multimodality and sequential correlation to handle high-dimensional action sequences. 

However, the above methods are all one-model-forone-task, lacking general-purpose capability. Due to the development of foundation models, general-purpose models have advanced. The representation of task instruction can be categorized into four types: language, human video, goal image, and multimodal prompts. BC-Z (Jang et al. (2022)) and Vid2Robot (Jain et al. (2024)) introduce a video-conditioned policy that uses human video as task instructions. DALL-E-Bot (Kapelyukh et al. (2023)) employs DALL-E to generate target images for tasks and generates actions for manipulation by combining the target image with the observation image. VIMA (Jiang et al. (2023)) and MIDAS (Li et al. (2023c)) observe that many robot manipulation tasks can be represented as multimodal prompts intertwining language and image/video frames. They construct multimodal prompts manipulation datasets and utilize pre-trained language foundation models for finetuning to control robot outputs. MUTEX (Shah et al. (2023)) extends instruction to various modalities and develops speech-conditioned, speech-goal-conditioned, image-goalconditioned, and text-goal-conditioned. 

Language-conditioned general-purpose policies remain the predominant paradigm in current research. RT-2 (Brohan et al. (2023)) refers to this approach as **V** ision- **L** anguage- **A** ction (VLA). Following this naming convention, we divide the policy into **V** ision- **L** anguage- **A** ction- **K** ey- **P** ose (VLAKP), **V** ision- **L** anguage- **A** ction- **D** ense- **P** ose (VLADP). VLAKP is more similar to traditional object/actioncentric approaches. On the other hand, VLADP resembles traditional end-to-end methods. Recent studies have explored the use of foundation models to directly synthesize low-level policy code (Liang et al. (2023); Yoshida et al. (2025)). Such policies generate executable code for robots, enabling finegrained human inspection and debugging. We denote this paradigm as **V** ision- **L** anguage- **A** ction- **C** ode (VLAC). 

The above methods integrate foundation models into policy models to guide action generation. Currently, some approaches leverage foundation models to assist in reinforcement learning training. 

## _7.1 VLAC_ 

Code generation and program synthesis have been demonstrated to be capable of developing generalizable, interpretable policy (Trivedi et al. (2021). However, a robot capable of generating code for multiple tasks, rich knowledge across various domains is essential (Ellis et al. (2023)). Therefore, scholars aim to apply the prior knowledge of LLM to code generation task (Chen et al. (2021b); Austin et al. (2021)). Code-As-Policy (Liang et al. (2023)) demonstrates the possibility of using LLMs to directly generate code for robot execution based on prompts. The study shows that 1) code-writing LLMs enable novel reasoning capability, such as encoding spatial relationships by leveraging familiarity with third-party libraries and 2) hierarchical code-writing inspired by recursive summarization improves code generation. Fromtext-to-motion (Yoshida et al. (2025)) translates descriptions of human actions into humanoid robot motion code, enabling it to perform various tasks autonomously. 

## _7.2 VLAKP_ 

The utilization of foundation models to generate key poses can be categorized into two approaches: 1) Directly using existing foundation models to output key poses. 2) Training RFMs to generate key poses through imitation learning. 

Utilizing foundation models pre-trained on existing largescale internet datasets enables the direct perception of observation images and outputting key poses. Instruct2Act (Huang et al. (2023b)) utilizes CLIP and SAM to identify manipulated objects within an observation image and outputs the 3D position of these manipulated objects. Voxposer (Huang et al. (2023c)) utilizes LLMs to generate code that interacts with VLMs to produce affordance maps and constraint maps, collectively referred to as value maps, grounded in the robot’s observation space. These composed value maps serve as objective functions for motion planners to synthesize trajectories for robot manipulation. ReKep (Huang et al. (2024a)) uses VFM and VLM to extract relational keypoint constraints from language instructions and RGBD observations. It then applies an optimization solver to generate a series of end-effector poses. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

14 

As for imitation learning methods, CLIPort (Shridhar et al. (2021)) demonstrates the capability of imitation learning in language-conditioned general manipulation. However, CLIPort (Shridhar et al. (2021)) addresses 4-DoF endeffector pose prediction by treating it as a pixel classification problem. Keypoint-based approaches are extended to handle 6-DoF end-effector pose prediction. Due to keypoint-based methods primarily focus on 3D scene-to-action tasks, these methods become computationally expensive as resolution requirements increase (Ke et al. (2024)). To address high spatial resolution, PerAct (Shridhar et al. (2023)) uses the latent set self-attention of Perceiver (Jaegle et al. (2021)), which has linear complexity with voxels. Act3D (Gervet et al. (2023)) represents scenes as a continuous 3D feature field, transforming 2D model features into 3D feature clouds using sensed depth and learns a 3D feature field of arbitrary spatial resolution through recurrent coarse-to-fine point sampling. 

Some research has extended the work on PerAct (Shridhar et al. (2023)) and Act3D (Gervet et al. (2023)). ChainedDiffuser (Xian et al. (2023)) builds upon Act3D (Gervet et al. (2023)) by replacing the motion planner with a diffusion model. This approach addresses the challenges of continuous interaction tasks. The 3D Diffuser Actor (Ke et al. (2024)), similar to Act3D (Gervet et al. (2023)), employs tokenized 3D scene representations. However, unlike Act3D (Gervet et al. (2023)) and 3D Diffusion Policy (Ze et al. (2024b)) with 1D point cloud embeddings, 3D Diffuser Actor (Ke et al. (2024)) leverages CLIP to extract features from 2D images and aggregates them into a 3D scene representation. GNFactor (Ze et al. (2023)) improves upon PerAct (Shridhar et al. (2023)) by enhancing 3D semantic features. It achieves this by distilling pre-trained semantic features from 2D foundation models into Neural Radiance Fields (NeRFs). DNAct (Yan et al. (2024)) builds on GNFactor (Ze et al. (2023)) and transforms the perceiver model into a diffusion head. VoxAct-B (Liu et al. (2024b)) uses VLM to divide the task into subtasks for the left arm and the right arm and applies PerAct (Shridhar et al. (2023)) to generate separate key poses for each arm. 

The current imitation learning approaches also include methods using large-scale LLM/VLM. LEO (Huang et al. (2023a)) expands upon language foundation models by incorporating modalities like images and 3D point clouds. It fine-tunes manipulation datasets using the LoRA method. This showcases the ability to transfer the original foundation model to more modalities and manipulation tasks. Xu et al. (2024) considers the object motion produced by LLM/VLM, the object’s physical properties, and the end-effector’s design and creates a ManiFoundation model to generate the key pose. However, the key pose output by the ManiFoundation model is not 6D pose. Instead, it provides the positions of multiple contact points and the force to be applied at each contact point. 3D-VLA (Zhen et al. (2024)) can generate the final state image and point cloud based on user input. This goal state is then used to create key poses in 3D VLA. 

## _7.3 VLADP_ 

The policy model for outputting dense pose resembles more closely the paradigm of human task execution, as it does not require camera and spatial calibration or robot body 

configuration. Instead, it takes observation images as input and directly outputs the direction and magnitude of the next waypoint. While this approach is more end-to-end, it still necessitates extensive data training to embed the parameters of robot execution in the policy model’s hidden layers. 

Effective robotic multi-task learning necessitates a highcapacity model, hence Gato (Reed et al. (2022)) and RT-1 (Brohan et al. (2022)) devise transformer-based architectures. Nonetheless, RT-1 and Gato differ; RT-1’s input lacks proprioception from the robot body, while Gato incorporates proprioception. Building upon Gato, RoboCat (Bousmalis et al. (2023)) demonstrates that a large sequence model can learn unseen tasks through few-shot learning. It proposes a simple but effective self-improvement process. Additionally, it shows that predicting both the next action and the hindsight image after executing that action can enhance performance. Building upon RT-1, RoboAgent (Bharadhwaj et al. (2023)) enhances model generalization and stability through data augmentation and action-chunking. MOO (Stone et al. (2023)) leverages Owl-ViT to extract object locations from observation images, enhancing RT-1’s openset detection capability. 

As for multi-task reinforcement learning. PI-QT-Opt (Lee et al. (2023)) leverages a large-scale, multi-task dataset and employs a model-free off-policy reinforcement learning approach for training. Q-Transformer (Chebotar et al. (2023)) facilitates training high-capacity sequential architectures on mixed-quality data by applying transformer models to RL. 

Utilizing pre-trained VLMs (Zhang et al. (2024b)) for fine-tuning to construct RFMs is considered efficient. RT-2 (Brohan et al. (2023)) collects manipulation trajectory data and fine-tunes manipulation datasets using VLM models like PaLI-X (Chen et al. (2023b)) and PaLM-E (Driess et al. (2023)) after treating pose as tokens. However, democratizing such an expensive framework for all robotics practitioners proves challenging as it relies on private models and necessitates extensive co-fine-tuning on vision-language data to fully exhibit effectiveness. Consequently, there is an urgent need within robot communities for a low-cost alternative solution, hence RoboFlamingo (Li et al. (2023d)) and OpenVLA (Kim et al. (2024)) emerge, effectively enabling a robot manipulation policy with VLMs. 

However, this approach necessitates a lot of data for the hidden layers to learn parameters related to the robot body, objects, and environment. Open X-Embodiment (Padalkar et al. (2023b)) assembles a dataset from 22 different robots, demonstrating 527 skills (160266 tasks). However, the current Open X-Embodiment dataset faces the heterogeneity dataset challenge. Octo (Team et al. (2024)) and HPT (Wang et al. (2024d)) propose multi-module networks to address this issue. RDT-1B (Liu et al. (2024d)) and PI (Black et al. (2024)) propose unified action space to address this issue. The Open X-Embodiment dataset lacks in-the-wild scenes. DROID (Khazatsky et al. (2024)) introduces an “in-the-wild” robot manipulation dataset. It contains 76k trajectories, or 350 hours of interaction data. This data is collected from 564 scenes, 86 tasks, and 52 buildings over 12 months. 

Internet videos contain information on the physics and dynamics of the world, some studies have explored training foundation models using both video datasets and 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

15 


**Figure 7.** Foundation Models for Policy. VLAC integrates task instruction, pre-written APIs, and example inputs into LLM. It generates corresponding execution code (Liang et al. (2023); Yoshida et al. (2025)). 2) VLAKP without foundation models training inputs task instruction into LLM, which specifies the manipulated object. The observation image is fed into VFM for object segmentation or keypoints, and both the manipulated object and object feature images are input into VLM, outputting the pixel mapping of the object to be manipulated into cartesian 3D key pose (Huang et al. (2023b)) or relational keypoint constraints (Huang et al. (2024a)). 3) VLAKP with training uses LLM to extract tokens from Task Instructions. VFM or VLM extract features from Multi-View Images and generate 3D features through 3D Lift. Finally, these features, along with proprioception, are used as input to the Diffusion Model to generate the key pose (Ke et al. (2024)). 4) VLADP with training (Single-System) outputs dense pose and the hindsight image by inputting task instruction and observation into a pre-trained model after training (Black et al.). The difference between VLADP and VLAKP with training lies in generating dense poses directly through policies, allowing for conversion into trajectory through time sequences, offering a more end-to-end approach compared to key pose. Key pose often requires subsequent motion planning. Outputting dense pose resembles more closely the paradigm of human task execution, as it does not require camera and spatial calibration or robot body configuration. However, it still necessitates extensive data training to embed the parameters of robot execution in the policy model’s hidden layer. As for imagining after the next movement, predicting both the next action and the hindsight image can improve the performance (Bousmalis et al. (2023)). 5) The VLADP with training (Double-System) generates dense pose by using models with different inference frequencies (Figure.ai (2025)). This method can effectively leverage prior knowledge from VLM and improve inference frequency. 6)Foundation Models assisting for Reinforment Learning. LLM generates subgoals based on task instruction to transform long-horizon tasks into short-horizon ones (Di Palo et al. (2023)), facilitating RL learning. LLM also creates a reward function for RL according to task instruction (Ma et al. (2023b)), while VLM can utilize prior knowledge to provide predicted action and sparse/dense reward, enhancing the effective exploration in reinforcement learning.(Ye et al. (2023a)). 

**Table 1. Strengths and Limitations of VLAC, VLAKP, and VLADP** 

|**Policy**|**Strengths**|**Limitations**|
|---|---|---|
|**VLAC**|• There are many Internet code datasets available. These can serve as<br>priors for code generation. This helps improve the generalization of<br>VLAC-style methods (Liang et al.(2023)).<br>• VLAC facilitates human attention to fine-grained details, enhancing<br>the debugging process.<br>• VLAC is able to generate more creative actions, as shown inYoshida<br>et al.(2025).<br>|• The use of third-party libraries in VLAC can constrain the<br>extensibility of policy tasks.<br>• Syntax errors and similar simple faults tend to appear frequently..<br>|
|**VLAKP**<br>**VLADP**|<br>• Compared to VLADP, VLAKP has a key advantage. It can leverage<br>rich prior knowledge from foundation models in CV and NLP. This<br>supports object-centric and action-centric action generation. As a<br>result, VLAKP requires less training data and generalizes better than<br>VLADP (Ke et al.(2024)).<br>• VLAKP improves upon VLAC by replacing sequential chaining with<br>spatial composition under joint optimization. This flexibility supports<br>more diverse manipulation tasks and ensures more stable execution<br>(Huang et al.(2023c)).<br>• Compared with VLAKP, it does not require calibration or motion<br>planning.<br>• It is more end-to-end, making it easier to transfer learned priors to<br>other tasks.<br>• Compared with other methods, VLADP has a smaller data annotation<br>burden.|• Mostly relies on 3D inputs, sensitive to pose errors. Requires precise<br>scene reconstruction and calibration.<br>• VLAKP often requires motion planning. However, motion planning<br>is not always reliable.<br>• It relies on large-scale training data, but faces data scarcity issues.<br>• It typically has a large number of parameters, requiring significant<br>computational resources and leading to high latency.<br>• It shows poor generalization across different embodiments.|


_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

16 

manipulation data. SuSIE (Black et al. (2023)) uses an image-editing diffusion model. This model is fine-tuned on human videos and robot rollouts. It acts as a high-level planner by proposing intermediate subgoals. These subgoals can be accomplished by a low-level controller. The two training steps of SuSIE do not share weights. GR-1 (Wu et al. (2023a)) is initially trained on a large-scale video dataset for video prediction, and then seamlessly fine-tuned with manipulation data. GR-2 (Cheang et al. (2024)) uses VQGAN to convert each image into discrete tokens and is trained with a larger text-video dataset than GR-1. LAPA (Ye et al. (2024)) begins by extracting the latent delta action between video frames. It then labels the video dataset with this information. These labeled datasets are used to train a VLM network. Finally, a small-scale robot manipulation dataset is applied for fine-tuning, enabling the mapping of latent actions to robot actions. Go-1 (Bu et al. (2025)) trains latent actions using human videos and combines those with manipulation data. Then, it trains the VLA on the merged dataset to boost the model’s generalization. 

Previous studies, such as GR-1 (Wu et al. (2023a)) and GR-2 (Cheang et al. (2024)), train the policy head using MSE regression. In contrast, OpenVLA (Kim et al. (2024)) and RT-2 (Brohan et al. (2023)) apply next-token prediction for their policy head. Building on the success of diffusion policy (Chi et al. (2023)), PI0 (Black et al.) and TinyVLA (Wen et al. (2024b)) adopt diffusion head as its policy head, achieving better performance than OpenVLA. In order to address higher degree of multi-modality in the distribution of feasible actions for bimanual manipulation, RDT-1B (Liu et al. (2024d)) utilizes Diffusion Transformers (DiTs) as its scalable backbone network. 

Although the diffusion policy can represent complex continuous action distributions, OpenVLA-OFT (Kim et al. (2025)) has shown in dual-arm tasks that fine-tuning the VLA with an L1 regression objective achieves performance similar to diffusion-based fine-tuning. However, it offers faster training convergence and inference speed. FAST (Pertsch et al. (2025)) proposes a new compression-based tokenization scheme for next-token prediction. This method matches the performance of diffusion VLAs, while reducing training time by up to 5x across multiple dexterous manipulation tasks. 

Previous methods face a basic tradeoff: VLM backbones are general but slow, while robot visuomotor policies are fast but not general. Synchronizing both does not improve inference speed. Helix (Figure.ai (2025)) and Groot N1 (Bjorck et al. (2025)) overcome this tradeoff with two asynchronous complementary systems, trained end-to-end to communicate. However, Groot N1 makes more use of human video latent action and simulated data compared to Helix. 

## _7.4 Foundation Models assisting for Reinforcement Learning_ 

Reinforcement learning has garnered widespread attention from researchers due to its ability to explore the environment by not requiring extensive annotated data. However, it also faces numerous challenges, such as dealing with longhorizon sequences, effectively exploring, reusing experience data, and designing reward functions (Kober et al. (2013)). 

Foundation models have demonstrated the emergence of common sense reasoning, the ability to sequence sub-goals and visual understanding. Due to the strong capability of foundation models, many studies aim to leverage the unprecedented capability of foundation models to address the challenges faced by reinforcement learning. RobotGPT (Jin et al. (2024)) aims to distill the knowledge of the brain ChatGPT into the mind of a small brain trained with reinforcement learning. At the same time, many studies explore the use of foundation models to solve challenges like long-horizon problems and effectively exploring and designing reward functions. 

Norman (Di Palo et al. (2023)) employs LLMs to decompose tasks into subgoals and utilizes CLIP to identify the completion of each subgoal, serving as a signal generator for sparse rewards. ROBOFUME (Yang et al. (2024a)) employs a fine-tuned VLM as the sparse reward function for the RL algorithm, tackling the issue of the extensive human supervision needed for training or fine-tuning a policy in the real world. Eureka (Ma et al. (2023b)) utilizes LLM to craft a reward function for five-fingered hand pen spinning. Subsequently, it engages in a cyclic process encompassing reward sampling, GPU-accelerated reward evaluation, and reward reflection to progressively refine its reward outputs. In contrast to Eureka’s self-iteration and sparse reward function design, TEXT2REWARD (Xie et al. (2023a)) incorporates human feedback into the iterative updating of the reward function, yielding a dense reward function. FAC (Ye et al. (2023a)) proposes using knowledge from foundation models as policy prior knowledge to improve sampling action efficiency, as value prior knowledge to measure the values of states and as success-reward prior knowledge to provide final feedback on task success. 

## _Summary_ 

According to Fig. 7, policies can be classified into VLAC, VLAKP, VLADP, and Foundation Models assisting for Reinforcement Learning. As shown in Appendix.A Tab. 4 and Tab. 5, comparison with baseline approaches reveals key distinctions. The strengths and limitations of VLAC, VLAKP, and VLADP are as described in Tab. 1. 

## **8 Manipulation Data Generation** 

Demonstration data plays a crucial role in robotic manipulation, particularly in the context of imitation learning (Padalkar et al. (2023b)). A common approach for gathering such demonstrations is human teleoperation in the real world. However, collecting real-world data often requires significant human labor and specialized teleoperation equipment. Recently, there has been a growing number of excellent developments in low-cost teleoperation hardware, which enables the collection of high-quality demonstration data (Fang et al. (2024); Cheng et al. (2024)). 

To collect data in real environments, human effort is required for scene setup and data annotation (Sermanet et al. (2023)). There are currently two methods for data collection: the bottom-up approach and the top-down step-by-step approach. The bottom-up approach focuses on selecting a task to perform based on the current scene. Then, it uses methods like crowd-sourcing to label the data. The top-down 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

17 

approach involves a step-by-step process where decisionmakers assign task labels and manage overheads, such as resets and scene preparations (Sermanet et al. (2023)). The robot then performs tasks according to these labels. RoboVQA (Sermanet et al. (2023)) shows that the bottom-up approach is more efficient in data collection compared to the top-down step-by-step approach. DIAL (Xiao et al. (2022a)) uses a fine-tuned CLIP to replace humans in labeling robot trajectories during bottom-up data collection. This transforms the robot manipulation dataset on the internet into the robot-language manipulation dataset. PAFF (Ge et al. (2023)) points out that incorrect robot trajectories can be linked to new tasks and uses fine-tuned CLIP to label the incorrect robot trajectories with appropriate task labels. The above methods demonstrate that high-level cognitive models can assist in data annotation. SOAR (Zhou et al. (2024b)) shows that integrating a high-level cognitive model with a low-level control policy can result in a fully autonomous data-collection system in varied real-world environments. 

Generating lots of data in simulation is a cheaper solution. However, it still requires human effort to create both scene generation and task execution code for specific tasks (Wang et al. (2023c)). Moreover, the notorious sim-to-real gap issue remains a challenge in transferring policies trained in simulation to real-world applications. But there are many methods to address the sim-to-real challenge. Matas et al. (2018) trains the policy fully in simulation through domain randomization and then successfully deployed in the real world, even though it has never encountered real deformable objects. Therefore, simulation plays an important role in manipulation and this section will analyze existing simulators, scene generation, demonstration generation and sim-to-real gap challenge. 

Compared to single-frame images and language data on the internet, internet videos contain information on the physics and dynamics of the world, as well as on human behaviors and actions (Chandrasegaran et al. (2024)). This information is precisely what is required for manipulation tasks. Therefore, in this section, we also introduce the internet-scale video data for robot learning. 

Regardless of whether it’s in a real or simulated environment, improving the efficiency of the existing dataset is essential. The mainstream approach is dataset augmentation. 

## _8.1 Low-cost Teleoperation Device_ 

The current low-cost teleoperation can be categorized into two types: online teleoperation and offline teleoperation. The distinction is similar to the difference between SLAM and SFM. Online teleoperation is a closed-loop interaction between a demonstrator and a robot (Darvish et al. (2023)). In the forward process, human motion is measured using devices that combine various sensors, such as vision, IMUs, or multi-joint encoders. The motion data from the demonstrator is then retargeted to the robot’s space. This allows the robot to accurately follow the demonstrator’s demonstrated trajectory. During the backward process, sensor data from the robot, such as forces, torques, and tactile information, should be retargeted to the demonstrator’s space. As a result, the demonstrator can experience an immersive teleoperation environment by sensor data 

feedback. At the same time, the synchronization and real-time performance between the forward and backward processes are also crucial (Darvish et al. (2023)). Offline teleoperation remove the reliance on real robots during data collection compared to online teleoperation (Chi et al. (2024)). Demonstrators directly perform tasks using handheld or wearable devices (Fang et al. (2024); Chi et al. (2024); Wang et al. (2024c)) or using cameras to record the task execution process (Shaw et al. (2023)). They do not need to supervise real robots to complete the tasks and operate tasks using human’s direct view perspective. Therefore, offline teleoperation lacks the backward feedback process. Without relying on real robots, the devices become more portable and intuitive. However, this increases the precision requirements for the retargeting algorithm. 

The differences among current low-cost teleoperation devices lie primarily in two aspects. One is human motion measurement on both online teleoperation and offline teleoperation. The other is visual feedback on online teleoperation. Human motion measurement component can be broadly categorized into two classes: one aimed at capturing and mapping the pose of end-effectors (Cheng et al. (2024); Liu et al. (2022a); Fu et al. (2024); Chi et al. (2024); Li et al. (2020)), and one exploited devices for joint copy (Zhao et al. (2023a); Wu et al. (2023c); Fang et al. (2024)). Visual feedback can be generally classified into two types third-person view and first-person view (Cheng et al. (2024)). The third-person view shows the demonstrator from an external position, offering a broader perspective of surroundings. In contrast, the first-person view mimics the robot’s perspective, providing an immersive and realistic experience such as teleoperation with VR/AR headset. 

For approaches capturing and mapping the pose of endeffectors, the common low-cost capturing devices include SpaceMouse (Liu et al. (2022a); Zhu et al. (2023b)), cameras (Cheng et al. (2024); Fu et al. (2024); Iyer et al. (2024); Shaw et al. (2023); Li et al. (2019); Fang et al. (2020a)), VR controllers (De Pace et al. (2021); Nakanishi et al. (2020)) and IMU sensors (Chi et al. (2024); Li et al. (2020); Fang et al. (2017a,b)). The SpaceMouse based method passes the position and orientation of the SpaceMouse as action commands of end-effectors. This method is lowcost, easy operation, and easy implementation, but it is not suitable for dual-arm operations. In contrast, methods based on cameras and VR are well suited for bimanual teleoperation and VR offers the advantage of visual feedback compared to cameras. However, teleoperation methods based on cameras and VR heavily relies on the accuracy of pose estimation algorithms and often affected by occlusion (Fu et al. (2024); Pavlakos et al. (2024); Iyer et al. (2024); Cheng et al. (2024)). The main advantage of teleoperation devices based on IMU sensors lies in their wearability (Li et al. (2020); Chi et al. (2024); Wang et al. (2024c)). Due to this advantage, UMI (Chi et al. (2024)) and DexCap (Wang et al. (2024c)) develope wearable devices capable of in-the-wild teleoperation and offline data collection. 

Above systems work in cartesian space, which needs inverse kinematic (IK) solver and off-the-shelf IK often suffering from fails when operating near singularities of the robot. Although some bilateral teleoperation systems use haptic feedback to provide a tangible sense of the 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

18 

**Table 2. Representative Low-cost Hardware Works.** 

|**Teleoperation Device**|**Teleoperation Type**|**Human Motion Measurement**|**Feedback**|**Cost**|**Embodiment Config**|**Manipulation Task**<br>|
|---|---|---|---|---|---|---|
|||||||Slide Ziploc;|
|Aloha(Zhao et al.(2023a))|Online Teleoperation|Joint Copy|Third-person View|$2000(include robot)|Dual-Arm; 2F Gripper|Slot Battery;<br>Open Cup; etc;<br>|
|||||||Place Hat on Rack;|
|GELLO(Wu et al.(2023c))|Online Teleoperation|Joint copy|Third-person View|$300|Dual-Arm; 2F Gripper|Hand Over;<br>Fold Towel; etc;|
|||||||Wear Shoe and Walk;|
|Human Plus(Fu et al.(2024))|Online Teleoperation|End-effectors mapping|Third-person View|$30(A RGB Camera)|Humanoid Robot; Dexterous Hand|Fold Clothes;<br>Warehouse; etc;|
|Transteleop(Li et al.(2020))|Online Teleoperation|End-effectors mapping|Third-person View|$170|Dual-Arm; Dexteours Hand|Pick-Place;<br>Handover; Push; etc;|
|OPEN TEACH(Iyer et al.(2024))|Online Teleoperation|End-effectors mapping|First-person View|$500|Dual-Arm; Dexteours Hand/2F Gripper;|Make Sandwich;<br>Ironing Cloth; Open Cabinet; etc;|
|||||||Can Sorting;<br>|
|Open-TeleVision(Cheng et al.(2024))|Online Teleoperation|End-effectors mapping|First-person View|$3499|Humanoid Robot; Dexteours Hand|Can Insertion;<br>Folding;<br>Unloading|
|AirExo (Fang et al.(2024))|Offline Teleoperation|Joint copy|-|$600|Dual-Arm; 2F Gripper|Gather Balls;<br>Grasp from the Curtained Shelf;|
|UMI(Chi et al.(2024))|Offline Teleoperation|End-effectors mapping|-|$371|Dual-Arm; 2F Gripper|Dish Washing;<br>Dynamic Tossing; Cloth Folding; etc;|
|DexCap(Wang et al.(2024c))|Offline Teleoperation|End-effectors mapping|-|$4000|Dual-Arm; Dexterous Hand|Scissor Cutting;<br>Tea Preparing; Sponge Picking; etc;|
|VideoDex(Shaw et al.(2023))|Offline Teleoperation|End-effectors mapping|-|-|Single-Arm; Dexterous Hand|Pick-Place;<br>Cover and Uncover;etc;|


robot’s kinematic constraints, they do not address the challenges of very tight operational spaces (Silva et al. (2009)). Therefore, multi-joint encoder teleoperation devices can solve the IK problem by working in the joint space. The current design of multi-joint teleoperation devices is mainly divided into isomorphic and non-isomorphic devices (Wu et al. (2023c)). Isomorphic devices refer to teleoperation systems using standard servo-based robotic arms to control manipulators with similar size and kinematics (Zhao et al. (2023a)), while non-isomorphic devices use such arms to control manipulators with different size and kinematic properties. Non-isomorphic devices use kinematically equivalent structures based on DH parameters to map joint spaces between different properties (Wu et al. (2023c)). AirExo (Fang et al. (2024)) expands this low-cost and scalable platform into a wearable device to collect cheap in-the-wild demonstrations at scale. 

As for teleoperation visual feedback, most of methods (Liu et al. (2022a); Zhu et al. (2023b); Fu et al. (2024); Li et al. (2020); Zhao et al. (2023a); Wu et al. (2023c)) are use third side view that observe the robot task with the operator’s own eyes directly. However, this observation involves some visual errors. For example, there may be inaccuracies in the distance between the gripper and the object being manipulated. While for first-person view, due to wearing VR head (Cheng et al. (2024); Iyer et al. (2024); De Pace et al. (2021); Nakanishi et al. (2020)), it allows operators to perceive the robot’s surroundings immersively. However, long time to use VR headset can lead to fatigue. 

To collect large-scale real-world manipulation data, teleoperation devices need trajectory following, intuitive, low-cost, portable and in-the-wild capabilities. In Tab. 2, we summarize several representative works on lowcost hardware teleoperation. For online teleoperation, it is important to ensure synchronization and real-time performance between the forward and backward processes and the backward process should provide forces and torques feedback, as well as tactile feedback. This is essential for dexterous hand manipulation tasks. For offline teleoperation, hardware development and retargeting algorithms are critical. Once these two aspects are well-executed, the offline teleoperation devices facilitate large-scale manipulation data collection from experts in specific industries. For instance, 

chefs can wear exoskeleton devices while cooking to gather relevant data. 

## _8.2 Simulator_ 

The current mainstream simulators (Zhou et al. (2023)) include PyBullet (Coumans and Bai (2016)), MuJoCo (Todorov et al. (2012)), CoppeliaSim (Rohmer et al. (2013)), NVIDIA Omniverse and Unity. Pybullet is easy to use and integrate, but its graphics are quite basic. It is not suitable for applications that require complex visual effects. Therefore, Pybullet is often used together with Blender (Shi et al. (2024)). Mujoco offers a high-precision physics engine. It is suitable for simulating articulated and deformable object manipulation. However, it has a high entry barrier for beginners. CoppeliaSim offers a wide range of ready-made environments, objects, and prototyping robotic systems for users. However, when dealing with many robots or complex scenes, CoppeliaSim may encounter performance issues. NVIDIA Omniverse provides realtime physics simulation and realistic rendering. However, it requires significant computational resources. NVIDIA Omniverse offers many interfaces. Users can use these to develop various applications. For example, Issac Gym is a platform for robot reinforcement learning, developed using Omniverse. Unity offers rich visual effects and a user-friendly interface. It allows for the creation of highly interactive applications. However, its physics engine is still not precise enough. The basic components of a simulator are the physics engine and the renderer. Improvements in these components can enhance the capability of sensors in simulations, such as optical tactile sensors (Chen et al. (2023d)). Learning-based simulators also show great potential. For example, Sora (Brooks et al. (2024)) and UniSim (Yang et al. (2023b)) use vast amounts of data from the internet to simulate the visual effects of many different actions. 

## _8.3 Scene and Demonstration Generation_ 

Simulation scenes can be created manually. However, this approach is time-consuming and labor-intensive. As a result, automated or semi-automated scene generation methods are more preferred (Deitke et al. (2022)). Two methods can be used. Real-to-Sim method converts real scenes 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

19 

to simulation. Automated generation method automatically generates simulation scenes without real-world observation. Real-to-Sim method can accurately mimic the real world, but it limits the diversity of scenes. The automated generation method can create more diverse scenes and increase the variety of collected demonstrations. 

The Real-to-Sim method directly refers to a digital twin. The Real-to-Sim method utilizes 3D-reconstruction technology (in Sec. 6) or inverse graphics (Chen et al. (2024c)) to create the real-world scene in a virtual environment (Torne et al. (2024)). But, 3D reconstruct scene is static environment where objects lack real-world physical properties, such as material, mass and friction coefficients, and are non-interactive (Torne et al. (2024)). The inverse graphics method, such as URDFormer (Chen et al. (2024c)), directly generates interactive simulation environment and articulated objects from input RGB image. Compared to 3Dreconstruction methods, it reduces human involvement and produces interactive simulation environment. However, it lacks physical plausibility and fails to address the mismatch between the generated object’s physical properties and the real world. 

As for the application of foundation models in Real-toSim methods, GRS (Zook et al. (2024)) employs SAM2 for object segmentation from RGBD image and utilizes VLMs to describe and match objects with simulation-ready assets. This approach combines the strengths of 3D-reconstruction and inverse graphics methods. It ensures the credibility of 3D-reconstruction methods and allowing objects in the scene to interact. However, it is impossible for the assert dataset to fully cover objects in the real world. Constructing an interact assert dataset often requires manual design by the creator or human-assisted interactive object generation. ACDC (Dai et al. (2024)) defines a digital cousin concept. Unlike a digital twin, it does not directly replicate a real-world counterpart. However, it retains similar geometric and semantic features by using similar asserts when the assert dataset does not include real-world objects. As for object pose, depth cameras are commonly used, but they struggle to capture reflective surfaces accurately. This limits their use in the wild. To address this issue, ACDC uses Depth-Anything-v2 (Yang et al. (2024b)), a state-of-the-art monocular depth estimation model, to estimate the depth map. 

Scene diversity primarily includes the diversity of scene layouts, such as floor plans and object placements, as well as the diversity of objects. The automated generation methods are more effective for producing large-scale diverse scenes. The automated generation methods can be categorized into rule-based and learning-based approaches. For instance, ProcTHOR (Deitke et al. (2022)) introduces a procedural generation pipeline for interactive scenes using rule-based constraints and statistical priors. However, the generated scenes often rely on pre-defined priors, resulting in unrealistic outcomes that hinder agent learning (Khanna et al. (2024)). To address this, PHYSCENE (Yang et al. (2024c)) incorporates physical collision avoidance, object layouts, interactivity, and reachability metrics into a diffusion model. This approach enhances the physical plausibility and interactivity of generated scenes. 

Due to the prior knowledge of foundation models, there are current efforts to use foundation models for scene 

construction. RoboGen (Wang et al. (2023e)) utilizes LLM to generate relevant assets, asset sizes, asset configuration, scene configuration based on the task proposals and use text-to-image-to-3D generation to create the corresponding assets. These assets are imported into the simulator to generate the appropriate scene. Finally, using VLM for task-specific scene verification. GenSim (Wang et al. (2023c)) uses LLMs to generate new task and task scenario codes based on the pre-cached scene codes in a task library. However, using foundation models to automate the generation of scene’s physical plausibility still relies on VLM for judgment. At the same time, the above research also uses LLMs to generate diverse instructions to ensure task diversity. However, generating diverse task instructions with LLMs presents challenges in ensuring rationality for the current environment. 

The Real-to-Sim method and the Automated generation method both rely on 3D assets. The diversity of 3D assets determines the variety of scenes (Nasiriany et al. (2024)). Although there are many existing 3D object assets (Chang et al. (2015); Deitke et al. (2023); Li et al. (2023a); Geng et al. (2023a); Xiang et al. (2020); Liu et al. (2022b); Calli et al. (2017)), their quantity is far from sufficient to cover the variety of real-world objects. As a result, many studies focus on the automatic generation of assets, such as zero-1to-3 (Wang et al. (2023e)), Luma.ai (Nasiriany et al. (2024)), LLaMA-Mesh (Wang et al. (2024e)), Trellis (Xiang et al. (2024)). However, the performance of generative models is also limited by the shortage of current 3D training data. To address this issue, data cleaning techniques or manual supervision are needed to filter and select high-quality generated object assets. 

The modeling of the interaction environment above primarily focuses on articulated object modeling. Articulated objects can be created manually by designers or generated using procedural (Jiang et al. (2022); Liu et al. (2023b); Zhang et al. (2023e)) or human-assisted interactive methods (Torne et al. (2024)) after 3D scanning. They can also be generated automatically through inverse graphics (Chen et al. (2024c)) or generative model (Xiang et al. (2024)). However, current automated methods for generating articulated object assets are limited to objects with few rotational joints. Real2Code (Mandi et al. (2024)) fine-tunes a CodeLlama model to process visual observation descriptions and then outputs joint predictions. This enables Real2Code to reconstruct complex articulated objects with up to 10 parts. At the same time, generative models mainly focus on rigid and articulated objects and research on deformable objects remains insufficient (Sundaresan et al. (2022)). 

To collect demonstrations in simulations, different approaches can be used based on task complexity. For simple tasks, like a two-finger gripper picking up a cube, a hard-coding method (Wang et al. (2022b)) can be used. However, for more complex tasks, remote teleoperation (Chen et al. (2024a)) or skill library (Ha et al. (2023)) should be employed. Building skill library can be done using reinforcement learning or gradient optimization methods. RoboGen (Wang et al. (2023e)) shows that gradientbased trajectory optimization is better for fine-grained manipulation tasks with soft bodies, like shaping dough into a specific form. On the other hand, reinforcement learning 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

20 

and evolutionary strategies are more effective for contactrich tasks and continuous interactions with other components in the scene. 

## _8.4 Sim-to-Real Gap Solutions_ 

The sim-to-real problem is a widespread issue across machine learning, not limited to manipulation (Zhao et al. (2020)). The goal is to successfully transfer the policy from the simulation (source domain) to the real world (target domain). The gap in the manipulation tasks between the simulation and the real-world includes two main types: visual gap and dynamic gap. Visual gap refers to the difference between the vision information produced by the renderer and the vision information in the real world. In terms of rendering realism, BEHAVIOR-1K (Li et al. (2023a)) highlights that Omniverse offers the highest rendering performance. The dynamic gap consists of several factors. First, there is a difference between the physics engine used in simulations and real-world physics. Second, the properties of objects, including robots, contribute to the object dynamic gap. Lastly, there is a control gap in robots, such as variations in static errors caused by different PID parameters. Currently, there are three main approaches to address sim-to-real gap: system identification, domain randomization, and transfer learning (Zhao et al. (2020)). 

Most of the system identification research (Kristinsson and Dumont (1992)) aims to create an accurate mathematical model of a physical system to make the simulator more realistic. However, it is impossible to accurately build models of complex environments in simulators. The primary methods for physical parameter identification include estimation from interaction (Seker and Kroemer (2024); Bohg et al. (2017); Xu et al. (2019)), estimation from demonstrations (Torne et al. (2024)), and estimation from observations using foundation models (Gao et al. (2023)). Among these, estimation from demonstrations appears more effective. Demonstrations inherently contain interaction information and can also assist policy training. However, improving the hardware performance for collecting demonstrations remains essential. 

Domain randomization (Ramos et al. (2019)) involves adding random disturbances to the parameters in simulation. This can include various elements, generally divided into visual and dynamic randomization. Visual randomization covers visual parameters like lighting, object textures, and camera positions. Dynamic randomization covers dynamic parameters like object sizes, surface friction coefficients, object masses, and actuator force gains. By experiencing diverse simulated environments, the policy can adapt to a broad range of real-world conditions. For the policy, the real world is essentially just another disturbed environment. However, parameter randomization requires human expertise. Ma et al. (2024) demonstrates that LLM excels in selecting randomized parameters and determining the randomization distribution. This makes domain randomization more automated. 

Transfer learning (Yu and Wang (2022); Tan et al. (2018)) involves using limited real-world data to adapt a policy trained on a abundant simulation data to the real world. Treat policies in the real-world and in the simulation as different tasks. We can use task transfer methods for transfer learning. For example, Rusu et al. (2017) uses the progressive 

network to apply knowledge from a policy trained in simulation to a new policy trained with limited real-world data, without losing the previous knowledge. Treat the policies in the real-world and in the simulation as the same task, even though the data distributions differ. We can use domain adaptation methods to address this issue. Three common methods for domain adaptation are discrepancybased (Lyu et al. (2024)), adversarial-based (Eysenbach et al. (2020)), and reconstruction-based methods (Bousmalis et al. (2016)). Discrepancy-based methods measure the feature distance between the source and target domains using predefined statistical metrics. This helps to align their feature spaces. Adversarial-based methods use a domain classifier to determine whether features come from the source or target domain. Once trained, the extractor can produce features that are invariant across both domains. Reconstruction-based methods also aim to find shared features between domains through setting up an auxiliary reconstruction task and using the shared features to recover the original input. 

The methods discussed above assume that the target domain remains unchanged. However, many physical parameters of the same robot can change significantly. Factors like temperature, humidity, positioning, and wear and tear over time can all affect these parameters. This makes it harder to bridge the sim-to-real gap. To address this issue, DORA (Zhang et al. (2024c)) uses an information bottleneck principle. It aims to maximize the mutual information between the dynamics encoding and environmental data. At the same time, it minimizes the mutual information between the dynamics encoding and the behavior policy actions. Transic (Jiang et al. (2024a)) proposes a data-driven approach that enables successful sim-to-real transfer using a human-in-the-loop framework. 

## _8.5 Internet-Scale Video Dataset_ 

Extensive and diverse video datasets are available from online repositories. The collection process requires querying and searching for videos with relevant content. After that, low-quality video data is removed through data cleansing. However, the raw video data cannot be directly transferred into the manipulation model due to the absence of (1) action or reward labels; (2) distribution shifts including physical embodiments, camera viewpoints, and environments. Although AVID (Smith et al. (2019)) and LbW (Xiong et al. (2021)) translate human action images from videos into robot action images, this type of translation remains limited to the pixel level; (3) essential low-level information like tactile feedback, force data, proprioceptive information, and depth perception (McCarthy et al. (2024)). However, these raw videos contain extensive visual information, such as objects, spatial information, human activities, and sequences of interactions between humans and objects (Eze and Crick (2024)). At the same time, language annotations are essential to support learning of semantic features in this visual information. 

Methods to obtain language annotations are divided into manual and automated captions. Manual captions are created by humans labeling video content. Automated captions include four types: (1) Automatic Speech Recognition (ASR), which converts audio in videos to text (Xue et al. (2022)). (2) Alt-text, which collects captions from 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

21 


**Figure 8.** Foundation Models for Manipulation Data Generation. Current mainstream simulators include Pybullet, MuJoCo, CoppeliaSim, NVIDIA Omniverse, and Unity. Meanwhile, learning-based generative models used as simulators have shown potential. Simulation environment generation can be classified into Real-to-Sim and Automated Generation methods. In the Real-to-Sim methods, assuming the object’s position is known, the main challenge lies in constructing the object’s 3D mesh. This can be achieved through scanning technique or by using VGM to generate the 3D mesh directly from RGB image (Chen et al. (2024c)). Additionally, GRS (Zook et al. (2024)) utilizes VLM to extract 3D object meshes corresponding to realworld object from assert database based on RGB image. In the Automated Generation methods, LLM can output scene descriptions or scene code based on task instruction. When the output is a scene description, VGM generates the objects and arranges them according to the description. Meanwhile, the generated scene need to be evaluated by VLM. (Wang et al. (2023e)). When the output is scene code, it directly generates the corresponding scene (Wang et al. (2023c)). However, this requires substantial prior knowledge of scene code within the task library. There are three methods for generating demonstrations in a scene: Hard-code, Teleoperation, and Skill Library. When building skill library, gradient optimization is effective in training skill for deformable tasks and reinforcement learning works better for contact-rich tasks (Wang et al. (2023e)). Solutions for the Sim-to-Real gap include System Identification, Domain Randomization, and Transfer Learning. For data augmentation, VFM is used to segment images first, and then VGM renders the object’s texture on the masked image. 

HTML alt-text attributes in web images and videos, like descriptions, tags, and titles (Bain et al. (2021)). (3) Transfer, which starts with a set of image-caption pairs. Then, captions are matched to video clips with similar frames (Nagrani et al. (2022)). (4) Foundation Models, which use pre-trained models to get captions. For example, VLMs provide single-frame image captions, while LLMs filter out inconsistent captions across frames (Blattmann et al. (2023)). Owing to recent advancements in language 

annotation techniques, most widely used internet video datasets incorporate language annotations, such as InternVid (Wang et al. (2023d)), HD-VILA-100M (Xue et al. (2022)), YT-Temporal-180M (Zellers et al. (2021)), WTS-70M (Shvetsova et al. (2025)), HowTo100M (Miech et al. (2019)), WebVid-10M (Nan et al. (2024)), and VideoCC3M (Yan et al. (2022)). At the same time, various off-the-shelf models can be used to annotate the current video with additional labels, such as pose (Shaw et al. (2023)), affordance (Mendonca et al. (2023)), key points trajectory (Wen et al. (2023b)), latent action (Ye et al. (2024)), mask and bounding boxes (Shan et al. (2020)). 

The task information contained in internet video data may not be highly relevant to the specific tasks performed by robots. Additionally, internet video data often suffers from issues such as missing action labels, low-level information, and distribution shifts. Therefore, manually recording custom videos can be an effective approach to collecting videos that are directly relevant to specific robot tasks or embodiments. This method can also help avoid the issue of re-annotating. By incorporating sensors such as IMUs, tactile sensors, and depth sensors during the recording process, manually recorded custom videos can exhibit lower noise compared to internet video data. However, the scale and diversity of manually recorded videos still cannot match the internet video data (McCarthy et al. (2024)). Currently, there are several commonly used manually recorded video datasets, such as Ego-4D (Grauman et al. (2022)), EgoExo-4D (Grauman et al. (2024)), RoboVQA (Sermanet et al. (2024)), Epic-Kitchens-100 (Damen et al. (2022)) and ActionSense (DelPreto et al. (2022)). 

## _8.6 Dataset Augmentation_ 

Current data augmentation can be mainly divided into scene-level and object-level. Scene-level refers to changing the layout of objects in the scene. For example, MimicGen (Mandlekar et al. (2023)) and DexMimicGen (Jiang et al. (2024c)) change the positions and orientations of objects, while CACTI (Mandi et al. (2022)) adds new, artificial objects to the scene. However, the reliability of data augmentation still needs validation. For example, MimicGen (Mandlekar et al. (2023)) filters data generation attempts based on task success. Current foundation models for dataset augmentation methods primarily operate at the object level. The main idea is to use semantic segmentation to extract masks for each object, and then employ generative rendering methods to alter the object’s texture. GenAug (Chen et al. (2023c)) leverages language prompts with a generative model to modify object textures and shapes, adding new distractors and background scenes. ROSIE (Yu et al. (2023)) localizes the augmentation region with an open vocabulary segmentation model and then runs image editor to perform text-guided image editing. 

## _Summary_ 

Following Fig. 8, LLMs can generate credible descriptions or code for task scenes. VGMs produce 3D object meshes and render textures. Nonetheless, the validity of the generated task scenes must be ultimately assessed by VLMs. For scene generation, Automated Generation Method 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

22 

ensures higher diversity than Real-to-Sim. The realism of simulation depends on the simulator. Omniverse provides the best rendering performance. 

## **9 Discussion** 

In this survey, we aim to outline the opportunities brought by foundation models for general manipulation. We believe the potential of embedding foundation models into manipulation tasks as a viable path towards achieving general manipulation. However, the primary applications of LLMs, VFMs, VLMs, LMMs and VGMs focus only on certain aspects of general manipulation capability, such as reasoning, perception, multimodal understanding, and data generation. The current framework for RFMs demands extensive data for learning, posing a crucial issue of constructing a data close-loop, and ensuring over a 99% success rate remains an unresolved concern. Therefore, this paper proposes a framework of robot learning for manipulation towards achieving general manipulation capability and detailing how foundation models can address challenges in each module of the framework. However, there are still many open questions in this survey. In this section, we delve into several open questions that we are particularly concerned about. 

## _9.1 What is the framework for general manipulation?_ 

_9.1.1 Definition of general manipulation._ The ultimate general manipulation framework should be able to interact with human or other agent and control whole-body to manipulate arbitrary objects in open-world scenarios and achieve diverse manipulation tasks. However, the interaction between robot and human involves not only recognizing intentions but also learning new skills or improving old skills from human experts in the external world. Openworld scenarios may be static or dynamic. Objects can be either rigid or deformable. Task objectives can vary from short-term to long-term. Furthermore, tasks may necessitate different degrees of precision with respect to contact points and applied forces/torques. We designate the restriction of the robot’s learning capability to improving old skills and to manipulating rigid objects in static scenes in order to achieve short-horizon task objectives with low precision requirements for contact points and forces/torques as Level 0 (L0), the current research has a high probability of achieving L0. However, safety and accuracy remain paramount concerns. 

_9.1.2 The design logic of the framework in this survey._ Based on the general manipulation definition and robot learning development history, this paper proposes a framework for a general manipulation capability. Given that the scenarios are static, the framework is designed in a modular, sequential manner. To facilitate module migration, it is preferable for each module to be plug-and-play. Given the current reliance on human-in-the-loop mechanisms in autonomous driving and medical robotics to ensure safety, this framework aims for human-robot interaction through corrective instruction to ensure the safety of manipulation 

actions. The corrective action can be collected into the dataset and then improve old skills through offline training. 

_9.1.3 The proposed framework limitations._ (1) The framework is designed with a sequential structure, which contrasts with the parallel execution in human operation. (2) Both the proposed framework and the surveyed literature are based on learning-based approaches. While modelbased methods may not generalize as well, they tend to significantly outperform learning-based methods in terms of success rates, precision and safety for specific tasks (Pang et al. (2023)). Therefore, investigating the integration of learning-based and model-based approaches remains an important research. (3) The framework proposed in this paper is based on the development of learning-based methods and the definition of general manipulation. The framework of brain-like cognitive research should also be explored. 

_9.1.4 Product implementation strategy._ During robot execution, continuous human supervision is not always feasible. Hence, integrating real-time monitoring through parallel surveillance videos during robot execution could enhance safety. The framework in this paper does not explicitly denote this parallel safety monitoring module, as it resembles the post-conditions detection module. The postconditions detection module analyzes the robot’s execution video to identify reasons for task failure, facilitating posthoc correction to ensure task success. If the algorithm’s task execution safety is 80%, and the monitoring module predicts safety at 80% as well, the probability of risky movements reduces to 4%. Of course, for household robots, ensuring an over 99% safety rate is imperative. Initially, cloud-based monitoring of multiple robots by a single operator, with human intervention to correct erroneous behaviors, appears to be the best approach. This strategy not only reduces labor requirements but also ensures safety. Later, by gathering extensive data to improve model accuracy. 

## _9.2 What kind of learning capability should a general manipulation framework possess?_ 

_9.2.1 The importance of learning ability._ As an intelligent robot for general manipulation, it is inevitable that one cannot learn all the skills of an open-world during offline development, hence possessing a certain learning capability is necessary (Wang et al. (2024b)). Within the framework of this paper, a module of corrective instruction is introduced, enabling the robot to rectify its actions. These corrective demonstrations are incorporated into the manipulation dataset and used to improve the policy offline through finetuning. However, this approach still focuses on learning old task skills and cannot acquire new ones. 

_9.2.2 Definition of learning ability._ The model of Policy should possess the capability of interactive, few-shot, continue, online learning to acquire a new skill and reinforce the policy’s mastery of the newly learned skill through corrective instruction offline. Interactive refers to the ability to learn through human demonstration or by observing instructional videos. Learning through demonstration often requires physical control or teleoperation, which is less natural. Learning through observation of instructional videos aligns better with human learning patterns. However, when 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

23 

humans learn from teachers, they often do not predict the teacher’s trajectory but rather understand the highlevel description of the actions, akin to VLaMP (Patel et al. (2023)). Few-shot continue learning enables the robot to learn new skills with minimal demonstrations without forgetting previously learned skills. Online learning entails processing observed data instantly and enabling the model to learn as quickly as possible. 

## _9.3 What foundation models bring for general manipulation?_ 

The emergence of foundation models can promote the progress of general manipulation. Meanwhile, for each section, we summarize the contributions of foundation models. As for Interaction, compared to traditional methods that use fixed questioning templates to eliminate instruction ambiguity, foundation models can provide the following for ambiguous instructions and corrective instructions: 1) more natural language communication, 2) multimodal perception to detect more types of ambiguity, and 3) powerful prior knowledge to better understand user intent. As for Object Affordance and Object Recognition in Pre- and Post-conditions Detection, foundation models bring several advantages. 1) They provide the perception capabilities for open-set affordance, detection, and segmentation, enabling zero-shot recognition of novel cases. 2) The powerful prior knowledge of foundation models accelerates the learning of tool affordance. 3) Foundation models assist methods in better understanding affordance and selecting more accurate poses. 

As for the hierarchy of skills: 1) Foundation models can assist in processing and interpreting natural language inputs. 2) The acquisition of world knowledge and commonsense reasoning by foundation models enhances their perception and reasoning abilities. This has the potential to improve the scalability and generalizability of tasks within the skill hierarchy. As for 3D Reconstruction and 6D Pose Estimation in State. 1) Foundation models assist in reconstructing scenes with semantic information. 2) Foundation models’ powerful 2D feature extraction ability can be applied to 3D lifting, aiding in the extraction of 3D features. 3) Foundation models enable open-set pose estimation. 

As for policy. 1) Foundation models can help the model follow instructions better. 2) Foundation models can enhance the model’s generalization ability and assist reinforcement learning. 3) Foundation models trained on large manipulation data can transfer prior knowledge to new task, such as PI0 transferring the mistake correction ability of pre-trained datasets to new task. As for manipulation data generation, the main contributions of foundation models are in simulation data and data augmentation. 1) Foundation models can generate 3D mesh assets in a zero-shot manner. 2) Foundation models help create diverse simulation scene layouts. 3) The vast priors of foundation models can be applied to data augmentation. 

## _9.4 How to use internet-scale video data for RFMs?_ 

As for what information from video dataset can be used, there are six main types of information to convert from 

video datasets: (1) Pose, such as capturing human hand poses and retargeting them to dexterous hand poses (Shaw et al. (2023); Qin et al. (2022)). (2) Affordance, including grasp locations on objects and post-grasp waypoints (Mendonca et al. (2023)). (3) Motion information, explicitly includes keypoints trajectories of objects and human hand during actions (Xiong et al. (2021); Yuan et al. (2024); Wen et al. (2023b)) and implicitly includes using VQ-VAE (Van Den Oord et al. (2017)) to generate a codebook for latent delta action (Ye et al. (2024)). (4) Environment transition dynamic information, such as predicting hindsight images after completing the current action (Wu et al. (2023a); Cheang et al. (2024); Yang et al. (2023b)). (5) Semantic information, such as descriptions of current task steps (Wang et al. (2024a)) and task instruction (Jain et al. (2024)). (6) Spatial and texture information, such as MVP (Radosavovic et al. (2023)) suggests using masked autoencoding (He et al. (2022)) for improving visual reconstruction. 

As for how to extract these useful information, various off-the-shelf models can be used to annotate the current video with additional labels, such as pose (Shaw et al. (2023)), affordance (Mendonca et al. (2023)), key points trajectory (Wen et al. (2023b)), latent action (Ye et al. (2024)), mask and bounding boxes (Shan et al. (2020)). When adding various labels to the video dataset, different training objectives can be used to extract features from the video dataset, such as MAE (Radosavovic et al. (2023)), contrastive learning (Ma et al. (2022)), time contrastive learning (Ma et al. (2023a)), temporal-difference learning (Bhateja et al. (2023)), video prediction objective(Du et al. (2024)), affordance prediction objective(Mendonca et al. (2023)), video-language alignment objective (Nair et al. (2022)), action motion objective(Yuan et al. (2024)) or combinations of these objectives (Karamcheti et al. (2023); Zhou et al. (2021)). 

As for how to utilize the extracted information to enhance or train robotic foundation models, the current robotic foundation models primarily use two learning methods: imitation learning and reinforcement learning. Therefore, the discussion on the third issue focuses on leveraging prior knowledge from video datasets in these two methods. As for imitation learning, when the robotic foundation model outputs pose and the video dataset annoated with pose label, the video dataset can be directly used as training data for the robotic foundation model (Shaw et al. (2023); Qin et al. (2022); Kareer et al. (2024)). When leveraging affordance information, motion information, environment transition dynamics information, semantic information, spatial and texture information, it is essential to employ GMM & CEM (Mendonca et al. (2023)), Inverse Dynamic Model (IDM) (Du et al. (2024); Ye et al. (2024); Wen et al. (2023b)), and Decoder (Wang et al. (2023a); Xiao et al. (2022b); Cheang et al. (2024); Wu et al. (2023a)) to transform these information into actions. Compared to other types of information, using semantic information treats the video as task instruction rather than observation (Jain et al. (2024); Shah et al. (2023); Jang et al. (2022)). At the same time, semantic information can also be used to organize tasks into a hierarchy of skills (Wang et al. (2024a)). 

As for reinforcement learning, the environment transition dynamics can be used as a transition model (Yang et al. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

24 

(2023b)). The encoder, trained on a video dataset with various objectives, can measure the distance between crossembodiment actions, which then serves as the reward function or value function (Bhateja et al. (2023)). For example, Guzey et al. (2024) and Xiong et al. (2021) use key points motion information to construct the encoder, which serves as the reward function for reinforcement learning. Since distribution shifts exist between cross-embodiment actions, AVID (Smith et al. (2019)) and LbW (Xiong et al. (2021)) translate human action images from videos into robot action images. However, this translation is limited to the pixel level. 

Current research focuses on different types of information in video datasets. The methods for extracting and using this information vary. It is important to consider which information from video datasets should be robustly applied to robotic foundation models. Video is similar to how humans perceive the world. Humans can improve their skills by watching experts. Similarly, using video datasets to construct a reinforcement learning from human feedback (RLHF) system in robotic foundation models is worth exploring (Luo et al. (2024)). 

## _9.5 How to uses foundation models for post-conditions detection and post-hoc correction?_ 

The current data collection mostly focuses on gathering successful task execution data, ignoring the collection of data related to failed task executions. However, if data on failed task executions are collected and annotated with corresponding error reasons, it would be possible to train a model to both determine task execution success and analyze the reasons for task execution failure. AHA (Duan et al. (2024)) trains a VLM to assess failures and output the reasons for these failures. However, the categories of failure modes are still limited, and it cannot output more open-ended failures, such as collaboration errors in dualarm tasks. Many current studies use internet video data to improve the generalization of policies. Exploring the use of internet video data to enhance post-condition detection and employing multimodal perception to more accurately identify the reasons for failures is a promising direction. Post-hoc correction could then generate corrective action sequences based on the reasons for task execution failure and the task objectives, which would be handed over to a policy to generate corresponding corrective actions. 

## _9.6 How to use foundation models for End-effector Design?_ 

Currently, there are two primary approaches to designing end-effector. The first approach customizes the end-effector for specific tasks. The second approach makes the multifingered end-effector resemble a human hand. The endeffector designed with the first approach is usually easier to control because it has fewer degrees of freedom compared to the end-effector designed with the second approach. In Billard and Kragic (2019), dexterity is divided into two types: extrinsic dexterity and intrinsic dexterity. Extrinsic dexterity involves using external support, such as friction, gravity, and contact surfaces, to compensate for the lack 

of degrees of freedom. Intrinsic dexterity refers to the hand’s ability to manipulate objects using its own degrees of freedom. Therefore, the first approach still has certain limitations for general manipulation. 

The first approach requires manual design, extensive testing, and continual adjustments. In Stella et al. (2023), LLMs are used for designing end-effector. However, this area is still in its early exploration stages. Using LLMs for end-effector design generates text descriptions, which still need to be manually translated into designs. This process is not fully automated. If we could develop modules for rotational and translational joints, and use something like protein structure prediction networks (Jumper et al. (2021)), training a foundation model to output graph including these joints could help reduce the challenges of manual design. As for the second approach, the human hand has many sensors and actuators. This makes it nearly impossible to design a robotic hand that closely resembles the human hand. Therefore, it’s essential to design the sensors and actuators carefully. 

## _9.7 How to use foundation models for dexterous manipulation?_ 

One major challenge in data collection for dexterous manipulation lies in gathering data from multi-fingered endeffectors. Although model-based hard code method (Zhu et al. (2024)) can collect data on dexterous manipulation, they still require data analysis such as mutual information (Hejna et al. (2025)) and entropy (Zhu et al. (2024)) to assess the quality of the data. Additionally, for multi-scenario and multi-task data collection, teleoperation methods are less dependent on algorithm performance compared to modelbased hard code methods. However online teleoperation requires a real-robot system, which is not portable and cannot achieve in-the-wild data collection. Therefore, current mainstream research focuses on directly tracking human hand motions during manipulation without controlling the real-robot (Wang et al. (2024c)). 

Two main learning-based methods for dexterous manipulation are imitation learning (Ze et al. (2024a)) and reinforcement learning (Ma et al. (2023b)). Imitation learning can use a visual encoder (in Sec. 6) for visuo-motor control. Diffusion policy (Chi et al. (2023)) adapts the concept of diffusion to visuo-motor control. It addresses challenges in visuo-motor control such as action multimodality, sequential correlation to accommodate high-dimensional action sequences. It can also use an existing RFMs for fine-tuning (in Sec. 7). Fine-tuning with a RFMs allows a skill to work in an open world. This often performs better on unseen objects compared to visuo-motor control (Brohan et al. (2023)). 

Reinforcement learning offers exploration capability, which address suboptimal issues. This advantage distinguishes it from imitation learning. However, reinforcement learning is primarily trained in simulation. It still has limitations in addressing the sim-to-real challenge of complex tasks, such as pen-spinning. In Sec. 7, the use of foundation models to assist reinforcement learning is introduced. FAC (Ye et al. (2023a)) offers potential for training reinforcement learning in real-world environment, but it still lacks consideration of environment resets (Gupta et al. (2021)) and safety. 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

25 

**Table 3. Representative Benchmarks.** 

|**Benchmark**<br>|**Assert Categories**<br>|**Assert Number**<br>|**Room Layout Number**<br>|**Task Number**<br>|**Long-horizon Task**|**Demonstration Instances**<br>**Simulator**<br><br>|
|---|---|---|---|---|---|---|
|RLBench (James et al.(2020))<br>|Rigid/Articulated/Deformable<br>|28<br>|Table-top<br>|100<br>|✓|90<br>CoppeliaSim<br>|
|Behavior-1K(Li et al.(2023a))<br>|Rigid/Articulated/Deformable<br>|9318<br>|50<br>|1000<br>|✓|-<br>Omniverse<br><br>|
|VirtualHome (Puig et al.(2018))<br>|Rigid/Articulated/Deformable<br>|1138<br>|50<br>|8014<br>|✓|5193<br>Unity<br><br>|
|RoboCasa (Nasiriany et al.(2024))<br>|Rigid/Articulated<br>|2509<br>|10<br>|100<br>|_×_|100K+<br>Mujoco<br><br>|
|LIBERO-1K(Liu et al.(2024a))<br>|Rigid/Articulated<br>|67<br>|Table-top<br>|130<br>|✓|6500<br>Mujoco<br>|
|Robosuite (Zhu et al.(2020))<br>|Rigid/Articulated<br>|20<br>|Table-top<br>|9<br>|_×_|-<br>Mujoco<br>|
|Sapien(Xiang et al.(2020))<br>|Rigid/Articulated<br>|2346<br>|Table-top|5<br>|_×_|-<br>Sapien(NVIDIA PhysX+OpenGL)<br><br>|
|Maniskill2 (Gu et al.(2023))<br>|Rigid/Articulated/Deformable<br>|2144<br>|-<br>|20<br>|_×_|30K+<br>Sapien<br><br>|
|CALVIN(Mees et al.(2022))|Rigid/Articulated|28|4|34|✓|40M<br>Pybullet|


Therefore, using foundation models to assist reinforcement learning in real-world training requires further exploration. 

Current learning methods each have their strengths and weaknesses (Zhang et al. (2024a)). Therefore, learning approaches for dexterous manipulation should integrate different methods. For example, diffusion policy can assist reinforcement learning in addressing high-dimensional action spaces issue, while reinforcement learning can help diffusion policy overcome issues with suboptimal and negative data. Additionally, the learning models should consider both inputs and outputs. The factors necessary for achieving dexterous manipulation are summarized in the Appendix.D. 

## _9.8 How to use foundation models for whole-body control?_ 

The above discussion primarily focuses on the contact between the end-effector and the object. However, wholebody control is still needed in dexterous manipulation. For example, in a polishing robot, force-position hybrid control of the robotic arm is often required to manage the trajectory of contact points and forces/torques. Mobile manipulation is essential for dexterous manipulation reachability. This idea is inspired by how humans handle objects. For example, when playing badminton, people use their waists, shoulders, elbows, and wrists together to hit the shuttlecock further. This aspect is often overlooked by current foundational models for manipulation. Although LEO (Huang et al. (2023a)) can provide poses for both navigation and manipulation, it still does not address the synchronization issue between the two. 

For whole-body control, the focus is on low-level control issues. A straightforward idea is to expand the action space of the policy model to include all joints of the robot. However, as the output dimensions increase, end-to-end training methods are more likely to diverge. Therefore, most current models output cartesian space poses and force/torques. These outputs are then optimized and converted into position or torque for each joint through a post-processing module (Haviland and Corke (2021)). To address end-to-end wholebody control issues, principal research is needed to facilitate network training and deployment. 

## _9.9 How to establish a benchmark?_ 

Current research on foundation models for manipulation focuses on various tasks, including interaction, hierarchical tasks, perception, detecting pre- and post-conditions, policy, and manipulation data generation. Therefore, a benchmark for foundation models for manipulation should include a comprehensive framework with diverse tasks. This framework should test individual tasks and tasks that involve connecting different modules. Since different simulators 

have unique physics engines and renderers, the benchmark should include standardized simulators and datasets. 

Tab. 4 lists the benchmarks used in current RFMs and we list some representative benchmarks in Tab. 3, highlighting a lack of standardization. This inconsistency hinders the development of RFMs for three main reasons. Firstly, current RFMs are tied to the specific parameters of each robot, such as the choice of sensors, camera pose, and the robot’s degrees of freedom. These factors prevent RFMs from being easily transferred across different robots. Secondly, testing the generalization and success rate of general manipulation capability requires a wide range of scenes and tasks. Thirdly, there is no standardized metric for assessing general manipulation capability. 

As for the RFMs are not transferable between different robots. The issue arises from focusing solely on testing RFM algorithms without considering hardware, which is an ineffective approach. General manipulation requires whole-body control. Thus, evaluating the generalization and success rate of RFMs should involve both algorithms and hardware, unlike in computer vision where only algorithms are considered. To address this, the simulation benchmark should include an easy interface for importing various robot hardware configurations. 

As for the requirment of a wide range of scenes and tasks. Although iGibson (Li et al. (2021)) and BEHAVIOR1K (Li et al. (2023a)) support simulating a variety of household tasks with high realism, they are still manually constructed. In Sec. 8, we discuss how foundation models can automate the generation of scenes and tasks. Using foundation models to create numerous scenes, combined with VLMs for accuracy checking and minimal human intervention, could be a valuable approach to explore. 

As for the metric for assessing general manipulation. The current evaluation standards mainly focus on success rates. However, in real-world applications, other metrics should also be considered. For instance, the system’s real-time performance is important. Most algorithms focus on building the generalization of skills. They often overlook the amount of data and speed required for RFMs to learn a new skill. Therefore, evaluation metric should also include the learning ability of RFMs. 

Overall, to assess the ability for general manipulation, methods used for testing medical robots can be referenced. Start with extensive testing in simulation environments, followed by limited tests in real-world settings. Continue evaluating the general manipulation capability during the product’s application phase. 

## **10 Conclusion** 

The impressive performance of foundation models in the fields of computer vision and natural language suggests the potential of embedding foundation models into manipulation 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

26 

tasks as a viable path toward achieving general manipulation capability. However, current research lacks consideration of a general manipulation framework. Thus, this paper proposes a general manipulation framework based on the development of robot learning for manipulation and the definition of general manipulation. It also describes the opportunities that foundation models bring to each module of the framework. 

We designate the restriction of the robot’s learning capability to improving old skills and to manipulating rigid objects in static scenes in order to achieve short-horizon task objectives with low precision requirements for contact points and forces/torques as Level 0 (L0), the current research has a high probability of achieving L0. 

Then, we discuss the following points: (1) the logic and implementation strategies of the designed framework, (2) the learning capability required for general manipulation, (3) what foundation models bring for general manipulation, (4) how to use internet-scale video data for RFMs, (5) how to uses foundation models for post-conditions detection and post-hoc correction, (6) how to use foundation models for end-effector design, (7) how to use foundation models for dexterous manipulation, (8) how to use foundation models for whole-body control, and (9) how to establish a benchmark. 

Additionally, the proposed framework has certain limitations: (1) The framework is designed with a sequential structure, which contrasts with the parallel execution in human operation. (2) Both the proposed framework and the surveyed literature are based on learning-based approaches. While model-based methods may not generalize as well, they tend to significantly outperform learning-based methods in terms of success rates, precision and safety for specific tasks (Pang et al. (2023)). Therefore, investigating the integration of learning-based and model-based approaches remains an important research. (3) The framework proposed in this paper is based on the development of learning-based methods and the definition of general manipulation. The framework of brain-like cognitive research should also be explored. 

Finally, foundation models present opportunities for each module of the framework, but many challenges still remain: 

1. **Interaction** Human interaction involves not only language but also gestures and actions. Incorporating multimodal inputs into interaction modules can enhance recognition capability. 

2. **Hierarchical of skills** The hierarchy of skills still has many unconsidered factors, such as achieving tasks in the shortest time with the highest efficiency, and how to generate strategies for dynamic scenes. 

3. **Pre- and post-conditions detection** Current research on post-condition detection primarily focuses on detection after robot execution. However, this delay is unacceptable. Therefore, it is necessary to implement failure detection and analysis of failure reasons during the robot execution. 

4. **State** The representation of state requires integration of multiple modalities, such as touch and hearing. Additionally, it’s important to consider the opportunities that foundation models can bring to active perception. 

5. **Policy** Current research on RFMs primarily involves fine-tuning VLMs. This approach deprives RFMs of the ability to self-explore. The extensive parameters of RFMs require significant computational resources for training and real-time reference, and model training also needs abundant data. Additionally, there is a lack of a unified benchmark for evaluating different RFMs. 

6. **Environment Transition Module** The foundation models inherently contain abundant physical priors. Applying foundation models to build a highly realistic physical model assist reinforcement learning training is a direction worth exploring. 

7. **Data Generation** The accuracy of data generated by LLMs and VGMs remains insufficient, necessitating appropriate check module and data cleaning algorithms. 

#### **Acknowledgements** 

The authors thank the editors and anonymous reviewers for the constructive feedback and in-depth review of this work. This paper pays tribute to the researchers and engineers who tirelessly advance the field of robotics — let’s change the world. 

#### **Declaration of conflicting interests** 

The author(s) declared no potential conflicts of interest with respect to the research, authorship, and/or publication of this article. 

#### **Funding** 

The author(s) disclosed receipt of the following financial support for the research, authorship, and/or publication of this article: This work was supported by the National Natural Science Foundation of China under Grants 62536001 and 62173197, and by the National Natural Science Foundation of China for Key International Collaboration under Grant 62120106005. 

# **Appendix.A Analysis of Policy Work** 

As shown in Tab. 4 and Tab. 5. The types of datasets currently used can be categorized into internet image-language pairs data, human video data, and robot demonstration data in real-world and simulation environments. RT-2 (Brohan et al. (2023)) demonstrates that co-training with internet imagelanguage pairs improves the model’s generalization. GR-1 (Wu et al. (2023a)), GR-2 (Cheang et al. (2024)), and LAPA (Ye et al. (2024)) show that training with human video data and robot demonstrations also enhances task generalization. GR-1 and GR-2 extract priors from human video data via image prediction, while LAPA uses latent-action for prior extraction. The advantages and disadvantages between these two methods are not clearly evident. 

The Input Modality shows that VLAKP primarily uses language and 3D representations as inputs, while VLADP relies on language, images, and proprioception. At the same time, adding a mask from the open-set visual module to the input improves the model’s generalization (Stone et al. (2023)). In terms of model architecture, VLAKP tends to use a 3D Feature Lift model combined with a Diffusion Model, while VLADP adopts a dual-system approach (slow and fast 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

27 

systems). This allows VLADP to effectively utilize the prior knowledge from VLM and enhance inference frequency. The current training objectives include next-token prediction, regression, diffusion, and TD learning in reinforcement learning. No research has conclusively shown which method is best. TD Learning in reinforcement learning can help robotic systems become more proficient than human teleoperators, exploiting the full potential of the hardware to perform tasks quickly, fluently, and reliably. It also enables robotic systems to improve autonomously through gathered experience, instead of relying solely on high-quality demonstrations. The Diffusion Objective can address action multi-modality issues and is widely applied in dexterous manipulation and high-dimensional action space tasks. Diffusion can be divided into Diffusion Policy-based and Flow Matching Policy-based approaches. Experiments in IMLE (Rana et al. (2025)) show that Diffusion Policy performs better than Flow Matching Policy. Fast (Pertsch et al. (2025)) introduces a compressionbased tokenization scheme that matches the performance of diffusion VLAs. OpenVLA-OFT (Kim et al. (2025)) shows that the regression train-objective outperforms nexttoken prediction and diffusion. Therefore, different data, architectures, and tasks require different training objectives. The specific situations corresponding to each train objective should be deeply researched. 

From the Output Modality, it can be seen that outputting the hindsight goal image along with the action improves model stability (Bousmalis et al. (2023); Cheang et al. (2024)). The Benchmark shows that current benchmarks vary across methods. A unified benchmark standard can promote progress in the field. Regarding Success Rate, there are few experiments testing adaptation ability. Adaptation ability refers not only to quickly adapting to new tasks but also to quickly adapting to new embodiment configurations. Crossembodiment learning can be divided into unified action space (Liu et al. (2024d); Black et al.) and changing the action head (Team et al. (2024); Wang et al. (2024d)). Currently, the comparison between these two methods for crossembodiment is not very clear. Regarding the manipulation task, it starts with single-arm pick-and-place tasks and evolves into dexterous manipulation using humanoid robot upper bodies. However, a considerable gap remains to achieve general dexterous manipulation. From the Failure Mode, it is observed that ”imprecise pose error” and ”wrong object error” occur most frequently. 

# **Appendix.B Comparative analysis of 2D and 3D-based methods.** 

As shown in Tab. 5, current methods utilize 2D observation or 3D observation. It is worth investigating which modality is more suitable for manipulation tasks. 

3D observation can be expressed in various forms. These include RGBD images, point clouds, voxels or multi-view images with camera extrinsic parameters (Ze et al. (2024b)). These 3D forms has not achieved large-scale adoption on the internet. As a result, the volume of 3D data remains significantly smaller than that of 2D images (Chen et al. (2024b)). Although SpatialVLM (Chen et al. (2024b)) uses off-the-shelf models to convert 2D images into 3D 

forms, the quality remains uncertain. Generating large-scale 3D observations in simulation environments might be an effective approach. However, there is still a sim-to-real gap. 

As for 2D and 3D representation learning, we have already introduced many pre-trained encoders for 2D representation in Sec. 4. For 3D representation encoders, the main options currently include PointNet++ (Qi et al. (2017)) and PointNext (Qian et al. (2022)). These encoders extract key features from point clouds. DP3 (Ze et al. (2024b)) introduces a holistic 1D embedding pooled from the 3D scene point cloud, which outperforms PointNet++ and PointNext. However, 3D Diffuser Actor (Ke et al. (2024)) shows that generating 3D representations by lifting features from perspective views to a 3D robot workspace, based on sensed depth and camera extrinsics, achieves even better results than DP3 (Ze et al. (2024b)). Additionally, converting 3D data into 2D allows the use of pre-trained 2D encoders that trained on large-scale datasets for feature extraction. Then, lifting 2D feature to 3D space. This method extracts texture features, spatial features and semantic features and become a notable trend in 3D representation. 

The current lift techniques can be categorized into three types: Direct Reconstruction, Feature Fusion, and Neural Field (Hong et al. (2023b)). Direct Reconstruction refers to features are mapped directly to the 3D space using camera extrinsics. However, this method is sensitive to noise in the camera pose. Feature Fusion combines 2D features into 3D maps using gradslam (Murthy Jatavallabhula et al. (2019)). This approach is more robust to camera pose noise. However, it requires depth map rendering from 3D data. Neural Field constructs 3D compact representation using a neural voxel field (Sun et al. (2022)). This method is more robust to noise in camera pose and does not require depth map renderings from 3D data. 

Current manipulation tasks are mainly divided into highlevel and low-level. High-level tasks involve decisionmaking, such as the hierarchy of skills. Low-level tasks focus on execution, like policies. For high-level manipulation task, 3D observation has stronger spatial reasoning capabilities compared to 2D observation (Chen et al. (2024b)). It can recognize quantitative relationships of physical objects, such as distances or size differences. For low-level manipulation task, ChainedDiffuser (Xian et al. (2023)) demonstrates that 3D methods are more stable than 2D methods under varying camera viewpoints. DP3 (Ze et al. (2024b)) has shown that diffusion policies with 3D input achieve higher success rates compared to 2D image and the point cloud format performs best. However, the comparison is based on a relatively small dataset. Lin et al. (2024a) introduces a scaling law for object diversity and environment diversity. However, it is still unclear whether 2D or 3D observation is more suitable for the scaling law. 

# **Appendix.C Analysis of Hierarchy of Skills** 

Regarding Tab. 6, it can be seen from the Foundation Models that current methods based on Video Instruction and Language Instruction have shifted from using the previous SOTA LLM to a stronger focus on utilizing the SOTA VLM. In terms of Manipulation Tasks and Horizon Steps, most current methods design tasks with a maximum length of 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

28 

about 10 steps. The comparison of Success Rate between Method and Baseline shows clear differences. Considering a robot’s abilities based on its embodiment, safety measures, action execution feedback, and enhanced scene grounding capability improves its task planning performance. The Failure Modes reveal that the main issues are Wrong Object Error, Plan Error, and Spatial Relations Error. This indicates that the key challenges in current task planning lie in perception and reasoning. 

# **Appendix.D Model-Based Methods for Dexterous Manipulation** 

Bicchi (2000) offers a thorough and widely accepted definition: dexterous manipulation is the capability of changing the position and orientation of the manipulated object from a given reference configuration to a different one, arbitrarily chosen within the hand workspace. Based on this definition, the dexterous manipulation can be described as: based on the designed end-effector, determining a sequence of contact points and the forces/torques to be exerted on the object, and control the whole-body to accomplish a specific task. 

Based on this definition, the challenges of dexterous manipulation lie in the design of the end-effector, determining a sequence of contact points and forces/torques, and whole-body control. The process of determining a sequence of contact points and forces/torques can be divided into model-based approach and the learningbased approach. The model-based approach is interpretable, explicitly showing the factors to consider in dexterous manipulation. Therefore, this section explains model-based approach. 

When solving simple tasks, contact points can remain fixed. However, for complex tasks, contact points need to change. Thus, a sequence of contact points and forces/torques is required, achieved through regrasping or finger gaiting. The sequence of contact points and forces/torques are positively correlated with the trajectory of the motion and wrench of the manipulated object. When the wrench and motion of the manipulated object at a given moment are determined, they can be mapped to the corresponding contact points and forces/torques between the end-effector and the manipulated object. Therefore, we will explain the pipeline of this mapping relationship for a specific moment. 

As shown in Figure 9, we use a simple process to explain the generation of a sequence of contact points and forces/torques. Assuming the motion trajectory of the object is already obtained, the target wrench can be calculated based on the object’s mass and inertia. Contact points can be optimized based on object geometry, object material, and end-effector geometry etc, using appropriate metrics (Ferrari et al. (1992)). Alternatively, they can be generated using a knowledge-based approach (Stansfield (1991)). Subsequently, a coordinate system is established at the centroid of the object. Based on the location of the contact points, the target wrench is converted into fingertip force. Finally, the force of the fingertip is converted into the forces/torques required by the actuators through hand jacobian (Okamura et al. (2000)). 


**Figure 9.** Model-based Generation of a Sequence of Contact Points and Forces/Torques. 


**Figure 10.** Non-smooth dynamic system. 

The pipeline contact points and forces/torques mentioned above are derived sequentially. In practical applications, both can be optimized simultaneously (Xu et al. (2024)). However, due to the discontinuities and mode changes inherent in contact dynamics, it creates challenges for planning in contact-rich manipulation (Pang (2023)). 

As shown in Fig. 10, _q_<sup>_a_</sup> and _µ_ represent the actual and commanded positions of the actuated ball, while _q_<sup>_u_</sup> represents an unactuated box that slides along a rail with sufficient damping. Our goal is to push the box by the ball to transition from the current configuration _q_<sup>_u_</sup> to the goal configuration _qgoal_<sup>_u_.Suppose</sup><sup>_q_</sup> +<sup>_u_isthesteady-stateposition</sup> of the box after the ball is commanded to position _µ_ . We expect that _q_ +<sup>_u_and</sup><sup>_q_</sup> _goal_<sup>_u_aresufficientlyclose.Typically,</sup> _q_ +<sup>_u_=</sup><sup>_f_(</sup><sup>_qu, qa, µ_)representsthesystem’sdynamic,which</sup> can be obtained through system identification (Suh et al. (2023)). 

As shown in Fig. 10, the gradient is non-smooth when the ball is either in contact with or separated from the box. This presents challenges for optimization-based problemsolving methods. Current approaches for smoothing contact dynamics are mainly divided into analytic smoothing and randomized smoothing (Pang et al. (2023)). However, it is often necessary to consider frictional contact constraints, which can make the optimization problem non-convex (Tedrake (2023); Le Lidec et al. (2024)). To address this issue, current methods primarily rely on Anitescu’s convex relaxation(Anitescu (2006); Pang et al. (2023); Jin (2024)) and Todorov’s model (Todorov et al. (2012); Todorov (2014)). At the same time, the contact dynamics also need to consider the robot’s joint limits constraint, the penetration constraint between the hand and the object, and 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

29 

the self-penetration constraint (Pang and Tedrake (2021); Xu et al. (2024)). Although smoothed dynamics on trajectory optimization, such as iMPC (Suh et al. (2022) and LQR (Shirai et al. (2024)) are considered effective, these methods are only suitable when the goal is close to the initial configuration. When the goal is farther from the initial configuration, a more global strategy is required. 

As shown in Fig. 10, there are two initial guesses: 1) the ball is on the left of the box, and 2) the ball is on the right of the box. Different initial guesses lead to different dynamic model. Choosing the wrong initial guess can prevent the optimization problem finding the optimal solution. To address this issue, the system dynamics need to be divided into contact modes, and a global strategy is required (Pang et al. (2023)). In Fig. 10, the ball and the box experience both contact and no contact. However, for a system with _n_ rigid bodies, there can be up to _Cn_<sup>2contact</sup> pairs. Each contact pair may have multiple contact modes, such as sticking/rolling, separation, and sliding, which can lead to an explosion of contact modes. Although Huang et al. (2021) considers kinematically feasible contact modes and reduces the number to _O_ ( _n_<sup>_d_2</sup><sup>_/_2+2</sup><sup>_._5</sup><sup>_d_</sup> )(where d is the number of degrees of freedom and n is the number of contact points), the reduced number of contact modes is still too large to handle. 

To address the above issues, current model-based techniques are mainly divided into contact-explicit and contact-implicit (Jiang et al. (2024b)). The contact-explicit approach in dexterous in-hand manipulation involves explicitly representing contacts, such as their locations, modes, and reaction forces (Cheng et al. (2023)). These representations form contact sequences, which are obtained through methods like enumerating (Aceituno-Cabezas and Rodriguez (2020); Hogan and Rodriguez (2020)), searching (Chen et al. (2021a); Zhu et al. (2023a); Cruciani et al. (2018)), sampling (Cheng et al. (2023)), or demonstration (Khadivar and Billard (2023)). However, these methods suffer from poor scalability (Pang et al. (2023)) and contacts easily fall into the local optimum (Jiang et al. (2024b)). The contact-implicit approach avoids the complexity of explicit contact representation. It uses methods like relaxed complementary constraints (Kim et al. (2023); Le Cleac’h et al. (2024)), smooth surrogate models (Pang et al. (2023); ¨Onol et al. (2019)), or direct control sampling (Howell et al. (2022)). However, the smoothing process introduces forceat-a-distance effects and sacrifices physical fidelity (Pang et al. (2023)). Although Jiang et al. (2024b) compensates for discrepancies between actual and planned contact modes using tactile feedback, this method assumes quasi-static contact model and struggles to handle highly dynamic actions, such as spinning a pen between fingers. 

From the above analysis, it is evident that choosing appropriate contact points and forces/torques requires considering the object’s geometry, mass, inertia, material, and friction parameters, as well as the end-effector’s geometry, material, and actuator capability. At the same time, the hybrid process between non-smooth contact modeling and planning faces significant challenges for contact-rich tasks. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

30 

**Table 4. Representative Policy Works in Sec. 7.** The policy type is consistent with VLAC, VLAKP, VLADP in Sec. 7. Current robot foundation model training recipes include From-Scratch and Pre-Train + Fine-Tune (Post-Train). Some methods use vision or language foundation models during training. However, these foundation models are not pre-trained on large manipulation datasets. So these methods are still considered From-Scratch( Shridhar et al. (2021)). Pre-Train refers to training on extensive manipulation datasets. Fine-Tune involves post-training a pre-trained model on a small task-specific manipulation dataset for a particular task. The datasets used in various stages are detailed in the ‘Dataset’. ‘Benchmark’ refers to the benchmark used in the experiment. The ‘Success Rate’ is categorized into Seen and Unseen. ‘Seen’ refers to test cases that have appeared in the training data, while ‘Unseen’ refers to test cases that have not been present in the training data. However, some studies do not clearly differentiate between Seen and Unseen cases, and in our analysis, we also do not make this distinction. Meanwhile, for the pre-train + fine-tune training recipe, the success rate is further divided into the out-of-box generalization ability of the pre-trained model and the adaptation ability of the fine-tuned model. We have also provided annotations on the success rates of both the out-of-box and fine-tuned models. Due to differences in benchmarks, solely estimating the success rate is meaningless. Therefore, we also include the success rates of the baseline for comparison. ‘Embodiment Config’ refers to the type of robot selected in the experiment. ‘Manipulation Task’ refers to the manipulation task designed for the experiment. ‘Failure Mode’ refers to the common failure cases of the method, as indicated in the paper. 

|**Method**|**Policy Type**|**From-Scratch**|**Dataset**<br>**Pre-Train**|**Fine-Tune**|**Benchmark**<br>|**Success**<br>**Seen**|**Rate**<br>**UnSeen**|**Embodiment Config**|**Manipulation Task**|**Failure Mode**<br>|
|---|---|---|---|---|---|---|---|---|---|---|
|Code as Policy (Liang et al.(2023))|VLAC|NA|NA|NA|CLIPort|Cap: 89.36%<br>CLIPort: 53.23%<br>|Cap: 71%<br>CLIPort: 0%<br>|Single-Arm<br>2F Gripper|Table-top Manipulation<br>(pick-place)|Code Generation Error ;<br>Imprecise Pose Error;<br>Wrong Object Error;|
|Instruct2Act (Huang et al.(2023b))|VLAKP|NA|NA|NA|VIMA|Instruct2A<br>Gato: 4<br>Flamingo|ct: 84.4%<br>0.8%<br>: 45.5%|Single-Arm<br>Varies tools|Table-top Manipulation<br>|Task Order Failure;|
|VoxPoser (Huang et al.(2023c))|VLAKP|NA|NA|NA|Self-Creation|VoxPoser: 76.9%<br>CaP: 46.5%|VoxPoser: 69.6%<br>CaP: 39.6%|Single-Arm<br>2F Gripper|Table-top Manipulation<br>(sweep; push; turn on;<br>open; pick-place)<br>P T|Motion Planning Error;<br>Imprecise Trajectory|
|ReKep (Huang et al.(2024a))|VLAKP|NA|NA|NA|Self-Creation|ReKep:<br>VoxPoser|44.3%<br>: 10.0%|Single-Arm;<br>Dual-Arm;<br>2F Gripper|our ea;<br>Recycle Can;<br>Stow Book;<br>Tape Box;<br>Fold Garment;<br>Pack Shoes;<br>Collab. Folding|Motion Planning Error;<br>Incorrect Keypoints|
|CLIPort (Shridhar et al.(2021))|VLAKP|1000 Demo. per Task<br>(Total 10 Tasks)|NA|NA|CLIPort|CLIPort: 87.7%|CLIPort: 57.1%|UR5e;<br>Suction Gripper.|Table-top Manipulation<br>(pick-up; sweep;<br>align rope; etc.)|Wrong Object Error;<br>Grasp Fail Error|
|PerAct (Shridhar et al.(2023))|VLAKP|100 Demo. per Task<br>(Total 18 Tasks)|NA|NA|RLBench|PerAct:|42.7%|Franka Panda;<br>2F Gripper|Table-top Manipulation<br>(pick-place; open-close;<br>sweep; screw; insert;)<br>|Grasp Fail Error|
|Act3D (Gervet et al.(2023))|VLAKP|100 Demo. per Task<br>(Total 18 Tasks)|NA|NA|RLBench|Act3D:<br>PerAct:|65%<br>42.7%|Franka Panda;<br>2F Gripper|Table-top Manipulation<br>(pick-place; open-close;<br>sweep; screw; insert;)<br>i i|Imprecise Pose Error|
|ChainedDiffuser (Xian et al.(2023))|VLAKP|100 Demo. per Task<br>(Total 10 Tasks)|NA|NA|Self-Creation|ChainedDiff<br>Act3D:|user: 80.9%<br>21%|Franka Panda;<br>2F Gripper|Contnuous Interactons<br>Manipulation Task<br>(unplug charger; wipe desk;<br>open-close; books on shelf)|Imprecise Pose Error|
|||||||RLBench(M<br>3D Diffuser A<br>Act3D:<br>PerAct:<br>RLBench(Si|ulti-View):<br>ctor: 81.3%<br>63.2%<br>49.4%<br>le-View):||||
|3D Diffuser Actor (Ke et al.(2024))|VLAKP|RLBench:<br>100 Demo. per Task<br>(Total 18 Tasks)<br>CALVIN:<br>Six Hours per Env<br>(Total 4 Envs)|NA|NA|RLBench;<br>CALVIN|3D Diffuser A<br>Act3D:<br>GNFactor<br>CALV<br>3D Diffuser A<br>GR-1:<br>SuSIE:<br>RoboFlamin<br>RT-1:<br>ChainedDiff|g<br>ctor: 78.4%<br>65.3%<br>: 31.7%<br>IN:<br>ctor: 66.96%<br>61.2%<br>53.8%<br>go: 49.5%<br>18%<br>user: 16.8%|Franka Panda;<br>2F Gripper|Table-top Manipulation<br>(pick-place; open-close;<br>sweep; screw; insert;<br>push; lift; turn on/off)|Intermediate<br>Task Fail Error|
|GNFactor (Ze et al.(2023))|VLAKP|20 Demo. per Task<br>(Total 10 Tasks)|NA|NA|RLBench|GNFactor: 31.7%<br>PerAct: 22.7%|GNFactor: 28.3%<br>PerAct: 18.0%|Franka Panda;<br>2F Gripper|Table-top Manipulation<br>(pick-place; open-close;<br>sweep; screw; insert; push)|NR|
|DNAct (Yan et al.(2024))|VLAKP|50 Demo. per Task<br>(Total 10 Tasks)|NA|NA|RLBench|DNAct: 59.6%<br>GNFactor: 43.3%<br>PerAct: 35.6%|DNAct: 52.3%<br>GNFactor: 30.9%<br>PerAct: 29.8%|Franka Panda;<br>2F Gripper|Table-top Manipulation<br>(pick-place; open-close;<br>sweep; screw; insert; push)<br>|NR|
|VoxAct-B (Liu et al.(2024b))|VLAKP|100 Demo. per Task<br>(Total 4 Tasks)|NA|NA|Self-Creation|VoxAct-<br>VoxPose<br>Act: 2<br>Diffusion P|B: 49%<br>r: 11%<br>7.6%<br>olicy: 8%|Dual-Arm;<br>2F Gripper|Asymmetric Bimanual<br>Manipulation<br>(open jar; open drawer;<br>put item in drawer;<br>handover)|Imprecise Pose Error;<br>Collisions;<br>Dual-Arm Collaboration Error;<br>Motion Planning Error|
|LEO (Huang et al.(2023a))|VLAKP|NA|100K Demo. per Task<br>(Total 3 Tasks)|NA|CLIPort|LEO: 87.2%<br>CLIPort: 91.1%|LEO: 63.4%<br>CLIPort: 59.6%|UR5e;<br>Suction Gripper<br>|Table-top Manipulation<br>(pick-place)<br>|NR|
|ManiFoundation ((Huang et al.(2023a)))|VLAKP|NA|200K Rigid, Clothes,<br>Deformation Data|NA|Self-Creation|ManiFounda|tion: 88.6%|Varies Single-Arm;<br>Varies 2F Gripper;<br>Varies Dexterous Hand|Rope Rearrangement;<br>Breakfast Preparation;<br>Cloth Folding<br>|NR|
|RT-1 (Brohan et al.(2022))|VLADP|NA|130K Demo.|NA|RT-1 Evaluation|RT-1: 97%<br>Gato: 65%|RT-1: 76%<br>Gato: 52%|Everyday Robots;<br>2F Gripper|Pick-Place;<br>Knock;<br>Open-Close|NR|
|Gato (Reed et al.(2022))|VLADP|NA|387K Simulation Demo.;<br>15.7K Real Robot Demo.|NA|Self-Creation|Gato: 7|5.6%|Sawyer Robot;<br>2F Gripper<br>|Stacking|NR|
|RoboCat (Bousmalis et al.(2023))|VLADP|NA|Internet Image Data;<br>Real Robot Data;<br>Simulation Data|1000 Demo|.<br>Self-Creation|Fine-t<br>RoboCat|une:<br>: 80.5%|Varies Single-Arm<br>(Sawyer; Panda; KUKA);<br>2F Gripper;<br>3F Dexterous Hand|<br>Stack;<br>Lift;<br>Insert|Imprecise Pose Error|
|RoboAgent (Bharadhwaj et al.(2023))|VLADP|NA|7500 Demo.|NA|Self-Creation|RoboAgent: 81.67%<br>RT-1: 22.5%<br>|RoboAgent: 48.25%<br>RT-1: 5.6%|Franka Panda;<br>2F Gripper|Making Tea;<br>Cleaning Up;<br>Serving Soup;<br>Baking Prep;<br>Stowing Bowl;<br>Heating Soup<br>|NR|
|MOO (Stone et al.(2023))|VLADP|NA|130K Demo.;<br>Augmented Data|NA|RT-1 Evaluation|MOO(111M): 98%<br>RT-1:_∼_99%|MOO(111M): 79%<br>RT-1:_∼_40%|Everyday Robot;<br>2F Gripper|Pick-Place;<br>Knock;<br>Open-Close|NR|


_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

31 

|**Method**|**Policy Type**<br>**F**|**rom-Scratch**|**Dataset**<br>**Pre-Train**<br>115000|**Fine-Tune**|**Benchmark**|**Success Rate**<br>**Seen**<br>**UnSeen**|**Embodiment Config**|**Manipulation Task**|**Failure Mode**|
|---|---|---|---|---|---|---|---|---|---|
|Q-Transformer (Chebotar et al.(2023))|VLADP|NA|Successful Demo.;<br>185000<br>Failed Episodes<br>|NA|RT-1 Evaluation|Q-Trans.: 56%<br>RT-1: 25%|Everyday Robot;<br>2F Gripper|Pick-Place;<br>Move;<br>Open-Close|NR|
|RT-2 (Brohan et al.(2023))|VLADP|NA|Internet<br>Image-Language<br>Pairs Data;<br>130K Demo.|NA|RT-1 Evaluation|RT-2:_∼_90%<br>RT-1:_∼_90%<br>RT-2: 62%<br>RT-1: 32%|Everyday Robot;<br>2F Gripper|Pick-Place;<br>Knock;<br>Open-Close|NR|
|OpenVLA (Kim et al.(2024))|VLADP|NA|970K Demo.<br>from Open-X;|50 Demo. per Task<br>(Total 10 Tasks)|BridgeData V2;<br>RT-1 Evaluation;<br>LIBERO|Out-of-Box:<br>OpenVLA: 88%;<br>RT-1X: 32.0%;<br>RT-2X: 72.0%;<br>Octo: 44.0%<br>Fine-tune:<br>Out-of-Box:<br>OpenVLA: 82.9%;<br>RT-1X: 34.3%;<br>RT-2X: 82.9%;<br>Octo: 14.3%<br>Fine-tune:|Single-Arm;<br>2F Gripper|Pick-Place;<br>Knock;<br>Open-Close;|NR|
|||||||OpenVLA: 83.7%;<br>Octo: 83.1%;<br>DP: 79.7%<br><br>OpenVLA: 53.7%;<br>Octo: 51.1%;<br>DP: 50.5%||Wipe Table||
|Octo (Team et al.(2024))|VLADP|NA|800K Demo.<br>From Open-X;|_∼_100 Demo. per Task<br>(Total 6 Tasks)|Self-Creation|Out-of-Box:<br>Octo:_∼_70%;<br>RT-1X:_∼_40%;<br>RT-2X:_∼_70%<br>Fine-tune:<br>Octo: 72%|Varies Single-Arm<br>(WidowX; BridgeV2; UR5);<br>Dual-Arm;<br>2F Gripper|Pick-Place;<br>Wipe a Table<br>with a Cloth;<br>Open-Close;<br>Handover;<br>Insert|Imprecise Pose Error|
|HPT (Wang et al.(2024d))|VLADP|NA|300K Demo.;<br>Simulation Data;<br>Human Video Data;|_∼_50 Traj.|Simpler|Fine-tune:<br>HPT: 46.7%;<br>Octo: 21.7%|Everyday Robot;<br>2F Gripper|Pick-Place;<br>Open-Close;<br>Sweep Leftover;<br>Fill Water;<br>Switch Insertion;<br>Scoop Food|Imprecise Pose Error|
|SuSIE (Black et al.(2023))|VLADP|NA|BridgeData V2<br>(60K Demo.);<br>Something-Something<br>(75K Video Clips)|NA|BridgeData V2;<br>CALVIN|SuSIE: 87%;<br>RT-2X: 43%;<br>MOO: 47%<br>SuSIE: 69%;<br>RT-2X: 37.5%;<br>MOO: 7.5%|Single-Arm;<br>2F Gripper|Pick-Place;<br>Fold Cloth;<br>Open-Close;<br>Sweep into Pile<br>|Grasp Fail Error;<br>Grasp Slip Error|
|GR-1 (Wu et al.(2023a))|VLADP|NA|Ego4D Video<br>(8M Frames);<br>20K Demo.|NA|Self-creation|GR-1: 84.2%;<br>RT-1: 48.9%<br>GR-1: 40.1%;<br>RT-1: 18%|Single-Arm;<br>2F Gripper|Pick-Place;<br>Open-Close;<br>Lift;<br>Turn on/off|Wrong Object Error|
|GR-2 (Cheang et al.(2024))|VLADP|NA|38M Text-Video Data;<br>40K Demo.|NA|Self-creation|GR-1:_∼_50%;<br>GR-2:_∼_80%<br>GR-1:_∼_20%;<br>GR-2:_∼_70%|Single-Arm;<br>2F Gripper|Pick-Place<br>|Wrong Object Error|
|LAPA (Ye et al.(2024))|VLADP|NA|3M Traj;<br>10K Demo.|NA|Self-creation|LAPA:50.1%;<br>OpenVLA:43.9%;|Franka Panda;<br>14 DOF bi-manual Robot|Pick-Place;<br>Knock Over;<br>Cover with Towel<br>|Imprecise Pose Error|
|PI0 (Black et al.)|VLADP|NA|Open-X;<br>PI Dataset;|5–100 Hours per Task<br>(Total 5 Tasks)|Self-creation|Out-of-Box:<br>PI0:_∼_90%;<br>OpenVLA:_∼_35%;<br>Fine-tune:<br>PI0:_∼_80%;<br>DP:_∼_30%|Single-Arm;<br>Dual-Arm;<br>Mobile-Manipulators|Laundry Folding;<br>Clearing a Table;<br>Putting Dishes<br>in a Microwave;<br>Stacking Eggs<br>into a Carton;<br>Assembling a Box;<br>Bagging Groceries|NR|
|RDT-1B (Liu et al.(2024d))|VLADP|NA|1M+ Demo.|6K+ Demo.|Self-creation|Fine-tune:<br>RDT-1B:_∼_70%;<br>ACT:_∼_10%;<br>OpenVLA:_∼_2%;<br>Octo: 2%|Mobile ALOHA|Wash Cup;<br>Pour Water;<br>Handover;<br>Fold Shorts;<br>Robot Dog<br>|NR|
|Go-1 (Bu et al.(2025))|VLADP|NA|Ego4D;<br>Open-X;<br>AgiBot World<br>(140K Traj.)|NA|Self-creation|Out-of-Box:<br>GO-1: 78%;<br>RDT-1B: 46%|Dual-Arm|Restock Bag;<br>Table Bussing;<br>Pour Water;<br>Restock Beverage;<br>Fold Shorts;<br>Wipe Table|NR|
|OpenVLA-OFT (Kim et al.(2025))|VLADP|NA|970K Demo.<br>from Open-X|20–300 Demo. per Task<br>(Total: 4 Tasks)|Self-creation|Fine-tune:<br>Openvla-oft: 87.8%;<br>PI0: 83.9%;<br>RDT-1B: 78.4%;<br>DP: 77.5%;<br>Act: 723%|ALOHA|Fold Shorts;<br>Fold Shirt;<br>Scoop X into Bowl;<br>Put X into Pot|NR|
|Helix (Figure.ai(2025))|VLADP|NA|_∼_500 Hours Demo.|NA|NR|.<br>NR|Figure 02<br>Humanoid Robot|Pick-Place;<br>Open the Refrigerator<br>Organize the Items;<br>Handover|;<br>NR|
|Groot-N1 (Bjorck et al.(2025))|VLADP|NA<br>|Real World Datasets;<br>Synthetic Dataset;<br>Human Video Datasets (592.9M|)<br>Human Teleoperation Data|Self-creation|Fine-tune:<br>GR00T-N1:76.8%;<br>DP:46.2%|GR-1 Humanoid Robot|Pick-Place;<br>Machinery Packing;<br>Mesh Cup Pouring;<br>Cylinder Handover|NR|


> 1 ”NA” stands for ”Not Application.” 

> 2 ”NR” stands for ”Not Reported.” 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

32 

**Table 5. Representative Policy Works in Sec. 7.** ‘Input Modality’ refers to the type of information that is fed into the model. ‘Architecture’ refers to the structural framework employed by the method or the integration of multiple foundational models. ‘Train Objective’ refers to the training loss used by the model. ‘Output Modality’ refers to the type of information produced by the model. ‘Inference Frequency’ refers to the frequency of actions generated by the model. ‘Computational Resources’ refers to the computational power utilized during the training and inference stages. 

|**Method**|**Policy Type**|**Input Modality**|**Architecture**|**Train Objective**|**Model Size**|**Output Modality**|**Inference Frequen**|**cy**<br>**Computation Resource**|
|---|---|---|---|---|---|---|---|---|
|Code as Policy<br>(Liang et al.(2023))|VLAC|Language|InstructGPT|NA|175B|Code|NR|NA|
|<br>Instruct2Act<br>(Huang et al.(2023b))|VLAKP|Language; Image|SAM; CLIP|NA|995M|Key Poses|NR|Inference:<br>1 NVIDIA 3090Ti|
|VoxPoser<br>(Huang et al.(2023b))|VLAKP|Language; RGBD Image|OWL-ViT; SAM; XMEM; GPT-4|NA|NR|Key Poses|NR|NR|
|ReKep<br>(Huang et al.(2024a))|VLAKP|Language; RGBD Image|DINO; SAM; GPT-4O|NA|NR|Key Poses|NR|NR|
|CLIPort<br>(Shridhar et al.(2021))|VLAKP|Language; RGBD Image|Two-Stream Architecture|Cross Entropy|NR|Key Poses|NR|Inference:<br>1 NVIDIA P100|
|PerAct<br>(Shridhar et al.(2023))|VLAKP|Language; Voxel Grid|PerceiverIO Transformer|Cross Entropy|33.2M|Key Poses|NR|Train:<br>8 NVIDIA V100 * 384h|
|Act3D<br>(Gervet et al.(2023))|VLAKP|Language; Multi-view Images|3D Feature Field Transformer|Cross Entropy; Regression|NR|Key Poses|NR|Train:<br>8 NVIDIA 32GB V100 * 120h|
|ChainedDiffuser<br>(Xian et al.(2023))|VLAKP|Language; Multi-view Images|3D Feature Field Transformer;<br>Diffusion Policy|Cross Entropy; Diffusion|NR|Key Poses|NR|Train:<br>4 NVIDIA A100 * 120h|
|3D Diffuser Actor<br>(Ke et al.(2024))|VLAKP|Language; RGBD Image|Encoders; Diffusion Model|Cross Entropy; Diffusion|NR|Key Poses|1.67 Hz|Inference:<br>1 NVIDIA 2080 Ti|
|GNFactor<br>(Ze et al.(2023))|VLAKP|Language; RGBD Image|Encoders;<br>Perceiver Transformer|Cross Entropy|41.7M|Key Poses|NR|Train:<br>2 NVIDIA RTX3090 * 48h|
|DNAct<br>(Yan et al.(2024))|VLAKP|Language; Point Cloud|Encoders; Diffusion Model|Cross Entropy; Diffusion|11.1M|Key Poses|NR|Train:<br>2 NVIDIA RTX3090 * 12h|
|VoxAct-B<br>(Liu et al.(2024b))<br>|VLAKP|Language; RGBD Image<br>|VLM;<br>Perceiver Transformer|Cross Entropy|NR|Key Poses|NR|Train:<br>1 NVIDIA 3080 * 48h<br>|
|LEO<br>(Huang et al.(2023a))|VLAKP|Language; Egocentric Image;<br>3D Observation<br>|Encoders; Vicuna|Cross Entropy|7B|Key Poses|NR|Train:<br>4 NVIDIA A100|
|Mani<br>Foundation<br>(Xu et al.(2024))|VLAKP|Language;<br>Object Point Cloud<br>& Physical Properties;<br>Hand Point Cloud|VLM; ManiFoundation|Regression|NR|Contact Points;<br>Force|NR|NR|
|RT-1<br>(Brohan et al.(2022))|VLADP|Language; Image|FiLM; Token Learner;<br>Transformer Model|Cross Entropy|35M|Dense Poses|3HZ|NR<br>|
|Gato<br>(Reed et al.(2022))|VLADP|Prompt; Image; Proprio.|Patch Embedding<br>Transformer Model|Cross Entropy|1.2B|Dense Poses|20HZ|Train:<br>16*16 TPU v3 slice * 96h<br>Inference:<br>1 NVIDIA RTX3090s|
|RoboCat<br>(Bousmalis et al.(2023))|VLADP|Prompt; Image; Proprio.|Patch Embedding<br>Transformer Model;<br>VQGAN|Cross Entropy|1.2B|Dense Poses;<br>Hindsight Image|NR|NR|
|RoboAgent<br>(Bharadhwaj et al.(2023))|VLADP|Language; Image; Proprio.|FiLM; Transformer Encoder;<br>Transformer Decoder<br>|Cross Entropy|NR<br>|Dense Poses|NR|Train:<br>1 NVIDIA 2080Ti * 48h|
|MOO<br>(Stone et al.(2023))|VLADP|Language; Mask Image|FiLM;<br>Token Learner;<br>Transformer Model|Cross Entropy|111M;<br>10.2M;<br>2.37M|Dense Poses|NR|NR|
|Q-Transformer<br>(Chebotar et al.(2023))|VLADP|Language; Image|FiLM;<br>Transformer Model|TD-Learning|NR|Dense Poses|3 Hz|NR|
|RT-2<br>(Brohan et al.(2023))|VLADP|Language; Image|Encoder; GPT-Style<br>Transformer; Action Head|Cross Entropy|12B;<br>55B|Dense Poses|1-3HZ (55B);<br>5HZ (5B)|Inference:<br>Multi-TPU Cloud Service<br>|
|OpenVLA<br>(Kim et al.(2024))|VLADP|Language; Image|Encoders; GPT-Style<br>Transformer;<br>Action Head|Cross Entropy|7B|Dense Poses|6Hz|Train:<br>64 NVIDIA A100 * 336h;<br>Inference:<br>1 NVIDIA RTX 4090|
|Octo<br>(Team et al.(2024))|VLADP|Language; Image; Proprio.|Tokenizers;<br>Transformer Backbone;<br>Readout Heads;<br>Diffusion Action Head|Diffusion|10M;<br>27M;<br>93M|Dense Poses|5–15Hz|Train:<br>1 TPU v4-128 pod * 14h;<br>Fine-tune:<br>1 NVIDIA A5000 * 5h<br>|
|HPT<br>(Wang et al.(2024d))|VLADP|Proprio.; Image|Varies Tokenization Stems;<br>Transformer Trunk;<br>Varies Action Heads|Regression|1B|Dense Poses|33Hz|Fine-tune:<br>1 NVIDIA RTX 2080Ti * 4h;<br>Inference:<br>1 NVIDIA RTX 3070|
|SuSIE<br>(Black et al.(2023))|VLADP|Language; Image|Goal Generation Model;<br>Goal-Reaching Model<br>|Diffusion|NR|Dense Poses|NR|Train:<br>1 v4-64 TPU pod * 17h<br>1 v4-8 TPU VM * 15h|
|GR-1<br>(Wu et al.(2023a))|VLADP|Language; Image; Proprio.|Encoders; GPT-style<br>Transformer;<br>Action Head|Regression|195M|Dense Poses|NR|NR|
|GR-2<br>(Cheang et al.(2024))|VLADP|Language; Image; Proprio.|Encoders; GPT-style<br>Transformer;<br>Action Head & VQGAN<br>|Regression|230M|Dense Poses;<br>Hindsight Image|NR|NR|
|LAPA<br>(Ye et al.(2024))|VLADP|Language; Image|Encoders; GPT-style<br>Transformer;<br>Action Head<br>|Cross Entropy|7B|Dense Poses|NR|Train:<br>8 NVIDIA H100 * 34h|
|PI0 (Black et al.)|VLADP|Language; Image; Proprio.|Encoders; GPT-style<br>Transformer;<br>Flow Matching Model|Diffusion|3.3B|Dense Poses|13Hz|Inference:<br>1 NVIDIA RTX 4090|
|RDT-1B<br>(Liu et al.(2024d))|VLADP|Language; Image; Proprio.|DiT Block; MLP|Diffusion|1B|Dense Poses|381Hz|Train:<br>48 NVIDIA 80GB H100 * 720h;<br>Fine-tune:<br>48 NVIDIA 80GB H100 * 72h;<br>Inference:|
|||||||||1 NVIDIA 24GB RTX 4090|
|Go-1<br>(Bu et al.(2025))|VLADP|Language; Image|Encodes; GPT-style<br>Transformer;<br>Latent Planner; Action Expert|Diffusion|2B|Dense Poses|NR|NR|
|OpenVLA-OFT<br>(Bu et al.(2025))|VLADP|Language; Image; Proprio.|FiLM; GPT-style<br>Transformer;<br>Action Head|Regression|7B|Dense Poses|77.9Hz|Fine-tune:<br>8 NVIDIA 80GB H100;<br>Inference:<br>1 NVIDIA A100|
|Helix<br>(Figure.ai(2025))|VLADP|Language; Image; Proprio.|System1 (fast) + System2 (slow)|Regression|7B|Dense Poses|200Hz|<br>NR<br>|
|Groot-N1<br>(Bjorck et al.(2025))|VLADP|Language; Image; Proprio.|System 1 (fast) + System 2 (slow)|Diffusion|2.2B|Dense Poses|120Hz|Train:<br>1024 NVIDIA H100 * 49h;<br>Fine-tune:<br>1 NVIDIA A6000;<br>Inference:<br>1 NVIDIA L40|


1 ”NA” stands for ”Not Application.” 

2 ”NR” stands for ”Not Reported.” 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

33 

**Table 6. Representative Hierarchy of Skills Works in Sec. 5.** ‘Instruction Type’ refers to the modality of instructions given to the model. ‘Foundation Models’ refers to the type of foundation model used by the method. ‘Manipulation Task’ refers to the task or benchmark designed for each method experiment. ‘Horizon Steps’ refers to the maximum number of steps in the examples provided in the method paper or website. ‘Success Rate’ refers to the average execution success rate of all tasks for each method and the baseline. ‘Failure Modes’ refers to the common failure cases of the method, as indicated in the paper. There are three main types of Failure Modes: Wrong Object Error: The method fails to recognize different objects. Spatial Relations Error: The method fails to reason about the spatial relations between objects for task planning. Task Order Failure: The method fails to generate the correct temporal order of actions. 

|**Method**|**Instruction**<br>**Type**|**Foundation**<br>**Models**|**Manipulation**<br>**Task**|**Horizon**<br>**Steps**|**Success**<br>**Rate**|**Failure**<br>**Modes**|
|---|---|---|---|---|---|---|
|VLaMP (Patel et al.(2023))|Video|GPT-2|Cooking; Assembly; etc.|8|47.9%|NR|
||||Vegetable Organization;|||Wrong Object Error;|
|SeeDo (Wang et al.(2024a))|Video|GPT-4o|Garments Organization;<br>Wooden Block Stacking|6|36.3%|Spatial Relations Error;<br>Task Order Failure|
|SayCan (Ahn et al.(2022))|Language|PaLM|Bring Something;<br>Throw away Something; etc.|16|67%|Wrong Object Error;|
|GD (Huang et al.(2023d))|Language|PaLM / InstructGPT|Bring Something;<br>Throw away Something; etc.|8|GD: 44%;<br>SayCan: 25%|Task Order Failure|
|TidyBot (Huang et al.(2023d))|Language|GPT-3|Household Organization|10|85%|Wrong Object Error|
|ReAct (Yao et al.(2022b))|Language|PaLM|ALFWorld|more than 50 steps|71%|Task Order Failure|
|LLM-Planner (Song et al.(2023))|Language|GPT-3|ALFRED|7|LLM-Planner: 30%;<br>SayCan: 23.5%|Wrong Object Error|
|VILA (Hu et al.(2023a))|Language|GPT-4V|Stack Plates Steadily;<br>Bring Something;<br>Take Out Something;<br>Prepare Art Class; etc.|6|VILA: 80%;<br>GD: 20%;<br>SayCan: 13%|Wrong Object Error;<br>Spatial Relations Error|
||||Rearrangement;||||
|LLM+P (Liu et al.(2023a))|Language|GPT-4|Create Cocktails;<br>Build Towers; etc.|NR|46%|Task Order Failure|


> 1 ”NR” stands for ”Not Reported.” 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

34 

### **References** 

- Aceituno-Cabezas B and Rodriguez A (2020) A global quasidynamic model for contact-trajectory optimization in manipulation . 

- Achiam J, Adler S, Agarwal S, Ahmad L, Akkaya I, Aleman FL, Almeida D, Altenschmidt J, Altman S, Anadkat S et al. (2023) Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ . 

- Ahn M, Brohan A, Brown N, Chebotar Y, Cortes O, David B, Finn C, Fu C, Gopalakrishnan K, Hausman K et al. (2022) Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ . 

- Anitescu M (2006) Optimization-based simulation of nonsmooth rigid multibody dynamics. _Mathematical Programming_ 105: 113–143. 

- Ausserlechner P, Haberger D, Thalhammer S, Weibel JB and Vincze M (2024) Zs6d: Zero-shot 6d object pose estimation using vision transformers. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 463–469. 

- Austin J, Odena A, Nye M, Bosma M, Michalewski H, Dohan D, Jiang E, Cai C, Terry M, Le Q et al. (2021) Program synthesis with large language models. _arXiv preprint arXiv:2108.07732_ 

- Bahl S, Mendonca R, Chen L, Jain U and Pathak D (2023) Affordances from human videos as a versatile representation for robotics. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 13778–13790. 

- Bai Y, Wong L and Twan T (2024) Survey on fundamental deep learning 3d reconstruction techniques. _arXiv preprint arXiv:2407.08137_ . 

- Bain M, Nagrani A, Varol G and Zisserman A (2021) Frozen in time: A joint video and image encoder for end-to-end retrieval. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 1728–1738. 

- Belkhale S, Ding T, Xiao T, Sermanet P, Vuong Q, Tompson J, Chebotar Y, Dwibedi D and Sadigh D (2024) Rt-h: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ . 

- Bharadhwaj H, Vakil J, Sharma M, Gupta A, Tulsiani S and Kumar V (2023) Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. _arXiv preprint arXiv:2309.01918_ . 

- Bhateja C, Guo D, Ghosh D, Singh A, Tomar M, Vuong Q, Chebotar Y, Levine S and Kumar A (2023) Robotic offline rl from internet videos via value-function pre-training. _arXiv preprint arXiv:2309.13041_ . 

- Bicchi A (2000) Hands for dexterous manipulation and robust grasping: A difficult road toward simplicity. _IEEE Transactions on robotics and automation_ 16(6): 652–662. 

- Billard A and Kragic D (2019) Trends and challenges in robot manipulation. _Science_ 364(6446): eaat8414. 

- Bjorck J, Casta˜neda F, Cherniadev N, Da X, Ding R, Fan L, Fang Y, Fox D, Hu F, Huang S et al. (2025) Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ . 

- Black K, Brown N, Driess D, Esmail A, Equi M, Finn C, Fusai N, Groom L, Hausman K, Ichter B et al. (????) _π_ 0: A vision-language-action flow model for general robot control. corr, abs/2410.24164, 2024. doi: 10.48550. _arXiv preprint ARXIV.2410.24164_ . 

- Black K, Brown N, Driess D, Esmail A, Equi M, Finn C, Fusai N, Groom L, Hausman K, Ichter B et al. (2024) pi0: A visionlanguage-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ . 

- Black K, Nakamoto M, Atreya P, Walke H, Finn C, Kumar A and Levine S (2023) Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arXiv preprint arXiv:2310.10639_ . 

- Blattmann A, Dockhorn T, Kulal S, Mendelevitch D, Kilian M, Lorenz D, Levi Y, English Z, Voleti V, Letts A et al. (2023) Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ . 

- Bohg J, Hausman K, Sankaran B, Brock O, Kragic D, Schaal S and Sukhatme GS (2017) Interactive perception: Leveraging action in perception and perception in action. _IEEE Transactions on Robotics_ 33(6): 1273–1291. 

- Bousmalis K, Trigeorgis G, Silberman N, Krishnan D and Erhan D (2016) Domain separation networks. _Advances in neural information processing systems_ 29. 

- Bousmalis K, Vezzani G, Rao D, Devin C, Lee AX, Bauza M, Davchev T, Zhou Y, Gupta A, Raju A et al. (2023) Robocat: A self-improving foundation agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ . 

- Brohan A, Brown N, Carbajal J, Chebotar Y, Chen X, Choromanski K, Ding T, Driess D, Dubey A, Finn C et al. (2023) Rt2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ . 

- Brohan A, Brown N, Carbajal J, Chebotar Y, Dabis J, Finn C, Gopalakrishnan K, Hausman K, Herzog A, Hsu J et al. (2022) Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ . 

- Brooks T, Holynski A and Efros AA (2023) Instructpix2pix: Learning to follow image editing instructions. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 18392–18402. 

- Brooks T, Peebles B, Holmes C, DePue W, Guo Y, Jing L, Schnurr D, Taylor J, Luhman T, Luhman E, Ng C, Wang R and Ramesh A (2024) Video generation models as world simulators URL https://openai.com/research/ video-generation-models-as-world-simulators. 

- Brown T, Mann B, Ryder N, Subbiah M, Kaplan JD, Dhariwal P, Neelakantan A, Shyam P, Sastry G, Askell A et al. (2020) Language models are few-shot learners. _Advances in neural information processing systems_ 33: 1877–1901. 

- Bu Q, Cai J, Chen L, Cui X, Ding Y, Feng S, Gao S, He X, Hu X, Huang X et al. (2025) Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ . 

- Bucker A, Figueredo L, Haddadin S, Kapoor A, Ma S, Vemprala S and Bonatti R (2023) Latte: Language trajectory transformer. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 7287–7294. 

- Burde V, Benbihi A, Burget P and Sattler T (2024) Comparative evaluation of 3d reconstruction methods for object pose estimation. _arXiv preprint arXiv:2408.08234_ . 

- Butime J, Gutierrez I, Corzo LG and Espronceda CF (2006) 3d reconstruction methods, a survey. In: _Proceedings of the First International Conference on Computer Vision Theory and Applications_ . pp. 457–463. 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

35 

- Cai J, He Y, Yuan W, Zhu S, Dong Z, Bo L and Chen Q (2024) Ov9d: Open-vocabulary category-level 9d object pose and size estimation. _arXiv preprint arXiv:2403.12396_ . 

- Calli B, Singh A, Bruce J, Walsman A, Konolige K, Srinivasa S, Abbeel P and Dollar AM (2017) Yale-cmu-berkeley dataset for robotic manipulation research. _The International Journal of Robotics Research_ 36(3): 261–268. 

- Caraffa A, Boscaini D, Hamza A and Poiesi F (2024) Freeze: Training-free zero-shot 6d pose estimation with geometric and vision foundation models. In: _European Conference on Computer Vision_ . Springer, pp. 414–431. 

- Caron M, Touvron H, Misra I, J´egou H, Mairal J, Bojanowski P and Joulin A (2021) Emerging properties in self-supervised vision transformers. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 9650–9660. 

- Cassinis R and Tampalini F (2007) Amirolos an active marker internet-based robot localization system. _Robotics and autonomous systems_ 55(4): 306–315. 

- Chabra R, Lenssen JE, Ilg E, Schmidt T, Straub J, Lovegrove S and Newcombe R (2020) Deep local shapes: Learning local sdf priors for detailed 3d reconstruction. In: _Computer Vision– ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part XXIX 16_ . Springer, pp. 608– 625. 

- Chandrasegaran K, Gupta A, Hadzic LM, Kota T, He J, Eyzaguirre C, Durante Z, Li M, Wu J and Fei-Fei L (2024) Hourvideo: 1-hour video-language understanding. _arXiv preprint arXiv:2411.04998_ . 

- Chang AX, Funkhouser T, Guibas L, Hanrahan P, Huang Q, Li Z, Savarese S, Savva M, Song S, Su H et al. (2015) Shapenet: An information-rich 3d model repository. _arXiv preprint arXiv:1512.03012_ . 

- Cheang CL, Chen G, Jing Y, Kong T, Li H, Li Y, Liu Y, Wu H, Xu J, Yang Y et al. (2024) Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ . 

- Chebotar Y, Vuong Q, Hausman K, Xia F, Lu Y, Irpan A, Kumar A, Yu T, Herzog A, Pertsch K et al. (2023) Q-transformer: Scalable offline reinforcement learning via autoregressive q- functions. In: _Conference on Robot Learning_ . PMLR, pp. 3909–3928. 

- Chen B, Chen Z, Chen X, Mao S, Pan F, Li L, Liu W, Min H, Ding X, Fang B et al. (2024a) Teleoperation of an anthropomorphic robot hand with a metamorphic palm and tunable-stiffness soft fingers. _Soft Robotics_ . 

- Chen B, Xia F, Ichter B, Rao K, Gopalakrishnan K, Ryoo MS, Stone A and Kappler D (2023a) Open-vocabulary queryable scene representations for real world planning. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 11509–11522. 

- Chen B, Xu Z, Kirmani S, Ichter B, Sadigh D, Guibas L and Xia F (2024b) Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 14455–14465. 

- Chen C, Culbertson P, Lepert M, Schwager M and Bohg J (2021a) Trajectotree: Trajectory optimization meets tree search for planning multi-contact dexterous manipulation. In: _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 8262–8268. 

- Chen JT and Huang CM (2023) Forgetful large language models: Lessons learned from using llms in robot programming. _arXiv preprint arXiv:2310.06646_ . 

- Chen M, Tworek J, Jun H, Yuan Q, Pinto HPdO, Kaplan J, Edwards H, Burda Y, Joseph N, Brockman G et al. (2021b) Evaluating large language models trained on code. _arXiv preprint arXiv:2107.03374_ . 

- Chen X, Djolonga J, Padlewski P, Mustafa B, Changpinyo S, Wu J, Ruiz CR, Goodman S, Wang X, Tay Y et al. (2023b) Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ . 

- Chen Z, Kiami S, Gupta A and Kumar V (2023c) Genaug: Retargeting behaviors to unseen situations via generative augmentation. _arXiv preprint arXiv:2302.06671_ . 

- Chen Z, Walsman A, Memmel M, Mo K, Fang A, Vemuri K, Wu A, Fox D and Gupta A (2024c) Urdformer: A pipeline for constructing articulated simulation environments from realworld images. _arXiv preprint arXiv:2405.11656_ . 

- Chen Z, Zhang S, Luo S, Sun F and Fang B (2023d) Tacchi: A pluggable and low computational cost elastomer deformation simulator for optical tactile sensors. _IEEE Robotics and Automation Letters_ 8(3): 1239–1246. 

- Cheng HK and Schwing AG (2022) Xmem: Long-term video object segmentation with an atkinson-shiffrin memory model. In: _European Conference on Computer Vision_ . Springer, pp. 640– 658. 

- Cheng X, Li J, Yang S, Yang G and Wang X (2024) Open-television: Teleoperation with immersive active visual feedback. _arXiv preprint arXiv:2407.01512_ . 

- Cheng X, Patil S, Temel Z, Kroemer O and Mason MT (2023) Enhancing dexterity in robotic manipulation via hierarchical contact exploration. _IEEE Robotics and Automation Letters_ 9(1): 390–397. 

- Chi C, Feng S, Du Y, Xu Z, Cousineau E, Burchfiel B and Song S (2023) Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ . 

- Chi C, Xu Z, Pan C, Cousineau E, Burchfiel B, Feng S, Tedrake R and Song S (2024) Universal manipulation interface: In-thewild robot teaching without in-the-wild robots. _arXiv preprint arXiv:2402.10329_ . 

- Coumans E and Bai Y (2016) Pybullet, a python module for physics simulation for games, robotics and machine learning. 

- Cruciani S, Smith C, Kragic D and Hang K (2018) Dexterous manipulation graphs. In: _2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 2040–2047. 

- Cui Y, Karamcheti S, Palleti R, Shivakumar N, Liang P and Sadigh D (2023) No, to the right: Online language corrections for robotic manipulation via shared autonomy. In: _Proceedings of the 2023 ACM/IEEE International Conference on HumanRobot Interaction_ . pp. 93–101. 

- Cui Y, Niekum S, Gupta A, Kumar V and Rajeswaran A (2022) Can foundation models perform zero-shot task specification for robot manipulation? In: _Learning for Dynamics and Control Conference_ . PMLR, pp. 893–905. 

- Dai Q, Zhang J, Li Q, Wu T, Dong H, Liu Z, Tan P and Wang H (2022) Domain randomization-enhanced depth simulation and restoration for perceiving and grasping specular and transparent objects. In: _European Conference on Computer Vision_ . Springer, pp. 374–391. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

36 

- Dai Q, Zhu Y, Geng Y, Ruan C, Zhang J and Wang H (2023) Graspnerf: Multiview-based 6-dof grasp detection for transparent and specular objects using generalizable nerf. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 1757–1763. 

- Dai T, Wong J, Jiang Y, Wang C, Gokmen C, Zhang R, Wu J and Fei-Fei L (2024) Automated creation of digital cousins for robust policy learning. _arXiv preprint arXiv:2410.07408_ . 

- Damen D, Doughty H, Farinella GM, Furnari A, Kazakos E, Ma J, Moltisanti D, Munro J, Perrett T, Price W et al. (2022) Rescaling egocentric vision: Collection, pipeline and challenges for epic-kitchens-100. _International Journal of Computer Vision_ : 1–23. 

- Darvish K, Penco L, Ramos J, Cisneros R, Pratt J, Yoshida E, Ivaldi S and Pucci D (2023) Teleoperation of humanoid robots: A survey. _IEEE Transactions on Robotics_ 39(3): 1706–1727. 

- Dasari S, Ebert F, Tian S, Nair S, Bucher B, Schmeckpeper K, Singh S, Levine S and Finn C (2019) Robonet: Large-scale multirobot learning. _arXiv preprint arXiv:1910.11215_ . 

- De Pace F, Gorjup G, Bai H, Sanna A, Liarokapis M and Billinghurst M (2021) Leveraging enhanced virtual reality methods and environments for efficient, intuitive, and immersive teleoperation of robots. In: _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 12967–12973. 

- Dehghani M, Djolonga J, Mustafa B, Padlewski P, Heek J, Gilmer J, Steiner AP, Caron M, Geirhos R, Alabdulmohsin I et al. (2023) Scaling vision transformers to 22 billion parameters. In: _International Conference on Machine Learning_ . PMLR, pp. 7480–7512. 

- Deitke M, Schwenk D, Salvador J, Weihs L, Michel O, VanderBilt E, Schmidt L, Ehsani K, Kembhavi A and Farhadi A (2023) Objaverse: A universe of annotated 3d objects. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 13142–13153. 

- Deitke M, VanderBilt E, Herrasti A, Weihs L, Ehsani K, Salvador J, Han W, Kolve E, Kembhavi A and Mottaghi R (2022) Procthor: Large-scale embodied ai using procedural generation. _Advances in Neural Information Processing Systems_ 35: 5982–5994. 

- DelPreto J, Liu C, Luo Y, Foshey M, Li Y, Torralba A, Matusik W and Rus D (2022) Actionsense: A multimodal dataset and recording framework for human activities using wearable sensors in a kitchen environment. _Advances in Neural Information Processing Systems_ 35: 13800–13813. 

- Deng J, Dong W, Socher R, Li LJ, Li K and Fei-Fei L (2009) Imagenet: A large-scale hierarchical image database. In: _2009 IEEE conference on computer vision and pattern recognition_ . Ieee, pp. 248–255. 

- Deng X, Mousavian A, Xiang Y, Xia F, Bretl T and Fox D (2021) Poserbpf: A rao–blackwellized particle filter for 6-d object pose tracking. _IEEE Transactions on Robotics_ 37(5): 1328– 1342. 

- Devlin J, Chang MW, Lee K and Toutanova K (2018) Bert: Pre-training of deep bidirectional transformers for language understanding. _arXiv preprint arXiv:1810.04805_ . 

- Di Palo N, Byravan A, Hasenclever L, Wulfmeier M, Heess N and Riedmiller M (2023) Towards a unified agent with foundation models. _arXiv preprint arXiv:2307.09668_ . 

- Ding Y, Zhang X, Amiri S, Cao N, Yang H, Esselink C and Zhang S (2022) Robot task planning and situation handling in open worlds. _arXiv preprint arXiv:2210.01287_ . 

- Ding Y, Zhang X, Paxton C and Zhang S (2023) Task and motion planning with large language models for object rearrangement. _arXiv preprint arXiv:2303.06247_ . 

- Driess D, Xia F, Sajjadi MS, Lynch C, Chowdhery A, Ichter B, Wahid A, Tompson J, Vuong Q, Yu T et al. (2023) Palme: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ . 

- Du Y, Yang S, Dai B, Dai H, Nachum O, Tenenbaum J, Schuurmans D and Abbeel P (2024) Learning universal policies via textguided video generation. _Advances in Neural Information Processing Systems_ 36. 

- Duan J, Pumacay W, Kumar N, Wang YR, Tian S, Yuan W, Krishna R, Fox D, Mandlekar A and Guo Y (2024) Aha: A visionlanguage-model for detecting and reasoning over failures in robotic manipulation. _arXiv preprint arXiv:2410.00371_ . 

- Ellis K, Wong L, Nye M, Sable-Meyer M, Cary L, Anaya Pozo L, Hewitt L, Solar-Lezama A and Tenenbaum JB (2023) Dreamcoder: growing generalizable, interpretable knowledge with wake–sleep bayesian program learning. _Philosophical Transactions of the Royal Society A_ 381(2251): 20220050. 

- Eysenbach B, Asawa S, Chaudhari S, Levine S and Salakhutdinov R (2020) Off-dynamics reinforcement learning: Training for transfer with domain classifiers. _arXiv preprint arXiv:2006.13916_ . 

- Eze C and Crick C (2024) Learning by watching: A review of video-based learning approaches for robot manipulation. _arXiv preprint arXiv:2402.07127_ . 

- Fang B, Ma X, Wang J and Sun F (2020a) Vision-based postureconsistent teleoperation of robotic arm using multi-stage deep neural network. _Robotics and Autonomous Systems_ 131: 103592. 

- Fang B, Sun F, Liu H and Guo D (2017a) A novel data glove using inertial and magnetic sensors for motion capture and robotic arm-hand teleoperation. _Industrial Robot: An International Journal_ 44(2): 155–165. 

- Fang B, Sun F, Liu H, Guo D, Chen W and Yao G (2017b) Robotic teleoperation systems using a wearable multimodal fusion device. _International journal of advanced robotic systems_ 14(4): 1729881417717057. 

- Fang H, Fang HS, Wang Y, Ren J, Chen J, Zhang R, Wang W and Lu C (2024) Airexo: Low-cost exoskeletons for learning wholearm manipulation in the wild. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 15031–15038. 

- Fang H, Fang HS, Xu S and Lu C (2022) Transcg: A large-scale real-world dataset for transparent object depth completion and a grasping baseline. _IEEE Robotics and Automation Letters_ 7(3): 7383–7390. 

- Fang HS, Wang C, Gou M and Lu C (2020b) Graspnet-1billion: A large-scale benchmark for general object grasping. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 11444–11453. 

- Ferrari C, Canny JF et al. (1992) Planning optimal grasps. In: _ICRA_ , volume 3. p. 6. 

- Figureai (2025) Helix. URL https://www.figure.ai/ news/helix?ref=fixthenews.com. Accessed: 202502-20. 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

37 

- Firoozi R, Tucker J, Tian S, Majumdar A, Sun J, Liu W, Zhu Y, Song S, Kapoor A, Hausman K et al. (2023) Foundation models in robotics: Applications, challenges, and the future. _The International Journal of Robotics Research_ : 02783649241281508. 

- Fu K, Peng J, He Q and Zhang H (2021) Single image 3d object reconstruction based on deep learning: A review. _Multimedia Tools and Applications_ 80(1): 463–498. 

- Fu Z, Zhao Q, Wu Q, Wetzstein G and Finn C (2024) Humanplus: Humanoid shadowing and imitation from humans. _arXiv preprint arXiv:2406.10454_ . 

- Gao J, Sarkar B, Xia F, Xiao T, Wu J, Ichter B, Majumdar A and Sadigh D (2023) Physically grounded vision-language models for robotic manipulation. 

- Gao P, Geng S, Zhang R, Ma T, Fang R, Zhang Y, Li H and Qiao Y (2024) Clip-adapter: Better vision-language models with feature adapters. _International Journal of Computer Vision_ 132(2): 581–595. 

- Ge Y, Macaluso A, Li LE, Luo P and Wang X (2023) Policy adaptation from foundation model feedback. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 19059–19069. 

- Geng H, Xu H, Zhao C, Xu C, Yi L, Huang S and Wang H (2023a) Gapartnet: Cross-category domain-generalizable object perception and manipulation via generalizable and actionable parts. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 7081–7091. 

- Geng Y, An B, Geng H, Chen Y, Yang Y and Dong H (2023b) Rlafford: End-to-end affordance learning for robotic manipulation. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 5880–5886. 

- Gervet T, Xian Z, Gkanatsios N and Fragkiadaki K (2023) Act3d: 3d feature field transformers for multi-task robotic manipulation. In: _7th Annual Conference on Robot Learning_ . 

- Gibson JJ (2014) _The ecological approach to visual perception: classic edition_ . Psychology press. 

- Grauman K, Westbury A, Byrne E, Chavis Z, Furnari A, Girdhar R, Hamburger J, Jiang H, Liu M, Liu X et al. (2022) Ego4d: Around the world in 3,000 hours of egocentric video. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 18995–19012. 

- Grauman K, Westbury A, Torresani L, Kitani K, Malik J, Afouras T, Ashutosh K, Baiyya V, Bansal S, Boote B et al. (2024) Egoexo4d: Understanding skilled human activity from first-and third-person perspectives. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 19383–19400. 

- Gu J, Xiang F, Li X, Ling Z, Liu X, Mu T, Tang Y, Tao S, Wei X, Yao Y et al. (2023) Maniskill2: A unified benchmark for generalizable manipulation skills. _arXiv preprint arXiv:2302.04659_ . 

- Gu X, Lin TY, Kuo W and Cui Y (2021) Open-vocabulary object detection via vision and language knowledge distillation. _arXiv preprint arXiv:2104.13921_ . 

- Guan J, Hao Y, Wu Q, Li S and Fang Y (2024) A survey of 6dof object pose estimation methods for different application scenarios. _Sensors_ 24(4): 1076. 

- Guo H, Wu F, Qin Y, Li R, Li K and Li K (2023) Recent trends in task and motion planning for robotics: A survey. _ACM Computing Surveys_ 55(13s): 1–36. 

- Gupta A, Yu J, Zhao TZ, Kumar V, Rovinsky A, Xu K, Devlin T and Levine S (2021) Reset-free reinforcement learning via multitask learning: Learning dexterous manipulation behaviors without human intervention. In: _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6664–6671. 

- Guzey I, Dai Y, Savva G, Bhirangi R and Pinto L (2024) Bridging the human to robot dexterity gap through object-oriented rewards. _arXiv preprint arXiv:2410.23289_ . 

- Ha H, Florence P and Song S (2023) Scaling up and distilling down: Language-guided robot skill acquisition. In: _Conference on Robot Learning_ . PMLR, pp. 3766–3777. 

- Ha H and Song S (2022) Semantic abstraction: Open-world 3d scene understanding from 2d vision-language models. _arXiv preprint arXiv:2207.11514_ . 

- Han K, Wang Y, Chen H, Chen X, Guo J, Liu Z, Tang Y, Xiao A, Xu C, Xu Y et al. (2022) A survey on vision transformer. _IEEE transactions on pattern analysis and machine intelligence_ 45(1): 87–110. 

- Haque A, Tancik M, Efros AA, Holynski A and Kanazawa A (2023) Instruct-nerf2nerf: Editing 3d scenes with instructions. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 19740–19750. 

- Haviland J and Corke P (2021) Neo: A novel expeditious optimisation algorithm for reactive motion control of manipulators. _IEEE Robotics and Automation Letters_ 6(2): 1043–1050. 

- He K, Chen X, Xie S, Li Y, Doll´ar P and Girshick R (2022) Masked autoencoders are scalable vision learners. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 16000–16009. 

- Hejna J, Mirchandani S, Balakrishna A, Xie A, Wahid A, Tompson J, Sanketi P, Shah D, Devin C and Sadigh D (2025) Robot data curation with mutual information estimators. _arXiv preprint arXiv:2502.08623_ . 

- Herzog A, Rao K, Hausman K, Lu Y, Wohlhart P, Yan M, Lin J, Arenas MG, Xiao T et al. (2023) Deep rl at scale: Sorting waste in office buildings with a fleet of mobile manipulators. 

- Hogan FR and Rodriguez A (2020) Feedback control of the pusher-slider system: A story of hybrid and underactuated contact dynamics. In: _Algorithmic Foundations of Robotics XII: Proceedings of the Twelfth Workshop on the Algorithmic Foundations of Robotics_ . Springer, pp. 800–815. 

- Hong Y, Zhen H, Chen P, Zheng S, Du Y, Chen Z and Gan C (2023a) 3d-llm: Injecting the 3d world into large language models. _Advances in Neural Information Processing Systems_ 36: 20482–20494. 

- Hong Y, Zhen H, Chen P, Zheng S, Du Y, Chen Z and Gan C (2023b) 3d-llm: Injecting the 3d world into large language models. _Advances in Neural Information Processing Systems_ 36: 20482–20494. 

- Howell T, Gileadi N, Tunyasuvunakool S, Zakka K, Erez T and Tassa Y (2022) Predictive sampling: Real-time behaviour synthesis with mujoco. _arXiv preprint arXiv:2212.00541_ . 

- Hu Y, Lin F, Zhang T, Yi L and Gao Y (2023a) Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning. _arXiv preprint arXiv:2311.17842_ . 

- Hu Y, Xie Q, Jain V, Francis J, Patrikar J, Keetha N, Kim S, Xie Y, Zhang T, Zhao Z et al. (2023b) Toward general-purpose robots via foundation models: A survey and meta-analysis. _arXiv_ 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

38 

_preprint arXiv:2312.08782_ . 

- Hu Y, Yang J, Chen L, Li K, Sima C, Zhu X, Chai S, Du S, Lin T, Wang W et al. (2023c) Planning-oriented autonomous driving. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 17853–17862. 

- Huang E, Cheng X and Mason MT (2021) Efficient contact mode enumeration in 3d. In: _Algorithmic Foundations of Robotics XIV: Proceedings of the Fourteenth Workshop on the Algorithmic Foundations of Robotics 14_ . Springer, pp. 485– 501. 

- Huang J, Yong S, Ma X, Linghu X, Li P, Wang Y, Li Q, Zhu SC, Jia B and Huang S (2023a) An embodied generalist agent in 3d world. _arXiv preprint arXiv:2311.12871_ . 

- Huang S, Jiang Z, Dong H, Qiao Y, Gao P and Li H (2023b) Instruct2act: Mapping multi-modality instructions to robotic actions with large language model. _arXiv preprint arXiv:2305.11176_ . 

- Huang W, Abbeel P, Pathak D and Mordatch I (2022) Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In: _International Conference on Machine Learning_ . PMLR, pp. 9118–9147. 

- Huang W, Wang C, Li Y, Zhang R and Fei-Fei L (2024a) Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. _arXiv preprint arXiv:2409.01652_ . 

- Huang W, Wang C, Zhang R, Li Y, Wu J and Fei-Fei L (2023c) Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ . 

- Huang W, Xia F, Shah D, Driess D, Zeng A, Lu Y, Florence P, Mordatch I, Levine S, Hausman K et al. (2023d) Grounded decoding: Guiding text generation with grounded models for robot control. _arXiv preprint arXiv:2303.00855_ . 

- Huang Z, Wen Y, Wang Z, Ren J and Jia K (2024b) Surface reconstruction from point clouds: A survey and a benchmark. _IEEE transactions on pattern analysis and machine intelligence_ . 

- Issac J, W¨uthrich M, Cifuentes CG, Bohg J, Trimpe S and Schaal S (2016) Depth-based object tracking using a robust gaussian filter. In: _2016 IEEE international conference on robotics and automation (ICRA)_ . IEEE, pp. 608–615. 

- Iyer A, Peng Z, Dai Y, Guzey I, Haldar S, Chintala S and Pinto L (2024) Open teach: A versatile teleoperation system for robotic manipulation. _arXiv preprint arXiv:2403.07870_ . 

- Jaegle A, Gimeno F, Brock A, Vinyals O, Zisserman A and Carreira J (2021) Perceiver: General perception with iterative attention. In: _International conference on machine learning_ . PMLR, pp. 4651–4664. 

- Jain V, Attarian M, Joshi NJ, Wahid A, Driess D, Vuong Q, Sanketi PR, Sermanet P, Welker S, Chan C et al. (2024) Vid2robot: End-to-end video-conditioned policy learning with cross-attention transformers. _arXiv preprint arXiv:2403.12943_ 

- James S, Ma Z, Arrojo DR and Davison AJ (2020) Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ 5(2): 3019–3026. 

- Jang E, Irpan A, Khansari M, Kappler D, Ebert F, Lynch C, Levine S and Finn C (2022) Bc-z: Zero-shot task generalization with robotic imitation learning. In: _Conference on Robot Learning_ . PMLR, pp. 991–1002. 

instructions. _arXiv preprint arXiv:2009.14259_ . 

   - Jatavallabhula KM, Kuwajerwala A, Gu Q, Omama M, Chen T, Maalouf A, Li S, Iyer G, Saryazdi S, Keetha N et al. (2023) Conceptfusion: Open-set multimodal 3d mapping. _arXiv preprint arXiv:2302.07241_ . 

   - Jiang Y, Gupta A, Zhang Z, Wang G, Dou Y, Chen Y, Fei-Fei L, Anandkumar A, Zhu Y and Fan L (2023) Vima: Robot manipulation with multimodal prompts . 

   - Jiang Y, Wang C, Zhang R, Wu J and Fei-Fei L (2024a) Transic: Sim-to-real policy transfer by learning from online correction. _arXiv preprint arXiv:2405.10315_ . 

   - Jiang Y, Yu M, Zhu X, Tomizuka M and Li X (2024b) Contact-implicit model predictive control for dexterous inhand manipulation: A long-horizon and robust approach. In: _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 5260–5266. 

   - Jiang Z, Hsu CC and Zhu Y (2022) Ditto: Building digital twins of articulated objects from interaction. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 5616–5626. 

   - Jiang Z, Xie Y, Lin K, Xu Z, Wan W, Mandlekar A, Fan L and Zhu Y (2024c) Dexmimicgen: Automated data generation for bimanual dexterous manipulation via imitation learning. _arXiv preprint arXiv:2410.24185_ . 

   - Jiang Z, Zhu Y, Svetlik M, Fang K and Zhu Y (2021) Synergies between affordance and geometry: 6-dof grasp detection via implicit representations. _arXiv preprint arXiv:2104.01542_ . 

   - Jin W (2024) Complementarity-free multi-contact modeling and optimization for dexterous manipulation. _arXiv preprint arXiv:2408.07855_ . 

   - Jin Y, Li D, Yong A, Shi J, Hao P, Sun F, Zhang J and Fang B (2024) Robotgpt: Robot manipulation learning from chatgpt. _IEEE Robotics and Automation Letters_ . 

   - Jing Y, Zhu X, Liu X, Sima Q, Yang T, Feng Y and Kong T (2023) Exploring visual pre-training for robot manipulation: Datasets, models and methods. _arXiv preprint arXiv:2308.03620_ . 

   - Joublin F, Ceravola A, Smirnov P, Ocker F, Deigmoeller J, Belardinelli A, Wang C, Hasler S, Tanneberg D and Gienger M (2023) Copal: Corrective planning of robot actions with large language models. _arXiv preprint arXiv:2310.07263_ . 

   - Jumper J, Evans R, Pritzel A, Green T, Figurnov M, Ronneberger O, Tunyasuvunakool K, Bates R, Z´ıdek<sup>ˇ</sup> A, Potapenko A et al. (2021) Highly accurate protein structure prediction with alphafold. _nature_ 596(7873): 583–589. 

   - Kannan SS, Venkatesh VL and Min BC (2023) Smart-llm: Smart multi-agent robot task planning using large language models. _arXiv preprint arXiv:2309.10062_ . 

   - Kapelyukh I, Vosylius V and Johns E (2023) Dall-e-bot: Introducing web-scale diffusion models to robotics. _IEEE Robotics and Automation Letters_ 8(7): 3956–3963. DOI: 10.1109/lra.2023.3272516. URL http://dx.doi.org/ 10.1109/LRA.2023.3272516. 

   - Karamcheti S, Nair S, Chen AS, Kollar T, Finn C, Sadigh D and Liang P (2023) Language-driven representation learning for robotics. _arXiv preprint arXiv:2302.12766_ . 

   - Karashchuk P, Rupp KL, Dickinson ES, Walling-Bell S, Sanders E, Azim E, Brunton BW and Tuthill JC (2021) Anipose: A toolkit for robust markerless 3d pose estimation. _Cell reports_ 36(13). 

- Jansen PA (2020) Visually-grounded planning without vision: Language models infer detailed plans from high-level 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

39 

- Kareer S, Patel D, Punamiya R, Mathur P, Cheng S, Wang C, Hoffman J and Xu D (2024) Egomimic: Scaling imitation learning via egocentric video. _arXiv preprint arXiv:2410.24221_ . 

- Ke TW, Gkanatsios N and Fragkiadaki K (2024) 3d diffuser actor: Policy diffusion with 3d scene representations. _arXiv preprint arXiv:2402.10885_ . 

- Kerbl B, Kopanas G, Leimk¨uhler T and Drettakis G (2023) 3d gaussian splatting for real-time radiance field rendering. URL https://arxiv.org/abs/2308.04079. 

- Kerr J, Kim CM, Goldberg K, Kanazawa A and Tancik M (2023) Lerf: Language embedded radiance fields. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 19729–19739. 

- Khadivar F and Billard A (2023) Adaptive fingers coordination for robust grasp and in-hand manipulation under disturbances and unknown dynamics. _IEEE Transactions on Robotics_ 39(5): 3350–3367. 

- Khan MA, Kenney M, Painter J, Kamale D, Batista-Navarro R and Ghalamzan-E A (2023) Natural language robot programming: Nlp integrated with autonomous robotic grasping. _arXiv preprint arXiv:2304.02993_ . 

- Khan S, Naseer M, Hayat M, Zamir SW, Khan FS and Shah M (2022) Transformers in vision: A survey. _ACM computing surveys (CSUR)_ 54(10s): 1–41. 

- Khandelwal A, Weihs L, Mottaghi R and Kembhavi A (2022) Simple but effective: Clip embeddings for embodied ai. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 14829–14838. 

- Khanna M, Mao Y, Jiang H, Haresh S, Shacklett B, Batra D, Clegg A, Undersander E, Chang AX and Savva M (2024) Habitat synthetic scenes dataset (hssd-200): An analysis of 3d scene scale and realism tradeoffs for objectgoal navigation. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 16384–16393. 

- Khazatsky A, Pertsch K, Nair S, Balakrishna A, Dasari S, Karamcheti S, Nasiriany S, Srirama MK, Chen LY, Ellis K et al. (2024) Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ . 

- Kim G, Kang D, Kim JH, Hong S and Park HW (2023) Contactimplicit mpc: Controlling diverse quadruped motions without pre-planned contact modes or trajectories. _arXiv preprint arXiv:2312.08961_ : 29–84. 

- Kim MJ, Finn C and Liang P (2025) Fine-tuning vision-languageaction models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ . 

- Kim MJ, Pertsch K, Karamcheti S, Xiao T, Balakrishna A, Nair S, Rafailov R, Foster E, Lam G, Sanketi P et al. (2024) Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ . 

- Kirillov A, Mintun E, Ravi N, Mao H, Rolland C, Gustafson L, Xiao T, Whitehead S, Berg AC, Lo WY et al. (2023) Segment anything. _arXiv preprint arXiv:2304.02643_ . 

- Kleeberger K, Bormann R, Kraus W and Huber MF (2020) A survey on learning-based robotic grasping. _Current Robotics Reports_ 1: 239–249. 

- Kober J, Bagnell JA and Peters J (2013) Reinforcement learning in robotics: A survey. _The International Journal of Robotics Research_ 32(11): 1238–1274. 

- Kokic M, Stork JA, Haustein JA and Kragic D (2017) Affordance detection for task-specific grasping using deep learning. In: _2017 IEEE-RAS 17th International Conference on Humanoid Robotics (Humanoids)_ . IEEE, pp. 91–98. 

- Kristinsson K and Dumont GA (1992) System identification and control using genetic algorithms. _IEEE Transactions on Systems, Man, and Cybernetics_ 22(5): 1033–1046. 

- Kroemer O, Niekum S and Konidaris G (2021) A review of robot learning for manipulation: Challenges, representations, and algorithms. _The Journal of Machine Learning Research_ 22(1): 1395–1476. 

- Kulhanek J and Sattler T (2024) Nerfbaselines: Consistent and reproducible evaluation of novel view synthesis methods. _arXiv preprint arXiv:2406.17345_ . 

- Kumar NJ (2023) Will scaling solve robotics? perspectives from corl 2023. https://nishanthjkumar.com/ Will-Scaling-Solve-Robotics-Perspectives% -from-CoRL-2023/. Accessed: 2023-11-25. 

- Labb´e Y, Manuelli L, Mousavian A, Tyree S, Birchfield S, Tremblay J, Carpentier J, Aubry M, Fox D and Sivic J (2022) Megapose: 6d pose estimation of novel objects via render & compare. _arXiv preprint arXiv:2212.06870_ . 

- Le Cleac’h S, Howell TA, Yang S, Lee CY, Zhang J, Bishop A, Schwager M and Manchester Z (2024) Fast contact-implicit model predictive control. _IEEE Transactions on Robotics_ 40: 1617–1629. 

- Le Lidec Q, Jallet W, Montaut L, Laptev I, Schmid C and Carpentier J (2024) Contact models in robotics: a comparative analysis. _IEEE Transactions on Robotics_ . 

- Lee KH, Xiao T, Li A, Wohlhart P, Fischer I and Lu Y (2023) Pi-qt-opt: Predictive information improves multi-task robotic reinforcement learning at scale. In: _Conference on Robot Learning_ . PMLR, pp. 1696–1707. 

- Li C, Xia F, Mart´ın-Mart´ın R, Lingelbach M, Srivastava S, Shen B, Vainio K, Gokmen C, Dharan G, Jain T et al. (2021) igibson 2.0: Object-centric simulation for robot learning of everyday household tasks. _arXiv preprint arXiv:2108.03272_ . 

- Li C, Zhang R, Wong J, Gokmen C, Srivastava S, Mart´ınMart´ın R, Wang C, Levine G, Lingelbach M, Sun J et al. (2023a) Behavior-1k: A benchmark for embodied ai with 1,000 everyday activities and realistic simulation. In: _Conference on Robot Learning_ . PMLR, pp. 80–93. 

- Li F, Vutukur SR, Yu H, Shugurov I, Busam B, Yang S and Ilic S (2023b) Nerf-pose: A first-reconstruct-then-regress approach for weakly-supervised 6d object pose estimation. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 2123–2133. 

- Li J, Gao Q, Johnston M, Gao X, He X, Shakiah S, Shi H, Ghanadan R and Wang WY (2023c) Mastering robot manipulation with multimodal prompts through pretraining and multi-task finetuning. _arXiv preprint arXiv:2310.09676_ . 

- Li J, Gao W, Wu Y, Liu Y and Shen Y (2022) High-quality indoor scene 3d reconstruction with rgb-d cameras: A brief review. _Computational Visual Media_ 8(3): 369–393. 

- Li S, Jiang J, Ruppel P, Liang H, Ma X, Hendrich N, Sun F and Zhang J (2020) A mobile robot hand-arm teleoperation system by vision and imu. In: _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 10900–10906. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

40 

- Li S, Ma X, Liang H, G¨orner M, Ruppel P, Fang B, Sun F and Zhang J (2019) Vision-based teleoperation of shadow dexterous hand using end-to-end deep neural network. In: _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 416–422. 

- Li S and Pan Y (2024) Interactive geometry editing of neural radiance fields. _Displays_ 84: 102810. 

- Li X, Liu M, Zhang H, Yu C, Xu J, Wu H, Cheang C, Jing Y, Zhang W, Liu H et al. (2023d) Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ . 

- Li Y, Wang G, Ji X, Xiang Y and Fox D (2018) Deepim: Deep iterative matching for 6d pose estimation. In: _Proceedings of the European conference on computer vision (ECCV)_ . pp. 683– 698. 

- Liang J, Huang W, Xia F, Xu P, Hausman K, Ichter B, Florence P and Zeng A (2023) Code as policies: Language model programs for embodied control. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 9493–9500. 

- Liao G, Zhou K, Bao Z, Liu K and Li Q (2024) Ov-nerf: Openvocabulary neural radiance fields with vision and language foundation models for 3d semantic understanding. _IEEE Transactions on Circuits and Systems for Video Technology_ . 

- Lin F, Hu Y, Sheng P, Wen C, You J and Gao Y (2024a) Data scaling laws in imitation learning for robotic manipulation. _arXiv preprint arXiv:2410.18647_ . 

- Lin J, Liu L, Lu D and Jia K (2024b) Sam-6d: Segment anything model meets zero-shot 6d object pose estimation. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 27906–27916. 

- Lin K, Agia C, Migimatsu T, Pavone M and Bohg J (2023) Text2motion: From natural language instructions to feasible plans. _arXiv preprint arXiv:2303.12153_ . 

- Lin Y, Tremblay J, Tyree S, Vela PA and Birchfield S (2022) Keypoint-based category-level object pose tracking from an rgb sequence with uncertainty estimation. In: _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 1258–1264. 

- Liu B, Jiang Y, Zhang X, Liu Q, Zhang S, Biswas J and Stone P (2023a) Llm+ p: Empowering large language models with optimal planning proficiency. _arXiv preprint arXiv:2304.11477_ 

- Liu B, Zhu Y, Gao C, Feng Y, Liu Q, Zhu Y and Stone P (2024a) Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ 36. 

- Liu H, Nasiriany S, Zhang L, Bao Z and Zhu Y (2022a) Robot learning on the job: Human-in-the-loop autonomy and learning during deployment. _The International Journal of Robotics Research_ : 02783649241273901. 

- Liu I, Arthur C, He S, Seita D and Sukhatme G (2024b) Voxactb: Voxel-based acting and stabilizing policy for bimanual manipulation. _arXiv preprint arXiv:2407.04152_ . 

- Liu J, Mahdavi-Amiri A and Savva M (2023b) Paris: Part-level reconstruction and motion analysis for articulated objects. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 352–363. 

- Liu J, Sun W, Yang H, Zeng Z, Liu C, Zheng J, Liu X, Rahmani H, Sebe N and Mian A (2024c) Deep learning-based object pose estimation: A comprehensive survey. _arXiv preprint_ 

_arXiv:2405.07801_ . 

- Liu K, Zhan F, Zhang J, Xu M, Yu Y, El Saddik A, Theobalt C, Xing E and Lu S (2023c) Weakly supervised 3d open-vocabulary segmentation. _Advances in Neural Information Processing Systems_ 36: 53433–53456. 

- Liu L, Xu W, Fu H, Qian S, Yu Q, Han Y and Lu C (2022b) Akb-48: A real-world articulated object knowledge base. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 14809–14818. 

- Liu M, Zhu Y, Cai H, Han S, Ling Z, Porikli F and Su H (2023d) Partslip: Low-shot part segmentation for 3d point clouds via pretrained image-language models. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 21736–21746. 

- Liu R, Wu R, Van Hoorick B, Tokmakov P, Zakharov S and Vondrick C (2023e) Zero-1-to-3: Zero-shot one image to 3d object. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 9298–9309. 

- Liu S, Wu L, Li B, Tan H, Chen H, Wang Z, Xu K, Su H and Zhu J (2024d) Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ . 

- Liu S, Zeng Z, Ren T, Li F, Zhang H, Yang J, Li C, Yang J, Su H, Zhu J et al. (2023f) Grounding dino: Marrying dino with grounded pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ . 

- Liu S, Zhang X, Zhang Z, Zhang R, Zhu JY and Russell B (2021) Editing conditional radiance fields. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 5773–5783. 

- Liu Y, Huang B, Zhu Z, Tian H, Gong M, Yu Y and Zhang K (2024e) Learning world models with identifiable factorization. _Advances in Neural Information Processing Systems_ 36. 

- Lu G, Zhang S, Wang Z, Liu C, Lu J and Tang Y (2024) Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation. In: _European Conference on Computer Vision_ . Springer, pp. 349–366. 

- Luo J, Hu Z, Xu C, Tan YL, Berg J, Sharma A, Schaal S, Finn C, Gupta A and Levine S (2024) Serl: A software suite for sample-efficient robotic reinforcement learning. _arXiv preprint arXiv:2401.16013_ . 

- Lynch C, Wahid A, Tompson J, Ding T, Betker J, Baruch R, Armstrong T and Florence P (2023) Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ . 

- Lyu J, Bai C, Yang J, Lu Z and Li X (2024) Cross-domain policy adaptation by capturing representation mismatch. _arXiv preprint arXiv:2405.15369_ . 

- Ma YJ, Kumar V, Zhang A, Bastani O and Jayaraman D (2023a) Liv: Language-image representations and rewards for robotic control. In: _International Conference on Machine Learning_ . PMLR, pp. 23301–23320. 

- Ma YJ, Liang W, Wang G, Huang DA, Bastani O, Jayaraman D, Zhu Y, Fan L and Anandkumar A (2023b) Eureka: Humanlevel reward design via coding large language models. _arXiv preprint arXiv:2310.12931_ . 

- Ma YJ, Liang W, Wang HJ, Wang S, Zhu Y, Fan L, Bastani O and Jayaraman D (2024) Dreureka: Language model guided simto-real transfer. _arXiv preprint arXiv:2406.01967_ . 

- Ma YJ, Sodhani S, Jayaraman D, Bastani O, Kumar V and Zhang A (2022) Vip: Towards universal visual reward and 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

41 

representation via value-implicit pre-training. _arXiv preprint arXiv:2210.00030_ . 

- Majumdar A, Yadav K, Arnaud S, Ma YJ, Chen C, Silwal S, Jain A, Berges VP, Abbeel P, Malik J et al. (2023) Where are we in the search for an artificial visual cortex for embodied intelligence? _arXiv preprint arXiv:2303.18240_ . 

- Maken P and Gupta A (2023) 2d-to-3d: a review for computational 3d image reconstruction from x-ray images. _Archives of Computational Methods in Engineering_ 30(1): 85–114. 

- Mandi Z, Bharadhwaj H, Moens V, Song S, Rajeswaran A and Kumar V (2022) Cacti: A framework for scalable multitask multi-scene visual imitation learning. _arXiv preprint arXiv:2212.05711_ . 

- Mandi Z, Weng Y, Bauer D and Song S (2024) Real2code: Reconstruct articulated objects via code generation. _arXiv preprint arXiv:2406.08474_ . 

- Mandlekar A, Nasiriany S, Wen B, Akinola I, Narang Y, Fan L, Zhu Y and Fox D (2023) Mimicgen: A data generation system for scalable robot learning using human demonstrations. _arXiv preprint arXiv:2310.17596_ . 

- Matas J, James S and Davison AJ (2018) Sim-to-real reinforcement learning for deformable object manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 734–743. 

- McCarthy R, Tan DC, Schmidt D, Acero F, Herr N, Du Y, Thuruthel TG and Li Z (2024) Towards generalist robot learning from internet video: A survey. _arXiv preprint arXiv:2404.19664_ . 

- Mees O, Hermann L, Rosete-Beas E and Burgard W (2022) Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ 7(3): 7327–7334. 

- Mendonca R, Bahl S and Pathak D (2023) Structured world models from human videos. _arXiv preprint arXiv:2308.10901_ . 

- Miech A, Zhukov D, Alayrac JB, Tapaswi M, Laptev I and Sivic J (2019) Howto100m: Learning a text-video embedding by watching hundred million narrated video clips. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 2630–2640. 

- Mildenhall B, Srinivasan PP, Tancik M, Barron JT, Ramamoorthi R and Ng R (2021) Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ 65(1): 99–106. 

- Minderer M, Gritsenko A, Stone A, Neumann M, Weissenborn D, Dosovitskiy A, Mahendran A, Arnab A, Dehghani M, Shen Z et al. (2022) Simple open-vocabulary object detection. In: _European Conference on Computer Vision_ . Springer, pp. 728– 755. 

- Mirjalili R, Krawez M, Silenzi S, Blei Y and Burgard W (2023) Lan-grasp: Using large language models for semantic object grasping. _arXiv preprint arXiv:2310.05239_ . 

- Mo Y, Zhang H and Kong T (2023) Towards open-world interactive disambiguation for robotic grasping. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 8061–8067. 

- Moon S, Son H, Hur D and Kim S (2024) Genflow: Generalizable recurrent flow for 6d pose refinement of novel objects. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 10039–10049. 

- Murthy Jatavallabhula K, Iyer G and Paull L (2019) gradslam: dense slam meets automatic differentiation. _arXiv preprint arXiv:1910.10672_ . 

- Nagrani A, Seo PH, Seybold B, Hauth A, Manen S, Sun C and Schmid C (2022) Learning audio-video modalities from image captions. In: _European Conference on Computer Vision_ . Springer, pp. 407–426. 

- Nair S, Rajeswaran A, Kumar V, Finn C and Gupta A (2022) R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ . 

- Nakanishi J, Itadera S, Aoyama T and Hasegawa Y (2020) Towards the development of an intuitive teleoperation system for human support robot using a vr device. _Advanced Robotics_ 34(19): 1239–1253. 

- Nan K, Xie R, Zhou P, Fan T, Yang Z, Chen Z, Li X, Yang J and Tai Y (2024) Openvid-1m: A large-scale high-quality dataset for text-to-video generation. _arXiv preprint arXiv:2407.02371_ 

- Nasiriany S, Maddukuri A, Zhang L, Parikh A, Lo A, Joshi A, Mandlekar A and Zhu Y (2024) Robocasa: Large-scale simulation of everyday tasks for generalist robots. _arXiv preprint arXiv:2406.02523_ . 

- NDI (2024) Polaris vega xt. https://www.ndigital. com/optical-navigation-technology/ polaris-vega-xt/#. Accessed: 2024. 

- Nguyen T, Vu MN, Huang B, Van Vo T, Truong V, Le N, Vo T, Le B and Nguyen A (2023) Language-conditioned affordance-pose detection in 3d point clouds. _arXiv preprint arXiv:2309.10911_ 

- Nguyen VN, Groueix T, Salzmann M and Lepetit V (2024) Gigapose: Fast and robust novel object pose estimation via one correspondence. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 9903–9913. 

- Okamura AM, Smaby N and Cutkosky MR (2000) An overview of dexterous manipulation. In: _Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No. 00CH37065)_ , volume 1. IEEE, pp. 255–262. 

- ¨Onol A ¨O, Long P and Padır T (2019) Contact-implicit trajectory optimization based on a variable smooth contact model and successive convexification. In: _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 2447–2453. 

- Padalkar A, Pooley A, Jain A, Bewley A, Herzog A, Irpan A, Khazatsky A, Rai A, Singh A, Brohan A et al. (2023a) Open x- embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ . 

- Padalkar A, Pooley A, Jain A, Bewley A, Herzog A, Irpan A, Khazatsky A, Rai A, Singh A, Brohan A et al. (2023b) Open x- embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ . 

- Pang T (2023) _Planning, Sensing, and Control for Contactrich Robotic Manipulation with Quasi-static Contact Models_ . Massachusetts Institute of Technology. 

- Pang T, Suh HT, Yang L and Tedrake R (2023) Global planning for contact-rich manipulation via local smoothing of quasidynamic contact models. _IEEE Transactions on robotics_ . 

- Pang T and Tedrake R (2021) A convex quasistatic time-stepping scheme for rigid multibody systems with contact and friction. In: _2021 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6614–6620. 

- Patel D, Eghbalzadeh H, Kamra N, Iuzzolino ML, Jain U and Desai R (2023) Pretrained language models as visual planners for human assistance. _arXiv preprint arXiv:2304.09179_ . 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

42 

- Pavlakos G, Shan D, Radosavovic I, Kanazawa A, Fouhey D and Malik J (2024) Reconstructing hands in 3d with transformers. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 9826–9836. 

- Pertsch K, Stachowicz K, Ichter B, Driess D, Nair S, Vuong Q, Mees O, Finn C and Levine S (2025) Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ . 

- Poiesi F and Boscaini D (2022) Learning general and distinctive 3d local deep descriptors for point cloud registration. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ 45(3): 3979–3985. 

- Puig X, Ra K, Boben M, Li J, Wang T, Fidler S and Torralba A (2018) Virtualhome: Simulating household activities via programs. In: _Proceedings of the IEEE conference on computer vision and pattern recognition_ . pp. 8494–8502. 

- Qi CR, Yi L, Su H and Guibas LJ (2017) Pointnet++: Deep hierarchical feature learning on point sets in a metric space. _Advances in neural information processing systems_ 30. 

- Qian G, Li Y, Peng H, Mai J, Hammoud H, Elhoseiny M and Ghanem B (2022) Pointnext: Revisiting pointnet++ with improved training and scaling strategies. _Advances in neural information processing systems_ 35: 23192–23204. 

- Qin Y, Wu YH, Liu S, Jiang H, Yang R, Fu Y and Wang X (2022) Dexmv: Imitation learning for dexterous manipulation from human videos. In: _European Conference on Computer Vision_ . Springer, pp. 570–587. 

- Radford A, Kim JW, Hallacy C, Ramesh A, Goh G, Agarwal S, Sastry G, Askell A, Mishkin P, Clark J et al. (2021) Learning transferable visual models from natural language supervision. In: _International conference on machine learning_ . PMLR, pp. 8748–8763. 

- Radosavovic I, Xiao T, James S, Abbeel P, Malik J and Darrell T (2023) Real-world robot learning with masked visual pretraining. In: _Conference on Robot Learning_ . PMLR, pp. 416– 426. 

- Ramesh A, Pavlov M, Goh G, Gray S, Voss C, Radford A, Chen M and Sutskever I (2021) Zero-shot text-to-image generation. In: _International Conference on Machine Learning_ . PMLR, pp. 8821–8831. 

- Ramos F, Possas RC and Fox D (2019) Bayessim: adaptive domain randomization via probabilistic inference for robotics simulators. _arXiv preprint arXiv:1906.01728_ . 

- Rana K, Lee R, Pershouse D and Suenderhauf N (2025) Imle policy: Fast and sample efficient visuomotor policy learning via implicit maximum likelihood estimation. _arXiv preprint arXiv:2502.12371_ . 

- Reed S, Zolna K, Parisotto E, Colmenarejo SG, Novikov A, BarthMaron G, Gimenez M, Sulsky Y, Kay J, Springenberg JT et al. (2022) A generalist agent. _arXiv preprint arXiv:2205.06175_ . 

- Ren AZ, Dixit A, Bodrova A, Singh S, Tu S, Brown N, Xu P, Takayama L, Xia F, Varley J et al. (2023a) Robots that ask for help: Uncertainty alignment for large language model planners. _arXiv preprint arXiv:2307.01928_ . 

- Ren AZ, Govil B, Yang TY, Narasimhan KR and Majumdar A (2023b) Leveraging language for accelerated learning of tool manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 1531–1541. 

- Rohmer E, Singh SP and Freese M (2013) V-rep: A versatile and scalable robot simulation framework. In: _2013 IEEE/RSJ_ 

   - _international conference on intelligent robots and systems_ . IEEE, pp. 1321–1326. 

- Rombach R, Blattmann A, Lorenz D, Esser P and Ommer B (2022) High-resolution image synthesis with latent diffusion models. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 10684–10695. 

- Ruiz N, Li Y, Jampani V, Pritch Y, Rubinstein M and Aberman K (2023) Dreambooth: Fine tuning text-to-image diffusion models for subject-driven generation. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 22500–22510. 

- Rusu AA, Veˇcer´ık M, Roth¨orl T, Heess N, Pascanu R and Hadsell R (2017) Sim-to-real robot learning from pixels with progressive nets. In: _Conference on robot learning_ . PMLR, pp. 262–270. 

- Sajjan S, Moore M, Pan M, Nagaraja G, Lee J, Zeng A and Song S (2020) Clear grasp: 3d shape estimation of transparent objects for manipulation. In: _2020 IEEE international conference on robotics and automation (ICRA)_ . IEEE, pp. 3634–3642. 

- Schwarz K, Liao Y, Niemeyer M and Geiger A (2020) Graf: Generative radiance fields for 3d-aware image synthesis. _Advances in Neural Information Processing Systems_ 33: 20154–20166. 

- Seker MY and Kroemer O (2024) Estimating material properties of interacting objects using sum-gp-ucb. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 16684–16690. 

- Sermanet P, Ding T, Zhao J, Xia F, Dwibedi D, Gopalakrishnan K, Chan C, Dulac-Arnold G, Maddineni S, Joshi NJ et al. (2023) Robovqa: Multimodal long-horizon reasoning for robotics. _arXiv preprint arXiv:2311.00899_ . 

- Sermanet P, Ding T, Zhao J, Xia F, Dwibedi D, Gopalakrishnan K, Chan C, Dulac-Arnold G, Maddineni S, Joshi NJ et al. (2024) Robovqa: Multimodal long-horizon reasoning for robotics. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 645–652. 

- Shafiullah NMM, Paxton C, Pinto L, Chintala S and Szlam A (2022) Clip-fields: Weakly supervised semantic fields for robotic memory. _arXiv preprint arXiv:2210.05663_ . 

- Shah R, Mart´ın-Mart´ın R and Zhu Y (2023) Mutex: Learning unified policies from multimodal task specifications. _arXiv preprint arXiv:2309.14320_ . 

- Shan D, Geng J, Shu M and Fouhey DF (2020) Understanding human hands in contact at internet scale. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 9869–9878. 

- Shaw K, Bahl S and Pathak D (2023) Videodex: Learning dexterity from internet videos. In: _Conference on Robot Learning_ . PMLR, pp. 654–665. 

- Shen W, Yang G, Yu A, Wong J, Kaelbling LP and Isola P (2023) Distilled feature fields enable few-shot language-guided manipulation. _arXiv preprint arXiv:2308.07931_ . 

- Shi J, Jin Y, Li D, Niu H, Jin Z, Wang H et al. (2024) Asgrasp: Generalizable transparent object reconstruction and grasping from rgb-d active stereo camera. _arXiv preprint arXiv:2405.05648_ . 

- Shirai Y, Zhao T, Suh H, Zhu H, Ni X, Wang J, Simchowitz M and Pang T (2024) Is linear feedback on smoothed dynamics sufficient for stabilizing contact-rich plans? _arXiv preprint arXiv:2411.06542_ . 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

43 

- Shridhar M, Manuelli L and Fox D (2021) Cliport: What and where pathways for robotic manipulation. 

- Shridhar M, Manuelli L and Fox D (2023) Perceiver-actor: A multitask transformer for robotic manipulation. In: _Conference on Robot Learning_ . PMLR, pp. 785–799. 

- Shvetsova N, Kukleva A, Hong X, Rupprecht C, Schiele B and Kuehne H (2025) Howtocaption: Prompting llms to transform video annotations at scale. In: _European Conference on Computer Vision_ . Springer, pp. 1–18. 

- Silva AJ, Ramirez OAD, Vega VP and Oliver JPO (2009) Phantom omni haptic device: Kinematic and manipulability. In: _2009 Electronics, Robotics and Automotive Mechanics Conference (CERMA)_ . IEEE, pp. 193–198. 

- Silver T, Hariprasad V, Shuttleworth RS, Kumar N, Lozano-P´erez T and Kaelbling LP (2022) Pddl planning with pretrained large language models. In: _NeurIPS 2022 foundation models for decision making workshop_ . 

- Singh I, Blukis V, Mousavian A, Goyal A, Xu D, Tremblay J, Fox D, Thomason J and Garg A (2023) Progprompt: Generating situated robot task plans using large language models. In: _2023 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 11523–11530. 

- Smith L, Dhawan N, Zhang M, Abbeel P and Levine S (2019) Avid: Learning multi-stage tasks via pixel-level translation of human videos. _arXiv preprint arXiv:1912.04443_ . 

- Song CH, Wu J, Washington C, Sadler BM, Chao WL and Su Y (2023) Llm-planner: Few-shot grounded planning for embodied agents with large language models. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 2998–3009. 

- Stansfield SA (1991) Robotic grasping of unknown objects: A knowledge-based approach. _The International journal of robotics research_ 10(4): 314–326. 

- Stella F, Della Santina C and Hughes J (2023) How can llms transform the robotic design process? _Nature Machine Intelligence_ : 1–4. 

- Stoiber M, Sundermeyer M and Triebel R (2022) Iterative corresponding geometry: Fusing region and depth for highly efficient 3d tracking of textureless objects. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 6855–6865. 

- Stone A, Xiao T, Lu Y, Gopalakrishnan K, Lee KH, Vuong Q, Wohlhart P, Kirmani S, Zitkovich B, Xia F et al. (2023) Openworld object manipulation using pre-trained vision-language models. _arXiv preprint arXiv:2303.00905_ . 

- Suh HJT, Pang T and Tedrake R (2022) Bundled gradients through contact via randomized smoothing. _IEEE Robotics and Automation Letters_ 7(2): 4000–4007. 

- Suh HT, Simchowitz M, Pang T and Tedrake R (2023) How does noising data affect learned contact dynamics? . 

- Sun C, Sun M and Chen HT (2022) Direct voxel grid optimization: Super-fast convergence for radiance fields reconstruction. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 5459–5469. 

- Sundaresan P, Antonova R and Bohgl J (2022) Diffcloud: Real-to-sim from point clouds with differentiable simulation and rendering of deformable objects. In: _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 10828–10835. 

- Tan C, Sun F, Kong T, Zhang W, Yang C and Liu C (2018) A survey on deep transfer learning. In: _Artificial Neural Networks and Machine Learning–ICANN 2018: 27th International Conference on Artificial Neural Networks, Rhodes, Greece, October 4-7, 2018, Proceedings, Part III 27_ . Springer, pp. 270– 279. 

- Tang C, Huang D, Ge W, Liu W and Zhang H (2023) Graspgpt: Leveraging semantic knowledge from a large language model for task-oriented grasping. _IEEE Robotics and Automation Letters_ . 

- Tang Y, Huang W, Wang Y, Li C, Yuan R, Zhang R, Wu J and Fei-Fei L (2025) Uad: Unsupervised affordance distillation for generalization in robotic manipulation. _arXiv preprint arXiv:2506.09284_ . 

- Tatiya G, Francis J, Wu HH, Bisk Y and Sinapov J (2023) Mosaic: Learning unified multi-sensory object property representations for robot perception. _arXiv preprint arXiv:2309.08508_ . 

- Team OM, Ghosh D, Walke H, Pertsch K, Black K, Mees O, Dasari S, Hejna J, Kreiman T, Xu C et al. (2024) Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ . 

- Tedrake R (2023) Underactuated robotics. _URL https://underactuated. csail. mit. edu_ 5. 

- Todorov E (2014) Convex and analytically-invertible dynamics with contacts and constraints: Theory and implementation in mujoco. In: _2014 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 6054–6061. 

- Todorov E, Erez T and Tassa Y (2012) Mujoco: A physics engine for model-based control. In: _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, pp. 5026– 5033. 

- Torne M, Simeonov A, Li Z, Chan A, Chen T, Gupta A and Agrawal P (2024) Reconciling reality through simulation: A real-tosim-to-real approach for robust manipulation. _arXiv preprint arXiv:2403.03949_ . 

- Trivedi D, Zhang J, Sun SH and Lim JJ (2021) Learning to synthesize programs as interpretable and generalizable policies. _Advances in neural information processing systems_ 34: 25146–25163. 

- Valmeekam K, Marquez M, Olmo A, Sreedharan S and Kambhampati S (2023) Planbench: An extensible benchmark for evaluating large language models on planning and reasoning about change. In: _Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ . 

- Van Den Oord A, Vinyals O et al. (2017) Neural discrete representation learning. _Advances in neural information processing systems_ 30. 

- Vemprala S, Bonatti R, Bucker A and Kapoor A (2023) Chatgpt for robotics: Design principles and model abilities. _Microsoft Auton. Syst. Robot. Res_ 2: 20. 

- Wang B, Zhang J, Dong S, Fang I and Feng C (2024a) Vlm see, robot do: Human demo video to robot action plan via vision language model. _arXiv preprint arXiv:2410.08792_ . 

- Wang C, Chai M, He M, Chen D and Liao J (2022a) Clip-nerf: Textand-image driven manipulation of neural radiance fields. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 3835–3844. 

- Wang C, Fan L, Sun J, Zhang R, Fei-Fei L, Xu D, Zhu Y and Anandkumar A (2023a) Mimicplay: Long-horizon imitation learning by watching human play. _arXiv preprint_ 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

44 

_arXiv:2302.12422_ . 

- Wang C, Ji K, Geng J, Ren Z, Fu T, Yang F, Guo Y, He H, Chen X, Zhan Z et al. (2024b) Imperative learning: A self-supervised neuro-symbolic learning framework for robot autonomy. _The International Journal of Robotics Research_ : 02783649251353181. 

- Wang C, Mart´ın-Mart´ın R, Xu D, Lv J, Lu C, Fei-Fei L, Savarese S and Zhu Y (2020a) 6-pack: Category-level 6d pose tracker with anchor-based keypoints. In: _2020 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 10059–10066. 

- Wang C, Shi H, Wang W, Zhang R, Fei-Fei L and Liu CK (2024c) Dexcap: Scalable and portable mocap data collection system for dexterous manipulation. _arXiv preprint arXiv:2403.07788_ . 

- Wang D, Kohler C, Zhu X, Jia M and Platt R (2022b) Bulletarm: An open-source robotic manipulation benchmark and learning framework. In: _The International Symposium of Robotics Research_ . Springer, pp. 335–350. 

- Wang F, Chen Z, Wang G, Song Y and Liu H (2023b) Masked space-time hash encoding for efficient dynamic scene reconstruction. _Advances in neural information processing systems_ 36: 70497–70510. 

- Wang H, Sridhar S, Huang J, Valentin J, Song S and Guibas LJ (2019) Normalized object coordinate space for categorylevel 6d object pose and size estimation. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 2642–2651. 

- Wang L, Chen X, Zhao J and He K (2024d) Scaling proprioceptivevisual learning with heterogeneous pre-trained transformers. _arXiv preprint arXiv:2409.20537_ . 

- Wang L, Ling Y, Yuan Z, Shridhar M, Bao C, Qin Y, Wang B, Xu H and Wang X (2023c) Gensim: Generating robotic simulation tasks via large language models. _arXiv preprint arXiv:2310.01361_ . 

- Wang R, Du SS, Yang L and Kakade S (2020b) Is long horizon rl more difficult than short horizon rl? _Advances in Neural Information Processing Systems_ 33: 9075–9085. 

- Wang Y, He Y, Li Y, Li K, Yu J, Ma X, Li X, Chen G, Chen X, Wang Y et al. (2023d) Internvid: A large-scale video-text dataset for multimodal understanding and generation. _arXiv preprint arXiv:2307.06942_ . 

- Wang Y, Xian Z, Chen F, Wang TH, Wang Y, Fragkiadaki K, Erickson Z, Held D and Gan C (2023e) Robogen: Towards unleashing infinite data for automated robot learning via generative simulation. _arXiv preprint arXiv:2311.01455_ . 

- Wang Z, Lorraine J, Wang Y, Su H, Zhu J, Fidler S and Zeng X (2024e) Llama-mesh: Unifying 3d mesh generation with language models. _arXiv preprint arXiv:2411.09595_ . 

- Wen B and Bekris K (2021) Bundletrack: 6d pose tracking for novel objects without instance or category-level 3d models. In: _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 8067–8074. 

- Wen B, Mitash C, Ren B and Bekris KE (2020) se (3)-tracknet: Data-driven 6d pose tracking by calibrating image residuals in synthetic domains. In: _2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 10367–10373. 

- Wen B, Tremblay J, Blukis V, Tyree S, M¨uller T, Evans A, Fox D, Kautz J and Birchfield S (2023a) Bundlesdf: Neural 6- dof tracking and 3d reconstruction of unknown objects. In: 

_Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 606–617. 

- Wen B, Yang W, Kautz J and Birchfield S (2024a) Foundationpose: Unified 6d pose estimation and tracking of novel objects. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 17868–17879. 

- Wen C, Lin X, So J, Chen K, Dou Q, Gao Y and Abbeel P (2023b) Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ . 

- Wen C, Zhang Y, Li Z and Fu Y (2019) Pixel2mesh++: Multi-view 3d mesh generation via deformation. In: _Proceedings of the IEEE/CVF international conference on computer vision_ . pp. 1042–1051. 

- Wen J, Zhu Y, Li J, Zhu M, Wu K, Xu Z, Liu N, Cheng R, Shen C, Peng Y et al. (2024b) Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ . 

- Wikipedia Contributors (2025) 3d _reconstruction_ . URL https: //en.wikipedia.org/wiki/3D_reconstruction. Accessed: 2025-01-30. 

- Wu H, Jing Y, Cheang C, Chen G, Xu J, Li X, Liu M, Li H and Kong T (2023a) Unleashing large-scale video generative pre-training for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ . 

- Wu J, Antonova R, Kan A, Lepert M, Zeng A, Song S, Bohg J, Rusinkiewicz S and Funkhouser T (2023b) Tidybot: Personalized robot assistance with large language models. _arXiv preprint arXiv:2305.05658_ . 

- Wu P, Shentu Y, Yi Z, Lin X and Abbeel P (2023c) Gello: A general, low-cost, and intuitive teleoperation framework for robot manipulators. _arXiv preprint arXiv:2309.13037_ . 

- Wu R, Zhao Y, Mo K, Guo Z, Wang Y, Wu T, Fan Q, Chen X, Guibas L and Dong H (2021) Vat-mart: Learning visual action trajectory proposals for manipulating 3d articulated objects. _arXiv preprint arXiv:2106.14440_ . 

- Xian Z, Gkanatsios N, Gervet T, Ke TW and Fragkiadaki K (2023) Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In: _7th Annual Conference on Robot Learning_ . 

- Xiang F, Qin Y, Mo K, Xia Y, Zhu H, Liu F, Liu M, Jiang H, Yuan Y, Wang H et al. (2020) Sapien: A simulated part-based interactive environment. In: _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ . pp. 11097–11107. 

- Xiang J, Lv Z, Xu S, Deng Y, Wang R, Zhang B, Chen D, Tong X and Yang J (2024) Structured 3d latents for scalable and versatile 3d generation. _arXiv preprint arXiv:2412.01506_ . 

- Xiao T, Chan H, Sermanet P, Wahid A, Brohan A, Hausman K, Levine S and Tompson J (2022a) Robotic skill acquisition via instruction augmentation with vision-language models. _arXiv preprint arXiv:2211.11736_ . 

- Xiao T, Radosavovic I, Darrell T and Malik J (2022b) Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ . 

- Xiao X, Liu J, Wang Z, Zhou Y, Qi Y, Cheng Q, He B and Jiang S (2023) Robot learning in the era of foundation models: A survey. _arXiv preprint arXiv:2311.14379_ . 

- Xie T, Zhao S, Wu CH, Liu Y, Luo Q, Zhong V, Yang Y and Yu T (2023a) Text2reward: Automated dense reward function generation for reinforcement learning. _arXiv preprint arXiv:2309.11489_ . 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

45 

- Xie Y, Yu C, Zhu T, Bai J, Gong Z and Soh H (2023b) Translating natural language to planning goals with large-language models. _arXiv preprint arXiv:2302.05128_ . 

- Xiong H, Li Q, Chen YC, Bharadhwaj H, Sinha S and Garg A (2021) Learning by watching: Physical imitation of manipulation skills from human videos. In: _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 7827–7834. 

- Xu K, Zhao S, Zhou Z, Li Z, Pi H, Zhu Y, Wang Y and Xiong R (2023a) A joint modeling of vision-language-action for targetoriented grasping in clutter. _arXiv preprint arXiv:2302.12610_ 

- Xu M, Huang P, Yu W, Liu S, Zhang X, Niu Y, Zhang T, Xia F, Tan J and Zhao D (2023b) Creative robot tool use with large language models. _arXiv preprint arXiv:2310.13065_ . 

- Xu Z, Gao C, Liu Z, Yang G, Tie C, Zheng H, Zhou H, Peng W, Wang D, Chen T et al. (2024) Manifoundation model for general-purpose robotic manipulation of contact synthesis with arbitrary objects and robots. _arXiv preprint arXiv:2405.06964_ 

- Xu Z, Wu J, Zeng A, Tenenbaum JB and Song S (2019) Densephysnet: Learning dense physical object representations via multi-step dynamic interactions. _arXiv preprint arXiv:1906.03853_ . 

- Xue H, Hang T, Zeng Y, Sun Y, Liu B, Yang H, Fu J and Guo B (2022) Advancing high-resolution video-language representation with large-scale video transcriptions. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 5036–5045. 

- Xue L, Gao M, Xing C, Mart´ın-Mart´ın R, Wu J, Xiong C, Xu R, Niebles JC and Savarese S (2023a) Ulip: Learning a unified representation of language, images, and point clouds for 3d understanding. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 1179–1189. 

- Xue L, Yu N, Zhang S, Li J, Mart´ın-Mart´ın R, Wu J, Xiong C, Xu R, Niebles JC and Savarese S (2023b) Ulip-2: Towards scalable multimodal pre-training for 3d understanding. _arXiv preprint arXiv:2305.08275_ . 

- Yan G, Wu YH and Wang X (2024) Dnact: Diffusion guided multitask 3d policy learning. _arXiv preprint arXiv:2403.04115_ . 

- Yan S, Zhu T, Wang Z, Cao Y, Zhang M, Ghosh S, Wu Y and Yu J (2022) Videococa: Video-text modeling with zero-shot transfer from contrastive captioners. _arXiv preprint arXiv:2212.04979_ 

- Yang J, Gao M, Li Z, Gao S, Wang F and Zheng F (2023a) Track anything: Segment anything meets videos. _arXiv preprint arXiv:2304.11968_ . 

- Yang J, Mark MS, Vu B, Sharma A, Bohg J and Finn C (2024a) Robot fine-tuning made easy: Pre-training rewards and policies for autonomous real-world reinforcement learning. In: _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, pp. 4804–4811. 

- Yang L, Kang B, Huang Z, Zhao Z, Xu X, Feng J and Zhao H (2024b) Depth anything v2. _Advances in Neural Information Processing Systems_ 37: 21875–21911. 

- Yang M, Du Y, Ghasemipour K, Tompson J, Schuurmans D and Abbeel P (2023b) Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ . 

- Yang T, Jing Y, Wu H, Xu J, Sima K, Chen G, Sima Q and Kong T (2023c) Moma-force: Visual-force imitation for realworld mobile manipulation. In: _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 6847–6852. 

- Yang Y, Jia B, Zhi P and Huang S (2024c) Physcene: Physically interactable 3d scene synthesis for embodied ai. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 16262–16272. 

- Yang Z, Raman SS, Shah A and Tellex S (2023d) Plug in the safety chip: Enforcing constraints for llm-driven robot agents. _arXiv preprint arXiv:2309.09919_ . 

- Yao L, Han J, Wen Y, Liang X, Xu D, Zhang W, Li Z, Xu C and Xu H (2022a) Detclip: Dictionary-enriched visual-concept paralleled pre-training for open-world detection. _Advances in Neural Information Processing Systems_ 35: 9125–9138. 

- Yao S, Zhao J, Yu D, Du N, Shafran I, Narasimhan K and Cao Y (2022b) React: Synergizing reasoning and acting in language models. _arXiv preprint arXiv:2210.03629_ . 

- Ye S, Jang J, Jeon B, Joo S, Yang J, Peng B, Mandlekar A, Tan R, Chao YW, Lin BY et al. (2024) Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ . 

- Ye W, Zhang Y, Wang M, Wang S, Gu X, Abbeel P and Gao Y (2023a) Foundation reinforcement learning: towards embodied generalist agents with foundation prior assistance. _arXiv preprint arXiv:2310.02635_ . 

- Ye Y, Li X, Gupta A, De Mello S, Birchfield S, Song J, Tulsiani S and Liu S (2023b) Affordance diffusion: Synthesizing hand-object interactions. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 22479–22489. 

- Yoshida T, Masumori A and Ikegami T (2025) From text to motion: grounding gpt-4 in a humanoid robot “alter3”. _Frontiers in Robotics and AI_ 12: 1581110. 

- Yu C and Wang P (2022) Dexterous manipulation for multi-fingered robotic hands with reinforcement learning: A review. _Frontiers in Neurorobotics_ 16: 861825. 

- Yu T, Xiao T, Stone A, Tompson J, Brohan A, Wang S, Singh J, Tan C, Peralta J, Ichter B et al. (2023) Scaling robot learning with semantically imagined experience. _arXiv preprint arXiv:2302.11550_ . 

- Yu X, Tang L, Rao Y, Huang T, Zhou J and Lu J (2022) Point-bert: Pre-training 3d point cloud transformers with masked point modeling. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 19313–19322. 

- Yuan C, Wen C, Zhang T and Gao Y (2024) General flow as foundation affordance for scalable robot learning. _arXiv preprint arXiv:2401.11439_ . 

- Zareian A, Rosa KD, Hu DH and Chang SF (2021) Openvocabulary object detection using captions. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 14393–14402. 

- Zarrin RS, Jitosho R and Yamane K (2023) Hybrid learning-and model-based planning and control of in-hand manipulation. In: _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 8720–8726. 

- Ze Y, Liu Y, Shi R, Qin J, Yuan Z, Wang J and Xu H (2024a) H-index: Visual reinforcement learning with hand-informed representations for dexterous manipulation. _Advances in Neural Information Processing Systems_ 36. 

_Prepared using sagej.cls_ 

_Journal Title XX(X)_ 

46 

- Ze Y, Yan G, Wu YH, Macaluso A, Ge Y, Ye J, Hansen N, Li LE and Wang X (2023) Gnfactor: Multi-task real robot learning with generalizable neural feature fields. In: _Conference on Robot Learning_ . PMLR, pp. 284–301. 

- Ze Y, Zhang G, Zhang K, Hu C, Wang M and Xu H (2024b) 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In: _ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation_ . 

- Zellers R, Lu X, Hessel J, Yu Y, Park JS, Cao J, Farhadi A and Choi Y (2021) Merlot: Multimodal neural script knowledge models. _Advances in neural information processing systems_ 34: 23634– 23651. 

- Zhai X, Kolesnikov A, Houlsby N and Beyer L (2022) Scaling vision transformers. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 12104–12113. 

- Zhang C, Han D, Qiao Y, Kim JU, Bae SH, Lee S and Hong CS (2023a) Faster segment anything: Towards lightweight sam for mobile applications. _arXiv preprint arXiv:2306.14289_ . 

- Zhang H, Du W, Shan J, Zhou Q, Du Y, Tenenbaum JB, Shu T and Gan C (2023b) Building cooperative embodied agents modularly with large language models. _arXiv preprint arXiv:2307.02485_ . 

- Zhang J, Guo Y, Chen X, Wang YJ, Hu Y, Shi C and Chen J (2024a) Hirt: Enhancing robotic control with hierarchical robot transformers. _arXiv preprint arXiv:2410.05273_ . 

- Zhang J, Huang J, Jin S and Lu S (2024b) Vision-language models for vision tasks: A survey. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ . 

- Zhang J, Zhang J, Pertsch K, Liu Z, Ren X, Chang M, Sun SH and Lim JJ (2023c) Bootstrap your own skills: Learning to solve new tasks with large language model guidance. _arXiv preprint arXiv:2310.10021_ . 

- Zhang K, Lucet E, Sandretto JAD, Kchir S and Filliat D (2022a) Task and motion planning methods: applications and limitations. In: _ICINCO 2022-19th International Conference on Informatics in Control, Automation and Robotics_ . SCITEPRESS-Science and Technology Publications, pp. 476–483. 

- Zhang R, Guo Z, Zhang W, Li K, Miao X, Cui B, Qiao Y, Gao P and Li H (2022b) Pointclip: Point cloud understanding by clip. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 8552–8562. 

- Zhang X, Kundu A, Funkhouser T, Guibas L, Su H and Genova K (2023d) Nerflets: Local radiance fields for efficient structureaware 3d scene representation from 2d supervision. In: _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ . pp. 8274–8284. 

- Zhang X, Qiu W, Li YC, Yuan L, Jia C, Zhang Z and Yu Y (2024c) Debiased offline representation learning for fast online adaptation in non-stationary dynamics. _arXiv preprint arXiv:2402.11317_ . 

- Zhang Z, Zhang L, Wang Z, Jiao Z, Han M, Zhu Y, Zhu SC and Liu H (2023e) Part-level scene reconstruction affords robot interaction. In: _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, pp. 11178– 11185. 

- Zhao TZ, Kumar V, Levine S and Finn C (2023a) Learning finegrained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ . 

- Zhao W, Queralta JP and Westerlund T (2020) Sim-to-real transfer in deep reinforcement learning for robotics: a survey. In: _2020 IEEE symposium series on computational intelligence (SSCI)_ . IEEE, pp. 737–744. 

- Zhao X, Ding W, An Y, Du Y, Yu T, Li M, Tang M and Wang J (2023b) Fast segment anything. _arXiv preprint arXiv:2306.12156_ . 

- Zhao X, Li M, Weber C, Hafez MB and Wermter S (2023c) Chat with the environment: Interactive multimodal perception using large language models. _arXiv preprint arXiv:2303.08268_ . 

- Zhao Z, Cheng S, Ding Y, Zhou Z, Zhang S, Xu D and Zhao Y (2024) A survey of optimization-based task and motion planning: From classical to learning approaches. _IEEE/ASME Transactions on Mechatronics_ . 

- Zhen H, Qiu X, Chen P, Yang J, Yan X, Du Y, Hong Y and Gan C (2024) 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ . 

- Zhi S, Laidlow T, Leutenegger S and Davison AJ (2021) Inplace scene labelling and understanding with implicit scene representation. In: _Proceedings of the IEEE/CVF International Conference on Computer Vision_ . pp. 15838–15847. 

- Zhou H, Yao X, Meng Y, Sun S, BIng Z, Huang K and Knoll A (2023) Language-conditioned learning for robotic manipulation: A survey. _arXiv preprint arXiv:2312.10807_ . 

- Zhou J, Wei C, Wang H, Shen W, Xie C, Yuille A and Kong T (2021) ibot: Image bert pre-training with online tokenizer. _arXiv preprint arXiv:2111.07832_ . 

- Zhou K, Yang J, Loy CC and Liu Z (2022) Learning to prompt for vision-language models. _International Journal of Computer Vision_ 130(9): 2337–2348. 

- Zhou L, Wu G, Zuo Y, Chen X and Hu H (2024a) A comprehensive review of vision-based 3d reconstruction methods. _Sensors_ 24(7): 2314. 

- Zhou Z, Atreya P, Lee A, Walke H, Mees O and Levine S (2024b) Autonomous improvement of instruction following skills via foundation models. _arXiv preprint arXiv:2407.20635_ . 

- Zhu H, Meduri A and Righetti L (2023a) Efficient object manipulation planning with monte carlo tree search. In: _2023 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ . IEEE, pp. 10628–10635. 

- Zhu H, Zhao T, Ni X, Wang J, Fang K, Righetti L and Pang T (2024) Should we learn contact-rich manipulation policies from sampling-based planners? _arXiv preprint arXiv:2412.09743_ . 

- Zhu Y, Joshi A, Stone P and Zhu Y (2023b) Viola: Imitation learning for vision-based manipulation with object proposal priors. In: _Conference on Robot Learning_ . PMLR, pp. 1199– 1210. 

- Zhu Y, Wong J, Mandlekar A, Mart´ın-Mart´ın R, Joshi A, Nasiriany S and Zhu Y (2020) robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv:2009.12293_ . 

- Zhuang J, Wang C, Lin L, Liu L and Li G (2023) Dreameditor: Textdriven 3d scene editing with neural fields. In: _SIGGRAPH Asia 2023 Conference Papers_ . pp. 1–10. 

- Zook A, Sun FY, Spjut J, Blukis V, Birchfield S and Tremblay J (2024) Grs: Generating robotic simulation tasks from realworld images. _arXiv preprint arXiv:2410.15536_ . 

- Zuo X, Samangouei P, Zhou Y, Di Y and Li M (2025) Fmgs: Foundation model embedded 3d gaussian splatting for holistic 

_Prepared using sagej.cls_ 

_Foundation Models for Manipulation_ 

47 

3d scene understanding. _International Journal of Computer Vision_ 133(2): 611–627. 

_Prepared using sagej.cls_ 

