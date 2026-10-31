---
title: "Mantis: A Versatile Vision-Language-Action Model with Disentangled Visual Foresight"
date: "2025-11-20"
authors: "Yi Yang; Xueqi Li; Yiyang Chen; Jin Song; Yihan Wang; Zipeng Xiao"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2511.16175
pdf: https://arxiv.org/pdf/2511.16175
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.16175)** / [論文ページ](https://arxiv.org/abs/2511.16175)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Mantis: A Versatile Vision-Language-Action Model with Disentangled Visual Foresight** 

Yi Yang<sup>1,2</sup> Xueqi Li<sup>2,3</sup> Yiyang Chen<sup>1</sup> Jin Song<sup>4</sup> Yihan Wang<sup>5</sup> Zipeng Xiao<sup>1</sup> Jiadi Su<sup>5</sup> You Qiaoben<sup>6</sup> Pengfei Liu<sup>1,2</sup> Zhijie Deng<sup>1,*</sup> 1SJTU 2SII 3SUSTech 4NJUPT 5Fudan University 6BOSCH 


## **Abstract** 

_Recent advances in Vision-Language-Action (VLA) models demonstrate that visual signals can effectively complement sparse action supervisions. However, letting VLA directly predict high-dimensional visual states can distribute model capacity and incur prohibitive training cost, while compressing visual states into more compact supervisory signals inevitably incurs information bottlenecks. Moreover, existing methods often suffer from poor comprehension and reasoning capabilities due to the neglect of language supervision. This paper introduces Mantis, a novel framework featuring a Disentangled Visual Foresight (DVF) to tackle these issues. Specifically, Mantis decouples visual foresight prediction from the backbone with the combination of meta queries and a diffusion Transformer (DiT) head. With the current visual state provided to the_ 

_DiT via a residual connection, a simple next-state prediction objective enables the meta queries to automatically capture the latent actions that delineate the visual trajectory, and hence boost the learning of explicit actions. The disentanglement reduces the burden of the VLA backbone, enabling it to maintain comprehension and reasoning capabilities through language supervision. Empirically, pretrained on human manipulation videos, robot demonstrations, and image-text pairs, Mantis achieves a 96.7% success rate on LIBERO benchmark after fine-tuning, surpassing powerful baselines while exhibiting high convergence speed. Real-world evaluations show that Mantis outperforms π_ 0 _._ 5 _, a leading open-source VLA model, particularly in instruction-following capability, generalization to unseen instructions, and reasoning ability. We also introduce the adaptive temporal ensemble (ATE) strategy to balance computational efficiency and motion stability during inference, yielding the Mantis-ATE variant, which re-_ 

*Corresponding author 

42505 

_duces inference counts by 50% while maintaining performance. We have released the code and model weights to the open-source community, which are available at https: //github.com/SJTU-DENG-Lab/Mantis._ 

## **1. Introduction** 

Robotic learning has witnessed remarkable progress, particularly in developing robust control strategies for diverse tasks across heterogeneous environments. Among the most promising approaches are Vision-Language-Action (VLA) models [7, 10, 25, 33, 40, 53, 58], which leverage pretrained Vision-Language Models (VLMs) [2, 3] to translate linguistic instructions and visual observations into executable robotic actions. Despite these advancements, existing VLA approaches face a fundamental challenge: the low-dimensional action signals can be too sparse to adequately supervise the large VLA model that processes highdimensional sensory inputs [27]. This mismatch leaves much of the model’s representational capacity underutilized, thereby constraining overall performance. 

A remedy is to integrate the visual foresight prediction problem into VLA training, with the model asked to predict dense future visual states in addition to forecasting actions [43, 55]. However, high-dimensional visual states usually contain redundancies that distract the model from action prediction, resulting in high training costs and slow convergence during downstream fine-tuning [17]. Alternative approaches compress visual states into more compact supervisory signals [44, 51]. Yet, compression inevitably diminishes subtle variations among visual states that convey fine-grained motions, thereby creating an information bottleneck. Furthermore, existing methods often overlook language supervision, rendering the context understanding and reasoning capabilities of the model unguarded [57]. 

We propose Mantis, a novel VLA model featuring a Disentangled Visual Foresight (DVF) to address these issues. As illustrated in Figure 2, Mantis combines meta queries [34] with a Diffusion Transformer (DiT) [35] head to predict future visual states. Despite its simplicity, this design can effectively disentangle the tight coupling of action learning and foresight prediction, considering its efficacy in text-to-image generation tasks [12, 34]. Furthermore, we advocate feeding the current visual state also to the DiT through a residual connection [19], which enables the meta queries to automatically capture the inter-frame dynamics that delineate the visual trajectory. Intuitively, these queries extract latent actions which can facilitate more effective explicit action generation; we therefore term them _latent-action queries_ . Then, we use learnable _action queries_ to extract information from both the input and latent-action queries via causal attention. We apply an action head to map the extraction outcomes to explicit actions as in [54]. 

The disentangled design of Mantis reduces the representation burden on the VLA backbone, thereby freeing up more capacity for language supervision, which helps preserve the model’s semantic understanding and reasoning capabilities after action learning. To minimize the competition between learning signals from various modalities, we develop a progressive training recipe that incrementally incorporates additional modalities for smooth fusion. For inference, Mantis leverages the Temporal Ensemble [56] method for motion stability. Considering its inefficiency issues, we also propose Adaptive Temporal Ensemble (ATE), which dynamically adjusts the ensemble strength according to the motion stability demand of the current timestep. _E.g_ ., finegrained object manipulation can require much higher motion stability than unladen movements. We term the corresponding model variant as Mantis-ATE. 

We pretrain Mantis based on three data sources: the SSV2 dataset [18] containing 220K human manipulation videos, the DROID dataset [24] with 76K robot demonstrations (covering video and action), and image–text pairs drawn from 38 multimodal datasets. We then evaluate Mantis on the LIBERO simulation benchmark [28] and in real-world settings. Extensive experiments validate our approach from multiple perspectives: (1) Mantis surpasses several strong baselines [8, 9, 32, 43, 44, 55], achieving 96.7% success on the LIBERO benchmark and showing faster convergence than previous visual foresight approaches [43]. (2) Experiments on the Agilex platform confirm Mantis’s robust instruction-following and generalization capabilities. Across three test scenarios, it accurately executes in-domain commands and effectively generalizes to out-of-domain instructions, outperforming the leading open-source VLA model _π_ 0 _._ 5 [21]. (3) The Mantis-ATE variant reduces inference calls by up to 50% while maintaining comparable task success rates. 

In summary, our main contributions are three-folds: 

- We propose Disentangled Visual Foresight (DVF) that provides concise and instructive look-ahead cues for action prediction and construct a new VLA model Mantis. 

- We design a progressive training recipe for modality fusion, enabling Mantis to effectively integrate action prediction with language understanding. 

- Mantis achieves 96.7% success on the LIBERO benchmark and demonstrates superior instruction-following capabilities in real-world robot experiments. 

## **2. Related Work** 

### **2.1. Vision-Language-Action Models** 

The rapid evolution of vision-language models (VLMs) [2, 3, 29, 39, 47] has catalyzed the emergence of VisionLanguage-Action (VLA) models [7, 10, 25, 26, 33, 40– 42, 45, 53, 58]. These systems integrate a vision-language 

42506 

backbone with an action prediction component, <mark>exte</mark> nding their functional capabilities beyond pure perception. By leveraging the rich perceptual and linguistic re <mark>presen</mark> tations of pretrained VLMs, VLA models enable robots to interpret and execute human commands with improved adaptability, transcending the limitations of purely reactive control policies. Despite this potential, existing VLA models suffer from limited understanding capabilities. Robot-specific training often overwrites the critical vision-text alignments acquired during pretraining [57], degradi <mark>ng ins</mark> tructionfollowing performance and undermining fundamental reasoning abilities. While some approaches employ explicit language assistance to mitigate this issue [38, 53], they are prone to error accumulation [17]. Other methods introduce implicit language supervision through auxilia <mark>ry los</mark> ses on language representations [13, 22, 57], but lack the visual foresight capabilities necessary for frame-level planning. In contrast, we propose a framework that incorporates visual foresight while simultaneously preserving semantic understanding and reasoning capabilities. 

### **2.2. Vision-Augmented Action Learning** 

Vision-augmented action learning effectively complements sparse action signals and better exploits the representational capacity of VLA models. We categorize vision-augmented action learning approaches as follows: 

**1) Visual Foresight.** This approach enhances action prediction by forecasting future frames, using either explicit or implicit methods. Explicit methods generate future frames through autoregressive discrete image tokens [32, 55] or learnable query tokens with a vision decoder [46, 54], which then inform action prediction. Implicit methods jointly train the VLA model on video generation and action prediction tasks, establishing an implicit connection between visual forecasting and action prediction [9, 23, 43]. However, pixel-level forecasting can introduce unnecessary information, distracting the model from action prediction and resulting in high training costs. Moreover, this approach may lead the model to mistakenly associate physical motion with visual appearances, such as texture or lighting changes, potentially resulting in hallucinations [16]. 

