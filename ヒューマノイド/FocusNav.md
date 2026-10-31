---
title: "FocusNav: Spatial Selective Attention with Waypoint Guidance for Humanoid Local Navigation"
date: "2026-01-19"
authors: "Yang Zhang; Jianming Ma; Liyun Yan; Zhanxiang Cao; Yazhou Zhang; Haoyang Li"
url: https://arxiv.org/abs/2601.12790
pdf: https://arxiv.org/pdf/2601.12790
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.12790)** / [論文ページ](https://arxiv.org/abs/2601.12790)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# FocusNav: Spatial Selective Attention with Waypoint Guidance for Humanoid Local Navigation 

Yang Zhang<sup>1,2</sup> , Jianming Ma<sup>1,2</sup> , Liyun Yan<sup>1,2</sup> , Zhanxiang Cao<sup>1,2</sup> , Yazhou Zhang<sup>1</sup> , Haoyang Li<sup>1,2</sup> , Yue Gao<sup>1,2</sup> 1Shanghai Jiao Tong University 2Shanghai Innovation Institute 

**_Abstract_ —Robust local navigation in unstructured and dynamic environments remains a significant challenge for humanoid robots, requiring a delicate balance between long-range navigation targets and immediate motion stability. In this paper, we propose FocusNav, a spatial selective attention framework that adaptively modulates the robot’s perceptual field based on navigational intent and real-time stability. FocusNav features a Waypoint-Guided Spatial Cross-Attention (WGSCA) mechanism that anchors environmental feature aggregation to a sequence of predicted collision-free waypoints, ensuring task-relevant perception along the planned trajectory. To enhance robustness in complex terrains, the Stability-Aware Selective Gating (SASG) module autonomously truncates distal information when detecting instability, compelling the policy to prioritize immediate foothold safety. Extensive experiments on the Unitree G1 humanoid robot demonstrate that FocusNav significantly improves navigation success rates in challenging scenarios, outperforming baselines in both collision avoidance and motion stability, achieving robust navigation in dynamic and complex environments.** 

## I. INTRODUCTION 

Humanoid robots, characterized by human-like bipedal locomotion systems and dexterous whole-body coordination [6, 38], possess the unique potential to unify locomotion and manipulation [41]. This potential enables them to exhibit human-like dynamic navigation and physical interaction within complex environments [11, 37]. However, their practical deployment remains strictly constrained by their mobile navigation capabilities [20], specifically the ability to traverse complex spaces adaptively and safely [1]. While existing methodologies have demonstrated reliable obstacle avoidance in controlled, flat environments with sparse obstacles [2], their navigational robustness remains fragile when transitioning to unstructured, rugged, and densely populated real-world settings [7]. In such sophisticated scenarios, robots must simultaneously manage dynamic obstacle avoidance and stable locomotion over uneven terrain, a dual challenge that current frameworks struggle to address effectively [12]. Consequently, enhancing robust mobile navigation for complex, dynamic, and unstructured environments is a core challenge and a critical bottleneck to fully unleashing the potential of humanoid robot applications [14]. 

To enhance the navigational capabilities of humanoid robots, researchers have explored various methodologies, including Large Language Model (LLM)-assisted navigation [45] and end-to-end Vision-Language Navigation (VLN) [3]. LLMassisted navigation leverages exceptional semantic understanding and logical reasoning to interpret task instructions and generate high-level plans, proving particularly effective for 


Fig. 1: Snapshots of dynamic obstacle avoidance on stairs. FocusNav anchors perception to navigational intent and adaptively maintains motion stability, significantly enhancing navigational performance in dynamic and complex scenarios. 

decision-making in large-scale, mapless environments [16]. Meanwhile, VLN aligns semantic and scene information through cross-modal models to achieve a direct mapping from natural language to real-time navigational actions, effectively mitigating the system latency and cumulative errors inherent in traditional modular approaches[44]. However, the scarcity of high-quality data constrains the scalable training of VLN at the level of fine-grained atomic joint actions [28]. Consequently, most contemporary VLN frameworks output either discrete directions or continuous velocity commands, relying on pre-designed low-level locomotion models for final execution [13]. This architectural decoupling obstructs the synergy between high-level perceptive planning and lowlevel motor control, hindering the exploration of globally optimal solutions [8]. Furthermore, locomotion models based on the velocity-command-tracking paradigm lack sufficient flexibility to support rapid velocity fluctuations and agile gait adjustments [23]. Such dual limitations prevent existing VLN methods from reconciling agile obstacle avoidance with robust traversal in dynamic, unstructured environments [35]. 

Drawing inspiration from the biological “cerebrumcerebellum” coordination mechanism [31], the cerebrum de- 

composes long-range navigation tasks into sequences of local waypoints through spatial reasoning, while the cerebellum coordinates whole-body movements via reflexive neural circuits to achieve local waypoint tracking [39]. Fig. 2 visualizes the operational mechanism of neural circuits in biological navigation, referred to as the Perception-Prediction-Attention (PPA) paradigm [27]. Specifically, once a local waypoint is determined, the system extracts feature information by observing the surrounding environment (Perception), pre-simulates potential trajectories in conjunction with target waypoints (Prediction), and dynamically and selectively focuses on critical environmental features along the heading direction (Attention) [25]. This paradigm enables low-latency responses for tasks such as terrain adaptation and dynamic obstacle avoidance, ultimately achieving robust local navigation [4]. 

In this work, we propose FocusNav, a spatial selective attention framework designed to enhance the locomotion stability and navigational efficiency of humanoid robots in complex environments. FocusNav employs a Waypoint-Guided Spatial Cross-Attention (WGSCA) mechanism that utilizes predicted collision-free waypoints to anchor the perception process, ensuring the model aggregates environmental features directly aligned with the intended motion trajectory. To further mitigate the risks posed by precarious terrains, we introduce a StabilityAware Selective Gating (SASG) module. This module dynamically modulates the robot’s perception field by truncating distal environmental information when the robot’s stability decreases, thereby forcing the policy to prioritize immediate foothold safety. We conduct extensive experiments on the Unitree G1 humanoid robot in a variety of challenging scenarios. The results demonstrate that FocusNav significantly outperforms baseline methods in navigation success rate, collision avoidance efficiency, and motion stability. 

In summary, the contributions of this work are as follows: 

- A Waypoint-Guided Spatial Cross-Attention mechanism that aligns navigational intent with environmental context, ensuring that feature aggregation is spatially anchored to the predicted trajectory. 

- A Stability-Aware Selective Gating module that adaptively modulates the perception field based on the robot’s dynamic stability, prioritizing local terrain features to ensure motion stability. 

- Extensive experimental results on real robots demonstrate that FocusNav significantly enhances navigation success rate, collision avoidance capability, and motion stability in dynamic and complex environments. 

## II. RELATED WORKS 

## _A. Humanoid Perceptive Locomotion_ 

In recent years, significant progress has been made in the perceptive locomotion of humanoid robots concerning complex terrain traversal and obstacle avoidance [29, 30]. Existing research predominantly utilizes onboard LiDAR and RGB-D sensors to achieve environmental perception through elevation maps, depth maps, or point clouds [34]. However, 


Fig. 2: Schematic of the PPA neural circuit paradigm. The system extracts environmental features through perception and predicts waypoints along the path by integrating the target point with the current location. An attention mechanism is then employed to focus on critical environmental information, enhancing mobile navigation performance. 

these methods still encounter technical constraints in practical applications [21]. On one hand, the processing of elevation and depth maps is highly susceptible to computational latency and environmental noise, respectively, which compromises terrain perception accuracy and responsiveness to dynamic obstacles [36]. On the other hand, the prevailing velocity-commandtracking paradigm limits the flexibility of gait adjustments and introduces an inherent objective conflict between obstacle avoidance reward terms and velocity tracking tasks during training, making it difficult to achieve globally optimal motion [7]. Although some studies have attempted to incorporate target position tracking, they remain confined to static obstacle avoidance in flat environments [1]. Simultaneously achieving dynamic obstacle avoidance and robust traversal in unstructured environments, particularly in coordinating terrain information with obstacle constraints to prevent motion conflicts, remains a critical and unresolved challenge. 

## _B. Local Navigation in Complex Environments_ 

Local navigation systems aim to achieve real-time path planning, dynamic obstacle avoidance, and robust locomotion from a robot’s current position to the subsequent local waypoint [9]. Early research primarily employed modular pipelines, integrating high-level perceptive planning with low-level motor skills, particularly on quadrupedal platforms [5]. To enhance terrain traversability assessment, hierarchical learning frameworks were introduced to jointly train navigation and locomotion policies, fostering a deeper understanding of robotenvironment interactions [22]. While end-to-end visual navigation strategies effectively mitigate system latency and cu- 

mulative errors, the inherent flexibility of locomotion models remains constrained by the prevailing velocity-commandtracking paradigm [2]. Recent advancements have significantly improved obstacle avoidance and traversal performance in complex terrains by incorporating local waypoint tracking [14] and utilizing cross-attention mechanisms to strengthen the capability of motion policies in extracting critical perceptive features [42]. However, fully leveraging rich environmental visual information to maintain navigational stability during simultaneous terrain adaptation and dynamic obstacle avoidance remains a pivotal challenge [48]. Distinct from existing methodologies, this paper draws inspiration from biological principles to construct a local navigation framework for humanoid robots based on the PPA mechanism. By guiding the robot to focus on task-relevant key perceptive information, our approach achieves robust mobile navigation performance in extremely complex scenarios. 

## III. GUIDEORACLE: LEARNING ORACLE POLICY FOR WAYPOINT TRACKING 

To bridge the gap between rich environmental information acquired from high-level perception and low-level motion execution, we first develop GuideOracle, a privileged policy specifically engineered for local waypoint tracking. Independent of visual perception, GuideOracle leverages the full observability of the simulation environment to directly access precise local maps and target coordinates. This enables the achievement of highly robust waypoint tracking, thereby providing optimal supervisory signals for the subsequent training of our vision-based navigation policy. 

## _A. Problem Formulation_ 

We formulate the learning of the GuideOracle as a Markov Decision Process (MDP), defined by the tuple M = (S _,_ A _,_ P _,_ R _, 𝛾_ ). The S and A represent the state and action spaces, respectively. The system’s transition dynamics are represented by P( _𝑠𝑡_ +1| _𝑠𝑡 , 𝑎𝑡_ ), R is the reward function, and _𝛾_ ∈[0 _,_ 1) is the discount factor. The objective of the GuideOracle is to optimize the policy _𝜋_ ( _𝑎𝑡_ | _𝑠𝑡_ ) to maximize the expected cumulative discounted reward: 


Consider a three-dimensional environment _𝐸_ ⊂ R<sup>3</sup> , the robot follows a policy _𝜋_ to reach a target region G ⊂ R<sup>3</sup> within a finite time horizon _𝑡_ ≤ _𝑇_ max, such that the relative target position satisfies ∥ _𝑝𝑡_ ∥ _< 𝜖_ , where _𝜖 >_ 0 represents a specified tolerance. We employ Isaac Gym [18] for simulation and Proximal Policy Optimization (PPO) [26] to train the GuideOracle. 

## _B. Observation and Action Space_ 

The observation space includes the base linear and angular velocities, joint positions and velocities, previous actions, navigation commands, and terrain information sampled around the robot. Specifically, the navigation command _𝑐𝑡_ ∈ R<sup>4</sup> is 


Fig. 3: The terrain used for simulation training includes rugged terrain such as stairs, slopes, and gaps. The environment features dense static obstacles such as forest-like pillars, along with dynamic obstacles represented by red robots following randomized trajectories. 

defined as the _𝑋_ - _𝑌_ axis vector position _𝑝_ xy of the robot relative to the target position, the angular deviation _𝑒_ yaw between the robot’s _𝑋_ -axis direction and _𝑝_ xy, and the remaining time to reach the target position. The navigation goal is established at the initial time _𝑡_ 0 of each episode as the relative target position sampled within the robot’s local coordinate frame and the maximum completion time _𝑇_ max. Unlike previous works [14] that rely solely on elevation maps _𝐼𝑒_ ∈ R<sup>_𝑁𝑡_</sup> , where _𝑁𝑡_ = _𝐻𝑡_ × _𝑊𝑡_ , we additionally include a traversability map _𝐼𝑡_ ∈ R<sup>_𝑁𝑡_</sup> , which provides explicit encoding of obstacle regions in the environment. The actions are interpreted as target joint positions given to the motors where a PD controller transforms them into joint torques. 

## _C. Rewards and Terrains Design_ 

The reward follows Ben et al. [1] with velocity tracking reward replaced by target position tracking reward: 


where _𝑇𝑟_ is a parameter defining the duration of the reward, which varies with the sampled _𝑇_ max. Additionally, we introduce an orientation-tracking reward: 


where _𝜔_ yaw denotes the yaw angular velocity of the robot base and _𝛿_ yaw is the weighting coefficient. This reward encourages the robot to align its heading with the target, leveraging the superior stability of forward locomotion on complex terrain. By prioritizing _𝑋_ -axis movement, the policy restricts lateral and backward maneuvers to essential emergency avoidance, ensuring both navigational efficiency and gait robustness. 

To enable robots to learn robust navigation strategies in complex scenarios via simulation, we construct a diverse training environment integrating unstructured rugged terrains and high-density dynamic spaces, as shown in Fig. 3. This environment incorporates unstructured rugged features including stairs, slopes, and gaps, so as to replicate the locomotion challenges caused by terrain elevation changes and traversal 


Fig. 4: Overview of the FocusNav framework. (a) Multi-modal perception encoder fuses spatially aligned LiDAR and depth camera data, utilizing voxel feature encoding and convolutional feature extraction to generate BEV feature of the environment. (b) Collision-free waypoint predictor encodes BEV feature and the robot’s proprioceptive states. Combined with the navigation goal, a goal-conditioned autoregressive decoder performs backward prediction of trajectory waypoints, enhancing the rationality of the trajectory. (c) Dual-layer spatial selective attention employs cross-attention, using predicted waypoints to guide the model’s focus toward high-relevance features along the planned trajectory. Furthermore, a Gumbel Softmax-based gating mechanism dynamically shifts the focus toward local terrain features beneath the robot’s feet according to its stability. 

constraints in real-world scenarios. In addition, we simulate the complex spatiotemporal uncertainties of real environments by integrating forest-like scenes composed of dense pillars, crowd-dense scenarios, and randomly moving robot entities as dynamic obstacles. This multi-dimensional environment design ensures that the learned policies exhibit excellent generalization performance when confronted with various spatial constraints and dynamic disturbances. Based on obstacles and terrain gaps, the environmental information acquired by the robot includes elevation maps and traversability map _𝐼_ et = { _𝐼𝑒, 𝐼𝑡_ }. Traversability map explicitly characterizes the nontraversability of obstacle and gap regions. In addition, the randomly sampled navigation target positions are processed by a reachability optimization layer, which projects the target positions located in non-traversable regions onto the nearest reachable areas along the direction connecting the robot and the target, thereby ensuring the effectiveness of the robot’s navigation tasks in complex environments. 

## IV. FOCUSNAV: LOCAL NAVIGATION WITH SPATIAL SELECTIVE ATTENTION 

In this section, we present a detailed exposition of the FocusNav framework, which is engineered to enhance the local navigation performance of humanoid robots in complex 

and dynamic environments by emulating the PPA paradigm in biological neural navigation circuits. As illustrated in Fig. 4, the FocusNav comprises three synergistically integrated modules: a multi-modal perception encoder for comprehensive environmental feature extraction, a collision-free waypoint predictor for safe path planning, and a dual-layer spatial selective attention mechanism for prioritized feature processing. By mimicking the hierarchical information processing of biological systems, FocusNav enables the robot to precisely focus on critical environmental cues, achieving effective dynamic obstacle avoidance while maintaining superior motion stability during goal-directed navigation tasks. 

## _A. Multi-Modal Perception Encoder_ 

_1) Efficient Sensor Simulation:_ To acquire environmental information, we utilize LiDAR and depth camera commonly integrated into robotic platforms. We implement highperformance LiDAR rendering [36] and depth synthesis [29] using NVIDIA Warp [17] for GPU-accelerated raycasting. To enhance the speed of dynamic geometry rendering, we adopt the method proposed by Ben et al. [1] to precompute the Bounding Volume Hierarchy (BVH) for meshes within its local frames. At each simulation step, the ray origin _𝑝𝑟_ and direction _𝑑𝑟_ are transformed into the local frame. Ray- 


