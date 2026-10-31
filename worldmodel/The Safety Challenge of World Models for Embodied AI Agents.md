---
title: "The Safety Challenge of World Models for Embodied AI Agents: A Review"
date: "2025-10-07"
authors: "Lorenzo Baraldi; Zifan Zeng; Chongzhe Zhang; Aradhana Nayak; Hongbo Zhu; Feng Liu"
url: https://arxiv.org/abs/2510.05865
pdf: https://arxiv.org/pdf/2510.05865
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2510.05865)** / [論文ページ](https://arxiv.org/abs/2510.05865)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **The Safety Challenge of World Models for Embodied AI Agents: A Review** 

**Lorenzo Baraldi**<sup>1</sup><sup>_∗_</sup> , **Zifan Zeng**<sup>2</sup><sup>_,_3</sup> , **Chongzhe Zhang**<sup>2</sup><sup>_,_4</sup> , **Aradhana Nayak**<sup>2</sup> , **Hongbo Zhu**<sup>5</sup><sup>_∗_</sup> , **Feng Liu**<sup>2</sup> , **Qunli Zhang**<sup>2</sup> , **Peng Wang**<sup>2</sup> , **Shiming Liu**<sup>2</sup> , 

**Zheng Hu**<sup>2</sup> , **Angelo Cangelosi**<sup>5</sup> and **Lorenzo Baraldi**<sup>6</sup> 

1University of Pisa 

2Huawei RAMS Lab 

3Technical University of Munich 

4Technical University of Berlin 

5University of Manchester 

6University of Modena and Reggio Emilia 

lorenzo.baraldi@phd.unipi.it, _{_ zifan.zeng, chongzhe.zhang, aradhana.nayak, hongbo.zhu, feng.liu1, zhangqunli1, wangpeng394, liushiming3, hu.zheng _}_ @huawei.com, _{_ angelo.cangelosi, hongbo.zhu _}_ @manchester.ac.uk, lorenzo.baraldi@unimore.it 

## **Abstract** 

The rapid progress in embodied artificial intelligence has highlighted the necessity for more advanced and integrated models that can perceive, interpret, and predict environmental dynamics. In this context, World Models (WMs) have been introduced to provide embodied agents with the abilities to anticipate future environmental states and fill in knowledge gaps, thereby enhancing agents’ ability to plan and execute actions. However, when dealing with embodied agents it is fundamental to ensure that predictions are safe for both the agent and the environment. In this article, we conduct a comprehensive literature review of World Models in the domains of autonomous driving and robotics, with a specific focus on the safety implications of scene and control generation tasks. Our review is complemented by an empirical analysis, wherein we collect and examine predictions from state-of-theart models, identify and categorize common faults (herein referred to as pathologies), and provide a quantitative evaluation of the results. 

## **1 Introduction** 

Recently, autonomous agents such as self-driving cars, humanoid robots and manipulators have been driven by the strong reasoning capability and ease of accessibility to large transformer models. However, researchers frequently try to address the questions, ‘can training data for an agent be autonomously generated?’ and ‘can an agent reason and perform complex maneuvers in dynamical scenarios?’ The common theme underlying these questions is the ability of the agent to comprehend the future evolution of its surroundings from the present state and predict the immediate outcome of its actions. Further, the recent emergence of large 

> _∗_ Work done during internship at Huawei RAMS Lab. 


Figure 1: Illustration of a World Model in the domain of autonomous driving or robotics. The current observation and conditions are used to predict future observations, on the tasks of novel scenes (yellow) or control actions (blue) generation. Our pathology criteria enable the evaluation of safety in the generated outputs for both tasks. 

language models and their unparalleled levels to linguistic comprehension has led to an increased interest in semantically driven agents. This creates a three-fold challenge. The agent must be able to 1) correctly comprehend an instruction 2) process information from its environment in order to interact with participants in it and 3) predict the outcome in the immediate future and thereby take steps to execute the instruction. To address the first two challenges, researchers have integrated multiple sources of information, derived from perceptual inputs, with the reasoning capabilities characteristic of language models leading to the creation of Multimodal Large Language Models (MLLMs) [Caffagni _et al._ , 2024]. The third challenge is addressed by so-called World Models (WMs) [Agarwal _et al._ , 2025] that have been proposed as a potential solution to estimate future environmental observations and possibly missing information. 

Although the concept of WMs is well known in control the- 

ory to learn the dynamics of an agent in static or unknown environments, recent research endeavors have significantly advanced WMs development, enabling prediction of future observations and their translation into various forms of output, including videos [Brooks _et al._ , 2024], control actions [Wang _et al._ , 2024c], or a combination of both [Hu _et al._ , 2023]. Through the training process, WMs implicitly acquire a fundamental understanding of the underlying physical laws, dynamics, and spatiotemporal continuity, which is reflected in the generated predictions. However, it is crucial to acknowledge that faulty predictions can lead to catastrophic results in embodied scenarios like autonomous driving. Therefore the focus should not solely be directed to correctly executing the task, but rather on ensuring that the predicted actions and outcomes do not compromise the safety of the agent, its environment, or other entities. 

In response to the growing research efforts aimed at constructing better World Models, this literature review undertakes a three-fold objective. Firstly, it provides a comprehensive and systematic overview of the current landscape of World Models in the field of autonomous driving and robotics. Secondly, it conducts an in-depth analysis of the safety aspects of WMs, with a focus on the tasks of scene and control generation. This analysis identifies the faults of world models, which are herein referred to as _pathologies_ , as well as it establishes qualitative criteria for their estimation. Finally, it identifies and discusses prominent future research directions for improved safety in WMs. 

This review differs from existing surveys [Zhu _et al._ , 2024; Guan _et al._ , 2024] in its focus on the safety aspect of WMs, rather than solely on their performance and taxonomy. Further, it builds on the definition proposed in [Zeng _et al._ , 2024], providing detailed analysis on both scene generation and control tasks in the domain of robotics and autonomous driving, including quantitative evaluations on the defined pathology criteria. By doing so, this review aims to provide a comprehensive understanding of the current state of World Models and their safety implications, ultimately contributing to the development of more robust and reliable WMs. 

## **2 Preliminaries on World Models** 

We define a World Model (Fig 1) as an entity which accepts the current observation of the environment from sensory modalities along with a condition as inputs and predicts future observations in a short time frame in the form of of one or more sensory modalities. Sensory inputs to the world model are images (camera) or states of a robot (joint torque sensor, cameras). The condition in natural language or a desired future observation in the form of bounding boxes in 2D (bird’s eye view with a drone) is a stimulus to change the current observation that is provided to the WM by a user or by a task organizer which dispatches goals valid for the small time frame. In what follows we discuss notable works in two broad domains of utilization of WMs: scene generation and control. Within each category, we explore two application areas: autonomous driving and robotics. 

