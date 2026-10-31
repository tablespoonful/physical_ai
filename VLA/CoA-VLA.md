---
title: "CoA-VLA: Improving Vision-Language-Action Models via Visual-Text Chain-of-Affordance"
date: "2025"
venue: "ICCV 2025"
url: https://openaccess.thecvf.com/content/ICCV2025/html/Li_CoA-VLA_Improving_Vision-Language-Action_Models_via_Visual-Text_Chain-of-Affordance_ICCV_2025_paper.html
pdf: https://openaccess.thecvf.com/content/ICCV2025/papers/Li_CoA-VLA_Improving_Vision-Language-Action_Models_via_Visual-Text_Chain-of-Affordance_ICCV_2025_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/ICCV2025/papers/Li_CoA-VLA_Improving_Vision-Language-Action_Models_via_Visual-Text_Chain-of-Affordance_ICCV_2025_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/ICCV2025/html/Li_CoA-VLA_Improving_Vision-Language-Action_Models_via_Visual-Text_Chain-of-Affordance_ICCV_2025_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This ICCV paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **CoA-VLA: Improving Vision-Language-Action Models via Visual-Textual Chain-of-Affordance** 

Jinming Li<sup>1,*,</sup><sup>_ω_</sup> , Yichen Zhu<sup>2,†,</sup><sup>_ω_</sup> , Zhibin Tang<sup>_ω_</sup> , Junjie Wen<sup>3,</sup><sup>_ω_</sup> , Minjie Zhu<sup>3,</sup><sup>_ω_</sup> , Xiaoyu Liu<sup>1,</sup><sup>_ω_</sup> , Chengmeng Li<sup>1,</sup><sup>_ω_</sup> , Ran Cheng<sup>2</sup> , Yaxin Peng<sup>1,†,</sup><sup>_ω_</sup> , Yan Peng<sup>1</sup> , Feifei Feng<sup>2</sup> 

- 1Shanghai University, 2Midea Group, 3East China Normal University 

   - Co-first author, † Corresponding Author, _ω_ Core Contributor 


Figure 1. This figure illustrates the overall framework of our CoA-VLA model, which empowers vision-language-action models with chain-of-thought reasoning capabilities for generalizable visuomotor policy learning. We achieve this by designing four distinct types of affordance and introducing a novel visual-text co-injection method to integrate this knowledge into the decision-making process. 

## **Abstract** 

_Robot foundation models, particularly Vision-LanguageAction (VLA) models, have garnered significant attention for their ability to enhance robot policy learning, greatly improving robot’s generalization and robustness. OpenAI’s recent model, O1, showcased impressive capabilities in solving complex problems by utilizing extensive reasoning chains. This prompts an important question: can robot models achieve better performance in multi-task, complex environments by reviewing prior observations and then providing task-specific reasoning to guide action prediction? In this paper, we introduce_ **_Chain-of-Affordance (CoAVLA)_** _, a novel approach to scaling robot models by incor-_ 

_porating reasoning in the format of sequential robot affordances to facilitate task completion. Specifically, we prompt the model to consider the following four types of affordances before taking action: (1) object affordance — what object to manipulate and where it is; (2) grasp affordance — the specific object part to grasp; (3) spatial affordance — the optimal space to place the object; and (4) movement affordance — the collision-free path for movement. We further transform each affordance into two prompting formats:_ **_visual affordance and textual affordance_** _. We introduce a novel vision-language co-injection module that integrates this knowledge into the policy network. This allows the robot to leverage essential contextual information during action inference, resulting in improved precision and ro-_ 

9759 

_bustness. Our experiments demonstrate that CoA-VLA outperforms state-of-the-art robot foundation models, including OpenVLA and Octo, on a variety of tasks. Furthermore, CoA-VLA exhibits strong generalization capabilities, including recognizing unseen object poses, identifying free space, and avoiding obstacles in novel environments._ 

## **1. Introduction** 

Recent advancements in Vision-Language-Action (VLA) models have shown that training with internet-scale data can empower end-to-end policy learning models to outperform non-VLA models. However, current approaches often rely heavily on high-level planning or task decomposition by off-the-shelf Large language models(LLMs) or Vision language models (VLMs), limiting models from developing implicit reasoning on their own. OpenAI’s recent O1 model has demonstrated that LLMs can improve performance on complex tasks through extensive reasoning chains. If this reasoning capability can be applied to the control model, it could enhance their action robustness and generalizability. Yet, the exploration of self-driven reasoning in robotics remains under-explored, highlighting an important frontier for future research. 

In this work, we propose **Chain-of-Affordance** , namely **CoA-VLA** , a novel perspective on generalizing model reasoning at test-time, and leverage such generated reasoning to facilitate the policy learning process. Our model builds upon the DiffusionVLA [46], a state-of-the-art VLM model combining autoregression and diffusion objectives. Our method leverages visual affordance in robot learning, conceptualizing various actions and interactions with objects or the environment that a robot can perform based on visual contexts. We consider four types of affordance that are critical for robots to understand their observational surroundings to interact effectively with objects and achieve tasks in dynamic: 

1) **Object affordance** . When a user provides vague instructions, the robot should be capable of identifying the target object for interaction and its location within the view. 

