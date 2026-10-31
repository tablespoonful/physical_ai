---
title: "FASTopoWM: Fast-Slow Lane Segment Topology Reasoning with Latent World Models"
date: "2025-07-31"
authors: "Yiming Yang; Hongbin Lin; Yueru Luo; Suzhong Fu; Chao Zheng; Xinrui Yan"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2507.23325
pdf: https://arxiv.org/pdf/2507.23325
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.23325)** / [論文ページ](https://arxiv.org/abs/2507.23325)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint, Under review. 

# FASTOPOWM: FAST-SLOW LANE SEGMENT TOPOLOGY REASONING WITH LATENT WORLD MODELS 

**Yiming Yang**<sup>**1,2**</sup> **, Hongbin Lin**<sup>**1,2**</sup> **, Yueru Luo**<sup>**1,2**</sup> **, Suzhong Fu**<sup>**1,2**</sup> **, Chao Zheng**<sup>**3**</sup> 

**Xinrui Yan**<sup>**3**</sup> **, Shuqi Mei**<sup>**3**</sup> **, Kun Tang**<sup>**3**</sup> **, Shuguang Cui**<sup>**2,1**</sup> **, Zhen Li**<sup>**2,1**</sup><sup>_∗_</sup> 

1 FNii, CUHK-Shenzhen 2 SSE, CUHK-Shenzhen 3 T Lab, Tencent 

_{_ yimingyang@link., shuguangcui, lizhen _}_ @cuhk.edu.cn 

## ABSTRACT 

Lane segment topology reasoning provides comprehensive bird’s-eye view (BEV) road scene understanding, which can serve as a key perception module in planning-oriented end-to-end autonomous driving systems. Existing lane topology reasoning methods often fall short in effectively leveraging temporal information to enhance detection and reasoning performance. Recently, stream-based temporal propagation method has demonstrated promising results by incorporating temporal cues at both the query and BEV levels. However, it remains limited by over-reliance on historical queries, vulnerability to pose estimation failures, and insufficient temporal propagation. To overcome these limitations, we propose FASTopoWM, a novel fast-slow lane segment topology reasoning framework augmented with latent world models. To reduce the impact of pose estimation failures, this unified framework enables parallel supervision of both historical and newly initialized queries, facilitating mutual reinforcement between the fast and slow systems. Furthermore, we introduce latent query and BEV world models conditioned on the action latent to propagate the state representations from past observations to the current timestep. This design substantially improves the performance of temporal perception within the slow pipeline. Extensive experiments on the OpenLane-V2 benchmark demonstrate that FASTopoWM outperforms state-of-the-art methods in both lane segment detection (37.4% v.s. 33.6% on mAP) and centerline perception (46.3% v.s. 41.5% on OLS). Code is accessible at https://github.com/YimingYang23/FASTopoWM. 

## 1 INTRODUCTION 

Lane segment topology reasoning predicts lane segments (including centerlines and boundary lines) along with their topological relationships to construct a comprehensive road network (Wang et al., 2024a; Li et al., 2023b). This capability can be integrated into planning-oriented end-to-end autonomous driving systems, serving as the perception module to provide bird’s-eye view (BEV) road scene understanding (Hu et al., 2023b; Jiang et al., 2023; Zhou et al., 2025). 

Most existing approaches (Liao et al., 2022; Fu et al., 2025a) focus on single-frame detection, failing to exploit the temporal consistency of predictions across consecutive frames. This limitation leads to inconsistent topology and position of lane segments in the global coordinate system. To overcome these issues, stream-based temporal propagation methods (Yuan et al., 2024) have proven effective in enhancing temporal consistency in perception. They reuse high-confidence historical queries and BEV features as anchors for current detection. Inspired by this observation, we introduce the streambased approach in this work to predict lane segment topology with temporal consistency. However, as illustrated in Fig. 1, current stream-based frameworks suffer from three critical limitations: **(1) Over-reliance on historical queries.** The historical queries demonstrate higher confidence levels, 

> _∗_ � Corresponding author. 

1 

Preprint, Under review. 

they are more likely to approximate the GT positions compared to the newly initialized queries. As a result, during Hungarian matching supervision, historical queries are prioritized while newly initialized queries are often neglected. However, in the first frame of a scene, only the newly initialized queries are available for lane segment detection. If their performance is suboptimal, errors may propagate and accumulate across subsequent frames. **(2) Vulnerability to pose estimation failures.** To align historical queries and BEV features with the current frame, stream-based approaches rely on continuous pose estimation between adjacent frames. However, when vehicles enter tunnels or remote areas where GPS signals are unavailable, or when IMU error accumulation prevents pose refinement, the system degrades to single-frame detection mode. This degradation leads to significant performance deterioration and may ultimately cause complete system failure. **(3) Weak temporal propagation.** When historical BEV features are warped, the details of the features at the edges of the BEV tend to be lost. Moreover, simply applying pose transformation to historical queries through a basic MLP architecture fails to achieve optimal performance. 

To address the aforementioned issues, we propose a novel **<u>fa</u>** <u>st-</u> **<u>s</u>** <u>low</u> lane segment **topo** logy reasoning framework with latent **<u>w</u>** <u>orld</u> **<u>m</u>** <u>odels</u> ( **FASTopoWM** ). Inspired by recent vision-language models (VLMs) (Zhang et al., 2025; Xiao et al., 2025), we decouple our network into dual pathways: a slow pipeline and a fast pipeline. The slow pipeline leverages temporal information to address challenging perception scenarios and improve detection performance, while the fast pipeline performs single-frame perception to ensure the basic functionality of the system. These two systems can perform inference in parallel or operate independently. A key innovation lies in the unified framework between the fast and slow systems that allowing parallel supervision of both historical and 


**Figure 1: Pipeline Comparison.** Existing stream-based methods suffer significant performance degradation when pose estimation is unavailable. Our approach addresses this issue by incorporating fast-slow pipelines and two latent world models. 

initialized queries. This eliminates the need for training separate models for temporal and singleframe detection and enables mutual reinforcement between the fast and slow pipelines. Specifically, the slow pipeline benefits from a better initialization for temporal propagation, while the fast pipeline implicitly leverages the temporal dynamics learned through shared weights. To improve temporal propagation, we propose latent query and BEV world models based on the principle that _”the present represents a continuation of the past.”_ Conditioned on the relative poses in adjacent frames, both latent world models propagate state representations from historical observations to the current timestep, significantly enhancing the robustness of temporal propagation in the slow pipeline. 

**Contributions:** (1) We identify severe performance degradation issues in existing stream-based methods. To address this, we propose **FASTopoWM** , a novel fast-slow framework augmented with latent world models for robust lane segment topology reasoning. (2) We introduce a unified fast-slow system that enables parallel supervision of both historical and newly initialized queries. This design facilitates mutual reinforcement and allows inference switching based on pose estimation conditions, thereby enhancing system robustness. (3) We design two latent world models that effectively capture temporal dynamics and enable strong temporal propagation. (4) FASTopoWM is evaluated on the OpenLane-V2 dataset (Wang et al., 2024a), achieving state-of-the-art performance in lane topology reasoning. 

## 2 RELATED WORK 

### 2.1 HD MAP AND LANE TOPOLOGY REASONING 

Current high-definition (HD) map learning frameworks employ end-to-end detection pipelines to generate vectorized representations of map elements. VectorMapNet (Liu et al., 2023) formulates map elements as polyline to eliminate heuristic post-processing. MapTR (Liao et al., 2022; 2023) 

2 

Preprint, Under review. 


**Figure 2: Overall Framework. (a) Encoder.** Historical queries and BEV features are processed by world models, conditioned on action latent, to predict the stream queries and stream BEV features. Multi-view images are encoded into BEV features, which are then fused with the stream BEV features. **(b) Decoder.** The slow and fast systems share the same Transformer layers and prediction heads to enable parallel supervision of both stream and newly initialized queries. **T** represents the frame at timestep **T** . 

develops permutation-equivalent modeling for lane point sets. Mask2map (Choi et al., 2024) incorporates mask-aware queries and BEV features to enhance semantic understanding. MapDR (Chang et al., 2025) decomposes road networks into geometric, connectivity, and regulatory layers. For temporal modeling, StreamMapNet (Yuan et al., 2024) implements stream-based propagation. SQDMapNet (Wang et al., 2024b) applies query denoising for BEV boundary consistency. InteractionMap (Wu et al., 2025) achieves comprehensive temporal fusion through local-to-global integration. In contrast to HD map learning, lane topology reasoning primarily focuses on the topological relationships among lanes. TopoNet (Li et al., 2023a) establishes dual lane-to-lane and lane-to-traffic graphs. TopoLogic (Fu et al., 2025a) and TopoPoint (Fu et al., 2025b) emphasize the critical role of endpoints in topological connectivity. TopoMLP (Wu et al., 2023) explicitly encodes coordinate information to improve topological reasoning. Topo2Mask (Kalfaoglu et al., 2024) introduces instance masks and mask attention mechanisms to update query representations. TopoFormer (Lv et al., 2025) proposes geometry-guided and counterfactual self-attention to enhance road topology understanding. In contrast to these approaches, we propose a fast-slow system that addresses the limitations of existing stream-based methods and incorporate two latent world models to effectively capture temporal dynamics. 

### 2.2 WORLD MODEL IN AUTONOMOUS DRIVING 

The world model serves as a bridge between understanding and generating future states. In autonomous driving, it can predict the future state of the ego vehicle conditioned on its actions (Bar et al., 2025). GAIA-1 (Hu et al., 2023a) leverages sequence learning to anticipate future events. DriveDreamer (Wang et al., 2024c) introduces a two-stage diffusion training pipeline to generate controllable driving scenes. Instead of synthesizing pixel-level content, OccWorld (Zheng et al., 2024) forecasts 3D occupancy to simulate future scenarios. To reduce computational overhead and modeling complexity, recent approaches have shifted toward predicting compact latent representations using world models. BEVWorld (Zhang et al., 2024) proposes a latent BEV sequence diffusion model to forecast future scenes conditioned on multi-modal inputs. WoTE (Li et al., 2025) predicts future BEV features to evaluate high-confidence trajectories. LAW (Li et al., 2024) employs a latent world model for self-supervised learning. Motivated by prior work, we design a dual latent world model framework that learns the transformation from past to present, enabling more effective temporal reasoning and enhancing current lane topology prediction. 

3 

Preprint, Under review. 

### 2.3 FAST-SLOW SYSTEM 

In autonomous driving scenarios, where real-time performance and reliability are essential, adding computational burden or auxiliary cues to boost prediction accuracy is often infeasible in practice. As a trade-off solution, fast-slow systems have recently been introduced. The fast system performs essential predictions with minimal overhead, while the slow system leverages additional computation and auxiliary cues to handle complex scenarios. Fast-slow systems enable flexible mode switching tailored to the varying demands of different scenarios. Chameleon (Zhang et al., 2025) utilizes a VLM with chain-of-thought (CoT) reasoning to conduct neuro-symbolic topology inference in the slow system. FAST (Xiao et al., 2025) dynamically switches between short and long reasoning paths based on task complexity. SlowFast-LLaVA (Xu et al., 2024) employs different sampling rates to capture motion cues and fuses slow and fast features to efficiently represent video information. Xu _et al._ (Xu et al., 2025) combine a “slow” LLM for command parsing with a “fast” RL agent for vehicle control. FASIONAD++ (Qian et al., 2025) incorporates a VLM as the slow system to provide feedback and evaluation for a fast end-to-end pipeline. However, in many of these approaches, the fast and slow systems are implemented as entirely separate frameworks, and switching occurs based on the scenario. In contrast, our method does not require additional models for the fast or slow pathways. Instead, fast and slow systems are trained under parallel supervision, enabling mutual reinforcement and improving overall robustness. 

## 3 METHOD 

### 3.1 PROBLEM FORMULATION 

Given surround-view images captured by vehicle-mounted cameras, our goal is to infer lane segments _{_ **L**<sup>_c_</sup> _,_ **L**<sup>_l_</sup> _,_ **L**<sup>_r_</sup> _}_ and their topological connectivity **A** in the bird’s-eye view (BEV). Each lane segment consists of a centerline **L**<sup>_c_</sup> = ( **P** _, Class_ ), a left boundary **L**<sup>_l_</sup> = ( **P** _, Type_ ), and a right boundary **L**<sup>_r_</sup> = ( **P** _, Type_ ). Here, **P** = _{_ ( _xi, yi, zi_ ) _}|_<sup>_M_</sup> _i_ =1<sup>denotesasetofvectorized3Dpoints,</sup> where _M_ is the number of points. _Class_ represents the semantic class of the lane segment (e.g., road line or pedestrian crossing), and _Type_ indicates the boundary type, such as dashed, solid, or non-visible. The adjacency matrix **A** encodes the topological connectivity between lane segments. In the following formulation, **T** denotes the current frame, and **T-1** denotes the previous frame. 

### 3.2 OVERVIEW 

Fig. 2 illustrates the framework of **FASTopoWM** . The overall architecture can be briefly divided into encoder and decoder parts. Both the slow and fast systems are integrated into a unified network. The PV-to-BEV encoder (Li et al., 2022; He et al., 2016; Lin et al., 2017) extracts BEV features **F**<sup>**T**</sup> **bev**<sup>_∈_R</sup><sup>_H×W ×C_,whereC,H,Wrepresentthenumberoffeaturechannels,height,andwidth,</sup> respectively. The initialized queries **Q**<sup>**T**</sup> _∈_ R<sup>_N×C_</sup> are derived from a learnable embedding space. _N_ is the number of queries. The relative ego poses between adjacent frames are encoded into an action latent Ψ. We employ memories for world models to store the historical queries. Conditioned on this action latent, the query world model and the BEV world model transform the historical queries **Q**<sup>**T**</sup><sup>_−_</sup><sup>**1**</sup> and BEV features **F**<sup>**T**</sup> **bev**<sup>_−_</sup><sup>**1**, respectively, to generate the stream queries</sup><sup>**˜QT**and stream</sup> BEV features **F**<sup>**˜T**</sup> **bev**<sup>forthecurrentframe.ThestreamBEVfeaturesarethenfusedwiththeBEV</sup> features extracted from the current frame. The first transformer layer takes the initialized queries **Q**<sup>**T**</sup> and the BEV features **F**<sup>**T**</sup> **bev**<sup>from the current frame as input.The subsequent transformer layers</sup> share weights and receive parallel inputs from both the slow and fast systems. The slow system incorporates temporal information, whereas the fast system does not. During training, both systems are supervised jointly. At inference time, the prediction from the slow system is used as the final output when reliable pose information is available. Otherwise, when such information is missing or inaccurate, the prediction from the fast system is adopted. This design improves robustness while leveraging temporal cues to enhance performance when conditions permit. 

### 3.3 TEMPORAL PROPAGATION VIA LATENT WORLD MODELS 

Temporal propagation leverages detection results from previous frames as auxiliary information to assist prediction in the subsequent frame (Yuan et al., 2024). In contrast to existing latent world 

4 

Preprint, Under review. 

model methods (Li et al., 2024), our approach eliminates the need for future trajectory prediction. Instead, grounded in the principle that “the present represents a continuation of the past,” we utilize known relative poses to infer the current state based on past observations. 

**Input of World Models.** We flatten the relative pose, which includes both relative rotation and translation, to obtain the action latent Ψ. Then, the action-aware query and BEV latent features are obtained by: 


where Ψ is duplicated and concatenated with the query and BEV feature along the channel dimension. 

**Future Latent Prediction.** Latent world models leverage the historical action-aware latent from timestep **T-1** to predict the stream features at the next timestep **T** : 


where query world model is composed of Transformer blocks, containing self-attention modules and feed-forward modules. Similarly, the BEV world model comprises Transformer blocks that incorporate temporal self-attention modules (Li et al., 2022) and feed-forward modules. 

Then, the stream BEV feature are fused with extracted BEV feature using gated recurrent unit (Chung et al., 2014) to enrich temporal cues. 

**Future Latent Supervision.** Unlike previous methods that rely on warping and often lose information at the BEV boundary (Wang et al., 2024b), our BEV world model imagines the evolution of the next-frame BEV representation based on historical BEV features and relative poses. Since dense BEV annotations are difficult to obtain, we adopt a self-supervised learning strategy based on BEV features from temporally adjacent frames. We use mean squared error (MSE) loss to align the stream BEV features with the extracted BEV features of the current frame: 


For queries, we employ transformation loss (Yang et al., 2025b) to supervise consistency of coordinate, category, and semantic BEV mask: 


where **L**<sup>˜</sup> _T_ , _Class_ ˜ _T_ , _Type_ ˜ _T_ and **M**<sup>˜</sup> _T_ are coordinates of lane segment, classes of centerline, boundary types and semantic BEV mask predicted from stream queries **Q**<sup>**˜T**</sup> . **L** _T_ , _Type T_ , _Class T_ and **M** _T_ are GT annotations transformed from T-1 frame to T frame. For brevity, we omit the weights for each loss term. More details can be found in appendix. The overall future latent supervision can be expressed as: 


In this way, the BEV world model is trained using self-supervised learning on BEV representations from adjacent frames to capture temporal cues in the BEV space. Simultaneously, the query world model is trained with temporally continuous annotations, enabling it to transform historical observations into reference anchors (e.g., stream queries) for the current frame. 

5 

Preprint, Under review. 

### 3.4 UNIFIED FAST-SLOW DECODER 

Previous methods incorporate historical information into the decoder to improve performance. However, stream queries enriched with historical cues typically exhibit higher confidence than newly initialized queries. Consequently, during Hungarian assignment, GT annotations are more likely to be matched with stream queries. This bias leads to performance degradation when historical information is unavailable, as the model relies solely on the initialized queries. To overcome this limitation, we propose a unified fast-slow decoder that decouples the forward path into fast and slow branches, allowing parallel supervision of both stream and initialized queries. 

As shown in Fig. 2 (b), the inputs of the first transformer layer are initialized queries and extracted BEV feature: 


where **TransLayer0** denotes the first transformer layer, consisting of a self-attention module, a laneattention module (Li et al., 2023b), and a feed-forward network. According to the classification confidence of **Q**<sup>**T**</sup> **1**<sup>, the lowest-ranked</sup><sup>_N −K_queries of</sup><sup>**QT**</sup> **1**<sup>are substituted with stream queries</sup><sup>**˜QT**.</sup> The slow branch of the remaining transformer layer is then formulated as: 


where **i** denotes the index of the Transformer layer. Notably, the input query to the second Transformer block, **Q**<sup>**˜T**</sup> **1**<sup>, comprises</sup><sup>_K_instances of</sup><sup>**˜QT**and</sup><sup>_N −K_instances of</sup><sup>**QT**</sup> **1**<sup>. For brevity, we reuse</sup> the notation **F**<sup>**˜T**</sup> bev<sup>to represent the fused BEV features obtained by combining the stream BEV fea-</sup> tures **F**<sup>**˜T**</sup> bev<sup>with the extracted BEV features</sup><sup>**FT**</sup> bev<sup>. Similarly, the fast branch of the second Transformer</sup> layer is formulated as: 


Then, shared-weight heads are employed to generate predictions at each layer from **Q**<sup>**T**</sup> **i** + **1**<sup>and</sup><sup>**˜QT**</sup> **i** + **1**<sup>,</sup> with Hungarian matching-based supervision applied in parallel. 

In this manner, the historical queries and the newly initialized queries are supervised concurrently, preventing the model from becoming overly reliant on historical queries. The temporal propagation in the slow system benefits from well-trained initialized queries, particularly at the first frame. Meanwhile, the fast system’s initialized queries implicitly gain from temporal dynamics through shared decoder parameters with the slow system. More details about prediction heads can be found in the appendix. 

## 4 TRAINING LOSS 

The loss function for slow system and fast system are defined as: 


where _Lls_ denotes the lane segment loss, which supervises the predicted lane segments using Hungarian matching (Li et al., 2023b). The details of _Lls_ can be found in the appendix. The overall loss function in FASTopoWM is defined as follows: 


## 5 EXPERIMENTS 

### 5.1 DATASETS AND METRICS 

**Datasets.** We evaluate our method on the multi-view lane topology benchmark OpenLane-V2 (Wang et al., 2024a), which comprises two subsets. SubsetA is re-annotated from Argoverse2 

6 

Preprint, Under review. 

**Table 1:** Comparison with the state-of-the-arts on OpenLane-V2 subsetA on lane segment. All models adopt ResNet-50 as the backbone network and are trained for 24 epochs.<sup>_†_</sup> : Our enhanced model employ GeoDist strategy from TopoLogic (Fu et al., 2025a). 

|Method|Venue<br>|Temporal|mAP|_↑_AP_ls _|_↑_AP_ped _|_↑_TOP_lsls _|_↑_Acc_b _|_↑_<br>FPS|
|---|---|---|---|---|---|---|---|---|
|MapTR (Liao et al., 2022)|ICLR23|No|27.0|25.9|28.1|-|-|14.5|
|MapTRv2 (Liao et al., 2023)|IJCV24|No|28.5|26.6|30.4|-|-|13.6|
|TopoNet (Li et al., 2023a)|Arxiv23|No|23.0|23.9|22.0|-|-|10.5|
|LaneSegNet (Li et al., 2023b)|ICLR24|No|32.6|32.3|32.9|25.4|45.9|14.7|
|TopoLogic (Fu et al., 2025a)|NIPS24|No|33.2|33.0|33.4|30.8|-|-|
|Topo2Seq (Yanget al.,2025a)|AAAI25|No|33.6|33.7|33.5|26.9|48.1|14.7|
|**FASTopoWM (ours)**<br>|-|No|34.1|33.9|34.4|26.6|48.2|14.0|
|**FASTopoWM**<sup>_†_</sup> **(ours)**|-|No|34.2|34.0|34.4|28.4|48.2|14.0|
|StreamMapNet (Yuan et al., 2024)|WACV24|Yes|20.3|22.1|18.6|13.2|33.2|14.1|
|SQD-MapNet(Wanget al.,2024b)|ECCV24|Yes|26.0|27.1|24.9|16.6|39.4|14.1|
|**FASTopoWM (ours)**<br>|-|Yes|**37.4**|**36.4**|**38.4**|29.6|51.2|11.4|
|**FASTopoWM**<sup>_†_</sup> **(ours)**|-|Yes|37.2|36.2|38.1|**31.6**|**51.3**|11.4|


(Wilson et al., 2023), while SubsetB is re-annotated from nuScenes (Caesar et al., 2020). Both subsets contain surround-view images collected from 1,000 scenes. SubsetA features seven camera views, whereas SubsetB includes only six. SubsetA provides annotations for both lane segments and their topology, while SubsetB contains annotations only for centerlines and topology. To generate boundary annotations for SubsetB, we apply a standardized lane width perpendicular to the centerline. For centerline perception evaluation on SubsetB, we approximate centerlines by averaging the coordinates of the left and right boundary lines. We re-train LaneSegNet, StreamMapNet, and SQD-MapNet with the same configuration to obtain their results on SubsetB. 

**Metrics.** We conduct evalua- 

tions on two tasks: lane segment **Table 2:** Comparison with the state-of-the-arts on OpenLane-V2 subperception on SubsetA and censetB on centerline perception. All models adopt ResNet-50 as the backterline perception on SubsetB. bone network and are trained for 24 epochs. TopoFormer<sup>_⋆_</sup> adopts a To assess lane quality, we adopt staged training strategy that utilizes a pretrained lane detector for topolChamfer Distance and Fr´echet ogy reasoning training. While this leads to better detection performance, Distance under fixed thresholds it offers only slight advantage in topology <u>prediction.</u> oflane _{_ 1.0,segments,2.0, 3.0AP _} ls_ meters.and APFor _ped_ VectorMapNet (Liu et al., 2023)STSU (Can et al., 2021)Method ICML23ICCV21Venue TemNoNoporal OLS-- _<u>↑</u>_ DET3.58.2 _l_ _<u>↑</u>_ --TOP _ll_ _<u>↑</u>_ are employed to evaluate the MapTR (Liao et al., 2022) ICLR23 No - 15.2 - detection performance of road TopoNet (Li et al., 2023a) Arxiv23 No 25.1 24.3 6.7 lanes and pedestrian crossings, TopoMLP (Wu et al., 2023) ICLR24 No 36.2 26.6 19.8 respectively. The mean averLaneSegNet (Li et al., 2023b) ICLR24 No 38.7 27.5 24.9 TopoLogic (Fu et al., 2025a) NIPS24 No 36.2 25.9 21.6 age precision (mAP) is calcuTopoFormer<sup>_⋆_</sup> <u>(Lv et al., 2025)</u> CVPR25 No 41.5 34.8 23.2 lated as the average of AP _ls_ and **<mark>FASTopoWM (ours)</mark>** <mark>No 41.8 31.6 27.1</mark> AP _ped_ . To evaluate topology StreamMapNet (Yuan et al., 2024) WACV24 Yes 26.7 18.9 11.9 reasoning, we report TOP _lsls_ . SQD-MapNet (Wang et al., 2024b) ECCV24 Yes 29.1 21.9 13.3 Lane boundary classification ac- **<mark>FASTopoWM (ours)</mark>** <mark>Yes</mark> **<mark>46.3 35.1 33.0</mark>** curacy is measured by Acc _b_ (Yang et al., 2025b). The evaluation protocol for centerline perception follows a similar approach as lane segments. Additionally, OLS (Wang et al., 2024a) is computed between DET _l_ and TOP _ll_ . 

|Method|Venue|Tempora|l<br>OLS|_↑_DET_l _|_↑_TOP_ll ↑_|
|---|---|---|---|---|---|
|VectorMapNet (Liu et al., 2023)|ICML23|No|-|3.5|-|
|STSU (Can et al., 2021)|ICCV21|No|-|8.2|-|
|MapTR (Liao et al., 2022)|ICLR23|No|-|15.2|-|
|TopoNet (Li et al., 2023a)|Arxiv23|No|25.1|24.3|6.7|
|TopoMLP (Wu et al., 2023)|ICLR24|No|36.2|26.6|19.8|
|LaneSegNet (Li et al., 2023b)|ICLR24|No|38.7|27.5|24.9|
|TopoLogic (Fu et al., 2025a)|NIPS24|No|36.2|25.9|21.6|
|TopoFormer<sup>_⋆_</sup>(Lv et al.,2025)|CVPR25|No|41.5|34.8|23.2|
|**FASTopoWM(ours)**|-|No|41.8|31.6|27.1|
|StreamMapNet (Yuan et al., 2024)|WACV24|Yes|26.7|18.9|11.9|
|SQD-MapNet(Wanget al.,2024b)|ECCV24|Yes|29.1|21.9|13.3|
|**FASTopoWM(ours)**|-|Yes|**46.3**|**35.1**|**33.0**|


### 5.2 IMPLEMENTATION DETAILS 

The PV-to-BEV encoder is composed of a pre-trained ResNet-50 (He et al., 2016), an FPN (Lin et al., 2017), and BevFormer (Li et al., 2022). The BEV features has a resolution of 200 _×_ 100, covering a perception area of _±_ 50m _× ±_ 25m. The decoder follows the Deformable DETR architecture, where the standard cross-attention module is substituted with lane attention (Li et al., 2023b). It consists of 6 transformer layers. A total of 200 queries are used, with 30% reserved for temporal propagation in the slow system. Both the query and BEV world models employ 2 transformer layers each. To optimize memory usage on the GPU, we introduce average pooling within the BEV world model to reduce the input BEV resolution from 200 _×_ 100 to 100 _×_ 50. Then, we use bilinear interpolation to restore the output resolution to 200 _×_ 100. The centerline, left boundary, and right boundary are ordered sequence of 10 points. Training is performed over 24 epochs with a batch size of 8 on NVIDIA V100 GPUs. To stabilize the streaming process, the first 12 epochs are trained using single-frame inputs. More details about stream-based training can be found in the appendix. The 

7 

Preprint, Under review. 


**Figure 3:** Qualitative results of baseline and our FASTopoWM. The baseline (BL) is LaneSegNet with streambased temporal propagation. For better viewing, zoom in on the image. learning rate is initialized at 2 _×_ 10<sup>_−_4</sup> and follows a cosine annealing schedule throughout training. We use the AdamW optimizer (Kingma & Ba, 2015). The loss weights _α_ 1 and _α_ 2 are set to 1.0 and 0.3, respectively. During inference, the fast and slow systems can operate in parallel to generate predictions, or alternatively, inference can be performed using only one of the systems. 

### 5.3 MAIN RESULTS 

**Results on Lane Segment.** The results are displayed in Tab. 1. Without incorporating temporal information, our fast system achieves detection performance comparable to current state-of-the-art (SOTA) methods. Our slow system significantly outperforms existing temporal approaches. Compared to current SOTA methods, our slow system achieve a 3.8% improvement in mAP. Furthermore, our enhanced model establishes a new SOTA performance in topology accuracy. 

**Results on Centerline Perception.** The results are presented in Tab. 2. Our fast system surpasses LaneSegNet by 3.1% in OLS. Our slow system outperforms TopoFormer by 4.8% in OLS. By introducing world models to capture temporal information, our slow system achieves a 4.5% improvement in OLS over the fast system. 

### 5.4 ABLATION STUDIES 

The ablation studies are mainly conducted on SubsetA. 

**Ablation Study on Modules.** As shown in Tab. 3, by integrating the fast-slow system with world models, the model achieves substantial performance improvements, surpassing the baseline by 3.4% and 4.3% mAP in temporal and single-frame detection, respectively. 

**Ablation Study on Training Methods.** As 

shown in Tab. 4a, the baseline method shows a significant drop in single-frame detection performance. PrevPredMap (Peng et al., 2025) addresses this issue by randomly alternating between single-frame and temporal training modes. However, this alternating training reduces the effectiveness of temporal feature learning. In contrast, our fast-slow system enables parallel training of both modes, achieving improvements of 2.1% mAP and 1.1% TOP _lsls_ in temporal detection. 

**Table 3:** Ablation studies on different modules. The baseline is LaneSegNet with stream-based temporal propagation. FS denotes the fast-slow system. _QWM_ and _BWM_ represent the query world model and BEV world model, respectively. _Tem._ and _Sin._ indicate temporal and single-frame detection. 

||Modules|T|em.|S|in.|
|---|---|---|---|---|---|
|FS|QWM<br>BWM|mAP|TOP_lsls_|mAP|TOP_lsls_|
|||34.0|28.1|29.8|23.4|
|✓||35.3|28.4|33.2|25.8|
|✓|✓|36.3|29.0|33.7|26.3|
|✓|✓|36.4|29.1|33.6|26.2|
|✓|✓<br>✓|**37.4**|**29.6**|**34.1**|**26.6**|


### **Ablation Study on World Models.** Tab. 4b 

examines the impact of different action conditions. Without action conditioning, the world model can still predict future states, but localization accuracy degrades. Inspired by end-to-end driving methods, we also condition on future trajectories, which provide future positions and could reduce reliance on pose estimation. However, this leads to clear performance drops, likely due to limited trajectory regression accuracy and the model’s lack of agent-awareness and dynamics inputs (e.g., speed, steering). Conditioning on relative ego pose yields the best results. Tab. 4c compares network architectures: linear layers and MLPs fail to capture temporal dependencies, while stacked 

8 

Preprint, Under review. 

**Table 4:** The ablation studies of different configurations in the proposed FASTopoWM. The experiments are conducted on OpenLane-V2 subset A. We bold the best scores. 

|**(a)**Different trainin<br>SegNet with stream<br>|g met<br>-based<br>Te|hods. T<br>tempor<br>m|he baseline is Lan<br>al propagation.<br>Sin|e-<br>**(b)**|Differe<br>Action|nt action|condition the<br>Tem.|world models.|
|---|---|---|---|---|---|---|---|---|
|Method<br>||.<br>|.<br><br>|||mAP|AP_ls_<br>AP_ped_|TOP_lsls_|
||mAP<br>|TOP_ll_|mAP<br>TOP_ll_||||||
|BaseLine<br>Random+WM<br>FastSlow+WM|34.0<br>35.3<br>**374**|_ss_<br>28.1<br>28.5<br>**296**|_ss_<br>29.8<br>23.4<br>33.9<br>26.2<br>**341**<br>**266**||None<br>Traj.<br>Pos.|36.5<br>31.2<br>**37.4**|35.1<br>37.9<br>30.8<br>31.5<br>**36.4**<br>**38.4**|28.5<br>24.5<br>**29.6**|
|**(c)**Different archit<br>Arch.|**.**<br>ecture|**.**<br>of worl<br>Tem.|**.**<br>**.**<br>d models.|**(d)**Diffe<br>No. QWM|rent num<br>Te|ber of l<br>m.|ayers in the wo<br>No. BWM|rld models.<br>Tem.|
|mAP|AP_ls_|AP_ped_|TOP_lsls_||mAP|TOP_lsls_|m|AP<br>TOP_lsls_|
|Linear<br>35.2<br>MLPs<br>36.2<br>Transformer<br>**37.4**|34.2<br>35.9<br>**36.4**|36.2<br>36.2<br>**38.4**|28.5<br>28.9<br>**29.6**|2<br>4<br>6|**37.4**<br>37.1<br>37.3|29.6<br>**29.9**<br>29.5|2<br>3<br>4<br>3<br>6<br>**3**|7.4<br>29.6<br>7.7<br>29.9<br>**7.8**<br>**30.2**|
|**T**<br>**T+1**||**T+2**<br>**(a)**|**T+3**<br>**T+4**|**T**||**T+1**|**T+2**<br>**T**<br>**(b)**|**+3**<br>**T+4**|


**Figure 4:** Visualization of topology predictions across consecutive 5 frames. The results of FASTopoWM are shown on the top, and the results of temporal baseline are shown on the bottom. The temporal baseline is LaneSegNet (Li et al., 2023b) with stream-based temporal propagation. For better viewing, zoom in on the images. 

transformers achieve the best performance. As shown in Tab. 4d, we fix the number of transformer layers in one world model while varying it in the other. The model performance is relatively insensitive to the number of query world model layers. While deeper models offer slight gains, they reduce inference efficiency. We use two layers as a trade-off. 

### 5.5 QUALITATIVE RESULTS 

Fig. 3 provides a qualitative result comparison between baseline method and our FASTopoWM under different road structures. The baseline method produces more misaligned endpoints, which confuses topology reasoning. It also suffers from missed detections and hallucinated results. In contrast, our method yields good lane segment perception with accurate topology reasoning. Fig. 4 visualizes the comparison of temporal detection results across 5 frames. The baseline method fails to maintain temporal topological consistency, resulting in false detections, missed detections, and hallucinated topologies. Our method demonstrates robust temporally consistent topology reasoning results. 

## 6 CONCLUSION 

In this paper, we propose FASTopoWM, a novel fast-slow lane segment topology reasoning framework enhanced with latent world models. To overcome the limitations of existing stream-based 

9 

Preprint, Under review. 

methods, we integrate fast and slow systems into a unified architecture that enables parallel supervision of both historical and newly initialized queries, fostering mutual reinforcement. The slow pipeline exploits temporal information to enhance detection performance, while the fast pipeline conducts single-frame perception to ensure the system’s basic functionality. To further strengthen temporal propagation, we introduce latent query and BEV world models conditioned on the action latent, allowing the system to propagate state representations from past observations to the current timestep. This design significantly boosts the performance of the slow pipeline. Extensive experiments on the OpenLane-V2 benchmark demonstrate that our model achieves SOTA performance and validate the effectiveness of our proposed components. 

## REFERENCES 

- Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 15791–15801, 2025. 

- Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 11621–11631, 2020. 

- Yigit Baran Can, Alexander Liniger, Danda Pani Paudel, and Luc Van Gool. Structured bird’seye-view traffic scene understanding from onboard images. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 15661–15670, 2021. 

- Xinyuan Chang, Maixuan Xue, Xinran Liu, Zheng Pan, and Xing Wei. Driving by the rules: A benchmark for integrating traffic sign regulations into vectorized hd map. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 6823–6833, 2025. 

- Sehwan Choi, Jungho Kim, Hongjae Shin, and Jun Won Choi. Mask2map: Vectorized hd map construction using bird’s eye view segmentation masks. In _European Conference on Computer Vision_ , pp. 19–36. Springer, 2024. 

- Junyoung Chung, Caglar Gulcehre, KyungHyun Cho, and Yoshua Bengio. Empirical evaluation of gated recurrent neural networks on sequence modeling. _arXiv preprint arXiv:1412.3555_ , 2014. 

- Yanping Fu, Wenbin Liao, Xinyuan Liu, Hang Xu, Yike Ma, Yucheng Zhang, and Feng Dai. Topologic: An interpretable pipeline for lane topology reasoning on driving scenes. _Advances in Neural Information Processing Systems_ , 37:61658–61676, 2025a. 

- Yanping Fu, Xinyuan Liu, Tianyu Li, Yike Ma, Yucheng Zhang, and Feng Dai. Topopoint: Enhance topology reasoning via endpoint detection in autonomous driving. _arXiv preprint arXiv:2505.17771_ , 2025b. 

- Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 770–778, 2016. 

- Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023a. 

- Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 17853–17862, 2023b. 

- Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 8340–8350, 2023. 

10 

Preprint, Under review. 

- M Kalfaoglu, Halil Ibrahim Ozturk, Ozsel Kilinc, and Alptekin Temizel. Topomaskv2: Enhanced instance-mask-based formulation for the road topology problem. _arXiv preprint arXiv:2409.11325_ , 2024. 

- Diederik P. Kingma and Jimmy Ba. Adam: A method for stochastic optimization. In _ICLR_ , 2015. 

- Tianyu Li, Li Chen, Huijie Wang, Yang Li, Jiazhi Yang, Xiangwei Geng, Shengyin Jiang, Yuting Wang, Hang Xu, Chunjing Xu, et al. Graph-based topology reasoning for driving scenes. _arXiv preprint arXiv:2304.05277_ , 2023a. 

- Tianyu Li, Peijin Jia, Bangjun Wang, Li Chen, Kun Jiang, Junchi Yan, and Hongyang Li. Lanesegnet: Map learning with lane segment perception for autonomous driving. _arXiv preprint arXiv:2312.16108_ , 2023b. 

- Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. _arXiv preprint arXiv:2406.08481_ , 2024. 

- Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. _arXiv preprint arXiv:2504.01941_ , 2025. 

- Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In _European conference on computer vision_ , pp. 1–18. Springer, 2022. 

- Bencheng Liao, Shaoyu Chen, Xinggang Wang, Tianheng Cheng, Qian Zhang, Wenyu Liu, and Chang Huang. Maptr: Structured modeling and learning for online vectorized hd map construction. _arXiv preprint arXiv:2208.14437_ , 2022. 

- Bencheng Liao, Shaoyu Chen, Yunchi Zhang, Bo Jiang, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Maptrv2: An end-to-end framework for online vectorized hd map construction. _arXiv preprint arXiv:2308.05736_ , 2023. 

- Tsung-Yi Lin, Piotr Doll´ar, Ross Girshick, Kaiming He, Bharath Hariharan, and Serge Belongie. Feature pyramid networks for object detection. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pp. 2117–2125, 2017. 

- Yicheng Liu, Tianyuan Yuan, Yue Wang, Yilun Wang, and Hang Zhao. Vectormapnet: End-to-end vectorized hd map learning. In _International Conference on Machine Learning_ , pp. 22352–22369. PMLR, 2023. 

- Changsheng Lv, Mengshi Qi, Liang Liu, and Huadong Ma. T2sg: Traffic topology scene graph for topology reasoning in autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 17197–17206, 2025. 

- Nan Peng, Xun Zhou, Mingming Wang, Xiaojun Yang, Songming Chen, and Guisong Chen. Prevpredmap: Exploring temporal modeling with previous predictions for online vectorized hd map construction. In _2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pp. 8134–8143. IEEE, 2025. 

- Kangan Qian, Ziang Luo, Sicong Jiang, Zilin Huang, Jinyu Miao, Zhikun Ma, Tianze Zhu, Jiayin Li, Yangfan He, Zheng Fu, et al. Fasionad++: Integrating high-level instruction and information bottleneck in fat-slow fusion systems for enhanced safety in autonomous driving with adaptive feedback. _arXiv preprint arXiv:2503.08162_ , 2025. 

- Huijie Wang, Tianyu Li, Yang Li, Li Chen, Chonghao Sima, Zhenbo Liu, Bangjun Wang, Peijin Jia, Yuting Wang, Shengyin Jiang, et al. Openlane-v2: A topology reasoning benchmark for unified 3d hd mapping. _Advances in Neural Information Processing Systems_ , 36, 2024a. 

- Shuo Wang, Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Zehui Chen, Tiancai Wang, Chi Zhang, Xiangyu Zhang, and Feng Zhao. Stream query denoising for vectorized hd-map construction. In _European Conference on Computer Vision_ , pp. 203–220. Springer, 2024b. 

11 

Preprint, Under review. 

- Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-drive world models for autonomous driving. In _European conference on computer vision_ , pp. 55–72. Springer, 2024c. 

- Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, et al. Argoverse 2: Next generation datasets for self-driving perception and forecasting. _arXiv preprint arXiv:2301.00493_ , 2023. 

- Dongming Wu, Jiahao Chang, Fan Jia, Yingfei Liu, Tiancai Wang, and Jianbing Shen. Topomlp: An simple yet strong pipeline for driving topology reasoning. _arXiv preprint arXiv:2310.06753_ , 2023. 

- Kuang Wu, Chuan Yang, and Zhanbin Li. Interactionmap: Improving online vectorized hdmap construction with interaction. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 17176–17186, 2025. 

- Wenyi Xiao, Leilei Gan, Weilong Dai, Wanggui He, Ziwei Huang, Haoyuan Li, Fangxun Shu, Zhelun Yu, Peng Zhang, Hao Jiang, et al. Fast-slow thinking for large vision-language model reasoning. _arXiv preprint arXiv:2504.18458_ , 2025. 

- Chengkai Xu, Jiaqi Liu, Yicheng Guo, Yuhang Zhang, Peng Hang, and Jian Sun. Towards humancentric autonomous driving: A fast-slow architecture integrating large language model guidance with reinforcement learning. _arXiv preprint arXiv:2505.06875_ , 2025. 

- Mingze Xu, Mingfei Gao, Zhe Gan, Hong-You Chen, Zhengfeng Lai, Haiming Gang, Kai Kang, and Afshin Dehghan. Slowfast-llava: A strong training-free baseline for video large language models. _arXiv preprint arXiv:2407.15841_ , 2024. 

- Yiming Yang, Yueru Luo, Bingkun He, Erlong Li, Zhipeng Cao, Chao Zheng, Shuqi Mei, and Zhen Li. Topo2seq: Enhanced topology reasoning via topology sequence learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pp. 9318–9326, 2025a. 

- Yiming Yang, Yueru Luo, Bingkun He, Hongbin Lin, Suzhong Fu, Chao Yan, Kun Tang, Xinrui Yan, Chao Zheng, Shuguang Cui, et al. Topostreamer: Temporal lane segment topology reasoning in autonomous driving. _arXiv preprint arXiv:2507.00709_ , 2025b. 

- Tianyuan Yuan, Yicheng Liu, Yue Wang, Yilun Wang, and Hang Zhao. Streammapnet: Streaming mapping network for vectorized online hd map construction. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pp. 7356–7365, 2024. 

- Yumeng Zhang, Shi Gong, Kaixin Xiong, Xiaoqing Ye, Xiaofan Li, Xiao Tan, Fan Wang, Jizhou Huang, Hua Wu, and Haifeng Wang. Bevworld: A multimodal world simulator for autonomous driving via scene-level bev latents. _arXiv preprint arXiv:2407.05679_ , 2024. 

- Zongzheng Zhang, Xinrun Li, Sizhe Zou, Guoxuan Chi, Siqi Li, Xuchong Qiu, Guoliang Wang, Guantian Zheng, Leichen Wang, Hang Zhao, et al. Chameleon: Fast-slow neuro-symbolic lane topology extraction. _arXiv preprint arXiv:2503.07485_ , 2025. 

- Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European conference on computer vision_ , pp. 55–72. Springer, 2024. 

- Zewei Zhou, Tianhui Cai, Seth Z Zhao, Yun Zhang, Zhiyu Huang, Bolei Zhou, and Jiaqi Ma. Autovla: A vision-language-action model for end-to-end autonomous driving with adaptive reasoning and reinforcement fine-tuning. _arXiv preprint arXiv:2506.13757_ , 2025. 

12 

Preprint, Under review. 

## A APPENDIX 

### A.1 ACTION LATENT 

In the ablation study, we try to use both relative pose and trajectory as conditions for the world models. Ultimately, conditioning on relative poses achieve the best performance. 

**Related Pose.** The relative pose is defined as the transformation matrix that maps the rotation matrix R and translation vector t from the LiDAR coordinate system of the previous frame to that of the current frame. It can be formulated as: 


**Trajectory.** The trajectory represents the future positions of the ego vehicle. We extract positions over a 3-second horizon (equivalent to 6 frames) and transform them into the current BEV coordinate system to generate 6 waypoints **W** _t_ = _{_ **w** _t_<sup>1</sup><sup>_,_</sup><sup>**w**</sup> _t_<sup>2</sup><sup>_, · · ·,_</sup><sup>**w**</sup> _t_<sup>6</sup><sup>_}_(Li et al., 2024).In the final five frames</sup> of a scene, some future positions may be unavailable; in such cases, interpolation is applied to complete the trajectory. The trajectory query is randomly initialized and refined via cross-attention with the BEV features and lane segment queries. A MLP is used to predict the trajectory from trajectory query. Then, the loss for trajectory prediction can be formulated as: 


We concatenate the predicted waypoints with the query and BEV features along the channel dimension, and use the world model to predict the state of the next frame. 

### A.2 TRANSFORMATION LOSS 

Transformation losses are applied to supervise both the stream query and the query world model, with the goal of minimizing projection errors across frame transitions. We employ MLPs to predict lane segment coordinate, lane segment class, boundary class and BEV mask from stream queries **˜Q**<sup>**T**</sup> : 


where **R**<sup>**S**</sup> **C**<sup>indicates the centerline reference points for stream queries. InSigmod refers to the inverse</sup> sigmoid function, while Denorm stands for denormalize.the centerline to both the left and right lanes. **L**<sup>˜</sup> _t_ , _Class_ ˜ _offsett_ , _Type_ ˜ represents the lateral distance from _t_ and **M**<sup>˜</sup> _t_ are coordinates of lane 

13 

Preprint, Under review. 

segment, classes of centerline, boundary types and semantic BEV mask. Then, the transformation losses are represented as: 


where the values of _κ_ 1, _κ_ 2, _κ_ 3, _κ_ 4, _κ_ 5, _κ_ 6, and _κ_ 7 are 1.0, 0.01, 1.0, 1.0, 0.025, 1.0 and 3.0. 

### A.3 PREDICTION HEADS 

After the decoder, we employ MLPs to predict lane segment coordinate, lane segment class, boundary class and BEV mask from the updated queries **Q** : 


where **Rc** denotes centerline reference points and **PE** indicates positional embedding. **A**<sup>˜</sup> denotes the adjacency matrix that encodes the topological associations. The confidence threshold for the adjacency matrix is set at 0.5 

### A.4 LANE SEGMENT LOSS 

Lane segment loss is proposed by LaneSegNet (Li et al., 2023b): 


where the hyperparameters are defined as: _ω_ 1 = 0 _._ 025, _ω_ 2 = 3 _._ 0, _ω_ 3 = 1 _._ 5, _ω_ 4 = 0 _._ 01, and _ω_ 5 = 5 _._ 0. _Lvec_ is the L1 loss computed between the predicted vectorized lanes and the ground truth lanes. _Lseg_ = _Lce_ + _Ldice_ consists of a Cross-Entropy loss and a Dice loss used to supervise the BEV semantic mask. The classification losses _Lcls_ and _Ltype_ are used for lane segment classification. _Ltopo_ is a focal loss applied to supervise the topological relationship prediction. 

### A.5 STREAMING TRAINING 

We adopt the streaming training strategy for temporal fusion. For each training sequence, we randomly divide it into 2 splits at the start of each training epoch to foster more diverse data sequences. During inference, we use the entire sequences. Suppose a batch contains N samples, each from a different scene, read in chronological order. Temporal fusion is performed by determining whether the current data and the previously read data belong to the same scene. To facilitate temporal fusion, we introduce several memory modules, including stream query memory, stream BEV memory, and stream reference point memory, which store the predictions from the preceding frame. 

14 

Preprint, Under review. 

### A.6 DEMO 

See the supplementary material vis.gif file for details. The visualization results demonstrate that our predictions maintain robust temporal consistency, reflected in the stable alignment of lane segment coordinates and topological structures as the ego vehicle moves. 

### A.7 LIMITATION AND FUTURE WORK 

World models demonstrate strong capability in predicting the next-timestep BEV and transforming query information for common driving scenarios, such as stationary states, straight-line driving, and gentle turns. However, their generalization may be inadequate for rare scenarios involving rapid changes in ego-vehicle pose, such as high-curvature turns. To address this, we plan to introduce noise to simulate diverse ego-vehicle pose variations, thereby enhancing the temporal transformation capability of world models in such corner cases. Furthermore, we intend to integrate Vision Language Models (VLMs) to aggregate world model outputs for improved detection, and leverage linguistic descriptions to enhance lane topology reasoning and interpretability. Finally, we aim to establish rules based on lane topology to provide actionable safety recommendations for autonomous driving. 

### A.8 USE OF LLM 

In this paper, Large Language Model is used only for writing enhancement purposes. 

15 