|**Model**|**Base Model**|**Output-Resolution**<br>|**Task**|
|---|---|---|---|
|1 GAIA-1 [Hu_et al._, 2023]|D + A|(1_×_288_×_512)_×_26|AD|
|DriveDreamer [Wang_et al._, 2023]|D + A|(1_×_256_×_448)_×_32|AD|
|DriveDreamer2 [Zhao_et al._, 2024]|D + LLM|(6_×_256_×_448)_×_8|AD|
|MagicDrive [Gao_et al._, 2024b]|D|(6_×_224_×_400)_×_7|AD|
|Panacea [Wen_et al._, 2024]|D|(6_×_256_×_512)_×_8|AD|
|Drive-WM [Wang_et al._, 2024d]|D|(6_×_192_×_384)_×_8|AD|
|DrivingDiffusion [Li_et al._, 2024c]|D|(6_×_512_×_512)_×_6|AD|
|DreamForge [Mei_et al._, 2024]|D|(6_×_224_×_400)_×_7|AD|
|DriveScape [Wu_et al._, 2024]|D|(6_×_576_×_1024)_×_30|AD|
|Vista [Gao_et al._, 2024c]|D|(1_×_576_×_1024)_×_25|AD|
|MagicDriveDiT [Gao_et al._, 2024a]|D|(6_×_848_×_1600)_×_129|AD|
|AVDC [Ko_et al._, 2023]|D|(1_×_48_×_64)_×_7|R|
|EVA [Chi_et al._, 2024]|D + LLM|(1_×_256_×_256)_×_16|R|
|VideoAgent [Soni_et al._, 2024]|D|(1_×_48_×_64)_×_7|R|
|This& That [Wang_et al._, 2024a]|D|(1_×_256_×_384)_×_25|R|
|Open-Sora Plan [Lin_et al._, 2024]|D|(1_×_352_×_640)_×_93|G|
|Cosmos [Agarwal_et al._, 2025]|D + A|(1_×_704_×_1280)_×_120|G|


Table 1: A summary of world models for scene generation. Base Model indicate, D: Diffusion, A: Autoregressive. Possible tasks are AD: Autonomous Driving, R: Robotics, G: General Purpose 

### **2.1 World Models for Scene Generation** 

The scene generation task involves predicting future observations in the form of sequential video frames. WMs for scene generation typically rely on two primary generative frameworks: autoregressive or diffusion models. Autoregressive models [Hu _et al._ , 2023; Agarwal _et al._ , 2025] generate future observations in a sequential manner, conditioning each new prediction on the previous ones. In contrast, diffusion models [Gao _et al._ , 2024a; Zhu _et al._ , 2024] operate by iteratively refining a Gaussian noise signal, progressively removing noise to produce a coherent visual representation. 

In what follows, we will focus mostly on diffusion models [Dhariwal and Nichol, 2021], which have emerged as a prominent architectural framework in both the domains of autonomous driving and robotics scene generation. 

**Autonomous Driving.** GAIA-1 [Hu _et al._ , 2023], is one of the pioneering World Model for driving scene generation and it operates on two components: a WM and a video diffusion decoder. The World Model is in charge of highlevel reasoning about the subjects represented in the scenes and their dynamics. Specifically, it tokenizes multimodal inputs ( _i.e._ video, text, action) into discrete tokens and autoregressively predicts the next observation in the latent space. The diffusion decoder, instead, is in charge of rendering the video based on the generated tokens. Differently, in DriveDreamer [Wang _et al._ , 2023] the autoregressive module is only used to predict future actions, while the conditioning input is expanded to HDMap, 3D Bounding box, initial frame and textual prompt, to improve the consistency on generated video. Further, DriveDreamer2 [Zhao _et al._ , 2024] removes the autoregressive module and eliminates the need for 3D Boxes and HD Maps from real images by generating them via LLM using user prompts. Unlike methods that explicitly provide position information for objects at every moment, Vista [Gao _et al._ , 2024c] is conditioned on three initial frames, allowing the diffusion module to learn to capture the motion priors of objects and generate plausible movements. 

On the other hand, MagicDrive [Gao _et al._ , 2024b] and Panacea [Wen _et al._ , 2024] implement video generation for driving scenes with six views (front-left, front-center, front- 

right, back-left, back-center, and back-right) The generation is conditioned on both text prompts and sequences of Bird Eye Views (BEVs), and is conducted in two stages: firstly, generating multi-view images, and secondly, using these images to generate future frames. To improve the consistency and realism of objects across views in the generated video, DrivingDiffusion [Li _et al._ , 2024c] and DreamForge [Mei _et al._ , 2024] enhance the local attention to key objects. 

Differently, DriveScape [Wu _et al._ , 2024] adopts a novel approach by transforming the process of generating six views at once into a two-step procedure: first, freely generating three non-overlapping perspectives, and then considering the spatial coherence between adjacent views to generate the remaining three views. In terms of boosting the length of generated videos, MagicDriveDit [Gao _et al._ , 2024a] makes a significant contribution by converting the architecture from the original U-Net implementation to the more scalable Diffusion Transformer [Peebles and Xie, 2023] architecture, which overcomes single GPU memory constraints due to sequence parallelism. Beyond generating driving videos, DriveWM [Wang _et al._ , 2024d] applies the generated videos to the training of an autonomous driving planner and improves the planner’s capabilities in out-of-distribution scenarios. 

**Robotics.** In AVDC [Ko _et al._ , 2023], the authors introduce a WM that generates manipulator actions. Firstly a diffusion model [Dhariwal and Nichol, 2021] synthetizes a video representing the required actions that are subsequently translated in movements of the manipulator via optical flow estimation. Following this method, VideoAgent [Soni _et al._ , 2024], improves AVDC by including feedbacks of a Multimodal Large Language Model (MLLM) to refine the video generation pipeline, making it more consistent. In contrast, This&That [Wang _et al._ , 2024a] focuses on addressing the ambiguity of textual prompts in robotics diffusion model generators. This is achieved by simplifying the textual prompt to pointing gestures and words, such as put this pen on that table. The gestures are then translated to 2D coordinates in the initial frame and employed as additional conditioning for the generation process. 

An alternative approach is presented in EVA [Chi _et al._ , 2024], where an MLLM is iteratively prompted to generate a video that solves a given task, based on current observation and task description. The MLLM refines its initial video prediction through multiple iterations until task completion is achieved (which is estimated by the model itself). 

