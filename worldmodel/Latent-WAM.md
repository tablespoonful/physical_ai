---
title: "Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving"
date: "2026-03-25"
authors: "Linbo Wang; Yupeng Zheng; Qiang Chen; Shiwei Li; Yichen Zhang; Zebin Xing"
url: https://arxiv.org/abs/2603.24581
pdf: https://arxiv.org/pdf/2603.24581
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.24581)** / [論文ページ](https://arxiv.org/abs/2603.24581)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving** 

Linbo Wang<sup>†∗</sup> MAIS-SKL, CASIA Chongqing Chang’an Technology Co., Ltd. Zhongguancun Academy Beijing, China wanglinbo2026@ia.ac.cn 

Yupeng Zheng<sup>†</sup> MAIS-SKL, CASIA Beijing, China zhengyupeng2022@ia.ac.cn 

Qiang Chen Chongqing Chang’an Technology Co., Ltd. Beijing, China chenqiang01@changan.com.cn 

Shiwei Li Chongqing Chang’an Technology Co., Ltd. Beijing, China lisw2@changan.com.cn 

# Yichen Zhang 

MAIS-SKL, CASIA Beijing, China zhangyichen2026@ia.ac.cn 

Deheng Qian Chongqing Chang’an Technology Co., Ltd. Beijing, China qiandeheng@changan.com.cn 

Zebin Xing Qichao Zhang<sup>‡</sup> Xiang Li MAIS-SKL, CASIA MAIS-SKL, CASIA Tsinghua University Beijing, China Beijing, China Beijing, China xingzebin2024@ia.ac.cn zhangqichao2014@ia.ac.cn l-x21@mails.tsinghua.edu.cn Pengxuan Yang Yihang Dong Ce Hao<sup>‡</sup> MAIS-SKL, CASIA Zhongguancun Academy Zhongguancun Academy Beijing, China Beijing, China Beijing, China yangpengxuan2024@ia.ac.cn 2022190901025@std.uestc.edu.cn cehao@berkeley.edu 

Xiaoqing Ye<sup>‡</sup> Junyu Han Wuhan University Chongqing Chang’an Wuhan, China Technology Co., Ltd. yxq@whu.edu.cn Beijing, China hanjunyu@changan.com.cn 

## **Abstract** 

We introduce Latent-WAM, an efficient end-to-end autonomous driving framework that achieves strong trajectory planning through spatially-aware and dynamics-informed latent world representations. Existing world-model-based planners suffer from inadequately compressed representations, limited spatial understanding, and underutilized temporal dynamics, resulting in sub-optimal planning under constrained data and compute budgets. Latent-WAM addresses these limitations with two core modules: a Spatial-Aware Compressive World Encoder (SCWE) that distills geometric knowledge from a foundation model and compresses multi-view images into compact scene tokens via learnable queries, and a Dynamic Latent World Model (DLWM) that employs a causal Transformer to autoregressively predict future world status conditioned on historical visual and ego status representations. Extensive experiments 

∗Work done during internship at Chongqing Chang’an Technology Co., Ltd. This work is supported by Beijing Natural Science Foundation under Grant 4242052 and Beijing Nova Program (20240484562, 202604841268). 

†Equal contribution. ‡Corresponding author. §Project Leader. 

Yifeng Pan<sup>§</sup> Dongbin Zhao<sup>§</sup> Chongqing Chang’an MAIS-SKL, CASIA Technology Co., Ltd. Zhongguancun Academy Beijing, China Beijing, China panyifeng@changan.com.cn dongbin.zhao@ia.ac.cn 

on NAVSIM v2 and HUGSIM demonstrate new state-of-the-art results: 89.3 EPDMS on NAVSIM v2 and 28.9 HD-Score on HUGSIM, surpassing the best prior perception-free method by 3.2 EPDMS with significantly less training data and a compact 104M-parameter model. The code and model weights have been open-sourced at _https://github.com/yukki555/Latent-WAM_ . 

## **CCS Concepts** 

### • **Computing methodologies** → **Motion path planning** . 

## **Keywords** 

Autonomous Driving, Latent World Model, Scene Representation 

#### **ACM Reference Format:** 

Linbo Wang<sup>†</sup> , Yupeng Zheng<sup>†</sup> , Qiang Chen, Shiwei Li, Yichen Zhang, Zebin Xing, Qichao Zhang<sup>‡</sup> , Xiang Li, Deheng Qian, Pengxuan Yang, Yihang Dong, Ce Hao<sup>‡</sup> , Xiaoqing Ye<sup>‡</sup> , Junyu Han, Yifeng Pan<sup>§</sup> , and Dongbin Zhao<sup>§</sup> . 2026. Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving. In _Proceedings of the 34th ACM International Conference on Multimedia (MM ’26), November 10–14, 2026, Rio de Janeiro, Brazil._ ACM, New York, NY, USA, 19 pages. https://doi.org/10.1145/3767308.3835210 

This work is licensed under a Creative Commons Attribution 4.0 International License. _MM ’26, Rio de Janeiro, Brazil_ 

© 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2213-4/2026/11 

https://doi.org/10.1145/3767308.3835210 

## **1 Introduction** 

End-to-end autonomous driving has attracted considerable attention due to its data-driven nature and scalability. Prior methods 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 


**Figure 1: Performance vs. training data scale on NAVSIM v2. Bubble size indicates model parameters. Our Latent-WAM achieves the highest EPDMS with significantly fewer training data and smaller model size, demonstrating superior data efficiency over existing world-model-based methods. World4Drive is marked separately as it employs an additional ViT-L depth estimator.** 

integrate perception and prediction into a unified differentiable network, extracting planning-relevant representations for end-to-end trajectory prediction [14, 16]. However, these methods generally rely on complex auxiliary task designs and perception annotations, limiting further scaling of end-to-end driving algorithms. Largescale studies [52] further show that end-to-end driving performance scales predictably with data, motivating more effective representation learning from limited data. 

Recently, world-model-based approaches learn scene representations through temporal self-supervised learning, providing dense supervision while reducing the dependence on perception labels. These methods can be broadly categorized into two groups. The first group [21, 47] learns driving planning through explicit video generation. However, these methods suffer from high computational cost and tend to focus on visual details irrelevant to planning. The second group learns planning-relevant representations through implicit future latent prediction [20, 53]. Although the latent representations are relatively lightweight and capture dynamic information via temporal self-supervision, they still suffer from insufficient representation quality. Specifically: (1) the latent representations remain inadequately compressed; (2) they lack spatial understanding or rely on external depth estimation models at inference time, introducing additional latency; and (3) historical and dynamic information are underutilized, as these methods are restricted to single-step transition ( _𝑇_ → _𝑇_ +1), which severely limits the temporal understanding that driving demands. Autonomous driving requires modeling long-horizon interactions among surrounding agents. However, next-frame prediction provides only short-term supervision and misses the cumulative dynamics needed for robust planning. As illustrated in Fig. 1, these limitations lead to sub-optimal planning performance. 

To address these issues, we propose Latent-WAM, which comprises a Spatial-Aware Compressive World Encoder (SCWE) and 

a Dynamic Latent World Model (DLWM), targeting the two most planning-relevant understanding tasks—spatial and dynamic understanding—to achieve highly compressed driving world representations with improved planning performance. Specifically, SCWE distills knowledge from a geometric foundation model into the vision backbone and employs learnable queries to extract spatiallyinformed tokens from the enriched features, achieving high compression of scene information. DLWM departs from prior singlestep latent world models by autoregressively predicting _multi-frame_ future world status conditioned on historical scene and ego status representations. Rather than learning a local _𝑇_ → _𝑇_ +1 transition, DLWM models the full trajectory of world evolution across multiple future timesteps via a causal Transformer, providing substantially richer self-supervised signals that encourage the encoder to capture long-range temporal dependencies and cumulative dynamics. Furthermore, DLWM jointly predicts both visual scene changes and ego status (driving command, velocity, acceleration), coupling scene dynamics with self-state awareness to produce representations inherently attuned to planning-relevant motion patterns. As a result, DLWM is entirely discarded at inference, with the lightweight trajectory decoder directly consuming the enriched representations to generate planned trajectories. 

We extensively evaluate Latent-WAM on NAVSIM v2 [3] and HUGSIM [54]. Latent-WAM achieves 89.3 EPDMS on NAVSIM v2, 45.9 RC and 28.9 HD-score on HUGSIM, establishing new stateof-the-art results. Under the perception-free setting, our method outperforms previous approaches by 3.2 EPDMS. Notably, attention map visualization reveals that our world representations are highly focused on spatial structures and driving intent, demonstrating the effectiveness of our approach for planning-centric representation learning. Our contributions are summarized as follows: 

- We propose Spatial-Aware Compressive World Encoder, a novel scene compression method that distills geometric knowledge into the vision backbone to extract highly compressed, spatially-aware visual representations. 

- We propose Dynamic Latent World Model, which autoregressively models multi-frame world evolution with a causal Transformer. Joint prediction of visual dynamics and ego status provides richer self-supervised signals for temporal understanding, producing planning-effective representations that eliminate the need for explicit future prediction at inference time. 

- Our method achieves new state-of-the-art results on both NAVSIM v2 and HUGSIM, outperforming the best prior perception-free method [21] by 3.2 EPDMS. 

## **2 Related Work** 

## **2.1 Scene Representation in End-to-End Autonomous Driving** 

End-to-end autonomous driving directly optimizes trajectory planning, making the intermediate scene representation critical to overall performance. Early works [14, 29] adopt dense BEV layouts supervised by semantic maps and occupancy labels. Subsequent methods [4, 15, 16, 31] shift towards lightweight vectorized or sparse representations for improved efficiency. Recent efforts leverage VLMs [12, 28, 32, 51] for richer semantic information, or employ 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 


**Figure 2: Overall architecture of Latent-WAM. The framework consists of three modules: (1) Spatial-Aware Compressive World Encoder (SCWE) compresses images into compact scene tokens with geometric distillation for spatial understanding; (2) Dynamic Latent World Model (DLWM) predicts future world states from historical scene representations and ego status; (3) Trajectory Decoder forecasts 4-second trajectories. SCWE and DLWM jointly optimize the vision backbone. Notably, DLWM is used only during training and discarded at inference, while its prediction objective enriches the vision backbone, enabling the trajectory decoder to directly use SCWE representations for planning.** 

latent world models [20, 53] and video generation [39] for scene representation. Besides, recent end-to-end planners also explore generative trajectory modeling and safety-aware imitation learning. MeanFuser [35] achieves one-step multimodal trajectory generation, and Beyond Imitation [34] enhances safety via expert demonstrations and hard negatives. However, these methods often exhibit weak 3D spatial understanding and rely on cumbersome representations. We address these issues by distilling geometric knowledge into the vision backbone for stronger spatial understanding, while compressing scene information into a compact set of tokens via learnable queries. 

trajectory evaluation. Our method similarly adopts a latent world model, but fundamentally differs in two respects: (1) we predict multi-frame future world status rather than the standard single-step transition, providing richer self-supervised signals for temporal understanding; and (2) we jointly model scene dynamics and ego status, coupling spatial-temporal prediction with self-state awareness. We additionally incorporate 3D-RoPE for spatio-temporal position encoding. 

## **3 Method** 

## **3.1 Overall** 

## **2.2 World Models for Autonomous Driving** 

World models have been widely adopted in autonomous driving for environment representation and future state prediction. One line of work applies video generation models [9, 11, 13, 26, 37, 38, 49] to construct pixel-level driving world representations, while 3D world models based on occupancy and point clouds [7, 48, 50, 55] enforce geometric constraints in 3D space, with subsequent works [17, 18] unifying 2D and 3D modeling. Building on these capabilities, some approaches [19, 45] use world models as closed-loop simulators, while others [20, 21, 39, 47, 53] directly leverage them for planning. To reduce computational overhead, LAW [20], World4Drive [53], and Drive-JEPA [36] perform trajectory planning in the latent space. Recent works extend latent world models to reinforcement learning and safety-aware closed-loop planning: DreamerAD [44] leverages one for efficient policy optimization, while SoAD [10] combines a vector world model with safety-oriented value estimation for 

The overall architecture of Latent-WAM is illustrated in Fig. 2, consisting of three core modules: 1) Spatial-Aware Compressive World Encoder (Sec. 3.2), which uses learnable queries and a vision encoder to compress images into compact scene tokens and a geometric foundation model is used to distill geometric perception ability into the encoder to improve spatial understanding, 2) Dynamic Latent World Model (Sec. 3.3), a causal transformer decoder that models world transition dynamics by autoregressively predicting future world status conditioned on historical scene representations and ego status, and 3) Trajectory Decoder (Sec. 3.4), which forecasts trajectories over a 4-second horizon from world status representations. The SCWE and DLWM jointly optimize the vision backbone. Geometric distillation enhances spatial understanding, while selfsupervised learning improves temporal dynamics modeling. Notably, the DLWM is used exclusively during training and is entirely discarded at inference time. The world prediction objective serves 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 

