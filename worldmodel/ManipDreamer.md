---
title: "ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance"
date: "2025-04-23"
authors: "Ying Li; Xiaobao Wei; Xiaowei Chi; Yuming Li; Zhongyu Zhao; Hao Wang"
url: https://arxiv.org/abs/2504.16464
pdf: https://arxiv.org/pdf/2504.16464
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2504.16464)** / [論文ページ](https://arxiv.org/abs/2504.16464)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance** 

## Xiaobao Wei 

Xiaowei Chi 

## Ying Li 

State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University 

Hong Kong University of Science and Technology Beijing, China litwellchi@gmail.com 

State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University Beijing, China 

Beijing, China 2301210309@stu.pku.edu.cn 

## Zhongyu Zhao 

## Yuming Li 

## Hao Wang 

State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University Beijing, China 

State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University Beijing, China 

State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University Beijing, China 

## Shanghang Zhang 

Ming Lu 

Ningning Ma Ming Lu Autonomous Driving Development, State Key Laboratory of Multimedia NIO Information Processing, School of Beijing, China Computer Science, Peking University Beijing, China 

State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University Beijing, China 

### **Abstract** 

### **CCS Concepts** 

While recent advancements in robotic manipulation video synthesis have shown promise, significant challenges persist in ensuring effective instruction-following and achieving high visual quality. Recent methods, like RoboDreamer, utilize linguistic decomposition to divide instructions into separate lower-level primitives. They condition the world model on these primitives to achieve compositional instruction-following. However, these separate primitives do not take into account the relationships that exist between them. Furthermore, recent methods neglect valuable visual guidance, including depth and semantic guidance, both crucial for enhancing visual quality. This paper introduces ManipDreamer, an advanced world model based on the action tree and visual guidance. To better learn the relationships between instruction primitives, we represent the instruction as the action tree and assign embeddings to tree nodes. Therefore, each instruction can acquire its embeddings by navigating through the action tree. The instruction embeddings can be used to guide the world model. To enhance visual quality, we combine depth and semantic guidance by introducing a visual guidance adapter compatible with the world model. This visual adapter enhances both the temporal and physical consistency of video generation. Based on the action tree and visual guidance, ManipDreamer significantly boosts the instruction-following ability and visual quality. Comprehensive evaluations on robotic manipulation benchmarks reveal that ManipDreamer achieves large improvements in video quality metrics in both seen and unseen tasks, with PSNR improved from 19.55 to 21.05, SSIM improved from 0.7474 to 0.7982 and reduced Flow Error from 3.506 to 3.201 in unseen tasks, compared to the recent RoboDreamer model. Additionally, our method increases the success rate of robotic manipulation tasks by 2.5% in 6 RLbench tasks on average. 

• **Computing methodologies** → **Vision for robotics** . 

### **Keywords** 

Robotic world model, Video generation, Action tree 

### **1 Introduction** 

Video generation technologies have developed into three main technical paradigms based on control modalities: text-to-video (T2V), image/video-to-video (I2V), and other modalities to video. Early works focus on generating video content that is conditioned by textual input (T2V) [14, 17, 18, 26, 28, 32, 36, 44]. Recent advancements in I2V [39, 46, 54] and V2V [1] techniques are focused on generating high-fidelity videos with complex motions and interactions. These developments illustrate the potential of using video generative models as world models. Other modalities of video generation methods have been proposed, such as motion trajectorycontrolled approaches [49, 58] that enable precise perspective movement, depth-guided synthesis [15, 53] that enhances realism and spatial coherence, and pose-driven [4, 5, 19, 22, 50, 51] methods that generate human animation videos. 

Creating high-quality datasets is essential for data-intensive fields, such as embodied intelligence [6, 8, 47, 63] and autonomous driving [20, 34, 42, 52, 62], where collecting physical data is often prohibitively expensive. Recent developments in generative models have enhanced the creation of world models, providing a costeffective solution for generating synthetic data. In autonomous driving, world models have shown impressive versatility by integrating various control signals to create physically consistent scenarios. Many works [9, 10, 30, 34, 42, 62] utilize control signals such as velocity profiles, steering angles, and traffic rule embeddings to condition the generation process, which is essential for applications like safety validation and rare-scenario augmentation. 

Conference’17, July 2017, Washington, DC, USA 

Li et al. 

Methods [34] based on diffusion transformers leverage MAE-style feature learning to generate multi-view driving videos based on driving actions and text prompts. Large-scale models [42] integrate LiDAR point clouds, BEV semantic maps, and traffic agent trajectories to generate geographically diverse multi-camera streams, facilitating closed-loop simulations for planning algorithms. 4D scene reconstruction [62] utilizes world model priors to synthesize novel trajectory videos, showcasing the synchronized spatial-temporal evolution of dynamic objects and static environments. 

In contrast, robotic video generation focuses on task-oriented synthesis guided by specific inductive biases. Typically, a robotic world model takes a scene snapshot and generates robotic videos conditioned on language instructions. Unlike approaches in autonomous driving, most existing methods rely solely on the RGB modality, which provides limited multi-modal information. Robodreamer [63] breaks down language instructions into lower-level primitives for the synthesis of compositional manipulation. Wang et al. [47] combine gesture-based spatial references with deictic language to clarify ambiguities in open-world environments. For action-conditioned generation, FLIP [8] introduces flow-centric planning, where optical flow fields act as intermediate representations of actions to guide video generation. Recent efforts, such as EVA [6], have introduced an Understand–Imagine–Predict world model loop. However, it still relies solely on RGB images as the input perception modality, limiting its ability to capture richer spatial and semantic context. By overcoming these limitations, world models can achieve a more accurate understanding of spatial affordances and physical constraints, ultimately enhancing their performance in sim-to-real transfer and complex manipulation tasks. 

While recent advancements in robotic world modeling show promise, significant challenges remain in ensuring effective instruction following and achieving high visual quality. This paper proposes ManipDreamer, an advanced robotic manipulation world model based on the action tree and multi-modal visual guidance. For instruction following, instead of breaking down language instructions into lower-level primitives, we represent each instruction as an action tree. We assign embeddings to the nodes of the action tree, allowing each instruction to derive its own embeddings through a traversal of the tree. These instruction embeddings are then utilized to guide the world model. 

Regarding visual quality, we observe that generated robotic videos exhibit significant artifacts. These issues include structural anomalies in the robotic arms, geometric deformations of objects, and temporal inconsistencies such as cross-frame attribute mutations. As a result, the fidelity of the synthetic content is compromised, affecting both spatial continuity and temporal coherence. We introduce a visual adapter to leverage the depth and semantic information in the video generation process to enhance the visual quality. The adapter features a multi-scale encoder that progressively incorporates depth-aware geometric constraints into the video diffusion pipeline. 

Our experiments demonstrate that ManipDreamer significantly improves the performance of robotic manipulation world models. Specifically, it achieves notable enhancements in video quality metrics such as PSNR, SSIM, and Flow Error, surpassing the recent RoboDreamer model. Additionally, our method shows consistent improvements in the success rate of robotic manipulation tasks 

across multiple RLbench[21] benchmarks. Our main contributions include: 

- We propose an advanced world model ManipDreamer for robotic manipulation that ensures effective instruction-following and achieves high visual quality. 

- We propose representing the instruction as an action tree to learn the relationships between instruction primitives. 

- We enhance visual quality with a well-designed adapter that integrates depth and semantics into robotic world models through hierarchical guidance. 

- We conduct a comprehensive experiment to evaluate the effectiveness of ManipDreamer, achieving significant improvements in both video quality and task compliance across six benchmark datasets. 

### **2 Related Works** 

### **2.1 Robotic Video Generation** 

Robotic video generation differs fundamentally from general video synthesis tasks in that it demands task-driven reasoning, physical interaction modeling, and scene-level spatial understanding. ManiGaussian [29] employs dynamic Gaussian splatting on depthderived point clouds for policy video generation but encounters rendering artifacts due to the Gaussian representation. RoboAgent [2] leverages SAM-2 [41] masks for data augmentation, rather than using semantic features as direct generative guidance. Recent advances in diffusion models have led to promising progress in the world model for robotics. AVDC [23] pioneers action-conditioned video generation via latent diffusion without requiring explicit action labels, demonstrating the potential of synthetic data for downstream policy learning. RoboDreamer [63] improves instruction generalization by decomposing language commands into reusable sub-task components. This&That [47] addresses language ambiguity by grounding instructions in both textual and gestural modalities. FLIP [8] proposes a flow-centric world model for manipulation planning, unifying flow prediction, flow-conditioned video generation, and vision-language value estimation. 

Despite these advancements, most existing methods rely solely on RGB frames and textual prompts, without explicitly modeling scene geometry or object-level semantics. This limits their ability to preserve spatial consistency and to capture fine-grained manipulation constraints, both of which are critical for generating realistic and executable robot videos in complex environments. Furthermore, these approaches predominantly focus on a single modality of scene representation, restricting their capacity to fully comprehend and reproduce the rich, multi-faceted nature of robotic interactions in real-world settings. 

### **2.2 Multi-modal Conditioned Generation** 

ControlNet [59] revolutionized conditional image generation by enabling spatial constraints while preserving the capabilities of the original model. Subsequent works have extended this idea to the video domain. For example, SparseCtrl [13] introduces sparse frame guidance to enhance temporal consistency, and Ctrl-Adapter [27] adapts pretrained ControlNets to various video generation backbones (e.g., I2VGen-XL [61]) through parameter-efficient fine-tuning. These methods demonstrate strong performance in incorporating diverse modalities to guide video generation. However, they typically 

Conference’17, July 2017, Washington, DC, USA 

ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance 


**Figure 1: Overview of ManipDreamer: a world model for robotic manipulation that integrates structured instruction representations (a) and multi-modal visual guidance (b). We encode language instructions as verb-preposition action trees to capture compositional task structure and inject depth and semantic features through a hierarchical adapter to enhance spatial-temporal consistency in video generation. In the UNet decoder, action tree embeddings and visual guidance features are sequentially injected every 3 layers using cross-attention mechanisms.(c)** 

rely on sparse but explicit multi-frame conditions, and are therefore ill-suited for scenarios like robotic video generation, where only the initial frame and a textual prompt are available at inference time. These approaches primarily focus on frame-to-frame conditioning patterns, where conditioned frames directly control corresponding output frames. This proves challenging in robotic world model scenarios that require long-horizon reasoning from a single initial observation, necessitating alternative conditioning mechanisms for effective trajectory synthesis. 

Contrary to the aforementioned methods focused on natural image generation, recent autonomous driving (AD) approaches have begun to exploit scene structure through geometric representations. SyntheOCC [25] combines multi-plane images with semantic occupancy maps to construct realistic driving environments, while UniScene [24] synthesizes multi-view videos using BEV-derived LiDAR and occupancy features. InfiniCube [31] introduces a scalable world-guided framework for generating unbounded dynamic 3D driving scenes. DriveDreamer4D [62] and ReconDreamer [33] introduce a 4D driving scene generation framework that leverages world model priors to synthesize videos. The introduction of these novel modalities has significantly enhanced scene understanding and motion prediction capabilities, demonstrating that incorporating geometric and semantic representations can substantially improve the quality and consistency of generated videos. This inspires our approach to leverage complementary modalities for more effective robotic scene understanding and manipulation planning. 

However, these methods primarily target high-fidelity video generation in structured scenarios with simple road trajectories. In contrast, robotic video generation typically involves decision-making and interaction within complex, unstructured environments, where spatial understanding and semantic awareness are essential. To address this challenge, we propose a novel framework that synergistically integrates multi-modal cues into robotic world models via hierarchical guidance. 

### **2.3 Action Tree in Robotics** 

Behavior Trees (BTs) have been widely adopted in traditional robotic manipulation as a modular and interpretable framework for task execution [11]. They offer a hierarchical and extensible structure for decomposing complex tasks into atomic behaviors (e.g., _grasp_ , _move_ ) and control operators (e.g., _sequence_ , _fallback_ ). This structured representation supports reusability, debugging, and runtime adaptability, making BTs well-suited for modeling reactive behaviors in dynamic environments [11]. Recent studies further show that BTs align with the models-at-runtime paradigm, enabling seamless coordination of low-level robot skills through high-level task specifications. FOON [38] proposes a structured bipartite graph representation, enabling robots to retrieve task trees and generate manipulation trajectories. Michele et al. [7] provide a practical analysis of Behavior Tree implementations in robotics, detailing execution engines, memory nodes, node parameterization, and asynchronous action handling for real-world robot control systems. 

Conference’17, July 2017, Washington, DC, USA 

Li et al. 

Approximate Task Tree Retrieval [43] proposes a method for generating executable task trees from a knowledge graph. Corrado et al. [40] proposes a hybrid framework combining active inference with behavior trees, enabling reactive robotic planning and execution. Long-Horizon FOON [37] proposes a hierarchical task planning framework that transforms symbolic FOON representations into executable robot plans. Yang et al. [56] represent manipulation actions as treebanks encoding physical constraints and task dependencies for action retrieval and adaptation. Another work [57] further bridges language and BTs by using language models (LMs) to generate XML-formatted trees from natural instructions. 

Unlike prior works that leverage action trees primarily for lowlevel control or symbolic planning, our approach is the first to integrate action tree semantics into generative models for robotic video synthesis. By embedding structured task representations into a diffusion-based video generation pipeline, we enforce spatiotemporal consistency between complex language instructions (e.g., “pick up the cup and pour water”) and the resulting motions. This demonstrates that action trees serve as a crucial symbolic prior to constrain the open-ended space of generative robotics. 

### **3 Method** 

In this section, we first review the preliminaries of robotic video generation using world models in Sec. 3.1. We then introduce our proposed world model, ManipDreamer, which aims to achieve accurate instruction-following and high-fidelity visual synthesis. To capture the relationships among instruction primitives, we present the Verb-Preposition Action Tree in Sec. 3.2. Finally, to improve the visual quality of generated robotic videos, we integrate Multi-modal Visual Guidance into the world model, as detailed in Sec. 3.3. 

### **3.1 Problem Formulation** 

A typical robotic world model includes a video generation module, enabling interaction through video outputs to convey reasoning results and enhance interpretability. Given an initial scene observation _𝐼_ ∈ R<sup>3×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> and text instruction _𝑐_ text, a robotic video generator aims to produce a physically plausible trajectory _𝑉_ ∈ R<sup>_𝐹_×3×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> depicting _𝐹_ subsequent frames of environment evolution under specified manipulation. Traditional approaches employ diffusion models F _𝜃_ ( _𝑧𝑡 ,𝑡,𝑐_ text) that gradually denoise latent representations _𝑧𝑡_ through iterative prediction of noise components _𝜖𝜃_ ( _𝑧𝑡 ,𝑡,𝑐_ text) conditioned on time _𝑡_ and _𝑐_ text minimizing the loss: 


Our extended formulation incorporates geometric depth _𝐷_ 0 ∈ R<sup>1×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , semantic segmentation _𝑆_ 0 ∈ R<sup>_𝐶_sam×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , and dynamic mask _𝑀_ 0 ∈ R<sup>1×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , all tied to the first frame _𝐼_ 0. These inputs help the enhanced model F _𝜃_ ( _𝑧𝑡 ,𝑡,𝑐_ text _,𝑆_ 0 _, 𝐷_ 0) achieve stronger spatial understanding and execute more accurate manipulations, while preserving object identity and allowing flexible state changes. 

### **3.2 Verb-Preposition Action Tree** 

_3.2.1 Action Tree Construction._ RoboDreamer [63] decomposes language instructions into sub-actions to improve generalization. However, its decomposition-and-composition strategy suffers from several limitations: 


**Figure 2: Different from the instruction decomposition manner in RoboDreamer, we propose a novel action tree method to represent the action to be generated consuming less computation resource.** 

- The decomposition ignores the temporal dependencies between sub-actions by using the average of predicted noises; 

- Executing the model separately for each sub-action incurs significant GPU memory and computational cost, especially for long instructions; 

- The denoising trajectories of individual sub-actions may be inconsistent with the overall video generation process. 

We propose a tree-based structure as an alternative mechanism to control the action generation process. The key difference between our method and RoboDreamer is illustrated in Fig. 2. To reduce the solution space, we represent each instruction as a hierarchical action tree composed of reusable embeddings of key action words—namely, verbs (e.g., pick, place) and prepositions (e.g., on, in). For each language instruction in the dataset, we extract its constituent action words and assign them to the appropriate layers in the tree. The action words are in order from the root of the tree down to the leaves. Finally we get a action tree tree with alternating layers of verbs and prepositionsas shown in Fig. 1. Each key action word is then embedded using the CLIP text encoder, which is also used in the original text-conditioning pathway. This tree structure aligns well with the compositional and hierarchical structure of complex actions in possible language instructions. 

_3.2.2 Action Tree Parsing._ To generate action condition for a video generation model, we obtain the text embeddings on the path nodes after traveling down the action tree. For example, we get the text embedding of words "pick", "from", "place", and "in" after traveling the instruction "pick the apple from the table and place it in the top drawer" down the constructed action tree. These embeddings are afterwards concatenated together to form the final action tree embedding. We fix the number of embeddings to the maximum number of action words in all possible text instructions, and zero embeddings are used for padding if the number of key words are less than that when encountering short instructions. Giving an 

Conference’17, July 2017, Washington, DC, USA 

ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance 

instruction _𝑐_ text, the final action tree embedding is defined as: 


in which _𝑉𝑒𝑟𝑏𝑖_ and _𝑃𝑟𝑒𝑝𝑖_ are the two adjacent verb and preposition action words. 

By encoding the full sequence of verbs and prepositions in a unified embedding, our method addresses the aforementioned key limitations of prior decomposition-based approaches. Our model captures the temporal dependencies between sub-actions as we view the actions as a whole and extract the most important part of it. The one forward property of the key action embedding avoids extra computational overhead. Moreover, generating actions with coherent tree embeddings ensures that the denoising trajectory remains globally consistent throughout the video generation process. 

### **3.3 Multi-modal Visual Guidance** 

_3.3.1 Multi Scene Modality Acquisition._ Due to the lack and low quality of depth and semantic annotations in third-view robotic datasets, we leverage pretrained foundation models to estimate these modalities without the need for costly manual labeling. Specifically, the Depth Anything v2 model [55] provides view-consistent and accurate depth estimation using a transformer-based monocular predictor. For semantic guidance, we adopt SAM-2 [41], which produces semantic embeddings that support instance-aware and multi-granularity object segmentation. To better preserve the original model’s representation capacity and avoid object-class misalignment, we use normalized depth maps as depth conditions and semantic embeddings—instead of discrete segmentation maps—as semantic conditions. To obtain the dynamic mask, we compute the similarity between SAM features from the first frame and subsequent frames, identifying regions with significant changes as potential dynamic parts. We also experiment with DINO [35] features and observe comparable results. Details of the dynamic mask algorithm are provided in the supplementary material. In addition to depth, semantics, and dynamic mask, we also incorporate the RGB image as a complementary modality. As a result, our model is conditioned on four visual modalities: depth, semantic embedding, RGB, and dynamic mask. 

_3.3.2 Hierarchical Feature Extraction with ControlNets._ As illustrated in Fig. 1, each visual modality is processed through a dedicated ControlNet branch that extracts pyramid features. Commonly, ControlNet initializes its input/output convolution layers with zeros to avoid perturbing the pretrained UNet features, while inheriting encoder weights from the base UNet backbone. However, we find that the original ControlNet design is suboptimal for multi-modal guidance in our setting, for the following reasons: First, each ControlNet receives a single-frame input, and replicating this frame across all _𝑇_ time steps leads to significant GPU memory overhead and increased inference latency. Second, when repeatedly feeding the same frame to a 3D ControlNet, we observe that its outputs remain nearly identical across time, suggesting limited temporal contribution. To address these issues, we propose a 2D ControlNet structure, which inherits the temporal-agnostic parameters from the base UNet and replaces 3D convolutions with 2D convolutions. 

This modification preserves spatial guidance while greatly improving computational efficiency for frame-wise visual conditions. 

Formally, given frame-replicated control signals _𝐷_ ∈ R<sup>_𝐶_depth×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , _𝑆_ ∈ R<sup>_𝐶_sam×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , _𝑅_ ∈ R<sup>_𝐶_rgb×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , and _𝑀_ ∈ R<sup>_𝐶_mask×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> , where _𝐶_ depth, _𝐶_ sam, _𝐶_ rgb, and _𝐶_ mask are the channel numbers of depth, semantic, RGB, and dynamic mask features respectively, we compute pyramidal features P _𝑑_ , P _𝑠_ , P _𝑟_ , and P _𝑚_ through the ControlNet branches. The above process can be formulated as: 


To fuse each layer of features from different modalities, we use a patch-lever q-former router [27] Φ that takes the concatenated features from different modalities of this layer as input, and outputs the score _𝜑_ for each modality in a patch-lever manner: 


Then the features are multiplied by the scores and added together to get the fused feature of this layer: 


_3.3.3 Spatial Feature Adapters._ To form the final control signal for UNet, we first repeat the spatial fused features Pfused along the temporal dimension to get Pfused<sup>′∈R</sup><sup>_𝑇_×</sup><sup>_𝐶_fused×</sup><sup>_𝐻_×</sup><sup>_𝑊_, Then we use a</sup> spatial-temporal feature adapter to adapt the fused features before feeding them into the base UNet. Our fusion module employs sequential spatial and temporal convolutions followed by spatial and temporal cross-attention layers inspired by [27]. In the temporal attention layer, the frames are added with temporal positional embeddings to introduce extra temporal difference, so that the model can learn more temporal-aware features. The four submodules in the feature adapter are: 


To effectively integrate the final guidance features G with the corresponding UNet decoder blocks at each layer, we compare two fusion strategies: **Additive Fusion.** At each layer, the guidance features from G are directly added to the residual features from Funet of the corresponding UNet encoder. **Cross-Attention Fusion.** At each decoder block, we apply cross-attention where the query is the decoder output, and the key and value are from the guidance features G. The impact of these two fusion strategies is evaluated in the ablation study presented in the experimental section. By introducing pyramid features, our model enables multi-level geometric and semantic conditioning throughout the denoising process. It’s worth noting that, in contrast to Ctrl-Adapter [27], which requires sparse, per-frame control signals, our framework relies only on single-frame inputs, making it more efficient and better suited for robotic video generation scenarios. 

Conference’17, July 2017, Washington, DC, USA 

Li et al. 

**Table 1: Comparison of Action Tree vs. Linguistic Decomposition in RoboDreamer [63] on Video Quality Metrics. The better results are in bold.** 

|**Method**|**FID**↓|**SSIM**↑|**Seen T**<br>**PSNR**↑|**asks**<br>**LPIPS**↓|**Flow Error**↓|**FID**↓|**SSIM**↑|**Unseen**<br>**PSNR**↑|**Tasks**<br>**LPIPS**↓|**Flow Error**↓|
|---|---|---|---|---|---|---|---|---|---|---|
|RoboDreamer (w/ linguistic decomposition)|7.014|0.7235|19.47|0.07484|4.064|**7.336**|0.7390|19.33|0.07634|3.885|
|RoboDreamer (w/ action tree)|**6.252**|**0.7358**|**19.79**|**0.07120**|**3.723**|7.433|**0.7461**|**19.50**|**0.07413**|**3.652**|


**Table 2: Comparison of different guidance methods on video quality metrics towards RoboDreamer. The best results of all are in bold and the best result of ControlNet variant are underlined. Semantic stands for SAM feature and Mask stands for dynamic mask.** 

|**Method**|**Action Tree**||**Visual In**<br>|**put**<br>||||**Seen T**<br>|**asks**<br>||||**Unseen**<br>|**Tasks**<br>||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||**Depth**|**Semantic**|**RGB**|**Mask**|**FID**↓|**SSIM**↑|**PSNR**↑|**LPIPS**↓|**Flow Error**↓|**FID**↓|**SSIM**↑|**PSNR**↑|**LPIPS**↓|**Flow Error**↓|
|Vanilla|�|�|�|�|�|**6.0721**|0.7300|19.66|0.07470|3.8004|**7.396**|0.7474|19.5474|0.07478|3.506|
||�|�|�|�|�|6.378|0.7355|19.75|0.07338|3.611|8.537|0.7543|19.69|0.07276|3.318|
|ControlNets|�<br>|�<br>|�<br>|�<br>|�<br>|6.563|0.7375|19.80|0.07265|3.555|8.696|0.7568|19.75|0.07259|3.265|
||�|�|�|�|�|6.600|0.7374|19.81|0.07267|3.545|8.668|0.7564|19.75|0.07267|3.257|
||�|�|�|�|�|6.456|0.7369|19.79|0.07288|3.566|11.177|0.7528|19.67|0.07490|3.348|
||�|�|�|�|�|6.252|0.7358|19.79|0.07120|3.723|7.433|0.7461|19.50|0.07413|3.652|
|ManipDreamer|�|�|�|�|�|8.182|0.7853|21.06|0.05702|**3.049**|9.480|**0.7982**|**21.05**|**0.05768**|**3.021**|
||�|�|�|�|�|7.209|**0.7867**|**21.13**|**0.05460**|3.145|8.483|0.7949|20.98|0.05782|3.178|


### **4 Experiments** 

We structure our experimental analysis as follows: Section 4.1 details the dataset configuration and evaluation protocols. Section 4.2 presents comprehensive comparisons with our baseline methods, while Section 4.3 systematically examines several interesting questions. 

### **4.1 Experimental Setup** 

_4.1.1 Video evaluation._ In this part, we provide the dataset preparation and training details for video quality evaluation experiment. **Dataset Configuration.** We utilize the RT-1 dataset [3], comprising 80K video demonstrations spanning over 590 distinct manipulation tasks categorized as Picking, Placing, Knocking and Opening/Closing. The structured composition of action-object pairs enables seamless integration with our action tree framework, eliminating the need for additional linguistic processing. To evaluate generalization capabilities, we adopt a task-based split allocating over 90% of episodes (denoted as seen tasks) for training while reserving novel task combinations (unseen tasks) for testing. 

**Training Protocol.** Our implementation follows RoboDreamer’s [63] two-stage paradigm: initial training of a base video generation model at 64×64 resolution, followed by cascaded super-resolution (SR) diffusion for 256×256 output. This design strategically separates policy learning from visual refinement based on three considerations: 

- **Decoupled Policy & SR** : Empirical analysis reveals that action semantics predominantly emerge in low-resolution generation, enabling policy-agnostic SR processing 

- **Training Efficiency** : High-resolution training demands much more computation per iteration and will be much slower considering our training budget 

- **Metric Reliability** : The cascaded super-resolution module could affect video quality, causing uncertainty in the results of video quality related metrics 

Nevertheless, we also train super-resolution networks to up-sample the video to 256 × 256 resolution. Detailed generation samples are shown in the appendix. 

**Metrics.** We mainly evaluate our method on two categories of metrics: image / video quality and task completion success rate. We use FID score [16], SSIM score [48], PSNR score, LPIPS score [60] and flow error score [45] to evaluate image / video quality. When evaluating the image/video quality, we randomly selected 20 seen tasks and 20 unseen tasks, each task is evaluated for 50 initial states. So there will be 1000 generated videos in total for both seen and unseen setting. 

_4.1.2 Robot Planning._ **Planning tasks.** We select the six tasks of rlbench reported in RoboDreamer: Close box, Lamp Off, Lamp On, Stack Blocks, Lift Block and Take Shoes. Both short term tasks like closing the box, turn on the lamp and long term tasks like stack blocks and take shoes out of box. 

**Trainging details.** Following former works [12, 63], We first pick out the macro steps according to velocity and gripper status change. The macro step dataset contains mainly the key decision frames, making sure the model concentrates on the policy. We finetune the two generative model on the RT-1 pretrained version to utilize the prior knowledge and fostering the training process. 

### **4.2 Main Results** 

_4.2.1 Action Tree Effectiveness._ To show the effectiveness of our proposed action tree method. We applied the action tree method on RoboDreamer, and removed the linguistic decomposition mechanism in it to compare these two action generalize methods. Tab. 1 demonstrates our action tree’s superiority over linguistic decomposition, achieving consistent improvements across 9/10 metrics. Notably, it reduces LPIPS by 4.9% (0.071 vs 0.075) on seen tasks while maintaining comparable unseen task performance, validating its enhanced generalization through structured action representation, even though fewer forward steps are performed. 

Conference’17, July 2017, Washington, DC, USA 

ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance 


**Figure 3: ManipDreamer alleviates multiple common defects in robotic video generation, including instruction misalignment, hallucinations, spatial errors, duplicate objects, temporal discontinuities, and failed executions. This figure presents sample comparisons between RoboDreamer and ManipDreamer, illustrating the effectiveness of our proposed approach.** 

**Table 3: Success rate comparison on 6 RLBench tasks. Better results are in bold.** 

|**Model**|**Close Box**|**Lamp Off**|**Lamp On**|**Stack Blocks**|**Lift Block**|**Take Shoes**|**Average**|
|---|---|---|---|---|---|---|---|
|RoboDreamer|0.95|**0.92**|0.49|0.12|0.31|0.09|0.480|
|ManipDreamer|**0.96**|0.91|**0.51**|**0.18**|**0.33**|**0.14**|**0.503**|


_4.2.2 Visual Guidance Analysis._ To illustrate our proposed method is more powerful than simply applying ControlNet in robotic video generation, we train four RoboDreamer ControlNet variants with different condition modalities: depth, semantic, RGB and dynamic mask as baselines and compare the video quality metric with our visual guiding method, the result are listed in Tab. 2. 

**Sigal-modal ControlNets.** As evidenced in Tab. 2, ControlNet variants demonstrate limited improvements over baseline RoboDreamer. For seen tasks, SAM-based conditioning achieves marginal gains of 0.75 percentage points in SSIM (0.7375 vs 0.7300) and 0.15 dB in PSNR (19.81 vs 19.66). Similar patterns emerge in LPIPS (2.05% relative reduction) and flow error (6.7% decrease from 3.800 to 3.545). Parallel trends hold for unseen tasks. This narrow performance improvement suggests single-modality conditioning inadequately addresses the complex spatial-temporal constraints in robotic video generation. 

**Multi-modal Control Adapter.** In contrast, our multi-modal control adapter (MCA) significantly outperforms single-modality ControlNet variants. On seen tasks, MCA achieves 21.06 PSNR (+1.32dB) 

with 0.0546 LPIPS (24.8% reduction) over best ControlNet, confirming that synergistic multi-modal fusion captures richer spatialtemporal constraints than individual conditioning. On the unseen tasks, our MCA also get the best performance over all metrics except from FID, we conclude that our novel visual conditioning method largely improved the visual quality of generated robotic videos. **Visualization Analysis.** Qualitative results from our inference experiments provide compelling evidence for the system’s improvements. As illustrated in Fig. 3, we systematically categorize six distinct failure modes prevalent in current world model’s capability, each alleviated by our method: **Instruction Misalignment.** This critical failure occurs when generated actions contradict textual specifications. In Fig. 3(a), RoboDreamer erroneously positions the rxbar chocolate near an apple instead of the instructed brown chip bag, whereas our method demonstrates precise instruction grounding through action tree parsing. **Object Duplication.** Manifested as persistent object presence post-manipulation, this artifact violates object permanence principles. Fig. 3(b) shows RoboDreamer’s output where the brown chip bag remains on the counter despite being 

Conference’17, July 2017, Washington, DC, USA 

Li et al. 

**Table 4: Visual Quality Metrics of Ablation study experiments. The best results are in bold in research question 1 and research question 3. The results with most decline from original Additive ManipDreamer are in italics in research question 2.Semantic stands for SAM feature and Mask stands for dynamic mask.** 

||**Method**|**FID**↓|**SSIM**↑|**Seen T**<br>**PSNR**↑|**asks**<br>**LPIPS**↓|**Flow Error**↓|**FID**↓|**SSIM**↑|**Unseen**<br>**PSNR**↑|**Tasks**<br>**LPIPS**↓|**Flow Error**↓|
|---|---|---|---|---|---|---|---|---|---|---|---|
|**R1**|ManipDreamer (v, Additive Fusion)|8.181|0.7853|21.06|0.05702|**3.049**|9.480|0.7982|21.05|0.05768|**3.021**|
|**Q**|ManipDreamer (v, Cross Attention Fusion)|**7.226**|**0.7922**|**21.27**|**0.05302**|3.166|**8.284**|**0.8024**|**21.20**|**0.05468**|3.1650|
|**R2**|ManipDreamer (v, lower)|**8.281**|0.7711|20.50|0.06197|3.309|**9.113**|0.7797|20.61|0.05979|3.659|
|**Q**|ManipDreamer (v, upper)|8.501|**0.7899**|**20.97**|**0.05593**|**3.097**|9.372|**0.7959**|**21.06**|**0.05383**|**3.387**|


supposedly placed in the drawer. Our spatial-aware generation eliminates such phantom objects in this case. **Physical Hallucinations.** Characterized by non-physical object interactions, these errors include teleportation and morphing artifacts. The baseline output in Fig. 3(c) demonstrates matter discontinuity where the target object instantaneously appears in the gripper, while our multi-modal constraints enforce coherent material transitions. **Temporal-Spatial Discontinuity.** We distinguish two subtypes: (1) Temporal discontinuity featuring implausible motion trajectories and (2) Spatial discontinuity with fractured object geometries, exemplified in Fig. 3(d) where the robotic arm’s shadow exhibits abrupt fragmentation during movement; **Spatial Misunderstanding.** Distinct from discontinuity errors, this category involves fundamental 3D relationship misinterpretations. Fig. 3(e) exposes one RoboDreamer’s failure to update spatial states - the rxbar chocolate appears both grasped and on the counter. Our depth-conditioned generation resolves this paradoxes. **Execution Failure.** Error mode includes premature termination and non-functional movements. As shown in Fig. 3(f), the baseline model aborts the action mid-execution, while our policy-aligned generation maintains complete action sequences. 

_4.2.3 Planning Ability._ Table 3 demonstrates ManipDreamer’s competitive task completion rates, outperforming RoboDreamer on 5 of 6 RLBench tasks. Key improvements include Stack Blocks (+33.3% relative) and Take Shoes (+55.6% relative), highlighting our method’s advantage in complex, multi-step tasks. The 5.2% average gain stems from better action decomposition and spatial-temporal modeling through our novel multi-modal conditioning framework and action tree method. 

### **4.3 Ablation Study** 

We conduct systematic ablation experiments to investigate three core research questions regarding our framework’s design choices: **RQ1: Fusion Strategy.** What is the better way to incorporate fused features into the generative model? **RQ2: Layer Injection.** What is the difference in impact caused by guidance at different decode layers? 

For the first question, we compare the results of the additive fusion and cross attention fusion methods, in addictive fusion setting, conditions are added onto the hidden states when sequentially pass the 12 decoders, along with the residuals from corresponding encoder layer. Whilst in cross attention fusion methods, the hidden states are view as query and conditioning features are view as key and value when doing a cross attention. We found this process 

memory-consuming thus only one cross attention layer is used. We inject the conditioning features every 3 layers. As shown in Tab. 4(RQ1), the cross attention fusion method results in better performance than additive fusion, achieving a margin of 0.87% on SSIM by and 0.21 dB on PSNR in seen tasks. This performance advantage is consistently maintained for unseen tasks. The enhanced performance stems from the cross-attention mechanism’s ability to effectively model complex spatiotemporal relationships between video dynamics and conditional features. 

For the second question, we split the decoder layers of Denoising UNet into two groups: the upper 6 layers is close to middle block of UNet, where hidden states has smaller spatial size and larger hidden size and the lower 6 layers in the opposite, note we inject conditions every 3 layers, therefore there are two conditioned layers in each setting. We trained two variant of multi-modal control adapter applied on RoboDreamer, one only injecting the corresponding conditioning features into upper 6 layers, and the other at lower 6 layers in an additive fusion manner. As shown in Tab 4(RQ2), upper-layer guidance yields better motion consistency (flow error 3.097 vs 3.309), while lower-layer conditioning enhances visual details (FID 8.28 vs 8.50). This aligns with the hierarchical nature of diffusion models - global structure forms early, local details refine later. 

Despite its higher memory footprint, cross-attention achieves superior metrics (Tab. 4(RQ2)), getting a margin of SSIM by 0.7% and PSNR by 0.21dB over additive fusion. This validates its enhanced capacity for modeling complex spatial-dynamic relationships. 

### **5 Conclusion** 

In this work, we propose ManipDreamer, a novel world model for robotic manipulation video synthesis that integrates structured instruction representation and multi-modal visual guidance. To enhance instruction-following ability, we introduce an action tree representation that explicitly captures the structural relationships among instruction primitives. Each instruction is encoded by traversing the tree, and the resulting embeddings are used to condition the dynamics generation in the world model. To improve visual quality, we further design a visual guidance adapter that fuses depth, semantic information, RGB and dynamic masks, effectively enhancing temporal and physical consistency during video generation, resulting in higher quality metrics. Extensive experiments on RLBench benchmarks demonstrate that ManipDreamer significantly outperforms prior methods, achieving substantial gains in video manipulation task success rates. We believe our approach provides a promising direction for advancing robotic video generation and 

Conference’17, July 2017, Washington, DC, USA 

ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance 

opens up new possibilities for integrating structured reasoning and multi-modal guidance in the robotic world model. 

- opens up new possibilities for integrating structured reasoning and [21] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. 2020. multi-modal guidance in the robotic world model. Rlbench: The robot learning benchmark & learning environment.and <u>Automation Letters 5, 2 (2020), 3019–3026. IEEE Robotics</u> [22] Johanna Karras, Aleksander Holynski, Ting-Chun Wang, and Ira KemelmacherShlizerman. 2023. Dreampose: Fashion video synthesis with stable diffusion. 

- **References** In22680–22690.Proceedings <u>of the IEEE/CVF International Conference on Computer Vision.</u> [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, [23] Po-Chen Ko, Jiayuan Mao, Yilun Du, Shao-Hua Sun, and Joshua B Tenenbaum. Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. 2025. Cosmos 2023. Learning to act from actionless videos through dense correspondences. world foundation model platform for physical ai. <u>arXiv preprint arXiv:2501.03575 arXiv preprint arXiv:2310.08576 (2023).</u> (2025). [24] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, 

- [2] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham TulHu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. 2024. UniScene: Unified siani, and Vikash Kumar. 2024. Roboagent: Generalization and efficiency in robot Occupancy-centric Driving Scene Generation. <u>arXiv preprint arXiv:2412.05435</u> manipulation via semantic augmentations and action chunking. In <u>2024 IEEE</u> (2024). <u>International Conference on Robotics and Automation (ICRA). IEEE, 4788–4795.</u> [25] Leheng Li, Weichao Qiu, Yingjie Cai, Xu Yan, Qing Lian, Bingbing Liu, and Ying- 

- [3] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Cong Chen. 2024. SyntheOcc: Synthesize Geometric-Controlled Street View Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Images through 3D Semantic MPIs. <u>arXiv preprint arXiv:2410.00337 (2024).</u> Hsu, et al. 2022. Rt-1: Robotics transformer for real-world control at scale. <u>arXiv</u> [26] Yitong Li, Martin Min, Dinghan Shen, David Carlson, and Lawrence Carin. 2018. <u>preprint arXiv:2212.06817 (2022).</u> Video generation from text. In <u>Proceedings of the AAAI conference on artificial</u> 

- [4] Peng Chen, Xiaobao Wei, Ming Lu, Hui Chen, and Feng Tian. 2025. Dif- <u>intelligence, Vol. 32.</u> fusionTalker: Efficient and Compact Speech-Driven 3D Talking Head via [27] Han Lin, Jaemin Cho, Abhay Zala, and Mohit Bansal. 2024. Ctrl-adapter: An Personalizer-Guided Distillation. <u>arXiv preprint arXiv:2503.18159 (2025).</u> efficient and versatile framework for adapting diverse controls to any diffusion 

- [5] Peng Chen, Xiaobao Wei, Qingpo Wuwu, Xinyi Wang, Xingyu Xiao, and Ming model. <u>arXiv preprint arXiv:2404.09967 (2024).</u> Lu. 2024. MixedGaussianAvatar: Realistically and Geometrically Accurate Head [28] Yue Liu, Xin Wang, Yitian Yuan, and Wenwu Zhu. 2019. Cross-modal dual learning Avatar via Mixed 2D-3D Gaussian Splatting. <u>arXiv preprint arXiv:2412.04955</u> for sentence-to-video generation. In <u>Proceedings of the 27th ACM international</u> (2024). <u>conference on multimedia. 1239–1247.</u> 

- [6] Xiaowei Chi, Hengyuan Zhang, Chun-Kai Fan, Xingqun Qi, Rongyu Zhang, [29] Guanxing Lu, Shiyi Zhang, Ziwei Wang, Changliu Liu, Jiwen Lu, and Yansong Anthony Chen, Chi-min Chan, Wei Xue, Wenhan Luo, Shanghang Zhang, et al. Tang. 2024. Manigaussian: Dynamic gaussian splatting for multi-task robotic 2024. EVA: An Embodied World Model for Future Video Anticipation. <u>arXiv</u> manipulation. In <u>European Conference on Computer Vision. Springer, 349–366. preprint arXiv:2410.15461 (2024).</u> [30] Hao Lu, Tianshuo Xu, Wenzhao Zheng, Yunpeng Zhang, Wei Zhan, Dalong 

- [7] Michele Colledanchise and Lorenzo Natale. 2021. On the implementation of Du, Masayoshi Tomizuka, Kurt Keutzer, and Yingcong Chen. 2024. DrivingRebehavior trees in robotics. <u>IEEE Robotics and Automation Letters</u> 6, 3 (2021), con: Large 4D Gaussian Reconstruction Model For Autonomous Driving. <u>arXiv</u> 5929–5936. <u>preprint arXiv:2412.09043 (2024).</u> 

- [8] Chongkai Gao, Haozhuo Zhang, Zhixuan Xu, Cai Zhehao, and Lin Shao. [31] Yifan Lu, Xuanchi Ren, Jiawei Yang, Tianchang Shen, Zhangjie Wu, Jun Gao, Yue [n. d.]. FLIP: Flow-Centric Generative Planning as General-Purpose ManipWang, Siheng Chen, Mike Chen, Sanja Fidler, et al. 2024. InfiniCube: Unbounded ulation World Model. In <u>The Thirteenth International Conference on Learning</u> and Controllable Dynamic 3D Driving Scene Generation with World-Guided <u>Representations.</u> Video Models. <u>arXiv preprint arXiv:2412.03934 (2024).</u> 

- [9] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung, and [32] Tanya Marwah, Gaurav Mittal, and Vineeth N Balasubramanian. 2017. AtQiang Xu. 2023. Magicdrive: Street view generation with diverse 3d geometry tentive semantic video generation using captions. In <u>Proceedings of the IEEE</u> control. <u>arXiv preprint arXiv:2310.02601 (2023). international conference on computer vision. 1426–1434.</u> 

- [10] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, [33] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Guan Jun Zhang, and Hongyang Li. 2024. Vista: A generalizable driving world model Huang, Chen Liu, Yuyin Chen, Yida Wang, Xueyang Zhang, et al. 2024. Reconwith high fidelity and versatile controllability. <u>arXiv preprint arXiv:2405.17398</u> Dreamer: Crafting World Models for Driving Scene Reconstruction via Online (2024). Restoration. <u>arXiv preprint arXiv:2411.19548 (2024).</u> 

- [11] Razan Ghzouli, Thorsten Berger, Einar Broch Johnsen, Swaib Dragule, and An[34] Jingcheng Ni, Yuxin Guo, Yichen Liu, Rui Chen, Lewei Lu, and Zehuan Wu. drzej Wąsowski. 2020. Behavior trees in action: a study of robotics applications. 2025. MaskGWM: A Generalizable Driving World Model with Video Mask In <u>Proceedings of the 13th ACM SIGPLAN international conference on software</u> Reconstruction. <u>arXiv preprint arXiv:2502.11663 (2025). language engineering. 196–209.</u> [35] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, 

- [12] Pierre-Louis Guhur, Shizhe Chen, Ricardo Garcia Pinel, Makarand Tapaswi, Ivan Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElLaptev, and Cordelia Schmid. 2023. Instruction-driven history-aware policies for Nouby, et al. 2023. Dinov2: Learning robust visual features without supervision. robotic manipulations. In <u>Conference on Robot Learning. PMLR, 175–187. arXiv preprint arXiv:2304.07193 (2023).</u> 

- [13] Yuwei Guo, Ceyuan Yang, Anyi Rao, Maneesh Agrawala, Dahua Lin, and Bo Dai. [36] Yingwei Pan, Zhaofan Qiu, Ting Yao, Houqiang Li, and Tao Mei. 2017. To create 2024. Sparsectrl: Adding sparse controls to text-to-video diffusion models. In what you tell: Generating videos from captions. In <u>Proceedings of the 25th ACM European Conference on Computer Vision. Springer, 330–348. international conference on Multimedia. 1789–1798.</u> 

- [14] Tanmay Gupta, Dustin Schwenk, Ali Farhadi, Derek Hoiem, and Aniruddha [37] David Paulius, Alejandro Agostini, and Dongheui Lee. 2023. Long-horizon planKembhavi. 2018. Imagine this! scripts to compositions to videos. In <u>Proceedings</u> ning and execution with functional object-oriented networks. <u>IEEE Robotics and of the European conference on computer vision (ECCV). 598–613. Automation Letters 8, 8 (2023), 4513–4520.</u> 

- [15] Yingqing He, Menghan Xia, Haoxin Chen, Xiaodong Cun, Yuan Gong, Jinbo [38] David Paulius, Yongqiang Huang, Roger Milton, William D Buchanan, Jeanine Xing, Yong Zhang, Xintao Wang, Chao Weng, Ying Shan, et al. 2023. Animate-aSam, and Yu Sun. 2016. Functional object-oriented network for manipulation story: Storytelling with retrieval-augmented video generation. <u>arXiv preprint</u> learning. In <u>2016 IEEE/RSJ International Conference on Intelligent Robots and arXiv:2307.06940 (2023). Systems (IROS). IEEE, 2655–2662.</u> 

- [16] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and [39] Xiangyu Peng, Zangwei Zheng, Chenhui Shen, Tom Young, Xinying Guo, Binluo Sepp Hochreiter. 2017. Gans trained by a two time-scale update rule converge Wang, Hang Xu, Hongxin Liu, Mingyan Jiang, Wenjun Li, et al. 2025. Open-sora to a local nash equilibrium. <u>Advances in neural information processing systems</u> 2.0: Training a commercial-level video generation model in $200 k. <u>arXiv preprint</u> 30 (2017). <u>arXiv:2503.09642 (2025).</u> 

- [17] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad [40] Corrado Pezzato, Carlos Hernández Corbato, Stefan Bonhof, and Martijn Wisse. Norouzi, and David J Fleet. 2022. Video diffusion models. <u>Advances in Neural</u> 2023. Active inference and behavior trees for reactive action planning and <u>Information Processing Systems 35 (2022), 8633–8646.</u> execution in robotics. <u>IEEE Transactions on Robotics 39, 2 (2023), 1050–1069.</u> 

- [18] Wenyi Hong, Ming Ding, Wendi Zheng, Xinghan Liu, and Jie Tang. 2022. [41] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Cogvideo: Large-scale pretraining for text-to-video generation via transformers. Tengyu Ma, Haitham Khedr, Roman Rädle, Chloe Rolland, Laura Gustafson, <u>arXiv preprint arXiv:2205.15868 (2022).</u> et al. 2024. Sam 2: Segment anything in images and videos. <u>arXiv preprint</u> 

- [19] Li Hu. 2024. Animate anyone: Consistent and controllable image-to-video syn- <u>arXiv:2408.00714 (2024).</u> thesis for character animation. In <u>Proceedings of the IEEE/CVF Conference on</u> [42] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shot- <u>Computer Vision and Pattern Recognition. 8153–8163.</u> ton, Elahe Arani, and Gianluca Corrado. 2025. GAIA-2: A Controllable Multi- 

- [20] Nan Huang, Xiaobao Wei, Wenzhao Zheng, Pengju An, Ming Lu, Wei Zhan, View Generative World Model for Autonomous Driving. <u>arXiv preprint</u> Masayoshi Tomizuka, Kurt Keutzer, and Shanghang Zhang. 2024. S3Gaussian: <u>arXiv:2503.20523 (2025).</u> Self-Supervised Street Gaussians for Autonomous Driving. <u>arXiv preprint</u> [43] Md Sadman Sakib, David Paulius, and Yu Sun. 2022. Approximate task tree <u>arXiv:2405.20323 (2024).</u> retrieval in a knowledge network for robotic cooking. <u>IEEE Robotics and</u> 

Conference’17, July 2017, Washington, DC, USA 

Li et al. 

   - <u>Automation Letters 7, 4 (2022), 11492–11499.</u> 

- [44] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang, Oron Ashual, Oran Gafni, et al. 2022. Make-a-video: Textto-video generation without text-video data. <u>arXiv preprint arXiv:2209.14792</u> (2022). 

- [45] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. 2018. Towards accurate generative models of video: A new metric & challenges. <u>arXiv preprint arXiv:1812.01717 (2018).</u> 

- [46] Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, et al. 2025. Wan: Open and Advanced Large-Scale Video Generative Models. <u>arXiv preprint arXiv:2503.20314</u> (2025). 

- [47] Boyang Wang, Nikhil Sridhar, Chao Feng, Mark Van der Merwe, Adam Fishman, Nima Fazeli, and Jeong Joon Park. 2024. This&that: Language-gesture controlled video generation for robot planning. <u>arXiv preprint arXiv:2407.05530 (2024).</u> 

- [48] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. 2004. Image quality assessment: from error visibility to structural similarity. <u>IEEE transactions on image processing 13, 4 (2004), 600–612.</u> 

- [49] Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li, Tianshui Chen, Menghan Xia, Ping Luo, and Ying Shan. 2024. Motionctrl: A unified and flexible motion controller for video generation. In <u>ACM SIGGRAPH 2024 Conference Papers.</u> 1–11. 

- [50] Xiaobao Wei, Peng Chen, Guangyu Li, Ming Lu, Hui Chen, and Feng Tian. 2024. GazeGaussian: High-Fidelity Gaze Redirection with 3D Gaussian Splatting. <u>arXiv preprint arXiv:2411.12981 (2024).</u> 

- [51] Xiaobao Wei, Peng Chen, Ming Lu, Hui Chen, and Feng Tian. 2024. GraphAvatar: Compact Head Avatars with GNN-Generated 3D Gaussians. <u>arXiv preprint arXiv:2412.13983 (2024).</u> 

- [52] Xiaobao Wei, Qingpo Wuwu, Zhongyu Zhao, Zhuangzhe Wu, Nan Huang, Ming Lu, Ningning Ma, and Shanghang Zhang. 2024. EMD: Explicit Motion Modeling for High-Quality Street Gaussian Splatting. <u>arXiv preprint arXiv:2411.15582</u> (2024). 

- [53] Jinbo Xing, Menghan Xia, Yuxin Liu, Yuechen Zhang, Yong Zhang, Yingqing He, Hanyuan Liu, Haoxin Chen, Xiaodong Cun, Xintao Wang, et al. 2024. Makeyour-video: Customized video generation using textual and structural guidance. <u>IEEE Transactions on Visualization and Computer Graphics (2024).</u> 

- [54] Jinbo Xing, Menghan Xia, Yong Zhang, Haoxin Chen, Wangbo Yu, Hanyuan Liu, Gongye Liu, Xintao Wang, Ying Shan, and Tien-Tsin Wong. 2024. Dynamicrafter: Animating open-domain images with video diffusion priors. In <u>European Conference on Computer Vision. Springer, 399–417.</u> 

- [55] Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. 2025. Depth anything v2. <u>Advances in Neural Information Processing Systems 37 (2025), 21875–21911.</u> 

- [56] Yezhou Yang, Anupam Guha, Cornelia Fermüller, and Yiannis Aloimonos. 2014. Manipulation action tree bank: A knowledge resource for humanoids. In <u>2014 IEEE-RAS International Conference on Humanoid Robots. IEEE, 987–992.</u> 

- [57] Zhuo Yang and Zhizhou Jia. 2023. Robot Behavior Tree Manipulation Using Language Models. In <u>2023 IEEE 11th Joint International Information Technology and Artificial Intelligence Conference (ITAIC), Vol. 11. IEEE, 1342–1345.</u> 

- [58] Shengming Yin, Chenfei Wu, Jian Liang, Jie Shi, Houqiang Li, Gong Ming, and Nan Duan. 2023. Dragnuwa: Fine-grained control in video generation by integrating text, image, and trajectory. <u>arXiv preprint arXiv:2308.08089 (2023).</u> 

- [59] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. 2023. Adding conditional control to text-to-image diffusion models. In <u>Proceedings of the IEEE/CVF international conference on computer vision. 3836–3847.</u> 

- [60] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. 2018. The unreasonable effectiveness of deep features as a perceptual metric. In <u>Proceedings of the IEEE conference on computer vision and pattern recognition.</u> 586–595. 

- [61] Shiwei Zhang, Jiayu Wang, Yingya Zhang, Kang Zhao, Hangjie Yuan, Zhiwu Qin, Xiang Wang, Deli Zhao, and Jingren Zhou. 2023. I2vgen-xl: High-quality image-tovideo synthesis via cascaded diffusion models. <u>arXiv preprint arXiv:2311.04145</u> (2023). 

- [62] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xueyang Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, et al. 2024. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. <u>arXiv preprint arXiv:2410.13571 (2024).</u> 

- [63] Siyuan Zhou, Yilun Du, Jiaben Chen, Yandong Li, Dit-Yan Yeung, and Chuang Gan. 2024. RoboDreamer: Learning compositional world models for robot imagination. <u>arXiv preprint arXiv:2404.12377 (2024).</u> 

Conference’17, July 2017, Washington, DC, USA 

ManipDreamer: Boosting Robotic Manipulation World Model with Action Tree and Visual Guidance 


|**Algorithm 1**Dynamic Mask Generation|
|---|
|**Require:** First frame_𝐼_0 ∈R<sup>3×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup>, Other frames_𝐼_1_, 𝐼_2_, . . . , 𝐼𝑇_∈<br>R<sup>3×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup>|
|**Ensure:** Final dynamic mask_𝑀_∈R<sup>_𝐻_×</sup><sup>_𝑊_</sup><br>|
|1: _𝐹_0 ←Extract feature vectors from_𝐼_0<br>_⊲𝐹_0 ∈R<sup>_𝐶𝑠𝑎𝑚_×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup>|
|2: **for**_𝑡_=1 to_𝑇_**do**|
|3:<br>_𝐹𝑡_←Extract feature vectors from_𝐼𝑡_<br>_⊲𝐹𝑡_∈R<sup>_𝐶𝑠𝑎𝑚_×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup>|
|4:<br>_𝑆𝑡_←Compute pointwise similarity between_𝐹_0 and_𝐹𝑡_<br>_⊲_<br>_𝑆𝑡_∈R<sup>_𝐻_×</sup><sup>_𝑊_</sup><br>|
|5:<br>_𝑀𝑡_←1−_𝑆𝑡_<br>_⊲𝑀𝑡_∈R<sup>_𝐻_×</sup><sup>_𝑊_</sup>|
|6: **end for**<br><br>|
|7: _𝑀_←<sup>1</sup><br>_𝑇_<br>�_𝑇_<br>_𝑡_=1 <sup>_𝑀𝑡_</sup><br>_⊲_Average over all frames<br>8: **return**_𝑀_|


### **B Training Protocol** 

**Figure 4: Distribution of average modality weights across layers 1, 4, 7, and 10 in our multi-modal visual adapter. The results demonstrate the relative importance of each modality in different network layers.** 

### **A Multi Scene Modality Acquisition** 

Due to lack of extra modality data in the RT-1 dataset, we obtain the depth, segmentation feature and dynamic mask using the following methods. 

**Depth estimation acquisition.** We obtain depth using the estimation of Depth Anything v2, which is able to generate precise and consistent depth giving a single monocular image. In particular, we use the ViT-L version of Depth Anything v2. 

**Segmentation feature acquisition.** We utilize the SAM2 model to get segmentation feature of the input scene snapshot. In particular, we use the SAM2 tiny for to save memory and forward time, which still performs well despite the smallest version of the series. **Dynamic mask acquisition.** We use the algorithm 1 to obtain dynamic mask from the pixel level feature of SAM2. 

### **B.1 Video Quality evaluations on RT-1** 

We trained RoboDreamer [63] as our base model for 240k steps (global batch size 128) using DDP across 8 H800 GPUs (2 days total). The UNet backbone remains frozen in all experiments to ensure fair comparison and demonstrate the effectiveness of our proposed enhancements. 

### **B.2 Task Execution in RLBench** 

We collected 200 episodes per evaluated task in RLbench [21], supplemented with additional episodes from other tasks to increase dataset diversity. All tasks were trained jointly to produce a single unified model. The diffusion model was initialized with RT-1 pretrained weights and fine-tuned for approximately 60k steps, focusing exclusively on macro-step generation. 

### **C Modality Weight Analysis** 

To quantify the contribution of each modality in our ManipDreamer framework, we analyzed the average weights generated by the patch-level router in our cross-attention fusion mechanism variant. We conducted 100 forward passes with initial observations and computed the mean weight values for each modality across different layers (1, 4, 7, and 10). As shown in Table 4, our analysis reveals that the model consistently assigns the highest weight to depth information across all layers, indicating its predominant role in the fusion process. 

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009 

