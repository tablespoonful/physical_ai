---
title: "AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models"
date: "2026-05-08"
authors: "Xiaoqi Li; Muhe Cai; Jiadong Xu; Juan Zhu; Hongwei Fan; Yan Shen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2605.07308
pdf: https://arxiv.org/pdf/2605.07308
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.07308)** / [論文ページ](https://arxiv.org/abs/2605.07308)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models** 

Xiaoqi Li<sup>1,2*</sup> , Muhe Cai<sup>1,2*</sup> , Jiadong Xu<sup>1</sup> , Juan Zhu<sup>2</sup> , Hongwei Fan<sup>1,2</sup> , Yan Shen<sup>1,2</sup> , Guangrui Ren<sup>3</sup> , Hao Dong<sup>1,2�</sup> 

1School of Computer Science, Peking University 2 PrimeBot 3 AGIBOT 


Figure 1. **AT-VLA** improves upon previous VLA approaches in contact-rich tasks by introducing Adaptive Tactile Injection, which balances pretrained knowledge with the learning of newly incorporated tactile representations. Furthermore, it enables rapid and accurate action adjustments based on tactile feedback through a Tactile Reaction Dual-Stream Strategy. 

## **Abstract** 

_Vision-Language-Action (VLA) models have significantly advanced the capabilities of robotic agents in executing diverse tasks; however, they still face challenges in contactrich manipulation scenarios that require precise physical interactions. To address this limitation, recent studies have attempted to incorporate tactile signals during downstream tasks, enabling pretrained VLAs to interpret tactile feedback. Nevertheless, introducing new modalities during finetuning, which are rarely present in the pretrain stage, may disrupt the pretrained capabilities of VLAs. In addition, the inherently slow inference speed of VLAs hampers real-time responsiveness and limits the effective utilization of tactile feedback for action adjustment. To overcome these challenges, we propose Adaptive Tactile Vision-Language-Action (AT-VLA), which introduces a novel Adaptive Tactile Injection mechanism. This mechanism dynamically determines_ 

*Equal contribution. 

_the appropriate timing and locations for tactile injection, incorporating only when it significantly contributes to action generation, thereby minimizing interference with pretrained representations. Furthermore, to enable rapid and accurate tactile responses, we propose a Tactile Reaction Dual-Stream mechanism, which decouples sensory processing into a slow visual-language stream for low-frequency perceptual reasoning and a fast tactile control stream for high-frequency physical interaction understanding, achieving real-time close-loop responses within 0.04 s. Real-world experiments thoroughly validate the effectiveness of AT-VLA in contact-rich manipulation tasks. Project page can be found at: https://sites.google.com/view/ at-vla_ 

## **1. Introduction** 

The development of Vision-Language-Action (VLA) models [6, 7, 9, 36, 39, 40, 45, 49] has greatly accelerated the progress toward generalist robotic agents. Empowered by 

28764 

large-scale manipulation datasets [10, 36, 41] and the emergence of foundation models [3, 38], VLAs demonstrate strong abilities that enable robots to ground language in perception and perform diverse tasks. However, when facing contact-rich manipulation scenarios that require precise understanding of physical interactions, these models remain limited, as they often overlook interaction feedback ( _e.g._ tactile signals) that are essential for achieving intricate control and safe interaction with the physical world. 

Since pretrained open-source manipulation datasets rarely include tactile information, researchers [4, 21, 43] often address this limitation by incorporating these modalities during downstream tasks finetuning. Their primary goal is to enable pretrained models to interpret these new types of sensory input. This is typically achieved by using multimodal alignment strategies through representation learning [14, 44, 46, 47], or leveraging chain-of-thought (CoT) [25] reasoning to understand these signals. However, tactile feedback provides fundamentally different types of information compared to the visual or linguistic data used in the pretrained models. While these approaches enhance the model’s ability to interpret tactile feedback, the direct introduction of these new modalities may disrupt the existing pretrained knowledge, such as visual perception or object grounding. Furthermore, the relatively slow inference speed of VLA models hampers their ability to react quickly to high-frequency tactile feedback. This slow response time reduces the effectiveness of tactile feedback in closed-loop manipulation, where swift adjustments are crucial. To this end, as illustrated in Fig. 1, we propose Adaptive Tactile Vision-Language-Action (AT-VLA), which, for the first time, achieves a balance between preserving pretrained capabilities and integrating tactile inputs, while ensuring rapid and effective tactile feedback reactions. 

Drawing inspiration from the complementary characteristics of visual and tactile modalities, where vision facilitates contextual localization and tactile provides precise contact feedback, we argue that the model should preserve its pretrained VLA structure in non-contact phases while introducing tactile feedback only upon contact to better utilize pretrained representations. To realize this, we introduce an **Adaptive Tactile Injection** mechanism that determines when and where to incorporate tactile signals. Specifically, a learnable _Tactile Gate_ is designed to automatically modulate the contribution of each modality across different manipulation phases, determining whether tactile features should be fed into the action expert for action generation. To accommodate different gate states, we further propose an _Adaptive Cross Attention_ mechanism within the action expert module, which dynamically adjusts its cross-attention behavior by conditionally switching the query source. This mechanism integrates tactile information when the gate is activated, without the need to modify the model structure or feature 

dimensionality compared to the inactive state. By doing so, we minimize the impact of tactile signals on the vanilla model, thus retaining its robust action generation capability, such as target object localization. 

Furthermore, since high-frequency tactile feedback requires rapid action adjustment, we design a **Tactile Reaction Dual-Stream** mechanism to ensure the model’s real-time responsiveness when tactile gate is activated. Specifically, we decouple sensory processing into two streams of different frequency: a _slow stream_ , where visual and language inputs are processed through a large Vision-Language Model (VLM) to leverage the pretrained visual perception and localization ability at a low frequency; and a _fast stream_ , where tactile feedback is continuously fed into the action expert at a high frequency. The action expert integrates heterogeneous modality features operating at different frequencies, conditioning each action prediction on both the latest tactile feedback and the most recent vision-language reasoning output that falls within the same action chunk horizon. This design enables a closed-loop control within 0.04 s inference speed, ensuring timely responses to tactile feedback. Moreover, to further enhance the model’s comprehension of tactile signals in the fast stream, we introduce a future _Tactile Generation_ objective that predicts subsequent tactile states, thereby improving the model’s understanding of underlying physical dynamics. 

Our main contributions are as follows: 1) We propose Adaptive Tactile Injection, making the first attempt to balance pretrained knowledge with the learning of newly introduced tactile representations. 2) Leveraging the highfrequency nature of tactile feedback that demands rapid response, we design a Tactile Reaction Dual-Stream mechanism to ensure accurate and timely action adjustments during contact. 3) AT-VLA achieves superior manipulation performance on real-world contact-rich tasks compared with other SOTA VLA or tactile-based policies. 4) Unlike prior tactilebased policies that heavily rely on tactile inputs, AT-VLA, although trained with tactile feedback, maintains strong performance even in the absence of tactile signals during inference. Benefiting from the adaptive training strategy, AT-VLA generalizes effectively across diverse sensory conditions while maintaining performance comparable to the vanilla VLA model, demonstrating strong modality-agnostic robustness in real-world circumstances where tactile signals may be unstable or unavailable. 

