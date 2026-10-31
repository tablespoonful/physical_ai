---
title: "Lift3D Policy: Lifting 2D Foundation Models for Robust 3D Robotic Manipulation"
date: "2025"
venue: "CVPR 2025"
url: https://openaccess.thecvf.com/content/CVPR2025/html/Jia_Lift3D_Policy_Lifting_2D_Foundation_Models_for_Robust_3D_Robotic_CVPR_2025_paper.html
pdf: https://openaccess.thecvf.com/content/CVPR2025/papers/Jia_Lift3D_Policy_Lifting_2D_Foundation_Models_for_Robust_3D_Robotic_CVPR_2025_paper.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://openaccess.thecvf.com/content/CVPR2025/papers/Jia_Lift3D_Policy_Lifting_2D_Foundation_Models_for_Robust_3D_Robotic_CVPR_2025_paper.pdf)** / [論文ページ](https://openaccess.thecvf.com/content/CVPR2025/html/Jia_Lift3D_Policy_Lifting_2D_Foundation_Models_for_Robust_3D_Robotic_CVPR_2025_paper.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Lift3D Policy: Lifting 2D Foundation Models for Robust 3D Robotic Manipulation** 

Yueru Jia<sup>1,2</sup><sup>_∗_</sup> , Jiaming Liu<sup>1</sup><sup>_∗,†_</sup> , Sixiang Chen<sup>1</sup><sup>_∗_</sup> , Chenyang Gu<sup>1</sup> , Zhilve Wang<sup>1</sup> , Longzan Luo<sup>1</sup> , Xiaoqi Li<sup>1</sup> , Pengwei Wang<sup>2</sup> , Zhongyuan Wang<sup>2</sup> , Renrui Zhang<sup>3</sup><sup>_†_</sup> , Shanghang Zhang<sup>1,2�</sup> 

- 1State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University;<sup>2</sup> Beijing Academy of Artificial Intelligence (BAAI);<sup>3</sup> CUHK **Project web page:** lift3d-web.github.io 


Figure 1. **Lift3D empowers 2D foundation models with 3D manipulation capabilities by refining implicit 3D robotic representations through task-related affordance masking and depth reconstruction, while enhancing explicit 3D robotic representations by leveraging the pretrained 2D positional embeddings to encode point cloud. Lift3D achieves robustness and surprising effectiveness in diverse simulation and real-world tasks.** 

## **Abstract** 

_3D geometric information is essential for manipulation tasks, as robots need to perceive the 3D environment, reason about spatial relationships, and interact with intricate spatial configurations. Recent research has increasingly focused on the explicit extraction of 3D features, while still facing challenges such as the lack of large-scale robotic 3D data and the potential loss of spatial geometry. To address these limitations, we propose the Lift3D framework, which progressively enhances 2D foundation models with implicit and explicit 3D robotic representations to construct a robust 3D manipulation policy. Specifically, we first design a task-aware masked autoencoder that masks task-relevant_ 

_affordance patches and reconstructs depth information, enhancing the 2D foundation model’s implicit 3D robotic representation. After self-supervised fine-tuning, we introduce a 2D model-lifting strategy that establishes a positional mapping between the input 3D points and the positional embeddings of the 2D model. Based on the mapping, Lift3D utilizes the 2D foundation model to directly encode point cloud data, leveraging large-scale pretrained knowledge to construct explicit 3D robotic representations while minimizing spatial information loss. In experiments, Lift3D consistently outperforms previous state-of-the-art methods across several simulation benchmarks and real-world scenarios._ 

> _∗_ : Equal contribution, _†_ : Project lead, �: Corresponding author. 

17347 

## **1. Introduction** 

A fundamental goal of vision-based manipulation policies is to understand the scene and predict corresponding 3D poses. Some existing methods utilize 2D images as input to directly predict 3D end-effector poses through reinforcement learning [1, 13, 21, 29, 44, 75] or imitation learning [6, 14, 18, 38, 41, 42, 84, 89]. While these approaches can effectively handle a range of manipulation tasks, they fall short of fully understanding the spatial relationships and 3D structures in the physical world [16, 19, 61, 62, 86]. In robotic manipulation, 3D geometric information is crucial for tackling complex tasks, as robots must perceive the 3D environment, reason about geometric relationships, and interact with intricate spatial configurations. 

Recent research has increasingly focused on the explicit extraction of 3D feature representations in robotic manipulation tasks, which can be categorized into two groups. **On one hand, some methods directly encode point cloud data** [9, 32, 43, 62, 67, 78, 83], either training 3D policy models from scratch or fine-tuning pretrained point cloud encoders(i.e., PointNet++ [52] and PointNext [53]). However, the limited availability of large-scale robotic 3D data and foundational models constrains their generalization capabilities. Additionally, processing 3D or voxel features incurs significant computational costs, hindering scalability and practicality in real-world applications. **On the other hand, some methods involve transforming modalities** , such as lifting pretrained 2D features into 3D space [22, 35, 61, 72] or projecting 3D point clouds into multi-view images for input into 2D pretrained models [23, 24, 70, 81]. Despite showing promising performance on several downstream manipulation tasks, these modality transformations inevitably lead to a loss of spatial information, hindering robots’ ability to understand 3D spatial relationships. Building on the challenges in the aforementioned 3D policies, we raise a question: “ _Can we develop a 3D policy model that integrates large-scale pretrained knowledge while incorporating complete 3D spatial data input?_ ” 

To address this question, we propose the Lift3D framework, which elevates transformer-based 2D foundation model (e.g., DINOV2 [50] or CLIP [55]) to construct robust 3D manipulation policy step by step. The key insight of Lift3D is first to enhance the implicit 3D robotic representation, followed by the explicit encoding of point cloud data for policy imitation learning. For implicit 3D robotic representation, we design a task-aware masked autoencoder (MAE) that processes 2D images and reconstructs 3D geometric information in a self-supervised manner, as shown in Figure 1 a). Specifically, we utilize large-scale unlabeled datasets from robotic manipulation [25, 49] and leverage a multimodal model (i.e., CLIP) to extract image attention maps based on task text descriptions. These attention maps are then back-projected onto the 2D input to guide the MAE 

masking strategy, focusing on task-related affordance regions. Reconstructing the depth of masked tokens enhances the 3D spatial awareness of the 2D foundation model, facilitating subsequent point cloud imitation learning. 

For explicit 3D robotic representation, we propose a 2D model-lifting strategy that directly leverages a 2D foundation model to encode 3D point cloud data, as shown in Figure 1 b). Specifically, inspired by the virtual camera setting in [23, 24], we first project the point cloud data onto multiple virtual planes. However, our projection process is not aimed at constructing the input for the policy model, but rather at establishing a positional correspondence between the input 3D points and the pretrained 2D positional embeddings (PEs) of each virtual plane. Guided by this positional mapping, the 2D foundation model can use its original PEs to encode the point cloud data, enabling the model to extract 3D features based on its large-scale pretrained knowledge. Unlike previous methods, Lift3D eliminates modality transformation during imitation learning, minimizing the loss of robotic spatial information, while reducing computational cost by directly leveraging the 2D foundation model for forward propagation. Through a two-stage training process, Lift3D enhances the 2D foundation model with robust 3D robotic manipulation capabilities by systematically improving both implicit and explicit 3D robotic representations. 