**2) Track Guidance.** To mitigate these limitations, several studies compress visual states into compact, controloriented representations such as keypoint tracks [4, 5, 44]. These tracks capture essential physical dynamics and facilitate action prediction. Nonetheless, this compression can cause information bottlenecks, and the precision of pointtracking extracted from videos is often limited, leading to higher action prediction errors. 

**3) Latent Action Supervision.** Other approaches employ latent actions to supervise action prediction [8, 14, 51]. Typically, an action quantization model is first trained to learn discrete latent actions from inter-frame differences. 


Figure 1. **Vision-augmented action learning paradigms.** (a) Visual Foresight enhances action prediction by forecasting future frames. (b) Track Guidance employs compressed visual state representations to guide action prediction. (c) Latent Action Supervision improves action learning through auxiliary latent actions. 

The VLA model is then trained to predict these latent actions before being fine-tuned on robot manipulation data. This strategy leverages the insight that inter-frame dynamics can be represented as action primitives that aid prediction. However, training an additional quantization model increases computational complexity. An overview of these vision-augmentation paradigms is provided in Fig. 1. In contrast to prior work, Mantis decouples visual foresight prediction from the backbone, yielding more compact and accurate auxiliary information for action prediction. 

## **3. Methodology** 

This section provides an overview of Mantis, beginning with its model architecture and specifications, followed by detailed descriptions of the progressive training recipe and the adaptive temporal ensemble mechanism. 

