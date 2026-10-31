---
title: "CoVLA: Comprehensive Vision-Language-Action Dataset for Autonomous Driving"
date: "2024-08-19"
authors: "Hidehisa Arai; Keita Miwa; Kento Sasaki; Yu Yamaguchi; Kohei Watanabe; Shunsuke Aoki"
url: https://arxiv.org/abs/2408.10845
pdf: https://arxiv.org/pdf/2408.10845
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2408.10845)** / [論文ページ](https://arxiv.org/abs/2408.10845)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **CoVLA: Comprehensive Vision-Language-Action Dataset for Autonomous Driving** 

Hidehisa Arai<sup>_∗_</sup> Keita Miwa<sup>_∗_</sup> Kento Sasaki<sup>_∗_</sup> Kohei Watanabe Yu Yamaguchi Shunsuke Aoki Issei Yamamoto Turing Inc. 

https://turingmotors.github.io/covla-ad/ 


Figure 1. **CoVLA framework overview** . We develop **CoVLA-Dataset** , a comprehensive dataset for autonomous driving encompassing unique 10,000 video clips, frame-level language captions describing the driving scenarios, and future trajectory actions. We also show **CoVLA-Agent** , a VLM-based path planning model capable of predicting the future trajectory of the vehicle and providing a textual description of its behavior and reasoning. 

## **Abstract** 

_Autonomous driving, particularly navigating complex and unanticipated scenarios, demands sophisticated reasoning and planning capabilities. While Multi-modal Large Language Models (MLLMs) offer a promising avenue for this, their use has been largely confined to understanding complex environmental contexts or generating high-level driving commands, with few studies extending their application to end-to-end path planning. A major research bottleneck is the lack of large-scale annotated datasets encompassing vision, language, and action. To address this issue, we propose CoVLA (Comprehensive Vision-LanguageAction) Dataset, an extensive dataset comprising realworld driving videos spanning more than 80 hours. This_ 

_dataset leverages a novel, scalable approach based on automated data processing and a caption generation pipeline to generate accurate driving trajectories paired with detailed natural language descriptions of driving environments and maneuvers. This approach utilizes raw in-vehicle sensor data, allowing it to surpass existing datasets in scale and annotation richness. Using CoVLA, we investigate the driving capabilities of MLLMs that can handle vision, language, and action in a variety of driving scenarios. Our results illustrate the strong proficiency of our model in generating coherent language and action outputs, emphasizing the potential of Vision-Language-Action (VLA) models in the field of autonomous driving. This dataset establishes a framework for robust, interpretable, and data-driven autonomous driving systems by providing a comprehensive platform for training and evaluating VLA models, contribut-_ 

> * equal contribution. 

1 

_ing to safer and more reliable self-driving vehicles. The dataset is released for academic purpose._ 

## **1. Introduction** 

A key challenge for autonomous driving technology lies in addressing the “long tail” of diverse and unpredictable driving environments [35, 63]. Self-driving vehicles must navigate not only common scenarios but also rare and complex situations, necessitating diverse world knowledge and advanced reasoning capabilities [20]. This demands a deep understanding of the environment and a capacity for reasoning that extends beyond recognizing objects to interpreting their behavior and planning actions accordingly. VisionLanguage-Action (VLA) models, by seamlessly integrating visual perception with language understanding and action planning, have emerged as a promising pathway towards this goal. Recent advancements in VLA, particularly in robotics [4, 28, 40] and autonomous driving [45], demonstrate their potential for enabling more robust and intelligent driving systems. 

However, a major obstacle in applying VLA models to autonomous driving is the lack of large-scale datasets that effectively combine visual data with language descriptions and driving actions. Existing datasets often fall short in terms of scale and comprehensive annotation, especially for language, which often requires laborious manual effort. This limits the development and evaluation of robust VLA models capable of handling the complexities of real-world driving. 

This paper introduces CoVLA ( **Co** mprehensive **V** ision- **L** anguage- **A** ction) Dataset, a novel large-scale dataset designed to overcome these limitations. CoVLA-Dataset utilizes scalable automated approaches for labeling and captioning, creating a rich dataset of 10,000 real-world driving scenes, totaling more than 80 hours of videos. Each 30second scene contains accurate driving paths and detailed descriptions in natural language, derived from synchronized front-facing camera footage and data from in-vehicle sensors. This rich dataset allows for a deeper understanding of the driving environment and agent behavior. To demonstrate its effectiveness in advancing autonomous driving research, we develop CoVLA-Agent, a VLA model trained on our dataset for trajectory prediction and traffic scene description generation. Our findings indicate that our VLA model is capable of making consistent and precise predictions, even in situations that demand complex and advanced judgements. The main contributions of this paper are summarized as follows: 

- We introduce CoVLA Dataset, a large-scale dataset that provides trajectory targets for diverse driving scenarios, as well as detailed frame-by-frame situational 

descriptions. 

- We present a scalable method that accurately estimates trajectories through sensor fusion and automatically generates frame-level text captions of critical driving information. 

- We develop CoVLA-Agent, a novel VLA model for interpretable end-to-end autonomous driving on top of CoVLA Dataset. Our model demonstrate the capability to consistently generate driving scene descriptions and predict trajectories, paving the way for more reliable autonomous driving. 

## **2. Related Works** 

### **2.1. Datasets for Autonomous Driving** 

Research in autonomous driving has been deeply connected with the development of large-scale datasets [29,34]. The evolution of these datasets has seen a clear trend toward incorporating richer sensors and modalities, moving from a focus on individual tasks like object recognition to more complex challenges such as scene understanding, motion prediction, and end-to-end driving. Early efforts primarily focused on the recognition of traffic environments, proposing datasets for tasks such as pedestrian recognition [14, 18, 39, 62], traffic light and sign recognition [3, 15, 19, 22, 41, 50, 61, 64], and driving scene segmentation [5, 13, 38, 46, 60]. 

The increasing complexity of autonomous driving tasks led to the development of large-scale datasets that incorporate data from various sensors. KITTI [21] is the pioneering work, which provides driving footage recorded from frontfacing cameras and LiDAR. It also includes 3D bounding box annotations and ground truth trajectories. Waymo Open Dataset [51], while employing a similar approach, has significantly enhanced both scale and diversity. Argoverse 1 [9], Argoverse 2 [55], and nuScenes [7] provide HighDefinition Maps (HD-Maps) along with multi-sensor information and 3D bounding box annotations to make them more suitable for motion prediction tasks. Lyft L5 [23] and nuPlan [8], which also include HD-Maps, are more focused on planning tasks. These rich, multi-modal datasets have significantly advanced research in areas such as 3D object detection, trajectory prediction, and behavior planning, enabling the development of algorithms capable of handling more complex and realistic driving scenarios. 

In recent years, the development of Large Language Models (LLMs) has given rise to attempts to employ Multimodal LLMs (MLLMs) for complex driving environment understanding and driving operation planning. This has led to the emergence of Vision-Language datasets specifically tailored to traffic environments. BDD-X [27] provides manually annotated free-form captions that describe the reasons 

2 

|**Dataset**|**Year**|**Vis**|**ion Data**|**La**|**nguage Da**|**ta**|**Action**|**Data**|
|---|---|---|---|---|---|---|---|---|
|||**Frames**|**Source**|**Type**|**Method**|**Count**|**Type**|**Method**|
|BDD-X[27]|2018|26.2K|BDD[59]|Caption|Manual|26K|—|—|
|BDD-OIA[56]|2020|22.9K|BDD[59]|Caption|Manual|27K|Command|Manual|
|DRAMA [36]|2023|17.8K|Original<br>(Real)|Caption|Manual|17K|Command|Manual|
|OpenDV-2K [58]|2024|65.1M|YouTube<br>Public Datasets|Caption|Auto<br>(Single)|65.1M|Command|Auto|
|HAD[26]|2019|1.1M|HDD[44]|Caption|Manual|47K|Traj,Command|Base|
|Talk2Car[17]|2019|400K|nuScenes[6]|Caption|Manual|12K|Traj|Base|
|Talk2Car-Trajectory [16]|2022|400K|nuScenes[6]|Caption|Manual|12K|Traj,Command|Base,Manual|
|DriveLM-nuScenes[49]|2023|4.8K|nuScenes[6]|QA|Manual|445K|Traj|Base|
|DriveLM-CARLA [49]|2023|183K|Original<br>(Sim)|QA|Auto<br>(Single)|3.76M|Traj|Sim|
|**CoVLA (ours)**|2024|6M|Original<br>(Real)|Caption|Auto<br>(Multi)|6M|Traj|GPS/IMU|


Table 1. **Comparison of driving datasets with language and action data** . 

behind the ego vehicle actions in driving videos. In BDDOIA [56] dataset, closed-form explanations about objects that trigger responses from the ego vehicle are provided, along with recommended actions. Similarly, DRAMA [36] provides closed-form and free-form captions aimed at identifying risks during driving. It also includes annotations of objects related to risk events and recommended action commands. OpenDV-2K [58] is a large-scale dataset derived from publicly available videos, annotated with automatically generated text captions and driving action commands. However, these datasets provide only high-level driving commands (e.g., “stop” and “turn left”) as actions and often lack fine-grained trajectory information, which is essential for representing detailed driving maneuvers and training end-to-end autonomous driving systems. HAD [26], Talk2Car [17], Talk2Car-Trajectory [16], and DriveLM [49] are Vision-Language datasets that include trajectory information as finer-grained action annotations. However, these datasets are often limited in scale, particularly in terms of the diversity and complexity of the driving scenarios they cover, hindering their ability to support the development of truly robust and generalizable VLA models. 

ADAPT [24] utilizes Vision-Language Models (VLMs) to generate natural language explanations of driving actions and provide reasoning behind them, enhancing the interpretability of the system. Early attempts to predict driving actions using language models involved employing GPT3.5 and GPT-4 [1] to predict high-level driving commands from situational descriptions [20, 54]. These initial efforts set the stage for more recent studies, which have explored fine-tuning LLMs to predict various types of driving behavior like trajectories [49, 57] or control signals such as steering and acceleration [10, 37, 47] through textual outputs. While these approaches handle driving maneuver directly through language, LMDrive [48] and DriveMLM [53] predict control signals by passing the embeddings from the Transformer outputs to decoders. CarLLaVA [45] uses the LLaVA architecture to predict trajectories by taking images, vehicle speed, and target location coordinates as inputs. Notably, this approach has achieved significantly superior performance compared to existing methods on the CARLA leaderboard 2.0, demonstrating the effectiveness of VLMs for complex trajectory prediction tasks. 

## **3. Dataset** 

### **2.2. MLLMs for Driving Tasks** 

Addressing the complex and often unpredictable nature of real-world driving scenarios, particularly those falling within the “long tail” of the driving distribution (e.g., navigating road closures), necessitates a higher level of reasoning and decision-making capabilities in autonomous systems. Recent research has increasingly focused on incorporating MLLMs into autonomous driving systems, aiming to leverage their powerful reasoning and language understanding capabilities to address these challenges. For instance, 

This section provides an in-depth look at CoVLADataset, detailing its structure, content, and the methods employed to create this valuable resource for autonomous driving research. We highlight its coverage of diverse realworld driving scenarios, synchronized multi-modal data streams (front-facing camera, in-vehicle signals and other sensors) and its large-scale annotated data: 10,000 driving scenes totaling over 80 hours of video, each with accurate frame-level trajectory and descriptive caption annotations. To create this extensive VLA dataset, we develop a novel 

3 

and scalable approach for automatically generating scene descriptions and ground truth trajectories from raw data. 

### **3.1. Development** 

#### **3.1.1 Raw Data** 

We develop multiple data collection vehicles to acquire realworld driving data, including sensor data from the frontfacing camera, Controller Area Network (CAN) bus, Global Navigation Satellite System (GNSS), and Inertial Measurement Unit (IMU) and deploy them around Tokyo, Japan. 

- **Data collection period:** 6 months (summer to winter), resulting in over 1000 hours of raw data. 

- **Data collection environments:** Various locations in and around Tokyo (urban centers, complex highway interchanges, narrow residential streets, mountainous areas with winding roads), different weather conditions (sunny, cloudy, rainy, heavy rain), and various times of day (daytime, evening, nighttime). 

- **Equipment:** Front-facing camera (1928 _×_ 1208 pixels, 20 FPS, H.265 codec), CAN bus (accelerator/brake pedal position, steering wheel angle, turn signal status, gear position, vehicle speed), GNSS and IMU (binary format with timestamps), in-vehicle storage devices. 


Figure 2. **Overview of the dataset generation pipeline** . We automatically label video frames and sensor signals to generate trajectories and other labels. Furthermore, we apply auto-captioning to the video frames to produce both behavior and reasoning captions. 

#### **3.1.2 Data Sampling** 

From over 1,000 hours of raw driving data, we carefully select several hundred hours that meet the following criteria: (1) recorded while the vehicle is in driving gear, (2) the maximum speed does not exceed 100 km/h, and (3) GNSS data is continuously available. 

To emphasize the diversity of driving scenarios, we sample individual data points with weighting inversely proportional to the pre-computed empirical distribution of a given set of features. Specifically, we select the maximum absolute value of steering angle, the maximum absolute value of acceleration, and turn signal as the features to balance over, applying binning for the first two. We calculate the empirical joint distribution of these categorical features. After applying additive smoothing [11] with a smoothing parameter of _δ_ = 50, we use the inverse of these values as probability weights during sampling. Based on these adjustments, we select 10,000 diverse 30-second scenes through this method, resulting in a total of 6,000,000 video frames, equivalent to 83.3 hours of driving data. 

#### **3.1.3 Auto Labeling** 

**Trajectory** To acquire future trajectory data, which will be predicted by the VLA models, we estimate the vehicle’s travel path with a Kalman Filter [25] using GNSS and IMU 

sensors. For each timestamp, we annotate future trajectory data points for the subsequent three seconds (60 frames). The trajectory data is expressed in the global coordinate system centered on the data collection vehicle. In some instances, GNSS data instability occasionally leads to erroneous trajectories characterized by significant vibrations. We implement a heuristic approach to identify and remove these inaccurate trajectories from the dataset. Further details are reported in the supplementary material. 

**Objects** Traffic lights are among the most critical objects in the driving environment, and accurate detection of their state provides strong support for the training of VLA models. We employ a deep learning model specifically designed for traffic light detection (OpenLenda-s<sup>1</sup> ) to annotate our data. This model can accurately identify not only the color of traffic lights but also the direction of arrow signals, providing a comprehensive understanding of traffic light information for each frame. 

In addition, accurate detection and tracking of leading vehicles are crucial for understanding traffic flow and predicting potential hazards, making it another vital element of 

> 1https : / / github . com / turingmotors / openlenda / releases/tag/v0.1.0 

4 


Figure 3. **Frame examples from CoVLA-Dataset** . Estimated trajectories ( **green line** ) and captions generated by the captioner model are shown. The **key objects** are highlighted in blue bold text, while the **failures** in captions are shown in red bold text. 

our dataset. To ensure robustness, we employ a sensor fusion approach, combining data from both radar and a frontfacing camera. Our dataset includes comprehensive information for the detected leading vehicle, including its speed, acceleration, and position relative to the ego vehicle. 

#### **3.1.4 Auto Captioning** 

**Rule-based Captioning** Captions are essential for visionlanguage-action datasets, but manual annotation presents significant challenges. Human annotation is costly, timeconsuming, and often suffers from inconsistencies in caption quality. To address these limitations and ensure scalability, we develop an automated captioning approach. 

Rule-based captions in natural language are generated as the first step of our approach. We consider various aspects of vehicle motion and detected objects, including speed, acceleration, trajectory curvature, leading vehicle presence, and traffic light status, to generate comprehensive rulebased captions for each frame in the dataset. 

**VLM-based Captioning** While efficient and costeffective, rule-based captioning often lacks the richness of natural language and may overlook critical details such as specific signs or uncommon objects. To enhance the 

expressiveness and informativeness of captions, we employ a pretrained VLM to augment the rule-based captions. While some datasets, such as OpenDV-2K [58], utilize single-frame auto captioning with models like BLIP-2 [30], this approach fails to capture crucial temporal information inherent in driving scenarios. To address this limitation, we employ a pretrained VideoLLaMA 2<sup>2</sup> , a large video language model proficient in spatiotemporal modeling and demonstrating strong performance in video question answering and captioning tasks [12]. 

The captioner model operates on a 60-frame (threesecond) window, processing eight representative frames, including the first and last frames of the window, sampled from the input video. To manage the processing load, each 30-second scene is divided into ten windows. This approach results in 100,000 VLM-generated captions and 6,000,000 combined captions after integrating both rulebased and VLM-generated captions. Caption generation is performed using eight NVIDIA H100 GPUs, with the entire process completes within a single day, demonstrating significant time savings compared to manual annotation. 

> 2https : / / huggingface . co / DAMO - NLP - SG / VideoLLaMA2-7B 

5 

**Hallucination Mitigation** A known challenge with VLMs is their tendency to generate hallucinations, producing captions that do not accurately reflect the visual content, particularly in tasks like visual question answering and image captioning [2, 33]. To mitigate this issue, we use comprehensive rule-based captions as factual constraints. These captions are then provided as context to the VLM, along with a prompt instructing it to supplement the captions with any additional information not already covered by the rules. This supplementary information, derived by querying the model and examining its internal token probability distributions, includes details regarding road type (e.g., narrow/wide, highway/non-highway, tunnel/non-tunnel), weather conditions (e.g., sunny, cloudy, rainy), potential risks (e.g., pedestrian presence), and other relevant factors. For instance, to determine the weather, we calculate the probability of each weather-related token (e.g., “sunny,” “cloudy,” or “rainy”) given the query “What is the weather in this video?” and select the token with the highest probability. Using these augmented rule-based captions as factual anchors, we prompt the VLM to generate free-form captions, focusing on identifying potential risks within the driving environment. 

### **3.2. Analysis** 

**Statistics** To assess the impact of our scene sampling methodology described in Section 3.1.2, we first analyze the distribution of key driving parameters. As shown in Figure 4a and Figure 4b, the distributions of vehicle speeds and steering angles become more uniform after sampling, with a noticeable increase in lower speed data points and a diminished central peak around zero degrees for steering angles, leading to a more balanced representation across different ranges. Consequently, CoVLA-Dataset exhibits diverse driving maneuvers, with active turn signals in 16.11% of frames and traffic lights in 22.90%. This diversity, including starting/stopping, turning, and lane changing, emphasizes the need for robust perception, decision-making, and control algorithms in autonomous driving systems. 

**Comparison** As presented in Table 1, our CoVLADataset demonstrates several key advantages. We construct our dataset using auto labeling and MLLMs-based auto captioning similar to OpenDV-2K [58]. This automated approach is crucial for constructing large-scale datasets, a growing trend in autonomous driving research [31], and enables us to develop a dataset significantly larger than those reliant on manual annotation. Furthermore, our dataset incorporates trajectory annotations, a feature absent in datasets lacking sufficient metadata like OpenDV-2K, derived from GPS and IMU data. 

CoVLA-Dataset distinguishes itself from other datasets through its seamless integration of vision, language, and ac- 


Figure 4. **Data distribution of vehicle speed and steering angle** . The red bars represent the distribution before sampling, while the yellow bars show the distribution after sampling. Note that a logarithmic scale is used for clarity in (b). 

tion modalities. This integration results from synchronized real-world data acquisition from various sensors, coupled with our automated labeling and captioning pipeline. This comprehensive annotation captures all relevant aspects of the driving environment, making it a valuable resource for training and evaluating autonomous driving systems. 

**Limitation of Auto Captioning** Figure 3 presents frames sampled from CoVLA-Dataset, highlighting both successful examples and instances where auto-captioning encountered challenges. While our proposed method effectively enables scalable and detailed video captioning, analysis of the generated captions reveals areas for further refinement. We identify two primary categories of errors. Firstly, the captioning model occasionally exhibits object hallucination, describing objects absent from the scene, such as a “wooden fence.” Furthermore, the VLM occasionally misidentifies object locations and scene elements, such as incorrectly labeling left-side objects as “right-side.” 

Another limitation we reveal is the recognition of local landmarks, particularly those unique to Japan. For instance, Japanese traffic signs often have unique designs and meanings, such as including Japanese characters, that necessitate proper identification and interpretation. 

These findings highlight key areas for future research, including the development of more robust object detection algorithms, context-aware captioning models with more knowledge of the driving environment, and culturally diverse training datasets. 

6 

## **4. Experiment** 

In this section, we present the development and evaluation methodology of our baseline model, CoVLA-Agent, which leverages the richness of CoVLA-Dataset for autonomous driving tasks. We detail the experimental setup, including dataset, model configurations, training procedures, and evaluation metrics, and analyze the results. 

### **4.1. Model** 

**Architecture** CoVLA-Agent as illustrated in Figure 5, is a VLA model designed for autonomous driving. We utilize the pretrained Llama-2 (7B) [52] as a language model and CLIP ViT-L (224 _×_ 224 pixels) [43] as a vision encoder. In addition, our model takes the ego vehicle’s speed as an input, which is transformed into an embedding vector using a Multi Layer Perceptron (MLP). The visual features extracted by CLIP ViT-L are concatenated with the speed embedding and text embedding, and then fed into the Llama-2 model. For trajectory prediction, special tokens are used as trajectory queries. The outputs of these trajectory queries are processed by an MLP layer, resulting in a sequence of 10 ( _x, y, z_ ) coordinates representing the predicted trajectory of the vehicle relative to its current position, spanning a three-second time horizon. 

**Training** Based on this architecture, we train CoVLAAgent on two tasks, which are traffic scene description generation and trajectory prediction. For traffic scene description generation, we use cross entropy loss as the loss function, and for trajectory prediction, we employ mean squared error loss. Ultimately, the training aims to minimize a combined loss function where both losses are weighted equally. 


Figure 5. **The architecture for CoVLA-Agent** . 

### **4.2. Experimental Settings** 

**Data** CoVLA-Agent is trained on CoVLA-Dataset. We split the 10,000 scenes in the dataset into a 70/15/15 for training, validation, and testing, respectively. For each scene, we sample frames at a frequency of 2Hz, excluding any frames that do not contain all trajectory coordinate points for the subsequent three seconds (60 coordinate points in total). From these 60 coordinate points, we uniformly sample 10 points to represent the future trajectory. This process yields a data subset comprising 302,989 samples for training, 64,153 samples for validation, and 64,920 samples for testing. We preprocess the training and validation datasets into the LLaVA instruction tuning format [32] for efficient model training. This format, illustrated in Figure 5, consists of a system prompt, a user instruction, and an assistant response. 

**Conditions** To examine the impact of the captioning task on subsequent trajectory prediction, we prepare two conditions: the _predicted caption_ condition, where CoVLAAgent generates captions prior to predict trajectory, and the _ground truth caption_ condition, where actual captions are used instead of predicted ones during trajectory prediction. 

**Metrics** We compute both Average Displacement Error (ADE) and Final Displacement Error (FDE) to assess the trajectory prediction accuracy [42]. ADE is computed as the mean Euclidean distance between the predicted trajectory points and the ground truth trajectory points over all time steps. FDE measures the Euclidean distance between the predicted final point and the ground truth final point. 


### **4.3. Results** 

We present qualitative results in Table 2. The ground truth captions achieve a lower ADE (0.814) and FDE (1.655) compared to the predicted captions’ ADE (0.955) and FDE (2.239). The results indicate that CoVLA-Agent performs better when using ground truth captions compared to predicted captions. 

|**Condition**|**Met**|**rics**|
|---|---|---|
||**ADE**_↓_|**FDE**_↓_|
|predicted caption|0.955|2.239|
|ground truth caption|**0.814**|**1.655**|


Table 2. **Quantitative comparison of different conditions** . 

7 

### **4.4. Discussion** 

We analyze our model’s performance across various driving scenarios. 

Figure 6a demonstrates accurate trajectory prediction on a straight road, while Figure 6b showcases successful freeway merging. Figure 6c illustrates a scene where the ego vehicle is in the right lane due to traffic control. A traffic officer stops a red car ahead in the right lane. To avoid them, our model predicts a trajectory that returns to the left lane. Our approach is capable of producing accurate routes even in such complex traffic control scene. 

Figure 6d shows the results of trajectory prediction at an intersection. In this scene, the ground truth caption includes the phrase “ _moving straight_ ” and the trajectory predicted with that condition is straight. In contrast, the predicted trajectory based on the predicted caption including phrase “ _turning right_ ,” accurately reflects a right-turn trajectory. While this result indicates the difficulty of estimating intention from a single frame in such scenes, it also underscores the consistency between language and action modality in CoVLA-Agent. 

To examine the impact of these captioning errors on trajectory, we investigate how errors in predicted captions affect ADE and FDE. Specifically, we analyze the mean ADE and FDE values for each word in the captions when the word appears in the ground truth rule-based caption part but not in the predicted caption, and vice versa. Excluding stop 


Figure 6. **Results of trajectory prediction by CoVLA-Agent across various traffic scenes** . **Red line** is the predicted trajectory with predicted caption condition, **blue line** is the trajectory predicted with ground truth caption condition and **green line** is the ground truth trajectory. 

words, the top ten words with frequencies exceeding ten that led to the largest ADE and FDE values are shown in Table 3, though their rankings vary between the two metrics. Large ADE and FDE occur when there are discrepancies in the predicted caption, particularly with words related to vehicle motion direction and acceleration, such as “deceleration,” “left,” “curve,” and “turning.” Based on these observations, we attribute the relatively low performance in the trajectory predicted using the generated caption largely to the difficulty of estimating intention from a single frame. 

|**Word**|**Mean ADE** _↓_|**Mean FDE** _↓_|**Frequency**|
|---|---|---|---|
|**deceleration**|2.236|5.458|324|
|**left**|2.037|5.009|274|
|**acceleration**|1.826|4.790|50|
|**curve**|1.527|3.608|167|
|following|1.400|3.192|20|
|**turning**|1.343|3.288|636|
|**right**|1.324|3.282|810|
|appear|1.244|3.044|93|
|present|1.244|3.044|93|
|signal|1.229|3.049|117|


Table 3. **Top-10 words with the largest mean ADE and FDE** . These words correspond to motions that are difficult to estimate from a single frame. Words explicitly signifying motion are presented in bold. 

These behaviors demonstrate that our CoVLA-Dataset led the model to generate consistent captions and trajectories, showing an outstanding capability to handle a variety of driving scenes and is useful for training autonomous driving models to manage complex scenarios. CoVLA-Dataset accelerates future research on the application of VLA models for self-driving vehicles. 

## **5. Conclusion** 

In this study, we presented CoVLA-Dataset, a novel dataset for autonomous driving with VLA models. By leveraging scalable automated approach, we have constructed a large-scale, comprehensive dataset enriched with detailed language annotations. Building on this robust dataset, we developed CoVLA-Agent, a sophisticated VLA autonomous driving model. The evaluation results underscore the strong capability of the model which generates coherent language and action outputs. These findings highlight the transformative potential of VLA multi-modal models and pave the way for future innovations in autonomous driving research. 

## **Acknowledgments** 

This paper is based on results obtained from a project, JPNP20017, subsidized by the New Energy and Industrial Technology Development Organization (NEDO). 

8 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 3 

- [2] Zechen Bai, Pichao Wang, Tianjun Xiao, Tong He, Zongbo Han, Zheng Zhang, and Mike Zheng Shou. Hallucination of multimodal large language models: A survey. _arXiv preprint arXiv:2404.18930_ , 2024. 6 

- [3] Karsten Behrendt, Libor Novak, and Rami Botros. A deep learning approach to traffic lights: Detection, tracking, and classification. In _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 1370–1377. IEEE, 2017. 2 

- [4] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alex Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _arXiv preprint arXiv:2307.15818_ , 2023. 2 

- [5] Gabriel J Brostow, Jamie Shotton, Julien Fauqueur, and Roberto Cipolla. Segmentation and recognition using structure from motion point clouds. In _Computer Vision–ECCV 2008: 10th European Conference on Computer Vision, Marseille, France, October 12-18, 2008, Proceedings, Part I 10_ , pages 44–57. Springer, 2008. 2 

- [6] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 3 

- [7] Holger Caesar, Varun Bankiti, Alex H Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11621–11631, 2020. 2 

- [8] Holger Caesar, Juraj Kabzan, Kok Seang Tan, Whye Kit Fong, Eric Wolff, Alex Lang, Luke Fletcher, Oscar Beijbom, and Sammy Omari. nuplan: A closed-loop ml-based planning benchmark for autonomous vehicles. _arXiv preprint arXiv:2106.11810_ , 2021. 2 

- [9] Ming-Fang Chang, John Lambert, Patsorn Sangkloy, Jagjeet Singh, Slawomir Bak, Andrew Hartnett, De Wang, Peter 

Carr, Simon Lucey, Deva Ramanan, et al. Argoverse: 3d tracking and forecasting with rich maps. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 8748–8757, 2019. 2 

- [10] Long Chen, Oleg Sinavski, Jan H¨unermann, Alice Karnsund, Andrew James Willmott, Danny Birch, Daniel Maund, and Jamie Shotton. Driving with llms: Fusing object-level vector modality for explainable autonomous driving. _arXiv preprint arXiv:2310.01957_ , 2023. 3 

- [11] Stanley F Chen and Joshua Goodman. An empirical study of smoothing techniques for language modeling. _Computer Speech & Language_ , 13(4):359–394, 1999. 4 

- [12] Zesen Cheng, Sicong Leng, Hang Zhang, Yifei Xin, Xin Li, Guanzheng Chen, Yongxin Zhu, Wenqi Zhang, Ziyang Luo, Deli Zhao, et al. Videollama 2: Advancing spatialtemporal modeling and audio understanding in video-llms. _arXiv preprint arXiv:2406.07476_ , 2024. 5 

- [13] Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler, Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele. The cityscapes dataset for semantic urban scene understanding. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 3213–3223, 2016. 2 

- [14] Navneet Dalal and Bill Triggs. Histograms of oriented gradients for human detection. In _2005 IEEE computer society conference on computer vision and pattern recognition (CVPR’05)_ , volume 1, pages 886–893. Ieee, 2005. 2 

- [15] Raoul De Charette and Fawzi Nashashibi. Real time visual traffic lights recognition based on spot light detection and adaptive traffic lights templates. In _2009 IEEE Intelligent Vehicles Symposium_ , pages 358–363. IEEE, 2009. 2 

- [16] Thierry Deruyttere, Dusan Grujicic, Matthew B Blaschko, and Marie-Francine Moens. Talk2car: Predicting physical trajectories for natural language commands. _Ieee Access_ , 10:123809–123834, 2022. 3 

- [17] Thierry Deruyttere, Simon Vandenhende, Dusan Grujicic, Luc Van Gool, and Marie-Francine Moens. Talk2Car: Taking control of your self-driving car. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan, editors, _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_ , pages 2088–2098, Hong Kong, China, Nov. 2019. Association for Computational Linguistics. 3 

- [18] Piotr Dollar, Christian Wojek, Bernt Schiele, and Pietro Perona. Pedestrian detection: An evaluation of the state of the art. _IEEE transactions on pattern analysis and machine intelligence_ , 34(4):743–761, 2011. 2 

- [19] Andreas Fregin, Julian Muller, Ulrich Krebel, and Klaus Dietmayer. The driveu traffic light dataset: Introduction and comparison with existing datasets. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 3376–3383. IEEE, 2018. 2 

- [20] Daocheng Fu, Xin Li, Licheng Wen, Min Dou, Pinlong Cai, Botian Shi, and Yu Qiao. Drive like a human: Rethinking autonomous driving with large language models. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pages 910–919, 2024. 2, 3 

9 

- [21] Andreas Geiger, Philip Lenz, and Raquel Urtasun. Are we ready for autonomous driving? the kitti vision benchmark suite. In _2012 IEEE conference on computer vision and pattern recognition_ , pages 3354–3361. IEEE, 2012. 2 

- [22] Sebastian Houben, Johannes Stallkamp, Jan Salmen, Marc Schlipsing, and Christian Igel. Detection of traffic signs in real-world images: The german traffic sign detection benchmark. In _The 2013 international joint conference on neural networks (IJCNN)_ , pages 1–8. Ieee, 2013. 2 

- [23] John Houston, Guido Zuidhof, Luca Bergamini, Yawei Ye, Long Chen, Ashesh Jain, Sammy Omari, Vladimir Iglovikov, and Peter Ondruska. One thousand and one hours: Self-driving motion prediction dataset. In _Conference on Robot Learning_ , pages 409–418. PMLR, 2021. 2 

- [24] Bu Jin, Xinyu Liu, Yupeng Zheng, Pengfei Li, Hao Zhao, Tong Zhang, Yuhang Zheng, Guyue Zhou, and Jingjing Liu. Adapt: Action-aware driving caption transformer. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7554–7561. IEEE, 2023. 3 

- [25] Rudolph Emil Kalman. A new approach to linear filtering and prediction problems. 1960. 4 

- [26] Jinkyu Kim, Teruhisa Misu, Yi-Ting Chen, Ashish Tawari, and John Canny. Grounding human-to-vehicle advice for self-driving vehicles. In _The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 3 

- [27] Jinkyu Kim, Anna Rohrbach, Trevor Darrell, John Canny, and Zeynep Akata. Textual explanations for self-driving vehicles. _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2018. 2, 3 

- [28] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2 

- [29] Hongyang Li, Yang Li, Huijie Wang, Jia Zeng, Huilin Xu, Pinlong Cai, Li Chen, Junchi Yan, Feng Xu, Lu Xiong, Jingdong Wang, Futang Zhu, Chunjing Xu, Tiancai Wang, Fei Xia, Beipeng Mu, Zhihui Peng, Dahua Lin, and Yu Qiao. Open-sourced data ecosystem in autonomous driving: the present and future. _SCIENTIA SINICA Informationis_ , 2024. 2 

- [30] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. BLIP-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors, _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pages 19730–19742. PMLR, 23–29 Jul 2023. 5 

- [31] Lincan Li, Wei Shao, Wei Dong, Yijun Tian, Kaixiang Yang, and Wenjie Zhang. Data-centric evolution in autonomous driving: A comprehensive survey of big data system, data mining, and closed-loop technologies. _arXiv preprint arXiv:2401.12888_ , 2024. 6 

- [32] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, _Advances in Neural Information Processing Systems_ , volume 36, pages 34892–34916. Curran Associates, Inc., 2023. 7 

- [33] Hanchao Liu, Wenyuan Xue, Yifei Chen, Dapeng Chen, Xiutian Zhao, Ke Wang, Liping Hou, Rongjun Li, and Wei Peng. A survey on hallucination in large vision-language models, 2024. 6 

- [34] Mingyu Liu, Ekim Yurtsever, Jonathan Fossaert, Xingcheng Zhou, Walter Zimmer, Yuning Cui, Bare Luka Zagar, and Alois C Knoll. A survey on autonomous driving datasets: Statistics, annotation quality, and a future outlook. _IEEE Transactions on Intelligent Vehicles_ , 2024. 2 

- [35] Osama Makansi, ¨Ozg¨un Cicek, Yassine Marrakchi, and Thomas Brox. On exposing the challenging long tail in future prediction of traffic actors. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 13147–13157, 2021. 2 

- [36] Srikanth Malla, Chiho Choi, Isht Dwivedi, Joon Hee Choi, and Jiachen Li. Drama: Joint risk localization and captioning in driving. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)_ , pages 1043–1052, January 2023. 3 

