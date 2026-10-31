---
title: "Transferring Vision-Language-Action Models to Industry Applications: Architectures, Performance, and Challenges"
date: "2025-09-27"
authors: "Shuai Li; Chen Yizhe; Li Dong; Liu Sichao; Lan Dapeng; Liu Yu"
url: https://arxiv.org/abs/2509.23121
pdf: https://arxiv.org/pdf/2509.23121
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.23121)** / [論文ページ](https://arxiv.org/abs/2509.23121)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Transferring Vision-Language-Action Models to Industry Applications: Architectures, Performance, and Challenges 

1<sup>st</sup> Shuai Li 2<sup>nd</sup> Yizhe Chen 3<sup>rd</sup> Dong Li _Shenyang Institute of Automation Shandong Normal University Shenyang Institute of Automation Chinese Academy of Sciences_ Shandong, China _Chinese Academy of Sciences_ Shenyang, China 2023317064@stu.sdnu.edu.cn Shenyang, China lishuai1@sia.cn lidong@sia.cn 4<sup>th</sup> Sichao Liu 5<sup>th</sup> Dapeng Lan 6<sup>th</sup> Yu Liu* 7<sup>th</sup> Zhibo Pang _Department of Production Engineering University of Chinese University of Chinese Department of Intelligent Systems Royal Institute of Technology (KTH) Academy of Sciences Academy of Sciences Royal Institute of Technology (KTH)_ Stockholm, Sweden Beijing, China Beijing, China Stockholm, Sweden sicliu@kth.se dapengl@ieee.org liu.yu@ieee.org zhibo@kth.se 

**_Abstract_ —The application of artificial intelligence (AI) in industry is accelerating the shift from traditional automation to intelligent systems with perception and cognition. Visionlanguage-action (VLA) models have been a key paradigm in AI to unify perception, reasoning, and control. Has the performance of the VLA models met the industrial requirements? In this paper, from the perspective of industrial deployment, we compare the performance of existing state-of-the-art VLA models in industrial scenarios and analyze the limitations of VLA models for real-world industrial deployment from the perspectives of data collection and model architecture. The results show that Pi0, after fine-tuning, achieves approximately 60% success rate on simple grasping tasks, while the positional error in highprecision placing tasks reaches up to 2.2 cm and 12.4°. There is much room for performance improvement in complex industrial environments, diverse object categories, and high-precision placing tasks. Our findings provide practical insight into the adaptability of VLA models for industrial use and highlight the need for task-specific enhancements to improve their robustness, generalization, and precision.** 

**_Index Terms_ —Vision-Language-Action, VLA, Industrial Artificial Intelligence** 

## I. INTRODUCTION 

Traditional control methods (e.g., PID control) demonstrate precise and reliable performance in the execution of a structured environment and repetitive tasks. Visual servoing can precisely align a screwdriver tip to M4-M8 screws, with average error of 0.8-1.3 mm [1]. However, there are significant challenges when dealing with an unstructured environment characterized by complex, dynamic, and diverse tasks, such as inefficient human interactions, limited manufacturing tasks, and a lack of self-learning intelligence [2]. 

This work has been submitted to the IEEE for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible. This work is supported by Liaoning Liaohe Lab with project number LLL24ZZ-02-01 and LLL24ZZ-02-02. 

Vision-language-action (VLA) models are multimodal AI systems that integrate visual perception, language understanding, and action generation within a unified framework [3], [4]. First, vision-language models (VLMs) pre-trained in Internetscale data [5]–[7] exhibit strong vision-language alignment capabilities, allowing open-vocabulary visual question answering in daily life scenarios [8]–[10]. Building upon these pre-trained VLMs, VLA models can be further trained on large-scale robot data, equipping them with basic control capabilities. These models generate control commands conditioned on visual input and natural language instructions through autoregressive or diffusion-based policy heads [11]–[17]. Besides, unlike daily life and laboratory scenarios, industrial environments are characterized by distinct technical indicators (e.g., illumination intensity _≥_ 500 lx, vibration amplitude _±_ 0 _._ 5 mm). Fine-tuning with collected industrial task-specific data enables the transfer of pre-trained VLA models originally designed for dailylife scenarios into industrial scenarios. This adaptation allows VLA models to retain their inherent generalization capabilities, enabling them to handle tasks in partially unstructured environments to a certain extent. 

TABLE I 

COMPARISON OF REVIEW STUDIES ON VLA 

|**Survey**|**Year**|**General**|**Specific**|**VLA Coverage**|**Quantitative Evaluation**|**Applications**|
|---|---|---|---|---|---|---|
|Ma et al.|2024|✓|✗||✗|✗|
|Sapkota et al.|2025|✓|✗|80|✗|✗|
|This Survey.|2025|✓|✓|18|✓|✓|


However, can the state-of-the-art VLA fulfill the industry requirement? To what extent must performance be improved to align with the anticipated objectives? These questions are still unclear. As shown in Table I, existing surveys focus on summarizing methods in general domains. VLA mod- 

els are designed primarily for autonomy, intelligence, and adaptability. However, they still face limitations in terms of operational precision, real-time responsiveness, and system stability when deployed in industrial settings. These limitations can be attributed to three key factors: 

- Lack of large-scale industrial data: Pre-trained VLMs fail to align domain-specific natural language instructions (e.g.,‘insert the shaft into the press-fit bearing’) with corresponding visual inputs, limiting their out-of-distribution (OOD) generalization capabilities in industrial scenarios. 

- High-precision requirements in an unstructured environment: Occlusions, diverse object categories, and complex spatial arrangements in an unstructured environment impose stringent demands on the control accuracy of VLA models. Although they can perform random picking within a single task, precision placing tasks remain a challenge. 

- Computational resources and inference latency: The larger models typically require substantial memory and exhibit slow inference speeds. While action chunking has been introduced to improve inference efficiency, it inherently presents a trade-off: larger chunk sizes enhance speed but compromise fine-grained control accuracy. 

In this study, we focus on evaluating the applicability and adaptability of VLA models in complex industrial environments. Specifically, we investigate the potential of VLA systems for use in real-world manufacturing settings, particularly under unstructured and dynamic conditions. 

The main contributions of this study are as follows. 

- We evaluated the performance of state-of-the-art VLA models in picking and placing tasks within industrial scenarios. 

- We analyze the adaptability of VLA models to unstructured environments from two perspectives: dataset and model architecture. Furthermore, we also discuss potential directions to improve their robustness and task generalization. 

## II. RELATED WORK 

Unstructured environments characterized by complex, dynamic, and diverse tasks demand VLA models that exhibit generalization, control precision, and computational efficiency. Thus, we categorize prior works by their capabilities in highprecision requirements, real-time execution, and deployability. 

## _A. High-precision Requirements_ 

To meet high-precision requirements, VLA models require accurate imitation of demonstration data and fine-grained alignment between language and observations. 

**Visual perception:** Visual-language grounding and spatial understanding. Embodied Chain-of-Thought (ECoT) is a structured reasoning mechanism that trains VLA models to perform multiple steps of reasoning about plans, subtasks, motions, and visually grounded features such as object bounding boxes and end effector positions, before predicting robot action [18]. ECoT improves the perceptual effectiveness of 

VLA models by explicitly guiding the alignment between subtasks and spatial features. EMMA-X [19] is an embodied multimodal action model with a grounded chain of thought and spatial reasoning, allowing for finer task decomposition and significantly improving success rates over ECoT and OpenVLA. Both models transform language and observations into interpretable, structured, and controllable planning units. 3D-VLA [20] unifies 3D perception, reasoning, and action with a generative world model. It enhances spatial understanding and localization in complex scenes by leveraging point cloud perception. Using natural language as a shared semantic representation, FuSe [21] proposes a cross-modal finetuning approach to integrate heterogeneous sensory modalities, such as touch and audio, into pre-trained VLA models (e.g., Octo [22] and PaliGemma [9]), thus improving robustness in visually degraded conditions such as occlusion or low lighting. 

**Language understanding:** Task decomposition and semantic reasoning. Through large-scale pretraining, VLM models acquire the ability to 1) align natural language instructions with visual context to enable semantic understanding of task goals; 2) identify and localize task-relevant entities (e.g., objects, spatial relations). RoboVLMs [23] conducts over 600 systematic experiments across CALVIN, SimplerEnv, and real-world robot platforms such as Kinova Gen3, evaluating eight different VLM models. The results consistently show that more substantial vision-language alignment leads to better downstream control performance, with models such as KosMos [24] and PaliGemma [9] outperforming others. Beyond these, models such as Prismatic VLMs [8], Qwen2VL [25], and Eagle-2 [10] are also commonly adopted as VLM backbones in recent VLA frameworks. Furthermore, the flexibility of VLM-based architectures supports modular VLA design, where VLMs can be paired with various policy heads, including autoregressive, diffusion, and hybrid, to predict action sequences. In summary, VLMs serve as the semantic backbone of VLA, mapping multimodal perception to middlesemantic and planning representation through their powerful alignment and generalization capabilities. 