Fig. 5: FoV of onboard LiDAR and depth camera for the robot. (a) Complementary sensing characteristics [33]: The LiDAR is characterized by an extended effective measurement range, whereas the depth camera reliably covers the proximal terrain surrounding the robot’s feet. (b) Cross-modal point cloud in simulation: The red and blue point clouds are from the LiDAR and the depth camera, respectively. 

mesh intersections are then efficiently computed using the precomputed BVH, after which the resulting local intersection coordinates are transformed back into the world frame. The raycasting process can be formally represented as: 


where _𝑀_ denotes the mesh geometry, _𝑇_ represents the homogeneous transformation matrix, and _𝑅_ indicates the rotational component. 

_2) Cross-Modal Spatial Alignment:_ Owing to the discrepancies in mounting positions and Fields of View (FOV) among various sensors, multi-modal fusion significantly extends the perceptual range and enhances sensing accuracy. Taking the Unitree G1 humanoid robot [32] as an example, the onboard LiDAR provides a significantly greater observation range than the depth camera, yet it is constrained by a blind spot regarding the immediate terrain surrounding the robot’s feet, as illustrated in Fig. 5(a). Uniform voxel sampling [24] is employed to extract the sparse point cloud _𝑃𝐿_ from the dense LiDAR data. Meanwhile, the depth map _𝐷𝐶_ ∈ R<sup>_𝐻_×</sup><sup>_𝑊_</sup> is backprojected into the camera-centric point cloud _𝑃𝐶_ using the camera intrinsic matrix _𝐾_ ∈ R<sup>3×3</sup> . For a pixel coordinate ( _𝑢, 𝑣_ ) with depth value _𝑑_ , the corresponding 3D point _𝑝𝑐_ ∈ _𝑃𝐶_ is computed as: 