- [37] Jiageng Mao, Yuxi Qian, Hang Zhao, and Yue Wang. Gpt-driver: Learning to drive with gpt. _arXiv preprint arXiv:2310.01415_ , 2023. 3 

- [38] Gerhard Neuhold, Tobias Ollmann, Samuel Rota Bulo, and Peter Kontschieder. The mapillary vistas dataset for semantic understanding of street scenes. In _Proceedings of the IEEE international conference on computer vision_ , pages 4990– 4999, 2017. 2 

- [39] Luk´aˇs Neumann, Michelle Karg, Shanshan Zhang, Christian Scharfenberger, Eric Piegert, Sarah Mistr, Olga Prokofyeva, Robert Thiel, Andrea Vedaldi, Andrew Zisserman, et al. Nightowls: A pedestrians at night dataset. In _Computer Vision–ACCV 2018: 14th Asian Conference on Computer Vision, Perth, Australia, December 2–6, 2018, Revised Selected Papers, Part I 14_ , pages 691–705. Springer, 2019. 2 

- [40] Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, Anthony Brohan, et al. Open x- embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 2 

- [41] Mark Philip Philipsen, Morten Bornø Jensen, Andreas Møgelmose, Thomas B Moeslund, and Mohan M Trivedi. Traffic light detection: A learning algorithm and evaluations on challenging dataset. In _2015 IEEE 18th International Conference on Intelligent Transportation Systems_ , pages 2341–2345. IEEE, 2015. 2 