## **2. Related Work** 

### **2.1. Vision Language Action Model** 

Rapid progress in Vision Language Models (VLMs) [1, 2, 32] has laid the foundation for the emergence of Vision Language Action (VLA) Models. By integrating environment perception, semantic reasoning, and action generation within 

28765 


Figure 2. **Framework of AT-VLA.** The tactile gate adaptively determines whether tactile tokens should be used as conditional inputs for action generation within the Action Expert module. When the tactile gate is inactive, all input modalities of the Action Expert operate at the same frequency. When activated, the tactile signal is processed at a higher frequency to enable rapid and precise action adjustments. 

a unified framework, VLAs [26, 28] demonstrate strong potential for task generalization and reliable manipulation. One common approach for action generation is to adopt diffusion-based models to formulate a conditional denoising process. For example, _π_ 0 [7] leverages flow matching (a specific instantiation of diffusion) to enhance temporal resolution and highlights the importance of effective training strategies by introducing a componentized architecture, where outputs from a visual-language model serve as preconditions for the diffusion-based action transformer. In this paper, following the vanilla VLA GO-1 [10], we adopt this manner to formulate the action modeling. Moreover, to enhance inference speed, several VLA [11, 11, 12, 16, 29– 31, 33 **?** , 34] approaches adopt a dual-system strategy for action generation, where the slow system targets on highlevel Vision-Language Model reasoning and the fast system acts as low-level policy. For instance, Groot-N1 [5] employs a fast visual stream alongside a slower semantic reasoning stream to preserve high-level planning ability and accelerate low-level action prediction. Different from these approaches, which use visual or point cloud data as the fast stream, we adopt high-frequency tactile feedback as the fast stream, enabling rapid reaction to contact events and safer physical interactions. 

### **2.2. Interaction Feedback Policies** 

Vision is fundamental to environmental perception, while other interactive modalities [8, 18, 19, 24, 35, 48], such as joint torque, force, and end-effector tactile signals, are equally crucial for precise, closed-loop manipulation. Specifically, RDP [42] utilizes PCA-reduced marker offset as tactile input for latent space decoder, achieving high-frequency feedback adjustment. TLA [21] relies on tactile and language input and works well in insertion tasks trained on simulation data. TA-VLA [47] identifies that incorporating a tactile adapter within the decoder yields better performance 

than placing it in the encoder. In contrast to those that focus on enabling the model to interpret the semantic meaning of tactile feedback but may compromise the model’s original visual perception ability, we carefully manage the balance between pretrained knowledge and newly introduced tactile feedback, ensuring reliable manipulation in both non-contact and contact-rich stages. Moreover, compared to current tactile gate works [20, 22, 27], our method is designed to accommodate the characteristics of pretrained VLAs. When tactile gate is activated, these works typically incorporate tactile features by augmenting token sequence. In contrast, we observe that naively appending previously unseen modality may disrupt VLA’s pretrained token sequence modeling. In addition, these works typically process all modalities at the same operation frequency. However, due to the inference latency of VLAs, we decouple different modality processing frequencies. 

## **3. Method** 

### **3.1. Framework of AT-VLA** 

**Problem Formulation.** As shown in Fig. 2, the policy _πθ_ takes as input the image observations _I_ = _{Ih, Ir, Il}_ from the head camera, right wrist camera, and left wrist camera, respectively; the language instruction _L_ ; the tactile feedback _T_ ; and the robot’s proprioceptive state _S_ . For the tactile feedback, we extract the resultant force from the tactile sensors, which contains both the 3D normal and 3D tangential components of contact forces. The policy then generates an action chunk _A_ , representing the 14-DoF endeffector pose for both arms: 