then _𝑃𝐶_ = { _𝑝𝑐,𝑖_ } _𝑖_<sup>_𝑁_</sup> =<sup>_𝑐_</sup> 1<sup>, where</sup><sup>_𝑁𝑐_=</sup><sup>_ℎ_×</sup><sup>_𝑤_represents the number</sup> of point clouds corresponding to the image. By leveraging sensor extrinsic parameters, both _𝑃𝐿_ and _𝑃𝐶_ are transformed into the world frame and concatenated to form the cross-modal point cloud _𝑃_ LC = { _𝑃_<sup>_𝑤_</sup> _𝐿_<sup>_, 𝑃_</sup> _𝐶_<sup>_𝑤_}.AsdemonstratedinFig.5(b),</sup> the red points represent the LiDAR-derived point cloud _𝑃𝐿_ , while the blue points denote the point cloud _𝑃𝐶_ acquired via the depth camera. 

_3) BEV Feature Extraction:_ Inspired by the VoxelNet architecture [47], we develop a lightweight perception encoder to transform the unstructured point cloud _𝑃_ LC into a structured Bird’s-Eye-View (BEV) representation. The process begins with voxelization V(·), where _𝑃_ LC is discretized into a 3D grid of size _𝐷_ × _𝐻_ × _𝑊_ . A voxel feature encoding layer learns a high-dimensional latent representation for each non-empty voxel, effectively capturing local geometric primitives. The encoded 4D tensor is processed through 3D convolution C3D. The resulting feature volume is subsequently projected onto the BEV plane via a _𝑍_ -axis global maximum pooling operator P _𝑧_ . A multi-scale convolutional network G is utilized to perform feature fusion, yielding the spatially consistent BEV feature _𝐹_ bev ∈ R<sup>_𝐶_×</sup><sup>_𝐻_×</sup><sup>_𝑊_</sup> . Formally, this composite mapping is expressed as: 


where ◦ denotes the function composition. This pipeline efficiently extracts a semantic-rich and spatially consistent environment representation. To augment latent features with semantic traversability, a traversability decoder upsamples the _𝐹_ bev into a traversability map _𝐼_<sup>ˆ</sup> _𝑡_ ∈ R<sup>_𝐻𝑡_×</sup><sup>_𝑊𝑡_</sup> . The network is optimized via the Binary Cross-Entropy loss: 


where _𝐼𝑡,𝑖_ ∈{0 _,_ 1} represents the ground-truth traversability. 

_B. Collision-Free Waypoint Predictor_ 

_1) Backward Prediction Paradigm:_ To bridge the gap between high-level perception and low-level control, we propose a goal-conditioned backward prediction paradigm for generating collision-free navigation waypoints. Unlike conventional forward prediction paradigms that are prone to accumulating compound errors [15], backward prediction paradigm explicitly generates waypoints starting from the navigation target _𝑔𝑛_ back to the robot’s current position. This formulation enforces a reverse causal dependency among waypoints, yielding a goal-conditioned reasoning chain that ensures global-to-local consistency [46]. By anchoring the trajectory to the navigation target, we enhance the logical coherence and traversability of the planned path. Formally, given the observation O, which includes the BEV features _𝐹_ bev, the robot’s proprioceptive state _𝑆 𝑝_ and the navigation target _𝑔𝑛_ , the predictor models the trajectory distribution as a joint probability of waypoints _𝑞_ ˆ in reverse chronological order: 