- [42] Tran Phong, Haoran Wu, Cunjun Yu, Panpan Cai, Sifa Zheng, and David Hsu. What truly matters in trajectory prediction for autonomous driving? _Advances in Neural Information Processing Systems_ , 36, 2024. 7 

- [43] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen 

10 

Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. In Marina Meila and Tong Zhang, editors, _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , pages 8748–8763. PMLR, 18–24 Jul 2021. 7 

- [44] Vasili Ramanishka, Yi-Ting Chen, Teruhisa Misu, and Kate Saenko. Toward driving scene understanding: A dataset for learning driver behavior and causal reasoning. In _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2018. 3 

- [45] Katrin Renz, Long Chen, Ana-Maria Marcu, Jan H¨unermann, Benoit Hanotte, Alice Karnsund, Jamie Shotton, Elahe Arani, and Oleg Sinavski. Carllava: Vision language models for camera-only closed-loop driving. _arXiv preprint arXiv:2406.10165_ , 2024. 2, 3 

- [46] Timo Scharw¨achter, Markus Enzweiler, Uwe Franke, and Stefan Roth. Efficient multi-cue scene segmentation. In _German Conference on Pattern Recognition_ , pages 435–445. Springer, 2013. 2 

- [47] Hao Sha, Yao Mu, Yuxuan Jiang, Li Chen, Chenfeng Xu, Ping Luo, Shengbo Eben Li, Masayoshi Tomizuka, Wei Zhan, and Mingyu Ding. Languagempc: Large language models as decision makers for autonomous driving. _arXiv preprint arXiv:2310.03026_ , 2023. 3 

