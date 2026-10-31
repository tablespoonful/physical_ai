---
title: "Selective Perception for Robot: Task-Aware Attention in Multimodal VLA"
date: "2026-02-17"
authors: "Young-Chae Son; Jung-Woo Lee; Yoon-Ji Choi; Dae-Kwan Ko; Soo-Chul Lim"
url: https://arxiv.org/abs/2602.15543
pdf: https://arxiv.org/pdf/2602.15543
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.15543)** / [論文ページ](https://arxiv.org/abs/2602.15543)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Selective Perception for Robot: Task-Aware Attention in Multimodal VLA 

Young-Chae Son<sup>_‡_</sup> , Jung-Woo Lee<sup>_‡_</sup> , Yoon-Ji Choi, Dae-Kwan Ko, Soo-Chul Lim* Dongguk University 


Fig. 1: **Operational process of the proposed model.** (a) **Camera Router Module:** The router utilizes the wrist camera and text prompt to analyze the current context and predict the real-time importance of each modality. (b) **Task-Aware Attention:** Based on the router’s prediction, the model selectively attends to the most informative visual streams. (c) **Real-world Execution:** Robot action sequence for Task 3 ( _Rotate the valve on the hot side and hold down the front button_ ). 

**_Abstract_ —In robotics, Vision-Language-Action (VLA) models that integrate diverse multimodal signals from multi-view inputs have emerged as an effective approach. However, most prior work adopts static fusion that processes all visual inputs uniformly, which incurs unnecessary computational overhead and allows task-irrelevant background information to act as noise. Inspired by the principles of human active perception, we propose a dynamic information fusion framework designed to maximize the efficiency and robustness of VLA models. Our approach introduces a lightweight adaptive routing architecture that analyzes the current text prompt and observations from a wristmounted camera in real-time to predict the task-relevance of multiple camera views. By conditionally attenuating computations for views with low informational utility and selectively providing only essential visual features to the policy network, Our framework achieves computation efficiency proportional to task relevance. Furthermore, to efficiently secure large-scale** 

**annotation data for router training, we established an automated labeling pipeline utilizing Vision-Language Models (VLMs) to minimize data collection and annotation costs. Experimental results in real-world robotic manipulation scenarios demonstrate that the proposed approach achieves significant improvements in both inference efficiency and control performance compared to existing VLA models, validating the effectiveness and practicality of dynamic information fusion in resource-constrained, real-time robot control environments.** 

## I. INTRODUCTION 

To realize general-purpose robotic intelligence that can flexibly adapt to diverse task environments, research on Vision–Language–Action (VLA) models that integrate visual, linguistic, and action-related information has been accelerating [1], [2], [3], [4], [5]. While early VLA models pre- 

dominantly relied on RGB images as their primary visual input [6], [7], [1],this approach often exhibits limitations in real-world environments. Consequently, recent research has expanded to incorporate diverse sensory modalities, such as depth information [8], [9], [10], tactile signals [11], [12], [13], [14], and audio cues [15], [16], into the model. Such research on multimodal integration [17] demonstrates that specialized tasks, previously unachievable by existing VLAs, can be performed while preserving large-scale prior knowledge. 

However, these approaches remain limited to static fusion, resulting in only an expansion of input modalities. Such static fusion suffers from two fundamental limitations. First, it gives rise to issues of information redundancy and interference. When irrelevant data are indiscriminately projected into highdimensional feature spaces, it hinders effective representation learning and degrades both training efficiency and convergence speed. Second, it can result in a degradation of robustness. At certain stages, irrelevant modalities can act as noise that dilutes meaningful information, negatively affecting the model’s reliability and generalizability. 

The importance of sensory information varies according to the type of tasks in real-world environments. To address these challenges, the human cognitive system employs active perception which actively modulates the weights of sensory information based on task contexts and goals [18]. This demonstrates that multimodal sensory processing involves not only integration but also inhibitory interactions across modalities [19], [20], [21]. This suggests that human perception does not indiscriminately process all sensory inputs; rather, it leverages attention to suppress irrelevant signals and selectively allocate resources to information most relevant to the current task. For example, in _Turn off an overheated electronic device_ task, humans rely on visual localization cues during the initial exploration phase, shift their attention to thermal sensing when assessing potential risk, and prioritize tactile feedback during object grasping. During this process, other sensory inputs are temporarily suppressed or attenuated. This implies that humans dynamically select which sensory modality to trust based on the task phase and objective, thereby minimizing interference from irrelevant information. 

Inspired by the selective inhibition mechanisms observed in human perception, we propose a Dynamic Routing-based adaptive multimodal fusion approach that dynamically suppresses task-irrelevant sensory data rather than processing all inputs uniformly. In contrast to prior approaches that rely on expert-defined rules or manually segmented phase labels, we introduce a Vision–Language Model (VLM)–based autolabeling pipeline that enables the generation of supervisory signals for large-scale datasets without human intervention. Furthermore, the proposed router is integrated with a Flow Matching–based VLA policy network, enabling it to be trained during robot fine-tuning without the need for additional training data or labeling. Consequently, the proposed framework avoids indiscriminate information fusion by prioritizing the integration of the most relevant modalities at each time step, thereby minimizing information interference in high- 

dimensional feature spaces and improving both task accuracy and efficiency. 

**The key contributions of this work are summarized as follows:** 

- **Context-Aware Router & Gating:** We propose a Dynamic Router that uses the wrist-mounted camera as an anchor to predict modality importance in real-time. 

- **Robustness in Long-Horizon Tasks:** By leveraging a router-based feature fusion structure to integrate key modalities, we mitigate inter-modality interference and achieve higher success rates than existing methods on long-horizon manipulation tasks. 

- **Scalable VLM Supervision:** We construct a VLM-based auto-labeling pipeline to obtain labeled data for router training, generating camera labels without additional data collection costs. 

## II. RELATED WORKS 

## _A. Vision-Language-Action (VLA) Models for Robotics_ 

Vision-Language-Action (VLA) models, which integrally understand vision, language, and action information, enable robots to perform general-purpose tasks by simultaneously comprehending visual context and language instructions [1], [2], [3]. However, complex interactions in real-world environments cannot be fully captured using only 2D image information. Previous studies have improved success rates on specific tasks by leveraging additional sensor modalities [22], [23], [24], [25], [26], [27]. For instance, the integration of tactile information is essential for tasks requiring precise contact, such as peg-in-hole tasks. Although TLA [13] demonstrated an 85% success rate using tactile information alone, the absence of visual feedback limited its ability to capture the global context of the task. Addressing this limitation, VTLA [14] introduced the Vision-Tactile-Action-Prompt dataset fusing visual and tactile inputs, leading to significantly more refined control performance. Furthermore, research has extended to leverage audio information. ManiWAV [16] demonstrated that auditory data, such as contact sounds or the sound of liquid flow, can serve as key cues to compensate for the uncertainty of visual information. Multimodal approaches have shown promising results, but most existing models still rely on static fusion strategies that process all incoming sensory data with fixed weights. This approach fails to account for the relative importance of information based on the task context and can lead to information interference due to the inclusion of unnecessary modalities. 

## _B. Adaptive Sensory Fusion and Modality Weighting_ 

For complex tasks in real-world environments, the relative importance of each sensory modality varies dynamically with the task context [28], [29], [30]. As a result, research has investigated adaptively controlling modality-specific weights according to task stages. With respect to visual information, prior work has explored predicting feature importance for each camera view in multi-view settings to reweight and fuse features [31]. In addition, Long-VLA [32] demonstrated that 


Fig. 2: **Overview of the proposed framework.** (a) Experiment Setup (b) Architecture of the proposed framework and the dynamic router. The router takes the wrist camera and langage prompt feed as inputs to predict importance weights for multiple visual sources, including external, thermal, and tactile cameras, thereby prioritizing task-relevant sensor information. 

masking unnecessary visual information based on the task stage can enhance success rates in long-horizon tasks. 

Recent studies have also explored approaches that leverage physical properties. Play to the Score [29] proposed a method that dynamically fuses diverse sensory information by adjusting modality weights in real-time, in a manner analogous to human perception. This approach demonstrated the capability to autonomously learn and determine when and which information to prioritize, rather than being limited to simple multimodal integration. FOAR [30] introduced a structural gating approach that modulates the weight of force/torque data based on contact status, thereby effectively mitigating noise interference in non-contact scenarios. However, this approach relied on manual annotation by humans. To address this limitation, subsequent studies proposed dynamically fusing visual and tactile modalities through attention-based architectures designed to predict future contact forces [33]. Despite these efforts, research on dynamically adjusting weights for each sensory modality in VLA frameworks remains limited. To address this, we propose leveraging the context-aware capabilities of VLMs to explicitly define modalities optimized for the task context and train the model to learn task-relevant sensory information. 

## _C. Scalable Supervision and Automated Labeling_ 

Traditional data curation for robotic learning relies on manual human annotation. However, this approach is costly and prone to inconsistency due to annotator fatigue or varying levels of expertise [33], [34]. Recent studies have demonstrated that Large Language Models (LLMs) and Vision Language 

Models (VLMs) can perform diverse tasks by leveraging their extensive prior knowledge and high-level reasoning capabilities [35], [36]. In particular, the visual reasoning capabilities of VLMs have been shown to effectively support robotic task execution [37]. Building upon these findings, recent studies have shown that VLM-based automated labeling can serve as a viable alternative for overcoming these limitations [38], [39]. For example, AutoRT [40] demonstrated that leveraging VLMs enables scene understanding and reasoning, thereby effectively scaling up the size of training dataset. Adopting this approach, we utilize VLMs to alleviate the burden of manual annotation in constructing large-scale datasets. Specifically, our approach designs the VLM to automatically assign relative importance weights to key multimodal features. This enables the Router, trained alongside a VLA model, to make real-time decisions on sensory modality prioritization while performing tasks. 

## III. METHOD 

In this section, we propose a VLA model architecture that operates effectively in multi-view environments. To achieve this, we introduce a Camera Router between the ViT and the pretrained VLM. This module computes the importance of the input information from each viewpoint. This importance ensures that visual information provided to the policy network is proportional to its relevance for task execution. This section is organized as follows: Section A presents the integrated training process of the Router and the VLA model, Section B details the architecture of the Camera Router, and Section C outlines the methodology for constructing a dataset for Router training using VLMs. 


Fig. 3: **Overview of VLA Training with Dynamic Router.** The Camera Router predicts importance weights ( _W_ ) for multiple camera views, acting as a gating mechanism. This allows the VLA framework to selectively prioritize task-relevant visual information during the action training process. 

## _A. Training with Vision Language Action Model_ 

Fig. 2 illustrates the training process for both the VLA and the router. Full fine-tuning of large-scale VLA models for specific tasks requires substantial computational resources and large-scale training data. To address these computational and data efficiency challenges, we adopt a fine-tuning strategy that applies LoRA to the pretrained base policy [3]. This approach keeps the billions of parameters in the pretrained base policy frozen. Instead, we insert lightweight, trainable LoRA modules into all weight groups of both the VLM and the Action expert, and train only these specific modules using our collected dataset. This approach enables us to perform the desired task actions using only 50 episodes and minimal computational resources, while preserving the extensive prior knowledge of base policy. The proposed framework is trained in an end-to-end manner to simultaneously achieve optimal robotic action generation and efficient camera routing. The overall loss function _L_ total is defined as a weighted sum of the action loss for action prediction and the routing loss for router optimization: 


where _λ_ represents the weight for routing loss function, which is set to 0.1 to ensure effective routing performance without degrading the primary action prediction objective. 

We use Flow Matching Loss for _L_ action, in accordance with the training strategy of the base policy. During training, the Camera Router is supervised using _L_ routing, while simultaneously being optimized to improve the VLA’s action prediction performance through gradient backpropagation from _L_ action. Finally, the router weight and the projection layer undergo 

full parameter updates, whereas only the LoRA parameters are updated for the VLA backbone, thereby maximizing training efficiency. 

## _B. Camera Router Architecture_ 

Fig. 3 illustrates the overall architecture of the proposed router. To perceive the current context, the router takes the wrist camera image and the task prompt as inputs. The detailed feature extraction process proceeds as follows. First, We apply Attention Pooling to the task prompt to obtain the text feature _h_ prompt that captures core keywords. In parallel, the wrist camera tokens are transformed into the visual feature _h_ wrist through Mean Pooling. In this paper, the wrist camera is designated as the base anchor view and designed to remain always active. This design ensures the stable availability of proximal visual information, which is considered essential for robotic manipulation. 


Finally, the router input _x_ is defined as the concatenation of the prompt and wrist camera features, which is then passed through an MLP and a Softmax layer to predict the importance weights _W_ for the remaining _K −_ 1 views. 


_1) Dynamic Gating:_ The Dynamic Router predicts the weights _w_ , which determine the contribution of each modality to the ongoing task and are applied in conjunction with a learnable parameter _γ ∈_ R<sup>_D_</sup> . 


