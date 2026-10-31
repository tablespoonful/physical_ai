---
title: "Humanoid-VLA: Towards Universal Humanoid Control with Visual Integration"
date: "2025-02-20"
authors: "Pengxiang Ding; Jianfei Ma; Xinyang Tong; Binghong Zou; Xinxin Luo; Yiguo Fan"
url: https://arxiv.org/abs/2502.14795
pdf: https://arxiv.org/pdf/2502.14795
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.14795)** / [論文ページ](https://arxiv.org/abs/2502.14795)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Humanoid-VLA: Towards Universal Humanoid Control with Visual Integration** 

**Pengxiang Ding**<sup>* 1 2</sup> **Jianfei Ma**<sup>* 3</sup> **Xinyang Tong**<sup>* 1</sup> **Binghong Zou**<sup>3</sup> **Xinxin Luo**<sup>3</sup> **Yiguo Fan**<sup>1</sup> **Ting Wang**<sup>1</sup> **Hongchao Lu**<sup>1</sup> **Panzhong Mo**<sup>3</sup> **Jinxin Liu**<sup>3</sup> **Yuefan Wang**<sup>1 2</sup> **Huaicheng Zhou**<sup>3</sup> **Wenshuo Feng**<sup>3</sup> **Jiacheng Liu**<sup>1 2</sup> **Siteng Huang**<sup>1</sup> **Donglin Wang**<sup>1 3</sup> 

## **Abstract** 

This paper addresses the limitations of current humanoid robot control frameworks, which primarily rely on reactive mechanisms and lack autonomous interaction capabilities due to data scarcity. We propose Humanoid-VLA, a novel framework that integrates language understanding, egocentric scene perception, and motion control, enabling universal humanoid control. Humanoid-VLA begins with language-motion pre-alignment using non-egocentric human motion datasets paired with textual descriptions, allowing the model to learn universal motion patterns and action semantics. We then incorporate egocentric visual context through a parameter efficient video-conditioned fine-tuning, enabling context-aware motion generation. Furthermore, we introduce a self-supervised data augmentation strategy that automatically generates pseudoannotations directly derived from motion data. This process converts raw motion sequences into informative question-answer pairs, facilitating the effective use of large-scale unlabeled video data. Built upon whole-body control architectures, extensive experiments show that Humanoid-VLA achieves object interaction and environment exploration tasks with enhanced contextual awareness, demonstrating a more human-like capacity for adaptive and intelligent engagement. 

## **1. Introduction** 

Humanoid robots are poised to transform diverse industries—from healthcare to manufacturing—by combining human-like dexterity with adaptability to execute complex tasks. Building on extensive human motion datasets from computer graphics research (Mahmood et al., 2019; Guo 

> *Equal contribution 1Milab, Westlake University 2Zhejiang University<sup>3</sup> Westlake Robotics. Correspondence to: Donglin Wang <wangdonglin@westlake.edu.cn>. 

_Preprint._ 


Figure 1: **Comparison between previous works and our approach.** With the capability of autonomous perception, Humanoid-VLA can perform tasks to interact with objects, significantly advancing beyond previous methods that rely on mimicking human demonstrations for motion execution. 

et al., 2020), recent advances have established data-driven frameworks for humanoid motion skill acquisition. 

Initial research (Cheng et al., 2024; Ji et al., 2024) developed whole-body controllers that translate basic human kinematic sequences into humanoid motion. The field has since progressed to integrate multimodal perception, enabling humanoids to perform real-time mimicry of human demonstrations (He et al., 2024b) and respond fluidly to natural language commands (Mao et al., 2024). While these approaches achieve high-fidelity motion control in humanoid robots, they operate primarily through reactive mechanisms, dynamically adjusting motions in response to external inputs. They cannot perceive autonomously and infer potential interaction targets within their immediate surroundings. This limitation substantially impedes their deployment in scenarios that demand object manipulation or adaptive exploration in complex environments. To this end, this paper aims to investigate universal humanoid control with egocentric visual integration. 

1 

However, developing such a system faces a significant bottleneck: **data scarcity** . Existing motion capture datasets lack synchronized first-person visual information, making direct transfer to egocentric tasks impossible. Moreover, while teleoperation offers a theoretical pathway for collecting visuomotor data, its prohibitive costs severely constrain large-scale acquisition. These constraints lead to inadequate training datasets in quantity and diversity, which hinders the development of a foundation model for humanoid control with egocentric visual integration. 

As to the challenge of data scarcity, we propose a feasible and cost-effective paradigm. Specifically, we begin by establishing a language-motion pre-alignment using nonegocentric human motion datasets paired with textual descriptions. This enables the model to learn universal motion patterns and action semantics from diverse third-person observations, yielding a robust, generalizable motion representation that does not rely on egocentric visual input. Next, we incorporate egocentric visual context through a parameter-efficient cross-attention module. This adaptive mechanism preserves the integrity of the pretrained model while allowing for the dynamic fusion of first-person visual features, thereby enabling context-aware motion generation. Our framework essentially reduces the dependence on egocentric datasets, making combining language understanding and egocentric scene perception with motion control feasible. 

Furthermore, the existing training paradigm alone is insufficient to ensure optimal model performance, primarily due to limitations in the alignment between motion and language. Drawing inspiration from the success of MLLMs (Liu et al., 2023; Zhang et al., 2023a)—where robust large language models (LLMs) serve as foundational components—we argue that the effectiveness of our framework hinges on the pre-alignment of motion and language representations. Achieving this alignment, however, heavily depends on the availability of large-scale and high-quality data. Unfortunately, current motion datasets are insufficient in scale to meet this need. While video sources offer a vast reservoir of human data, their utility for model training is constrained by the lack of motion description annotations. 

To address this limitation, we propose a self-supervised data augmentation framework that generates pseudo-annotations through automated motion analysis. Our solution features an automatic annotation pipeline that extracts semantic meaning directly from motion sequences via carefully designed self-supervised tasks. A representative implementation involves temporarily masking specific body joints within motion sequences and training the model to reconstruct the occluded movements. We automatically generate instructional prompts for such tasks as "missing left arm <Occlusion> motion data. Please complete the motion" paired with cor- 

responding ground truth motions as target outputs. This automated process systematically converts raw motion data into meaningful question-answer pairs. By integrating these self-supervised learning objectives, our approach circumvents the need for manually annotated textual descriptions while effectively utilizing large-scale and unlabeled motion data extracted from video repositories. 

Finally, integrating a whole-body controller following previous work (He et al., 2024b), our proposed **HumanoidVLA** seamlessly combines language understanding, scene perception, and motion control into a unified system. Extensive experiments show our approach significantly enhances humanoid robots’ autonomous interaction capabilities in real-world environments, paving the way for practical deployment across diverse applications. 

## **2. Related Works** 

### **2.1. Humanoid Control** 

Traditional humanoid control methods (Li et al., 2023; Kuindersma et al., 2016; Elobaid et al., 2023; Dantec et al., 2021; Dai et al., 2014) like MPC provide accuracy and stability but lack adaptability, while learning-based methods offer flexibility but rely on human motion data due to limited humanoid datasets. Works like Exbody (Cheng et al., 2024), Exbody2 (Ji et al., 2024), HARMON (Jiang et al., 2024), and mobile-television (Lu et al., 2024) perform upper-body motion retargeting for humanoid robots using the SMPL model (Loper et al., 2023) and root velocity tracking for lower-body locomotion. To achieve flexible and complex motions, methods such as PHC (Luo et al., 2023), H2O (He et al., 2024b), and OmniH2O (He et al., 2024a) use the SMPL model to extend motion retargeting to whole-body control. Additionally, approaches like OmniH2O (He et al., 2024a), HARMON (Jiang et al., 2024), and UH-1 (Mao et al., 2024) enable language-guided motion generation. However, these methods are reactivate, meaning that the models generate various motions passively based on text or key points. To perform more advanced tasks autonomously in dynamic and complex environments, **egocentric visual information** is indispensable. 

### **2.2. Humanoid Dataset** 

Apart from the first-person visual information, aligning motion with semantically relevant textual information is crucial for the construction of a foundational humanoid robot model. Previous human datasets, such as AMASS (Mahmood et al., 2019), HumanML3D (Guo et al., 2022a), Motion-X (Lin et al., 2023), and Human3.6M (Ionescu et al., 2014; Catalin Ionescu, 2011) provide large-scale human motion data. While some works use human motion retargeting to develop humanoid robot datasets (He et al., 2024a;b; 

2 

Cheng et al., 2024; Ji et al., 2024), these datasets often suffer from sparse text annotations and limited scale, restricting their use in training foundational models. Even though some methods can mitigate this issue, they generally suffer from high costs (Mao et al., 2024) and a lack of precision (Tevet et al., 2023). In contrast, we propose a self-suprvised data augmentation method that circumvents the need for manually annotated textual descriptions while effectively utilizing large-scale, unlabeled motion data extracted from video repositories for the training of robot foundation model. 

### **2.3. VLA for Robotics Learning** 

In recent years, VLA models have advanced robot learning, particularly for robotic arms and quadrupeds, by integrating vision, language, and action to enhance task and environment generalization. For robotic arms, models like RT-2 (Brohan et al., 2023), OpenVLA (Kim et al., 2024), GR-2 (Cheang et al., 2024), RoboMamba (Liu et al., 2024a), and RDT-1B (Liu et al., 2024b) leverage visual and language inputs for efficient task execution. In quadrupeds, models such as QUAR-VLA (Ding et al., 2025) and QUARTOnline (Tong et al., 2024) improve generalization and adaptability in dynamic environments, while _π_ 0 (Black et al., 2024) enables multi-embodied robots to perform diverse tasks. Despite these advances, due to the scarcity of datasets that combine first-person visual information, textual motion descriptions, and whole-body motion data for humanoid robots, VLA models have yet to be applied to humanoid robots. This paper takes the first step in building the Humanoid-VLA model to enable humanoid robots to autonomously perform loco-manipulation tasks. 

|Category|Text|Motion|Clips|Frames|Hours|
|---|---|---|---|---|---|
|Motion capture|✓|✓|29K|0.3M|4.1|
|Online Video|✗|✓|0.8M|541M|7515.7|
|Synthetic Data|✓|✓|100K|16M|227.7|
|To|tal||**0.929M**|**557.3M**|**7790.2**|


Table 1: **Datasets Statistics** 

methods, focusing mainly on human joint poses, lack integration with egocentric vision. Thus, they can only teach robots what actions are performed, not the underlying intent or context. Consequently, pose-level imitation is inherently limited in generalizability due to environmental discrepancies. 

**Our solution.** We present Humanoid-VLA, the first VLA model for humanoid robots, seamlessly integrating language understanding, scene perception, and motion control into a unified system to address previous limitations in humanoid control. Next, we demonstrate the framework from two main parts: **Language-Motion Pre-Alignment** and **Visionconditioned Fine-tuning** . 

### **3.2. Language-Motion Pre-Alignment** 

In this stage, we align non-egocentric human motion data with language descriptions. This alignment enables the model to learn motion patterns and action semantics from non-egocentric data sources, laying a robust foundation for motion generation without requiring egocentric visual input. 

### 3.2.1. DATA ACQUISITION 

## **3. Humanoid-VLA** 

### **3.1. Preliminary** 

**Definition of humanoid control.** With the growing availability of human data in the graphics community, recent humanoid control has increasingly adopted methods that learn from human data. Specifically, given a target body pose from physical teleoperation (e.g., a motion capture system) and the humanoid’s proprioception, the whole-body controller _P_ generates joint torques to control the humanoid robot. Formally, this can be expressed as 


where _st, pt, jt_ means target body pose, humanoid’s proprioception and joint torques at time _t ∈_ N<sup>+</sup> . 

### **Limitation of humanoid control.** 

However, developing a general-purpose robot requires purposive learning, which involves extracting meaningful intentions from human data and adapting prior experiences to novel tasks or environments. Current data acquisition 

**Limitations of data acquisition.** Previous studies have predominantly utilized well-curated datasets that pair motion trajectories with language descriptions to train textconditioned motion generation models. While these datasets facilitate effective training, they are limited in both quantity and diversity, which constrains their ability to achieve better alignment. In contrast, large-scale online video datasets (as shown in Table 1) offer abundant and diverse motion data. However, the absence of corresponding language annotations significantly limits their applicability for this task. 

Recent efforts to address this bottleneck have focused on annotating large-scale video datasets manually or using video large language models (VLLMs)(Zhang et al., 2023a). However, manual labeling is prohibitively expensive, and VLLMs often produce noisy, incomplete, or imprecise annotations due to their inability to capture fine-grained motion details or describe complex actions. These limitations undermine the effectiveness of the resulting datasets for aligning language and motion. 

**Self-supervised data augmentation.** Instead of relying on 

3 


Figure 2: **Overview of Humanoid-VLA** . Humanoid-VLA includes two main parts: language-Motion Pre-alignment and vision-conditioned fine-tuning. 

explicit motion descriptions, we propose a cost-effective annotation method by designing various self-supervised tasks directly derived from motion data. For instance, one representative approach involves temporarily masking specific body joints within motion sequences and training the model to reconstruct the occluded movements. Instructional prompts such as "missing left arm <Occlusion> motion data. Please complete the motion" can be generated for these tasks, paired with the corresponding ground truth motions as target outputs. This automatic approach eliminates the need for explicit annotations and is more accurate than adding extra annotation for motion data from video sources. 

Next, we explain how this is achieved through two key modules: **compositional motion quantitation** and **automatic data augmentation.** 

**Compositional motion quantitation.** As shown in Figure 2, we propose a decompositional compression method for body pose representation. Specifically, we decompose each body pose into five body-based tokens corresponding to five distinct parts: the left leg, right leg, torso, left arm, and right arm. We independently train each encoder _Eb_ and its corresponding codebook _Vb_ for each body part to compress the body part data at time _t_ , denoted as _ct_ , into a quantized representation _zt ∈_ R<sup>5</sup> . 

Formally, we define the motion encoder as _Em_ = _{Eb}_<sup>5</sup> _b_ =1<sup>,</sup> 

which compresses _ct_ into _zt_ . 


where _z_ ˆ _t_ = _{_ ˆ _zb}_<sup>5</sup> _b_ =1<sup>isthecollectivediscretevectorob-</sup> tained from _Em_ , which are the most similar elements to the quantization of _ct_ in vocabulary _Vm_ = _{Vb}_<sup>5</sup> _b_ =1<sup>.Similar</sup> to the encoder, we employ a motion decoder to project the latent variable back onto the action space: 


The optimize goal _Lhvq_ can be expressed as the combination of reconstruction loss _L_ rec, embedding loss _L_ emb and commitment loss _L_ com: 


This compositional encoding method is crucial, allowing for flexible editing of motion sequences. The advantage of decomposing a body pose into multiple parts and encoding them separately lies in that we can form flexible operations on the motion sequence at the token level. For instance, we can replace, perturb, or rearrange the tokens corresponding to specific body parts to generate new motion patterns. This flexibility significantly enhances control over motion data, laying the foundation for further task design. 

4 


Figure 3: **Data Acquisition Pipeline** . We propose a cost-effective, self-supervised data augmentation approach that converts abundant pure motion data from videos into annotated motion data with captions. The framework consists of two key modules: a compositional motion quantization method and an autonomous data augmentation approach, which together enable scalable expansion of the dataset. 

**Automatic data augmentation.** As illustrated in Figure 3, we introduce four types of augmentations—<Track>, <Time>, <Occlusion>, and <State>—to extract diverse features from raw motion data. For example, in the <Track> augmentation, we isolate the temporal trajectory of a specific joint (e.g., the root joint) and encode it as a corresponding motion token. To create meaningful questionanswer pairs, we pair this motion feature with an instructional prompt, such as “Please move your center position along the trajectory of <Track>,” while using the complete motion sequence as the answer. This approach effectively augments datasets that initially lacked linguistic annotations, enabling their use in tasks requiring text-motion alignment. 

**Discussion.** This method presents several key advantages. 1) It is highly flexible and extensible: augmentation types like <Track> can be combined with other conditions (e.g., <Time>) to create more complex tasks, while linguistic diversity can be further enriched by rephrasing the same instruction through tools like GPT-4(Achiam et al., 2023). 2) The framework leverages motion data’s inherent temporal and spatial dynamics, allowing models to learn richer and more robust motion-language relationships. 3) Lastly, the use of interleaved datasets enhances cross-modal alignment by incorporating both motion and text in inputs and outputs. As demonstrated by prior work such as VILA (Lin et al., 2024), such training paradigms enable models to better cap- 