- [48] Hao Shao, Yuxuan Hu, Letian Wang, Guanglu Song, Steven L Waslander, Yu Liu, and Hongsheng Li. Lmdrive: Closed-loop end-to-end driving with large language models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15120–15130, 2024. 3 

- [49] Chonghao Sima, Katrin Renz, Kashyap Chitta, Li Chen, Hanxue Zhang, Chengen Xie, Ping Luo, Andreas Geiger, and Hongyang Li. Drivelm: Driving with graph visual question answering. _arXiv preprint arXiv:2312.14150_ , 2023. 3 

- [50] Johannes Stallkamp, Marc Schlipsing, Jan Salmen, and Christian Igel. Man vs. computer: Benchmarking machine learning algorithms for traffic sign recognition. _Neural networks_ , 32:323–332, 2012. 2 

- [51] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, et al. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2446–2454, 2020. 2 

- [52] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 7 

- [53] Wenhai Wang, Jiangwei Xie, ChuanYang Hu, Haoming Zou, Jianan Fan, Wenwen Tong, Yang Wen, Silei Wu, Hanming Deng, Zhiqi Li, et al. Drivemlm: Aligning multi-modal large language models with behavioral planning states for autonomous driving. _arXiv preprint arXiv:2312.09245_ , 2023. 3 

