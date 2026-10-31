---
title: "Omnidirectional Humanoid Locomotion on Stairs via Unsafe Stepping Penalty and Sparse LiDAR Elevation Mapping"
date: "2026-03-09"
authors: "Yuzhi Jiang; Yujun Liang; Junhao Li; Han Ding; Lijun Zhu"
url: https://arxiv.org/abs/2603.07928
pdf: https://arxiv.org/pdf/2603.07928
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.07928)** / [論文ページ](https://arxiv.org/abs/2603.07928)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Omnidirectional Humanoid Locomotion on Stairs via Unsafe Stepping Penalty and Sparse LiDAR Elevation Mapping** 

Yuzhi Jiang<sup>1</sup> , Yujun Liang<sup>1</sup> , Junhao Li<sup>1</sup> , Han Ding<sup>2</sup><sup>_,_3</sup> , Lijun Zhu<sup>1</sup><sup>_,_2</sup><sup>_,_†</sup> 

**_Abstract_ — Humanoid robots, characterized by numerous degrees of freedom and a high center of gravity, are inherently unstable. Safe omnidirectional locomotion on stairs requires both omnidirectional terrain perception and reliable foothold selection. Existing methods often rely on forward-facing depth cameras, which create blind zones that restrict omnidirectional mobility. Furthermore, sparse post-contact unsafe stepping penalties lead to low learning efficiency and suboptimal strategies. To realize safe stair-traversal gaits, this paper introduces a single-stage training framework incorporating a dense unsafe stepping penalty that provides continuous feedback as the foot approaches a hazardous placement. To obtain stable and reliable elevation maps, we build a rolling point-cloud mapping system with spatiotemporal confidence decay and a self-protection zone mechanism, producing temporally consistent local maps. These maps are further refined by an Edge-Guided Asymmetric U-Net (EGAU), which mitigates reconstruction distortion caused by sparse LiDAR returns on stair risers. Simulation and real-robot experiments show that the proposed method achieves a near-100% safe stepping rate on stair terrains in simulation, while maintaining a remarkably high safe stepping rate in real-world deployments. Furthermore, it completes a continuous long-distance walking test on complex outdoor terrains, demonstrating reliable sim-to-real transfer and longterm stability.** 

## I. INTRODUCTION 

Humanoid robots, with their anthropomorphic morphology and versatile motion capabilities, hold significant potential for deployment in unstructured environments such as domestic service, post-disaster rescue, and industrial inspection. Compared with quadrupedal robots, however, humanoids exhibit a higher center of gravity and larger foot soles, presenting serious balance and stability challenges when traversing rough terrain [1]. 

Reinforcement-learning-based methods have made significant progress in robust locomotion control across complex environments [2]. Early blind-walking policies that rely solely on proprioception perform well on flat ground but are largely ineffective on terrain with pronounced height variations such as tall stair steps [3]. To overcome this limitation, external perceptive information must be incorporated. Common approaches typically mount a depth camera on the robot head to construct a depth map as the network input. Such a 

> †Corresponding author. 

> 1School of Artificial Intelligence and Automation, Huazhong University of Science and Technology, Wuhan 430074, China. {yzjiang, andrew, junhaoli, ljzhu}@hust.edu.cn 

> 2State Key Laboratory of Intelligent Manufacturing Equipment and Technology, Huazhong University of Science and Technology, Wuhan 430074, China. dinghan@mail.hust.edu.cn 

> 3School of Mechanical Science and Engineering, Huazhong University of Science and Technology, Wuhan 430074, China. 


Fig. 1. Overview of the proposed omnidirectional perceptive locomotion framework deployed on the Unitree G1 humanoid robot. The robot safely performs omnidirectional stair traversal in both indoor and outdoor settings, including forward ascent (a), (c), lateral ascent (b), and backward ascent (d). Orange arrows indicate the direction of motion, and the teal overlay on the stairs illustrates the real-time reconstructed elevation map. 

forward-facing camera, however, has a limited field of view that leaves substantial lateral and rear blind zones, preventing the robot from traversing complex terrain during sideways or backward motion. Moreover, depth images from such cameras are susceptible to illumination changes and motion blur, undermining policy robustness. 

Guiding the robot toward safe foothold selection requires carefully designed reward functions. Conventional unsafestepping penalties are sparse: punishment is applied only after a physical collision or an edge contact has already occurred [4], [5]. Such delayed feedback fails to steer the policy toward precise foot placements, resulting in slow convergence or overly conservative suboptimal strategies. 

To address these challenges, this paper proposes a singlestage omnidirectional perceptive locomotion framework for humanoid robots. To tackle the unsafe-stepping problem, we introduce a dense unsafe stepping penalty comprising a foot-collision term and an edge-contact term, both of which provide continuous negative feedback before a hazardous footstep occurs. This dense reward signal effectively guides the policy to adjust foot placements proactively. To address the perception blind-zone problem, we employ LiDAR to 

construct a robot-centric elevation map whose omnidirectional coverage significantly mitigates the field-of-view limitation, enabling confident lateral and backward movements. 

In summary, the main contributions of this paper include: 

- A dense reward function is proposed that imposes continuous penalties before foot-collision and edgestepping events, substantially improving both the safe stepping rate and learning efficiency on complex terrain. 

- A perceptive architecture is developed that integrates point-cloud-based rolling mapping with an Edge-Guided Asymmetric U-Net (EGAU), effectively addressing the feature reconstruction distortion caused by extremely sparse onboard point clouds and physical blind zones. 

- Validation across a continuous 407.9-meter outdoor trajectory and diverse stair configurations demonstrates the method’s capability in omnidirectional traversal and sim-to-real transfer. 

## II. RELATED WORK 

Deep reinforcement learning has become the dominant paradigm for locomotion control of legged robots on complex terrain. Early proprioceptive approaches achieve stable walking on flat ground but perform poorly on discontinuous terrain such as stairs, where external terrain perception becomes essential. Many studies use forward-facing depth cameras to obtain depth maps of the frontal terrain [6]–[11]. To reduce the difficulty of learning directly from high-dimensional observations, teacher-student architectures are commonly adopted [12]–[15]. Two-stage distillation, however, is prone to information loss [9], and the student policy often passively mimics the teacher output, thereby limiting robustness. Depth maps also exhibit a considerable sim-to-real gap that demands additional image processing, and the forward-only field of view restricts both lateral and backward mobility. 

To provide richer perceptive information, numerous studies feed elevation maps into the policy [4], [16]–[19]. Classical probabilistic mapping, as represented by Fankhauser et al. [20], suffers from stale observations and step-edge melting when confronted with the extremely sparse and chronically occluded point clouds produced by onboard LiDAR. Subsequent research introduces learning-based perception modules such as VAE-based denoising [18] or hybrid internal models [16] to improve robustness. As a leading recent work in blind-zone reconstruction, Song et al. [21] utilize a standard multi-task U-Net. However, the late-branching design lacks explicit geometric priors during progressive decoding and tends to lose critical step-edge features when filling sparse holes. In contrast, our framework systematically addresses this perception challenge: a rolling point-cloud map with spatiotemporal confidence decay and a protectionzone mechanism preserves historical observations in blind regions, while EGAU explicitly injects geometric boundary priors to block cross-edge smooth interpolation, producing high-quality omnidirectional elevation maps with accurate step-edge features for safe omnidirectional locomotion. 

Avoiding unsafe foot placements when traversing complex terrain is critical. Prior work has proposed various constraint 

mechanisms: Zhuang et al. [5] penalize the deviation between actual and ideal foothold centers; Zhang et al. [4] apply penalties when sampled points on the foot sole lack terrain support; He et al. [2] implicitly guide foothold selection through attention mechanisms. While promising, these methods either generalize poorly across different terrains or fail to provide explicit constraints for safe foothold selection. Building on these methods, we propose a dense unsafe stepping penalty. Unlike post-contact penalties, the proposed penalty provides continuous negative feedback before hazardous contact occurs, guiding the policy toward safe foot placements and substantially improving both the safety and learning efficiency of omnidirectional locomotion. 

## III. METHODS 

Fig. 2 illustrates the overall pipeline of the proposed framework, which consists of a simulation training stage and a real-world deployment stage. The following subsections describe each component in detail. 

## _A. Simulation Training_ 

Owing to the limitations of onboard sensors, the robot cannot access the complete ground-truth state of itself or the surrounding environment. We therefore formulate the reinforcement learning problem as a Partially Observable Markov Decision Process (POMDP), described by the tuple _M_ = _⟨S, A, P, O, r, γ⟩_ , where _S_ and _A_ denote the continuous full state and action spaces, respectively, and _O_ denotes the partial observation space. The transition dynamics are _P_ ( **s** _t_ +1 _|_ **s** _t ,_ **a** _t_ ), the reward function is _r_ ( **s** _t ,_ **a** _t_ ) and _γ ∈_ [0 _,_ 1) is the discount factor. The objective is to optimize a policy _πφ_ ( **a** _t |_ **s** _t_ ) that maximizes the expected discounted return: 


In this work, we train the actor-critic network using Proximal Policy Optimization (PPO) [22]. 

_1) Policy Network:_ The policy network maps robot observations to the action space. The input consists of two components: the proprioceptive observation **o** _t_ and a history of elevation maps **e** _t−h_ : _t_ . The proprioceptive observation **o** _t_ is a vector obtained directly from sensors, defined as: 