To comprehensively evaluate our proposed Lift3D, we conduct extensive experiments across three simulation benchmarks [31, 57, 76] and several real-world scenarios, including over 30 different gripper and dexterous hand manipulation tasks, as shown in Figure 1. We compare various baseline methods, such as robotic 2D representation methods [46, 48, 55], 3D representation methods [52, 53, 87], and 3D imitation learning policies [23, 24, 35]. Lift3D consistently outperforms other methods, even when utilizing the simplest MLP policy head and single-view point cloud, demonstrating the robustness of our model’s manipulation capabilities and its understanding of robotic 3D spatial awareness. For instance, Lift3D achieves improvements in the average success rates of 18.2% and 21.3% over previous state-of-the-art 3D policy methods [78] on the Meta-World and Adroit benchmarks, respectively. We also explore the model scalability across several complex tasks, gradually increasing the parameters of the 2D foundation model. In real-world experiments, Lift3D can learn novel manipulation skills with just 30 episodes per task. To evaluate the generalization capabilities of Lift3D, we incorporate different manipulated instances, background scenes, and lighting conditions from the training set into the real-world testing process. Lift3D shows strong generalization abilities, effectively leveraging the large-scale pretrained knowledge of the 2D foundation model and comprehensive 3D robotic representations. In summary, our contributions are as follows: 

• We propose Lift3D, which elevates 2D foundation models 

17348 

to construct a 3D manipulation policy by systematically improving implicit and explicit 3D robotic representations. 

- For implicit 3D robotic representation, we design a taskaware MAE that masks task-related affordance regions and reconstructs the depth geometric information, enhancing the 3D spatial awareness of the 2D foundation model. 

- For explicit 3D robotic representation, we propose a 2D model-lifting strategy that leverages the pretrained PEs of a 2D foundation model to encode 3D point cloud data for manipulation imitation learning. 

## **2. Related work** 

**Robotic Representation Learning** In recent years, substantial progress has been made in the field of pretrained visual representations, with a primary focus on self-supervised learning paradigms such as contrastive learning [11, 12, 26, 50], self-distillation [5, 7, 8], and masked autoencoders (MAE) [4, 17, 27, 68, 73]. Additionally, multi-modal alignment approaches [55, 80] leverage large-scale paired imagelanguage data to learn more semantically-aware representations. Building on the above research, more studies are dedicated to enhancing 2D representations in the field of robotics. Specifically, R3M [48] leverages contrastive learning to learn a universal embodied representation from diverse human video data. Vip [45] generates dense, smooth reward functions for unseen robotic tasks. MVP [56], VC-1 [46], and Voltron [34] delve into the effectiveness of the MAE strategy in robotic pretraining. [74, 79] consider the impact of multiple frames on the current state. However, 2D representations often struggle to capture the spatial context needed for complex robotic tasks, prompting other pretraining work to explore 3D robotic representations. MV-MWM [59], 3D-MVP [54], and SPA [87] leverage multi-view MAE to learn 3D visual representation. SUGAR [10] and Point Cloud Matters [86] introduce point cloud-based 3D representations, showing that these observations often improve policy performance and generalization capabilities. DPR [71] leverages depth information as auxiliary knowledge for pretraining. Unlike previous robotic pretraining methods, Lift3D fully leverages existing 2D foundation models [50, 55] by enhancing them with implicit 3D robotic representations. This approach makes the first attempt to mask task-related affordance regions and reconstruct depth information, not only improving 3D spatial awareness but also facilitating subsequent point cloud imitation learning. **Robotic Manipulation.** Traditional robotic manipulation typically relies on state-based reinforcement learning [2, 20, 33, 75]. In contrast, recent approaches [14, 16, 47, 65, 69, 84, 85] utilize visual observations as input to inform predictions. Inspired by the success of Multimodal Large Language Models [3, 39], several Vision-Language-Action models [15, 30, 40–42, 89] are designed for task planning and manipulation. However, [86] demonstrates that explicit 

3D representation is essential for complex robotic tasks, offering strong robustness to variations. Another category of works focuses on directly encoding 3D information to predict end-effector poses [32, 43, 67, 78, 83]. Anygrasp [19] employs point cloud data to learn grasp poses on a largescale dataset. [23, 24, 70] project 3D point clouds into multi-view images for input into large-scale 2D pretrained models, while [22, 35, 61, 72] lift pretrained 2D features into 3D space. PolarNet [9] and M2T2 [77] directly utilize point clouds reconstructed from RGB-D data, processing them through an encoder-transformer combination for action prediction, while C2F-ARM [32] and PerAct [62] employ voxelized point clouds with a 3D backbone for action inference. Act3D [22] and ChainedDiffuser [72] take a different approach by representing scenes as multi-scale 3D features. Recently, 3D Diffusion Actor [36] and 3D Diffusion Policy [14] harness diffusion models to generate precise actions in 3D space. Unlike previous 3D policies, Lift3D directly encodes point cloud data using a pretrained 2D foundation model and its positional embeddings, minimizing spatial information loss and enhancing the generalization capability. 

## **3. Lift3D Method** 

In Section 3.1, we introduce the problem statement of our proposed Lift3D framework. In Sections 3.2 and 3.3, we detail the technical aspects of our Task-aware MAE and 2D Model-lifting Strategy, which enhance implicit and explicit 3D robotic representations, respectively 

### **3.1. Problem Statement** 

**For implicit 3D robotic representation** , following previous MAE methods [27, 56], we first input the masked image _I ∈_ R<sup>_W ×H×_3</sup> into the 2D foundation model 2 _De_ . The output features are then fed into a decoder 2 _Dd_ for depth reconstruction, _D_ = 2 _Dd_ (2 _De_ ( _I_ )), where _D ∈_ R<sup>_W ×H×_1</sup> . This process enhances the 3D spatial awareness of the 2 _De_ model and facilitates subsequent 3D imitation learning. **For explicit 3D robotic representation** , we directly utilize the 2D foundation model 2 _De_ to encode 3D point cloud data _P ∈_ R<sup>_N×_3</sup> and the robot state _RS_ . We then use a simple policy head _π_ to predict the action _a_ = _π_ (2 _De_ ( _P, RS_ )). Following previous manipulation works [22, 23], we adopt 7- DoF action to express the end-effector pose of the robot arm, which includes 3-DoF for translation, 3-DoF for rotation, and 1-DoF for the gripper state (open or closed). 

### **3.2. Task-aware Masked Autoencoder** 

Several studies [37, 46, 60] have shown that 2D foundation models exhibit strong representation and generalization capabilities across various downstream robotic tasks. Building on this, Lift3D first enhances the implicit 3D robotic representations within 2D foundation models. Existing robotic MAE reconstruction methods [46, 54, 56] employ an aggressive 