ture the interplay between motion and language without compromising performance on their original tasks. 

Using this augmentation approach, we collect the largest motion-language interleaved dataset to date, with a scale that is 25 times larger than previous work (Mao et al., 2024). This effectively addresses the data scarcity issue for training foundational human motion models. 

### 3.2.2. TRAINING. 

When we acquire enough data with language annotations, we still need to consider the quality of raw motion data from video sources. Therefore, we divide our whole training process into two stages. First, we leverage low-quality data to establish initial alignment between motion and language. Even if they are not precise, the large-scale data could also lay a foundation. Later, we continue to train the model using a smaller but high-quality dataset from Mocap, ensuring that it conforms to proper human kinematics. 

**Details.** We utilize LLMs to map input conditions to generate motion sequences effectively. Our data augmentation approach and compositional motion encoding allow LLMs to seamlessly embed motion conditions into input descriptions. For instance, an instruction _lt_ for motion generation can be structured as: "Plan a sequence of actions ending with <State> over <Time> seconds." Here, <State> corre- 

5 

sponds to the discrete action representation token _zt_ , which is derived from the motion pose _ct_ at timestep _t_ in the motion sequence, while <Time> specifies the motion duration. By unifying the motion codebook _Vm_ and the language codebook _Vl_ into a shared vocabulary _V_ = _{Vl, Vm}_ , we can encode the instruction _lt_ alongside the motion representations _zt_ and temporal representations _dt_ as language tokens _Xd_ = _{x_<sup>_i_</sup> _d_<sup>_}_</sup> _i_<sup>_N_</sup> =1<sup>, where</sup><sup>_xd∈V_and</sup><sup>_N_represents the</sup> length of the input description. This transformation makes the combined motion and temporal data compatible with LLMs, enabling precise and flexible input encoding. 

