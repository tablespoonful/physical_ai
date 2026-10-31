---
title: "DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation"
date: "2024-03-11"
authors: "Guosheng Zhao; Xiaofeng Wang; Zheng Zhu; Xinze Chen; Guan Huang; Xiaoyi Bao"
url: https://arxiv.org/abs/2403.06845
pdf: https://arxiv.org/pdf/2403.06845
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2403.06845)** / [論文ページ](https://arxiv.org/abs/2403.06845)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation** 

- Guosheng Zhao<sup>1</sup><sup>_∗_</sup> , Xiaofeng Wang<sup>1</sup><sup>_∗_</sup> , Zheng Zhu<sup>2</sup><sup>_∗_�</sup> , Xinze Chen<sup>2</sup> , Guan Huang<sup>2</sup> , Xiaoyi Bao<sup>1</sup> , and Xingang Wang<sup>1�</sup> 

   - 1 Institute of Automation, Chinese Academy of Sciences 2 GigaAI Project Page: `https://drivedreamer2.github.io` 


**Fig. 1:** _DriveDreamer-2_ demonstrates powerful capabilities in generating multi-view driving videos. _DriveDreamer-2_ can produce driving videos based on user descriptions, which improves the diversity of the synthetic data. Besides, the generation quality of _DriveDreamer-2_ surpasses other state-of-the-art methods and effectively enhances downstream tasks. 

**Abstract.** World models have demonstrated superiority in autonomous driving, particularly in the generation of multi-view driving videos. However, significant challenges still exist in generating customized driving 

2 G. Zhao, X. Wang et al. 

videos. In this paper, we propose _DriveDreamer-2_ , which builds upon the framework of DriveDreamer and incorporates a Large Language Model (LLM) to generate user-defined driving videos. Specifically, an LLM interface is initially incorporated to convert a user’s query into agent trajectories. Subsequently, a HDMap, adhering to traffic regulations, is generated based on the trajectories. Ultimately, we propose the Unified Multi-View Model to enhance temporal and spatial coherence in the generated driving videos. _DriveDreamer-2_ is the first world model to generate customized driving videos, it can generate uncommon driving videos (e.g., vehicles abruptly cut in) in a user-friendly manner. Besides, experimental results demonstrate that the generated videos enhance the training of driving perception methods (e.g., 3D detection and tracking). Furthermore, video generation quality of _DriveDreamer-2_ surpasses other state-of-the-art methods, showcasing FID and FVD scores of 11.2 and 55.7, representing relative improvements of _∼_ 30% and _∼_ 50%. 

**Keywords:** World models · Autonomous driving · Video generation 

## **1 Introduction** 

World models for autonomous driving [23,25,59,62] have drawn extensive attention from both the industry and academia in recent years. Benefiting from their excellent predictive capabilities, autonomous driving world models facilitate the generation of diverse driving videos, encompassing even long-tail scenarios. The generated driving videos can be utilized to enhance the training of various driving perception approaches, proving highly beneficial for practical applications in autonomous driving. 

World modeling in autonomous driving presents a formidable challenge due to its inherent complexity and large sampling space. Early approaches [8, 22] mitigate these problems by incorporating world modeling within the Bird’s Eye View (BEV) semantic segmentation space. However, these methods primarily explore world models in simulated autonomous driving environments. In the recent evolution of autonomous driving technologies, there has been a substantial leap forward in the development of world models. This progress has been propelled by the utilization of cutting-edge diffusion models [5, 17, 18, 39, 40, 46], exemplified by notable contributions such as DriveDreamer [59], Drive-WM [62], MagicDrive [7], Panacea [64], and the integration of large language models like GAIA1 [23], ADriver-I [25]. These sophisticated models have played a pivotal role in pushing the boundaries of world modeling capabilities, enabling researchers and engineers to delve into increasingly intricate and realistic driving scenarios. However, it is important to note that a majority of these methods rely heavily on structured information (e.g., 3D boxes, HDMaps, and optical flow) or real-world image frames as conditions. This dependence not only constrains interactivity but also limits the diversity of generated videos. 

To tackle the aforementioned challenges, we propose _DriveDreamer-2_ , which is the first world model to generate diverse driving videos in a user-friendly manner. In contrast to previous methods [7,59,62] that rely on structured conditions 

DriveDreamer-2 3 

either from specific datasets or sophisticated annotations, _DriveDreamer-2_ emphasizes generating customized driving videos by simulating various traffic conditions with user-friendly text prompts. Specifically, the traffic simulation task has been disentangled into the generation of foreground conditions (trajectories of the ego-car and other agents) and background conditions (HDMaps of lane boundary, lane divider, and pedestrian crossing). For foreground generation, a functional library is constructed to finetune a Large Language Model (LLM), enabling it to generate agent trajectories based on user text input. For background conditions, we propose the HDMap generator that employs a diffusion model to simulate road structures. In this process, the previously generated agent trajectories are involved as conditional inputs, which allows the HDMap generator to learn the associations between foreground and background conditions in driving scenes. Building upon the generated traffic structured conditions, we employ the DriveDreamer [59] framework to generate multi-view driving videos. It is noted that we introduce the Unified Multi-view Video Model (UniMVM) within the DriveDreamer framework, which is designed to unify both intra-view and crossview spatial consistency, enhancing the overall temporal and spatial coherence in the generated driving videos. 

Extensive experiment results show that _DriveDreamer-2_ is capable of producing diverse user-customized videos, including uncommon scenarios where vehicles abruptly cut in (depicted in Fig. 1). Besides, _DriveDreamer-2_ can generate highquality driving videos with an FID of 11.2 and FVD of 55.7, relatively improving previous best-performing methods by _∼_ 30% and _∼_ 50%. Furthermore, experiments are conducted to verify that driving videos generated by _DriveDreamer-2_ can enhance the training of various autonomous driving perception methods, where the performance of detection and tracking are relatively improved by _∼_ 4% and _∼_ 8%. 

The main contributions of this paper can be summarized as follows: 

- We present _DriveDreamer-2_ , which is the first world model to generate diverse driving videos in a user-friendly manner. 

- We propose a traffic simulation pipeline employing only text prompts as input, which can be utilized to generate diverse traffic conditions for driving video generation. 

- UniMVM is presented to seamlessly integrate intra-view and cross-view spatial consistency, elevating the overall temporal and spatial coherence within the generated driving videos. 

- Extensive experiments are conducted to show that _DriveDreamer-2_ can craft diverse customized driving videos. Besides, _DriveDreamer-2_ enhances the FID and FVD by _∼_ 30% and _∼_ 50% compared to previous best-performing methods. Moreover, the driving videos generated by _DriveDreamer-2_ enhance the training of various driving perception methods. 

4 G. Zhao, X. Wang et al. 

## **2 Related Works** 

### **2.1 World Models** 

The primary objective of world methods is to establish dynamic environmental models, endowing agents with predictive capabilities for the future. In the early exploration, Variational Autoencoders (VAE) [31] and Long Short-Term Memory (LSTM) [19] are employed to capture transition dynamics and rendering functionality, showcasing remarkable success across diverse applications [9–13,13,29,36,48,65]. Constructing driving world models poses distinctive challenges, primarily arising from the high sample complexity inherent in real-world driving tasks [3]. To address these challenges, ISO-Dream [42] introduces an explicit disentanglement of visual dynamics into controllable and uncontrollable states. MILE [22] strategically incorporates world modeling within the Bird’s Eye View (BEV) semantic segmentation space. Recently, DriveDreamer [59], GAIA1 [23], ADriver-I [25], and Drive-WM [62] have explored the training of driving world models in the real world, leveraging powerful diffusion models or natural language models. However, most of these methods heavily depend on structured information (e.g., 3D boxes, HDMaps, and optical flow) as conditions. This dependency not only constrains interactivity but also limits generation diversity. 

### **2.2 Video Generation** 

Video generation and prediction are pivotal techniques for understanding the visual world. In the early stages of video generation, methods like Variational Autoencoders (VAEs) [4, 21], flow-based model [33], and Generative Adversarial Networks (GANs) [38, 47, 53, 56] are explored. Language models [20, 26, 32, 45, 51, 55, 60, 63] are also employed for intricate visual dynamics modeling. Recent advancements have seen diffusion models [5, 17, 18, 39, 40, 46] extending their influence to video generation. Notably, video diffusion models [1, 14, 16, 28, 49, 58, 67] exhibit superior capabilities in generating high-quality videos with realistic frames and smooth transitions, offering enhanced controllability. These models adapt seamlessly to various input conditions, including text, canny, sketch, semantic maps, and depth maps. In the realm of autonomous driving, _DriveDreamer-2_ leverages powerful diffusion models for learning visual dynamics. 

### **2.3 Traffic Simulation** 

Driving simulators stand as a cornerstone in self-driving development, aiming to offer a controlled environment to mimic real-world conditions. LCTGen [52] utilizes an LLM to encode detailed language descriptions to a vector and subsequently employs a generator to produce corresponding simulated scenarios. This method requires highly detailed language descriptions, including information such as the speed and orientation of agents. TrafficGen [6] comprehends the inherent relationships within traffic scenarios, enabling the generation of 

DriveDreamer-2 5 


**Fig. 2:** The overall framework of _DriveDreamer-2_ involves initially generating agent trajectories according to the user query, followed by producing a realistic HDMap, and finally generating multi-view driving videos. 

diverse and legitimate traffic flows within the same map. CTG [70] generates traffic simulations by employing manually designed loss functions that adhere to traffic constraints. CTG++ [69] further extends CTG by utilizing GPT-4 [41] to convert user language descriptions into a loss function, which guides the scene-level conditional diffusion model to generate the corresponding scenario. In _DriveDreamer-2_ , we construct a functional library to finetune the LLM to achieve a user-friendly text-to-traffic simulation, which eliminates intricate loss design or complex text prompt inputs. 

## **3 DriveDreamer-2** 

Fig. 2 illustrates the overall framework of _DriveDreamer-2_ . A customized traffic simulation is first proposed to generate foreground agent trajectories and background HDMaps. Specifically, _DriveDreamer-2_ utilizes a finetuned LLM to translate user prompts into agent trajectories, and the HDMap generator is then introduced to simulate road structures using the generated trajectories as conditions. Leveraging the customized traffic simulation pipeline, _DriveDreamer-2_ is capable of generating diverse structured conditions for the subsequent video generation. Building upon the architecture of DriveDreamer [59], the UniMVM framework is proposed to unify both intra-view and cross-view spatial consistency, thereby enhancing the overall temporal and spatial coherence in the generated driving videos. In the subsequent sections, we delve into the details of the customized traffic simulation and the UniMVM framework. 

### **3.1 Customized Traffic Simulation** 

In the proposed customized traffic simulation pipeline, a trajectory-generation function library is constructed to finetune the LLM, which facilitates transferring user prompts into diverse agent trajectories, encompassing maneuvers such as cut-ins and U-turns. Additionally, the pipeline incorporates the HDMap generator to simulate the background road structures. During this phase, the previously 

G. Zhao, X. Wang et al. 

6 


**Fig. 3:** The overview of customized trajectory generation. Initially, we leverage the established function library to assemble Text-to-Python-Script pairs. Subsequently, the constructed dataset is employed to finetune LLM. Finally, the customized trajectories is generated by LLM based on user query. 

generated agent trajectories serve as conditional inputs, ensuring that the resulting HDMap adheres to traffic constraints. In the following, we elaborate on the finetuning process of the LLM and the framework of the HDMap generator. 

**Finetuning LLM for Trajectory Generation** Previous traffic simulation methods [37, 69, 70] necessitate the intricate specification of parameters, involving details such as the agent’s speed, position, acceleration, and mission goal. To simplify this intricate process, we propose to finetune LLM with the constructed trajectory-generation function library, allowing for the efficient transformation of user-friendly language inputs into comprehensive traffic simulation scenarios. As depicted in Fig. 3, the constructed function library encompasses 18 functions, including agent functions (steering, constant speed, acceleration, and braking), pedestrian functions (walking direction and speed), and other utility functions such as saving trajectories. Building upon these functions, Text-toPython-Scripts pairs are manually curated for finetuning LLM (GPT-3.5). The scripts include a range of fundamental scenarios such as lane-changing, overtaking, following other vehicles, and executing U-turns. Additionally, we encompass more uncommon scenarios like pedestrians abruptly crossing, and vehicles cutting into the lane. Taking the user input _a vehicle cuts in_ as an example, the corresponding script involves the following steps: initially generating a trajectory of cutting in ( `agent.cut_in()` ), followed by generating the corresponding ego car trajectory ( `agent.forward()` ), and ultimately utilizing the saving function from utilities to directly output the trajectory of the ego-car and other agents in array format. For additional details, please refer to the supplementary materials. In the inference phase, we follow [37] to expand prompt inputs to a pre-defined template, and the finetuned LLM can directly output the trajectory array. **HDMap Generation** A comprehensive traffic simulation not only entails the trajectories of foreground agents but also necessitates the generation of back- 

DriveDreamer-2 7 


BEV trajectory BEV HDMap 1 BEV HDMap 2 BEV HDMap 3 

**Fig. 4:** The proposed HDMap generator can generate diverse BEV HDMaps based on the same BEV trajectory input. The orange and yellow colors represent the motion trajectories of the ego car and other vehicles, respectively. The red color indicates road boundaries, the blue color represents lane dividers, and the green color signifies pedestrian crossings. 

ground HDMap elements such as lanes and pedestrian crosswalks. Therefore, the HDMap generator is proposed to ensure the background elements do not conflict with the foreground trajectories. In the HDMap generator, we formulate the background elements generation as a conditional image generation problem, where the conditional input is the BEV trajectory map _Tb ∈R_<sup>3</sup><sup>_×Hb×Wb_</sup> , and the target is the BEV HDMap _Hb ∈R_<sup>3</sup><sup>_×Hb×Wb_</sup> . Different from previous conditional image generation approaches [35, 68] that predominantly rely on outline conditions (edges, depths, boxes, segmentation maps), the proposed HDMap generator explores the correlations between the foreground and background traffic elements. Specifically, the HDMap generator is constructed upon an imagegeneration diffusion model. To train the generator, we curate a trajectory-toHDMap dataset _D_ = _{Tb, Hb}_ . In the trajectory map, distinct colors are assigned to represent different agent categories. Meanwhile, the target HDMap comprises three channels, representing lane boundaries, lane dividers, and pedestrian crossings, respectively. Within the HDMap generator, we employ stacks of 2D convolution layers to incorporate the trajectory map condition. The resulting feature maps _CT_ are then seamlessly integrated into the diffusion model using [68] (see supplement for additional architectural details). In the training stage, the diffusion forward process gradually adds noise _ϵ_ to the latent feature _Z_ 0, resulting in the noisy latent feature _ZTb_ . Then we train _ϵθ_ to predict the noise we added, and the HDMap generator _ϕ_ is optimized via 


where time step t is uniformly sampled from [1 _, Tb_ ]. As shown in Fig. 4, leveraging the proposed HDMap generator allows us to generate diverse HDMaps based on the same trajectory conditions. It is noteworthy that the generated HDMaps not only adhere to traffic constraints (lane boundaries positioned on either side of lane dividers, and pedestrian crossings at intersections) but also seamlessly integrate with trajectories. 

8 G. Zhao, X. Wang et al. 


**Fig. 5:** The comparison of multi-view video generation paradigms. All structural conditions and text prompts are omitted here to emphasize the distinctions between our UniMVM and previous methods. By adjusting the mask, UniMVM can generate videos conditioned on the initial frame, front view video, and without image input. 

### **3.2 UniMVM** 

Utilizing structured information generated by the customized traffic simulation, multi-view driving videos can be generated via the framework of DriveDreamer [59]. However, the view-wise attention introduced in previous methods [59, 66] can not guarantee multi-view consistency. To mitigate this problem, [34, 62, 64] employ image or video conditions to generate multi-view driving videos. While this approach enhances consistency between different views, it comes at the expense of reduced generation efficiency and diversity. In _DriveDreamer-2_ , we introduce the UniMVM within the DriveDreamer framework. The UniMVM is designed to unify the generation of multi-view driving videos both with and without adjacent view conditions, which ensures temporal and spatial coherence without compromising generation speed and diversity. 

**Formulation** In multi-view video dataset _pdata_ , x _∈R_<sup>_K×T ×_3</sup><sup>_×H×W_</sup> is a sequence of _T_ images with _K_ views, with height _H_ and width _W_ . Let x _i_ denote the sample of _i_ -th view, then the multi-view video joint distribution _p_ (x1 _, ...,_ xK) can be obtained by [62]: 


Eq. 2 indicates that adjacent view videos can be expanded with multiple generation steps, which is inefficient. In the proposed UniMVM, we draw inspiration from the Eq. 2 to expand the view. However, unlike Drive-WM [62] which requires the independent generation of views, UniMVM unifies multiple views as a complete patch. Specifically, we concatenate the multi-view video in the order of {FL, F, FR, BR, B, BL}<sup>1</sup> to obtain the spatially unified image x<sup>_′_</sup> _∈R_<sup>_T ×_3</sup><sup>_×H×KW_</sup> . Then we can obtain the multi-view driving video distribution _p_ (x<sup>_′_</sup> ): 


> 1 F:Front, L: Left, R: Right, B: Back. 

DriveDreamer-2 9 

where _m_ represents the mask of one of the all views. As shown in Fig. 5, we compare the paradigm of UniMVM with that of DriveDreamer [59] and DriveWM [62]. In contrast to these counterparts, UniMVM unifies multiple views into a complete patch for video generation without introducing cross-view parameters. Furthermore, various driving video generation tasks can be accomplished via adjusting the mask _m_ . Specifically, when _m_ is set to mask future _T −_ 1 frames, UniMVM enables future video prediction based on the input of the first frame. Configuring _m_ to mask {FL, FR, BR, B, BL} views empowers UniMVM to achieve multi-view video outpainting, leveraging a front-view video input. Furthermore, UniMVM can generate multi-view videos when _m_ is set to mask all video frames, and both quantitative and qualitative experiments verify that UniMVM is capable of generating temporally and spatially coherent videos with enhanced efficiency and diversity. 

**Video Generation** Based on the UniMVM formulation, driving videos can be generated within the framework of DriveDreamer [59]. Specifically, our approach first unify the traffic structured conditions, which results in sequences of HDMaps _{Hi}i_<sup>_N_</sup> =0<sup>_−_1</sup> _∈R_<sup>_N×_3</sup><sup>_×H×KW_</sup> and 3D boxes _{Bi}_<sup>_N_</sup> _i_ =0<sup>_−_1</sup> _∈R_<sup>_N×C×H×KW_</sup> ( _N_ is the frame number of video clip, and _C_ is the category number). Note that sequences of 3D boxes can be derived from agent trajectories, and the sizes of 3D boxes are determined based on the respective agent category. Unlike DriveDreamer, the 3D box conditions in _DriveDreamer-2_ no longer rely on position embedding and category embedding. Instead, the boxes are directly projected onto the image plane, functioning as a control condition. This approach eliminates introducing additional control parameters as in [59]. We adopt three encoders to embed HDMaps, 3D boxes, and image frames into latent space features _yH_ , _yB_ , and _yI_ . Then we concatenate the spatially aligned conditions _yH_ , _yB_ with _Zt_ to obtain the feature input _Zin_ , where _Zt_ is the noisy latent feature generated from _yI_ by the forward diffusion process. For the training of the video generator, all parameters are optimized via denoising score matching [27] (see supplement for details). 

## **4 Experiment** 

### **4.1 Experiment Details** 

**Dataset.** The training dataset is derived from the nuScenes dataset [2], consisting of 700 training videos and 150 validation videos. Each video encompasses approximately 20 seconds of recorded footage, captured by six surround-view cameras. With a frame rate of 12Hz, this accumulates to around 1 million video frames available for training. Following [59,61], we preprocess the nuScenes dataset to calculate 12Hz annotations. Specifically, HDMaps and 3D boxes are transformed to BEV perspective to train HDMap generation, and these annotations are projected to pixel coordinate to train video generation. 

**Training.** For agent trajectory generation, we employ GPT-3.5 as the LLM. Subsequently, we utilize the constructed text-to-script dataset to finetune GPT3.5 into an LLM with specialized trajectory generation knowledge. The proposed 

10 G. Zhao, X. Wang et al. 


**Fig. 6:** User-customized driving videos generated by _DriveDreamer-2_ . The top row depicts a scene where the ego car changes lanes, while the bottom row shows an unexpected pedestrian crossing the road at night. 

HDMap generator is built upon SD2.1 [46] with the ControlNet parameters [68] being trainable. The HDMap generator undergoes 55K training iterations with a batch size of 24 and a resolution of 512 _×_ 512. For the video generator, we harness the powerful video generation capabilities of SVD [1], and all the parameters are finetuned. During the training of the video generator, the mode is trained for 200K iterations with a batch size of 1, a video frame length of _N_ = 8, a view number of _K_ = 6, and a spatial size of 256 _×_ 448. All the experiments are conducted on NVIDIA A800 (80GB) GPUs, and we use the AdamW optimizer [30] with a learning rate 5 _×_ 10<sup>_−_5</sup> . 

**Evaluation.** Extensive qualitative and quantitative experiments are conducted to assess _DriveDreamer-2_ . For qualitative experiments, we visualize customized driving video generation to validate that _DriveDreamer-2_ can produce diverse driving videos in a user-friendly manner. Additionally, visualization comparisons are conducted between UniMVM and other generative paradigms to demonstrate that _DriveDreamer-2_ excels in generating temporally and spatially coherent videos. For quantitative experiments, the frame-wise Fréchet Inception Distance (FID) [43] and Fréchet Video Distance (FVD) [54] are utilized as metrics. Besides, StreamPETR [57], building upon a ResNet-50 [15] backbone, is trained at the same resolution of 256 _×_ 448 to evaluate the improvements of 3D object detection and multi-object tracking achieved by our generated results. More details can be found in the supplementary material. 

### **4.2 User-Customized Driving Video Generation** 

_DriveDreamer-2_ offers a user-friendly interface for generating driving videos. As depicted in Fig. 1a, users are only required to input a text prompt (e.g., _on a rainy day, there is a car cut in_ ). Then _DriveDreamer-2_ produces multiview driving videos aligned with the text input. Fig. 6 illustrates another two customized driving videos. The upper one depicts the process of the ego car changing lanes to the left during the daytime. The lower one showcases an unexpected pedestrian crossing the road at night, prompting the ego car to brake 

DriveDreamer-2 11 

to avoid the collision. Notably, the generated videos demonstrate an exceptional level of realism, where we can even observe the reflection of high beams on the pedestrian. 

**Table 1:** Comparison of the generation quality on nuScenes validation set. † denotes that the corresponding conditions are generated. 

|Method|Conditions|FID_↓_|FVD_↓_|
|---|---|---|---|
|DriveDreamer [59]|-|26.8|353.2|
|_DriveDreamer-2_|-|**25.0**|**105.1**|
|Drive-WM [62]|3-view videos†|**15.8**|122.7|
|_DriveDreamer-2_|1-view video|18.4|**74.9**|
|DriveDreamer [59]|1st-frame multi-view image|14.9|340.8|
|Drivingdiffusion [34]|1st-frame multi-view image†|15.8|332.0|
|Panacea [64]|1st-frame multi-view image†|16.9|139.0|
|_DriveDreamer-2_|1st-frame multi-view image|**11.2**|**55.7**|


### **4.3 Quality Evaluation of Generated Videos** 

To verify the video generation quality, we compare _DriveDreamer-2_ with various driving video generation approaches on the nuScenes validation set. For a fair comparison, we conducted evaluations under three different experimental settings—without image condition, with video condition, and with first frame multi-view image condition. Additionally, Drive-WM [62], DrivingDiffusion [34] and Panacea [64] adopt a two-stage pipeline, first generating visual conditions and then generating videos. The experimental results, as shown in Tab. 1, indicate that _DriveDreamer-2_ consistently achieves high-quality evaluation outcomes across all three settings. Specifically, in the absence of the image condition, _DriveDreamer-2_ attains an FID of 25.0 and an FVD of 105.1, showcasing a significant improvement over DriveDreamer [59]. Moreover, despite being limited to a single-view video condition, _DriveDreamer-2_ exhibits a 39% relative improvement in FVD compared to DriveWM [62], which utilizes a three-view video condition. Furthermore, when provided with the first-frame multi-view image condition, _DriveDreamer-2_ achieves an FID of **11.2** and an FVD of **55.7** , surpassing all previous methods by a considerable margin. 

**Table 2:** Comparison involving data augmentation using synthetic data on 3D object detection. 

|Image size|Initial frame|Real|Generated|mAP_↑_|mAOE_↓_|mAVE_↓_|NDS_↑_|
|---|---|---|---|---|---|---|---|
||-|✓|-|31.7|67.9|33.0|43.5|
|256_×_448|✓|✓|✓|32.6|61.7|**29.7**|45.2|
||-|✓|✓|**32.9**|**61.5**|30.4|**45.4**|


12 G. Zhao, X. Wang et al. 

**Table 3:** Comparison involving data augmentation using synthetic data on multiobject tracking. 

|Image size|Initial frame|Real|Generated|AMOTA_↑_|AMOTP_↓_|IDS_↓_|
|---|---|---|---|---|---|---|
||-|✓|-|28.9|1.419|687|
|256_×_448|✓|✓|✓|31.2|1.396|**542**|
||-|✓|✓|**31.3**|**1.387**|593|


To further validate the quality of the generated data, we employ the generated driving videos to enhance the training of 3D object detection and multi-object tracking. Specifically, we employ all structured conditions in the nuScenes training set to generate driving videos, which are combined with real videos to train StreamPETR [57] on downstream tasks. The experiment results are in Tab. 2 and Tab. 3. When the initial frame is used as a condition, the generated videos prove to be effective in enhancing the performance of downstream tasks. The 3D detection metrics, mAP and NDS, show a relative improvement of 2.8% and 3.9%, respectively. Besides, the tracking metrics, AMOTA and AMOTP, exhibit a relative enhancement of 8.0% and 1.6%. Furthermore, _DriveDreamer-2_ is capable of generating high-quality driving videos even in the absence of image conditions. Removing the image condition leads to increased diversity in the generated content, consequently further improving performance metrics for downstream tasks. Specifically, the mAP and NDS for 3D detection show a relative improvement of 3.8% and 4.4%, respectively, while the AMOTA and AMOTP for tracking tasks exhibit enhancements of 8.3% and 2.3%, compared to the baseline. 


**Fig. 7:** Visualization comparison between _DriveDreamer-2_ generation with and without UniMVM. The upper part depicts generation without UniMVM, while the lower part illustrates generation with UniMVM. It is evident that the inclusion of UniMVM results in higher multi-view consistency in the generated content. 


**Fig. 8:** Visualization comparison with different conditions. Under different image conditions, _DriveDreamer-2_ produces videos with a high level of multi-view consistency. Using the 1st frame image (row 1) as a condition, the diversity of the generated second frame (row 3) is constrained, which closely resembles the ground truth second frame (row 2). Employing the front-view video as a condition results in increased generation diversity (row 4), only the front-view image aligns closely with the ground truth (row 2). Strikingly, in the absence of image as a condition, _DriveDreamer-2_ produces the highest diversity (row 5). The generated colors of the cars and the street backgrounds differ significantly from the ground truth (row 2). 

### **4.4 Ablation Study** 

We conduct an ablation study to investigate the effect of diffusion backbone and the proposed UniMVM, and the results are in Tab. 4. Compared to SD1.4 [46] used in DriveDreamer, SVD [1] provides richer prior knowledge of videos, resulting in 17.2 FID and 94.6 FVD. The introduction of SVD results in an almost 70% improvement in FVD. Additionally, we also note that a slight decrease in FID, which we hypothesize is attributed to the introduction of the cross-view module, disrupting the SVD’s ability to learn spatial features. To fully unleash the potential of SVD in multi-view video generation, we propose UniMVM, which unifies constraints on intra- and cross-view, achieving remarkable FID and FVD scores of 11.2 and 55.7, respectively. These represent relative improvements of _∼_ 30% and _∼_ 80% compared to DriveDreamer. As depicted in Fig. 7, the upper row in each compared pair is generated by _DriveDreamer-2_ without UniMVM, while the lower row is generated by _DriveDreamer-2_ with UniMVM. In the absence of UniMVM, _DriveDreamer-2_ generates inconsistent results between views, including foreground vehicles and background structures. The introduction of UniMVM leads to significant improvements in generating multi-view videos, both in foreground and background aspects. The qualita- 

14 G. Zhao, X. Wang et al. 

**Table 4:** The ablation study on the backbone and UniMVM. Cross-view module denotes the cross-view attention used in previous methods [34, 59, 62, 64]. 

|Method|Backbone|Cross-view module|UniMVM|FID_↓_|FVD_↓_|
|---|---|---|---|---|---|
|DriveDreamer [59]|SD1.4|✓|-|14.9|340.8|
|DriveDreamer-2|SVD|✓<br>-|-<br>✓|17.2<br>**11.2**|94.6<br>**55.7**|


**Table 5:** The ablation study on different conditions. 

|Method|Conditions|FID_↓_|FVD_↓_|
|---|---|---|---|
|DiD59|-|26.8|353.2|
|rvereamer []|1st-frame multi-view image|14.9|340.8|
||-|25.0|105.1|
|DriveDreamer-2|1-view video|18.4|74.9|
||1-st frame multi-view image|**11.2**|**55.7**|


tive results demonstrate the impressive capability of our UniMVM in achieving multi-view consistency. 

Moreover, we explore the influence of various conditions on driving video generation, as shown in Tab. 5 and Fig. 8. The first row in Fig. 8 illustrates the ground truth (GT) of the first frame, representing the style of the GT video. Meanwhile, the second row displays the GT of the second frame, representing the GT of the generated multi-view frame. _DriveDreamer-2_ with the initial frame can generate results that are highly similar to the GT video, achieving optimal results in terms of FID and FVD, with scores of 11.2 and 55.7, respectively. The video generated by _DriveDreamer-2_ with the front-view video retains some aspects of the GT scene while also introducing some diversity, resulting in 17.2 FID and 94.6 FVD. _DriveDreamer-2_ can also generate extremely competitive results even without any image conditioning, achieving FID and FVD scores of 25.0 and 105.1, respectively. Notably, _DriveDreamer-2_ exhibits the highest diversity in this setting, where the generated appearance of cars and the street backgrounds differ significantly from the ground truth. 

## **5 Discussion and Conclusion** 

This paper introduces _DriveDreamer-2_ , an innovative extension of the DriveDreamer framework that pioneers the generation of user-customized driving videos. Leveraging a Large Language Model, _DriveDreamer-2_ first transfers user queries into foreground agent trajectories. Then the background traffic conditions can be generated using the proposed HDMap generator, with agent trajectories as conditions. The generated structured conditions can be utilized for video generation, and we propose UniMVM to enhance temporal and spatial coherence. We conduct extensive experiments to verify that _DriveDreamer-2_ can generate uncommon driving videos, such as abrupt vehicle maneuvers. Importantly, experimental results showcase the utility of the generated videos in enhancing the training of driving perception methods. Furthermore, _DriveDreamer-2_ demonstrates superior video generation quality compared to state-of-the-art methods, 

DriveDreamer-2 15 

achieving FID and FVD scores of 11.2 and 55.7, respectively. These scores represent remarkable relative improvements of approximately 30% and 50%, affirming the efficacy and advancement of _DriveDreamer-2_ in multi-view driving video generation. 

## **References** 

1. Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., et al.: Stable video diffusion: Scaling latent video diffusion models to large datasets. arXiv preprint arXiv:2311.15127 (2023) 4, 10, 13 

2. Caesar, H., Bankiti, V., Lang, A.H., Vora, S., Liong, V.E., Xu, Q., Krishnan, A., Pan, Y., Baldan, G., Beijbom, O.: nuscenes: A multimodal dataset for autonomous driving. CVPR (2019) 9, 23 

3. Chen, L., Wu, P., Chitta, K., Jaeger, B., Geiger, A., Li, H.: End-to-end autonomous driving: Challenges and frontiers. arXiv preprint arXiv:2306.16927 (2023) 4 

4. Denton, E., Fergus, R.: Stochastic video generation with a learned prior. In: ICML (2018) 4 

5. Dhariwal, P., Nichol, A.: Diffusion models beat gans on image synthesis. NeurIPS (2021) 2, 4, 21 

6. Feng, L., Li, Q., Peng, Z., Tan, S., Zhou, B.: Trafficgen: Learning to generate diverse and realistic traffic scenarios. In: ICRA (2023) 4 

7. Gao, R., Chen, K., Xie, E., Hong, L., Li, Z., Yeung, D.Y., Xu, Q.: Magicdrive: Street view generation with diverse 3d geometry control. arXiv preprint arXiv:2310.02601 (2023) 2 

8. Gao, Z., Mu, Y., Shen, R., Chen, C., Ren, Y., Chen, J., Li, S.E., Luo, P., Lu, Y.: Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model. arXiv preprint arXiv:2210.04017 (2022) 2 

9. Ha, D., Schmidhuber, J.: Recurrent world models facilitate policy evolution. NeurIPS (2018) 4 

10. Hafner, D., Lee, K.H., Fischer, I., Abbeel, P.: Deep hierarchical planning from pixels. NeurIPS (2022) 4 

11. Hafner, D., Lillicrap, T., Ba, J., Norouzi, M.: Dream to control: Learning behaviors by latent imagination. arXiv preprint arXiv:1912.01603 (2019) 4 

12. Hafner, D., Lillicrap, T., Norouzi, M., Ba, J.: Mastering atari with discrete world models. arXiv preprint arXiv:2010.02193 (2020) 4 

13. Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T.: Mastering diverse domains through world models. arXiv preprint arXiv:2301.04104 (2023) 4 

14. Harvey, W., Naderiparizi, S., Masrani, V., Weilbach, C., Wood, F.: Flexible diffusion modeling of long videos. NeurIPS (2022) 4 

15. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition. In: CVPR (2016) 10 

16. Ho, J., Chan, W., Saharia, C., Whang, J., Gao, R., Gritsenko, A., Kingma, D.P., Poole, B., Norouzi, M., Fleet, D.J., et al.: Imagen video: High definition video generation with diffusion models. arXiv preprint arXiv:2210.02303 (2022) 4 

17. Ho, J., Jain, A., Abbeel, P.: Denoising diffusion probabilistic models. NeurIPS (2020) 2, 4, 21 

18. Ho, J., Saharia, C., Chan, W., Fleet, D.J., Norouzi, M., Salimans, T.: Cascaded diffusion models for high fidelity image generation. JMLR (2022) 2, 4, 21 

G. Zhao, X. Wang et al. 

16 

19. Hochreiter, S., Schmidhuber, J.: Long short-term memory. Neural computation (1997) 4 

20. Hong, W., Ding, M., Zheng, W., Liu, X., Tang, J.: Cogvideo: Large-scale pretraining for text-to-video generation via transformers. arXiv preprint arXiv:2205.15868 (2022) 4 

21. Hsieh, J.T., Liu, B., Huang, D.A., Fei-Fei, L.F., Niebles, J.C.: Learning to decompose and disentangle representations for video prediction. NeurIPS (2018) 4 

22. Hu, A., Corrado, G., Griffiths, N., Murez, Z., Gurau, C., Yeo, H., Kendall, A., Cipolla, R., Shotton, J.: Model-based imitation learning for urban driving. NeurIPS (2022) 2, 4 

23. Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., Corrado, G.: Gaia-1: A generative world model for autonomous driving. arXiv preprint arXiv:2309.17080 (2023) 2, 4 

24. Hyvärinen, A., Dayan, P.: Estimation of non-normalized statistical models by score matching. JMLR (2005) 22 

25. Jia, F., Mao, W., Liu, Y., Zhao, Y., Wen, Y., Zhang, C., Zhang, X., Wang, T.: Adriver-i: A general world model for autonomous driving. arXiv preprint arXiv:2311.13549 (2023) 2, 4 

26. Kalchbrenner, N., Oord, A., Simonyan, K., Danihelka, I., Vinyals, O., Graves, A., Kavukcuoglu, K.: Video pixel networks. In: ICML (2017) 4 

27. Karras, T., Aittala, M., Aila, T., Laine, S.: Elucidating the design space of diffusionbased generative models. NeurIPS (2022) 9, 22 

28. Khachatryan, L., Movsisyan, A., Tadevosyan, V., Henschel, R., Wang, Z., Navasardyan, S., Shi, H.: Text2video-zero: Text-to-image diffusion models are zeroshot video generators. arXiv preprint arXiv:2303.13439 (2023) 4 

29. Kim, S.W., Zhou, Y., Philion, J., Torralba, A., Fidler, S.: Learning to simulate dynamic environments with gamegan. In: CVPR (2020) 4 

30. Kingma, D.P., Ba, J.: Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 (2014) 10 

31. Kingma, D.P., Welling, M.: Auto-encoding variational bayes. arXiv preprint arXiv:1312.6114 (2013) 4 

32. Kondratyuk, D., Yu, L., Gu, X., Lezama, J., Huang, J., Hornung, R., Adam, H., Akbari, H., Alon, Y., Birodkar, V., et al.: Videopoet: A large language model for zero-shot video generation. arXiv preprint arXiv:2312.14125 (2023) 4 

33. Kumar, M., Babaeizadeh, M., Erhan, D., Finn, C., Levine, S., Dinh, L., Kingma, D.: Videoflow: A flow-based generative model for video. arXiv preprint arXiv:1903.01434 (2019) 4 

34. Li, X., Zhang, Y., Ye, X.: Drivingdiffusion: Layout-guided multi-view driving scene video generation with latent diffusion model. arXiv preprint arXiv:2310.07771 (2023) 8, 11, 14 

35. Li, Y., Liu, H., Wu, Q., Mu, F., Yang, J., Gao, J., Li, C., Lee, Y.J.: Gligen: Open-set grounded text-to-image generation. In: CVPR (2023) 7 

36. Lin, J., Du, Y., Watkins, O., Hafner, D., Abbeel, P., Klein, D., Dragan, A.: Learning to model the world with language. arXiv preprint arXiv:2308.01399 (2023) 4 

37. Mao, J., Qian, Y., Zhao, H., Wang, Y.: Gpt-driver: Learning to drive with gpt. arXiv preprint arXiv:2310.01415 (2023) 6 

38. Mathieu, M., Couprie, C., LeCun, Y.: Deep multi-scale video prediction beyond mean square error. arXiv preprint arXiv:1511.05440 (2015) 4 

39. Nichol, A., Dhariwal, P., Ramesh, A., Shyam, P., Mishkin, P., McGrew, B., Sutskever, I., Chen, M.: Glide: Towards photorealistic image generation and edit- 

DriveDreamer-2 17 

ing with text-guided diffusion models. arXiv preprint arXiv:2112.10741 (2021) 2, 4 

40. Nichol, A.Q., Dhariwal, P.: Improved denoising diffusion probabilistic models. In: ICML (2021) 2, 4 

41. OpenAI, R.: Gpt-4 technical report. arxiv 2303.08774. View in Article (2023) 5 42. Pan, M., Zhu, X., Wang, Y., Yang, X.: Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. NeurIPS (2022) 4 

43. Parmar, G., Zhang, R., Zhu, J.Y.: On aliased resizing and surprising subtleties in gan evaluation. In: CVPR (2022) 10 

44. Poole, B., Jain, A., Barron, J.T., Mildenhall, B.: Dreamfusion: Text-to-3d using 2d diffusion. arXiv preprint arXiv:2209.14988 (2022) 21 

45. Ranzato, M., Szlam, A., Bruna, J., Mathieu, M., Collobert, R., Chopra, S.: Video (language) modeling: a baseline for generative models of natural videos. arXiv preprint arXiv:1412.6604 (2014) 4 

46. Rombach, R., Blattmann, A., Lorenz, D., Esser, P., Ommer, B.: High-resolution image synthesis with latent diffusion models. In: CVPR (2022) 2, 4, 10, 13 

47. Saito, M., Matsumoto, E., Saito, S.: Temporal generative adversarial nets with singular value clipping. In: ICCV (2017) 4 

48. Seo, Y., Hafner, D., Liu, H., Liu, F., James, S., Lee, K., Abbeel, P.: Masked world models for visual control. In: CoRL (2023) 4 

49. Singer, U., Polyak, A., Hayes, T., Yin, X., An, J., Zhang, S., Hu, Q., Yang, H., Ashual, O., Gafni, O., et al.: Make-a-video: Text-to-video generation without textvideo data. arXiv preprint arXiv:2209.14792 (2022) 4 

50. Song, Y., Sohl-Dickstein, J., Kingma, D.P., Kumar, A., Ermon, S., Poole, B.: Scorebased generative modeling through stochastic differential equations. arXiv preprint arXiv:2011.13456 (2020) 21 

51. Srivastava, N., Mansimov, E., Salakhudinov, R.: Unsupervised learning of video representations using lstms. In: ICML (2015) 4 

52. Tan, S., Ivanovic, B., Weng, X., Pavone, M., Kraehenbuehl, P.: Language conditioned traffic generation. arXiv preprint arXiv:2307.07947 (2023) 4 

53. Tulyakov, S., Liu, M.Y., Yang, X., Kautz, J.: Mocogan: Decomposing motion and content for video generation. In: CVPR (2018) 4 

54. Unterthiner, T., Van Steenkiste, S., Kurach, K., Marinier, R., Michalski, M., Gelly, S.: Towards accurate generative models of video: A new metric & challenges. arXiv preprint arXiv:1812.01717 (2018) 10 

55. Villegas, R., Babaeizadeh, M., Kindermans, P.J., Moraldo, H., Zhang, H., Saffar, M.T., Castro, S., Kunze, J., Erhan, D.: Phenaki: Variable length video generation from open domain textual description. ICLR (2023) 4 

56. Vondrick, C., Pirsiavash, H., Torralba, A.: Generating videos with scene dynamics. NeurIPS (2016) 4 

57. Wang, S., Liu, Y., Wang, T., Li, Y., Zhang, X.: Exploring object-centric temporal modeling for efficient multi-view 3d object detection. arXiv preprint arXiv:2303.11926 (2023) 10, 12, 22 

58. Wang, X., Yuan, H., Zhang, S., Chen, D., Wang, J., Zhang, Y., Shen, Y., Zhao, D., Zhou, J.: Videocomposer: Compositional video synthesis with motion controllability. arXiv preprint arXiv:2306.02018 (2023) 4 

59. Wang, X., Zhu, Z., Huang, G., Chen, X., Lu, J.: Drivedreamer: Towards real-worlddriven world models for autonomous driving. arXiv preprint arXiv:2309.09777 (2023) 2, 3, 4, 5, 8, 9, 11, 14 

G. Zhao, X. Wang et al. 

18 

60. Wang, X., Zhu, Z., Huang, G., Wang, B., Chen, X., Lu, J.: Worlddreamer: Towards general world models for video generation via predicting masked tokens. arXiv preprint arXiv:2401.09985 (2024) 4 

61. Wang, X., Zhu, Z., Zhang, Y., Huang, G., Ye, Y., Xu, W., Chen, Z., Wang, X.: Are we ready for vision-centric driving streaming perception? the asap benchmark. In: CVPR (2023) 9 

62. Wang, Y., He, J., Fan, L., Li, H., Chen, Y., Zhang, Z.: Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving. arXiv preprint arXiv:2311.17918 (2023) 2, 4, 8, 9, 11, 14 

63. Weissenborn, D., Täckström, O., Uszkoreit, J.: Scaling autoregressive video models. arXiv preprint arXiv:1906.02634 (2019) 4 

64. Wen, Y., Zhao, Y., Liu, Y., Jia, F., Wang, Y., Luo, C., Zhang, C., Wang, T., Sun, X., Zhang, X.: Panacea: Panoramic and controllable video generation for autonomous driving. arXiv preprint arXiv:2311.16813 (2023) 2, 8, 11, 14 

65. Wu, P., Escontrela, A., Hafner, D., Abbeel, P., Goldberg, K.: Daydreamer: World models for physical robot learning. In: CoRL (2023) 4 

66. Yang, K., Ma, E., Peng, J., Guo, Q., Lin, D., Yu, K.: Bevcontrol: Accurately controlling street-view elements with multi-perspective consistency via bev sketch layout. arXiv preprint arXiv:2308.01661 (2023) 8 

67. Yang, R., Srivastava, P., Mandt, S.: Diffusion probabilistic modeling for video generation. arXiv preprint arXiv:2203.09481 (2022) 4 

68. Zhang, L., Rao, A., Agrawala, M.: Adding conditional control to text-to-image diffusion models. In: ICCV (2023) 7, 10 

69. Zhong, Z., Rempe, D., Chen, Y., Ivanovic, B., Cao, Y., Xu, D., Pavone, M., Ray, B.: Language-guided traffic simulation via scene-level diffusion. arXiv preprint arXiv:2306.06344 (2023) 5, 6 

70. Zhong, Z., Rempe, D., Xu, D., Chen, Y., Veer, S., Che, T., Ray, B., Pavone, M.: Guided conditional diffusion for controllable traffic simulation. In: ICRA (2023) 5, 6 

DriveDreamer-2 19 

In the supplementary material, we begin by detailing the implementation of customized traffic simulation and the Unified Mulit-view Video Model (UniMVM). This is followed by an overview of the training specifics for downstream tasks and evaluation details. Additionally, a collection of visualization results is provided for further analysis. 

## **6 Implement Details** 

**Function Library** Below is an example of a _cut in_ trajectory generation function. Firstly, we initialize a starting point coordinate, and then during the generation of the _cut in_ trajectory, we check the distance between the agent and other agents to control direction and avoid collisions. To enhance the diversity of generated trajectories, we introduce random disturbances to the agent’s speed and orientation, aiming to approximate real-world scenarios as closely as possible. Moreover, this function library can be further expanded to meet users’ demands for generating scenes. More details about the function library can be found in the code that we will release later. 

```
defcut_in(obj_trajs=None ,obj_vels=None ,
safe_dis=10 ,is_ego=False):
’’’
Generateatrajectoryforaagentcuttingin.
Parameters:
Returns:
obj_trajs:thecuttingintrajectoryoftheagent.
obj_vels:thevelocitiesoftheagent.
’’’
agent_trajs=np.zeros ((1,NUM_POINT ,3))
agent_vels=np.zeros ((1,NUM_POINT ,1))
#initializethestartpoint
ifnotis_ego:
xy0=np.random.rand(2)
xy0[0]=utils. get_random_value (xy0[0],[0,10])
multi_factor=1ifrandom.random ()>0.5else-1
xy0[1]=utils. get_random_value (xy0[1],Y_RANGE)\
*multi_factor
y_margin=xy0[1]*multi_factor
agent_trajs[0,0,:2]=xy0
target_y=0
else:
y_margin=abs(obj_trajs[0,0,1])
target_y=obj_trajs[0,0,1]
vel=utils. get_random_value (np.random.rand (),V_RANGE)
agent_vels[0,0]=vel
yaw=utils. get_random_value (np.random.rand (),
FORWARD_RANGE )
vel_x=vel*np.cos(yaw)
```

20 G. Zhao, X. Wang et al. 

```
vel_y=vel*np.sin(yaw)
flag=True
#generatethecutintrajectory
fortinrange(1,NUM_POINT):
agent_trajs[0,t,0]=agent_trajs[0,t-1,0]\
+vel_x*T_INTER
agent_trajs[0,t,1]=agent_trajs[0,t-1,1]\
+vel_y*T_INTER
#checkwhethertheagentreachesthefrontofthe
#targetvehicle
if(agent_trajs[0,t-1,1]-y_margin)*\
(agent_trajs[0,t,1]-y_margin)<=0:
flag=False
#approachthetargetvehicle
ifabs(agent_trajs[0,t,1]-target_y)\
>y_margin/2andflag:
yaw_range=[-0.1,0]ifmulti_factor ==1\
else[0,0.1]
yaw_max=0ifmulti_factor==1else20*np.pi/180
yaw_min=-20*np.pi/180ifmulti_factor==1else0
#graduallyreturntotheforwarddirection.
elifabs(agent_trajs[0,t,1]-target_y)\
>0.5andflag:
yaw_range=[0,0.1]ifmulti_factor==1\
else[-0.1,0]
yaw_max=-10*np.pi/180ifmulti_factor==1\
else20*np.pi/180
yaw_min=-20*np.pi/180ifmulti_factor==1\
else10*np.pi/180
#moveforward
else:
yaw_range=[-0.3*np.pi/180 ,0]ifyaw>=0\
else[0,0.3*np.pi/180]
yaw_max=1*np.pi/180
yaw_min=-1*np.pi/180
#finetunethedirectiontoavoidcollision
ifobj_trajsisnotNone:
yaw_range=utils.update_yaw(yaw ,safe_dis ,
agent_trajs ,
obj_trajs)
yaw+=utils. get_random_value (np.random.rand (),
yaw_range)
yaw=np.clip(yaw ,yaw_min ,yaw_max)
vel+=utils. get_random_value (np.random.rand (),[-2,2]
)
#guarenteethegeneratedvelocitysurpassesthe
#othervehicletorelizecuttingin
ifobj_velsisnotNone:
v_range=[obj_vels[0,t,0]+0.5,V_RANGE[1]+0.5]
else:
```

DriveDreamer-2 

21 

```
v_range=V_RANGE
vel=np.clip(vel ,v_range[0],v_range[1])
agent_vels[0,t]=vel
vel_x=vel*np.cos(yaw)
vel_y=vel*np.sin(yaw)
returnagent_trajs ,agent_vels
```

**Prompt Template** Fig. 9 depicts the general prompt template designed for finetuning LLM. It includes encapsulated trajectory generation functions, and instruction. During usage, the user prompt integrates into the instruction, directly guiding the finetuned LLM to generate the corresponding Python script. 

You are an expert for generate trajectoris for ego car and other agents. Next you will see some Python functions. Given a user prompt, you are asked to use these functions to generate agent tajectories that matches the user prompt. 

There are some of Python functions that you can call for generating trajectories. Note the docstring of the functions to understand what they do. def cut_in(): def pedestrian_crossing(): ''' ''' Generate a trajectory for a agent cutting in. Generate a trajectory of the pedestrian crossing raod. Parameters: Parameters: Returns: Returns: obj_trajs: the cutting in trajectory of the agent. obj_trajs: the unexpected crossing trajectory of the agent. obj_vels: the velocities of the agent. obj_vels: the velocities of the agent. '''... ''' 

Now follow the prompt  {USER QUERY} to write the corresponding the Python script." 

**Fig. 9:** Our prompt template designed for finetuning LLM. It contains information about functions, and instruction. The user query is inserted into the placeholder {USER QUERY}. 

**BEV HDMap Post-Process** Since the generated HDMap is in the BEV perspective, it cannot be directly applied to UniMVM for video generation. Hence, we need post-processing to project the BEV HDMap onto the image coordinate system. Firstly, binarization and skeleton extraction algorithms are employed to extract different types of lane markings (as depicted in Fig. 4 (in the main text), red for lane boundaries, blue for lane dividers, and green for pedestrian crossings). Then, the extracted lane markings are transformed into pixel coordinates to serve as the condition for UniMVM. 

**Training UniMVM** We assume the data distribution is _pdata_ ( _yI_ ), where _yI_ denotes the image latents, and let _p_ ( _y_ ; _σ_ ) be the distribution obtained by adding i.i.d. _σ_<sup>2</sup> -variance Gaussian noise to the data. Note that or sufficiently large _σmax_ , _p_ ( _y_ ; _σmax_ 2) _≈N_ (0 _, σmax_ 2). Diffusion models (DM) [5, 17, 18, 44] use this fact and, starting from high variance Gaussian noise _yM ∼N_ (0 _, σmax_ 2), sequentially denoise towards _σ_ 0 = 0. In practice, this iterative refinement process can be implemented through the numerical simulation of the Probability Flow ordinary differential equation (ODE) [50] 


22 G. Zhao, X. Wang et al. 


**Fig. 10:** Visualization of the generated multi-view video. Regions highlighted by yellow rectangles indicate that _DriveDreamer-2_ exhibits strong temporal consistency. 


**Fig. 11:** A generated video of a rainy day scene. The movement of the windshield wipers (highlighted by yellow rectangles) demonstrates that _as DriveDreamer-2_ possesses a high level of scene understanding. 

where _∇y_ log _p_ ( _y_ ; _σ_ ) is the score function [24]. DM training reduces to learning a model _sθ_ ( _x_ ; _σ_ ) for the score function _∇x_ log _p_ ( _y_ ; _σ_ ). The model can, for example, be parameterized as _∇x_ log _p_ ( _y_ ; _σ_ ) _≈ sθ_ ( _y_ ; _σ_ ) = ( _Dθ_ ( _y_ ; _σ_ ) _− y_ ) _/σ_<sup>2</sup> [27], where _Dθ_ is a learnable denoiser that tries to predict the clean _yI_ . The denoiser _Dθ_ is trained via denoising score matching (DSM) 


where _p_ ( _σ, n_ ) = _p_ ( _σ_ ) _N_ ( _n_ ; 0 _, σ_<sup>2</sup> ), _p_ ( _σ_ ) can be a probability distribution or density over noise levels _σ_ . _λσ_ = (1 + _σ_<sup>2</sup> ) _σ_<sup>_−_2</sup> is a weighting function, and _c_ is the conditional signal, which including the HDMap features _yH_ , box conditions _yB_ and text prompt embeddings _cp_ . In this work, we follow the EDM preconditioning framework [27], parameterizing the learnable denoiser _Dθ_ as 


where _Fθ_ is the network to be trained, and _cskip_ ( _σ_ ) = 1 _/_ ( _σ_<sup>2</sup> + 1) _, cout_ ( _σ_ ) = _−σ/_ _~~√~~ σ_<sup>2</sup> + 1, _cin_ ( _σ_ ) = 1 _/_ _~~√~~ σ_<sup>2</sup> + 1, _cnoise_ ( _σ_ ) = 0 _._ 25 log _σ_ . **Training Downstream Tasks** StreamPETR is retrained at a resolution of 512 _×_ 256 instead of the 704 _×_ 256 in original baseline [57]. The augmented training data is generated by utilizing the structured information from the training set. 


**Fig. 12:** A long video generated by the prompt _a person crosses the road on a rainy day_ . Regions highlighted by yellow rectangles indicate the movement of the pedestrian. **Evaluation Details** The FID and FVD calculations are performed on 150 validation videos from the nuScenes dataset [2]. A setting with a frame rate of 4Hz and 8 frames per clip is employed to generate data for evaluating FID and FVD. And we use the official UCF FVD evaluation code<sup>2</sup> . 

## **7 Visualization** 


**Fig. 13:** A long video generated by the prompt _the ego car changes lane during the daytime_ . 

As shown in Fig. 10, _DriveDreamer-2_ demonstrates strong consistency across views and frames, allowing even the completely occluded car to reappear in subsequent frames (as highlighted by yellow rectangles). The more details can be seen in videos/occluded_car.mp4. Fig. 11 depicts a rainy scene video generated by _DriveDreamer-2_ (see videos/windshield_wiper.mp4 for more details). As illustrated in Fig. 11, the windshield wipers of the truck are continuously clearing 

> 2 `https://github.com/SongweiGe/TATS/` 

24 G. Zhao, X. Wang et al. 

the windshield. This showcases the powerful scene understanding capabilities of our _DriveDreamer-2_ . It can not only manipulate macroscopic weather conditions but also adjust the behaviors of generated agents within the scene according to the weather. 


**Fig. 14:** A long video generated by the prompt _on a rainy day, a car cuts in_ . 

Regarding the generation of long videos, we can utilize _DriveDreamer-2_ without any image conditioning to first generate a clip. Subsequently, the last frame of this clip is employed as the initial image condition to generate subsequent clips. Below, we showcase the results of directly using text prompts to generate a 29-frame multi-view video. Fig. 12 is a long video generated by the prompt _a person crosses the road on a rainy day_ . (see videos/cross_road.mp4 for more details). It depicts a pedestrian crosses the road in front of the ego vehicle on a rainy day. Fig. 13 is generated by a prompt _the ego car changes lane during the daytime_ . (see videos/change_lane.mp4 for more details). It showcases the ego car changes lanes to the right side during the daytime. As shown in Fig. 14, a vehicle cuts in from the left to the front of the ego car (prompted by _on a rainy day, a car cuts in_ and see more details in videos/cut_in.mp4). 