17349 


Figure 2. **Overall pipeline of Lift3D.** a) For implicit 3D robotic representation, we leverage CLIP [55] to offline extract image attention maps based on task descriptions, which are back-projected onto the 2D input to guide the MAE masking. We then input the visible tokens into the 2D foundation model to extract features. The masked tokens and encoded visible tokens are processed by the MAE decoder for depth reconstruction, enhancing 3D spatial awareness. Meanwhile, the encoded visible tokens are also distilled using corresponding features from the off-the-shelf pretrained model to mitigate catastrophic forgetting. b) For explicit 3D robotic representation, we first project the point cloud data onto multiple virtual planes, establishing a positional mapping between the 3D input points and the 2D positional embeddings (PEs) on each virtual plane. After mapping, we average the 2D PEs corresponding to each 3D patch to form a unified positional indicator(3D PEs), which is then integrated with the 3D tokens. These 3D tokens are generated by feeding the point cloud into a lightweight 3D tokenizer. Finally, the output features from the 2D foundation model are processed through a policy head to predict the pose for imitation learning. 

masking strategy, where a large portion of the input image patches is randomly masked. However, the masked patches may mostly contain irrelevant background information, hindering the effective learning of foreground object representations. Unlike previous methods, Lift3D aims to mask task-related affordance patches and reconstruct the depth geometric information, enhancing the 3D spatial awareness of the 2D foundation model. Specifically, we leverage largescale datasets from robotic manipulation [49] to construct our MAE training dataset, which includes 1 million training samples randomly sampled from videos, consisting of paired image and depth data. The additional details of the reconstruction dataset are shown in Appendix A. As shown in Figure 2 a), once the data is obtained, we use a multimodal model (i.e., CLIP) to generate image attention maps based on task-specific text descriptions. For instance, the text prompt used to extract the attention map in Figure 2 is ”Robot arm take the red bowl and put it in the grey bowl.” These attention maps are then bilinearly resized and backprojected onto the input image to guide the MAE masking strategy. To distinguish task-related affordance tokens from background tokens, we apply a threshold (i.e., _θ_ = 0 _._ 5) to filter the attention values of all tokens. Note that the attention value for each token is computed by averaging its pixel-level values. Consistent with the masking ratio used in previous methods [27], we also randomly mask background tokens to 

#### achieve the desired ratio (i.e., _r_ = 75 _._ 0%). 

The visible ( _x_ vis) tokens are fed into the 2D foundation model, then concatenated with the masked tokens ( _x_ mask), which are directed to a decoder for reconstruction. The reconstruction target plays a crucial role in masked image modeling, directly influencing the learning of feature representations. Previous robotic MAE methods typically use low-level RGB information [46, 54, 56] as the reconstruction target. To enhance the 3D spatial awareness of the 2D foundation model, we reconstruct depth information ( _D_ target) for task-related affordance patches and randomly selected background patches. Finally, to preserve the inherent capabilities of the foundation model, we introduce a distillation loss that constrains the distance between our model’s visible token outputs and the corresponding features from the offthe-shelf pretrained model (2 _De_<sup>pre).As shown in Figure 2</sup> a), during the stage 1 training process, we fine-tune the injected adapter [28] and decoder using reconstruction and distillation losses, which are formulated as: 


### **3.3. 2D Model-lifting Strategy** 

After endowing the 2D foundation model with implicit 3D robotic awareness, we introduce a lifting strategy that en- 

17350 

ables the 2D model to explicitly comprehend point cloud data. Recent works, whether projecting 3D point clouds into multi-view images [23, 70] or lifting 2D features into 3D space [22, 61], have faced the challenge of losing spatial information due to modality transformation. Therefore, efficiently encoding 3D data has been a key research focus in the 3D robotics field. For transformer-based 2D models, positional embeddings (PEs) play an important role, as they provide positional indicators for input tokens within the attention mechanism. However, directly creating new 3D PEs to encode 3D tokens could introduce semantic discrepancies between the pretrained 2D foundation model and the newly added 3D PEs, potentially causing a loss of large-scale pretrained knowledge. 

Therefore, inspired by [23, 24, 64], we project the 3D tokens onto multiple virtual planes. Unlike previous works, our projection process is not intended to construct the model’s input. Instead, it establishes a positional correspondence between the input 3D points and the pretrained 2D PEs of each virtual plane. These 2D PEs are then used to directly encode the 3D tokens. Specifically, as shown in Figure 2 b), we transform the raw point clouds into high-dimensional space (i.e., _B ×_ 128 _×_ 768), obtaining _k_ (128) 3D tokens through a lightweight 3D tokenizer, following previous methods [82, 88]. The 3D tokenizer consists of farthest point sampling [51] for downsampling the number of points, the k-Nearest Neighbor algorithm for local aggregation, and learnable linear layers for feature encoding. Additionally, we use _{C_ 3<sup>_i_</sup> _D_<sup>_}_</sup> _i_<sup>_k_</sup> =1<sup>to represent the 3D coordinates of each 3D</sup> token. Subsequently, each 3D coordinate are projected onto _n_ virtual planes, obtaining corresponding 3D-to-2D coordinates _{C_ 2<sup>_ij_</sup> _D_<sup>_}n_</sup> _j_ =1<sup>.The projection mechanism is parameter-</sup> free and efficient. We adopt a cube projection method with 6 faces, effectively capturing spatial information. The _n_ virtual planes correspond to _n_ original 2D PEs. Using the 3D-to-2D coordinates, we assign each 3D token to _n_ original 2D PEs, denoted as _{PE_ 2 _D_ ( _C_ 2<sup>_ij_</sup> _D_<sup>)</sup><sup>_}n_</sup> _j_ =1<sup>.</sup> After aligning each 3D token with _n_ 2D PEs, we simply average them to create a unified positional indicator, denoted as _PE_ 3 _D_ , which is formulated as: 


We incorporate _PE_ 3 _D_ with the 3D tokens and input them into the 2D foundation model. In this way, we utilize the _n_ combined original 2D PEs to encode the 3D tokens, which effectively provides diverse positional relations within 2D space and mitigates spatial information loss. The output features (i.e., _B ×_ 128 _×_ 768) from the 2D foundation model are processed through a simple policy head to predict the pose for imitation learning. We employ a three-layer multilayer perceptron (MLP) to construct the policy head. It is important to note that our Lift3D encoder can be easily 

adapted to different decoders or policy heads; the MLP head is used here for simple validation. Finally, the supervision loss is formulated as: 


Where T, R, and G represent translation, rotation, and gripper state in the 7-DoF end-effector pose, respectively. As shown in Figure 2 b), during stage 2 imitation learning, we freeze the parameters of the 2D foundation model and update only the 3D tokenizer, injected adapter, and policy head. Lift3D can also operate without injecting the adapter, resulting in a minor reduction in manipulation performance. The additional validations are shown in Appendix B. 

## **4. Experiments** 