### **3.1. Model Overview** 

As illustrated in Fig. 2, Mantis comprises the following components: a backbone model _P_ , a connector _C_ , a DVF head _D_ , an action head _π_ , a set of trainable latent-action queries [LAT], and action queries [ACT]. The task is specified by a language instruction _l_ . At each time step _t_ , the backbone _P_ receives _l_ and a visual state ( _e.g_ ., a raw 

42507 


Figure 2. _Left:_ **Progressive training recipe.** Mantis progressively integrates multiple modalities to achieve stable and well-balanced optimization. _Center:_ **Overview of Mantis.** The framework consists of a backbone network, a DVF head, and an action head. The DVF head predicts future frames to facilitate latent action learning, thereby improving action prediction. Language supervision helps maintain the backbone’s capability for understanding and reasoning. _Right:_ **Adaptive Temporal Ensemble.** Mantis-ATE dynamically adjusts the ensemble strength based on the overlap between target tokens and dynamic tokens. 

image frame) **o** _t_ . These inputs, together with [LAT], are packed into a sequence and mapped as 


**h** _t_ are then concatenated with **o** _t_ and fed into the connector _C_ , which projects them into the conditional input of _D_ to generate the future image frame **o** _t_ + _n_ with _n_ as the time step gap between the current and future frames: 


This design prevents the VLA backbone from producing redundant visual information directly. Besides, feeding **o** _t_ into _D_ via a residual connection [19] enables the [LAT] queries to capture inter-frame dynamics that characterize the visual trajectory rather than reconstructing complete frames. These dynamics connect to _latent actions_ —a visual manifestation of explicit robot motions—thereby providing targeted guidance for action prediction. 

Next, the actions for the next _n_ time steps can be generated by the action head _π_ via 


where the latent-action queries [LAT] is added to the context and the action queries [ACT] are used to extract information from the context. 

Furthermore, to produce denser visual predictions during training and accommodate diverse downstream tasks, we introduce multi-gap queries [GAP]. These queries are inserted before [LAT] to guide the generation of future frames at varying time step intervals. 

### **3.2. Model Specification** 

**VLM Backbone.** Considering the robust understanding and reasoning capabilities of Qwen2.5-VL [2], we adopt it as our backbone. Qwen2.5-VL natively supports flexible input resolutions, allowing us to assign higher resolution to the primary camera while allocating lower resolution to the wrist camera, which captures less spatial detail. 

**DVF Head.** We employ Sana [48] as the DVF head due to its superior performance in text-to-image generation. Sana is a highly efficient DiT that integrates a deep compression autoencoder [11]. We define a connector comprising 12 transformer encoder layers and a projection layer that bridges the backbone’s output space with the DiT’s input space, following the Qwen2.5 LLM architecture [50] while using bidirectional attention. During action inference, the DVF head is omitted to reduce computational overhead, as visual state prediction is not required for robot execution. 

**Action Head.** Following [54], we employ a DiT-based action head for action prediction. Learnable action queries first aggregate information from input and latent-action queries via causal attention, then the action head is used to denoise Gaussian noise into an _n_ -step action trajectory. 

### **3.3. Progressive Training Recipe** 