2) **Grasp affordance** . It involves the robot assessing the object’s most appropriate points or surfaces to enable secure and stable handling. 

3) **Spatial affordance** . The robot needs to identify a set of coordinates that satisfy relationships described in language, such as free space for placement. 

4) **Movement affordance** . Identifying a trajectory for the robot to move without collision is crucial in the real world to avoid catastrophic damage. 

These four affordances form a sequential chain, requiring the robot to possess prior knowledge at each step to advance to the next. Specifically, at test time, the robot must first understand “what to manipulate and where the object 

is located.” Next, it determines “how to grasp the object and finally”, “where to place it,” all while following a trajectory that ensures safe task completion. During inference, the affordance chain is progressively generated as the action state evolves, avoiding unnecessary computational costs associated with outputting extensive language. We introduce two formats for chain-of-affordance reasoning: text-based and image-based chain-of-affordance prompting. Our model’s architecture natively supports text prompting integration, but image prompting requires adaptation. To address this, we developed an image affordance injection module that seamlessly integrates visual affordances into the policy network. Once generated by the model, this affordance knowledge is reused in policy learning, enabling the model to produce robust and generalizable actions. 

We conduct extensive experiments on both simulated benchmarks and real-world tasks. Specifically, on the LIBERO [30] benchmark, our proposed CoA-VLA outperforms several other state-of-the-art approaches, including the Diffusion Policy [10], Octo [36], and OpenVLA [22]. Due to the substantial sim-to-real gap, many existing studies also evaluate real robots. We set up seven real-world robot tasks, including long-horizon and challenging tasks such as serving tea, cleaning garbage, and wiping tables. We perform multi-task learning on these real-world tasks and demonstrate that the VLA model, enhanced by chainof-affordance reasoning, successfully handles most of these complex tasks with a high average success rate. Furthermore, CoA-VLA exhibits strong generalization capabilities to handle unseen object poses, adjust motion when obstacles appear, and identify free space for placement. 

The core contribution of our work lies in a novel framework that enhances vision-language-action (VLA) models by integrating affordance-aware reasoning. Central to this framework is a new module designed to strategically infuse affordance knowledge into policy learning, enabling robots to better ground actions in physical and contextual understanding. While our approach draws inspiration from prior studies on affordance, the synthesis of these concepts with VLA systems represents a significant advancement. Specifically, our framework uniquely combines these components to forge more robust, interpretable, and generalizable robotic policies, addressing critical limitations in existing VLA systems that often overlook the role of object affordances in decision-making. 

## **2. Related Works** 

**Affordance in robotics.** In robot learning, the concept of affordance is interpreted in various ways. Typically, affordance is defined as the functions of an object, encompassing what the object is, how it can be manipulated, and its spatial relationship to the target. This concept extends beyond visual properties, linking observations directly to actions. The 

9760 

efficacy of affordance prediction has been shown by many learning-based manipulation methods for 6-DoF grasping [12, 13, 42] and stable object placement. It can also represented in many ways [6, 17, 18, 27, 31, 33, 34, 50, 53] such as part segmentation, dense image feature descriptors and keypoints. Some methods leverage human videos to obtain affordances [2], while others use vision-language models (VLMs) to predict points representing spatial affordances [9, 51]. RT-Affordance [35] employs more descriptive affordance representations, and TraceVLA [1] incorporates visual traces as additional input to enhance VLA. Our approach introduces multiple types of affordances and formulates them as chain-of-thought reasoning to further improve VLA model performance. 

**Reasoning for language and control.** Prompting large language models (LLMs) with ”think step-by-step” [45] has significantly advanced their ability to solve complex tasks. Numerous approaches [3, 55] have since been developed to encourage deeper reasoning in LLMs, such as Tree-of-Thought [49] and Chain-of-Code [24], establishing this as a standard practice in language modeling. Recent research has leveraged LLMs and vision-language models (VLMs) [11, 14–17, 17, 27] as high-level planners in robotics, often using fine-tuned, open-source models or closed-source LLMs alongside policy networks for lowlevel task execution. These studies illustrate that detailed reasoning can enhance low-level control. ECoT [52] introduces a reasoning strategy for VLMs that includes task decomposition, subtask descriptions, fine-grained movement instructions, gripper positioning, and object tracking on the table. CoT-VLA [54] generates sub-goa for autoregressive VLA to guide action. Unlike existing approaches, our work introduces an affordance taxonomy (categorized into four types) to unify textual and visual affordance representations in robot learning. Coupled with a dynamic selection mechanism, this taxonomy enables adaptive policy training, where task-relevant affordances are prioritized at each timestep. The resultant framework achieves computationally efficient reasoning while retaining robustness to environmental ambiguities. 

## **3. Preliminary on Vision-Language-Action Models** 

Our work builds upon Vision-Language-Action (VLAs) as the backbone for our chain-of-affordance policies. VLAs employ a straightforward policy-learning approach: beginning with a pre-trained vision-language model, they finetune it to predict the next robot action _a_ based on the current image observation _I_ , task instruction _T_ , and reasoning _r_ . There are two types of VLAs: autoregressive VLAs [1, 8, 22, 29, 37, 39, 52] and diffusionVLAs [7, 26, 46, 47]. The former uses discrete action tokens within the vision- 