**Action generation:** Action head design and control accuracy. OpenVLA [11] discretizes each action dimension into 256 uniformly spaced tokens based on quantile statistics and embeds these tokens directly into the LLaMA tokenizer. FAST [12] improves on this by applying the Discrete Cosine Transform to compress action sequences, followed by Byte Pair Encoding to generate compact and information-dense tokens. Compared to OpenVLA, this representation enables faster training and higher precision in high-frequency tasks. Models such as Pi0 [14], GR00T-N1 [16], and GraspVLA [17] use flow matching to align visual language conditions with continuous action trajectories, ensuring policy stability and precision. RDT-1B [13] and CogACT [15] employ probabilistic diffusion denoising models to model the distribution from visual language inputs to actions, enabling highfidelity trajectory synthesis through multistep sampling. These continuous-space diffusion approaches generally outperform discrete tokenization methods in both representation quality 

and control accuracy. DiVLA [26] adopts a ’reasoning-thendiffusion’ framework, where an autoregressive module first performs task interpretation and subgoal decomposition, which is subsequently followed by a diffusion module responsible for fine-grained action generation. This design enhances both interpretability and execution accuracy by decoupling highlevel semantic reasoning from low-level motion synthesis. HybridVLA [27] advances this direction by integrating autoregressive and diffusion-based mechanisms within a unified vision language model. Through coordinated training and action ensemble strategies, it delegates diffusion modules to handle fine-grained motion control, while autoregressive modules are tasked with stage-level task planning. This complementary design enables each component to focus on its respective strength during execution. 

