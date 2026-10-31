---
title: "Developing Vision-Language-Action Model from Egocentric Videos"
date: "2025-09-26"
authors: "Tomoya Yoshida; Shuhei Kurita; Taichi Nishimura; Shinsuke Mori"
url: https://arxiv.org/abs/2509.21986
pdf: https://arxiv.org/pdf/2509.21986
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.21986)** / [論文ページ](https://arxiv.org/abs/2509.21986)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Developing Vision-Language-Action Model from Egocentric Videos** 

Tomoya Yoshida<sup>1</sup><sup>_,_4</sup> , Shuhei Kurita<sup>2</sup><sup>_,_3</sup><sup>_,_4</sup> , Taichi Nishimura<sup>5</sup> , Shinsuke Mori<sup>1</sup> 

**_Abstract_ — Egocentric videos capture how humans manipulate objects and tools, providing diverse motion cues for learning object manipulation. Unlike the costly, expert-driven manual teleoperation commonly used in training Vision-LanguageAction models (VLAs), egocentric videos offer a scalable alternative. However, prior studies that leverage such videos for training robot policies typically rely on auxiliary annotations, such as detailed hand-pose recordings. Consequently, it remains unclear whether VLAs can be trained directly from raw egocentric videos. In this work, we address this challenge by leveraging EgoScaler, a framework that extracts 6DoF object manipulation trajectories from egocentric videos without requiring auxiliary recordings. We apply EgoScaler to four large-scale egocentric video datasets and automatically refine noisy or incomplete trajectories, thereby constructing a new large-scale dataset for VLA pre-training. Our experiments with a state-of-the-art** _π_ 0 **architecture in both simulated and realrobot environments yield three key findings: (i) pre-training on our dataset improves task success rates by over 20% compared to training from scratch, (ii) the performance is competitive with that achieved using real-robot datasets, and (iii) combining our dataset with real-robot data yields further improvements. These results demonstrate that egocentric videos constitute a promising and scalable resource for advancing VLA research.** 

## I. INTRODUCTION 

Vision-Language-Action models (VLAs) aim to learn general-purpose robot behaviors that follow natural language instructions across environments [3], [4], [5], [6], [7], [8], [9], [10], [11]. Such models are pre-trained with large-scale, multi-embodiment datasets [5], [8], [11] and then fine-tuned on embodiment-specific datasets. However, most pre-training datasets for VLAs heavily rely on human teleoperation, where a number of experts directly manipulate robots to collect instances for imitation learning. This is inherently costly and labor-intensive, leaving a data scarcity problem. 

One promising direction to address this problem is to leverage first-person perspective recordings of humans performing everyday tasks, enabled by the advancement of AR/VR devices and smart glasses [12], [13], [14]. Particularly, such egocentric videos provide diverse human-object interactions at a close range and inherently provide motion cues for learning object manipulation. Several studies have begun to explore how to utilize egocentric videos in robot learning [15], [16], [17], [18]. For example, EgoMimic [16] and EgoVLA [17] leverage enriched egocentric recordings including hand poses to learn robot policies. These studies 

> 1Kyoto University, Kyoto 606-8501, Japan 

> 2National Institute of Informatics, Tokyo 101-8430, Japan 

> 3Institute of Science Tokyo, Tokyo, Japan, Tokyo 152-8550, Japan 

> 4NII LLMC, Tokyo 100-0003, Japan 

> 5Sony Interactive Entertainment, Tokyo 108-0075, Japan Contact: yoshida.tomoya.25h@st.kyoto-u.ac.jp 

demonstrate that utilizing egocentric videos is more timeand scale-efficient than those from teleoperation-based data collection. Unfortunately, these approaches depend on dense auxiliary recordings, such as hand poses and action start/end timestamps. Obtaining these dense auxiliary recordings requires specialized hardware, such as multi-camera systems or depth sensors, as well as extensive manual annotation. In a recent study, LAPA [19] attempted to learn latent action representations from egocentric videos. While this approach is scalable because it does not require auxiliary labels, such latent representations often struggle to capture fine-grained motions. For example, they showed strong performance on simple actions like pushing but only mediocre performance on more complex skills like pick-and-place. 

Considering the limited scalability of rich egocentric recordings and the lack of fine-grained motion cues in egocentric videos, existing methods provide valuable insights but may fall short of offering sufficiently detailed and diverse action examples for robotic foundation models (see Fig. 1). It is also notable that robot policies trained on diverse realworld egocentric recordings can fall short when evaluated within controlled environments, particularly simulators, due to simplified visual systems [20], [21]. Therefore, although egocentric recordings are undeniably valuable resources of human motion cues, they remain underexplored in the existing literature. 

To address this issue, we focus on extracting explicit action trajectories, which provide supervision that represents how to move and rotate objects. We leverage EgoScaler [1], a framework designed to extract object manipulation trajectories from egocentric videos. Each pose in a trajectory represents the centroid and rotation of the manipulated object, approximated as the end-effector states of a robot, excluding the gripper. We apply this framework to four large egocentric video datasets, including Ego4D [22], Ego-Exo4D [23], HDEPIC [24], and Nymeria [25]. The extracted trajectories are then curated by automatically removing noisy or incomplete instances. After this careful filtering process, we construct a new large-scale dataset for VLA pre-training. 

We conduct our experiments based on a state-of-the-art _π_ 0 [8] architecture. For comparison, we include three realrobot datasets—BC-Z [26], BridgeData V2 [27], and Fractal [3], which match our dataset in scale and diversity. We evaluate performance in both simulated (SIMPLER [20]) and real-robot (ALOHA [28]) environments. Our key findings are threefold: 

- 1) We successfully train _π_ 0 from egocentric videos without auxiliary labels, achieving significant improvements over both training from scratch and LAPA. 