This vector comprises the base angular velocity _ωt_ , the gravity projection in the body frame **g** _t_ , the linear velocity command **c** _t_ , the joint positions _θ t_ , the joint velocities _θ_<sup>˙</sup> _t_ , and the previous action **a** _t−_ 1. The perceptive history **e** _t−h_ : _t_ corresponds to a robot-centric local elevation map of size 1 _._ 4 m _×_ 1 _._ 0 m at a resolution of 0 _._ 05 m, which is obtained directly from Isaac Lab and formed by stacking _h_ consecutive frames. We set _h_ = 5 throughout this work. For the network architecture, the low-dimensional proprioceptive observation **o** _t_ is processed by a Multilayer Perceptron (MLP), while the elevation map **e** _t−h_ : _t_ is processed by a Convolutional Neural Network (CNN). The two resulting feature vectors are concatenated and fed into the actor head, which outputs the action **a** _t_ . 


Fig. 2. Overview of the proposed framework. (A) Simulation training: an MLP and a CNN extract proprioceptive and perceptive features, respectively, which are then concatenated. Meanwhile, an unsafe foot penalty function guides the policy to learn safe stair-traversal gaits. (B) Real-world deployment: the trained policy network is directly transferred to the real robot, with a point-cloud mapping and edge-guided elevation map module providing stable and accurate elevation map inputs. 