## _B. Model Efficiency and Real-Time Responsiveness_ 

Real-time responsiveness is essential for deploying VLA models in the real world, where latency directly impacts control stability. A series of recent works focus on model compression, lightweight architecture design, and adaptive inference strategies. SARA-RT [28] introduces a robust self-adaptive attention mechanism that replaces traditional softmax attention with efficient linear attention through up-training, enabling large-scale VLA models such as RT-2 to achieve real-time inference without compromising performance. TinyVLA [29] replaces the conventional autoregressive policy head with a diffusion-based policy head, enabling parallelizable and lowlatency inference while maintaining high action precision. Evaluated for both simulated and real-world robotic tasks, TinyVLA demonstrates up to 20× lower latency and superior success rates compared to OpenVLA, all without relying on robot-specific large-scale pretraining. DeeR-VLA [30] proposes a dynamic early-exit mechanism designed for multimodal LLMs. By dynamically distributing computation across time steps based on prediction confidence, it achieves 5–6× reductions in FLOPs and memory consumption with negligible performance degradation. In addition, diffusion-based models can also generate action sequences with large chunk sizes, balancing real-time and accuracy. 

## _C. Deployability_ 

Deployability is a crucial consideration for the practical application of VLA models in industrial applications. We evaluated deployability from three dimensions: (1) open source model and code, (2) validation on real-world robot data, and (3) existence of real-world deployment demonstrations. Among existing works, the work stands out for its high level of openness and deployment on real robots, such as GR-1 and Mobile ALOHA. 