Fig. 4: **Experimental Setup for Each Task.** (a) Battery Sorting, (b) Wire Selection, and (c) Valve Operation. While all tasks share a dual RGB camera system for visual perception, each setup incorporates task-specific modalities—such as thermal cameras or tactile sensors—to provide complementary sensory information. 

Here, _γ_ is a scaling parameter for mitigating abrupt changes during the gating process and enhancing training stability. Through this process, features from camera views with lower importance are naturally attenuated, while task-relevant visual information is relatively emphasized. Subsequently, the visual features are concatenated along the channel dimension and fused into a unified visual representation. Specifically, the wrist camera feature _F_ wrist is concatenated with the gated external camera and multimodal features _F_ external<sup>_′_,</sup><sup>_F ′_</sup> thermal<sup>,</sup> and _F_ tactile<sup>_′_. The concatenated features are then projected back</sup> to the original embedding dimension using a linear projection. Finally, the fused feature _F_ fused is used as the input for the pretrained VLM, providing the model with visual information that is selectively emphasized based on the task context. 

_2) Imbalanced Routing Learning:_ In robotic manipulation tasks, certain sensory modalities (e.g. tactile, thermal) are not required throughout the entire task, but are sparsely needed only at specific moments involving contact or decisionmaking. Due to this data imbalance, the use of a standard cross-entropy loss may lead to biased model training. To address the imbalance of sparsely occurring ground-truth labels, we train the router using Focal Loss. 


