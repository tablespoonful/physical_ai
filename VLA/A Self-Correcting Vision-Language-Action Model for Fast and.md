---
title: "A Self-Correcting Vision-Language-Action Model for Fast and Slow System Manipulation"
date: "2024-05-27"
authors: "Chenxuan Li; Jiaming Liu; Guanqun Wang; Xiaoqi Li; Sixiang Chen; Liang Heng"
url: https://arxiv.org/abs/2405.17418
pdf: https://arxiv.org/pdf/2405.17418
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2405.17418)** / [論文ページ](https://arxiv.org/abs/2405.17418)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **A Self-Correcting Vision-Language-Action Model for Fast and Slow System Manipulation** 

Chenxuan Li<sup>1</sup><sup>_∗_</sup> , Jiaming Liu<sup>1</sup><sup>_∗_</sup> , Guanqun Wang<sup>1</sup><sup>_∗_</sup> , Xiaoqi Li<sup>1</sup> , Sixiang Chen<sup>1</sup> , Liang Heng<sup>1</sup> , Chuyan Xiong<sup>1</sup> , Jiaxin Ge<sup>1</sup> , Renrui Zhang<sup>1</sup> , Kaichen Zhou<sup>1</sup> , Shanghang Zhang<sup>1�</sup> 

1State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University 


Figure 1. **Overview of self-corrected (SC)-VLA.** a) **Fast system of SC-VLA** enhances the pretrained MLLM with pose prediction capabilities in an autoregressive manner. b) **Slow system of SC-VLA** utilizes the end-state image and end-effector states to recognize failures, intelligently seeking expert prompt feedback to reflect on and correct the action pose through step-by-step reasoning. c) **Slow to fast: Continuous policy learning.** When an action is successfully corrected, SC-VLA continuously learns policies from these samples, enhancing the manipulation accuracy of the fast system prediction. 

## **Abstract** 

_Recently, some studies have integrated Multimodal Large Language Models into robotic manipulation, constructing vision-language-action models (VLAs) to interpret multimodal information and predict SE(3) poses. While VLAs have shown promising progress, they may suffer from failures when faced with novel and complex tasks. To emulate human-like reasoning for more robust manipulation, we propose the self-corrected (SC-)VLA framework, which integrates fast system for directly predicting actions and slow system for reflecting on failed actions within a single VLA policy. For the fast system, we incorporate parameterefficient fine-tuning to equip the model with pose prediction capabilities while preserving the inherent reasoning abilities of MLLMs. For the slow system, we propose a Chain-ofThought training strategy for failure correction, designed to mimic human reflection after a manipulation failure. Specifically, our model learns to identify the causes of action fail-_ 

*: Equal contribution, �: Corresponding author 

_ures, adaptively seek expert feedback, reflect on the current failure scenario, and iteratively generate corrective actions, step by step. Furthermore, a continuous policy learning method is designed based on successfully corrected samples, enhancing the fast system’s adaptability to the current configuration. We compare SC-VLA with the previous SOTA VLA in both simulation and real-world tasks, demonstrating an efficient correction process and improved manipulation accuracy on both seen and unseen tasks._ 

_“System 1 is fast, automatic, and intuitive, operating with little to no effort. In contrast, System 2 is slow, deliberate, and conscious, requiring intentional effort.” — [24]._ 

## **1. Introduction** 

Recently, Multimodal Large Language Models (MLLMs) [3, 28, 38] have showcased remarkable abilities in common sense reasoning. Some studies [2, 8, 34, 49] integrate MLLMs into robot manipulation, enabling robots to explore multimodal information and formulate task plan- 

1 

ning. Concurrently, other researchers [25, 30, 31, 39, 73] are focusing on developing vision-language-action (VLA) models for predicting robotic low-level action poses. While the integration of MLLMs into robotics has made encouraging strides, the current pipelines may lead to failure predictions when faced with novel tasks or object instances. Most prior research overlooks the detection and correction of failure actions within the control process, limiting their practicality in real-world scenarios where uncertainties and unexpected obstacles are common. 

Recognizing the crucial role of correction in manipulation, recent studies have proposed solutions. REFLECT [40] stands out by utilizing LLMs to generate failure explanations and assist a language-based planner in correcting errors. Building on this innovation, subsequent research [17, 41, 47, 50, 67, 69] delve deeper into LLMs’ robot correction capabilities, reflecting on failure scenes and generating correction prompts (e.g.,“Move a little bit to the right”). However, the existing correction methods still face two main challenges. **1) Lack of ability to directly correct low-level SE(3) poses.** Existing methods struggle to correct end-effector poses, as language correction prompts often cause misinterpretations in the action model due to its lack of prior exposure during training. **2) Lack of ability to learn from correction feedback.** Current correction frameworks fail to learn from successful correction cases and improve policy predictions. They still rely on external experts (e.g., GPT-4 [1]) when encountering similar failures. Given these challenges, we raise a question: “ _Can we develop a VLA model that not only possesses manipulation skills but also effectively corrects low-level failures?”_ 

Drawing inspiration from Daniel Kahneman’s assertion that “human thinking is divided into a fast system and a slow system, which separately represent intuitive processes and more logical reasoning,” [24] we introduce a self-corrected (SC-) VLA framework that mimics a human-like thinking paradigm to address the above question. As shown in Figure 1, the SC-VLA possesses both the fast system capability to directly predict end-effector poses and the slow system ability to reflect on and correct failure actions within a single VLA model. For fast system construction, we transform low-level actions into a language modeling problem, adopting parameter-efficient fine-tuning to the LLM while preserving its inherent reasoning abilities. To equip the SCVLA with slow system capabilities, we propose a Chain-ofThought training strategy for failure correction, designed to emulate human reflection when encountering manipulation failures. Specifically, the SC-VLA first recognizes SE(3) pose errors as position, rotation, or combined errors by utilizing the final state image and the robot state. Based on the identified error type, the SC-VLA adaptively requests correction feedback from experts, such as position [44], rotation [10], and reasoning expert [1]. Drawing on insights 

from previous errors and expert prompts, the SC-VLA reflects on the current failure scenario and regenerates the actions. 

During inference, the SC-VLA initially interacts with the physical world using the fast system, activating the slow system for reflection and correction only when a failure action occurs. The transition between the two systems in SCVLA can be flexibly switched using different input question prompts. Moreover, as shown in Figure 1 c), we design a continuous policy learning method that transfers successfully corrected samples from the slow system to the fast system, using exponential moving average techniques [52] along with injected adapters. This approach enhances the model’s manipulation stability in the current scene configuration while reducing the frequency of expert intervention. To train our SC-VLA, we generate 12k manipulation success samples, 15k failure samples, and 60k correction prompts in the SAPIEN simulation [61]. We evaluate our method through extensive experiments in both simulation and real-world datasets. In SAPIEN, SC-VLA improves the manipulation success rate from 66% to 87% in seen tasks and from 30% to 68% in unseen tasks. In real-world experiments, SC-VLA achieves sim-to-real transfer through simple fine-tuning on novel manipulation demonstrations with fast system training prompts, delivering superior performance compared to previous methods. In summary, our contributions are as follows: 

**1)** To mimic a human-like thinking paradigm in manipulation, we propose a Self-Corrected (SC)-VLA, equipping our model with not only the fast system ability to predict end-effector poses but also the slow system ability to reflect on and correct failure actions. 

**2)** For the slow system, we propose a Chain-of-Thought training strategy for detecting, reflecting on, and correcting low-level failure actions. SC-VLA can adaptively request expert prompt feedback to regenerate the contact pose. 

**3)** For successfully corrected samples, we introduce a continuous policy learning method to progressively enhance the model’s stability in the current scene configurations while reducing the frequency of expert intervention. 

## **2. Related Work** 

**Robotic Manipulation.** Robotic manipulation is a crucial research area with broad applications. State-based reinforcement learning is widely used [4, 14, 23, 66]. While some works use pure state as policy input [4], complex tasks often require vision-based observation [9, 13, 15, 21, 36, 42, 44, 54, 56, 60, 62–64, 73] for environment perception [7, 27]. Inspired by MLLMs’ success in general tasks, several works apply MLLMs’ reasoning capabilities to manipulation. Palm-E [8] trains multimodal encodings with LLMs for manipulation planning. VoxPoser [21] uses MLLMs for zero-shot trajectory generation. RT-2 [73] en- 

2 

ables fast adaptation to novel tasks. Robotflamingo [30] fine-tunes MLLMs on imitation learning tasks for longhorizon manipulation. Recent approaches [31, 39] enhance MLLMs with end-effector pose prediction. 

**Robotic Failure Correction.** Several studies focus on correcting robotic failures. REFLECT [40] uses LLMs for reasoning based on past experiences, improving planning with failure explanations. MULTIREACT [67] applies a vision-language model [45] as a reward model for recognizing and recovering from intermediate failures. DoReMi [17] detects misalignments between plans and execution in real-time using LLMs. CLAIRify [50] ensures plan validity through iterative prompting. Additional related work is provided in Appendix. 

## **3. Approach** 

