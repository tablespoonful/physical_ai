---
title: "Delta-Triplane Transformers as Occupancy World Models"
date: "2026"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2503.07338
pdf: https://arxiv.org/pdf/2503.07338
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.07338)** / [論文ページ](https://arxiv.org/abs/2503.07338)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Aligned Delta-Triplane Transformers as Occupancy World Models** 

**Haoran Xu**<sup>1</sup> **, Peixi Peng**<sup>1</sup><sup>_,_3</sup> **,**<sup>_∗_</sup> **Shijun Guo**<sup>4</sup> **, Guang Tan**<sup>2</sup> **,**<sup>_∗_</sup> 

**Yiqian Chang**<sup>5</sup> , **Yisen Zhao**<sup>1</sup> , **Shuaixian Wang**<sup>6</sup> , and **Yonghong Tian**<sup>1</sup><sup>_,_3</sup> 

- 1Peking University 2Shenzhen Campus of Sun Yat-sen University 

      - 3Peng Cheng Laboratory 4Xidian University 

   - 5Shenzhen Campus of Harbin Institute of Technology 

         - 6Shenzhen Polytechnic University 

- `{xuhr.sz, pxpeng}@pku.edu.cn tanguang@mail.sysu.edu.cn` 

## **Abstract** 

Occupancy World Models (OWMs) aim to predict future 3D occupancy scenes from historical observations and future ego motions, providing a useful world simulation tool for autonomous driving. Existing methods usually rely on large networks to implicitly align multi-frame historical states and predict future occupancy in a full-state manner, which is costly and redundant because most scene regions remain unchanged over short time intervals. In this paper, we propose _Aligned Delta-Triplane Transformer_ (ADTT), a compact 4D OWM that explicitly aligns historical triplanes with ego-motion compensation and predicts only future scene changes. Based on the aligned triplane prior, a query-conditioned Transformer predicts residual changes, where ego-motion queries guide controllable future motion and learnable external queries capture scene changes beyond ego motion. The predicted changes are added to the aligned prior and decoded into future occupancy scenes. Experiments on Occ3D-nus show that ADTT achieves state-ofthe-art forecasting performance with fewer parameters and higher FPS. Our code is publicly available online: `https://github.com/kyoran/ADTT` . 

## **1 Introduction** 

Recently, Occupancy World Models (OWMs) [47, 34, 37, 43, 8, 17, 28, 22, 45] have emerged as a promising framework for modeling dynamic 3D scenes. Instead of representing the environment with 2D images [35] or bird’s-eye-view (BEV) features [20], OWMs describe real-world scenes with structured 3D semantic voxels and predict how these scenes evolve over time under different ego actions. This makes OWMs a useful tool for simulating future physical worlds, and provides a scalable way to generate training data, including rare corner cases, for autonomous driving and indoor navigation. 

In designing OWMs, there are two tasks need to be solved: (i) removing historical ego-motion 


Figure 1: (a-b) Comparison between the full occupancy and occupancy changes (∆) of a scene. In the change map, red indicates newly appeared voxels, while blue denotes disappeared voxels. (c) Distribution of latent-space feature values for full occupancy versus occupancy changes. 

- _∗_ Corresponding authors. 

40th Conference on Neural Information Processing Systems (NeurIPS 2026). 


Figure 2: ADTT follows a simple yet effective procedure: it first represents occupancy scenes with pretrained triplanes, then explicitly aligns historical triplanes through historical ego-motion compensation, and finally employs a Transformer to predict triplane changes (∆) based on the aligned triplane features, future ego-motion query, and external learnable query. 

effects to better model surrounding object motion; and (ii) using future ego motions to generate controllable future occupancy scenes. 

For the first task, the observed occupancy changes usually come from two sources: ego-motion and the motion of surrounding objects. If the scene variation introduced by ego-motion can be removed, the remaining changes mainly come from moving objects, making future prediction much easier. This process is usually referred to as motion compensation. Most existing OWMs perform this step implicitly. They first compress high-dimensional 3D occupancy data into latent xy-plane features, and then rely on neural networks to learn the alignment across multiple frames. Such an implicit formulation often requires large model capacity to fit the geometric transformation between frames. Recent works such as _I_<sup>2</sup> -World [22] and GenieDrive [45] introduce dedicated ego-motion-related attention mechanisms to ease the learning of temporal correspondence. However, their alignment is mainly learned through network attention rather than explicit 3D geometric transformation. 

We provide an intuitive example in Figure 1. Figure 1(a) shows the full occupancy state in Occ3D-nus benchmark [2, 31], while Figure 1(b) shows the occupancy changes between two adjacent frames after compensating the previous frame to the next timestep. It is clear that occupancy changes are inherently sparse and key elements of interest are more distinct in the change map. We further compare their latent-space distributions in Figure 1(c), where the _x_ axis denotes a scalar feature value. Full occupancy states exhibit a scattered distribution, while occupancy change states are much more tightly concentrated around zero, which reduces variance and is easier to learn. 

For the second task, future ego-motion should be used as a condition to guide scene prediction. Existing OWMs typically feed ego-motion signals into large Transformers or diffusion models to directly predict the full future occupancy state [43, 37]. However, as suggested by Figure 1, full-state prediction is often redundant, since most regions remain unchanged after motion compensation. This has motivated a compensation-then-prediction paradigm, where the model first removes ego-motion effects and then predicts future occupancy changes. Although this reduces the prediction burden, current methods [22, 45] mainly use future ego-motion as the only condition for prediction. Such signals specify how the ego coordinate frame moves and which areas may enter the future view, but they do not provide enough guidance for the uncertain content that should appear in the future scene. As a result, the predicted future scenes may have limited temporal consistency. 

Based on these observations, we propose _Aligned Delta-Triplane Transformer_ (ADTT), a compact 4D OWM that explicitly aligns historical triplanes and predicts sparse future changes in the triplane latent space, as shown in Figure 2. Specifically, we first pretrain a triplane encoder-decoder to obtain compact and geometry-aware occupancy representations. Then, using ego poses recorded at different timesteps, we perform ego-motion compensation to warp historical triplanes into the target prediction frame. This gives the predictor a stable geometric prior, so that it only needs to model residual changes that cannot be explained by ego motion. To predict these residuals, we design a query-conditioned Transformer. Ego-motion queries inject deterministic future motion guidance, while learnable external queries provide additional flexibility for modeling scene changes that are not explicitly controlled by ego motion. The predicted delta triplanes are added to the motion-aligned prior and decoded into future occupancy scenes. In summary, our contributions are three-fold: 

- We propose ADTT, a compact 4D autoregressive OWM that aligns historical triplanes with ego- 

- motion compensation and forecasts sparse future scene changes. 

2 

_•_ Within ADTT, we introduce two key modules: triplane motion compensation, which aligns historical triplanes into the target frame, and query-conditioned delta prediction, which predicts residual changes from the aligned triplane using ego-motion queries for controllable future guidance and learnable external queries for scene dynamics beyond ego motion. 

- Extensive experiments on Occ3D-nus [2, 31] validate the state-of-the-art (SOTA) performance of 

- ADTT in short- and long-term forecasting, cross-dataset generalization, and real-time inference. 

## **2 Related Works** 

**3D occupancy reconstruction.** 3D occupancy reconstruction methods [32, 31, 38, 23, 26] aim to represent the environment as a 3D voxel grid where each voxel encodes both geometric and semantic information. The field was pioneered by SSCNet [29] for indoor scenes using depth sensors, and later extended to outdoor camera-based settings by MonoScene [3]. These approaches primarily utilize multi-camera RGB images [19, 11] or LiDAR point clouds [4, 40] to infer voxel-wise occupancy and semantics in an agent-centric coordinate system. A core challenge lies in building accurate correlations between raw sensor data and 3D voxel space. Once an accurate occupancy reconstruction is achieved, further learning of the temporal dynamics of scene changes becomes necessary [18]. 

**4D occupancy prediction.** To anticipate future scene changes, various 4D occupancy prediction methods have been proposed to capture the temporal dynamics of scene evolution. Some [24, 27, 15] predict future sensor-level data, which is subsequently voxelized into occupancy results, while others [25, 6, 42, 41] directly forecast occupancy outcomes from historical observations. These methods mainly aim to reduce spatio-temporal prediction errors, but they generally do not consider controllable forecasting conditioned on ego motion. 

**World models for autonomous driving.** World models [10, 9] aim to compress high-dimensional scene representations to capture the temporal dynamics of scene transitions, facilitating both future scene predictions and motion planning for the agent. In autonomous driving, existing models [14, 46] typically map surrounding traffic participants to the BEV perspective to predict instance-level tracklets or directly use diffusion models [39, 36, 35, 7, 13] to generate pixel-level future driving views. Recent world models [37, 43, 47, 44, 8] further exploit structured 3D occupancy data for future scene prediction. However, most of them still compress occupancy scenes into BEV latent features and rely on Transformers or diffusion models to implicitly align multi-frame historical context, which often requires large model capacity to forecast the full future scene. In contrast, our method explicitly aligns historical features and predicts sparse scene changes, both in the triplane latent space [45, 11]. 

## **3 Methodology** 

### **3.1 Problem Formulation** 

Let _S_<sup>_t_</sup> _∈_ R<sup>_H×W ×L_</sup> denote the semantic occupancy scene at timestep _t_ in the ego-centric coordinate frame, where _H_ , _W_ , and _L_ denote the height, width, and length of the voxel space. Given a sequence of historical occupancy observations and ego motions, the model uses them as predefined scene context and predicts future occupancy scenes under given future ego motions. 

For clarity, we denote the historical occupancy context as 


and the ego motions associated with the observed and future intervals as 


Here, each ego motion _m_<sup>_i_</sup> describes the ego transformation from timestep _i −_ 1 to timestep _i_ , such as translation and rotation. The historical occupancy sequence provides scene context, including static structures, visible objects, and recent scene evolution. The historical ego motions are used to align observations captured under different ego-centric frames, while future ego motions serve as conditions for controllable future generation. 

Formally, the OWM learns a mapping: 


3 

where _S_<sup>ˆ</sup><sup>_t_+1:</sup><sup>_t_+</sup><sup>_τf_</sup> denotes the predicted future occupancy sequence. 

Accordingly, as shown in Figure 3, we propose _Aligned Delta-Triplane Transformer_ (ADTT), which aligns historical states and predicts sparse future changes in the aligned triplane latent space. 


### **3.2 Ego-Motion-Aligned Triplane Representation** 

Recent occupancy-related works [45, 11] have gradually shifted their latent space from BEV features to triplane representations, since triplanes provide a compact latent space while preserving more explicit spatial structure. Following this trend, we build our OWM on a pretrained triplane latent space. Different from prior methods that mainly use triplanes as compact scene encodings, we further exploit their geometric structure for ego-motion compensation, explicitly aligning historical triplanes across ego-centric frames before predicting sparse future changes. 

Figure 3: ADTT performs motion compensation and tokenization in the triplane latent space. The Transformer encoder then encodes historical context from triplane tokens, while the decoder predicts next-frame triplane changes using deterministic ego-motion queries and learnable external queries. These predicted changes are added to the latest triplane and finally decoded into future occupancy states. 

As shown in Figure 4, the occupancy scene future occupancy states. _S_<sup>_t_</sup> is encoded by **Φ**<sup>enc</sup> Tri<sup>and compressed into three orthogonal feature planes:</sup> 


where 


The three planes provide complementary projections of the 3D scene. To reconstruct the occupancy scene, each 3D point _pos_ = ( _x, y, z_ ) queries its corresponding features from the _xy_ , _xz_ , and _yz_ planes. The queried features are fused with positional encoding PE( _pos_ ) and passed into **Φ**<sup>dec</sup> Tri<sup>to predict</sup> the semantic occupancy label. 


We pretrain **Φ**<sup>enc</sup> Tri<sup>and</sup><sup>**Φ**dec</sup> Tri<sup>with occupancy reconstruction:</sup> 

where _T_ denotes the set of timesteps in the training data, and _Loccocc_ = _Lce_ + _λLlz_ combines cross-entropy and Lovasz-softmax losses [1, 16].1, 16]., 16]. 16].]. After pretraining, **Φ** enc provides compact and geometry-aware triplane states for future prediction. 


