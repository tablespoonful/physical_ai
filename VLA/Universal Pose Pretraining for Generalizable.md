---
title: "Universal Pose Pretraining for Generalizable Vision-Language-Action Policies"
date: "2026-02-23"
authors: "Haitao Lin; Hanyang Yu; Jingshun Huang; He Zhang; Yonggen Ling; Ping Tan"
venue: "RSS 2026"
url: https://arxiv.org/abs/2602.19710
pdf: https://arxiv.org/pdf/2602.19710
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.19710)** / [論文ページ](https://arxiv.org/abs/2602.19710)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# Universal Pose Pretraining for Generalizable Vision-Language-Action Policies 

Haitao Lin<sup>1</sup><sup>_,_2</sup><sup>_∗,†_</sup> Hanyang Yu<sup>3</sup><sup>_∗,‡_</sup> Jingshun Huang<sup>4</sup><sup>_,_5</sup><sup>_∗,‡_</sup> He Zhang<sup>1</sup><sup>_,_2</sup> Yonggen Ling<sup>1</sup><sup>_,_2</sup> Ping Tan<sup>3</sup><sup>_†_</sup> Xiangyang Xue<sup>4</sup> Yanwei Fu<sup>4</sup><sup>_,_5</sup><sup>_†_</sup> 

> 1 Tencent Robotics X 2 Futian Laboratory 

> 3 The Hong Kong University of Science and Technology 

> 4 Fudan University 5 Shanghai Innovation Institute 

**Project Page:** https://hetolin.github.io/PoseVLA 

**_Abstract_ —Existing Vision-Language-Action (VLA) models often suffer from feature collapse and low training efficiency because they entangle high-level perception with sparse, embodiment-specific action supervision. Since these models typically rely on VLM backbones optimized for Visual Question Answering (VQA), they excel at semantic identification but often overlook subtle 3D state variations that dictate distinct action patterns. To resolve these misalignments, we propose PoseVLA, a decoupled paradigm that separates VLA training into a pre-training phase for extracting universal 3D spatial priors in a unified camera-centric space, and a post-training phase for efficient embodiment alignment within robot-specific action space. By introducing discrete pose tokens as a universal representation, Pose-VLA seamlessly integrates spatial grounding from diverse 3D datasets with geometry-level trajectories from robotic demonstrations. Our framework follows a two-stage pre-training pipeline, establishing fundamental spatial grounding via poses followed by motion alignment through trajectory supervision. Extensive evaluations demonstrate that Pose-VLA achieves stateof-the-art results on RoboTwin 2.0 with a 79.5% average success rate and competitive performance on LIBERO at 96.0%. Realworld experiments further showcase robust generalization across diverse objects using only 100 demonstrations per task, validating the efficiency of our pre-training paradigm.** 

## I. INTRODUCTION 

The pursuit of general-purpose embodied intelligence has been significantly accelerated by the emergence of VisionLanguage-Action (VLA) models. State-of-the-art frameworks such as _π_ [5, 6] and the GR00T series [4] have demonstrated remarkable potential in end-to-end robotic manipulation through the adoption of dual-system architectures. In this paradigm, a Vision-Language Model (VLM) acts as a highlevel semantic interpreter, while a specialized action expert that employs generative techniques like flow matching [28] serves as the low-level controller for precise action denoising. 

Despite these advances, scaling vision-language representations into physically grounded, generalizable action policies remains a fundamental challenge. While existing VLAs leverage off-the-shelf VLMs [3, 2, 39] as perception backbones, their general semantic features often fail to translate into 

> _∗_ Equal contribution. 

> _†_ Corresponding authors. 

> _‡_ Work done during an internship at Tencent Robotics X. 


Fig. 1. Overview of Pose-VLA. Unlike previous VLAs that rely solely on sparse action supervision, our approach decouples policy learning into two stages by _using unified pose prediction as a proxy task_ : (1) Pre-training, extracting universal 3D spatial priors in a unified camera-centric space; and (2) Alignment, adapting these priors to specific embodiments. This decoupling allows the model to leverage diverse 3D datasets, enabling efficient transfer as backbone when adapting to robotic control with only few-shot fine-tuning. 

robust downstream policy performance. This discrepancy is reinforced by recent findings [56] showing that fine-tuning on auxiliary tasks like depth estimation or VQA does not inherently guarantee improved control. This persistent gap underscores a critical open question: _how can we efficiently adapt VLMs to acquire transferable embodied priors that directly facilitate downstream policy learning?_ 

We observe that this failure is not incidental, but structural. It stems from two persistent misalignments between how VLMs are pretrained and how robotic actions are defined. (1) **Granularity Mismatch** : VLM pretraining is dominated by tasks such as image–text alignment and visual question answering, which emphasize categorical recognition and highlevel semantics. Robotic manipulation, in contrast, depends critically on fine-grained 3D state variations, such as subtle changes in pose, contact geometry, or relative motion that demand qualitatively different actions. As a result, a VLM may correctly recognize what an object is while remaining 

insensitive to how its physical state evolves. (2) **Data Heterogeneity Gap** : Internet-scale visual corpora lack physical action grounding, while robotic demonstration datasets are scarce, narrowly distributed, and expensive to collect. Existing VLAs struggle to reconcile these two extremes, preventing them from absorbing diverse spatial experiences while remaining relevant to real-world control. 

To address these challenges, we propose a decoupled learning paradigm for Vision–Language–Action modeling. Rather than entangling perception with embodiment-specific actions as in prior VLAs [5, 20], we separate learning into two stages as in Fig. 1: (1) large-scale pretraining of universal spatial priors in a unified, camera-centric observation space, and (2) lightweight post-training for embodiment alignment. This decoupling fundamentally reshapes the objective of largescale pre-training. By incorporating 3D spatial supervision, the model learns to distinguish subtle 3D variations that dictate distinct action patterns. Once these robust spatial priors are established, the VLM serves as a powerful initialization that makes adapting to a new robotic policy significantly more efficient than learning from scratch. 

Building on this principle, we introduce Pose-VLA, a framework that re-centers VLA learning around a universal pose representation. In this architecture, pose acts as a _structural bridge_ that maps high-level visual perception to low-level physical execution. Specifically, (1) to bridge the _granularity mismatch_ , we represent object states and actions as 3D poses and temporal sequences, explicitly constraining the model to reason over fine-grained spatial supervision. (2) To bridge the _data heterogeneity gap_ , pose tokens provide a common language across diverse 3D sources, enabling Pose-VLA to ingest large-scale non-robotic 3D datasets alongside limited robot demonstrations. By unifying these elements, Pose-VLA transforms the VLM into a geometrically-aware backbone optimized for downstream manipulation. 

Technically, Pose-VLA builds upon the PaliGemma [3] architecture to unify semantic understanding with spatial grounding. We integrate RGB images with depth maps and camera intrinsics encoded as raymaps to instill intrinsic 3D awareness. A modality masking strategy is employed during training to ensure robustness to varying sensor availability at inference time. We further extend the language model vocabulary with discrete pose tokens that represent 3D transformations in the camera frame, enabling a unified tokenization of spatial information across heterogeneous datasets. 

Our training follows a two-stage pipeline. First, spatial foundation pre-training on large-scale 3D datasets establishes geometric grounding. Second, pose alignment pre-training leverages dense multi-view supervision to project robotic trajectories into the same camera-centric observation space. Together, these stages transform the VLM from a semantic describer into a foundation for embodied control. During posttraining, we follow [5] by appending a lightweight action expert that maps pretrained representations into robot-specific commands. This strategy ensures that the VLM acquires rich, 3D-aware features that drastically reduce the amount of 

demonstration data required for downstream policy adaptation. 

Our contributions are summarized as follows: (1) we propose a unified VLM framework that integrates RGB images, depth maps, and camera intrinsics to instill intrinsic 3D awareness, facilitating the effective transfer of vision-language knowledge to robotic control; (2) we introduce discrete Pose Tokens as a universal interface (within consistent cameracentric observation space) for aligning and ingesting spatial priors from heterogeneous non-robotic 3D data and specialized robotic demonstrations; and (3) we curate a comprehensive pre-training corpus comprising 1.4M images with 6.5M 3D annotations for spatial grounding, complemented by approximately 1.55M diverse robotic trajectories for motion alignment. (4) we demonstrate that Pose-VLA achieves state-of-theart performance on RoboTwin 2.0 (avg. 79.5% success) and competitive results on LIBERO (avg. 96.0%); notably, a single multi-task model exhibits robust real-world generalization across rigid, articulated, and deformable objects, requiring as few as 100 demonstrations per task. 

## II. RELATED WORK 

**Vision-Language Models for 3D Grounding** Growing efforts extend VLMs to 3D understanding [16, 39, 44, 52, 12, 51, 45], as spatial grounding is crucial for robotic manipulation [26, 27, 50, 17, 57, 25, 49]. Unlike earlier language conditioned pipelines that sequentially detect and estimate poses [43, 14, 9], VLMs provide the distinct advantage of direct, open vocabulary 3D grounding. Several methods focus specifically on bridging the gap between vision-language reasoning and 3D geometric tasks. For instance, SpatialLM [35] performs 3D grounding from point clouds to generate 3D bounding boxes, although it is limited to a small number of object categories. Spatial-Reasoner [33] estimates object positions and orientations as intermediate outputs to enhance spatial awareness, while the concurrent N3D-VLA [48] utilizes a massive depth-lifted dataset to enable 3D localization via bounding boxes, yet lacks explicit orientation modeling. Unlike previous methods, Pose-VLA utilizes pose tokens to unify object poses and motion trajectories within a shared representation. This enables joint pre-training on heterogeneous 3D datasets and robotic demonstrations, while incorporating camera rays and depth as spatial priors to provide the additional geometric awareness for 3D grounding and robotic manipulation. **Vision-Language-Action Models** Vision-Language-Action (VLA) models extend the reasoning capabilities of VisionLanguage Models (VLMs) to the direct prediction of robotic actions. Current VLA methods can be generally categorized into discrete and continuous action outputs. Discrete approaches [61, 20, 36, 54, 47, 23, 30, 15] treat action prediction as a next-token prediction task in order to align with the native training paradigm of Large Language Models (LLMs). Alternatively, continuous approaches [46, 5, 4, 6, 21, 32, 40, 30, 53, 37] add generative heads like diffusion or flowmatching to achieve higher control fidelity. Despite these advances, how to effectively adapt a VLM’s semantic and reasoning abilities to the action modality remains an open 

question. Recent studies indicate that while VLM pre-training is fundamental, a model’s general VQA competence does not always predict its downstream control performance, highlighting a persistent domain gap. To bridge this gap, strategies like co-training with vision-text data [6, 60, 24, 37] or incorporating Embodied Chain-of-Thought (ECoT) [54, 21, 11, 42] have been proposed to preserve reasoning traces. Furthermore, some VLAs [22, 19, 58] introduce regularization within the VLM’s latent space, such as aligning mid-layer features with a vision teacher or utilizing hidden space world modeling. While VLM4VLA [56] indicates that fine-tuning VLMs on auxiliary tasks rarely translates to better policy performance, we show that 3D pose pre-training establishes a vital geometric foundation for downstream control. 

## III. METHOD 

## _A. Preliminaries_ 

Given a multi-modal observation **O** and a language instruction **L** , Pose-VLA aims to model the joint probability of an output token sequence **S** . Following the auto-regressive paradigm, the generation process is formulated as: 


where **s** _k_ denotes the _k_ -th token in a sequence of length _K_ , and **L** represents the natural language instruction. To bridge high-level semantics with fine-grained 3D control, we define the output as a structured sequence of tuples _S_ = ( _τ_ 1 _, τ_ 2 _, . . . , τT_ ), where each tuple _τt_ serves as the fundamental unit for spatial representation: 


In this formulation, **c** _t_ represents the object category, **b** _t ∈_ R<sup>2</sup> denotes the box center in image coordinates, and **p** _t ∈ SE_ (3) signifies the pose in the camera-centric frame. This design enables _τt_ to serve as a universal geometric primitive: in static contexts, it localizes the object for spatial grounding; in temporal sequences, it characterizes the trajectory waypoints for motion estimation. By unifying 2D centroids with 3D poses, _τt_ provides a versatile representation that describes both discrete physical entities and continuous motion paths within a unified generative framework. 

## _B. VLM architecture_ 

Our approach adopts PaliGemma [3] as the backbone. PaliGemma employs SigLip [55] as the visual encoder, which extracts rich semantic features from images. However, PaliGemma is trained mainly on the VQA task and detection task. We empirically find that such supervision on text level or 2D location-level may focus on high-level semantics, while losing the fine-grained details for control-oriented features. Thus, we use the pose as the universal representation to bridge the non-robotics data in computer vision task and robotics data in manipulation task as in Fig. 2. As pose is described in the 3D world, it can force the model to understand 

the spatial relationship in the 3D world. To maintain the inherent 2D visual grounding capabilities, we reuse the text and <loc> vocabularies from the original PaliGemma model for representing **c** _t_ and **b** _t_ . 

To incorporate 3D priors, we leverage auxiliary inputs, including depth maps and camera intrinsics, which are commonly available in 3D-annotated, non-robotic datasets. The inclusion of such auxiliary information has been shown to markedly improve 3D prediction performance at test time. 

For 3D-annotated non-robotics data, poses are defined within the camera coordinate frame. To maintain alignment with these diverse geometric datasets, our approach requires the model to predict actions directly within the camera frame of the image view, rather than estimating robot-centric actions defined in the robot’s base frame. This design ensures a shared camera-centric representation across heterogeneous data sources, enabling the model to fully leverage the 3D awareness acquired during VLM pre-training for precise robotic control. 

## _C. Unified Pose Representation_ 

We adopt 3D pose as a universal representation to unify the feature spaces of non-robotic 3D datasets and robotic manipulation data. This choice is motivated by the fact that both objects and robotic grippers can be effectively parameterized within this shared geometric space. By imposing this representation, we constrain the model to estimate spatial coordinates directly from visual observations within the camera frame, which naturally fosters the development of robust 3D spatial grounding capabilities. To implement this, we introduce a dedicated **pose token** defined in the camera coordinate system. This design choice explicitly addresses the challenge of coordinate misalignment encountered during pre-training, facilitating a seamless integration of diverse data sources into a consistent framework. 

We represent object states and robotic motion trajectories using a parameterization of translation and rotation. In the following sections, we detail the implementation of these pose tokens and demonstrate their versatility across both general 3D spatial grounding and embodied robotic manipulation tasks. **Object-Level Representation.** Each object is characterized by its rigid-body transformation, comprising translation and rotation. We discretize these continuous parameters to integrate them into the VLM as an extended vocabulary of specialized tokens. For rotation, we perform uniform quantization of the Euler angles and assign a dedicated <rot> token to each principal axis. 

Regarding translation, an empirical analysis of our largescale pre-training statistics reveals a distinct distributional divergence between the lateral ( _x, y_ ) and longitudinal ( _z_ ) axes as shown in our Appendix. While the _x_ and _y_ distributions exhibit comparable means and variances, the _z_ -axis (depth) distribution is significantly shifted, reflecting the inherent perspective projection and depth range of the camera. To accommodate this discrepancy and enforce depth-aware geometric grounding, we employ a shared <trans_xy> token 


Fig. 2. Pipeline of Pose-VLA. Pose-VLA decouples VLA training into: (1) **Pre-training** for extracting universal 3D spatial priors in a camera-centric space, and (2) **Post-training** for embodiment alignment. The VLM predicts a structured sequence _S_ = ( _τ_ 1 _, . . . , τT_ ) via next-token prediction, where each tuple _τt_ = _{_ **c** _t,_ **b** _t,_ **p** _t}_ consists of a category **c** _t_ , 2D box center **b** _t_ , and camera-centric pose **p** _t_ . To enhance spatial reasoning, auxiliary 3D geometry priors are integrated via additive fusion with RGB embeddings, analogous to positional encodings. This unified format enables seamless knowledge transfer from diverse 3D datasets to robotic domains, achieving robust alignment with minimal demonstrations. 

for the _x_ and _y_ dimensions and a distinct <trans_z> token for the depth dimension. 

To evaluate 3D grounding performance in general 3D benchmark [7], we incorporate object scale into the representation. Since object dimensions across all three axes exhibit similar statistical characteristics, we represent object scale using a unified <size> token for spatial dimensions. 

By mapping image observations into structured pose tokens, Pose-VLA establishes a direct correspondence between image pixels and physical entities within a metric-aligned coordinate system. Unlike previous methods [2, 34] that rely on decomposing numerical coordinates into individual digit tokens, our tokenization scheme significantly enhances efficiency by reducing the required token sequence length per coordinate. Crucially, this approach ensures that all task data are optimized within a shared real-world metric space, enabling a unified physical vocabulary across both perception and action. By supervising the model to estimate target object poses, we drive the network to implicitly learn 3D spatial features, leading to a level of fine-grained geometric reasoning that far surpasses the capabilities of conventional VLMs dominated by VQA supervision. 

**Trajectory-Level Representation.** Robot actions can be parameterized by the 6-DoF pose of the gripper. By adopting this convention, the gripper pose can directly reuse the discretized tokens established for object-level representations. For dynamic manipulation, we represent action trajectories as temporally ordered sequences of these unified pose tokens. 

Unlike contemporary VLA frameworks [20] that define actions as joint angles or base-frame poses, our approach addresses the fundamental misalignment between the observation space (camera-centric) and the action space (robot-centric). 

Such spatial discrepancies often hinder cross-embodiment generalization, as the model must implicitly bridge the gap between localized visual observations and a global robot-base coordinate system. To resolve this conflict, we project all action trajectories into the respective camera coordinate frame of each view. This alignment ensures that both non-robotic 3D grounding data and robotic demonstration data share a consistent geometric reference frame. 

By supervising the model to estimate future trajectories directly within the image observation space, we provide a significantly denser and more grounded supervision signal compared to mapping pixels to embodiment-specific tokens [20]. Furthermore, this camera-centric formulation enhances implicit 3D correspondence learning across diverse viewpoints, such as head-mounted and wrist-mounted cameras. This dense supervision encourages the model to learn representative, control-oriented features that are sensitive to subtle variations between consecutive observations. Ultimately, representing the gripper and objects within a shared token space unifies the optimization objectives of large-scale computer vision and robotics tasks, facilitating the scalable transfer of 3D geometric knowledge to downstream robotic manipulation. 

## _D. Adding Prior Conditioning_ 

To enhance the framework’s geometric awareness, we incorporate auxiliary spatial priors. Inspired by Pow3R [18], these embeddings are integrated via additive fusion with the RGB token embeddings prior to the initial Transformer block, analogous to standard positional encodings. 

**Camera Ray Encoding.** To establish a direct correspondence between pixels and their physical viewing directions, we construct camera rays derived from the intrinsic matrix **K** _∈_ R<sup>3</sup><sup>_×_3</sup> . The ray **r** for each pixel ( _u, v_ ) is computed 

as **r** = **K**<sup>_−_1</sup> [ _u, v,_ 1]<sup>_⊤_</sup> , which encodes the viewing direction relative to the camera’s optical center. This ray encoding enables the model to effectively process non-centered crops and facilitates high-resolution inference by providing absolute geometric anchors. Following the RGB processing pipeline, these dense ray maps are patchified and projected into the latent space before being fused with the visual features. **Depth Prior Integration.** For the depth prior, given a depth map **D** and its corresponding sparsity mask **M** , we deliberately avoid value normalization to maintain explicit alignment with the metric space. We stack the depth and mask into a joint representation [ **D** _,_ **M** ] _∈_ R<sup>_H×W ×_2</sup> , which is then patchified and embedded. This configuration allows the encoder to robustly handle varying levels of sparsity through integrated valid-pixel masking. 

This multi-modal conditioning ensures the seamless integration of semantic and 3D geometric information, significantly bolstering the model’s capacity for precise 3D reasoning in complex manipulation scenarios. 

## _E. Training Strategy_ 

**Pre-training stage.** In this stage, we employ a next-token prediction loss to instill fundamental spatial priors into the model. To preserve the extensive vision-language capabilities of the base VLM, we jointly supervise the generation of 2D localization tokens and our extended 3D pose tokens. Given the multi-modal input **O** and language instruction **L** , we utilize the standard auto-regressive objective: 


where _sk_ denotes the _k_ -th token in the structured sequence _S_ , and _ϕ_ ( **O** ) represents the modality masking strategy. Specifically, during training, we randomly zero-pad raymaps or depth values to ensure the model maintains robust inference capabilities even with RGB-only inputs. Furthermore, for depth images, we sample sparse depth points to enhance robustness to diverse sensor noise patterns. This training phase equips the VLM with coarse yet semantically grounded spatial awareness, enabling it to transition from a semantic describer to a geometric reasoner. 

**Post-training stage.** For embodiment alignment, we follow [5] by appending a lightweight action expert to map the pretrained representations from the VLM backbone into robotspecific commands. This decoupling allows our primary focus to remain on large-scale spatial prior acquisition during pre-training. Specifically, we employ a flow matching objective [28, 31] to denoise the action tokens, where the VLM backbone interacts with the action expert through selfattention layers to provide semantic and geometric conditioning. Notably, the action expert is trained from scratch without inheriting initialization parameters from [5], ensuring that the learned alignment is natively grounded in our PoseVLA representations. 

**Remark on Inference:** We emphasize that 3D pose prediction serves strictly as an _auxiliary proxy task_ during pre-training to learn spatial representations. At inference time, the action expert maps implicit features directly to continuous actions end-to-end, introducing zero overhead for explicit pose or camera trajectory estimation. 

## _F. Pre-training Datasets_ 

Our pre-training utilizes two types of datasets: **(1) Spatial Grounding and 3D Perception.** We curate 1.4M images with 6.5M 3D annotations across three pillars: (1) _General 3D Detection_ via Omni3D [7] (Objectron, SUN RGB-D, ARKitScene); (2) _6D Pose Estimation_ via Omni6DPose [57] (SOPE, ROPE); and (3) _Manipulation-centric Perception_ from the BOP Challenge (YCB-V, LineMOD, HOT3D). This mixture of real and synthetic data ensures robust awareness of 3D geometry and lighting variations. **(2) Robotic Trajectory Pretraining.** This stage aligns spatial features with motion control using nearly 1.55M trajectories. All end-effector poses are transformed into a unified camera-centric frame via calibration parameters provided by datasets. (1) _AgibotWorld Beta (Real):_ 1M trajectories from 100 isomorphic robots, covering 200 tasks and 87 atomic skills. (2) _InternData-A1 (Sim):_ 550K trajectories across heterogeneous platforms, including ARX, Aloha, Franka. Spanning 4 embodiments and 227 scenes, it provides dense supervision for articulated objects and longhorizon tasks. 

**Implementation Details.** The model is optimized via AdamW with a cosine schedule, reaching a peak learning rate of 5 _×_ 10<sup>_−_5</sup> after a 1,000-step warmup. This is followed by a cosine decay to a minimum of 2 _._ 5 _×_ 10<sup>_−_6</sup> . Training is performed on 16 NVIDIA H20 GPUs with bfloat16 precision and a perGPU batch size of 8. Specifically, both 3D spatial grounding and trajectory estimation tasks are completed within 2 days each on 16 H20 GPUs. This approach significantly reduces GPU hours compared to previous VLA training [4, 5] while effectively instilling robust spatial priors for the VLM. 

## IV. EXPERIMENT 

## _A. Evaluation in 3D Grounding Benchmarks_ 

**Baselines.** For the 3D grounding task, we compare against recent open-source and closed-source vision-language models capable of end-to-end 3D spatial grounding directly from language prompts. Our open-source baselines include the Qwen3-VL series [39] and the Visual Spatial Tuning (VST) models [52]. For closed-source baselines, we evaluate against Seed1.5-VL [16], Gemini-2.0-Pro [13], and the state-of-the-art Gemini Robotics-ER [44], as their settings align most closely with our experimental protocol. 

**Evaluation Metrics.** Following the protocols established in Qwen3-VL [39] and Seed1.5-VL [16], we adopt Average Precision (AP) as our primary evaluation metric. Each evaluation input consists of an image-text pair, where the textual prompt specifies the target object category. To ensure a fair and consistent comparison with existing VLMs, we set the Intersection over Union (IoU) threshold to 0.15 and report 

mAP@0.15 on the Omni3D test set [7]. We primarily conduct evaluations on the SUN-RGBD [41] and Objectron [1] subsets of Omni3D [7], which cover a wide range of indoor and tabletop environments. In line with previous benchmarks, the detection confidence for all predictions is fixed at 1.0 to evaluate the spatial grounding accuracy independently of confidence scoring. 

**Results and Analysis** Table I summarizes the 3D spatial grounding performance across various foundational models. Our proposed Pose-VLA achieves a substantial performance leap on the _Objectron_ dataset, reaching an _AP_ 15 of 87.3. This represents a 16.1% absolute improvement over the strongest open-source baseline, Qwen3-VL [39] (235B, _Thinking_ ), and a significant margin over closed-source models such as Seed1.5VL [16] and Gemini-2.0-Pro [44]. On the SUN RGB-D benchmark [41], Pose-VLA delivers a competitive score of 45.5, outperforming all open-source variants and the VST-3BSFT [52] model, while remaining closely comparable to the state-of-the-art Gemini Robotics-ER [44]. 

The results on Objectron [1] are particularly significant as they highlight the model’s robust capability in handling diverse daily objects essential for robotic manipulation, such as _bottles, cups, and cameras_ . While SUN RGB-D evaluates general indoor scene understanding, Objectron demands precise geometric localization of individual objects. The fact that Pose-VLA maintains superior spatial awareness across both large-scale indoor environments and object-centric contexts validates our _pose-centric_ pre-training paradigm. 

Crucially, Fig. 3 demonstrates that Pose-VLA generalizes robustly across unseen scenarios, ranging from tabletop layouts to complex robotic workspaces. Unlike baselines that frequently suffer from orientation misalignment in novel environments, Pose-VLA provides precise localization and orientation estimation. This superior generalization highlights the effectiveness of utilizing auxiliary spatial priors and diverse 3D datasets, enabling the model to maintain high-fidelity spatial awareness even in out-of-distribution scenarios. 

TABLE I 

COMPARISON OF 3D SPATIAL GROUNDING PERFORMANCE USING THE _AP_ 15 METRIC ACROSS DIFFERENT VLM BACKBONES. BASELINE RESULTS ARE SOURCED FROM THE OFFICIAL QWEN3-VL REPORT [39]. 

|Category|Model|SUN RGB-D [41]|Objectron [1]|
|---|---|---|---|
||Qwen3-VL [39] (235B, Thinking)|34.9|71.2|
||Qwen3-VL [39] (235B, Instruct)|39.4|-|
|Open|Qwen3-VL [39] (4B, Instruct)|34.7|-|
|Source|Qwen3-VL [39] (2B, Instruct)|33.8|-|
||VST-SFT(3B) [52]|37.3|-|
||VST-RL(3B) [52]|40.1|-|
|Cld|Seed1.5-VL [16]|33.5|8.1|
|ose<br>Source|Gemini-2.0-Pro [13]|32.5|5.5|
||Gemini Robotics-ER [44]|**48.3**|-|
||Ours-VLM (3B)|45.5|**87.3**|


## _B. Evaluation in Simulation Benchmarks_ 

To evaluate the cross-embodiment generalization and tasklevel robustness of Pose-VLA, we conduct extensive experi- 

ments on two large-scale simulation benchmarks: RoboTwin2.0 [10] and LIBERO [29]. 

**RoboTwin-2.0.** To evaluate the generalization capabilities of our method, we perform _multi-task training_ on the RoboTwin2.0 benchmark [10]. Specifically, Pose-VLA and all baseline models [5, 6, 3] are trained on a comprehensive dataset comprising 2,500 demonstrations collected in clean scenes (50 per task), augmented with an additional 25,000 demonstrations gathered in heavily randomized scenes (500 per task). To ensure a strictly fair comparison across this dataset, all models are initialized from their respective pre-trained checkpoints and fine-tuned using an identical training budget of 80K optimization steps with a total batch size of 32. 

To rigorously assess performance under distribution shifts, we conduct inference across both ”Easy” and ”Hard” scenarios. While the ”Easy” setting serves as a controlled baseline, the ”Hard” scenes introduce significant visual and geometric noise to evaluate the model’s robustness. We report the average success rate over 100 evaluation trials per task. 

**LIBERO.** Following the protocol of OpenVLA [20], we evaluate our model on four distinct task suites: LIBEROSpatial, LIBERO-Object, LIBERO-Goal, and LIBERO-Long. Each suite comprises 10 diverse tasks with 500 demonstrations in total. These benchmarks allow us to evaluate Pose-VLA across multiple dimensions, ranging from spatial reasoning to long-horizon planning. We compare our approach against a broad range of state-of-the-art generalist policies, including OpenVLA [20], SpatialVLA [38], _π_ 0 [5], _π_ 0 _._ 5 [6], _π_ 0-FAST [36], CoT-VLA [59], WorldVLA [8], and GR00T-N1 [4]. **Results and Analysis.** Table II and Table III present the comprehensive evaluation results across simulation benchmarks. To ensure a fair comparison with RGB-only baselines, we evaluate Pose-VLA using only RGB input by masking out depth and raymap modalities. On RoboTwin 2.0, Pose-VLA establishes a new state-of-the-art, achieving an average success rate of 79.1% in the challenging _Hard_ setting. This represents a substantial margin of 14.0% over the strong baseline _π_ 0 and a dramatic improvement of over 45% compared to the vanilla PaliGemma baseline, confirming that our spatial pretraining effectively prevents feature collapse where standard VQA-oriented backbones fail. Extending this evaluation to LIBERO, Pose-VLA demonstrates superior cross-task generalization with an overall average of 96.0%, surpassing _π_ 0 and ranking second only to _π_ 0 _._ 5. Notably, in the LIBERO-Long suite which demands multi-stage reasoning, our model attains 92.4%, tying with _π_ 0 _._ 5 for the top position. Thus, these results validate that integrating 3D spatial priors not only enhances robustness against visual perturbations but also provides the structural consistency required for long-horizon planning. 

## _C. Evaluation in Real-world Tasks._ 

**Real-world Experimental Setup.** We evaluate our model using a Dual-arm Xtrainer robotic platform, where each arm is equipped with a 1-DoF parallel gripper. For visual perception, we employ a multi-camera configuration: a RealSense D455 depth camera serves as the head-mounted _Eye-on-Base_ sensor 


Fig. 3. Generalization of 3D spatial grounding across unseen scenarios. Pose-VLA exhibits robust generalization across various unseen settings, ranging from indoor tabletop layouts to complex robotic manipulation workspaces, providing more precise geometric localization than baseline methods. 

TABLE II 

**COMPARISON ON THE ROBOTWIN 2.0 SIMULATION.** ALL MODELS ARE POST-TRAINED FOR 80K STEPS (BATCH SIZE=32) FOR FAIR COMPARISON, EXCEPT FOR THE POSEVLA(UPPERBOUND), WHICH IS TRAINED FOR 100K STEPS (BATCH SIZE=288, CHUNK SIZE=16). 

|**ManipulationTask**|_π_0 <br>|[5]<br>|_π_0_._5<br>|[6]<br>|PaliGem<br>|ma<br>expert<br>|Pose-VLA(<br>|w/o depth)<br>|PoseVLA(U<br>|pperbound)<br>|
|---|---|---|---|---|---|---|---|---|---|---|
||Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|_Adjust Bottle_|70%|57%|62%|69%|67%|47%|97%|77%|100%|92%|
|_Beat Block Hammer_|80%|73%|78%|93%|40%|37%|100%|87%|80%|68%|
|_Click Alarmclock_|83%|73%|92%|89%|80%|57%|83%|93%|98%|100%|
|_Dump Bin Bigbin_|100%|90%|89%|97%|73%|77%|97%|97%|98%|98%|
|_Grab Roller_|93%|97%|100%|100%|53%|57%|97%|100%|100%|100%|
|_Handover Block_|33%|40%|84%|57%|7%|17%|73%|80%|92%|86%|
|_Lift Pot_|63%|73%|100%|85%|37%|30%|100%|97%|100%|98%|
|_Move Pillbottle Pad_<br>|73%|67%|85%|61%|10%|20%|90%|87%|88%|90%|
|_...(50 tasks)_|...|...|...|...|...|...|...|...|...|...|
|_Open Laptop_|73%|70%|88%|96%|67%|70%|93%|93%|96%|96%|
|_Pick Dual Bottles_|47%|50%|21%|63%|10%|0%|87%|87%|98%|74%|
|_Place A2b Left_|60%|43%|84%|82%|27%|10%|90%|80%|100%|88%|
|_Place Cans Plasticbox_|83%|73%|90%|84%|23%|17%|97%|87%|100%|100%|
|_Place Container Plate_|93%|100%|89%|95%|90%|80%|97%|100%|100%|100%|
|_Place Dual Shoes_|63%|50%|93%|75%|3%|0%|87%|77%|92%|98%|
|_Place Object Scale_|70%|43%|82%|80%|10%|10%|67%|83%|90%|84%|
|_Place Phone Stand_|70%|57%|83%|81%|30%|20%|87%|87%|88%|94%|
|_Place Shoe_|87%|80%|96%|93%|23%|30%|100%|87%|98%|100%|
|**_Average (%)_**|67.00|65.12|79.48|76.16|35.40|33.36|79.91|79.10|**89.40**|**88.60**|


### TABLE III 

**SUCCESS RATES (%) ON LIBERO BENCHMARK. BOLD** AND <u>UNDERLINE</u> DENOTE THE **BEST** AND <u>SECOND BEST</u> RESULTS ACROSS FOUR SUITES AND THEIR **AVERAGE** . 

|**Method**|**Spatial**|**Object**|**Goal**|**Long**|**Avg**|
|---|---|---|---|---|---|
|OpenVLA [20]|84.7|88.4|79.2|53.7|76.5|
|SpatialVLA [38]|88.2|89.9|78.6|55.5|78.1|
|CoT-VLA [59]|87.5|91.6|87.6|69.0|83.9|
|WorldVLA [8]|87.6|96.2|83.4|60.0|79.1|
|GR00T-N1 [4]|94.4|97.6|93.0|90.6|93.9|
|_π_0 [5]|96.8|98.8|95.8|85.2|94.1|
|_π_0_._5 [6]|**98.8**|**98.2**|**98.0**|**92.4**|**96.8**|
|_π_0-FAST [36]|96.4|96.8|88.6|60.2|85.5|
|Pose-VLA(w/o depth)|96.5|98.0|97.1|**92.4**|96.0|


for global scene understanding, while a RealSense D405 depth camera is integrated as an _Eye-on-Hand_ sensor to provide 

## localized, high-resolution visual feedback. 

**Tasks and Evaluation.** To verify the generalizability of PoseVLA, we define four representative and challenging manipulation tasks as in Fig. 4: (1) _Stacking_ : stacking three nested bowls; (2) _Hanging_ : hanging a mug onto a designated peg on a wooden stand; (3) _Long-horizon Interaction_ : a complex multistage task involving opening a drawer, picking and placing a pen inside, and closing the drawer; (4) _Deformable Object Manipulation_ : folding a fabric towel. We collect an average of 100 demonstrations per task to facilitate embodiment alignment. Each model is evaluated over 20 trials per random seed, totaling 60 trials per task with diverse object placements. The success rate across these 60 trials is reported as the primary performance metric. 

**Results and Analysis.** As shown in Fig 5, Pose-VLA demonstrates superior manipulation capability with an average suc- 


Fig. 5. Success rate comparison of Pose-VLA and baseline models across four real-world manipulation tasks. Each model is evaluated over 60 trials per task, with success rates reported as percentages. Under the same demonstration scale, Pose-VLA consistently outperforms current vision-language-action baselines, especially in long-horizon and deformable object tasks. 

cess rate of 81 _._ 25%, significantly outperforming the vanilla PaliGemma (29 _._ 6%) and the strong baseline _π_ 0 _._ 5 (71 _._ 65%). Our method consistently outperforms or matches _π_ 0 _._ 5 across all tasks, notably achieving significant improvements in Task 2 (78 _._ 3% vs. 53 _._ 3%) and Task 3 (81 _._ 7% vs. 73 _._ 3%). Furthermore, the ablation study highlights the critical role of the depth modality; removing depth information leads to a marked performance decline, particularly in Task 3 where the success rate drops by 15 _._ 0 percentage points (from 81 _._ 7% to 66 _._ 7%). This substantial gap, alongside the 8 _._ 3% drop in Task 1 (from 88 _._ 3% to 80 _._ 0%), confirms that explicit 3D geometry is indispensable for precise spatial alignment and minimizing execution ambiguity. 

## _D. Ablation Study_ 

To verify how our 3D spatial pre-training and key design choices facilitate downstream performance, we conduct a series of ablation studies on both the 3D perception and RoboTwin 2.0 benchmarks. We systematically evaluate the impact of input modalities, pre-training objectives, architectural backbones, and action representations. 

**Ablation of Geometric Modalities.** We first investigate the contribution of each geometric modality on 3D grounding tasks, as shown in Table IV. On the SUN RGB-D benchmark, which contains complex indoor layouts, the integration of depth information provides a pivotal boost, increasing the AP15 from 39.0 ( _RGB Only_ ) to 45.1 ( _RGB+Depth_ ). In contrast, the performance gain on the Objectron dataset is less pronounced. We attribute this to the nature of the Objectron data, which primarily provides sparse and localized depth points centered around specific objects, offering limited additional geometric context compared to the dense depth maps in SUN RGB-D. Notably, the combination of Raymap and Depth ( _Full Model_ ) yields the best overall performance, confirming the synergy between explicit ray-based priors and metric depth. 

TABLE IV 

ABLATION STUDY OF GEOMETRIC MODALITIES ON 3D GROUNDING. 

|Configuration|SUN RGB-D [41]|Objectron [1]|
|---|---|---|
|RGB Only|39.0|86.4|
|RGB + Raymap|38.5|86.7|
|RGB + Depth|45.1|85.4|
|**Full Model**|**45.5**|**87.3**|


To thoroughly evaluate our design choices for robotic tasks, we perform two sets of ablation studies on the RoboTwin 2.0 benchmark. First, in Table V, we present an _incremental analysis_ to trace how each component, ranging from data scaling to action space optimization, contributes to the final performance of Pose-VLA. Second, in Table VI, we conduct an _orthogonal comparison_ to validate specific architectural choices, such as the VLM backbone and tokenization strategy, against prominent alternatives. Crucially, to eliminate confounding variables and ensure a strictly fair comparison, every evaluated variant is fine-tuned under a unified regime of 80K optimization steps with a batch size of 32, starting directly from its original pre-trained checkpoint. 

TABLE V 

**INCREMENTAL** ABLATION STUDY ON THE ROBOTWIN 2.0 BENCHMARK. GREEN AND RED DENOTE RELATIVE PERFORMANCE CHANGES FROM THE PRECEDING ROW. (80K STEPS, AND BATCH SIZE=32). 

|**Type**|**Improvements**|**Success **|**Rate (%)**|
|---|---|---|---|
|||**Easy**|**Hard**|
|Baseline|PaliGemma + Action-Expert|35.4|33.4|
|D|+ 3D Data|70.2 (+34.6)|69.1<br>(+35.7)|
|ata|+ 3D Data & Robotic Data|72.9 (+2.7)|72.0<br>(+2.9)|
|Action|Post-train: Joint _→_EE pose<br>Pre-train: Cam _→_Base|**79.9** (+7.0)<br>80.4 (+0.5)|**79.1**<br>(+7.1)<br>76.7<br>(-2.4)|


**Ablation of Pose Pre-training Data.** We evaluate our data scaling strategy and mixture compositions across both Table V and Table VI. As shown in the incremental analysis (Table V), incorporating diverse non-robotic 3D grounding data to the vanilla _PaliGemma_ baseline yields a substantial +35 _._ 7% boost in success rate. This confirms that pre-training on 3D spatial tasks establishes a more robust geometric foundation than conventional VQA-dominated pre-training. To further isolate 

the impact of these data sources, Table VI compares orthogonal data mixtures. Crucially, pre-training on robot data only severely degrades results, proving that generic 3D vision data is the key driver of our framework’s spatial capabilities. Conversely, relying solely on non-robotic 3D data ( _3D data only_ ) maintains highly competitive performance. Together, these results demonstrate that a strong grasp of 3D geometry constitutes the most significant contribution to success in our setting, effectively enhancing data efficiency by alleviating the reliance on costly, large-scale robotic demonstrations. **Ablation of Action Representation.** As shown in Table V, shifting the action space from joint angles to end-effector (EE) pose yields an average performance gain of over +7 _._ 0%. This improvement stems from the fact that our VLM is pre-trained to reason over 3D spatial poses; thus, adopting an EE pose interface allows the model to more directly leverage its learned geometric features. In contrast, joint-space control introduces a transformation overhead that degrades knowledge transfer. Conversely, we observe that predicting actions in the base frame leads to a performance drop ( _−_ 2 _._ 4%) in _RoboTwinHard_ scenarios. This indicates that camera-centric representations provide more robustness when facing significant visual variations in downstream policy transfer. 

TABLE VI 

**ORTHOGONAL** ABLATION STUDY ON THE ROBOTWIN 2.0 BENCHMARK. SR DENOTES SUCCESS RATE. (80K STEPS, AND BATCH SIZE=32). 

|**Dimension**|**Variant**|**Easy SR (%)**|**Hard SR (%)**|
|---|---|---|---|
|Backbone|Qwen3PI|57.7|55.3|
|Tokenization|Pose-VLA (OpenVLA binning)|68.5|65.9|
|Data Mixture|Pose-VLA (Robotic data only)<br>Pose-VLA (3D data only)|71.3<br>77.2|68.3<br>76.2|
|**Full Model**|**Pose-VLA**|**79.9**|**79.1**|


**Ablation of VLM Backbone.** To verify whether the performance gain of Pose-VLA stems from our specific pre-training rather than simply the scale of the VLM backbone, we evaluate a baseline using Qwen3-VL [39] (denoted as _Qwen3PI_ ). Although Qwen3-VL possesses state-of-the-art 3D grounding capabilities, Table VI shows that Qwen3PI, which undergoes only post-training, trails Pose-VLA by more than 20%, despite outperforming the scratch baseline. This gap confirms that even powerful VLMs lack robust 3D representations necessary for fine-grained manipulation without explicit pose-centric pre-training. Furthermore, our approach shows superior data efficiency under _tighter demonstration budgets_ . Remarkably, this advantage persists even when pre-training utilizes _solely non-robotic 3D data_ , validating pose tokens as a “universal interface” to transfer geometric knowledge to robotic policies. **Ablation of Tokenization.** We evaluate the structural advantages of our pose token representation by comparing it against standard methods, as reported in Table VI. Specifically, we contrast our approach with the uniform binning of delta actions used in OpenVLA [20]. OpenVLA’s tokenization is fundamentally limited in two ways: **1)** It relies on _local delta_ representations tied to specific robot kinematics, which inherently blocks the absorption of non-robotic data. In contrast, our 