This backward chaining mechanism utilizes the navigation target _𝑔𝑛_ as a strong prior to regularize the entire decoding sequence, forcing the latent representation to focus on the reachable manifold of the terrain, thereby enhancing the logical consistency and robustness of trajectory prediction in complex unstructured environments. 

_2) Autoregressive Network with Latent Consistency:_ To implement the backward prediction paradigm, we develop a goalconditioned Transformer architecture that recursively predicts waypoints in reverse-time autoregression by integrating multimodal environmental context with robot proprioceptive states, as shown in Fig. 4(b). The transformer encoder serves as a perception backbone that extracts context-aware latent embeddings by processing a concatenated sequence of flattened BEV patches and the robot’s proprioceptive state _𝑆 𝑝_ . Utilizing the causal transformer decoder, we generate the waypoint sequence { ˆ _𝑞 𝑘_ } _𝑘_<sup>_𝑁_</sup> =1<sup>autoregressively starting from the navigation</sup> target _𝑔𝑛_ . This setup ensures that each waypoint prediction is strictly conditioned on both the global goal and the sequence of previously predicted distal points. The network is optimized via a multi-task objective function that jointly supervises spatial accuracy and temporal coherence. Specifically, we employ a waypoint reconstruction loss Lrec based on Mean Squared Error (MSE) to minimize the geometric discrepancy between predicted coordinates _𝑞_ ˆ _𝑘_ and ground-truth waypoints _𝑞 𝑘_ . To address the temporal inconsistency and error propagation inherent in continuous latent space autoregression [43], we introduce latent consistency regularization Lreg. This mechanism explicitly aligns the predicted latent tokens _𝑥_ ˆ _𝑘_ with the expert latent representations _𝑓_ enc ( _𝑞𝑘_ ), forcing the model to adhere to the feasible manifold. The waypoint prediction loss L _𝑝_ = Lrec + Lreg is formulated as: 


where _𝑁_ represents the number of waypoints, _𝜆_ reg is a weighting coefficient used to balance waypoints prediction accuracy and temporal consistency. 

## _C. Dual-Layer Spatial Selective Attention_ 

To extract task-critical features from high-dimensional environment representations, we propose a dual-layer spatial selective attention module, as illustrated in Fig. 4(c). This module mimics selective attention by dynamically focusing on navigation-relevant spatial cues, thereby enhancing the control robustness of humanoid robots in unstructured terrains [19]. 

_1) Waypoint-Guided Spatial Cross-Attention:_ The first layer of our attention mechanism utilizes the predicted collision-free waypoints { ˆ _𝑞𝑘_ } _𝑘_<sup>_𝑁_</sup> =1<sup>toguidetheperceptionpro-</sup> cess. Specifically, we utilize the latent tokens { _𝑥_ ˆ _𝑘_ } _𝑘_<sup>_𝑁_</sup> =1<sup>,the</sup> intermediate representations of the predicted waypoints, as queries, while the sequence of flattened BEV patches serves as keys and values. To reinforce the spatial correspondence between these modalities, we introduce a Spatially-Aligned Position Embedding (PE) mechanism. By projecting both the waypoints and BEV patches into a unified coordinate system, we employ sinusoidal position embeddings to preserve their relative spatial topological structure. Consequently, the crossattention module performs precise point-wise attention over the environment, ensuring that the attention scores accurately reflect the physical proximity between the robot’s intended 

path and surrounding terrain features. Formally, this process yields a sequence of waypoint-focused map embeddings { _𝑚𝑘_ } _𝑘_<sup>_𝑁_</sup> =1<sup>∈R</sup><sup>_𝑁_×</sup><sup>_𝑑_:</sup> 


where each embedding _𝑚𝑘_ ∈ R<sup>_𝑑_</sup> represents the environmental feature context specifically aggregated at the spatial location of the _𝑘_ -th predicted waypoint. This operation effectively anchors the perception to the planned path, filtering out irrelevant background noise and focusing the representation on the local traversability and obstacles critical to the robot’s immediate movement. 

_2) Stability-Aware Selective Gating:_ To further ensure the robot’s immediate survival in highly dynamic or precarious terrains, we introduce a gating mechanism as the second layer of our spatial attention module. This layer operates on the trajectory-aligned map embeddings { _𝑚 𝑘_ } _𝑘_<sup>_𝑁_</sup> =1<sup>bydynamically</sup> truncating distal spatial information based on the robot’s proprioceptive state _𝑆 𝑝_ . Specifically, _𝑆 𝑝_ is processed through a Multi-Layer Perceptron (MLP) to generate the gating logits _𝑉_<sup>_𝑔_</sup> ∈ R<sup>2</sup> , representing the activation and deactivation probabilities for the gating module. To maintain end-to-end differentiability while performing discrete selection, the gate control variable _𝑔_ is sampled using the Gumbel-Softmax distribution [10]: 


where _𝜏_ denotes the temperature parameter. The variable _𝑔_ serves as a binary switch that governs the inclusion of distal environmental context { _𝑚 𝑘_ } _𝑘_<sup>_𝑁_</sup> =2<sup>.Specifically,when</sup><sup>_𝑔_= 1,the</sup> activated gate indicates a stable robotic state, whereby the model aggregates environmental information along the entire trajectory to fulfill the navigation task. Conversely, _𝑔_ = 0 signifies a decrease in dynamic stability, prompting the model to truncate far-field environmental embeddings and refocus exclusively on the immediate terrain features surrounding the robot’s feet. The resulting stability-aware hybrid map embedding _𝑚_<sup>_ℎ_</sup> is formulated as: 


By prioritizing local foothold safety over distant navigation targets during periods of instability, this mechanism ensures effective recovery and robust traversal in complex, nonstructured environments. To supervise the gating mechanism, we derive a stability metric S _𝑚_ ∈[0 _,_ 1] based on the robot’s real-time proprioceptive feedback, including angular velocities _𝜔_ and Euler angles _𝜙_ . The stability metric is formulated to quantify the deviation from a balanced state: 


where { _𝑘𝑖_ } are scaling constants. The gating module is optimized via a cross-entropy loss L _𝑔_ that aligns the gating probabilities _𝑝𝑘_ = _𝑃_ ( _𝑔_ = _𝑘_ ) with the stability metric S _𝑚_ : 


This objective ensures that the gating module learns to autonomously modulate its perceptual focus based on the robot’s dynamic equilibrium. 

The selectively extracted hybrid map embedding _𝑚_<sup>_ℎ_</sup> is concatenated with the robot’s state _𝑆 𝑝_ and processed by a GRU-based control policy. By leveraging its hidden state _ℎ𝑡_ , the GRU maintains a latent memory of the environment, ensuring that global navigation consistency is preserved even when the gating mechanism temporarily shifts focus toward immediate local footholds. The control policy is optimized using a Behavior Cloning (BC) objective Lbc to minimize the discrepancy between the FocusNav’s actions and the GuideOracle’s expert demonstrations. To ensure that the internal representations are task-relevant, the entire pipeline is trained in an end-to-end differentiable manner. The total training loss Ltotal can be expressed as: 


where the coefficients { _𝜆𝑖_ } _𝑖_ =1 _,_ 2 _,_ 3 are hyperparameters used to balance the contribution of each auxiliary task. This joint optimization ensures that the perception, prediction, attention, and control modules are mutually aligned for robust mobile navigation in unstructured environments. 