We then perform ego-motion compensation using the known ego poses at different timesteps. These poses describe the trajectory of the ego vehicle and are recorded by the vehicle localization system, such as odometry and IMU [2]. Inspired by spatial transformation and differentiable warping [12, 48], we design an ego-motion compensation operation in the triplane latent space. 

Figure 4: Pretrained triplane for OWM. 

For each timestep _k_ , we denote its ego pose in the global coordinate frame as ( **R** _k,_ **T** _k_ ), where **R** _k_ and **T** _k_ transform a point from the ego coordinate frame at timestep _k_ to the global coordinate frame: 


Here, **p**<sup>_k_</sup> local<sup>denotes a point in the ego coordinate frame at timestep</sup><sup>_k_, and</sup><sup>**p**</sup><sup>_k_</sup> global<sup>denotes the same</sup> point in the global coordinate frame. 

Given a historical timestep _i_ and a target prediction timestep _j_ , our goal is to align the historical triplane _s_<sup>_i_</sup> to the target ego coordinate frame at timestep _j_ . For each location on the target plane, we 

4 

first regard it as a 3D point **p**<sup>_j_</sup> local<sup>in the target ego coordinate frame, and then find where this point</sup> should sample from in the historical triplane. Specifically, we first map **p**<sup>_j_</sup> local<sup>to the global coordinate</sup> frame using the target ego pose, and then map it back to the historical ego coordinate frame: 