**Loss function.** Motion generation can thus be framed as an autoregressive process that predicts the dictionary index of the next action token, ultimately producing the final motion output _Xo_ = _{x_<sup>_i_</sup> _o_<sup>_}L_</sup> _i_ =1<sup>,where</sup><sup>_xo∈V_and</sup><sup>_L_denotesthe</sup> output sequence length. The training objective is defined as maximizing the log-likelihood of the data distribution: 


Finally, the predicted discrete motion sequence _z_ ˆ _t_ can be derived from the LLM’s output sequence _Xo_ through vocabulary mapping. This sequence can then be used to reconstruct the final predicted motion _S_ = _{st}_<sup>_T_</sup> _t_ =1<sup>, where</sup><sup>_T_</sup> represents the length of the motion sequence. 

### **3.3. Vision-Conditioned Fine-Tuning** 

Visual information provides humanoids with detailed objectaware insights, helping them not only understand how to act but also decide what actions to take. While previous research has trained humanoids using large datasets of human motion, the lack of egocentric visual data limits their ability to react based on autonomous perception. To address this, we collect real-world motion capture data paired with egocentric visuals, enabling the transfer of learned motion knowledge to real-world, visually grounded scenarios. 

**Details.** We copy and freeze the transformer layers from the language-motion pre-alignment phase to integrate visual information with language descriptions. Additionally, we introduce a vision encoder and utilize cross-attention layers to fuse visual features _Xv_ with language features _Xd_ into a unified embedding _Xu_ . Specifically, the decoder comprises _L_ layers, with the _l_ -th layer consisting of a copied transformer decoder layer and a cross-attention layer. In the cross-attention layer, the tokenized language tokens _Xd_<sup>_l_are</sup> used as the query, while the encoded visual tokens _Xv_<sup>_l_serve</sup> as both the key and the value: 