**General Purpose.** The research domain of video generation extends far beyond the specific application of robotics and driving scene generation. Cosmos [Agarwal _et al._ , 2025] comprises a family of world foundation models (including both diffusion-based and autoregressive architectures) which have been trained on a large-scale video dataset consisting of approximately 100 million clips. These models are capable of generating videos conditioned on either text-only inputs or a combination of text and previous visual observations. Further, Cosmos optimizes the latent space representation of videos, enabling more efficient and effective video generation. In a similar vein, Open-Sora Plan [Lin _et al._ , 2024] is a diffusion model generator that targets the video encoding 

|**Model**|**Base ModelI**|**nput Modalit**|**yTask**|
|---|---|---|---|
|MILE [Hu_et al._, 2022]|RNN|Im, M|AD|
|CTG++ [Zhong_et al._, 2023]|D|Tr, M, Tx|AD|
|LCTGen [Tan_et al._, 2023]|MLP|Tr, M, Tx|AD|
|GenAD [Zheng_et al._, 2024a]|RNN|Im, M|AD|
|SEM2 [Gao_et al._, 2024d]|RNN|Im, Pc|AD|
|Think2Drive [Li_et al._, 2024b]|RNN|Tr, M|AD|
|Doe-1 [Zheng_et al._, 2024b]|A|Im, Tr, Tx|AD|
|GUMP [Hu_et al._, 2024]|A|Tr, M|AD|
|BC-Z [Jang_et al._, 2022]|CNN|Im, Tx|R|
|RT-1 [Brohan_et al._, 2023]|A|Im, Tx|R|
|SayCan [Ichter_et al._, 2023]|CNN+LLM|Im, Tx|R|
|PaLM-E [Driess_et al._, 2023]|MLLM|Im, Tx|R|
|Eureka [Ma_et al._, 2024]|MLP+LLM|S, Tx|R|
|Octo [Ghosh_et al._, 2024]|CNN+A|Im, Tx|R|
|Robogen [Wang_et al._, 2024c]|MLP+LLM|S, Tx|R|
|OpenVLA [Kim_et al._, 2024]|LLM|Im, Tx|R|
|Manipulate Anything [Duan_et al._, 2024]|<br>MLLM|Im, Tx|R|


Table 2: A summary of world models for control generation. D: Diffusion, A: Autoregressive; Im: Image, Tr: Trajectory, M: Map, Pc: Pointcloud, Tx: Text, S: Simulator Environment. 

pipeline and the diffusion transformer architecture. 

### **2.2 World Models for Control** 

WMs presented in this subsection predict future observations in the form of sparse control signals. In autonomous driving, WMs can be used to control the ego vehicle in closed-loop or to control multiple background vehicles generating traffic scenarios. In robotics, WMs are used to control the agent with an initial image (encapsulating the current environmental state) and the desired goal (in the form of image/language instruction). In what follows, we describe SoTA methods for control using WM for autonomous driving and robotics. 

**Autonomous Driving.** WMs for control in autonomous driving are primarily divided into two applications: controlling the ego vehicle for closed-loop driving and generating the future trajectories of background vehicles based on the current state to create traffic scenarios. For the former, MILE [Hu _et al._ , 2022] is a model-based Imitation Learning (IL) approach with a Recurrent Neural Network (RNN) [Rumelhart _et al._ , 1988] in latent space and an encoder-decoder architecture to process vision input. MILE is the first method that realizes closed-loop autonomous driving with only visual input in urban scenarios of the Carla simulator [Dosovitskiy _et al._ , 2017]. Think2Drive [Li _et al._ , 2024b] adopts a Recurrent State-Space Model (RSSM) [Hafner _et al._ , 2019] instead of the RNN, to predict the transition of environment states in latent space for the planner to give control signals. The improved method is the first model that successfully completes all 39 challenging scenarios in Carla Leaderboard v2. On the other hand, GenAD [Zheng _et al._ , 2024a] and SEM2 [Gao _et al._ , 2024d] utilize Gated Recurrent Unit (GRU) [Cho _et al._ , 2014] to predict the future states in the latent space. The difference is that GenAD uses self- and cross-attention mechanisms to process temporal and multimodal information, whereas SEM2 proposes to train a semantic latent filter to mask out the irrelevant information in the latent space. With the introduction of the transformer, Doe-1 [Zheng _et al._ , 2024b] considers closed-loop autonomous driving as a nexttoken generation problem and trains a multi-modal autoregressive transformer to generate tokens for the tasks of visual 

question answering, action-conditioned video generation, and end-to-end motion planning as a unified framework. 

In traffic scenario generation, CTG++ [Zhong _et al._ , 2023] trains a diffusion model to sample the trajectory of vehicles from Gaussian noise. To improve the controllability of the generation, a differentiable target function is introduced during the denoising process to guide the generation explicitly through SGD. With the help of LLM, the target function can be designed using natural language to describe the guidance of the generated traffic scenario. Differently, in LCTGen [Tan _et al._ , 2023] and GUMP [Hu _et al._ , 2024], transformer architecture is introduced to predict the embeddings of the states of the environment for the next few steps. Similar to CTG++, LCTGen incorporates an LLM-driven text interpreter to process language input as the condition for the traffic scenario. 

**Robotics.** WMs can be used to generate trajectories to control an embodiment such as a manipulator, a mobile base or a humanoid robot. WM predicts the pose of the endeffector of a manipulator (or generates _actions_ ) in 6-DOF space, in 1-DOF for a gripper, in 2-DOF for a mobile base, or in the joint space of a humanoid agent. In robotics, WMs have been used in context of language conditioned IL methods (also called transfer learning) such as BC-Z [Jang _et al._ , 2022] and RL methods such as MT-OPT [Kalashnikov _et al._ , 2021], wherein the focus is learning the dynamics of the embodiment along with the tasks. These methods encourage task, environment and embodiment generalizability and the research challenge is to learn from few _demonstrations_ in IL and from few trials in RL. _Demonstrations_ are robot trajectories labelled with task instructions generated by an expert through tele-operation or by kinesthetic teaching and hence, they are expensive to obtain. Furthermore in these methods, the network architecture is designed to either maximize a reward function in case of RL or to determine a policy that matches demonstration data as closely as possible in case of IL. With the ease of availability in MLLMs, there is an increased effort in recent years to train IL policies on this architecture such as Octo [Ghosh _et al._ , 2024], RT-1 [Brohan _et al._ , 2023], OpenVLA[Kim _et al._ , 2024] along with generation of massive amount of demonstration data such as Open X-Embodiment dataset [Padalkar _et al._ , 2023]. In RT-1, vision language **.** tokens are generated via CNN and a transformer outputs _action_ tokens. Octo Base (93M parameters) is trained on a large transformer, it accepts goal images instead of task instructions as inputs and performs better than RT-1 trained on Open X-Embodiment (RT-1-X) in zero shot evaluation. OpenVLA predicts end effector and gripper _actions_ by projecting visual features into language embedding space followed by an LLM backbone and it shows better generalizability compared to Octo and RT-1. 