This transformation gives the corresponding sourceframe location for each target-frame point. In practice, if the projected location lies inside the valid range of the historical plane, we copy the nearest source feature to the target frame. Otherwise, the location is filled with zeros, indicating that this region has no valid historical correspondence and should be inferred by the prediction module. 

We denote the motion-compensated triplane as: 


Figure 5: Motion compensation in the triplane latent space. 

which provides an aligned geometric prior for predicting the target scene at timestep _j_ . 

### **3.3 Query-Conditioned Delta Prediction** 

Given the motion-aligned triplane representation, ADTT predicts the triplane changes ∆ _st_ +1 with a Transformer encoder-decoder [33, 5]. The encoder builds a spatio-temporal memory from historical triplanes, while the decoder predicts future state changes using ego queries and external queries. 

**Triplane tokenization.** We first convert the motion-compensated triplane _<u>s</u>_<sup>_~~j~~_</sup> into a low-resolution 3D latent token grid, allowing the Transformer to model the scene in a unified and compact spatial structure. Specifically, each plane is projected and downsampled by a lightweight 2D convolutional tokenizer, denoted as _ϕxy_ , _ϕxz_ , and _ϕyz_ , with _D_ down output channels. As shown in Figure 5, the three plane features are then broadcast to the same 3D grid of size _Gx × Gy × Gz_ and fused. For each 3D grid location _pos_ , the fused feature is computed as: 


where Broad _uv_ ( _·_ ) denotes broadcasting a plane feature to the 3D latent grid along its missing axis. The fused feature is then projected to the Transformer token dimension and combined with 3D sinusoidal positional encoding: 


where FC( _·_ ) denotes a fully connected layer that maps the feature to _D_ token dimensions, LN( _·_ ) denotes layer normalization, and PE( _pos_ ) is the 3D spatial positional encoding. 

**Historical memory encoding.** For each prediction step, we use the most recent _τp_ motioncompensated triplane states as temporal context. After tokenization, the historical token sequences are concatenated along the temporal dimension: 


We add a learnable temporal embedding to distinguish different history frames and feed the sequence into a Transformer encoder: 


where _M_<sup>_t_</sup> denotes the encoded spatio-temporal memory. Through self-attention, the encoder allows tokens from different spatial locations and historical timesteps to interact, producing a memory bank that summarizes recent scene context. 

