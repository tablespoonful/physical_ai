---
title: "DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving"
date: "2026-03-20"
authors: "Xiaolu Liu; Yicong Li; Song Wang; Junbo Chen; Angela Yao; Jianke Zhu"
url: https://arxiv.org/abs/2603.19675
pdf: https://arxiv.org/pdf/2603.19675
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.19675)** / [論文ページ](https://arxiv.org/abs/2603.19675)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving** 

Xiaolu Liu<sup>1</sup><sup>_,_2</sup> , Yicong Li<sup>2</sup> , Song Wang<sup>1</sup> , Junbo Chen<sup>3</sup> *, Angela Yao<sup>2</sup> , and Jianke Zhu<sup>1</sup><sup>_⋆_</sup> 

> 1Zhejiang University, 2National University of Singapore, 3Udeer.AI {xialuliu, jkzhu}@zju.edu.cn 


**Fig. 1: (a)** Comparisons of perception-based and latent world model-based approaches on nuScenes and NavSim benchmarks. **(b)** Planning visualization on the front view and bird’s-eye-view (BEV) space. Our DynFlowDrive achieves comparable performance. 

**Abstract.** Recently, world models have been incorporated into the autonomous driving systems to improve the planning reliability. Existing approaches typically predict future states through appearance generation or deterministic regression, which limits their ability to capture trajectory-conditioned scene evolution and leads to unreliable action planning. To address this, we propose **DynFlowDrive** , a latent world model that leverages flow-based dynamics to model the transition of world states under different driving actions. By adopting the rectifiedflow formulation, the model learns a velocity field that describes how the scene state changes under different driving actions, enabling progressive prediction of future latent states. Building upon this, we further introduce a stability-aware multi-mode trajectory selection strategy that evaluates candidate trajectories according to the stability of the induced scene transitions. Extensive experiments on the nuScenes and NavSim benchmarks demonstrate consistent improvements across diverse driving frameworks without introducing additional inference overhead. Source code will be available at https://github.com/xiaolul2/DynFlowDrive. 

**Keywords:** Autonomous Driving · Latent World Model · Trajectory Planning 

> _⋆_ Corresponding authors. 

2 X. Liu et al. 

## **1 Introduction** 

End-to-end autonomous driving has emerged as a promising paradigm for building driving systems [3, 7, 10, 18]. Given the data captured by onboard sensors, it aims to predict safe and reliable future trajectories for planning and control [4, 18, 50]. However, trajectory planning is a highly interactive process with the surroundings. A planned trajectory represents the intended action whose safety depends on how the environment responds after it is executed. Therefore, achieving reliable and safe planning requires anticipating future scene evolution, which remains a key challenge for autonomous driving systems. 

To equip the vehicle with such foresight capabilities, a new line of research introduces world models [1, 22] for the end-to-end methods [14, 49]. By enabling action-conditioned future simulations, these approaches allow the system to foresee the consequences of candidate trajectories and anticipate potential risks, thereby supporting safer and more reliable driving decisions. World models mainly follow two approaches: one line of work predicts future scenes explicitly, for example, by generating pixel-level images or 3D occupancy grids [47,56, 58,60]. In contrast, another line of work models the scene prediction of the world in a latent space [24, 55, 62], without explicitly reconstructing the full scenes. 

Despite the advances, existing world models still suffer from critical limitations. For explicit scene-level prediction, many approaches rely on diffusion [12, 40] or autoregressive models [16, 58] to synthesize future observations. While produced visually pleasing results, these methods primarily focus on appearance details such as textures and lighting. The emphasis on high-frequency visual patterns overlooks the underlying geometry and dynamics, which introduces extra computational overhead without improving action-oriented reasoning. 

On the other hand, latent-space world models shift the focus from appearance synthesis to inner features [24, 62]. As illustrated in Figure 2 (a), most works adopt the one-step regression that directly maps the current latent state to the next timestep. Such a static formulation simplifies the prediction as a rigid mapping and neglects the dynamic transition process, making it hard to assess the safety and feasibility of candidate actions. For instance, when a vehicle approaches pedestrians, it may either gradually slow down to yield or maintain speed and brake abruptly at the last moment. Although both actions may lead to a similar stopping position, the underlying scene evolution and safety implications are fundamentally different. Without modeling this transition process, the world model cannot faithfully capture trajectory-dependent dynamics or assess whether the induced evolution is smooth and physically plausible. 

To bridge this gap, we argue that effective world modeling must move beyond discrete endpoint regression and explicitly formulate trajectory-conditioned scene evolution as a continuous dynamical system. Motivated by this, we propose **DynFlowDrive** , a latent world model that leverages flow-based dynamics to model the transition of world states under different driving actions. Specifically, based on the extracted latent features, DynFlowDrive adopts a rectified-flow formulation to model the transition dynamics in latent space and predict future latent states conditioned on the current observation and multiple candidate 

DynFlowDrive 3 


**Fig. 2:** Comparison between **(a)** the existing **static world model** and **(b)** the **dynamic latent world model of our DynFlowDrive** . Instead of the static regression of next-frame latents, we propose the dynamic modeling that learns a continuous velocity field _vθ_ to capture the evolution of world transitions. 

trajectories. The learned velocity field explicitly captures the rate of change of the scene during state transitions, enabling the model to capture how the environment progressively evolves under different driving actions. Building upon the learned flow dynamics, we further introduce the stability-aware multi-mode trajectory selection mechanism. By exploiting the velocity field produced by the flow-based world model, we derive a stability measure that reflects the smoothness of trajectory-conditioned scene transitions. Combined with trajectory error measured with the ground truth and latent reconstruction discrepancy, this dynamics-aware stable criterion enables more reliable planning assessment and trajectory selection for safer autonomous driving systems. 

For evaluation, DynFlowDrive achieves comparable performance on challenging benchmarks, including nuScenes [2] and NavSim [9]. As shown in Figure 1, our method consistently improves planning accuracy for BEV-based and w/o BEV approaches. Without auxiliary tasks, DynFlowDrive is still comparable to perception-based models. In particular, compared with SSR [23], DynFlowDrive reduces the average _L_ 2 displacement error from 0.39m to 0.31m and achieves 88.7 PDMS on NavSim. Our main contributions are summarized as follows: 

- We propose **DynFlowDrive** , a dynamic latent world model that leverages rectified flow to explicitly model dynamic world evolution, enabling the progressive next-frame latent prediction conditioned on candidate trajectories. 

- We introduce the stability-aware multi-mode selection strategy that leverages the flow-based stability for more reliable trajectory selection. 

- Extensive experiments demonstrate the consistent and stable performance improvements across autonomous driving paradigms, without introducing additional computational overhead during inference. 

## **2 Related Work** 

**End-to-End Autonomous Driving.** Conventional autonomous systems decompose the whole paradigm into three stages: perception [29, 35, 36, 45, 46], 

4 X. Liu et al. 

prediction [34, 42, 51], and planning [13, 32]. Such modular designs often lead to error accumulation and substantial engineering overhead. To address these limitations, recent works explore end-to-end autonomous driving, which learns a direct mapping from sensory observations to driving actions or trajectories [19, 20, 30, 44]. Existing methods can be broadly categorized based on the form of action outputs, including regression-based methods [17,20], generation-based approaches [31, 61], and reinforcement-based methods [11, 53]. In regression-based approaches, UniAD [19], VAD [20], and SparseDrive [44] construct end-to-end architectures by leveraging BEV representations and vectorized or sparse queries. For generative methods, GenAD [61] leverages generative models for trajectory regression. DiffusionDrive [31] and GoalFlow [52] utilize flow matching [33] and diffusion policy [5] paradigms to sample multi-mode actions. For reinforcement learning-based approaches, recent studies [21,26,27] formulate autonomous driving as a sequential decision-making problem, which optimizes driving policies through reward design and interaction with the environment. In addition, some recent approaches incorporate large language models (LLMs) into visionlanguage-action (VLA) frameworks by injecting language context as high-level guidance for reasoning and decision-making [6, 26, 63]. 

However, most existing end-to-end driving methods lack the ability to reason about future scene dynamics under different driving actions. This limitation motivates the development of world models that simulate future world evolution to support more informed decision-making. 

**World Models for Autonomous Driving** In autonomous driving systems, the world model aims to predict the future evolution of scenes following various actions [14,22,24,49,62]. Combining with the next state prediction, existing world models can be categorized into two types: future scene prediction [48, 49, 58–60] and feature-level world models in latent space [23–25, 55]. Representative works of future scene prediction focus on directly forecasting future observations or structured scene representations. For instance, GenAD [54], DrivingFuture [49], and Epona [58] predict future pixel-level scenes conditioned on actions, while DriveDreamer4D [59] extends this paradigm to 4D dynamic scene generation with 4D Gaussian Splatting reconstruction. Other approaches like UniOcc [48] and OccWorld [60] operate in voxelized or occupancy space, predicting future 3D occupancy or semantic fields to model scene evolution. Complementary to explicit scene forecasting, another line of research efforts learns the world model in a compact latent space, where the model predicts action-conditioned transitions over intermediate features rather than reconstructing full observations. LAW [24] and World4Drive [62] construct the world model in latent feature space for planning-oriented prediction, while SSR [23] and WoTE [25] further explore latent modeling in BEV space, moving beyond perspective-view representations. 

For our design, DynFlowDrive avoids explicit pixel-level scene generation and instead operates in latent space, focusing on modeling the underlying dynamics of world evolution for action-conditioned prediction. 


**Fig. 3: Overview of DynFlowDrive.** Given current observations, multi-mode trajectories are firstly generated by the standard planning module. A flow-based dynamic latent world model is incorporated to simulate the progressive future evolution in latent space. The resulting dynamics are used by a stability-aware multi-mode selection module, which assess the trajectory based on reconstruction quality and flow-based stabilit <mark>y</mark> , enabling reliable supervision and improved planning robustness. 

## **3** **<mark>M</mark> e** **<mark>th</mark>** **~~od~~** 

As illustrated in Figure 3, <mark>Dy</mark> nFlowDrive is <mark>bu</mark> ilt upon a standard end-to-end planning f <mark>ramework toge</mark> <u>ther</u> with a flow-based latent world modeling. Given the surrounding _N_ -view camera images **I** _t_ = _{It_<sup>_i}N_</sup> _i_ =1<sup>and a high-level navigation</sup> command _cmd_ at current timestep _t_ , a vision-based approach aims to predict the planning trajectory **T** that consists of a set of future points in BEV space. DynFlowDrive comprises three key parts: **1) Trajectory Planning Paradigm** (Sec. 3.1), which produces multi-mode trajectories based on the observations following the standard planning paradigm in end-to-end autonomous driving; **2) Dynamic World Model Prediction** (Sec. 3.2), that simulates latent scenes’ evolution conditioned on the planning trajectory with the flow-based dynamic model, and **3) Stability-aware Multi-mode Selection** (Sec. 3.3), which selects trajectory modes with respect to the dynamic stability for reliable supervision. These modules work in a complementary manner, coupling dynamic world simulation with multi-mode trajectory selection. 