Directly fusing vision, language, and action during pretraining can bias learning toward the easiest signal ( _e.g_ ., actions) or overfit dominant modalities ( _e.g_ ., language), causing cross-modal competition and unstable convergence. To address this, we adopt a progressive training recipe that introduces modalities in stages, promoting more stable optimization (Fig. 2, left). The training proceeds in three stages: 

42508 


Figure 3. **Visualization of multi-gap future frame generation.** 

**Stage 1: Multiple Gap Vision Training.** We first train Mantis on videos without action annotations to predict future frames, encouraging the model to infer latent actions from visual dynamics. We use human manipulation videos so that Mantis learns general manipulation skills and broad world knowledge [51]. During training, we unfreeze the DVF head and latent-action queries, optimizing the diffusion loss _L_ DVF while keeping the backbone frozen to preserve its pretrained language representations. Additionally, the multi-gap queries are unfrozen to guide future frame generation across different time step intervals. Fig. 3 visualizes examples of multi-gap future frame generation. 

**Stage 2: Vision-Action Joint Training.** Then we introduce the action modality using a robot demonstration dataset. The time step gap is fixed to match the action chunk size for temporal alignment between visual and action streams. The model is optimized with _αL_ DVF + _L_ action, where _L_ action denotes the action head’s diffusion loss and _α_ balances the terms. In this stage, we unfreeze the action queries while keeping the backbone frozen. 

**Stage 3: Language Supervised Mix Training.** To supervise the language modality, we jointly train on a collection of multimodal datasets together with the robot demonstration data. The backbone is unfrozen, and a cross-entropy loss _L_ lang is applied to the language outputs. The overall objective is _αL_ DVF + _L_ action + _βL_ lang, where _α_ and _β_ weight the contributions of the vision and language losses. This progressive fusion yields stable and efficient optimization, producing a vision-augmented foundation with robust multimodal understanding for downstream tasks. 

### **3.4. Adaptive Temporal Ensemble** 

During inference, Mantis incorporates the commonly used Temporal Ensemble method [56] to enhance motion stability. Considering its high computational overhead, we also introduce an Adaptive Temporal Ensemble (ATE) strategy that dynamically adjusts the ensemble strength according to the motion stability required at each inference time step. 

As shown in Fig. 2 (right), ATE maintains two sets of input vision patches at each time step. **(1) Target patches** denote image regions that are most relevant to the language instruction. Following [49], we compute text-to-vision attention scores from Mantis backbone’s cross-attention module and select the top _τ_ target% of vision tokens with the highest 


Figure 4. **Visualization of ATE.** The attention heatmap uses darker colors to represent higher values, whereas in the cosine similarity heatmap the opposite holds. The parameters are set as _τ_ target = 1 and _τ_ dynamic = 12. 

scores. **(2) Dynamic patches** correspond to regions that exhibit significant visual changes. To detect them, we divide the current and previous input images into patches aligned with the vision tokens, compute the cosine similarity between corresponding patches in pixel space, and select the top _τ_ dynamic% with the lowest similarity values. 

Intuitively, dynamic patches capture the motion of the robotic arm and end-effector, while target patches highlight instruction-relevant objects. Overlap between them indicates fine-grained manipulations, such as grasping. As shown in Fig. 4, visualization of both patch types during Mantis inference supports this observation. When such overlap occurs, the Temporal Ensemble is activated to enhance motion stability; otherwise, it is disabled to improve computational efficiency. Integrating ATE into Mantis yields a more efficient variant, termed Mantis-ATE. For more details about ATE, please refer to Appendix A. 

## **4. Experiments** 

### **4.1. Implementation Details** 

**Basic configuration.** Mantis comprises 5.8 billion parameters in total: 3.7B in the backbone, 1.4B in the DVF head, 0.3B in the action head, and 0.3B in the VAE. We set the number of [LAT] to 9, [ACT] to 6, and [GAP] to 6 _×_ 3 corresponding to time step gaps from 1 to 6. The diffusion process uses 30 steps for the DVF head and 10 steps 

42509 

Table 1. **Comparison on the LIBERO benchmark.** Mantis exhibits superior performance on 3 of 4 tasks and attains the highest average success rate compared to existing baseline methods, demonstrating the effectiveness of leveraging DVF for action prediction. **Bold** indicates the best performance, and _<u>Italics</u>_ indicates the second-best performance. 