In Sections 4.1 and 4.2, we evaluate the manipulation capability of our proposed Lift3D by presenting the experimental settings and results from both simulation and real-world tasks, respectively. The effectiveness of each component is validated through an ablation study in Section 4.3. The generalization capabilities of Lift3D are examined in Section 4.4, where we test the model on different manipulated instances, background scenes, and lighting conditions. In Section 4.5, we explore the model scalability by gradually increasing the parameters of the 2D foundation model. 

### **4.1. Simulation Experiment** 

**Benchmarks.** We select over 30 tasks from three widelyused manipulation simulation benchmarks: MetaWorld [76] and Adroit [57] in the MuJoCo simulator, and RLBench [31] in the CoppeliaSim simulator. The point cloud data is derived from single-view RGBD data using the camera extrinsics and intrinsics. For **MetaWorld** , a tabletop environment with a Sawyer arm and two-finger gripper, we select 15 tasks of varying difficulty levels [58]. These tasks, captured from two corner camera perspectives, are categorized as follows: easy tasks include _button-press_ , _drawer-open_ , _reach_ , _handlepull_ , _peg-unplug-side_ , _lever-pull_ , and _dial-turn_ ; medium tasks include _hammer_ , _sweep-into_ , _bin-picking_ , _push-wall_ , and _box-close_ ; hard and very hard tasks include _assembly_ , _hand-insert_ , and _shelf-place_ . For **Adroit** , which focuses on dexterous hand manipulation with the same camera view as in [46], we include three tasks: _hammer_ , _door_ , and _pen_ . For **RLBench** , which uses a Franka Panda robot and a front-view camera. Due to space constraints, the results and details of RLBench are provided in Appendix B. **Data collection.** Scripted policies are used in MetaWorld [76], where 25 demonstrations are collected, each consisting of 200 steps. For the Adroit tasks, trajectories are obtained from agents trained with reinforcement learning 

17351 

|Method|Type|Input Type|Easy (7)|Met<br>Medium(5)|aWorld<br>Hard(2)|VeryHard(1)|**Mean S.R.**|A<br>Hammer|droit<br>Door|Pen|**Mean S.R.**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|CLIP [55]||RGB|72.9|68.8|50.0|26.0|65.3|100|100|52|84.0|
|R3M [48]|2D Rep.|RGB|84.6|66.4|83.0|36.0|75.1|100|100|56|85.3|
|VC-1[46]||RGB|62.6|71.6|52.0|12.0|60.8|88|100|48|78.7|
|PointNet [51]||PC|72.0|37.6|66.0|14.0|55.9|60|100|48|69.3|
|PointNet++ [52]|3D R|PC|70.3|59.6|61.0|12.0|61.6|68|100|60|76.0|
|PointNeXt [53]|ep.|PC|82.6|62.8|59.0|20.0|68.7|52|96|48|65.3|
|SPA[87]||RGB|72.6|77.4|66.0|16.0|69.5|100|100|44|81.3|
|DP3[78]|3D Policy|PC|85.7|49.6|57.0|18.0|65.3|88|100|12|66.7|
|**Lift3D (DINOV2)**|O|PC|93.1|**82.4**|**88.0**|28.0|**84.5**|100|100|56|85.3|
|**Lift3D(CLIP)**|urs|PC|**94.0**|78.8|82.0|**42.0**|83.9|100|100|**64**|**88.0**|


Table 1. **Comparison of manipulation success rates between Lift3D and 2D & 3D baselines in simulation benchmarks.** ‘2D Rep.’ and ‘3D Rep.’ refer to robotic 2D representation and 3D representation methods, respectively. ‘PC’ indicates that the model input is point cloud. 

algorithms. Specifically, DAPG [57] is applied to the _door_ and _hammer_ tasks, while VRL3 [66] is used for the _pen_ task. We collect 100 demonstrations, each consisting of 100 steps. Demonstrations in RLBench are collected through pre-defined waypoints and the Open Motion Planning Library [63], with 100 episodes gathered, each containing several key frames. 

**Baselines.** The innovation of Lift3D lies in systematically enhancing both implicit and explicit 3D robotic representations. To evaluate its effectiveness, we compare Lift3D with 9 methods from three categories: **1) 2D Robotic Representation Methods.** We select CLIP (ViT-base) [55], which is a 2D foundation model. Additionally, R3M [48] and VC1 [46] are included, both of 2D robotic pretraining methods. **2) 3D Representation Methods.** Following [86], we incorporate foundational 3D models, including PointNet [51], PointNet++ [52], and PointNext [53]. Additionally, we examine SPA [87], the previous SOTA 3D robotic pretraining method. Following [46], all robotic representation methods use the same three-layer policy head and training loss as Lift3D. **3) 3D Policies.** Lift3D is compared with the previous SOTA 3D Diffusion Policy (DP3) [78] on MetaWorld and Adroit, and with RVT-2 [24] on RLBench. 

**Training and Evaluation Details.** For fair comparisons, all baselines are trained and evaluated under the same configuration, while 3D policy methods follow their original settings. The 2D and 3D visual inputs consist of 224 _×_ 224 RGB images and single-view point clouds with 1,024 points, respectively. The robot state includes end-effector pose, joint positions, and velocities, which are concatenated with the visual features. We use CLIP [55] and DINOV2 [50] (ViTbase) as our 2D foundation models. Following previous work [46], the Adam optimizer is employed with parameters ( _β_ 1 _, β_ 2) = (0 _._ 9 _,_ 0 _._ 999) and a learning rate of 1e-3. A constant learning rate is used for MetaWorld, while a cosine annealing scheduler with a 0.1 warm-up factor is applied for Adroit. Each method is trained for 100 epochs, with 25 rollouts performed every 10 epochs. We report the average success rate of the best-performing policy models across training. For MetaWorld, we further average the scores across the two camera views. 

**Quantitative Results.** In Table 1, Lift3D(CLIP) achieves an average success rate of 83.9 on the MetaWorld benchmark, with 78.8 accuracy on medium-level tasks and 82.0 accuracy on hard level tasks. Compared to other robotic representation methods, Lift3D improves the mean success rate by 8.8 over the top-performing 2D method and by 14.4 over the top-performing 3D method. In addition, compared to the previous SOTA 3D policy (DP3), Lift3D achieves an accuracy improvement of 18.6. These results demonstrate that Lift3D effectively enhances the 2D foundation model with robust manipulation capabilities, enabling a deeper understanding of robotic 3D scenes by leveraging large-scale pretrained knowledge. Furthermore, Lift3D also achieves superior performance on dexterous hand tasks compared to previous robotic representation and policy methods. Note that the DoF of the dexterous hand varies across tasks, with the _hammer_ , _door_ , and _pen_ tasks having 26, 28, and 24 DoF, respectively. The results demonstrate that our method is also effective for more complex dexterous hand manipulation tasks, owing to the strong 3D robotic representation. Lift3D(DINOV2) also shows promising results, demonstrating the method’s practicality for other 2D foundation models. The detailed scores are shown in Appendix B. 