technical components within the prevalent methodological paradigms. Detailed insights into the technical components of various prevalent methods are delineated in Table II. Several primary technological modules encompass normalization and unnormalization, augmentation, a projector, pre-trained VLM, and policy heads. A comprehensive overview of each module is provided below. 


Fig. 1. Generalized technical framework for VLA. 

## _A. Normalization and unnormalization_ 

Normalization eliminates dimensional inconsistencies across different tasks or robotic platforms, thereby enabling the model to learn consistent distributions of actions and states. As illustrated in Fig. 1, normalization and unnormalization are applied to both actions and states, depending on the model design. Specifically, normalization maps raw physical values (e.g., joint positions, gripper poses) into standardized ranges, facilitating stable learning and generalization. Unnormalization reverses this transformation, converting model output back into task-specific or robot-specific physical units for execution. VLA models can be broadly categorized into two types based on whether proprioceptive state inputs are used: action-only normalization, used when the model does not explicitly take robot state as input; action-and-state normalization, used when both are fed into the policy network. Common normalization strategies include: Quantile normalization, Z-score normalization (standardization to zero mean and unit variance), and Min-Max normalization (scaling values to a fixed interval such as [–1, 1]). 

## _B. Augmentation_ 

## III. ARCHITECTURE OF VLA 

The existing reviews lack sufficiently detailed analyses of technical components, so we propose a generalized technical framework for VLA, as shown in Fig. 1. The framework can be interpreted as the disassembly and amalgamation of 

Augmentation is applied to both visual observations and language instructions, enabling the VLM backbone to better handle perceptual variability and instruction diversity. Image augmentation includes standard techniques such as random cropping, color jittering, image corruption, and adding 

Gaussian noise. These techniques are critical to improving robustness against variations in camera pose, illumination, and background clutter, which frequently occur in real-world robotic deployments. Instruction enhancement typically involves prompt variation, paraphrasing, or template-based sampling, which helps the language model generalize across semantically equivalent but syntactically diverse instructions (e.g., ‘grasp the red block’ vs. ‘pick up the red cube’). 

## _C. Projector_ 

Visual observations are encoded by a vision encoder into a high-dimensional latent representation, while language instructions are embedded via pre-trained LLM tokenizers. However, these representations typically differ in both dimensionality and semantic space. The projector serves as a bridge between the vision encoder and the LLM and is designed to perform both dimension alignment and semantic mapping. A projector network, often implemented as a linear layer, MLP, or FusedMLP, allows visual tokens to be concatenated or interleaved with language tokens as input to the LLM or the policy heads. These networks are defined by the following equation, where image embeddings **e** image _∈_ R<sup>_L×h_text</sup> is output by a learned projector **F** _ψ_ 


where linear projector **F**<sup>linear</sup> _ψ_ consists of a single linear layer; MLP projector **F**<sup>mlp</sup> _ψ_ consists of two Linear layers and a GELU activation layer in between; FusedMLP projector **F**<sup>fused</sup> _ψ_ comprises three linear layers interleaved with two GELU activation layers. In particular, RDT-1B uses linear projectors to align **e** image and **e** instruction. 

## _D. Pre-trained VLM_ 

Formally, pre-trained VLM takes as input an image **x** image _∈_ R<sup>_H×W_</sup> and language instruction **x** instruction. These inputs are then fed to the vision encoder and the pre-trained LLM. 