where _D_ represents the hidden dimension size, _WQ_<sup>_l∈_</sup> R<sup>_Dd×D_</sup> represents the linear transformation matrix of language token, and _WK_<sup>_l, W_</sup> _V_<sup>_l∈_R</sup><sup>_Dv×D_represents the trans-</sup> formation of visual tokens. 

**Loss function.** Here, we optimize the model in the same way as the former language-action pre-alignment phase. 

### **3.4. Whole-Body Controller** 

**Details.** Once the two training phases are completed, the model can be integrated with a whole-body controller to enable control of a humanoid robot. The whole-body controller _P_ is essentially a goal-conditioned RL policy that maps human motion onto the joints of a humanoid robot _jt ∈_ R<sup>24</sup> . We define a reward strategy _R_ , which takes the observation _O_ and the given goal _G_ as input, and outputs the target positions for the proportional-derivative (PD) controller in the action space _A_ . We use the proximal policy optimization (PPO) (Schulman et al., 2017) to maximize the accumulated reward. 

## **4. Experiments** 

We evaluate the proposed **Humanoid-VLA** in terms of its ability to enable universal humanoid control. We structure the experiments to answer the following questions: **1) RQ1** : Does **Humanoid-VLA** generate kinematically accurate and physically plausible motions? **2) RQ2** : How effective is the humanoid control with vision integration? 

### **4.1. Evaluation on motion generation** 

In this section, we take a comprehensive evaluation of the quality of the pose trajectory generated by the model. To comprehensively demonstrate the effectiveness of our approach, we access motion quality from two perspectives: **1) Kinematic fidelity:** This metric evaluates the kinematic performance, measuring positional changes without considering physical dynamics. Following (Mao et al., 2024), we evaluate our model on the standard text-to-motion (T2M) task, which generates motion sequences based on textual action descriptions. It highlights the model’s core capability of translating natural language into human motion. 

**2) Physical plausibility:** Unlike the above metric, this evaluation assesses the physical feasibility of generated poses in real-world environments. Beyond standard T2M tasks, we evaluate our model on more challenging scenarios that exceed the capabilities of existing models, particularly tasks incorporating diverse input conditions such as joint trajectories. This comprehensive assessment demonstrates the robustness and versatility of the model across a broad spectrum of applications. 


6 

|Types|Input||Accu|racy||
|---|---|---|---|---|---|
|||_E_<sup>_g_</sup><br>mpjpe <sup>_↓_</sup>|_E_<sup>pa</sup><br>mpjpe <sup>_↓_</sup>|_E_accel _↓_|_E_vel _↓_|
||D|36.13|1.53|34.42|18.73|
||T|36.57|1.48|35.10|18.53|
|Easy|A|39.02|1.32|34.32|17.91|
||_Sn_|36.29|1.55|34.93|18.88|
||D + T|31.07|1.18|27.84|14.76|
|Medium|D + A|36.98|1.30|34.87|18.16|
||D +_Sn_|35.75|1.18|33.41|17.18|
|Hard|D +_S_1+_SN_|37.14|1.34|34.69|18.08|


Table 2: **Physical plausibility of generated motion under versatile conditions.** Humanoid-VLA provides four conditional input types: motion description ( **D** ), motion time duration ( **T** ), motion sequence with absent body parts ( **A** ), and motion state ( _Sn_ ) at time n within total N timesteps. Based on input combinations, we establish three tiers of motion generation tasks with increasing complexity. 

|Method|Human|ML3D|Huma|noid-S|
|---|---|---|---|---|
||FID_↓_|DIV_↑_|FID_↓_|DIV_↑_|
|MDM|0_._889<sup>_±._026</sup>|3_._855<sup>_±._053</sup>|2_._351<sup>_±._590</sup>|4_._111<sup>_±._261</sup>|
|T2M-GPT|0_._531<sup>_±._020</sup>|4_._555<sup>_±._058</sup>|1_._101<sup>_±._189</sup>|4_._199<sup>_±._218</sup>|
|Humanoid-VLA|**0****_._467**<sup>_±._018</sup>|**4****_._585**<sup>_±._086</sup>|**1****_._037**<sup>_±._147</sup>|**4****_._466**<sup>_±._213</sup>|


Table 3: **Kinematic fidelity of generated motion in HumanML3D and Humanoid-S.** We use FID score and Diversity to evaluate the quality of the motion generated by the model, where bold values indicate the best results. 