### **4.2. Real-World Experiment** 

**Dataset collection.** In our real-world setup, we conduct experiments using a Franka Research 3 arm, with a static front view captured by an Intel RealSense L515 RGBD camera. We perform ten tasks: 1) _place bottle at rack_ , 2) _pour water_ , 3) _unplug charger_ , 4) _stack blocks_ , 5) _pick and place_ , 6) _slide block_ , 7) _water plants_ , 8) _wipe table_ , 9) _open drawer_ , and 10) _close drawer_ . These tasks involve various types of interacted objects and manipulation actions. For each task, 40 demonstrations are collected in diverse spatial positions, with trajectories recorded at 30 fps. We select 30 episodes and extract key frames to construct the training set for each task. Examples of input point cloud data and images are displayed in Figure 3. Additional details of the real-world dataset and assets are provided in Appendix A. **Training and Evaluation Details.** The implementation details are the same as in our simulation experiments. We train 

17352 

|Method|VC-1[46]|PointNet[51]|DP3[78]|Lift3D|
|---|---|---|---|---|
|Pick and Place|30|20|40|**85**|
|Place Bottle|30|40|50|**90**|
|Slide Block|20|30|50|**60**|
|Unplug Charger|25|20|45|**55**|
|Water Plants|10|10|20|**40**|
|Wipe Table|10|20|30|**40**|
|Pour Water|35|30|60|**85**|
|Stack Block|0|15|30|**35**|
|Open Drawer|10|30|**60**|**60**|
|Close Drawer|35|30|70|**75**|
|Mean Success Rate|20.5|24.5|45.5|**62.5**|


Table 2. **Quantitative results for real robot experiments.** The training setup is consistent with the real-world experiments described in the main text. For evaluation, we use the model from the final epoch and test it 20 times across diverse spatial positions. 

each method from scratch for each task. During the training process, point clouds and action poses in the world coordinate system are used as inputs and supervision, respectively. For evaluation, we use the model from the final epoch and evaluate it 20 times in diverse spatial positions. 

**Quantitative Results.** As shown in Table 2, we compare Lift3D(CLIP) with DP3 [78], VC-1 [46], and PointNet [51]. Among the 10 tasks, we include complex ones such as _wipe table_ , which requires manipulating deformable objects, and _place bottle at rack_ , which requires accurate 3D position and rotation predictions. The results show that Lift3D performs consistently well across multiple tasks. Lift3D achieves a success rate of 62.5%, which is a 17-point improvement over the state-of-the-art 3D policy, DP3, which achieves 45.5%. These results show that Lift3D effectively understands 3D scenes and predicts poses accurately in real-world settings. **Qualitative Results.** As shown in Figure 3, we visualize the manipulation process of six real-world tasks. Our method accurately predicts the continuous 7-DoF end-effector poses, allowing tasks to be completed along the trajectories. For example, in the _water plants_ task, Lift3D first accurately grasps the handle of the watering can. It then smoothly lifts the can and positions it above the plants. Finally, the gripper is gradually rotated to control the flow of “water”. The demonstration video is provided in the supplementary material, and failure cases are analyzed in Appendix C. 

### **4.3. Ablation Study** 

In Table 3, we conduct a series of ablation experiments on all 15 MetaWorld simulation tasks and compute the average manipulation accuracy. **For the Task-aware MAE** , in Ex2 - Ex4, we observe that Depth and RGB+Depth reconstruction outperform Ex1 with success rates of 6 and 5, respectively, while RGB reconstruction alone does not show a significant improvement. This highlights the importance of reconstructing geometric information in manipulation tasks, leading us to choose Depth as our reconstruction target. By comparing Ex2 and Ex5, we find that the affordance-guided masking strategy increases the success rate by 4 compared to the 

||T|ask-awar|e MAE||2D Model-|Lifting|||
|---|---|---|---|---|---|---|---|---|
||AMS|Depth|RGB|VD|2ML-PEs|L-PEs|**Mean**|**Gain**|
|Ex1|-|-|-|-|-|-|65.3|+0|
|Ex2|-|✓|-|-|-|-|68.1|+6|
|Ex3|-|-|✓|-|-|-|65.4|+1|
|Ex4|-|✓|✓|-|-|-|66.1|+5|
|Ex5|✓|✓|-|-|-|-|71.9|+10|
|Ex6|✓|✓|-|✓|-|-|76.5|+18|
|Ex7|-|-|-|-|✓|-|74.9|+14|
|Ex8|✓|✓|-|✓|✓|-|83.9|+34|
|Ex9|✓|✓|-|✓|-|✓|79.2|+28|


Table 3. **Ablation study.** In the Task-aware MAE, AMS refers to the affordance-guided masking strategy, Depth and RGB refer to the reconstruction targets, and VD stands for visual token distillation. In the 2D Model-Lifting, 2ML-PEs and L-PEs represent the pretrained 2D PEs constructed using our method and the newly injected learnable PEs, respectively. 


Table 4. **Generalization.** ‘Object’, ‘Background’, and ‘Brightness’ represent different manipulated objects, background scenes, and lighting conditions, respectively. The image above illustrates the three test scenarios, with the red box highlighting the main changes. 

random masking strategy, demonstrating that focusing on task-relevant affordance regions for learning geometric information is more efficient. Compared to Ex5, pretraining with visual token distillation (Ex6) results in an additional increase of 8, suggesting that preventing catastrophic forgetting of pretrained knowledge is essential when endowing 2D foundation models with implicit 3D robotic awareness. **For the 2D model-lifting strategy** , compared to Ex1 with image input, Ex7 introduces our lifting strategy with explicit point cloud encoding, which results in a significant improvement. The results demonstrate that 3D spatial information is crucial for achieving robust manipulation. Ex8 also shows a clear improvement over Ex7, verifying that our implicit 3D representation learning can facilitate subsequent explicit 3D imitation learning. Finally, compared to Ex8, Ex9 adopts the newly introduced PEs without pretraining and shows a 6 performance decrease, validating that our lifting strategy most effectively leverages large-scale 2D pretrained knowledge. In Appendix B, we explore the impact of the number and placement of virtual planes, PE integration methods, and the effect of parameter update strategies in imitation learning. 

17353 


Figure 3. The qualitative results of Lift3D in real-world experiments, including the input point cloud examples, manipulation progress, and the task completion end state, are shown. More visualizations can be found in Appendix C. 

### **4.4. Exploration of Generalization** 

Leveraging the large-scale pretrained knowledge of the 2D foundation model and comprehensive 3D robotic representations, Lift3D exhibits strong real-world generalization. As shown in Table 4, we design three real-world test scenarios, different from the training scenarios, to validate its generalization ability. **1) Different manipulated instances.** Lift3D demonstrates robustness across various manipulated objects, achieving the smallest accuracy loss. This success can primarily be attributed to the semantic understanding capabilities of the pretrained 2D foundation models. **2) Complex background scenes.** Background distractions significantly reduce accuracy across all methods, but Lift3D shows the smallest drop, maintaining a manipulation success rate above 50. This can be attributed to the effective use of largescale pretrained knowledge in 3D space. Additionally, the affordance-guided masking strategy enhances the model’s understanding of the spatial geometry of the foreground region through reconstruction, while minimizing the impact of background distractions. **3) Different lighting conditions.** Lighting variations affect the data distribution of 2D images and also impact depth capture, thereby influencing the point cloud data. Under the effect of lighting changes, Lift3D shows only an average accuracy drop of 20%, demonstrating its robust 3D robotic representation. 