## V. EXPERIMENTS 

In this section, we present extensive experimental results of FocusNav conducted in both simulation and real-world environments. Our experiments are designed to systematically evaluate the effectiveness of the proposed framework in navigating complex and dynamic environments, specifically addressing the following research questions: (1) Does the WGSCA mechanism effectively leverage predicted waypoints to anchor task-relevant environmental features? (2) Does the SASG module effectively modulate the attention span to prioritize stability when necessary? (3) Does FocusNav significantly outperform baseline methods in humanoid local navigation across dynamic and unstructured terrains? 

## _A. Experimental Setup_ 

We deploy FocusNav on the Unitree G1, a 29-DoF humanoid robot equipped with a Livox MID-360 LiDAR and a RealSense D435i depth camera for environmental perception. Training is conducted within the IsaacGym simulation environment [18], distributed across four NVIDIA RTX 4090 GPUs. For real-world deployment, the robot’s relative localization is estimated via the Fast-LIO algorithm [40] using LiDAR point clouds. 

_1)_ **_Baselines_** _:_ To evaluate the contribution of each core component in FocusNav, we compare our framework against the following three baseline methods: 

- **Gallant** [1]: Following the standard feature fusion paradigm, this baseline directly concatenates processed environmental features with proprioceptive states before feeding them into the policy network. 

- **Proprioception-Guided Cross-Attention** ( **PGCA** ) [7]: This variant utilizes the robot’s proprioceptive state _𝑆_ as the query to attend to the BEV environmental features. 

- **WGSCA-Only** : This version incorporates our proposed WGSCA mechanism but excludes the SASG module. It is designed specifically to isolate and evaluate the impact of the stability-aware gating module on motion performance. 

- _2)_ **_Metrics_** _:_ We employ the following four quantitative 

- metrics to evaluate the performance of our model: 

- **Success Rate** _𝐸_ success: The percentage of episodes in which the robot successfully reaches the target location without terminal failure. 

- **Traverse Rate** _𝐸_ traverse: The ratio of the actual distance traveled by the robot before termination to the planned travel distance. 

- **Collision Frequency** _𝐸_ collision: The frequency of collision events between the robot and environmental obstacles per unit time. 

- **Motion Stability** _𝐸_ stability: The average stability metric S _𝑚_ of robot motion trajectory. 

## _B. Simulation Results_ 

_1) Quantitative Results:_ We report a detailed quantitative comparison of FocusNav against baseline methods in Table I, evaluated across four quantitative metrics: success rate _𝐸_ success, traverse rate _𝐸_ traverse, collision frequency _𝐸_ collision, and motion stability _𝐸_ stability. These benchmarks are conducted in diverse scenarios, including flat and unstructured terrains with both static and dynamic obstacles. For each configuration, we compute the mean and standard deviation from policies trained with three distinct random seeds, each validated across 100 randomized episodes. The experimental results lead to the following key conclusions and insights: 

**Superiority of FocusNav in complex environments.** Quantitative results demonstrate that FocusNav consistently outperforms all baseline methods, particularly as environmental complexity increases. In the most challenging dynamic and unstructured scenario, FocusNav achieves a success rate _𝐸_ success of 87 _._ 02%, significantly surpassing Gallant (50 _._ 32%) and PGCA (63 _._ 67%). This substantial margin highlights the limitations of standard environmental feature extraction and proprioception-guided attention mechanisms when handling simultaneous terrain disturbances and moving obstacles. In contrast, our framework maintains high reliability by anchoring environmental attention to the predicted trajectory while dynamically focusing on local foothold features. 

**Enhanced long-range perception via WGSCA.** Compared to PGCA, which primarily extracts environmental features around the robot’s feet via proprioceptive attention, WGSCA enhances long-range proactive perception by anchoring spatial attention to predicted waypoints. This approach establishes a direct correlation between distal environmental features and the current motion plan, thereby improving adaptability to complex navigation tasks. By filtering out irrelevant environmental interference outside the intended trajectory, 

TABLE I: Quantitative simulation results of FocusNav and baseline methods. Evaluated across flat and unstructured terrains with static/dynamic obstacles, the results demonstrate the robustness of FocusNav in balancing environmental feature extraction and immediate motion stability. Bold values indicate the best performance in each experimental setting. 

|**Method**|Flat T|errain|||Unstructure|d Terrain||
|---|---|---|---|---|---|---|---|
|_𝐸_success(%) ↑|_𝐸_traverse(%) ↑|_𝐸_collision(%) ↓|_𝐸_stability ↑|_𝐸_success(%) ↑|_𝐸_traverse(%) ↑|_𝐸_collision(%) ↓|_𝐸_stability ↑|
|**Static Obstacle Environment**||||||||
|Gallant<br>85_._45±2_._12|88_._30±3_._45|2_._65±0_._32|0_._79±0_._04|60_._14±3_._56|65_._55±4_._12|4_._42±0_._45|0_._61±0_._05|
|PGCA<br>90_._67±1_._55|92_._12±2_._05|2_._24±0_._15|0_._82±0_._03|71_._89±2_._89|75_._34±3_._21|3_._52±0_._25|0_._70±0_._04|
|WGSCA-Only 95_._12±0_._85|96_._45±1_._15|1_._69±0_._06|0_._84±0_._02|82_._23±2_._01|85_._17±2_._55|2_._58±0_._09|0_._73±0_._05|
|**FocusNav**<br>**97**_._**54**±**0**_._**35**|**98**_._**88**±**0**_._**52**|**1**_._**42**±**0**_._**05**|**0**_._**88**±**0**_._**02**|**91**_._**15**±**0**_._**88**|**93**_._**20**±**1**_._**12**|**2**_._**08**±**0**_._**08**|**0**_._**81**±**0**_._**03**|
|**Dynamic Obstacle Environme**|**nt**|||||||
|Gallant<br>68_._23±4_._15|72_._12±5_._22|8_._45±0_._89|0_._67±0_._05|50_._32±7_._67|53_._15±8_._12|12_._55±1_._25|0_._55±0_._07|
|PGCA<br>75_._45±3_._25|78_._88±4_._05|6_._62±0_._65|0_._72±0_._04|63_._67±5_._45|66_._23±5_._15|8_._94±0_._88|0_._62±0_._06|
|WGSCA-Only 84_._34±1_._85|88_._12±2_._45|3_._88±0_._22|0_._77±0_._03|74_._15±3_._15|78_._78±4_._25|**4**_._**32**±**0**_._**35**|0_._68±0_._05|
|**FocusNav**<br>**93**_._**45**±**1**_._**02**|**94**_._**42**±**1**_._**85**|**3**_._**75**±**0**_._**15**|**0**_._**84**±**0**_._**06**|**87**_._**02**±**1**_._**15**|**89**_._**17**±**2**_._**99**|4_._56±0_._21|**0**_._**76**±**0**_._**04**|
|(a)||(b)||(a)||(b)||


Fig. 6: Visualization of traversability and waypoints prediction. (a) Robot-centric local traversability prediction results.Red regions indicate untraversable areas due to obstacles in the environment. (b) Waypoint prediction results across four navigation directions. Collision-free trajectories are predicted within environments featuring diverse obstacles. 