- [54] Licheng Wen, Daocheng Fu, Xin Li, Xinyu Cai, Tao MA, Pinlong Cai, Min Dou, Botian Shi, Liang He, and Yu Qiao. 

Dilu: A knowledge-driven approach to autonomous driving with large language models. In _The Twelfth International Conference on Learning Representations_ , 2024. 3 

- [55] Benjamin Wilson, William Qi, Tanmay Agarwal, John Lambert, Jagjeet Singh, Siddhesh Khandelwal, Bowen Pan, Ratnesh Kumar, Andrew Hartnett, Jhony Kaesemodel Pontes, et al. Argoverse 2: Next generation datasets for self-driving perception and forecasting. _arXiv preprint arXiv:2301.00493_ , 2023. 2 

- [56] Y. Xu, X. Yang, L. Gong, H. Lin, T. Wu, Y. Li, and N. Vasconcelos. Explainable object-induced action decision for autonomous vehicles. In _2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 9520– 9529, Los Alamitos, CA, USA, jun 2020. IEEE Computer Society. 3 

- [57] Zhenhua Xu, Yujia Zhang, Enze Xie, Zhen Zhao, Yong Guo, Kenneth KY Wong, Zhenguo Li, and Hengshuang Zhao. Drivegpt4: Interpretable end-to-end autonomous driving via large language model. _arXiv preprint arXiv:2310.01412_ , 2023. 3 