**Model Instantiation.** AT-VLA is designed to be general and modular, allowing most VLAs to be integrated with minimal modification. For a specific instantiation, we employ the 

28766 


Figure 3. **Intuition.** We visualize the attention maps in the Action Expert module to examine how the model’s attention distribution and action reasoning vary across downstream finetuning strategies, contrasting settings with and without tactile feedback. 

pretrained GO-1 [10] as the vanilla VLA, since it is trained on the same robot hardware (Genie 1 from AgiBot) as ours and demonstrates strong performance across diverse tasks. GO-1 is pretrained in the AgiBot world dataset [10] and adopts Intern-VL-2B [13] as its base vision-language model (VLM). It utilizes a DiT [37] module as the action expert. We inherit both its model architecture and its action generation pipeline, where the actions are supervised by the action loss _La_ . To enable the model to handle contact-rich tasks, we introduce an additional tactile encoder. The tactile encoder is a lightweight module composed of several MLP layers, designed to ensure fast inference while efficiently processing tactile signals. 

### **3.2. Adaptive Tactile Injection** 

**Intuition.** We conduct a simple experiment that compares two training strategies for learning downstream manipulation tasks: (1) a typical fine-tuning strategy, which fine-tunes only the action expert of the vanilla VLA model without tactile input; and (2) a direct way to incorporate tactile feedback, which introduces tactile signals processed by the tactile encoder and fine-tunes only the action expert to condition on both the tactile tokens and the vision-language tokens. Surprisingly, the latter not only fails to improve performance but even causes noticeable inaccuracies in grasp localization. A detailed analysis of the attention maps within the action expert (Fig. 3) reveals that the additional tactile input shifts the model’s attention distribution away from the target object towards surrounding regions. We hypothesize that the addition of token sequences from newly introduced modalities can interfere with the pretrained model’s perceptual focus. Further quantitative results supporting this observation are provided in Tab. 3. This observation motivates us to consider that balancing pretrained knowledge with the learning of newly introduced tactile feedback must be carefully managed. 

Therefore, to address these issues, we propose the _Adaptive Tactile Injection_ module, which dynamically controls when and where tactile feedback is injected and enables the action expert to flexibly handle different gate states through adaptive cross-attention. Given the complementary nature of vision and tactile sensing, where vision provides contextual information for localization and tactile sensing offers 

detailed feedback on physical contact, the key insight is to enable the model to retain the behavior of the vanilla VLA in non-contact phases while leveraging tactile information only during contact. 

**Tactile Gating.** To realize it, we first design a learnable Tactile Gate mechanism that automatically determines when tactile feedback should be incorporated, which is when the robot is in contact with an object. Specifically, after extracting the tactile token **z** _T_ using the tactile encoder, we introduce a lightweight Tactile Gating Network composed of MLP layers to classify whether the current tactile signal indicates contact or non-contact. The network takes the tactile token as input and outputs a score representing the contact state. For supervision, we manually annotate the training episodes by assigning a label of 0 to non-contact frames and 1 to contact frames, and adopt binary cross-entropy gating loss _Lg_ to supervise. When the score exceeds the threshold (e.g., 0.5), the tactile gate is activated. 

**Adaptive Cross Attention.** With the tactile gate to determine when to incorporate tactile feedback, the action expert’s architecture must be able to handle inputs under both states of the tactile gate, whether or not tactile features are present. To realize this, we propose _Adaptive Attention_ in cross-attention module, which dynamically processes different input modalities of the action expert as conditions for action generation. Specifically, in the cross attention module of the action expert in the vanilla VLA, the image token **z** _I_ and text token **z** _L_ serve as the key and value, while the state token **z** _S_ is used as the query. To maintain consistency with the vanilla VLA and preserve its pretrained representations, the state token is used as the query when the tactile gate is inactive, and is replaced by the tactile token **z** _F_ when the gate is active. In this way, when there is no contact, the model’s input and architecture remain identical to those of the vanilla VLA. Once contact occurs, however, the model starts interpreting the tactile feedback as action generation conditioning. The model thus preserves pretrained representations to the greatest extent, maintaining action behaviors derived from strong visual perception and localization capabilities, such as approaching target objects. 

### **3.3. Effective Tactile Reaction Dual-Stream** 

In Sec. 3.2, our model adaptively determines _when_ and _where_ to inject tactile feedback, balancing the preservation of pretrained knowledge and learning of newly introduced modality. In this section, motivated by the high-frequency nature of tactile inputs requiring rapid action adaptation, we explore _how_ to enable the model to respond effectively when the tactile gate is activated. We decompose the reaction capability into two aspects: (1) rapid reaction. The model should quickly adjust its predicted actions based on incoming tactile feedback to ensure safety and precision, and (2) tactile understanding. The model should learn to interpret the meaning 

28767 

of tactile signals and modify its actions accordingly. 

**For a rapid reaction** , we define the input modalities process into two streams: a slow stream operates at a lower inference speed to interpret visual and language input via large vision language model; a fast stream operates at a high inference speed to interpret tactile feedback. Slow stream is responsible for task understanding and visual perception, producing a comprehensive output in the form of latent features serving as the key and value in the cross attention of action expert module, whereas fast stream processes tactile feedback that requires closed-loop real-time response serving as the cross attention query conditions. Therefore, the input of action expert module is at asynchronous frequency and with heterogeneous modality. 