**Vision Encoder:** Vision encoders are responsible for extracting rich spatial and semantic representations from raw visual observations. Common choices include ViT-based models such as DINOv2 [31] and SigLIP [32]. Different vision encoders offer complementary strengths in visual representation. DINOv2, a self-supervised ViT-based model, excels at capturing fine-grained spatial details and low-level geometric features, making it suitable for tasks requiring precise spatial reasoning and object localization. In contrast, SigLIP, a contrastive vision-language pre-training model, emphasizes semantic alignment and extracts high-level conceptual features that are strongly correlated with language instructions. Vision encoders are defined by the following equation. 


where _Vω_ represents the vision encoders, _p_ image _∈_ R<sup>_L×h_vision</sup> could be the patch features output by DINOV2 and SigLIP. 

**Language Encoder/Pre-trained LLM:** LLMs serve as the core of reasoning and decision making in VLA architectures. 

They interpret natural language instructions, align them with visual representations, and generate either structured task representations or direct control actions. Common choices include LLaMA, Gemma, Qwen2-VL, and SmolLM2, which are typically used in frozen or lightly fine-tuned configurations. The LLM takes as input the tokenized language instruction embedding **e** instruction along with the visual embeddings **e** image. This process is defined by the following equation. 


where LM _θ_ represents the LLM, **e** image and **e** instruction are concatenated. 

## _E. Policy heads_ 

The policy head serves as the final component in VLA, mapping the fused language vision representations _f_ gen to robot actions. Depending on the type of action space and the task requirements, different architectural variants and training objectives have been proposed. There are three main architectural types: autoregressive, diffusion, and hybrid models. 

**Autoregressive:** Autoregressive-based policy heads typically adopt a De-tokenizer structure, treating action prediction as a next-token prediction task over discretized tokens. These heads are optimized with cross-entropy (CE) loss. 

**Diffusion:** Diffusion-based policy heads operate in continuous action space and predict actions by denoising a noisy trajectory input. It includes different architectures, such as the DiT architecture, the Gemma architecture, and the scaleDP. These heads are optimized with Mean Squared Error (MSE) loss or flow-matching loss. 

**Hybrid:** Depending on the architecture, LLM-dominant designs integrate diffusion modeling into the autoregressive prediction of the next token within a single LLM. In contrast, diffusion-dominant designs use a diffusion model as the main trajectory generator, with the LLM providing semantic conditioning or latent planning inputs. These heads are typically optimized with a combination of MSE and CE loss, aligning continuous action prediction with a discrete planning structure. 

## _F. Action space_ 

The design of the action space directly impacts the tradeoff between control precision and learning efficiency. Joint space and task space control are the two dominant action modes for controlling robot arms within the robot learning literature [33]. Furthermore, the action space can be further divided into absolute and relative control modes. Both are defined by the following equation. 


where ∆ _x,_ ∆ _y,_ ∆ _z_ are the relative translation offsets of the end effector, ∆ _ϕ,_ ∆ _θ,_ ∆ _ψ_ denote the rotation changes. _AJ ∈_ R<sup>_n_</sup> , where _n_ is the number of joints in the robot arm. _g_ indicates the gripper’s open/close state. 

TABLE II 

CONSTITUENTS OF DIVERSE PREVALENT METHODS 