Focal Loss reduces the influence of easy samples, thereby reweighting the learning focus toward difficult and sparsely occurring instances. This approach allows for effective training by preventing the router from missing sparse, high-value moments. We set _α_ focal = 0 _._ 25 and _β_ = 2 _._ 0. 

## _C. Auto-Labeling with VLM Labels_ 

Task decomposition has been explored in robotics, as such structured approaches [41], [42] are known to enhance task performance. However, manually annotating task stages or required sensory data for every frame in large-scale datasets is prohibitively time-consuming and expensive, posing a bottleneck to scalability. To address this challenge, we established an automated pipeline utilizing Qwen3-VL [43] to recognize 

task phases within videos and automatically generate the corresponding camera importance labels. Determining the robot’s state from a single frame alone is inherently ambiguous. For example, a static grasping state can be difficult to interpret as either the onset of Transporting or Placing. To overcome this limitation, we employ a History-Aware Prompting strategy that incorporates past action history in addition to the current visual information. The collected input videos are segmented into chunks of _T_ = 30 frames. To capture the temporal context within each chunk, we uniformly sample _K_ = 10 images, which are fed into the VLM. To facilitate context understanding, the prompt is constructed using the following key elements: 

- 1) _Role:_ The assigned persona defining the agent’s behavioral context. 