Fig. 7: Visualization of waypoint-guided cross-attention over BEV features. (a) Proximal waypoint: Attention concentrates near the robot’s feet, focusing on terrain features critical for foothold safety. (b) Distal waypoint: Attention anchors to the distant predicted path, extracting long-range environmental cues for navigational consistency. 

WGSCA ensures that long-range perception is more taskoriented, enabling more predictive and smoother dynamic obstacle avoidance. 

**Necessity of SASG in dynamic perceptual field modulation.** In unstructured terrain navigation, when local terrain complexity leads to degraded robot stability, the SASG module autonomously truncates distal information. This compels the motion policy to concentrate attention on immediate foothold features, thereby enhancing instantaneous motion robustness and facilitating the completion of long-range navigation tasks. Furthermore, in dynamic unstructured environments, FocusNav exhibits a slightly higher collision frequency compared to the WGSCA-only variant. This reveals a critical trade-off between terrain traversal and dynamic obstacle avoidance in complex environments. To maintain motion stability throughout long-range tasks, the SASG module enables the robot to prioritize self-stability over aggressive collision avoidance, preventing catastrophic falls and ensuring task completion. 

_2) Task-Oriented Perceptual Anchoring via WGSCA:_ To further elucidate how WGSCA effectively filters environmental noise and precisely anchors perceptual focus to critical spatial regions, we systematically analyze several key components. We visualize the terrain traversability reconstructed from the BEV features in a multi-obstacle environment, as shown in Fig. 6(a), where red regions denote non-traversable areas containing obstacles. By comparing the reconstructed maps with the ground truth, it is evident that the BEV features effectively identify irregular and disordered obstacles. Furthermore, we visualize the goal-conditioned backward waypoint trajectory predictions for navigation tasks with different directions of motion, as shown in Fig. 6(b). The results demonstrate that, by integrating navigational goals with environmental BEV features, the WGSCA module accurately interprets global task intents and generates collision-free waypoints. This capability provides proactive spatial guidance for long-range navigation tasks. 

Furthermore, by comparing the cross-attention distributions 


Fig. 8: Visualization of attention gates in dynamic and complex terrain navigation. As the robot transitions from flat ground to stairs, the attention gating selectively truncates distal perceptual information to prioritize proximal terrain features, thereby enhancing foothold safety. 


Fig. 9: Correlation between SASG and motion stability. (a) Spatial distribution of attention gating truncation rate. The truncation rate increases significantly as the robot transitions from central flat ground to surrounding stairs. (b) Stability improvement attributed to SASG. Comparative analysis of spatial stability distributions demonstrates that SASG significantly enhances FocusNav’s performance on stair terrain relative to the WGSCA-Only baseline. 

Fig. 8, we visualize the attention gating signals of the robot navigating through dynamic and complex terrains. The spatiotemporal relationship between the robot’s position and the gating signals demonstrates that during stable locomotion on flat ground, the gating mechanism remains fully open, allowing the integration of long-range waypoint features for global navigation. However, when the robot encounters unstructured terrain disturbances that compromise its stability, the SASG module rapidly truncates environmental information from distal waypoints. This prevents distant obstacles from interfering with motion decisions, thereby mitigating potential stability issues during navigational maneuvers. This dynamic selective attention compels the model to prioritize proximal spatial features in complex terrains, enhancing foothold safety. Consequently, the mechanism achieves an optimal balance between short-term motion stability and global goal-directed perception. Furthermore, we visualize the correlation between the SASG module and the robot’s motion stability. 

As illustrated in Fig. 9(a), we present the spatial distribution of the attention gating truncation rate. Specifically, by having the robot navigate from a central flat region across surrounding staircase areas, we recorded the frequency of gating activations at different spatial coordinates to calculate the spatial distribution across various terrains. The results indicate that the gating activation rate remains low in the flat central region but increases significantly as the robot transitions to the staircases. This trend aligns with the human-like heuristic that prioritizes local terrain details in complex areas to ensure foothold safety. Fig. 9(b) demonstrates the percentage of stability improvement achieved by FocusNav compared to the WGSCA-Only baseline. The positive correlation between stability improvement and SASG activation suggests that without SASG, the robot tends to execute aggressive navigational maneuvers influenced by distal obstacles, which often leads to falls on unstructured terrains. In contrast, FocusNav prioritizes local stability when necessary, thereby significantly improving the overall completion rate of long-range navigation tasks. 

## _C. Real-World Experiments_ 

guided by waypoints at varying distances, we demonstrate that WGSCA dynamically extracts trajectory-relevant environmental features based on the predicted path. As illustrated in Fig. 7, when queried with proximal waypoints, the attention selectively prioritizes the immediate surroundings to extract terrain structures critical for foothold selection. In contrast, with distal waypoints, attention extends along the anticipated trajectory to distill long-range environmental cues. This spatial selective attention mechanism enables the model to establish a spatio-temporal correlation between navigational intent and environmental perception, which significantly enhances the consistency of the robot’s navigational decision-making in complex and dynamic environments. 

_3) Detailed Analysis of the SASG:_ To further investigate the impact of the SASG module, we evaluate its dynamic response in challenging, unstable terrains. As illustrated in 

FocusNav is deployed on a Unitree G1 humanoid robot to evaluate the practical performance of local navigation in unstructured and dynamic environments. We establish a standardized testing arena that features a variety of challenging terrains and obstacles, including 16 cm stairs, 22<sup>◦</sup> slopes, static box obstacles, and dynamic pedestrian interference. Based on the combinations of terrain and obstacle types, the experimental configurations are categorized into six distinct scenarios. Snapshots of FocusNav successfully traversing these diverse complex environments are illustrated in Fig. 10. We compare FocusNav against several baseline methods. For each scenario, we conduct 15 independent trials to record the number of successful missions, defined as reaching the navigation target point without falling or colliding. As shown in Fig. 11, FocusNav significantly outperforms all baseline methods across all test cases. In highly demanding tasks, such as traversing narrow 16cm stairs amidst dynamic obsta- 


Fig. 10: Robust local navigation of FocusNav in diverse and challenging environments. (a) Traversing 22<sup>◦</sup> slopes. (b) Traversing 16 cm stairs. (c) Local navigation through static obstacles on flat ground. (d) Concurrent 22<sup>◦</sup> slope traversal and dynamic obstacle avoidance. (e) Navigating through static obstacles on 22<sup>◦</sup> slopes. (f) Navigation across 16 cm stairs with static obstacles. The results highlight the effectiveness of FocusNav in maintaining motion stability while executing navigational maneuvers in unstructured and dynamic settings. 


Fig. 11: Navigation success rates across 15 trials in real-world dynamic and complex environments. FocusNav outperforms all baselins. Benefiting from the dual-layer spatial selective attention mechanism, FocusNav effectively handles both dynamic obstacles and complex terrains, substantially enhancing the navigational performance of the humanoid robot. 

of navigation and stability for humanoid robots in unstructured environments. By integrating the WGSCA mechanism with the SASG module, our approach enables the robot to dynamically shift its perceptual focus between global navigation targets and local terrain features in response to real-time dynamic stability. Experimental results on the Unitree G1 humanoid robot validate that the proposed method effectively enhances motion robustness and collision avoidance capabilities in complex navigation scenarios. Our work advances the practical application of robust humanoid navigation, demonstrating that spatial selective perception is a key enabler for agile locomotion. By bridging the gap between intentional guidance and reactive stability, FocusNav paves the way for the deployment of versatile humanoid robots in complex, real-world applications. 