### **3.1 Trajectory Planning Paradigm** 

As shown in the yellow part of Figure 3, the trajectory planning paradigm predicts multiple candidate trajectories. It first encodes the sensor inputs into a unified scene representation, a trajectory decoder then attends to the scene queries to iteratively refine the trajectory queries into final trajectory proposals. **Scene Encoder.** Given multi-view images **I** _t_ = _{It_<sup>_i}V_</sup> _i_ =1<sup>atthecurrenttimestep</sup> _t_ , each view is encoded into perspective-view features **F**<sup>pv</sup> _t_ = _{_ **F**<sup>_i_</sup> _t_<sup>_}V_</sup> _i_ =1<sup>.Asetof</sup> 

6 X. Liu et al. 

learnable scene queries **Q**<sup>_s_</sup> _t_<sup>isthenintroducedtoaggregatemulti-viewinforma-</sup> tion via cross-attention, which is formulated as: 


It yields a unified scene representation that captures the spatial layout and context from the driving scenes of the current time step. **Multi-modal Trajectory Decoder.** Since **Q**<sup>scene</sup> _t_ contains relevant scene information, following [19, 20], we initialize a set of candidate waypoint queries **Q**<sup>traj</sup> _t_ = _{qt_<sup>_i}N_</sup> _n_ =1<sup>_∈_R</sup><sup>_Nm×N××D_toextractmulti-modeplanningtrajectories,</sup> where _Nm_ denotes the number of driving commands, _N_ denotes the number of trajectory modes, and _D_ is the dimensions of query feature. 

Then, scene-level context **Q**<sup>scene</sup> _t_ is incorporated into the trajectory queries through cross-attention with the scene queries: 


Following the context-enhanced trajetcory queries, two diiferent MLP heads are applied for trajectory refinement and mode scoring. The trajectory head MLPtraj predicts a residual update to refine the waypoints, while the score head MLPs estimates a confidence score for each mode, which can be formulated as: 


where **T**<sup>ˆ</sup> _t_ = _{T_<sup>ˆ</sup> _t_<sup>_n}N_</sup> _n_ =1<sup>denotestherefinedtrajectories,and</sup><sup>**c**</sup><sup>_t_=</sup><sup>_{c_</sup> _t_<sup>_n}N_</sup> _n_ =1<sup>repre-</sup> sents their corresponding mode scores. These ( **T**<sup>ˆ</sup> _t,_ **c** _t_ ) pairs are treated as the multi-modal trajectory proposals for subsequent selection and training supervision. 

This formulation provides a set of diverse trajectory hypotheses while maintaining a unified query-based decoding structure, which serves as the foundation for subsequent trajectory selection and dynamic world modeling. 