Since the generalizability of RL approaches to new tasks is better compared to IL [Fu _et al._ , 2019] and, given excellent code generation capability of LLMs, many approaches focus on reward code generation from language instruction RoboGen [Wang _et al._ , 2024c], Eureka [Ma _et al._ , 2024], and Manipulate Anything [Duan _et al._ , 2024]. In RoboGen _demonstrations_ are generated in a simulator environment by first defining sub-tasks followed by policy generation through RL or sampling based motion planning. In 

Eureka [Ma _et al._ , 2024] reward function code is generated from simulator environment source code through an LLM and prompts. In Manipulate Anything [Duan _et al._ , 2024], subtasks are verified allowing for possible error recovery through language conditions and, a MLLM generates _action_ code through prompts and task primitives. Given a long horizon task, some approaches use LLM for task and motion planning from a vocabulary of skills or language labelled _demonstrations_ . PaLM-E [Driess _et al._ , 2023] generates sub-tasks autoregressively through multi-modal inputs to an LLM. SayCan [Ichter _et al._ , 2023] chooses the right skill sequence with an LLM from a value function space of skills with language descriptions called ‘affordance space’. Safety constraints from natural language can be possibly incorporated in this space. 

## **3 Pathologies in World Models Safety** 

Our study endeavors to address the safety limitations of World Models. To this end, we undertake a two-step approach. Firstly, we generate future observations with stateof-the-art WMs focusing on the scene generation and control tasks. Secondly, we perform a thorough analysis of the generated data, with a primary focus on identifying and categorizing anomalous scenarios, that we refer to as _pathologies_ . To facilitate this analysis, we establish a set of _pathology criteria_ to classify the faults of WMs, providing a systematic framework for future research. 

### **3.1 Experimental Settings** 

Concerning scene generation we include in our analysis WMs that were expressly designed for the generation of driving scenes, namely Panacea [Wen _et al._ , 2024], Vista [Gao _et al._ , 2024c], and MagicDriveDit [Gao _et al._ , 2024b]. Additionally, we employ Cosmos [Agarwal _et al._ , 2025] and OpenSora Plan [Lin _et al._ , 2024] as general purpose scene generators and This&That [Wang _et al._ , 2024a] for robotics scenes. General purpose and AD WMs are tasked to generate driving scenes from the nuScenes [Caesar _et al._ , 2020] validation set. In cases where models require textual prompts as condition, we prompted ChatGpt-4o-mini to generate descriptive caption based on the initial frame. Differently we prompt This&That to generate 100 scenes of the Bridge-v2 dataset [Walke _et al._ , 2023]. We follow This&That input pipeline to transform the textual task in visual coordinates. 

Regarding WMs for AD control, we select MILE [Hu _et al._ , 2022], CTG++ [Zhong _et al._ , 2023], and LCTGen [Tan _et al._ , 2023]. As traffic scenario generator, CTG++ and LCTGen take the initial frames of 100 randomly selected scenarios from the nuScenes [Caesar _et al._ , 2020] dataset and the Waymo Open Dataset [Sun _et al._ , 2020], respectively. To verify the safety of interactions between multiple vehicles controlled by MILE, we deploy the models on multiple agents within the same simulation scenario in Carla. We adopt the method proposed in [Li _et al._ , 2024a] to setup challenging scenarios and explore edge configurations of the initial states. 

In robotics control, we consider 3 SoTA models RT-1-X [Brohan _et al._ , 2023] and Octo-Base [Ghosh _et al._ , 2024] trained on Open-X dataset and, RoboGen [Wang _et al._ , 2024c]. Our choice is motivated by their different base architectures, parameters and training. The tabletop set-up for 


Figure 2: Illustration of pathologies identified in SoTA WMs for scene generation. Visual Quality (MagicDriveDit), Temporal Consistency (Open-Sora), Traffic Adherence (Comsos), Physical Conformity (Vista), Condition Consistency (This&That) 

RT-1-X, Octo is that of Bridge-v2 dataset (WidowX arm with parallel gripper) realised in a OpenAI Gym Simulator through SimplerEnv [Li _et al._ , 2024d]. For RoboGen, a Franka 7-DOF arm mounted on a mobile base, 2 finger Franka Hand parallel gripper are used and tasks are set on tabletop in PyBullet simulator. All the example tasks in Bridge-v2 provided in SimplerEnv are tested along with 10 new instruction set-up by introducing 1) positional changes in language instruction (e.g. ‘outside’ to ‘inside’) and 2) sub-tasks by altering the orientation of the manipulated object. We test RoboGen in 4 example tasks and 7 new tasks involving 1) sensitive objects (eg. laptop, phone) 2) positional language instruction such as ‘Place bottle **beside** laptop’. 

### **3.2 Pathology Criteria in WM for Scene Generation** 

**Visual Quality.** Building on the definition of VideoScore [He _et al._ , 2024], a relevant pathology criteria for generated scenes consist on assessing the representations of all the depicted subjects, verifying their clarity, shape, and color correctness. A violation of this criterion would result in blurred frame regions, unrealistic shapes and deformed objects e.g. in Fig 2 (a), wherein a truck is in an odd shape. 

**Temporal Consistency.** Temporal consistency [Liu _et al._ , 2024b] assess the preservation of subject continuity across generated frames. In details, each represented subject should maintain a consistent visual identity (shape, color, and texture) throughout the generated video, while the scene should exhibit an adequate level of dynamism (avoiding static representation). This criterion should be enforced also in case of multi-view scenes generation (e.g frontal and back cameras in autonomous driving) where subjects that leave the field of view of a camera could enter in another one in case of coherent motion. Any deviation, such as abrupt introduction, removal, or change of visual entities, constitute a violation of temporal consistency for e.g. in Figure 2 (b) the blue car abruptly appears from the back of the truck. 

**Traffic Adherence (AD only).** To ensure the generation of realistic and safe driving scenarios, it is essential that the produced scenes conform to standard traffic regulations, unless explicitly prompted to deviate from them. For instance, at intersections regulated by traffic lights, vehicles should remain 