### **4.5. Exploration of Model Scalability** 

In computer vision, 2D foundation models typically enhance performance on downstream tasks as their parameters scale up [50, 55]. Building on this, we investigate whether our proposed Lift3D policy also exhibits scalability. We conduct experiments on the very hard MetaWorld simulation task: _shelf-place_ . For this complex task, Lift3D (DINOV2-ViTbase) achieves only 28 accuracy. The parameter count of ViT-base is only 86M, while ViT-large and ViT-giant have 304M and 1B parameters, respectively. By substituting the 2D foundation model with DINOV2-ViT-large and DINOV2ViT-giant, Lift3D achieves 58 and 68 accuracy on the _shelfplace_ task and demonstrates faster convergence, as shown 


Figure 4. **Scalability.** Y-axis is the manipulation success rate. 

in Figure 4. Moreover, Lift3D exhibits better scalability than the original DINOv2 models by leveraging its robotic 3D representation to enhance the understanding of object geometry during interactions.These improvements demonstrate Lift3D’s scalability, enabling it to generate more robust manipulation policies with larger 2D foundation models. 

## **5. Conclusion and Limitation** 

In this paper, we introduce Lift3D, a novel framework that integrates large-scale pretrained 2D foundation models with robust 3D manipulation capabilities. First, we design a taskaware MAE that masks task-relevant affordance regions and reconstructs depth geometric information, enhancing implicit 3D robotic representation. Second, we propose a 2D model-lifting strategy that utilizes the pretrained 2D foundation model to explicitly encode 3D point cloud data for manipulation imitation learning. Lift3D consistently outperforms existing methods in both simulation and real-world experiments, showing strong generalization ability in diverse real-world scenarios. In terms of limitations, our Lift3D framework focuses on lifting 2D vision models to 3D manipulation tasks, which means it cannot comprehend language conditions. However, our approach can adapt to multimodal models like CLIP, enabling the integration of the Lift3D encoder with a language model and paving the way for a new 3D Vision-Language-Action model. 

17354 

## **6. Acknowledgements** 

This work was supported by the National Natural Science Foundation of China (62476011). We gratefully acknowledge Chenyang Gu for his assistance with the real-robot experiments. 

## **References** 

- [1] Boshi An, Yiran Geng, Kai Chen, Xiaoqi Li, Qi Dou, and Hao Dong. Rgbmanip: Monocular image-based robotic manipulation through active object pose estimation. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7748–7755. IEEE, 2024. 2 

- [2] OpenAI: Marcin Andrychowicz, Bowen Baker, Maciek Chociej, Rafal Jozefowicz, Bob McGrew, Jakub Pachocki, Arthur Petron, Matthias Plappert, Glenn Powell, Alex Ray, et al. Learning dexterous in-hand manipulation. _The International Journal of Robotics Research_ , 39(1):3–20, 2020. 3 

- [3] Anas Awadalla, Irena Gao, Josh Gardner, Jack Hessel, Yusuf Hanafy, Wanrong Zhu, Kalyani Marathe, Yonatan Bitton, Samir Gadre, Shiori Sagawa, et al. Openflamingo: An opensource framework for training large autoregressive visionlanguage models. _arXiv preprint arXiv:2308.01390_ , 2023. 

   - 3 

- [4] Roman Bachmann, David Mizrahi, Andrei Atanov, and Amir Zamir. Multimae: Multi-modal multi-task masked autoencoders. In _European Conference on Computer Vision_ , pages 348–367. Springer, 2022. 3 

- [5] Alexei Baevski, Wei-Ning Hsu, Qiantong Xu, Arun Babu, Jiatao Gu, and Michael Auli. Data2vec: A general framework for self-supervised learning in speech, vision and language. In _International Conference on Machine Learning_ , pages 1298–1312. PMLR, 2022. 3 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2 

- [7] Jiajun Cao, Yuan Zhang, Tao Huang, Ming Lu, Qizhe Zhang, Ruichuan An, Ningning Ma, and Shanghang Zhang. Movekd: Knowledge distillation for vlms with mixture of visual encoders. _arXiv preprint arXiv:2501.01709_ , 2025. 3 

- [8] Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and Armand Joulin. Unsupervised learning of visual features by contrasting cluster assignments. _Advances in neural information processing systems_ , 33:9912– 9924, 2020. 3 

- [9] Shizhe Chen, Ricardo Garcia, Cordelia Schmid, and Ivan Laptev. Polarnet: 3d point clouds for language-guided robotic manipulation. _arXiv preprint arXiv:2309.15596_ , 2023. 2, 3 

- [10] Shizhe Chen, Ricardo Garcia, Ivan Laptev, and Cordelia Schmid. Sugar: Pre-training 3d visual representations for robotics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18049– 18060, 2024. 3 

- [11] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. A simple framework for contrastive learning of visual representations. In _International conference on machine learning_ , pages 1597–1607. PMLR, 2020. 3 

- [12] Xinlei Chen, Saining Xie, and Kaiming He. An empirical study of training self-supervised vision transformers. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 9640–9649, 2021. 3 

- [13] Yuanpei Chen, Tianhao Wu, Shengjie Wang, Xidong Feng, Jiechuan Jiang, Zongqing Lu, Stephen McAleer, Hao Dong, Song-Chun Zhu, and Yaodong Yang. Towards human-level bimanual dexterous manipulation with reinforcement learning. _Advances in Neural Information Processing Systems_ , 35:5150– 5163, 2022. 2 

- [14] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 2, 3 

- [15] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 3 

- [16] Ben Eisner, Harry Zhang, and David Held. Flowbot3d: Learning 3d articulation flow to manipulate articulated objects. _arXiv preprint arXiv:2205.04382_ , 2022. 2, 3 

- [17] David Fan, Jue Wang, Shuai Liao, Zhikang Zhang, Vimal Bhat, and Xinyu Li. Text-guided video masked autoencoder. _arXiv preprint arXiv:2408.00759_ , 2024. 3 

- [18] Bin Fang, Shidong Jia, Di Guo, Muhua Xu, Shuhuan Wen, and Fuchun Sun. Survey of imitation learning for robotic manipulation. _International Journal of Intelligent Robotics and Applications_ , 3:362–369, 2019. 2 

- [19] Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, and Cewu Lu. Anygrasp: Robust and efficient grasp perception in spatial and temporal domains. _IEEE Transactions on Robotics_ , 2023. 2, 3 