### **3.2 Dynamic Latent World Model** 

To explicitly characterize planning quality through trajectory-induced world evolution, we introduce a dynamic latent world model that simulates how the environment evolves under different trajectory hypotheses. Given the current latent state and candidate trajectories, the model predicts future latent states via, which are used to evaluate the resulting trajectory outputs in latent space. **World Feature Extraction.** For the dynamic world simulator, directly reusing the driving encoder may lead to representation shifts and unstable features for modeling temporal evolution. Rather than follow prior works [23,24], we employ a pretrained foundation encoder to obtain more stable and dynamics-aligned latent representations. 

Given the surrounding _V_ -view images **I** _t_ = _{It_<sup>_i}V_</sup> _i_ =1<sup>,wefirstlyencodeeach</sup> view into a latent representation using a pretrained VAE encoder **E** vae followed by the lightweight MLP : 


DynFlowDrive 

7 

where **z** ˜<sup>_i_</sup> _t_<sup>denotesthedynamics-awarelatentfeatureforthe</sup><sup>_i_-thview.Suchrep-</sup> resentation benefits from the diverse training data and strong generalization capability of foundation models to obtain dynamics-oriented features. 

To incorporate global scene contexts, we aggregate the multi-view latent features by interacting them with the scene queries **Q**<sup>scene</sup> _t_ via cross-attention: 

> <sup>scene</sup> _t_ via cross-attention: 


where **z** ˜<sup>w</sup> _t_<sup>denotestheworldlatentthatcapturesbothmulti-viewspatialfeatures</sup><sup><mark>and</mark></sup> global scene context. 