to enrich the vision backbone with dynamic scene understanding, producing representations that already encode the temporal foresight needed for planning. During inference, the trajectory decoder directly employs these enriched representations from SCWE, eliminating any additional latency from auxiliary modules. 

## **3.2 Spatial-Aware Compressive World Encoder** 

To model long-horizon world state transition, world status representations need to be sufficiently lightweight while compressing rich scene information. Different from prior methods that rely on extensive visual information, we use only a small set of learnable queries that fully interact with image patch tokens from the inputs, compressing rich world perception information into the latent space. In addition, to enhance the spatial understanding of the vision backbone, we use a geometric foundation model WorldMirror [25] to inject geometric awareness into the backbone through distillation. 

_3.2.1_ **Scene Compression.** We use a set of compact scene tokens to compress the heavy vision tokens from multi-view images, forming a foundational component of world status representations. 

Given sequential multi-view images _𝐼_ ∈ R<sup>T×M×</sup><sup>_𝐻_×</sup><sup>_𝑊_×3</sup> as input, we first embed them into image patch tokens _𝑋_ ∈ R<sup>T×M×S×</sup><sup>_𝐷𝑒_</sup> , where T _,_ M _,_ S denote the temporal horizon, number of cameras, and number of image patches, respectively. A set of scene queries _𝑄_ scene ∈ R<sup>T×M×N×</sup><sup>_𝐷𝑒_</sup> are randomly initialized and concatenated with _𝑋_ . The concatenated features are fed into a DINO encoder E containing an MLP that projects to _𝐷𝑙_ -dimensional latent space, yielding frame-wise and view-specific scene representations _𝑄_<sup>ˆ</sup> scene ∈ R<sup>T×M×N×</sup><sup>_𝐷𝑙_</sup> and image tokens _𝑋_<sup>ˆ</sup> ∈ R<sup>T×M×S×</sup><sup>_𝐷𝑙_</sup> : 


where N is the number of scene query tokens, _𝐷𝑒_ the encoder dimension, and _𝐷𝑙_ the latent dimension. 

By integrating scene queries with raw image tokens, extensive visual information from numerous image patch tokens is efficiently compressed into a compact set of tokens, significantly reducing computational overhead for subsequent long-term world model training and trajectory planning. 

_3.2.2_ **Geometric Alignment.** To distill the spatial understanding capabilities of geometric models into the DINO encoder, we employ the image patch tokens output by SCWE as carriers for receiving dense spatial-semantic information from geometric features. 

