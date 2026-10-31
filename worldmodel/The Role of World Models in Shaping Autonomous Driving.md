---
title: "The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey"
date: "2025-02-14"
authors: "Sifan Tu; Xin Zhou; Dingkang Liang; Xingyu Jiang; Yumeng Zhang; Xiaofan Li"
url: https://arxiv.org/abs/2502.10498
pdf: https://arxiv.org/pdf/2502.10498
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2502.10498)** / [論文ページ](https://arxiv.org/abs/2502.10498)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey** 

Sifan Tu<sup>1</sup> , Xin Zhou<sup>1</sup> , Dingkang Liang<sup>1</sup> , Xingyu Jiang<sup>1</sup> , Yumeng Zhang<sup>2</sup> , Xiaofan Li<sup>2</sup> , Xiang Bai<sup>1</sup> 1Huazhong University of Science and Technology, 2Baidu Inc. 

_{_ sifantu, xzhou03, dkliang _}_ @hust.edu.cn 

## **Abstract** 

_The Driving World Model (DWM), which focuses on predicting scene evolution during the driving process, has emerged as a promising paradigm in the pursuit of autonomous driving (AD). DWMs enable AD systems to better perceive, understand, and interact with dynamic driving environments. In this survey, we provide a comprehensive overview of the latest progress in DWM. First, we review the DWM ecosystem, which is constructed using mainstream simulators, high-impact datasets, and various metrics that evaluate DWMs across multiple dimensions. We then categorize existing approaches based on the modalities of the predicted scenes, including video, point cloud, occupancy, latent feature, and traffic map, and summarize their specific applications in AD research. In addition, the performance of representative approaches across generating and driving tasks is presented. Finally, we discuss the potential limitations of current research and propose future directions. This survey provides valuable insights into the development and application of DWM, fostering its broader adoption in AD. The relevant papers are collected at https://github. com/LMD0311/Awesome-World-Model._ 

## **1. Introduction** 

World Models are designed to forecast the future scene given historical observations, thereby internalizing the principles governing the external world [39]. This paradigm is regarded as a promising path toward human-level realworld cognition [58]. In the domain of Autonomous Driving (AD), the inherent complexity of environmental dynamics and stringent operational-safety requirements pose significant challenges for traditional perception systems [46], while the scarcity of high-quality annotations limits their scalability. In this context, Driving World Models (DWMs) emerge as an instrumental methodology for addressing these hurdles. 

As illustrated in Fig. 1, the primary objective of DWMs 

is to forecast the temporal evolution of driving scenes conditioned on diverse instructions. This paradigm promotes category-agnostic perception, enabling a holistic understanding of complex environments. Furthermore, the DWM diagram facilitates self-supervised training, enabling the effective utilization of vast unlabeled data. Therefore, these methods are of great significance for the realization of reliable AD systems. 

Recently emerging research on DWMs encompass a diverse array of modalities within the AD research landscape, ranging from real-world representations, such as video [10, 24, 43, 90, 102, 122], point clouds [71, 149, 171, 173, 178] and occupancy [32, 119, 127, 141, 167], to latent features [55, 63, 68, 96, 170] and traffic maps [53, 103, 108, 161]. Each modality in DWM involves its own characteristics, resulting in unique developmental paths. For example, video-targeted DWMs [27, 125, 150] focus on high-fidelity and multi-view-consistent generation, whereas occupancytargeted DWMs [85, 138, 155] place a greater emphasis on computational efficiency. On the other hand, the comprehensive impact of DWMs on AD research is also reflected in diverse application pathways. The controllable and realistic generation capability of DWMs enables driving scene simulation [140, 147] and diverse data synthesis [122, 150, 178], while the understanding and forecasting of dynamic scenes augment planners with robust perception [68, 127, 167] and enriched contextual awareness [152, 154]. In addition, DWM-based pre-training diagrams [1, 47, 87, 104, 149] demonstrate a significant enhancement in the performance of various downstream tasks. 

Diverse generative and functional capabilities foster a deep integration between DWMs and AD research. However, this variety simultaneously introduces considerable complexity, leading to a fragmented research landscape. Existing surveys [18, 21, 33, 49, 153, 176] tend to group DWMs within a single system, overlooking the unique challenges associated with specific implementations. In contrast, this survey provides a comprehensive review of DWM research and offers a detailed classification based on distinct prediction modalities and applications. By investigating 

1 


Figure 1. DWMs perceive historical observations and predict future scene evolutions, which adhere to multimodal conditions. This paradigm is applied to various domains of AD research, including simulation, data generation, driving, and pre-training. 

these unique technical paths, this paper aims to provide an exhaustive reference for researchers entering the field and present insightful perspectives for future DWM research. Our contributions can be summarized as follows: 

- We provide a comprehensive review of the recent evolution of DWMs, categorizing methods by prediction modalities, along with a systematic analysis of their respective development paths. 

- We synthesize the integration of DWMs with AD research, elucidating their impact on simulation, data generation, driving performance, and training paradigms. 

- We conduct a critical analysis of current limitations and outline promising future directions, delivering valuable insights for the community and facilitating the further development of DWMs. 

The overall organization of this survey is illustrated in Figure 2. Sec. 2 introduces mainstream simulators, highimpact datasets, and multi-dimensional metrics of current DWMs. Sec. 3 and Sec. 4 discuss existing approaches from the perspectives of prediction modalities and applications, respectively. Sec. 5 presents the performance of DWMs on primary tasks, including generation tasks of various modalities and driving planning. Finally, Sec. 6 summarizes the current limitations and outlines future research directions. 

## **2. DWM Ecosystem** 

Simulators, datasets, and metrics form the ecosystem of DWM search, serving as the foundation for training and evaluation. Early DWMs [65, 94, 122, 129] are trained and evaluated on traditional AD datasets and simulators, with their capabilities measured by generation and driving planning metrics. Following the rapid development of this field, an ecosystem specifically for DWMs is gradually tak- 

ing shape. In this section, we conduct a systematic review of existing simulators, datasets, and metrics to clarify how these factors work together to shape the current research landscape of DWMs. 

### **2.1. Simulator & Dataset** 

Simulators and datasets serve as the fundamental basis of DWM research. Specifically, simulators enable the acquisition of interactive data within virtual scenarios, while datasets facilitate the training and evaluation of frameworks with real-world data, thereby enhancing their generalization capabilities in the physical world. 

**Simulators.** Simulators enable large-scale closed-loop training and evaluation, serving as the foundation of the DWM ecosystem. Tab. 1 provides a comprehensive overview of the simulators widely utilized in DWM research. We categorize these platforms based on their functional scope. Full-stack simulators [19, 92] support the generation of both agent behaviors and sensory observations, while Behavior simulators [34, 38, 62] focus on agent dynamics and logic. Notably, behavior simulators can be integrated with scene rendering models to construct full-stack simulations [140, 147], demonstrating a feasible path towards photorealistic closed-loop simulation. 

**Datasets.** Tab. 2 presents the primary datasets in current DWM research. Traditional AD datasets such as KITTI [31], Waymo Open Dataset [106], and nuScenes [7], characterized by comprehensive data modalities and meticulous annotations, serve as a pivotal driving force for DWM research. However, the majority of these driving datasets require field acquisition and considerable cost, which restricts the scale and diversity of the dataset and gradually becomes a bottleneck amidst the rapid advancement of selfsupervised DWMs [66, 87, 149]. 

While datasets like OpenDV-YouTube [142] attempt to address this by harvesting large-scale data from the internet, they fail to adequately compensate for the extreme scarcity of long-tail scenarios and the lack of multi-modal data. Recent studies try to construct datasets rich in complex driving behaviors, aiming to address the urgent demand within DWM research for large-scale, diverse data. For instance, DrivingDojo [124] conducts field collection and meticulous filtering of large-scale driving videos to establish a diverse dataset covering ego-actions, multi-agent interplay, and open-world knowledge. 

With the continuous progress of DWM, new characteristics and requirements gradually emerge, such as vision-to-4D prediction and controllable action simulation. In parallel, New datasets and benchmarks, including Cam4DOcc [84], ACT-Bench [3], and WorldSimBench [98], are also introduced to satisfy the evaluation needs of existing approaches and guide the direction of subsequent studies. 

2 


Figure 2. Main structure. Sec. 2 introduces simulators, datasets, and metrics involved in DWM studies. Sec. 3 and Sec. 4 delineate the development of DWMs separately from prediction modalities and applications. Sec. 5 presents the performance of DWMs across generation and planning tasks. Sec. 6 outlines current limitations and future research directions. 

Table 1. Mainstream simulators. Full-stack simulation encompasses the simulation of both driving behaviors and observed scenarios, whereas behavior simulation refers to the simulation of driving behaviors alone. 

|**Platform**|**Year**|**Domain**|**Description**|
|---|---|---|---|
|CARLA [19]|2016|Full-Stack Simulation|Providing multimodal scene data, along with comprehensive annotations.|
|Nvidia Drive Sim [92]|2020|Full-Stack Simulation|Simulation and synthetic data generation pipelines powered by NVIDIA’s advanced models, tools, and libraries.|
|MetaDrive [62]|2021|Behavior Simulation|Featuring scene composability and scalability to accommodate diverse reinforcement learning training tasks.|
|NuPlan [38]|2021|Behavior Simulation|Providing a large-scale driving dataset and an open-source traffic simulator.|
|Waymax [34]|2023|Behavior Simulation|Multi-agent behavior simulator based on the Waymo Open Dataset [95].|
|LimSim [128]|2023|Behavior Simulation|Long-term interactive traffic simulator.|


### **2.2. Metric** 

Tab. 3 presents metrics previously used in DWM research. In most DWM research, the objectives are largely indistinguishable from those of standard generative tasks. Researchers prioritized the global similarity between data synthesized by the DWM and ground-truth (GT) data. A model exhibiting higher generation fidelity (or lower error) is deemed to have more effectively acquired the world knowledge inherent in driving scenarios. Consequently, during this stage, the capabilities of DWMs are predominantly evaluated using generative metrics. Specifically, video generation tasks utilize FID and FVD to quantify the 

divergence between the generated and GT data. Point cloud generation tasks employ CD to measure the average bidirectional nearest neighbor distance between the generated and GT point sets. Meanwhile, occupancy generation tasks relie on IoU and mIoU to assess the degree of volumetric overlap between the generated and GT occupancy grids. 

However, generative metrics often place disproportionate emphasis on low-level scene details, thereby obscuring the evaluation of the model’s ability to internalize underlying environmental dynamics. Therefore, several benchmarks introduce additional metrics to conduct a multidimensional assessment of DWM generation quality. For 

3 

Table 2. High-impact datasets. # Scene reflects the dataset diversity, while Duration indicates the dataset scale. 

|Dataset|# Scene|Duration (h|)<br>Example|
|---|---|---|---|
|KITTI [31]|22|1.5|[158]|
|Waymo [106]|1k|6.4|[36]|
|Arg 2 LiDAR [130]|20k|167|[36]|
|nuScenes [7]|1k|5.5|[32] [149] [173] [138] [141] [177]|
|nuPlan [38]|-|1200|[45]|
|NAVSIM [15]|115k|-|[11,68,69,157,170]|
|OpenScene [12]|-|120|[155] [87]|
|Occ3D-nuScenes [111]|1k|5.5|[167] [105] [4] [119] [138]|
|OpenDV-YouTube [142]|-|1700|[27] [142]|
|OpenDV-2K [142]|-|2059|[90]|
|Cityscapes [13]|25k|12.5|[56]|
|OpenOccupancy [121]|1.1k|5.5|[148] [127] [59] [9]|
|DIVA[174]|135|121|[174]|
|DrivingDojo [124]|18k|150|[41]|
|ACT-Bench [3]|2.3k|-|-|
|Cam4DOcc [84]|24k|-|[148]|
|UniOcc [126]|2.2k|14.2|-|
|Bench2Drive [50]|10k|-|[63] [151]|
|WorldSimBench [98]|36k|-|-|


instance, ACT-BENCH [3] employs ADE and FDE to determine if the generated videos follow behavioral commands, whereas WorldSimBench [98] utilizes various metrics (e.g., AE, IA, PV, TJ, KE, and SF) to evaluate different video properties relevant to AD, such as video quality, controllability, and path validity. 

Finally, DWMs can be indirectly assessed by evaluating the performance of the frameworks into which they are integrated. Comparing planning performance is a common paradigm for gauging the impact of DWMs on the overall framework. For example, metrics such as L2 and Col. in open-loop evaluation, and DS and SR in closed-loop evaluation, are all applicable in related studies. This broad applicability underscores the flexibility and generalization capabilities of DWMs. Furthermore, evaluation on various downstream tasks can also serve to validate the quality of DWM-generated data [122, 129, 150] while also reflecting the generalizability of pre-trained DWMs [20, 87, 104, 126, 149]. 

## **3. DWM Taxonomy** 

DWMs involve driving scenarios of various modalities, such as video, point clouds, occupancy, latent features, and traffic map. Each modality offers distinct advantages as well as corresponding challenges. This section reviews the latest research progress in DWMs from the perspective of prediction modalities and summarizes the development pathways of these models for each modality. 

### **3.1. DWM in Visual Space** 

Video data offers distinct advantages, including low acquisition costs, high resolution, and rich semantic and textural information, making video-targeted DWM a pivotal research direction. However, its reliance on pixel distribu- 

tions to indirectly represent observed 3D space often compromises localization accuracy. Furthermore, the susceptibility of camera sensors to environmental variables, such as adverse weather and fluctuating illumination, limits their robustness in complex driving scenarios. The core objective of video-targeted DWMs is to learn spatiotemporal dynamics and physical laws from visual inputs via driving video prediction. Early approaches [29, 42, 94] are constrained by the generative techniques available at the time, and are therefore trained and evaluated within simulated scenarios. In recent years, the application of generative technologies [65, 95, 100] has propelled video-targeted DWMs toward predicting complex real-world scenes. 

Diffusion-based DWMs [24, 65, 122, 129] demonstrate superior generation capabilities characterized by finegrained controllability. Based on several reference frames, they can synthesize photorealistic long-term driving videos of diverse environments and views that adhere to multimodal instructions, including layouts, 3D boxes, and actions. This paradigm aims to achieve the goal of generating high-fidelity, flexibly controllable, and spatiotemporally consistent driving videos. 

Conditions provide Diffusion-based DWMs with motion and scene priors. Through improved alignment with generative modules, these conditions enable flexible controllability and high-quality generation. For example, SimGen [174] and Dreamland [88] transform diversityconstrained scene conditions into forms that better conform to real-world distributions, while DriveDreamer-2 [163] converts textual instructions into structured conditions, enabling accessible control of complex driving scenes. Additionally, GAIA-2 [102] and Vista [27] establish multi-level scene control mechanisms via diverse conditions, while UniMLVG [10] fuses text instructions with 3D conditions, thereby supporting diverse generation paradigms. To enhance realism, DrivePhysica [150] introduces physical priors, such as global coordinates, as control conditions. Furthermore, predicting spatial-aware representations beforehand to provide 4D prior [8, 48, 82] also significantly improves spatial plausibility and spatial consistency. 

On the other hand, advancements in model architectures and training strategies significantly advance the spatiotemporal consistency of DWMs. Specifically, DriveWM [125] introduces a masked view prediction task, whereas MagicDrive-V2 [25] and DiVE [52] design view interaction modules. These architectures model multiview correlations, significantly improving the consistency across multiple views in the predicted videos. For long-horizon generation, multi-temporal granularity prediction mechanisms are introduced to enhance stability and improve performance. For instance, InfinitiDrive [37] achieves efficient spatiotemporal modeling through parallel branches with distinct sampling rates, while MiLA [114] 

4 

Table 3. Multi-dimensional metrics. _↑_ indicates better performance with higher values, while _↓_ indicates better performance with lower values. 

|Metric|_↓_or_↑_|Task|Description|
|---|---|---|---|
|Fr´echet Inception Distance (FID)|_↓_|Image / Video Generation|Feature distribution distance between the predicted and GT images.|
|Fr´echet Video Distance (FVD)|_↓_|Video Generation|Feature distribution distance between the predicted and GT videos.|
|Chamfer Distance (CD)|_↓_|Point Cloud Generation|Average bidirectional nearest neighbor distance between the predicted and GT point clouds.|
|Displacement Error (L2)|_↓_|Open-loop Planning|L2 distance between the predicted and GT trajectory.|
|Collision Rate (Col.)|_↓_|Open-loop Planning|Rate of collisions that occur with other objects when following the predicted trajectory.|
|Average Displacement Error (ADE)|_↑_|Video Generation|Average point-wise error between actual and predicted trajectories.|
|Final Displacement Error (FDE)|_↑_|Video Generation|Error between the actual and predicted positions at the final time step.|
|Aesthetics (AE)|_↑_|Video Generation|Visual quality of generated video.|
|Instruction Alignment (IA)|_↑_|Video Generation|Whether the video aligns with the provided instruction.|
|Perspectivity (PV)|_↑_|Video Generation|Whether the video has spatial realism.|
|Trajectory (TJ)|_↑_|Video Generation|Whether the movement and the trajectory of elements in the video are logical.|
|Key Element (KE)|_↑_|Video Generation|The generated quality of embodied elements.|
|Safety (SF)|_↑_|Video Generation|Whether the behavior of the vehicles complies with traffic rules.|
|Intersection over Union (IoU)|_↑_|Occupancy Generation|Ratio of the intersection and union between the predicted and GT occupancy.|
|Mean IoU (mIoU)|_↑_|Occupancy Generation|Average of IoU values across all categories.|
|Route Completion (RC)|_↑_|Closed-loop Planning|Percentage of the route completed by ego.|
|Infraction Score (IS)|_↑_|Closed-loop Planning|Initialized at 1.0 and decreases by a penalty coefficient for each Infraction.|
|Driving Score (DS)|_↑_|Closed-loop Planning|Product of RC and IS for each sample.|
|Success Rate (SR)|_↑_|Closed-loop Planning|Proportion of routes completed successfully on time and without traffic violations.|
|Efficient (Effi.)|_↑_|Closed-loop Planning|Mean of ego speed versus average surrounding traffic speed ratio per sampling point.|
|Comfortness (Comf.)|_↑_|Closed-loop Planning|Ratio of smooth trajectory segments to the total number of segments.|


and LongDWM [123] establish a coarse-to-fine progressive paradigm. In addition, Epona [157] employs multi-round propagation conditioned on generated frames, enhancing adaptation to errors during long-horizon rollouts and mitigating degradation phenomena. 

Another pathway, Autoregressive-Transformer-based DWMs, explores handling multiple tasks within a unified sequence. These approaches aim to facilitate the integration of world knowledge learned from generation and driving tasks, thereby enhancing overall performance. In detail, GAIA-1 [43] demonstrates that DWMs can learn scene distributions from large-scale data, while DrivingGPT [11] and DrivingWorld [45] refine the unification of scene and action representations. Furthermore, Doe-1 [168] shifts focus towards the closed-loop unified modeling of perception, prediction, and planning tasks. 

In conclusion, the advancement of vision-targeted DWMs presents distinct challenges in modeling rapid scene dynamics and ensuring multi-view spatial consistency. With the development of generative technologies, research paradigms evolve from simulator-based training to leveraging robust generative baselines. Diffusion-based approaches successfully enhance fidelity and controllability, while Autoregressive Transformer architectures pioneer the unified modeling of diverse driving tasks within a single sequence. However, achieving robust long-horizon video generation without error accumulation and effectively embedding rigorous physical laws to support reliable closed-loop decision-making in open-world scenarios remains a pivotal area yet to be fully realized. 

### **3.2. DWM in 4D Space** 

4D data refers to data modalities that comprise 3D spatial and 1D temporal information. These data inherently preserve structural consistency, detailed geometric information, and precise spatiotemporal dynamics, and are extensively adopted in AD research [72, 112, 172], emerging as a pivotal focus in the development of DWMs. Here, we introduce primary 4D data modalities (i.e., point cloud sequence and occupancy sequence), and review the corresponding DWM research within their respective domains. 

**Point Cloud.** LiDAR sensors acquire point clouds through laser reflection, ensuring robustness against environmental interference such as low illumination and smoke. In contrast to 2D pixels, point clouds provide precise depth measurements and explicit geometric structure, which are essential for achieving high-fidelity 4D generation. However, the intrinsic irregularities of this data, particularly sparsity and lack of ordered topology, present substantial difficulties for modeling in long-horizon and highly dynamic scenarios. 

The core challenge in point cloud forecasting lies in accurately predicting the geometric evolution within continuous 3D space. Direct regression of 3D point coordinates is not only computationally prohibitive but also highly sensitive to sensor-specific characteristics. To address this, Bird’s-Eye-View (BEV) representations serve as a promised dimensionality reduction solution, projecting sparse, unordered 3D points onto structured grids to lower complexity while preserving spatial topology. Copilot4D [158] encodes unstructured point cloud data into discrete BEV token sequences, demonstrating a scalable method for point-cloudtargeted DWMs. Additionally, the viewpoint retention of 

5 

BEV facilitates modality transformation. For instance, ViDAR [149] constructs a vision-to-point-cloud forecasting framework via BEV, achieving broad generalization across various downstream tasks. Taking a step further, HERMES [173] unifies point cloud forecasting, driving planning, and scene question answering, while integrating textual world knowledge into the prediction of BEV features. As a result, it enables a synergistic interplay between understanding and generation. 

The ray-scanning mechanism of LiDARs inevitably results in a significant reduction in point density at long ranges, whereas the BEV representation projects features onto uniform grids. Due to the misalignment between grid uniformity and the inherent divergence of sensor beams, this transformation often results in the loss of detail for distant objects. To address this, LiSTAR [79] introduces a raycentric representation paradigm that aligns with the sensor’s native scanning geometry, mitigating morphological distortion and enabling the generation of 4D point cloud scenes that are both physically realistic and precisely controllable. Similarly, LaGen [171] processes point clouds into more compact range images via spherical projection, facilitating spatiotemporally consistent long-range point cloud prediction. 

Point cloud DWMs extend beyond merely comprehending scene dynamics and forecasting future evolution, while facilitating the synthesis of 4D driving scenes characterized by physical plausibility, temporal consistency, and finegrained controllability. Specifically, LidarDM [178] synthesizes background and object point clouds, selecting suitable paths to compose them into dynamic scenes. While capable of autonomously generating point cloud digital assets, it remains dependent on real trajectory data. In contrast, LiDARCrafter [71] establishes a multi-stage pipeline spanning from trajectory and object generation to dynamic scene construction, thereby enabling dynamic point cloud synthesis and fine-grained editing driven solely by language instructions. In addition, U4D [139] employs a hard-to-easy two-stage generation strategy to improve reconstruction in uncertain regions, such as fine-grained structures and distant areas, effectively reinforcing the overall reliability of 4D point cloud synthesis. 

In the research of point cloud forecasting, the inherent sparsity and topological disorder of point cloud data pose significant challenges to efficient spatiotemporal modeling. To address this, the adoption of representations such as BEV, ray-based representations, and range images successfully strikes a balance between computational scalability and topological structure preservation. In the realm of 4D scene generation, research paradigms gradually transition from individual digital asset generation to full-scene generation, capable of fine-grained editing, which further enhances reliability in complex regions. However, model- 

ing rare events or high-complexity environments, alongside the development of 4D generation paradigms that simultaneously balance accuracy and efficiency, remains a pivotal area yet to be explored. Transforming point clouds from the spatial domain [73] to the spectral domain represents a promising solution. 

**Occupancy.** Occupancy data represents 3D scenes through voxelization, which determines the existence of objects within discrete volumetric units. By assigning semantic labels to each occupied voxel, this representation constitutes semantic occupancy. A critical advantage of occupancy lies in its emphasis on geometric structure over predefined categorization. This property enables the explicit modeling of general obstacles independent of predefined taxonomies, a capability that facilitates collision avoidance for open-vocabulary objects. Its capacity for geometrically consistent volumetric modeling and structured spatial encoding makes occupancy exceptionally suitable for modeling 4D scene evolution, leading to its widespread adoption. 

Different objectives correspond to different generation paradigms. Diffusion-based paradigms [4, 32, 105, 119] typically encode occupancy into noisy continuous features. Under the guidance of multimodal conditions, these methods utilize core frameworks, such as Diffusion Transformers [95], to forecast future states, thereby achieving highquality generation characterized by realism, controllability, and temporal consistency. In contrast, AutoregressiveTransformer-based paradigms [127, 138, 141, 155, 167] encode occupancy scenes into latent space and serialize them with data of other modalities (e.g., trajectories and text) into a unified sequence. By leveraging the next-tokenprediction mechanism, these approaches unify diverse tasks ranging from scene prediction and behavior planning to Occupancy Question Answering. Additionally, OccTENS [54] applies the next-scale-prediction paradigm [110] to 4D occupancy prediction, exploring a novel autoregressive generative paradigm. 

Despite the outstanding performance of these occupancy-targeted approaches, they suffer from severe performance degradation when relying solely on visual inputs, a limitation that significantly impedes their deployment in end-to-end AD systems. To address this challenge, RenderWorld [141] devises a self-supervised image-tooccupancy translation module, while Cam4DOcc [84] explores end-to-end vision-to-4D occupancy forecasting. Furthermore, Drive-OccWorld [148] constructs a vision-to-occupancy DWM adapted to diverse control conditions, integrating it with a planner to select the optimal trajectory. Although challenging, the paradigm of vision-to-4D occupancy forecasting is demonstrated to enhance DWMs to capture precise spatiotemporal dynamics from visual inputs. Accordingly, it is leveraged for 4D pre-training [86, 87] and demonstrates effective 

6 

generalization across diverse downstream tasks. Additionally, PreWorld [66] utilizes video data for 4D pre-training, enhancing semantic supervision while showcasing the potential for scaling to significantly larger datasets. 

Real-world scenarios are dominated by extensive static backgrounds, which not only hold minimal relevance to driving behaviors but also interfere with the prediction of dynamic objects. Hence, decoupling strategies are widely adopted in occupancy-targeted DWMs. For example, OccLLM [138] encodes static backgrounds and dynamic objects separately, thereby shifting the computational focus towards the evolution of dynamic trajectories. Similarly, DFIT-OccWorld [155] and GaussianWorld [177] predict exclusively dynamic objects and newly observed regions, while the state changes of the static scene are directly mapped via pose transformations. These object-background decoupling approaches are simple and effective, but they remain constrained by predefined semantic labels, making it difficult to accommodate the complex dynamics in realworld driving situations. Rather than conducting objectspecific predictions, implicit decoupling strategies [85, 137] estimate the global state transitions induced by the coupling of ego-motion and object dynamics. This approach not only enhances modeling efficiency but also prevents the omission of details. Moreover, other methods [54, 77] simultaneously model inter-frame dynamics and intra-frame structure, further bolstering spatiotemporal modeling capabilities and controllability. 

On the other hand, constructing rational and flexible 4D scene representations constitutes another pivotal strategy for enhancing model efficiency. BEV representations are widely adopted [32, 66, 105, 127, 148, 155] due to their effective compression of spatial complexity. Furthermore, OccProphet [9] augments BEV with height and global features and preserves 3D structural information, whereas DTT [137] and DynamicCity [4] employ multiplane projection representations. More recently, sparse representations [14, 20] have garnered increasing attention. This paradigm models state transitions by leveraging a set of queries that adaptively traverse and interact with the original scene, exhibiting superior flexibility and holding significant potential for scaling to large-scale 4D scenes. In addition, UNO [1] and DIO [17] leverage a novel 4D occupancy form, continuous occupancy fields, instead of occupancy grids. They sampled both occupied and non-occupied points, ensuring a balanced data distribution while simultaneously enhancing computational efficiency and structural granularity. 

In conclusion, the evolution of occupancy-targeted DWMs is driven by the dual pursuit of robust, realistic 4D prediction and multi-task unification. While the occupancy paradigm enables precise representation, it simultaneously introduces challenges regarding significantly 

increased computational complexity and data acquisition costs. To address this, existing research has adopted strategies such as decoupled prediction and sparse representations, achieving remarkable results in processing efficiency. Nevertheless, despite attempts to leverage video data, the scarcity of direct large-scale 4D data persists. Addressing this data gap remains a significant objective for future work. 

### **3.3. DWM in Multimodal Space** 

Visual data provides high-resolution texture and rich semantics, whereas 3D data captures precise spatiotemporal dynamics and inter-object relationships. Although these modalities prioritize different attributes, they describe the same underlying physical reality, permitting mutual translation and synergistic integration. The implementation of this concept has emerged within single-modal generative DWMs. For instance, video-targeted DWMs [48, 82, 159] integrate spatial representations into their pipelines to enhance layout accuracy and spatial consistency, while 4Ddata-targeted DWMs leverage visual data to facilitate training [93, 155] or to forecast future 4D scenes conditioned on visual observations [86, 87, 149, 173]. However, these methodologies remain focused on single data modalities, rendering them inadequate for the multi-sensor, multimodal operational architectures of modern AD systems. To address this gap, Multimodal generative DWMs are proposed, which entail forecasting future scenes across diverse data modalities, including video, occupancy, point cloud, depth, and even traffic maps. While this paradigm confronts the significant challenge of inherent data heterogeneity, it simultaneously offers the potential to leverage the intrinsic correlations that naturally exist between modalities of the same scene. 

A fundamental challenge in multimodal DWMs is constructing a unified representation that can simultaneously capture both spatiotemporal dynamics and semantic information. Since depth maps and monocular videos share the same views, effective fusion can be readily achieved via direct concatenation [41, 56, 131]. In contrast, fusing multi-view videos with 4D scene data, such as occupancy and point clouds, presents a substantially greater challenge due to the significant heterogeneity in their representational modalities. MUVO [5] addresses this by employing sequence concatenation and self-attention mechanisms to fuse multimodal information, while UMGen [132] unifies the modeling of images and traffic maps within an autoregressive framework and fuses them with cross-attention blocks. On the other hand, NeMo [47] constructs volumetric representations for detailed object modeling. More recently, capitalizing on the ability of BEV to preserve geometric spatial correspondences across diverse views, mainstream methodologies [104, 109, 160] construct the unified multimodal data in BEV representations, thereby facilitating the 

7 

comprehensive fusion and mutual enhancement of multimodal predictions. Furthermore, GaussianDWM [16] utilizes language guidance to sample from dense Gaussian Splatting [166], thereby establishing a joint image-depth generation framework that integrates world knowledge with visual features. 

Despite the scalability and flexibility of the unified representations, the single-step fitting paradigm often struggles to characterize the complex data distribution characteristics inherent in real-world driving scenarios. To address this, some approaches [59, 60, 83] introduce 4D semantic occupancy as the intermediate prediction targets to model these complex distributions, achieving large-scale and physicsaware data synthesis through hierarchical generation strategies. 

In addition, the interaction mechanisms between different modal representations constitute another promising direction for exploration. Unlike the conventional practice of interacting via a unified representation, UniFuture [75] derives depth representations from visual features and establishes adaptive interaction through feedback branches, thereby achieving a mutual reinforcement between perception and generation. Similarly, HoloDrive [134] constructs separate generators for video and point clouds and fuses multimodal information via dual projecting. This mechanism of adaptive interaction with decoupled representations demonstrates the potential for better accommodating modal biases, yielding superior quality in the generation process. 

In summary, multimodal DWMs represent a pivotal breakthrough that bridges the semantic richness of visual data with the geometric precision of 3D representations, effectively addressing the limitations inherent in the heterogeneity of single-modal frameworks. However, most methods remain confined to specific modality combinations. Future foundational multimodal DWMs are expected to learn modality-agnostic world dynamics from observational data, thereby supporting the generation and transformation of arbitrary modalities. 

### **3.4. DWM in Latent Space** 

Distinct from paradigms that strive for high-fidelity prediction of real-world scenes, latent DWMs focus on predicting latent representations fitting task-oriented AD frameworks. This design affords greater architectural flexibility, thereby effectively empowering AD research. 

Latent DWMs can be seamlessly integrated into existing frameworks, enhancing their performance. For instance, LAW [68] and World4Drive [170] predict future scene features conditioned on planned trajectories, enabling joint self-supervised training of scene perception and motion planning. AdaWM [115] adaptively fine-tunes the planner by evaluating the discrepancy between the latent DWM’s predictions and the true next states, significantly improving 

adaptability to novel scenes. Moreover, LatentDriver [136] injects latent DWM outputs into the planner to synthesize physically plausible stochastic driving behaviors. Furthermore, DINO-Foresight [55] and AD-L-JEPA [175] concentrate on high-level semantic representation learning rather than low-level detail noise. This strategy not only mitigates the interference of scene noise on the learning of high-level semantics but also supports scalable multi-task processing and modular integration. 

Beyond serving as model components, latent DWMs also significantly augment training environments. By leveraging parallel rollouts, Think2Drive [63] and Raw2Drive [151] simulate hundreds of potential trajectories at each simulation step, yielding forward-looking, dense feedback signals. From another perspective, Popov et al. [96] introduce stochastic disturbances within closedloop driving scenarios, thereby training the agent to recover from accumulated shifts robustly. 

In addition, Latent DWMs demonstrate significant potential for incorporating reasoning paradigms [35]. By enabling flexible reasoning and rethinking within the latent space, these approaches [76, 107] can effectively tackle challenging tasks, such as ambiguous instructions and complex multi-agent interactions. This capability leads to safer and more forward-looking planning, while mitigating the visual information loss and computational inefficiency often associated with text-based Chain-of-Thought strategies. 

Collectively, latent DWMs are creatively integrated with a diverse array of AD paradigms. Functioning variously as auxiliary training objectives, model components, or closedloop simulation environments, they have introduced a significant shift in existing research paradigms. However, the divergence between latent prediction targets and physical sensory observations limits model interpretability. Although this abstraction favors strong correlations with specific tasks, it simultaneously introduces the risk of representation degeneration, where features may become detached from physical reality. While some approaches have acknowledged and tried to address this issue [63, 76, 151], developing mechanisms to ground latent predictions effectively remains a critical imperative for future investigation. 

### **3.5. DWM in Vectorized Space** 

The vectorized space comprises low-dimensional scene representations (e.g., traffic maps) synthesized using privileged data. In this paradigm, raw sensory processing is bypassed. Instead, traffic participants are abstracted as geometric primitives with specific dimensions, while traffic indications are encoded as discrete control signals. The inherent sparsity of this low-dimensional representation empowers DWMs to effectively model the diverse behaviors and complex multi-agent interactions within the scene. 

The first pathway focuses on generative traffic simula- 

8 

tion. Traditional rule-based traffic simulations [19] struggle to adaptively adjust behaviors, often exhibiting rigid and unrealistic patterns, and are prone to accumulating errors in closed-loop simulations due to their lack of self-correcting capacity. In contrast, Trafficbots [161] enables the simulation of autonomous behaviors for multi-agent systems by endowing each agent with a private attribute context and a shared scene context. Recently, the application of diffusion models [65, 95, 100] provides a new impetus for closedloop generative traffic simulation [53, 78, 101, 103, 108], propelling the field toward large-scale, diverse, and precisely controllable developing directions. 

Another pathway tends to infer multi-agent behavior from real-world observation and enhance ego planning. AdaptiveDriver [113] predicts the behavioral traits of each agent individually to derive future trajectories, thereby empowering rule-based planners. In a different approach, CarFormer [40] models holistic driving context information within a unified Autoregressive Transformer framework, integrating the features of each object into separate slots [133]. In addition to modeling the behavior of individual agents, PIWM [28] constructs a multi-agent interaction mechanism, which more accurately characterizes interagent interactions and their impact on the ego vehicle. 

Distinct from real-world approaches that aim for scene fidelity and physical simulation, DWMs in low-dimensional vectorized space emphasize behavioral fidelity and intent simulation. The success of these frameworks demonstrates the existence of intrinsic regularities in driving behavior that can be internalized. The future integration of these models with physical-world DWMs constitutes a promising path for constructing comprehensive, closed-loop endto-end DWMs. 

## **4. DWM Application** 

DWMs are highly flexible and widely used in various research areas, with their controllable generation enabling them to serve as effective neural simulators and data generators. By learning real-world dynamics, these models can adapt to different tasks or even combine generation and planning in a single framework. Furthermore, DWMs help traditional planners achieve better long-term results by overcoming the limits of immediate observations. This section provides a categorized overview of various DWM applications in the field of AD. 

### **4.1. Simulation** 

Simulators constitute a pivotal instrument within the AD domain, affording a mechanism to simulate reproducible and complex driving scenarios within virtual environments. This significantly attenuates training and evaluation costs, enhances safety, and establishes a platform for equitable benchmarking. While engine-based simulators, such as 


Figure 3. DWM-based simulation. (a) Future scene simulation following multimodal instruction. (b) Generative traffic simulation and editing. (c) Closed-loop simulation providing photorealistic observation. 

CARLA [19] and NAVSIM [15], have substantially propelled advancements in AD research, they remain constrained by their reliance on fixed digital assets, suboptimal photorealism, and limited diversity. The potent generative capabilities of DWMs hold promise for addressing the deficiencies inherent in traditional simulators, delineating the trajectory for the next generation of generative simulators. 

Extensive research across diverse modalities, including video [24, 25, 27, 144], point cloud [71, 158, 171, 178], and occupancy [32, 119], has demonstrated that DWMs possess robust generative capabilities and instruction-following proficiency, thereby establishing a solid foundation for highfidelity simulation. Through training with massive realworld data, these approaches can synthesize complex yet reasonable object distributions and visual textures that remain elusive for conventional graphics-based simulators. 

As illustrated in Fig. 3(a), DWM-based simulators synthesize dynamic driving environments directly from raw observations [27, 43, 67, 158, 167] and structural conditions [24, 25, 119, 122, 178], in contrast to conventional engine-based simulators that necessitate laborious manual asset creation, which suffer from high development costs and alleviates the constraints of limited scenario diversity. DWM-based simulators accommodate a diverse spectrum of control modalities and granularities. For instance, Vista [27] and Drive-OccWorld [148] accept 

9 


Figure 4. DWM-based data generation. (a) DWM generates data of the same layouts but diverse environments. (b) DWM generates novel views of the same scene. (c) Different DWMs support the generation of various data modalities. 

high-level intent directives such as navigational commands, alongside low-level behavioral constraints including trajectories, steering angles, and speeds, GEM [41] enables precise manipulation of object distributions and pedestrian poses, while DriveDreamer-2 [163], Dreamland [88], and Talk2Traffic [103] further facilitate interactive scene editing via language prompts. In addition, DWMs support the synthesis of details unspecified by instructions, ensuring that induced transitions are both coherent and physically plausible. The cost-effectiveness, ease of use, and flexible controllability inherent in this generative paradigm significantly streamline the simulation pipeline, lowering the barrier to entry sufficiently to permit usage by non-expert personnel. 

Traditional simulators typically rely on vehicle trajectories harvested from real-world driving data. This dependence not only incurs high acquisition costs and struggles to cover long-tail distributions but also introduces domain gaps when compositing trajectories with simulated backgrounds, thereby compromising the fidelity of the simulation environment. DWMs present a promising avenue for mitigating these limitations. As shown in Fig. 3(b), generative traffic simulation [53, 78, 101, 103, 161] is leveraged to endow all agents within a scene with plausible driving behaviors. SceneDiffuser++ [108] further escalates the simulation scale to the city level, encompassing the full driving duration, whereas MARL-CCE [97] focuses on modeling competitive driving interactions. Furthermore, As shown in Fig. 3(c), integrating traffic simulators with scene simulators [140, 147] facilitates the construction of closed-loop driving, thereby significantly enhancing both the degrees of freedom and the realism of the simulation. 

Fundamentally, DWM-based simulators function as learnable models rather than static assemblages of fixed digital assets and predefined behaviors. This distinction significantly broadens their applicability within AD research. Possessing inherent world knowledge and predictive capabilities, these models facilitate the direct evalua- 

tion of trajectories [27] and the estimation of training rewards [63, 144, 151], while also enabling the forecasting of environmental feedback over future horizons [30]. Furthermore, the differentiability of their outputs permits comprehensive supervision by aligning predictions with observations [68, 96, 115]. Their support for parallel rollouts enables the efficient simulation of the stochasticity inherent in driving, thereby yielding rich and dense supervisory signals [63, 96, 151]. Finally, DWMs can be jointly trained with a planner to construct customized environments, then effectively distill teacher-planner knowledge into students [169]. 

In summary, DWMs not only establish a simulation pipeline characterized by superior fidelity, cost-efficiency, and controllability but also expand the frontiers of simulation tasks, fostering a deeper synergy with AD research. However, the reliability issues inherent in generative simulation constitute a significant bottleneck that restricts its widespread adoption. Although recent works [144] have attempted to address this challenge, achieving a definitive solution remains an open problem that requires further exploration. 

### **4.2. Data Generation** 

Data serves as the cornerstone of neural network research, with real-world datasets such as KITTI [31], Waymo [106], and nuScenes [7] standing as pivotal pillars in the AD domain. However, due to the prohibitive costs and inherent risks associated with data collection, existing datasets suffer from significant limitations. Taking the nuScenes dataset as an example, its total duration of merely 5.5 hours is significantly shorter than the empirical experience of an average human driver. Furthermore, it exhibits a highly skewed data distribution, with approximately 70% of scenarios featuring straight lines. It also lacks sufficient diversity, failing to capture extreme scenarios such as dangerous maneuvers or traffic accidents. These deficiencies severely impede the 

10 


Figure 5. DWMs enhance driving. (a) DWMs evaluate candidate actions and choose the best one. (b) DWMs provide dense scene supervision for the planner through back-propagation. (c) DWMs unify prediction and planning. (d) DWMs enable reasoning with future prediction. 


Figure 6. DWMs enable 4D pretraining. DWM learns world representation through forecasting the future, then improves performance on downstream tasks. 

advancement of AD research. In response, DWMs explore a cost-effective method to mitigate these challenges. 

As illustrated in Fig. 4(a), DWMs can synthesize diverse driving videos conditioned on a unified set of structured inputs [65, 122, 129, 150, 163]. This effectively mitigates the scarcity of long-tail scenarios in real-world datasets, such as nighttime, rainy weather, and diverse cityscapes. Furthermore, this synthetic data can be directly utilized to train downstream tasks, yielding significant performance improvements. A distinct paradigm shown by Fig. 4(b) focuses on novel views. Some approaches [26, 81, 93] directly employ DWMs to synthesize 3D Gaussian Splatting (3D-GS) [57] scenes that enable arbitrary viewpoint sampling, while others [89, 162] utilize DWMs to generate video data featuring diverse driving behaviors, thereby facilitating the training of 3D-GS reconstruction frameworks. 

In parallel, DiST-4D [36] utilizes a decoupled spatiotemporal diffusion framework to achieve both future temporal prediction and arbitrary view synthesis. Additionally, TeraSimWorld [117] supports the construction of diverse adversarial scenarios at arbitrary geographic locations, effectively generating corner cases and mitigating the data scarcity inherent in long-tail distributions. 

The acquisition cost of 3D data, such as point clouds and occupancy grids, is significantly higher than that of driving videos. In addition to content distribution skew, driving datasets suffer from severe modal imbalance. DWMs illustrated by Fig. 4(c) effectively lower the barrier to acquiring 3D data. Point-cloud-targeted paradigms [44, 71, 178] support the generation of realistic scene appearance and faithfully simulate sensor noise. Meanwhile, occupancytargeted DWMs [4, 119, 141] enable the synthesis of scalable, dense 4D scenes enriched with semantic labels. Finally, multimodal DWMs [2, 59, 75, 131, 134] facilitate the generation of high-quality aligned multimodal data or the translation of existing modalities, thereby supporting selfsupervised learning paradigms and large-scale research into multi-sensor AD. 

Constrained by prohibitive costs and inherent safety risks, real-world driving datasets struggle to achieve a balanced and diverse distribution across scenarios, behaviors, and modalities. In contrast, DWMs offer a promising, costeffective path to address this data bottleneck. They not only synthesize critical corner cases to enhance data coverage but also serve to diversify and augment existing datasets. Nevertheless, generating high-resolution scenes remains computationally intensive, and purely synthetic data cannot yet 

11 

fully replace real-world data. Consequently, improving synthesis efficiency and further elevating data quality remain critical challenges to be addressed. 

### **4.3. Enhancing Driving** 

Conventional AD paradigms typically plan actions relying solely on historical context. Lacking an understanding of the consequences of their actions and the future temporal evolution of the scene, these models suffer from a deficiency in forward-looking planning and risk assessment. Although approaches such as UniAD [46] and VAD [51] incorporate prediction modules, they remain confined to predicting traffic participants. This approach not only necessitates intricate annotations of various aux-tasks but also overlooks the influence of ego-motion on the global observational environment. In contrast, the introduction of DWMs empowers planners to gain a deeper understanding of the relationship between ego-behavior and environmental dynamics, thereby enhancing the safety and foresight of driving. 

The most straightforward strategy to enhance planning involves integrating a DWM directly into the planning pipeline. As shown in Figure 5(a), the planner generates multiple candidate trajectories, for which the DWM predicts the resulting scene evolution. Rewards or costs are then derived from these predicted futures to select the optimal decision. While similar approaches [61, 69, 125, 148] yield significant gains in planning performance, the requirement for multiple planning and prediction iterations at each step severely impedes the runtime efficiency of the AD system. Furthermore, this sample-and-filter paradigm essentially shifts the planning task from a pass@1 to an approximate pass@K regime, masking the planner’s deficiencies rather than enhancing its intrinsic capabilities. In contrast, PWM [165] and SeerDrive [154] utilize DWMs to predict future scenes prior to planning, enhancing the planner’s foresight by extending the input context. Furthermore, as illustrated in Figure 5(b), other approaches [68, 96] integrate planning outputs into the training pipeline. By aligning predicted scenes with GT observations, these methods provide denser supervision for the planner, thereby improving its performance without imposing additional computational overhead during inference. 

As presented by Fig. 5(c), unifying planning and prediction tasks represents a more elegant solution, adhering closely to the end-to-end philosophy. Autoregressive Transformer frameworks [11, 43, 45, 102, 167] unify these tasks under the next-token prediction paradigm, directly internalizing the comprehension of dynamic driving scenes into the model itself to enhance planning capabilities. Recent advancements [127, 138, 168, 173] extend this by establishing a unified prediction-planning-understanding framework, where textual understanding tasks further re- 

inforce scene cognition and improve the interpretability of decision-making behaviors. Additionally, DriveLaw [135] further integrates prediction and planning within a unified representation. Finally, Fig. 5(d) illustrates the pathway to integrate this unified architecture with Chain-ofThought reasoning [107, 152], enhancing planning performance while enabling reflection and trial-and-error, thus demonstrating a promising trajectory for the development of DWM-based unified frameworks. 

In summary, DWMs are facilitating a paradigm shift in AD from direct reactive planning to foresight-driven scene cognition. While integrating DWMs as auxiliary modules significantly enhances performance, constructing a unified model represents the definitive future trajectory for end-toend AD. However, unified architectures remain hindered by the gaps between distinct tasks and have not yet established a significant advantage over traditional methods. Therefore, designing flexible unified architectures capable of bridging these gaps and unleashing the potential of DWMs remains a pivotal research direction. 

### **4.4. Pre-training** 

Mainstream perception techniques, such as object detection, tracking, and depth estimation, are confined to learning representations of specific objects or isolated perspectives. Furthermore, their reliance on intricate annotations significantly impedes the effective utilization of large-scale datasets. In contrast, DWMs can capture faithful representations of the real world and learn the physical laws governing world dynamics [43] through learning to forecast scene evolution. Thus, pre-training on DWM tasks equips the model with comprehensive environmental cognition, enabling robust generalization performance across a diverse range of downstream tasks. 

Vision-only frameworks constitute a pivotal research trajectory within the domain of embodied intelligence, encompassing AD. However, recent research [145, 146] has demonstrated that constructing a comprehensive cognition of physical space solely from visual inputs presents substantial challenges. This difficulty is particularly acute in high-speed driving scenarios, where the precise perception of 3D geometry and temporal dynamics remains exceptionally demanding while paramount for driving safety. To address this challenge, DWMs [45, 86, 149] establish a vision-to-4D predictive pre-training paradigm illustrated by Fig. 6. By leveraging self-supervised learning on large-scale image-4D data pairs, these models effectively construct 4D dynamic representations. This approach has yielded significant performance gains across multiple downstream tasks, including 3D object detection [70], semantic occupancy prediction [112], and driving planning [46], validating the robust generalization capability of DWMs. Similarly, within the domain of 3D- 

12 

Table 4. Video generation performance on the nuScenes [7] validation set. MV means supporting multi-view forecasting. Core Arc. denotes the core architecture of the DWM. Auto. Tran. is Autoregressive Transfomer. MD means the max generation duration. 

|Method|Reference|MV|Resolution|Core Arc.|FID_↓_|FVD_↓_|MD (s)|
|---|---|---|---|---|---|---|---|
|MagicDrive [24]|ICLR 24|✓|224×400|Diffusion|16.2|-|-|
|DriveDreamer [122]|ECCV 24|✗|256×448|Diffusion|14.9|340.8|4|
|DrivingDiffusion [65]|ECCV 24|✓|512×512|Diffusion|15.8|332.0|-|
|Panacea [129]|CVPR 24|✓|256×512|Diffusion|17.0|139.0|-|
|Drive-WM [125]|CVPR 24|✓|192×384|Diffusion|15.8|122.7|8|
|WoVoGen [82]|ECCV 24|✓|256×448|Diffusion|27.6|417.7|3|
|GenAD [142]|CVPR 24|✗|-|Diffusion|15.4|184.0|4|
|Vista [27]|NeurIPS 24|✗|576×1024|Diffusion|6.9|89.4|15|
|BEVWorld [160]|arXiv 24|✓|-|Diffusion|19.0|154.0|-|
|InfinityDrive [37]|arXiv 24|✗|576×1024|Diffusion|10.9|70.1|120|
|HoloDrive [134]|arXiv 24|✓|-|Diffusion|13.6|103.0|-|
|DrivePhysica [150]|arXiv 24|✓|-|Diffusion|4.0|38.1|-|
|UniMLVG [10]|arXiv 24|✓|-|Diffusion|5.8|36.1|20|
|DrivingWorld [45]|arXiv 24|✗|512×1024|Auto. Tran.|7.4|90.9|40|
|<br>Doe-1 [168]|arXiv 24|✗|384×672|LLM|15.9|-|-|
|<br>DriveDreamer-2 [163]|AAAI 25|✓|256×448|Diffusion|11.2|55.7|-|
|UniScene (GT Occ) [59]|CVPR 25|✓|256×512|Diffusion|6.1|70.5|-|
|GEM [41]|CVPR 25|✗|320×576|Diffusion|10.5|158.5|15|
|MaskGWM-long [90]|CVPR 25|✗|-|Diffusion|4.0|59.4|-|
|MagicDrive-V2 [25]|ICCV 25|✓|848×1600|Diffusion|20.9|94.8|24|
|<br>DiST-T [36]|ICCV 25|✓|424×800|Diffusion|6.8|22.7|-|
|Epona [157]|ICCV 25|✗|512×1024|Diffusion|7.5|82.8|120|
|<br>DriVerse [67]|ACM MM 25|✗|480×832|Diffusion|18.2|95.2|15|
|OmniGen [109]|ACM MM 25|✓|-|Diffusion|22.2|-|-|
|<br>STAGE [118]|IROS 25|✗|768×512|Diffusion|11.0|242.8|-|
|MiLA [114]|arXiv 25|✓|-|Diffusion|3.0|18.2|10|
|CoGen [48]|arXiv 25|✓|360×640|Diffusion|10.2|68.4||
|GeoDrive [8]|arXiv 25|✗|-|Diffusion|4.1|61.6|-|
|MoVieDrive [131]|arXiv 25|✓|512×256|Diffusion|-|46.8|-|
|<br>UniScenev2 [60]|arXiv 25|✓|-|Diffusion|7.6|61.4|-|
|CVD-STORM [159]|arXiv 25|✓|256×448|Diffusion|3.8|14.0|20|
|UniFuture [75]|arXiv 25|✗|320×576|Diffusion|11.8|99.9|-|
|LongDWM [123]|AAAI 26|✗|720×480|Diffusion|12.3|102.9|11|


based framework research [1, 17, 175], DWMs likewise exhibit superior transferability. Furthermore, multimodal DWMs [47, 104, 160] jointly capture the geometric structure and visual semantic information of the environment. This capability mitigates modality bias, leading to a more holistic cognition and facilitating a broader spectrum of applications. 

Although the DWM-based pre-training paradigm has demonstrated robust generalizability and high data efficiency, its further expansion is impeded by the limited scale of aligned multimodal data. To address this, PreWorld [66] explores a pathway for pre-training spatial representations using abundant 2D data. Concurrently, other DWM studies are investigating the generation of aligned multimodal data [60, 99, 134]. Consequently, how to surmount these data constraints remains a pivotal direction for future research. 

## **5. DWM Performance** 

DWMs are widely adopted in the field of AD and have significantly advanced relevant research. To better illustrate this development, this section reviews the performance of representative works across major tasks. These tasks include video, point cloud, and occupancy generation, as well as open-loop and closed-loop planning. 

Table 5. Point cloud forecasting prtformance on the nuScenes [7] validation set. Core Arc. denotes the core architecture of the DWM. Avg. corresponds to the mean of the scores at 1s, 2s, and 3s. L and C separately denote Lidar and Camera. 

|Method|Reference|Core Arc.|Input|Cham|fer Di|stance|(_m_<sup>2</sup>)_↓_|
|---|---|---|---|---|---|---|---|
|||||1s|2s|3s|Avg.|
|Copilot4D [158]|ICLR 24|Diffusion|L|0.36|-|0.58|-|
|LiSTAR [79]|arXiv 25|Transformer|L|0.30|-|-|-|
|LaGen [171]|arXiv 25|Diffusion|L|0.61|0.81|1.08|0.83|
|ViDAR [149]|CVPR 24|Transformer|C|1.12|1.38|1.73|1.41|
|HERMES [173]|ICCV 25|LLM|C|0.78|0.95|1.17|0.97|
|DriveX-B [104]|ICCV 25|Transformerr|C|0.66|0.86|1.10|0.87|
|BEVWorld [160]|arXiv 24|Diffusion|L & C|0.44|-|0.73|-|
|HoloDrive [134]|arXiv 24|Diffusion|L & C|-|-|0.83|-|


### **5.1. Video Prediction** 

Driving video generation aims to predict future frame sequences from single or multiple views based on past observations and control signals. Generating high-quality and high-resolution results requires a balance between semantic logic and visual details. Additionally, the need for consistency across views and long-term prediction creates significant challenges for spatiotemporal dynamic modeling. Tab. 4 illustrates the performance of DWMs for the driving video generation task on the nuScenes [7] validation set. 

The final generative performance is influenced by various factors. For instance, structured conditions incorporate spatial priors while command conditions do not. Meanwhile, generating high-resolution and long-term content is significantly more challenging, resulting in lower FID and FVD scores compared to low-resolution and short-term content. The comparison presented in Tab. 4 is therefore not strictly fair. However, from an overall perspective, DWMs have achieved significant performance progress, delivering higher FID and FVD scores, greater resolution, and more stable long-term generation, demonstrating a major advance in the overall quality of generated video content. 

It is important to note that earlier models frequently exhibited FVD values significantly higher than their FID scores [65, 82, 122]. This difference suggested a lack of ability in temporal modeling. In contrast, recent studies simultaneously reduce both FID and FVD, significantly narrowing the gap between these two metrics [10, 123, 159]. This change shows that these models have evolved from understanding single frames to achieving coherent video perception. Furthermore, improvements in resolution and generation horizon suggest that these models are steadily moving toward simulating complete driving events. 

### **5.2. Point Cloud Prediction** 

The point cloud prediction task requires both the effective modeling of spatiotemporal dynamics and the integration of high-fidelity rendering techniques, which accurately em- 

13 

Table 6. Occupancy forecasting performance on Occ3D-nuScenes [111]. Core Arc. denotes the core architecture of the DWM. Auto. Tran. is Autoregressive Transfomer. Recon. denotes the score at current time step. Avg. corresponds to the mean of the scores at 1s, 2s, and 3s. O and C separately denote Occupancy and Camera. 

|Method|Reference|Core Arc.|Input||m|IoU (%)_↑_||||I|oU (%)_↑_|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||Recon.|1s|2s|3s|Avg.|Recon.|1s|2s|3s|Avg.|
|OccWorld-O [167]|ECCV 24|Auto. Tran.|O|66.38|25.78|15.14|10.51|17.14|62.29|34.63|25.07|20.18|26.63|
|OccSora [119]|arXiv 24|Diffusion|O|27.40|-|-|-|-|37.00|-|-|-|-|
|OccLLaMA-O [127]|arXiv 24|LLM|O|75.20|25.05|19.49|15.26|19.93|63.76|34.56|28.53|24.41|29.17|
|DFIT-OccWorld-O [155]|arXiv 24|Auto. Tran.|O|-|31.68|21.29|15.18|22.71|-|40.28|31.24|25.29|32.27|
|DOME-O [32]|arXiv 24|Diffusion|O|83.08|35.11|25.89|20.29|27.10|77.25|43.99|35.36|29.74|36.36|
|<br>RenderWorld [141]|ICRA 25|Auto. Tran.|O|-|28.69|18.89|14.83|20.80|-|37.74|28.41|24.08|30.08|
|<br>Occ-LLM [138]|ICRA 25|LLM|O|-|36.65|32.14|28.77|32.52|-|24.02|21.65|17.29|20.99|
|DynamicCity [4]|ICLR 25|Diffusion|O|40.79|-|-|-|-|-|-|-|-|-|
|<br>_I_<sup>2</sup>-World [77]|ICCV 25|Transformer|O|81.22|47.62|38.58|32.98|39.73|68.30|54.29|49.43|45.69|49.80|
|Liu. et. al. [80]|NeurIPS 25|Transformer|O|-|36.42|27.39|21.66|28.49|-|43.68|36.89|31.98|37.52|
|COME [105]|arXiv 25|Diffusion|O|-|42.75|32.97|26.98|34.23|-|50.57|43.47|38.36|44.13|
|OccTENS-O [54]|arXiv 25|Auto. Tran.|O|-|27.96|21.75|16.47|22.06|-|38.73|29.50|24.86|31.03|
|DTT-O [137]|arXiv 25|Transformer|O|85.50|37.69|29.77|25.10|30.85|92.07|76.60|74.44|72.71|74.58|
|OccWorld-S [167]|ECCV 24|Auto. Tran.|C|0.27|0.28|0.26|0.24|0.26|4.32|5.05|5.01|4.95|5.00|
|OccWorld-D [167]|ECCV 24|Auto. Tran.|C|18.63|11.55|8.10|6.22|8.62|22.88|18.90|16.26|14.43|16.53|
|OccLLaMA-F [127]|arXiv 24|LLM|C|37.38|10.34|8.66|6.98|8.66|38.92|25.81|23.19|19.97|22.99|
|DOME-F [32]|arXiv 24|Diffusion|C|75.00|24.12|17.41|13.24|18.25|74.31|35.18|27.90|23.44|28.84|
|DFIT-OccWOrld-V [155]|arXiv 24|Auto. Tran.|C|-|13.38|10.16|7.96|10.50|-|19.18|16.85|15.02|17.02|
|PreWorld [66]|ICLR 25|Transformer|C|-|12.27|9.24|7.15|9.55|-|23.62|21.62|19.63|21.62|
|RenderWorld [141]|ICRA 25|Auto. Tran.|C|-|2.83|2.55|2.37|2.58|-|14.61|13.61|12.98|13.73|
|Occ-LLM [138]|ICRA 25|LLM|C|-|27.11|24.07|20.19|23.79|-|11.28|10.21|9.13|10.21|
|_I_<sup>2</sup>-World [77]|ICCV 25|Transformer|C|25.13|21.67|18.78|16.47|18.97|32.66|30.55|28.76|26.99|28.77|
|DTT-F [137]|arXiv 25|Transformer|C|43.52|24.87|18.30|15.63|19.60|54.31|38.98|37.45|31.89|36.11|
|COME [105]|arXiv 25|Diffusion|C|-|26.56|21.73|18.49|22.26|-|48.08|43.84|40.28|44.07|
|SparseWorld-TC [20]|arXiv 25|VGGT [116]|C|-|32.76|29.62|27.28|29.89|-|55.28|53.56|51.71|53.52|
|OccTENS–F [54]|arXiv 25|Auto. Tran.|C|-|17.17|10.38|7.82|11.79|-|27.60|25.14|20.33|24.35|
|SparseWorld [14]|AAAI 26|Transformer|C|-|14.93|13.15|11.51|13.20|-|22.96|22.10|21.05|22.03|
|UniScene [59]|CVPR 25|Diffusion|Layout|92.10|35.37|29.59|25.08|31.76|87.00|38.34|32.70|29.09|34.84|


ulate the distribution of real-world point clouds. Tab. 5 presents a performance comparison of representative methods on the nuScenes [7] validation set. It shows the Chamfer Distance values at three future time steps, where Avg. corresponds to the arithmetic mean of these three values. 

The prediction performance of point-cloud-targeted DWMs depends heavily on specific experimental settings. For instance, frameworks that leverage point cloud inputs, such as Copilot4D [158] and LaGen [171], demonstrate superior performance compared to vision-only counterparts like ViDAR [149] and DriveX [104]. Nevertheless, visiononly approaches [104, 149, 171, 173] are showing a steady increase in their prediction ability. 

### **5.3. Occupancy Prediction** 

Occupancy forecasting requires modeling precise spatial structures and capturing complex spatiotemporal dynamics. Tab. 6 summarizes the performance of existing methods on the Occ3D-nuScenes [111] validation set. Within this table, Recon. evaluates the occupancy reconstruction fidelity at the current timestamp, and Avg. represents the mean predictive performance across the three future time steps. 

As shown in Tab. 6, the evolution of occupancy-targeted DWM from early frameworks [119, 127, 167] to recent architectures [14, 20, 77] reveals significant improvement in predictive performance. Early methodologies, exemplified 

by DOME [32] and OccLLaMA [127], exhibit a substantial performance gap where reconstruction IoU often exceeds prediction IoU by more than twofold. Furthermore, these methods suffer from a pronounced temporal decay as the prediction horizon extends from one to three seconds. In contrast, recent advancements [20, 77] not only bolster both reconstruction and prediction benchmarks but also narrow the discrepancy between them. This trend underscores a pivotal breakthrough in capturing complex spatiotemporal dynamics. 

Notably, for the majority of the presented frameworks, the IoU score in predictive tasks typically surpasses the mIoU score, despite the fact that mIoU is often higher in reconstruction tasks. This discrepancy suggests that these models exhibit a lower proficiency in capturing the dynamics of small-scale objects compared to large-scale entities and background. In contrast, Occ-LLM [138] allocates the preponderance of its modeling capacity toward dynamic object prediction and achieves an mIoU that exceeds the corresponding IoU. Finally, the performance of vision-tooccupancy prediction remains lower than results with occupancy or layout input, highlighting the formidable challenge of constructing 4D spatial cognition from visual inputs. 

14 

Table 7. Open-loop driving performance on the nuScenes [7] validation set. Core Arc. denotes the core architecture of the DWM. Auto. Tran. is Autoregressive Transfomer. Pred. Mod. means the modality of predicted scenes. Avg. corresponds to the mean of the scores at 1s, 2s, and 3s. O, C, and D separately denote Occupancy, Camera, and Depth. 

|Method|Reference|Core Arc.|Pred. Mod.||L2 (|_m_)_↓_|||Col.|(%)_↓_||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|UniAD [46]|CVPR 23|Transformer|Not DWM|0.48|0.96|1.65|1.03|0.05|0.17|0.71|0.31|
|VAD [51]|ICCV 23|Transformer|Not DWM|0.54|1.15|1.98|1.22|0.10|0.24|0.96|0.43|
|Drive-WM [125]|CVPR 24|Diffusion|C|0.43|0.77|1.20|0.80|0.10|0.21|0.48|0.26|
|DriveDreamer [122]|ECCV 24|Diffusion|C|-|-|-|0.29|-|-|-|0.15|
|Doe-1 [168]|arXiv 24|LLM|C|0.50|1.18|2.11|1.26|0.04|0.37|1.19|0.53|
|Epona [157]|ICCV25|Diffusion|C|0.61|1.17|1.98|1.25|0.01|0.22|0.85|0.36|
|<br>PWM [165]|NeurIPS 25|LLM|C|0.41|0.75|1.17|0.78|0.01|0.01|0.18|0.07|
|FSDrive [152]|NeurIPS 25|LLM|C|0.18|0.39|0.77|0.45|0.00|0.06|0.42|0.16|
|Occ-World-O [167]|ECCV 24|Auto. Tran.|O|0.43|1.08|1.99|1.17|0.07|0.38|1.35|0.60|
|Occ-LLaMA-O [127]|arXiv 24|LLM|O|0.37|1.02|2.03|1.14|0.04|0.24|1.20|0.49|
|DFIT-OccWorld-O [155]|arXiv 24|Auto. Tran.|O|0.38|0.96|1.73|1.02|0.07|0.39|0.90|0.45|
|Drive-OccWorld [148]|AAAI 25|Transformer|O|0.25|0.44|0.72|0.47|0.03|0.08|0.22|0.11|
|PreWorld [66]|ICLR 25|Transformer|O|0.22|0.30|0.40|0.31|0.21|0.66|0.71|0.53|
|RenderWorld [141]|ICRA 25|Auto. Tran.|O|0.35|0.91|1.84|1.03|0.05|0.40|1.39|0.61|
|Occ-LLM [138]|ICRA 25|LLM|O|0.12|0.24|0.49|0.28|-|-|-|-|
|IR-WM [85]|arXiv 25|Transformer|O|0.23|0.51|0.85|0.53|0.14|0.20|0.16|0.17|
|DTT [137]|arXiv 25|Transformer|O|0.32|0.91|1.76|1.00|0.08|0.32|0.51|0.30|
|OccTENS-O [54]|arXiv 25|Auto. Tran.|O|0.39|1.02|1.96|1.12|0.08|0.25|1.12|0.48|
|SparseWorld [14]|AAAI 26|Transformer|O|0.19|0.25|0.36|0.27|0.11|0.29|0.46|0.29|
|NeMo [47]|ECCV 24|Transformer|O & C|0.35|0.94|1.77|1.02|0.11|0.30|1.37|0.59|
|DiST-4D [36]|ICCV 25|Diffusion|D & C|0.56|1.11|1.91|1.19|-|-|-|-|
|LAW [68]|ICLR 24|Transformer|-|0.24|0.46|0.76|0.49|0.08|0.10|0.39|0.19|
|World4Drive [170]|ICCV 25|Transformer|-|0.23|0.47|0.81|0.50|0.02|0.12|0.33|0.16|


Table 8. Closed-loop evaluation on CARLA [19]. Core Arc. denotes the core architecture of the DWM. Pred. Mod. means the modality of predicted scenes. Effi. is the Efficiency score, while Comf. is the Comfortness score. O, C, and B separately denote Occupancy, Camera, and BEV Map. 

|Method|Reference|RL|Core Arc.|Pred. Mod.|IS_↑_|RC (%)_↑_|DS_↑_|SR (%)_↑_|Effi. _↑_|Comf. _↑_|Benchmark|
|---|---|---|---|---|---|---|---|---|---|---|---|
|VAD-Base [51]|ICCV 23|✗|Transformer|Not DWM|0.74|87.26|64.29|-|-|-|Town05 Short|
|Nemo [47]|ECCV 24|✗|Transformer|C & O|-|90.12|75.87|-|-|-|Town05 Short|
|VAD-Base [51]|ICCV 23|✗|Transformer|Not DWM|0.40|75.20|30.31|-|-|-|Town05 Long|
|MILE [6]|NeurIPS 22|✗|RNN|C & B|0.63|97.40|61.10|-|-|-|Town05 Long|
|Nemo [47]|ECCV 24|✗|Transformer|C & O|-|80.98|42.57|-|-|-|Town05 Long|
|Popov. et. al. [96]|ArXiv 24|✓|GRU|-|0.80|100.00|70.00|-|-|-|Town05 Long|
|LAW [68]|ICLR 25|✗|Transformer|-|0.72|97.80|70.10|-|-|-|Town05 Long|
|Think2Drive [63]|ECCV 24|✓|RSSM|-|0.73|78.20|43.80|-|-|-|Town13|
|Raw2Drive [151]|NeurIPS 25|✓|RSSM|-|0.43|9.32|4.12|-|-|-|Town13|
|ORION [22]|ICCV 25|✗|LLM|Not DWM|-|-|77.74|54.62|151.48|17.38|Bench2Drive [50]|
|Think2Drive [63]|ECCV 24|✓|RSSM|-|-|-|91.85|85.41|269.14|25.97|Bench2Drive [50]|
|WoTE [69]|ICCV 25|✗|Transformer|B|-|-|61.71|31.36|-|-|Bench2Drive [50]|
|Raw2Drive [151]|NeurIPS 25|✓|RSSM|-|-|-|71.36|50.24|214.17|22.42|Bench2Drive [50]|
|SeerDrive [154]|NeurIPS 25|✗|Transformer|B|-|-|58.32|30.17|-|-|Bench2Drive [50]|


### **5.4. Planning** 

Planning tasks are primarily categorized into open-loop and closed-loop paradigms. In open-loop evaluations, the model plans future behaviors over a short horizon based on recorded observations. In contrast, closed-loop evaluations involve a dynamic process where the simulation environment provides real-time feedback, requiring the agent to engage in continuous interaction to complete the entire driving mission. While open-loop protocols leverage real-world datasets to provide photorealistic observations, closed-loop settings align more closely with the real-world driving pro- 

cess, thereby offering a more rigorous assessment of the agent’s comprehensive driving capability. 

**Open-Loop Planning.** Tab. 7 presents the open-loop planning performance of DWMs on the nuScenes validation set. In the table, Core Arc. denotes the core architecture of the DWM framework, while Pred. Mod. indicates the target prediction modality. The results cover a future 3-second planning horizon, with Avg. representing the average performance across the three evaluated time steps. 

Open-loop planning is influenced by various factors, including input resolution and foundation models. How- 

15 

ever, from a comprehensive viewpoint, DWMs have generally surpassed traditional mainstream end-to-end frameworks [46, 51], demonstrating the significant benefits of these models for AD research. It is noteworthy that OccLLM [138] and SparseWorld [14] improve trajectory reasonableness by focusing on moving objects through decoupling methods. Meanwhile, PWM [165] and DriveOccWorld [148] utilize DWMs to enhance the foresight of planners regarding hazards, effectively reducing collision rates and demonstrating safer driving. 

**Closed-Loop Planning.** As shown in Tab. 8, DWMs outperform traditional end-to-end methods in closed-loop planning within the widely used Town05 and Town13 benchmarks in CARLA [19]. Furthermore, Tab. 8 also presents the performance on Bench2Drive [50], which evaluates closed-loop performance across diverse driving environments. Think2Drive [63] achieves the best results by using privileged information from the simulator, but other DWMs still show a gap compared to mainstream methods [22]. This suggests that there is still considerable room for improvement in closed-loop driving for DWMs. Notably, although Raw2Drive [151] achieves lower scores in DS score and SR score, its higher scores in Efficiency and Comfortness suggest that it has a more substantial capacity for smooth driving. 

## **6. Limitation and Future Direction** 

While research on DWMs has made significant progress, several limitations remain that may limit their full potential. Additionally, adjusting DWMs for various AD tasks is a continuous challenge. In this section, we provide a detailed discussion of current limitations and describe possible directions for future research and development. 

**Data Scarcity.** The acquisition of AD data involves prohibitive costs, particularly for long-tail and safety-critical cases. This results in the limited scale and uneven distribution of existing datasets. Although recent works [124, 143] have established large-scale and diverse driving video datasets, reliably acquiring synchronized multi-modal data remains a significant challenge. 

While research on DWM-based data synthesis [89, 150] has made substantial progress and demonstrated effectiveness in various downstream tasks, the quality of such synthesized data is not guaranteed. We argue that future efforts should not only focus on enhancing the diversity and quality of data synthesis, but also on establishing a GT-free evaluation paradigm that encompasses driving behaviors, object distributions, and geometry-texture details. Leveraging powerful generative models and robust evaluation suites, a full-stack automated synthesis, filtering, and refining pipeline can be constructed to facilitate the creation of high-quality, large-scale multimodal driving datasets. 

**Reliable Simulation.** Although DWMs have been 

demonstrated to apply to closed-loop simulation [147], their reliability remains a major concern. A key problem is to ensure that DWM performance would not drop significantly when confronted with complex simulation scenarios, such as long-horizon rollouts and drastic viewpoint shifts, as well as variable driving conditions, including diverse traffic flows and varying weather conditions. This presents significant challenges to the robustness and generalization of DWMs. On the other hand, generative models suffer from intrinsic flaws that are prone to hallucinations and physically inconsistent outputs (e.g., sudden vehicle appearances, speed estimation errors). Even under nominal conditions, these issues can lead to hazardous decision outcomes. Finally, evaluations of DWM’s predictive capabilities are predominantly based on offline datasets, which fail to reflect the dynamic interplay between the planner and the DWMbased simulator within more realistic closed-loop driving behaviors. Thus, investigating how to evaluate the capabilities for DWMs to serve as a simulator, as well as how to achieve reliable simulation, remains a valuable research direction. 

**Task Unification.** AD scene prediction is a multi-level modeling challenge encompassing environmental layout, motion dynamics, and driving intentions. However, current research faces a major division. DWMs that focus on detailed scene prediction often implicitly reflect behavioral intentions by predicting pixel variations, yet lack the explicit modeling of driving logic. Meanwhile, DWMs that focus on behavior simulation prioritize strategic planning but frequently overlook the fine-grained perception of complex, real-world visual environments. This disconnect hinders models from forming a unified cognition of driving scenes. Recently, the exploration of language capabilities has emerged as a key development trend in DWMs [127, 138, 168, 173], AD research [23, 91, 164], and even in the embodied intelligence domain [64, 74, 156]. Looking ahead, building an integrated end-to-end framework that unifies prediction, planning, and understanding will be pivotal to unlocking the full potential of DWMs. 

**Multi-Sensor Modeling.** AD systems universally rely on multi-sensor fusion schemes. Data from different modalities exhibits inherent modality-specific biases while simultaneously corresponding to the same physical world. Despite significant progress in unified multimodal representation [104, 160], the alignment of different modalities has received little attention. For instance, most multi-modal generation approaches lack interaction between the generated outputs. Aligning these results could not only facilitate mutual error correction but also foster the learning of modality-agnostic world knowledge. Furthermore, acquiring matched multi-sensor data is considerably expensive. Leveraging easily accessible unaligned data (i.e., multimodal data not corresponding to the same scene) for train- 

16 

ing could effectively expand the scale of available data. 

**Efficiency.** Generative tasks pose significant challenges to the deployment efficiency of DWMs. The inherent complexity of 4D data leads to substantial computational overhead. Moreover, model scaling and the integration of technologies like LLMs and Chain-of-Thought exacerbate computational burdens and inference latency. While DWMs have achieved notable progress in predicting and planning tasks, balancing performance with efficiency remains a core obstacle to their real-world deployment. To address this, the latent DWM paradigm [29, 63] circumvents efficiency bottlenecks by omitting scene decoding, while recent studies effectively enhance generation efficiency through scene decoupling [85, 137, 155, 177] or sparse representation [14, 16, 20]. Beyond model and representation lightweighting, reducing scene decoding frequency and implementing multi-task parallelism are also promising solutions. Such efficiency-centric innovations will continue to be a pivotal focus in future research. 

**Attack and Defense.** Adversarial attacks [120] pose a severe threat to AD safety, as they can easily trigger catastrophic traffic accidents. These attacks are typically implemented via carefully crafted, human-imperceptible adversarial perturbation patches. Since such samples are virtually non-existent in training data, detection and defense become incredibly challenging. Despite the importance of this issue, dedicated research on adversarial attacks against DWMs remains scarce. Therefore, investigating such attacks and developing effective defense strategies is of vital practical significance. Meanwhile, leveraging the predictive capability and generalization of DWMs to locate and mitigate the impact of adversarial patches represents a highly valuable research direction. Collectively, these efforts play a crucial role in ensuring the safe and reliable deployment of DWMs in the real world. 

## **7. Conclusion** 

DWMs have been widely recognized as fundamental components in the architecture of AD systems. Their primary goal is to enhance a comprehensive understanding of dynamic environments by predicting the evolution of future scenes. This paper first introduces the datasets and evaluation metrics commonly used in DWM research. We then provide a systematic survey of DWMs according to their prediction modalities, summarizing the unique challenges and development paths for each modality. We also summarize the applications of DWMs and their comprehensive impact on AD research. Next, this paper compares the performance of representative works in major prediction and planning tasks. Finally, we discuss the limitations of current DWMs and identify promising research directions to overcome existing difficulties and promote continuous progress in this field. We believe that this survey will help new researchers to under- 

stand the key technical developments in this area quickly. 

## **References** 

- [1] Ben Agro, Quinlan Sykora, Sergio Casas, Thomas Gilles, and Raquel Urtasun. Uno: Unsupervised occupancy fields for perception and forecasting. In _CVPR_ , pages 14487– 14496, 2024. 1, 7, 13 

- [2] Hassan Abu Alhaija, Jose Alvarez, Maciej Bala, Tiffany Cai, Tianshi Cao, Liz Cha, Joshua Chen, Mike Chen, Francesco Ferroni, Sanja Fidler, et al. Cosmos-transfer1: Conditional world generation with adaptive multimodal control. _arXiv preprint arXiv:2503.14492_ , 2025. 11 

- [3] Hidehisa Arai, Keishi Ishihara, Tsubasa Takahashi, and Yu Yamaguchi. Act-bench: Towards action controllable world models for autonomous driving. _arXiv preprint arXiv:2412.05337_ , 2024. 2, 4 

- [4] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. Dynamiccity: Large-scale 4d occupancy generation from dynamic scenes. In _ICLR_ , 2025. 4, 6, 7, 11, 14 

- [5] Daniel Bogdoll, Yitian Yang, Tim Joseph, Melih Yazgan, and J Marius Zollner. Muvo: A multimodal generative world model for autonomous driving with geometric representations. In _2025 IEEE Intelligent Vehicles Symposium (IV)_ , pages 2243–2250. IEEE, 2025. 7 

- [6] Eli Bronstein, Mark Palatucci, Dominik Notz, Brandyn White, Alex Kuefler, Yiren Lu, Supratik Paul, Payam Nikdel, Paul Mougin, Hongge Chen, et al. Hierarchical model-based imitation learning for planning in autonomous driving. In _Proc. IEEE Int. Conf. Intell. Robots Syst._ , pages 8652–8659. IEEE, 2022. 15 

- [7] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _CVPR_ , pages 11621–11631, 2020. 2, 4, 10, 13, 14, 15 

- [8] Anthony Chen, Wenzhao Zheng, Yida Wang, Xueyang Zhang, Kun Zhan, Peng Jia, Kurt Keutzer, and Shanghang Zhang. Geodrive: 3d geometry-informed driving world model with precise action control. _arXiv preprint arXiv:2505.22421_ , 2025. 4, 13 

- [9] Junliang Chen, Huaiyuan Xu, Yi Wang, and Lap-Pui Chau. Occprophet: Pushing the efficiency frontier of cameraonly 4d occupancy forecasting with an observer-forecasterrefiner framework. In _ICLR_ , 2025. 4, 7 

- [10] Rui Chen, Zehuan Wu, Yichen Liu, Yuxin Guo, Jingcheng Ni, Haifeng Xia, and Siyu Xia. Unimlvg: Unified framework for multi-view long video generation with comprehensive control capabilities for autonomous driving. _arXiv preprint arXiv:2412.04842_ , 2024. 1, 4, 13 

- [11] Yuntao Chen, Yuqi Wang, and Zhaoxiang Zhang. Drivinggpt: Unifying driving world modeling and planning with multi-modal autoregressive transformers. In _ICCV_ , 2025. 4, 5, 12 

- [12] OpenScene Contributors. Openscene: The largest up-todate 3d occupancy prediction benchmark in autonomous 

17 

driving. https://github.com/OpenDriveLab/ OpenScene, 2023. 4 

- [13] Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele. The cityscapes dataset for semantic urban scene understanding. In _CVPR_ , pages 3213–3223, 2016. 4 

- [14] Chenxu Dang, Haiyan Liu, Jason Bao, Pei An, Xinyue Tang, Jie Ma, Bingchuan Sun, Yan Wang, et al. Sparseworld: A flexible, adaptive, and efficient 4d occupancy world model powered by sparse and dynamic queries. In _AAAI_ , 2026. 7, 14, 15, 16, 17 

- [15] Daniel Dauner, Marcel Hallgarten, Tianyu Li, Xinshuo Weng, Zhiyu Huang, Zetong Yang, Hongyang Li, Igor Gilitschenski, Boris Ivanovic, Marco Pavone, et al. Navsim: Data-driven non-reactive autonomous vehicle simulation and benchmarking. _NeurIPS_ , 37:28706–28719, 2024. 4, 9 

- [16] Tianchen Deng, Xuefeng Chen, Yi Chen, Qu Chen, Yuyao Xu, Lijin Yang, Le Xu, Yu Zhang, Bo Zhang, Wuxiong Huang, et al. Gaussiandwm: 3d gaussian driving world model for unified scene understanding and multi-modal generation. _arXiv preprint arXiv:2512.23180_ , 2025. 8, 17 

- [17] Christopher Diehl, Quinlan Sykora, Ben Agro, Thomas Gilles, Sergio Casas, and Raquel Urtasun. Dio: Decomposable implicit 4d occupancy-flow world model. In _CVPR_ , pages 27456–27466, 2025. 7, 13 

- [18] Jingtao Ding, Yunke Zhang, Yu Shang, Yuheng Zhang, Zefang Zong, Jie Feng, Yuan Yuan, Hongyuan Su, Nian Li, Nicholas Sukiennik, et al. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 1 

- [19] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator. In _Conference on robot learning_ , pages 1–16. PMLR, 2017. 2, 3, 9, 15, 16 

- [20] Jiayuan Du, Yiming Zhao, Zhenglong Guo, Yong Pan, Wenbo Hou, Zhihui Hao, Kun Zhan, and Qijun Chen. Sparseworld-tc: Trajectory-conditioned sparse occupancy world model. _arXiv preprint arXiv:2511.22039_ , 2025. 4, 7, 14, 17 

- [21] Ao Fu, Yi Zhou, Tao Zhou, Yi Yang, Bojun Gao, Qun Li, Guobin Wu, and Ling Shao. Exploring the interplay between video generation and world models in autonomous driving: A survey. _arXiv preprint arXiv:2411.02914_ , 2024. 1 

- [22] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Dingkang Liang, Chong Zhang, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Orion: A holistic end-to-end autonomous driving framework by visionlanguage instructed action generation. In _ICCV_ , 2025. 15, 16 

- [23] Haoyu Fu, Diankun Zhang, Zongchuang Zhao, Jianfeng Cui, Hongwei Xie, Bing Wang, Guang Chen, Dingkang Liang, and Xiang Bai. Minddrive: A vision-languageaction model for autonomous driving via online reinforcement learning. _arXiv preprint arXiv:2512.13636_ , 2025. 16 

- [24] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. In _ICLR_ , 2024. 1, 4, 9, 13 

- [25] Ruiyuan Gao, Kai Chen, Bo Xiao, Lanqing Hong, Zhenguo Li, and Qiang Xu. Magicdrive-v2: High-resolution long video generation for autonomous driving with adaptive control. In _ICCV_ , pages 28135–28144, 2025. 4, 9, 13 

- [26] Ruiyuan Gao, Kai Chen, Zhihao Li, Lanqing Hong, Zhenguo Li, and Qiang Xu. MagicDrive3D: Controllable 3d generation for any-view rendering in street scenes. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , 2026. 11 

- [27] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In _NeurIPS_ , 2024. 1, 4, 9, 10, 13 

- [28] Yinfeng Gao, Qichao Zhang, Da-Wei Ding, and Dongbin Zhao. Dream to drive with predictive individual world model. _IEEE Trans. Intell. Vehicles_ , 2024. 9 

- [29] Zeyu Gao, Yao Mu, Chen Chen, Jingliang Duan, Ping Luo, Yanfeng Lu, and Shengbo Eben Li. Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model. _IEEE Trans. Intell. Transportation Syst._ , 2024. 4, 17 

- [30] Anant Garg and K Madhava Krishna. Imagine-2-drive: High-fidelity world modeling in carla for autonomous vehicles. _arXiv preprint arXiv:2411.10171_ , 2024. 10 

- [31] Andreas Geiger, Philip Lenz, Christoph Stiller, and Raquel Urtasun. Vision meets robotics: The kitti dataset. _Intl. Journal of Robotics Research_ , 2013. 2, 4, 10 

- [32] Songen Gu, Wei Yin, Bu Jin, Xiaoyang Guo, Junming Wang, Haodong Li, Qian Zhang, and Xiaoxiao Long. Dome: Taming diffusion model into high-fidelity controllable occupancy world model. _arXiv preprint arXiv:2410.10429_ , 2024. 1, 4, 6, 7, 9, 14 

- [33] Yanchen Guan, Haicheng Liao, Zhenning Li, Jia Hu, Runze Yuan, Yunjian Li, Guohui Zhang, and Chengzhong Xu. World models for autonomous driving: An initial survey. _IEEE Trans. Intell. Vehicles_ , 2024. 1 

- [34] Cole Gulino, Justin Fu, Wenjie Luo, George Tucker, Eli Bronstein, Yiren Lu, Jean Harb, Xinlei Pan, Yan Wang, Xiangyu Chen, et al. Waymax: An accelerated, datadriven simulator for large-scale autonomous driving research. _NeurIPS_ , 36:7730–7742, 2023. 2, 3 

- [35] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Peiyi Wang, Qihao Zhu, Runxin Xu, Ruoyu Zhang, Shirong Ma, Xiao Bi, et al. Deepseek-r1 incentivizes reasoning in llms through reinforcement learning. _Nature_ , 645(8081): 633–638, 2025. 8 

- [36] Jiazhe Guo, Yikang Ding, Xiwu Chen, Shuo Chen, Bohan Li, Yingshuang Zou, Xiaoyang Lyu, Feiyang Tan, Xiaojuan Qi, Zhiheng Li, et al. Dist-4d: Disentangled spatiotemporal diffusion with metric depth for 4d driving scene generation. In _ICCV_ , 2025. 4, 11, 13, 15 

- [37] Xi Guo, Chenjing Ding, Haoxuan Dou, Xin Zhang, Weixuan Tang, and Wei Wu. Infinitydrive: Breaking time limits 

18 

in driving world models. _arXiv preprint arXiv:2412.01522_ , 2024. 4, 13 

- [38] K. Tan et al. H. Caesar, J. Kabzan. Nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. In _CVPRW_ , 2021. 2, 3, 4 

- [39] David Ha and J¨urgen Schmidhuber. World models. In _NeurIPS_ , 2018. 1 

- [40] Shadi Hamdan and Fatma G¨uney. Carformer: Self-driving with learned object-centric representations. In _ECCV_ , pages 177–193. Springer, 2024. 9 

- [41] Mariam Hassan, Sebastian Stapf, Ahmad Rahimi, Pedro Rezende, Yasaman Haghighi, David Br¨uggemann, Isinsu Katircioglu, Lin Zhang, Xiaoran Chen, Suman Saha, et al. Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In _CVPR_ , 2025. 4, 7, 10, 13 

- [42] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zachary Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. In _NeurIPS_ , pages 20703–20716, 2022. 4 

- [43] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 1, 5, 9, 12 

- [44] Qianjiang Hu, Zhimin Zhang, and Wei Hu. Rangeldm: Fast realistic lidar point cloud generation. In _ECCV_ , pages 115– 135. Springer, 2024. 11 

- [45] Xiaotao Hu, Wei Yin, Mingkai Jia, Junyuan Deng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Ping Tan. Drivingworld: Constructingworld model for autonomous driving via video gpt. _arXiv preprint arXiv:2412.19505_ , 2024. 4, 5, 12, 13 

- [46] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, et al. Planning-oriented autonomous driving. In _CVPR_ , pages 17853–17862, 2023. 1, 12, 15, 16 

- [47] Zanming Huang, Jimuyang Zhang, and Eshed Ohn-Bar. Neural volumetric world models for autonomous driving. In _ECCV_ , pages 195–213. Springer, 2024. 1, 7, 13, 15 

- [48] Yishen Ji, Ziyue Zhu, Zhenxin Zhu, Kaixin Xiong, Ming Lu, Zhiqi Li, Lijun Zhou, Haiyang Sun, Bing Wang, and Tong Lu. Cogen: 3d consistent video generation via adaptive conditioning for autonomous driving. _arXiv preprint arXiv:2503.22231_ , 2025. 4, 7, 13 

- [49] Feiyang Jia, Caiyan Jia, Ziying Song, Zhicheng Bao, Lin Liu, Shaoqing Xu, Yan Gong, Lei Yang, Xinyu Zhang, Bin Sun, et al. Progressive robustness-aware world models in autonomous driving: A review and outlook. _Authorea Preprints_ , 2025. 1 

- [50] Xiaosong Jia, Zhenjie Yang, Qifeng Li, Zhiyuan Zhang, and Junchi Yan. Bench2drive: Towards multi-ability benchmarking of closed-loop end-to-end autonomous driving. In _NeurIPS 2024 Datasets and Benchmarks Track_ , 2024. 4, 15, 16 

- [51] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang 

Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. In _ICCV_ , pages 8340–8350, 2023. 12, 15, 16 

- [52] Junpeng Jiang, Gangyi Hong, Miao Zhang, Hengtong Hu, Kun Zhan, Rui Shao, and Liqiang Nie. Dive: Efficient multi-view driving scenes generation based on video diffusion transformer. _arXiv preprint arXiv:2504.19614_ , 2025. 4 

- [53] Max Jiang, Yijing Bai, Andre Cornman, Christopher Davis, Xiukun Huang, Hong Jeon, Sakshum Kulshrestha, John Lambert, Shuangyu Li, Xuanyu Zhou, et al. Scenediffuser: Efficient and controllable driving simulation initialization and rollout. _NeurIPS_ , 37:55729–55760, 2024. 1, 9, 10 

- [54] Bu Jin, Songen Gu, Xiaotao Hu, Yupeng Zheng, Xiaoyang Guo, Qian Zhang, Xiaoxiao Long, and Wei Yin. Occtens: 3d occupancy world model via temporal next-scale prediction. _arXiv preprint arXiv:2509.03887_ , 2025. 6, 7, 14, 15 

- [55] Efstathios Karypidis, Ioannis Kakogeorgiou, Spyros Gidaris, and Nikos Komodakis. Dino-foresight: Looking into the future with dino. In _NeurIPS_ , 2025. 1, 8 

- [56] Efstathios Karypidis, Ioannis Kakogeorgiou, Spyros Gidaris, and Nikos Komodakis. Advancing semantic future prediction through multimodal visual sequence transformers. In _CVPR_ , pages 3793–3803, 2025. 4, 7 

- [57] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM TOG_ , 42(4):1–14, 2023. 11 

- [58] Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. _Open Review_ , 62(1): 1–62, 2022. 1 

- [59] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, et al. Uniscene: Unified occupancycentric driving scene generation. In _CVPR_ , pages 11971– 11981, 2025. 4, 8, 11, 13, 14 

- [60] Bohan Li, Xin Jin, Hu Zhu, Hongsi Liu, Ruikai Li, Jiazhe Guo, Kaiwen Cai, Chao Ma, Yueming Jin, Hao Zhao, et al. Scaling up occupancy-centric driving scene generation: Dataset and method. _arXiv preprint arXiv:2510.22973_ , 2025. 8, 13 

- [61] Jingyu Li, Bozhou Zhang, Xin Jin, Jiankang Deng, Xiatian Zhu, and Li Zhang. Imagidrive: A unified imaginationand-planning framework for autonomous driving. _arXiv preprint arXiv:2508.11428_ , 2025. 12 

- [62] Quanyi Li, Zhenghao Peng, Lan Feng, Qihang Zhang, Zhenghai Xue, and Bolei Zhou. Metadrive: Composing diverse driving scenarios for generalizable reinforcement learning. _IEEE TPAMI_ , 45(3):3461–3475, 2022. 2, 3 

- [63] Qifeng Li, Xiaosong Jia, Shaobo Wang, and Junchi Yan. Think2drive: Efficient reinforcement learning by thinking in latent world model for quasi-realistic autonomous driving (in carla-v2). In _ECCV_ , 2024. 1, 4, 8, 10, 15, 16, 17 

- [64] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 16 

19 

- [65] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. Drivingdiffusion: layout-guided multi-view driving scenarios video generation with latent diffusion model. In _ECCV_ , pages 469–485. Springer, 2024. 2, 4, 9, 11, 13 

- [66] Xiang Li, Pengfei Li, Yupeng Zheng, Wei Sun, Yan Wang, and Yilun Chen. Semi-supervised vision-centric 3d occupancy world model for autonomous driving. In _ICLR_ , 2025. 2, 7, 13, 14, 15 

- [67] Xiaofan Li, Chenming Wu, Zhao Yang, Zhihao Xu, Yumeng Zhang, Dingkang Liang, Ji Wan, and Jun Wang. Driverse: Navigation world model for driving simulation via multimodal trajectory prompting and motion alignment. In _ACM MM_ , pages 9753–9762, 2025. 9, 13 

- [68] Yingyan Li, Lue Fan, Jiawei He, Yuqi Wang, Yuntao Chen, Zhaoxiang Zhang, and Tieniu Tan. Enhancing end-to-end autonomous driving with latent world model. In _ICLR_ , 2025. 1, 4, 8, 10, 12, 15 

- [69] Yingyan Li, Yuqi Wang, Yang Liu, Jiawei He, Lue Fan, and Zhaoxiang Zhang. End-to-end driving with online trajectory evaluation via bev world model. In _ICCV_ , 2025. 4, 12, 15 

- [70] Zhiqi Li, Wenhai Wang, Hongyang Li, Enze Xie, Chonghao Sima, Tong Lu, Qiao Yu, and Jifeng Dai. Bevformer: learning bird’s-eye-view representation from lidar-camera via spatiotemporal transformers. _IEEE TPAMI_ , 2024. 12 

- [71] Ao Liang, Youquan Liu, Yu Yang, Dongyue Lu, Linfeng Li, Lingdong Kong, Huaici Zhao, and Wei Tsang Ooi. Lidarcrafter: Dynamic 4d world modeling from lidar sequences. In _AAAI_ , 2026. 1, 6, 9, 11 

- [72] Dingkang Liang, Xin Zhou, Wei Xu, Xingkui Zhu, Zhikang Zou, Xiaoqing Ye, Xiao Tan, and Xiang Bai. Pointmamba: A simple state space model for point cloud analysis. In _NeurIPS_ , pages 32653–32677, 2024. 5 

- [73] Dingkang Liang, Tianrui Feng, Xin Zhou, Yumeng Zhang, Zhikang Zou, and Xiang Bai. Parameter-efficient finetuning in spectral domain for point cloud learning. _IEEE TPAMI_ , 2025. 6 

- [74] Dingkang Liang, Cheng Zhang, Xiaopeng Xu, Jianzhong Ju, Zhenbo Luo, and Xiang Bai. Cook and clean together: Teaching embodied agents for parallel task execution. In _AAAI_ , 2026. 16 

- [75] Dingkang Liang, Dingyuan Zhang, Xin Zhou, Sifan Tu, Tianrui Feng, Xiaofan Li, Yumeng Zhang, Mingyang Du, Xiao Tan, and Xiang Bai. Seeing the future, perceiving the future: A unified driving world model for future generation and perception. In _Proc. IEEE Int. Conf. Robotics Automation_ , 2026. 8, 11, 13 

- [76] Haicheng Liao, Huanming Shen, Bonan Wang, Yongkang Li, Yihong Tang, Chengyue Wang, Dingyi Zhuang, Kehua Chen, Hai Yang, Chengzhong Xu, et al. Think before you drive: World model-inspired multimodal grounding for autonomous vehicles. _arXiv preprint arXiv:2512.03454_ , 2025. 8 

- [77] Zhimin Liao, Ping Wei, Ruijie Zhang, Shuaijia Chen, Haoxuan Wang, and Ziyang Ren. I2-world: Intra-inter tokenization for efficient dynamic 4d scene forecasting. In _ICCV_ , pages 25810–25819, 2025. 7, 14 

- [78] Haohong Lin, Xin Huang, Tung Phan, David Hayden, Huan Zhang, Ding Zhao, Siddhartha Srinivasa, Eric Wolff, and Hongge Chen. Causal composition diffusion model for closed-loop traffic generation. In _CVPR_ , pages 27542– 27552, 2025. 9, 10 

- [79] Pei Liu, Songtao Wang, Lang Zhang, Xingyue Peng, Yuandong Lyu, Jiaxin Deng, Songxin Lu, Weiliang Ma, Xueyang Zhang, Yifei Zhan, et al. Listar: Ray-centric world models for 4d lidar sequences in autonomous driving. _arXiv preprint arXiv:2511.16049_ , 2025. 6, 13 

- [80] Tianran Liu, Shengwen Zhao, and Nicholas Rhinehart. Towards foundational lidar world models with efficient latent flow matching. In _NeurIPS_ , 2025. 14 

- [81] Hao Lu, Zhuang Ma, Guangfeng Jiang, Wenhang Ge, Bohan Li, Yuzhan Cai, Wenzhao Zheng, Yunpeng Zhang, and Yingcong Chen. 4d driving scene generation with stereo forcing. _arXiv preprint arXiv:2509.20251_ , 2025. 11 

- [82] Jiachen Lu, Ze Huang, Zeyu Yang, Jiahui Zhang, and Li Zhang. Wovogen: World volume-aware diffusion for controllable multi-camera driving scene generation. In _ECCV_ , pages 329–345. Springer, 2024. 4, 7, 13 

- [83] Yifan Lu, Xuanchi Ren, Jiawei Yang, Tianchang Shen, Zhangjie Wu, Jun Gao, Yue Wang, Siheng Chen, Mike Chen, Sanja Fidler, et al. Infinicube: Unbounded and controllable dynamic 3d driving scene generation with worldguided video models. In _ICCV_ , pages 27272–27283, 2025. 8 

- [84] Junyi Ma, Xieyuanli Chen, Jiawei Huang, Jingyi Xu, Zhen Luo, Jintao Xu, Weihao Gu, Rui Ai, and Hesheng Wang. Cam4docc: Benchmark for camera-only 4d occupancy forecasting in autonomous driving applications. In _CVPR_ , pages 21486–21495, 2024. 2, 4, 6 

- [85] Jianbiao Mei, Yu Yang, Xuemeng Yang, Licheng Wen, Jiajun Lv, Botian Shi, and Yong Liu. Vision-centric 4d occupancy forecasting and planning via implicit residual world models. _arXiv preprint arXiv:2510.16729_ , 2025. 1, 7, 15, 17 

- [86] Chen Min, Dawei Zhao, Liang Xiao, Yiming Nie, and Bin Dai. Uniworld: Autonomous driving pre-training via world models. _arXiv preprint arXiv:2308.07234_ , 2023. 6, 7, 12 

- [87] Chen Min, Dawei Zhao, Liang Xiao, Jian Zhao, Xinli Xu, Zheng Zhu, Lei Jin, Jianshu Li, Yulan Guo, Junliang Xing, et al. Driveworld: 4d pre-trained scene understanding via world models for autonomous driving. In _CVPR_ , pages 15522–15533, 2024. 1, 2, 4, 6, 7 

- [88] Sicheng Mo, Ziyang Leng, Leon Liu, Weizhen Wang, Honglin He, and Bolei Zhou. Dreamland: Controllable world creation with simulator and generative models. _arXiv preprint arXiv:2506.08006_ , 2025. 4, 10 

- [89] Chaojun Ni, Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Wenkang Qin, Guan Huang, Chen Liu, Yuyin Chen, Yida Wang, Xueyang Zhang, et al. Recondreamer: Crafting world models for driving scene reconstruction via online restoration. In _CVPR_ , 2025. 11, 16 

- [90] Jingcheng Ni, Yuxin Guo, Yichen Liu, Rui Chen, Lewei Lu, and Zehuan Wu. Maskgwm: A generalizable driving world model with video mask reconstruction. In _CVPR_ , pages 22381–22391, 2025. 1, 4, 13 

20 

- [91] Ming Nie, Renyuan Peng, Chunwei Wang, Xinyue Cai, Jianhua Han, Hang Xu, and Li Zhang. Reason2drive: Towards interpretable and chain-based reasoning for autonomous driving. In _ECCV_ , pages 292–308. Springer, 2024. 16 

- [92] Nvidia. Accelerating the future of autonomous vehicles. https://www.nvidia.com/en-us/solutions/ autonomous-vehicles/, 2024. 2, 3 

- [93] Julian Ost, Andrea Ramazzina, Amogh Joshi, Maximilian B¨omer, Mario Bijelic, and Felix Heide. Lsd-3d: Largescale 3d driving scene generation with geometry grounding. In _ICCV_ , 2026. 7, 11 

- [94] Minting Pan, Xiangming Zhu, Yunbo Wang, and Xiaokang Yang. Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. In _NeurIPS_ , pages 23178–23191, 2022. 2, 4 

- [95] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _ICCV_ , pages 4195–4205, 2023. 3, 4, 6, 9 

- [96] Alexander Popov, Alperen Degirmenci, David Wehr, Shashank Hegde, Ryan Oldja, Alexey Kamenev, Bertrand Douillard, David Nist´er, Urs Muller, Ruchi Bhargava, et al. Mitigating covariate shift in imitation learning for autonomous vehicles using latent space generative world models. _arXiv preprint arXiv:2409.16663_ , 2024. 1, 8, 10, 12, 15 

- [97] Guanren Qiao, Guorui Quan, Rongxiao Qu, and Guiliang Liu. Modelling competitive behaviors in autonomous driving under generative world model. In _ECCV_ , pages 19–36. Springer, 2024. 10 

- [98] Yiran Qin, Zhelun Shi, Jiwen Yu, Xijun Wang, Enshen Zhou, Lijun Li, Zhenfei Yin, Xihui Liu, Lu Sheng, Jing Shao, et al. Worldsimbench: Towards video generation models as world simulators. In _Proc. Int. Conf. Mach. Learn._ , 2025. 2, 4 

- [99] Xuanchi Ren, Yifan Lu, Tianshi Cao, Ruiyuan Gao, Shengyu Huang, Amirmojtaba Sabour, Tianchang Shen, Tobias Pfaff, Jay Zhangjie Wu, Runjian Chen, Seung Wook Kim, Jun Gao, Laura Leal-Taixe, Mike Chen, Sanja Fidler, and Huan Ling. Cosmos-drive-dreams: Scalable synthetic driving data generation with world foundation models, 2025. 13 

- [100] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _CVPR_ , pages 10684–10695, 2022. 4, 9 

- [101] Luke Rowe, Roger Girgis, Anthony Gosselin, Liam Paull, Christopher Pal, and Felix Heide. Scenario dreamer: Vectorized latent diffusion for generating driving simulation environments. In _CVPR_ , pages 17207–17218, 2025. 9, 10 

- [102] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving. _arXiv preprint arXiv:2503.20523_ , 2025. 1, 4, 12 

- [103] Zihao Sheng, Zilin Huang, Yansong Qu, Yue Leng, and Sikai Chen. Talk2traffic: Interactive and editable traffic scenario generation for autonomous driving with multimodal 

   - large language model. In _CVPR_ , pages 3788–3797, 2025. 1, 9, 10 

- [104] Chen Shi, Shaoshuai Shi, Kehua Sheng, Bo Zhang, and Li Jiang. Drivex: Omni scene modeling for learning generalizable world knowledge in autonomous driving. In _ICCV_ , 2025. 1, 4, 7, 13, 14, 16 

- [105] Yining Shi, Kun Jiang, Qiang Meng, Ke Wang, Jiabao Wang, Wenchao Sun, Tuopu Wen, Mengmeng Yang, and Diange Yang. Come: Adding scene-centric forecasting control to occupancy world model. _arXiv preprint arXiv:2506.13260_ , 2025. 4, 6, 7, 14 

- [106] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _CVPR_ , pages 2446–2454, 2020. 2, 4, 10 

- [107] Shuhan Tan, Kashyap Chitta, Yuxiao Chen, Ran Tian, Yurong You, Yan Wang, Wenjie Luo, Yulong Cao, Philipp Krahenbuhl, Marco Pavone, et al. Latent chain-of-thought world modeling for end-to-end driving. _arXiv preprint arXiv:2512.10226_ , 2025. 8, 12 

- [108] Shuhan Tan, John Lambert, Hong Jeon, Sakshum Kulshrestha, Yijing Bai, Jing Luo, Dragomir Anguelov, Mingxing Tan, and Chiyu Max Jiang. Scenediffuser++: City-scale traffic simulation via a generative world model. In _CVPR_ , pages 1570–1580, 2025. 1, 9, 10 

- [109] Tao Tang, Enhui Ma, Xia Zhou, Letian Wang, Tianyi Yan, Xueyang Zhang, Kun Zhan, Peng Jia, Xianpeng Lang, JiaWang Bian, et al. Omnigen: Unified multimodal sensor generation for autonomous driving. In _ACM MM_ , pages 9365–9374, 2025. 7, 13 

- [110] Keyu Tian, Yi Jiang, Zehuan Yuan, Bingyue Peng, and Liwei Wang. Visual autoregressive modeling: Scalable image generation via next-scale prediction. In _NeurIPS_ , pages 84839–84865, 2024. 6 

- [111] Xiaoyu Tian, Tao Jiang, Longfei Yun, Yucheng Mao, Huitong Yang, Yue Wang, Yilun Wang, and Hang Zhao. Occ3d: A large-scale 3d occupancy prediction benchmark for autonomous driving. In _NeurIPS_ , 2023. 4, 14 

- [112] Wenwen Tong, Chonghao Sima, Tai Wang, Li Chen, Silei Wu, Hanming Deng, Yi Gu, Lewei Lu, Ping Luo, Dahua Lin, et al. Scene as occupancy. In _ICCV_ , pages 8406–8415, 2023. 5, 12 

- [113] Arun Balajee Vasudevan, Neehar Peri, Jeff Schneider, and Deva Ramanan. Planning with adaptive world models for autonomous driving. In _Proc. IEEE Int. Conf. Robotics Automation_ , pages 14938–14945. IEEE, 2024. 9 

- [114] Haiguang Wang, Daqi Liu, Hongwei Xie, Haisong Liu, Enhui Ma, Kaicheng Yu, Limin Wang, and Bing Wang. Mila: Multi-view intensive-fidelity long-term video generation world model for autonomous driving. _arXiv preprint arXiv:2503.15875_ , 2025. 4, 13 

- [115] Hang Wang, Xin Ye, Feng Tao, Chenbin Pan, Abhirup Mallik, Burhaneddin Yaman, Liu Ren, and Junshan Zhang. Adawm: Adaptive world model based planning for autonomous driving. In _ICLR_ , 2025. 8, 10 

- [116] Jianyuan Wang, Minghao Chen, Nikita Karaev, Andrea Vedaldi, Christian Rupprecht, and David Novotny. Vggt: 

21 

Visual geometry grounded transformer. In _CVPR_ , pages 5294–5306, 2025. 14 

- [117] Jiawei Wang, Haowei Sun, Xintao Yan, Shuo Feng, Jun Gao, and Henry X Liu. Terasim-world: Worldwide safetycritical data synthesis for end-to-end autonomous driving. _arXiv preprint arXiv:2509.13164_ , 2025. 11 

- [118] Jiamin Wang, Yichen Yao, Xiang Feng, Hang Wu, Yaming Wang, Qingqiu Huang, Yuexin Ma, and Xinge Zhu. Stage: A stream-centric generative world model for long-horizon driving-scene simulation. In _Proc. IEEE Int. Conf. Intell. Robots Syst._ , 2025. 13 

- [119] Lening Wang, Wenzhao Zheng, Yilong Ren, Han Jiang, Zhiyong Cui, Haiyang Yu, and Jiwen Lu. Occsora: 4d occupancy generation models as world simulators for autonomous driving. _arXiv preprint arXiv:2405.20337_ , 2024. 1, 4, 6, 9, 11, 14 

- [120] Lu Wang, Tianyuan Zhang, Yang Qu, Siyuan Liang, Yuwei Chen, Aishan Liu, Xianglong Liu, and Dacheng Tao. Black-box adversarial attack on vision language models for autonomous driving. _arXiv preprint arXiv:2501.13563_ , 2025. 17 

- [121] Xiaofeng Wang, Zheng Zhu, Wenbo Xu, Yunpeng Zhang, Yi Wei, Xu Chi, Yun Ye, Dalong Du, Jiwen Lu, and Xingang Wang. Openoccupancy: A large scale benchmark for surrounding semantic occupancy perception. In _ICCV_ , pages 17850–17859, 2023. 4 

- [122] Xiaofeng Wang, Zheng Zhu, Guan Huang, Xinze Chen, Jiagang Zhu, and Jiwen Lu. Drivedreamer: Towards realworld-driven world models for autonomous driving. In _ECCV_ , 2024. 1, 2, 4, 9, 11, 13, 15 

- [123] Xiaodong Wang, Zhirong Wu, and Peixi Peng. Longdwm: Cross-granularity distillation for building a long-term driving world model. In _AAAI_ , 2026. 5, 13 

- [124] Yuqi Wang, Ke Cheng, Jiawei He, Qitai Wang, Hengchen Dai, Yuntao Chen, Fei Xia, and Zhaoxiang Zhang. Drivingdojo dataset: Advancing interactive and knowledgeenriched driving world model. In _NeurIPS_ , 2024. 2, 4, 16 

- [125] Yuqi Wang, Jiawei He, Lue Fan, Hongxin Li, Yuntao Chen, and Zhaoxiang Zhang. Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. In _CVPR_ , pages 14749–14759, 2024. 1, 4, 12, 13, 15 

- [126] Yuping Wang, Xiangyu Huang, Xiaokang Sun, Mingxuan Yan, Shuo Xing, Zhengzhong Tu, and Jiachen Li. Uniocc: A unified benchmark for occupancy forecasting and prediction in autonomous driving. In _ICCV_ , 2025. 4 

- [127] Julong Wei, Shanshuai Yuan, Pengfei Li, Qingda Hu, Zhongxue Gan, and Wenchao Ding. Occllama: An occupancy-language-action generative world model for autonomous driving. _arXiv preprint arXiv:2409.03272_ , 2024. 1, 4, 6, 7, 12, 14, 15, 16 

- [128] Licheng Wen, Daocheng Fu, Song Mao, Pinlong Cai, Min Dou, Yikang Li, and Yu Qiao. Limsim: A long-term interactive multi-scenario traffic simulator. In _IEEE 26th International Conference on Intelligent Transportation Systems (ITSC)_ , pages 1255–1262, 2023. 3 

- [129] Yuqing Wen, Yucheng Zhao, Yingfei Liu, Fan Jia, Yanhui Wang, Chong Luo, Chi Zhang, Tiancai Wang, Xiaoyan Sun, and Xiangyu Zhang. Panacea: Panoramic and controllable video generation for autonomous driving. In _CVPR_ , pages 6902–6912, 2024. 2, 4, 11, 13 

- [130] Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, Deva Ramanan, Peter Carr, and James Hays. Argoverse 2: Next generation datasets for self-driving perception and forecasting. In _NeurIPS_ , 2021. 4 

- [131] Guile Wu, David Huang, Dongfeng Bai, and Bingbing Liu. Moviedrive: Multi-modal multi-view urban scene video generation. _arXiv preprint arXiv:2508.14327_ , 2025. 7, 11, 13 

- [132] Yanhao Wu, Haoyang Zhang, Tianwei Lin, Lichao Huang, Shujie Luo, Rui Wu, Congpei Qiu, Wei Ke, and Tong Zhang. Generating multimodal driving scenes via nextscene prediction. In _CVPR_ , pages 6844–6853, 2025. 7 

- [133] Ziyi Wu, Nikita Dvornik, Klaus Greff, Thomas Kipf, and Animesh Garg. Slotformer: Unsupervised visual dynamics simulation with object-centric models. In _ICLR_ , 2022. 9 

- [134] Zehuan Wu, Jingcheng Ni, Xiaodong Wang, Yuxin Guo, Rui Chen, Lewei Lu, Jifeng Dai, and Yuwen Xiong. Holodrive: Holistic 2d-3d multi-modal street scene generation for autonomous driving. _arXiv preprint arXiv:2412.01407_ , 2024. 8, 11, 13 

- [135] Tianze Xia, Yongkang Li, Lijun Zhou, Jingfeng Yao, Kaixin Xiong, Haiyang Sun, Bing Wang, Kun Ma, Hangjun Ye, Wenyu Liu, et al. Drivelaw: Unifying planning and video generation in a latent driving world. _arXiv preprint arXiv:2512.23421_ , 2025. 12 

- [136] Lingyu Xiao, Jiang-Jiang Liu, Sen Yang, Xiaofan Li, Xiaoqing Ye, Wankou Yang, and Jingdong Wang. Learning multiple probabilistic decisions from latent world model in autonomous driving. In _Proc. IEEE Int. Conf. Robotics Automation_ , pages 1279–1285. IEEE, 2024. 8 

- [137] Haoran Xu, Peixi Peng, Guang Tan, Yiqian Chang, Yisen Zhao, and Yonghong Tian. Temporal triplane transformers as occupancy world models. _arXiv preprint arXiv:2503.07338_ , 2025. 7, 14, 15, 17 

- [138] Tianshuo Xu, Hao Lu, Xu Yan, Yingjie Cai, Bingbing Liu, and Yingcong Chen. Occ-llm: Enhancing autonomous driving with occupancy-based large language models. In _Proc. IEEE Int. Conf. Robotics Automation_ , 2025. 1, 4, 6, 7, 12, 14, 15, 16 

- [139] Xiang Xu, Ao Liang, Youquan Liu, Linfeng Li, Lingdong Kong, Ziwei Liu, and Qingshan Liu. U4d: Uncertaintyaware 4d world modeling from lidar sequences. _arXiv preprint arXiv:2512.02982_ , 2025. 6 

- [140] Tianyi Yan, Dongming Wu, Wencheng Han, Junpeng Jiang, Xia Zhou, Kun Zhan, Cheng-zhong Xu, and Jianbing Shen. Drivingsphere: Building a high-fidelity 4d world for closed-loop simulation. In _CVPR_ , pages 27531–27541, 2025. 1, 2, 10 

- [141] Ziyang Yan, Wenzhen Dong, Yihua Shao, Yuhang Lu, Haiyang Liu, Jingwen Liu, Haozhe Wang, Zhe Wang, Yan 

22 

Wang, Fabio Remondino, et al. Renderworld: World model with self-supervised 3d label. In _Proc. IEEE Int. Conf. Robotics Automation_ , pages 6063–6070. IEEE, 2025. 1, 4, 6, 11, 14, 15 

- [142] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, Jun Zhang, Andreas Geiger, Yu Qiao, and Hongyang Li. Generalized predictive model for autonomous driving. In _CVPR_ , 2024. 2, 4, 13 

- [143] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Generalized predictive model for autonomous driving. In _CVPR_ , pages 14662–14672, 2024. 16 

- [144] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. Resim: Reliable world simulation for autonomous driving. _arXiv preprint arXiv:2506.09981_ , 2025. 9, 10 

- [145] Jihan Yang, Shusheng Yang, Anjali W Gupta, Rilyn Han, Li Fei-Fei, and Saining Xie. Thinking in space: How multimodal large language models see, remember, and recall spaces. In _CVPR_ , pages 10632–10643, 2025. 12 

- [146] Shusheng Yang, Jihan Yang, Pinzhi Huang, Ellis Brown, Zihao Yang, Yue Yu, Shengbang Tong, Zihan Zheng, Yifan Xu, Muhan Wang, et al. Cambrian-s: Towards spatial supersensing in video. _arXiv preprint arXiv:2511.04670_ , 2025. 12 

- [147] Xuemeng Yang, Licheng Wen, Tiantian Wei, Yukai Ma, Jianbiao Mei, Xin Li, Wenjie Lei, Daocheng Fu, Pinlong Cai, Min Dou, et al. Drivearena: A closed-loop generative simulation platform for autonomous driving. In _CVPR_ , pages 26933–26943, 2025. 1, 2, 10, 16 

- [148] Yu Yang, Jianbiao Mei, Yukai Ma, Siliang Du, Wenqing Chen, Yijie Qian, Yuxiang Feng, and Yong Liu. Driving in the occupancy world: Vision-centric 4d occupancy forecasting and planning via world models for autonomous driving. In _AAAI_ , 2025. 4, 6, 7, 9, 12, 15, 16 

- [149] Zetong Yang, Li Chen, Yanan Sun, and Hongyang Li. Visual point cloud forecasting enables scalable autonomous driving. In _CVPR_ , pages 14673–14684, 2024. 1, 2, 4, 6, 7, 12, 13, 14 

- [150] Zhuoran Yang, Xi Guo, Chenjing Ding, Chiyu Wang, and Wei Wu. Physical informed driving world model. _arXiv preprint arXiv:2412.08410_ , 2024. 1, 4, 11, 13, 16 

- [151] Zhenjie Yang, Xiaosong Jia, Qifeng Li, Xue Yang, Maoqing Yao, and Junchi Yan. Raw2drive: Reinforcement learning with aligned world models for end-to-end autonomous driving (in carla v2). In _NeurIPS_ , 2025. 4, 8, 10, 15, 16 

- [152] Shuang Zeng, Xinyuan Chang, Mengwei Xie, Xinran Liu, Yifan Bai, Zheng Pan, Mu Xu, Xing Wei, and Ning Guo. Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving. In _NeurIPS_ , 2025. 1, 12, 15 

- [153] Zifan Zeng, Chongzhe Zhang, Feng Liu, Joseph Sifakis, Qunli Zhang, Shiming Liu, and Peng Wang. World models: The safety perspective. In _2024 IEEE 35th International Symposium on Software Reliability Engineering Workshops (ISSREW)_ , pages 369–376. IEEE, 2024. 1 

- [154] Bozhou Zhang, Nan Song, Jingyu Li, Xiatian Zhu, Jiankang Deng, and Li Zhang. Future-aware end-to-end driving: Bidirectional modeling of trajectory planning and scene evolution. In _NeurIPS_ , 2025. 1, 12, 15 

- [155] Haiming Zhang, Ying Xue, Xu Yan, Jiacheng Zhang, Weichao Qiu, Dongfeng Bai, Bingbing Liu, Shuguang Cui, and Zhen Li. An efficient occupancy world model via decoupled dynamic flow and image-assisted training. _arXiv preprint arXiv:2412.13772_ , 2024. 1, 4, 6, 7, 14, 15, 17 

- [156] Jiazhao Zhang, Anqi Li, Yunpeng Qi, Minghan Li, Jiahang Liu, Shaoan Wang, Haoran Liu, Gengze Zhou, Yuze Wu, Xingxing Li, et al. Embodied navigation foundation model. _arXiv preprint arXiv:2509.12129_ , 2025. 16 

- [157] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, et al. Epona: Autoregressive diffusion world model for autonomous driving. In _ICCV_ , 2025. 4, 5, 13, 15 

- [158] Lunjun Zhang, Yuwen Xiong, Ze Yang, Sergio Casas, Rui Hu, and Raquel Urtasun. Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion. In _ICLR_ , 2024. 4, 5, 9, 13, 14 

- [159] Tianrui Zhang, Yichen Liu, Zilin Guo, Yuxin Guo, Jingcheng Ni, Chenjing Ding, Dan Xu, Lewei Lu, and Zehuan Wu. Cvd-storm: Cross-view video diffusion with spatial-temporal reconstruction model for autonomous driving. _arXiv preprint arXiv:2510.07944_ , 2025. 7, 13 

- [160] Yumeng Zhang, Shi Gong, Kaixin Xiong, Xiaoqing Ye, Xiao Tan, Fan Wang, Jizhou Huang, Hua Wu, and Haifeng Wang. Bevworld: A multimodal world model for autonomous driving via unified bev latent space. _arXiv preprint arXiv:2407.05679_ , 2024. 7, 13, 16 

- [161] Zhejun Zhang, Alexander Liniger, Dengxin Dai, Fisher Yu, and Luc Van Gool. Trafficbots: Towards world models for autonomous driving simulation and motion prediction. In _Proc. IEEE Int. Conf. Robotics Automation_ , pages 1522– 1529. IEEE, 2023. 1, 9, 10 

- [162] Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xueyang Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, et al. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. In _CVPR_ , 2025. 11 

- [163] Guosheng Zhao, Xiaofeng Wang, Zheng Zhu, Xinze Chen, Guan Huang, Xiaoyi Bao, and Xingang Wang. Drivedreamer-2: Llm-enhanced world models for diverse driving video generation. In _AAAI_ , 2025. 4, 10, 11, 13 

- [164] Zongchuang Zhao, Haoyu Fu, Dingkang Liang, Xin Zhou, Dingyuan Zhang, Hongwei Xie, Bing Wang, and Xiang Bai. Extending large vision-language model for diverse interactive tasks in autonomous driving. _arXiv preprint arXiv:2505.08725_ , 2025. 16 

- [165] Zhida Zhao, Talas Fu, Yifan Wang, Lijun Wang, and Huchuan Lu. From forecasting to planning: Policy world model for collaborative state-action prediction. In _NeurIPS_ , 2025. 12, 15, 16 

- [166] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d- 

23 

vla: A 3d vision-language-action generative world model. In _Proc. Int. Conf. Mach. Learn._ , 2024. 8 

- [167] Wenzhao Zheng, Weiliang Chen, Yuanhui Huang, Borui Zhang, Yueqi Duan, and Jiwen Lu. Occworld: Learning a 3d occupancy world model for autonomous driving. In _ECCV_ , pages 55–72. Springer, 2024. 1, 4, 6, 9, 12, 14, 15 

- [168] Wenzhao Zheng, Zetian Xia, Yuanhui Huang, Sicheng Zuo, Jie Zhou, and Jiwen Lu. Doe-1: Closed-loop autonomous driving with large world model. _arXiv preprint arXiv:2412.09627_ , 2024. 5, 12, 13, 15, 16 

- [169] Xiaoji Zheng, Ziyuan Yang, Yanhao Chen, Yuhang Peng, Yuanrong Tang, Gengyuan Liu, Bokui Chen, and Jiangtao Gong. Coirl-ad: Collaborative-competitive imitationreinforcement learning in latent world models for autonomous driving. _arXiv preprint arXiv:2510.12560_ , 2025. 10 

- [170] Yupeng Zheng, Pengxuan Yang, Zebin Xing, Qichao Zhang, Yuhang Zheng, Yinfeng Gao, Pengfei Li, Teng Zhang, Zhongpu Xia, Peng Jia, et al. World4drive: End-toend autonomous driving via intention-aware physical latent world model. In _ICCV_ , pages 28632–28642, 2025. 1, 4, 8, 15 

- [171] Sizhuo Zhou, Xiaosong Jia, Fanrui Zhang, Junjie Li, Juyong Zhang, Yukang Feng, Jianwen Sun, Songbur Wong, Junqi You, and Junchi Yan. Lagen: Towards autoregressive lidar scene generation. _arXiv preprint arXiv:2511.21256_ , 2025. 1, 6, 9, 13, 14 

- [172] Xin Zhou, Dingkang Liang, Wei Xu, Xingkui Zhu, Yihan Xu, Zhikang Zou, and Xiang Bai. Dynamic adapter meets prompt tuning: Parameter-efficient transfer learning for point cloud analysis. In _CVPR_ , pages 14707–14717, 2024. 5 

- [173] Xin Zhou, Dingkang Liang, Sifan Tu, Xiwu Chen, Yikang Ding, Dingyuan Zhang, Feiyang Tan, Hengshuang Zhao, and Xiang Bai. Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation. In _ICCV_ , 2025. 1, 4, 6, 7, 12, 13, 14, 16 

- [174] Yunsong Zhou, Michael Simon, Zhenghao Peng, Sicheng Mo, Hongzi Zhu, Minyi Guo, and Bolei Zhou. Simgen: Simulator-conditioned driving scene generation. In _NeurIPS_ , pages 48838–48874, 2024. 4 

- [175] Haoran Zhu, Zhenyuan Dong, Kristi Topollai, and Anna Choromanska. Ad-l-jepa: Self-supervised spatial world models with joint embedding predictive architecture for autonomous driving with lidar data. In _CVPR_ , 2026. 8, 13 

- [176] Zheng Zhu, Xiaofeng Wang, Wangbo Zhao, Chen Min, Nianchen Deng, Min Dou, Yuqi Wang, Botian Shi, Kai Wang, Chi Zhang, et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arXiv preprint arXiv:2405.03520_ , 2024. 1 

- [177] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Gaussianworld: Gaussian world model for streaming 3d occupancy prediction. In _CVPR_ , 2025. 4, 7, 17 

- [178] Vlas Zyrianov, Henry Che, Zhijian Liu, and Shenlong Wang. Lidardm: Generative lidar simulation in a generated world. In _Proc. IEEE Int. Conf. Robotics Automation_ , pages 6055–6062. IEEE, 2025. 1, 6, 9, 11 

24 