Fig. 1: **Comparison of conventional VLA pre-training sources and ours.** We leverage egocentric videos _without auxiliary labels_ for VLA pre-training. Using EgoScaler [1] to extract 6DoF object manipulation trajectories, we construct a large-scale dataset. The multi-camera example is adapted from [2]. 

- 2) Our dataset achieves performance on par with leading real-robot datasets, while slightly outperforming BC-Z and BridgeData V2. 

- 3) Combining our dataset with BridgeData V2 yields further gains, surpassing the performance of pre-training on either dataset alone. 

II. RELATED WORK 

## _A. Dataset for Robotic Foundation Model_ 

Robotic foundation models have been revolutionizing the robot learning literature, as they enable the execution of multi-purpose and environment-agnostic actions across diverse robotic hardware. Such robotic foundation models, however, rely on large-scale datasets for robotic actions that typically cover multiple robotic hardware and diverse tasks [5], [8], [11], [10]. As constructing such collections requires substantial effort from the robotics community, several datasets have been created through worldwide collaborations [29], [5]. Open X-Embodiment (OXE) dataset [5] aggregates over 60 individual datasets from various institutions into a unified collection that spans diverse manipulation tasks across multiple embodiments. In OXE, they demonstrate that scaling datasets is crucial for improving model performance. Similarly, _π_ 0 model [8] depends on the internal dataset of ‘ _π_ ,’ which consists of over 10,000 hours of dexterous manipulation data and makes it possible to execute environment-agnostic and long-horizon tasks. While these datasets have substantially advanced robot learning, the reliance on extensive human effort to construct large-scale robot datasets has become a major bottleneck to progress toward a general-purpose robotic foundation model. To ad- 

dress this inherent limitation of manual dataset collection, we leverage egocentric videos to automatically construct a pre-training dataset for robotic foundation models. 

## _B. Egocentric Video Dataset_ 

Egocentric vision captures fine-grained hand–object interactions, providing motion cues for action understanding [2], [30]. Reflecting its importance, a number of datasets have been introduced over the past decade [22], [23], [31], [32], [33], [34], [24], [35]. For example, Ego4D [22] comprises over 3,000 hours of human daily activity videos spanning hundreds of scenarios, including cooking and crafting. Although egocentric videos remain relatively limited in scale compared to internet videos, the domain is expected to grow with the advancement of AR/VR agents and smart glasses [36], [35], [37]. This anticipated growth will further expand egocentric video collections, underscoring their potential as a scalable resource for robot learning. 

## _C. Robot Learning from Human Demonstration Recordings_ 

Recordings of human everyday tasks in the real world have emerged as a promising source for robot learning, reducing reliance on costly teleoperation-based data collection [15], [19], [38]. In VRB [39] and HRP [40], they extract visual affordances during human-object interaction for grasping tasks from egocentric videos to predict potential interaction regions, providing implicit guidance for robotic dexterous manipulation tasks. Beyond grasping capabilities, a variety of approaches have been explored for more complex manipulation tasks [16], [41], [42], [18], [43], [44], [17], [45], [46]. MimicPlay [41] introduces an approach to learn highlevel action plans by imitating hand trajectories from multi- 


Fig. 2: **Samples of extracted trajectories via EgoScaler [1].** The trajectory is color-coded from cyan (start) to purple (end) to indicate temporal progression. Red, green, and blue arrows represent the X, Y, and Z axes of the object’s coordinate frame at each time step. 

view recordings of human demonstrations. By incorporating these high-level plans as latent representations into robot policies, this work achieves improved performance with minimal robot data. More recently, EgoVLA [17] pre-trains on egocentric recordings including hand poses captured with specialized hardware, significantly enhancing VLA performance compared to training from scratch. Although the utilization of egovision in robot learning seems successful, these existing approaches rely on recordings captured with specialized hardware, such as multi-camera systems, depth sensors, or proprietary devices like Aria Glasses [13], which limits the scalability of the resulting datasets. In contrast, our work focuses on constructing a pre-training dataset from egocentric videos without auxiliary labels, thereby unlocking the scalability of large-scale egocentric video resources for robot learning. 

## III. METHOD 

Considering the cost and scalability issues of collecting teleoperation data, we leverage egocentric videos for VLA pre-training. However, egocentric videos do not directly provide action trajectories. To address this, we use EgoScaler [1], a framework that extracts object manipulation trajectories from egocentric videos. Applying this framework to large and diverse egocentric video datasets, we construct a large-scale pre-training dataset. As shown in Fig. 1, each episode in this dataset comprises an image sequence, a text instruction, and a 6DoF object pose trajectory. We pretrain a VLA on this dataset and then post-train it on small embodiment-specific datasets. 

## _A. Problem Definition_ 

Following previous studies [28], [8], [47], we train a robot policy that outputs sequences of future robot actions (action chunks). Formally, at each timestep _t_ , given a language instruction _ℓ_ , RGB observations _vt_ , and proprioceptive state **_τ_** _t_ , we model a policy _π_ ( **a** 1: _H | vt,_ **_τ_** _t, ℓ_ ) that defines a distribution over the next _H_ actions _{_ **a** _t, . . . ,_ **a** _t_ + _H−_ 1 _}_ . In pre-training, _vt_ is a single image, and both **_τ_** _t_ and **a** _t_ are approximated in an end-effector space without gripper states, derived from egocentric videos. In post-training and evaluation, _vt_ may comprise images from one or several 