Multi-view images across consecutive frames _𝐼_ are additionally fed into a geometric foundation model _𝑓𝑔_ , producing patch-level geometric features _𝑓𝑔_ ( _𝐼_ ) ∈ R<sup>**T**×</sup><sup>**M**×</sup><sup>**S**×</sup><sup>_𝐷𝑔_</sup> . The DINO backbone outputs _𝑋_ ˆ are subsequently projected via a geometric projector _𝜙_ , yielding _𝜙_ ( _𝑋_<sup>ˆ</sup> ) ∈ R<sup>**T**×</sup><sup>**M**×</sup><sup>**S**×</sup><sup>_𝐷𝑔_</sup> . Both _𝑓𝑔_ ( _𝐼_ ) and _𝜙_ ( _𝑋_<sup>ˆ</sup> ) are first normalized using LayerNorm, then we compute their cosine similarity loss: 


where cos(· _,_ ·) denotes cosine similarity, LN(·) denotes LayerNorm. 

Notably, since _𝑓𝑔_ remains frozen throughout training, the geometric features can be pre-computed and offline-cached, enabling direct loading during training without incurring repeated inference costs or GPU memory overhead. This design substantially reduces training time and computational expenses. 


**Figure 3: Teacher Forcing Attention Mask.** 

## **3.3 Dynamic Latent World Model** 

In this section, we propose a Dynamic Latent World Model (DLWM). By predicting future world status representations causally in the latent space, the backbone obtains temporal dynamics modeling capabilities through a self-supervised training paradigm under the perception-free setting. 

_3.3.1_ **World Latent Status Aggregation.** The per-camera scene tokens _𝑄_<sup>ˆ</sup> scene only capture isolated view-specific information, which is insufficient for holistic world modeling. To enable effective future prediction and trajectory planning, we aggregate these tokens and integrate with ego status to construct unified frame-wise world status representations. The ego status across consecutive frames, which include driving commands, velocity, and acceleration, is encoded by an ego status encoder (a single-layer MLP) into ego status embeddings _𝑆_ ego ∈ R<sup>**T**×</sup><sup>_𝐷𝑙_</sup> . The scene tokens _𝑄_<sup>ˆ</sup> scene from the SCWE and the ego status embeddings _𝑆_ ego collectively constitute the frame-wise world latent state. 

Specifically, scene tokens from different cameras are aggregated to form a holistic perception representation of the surrounding environment, which is subsequently concatenated with _𝑆_ ego encoding the ego status, yielding a unified Scene-Ego world status representation _𝑆_ world ∈ R<sup>**T**×(</sup><sup>**M**×</sup><sup>**N**+1)×</sup><sup>_𝐷𝑙_</sup> . This representation serves as the foundation for subsequent future world status prediction within the world model and trajectory planning. 

_3.3.2_ **Causal World Model Prediction.** We formulate world state transition dynamics modeling as an autoregressive prediction problem, where all future frame world status predictions are conditioned on historical world status representations, encompassing holistic scene representations and ego status. This unified autoregressive framework enables a natural training strategy: treating the alternating Scene-Ego world status token sequence _𝑆_ world<sup>_𝑖_as</sup> 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 

frame-wise blocks and adopting the standard next-token prediction paradigm to train the world model. 

In detail, we randomly initialize a set of learnable future world status queries _𝑄_ future ∈ R<sup>(</sup><sup>**T**−1)×(</sup><sup>**M**×</sup><sup>**N**+1)×</sup><sup>_𝐷𝑙_</sup> , with _𝑆_ world<sup>_𝑖,𝑖_∈{1</sup><sup>_, . . . ,_</sup> _𝑇_ − 1} forming the key-value cache _𝐾𝑉_ future ∈ R<sup>(</sup><sup>**T**−1)×(</sup><sup>**M**×</sup><sup>**N**+1)×</sup><sup>_𝐷𝑙_</sup> . The DLWM adopts a standard Transformer decoder incorporating Rotary Position Embedding, producing future world status predictions _𝑆_ future ∈ R<sup>(</sup><sup>**T**−1)×(</sup><sup>**M**×</sup><sup>**N**+1)×</sup><sup>_𝐷𝑙_</sup> . Formally, 


The ground truth _𝑆_ future<sup>GTis generated by a target encoder, which is a</sup> frozen copy of the SCWE updated via Exponential Moving Average (EMA) to provide stable supervision signals. 

_3.3.3_ **Teacher Forcing Attention Mask.** Given a Scene-Ego interleaved token sequence, the world model predicts each future token by attending to all historical tokens. We adopt teacher forcing during training: ground truth tokens serve as context for predicting subsequent tokens, preventing error accumulation across timesteps. 

Causal prediction is implemented via frame-wise attention masks, as shown in Fig. 3. Within each frame block, tokens attend bidirectionally to each other. Cross-frame, each token can only attend to tokens appearing earlier in the sequence, enforcing temporal causality. This frame-wise attention design enables parallel prediction of all future world status while maintaining causal consistency, significantly improving training speed and efficiency. 

_3.3.4_ **3D-RoPE** _._ Although _𝑆_ world contains world status representations across multiple timestamps and camera views, the query vectors _𝑄_ future and context features _𝐾𝑉_ future do not explicitly carry temporal or spatial position information. To enable the model to distinguish temporal and spatial relationships among tokens, we inject spatio-temporal position information into multi-head attention via 3D-RoPE, which differentiates tokens across timesteps, camera views, and positions within long sequences. 

In practice, we split the head dimension _𝐷ℎ_ into three parts to encode temporal coordinate _𝑡_ , camera index _𝑚_ , and token index _𝑛_ into _𝑄_ future and _𝐾𝑉_ future. We use absolute position indices to encode all three coordinates: temporal index with frequency 50, camera index with frequency 10, and token index with frequency 100. 

_3.3.5_ **Ego Status Supervision.** The world status representation _𝑆_ world contains both scene tokens and ego status embeddings. During world model prediction, ego status guides the evolution of scene representations as well as itself. Therefore, accurate prediction of ego status is crucial for modeling world dynamics. To provide precise guidance for the transition of world state, we introduce ego status supervision built upon the self-supervised future status prediction. We extract ego status embeddings _𝑆_ ego<sup>_𝑖_′from the predicted</sup> future world status _𝑆_ future, where _𝑖_<sup>′</sup> ∈{2 _, . . . ,𝑇_ }. These embeddings are then fed into three separate MLPs: a driving command decoder _𝐷_ cmd, a velocity decoder _𝐷𝑣_ , and an acceleration decoder _𝐷𝑎_ , producing predictions _𝐶_ pred ∈ R<sup>(</sup><sup>**T**−1)×4</sup> , _𝑉_ pred ∈ R<sup>(</sup><sup>**T**−1)×2</sup> , and _𝐴_ pred ∈ R<sup>(</sup><sup>**T**−1)×2</sup> , respectively. Formally: 


where _𝑆_ ego′<sup>∈R(</sup><sup>**T**−1)×</sup><sup>_𝐷𝑙_is the set containing all predicted future</sup> ego status embeddings _𝑆_ ego<sup>_𝑖_′with</sup><sup>_𝑖_′∈{2</sup><sup>_, . . . ,𝑇_}.</sup> 

## **3.4 Trajectory Planning** 

We employ a trajectory decoder _𝐷𝜏_ for planning, which generates trajectories corresponding to different driving intentions based on the control commands. A set of randomly initialized learnable trajectory queries _𝑄𝜏_<sup>_𝑡_∈R</sup><sup>_𝐾_×</sup><sup>_𝑛𝑝_×</sup><sup>_𝐷𝑙_is fed into the trajectory decoder</sup> along with the current world status representation _𝑆𝑤𝑜𝑟𝑙𝑑_<sup>_𝑡_of the</sup> driving scenario. After processing, the trajectory tokens are decoded via a lightweight MLP into _𝐾_ candidate trajectories. Finally, conditioned on the driving command _𝐶_<sup>_𝑡_</sup> at the current timestep _𝑡_ , the corresponding candidate trajectory is selected as the final trajectory _𝜏_ . Formally, 