Building on previous action chunking strategies, the visual and language observation at time step _tn_ can provide guidance for a future horizon of action steps ( _tn_ : _tn_ + _H_ ). Consequently, slow stream’s output serves as a latent condition that temporally guides action generation across the following _H_ time steps. In contrast, fast stream focuses on generating executable actions in real time. At each time step, action expert leverages the most recent tactile feedback _tn_ + _k,_ 0 _<k<H_ to generate actions, while conditioning on the periodically updated output from the slow stream, i.e., the slow stream’s output at time _tn_ . During training, the frequency ratio between the fast and slow streams is randomly set to _h_ :1 _,_ where 1 _< h < H_ , meaning that the fast stream’s input can be ahead of the slow stream by at most the action chunk horizon. Note that, when the tactile gate is inactive, the input of the action expert module is at synchronous frequency. In this way, the fast stream leverages the pretrained representations from the slow stream to ensure reliable visual perception, while simultaneously reacting to tactile dynamics within a 0.04s inference speed. 

Furthermore, to advance the fast stream with an accurate reaction to tactile input, we aim to enhance the model towards **a deeper understanding of tactile feedback** along with robotic physical interactions. Concretely, we propose a Tactile Generation strategy, which enables the model to forecast both the 3D normal and tangential forces for the next time step. We extract the tactile token after the Action Expert module and employ a lightweight decoder network to generate the next-step tactile signal, supervised by an MSE generation loss _Lr_ against the ground-truth tactile measurement. These designs encourage the model to develop a more comprehensive representation of physical dynamics and tactile semantics, bridging instantaneous contact perception and predictive interaction reasoning. 

### **3.4. Training Objectives and Inference Pipeline** 

All objectives are trained simultaneously, under the overall supervision _L_ = _La_ + _λ_ 1 _∗Lg_ + _λ_ 2 _∗Lr_ , _λ_ 1 and _λ_ 2 are all both to 0.01 to balance different losses’ scale. By doing 

so, AT-VLA is able to preserve pretrained knowledge and response to tactile feedback promptly and accurately. 

During inference, when the tactile gate is inactive, the model is identical to the original VLA, the input of fast and slow stream is at the same frequency, the attention query in the action expert module is same as the vanilla VLA. When the tactile gate is active, asynchronous frequency of slow and fast starts. Inspired by previous work [5, 11], we set the frequency ratio between fast stream and slow stream to 3:1 to ensure a balance of efficiency and performance, which means that the fast stream infers three times consecutively after a single inference of the slow stream. At the same time, the attention queries in the action expert module are switched to tactile tokens, which serve as the conditioning for action generation. 

## **4. Experiment** 

### **4.1. Setup** 

**Hardware.** We use the hardware, AgiBot Genie1, featuring dual 7-DoF arms, equipped with a front-view camera and two cameras mounted on the wrist. For tactile feedback, a gripper equipped with tactile sensors from Xense Robotics is utilized. We use the VR headset control for teleoperation. **Task Definition.** We evaluate our model on four contactrich tasks and two non contact-rich tasks. For each task, we collect 30-50 demonstrations and test in 15 trials. **Contactrich tasks** : a). _Unzip Bag_ . The robot is required to open a bag by unzipping its zipper. During this process, it must continuously adjust its trajectory to follow the curved path of the zipper. Failure to do so may cause the zipper to get stuck or jammed. b). _Stamp_ . The robot is required to stamp within a designated region. It must recognize when the stamping action is complete; otherwise, excessive downward actions could cause the end effector to collide with the desk surface. c). _Wipe Vase_ . The robot needs to wipe the surface of a vase, adapting its motion to the vase’s curved geometry. Insufficient compliance could result in collisions with the neck of the vase. d). _Uncrew Lid_ . The robot is required to rotate a lid to open a container. This task demands precise force and motion coordination to ensure smooth rotation without slipping. **Non contact-rich tasks** : a). _Pick and Place_ . The robot needs to pick a carrot and place it in the plate. b). _Open Drawer_ . The robot needs to grasp the handle of a drawer and open it. 

### **4.2. Contact-rich Task Evaluation** 

**Baselines.** We compare with four SOTA baselines: 

1. **GO-1** [10] serves as the vanilla model of our approach and is pretrained on the same dataset as ours. It can reflect how much improvement our method achieves. 

2. _π_ **0** _._ **5** [6] is a state-of-the-art VLA model consisting of both pretraining and post-training stages. 

28768 

Table 1. **Evaluation in contact-rich tasks.** We report the success rate of each subtask, reflecting the progress. 