cameras, depending on the hardware design, and both **_τ_** _t_ and **a** _t_ are defined in the robot’s native control space (e.g., joint space or end-effector space). Despite these gaps, recent studies have demonstrated that VLAs are capable of dealing with such modality differences [5], [8]. At inference time, an action chunk _a_ 1: _H ∼ π_ ( _a_ 1: _H | vt, τt, ℓ_ ) is sampled from the trained policy and then executed sequentially. 

## _B. Pre-training Dataset Construction_ 

**Re-visiting EgoScaler Framework.** EgoScaler [1] extracts a 6DoF object manipulation trajectory from an egocentric video. This framework consists of four stages. First, given a video clip, the start and end timestamps of the action as well as the manipulated object within the scene are identified using GPT-4o [48]. Second, the position sequence of the manipulated object is extracted using an open-vocabulary segmentation model [49], [50] and a dense 3D point tracker [51]. Third, this sequence is projected into the camera coordinate system of the action start frame via point cloud registration [52], eliminating the camera-wearer’s movement. Fourth, a rotation sequence is obtained by computing the transformation between consecutive object point clouds using singular value decomposition. Combining these steps yields a sequence of 6DoF poses **_τ_** = _{_ **_τ_** 1 _,_ **_τ_** 2 _, . . . ,_ **_τ_** _T }_ , where **_τ_** _t_ = ( _x, y, z,_ roll _,_ pitch _,_ yaw). Here, ( _x, y, z_ ) captures the translational components of the object’s centroid position, and (roll _,_ pitch _,_ yaw) represents the rotational components of the object. These trajectories represent the object’s pose over time, enabling us to approximate the end-effector states during manipulation without gripper states. As illustrated in Fig. 2, we successfully obtain action trajectories across diverse environments. 

**Egocentric Video Resources.** EgoScaler can be applied to various types of egocentric videos. The original paper of EgoScaler targets only Exo-Ego4D [23], but this work expands it to four large egocentric video datasets with diverse activities and scenarios: Ego4D [22], Ego-Exo4D [23], HDEPIC [24], and Nymeria [25]. Ego4D and Ego-Exo4D have a broader range of scenarios, including cooking, experiments, crafting, and repair. HD-EPIC primarily captures human activities in the cooking domain. Nymeria focuses on full-body 


Fig. 3: **Samples of computing background track similarity (BGTS).** Tracked sequences are depicted in red. Low BGTS indicates the object moves due to hand interaction. 

motion understanding, resulting in fewer scenarios involving hand–object interactions. Unlike the other datasets, Ego4D does not provide camera intrinsics required by EgoScaler to reconstruct 3D trajectories. We therefore estimate them in advance using COLMAP [53], [54]. COLMAP searches for an initial image pair that satisfies predefined featurematching and geometric constraints, such as a minimum number of inliers and a maximum re-projection error. If no valid pair is found, we exclude the corresponding instance from our dataset. By applying EgoScaler to these datasets, we initially obtained 124,559 episodes. 

**Data Curation Methods.** We found that EgoScaler sometimes produces inaccurate trajectories, mainly due to object detection and point cloud registration errors. To remove them automatically, we apply two rule-based filters: a travel distance threshold for registration errors and a background track similarity threshold for detection errors. 

For the travel distance threshold ( _δDT_ ), we define the travel distance _D_ of a trajectory as the cumulative displacement of its positional component, _D_ =<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_−_1</sup><sup>_∥_</sup><sup>**p**</sup><sup>_t_+1</sup><sup>_−_</sup><sup>**p**</sup><sup>_t∥_2,</sup> where **p** _t_ = ( _xt, yt, zt_ ) denotes the translational element of the object trajectory **_τ_** _t_ . Trajectories corrupted by registration errors often contain abrupt mismatches across consecutive frames, leading to abnormally large _D_ . We therefore discard trajectories with _D > δ_ TD. 

For the background track similarity threshold ( _δ_ BGTS), let the object track be _{_ **o** _t}_<sup>_T_</sup> _t_ =1<sup>andthebackgroundtrack</sup> be _{_ **q** _t}_<sup>_T_</sup> _t_ =1<sup>,where</sup><sup>**o**</sup><sup>_t,_</sup><sup>**q**</sup><sup>_t∈_R2areimage-planepositions</sup> obtained by point tracker [51] within EgoScaler framework. We observed that tracks from detection errors often resemble 


TABLE I: **Statistics of previous robot datasets and ours.** 

|Dataset|#Episodes|#Verbs|#Objects|
|---|---|---|---|
|RoboTurk [55]|1,796|2|2|
|BC-Z [26]|39,350|9|17|
|BridgeData V2 [27]|53,192|270|749|
|Fractal [3]|87,212|6|13|
|DROID [29]|92,233|194|907|
|Ours|45,157|313|1,217|


those of the background, as shown in Fig. 3. This is because detection errors typically occur on non-interacted, static objects. To detect such cases, we compute the background track similarity (BGTS) as the average cosine similarity between the object and background displacements: 


where **u** _t_ = **o** _t_ +1 _−_ **o** _t_ and **b** _t_ = **q** _t_ +1 _−_ **q** _t_ are velocity vectors from the object and background tracks. We discard episodes with BGTS _> δ_ BGTS, where we empirically set _δ_ BGTS = 0 _._ 7 based on simulator experiments. 