- 2) _Task Description:_ The overall objective of the task. 

- 3) _Workflow Definition:_ The sequence of actions during task execution. 

- 4) _Gripper Action:_ The scalar value representing the gripper’s opening width. 

- 5) _Action History:_ A summary of the previous three chunks. 

Through this process, the VLM jointly considers the visual inputs and contextual information to determine the activation status of each camera according to predefined rules: 


The generated _D_ vlm provides supervision for the Router through the Focal Loss described in Section B, enabling it to learn critical segments. 

IV. EXPERIMENT 

## _A. Experimental Setup_ 

Fig. 4 illustrates the experimental setup for each task. A wrist-mounted camera (Intel RealSense D435) and an external camera (Intel RealSense L515) are utilized across all tasks, with task-specific sensors incorporated for each scenario. Specifically, Task 1 incorporates a thermal camera (ThermoEye TMC256B) to acquire thermal data, while Task 

TABLE I: **Quantitative comparison of subtask success rates.** Bold values indicate the best performance in each row. 

||**w/o **|**Router**|||**w/ Router**||
|---|---|---|---|---|---|---|
|**Policy Input**|**w/o Multimodal**|**w/ Multimodal**|**Router Input**|**Wrist Cam + State**|**Ext. Cam + Prompt**|**Wrist Cam + Prompt**|
|**Task1**|0.00%|30.00%|**Task1**|20.00%|**90.00%**|**90.00%**|
||(0/10)|(3/10)||(2/10)|**(9/10)**|**(9/10)**|
|**Task2**|0.00%|0.00%|**Task2**|60.00%|70.00%|**90.00%**|
||(0/10)|(0/10)||(6/10)|(7/10)|**(9/10)**|
|**Task3**|0.00%|0.00%|**Task3**|10.00%|60.00%|**70.00%**|
||(0/10)|(0/10)||(1/10)|(6/10)|**(7/10)**|
|**Average SR**|**0****_._00****_±_ 0****_._00%**|**10****_._00****_±_ 17****_._32%**|**Average SR**|**30****_._00****_±_ 26****_._46%**|**73****_._33****_±_ 15****_._28%**|**83****_._33****_±_ 11****_._55%**|


2 is equipped with a tactile sensor (Meta Digit). Task 3 utilizes both sensors. 

_1) Experimental datasets:_ To train the VLA Executor, we collected 50 expert demonstrations for each task. The dataset consists of four components: _State_ , _Action_ , _Image_ , and _Task prompt_ . 


_State_ is a 7-dimensional vector containing the robot’s 6 joint angles and the gripper state, and _Action_ is a 7-dimensional vector comprising the 6 target joint angles and the gripper command. _Image_ is collected via the wrist camera, the external camera, and additional sensors. All cameras were synchronized at a frame rate of 15 Hz; the wrist and external cameras captured 640 _×_ 480 RGB images, while the thermal camera captured 256 _×_ 192 thermal images. The thermal data was normalized within a standard ambient temperature range to ensure consistency, and then colorized for use. Tactile images were captured at a resolution of 640 _×_ 480 and subsequently normalized to enhance visibility before being employed. Finally, the _Task prompt_ consists of the target task description provided in natural language. 

_2) Experimental Tasks:_ The proposed method was evaluated in scenarios set in industrial environments, selected from diverse real-world settings. In industrial environments, relying only on RGB camera data is often insufficient for tasks such as detecting component overheating or sorting micro-parts; therefore, such tasks require diverse sensory information, including thermal and tactile data. For example, when performing a pickand-place operation with a heated object, thermal information becomes crucial during the detection phase. Similarly, tactile information is essential during processes such as comparing object thickness or physically interacting with the object. Motivated by these attributes, we designed three tasks where determining the object’s state is difficult using a single sensory modality alone. By structuring tasks where a specific modality is highly relevant only at certain stages, we aim to verify whether the proposed model can dynamically select and utilize necessary sensory information while suppressing irrelevant inputs based on the context. 

## **Task 1: Battery Sorting (Visual + Thermal)** 

The objective of this task is to discard the overheated battery while transferring the normal-temperature battery onto 

a conveyor belt. Since the thermal state of the batteries is indistinguishable using RGB cameras alone, the robot must selectively activate the thermal camera to accurately sort the normal battery. This task allows verification of whether the Router dynamically modulates the importance of thermal information during relevant task phases. 

## **Task 2: Wire Selection (Visual + Tactile)** 

This task involves sorting two types of wires with differing thicknesses into pre-assigned bins. Specifically, thin wires must be placed at the rear, while thick wires are positioned at the front. To make visual distinction difficult, wires of identical color were selected, with a diameter difference of approximately 0.4 mm. Since this minute difference in thickness can be visually ambiguous, the robot must determine the wire’s thickness using tactile feedback upon grasping. This task allows us to verify whether the Router dynamically modulates the importance of tactile information during relevant task phases. 