_2) Critic Network:_ The critic network estimates the value function _V_<sup>ˆ</sup> _t_ to guide the policy update. Its input likewise consists of two components: a privileged proprioceptive observation **s** _t_ and noise-free historical elevation maps **e** _t_<sup>_∗_</sup> _−h_ : _t_<sup>.</sup> Compared with the policy input **o** _t_ , the privileged observation **s** _t_ additionally includes the ground-truth base linear velocity **v** _t_ . The critic network uses the same network architecture as the policy network and outputs the estimated value _V_<sup>ˆ</sup> _t_ . 

_3) Action Space:_ The action space _A_ consists of relative target positions for the robot’s joint motors. We define _θ_ def as the joint positions in which the robot stands stably. The policy output **a** _t_ is added to _θ_ def to form the desired joint positions _θ_ des = _θ_ def + **a** _t_ , which are then converted to joint torques _τ_ through a PD controller: 


TABLE I 

REWARD FUNCTION TERMS 

|**Name**|**Expression**|**Weight**|
|---|---|---|
|Linear Vel. Tracking|exp(_−_4_∥_**v**_xy −_**v**<sup>cmd</sup><br>_xy _<sup>_∥_2)</sup><br><br>|5_._0|
|Angular Vel. Tracking|exp(_−_4_∥ωz −ω_<sup>cmd</sup><br>_z_<br>_∥_<sup>2</sup>)<br>|5_._0|
|Base Height|exp(_−_400_∥h−h_tar_∥_<sup>2</sup>)|1_._0|
|Feet Air Time|1**c**_i_=1_·_min(_t_air_,t_c_,_1_._0)|7_._0|
|Base Lin. Vel. Z|_−∥_**v**_z∥_<sup>2</sup><br>|_−_1_._0|
|Base Ang. Vel. XY|_−∥ωxy∥_<sup>2</sup><br>|_−_0_._05|
|Base Orientation|_−∥_**g**_∥_<sup>2</sup>|_−_6_._0|
|Joint Action Rate|_−∥_˙**a**_t∥_<sup>2</sup>|_−_0_._01|
|Joint Action Smooth|_−∥_¨**a**_t∥_<sup>2</sup>|_−_0_._01|
|Joint Acceleration|_−∥_<sup>¨</sup>_θ∥_<sup>2</sup><br>|_−_1_e_<sup>_−_6</sup>|
|Joint Torques|_−∥τ∥_<sup>2</sup>|_−_0_._2|
|Feet Slide|∑_i∈_feet1**c**_i_=1_∥_**v**_i,xy∥_<sup>2</sup><br>|_−_0_._1|
|Joint Deviation|_−_∑_j ∥θj −θ_nom_,j∥_<sup>2</sup>|_−_0_._5|
|Termination|1(terminate)|_−_250_._0|
|Unsafe stepping|Eq. (10)|1_._0|


where **k** p and **k** d are the proportional and derivative gains. 

_4) Reward Function:_ The reward function is designed to promote robust locomotion while minimizing unsafe behavior. Table I lists all reward terms used in training, where **c** _i_ indicates that the _i_ -th foot has made contact with the terrain. The total reward is a weighted sum of the individual terms. 

The last entry in the table, labeled Unsafe stepping, corresponds to our proposed unsafe stepping penalty function. When a humanoid robot traverses stairs, we define hazardous foot placement as comprising two primary types: collision between the foot and the stair riser, and landing on the step edge such that more than 50% of the foot sole is suspended. Existing safety constraints are typically based on physical collision detection, producing sparse reward signals that activate only after the foot has already collided or fully landed, leading to poor training outcomes. To provide continuous guidance before a hazardous step occurs, we design a dense unsafe stepping penalty. This penalty is equally applicable to 

other terrain types such as slopes and ditches, enabling the policy to be trained with a unified reward function across all terrain configurations. 

For the foot-collision term (left side of Fig. 3), the penalty magnitude increases as the foot approaches an obstacle at higher speed. We first obtain the foot velocity vector **v** _xy_ (red arrow) in the XY plane, then find the nearest obstacle vector **d** _xy_ (blue arrow) within a 30<sup>_◦_</sup> cone centered on **v** _xy_ . The collision penalty base value _p_ colli is computed as: 