Moreover, due to depth inconsistencies between consecutive frames, the translational components of the extracted trajectories often contain jitter noise. To suppress this, we apply a smoothing filter by averaging each translation vector over a five-frame window centered at the current frame. At sequence boundaries (i.e., _t_ = 1 _,_ 2 _, T −_ 1 _, T_ ), the window size is reduced accordingly, increasing the influence of the central frame. Applying these curation methods, we finally obtain 45,157 episodes. The statistics of our dataset, along with teleoperation-based robot datasets, are shown in Table I. 

## _C. Policy Training_ 

In this work, we use a state-of-the-art VLA _π_ 0 [8]. Built on the pre-trained VLM PaliGemma [56], _π_ 0 employs a flow-matching–based [57], [58] action head that incorporates robot state and generates continuous, high-frequency actions. **Action Representation.** During pre-training on our dataset, an action is represented as the displacement of the 6DoF 


Fig. 5: **Performance of baselines and our dataset across manipulation tasks.** “ObjectA – ObjectB” denotes the task “pick ObjectA and place it into ObjectB.” Parentheses indicate the used dataset for latent action pretraining. Average success rates (%) with standard error are reported. 

object pose trajectory **_τ_** : 


Here, _{xt, yt, zt}_ denotes the positional coordinates, and rot6D _t ∈_ R<sup>6</sup> is a flattened vector of the first two columns of the rotation matrix _Rt_ . Because gripper states cannot be obtained from Section III-B, each action is represented by a 9-dimensional vector. For proprioceptive states, we use the original trajectories **_τ_** for each timestep, converting rotational elements into rot6D representation. To mitigate distribution differences between human and robot data, all actions and proprioceptive states are normalized during training [16]. **Dataset Merging for Pre-training.** Pre-training VLAs often involves combining multiple robot-embodiment datasets to enable large-scale and diverse training [5], [8]. Following these, when merging our dataset with existing robot datasets, we pad and normalize action and proprioceptive vectors as needed to match dimensionalities across datasets, and then perform joint training on the concatenated data. 

**Training Objective.** The model is trained to predict a sequence of future actions conditioned on language, vision, and proprioception inputs. We minimize the mean squared error between the predicted action **a** ˆ _t_ and the ground truth action **a** _t_ across a chunk of _H_ future steps: 


This loss is used for both pre-training and post-training. 

## IV. EXPERIMENTS 

We evaluate the effectiveness of our dataset as a pretraining source in simulated and real-robot environments. For all experiments, we employ the _π_ 0 [8] architecture. Unlike the conventional settings of fine-tuning a publicly available _π_ 0 checkpoint, we **pre-train** a _π_ 0 model within our dataset. 

## _A. Experimental Setup_ 

**Manipulation Task Details.** For simulated environments, we use SIMPLER [20] BridgeData V2 environment, which contains four pick-and-place tasks. Inspired by [19], we decided to collect a small amount of successful rollouts for the post-training purpose. For this purpose, we applied a pretrained _π_ 0 [8] on _π_ [8] dataset and post-trained it on BridgeData V2 [27] dataset. Using the _π_ 0, 25 successful rollouts were collected for each task. For evaluation, performance is measured with 200 rollouts for each task. 

For real-robot environments, as shown in Fig. 4, we use ALOHA [28] and design four language-aware pick-and-place tasks with four objects. The task instruction follows the template: “Pick up the [carrot/onion] and place it into the [pot/bowl].” In each rollout, all four objects are present simultaneously, requiring the model to interpret the given instruction correctly. We manually collect 200 episodes per task, totaling 800 episodes. For evaluation, performance is measured with 10 rollouts for each task. The success rate is calculated using a two-stage scoring scheme: 0.5 points for grasping the correct object, and an additional 0.5 points for placing it in the correct location. 

**Implementation Details.** We trained _π_ 0 on 8×H200 GPUs using AdamW [59] optimizer with bfloat16 precision under a constant learning rate of 5 _×_ 10<sup>_−_5</sup> . We freeze the pretrained VLM parameters during both pre-training and posttraining. This design, inspired by SmolVLA [9], makes training GPU-friendly and time-efficient while preserving competitive performance. Pre-training was conducted for 20,000 steps with a batch size of 1,024. In evaluation, we use 40,000 steps with a batch size of 128 for the realrobot setting. For the simulator setting, we select the best checkpoint on a validation set, evaluated every 10,000 steps between 10,000 and 50,000 steps. 

## _B. Results_ 

**Comparison with Scratch and Our Approach.** The scratch baseline is a model trained only on the post-training dataset. 

|ABLE II: **Com**|**parison **|**with rob**|**ot data**|**sets.** S|uccesses||`SIMPLER`|`Real Robot`|
|---|---|---|---|---|---|---|---|---|
|t of 10 rollouts|are repo|rted for|each task|, with t|he final|`50`<br>**`% Success Rate`**|`62`||
|lumn showing t<br>Dataset|he total.<br>Carrot<br>-Pot|Carrot<br>-Bowl|Onion<br>-Pot|Onion<br>-Bowl|_Total_|`25`<br><br>~~`27`~~|`46`|`55`|
||||||||||
|BridgeData V2 [27]|4/10|3/10|6/10|4/10|17/40|`25`<br>||`44`|
|BC-Z [26]|5/10|5/10|4/10|5/10|19/40||`40`||
|Fractal [3]|7/10|4/10|7/10|4/10|22/40||||
|Ours|4/10|6/10|7/10|4/10|21/40|`0`|`30`||
|Ours + [27]|7/10|7/10|7/10|6/10|**27/40**|`5K`<br>`20K`<br>`45K`|`5K`<br>`2`|`0K`<br>`45K`|
|||||||`Dataset size (#Episodes)`|`Dataset size`|`(#Episodes)`|