### 4.1.1. KINEMATIC FIDELITY 

**Setup.** We evaluate the motion quality using a widely used dataset HumanML3D (Guo et al., 2022c) and our collected dataset Humanoid-S, which contains manually annotated action descriptions for human pose extracted from 4646 video clips. While HumanML3D focuses on basic locomotion patterns such as running, swimming, and dancing, Humanoid-S encompasses more complex human actions. We choose the whole testing dataset and randomly select one textual description per clip to serve as the input for evaluation. For a fair comparison, we evaluate all models using 15 joints consistent with our model’s configuration, selected for their presence in both humans and humanoid robots to enhance generalizability. 

**Metrics.** We follow the evaluation framework from (Guo et al., 2022b), utilizing two established metrics to evaluate the quality of motion generation: **(1) FID** measuring distribution similarity between generated and real motions, and **(2) Diversity** quantifying action variation degree, and calculating the average Euclidean distance between 200 randomly generated motions. Lower FID indicates better distribution matching and higher DIV scores reflect superior diversity. 

**Baselines.** We consider two baselines commonly used in humanoid control: **(1) MDM** (Tevet et al., 2023): A diffusion-based generation model that utilizes a classifier- 

|Low-quality data|High-quality Data|FID_↓_|DIV_↑_|
|---|---|---|---|
|w aug|w aug|||
|✓||0_._698<sup>_±._037</sup>|4_._576<sup>_±._098</sup>|
||✓|0_._557<sup>_±._016</sup>|3_._867<sup>_±._062</sup>|
|✓|✓|**0****_._467**<sup>_±._018</sup>|**4****_._585**<sup>_±._086</sup>|


Table 4: **Ablation on data augmentation.** Here, lowquality data refers to motion data extracted through human motion recovery, which tends to lack precision. In contrast, high-quality data refers to motion data obtained directly from physical devices, ensuring greater accuracy. 

free paradigm to produce natural and diverse motions. **(2) T2M-GPT** (Zhang et al., 2023b): A transformer-based generation model that combines VQ-VAE(Van Den Oord et al., 2017) with an autoregressive approach to generate human motions from text. 

**Implementation details.** We utilize Llama3-70B (Dubey et al., 2024) as the foundation model. In the training phase, warm up ratio is set at 0.01, with learning rate configured at 2e-5, and the cosine learning scheduler. The batch size per device is set to 4. For the encoder of each body part, its codebook size is set to 1024. We conduct model training using 8 NVIDIA H100 GPUs through 216 hours. 

**Results.** The comparative evaluation results between Humanoid-VLA and the baseline models are presented in Table 3. On the HumanML3D dataset, Humanoid-VLA achieves a significant FID score of 0.467, representing substantial improvements of 47.5% and 12% over MDM and T2M-GPT respectively, which indicates its superior capability in capturing real motion distributions. Furthermore, Humanoid-VLA demonstrates remarkable performance in motion diversity, attaining a diversity score of 4.466 on the Humanoid-S dataset, outperforming MDM by 6%. This achievement is particularly noteworthy as it reflects the model’s ability to generate diverse motions under challenging linguistic constraints. The comprehensive experimental results demonstrate that Humanoid-VLA excels in highquality action generation, establishing its effectiveness in text-to-motion synthesis tasks. 

### 4.1.2. PHYSICAL PLAUSIBILITY 

**Setup.** We evaluate this metric in the IsaacGym physics simulator (Makoviychuk et al., 2021). Following (He et al., 2024a; Ji et al., 2024), we assess the humanoid’s tracking accuracy in executing the model-generated kinematic trajectories to quantify physical plausibility. 

**Metrics.** Our metrics are designed across two dimensions: (1) **_State-related._** The global Mean Per-Joint Position Error (MPJPE) _E_ mpjpe<sup>_g_(mm) quantifies the average positional</sup> error of individual joints. The Procrustes-aligned MPJPE (PA-MPJPE) _E_ mpjpe<sup>pa(mm) eliminates global scale and rota-</sup> tional discrepancies to assess shape accuracy specifically. 

7 


Figure 4: **Robot experiments in real world** . Humanoid-VLA demonstrates its ability to interact with objects, showcasing robust performance in real-world environments. The humanoid model successfully executes precise object-kicking tasks and avoids obstacle task in real-world scenarios. 

(2) **_Transition-related._** We evaluate acceleration error _E_ accel (mm/s²) and velocity error _E_ vel (mm/s) metrics to assess physical plausibility by computing the average joint-level distances in acceleration and velocity respectively. For all metrics, lower values correspond to better performance. 

**Baselines.** As these conditional motion tasks are uniquely solvable by our model, conventional baselines are not applicable. Therefore, we focus on evaluating our approach independently, adopting the tracking error widely accepted in (Ji et al., 2024) to evaluate the effectiveness of our method. 

**Results.** As shown in Table 2, our RL policy achieves robust motion imitation joint control with mean position errors _E_ mpjpe<sup>_g_consistentlybelow40mm,andminimum</sup> score 31.07mm under medium difficulty with caption and time conditions. The policy achieves remarkably low errors in pose accuracy _E_ mpjpe<sup>paat 1.18mm, acceleration</sup><sup>_E_accel</sup> at 27.84mm, and velocity _E_ vel at 14.76mm, demonstrating smooth and physically consistent motion generation. This experiment validates our method’s ability to generate high-quality motions across diverse control conditions while preserving physical plausibility and control fidelity. 

### **Ablation on data augmentation.** 

As shown in Table 4, incorporating extensive video motion data reduces the FID from 0.557 to 0.467, representing a 16% improvement. This significant enhancement demonstrates that large-scale motion data extracted from videos strengthens the alignment between motion and language. We can still achieve comparable results Even with low-quality mocap data for fine-tuning. These two points strongly validate the significance of incorporating video data to expand the training process. These findings underscore the effectiveness of our self-supervised data augmentation strategy. 

### **4.2. Evaluation on vision integration** 

### **Experimental setup.** 

We evaluate the performance of our Humanoid-VLA model in real-world environments utilizing visual information. An 

