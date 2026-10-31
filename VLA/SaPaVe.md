---
title: "SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics"
date: "2026-03-12"
authors: "Mengzhen Liu; Enshen Zhou; Cheng Chi; Yi Han; Shanyu Rong; Liming Chen"
venue: "CVPR 2026"
url: https://arxiv.org/abs/2603.12193
pdf: https://arxiv.org/pdf/2603.12193
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.12193)** / [論文ページ](https://arxiv.org/abs/2603.12193)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This CVPR paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics** 

Mengzhen Liu<sup>1,3</sup> , Enshen Zhou<sup>2,3‡</sup> , Cheng Chi<sup>3</sup> , Yi Han<sup>2,3</sup> , Shanyu Rong<sup>1,3</sup> , Liming Chen<sup>3</sup> , Pengwei Wang<sup>3</sup> , Zhongyuan Wang<sup>3</sup> , Shanghang Zhang<sup>1,3†</sup> 

- 1State Key Laboratory of Multimedia Information Processing, School of Computer Science, Peking University 

2School of Software, Beihang University 3Beijing Academy of Artificial Intelligence 

mengzhenliu25@stu.pku.edu.cn zhouenshen@buaa.edu.cn shanghang@pku.edu.cn 


Figure 1. We propose SaPaVe, an end-to-end active manipulation framework that jointly integrates semantic active perception and activeview execution; the former selectively shifting viewpoints to reveal task-critical cues in cluttered scenes, while the latter grounds newly acquired observations into immediate actions, enabling success even from suboptimal views. **(a)** For instance, grasping the white bowl in _O_ 1 requires rotating the egocentric view, as both fixed ego view and third-person view are occluded. In contrast, targeting the range hood handle ( _O_ 5) only needs a brief upward shift, since precise centering is unnecessary and awkward to reach. **(b)** To address the limitations of fixed-view benchmarks and the cost of real-world trials, we introduce ActiveManip-Bench, a richly annotated benchmark spanning 12 tasks, 100 objects, and 20 diverse scenes. **(c)** On this benchmark, SaPaVe outperforms all baselines with an average success rate of 75.2%. 

## **Abstract** 

_Active perception and manipulation are crucial for robots to interact with complex scenes. Existing methods struggle to unify semantic-driven perception actively with robust, viewpoint-invariant execution accordingly. To this end, we propose SaPaVe, an end-to-end framework that jointly learns these capabilities in a data-efficient manner. Central to our approach is a decoupling of camera and manipulation actions, contrary to shared-action-space, and learning in a bottom-up strategy: we first train semantic camera control on our proposed large-scale dataset, then jointly optimizes both action types via hybrid data. To support this, we introduce ActiveViewPose-200K, comprising_ 

_200k image-language-camera movement pairs for semantic camera movement learning, and a 3D geometry-aware module that improves execution robustness under dynamic viewpoints. We further present ActiveManip-Bench, the first benchmark filling the gap to evaluate active manipulation. Extensive experiments in both simulation and real-world settings show that SaPaVe outperforms recent VLA models such as GR00T N1 and π_ 0 _, achieving up to 31.25% higher success rates in real-world tasks. Our results show that tightly coupled perception and execution, when trained with decoupled yet coordinated strategies, enable efficient and generalizable active manipulation. Please see the project page at https://lmzpai.github.io/SaPaVe._ 

> _†_ Corresponding author _‡_ Project leader 

37164 

## **1. Introduction** 

It is a long-lasting goal to create embodied agents that can actively perceive complex, dynamic scenes and act accordingly in a human-like manner [19, 46]. Achieving such active manipulation is challenging, as it demands two distinct yet complementary abilities, _semantic active perception_ and _active-view execution_ , as shown in Fig. 1. The former involves strategically adjusting viewpoints to acquire relevant information in cluttered scenes ( _e.g._ , shifting the ego-view to reveal a bowl hidden inside a cabinet, reducing occlusions). The latter grounds newly obtained perceptual cues into immediate actions, ensuring successful task completion, even from suboptimal viewpoints ( _e.g._ , briefly glancing upward to locate a range hood handle without centering it is sufficient to initiate interaction). Crucially, effective active manipulation hinges on the tight coupling of these two abilities, enabling the agent to perceive purposefully and act meaningfully, with both informing each other in real time. 

Recent advances in Vision-Language Models (VLMs) [10, 25, 48, 53] have improved semantic instruction understanding. A common approach leverages VLMs for _active perception_ by formulating it as a Visual Question Answering (VQA) task, selecting the best viewpoint from a discrete set of candidates [37, 43]. However, this discretization hinders fine-grained camera control and manipulation, as it fails to connect high-level semantics with the continuous camera pose space. End-to-end Vision-LanguageAction (VLA) models [5, 6] aim to bridge this gap, but are typically trained on fixed near-optimal head-camera views, making them sensitive to viewpoint shifts and limiting their robustness in _active-view execution_ . Moreover, collecting additional data with both head-camera and action labels in the real world [9, 31, 51, 52] is expensive and constrained, so simply fine-tuning VLA models in a unified action space leads to conflicts and suboptimal performance. 

In this work, we introduce **SaPaVe** ( **S** emantic **a** ctive **P** erception and **a** ctive- **V** iew **e** xecution), an end-to-end active manipulation framework that can achieve semantic active perception and active-view execution simultaneously, not only benefiting from the semantic power of VLMs, but also enjoying control over both head camera and manipulation actions in a data-efficient manner. Our key insight is that camera movement is embodiment-agnostic and easier to learn, and we design a bottom-up learning strategy: we first learn camera movement independently using a largescale dataset, then jointly optimize camera movement and other action generation via a decoupled action space using a mix of manipulation datasets. This decoupling minimizes cross-interference and allows each action type to benefit from specific data. 

To be specific, we first propose **ActiveViewPose-200K** , a high-quality dataset comprising 200k image-language and camera movements pairs, enriched with highly detailed se- 

mantic annotations to enable task-oriented camera movement learning. In the first stage, we use this dataset to supervise only camera movement and introduce a camera adapter to retain semantic camera movement knowledge to support _active perception_ . Meanwhile, we design a simple yet effective universal spacial knowledge injection approach to 3D geometry information, supporting _active-view execution_ learning in the second stage, even under dynamic viewpoint changes induced by active perception. In this second stage, we leverage diverse hybrid data to achieve robust, semantically grounded active manipulation, guided by the pretrained camera adapter, with high data efficiency. 

To comprehensively evaluate SaPaVe, we conduct extensive experiments in both simulation and real-world settings. First, we assess our semantic active perception capability on the ActiveViewPose-200K and surpass Gemini 2.5 Pro [10] by 16% despite having only 2B parameters. To address the limitations of fixed-viewpoint manipulation evaluation, we introduce the first simulated active manipulation benchmark, featuring 12 richly annotated tasks across 100 objects and 20 diverse scenes. On this benchmark, our model achieves the best performance, even surpassing fixed-view VLA ( _e.g._ , GR00T-N1 [5]) by an absolute 58% success rate. Moreover, we collect real-world active manipulation data and directly fine-tune existing VLA models (e.g., _π_ 0 [6], GR00T-N1 [5]) with a unified action space. Our model still outperforms these baselines, exceeding _π_ 0 by 40% and GR00T-N1 by 31.25%. In summary, our contributions are threefold: 

- We propose **SaPaVe** , a novel end-to-end framework that first achieves active manipulation with a bottom-up learning strategy in a data-efficient way. 

- We introduce **ActiveViewPose-200K** , a well-annotated dataset tailored for learning semantic camera control, and **ActiveManip-Bench** , the first benchmark that fills the gap in evaluating active manipulation. 

- Extensive experiments show that **SaPaVe** excels in active perception and showcases impressive active manipulation capability in simulation and real-world settings. 

## **2. Related Work** 

**Active Perception and Manipulation.** Active perception and manipulation [3, 46] is a long-standing research area in robotics and computer vision. Traditionally, this problem is formulated as a Next-Best-View (NBV) task [4, 7, 11, 16, 18, 34, 54], where an agent iteratively selects a viewpoint to maximize an information gain metric. However, these methods often rely on non-end-to-end pipelines and lack semantic input, rendering them computationally prohibitive and incapable of adapting to diverse, semantically rich tasks. With the advent of VLMs [1, 10, 14, 36, 39– 41, 48, 55–58], recent works have explored new paradigms. Some regard active perception as a VQA task [37, 43], 

37165 

where a VLM evaluates a discrete set of candidate camera motions to select the optimal one. A significant limitation of this approach is its inability to operate within a continuous camera motion space, constraining the agent’s flexibility. To address this, the rapid development of VLA models [5, 6, 20–24] has spurred interest in end-to-end solutions that jointly model camera control and manipulation actions. Nevertheless, directly augmenting the action space of a VLA to include continuous camera movement [49, 52] exacerbates the demand for large-scale training data. Such demonstration data, featuring concurrent camera movement and manipulation, is exceptionally scarce, hindering the model’s ability to acquire a genuine active manipulation capability. In contrast, our work proposes a bottom-up, endto-end strategy that endows policies with active manipulation skills in a data-efficient manner. 

**VLA for Robotics.** VLA has made significant strides in recent years. However, The majority existing VLA models [5, 27–29], are trained and evaluated under the assumption of a fixed camera viewpoint that is near-optimal. This setting largely overlooks the critical necessity of active perception for handling visual ambiguity and occlusions in real-world scenarios. While some concurrent works [49, 52] attempt to naively finetune VLA for both camera and other control, they face two primary challenges. **(1)** Data Scarcity: Existing VLA training datasets [8, 35, 44] mainly consist of demonstrations from a fixed perspective. The high cost and complexity of collecting active perception and manipulation data in the real world make it difficult to scale. **(2)** Lack of 3D Geometric Awareness: Current VLA models [6, 38] often fail to fully leverage 3D geometric priors. This makes them highly sensitive to camera perturbations and unable to reason effectively under viewpoint changes. To address these challenges, we propose a data-efficient training strategy that systematically incorporates diverse 3D geometric priors, which augment active manipulation capabilities and fortify the model’s robustness against viewpoint variations. 

**Benchmarks for Active Perception and Manipulation.** Existing active perception and manipulation studies are primarily evaluated in real-world using a single robot arm with a wrist-mounted camera [7, 13, 30, 37, 43, 50, 54], a humanoid robot equipped with a customized 2-DoF head [9, 19, 49, 51, 52], or a humanoid robot with a modified 6-DoF head [46]. However, such evaluations are difficult to reproduce due to the inherent challenges in replicating identical real-world experimental setups. In contrast, simulation environments [32, 42, 45] offer perfect reproducibility and standardized testbeds. However, the vast majority of existing simulation-based benchmarks [26, 33] are restricted to fixed camera viewpoints. Consequently, there is currently a noticeable absence of established benchmarks specifically designed for evaluating active perception. To bridge this gap, we propose the first simulation benchmark specifically 

designed for evaluating active manipulation. 

## **3. Method** 

We first formulate the active manipulation task (Sec. 3.1). Then, we elaborate on SaPaVe, including its architecture (Sec. 3.2) and training strategies (Sec. 3.3). Finally, we describe the construction of ActiveViewPose-200K dataset and details about ActiveManip-Bench (Sec. 3.4). 

### **3.1. Problem Formulation** 

We define the active manipulation task as learning a policy _πθ_ : _O × L →A_ . Given an observation _Ot ∈O_ and a language instruction _L ∈L_ , the policy predicts a joint action trajectory _At_ = _{A_ head _,t, A_ other _,t} ∈A_ . At each timestep _t_ , the observation _Ot_ comprises the current RGB image _It ∈_ R<sup>_H×W ×_3</sup> and optional 3D geometric information _Gt_ ( _e.g._ , depth maps and camera intrinsics/extrinsics). To ensure temporal consistency and smooth execution, we adopt an action chunking strategy where the policy predicts an action sequence over a horizon _k_ . The head camera action sequence is defined as _A_ head _,t_ = _{a_ head<sup>_τ}_</sup> _τ_<sup>_t_+</sup> =<sup>_k_</sup> _t_<sup>_−_1</sup> , where each _a_<sup>_τ_</sup> head<sup>_∈_R2 represents the relative pitch and yaw</sup> adjustments of the robot’s head. Similarly, the manipulation action sequence is denoted as _A_ other _,t_ = _{a_ other<sup>_τ}_</sup> _τ_<sup>_t_+</sup> =<sup>_k_</sup> _t_<sup>_−_1</sup> . Specifically, for our platform—a Unitree G1 humanoid equipped with dual 7-DoF arms and dual 6-DoF Inspire hands—each _a_<sup>_τ_</sup> other<sup>_∈_R26representsthe26-DoFjointpo-</sup> sition deltas at timestep _τ_ , specifying the relative angular change for each controllable joint. 

Unlike prior works that unify camera motion and manipulation into a single action space, we decouple them and propose a two-stage learning strategy for active manipulation. This approach first enrich the model with semantic active perception priors in a data-efficient way, and further optimize both camera control and manipulation actions for effective active-view execution in bottom-up manner. Moreover, our observation space includes diverse 3D geometric inputs, enabling the model to acquire strong spatial understanding and more resilient to viewpoint changes. Therefore, our model excels in complex active manipulation tasks with strong semantic-aware perception. 

### **3.2. Architecture** 

Effective active manipulation requires both semantic active perception and robust active-view execution. However, we find that existing active manipulation approaches do not support semantic input [7, 46, 54]. Moreover, a straightforward fine-tuning of existing VLA models [5, 6] is insufficient. First, directly adding camera movement into the existing VLA action space would break the large-scale fixed-view manipulation priors learned from previous training. Second, this disruption to such priors increases data demands, making it difficult to scale up due to the high 

37166 


Figure 2. **Overview of SaPaVe** . SaPaVe can process RGB images and task instructions and output camera movement and manipulation actions in a decoupled action space. This decoupled design enables the model to achieve active manipulation via a bottom-up, two-stage training strategy: First, large-scale embodiment-agnostic camera control data fosters _semantic active perception_ , which is encoded as prior knowledge in a camera adapter. Second, mixed data together with Universal Spatial Knowledge Injection flexibly incorporate various geometric configurations ( _e.g._ , absolute depth, camera intrinsics), thereby enhancing spatial precision for _active-view execution_ . 

cost and time-consuming nature of real-world data collection [9, 49, 52]. Therefore, we propose _Decoupled Action Heads and Camera Adapter_ to enable our model to acquire rich semantic active perception priors and retain general manipulation knowledge in a data-efficient manner. Meanwhile, existing VLA methods often exhibit insufficient view-invariant 3D geometric consistency, hindering their ability to generate temporally stable action chunks under an actively changing egocentric perspective. To bridge this gap, we propose _Universal Spatial Knowledge Injection_ , which efficiently leverages as much 3D information as possible to directly optimize the action output. 

**Decoupled Action Heads and Camera Adapter.** We design two parts. **(1)** Camera Adapter: We add a Camera Adapter using LoRA [15] on the VLM to learn semantic active perception priors without altering the original VLM’s weights. It is trained on a large-scale semantic camera movement dataset (see Sec. 3.4) to enhance the model’s semantic active perception capabilities. **(2)** Decoupled Action Head: In Fig. 2, we design two decoders to decouple camera movement from other actions. This simple, lightweight decoupling approach enables the model to quickly learn ac- 

curate camera movements and other actions. 

**Universal Spatial Knowledge Injection.** A most straightforward approach to enhance VLA’s 3D spatial perception and understanding is to introduce as much accurate 3D information as possible. Therefore, we propose a Universal Spatial Knowledge Injection approach that supports the optional inclusion of arbitrary varieties of 3D geometry information and injects them into the action head to guide the action-decoding process. As shown in Fig. 2, we adopt a Universal Spatial Encoder inherited from a powerful feedforward 3D geometry model [17]. This encoder can support a wide range of 3D geometry configurations as inputs without requiring retraining or architectural modifications. The encoded spatial tokens are element-wise added to the VLM output tokens, and then the mixed tokens are injected into the Decoupled Action Head during the action denoising process. In this way, it not only strengthens semantic camera movement but also enhances active-view execution. 

### **3.3. Two-Stage Training Strategy** 

We design a two-stage training strategy to equip our model with semantic active perception and active-view execution 

37167 


Figure 3. **Overview of ActiveViewPose-200K** . It is a high-quality dataset comprising 200k image-language and camera movement pairs, enriched with highly detailed semantic annotations to enable semantic camera movement learning. 

to achieve active manipulation in a bottom-up manner. 

**Stage 1: Semantic Active Perception Alignment.** Our goal is to first equip the model with sufficient semantic active perception priors, which requires a large amount of high-quality data. However, existing datasets are all collected from a fixed near-optimal view. To fill this gap, we propose a large-scale, high-quality dataset, ActiveViewPose-200K, comprising 200k image-language and camera movement pairs (see Sec. 3.4). We thus use this dataset to train Camera Adapter and Camera Action Decoder by supervising camera movement (see Fig. 2). The objective is to minimize the Mean Squared Error between the predicted ego camera movement _A_ head and the groundtruth _A_<sup>_∗_</sup> head,t<sup>,definedas</sup><sup>_L_stage1=</sup><sup>_L_MSE(</sup><sup>_A_head,t</sup><sup>_,A∗_</sup> head,t<sup>)</sup><sup>_._</sup> Upon completion, the model develops a robust prior for semantic active perception. 

**Stage 2: Active Manipulation Fine-tuning.** Building upon the semantic active perception prior, this stage trains the model to perform effective active manipulation. The data is a mixture of ActiveViewPose-200K and active manipulation robot data (See Sec. 3.4). We freeze the Camera Adapter and train the Decoupled Action Head using MSE loss, such that _L_ stage2 = _λ_ head _L_ head + _λ_ other _L_ other _,_ Therefore, the model acquires comprehensive active manipulation skills. More details can be found in the Appx. E. 

### **3.4. ActiveViewPose-200K and ActiveManip-Bench** 

**ActiveViewPose-200K Dataset.** Existing large-scale robotics datasets [35, 44] have been instrumental in advancing policy learning. However, they are predominantly composed of data collected from nearly optimal fixed camera viewpoints. To fill this gap, we introduce ActiveViewPose200K, the first large-scale, high-quality semantic active perception dataset, comprising 200k image-language and optimal camera movement pairs. We construct this dataset through an efficient semi-automatic process. First, we meticulously collected 4k high-quality, semantically annotated assets from Objaverse [12] and collected 500 diverse scenes. Next, we use a heuristic algorithm to produce a large number of image-to-camera movement pairs. Meanwhile, we semi-automatically built 3,000 detailed task templates. These templates, along with the images, are sent to GPT-4o to generate relevant instructions, which are then manually refined. This data collection process is highly efficient and cost-effective, and can be used to train and evaluate the model’s semantic active perception capability. 

**ActiveManip-Bench.** Following the bottom-up strategy, after we equip our model with sufficient semantic active perception priors, we need a benchmark for both training and evaluating our model’s active manipulation capability. However, existing simulation benchmarks [26, 33, 45] are 

37168 


Figure 4. **Overview of ActiveManip-Bench** : It is the first simulation benchmark to evaluate active manipulation beyond traditional fixedview settings. ActiveManip-Bench features 12 richly annotated tasks across 100 objects and 20 diverse scenes. 

Table 1. The performance of semantic active perception evaluation. We report the success rate (%) compared to current general VLMs and specialized spatial VLMs. 

|**Method**|**Val**|**Test1**|**Test2**|**Avg.**|
|---|---|---|---|---|
|Qwen2.5-VL-72B [2]|63.9|65.1|58.0|62.3|
|Multi-SpatialMLLM [47]|72.8|74.3|63.6|70.2|
|Gemini-2.5-Pro [10]|73.3|76.5|68.2|72.7|
|**Ours (Stage 1)**|**85.5**|**89.1**|**78.3**|**84.3**|


active manipulation priors can our model actually acquire (Sec. 4.2) ? **(2)** Where and to what extent does our active camera design improve upon previous fixed-camera or wrist-camera setups (Sec. 4.3)? **(3)** Compared to existing VLA models, how does our model architecture enhance active manipulation capabilities (Sec. 4.4)? **(4)** How well does our model generalize to out-of-distribution (OOD) scenarios (Sec. 4.5)? **(5)** What role do each of the system components play in enhancing its overall performance (Sec. 4.6)? 

### **4.1. Experimental Setup** 

all confined to a fixed view and do not evaluate this capability. To meet our requirements, we are the first to propose an Active Manipulation benchmark named ActiveManipBench. ActiveManip-Bench is built on NVIDIA Isaac Sim and features a G1 humanoid equipped with a pair of Inspire Hands and an active, head-mounted perception camera. ActiveManip-Bench now covers 100 different objects distributed across 20 distinct scenes, featuring 12 semantic active manipulation tasks with rich and detailed annotations. It is also designed to be easily extensible, allowing for the simple addition of new scenes and objects. More details can be found in the Appx. C 

## **4. Experiments** 

In this section, we conduct a series of experiments to rigorously evaluate our proposed framework. We want to answer the following key questions: **(1)** How much semantic 

**Datasets and Benchmarks.** We design a series of experiments leveraging different components of our dataset and benchmarks: **(1)** For the first experiment to evaluate semantic active perception (Sec. 4.2), we test models on our ActiveViewPose-200K, which is split into Train/Val/Test1/Test2. In Test1, the language instructions contain explicit positional indicators ( _e.g._ , “on the left”), whereas in Test2, the instructions omit detailed camera movements, requiring the model to infer them from both the text and the image. **(2)** For the second experiment to evaluate the effect of fixed or dynamic cameras across different types (Sec. 4.3), we assess performance on ActiveManip-Bench (see Sec. 3.4), which comprises 6 task types: Unoccluded/Occluded/Out-of-View Pick-andPlace, as well as Unoccluded/Occluded/Out-of-View Articulated Manipulation. **(3)** For All subsequent experiments (Sec. 4.3, Sec. 4.4, Sec. 4.6), we employ our real- 

37169 

Table 2. Evaluation results for fixed and dynamic cameras in simulation of ActiveManip-Bench. We report the success rate (%) compare to different camera configurations with the same architecture. P.a.P and A.M denote Pick-and-Place and articulated Manipulation. 

|Method|Unoccluded P.a.P|Occluded P.a.P|Out-of-View P.a.P|Unoccluded A.M|Occluded A.M|Out-of-View A.M|Avg.|
|---|---|---|---|---|---|---|---|
|Fixed Camera|74|46|11|52|27|7|36.17|
|Fixed Camera + Wrist Camera|83|62|28|66|51|24|52.33|
|Active Camera + Wrist Camera|**86**|75|70|74|68|66|73.16|
|**Ours(Active Camera)**|85|**78**|**72**|**76**|**70**|**68**|**74.83**|


Table 3. Performance on active manipulation in real-world settings. We report the success rate (%) compared to the existing VLA models. Our approach achieves the best performance. 

|Method|Occluded<br>Pick-and-Place|Out-of-View<br> Pick-and-Place|Occluded<br> Arti-Manip|Out-of-View <br>Arti-Manip|Avg.|
|---|---|---|---|---|---|
|_π_0 [6]|55|45|45|35|45.00|
|GR00T-N1 [5]|60|55|50|50|53.75|
|**Ours**|**90**|**85**|**85**|**80**|**85.00**|


robot teleoperated dataset, including 4 task categories: Occluded/Out-of-View Pick-and-Place, and Occluded/Outof-View Articulated Manipulation. See Appx. D for details. 

**Baselines.** We compare our method against several strong baselines: **(1)** In the first experiment, we compare our model with current powerful VLM, including the general models ( _e.g._ , Qwen2.5-VL-72B [2], Gemini-2.5-Pro [10]), as well as the specialized spatial VLM ( _e.g._ , MultiSpacialMLLM [47]). **(2)** In the second experiment, we adopt the same underlying architecture but explore different camera configurations: (a) Fixed Camera: A standard VLA model that operates from a static camera—this is the most common setup in prior work. We use our model but keep the head camera fixed. (b) Fixed Camera + Wrist Camera: We again use our model with a fixed head camera and introduce two wrist cameras. (c) Active Camera + Wrist Camera: We use our model, combining the active head camera with two wrist cameras. **(3)** Finally, in the third experiment, we compare our model with existing VLA baselines, _π_ 0 [6] and GR00T-N1 [5], both of which are recognized for their strong general-purpose capabilities. 

**Evaluation Metrics.** For all experiments, we report the success rate. For the first experiment, a prediction is considered successful if it falls within a tolerance of the groundtruth pitch and yaw changes (See Appx. A). 

### **4.2. Semantic Active Perception Evaluation** 

We evaluate our model on the ActiveViewPose-200K test sets and present the following findings. As shown in Table 1, our model significantly outperforms powerful VLMs across all test splits, especially on test2, where semantic understanding is paramount. Notably, our model achieves an average score 11.6% higher than Gemini-2.5-Pro [10] with only 2B parameters. This is because the generalist VLMs struggle to translate abstract instructions into precise camera poses, whereas our specialized training yields a much more accurate and robust perception policy. It demonstrates 

that acquiring an embodied skill like semantic active perception is not an emergent property of generalist VLMs. Instead, direct training on specialized data, as enabled by our ActiveViewPose dataset, is crucial for learning a functional and precise policy. 

### **4.3. Fixed and Dynamic Cameras Evaluation.** 

We conduct this evaluation using ActiveManip-Bench in simulation. The following paragraphs present our analyses. 

**Dynamic viewpoints are crucial in active manipulation.** In Tab. 2, under a fixed viewpoint, the success rates of unoccluded, occluded, and out-of-view tasks all decrease substantially—especially for the Out-of-View task, which drops by more than 60%. This result indicates that a fixed camera greatly limits the model’s ability to explore the accessible space, leading to failures for active manipulation. 

**The combination of Fixed camera and Wrist camera remains insufficient for active manipulation.** We observe that, although this setup outperforms using a single fixed camera setting, it still falls short of active camera setting in every task—especially out-of-view tasks, which heavily depend on the model’s ability to rotate the main viewpoint for active perception of the environment. Since the fixed main viewpoint can never observe all objects, this combination fails to address active manipulation tasks. 

**The gain from combining an active camera with a wrist camera is minimal and can even degrade certain performance metrics.** This outcome may seem counterintuitive, as one would expect more viewpoints to yield better results. However, we find that if the model already possesses robust dynamic perception ( _i.e._ , the ability to avoid occlusions and observe effectively) and strong 3D spatial understanding, adding additional dynamic viewpoints does not necessarily improve performance in active manipulation tasks. 

### **4.4. Comparison with existing VLA models** 

We compare our model with existing VLAs whose action spaces are extended to incorporate camera movement. Both are fine-tuned for active manipulation tasks. 

**Directly fine-tuning existing VLA models is insufficient to fully address active manipulation tasks** In Tab. 3, both GR00T-N1 and _π_ 0 underperform our approach in nearly all tasks. Two main factors account for this shortfall: **(1)** Direct VLA fine-tuning does not provide sufficient active perception priors. **(2)** Current VLA models lack dedicated mod- 

37170 

Table 4. Performance on generalization ability evaluation. We report the success rate (%). Our model demonstrates robust generalization when performing active manipulation across unseen objects, varying lighting conditions, and diverse scenes. 

|**Task Name**|**Object 1**|**Object 2 **|**Light 1**|**Light 2**|**Scene 1**|**Scene 2 **|**Original**|
|---|---|---|---|---|---|---|---|
|Occluded<br>Pick-and-Place|85|90|90|95|90|85|**90**|
|Out-of-View<br>Pick-and-Place|85|90|80|90|85|85|**85**|
|Occluded<br>Arti-Manip|80|85|80|85|85|80|**85**|
|Out-of-View<br>Arti-Manip|75|80|80|85|80|75|**80**|


ules for enhancing active-view manipulation. These observations validate the necessity of our work. 

**Our bottom-up strategy proves to be highly effective.** In Tab. 3, our bottom-up approach significantly outperforms direct VLA fine-tuning, demonstrating that first establishing robust semantic active perception priors and then learning active manipulation tasks is extremely effective. Meanwhile, the decoupled action head benefits more fully from this two-stage training strategy, thereby enhancing the model’s active manipulation capability. 

### **4.5. Generalization Ability Evaluation.** 

We evaluate our model’s generalization ability in two realworld tasks, examining variations in lighting, objects, and operational backgrounds. As shown in Tab. 4, our model demonstrates strong generalization to previously unseen objects, indicating robust high-level semantic understanding that enables it to interpret out-of-distribution objects and correctly follow instructions. Meanwhile, across different lighting conditions and scenarios, the model continues to exhibit strong generalization, suggesting that incorporating 3D information bolsters its 3D spatial perception and ensures reliably robust operations in diverse environments. 

### **4.6. Ablation Studies** 

We conduct a series of ablation experiments on 4 real-world tasks to evaluate the effectiveness of different components in our method. We present our analyses below. 

**The bottom-up training strategy is crucial for active manipulation tasks.** Tab. 5 indicates that both training stages substantially improve the model’s performance. In particular, for out-of-view tasks, omitting Stage 1 drastically reduces the success rate—by half in artifact manipulation—showing that first equipping the model with semantic active perception priors is essential for completing active manipulation tasks. Meanwhile, omitting Stage 2 reduces the model’s overall success rate, underscoring the necessity of active manipulation finetuning. 

**The decoupled formulation is correct.** We find that using 

Table 5. Ablation Study on the effect about training strategy of Stage 1 and Stage2, decoupled action head (D.A.H.), camera adapter (C.A.), and universal spatial knowledge injection (U.S.K.I). We report the avarage success rate (%). 

|Ablti|Occluded|Out-of-View|Occluded|Out-of-View|A|
|---|---|---|---|---|---|
|aon|Pick-and-Place|Pick-and-Place|Arti-Manip|<br>Arti-Manip|vg.|
|w/o. Stage 1|65|55|50|45|53.75|
|w/o. Stage 2|75|60|70|60|66.25|
|w/o. D.A.H.|80|70|70|65|71.25|
|w/o. C.A.|80|75|70|70|73.75|
|w/o. U.S.K.I.|75|75|65|60|68.75|


a unified single action decoder for simultaneously learning camera movement and other actions, compared to using a decoupled approach, weakens the model’s active manipulation ability. This is mainly because camera movement is inherently embodiment-agnostic. Forcing the use of a unified action decoder couples the two training stages in the action space, not only disrupting the semantic active perception priors but also impairing the active manipulation capability. 

**Using a lightweight camera adapter to learn camera movement proves superior to fully finetuning.** As shown in Tab. 5, comparing the Camera Adapter approach with fully finetuning reveals that fully finetuning leads to performance drops across all four experiments. This suggests that the camera adapter can learn camera rotation while preserving the VLM’s general high-level semantic information, a crucial factor for maintaining the model’s fundamental understanding of active manipulation tasks. 

**Universal Spatial Knowledge Injection greatly enhances the model’s robustness for basic operations under active views** . In Tab. 5, we observe that omitting Universal Spatial Knowledge Injection leads to a 15% performance drop even in relatively simple Occluded Pick-and-Place tasks. This indicates that maintaining a consistent 3D spatial understanding is critical for active manipulation. It further underscores how Universal Spatial Knowledge Injection effectively guides the model’s action output, since prior 3D knowledge can facilitate implicit 3D learning. 

## **5. Conclusion** 

In this paper, we propose SaPaVe, an end-to-end framework that unifies semantic active perception with active-view execution for active manipulation. By first leveraging largescale semantic camera control data, we use a decoupled action space to learn semantic active perception, acquired as prior knowledge in a camera adapter. We then integrate Universal Spatial Knowledge Injection to handle arbitrary geometric inputs, improving active-view execution. Moreover, we present ActiveViewPose-200K, a large-scale dataset for semantic camera learning, and ActiveManip-Bench, a tailored benchmark for active manipulation. Extensive experiments show the effectiveness of SaPaVe and highlight its potential for human-like robots. 

37171 

## **Acknowledgement** 

This work was supported by the National Natural Science Foundation of China (62476011), and by the Beijing Natural Science Foundation (L252060). We sincerely thank Yuran Wang and Xinqiang Yu for their insightful discussions and valuable feedback regarding the development of our simulation environment. We are also grateful to Yibo Li for refining the teaser figure, and to Zhengliang Cai, Ning Chen, Yangyang Wei and Yankai Fu for their indispensable support with the real-world experiments, particularly in troubleshooting and repairing the robot hardware. 

## **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 2 

- [2] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen, Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei Ding, Chang Gao, Chunjiang Ge, et al. Qwen3-vl technical report. _arXiv preprint arXiv:2511.21631_ , 2025. 6, 7 

- [3] Ruzena Bajcsy. Active perception. _Proceedings of the IEEE_ , 76(8):966–1005, 1988. 2 

- [4] Andreas Bircher, Mina Kamel, Kostas Alexis, Helen Oleynikova, and Roland Siegwart. Receding horizon” nextbest-view” planner for 3d exploration. In _2016 IEEE international conference on robotics and automation (ICRA)_ , pages 1462–1468. IEEE, 2016. 2 

- [5] Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 2, 3, 7 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control, 2026. 2, 3, 7 

- [7] Michel Breyer, Lionel Ott, Roland Siegwart, and Jen Jen Chung. Closed-loop next-best-view planning for targetdriven grasping. In _2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1411–1416. IEEE, 2022. 2, 3 

- [8] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025. 3 

- [9] Xuxin Cheng, Jialong Li, Shiqi Yang, Ge Yang, and Xiaolong Wang. Open-television: Teleoperation with immersive active visual feedback. _arXiv preprint arXiv:2407.01512_ , 2024. 2, 3, 4 

- [10] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 2, 6, 7 

- [11] Cl Connolly. The determination of next best views. In _Proceedings. 1985 IEEE international conference on robotics and automation_ , pages 432–435. IEEE, 1985. 2 

- [12] Matt Deitke, Dustin Schwenk, Jordi Salvador, Luca Weihs, Oscar Michel, Eli VanderBilt, Ludwig Schmidt, Kiana Ehsani, Aniruddha Kembhavi, and Ali Farhadi. Objaverse: A universe of annotated 3d objects. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 13142–13153, 2023. 5 

- [13] Yankai Fu, Qiuxuan Feng, Ning Chen, Zichen Zhou, Mengzhen Liu, Mingdong Wu, Tianxing Chen, Shanyu Rong, Jiaming Liu, Hao Dong, et al. Cordvip: Correspondence-based visuomotor policy for dexterous manipulation in real-world. _arXiv preprint arXiv:2502.08449_ , 2025. 3 

- [14] Yi Han, Cheng Chi, Enshen Zhou, Shanyu Rong, Jingkun An, Pengwei Wang, Zhongyuan Wang, Lu Sheng, and Shanghang Zhang. Tiger: Tool-integrated geometric reasoning in vision-language models for robotics. _arXiv preprint arXiv:2510.07181_ , 2025. 2 

- [15] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Liang Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _Iclr_ , 1(2):3, 2022. 4 

- [16] Stefan Isler, Reza Sabzevari, Jeffrey Delmerico, and Davide Scaramuzza. An information gain formulation for active volumetric 3d reconstruction. In _2016 IEEE international conference on robotics and automation (ICRA)_ , pages 3477– 3484. IEEE, 2016. 2 

- [17] Nikhil Keetha, Norman M¨uller, Johannes Sch¨onberger, Lorenzo Porzi, Yuchen Zhang, Tobias Fischer, Arno Knapitsch, Duncan Zauss, Ethan Weber, Nelson Antunes, et al. Mapanything: Universal feed-forward metric 3d reconstruction. _arXiv preprint arXiv:2509.13414_ , 2025. 4 

- [18] Michael Krainin, Brian Curless, and Dieter Fox. Autonomous generation of complete 3d object models using next best view manipulation planning. In _2011 IEEE international conference on robotics and automation_ , pages 5031– 5037. IEEE, 2011. 2 

- [19] Jialong Li, Xuxin Cheng, Tianshu Huang, Shiqi Yang, RiZhao Qiu, and Xiaolong Wang. Amo: Adaptive motion optimization for hyper-dexterous humanoid whole-body control. _arXiv preprint arXiv:2505.03738_ , 2025. 2, 3 

- [20] Zhe Li, Yisheng He, Lei Zhong, Weichao Shen, Qi Zuo, Lingteng Qiu, Zilong Dong, Laurence Tianruo Yang, and Weihao Yuan. Mulsmo: Multimodal stylized motion generation by bidirectional control flow. _arXiv preprint arXiv:2412.09901_ , 2024. 3 

- [21] Zhe Li, Weihao Yuan, Yisheng He, Lingteng Qiu, Shenhao Zhu, Xiaodong Gu, Weichao Shen, Yuan Dong, Zilong Dong, and Laurence T Yang. Lamp: Language-motion 

37172 

   - pretraining for motion generation, retrieval, and captioning. _arXiv preprint arXiv:2410.07093_ , 2024. 

- [22] Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Tao Huang, Zhenguo Sun, Yibo Peng, Pengwei Wang, Zhongyuan Wang, Fangzhou Liu, et al. Do you have freestyle? expressive humanoid locomotion via audio control. _arXiv preprint arXiv:2512.23650_ , 2025. 

- [23] Zhe Li, Cheng Chi, Yangyang Wei, Boan Zhu, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, Shanghang Zhang, and Chang Xu. From language to locomotion: Retargeting-free humanoid control via motion latent guidance. _arXiv preprint arXiv:2510.14952_ , 2025. 

- [24] Zhe Li, Cheng Chi, Boan Zhu, Yangyang Wei, Shuanghao Bai, Yuheng Ji, Yibo Peng, Tao Huang, Pengwei Wang, Zhongyuan Wang, et al. Robomirror: Understand before you imitate for video to humanoid locomotion. _arXiv preprint arXiv:2512.23649_ , 2025. 3 

- [25] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ , 2024. 2 

- [26] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36:44776–44791, 2023. 3, 5 

- [27] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Pengju An, Xiaoqi Li, Kaichen Zhou, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. _Advances in Neural Information Processing Systems_ , 37:40085–40110, 2024. 3 

- [28] Jiaming Liu, Mengzhen Liu, Zhenyu Wang, Lily Lee, Kaichen Zhou, Pengju An, Senqiao Yang, Renrui Zhang, Yandong Guo, and Shanghang Zhang. Robomamba: Multimodal state space model for efficient robot reasoning and manipulation. _arXiv preprint arXiv:2406.04339_ , 1(3):5, 2024. 

- [29] Jiaming Liu, Hao Chen, Pengju An, Zhuoyang Liu, Renrui Zhang, Chenyang Gu, Xiaoqi Li, Ziyu Guo, Sixiang Chen, Mengzhen Liu, et al. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. _arXiv preprint arXiv:2503.10631_ , 2025. 3 

- [30] Mengzhen Liu, Mengyu Wang, Henghui Ding, Yilong Xu, Yao Zhao, and Yunchao Wei. Segment anything with precise interaction. In _Proceedings of the 32nd ACM International Conference on Multimedia_ , pages 3790–3799, 2024. 3 

- [31] Chenhao Lu, Xuxin Cheng, Jialong Li, Shiqi Yang, Mazeyu Ji, Chengjing Yuan, Ge Yang, Sha Yi, and Xiaolong Wang. Mobile-television: Predictive motion priors for humanoid whole-body control. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5364–5371. IEEE, 2025. 2 

- [32] Viktor Makoviychuk, Lukasz Wawrzyniak, Yunrong Guo, Michelle Lu, Kier Storey, Miles Macklin, David Hoeller, Nikita Rudin, Arthur Allshire, Ankur Handa, et al. Isaac gym: High performance gpu-based physics simulation for robot learning. _arXiv preprint arXiv:2108.10470_ , 2021. 3 

- [33] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3): 7327–7334, 2022. 3, 5 