|||**U**|**nzip Bag**||||**Stamp**|||
|---|---|---|---|---|---|---|---|---|---|
|Method|Left Grasp_→_|Right Grasp_→_|Unzip Half_→_|Unzip Full|**Overall**|Right Grasp_→_|Stamp_→_|Place|**Overall**|
|GO-1|**1.0**|**0.87**|**0.87**|0.20|0.20|**1.0**|0.80|0.33|0.33|
|_π_0_._5|**1.0**|0.67|0.67|0.0|0.0|**1.0**|0.53|0.20|0.20|
|**AT-VLA (Ours)**|**1.0**|0.80|0.80|**0.33**|**0.33**|0.90|0.87|**0.46**|**0.46**|
|VTLA|-|-|0.20|0.00|-|-|**0.93**|0.13|-|
|RDP|-|-|0.87|0.06|-|-|0.40|0.40|-|
|Method|Left Grasp_→_|Right Grasp_→_|Wipe Half_→_|Wipe Full|**Overall**|Left Grasp_→_|Right Grasp_→_|<br>Rotate|**Overall**|
|GO-1|**1.0**|**0.93**|0.30|0.07|0.07|**1.0**|**0.87**|0.27|0.27|
|_π_0_._5|**1.0**|0.73|0.40|0.33|0.33|0.93|0.80|0.47|0.47|
|**AT-VLA (Ours)**|**1.0**|0.80|0.80|**0.33**|**0.33**|0.90|0.87|**0.46**|**0.46**|
|VTLA|-|-|0.93|**0.60**|-|-|-|0.80|-|
|RDP|-|-|0.80|0.33|-|-|-|**0.87**|-|


3. **VTLA** [46] is a vision-language-action (VLA) model that incorporates tactile input. It employs Qwen2-VL [38] as the VLM backbone and adds an additional ViT [17] to extract tactile features, where tactile information is represented as visual-tactile images. Since the official implementation is not publicly available, we replicate it based on the DexVLA [39] codebase, which also builds upon Qwen2-VL. 

4. **RDP** [42] is built upon Diffusion Policy [15] and takes 2D tactile marker inputs. It applies PCA for dimensionality reduction before extracting tactile features. 

Note that, 1) GO-1 and _π_ 0 _._ 5, which have pretrained weights, are trained on the same downstream dataset as ours but without tactile input. 2) In contrast, VTLA and RDP, which do not have pretrained models on large-scale datasets, are trained only on the subset of our downstream tasks corresponding to the contact-rich manipulation phases. We found that training them on the full sequence often leads to failures during the grasping stage, which makes it difficult to reveal their core capability—namely, reacting to tactile feedback. Therefore, we remove the perception and grounding requirements for these two models to better isolate their ability to respond to tactile feedback. In practice, during testing, we manually place the robot in an ideal initial configuration ( _e.g.,_ already grasping the stamp) to evaluate these two models’ capability in completing the contact-rich portion of the task ( _e.g.,_ stamping). 

**Result Analysis.** As shown in Table 1, our model outperforms all baseline methods. The execution progress is shown in Fig. 4. Compared with state-of-the-art VLA models GO-1 and _π_ 0 _._ 5, which are trained without tactile feedback, our model demonstrates comparable performance during the pre-contact manipulation phase, indicating that it effectively preserves the pretrained knowledge in aspects such as visual grounding and semantic reasoning required for reliable 

object grasping. During the contact-rich stage, AT-VLA achieves an improvement over them, clearly demonstrating the necessity of tactile signals for complex manipulation tasks. In contrast, these models usually get stuck in stages, such as getting stuck by the zipper, or stamping on the desk too much, or getting stuck by the protuding surface. 

Furthermore, when compared with policies that incorporate tactile feedback like VTLA and RDP, our model still achieves superior performance in contact-rich phase manipulation, validating the effectiveness of our model to promptly and accurately adjust actions based on tactile feedback. The only exception is Unscrew Lid task, where our model performs slightly worse than them. This is mainly because, for baseline policies, we manually set the robot in an ideal grasping pose before rotating the lid, ensuring a stable grasp during the process. In contrast, our model, although capable of grasping the lid, does not always guarantee a sufficiently firm grip, occasionally leading to failure cases where the gripper slips during unscrewing. 

### **4.3. Modality-agnostic Evaluation** 

Table 2. **Modality-agnostic evaluation.** The AT-VLA variants with (w/.) and without (w/o.) tactile input share identical model weights, differing only in whether tactile information is provided during inference. The former serves as upper bound. 

|Method|**Pick Place**|**Open Drawer**|**Stamp**|AVG.|
|---|---|---|---|---|
|GO-1|**1.0**|**0.93**|0.13|0.68|
|_π_0_._5|**1.0**|**0.93**|**0.20**|**0.70**|
|**AT-VLA w/o.**|**1.0**|**0.93**|**0.20**|**0.70**|
|AT-VLA w/.|1.0|0.93|0.46|0.79|


In this section, we aim to evaluate the modality-agnostic robustness of our model. That is, how well it performs when trained on downstream tasks with tactile feedback but deployed without tactile signals during inference, which 

28769 


Figure 4. **Visualization.** We visualize the execution progress of four typical contact-rich tasks. 

is crucial for real-world robotic applications where sensor failures or missing modalities are common. 

As shown in Table 2, we compare our method with two VLA baselines, GO-1 and _π_ 0 _._ 5, which are also without tactile feedback input. Our two model alternatives, AT-VLA w/. and AT-VLA w/o., share the same model weights trained with tactile input; however, the former performs inference with tactile feedback which serves as an upper bound, while the latter infers without it. When compared with the VLA baselines, AT-VLA (w/o tactile) achieves comparable performance on two non contact-rich tasks, Pick-and-Place and Open Drawer. Thanks to the Adaptive Tactile Injection mechanism, our model can still generate reliable actions even when tactile feedback is absent at inference, demonstrating strong modality-agnostic and robustness to missing sensory modalities. 