|||**Spatial**|**Object**|**Goal**|**Long**|**Avg.**|
|---|---|---|---|---|---|---|
||Diffusion Policy [15]|78.3|92.5|68.3|50.5|72.4|
|_ii_|OpenVLA [25]|84.7|88.4|79.2|53.7|76.5|
|_non-vson-_<br>_aumented_|_π_0[6]|96.8|_98.8_|**95.8**|85.2|94.2|
|_g_|_π_0-FAST [36]|96.4|96.8|88.6|60.2|85.5|
||NORA [20]|92.2|95.4|89.4|74.6|87.9|
||ATM [44]|68.5|68.0|77.8|39.3|63.4|
||CoT-VLA [55]|87.5|91.6|87.6|69.0|81.1|
||WorldVLA [9]|87.6|96.2|83.4|60.0|81.8|
|_vision-_|UniVLA [8]|96.5|96.8|_95.6_|92.0|95.2|
|_augmented_|UnifiedVLA [43]|95.4|_98.8_|93.6|_94.0_|95.5|
||DreamVLA [54]|97.5|94.0|89.5|89.5|92.6|
||_F_1[32]|_98.2_|97.8|95.4|91.3|_95.7_|
||Mantis (Ours)|**98.8**|**99.2**|94.4|**94.2**|**96.7**|


for the action head. Training adopts AdamW [31] with 0.1 weight decay and 0.5 gradient clipping, and leverages DeepSpeed [37] for efficient distributed training. 

**Pretraining Setup.** In _Stage 1_ , the model is pretrained on the SSV2 dataset [18], which contains approximately 220K videos of human manipulations. The time step gap is randomly sampled between 1 and 6. In _Stage 2_ , the model is pretrained on the DROID dataset [24], consisting of 76K robot episodes. The vision loss weight _α_ is set to 0.1. In _Stage 3_ , we introduce language supervision by jointly training on 38 multimodal datasets and DROID for 1.5 epochs. 

**Finetuning Setup.** For downstream finetuning on the LIBERO benchmark [28], we use the same learning rate configuration as in pretraining stages 1 and 2 and train for 30 epochs without language supervision. The vision loss weight is set to _α_ = 0 _._ 1. The checkpoint with the highest validation success rate (SR) is selected for final evaluation. Further implementation details are provided in Appendix B. 

### **4.2. Simulation Experiments** 

We evaluate Mantis on the widely adopted LIBERO benchmark [28], which comprises four task suites: Spatial, Object, Goal, and Long. Each suite contains 10 tasks, with 50 trials per task to reduce random variation. Performance is measured using Success Rate (SR) from 0 to 100, where higher is better. For comprehensive comparison, we select high-performance VLA models both with [8, 9, 32, 43, 44, 54, 55] and without [6, 15, 20, 25, 36] vision augmentation as baselines. We also compare the convergence speed of Mantis against four vision-augmented baselines. 


Figure 5. **Convergence speed comparison.** Compared with traditional visual foresight methods such as UnifiedVLA [43], Mantis achieves significantly faster convergence speed, underscoring the necessity of decoupling foresight prediction from action learning. 

**Main Results.** As shown in Table 1, Mantis exhibits superior performance on 3 of 4 task suites and attains the highest average SR, outperforming previous vision-augmented and non-vision-augmented methods. This underscores the efficacy of leveraging DVF to enhance action prediction. Furthermore, vision-augmented methods mostly outperform their non-vision-augmented counterparts, corroborating the findings in [27] that dense visual states effectively complement sparse action signals. Notably, ATM [44] exhibits inferior performance, which we attribute to the limited accuracy of point trajectories extracted via video tracking methods, resulting in accumulated errors. 

42510 


Figure 6. **Real World Experiments.** (a) The Agilex platform. (b) Scenario setups and example instructions. Each scenario shows one ID instruction and the corresponding OOD instruction. (c) Average success counts for Mantis and _π_ 0 _._ 5 on ID and OOD tasks across three scenarios. (d) Per-task success counts for Mantis and _π_ 0 _._ 5 in Scenario 1. 

**Convergence Speed.** We evaluate the convergence speed of Mantis and four baseline methods representing different learning paradigms: non-vision-augmentation (OpenVLA [25]), visual foresight (UnifiedVLA [43]), track guidance (ATM [44]), and latent action supervision (UniVLA [8]). Each model is fine-tuned from its pretrained checkpoint for 20 epochs on the LIBERO Spatial suite following the prescribed configuration. Evaluation is conducted at each epoch, and the results are presented as an epoch-SR line graph in Fig. 5. As illustrated, Mantis demonstrates a relatively fast convergence speed, comparable to the non-vision-augmented OpenVLA and the latent action supervision method UniVLA. In contrast, the entangled visual foresight approach, UnifiedVLA, converges the slowest, maintaining a success rate of zero during the first ten epochs. This observation highlights the necessity of decoupling foresight prediction from action learning in order to achieve efficient optimization. 

