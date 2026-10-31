---
title: "Motion Focus Recognition in Fast-Moving Egocentric Video"
date: "2026-01-12"
authors: "Si-En Hong; James Tribble; Alexander Lake; Hao Wang; Chaoyi Zhou; Ashish Bastola"
url: https://arxiv.org/abs/2601.07154
pdf: https://arxiv.org/pdf/2601.07154
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.07154)** / [論文ページ](https://arxiv.org/abs/2601.07154)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Motion Focus Recognition in Fast-Moving Egocentric Video** 

Si-En Hong<sup>1</sup> , James Tribble<sup>1</sup> , Alexander Lake<sup>1</sup> , Hao Wang<sup>1</sup> , Chaoyi Zhou<sup>1</sup> , Ashish Bastola<sup>1</sup> , Siyu Huang<sup>1</sup> , Eisa Chaudhary<sup>2</sup> , Brian Canada<sup>2</sup> , Ismahan Arslan-Ari<sup>3</sup> , and Abolfazl Razi<sup>1*</sup> 

1Clemson University, SC, USA 

2University of South Carolina Beaufort, SC, USA 

3University of South Carolina, SC, USA 

_{_ sienh, jjtribb, lake8, hao9, chaoyiz, abastol, siyuh, arazi _}_ @clemson.edu eisa@email.uscb.edu, bcanada@uscb.edu, arslanai@mailbox.sc.edu 

## **Abstract** 

_From Vision–Language–Action (VLA) systems to robotics, existing egocentric datasets primarily focus on action recognition tasks, while largely overlooking the inherent role of motion analysis in sports and other fast-movement scenarios. To bridge this gap, we propose a real-time motion focus recognition method that estimates the subject’s locomotion intention from any egocentric video. We leverages the foundation model for camera pose estimation and introduces system-level optimizations to enable efficient and scalable inference. Evaluated on a collected egocentric action dataset, our method achieves real-time performance with manageable memory consumption through a sliding batch inference strategy. This work makes motion-centric analysis practical for edge deployment and offers a complementary perspective to existing egocentric studies on sports and fast-movement activities._<sup>1</sup> _Our code and dataset are available on: https://arazi2.github.io/aisends. github.io/project/VisionGPT_ 

## **1. Introduction** 

In fast human movement, egocentric perception is fundamentally more challenging than vision tasks developed for autonomous vehicles or rigid robotic platforms [6]. Unlike vehicle-mounted cameras operating under stable kinematic constraints, egocentric video is shaped by frequent head movements, body sway, and intentional gaze shifts, leading to unstable viewpoints and noisy motion feedback [2]. In such settings, common assumptions, such as image- 

*Corresponding author. 

> 1Research reported in this publication was supported in part by the NSF and SC EPSCoR Program under award number (NSF Award # OIA2242812 and SC EPSCoR 26-CRP03). The views, perspective, and content do not necessarily represent the official views of the SC EPSCoR Program nor those of the NSF. 

center relevance and consistent camera orientation, break down, making reliable real-time ego-motion estimation particularly challenging [4]. 

Most existing attention and relevance estimation methods for egocentric vision rely primarily on static or appearance-based saliency to identify important regions and objects [5]. While effective in relatively stable settings, such approaches can introduce substantial bias in high-motion environments, as visually salient but motioninconsistent objects often appear only transiently and disappear within a few frames. Consequently, static saliency fails to capture the temporally persistent information that is most informative for understanding ego-motion and shortterm movement intent [7]. 


Figure 1. (a) Selected frame from the dataset collected during the winter season. (i) is the raw city street image, (ii) is the motionfocus map, and (iii) is the motion-guided depth map. (b) is the example camera system for data capturing. 

To address this limitation, we propose a real-time motion focus recognition method that estimates human locomotion trends from egocentric video while being robust to irregular camera movement noise induced by natural head and body movements. Our approach is grounded in physical priors of camera pose dynamics and does not require additional training, enabling flexible motion trend estimation under highly dynamic viewpoints. Furthermore, the proposed method can be embedded into arbitrary camera pose 


Figure 2. Framework for motion focus prediction and projection. 

estimation frameworks with minimal computational cost, supporting real-time deployment on resource-constrained systems in fast-movement settings. 

Specifically, we adopt the camera pose prediction from an existing foundation model and apply deep systematic optimization for real-time egocentric motion recognition [3]. To overcome the shortage of existing egocentric datasets in fast-movement scenarios, we collect a lightweight egocentric action dataset and incorporate real camera intrinsics as physical constraints for error compensation, enabling more stable motion focus recognition under real-world capture conditions. Experimental results show that the predicted motion focus highlights the videographer’s locomotion trend. **2. Method** 

### **2.1. Data Collection** 

We collect an egocentric action video dataset through inperson acquisition to capture realistic human locomotion under dynamic environments. All videos are recorded using a single monocular handheld mobile phone carried by a walking subject, resulting in camera motion that reflects natural translation, head turns, and body-induced perturbations. 

|Scene|Clips|Resolution|FPS|Total length|Total Frames|
|---|---|---|---|---|---|
|Suburban|42|960x544|30|37 mins|65934|
|City|56|1920x1080|30|79 mins|5464|
|Town|36|3840x2160|30|24 mins|21528|
|Campus|72|1920x1080|60|75 mins|269550|


ego-motion dynamics. In total, the dataset contains action video clips captured at varying resolutions and frame rates, as summarized in Table 1. 

### **2.2. System Optimization for Real-Time Inference** 

Since Depth Anything 3 is primarily designed for offline inference in industrial applications [3], processing an entire long video in one pass quickly exceeds GPU memory. During our testing on a 24 GB desktop GPU, sequences exceeding 1000 frames fail due to running out of memory. To avoid this, we split the video into overlapping batches, perform inference per batch, and align them temporally. This reduces peak memory usage while preserving a complete, consistent sequence of depth maps and camera poses, as shown in Figure 3. 


Figure 3. Depth alignment in the real-time inference. We applied a sliding window for consecutive inference in real time. 

Table 1. Collected egocentric video clips for motion analysis tasks. 

Data is collected during winter conditions across diverse and challenging environments, including outdoor sidewalks and pedestrian walkways with uneven surfaces and icy roads, as shown in Figure 1. The dataset further includes multiple locomotion patterns, such as walking, scooter riding, and biking, together with motion variations including turning, slowing down, and brief stopping, producing rich 

Specifically, to handle extended video streams _{_ **I** _t}_ under memory constraints while maintaining real-time performance, we adopt a sliding-window inference strategy. The continuous stream is partitioned into overlapping segments (batches) of size _L_ , where consecutive windows share _O_ frames to ensure temporal context, as shown in Figure 3. 

For each batch, the model predicts depth maps _{_ **D** _t}_ and camera extrinsics _{_ **T**<sup>_w_</sup> _t_<sup>_→c_</sup> _}_ in a local coordinate frame. To resolve the coordinate ambiguity between consecutive 

batches, we perform an incremental anchoring process. Let _tanchor_ denote the transition frame shared by the current and previous windows. We compute a rigid transformation to align the current batch’s local origin to the terminal pose of the previous trajectory, effectively stitching the segments into a unified world coordinate system. 

Specifically, to maintain the physical consistency of the motion, we lock the gravity-aligned rotation (pitch and roll) and propagate only the horizontal yaw and translation across batch boundaries. This incremental anchoring avoids the global drift typical of large-scale Sim(3) optimization while preserving the predictive power of the foundation model for long-range navigation [3]. Following the alignment, only the newly processed, non-overlapping frames are emitted, ensuring a continuous and temporally coherent flow of depth and pose estimates for downstream motion analysis. 

|Model|Resolution|Batch Size|FPS|GPU Mem.|
|---|---|---|---|---|
|DA3 Base|504|60|31.53|8113 MB|
|DA3 Base|384|60|34.01|5556 MB|
|DA3 Base|384|30|28.65|4501 MB|
|DA3 Small|504|60|32.95|4609 MB|
|DA3 Small|384|60|38.44|3437 MB|
|DA3 Small|504|30|35.87|3677 MB|
|DA3 Small|384|30|32.32|3064 MB|


Table 2. Performance of DA3. 

We evaluate the batch inference strategy under different configurations to assess its suitability for real-time deployment. As shown in Table 2, the DA3 base model achieves 31.53 FPS with approximately 8 GB GPU memory at a batch size of 60, and further improves to 34.01 FPS with reduced memory usage when the resolution is lowered to 384 px. While smaller batch sizes reduce memory consumption, they also lead to decreased throughput due to increased I/O and scheduling overhead. By replacing the base model with the DA3 small variant, our framework maintains stable real-time performance above 30 FPS with GPU memory usage below 5 GB, enabling practical deployment on consumer-grade hardware. 

### **2.3. Motion Focus Recognition** 

To enable motion-aware prioritization in fast movements, we introduce a lightweight Motion Focus Recognition module that estimates the impact region induced by the user’s locomotion. The core intuition is that the acceleration vector induced by camera translation, when projected onto the image plane, provides a physically grounded focus of attention indicating where near-field interactions or potential collisions are most likely to occur [1]. 

Let **T**<sup>_w_</sup> _t_<sup>_→c_</sup> _∈_ R<sup>4</sup><sup>_×_4</sup> denote the camera pose at time _t_ , expressed as a world-to-camera transformation. We first re- 

cover the camera positions in the world coordinate system by inverting the poses: 


To characterize the dynamic trend of the trajectory, we compute the discrete acceleration vector in world space, **a** _w_ , by considering three consecutive pose samples: 


To align this motion trend with the user’s current egocentric perspective, the acceleration vector is transformed from the world frame into the local camera coordinate frame: 


where **R**<sup>_w_</sup> _t_<sup>_→c_</sup> is the rotation matrix of **T**<sup>_w_</sup> _t_<sup>_→c_</sup> . The local vector **a** _c_ = ( _ax, ay, az_ )<sup>_⊤_</sup> encapsulates the directional change of motion relative to the optical axis. 

Assuming a pinhole camera model with an intrinsic matrix 


We project the motion direction onto the image plane to obtain an estimated impact point: 


The coordinate ( _uacc, vacc_ ) serves as the center of a motion-induced saliency map. Unlike velocity-based projection, this acceleration-based focus effectively anticipates the user’s intent to turn or decelerate, as shown in Figure 4. 


Figure 4. Motion focus calculation process. We first calculate the camera center and project the acceleration vector to the _n_ -th frame. Then we aggregate _N_ camera centers and apply Gaussian kernels for rendering. The final results represent the camera movement trends, which aligned with the defined motion focus. 

As shown in Figure 4, we then construct a motion focus map by aggregating _N_ motion points (e.g., _N_ = 15) in the image plane. Each motion point contributes a Gaussian kernel centered at its projected pixel location, with the kernel 


Figure 5. Visualization of motion focus. Left: raw image with predicted motion focus map; Right: depth map guided by motion direction. 

spread modulated by the corresponding motion magnitude to reflect its spatial influence. The final focus map is obtained by summing all kernels and normalizing the result: 


where ( _ui, vi_ ) denotes the _i_ -th motion point, _si_ its motion magnitude, _σ_ a scale factor, and _Z_ a normalization constant. The resulting motion focus allowing the system to prioritize recognition in regions that align with the predicted future path. 

### **2.4. Qualitative Analysis for Motion Focus** 

We conduct qualitative analysis on 30 video clips and select 3 representative scenes. Visual inspection reveals that the proposed motion focus mechanism operates robustly across diverse navigation scenarios, consistently highlighting motion-relevant regions. 

As illustrated in Figure 5, the proposed motion focus consistently highlights motion-relevant regions across diverse egocentric scenarios. In Scene 1 (scooter), static but semantically salient objects such as parked vehicles are suppressed, while nearby obstacles along the walking path (e.g., poles, trees, and trash bins) are emphasized, demonstrating effective filtering of action-irrelevant visual clutter. In Scene 2 (walking), the predicted motion center adapts to vertical locomotion, shifting toward the ascending direction rather than remaining fixed at the image center. Furthermore, during Scene 3 (biking), when head orientation and body movement direction diverge, motion focus remains aligned with the torso-driven locomotion trend, prioritizing areas along the actual movement path. 

## **3. Conclusion** 

This work shows that motion–driven analysis can serve as a lightweight and practical foundation for real-time egocentric perception, complementing existing action- and 

semantics-driven approaches in sports and fast-movement scenarios. More broadly, our findings suggest that grounding egocentric perception in physically significant motion is essential for understanding sports, robotics, and other dynamic embodied activities. By enabling lightweight, realtime ego-motion reasoning, this work takes a step toward more reliable and human-centered perception systems that can support safety, performance analysis, and assistive feedback in challenging real-world environments. 

## **References** 

- [1] Masaki Fukuchi, Naotsugu Tsuchiya, and Christof Koch. The focus of expansion in optical flow fields acts as a strong cue for visual attention. _Journal of Vision_ , 9(8):137–137, 2009. 3 

- [2] Hassan A Karimi, Ming Jiang, and Rui Zhu. Pedestrian navigation services: challenges and current trends. _Geomatica_ , 67 (4):259–271, 2013. 1 

- [3] Haotong Lin, Sili Chen, Junhao Liew, Donny Y Chen, Zhenyu Li, Guang Shi, Jiashi Feng, and Bingyi Kang. Depth anything 3: Recovering the visual space from any views. _arXiv preprint arXiv:2511.10647_ , 2025. 2, 3 

- [4] Miao Liu, Siyu Tang, Yin Li, and James M Rehg. Forecasting human-object interaction: joint prediction of motor attention and actions in first person video. In _European conference on computer vision_ , pages 704–721. Springer, 2020. 1 

- [5] Minglang Qiao, Mai Xu, Shijie Wen, Lai Jiang, Shengxi Li, Tao Xu, Yunjin Chen, and Leonid Sigal. Saliency prediction of sports videos: A large-scale database and a self-adaptive approach. In _ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ , pages 6615–6619. IEEE, 2024. 1 

- [6] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2446–2454, 2020. 1 

- [7] Lingfeng Yang, Zhenyuan Chen, Xiang Li, Peiyang Jia, Liangqu Long, and Jian Yang. Agent-based video trimming. _arXiv preprint arXiv:2412.09513_ , 2024. 1 