language model’s vocabulary, enabling action generation similar to language modeling through next-token prediction. The latter leverages a policy head [5, 6, 28], such as a diffusion policy [25, 47] or flow matching [7], to output continuous robot actions. 

In this work, we employ the recently released DiVLA [46] model, which integrates the Qwen2-VL [44] vision-language model with a diffusion model head for action prediction. In the following sections, we will discuss how we improve this VLA by enabling it to reason through robot affordances before selecting an action. 

## **4. Methodology** 

This section introduces our approach to explicitly leveraging affordance as a foundation for the robot models. In Section 4.1, we formally define the concept of chain of affordance as a structured sequence of affordances, each representing an actionable insight. We provide detailed descriptions of four distinct types of affordances that together constitute this chain, explaining how each type contributes to understanding and executing complex tasks. In Section 4.2, we present two formats for representing the chain of affordances: a text format and an image format. We then discuss how these representations can be integrated into the policy learning process. Finally, in Section 4.3, we outline the pipeline used to automatically generate large-scale chain-of-affordance data. 

### **4.1. Definition of Chain-of-Affordance** 

Given a dataset _D_ = _{_ ( _ω_ 1 _, g_ 1) _, . . . ,_ ( _ωN , gN_ ) _}_ consisting of _N_ expert demonstrations, where each demonstration _ωi_ is paired with a task description _gi_ in natural language. Each task description _g →G_ specifies a composition of multiple sub-tasks, and each demonstration _ωi_ is represented by a sequence of observations. We define _z →Z_ as the affordance-based reasoning in natural language that guides the task. The model decomposes _z_ into four components, _z_ = _{zobj, zgrasp, zspat, zmove}_ , where _zobj, zgrasp, zspat,_ and _zmove_ represent object, grasp, spatial, and movement affordances, respectively. Our objective is to learn an intermediate language output _z_ : _O ↑G ↓Z_ that maps observations and task descriptions to affordance reasoning in natural language. This intermediate output provides specific guidance for action generation, enabling the generation of low-level actions _a →A_ . Note that low-level actions are generated conditioned on the demonstration, task description, and affordance reasoning: _a ↔ p_ ( _a|ω, g, z_ ). 

**Details for diverse robot affordance.** In our approach, we model the robot affordance in the format of natural language as intermediate outputs. We will give detailed description on each type of affordance. 

**_Object affordance:_** Object affordance equips robots with the foundational ability to autonomously determine which 

9761 


Figure 2. **An example of the chain-of-affordance for the PourTea task.** The first row presents the text affordance and the second row shows the visual affordance. By employing a dynamic affordance selection mechanism, our method avoids generating redundant affordances at every timestep. 

object to interact with and where it is located, particularly in scenarios where user instructions lack explicit spatial or semantic details. This capability bridges the gap between ambiguous queries (e.g., “Pour the drink”) and actionable execution by enabling the robot to: 1) Identify the target object through natural language grounding (e.g., resolving “drink” to “teapot”), 2) Localize the object within its environment using pixel-aligned bounding box predictions. In our framework, object affordance is operationalized through two tightly coupled components: 1) **Semantic identification** : Resolving object names from free-form language input, and 2) **Spatial grounding** : Predicting the object’s 2D location via visual scene understanding. By integrating these capabilities, the robot establishes a contextual foundation for downstream decision-making, ensuring interactions are both intention-aware (aligned with user goals) and environmentally grounded (physically feasible). 

**_Grasp affordance:_** Grasp affordance encompasses the possible functions or ways an object can be manipulated. This affordance goes beyond visual characteristics, linking observations directly to actions, and is crucial for tasks requiring 6-DoF (degrees of freedom) grasping [18, 34, 43]. Prior work has demonstrated the effectiveness of affordance prediction for stable object handling and placement. Representations of grasp affordance vary, including part segmentation or keypoints. In our work, we use a set of 2D points to represent the grasping point for an object. 

**_Spatial affordance:_** Spatial affordance centers on a robot’s ability to interpret and reason about spatial relationships within 3D environments, enabling tasks such as identifying collision-free regions for object placement or navigation. For instance, RoboPoint [51] locates free space, and SpatialVLM [9] predicts spatial relations quantitatively and qualitatively. In our framework, spatial affordance is operationalized as actionable destinations—discrete 2D coordinates representing feasible interaction zones. 

**_Movement affordance:_** Movement affordance defines the trajectory a robot can follow during a task. This path may change depending on environmental factors, such as obstacles introduced along an intended trajectory. By modeling movement affordance, we provide the robot with adaptable paths for action, allowing it to respond dynamically to environmental changes and complete its task effectively. These affordances collectively enable the robot to understand and act upon various elements within its operational space, enhancing its interaction capabilities and responsiveness. 

**Dynamic affordance selection.** Our proposed method formulates affordances as combined text and visual prompts. While this approach offers benefits, it introduces additional computation at test time, potentially slowing down the algorithm. We observe that it’s unnecessary to utilize all available affordances during testing. For example, once an object is picked up, predicting its object affordance and the grasp affordance becomes redundant. The specific affordances required in a given sub-step depend on the task’s progress and the environment. Therefore, we implement dynamic affordance selection, adaptively choosing the necessary affordances at both training and test times to reduce computational cost. Several methods can achieve this, such as gradient-based selection [48]. Our approach prioritizes simplicity by leveraging proprioception. Proprioception refers to information about the robot’s state, including joint angles and other movement data. We transform this proprioceptive data into a single token and concatenate it with the visual token before feeding it into the large language model. Training on large-scale annotated datasets like Droid [21] enables our model to intelligently select relevant affordances at each time step. This is straightforward for the model to learn. For instance, if the proprioceptive state indicates a partially closed gripper and the wristmounted camera detects an object, the model can infer that 