**Task 3: Valve Operation (Visual + Thermal + Tactile)** This is an emergency shutdown task simulating a pipeline overheating and leakage accident in an industrial setting. Multiple hoses and valves, along with a switch, are positioned in front of the robot. Upon detecting overheating in one of the hoses, the robot is tasked with rotating the corresponding valve to the open position, followed by pressing the switch to terminate the operation. In this scenario, the thermal camera is required for detecting overheating, while tactile information is necessary for rotating the valve. While Tasks 1 and 2 verified the selective utilization of a single auxiliary modality, Task 3 assesses the model’s capability to integrate and coordinate multiple sensory modalities. 

## _B. Analyzing Learning Efficiency with a Router_ 

In this paper, we propose a Dynamic Router that integrates multimodal information by assigning context-dependent weights. Table I summarizes the overall experimental results. We validate the proposed method through experiments, demonstrating its effectiveness in improving the task success rate in complex environments. The evaluation is based on the success of individual sub-tasks. Each task follows a longhorizon sequence and requires inference based on multimodal visual feedback during execution. The baseline policy using only RGB input ( _w/o Multimodal_ ) failed to achieve any 


Fig. 5: **Performance on Long-Horizon Sequential Tasks.** (a) Illustration of the three-stage task progression (b) Success rates for each sub-task. Our method demonstrates sustained performance across the entire sequence, highlighting its robustness in long-horizon manipulation scenarios. 

success across all tasks. In contrast, incorporating multimodal feedback resulted in a success rate of 10%. In contrast, the proposed method achieved a success rate of 73.33%. In the following sections, we analyze these performance differences focusing on three key aspects: Router input configurations, long-horizon robustness, and the efficacy of VLM labeling. 

_1) Router Input Comparison:_ To identify the optimal input configuration for the router in our proposed method, we conducted comparative experiments on the following three combinations. 

- Wrist Camera + Prompt: The router is trained using wristmounted camera observations and prompts. 

- Wrist Camera + State: The router is trained using wristmounted camera observations and robot states. 

- External Camera + Prompt: The router is trained using external camera observations and prompts. 

We observed that the model demonstrated superior performance when _Wrist Cam + Prompt_ was utilized as inputs, reaching an average of 83.33%. Meanwhile, the _External Cam + Prompt_ method achieved a relatively decent average success rate of 73.33%; however, this represents a performance decrease of 10% compared to the proposed method. We attribute this to the characteristics of our experimental 

setup, where the physical distance and perspective differences inherent to the fixed external view posed relative constraints in capturing fine-grained contacts or the precise timing of manipulation. In contrast, the _Wrist Cam_ provided an egocentric view in close proximity to the target objects. This offered a distinct advantage in clearly distinguishing object state changes and task phases, particularly within the fine manipulation tasks required in this study. The _Wrist Cam + State_ configuration yielded a significantly lower success rate. We hypothesize that raw state information, without specific processing, acted as noise rather than a meaningful feature, thereby hindering training convergence. Notably, in Task 1, the performance of _Wrist Cam + State_ method even fell below that of the baseline model. This negative transfer suggests that providing inconsistent data to the router can adversely affect performance. In particular, incorrect routing decisions may lead the policy model to focus on sensor data that are irrelevant to the current task. In conclusion, the experimental results demonstrate that effective router training enhances the manipulation performance of multimodal VLA models. 

_2) Long-Horizon Tasks with Dynamic Router:_ Fig. 5 presents the long-horizon task performance of the proposed method ( _w/ Router_ ). Prior VLA-based approaches tend to 


Fig. 6: Performance comparison on Tasks 1–3 over 10 trials across three settings: no-labeled baseline, human-labeled, and VLM-labeled datasets. 

achieve relatively stable performance on short-horizon tasks; however, as the number of steps increases, their performance often degrades due to unstable skill chaining and error accumulation, as reported in prior work [44], [32]. Experimental results show that the baseline model exhibits a gradual decline in success rate as the number of task steps increases. In contrast, the proposed method consistently maintains a high average success rate of 83.33% across all evaluation tasks. We attribute this improvement to the router-provided weights, which serve as an implicit step-awareness signal for the VLA model, helping it preserve task context even in long-horizon sequences. 

Furthermore, the proposed approach reduces the negative impact of noise on reasoning performance by selectively filtering out irrelevant modalities. Existing models, which utilize all sensory information with equal weighting, tend to exhibit an higher failure rate as the task horizon extends, even if they successfully process the first object. By selectively attending only to task-relevant information, our method improves success rates over continuous multi-step task execution. Experimental analysis indicates that failures of the proposed method are mainly caused by object drops during transport or grasping failures, while it consistently made accurate decisions about which sensors were critical. These findings demonstrate that, in VLA training with sensory inputs, a routing mechanism that dynamically selects necessary information is more effective than naive modality fusion for high-level situational understanding and the completion of complex manipulation tasks. 

_3) Validation of VLM Labeling:_ In this study, we propose an automated labeling method that leverages VisionLanguage Models (VLMs) capable of high-level reasoning and situational assessment. To validate our approach, we trained routing policies using VLM-generated labels and compared 

them against policies trained with human annotations, using task success rate as the primary evaluation metric. For each task, we conducted 10 trials and reported performance as the proportion of successful executions. 

Accurate sensory labeling requires not only task understanding but also the ability to identify which sensory inputs are essential at each stage of execution. The results are summarized in Fig. 6. Across all tasks, VLM-based labeling achieved an average success rate of 83.33%, which is comparable to the 86.67% obtained with human labeling. Across the three tasks, VLM can select task-relevant sensory information given human prompts, especially in scenarios where spatial relations among objects, temporal task structure, and contextual cues are critical. 