In Section 3.1, we introduce the design motivation and problem formulation of SC-VLA. Subsequently, in Section 3.2, we present the proposed self-corrected visionlanguage-action (SC-VLA) model, detailing how the model is equipped with both fast system and slow system capabilities. Finally, we explain the continuous policy learning mechanism in Section 3.3. 

### **3.1. Overview** 

Inspired by Kahneman’s dual-process theory [24], which posits that human cognition operates through two distinct systems—the fast system and the slow system—we propose the self-corrected vision-language-action (SC-VLA) framework. In this theory, the fast system is automatic and intuitive, enabling quick decisions based on prior experience. In contrast, the slow system is deliberate and reflective, involving complex reasoning for challenging situations. Building upon this, SC-VLA integrates both systems to optimize the robotic manipulation process. The fast system enables direct end-effector pose prediction, allowing the robot to make rapid decisions. 

However, relying solely on quick, intuitive responses can lead to failure actions, especially in complex or unexpected scenarios. To address this, the slow system is employed to reflect on and correct low-level SE(3) failures through our designed Chain-of-Thought training strategy. The integration of fast and slow systems in SC-VLA mimics the human manipulation process, where rapid pose prediction and reflection work in tandem, improving the robustness of robotic actions. Next, we describe the problem formulation of our model. 

**End-effector Pose Prediction.** The core task of SCVLA is to predict the end-effector pose. Our SC-VLA policy, denoted as _π_ , generates an action _ai_ based on the initial input image ( _Ii ∈_ R<sup>_W ×H×_3</sup> ) and the corresponding language prompt ( _Li_ ). This action corresponds to the 6-DoF control of a Franka Panda robot arm, where _ai_ = 

( _a_<sup>pos</sup> _i , a_<sup>rot</sup> _i_<sup>).Here,</sup><sup>_a_pos</sup> _i ∈_ R<sup>3</sup> represents the 3D position of the end-effector, and _a_<sup>rot</sup> _i ∈_ R<sup>3</sup><sup>_×_3</sup> is the rotation matrix that describes the orientation. Following [25, 31], the endeffector pose is embedded directly into the language prompt during fine-tuning, enabling the model to predict actions along with textual information in an autoregressive manner. **Failure Reflection and Correction.** In practice, the robot action _ai_ often encounters failures, which are represented as error actions _a_<sup>_err_</sup> _i_ . For failure correction, our SC-VLA policy utilizes the end-state RGB image ( _Ie ∈_ R<sup>_W ×H×_3</sup> ) and the language-descriptive robot state ( _L_<sup>_a_</sup> _i_<sup>_i_) to</sup> identify failure cases. This is formulated as _π_ ( _Ie, L_<sup>_a_</sup> _i_<sup>_i_)</sup><sup>_→_</sup> _ci_ , where _ci_ denotes the failure type (e.g., position or rotation error). Based on _ci_ , the slow system dynamically requests corrective feedback _fi_ from experts. The feedback is then fed into the SC-VLA policy to re-predict the action _ac_ using the adjusted input _π_ ( _Ii, fi_ ) _→ ac_ . 

### **3.2. Self-Corrected VLA** 

To equip our model with foundational reasoning abilities for robotic manipulation, we load pretrained parameters from LLaMA-Adapter V2 [12]. This choice provides flexibility, as our approach can easily accommodate other MLLMs as the base model. As illustrated in Figure 2, the model architecture is composed of several key components. Due to space constraints, detailed architectural descriptions are provided in the Appendix. Next, we explain how we equip the base model with both fast and slow system capabilities, allowing it to make quick decisions while robustly refining its actions with corrective feedback. 

#### **3.2.1. Fast system: pose prediction** 

The fast system of our SC-VLA model is designed to directly generate end-effector poses for robotic manipulation tasks. During the pre-collection of training data, we capture RGB images and their corresponding successful endeffector poses for imitation learning. During fine-tuning, as shown in the fast system part of Figure 2, we structure the input text prompt for pose prediction as: “ _Predict the contact point and orientation for [task name]._ ” The output format is specified as: “ _The contact point is [x, y, z], the gripper up 3D direction is [xu, yu, zu], and the gripper forward 3D direction is [xf , yf , zf ]._ ” To represent the 6-DOF pose in text, we convert it into a classification problem by discretizing the continuous values into bins ranging from (- 50, 50] using 100 normalized integer vectors [31, 73]. For the trajectory prediction, we continuously feed the current state image into the model to generate the next 6-Dof pose. 

#### **3.2.2. Slow system: reflection and correction** 

The slow system in our SC-VLA model is designed to reflect on and correct failure actions during manipulation. Unlike previous works [40, 41] that focus on correcting highlevel planning, we introduce the novel approach of directly 

3 


Figure 2. **Overall framework of SC-VLA.** The left part shows the SC-VLA model architecture, where a vision encoder and projection layer transform robot images into LLM language embeddings. These embeddings are combined with text tokens and input into the LLM to generate end-effector poses. The right part illustrates SC-VLA’s training strategy, using both the fast and slow systems. The fast system predicts poses, while the slow system corrects failures through CoT reasoning strategy. SC-VLA uses the same prompt format for both training and inference. After correcting failures, continuous policy learning is designed to fine-tune the adapters to improve the fast system’s manipulation stability. 

correcting the end-effector’s 6-DoF control actions through a Chain-of-Thought (CoT) strategy. This correction operation is applied to key frames in the trajectory, which represent crucial or bottleneck steps of the gripper during task execution [16, 48], such as pre-pick, grasp, or place poses. Before performing the correction, the system first assesses whether the action has failed and identifies the cause of the failure. Leveraging our model’s visual understanding capabilities, we use specific prompts to determine task completion. For example, we input the end-state image and ask, “ _Is the drawer open? Please answer yes or no._ ” If the task is incomplete, the system reflects on the failure case by breaking it down into potential causes, such as incorrect position or rotation. This step-by-step reasoning approach, inspired by CoT, allows the model to systematically identify and address the underlying issues. 

Since the pre-trained MLLM lacks failure recognition capabilities, we collected 15,000 failure samples and 60,000 correction prompts in the SAPIEN simulator [61]. These failures are categorized into position, rotation, and combined errors. For position errors, we check if the contact point falls within the object’s affordance region. For rotation errors, we assess whether the angle between the predicted Z-axis and the normal of the object’s movable plane 

exceeds 30 degrees. Both the affordance region and the movable parts are automatically generated in the simulator, enabling rapid failure analysis. Once the failure cause is identified, we fine-tune our model’s adapter using failure detection prompts, as shown in Figure 2. Based on the error type, SC-VLA dynamically requests corrective feedback from specific experts, as illustrated in Figure 3. For position correction, we use Where2Act [44] to generate an affordance map from the input image, indicating potential manipulable regions. However, due to the limitations of existing affordance-based methods [9, 42], we further refine the predicted contact points using a reasoning expert (e.g., GPT-4V [1]). We select points with high affordance scores, project them back onto the image, and ask the reasoning expert, “ _Which of the contact points shown in the image can close the object? Please select n points._ ” This iterative refinement ensures more reliable contact points. For rotation correction, as shown in Figure 3 b), we use Anygrasp [10] to predict potential rotations within a manipulation box. The manipulation box is defined by expanding 5 pixels outward from the predicted contact point. The rotation expert uses the highest-confidence contact point provided by the position expert to generate the corresponding rotation. If the failure involves both position and rotation errors, the system 

4 


Figure 3. **The process of expert feedback.** For position correction, we sequentially use the position expert and reasoning expert to generate an affordance map and select contact points for prediction. For rotation correction, we automatically identify the manipulation area and leverage the rotation expert to predict potential action rotations. 

applies position correction first, followed by rotation correction. To encourage SC-VLA to reflect on failure actions through CoT reasoning, we combine the erroneous action’s 6DOF pose, the cause of the error, and the expert’s correction feedback, using them as input prompts for our model to re-predict the pose, as shown in Figure 2. This correction CoT process mimics human manipulation reasoning, where we often analyze errors step by step—first recognizing what went wrong, then understanding the underlying cause, and finally adjusting our actions based on expert guidance or prior knowledge. By adopting this slow-system reasoning, we enable SC-VLA to break down the failure action into manageable components, such as identifying where the error occurred (pose), why it happened (cause), and how it can be rectified (correction feedback). This design significantly improves the accuracy of actions for failure samples, as demonstrated in Section 4.2 and Section 4.3. 

### **3.3. Continuous policy learning** 

To equip our model with both the fast system’s ability for direct manipulation and the slow system’s ability for failure correction, we integrate pose prediction, failure detection, and failure correction data for co-fine-tuning using crossentropy loss. During inference, the relative position of the robot and the object changes with each execution, making it impractical to reuse previous expert feedback. To address this, once we obtain successfully corrected samples, we implement a continuous policy learning (CPL) method, as illustrated in Figure 2. This method enhances the fast system’s pose prediction accuracy without relying on the slow system’s CoT reasoning and expert interventions. 

In continuous policy learning, we update the model after every fifty corrected samples, using the same prompt format as in the fast system training. However, fine-tuning on new successful samples risks catastrophic forgetting, poten- 