When the foot is far from a step, no penalty should be applied. We therefore introduce a safety distance term: 


Fig. 3. Illustration of the proposed dense unsafe stepping penalty. The left panel depicts the foot-collision penalty computation, and the right panel depicts the edge-stepping penalty computation. 

where _d_ unsafe is the distance threshold below which the penalty takes effect. To distinguish stairs from ordinary slopes, we compute the terrain slope _s_ at the endpoint of **d** _xy_ . When _s_ falls below a threshold _ε_ slope, the surface is classified as a slope and no penalty is applied. The total foot-collision penalty _r_ colli is defined as: 


For the edge-stepping term (right side of Fig. 3), the penalty magnitude similarly increases as the foot approaches a step edge at higher speed. We first obtain the local elevation map directly beneath the foot and compute the gradient magnitude **G** = _∥_ ∇ **H** fl _∥_ 2 using a Sobel operator. Points whose gradient magnitude exceeds a threshold are marked as edge points **e** _i_ . We then compute the geometric centroid **e** c (midpoint of the green line in the figure) of all edge points and construct the vector **e** _xy_ (blue arrow) from the foot center **f** c to the edge centroid **e** c. Taking the current linear velocity command **v**<sup>cmd</sup> xy (red arrow), the edge penalty _p_ edge is: 


Because the sign of _p_ edge must reverse depending on the traversal direction, we introduce the sign correction factor _s f_ = _−_ sgn( **g** _·_ **v**<sup>cmd</sup> xy<sup>), where</sup><sup>**g**is the local mean gradient vector.</sup> Under this formulation, when the robot ascends stairs, a negative _p_ edge results if the edge lies under the front half of the foot, which acts as a valid penalty. Conversely, if the edge lies under the rear half, _p_ edge equals zero, applying no penalty. We further introduce a height weighting term: _d_ edge = max(0 _,_ 1 _−_<sup>**d**</sup><sup>_z_</sup> ) (8) _d_ min where **d** _z_ is the vertical distance from the foot to the ground and _d_ min is the minimum height threshold below which the penalty becomes active. The final edge-stepping penalty _r_ edge is: 


If no edge points are detected in the local elevation map, _r_ edge is set to zero. 

When the stair tread is narrow, the robot may need to step on the edge to avoid riser collision. We therefore define the 

final unsafe stepping penalty _r_ safe as a weighted sum of the two terms: 


where _w_ 1 and _w_ 2 are the respective weighting coefficients. 

_5) Terrain Curriculum:_ To enable the policy to progressively advance from simple tasks to complex terrains, we employ a terrain curriculum during training. When the robot successfully completes the task at a given difficulty level, it is promoted to the next level; otherwise, it is demoted. We define 10 difficulty levels in total. 

The terrain types include stairs, slopes, and flat ground. Stair terrain is divided into ascending and descending variants, with tread depths uniformly sampled from [0 _._ 25 _,_ 0 _._ 6] m and step heights from [0 _,_ 0 _._ 23] m. Slope terrain includes ascending and descending configurations with slope angles from [0 _,_ 0 _._ 4] rad. The difficulty parameters of all sub-terrains increase linearly with the curriculum level. 

## _B. Edge-Guided Elevation Map Reconstruction_ 

To obtain high-frequency elevation maps that preserve precise geometric features, we propose an edge-guided reconstruction framework that operates on sparse point cloud inputs. 

_1) Spatiotemporal Rolling Mapping and Sparse Rasterization:_ To acquire continuous and stable terrain features in unstructured environments, we construct a spatiotemporal rolling map from point clouds in the odometry frame _O_ . Naive accumulation of observations readily produces terrain ghosting artifacts because of environmental dynamics and local drift of the odometry. We therefore introduce a temporal confidence decay mechanism that progressively filters out aging point clouds. However, conventional timeout-based decay [20] exhibits a critical perception flaw for humanoid robots. When the robot steps in place or performs slow and delicate maneuvers, the historical memory of the terrain within the physical blind zone beneath the body of the robot (the red region in Fig. 4) is erroneously discarded upon expiration. 

To guarantee safe foot placement during backward and lateral omnidirectional motion, we propose an egocentric protection zone mechanism. When valid points fall within the cylindrical space _Z_ safe directly beneath the base of the robot, the temporal confidence of these points is locked to the maximum value (the dark red points in the blue region of Fig. 4). This mechanism prevents the loss of critical terrain memory beneath the body, thereby providing highly reliable constraints of the physical support surface for omnidirectional locomotion. 

For map maintenance and local feature extraction, we adopt an asynchronous decoupled architecture operating at two frequencies. We maintain a robot-centric global map of point clouds, which undergoes incremental spatial fusion and confidence updates at a lower rate (10 Hz). To satisfy the high-frequency control loop, the state extraction module constructs a robot-centric local point-cloud map at a rate of no less than 50 Hz. Specifically, based on the real-time body pose of the robot, we transform the relevant points from the 


