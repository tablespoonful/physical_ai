---
title: "DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving"
date: "2026-04-01"
authors: "Yiyao Zhu; Ying Xue; Haiming Zhang; Guangfeng Jiang; Wending Zhou; Xu Yan"
url: https://arxiv.org/abs/2604.00969
pdf: https://arxiv.org/pdf/2604.00969
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.00969)** / [論文ページ](https://arxiv.org/abs/2604.00969)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving** 

Yiyao Zhu<sup>1</sup><sup>_∗_</sup> , Ying Xue<sup>2</sup><sup>_∗_</sup> , Haiming Zhang<sup>2</sup> , Guangfeng Jiang<sup>3</sup> , Wending Zhou<sup>4</sup> , Xu Yan<sup>4✉</sup> Jiantao Gao<sup>4</sup> , Yingjie Cai<sup>4</sup> , Bingbing Liu<sup>4</sup> , Zhen Li<sup>2✉</sup> , Shaojie Shen<sup>1</sup> 1HKUST 2CUHK-SZ 3USTC 4Huawei Foundation Model Department 

yzhucp@connect.ust.hk, yanxu44@huawei.com, lizhen@cuhk.edu.cn 

## **Abstract** 

_Vision-based autonomous driving has gained much attention due to its low costs and excellent performance. Compared with dense BEV (Bird’s Eye View) or sparse query models, Gaussian-centric method is a comprehensive yet sparse representation by describing scene with 3D semantic Gaussians. In this paper, we introduce_ **_DLWM_** _, a novel paradigm with_ **_D_** _ual_ **_L_** _atent_ **_W_** _orld_ **_M_** _odels specifically designed to enable holistic gaussian-centric pretraining in autonomous driving using two stages. In the first stage, DLWM predicts 3D Gaussians from queries by selfsupervised reconstructing multi-view semantic and depth images. Equipped with fine-grained contextual features, in the second stage, two latent world models are trained separately for temporal feature learning, including Gaussianflow-guided latent prediction for downstream occupancy perception and forecasting tasks, and ego-planning-guided latent prediction for motion planning. Extensive experiments in SurroundOcc and nuScenes benchmarks demonstrate that DLWM shows significant performance gains across Gaussian-centric 3D occupancy perception, 4D occupancy forecasting and motion planning tasks._ 

## **1. Introduction** 

Recently, vision-based autonomous driving systems [8, 41, 42] have matured into a dominant paradigm that offers a cost-effective and scalable alternative to multi-sensor fusion approaches. This system leverages advanced deep learning and is compatible with multi-task heads, maintaining accurate scene understanding and safe motion planning [14, 15]. A foundational challenge in achieving robust autonomy is developing a scene representation that is simultaneously expressive, efficient, and temporally coherent for perception, 

> * Equal contribution. 

> ✉ Corresponding authors. 


Figure 1. **Illustration of our DLWM for pre-training and performance improvements for downstream tasks** . 

forecasting, and planning tasks. 

Early approaches primarily relied on dense or coarse representations: Voxel-based [57] methods use 3D voxel grids to represent the surroundings, offering detailed geometric information at the cost of computational overhead. BEVbased methods [10, 23] squeeze multi-view features into a 2D plane; follow-up sparse-query [25, 26] approaches replace the grid with a handful of sparse queries (e.g., instance boxes, map elements). Despite their relative efficiency, these approaches either sacrifice vertical detail and dense geometry or leave the decision module with only coarse scene knowledge. To overcome these limitations, the research moves to Gaussian-centric representation [13, 54]. A set of 3D semantic Gaussians provides a comprehensive yet sparse representation, offering an optimal balance of detail and efficiency. 

Although Gaussian-centric representations have demon- 

1 

strated significant potential, their reliance on extensive manual annotations hinders scalable deployment. The recent pre-training paradigms utilizing unlabeled data offer a promising solution. For instance, self-supervised approaches like Masked Autoencoders (MAE) [29] apply contrastive learning for pre-training, but fail to explicitly learn the 3D geometric structures due to rely on coarse supervision. Recently, to learn a complete geometric representation, rendering-based methods such as UniPAD [44] and ViDAR [45] utilize LiDAR depth to supervise voxel rendering. In contrast, recent GaussianFlowOcc [1] and SQS [50] show that 3D Gaussians alone can be learned from unlabeled videos through differentiable RGB/depth rendering. Still, a comprehensive self-supervised pre-training strategy tailored for the full lifecycle of Gaussian-centric models remains largely unexplored. 

Building upon the necessity of robust feature learning, temporal prediction becomes the next challenge for highlevel scene evolution. Latent world model [22] has emerged as a key approach to unsupervised temporal modeling. It bypasses explicit image or occupancy generation and forecasts future dynamics directly in a compact latent space. Currently, the latent world model has been developed for motion planning [33], but it has rarely been explored for other critical tasks such as perception [13] and forecasting [48, 58], let alone being integrated with Gaussiancentric models. 

This integration, however, presents a fundamental technical challenge regarding the selection of latent representations. Since Gaussian queries are initialized independently for the current frame and future frames, they lack a oneto-one correspondence [4]. Consequently, the permutation equivalence of Gaussian queries renders direct supervision of Gaussian query features between two frames impossible [13]. Fortunately, 3D Gaussian Splatting (3DGS) possesses arbitrary view rendering capabilities. BEV rasterization [27] derived from sparse Gaussian queries, as a dense grid representation, preserves height information by vertical stacking [27] and allows for clear inter-frame regional correspondence. Thus, we select BEV features as the most suitable latent representation for temporal supervision. 

To bridge this gap and fully leverage the benefits of both Gaussian-centric representation and latent world models, we introduce **DLWM** , a novel holistic pre-training paradigm with **D** ual **L** atent **W** orld **M** odels as shown in Fig. 1. DLWM utilizes a two-stage approach to unify spatiotemporal Gaussian representation learning, improving all downstream tasks without pre-training (i.e., +1.02 mIoU on occupancy perception, +2.68 mIoU on occupancy forecasting, and -16% L2 error on motion planning as Fig. 1). Specifically, in the first stage, we reconstruct semantic and depth maps for learning Gaussian context. With the pre-trained weights, in the second stage, dual latent world 

models are utilized separately for pre-training. The first one guided by Gaussian flow is specifically designed for downstream 3D occupancy perception and 4D occupancy forecasting tasks. Another latent world model based on predicted ego trajectory is used for improving motion planning. 

To summarize, we list the contributions of this paper as follows: 

- We propose **DLWM** , a self-supervised paradigm for holistic gaussian-centric pre-training, which includes the unified first stage for learning gaussian-centric geometric and semantic representation, followed by training dual latent world model separately in the second stage. 

- We introduce a latent world model guided by gaussian flow and ego motion alignment to learn spatiotemporal gaussian feature representation, specifically designed for downstream occupancy perception and forecasting tasks. 

- We design another latent world model guided by the current Gaussian latent and predicted ego trajectory, jointly improving temporal Gaussian-centric representation and ego trajectory planning. 

- DLWM significantly enhances performance in gaussiancentric occupancy perception, forecasting, and planning tasks, achieving state-of-the-art results on SurroundOcc and nuScenes benchmarks. 

## **2. Related Work** 

### **2.1. World Models in Autonomous Driving** 

World models for autonomous driving are primarily categorized based on their scene representation: 2D imagebased versus 3D geometry-based approaches. 2D imagebased world models focus on visual generation. Early efforts like GAIA-1 [5] generated single-view videos. Later research, such as DriveDreamer [36] and Drive-WM [37], further enhanced multi-view consistency and temporal coherence. 3D geometry-based world models focus on spatial dynamics using 4D occupancy forecasting. OccWorld [52] and DriveWorld [30] set baselines by predicting future scenes and ego states. RenderWorld [43] designs a more effective VAE for occupancy reconstruction. GaussianWorld [60] innovates by modeling scene evolution in a 3D Gaussian space, enhancing perception with scene priors. WPT [16] enables policy distillation under the world model. 

More recently, latent-based world models [22, 33, 55] take a different approach by bypassing explicit image or occupancy forecasting, predicting future dynamics directly in a compressed latent space. To the best of our knowledge, the utilization of latent world model for perception and forecasting tasks remain largely unexplored. 

### **2.2. Pre-training in Autonomous Driving** 

Pre-training has been a pivotal strategy in autonomous driving, enabling models to learn robust representations 

2 


Figure 2. **Overall pipeline of DLWM.** Stage 1 (Sec. 3.1) focuses on learning robust 3D Gaussian scene representations from multi-view videos using self-supervised reconstruction on depth and semantic maps. Stage 2 introduces dual latent world models. a. Gaussianflow-guided model (Sec. 3.2) explicitly predicts 3D Gaussian flow, propagating the current Gaussian states to the future frame for latent prediction. b. Ego-planning-guided model (Sec. 3.3) conditions the future scene forecasting on the predicted ego trajectory. All predicted latents are supervised by the perceived features from next multi-view image using a frozen Gaussian perception module. 

from extensive datasets. Particularly, rendering-based pretraining enforces the model to learn physical priors. UniPAD [44] and MIM4D [59] use masked multi-view images and volume rendering for detailed geometric learning. ViDAR [45] predicts future point clouds from past images, while VisionPAD [49] uses image supervision to learn geometry and motion. More recently, SQS [50] introduces a novel pre-training approach tailored for sparse perception models. While various pre-training strategies have improved the foundation of vision-based systems, selfsupervised pre-training tailored for full life-cycle Gaussiancentric tasks has yet to be addressed. 

### **2.3. 3D Gaussian Splatting in Autonomous Driving** 

3D Gaussian Splatting (3DGS) further advances explicit scene representation in autonomous driving. The explicit and parameter-efficient nature of 3DGS has been effectively utilized for high-fidelity driving scene reconstruction [38, 56]. More recently, models like GaussianAD [54] and Gaussianformer [13] adopted 3DGS for geometric reasoning in tasks like occupancy prediction. Beyond direct perception, 3DGS is increasingly used as a self-supervision representation. GaussianFlowOcc [1] predicts temporal flow of each Gaussian, effectively learning 4D movement. GaussTR [17] enhances self-supervised understanding by aligning Gaussian representations with 2D models. SQS [50] enhances sparse perception models by predicting 

3D Gaussians for multi-view reconstruction. 

## **3. Methodology** 

We propose DLWM, a two-stage paradigm for holistic Gaussian-centric pre-training as shown in Fig. 2. In Sec. 3.1, we present the first stage, which focuses on Gaussian representation learning through the reconstruction of multiview depth and semantic images. Building upon the pretrained Gaussian perception module from the first stage, Sec. 3.2 describes a latent world model guided by Gaussian flow pre-trained for downstream tasks such as occupancy perception and forecasting. Subsequently, Sec. 3.3 introduces a separate latent world model in the second stage, dedicated to ego-motion planning, which is trained independently while leveraging the pre-trained perceptual representations from the first stage. 

### **3.1. Gaussian Representation Learning** 

**Preliminaries.** 3D Gaussian Splatting (3DGS) [18] represents a scene as a collection of _K_ 3D Gaussian ellipsoids. Each primitive _gk_ is specified by a three-dimensional center _µk ∈_ R<sup>3</sup> , a covariance **Σ** _k_ , an opacity _αk ∈_ [0 _,_ 1], and a set of spherical harmonic (SH) coefficients _ck ∈_ R<sup>_k_</sup> . Therefore, the Gaussian distribution at point _x_ is represented as: 


3 

Here, the covariance is parameterized via a scale–rotation factorization **Σ** = **RSS**<sup>_T_</sup> **R**<sup>_T_</sup> , where **S** _∈_ R<sup>3</sup> +<sup>denotesthe</sup> scaling factors, **R** _∈ SO_ (3) is the rotation matrix, parameterized as a quaternion. 

When rendering, we aggregate the contributions of the Gaussians in a depth-ordered fashion via an alpha-blending procedure [28]. The rendering pipeline can be readily adapted to facilitate the retrieval of geometric and semantic information, via: 


where **D** and **S** represent the accumulated depth and semantic logits, respectively. _di_ denotes the distance from the _i_ -th Gaussian to the camera. 

**Gaussians From Images.** Existing dense 3D voxel representations suffer from high overhead and poor resource allocation. We address this by adopting a sparse, explicit representation based on 3D semantic Gaussians, following the design of GaussianFormer [13]. Each Gaussian query is a sparse, learnable vector used to predict its mean, covariance, opacity and semantic logits. 

We introduce the details of the Gaussian perception module in Fig. 2. At each timestep, we first feed multi-view images through an Image Encoder, which consists of a backbone network (e.g., ResNet101) and a Feature Pyramid Network (FPN), to extract multi-level features. A Gaussian encoder then refines the features block-by-block. Each Gaussian block has three parts: 1) a self-encoding module for Gaussian–to-Gaussian interaction. This interaction captures the relations of Gaussians within the current frame as well as their temporal propagation from the previous frame through a 4D Sparse Convolution module. 2) an image cross-attention module that aggregates current visual information for deformable feature sampling with camera intrinsics and extrinsics, and 3) a refinement module that adjusts Gaussian attributes. These queries are transformed into a set of fine-grained Gaussians, and propagated to future timesteps in a streaming fashion. 