9762 

the object and grasp affordances are likely unnecessary. Instead, it can focus on the movement affordance to guide the action trajectory and the spatial affordance to determine a suitable placement location. We found this strategy to be simple and useful, reducing the model’s computational cost without hurting performance. 

### **4.2. Formatting of Visual-Textual Chain-ofAffordance** 

In this section, we present a multimodal chain-ofaffordance framework that formalizes affordance reasoning through two complementary representations: (1) **textual affordance** , which provides a structured, language-driven representation of actionable possibilities (e.g., “graspable handle” or “navigable path”), and (2) **visual affordance** , which delivers a spatially grounded, scene-aware perspective via pixel-aligned cues. While the textual format enables explicit semantic reasoning, the visual modality enhances interpretability in visually dense or ambiguous environments by grounding affordances in observable scene geometry. 

To unify these modalities, we introduce a visuallanguage co-injection module that dynamically aligns and integrates visual affordance prompts in a shared parameter space. This module bridges the gap between abstract language-based reasoning and pixel-level visual context, enabling the policy model to synergistically leverage both modalities for robust, context-aware action generation. 

**Textual affordance.** Natural language serves as the predominant modality for representing visual affordances due to its semantic richness and compatibility with human-AI interaction. For instance, object affordances can be encoded as coordinate pairs (e.g., bounding boxes localizing a ”graspable cup”), while spatial affordances are expressed as coordinate pairs defining navigable regions (e.g., ”reachable shelf area”). Figure 2 (top) illustrates how diverse affordances (e.g., ”movable,” ”stackable”) are mapped to natural language descriptors.To avoid rigid linguistic templates that might bias policy learning, we employ ChatGPT to dynamically paraphrase affordance descriptions with varied syntactic structures and vocabulary (e.g., alternating between ”placeable surface” and ”flat area for stacking”). This strategy, analogous to data augmentation in NLP, enhances the model’s robustness to linguistic variability while preserving its conversational fluency. 

**Visual affordance.** Inspired by visual prompting methods that enhance model interpretability, we propose visual affordance augmentation—a technique that augments natural language affordance descriptions with direct, pixelaligned visual cues. This approach encodes affordances by overlaying coordinate markers (e.g., bounding boxes, interaction points) or motion trajectories onto the robot’s historical observation frames (Figure 2, bottom). These annota- 

tions act as chain-of-affordance prompts, visually grounding the model’s understanding of actionable properties like ”graspable” or ”navigable” within the scene’s geometry. By embedding affordances directly into the visual input, we create an explicit structure that bridges the gap between abstract language and actionable visual context.For movement affordances, we employ thin, low-saliency trajectories to avoid overshadowing critical scene elements while guiding motion planning. Conversely, key interaction zones — such as grasping points, object bounding boxes, and spatial affordances — are rendered with thicker, high-contrast overlays (e.g., semi-transparent colors) to ensure visual salience without occluding environmental context. This hierarchical visual encoding distinguishes affordance types at a glance, enabling the model to prioritize task-relevant cues while maintaining computational efficiency. 

**Visual-textual co-injection.** To integrate visual and textual affordances into action generation, we design a unified embedding pipeline that seamlessly fuses both modalities into the diffusion policy. For textual affordances, we use the last embedding from the VLM models and add an MLP layer to tokenize it. Concurrently, visual affordances are processed into patch tokens via a pretrained Vision Transformer (ViT-Small). The fused tokens are then processed by two standard Transformer blocks, balancing computational efficiency with sufficient expressive power for crossmodal reasoning. The encoder’s output embeddings are projected into the diffusion model using FiLM conditioning layers, inspired by MT-ACT [4]. This conditioning dynamically modulates the diffusion process by injecting affordance-aware features, enabling the policy to generate actions that respect both spatial constraints and semantic intent. By unifying affordance modalities early in the pipeline, our method retains the computational efficiency of standard diffusion frameworks while enhancing robustness. The FiLM-based conditioning acts as a bottleneck, distilling only the most salient affordance cues to guide action generation, thereby avoiding overfitting to redundant visual or linguistic signals. 

### **4.3. Generating Chain-of-Affordance Data** 

To prevent overfitting on affordance diversity, generating large-scale, high-quality data is crucial. While the standard approach typically relies on direct human labeling, this method is both costly and labor-intensive. Therefore, in this section, we outline a comprehensive pipeline for automatically generating diverse affordances using a range of tools to streamline the data generation process. 

Our pipeline begins with GPT-4o [38], which generates a detailed description of the scene and identifies relevant entities from the language instructions. This allows us to create contextually rich, entity-specific affordances tailored to the task at hand. Using these entities, we leverage Ground- 

9763 


Figure 3. **Robot setup and examples for real-world manipulation tasks.** We evaluate seven real-world tasks on Franka robot arm equipped with two external Zed cameras and a Realsense 435i wrist camera. 