- [34] Menaka Naazare, Francisco Garcia Rosas, and Dirk Schulz. Online next-best-view planner for 3d-exploration and inspection with a mobile manipulator robot. _IEEE Robotics and Automation Letters_ , 7(2):3779–3786, 2022. 2 

- [35] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 3, 5 

- [36] Yiran Qin, Enshen Zhou, Qichang Liu, Zhenfei Yin, Lu Sheng, Ruimao Zhang, Yu Qiao, and Jing Shao. Mp5: A multi-modal open-ended embodied system in minecraft via active perception. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16307–16316, 2024. 2 

- [37] Venkatesh Sripada, Samuel Carter, Frank Guerin, and Amir Ghalamzan. Ap-vlm: Active perception enabled by visionlanguage models. _arXiv preprint arXiv:2409.17641_ , 2024. 2, 3 

- [38] Huajie Tan, Sixiang Chen, Yijie Xu, Zixiao Wang, Yuheng Ji, Cheng Chi, Yaoxu Lyu, Zhongxia Zhao, Xiansheng Chen, Peterson Co, et al. Robo-dopamine: General process reward modeling for high-precision robotic manipulation. _arXiv preprint arXiv:2512.23703_ , 2025. 3 

- [39] Huajie Tan, Yuheng Ji, Xiaoshuai Hao, Minglan Lin, Pengwei Wang, Zhongyuan Wang, and Shanghang Zhang. Reason-rft: Reinforcement fine-tuning for visual reasoning. _arXiv e-prints_ , pages arXiv–2503, 2025. 2 