Fig. 4. Illustration of the spatiotemporal rolling mapping and the protection zone mechanism. The colors of the point cloud indicate temporal confidence levels. The red conical region represents the physical blind zone of the LiDAR, and the light blue cylinder denotes the self-protection zone _Z_ safe constructed beneath the base of the robot. 

global map into the foot frame _F_ and crop a local region of 1 _._ 4 m _×_ 1 _._ 0 m. This region is then rasterized in 2.5D, yielding an initial sparse pointcloud map at a resolution of 0.05 m alongside a mask of invalid cells, which jointly serve as the raw input to the subsequent reconstruction network. 

_2) Edge-Guided Asymmetric Reconstruction Network:_ To achieve accurate reconstruction of elevation maps from the sparse rasterized local maps described above, we propose the EGAU architecture. This network employs a featurecascaded design with a single encoder and dual decoders. This design explicitly injects geometric boundary priors during the progressive recovery of spatial resolution, thereby overcoming the over-smoothing effect inherent in linear interpolation. 

Let _i ∈{_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ denote the spatial resolution level of the decoding stage, where _i_ = 1 corresponds to the bottleneck with the lowest resolution and _i_ = 4 corresponds to the output at the original resolution. At the _i_ -th level, the feature map of the height decoding stream **F**<sup>(</sup> h<sup>_i_)</sup> is computed as: 


where _D_<sup>(</sup><sup>_i_)</sup> h<sup>(</sup><sup>_·_)denotestheheight-streamdecoderatlevel</sup><sup>_i_;</sup> [ _·, ·_ ] denotes the concatenation; **F** enc<sup>(</sup><sup>_i_)istheskip-connection</sup> feature from the corresponding level of the encoder; and _U_ ( _·_ ) represents the bilinear upsampling operation. Crucially, the hidden features **F**<sup>(</sup> edge<sup>_i_)extractedbytheedge</sup> decoding stream at the same level are explicitly injected into the height decoding stream through a feature alignment function Φ( _·_ ). This cascaded topology enables the edge stream to continuously supply strong geometric boundary priors to the height stream during the layer-by-layer decoding process, which effectively suppresses the cross-edge smooth interpolation caused by sparse inputs. 

_3) Region-Decoupled Hybrid Loss:_ Under sparse inputs of point clouds, a globally uniform regression loss is insufficient 

for accurately recovering the physical structures of the terrain. To address this limitation, we propose a fine-grained RegionAware Loss: 


We first compute the gradient magnitude **M** gt = _∥_ ∇ **H** gt _∥_ 2 of the ground-truth elevation map by applying a Sobel operator, and we derive the edge mask **M** edge and the flat-region mask **M** flat from **M** gt. In addition to the standard global height regression loss _L_ h and the edge classification loss _L_ e adopted from the baseline [21], we introduce three region-specific penalties. 

First, the Edge-aware Regression Loss _L_ r imposes an additional L1 penalty within **M** edge to correct the height collapse at step edges. Second, the Smoothness Loss _L_ s operates exclusively in flat regions ( **M** flat) and suppresses high-frequency noise from sparse interpolation through a combined L1 and L2 penalty on first-order differences. Third, the Adaptive Gradient Loss _L_ g is defined as: 


where **M** pred represents the gradient magnitude of the reconstructed elevation map. Through the adaptive amplification coefficient _α_ , the network is explicitly constrained to fit physical right angles in regions where the ground-truth gradient is steep. 

To bridge the perception gap between simulation and reality, we incorporate a physics-based sensor noise model into the simulation data generation pipeline. Due to the frequent loss of return signals in real solid-state LiDAR at large incidence angles (e.g., stair risers), we apply a ray-drop mechanism in the simulation conditioned on the local terrain gradient. This targeted blind-zone simulation forces the network to accommodate the severely incomplete point-cloud inputs encountered during deployment, substantially enhancing realworld robustness. 

## IV. RESULTS 

We conduct simulation and real-robot experiments to validate the proposed method. In simulation, we independently evaluate the reinforcement learning locomotion policy and the elevation map reconstruction module. In the real-world experiments, the trained policy is directly deployed on a physical robot that uses the elevation map module for terrain perception in both indoor and outdoor settings. The following subsections present the experimental setup, results, and analysis. 

## _A. Experimental Setup_ 

The locomotion policy is trained in Isaac Lab using a single NVIDIA RTX 4090 GPU. The robotic platform used in this paper is the Unitree G1 humanoid robot, which has 29 degrees of freedom and is capable of executing complex whole-body motions. For perception, a Livox Mid-360 LiDAR mounted on the head of the robot provides a 360<sup>_◦_</sup> _×_ 59<sup>_◦_</sup> field of view with point clouds. During real-world experiments, 


Fig. 5. Comprehensive performance comparison in simulation. (a) Safe stepping rate as a function of stair height for each method. The top row corresponds to forward, backward, and lateral stair ascent, while the bottom row shows the corresponding descent results. (b) Terrain curriculum level progression over the course of training. (c) Forward linear velocity tracking when ascending 15-cm stairs with a commanded velocity of 0.7 m/s. 