Table 1. **Experimental results for multi-task learning.** Our method achieved the best performance in both the in-distribution test setup and under visual changes. 

|**Model**_\_**Tasks**|||Seven Task<br>In|s on Franka Ro<br>-Distribution|bot Arm||||
|---|---|---|---|---|---|---|---|---|
||CleanTrash|PourTea|NailHammer|PlaceBread|PlaceCar|WipeWater|HangCup|Avg.|
|Diffusion Policy [10]|4/11|0|8/11|3/11|9/11|2/11|7/11|33/77 (42.93%)|
|Octo [36]|4/11|0/11|7/11|4/11|8/11|3/11|8/11|34/77 (44.13%)|
|OpenVLA [22]|4/11|0/11|9/11|6/11|9/11|5/11|9/11|52/77 (54.89%)|
|DiffusionVLA [46]|**10/11**|6/11|**10/11**|7/11|**10/11**|6/11|**10/11**|59/77 (76.60%)|
|**CoA-VLA**|**10/11**|**8/11**|9/11|**10/11**|**10/11**|**9/11**|**10/11**|**64/77 (85.54%)**|
|**Model**_\_**Tasks**|CleanTrash|PourTea|Visu<br>NailHammer|al Generlizatio<br>PlaceBread|n<br>PlaceCar|WipeWater|HangCup|Avg.|
|Diffusion Policy [10]|0/9|0/9|0/9|0/9|3/9|0/9|0/9|3/63 (4.76%)|
|Octo [36]|0/9|0/9|3/9|0/9|4/9|2/9|3/9|12/63 (19.05%)|
|OpenVLA [22]|3/9|0/9|0/9|4/9|4/9|3/9|0/9|14/63 (22.22%)|
|DiffusionVLA [46]|2/9|2/9|5/9|5/9|**5/9**|3/9|6/9|28/63 (44.44%)|
|**CoA-VLA**|**4/9**|**4/9**|**6/9**|**6/9**|**5/9**|**4/9**|**7/9**|**36/63 (57.14%)**|


ing DINOv2 [32] and SAM [23, 40] to produce bounding boxes around each identified object within the scene. SAM initially provides masks, which we convert into bounding boxes, and we finalize these by taking out the intersection over union (IoU) between the outputs of Grounding DINOv2 and SAM. This IoU-based refinement ensures that bounding boxes are accurately aligned with object contours. At this stage, we also capture the gripper’s position for subsequent affordance calculations.To represent spatial affordance, we integrate RoboPoint [51], a state-of-the-art model that predicts spatial affordances directly within the image. 

Additionally, we prompt GPT-4o to annotate spatial points based on the scene context. The spatial predictions from RoboPoint and GPT-4o are then combined, after which we cluster these points to form a coherent representation, eliminating any outliers to maintain accuracy. This process captures spatial affordances that are not only visually aligned but contextually relevant.For capturing movement trajectories, we employ CoTracker [19, 20], an advanced transformer-based tracking model. CoTracker enables us to follow the robot gripper’s path, recording its movement through the scene and gathering essential trajectory data. 

9764 

This movement data provides insight into how the robot interacts dynamically with the environment, adding temporal dimensions to our affordance representation. The combination of spatial affordances, grasping points, and movement trajectories enables us to model a rich, multi-faceted affordance landscape for each scenario. This automated, tool-assisted pipeline produces a detailed and diverse set of affordance annotations, significantly reducing the need for manual labeling. 

## **5. Experiments** 

The objective of our experimental evaluations is to assess the efficacy of CoA-VLA as a reasoning framework that augments the policy-learning capabilities of a baseline robot foundation model. Specifically, we seek to address the following questions: 1) Does the VLA model demonstrate improved performance with the integration of CoA in realworld experiments? 2) What is the performance of CoAVLA in simulation benchmarks? 3) How effectively does CoA-VLA generalize to challenging scenarios? 4) How important is our proposed visual-textual affordance approach, compared to the vanilla VLA? We will give a detailed analysis in this section. Note that some experiments are presented in the Appendix due to limited space. 

### **5.1. Evaluation on Real Robot** 

**Experimental setup.** We conduct evaluations using the 6- DoF Franka robot arm, a widely adopted setup for assessing generalizable robot policies. Our setup includes two thirdperson cameras (ZED cameras) positioned on either side of the robot arm, as well as an egocentric camera (Realsense D435i) mounted on the wrist. We design seven challenging tasks, such as pouring tea and cleaning the table, incorporating both short-horizon and long-horizon tasks to test the adaptability of our approach. We illustrate our robot setup and tasks with examples in Figure 3. Detailed descriptions of each task and the experimental setup, and our ablation experiments are provided in the Appendix. 

**Train data.** We use the Droid dataset [21] as an external data source, filtering out samples without language annotations, leaving 39K trajectories. Our pipeline generates synthetic chain-of-affordance data for pre-training. The model is then post-trained on 692 trajectories across seven tasks. 