**Reconstruction Loss for the First Stage.** The first stage is trained via self-supervision, compelling the predicted 3D Gaussians to reconstruct depth and semantic maps. We compute the depth loss _Ld_ only at pixels with valid LiDAR data, which serves as the ground truth for depth. Given the sparsity of LiDAR-based depth supervision, we leverage perceptual pseudo-depth generated by Metric3D [46] as a dense supervisory signal for loss item _Lpd_ . The semantic labels are automatically generated using foundation models Grounded SAM [32]. The overall loss is a combination of 

L1 Loss on depth and cross-entropy loss on semantics without any human label: 


where _ω_ 1, _ω_ 2 and _ω_ 3 are set to 1.0, 0.05 and 1.0 respectively. 

### **3.2. Latent World Model Guided by Gaussian Flow** 

For the second stage, given the pre-trained gaussian perception weights in the first stage, we design a latent world model guided by Gaussian flow indicated with blue arrows in Fig. 2. In the end, the pre-trained perception model with enhanced spatiotemporal representation is prepared for improving the performance of downstream 3D occupancy perception and 4D occupancy forecasting tasks. **Gaussian Flow Prediction.** Our primary task is to ef- 

ficiently predict the motion of 3D Gaussians within the scene. It begins by feeding the current perceived Gaussian query features into a flow prediction head. This network is tasked with estimating a local, dynamic displacement vector for each Gaussian. The estimated dynamic displacement, termed the Gaussian flow, will be propagated to the next frame via ego motion alignment: 


where _µ_<sup>_t_</sup> _k_<sup>_∈_R3and</sup><sup>_µt_</sup> _k_<sup>+1</sup> _∈_ R<sup>3</sup> are the mean of each Gaussian in the current ego frame _t_ and next _t_ + 1 respectively, **∆** _µ_<sup>_t_</sup> _k_<sup>isthepredictedGaussianflow,and</sup><sup>**T**</sup><sup>_t_</sup> _ego_<sup>_→t_+1</sup> _∈_ R<sup>4</sup><sup>_×_4</sup> is the coordinate transformation from the current frame to the next frame. 

Similar to the reconstruction loss Eq. 4 in the first stage, the predicted 3D Gaussians are supervised by rendering depth and semantic images for the next frame. 

**Future Latent Prediction.** The next step is to convert the predicted 3D scene into a compact latent representation. After moving and transforming current 3D Gaussians to the next frame, we take the resulted 3D Gaussian set as input, and all other attributes maintain consistency with the current frame. Motivated by GaussianLSS [27], we perform BEV rasterization to project and rasterize feature of each Gaussian query onto a 2D BEV plane, as the predicted latent in the world model. 

**Future Latent Supervision.** We utilize a **L2** loss to supervise the propagated and rasterized future BEV latent feature _B_ ˆ _t_ +1 against the corresponding ground-truth BEV feature _Bt_ +1, which is defined as the BEV reconstruction loss _Lbev_ : 


The ground-truth BEV feature _Bt_ +1 is generated by feeding multi-view image at time _t_ +1 into the frozen Gaussian perception module, as shown in the rightmost of Fig. 2. The resulting 3D Gaussians are then rendered and rasterized to produce the true future latent _Bt_ +1. Minimizing 

4 


Figure 3. **4D occupancy forecasting in a stream manner.** We transform current 3D Gaussians to the next frame with ego motion alignment and complete new area with random Gaussians. 