- [58] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, Jun Zhang, Andreas Geiger, Yu Qiao, and Hongyang Li. Generalized predictive model for autonomous driving. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024. 3, 5, 6 

- [59] Fisher Yu, Haofeng Chen, Xin Wang, Wenqi Xian, Yingying Chen, Fangchen Liu, Vashisht Madhavan, and Trevor Darrell. Bdd100k: A diverse driving dataset for heterogeneous multitask learning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 3 

- [60] Fisher Yu, Haofeng Chen, Xin Wang, Wenqi Xian, Yingying Chen, Fangchen Liu, Vashisht Madhavan, and Trevor Darrell. Bdd100k: A diverse driving dataset for heterogeneous multitask learning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 2636–2645, 2020. 2 

- [61] Jianming Zhang, Xin Zou, Li-Dan Kuang, Jin Wang, R Simon Sherratt, and Xioafeng Yu. Cctsdb 2021: a more comprehensive traffic sign detection benchmark. _Human-centric Computing and Information Sciences_ , 12, 2022. 2 

- [62] Shanshan Zhang, Rodrigo Benenson, and Bernt Schiele. Citypersons: A diverse dataset for pedestrian detection. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 3213–3221, 2017. 2 

- [63] Weitao Zhou, Zhong Cao, Yunkang Xu, Nanshan Deng, Xiaoyu Liu, Kun Jiang, and Diange Yang. Long-tail prediction uncertainty aware trajectory planning for self-driving vehicles. In _2022 IEEE 25th International Conference on Intelligent Transportation Systems (ITSC)_ , pages 1275–1282. IEEE, 2022. 2 