Each decoded candidate trajectory _𝜏𝑖_ is a sequence of _𝑛𝑝_ poses spanning from the current timestep _𝑡_ to a future time _𝑡_ + _𝑇_ , where _𝑇_ represents the total prediction horizon. Each pose is represented as ( _𝑥,𝑦,𝜃_ ) ∈ R<sup>3</sup> , yielding complete trajectories in R<sup>_𝑛𝑝_×3</sup> , where _𝑥_ and _𝑦_ correspond to longitudinal and lateral displacements, respectively, with _𝜃_ denoting the heading angle. All quantities are referenced to the ego vehicle’s local coordinate system at timestep _𝑡_ . The time interval between consecutive predicted poses is assumed to be uniform. 

## **3.5 Training and Inference** 

**Training Objective.** Following prior work, we employ _𝐿_ 1 loss L _𝑡𝑟𝑎𝑗_ to optimize the generated multi-candidate trajectories by imitating expert trajectories. Geometric alignment computes cosine similarity loss L _𝑎𝑙𝑖𝑔𝑛_ on normalized features, maximizing cosine similarity to distill spatial understanding capability. For the world model, we use MSE loss L _𝑤𝑚_ to optimize the prediction of future world state. Future ego status requires supervision over driving command, velocity, and acceleration, including L _𝑐𝑚𝑑_ = CrossEntropy( _𝐶𝑝𝑟𝑒𝑑,𝐶𝑔𝑡_ ), L _𝑣_ = MSE( _𝑉𝑝𝑟𝑒𝑑,𝑉𝑔𝑡_ ) and L _𝑎_ = MSE ( _𝐴𝑝𝑟𝑒𝑑,𝐴𝑔𝑡_ ). The total loss for ego status is L _𝑒𝑔𝑜_ = L _𝑐𝑚𝑑_ + L _𝑣_ + L _𝑎_ . The final loss for end-to-end training is: 


**Inference.** During inference, the Dynamic Latent World Model is entirely bypassed—only the Spatial-Aware Compressive World Encoder and the Trajectory Decoder are required. Since the training objective already endows the scene representations with temporal dynamics and ego-awareness, no explicit future prediction is needed at test time. Inference reduces to a single forward pass through the encoder and decoder, without any auxiliary modules. 

## **4 Experiment** 

## **4.1 Implementation Details** 

_4.1.1_ **Architecture.** We adopt DINOv2-Base [27] as our vision encoder (86.6M parameters), which constitutes the foundation of the Spatial-Aware Compressive World Encoder (SCWE) and produces patch tokens of dimension _𝐷𝑒_ = 768. We employ _𝑁_ = 16 learnable scene queries with dimension _𝐷𝑒_ , projected to latent space _𝐷𝑙_ = 256 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 

**Table 1: Comparison with state-of-the-art methods on the NAVSIM v2 with extended metrics. We indicate the best and second best with bold and underlined respectively.** † **: The reported results are dependent on perception-based annotation.** 

|**Method**|**NC**↑|**DAC**↑|**DDC**↑|**TLC**↑|**EP**↑|**TTC**↑|**LK**↑|**HC**↑|**EC**↑|**EPDMS**↑|**Latency (s)**↓|
|---|---|---|---|---|---|---|---|---|---|---|---|
|_Perception-based Meth_|_ods_|||||||||||
|TransFuser [29]|96.9|89.9|97.8|99.7|87.1|95.4|92.7|**98.3**|87.2|76.7|0.02s|
|DriveSuprim [46]|97.5|96.5|99.4|99.6|88.4|96.6|95.5|**98.3**|77.0|83.1|—|
|ReCogDrive [42]|98.3|95.2|99.5|**99.8**|87.1|97.5|96.6|**98.3**|86.5|83.6|—|
|DiffusionDrive [23]|98.2|95.9|99.4|**99.8**|87.5|97.3|96.8|**98.3**|**87.7**|84.5|0.03s|
|WorldRFT[43]|97.8|96.5|99.5|**99.8**|88.5|97.0|97.4|98.1|69.1|86.7|0.29s|
|GoalFlow[41]<br>|98.4|98.2|99.5|**99.8**|88.1|97.4|96.7|98.1|57.9|87.3|—|
|Drive-JEPA<sup>† </sup>[36]|98.4|98.6|99.1|**99.8**|88.4|97.8|97.6|97.9|84.8|87.8|—|
|_Perception-free Metho_|_ds_|||||||||||
|World4Drive [53]|97.8|96.3|99.4|**99.8**|88.3|97.1|**97.7**|98.0|53.9|84.8|0.73s|
|Epona [47]|97.1|95.7|99.3|99.7|**88.6**|96.3|97.0|98.0|67.8|85.1|2.00s|
|DriveVLA-W0 [21]|**98.5**|**99.1**|98.0|99.7|86.4|**98.1**|93.2|97.9|58.9|86.1|—|
|Latent-WAM (Ours)|98.1|97.3|**99.6**|**99.8**|87.7|97.3|97.6|98.1|87.3|**89.3**|0.11s|


via an MLP. We set the temporal horizon to _𝑇_ = 4 frames and adopt three camera views—left, front, and right. Each view is resized to 224 × 448 before feeding into the World Encoder. Notably, the geometric foundation model we employ is WorldMirror [25], a feedforward model built upon VGGT [33]. The dimension of groundtruth geometric feature map is _𝐷𝑔_ = 2048. For the DLWM, we design a causal transformer decoder with 3D-RoPE for position embedding. The trajectory decoder follows a standard transformer architecture. Both DLWM and trajectory decoder comprise 4 layers with 8 attention heads, hidden dimension 256, and FFN dimension 1024. To provide ground truth world status representations for self-supervised training, we additionally introduce a frozen SCWE updated via Exponential Moving Average (EMA) with momentum 0.999, maintaining complete architectural symmetry with the online encoder. The model contains 104M parameters at inference time. During training, an additional EMA encoder is introduced for selfsupervised learning, bringing the total to 191M, of which only 104M are trainable. 

_4.1.2_ **Training Configuration.** Latent-WAM is trained on 32 A100 GPUs for 100 epochs with a total batch size of 512, taking about two days. We use AdamW with learning rate 2 × 10<sup>−4</sup> and weight decay 0.05, with linear warm-up over the first 10% steps followed by cosine annealing to 1 × 10<sup>−6</sup> . BF16 mixed-precision training is applied throughout. 

## **4.2 Benchmarks & Main Results** 

_4.2.1_ **NAVSIM** _._ NAVSIM [8] is a real-world dataset built upon OpenScene [6] and nuPlan [2], containing 103k training and 12k evaluation scenarios. NAVSIM v1 evaluates closed-loop planning via PDMS, which aggregates No at-fault Collisions (NC), Drivable Area Compliance (DAC), Time to Collision (TTC), Ego Progress (EP), and Comfort (C). NAVSIM v2 [3] extends PDMS to EPDMS by adding Driving Direction Compliance (DDC), Traffic Light Compliance (TLC), Lane Keeping (LK), and refining Comfort into History Comfort (HC) and Extended Comfort (EC). 

**Table 2: Photorealistic closed-loop evaluation on HUGSIM [54]. Zero-shot generalization using our model trained from NAVSIM-v2. Scores are per difficulty and overall average road completion (RC) and HD-Score, higher always better.** 

|**Mhd**|||**RC**↑||||**H**|**D-Sco**|**re**↑||
|---|---|---|---|---|---|---|---|---|---|---|
|**eto**|E|M|H|X|**Avg**.|E|M|H|X|**Avg**.|
|UniAD[14]|58.6|41.2|40.4|26.0|40.6|48.7|29.5|27.3|14.3|**28.9**|
|VAD[16]|38.7|27.0|25.5|23.0|27.9|24.3|9.9|10.4|8.2|12.3|
|LTF[5]|68.4|40.7|36.9|25.5|41.4|52.8|24.6|19.8|8.1|24.8|
|GTRS-Dense[22]|64.2|50.0|20.7|22.3|38.0|55.5|39.0|11.7|14.3|28.6|
|Latent-WAM|84.2|42.5|30.6|35.5|**45.9**|72.5|24.0|12.2|18.1|**28.9**|