### **4.3. Real World Experiments** 

We evaluate Mantis on an Agilex platform (Fig. 6 (a)) to investigate the effect of language supervision on preserving the backbone’s capabilities. We design three experimental scenarios, each containing four in-domain (ID) instructions to assess instruction following and four out-of-domain (OOD) instructions to evaluate generalization. Fig. 6 (b) shows the setup of the scenarios and provides example instructions. Effective generalization demands a nuanced un- 

derstanding and reasoning. For example, the first scenario requires world knowledge ( _e.g_ ., Taylor Swift), while the second involves basic arithmetic logic. We compare Mantis with _π_ 0 _._ 5 [21], a state-of-the-art open-source VLA model. Both are fine-tuned separately on the three scenarios, with Mantis maintaining language supervision throughout training. Each instruction is executed 10 times, and performance is reported as the average number of successful executions, allowing up to 5 consecutive attempts per trial. 

As shown in Fig. 6 (c), Mantis consistently outperforms _π_ 0 _._ 5 on both ID and OOD instructions across all three scenarios, demonstrating its superior instruction-following capability, generalization to unseen instructions, and fundamental reasoning ability. In contrast, _π_ 0 _._ 5 exhibits subpar instruction-following ability and almost no generalization capability to OOD instructions (Fig. 6 (d)). This corroborates the efficacy of language supervision in preserving the backbone’s understanding and reasoning capability. Additionally, we activated the DVF head in certain experiments to collect the generated future frame sequences, as visualized in Fig. 7. Further details are provided in Appendix C. 

### **4.4. Ablation Study** 

**ATE Analysis.** We evaluated ATE’s impact on task execution speed by comparing the standard Mantis (TE) and Mantis-ATE across four LIBERO suites. We measured the average inference count (IC) and success rate (SR), where a lower IC indicates higher efficiency. The parameters are 

42511 


Figure 7. **Visualization of Generated Future Frames.** The last generated future frame closely mirrors the ground truth final state, substantiating the efficacy of the DVF in refining action prediction across diverse manipulation tasks. 


Figure 8. **Comparison between standard Mantis (TE) and Mantis-ATE.** The primary vertical axis denotes success rate (SR), and the secondary vertical axis denotes inference count (IC). 

set as _τ_ target = 1 and _τ_ dynamic = 12. As shown in Fig. 8, Mantis-ATE reduces the IC by nearly 50% while maintaining comparable performance, demonstrating a substantial improvement in inference efficiency. 

**DVF Ablations.** We evaluated the effect of the DVF through four architectural variants across four LIBERO suites: (1) vanilla-DVF, (2) flawed-DVF (DVF without the residual connection), (3) no-DVF (only the action head), and (4) pretrained-DVF (DVF pretrained on human and robot videos). The first three models were trained from scratch, while all four were trained for 30 epochs on each task suite. The best-performing checkpoint from each model was used for evaluation. The results, summarized in Table 2, show that the pretrained-DVF achieved the highest success rate (SR), followed by the vanilla-DVF, then the flawed-DVF, with the no-DVF configuration performing the 

Table 2. **Comparison of four DVF variants. Bold** indicates the best performance, _<u>Italics</u>_ indicates the second-best performance. 

||Spatial|Object|Goal|Long|Avg.|
|---|---|---|---|---|---|
|vanilla-DVF|_98.2_|_98.8_|93.6|_92.2_|_95.7_|
|flawed-DVF|96.8|97.0|_93.8_|89.8|94.4|
|no-DVF|93.4|93.0|90.4|88.2|91.3|
|pretrained-DVF|**98.4**|**99.0**|**94.0**|**93.2**|**96.2**|


worst. These results support the following conclusions: (a) DVF facilitates action learning, (b) the residual connection enables DVF to better capture latent actions, and (c) video pretraining further enhances the performance of DVF. 

**Language Supervision Ablations.** We assessed the understanding and reasoning abilities of Mantis using multiple multimodal benchmarks and performed ablation studies without language supervision in real-world settings. The results are provided in Appendix D. 

## **5. Conclusion, Limitations and Future Work** 

In this work, we present Mantis, a framework featuring Disentangled Visual Foresight (DVF). Simulation experiments demonstrate that DVF enhances performance and convergence speed, while real-world experiments validate the effectiveness of language supervision. Limitations include minor motion rollbacks in real-world scenarios due to missing robot state inputs. Future work will integrate richer inputs ( _e.g_ ., 3D point clouds) and optimize inference speed. 

42512 

## **Acknowledgements** 