- [40] Huajie Tan, Enshen Zhou, Zhiyu Li, Yijie Xu, Yuheng Ji, Xiansheng Chen, Cheng Chi, Pengwei Wang, Huizhu Jia, Yulong Ao, et al. Robobrain 2.5: Depth in sight, time in mind. _arXiv preprint arXiv:2601.14352_ , 2026. 

- [41] BAAI RoboBrain Team, Mingyu Cao, Huajie Tan, Yuheng Ji, Minglan Lin, Zhiyu Li, Zhou Cao, Pengwei Wang, Enshen Zhou, Yi Han, et al. Robobrain 2.0 technical report. _arXiv preprint arXiv:2507.02029_ , 2025. 2 

- [42] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 3 

- [43] Hecheng Wang, Jiankun Ren, Jia Yu, Lizhe Qi, and Yunquan Sun. Roboretriever: Single-camera robot object retrieval via active and interactive perception with dynamic scene graph. _arXiv preprint arXiv:2508.12916_ , 2025. 2, 3 

- [44] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multiembodiment intelligence normative data for robot manipulation. _arXiv preprint arXiv:2412.13877_ , 2024. 3, 5 

- [45] Fanbo Xiang, Yuzhe Qin, Kaichun Mo, Yikuan Xia, Hao Zhu, Fangchen Liu, Minghua Liu, Hanxiao Jiang, Yifu Yuan, 