both the RL controller and the elevation map module run on the onboard NVIDIA Jetson Orin NX edge computing platform. The odometry used in our experiments is provided by DLIO [23], which outputs reliable odometry information at 100 Hz. The RL controller operates at 50 Hz. 

To comprehensively evaluate the framework, the simulation assessment proceeds along two lines: ablation and comparison experiments for the locomotion policy and the elevation map reconstruction module. For the locomotion policy comparison, we design four experimental groups: 

- **Naive** : Uses the default humanoid training framework provided by Isaac Lab. This baseline employs a simple MLP and does not incorporate the unsafe stepping penalty. 

- **Ours w/o penalty** : Adopts the network architecture proposed in this paper but excludes the unsafe stepping penalty. 

- **PIM** [16]: A single-stage perceptive locomotion policy for humanoid robots that uses elevation maps as perceptive input and trains the network with a hybrid internal model. 

- **Ours** : The complete proposed method, which augments Ours w/o penalty with the unsafe stepping penalty. 

The ablation setup and evaluation metrics for the perception reconstruction module are detailed in Section IV-B.2. 

_B. Simulation Experiments_ 

_1) Locomotion Policy Experiments:_ We evaluate the overall performance of each method in simulation, including the safe stepping rate, terrain curriculum training curves, and velocity tracking performance, as shown in Fig. 5. 

We examine the safe stepping performance of each method when ascending and descending stairs in different directions, as shown in Fig. 5(a). The linear velocity command is set to 0.7 m/s for forward and backward traversal and 0.5 m/s for lateral traversal. The safe stepping rate is defined as the number of non-hazardous steps divided by the total number of steps. Naive, owing to the simple network structure, fails to learn from the large volume of perceptive information, and the success rate drops as the stair height increases. Both PIM and Ours w/o penalty can traverse stairs exceeding 25 cm in height; however, without the unsafe stepping penalty, these policies tend to adopt aggressive gaits that disregard foot placement safety, resulting in frequent collisions with stair risers and landings on step edges. Although such aggressive strategies enable the robot to pass extremely challenging stairs in simulation, they severely compromise deployment safety on a physical robot, where a single hazardous footstep can cause hardware damage or a fall. In contrast, benefiting from the proposed unsafe stepping penalty, Ours learns to lift the feet cautiously and select safe footholds. Although it does not pass certain tests under extreme difficulty settings, it achieves a near-100 % safe stepping rate across all passable terrains, significantly outperforming all other methods. Such a high safe stepping rate is crucial for real-world deployment. This confirms that the proposed unsafe stepping penalty effectively guides the policy to traverse stair terrains safely. Notably, in some experiments the unsafe stepping rate on lower stairs is higher than on taller ones. This is because the policy perceives lower steps as less hazardous and consequently tolerates landing closer to the step edge. 

Fig. 5(b) shows the terrain level progression over 12k training iterations. Naive rises quickly in terrain level during early 


Fig. 6. Real-world experimental results. (A) The robot traverses stairs in an indoor environment: (a) forward ascent, (b) forward descent, (c) backward descent, and (d) lateral descent. (B) The robot performs long-distance outdoor walking, successfully traversing downhill slopes, flat ground, and stairs. The upper-left inset in each robot image displays the raw elevation map (black dots indicate missing data holes), while the lower-left inset shows the elevation map processed by the proposed reconstruction network. 

training owing to the simple architecture, but performance degrades severely as terrain difficulty increases, indicating that a simple MLP alone cannot extract effective terrain features from elevation maps. Ours w/o penalty, which introduces a CNN for elevation map processing, achieves a substantial improvement in performance, reaching approximately level 6 around iteration 4000 and remaining stable thereafter. PIM exhibits considerably slower learning, reaching only about level 3.5 by the end of 12k iterations, likely because the implicit representation learning strategy is inefficient for this complex terrain task. Ours demonstrates the best learning efficiency throughout training, reaching the highest terrain level first at around iteration 3000. This result confirms that the proposed unsafe stepping penalty enables the policy to acquire stair-traversal skills more rapidly. 

Finally, Fig. 5(c) presents the linear velocity tracking performance on 15-cm stairs in the forward direction. Given a target velocity of 0.7 m/s, both Ours and Ours w/o penalty track the reference smoothly and accurately. Naive fails to reach the target velocity, and PIM exhibits significant overshoot. This further confirms that the proposed method maintains excellent velocity tracking accuracy while achieving safe foot placement. 

_2) Elevation Map Reconstruction Experiments:_ To validate the effectiveness of the EGAU architecture and the regionaware loss under conditions with sparse point clouds, ablation experiments are conducted in simulation (see Table II). All experiments retain the base losses _Lh_ and _Le_ . In addition to the global mean squared error (G-MSE), the edge mask **M** _edge_ and the flat-region mask **M** _flat_ are utilized to compute the edge mean absolute error (E-MAE) and the flat-region mean absolute error (F-MAE), respectively. Furthermore, the mean spatial gradient of the reconstructed elevation map within flat regions is reported as the flat-region roughness (F-Rgh). This metric provides a comprehensive assessment regarding 