For contact-rich manipulation, we select Stamp task as a representative example, since it involves intensive physical interaction while remaining executable by base VLA baselines with relatively high safety. Interestingly, AT-VLA (w/o tactile) even shows a slight performance improvement over its vanilla model GO-1. This can be attributed to the fact that, although tactile feedback is absent during inference, the model is trained with tactile input. Consequently, it has implicitly learned richer contact dynamics and cross-modal correlations during training, allowing it to infer approximate tactile cues from visual features at test time. 

### **4.4. Ablation Study** 

#### **4.4.1. Contribution of Each Component** 

From Rows Ex0–Ex4 in Tab. 3, we verify the contribution of each proposed component across four contact-rich tasks: **Ex0: Vanilla VLA.** This setting corresponds to the vanilla VLA model ( _i.e.,_ GO-1 [10]), which achieves an average success rate of 0.22. 

**Ex1: With Adaptive Cross Attention.** Compared to Ex0, we introduce tactile input but in a direct manner, consistent with the experiments discussed in the intuition analysis in Sec. 3.2. Specifically, since there is no gating mechanism, the queries in the Adaptive Cross Attention module are conditioned on the tactile features extracted from the tactile encoder throughout the entire manipulation process. However, this configuration even results in a lower success rate than the vanilla VLA, with a decrease of 9%. Most failures occur during object grasping, indicating degraded visual grounding and perception ability. This phenomenon is consistent with our intuition analysis in Sec. 3.2. **Ex2: With Tactile Gate.** Compared to Ex1, we further incorporate a Tactile Gate. Together with Adaptive Cross Attention, it enables the attention query to switch to tactile tokens only when the gate is activated; otherwise, the attention query remains identical to that of the vanilla VLA. Note that, in this setting, the visual and tactile inputs are processed at the same frequency. This configuration achieves a significant 17% improvement over the vanilla VLA, demonstrating the 

28770 

Table 3. **Ablation study.** Each variant selectively removes or changes components to assess their contributions. 

|||**Com**|**ponents**||**Tact**|**ile For**|**mat**||**T**|**asks**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Tactile<br>Gate|Adaptive<br>Cross Attention|Tactile<br>Generation|Reaction<br>Dual-Stream|V-T<br>Image|Marker<br>2D|Force<br>6D|Unzip<br>Bag|Stamp|<sup>Wipe</sup><br>Vase|Unscrew<br>Lid|AVG.|
|Ex0|-|-|-|-|-|-|-|0.20|0.33|0.07|0.27|0.22|
|Ex1|-|✓|-|-|-|-|✓|0.07|0.13|0.07|0.20|0.13|
|Ex2|✓|✓|-|-|-|-|✓|0.27|0.40|0.53|0.33|0.39|
|Ex3|✓|✓|✓||-|-|✓|0.27|**0.46**|0.60|0.40|0.43|
|Ex4 (Ours)|✓|✓|✓|✓|-|-|✓|**0.33**|**0.46**|**0.67**|**0.53**|**0.50**|
|Ex5|-|✓|-|-|-|✓|-|0.00|0.13|0.07|0.00|0.05|
|Ex6|✓|✓|✓|✓|-|✓|-|0.27|0.33|0.27|0.40|0.32|
|Ex7|-|✓|-|-|✓|-|-|0.00|0.00|0.07|0.00|0.02|
|Ex8|✓|✓|✓|✓|✓|-|-|0.27|**0.46**|0.47|0.40|0.40|


effectiveness of the tactile gate in preserving the pretrained knowledge of the model. **Ex3: With Tactile Generation.** Building upon Ex2, we add the tactile generation objective that supervises the prediction of future tactile states, encouraging the model to better understand underlying physical dynamics. This leads to a further improvement of 4% over Ex2. 

**Ex4: With Reaction Dual-Stream.** Compared to Ex3, we adopt the Tactile Reaction Dual-stream, setting different input frequencies for visual and tactile modalities. This setting yields an improvement of 7%, highlighting the necessity of rapid tactile feedback responses. In _Unzip_ task, for instance, where delayed reactions may cause the zipper to jam and hinder successful completion. 

#### **4.4.2. Different Tactile Format** 

We compare the effectiveness of incorporating tactile information in different formats, including visual-tactile images (V-T image in Tab. 3), marker 2D, and force 6D. Specifically, the _visual-tactile image_ contains contact geometry by mapping tactile deformation into an RGB image of size _H ×W ×_ 3, _H_ and _W_ are the size of tactile sensor. We adopt a pretrained tactile encoder Sparsh [23] to extract its feature, serving as tactile token in Fig. 2; the _marker 2D_ format represents the displacement of surface markers as a _N ×_ 2 array, where _N_ denotes the number of tracked markers. We initialize a lightweight encoder consisting of several MLP and non-linear activation layers to extract its feature; and the _force 6D_ format represents the resultant contact force, composed of a 3D tangential force vector and a 3D normal force vector, jointly capturing the surface’s shear and normal interactions during contact. 

Comparing Ex1, Ex5, and Ex7 with the vanilla VLA (Ex0), these variants all introduce tactile modalities—namely, 6D force, 2D marker, or visual-tactile images. The extracted tactile tokens are fed into the crossattention queries of the action expert module throughout 