tially reducing accuracy on previously trained samples. To mitigate this risk, we employ an exponential moving average (EMA) [52] along with a parameter-efficient fine-tuning strategy, enabling continuous learning from new data while preserving previously learned knowledge. The EMA update rule is _π_<sup>_t_</sup> = _απ_<sup>_t−_1</sup> + (1 _− α_ ) _π_<sup>_t_</sup> . Where _t_ represents the time step, and _π_ denotes our model. We set the updating weight _α_ = 0 _._ 999 based on [51]. The effectiveness of this EMA scheme for action continual learning is evaluated in the Appendix. In summary, SC-VLA can iteratively perform continuous policy learning using corrected samples, progressively transferring knowledge from the slow system to the fast system. This mechanism enables the model to adapt to environmental variations over time, without relying solely on rule-based corrections. 

## **4. Experiment** 

In this section, we conduct extensive experiments in both simulation and real-world settings. First, we introduce the simulation experimental setup in Sec.4.1. In Sec.4.2, we compare our SC-VLA with previous baselines on the simulation dataset. The ablation study is presented in Sec.4.4, demonstrating the effectiveness of each component. Finally, in Sec.4.3, we present the robust manipulation ability of our SC-VLA in real-world scenarios. 

### **4.1. Simulation experiment setting** 

In our experiments, we evaluate both open-loop and closeloop control for robotic manipulation tasks. For the openloop experiment, we use the SAPIEN [61] engine to simulate interactions with objects from PartNet-Mobility [43], collecting a dataset of 12k successful manipulation samples and 15k failure samples. To prevent the potential sim-toreal gap, in simulation training, we increase data diversity by varying object poses, camera angles, and lighting. We 

5 

Table 1. Comparison of SC-VLA with baseline methods. The table shows the performance of different methods across various seen and unseen tasks. “Experts” refers to our position and rotation experts generating action poses in a zero-shot manner. “Fast” and “Slow” represent our method’s results for the fast system’s direct prediction and the slow system’s CoT corrected prediction based on expert prompts, respectively. “CPL” refers to using our continuous policy learning method. Each task icon is described in the Appendix. 

|||||||||**Seen**|**tasks**||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|||||||||||||||||
|UMPNet [63]|0.23|0.36|0.41|0.22|0.24|0.30|0.43|0.34|**0.51**|0.21|0.66|0.27|0.23|0.23|0.29|0.60|
|FlowBot3D [9]|0.45|0.48|0.45|0.32|0.32|0.37|0.43|0.23|0.26|0.14|0.39|0.31|0.38|0.32|0.23|0.43|
|ManipLLM [31]|0.72|0.56|0.32|0.79|0.48|0.53|0.66|0.69|0.39|0.52|0.53|0.4|**0.64**|0.73|**0.62**|0.52|
|Experts|0.34|0.36|0.33|0.44|0.45|**0.56**|0.32|0.19|0.48|0.28|0.53|0.29|0.27|0.32|0.27|0.45|
|Ours(Fast)|0.78|0.63|0.58|0.70|0.52|0.13|0.81|0.88|0.56|0.71|0.84|0.80|0.46|0.76|0.30|0.83|
|Ours(Fast+Slow)|0.97|0.90|0.66|0.93|0.95|0.66|0.97|0.96|0.87|0.92|0.90|0.87|0.78|0.94|0.30|0.90|
|Ours(CPL+Fast)|**0.90**|**0.75**|**0.58**|**0.87**|**0.95**|0.46|**0.89**|**0.92**|0.50|**0.78**|**0.90**|**0.85**|0.63|**0.90**|0.38|**0.90**|
|||**Se**|**en task**|**s**||||||**Un**|**seen tas**|**ks**|||||
|**Method**|||||**AVG**|||||||||||**AVG**|
|UMPNet [63]|0.32|0.30|0.11|0.58|0.34|**0.36**|0.36|0.38|0.47|0.21|0.12|0.24|0.23|0.28|0.12|0.28|
|FlowBot3D [9]|0.19|0.33|0.23|0.47|0.33|0.29|0.47|0.64|0.31|0.27|0.30|0.09|0.41|0.35|0.37|0.35|
|ManipLLM [31]|0.39|**0.75**|0.44|0.67|0.57|0.32|0.22|0.65|**0.69**|0.38|0.85|0.27|0.53|0.26|0.38|0.47|
|Experts|0.21|0.49|0.29|0.24|0.36|0.33|0.36|0.49|0.36|0.19|0.42|0.28|0.41|0.47|0.56|0.39|
|Ours(Fast)|0.20|0.68|0.48|0.60|0.66|0.09|0.25|0.39|0.66|0.64|0.23|0.21|0.56|0.10|0.50|0.30|
|Ours(Fast+Slow)|0.80|0.89|0.74|0.98|0.87|0.27|0.65|0.71|0.83|0.85|0.71|0.73|0.87|0.48|0.90|0.68|
|Ours(CPL+Fast)|**0.60**|0.71|**0.74**|**0.90**|**0.79**|0.27|**0.61**|**0.71**|0.50|**0.92**|**0.69**|**0.69**|**0.80**|**0.70**|**0.81**|**0.69**|


evaluate the model’s generalization using a test set with both seen and unseen categories. The close-loop experiments are conducted using RLBench tasks [22] with a single front view input and predefined key frame selection [16, 48]. We collect 100 episodes per task as the training dataset and conduct 20 test trials in the simulator for each task. We use the Adam optimizer with a learning rate of 2e-5 to train the model on 80GB A100 GPUs for 10 epochs, completing the process in approximately 3 hours. The evaluation metrics follow previous works, using success rates based on predefined conditions for both open-loop and closed-loop tasks. More details about the dataset can be found in Appendix. 

### **4.2. Simulation results** 

For the open-loop experiment, we compare our SC-VLA against four representative baselines: UMPNet [63], Flowbot3D [9], ManipLLM [32], and our utilized experts. Specifically, UMPNet [63] inputs visual observations, such as RGB images and depth maps, of an articulated object to generate sequence of actions in SE(3) space. Flowbot3D [9] takes point cloud as input, and select the predicted 3D flow with the maximum magnitude to interact with objects. ManipLLM [32] uses chain-of-thought reasoning to enable the model to precisely generate an initial contact end-effector 

pose. To ensure a fair comparison, all methods use the same train/test split and end-effector settings. Reproduction details of the baselines are provided in the Appendix. 

As shown in Table 1, using our combined fast and slow systems Ours(Fast+Slow) achieves an impressive 87% accuracy on seen tasks and 68% accuracy on unseen tasks, significantly outperforming the other methods. Specifically, compared to the previous SOTA ManipLLM, Ours(Fast+Slow) achieves improvements of 30% and 21% in accuracy for seen and unseen tasks, respectively. These results demonstrate that SC-VLA can effectively correct failed actions through the slow system’s Chain of Thought (CoT) reasoning. Additionally, the experts we employed achieved only 36% and 39% accuracy on seen and unseen categories, respectively. While these experts can provide potential position and rotation estimates, simply combining their outputs does not yield an optimal 6-DoF pose. The lower accuracy compared to our method demonstrates that our advantages stem not solely from the use of experts but from the overall effectiveness of our approach. When comparing Ours(CPL+Fast) and Ours(Fast), we find that Ours(CPL+Fast) achieves improvements of 13% and 39% in accuracy for seen and unseen tasks. This indicates that our method effectively enhances the model’s manipulation 

6 


Figure 4. **Task Execution Flow Illustrated with Keyframes.** perspective. The flow is from left to the right. 

We visualize the agent’s execution process for each task from the front 

Table 2. **Real-world experiments.** We test each method 10 times across diverse object poses. 

||Pick|Place|Stack|Unplug||
|---|---|---|---|---|---|
|Method|place|bottle|block|charger|Mean|
|ManipLLM|0.40|0.20|0.10|0.20|0.23|
|DP3|0.40|0.50|0.30|0.50|0.43|
|Ours(Fast+Slow)|**0.50**|**0.60**|**0.50**|**0.70**|**0.58**|


accuracy and adaptability to varying scene configurations. The significant improvement observed in unseen tasks further demonstrates that our proposed method can effectively enhance the model’s generalization capabilities. 

As for the close-loop experiment in RLBench [22], Ours(Fast) achieves an average success rate of 63% on the following five tasks “take USB out of computer,” “close fridge,” “close box,” “toilet seat down,” and “unplug charger.” In contrast, Ours (Fast+Slow) achieves a success rate of 91% This demonstrates that our SC-VLA effectively handles sequential action prediction and correction, further highlighting its robustness and effectiveness. Due to space limitations, a comprehensive description of the closed-loop experiment and its settings is provided in the Appendix. 

### **4.3. Real-world results** 

**Experiment setting.** In Figure 4, we present real-world experiments using the SC-VLA model with a Franka Research 3 (FR3) robot and a 3D-printed UMI gripper [6] across four manipulation tasks, including _pick and place_ , _unplug charger_ , _place bottle at rack_ , and _stack blocks_ . We use a RealSense L515 camera to capture real-world visual observations from the front view. For each task, we collect 30 demonstrations with randomized object poses via teleoperation. Key frames are then extracted to construct the training set. We train our method for 10 epochs, loading 