stationary when the signal is red, and proceed when the signal turns green. Further, any vehicle maneuver, such as turning, merging, or changing lanes, should be informed by the presence of other subjects in the nearby area. A violation of the criteria is illustrated in Fig 2 (c), where a truck is depicted crossing a road with an inconsistent traffic signal sequence, specifically a red light followed by a green light. 

**Physical Conformity.** Generated scenes must adhere to the fundamental principles of physics to ensure safety. For instance, the motion of represented subjects should exhibit smooth and continuous trajectories, avoiding abrupt and anomalous movements [Huang _et al._ , 2024]. Further, the generated scenes should also adhere to the principles of gravity, avoiding floating objects and, in the event of a direct collision between two objects, the generated scene should accurately depict the resulting interactions. Violations of physical conformity criteria is illustrated in Fig 2 (d), where a car undergoes an abrupt change in its driving trajectory, modifying its orientation between the first and second frames. The third frame violates gravity: traffic lights are floating in the air. 

**Condition Consistency.** Condition consistency is concerned with assessing the degree to which generated scenes conform to the conditioning information. While current literature focus mostly on text-to-video alignment [He _et al._ , 2024], conditioning information can take various forms, including but not limited to: textual prompts, LiDAR data, images, videos, 2D/3D bounding boxes, trajectories, bird’s eye views. A violation of the criterion is illustrated in Fig 2 (e), where the user’s prompt ‘Take the red object out of the pot and put it on the left burner’ is not fulfilled. Instead, only the lid is placed on the burner without extracting the red object which is not present in the pot. 

### **3.3 Pathology Criteria in WM for Control** 

**Condition Consistency.** For robotics, we refer to two aspects of input conditioning which is applied through the user provided instruction (or prompt). The first refers to recognizing the correct articulated object amidst distractors. The second refers to task comprehension and thereby task completion through the generated control sequence. In experiments we observed that models had poor positional awareness hence failed in tasks and, also collided with nearby objects. 


Figure 3: Illustration of pathologies identified in SoTA WMs for control: RoboGen (a), Octo (b), MILE (c), (d) 

Concerning ego vehicle controller, condition consistency refers to completing the navigation task and traveling to the goal in the scenarios. Differently, for traffic scenario generation, condition consistency assess whether models can generate trajectories of the background vehicles that are consistent with the language condition. 

**Physical Conformity.** The generated policy of WM should avoid a direct impact on the embodiment in both AD and R. In R, we observe that the tested models avoid self-collision. In those trained on demonstration data, sensitive manipulation is not an implicit feature. Motion planning based on sampling approaches which are suited for navigation tasks suffer from possible collision occurrence within a time-step when used for manipulation e.g. collision of gripper and base with table in Figure 3 (a) and (b) respectively. In AD, the safetyrelevant criterion described by physical conformity is the collision with surrounding vehicles e.g. in Figure 3 (d), where the ego vehicle controlled by MILE collides into another vehicle which is controlled by another MILE instance. 

**Grasp Consistency (R only).** The generated grasp poses must respect physical characteristics of the gripper and correspond to the manipulated object. The gripper should close after the correct grasp pose and arm position are both attained. Lack of coordination leads to task failure e.g. in Fig 3 (b). 

**Traffic Adherence (AD only).** The selection criterion for the generated control trajectories that disobey traffic rules mainly focuses on the violation of driving direction and the drivable area for e.g. in Fig 3 (c), where vehicle 6 crosses the boundary between the lanes in different directions and travels into the reverse lane. 

## **4 Metrics for World Models Safety** 

**Metrics for Scene Generation.** A popular evaluation metric for World Models for scene generation consist of the Fr´echet video distance (FVD) [Unterthiner _et al._ , 2019]. However, FVD has been proven to favor frame quality against temporal realism [Ge _et al._ , 2024]. While this problematic has been addressed by employing a different feature extractor backbone, it is clear that FVD can not provide detailed insights on each of the pathology enumerated in Section 3. 

The adoption of MLLMs has recently pushed the performance of AI-generated content evaluation. Notably, [He _et_ 

_al._ , 2024] fine-tunes a MLLM to evaluate generated videos along multiple dimensions, including visual quality, temporal consistency, dynamic degree, text-to-video alignment, and factual consistency. Similarly, [Qin _et al._ , 2024] employs an MLLM to evaluate autonomous driving, robotics, and openended embodied scenes, taking into account different criteria and collecting 35k human annotations for training purposes. Differently, in [Arai _et al._ , 2024] the authors propose a pipeline to evaluate condition consistency in autonomous driving generated scene, by building an estimator module that compares the prompted driving commands with the actual generated trajectory. 

**Metrics for Control in AD.** Concerning the generation of traffic scenarios, evaluation metrics for trajectory prediction tasks are commonly used, such as Maximum Mean Discrepancy (MMD), mean Average Distance Error (mADE), mean Final Distance Error (mFDE), which are not related to safety, though. CTG++ [Zhong _et al._ , 2023] proposes to use assessment functions derived from Signal Temporal Logic (STL) formulas to calculate the violation of traffic rules, which can be adopted to measure the level of traffic adherence as introduced in Section 3. Differently, the Scenario Collision Rate (SCR) and Success Rate (SR) are mostly employed to evaluate the performance in closed-loop autonomous driving for WMs that control the ego vehicle. The former evaluates whether the vehicle driven by the WM follows physical conformity and avoids collision, and the latter indicates if the model can complete the conditioned driving task. 

**Metrics and Benchmarks for Robotics.** Most WM robotics models focus on generalization to unseen tasks, environment and embodiment through few-shot or zero-shot learning methods. There exist metrics for high-level task planning by WM agent such as LoTa-Bench, Behavior 1K, or for policy generation with RL such as Meta-world [Yu _et al._ , 2020] where focus is on condition consistency and generalization capability. SimplerEnv [Li _et al._ , 2024d] is a simulator-based assessment for both high level plans and _actions_ . The evaluation process identifies if the correct or incorrect object was moved or grasped, grasp success (grasp consistency) and finally if correct object reaches the target (both aspects of condition consistency) for a limited set of instructions. The evaluations are based on contact information, object poses and scene information provided by the simulator. ManipulateAnything [Duan _et al._ , 2024] breaks down the type of errors to perception or reasoning (high level task execution capability) and quantifies them by a human-in-loop. There is limited attention in the literature in developing metrics to evaluate all the _pathology criteria_ identified in Section 3 for arbitrary natural language tasks. 

## **5 Quantitative Results** 

**WMs for Scene Generation.** We adopt VideoScore [He _et al._ , 2024] to assess with a score 1-4 the pathologies of visual quality, temporal consistency, and condition consistency (text-to-video alignment in our experiments). Further, we score the remaining criteria ( _i.e._ physical consistency and traffic adherence) with the Qwen-72B MLLM [Wang _et al._ , 2024b] following a similar prompt of VideoScore. However, 