- [64] Zhe Zhu, Dun Liang, Songhai Zhang, Xiaolei Huang, Baoli Li, and Shimin Hu. Traffic-sign detection and classification in the wild. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , pages 2110–2118, 2016. 2 

11 

## **CoVLA: Comprehensive Vision-Language-Action Dataset for Autonomous Driving — Supplementary Material —** 

## **A. Heuristic Trajectory Filtering** 

In some instances, trajectory data instability was detected. Specifically, we identified two erroneous behaviors: 

1. Significant jumps 

2. Movement in the wrong direction 

To detect significant jumps, we filtered the trajectory data by the distance between adjacent points. Given a recording frequency of 20 Hz and a maximum speed of 100 km/h, the distance between points should be at most 1.38 meters, which is calculated as following: 


With a tolerance rate of 1.15, the threshold was set to 1.59 meters. All trajectories exceeding this threshold were filtered. 

To detect movement in the wrong direction, we manually checked 400 samples from all scenes and identified 43 invalid trajectories (10.75%). Observations revealed a vibration frequency of 10 Hz in these trajectories. To implement vibration detection, we smoothed the trajectory using a 3-point moving average and calculated the difference between the smoothed trajectory and the original trajectory. We then analyzed the variance of these differences. If the variance exceeded a certain threshold, the trajectory was classified as invalid. This method yielded a precision of 0.64 and a recall of 0.75 on the test dataset, reducing the invalid trajectory rate to 2.6%. Although this method has a relatively high false-positive rate, it is acceptable for the dataset’s scale. 