|**Method**|**Normalize**|**Augmentat**|**ion**|**Projector**|||**Pre-trained VLM**|**Policy Head**|**Unnormalize**|**Loss**|**Chunk size**|**Frequency (hz)**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||**Image Augmentation**|**Instruction Augmentation**|**Image**|**Text**|**Vision Encoder**|**Language Encoder/Pre-trained LLM**||||||
|OpenVLA|Quantile|||Linear, MLP, FusedMLP||DinoV2, SigLIP|Llama2-7B|De-Tokenizer|Quantile|CE||5|
|RDT-1B||color jittering, image corruption,<br>and Gaussian noise|GPT-4-Turbo|Linear|Linear|SigLIP|T5-XXL|DiT||MSE|64|381|
|Pi0|Z-score|||Linear||SigLIP|Gemma (2.6B)|Gemma (300M)|Z-score|Conditional Flow Matching|50|50|
|Pi0-Fast|Z-score|random crop, random brightness,||Linear||SigLIP|Gemma(2.6B)|De-Tokenizer|Z-score|CE||50|
|CogACT|Quantile|random contrast, random saturation,<br>and random hue||Linear, MLP, FusedMLP||DinoV2, SigLIP|Llama-2-7B|DiT|Quantile|MSE|16|80|
|GR00T-N1|Min-max|||MLP||SigLIP-2|SmolLM2|DiT|Min-max|Flow Matching|16|120|
|DiVLA|Z-score||GPT-4o|MLP||SigLIP|Qwen2-VL|ScaleDP|Z-score|MSE+CE|16|82|
|HybridVLA|Quantile|||Linear, MLP, FusedMLP||DinoV2, SigLIP|Llama-2-7B|De-Tokenizer, MLP|Quantile|MSE+CE||9.4|


In unstructured environments, absolute joint angle control ensures high precision and repeatability by avoiding inverse kinematics (IK) and its associated issues. However, it has lower training efficiency and limited generalization. In contrast, relative end-effector control offers better sample efficiency and generalization but depends on IK and lacks the precision and safety required in industrial settings. 

## IV. EVALUATION OF VLA 

We aim to evaluate the robustness and generalizability of VLA models in real-world industrial environments. To do this, we design a structured benchmark comprising three industrial scenarios, focusing on the models’ ability to perform random object picking and precision placing. 

## _A. Experiment setups_ 

**Task:** We consider four types of perturbation commonly encountered in industrial deployments: visual occlusion, camera jitter, object pose randomisation, and object diversity. An illustration of each task, detailed definitions, and visualizations are provided in Fig. 2. 

**Data:** We fine-tune the VLA model using episodes collected from real-world industrial scenarios, and 100 episodes are used for each task individually. 

**Method:** To evaluate VLA, we select Pi0 in robotic foundation models from deployability and real-time. As OpenVLA and CogACT rely solely on third-person demonstrations, their performance under occlusion conditions is limited due to the lack of egocentric visual input. 

**Metric & Hardware:** We employ the success rate (%) as our main metric, which is calculated by dividing the successful trials by the total number of trials. The model is fine-tuned on an NVIDIA H20 96GB GPU for 10 hours using Ubuntu 20.04 and ROS 1 noetic. All tests are performed on the Mobile ALOHA dual-arm robot. Every trial incorporates object pose randomization and diverse object categories, 10 trials in total. 

## _B. Results analysis_ 

In the zero-shot setting, none of the evaluated VLA models successfully completed the grasping task. Table III provides a quantitative assessment of the effects of visual occlusion and camera jitter on task performance. All results were obtained after fine-tuning the models in real-world demonstrations. H- O and W-O denote the occlusion of head and wrist cameras, respectively, where 30% of the pixels in the entire image 


Fig. 2. Task definition and visualization. 

are randomly masked. H-J refers to the head camera jitter. Performance degrades significantly under head and wrist camera occlusion (H-O, W-O), especially in Task 2, suggesting that visual occlusion has a more pronounced impact under object diversity. The relatively stable results under H-J across tasks imply the model’s robustness to moderate head camera jitter. However, the average error (2.2 cm, 12.4°) highlights a substantial potential for improvement when deploying Pi0 in unstructured environments. 

TABLE III 

QUANTITATIVE RESULTS 

|Method||**Random **|**Pick U**|**p**||**Precisi**|**on Plac**|**e**||**Error**|
|---|---|---|---|---|---|---|---|---|---|---|
|||**H-O**|**W-O**|**H-J**||**H-O**|**W-O**|**H-J**|**Distance **|**(cm)**<br>**Orientation (°)**|
|Pi0-task1|60|50|60|60|40|20|20|20|||
|Pi0-task2|40|30|30|40|40|30|20|30|||
|Pi0-task3|50|40|30|40|50|20|20|30|2.2|12.4|