Specifically, Tasks 1 and 2 require selecting and executing appropriate actions based on the states of two objects. Task 3 requires inferring the correct outcome (e.g., closing the appropriate valve) from environmental conditions such as the temperature of a connecting hose. These results demonstrate the practical potential of VLM-based labeling to either replace or complement human annotation. This is valuable in robot learning, where labeling costs increase rapidly as the dataset scales. In such environments, VLM-driven automated labeling provides promising approach to streamline data collection and dataset construction. 

## V. CONCLUSION 

In this work, we proposed a framework to enhance the efficiency and robustness of multimodal robotic manipulation. We introduced a Dynamic Router that utilizes wrist camera images and task prompts to predict real-time modality importance based on the task context. By minimizing interference from irrelevant information, our method demonstrated improved success rates in long-horizon tasks that require accurate reasoning over sensory data. Furthermore, our framework leverages a Vision-Language-Model(VLM) to determine sensory weights without the need for additional data collection or human labeling. Consequently, the resulting Vision-LanguageAction (VLA) model achieved performance comparable to baselines trained with human supervision. While this study primarily focused on selectively leveraging multimodal inputs such as vision, tactile, and thermal signals, force feedback from physical interactions also offers valuable cues. Future work aims to expand the input dimensions of the Dynamic Router to incorporate these diverse modalities. We anticipate that such extensions, combined with further validation, will further enhance the robustness and generalizability of the proposed approach. 

## REFERENCES 

- [1] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2679–2713. 

- [2] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, C. Xu, J. Luo, T. Kreiman, Y. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- [3] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-language-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [4] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang _et al._ , “Spatialvla: Exploring spatial representations for visual-language-action model,” _arXiv preprint arXiv:2501.15830_ , 2025. 

- [5] R. Sapkota, Y. Cao, K. I. Roumeliotis, and M. Karkee, “Vision-languageaction models: Concepts, progress, applications and challenges,” 2025. [Online]. Available: https://arxiv.org/abs/2505.04769 

- [6] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _arXiv preprint arXiv:2212.06817_ , 2022. 

- [7] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [8] C. Li, J. Wen, Y. Peng, Y. Peng, F. Feng, and Y. Zhu, “Pointvla: Injecting the 3d world into vision-language-action models,” _arXiv preprint arXiv:2503.07511_ , 2025. 

- [9] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” in _International Conference on Machine Learning_ , 2024. 

- [10] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 3157–3181. 

- [11] J. Huang, S. Wang, F. Lin, Y. Hu, C. Wen, and Y. Gao, “Tactilevla: Unlocking vision-language-action model’s physical knowledge for tactile generalization,” _arXiv preprint arXiv:2507.09160_ , 2025. 

- [12] J. Yu, H. Liu, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai _et al._ , “Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation,” _arXiv preprint arXiv:2505.22159_ , 2025. 

- [13] P. Hao, C. Zhang, D. Li, X. Cao, X. Hao, S. Cui, and S. Wang, “Tla: Tactile-language-action model for contact-rich manipulation,” _arXiv preprint arXiv:2503.08548_ , 2025. 

- [14] C. Zhang, P. Hao, X. Cao, X. Hao, S. Cui, and S. Wang, “Vtla: Visiontactile-language-action model with preference learning for insertion manipulation,” _arXiv preprint arXiv:2505.09577_ , 2025. 

- [15] W. Zhao, P. Ding, M. Zhang, Z. Gong, S. Bai, H. Zhao, and D. Wang, “Vlas: Vision-language-action model with speech instructions for customized robot manipulation,” _arXiv preprint arXiv:2502.13508_ , 2025. 

- [16] Z. Liu, C. Chi, E. Cousineau, N. Kuppuswamy, B. Burchfiel, and S. Song, “Maniwav: Learning robot manipulation from in-the-wild audio-visual data,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 947–962. 

- [17] J. Jones, O. Mees, C. Sferrazza, K. Stachowicz, P. Abbeel, and S. Levine, “Beyond sight: Finetuning generalist robot policies with heterogeneous sensors via language grounding,” in _Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

- [18] D. Birman and J. L. Gardner, “A flexible readout mechanism of human sensory representations,” _Nature communications_ , vol. 10, no. 1, p. 3500, 2019. 

- [19] M. Ide and S. Hidaka, “Tactile stimulation can suppress visual perception,” _Scientific reports_ , vol. 3, no. 1, p. 3453, 2013. 

- [20] M. Ide, S. Hidaka, H. Ikeda, and M. Wada, “Neural mechanisms underlying touch-induced visual perceptual suppression: An fmri study,” _Scientific reports_ , vol. 6, no. 1, p. 37301, 2016. 

- [21] S. Hidaka and M. Ide, “Sound can suppress visual perception,” _Scientific reports_ , vol. 5, no. 1, p. 10483, 2015. 

- [22] D.-K. Ko, K.-W. Lee, D. H. Lee, and S.-C. Lim, “Vision-based interaction force estimation for robot grip motion without tactile/force sensor,” _Expert Systems with Applications_ , vol. 211, p. 118441, 2023. 