**Ego-motion and external queries.** The decoder queries serve as conditions for future scene prediction. Different from methods that only rely on ego motion, we construct the decoder query from two complementary sources. First, the future ego motion _m_<sup>_t_+1</sup> is encoded by an MLP and expanded into _N_ ego ego-motion queries: 


5 

These queries inject explicit information about the future ego transformation. Second, we introduce _N_ ext learnable external queries _Q_<sup>ext</sup> _∈_ R<sup>_N_ext</sup><sup>_×D_token</sup> . Unlike ego-motion queries, these queries are not tied to a specific motion input. They provide additional learnable slots for modeling residual scene changes that are not fully determined by ego motion, such as local appearance changes, occlusion variations, and newly observed regions. 

The final decoder query is obtained by concatenating the two query groups and adding a learnable future-step embedding: 


The total number of queries is set to match the number of target latent tokens, where _N_ = _N_ ego + _N_ ext = _GxGyGz_ . The Transformer decoder attends to the encoded memory and predicts: 


where ∆ _Z_<sup>_t_+1</sup> _∈_ R<sup>_N×D_token</sup> denotes the predicted delta token sequence. 

The predicted delta tokens are reshaped back to the predefined 3D latent grid and then upsampled Up( _·_ ) to the triplane resolution. We denote this operation as: 


where Up( _·_ ) includes 3D feature refinement, interpolation, and projection back to the three triplane feature maps ∆ _s_<sup>_t_+1</sup> = _{_ ∆ _s_<sup>_t_</sup> _xy_<sup>+1</sup><sup>_,_∆</sup><sup>_s_</sup> _xz_<sup>_t_+1</sup><sup>_,_∆</sup><sup>_st_</sup> _yz_<sup>+1</sup><sup>_}_.The predicted delta triplane is added to the latest</sup> motion-aligned triplane prior to obtain the updated triplane: 


Finally, the updated triplane is decoded into the future occupancy scene: 


The future prediction module is trained with both latent-space and occupancy-space supervision: 


where _L_ tri is the sum of L1 and L2 regression losses, and _ξ_ balances triplane- and occupancy-level supervision. During training, we fix the pretrained encoder to keep the target triplanes stable and fine-tune the decoder to better reconstruct occupancy scenes from predicted latent states. 

## **4 Experiments** 

### **4.1 Experimental settings** 

**Dataset and evaluation metrics.** We evaluate occupancy forecasting on the widely used nuScenes dataset [2] adopted by OWM methods [47, 34, 37, 43, 8, 17, 28, 22, 45] with occupancy annotations from Occ3D [31], referred to as Occ3D-nus. The dataset contains 1,000 scenes, with 700 scenes for training and 100 scenes for testing. For the main evaluation, we use the past four frames (2 seconds) to predict the next six frames (3 seconds), which measures short-term forecasting performance. We further evaluate two types of zero-shot inference ability without additional training. First, following GenieDrive [45], we directly evaluate the model trained on the 3-second setting for longer forecasting horizons. Second, following _I_<sup>2</sup> -World [22], we use Occ3D-Waymo [30, 31] to evaluate cross-dataset generalization on 202 validation scenes. For all tasks, we report intersection over union (IoU) for occupied and unoccupied voxels, as well as mean IoU (mIoU) over 18 semantic classes. 

**Implementation details.** At each timestep, the occupancy data _S_<sup>_t_</sup> has a resolution of 16 _×_ 200 _×_ 200. It covers a spatial range of [ _−_ 40 _,_ 40] meters along the X and Y axes and [ _−_ 1 _,_ 5 _._ 4] meters along the Z axis, with a voxel size of 0 _._ 4 meters. The pretrained triplane representation has a resolution of 16 _×_ 100 _×_ 100 with 8 channels. During triplane tokenization, we use a 3D latent grid size of ( _Gx, Gy, Gz_ ) = (8 _,_ 8 _,_ 4), resulting in _N_ = _GxGyGz_ = 256 latent tokens with token dimension _D_ token = 96. For each frame, the triplane tokens are first augmented with 3D sinusoidal positional encoding, and then with a learnable temporal embedding _e_ time. In the Transformer decoder, we set the numbers of ego-motion queries and learnable external queries to _N_ ego = 64 and _N_ ext = 192, 

6 

Table 1: Comparison on Occ3D-nus 4D occupancy forecasting at 1s, 2s, and 3s. The best and second-best results are shown in **bold** and underlined, respectively. 