simulation-pretrained model parameters. Since fine-tuning on real-world data is primarily aimed at addressing the simto-real gap, we use the simple fast system prompt for training. For evaluation, we use the model from the final training epoch and test it on 10 trials with diverse object poses for a robust evaluation. 

**Quantitative results.** As shown in Table 2, we evaluate the effectiveness of SC-VLA by comparing it with two methods: (1) ManipLLM [31], where we load its simulation-pretrained parameters for a fair comparison, and (2) 3D Diffusion Policy (DP3) [68], a state-of-the-art (SOTA) point cloud-based method that employs diffusionbased generation for action prediction. Compared to ManipLLM, SC-VLA outperforms it in multiple tasks. Since both methods adopt the same backbone, this comparison directly reflects our method’s Chain-of-Thought reasoning ability to recognize failures, request feedback from experts, and correct action poses. Notably, in the _stack block_ task, which demands high precision in pose prediction, SC-VLA achieves a 50% success rate, representing a 40% improvement over ManipLLM. Furthermore, compared to DP3, our SC-VLA achieves superior performance across various tasks, resulting in a 15% performance improvement. This further demonstrates SC-VLA’s ability to predict accurate contact points and 3D directions in real-world scenarios. 

**Qualitative results.** As shown in Figure 4, we visualize the key frames of manipulation process for four realworld tasks. Our method accurately predicts the 7-DoF endeffector poses, enabling successful task completion along the predicted trajectories. For instance, in the _place bottle at rack_ task, our method first secures a precise grasp near the bottle’s neck, then rotates the gripper to the optimal placement angle, and finally determines the perfect timing to open the gripper for placement. More real-world 

7 


Figure 5. Ablation study for each method in our SC-VLA framework. a) examines the impact of various expert feedback prompts on slow system reasoning. b) investigates the effects of different correction times on pose correction accuracy. c) analyzes the influence of continuous policy learning iterations on the model’s prediction accuracy. 

demonstrations are shown in the supplementary video. 

### **4.4. Ablation study** 

To elucidate the contribution and effectiveness of individual methods within our SC-VLA, we conduct extensive ablation studies in the SAPIEN simulator. 

**The impact of expert type.** First, we explore the influence of different types of expert feedback prompts on the success rate of corrections performed by the slow system. As shown in Figure 5 a), “P” and “R” represent utilizing our designed position and rotation feedback, respectively. “P + R” represents the utilization of combined expert feedback, while “Adaptive” (ours) refers to adaptively seeking expert feedback based on the cause of failure. For all experiments, we input the prompt feedback into our SC-VLA, allowing it to re-predict end-effector poses. We find that any type of expert prompt can improve unseen manipulation accuracy, demonstrating the importance of correction for novel object manipulation. Additionally, we observe that ours (“Adaptive”) achieves comparable results to “P + R”, but with lower expert intervention costs. The results confirm that detecting failure cases and adaptively seeking expert feedback is essential for stable manipulation. The accuracy of failure detection is shown in the Appendix. 

**The impact of correction times.** In the slow system, our experts can return multiple prompts simultaneously; for example, the position expert can provide _n_ potential contact points. Therefore, we explore the impact of different correction times on pose correction accuracy. As shown in Figure 5 b), the x-axis represents the number of expert prompts used for correction. Note that we count a manipulation as successful if it succeeds even once during multiple corrected actions. We find that with just one correction, SCVLA achieves an improvement of 15.4% on seen tasks and 17.8% on unseen tasks compared to our fast system. The results demonstrate the effectiveness of our designed CoT 

correction paradigm. Furthermore, once the number of corrections reaches three or more, the slow system achieves robust manipulation accuracy. 

#### **The impact of continuous policy learning times** 

After correction by the slow system, SC-VLA can output the correct pose and rotation. We save the successfully corrected samples and use them for continuous policy learning. The varying update iterations will impact the finetuning time and the manipulation accuracy achieved after fine-tuning. As shown in Figure 5 c), all manipulation results are evaluated using the fast system’s inference manner after the continual learning process. The x-axis represents the training iteration for each corrected sample in continual policy learning. Both seen and unseen tasks improve significantly after multiple fine-tuning rounds, validating the effectiveness of our method in transferring knowledge from the slow system to the fast system. To rule out overfitting on the test set, we also evaluate the model on the test B set after continuous learning (shown in the Appendix). 

## **5. Conclusion and limitation** 

Drawing on Daniel Kahneman’s concept of a “fast system” and “slow system,” we propose a self-corrected VLA that emulates human-like thinking for stable manipulation. SCVLA combines a fast system for direct end-effector pose prediction and a slow system for CoT reflecting on and correcting failed actions. During inference, the fast system interacts with the physical world, while the slow system activates only when a failure occurs. We also introduce continuous policy learning, allowing SC-VLA to learn from corrected actions and continuously improve the fast system’s accuracy. Experimental results demonstrate that SC-VLA significantly enhances manipulation performance in both simulation and real-world scenarios. 

A limitation of SC-VLA is that our slow system chainof-thought reasoning leads to additional computational cost, 

8 

which can be overcomed by integrating more efficient LLMs [39, 59, 71]. 

## **6. Acknowledge** 

This work was supported by the National Natural Science Foundation of China (62476011). 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 2, 4 

- [2] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv:2204.01691_ , 2022. 1 

- [3] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. _Advances in Neural Information Processing Systems_ , 35:23716–23736, 2022. 1, 4 

- [4] OpenAI: Marcin Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew, Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, et al. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research_ , 39(1):3–20, 2020. 2 

- [5] Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, and Rui Zhao. Shikra: Unleashing multimodal llm’s referential dialogue magic. _arXiv preprint arXiv:2306.15195_ , 2023. 5 

- [6] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. _arXiv preprint arXiv:2402.10329_ , 2024. 7 

- [7] Congyue Deng, Jiahui Lei, Bokui Shen, Kostas Daniilidis, and Leonidas Guibas. Banana: Banach fixed-point network for pointcloud segmentation with inter-part equivariance. _arXiv preprint arXiv:2305.16314_ , 2023. 2 

- [8] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palme: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 1, 2 

- [9] Ben Eisner, Harry Zhang, and David Held. Flowbot3d: Learning 3d articulation flow to manipulate articulated objects. _arXiv preprint arXiv:2205.04382_ , 2022. 2, 4, 6 

- [10] Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, and Cewu Lu. Anygrasp: Robust and efficient grasp perception in spatial and temporal domains. _IEEE Transactions on Robotics_ , 2023. 2, 4 

- [11] Luciano Floridi and Massimo Chiriatti. Gpt-3: Its nature, scope, limits, and consequences. _Minds and Machines_ , 30: 681–694, 2020. 4 

- [12] Peng Gao, Jiaming Han, Renrui Zhang, Ziyi Lin, Shijie Geng, Aojun Zhou, Wei Zhang, Pan Lu, Conghui He, Xiangyu Yue, et al. Llama-adapter v2: Parameter-efficient visual instruction model. _arXiv preprint arXiv:2304.15010_ , 2023. 3, 5 

- [13] Haoran Geng, Songlin Wei, Congyue Deng, Bokui Shen, He Wang, and Leonidas Guibas. Sage: Bridging semantic and actionable parts for generalizable articulated-object manipulation under language instructions. _arXiv preprint arXiv:2312.01307_ , 2023. 2 

- [14] Yiran Geng, Boshi An, Haoran Geng, Yuanpei Chen, Yaodong Yang, and Hao Dong. End-to-end affordance learning for robotic manipulation. In _International Conference on Robotics and Automation (ICRA)_ , 2023. 2 

- [15] Ran Gong, Jiangyong Huang, Yizhou Zhao, Haoran Geng, Xiaofeng Gao, Qingyang Wu, Wensi Ai, Ziheng Zhou, Demetri Terzopoulos, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. Arnold: A benchmark for language-grounded task learning with continuous states in realistic 3d scenes. _arXiv preprint arXiv:2304.04321_ , 2023. 2 

- [16] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In _Conference on Robot Learning_ , pages 694– 710. PMLR, 2023. 4, 6 

- [17] Yanjiang Guo, Yen-Jen Wang, Lihan Zha, Zheyuan Jiang, and Jianyu Chen. Doremi: Grounding language model by detecting and recovering from plan-execution misalignment. _arXiv preprint arXiv:2307.00329_ , 2023. 2, 3, 5 

- [18] Ziyu Guo, Renrui Zhang, Xiangyang Zhu, Yiwen Tang, Xianzheng Ma, Jiaming Han, Kexin Chen, Peng Gao, Xianzhi Li, Hongsheng Li, et al. Point-bind & point-llm: Aligning point cloud with multi-modality for 3d understanding, generation, and instruction following. _arXiv preprint arXiv:2309.00615_ , 2023. 5 

- [19] Yining Hong, Haoyu Zhen, Peihao Chen, Shuhong Zheng, Yilun Du, Zhenfang Chen, and Chuang Gan. 3d-llm: Injecting the 3d world into large language models. _arXiv preprint arXiv:2307.12981_ , 2023. 5 

- [20] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 6 

- [21] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 2 

- [22] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 6, 7, 1, 4 