cles, FocusNav demonstrates the capability to plan collisionfree paths for pedestrian avoidance while maintaining precise foothold placement, as illustrated in Fig. 1. FocusNav’s superior performance stems from its dual-layer spatial selective attention. By anchoring perception to predicted navigational intent via WGSCA, the framework filters task-irrelevant noise to maintain focus on collision-free trajectories. Concurrently, the SASG module dynamically prioritizes proximal terrain features over distal cues during instability to ensure foothold safety. This hierarchical perception achieves an optimal balance between goal-directed navigation and motion stability, significantly enhancing performance in complex real-world settings. 

## VI. CONCLUSION 

In this work, we propose FocusNav, a novel spatial selective attention framework designed to address the dual challenges 

## VII. LIMITATIONS 

Despite the superior performance of FocusNav, several limitations remain to be addressed in future research. FocusNav primarily concentrates on the forward direction and lacks comprehensive focus on the robot’s immediate surroundings. This limits its applicability in scenarios requiring backward maneuvers or those with obstacles situated behind the robot. Future work could focus on integrating proactive spatial region selection modules to enhance omnidirectional perceptual awareness. FocusNav requires pre-defined navigational goals and lacks high-level semantic understanding for long-chain navigation tasks. Future research will explore the integration of Vision-Language Models (VLMs) to enable socially-aware navigation and complex reasoning within human-centric environments. 

REFERENCES 

eadi9641, 2024. 

- [1] Qingwei Ben, Botian Xu, Kailin Li, Feiyu Jia, Wentao Zhang, Jingping Wang, Jingbo Wang, Dahua Lin, and Jiangmiao Pang. Gallant: Voxel grid-based humanoid locomotion and local-navigation across 3d constrained terrains. _arXiv preprint arXiv:2511.14625_ , 2025. 

- [2] Wenzhe Cai, Jiaqi Peng, Yuqiang Yang, Yujian Zhang, Meng Wei, Hanqing Wang, Yilun Chen, Tai Wang, and Jiangmiao Pang. Navdp: Learning sim-to-real navigation diffusion policy with privileged information guidance. _arXiv preprint arXiv:2505.08712_ , 2025. 

- [3] An-Chieh Cheng, Yandong Ji, Zhaojing Yang, Zaitian Gongye, Xueyan Zou, Jan Kautz, Erdem Bıyık, Hongxu Yin, Sifei Liu, and Xiaolong Wang. Navila: Legged robot vision-language-action model for navigation. _arXiv preprint arXiv:2412.04453_ , 2024. 

- [4] Daria de Tinguy, Tim Verbelen, Emilio Gamba, and Bart Dhoedt. Bio-inspired topological autonomous navigation with active inference in robotics. _arXiv preprint arXiv:2508.07267_ , 2025. 

- [5] Alejandro Escontrela, Justin Kerr, Arthur Allshire, Jonas Frey, Rocky Duan, Carmelo Sferrazza, and Pieter Abbeel. Gaussgym: An open-source real-to-sim framework for learning locomotion from pixels. _arXiv preprint arXiv:2510.15352_ , 2025. 

- [6] Zhaoyuan Gu, Junheng Li, Wenlan Shen, Wenhao Yu, Zhaoming Xie, Stephen McCrory, Xianyi Cheng, Abdulaziz Shamsah, Robert Griffin, C Karen Liu, et al. Humanoid locomotion and manipulation: Current progress and challenges in control, planning, and learning. _arXiv preprint arXiv:2501.02116_ , 2025. 

- [7] Junzhe He, Chong Zhang, Fabian Jenelten, Ruben Grandia, Moritz B¨acher, and Marco Hutter. Attentionbased map encoding for learning generalized legged locomotion. _Science Robotics_ , 10(105):eadv3604, 2025. 

- [8] Tairan He, Chong Zhang, Wenli Xiao, Guanqi He, Changliu Liu, and Guanya Shi. Agile but safe: Learning collision-free high-speed legged locomotion. _arXiv preprint arXiv:2401.17583_ , 2024. 

- [9] David Hoeller, Nikita Rudin, Dhionis Sako, and Marco Hutter. Anymal parkour: Learning agile navigation for quadrupedal robots. _Science Robotics_ , 9(88):eadi7566, 2024. 

- [10] Eric Jang, Shixiang Gu, and Ben Poole. Categorical reparameterization with gumbel-softmax. _arXiv preprint arXiv:1611.01144_ , 2016. 

- [11] Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, Chuang Wang, Zhihui Peng, et al. Wholebodyvla: Towards unified latent vla for whole-body loco-manipulation control. _arXiv preprint arXiv:2512.11047_ , 2025. 

- [12] Joonho Lee, Marko Bjelonic, Alexander Reske, Lorenz Wellhausen, Takahiro Miki, and Marco Hutter. Learning robust autonomous navigation and locomotion for wheeled-legged robots. _Science Robotics_ , 9(89): 

- [13] Anqi Li, Zhiyong Wang, Jiazhao Zhang, Minghan Li, Yunpeng Qi, Zhibo Chen, Zhizheng Zhang, and He Wang. Urbanvla: A vision-language-action model for urban micromobility. _arXiv preprint arXiv:2510.23576_ , 2025. 

- [14] Kwan-Yee Lin and Stella X Yu. Let humanoids hike! integrative skill development on complex trails. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22498–22507, 2025. 

- [15] Dongxiu Liu, Haoyi Niu, Zhihao Wang, Jinliang Zheng, Yinan Zheng, Zhonghong Ou, Jianming Hu, Jianxiong Li, and Xianyuan Zhan. Efficient robotic policy learning via latent space backward planning. _arXiv preprint arXiv:2505.06861_ , 2025. 

- [16] Yunhao Liu, Li Liu, Yawen Zheng, Yunhuai Liu, Fan Dang, Ningbo Li, and Ke Ma. Embodied navigation. _Science China Information Sciences_ , 68(4):1–39, 2025. 

- [17] Miles Macklin. Warp: A high-performance python framework for gpu simulation and graphics. In _NVIDIA GPU Technology Conference (GTC)_ , volume 3, 2022. 

- [18] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 

- [19] Jonathan Samir Matthis, Jacob L Yates, and Mary M Hayhoe. Gaze and the control of foot placement when walking in natural terrain. _Current Biology_ , 28(8):1224– 1233, 2018. 

- [20] Jiaqi Peng, Wenzhe Cai, Yuqiang Yang, Tai Wang, Yuan Shen, and Jiangmiao Pang. Logoplanner: Localization grounded navigation policy with metric-aware visual geometry. _arXiv preprint arXiv:2512.19629_ , 2025. 

- [21] Junli Ren, Tao Huang, Huayi Wang, Zirui Wang, Qingwei Ben, Junfeng Long, Yanchao Yang, Jiangmiao Pang, and Ping Luo. Vb-com: Learning vision-blind composite humanoid locomotion against deficient perception. _arXiv preprint arXiv:2502.14814_ , 2025. 