_Lbev_ compels the prediction framework to generate a future scene representation that is both geometrically and semantically consistent with the true future state. 

**3D Occupancy Perception.** Regarding 3D occupancy perception task, we design a baseline model with the Gaussian perception module in Sec. 3.1 to obtain current 3D Gaussians, followed by Gaussian-to-Occupancy Splatting [13] for occupancy prediction. 

After the two-stage pre-training, during the fine-tuning stage, we load the pre-trained Gaussian perception module for downstream 3D occupancy perception task. More details can be referred to GaussianFormer [13] about prediction head and training loss. 

**4D Occupancy Forecasting.** Another downstream task is 4D occupancy forecasting. We design a simple model for stream occupancy forecasting based on Gaussian-centric representation. Motivated by GaussianWorld [60], as illustrated in Fig. 3, the future occupancy is forecast in an autoregressive manner using three key steps, including aligning static scenes, moving dynamic objects and completing of new areas. Concretely, we first obtain the current 3D Gaussians perceived from multi-view videos using Gaussian perception module in Sec. 3.1. We then align current 3D Gaussians to the next frame based on the ego trajectory. Meanwhile, the newly-observed areas are completed with random Gaussians, facilitating the imagination of these new areas. We employ 3D sparse convolution followed by refinement layers to simultaneously model the current Gaussians and the newly-completed Gaussians. Finally, we utilize all refined Gaussians to predict occupancy in the next frame using Gaussian-to-Occupancy Splatting [13]. We forecast all future occupancy in an autoregressive manner, and each frame follows the pipeline mentioned above. 

During the fine-tuning stage, we load the pre-trained weights from two-stage (Sec. 3.1 and Sec. 3.2) pre-training for Gaussian perception module, followed by further training stream 4D occupancy forecasting. 

### **3.3. Latent World Model Guided by Ego Planning** 

Based on the first stage in Sec. 3.1, another latent world model in the second stage focuses on predicting future scene features optimized for motion planning. As the orange arrows shown in Fig. 2, this world model is trained independently with the model in Sec. 3.2. Motivated by LAW [22] and SSR [20], we design a forecasting module that uses the predicted trajectory to condition the future latent scene representation, providing motion-aware context for planning. **Current Latent Construction.** To provide the planning head with a comprehensive, structured, and temporally relevant context, we first transform the current frame’s sparse Gaussian features into a dense latent BEV feature via rasterization (as described in Sec. 3.2). To reduce computational load, we extract scene queries **Q**<sup>_t_</sup> scene<sup>from BEV feature fol-</sup> lowing [20]. Next these queries interact via self-attention to capture the spatial relationships and global context of the BEV scene. These contextualized **Q**<sup>_t_</sup> scene<sup>thenserveasthe</sup> key/value for the waypoint queries **Q** wp, coupling the scene perception with the trajectory prediction task. 

**Motion Planning.** The objective is to predict the optimal ego trajectory over a future time horizon. The planning head is instantiated by a set of waypoint queries **Q** wp. These queries interact with the scene features **Q**<sup>_t_</sup> scene<sup>viacross-</sup> attention to generate the trajectory **T**<sup>**ˆ**</sup> through a MLP head for imitation learning with regression: 


**Future Latent Prediction.** The core of future prediction is generating the next frame’s scene queries **Q**<sup>_t_</sup> scene<sup>+1.</sup> We achieve this by conditioning the current scene queries **Q**<sup>_t_</sup> scene on the predicted trajectory **T**<sup>**ˆ**</sup> using a specialized MotionAware Layer Normalization (MLN) [34] layer; the action **ˆT** directly modulates **Q**<sup>_t_</sup> scene<sup>’snormalizationparameters.</sup> We predict the next **Q**<sup>_t_</sup> scene<sup>+1bymulti-layerself-attentionon</sup> motion-aware **Q**<sup>_t_</sup> scene<sup>.Finally, motivated by [20], predicted</sup> scene queries are fused with the current latent BEV feature **B** _t_ to yield the predicted latent BEV _B_<sup>ˆ</sup> _t_ +1 with BEV reconstruction loss _Lbev_ in Eq. 6. 

**Total Loss for Motion Planning.** The final losses for motion planning consist of the imitation learning regression loss and the BEV reconstruction loss: 


## **4. Experiments** 

### **4.1. Datasets** 

We evaluate our DLWM using the widely recognized nuScenes [2] dataset, which comprises 1000 driving sequences. Each sequence contains 20 seconds of video captured by both RGB and LiDAR sensors. The data is 

5 

Table 1. **3D occupancy perception results on the SurroundOcc-nuScenes validation set [39].** *: We re-evaluate the checkpoints released by GaussianWorld because they repeatedly calculated the metrics for intermediate time-interval frames within each video. 

|Method|IoU<br>|mIoU|■barrier|■bicycle|■bus|■car|■const. veh.|■motorcycle|■pedestrian|■traffic cone|■trailer|■truck|■drive. suf.|■other flat|■sidewalk|■terrain|■manmade|■vegetation|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|MonoScene [3]|23.96|7.31|4.03|0.35|8.00|8.04|2.90|0.28|1.16|0.67|4.01|4.35|27.72|5.20|15.13|11.29|9.03|14.86|
|Atlas [31]|28.66|15.00|10.64|5.68|19.66|24.94|8.90|8.84|6.47|3.28|10.42|16.21|34.86|15.46|21.89|20.95|11.21|20.54|
|BEVFormer [23]|30.50|16.75|14.22|6.58|23.46|28.28|8.66|10.77|6.64|4.05|11.20|17.78|37.28|18.00|22.88|22.17|13.80|22.21|
|TPVFormer [11]|30.86|17.10|15.96|5.31|23.86|27.32|9.79|8.74|7.09|5.20|10.97|19.22|38.87|21.25|24.26|23.15|11.73|20.81|
|OccFormer [51]|31.39|19.03|18.65|10.41|23.92|30.29|10.31|14.19|13.59|10.13|12.49|20.77|38.78|19.79|24.19|22.21|13.48|21.35|
|SurroundOcc [39]|31.49|20.30|20.59|11.68|28.06|30.86|10.70|15.14|14.09|12.06|14.38|22.26|37.29|23.70|24.49|22.77|14.89|21.86|
|GaussianFormer [13]|29.83|19.10|19.52|11.26|26.11|29.78|10.47|13.83|12.58|8.67|12.74|21.57|39.63|23.28|24.46|22.99|9.59|19.12|
|GaussianFormer-2 [12]|31.74|20.82|21.39|13.44|28.49|30.82|10.92|15.84|13.55|10.53|14.04|22.92|40.61|24.36|26.08|24.27|13.83|21.98|
|GaussianWorld* [60]|32.77|21.79|21.61|13.30|27.28|31.21|13.89|16.91|13.28|11.77|14.82|23.66|41.91|24.31|28.35|26.32|15.67|24.54|
|**Baseline**<br>**DLWM (ours)**|31.77 <br>**34.61 **|20.83<br>**21.85**|21.17 <br>21.71|13.82 <br> 13.56|26.74 <br> 27.65|31.95 <br> 31.22|10.90 <br> 12.50|16.03 <br> 16.93|13.94 <br> 12.35|10.87 <br> 11.42|13.44 <br> 13.96|22.52 <br> 24.12|40.79 <br> 42.27|24.28 <br> 24.94|26.06 <br> 27.39|24.13 <br> 26.36|14.05 <br> 16.61|22.55<br> 26.64|


Table 2. **4D occupancy forecasting results on the SurroundOcc-nuScenes validation set [39].** Aux. Sup. represents auxiliary supervision. Avg. computes the average result of 1s, 2s, and 3s. 