## V. DISCUSSIONS 

The deployment of VLA models in industrial settings introduces unique challenges due to the unstructured and dynamic nature of these environments. Based on the empirical results in Section IV, we revisit two key questions that directly reflect the gap between current VLA capabilities and industrial requirements. 

Q1: Why do VLA models struggle to generalize to unstructured industrial environments? Most existing VLA models are designed for general-purpose or household manipulation tasks, focusing on broad generalization over precision. Industrial environments exhibit unique challenges such as visual occlusions, camera motion jitter, and diverse object arrangements, which are rarely addressed in existing architectures. 

For example, they lack explicit mechanisms to handle partial observability or visual disturbances and do not incorporate feedback loops to correct actions based on execution outcomes. Moreover, the limited availability of demonstration data and the scarcity of vision-language aligned datasets result in poor zero-shot transferability of VLA models to new robot arms and task layouts. Our experiments indicate that successful adaptation typically requires hundreds of domainspecific episodes for fine-tuning. 

Q2: Why do VLA models not yet satisfy industrial control requirements? In terms of action space design, the use of absolute joint angle control is more suitable for high-precision tasks compared to relative end-effector control, which relies on inverse kinematics and introduces instability in constrained workspaces. However, the inference latency of large VLA models (often below 10 Hz) poses challenges for real-time industrial deployment. These delays lead to unstable execution, including motion jitter and lag, which severely affect task reliability in industrial deployments. Moreover, current VLAs are highly sensitive to the distribution of training data. Differences in robot arm, joint configuration, or frequency between platforms require extensive data collection and retraining, which undermines general-purpose deploymentability. 

## VI. CONCLUSIONS 

In this study, we evaluated state-of-the-art VLA models in real-world industrial scenarios to assess their applicability. While current models show the ability to perform randomized object picking under occlusion and jitter, their placing accuracy remains below industrial standards, with errors typically at the centimeter level. Our analysis attributes the limitations of VLA models to meet industrial requirements (high accuracy, real-time responsiveness, deployability) to limited high-quality industrial data, high computational demands, and insufficient attention to deployment constraints in model design. Despite some task adaptability, these models lack generalization across embodiments. Future work should focus on improving perceptual robustness, enabling real-time feedback, and developing lightweight architectures to bridge the gap toward industrial deployment. 

## REFERENCES 

- [1] J. Xue et al., “High-Precision Transformer-Based Visual Servoing for Humanoid Robots in Aligning Tiny Objects,” arXiv preprint arXiv:2503.04862, 2025. 

- [2] J. Xu, Q. Sun, Q. Han, Y. Tang, ”When Embodied AI Meets Industry 5.0: Human-Centered Smart Manufacturing,” IEEE/CAA Journal of Automatica Sinica, vol. 12, no. 3, pp. 485-501, 2025. 

- [3] R. Sapkota, Y. Cao, K. I. Roumeliotis, and M. Karkee, “VisionLanguage-Action Models: Concepts, Progress, Applications and Challenges,” arXiv preprint arXiv:2505.04769, 2025. 

- [4] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on vision-language-action models for embodied ai,” arXiv preprint arXiv:2405.14093, 2024. 