RGB camera is employed to capture first-person view images, and experiments are conducted using the Unitree G1 robot across four task categories: upper-body motion, lower-body motion, full-body motion, and object interaction. These tasks, such as approaching targets, kicking a ball, and obstacle navigation, require visual guidance for accurate positioning, aiming to validate the effectiveness of our VLA approach. 

**Results.** For each task category, we carefully select 4 representative tasks and evaluate 10 tests on each task, using success rate as the evaluation metric. Our humanoid-VLA model shows great performance in various object interaction tasks shown in Table 5. Selected tasks are shown in Figure 4. In the "kick ball" task, our humanoid model enables the robot to effectively utilize visual information to accurately approach the object and execute a kicking motion. In the "avoid obstacles" task, our robot successfully navigates around obstacles to reach the desired target position. These results demonstrate that our VLA model effectively leverages visual information to generate appropriate motions. 

|**Task**|**SR**|
|---|---|
|Turn to an object|10/10|
|Hold an object|9/10|
|Wave to people|10/10|
|Avoid an obstacle|9/10|
|Jump over an object|9/10|
|Dance with a partner|8/10|
|Punch an obstacle|10/10|
|Kick a ball|9/10|


Table 5: **Evaluation on Vision Integration.** 

## **5. Conclusion** 

This paper introduces Humanoid-VLA, a novel framework designed to address the challenges of humanoid robot control with egocentric visual integration. The framework aligns language and motion using human motion datasets, enables context-aware motion generation through crossattention mechanisms, and tackles data scarcity using selfsupervised pseudo-annotations. Built on whole-body con- 

8 

trol architectures, Humanoid-VLA facilitates adaptive object interaction and exploration with enhanced contextual understanding. The effectiveness of Humanoid-VLA has been validated through evaluations of motion generation quality and execution success rates on real humanoid robots, demonstrating high executability. In the future, we aim to enhance the success rate of humanoid robots in performing more complex loco-manipulation tasks. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning in Robotics. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **References** 

- Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _pi_ _0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Catalin Ionescu, Fuxin Li, C. S. Latent structured models for human pose estimation. In _International Conference on Computer Vision_ , 2011. 

- Cheang, C.-L., Chen, G., Jing, Y., Kong, T., Li, H., Li, Y., Liu, Y., Wu, H., Xu, J., Yang, Y., et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 

- Cheng, X., Ji, Y., Chen, J., Yang, R., Yang, G., and Wang, X. Expressive whole-body control for humanoid robots. _arXiv preprint arXiv:2402.16796_ , 2024. 

- Dai, H., Valenzuela, A., and Tedrake, R. Whole-body motion planning with centroidal dynamics and full kinematics. In _2014 IEEE-RAS International Conference on Humanoid Robots_ , pp. 295–302. IEEE, 2014. 

- Dantec, E., Budhiraja, R., Roig, A., Lembono, T., Saurel, G., Stasse, O., Fernbach, P., Tonneau, S., Vijayakumar, 

S., Calinon, S., et al. Whole body model predictive control with a memory of motion: Experiments on a torquecontrolled talos. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 8202–8208. IEEE, 2021. 

- Ding, P., Zhao, H., Zhang, W., Song, W., Zhang, M., Huang, S., Yang, N., and Wang, D. Quar-vla: Vision-languageaction model for quadruped robots. In _European Conference on Computer Vision_ , pp. 352–367. Springer, 2025. 

- Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan, A., et al. The llama 3 herd of models. _arXiv preprint arXiv:2407.21783_ , 2024. 

- Elobaid, M., Romualdi, G., Nava, G., Rapetti, L., Mohamed, H. A. O., and Pucci, D. Online non-linear centroidal mpc for humanoid robots payload carrying with contact-stable force parametrization. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 12233– 12239. IEEE, 2023. 

- Guo, C., Zuo, X., Wang, S., Zou, S., Sun, Q., Deng, A., Gong, M., and Cheng, L. Action2motion: Conditioned generation of 3d human motions. In _Proceedings of the 28th ACM International Conference on Multimedia_ , pp. 2021–2029, 2020. 

- Guo, C., Zou, S., Zuo, X., Wang, S., Ji, W., Li, X., and Cheng, L. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 5152–5161, June 2022a. 

- Guo, C., Zou, S., Zuo, X., Wang, S., Ji, W., Li, X., and Cheng, L. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 5152–5161, 2022b. 

- Guo, C., Zou, S., Zuo, X., Wang, S., Ji, W., Li, X., and Cheng, L. Generating diverse and natural 3d human motions from text. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 5152–5161, June 2022c. 

- He, T., Luo, Z., He, X., Xiao, W., Zhang, C., Zhang, W., Kitani, K., Liu, C., and Shi, G. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. _arXiv preprint arXiv:2406.08858_ , 2024a. 

- He, T., Luo, Z., Xiao, W., Zhang, C., Kitani, K., Liu, C., and Shi, G. Learning human-to-humanoid real-time wholebody teleoperation. _arXiv preprint arXiv:2403.04436_ , 2024b. 

9 

- Ionescu, C., Papava, D., Olaru, V., and Sminchisescu, C. Human3.6m: Large scale datasets and predictive methods for 3d human sensing in natural environments. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 36(7):1325–1339, jul 2014. 

- Ji, M., Peng, X., Liu, F., Li, J., Yang, G., Cheng, X., and Wang, X. Exbody2: Advanced expressive humanoid whole-body control. _arXiv preprint arXiv:2412.13196_ , 2024. 

- Jiang, Z., Xie, Y., Li, J., Yuan, Y., Zhu, Y., and Zhu, Y. Harmon: Whole-body motion generation of humanoid robots from language descriptions. In _CoRL 2024 Workshop CoRoboLearn: Advancing Learning for Human-Centered Collaborative Robots_ , 2024. 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Kuindersma, S., Deits, R., Fallon, M., Valenzuela, A., Dai, H., Permenter, F., Koolen, T., Marion, P., and Tedrake, R. Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot. _Autonomous robots_ , 40:429–455, 2016. 

- Li, J., Ma, J., Kolt, O., Shah, M., and Nguyen, Q. Dynamic loco-manipulation on hector: Humanoid for enhanced control and open-source research. _arXiv preprint arXiv:2312.11868_ , 2023. 