- [23] K.-W. Lee, Y. Qin, X. Wang, and S.-C. Lim, “Dextouch: Learning to seek and manipulate objects with tactile dexterity,” _IEEE Robotics and Automation Letters_ , 2024. 

- [24] X. Zhao, M. Li, C. Weber, M. B. Hafez, and S. Wermter, “Chat with the environment: Interactive multimodal perception using large language models,” in _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2023, pp. 3590–3596. 

- [25] L. Sun, D. K. Jha, C. Hori, S. Jain, R. Corcodel, X. Zhu, M. Tomizuka, and D. Romeres, “Interactive planning using large language models 

for partially observable robotic tasks,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 14 054–14 061. 

- [26] W. Lai, T. Zhang, T. L. Lam, and Y. Gao, “Vision-language modelbased physical reasoning for robot liquid perception,” in _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2024, pp. 9652–9659. 

- [27] Z. Liang, Y. Xu, Y. Hong, P. Shang, Q. Wang, Q. Fu, and K. Liu, “A survey of multimodel large language models,” in _Proceedings of the 3rd International Conference on Computer, Artificial Intelligence and Control Engineering_ , 2024, pp. 405–409. 

- [28] A. Krishna, E. Hu, and D. Jayaraman, “The value of sensory information to a robot,” in _International Conference on Representation Learning_ , Y. Yue, A. Garg, N. Peng, F. Sha, and R. Yu, Eds., vol. 2025, 2025, pp. 90 348–90 376. 

- [29] R. Feng, D. Hu, W. Ma, and X. Li, “Play to the score: Stage-guided dynamic multi-sensory fusion for robotic manipulation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 340–363. 

- [30] Z. He, H. Fang, J. Chen, H.-S. Fang, and C. Lu, “Foar: Force-aware reactive policy for contact-rich robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [31] Z. Lan, W. Mao, H. Li, L. Wang, T. Wang, H. Fan, and O. Yoshie, “Bfa: Best-feature-aware fusion for multi-view fine-grained manipulation,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 9, pp. 8930–8937, 2025. 

- [32] Y. Fan, P. Ding, S. Bai, X. Tong, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang, Z. Fan, B. Chen, and D. Wang, “Long-vla: Unleashing long-horizon capability of vision language action model for robot manipulation,” 2025. [Online]. Available: https://arxiv.org/abs/2508.19958 

- [33] J. Li, T. Wu, J. Zhang, Z. Chen, H. Jin, M. Wu, Y. Shen, Y. Yang, and H. Dong, “Adaptive visuo-tactile fusion with predictive force attention for dexterous manipulation,” _arXiv preprint arXiv:2505.13982_ , 2025. 

- [34] T. Yu, H. Zhang, Q. Li, Q. Xu, Y. Yao, D. Chen, X. Lu, G. Cui, Y. Dang, T. He _et al._ , “Rlaif-v: Open-source ai feedback leads to super gpt-4v trustworthiness,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 19 985–19 995. 

- [35] T. Kwon, N. Di Palo, and E. Johns, “Language models as zero-shot trajectory generators,” _IEEE Robotics and Automation Letters_ , 2024. 

- [36] H. Singh, R. J. Das, M. Han, P. Nakov, and I. Laptev, “Malmm: Multiagent large language models for zero-shot robotics manipulation,” _arXiv preprint arXiv:2411.17636_ , 2024. 

- [37] A. Mei, G.-N. Zhu, H. Zhang, and Z. Gan, “ReplanVLM: Replanning Robotic Tasks With Visual Language Models,” _IEEE Robotics and Automation Letters_ , vol. 9, no. 11, pp. 10 201–10 208, Jan. 2024, conference Name: IEEE Robotics and Automation Letters. 

- [38] L. Chen, J. Li, X. Dong, P. Zhang, C. He, J. Wang, F. Zhao, and D. Lin, “Sharegpt4v: Improving large multi-modal models with better captions,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 370– 387. 

- [39] Y. Wang, Z. Xian, F. Chen, T.-H. Wang, Y. Wang, K. Fragkiadaki, Z. Erickson, D. Held, and C. Gan, “Robogen: Towards unleashing infinite data for automated robot learning via generative simulation,” in _ICML_ , 2024. 

- [40] M. Ahn, D. Dwibedi, C. Finn, M. G. Arenas, K. Gopalakrishnan, K. Hausman, B. Ichter, A. Irpan, N. Joshi, R. Julian _et al._ , “Autort: Embodied foundation models for large scale orchestration of robotic agents,” _arXiv preprint arXiv:2401.12963_ , 2024. 

- [41] E. Triantafyllidis, F. Acero, Z. Liu, and Z. Li, “Hybrid hierarchical learning for solving complex sequential tasks using the robotic manipulation network roman,” _Nature Machine Intelligence_ , vol. 5, no. 9, pp. 991– 1005, 2023. 

- [42] M. Dalal, M. Liu, W. Talbott, C. Chen, D. Pathak, J. Zhang, and R. Salakhutdinov, “Local policies enable zero-shot long-horizon manipulation,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 13 875–13 882. 

- [43] S. Bai, Y. Cai, R. Chen _et al._ , “Qwen3-vl technical report,” _arXiv preprint arXiv:2511.21631_ , 2025. 