_global spatial_ representation decouples actions from specific embodiments, serving as a “universal interface” that seamlessly integrates both robotic and non-robotic 3D trajectories. **2)** OpenVLA employs _uniform binning_ , which inefficiently utilizes token capacity. Our _non-uniform_ approach, detailed in the Appendix, allocates higher resolution at close proximities, yielding significantly higher precision for delicate, nearcontact manipulation. Consequently, reverting to OpenVLA’s standard tokenization results in strictly inferior performance, validating that our unique design is essential for both data scaling and precise 3D manipulation. 

## V. LIMITATIONS AND FUTURE WORK 

While _Pose-VLA_ provides a robust spatial foundation for robotic manipulation, its current scope presents promising avenues for future exploration. First, due to computational constraints, the full potential of large-scale 3D data scaling and high-efficiency 3D annotation for robotic videos remains partially unexplored. Furthermore, while our framework inherently supports deformable object manipulation during downstream adaptation, such as towel folding, the pre-training stage is currently driven by rigid-object datasets. Explicitly formulating deformable states, such as 3D keypoints or dense grasp annotations, into the pose token vocabulary during the large-scale pre-training phase represents a critical next step. Alongside this, extending these spatial priors from parallel-jaw grippers to multi-fingered dexterous hands will further unlock complex manipulation capabilities. Additionally, scaling our real-world experiments to a broader diversity of behaviors in unstructured environments remains a key objective. In particular, transitioning from static tabletop setups to mobile and egocentric manipulation presents an exciting frontier for future work. Finally, as our core focus in this work is maximizing spatial priors, we observe a natural trade-off regarding the backbone’s original semantic reasoning when facing complex semantic distractors. Exploring semantic-preserving training paradigms to maintain general reasoning capabilities without compromising 3D awareness offers a compelling direction for future research. 