37173 

He Wang, et al. Sapien: A simulated part-based interactive environment. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 11097– 11107, 2020. 3, 5 

- [46] Haoyu Xiong, Xiaomeng Xu, Jimmy Wu, Yifan Hou, Jeannette Bohg, and Shuran Song. Vision in action: Learning active perception from human demonstrations. _arXiv preprint arXiv:2506.15666_ , 2025. 2, 3 

Huang, Lu Sheng, et al. Roborefer: Towards spatial referring with reasoning in vision-language models for robotics. _arXiv preprint arXiv:2506.04308_ , 2025. 

   - [58] Enshen Zhou, Cheng Chi, Yibo Li, Jingkun An, Jiayuan Zhang, Shanyu Rong, Yi Han, Yuheng Ji, Mengzhen Liu, Pengwei Wang, et al. Robotracer: Mastering spatial trace with reasoning in vision-language models for robotics. _arXiv preprint arXiv:2512.13660_ , 2025. 2 

- [47] Runsen Xu, Weiyao Wang, Hao Tang, Xingyu Chen, Xiaodong Wang, Fu-Jen Chu, Dahua Lin, Matt Feiszli, and Kevin J Liang. Multi-spatialmllm: Multi-frame spatial understanding with multi-modal large language models. _arXiv preprint arXiv:2505.17015_ , 2025. 6, 7 