|Models|Input||mIoU<br>|(%)_↑_<br>|||IoU<br>|(%)_↑_<br>||FPS_↑_|Params_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||1s|2s|3s|Avg.|1s|2s|3s|Avg.|||
|OccWorld [47]|Occ|25.78|15.14|10.51|17.14|34.63|25.07|20.18|26.63|18|72M|
|OccSora [34]|Occ|32.77|22.04|14.40|23.07|41.39|33.68|29.97|35.01|20|174M|
|OccLLaMA [37]|Occ&Text|25.05|19.49|15.26|19.93|34.56|28.53|24.41|29.17|-|> 7B|
|OccLLM [43]|Occ&Text|24.02|21.65|17.29|20.99|36.65|32.14|28.77|32.52|-|> 7B|
|DOME [8]|Occ|35.11|25.89|20.29|27.10|43.99|35.36|29.74|36.36|6.54|397M|
|UniScene [17]|Occ&Box&Map|35.37|29.59|25.08|31.76|38.34|32.70|29.09|34.84|1.72|69M|
|COME [28]|Occ|42.75|32.97|26.98|34.23|50.57|43.47|38.36|44.13|0.30|692M|
|_I_<sup>2</sup>-World [22]|Occ|47.62|38.58|32.98|39.73|54.29|49.43|45.69|49.80|37|22M|
|GenieDrive [45]|Occ|50.47|41.47|35.83|42.59|56.87|51.46|**47.08**|51.80|41|3.47M|
|ADTT (Ours)|Occ|**55.88**|**45.47**|**39.27**|**46.87**|**59.15**|**51.89**|46.87|**52.63**|**46**|**2.30M**|
|OccWorld-V|Camera|10.97|15.16|10.19|7.53|20.68|24.81|20.09|17.14|3.77|132M|
|DOME-V|Camera|17.79|14.23|11.58|14.53|26.39|23.20|20.42|23.33|2.75|457M|
|_I_<sup>2</sup>-World-V|Camera|21.67|18.78|16.47|18.97|30.55|28.76|26.99|28.77|4.21|82M|
|ADTT-V (Ours)|Camera|**24.15**|**20.37**|**17.63**|**20.71**|**33.62**|**31.05**|**28.49**|**31.05**|**6.16**|**62.30M**|


Table 2: Comparison on the long-term occupancy forecasting at 4s, 5s, and 6s in Occ3D-nus. 

Table 3: Cross-dataset generalization performance in Occ3D-Waymo. 

|Models|4s|mIoU<br>5s|(%)_↑_<br>6s|Avg.|4s|IoU (<br>5s|%)_↑_<br>6s|Avg.|cc-ay|o.||
|---|---|---|---|---|---|---|---|---|---|---|---|
|OccWorld [47]|7.79|6.29|5.76|6.61|17.23|15.31|14.54|15.69|Models|Avg.<br>mIoU|Avg.<br>IoU|
|DOME [8]|23.50|19.37|17.27|20.05|13.84|10.14|8.15|10.71||||
|UniScene [17]<br>|16.44|16.41|15.61|16.15|14.31|14.33|14.15|14.26|Copy&Paste|17.17|28.21|
|_I_<sup>2</sup>-World [22]|28.59|25.32|22.55|25.49|41.75|38.47|35.41|38.54|_I_<sup>2</sup>-World [22]|36.38|52.36|
|GenieDrive [45]|31.16|27.17|23.66|27.33|42.81|39.00|35.60|39.14|<br>ADTT (Ours)|**38.46**|**53.19**|
|ADTT (Ours)|**35.53**|**31.32**|**27.42**|**31.42**|**43.95**|**40.12**|**37.79**|**40.62**||||


respectively. The upsampling operator Up( _·_ ) uses nearest-neighbor interpolation to recover the triplane resolution from the predicted latent tokens. Training is performed on 4 NVIDIA RTX A6000 GPUs, while testing is conducted on a single NVIDIA RTX 4090 GPU. Our code is available online<sup>2</sup> . 

### **4.2 Comparisons with the state-of-the-art** 

**Quantitative comparisons.** Table 1 reports the occupancy forecasting results over the next 3 seconds. With direct occupancy input, our method uses explicit motion compensation and sparse delta prediction, achieving the best overall performance with the highest FPS and the fewest parameters. The only exception is the 3s IoU, where our result is slightly lower. For the vision-input setting (-V), we follow _I_<sup>2</sup> -World [22] and use the output of the vision-based occupancy prediction model STCOcc [21] as the input to the OWM. In this setting, the inference speed is mainly limited by the VON network. Nevertheless, our compact OWM still achieves the best efficiency and performance. Table 2 compares long-term forecasting results under the same setting as GenieDrive [45]. Our method shows better long-term consistency. Motion compensation provides a stable prior for future scenes, and the two decoder queries help model scene changes and newly observed regions from historical context. Finally, Table 3 shows the direct evaluation results on Occ3D-Waymo under the 2Hz setting. “Copy-paste” directly uses the current frame as the future prediction and serves as a lower-bound baseline. Our method achieves the best generalization performance. 

**Qualitative comparisons.** As shown in Figure 6, GenieDrive misses the pedestrian in the first frame and the vehicle in the third frame, and these errors persist in later predictions. It also predicts the pedestrian motion inaccurately in the last frame. In contrast, our method consistently tracks the pedestrian and keeps the correct number of vehicles in the lower region. For the newly observed region at the bottom, our prediction is less smooth than that of GenieDrive because we do not use a generative diffusion module. Nevertheless, it still recovers a reasonably accurate drivable area. 

### **4.3 Ablation study** 

> 2 `https://github.com/kyoran/ADTT` 

7 


Figure 6: Occupancy forecasting comparison on the Occ3D-nus val set (zoom in for details). 

### **Effect of key designs in ADTT.** 

Table 4: Ablation on key designs in ADTT. 