## VI. CONCLUSION 

We present Pose-VLA, a framework utilizing a unified pose token as a universal interface to bridge spatial perception and robotic control. By integrating RGB-D data with camera intrinsics, our architecture instills an intrinsic 3D awareness that enables the learning of robust spatial and motion priors through large-scale pre-training. Pose-VLA achieves state-ofthe-art results in 3D grounding and provides a generalizable physical foundation for downstream robotic tasks, as validated across LIBERO, RoboTwin, and real-world experiments. Our work demonstrates a viable avenue for scaling VLA models by leveraging heterogeneous non-robotic 3D data alongside specialized robotic demonstrations. We advocate for a shift from VQA-based foundations toward pre-training embodiedaware VLMs, fostering the development of backbones that are inherently grounded in the physical world. 

REFERENCES 

- [1] Adel Ahmadyan, Liangkai Zhang, Artsiom Ablavatski, Jianing Wei, and Matthias Grundmann. Objectron: A large scale dataset of object-centric videos in the wild with pose annotations. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 7822–7831, 2021. 

- [2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- [3] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- [4] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- [5] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- [6] Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y Galliker, et al. _π_ 0 _._ 5: a vision-language-action model with openworld generalization. In _9th Annual Conference on Robot Learning_ , 2025. 

- [7] Garrick Brazil, Abhinav Kumar, Julian Straub, Nikhila Ravi, Justin Johnson, and Georgia Gkioxari. Omni3d: A large benchmark and model for 3d object detection in the wild. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 13154– 13164, 2023. 

- [8] Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- [9] Chilam Cheang, Haitao Lin, Yanwei Fu, and Xiangyang Xue. Learning 6-dof object poses to grasp category-level objects by language instructions. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 8476–8482. Ieee, 2022. 

- [10] Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data 

generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025. 

- [11] William Chen, Suneel Belkhale, Suvir Mirchandani, Oier Mees, Danny Driess, Karl Pertsch, and Sergey Levine. Training strategies for efficient embodied reasoning. _arXiv preprint arXiv:2505.08243_ , 2025. 

- [12] Jang Hyun Cho, Boris Ivanovic, Yulong Cao, Edward Schmerling, Yue Wang, Xinshuo Weng, Boyi Li, Yurong You, Philipp Kr¨ahenb¨uhl, Yan Wang, et al. Languageimage models with 3d understanding. _arXiv preprint arXiv:2405.03685_ , 2024. 

- [13] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 

- [14] Bowen Fu, Sek Kun Leong, Yan Di, Gu Wang, Jiwen Tang, Federico Tombari, and Xiangyang Ji. Lanpose: Language-instructed 6d object pose estimation for robotic assembly. In _European Conference on Computer Vision_ , pages 43–59. Springer, 2024. 

- [15] Ankit Goyal, Hugo Hadfield, Xuning Yang, Valts Blukis, and Fabio Ramos. Vla-0: Building state-of-the-art vlas with zero modification. _arXiv preprint arXiv:2510.13054_ , 2025. 

- [16] Dong Guo, Faming Wu, Feida Zhu, Fuxing Leng, Guang Shi, Haobin Chen, Haoqi Fan, Jian Wang, Jianyu Jiang, Jiawei Wang, et al. Seed1. 5-vl technical report. _arXiv preprint arXiv:2505.07062_ , 2025. 

- [17] Jingshun Huang, Haitao Lin, Tianyu Wang, Yanwei Fu, Xiangyang Xue, and Yi Zhu. Cap-net: A unified network for 6d pose and size estimation of categorical articulated parts from a single rgb-d image. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 11654–11664, 2025. 

- [18] Wonbong Jang, Philippe Weinzaepfel, Vincent Leroy, Lourdes Agapito, and Jerome Revaud. Pow3r: Empowering unconstrained 3d reconstruction with camera and scene priors. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1071–1081, 2025. 

- [19] Nikita Kachaev, Mikhail Kolosov, Daniil Zelezetsky, Alexey K Kovalev, and Aleksandr I Panov. Don’t blind your vla: Aligning visual representations for ood generalization. _arXiv preprint arXiv:2510.25616_ , 2025. 

- [20] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- [21] Jason Lee, Jiafei Duan, Haoquan Fang, Yuquan Deng, Shuo Liu, Boyang Li, Bohan Fang, Jieyu Zhang, Yi Ru Wang, Sangho Lee, et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 

- [22] Fuhao Li, Wenxuan Song, Han Zhao, Jingbo Wang, Pengxiang Ding, Donglin Wang, Long Zeng, and Haoang Li. Spatial forcing: Implicit spatial representation alignment for vision-language-action model. _arXiv preprint arXiv:2510.12276_ , 2025. 

- [23] Zhixuan Liang, Yizhuo Li, Tianshuo Yang, Chengyue Wu, Sitong Mao, Liuao Pei, Xiaokang Yang, Jiangmiao Pang, Yao Mu, and Ping Luo. Discrete diffusion vla: Bringing discrete diffusion to action decoding in vision-language-action policies. _arXiv preprint arXiv:2508.20072_ , 2025. 

- [24] Fanqi Lin, Ruiqian Nai, Yingdong Hu, Jiacheng You, Junming Zhao, and Yang Gao. Onetwovla: A unified vision-language-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 

- [25] Haitao Lin, Chilam Cheang, Yanwei Fu, and Xiangyang Xue. I know what you draw: Learning grasp detection conditioned on a few freehand sketches. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 8417–8423. Ieee, 2022. 

- [26] Haitao Lin, Zichang Liu, Chilam Cheang, Yanwei Fu, Guodong Guo, and Xiangyang Xue. Sar-net: Shape alignment and recovery network for category-level 6d object pose and size estimation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 6707–6717, 2022. 

- [27] Haitao Lin, Yanwei Fu, and Xiangyang Xue. Pourit!: Weakly-supervised liquid perception from a single image for visual closed-loop robotic pouring. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 241–251, 2023. 

- [28] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- [29] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [30] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-languageaction model. _arXiv preprint arXiv:2503.10631_ , 2025. 

- [31] Qiang Liu. Rectified flow: A marginal preserving approach to optimal transport. _arXiv preprint arXiv:2209.14577_ , 2022. 

- [32] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- [33] Wufei Ma, Yu-Cheng Chou, Qihao Liu, Xingrui Wang, Celso de Melo, Jianwen Xie, and Alan Yuille. Spatialreasoner: Towards explicit and generalizable 3d spatial reasoning. _arXiv preprint arXiv:2504.20024_ , 2025. 

- [34] Yunze Man, Shihao Wang, Guowen Zhang, Johan Bjorck, Zhiqi Li, Liang-Yan Gui, Jim Fan, Jan Kautz, Yu- 

Xiong Wang, and Zhiding Yu. Locateanything3d: Visionlanguage 3d detection with chain-of-sight. _arXiv preprint arXiv:2511.20648_ , 2025. 

- [35] Yongsen Mao, Junhao Zhong, Chuan Fang, Jia Zheng, Rui Tang, Hao Zhu, Ping Tan, and Zihan Zhou. Spatiallm: Training large language models for structured indoor modeling. _arXiv preprint arXiv:2506.07491_ , 2025. 

- [36] Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- [37] Delin Qu, Haoming Song, Qizhi Chen, Zhaoqing Chen, Xianqiang Gao, Xinyi Ye, Qi Lv, Modi Shi, Guanghui Ren, Cheng Ruan, et al. Eo-1: Interleaved visiontext-action pretraining for general robot control. _arXiv preprint arXiv:2508.21112_ , 2025. 

- [38] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- [39] Qwen Team. Qwen3-vl: A frontier multimodal large language model. https://github.com/QwenLM/Qwen3-VL, 2025. Accessed: 2026-01-22. 

- [40] Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptualcognitive memory in vision-language-action models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 

- [41] Shuran Song, Samuel P Lichtenberg, and Jianxiong Xiao. Sun rgb-d: A rgb-d scene understanding benchmark suite. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 567–576, 2015. 

- [42] Qi Sun, Pengfei Hong, Tej Deep Pala, Vernon Toh, U-Xuan Tan, Deepanway Ghosal, and Soujanya Poria. Emma-x: An embodied multimodal action model with grounded chain of thought and look-ahead spatial reasoning. In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 14199–14214, 2025. 

- [43] Qiang Sun, Haitao Lin, Ying Fu, Yanwei Fu, and Xiangyang Xue. Language guided robotic grasping with fine-grained instructions. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1319–1326. Ieee, 2023. 

- [44] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- [45] HY Team, Xumin Yu, Zuyan Liu, Ziyi Wang, He Zhang, Yongming Rao, Fangfu Liu, Yani Zhang, Ruowen Zhao, Oran Wang, et al. Hy-embodied-0.5: Embodied foun- 

dation models for real-world agents. _arXiv preprint arXiv:2604.07430_ , 2026. 

- [46] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- [47] Yating Wang, Haoyi Zhu, Mingyu Liu, Jiange Yang, HaoShu Fang, and Tong He. Vq-vla: Improving visionlanguage-action models via scaling vector-quantized action tokenizers. _arXiv preprint arXiv:2507.01016_ , 2025. 

- [48] Yuxin Wang, Lei Ke, Boqiang Zhang, Tianyuan Qu, Hanxun Yu, Zhenpeng Huang, Meng Yu, Dan Xu, and Dong Yu. N3d-vlm: Native 3d grounding enables accurate spatial reasoning in vision-language models. _arXiv preprint arXiv:2512.16561_ , 2025. 

- [49] Bowen Wen, Wenzhao Lian, Kostas Bekris, and Stefan Schaal. Catgrasp: Learning category-level task-relevant grasping in clutter from simulation. In _2022 International Conference on Robotics and Automation (ICRA)_ , pages 6401–6408. IEEE, 2022. 

- [50] Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 17868–17879, 2024. 

object pose estimation and tracking. In _European Conference on Computer Vision_ , pages 199–216. Springer, 2024. 

   - [58] Zhilong Zhang, Xiong-Hui Chen, Yidi Wang, Yihao Sun, Wenyu Luo, Haoxiang Ren, Haoxin Lin, and Yang Yu. On the representation degradation in vision-languageaction models. 

   - [59] Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chainof-thought reasoning for vision-language-action models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1702–1713, 2025. 

   - [60] Zhongyi Zhou, Yichen Zhu, Minjie Zhu, Junjie Wen, Ning Liu, Zhiyuan Xu, Weibin Meng, Yaxin Peng, Chaomin Shen, Feifei Feng, et al. Chatvla: Unified multimodal understanding and robot control with visionlanguage-action model. In _Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing_ , pages 5377–5395, 2025. 

   - [61] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

- [51] Runsen Xu, Zhiwei Huang, Tai Wang, Yilun Chen, Jiangmiao Pang, and Dahua Lin. Vlm-grounder: A vlm agent for zero-shot 3d visual grounding. _arXiv preprint arXiv:2410.13860_ , 2024. 

- [52] Rui Yang, Ziyu Zhu, Yanwei Li, Jingjia Huang, Shen Yan, Siyuan Zhou, Zhe Liu, Xiangtai Li, Shuangye Li, Wenqian Wang, et al. Visual spatial tuning. _arXiv preprint arXiv:2511.05491_ , 2025. 

- [53] Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 

- [54] Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 

- [55] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pretraining. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 11975–11986, 2023. 

- [56] Jianke Zhang, Xiaoyu Chen, Qiuyue Wang, Mingsheng Li, Yanjiang Guo, Yucheng Hu, Jiajun Zhang, Shuai Bai, Junyang Lin, and Jianyu Chen. Vlm4vla: Revisiting vision-language-models in vision-language-action models. _arXiv preprint arXiv:2601.03309_ , 2026. 

- [57] Jiyao Zhang, Weiyao Huang, Bo Peng, Mingdong Wu, Fei Hu, Zijian Chen, Bo Zhao, and Hao Dong. Omni6dpose: A benchmark and model for universal 6d 

APPENDIX 

This supplemental material is organized as follows: In Section A, we provide a detailed analysis of our distribution-aware pose discretization strategy and the initialization of the spatial tokens. Section B presents comprehensive success rates across all 50 tasks in the RoboTwin 2.0 benchmark, alongside an ablation study on action expert pre-training. In Section C, we investigate the latent representations via t-SNE visualizations to demonstrate the discriminability of Pose-VLA features. Finally, we showcase additional qualitative results and realworld robotic executions in the **accompanying video** . 

## _A. Distribution-Aware Pose Discretization_ 

To integrate spatial grounding into the VLM’s expanded vocabulary, we discretize continuous 6-DoF poses into a sequence of discrete tokens. A naive uniform discretization across the workspace often leads to a sub-optimal allocation of representational capacity, as it overlooks the heteroscedastic precision requirements inherent in robotic manipulation. Specifically, near-field interactions demand higher control resolution, whereas far-field movements are naturally more tolerant of spatial quantization errors. 

An analysis of our training statistics reveals a distinct distributional disparity between the horizontal ( _x, y_ ) and vertical ( _z_ ) axes, as illustrated in Fig. 6. Specifically, the _x_ and _y_ coordinates are densely concentrated around the origin. Conversely, the _z_ axis exhibits a highly skewed distribution, characterized by a positive offset and a extended right tail. 

To address this, we adopt a non-uniform discretization strategy. Specifically, we compute bin boundaries such that the bin width is inversely proportional to the data density, resulting in narrower bins within high-density regions and wider bins at the distribution tails. This ensures that the resulting pose tokens are utilized with approximately equal frequency across the training set, thereby maximizing the informational entropy of the discrete representation. Following this approach, we extend the PaliGemma vocabulary with specialized tokens <rot>, <trans_xy>, <trans_z>, and <size>, assigning _N_ = 2048 bins to each. While alternative quantization methods could potentially offer further refinements, they fall outside the primary scope of this work and are reserved for future exploration. 


Fig. 7. T-SNE visualization of VL features across 20 tasks in RoboTwin 2.0. Each point represents a feature vector at a specific timestep, with colors denoting different tasks. Our Pose-VLA exhibits clearer inter-task separation and tighter intra-task clusters compared to _π_ 0 and _π_ 0 _._ 5, effectively mitigating the representation collapse observed in baseline methods. 

## _B. Detailed Results on RoboTwin_ 

Table VII presents the individual success rates for all 50 tasks within the RoboTwin 2.0 [10] benchmark. Furthermore, we conduct an ablation study regarding the **pre-training of the action expert** to evaluate its impact on downstream performance. We compare our full model, Pose-VLA ( _π_ 0), which initializes the action expert from official _π_ 0 checkpoints, against Pose-VLA (scratch), where the action expert is trained from randomly initialized weights. The results indicate that while action pre-training provides benefits, the spatial pretraining on the VLM backbone contributes most significantly to the overall performance gains. 

## _C. T-SNE Visualization of VLM Features_ 

To further investigate the latent representations, we visualize the Vision-Language (VL) features from various VLA methods using t-SNE. As illustrated in Fig. 7, we compare the token embeddings of _PaliGemma-with-Expert_ , _π_ 0, _π_ 0 _._ 5, and our Pose-VLA. 

While _Pose-VLA_ maintains well-separated clusters for target tasks, _PaliGemma-with-Expert_ exhibits significant overlap across classes. This indicates that vanilla action fine-tuning often leads to representation collapse, where the model loses the ability to distinguish between diverse task semantics. In contrast, _Pose-VLA_ features demonstrate superior intertask discriminability and intra-task consistency, forming more compact and well-defined clusters that facilitate more robust policy learning. 

Fig. 6. Data statistics of object translation and size in datasets. Translations along the x and y axes show similar distributions, while the z-axis translation exhibits a notably different pattern. In contrast, object sizes are similarly distributed across all three axes. 

TABLE VII 

**COMPARISON OF OUR METHOD AND VLA MODELS ON ROBOTWIN 2.0 SIMULATION** 

|**ManipulationTask**|_π_|0<br>|_π_|0_._5<br>|PaliGem|ma<br>expert<br>|_Pose_|_-VLA_<br>|_Pose-V_|_LA (_**_π_**0_)_<br>|
|---|---|---|---|---|---|---|---|---|---|---|
||Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|Easy|Hard|
|_Adjust Bottle_|70%|57%|62%|69%|67%|47%|97%|77%|97%|90%|
|_Beat Block Hammer_|80%|73%|78%|93%|40%|37%|100%|87%|87%|87%|
|_Blocks Ranking Rgb_|80%|83%|86%|85%|47%|40%|83%|77%|83%|80%|
|_Blocks Ranking Size_|43%|60%|76%|26%|17%|3%|60%|73%|80%|60%|
|_Click Alarmclock_|83%|73%|92%|89%|80%|57%|83%|93%|87%|90%|
|_Click Bell_|67%|83%|98%|66%|57%|57%|87%|83%|97%|97%|
|_Dump Bin Bigbin_|100%|90%|89%|97%|73%|77%|97%|97%|97%|97%|
|_Grab Roller_|93%|97%|100%|100%|53%|57%|97%|100%|100%|100%|
|_Handover Block_|33%|40%|84%|57%|7%|17%|73%|80%|70%|60%|
|_Handover Mic_|90%|100%|92%|97%|83%|87%|93%|93%|100%|100%|
|_HangingMug_|20%|21%|22%|17%|7%|10%|27%|23%|13%|33%|
|<br>_Lift Pot_|63%|73%|100%|85%|37%|30%|100%|97%|93%|98%|
|_Move Can Pot_|57%|53%|72%|55%|23%|20%|63%|53%|60%|70%|
|_Move Pillbottle Pad_|73%|67%|85%|61%|10%|20%|90%|87%|93%|86%|
|_Move Playingcard Away_|80%|83%|96%|84%|33%|30%|87%|83%|100%|96%|
|_Move StaplerPad_|37%|50%|61%|42%|7%|10%|70%|53%|73%|72%|
|_Open Laptop_|73%|70%|88%|96%|67%|70%|93%|93%|93%|98%|
|_Open Microwave_|71%|83%|71%|77%|70%|83%|60%|63%|60%|82%|
|_Pick Diverse Bottles_|40%|53%|20%|71%|7%|3%|60%|77%|53%|50%|
|_Pick Dual Bottles_|47%|50%|21%|63%|10%|0%|87%|87%|77%|54%|
|_Place A2b Left_|60%|43%|84%|82%|27%|10%|90%|80%|93%|86%|
|_Place A2b Right_|30%|47%|83%|84%|13%|7%|77%|80%|80%|88%|
|_Place Bread Basket_|77%|47%|83%|64%|30%|17%|83%|73%|80%|70%|
|_PlaceBread Skillet_|63%|60%|86%|66%|3%|3%|93%|77%|77%|74%|
|_Place Burger Fries_|93%|93%|97%|87%|17%|27%|83%|83%|90%|82%|
|_Place Can Basket_|45%|40%|53%|62%|27%|23%|53%|70%|87%|72%|
|_Place Cans Plasticbox_|83%|73%|90%|84%|23%|17%|97%|87%|97%|90%|
|_Place Container Plate_|93%|100%|89%|95%|90%|80%|97%|100%|97%|98%|
|_Place Dual Shoes_|63%|50%|93%|75%|3%|0%|87%|77%|80%|82%|
|_Place Empty Cup_|100%|97%|96%|99%|67%|77%|100%|97%|100%|100%|
|_Place Fan_|57%|73%|87%|85%|13%|10%|77%|77%|83%|82%|
|_Place Mouse Pad_|43%|40%|63%|39%|13%|13%|43%|57%|73%|66%|
|_Place Object Basket_|60%|73%|60%|76%|20%|20%|77%|80%|90%|86%|
|_Place Object Scale_|70%|43%|82%|80%|10%|10%|67%|83%|77%|74%|
|_Place Object Stand_|70%|77%|90%|85%|27%|43%|83%|80%|87%|82%|
|_Place Phone Stand_|70%|57%|83%|81%|30%|20%|87%|87%|83%|84%|
|_Place Shoe_|87%|80%|96%|93%|23%|30%|100%|87%|97%|96%|
|_Press Stapler_|70%|80%|80%|83%|70%|67%|83%|83%|83%|84%|
|_Put Bottles Dustbin_|63%|83%|76%|79%|13%|13%|80%|81%|90%|84%|
|_Put Object Cabinet_|53%|43%|83%|79%|26%|7%|62%|63%|63%|71%|
|_Rotate Qrcode_|67%|60%|79%|87%|27%|23%|70%|70%|67%|76%|
|_Scan Object_|47%|23%|80%|65%|7%|3%|87%|90%|70%|62%|
|_Shake Bottle Horizontally_|100%|90%|100%|99%|87%|83%|100%|100%|100%|94%|
|_Shake Bottle_|97%|90%|97%|97%|70%|73%|100%|100%|100%|94%|
|_Stack Blocks Three_|50%|63%|82%|76%|11%|7%|47%|44%|77%|84%|
|_Stack Blocks Two_|80%|93%|100%|100%|27%|27%|93%|90%|97%|94%|
|_Stack Bowls Three_|77%|63%|77%|71%|39%|63%|69%|73%|60%|88%|
|_StackBowlsTwo_|93%|97%|93%|96%|83%|90%|93%|100%|87%|96%|
|<br>_Stamp Seal_|60%|53%|73%|55%|46%|23%|67%|73%|60%|70%|
|_Turn Switch_|27%|27%|57%|54%|33%|27%|43%|37%|26%|27%|
|**_Average (%)_**|67.00|65.12|79.48|76.16|35.40|33.36|79.91|79.10|**81.30**|**80.72**|