- [22] Pascal Roth, Jonas Frey, Cesar Cadena, and Marco Hutter. Learned perceptive forward dynamics model for safe and platform-aware robotic navigation. _arXiv preprint arXiv:2504.19322_ , 2025. 

- [23] Nikita Rudin, David Hoeller, Marko Bjelonic, and Marco Hutter. Advanced skills by learning locomotion and local navigation end-to-end. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 2497–2503. IEEE, 2022. 

- [24] Radu Bogdan Rusu and Steve Cousins. 3d is here: Point cloud library (pcl). In _2011 IEEE international conference on robotics and automation_ , pages 1–4. IEEE, 2011. 

- [25] Sourav Sanyal, Amogh Joshi, Adarsh Kosta, and Kaushik Roy. Real-time neuromorphic navigation: Guiding physical robots with event-based sensing and task- 

specific reconfigurable autonomy stack. _arXiv preprint arXiv:2503.09636_ , 2025. 

- [26] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ , 2017. 

- [27] C. Sheikder, W. Zhang, X. Chen, et al. Bioinspired navigation systems for robots. _Nature Reviews Bioengineering_ , 3:910–911, 2025. doi: 10. 1038/s44222-025-00367-6. URL https://doi.org/10.1038/ s44222-025-00367-6. 

- [28] Xinshuai Song, Weixing Chen, Yang Liu, Weikai Chen, Guanbin Li, and Liang Lin. Towards long-horizon visionlanguage navigation: Platform, benchmark and method. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 12078–12088, 2025. 

- [29] Jingkai Sun, Gang Han, Pihai Sun, Wen Zhao, Jiahang Cao, Jiaxu Wang, Yijie Guo, and Qiang Zhang. Dpl: Depth-only perceptive humanoid locomotion via realistic depth synthesis and cross-attention terrain reconstruction. _arXiv preprint arXiv:2510.07152_ , 2025. 

- [30] Wandong Sun, Baoshi Cao, Long Chen, Yongbo Su, Yang Liu, Zongwu Xie, and Hong Liu. Learning perceptive humanoid locomotion over challenging terrain. _arXiv preprint arXiv:2503.00692_ , 2025. 

- [31] Huajie Tan, Xiaoshuai Hao, Cheng Chi, Minglan Lin, Yaoxu Lyu, Mingyu Cao, Dong Liang, Zhuo Chen, Mengsi Lyu, Cheng Peng, et al. Roboos: A hierarchical embodied framework for cross-embodiment and multiagent collaboration. _arXiv preprint arXiv:2505.03673_ , 2025. 

- [32] Unitree G1. https://www.unitree.com/cn/g1, 2025. [Online; accessed 09-January-2026]. 

- [33] Unitree Robotics. G1 Developer Documentation: About G1. https://support.unitree.com/home/en/G1 <u>developer/</u> about <u>G1,</u> 2026. Accessed: Jan. 9, 2026. 

- [34] Huayi Wang, Zirui Wang, Junli Ren, Qingwei Ben, Tao Huang, Weinan Zhang, and Jiangmiao Pang. Beamdojo: Learning agile humanoid locomotion on sparse footholds. _arXiv preprint arXiv:2502.10363_ , 2025. 

- [35] Liuyi Wang, Xinyuan Xia, Hui Zhao, Hanqing Wang, Tai Wang, Yilun Chen, Chengju Liu, Qijun Chen, and Jiangmiao Pang. Rethinking the embodied gap in visionand-language navigation: A holistic study of physical and visual disparities. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 9455–9465, 2025. 

- [36] Zifan Wang, Teli Ma, Yufei Jia, Xun Yang, Jiaming Zhou, Wenlong Ouyang, Qiang Zhang, and Junwei Liang. Omni-perception: Omnidirectional collision avoidance for legged locomotion in dynamic environments. _arXiv preprint arXiv:2505.19214_ , 2025. 

- [37] Meng Wei, Chenyang Wan, Jiaqi Peng, Xiqian Yu, Yuqiang Yang, Delin Feng, Wenzhe Cai, Chenming Zhu, Tai Wang, Jiangmiao Pang, et al. Ground slow, move fast: A dual-system foundation model for generalizable vision-and-language navigation. _arXiv preprint_ 

_arXiv:2512.08186_ , 2025. 

- [38] Haoyang Weng, Yitang Li, Nikhil Sobanbabu, Zihan Wang, Zhengyi Luo, Tairan He, Deva Ramanan, and Guanya Shi. Hdmi: Learning interactive humanoid whole-body control from human videos. _arXiv preprint arXiv:2509.16757_ , 2025. 

- [39] Jiahao Xiao, Jianbo Zhang, BoWen Yan, Shengyu Guo, Tongrui Ye, Kaiwei Zhang, Zicheng Zhang, Xiaohong Liu, Zhengxue Cheng, Lei Fan, et al. Static and plugged: Make embodied evaluation simple. _arXiv preprint arXiv:2508.06553_ , 2025. 

- [40] Wei Xu and Fu Zhang. Fast-lio: A fast, robust lidarinertial odometry package by tightly-coupled iterated kalman filter. _IEEE Robotics and Automation Letters_ , 6(2):3317–3324, 2021. 

- [41] Haoru Xue, Xiaoyu Huang, Dantong Niu, Qiayuan Liao, Thomas Kragerud, Jan Tommy Gravdahl, Xue Bin Peng, Guanya Shi, Trevor Darrell, Koushil Sreenath, et al. Leverb: Humanoid whole-body control with latent visionlanguage instruction. _arXiv preprint arXiv:2506.13751_ , 2025. 

- [42] Fan Yang, Per Frivik, David Hoeller, Chen Wang, Cesar Cadena, and Marco Hutter. Spatially-enhanced recurrent memory for long-range mapless navigation via end-toend reinforcement learning. _The International Journal of Robotics Research_ , page 02783649251401926, 2025. 

- [43] Wenbo Zhang, Tianrun Hu, Yanyuan Qiao, Hanbo Zhang, Yuchu Qin, Yang Li, Jiajun Liu, Tao Kong, Lingqiao Liu, and Xiao Ma. Chain-of-action: Trajectory autoregressive modeling for robotic manipulation. _arXiv preprint arXiv:2506.09990_ , 2025. 

- [44] Duo Zheng, Shijia Huang, Lin Zhao, Yiwu Zhong, and Liwei Wang. Towards learning a generalist model for embodied navigation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13624–13634, 2024. 

- [45] Gengze Zhou, Yicong Hong, and Qi Wu. Navgpt: Explicit reasoning in vision-and-language navigation with large language models. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 38, pages 7641–7649, 2024. 

- [46] Pengfei Zhou, Liliang Chen, Shengcong Chen, Di Chen, Wenzhi Zhao, Rongjun Jin, Guanghui Ren, and Jianlan Luo. Act2goal: From world model to general goalconditioned policy. _arXiv preprint arXiv:2512.23541_ , 2025. 

- [47] Yin Zhou and Oncel Tuzel. Voxelnet: End-to-end learning for point cloud based 3d object detection. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 4490–4499, 2018. 

- [48] Shaoting Zhu, Linzhan Mou, Derun Li, Baijun Ye, Runhan Huang, and Hang Zhao. Vr-robo: A real-tosim-to-real framework for visual robot navigation and locomotion. _IEEE Robotics and Automation Letters_ , 2025. 