all manipulation stages, which leads to a significant performance degradation. This observation further confirms that directly incorporating newly added modality tokens can disrupt the pretrained knowledge, resulting in failures even in basic manipulation skills such as object grasping. 

In contrast, adopting our proposed method to incorporate tactile input leads to substantial performance improvements—Ex6 outperforms Ex5 by 27%, and Ex8 surpasses Ex7 by 38%—demonstrating the robustness of our framework across different tactile formats. Moreover, we observe that the _force 6D_ modality achieves the best performance, followed by _marker 2D_ , and then the _visual-tactile image_ . We hypothesize that higher-dimensional tactile inputs may excessively perturb the pretrained representation space, as they introduce a larger number of tactile tokens. This highlights the importance of maintaining an appropriate balance between the influence of the newly added tactile modality and that of the pretrained vanilla models. 

## **5. Conclusion** 

In summary, AT-VLA introduces an adaptive framework that seamlessly integrates tactile sensing into vision-languageaction models. Through the Adaptive Tactile Injection mechanism, AT-VLA dynamically balances pretrained visuallanguage knowledge with newly learned tactile representations, preserving model integrity while enhancing action precision. The Tactile Reaction Dual-Stream mechanism further enables rapid, high-frequency tactile responses by decoupling slow perceptual reasoning from fast physical control, achieving closed-loop reaction within 0.04 s. Extensive real-world experiments demonstrate that AT-VLA significantly outperforms state-of-the-art VLA and tactilebased policies in contact-rich manipulation tasks. Future work may explore scaling this framework to more complex tasks and diverse real-world environments, further advancing general-purpose embodied intelligence. 

28771 

## **Acknowledge** 

This project was supported by National Youth Talent Support Program (8200800081) and National Natural Science Foundation of China (62376006). 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [2] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. _Advances in neural information processing systems_ , 35:23716–23736, 2022. 

- [3] Lucas Beyer, Andreas Steiner, Andre Susano Pinto, Alexan-´ der Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [4] Jianxin Bi, Kevin Yuchen Ma, Ce Hao, Mike Zheng Shou, and Harold Soh. Vla-touch: Enhancing vision-languageaction models with dual-level tactile feedback. _arXiv preprint arXiv:2507.17294_ , 2025. 

- [5] Johan Bjorck, Fernando Castaneda,˜ Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [6] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. pi0.5: a vision-language-action model with open-world generalization, 2025. _URL https://arxiv. org/abs/2504.16054_ , 1(2):3. 

- [7] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. pi0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [8] Alina Bohm,¨ Tim Schneider, Boris Belousov, Alap Kshirsagar, Lisa Lin, Katja Doerschner, Knut Drewing, Constantin A Rothkopf, and Jan Peters. What matters for active texture recognition with vision-based tactile sensors. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15099–15105. IEEE, 2024. 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [10] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [11] Hao Chen, Jiaming Liu, Chenyang Gu, Zhuoyang Liu, Renrui Zhang, Xiaoqi Li, Xiao He, Yandong Guo, Chi-Wing Fu, Shanghang Zhang, et al. Fast-in-slow: A dual-system foundation model unifying fast manipulation within slow reasoning. _arXiv preprint arXiv:2506.01953_ , 2025. 

- [12] Sixiang Chen, Jiaming Liu, Siyuan Qian, Han Jiang, Lily Li, Renrui Zhang, Zhuoyang Liu, Chenyang Gu, Chengkai Hou, Pengwei Wang, et al. Ac-dit: Adaptive coordination diffusion transformer for mobile manipulation. _arXiv preprint arXiv:2507.01961_ , 2025. 

- [13] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 24185–24198, 2024. 

- [14] Zhengxue Cheng, Yiqian Zhang, Wenkang Zhang, Haoyu Li, Keyu Wang, Li Song, and Hengdi Zhang. Omnivtla: Visiontactile-language-action model with semantic-aligned tactile sensing. _arXiv preprint arXiv:2508.08706_ , 2025. 

- [15] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44 (10-11):1684–1704, 2025. 

- [16] Can Cui, Pengxiang Ding, Wenxuan Song, Shuanghao Bai, Xinyang Tong, Zirui Ge, Runze Suo, Wanqi Zhou, Yang Liu, Bofang Jia, et al. Openhelix: A short survey, empirical analysis, and open-source dual-system vla model for robotic manipulation. _arXiv preprint arXiv:2505.03912_ , 2025. 

- [17] Alexey Dosovitskiy. An image is worth 16x16 words: Transformers for image recognition at scale. _arXiv preprint arXiv:2010.11929_ , 2020. 

- [18] Niklas Funk, Erik Helmut, Georgia Chalvatzaki, Roberto Calandra, and Jan Peters. Evetac: An event-based optical tactile sensor for robotic manipulation. _IEEE Transactions on Robotics_ , 2024. 

- [19] Niklas Funk, Changqi Chen, Tim Schneider, Georgia Chalvatzaki, Roberto Calandra, and Jan Peters. On the importance of tactile sensing for imitation learning: A case study on robotic match lighting. _arXiv preprint arXiv:2504.13618_ , 2025. 

- [20] Johanna Hansen, Francois Hogan, Dmitriy Rivkin, David Meger, Michael Jenkin, and Gregory Dudek. Visuotactilerl: Learning multimodal manipulation policies with deep reinforcement learning. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 8298–8304. IEEE, 2022. 