- Lin, J., Zeng, A., Lu, S., Cai, Y., Zhang, R., Wang, H., and Zhang, L. Motion-x: A large-scale 3d expressive whole-body human motion dataset. _Advances in Neural Information Processing Systems_ , 36:25268–25280, 2023. 

- Lin, J., Yin, H., Ping, W., Molchanov, P., Shoeybi, M., and Han, S. Vila: On pre-training for visual language models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 26689– 26699, 2024. 

- Liu, H., Li, C., Wu, Q., and Lee, Y. J. Visual instruction tuning, 2023. 

- Liu, J., Liu, M., Wang, Z., An, P., Li, X., Zhou, K., Yang, S., Zhang, R., Guo, Y., and Zhang, S. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024a. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024b. 

- Liu, Y., Yang, B., Zhong, L., Wang, H., and Yi, L. Mimicking-bench: A benchmark for generalizable humanoid-scene interaction learning via human mimicking. _arXiv preprint arXiv:2412.17730_ , 2024c. 

- Loper, M., Mahmood, N., Romero, J., Pons-Moll, G., and Black, M. J. Smpl: A skinned multi-person linear model. In _Seminal Graphics Papers: Pushing the Boundaries, Volume 2_ , pp. 851–866. 2023. 

- Lu, C., Cheng, X., Li, J., Yang, S., Ji, M., Yuan, C., Yang, G., Yi, S., and Wang, X. Mobile-television: Predictive motion priors for humanoid whole-body control. _arXiv preprint arXiv:2412.07773_ , 2024. 

- Luo, Z., Cao, J., Kitani, K., Xu, W., et al. Perpetual humanoid control for real-time simulated avatars. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 10895–10904, 2023. 

- Mahmood, N., Ghorbani, N., Troje, N. F., Pons-Moll, G., and Black, M. J. Amass: Archive of motion capture as surface shapes. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 5442–5451, 2019. 

- Makoviychuk, V., Wawrzyniak, L., Guo, Y., Lu, M., Storey, K., Macklin, M., Hoeller, D., Rudin, N., Allshire, A., Handa, A., et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- Mao, J., Zhao, S., Song, S., Shi, T., Ye, J., Zhang, M., Geng, H., Malik, J., Guizilini, V., and Wang, Y. Learning from massive human videos for universal humanoid pose control. _arXiv preprint arXiv:2412.14172_ , 2024. 

- Schulman, J., Wolski, F., Dhariwal, P., Radford, A., and Klimov, O. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- Tevet, G., Raab, S., Gordon, B., Shafir, Y., Cohen-or, D., and Bermano, A. H. Human motion diffusion model. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https://openreview. net/forum?id=SJ1kSyO2jwu. 

- Tong, X., Ding, P., Wang, D., Zhang, W., Cui, C., Sun, M., Fan, Y., Zhao, H., Zhang, H., Dang, Y., et al. Quart-online: Latency-free large multimodal language model for quadruped robot learning. _arXiv preprint arXiv:2412.15576_ , 2024. 

- Van Den Oord, A., Vinyals, O., et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

10 

- Wang, Y., Wang, Z., Liu, L., and Daniilidis, K. Tram: Global trajectory and motion of 3d humans from in-thewild videos. In _European Conference on Computer Vision_ , pp. 467–487. Springer, 2025. 

- Xu, X., Zhang, Y., Li, Y.-L., Han, L., and Lu, C. Humanvla: Towards vision-language directed object rearrangement by physical humanoid. _arXiv preprint arXiv:2406.19972_ , 2024. 

- Zhang, H., Li, X., and Bing, L. Video-llama: An instructiontuned audio-visual language model for video understanding. _arXiv preprint arXiv:2306.02858_ , 2023a. 

- Zhang, J., Zhang, Y., Cun, X., Zhang, Y., Zhao, H., Lu, H., Shen, X., and Shan, Y. Generating human motion from textual descriptions with discrete representations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 14730–14740, 2023b. 

11 

## **A. Data collection** 

Our motion dataset is derived from three primary sources: Motion Capture, Online Videos, and Synthetic Data. Specifically, the motion capture data is sourced from the open-source AMASS dataset, which includes textual annotations. Synthetic Data is generated by inputting random text into an open-source motion model to produce corresponding movements. Online Videos are collected from the web, with human motions extracted using the method described in (Wang et al., 2025). 

It is important to note that we select 15 universal humanoid joint points from the standard 22 SMPL joints in these open-source datasets. The framework enhances flexibility and extensibility by seamlessly integrating augmentation types with other conditions to create complex tasks, while advanced tools such as GPT-4 expand linguistic diversity through instruction rephrasing. By leveraging the inherent temporal and spatial dynamics of motion data, it enables models to learn more comprehensive and robust motion-language relationships. Additionally, improved cross-modal alignment is achieved through interleaved datasets that incorporate both motion and text, allowing models to better capture the interplay between motion and language. 

## **B. Data templates** 