|Method|Input|Aux. Sup.||mI<br>|oU (%) <br>|_↑_<br>|||I<br>|oU (%) <br>|_↑_<br>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||0s|1s|2s|3s|Avg.|0s|1s|2s|3s|Avg.|
|Copy&Paste|3D-Occ|None|66.38|14.91|10.54|8.52|11.33|62.29|24.47|19.77|17.31|20.52|
|OccWorld-O [52]|3D-Occ|None|**66.38**|**25.78**|15.14|10.51|17.14|**62.29**|**34.63**|25.07|20.18|26.63|
|OccWorld-T [52]|Camera|Semantic LiDAR|7.21|4.68|3.36|2.63|3.56|10.66|9.32|8.23|7.47|8.34|
|OccWorld-S [52]|Camera|None|0.27|0.28|0.26|0.24|0.26|4.32|5.05|5.01|4.95|5.00|
|OccWorld-D [52]|Camera|3D-Occ|18.63|11.55|8.10|6.22|8.62|22.88|18.90|16.26|14.43|16.53|
|PreWorld [21]|Camera|2D Labels & 3D-Occ|-|12.27|9.24|7.15|9.55|-|23.62|21.62|19.63|21.62|
|**Baseline**|Camera|3D-Occ|21.12|18.18|15.11|11.97|15.09|32.12|29.98|25.43|21.55|25.65|
|**DLWM (ours)**|Camera|3D-Occ|22.21|19.66|**17.79**|**15.87**|**17.77**|33.47|32.63|**30.68**|**28.49**|**30.60**|


recorded at a rate of 20Hz with keyframes at 2Hz. To facilitate evaluation on 3D scene perception and forecasting, we incorporate SurroundOcc [39] with 3D semantic occupancy annotations based on nuScenes. Each voxel in the dataset is labeled with one of 18 categories, consisting of 16 semantic classes, 1 empty class, and 1 unknown class. 

### **4.2. Evaluation Metrics** 

For evaluation, we assess the performance of our model across perception, forecasting, and planning tasks. For perception, the quality of semantic occupancy prediction is evaluated using the mean Intersection-over-Union (mIoU) and Intersection-over-Union (IoU) metrics. For the forecasting task, we adopt the same mIoU and IoU metrics to evaluate the model’s ability to predict future 3D occupancy grids within the next 3 seconds. For the planning task, we 

evaluate the predicted ego-vehicle trajectories using the L2 error and collision rate, which quantify the accuracy and safety of the generated motion plans. 

### **4.3. Implementation Details** 

We utilize a ResNet101-DCN backbone, initialized from an FCOS3D [35] checkpoint, as the image encoder. Feature extraction is performed using a Feature Pyramid Network (FPN) with downsampled scales of 4, 8, 16, and 32. We set the Gaussian counts to 25,600 and apply four transformer layers to enhance Gaussian attributes for each frame. The model is trained using the AdamW optimizer with a weight decay of 0.01. The learning rate warms up linearly to 4e-4 over the first 500 steps, followed by a cosine decay schedule. Regarding to the pre-training, the first stage is trained for 12 epochs with a batch size of 16. After that, we 

6 

Table 3. **Motion Planning Results on the nuScenes validation set.** The metrics are computed by the way in VAD [15]. _⋄_ : Lidar-based methods. We do not utilize ego status in the planning module. 

|Method|Aux. Task||L2 (|m)_↓_||Col|lision|Rate (|%)_↓_|
|---|---|---|---|---|---|---|---|---|---|
|||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|NMP_⋄_[47]|Det & Motion|0.53|1.25|2.67|1.48|**0.04**|0.12|0.87|0.34|
|FF_⋄_[6]|FreeSpace|0.55|1.20|2.54|1.43|0.06|0.17|1.07|0.43|
|EO_⋄_[19]|FreeSpace|0.67|1.36|2.78|1.60|**0.04**|0.09|0.88|0.33|
|ST-P3 [7]|Det & Map & Depth|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|
|UniAD [9]|Det&Track&Map&Motion&Occ|0.44|0.67|0.96|0.69|**0.04**|**0.08**|**0.23**|**0.12**|
|VAD-Tiny [15]|Det & Map & Motion|0.46|0.76|1.12|0.78|0.21|0.35|0.58|0.38|
|VAD-Base [15]|Det & Map & Motion|0.41|0.70|1.05|0.72|0.07|0.17|0.41|0.22|
|PARA-Drive [40]|Det&Track&Map&Motion&Occ|0.25|0.46|0.74|0.48|0.14|0.23|0.39|0.25|
|GenAD [53]|Det & Map & Motion|0.28|0.49|0.78|0.52|0.08|0.14|0.34|0.19|
|OccWorld [52]|3D-Occ|0.39|0.73|1.18|0.77|0.11|0.19|0.67|0.32|
|BEV-Planner [24]|None|0.28|**0.42**|**0.68**|**0.46**|**0.04**|0.37|1.07|0.49|
|LAW [22]|None|0.26|0.57|1.01|0.61|0.14|0.21|0.54|0.30|
|**Baseline**|None|0.27|0.51|0.87|0.55|0.11|0.17|0.46|0.24|
|**DLWM (ours)**|None|**0.21**|0.43|0.76|**0.46**|0.11|0.14|0.32|0.19|


further pre-train the perception module using latent world model guided by Gaussian flow with the same training setting. For the fine-tuning, we train our models for 20 epochs for both occupancy perception and forecasting by loading the pre-trained weights, with a batch size of 16. Based on the same first stage, another latent world model guided by ego-planning is trained for 20 epochs in the second stage for the final planning results via temporal learning. 

### **4.4. Main Results** 

We evaluate the effectiveness of DLWM on three challenging downstream tasks: 3D occupancy perception, 4D occupancy forecasting, and motion planning. More visualization results are shown in the supplementary material. **3D Occupancy Perception.** Tab. 1 compares 3D semantic occupancy results on the nuScenes validation set with SurroundOcc labels. Without pre-training, our baseline model yields 20.83 mIoU and 31.77 IoU. After two-stage pretraining, the model (ours) rises to 21.85 mIoU and 34.61 IoU, achieving SOTA and outperforming the model without pre-training by 1.02 mIoU and 2.84 IoU. The results demonstrate the benefit of our pre-training strategy. 

**4D Occupancy Forecasting.** Tab. 2 summarizes the 4D occupancy forecasting results on the nuScenes validation set. We evaluate two variants: Baseline (without pre-training) and DLWM (with two-stage pre-training). The benchmark include Copy&Paste, OccWorld-O/T/S/D [52]. The Baseline already surpasses all OccWorld variants, yielding 15.09 mIoU and 25.65 IoU averaged over 1–3 s. After pre-training, our approach establishes a new state-of-the-art 

with an average 17.77 mIoU and 30.60 IoU, outperforming 3D-Occ input method OccWorld-O. The consistent gains confirm the superiority of our pre-trained world model on the 4D occupancy forecasting task. 

**Motion Planning.** We evaluate our DLWM on the nuScenes motion planning task, measuring performance via L2 distance and collision rate over a 3-second horizon (Tab. 3). Our method achieves an average L2 distance of 0.46m, tying for the best score with BEV-Planner and surpassing dedicated world models like LAW (L2: 0.61m). Compared with UniAD with multiple auxillary tasks, our method achieves a better L2 score with comparable collision avoidance, confirming that the designed latent world model is highly effective. Furthermore, our two-stage selfsupervised pre-training yields a substantial 0.09m improvement in L2 distance (from 0.55m to 0.46m) over the baseline without pre-training. 

### **4.5. Ablation Study** 

In this section, we maintain a consistent data scale to ensure fair comparison. Specifically, we utilize half of the training data during the two-stage pre-training and a quarter for occupancy prediction during the fine-tuning stage, while all training data are used for planning. 

**Rendering Objectives.** To investigate the impact of various rendering objectives in Stage 1, we conduct an ablation study from Exp1 to Exp3 in Tab. 4. Starting with the sparse LiDAR depth supervision (Sup- _DL_ , Exp1, mIoU 18.40), we observe cumulative gains from introducing denser signals (Sup- _D_ , Exp2) with mIoU to 18.74, confirming the 

7 

Table 4. **Ablation study on render supervision and latent world model guided by Gaussian flow.** “Sup- _DL_ ”: sparse depth supervision derived from LiDAR points. “Sup- _D_ ”: dense pseudo-depth map supervision. “Sup- _S_ ”: semantics supervision. “Gaussian Flow”: denotes the inclusion of the Stage 2 latent world model guided by Gaussian flow. 

|Exp.||Settings||Perc|eption|
|---|---|---|---|---|---|
||Sup-_DL_|Sup-_D_<br>Sup-_S_|Gaussian Flow|IoU (%)_↑_|mIoU (%)_↑_|
|Exp1|✓|||18.40|29.83|
|Exp2|✓|✓||18.74|30.05|
|Exp3|✓|✓<br>✓||18.99|30.23|
|Exp4|✓|✓<br>✓|✓|**19.30**|**30.56**|