Table 4 shows the ablation study of our core modules. M0 is the full model, and the other variants are built by removing key components from M0. M1 removes the _xz_ and _yz_ planes and uses only the _xy_ plane (i.e., BEV). Without height information, it cannot provide accurate 3D predictions. In M2, the triplane and the transformer are trained fully end-to-end. This makes the prediction model rely on unstable triplane features, leading to limited performance. M3 uses only motion compensation without the transformer. Since objects move in the scene, motion compensation causes overlaps. Without the transformer, the model cannot understand scene dynamics or predict future changes, and it cannot infer newly appeared regions, resulting in poor performance. M4 removes motion compensation, and M5 directly predicts the full future scene. Both show clear performance drops. With limited model capacity, misaligned triplane features or direct full-scene prediction makes the learning problem harder. In M6, the triplane decoder is fixed when training the transformer, which leads to a slight performance drop. 

|Idx. Models|Avg.<br>mIoU|Avg.<br>IoU|FPS|
|---|---|---|---|
|**M0**ADTT|**46.87**|**52.63**|46|
|**M1**w/o triplane representation|41.16|47.85|**52**|
|**M2**w/o pretraining triplane|35.43|40.08|46|
|**M3**w/o transformer|28.69|34.36|59|
|**M4**w/o motion compensation|31.87|37.48|43|
|**M5**w/o delta prediction|36.65|45.50|46|
|**M6**w/o finetuning tri. decoder|45.13|51.42|46|


### Table 5: Ablation on hyperparameters. 

|_G{x,y,z}_|_D_token|depth|Avg.<br>mIoU|Avg.<br>IoU|FPS|
|---|---|---|---|---|---|
|8,8,4|32|1|43.94|51.77|**48**|
|8,8,4|128|2|46.87|52.63|46|
|12,12,3|128|2|46.91|53.11|43|
|12,12,3|128|8|47.05|52.49|39|
|16,16,6|256|8|**49.13**|**54.89**|32|


Table 6: Ablation on motion compensation. 

|Compensation strategy|Avg.<br>mIoU|Avg.<br>IoU|FPS|
|---|---|---|---|
|**C1.1**Occ.-space warp|44.99|50.61|44|
|**C1.2**Occ.-space learnable|43.07|48.36|42|
|**C2.1**Tri.-space warp|46.87|52.63|46|
|**C2.2**Tri.-space learnable|45.62|52.71|44|


**Effect of hyperparameters.** Table 5 shows the **C2.2** Tri.-space learnable 45.62 52.71 44 impact of tokenization grid size ( _Gx, Gy, Gz_ ), token dimension _D_ token, and transformer depth. Larger values improve occupancy forecasting by reducing information loss during tokenization and increasing model capacity, but lower the FPS. The gray row denotes our trade-off version. 

**Effect of motion compensation.** Table 6 compares different motion compensation strategies. All variants use the same model and training settings, and only differ in the compensation strategy. Methods marked with “warp” use the explicit compensation operation in Section 3.2. “Occ.-space” and “Tri.-space” denote the compensation in the occupancy space and the triplane space, respectively. “learnable” replaces explicit warping with a learnable alignment module, i.e., Mutual Control Attention 

8 

Table 7: Ablation on ego and external query counts. 

|Idx.|_N_ego|_N_ext|Avg.<br>mIoU<sup>_↑_</sup>|Avg.<br>IoU <sup>_↑_</sup>|
|---|---|---|---|---|
|**Q1**|0|256|40.14|50.28|
|**Q2**|64|192|**46.87**|**52.63**|
|**Q3**|128|128|40.53|45.35|
|**Q4**|192|64|41.85|50.39|
|**Q5**|256|0|41.72|46.37|


Figure 7: Visualization of ego queries and external queries on all prediction timesteps from Occ3Dnus val set, with five queries per type. 

in _I_<sup>2</sup> -World [22]. C1.1<C2.1 and C1.2<C2.2 show that warping discrete occupancy labels can introduce boundary artifacts, holes, and label discontinuities. Triplane features are smoother and more compact, making alignment more stable. The learnable module adds flexibility, but it leads to less stable performance and lower FPS. We therefore use C2.1 as our trade-off setting. 

**Effect of query counts.** Ego queries provide explicit control signals that describe future ego motion, while external queries model scene dynamics outside direct control. When either type is insufficient, performance drops. In Q1, without ego queries, the model relies mainly on historical context, leading to weaker controllability. In Q5, without external queries, the model depends mostly on ego motion and cannot fully capture interactions in the scene. Increasing the number of ego queries (from Q1 to Q5) does not consistently improve performance, as they are derived from the same control signal and become redundant. Q2 achieves the best balance between ego guidance and scene modeling. Figure 7 shows the statistical behavior of different queries. For each query, we aggregate its activation over all samples in the Occ3D-nus val set on the _xy_ plane and then normalize it to [0 _,_ 1]. The resulting maps indicate which regions each query mainly contributes to when decoding future state changes. Ego queries exhibit similar patterns and concentrate around the ego vehicle, while external queries cover surrounding areas. This indicates that ego queries mainly encode local control, and a moderate number is sufficient, which explains the strong performance of Q2. 


Figure 8: Controllable future occupancy prediction under different ego-motion inputs. 

**Effect of controllable ego query.** The learned external queries are fixed after training, while the ego queries are generated from variable ego-motion inputs, including displacement along the _x_ axis, displacement along the _y_ axis, and the yaw angle in radians. Figure 8 shows two examples with the same initial scene but different ego-motion inputs over the next 6 seconds. In each example, adjacent frames show the specific ego-motion control signal and the visualization of one corresponding ego query. The upper example shows the vehicle turning left, while the lower example shows the vehicle going straight. The ego query mainly attends to the region around the ego vehicle and changes consistently with the given control signal, demonstrating the controllability of our method. 