_E: Easy, M: Medium, H: Hard, X: Extreme_ 

On NAVSIM v2 (Table 1), Latent-WAM achieves the highest EPDMS among all methods, including those using perception annotations, and ranks top in DDC, TLC, and LK. Compared to DriveJEPA [36], which relies on perception annotations, our perceptionfree approach is slightly behind on safety metrics but substantially better on EC. 

_4.2.2_ **HUGSIM** _._ For closed-loop evaluation, we employ HUGSIM [54], which reconstructs scenarios from KITTI-360 [24], nuScenes [1], PandaSet [40], and Waymo [30] as photorealistic 3D environments, where the planner controls the ego vehicle via RGB cameras with dynamically adjusted viewpoints. On its pre-challenge test set (436 scenarios, four difficulty levels), we adopt the zero-shot protocol and report Road Completion (RC) and HUGSIM Driving Score (HDScore), with HD-Score combining RC and averaged NC, DAC, TTC, and comfort. Latent-WAM, trained only on NAVSIM without finetuning, achieves 45.9 RC and 28.9 HD-Score, ranking first in RC and matching the best HD-Score among all baselines. 

_4.2.3_ **Inference Latency** _._ As illustrated in Table 1, we report the inference latency of each method on an A100. Our Latent-WAM has a total latency of 107 ms, meeting the requirements for real-time deployment. 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 

**Table 3: Ablation study of each proposed component. + and - denote improvement/degradation relative to the baseline.** 

|**Scene Repre**|**sentation**|**Dynamic Worl**|**d Modeling**||
|---|---|---|---|---|
|||||**EPDMS**↑|
|Compression|Geometry|World Model|Ego Status||
|�|�|�|�|87.9|
|�|�|�|�|87.7−0_._2|
|�|�|�|�|88.0+0_._1|
|�|�|�|�|88.3+0_._4|
|�|�|�|�|88.6+0_._7|
|�<br>|�<br>|�<br>|�<br>|89.0+1_._1|
|�|�|�|�|**89.3**+1_._4|


**Table 4: Ablation study on geometry injection method** 

|**Geometric Information**|**EPDMS**↑|
|---|---|
|w/o Geometric feature|88.3|
|Concatenation|88.0|
|Distillation|**89.3**|


## **4.3 Ablation Study** 

_4.3.1_ **Effectiveness of Each Component.** We conduct progressive ablation experiments by gradually adding modules to the baseline, as shown in Table 3. 

**Scene Representation.** The baseline directly feeds image patch tokens to the trajectory decoder, achieving 87.9 EPDMS. To enable long-horizon prediction in the world model, we compress image patches into compact scene tokens, incurring only a negligible performance drop (↓ 0 _._ 2). Injecting geometric information boosts performance to 88.6, demonstrating that geometric perception is crucial for accurate trajectory planning. 

**Dynamic World Modeling.** Building upon compressed scene tokens, the DLWM improves performance from 87.7 to 88.0 by capturing future dynamics. Adding ego status further increases the score to 88.3, indicating that self-state awareness benefits planning. With geometric information, the world model further reaches 89.0. The full model combining all components achieves 89.3, showing that all modules contribute synergistically. 

_4.3.2_ **Impact of Geometric Information.** We compare geometric information integration approaches in Table 4. Without geometry, the full model achieves 88.3 EPDMS. Directly concatenating frozen geometry features as key-value inputs degrades performance to 88.0, likely due to misalignment with the planning objective. In contrast, distilling geometric knowledge into the vision backbone improves EPDMS to 89.3, as end-to-end fine-tuning learns spatial-aware representations inherently aligned with downstream planning. 

_4.3.3_ **Vision Backbone for Geometric Distillation.** We compare different backbone scales and fine-tuning strategies for geometric distillation, as shown in Table 5. 

**Backbone Scale.** DINO-Small achieves 86.3 EPDMS but remains suboptimal due to insufficient parameter capacity for highdimensional geometric features. DINO-Base with full fine-tuning achieves the best performance (89.3), indicating that sufficient backbone capacity is essential for effective distillation. 

**Table 5: Ablation study on vision backbone** 

|Dino Backbone|**EPDMS**↑|
|---|---|
|Small|86.3|
|Base|**89.3**|
|Small-LoRA|84.7|
|Base-LoRA|68.5|


**Table 6: Ablation study on world model prediction stride** 

|**Prediction Temporal Stride**|**EPDMS**↑|
|---|---|
|0→8|88.4|
|−3→0→4→8|**89.3**|
|−3→−2→−1→0→2→4→6→8|89.1|


**Training Strategy.** Parameter-efficient fine-tuning via LoRA leads to severe degradation and unstable training for both DINOSmall-LoRA (84.7) and DINO-Base-LoRA (68.5). LoRA’s low-rank constraints are inadequate for distilling high-dimensional geometric features, which require full parameter updates to capture geometric awareness. Notably, DINO-Base-LoRA degrades more severely than DINO-Small-LoRA, as the larger model has more parameters frozen under LoRA, amplifying the mismatch between the low-rank update subspace and the high-dimensional distillation target. 

In summary, effective geometric distillation requires both sufficient model capacity and full fine-tuning flexibility. 

_4.3.4_ **World Model Prediction Temporal Stride.** We investigate the effect of prediction temporal stride in the DLWM (Table 6). Predicting only the final frame (0 → 8) achieves 88.4 EPDMS. Incorporating historical and intermediate future predictions with stride 4 (−3 → 0 → 4 → 8) improves performance to 89.3, as multi-step prediction provides richer supervision. Further densifying to stride 2 (−3 →−2 →−1 → 0 → 2 → 4 → 6 → 8) yields 89.1, providing no additional gain. Since all configurations predict to the same horizon, denser sampling does not extend temporal reasoning; adjacent frames are highly similar and offer limited new signal, while more prediction targets increase optimization burden and computational cost. Thus, moderate prediction density best balances supervision effectiveness and training efficiency. 

## **4.4 Qualitative Analysis.** 

We qualitatively evaluate Latent-WAM on NAVSIM, focusing on the spatial understanding of the World Encoder. 

**Spatial Understanding.** To investigate how geometric distillation enhances spatial understanding, we visualize attention maps between scene tokens and image patches (Fig. 4). Compared to the baseline without geometric distillation, our model exhibits much more focused attention, concentrating on lane markings, scene structures, and drivable areas critical for trajectory planning; the baseline distributes attention broadly across irrelevant background regions, suggesting that without geometric supervision, compressed scene tokens encode noisy information that interferes with planning. 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 


**Figure 4: Visualization of attention maps between scene tokens and image patches, comparing our SCWE (with geometric distillation) against a baseline (without distillation). Our model exhibits three key properties: (1) More focused attention distributions that concentrate on lane markings and drivable areas rather than irrelevant backgrounds; (2) Stronger alignment with geometric structure, producing compact patterns that tightly follow lane boundaries and obstacle contours; (3) Intent-aware attention that dynamically shifts focus toward regions along the intended driving direction.** 


**Figure 5: Visualization of planning trajectories. Green: human expert demonstration. Yellow: predicted trajectory of the corresponding method.** 

Our attention maps also align more strongly with geometric structure: the baseline shows loose, diffuse regions, while our World Encoder produces compact patterns that tightly follow boundaries such as lane markings and open spaces near obstacles. Under different driving intentions—going straight, turning right, and turning left—attention strongly correlates with the intended direction, with minimal attention given to regions deviating from the planned trajectory. This intent-aware behavior demonstrates that our World Encoder selectively focuses on task-relevant spatial information conditioned on the driving context. 