- [23] Shirin Joshi, Sulabh Kumra, and Ferat Sahin. Robotic grasping using deep reinforcement learning. In _2020 IEEE 16th International Conference on Automation Science and Engineering (CASE)_ , pages 1461–1466. IEEE, 2020. 2 

9 

- [24] Daniel Kahneman. Thinking, fast and slow. _Farrar, Straus and Giroux_ , 2011. 1, 2, 3 

- [25] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2, 3 

- [26] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka GrabskaBarwinska, et al. Overcoming catastrophic forgetting in neural networks. _Proceedings of the national academy of sciences_ , 114(13):3521–3526, 2017. 4 

- [27] Jiahui Lei, Congyue Deng, Bokui Shen, Leonidas Guibas, and Kostas Daniilidis. Nap: Neural 3d articulation prior. _arXiv preprint arXiv:2305.16315_ , 2023. 2 

- [28] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation. In _International Conference on Machine Learning_ , pages 12888– 12900. PMLR, 2022. 1, 4 

- [29] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models, 2023. 4 

- [30] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 2, 3 

- [31] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. _arXiv preprint arXiv:2312.16217_ , 2023. 2, 3, 6, 7, 1, 4 

- [32] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18061–18070, 2024. 6 

- [33] Zhizhong Li and Derek Hoiem. Learning without forgetting. _IEEE transactions on pattern analysis and machine intelligence_ , 40(12):2935–2947, 2017. 4 

- [34] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 9493–9500. IEEE, 2023. 1 

- [35] Ziyi Lin, Chris Liu, Renrui Zhang, Peng Gao, Longtian Qiu, Han Xiao, Han Qiu, Chen Lin, Wenqi Shao, Keqin Chen, et al. Sphinx: The joint mixing of weights, tasks, and visual embeddings for multi-modal large language models. _arXiv preprint arXiv:2311.07575_ , 2023. 5 

- [36] Chang Liu, Kejian Shi, Kaichen Zhou, Haoxiao Wang, Jiyao Zhang, and Hao Dong. Rgbgrasp: Image-based object grasping by capturing multiple views during robot arm movement with neural radiance fields. _IEEE Robotics and Automation Letters_ , 2024. 2 

- [37] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction tuning. _arXiv preprint arXiv:2310.03744_ , 2023. 5 

- [38] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _arXiv preprint arXiv:2304.08485_ , 2023. 1 

- [39] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv preprint arXiv:2406.04339_ , 2024. 2, 3, 

9 

- [40] Zeyi Liu, Arpit Bahety, and Shuran Song. Reflect: Summarizing robot experiences for failure explanation and correction. _arXiv preprint arXiv:2306.15724_ , 2023. 2, 3, 5 

- [41] Chenlin Ming, Jiacheng Lin, Pangkit Fong, Han Wang, Xiaoming Duan, and Jianping He. Hicrisp: A hierarchical closed-loop robotic intelligent self-correction planner. _arXiv preprint arXiv:2309.12089_ , 2023. 2, 3 

- [42] Kaichun Mo, Shilin Zhu, Angel X. Chang, Li Yi, Subarna Tripathi, Leonidas J. Guibas, and Hao Su. PartNet: A largescale benchmark for fine-grained and hierarchical part-level 3D object understanding. In _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 2, 4 

- [43] Kaichun Mo, Shilin Zhu, Angel X Chang, Li Yi, Subarna Tripathi, Leonidas J Guibas, and Hao Su. Partnet: A largescale benchmark for fine-grained and hierarchical part-level 3d object understanding. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 909–918, 2019. 5, 1, 2 

- [44] Kaichun Mo, Leonidas J Guibas, Mustafa Mukadam, Abhinav Gupta, and Shubham Tulsiani. Where2act: From pixels to actions for articulated 3d objects. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6813–6823, 2021. 2, 4, 1 

- [45] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 3, 1, 5 

- [46] David Rolnick, Arun Ahuja, Jonathan Schwarz, Timothy Lillicrap, and Gregory Wayne. Experience replay for continual learning. _Advances in neural information processing systems_ , 32, 2019. 4 

- [47] Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, and Chelsea Finn. Yell at your robot: Improving on-the-fly from language corrections. _arXiv preprint arXiv:2403.12910_ , 2024. 2 

- [48] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pages 785–799. PMLR, 2023. 4, 6, 1 

- [49] Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. Progprompt: Generating situated robot 

10 

task plans using large language models. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 11523–11530. IEEE, 2023. 1 

- [50] Marta Skreta, Naruki Yoshikawa, Sebastian ArellanoRubach, Zhi Ji, Lasse Bjørn Kristensen, Kourosh Darvish, Al´an Aspuru-Guzik, Florian Shkurti, and Animesh Garg. Errors are useful prompts: Instruction guided task programming with verifier-assisted iterative prompting. _arXiv preprint arXiv:2303.14100_ , 2023. 2, 3, 5 

- [51] Antti Tarvainen and Harri Valpola. Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. _Learning_ , 2017. 5 

- [52] Antti Tarvainen and Harri Valpola. Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results. _Advances in neural information processing systems_ , 30, 2017. 2, 5 

- [53] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 1, 4, 5 

- [54] Weikang Wan, Haoran Geng, Yun Liu, Zikang Shan, Yaodong Yang, Li Yi, and He Wang. Unidexgrasp++: Improving dexterous grasping policy learning via geometryaware curriculum and iterative generalist-specialist learning. _arXiv preprint arXiv:2304.00464_ , 2023. 2 

- [55] Guanqun Wang, Jiaming Liu, Chenxuan Li, Junpeng Ma, Yuan Zhang, Xinyu Wei, Kevin Zhang, Maurice Chong, Ray Zhang, Yijiang Liu, et al. Cloud-device collaborative learning for multimodal large language models. _arXiv preprint arXiv:2312.16279_ , 2023. 5 

- [56] Qianxu Wang, Haotong Zhang, Congyue Deng, Yang You, Hao Dong, Yixin Zhu, and Leonidas Guibas. Sparsedff: Sparse-view feature distillation for one-shot dexterous manipulation. _arXiv preprint arXiv:2310.16838_ , 2023. 2 

- [57] Wenhai Wang, Zhe Chen, Xiaokang Chen, Jiannan Wu, Xizhou Zhu, Gang Zeng, Ping Luo, Tong Lu, Jie Zhou, Yu Qiao, et al. Visionllm: Large language model is also an open-ended decoder for vision-centric tasks. _arXiv preprint arXiv:2305.11175_ , 2023. 5 

- [58] Zehan Wang, Haifeng Huang, Yang Zhao, Ziang Zhang, and Zhou Zhao. Chat-3d: Data-efficiently tuning large language model for universal dialogue of 3d scenes. _arXiv preprint arXiv:2308.08769_ , 2023. 5 

- [59] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Kun Wu, Zhiyuan Xu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _arXiv preprint arXiv:2409.12514_ , 2024. 9 

- [60] Ruihai Wu, Yan Zhao, Kaichun Mo, Zizheng Guo, Yian Wang, Tianhao Wu, Qingnan Fan, Xuelin Chen, Leonidas Guibas, and Hao Dong. Vat-mart: Learning visual action trajectory proposals for manipulating 3d articulated objects. _arXiv preprint arXiv:2106.14440_ , 2021. 2 

- [61] Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, He Wang, Li Yi, Angel X. Chang, Leonidas J. Guibas, and 

Hao Su. SAPIEN: A simulated part-based interactive environment. In _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2020. 2, 4, 5, 1 

- [62] Yinzhen Xu, Weikang Wan, Jialiang Zhang, Haoran Liu, Zikang Shan, Hao Shen, Ruicheng Wang, Haoran Geng, Yijia Weng, Jiayi Chen, et al. Unidexgrasp: Universal robotic dexterous grasping via learning diverse proposal generation and goal-conditioned policy. _arXiv preprint arXiv:2303.00938_ , 2023. 2 

- [63] Zhenjia Xu, Zhanpeng He, and Shuran Song. Universal manipulation policy network for articulated objects. _IEEE Robotics and Automation Letters_ , 7(2):2447–2454, 2022. 6, 2 

- [64] Jingyun Yang, Congyue Deng, Jimmy Wu, Rika Antonova, Leonidas Guibas, and Jeannette Bohg. Equivact: Sim(3)equivariant visuomotor policies beyond rigid object manipulation. _arXiv preprint arXiv:2310.16050_ , 2023. 2 

- [65] Senqiao Yang, Jiaming Liu, Ray Zhang, Mingjie Pan, Zoey Guo, Xiaoqi Li, Zehui Chen, Peng Gao, Yandong Guo, and Shanghang Zhang. Lidar-llm: Exploring the potential of large language models for 3d lidar understanding. _arXiv preprint arXiv:2312.14074_ , 2023. 5 

- [66] Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Mastering visual continuous control: Improved data-augmented reinforcement learning. _arXiv preprint arXiv:2107.09645_ , 2021. 2 

- [67] Zhouliang Yu, Jie Fu, Yao Mu, Chenguang Wang, Lin Shao, and Yaodong Yang. Multireact: Multimodal tools augmented reasoning-acting traces for embodied agent planning. 2023. 2, 3, 5 