- [21] Peng Hao, Chaofan Zhang, Dingzhe Li, Xiaoge Cao, Xiaoshuai Hao, Shaowei Cui, and Shuo Wang. Tla: Tactilelanguage-action model for contact-rich manipulation. _arXiv preprint arXiv:2503.08548_ , 2025. 

- [22] Zihao He, Hongjie Fang, Jingjing Chen, Hao-Shu Fang, and Cewu Lu. Foar: Force-aware reactive policy for contact-rich robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [23] Carolina Higuera, Akash Sharma, Chaithanya Krishna Bodduluri, Taosha Fan, Patrick Lancaster, Mrinal Kalakrishnan, 

28772 

   - Michael Kaess, Byron Boots, Mike Lambeta, Tingfan Wu, et al. Sparsh: Self-supervised touch representations for visionbased tactile sensing. _arXiv preprint arXiv:2410.24090_ , 2024. 

- [24] Binghao Huang, Jie Xu, Iretiayo Akinola, Wei Yang, Balakumar Sundaralingam, Rowland O’Flaherty, Dieter Fox, Xiaolong Wang, Arsalan Mousavian, Yu-Wei Chao, et al. Vt-refine: Learning bimanual assembly with visuo-tactile feedback via simulation fine-tunin. _arXiv preprint arXiv:2510.14930_ , 2025. 

- [25] Jialei Huang, Shuo Wang, Fanqi Lin, Yihang Hu, Chuan Wen, and Yang Gao. Tactile-vla: Unlocking vision-language-action model’s physical knowledge for tactile generalization. _arXiv preprint arXiv:2507.09160_ , 2025. 

- [26] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [27] Jinzhou Li, Tianhao Wu, Jiyao Zhang, Zeyuan Chen, Haotian Jin, Mingdong Wu, Yujun Shen, Yaodong Yang, and Hao Dong. Adaptive visuo-tactile fusion with predictive force attention for dexterous manipulation. In _2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 3232–3239. IEEE, 2025. 

- [28] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 

- [29] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18061–18070, 2024. 

- [30] Xiaoqi Li, Jingyun Xu, Mingxu Zhang, Jiaming Liu, Yan Shen, Iaroslav Ponomarenko, Jiahui Xu, Liang Heng, Siyuan Huang, Shanghang Zhang, et al. Object-centric prompt-driven vision-language-action model for robotic manipulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 27638–27648, 2025. 

- [31] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified visionlanguage-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 

- [32] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 

- [33] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv preprint arXiv:2406.04339_ , 1(3):5, 2024. 

- [34] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 

- [35] Zhuoyang Liu, Jiaming Liu, Jiadong Xu, Nuowei Han, Chenyang Gu, Hao Chen, Kaichen Zhou, Renrui Zhang, Kai Chin Hsieh, Kun Wu, et al. Mla: A multisensory language-action model for multimodal understanding and forecasting in robotic manipulation. _arXiv preprint arXiv:2509.26642_ , 2025. 

- [36] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 

- [37] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 

- [38] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

- [39] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 

- [40] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient vision-languageaction models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- [41] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. _arXiv preprint arXiv:2412.13877_ , 2024. 

- [42] Han Xue, Jieji Ren, Wendi Chen, Gu Zhang, Yuan Fang, Guoying Gu, Huazhe Xu, and Cewu Lu. Reactive diffusion policy: Slow-fast visual-tactile policy learning for contactrich manipulation. _arXiv preprint arXiv:2503.02881_ , 2025. 

- [43] Shaobo Yang, Hongtong Li, Jiangyu Hu, Shixin Zhang, Guocai Yao, Ziqiang Ni, and Bin Fang. Bitla: A bimanual tactilelanguage-action model for contact-rich robotic manipulation. In _Proceedings of the 1st International Workshop on MultiSensorial Media and Applications_ , pages 12–17, 2025. 

- [44] Jiawen Yu, Hairuo Liu, Qiaojun Yu, Jieji Ren, Ce Hao, Haitong Ding, Guangyu Huang, Guofan Huang, Yan Song, Panpan Cai, et al. Forcevla: Enhancing vla models with a force-aware moe for contact-rich manipulation. _arXiv preprint arXiv:2505.22159_ , 2025. 

- [45] Yang Yue, Yulin Wang, Bingyi Kang, Yizeng Han, Shenzhi Wang, Shiji Song, Jiashi Feng, and Gao Huang. Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution. _Advances in Neural Information Processing Systems_ , 37:56619–56643, 2024. 

- [46] Chaofan Zhang, Peng Hao, Xiaoge Cao, Xiaoshuai Hao, Shaowei Cui, and Shuo Wang. Vtla: Vision-tactile-language- 

28773 

action model with preference learning for insertion manipulation. _arXiv preprint arXiv:2505.09577_ , 2025. 

- [47] Zongzheng Zhang, Haobo Xu, Zhuo Yang, Chenghao Yue, Zehao Lin, Huan-ang Gao, Ziwei Wang, and Hao Zhao. Tavla: Elucidating the design space of torque-aware visionlanguage-action models. _arXiv preprint arXiv:2509.07962_ , 2025. 

- [48] Xinyue Zhu, Binghao Huang, and Yunzhu Li. Touch in the wild: Learning fine-grained manipulation with a portable visuo-tactile gripper. _arXiv preprint arXiv:2507.15062_ , 2025. 

- [49] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

28774 