This work was supported by Shanghai Key Technology R&D Program “New Generation of Information Technology” (No. 25511103700), NSF of China (Nos. 62306176, 92470118), Natural Science Foundation of Shanghai (No. 23ZR1428700), CCF-ALIMAMA TECH Kangaroo Fund (NO. CCF-ALIMAMA OF 2025010), and Ant Group. 

## **References** 

- [1] Xiang An, Yin Xie, Kaicheng Yang, Wenkang Zhang, Xiuwei Zhao, Zheng Cheng, Yirui Wang, Songcen Xu, Changrui Chen, Chunsheng Wu, et al. Llava-onevision-1.5: Fully open framework for democratized multimodal training. _arXiv preprint arXiv:2509.23661_ , 2025. 1, 2 

- [2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 2, 4 

- [3] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 2 

- [4] Homanga Bharadhwaj, Debidatta Dwibedi, Abhinav Gupta, Shubham Tulsiani, Carl Doersch, Ted Xiao, Dhruv Shah, Fei Xia, Dorsa Sadigh, and Sean Kirmani. Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. _arXiv preprint arXiv:2409.16283_ , 2024. 3 

- [5] Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation. In _ECCV_ , pages 306–324. Springer, 2024. 3 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0 : A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 6 

- [7] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [8] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2502.14420_ , 2025. 2, 3, 6, 7 

- [9] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 2, 3, 6 

- [10] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 2 

- [11] Junyu Chen, Han Cai, Junsong Chen, Enze Xie, Shang Yang, Haotian Tang, Muyang Li, Yao Lu, and Song Han. Deep compression autoencoder for efficient high-resolution diffusion models. _arXiv preprint arXiv:2410.10733_ , 2024. 4 

- [12] Jiuhai Chen, Zhiyang Xu, Xichen Pan, Yushi Hu, Can Qin, Tom Goldstein, Lifu Huang, Tianyi Zhou, Saining Xie, Silvio Savarese, et al. Blip3-o: A family of fully open unified multimodal models-architecture, training and dataset. _arXiv preprint arXiv:2505.09568_ , 2025. 2 

- [13] William Chen, Suneel Belkhale, Suvir Mirchandani, Oier Mees, Danny Driess, Karl Pertsch, and Sergey Levine. Training strategies for efficient embodied reasoning. _arXiv preprint arXiv:2505.08243_ , 2025. 3 

- [14] Yi Chen, Yuying Ge, Weiliang Tang, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 19752– 19763, 2025. 3 

- [15] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , 44 (10-11):1684–1704, 2025. 6 

- [16] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 3 

- [17] Chongkai Gao, Zixuan Liu, Zhenghao Chi, Junshan Huang, Xin Fei, Yiwen Hou, Yuxuan Zhang, Yudi Lin, Zhirui Fang, Zeyu Jiang, et al. Vla-os: Structuring and dissecting planning representations and paradigms in vision-languageaction models. _arXiv preprint arXiv:2506.17561_ , 2025. 2, 

   - 3 

- [18] Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska, Susanne Westphal, Heuna Kim, Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz Mueller-Freitag, et al. The” something something” video database for learning and evaluating visual common sense. In _Proceedings of the IEEE international conference on computer vision_ , pages 5842–5850, 2017. 2, 6 

- [19] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 770–778, 2016. 2, 4 

- [20] Chia-Yu Hung, Qi Sun, Pengfei Hong, Amir Zadeh, Chuan Li, U Tan, Navonil Majumder, Soujanya Poria, et al. Nora: A small open-sourced generalist vision language action model for embodied tasks. _arXiv preprint arXiv:2504.19854_ , 2025. 6 

- [21] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 2, 7 

- [22] Yuheng Ji, Huajie Tan, Jiayu Shi, Xiaoshuai Hao, Yuan Zhang, Hengyuan Zhang, Pengwei Wang, Mengdi Zhao, Yao 

42513 

Mu, Pengju An, et al. Robobrain: A unified brain model for robotic manipulation from abstract to concrete. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1724–1734, 2025. 3 

- [23] Yuming Jiang, Siteng Huang, Shengke Xue, Yaxi Zhao, Jun Cen, Sicong Leng, Kehan Li, Jiayan Guo, Kexiang Wang, Mingxiu Chen, et al. Rynnvla-001: Using human demonstrations to improve robot manipulation. _arXiv preprint arXiv:2509.15212_ , 2025. 3 

- [24] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2, 6 

- [25] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2, 6, 7 

- [26] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 2 

- [27] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. _arXiv preprint arXiv:2510.12796_ , 2025. 2, 6 

- [28] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 2, 6 

- [29] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023. 2, 1 

- [30] Yuliang Liu, Zhang Li, Mingxin Huang, Biao Yang, Wenwen Yu, Chunyuan Li, Xu-Cheng Yin, Cheng-Lin Liu, Lianwen Jin, and Xiang Bai. Ocrbench: on the hidden mystery of ocr in large multimodal models. _Science China Information Sciences_ , 67(12):220102, 2024. 1 

- [31] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 6 

- [32] Qi Lv, Weijie Kong, Hao Li, Jia Zeng, Zherui Qiu, Delin Qu, Haoming Song, Qizhi Chen, Xiang Deng, and Jiangmiao Pang. F1: A vision-language-action model bridging understanding and generation to actions. _arXiv preprint arXiv:2509.06951_ , 2025. 2, 3, 6 

- [33] Yao Mu, Qinglong Zhang, Mengkang Hu, Wenhai Wang, Mingyu Ding, Jun Jin, Bin Wang, Jifeng Dai, Yu Qiao, and Ping Luo. Embodiedgpt: Vision-language pre-training via embodied chain of thought. _Advances in Neural Information Processing Systems_ , 36:25081–25094, 2023. 2 

- [34] Xichen Pan, Satya Narayan Shukla, Aashu Singh, Zhuokai Zhao, Shlok Kumar Mishra, Jialiang Wang, Zhiyang Xu, 

Jiuhai Chen, Kunpeng Li, Felix Juefei-Xu, et al. Transfer between modalities with metaqueries. _arXiv preprint arXiv:2504.06256_ , 2025. 2 

- [35] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 2 

- [36] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for visionlanguage-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 6 

- [37] Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase, and Yuxiong He. Deepspeed: System optimizations enable training deep learning models with over 100 billion parameters. In _Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining_ , pages 3505– 3506, 2020. 6 

- [38] Qi Sun, Pengfei Hong, Tej Deep Pala, Vernon Toh, U-Xuan Tan, Deepanway Ghosal, and Soujanya Poria. Emma-x: An embodied multimodal action model with grounded chain of thought and look-ahead spatial reasoning. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 14199– 14214, 2025. 3 

- [39] Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models. _arXiv preprint arXiv:2405.09818_ , 2024. 2 

- [40] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2 

- [41] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 

- [42] Yihao Wang, Pengxiang Ding, Lingxiao Li, Can Cui, Zirui Ge, Xinyang Tong, Wenxuan Song, Han Zhao, Wei Zhao, Pengxu Hou, et al. Vla-adapter: An effective paradigm for tiny-scale vision-language-action model. _arXiv preprint arXiv:2509.09372_ , 2025. 2 

- [43] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arXiv preprint arXiv:2506.19850_ , 2025. 2, 3, 6, 7 

- [44] Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. _arXiv preprint arXiv:2401.00025_ , 2023. 2, 3, 6, 7 

- [45] Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 2 

- [46] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and 

42514 

- Tao Kong. Unleashing large-scale video generative pretraining for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 3 

Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 2 

- [47] Yecheng Wu, Zhuoyang Zhang, Junyu Chen, Haotian Tang, Dacheng Li, Yunhao Fang, Ligeng Zhu, Enze Xie, Hongxu Yin, Li Yi, et al. Vila-u: a unified foundation model integrating visual understanding and generation. _arXiv preprint arXiv:2409.04429_ , 2024. 2 

- [48] Enze Xie, Junsong Chen, Junyu Chen, Han Cai, Haotian Tang, Yujun Lin, Zhekai Zhang, Muyang Li, Ligeng Zhu, Yao Lu, et al. Sana: Efficient high-resolution image synthesis with linear diffusion transformers. _arXiv preprint arXiv:2410.10629_ , 2024. 4 

- [49] Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient visionlanguage-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 5 

- [50] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 4 

- [51] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 2, 3, 5 

- [52] Shukang Yin, Chaoyou Fu, Sirui Zhao, Ke Li, Xing Sun, Tong Xu, and Enhong Chen. A survey on multimodal large language models. _National Science Review_ , 11(12): nwae403, 2024. 1 

- [53] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 2, 3, 1 

- [54] Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, Xinqiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, Fan Lu, He Wang, et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025. 2, 3, 4, 6 

- [55] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _CVPR_ , pages 1702–1713, 2025. 2, 3, 6 

- [56] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 2, 5 

- [57] Zhongyi Zhou, Yichen Zhu, Minjie Zhu, Junjie Wen, Ning Liu, Zhiyuan Xu, Weibin Meng, Yaxin Peng, Chaomin Shen, Feifei Feng, et al. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 5377–5395, 2025. 2, 3, 1 

- [58] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, 

42515 