- [20] Yiran Geng, Boshi An, Haoran Geng, Yuanpei Chen, Yaodong Yang, and Hao Dong. End-to-end affordance learning for robotic manipulation. In _International Conference on Robotics and Automation (ICRA)_ , 2023. 3 

- [21] Yiran Geng, Boshi An, Haoran Geng, Yuanpei Chen, Yaodong Yang, and Hao Dong. Rlafford: End-to-end affordance learning for robotic manipulation. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5880– 5886. IEEE, 2023. 2 

- [22] Theophile Gervet, Zhou Xian, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Act3d: 3d feature field transformers for multi-task robotic manipulation. In _7th Annual Conference on Robot Learning_ , 2023. 2, 3, 5 

- [23] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In _Conference on Robot Learning_ , pages 694– 710. PMLR, 2023. 2, 3, 5 

- [24] Ankit Goyal, Valts Blukis, Jie Xu, Yijie Guo, Yu-Wei Chao, and Dieter Fox. Rvt-2: Learning precise manipulation from 

17355 

few demonstrations. _arXiv preprint arXiv:2406.08545_ , 2024. 

2, 3, 5, 6 

- [25] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18995–19012, 2022. 2 

- [26] Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick. Momentum contrast for unsupervised visual representation learning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9729–9738, 2020. 3 

- [27] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollar, and Ross Girshick.´ Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 16000– 16009, 2022. 3, 4 

- [28] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 4 

- [29] Hengyuan Hu, Suvir Mirchandani, and Dorsa Sadigh. Imitation bootstrapped reinforcement learning. _arXiv preprint arXiv:2311.02198_ , 2023. 2 

- [30] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. _arXiv preprint arXiv:2307.05973_ , 2023. 3 

- [31] Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 2, 5 

- [32] Stephen James, Kentaro Wada, Tristan Laidlow, and Andrew J Davison. Coarse-to-fine q-attention: Efficient learning for visual robotic manipulation via discretisation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13739–13748, 2022. 2, 3 

- [33] Shirin Joshi, Sulabh Kumra, and Ferat Sahin. Robotic grasping using deep reinforcement learning. In _2020 IEEE 16th International Conference on Automation Science and Engineering (CASE)_ , pages 1461–1466. IEEE, 2020. 3 

- [34] Siddharth Karamcheti, Suraj Nair, Annie S Chen, Thomas Kollar, Chelsea Finn, Dorsa Sadigh, and Percy Liang. Language-driven representation learning for robotics. _arXiv preprint arXiv:2302.12766_ , 2023. 3 

- [35] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. 3d diffuser actor: Policy diffusion with 3d scene representations. _arXiv preprint arXiv:2402.10885_ , 2024. 2, 3 

- [36] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. 3d diffuser actor: Policy diffusion with 3d scene representations, 2024. 3 

- [37] Apoorv Khandelwal, Luca Weihs, Roozbeh Mottaghi, and Aniruddha Kembhavi. Simple but effective: Clip embeddings for embodied ai. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14829– 14838, 2022. 3 

- [38] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2 

- [39] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP2: Bootstrapping language-image pre-training with frozen image encoders and large language models, 2023. 3 

- [40] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 3 

- [41] Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for object-centric robotic manipulation. _arXiv preprint arXiv:2312.16217_ , 2023. 2 

- [42] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv preprint arXiv:2406.04339_ , 2024. 2, 3 

- [43] Minghua Liu, Xuanlin Li, Zhan Ling, Yangyan Li, and Hao Su. Frame mining: a free lunch for learning robotic manipulation from 3d point clouds. _arXiv preprint arXiv:2210.07442_ , 2022. 2, 3 

- [44] Andrew Lobbezoo, Yanjun Qian, and Hyock-Ju Kwon. Reinforcement learning for pick and place operations in robotics: A survey. _Robotics_ , 10(3):105, 2021. 2 

- [45] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. _arXiv preprint arXiv:2210.00030_ , 2022. 3 

- [46] Arjun Majumdar, Karmesh Yadav, Sergio Arnaud, Jason Ma, Claire Chen, Sneha Silwal, Aryan Jain, Vincent-Pierre Berges, Tingfan Wu, Jay Vakil, et al. Where are we in the search for an artificial visual cortex for embodied intelligence? _Advances in Neural Information Processing Systems_ , 36:655–677, 2023. 2, 3, 4, 5, 6, 7 

- [47] Kaichun Mo, Leonidas J Guibas, Mustafa Mukadam, Abhinav Gupta, and Shubham Tulsiani. Where2act: From pixels to actions for articulated 3d objects. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 6813–6823, 2021. 3 

- [48] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 2, 3, 6 

- [49] Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, et al. Open x-embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 2, 4 

- [50] Maxime Oquab, Timothee Darcet, Th´ eo Moutakanni, Huy Vo,´ Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: 

17356 

Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 2, 3, 6, 8 

- [51] Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 652–660, 2017. 5, 6, 7 

- [52] Charles Ruizhongtai Qi, Li Yi, Hao Su, and Leonidas J Guibas. Pointnet++: Deep hierarchical feature learning on point sets in a metric space. _Advances in neural information processing systems_ , 30, 2017. 2, 6 

- [53] Guocheng Qian, Yuchen Li, Houwen Peng, Jinjie Mai, Hasan Hammoud, Mohamed Elhoseiny, and Bernard Ghanem. Pointnext: Revisiting pointnet++ with improved training and scaling strategies. _Advances in neural information processing systems_ , 35:23192–23204, 2022. 2, 6 

- [54] Shengyi Qian, Kaichun Mo, Valts Blukis, David F Fouhey, Dieter Fox, and Ankit Goyal. 3d-mvp: 3d multiview pretraining for robotic manipulation. _arXiv preprint arXiv:2406.18158_ , 2024. 3, 4 

- [55] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 2, 3, 4, 6, 8 

- [56] Ilija Radosavovic, Tete Xiao, Stephen James, Pieter Abbeel, Jitendra Malik, and Trevor Darrell. Real-world robot learning with masked visual pre-training. In _Conference on Robot Learning_ , pages 416–426. PMLR, 2023. 3, 4 

- [57] Aravind Rajeswaran, Vikash Kumar, Abhishek Gupta, Giulia Vezzani, John Schulman, Emanuel Todorov, and Sergey Levine. Learning complex dexterous manipulation with deep reinforcement learning and demonstrations. _arXiv preprint arXiv:1709.10087_ , 2017. 2, 5, 6 

- [58] Younggyo Seo, Danijar Hafner, Hao Liu, Fangchen Liu, Stephen James, Kimin Lee, and Pieter Abbeel. Masked world models for visual control. In _Conference on Robot Learning_ , pages 1332–1344. PMLR, 2023. 5 

- [59] Younggyo Seo, Junsu Kim, Stephen James, Kimin Lee, Jinwoo Shin, and Pieter Abbeel. Multi-view masked world models for visual robotic manipulation. In _International Conference on Machine Learning_ , pages 30613–30632. PMLR, 2023. 3 