TABLE II: **Comparison with robot datasets.** Successes out of 10 rollouts are reported for each task, with the final column showing the total. 

Fig. 6: **Dataset size and performance.** Average success rates (%) with standard error reported. 

As shown in Fig. 5, our method outperforms the scratch baseline in real-robot tasks, while achieving smaller but consistent gains in simulation. Under an identical architecture and post-training setting, the scratch model attains 0% success in real-robot, indicating a failure to ground instructions and generate meaningful trajectories. The smaller performance gap in simulation is likely due to a visual domain gap, which we discuss in Section IV-C. Moreover, merging our dataset with BridgeData V2 [27] yields additional improvements compared to our dataset alone. 

TABLE III: **Performance comparison across different background track similarity thresholds (BGTS).** 

|_δ_BGTS|#Episodes|SIMPLER [20]|Real Robot|
|---|---|---|---|
|0.5|28,719|25.8_±_5_._4|53.8_±_5_._2|
|0.7|45,157|**26.0**_±_5_._9|**55.0**_±_6_._1|
|1.0|86,427|22.5_±_4_._8|38.8_±_4_._3|


**Comparison of LAPA and Our Approach.** LAPA [19] is an implicit pre-training approach that does not rely on auxiliary labels, enabling the use of egocentric videos as VLA pretraining data. In latent action pre-training, a discrete set of “action” tokens is first learned via a VQ-VAE [60] quantizer applied to temporally separated image frame pairs. This approach then pre-trains a VLA to predict these tokens from image–text pairs. We apply the pretraining methodology of LAPA to the same _π_ 0 model instead of the original VLA architecture proposed in the paper for the sake of fair comparison. For the latent action pre-training setting, we conduct experiments on both our dataset without action labels and Something-Something V2 (SthV2) [61] dataset used in the paper. SthV2 consists of short first- and thirdperson perspective videos, covering human actions with a variety of objects. 

complement robot datasets and serve as a useful component within larger multi-embodiment collections such as OXE [5]. Second, pre-training on our dataset alone yields higher performance than BC-Z and BridgeData V2, but lower than Fractal, owing to its much larger scale. Together, these results highlight the importance of large-scale pre-training for VLAs and demonstrate that our dataset is effective both on its own and when combined with existing robot datasets. 

## _C. Ablation Study_ 

**Dataset Scalability.** As our framework automatically extracts object manipulation trajectories, we examine how dataset scale affects performance. We utilize data at ratios of 1.0, 0.5, and 0.1 of the full dataset (corresponding to 45K, 20K, and 5K episodes, respectively). Fig. 6 illustrates the results across different dataset sizes. In the real-robot setting, scaling our dataset significantly improves task performance. In contrast, in simulation, the full dataset slightly underperforms the 0.1-ratio subset by 1% on average. The limited improvement from scaling in simulation likely stems from a visual domain gap. While the simulator provides reduced noise and controlled variability, the rich and diverse cues in egocentric videos may hinder performance. 

Fig. 5 presents the performance comparison between LAPA and ours. Our approach consistently outperforms LAPA in both real-robot and simulated environments. Although LAPA outperforms the scratch baseline in real-robot tasks, its performance degrades in simulation, likely due to the simplified visual systems in simulated environments. This suggests that leveraging rich, diverse egocentric video without action labels can harm performance in simulation. Similarly, the greater visual diversity in our dataset is more effective than SthV2 in the real-robot setting, but it leads to performance drops in simulation. These results indicate that explicit action trajectories provide more robust and informative supervision across environments. 

**Hyperparameter of Background Trajectory Similarity.** Setting an appropriate curation threshold is crucial to balancing the scale and quality of our dataset. We conduct an ablation study, varying the background trajectory similarity threshold _δ_ BGTS = _{_ 0 _._ 5 _,_ 0 _._ 7 _,_ 1 _._ 0 _}_ . As shown in Table III, a lower threshold ( _δ_ BGTS = 0 _._ 5) removes noisy trajectories but significantly reduces the dataset scale. In contrast, a higher threshold ( _δ_ BGTS = 1 _._ 0) retains more episodes but leads to degraded performance due to increased noise. We find that _δ_ BGTS = 0 _._ 7 achieves the best trade-off between dataset size and task performance in simulation experiments. We therefore adopt this value for constructing our dataset. 

**Comparison of Robot Datasets and Ours.** Table II summarizes the performance of _π_ 0 pre-trained separately on three robot datasets (Fractal [3], BridgeData V2 [27], and BC-Z [26]) and on our dataset in real-robot tasks. This comparison reveals two key findings. First, merging ours with BridgeData V2 outperforms using any robot dataset alone. This result suggests that our dataset can effectively 

## V. CONCLUSION 

In this paper, we demonstrated that egocentric videos without auxiliary labels can serve as an effective resource for VLA pre-training. Using EgoScaler, we constructed a large-scale dataset by extracting explicit object manipulation trajectories from egocentric videos. Pre-training on this dataset yields performance competitive with real-robot datasets and significantly outperforms training from scratch and LAPA. Moreover, merging our dataset with a real-robot dataset further boosts performance. These findings highlight that utilizing egocentric videos is a promising step toward addressing the data scarcity problem in robot learning. 

## ACKNOWLEDGMENT 

This work was supported by JSPS KAKENHI Grant Number JP22K17983, JP22KK0184 and JST CRONOS JPMJCS24K6. 