||**Vid**|**eoSc**|**ore**|**Qwe**|**n-72B**||
|---|---|---|---|---|---|---|
|**Model**|**V**|**TC**|**C**|**P**|**TA**|**AVG**|
|Panacea [Wen_et al._, 2024]|2.3|2.0|3.1|**3.0**|**2.7**|2.6|
|Vista [Gao_et al._, 2024c]|2.4|1.9|3.1|2.3|1.9|2.3|
|MagicDriveDiT [Gao_et al._, 2024a] <br>|**2.6 **|**2.2 **|**3.2**|2.9|2.4|**2.7**|
|This&That[Wang_et al._, 2024a]|2.2|1.8|3.0|**3.0**|-|2.5|
|Open-Sora Plan [Lin_et al._, 2024]|2.3|2.0|3.1|2.5|2.2|2.4|
|Cosmos [Agarwal_et al._, 2025]|2.3|1.9|3.1|2.9|2.5|2.5|


Table 3: Quantitative evaluation of scene generation. Visual Quality (V), Temporal Consistency (TC), and Condition Consistency (C) are estimated with VideoScore. Physical Conformity (P) and Traffic Adherence (TA) are estimated with Qwen-72B model. 

||**E**|**xample**|**s**|**New**|**Instruc**|**tions**|
|---|---|---|---|---|---|---|
|**Model**|**C-I**|**C-II**|**G**|**C-I**|**C-II**|**G**|
|Octo [Ghosh_et al._, 2024]|47.9|16.0|46.5|16|0|9.3|
|RT-1-X [Brohan_et al._, 2023]|16.5|1.7|9.1|29.3|4|14.7|
|RoboGen [Wang_et al._, 2024c]|100|50|50|100|71|14|


Table 4: Quantitative evaluation of robot control. Condition consistency C-I (moved correct object), C-II (sourced object on target) and grasp consistency: G (sourced object grasped) percentages. 

while MLLM metrics can serve as a proxy for performance, human annotation remains the most reliable method for addressing pathologies of generated scenes. The evaluation results averaged over all generated scenes are reported in Tab 3. 

Looking at the table, we have to consider the mutual influence of multiple factors: the length of the generated video, the input condition and the output resolution. Theoretically, shorter video sequences are expected to yield better results, as longer generation sequences are more susceptible to error propagation. This hypothesis is supported by the average score of 2.6 achieved by Panacea, which generates relatively short sequences of 8 frames. Conversely, models that rely solely on image frames and textual descriptions, as conditioning, may be more susceptible to performance degradation when tasked with generating longer sequences of frames compared to having additional conditioning constraint like bounding box and BEV representation. This phenomenon is particularly relevant for Vista, Open-Sora Plan, and Cosmos with averages a score of 2.3, 2.4 and 2.5 respectively. On the other hand, additional conditioning information and architectural change in MagicDriveDit favor this model in on this experimental setting. Notably, the average score of all models falls below 3, highlighting the existing gap between current performance and realistic generations (score 4). 

**WMs for Control.** We evaluate condition and grasp consistency through functions provided in SimplerEnv [Li _et al._ , 2024d]. We test Octo in 288 and RT-1-X in 119 example subtasks of the type ‘Place object1 on object2’ based on two aspects of condition consistency: C-I (moved correct object), C-II (sourced object on target) and grasp consistency: G (sourced object grasped). We also test Octo and RT-1-X in 75 new instruction sub-tasks of the type, ‘Place object1 <preposition> object2’. We observe that even if Octo performs better in pathologies considered for example tasks, in new instructions RT-1-X exceeds Octo in all parameters. For ‘Cube right of Plate’, RT-1-X successfully grasps and executes 3 of 15 sub-tasks while Octo fails. In 

11 manually evaluated tasks of RoboGen, the grasp inconsistency is due to change from parallel to suction in gripper functionality, physical consistency is violated in 45 _._ 5% of tasks (and, several times per task) as opposed to isolated occurrences in 5% for both Octo and RT-1-X. Misplaced objects (eg. lamp on floor, laptop on the table etc.) are also generated along with unnecessary sub-tasks (eg. open and close box for a task description ‘Place phone near the box’). 

## **6 Conclusions and Future Directions** 

In this article we present a literature review of World Models, with an emphasis on the safety implications of their predictions. Further, we have identified and elucidated key criteria for defining pathologies in the generation, through an analysis of future observations generated by SoTA World Models. Building on this foundation, we proceed to outline promising research directions that aim to address detected pathologies. 

**Improved Metrics.** Concerning scene generation, physical conformity has only been addressed by explicitly prompting generators to depict physics-related event [Meng _et al._ , 2024] which is not applicable to the tasks of AD and robotics where physics is an intrinsic aspect of the video. Similarly, traffic adherence has been investigated in [Qin _et al._ , 2024] where generated videos are translated to control signals, and driving actions are evaluated inside CARLA simulator. 

**Self-Improving Methods.** Recent studies have demonstrated the potential of MLLMs used as feedback for the scene generation process [Soni _et al._ , 2024], either for fine-tuning or as a refiner at inference. Further, iterative verification based on semantic metrics can improve grasp and condition consistency [Xiong _et al._ , 2024; Duan _et al._ , 2024] in robotics. 

**Neurosymbolic AI for Control Generation.** WMs for control generation could leverage rigorous symbolic logic [Sheth _et al._ , 2023] to build the guardrail of the control signals for embodied agents. The limitation in generazibilty of existing Neurosymbolic methods in unseen scenarios could be mitigated by the development of MLLM techniques, serving as a potential bridge between unstructured data and the semiformal expression of safety-related symbolic knowledge. 

**Correction in Affordance Space.** The identified pathologies in robotics arise from poor understanding of the affordance space which has been addressed for grasping consistency in [Liu _et al._ , 2024a], for physical consistency in [Huang _et al._ , 2023] by breaking down the end-to-end _action_ generation to first generating high level plans followed by low level reasoning in affordance space through value function or keypoints. 

**Reward Function Design.** In methods such as RoboGen where policy is derived through RL, the backbone predicts reward functions. However, while the high level plan for user prompt does take into account sensitivity of articulated objects, the reward function of the sub tasks is defined simply as vector norm of difference in poses. Sophisticated reward function from language such as [Ma _et al._ , 2024] offer a promising research direction. 

## **References** 