- [60] Jinghuan Shang, Karl Schmeckpeper, Brandon B May, Maria Vittoria Minniti, Tarik Kelestemur, David Watkins, and Laura Herlant. Theia: Distilling diverse vision foundation models for robot learning. _arXiv preprint arXiv:2407.20179_ , 2024. 3 

- [61] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. In _Conference on robot learning_ , pages 894–906. PMLR, 2022. 2, 3, 5 

- [62] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pages 785–799. PMLR, 2023. 2, 3 

- [63] Ioan A Sucan, Mark Moll, and Lydia E Kavraki. The open motion planning library. _IEEE Robotics & Automation Magazine_ , 19(4):72–82, 2012. 6 

- [64] Yiwen Tang, Ray Zhang, Jiaming Liu, Zoey Guo, Bin Zhao, Zhigang Wang, Peng Gao, Hongsheng Li, Dong Wang, and Xuelong Li. Any2point: Empowering any-modality large models for efficient 3d understanding. In _European Conference on Computer Vision_ , pages 456–473. Springer, 2025. 

5 

- [65] Weikang Wan, Haoran Geng, Yun Liu, Zikang Shan, Yaodong Yang, Li Yi, and He Wang. Unidexgrasp++: Improving dexterous grasping policy learning via geometry-aware curriculum and iterative generalist-specialist learning. _arXiv preprint arXiv:2304.00464_ , 2023. 3 

- [66] Che Wang, Xufang Luo, Keith Ross, and Dongsheng Li. Vrl3: A data-driven framework for visual deep reinforcement learning. _Advances in Neural Information Processing Systems_ , 35: 32974–32988, 2022. 6 

- [67] Chenxi Wang, Hongjie Fang, Hao-Shu Fang, and Cewu Lu. Rise: 3d perception makes real-world robot imitation simple and effective. _arXiv preprint arXiv:2404.12281_ , 2024. 2, 3 

- [68] Limin Wang, Bingkun Huang, Zhiyu Zhao, Zhan Tong, Yinan He, Yi Wang, Yali Wang, and Yu Qiao. Videomae v2: Scaling video masked autoencoders with dual masking. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 14549–14560, 2023. 3 

- [69] Qianxu Wang, Haotong Zhang, Congyue Deng, Yang You, Hao Dong, Yixin Zhu, and Leonidas Guibas. Sparsedff: Sparse-view feature distillation for one-shot dexterous manipulation. _arXiv preprint arXiv:2310.16838_ , 2023. 3 

- [70] Weiyao Wang, Yutian Lei, Shiyu Jin, Gregory D Hager, and Liangjun Zhang. Vihe: Virtual in-hand eye transformer for 3d robotic manipulation. _arXiv preprint arXiv:2403.11461_ , 2024. 2, 3, 5 

- [71] Wanying Wang, Jinming Li, Yichen Zhu, Zhiyuan Xu, Zhengping Che, Yaxin Peng, Chaomin Shen, Dong Liu, Feifei Feng, and Jian Tang. Visual robotic manipulation with depth-aware pretraining. _arXiv preprint arXiv:2401.09038_ , 2024. 3 

- [72] Zhou Xian, Nikolaos Gkanatsios, Theophile Gervet, TsungWei Ke, and Katerina Fragkiadaki. Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In _7th Annual Conference on Robot Learning_ , 2023. 2, 3 

- [73] Zhenda Xie, Zheng Zhang, Yue Cao, Yutong Lin, Jianmin Bao, Zhuliang Yao, Qi Dai, and Han Hu. Simmim: A simple framework for masked image modeling. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9653–9663, 2022. 3 

- [74] Jiange Yang, Bei Liu, Jianlong Fu, Bocheng Pan, Gangshan Wu, and Limin Wang. Spatiotemporal predictive pre-training for robotic motor control. _arXiv preprint arXiv:2403.05304_ , 2024. 3 

- [75] Denis Yarats, Rob Fergus, Alessandro Lazaric, and Lerrel Pinto. Mastering visual continuous control: Improved data-augmented reinforcement learning. _arXiv preprint arXiv:2107.09645_ , 2021. 2, 3 

- [76] Tianhe Yu, Deirdre Quillen, Zhanpeng He, Ryan Julian, Karol Hausman, Chelsea Finn, and Sergey Levine. Meta-world: 

17357 

A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 2, 5 

web knowledge to robotic control. In _7th Annual Conference on Robot Learning_ , 2023. 2, 3 

- [77] Wentao Yuan, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. M2t2: Multi-task masked transformer for object-centric pick and place. _arXiv preprint arXiv:2311.00926_ , 2023. 3 

- [78] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation_ , 2024. 2, 3, 6, 7 

- [79] Jia Zeng, Qingwen Bu, Bangjun Wang, Wenke Xia, Li Chen, Hao Dong, Haoming Song, Dong Wang, Di Hu, Ping Luo, et al. Learning manipulation by predicting interaction. _arXiv preprint arXiv:2406.00439_ , 2024. 3 

- [80] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 11975–11986, 2023. 3 

- [81] Junjie Zhang, Chenjia Bai, Haoran He, Wenke Xia, Zhigang Wang, Bin Zhao, Xiu Li, and Xuelong Li. Sam-e: Leveraging visual foundation model with sequence imitation for embodied manipulation. _arXiv preprint arXiv:2405.19586_ , 2024. 2 

- [82] Renrui Zhang, Liuhui Wang, Yali Wang, Peng Gao, Hongsheng Li, and Jianbo Shi. Starting from non-parametric networks for 3d point cloud analysis. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 5344–5353, 2023. 5 

- [83] Tong Zhang, Yingdong Hu, Jiacheng You, and Yang Gao. Leveraging locality to boost sample efficiency in robotic manipulation. _arXiv preprint arXiv:2406.10615_ , 2024. 2, 3 

- [84] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with lowcost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 2, 3 

- [85] Enshen Zhou, Qi Su, Cheng Chi, Zhizheng Zhang, Zhongyuan Wang, Tiejun Huang, Lu Sheng, and He Wang. Code-as-monitor: Constraint-aware visual programming for reactive and proactive robotic failure detection, 2024. 3 

- [86] Haoyi Zhu, Yating Wang, Di Huang, Weicai Ye, Wanli Ouyang, and Tong He. Point cloud matters: Rethinking the impact of different observation spaces on robot learning. _arXiv preprint arXiv:2402.02500_ , 2024. 2, 3, 6 

- [87] Haoyi Zhu, Honghui Yang, Yating Wang, Jiange Yang, Limin Wang, and Tong He. Spa: 3d spatial-awareness enables effective embodied representation. _arXiv preprint arXiv:2410.08208_ , 2024. 2, 3, 6 

- [88] Xiangyang Zhu, Renrui Zhang, Bowei He, Ziyu Guo, Jiaming Liu, Han Xiao, Chaoyou Fu, Hao Dong, and Peng Gao. No time to train: Empowering non-parametric networks for fewshot 3d scene segmentation. _arXiv preprint arXiv:2404.04050_ , 2024. 5 

- [89] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer 

17358 