## **B. Privacy Protection for Dataset Publication** 

We published CoVLA-Dataset<sup>3</sup> on HuggingFace. For privacy protection, we anonymized human faces and license plates in the CoVLA-Dataset images and videos, using Dashcam Anonymizer<sup>4</sup> . 

## **C. Example data in CoVLA-Dataset** 

We present sample data from CoVLA-Dataset. Each data point includes an image, a caption, and vehicle states. An example of an actual caption is shown in Figure 7. For auto-captioning, we use the traffic light detection provided by OpenLenda-s and the front car detection results from the sensor fusion. The list of vehicle states is indicated in Table 4. Each frame contains information on the speed, steering angle, coordinates of the trajectory, and more. 


Figure 7. Example of image and caption in CoVLA-Dataset. 

> 3https://huggingface.co/datasets/turing-motors/CoVLA-Dataset 

> 4https://github.com/varungupta31/dashcam_anonymizer 

12 

|**Key**|**Value**|
|---|---|
|frame<br>~~i~~d|569|
|image<br>~~p~~ath|images/2022-07-08–11-37-27–5<br>~~f~~irst/0569.png|
|vEgo|7.43082332611084|
|vEgoRaw|7.4395833015441895|
|aEgo|0.6044138669967651|
|steeringAngleDeg|0.6073870658874512|
|steeringTorque|69.0|
|brake|0.0|
|brakePressed|false|
|gas|0.20499999821186066|
|gasPressed|true|
|doorOpen|false|
|seatbeltUnlatched|false|
|gearShifter|drive|
|leftBlinker|false|
|rightBlinker|false|
|orientations<br>~~c~~alib|�<br>2_._9467956252753775<br>0_._9174552319868815<br>2_._2181786819453384<br>�<br><br>|
|orientations<br>~~e~~cef|�<br>2_._9243210649189977<br>0_._9224135550861058<br>2_._1900513923432348<br>�|
|orientations<br>~~n~~ed|�<br>_−_0_._013463193567253392<br>0_._006326533926443111<br>_−_2_._990125370637735<br>�|
|positions<br>~~e~~cef|�<br>_−_3959574_._486029379<br>3328427_._354910454<br>3719065_._7393601397<br>�<br><br>|
|velocities<br>~~c~~alib|�<br>7_._317097759615114<br>0_._003242519329502727<br>0_._005369323447773883<br>�|
|velocities<br>~~e~~cef|�<br>_−_2_._6767882666706004<br>3_._547338396353873<br>_−_5_._813015899212604<br>�<br><br>|
|accelerations<br>~~c~~alib|�<br>0_._4734579094803297<br>0_._08559864698994124<br>_−_0_._13132037594775653<br>�|
|accelerations<br>~~d~~evice|�<br>0_._4736293760658642<br>0_._07819260264673351<br>_−_0_._13526157094253702<br>�|
|angular<br>~~v~~elocities<br>~~c~~alib|�<br>0_._011550541795216845<br>0_._012243857869171634<br>_−_0_._007753300486330907<br>�|
|angular<br>~~v~~elocities<br>~~d~~evice|�<br>0_._011675888068301523<br>0_._01206267096884485<br>_−_0_._007848971055415363<br>�|
|timestamp|1657248173200|
||<br><br>_−_0_._015688330416257182<br>_−_0_._9998769191404183<br>0_._00012959444326649344<br>0_._0<br><br>|
||<br>_−_0_._008260370686184616<br>2_._879912020664621_e −_21<br>_−_0_._9999658837914467<br>1_._2200000286102295<br>|
|extrinsic<br>~~m~~atrix|<br>0_._9998428078989188<br>_−_0_._01568886620613436<br>_−_0_._008259354077745229<br>0_._0<br>|
||<br>0_._0<br>0_._0<br>0_._0<br>1_._0<br>|
||<br><br>2648_._0<br>0_._0<br>964_._0<br><br>|
|intrinsic<br>~~m~~atrix|<br>0_._0<br>2648_._0<br>604_._0<br>|
||<br>0_._0<br>0_._0<br>1_._0<br>|
|trajectory<br>~~c~~ount|60|


13 

|<br><br>0_._0<br>|_−_0_._0<br>|0_._0<br><br><br>|
|---|---|---|
|<br>_..._<br>2_._2367286927600376|_..._<br>0_._021314714278469867|_..._<br>0_._011369742248091336<br>|
|<br>_..._<br>4_._529136516056675|_..._<br>0_._05988551136966269|_..._<br>0_._03572205827208557<br>|
|<br>_..._<br>6_._919731941586808|_..._<br>0_._08958899605082428|_..._<br>0_._050459818682157966<br>|
|<br>_..._<br>9_._301852576186251|_..._<br>0_._1417775525229876|_..._<br>0_._07520389298492622<br>|
|trajectory<br><br>_..._|_..._|_..._<br>|
|<br>11_._677091075613516|0_._2108797042962825|0_._09371664992653018<br>|
|<br>_..._<br>14_._027571172292527|_..._<br>0_._28508464282229706|_..._<br>0_._10760938523286476<br>|
|<br>_..._<br>16_._350994760951718|_..._<br>0_._38061347529509826|_..._<br>0_._1208462683905208<br>|
|<br>_..._<br>18_._675065252972097<br>|_..._<br>0_._4777731491748536<br>|_..._<br>0_._14622174266379429<br><br>|
|<br>_..._<br>20_._998125620182435|_..._<br>0_._5860796022647292|_..._<br>0_._1657656398148593<br>|


Table 4. Example of Vehicle States List. 

14 