Table 5. **Ablation study on latent world model guided by ego planning.** Latent BEV: planning with latent BEV rendered from 3D Gaussians. BEV Forecasting: future latent BEV forecasting integrated into planning. Stage-1 Pretrain: image reconstruction. 

|Exp.||Settings|||L2 (|m)_↓_|||Col.|(%)_↓_||
|---|---|---|---|---|---|---|---|---|---|---|---|
||Latent BEV|BEV Forecast|Stage-1 Pre-train|1s|2s|3s|Avg|1s|2s|3s|Avg|
|Exp1||||0.27|0.51|0.87|0.55|0.11|0.17|0.46|0.24|
|Exp2|✓|||0.26|0.48|0.82|0.52|0.12|0.16|0.38|0.22|
|Exp3|✓|✓||0.23|0.47|0.81|0.50|**0.10**|**0.13**|0.36|0.20|
|Exp4|✓|✓|✓|**0.21**|**0.43**|**0.76**|**0.46**|0.11|0.14|**0.32**|**0.19**|


Table 6. **Ablation study on data scale.** 3D occupancy perception performance under different pre-training data scales. 

|Dataset fraction|mIoU (%)_↑_|IoU (%)_↑_|
|---|---|---|
|10%|18.24|28.59|
|50%|19.30|30.56|
|100%|**19.98**|**31.17**|


value of dense geometric supervision. Further incorporating semantic supervision (Sup- _S_ , Exp3) yields additional gains, reaching 18.99 mIoU and 30.23 IoU. 

**Latent World Model Guided by Gaussian Flow.** We evaluate the contribution of the Gaussian-flow-guided latent world model (Stage 2) for temporal feature learning in Tab. 4 Exp4. By enabling the Gaussian flow module, the final 3D occupancy performance sees a significant boost, achieving a peak 19.30 mIoU and 30.56 IoU. It indicates that Stage 2 Gaussian-flow-guided latent forecasting is crucial for injecting spatio-temporal coherence and predictability into the Gaussian features. 

**Latent World Model Guided by Ego Trajectory.** We conduct detailed ablation studies (Tab. 5) to validate the effectiveness of our motion planning components. Comparing Exp1 (raw Gaussian features) against Exp2 (current latent BEV feature) demonstrates that the rasterized BEV latent representation is superior for the planning head, reducing the average L2 distance from 0.55m to 0.52m and collision rate from 0.24 to 0.21. Integrating future BEV forecasting (Exp3), even without pre-training, significantly improves performance. The most substantial gain is achieved by in- 

corporating the Stage 1 reconstruction pre-training (Exp4, our final method). This pre-training ensures Gaussian features are initialized with rich geometric priors for more accurate scene modeling. As a result, Exp4 achieves the best overall performance, reducing the average L2 distance further to 0.46m and the average collision rate to 0.19. 

**Data Scaling.** We investigate the impact of the data scale of two-stage self-supervised pre-training on the downstream occupancy perception. We vary the proportion of data used for the pre-training between 10%, 50%, and 100% of training data. As shown in Tab. 6, performance scales positively with data size. Utilizing the full 100% of the training set yields the best result, achieving a peak mIoU of 19.98 and IoU of 31.17. This confirms that our pre-training leverages unlabeled data to reinforce the geometric and semantic priors of the Gaussians with temporal coherence. 

## **5. Conclusion** 

In this work, we propose DLWM (Dual Latent World Models), a novel two-stage self-supervised pre-training paradigm designed for Gaussian-centric representation for vision-based autonomous driving. DLWM improves sparse query learning and temporal coherence by establishing a two-stage process: Stage 1 focuses on geometric and semantic feature learning via diverse rendering objectives. Stage 2 introduces our dual latent world models including Gaussian-flow-guided and ego-planning-guided latent forecasting. DLWM achieves state-of-the-art results on occupancy perception, forecasting and motion planning tasks, confirming the essential, scalable contribution of our holistic Gaussian-centric pre-training framework. 

8 

## **References** 

- [1] Simon Boeder, Fabian Gigengack, and Benjamin Risse. Gaussianflowocc: Sparse and weakly supervised occupancy estimation using gaussian splatting and temporal flow. _arXiv preprint arXiv:2502.17288_ , 2025. 2, 3 

- [2] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11621–11631, 2020. 5 

- [3] Anh-Quan Cao and Raoul De Charette. Monoscene: Monocular 3d semantic scene completion. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 3991–4001, 2022. 6 

- [4] Wanshui Gan, Fang Liu, Hongbin Xu, Ningkai Mo, and Naoto Yokoya. Gaussianocc: Fully self-supervised and efficient 3d occupancy estimation with gaussian splatting. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 28980–28990, 2025. 2 

- [5] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 2 

- [6] Peiyun Hu, Aaron Huang, John Dolan, David Held, and Deva Ramanan. Safe local motion planning with selfsupervised freespace forecasting. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 12732–12741, 2021. 7 

- [7] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _European Conference on Computer Vision_ , pages 533–549. Springer, 2022. 7 

- [8] Tianshuai Hu, Xiaolu Liu, Song Wang, Yiyao Zhu, Ao Liang, Lingdong Kong, Guoyang Zhao, Zeying Gong, Jun Cen, Zhiyu Huang, et al. Vision-language-action models for autonomous driving: Past, present, and future. _arXiv preprint arXiv:2512.16760_ , 2025. 1 

- [9] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17853–17862, 2023. 7 

- [10] Junjie Huang, Guan Huang, Zheng Zhu, Yun Ye, and Dalong Du. Bevdet: High-performance multi-camera 3d object detection in bird-eye-view. _arXiv preprint arXiv:2112.11790_ , 2021. 1 

- [11] Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. Tri-perspective view for visionbased 3d semantic occupancy prediction. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9223–9232, 2023. 6 

- [12] Yuanhui Huang, Amonnut Thammatadatrakoon, Wenzhao Zheng, Yunpeng Zhang, Dalong Du, and Jiwen Lu. Prob- 

   - abilistic gaussian superposition for efficient 3d occupancy prediction. _arXiv preprint arXiv:2412.04384_ , 2024. 6 

- [13] Yuanhui Huang, Wenzhao Zheng, Yunpeng Zhang, Jie Zhou, and Jiwen Lu. Gaussianformer: Scene as gaussians for vision-based 3d semantic occupancy prediction. In _European Conference on Computer Vision_ , pages 376–393. Springer, 2024. 1, 2, 3, 4, 5, 6 

- [14] Xiaosong Jia, Yulu Gao, Li Chen, Junchi Yan, Patrick Langechuan Liu, and Hongyang Li. Driveadapter: Breaking the coupling barrier of perception and planning in end-to-end autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 7953–7963, 2023. 1 

- [15] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8340–8350, 2023. 1, 7 

- [16] Guangfeng Jiang, Yueru Luo, Jun Liu, Yi Huang, Yiyao Zhu, Zhan Qu, Dave Zhenyu Chen, Bingbing Liu, and Xu Yan. Wpt: World-to-policy transfer via online world model distillation. _arXiv preprint arXiv:2511.20095_ , 2025. 2 

- [17] Haoyi Jiang, Liu Liu, Tianheng Cheng, Xinjie Wang, Tianwei Lin, Zhizhong Su, Wenyu Liu, and Xinggang Wang. Gausstr: Foundation model-aligned gaussian transformer for self-supervised 3d spatial understanding. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11960–11970, 2025. 3 

- [18] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Transactions on Graphics_ , 42 (4):1–14, 2023. 3 

- [19] Tarasha Khurana, Peiyun Hu, Achal Dave, Jason Ziglar, David Held, and Deva Ramanan. Differentiable raycasting for self-supervised occupancy forecasting. In _European Conference on Computer Vision_ , pages 353–369. Springer, 2022. 7 

- [20] Peidong Li and Dixiao Cui. Navigation-guided sparse scene representation for end-to-end autonomous driving. _arXiv preprint arXiv:2409.18341_ , 2024. 5, 2 

- [21] Xiang Li, Pengfei Li, Yupeng Zheng, Wei Sun, Yan Wang, and Yilun Chen. Semi-supervised vision-centric 3d occupancy world model for autonomous driving. _arXiv preprint arXiv:2502.07309_ , 2025. 6 