the capability of the model to preserve step structures and suppress noise within flat areas. 

TABLE II 

ABLATION RESULTS FOR THE RECONSTRUCTION NETWORK AND THE LOSS FUNCTIONS 

|**Net**|_Lr_|**Loss**<br>_Ls_|_Lg_|**G-MSE** _↓_<br>(_×_10<sup>_−_4</sup>)|**E-MAE** _↓_<br>(_×_10<sup>_−_2</sup>)|**F-MAE** _↓_<br>(_×_10<sup>_−_3</sup>)|**F-Rgh** _↓_<br>(_×_10<sup>_−_2</sup>)|
|---|---|---|---|---|---|---|---|
|Baseline||||2.05|1.32|5.57|2.57|
|EGAU||||1.99|1.18|5.89|2.26|
|EGAU|✓|||1.54|0.93|5.58|2.36|
|EGAU|✓|✓||1.46|0.87|5.41|1.87|
|EGAU|✓|✓|✓|**1.23**|**0.75**|**4.24**|**1.32**|


Table II presents the quantitative ablation results concerning the network architecture and the loss functions. The full model, which integrates the EGAU architecture with all region-decoupled losses, achieves the highest performance across all evaluation metrics. The baseline method, which adopts a late-branching U-Net [21], yields the highest errors at the step edges. This observation indicates that standard architectures tend to over-smooth geometric boundaries when provided with sparse inputs. The introduction of the EGAU explicitly mitigates this issue by injecting edge boundary priors, which notably reduces the E-MAE. 

Furthermore, the progressive addition of the region-aware losses targets specific reconstruction artifacts. Specifically, the edge-aware regression loss _Lr_ corrects the absolute height collapse at step edges, while the smoothness loss _Ls_ strictly suppresses high-frequency noise in flat areas, as reflected by a significant reduction in the F-Rgh. Finally, the adaptive gradient loss _Lg_ explicitly penalizes gradient distortions to preserve sharp discontinuities. These results demonstrate that the explicit injection of edge features and the application of region-specific loss constraints fulfill complementary roles in generating accurate and coherent height maps. 

## _C. Real-World Experiments_ 

The complete perception model is executed on an onboard NVIDIA Jetson Orin NX computing platform via Onnxruntime-GPU. With a compact model size comprising only 2.76 M parameters, the network maintains a stable singleframe inference latency of 2 ms. This high efficiency ensures that the reconstruction module easily satisfies the 50 Hz control loop requirement without competing for computational resources with the reinforcement learning controller. 

As shown in Figs. 1 and 6(A), we evaluate the ability of the robot to traverse standard stairs (height 15 cm, tread width 20 cm) in different directions. Owing to the simulated ray-drop mechanism, the reconstruction network demonstrates strong robustness to real sensor noise. Guided jointly by the high-quality omnidirectional elevation map and the dense unsafe stepping penalty function, the robot maintains stable gaits across forward, lateral, and backward traversals. By consistently avoiding edge stepping and riser collisions, these results strongly validate the effectiveness of the proposed framework for safe foot placement in real-world deployment. 

To verify the performance and stability of the proposed method during long-term motion in outdoor environments, we conducted a continuous, uninterrupted outdoor walking experiment exceeding 400 meters, which was eventually terminated manually, see Fig. 6(B). Starting from a hillside, the robot traversed a sequence of terrains including a downhill slope, flat ground, and stairs (both ascending and descending). Throughout the entire process, the robot maintained a stable gait and safe foot placement, remaining unaffected by surrounding pedestrians and vehicles. These results demonstrate that the proposed method possesses excellent stability and is capable of long-term operation in complex outdoor environments. 

## V. CONCLUSIONS 

This paper presents a robust framework for safe omnidirectional humanoid stair traversal. A dense unsafe stepping penalty provides continuous feedback to guide foot placement, significantly enhancing safety and learning efficiency. Additionally, our LiDAR-based mapping with edge-guided reconstruction substantially reduces the impact of blind zones, yielding consistent terrain geometry. Zero-shot simto-real experiments on the Unitree G1 confirm reliable omnidirectional mobility on indoor stairs and complex outdoor terrains. 

Despite these promising results, this work has certain limitations. The use of omnidirectional 2.5D elevation maps restricts the representation of ditches and similar terrains, and sensorinduced distortions lead to slight performance degradation in real-world deployments compared to simulations. 

## REFERENCES 

- [1] B. Li, W. Zhang, X. Huang, L. Zhu, and H. Ding, “A whole-body disturbance rejection control framework for dynamic motions in legged robots,” _IEEE Robotics and Automation Letters_ , vol. 10, no. 10, pp. 9774–9781, 2025. 