## REFERENCES 

- [1] T. Yoshida, S. Kurita, T. Nishimura, and S. Mori, “Generating 6dof object manipulation trajectories from action description in egocentric vision,” in _Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)_ , 2025. 

- [2] T. Kwon, B. Tekin, J. St¨uhmer, F. Bogo, and M. Pollefeys, “H2o: Two hands manipulating objects for first person interaction recognition,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2021. 

- [3] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, J. Ibarz, B. Ichter, A. Irpan, T. Jackson, S. Jesmonth, N. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, K.-H. Lee, S. Levine, Y. Lu, U. Malla, D. Manjunath, I. Mordatch, O. Nachum, C. Parada, J. Peralta, E. Perez, K. Pertsch, J. Quiambao, K. Rao, M. Ryoo, G. Salazar, P. Sanketi, K. Sayed, J. Singh, S. Sontakke, A. Stone, C. Tan, H. Tran, V. Vanhoucke, S. Vega, Q. Vuong, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich, “Rt-1: Robotics transformer for real-world control at scale,” in _arXiv preprint arXiv:2212.06817_ , 2022. 

- [4] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, Q. Vuong, V. Vanhoucke, H. Tran, R. Soricut, A. Singh, J. Singh, P. Sermanet, P. R. Sanketi, G. Salazar, M. S. Ryoo, K. Reymann, K. Rao, K. Pertsch, I. Mordatch, H. Michalewski, Y. Lu, S. Levine, L. Lee, T.-W. E. Lee, I. Leal, Y. Kuang, D. Kalashnikov, R. Julian, N. J. Joshi, A. Irpan, B. Ichter, J. Hsu, A. Herzog, K. Hausman, K. Gopalakrishnan, C. Fu, P. Florence, C. Finn, K. A. Dubey, D. Driess, T. Ding, K. M. Choromanski, X. Chen, Y. Chebotar, J. Carbajal, N. Brown, A. Brohan, M. G. Arenas, and K. Han, “Rt2: Vision-language-action models transfer web knowledge to robotic control,” in _Proceedings of The 7th Conference on Robot Learning_ , 2023. 

- [5] O. X.-E. Collaboration, “Open x-embodiment: Robotic learning datasets and rt-x models,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [6] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo, Y. L. Tan, L. Y. Chen, Q. Vuong, T. Xiao, P. R. Sanketi, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _Robotics: Science and Systems_ , 2024. 

- [7] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” in _Proceedings of The 8th Conference on Robot Learning_ , 2025. 

- [8] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [9] M. Shukor, D. Aubakirova, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, _et al._ , “Smolvla: A vision-language-action model for affordable and efficient robotics,” _arXiv preprint arXiv:2506.01844_ , 2025. 

- [10] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang, _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” _arXiv preprint arXiv:2503.06669_ , 2025. 

- [11] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang, _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [12] Meta, “Quest 3,” 2023. [Online]. Available: https://www.meta.com/ quest/quest-3/ 

- [13] J. Engel, K. Somasundaram, M. Goesele, A. Sun, A. Gamino, A. Turner, A. Talattof, A. Yuan, B. Souti, B. Meredith, _et al._ , “Project aria: A new tool for egocentric multi-modal ai research,” _arXiv preprint arXiv:2308.13561_ , 2023. 

- [14] Apple, “Apple vision pro,” 2024. [Online]. Available: https: //www.apple.com/apple-vision-pro/ 

- [15] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta, “R3m: A universal visual representation for robot manipulation,” in _Proceedings of The 6th Conference on Robot Learning_ , 2023. 

- [16] S. Kareer, D. Patel, R. Punamiya, P. Mathur, S. Cheng, C. Wang, J. Hoffman, and D. Xu, “Egomimic: Scaling imitation learning via egocentric video,” _arXiv preprint arXiv:2410.24221_ , 2024. 

- [17] R. Yang, Q. Yu, Y. Wu, R. Yan, B. Li, A.-C. Cheng, X. Zou, Y. Fang, H. Yin, S. Liu, _et al._ , “Egovla: Learning vision-language-action models from egocentric human videos,” _arXiv preprint arXiv:2507.12440_ , 2025. 

- [18] R. Hoque, P. Huang, D. J. Yoon, M. Sivapurapu, and J. Zhang, “Egodex: Learning dexterous manipulation from large-scale egocentric video,” _arXiv preprint arXiv:2505.11709_ , 2025. 

- [19] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin, L. Liden, K. Lee, J. Gao, L. Zettlemoyer, D. Fox, and M. Seo, “Latent action pretraining from videos,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [20] X. Li, K. Hsu, J. Gu, O. Mees, K. Pertsch, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, S. Levine, J. Wu, C. Finn, H. Su, Q. Vuong, and T. Xiao, “Evaluating real-world robot manipulation policies in simulation,” in _Proceedings of The 8th Conference on Robot Learning_ , 2025. 

- [21] S. H¨ofer, K. Bekris, A. Handa, J. C. Gamboa, M. Mozifian, F. Golemo, C. Atkeson, D. Fox, K. Goldberg, J. Leonard, C. Karen Liu, J. Peters, S. Song, P. Welinder, and M. White, “Sim2real in robotics and automation: Applications and challenges,” _IEEE Transactions on Automation Science and Engineering_ , vol. 18, no. 2, pp. 398–400, 2021. 

- [22] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu, _et al._ , “Ego4d: Around the world in 3,000 hours of egocentric video,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022, pp. 18 995–19 012. 