- [22] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. _arXiv preprint arXiv:2406.08481_ , 2024. 2, 5, 7 

- [23] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Yu Qiao, and Jifeng Dai. Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers. In _European Conference on Computer Vision_ , pages 1–18. Springer, 2022. 1, 6 

- [24] Zhiqi Li, Zhiding Yu, Shiyi Lan, Jiahan Li, Jan Kautz, Tong Lu, and Jose M Alvarez. Is ego status all you need for openloop end-to-end autonomous driving? In _Proceedings of_ 

9 

_the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14864–14873, 2024. 7 

- [25] Xuewu Lin, Tianwei Lin, Zixiang Pei, Lichao Huang, and Zhizhong Su. Sparse4d: Multi-view 3d object detection with sparse spatial-temporal fusion. _arXiv preprint arXiv:2211.10581_ , 2022. 1 

- [26] Haisong Liu, Yao Teng, Tao Lu, Haiguang Wang, and Limin Wang. Sparsebev: High-performance sparse 3d object detection from multi-camera videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 18580–18590, 2023. 1 

- [27] Shu-Wei Lu, Yi-Hsuan Tsai, and Yi-Ting Chen. Toward real-world bev perception: Depth uncertainty estimation via gaussian splatting. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17124–17133, 2025. 2, 4, 3 

- [28] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. In _European conference on computer vision_ , pages 405–421. Springer, 2020. 4 

- [29] Chen Min, Liang Xiao, Dawei Zhao, Yiming Nie, and Bin Dai. Occupancy-mae: Self-supervised pre-training largescale lidar point clouds with masked occupancy autoencoders. _IEEE Transactions on Intelligent Vehicles_ , 9(7): 5150–5162, 2023. 2 

- [30] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15522–15533, 2024. 2 

- [31] Zak Murez, Tarrence Van As, James Bartolozzi, Ayan Sinha, Vijay Badrinarayanan, and Andrew Rabinovich. Atlas: Endto-end 3d scene reconstruction from posed images. In _European Conference on Computer Vision_ , pages 414–431. Springer, 2020. 6 

- [32] Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao, Jiayu Chen, Xinyu Huang, Yukang Chen, Feng Yan, et al. Grounded sam: Assembling open-world models for diverse visual tasks. _arXiv preprint arXiv:2401.14159_ , 2024. 4 

- [33] Jintao Sun, Hu Zhang, Gangyi Ding, and Zhedong Zheng. Echo planning for autonomous driving: From current observations to future trajectories and back. _arXiv preprint arXiv:2505.18945_ , 2025. 2 

- [34] Shihao Wang, Yingfei Liu, Tiancai Wang, Ying Li, and Xiangyu Zhang. Exploring object-centric temporal modeling for efficient multi-view 3d object detection. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 3621–3631, 2023. 5, 2 

- [35] Tai Wang, Xinge Zhu, Jiangmiao Pang, and Dahua Lin. Fcos3d: Fully convolutional one-stage monocular 3d object detection. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 913–922, 2021. 6 

- [36] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-worlddrive world models for autonomous driving. In _European_ 

_Conference on Computer Vision_ , pages 55–72. Springer, 2024. 2 

- [37] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14749–14759, 2024. 2 

- [38] Dongxu Wei, Zhiqi Li, and Peidong Liu. Omni-scene: Omnigaussian representation for ego-centric sparse-view scene reconstruction. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22317–22327, 2025. 3 

- [39] Yi Wei, Linqing Zhao, Wenzhao Zheng, Zheng Zhu, Jie Zhou, and Jiwen Lu. Surroundocc: Multi-camera 3d occupancy prediction for autonomous driving. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 21729–21740, 2023. 6 

- [40] Xinshuo Weng, Boris Ivanovic, Yan Wang, Yue Wang, and Marco Pavone. Para-drive: Parallelized architecture for realtime autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15449–15458, 2024. 7 

- [41] Xu Yan, Jiantao Gao, Chaoda Zheng, Chao Zheng, Ruimao Zhang, Shuguang Cui, and Zhen Li. 2dpass: 2d priors assisted semantic segmentation on lidar point clouds. In _European Conference on Computer Vision_ , pages 677–695. Springer, 2022. 1 

- [42] Xu Yan, Haiming Zhang, Yingjie Cai, Jingming Guo, Weichao Qiu, Bin Gao, Kaiqiang Zhou, Yue Zhao, Huan Jin, Jiantao Gao, et al. Forging vision foundation models for autonomous driving: Challenges, methodologies, and opportunities. _arXiv preprint arXiv:2401.08045_ , 2024. 1 

- [43] Ziyang Yan, Wenzhen Dong, Yihua Shao, Yuhang Lu, Liu Haiyang, Jingwen Liu, Haozhe Wang, Zhe Wang, Yan Wang, Fabio Remondino, and Yuexin Ma. Renderworld: World model with self-supervised 3d label. _arXiv preprint arXiv: 2409.11356_ , 2024. 2 

- [44] Honghui Yang, Sha Zhang, Di Huang, Xiaoyang Wu, Haoyi Zhu, Tong He, Shixiang Tang, Hengshuang Zhao, Qibo Qiu, Binbin Lin, et al. Unipad: A universal pre-training paradigm for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15238–15250, 2024. 2, 3 

- [45] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. Visual point cloud forecasting enables scalable autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 2, 3 

- [46] Wei Yin, Chi Zhang, Hao Chen, Zhipeng Cai, Gang Yu, Kaixuan Wang, Xiaozhi Chen, and Chunhua Shen. Metric3d: Towards zero-shot metric 3d prediction from a single image. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9043–9053, 2023. 4 

- [47] Wenyuan Zeng, Wenjie Luo, Simon Suo, Abbas Sadat, Bin Yang, Sergio Casas, and Raquel Urtasun. End-to-end interpretable neural motion planner. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 8660–8669, 2019. 7 

10 

- [48] Haiming Zhang, Ying Xue, Xu Yan, Jiacheng Zhang, Weichao Qiu, Dongfeng Bai, Bingbing Liu, Shuguang Cui, and Zhen Li. An efficient occupancy world model via decoupled dynamic flow and image-assisted training. _arXiv preprint arXiv:2412.13772_ , 2024. 2 

- [49] Haiming Zhang, Wending Zhou, Yiyao Zhu, Xu Yan, Jiantao Gao, Dongfeng Bai, Yingjie Cai, Bingbing Liu, Shuguang Cui, and Zhen Li. Visionpad: A vision-centric pre-training paradigm for autonomous driving. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17165–17175, 2025. 3 

      - video for autonomous driving representation learning. _International Journal of Computer Vision_ , pages 1–14, 2025. 3 

   - [60] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Gaussianworld: Gaussian world model for streaming 3d occupancy prediction. _arXiv preprint arXiv:2412.10373_ , 2024. 2, 5, 6 

- [50] Haiming Zhang, Yiyao Zhu, Wending Zhou, Xu Yan, Yingjie Cai, Bingbing Liu, Shuguang Cui, and Zhen Li. Sqs: Enhancing sparse perception models via query-based splatting in autonomous driving. _arXiv preprint arXiv:2509.16588_ , 2025. 2, 3 

- [51] Yunpeng Zhang, Zheng Zhu, and Dalong Du. Occformer: Dual-path transformer for vision-based 3d semantic occupancy prediction. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9433–9443, 2023. 6 

- [52] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _European Conference on Computer Vision_ , pages 55–72. Springer, 2024. 2, 6, 7 

- [53] Wenzhao Zheng, Ruiqi Song, Xianda Guo, Chenming Zhang, and Long Chen. Genad: Generative end-to-end autonomous driving. In _European Conference on Computer Vision_ , pages 87–104. Springer, 2024. 7 

- [54] Wenzhao Zheng, Junjie Wu, Yao Zheng, Sicheng Zuo, Zixun Xie, Longchao Yang, Yong Pan, Zhihui Hao, Peng Jia, Xianpeng Lang, et al. Gaussianad: Gaussian-centric end-toend autonomous driving. _arXiv preprint arXiv:2412.10371_ , 2024. 1, 3 

- [55] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, et al. World4drive: End-to-end autonomous driving via intention-aware physical latent world model. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 28632–28642, 2025. 2 