## **5 Conclusion** 

This paper introduces ADTT, a compact and efficient 4D OWM that performs both motion compensation and scene-change prediction in the triplane latent space. ADTT achieves SOTA performance in short- and long-term forecasting, while delivering faster inference than existing methods. 

9 

## **Acknowledgments and Disclosure of Funding** 

The study was funded by the Shenzhen Science and Technology Program under contracts No. KQTD20240729102051063 and No. JCYJ20241202130025030, the Postdoctoral Fellowship Program (Grade B) of China Postdoctoral Science Foundation under contract No. GZB20260408, the National Natural Science Foundation of China under contracts No. U25B6003, No. 62422602, No. 62372010, No. 62425101, No. 62332002, and the Major Key Project of Pengcheng Laboratory (2024B0101010003). Computing support was provided by Pengcheng Cloudbrain. 

## **References** 

- [1] Maxim Berman, Amal Rannen Triki, and Matthew B Blaschko. The lovász-softmax loss: A tractable surrogate for the optimization of the intersection-over-union measure in neural networks. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 4413–4421, 2018. 

- [2] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11621–11631, 2020. 

- [3] Anh-Quan Cao and Raoul De Charette. Monoscene: Monocular 3d semantic scene completion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 3991–4001, 2022. 

- [4] Anh-Quan Cao, Angela Dai, and Raoul De Charette. Pasco: Urban 3d panoptic scene completion with uncertainty awareness. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14554–14564, 2024. 

- [5] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-end object detection with transformers. In _European conference on computer vision_ , pages 213–229. Springer, 2020. 

- [6] Junliang Chen, Huaiyuan Xu, Yi Wang, and Lap-Pui Chau. Occprophet: Pushing efficiency frontier of camera-only 4d occupancy forecasting with observer-forecaster-refiner framework. In _ICLR_ , 2025. 

- [7] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems_ , 37:91560–91596, 2025. 

- [8] Songen Gu, Wei Yin, Bu Jin, Xiaoyang Guo, Junming Wang, Haodong Li, Qian Zhang, and Xiaoxiao Long. Dome: Taming diffusion model into high-fidelity controllable occupancy world model. _arXiv preprint arXiv:2410.10429_ , 2024. 

- [9] David Ha and Jürgen Schmidhuber. Recurrent world models facilitate policy evolution. _Advances in neural information processing systems_ , 31, 2018. 

- [10] David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018. 

- [11] Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. Tri-perspective view for vision-based 3d semantic occupancy prediction. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9223–9232, 2023. 

- [12] Max Jaderberg, Karen Simonyan, Andrew Zisserman, et al. Spatial transformer networks. _Advances in neural information processing systems_ , 28, 2015. 

- [13] Fan Jia, Weixin Mao, Yingfei Liu, Yucheng Zhao, Yuqing Wen, Chi Zhang, Xiangyu Zhang, and Tiancai Wang. Adriver-i: A general world model for autonomous driving. _arXiv preprint arXiv:2311.13549_ , 2023. 

- [14] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8340–8350, 2023. 

- [15] Tarasha Khurana, Peiyun Hu, David Held, and Deva Ramanan. Point cloud forecasting as a proxy for 4d occupancy forecasting. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1116–1124, 2023. 

10 

- [16] Jumin Lee, Sebin Lee, Changho Jo, Woobin Im, Juhyeong Seon, and Sung-Eui Yoon. Semcity: Semantic scene generation with triplane diffusion. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 28337–28347, 2024. 

- [17] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. Uniscene: Unified occupancy-centric driving scene generation. In _Proceedings of the computer vision and pattern recognition conference_ , pages 11971–11981, 2025. 

- [18] Jinke Li, Xiao He, Chonghua Zhou, Xiaoqiang Cheng, Yang Wen, and Dan Zhang. Viewformer: Exploring spatiotemporal modeling for multi-view 3d occupancy perception via view-guided transformers. In _European Conference on Computer Vision_ , pages 90–106. Springer, 2024. 

- [19] Yiming Li, Zhiding Yu, Christopher Choy, Chaowei Xiao, Jose M Alvarez, Sanja Fidler, Chen Feng, and Anima Anandkumar. Voxformer: Sparse voxel transformer for camera-based 3d semantic scene completion. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9087–9098, 2023. 

- [20] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 27137–27146, 2025. 

- [21] Zhimin Liao, Ping Wei, Shuaijia Chen, Haoxuan Wang, and Ziyang Ren. Stcocc: Sparse spatial-temporal cascade renovation for 3d occupancy and scene flow prediction. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1516–1526, 2025. 

- [22] Zhimin Liao, Ping Wei, Ruijie Zhang, Shuaijia Chen, Haoxuan Wang, and Ziyang Ren. I2-world: Intra-inter tokenization for efficient dynamic 4d scene forecasting. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 25810–25819, 2025. 

- [23] Rui Liu, Wenguan Wang, and Yi Yang. Volumetric environment representation for vision-language navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16317–16328, 2024. 

- [24] Fan Lu, Guang Chen, Zhijun Li, Lijun Zhang, Yinlong Liu, Sanqing Qu, and Alois Knoll. Monet: Motionbased point cloud prediction network. _IEEE Transactions on Intelligent Transportation Systems_ , 23(8): 13794–13804, 2021. 