- [3] Z. Zhuang, Z. Fu, J. Wang, C. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” in _Conference on Robot Learning (CoRL)_ , 2023. 

- [4] H. Wang, Z. Wang, J. Ren, Q. Ben, T. Huang, W. Zhang, and J. Pang, “Beamdojo: Learning agile humanoid locomotion on sparse footholds,” _arXiv:2502.10363_ , 2025. 

- [5] Z. Zhuang, S. Yao, and H. Zhao, “Humanoid parkour learning,” in _Conference on Robot Learning, 6-9 November 2024, Munich, Germany_ , vol. 270. PMLR, 2024, pp. 1975–1991. 

- [6] W. Yu, D. Jain, A. Escontrela, A. Iscen, P. Xu, E. Coumans, S. Ha, J. Tan, and T. Zhang, “Visual-locomotion: Learning to walk on complex terrains with vision,” in _Conference on Robot Learning (CoRL)_ , vol. 164. PMLR, 2021, pp. 1291–1302. 

- [7] R. Yang, M. Zhang, N. Hansen, H. Xu, and X. Wang, “Learning vision-guided quadrupedal locomotion end-to-end with cross-modal transformers,” in _The Tenth International Conference on Learning Representations (ICLR)_ , 2022. 

- [8] R. Yang, G. Yang, and X. Wang, “Neural volumetric memory for visual locomotion control,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ . IEEE, 2023, pp. 1430–1440. 

- [9] S. Luo, S. Li, R. Yu, Z. Wang, J. Wu, and Q. Zhu, “PIE: parkour with implicit-explicit learning framework for legged robots,” _IEEE Robotics Autom. Lett._ , vol. 9, no. 11, pp. 9986–9993, 2024. 

- [10] R. Yu, Q. Wang, Y. Wang, Z. Wang, J. Wu, and Q. Zhu, “Walking with terrain reconstruction: Learning to traverse risky sparse footholds,” _arXiv:2409.15692_ , 2024. 

- [11] H. Duan, B. Pandit, M. S. Gadde, B. van Marum, J. Dao, C. Kim, and A. Fern, “Learning vision-based bipedal locomotion for challenging terrain,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 56–62. 

- [12] Z. Zhuang, Z. Fu, J. Wang, C. G. Atkeson, S. Schwertfeger, C. Finn, and H. Zhao, “Robot parkour learning,” in _Conference on Robot Learning (CoRL)_ , vol. 229. PMLR, 2023, pp. 73–92. 

- [13] A. Agarwal, A. Kumar, J. Malik, and D. Pathak, “Legged locomotion in challenging terrains using egocentric vision,” in _Conference on Robot Learning (CoRL)_ , vol. 205. PMLR, 2022, pp. 403–415. 

- [14] X. Cheng, K. Shi, A. Agarwal, and D. Pathak, “Extreme parkour with legged robots,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 11 443–11 450. 

- [15] E. Chane-Sane, J. Amigo, T. Flayols, L. Righetti, and N. Mansard, “Soloparkour: Constrained reinforcement learning for visual locomotion from privileged experience,” in _Conference on Robot Learning (CoRL)_ , vol. 270. PMLR, 2024, pp. 4268–4285. 

- [16] J. Long, J. Ren, M. Shi, Z. Wang, T. Huang, P. Luo, and J. Pang, “Learning humanoid locomotion with perceptive internal model,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 9997–10 003. 

- [17] W. Sun, B. Cao, L. Chen, Y. Su, Y. Liu, Z. Xie, and H. Liu, “Learning perceptive humanoid locomotion over challenging terrain,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2025, pp. 6571–6578. 

- [18] T. Miki, J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter, “Learning robust perceptive locomotion for quadrupedal robots in the wild,” _Sci. Robotics_ , vol. 7, no. 62, 2022. 

- [19] D. Hoeller, N. Rudin, D. V. Sako, and M. Hutter, “Anymal parkour: Learning agile navigation for quadrupedal robots,” _Sci. Robotics_ , vol. 9, no. 88, 2024. 

- [20] P. Fankhauser, M. Bloesch, and M. Hutter, “Probabilistic terrain mapping for mobile robots with uncertain localization,” _IEEE Robotics Autom. Lett._ , vol. 3, no. 4, pp. 3019–3026, 2018. 

- [21] H. Song, H. Zhu, T. Yu, Y. Liu, M. Yuan, W. Zhou, H. Chen, and H. Li, “Gait-adaptive perceptive humanoid locomotion with real-time under-base terrain reconstruction,” _arXiv:2512.07464_ , 2025. 

- [22] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _arXiv:1707.06347_ , 2017. 

- [23] K. Chen, R. Nemiroff, and B. T. Lopez, “Direct lidar-inertial odometry: Lightweight LIO with continuous-time motion correction,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 3983–3989. 

> [2] J. He, C. Zhang, F. Jenelten, R. Grandia, M. Bächer, and M. Hutter, “Attention-based map encoding for learning generalized legged locomotion,” _Sci. Robotics_ , vol. 10, no. 105, 2025. 