- [56] Xiaoyu Zhou, Zhiwei Lin, Xiaojun Shan, Yongtao Wang, Deqing Sun, and Ming-Hsuan Yang. Drivinggaussian: Composite gaussian splatting for surrounding dynamic autonomous driving scenes. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21634–21643, 2024. 3 

- [57] Yin Zhou and Oncel Tuzel. Voxelnet: End-to-end learning for point cloud based 3d object detection. In _Proceedings of the IEEE conference on Computer Vision and Pattern Recognition_ , pages 4490–4499, 2018. 1 

- [58] Yiyao Zhu, Di Luan, and Shaojie Shen. Biff: Bi-level future fusion with polyline-based coordinate for interactive trajectory prediction. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 8260–8271, 2023. 2 

- [59] Jialv Zou, Bencheng Liao, Qian Zhang, Wenyu Liu, and Xinggang Wang. Mim4d: Masked modeling with multi-view 

11 

# **DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving** 

# Supplementary Material 

## **F. Evaluation Metrics** 

**3D Occupancy Perception.** The primary metrics for 3D occupancy perception are the mean Intersection over Union (mIoU) and the Intersection over Union (IoU): 


where _C_<sup>_′_</sup> is the set of non-empty classes, _c_ 0 is the empty class, and _TPi_ , _FPi_ , and _FNi_ are the number of true positives, false positives, and false negatives for class _i_ , respectively. _TP̸_ = _c_ 0, _FP̸_ = _c_ 0, and _FN_ = _̸ c_ 0 are the aggregation of these values across all non-empty classes. 

**4D Occupancy Forecasting.** For the forecasting task, we assess the model’s ability to predict scene evolution over a future horizon of 3 seconds, corresponding to 6 frames (at 2Hz). The final metrics are reported as the average of the mIoU and IoU scores computed across these 6 future timestamps: 


where _T_ is the total future time steps, mIoU _t_ and IoU _t_ denote the metrics calculated at the _t_ -th future frame. **Motion Planning.** For the motion planning task, we evaluate the quality of the predicted ego-vehicle trajectories using the L2 error and collision rate. 

- **L2 Error.** The average Euclidean distance between the predicted waypoints _T_<sup>ˆ</sup> _t_ and the ground-truth waypoints _Tt_ over the future horizon _Nf_ : 


- **Collision Rate.** A collision occurs if the ego-vehicle’s bounding box, at future timestep _Nf_ intersects with the set of all ground-truth obstacle voxels. The final metric is the percentage of scenes where a collision is detected. 

## **G. Implementation Details** 

**Details of Gaussian Perception Module.** The Gaussian perception module is formulated to construct a compact and high-fidelity 3D scene representation _G_ parameterized by a set of 3D Gaussians from multi-view image observations. The architecture is composed of an image encoder and a Gaussian transformer decoder. 

The image encoder _E_ takes the multi-view images _I_ = _{_ **I** _i ∈_ R<sup>3</sup><sup>_×H×W_</sup> _|i_ = 1 _, ..., N }_ as input. For each view, a potent backbone (e.g., ResNet-101) first encodes the images into multi-level features _F_<sup>_′_</sup> . A Feature Pyramid Network (FPN) then refines _F_<sup>_′_</sup> to generate the final multi-scale image features _F_ , which capture both semantic and spatial details. 

Central to the Gaussian perception module is a Gaussian transformer decoder. The 3D scene is represented by _K_ distinct, learnable Gaussian queries. Each query _k_ is initialized with a learnable Gaussian anchor _gk ∈_ R<sup>_K×C_</sup> , which constitutes the learnable 3D geometric primitive, and its associated query features _qk ∈_ R<sup>_K×D_</sup> , initially set as zero vectors. _C_ and _D_ are the dimension of Gaussian primitives and query features respectively. These query features _qk_ are guided by their corresponding anchors _gk_ to interact with each other via a self-encoding block, and interact with the image features _F_ via deformable cross-attention to predict the Gaussian attributes. 

Specifically, the self-encoding block applies 4D sparse convolution to capture the relations of Gaussians within the current frame, and propagates temporal Gaussian queries from the previous frame in a stream manner. The deformable cross-attention aggregates the current image information from 2D image to 3D Gaussian queries via camera intrinsics _K_ and extrinsics _T_ . Finally, an MLP-based Gaussian head is applied to each Gaussian query, and Gaussian parameters are iteratively refined across decoder layers including position _µ_ , scale _S_ , rotation _R_ , opacity _α_ , and semantics _c_ . 

**Details of Latent World Model with Gaussian Flow.** To further illustrate the latent world model guided by Gaussian flow, we provide a pseudo code in Alg. 1. Given the current Gaussian _Gt_ , we aim to predict latent BEV _B_<sup>ˆ</sup> _t_ +1 at the next time step. Firstly, we estimate the Gaussian flow ∆ _µ_<sup>_t_</sup> by feeding the current Gaussian query features _qt_ to the flow head. Then in the next frame, we obtain the mean _µ_<sup>_t_+1</sup> of Gaussians by propagating dynamic flow ∆ _µ_<sup>_t_</sup> to the next frame via the ego motion alignment _Tego_<sup>_t→t_+1</sup> : _Tego_<sup>_t→t_+1</sup> ( _µ_<sup>_t_</sup> _k_<sup>+</sup> ∆ _µ_<sup>_t_</sup> _k_<sup>).TopredicttheGaussianset</sup><sup>_G_ˆ</sup><sup>_t_+1,weupdatethe</sup> 

1 

|**Algorithm 1**Latent World Model with Gaussian Flow.|
|---|
|**Input:** _Gt_ =_{µ_<sup>_t_</sup>_,_Σ<sup>_t_</sup>_, α_<sup>_t_</sup>_, c_<sup>_t_</sup>_, q_<sup>_t_</sup>_}_,_T _<sup>_t→t_+1</sup><br>_ego_<br><sup>ˆ</sup>|
|**Output:** _Bt_+1|
|_# predict the absolute flow for each Gaussian_|
|∆_µ_<sup>_t _</sup>_←_**FlowHead**(_q_<sup>_t_</sup>)|
|_# apply flow and align ego motion_<br>|
|_µ_<sup>_t_+1</sup> _←T _<sup>_t→t_+1</sup><br>_ego_<br>(_µ_<sup>_t_ </sup>+ ∆_µ_<sup>_t_</sup>)|
|_# update Gaussian set_<br>ˆ|
|_Gt_+1 _←{µ_<sup>_t_+1</sup>_,_Σ<sup>_t_</sup>_, α_<sup>_t_</sup>_, c_<sup>_t_</sup>_, q_<sup>_t_</sup>_}_|
|_# predict latent BEV by rasterization_<br>ˆ_Bt_+1 _←_**Rasterize**( ˆ_Gt_+1)<br>ˆ_Bt_+1|


#### **Algorithm 2** Latent World Model with Ego Planning. 

|**Input:** _Gt_,_Qwp_<br><sup>ˆ</sup>|
|---|
|**Output:** _Bt_+1|
|_# obtain current latent BEV by rasterization_|
|_Bt ←_**Rasterize**(_Gt_)|
|_# extract scene queries from BEV_<br>|
|_Q_<sup>_t_</sup><br>_scene _<sup>_←_</sup><sup>**ExtractQueries**(</sup><sup>_Bt_)</sup><br><br><br>|
|_Q_<sup>_t_</sup><br>_scene _<sup>_←_</sup><sup>**SelfAttn**(</sup><sup>_Qt_</sup><br>_scene_<sup>)</sup><br>|
|_# predict ego trajectory_<br>|
|_Q_<sup>_′_</sup><br>_wp _<sup>_←_</sup><sup>**CrossAttn**(</sup><sup>_Qwp, Qt_</sup><br>_scene_<sup>)</sup><br>ˆ|
|_T ←_**MLP**(_Q_<sup>_′_</sup><br>_wp_<sup>)</sup><br>|
|_# motion-aware layer norm conditioned on_ <sup>ˆ</sup>_T_<br><sup>ˆ</sup>|
|_Qnorm ←_**MLN**(_Q_<sup>_t_</sup><br>_scene_<sup>_,_ </sup><sup>_T_)</sup>|
|_# predict next scene queries_<br>|
|_Q_<sup>_t_+1</sup><br>_scene _<sup>_←_</sup><sup>**SelfAttn**(</sup><sup>_Qnorm_)</sup><br>_# reconstruct future BEV_<br>ˆ|
|_Bt_+1 _←_**Fuse**(_Q_<sup>_t_+1</sup><br>_scene_<sup>_, Bt_)</sup><br>ˆ_Bt_+1|