and maintains safer distances from vehicles, unlike Epona [47] and World4Drive [53], which yield sub-optimal paths. 

## **5 Conclusion** 

In this paper, we presented Latent-WAM, an end-to-end autonomous driving framework that builds compact, planning-relevant world representations using a Spatial-Aware Compressive World Encoder to distill geometry while compressing multi-view images into compact scene tokens, and a Dynamic Latent World Model that autoregressively predicts future world states during training to equip the encoder with dynamic scene understanding. DLWM is discarded at inference, yet its prediction objective substantially improves planning performance, indicating that the value of latent world modeling lies in representation learning rather than explicit future prediction. At inference, only SCWE and a lightweight trajectory decoder are needed, yielding a compact 104M-parameter model that runs in a single forward pass. Latent-WAM achieves state-ofthe-art results on NAVSIM v2 (89.3 EPDMS) and HUGSIM (45.9 RC and 28.9 HD-Score in zero-shot evaluation), outperforming the best prior perception-free method by 3.2 EPDMS with significantly less training data and fewer parameters. Qualitative analysis reveals focused, geometry-aligned attention patterns, validating the effectiveness of combining spatial-aware compression with dynamic world modeling. 

**Trajectory Comparison.** Fig. 5 compares trajectory predictions across methods. Our method better matches human trajectories 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 

## **References** 

- [1] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. 2020. nuscenes: A multimodal dataset for autonomous driving. In _2020 IEEE/CVF conference on computer vision and pattern recognition (CVPR)_ . IEEE, 11618–11628. 

- [2] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. 2021. nuplan: A closedloop ml-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ (2021). 

- [3] Wei Cao, Marcel Hallgarten, Tianyu Li, Daniel Dauner, Xunjiang Gu, Caojun Wang, Yakov Miron, Marco Aiello, Hongyang Li, Igor Gilitschenski, et al. 2025. Pseudo-simulation for autonomous driving. _arXiv preprint arXiv:2506.04218_ (2025). 

- [4] Shaoyu Chen, Bo Jiang, Hao Gao, Bencheng Liao, Qing Xu, Qian Zhang, Chang Huang, Wenyu Liu, and Xinggang Wang. 2024. Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. _arXiv preprint arXiv:2402.13243_ (2024). 

- [5] Kashyap Chitta, Aditya Prakash, Bernhard Jaeger, Zehao Yu, Katrin Renz, and Andreas Geiger. 2022. Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. _TPAMI_ (2022). 

- [6] OpenScene Contributors. 2023. Openscene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving. In _Proceedings of the Conference on Computer Vision and Pattern Recognition, Vancouver, Canada_ . 18–22. 

- [7] Chenxu Dang, Haiyan Liu, Jason Bao, Pei An, Xinyue Tang, An Pan, Jie Ma, Bingchuan Sun, and Yan Wang. 2026. Sparseworld: A flexible, adaptive, and efficient 4d occupancy world model powered by sparse and dynamic queries. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 40. 3497–3505. 

- [8] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. 2024. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. _Advances in Neural Information Processing Systems_ 37 (2024), 28706–28719. 

- [9] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. 2024. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems_ 37 (2024), 91560–91596. 

- [10] Yinfeng Gao, Deqing Liu, Yupeng Zheng, Qichao Zhang, Da-Wei Ding, and Dongbin Zhao. 2026. SoAD: Safety-Oriented Value Estimation for Enhanced Closed-Loop End-to-End Autonomous Driving. _IEEE Transactions on Systems, Man, and Cybernetics: Systems_ 56, 9 (2026), 4942–4955. 

- [11] Jiazhe Guo, Yikang Ding, Xiwu Chen, Shuo Chen, Bohan Li, Yingshuang Zou, Xiaoyang Lyu, Feiyang Tan, Xiaojuan Qi, Zhiheng Li, et al. 2025. Dist-4d: Disentangled spatiotemporal diffusion with metric depth for 4d driving scene generation. In _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 27231–27241. 

- [12] Deepti Hegde, Rajeev Yasarla, Hong Cai, Shizhong Han, Apratim Bhattacharyya, Shweta Mahajan, Litian Liu, Risheek Garrepalli, Vishal M Patel, and Fatih Porikli. 2025. Distilling multi-modal large language models for autonomous driving. In _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 27575–27585. 

- [13] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. 2023. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ (2023). 

- [14] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. 2023. Planning-oriented autonomous driving. In _2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 17853–17862. 

- [15] Xiaosong Jia, Junqi You, Zhiyuan Zhang, and Junchi Yan. 2025. Drivetransformer: Unified transformer for scalable end-to-end autonomous driving. In _International Conference on Learning Representations_ , Vol. 2025. 67227–67243. 

- [16] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. 2023. Vad: Vectorized scene representation for efficient autonomous driving. In _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 8306–8316. 

- [17] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. 2025. Uniscene: Unified occupancy-centric driving scene generation. In _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 11971–11981. 

- [18] Bohan Li, Xin Jin, Hu Zhu, Hongsi Liu, Ruikai Li, Jiazhe Guo, Kaiwen Cai, Chao Ma, Yueming Jin, Hao Zhao, et al. 2026. Scaling up occupancy-centric driving scene generation: Dataset and method. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ (2026). 

- [19] Bohan Li, Zhuang Ma, Dalong Du, Baorui Peng, Zhujin Liang, Zhenqiang Liu, Chao Ma, Yueming Jin, Hao Zhao, Wenjun Zeng, et al. 2025. OmniNWM: Omniscient Driving Navigation World Models. _arXiv preprint arXiv:2510.18313_ (2025). 

- [20] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. 2025. Enhancing end-to-end autonomous driving with latent world 

model. In _International Conference on Learning Representations(ICLR)_ , Vol. 2025. 42942–42959. 

- [21] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. 2026. Drivevla-w0: World models amplify data scaling law in autonomous driving. In _International Conference on Learning Representations_ , Vol. 2026. 7890–7911. 

- [22] Zhenxin Li, Wenhao Yao, Zi Wang, Xinglong Sun, Joshua Chen, Nadine Chang, Maying Shen, Zuxuan Wu, Shiyi Lan, and Jose M Alvarez. 2025. Generalized Trajectory Scoring for End-to-end Multimodal Planning. _arXiv preprint arXiv:2506.06664_ (2025). 

- [23] Bencheng Liao, Shaoyu Chen, Haoran Yin, Bo Jiang, Cheng Wang, Sixu Yan, Xinbang Zhang, Xiangyu Li, Ying Zhang, Qian Zhang, et al. 2025. Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ . 12037–12047. 

- [24] Yiyi Liao, Jun Xie, and Andreas Geiger. 2022. Kitti-360: A novel dataset and benchmarks for urban scene understanding in 2d and 3d. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ 45, 3 (2022), 3292–3310. 

- [25] Yifan Liu, Zhiyuan Min, Zhenwei Wang, Junta Wu, Tengfei Wang, Yixuan Yuan, Yawei Luo, and Chunchao Guo. 2025. Worldmirror: Universal 3d world reconstruction with any-prior prompting. _arXiv preprint arXiv:2510.10726_ (2025). 

- [26] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. 2024. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 15522– 15533. 

- [27] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, et al. 2023. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ (2023). 

- [28] Chenbin Pan, Burhaneddin Yaman, Tommaso Nesti, Abhirup Mallik, Alessandro G Allievi, Senem Velipasalar, and Liu Ren. 2024. Vlp: Vision language planning for autonomous driving. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 14760–14769. 

- [29] Aditya Prakash, Kashyap Chitta, and Andreas Geiger. 2021. Multi-modal fusion transformer for end-to-end autonomous driving. In _CVPR_ . 

- [30] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. 2020. Scalability in perception for autonomous driving: Waymo open dataset. In _2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 2443–2451. 