- [Agarwal _et al._ , 2025] Niket Agarwal, Arslan Ali, et al. Cosmos World Foundation Model Platform for Physical AI. _arXiv preprint arXiv:2501.03575_ , 2025. 

- [Arai _et al._ , 2024] Hidehisa Arai, Keishi Ishihara, Tsubasa Takahashi, and Yu Yamaguchi. ACT-Bench: Towards Action Controllable World Models for Autonomous Driving. _arXiv preprint arXiv:2412.05337_ , 2024. 

- [Brohan _et al._ , 2023] Anthony Brohan, Noah Brown, et al. RT-1: Robotics Transformer for Real-World Control at Scale. In _Robotics: Science and Systems_ , 2023. 

- [Brooks _et al._ , 2024] Tim Brooks, Bill Peebles, et al. Video Generation Models as World Simulators. 2024. 2024. 

- [Caesar _et al._ , 2020] Holger Caesar, Varun Bankiti, Alex H. Lang, et al. nuScenes: A multimodal dataset for autonomous driving. In _CVPR_ , 2020. 

- [Caffagni _et al._ , 2024] Davide Caffagni, Federico Cocchi, et al. The Revolution of Multimodal Large Language Models: A Survey. In _ACL Findings_ , 2024. 

- [Chi _et al._ , 2024] Xiaowei Chi, Hengyuan Zhang, et al. EVA: An Embodied World Model for Future Video Anticipation. _arXiv preprint arXiv:2410.15461_ , 2024. 

- [Cho _et al._ , 2014] Kyunghyun Cho, Bart van Merrienboer, et al. On the Properties of Neural Machine Translation: Encoder-Decoder Approaches. _arXiv preprint arXiv:1409.1259_ , 2014. 

- [Dhariwal and Nichol, 2021] Prafulla Dhariwal and Alexander Nichol. Diffusion Models Beat GANs on Image Synthesis. In _NeurIPS_ , 2021. 

- [Dosovitskiy _et al._ , 2017] Alexey Dosovitskiy, German Ros, Felipe Codevilla, et al. CARLA: An Open Urban Driving Simulator. In _CoRL_ , 2017. 

- [Driess _et al._ , 2023] Danny Driess, Fei Xia, Mehdi SM Sajjadi, et al. PaLM-E: An Embodied Multimodal Language Model. In _ICML_ , 2023. 

- [Duan _et al._ , 2024] Jiafei Duan, Wentao Yuan, et al. Manipulate-Anything: Automating Real-World Robots using Vision-Language Models. In _CoRL_ , 2024. 

- [Fu _et al._ , 2019] Justin Fu, Anoop Korattikara, et al. From Language to Goals: Inverse Reinforcement Learning for Vision-Based Instruction Following. In _ICLR_ , 2019. 

- [Gao _et al._ , 2024a] Ruiyuan Gao, Kai Chen, Bo Xiao, et al. MagicDriveDiT: High-Resolution Long Video Generation for Autonomous Driving with Adaptive Control, 2024. 

- [Gao _et al._ , 2024b] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, et al. MagicDrive: Street View Generation with Diverse 3D Geometry Control. In _ICLR_ , 2024. 

- [Gao _et al._ , 2024c] Shenyuan Gao, Jiazhi Yang, et al. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. In _NeurIPS_ , 2024. 

- [Gao _et al._ , 2024d] Zeyu Gao, Yao Mu, Chen Chen, Jingliang Duan, et al. Enhance Sample Efficiency and Robustness of End-to-End Urban Autonomous Driving via Semantic Masked World Model. _IEEE Trans. ITS_ , 2024. 

- [Ge _et al._ , 2024] Songwei Ge, Aniruddha Mahapatra, Gaurav Parmar, Jun-Yan Zhu, and Jia-Bin Huang. On the Content Bias in Fr´echet Video Distance. In _CVPR_ , 2024. 

- [Ghosh _et al._ , 2024] Dibya Ghosh, Homer Walke, Karl Pertsch, et al. Octo: An Open-Source Generalist Robot Policy. _Robotics: Science and Systems_ , 2024. 

- [Guan _et al._ , 2024] Yanchen Guan, Haicheng Liao, et al. World Models for Autonomous Driving: An Initial Survey. _IEEE Transactions on Intelligent Vehicles_ , 2024. 

- [Hafner _et al._ , 2019] Danijar Hafner, Timothy Lillicrap, Ian Fischer, et al. Learning Latent Dynamics for Planning from Pixels. In _ICML_ , 2019. 

- [He _et al._ , 2024] Xuan He, Dongfu Jiang, et al. VideoScore: Building Automatic Metrics to Simulate Fine-grained Human Feedback for Video Generation. In _EMNLP_ , 2024. 

- [Hu _et al._ , 2022] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, and Zachary Murez. Model-Based Imitation Learning for Urban Driving. In _NeurIPS_ , 2022. 

- [Hu _et al._ , 2023] Anthony Hu, Lloyd Russell, et al. GAIA1: A Generative World Model for Autonomous Driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- [Hu _et al._ , 2024] Yihan Hu, Siqi Chai, Zhening Yang, et al. Solving Motion Planning Tasks with a Scalable Generative Model. In _ECCV_ , 2024. 

- [Huang _et al._ , 2023] Wenlong Huang, Chen Wang, et al. VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models. In _CoRL_ , 2023. 

- [Huang _et al._ , 2024] Ziqi Huang, Yinan He, Jiashuo Yu, and Fan Zhang. VBench: Comprehensive Benchmark Suite for Video Generative Models. In _CVPR_ , 2024. 

- [Ichter _et al._ , 2023] Brian Ichter, Anthony Brohan, Yevgen Chebotar, et al. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. In _CoRL_ , 2023. 

- [Jang _et al._ , 2022] Eric Jang, Alex Irpan, Mohi Khansari, et al. BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning. In _CoRL_ , 2022. 

- [Kalashnikov _et al._ , 2021] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, et al. Scaling Up Multi-Task Robotic Reinforcement Learning. _CoRL_ , 2021. 

- [Kim _et al._ , 2024] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al. OpenVLA: An Open-Source VisionLanguage-Action Model. In _CoRL_ , 2024. 

- [Ko _et al._ , 2023] Po-Chen Ko, Jiayuan Mao, Yilun Du, et al. Learning to Act from Actionless Videos through Dense Correspondences. _arXiv preprint arXiv:2310.08576_ , 2023. 

- [Li _et al._ , 2024a] Changwen Li, Joseph Sifakis, et al. Rigorous Simulation-based Testing for Autonomous Driving Systems–Targeting the Achilles’ Heel of Four Open Autopilots. _arXiv preprint arXiv:2405.16914_ , 2024. 