current set _Gt_ with the estimated mean _µ_<sup>_t_+1</sup> while all the others remain the same. Finally, to obtain the next latent BEV _B_<sup>ˆ</sup> _t_ +1, we project the predicted _G_<sup>ˆ</sup> _t_ +1 to 2D BEV plane by query feature rasterization [27]. 

**Details of Latent World Model with Ego Planning.** Regarding the latent world model guided by ego planning, we list the pseudo code step by step in Alg. 2. Our target is to predict the next latent BEV _B_<sup>ˆ</sup> _t_ +1 based on the current Gaussian _Gt_ coupled with ego planning. Firstly, we rasterize current Gaussian _Gt_ to latent BEV _Bt_ [27]. To improve computational efficiency, we extract scene queries _Q_<sup>_t_</sup> _scene_<sup>fromthecurrentBEV</sup><sup>_Bt_motivatedby[20].The</sup> following self-attention module is used to capture global context. To predict ego trajectory, the randomly initialized waypoint queries _Qwp_ interact with _Qscene_<sup>_t_through</sup> cross attention, followed by a MLP head for predicting ego trajectory _T_<sup>ˆ</sup> . Then we apply a Motion-Aware Layer Normalization (MLN) [34] layer for conditioning scene queries 

_Q_<sup>_t_</sup> _scene_<sup>on the predicted trajectory</sup><sup>_T_ˆ.The obtained</sup><sup>_Qnorm_</sup> predicts the next scene queries _Q_<sup>_t_</sup> _scene_<sup>+1by self attention.Fi-</sup> nally, we predict future BEV _B_<sup>ˆ</sup> _t_ +1 by fusing _Q_<sup>_t_</sup> _scene_<sup>+1with</sup> the current BEV _Bt_ following [20]. 

Table 7. **Ablation study on “Dual” and “Unified”.** 

|Model|mIoU (%)_↑_|L2 (m)_↓_|Col. (%)_↓_|
|---|---|---|---|
|Unified|18.9|0.58|0.22|
|Dual|**19.3**|**0.46**|**0.19**|


Table 8. **Ablation study on the number of 3D Gaussians.** 

|Nums|mIoU (%)_↑_|IoU (%)_↑_|
|---|---|---|
|7500|18.35|28.83|
|25600|19.30|**30.56**|
|51200|**19.43**|29.79|


Table 9. **Ablation study on the number of future frames.** 

|Nums|mIoU (%)_↑_|IoU (%)_↑_|
|---|---|---|
|0|18.83|30.12|
|1|**19.30**|**30.56**|
|2|19.23|30.52|
|4|19.06|29.20|


Table 10. **The computation cost analysis of all three tasks.** 

|Task|Memory|Latency|
|---|---|---|
|Perception|4.4GB|327ms|
|Forecasting|6.8GB|684ms|
|Planning|4.2GB|274ms|


## **H. Additional Experimental Results** 

**Comparing Dual Models with Unified Model.** The motivation of using two world models is that decoupling the training of Gaussian flow and ego planning is imperative for reducing learning complexity. 

As illustrated in Eq.5 (main paper), the predicted Gaussian mean is propagated through a combination of Gaussian flow and ego-motion alignment. For the Gaussian-flowguided model, leveraging GT ego motion reduces the learning complexity of Gaussian flow. Conversely, explicitly integrating Gaussian flow learning into the motion planning model would increase the latter’s learning burden. This is because self-supervised Gaussian flow lacking explicit supervision introduces unnecessary complexity to the planning, since the two items are coupled as shown in Eq.5 (main paper). 

2 


Figure 4. **Qualitative results of depth and semantic reconstruction and forecasting during the pre-training.** The left column shows the depth and semantic reconstruction at the current frame while the right column illustrates the depth and semantic images rendered by predicted Gaussians at the next frame compared with the GT RGB images. 

To verify this, we supplement an ablation experiment comparing the “Dual” models with the “Unified” model, where the predicted ego motion is utilized for motion transformation in place of GT in Eq. 5 for unifying learning of both flow and planning. The results in Tab. 7 confirm that the decoupled design achieves superior performance in perception and planning, justifying its necessity. 

**Number of Gaussians.** We conduct an ablation study (see Tab. 8) to evaluate the influence of the number of 3D Gaussian queries on the 3D occupancy perception performance. Testing configurations of 7,500, 25,600, and 51,200 Gaussians, the results reveal a trade-off: The mIoU (19.43) peaks at 51,200 Gaussians, indicating superior semantic granularity and expressive power. The IoU (30.56) achieves its best geometric accuracy with 25,600 Gaussians, suggesting this configuration strikes the optimal balance between density and reconstruction efficiency. We prioritize the configuration with 25,600 Gaussians for our final model. 

**Number of Future Frames.** We investigate the influence of the predicted number of future frames for pre-training stage 2 regarding Gaussian-flow-guided latent world model. 3D occupancy perception is selected for an ablation study. As shown in Tab. 9, we predict future Gaussians with four settings including “0”, “1”, “2”, and “4” future frames. The setting “0” denotes that we only reconstruct images without future prediction. By incorporating the prediction of the future frame _N_ = 1, the performance peaks at 19 _._ 30 mIoU and 30 _._ 56 IoU, demonstrating the beneficial impact of the 

Gaussian-flow-guided latent world model. The inclusion of additional future frames may slightly impair performance, potentially attributable to the greater scene changes caused by more distant future frames, which complicates accurate future prediction. 

**Inference Latency and Memory Analysis.** The dual world models are only used during the pre-training to facilitate representation learning in Gaussian perception module. For the inference stage, only the perception module and each task-specific head are used. Thus, the pre-training does not introduce additional inference latency. We measure inference latency and memory for each task on one GPU with batch size one. The evaluated results in Tab. 10 show lightweight memory and latency cost. 

## **I. BEV Supervision Discussion** 

BEV rasterization is used only for temporal supervision, not as the representation itself. Crucially: 1. All geometric reasoning happens in 3D Gaussian space during both pre-training and inference. 2. BEV features are derived from 3D Gaussians via differentiable rasterization that preserves height information through vertical stacking (following GaussianLSS [27]). 

## **J. Visualization Results** 

**Depth and Semantic Reconstruction and Forecasting.** To validate the effectiveness of our holistic Gaussian-centric 

3 


Figure 5. **Qualitative comparison of 3D Occupancy Perception over GT, baseline without pre-training and ours with pre-training.** 

pre-training, we present qualitative visualization results for depth and semantic image rendering in Fig. 4. During the pre-training stage, the model is tasked with reconstructing and forecasting the 3D scene geometry and semantics under self-supervision. The rendered depth maps (shown in the middle rows) exhibit sharp boundaries and accurate depth stratification, showing the ability for recovering detailed geometric structures. The rendered semantic maps (shown in the bottom rows) demonstrate high consistency with the semantic priors. Based on the excellent reconstruction performance in the left column of Fig. 4, the model exhibits accurate depth and semantic prediction at the next frame in the right column, meaning that the pre-training paradigm is able to model the temporal evolution for the driving scene. 

**3D Occupancy Perception.** We provide additional visualization results for the 3D occupancy perception task in Fig. 5. DLWM significantly outperforms the baseline with- 

out pre-training in both geometric completeness and semantic consistency. While the baseline suffers from fragmented structures and boundary misclassifications due to sparse observations, DLWM generates significantly more complete geometric structures and more accurate semantic classifications (e.g., for vehicles and vegetation) compared to the baseline. 

**4D Occupancy Forecasting.** We display the forecasted occupancy scenes at future time steps (e.g., 1s, 2s, and 3s) in Fig. 6. Compared to the baseline without pre-training, DLWM generates temporally consistent predictions with sharper geometric details. In contrast to the baseline, which produces blurred or static predictions, DLWM is pre-trained with Gaussian-flow-guided latent world model to explicitly predict Gaussian displacement, ensuring accurate trajectory forecasting for dynamic agents. 

4 


Figure 6. **Qualitative comparison of 4D Occupancy Forecasting over GTs, baseline without pre-training and ours with pre-training.** 

5 