- [44] Y. Yang, J. Sun, S. Kou, Y. Wang, and Z. Deng, “Lohovla: A unified vision-language-action model for long-horizon embodied tasks,” _arXiv preprint arXiv:2506.00411_ , 2025. 

## APPENDIX 

## _A. Attention Analysis for Modality Selection_ 

The proposed router model takes wrist camera images and prompts as inputs and outputs probability weights indicating the importance of sensory information in the current state. In this section, we visualize attention maps to analyze which regions of the visual input the router attends to during sensor selection and examine whether it associates the semantic meaning of the prompt with the physical interaction state. Fig. 7 compares raw wrist camera images and attention maps for the valve operation task, divided into nine key frames. The red regions in the heatmaps indicate areas of high activation. 

During the initial phase where the robot approaches the valve, the router focuses on the center of the target valve, suggesting recognition of the object specified in the prompt and prioritization of visual information for path planning. When the gripper attempts to contact the valve, attention shifts to the interface between the valve and the Digit sensor mounting area, corresponding to the phase of physical contact and indicating increasing relevance of tactile sensing. During valve rotation, attention is distributed along the geometry of the handle, while in the verification stage, it spreads across the valve and surrounding regions to assess task completion. Based on these visual cues, the router dynamically adjusts weights for the external view, thermal, and tactile modalities to perform complex manipulation tasks. 

## _B. Task Definitions and Qualitative Analysis_ 

Fig. 8 illustrates the complete execution sequences for the three experimental tasks, displaying the observations captured from each modality. This figure demonstrates how distinct sensory modalities provide unique information at each stage 

_Task 1: Sorting Battery (Visual + Thermal):_ thermal information serves as a critical modality during the object detection and discrimination phases. While the heated battery is indistinguishable from the other battery in the wrist and external camera images, it can be reliably identified based on the thermal image. _Task 2: Wire Selection (Visual + Tactile):_ tactile information serves as a critical modality during the object detection and discrimination phases. While it is challenging to visually distinguish between two wires with a thickness difference of only 0.4 mm using RGB camera images, the tactile sensor exhibits distinct patterns corresponding to the wire thickness, enabling accurate comparison and identification. _Task 3: Valve Operation (Visual + Thermal + Tactile):_ thermal and tactile information are both utilized as crucial modalities. The thermal camera is employed to identify which hose is generating heat in the initial phase, while tactile feedback ensures a secure grip during valve rotation. We selected these three tasks to demonstrate that sensory information is not uniformly required throughout task execution, and that specific modalities become critical only at particular stages, as shown in Fig. 8. Instead, specific modalities play a decisive role at specific stages. This suggests that the proposed model improves performance by selectively 

focusing on sensory information relevant to the current context, rather than processing all modalities uniformly. 

## _C. VLM Prompt Design_ 

The Vision Language Model employed in this study is Qwen3-VL-30B-A3B-Instruct. To prevent the model from drawing premature conclusions based solely on visual information, we designed the system to guide the reasoning process in a step-by-step manner. The specific reasoning process is structured into the following four stages. First, we analyze the robot’s movement direction. We primarily determine whether the motion is horizontal or vertical to initially classify the task phases into those dominated by horizontal movement and those dominated by vertical movement. Second, we verify the open/closed status of the gripper. This determination is based on integrating both the visual input and the robot’s actual gripper state. To mitigate the potential difficulty of the model in discerning fine-grained robot states solely from visual information, we explicitly injected the current gripper state into the prompt. Third, we verify the visibility of key objects, such as valves and buttons, within the current camera view. Finally, we perform a workflow consistency verification. By referencing the history of previous plans, we conduct a final verification to ensure that the preceding analysis results logically align with the predefined task sequence, before outputting the determined stage. 

## **Auto Labeled VLM Prompt** 

**Role:** You are an expert who analyzes the robot’s actions to activate the appropriate camera. 

**Task:** _Rotate the valve on the hot side and hold down the front button._ 

**Gripper Action:** _Gripper Action_ **Action History:** _History of Action_ **Workflow Definition:** The task is divided into six phases. Each phase specifies the expected robot behavior, gripper state, movement direction, and the most informative camera modality. 

_Approaching phase:_ The robot searches for the valve while keeping the gripper open and performing left or right movements. 

Analyze the 10 image frames and sensor data: 

- 1) Movement: Is the robot moving Left/Right (Approaching/Transporting) or Up/Down (Adjusting/Lifting/Pressing)? 

- 2) Gripper State: Is the gripper closing (Grasping), opening (Lifting), or stable? 

- 3) Visual Cues: What objects are visible (valve, button, gripper state)? 

- 4) Sequence Check: Strict order is Approaching _→_ Adjusting _→_ Grasping _→_ Lifting _→_ Transporting _→_ Pressing. No skipping or reversing. 


Fig. 7: **Visualization of Attention Maps in the Proposed Model** (a) Real robot manipulation sequence showing the progression of the task, including approaching, grasping, rotating, and lifting stages. (b) The router takes the wrist camera view and the prompt as inputs. We visualize the attention over the wrist camera view to illustrate how the router focuses on task-relevant regions across different stages of the manipulation task. 


Fig. 8: **Camera Views over Time for Each Task.** Each column represents temporal progression, while rows show sensory observations from different modalities. Task 1 (Battery Sorting), Task 2 (Wire Selection), Task 3 (Valve Operation). 