- [23] K. Grauman, A. Westbury, L. Torresani, K. Kitani, J. Malik, T. Afouras, K. Ashutosh, V. Baiyya, S. Bansal, B. Boote, E. Byrne, Z. Chavis, J. Chen, F. Cheng, F.-J. Chu, S. Crane, A. Dasgupta, J. Dong, M. Escobar, C. Forigua, A. Gebreselasie, S. Haresh, J. Huang, M. M. Islam, S. Jain, R. Khirodkar, D. Kukreja, K. J. Liang, J.-W. Liu, S. Majumder, Y. Mao, M. Martin, E. Mavroudi, T. Nagarajan, F. Ragusa, S. K. Ramakrishnan, L. Seminara, A. Somayazulu, Y. Song, S. Su, Z. Xue, E. Zhang, J. Zhang, A. Castillo, C. Chen, X. Fu, R. Furuta, C. Gonzalez, P. Gupta, J. Hu, Y. Huang, Y. Huang, W. Khoo, A. Kumar, R. Kuo, S. Lakhavani, M. Liu, M. Luo, Z. Luo, B. Meredith, A. Miller, O. Oguntola, X. Pan, P. Peng, S. Pramanick, M. Ramazanova, F. Ryan, W. Shan, K. Somasundaram, C. Song, A. Southerland, M. Tateno, H. Wang, Y. Wang, T. Yagi, M. Yan, X. Yang, Z. Yu, S. C. Zha, C. Zhao, Z. Zhao, Z. Zhu, J. Zhuo, P. Arbelaez, G. Bertasius, D. Damen, J. Engel, G. M. Farinella, A. Furnari, B. Ghanem, J. Hoffman, C. Jawahar, R. Newcombe, H. S. Park, J. M. Rehg, Y. Sato, M. Savva, J. Shi, M. Z. Shou, and M. Wray, “Ego-exo4d: Understanding skilled human activity from first- and third-person perspectives,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

- [24] T. Perrett, A. Darkhalil, S. Sinha, O. Emara, S. Pollard, K. K. Parida, K. Liu, P. Gatti, S. Bansal, K. Flanagan, J. Chalk, Z. Zhu, R. Guerrier, F. Abdelazim, B. Zhu, D. Moltisanti, M. Wray, H. Doughty, and D. Damen, “Hd-epic: A highly-detailed egocentric video dataset,” in 

_Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [25] L. Ma, Y. Ye, F. Hong, V. Guzov, Y. Jiang, R. Postyeni, L. Pesqueira, A. Gamino, V. Baiyya, H. J. Kim, _et al._ , “Nymeria: A massive collection of multimodal egocentric daily motion in the wild,” in _European Conference on Computer Vision (ECCV)_ , 2024. 

- [26] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn, “Bc-z: Zero-shot task generalization with robotic imitation learning,” in _Proceedings of the 5th Conference on Robot Learning_ , 2022. 

- [27] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. HansenEstruch, A. W. He, V. Myers, M. J. Kim, M. Du, A. Lee, K. Fang, C. Finn, and S. Levine, “Bridgedata v2: A dataset for robot learning at scale,” in _Proceedings of The 7th Conference on Robot Learning_ , 2023. 

- [28] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware,” in _Proceedings of Robotics: Science and Systems_ , 2023. 

- [29] S. Jayanthi, L. Chen, N. Balabanska, V. Duong, E. Scarlatescu, E. Ameperosa, Z. H. Zaidi, D. Martin, T. K. D. Matto, M. Ono, and M. Gombolay, “Droid: Learning from offline heterogeneous demonstrations via reward-policy distillation,” in _Proceedings of The 7th Conference on Robot Learning_ , 2023, pp. 1547–1571. 

- [30] Y. Liu, Y. Liu, C. Jiang, K. Lyu, W. Wan, H. Shen, B. Liang, Z. Fu, H. Wang, and L. Yi, “Hoi4d: A 4d egocentric dataset for categorylevel human-object interaction,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- [31] D. Damen, H. Doughty, G. M. Farinella, S. Fidler, A. Furnari, E. Kazakos, D. Moltisanti, J. Munro, T. Perrett, W. Price, and M. Wray, “Scaling egocentric vision: The epic-kitchens dataset,” in _European Conference on Computer Vision (ECCV)_ , 2018. 

- [32] D. Damen, H. Doughty, G. M. Farinella, A. Furnari, J. Ma, E. Kazakos, D. Moltisanti, J. Munro, T. Perrett, W. Price, and M. Wray, “Rescaling egocentric vision: Collection, pipeline and challenges for epickitchens-100,” _International Journal of Computer Vision (IJCV)_ , vol. 130, p. 33–55, 2022. 

- [33] F. Sener, D. Chatterjee, D. Shelepov, K. He, D. Singhania, R. Wang, and A. Yao, “Assembly101: A large-scale multi-view video dataset for understanding procedural activities,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 

- [34] Y. Li, M. Liu, and J. M. Rehg, “In the eye of beholder: Joint learning of gaze and actions in first person video,” in _Proceedings of the European Conference on Computer Vision (ECCV)_ , 2018. 

- [35] J. Yang, S. Liu, H. Guo, Y. Dong, X. Zhang, S. Zhang, P. Wang, Z. Zhou, B. Xie, Z. Wang, B. Ouyang, Z. Lin, M. Cominelli, Z. Cai, B. Li, Y. Zhang, P. Zhang, F. Hong, J. Widmer, F. Gringoli, L. Yang, and Z. Liu, “Egolife: Towards egocentric life assistant,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