**Baseline.** We compare CoA-VLA with Diffusion Policy [10], Octo [36], OpenVLA [22], TinyVLA [47], DiffusionVLA [46]. The latter three methods are all visionlanguage-action models that achieve state-of-the-art performance in the real world. Notably, the DiffusionVLA is the same model our approach is built upon, but trained with vanilla reasoning instead of our proposed chain-ofaffordance. To ensure a fair comparison, all models are finetuned on the same dataset we use for training our approach. All models are trained with the same number of iterations, 

and the last checkpoint is used for evaluation. It ensures that no model is cherry-picked for comparison. 

**Real robot experimental results.** The experimental results are presented in Table 1. We assess the performance using two different settings: the in-distribution setup and visual generalization testing. In the in-distribution setup, our method surpasses all SOTA robot foundation models in terms of average success rate. Notably, our method exceeds the performance of OpenVLA by 30.65%, despite having a significantly smaller model size and less pretraining data. Compared to our baseline model, which employs vanilla reasoning, our method achieves a 14.29% increase in accuracy. To assess visual generalization, we further evaluate these advanced models under varying visual conditions. As observations become more complex—such as through the addition of distractors or vibrant backgrounds—the performance gap between CoA-VLA and OpenVLA/DiffusionVLA widens. These findings highlight the critical role of embodied, task-specific chain-ofaffordance reasoning in enhancing the performance of VLA models. 

### **5.2. Evaluation on Simulation** 

In this section, we examine the performance of CoA-VLA on LIBERO [30]. LIBERO is a robot learning benchmark comprising over 130 language-conditioned manipulation tasks. We follow the setting as in OpenVLA [22] opensourced code and test on four task suites: LIBERO-Spatial, LIBERO-Goal, LIBERO-Object, and LIBERO-Long. The detailed experimental setup is in the Appendix. 

**Simulation experimental results.** We compare with the Diffusion Policy [10], ScaleDP [56], Octo [36], and OpenVLA [22]. The experimental results of LIBERO are presented in Table 2. Our findings indicate that CoA-VLA consistently achieves superior performance across all evaluated settings, securing the highest success rate among the methods tested. Specifically, CoA-VLA achieves an overall success rate of 79.8%, outperforming OpenVLA, the previous best-performing method, by a margin of 3.3%. This improvement demonstrates the effectiveness of our approach in simulation. Compared to pre-trained robotic models like Octo and OpenVLA, CoA-VLA demonstrates non-trivial gains, showing its effectiveness in leveraging prior knowledge while adapting to diverse task requirements. Additionally, when benchmarked against train-from-scratch methods such as Diffusion Policy and ScaleDP, CoA-VLA exhibits substantial improvements, underscoring the advantages of our approach. 

### **5.3. More Experiments** 

**Spatial affordance enables safe placement.** We evaluate the effectiveness of our spatial affordance approach in the PlaceBread task, as illustrated in Figure 4. In this task, the 

9765 

Table 2. **Experimental results for LIBERO benchmark.** We report the success rate and standard error for four task suites. 

|Method / Task|LIBERO-Spatial<br>Success Rate (_↗_)|LIBERO-Object<br>Success Rate (_↗_)|LIBERO-Goal<br>Success Rate (_↗_)|LIBERO-Long<br>Success Rate (_↗_)|Average<br>Success Rate (_↗_)|
|---|---|---|---|---|---|
|Diffusion Policy [10]|78_._3_±_1_._1%|92_._5_±_0_._7%|68_._3_±_1_._2%|50_._5_±_1_._3%|72_._4_±_0_._7%|
|ScaleDP [56]|79_._1_±_0_._7%|90_._4_±_0_._9%|73_._6_±_0_._8%|48_._4_±_1_._2%|72_._9_±_0_._5%|
|Octo [36]|78_._9_±_1_._0%|85_._7_±_0_._9%|84_._6_±_0_._9%|51_._1_±_1_._3%|75_._1_±_0_._6%|
|OpenVLA [22]|84_._7_±_0_._9%|88_._4_±_0_._8%|79_._2_±_1_._0%|53_._7_±_1_._3%|76_._5_±_0_._6%|
|**CoA-VLA**|85_._3_±_0_._9%|93_._1_±_1_._0%|85_._8_±_0_._9%|55_._0_±_1_._2%|79_._8_±_0_._5%|


|**Method \ Spatial Affordance**|
|---|
|OpenVLA|
|DiffusionVLA|
|**CoA-VLA**|


Figure 4. **Spatial affordance for CoA-VLA.** CoA-VLA can identify free space for object placement.. 


Figure 5. **Movement generalization for CoA-VLA.** CoAVLA can avoid obstacles and operate safely. 

robot is presented with a plate on which three distinct objects are already placed, and it is instructed to add a piece of bread onto the plate. Our method successfully identifies open areas on the plate, allowing it to accurately position the bread without interference, thereby enabling CoA-VLA to complete all three task scenarios with precision. In contrast, alternative methods, such as OpenVLA and DiffusionVLA, succeed in only one scenario each, failing to generalize across all spatial configurations. This experiment underscores the crucial role of spatial affordance in enhancing the model’s ability to recognize and utilize available space, ultimately improving task completion accuracy and reliability across varied setups. 

**Obstacle avoidance.** Collision avoidance is essential for safe and effective physical interactions, as improper maneuvers can lead to significant damage or even catastrophic outcomes. We evaluated CoA-VLA’s obstacle avoidance capabilities in two specific tasks, illustrated in Figure 5. In the first task, we positioned a vase near the center of the task 