- [Li _et al._ , 2024b] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2Drive: Efficient Reinforcement Learning by Thinking in Latent World Model for QuasiRealistic Autonomous Driving (in CARLA-v2). _arXiv preprint arXiv:2402.16720_ , 2024. 

- [Li _et al._ , 2024c] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. DrivingDiffusion: Layout-Guided Multi-view Driving Scenarios Video Generation with Latent Diffusion Model. In _ECCV_ , 2024. 

- [Li _et al._ , 2024d] Xuanlin Li, Kyle Hsu, Jiayuan Gu, et al. Evaluating Real-World Robot Manipulation Policies in Simulation. In _CoRL_ , 2024. 

- [Lin _et al._ , 2024] Bin Lin, Yunyang Ge, Xinhua Cheng, et al. Open-sora plan: Open-source large video generation model. _arXiv preprint arXiv:2412.00131_ , 2024. 

- [Liu _et al._ , 2024a] Fangchen Liu, Kuan Fang, et al. MOKA: Open-vocabulary robotic manipulation through markbased visual prompting. In _ICRA Workshops_ , 2024. 

- [Liu _et al._ , 2024b] Yaofang Liu, Xiaodong Cun, Xuebo Liu, Xintao Wang, et al. EvalCrafter: Benchmarking and Evaluating Large Video Generation Models. In _CVPR_ , 2024. 

- [Ma _et al._ , 2024] Yecheng Jason Ma, William Liang, et al. Eureka: Human-Level Reward Design via Coding Large Language Models. In _ICLR_ , 2024. 

- [Mei _et al._ , 2024] Jianbiao Mei, Yukai Ma, et al. DreamForge: Motion-Aware Autoregressive Video Generation for Multi-View Driving Scenes. _ECCV Workshops_ , 2024. 

- [Meng _et al._ , 2024] Fanqing Meng, Jiaqi Liao, Xinyu Tan, Wenqi Shao, et al. Towards World Simulator: Crafting Physical Commonsense-Based Benchmark for Video Generation. _arXiv preprint arXiv:2410.05363_ , 2024. 

- [Padalkar _et al._ , 2023] Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- [Peebles and Xie, 2023] William Peebles and Saining Xie. Scalable Diffusion Models with Transformers. In _ICCV_ , 2023. 

- [Qin _et al._ , 2024] Yiran Qin, Zhelun Shi, et al. WorldSimBench: Towards Video Generation Models as World Simulators. _arXiv preprint arXiv:2410.18072_ , 2024. 

- [Rumelhart _et al._ , 1988] David E. Rumelhart, Geoffrey E. Hinton, et al. Learning Internal representations by error propagation. In _Readings in Cognitive Science_ , 1988. 

- [Sheth _et al._ , 2023] Amit Sheth, Kaushik Roy, and Manas Gaur. Neurosymbolic Artificial Intelligence (Why, What, and How) . _IEEE Intelligent Systems_ , 2023. 

- [Soni _et al._ , 2024] Achint Soni, Sreyas Venkataraman, et al. VideoAgent: Self-Improving Video Generation. _arXiv preprint arXiv:2410.10076_ , 2024. 

- [Sun _et al._ , 2020] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, et al. Scalability in Perception for Autonomous Driving: Waymo Open Dataset. In _CVPR_ , 2020. 

- [Tan _et al._ , 2023] Shuhan Tan, Boris Ivanovic, et al. Language Conditioned Traffic Generation. In _CoRL_ , 2023. 

- [Unterthiner _et al._ , 2019] Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, et al. FVD: A new Metric for Video Generation. In _ICLR Workshops_ , 2019. 

- [Walke _et al._ , 2023] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, et al. BridgeData V2: A Dataset for Robot Learning at Scale. In _CoRL_ , 2023. 

- [Wang _et al._ , 2023] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, et al. DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving. _arXiv preprint arXiv:2309.09777_ , 2023. 

- [Wang _et al._ , 2024a] Boyang Wang, Nikhil Sridhar, Chao Feng, et al. This&That: Language-Gesture Controlled Video Generation for Robot Planning. In _ICRA_ , 2024. 

- [Wang _et al._ , 2024b] Peng Wang, Shuai Bai, Sinan Tan, et al. Qwen2-VL: Enhancing Vision-Language Model’s Perception of the World at Any Resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

- [Wang _et al._ , 2024c] Yufei Wang, Zhou Xian, et al. RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation. In _ICML_ , 2024. 

- [Wang _et al._ , 2024d] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, et al. Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving. In _CVPR_ , 2024. 

- [Wen _et al._ , 2024] Yuqing Wen, Yucheng Zhao, Yingfei Liu, Fan Jia, et al. Panacea: Panoramic and Controllable Video Generation for Autonomous Driving. In _CVPR_ , 2024. 

- [Wu _et al._ , 2024] Wei Wu, Xi Guo, Weixuan Tang, Tingxuan Huang, et al. DriveScape: Towards High-Resolution Controllable Multi-View Driving Video Generation. _arXiv preprint arXiv:2409.05463_ , 2024. 

- [Xiong _et al._ , 2024] Chuyan Xiong, Chengyu Shen, Xiaoqi Li, et al. Autonomous Interactive Correction MLLM for Robust Robotic Manipulation. In _CoRL_ , 2024. 

- [Yu _et al._ , 2020] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, et al. Meta-World: A Benchmark and Evaluation for Multi-Task and Meta Reinforcement Learning. In _CoRL_ , 2020. 

- [Zeng _et al._ , 2024] Zifan Zeng, Chongzhe Zhang, et al. World Models: The Safety Perspective. In _ISSREW_ , 2024. 

- [Zhao _et al._ , 2024] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, et al. DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation. _arXiv preprint arXiv:2403.06845_ , 2024. 

- [Zheng _et al._ , 2024a] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, et al. GenAD: Generative End-toEnd Autonomous Driving. In _ECCV_ , 2024. 

- [Zheng _et al._ , 2024b] Wenzhao Zheng, Zetian Xia, et al. Doe-1: Closed-Loop Autonomous Driving with Large World Model. _arXiv preprint arXiv:2412.09627_ , 2024. 

- [Zhong _et al._ , 2023] Ziyuan Zhong, Davis Rempe, Yuxiao Chen, Boris Ivanovic, et al. Language-Guided Traffic Simulation via Scene-Level Diffusion. In _CoRL_ , 2023. 

- [Zhu _et al._ , 2024] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, et al. Is Sora a World Simulator? A Comprehensive Survey on General World Models and Beyond. _arXiv preprint arXiv:2405.03520_ , 2024. 