- [48] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_ , 2025. 2 

- [49] Justin Yu, Yide Shentu, Di Wu, Pieter Abbeel, Ken Goldberg, and Philipp Wu. Egomi: Learning active vision and whole-body manipulation from egocentric human demonstrations. _arXiv preprint arXiv:2511.00153_ , 2025. 3, 4 

- [50] Chengbo Yuan, Rui Zhou, Mengzhen Liu, Yingdong Hu, Shengjie Wang, Li Yi, Chuan Wen, Shanghang Zhang, and Yang Gao. Motiontrans: Human vr data enable motion-level learning for robotic manipulation policies. _arXiv preprint arXiv:2509.17759_ , 2025. 3 

- [51] Yanjie Ze, Siheng Zhao, Weizhuo Wang, Angjoo Kanazawa, Rocky Duan, Pieter Abbeel, Guanya Shi, Jiajun Wu, and C Karen Liu. Twist2: Scalable, portable, and holistic humanoid data collection system. _arXiv preprint arXiv:2511.02832_ , 2025. 2, 3 

- [52] Qiyuan Zeng, Chengmeng Li, Jude St John, Zhongyi Zhou, Junjie Wen, Guorui Feng, Yichen Zhu, and Yi Xu. Activeumi: Robotic manipulation with active perception from robot-free human demonstrations. _arXiv preprint arXiv:2510.01607_ , 2025. 2, 3, 4 