- [31] Wenchao Sun, Xuewu Lin, Yining Shi, Chuang Zhang, Haoran Wu, and Sifa Zheng. 2025. Sparsedrive: End-to-end autonomous driving via sparse scene representation. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 8795–8801. 

- [32] Ran Tian, Boyi Li, Xinshuo Weng, Yuxiao Chen, Edward Schmerling, Yue Wang, Boris Ivanovic, and Marco Pavone. 2024. Tokenize the world into object-level knowledge to address long-tail events in autonomous driving. _arXiv preprint arXiv:2407.00959_ (2024). 

- [33] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. 2025. Vggt: Visual geometry grounded transformer. In _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 5294–5306. 

- [34] Junli Wang, Zhihua Hua, Xueyi Liu, Zebin Xing, Haochen Tian, Kun Ma, Hangjun Ye, Guang Chen, Long Chen, and Qichao Zhang. 2026. Beyond imitation: Learning safe end-to-end autonomous driving from hard negatives. In _European Conference on Computer Vision (ECCV)_ . 

- [35] Junli Wang, Yinan Zheng, Xueyi Liu, Zebin Xing, Pengfei Li, Kun Ma, Hangjun Ye, Guang Chen, Guang Li, Long Chen, Zhongpu Xia, and Qichao Zhang. 2026. MeanFuser: Fast One-Step Multi-Modal Trajectory Generation and Adaptive Reconstruction via MeanFlow for End-to-End Autonomous Driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . 17884–17893. 

- [36] Linhan Wang, Zichong Yang, Chen Bai, Guoxiang Zhang, Xiaotong Liu, Xiaoyin Zheng, Xiao-Xiao Long, Chang-Tien Lu, and Cheng Lu. 2026. Drive-jepa: Video jepa meets multimodal trajectory distillation for end-to-end driving. _arXiv preprint arXiv:2601.22032_ (2026). 

- [37] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. 2024. Drivedreamer: Towards real-world-drive world models for autonomous driving. In _European conference on computer vision_ . Springer, 55–72. 

- [38] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. 2024. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 14749–14759. 

- [39] Tianze Xia, Yongkang Li, Lijun Zhou, Jingfeng Yao, Kaixin Xiong, Haiyang Sun, Bing Wang, Kun Ma, Hangjun Ye, Wenyu Liu, et al. 2025. DriveLaW: Unifying Planning and Video Generation in a Latent Driving World. _arXiv preprint arXiv:2512.23421_ (2025). 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 

- [40] Pengchuan Xiao, Zhenlei Shao, Steven Hao, Zishuo Zhang, Xiaolin Chai, Judy Jiao, Zesong Li, Jian Wu, Kai Sun, Kun Jiang, et al. 2021. Pandaset: Advanced sensor suite dataset for autonomous driving. In _2021 IEEE international intelligent transportation systems conference (ITSC)_ . IEEE, 3095–3101. 

- [41] Zebin Xing, Xingyu Zhang, Yang Hu, Bo Jiang, Tong He, Qian Zhang, Xiaoxiao Long, and Wei Yin. 2025. Goalflow: Goal-driven flow matching for multimodal trajectories generation in end-to-end autonomous driving. In _2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 1602–1611. 

- [42] Kaixin Xiong, Xiangyu Guo, Fang Li, Sixu Yan, Gangwei Xu, Lijun Zhou, Long Chen, Haiyang Sun, Bing Wang, Kun Ma, et al. 2026. Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. In _International Conference on Learning Representations_ , Vol. 2026. 157518–157556. 

- [43] Pengxuan Yang, Ben Lu, Zhongpu Xia, Chao Han, Yinfeng Gao, Teng Zhang, Kun Zhan, XianPeng Lang, Yupeng Zheng, and Qichao Zhang. 2026. Worldrft: Latent world model planning with reinforcement fine-tuning for autonomous driving. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 40. 11649–11657. 

- [44] Pengxuan Yang, Yupeng Zheng, Deheng Qian, Zebin Xing, Qichao Zhang, Linbo Wang, Yichen Zhang, Shaoyu Guo, Zhongpu Xia, Qiang Chen, et al. 2026. Dreamerad: Efficient reinforcement learning via latent world model for autonomous driving. In _European Conference on Computer Vision (ECCV)_ . 

- [45] Xuemeng Yang, Licheng Wen, Tiantian Wei, Yukai Ma, Jianbiao Mei, Xin Li, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, et al. 2025. Drivearena: A closedloop generative simulation platform for autonomous driving. In _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 26933–26943. 

- [46] Wenhao Yao, Zhenxin Li, Shiyi Lan, Zi Wang, Xinglong Sun, Jose M Alvarez, and Zuxuan Wu. 2026. Drivesuprim: Towards precise trajectory selection for endto-end planning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 40. 11910–11918. 

- [47] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, et al. 2025. Epona: Autoregressive diffusion world model for autonomous driving. In _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 27220–27230. 

- [48] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. 2024. Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion. In _International Conference on Learning Representations_ , Vol. 2024. 7269–7299. 

- [49] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. 2025. Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 39. 10412–10420. 

- [50] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. 2024. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European Conference on Computer Vision_ . Springer, 55–72. 

- [51] Yupeng Zheng, Zebin Xing, Qichao Zhang, Bu Jin, Pengfei Li, Yuhang Zheng, Zhongpu Xia, Yaran Chen, and Dongbin Zhao. 2026. PlanAgent: A Multi-modal Large Language Agent for Closed-loop Vehicle Motion Planning. _IEEE Transactions on Cognitive and Developmental Systems_ (2026), 1–14. doi:10.1109/TCDS. 2026.3664120 

- [52] Yupeng Zheng, Pengxuan Yang, Zhongpu Xia, Qichao Zhang, Yuhang Zheng, Songen Gu, Bu Jin, Teng Zhang, Ben Lu, Chao Han, et al. 2026. Data scaling laws for imitation learning-based end-to-end autonomous driving. In _2026 IEEE International Conference on Robotics and Automation (ICRA)_ . 

- [53] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, et al. 2025. World4drive: End-to-end autonomous driving via intention-aware physical latent world model. In _2025 IEEE/CVF International Conference on Computer Vision (ICCV)_ . IEEE, 28632–28642. 

- [54] Hongyu Zhou, Longzhong Lin, Jiabao Wang, Yichong Lu, Dongfeng Bai, Bingbing Liu, Yue Wang, Andreas Geiger, and Yiyi Liao. 2025. Hugsim: A real-time, photorealistic and closed-loop simulator for autonomous driving. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ (2025). 

- [55] Vlas Zyrianov, Henry Che, Zhijian Liu, and Shenlong Wang. 2025. Lidardm: Generative lidar simulation in a generated world. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 6055–6062. 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 

## **Supplementary Material** 

## **A Metrics** 

## **A.1 NAVSIM** 

NAVSIM v2 [3] extends the PDMS metric from NAVSIM v1 [8] to the Extended PDMS (EPDMS): 


where NC, DAC, DDC, TLC, EP, TTC, LK, HC, and EC denote No at-fault Collision, Drivable Area Compliance, Driving Direction Compliance, Traffic Light Compliance, Ego Progress, Time to Collision, Lane Keeping, History Comfort, and Extended Comfort, respectively. Among these, DDC, TLC, LK, HC, and EC are newly introduced in NAVSIM v2. 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

( _𝑊_ orig _, 𝐻_ orig) to ( _𝑊_ resize _, 𝐻_ resize), the scale factors are computed as: 


For center cropping to ( _𝑊_ crop _, 𝐻_ crop), the crop offsets are: 


The adjusted intrinsic parameters are then: 