- [5] D. A. Hudson and C. D. Manning, “Gqa: A new dataset for real-world visual reasoning and compositional question answering,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2019, pp. 6700–6709. 

   - [7] P. Sharma, N. Ding, S. Goodman, and R. Soricut, “Conceptual captions: A cleaned, hypernymed, image alt-text dataset for automatic image captioning,” in Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2018, pp. 2556–2565. 

   - [8] S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh, “Prismatic vlms: Investigating the design space of visuallyconditioned language models,” 2024. 

   - [9] L. Beyer et al., “Paligemma: A versatile 3b vlm for transfer,” arXiv preprint arXiv:2407.07726, 2024. 

   - [10] Y. Li, F. Wei, C. Zhang, and H. Zhang, “Eagle-2: Faster inference of language models with dynamic draft trees,” arXiv preprint arXiv:2406.16858, 2024. 

   - [11] M. J. Kim et al., “Openvla: An open-source vision-language-action model,” arXiv preprint arXiv:2406.09246, 2024. 

   - [12] K. Pertsch et al., “Fast: Efficient action tokenization for vision-languageaction models,” arXiv preprint arXiv:2501.09747, 2025. 

   - [13] S. Liu et al., “Rdt-1b: a diffusion foundation model for bimanual manipulation,” arXiv preprint arXiv:2410.07864, 2024. 

   - [14] K. Black et al., “pi0: A vision-language-action flow model for general robot control,” arXiv preprint arXiv:2410.24164, 2024. 

   - [15] Q. Li et al., “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” arXiv preprint arXiv:2411.19650, 2024. 

   - [16] J. Bjorck et al., “Gr00t n1: An open foundation model for generalist humanoid robots,” arXiv preprint arXiv:2503.14734, 2025. 

   - [17] K. Black et al., “pi0.5: a vision-language-action model with open-world generalization,” arXiv preprint arXiv:2504.16054, 2025,” 

   - [18] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” arXiv preprint arXiv:2407.08693, 2024. 

   - [19] Q. Sun et al., “Emma-X: An Embodied Multimodal Action Model with Grounded Chain of Thought and Look-ahead Spatial Reasoning,” arXiv preprint arXiv:2412.11974, 2024. 

   - [20] H. Zhen et al., “3d-vla: A 3d vision-language-action generative world model,” arXiv preprint arXiv:2403.09631, 2024. 

   - [21] J. Jones, O. Mees, C. Sferrazza, K. Stachowicz, P. Abbeel, and S. Levine, “Beyond sight: Finetuning generalist robot policies with heterogeneous sensors via language grounding,” arXiv preprint arXiv:2501.04693, 2025. 

   - [22] O. M. Team et al., “Octo: An open-source generalist robot policy,” arXiv preprint arXiv:2405.12213, 2024. 

   - [23] X. Li et al., “Towards generalist robot policies: What matters in building vision-language-action models,” arXiv preprint arXiv:2412.14058, 2024. 

   - [24] Z. Peng et al., “Kosmos-2: Grounding multimodal large language models to the world,” arXiv preprint arXiv:2306.14824, 2023. 

   - [25] P. Wang et al., “Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution,” arXiv preprint arXiv:2409.12191, 2024. 

   - [26] J. Wen et al., “Diffusion-VLA: Scaling Robot Foundation Models via Unified Diffusion and Autoregression,” arXiv preprint arXiv:2412.03293, 2024. 

   - [27] J. Liu et al., “Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model,” arXiv preprint arXiv:2503.10631, 2025. 

   - [28] I. Leal et al., “Sara-rt: Scaling up robotics transformers with selfadaptive robust attention,” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 6920–6927. 

   - [29] J. Wen et al., “Tinyvla: Towards fast, data-efficient vision-languageaction models for robotic manipulation,” IEEE Robotics and Automation Letters, 2025. 

   - [30] Y. Yue et al., “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” Advances in Neural Information Processing Systems, vol. 37, pp. 56619–56643, 2024. 

   - [31] M. Oquab et al., “Dinov2: Learning robust visual features without supervision,” arXiv preprint arXiv:2304.07193, 2023. 

   - [32] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in Proceedings of the IEEE/CVF international conference on computer vision, 2023, pp. 11975–11986. 

   - [33] P. Mazzaglia, N. Backshall, X. Ma, and S. James, “Redundancy-Aware Action Spaces for Robot Learning,” IEEE Robotics and Automation Letters, 2024. 

- [6] C. Schuhmann et al., “Laion-400m: Open dataset of clip-filtered 400 million image-text pairs,” arXiv preprint arXiv:2111.02114, 2021. 

