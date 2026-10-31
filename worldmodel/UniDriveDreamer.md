---
title: "UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving"
date: "2026-02-02"
authors: "Guosheng Zhao; Yaozeng Wang; Xiaofeng Wang; Zheng Zhu; Tingdong Yu; Guan Huang"
url: https://arxiv.org/abs/2602.02002
pdf: https://arxiv.org/pdf/2602.02002
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.02002)** / [論文ページ](https://arxiv.org/abs/2602.02002)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_2026-2-3_ 


# **UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving** 

**Guosheng Zhao**<sup>1</sup><sup>_,_2</sup><sup>_*_</sup> **Yaozeng Wang**<sup>1</sup><sup>_*_</sup> **Xiaofeng Wang**<sup>1</sup><sup>_*_</sup> **Zheng Zhu**<sup>1</sup><sup>_*_�</sup> **Tingdong Yu**<sup>1</sup> **Guan Huang**<sup>1</sup> **Yongchen Zai**<sup>3</sup> **Ji Jiao**<sup>3</sup> **Changliang Xue**<sup>3</sup> **Xiaole Wang**<sup>3</sup> **Zhen Yang**<sup>3</sup> **Futang Zhu**<sup>3</sup> **Xingang Wang**<sup>2�</sup> **1 GigaAI 2 CASIA 3 BYD** 

## **Abstract** 

**World models have demonstrated significant promise for data synthesis in autonomous driving. However, existing methods predominantly concentrate on single-modality generation, typically focusing on either multi-camera video or LiDAR sequence synthesis. In this paper, we propose** **_UniDriveDreamer_ , a single-stage unified multimodal world model for autonomous driving, which directly generates multimodal future observations without relying on intermediate representations or cascaded modules. Our framework introduces a LiDAR-specific variational autoencoder (VAE) designed to encode input LiDAR sequences, alongside a video VAE for multi-camera images. To ensure cross-modal compatibility and training stability, we propose Unified Latent Anchoring (ULA), which explicitly aligns the latent distributions of the two modalities. The aligned features are fused and processed by a diffusion transformer that jointly models their geometric correspondence and temporal evolution. Additionally, structured scene layout information is projected per modality as a conditioning signal to guide the synthesis. Extensive experiments demonstrate that** **_UniDriveDreamer_ outperforms previous state-of-the-art methods in both video and LiDAR generation, while also yielding measurable improvements in downstream driving tasks.** 

## **1. Introduction** 

World models (Agarwal et al., 2025; Ali et al., 2025; Gao et al., 2024; Hu et al., 2023; LeCun, 2022; Ni et al., 2025,; Ren et al., 2025; Team et al., 2025; Wang et al., 2024,; Zhao et al., 2025,) have made significant progress in autonomous driving, and their powerful data synthesis capabilities offer a promising solution for reducing the costs of data acquisition and annotation. Recent studies (Gao et al., 2023, 2025; Russell et al., 2025; Wen et al., 2024; Yang et al., 2025) have established a notable paradigm that leverages structured scene layouts, such as 3D bounding boxes and HDMaps, as conditional inputs for driving data generation. The synthesized data can be further utilized to enhance the performance of downstream tasks (Li et al., 2024; Liu et al., 2023). 

Nevertheless, existing methods primarily focus on single-modality generation, such as camera-only RGB synthesis (Gao et al., 2023, 2025, 2024; Li et al., 2024; Wang et al., 2024,; Wen et al., 2024; Yang et al., 2023; Zhao et al., 2025) or LiDAR sequence generation (Caccia et al., 2019; Hu et al., 2024; Zyrianov et al., 2022, 2025). Although these approaches are able to produce highly realistic data that benefit downstream perception tasks, the inherent single-modality nature limits their applicability in scenarios demanding diverse multi-sensor observations. Recently, a few efforts have explored multimodal generation for autonomous driving, demonstrating the concrete potential of multimodal data synthesis to improve downstream task performance. However, existing methods (Guo et al., 2025; Li et al., 2025) typically decouple the generation of different modalities. In such frameworks, the synthesis of one modality (e.g., LiDAR) is explicitly conditioned on the output or latent representation of another (e.g., RGB). This decoupled architecture lacks explicit, bidirectional interaction between the RGB and LiDAR modalities during the synthesis process, which consequently undermines cross-modal consistency. The resulting unidirectional information flow impedes the effective utilization of complementary sensor data, consequently degrading the overall quality and coherence of the generated multimodal outputs. 

© 2026 GigaAI. All rights reserved. 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

To address this challenge, we introduce _UniDriveDreamer_ , a single-stage multimodal world model designed for autonomous driving, which enables deep fusion and bidirectional interaction across different modalities, thereby substantially enhancing the spatiotemporal and cross-modal consistency of synthesized outputs. Specifically, a LiDAR-specific variational autoencoder (VAE) is designed to encode input range images into a latent space, while multi-view images are processed by a video VAE (Kingma and Welling, 2013; Wan et al., 2025). Furthermore, to stabilize training and ensure compatibility between modalities, we propose Unified Latent Anchoring (ULA), which aligns the distribution of LiDAR latents with the prior of a pretrained RGB VAE via affine transformations derived from empirical statistics. The aligned latent features are then fused and processed by a diffusion transformer, which jointly models both intra- and cross-modal spatiotemporal relationships. In addition, we incorporate structured scene layout information to guide the generation process by projecting it into each modality as a conditioning signal. Extensive experimental results demonstrate that _UniDriveDreamer_ surpasses previous state-of-the-art methods (SOTA) in multimodal data synthesis quality. Specifically, for video generation, _UniDriveDreamer_ achieves an FID of 2.81 and an FVD of 11.44. For LiDAR synthesis, it attains an MMD of 0.27 and a JSD of 0.039, corresponding to 82.3% and 45.8% relative improvements over UniScene (Li et al., 2025). In addition, downstream task evaluations further confirm the practical effectiveness of the generated data, showing relative improvements of +1.2% in mAP and +0.7% in NDS. 

Overall, our contributions can be summarized as follows: 

- We propose _UniDriveDreamer_ , a single-stage multimodal world model for autonomous driving, which directly generates temporally consistent and geometrically coherent future observations, including multi-camera videos and LiDAR sweeps, without relying on intermediate representations or cascaded modules. 

- We propose a LiDAR-specific VAE, capable of accurately reconstructing LiDAR sequences. Furthermore, to ensure cross-modal compatibility, Unified Latent Anchoring (ULA) is proposed to align their distributions via affine transformations based on empirical statistics, thereby stabilizing training and ensuring crossmodal compatibility. 

- Experimental results demonstrate that _UniDriveDreamer_ not only surpasses previous SOTA methods in multimodal synthesis quality but also delivers significant improvements in downstream perception task performance. 

## **2. Related Work** 

### **2.1. Unimodal Driving Scene Generation** 

The rapid advancement of diffusion models (Agarwal et al., 2025; Ali et al., 2025; Ball et al., 2025; Blattmann et al., 2023; Kong et al., 2024; Rombach et al., 2022; Wan et al., 2025; Wang et al., 2025, 2024; Zhang et al., 2023; Zhu et al., 2024) has catalyzed a surge of research in driving video generation (Alhaija et al., 2025; Gao et al., 2023, 2025, 2024; Hu et al., 2023; Li et al., 2024; Ren et al., 2025; Russell et al., 2025; Swerdlow et al., 2024; Wang et al., 2024; Wen et al., 2024; Yang et al., 2025; Zhao et al., 2025). These methods commonly employ structured scene layouts as conditional inputs to synthesize realistic driving videos, substantially lowering the cost of data acquisition and annotation while demonstrating effectiveness in enhancing downstream perception performance. Furthermore, several approaches (Ma et al., 2024; Wang et al., 2024; Yang et al., 2024) have investigated the application of world models in end-to-end autonomous driving. In parallel, as LiDAR serves as a crucial sensing modality in driving scenarios, recent methods (Caccia et al., 2019; Hu et al., 2024; Ren et al., 2025; Zyrianov et al., 2022, 2025) have begun to introduce generative techniques for LiDAR data synthesis. These methods typically represent LiDAR data as range images by transforming the 3D point clouds to 2D pixel space, thereby aligning its format with that of RGB images. This representation facilitates the application of well-established image and video generation techniques, leading to significant advancements in the field. Despite these advances, existing approaches remain predominantly focus on single-modality generation, thereby limiting the realization of sensor-complete autonomous driving 

2 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 


Figure 1: The overall framework of _UniDriveDreamer_ . Our _UniDriveDreamer_ consists of four core components: (1) two modality-specific VAEs that encode multi-view camera images and LiDAR range maps into a shared latent space; (2) a layout encoder that projects structured scene layout information into corresponding latent representations; (3) a text encoder that encode multi-view text prompts into corresponding prompt embeddings; and (4) a diffusion transformer that jointly models spatiotemporal coherence within each modality and crossmodal consistency across modalities. 

simulation environments. To bridge this gap, we propose _UniDriveDreamer_ , a unified world model designed to address multimodal data synthesis in driving scenarios, capable of jointly generating multi-view camera videos and LiDAR sequences. 

### **2.2. Multimodal Driving Scene Generation** 

To meet the demand for multimodal data in downstream tasks, recent works (Guo et al., 2025; Li et al., 2025; Liang et al., 2025; Tang et al., 2025; Zhang et al., 2024) have begun to explore multimodal data generation for driving scenarios. For instance, UniScene (Li et al., 2025) proposes a two-stage pipeline that first generates an occupancy representation, then synthesizes camera and LiDAR data conditioned on it. Following a similar cascaded philosophy, Genesis (Guo et al., 2025) employs a dual-branch architecture, where the explicit occupancy is replaced by a latent video representation extracted from the RGB branch, and LiDAR generation is conditioned on these features sequentially. Despite these advances, such cascaded or sequential paradigms lack explicit bidirectional interaction between RGB and LiDAR during synthesis, which constrains the overall quality and consistency of the generated multimodal outputs. In contrast, our _UniDriveDreamer_ adopts a single-stage architecture that enables bidirectional interaction between RGB and LiDAR modalities throughout the generation process, facilitating deeper fusion and more coherent multimodal synthesis. 

## **3. UniDriveDreamer** 

The overall framework is illustrated in Fig. 1. Multi-view images and LiDAR range maps are first encoded by their dedicated VAEs. The resulting latent features are then concatenated in the channel dimension with the corresponding modality-specific layout latent features and view embeddings. Next, the two sets of multimodal latent tokens are concatenated along the sequence dimension and fed directly into a diffusion transformer, which jointly models both intra-modal spatiotemporal consistency and cross-modal alignment in the latent space. Finally, the output latent representations are decoded back into their respective modalities, RGB video frames and LiDAR range sequences, through the corresponding decoder networks. 

3 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

### **3.1. LiDAR VAE** 

In this section, we detail the training and inference process of the proposed LiDAR-specific VAE. Notably, to facilitate joint generation of LiDAR sequences and camera videos, we adopt range images as the LiDAR representation, thereby aligning its format more closely with RGB imagery. 

**Training.** Our LiDAR VAE preserves the same architectural backbone as the RGB VAE proposed in (Wan et al., 2025), differing only in the number of input and output channels, which are set to 1 instead of 3 to accommodate the single-channel nature of range images. Following (Ren et al., 2025), we further mitigate the inherent sparsity of range images by repeating each row of the range map four times, yielding an input sequence _𝑣_<sup>L</sup> _∈_ R<sup>(1+</sup><sup>_𝑇_)</sup><sup>_×𝐻_L</sup><sup>_×𝑊_L</sup><sup>_×_1</sup> . The encoder of the LiDAR VAE maps the sequence to a latent representation 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>L</sup><sup>_×_</sup><sup>_<u>𝑊</u>_L</sup> _𝑧_<sup>L</sup> = _𝜉_ ( _𝑣_<sup>L</sup> ) _∈_ R<sup>(1+</sup><sup>_<u>𝑇</u>_</sup> 8<sup>_×𝐶_</sup> , which is subsequently decoded back into the reconstructed LiDAR video _𝑣_ ˆ<sup>L</sup> = _𝒢_ ( _𝑧_<sup>L</sup> ) _∈_ R<sup>(1+</sup><sup>_𝑇_)</sup><sup>_×𝐻_L</sup><sup>_×𝑊_L</sup><sup>_×_1</sup> . The model is trained using the following composite loss function: 


where _𝐷_ KL( _·_ ) is the Kullback–Leibler divergence between the approximate posterior _𝑞_ ( _𝑧_<sup>L</sup> _|𝑣_<sup>L</sup> ) and the standard Gaussian prior _𝑝_ ( _𝑧_<sup>L</sup> ) _∼𝒩_ ( _𝑧_<sup>L</sup> ; **0** _,_ **I** ), and _ℒ_ LPIPS is the Learned Perceptual Image Patch Similarity (LPIPS) loss (Zhang et al., 2018). Since LPIPS is originally defined for RGB images, we replicate the single-channel range images across three channels when computing this perceptual loss term. 

**Inference.** Once trained, the LiDAR VAE is integrated into the multimodal world model for joint training. To stabilize training and ensure cross-modal compatibility, we introduce Unified Latent Anchoring (ULA), which aligns the latent distribution of LiDAR features with that of the camera modality. Let _𝜇_<sup>C</sup> _, 𝜎_<sup>C</sup> be the normalization parameters of the pretrained RGB VAE, _𝜇_<sup>C</sup> 1<sup>_, 𝜎_</sup> 1<sup>Cdenote the statistics computed from the current</sup> driving dataset using the RGB VAE, and _𝜇_<sup>L</sup> 1<sup>_, 𝜎_</sup> 1<sup>LreferthecorrespondingstatisticsfromtheLiDARVAE.The</sup> calibrated normalization parameters _𝜇_<sup>L</sup> _, 𝜎_<sup>L</sup> for the LiDAR latent features are then obtained as: 


### **3.2. Single-Stage Multimodal World Model** 

In this section, we present the detailed design of our single-stage multimodal world model, _UniDriveDreamer_ . As illustrated in Fig. 1, _UniDriveDreamer_ comprises four key components: two modality-specific VAEs, a layout encoder, a text encoder, and a diffusion transformer. Given an input sequence of multi-camera videos _𝑣_<sup>C</sup> _∈_ R<sup>_𝑉×_(1+</sup><sup>_𝑇_)</sup><sup>_×𝐻_C</sup><sup>_×𝑊_C</sup><sup>_×_3</sup> and LiDAR sweeps _𝑣_<sup>L</sup> _∈_ R<sup>(1+</sup><sup>_𝑇_)</sup><sup>_×𝐻_L</sup><sup>_×𝑊_L</sup><sup>_×_1</sup> , each modality is first encoded into the latent space _𝑧_<sup>C</sup> _∈_ R<sup>_𝑉×_(1+</sup><sup>_<u>𝑇</u>_</sup> 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>C</sup><sup>_×_</sup><sup>_<u>𝑊</u>_</sup> 8<sup>C</sup><sup>_×𝐶_</sup> , _𝑧_<sup>L</sup> _∈_ R<sup>(1+</sup><sup>_<u>𝑇</u>_</sup> 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>L</sup><sup>_×_</sup><sup>_<u>𝑊</u>_</sup> 8<sup>L</sup><sup>_×𝐶_</sup> by its corresponding VAE. Multi-view textual prompts are encoded using a pretrained text encoder Chung et al. (2023). The layout encoder and the diffusion transformer are described in detail below. 

**Layout Encoder.** The Layout Encoder consists of a spatial downsampling block followed by two spatiotemporal downsampling blocks (Wan et al., 2025), aligning the spatiotemporal compression rate of layout latents with that of the multimodal data. Specifically, we first project structured 3D scene information, including 3D bounding boxes and HDMap, into both camera views and LiDAR range views. In camera views, different object categories and lane markings are distinguished by distinct colors, while in range views, the projection yields 

4 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 


Figure 2: Transformer block of _UniDriveDreamer_ . 

single-channel distance values. To enable the same layout encoder to process both modalities, we replicate the single-channel range-view layout map three times along the channel dimension before feeding it into the encoder. The encoder then outputs multi-camera view condition latents _𝑐_<sup>C</sup> layout<sup>_∈_R</sup><sup>_𝑉×_(1+</sup><sup>_<u>𝑇</u>_</sup> 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>C</sup><sup>_×_</sup><sup>_<u>𝑊</u>_</sup> 8<sup>C</sup><sup>_×𝐶_</sup> and 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>L</sup><sup>_×_</sup><sup>_<u>𝑊</u>_L</sup> range-view condition latents _𝑐_<sup>L</sup> layout<sup>_∈_R(1+</sup><sup>_<u>𝑇</u>_</sup> 8<sup>_×𝐶_</sup> , which are then used to guide the respective modality synthesis. 

**Diffusion Transformer.** The diffusion transformer architecture comprises three main components: (1) two modality-specific patchifying modules, (2) a shared stack of transformer blocks, and (3) two modality-specific unpatchifying modules. In the patchifying modules, a 3D convolution with a kernel size of (1, 2, 2) followed by a flattening operation is applied to convert the camera-views and range-view inputs into camera tokens _𝑇_<sup>C</sup> and LiDAR tokens _𝑇_<sup>L</sup> of shapes (︀ _𝐵,_ ( _𝑉𝐿_<sup>C</sup> ) _, 𝐷_ )︀ and ( _𝐵, 𝐿_<sup>L</sup> _, 𝐷_ ), respectively. The camera-view input is constructed by concatenating along the channel dimension the noisy latents _𝑧_ t<sup>C,view-specificembeddings</sup> _𝑒𝑚𝑏_<sup>C</sup> , layout-conditioning latents _𝑐_<sup>C</sup> layout<sup>,and first frame conditioning latents</sup><sup>_𝑐_</sup> frame<sup>C;the range-view input is</sup> formed analogously. These two sets of modality tokens are then concatenated along the sequence dimension and fed into the shared transformer block stack. As depicted in Fig. 2, the concatenated multimodal tokens first pass through a self-attention module, which jointly models intra-modal spatiotemporal dependencies and enforces cross-modal consistency. The tokens are then separated by modality. The camera tokens are reshaped to (︀( _𝐵𝑉_ ) _, 𝐿_<sup>C</sup> _, 𝐷_ )︀ and processed together with the LiDAR tokens through a cross-attention layer that conditions the generation on textual prompts. Subsequently, the camera tokens are reshaped back to their original layout and concatenated with the LiDAR tokens before being passed through a feed-forward network. After passing through the stack of transformer blocks, the modality-specific tokens are individually transformed by their corresponding unpatchifying modules to recover the original latent shape of each modality. 

**Optimization.** _UniDriveDreamer_ is optimized by using the flow matching framework (Esser et al., 2024; Lipman et al., 2023). Given a timestep _𝑡 ∈_ [0 _,_ 1] sampled from a logit-normal distribution, a random camera noise _𝑧_ 0<sup>C</sup><sup>_∈_R(1+</sup><sup>_<u>𝑇</u>_</sup> 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>C</sup><sup>_×_</sup><sup>_<u>𝑊</u>_</sup> 8<sup>C</sup><sup>_×𝐶_</sup> , and a random range-view noise _𝑧_ 0<sup>L</sup><sup>_∈_R(1+</sup><sup>_<u>𝑇</u>_</sup> 4<sup>)</sup><sup>_×_</sup><sup>_<u>𝐻</u>_</sup> 8<sup>L</sup><sup>_×_</sup><sup>_<u>𝑊</u>_</sup> 8<sup>L</sup><sup>_×𝐶_</sup> , the noisy latent _𝑧𝑡_ is obtained as: 


where _𝑧_ 1<sup>Cand</sup><sup>_𝑧_</sup> 1<sup>Ldenote the clean camera and LiDAR latents, respectively.The corresponding ground-truth</sup> velocity _𝜈𝑡_ is computed as: 


The model is then optimized to predict this velocity via the following objective: 


5 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

where the conditioning signal _𝑐_ comprises layout conditions, multi-view text prompt embeddings, and first frame latents. The parameter set _𝜃_ includes the weights of the diffusion transformer and the layout encoder. 

Table 1: Comparison of the generation quality on nuScenes validation set. 

|Modality|Method|Camera G|eneration|LiDAR Ge|neration|
|---|---|---|---|---|---|
|||FID_↓_|FVD_↓_|MMD_↓_|JSD_↓_|
||DriveDreamer (Wang et al.,2024)|14.90|340.80|-|-|
||DriveDreamer-2 (Zhao et al.,2025)|11.20|55.70|-|-|
|C|MagicDrive (Gao et al.,2023)|16.20|-|-|-|
|amera|MagicDrive-V2 (Gao et al.,2025)|20.91|94.84|-|-|
||Panacea (Wen et al.,2024)|16.96|139.0|-|-|
||Drive-WM (Wang et al.,2024)|15.80|122.70|-|-|
||LiDARVAE (Caccia et al.,2019)|-|-|11.0|-|
|LiDAR|LiDARGen (Zyrianov et al.,2022)|-|-|19.0|0.160|
||RangeLDM (Hu et al.,2024)|-|-|1.90|0.054|
||UniScene (Li et al.,2025)|6.12|70.52|1.53|0.072|
|Mlidl|OmniGen (Tang et al.,2025)|21.01|-|2.94|0.105|
|utmoa|Genesis (Guo et al.,2025)|4.24|16.95|-|-|
||_UniDriveDreamer_|**2.81**|**11.44**|**0.27**|**0.039**|


## **4. Experiment** 

In this section, we present our experimental setup, including the datasets, implementation details and evaluation metrics. Subsequently, both quantitative and qualitative results are provided to demonstrate the superior performance of the proposed _UniDriveDreamer_ . In addition, ablation studies are conducted to validate key design choices. 

### **4.1. Experiment Setup** 

**Datasets.** The training dataset is derived from the nuScenes dataset (Caesar et al., 2020), consisting of 700 training sequences and 150 validation sequences. Each sequence encompasses approximately 20 seconds of recorded driving data, captured by six surround-view cameras and a roof-mounted LiDAR. Following (Wang et al., 2023, 2024; Zhao et al., 2025), we preprocess the nuScenes dataset to calculate 12Hz annotations. 

**Implementation Details.** In our experiments, camera videos are processed at a resolution of 432 _×_ 768 and LiDAR range maps at 32 _×_ 1024, with a temporal length of 17 frames. _UniDriveDreamer_ is initialized with the pretrained weights of Wan-2.1 T2V-1.3B (Wan et al., 2025). The model is optimized with a learning rate of 2 _×_ 10<sup>_−_5</sup> . For the LiDAR VAE, we load the pretrained VAE weights from Wan-2.1 (Wan et al., 2025) and set the learning rate to 5 _×_ 10<sup>_−_5</sup> . The reconstruction loss, KL divergence loss, and LPIPS loss are weighted with coefficients _𝜆_ 1 = 1, _𝜆_ 2 = 1, and _𝜆_ 3 = 0 _._ 3 respectively. Furthermore, following (Wan et al., 2025), we adopt the umT5 model (Chung et al., 2023) as the text encoder. 

**Evaluation Metrics.** The evaluation in this work covers three key aspects: generation quality, LiDAR reconstruction fidelity, and downstream task performance. To assess the quality of synthesized camera videos, we employ Fréchet Inception Distance (FID) (Heusel et al., 2017) and Fréchet Video Distance (FVD) (Unterthiner et al., 2018). For LiDAR sequences, we follow the evaluation protocol of (Zyrianov et al., 2025) and adopt Maximum Mean Discrepancy (MMD) and Jensen–Shannon Divergence (JSD), where the MMD results are reported scaled by 10<sup>4</sup> . The geometric accuracy of LiDAR reconstruction is measured using Chamfer Distance and F-Score as adopted in (Tang et al., 2025). Finally, we employ BEVFusion (Liu et al., 2023) to assess the 

6 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

utility of the generated data for downstream perception and report the nuScenes Detection Score (NDS) and mean Average Precision (mAP) for 3D object detection. 


Figure 3: Qualitative comparison of generated outputs with Genesis (Guo et al., 2025). The top row shows the ground truth. The middle row presents results from Genesis. The bottom row displays outputs from our _UniDriveDreamer_ . 

### **4.2. Main Results** 

In this section, we present the experimental results in three aspects: (1) quality of multimodal data generation, (2) LiDAR reconstruction fidelity, and (3) downstream perception performance gains. 

**Multimodal Generation Results.** As shown in Tab. 1, we compare _UniDriveDreamer_ against SOTA single-modal and multimodal methods (Caccia et al., 2019; Gao et al., 2023, 2025; Guo et al., 2025; Hu et al., 2024; Li et al., 2025; Tang et al., 2025; Wang et al., 2024,; Wen et al., 2024; Zhao et al., 2025; Zyrianov et al., 2022) on the nuScenes validation set (Caesar et al., 2020) in terms of generation quality. Quantitative results demonstrate that _UniDriveDreamer_ achieves superior performance in both camera video and LiDAR sequence synthesis. Specifically, for video generation, _UniDriveDreamer_ attains an FID of 2.81 and an FVD of 11.44. For LiDAR synthesis, it yields an MMD of 0.27 and a JSD of 0.039, corresponding to improvements of 82.3% in MMD and 45.8% in JSD over UniScene (Li et al., 2025). Qualitative comparisons in Fig. 3 demonstrate the superior generation quality of _UniDriveDreamer_ . For LiDAR synthesis, the results of _UniDriveDreamer_ exhibit more 

7 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

complete ground coverage and higher geometric fidelity than those of Genesis (Guo et al., 2025), showing closer alignment with the ground truth. For camera video generation, our method produces visually sharper and more realistic outputs with enhanced detail preservation. Additional generated examples are presented in Fig. 4 and Fig. 5. These visual results further demonstrate the high controllability of our model under varied scene layouts, its strong spatiotemporal consistency across extended sequences, and its robust cross-modal alignment between camera views and LiDAR sweeps. 


Figure 4: Qualitative visualization of multimodal outputs generated by _UniDriveDreamer_ . In each example set, the upper row presents the ground truth, while the lower row shows the corresponding synthesized results generated by _UniDriveDreamer_ . 

8 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 


Figure 5: Qualitative visualization of multimodal outputs generated by _UniDriveDreamer_ . In each example set, the upper row presents the ground truth, while the lower row shows the corresponding synthesized results generated by _UniDriveDreamer_ . 

**LiDAR Reconstruction Results.** As shown in Tab. 2, we compare our LiDAR VAE against OmniGen (Tang et al., 2025) on LiDAR sequence reconstruction. The results demonstrate that our LiDAR VAE substantially outperforms the current SOTA in reconstruction fidelity, achieving a Chamfer Distance of 0.154 and an F-Score of 0.900. This corresponds to an improvement of approximately 80.6% in Chamfer Distance and 21.3% in F-Score over the baseline. Fig. 6 provides a visual comparison across several distinct driving scenarios between 

9 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 


Figure 6: Qualitative visualization of LiDAR reconstruction. The upper row shows the real LiDAR data, while the lower row presents the reconstructed point clouds from the LiDAR-specific VAE in _UniDriveDreamer_ . 

our reconstructed LiDAR sweeps and the ground truth. The visualization clearly demonstrates that the proposed LiDAR VAE preserves geometric structures effectively, producing dense and coherent point clouds that closely match the original scans. 

Table 2: Comparison of the reconstruction quality on nuScenes validation set. 

|Method|Chamfer Distance_↓_|F-Score_↑_|
|---|---|---|
|OmniGen (Tang et al.,2025)|0.793|0.742|
|_UniDriveDreamer_|**0.154**|**0.900**|


**Downstream Task Results.** Since the generated data lack LiDAR intensity information, we set the intensity channel to zero for all data points during downstream task training. Using this preprocessed real data, we train BEVFusion (Liu et al., 2023) from scratch to establish our baseline. As shown in Tab. 3, the data generated by _UniDriveDreamer_ leads to notable improvements in downstream perception performance, increasing mAP by +0.8 and NDS by +0.52 compared to training with real data alone. These results validate the effectiveness of _UniDriveDreamer_ in enhancing perception performance for autonomous driving. 

Table 3: Multimodal Generation Data Augmentation for 3D Object Detection. 

|Training Data|mAP_↑_|NDS_↑_|
|---|---|---|
|Original Data|66.38|70.01|
|Augmented Data by_UniDriveDreamer_|**67.18**|**70.53**|


### **4.3. Ablation Study** 

In this section, we conduct ablation studies to analyze two key design choices: (1) the effect of range-map height repetition on LiDAR reconstruction fidelity, and (2) the impact of Unified Latent Anchoring (ULA) on cross-modal alignment and generation quality. 

**Effect of Range-Map Repeat Height.** We investigate the influence of height repetition in range-map encoding 

10 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 


Figure 7: Qualitative comparison of generated outputs with and without the Unified Latent Anchoring (ULA) module. The top row displays the ground truth. The middle row illustrates results without ULA, highlighting geometric inconsistencies and cross-modal misalignment between LiDAR points and RGB content. The bottom row presents results with ULA,showing enhanced cross-modal geometric coherence and improved visual quality. 

on LiDAR reconstruction quality. As reported in Tab. 4, progressively increasing the number of height repetitions from 1 to 4 leads to consistent improvements in Chamfer Distance and F-Score. The best performance is achieved with 4 repetitions, reaching a Chamfer Distance of 0.154 and an F-Score of 0.900, which validates that repeated height channels effectively mitigate range-map sparsity and improve geometric detail recovery. Therefore, we adopt 4 repetitions as the default setting in our model. 

Table 4: Effect of range-map repeat height for LiDAR reconstruction fidelity. 

|Repeat Height|Chamfer Distance_↓_|F-Score_↑_|
|---|---|---|
|1|0.513|0.794|
|2|0.336|0.829|
|4|**0.154**|**0.900**|


**Effect of ULA.** We ablate the proposed Unified Latent Anchoring (ULA) module to examine its contribution to training stability and cross-modal alignment. As illustrated in Fig. 7, removing ULA leads to noticeable 

11 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

degraded consistency between the RGB and LiDAR outputs, demonstrating that explicit latent alignment enhances both intra-modal quality and cross-modal coherence. These results validate the importance of ULA in enabling robust joint multimodal learning. 

## **5. Conclusion** 

This paper introduces _UniDriveDreamer_ , a single-stage unified multimodal world model. By adopting range images as the LiDAR representation, designing a LiDAR-specific VAE, and proposing Unified Latent Anchoring (ULA) for explicit cross-modal distribution alignment, our model effectively bridges the modality gap between camera and LiDAR data. Built upon a shared diffusion transformer, the model directly synthesizes temporally consistent and geometrically coherent multi-camera videos and LiDAR sweeps, eliminating the need for cascaded or intermediate representations. Extensive experiments validate that _UniDriveDreamer_ surpasses SOTA methods in both camera and LiDAR synthesis. It achieves an FID of 2.81 and an FVD of 11.44 for video generation, and attains an MMD of 0.27 and a JSD of 0.039 for LiDAR generation, corresponding to relative improvements of 82.3% in MMD and 45.8% in JSD over the best prior work. Moreover, downstream perception tasks benefit measurably from the synthesized multimodal data, with improvements of +0.8 mAP and +0.52 NDS, confirming its practical utility for enhancing autonomous driving systems. Our work provides an efficient paradigm for multimodal sensor simulation, paving the way for more data-efficient and robust autonomous driving development. 

12 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

## **References** 

- [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 1, 2 

- [2] Hassan Abu Alhaija, Jose Alvarez, Maciej Bala, Tiffany Cai, Tianshi Cao, Liz Cha, Joshua Chen, Mike Chen, Francesco Ferroni, Sanja Fidler, et al. Cosmos-transfer1: Conditional world generation with adaptive multimodal control. _arXiv preprint arXiv:2503.14492_ , 2025. 2 

- [3] Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Aaron Blakeman, Tiffany Cai, Jiaxin Cao, Tianshi Cao, Elizabeth Cha, Yu-Wei Chao, et al. World simulation with video foundation models for physical ai. _arXiv preprint arXiv:2511.00062_ , 2025. 1, 2 

- [4] Philip J. Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, et al. Genie 3: A new frontier for world models. 2025. URL `https://deepmind.google/blog/ genie-3-a-new-frontier-for-world-models/` . 2 

- [5] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint arXiv:2311.15127_ , 2023. 2 

- [6] Lucas Caccia, Herke Van Hoof, Aaron Courville, and Joelle Pineau. Deep generative modeling of lidar data. In _IROS_ , 2019. 1, 2, 6, 7 

- [7] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _CVPR_ , 2020. 6, 7 

- [8] Hyung Won Chung, Xavier Garcia, Adam Roberts, Yi Tay, Orhan Firat, Sharan Narang, and Noah Constant. Unimax: Fairer and more effective language sampling for large-scale multilingual pretraining. In _ICLR_ , 2023. 4, 6 

- [9] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas Müller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for high-resolution image synthesis. In _ICML_ , 2024. 5 

- [10] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing HONG, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. In _ICLR_ , 2023. 1, 2, 6, 7 

- [11] Ruiyuan Gao, Kai Chen, Bo Xiao, Lanqing Hong, Zhenguo Li, and Qiang Xu. Magicdrive-v2: Highresolution long video generation for autonomous driving with adaptive control. In _CVPR_ , 2025. 1, 2, 6, 7 

- [12] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. _NeurIPS_ , 2024. 1, 2 

- [13] Xiangyu Guo, Zhanqian Wu, Kaixin Xiong, Ziyang Xu, Lijun Zhou, Gangwei Xu, Shaoqing Xu, Haiyang Sun, Bing Wang, Guang Chen, et al. Genesis: Multimodal driving scene generation with spatio-temporal and cross-modal consistency. _arXiv preprint arXiv:2506.07497_ , 2025. 1, 3, 6, 7, 8 

- [14] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. _NeurIPS_ , 2017. 6 

13 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

- [15] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 1, 2 

- [16] Qianjiang Hu, Zhimin Zhang, and Wei Hu. Rangeldm: Fast realistic lidar point cloud generation. In _ECCV_ , 2024. 1, 2, 6, 7 

- [17] Diederik P Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 2 

- [18] Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu, Jianwei Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models. _arXiv preprint arXiv:2412.03603_ , 2024. 2 

- [19] Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 2022. 1 

- [20] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. Uniscene: Unified occupancy-centric driving scene generation. In _CVPR_ , 2025. 1, 2, 3, 6, 7 

- [21] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. Drivingdiffusion: layout-guided multi-view driving scenarios video generation with latent diffusion model. In _ECCV_ , 2024. 1, 2 

- [22] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. _IEEE TPAMI_ , 2024. 1 

- [23] Dingkang Liang, Dingyuan Zhang, Xin Zhou, Sifan Tu, Tianrui Feng, Xiaofan Li, Yumeng Zhang, Mingyang Du, Xiao Tan, and Xiang Bai. Seeing the future, perceiving the future: A unified driving world model for future generation and perception. _arXiv preprint arXiv:2503.13587_ , 2025. 3 

- [24] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. In _ICLR_ , 2023. 5 

- [25] Zhijian Liu, Haotian Tang, Alexander Amini, Xinyu Yang, Huizi Mao, Daniela L Rus, and Song Han. Bevfusion: Multi-task multi-sensor fusion with unified bird’s-eye view representation. In _ICRA_ , 2023. 1, 6, 10 

- [26] Enhui Ma, Lijun Zhou, Tao Tang, Zhan Zhang, Dong Han, Junpeng Jiang, Kun Zhan, Peng Jia, Xianpeng Lang, Haiyang Sun, et al. Unleashing generalization of end-to-end autonomous driving with controllable long video generation. _arXiv preprint arXiv:2406.01349_ , 2024. 2 

- [27] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Xinze Chen, Guanghong Jia, Guan Huang, and Wenjun Mei. Recondreamer-rl: Enhancing reinforcement learning via diffusion-based scene reconstruction. _arXiv preprint arXiv:2508.08170_ , 2025. 1 

- [28] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Guan Huang, Chen Liu, Yuyin Chen, Yida Wang, Xueyang Zhang, et al. Recondreamer: Crafting world models for driving scene reconstruction via online restoration. In _CVPR_ , 2025. 1 

- [29] Xuanchi Ren, Yifan Lu, Tianshi Cao, Ruiyuan Gao, Shengyu Huang, Amirmojtaba Sabour, Tianchang Shen, Tobias Pfaff, Jay Zhangjie Wu, Runjian Chen, et al. Cosmos-drive-dreams: Scalable synthetic driving data generation with world foundation models. _arXiv preprint arXiv:2506.09042_ , 2025. 1, 2, 4 

14 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

- [30] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image synthesis with latent diffusion models. In _CVPR_ , 2022. 2 

- [31] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 1, 2 

- [32] Alexander Swerdlow, Runsheng Xu, and Bolei Zhou. Street-view image generation from a bird’s-eye view layout. _IEEE Robotics and Automation Letters_ , 2024. 2 

- [33] Tao Tang, Enhui Ma, Xia Zhou, Letian Wang, Tianyi Yan, Xueyang Zhang, Kun Zhan, Peng Jia, Xianpeng Lang, Jia-Wang Bian, et al. Omnigen: Unified multimodal sensor generation for autonomous driving. In _ACM MM_ , 2025. 3, 6, 7, 9, 10 

- [34] GigaWorld Team, Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Haoyun Li, Jiagang Zhu, Kerui Li, Mengyuan Xu, et al. Gigaworld-0: World models as data engine to empower embodied ai. _arXiv preprint arXiv:2511.19861_ , 2025. 1 

- [35] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 6 

- [36] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 2, 4, 6 

- [37] Weijie Wang, Jiagang Zhu, Zeyu Zhang, Xiaofeng Wang, Zheng Zhu, Guosheng Zhao, Chaojun Ni, Haoxiao Wang, Guan Huang, Xinze Chen, et al. Drivegen3d: Boosting feed-forward driving scene generation with efficient video diffusion. _arXiv preprint arXiv:2510.15264_ , 2025. 2 

- [38] Xiaofeng Wang, Zheng Zhu, Yunpeng Zhang, Guan Huang, Yun Ye, Wenbo Xu, Ziwei Chen, and Xingang Wang. Are we ready for vision-centric driving streaming perception? the asap benchmark. In _CVPR_ , 2023. 6 

- [39] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards real-world-drive world models for autonomous driving. In _ECCV_ , 2024. 1, 2, 6, 7 

- [40] Xiaofeng Wang, Zheng Zhu, Guan Huang, Boyuan Wang, Xinze Chen, and Jiwen Lu. Worlddreamer: Towards general world models for video generation via predicting masked tokens. _arXiv preprint arXiv:2401.09985_ , 2024. 2 

- [41] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _CVPR_ , 2024. 1, 2, 6, 7 

- [42] Yuqing Wen, Yucheng Zhao, Yingfei Liu, Fan Jia, Yanhui Wang, Chong Luo, Chi Zhang, Tiancai Wang, Xiaoyan Sun, and Xiangyu Zhang. Panacea: Panoramic and controllable video generation for autonomous driving. In _CVPR_ , 2024. 1, 2, 6, 7 

- [43] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Generalized predictive model for autonomous driving. In _CVPR_ , 2024. 2 

- [44] Kairui Yang, Enhui Ma, Jibin Peng, Qing Guo, Di Lin, and Kaicheng Yu. Bevcontrol: Accurately controlling street-view elements with multi-perspective consistency via bev sketch layout. _arXiv preprint arXiv:2308.01661_ , 2023. 1 

15 

UniDriveDreamer: A Single-Stage Multimodal World Model for Autonomous Driving 

- [45] Zhuoran Yang, Xi Guo, Chenjing Ding, Chiyu Wang, Wei Wu, and Yanyong Zhang. Instadrive: Instanceaware driving world models for realistic and consistent video generation. In _ICCV_ , 2025. 1, 2 

- [46] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models. In _ICCV_ , 2023. 2 

- [47] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _CVPR_ , 2018. 4 

- [48] Yumeng Zhang, Shi Gong, Kaixin Xiong, Xiaoqing Ye, Xiao Tan, Fan Wang, Jizhou Huang, Hua Wu, and Haifeng Wang. Bevworld: A multimodal world model for autonomous driving via unified bev latent space. _arXiv preprint arXiv:2407.05679_ , 2024. 3 

- [49] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xueyang Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, et al. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. In _CVPR_ , 2025. 1 

- [50] Guosheng Zhao, Xiaofeng Wang, Chaojun Ni, Zheng Zhu, Wenkang Qin, Guan Huang, and Xingang Wang. Recondreamer++: Harmonizing generative and reconstructive models for driving scene representation. In _ICCV_ , 2025. 1 

- [51] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. In _AAAI_ , 2025. 1, 2, 6, 7 

- [52] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Bohan Li, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ , 2024. 2 

- [53] Vlas Zyrianov, Xiyue Zhu, and Shenlong Wang. Learning to generate realistic lidar point clouds. In _ECCV_ , 2022. 1, 2, 6, 7 

- [54] Vlas Zyrianov, Henry Che, Zhijian Liu, and Shenlong Wang. Lidardm: Generative lidar simulation in a generated world. In _ICRA_ , 2025. 1, 2, 6 

16 