area to observe whether CoA-VLA could successfully navigate around the vase to retrieve a piece of paper trash. In the second task, we introduced a series of obstacles on a table, rearranging them in different configurations to assess the robot’s adaptability in maneuvering through varied layouts to complete the task. Our approach successfully completed all three scenarios, demonstrating robust collision avoidance and spatial adaptability. In contrast, OpenVLA failed to complete any of the tasks, while DiVLA succeeded in only one scenario. These results highlight the critical role of integrating movement affordance into the model’s reasoning process, enhancing its ability to navigate complex environments and complete tasks with precision and safety. 

## **6. Conclusion** 

Explicit reasoning is essential for language models to handle complex tasks. In this work, we design a reasoningaware foundation model for robotics, focusing on various affordances: object, grasp, spatial, and movement. These affordances form an interdependent chain: the robot identifies the target object and location, determines how to grasp it, decides where to place it, and navigates accordingly. By structuring this chain of affordances as intermediate language and image outputs and feeding this reasoning into the policy model, our Chain-of-Affordances (CoAVLA) model outperforms baselines on real-world robotic tasks.CoA-VLA models also generalize well to complex environments, tackling challenges like grasping in unfamiliar orientations, avoiding obstacles, and spatial generalization. Our approach provides a novel perspective on designing reasoning chains to enhance embodied control. 

## **Acknowledegments** 

This work is supported by the National Science Foundation of China (12471501), and the Sci-Tech Innovation Initiative by the Science and Technology Commission of Shanghai Municipality (24ZR1419000). 

9766 

## **References** 

- [1] Anonymous. TraceVLA: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. In _Submitted to The Thirteenth International Conference on Learning Representations_ , 2024. under review. 3 

- [2] Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from human videos as a versatile representation for robotics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13778–13790, 2023. 3 

- [3] Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, et al. Graph of thoughts: Solving elaborate problems with large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , pages 17682–17690, 2024. 3 

- [4] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 4788–4795. IEEE, 2024. 5 

- [5] Kevin Black, Michael Janner, Yilun Du, Ilya Kostrikov, and Sergey Levine. Training diffusion models with reinforcement learning. _arXiv preprint arXiv:2305.13301_ , 2023. 3 

- [6] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained imageediting diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 3 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _ω_ 0: A vision-language-action flow model for general robot control, 2024. 3 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 3 

- [9] Boyuan Chen, Zhuo Xu, Sean Kirmani, Brain Ichter, Dorsa Sadigh, Leonidas Guibas, and Fei Xia. Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14455–14465, 2024. 3, 4 

- [10] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 2, 6, 7, 8 

- [11] Jiafei Duan, Wentao Yuan, Wilbert Pumacay, Yi Ru Wang, Kiana Ehsani, Dieter Fox, and Ranjay Krishna. Manipulateanything: Automating real-world robots using vision- 

language models. _arXiv preprint arXiv:2406.18915_ , 2024. 3 

- [12] Hao-Shu Fang, Chenxi Wang, Minghao Gou, and Cewu Lu. Graspnet-1billion: A large-scale benchmark for general object grasping. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11444– 11453, 2020. 3 

- [13] Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, and Cewu Lu. Anygrasp: Robust and efficient grasp perception in spatial and temporal domains. _IEEE Transactions on Robotics_ , 2023. 3 

- [14] Haoxu Huang, Fanqi Lin, Yingdong Hu, Shengjie Wang, and Yang Gao. Copa: General robotic manipulation through spatial constraints of parts with foundation models. _arXiv preprint arXiv:2403.08248_ , 2024. 3 

- [15] Siyuan Huang, Haonan Chang, Yuhan Liu, Yimeng Zhu, Hao Dong, Peng Gao, Abdeslam Boularias, and Hongsheng Li. A3vlm: Actionable articulation-aware vision language model. _arXiv preprint arXiv:2406.07549_ , 2024. 

- [16] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 

- [17] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. _arXiv preprint arXiv:2409.01652_ , 2024. 3 

- [18] Zhenyu Jiang, Yifeng Zhu, Maxwell Svetlik, Kuan Fang, and Yuke Zhu. Synergies between affordance and geometry: 6-dof grasp detection via implicit representations. _arXiv preprint arXiv:2104.01542_ , 2021. 3, 4 

- [19] Nikita Karaev, Ignacio Rocco, Benjamin Graham, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker: It is better to track together. _arXiv preprint arXiv:2307.07635_ , 2023. 6 

- [20] Nikita Karaev, Iurii Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudolabelling real videos. _arXiv preprint arXiv:2410.11831_ , 2024. 6 

- [21] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 4, 7 

- [22] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. OpenVLA: An opensource vision-language-action model. 2, 3, 6, 7, 8 

- [23] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4015–4026, 2023. 6 

- [24] Chengshu Li, Jacky Liang, Andy Zeng, Xinyun Chen, Karol Hausman, Dorsa Sadigh, Sergey Levine, Li Fei-Fei, Fei 

9767 

Xia, and Brian Ichter. Chain of code: Reasoning with a language model-augmented code emulator. _arXiv preprint arXiv:2312.04474_ , 2023. 3 