|**Task**|**Template descriptions**|
|---|---|
|<Occlusion>_→_<Motion>|**Your help is crucial for us. Please complete the missing left leg data: <Occlusion>.**<br>1. <Occlusion>is part of the left leg motion. Please predict its complete data.<br>2. The left leg data: <Occlusion>is incomplete. Please help us fill in this part.<br>3. Please provide the complete left leg data: <Occlusion>.<br>...<br>N. To perfect the motion, we need the complete left leg data: <Occlusion>. Please assist us.<br>Your help is crucial for us. Please complete the missing right leg data: <Occlusion>. (×N)<br><Occlusion>is part of the left arm motion. Please predict its complete data. (×N)<br>The right arm data: <Occlusion>is missing. Could you help us fill in this part? (×N)|
|<Track>_→_<Motion>|Please ensure your root moves along<Track>for the next action. (×N)<br>Please move your left hand according to the trajectory of<Track>. (×N)<br>Please keep the movement of your right hand consistent with<Track>. (×N)|
|<Motion>_→_<Track>|I would like a detailed analysis of the trajectory of the central position in this action: <Motion>. (×N)<br>Tell me the path of the left hand: <Motion>. (×N)<br>I would like a detailed analysis of the trajectory of the right hand in this action: <Motion>. (×N)|
|<Time>_→_<Motion>|Can you make a motion that lasts for<Time>frames, with a certain percentage of variability? (×N)<br>Show me a motion that is longer than<Time>seconds in duration. (×N)|
|<Motion>_→_<Time>|Calculate the frame duration for<Motion>’s poses. (×N)<br>Compute the duration in seconds for<Motion>’s poses. (×N)|
|<State>_→_<Motion>|Randomly generate an entire action sequence from<State1>. (×N)<br>Create actions randomly using the last state<StateN>. (×N)<br>Move from the initial position<State1>to the final position<StateN>. (×N)|
|<Caption>+<Occlusion>_→_<Motion>|Explain the state before executing<Motion>actions. (×N)<br>Explain the final conditions following<Motion>actions. (×N)|
|<State>+<Time>_→_<Motion>|Design a full action sequence culminating in<StateN>across<Time>frames. (×N)<br>Plan a sequence of actions ending with<StateN>over<Time>seconds. (×N)|
|<Occlusion>+<Caption>_→_<Motion>|To complete the<Caption>action, we need the missing center motion data: <Occlusion>. Please assist us. (×N)<br>To complete the<Caption>action, we need the missing left leg motion data: <Occlusion>. Please assist us. (×N)<br>To finish the<Caption>action, we need to fill in the missing left arm motion data: <Occlusion>. Please assist us. (×N)<br>Your assistance is crucial. Please help us complete the missing right arm data: <Occlusion>for the<Caption>action. (×N)|
|<Track>+<Caption>_→_<Motion>|Please keep your root on the trajectory of<Track>while performing the actions described by<Caption>. (×N)<br>While your left hand is moving along<Track>, perform the action described by<Caption>. (×N)<br>Generate an action according to the description<Caption>while ensuring your right hand remains on the trajectory of<Track>. (×N)|
|<State>+<Track>+<Caption>_→_<Motion>|Starting from<State1>, follow the direction of your root guided by<Track>to perform the dynamic described by<Caption>. (×N)<br>Starting from<State1>, your right hand needs to follow the path of<Track>and complete the dynamic described in<Caption>. (×N)<br>Starting from<State1>, follow the direction of your root guided by<Track>to perform the dynamic described by<Caption>. (×N)|
|<Motion>+<Time>+<Caption>_→_<Motion>|Produce an action sequence for<Caption>incorporating a partial motion sequence described as<Motion>spanning<Time>frames. (×N)|


Table 6: **Examples of conditional language description.** All task descriptions could be expanded _N_ times similar to the first example. 

The input descriptions for our subtasks are presented in Table 6. Specifically, for each category of subtasks, such as "Complete left leg data," we have developed N variations of expressions. This allows our self-supervised augmentation approach to significantly expand the range of task descriptions, increasing the original 59 subtasks at N times. 

12 


Figure 5: **Simulation robot experiment** . 

## **C. Simulation Performance** 

To enhance humanoid robots’ environmental interaction capabilities, we selected 2 representative object interaction tasks from the HITR dataset referencing HumanVLA (Xu et al., 2024). For each task, we collected comprehensive data including egocentric visual frames, natural language instructions, and robot control signals. Our approach extends beyond real-world scenarios into simulation environments, where we followed HumanVLA’s setup to extract 15 key joints from stick figure trajectories for constructing our training dataset. This methodology leverages the abundance of existing stick figure/humanoid datasets, enabling efficient data acquisition through retargeting for both visual and motion aspects. Although joint retargeting to humanoid forms may not match the quality of motion capture data, it presents promising opportunities for continued research using large-scale simulation-based VLA data for downstream task training. 

A key strength of our universal framework lies in its demonstrated adaptability across different robot configurations. Unlike previous approaches that are often constrained to specific platforms, our framework successfully generalizes between distinct robot architectures in simulation and real-world implementations. This universal applicability represents a significant advancement over prior work such as HumanVLA, which, while providing excellent policy foundations, was limited in achieving universal humanoid control and real robot deployment. Our framework transcends these limitations by establishing a universal bridge between simulation and physical robot systems, paving the way for truly generalizable humanoid control strategies that can be deployed across diverse platforms and tasks. 

## **D. More Details** 

It is noteworthy that the joint points for motion generation in our model are not the conventional 22 joints, but rather a set of 15 joints that are common to both humanoid robots and humans. This approach ensures universality across different configurations. However, an additional optimization step is required to adapt the poses generated by the large model for downstream applications. Specifically, generating a motion sequence with 15 joints necessitates an optimization process to map it onto the target downstream configuration. 

To acquire training data, we extract 15 joint points from standard datasets for training purposes. This ensures that the model learns from a consistent and universally applicable set of joint points. 

To enable humanoid robots to execute corresponding motions through joint-point mapping, we employ the Adam optimizer similar to (Mao et al., 2024; Jiang et al., 2024), which map the positions of the 15 joints from keypoints to the 24 joints of the humanoid robot. By maintaining the end-effector positions as closely aligned as possible with the existing joint node positions, the overall motion pattern of the humanoid robot remains consistent with the keypoint representation. 

We define the problem as training a goal-conditioned RL policy _π_ that maps human motion onto the joints of a humanoid robot _jt ∈_ R<sup>24</sup> . We define a reward strategy _R_ , which takes the observation _O_ and the given goal _G_ as input, and outputs the target positions for the proportional-derivative (PD) controller in the action space _A_ . We use the proximal policy gradient (PPO) to maximize the accumulated reward. 

13 

## **E. Limitation** 

**Robustness of the RL Policy** . Although we have developed a general RL policy, its performance lacks sufficient robustness. We plan to further refine the policy to enhance task completion. 

**Limited Availability of High-Quality Data** . The availability of high-quality data is limited, including manually annotated data and execution data from real-world humanoid robots. While we considered leveraging datasets from works like Mimicking-Bench (Liu et al., 2024c), the restricted robot configurations render them unsuitable for general robotics tasks. Consequently, we will undertake the collection of data for general humanoid robot tasks and encourage the community to recognize and address this data scarcity. 

**Training Approach** . Our current training methodology is relatively simple, and not fully leveraging the available data. We have identified several strategies to enhance the training of motion generation models, we will incorporate these techniques into our future work. 

14 

