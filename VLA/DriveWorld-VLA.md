---
title: "DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving"
date: "2026-02-06"
authors: "Feiyang jia; Lin Liu; Ziying Song; Caiyan Jia; Hangjun Ye; Xiaoshuai Hao"
venue: "ICML 2026"
url: https://arxiv.org/abs/2602.06521
pdf: https://arxiv.org/pdf/2602.06521
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06521)** / [論文ページ](https://arxiv.org/abs/2602.06521)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure 1._ **Comparison of VLA & World Model Coupling Strategies.** _(a) Disentangled Interaction_ : The world model acts as an external simulator, but its structural isolation from the VLA prevents effective latent knowledge transfer. _(b) Feature Sharing_ : Despite sharing representations, these models lack action-conditioned causal reasoning, which limits their counterfactual imagination and long-horizon planning. _(c) Our DriveWorld-VLA_ : By optimizing world model latents as decision variables, we enable unified causal “what-if” reasoning through controllable imagination in a shared latent space. _(d) Performance_ : DriveWorld-VLA achieves SOTA results—91.3 PDMS on NAVSIMv1, 86.8 EPDMS on NAVSIMv2, and 0.16 CR on nuScenes—significantly outperforming specialized baselines like LAW (Li et al., 2024a), Epona (Zhang et al., 2025), and HERMES-p (Zhou et al., 2025b). 

## **Abstract** 

End-to-end (E2E) autonomous driving has recently attracted increasing interest in unifying Vision–Language–Action (VLA) with World Models to enhance decision-making and forwardlooking imagination. However, existing methods fail to effectively unify future scene evolution and action planning within a single architecture due to inadequate sharing of latent states, limiting the impact of visual imagination on action decisions. To address this limitation, we propose **_DriveWorld-VLA_** , a novel framework that unifies world modeling and planning within a la- 

> *Equal contribution , _†_ Corresponding authors, _‡_ Project leader. 

> 1School of Computer Science and Technology, Beijing Key Laboratory of Traffic Data Mining and Embodied Intelligence, Beijing Jiaotong University<sup>2</sup> Xiaomi EV. Correspondence to: Caiyan Jia _<_ cyjia@bjtu.edu.cn _>_ , Xiaoshuai Hao _<_ haoxiaoshuai@xiaomi.com _>_ . 

tent space by tightly integrating VLA and world models at the representation level, which enables the VLA planner to benefit directly from holistic scene-evolution modeling and reducing reliance on dense annotated supervision. Additionally, **_DriveWorld-VLA_** incorporates the latent states of the world model as core decision-making states for the VLA planner, facilitating the planner to assess how candidate actions impact future scene evolution. By conducting world modeling entirely in the latent space, **_DriveWorld-VLA_** supports controllable, action-conditioned imagination at the feature level, avoiding expensive pixellevel rollouts. Extensive open-loop and closedloop evaluations demonstrate the effectiveness of **_DriveWorld-VLA_** , which achieves state-of-the-art performance with 91.3 PDMS on NAVSIMv1, 86.8 EPDMS on NAVSIMv2, and 0.16 3-second average collision rate on nuScenes. Code and models will be released in the DriveWorld-VLA. 

_Preprint. February 9, 2026._ 

1 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

## **1. Introduction** 

Autonomous driving is undergoing a transformative paradigm shift from modular pipelines toward End-to-End (E2E) learning (Cui et al., 2024). Despite their success in mapping sensor inputs to control signals (Song et al., 2025a; Liu et al., 2025; Liao et al., 2025; Song et al., 2025b), these models often lack the capacity for long-horizon reasoning and fail to comprehend the causal consequences of their actions. In response, the integration of VisionLanguage-Action (VLA) models with World Models (WM) has emerged as a promising frontier to bridge this gap. In this synergy, VLA models provide sophisticated multimodal perception and linguistic reasoning, while World Models empower agents with “prospective imagination” by explicitly modeling environmental dynamics and actionconditioned future states. 

Despite this potential synergy, existing attempts to unify these paradigms remain loosely coupled, typically falling into two suboptimal categories. The first class includes **_Disentangled Interaction_** methods (Yan et al., 2025; Yang et al., 2025a), as shown in Figure 1.(a), which treat the world model merely as an external simulator or data source. However, these methods create a structural bottleneck that prevents the VLA from internalizing fundamental physical laws and environment dynamics. The second category is composed of **_Feature-Sharing_** approaches (Zhang et al., 2025; Li et al., 2025b; Zhou et al., 2025b), depicted in Figure 1.(b), which employ shared representations for joint prediction but fail to leverage the world model’s most critical capability: explicit causal reasoning and prospective “what-if” imagination. Consequently, by neglecting the action-outcome causal chain, these models remain restricted to reactive planning rather than proactive, long-horizon optimization through counterfactual simulation. 

To address these limitations, we propose **_DriveWorld-VLA_** (as shown in Figure 1.(c)), a unified framework that integrates VLA and World Models across both representation and decision-making through three core innovations. First, **_Feature-Level Sharing_** utilizes Large Language Model (LLM) hidden states as a shared latent space for both imagination and action prediction, enabling the model to internalize fundamental physical laws and environmental dynamics within its core reasoning engine. Second, **_ActionConditioned “What-If” Reasoning_** leverages a Diffusion Transformer (DiT) architecture to perform prospective rollouts of multiple candidate actions; this empowers the agent to transition from reactive planning to proactive optimization by explicitly evaluating the long-term consequences of distinct trajectories. Third, a **_Three-Stage Progressive Training paradigm_** stabilizes joint optimization by sequentially aligning multi-modal perception with BEV generation, enforcing action-conditioned controllability via flow- 

matching, and finally retroactively refining VLA decisions through a closed-loop reward mechanism. Extensive evaluations across open-loop and closed-loop benchmarks demonstrate that **_DriveWorld-VLA_** achieves state-of-the-art performance, significantly outperforming specialized baselines in both reasoning accuracy and safety-critical planning. 

In summary, our main contributions are as follows: 

- We propose **_DriveWorld-VLA_** , a tightly coupled framework where a world model serves as the reasoning engine bridging action and prospective imagination. 

- We introduce Feature-Level Sharing that uses LLM hidden states as shared latent space for both imagination and action prediction, helping internalize physical laws and environment dynamics. 

- We develop action-conditioned “what-if” reasoning to generate and evaluate candidate trajectories for proactive, consequence-aware decision-making. 

- We conduct extensive evaluations on both closed-loop (NAVSIM) and open-loop (nuScenes) benchmarks, demonstrating feature-level sharing and causal rollout guidance are critical for robust decision-making. 

## **2. Related Works** 

**World Models for Autonomous Driving** World models (WMs) have emerged as a cornerstone for autonomous driving, providing a technical foundation for modeling complex environmental evolutions (Jia et al., 2025; Tu et al., 2025; Guan et al., 2024; Feng et al., 2025b). Early efforts such as DriveWorld (Min et al., 2024) and Vista (Gao et al., 2024b) focus on generating spatiotemporally consistent video sequences, while LidarDM (Zyrianov et al., 2025) and Copilot4D (Zhang et al., 2023) explore driving-conditioned point cloud synthesis. Other works, including ViDAR (Yang et al., 2024) and Occ-LLM (Xu et al., 2025), treat occupancy prediction as a foundational representation for world dynamics. Beyond pixel-level generation, some models map observations into latent spaces to forecast agent behaviors and motion (Li et al., 2024a; Hu et al., 2022), partially bridging the gap between conventional pipelines and holistic traffic modeling. Despite these advances, the community lacks a unified objective, with research often split between highfidelity future prediction and trajectory modeling. Only a few pioneering studies, such as HERMES (Zhou et al., 2025b) and Epona (Zhang et al., 2025), explicitly connect generative imagination with downstream planning. In this context, _DriveWorld-VLA_ unifies these paradigms by integrating generative modeling and decision-making within a single framework. 

**VLAs for Autonomous Driving** The rapid evolution of VLA models in autonomous driving is primarily fueled by the profound semantic understanding and reasoning capa- 

2 

#### **DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure 2._ **DriveWorld-VLA pipeline.** DriveWorld-VLA unifies action and prospective imagination through a progressive training scheme. **Stage 1** jointly learns future BEV imagination and action prediction from a shared latent representation. **Stage 2** conditions the generative branch on future actions, enabling controllable imagination that maps a given action sequence to its corresponding future. **Stage 3** closes the loop: first predicts actions, then imagines the resulting future, and finally uses reward feedback to refine action prediction. 

bilities of VLMs. Early research predominantly utilized VLMs as high-level semantic interpreters to process textualized driving logic and rule-based constraints (Xu et al., 2024; Zhou et al., 2025a; Yang et al., 2025b; Hao et al., 2025b;a). However, with the emergence of multi-modal foundation models, the paradigm has shifted toward end-toend VLA architectures that directly map multi-sensor inputs and linguistic instructions to control trajectories (Shao et al., 2024; Renz et al., 2025; Jiang et al., 2025). Recent frontiers have explored the deep integration of VLAs with world models to enable future-aware reasoning and latent state prediction (Zhou et al., 2025b; Li et al., 2025b; Zhou et al., 2025c; Wang et al., 2025; Zheng et al., 2025; Gao et al., 2024a; Gu et al., 2024). For instance, HERMES (Zhou et al., 2025b) jointly models scene interpretation and evolution, while DriveVLA-W0 (Li et al., 2025b) employs future image prediction as a self-supervised signal for VLA refinement. _DriveWorld-VLA_ advances this trajectory by unifying future visual prediction and action generation within a shared latent space, systematically bridging the gap between generative imagination and proactive decision-making. 

## **3. Method** 

_DriveWorld-VLA_ is designed to tightly integrate VLA model with World Model in a unified architecture that supports both multi-modal reasoning and prospective imagination. To progressively align representation learning, action con- 

trollability, and consequence-aware decision making, we adopt a three-stage training paradigm. Each stage incrementally unlocks a key capability of the world model, while ensuring stable joint optimization with the VLA. Specifically, the training process is organized into three sequential stages: VLA & WM Joint Training, Action Controllability Fine-Tuning and Guided Evaluation & Refinement. Figure 2 shows the pipeline of _DriveWorld-VLA_ . 

### **3.1. VLA & WM Joint Training** 

_DriveWorld-VLA_ supports multi-modal inputs, including multi-view images _It_ , textual prompts _Tt_ , historical actions _At−_ 1, and BEV representations _Bt_ . All modalities are independently tokenized before being fed into the VisionLanguage Model (VLM). Image and text tokenization follow InternVL (Zhu et al., 2025), while dedicated tokenizers are introduced for BEV features and historical actions. BEV features _Bt ∈_ R<sup>_H×W ×C_</sup> are extracted by BEVFormer (Li et al., 2024c), flattened spatially, and projected into the VLM embedding space as BEV tokens. Historical ego actions are serialized into natural language prompts and concatenated with textual instructions, then encoded using the same text tokenizer as InternVL. 

After tokenization, _It_ , _Tt_ , _At−_ 1, and _Bt_ are jointly fed into the VLM. The VLM aggregates information across all modalities and produces a sequence of hidden states. We extract the hidden states from the final VLM layer as a 

3 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

shared latent representation, denoted as _Ht_ , 


where _Ht_ serves as the common feature space for both future imagination and future action prediction. During this stage, _DriveWorld-VLA_ is trained to jointly perform **future imagination** and **action prediction** based on shared latent representation, facilitating the transfer of world model knowledge into the VLA. 

**Future imagination** is modeled in the BEV space. Denoiser takes _Ht_ and _Bt_ as input to predict future BEV states _Bt_ +∆ _t_ as below, 


which are then decoded by a lightweight segmentation head SEG, 


DENOISER comprises a history-conditioned branch and a future action-conditioned branch. At this stage, only historyconditioned branch is activated and enforce reasoning from historical observations. This lightweight branch provides dense future supervision, enabling predictive representation learning and effective training of images to BEV tokenizers. The future action-conditioned branch follows a generative paradigm to model controllable future evolution under different action sequences. 

**Action prediction** is formulated as trajectory forecasting. A lightweight action decoder takes _Ht_ , _Bt_ , and _At−_ 1 as input, and outputs the predicted future actions _A_<sup>_′_</sup> _t_ +∆ _t_<sup>:</sup> 


where ACT denotes an action decoder. 

**Supervision.** The future BEV state is supervised by decoding a semantic BEV map, while the action decoder is supervised via imitation learning on expert actions. The overall loss at this stage is defined as: 


where _Lseg_ supervises the semantic BEV map decoding and _Lact_ supervises the predicted actions. 

### **3.2. Action Controllability Fine-Tuning** 

During co-training, _DriveWorld-VLA_ is not conditioned on future actions, which prevents it from imagining outcomes based on prospective actions. As a result, _DriveWorld-VLA_ cannot form a closed-loop reasoning between actions and 


_Figure 3._ **The structure of Action-conditioned Flow-matching Denoiser.** The Denoiser conditions the flow-matching process on the BEV state and GT future actions. The BEV state is processed through LayerNorm, followed by scaling and Embedding. These features are then passed through DiT blocks to perform denoising and generate the future BEV states. 

future scene generation. Ideally, _DriveWorld-VLA_ should be aware of how its actions affect the future evolution of the environment to evaluate action quality, rather than solely extrapolating from historical observations. 

Motivated by this limitation, this stage focuses on endowing _DriveWorld-VLA_ with the capability of action-conditioned future imagination. Due to the absence of sensor observations in the BEV space, we adopt an explicit feature-level supervision strategy for BEV prediction, which fundamentally differs from downstream-task supervision used in prior works such as WoTE (Li et al., 2025c) and LAW (Li et al., 2024a). After co-training, _Bt_<sup>_′_producedbytheBEVtok-</sup> enizer and VLM can be reliably decoded into a semantic BEV map. We therefore treat this BEV latent space as a pretrained variational representation. Given future multiview images _It_ + _δt_ , we reuse the Stage 1 encoding pipeline to obtain the corresponding ground truth (GT) BEV latent representation _Bt_<sup>_′_</sup> +∆ _t_<sup>as follows:</sup> 


Subsequently, the second branch of the denoiser employs a DiT-based architecture to learn an action-conditioned flowmatching denoising process, using the BEV state _Bt_<sup>_′_and the</sup> GT future action _At_ +∆ _t_ as conditions, as shown in Figure 3. The supervision is defined as: 


where DIT = DENOISER<sup>2</sup> denotes the second branch of the denoiser and _x_ 0 _∼N_ ( **0** _,_ **I** ), _k_ represents timestep in the flow matching process and is uniformly sampled from the interval [1,N]. 

**Supervision.** In Action Controllablity Fine-Tuning stage, the overall loss _Ls_ 2 consists solely of the loss _LF M_ . 

4 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

### **3.3. Future-Guided Evaluation & Refinement** 

This stage aims to establish a closed-loop interaction between action prediction and future imagination based on the highly shared representation _Ht_ between the VLA and the world model. _DriveWorld-VLA_ is required not only to predict actions but also to effectively imagine the corresponding future outcomes induced by those actions, and to evaluate and refine actions according to the imagined future states. Given the _Bt_ , _Ht_ and _At−_ 1, _DriveWorld-VLA_ first predicts future actions _A_<sup>_′_</sup> _t_ +∆ _t_<sup>and generates future imagi-</sup> nation _Bt_ +∆ _t_ via the first denoising branch. The predicted actions are subsequently used to condition the second denoising branch, where Euler-based sampling is performed to produce action-conditioned future imagination _Bt_<sup>_′_</sup> +∆ _t_<sup>:</sup> 


where _Bt_<sup>_′_</sup> +∆ _t_<sup>=</sup><sup>_B_</sup> _t_<sup>_k_</sup> +∆<sup>+1</sup> _t_<sup>, and</sup><sup>_N_denotes the sampling steps</sup> and is set to 25. 

To evaluate the quality of predicted actions, we jointly consider the consistency between the action-conditioned imagination _Bt_<sup>_′_</sup> +∆ _t_<sup>and the corresponding future BEV representa-</sup> tion _Bt_ +∆ _t_ . A learned reward function _R_ assigns a scalar score ˆ _rt_ +∆ _t_ to each predicted trajectory, with ground-truth rewards obtained by executing the predicted trajectories in a simulator and performing online evaluation. This process can be formulated as, 


Beyond trajectory quality assessment, this reward-driven design promotes close-loop between future imagination and action generation. Rather than uniformly supervising all multi-modal predictions, training prioritizes trajectories with higher predicted rewards, reinforcing those that lead to more favorable imagined outcomes and enabling consequence-aware action refinement, 


**Supervision.** During this stage, DENOISER and VLM are frozen. Training focuses on refining the reward function and the action head. The future BEV latents generated by the two denoising branches are fused and fed into the segmentation decoder for supervised BEV decoding, resulting in three complementary supervision signals: 


where _Lseg_ also supervises the semantic BEV map decoding, _L_<sup>_′_</sup> _act_<sup>supervises the predicted actions weighted by re-</sup> wards and _Lrew_ supervises the reward function _R_ . 

## **4. Experiments** 

### **4.1. Details** 

**Dataset and Metrics.** We evaluate _DriveWorld-VLA_ on NAVSIMv1 (Dauner et al., 2024), NAVSIMv2 (Cao et al., 2025) and nuScenes (Caesar et al., 2020). **NAVSIMv1** is an autonomous driving planning benchmark built on the OpenScene (Contributors, 2023) dataset, providing 120 hours of driving data at 2 Hz with multi-camera inputs and fused LiDAR point clouds. NAVSIMv1 adopts a non-reactive open-loop simulation protocol, where the core metric Predictive Driver Model Score (PDMS) is defined as the product of a penalty term and a weighted average score. The penalty term reflects constraint satisfaction such as No Collision (NC) and Drivable Area Compliance (DAC), while the weighted average combines Ego Progress (EP), TimeTo-Collision (TTC), and Comfort (C) with weights of 5:5:2. **NAVSIMv2** proposes a two-stage pseudo-simulation evaluation. Its core metric is called the Extended Predictive Driver Model Score (EPDMS), which is constructed from the following metrics: No at-fault Collision (NC), Drivable Area Compliance (DAC), Driving Direction Compliance (DDC), Traffic Light Compliance (TLC), Ego Progress (EP), Time to Collision (TTC), Lane Keeping (LK), History Comfort (HC), and Extended Comfort (EC). For open-loop planning, **nuScenes** is a large-scale outdoor driving dataset with 1000 multi-modal scenes. Each scene lasts 20 s, is annotated at 2 Hz, and includes six synchronized camera images and LiDAR point clouds. We use L2 and Collision Rate (CR) as evaluation metrics. See Appendix A for more details. 

**Implementation.** For **NAVSIM** , we concatenate the leftfront view, front view, and right-front view in the order to form a 256 _×_ 1024 composite image as the model input. We use ResNet-34 (He et al., 2016) as the BEV encoder. Training is performed with the AdamW optimizer using an initial learning rate of 1e-4 and a batch size of 16. Each stage is trained for 20 epochs on 8 NVIDIA H20 GPUs, with a total training time of approximately 120 hours. For the **nuScenes** open-loop evaluation, the 6-view input images are resized to 640 _×_ 384. We adopt a Swin-T (Liu et al., 2021) backbone initialized with pretrained weights and follow BEV-Planner (Li et al., 2024d) to encode the BEV feature map. We train with AdamW using an initial learning rate of 7e-5 and a batch size of 1. Each stage is trained for 24 epochs on 8 NVIDIA H20 GPUs, for a total training time of approximately 93 hours. Note that, for a fair comparison, none of the nuScenes-based experiments uses ego-state information. 

### **4.2. Main Results** 

**NAVSIMv1.** Table 1 reports the closed-loop planning performance on NAVSIMv1. Our _DriveWorld-VLA_ achieves a PDMS of 91.3, outperforming top methods across dif- 

5 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

_Table 1._ Comparison with state-of-the-art methods on the **NAVSIMv1** (Dauner et al., 2024). Abbreviations: 1 _×_ C (front single-view camera), N _×_ C (surround multi-view cameras), L (LiDAR), NC (No Collision), DAC (Drivable Area Compliance), TTC (Time-ToCollision), EP (Ego Process), C (Comfort), PDMS (Predictive Driver Model Score). 

|Methods|Venue|Sensors|NC_↑_|DAC_↑_|TTC_↑_|C_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|---|---|
|Human|-|-|100.0|100.0|100.0|99.9|87.5|94.8|
|_E2E-based Methods_|||||||||
|TransFuser (Chitta et al.,2022)|TPAMI 2023|3_×_C+L|97.7|92.8|92.8|**100.0**|79.2|84.0|
|PARA-Drive (Weng et al.,2024)|CVPR 2024|6_×_C|97.9|92.4|93.0|99.8|79.3|84.0|
|<br>Hydra-MDP (Li et al.,2024b)|arXiv 2024|3_×_C+L|98.3|96.0|94.6|**100.0**|78.7|86.5|
|<br>DiffusionDrive (Liao et al.,2025)|CVPR 2025|3_×_C+L|98.2|96.2|94.7|**100.0**|82.2|88.1|
|_World-Model-based Methods_|||||||||
|LAW (Li et al.,2024a)|ICLR 2024|1_×_C|96.4|95.4|88.7|99.9|81.7|84.6|
|DrivingGPT (Chen et al.,2025)|ICCV 2025|1_×_C|98.9|90.7|94.9|95.6|79.7|82.4|
|<br>WoTE (Li et al.,2025c)|ICCV 2025|3_×_C+L|98.5|96.8|94.4|99.9|81.9|88.3|
|<br>Epona (Zhang et al.,2025)|ICCV 2025|3_×_C|97.9|95.1|93.8|99.9|80.4|86.2|
|_VLA-based Methods_|||||||||
|AutoVLA (Zhou et al.,2025c)|NeurIPS 2025|3_×_C|98.4|95.6|**98.0**|99.9|81.9|89.1|
|<br>Recogdrive (Li et al.,2025d)|ICLR 2026|3_×_C|98.2|97.8|95.2|99.8|83.5|89.6|
|<br>DriveVLA-W0 (Li et al.,2025b)|ICLR 2026|1_×_C|98.7|**99.1**|95.3|99.3|83.3|90.2|
|**DriveWorld-VLA (Ours)**|-|3_×_C|**99.1**|98.2|96.1|**100.0**|**85.9**|**91.3**|


_Table 2._ Comparison with state-of-the-art methods on the **NAVSIMv2** (Cao et al., 2025). Abbreviations: NC (No at-fault Collision), DAC (Drivable Area Compliance), DDC (Driving Direction Compliance), TLC (Traffic Light Compliance), EP (Ego Progress), TTC (Time to Collision), LK (Lane Keeping), HC (History Comfort), EC (Extended Comfort), EPDMS (Extended Predictive Driver Model Score). 

|Methods|NC_↑_|DAC_↑_|DDC_↑_|TLC_↑_|EP_↑_|TTC_↑_|LK_↑_|HC_↑_|EC_↑_|EPDMS_↑_|
|---|---|---|---|---|---|---|---|---|---|---|
|_E2E-based Methods_|||||||||||
|TransFuser (Chitta et al.,2022)|96.9|89.9|97.8|99.7|87.1|95.4|92.7|**98.3**|87.2|76.7|
|DiffusionDrive (Liao et al.,2025)|98.2|95.9|99.4|**99.8**|87.5|97.3|96.8|**98.3**|**87.7**|84.5|
|HydraMDP++ (Li et al.,2025a)|97.2|97.5|99.4|99.6|83.1|96.5|94.4|98.2|70.9|81.4|
|Drivesuprim (Yao et al.,2025)|97.5|96.5|99.4|99.6|**88.4**|96.6|95.5|**98.3**|77.0|83.1|
|ARTEMIS (Feng et al.,2025a)|98.3|95.1|98.6|**99.8**|81.5|97.4|96.5|**98.3**|-|83.1|
|_VLA-based Methods_|||||||||||
|DriveVLA-W0 (Li et al.,2025b)<br>|98.5|**99.1**|98.0|99.7|86.4|**98.1**|93.2|97.9|58.9|86.1|
|**DriveWorld-VLA (Ours)**|**98.6**|**99.1**|**99.6**|**99.8**|87.4|97.9|**97.0**|97.8|78.6|**86.8**|


ferent paradigms, including DiffusionDrive (Liao et al., 2025), WoTE (Li et al., 2025c), and DriveVLA-W0 (Li et al., 2025b). Notably, _DriveWorld-VLA_ attains an NC of 99.1 and an EP of 85.9, suggesting that our policy effectively enforces safety constraints while sustaining efficient forward progress. 

**NAVSIMv2.** Table 2 reports the closed-loop planning performance on NAVSIMv2. _DriveWorld-VLA_ achieves an EPDMS of 86.8, again outperforming all compared methods. Particularly, it performs excellently in DAC, DDC, and LK, achieving 99.1, 99.6, and 97.0, respectively. 

**nuScenes.** Table 3 reports the 3-second planning results on the nuScenes (Caesar et al., 2020) validation dataset. The performance of recent methods suggests that short-horizon planning has been extensively studied. Compared with E2E-based methods and world-model-based methods, our _DriveWorld-VLA_ demonstrates a clear advantage, achieving an average L2 of 0.61m and a collision rate as low as 0.16%. Even relative to the state-of-the-art approaches FSDrive (Zeng et al., 2025) and HERMES-p (Zhou et al., 2025b), _DriveWorld-VLA_ still maintains a decisive advantage in terms of collision rate. These results indicate that 

the policy of _DriveWorld-VLA_ is beneficial throughout the entire short-horizon planning process. We reiterate that ego-state information is disabled. 

### **4.3. Ablation Study** 

**Ablation on training process.** Table 4 presents the performance of different stages of the _DriveWorld-VLA_ training process across various datasets. For NAVSIMv1 (Dauner et al., 2024), each training stage significantly improves the model’s performance, with PDMS achieving increases of +1.9 and +1.8, respectively. For nuScenes (Caesar et al., 2020), the positive impact of Stage 2 is more pronounced. Short-term planning in the 2nd and 3rd seconds shows almost no improvement from Stage 3, with only -0.01 and -0.02 changes. We propose two hypotheses to explain this phenomenon. First, open-loop planning tasks do not necessarily benefit from generative supervision at all times. Second, the Reward Model has a greater effect on closed-loop planning than on open-loop planning. From an engineering perspective, _DriveWorld-VLA_ uses different baselines (Li et al., 2025c; 2024a) and Reward Models across the two benchmarks. From a theoretical standpoint, the integration 

6 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

_Table 3._ Comparison with state-of-the-art methods on the **nuScenes** (Caesar et al., 2020) validation dataset.<sup>_∗_</sup> denotes results reproduced with the official checkpoint. Abbreviations: C (surround multi-view cameras), CR (Collision Rate). 

|Methods|Venue|Sensors||L2(|m)_↓_|||CR(|%)_↓_||
|---|---|---|---|---|---|---|---|---|---|---|
||||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|_E2E-based Methods_|||||||||||
|UniAD (Hu et al.,2023)|CVPR 2023|C|0.48|0.96|1.65|1.03|0.05|0.17|0.71|0.31|
|<br>VAD (Jiang et al.,2023)|ICCV 2023|C|0.41|0.70|1.05|0.72|0.07|0.17|0.41|0.22|
|<br>MomAD (Song et al.,2025a)|CVPR 2025|C|0.43|0.88|1.62|0.98|0.06|0.16|0.68|0.30|
|_World-Model-based Methods_|||||||||||
|LAW<sup>_∗_</sup>(Li et al.,2024a)|ICLR 2024|C|0.31|0.61|1.02|0.65|0.27|0.21|0.54|0.34|
|GenAD (Zheng et al.,2024)|ECCV 2024|C|0.36|0.83|1.55|0.91|0.06|0.23|1.00|0.43|
|<br>Epona (Zhang et al.,2025)|ICCV 2025|C|0.61|1.17|1.98|1.25|0.01|0.22|0.85|0.36|
|<br>FSDrive (Zeng et al.,2025)|NeurIPS 2025|C|0.28|0.52|0.80|0.53|0.06|0.13|**0.32**|0.17|
|_VLA-based Methods_|||||||||||
|HERMES-p (Zhou et al.,2025b)|ICCV 2025|C|**0.16**|**0.32**|**0.59**|**0.36**|**0.00**|0.14|0.82|0.32|
|<br>**DriveWorld-VLA (Ours)**|-|C|0.28|0.58|0.99|0.61|**0.00**|**0.10**|0.38|**0.16**|


_Table 4._ Ablation study of **training process** on **NAVSIMv1** (Dauner et al., 2024) and **nuScenes** (Caesar et al., 2020) validation dataset. 

|Tr|aining Proc|ess||NA|VSIMv1|(Closed-|Loop)|||nuScenes|(Open-Loop|)|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Stage 1|Stage 2|Stage 3|NC_↑_|DAC_↑_|TTC_↑_|C_↑_|EP_↑_|PDMS_↑_|CR_↓_@1s|CR_↓_@2s|CR_↓_@3s|CR_↓_@Avg.|
|_×_|_×_|_×_|98.5|95.8|94.4|99.9|80.9|87.1|0.27|0.21|0.54|0.34|
|✓|_×_|_×_|98.6|96.1|95.1|99.9|81.0|87.6|0.09|0.19|0.48|0.25|
|✓|✓|_×_|98.9|97.3|94.4|100.0|84.5|89.5|0.05|0.11|0.40|0.19|
|✓|✓|✓|99.1|98.2|96.1|100.0|85.9|91.3|0.00|0.10|0.38|0.16|


_Table 5._ Ablation study of **training strategies** on **NAVSIMv1** (Dauner et al., 2024). ‘Non-progressive’ denotes that Stage 2 and Stage 3 are trained simultaneously after the completion of Stage 1, while ‘Progressive’ denotes the strategy adopted in our work. 

|Training Strategies|NC_↑_|DAC_↑_|TTC_↑_|C_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|
|Non-progressive<br>|97.8<br>|94.5<br>|93.5<br>|99.9<br>|75.6<br>|83.6<br>|
|Progressive|99.1|98.2|96.1|100.0|85.9|91.3|


_Table 7._ Ablation study of **Supervision** on **NAVSIMv1** (Dauner et al., 2024). 

|Supervision<br>Task<br>Features|NC_↑_|DAC_↑_|TTC_↑_|C_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|
|✓<br>_×_|98.7|96.3|94.0|100.0|82.9|87.9|
|✓<br>✓|99.1|98.2|96.1|100.0|85.9|91.3|


_Table 6._ Ablation study of **VLM Strategies** on **NAVSIMv1** (Dauner et al., 2024). ‘Freeze’ denotes whether the parameters of VLM are also frozen during Stage 1. ‘Pre-train’ denotes whether the pre-training strategy aligned with RecogDrive (Li et al., 2025d) is adopted. 

|VLM<br>Freeze|Strategies<br>Pre-train|NC_↑_|DAC_↑_|TTC_↑_|C_↑_|EP_↑_|PDMS_↑_|
|---|---|---|---|---|---|---|---|
|✓|_×_|98.4|95.7|96.2|99.9|80.4|87.2|
|✓|✓|98.6|96.1|95.1|99.9|81.0|87.6|
|_×_|✓|98.7|96.7|95.6|99.9|83.1|88.3|


of generative tasks and planning tasks is constrained by the feedback mechanism within the inference process. 

**Ablation on training strategies.** Table 5 shows the performance of _DriveWorld-VLA_ under different training strategies. The ‘Non-progressive’ strategy refers to updating the parameters of both the future imagination branch and the action prediction branch after Stage 1, enabling the reward model, and using double the training length for a fair comparison. The ‘Progressive’ strategy follows the training scheme outlined in Figure 2. Clearly, the ‘Non-progressive’ 

strategy results in a significant performance drop, achieving -7.7 PDMS, which indicates that our strategy is effective and non-redundant. The model must first learn from the GT action and enhance the latent feature space before benefiting from action prediction. Additionally, this further demonstrates that even within the same feature space, generative and planning tasks need to be asynchronously unified. 

**Ablation on VLM strategies.** Table 6 shows the different VLM strategies used during the training of _DriveWorld-VLA_ . ‘Freeze’ indicates whether the VLM parameters are frozen during Stage 1, and ‘Pre-Train’ indicates whether the VLM is pre-trained and fine-tuned following the settings in RecogDrive (Li et al., 2025d) (conducting 3 epochs of SFT using the dataset constructed by the hierarchical data pipeline). The optimal strategy is shown in the third row of the table. Both omitting pre-training and fully freezing the VLM parameters limit the model’s performance. This indicates that while non-targeted pre-training can contribute, it does not fully unlock the VLM’s potential. The VLM parameters must undergo optimization through a learning process during the initial stage to accurately model shared space features and enhance the model’s performance. Consider- 

7 

#### **DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure 4._ **The 4s trajectory planning visualization examples from NAVSIM (Dauner et al., 2024) for DriveWorld-VLA** . Stage 2 generates predictions similar to the GTs, but with a higher collision risk. In contrast, Stage 3 introduces future imagination, resulting in more robust predictions and significantly reducing the collision risk. The changes observed across the training stages confirm the accuracy of world modeling and its understanding of physical dynamics. Left label: sample tokens. Top label: source of trajectory. 

ing the future need for lightweight design, we believe that completely abandoning VLM updates is also acceptable. 

**Ablation on Supervision.** Table 7 shows the impact of task-level supervision and feature-level supervision on _DriveWorld-VLA_ . _Lseg_ and _Lact_ are considered task-level supervision, while the supervision from the denoising process is considered feature-level supervision. We introduce noise that follows the distribution _N_ (0 _,_ 5) into the latent variables during the inference phase, in order to mitigate the constraining effect of feature-level supervision. The results show that weakening feature-level supervision leads to a decline in model performance. Relying solely on task-level supervision causes the model to lack fine-grained feature guidance, which in turn affects performance. 

### **4.4. Visualization** 

As shown in Figure 4, we provide some visual examples stemming from NAVSIM (Dauner et al., 2024) for _DriveWorld-VLA_ . By the Figure, _DriveWorld-VLA_ with three-stage training scheme empowered by future imagination demonstrates excellent and progressive planning results. 

See Appendix B for more illustration samples (Figures S2S6 for NAVSIM and Figures S7-S8 for nuScenes). 

## **5. Conclusion** 

In this study, we introduce **_DriveWorld-VLA_** , a novel framework designed to enhance autonomous driving decisionmaking and forward-looking reasoning by tightly integrating VLA and world models. _DriveWorld-VLA_ shares scene representations within the latent space, allowing the VLA to benefit more effectively from the world model. This integration enables direct access to global information regarding the future evolution of scenes, which is then applied to the decision-making process. Unlike existing approaches, _DriveWorld-VLA_ uses the latent states of the world model as the basis for decision-making, assisting the system in evaluating the long-term impact of actions on future scenarios. We conduct extensive closed-loop and open-loop planning evaluations of _DriveWorld-VLA_ across multiple benchmarks. The results demonstrate that _DriveWorld-VLA_ significantly outperforms current state-of-the-art methods, showcasing its immense potential in decision-making. 

8 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

## **Impact Statement** 

This paper presents work aimed at advancing the field of end-to-end autonomous driving by integrating VisionLanguage-Action (VLA) and World Models to enhance decision-making and forward-looking imagination. The datasets and references used in this work are publicly available, and the goal is to improve the safety of autonomous driving systems. We believe this work has positive societal implications, particularly in the context of autonomous vehicle technology, by contributing to safer transportation systems. Additionally, there are no specific ethical concerns that we feel must be highlighted here at this stage. 

## **References** 

- Caesar, H., Bankiti, V., Lang, A. H., Vora, S., Liong, V. E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., and Beijbom, O. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11621–11631, 2020. 

- Cao, W., Hallgarten, M., Li, T., Dauner, D., Gu, X., Wang, C., Miron, Y., Aiello, M., Li, H., Gilitschenski, I., et al. Pseudo-simulation for autonomous driving. _arXiv preprint arXiv:2506.04218_ , 2025. 

- Chen, Y., Wang, Y., and Zhang, Z. Drivinggpt: Unifying driving world modeling and planning with multimodal autoregressive transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 26890–26900, 2025. 

- Chitta, K., Prakash, A., Jaeger, B., Yu, Z., Renz, K., and Geiger, A. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _IEEE transactions on pattern analysis and machine intelligence_ , 45(11): 12878–12895, 2022. 

- Contributors, O. Openscene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving. In _Proceedings of the Conference on Computer Vision and Pattern Recognition, Vancouver, Canada_ , pp. 18–22, 2023. 

- Cui, C., Ma, Y., Cao, X., Ye, W., Zhou, Y., Liang, K., Chen, J., Lu, J., Yang, Z., Liao, K.-D., et al. A survey on multimodal large language models for autonomous driving. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pp. 958–979, 2024. 

- Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. _Advances in Neural Information Processing Systems_ , 37:28706–28719, 2024. 

- Feng, R., Xi, N., Chu, D., Wang, R., Deng, Z., Wang, A., Lu, L., Wang, J., and Huang, Y. Artemis: Autoregressive end-to-end trajectory planning with mixture of experts for autonomous driving. _arXiv preprint arXiv:2504.19580_ , 2025a. 

- Feng, T., Wang, W., and Yang, Y. A survey of world models for autonomous driving. _arXiv preprint arXiv:2501.11260_ , 2025b. 

- Gao, D., Cai, S., Zhou, H., Wang, H., Soltani, I., and Zhang, J. Cardreamer: Open-source learning platform for world model based autonomous driving. _IEEE Internet of Things Journal_ , 2024a. 

- Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., and Li, H. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems_ , 37: 91560–91596, 2024b. 

- Gu, S., Yin, W., Jin, B., Guo, X., Wang, J., Li, H., Zhang, Q., and Long, X. Dome: Taming diffusion model into high-fidelity controllable occupancy world model. _arXiv preprint arXiv:2410.10429_ , 2024. 

- Guan, Y., Liao, H., Li, Z., Hu, J., Yuan, R., Li, Y., Zhang, G., and Xu, C. World models for autonomous driving: An initial survey. _IEEE Transactions on Intelligent Vehicles_ , 2024. 

- Hao, X., Diao, Y., Wei, M., Yang, Y., Hao, P., Yin, R., Zhang, H., Li, W., Zhao, S., and Liu, Y. Mapfusion: A novel bev feature fusion network for multi-modal map construction. _Information Fusion_ , 119:103018, 2025a. 

- Hao, X., Zhou, L., Huang, Z., Hou, Z., Tang, Y., Zhang, L., Li, G., Lu, Z., Ren, S., Meng, X., et al. Mimo-embodied: X-embodied foundation model technical report. _arXiv preprint arXiv:2511.16518_ , 2025b. 

- He, K., Zhang, X., Ren, S., and Sun, J. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 770–778, 2016. 

- Hu, A., Corrado, G., Griffiths, N., Murez, Z., Gurau, C., Yeo, H., Kendall, A., Cipolla, R., and Shotton, J. Model-based imitation learning for urban driving. _Advances in Neural Information Processing Systems_ , 35:20703–20716, 2022. 

- Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 17853–17862, 2023. 

9 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

- Jia, F., Jia, C., Song, Z., Bao, Z., Liu, L., Xu, S., Gong, Y., Yang, L., Zhang, X., Sun, B., et al. Progressive robustnessaware world models in autonomous driving: A review and outlook. _Authorea Preprints_ , 2025. 

- Jiang, A., Gao, Y., Sun, Z., Wang, Y., Wang, J., Chai, J., Cao, Q., Heng, Y., Jiang, H., Dong, Y., et al. Diffvla: Visionlanguage guided diffusion planning for autonomous driving. _arXiv preprint arXiv:2505.19381_ , 2025. 

- Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., and Wang, X. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 8340–8350, 2023. 

- Li, K., Li, Z., Lan, S., Xie, Y., Zhang, Z., Liu, J., Wu, Z., Yu, Z., and Alvarez, J. M. Hydra-mdp++: Advancing end-to-end driving via expert-guided hydra-distillation. _arXiv preprint arXiv:2503.12820_ , 2025a. 

- Li, Y., Fan, L., He, J., Wang, Y., Chen, Y., Zhang, Z., and Tan, T. Enhancing end-to-end autonomous driving with latent world model. _arXiv preprint arXiv:2406.08481_ , 2024a. 

- Li, Y., Shang, S., Liu, W., Zhan, B., Wang, H., Wang, Y., Chen, Y., Wang, X., An, Y., Tang, C., et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. _arXiv preprint arXiv:2510.12796_ , 2025b. 

- Li, Y., Wang, Y., Liu, Y., He, J., Fan, L., and Zhang, Z. Endto-end driving with online trajectory evaluation via bev world model. _arXiv preprint arXiv:2504.01941_ , 2025c. 

- Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. _arXiv preprint arXiv:2506.08052_ , 2025d. 

- Li, Z., Li, K., Wang, S., Lan, S., Yu, Z., Ji, Y., Li, Z., Zhu, Z., Kautz, J., Wu, Z., et al. Hydra-mdp: End-to-end multimodal planning with multi-target hydra-distillation. _arXiv preprint arXiv:2406.06978_ , 2024b. 

- Li, Z., Wang, W., Li, H., Xie, E., Sima, C., Lu, T., Yu, Q., and Dai, J. Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2024c. 

- Li, Z., Yu, Z., Lan, S., Li, J., Kautz, J., Lu, T., and Alvarez, J. M. Is ego status all you need for open-loop end-to-end autonomous driving? In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 14864–14873, 2024d. 

- Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 12037–12047, 2025. 

- Liu, L., Jia, C., Yu, G., Song, Z., Li, J., Jia, F., Wu, P., Hao, X., and Luo, Y. Guideflow: Constraint-guided flow matching for planning in end-to-end autonomous driving. _arXiv preprint arXiv:2511.18729_ , 2025. 

- Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., and Guo, B. Swin transformer: Hierarchical vision transformer using shifted windows. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 10012–10022, 2021. 

- Min, C., Zhao, D., Xiao, L., Zhao, J., Xu, X., Zhu, Z., Jin, L., Li, J., Guo, Y., Xing, J., et al. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15522–15533, 2024. 

- Renz, K., Chen, L., Arani, E., and Sinavski, O. Simlingo: Vision-only closed-loop autonomous driving with language-action alignment. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 11993–12003, 2025. 

- Shao, H., Hu, Y., Wang, L., Song, G., Waslander, S. L., Liu, Y., and Li, H. Lmdrive: Closed-loop end-to-end driving with large language models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15120–15130, 2024. 

- Song, Z., Jia, C., Liu, L., Pan, H., Zhang, Y., Wang, J., Zhang, X., Xu, S., Yang, L., and Luo, Y. Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 22432–22441, 2025a. 

- Song, Z., Liu, L., Pan, H., Liao, B., Guo, M., Yang, L., Zhang, Y., Xu, S., Jia, C., and Luo, Y. Diver: Reinforced diffusion breaks imitation bottlenecks in end-to-end autonomous driving. _arXiv preprint arXiv:2507.04049_ , 2025b. 

- Tu, S., Zhou, X., Liang, D., Jiang, X., Zhang, Y., Li, X., and Bai, X. The role of world models in shaping autonomous driving: A comprehensive survey. _arXiv preprint arXiv:2502.10498_ , 2025. 

- Wang, H., Ye, X., Tao, F., Pan, C., Mallik, A., Yaman, B., Ren, L., and Zhang, J. Adawm: Adaptive world model 

10 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

based planning for autonomous driving. _arXiv preprint arXiv:2501.13072_ , 2025. 

- Weng, X., Ivanovic, B., Wang, Y., Wang, Y., and Pavone, M. Para-drive: Parallelized architecture for real-time autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 15449–15458, 2024. 

- Xu, T., Lu, H., Yan, X., Cai, Y., Liu, B., and Chen, Y. Occ-llm: Enhancing autonomous driving with occupancy-based large language models. _arXiv preprint arXiv:2502.06419_ , 2025. 

- Xu, Z., Zhang, Y., Xie, E., Zhao, Z., Guo, Y., Wong, K.Y. K., Li, Z., and Zhao, H. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _IEEE Robotics and Automation Letters_ , 2024. 

- Yan, T., Tang, T., Gui, X., Li, Y., Zhesng, J., Huang, W., Kong, L., Han, W., Zhou, X., Zhang, X., et al. Adr1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. _arXiv preprint arXiv:2511.20325_ , 2025. 

- Yang, J., Chitta, K., Gao, S., Chen, L., Shao, Y., Jia, X., Li, H., Geiger, A., Yue, X., and Chen, L. Resim: Reliable world simulation for autonomous driving. _arXiv preprint arXiv:2506.09981_ , 2025a. 

- Yang, Z., Chen, L., Sun, Y., and Li, H. Visual point cloud forecasting enables scalable autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pp. 14673–14684, 2024. 

- Yang, Z., Chai, Y., Jia, X., Li, Q., Shao, Y., Zhu, X., Su, H., and Yan, J. Drivemoe: Mixture-of-experts for visionlanguage-action model in end-to-end autonomous driving. _arXiv preprint arXiv:2505.16278_ , 2025b. 

   - Zheng, W., Song, R., Guo, X., Zhang, C., and Chen, L. Genad: Generative end-to-end autonomous driving. In _European Conference on Computer Vision_ , pp. 87–104. Springer, 2024. 

   - Zheng, Y., Yang, P., Xing, Z., Zhang, Q., Zheng, Y., Gao, Y., Li, P., Zhang, T., Xia, Z., Jia, P., et al. World4drive: Endto-end autonomous driving via intention-aware physical latent world model. _arXiv preprint arXiv:2507.00603_ , 2025. 

   - Zhou, X., Han, X., Yang, F., Ma, Y., Tresp, V., and Knoll, A. Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. _arXiv preprint arXiv:2503.23463_ , 2025a. 

   - Zhou, X., Liang, D., Tu, S., Chen, X., Ding, Y., Zhang, D., Tan, F., Zhao, H., and Bai, X. Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation. _arXiv preprint arXiv:2501.14729_ , 2025b. 

   - Zhou, Z., Cai, T., Zhao, S. Z., Zhang, Y., Huang, Z., Zhou, B., and Ma, J. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025c. 

   - Zhu, J., Wang, W., Chen, Z., Liu, Z., Ye, S., Gu, L., Tian, H., Duan, Y., Su, W., Shao, J., et al. Internvl3: Exploring advanced training and test-time recipes for open-source multimodal models. _arXiv preprint arXiv:2504.10479_ , 2025. 

   - Zyrianov, V., Che, H., Liu, Z., and Wang, S. Lidardm: Generative lidar simulation in a generated world. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6055–6062. IEEE, 2025. 

- Yao, W., Li, Z., Lan, S., Wang, Z., Sun, X., Alvarez, J. M., and Wu, Z. Drivesuprim: Towards precise trajectory selection for end-to-end planning. _arXiv preprint arXiv:2506.06659_ , 2025. 

- Zeng, S., Chang, X., Xie, M., Liu, X., Bai, Y., Pan, Z., Xu, M., and Wei, X. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. _arXiv preprint arXiv:2505.17685_ , 2025. 

- Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.-X., et al. Epona: Autoregressive diffusion world model for autonomous driving. _arXiv preprint arXiv:2506.24113_ , 2025. 

- Zhang, L., Xiong, Y., Yang, Z., Casas, S., Hu, R., and Urtasun, R. Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion. _arXiv preprint arXiv:2311.01017_ , 2023. 

11 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

## **A. More Experiment Details.** 

### **A.1. Prompt** 

In the system prompt for InternVL (Zhu et al., 2025), we include a description of the task, metrics, input and output. Figure S1 is an example for the two benchmarks (Dauner et al., 2024; Cao et al., 2025; Caesar et al., 2020). 

### **A.2. Image Tokens** 

We explicitly inject visual information into the input sequence in the form of a ‘text-domain visual placeholder token sequence’. Given an input image (after view stitching), we first perform adaptive tiling to accommodate varying aspect ratios. Where the image is partitioned into _NP_ feature patches of size 448 _×_ 448. When multiple patches are used, an additional 448 _×_ 448 thumbnail is appended to provide a global view. We then insert the textual prompts into a placeholder span delimited by special boundary markers (e.g., <img>...</img>), within which a dedicated placeholder token <IMG ~~C~~ ONTEXT> is repeated. We assign a fixed number of _K_ = 256 <IMG ~~C~~ ONTEXT> tokens to each patch. This design ensures that variations in image resolution or the number of patches are directly reflected in the number of text-side image tokens, while the overall sequence is subsequently tokenized and padded to a fixed maximum length. 

### **A.3. Vision-language Representation** 

On the vision side, we stack the normalized patches into a tensor in R<sup>_P ×_3</sup><sup>_×_448</sup><sup>_×_448</sup> , together with an accompanying mask that indicates which patches are valid. During multi-modal fusion, the model first locates all occurrences of <IMG ~~C~~ ONTEXT> in the text indices, and then applies a visual encoder to extract per-patch features and project them into the language hidden space. The resulting visual features and language tokens are jointly processed by the backbone network. This yields fused sequence hidden states **H** _∈_ R<sup>_B×L×D_</sup> , where _L_ denotes the maximum tokenized sequence length and _D_ is the language backbone hidden dimension. The representation thus captures both textual context and visual information carried at the <IMG ~~C~~ ONTEXT> positions. To obtain a fixed-length compact representation, we first linearly project the fused hidden states from _D_ = 1536 to a lower dimension _d_ = 256, producing **H**<sup>˜</sup> _∈_ R<sup>_B×L×d_</sup> . We then introduce a set of learnable latent query vectors **Z** 0 _∈_ R<sup>_B×NL×d_</sup> , where we set the number of latents to _NL_ = 700. Using cross-attention with **Z** 0 as queries and **H**<sup>˜</sup> as keys/values, we aggregate information from a variable-length sequence into a fixed-length representation **Z** _∈_ R<sup>_B×NL×d_</sup> , which serves as a compact vision–language representation for downstream tasks. 

## **B. More Visualization.** 

We have provided more visual examples showed in Figure S2, Figure S3, Figure S4, Figure S5 and Figure S6 for NAVSIM (Dauner et al., 2024), as well as Figure S7, Figure S8 for nuScenes (Caesar et al., 2020). 

12 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 

#### **For NAVSIM** 

You are a vehicle trajectory prediction model for autonomous driving. Your task is to predict the ego vehicle's 4-second trajectory based on the following inputs: multi-view images from 8 cameras, ego vehicle states (position), and discrete navigation commands. The input provides a 2-second history, and your output should ensure a safe trajectory for the next 4 seconds. Your predictions must adhere to the following metrics: 

1. Non Collisions (NC): Avoid collisions with other objects/vehicles. 

2. Drivable Area Compliance (DAC): Stay within the drivable area. 

3. Time to Collision (TTC): Maintain a safe distance from other vehicles. 

4. Ego Progress (EP): Ensure the ego vehicle moves forward without being stuck. 

5. Comfort (C): Avoid sharp turns and sudden decelerations. 

6. Driving Direction Compliance (DDC): Align with the intended driving direction. 

For evaluation, use the PDM Score, which combines these metrics: PDM Score = NC * DAC * (5*TTC + 5*EP + 2*C + 0*DDC) / 12. Your predictions will be evaluated through a non-reactive 4-second simulation with an LQR controller and background actors following their recorded trajectories. The better your predictions, the higher your score. 

#### **For nuScenes** 

You are an autonomous vehicle planning model for autonomous driving. Your task is to plan the ego vehicle's 3-second trajectory based on the following inputs: multi-view images from 6 cameras, ego vehicle states (position, velocity), and discrete navigation commands. The input provides a 2-second history, and your output should ensure a safe and efficient trajectory for the next 3 seconds. Your predictions will be evaluated using the following metrics: 

1. L2 Distance (L2): The square root of the sum of squared differences between the corresponding coordinates of predicted and actual points, measuring the accuracy of the predicted trajectory. 

2. Collision Rate (CR): Measures the safety of the predicted trajectory by quantifying the frequency of collisions with vehicles, pedestrians, and obstacles. The goal is to avoid such collisions. 

#### **Common** 

As an autonomous driving system, predict the vehicle's trajectory based on: 

1. Visual perception from camera 

2. Historical motion context (last 4 timesteps): {history_str} 3. Active navigation command: [{command_str}] Output requirements: Predict 8 future trajectory points 

- Each point format: (x:float, y:float, heading:float) 

- Use [PT, ...] to encapsulate the trajectory - Maintain numerical precision to 2 decimal places 

_Figure S1._ **InternVL system prompts** . _{_ history ~~s~~ tr _}_ denotes the ground-truth historical trajectory sequence, where each frame in the sequence is represented by a 2D coordinate. _{_ command ~~s~~ tr _}_ denotes navigation commands in text form, e.g., ‘turn left’, ‘go straight’ or ‘turn right’. The full prompt fed into the model is composed of each benchmark’s specific prompt and the common prompt. 

13 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure S2._ Visualization examples of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory. 

14 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure S3._ Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory. 

15 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure S4._ Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory. 

16 


_Figure S5._ Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory. 

17 

#### **DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure S6._ Visualization examples (cont.) of NAVSIM (Dauner et al., 2024). Left label: sample tokens. Top label: source of trajectory. 

18 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure S7._ Visualization examples of nuScenes (Caesar et al., 2020) validation dataset. Top label: source of trajectory. 

19 

**DriveWorld-VLA: Unified Latent-Space World Modeling with Vision–Language–Action for Autonomous Driving** 


_Figure S8._ Visualization examples (cont.) of nuScenes (Caesar et al., 2020) validation dataset. Top label: source of trajectory. 

20 

