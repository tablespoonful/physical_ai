---
title: "Embody4D: A Generalist Data Engine for Embodied 4D World Modeling"
date: "2026-05-03"
authors: "Peiyan Tu; Hanxin Zhu; Jingwen Sun; Shaojie Ren; Cong Wang; Yuyan Xu"
url: https://arxiv.org/abs/2605.01799
pdf: https://arxiv.org/pdf/2605.01799
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2605.01799)** / [論文ページ](https://arxiv.org/abs/2605.01799)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Embody4D: A Generalist Data Engine for Embodied 4D World Modeling** 

**Peiyan Tu**<sup>**1,2,***</sup> **, Hanxin Zhu**<sup>**3,***</sup> **, Jingwen Sun**<sup>**3,2**</sup> **, Shaojie Ren**<sup>**4,2**</sup> **, Cong Wang**<sup>**4,2**</sup> **, Yuyan Xu**<sup>**5,2**</sup> **, Jiayi Luo**<sup>**6,2**</sup> **, Xiaoqian Cheng**<sup>**3,2**</sup> **, Zhibo Chen**<sup>**3,2,†**</sup> 

**1Zhejiang University, 2Beijing Zhongguancun Academy, 3University of Science and Technology of China,** 

**4Institute of Automation, Chinese Academy of Sciences, 5Shanghai Jiao Tong University,** 

**6Beihang University** 

***Equal contribution. †Corresponding author.** 

### **Abstract:** 

Embodied agents require robust and comprehensive 3D spatiotemporal representations to support spatial reasoning, manipulation understanding, and downstream decision making. However, existing robot data are typically captured from fixed or sparse viewpoints, providing only partial and view-dependent observations, which limits multi-view perception and generalization across viewpoints. Given the difficulty of collecting additional viewpoints in real-world settings, we propose Embody4D, a dedicated video-to-video world model for embodied scenarios to bridge this observation gap by transforming a monocular robot video into novel-view videos from flexible target camera viewpoints. First, to tackle training data scarcity, we introduce a 3D-aware compositional synthesis pipeline to curate a heterogeneous dataset compositing cross-embodiment robotic arms with diverse backgrounds, promoting broad generalization. Second, to enforce geometric stability, we devise a latent confidence-aware expert modulation strategy, which estimates the reliability of warped latent priors and adaptively routes regions to copy, repair, or inpaint experts for spatiotemporally consistent 4D generation. Finally, to enhance the fidelity of the manipulation, we incorporate an interaction-aware attention mechanism that explicitly attends to the robotic interaction regions. Extensive experiments show that Embody4D achieves stateof-the-art performance on visual evaluation benchmarks, while both simulated and real-world robotic experiments further demonstrate its effectiveness as a robust data engine for synthesizing high-fidelity, view-consistent videos that empower downstream robotic planning and learning. The anonymous project page: `https://peiyantu.github.io/Embody4D/page.html` 

**Keywords:** World Model, Novel View Synthesis, 4D Generation, Data Engine 

## **1 Introduction** 

Embodied agents require robust and comprehensive 3D spatiotemporal representations to support spatial reasoning, manipulation understanding, and downstream decision making. However, while the physical world is inherently three-dimensional, many existing models for downstream policy learning remain confined to 2D pixel observations [1, 2] or rely on limited, fixed multi-view captures [3]. As a result, they struggle to generalize across unseen viewpoints or construct complete 3D spatiotemporal scene representations. This limitation results in impoverished spatial representations, depriving embodied agents of the comprehensive multi-view information required for robust manipulation and spatial reasoning [4]. 

A key bottleneck behind this limitation is the scarcity of dense multi-view video data with flexible viewpoint coverage in embodied scenarios [5]. Although simulators offer scalable access to controllable multi-view observations, the resulting data often remain misaligned with real-world robot interactions, particularly in appearance, dynamics, and contact-rich behaviors [6]. In contrast, ac- 


Figure 1: **Illustration of the proposed Embody4D.** A generalist data engine that transforms monocular robot videos into videos from flexible viewpoints for embodied 4D world modeling, thereby enhancing downstream task performance. 

quiring dense multi-view videos in the real world requires carefully calibrated and synchronized camera systems, making large-scale collection prohibitively expensive and difficult to deploy [7]. 

This motivates a generalist data engine for transforming widely available monocular or sparsely captured robot videos into dense multi-view videos under flexible camera viewpoints. Such videos faithfully capture the same robot-object interaction across viewpoints and time, forming a temporally coherent multi-view representation of the dynamic 3D scene. We refer to this representation as 4D embodied data, which provides embodied agents with dense spatiotemporal supervision for crossview generalization, scene understanding, and manipulation reasoning [8]. 

To this end, we propose **Embody4D** , a generalist data engine for embodied 4D world modeling, as illustrated in Fig. 1. Given a monocular robot video, Embody4D generates temporally coherent novel-view videos from flexible target viewpoints, thereby bridging the gap between limited 2D recordings and rich 4D embodied data. 

Specifically, 4D generative models are fundamentally constrained by the scarcity of multi-view dynamic training data, a challenge that becomes even more acute in embodied scenarios. To mitigate this issue, we first establish a **compositional 4D embodied data synthesis** pipeline to composite 30 cross-morphology manipulators from the MuJoCo Menagerie [9] with diverse real-world backgrounds. This heterogeneous data construction significantly enhances Embody4D’s generalization capabilities. To stabilize the generative process, we devise a **latent confidence-aware expert modulation** strategy, which converts the reliability of the warped prior into token-wise expert routing in the latent space. By adaptively assigning tokens to _copy_ , _repair_ , and _inpaint_ experts, our method preserves reliable projections, corrects geometric misalignments, and completes uncertain regions, thereby improving spatiotemporal coherence and texture fidelity during viewpoint transitions. To further guarantee the fidelity of complex interactions, we introduce an **interaction-aware attention** mechanism that leverages segmentation-based motion biases to decouple manipulation dynamics from the background [10], thereby preserving the structural integrity of interacting entities. Finally, extensive experiments across diverse benchmarks demonstrate that Embody4D achieves state-ofthe-art performance. Furthermore, comprehensive evaluations across simulation benchmarks and real-world robotic platforms validate our model as a robust data engine, capable of generating highfidelity and temporally coherent video data to improve downstream robotic planning and policy learning. 

In summary, our key contributions can be concluded as follows: 

- We propose Embody4D, a 4D world model that synthesizes novel-view videos from monocular 

- videos under flexible viewpoint control, providing comprehensive multi-view representations. 

- We design a unified generation framework with three key components: compositional data syn- 

- thesis to alleviate data scarcity, latent confidence-aware expert modulation to improve cross-view consistency, and interaction-aware attention to preserve the manipulation fidelity of dynamic robotobject interactions. 

2 

_•_ We achieve state-of-the-art performance across visual benchmarks, while simulation benchmarks and real-world robotic experiments further demonstrate the effectiveness of Embody4D in empowering downstream robotic planning and policy learning. 

## **2 Related Works** 

**Generative Video Models as Data Engines.** Existing robotic data engines based on video generation mainly convert human object interaction videos into robot demonstrations [11, 12] or synthesize robot videos conditioned on manipulator actions [13, 14, 15, 16]. For example, Human2Robot [11] generates robot videos from human demonstrations and then estimates robot actions from the generated videos, but such human to robot transfer suffers from inaccurate action recovery due to the embodiment and action space gap. Action conditioned methods such as EnerVerse [16] train video world models conditioned on robot actions to generate interactive robot rollouts, yet they still struggle to strictly align generated visual dynamics with input actions and may produce physically implausible interactions, particularly in fine grained robot object manipulation. We instead explore a novel view synthesis paradigm that expands existing monocular robot videos into flexible target camera viewpoints without generating new action trajectories. By preserving accurate action annotations and enriching each trajectory with multi view observations, our approach alleviates the limited viewpoint bias of robot datasets, strengthens 3D spatiotemporal modeling and improves viewpoint generalization for downstream policy learning. 

**4D Generation Model.** Video-to-video 4D generation aims to synthesize temporally and spatially consistent dynamic 3D scenes from monocular videos, providing comprehensive environmental representations for embodied intelligence and content creation [8, 17, 18]. Nevertheless, progress in this domain remains severely constrained by the scarcity of high-quality training data. [19, 20]. Early approaches [21] like DimensionX [22] employs LoRA fine-tuning to extend single-view videos into multi-view sequences but lacks the capability for precise viewpoint control. To mitigate data and camera control limitations, recent “warp-then-inpaint” paradigms [23], represented by Trajectory Crafter [24], construct pseudo-4D data with camera information from monocular videos to serve as generation conditions. Conversely, ReCamMaster [25] tackles these issues by synthesizing 4D data via game engines and optimizing the camera information injection mechanism. Inspired by these advancements, to address the scarcity of high-quality 4D data in embodied scenarios, we leverage the MuJoCo simulator to construct a dataset exhibiting high 4D consistency across diverse scenes and robotic arm morphologies. Furthermore, we adopt and refine the “warp-then-inpaint” paradigm to achieve enhanced generation quality. 

## **3 Methodology** 

**Preliminary: Video Diffusion Models.** Video diffusion models generate videos by learning to reverse a gradual noising process [26]. Given a clean video _x_ 0 _∈_ R<sup>_n×_3</sup><sup>_×h×w_</sup> , Gaussian noise _ϵ ∼N_ (0 _, I_ ) is progressively injected to obtain noisy samples at different timesteps. To improve efficiency, latent video diffusion models perform this process in the latent space of a pretrained 3D VAE, where the video is encoded as _z_ 0 = _E_ ( _x_ 0). A denoising network, commonly implemented with a Diffusion Transformer (DiT), is trained to predict the injected noise from the noisy latent _zt_ : 


where _c_ denotes optional conditional information, such as text tokens, source observations, or camera conditions. During inference, Gaussian latent noise is iteratively denoised into clean latent tokens, which are decoded by the VAE decoder _D_ to produce the final video _x_ ˆ = _D_ ( _z_ 0) [27]. 

**Compositional 4D Embodied Data Synthesis.** To address the scarcity of embodied 4D data and improve cross-embodiment generalization, we design a compositional data synthesis strategy for constructing view-consistent robotic 4D videos. As shown in Fig. 2 (left), we select 30 embodied models from MuJoCo Menagerie [28], including humanoid robots, single-arm manipulators, dualarm manipulators, and small grippers. Each model is controlled in MuJoCo to perform random 

3 


Figure 2: **Overview of Embody4D.** We build paired embodied 4D training data through compositional synthesis and adopt a “warp-then-inpaint” framework for novel-view video generation. Given a source video, Embody4D reconstructs dynamic geometry, warps RGB/masks to target views, and generates the final video with confidence-aware modulation and interaction-aware attention. 

motions around its default pose, producing diverse foreground robot dynamics. For background construction, we sample image pairs from DL3DV [29]. Candidate pairs are first selected by minimizing camera translation within fixed-interval frames, and then filtered with GPT-4o [30] to ensure that the scene center remains visible across views, resulting in temporally consistent real-world backgrounds. 

To obtain view-consistent foreground-background composition, we configure two virtual MuJoCo cameras whose extrinsics are aligned with the selected DL3DV image pair. The robot is first composited into the reference view with random rotation and scaling. For the second view, we further introduce a 3D anchor tracking strategy to preserve geometric consistency across viewpoints. Specifically, VGGT [31] is used to reconstruct the 3D geometry of source-view video and estimate per-pixel depth together with camera poses. Let _Isrc_ denote the first 49 frames of the source video, we randomly sample a subset _S ⊂Isrc_ with _|S|_ = 5. For each sampled frame _k ∈S_ , we lift the robot center **u** _k_ to the VGGT reconstructed world coordinate system and then transform it into the target camera coordinate system as 


where _zk_ is the estimated depth, **u** ˜ _k_ is the homogeneous image coordinate, ( **R** _k,_ **T** _k_ ) denotes the source-view extrinsics, and ( **R** _t_<sup>_′_</sup> _,_ **T** _t_<sup>_′_</sup> ) denotes the VGGT-estimated target-view extrinsics. To reduce depth and pose noise, we average the transformed points in the target camera coordinate system to obtain a robust 3D anchor: 


Finally, this anchor is projected onto the target image plane as **u** ˜ _t′ ∼_ **KP**<sup>¯</sup><sup>_c_</sup> _t_<sup>_′_, followed by homoge-</sup> neous normalization to obtain the target-view robot center **u** _t′_ for accurate second-view composition. 

**Latent Confidence-Aware Expert Modulation.** Recent 4D novel-view generation methods often follow a “warp-then-inpaint” paradigm [24, 23], where source-view observations are first projected to the target camera using reconstructed geometry and then refined by a generative model. However, the projected prior is spatially heterogeneous: well-aligned regions should be preserved, geometrically inconsistent regions require correction, and disoccluded or highly uncertain areas demand completion. This motivates a region-adaptive formulation of target-view synthesis, rather than uniform denoising. To this end, we propose Latent Confidence-Aware Expert Modulation, which decomposes target-view generation into three confidence-conditioned behaviors: _copy_ , _repair_ , and _inpaint_ [32]. Instead of relying on a binary valid mask to impose a coarse projected/unprojected partition, we learn a continuous latent confidence map that estimates the reliability of the warped 

4 


Figure 3: **Interaction-Aware Block.** The module injects mask-derived interaction biases into cross attention to prioritize manipulation regions and enhance cross-view consistency. (qualitative comparison in heatmaps). 

prior. This map provides a soft routing signal: reliable regions are encouraged to copy the warped content, moderately unreliable regions are routed to repair, and highly uncertain or missing regions are routed to inpaint. 

To supervise this routing signal, we use the warp-to-target discrepancy in the VAE latent space as an oracle measure of correction demand [33]. Given a warped video **x** _w_ and its ground-truth target video **x** _t_ , a frozen VAE encoder _E_ ( _·_ ) [34] maps them into a shared latent space. The latent residual _E_ ( **x** _t_ ) _−E_ ( **x** _w_ ) characterizes the ideal correction required to transform the warped prior toward the target. Its magnitude naturally reflects the reliability of the warped latent: smaller discrepancies indicate content that can be largely preserved, while larger discrepancies reveal regions that require repair or completion. 

To obtain a routing signal without relying on the ground-truth target video, we train a lightweight 3D U-Net _fϕ_ [35] to predict the latent correction from available conditioning inputs, including the warped latent _E_ ( **x** _w_ ) and the geometric mask **M** _s_ resized to the latent resolution: 


We aggregate the predicted residual magnitude along the channel dimension to obtain a scalar correction-demand map, which is then converted into a continuous routing cue for the _copy_ , _repair_ , and _inpaint_ experts. 

During generative training, this routing cue is tokenized and mapped into expert weights **A**<sup>tok</sup> _∈_ R<sup>_B×N×_3</sup> . For the _l_ -th Transformer block, let **u**<sup>_l_</sup> _n_<sup>=FFN</sup><sup>_l_(¯</sup><sup>**h**</sup><sup>_l_</sup> _n_<sup>) denote the standard FFN output of</sup> token _n_ , where **h**<sup>¯</sup><sup>_l_</sup> _n_<sup>is the normalized hidden state before the FFN. We augment this FFN branch with</sup> a routing-adaptive expert residual: 


Here, _Er_<sup>_l_denotes the expert for route</sup><sup>_r_,</sup><sup>**A**tok</sup> _n,r_<sup>is the corresponding token-level routing weight,</sup><sup>_s_con-</sup> trols the expert residual strength, and **g** _n_<sup>_l_is the FFN gate inherited from the Transformer block.This</sup> design preserves the original FFN pathway as a stable generative backbone, while using confidenceaware expert residuals to adaptively allocate modeling capacity across copied, repaired, and inpainted regions. 

**Embodied Interaction-Aware Attention.** The core idea of Embodied Interaction-Aware Attention is to explicitly bias the model toward dynamic robot-object interaction regions during novel-view synthesis. To compensate for the limited object manipulation in our synthetic data, we construct pseudo-4D pairs from monocular robotic manipulation videos using a forward-backward view cycle: the source video is warped to a sampled novel view and then warped back to the original source view, yielding pseudo paired supervision for view-consistent embodied 4D generation [24]. For these data, we extract temporally consistent interaction masks **M** that cover both the robotic arm 

5 

and manipulated objects. Specifically, we adopt MemFlow [36] for simulation or stable videos, and use SAM3 [37] for real-world sequences with camera jitter. For our synthetic data, the arm foreground masks are directly obtained from rendering. These masks provide explicit motion priors, indicating where the model should focus when synthesizing high-dynamic embodied interactions. 

Given queries **Q** from the synthesized features and keys/values **K** _,_ **V** from the reference features [38], we decompose attention into a global path and an interaction-guided path: 


Here, **M** _i,j_ denotes a pairwise token-level interaction indicator, where **M** _i,j_ = 1 if both query token _i_ and key token _j_ correspond to the robot-object interaction region after downsampling the pixellevel mask to the attention resolution, and **M** _i,j_ = 0 otherwise. The global path preserves overall scene context, while the guided path increases the attention response on interaction regions through the mask-induced bias **B** . Finally, the two paths are fused with a curriculum coefficient _α_ : 


allowing the model to progressively shift from global structure modeling to fine-grained embodied interaction modeling during training. 

## **4 Experiments** 

**Dataset.** To train this model, we initially utilize a curated dataset of 23K 4D samples synthesized via foreground-background composition, enabling the model to learn diverse robotic arm morphologies and enhancing its 4D consistency. Subsequently, we leverage 24K monocular embodied data uniformly sampled from five datasets (AGIBOT [7], Rh20t [39], Robset [40], Bc-z [41], and InterndataA1 [42]) to learn real-world robotic arm interactive operations. 

We evaluate our method on a held-out test set of 120 monocular videos that are disjoint from the training data and cover diverse robotic embodiments, scenes, and manipulation scenarios. 

**Implementation.** We fine-tune Embody4d based on the pretrained TrajectoryCrafter [24] architecture. During training, the frame resolution is fixed at 384×672, and the video length is set to 49 frames. Both training stages use a batch size of 2 and are conducted on 8 A100 GPUs. We apply vggt [31] as the reconstruction foundation model for estimating camera parameters and depth maps. 

**Baselines and Metrics.** For a fair comparison, we evaluate our approach against several state-ofthe-art baselines, including camera-controlled video generation models and point cloud rendered multi-view generation models, i.e., TrajectoryCrafter [24], ReCamMaster [25], Ex-4D [43], and Reangle-A-Video [44]. For video generation evaluation, we strictly follow the VBench [45] protocol, reporting scores across multiple dimensions: Subject Consistency, Background Consistency, Temporal Flickering, Motion Smoothness, and Imaging Quality. In addition, we evaluated the 3D consistency metric on the MEt3R [46] benchmark. 

### **4.1 Comparison With Other Methods** 

We compare our method with existing baselines in Fig. 10 and Tab. 1. Qualitatively, ReCamMaster suffers from artifacts and geometric distortions under large viewpoint changes, as its view transformation is mainly driven by camera extrinsics without exploiting source-video geometric priors. Reangle-A-Video and Ex-4D, which rely on LoRA-based fine-tuning, often exhibit incomplete hole filling and degraded visual quality in challenging regions, while the previous state-of-the-art TrajectoryCrafter tends to hallucinate fine structures around robotic arms and grippers. In contrast, our method produces high-fidelity novel-view embodied videos with stronger 4D consistency and more reliable manipulation details. Quantitatively, our approach achieves the best results across 

6 

Table 1: **Quantitative comparisons. Bold** : Best. Underline: Second Best. Our method consistently outperforms previous solutions on both VBench and MEt3R 

|**VBench**_↑_<br>**Method**<br>Subject<br>Background<br>Tempor|<br>**MEt3R**_↓_<br>al<br>Motion<br>Imaging<br>3D Consistency|
|---|---|
|ReCamMaster [25]<br>0.8981<br>0.8976<br>0.9717<br>Ex-4D [43]<br>0.8088<br>0.8906<br>0.9213<br>Reangle-A-Video [44]<br>0.9152<br>0.9224<br>0.9711<br>TrajectoryCrafter [24]<br>0.9202<br>0.9388<br>0.9714<br>**Ours**<br>**0.9351**<br>**0.9491**<br>**0.9734**|0.9841<br>0.5914<br>0.2454<br><br>0.9742<br>0.5732<br>0.2713<br><br>0.9879<br>0.6437<br>0.2288<br><br>0.9911<br>0.6257<br>0.2040<br><br>**0.9937**<br>**0.6566**<br>**0.1681**|
|**Source**<br>**video**||
|**ReCam**<br>**master**||
|**Trajectory**<br>**Crafter**||
|**Ex-4D**||
|**Reangle**<br>**Video**||
|**Ours**||


Figure 4: **Qualitative comparisons of novel view video synthesis.** Our method achieves better structural consistency and visual quality than baselines. 

all evaluated metrics, establishing a new state of the art and demonstrating superior robustness, visual realism, and temporal stability for flexible-view embodied video synthesis. More qualitative comparisons are provided in Fig. 20, 21 

### **4.2 Ablation Study** 

We conduct ablation studies to quantify the contribution of each component. Table 2 reTable 2: Ablation study on video generation quality metrics. ports the results of our framework. The baseline is the TrajectoryCrafter backbone fine-tuned **Method** PSNR _↑_ SSIM _↑_ LPIPS _↓_ MEt3R _↓_ only on embodied pseudo-4D data. Adding our Baseline 19.0293 0.6564 0.3303 0.1923 + data 23.1277 0.7899 0.2136 0.1757 compositional 4D embodied data ( _+data_ ) and + data + IA 23.4920 0.7907 0.2112 0.1702 interaction-aware attention ( _+data+IA_ ) pro- **+ data + IA + Expert 23.6397 0.8064 0.1846 0.1681** gressively improves generation quality. The full model ( _+data+IA+Expert_ ), further equipped with latent confidence-aware expert modulation, achieves the best performance, improving PSNR by 24.23% and SSIM by 22.85%, while reducing LPIPS by 44.11% and MEt3R by 12.58%. These results validate the effectiveness of our data curation, interaction-aware attention, and confidence-aware modulation for stable embodied 4D generation. As illustrated in Fig. 6 and Fig. 7, both the proposed modules and the curated robotic data enhance temporal stability, interaction fidelity, and cross-embodiment generalization. 

### **4.3 Downstream Task Performance Evaluation** 

**Simulation Experiments.** In our simulation experiments, we used LIBERO-Plus [47], a generalpurpose single-arm manipulation benchmark built on LIBERO [48], and introduced seven perturbation settings to evaluate policy robustness. To ensure a fair comparison, we fine-tuned _π_ 0 _._ 5 [2] on the 

7 

Table 3: Real-world embodied experiments on FR3 with _π_ 0 _._ 5 Droid. Each task has 10 trials with randomized object positions. T1–T3 are seen tasks and T4–T5 are unseen tasks (OOD). 

|**Task**|**Single-view **|**ReCamMaster [25] **|**TrajCrafter [24]**|**Embody4D**|
|---|---|---|---|---|
|T1 (Grapes_→_Bowl)|5/10|4/10|6/10|**8/10**|
|T2 (Grapes_→_Plate)|5/10|5/10|6/10|**8/10**|
|T3 (Mangoes_→_Bowl)|4/10|2/10|4/10|**9/10**|
|T4 (Lemons_→_Bowl)|1/10|2/10|0/10|**6/10**|
|T5 (Bananas_→_Plate)|1/10|2/10|7/10|**6/10**|
|SR|32%|30%|46%|**74%**|


LIBERO dataset augmented using our method and compared it with the same _π_ 0 _._ 5 model fine-tuned on the original LIBERO dataset. Figure 9 presents representative generation results, while Figure 10 shows an example comparison. 

**Real World Experiments.** Embodied world models offer a promising data engine for robot learning [16, 49]. We study whether Embody4D can enhance multi-view perception for real-world deployment by augmenting monocular robot data with synthesized novel views. Using Embody4D, ReCamMaster, and TrajectoryCrafter, we generate an additional third-person view from a single external-camera dataset and train the state-of-the-art VLA policy _π_ 0 _._ 5 [2] on the augmented data. 

We evaluate on real-world tabletop manipulation with a Franka Research 3 (FR3) arm [50] and a Robotiq 2F-85 gripper. The setup contains two fixed external cameras and one wrist-mounted camera. From 100 human demonstrations, we train four variants: a single-view baseline, Embody4D-augmented two-view training, ReCamMaster-augmented training, and TrajectoryCrafter-augmented training. Policies are tested on five pick-and-place tasks with randomized object placements, including three seen tasks and two unseen OOD tasks, with 10 trials per task. 


Figure 5: **real-world policy success counts** under four experimental settings on seen tasks and OOD unseen tasks 

As shown in Tab. 3 and Fig. 5, Embody4D tasks achieves the highest success rate of 74% and shows superior OOD generalization. These results demonstrate that Embody4D can effectively function as a data engine for downstream embodied policy learning. 

## **5 Limitation** 

A limitation of our current framework lies in the limited temporal horizon of existing video generation models, which commonly support only fixed-length generation, such as 49 or 81 frames [51, 34, 52]. As a result, long input videos must be split into multiple clips for novel-view synthesis. Since each clip is generated independently, stitching them into a full sequence may introduce temporal discontinuities at clip boundaries, causing mild jitter and slightly degrading visual quality. Additional failure cases are shown in Fig. 17. 

## **6 Conclusion** 

We presented Embody4D, a video-to-video 4D world model for Embodied AI that synthesizes flexible novel views from monocular videos. Embody4D combines a scalable compositional data synthesis pipeline with confidence-aware expert modulation and interaction-aware attention, enabling geometrically consistent, temporally stable, and interaction-faithful generation. Extensive experiments demonstrate state-of-the-art synthesis quality and show that Embody4D serves as an effective data engine for downstream robotic policy learning in both simulation and real-world deployment. 

8 

## **References** 

- [1] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [2] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. 

- [3] S. Ye, Y. Ge, K. Zheng, S. Gao, S. Yu, G. Kurian, S. Indupuru, Y. L. Tan, C. Zhu, J. Xiang, et al. World action models are zero-shot policies. _arXiv preprint arXiv:2602.15922_ , 2026. 

- [4] W. Huang, Y.-W. Chao, A. Mousavian, M.-Y. Liu, D. Fox, K. Mo, and L. Fei-Fei. Pointworld: Scaling 3d world models for in-the-wild robotic manipulation. _arXiv preprint arXiv:2601.03782_ , 2026. 

- [5] S. Wu, H. Fei, J. Yang, X. Li, J. Li, H. Zhang, and T.-s. Chua. Learning 4d panoptic scene graph generation from rich 2d visual scene. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 24539–24549, 2025. 

- [6] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [7] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 

- [8] Q. Miao, K. Li, J. Quan, Z. Min, S. Ma, Y. Xu, Y. Yang, P. Liu, and Y. Luo. Advances in 4d generation: A survey. _arXiv preprint arXiv:2503.14501_ , 2025. 

- [9] E. Todorov, T. Erez, and Y. Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 

- [10] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [11] S. Xie, H. Cao, Z. Weng, Z. Xing, H. Chen, S. Shen, J. Leng, Z. Wu, and Y.-G. Jiang. Human2robot: Learning robot actions from paired human-robot videos. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 40, pages 11078–11086, 2026. 

- [12] G. Zhang, Q. Xu, H. Zhang, J. Ma, L. He, Y. Bao, Z. Ping, Z. Yuan, C. Lu, C. Yuan, et al. Unidex: A robot foundation suite for universal dexterous hand control from egocentric human videos. _arXiv preprint arXiv:2603.22264_ , 2026. 

- [13] S. Gao, W. Liang, K. Zheng, A. Malik, S. Ye, S. Yu, W.-C. Tseng, Y. Dong, K. Mo, C.-H. Lin, et al. Dreamdojo: A generalist robot world model from large-scale human videos. _arXiv preprint arXiv:2602.06949_ , 2026. 

- [14] X. Yang, B. Li, S. Xu, N. Wang, C. Ye, Z. Chen, M. Qin, Y. Ding, Z. Zhu, X. Jin, et al. Orv: 4d occupancy-centric robot video generation. _arXiv preprint arXiv:2506.03079_ , 2025. 

9 

- [15] F. Zhu, H. Wu, S. Guo, Y. Liu, C. Cheang, and T. Kong. Irasim: A fine-grained world model for robot manipulation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9834–9844, 2025. 

- [16] Y. Jiang, S. Chen, S. Huang, L. Chen, P. Zhou, Y. Liao, X. He, C. Liu, H. Li, M. Yao, et al. Enerverse-ac: Envisioning embodied environments with action condition. _arXiv preprint arXiv:2505.09723_ , 2025. 

- [17] Y. Lu, W. Luo, P. Tu, H. Li, H. Zhu, Z. Yu, X. Wang, X. Chen, X. Peng, X. Li, et al. 4dworldbench: A comprehensive evaluation framework for 3d/4d world generation models. _arXiv preprint arXiv:2511.19836_ , 2025. 

- [18] L. Kong, W. Yang, J. Mei, Y. Liu, A. Liang, D. Zhu, D. Lu, W. Yin, X. Hu, M. Jia, et al. 3d and 4d world modeling: A survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- [19] X. Li, Q. Zhang, D. Kang, W. Cheng, Y. Gao, J. Zhang, Z. Liang, J. Liao, Y.-P. Cao, and Y. Shan. Advances in 3d generation: A survey. _arXiv preprint arXiv:2401.17807_ , 2024. 

- [20] B. Wen, H. Xie, Z. Chen, F. Hong, and Z. Liu. 3d scene generation: A survey. _arXiv preprint arXiv:2505.05474_ , 2025. 

- [21] Y. Xie, C.-H. Yao, V. Voleti, H. Jiang, and V. Jampani. Sv4d: Dynamic 3d content generation with multi-frame and multi-view consistency. _arXiv preprint arXiv:2407.17470_ , 2024. 

- [22] W. Sun, S. Chen, F. Liu, Z. Chen, Y. Duan, J. Zhang, and Y. Wang. Dimensionx: Create any 3d and 4d scenes from a single image with controllable video diffusion. _arXiv preprint arXiv:2411.04928_ , 2024. 

- [23] D. Lu, A. Liang, T. Huang, X. Fu, Y. Zhao, B. Ma, L. Pan, W. Yin, L. Kong, W. T. Ooi, et al. See4d: Pose-free 4d generation via auto-regressive video inpainting. _arXiv preprint arXiv:2510.26796_ , 2025. 

- [24] M. YU, W. Hu, J. Xing, and Y. Shan. Trajectorycrafter: Redirecting camera trajectory for monocular videos via diffusion models. _arXiv preprint arXiv:2503.05638_ , 2025. 

- [25] J. Bai, M. Xia, X. Fu, X. Wang, L. Mu, J. Cao, Z. Liu, H. Hu, X. Bai, P. Wan, et al. Recammaster: Camera-controlled generative rendering from a single video. _arXiv preprint arXiv:2503.11647_ , 2025. 

- [26] Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [27] F.-A. Croitoru, V. Hondru, R. T. Ionescu, and M. Shah. Diffusion models in vision: A survey. _IEEE transactions on pattern analysis and machine intelligence_ , 45(9):10850–10869, 2023. 

- [28] K. Zakka, Y. Tassa, and M. M. Contributors. Mujoco menagerie: A collection of high-quality simulation models for mujoco. _URL http://github. com/deepmind/mujoco_ _~~m~~ enagerie_ , 2022. 

- [29] L. Ling, Y. Sheng, Z. Tu, W. Zhao, C. Xin, K. Wan, L. Yu, Q. Guo, Z. Yu, Y. Lu, et al. Dl3dv-10k: A large-scale scene dataset for deep learning-based 3d vision. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 22160–22169, 2024. 

- [30] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- [31] J. Wang, M. Chen, N. Karaev, A. Vedaldi, C. Rupprecht, and D. Novotny. Vggt: Visual geometry grounded transformer. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 5294–5306, 2025. 

10 

- [32] H. Zhu, C. Wang, P. Tu, J. Luo, T. He, X. Jin, and Z. Chen. Gta: Advancing image-to-3d world generation via geometry then appearance video diffusion. _arXiv preprint arXiv:2605.12957_ , 2026. 

- [33] Y. Hong, S. Lee, H. Chung, and J. C. Ye. Inversecrafter: Efficient video recapture as a latent domain inverse problem. _arXiv preprint arXiv:2512.05672_ , 2025. 

- [34] W. Hong, M. Ding, W. Zheng, X. Liu, and J. Tang. Cogvideo: Large-scale pretraining for text-to-video generation via transformers. _arXiv preprint arXiv:2205.15868_ , 2022. 

- [35] H. Cao, Y. Wang, J. Chen, D. Jiang, X. Zhang, Q. Tian, and M. Wang. Swin-unet: Unet-like pure transformer for medical image segmentation. In _European conference on computer vision_ , pages 205–218. Springer, 2022. 

- [36] Q. Dong and Y. Fu. Memflow: Optical flow estimation and prediction with memory. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 19068–19078, 2024. 

- [37] N. Carion, L. Gustafson, Y.-T. Hu, S. Debnath, R. Hu, D. Suris, C. Ryali, K. V. Alwala, H. Khedr, A. Huang, et al. Sam 3: Segment anything with concepts. _arXiv preprint arXiv:2511.16719_ , 2025. 

- [38] Y. Balaji, S. Nah, X. Huang, A. Vahdat, J. Song, Q. Zhang, K. Kreis, M. Aittala, T. Aila, S. Laine, et al. ediff-i: Text-to-image diffusion models with an ensemble of expert denoisers. _arXiv preprint arXiv:2211.01324_ , 2022. 

- [39] H.-S. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, and C. Lu. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. _arXiv preprint arXiv:2307.00595_ , 2023. 

- [40] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 4788– 4795. IEEE, 2024. 

- [41] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 

- [42] Y. Tian, Y. Yang, Y. Xie, Z. Cai, X. Shi, N. Gao, H. Liu, X. Jiang, Z. Qiu, F. Yuan, et al. Interndata-a1: Pioneering high-fidelity synthetic data for pre-training generalist policy. _arXiv preprint arXiv:2511.16651_ , 2025. 

- [43] T. Hu, H. Peng, X. Liu, and Y. Ma. Ex-4d: Extreme viewpoint 4d video synthesis via depth watertight mesh. _arXiv preprint arXiv:2506.05554_ , 2025. 

- [44] H. Jeong, S. Lee, and J. C. Ye. Reangle-a-video: 4d video generation as video-to-video translation. _arXiv preprint arXiv:2503.09151_ , 2025. 

- [45] Z. Huang, Y. He, J. Yu, F. Zhang, C. Si, Y. Jiang, Y. Zhang, T. Wu, Q. Jin, N. Chanpaisit, et al. Vbench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21807–21818, 2024. 

- [46] M. Asim, C. Wewer, T. Wimmer, B. Schiele, and J. E. Lenssen. Met3r: Measuring multi-view consistency in generated images. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6034–6044, 2025. 

11 

- [47] S. Fei, S. Wang, J. Shi, Z. Dai, J. Cai, P. Qian, L. Ji, X. He, S. Zhang, Z. Fei, J. Fu, J. Gong, and X. Qiu. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- [48] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _arXiv preprint arXiv:2306.03310_ , 2023. 

- [49] X. Wang, L. Liu, Y. Cao, R. Wu, W. Qin, D. Wang, W. Sui, and Z. Su. Embodiedgen: Towards a generative 3d world engine for embodied intelligence. _arXiv preprint arXiv:2506.10600_ , 2025. 

- [50] S. Haddadin, S. Parusel, L. Johannsmeier, S. Golz, S. Gabl, F. Walch, M. Sabaghian, C. J¨ahne, L. Hausperger, and S. Haddadin. The franka emika robot: A reference platform for robotics research and education. _IEEE robotics & automation magazine_ , 29(2):46–64, 2022. 

- [51] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang, et al. Wan: Open and advanced large-scale video generative models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- [52] A. Ali, J. Bai, M. Bala, Y. Balaji, A. Blakeman, T. Cai, J. Cao, T. Cao, E. Cha, Y.-W. Chao, et al. World simulation with video foundation models for physical ai. _arXiv preprint arXiv:2511.00062_ , 2025. 

12 

## **A Ablation Study** 

**Ablations of Embody4d.** To systematically evaluate the contribution of each module within Embody4D, we conducted ablation studies on two core architectural components: the latent confidenceaware expert modulation mechanism and the interaction-aware attention module. As illustrated in Fig. 6, the confidence-aware strategy performs reliability-conditioned expert routing, adaptively assigning spatial regions to the _copy_ , _repair_ , and _inpaint_ experts based on their estimated projection reliability. This approach preserves fine-grained structural details in high-confidence areas while ensuring seamless geometric and textural transitions, thereby significantly enhancing the spatiotemporal consistency and visual quality of the synthesized videos. Furthermore, the interactionaware attention mechanism introduces a spatial bias focused on manipulation zones, directing the model to prioritize critical robot-object interactions. This ensures superior fidelity in delicate manipulation regions and strengthens the physical plausibility of complex scenarios. Quantitative results in Tab. 2 further demonstrate that these two modules synergistically bolster the stability of Embody4D, enabling the synthesis of highly realistic 4D robotic interaction videos with consistent multi-view structures. 


Figure 6: **Qualitative comparisons of the ablations.** Results of ablation on embodied interactionaware attention and confidence-aware expert modulation strategy. 

**Ablation on the training data.** The dataset curation strategy represents another key contribution of our work, where the model is trained on a hybrid dataset comprising open-source monocular embodied data and compositionally constructed diverse robotic embodied data. To validate its effectiveness, we conducted an ablation study comparing models trained with and without the compositionally constructed data. Qualitative results in Fig. 7 demonstrate that the model lacking diverse robotic data struggles to generalize to unseen robotic structures, frequently producing implausible geometric hallucinations in occluded regions. Conversely, our hybrid training strategy enables the model to internalize robust structural priors, allowing it to synthesize physically consistent robotic poses across various morphologies while maintaining a motion distribution that aligns with the source video. The quantitative results in Tab. 2 further substantiate that this curated diversity is essential for achieving strong generalization in complex manipulation scenarios. 

## **B Downstream Task Performance Evaluation** 

### **B.1 Simulation Experiments** 

For simulation experiments, we use Embody4D to generate view-randomized training videos, while evaluating policies from a fixed third-person camera. This setting isolates the effect of synthetic view augmentation on cross-view generalization and policy robustness. 

13 


Figure 7: **Ablation on the compositional training data.** Comparison between our full model and a variant trained without compositional data. The yellow boxes show that our strategy is key to mitigating geometric distortions and ensuring generalization across diverse robotic morphologies. 


Figure 8: **Illustration of downstream task evaluation.** Embody4D generates flexible novel views from a single input viewpoint, providing more complete geometric information to augment the training of _π_ 0 _._ 5 [2]. 

For real-world experiments, we introduce an additional Embody4D-generated third-person view during training and inference. By expanding the observational coverage of robot-object interactions, this setting evaluates whether Embody4D can improve spatial reasoning, interaction understanding, and manipulation performance. 

### **B.2 Simulation Experiments** 

We first evaluate Embody4D on the LIBERO benchmark [47] under three training settings: (i) _π_ 0 _._ 5 trained on the original LIBERO dataset; (ii) _π_ 0 _._ 5 fine-tuned with additional random-view samples generated by Embody4D; and (iii) _π_ 0 _._ 5 fine-tuned with real multi-view observations captured at the same target viewpoints, which provides an oracle reference for viewpoint augmentation. For random-view generation, we fix the camera to look at the LIBERO world [48] origin and randomly sample one of six perturbation directions: up, down, left, right, forward, and backward. The left/right rotations are sampled within 20<sup>_◦_</sup> –40<sup>_◦_</sup> , the up/down rotations within 10<sup>_◦_</sup> –20<sup>_◦_</sup> , and the forward/backward translations within 10–20 cm. 

As shown in Table 4, all three training settings achieve strong performance on the original LIBERO benchmark, with only marginal performance gaps. This indicates that the standard LIBERO benchmark is relatively saturated under these settings and may not fully reveal the effect of viewpoint augmentation. We therefore further evaluate the three trained policies on the more challenging LIBERO-Plus benchmark, as reported in Table 5. 

14 

Table 4: **Effect of Embody4D augmentation on LIBERO.** We evaluate _π_ 0 _._ 5 on the LIBERO benchmark and compare training with the original LIBERO data, Embody4D-generated views, and matched real multi-view data. 

|Training Setting|||LIBERO|||
|---|---|---|---|---|---|
||LIBERO-10|LIBERO-Goal|LIBERO-Spatial|LIBERO-Object|Total|
|_π_0_._5[2]|**92.4%**|**98.0%**|98.8%|98.2%|**96.9%**|
|_π_0_._5+ Embody4D|90.6%|95.8%|98.2%|**98.6%**|95.8%|
|_π_0_._5+ Real Multi-view Data|91.2%|96.0%|**99.0%**|98.2%|96.1%|


Table 5: **Effect of Embody4D augmentation on LIBERO-Plus.** We evaluate _π_ 0 _._ 5 under seven LIBERO-Plus perturbation settings and compare training on the original LIBERO data with training using Embody4D-generated random-view samples and matched real multi-view data. 

|Training Setting||||LIBE|RO-Plus||||
|---|---|---|---|---|---|---|---|---|
||Camera|Robot|Language|Light|Background|Noise|Layout|Total|
|_π_0_._5[2]|64.8%|71.8%|83.0%|93.5%|92.2%|78.8%|85.5%|81.4%|
|_π_0_._5+ Embody4D|**86.8%**|50.7%|73.2%|86.3%|82.5%|**86.1%**|76.5%|77.0%|
|_π_0_._5+ Real Multi-view Data|81.3%|55.9%|75.8%|87.4%|78.9%|85.4%|76.9%|77.0%|


The results show that training with Embody4D-generated random-view samples achieves performance close to the real multi-view oracle, demonstrating that Embody4D preserves sufficient visual fidelity and task-relevant spatial information for downstream policy learning. Notably, under the camera perturbation setting, Embody4D improves the success rate from 64 _._ 8% to 86 _._ 8%, yielding a +22 _._ 0% improvement. Under the noise perturbation setting, Embody4D further improves the success rate from 78 _._ 8% to 86 _._ 1%. 

Interestingly, Embody4D slightly outperforms the real multi-view oracle on camera, noise, and background perturbations. We attribute this to the mild background variation and small camera jitter introduced during the novel-view generation process, which act as implicit data augmentation and improve policy robustness beyond the clean real-view setting. For the remaining perturbation types, Embody4D shows a moderate drop compared with the original _π_ 0 _._ 5 baseline. This is expected because our augmentation primarily introduces viewpoint variations, whereas LIBERO-Plus additionally includes non-viewpoint shifts such as language, light, and layout changes. 

Overall, the simulation results demonstrate that Embody4D-generated views provide effective multiview augmentation for downstream policy learning, achieving near-oracle performance and substantially improving policy generalization to viewpoint changes. 

### **B.3 Real World Experiments** 

In our real-world experiments, the input camera pose is illustrated in Fig. 12. The target output pose is defined by a 20<sup>_◦_</sup> rightward rotation and a 30 cm forward translation relative to the input. We selected TrajectoryCrafter [24] and ReCamMaster [25], the two top-performing models as baselines to generate videos from identical target viewpoints for a fair comparison. Our robotic manipulation setup employs a third-person view coupled with a wrist-mounted camera as the primary baseline. To evaluate performance improvements, we integrated novel-view data generated by Embody4D, TrajCrafter, and ReCamMaster into the training pipeline and measured their respective performance gains relative to the baseline. Consistent with the main text, our downstream model is the current state-of-the-art Vision-Language-Action model _π_ 0 _._ 5. In addition, we collect one hundred human demonstration trajectories for post-training. 

The experimental results are summarized in Tab. 3. ReCamMaster, designed for continuous camera motion via direct extrinsic control, struggles with motion instability when simulating the fixed camera poses required by our downstream tasks, leading to a performance decline. TrajCrafter also delivers sub-optimal performance in embodied scenarios, often suffering from visual artifacts and hallucinations, resulting in marginal improvements. As shown in Fig. 12, incorporating a 4D 

15 


Figure 9: **Qualitative results on the LIBERO benchmark.** Our method synthesizes plausible videos from randomly varying viewpoints while preserving visual fidelity and temporal consistency. 


Pick up the black bowl on the ramekin and place it on the plate 𝝅𝟎.𝟓 **+ Embody4D** 


Figure 10: **An example episode from the LIBERO-Plus benchmark.** The policy fails in the original setting but successfully completes the task after the Embody4D is added. 

generation model improves downstream manipulation and planning performance, with particularly significant gains on OOD tasks. Embody4D achieves better generation quality than the other two baseline models. In contrast, ReCamMaster relies on camera extrinsic control, which can easily introduce camera jitter, thereby leading to a decline in performance. Additionally, our method supports scalability by integrating multiple third-person image sequences into the VGGT [31] pipeline, enabling a more comprehensive point cloud reconstruction that can be projected onto flexible target views for completion and novel view synthesis. 

As shown in Fig. 8, Embody4D generates flexible novel-view observations from a single input view, serving both as policy-training augmentation and as auxiliary visual input during inference. While Embody4D is primarily formulated as video-to-video novel-view generation, it also supports imageto-image generation at inference time. Given a single-view image observation and a target relative viewpoint change, Embody4D synthesizes the corresponding novel-view image without requiring additional camera hardware. 

As illustrated in Fig. 11, the upper part shows a failure case where the red cube is occluded in the original observation. Without a viewpoint change, the VLA receives insufficient visual evidence to localize the target object and therefore fails to complete the task. In contrast, the lower part shows that Embody4D synthesizes a complementary novel view without requiring additional camera hardware, exposing the previously occluded region and providing geometric and spatial cues for downstream reasoning. This additional observation enables the VLA to identify the red cube more reliably and generate the correct action. 

16 


Figure 11: **Application of Embody4D during VLA inference.** In addition to video-to-video generation, Embody4D supports image-to-image novel-view generation during VLA inference, providing complementary visual observations that can reveal occluded objects and assist the VLA in generating more reliable actions. 

## **C More Experimental Details** 

### **C.1 Dataset Curation** 

When rendering the robotic arm foreground in the MuJoCo [9] simulation environment, we ensure that the simulated motion closely mimics real world dynamics by strictly constraining the movement magnitude. Specifically, each movement step size is set to one hundredth of the total range of motion for each joint. To maintain spatial consistency, the camera placement within the simulation environment must strictly adhere to the extrinsic parameters of the target backgrounds intended for compositing. This process necessitates a precise coordinate transformation to map the OpenGL coordinate system used in the DL3DV [29] dataset into the XML format required by MuJoCo, which is defined by specific values for distance as well as azimuth and elevation angles. 

Our empirical evaluation demonstrated that employing 49 frame sequences with independent camera and background poses leads to suboptimal performance. The compounding motion of both the foreground robotic arm and the background camera generates highly complex data that hinders the ability of the model to achieve convergence. To mitigate this issue, each data sample consists of two separate videos captured from two distinct and fixed camera poses. To avoid excessive parallax that may cause the composited robotic arm to drift out of the frame, we use GPT-4o [30] to select background sequences with moderate viewpoint variation. Specifically, for each scene in the DL3DV dataset, we randomly choose a starting frame and take the subsequent 40 frames as a temporally coherent background sequence. The selected sequence is required to preserve the same scene identity and dominant content, while exhibiting sufficient but not excessive parallax induced by camera motion. To this end, we design detailed prompts to filter sequences according to both geometric variation and semantic consistency. After foreground-background composition, we further apply an additional GPT-based filtering step to discard implausible or inconsistent composites, as illustrated in Fig. 13. 

As illustrated in Fig. 14, our training pairs are annotated by concatenating the identifier of the robotic arm with a detailed background description to form the final text prompt. This composition based approach yields more precise labels than the direct annotation of the final composited video sequence. For this purpose, we employ the CogVLM2 Llama3 Caption model [34] as our primary labeling tool to ensure high quality descriptive metadata. 

17 


Figure 12: **Visualization results of real-world embodied experiments.** 

### **C.2 Implementation Details of Latent Confidence-Aware Expert Modulation** 

**Latent Residual Routing.** We design a lightweight 3D U-Net to estimate the latent discrepancy between the warped prior and the ground-truth target, which provides the routing signal for expert modulation. As shown in Fig. 15, the warped latent is concatenated with the soft validity mask, resized to the latent resolution, and fed into the residual estimator. The estimator predicts the latentspace correction demand required to transform the warped prior toward the target. A larger predicted discrepancy indicates that the warped prior deviates more from the target latent and therefore requires stronger correction. 

The residual estimator is trained on the full training set for two epochs and then frozen during expert training. As shown in Fig. 15(b), the rightmost error map indicates that the estimator closely fits the target discrepancy. More importantly, the predicted discrepancy map exhibits a clear region-level structure, corresponding to different correction demands in the warped latent. This motivates us to route different latent regions to specialized FFN experts. 

In 4D video generation, the target-view video is not generated freely from noise, but is jointly constrained by the source-view observation and geometric warping. Accordingly, regions in the warped latent have different semantic roles. Some regions remain highly consistent with the source-view observation and should be preserved; some regions are still supported by the source view but require fine-grained correction due to geometric errors, occlusion boundaries, or local misalignment; and other regions are newly exposed in the target view, where the source view cannot provide sufficient content and the model must synthesize plausible details from context. Therefore, the latent space can be naturally decomposed into three semantic regions: _copy_ , _repair_ , and _inpaint_ . 

Based on this observation, we employ three FFN experts to model these three region types. This design matches the intrinsic structure of the task while avoiding unnecessary expert fragmentation. With fewer experts, the same parameters must handle both reliable source-supported regions and 

18 


Figure 13: **Prompt template for evaluating 4D video consistency.** 

newly exposed unseen regions, creating a conflict between preserving source-view consistency and generating novel content. Conversely, using more experts may increase capacity but can make expert boundaries unstable and spatially fragmented, assigning adjacent regions to different experts and harming spatial continuity and temporal consistency. The three-expert design therefore provides a balanced trade-off between semantic specialization and routing stability. 

We then define a confidence-aware latent routing function. Let _V_<sup>¯</sup> denote the smoothed source coverage map derived from the soft validity mask, and let _D_<sup>¯</sup> denote the smoothed predicted residual magnitude. The validity mask mainly reflects whether a region is covered by source-view information, while the predicted residual magnitude further measures how much the warped latent deviates from the target latent. Therefore, regions with high source coverage but large residuals are routed to _repair_ rather than directly copied, whereas regions with low source coverage and large residuals are more likely to require _inpainting_ . 

Specifically, copy regions are required to have both high source-view coverage and low residual magnitude. Inpaint regions correspond to positions with insufficient source-view coverage and high residual magnitude, or to severely misaligned positions with extremely large residuals. All remaining positions are assigned to the repair expert. We use the following routing thresholds: 


Here, _τv_ denotes the minimum source coverage required for copy, _τc_ denotes the residual upper bound for copy, _τi_ denotes the residual threshold for assigning low-coverage regions to inpaint, _τiv_ denotes the low-coverage threshold, and _τf_ denotes the residual threshold for forced inpainting. The final routing rule is 


The thresholds are determined by a two-stage calibration procedure. First, we visualize route maps under different threshold combinations on randomly sampled videos to identify a stable candidate range. This step rejects degenerate settings: overly conservative copy thresholds shrink copy regions and weaken source-view constraints, while overly aggressive inpaint thresholds expand inpaint regions or introduce high-frequency routing fragments, causing the model to prematurely discard warped information. Second, we perform route profiling over the full training set and analyze 

19 


Figure 14: **Visualization results of compositional 4D embodied data** , featuring 4D-consistent sequences with diverse robotic arm foregrounds and varied backgrounds. 

the copy/repair/inpaint distributions across different data sources and disparity conditions. The final thresholds are selected to satisfy three criteria: copy regions should remain non-trivial even under large viewpoint changes, high-coverage regions with large residuals should be primarily routed to repair to reduce generative drift, and low-coverage or severely misaligned regions should be consistently routed to inpaint to preserve the ability to synthesize newly exposed content. 

To reduce fragmentation caused by high-frequency latent residual responses, we apply local smoothing to the residual magnitude and source coverage map with 9 _×_ 9 and 7 _×_ 7 kernels, respectively. We further adopt top-2 expert routing, where the auxiliary expert weight is set to _α_ = 0 _._ 20, followed by a 5 _×_ 5 local smoothing on the route weights. This setting is selected as a trade-off between visual continuity and global route profiling: it removes isolated routing artifacts while preserving coherent inpaint regions. 

### **C.3 Acquisition of Interaction Priors** 

When utilizing the interaction-aware attention mechanism, it is first necessary to obtain a motion prior bias. For data captured in real world scenarios, camera movement often introduces a certain 

20 


Figure 15: **Latent Confidence Estimation Module.** (a) U-Net architecture for estimating latent confidence maps from the warped latent and soft validity mask. (b) Visualization of the estimated confidence maps, where lower-confidence regions indicate higher correction demand for expert modulation. 

degree of jitter, which in turn leads to noise in the optical flow estimation [36]. In cases where the noise level is excessively high, we directly employ the Segment Anything Model 3 [37] to perform segmentation. The input prompt for this process is defined as “robot arm and objects”. As illustrated in Fig. 16, we provide several examples of the resulting optical flow estimations alongside the segmentation masks generated by the Segment Anything Model 3, all masks will be normalized to the range of 0 to 1 for calculations. To prevent the model from over-relying on perfectly foregrounds during training, we introduce a dropout mechanism on the interaction masks. This forces the network to learn robust attention patterns even when the motion prior or mask quality is imperfect, ensuring that the model can handle real-world scenarios with noisy or partially missing foreground information. 

### **C.4 Training Implementation Details** 

We implement our Embody4D using the TrajCrafter diffusion transformer as the generative backbone. All parameters are fully fine-tuned in an end-to-end manner. During training, the frame resolution is fixed at 384 _×_ 672, with a sequence length of 49 frames. 

We adopt a two-stage training strategy. In the first stage, the model is trained on our self-constructed combinatorial real-world 4D dataset to enhance temporal consistency. In the second stage, we freeze 

21 


Figure 16: **Visualization of interaction motion priors.** Showcasing three different foreground acquisition strategies: direct acquisition from compositional data, optical flow estimation, and video object segmentation. 

the interaction-aware blocks and utilize pseudo-4D data, generated by projecting interaction data onto flexible perspectives and back-projecting them to the initial view. This augmentation enables the model to generalize effectively to complex real-world interactions. Finally, all model parameters are fully fine-tuned in an end-to-end manner. 

The training configurations are summarized as follows: 

- **Stage 1:** Conducted for 5.3k iterations with a learning rate of 1 _×_ 10<sup>_−_5</sup> . 

- **Stage 2:** Conducted for 8.1k iterations with a learning rate of 2 _×_ 10<sup>_−_6</sup> . 

Both stages utilize a mini-batch size of 16 (2 per GPU) and are performed on 8 NVIDIA A100 GPUs. Moreover, the latent confidence-aware expert modulation adopts a soft routing scheme and remains frozen during training. Based on the estimated confidence, each token is assigned to two neighboring experts, and their responses are linearly combined with weights 0 _._ 8 and 0 _._ 2 to form the final modulation signal. This avoids abrupt expert switching and encourages smoother transitions across copy, repair, and inpaint behaviors. 

22 


Figure 17: **Visualization of failure cases.** 

## **D Limitations and Future Works** 

Due to the limited temporal modeling capability of current video generation foundation models, our framework can only synthesize fixed-length video sequences. For long input videos, we therefore split them into multiple short clips, perform novel-view synthesis independently for each clip, and then concatenate the generated clips into a complete sequence. However, since different clips are generated independently, temporal discontinuities or visual state inconsistencies may arise at clip boundaries, leading to mild jitter in the final video. Representative failure cases are shown in Fig. 17. Existing long-video generation techniques remain imperfect and still cannot reliably support arbitrary-length or indefinitely long video synthesis. In future work, we will explore more advanced video generation foundation models to improve long-horizon temporal modeling and cross-clip consistency. 

## **E Supplementary Results** 

As shown in Fig. 18, Fig. 19, Fig. 20, and Fig. 21, we provide more experimental results and additional visual comparisons with the baseline method. These results highlight that our method achieves state-of-the-art quality, characterized by fine-grained interaction details, high visual fidelity, and robust spatiotemporal consistency. 

23 


Figure 18: **Visualization results of Embody4D** 

24 


Figure 19: **Visualization results of Embody4D** 


Figure 20: **Qualitative visualization results of our method and the baselines.** 

25 


Figure 21: **Qualitative visualization results of our method and the baselines.** 

26 