- [53] Qizhe Zhang, Mengzhen Liu, Lichen Li, Ming Lu, Yuan Zhang, Junwen Pan, Qi She, and Shanghang Zhang. Beyond attention or similarity: Maximizing conditional diversity for token pruning in mllms. _arXiv preprint arXiv:2506.10967_ , 2025. 2 

- [54] Xuechao Zhang, Dong Wang, Sun Han, Weichuang Li, Bin Zhao, Zhigang Wang, Xiaoming Duan, Chongrong Fang, Xuelong Li, and Jianping He. Affordance-driven nextbest-view planning for robotic grasping. _arXiv preprint arXiv:2309.09556_ , 2023. 2, 3 

- [55] Enshen Zhou, Yiran Qin, Zhenfei Yin, Yuzhou Huang, Ruimao Zhang, Lu Sheng, Yu Qiao, and Jing Shao. Minedreamer: Learning to follow instructions via chain-ofimagination for simulated-world control. _arXiv preprint arXiv:2403.12037_ , 2024. 2 

- [56] Enshen Zhou, Qi Su, Cheng Chi, Zhizheng Zhang, Zhongyuan Wang, Tiejun Huang, Lu Sheng, and He Wang. Code-as-monitor: Constraint-aware visual programming for reactive and proactive robotic failure detection. _arXiv preprint arXiv:2412.04455_ , 2024. 

- [57] Enshen Zhou, Jingkun An, Cheng Chi, Yi Han, Shanyu Rong, Chi Zhang, Pengwei Wang, Zhongyuan Wang, Tiejun 

37174 