_𝑓𝑥_<sup>′=</sup><sup>_𝑓𝑥_·</sup><sup>_𝑠𝑥,_</sup> _𝑓𝑦_<sup>′=</sup><sup>_𝑓𝑦_·</sup><sup>_𝑠𝑦,_</sup> _𝑐𝑥_<sup>′=</sup><sup>_𝑐𝑥_·</sup><sup>_𝑠𝑥_−Δ</sup><sup>_𝑥,_</sup> _𝑐𝑦_<sup>′=</sup><sup>_𝑐𝑦_·</sup><sup>_𝑠𝑦_−Δ</sup><sup>_𝑦,_(13)</sup> yielding the adjusted intrinsic matrix K<sup>′</sup> : 


## **B.3 Camera Extrinsic Transformation** 

## **A.2 HUGSIM** 

The HUGSIM [54] Driving Score (HD-Score) at timestamp _𝑡_ is computed as the product of driving policy items and a weighted average of contributory items: 


where NC, DAC, TTC, and COM denote No at-fault Collision, Drivable Area Compliance, Time to Collision, and Ego Comfort, respectively. These metrics follow the same definitions as used in NAVSIM v1. 

The final HD-Score averages per-frame scores across all timestamps and scales by the route completion score _𝑅𝑐_ ∈[0 _,_ 1]: 


Notably, NC and TTC account for collisions with static background entities (e.g., buildings, fences, vegetation) using semantic segmentation. 

## **B Data Processing Pipeline** 

## **B.1 Image Preprocessing** 

We utilize three camera views (left, front, right) as input. Each image undergoes a two-stage preprocessing pipeline: resizing followed by center cropping. Specifically, the original 1920 × 1080 images are first resized to 455 × 256, then center-cropped to the final resolution of 448 × 224, yielding an aspect ratio of 2:1. 

## **B.2 Camera Intrinsic Adjustment** 

When applying geometric feature extraction to images, the camera intrinsic matrix must be adjusted accordingly to maintain geometric consistency. Given the original intrinsic matrix K: 


where _𝑓𝑥_ and _𝑓𝑦_ denote the focal lengths along the _𝑥_ and _𝑦_ axes, and ( _𝑐𝑥,𝑐𝑦_ ) represents the principal point. After resizing from 

The camera extrinsic matrix represents the transformation from camera coordinates to world (LiDAR) coordinates. We construct the camera-to-world matrix T _𝑐_ → _𝑤_ ∈ R<sup>4×4</sup> as: 


where R _𝑐_ → _𝑤_ ∈ R<sup>3×3</sup> is the rotation matrix and t _𝑐_ → _𝑤_ ∈ R<sup>3</sup> is the translation vector. The world-to-camera matrix T _𝑤_ → _𝑐_ used for 3Dto-2D projection is obtained by matrix inversion: 


## **B.4 Geometric Feature Extraction** 

Following the geometric alignment formulation in the Method section, we extract patch-level geometric features _𝑓𝑔_ ( _𝐼_ ) ∈ R<sup>_𝑇_×</sup><sup>_𝑀_×</sup><sup>_𝑆_×</sup><sup>_𝐷𝑔_</sup> from multi-view images using the frozen geometric foundation model WorldMirror [25] as _𝑓𝑔_ , where _𝑇_ denotes the number of temporal frames, _𝑀_ denotes the number of camera views, _𝑆_ denotes the number of patch tokens per view, and _𝐷𝑔_ = 2048 denotes the geometric feature dimension. 

**Camera Prior Extraction.** Given multi-view images I ∈ R<sup>_𝑀_×3×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> along with their camera intrinsics K ∈ R<sup>_𝑀_×3×3</sup> and extrinsics T ∈ R<sup>_𝑀_×4×4</sup> , the geometric foundation model first encodes these inputs into spatial-geometric priors P that encapsulate camera poses, depth estimates, and intrinsic parameters: 


**Geometric Feature Encoding.** The visual geometry transformer then processes the images conditioned on these priors. Following the model’s conditional design, we utilize camera pose and intrinsic information (indicated by condition flags c = [1 _,_ 0 _,_ 1] for camera pose, depth, and intrinsics respectively) while excluding depth supervision: 


Since _𝑓𝑔_ remains frozen throughout training, we pre-compute and offline-cache _𝑓𝑔_ ( _𝐼_ ) for all training samples, enabling direct loading during training without repeated inference costs. This design substantially reduces training time and GPU memory overhead. 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 


**Figure 6: Additional trajectory visualizations on NAVSIM. Green: human driving trajectory. Yellow: predicted trajectory from the corresponding method.** 

## **C Inference Latency** 

We measured the inference latency per module of Latent-WAM on a single A100 GPU for a single batch. The inference latency of each module is shown in Table 7. Latency was evaluated after three warm-up iterations, with the final number averaged over 10 forward passes. 

**Table 7: Per-module inference latency of Latent-WAM** 

|**Module**|**Parameters**|**Latency**|
|---|---|---|
|World Encoder|86.6M|100ms|
|Trajectory Decoder|8.4M|6ms|
|All modules|104M|107ms|


## **D More Visualization** 

We provide additional qualitative results to complement the quantitative analysis. 

## **D.2 Attention Map Visualization** 

Figs. 7–10 present additional attention map visualizations between scene tokens and image patches across consecutive frames, covering four driving scenarios: going-forward (Fig. 7), lane-changing (Fig. 8), right-turning (Fig. 9), and left-turning (Fig. 10). Consistent with the observations in the main paper, our model with geometric distillation yields more focused attention on task-relevant regions such as lane markings and drivable areas, while the baseline without distillation produces scattered attention over irrelevant backgrounds. Furthermore, the attention distribution is strongly correlated with the driving intent across all scenarios, confirming that our SCWE learns to selectively focus on spatial information conditioned on the driving context. 

## **D.3 HUGSIM Benchmark Visualization** 

Figs. 11–15 present trajectory planning visualizations on the HUGSIM benchmark across four datasets: nuScenes [1] (Fig. 11), KITTI360 [24] (Figs. 12 and 13), Waymo [30] (Fig. 14), and PandaSet [40] (Fig. 15). Despite being trained exclusively on NAVSIM without any fine-tuning, Latent-WAM demonstrates strong zero-shot generalization capability, producing reasonable and safe trajectories across diverse driving environments reconstructed from different real-world datasets. 

## **D.1 Trajectory Planning** 

Fig. 6 presents additional trajectory planning comparisons on NAVSIM across diverse driving scenarios. The green line denotes the human expert trajectory and the yellow line represents the predicted trajectory. Compared to Epona [47] and World4Drive [53], LatentWAM consistently produces trajectories that more closely follow the expert demonstration while maintaining safer distances from surrounding vehicles, demonstrating the robustness of our approach across different traffic conditions. 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 


**Figure 7: Visualization of attention maps between scene tokens and image patches across consecutive frames. All groups depict going-forward scenarios. Geometric distillation yields more focused attention on task-relevant regions.** 


**Figure 8: Visualization of attention maps between scene tokens and image patches across consecutive frames. All groups depict lane-changing scenarios. Geometric distillation yields more focused attention on task-relevant regions.** 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 


**Figure 9: Visualization of attention maps between scene tokens and image patches across consecutive frames. All groups depict turn-right scenarios. Geometric distillation yields more focused attention on task-relevant regions.** 


**Figure 10: Visualization of attention maps between scene tokens and image patches across consecutive frames. All groups depict turn-left scenarios. Geometric distillation yields more focused attention on task-relevant regions.** 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 


**Figure 11: Visualization of trajectory planning on HUGSIM benchmark(nuScenes [1])** 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 


**Figure 12: Visualization of trajectory planning on HUGSIM benchmark(KITTI-360 [24])** 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 


**Figure 13: Visualization of trajectory planning on HUGSIM benchmark(KITTI-360)** 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Linbo Wang et al. 


**Figure 14: Visualization of trajectory planning on HUGSIM benchmark(Waymo [30])** 

MM ’26, November 10–14, 2026, Rio de Janeiro, Brazil 

Latent-WAM: Latent World Action Modeling for End-to-End Autonomous Driving 


**Figure 15: Visualization of trajectory planning on HUGSIM benchmark(PandaSet [40])** 