- [68] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy. _arXiv preprint arXiv:2403.03954_ , 2024. 7 

- [69] Lihan Zha, Yuchen Cui, Li-Heng Lin, Minae Kwon, Montserrat Gonzalez Arenas, Andy Zeng, Fei Xia, and Dorsa Sadigh. Distilling and retrieving generalizable knowledge for robot manipulation via language corrections. _arXiv preprint arXiv:2311.10678_ , 2023. 2 

- [70] Renrui Zhang, Jiaming Han, Aojun Zhou, Xiangfei Hu, Shilin Yan, Pan Lu, Hongsheng Li, Peng Gao, and Yu Qiao. Llama-adapter: Efficient fine-tuning of language models with zero-init attention. _arXiv preprint arXiv:2303.16199_ , 2023. 1, 4 

- [71] Baichuan Zhou, Ying Hu, Xi Weng, Junlong Jia, Jie Luo, Xien Liu, Ji Wu, and Lei Huang. Tinyllava: A framework of small-scale large multimodal models. _arXiv preprint arXiv:2402.14289_ , 2024. 9 

- [72] Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 5 

- [73] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _7th Annual Conference on Robot Learning_ , 2023. 2, 3 

11 

# Appendix 

Due to space limitations, we provide additional details on the dataset, baseline reproduction, SC-VLA failure detection evaluation, and supplementary experiments. Below, we outline the contents of our appendix. 

- **A. Additional simulation experiment setting** 

**B. Dataset & baseline reproduction details** 

- **C. Failure detection results** 

- **D. Additional ablation study** 

- **E. Experimental results on Test B set** 

- **F. Details of Close-loop Experiments** 

- **G. Additional related work** 

**H. Model architecture of SC-VLA** 

- **I. Advantages of fast & slow systems** 

## **A. Additional simulation experiment setting** 

### **A.1. Data Collection** 

We use the simulator to collect training data under openloop and closed-loop control. For the open-loop experiment, we follow the data collection process of previous works [31, 44], adopting the SAPIEN engine [61] to set up an interactive simulation environment with articulated objects from PartNet-Mobility [43]. The Franka Panda Robot, equipped with a suction gripper, serves as the robotic actuator. During data collection, we randomly select a contact point **p** on the movable part and orient the end-effector’s z-axis opposite to its normal vector, with a random y-axis direction to interact with the object. Successful operations are categorized as successful samples and integrated into the dataset. Our training dataset comprises 12k successful manipulation samples across 20 categories. Meanwhile, we collect 15k failure samples and 60k corresponding correction prompts, covering position, rotation, and combined errors. For evaluation, we generate 1k examples for the test set, comprising 20 training (seen) and 10 testing (unseen) categories. The unseen categories are used to evaluate the generalization capability of SC-VLA. The additional description of the dataset and variation can be found in Appendix B.1 and B.2. For the closed-loop experiment, we select five tasks from RLBench [22], including “take USB out of computer,” “close fridge,” “close box,” “toilet seat down,” and “unplug charger.” We utilize a single-view input (the front view from a third-person perspective) and follow to the key frame selection manner outlined in previous work [48]. 

### **A.2. Implementation Details** 

Our SC-VLA loads the pre-trained parameters of LLaMAAdapter-v2[70], which integrates a pre-trained CLIP[45] as the visual encoder and a 7B LLaMA[53] model as the language model. The multi-modal projection module is built 

with 32 transformer layers, each configured with a hidden dimension of 4096—carefully chosen as a multiple of 256—to ensure efficient scaling. Each layer also features 32 attention heads and employs a layer normalization epsilon of 1e-05 for enhanced stability, while the vocabulary size is set to -1 to enable flexible token handling. Throughout the fine-tuning phase, we utilize the Adam optimizer with (( _β_ 1 _, β_ 2) = (0 _._ 9 _,_ 0 _._ 999) and an initial learning rate of 1e-4, accompanied by a warm-up period of one epoch. We finetuned our model on four 80G A100 GPUs for 10 epochs. 

### **A.3. Evaluation Metric** 

For the open-loop experiment, we follow the metrics from previous works [31], using the manipulation success rate. Specifically, the object starts in its initial state, and the goal is to actuate the joint to its target state. We use the predicted contact point and rotation to interact with objects and complete the task. Similar to [44], the trajectory for each task is predefined, i.e., moving backward along the z-axis of the end-effector pose. An action is considered successful if the joint state difference before and after interaction exceeds a threshold of 0.1 meters. For the closed-loop experiment, we follow the evaluation metrics from previous works[22], assessing task success rate based on predefined success conditions. 

## **B. Dataset & baseline reproduction details** 

### **B.1. Sapien Dataset Details** 

As shown in Table 3, our training dataset comprises 12k manipulation scenarios, encompassing 20 distinct object categories, specifically including: Safe ( _S_ ), Door ( _D_ ), Display ( _DS_ ), Refrigerator ( _RF_ ), Laptop ( _LT_ ), Lighter ( _LI_ ), Microwave ( _MW_ ), Mouse ( _MO_ ), Box ( _BX_ ), Trash Can ( _TC_ ), Kitchen Pot ( _KP_ ), Suitcase ( _SU_ ), Pliers ( _PL_ ), Storage Furniture ( _SF_ ), Remote ( _RM_ ), Bottle ( _B_ ), Folding Chair ( _FD_ ), Toaster ( _TS_ ), Lamp ( _L_ ), and Dispenser ( _DP_ ). Following Partnet [43], different tasks are designed for each category. For instance, opening the door or control panel of a refrigerator, opening the cap of a bottle, and rotating the lid of a box. The detailed task design can be found at: https://sapien.ucsd.edu/browse 

In performance evaluation experiments, we utilize two primary test datasets: Test set and Test B set. Both datasets consist of 1081 manipulation scenarios and include 30 object categories, as detailed in Table 3. We collect the test B set where only the relative positions between the robot and the object are altered compared to the test set. This test B set aims to validate the effectiveness of our continuous policy learning, ensuring it does not overfit on the test set. Among these, 20 categories are present in the training set (seen), while 10 categories are not included in the training set (unseen), which are: Toilet ( _TL_ ), Scissors ( _SC_ ), Table ( _T_ ), Sta- 

1 

pler ( _ST_ ), Kettle ( _K_ ), USB ( _U_ ), Switch ( _SW_ ), Washing Machine ( _WM_ ), Faucet ( _FC_ ), and Phone ( _PH_ ). This setup aims to thoroughly assess the model’s generalization capabilities. 

### **B.2. Sapien Dataset variation** 

Regarding the variation between training and testing data, we followed the data collection settings of where2act [44] and ManipLLM [31]. The specific variations can be divided into two aspects: 1) Asset Variation and 2) State Variation. 

1) Asset Variation: We use 20 categories from PartNet [43] for seen objects and reserve the remaining 10 categories for unseen objects to analyze if RoboMamba can generalize to novel categories. Specifically, we further divide the seen objects into 1037 training shapes and 489 testing shapes, using only the training shapes to construct the training data. Thus, the shapes of the seen objects encountered during training and testing are different. For unseen categories, there are a total of 274 shapes, which are used exclusively in the testing data. 

2) State Variation: We observe the object in the scene from an RGB-D camera with known intrinsics, mounted 4.5-5.5 units away from the object, facing its center. The camera is located at the upper hemisphere of the object with a random azimuth between [-45, 45] and a random altitude between [30, 60]. Since the tasks involve ’pulling,’ we also initialize the starting pose for each articulated part randomly between its rest joint state (fully closed) and any position up to half of its joint state (half-opened). These state settings are utilized for both training and testing data, aiming to boost the model’s generalization ability. 

### **B.3. Baseline Reproduction** 

**UMPNet [63]** : It inputs visual observations, such as RGB images and depth maps, of an articulated object to generate a sequence of actions in SE(3) space. It identifies the correct position on the object to interact with ( _e.g._ ., interacting with the lid rather than the base) and determines the appropriate action direction ( _e.g._ , pulling up instead of pushing down) for interaction. 

**Flowbot3D [9]** : Flowbot3D begins by observing the initial configuration of the object of interest in the form of point cloud data. It is then post-processed and inputted into the model, which predicts 3D flow vectors for each point. It selects the point with the maximum flow vector magnitude and uses motion planning to make contact with that point via suction based on the selected flow. 

**ManipLLM [31]** : ManipLLM uses chain-of-thought reasoning to enable the model to precisely generate an initial contact end-effector pose, including the pixel coordinates, gripper upward direction, and gripper forward direction. It then employs an active impedance adaptation policy that adjusts the direction based on force feedback to ensure a smooth movement trajectory. 

## **C. Failure detection results** 

In this paper, we introduce a self-corrected (SC) MLLM that mimics a human-like thinking paradigm, including two reasoning modes: fast system and slow system. SC-VLA possesses both the fast system’s capability to directly predict end-effector poses and the slow system’s ability to reflect on and correct failure actions. In the slow system chain of thought reasoning, one important intermediate process is failure case detection. The failure detection results are shown in Table 4. The experiments are evaluated on a selfcollected dataset, which contains 1K failure test samples on 20 seen categories of objects with three failure causes (i.e., position, rotation, or combined error). 