- [25] Junyi Ma, Xieyuanli Chen, Jiawei Huang, Jingyi Xu, Zhen Luo, Jintao Xu, Weihao Gu, Rui Ai, and Hesheng Wang. Cam4docc: Benchmark for camera-only 4d occupancy forecasting in autonomous driving applications. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21486–21495, 2024. 

- [26] Nicola Marinello, Simen Cassiman, Jonas Heylen, Marc Proesmans, and Luc Van Gool. Camera-only 3d panoptic scene completion for autonomous driving through differentiable object shapes. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 2520–2529, 2025. 

- [27] Benedikt Mersch, Xieyuanli Chen, Jens Behley, and Cyrill Stachniss. Self-supervised point cloud prediction using 3d spatio-temporal convolutional networks. In _Conference on Robot Learning_ , pages 1444–1454. PMLR, 2022. 

- [28] Yining Shi, Kun Jiang, Qiang Meng, Ke Wang, Jiabao Wang, Wenchao Sun, Tuopu Wen, Mengmeng Yang, and Diange Yang. Come: Adding scene-centric forecasting control to occupancy world model. _arXiv preprint arXiv:2506.13260_ , 2025. 

- [29] Shuran Song, Fisher Yu, Andy Zeng, Angel X Chang, Manolis Savva, and Thomas Funkhouser. Semantic scene completion from a single depth image. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 1746–1754, 2017. 

- [30] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2446–2454, 2020. 

- [31] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. _Advances in Neural Information Processing Systems_ , 36:64318–64330, 2023. 

11 

- [32] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei Wu, Hanming Deng, Yi Gu, Lewei Lu, Ping Luo, Dahua Lin, et al. Scene as occupancy. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8406–8415, 2023. 

- [33] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [34] Lening Wang, Wenzhao Zheng, Yilong Ren, Han Jiang, Zhiyong Cui, Haiyang Yu, and Jiwen Lu. Occsora: 4d occupancy generation models as world simulators for autonomous driving. _arXiv preprint arXiv:2405.20337_ , 2024. 

- [35] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-drive world models for autonomous driving. In _European conference on computer vision_ , pages 55–72. Springer, 2024. 

- [36] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14749–14759, 2024. 

- [37] Julong Wei, Shanshuai Yuan, Pengfei Li, Qingda Hu, Zhongxue Gan, and Wenchao Ding. Occllama: An occupancy-language-action generative world model for autonomous driving. _arXiv preprint arXiv:2409.03272_ , 2024. 

- [38] Yi Wei, Linqing Zhao, Wenzhao Zheng, Zheng Zhu, Jie Zhou, and Jiwen Lu. Surroundocc: Multicamera 3d occupancy prediction for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 21729–21740, 2023. 

- [39] Zehuan Wu, Jingcheng Ni, Xiaodong Wang, Yuxin Guo, Rui Chen, Lewei Lu, Jifeng Dai, and Yuwen Xiong. Holodrive: Holistic 2d-3d multi-modal street scene generation for autonomous driving. _arXiv preprint arXiv:2412.01407_ , 2024. 

- [40] Zhaoyang Xia, Youquan Liu, Xin Li, Xinge Zhu, Yuexin Ma, Yikang Li, Yuenan Hou, and Yu Qiao. Scpnet: Semantic scene completion on point cloud. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 17642–17651, 2023. 

- [41] Haoran Xu, Peixi Peng, Xinyi Zhang, Guang Tan, Yaokun Li, Shuaixian Wang, and Luntong Li. Exploiting continuous motion clues for vision-based occupancy prediction. In _AAAI_ , 2025. 

- [42] Jingyi Xu, Xieyuanli Chen, Junyi Ma, Jiawei Huang, Jintao Xu, Yue Wang, and Ling Pei. Spatiotemporal decoupling for efficient vision-based occupancy forecasting. _arXiv preprint arXiv:2411.14169_ , 2024. 

- [43] Tianshuo Xu, Hao Lu, Xu Yan, Yingjie Cai, Bingbing Liu, and Yingcong Chen. Occ-llm: Enhancing autonomous driving with occupancy-based large language models. In _International Conference on Robotics and Automation_ , 2025. 

- [44] Ziyang Yan, Wenzhen Dong, Yihua Shao, Yuhang Lu, Liu Haiyang, Jingwen Liu, Haozhe Wang, Zhe Wang, Yan Wang, Fabio Remondino, et al. Renderworld: World model with self-supervised 3d label. In _International Conference on Robotics and Automation_ , 2025. 

- [45] Zhenya Yang, Zhe Liu, Yuxiang Lu, Liping Hou, Chenxuan Miao, Siyi Peng, Bailan Feng, Xiang Bai, and Hengshuang Zhao. Geniedrive: Towards physics-aware driving world model with 4d occupancy guided video generation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2026. 

- [46] Yumeng Zhang, Shi Gong, Kaixin Xiong, Xiaoqing Ye, Xiao Tan, Fan Wang, Jizhou Huang, Hua Wu, and Haifeng Wang. Bevworld: A multimodal world model for autonomous driving via unified bev latent space. _arXiv preprint arXiv:2407.05679_ , 2024. 

- [47] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European conference on computer vision_ , pages 55–72. Springer, 2024. 

- [48] Tinghui Zhou, Matthew Brown, Noah Snavely, and David G Lowe. Unsupervised learning of depth and ego-motion from video. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 1851–1858, 2017. 

12 