- [25] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, Xiaofan Wang, Bei Liu, Jianlong Fu, Jianmin Bao, Dong Chen, Yuanchun Shi, Jiaolong Yang, and Baining Guo. Cogact: A foundational vision-languageaction model for synergizing cognition and action in robotic manipulation, 2024. 3 

- [26] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 3 

- [27] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18061–18070, 2024. 3 

- [28] Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data scaling laws in imitation learning for robotic manipulation, 2024. 3 

- [29] Qingqing Zhao Yao Lu Moo Jin Kim Zipeng Fu Zhuoyang Zhang Yecheng Wu Max Li Qianli Ma Song Han Chelsea Finn Ankur Handa Ming-Yu Liu Donglai Xiang* Gordon Wetzstein* Tsung-Yi Lin*. Cot-vla visual chain-of-thought reasoning for vision-language-action models. 2024. 3 

- [30] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 2, 7 

- [31] Fangchen Liu, Kuan Fang, Pieter Abbeel, and Sergey Levine. Moka: Open-vocabulary robotic manipulation through mark-based visual prompting. In _First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024_ , 2024. 3 

- [32] S Liu, Z Zeng, T Ren, F Li, H Zhang, J Yang, C Li, J Yang, H Su, J Zhu, et al. Marrying dino with grounded pre-training for open-set object detection. _arXiv preprint arXiv:2303.05499_ . 6 

- [33] Weiyu Liu, Chris Paxton, Tucker Hermans, and Dieter Fox. Structformer: Learning spatial structure for language-guided semantic rearrangement of novel objects. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 6322–6329. IEEE, 2022. 3 

- [34] Adithyavairavan Murali, Weiyu Liu, Kenneth Marino, Sonia Chernova, and Abhinav Gupta. Same object, different grasps: Data and semantic knowledge for task-oriented grasping. In _Conference on robot learning_ , pages 1540– 1557. PMLR, 2021. 3, 4 

- [35] Soroush Nasiriany, Sean Kirmani, Tianli Ding, Laura Smith, Yuke Zhu, Danny Driess, Dorsa Sadigh, and Ted Xiao. Rtaffordance: Affordances are versatile intermediate representations for robot manipulation, 2024. 3 

- [36] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey 

   - Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 2, 6, 7, 8 

- [37] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 3 

- [38] OpenAI. Chatgpt. 5 

- [39] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv e-prints_ , pages arXiv–2501, 2025. 3 

- [40] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman R¨adle, Chloe Rolland, Laura Gustafson, et al. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ , 2024. 6 

- [41] Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, and Chelsea Finn. Yell at your robot: Improving on-the-fly from language corrections. _arXiv preprint arXiv:2403.12910_ , 2024. 2 

- [42] Martin Sundermeyer, Arsalan Mousavian, Rudolph Triebel, and Dieter Fox. Contact-graspnet: Efficient 6-dof grasp generation in cluttered scenes. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13438– 13444. IEEE, 2021. 3 

- [43] Martin Sundermeyer, Arsalan Mousavian, Rudolph Triebel, and Dieter Fox. Contact-graspnet: Efficient 6-dof grasp generation in cluttered scenes. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 13438– 13444. IEEE, 2021. 4 

- [44] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 3 

- [45] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in neural information processing systems_ , 35:24824–24837, 2022. 3 

- [46] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Chengmeng Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. DiffusionVLA: Scaling robot foundation models via unified diffusion and autoregression. 2024. 2, 3, 6, 7 

- [47] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 3, 7 

9768 

- [48] Zhixiang Xu, Gao Huang, Kilian Q Weinberger, and Alice X Zheng. Gradient boosted feature selection. In _Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining_ , pages 522–531, 2014. 4 

- [49] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. _Advances in Neural Information Processing Systems_ , 36, 2024. 3 

- [50] Wentao Yuan, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. M2t2: Multi-task masked transformer for object-centric pick and place. _arXiv preprint arXiv:2311.00926_ , 2023. 3 

- [51] Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance prediction for robotics. _arXiv preprint arXiv:2406.10721_ , 2024. 3, 4, 6 

- [52] Micha! Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 3 

- [53] Andy Zeng, Pete Florence, Jonathan Tompson, Stefan Welker, Jonathan Chien, Maria Attarian, Travis Armstrong, Ivan Krasin, Dan Duong, Vikas Sindhwani, et al. Transporter networks: Rearranging the visual world for robotic manipulation. In _Conference on Robot Learning_ , pages 726–747. PMLR, 2021. 3 

- [54] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Max Li Qianli Ma, Song Han, Chelsea Finn, Ankur Handa, Ming-Yu Liu, Donglai Xiang, Gordon Wetzstein, and Tsung-Yi Lin. Cot-vla: Visual chain-ofthought reasoning for vision-language-action models, 2024. 

3 

- [55] Denny Zhou, Nathanael Sch¨arli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Claire Cui, Olivier Bousquet, Quoc Le, et al. Least-to-most prompting enables complex reasoning in large language models. _arXiv preprint arXiv:2205.10625_ , 2022. 3 

- [56] Minjie Zhu, Yichen Zhu, Jinming Li, Junjie Wen, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Scaling diffusion policy in transformer to 1 billion parameters for robotic manipulation. _arXiv preprint arXiv:2409.14411_ , 2024. 7, 8 

9769 