SC-VLA achieves an impressive average accuracy of **0.89** for rotation-related failures. This high accuracy underscores the model’s capability to precisely identify and diagnose issues related to the robot’s manipulation direction. Notably, categories such as _Remote_ , _Lamp_ , and _Laptop_ exhibit exceptional accuracy rates, reflecting the model’s robustness across varied object geometries and complexities. 

For position-related failures, SC-VLA achieves an outstanding average accuracy of **0.98** . This near-perfect detection rate emphasizes the reliability of our SC-VLA in pinpointing positional inaccuracies during manipulation actions. Categories including _Mouse_ , _Phone_ , _Pliers_ , and _Refrigerator_ all attain a flawless accuracy of 1.00, demonstrating the SC-VLA’s precision in handling positional errors. 

When addressing failures caused by both position and rotation, the model maintains a commendable average accuracy of **0.84** . Despite the increased complexity of these cases, our method effectively diagnoses combined failures, ensuring that subsequent correction experts are accurately requested. Categories such as _Remote_ , _Kettle_ , and _Laptop_ once again exhibit high accuracy rates, reaffirming the model’s adaptability and precision. 

These results highlight the effectiveness of our SC-VLA in failure case detection and reflection. Accurately identifying the failure cause can significantly enhance the stability of our slow system reasoning, thereby improving failure correction. 

## **D. Additional ablation study** 

To further validate the robustness of our proposed SC-VLA, we conduct supplementary ablation studies. In this section, we assess the efficacy of our approach in the context of continual policy learning. Specifically, we integrate various continual learning methods into our self-correction process to update the model and evaluate the performance of the updated model. The test set used for this evaluation, is consistent with the experimental setup described in the main text. It comprises 30 categories of manipulation targets, totaling 1081 manipulation scenarios. The results of these 

2 

Table 3. Representation of each category icon. 


|**_Safe_**|**_Door_**|**_Display_**|**_Refrigerator _**|**_Laptop_**|**_Lighter_**|**_Microwave_**|**_Mouse_**|**_Box_**|**_Trashcan_**|
|---|---|---|---|---|---|---|---|---|---|
|**_Kitchen_**<br>**_Pot_**|**_Suitcase_**|**_Pliers_**|**_Storage_**<br>**_Furniture_**|**_Remote_**|**_Bottle_**|**_Folding_**<br>**_Chair_**|**_Toaster_**|**_Lamp_**|**_Dispenser_**|
|**_Toilet_**|**_Scissors_**|**_Table_**|**_Stapler_**|**_Kettle_**|**_USB_**|**_Switch_**|**_Washing_**<br>**_Machine_**|**_Faucet_**|**_Phone_**|


Table 4. Failure detection accuracy is evaluate on collected failure manipulation samples across 20 seen categories with three failure causes: position, rotation, or both. 

|**Failure Causes**||||||||||**Object**|**Categ**|**ories**|||||||||**AVG**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|_Rotation_|0.95|0.84|0.88|0.80|0.81|0.96|0.88|0.82|0.94|0.78|0.93|0.73|0.83|0.89|0.93|0.94|1.00|0.82|0.95|0.95|**0.89**|
|_Position_|0.95|1.00|1.00|1.00|1.00|1.00|0.95|1.00|0.94|1.00|0.95|1.00|1.00|0.93|1.00|0.91|1.00|1.00|1.00|0.95|**0.98**|
|_Position & Rotation_|0.71|0.74|0.92|0.88|0.83|1.00|0.71|0.91|0.91|0.95|0.83|0.82|0.82|0.82|0.92|0.84|1.00|0.84|1.00|0.61|**0.84**|


evaluations are presented in Table 5, demonstrating the performance improvements achieved through the integration of continual learning methods in our method. After each update, the model undergoes a new round of manipulation tests, and successful manipulation instances are collected. These successful examples were then incorporated as new data for continual learning, further updating the model. All test results are obtained after the base model is updated four times continually, with performance measured and recorded accordingly. 

As shown in Table 5, Ours(CPL+Fast) seamlessly integrates Exponential Moving Average (EMA) to continually fine-tune the injected adapters, showing significant performance improvements across multiple evaluation metrics. Our method surpasses Elastic Weight Consolidation (EWC), Learning without Forgetting (LwF), and Experience Replay in both seen and unseen categories. Specifically, in the seen categories, our method achieves an impressive average successful rate of 0.79, compared to 0.68 for EWC, 0.75 for LwF, and 0.71 for Experience Replay. This superior performance indicates that our approach not only retains knowledge from previous tasks but also effectively assimilates new information, thereby addressing the prevalent problem of catastrophic forgetting. 

In the unseen categories, our method consistently maintains a high performance with an average score of 0.69, compared to 0.42 for EWC, 0.62 for LwF, and 0.52 for Ex- 

perience Replay. This consistent performance across both seen and unseen categories underscores the robustness of our continual learning strategy. Notably, our method excels in categories such as _Laptop (LT)_ , _Phone (PH)_ , and _Refrigerator (RF)_ , demonstrating its effectiveness to generalize across a diverse array of objects and scenarios. 

Furthermore, our approach exhibits marked improvement in categories with lower baseline performances. For instance, in the _Dispenser (DP)_ category, our method achieves a perfect score of 0.95, highlighting its capacity to manage challenging tasks with remarkable efficacy. Similarly, in the _Lamp (L)_ and _Kettle (K)_ categories, our method significantly outperforms other continual learning methods, achieving scores of 0.74 and 0.92, respectively. Overall, the experimental results validate the effectiveness of our proposed continuous policy learning. By incorporating the Exponential Moving Average scheme in the fine-tuning process, our approach ensures robust performance improvements while mitigating the risks of catastrophic forgetting. This enables our model to efficiently transfer successfully corrected samples from the slow system to the fast system. 

## **E. Experimental results on Test B set** 

In this section, we evaluate our proposed method on the Test B set following the continuous learning process, aiming to demonstrate that the observed improvements are not simply due to overfitting on the test set. Similar to the Test 

3 

Table 5. Comparisons of our proposed method against other continual learning methods. The table presents the performance of different methods across various seen and unseen categories. ”Ours(CPL+Fast)” represents our method’s results for continually learned policies without slow system reasoning. 

|||||||||**Seen Ca**|**tegories**||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|||||||||||||||||
|EWC [26]|0.71|0.80|0.33|0.72|0.71|0.40|0.78|0.96|0.56|0.71|0.85|0.80|0.38|0.76|0.15|0.90|
|LwF [33]|0.88|0.73|0.41|0.81|0.90|0.40|0.83|0.88|0.37|0.82|0.90|0.84|0.51|0.88|0.30|0.93|
|Experience Replay[46]|0.83|0.73|0.50|0.84|0.85|0.26|0.72|0.88|0.56|0.75|0.90|0.79|0.42|0.83|0.23|0.90|
|Ours(CPL+Fast)|0.90|0.75|0.58|0.87|0.95|0.46|0.89|0.92|0.50|0.78|0.90|0.85|0.63|0.90|0.38|0.90|
|||**Seen**|**Catego**|**ries**||||||**Unsee**|**n Categ**|**ories**|||||
|**Method**|||||**AVG**|||||||||||**AVG**|
|EWC [26]|0.20|0.68|0.53|0.90|0.68|0.00|0.29|0.50|0.33|0.35|0.52|0.47|0.56|0.25|0.87|0.42|
|LwF [33]|0.40|0.73|0.67|0.80|0.75|0.27|0.53|0.67|0.83|0.92|0.64|0.65|0.78|0.47|0.93|0.62|
|Experience Replay[46]|0.00|0.70|0.61|0.80|0.71|0.00|0.40|0.61|0.66|0.57|0.58|0.56|0.68|0.34|0.93|0.52|
|Ours(CPL+Fast)|0.60|0.71|0.74|0.90|0.79|0.27|0.61|0.71|0.50|0.92|0.69|0.69|0.80|0.70|0.81|0.69|


set, the Test B set consists of 1,081 manipulation scenarios involving 30 different objects. To simulate real-world applications, we adjusted the relative positions between the robot and the objects in the Test B set compared to the Test set. It is important to note that the Test B set is not used for any fine-tuning. The model’s performance on the Test B set is recorded after each iteration of continual policy learning on the Test set. 

The results presented in Table 6 highlight the robustness and adaptability of our SC-VLA in a continual learning context. After four iterations of updates, our method does not overfit the Test set and demonstrates significant performance improvements across various object categories in the Test B set. Notably, our approach shows superior performance in categories such as _Laptop (LT)_ , _Phone (PH)_ , and _Refrigerator (RF)_ . This consistency underscores our model’s ability to mitigate catastrophic forgetting effectively, ensuring sustained high performance through the integration of the Exponential Moving Average and finetuning process. 

## **F. Details of close-loop experiments** 

In the ”Main Results on Manipulation” section, we validate that SC-VLA can effectively perform both open-loop and closed-loop control in multiple tasks. In this section, we provide the detailed settings and experiment table for the closed-loop experiments. Specifically, we use the well-known closed-loop benchmark, RLBench [22], as our closed-loop dataset. Five representative tasks with different manipulation trajectories were selected, including “take USB out of computer,” “close fridge,” “close box,” “toilet seat down,” and “unplug charger.” The evaluation met- 