Following the same procedure, we extract the corresponding world features for the next timestep, denoted as **z** ˜<sup>w</sup> _t_ +1<sup>,whichserveasthesupervisiontargetfortrainingthe</sup> dynamic flow model. **Flow-based Latent World Model Simulation.** Given Q<sup>)*+,+</sup> $ z$( ( **Dynamic Latent World Model** $z$ the current world latent ˜ **z**<sup>w</sup> _t_ Sup. and predicted trajectories **T** ˆ _t_ , we model trajectory- **Dynamic** 𝒗𝒗𝜽𝜽 conditionedtion in latentworldspace.evolu-As **… … …** Add Noise **… Flow Model …** shown in Figure 4, instead Grad. of learning a generic mapTrajectory Planning z$( ping between noise and Paradigm Condition data, we aim to learn a !𝐓𝐓" **Fig. 4:** The architecture of our **dynamic latent world** trajectory-conditioned ve- **model design** , in which the velocity field _vθ_ is learnt to locity field that describes capture the trajectory-conditioned dynamics transitions how the latent state evolves in the latent space. under different motion hypotheses. Following the rectified flow formulation [37], we construct the noised anchor state **a** from the current latent to provide a stochastic starting point for modeling local state transitions: 


where **_ϵ_** is the Gaussian noise with the same shape as **z**<sup>w</sup> _t_<sup>,and</sup><sup>_α∈_[0</sup><sup>_,_1]controlsthe</sup> perturbation strength. Then the continuous interpolation between the anchor **a** and the target latent **z** ˜<sup>w</sup> _t_ +1<sup>isthendefinedas:</sup> 


where _s_ denotes the flow timestep. 

To incorporate the trajectory conditions, planning modes _{T_<sup>ˆ</sup> _t_<sup>_n}_</sup> _i_<sup>_N_</sup> = _n_<sup>areencoded</sup> into a trajectory embeddings by TrajEmb( _·_ ) and fused with the original VAE latent to obtain the condition features _{_ **h**<sup>_n_</sup> _t_<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>:</sup> 


where _λz_ and _λT_ are scalar weights to balance the latent state and trajectory embeddings. Then, the velocity field can be predicted by a transformer-based flow model _Fθ_ ( _·_ ), which is formulated as: 


8 X. Liu et al. 

This formulation models how the latent state evolves under the corresponding trajectory hypothesis. 

Thus, during training, we adopt the flow matching objective that supervises the velocity along the interpolation path between the anchor state **a** and the target latent **z** ˜<sup>w</sup> _t_ +1<sup>:</sup> 


where the target velocity corresponds to the displacement from the anchor state toward the future latent along the interpolation path. For sampling integration, the learned velocity defines a trajectory-conditioned dynamical system so that the future world latent can be obtained via integration: 


Each step corresponds to an integration step along the flow variable _s_ , which simulates a small portion of the latent evolution between the driving timesteps _t_ and _t_ + 1. 

Thus, starting from the current latent **z** ˜ _t_<sup>w,thefutureworldlatentcanbeobtained</sup> by integrating the velocity field from _s_ = 0 to 1. In practice, we approximate this integration using a discrete Euler solver: 


where _sk_ is the corresponding flow timestep, and _∆s_ is the integration step size. 

This formulation models how different trajectory hypotheses induce distinct latent state transitions, enabling dynamics-aware <mark>trajec</mark> tory evaluation based on the progressive evolution dynamics. 

### **3.3 Stability-aware Multi-mode Selection** 

Our multi-modal trajectory predictor generates a set of candidate trajectories _{_ **T**<sup>ˆ</sup><sup>_n_</sup> _t_<sup>_}_</sup> _n_<sup>_N_</sup> =1<sup>tocapturethein-</sup> herent uncertainty of future driving behaviors. Conventional selection strategies typically rely on geometric or reconstruction criteria, such as trajectory error (e.g., ADE/FDE) and latent reconstruction loss. However, these metrics only measure spatial or feature-level similarity and fail to reflect the quality of trajectory-induced world evolution. 

In practice, different trajectory candidates may produce similar geometric errors while leading to substantially different latent state evolutions. Selecting trajectories solely based on geometric criteria may therefore favor modes that are spatially accurate but induce unstable or unrealistic scene dynamics, which is undesirable for reliable planning. 

To address this issue, as shown in Figure 5, we introduce a stability-aware selection strategy that evaluates each trajectory based on the induced dynamics. Given a trajectory candidate **T**<sup>ˆ</sup> _t_<sup>_n_, the flow-based world</sup> model simulates the latent evolution conditioned on 


**Fig. 5:** Stability-aware Multimode Selection. For training, the score head is supervised by the stable criterion. For Inference, the best mode trajectory is selected according to the highest score index. 

DynFlowDrive 9 

this trajectory and produces a sequence of velocities _{_ **v** _k_<sup>_n}_</sup> _k_<sup>_K_</sup> =1<sup>alongtheintegration</sup> steps, where _K_ is the discrete steps during transitions. We measure the directional consistency of the evolution by computing the average angular deviation between consecutive normalized velocity directions **u** ˆ<sup>_n_</sup> _k−_ 1<sup>and</sup><sup>**u**ˆ</sup> _k_<sup>_n_:</sup> 


where smaller _Sθ_<sup>_n_valueindicatessmootherandmorephysicallyconsistentdynamics.</sup> Based on this, we define the unified selection criterion, combined with other commonly used metrics [62] for each trajectory mode assessment: 


where _L_<sup>_n_</sup> _traj_<sup>denotesthetrajectoryerrorbetweenthepredictedtrajectoryandthe</sup> ground truth, and _Lrec_<sup>_n_measuresthereconstructiondiscrepancyofthepredictedla-</sup> tent state. The selected optimal mode _n_<sup>_∗_</sup> is employed to supervise the learning of the trajectory scoring head. 

By explicitly incorporating trajectory-conditioned dynamical stability, the proposed strategy favors trajectories that induce smooth and physically consistent world evolution, leading to more reliable trajectory assessment beyond conventional criteria. 

### **3.4 Training and Inference Settings** 

For model training, we jointly optimize trajectory prediction, scoring, latent reconstruction, and flow-based dynamics with a unified objective: 


Here, _Ltraj_ denotes the _L_ 1 loss between predicted trajectories and the ground-truth future trajectory. The scoring loss _Lscore_ is supervised using the selected optimal mode _n_<sup>_∗_</sup> defined in Sec. 3.3. _Lrec_ enforces consistency between the predicted latent state and the target latent representation, while _Lflow_ corresponds to the flow matching objective used to learn the trajectory-conditioned velocity field. The coefficients _λscore_ , _λrec_ , and _λflow_ balance the contributions of different objectives. 

During inference, the world model is not involved, since the driving system has already acquired the capability to select the optimal trajectory. The planning module directly selects the trajectory with the highest predicted score as the final output, introducing no additional computational overhead compared with the standard trajectory prediction framework. 

## **4 Experiment** 

### **4.1 Dataset and Metrics** 

For comprehensive evaluations, we train and evaluate our DynFlowDrive on two benchmarks, including the open-loop nuScenes [2] and the closed-loop NavSim [9]. **Open-Loop nuScenes Benchmark.** The nuScenes dataset contains 1000 driving scenes across different driving scenarios in Singapore and Boston. In line with previous 

10 X. Liu et al. 

studies [23, 24, 30], we make use of the calculated displacement error ( _L_ 2) with the ground truth and collision rate (CR) for performance evaluation. Displacement error is calculated by _L_ 2 error between the prediction and the GT trajectory, while CR quantifies the collision probability with surrounding objects following the predicted trajectories. All metrics are calculated within the 3s future with a 0.5s interval and evaluated at 1s, 2s, and 3s. We utilize the VAD evaluation metrics [20] that compute the average across all previous frames. 

**Closed-loop NavSim Benchmark.** NavSim provides a closed-loop benchmark built on the OpenScene dataset. It contains 103K keyframes with 1192 training scenarios and 136 test scenarios. During evaluation, the predicted trajectories are interpolated using an LQR controller sampled at 2 Hz over a 4-second horizon. It is evaluated by a simulator to get the rule-based simulation metric score, which is calculated based on five key metrics, including No at-fault Collisions (NC), Drivable Area Compliance (DAC), Time to Collision with bounds (TTC), Ego Progress (EP), and Comfort (C). Thus, the final PDM Score (PDMS) is derived by aggregating these metrics as follows PDMS = NC _×_ DAC _×_<sup>5</sup><sup>_×_</sup><sup><u>(EP+TTC</u></sup> 12<sup><u>)+2</u></sup><sup>_×_C</sup> . 

### **4.2 Implementation Details** 

**nuScenes.** For open-loop evaluation, our DynFlowDrive is trained for 12 epochs on 8 NVIDIA RTX 4090 GPUs with a batch size of 1 per GPU, which is built on the open-sourced LAW [24], SSR [23]. The driving commands align with previous works [19], including left, right, and go straight. For the SSR-based approaches, we adopt ResNet50 [15] as image backbone operating at an image resolution of 640 × 360. We utilize the AdamW optimizer [39] with a learning rate set to 1 _×_ 10<sup>_−_4</sup> . The weights _λscore_ for scoring loss, _λrec_ for latent reconstruction loss, and _λflow_ for flow loss are set to 0.5, 0.2, and 0.1, respectively. 

**NavSim.** We further conduct the closed loop evaluation of DynFlowDrive on the NavSim benchmark. Our model is trained for 30 epochs with a batch size of 16 per GPU. Following the setting of WoTE [25], we concatenate the front-view image with center-cropped front-left and front-right images, resulting in a combined resolution of 256 × 1024 pixels. For LiDAR, the 64m × 64m point cloud surrounding the ego vehicle is used. For network architecture, we employ ResNet34 [15] as the backbone for image feature extraction. The number of trajectory anchors is set to _N_ = 256. We utilize the Adam optimizer with a learning rate of 1 _×_ 10<sup>_−_4</sup> . 

### **4.3 Main Results** 

**Open-Loop Evaluation.** On the nuScenes [2] benchmark, we compare our proposed DynFlowDrive with the prior approaches following the evaluation metrics in VAD [20]. As shown in Table 1, our method consistently achieves superior results in both the _L_ 2 distance error and collision rate. We implement our DynFlowDrive based on two representative latent world model baselines. For the approaches without BEV representation, compared with LAW [24], our DynFlowDrive reduces the _L_ 2 displacement error by 0.4m and lowers the collision rate by 26%. Based on the BEV representation, we replace the latent world model in SSR [23] with our DynFlowDrive design, which yields nearly a 20% reduction on _L_ 2 distance by 0.08m and achieves 0.11% collision rate. It indicates that our approach can be seamlessly integrated into existing frameworks and consistently improve planning quality. Compared to the perception-based approaches, 

||||||||Dyn|Flow|Drive|11|
|---|---|---|---|---|---|---|---|---|---|---|
|**Method**|**Pub.**|**BEV**||**L2 (**|**m)** _↓_||**Col**|**lision **|**Rate (**|**%)** _↓_|
||||**1s**|**2s**|**3s**|**Avg.**|**1s**|**2s**|**3s**|**Avg.**|
|||_Perceptio_|_n-based _|_Approa_|_ches_||||||
|ST-P3 [17]|ECCV 2022|✓|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|
|UniAD [19]|CVPR 2023|✓|0.48|0.96|1.65|1.03|0.05|0.17|0.71|0.31|
|VAD-Tiny [20]|ICCV 2023|✓|0.46|0.76|1.12|0.78|0.21|0.35|0.58|0.38|
|VAD-Base [20]|ICCV 2023|✓|0.41|0.70|1.05|0.72|0.07|0.17|0.41|0.22|
|BEV-Planner [30]|CVPR 2024|✓|0.28|0.42|0.68|0.46|0.04|0.37|1.07|0.49|
|PARA-Drive [50]|CVPR 2024|✓|0.25|0.46|0.74|0.48|0.14|0.23|0.39|0.25|
|GenAD [61]|ECCV 2024|✓|0.28|0.49|0.78|0.52|0.08|0.14|0.34|0.19|
|SparseDrive [44]|ICCV 2025|✗|0.29|0.58|0.96|0.61|0.01|0.05|0.18|0.08|
|Drive-OccWorld [56]|AAAI 2025|✗|0.25|0.44|0.72|0.47|0.03|0.08|0.22|0.11|
|MomAD [43]|CVPR 2025|✗|0.31|0.57|0.91|0.60|0.01|0.05|0.22|0.09|
|DiffusionDrive [31]|CVPR 2025|✗|0.27|0.54|0.90|0.57|0.03|0.05|0.16|0.08|
||_La_|_tent Wo_|_rld Mod_|_el Appr_|_oaches_||||||
|LAW [24]|ICLR 2025|✗|0.26|0.57|1.01|0.61|0.14|0.21|0.54|0.30|
|**DynFlowDrive**(LAW)|-|✗|**0.24**|**0.54**|**0.92**|**0.57**|**0.11**|**0.12**|**0.48**|**0.22**|
|SSR<sup>_∗_</sup>[23]|ICLR 2025|✓|0.18|0.35|0.63|0.39|0.08|0.12|0.24|0.15|
|**DynFlowDrive** (SSR)|-|✓|0.16|0.32|0.57|0.35|0.07|0.09|0.21|0.14|
|**DynFlowDrive**_⋄_(SSR)|-|✓|**0.13**|**0.27**|**0.52**|**0.31**|**0.06**|**0.09**|**0.18**|**0.11**|


**Table 1: Comparison of the SOTA methods on the nuScenes dataset.** “ _∗_ ” denotes the re-implemented result from SSR [23] by official public codes. “ _⋄_ ” denotes using ego status in the planning module following BEVPlanner++ [30]. Evaluations are conducted in the same way as the settings in VAD [20]. Our DynFLowDrive are implemented based on LAW [24] and SSR. LAW adopts Swin-Tiny [38] as image backbone, while others adopt ResNet-50 [15]. 

without the incorporation of any auxiliary tasks, our dynamic latent world model still achieves comparable performance. 

**Qualitative Result.** In Figure 6, we present the qualitative comparisons between our DynFlowDrive and the baseline SSR with three different commands. As illustrated in both the BEV space and front-view camera perspectives, our planning results exhibit stronger alignment with the ground truth of the scene structure. In particular, our method produces smoother and more coherent trajectories that better follow lane geometry and surrounding dynamics, indicating improved consistency between predicted motions and the underlying environment. More visualizations are provided in our supplementary materials. 

**Closed-Loop Evaluation.** We further evaluate DynFlowDrive under closed-loop settings on the NavSim benchmark [9]. The comparison results are summarized in Table 2. As shown, DynFlowDrive achieves competitive performance across closed-loop metrics and reaches the state-of-the-art planning accuracy of 88.7% PDMS, surpassing the baseline world model approach WoTE [25]. Notably, without relying on auxiliary tasks such as object detection or online mapping, our method also outperforms previous world model-based approaches, including LAW [24] and World4Drive [62]. These results demonstrate that incorporating the flow-based latent world model together with the stability-aware selection mechanism enables the model to better capture trajectoryconditioned world dynamics, leading to safer and more reliable planning behavior in closed-loop driving scenarios. 

12 X. Liu et al. 


**Fig. 6: Visualization of Planning Results on nuScenese dataset.** The perception representations are rendered from annotations. Surrounding light lines denote the maps of the scene, while black boxes represent the object detection. The ego vehicle is drawn by the green box in the center. 

### **4.4 Ablation Study** 

In this section, we conduct comprehensive ablation studies to investigate the effectiveness of our DynFlowDrive designs. For fair comparison, all ablations are conducted on the nuScenes benchmark. More ablations and analyses on NavSim benchmark are provided in our supplementary materials. 

**Verification of Component Designs.** In this section, we conduct ablation studies to evaluate the contribution of each component and the combinations. As shown in Table 3, starting from the vanilla end-to-end autonomous driving paradigm without BEV representation or world modeling modules, incorporating the static transformerbased world model yields only marginal improvement. By introducing the proposed dynamic latent world model, we achieve an average _L_ 2 error reduction of 0.1 m and a 11% decrease in collision rate, demonstrating the benefit of dynamic simulation of world evolution. Furthermore, when combined with the stability-aware multi-mode selection, DynFlowDrive achieves the best overall performance, reaching an _L_ 2 error of 0.57 m and 

DynFlowDrive 13 

|**Method**|**Input**<br>|**#Traj.**|**Traj. Eval.**|**NC** _↑_|**DAC** _↑_|**EP** _↑_|**TTC** _↑_|**Comf.** _↑_<br>|**PDMS** _↑_|
|---|---|---|---|---|---|---|---|---|---|
|Human|-|-|-|100|100|87.5|100|99.9|94.8|
|Constant Velocity|-|1|✗|69.9|58.8|49.3|49.3|100.0|21.6|
|Ego Status MLP|-|1|✗|93.0|77.3|62.8|83.6|100.0|65.6|
|VADv2 [4]|C|8192|Rule-based|97.9|91.7|77.6|92.9|100.0|83.0|
|UniAD [19]|C|1|Rule-based|97.8|91.9|78.8|92.9|100.0|83.4|
|LTF [41]|C|1|✗|97.4|92.8|79.0|92.4|100.0|83.8|
|PARA-Drive [50]|C|1|Rule-based|97.9|92.4|79.3|93.0|99.8|84.0|
|TransFuser [8]|C & L|1|✗|97.7|92.8|79.2|92.8|100.0|84.0|
|LAW [24]|C|1|✗|96.4|95.4|81.7|88.7|99.9|84.6|
|World4Drive [62]|C|6|✗|97.4|94.3|79.9|92.8|100.0|85.1|
|DRAMA [57]|C & L|1|✗|98.0|93.1|80.1|94.8|100.0|85.5|
|Hydra-MDP [28]|C & L|8192|Model-free|98.3|96.0|78.7|94.6|100.0|86.5|
|DiffusionDrive [31]|C & L|20|✗|98.2|96.2|82.2|94.7|100.0|88.1|
|WoTE [25]|C & L|256|Model-based|98.5|96.8|81.9|94.9|99.9|88.3|
|**DynFlowDrive (Ou**|**rs)**<br>C & L|256|Model-based|**98.7**|**96.8**|**82.5**|**95.5**|**100.0**|**88.7**|


**Table 2: Comparison with the SOTA approaches on the NavSim test set.** C: Camera. L: LiDAR. Rule-based means that trajectory evaluation follows specific rules. Model-free represents the evaluation without world modeling. Model-based denotes evaluating the trajectory with the assistance of the world model. 

|**M**|**odules**|||_L_2 (|m) _↓_|||CR (|%) _↓_||FPS_↑_|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Static-WM|Dyn-WM|MS|1s|2s|3s|Avg.|1s|2s|3s|Avg.||
|-|-|-|0.31|0.63|1.12|0.69|0.19|0.27|0.64|0.37|13.8|
|✓|-|-|0.26|0.57|1.01|0.61|0.14|0.21|0.54|0.30|13.8|
|-|✓|-|0.26|0.55|0.94|0.59|0.11|0.16|0.51|0.26|13.8|
|-|-|✓|0.25|0.55|0.93|0.58|0.11|0.15|0.49|0.25|13.6|
|-|✓|✓|**0.24**|**0.54**|**0.92**|**0.57**|**0.10**|**0.12**|**0.45**|**0.22**|13.6|


**Table 3: Component-wise Ablation.** Static-WM and Dyn-WM mean the existing stable world model design and our flow-based dynamic modeling. MS denotes the strategy of stability-aware multi-mode selection. FPS are measured on one RTX 4090. 

a collision rate of 0.22%. These results validate that dynamic evolution modeling and stability-guided mode selection jointly contribute to safer and more accurate trajectory planning. For inference, no additional computational burdens are introduced, as the flow-based world model is only used during training and does not participate in the forward prediction pipeline. 

**Ablations on the Dynamic Latent World Model Design.** We evaluate different world model designs in Table 4. Replacing the static transformer-based world model with the proposed flow-based formulation consistently improves long-horizon prediction. In particular, the 3s _L_ 2 error is reduced from 1.01 m to 0.94 m and the collision rate decreases from 0.54% to 0.51%. This improvement indicates that flow-based modeling better captures the dynamic evolution of the driving scene in latent space, resulting in smoother and more coherent trajectory predictions. Furthermore, applying the flow-based dynamics on world features extracted by the pretrained encoder brings additional gains. By decoupling representation learning from dynamic evolution modeling, the model achieves more stable latent transitions, reducing the average _L_ 2 error to 0.57 m and the collision rate to 0.22%. These results demonstrate that combining flow-based dynamics with stable latent representations leads to more reliable trajectory-conditioned world modeling. 

14 X. Liu et al. 

|**World Model Design**|1s|_L_2 (<br>2s|m) _↓_<br>3s|Avg.|1s|CR (<br>2s|%) _↓_<br>3s|Avg.|
|---|---|---|---|---|---|---|---|---|
|Static WM|0.26|0.57|1.01|0.61|0.14|0.21|0.54|0.30|
|Flow WM|0.26|0.55|0.94|0.59|0.11|0.16|0.51|0.26|
|+ World Feat. Design|**0.24**|**0.54**|**0.92**|**0.57**|**0.10**|**0.12**|**0.45**|**0.22**|


**Table 4: Ablations on the Dynamic Latent World Model Design.** 

**Ablations on Flow Integration Steps.** We study the impact of the number of integration steps used to approximate the continuous flow dynamics. As shown in Table 5a, increasing the number of steps from 1 to 5 consistently improves both trajectory accuracy and safety, reducing the _L_ 2 error from 0.60 m to 0.57 m and the collision rate from 0.28% to 0.22%. This demonstrates that a finer discretization better captures the underlying trajectory-conditioned dynamics. However, further increasing the number of steps to 10 yields no additional gains and even slightly degrades performance. We attribute this to accumulated numerical errors and over-smoothing during integration. Overall, a moderate number of integration steps of 5 achieves the best trade-off between accuracy and stability. 

|**# Steps**|1|3|5|10|**Selection Strategy**<br>/|_L_2 (m) Avg. _↓_<br>0.61|CR (%) Avg. _↓_<br>0.30|
|---|---|---|---|---|---|---|---|
|_L_2 (m) Avg._↓_|0.60|0.59|**0.57**|0.59|_L_2 Only<br>+Recons|0.59<br>058|0.24<br>022|
|CR (%) Avg._↓_|0.28|0.23|**0.22**|0.24|.<br>+ Flow Stab.|.<br>**0.57**|.<br>**0.22**|


**(a)** Ablations on Flow Integration Steps. 

**(b)** Ablations on Mode Selection Criteria. 

**Table 5: Ablations on Flow Steps and Multi-Mode Selection Strategies.** 

**Ablations on Multi-Mode Selection.** We study different multi-mode selection strategies in Table 5b. Selecting modes solely based on _L_ 2 distance is suboptimal, as it emphasizes point-wise accuracy while neglecting temporal consistency and physical plausibility, leading to higher collision rates. Incorporating reconstruction similarity improves latent alignment and trajectory coherence, yielding consistent gains. Further introducing flow direction as a stability-aware criterion encourages modes to follow the learned dynamic evolution, resulting in the lowest collision rate of 0.22% with competitive _L_ 2 distance of 0.57 m. These results show that combined with the reconstruction similarity, flow-based stability provides a more reliable selection criterion for safe and robust trajectory planning. 

## **5 Conclusion** 

In this work, we propose **DynFlowDrive** , a flow-based dynamic latent world modeling that explicitly models the progressive scene evolution in latent space via rectified flow. By conditioning on candidate trajectories, our approach enables dynamic simulation of future world states and supports more reliable trajectory evaluation through stability-aware multi-mode selection. Extensive experiments on nuScenes and NavSim demonstrate that DynFlowDrive consistently improves planning accuracy and safety across different end-to-end driving frameworks. These results highlight the importance of explicitly modeling world dynamics for robust and scalable autonomous driving systems. Future work includes integrating vision-language models (VLMs) for stronger semantic reasoning, improving robustness under rare corner cases, and ensuring scalability to diverse driving environments. 

DynFlowDrive 

15 

## **References** 

1. Allen, J.F., Koomen, J.A.: Planning using a temporal world model. In: IJCAI. pp. 741–747 (1983) 2 

2. Caesar, H., Bankiti, V., Lang, A.H., Vora, S., Liong, V.E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., Beijbom, O.: nuscenes: A multimodal dataset for autonomous driving. In: CVPR. pp. 11621–11631 (2020) 3, 9, 10 

3. Chen, L., Wu, P., Chitta, K., Jaeger, B., Geiger, A., Li, H.: End-to-end autonomous driving: Challenges and frontiers. IEEE TPAMI (2024) 2 

4. Chen, S., Jiang, B., Gao, H., Liao, B., Xu, Q., Zhang, Q., Huang, C., Liu, W., Wang, X.: Vadv2: End-to-end vectorized autonomous driving via probabilistic planning. arXiv preprint arXiv:2402.13243 (2024) 2, 13 

5. Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S.: Diffusion policy: Visuomotor policy learning via action diffusion. The International Journal of Robotics Research **44** (10-11), 1684–1704 (2025) 4 

6. Chi, H., Gao, H.a., Liu, Z., Liu, J., Liu, C., Li, J., Yang, K., Yu, Y., Wang, Z., Li, W., et al.: Impromptu vla: Open weights and open data for driving visionlanguage-action models. arXiv preprint arXiv:2505.23757 (2025) 4 

7. Chib, P.S., Singh, P.: Recent advancements in end-to-end autonomous driving using deep learning: A survey. TIV **9** (1), 103–118 (2023) 2 

8. Chitta, K., Prakash, A., Jaeger, B., Yu, Z., Renz, K., Geiger, A.: Transfuser: Imitation with transformer-based sensor fusion for autonomous driving. IEEE TPAMI **45** (11), 12878–12895 (2022) 13 

9. Dauner, D., Hallgarten, M., Li, T., Weng, X., Huang, Z., Yang, Z., Li, H., Gilitschenski, I., Ivanovic, B., Pavone, M., et al.: Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. In: NeurIPS (2024) 3, 9, 11 

10. Dong, W., Lu, S., Chen, X., Zhang, S., Liu, Q., Liu, Z., Chen, L., Wang, H., Cai, Y.: End-to-end autonomous driving: From classic paradigm to large model empowerment—a comprehensive survey. IEEE Internet of Things Journal **13** (3), 3870–3898 (2025) 2 

11. Gao, H., Chen, S., Jiang, B., Liao, B., Shi, Y., Guo, X., Pu, Y., Yin, H., Li, X., Zhang, X., Zhang, Y., Liu, W., Zhang, Q., Wang, X.: Rad: Training an end-to-end driving policy via large-scale 3dgs-based reinforcement learning. arXiv preprint arXiv:2502.13144 (2025) 4 

12. Gao, R., Chen, K., Xie, E., Hong, L., Li, Z., Yeung, D.Y., Xu, Q.: Magicdrive: Street view generation with diverse 3d geometry control. In: ICLR (2024) 2 

13. González, D., Pérez, J., Milanés, V., Nashashibi, F.: A review of motion planning techniques for automated vehicles. TITS **17** (4), 1135–1145 (2015) 4 

14. Guan, Y., Liao, H., Li, Z., Hu, J., Yuan, R., Zhang, G., Xu, C.: World models for autonomous driving: An initial survey. TIV (2024) 2, 4 

15. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition. In: CVPR. pp. 770–778 (2016) 10, 11 

16. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023) 2 

17. Hu, S., Chen, L., Wu, P., Li, H., Yan, J., Tao, D.: St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In: ECCV. pp. 533–549. Springer (2022) 4, 11 

18. Hu, T., Liu, X., Wang, S., Zhu, Y., Liang, A., Kong, L., Zhao, G., Gong, Z., Cen, J., Huang, Z., et al.: Vision-language-action models for autonomous driving: Past, present, and future. arXiv preprint arXiv:2512.16760 (2025) 2 

- 16 X. Liu et al. 

19. Hu, Y., Yang, J., Chen, L., Li, K., Sima, C., Zhu, X., Chai, S., Du, S., Lin, T., Wang, W., et al.: Planning-oriented autonomous driving. In: CVPR. pp. 17853– 17862 (2023) 4, 6, 10, 11, 13 

20. Jiang, B., Chen, S., Xu, Q., Liao, B., Chen, J., Zhou, H., Zhang, Q., Liu, W., Huang, C., Wang, X.: Vad: Vectorized scene representation for efficient autonomous driving. In: ICCV. pp. 8340–8350 (2023) 4, 6, 10, 11 

21. Jiao, S., Qian, K., Ye, H., Zhong, Y., Luo, Z., Jiang, S., Huang, Z., Fang, Y., Miao, J., Fu, Z., et al.: Evadrive: Evolutionary adversarial policy optimization for end-to-end autonomous driving. arXiv preprint arXiv:2508.09158 (2025) 4 

22. Kong, L., Yang, W., Mei, J., Liu, Y., Liang, A., Zhu, D., Lu, D., Yin, W., Hu, X., Jia, M., et al.: 3d and 4d world modeling: A survey. arXiv preprint arXiv:2509.07996 (2025) 2, 4 

23. Li, P., Cui, D.: Navigation-guided sparse scene representation for end-to-end autonomous driving. arXiv preprint arXiv:2409.18341 (2024) 3, 4, 6, 10, 11 

24. Li, Y., Fan, L., He, J., Wang, Y., Chen, Y., Zhang, Z., Tan, T.: Enhancing end-toend autonomous driving with latent world model. arXiv preprint arXiv:2406.08481 (2024) 2, 4, 6, 10, 11, 13 

25. Li, Y., Wang, Y., Liu, Y., He, J., Fan, L., Zhang, Z.: End-to-end driving with online trajectory evaluation via bev world model. arXiv preprint arXiv:2504.01941 (2025) 4, 10, 11, 13 

26. Li, Y., Xiong, K., Guo, X., Li, F., Yan, S., Xu, G., Zhou, L., Chen, L., Sun, H., Wang, B., et al.: Recogdrive: A reinforced cognitive framework for end-to-end autonomous driving. arXiv preprint arXiv:2506.08052 (2025) 4 

27. Li, Y., Tian, M., Zhu, D., Zhu, J., Lin, Z., Xiong, Z., Zhao, X.: Drive-r1: Bridging reasoning and planning in vlms for autonomous driving with reinforcement learning. arXiv preprint arXiv:2506.18234 (2025) 4 

28. Li, Z., Li, K., Wang, S., Lan, S., Yu, Z., Ji, Y., Li, Z., Zhu, Z., Kautz, J., Wu, Z., et al.: Hydra-mdp: End-to-end multimodal planning with multi-target hydradistillation. arXiv preprint arXiv:2406.06978 (2024) 13 

29. Li, Z., Wang, W., Li, H., Xie, E., Sima, C., Lu, T., Yu, Q., Dai, J.: Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. IEEE TPAMI (2024) 3 

30. Li, Z., Yu, Z., Lan, S., Li, J., Kautz, J., Lu, T., Alvarez, J.M.: Is ego status all you need for open-loop end-to-end autonomous driving? In: CVPR (2024) 4, 10, 11 

31. Liao, B., Chen, S., Yin, H., Jiang, B., Wang, C., Yan, S., Zhang, X., Li, X., Zhang, Y., Zhang, Q., et al.: Diffusiondrive: Truncated diffusion model for end-to-end autonomous driving. In: CVPR. pp. 12037–12047 (2025) 4, 11, 13 

32. Lim, W., Lee, S., Sunwoo, M., Jo, K.: Hybrid trajectory planning for autonomous driving in on-road dynamic scenarios. TITS **22** (1), 341–355 (2019) 4 

33. Lipman, Y., Chen, R.T., Ben-Hamu, H., Nickel, M., Le, M.: Flow matching for generative modeling. arXiv preprint arXiv:2210.02747 (2022) 4 

34. Liu, J., Mao, X., Fang, Y., Zhu, D., Meng, M.Q.H.: A survey on deep-learning approaches for vehicle trajectory prediction in autonomous driving. In: ROBIO. pp. 978–985. IEEE (2021) 4 

35. Liu, X., Wang, S., Li, W., Yang, R., Chen, J., Zhu, J.: Mgmap: Mask-guided learning for online vectorized hd map construction. In: CVPR. pp. 14812–14821 (2024) 3 

36. Liu, X., Yang, R., Wang, S., Li, W., Chen, J., Zhu, J.: Uncertainty-instructed structure injection for generalizable hd map construction. In: CVPR. pp. 22359– 22368 (2025) 3 

DynFlowDrive 17 

37. Liu, X., Gong, C., Liu, Q.: Flow straight and fast: Learning to generate and transfer data with rectified flow. arXiv preprint arXiv:2209.03003 (2022) 7 

38. Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., Guo, B.: Swin transformer: Hierarchical vision transformer using shifted windows. In: ICCV. pp. 10012–10022 (2021) 11 

39. Loshchilov, I., Hutter, F.: Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101 (2017) 10 

40. Podell, D., English, Z., Lacey, K., Blattmann, A., Dockhorn, T., Müller, J., Penna, J., Rombach, R.: Sdxl: Improving latent diffusion models for high-resolution image synthesis. In: ICLR (2024) 2 

41. Prakash, A., Chitta, K., Geiger, A.: Multi-modal fusion transformer for end-to-end autonomous driving. In: CVPR. pp. 7077–7087 (2021) 13 

42. Song, H., Ding, W., Chen, Y., Shen, S., Wang, M.Y., Chen, Q.: Pip: Planninginformed trajectory prediction for autonomous driving. In: ECCV. pp. 598–614. Springer (2020) 4 

43. Song, Z., Jia, C., Liu, L., Pan, H., Zhang, Y., Wang, J., Zhang, X., Xu, S., Yang, L., Luo, Y.: Don’t shake the wheel: Momentum-aware planning in end-to-end autonomous driving. In: CVPR. pp. 22432–22441 (2025) 11 

44. Sun, W., Lin, X., Shi, Y., Zhang, C., Wu, H., Zheng, S.: Sparsedrive: End-toend autonomous driving via sparse scene representation. In: ICRA. pp. 8795–8801. IEEE (2025) 4, 11 

45. Wang, S., Liu, Y., Wang, T., Li, Y., Zhang, X.: Exploring object-centric temporal modeling for efficient multi-view 3d object detection. In: ICCV. pp. 3621–3631 (2023) 3 

46. Wang, S., Yu, J., Li, W., Liu, W., Liu, X., Chen, J., Zhu, J.: Not all voxels are equal: Hardness-aware semantic scene completion with self-distillation. In: CVPR. pp. 14792–14801 (2024) 3 

47. Wang, X., Zhu, Z., Huang, G., Chen, X., Zhu, J., Lu, J.: Drivedreamer: Towards real-world-drive world models for autonomous driving. In: ECCV. pp. 55–72 (2024) 2 

48. Wang, Y., Huang, X., Sun, X., Yan, M., Xing, S., Tu, Z., Li, J.: Uniocc: A unified benchmark for occupancy forecasting and prediction in autonomous driving. arXiv preprint arXiv:2503.24381 (2025) 4 

49. Wang, Y., He, J., Fan, L., Li, H., Chen, Y., Zhang, Z.: Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In: CVPR. pp. 14749–14759 (2024) 2, 4 

50. Weng, X., Ivanovic, B., Wang, Y., Wang, Y., Pavone, M.: Para-drive: Parallelized architecture for real-time autonomous driving. In: CVPR. pp. 15449–15458 (2024) 2, 11, 13 

51. Xin, L., Wang, P., Chan, C.Y., Chen, J., Li, S.E., Cheng, B.: Intention-aware long horizon trajectory prediction of surrounding vehicles using dual lstm networks. In: ITSC. pp. 1441–1446. IEEE (2018) 4 

52. Xing, Z., Zhang, X., Hu, Y., Jiang, B., He, T., Zhang, Q., Long, X., Yin, W.: Goalflow: Goal-driven flow matching for multimodal trajectories generation in endto-end autonomous driving. In: CVPR. pp. 1602–1611 (2025) 4 

53. Yan, T., Tang, T., Gui, X., Li, Y., Zhesng, J., Huang, W., Kong, L., Han, W., Zhou, X., Zhang, X., et al.: Ad-r1: Closed-loop reinforcement learning for end-to-end autonomous driving with impartial world models. arXiv preprint arXiv:2511.20325 (2025) 4 

- 18 X. Liu et al. 

54. Yang, J., Gao, S., Qiu, Y., Chen, L., Li, T., Dai, B., Chitta, K., Wu, P., Zeng, J., Luo, P., et al.: Generalized predictive model for autonomous driving. In: CVPR. pp. 14662–14672 (2024) 4 

55. Yang, P., Lu, B., Xia, Z., Han, C., Gao, Y., Zhang, T., Zhan, K., Lang, X., Zheng, Y., Zhang, Q.: Worldrft: Latent world model planning with reinforcement finetuning for autonomous driving. arXiv preprint arXiv:2512.19133 (2025) 2, 4 

56. Yang, Y., Mei, J., Ma, Y., Du, S., Chen, W., Qian, Y., Feng, Y., Liu, Y.: Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In: AAAI. vol. 39, pp. 9327–9335 (2025) 2, 11 

57. Yuan, C., Zhang, Z., Sun, J., Sun, S., Huang, Z., Lee, C.D.W., Li, D., Han, Y., Wong, A., Tee, K.P., et al.: Drama: An efficient end-to-end motion planner for autonomous driving with mamba. arXiv preprint arXiv:2408.03601 (2024) 13 

58. Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.X., et al.: Epona: Autoregressive diffusion world model for autonomous driving. arXiv preprint arXiv:2506.24113 (2025) 2, 4 

59. Zhao, G., Ni, C., Wang, X., Zhu, Z., Zhang, X., Wang, Y., Huang, G., Chen, X., Wang, B., Zhang, Y., et al.: Drivedreamer4d: World models are effective data machines for 4d driving scene representation. In: CVPR. pp. 12015–12026 (2025) 4 

60. Zheng, W., Chen, W., Huang, Y., Zhang, B., Duan, Y., Lu, J.: Occworld: Learning a 3d occupancy world model for autonomous driving. In: ECCV. pp. 55–72. Springer (2024) 2, 4 

61. Zheng, W., Song, R., Guo, X., Zhang, C., Chen, L.: Genad: Generative end-to-end autonomous driving. In: ECCV. pp. 87–104. Springer (2024) 4, 11 

62. Zheng, Y., Yang, P., Xing, Z., Zhang, Q., Zheng, Y., Gao, Y., Li, P., Zhang, T., Xia, Z., Jia, P., et al.: World4drive: End-to-end autonomous driving via intentionaware physical latent world model. In: ICCV. pp. 28632–28642 (2025) 2, 4, 9, 11, 13 

63. Zhou, X., Han, X., Yang, F., Ma, Y., Tresp, V., Knoll, A.: Opendrivevla: Towards end-to-end autonomous driving with large vision language action model. arXiv preprint arXiv:2503.23463 (2025) 4 