- [36] C. Plizzari, G. Goletto, A. Furnari, S. Bansal, F. Ragusa, G. M. Farinella, D. Damen, and T. Tommasi, “An outlook into the future of egocentric vision,” _International Journal of Computer Vision_ , vol. 132, no. 11, pp. 4880–4936, 2024. 

- [37] X. Wang, T. Kwon, M. Rad, B. Pan, I. Chakraborty, S. Andrist, D. Bohus, A. Feniello, B. Tekin, F. V. Frujeri, N. Joshi, and M. Pollefeys, “Holoassist: an egocentric human interaction dataset for interactive ai assistants in the real world,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

- [38] H. Kim, J. Kang, H. Kang, M. Cho, S. J. Kim, and Y. Lee, “Uniskill: Imitating human videos via cross-embodiment skill representations,” _arXiv preprint arXiv:2505.08787_ , 2025. 

- [39] S. Bahl, R. Mendonca, L. Chen, U. Jain, and D. Pathak, “Affordances from human videos as a versatile representation for robotics,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023, pp. 13 778–13 790. 

- [40] M. K. Srirama, S. Dasari, S. Bahl, and A. Gupta, “HRP: Human affordances for Robotic Pre-training,” in _Proceedings of Robotics: Science and Systems_ , 2024. 

   - [42] M. Lepert, J. Fang, and J. Bohg, “Phantom: Training robots without robots using only human videos,” _arXiv preprint arXiv:2503.00779_ , 2025. 

   - [43] J. Shi, Z. Zhao, T. Wang, I. Pedroza, A. Luo, J. Wang, J. Ma, and D. Jayaraman, “Zeromimic: Distilling robotic manipulation skills from web videos,” in _IEEE International Conference on Robotics and Automation (ICRA)_ , 2025. 

   - [44] H. Chen, B. Sun, A. Zhang, M. Pollefeys, and S. Leutenegger, “Vidbot: Learning generalizable 3d actions from in-the-wild 2d human videos for zero-shot robotic manipulation,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 

   - [45] V. Liu, A. Adeniji, H. Zhan, S. Haldar, R. Bhirangi, P. Abbeel, and L. Pinto, “Egozero: Robot learning from smart glasses,” _arXiv preprint arXiv:2505.20290_ , 2025. 

   - [46] M. Lepert, J. Fang, and J. Bohg, “Masquerade: Learning from in-the-wild human videos using data-editing,” _arXiv preprint arXiv:2508.09976_ , 2025. 

   - [47] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “Fast: Efficient action tokenization for vision-language-action models,” _arXiv preprint arXiv:2501.09747_ , 2025. 

   - [48] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford, _et al._ , “Gpt-4o system card,” _arXiv preprint arXiv:2410.21276_ , 2024. 

   - [49] S. Liu, Z. Zeng, T. Ren, F. Li, H. Zhang, J. Yang, Q. Jiang, C. Li, J. Yang, H. Su, _et al._ , “Grounding dino: Marrying dino with grounded pre-training for open-set object detection,” in _European Conference on Computer Vision (ECCV)_ , 2024. 

   - [50] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo, P. Doll´ar, and R. Girshick, “Segment anything,” _arXiv:2304.02643_ , 2023. 

   - [51] Y. Xiao, Q. Wang, S. Zhang, N. Xue, S. Peng, Y. Shen, and X. Zhou, “Spatialtracker: Tracking any 2d pixels in 3d space,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 

   - [52] J. Park, Q.-Y. Zhou, and V. Koltun, “Colored point cloud registration revisited,” in _Proceedings of the IEEE international conference on computer vision (ICCV)_ , 2017. 

   - [53] J. L. Sch¨onberger and J.-M. Frahm, “Structure-from-motion revisited,” in _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2016. 

   - [54] J. L. Sch¨onberger, E. Zheng, M. Pollefeys, and J.-M. Frahm, “Pixelwise view selection for unstructured multi-view stereo,” in _European Conference on Computer Vision (ECCV)_ , 2016. 

   - [55] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, J. Gao, J. Emmons, A. Gupta, E. Orbay, S. Savarese, and L. FeiFei, “Roboturk: A crowdsourcing platform for robotic skill learning through imitation,” in _Proceedings of The 2nd Conference on Robot Learning_ , 2018. 

   - [56] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello, _et al._ , “Paligemma: A versatile 3b vlm for transfer,” _arXiv preprint arXiv:2407.07726_ , 2024. 

   - [57] Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, and M. Le, “Flow matching for generative modeling,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

   - [58] Q. Liu, “Rectified flow: A marginal preserving approach to optimal transport,” _arXiv preprint arXiv:2209.14577_ , 2022. 

   - [59] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” in _International Conference on Learning Representations_ , 2019. 

   - [60] A. van den Oord, O. Vinyals, and k. kavukcuoglu, “Neural discrete representation learning,” in _Advances in Neural Information Processing Systems_ , 2017. 

   - [61] R. Goyal, S. Ebrahimi Kahou, V. Michalski, J. Materzynska, S. Westphal, H. Kim, V. Haenel, I. Fruend, P. Yianilos, M. Mueller-Freitag, _et al._ , “The” something something” video database for learning and evaluating visual common sense,” in _Proceedings of the IEEE international conference on computer vision_ , 2017. 

- [41] C. Wang, L. Fan, J. Sun, R. Zhang, L. Fei-Fei, D. Xu, Y. Zhu, and A. Anandkumar, “Mimicplay: Long-horizon imitation learning by watching human play,” in _Proceedings of The 7th Conference on Robot Learning_ , 2023. 