rics follow previous works [22], assessing task success rate based on predefined success conditions. For the model input, we utilize the front-view image from a third-person perspective, as this view fully captures the manipulated object without occlusion. The key frame filtering method follows the previous work [48]. We use 7-DoF to control the Franka Panda robot arm, including not only the position and rotation of the end-effector but also the opening and closing state of the gripper. As shown in Table 7, we compare our proposed method with the previous MLLM-based SOTA method [31] under the same experimental setting. Ours (Fast + Slow) achieves an average success rate of 91%, improving accuracy by 23% compared to ManipLLM. The results demonstrate that our slow system can also perform corrections for closed-loop control, showcasing the generalizability of our method. 

## **G. Additional related work** 

In this section, we present additional related work that could not be fully discussed in the main text, highlighting the broader research landscape and its relation to our work. Specifically, we examine recent advances in multimodal large language models and techniques for robotic failure correction. These discussions underscore the strengths and limitations of existing approaches, motivating our development of a slow system that not only corrects errors but also continuously learns from corrective feedback. 

**Multimodal Large Language Models.** Large language models (LLMs) have shown impressive reasoning capabilities across downstream tasks [11, 53]. In multi-modal reasoning, Multimodal Large Language Models (MLLMs) [3, 28, 70] excel in bridging modalities. BLIP [28, 29] pre- 

4 

Table 6. **Performance on Test B set.** The success rate is recorded after each iteration of continual policy learning on the Test set. 

||||||||**S**|**een Ca**|**tegories**||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|||||||||||||||||
|Ours-cl-turn1|0.69|0.70|0.25|0.81|0.71|0.33|0.83|0.88|0.62|0.60|1.00|0.74|0.31|0.71|0.07|0.93|
|Ours-cl-turn2|0.71|0.58|0.16|0.67|0.85|0.40|0.78|0.80|0.56|0.75|0.66|0.76|0.42|0.74|0.07|0.93|
|Ours-cl-turn3|0.80|0.63|0.33|0.74|0.90|0.53|0.75|0.73|0.62|0.67|1.00|0.74|0.38|0.81|0.07|1.00|
|Ours-cl-turn4|0.80|0.75|0.41|0.74|0.85|0.40|0.70|0.76|0.68|0.67|1.00|0.79|0.27|0.85|0.15|1.00|
|||**Seen**|**Catego**|**ries**||||||**Unsee**|**n Categ**|**ories**|||||
|**Method**|||||**AVG**|||||||||||**AVG**|
|Ours-cl-turn1|0.00|0.56|0.29|0.60|0.61|0.00|0.26|0.35|0.00|0.71|0.26|0.65|0.53|0.12|0.62|0.32|
|Ours-cl-turn2|0.00|0.56|0.33|0.80|0.61|0.00|0.29|0.52|0.00|0.50|0.45|0.56|0.43|0.17|1.00|0.40|
|Ours-cl-turn3|0.00|0.62|0.43|0.80|0.65|0.18|0.33|0.57|0.50|0.64|0.53|0.65|0.68|0.27|0.93|0.49|
|Ours-cl-turn4|0.20|0.57|0.46|1.00|0.66|0.18|0.44|0.56|0.33|0.71|0.57|0.65|0.68|0.25|0.93|0.51|


Table 7. **The close-loop experiments.** “Fast” and “Slow” represent our method’s results for the fast system’s direct pose prediction and the slow system’s corrected prediction based on expert prompts, respectively. “Mean” represents the average manipulation success rate across all tasks. 

|Method|Ref|Take USB out|Close fridge|Close box|Toilet seat down|Unplug charg|er<br>Mean|
|---|---|---|---|---|---|---|---|
|ManipLLM|CVPR2024|0.45|0.90|0.55|0.95|0.55|0.68|
|Ours(Fast)|-|0.55|0.70|0.40|0.90|0.60|0.63|
|Ours(Fast+Slow)|-|0.85|0.95|0.75|1.0|1.0|0.91|


trains encoder-decoder models with image-text pairs, enhancing vision-language understanding by adding synthetic captions and filtering noise. LLaVA [37] and MiniGPT4 [72] introduce simple fully connected layers between image encoders and LLMs, emphasizing dataset pre-training and instruction tuning. Some MLLMs [5, 35, 55, 57] focus on vision-centric tasks, confirming MLLMs’ capacity for fine-grained perceptual results. Additionally, 3D MLLMs [18, 19, 58, 65] extend reasoning and conversational abilities to 3D modalities. 

**Robotic Failure Correction.** While these approaches—namely REFLECT [40], MULTIREACT [67], DoReMi [17], and CLAIRify [50] effectively address lowlevel execution failures, they do so by directly correcting immediate errors (such as 6 DoF end-effector poses) without incorporating the corrective feedback into a learning framework. REFLECT leverages LLMs to reason from summaries of past experiences, using failure explanations to refine planning; MULTIREACT employs a visionlanguage model [45] as a reward mechanism to identify and autonomously recover from intermediate execution failures; DoReMi focuses on promptly detecting misalignments between planned and executed actions and then recovering from these discrepancies; and CLAIRify uses iterative prompting combined with program verification to en- 

sure the validity of action plans. These approaches, as mentioned above, are adept at handling immediate, low-level corrections but lack the ability to learn from the corrective interventions they perform. This limitation undermines their long-term adaptability and practical deployment in dynamic, real-world settings. In contrast, our work aims to develop a slow system that enables multi-modal large language models (MLLMs) not only to autonomously correct end-effector poses but also to continually incorporate and learn from the corrective feedback, thereby enhancing robustness and overall performance over time. 

## **H. Model architecture of SC-VLA** 

As shown in Figure 6 , to equip our model with foundational reasoning abilities for robotic manipulation, we load pretrained parameters from LLaMA-Adapter V2 [12]. This choice provides flexibility, as our approach can easily accommodate other MLLMs as the base model. As illustrated in Figure 2(in the main text), the model architecture is composed of several key components. When presented with an RGB image, we use the CLIP visual encoder [45] to extract visual features. Simultaneously, a language prompt is processed by the pre-trained LLaMA tokenizer [53] to produce textual embeddings. To enable multimodal comprehension, our MLLM employs a projection layer to align 

5 


Figure 6. **Detail architecture of SC-VLA.** 

the visual tokens from CLIP with the token embeddings of the LLaMA language model. This alignment allows the LLaMA model to understand both visual and textual information, thereby generating corresponding answers, such as the predicted end-effector pose for manipulation tasks. During training, we fine-tune only the injected adapters [20] within the LLaMA model, keeping the majority of the pretrained parameters frozen. This strategy preserves the robust capabilities of the pre-trained MLLM while enhancing the model with additional functionalities specific to manipulation and failure correction tasks. By injecting taskspecific knowledge through adapters, we ensure that our model remains efficient without the need for large-scale retraining. 

## **I. Advantages of fast & slow systems** 

The dual-process structure in our model offers significant advantages in balancing speed, efficiency, and robustness for robotic manipulation tasks. By decomposing the action sequence into high-frequency predictions managed by the fast system and low-frequency corrections by the slow system, the model achieves an optimal allocation of computational resources. This separation enables rapid, direct pose predictions essential for responsive manipulation, while the slow system selectively intervenes to ensure accuracy and robustness, particularly under uncertain conditions. 

sented as: 


where _X_ fast handles high-frequency, immediate responses, and _X_ slow captures the corrective actions. This decomposition allows the model to allocate more resources to the fast system for most interactions, activating the slow system only when necessary. This approach effectively reduces computational load and improves response times without compromising accuracy. 

In robotic manipulation, entropy reflects SC-VLA’s uncertainty regarding a specific action or prediction. This design’s key advantage is its ability to mitigate cumulative errors by reducing the overall uncertainty of the model’s predictions through decreased entropy. The slow system specifically targets and corrects high-entropy actions, effectively reducing the entropy _H_ ( _X_ ) of the action sequence: 


where _H_ ( _X_ slow) represents the entropy reduction achieved through corrective interventions. This entropy minimization improves the reliability of predictions by reducing the risk of error propagation, especially in complex or novel manipulation tasks. 

Furthermore, the fast system benefits from an adaptive Exponential Moving Average (EMA) update mechanism, incorporating corrections from the slow system to continuously improve performance. The EMA update is given by: 


where _α_ is dynamically adjusted based on task complexity or recent feedback. This adaptive weighting allows the model to prioritize recent corrections, enhancing the accuracy of future predictions across varying manipulation conditions. As a result, the model maintains high performance on both seen and unseen scenarios without extensive retraining. 

The hierarchical design also supports an efficient approach to task execution, where the fast system generates initial, coarse predictions, and the slow system provides precision corrections as needed. This layered strategy improves the success rate of tasks and enables scalability to new scenarios, as evidenced by significant performance gains (see Table 1 in the main text). The dual-process model thus offers an effective balance of speed, precision, and adaptability, demonstrating its robustness in complex, realworld robotic applications. 

Mathematically, the action sequence _X_ can be repre- 

6 

