---
title: "BFA++: Hierarchical Best-Feature-Aware Token Prune for Multi-View Vision Language Action Model"
date: "2026-02-24"
authors: "Haosheng Li; Weixin Mao; Zihan Lan; Hongwei Xiong; Hongan Wang; Chenyang Si"
venue: "RA-L"
url: https://arxiv.org/abs/2602.20566
pdf: https://arxiv.org/pdf/2602.20566
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.20566)** / [論文ページ](https://arxiv.org/abs/2602.20566)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **BFA++: Hierarchical Best-Feature-Aware Token Prune for Multi-View Vision Language Action Model** 

Haosheng Li<sup>1</sup><sup>_,_2</sup><sup>_∗_</sup> , Weixin Mao<sup>3</sup><sup>_∗_†</sup> , Zihan Lan<sup>3</sup><sup>_∗_</sup> , Hongwei Xiong<sup>3</sup> , Hongan Wang<sup>1</sup><sup>_,_2</sup> , Chenyang Si<sup>4</sup> , Ziwei Liu<sup>5</sup> , Xiaoming Deng<sup>1</sup><sup>_,_2‡</sup> , and Hua Chen<sup>3</sup><sup>_,_6‡</sup> 

**_Abstract_ — Vision-Language-Action (VLA) models have achieved significant breakthroughs by leveraging Large Vision Language Models (VLMs) to jointly interpret instructions and visual inputs. However, the substantial increase in visual tokens, particularly from multi-view inputs, poses serious challenges to real-time robotic manipulation. Existing acceleration techniques for VLMs, such as token pruning, often result in degraded performance when directly applied to VLA models, as they overlook the relationships between different views and fail to account for the dynamic and task-specific characteristics of robotic operation. To address this, we propose BFA++, a dynamic token pruning framework designed specifically for VLA models. BFA++ introduces a hierarchical pruning strategy guided by two-level importance predictors: an intra-view predictor highlights task-relevant regions within each image to suppress spatial noise, while an inter-view predictor identifies critical camera views throughout different manipulation phases to reduce cross-view redundancy. This design enables efficient token selection while preserving essential visual cues, resulting in improved computational efficiency and higher manipulation success rates. Evaluations on the RoboTwin benchmark and real-world robotic tasks demonstrate that BFA++ consistently outperforms existing methods. BFA++ improves the success rate by about 10% on both the** _π_ 0 **and RDT models, achieving speedup of 1.8** _×_ **and 1.5** _×_ **, respectively. Our results highlight that context-sensitive and task-aware token pruning serves as a more effective strategy than full visual processing, enabling faster inference and improved manipulation accuracy in real-world robotic systems.** 

## I. INTRODUCTION 

Recent advances in robotics have been significantly driven by Vision-Language-Action (VLA) models [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], which integrate visual perception and natural language understanding to enable robots to perform complex tasks from human instructions. To further enhance perceptual capability and action precision, a notable trend in recent research is the use of multiview visual inputs. This approach provides richer visual observations by capturing the scene from multiple camera views and is especially beneficial for dual-arm systems that require fine-grained coordination between manipulators, such as RDT [14] and _π_ 0 [9]. 

> _∗_ Co-first authors. †Project leader. ‡Corresponding authors. 

> 1Institute of Software, Chinese Academy of Sciences, Beijing, China. 

> 2University of Chinese Academy of Sciences, Beijing, China. 

> 3LimX Dynamic, Shenzhen, China. 

> 4Nanjing University, Nanjing, China. 

> 5Nanyang Technological University, Singapore. 

> 6Zhejiang University, Zhejiang, China. 


Fig. 1: The comparison between BFA++ and other methods. Compared to existing token pruning methods, our approach not only improves inference speed but also significantly increases the success rate. 

However, while multi-view settings provide richer information, they also bring challenges for VLA models. Unlike VLM domains with abundant training data, robotics datasets are inherently limited, resulting in VLA models having less well-established attention mechanisms. Consequently, these models struggle to distinguish task-relevant visual cues from redundant information across multiple views. Without proper guidance, this redundancy can misdirect attention, causing critical manipulation cues to be overlooked. This challenge makes incorporating human manipulation priors into VLA both practical and necessary [15], [7], [16]. 

In VLA models, limited pretraining data and fixed action output spaces constrain the model’s ability to learn robust attention mechanisms [4], [17], [18]. This setting gives rise to two major challenges in attention allocation. First, at the inter-view level, standard VLA training cannot reliably estimate the relative importance of different camera views, which changes dynamically depending on the task phase. Second, at the intra-view level, models may focus on irrelevant regions, such as backgrounds or disrupting objects, rather than task-aware areas. Although using unsupervised token importance predictors [19] and general unsupervised pruning methods [7], [16], [20], [21] show promise in other domains like VLMs and image classification, they fail in VLA scenarios due to the lack of proper supervisory signals to identify task-relevant regions and ignore the relationships between multiple images. Without supervision, these methods tend to treat all tokens equally and can even degrade performance, as the long optimization chain from action head to LLM to image encoder makes the supervision signals unclear, highlighting the need for direct guidance in 

manipulation scenarios. 

To address these attention allocation challenges, we conducted qualitative experiments detailed in Sec III-A, we find that inter-view importance varies dynamically: the head view suffices for approach and post-manipulation phases, while the wrist view is crucial during manipulation. Within each view, attention should focus on task-relevant regions such as the end-effector and target objects, while avoiding background distractions. 

Based on the above challenges and findings about twolevel importance variations, we propose a supervised dynamic token pruning method specifically designed for VLA post-training. It employs a hierarchical local-global token pruning strategy: first, locally pruning less important tokens within each view; then, globally ranking all remaining tokens by their combined importance scores to eliminate the least critical tokens across all views. We design two networks for hierarchical token pruning: an intra-view importance predictor (Intra-IP) identifies crucial tokens (e.g., robotic grippers, target objects) within each view, and an inter-view importance predictor (Inter-IP) determines critical views across manipulation stages. The training data is annotated using our comprehensive annotation system. Inter-view importance can be annotated through multiple approaches: LLM-based annotation [22], bounding box detection [23], [24] with hard-coded rules, or human annotation. Meanwhile, intraview importance is annotated using task-oriented bounding box prediction methods [25], [23], [24]. Both predictors are jointly trained with the backbone during post-training, enabling robust elimination of redundant tokens while preserving task-critical information. 

Our method produces better-distributed visual tokens with reduced similarity, enabling more accurate manipulation (Figure 1). Experiments on RoboTwin [26] and real environments demonstrated that our method achieves 1.8 _×_ speedup with 10% success improvement on _π_ 0 [9] and 1.5 _×_ speedup with 10% improvement on RDT [14]. Our main contributions can be summarized as follows: 1) We design a hierarchical token pruning method using inter-view and intra-view importance scores for VLA models to robustly eliminate redundant tokens while preserving task-aware information. 2) Experiments demonstrate that our plug-andplay pruning framework can be used effectively in both _π_ 0 [9] and RDT [14] models, which can achieve 1.5-1.8× speedup with improved about 10% success rates. 

## II. RELATED WORKS 

## _A. Vision Language Action Model_ 

Vision-Language-Action (VLA) models have emerged as a promising paradigm for robotic manipulation, integrating visual perception, language understanding, and action generation. Early VLA models primarily used single-image inputs. Among these, RT-2 [1] were pioneering works that demonstrated large-scale data collection and transformer architectures could enable robust real-world robotic control, and that web-scale pre-training effectively transfers to embodied tasks. OpenVLA [2] proposed an open-source 

VLA trained on diverse robot demonstrations with strong generalization. TinyVLA [4] explored model compression for resource-constrained deployment. 

Researchers later recognized that single images provide insufficient information, leading to multi-image VLA approaches. _π_ 0 [9] and _π_ 0 _._ 5 [27] introduced flow matching techniques and take three images as input. RDT [14] proposed a unified framework integrating multiple images for enhanced spatial-temporal understanding. OpenVLA-OFT [3] extended OpenVLA [2] with dedicated action heads and multi-image inputs to improve performance on complex tasks. Other works explored additional modalities, such as 3D-VLA [5] with 3D scene understanding and PointVLA [6] with point cloud representations. 

## _B. Token Prune Method_ 

Token pruning has emerged as an effective technique to reduce computational costs in vision transformers by dynamically removing redundant tokens during inference [15], [19], [7], [21], [28], [20]. DynamicViT [19] pioneered this approach by introducing a learnable prediction module that identifies and prunes less important tokens at different transformer layers. Token Merging [28] proposed merging similar tokens rather than discarding them, using bipartite soft matching to preserve information while reducing the token count. Recent advances have improved pruning strategies. But most of them primarily focus on pruning within transformer backbones based on token similarity and attention scores. FastV [21] used attention scores to identify important tokens with minimal changes to the architecture. DART [20] introduced token ranking by computing visual token similarity. BFA [15] developed a budget-aware framework that adjusts fusion ratios based on inter-view importance. EfficientVLA [7] and SP-VLA [16] use attention-based or spatial heuristics but lack task-specific token selection guidance. However, different from our BFA++, nearly all these methods were primarily designed for general vision-language models, and these methods [7], [16], [20], [21] fail to dynamically adapt token pruning to specific manipulation requirements, potentially discarding action-critical visual information. Our BFA++ addresses this issue by task-aware dynamic token selection tailored to robotic manipulation. 

## III. METHOD 

We propose BFA++ (Figure 2), a hierarchical token pruning framework for VLA models that accelerates inference and improves task success rates by filtering visual information. We use the inter-view importance score to evaluate the importance of each view, and use intra-view importance to rate the importance of tokens within view. Then, we locally prune less important tokens within each view using the intra-view importance score, and globally rank all remaining tokens by intra-view and inter-view importance scores to eliminate less critical tokens across all views. 

We first analyzed the inter-view and intra-view importance during the manipulation process in Sec. III-A. Then we 


Fig. 2: The pipeline of BFA++. The left figure shows our plug-and-play module for token pruning, and the right figure further details it. After obtaining the offline annotated inter-view importance _Sinter_<sup>_gt_andintra-viewimportance</sup><sup>_S_</sup> _intra_<sup>_gt_,wetrain</sup> the two importance predictor, and predict these two importance scores ( _Sinter_ , _Sintra_ ). Based on the predicted intra-view importance, we perform local pruning on the tokens. Then, based on both inter-view importance and intra-view importance, we conduct global pruning to obtain the final pruned tokens. 

detail our offline preparation of supervisory data for twolevel importance in Sec. III-B. Finally, we present the BFA++ pruning pipeline and its integration into VLA post-training in Sec. III-C. 

_A. Intra-View and Inter-View Importance of Token During Manipulation_ 


Fig. 3: Analyzing the importance of different viewpoints. We remove one or two view images to see how the performance of a trained _π_ 0 model is affected. This experiment demonstrates that the importance of different viewpoints varies across different stages of operation. 

Understanding the importance of different tokens across and within camera views is crucial for effective multi-view robotic manipulation. Within each view, models should focus on task-oriented regions, such as the robotic end-effector and target objects, rather than scattering attention across background elements or irrelevant scene components, as also demonstrated by methods [29], [18]. 

Moreover, to demonstrate the dynamic nature of token importance, we conduct perturbation experiments by excluding 

different camera views across manipulation stages, as shown in Figure 3. The experimental results reveal significant variations in the impact of view removal across the manipulation phases. When the wrist camera input is occluded during the approach or post-manipulation stages, it does not affect the success rate. However, during the manipulation stage, occluding the wrist camera causes the experiment to fail. These findings indicate that camera importance varies dynamically, consistent with BFA [15]: the head view suffices during approach phases, whereas the wrist camera becomes critical during fine manipulation when the head view is occluded. 

## _B. Offline Two-Level Importance Annotation_ 

Based on the findings above, we built a two-level offline importance annotation system to separately annotate the inter-view importance and the intra-view importance across tokens within each view, providing explicit supervision during post-training. 

For intra-view token importance, we use off-the-shelf models to select task-relevant regions. Typical approaches include background removal or bounding box detection method [30], [31], [23] to identify task-relevant areas. We selected the bounding box detection method for annotation because of its efficiency and suitability for our specific task requirements. 

For inter-view importance, we set the importance score to 1 for cameras that capture detailed interactions: specifically, when a manipulator interacts with objects, both the corresponding wrist and head cameras receive an importance score of 1. At all other times, only the head camera has an importance score of 1, while both wrist cameras are set to 0. We use three alternative methods for annotating inter-view importance. First, following BFA [15], we use large language 


Fig. 4: The annotation system of BFA++. For inter-view importance, we provide three optional methods (VLM, manual annotation, bounding boxes to detect overlaps). For intraview importance, we use the Grounding-SAM method to identify task-related regions. Details of the VLM annotation method can be found in BFA [15]. 

models [22] that analyze gripper trajectories, rest pose data, and gripper open/close status to determine when each manipulator is actively interacting with objects. Second, we employ a bounding box detector [30], [23] to detect overlaps between object and gripper bounding boxes, identifying interaction moments through visual detection. Third, we offer manual annotation as an option, where experienced annotators can complete one task in approximately one hour. These three methods categorize the manipulator states of each arm into phases (approaching, starting operation, moving with object, and retracting) and combine the states of both arms to determine which cameras should be marked as important at each timestamp. 

With the generated mask, we map it back to image patches to obtain importance scores for each patch (token). If a patch contains pixels within the mask, we assign it a score of 1, otherwise, 0. 

## _C. BFA++ Token Prune_ 

To address redundant input information in VLA models, we propose BFA++, a token pruning method that dynamically prunes redundant tokens during operation by predicting each token’s importance. Our BFA++ framework consists of three key components: 1) Two-level importance predictors, 2) a hierarchical token pruning strategy, and 3) integration with VLA post-training. 

**Two-level Importance Predictors.** As shown in Figure 2, we design two lightweight neural networks with the same architecture to predict importance scores at different levels. The inter-view importance predictor _f_ inter takes CLS tokens _{Tcls_<sup>_v}V_</sup> _v_ =1<sup>ofallviewsasinput(inourexperiment,</sup><sup>_V_= 3),</sup> which is the output of the vision encoder from all views, and outputs importance weights _Sinter_ = [ _Sinter_<sup>1</sup><sup>_,S_</sup> _inter_<sup>2</sup><sup>_,S_</sup> _inter_<sup>3]</sup> for each view: 


The intra-view importance predictor _f_ intra takes individual visual token _T_ Image<sup>_v,n_fromthevisionencoderasinput,and</sup> outputs intra-view importance score _Sintra_<sup>_v,n_ofthe</sup><sup>_n_-thtoken</sup> of the _v_ -th image: 


In this way, we obtain two-level token importance through these two lightweight networks. 

**Hierarchical Token Pruning.** Given the predicted two-level importance scores _Sinter_ and _Sintra_<sup>_v,n_, we perform token pruning</sup> in two stages: local pruning and global pruning, shown in Figure 5. 

_Local Pruning:_ We use the intra-view importance scores to perform local pruning within each view. At this stage, we rank tokens within each view by their intra-view importance scores and remove a fixed proportion of the least important tokens. However, to ensure that our score map is spatially coherent and avoid abrupt changes in importance values, we apply spatial adaptive weighting (Eq. 3) to refine the raw importance scores before pruning. Specifically, each token’s final importance score is refined by incorporating information from spatially neighboring tokens, where closer tokens have a stronger influence on the final score: 


where _N_ is the number of tokens output by the vision encoder for each image, _d_ ( _posn, posi_ ) represents the spatial distance between the 2D positions of tokens _n_ and _i_ in the feature map, and _ε_ is a small constant to prevent division by zero. This adaptive weighting creates spatially smooth importance distributions and avoids isolated high-importance regions. We then normalize the scores within each view and independently prune the _αv_ ( _v ∈{_ 1 _,_ 2 _,_ 3 _}_ ) ratio of tokens with the lowest intra-view importance scores for each image view. 


Fig. 5: The local and global token prune in _π_ 0+BFA++. _Global Pruning:_ After local pruning, we perform global pruning to further reduce tokens by ranking all remaining tokens in all views and removing less important tokens. 

We fuse inter-view and intra-view importance by multiplying each token’s importance score with its view weight: 


where _S_<sup>_v_</sup> _final_<sup>_,n_isthefinalglobalimportancescorefortoken</sup><sup>_n_</sup> in view _v_ , and _Sinter_<sup>_v_istheimportanceweightforview</sup><sup>_v_.</sup> Next, we rank remaining tokens by their final global importance scores _S_<sup>_v_</sup> _final_<sup>_,n_.Thisrankingconsidersbothhow</sup> important each token is within its view and how important that view is with respect to all views. 

Finally, we remove the tokens with the lowest _β_ proportion from the final scores in this unified ranking. This ensures that we keep the most important tokens regardless of which view they come from. 

**Integration with VLA Post-Training.** During VLA posttraining, we jointly optimize the importance predictors InterIP and Intra-IP alongside the main model. Based on the standard action prediction loss _L_ action of the baseline VLA model, we introduce two auxiliary losses. The inter-view importance loss _L_ inter supervises inter-view importance: _L_ inter = BCE( _f_ inter([ _Tcls_<sup>1</sup><sup>_,T_</sup> _cls_<sup>2</sup><sup>_,T_</sup> _cls_<sup>3])</sup><sup>_,S_</sup> inter<sup>gt) where</sup><sup>_f_inter is the inter-view</sup> importance predictor that takes concatenated CLS tokens from three views as input. The intra-view importance loss _L_ intra guides intra-view importance based on task-oriented masks: _L_ intra = ∑<sup>_V_</sup> _v_ =1<sup>∑</sup> _n_<sup>_N_</sup> =1<sup>BCE(</sup><sup>_S_</sup> intra<sup>_v,n,S_</sup> intra<sup>_v,n,_gt) where</sup><sup>_S_</sup> intra<sup>_v,n,_gtand</sup> _S_ inter<sup>gtdenotethegroundtruthintra-viewandinter-viewim-</sup> portance annotated by our annotation system. Both auxiliary losses use binary cross-entropy (BCE) loss. The total training loss is formulated as: _L_ total = _L_ action + _λ_ 1 _L_ inter + _λ_ 2 _L_ intra (5) where _λ_ 1 _, λ_ 2 are two weighting coefficients. In our experiments, we find that both two-level predictors converge quickly, and we can use the same hyperparameters as the original baseline for all other parameters. 

## IV. EXPERIMENT 

## _A. Implementation Details_ 

We evaluate our algorithm in both RoboTwin and realworld environments. During comparison, all baseline methods and our approach are trained on the same dataset for the same number of steps. We use the officially released codes of _π_ 0 [9] and RDT-1B [14]. For _π_ 0 [9] and algorithms built on _π_ 0 [9], we perform full-parameter fine-tuning for 5000 steps with a global batch size of 256 for each task. For RDT [14] and algorithms built on RDT, we fine-tune for 1200 steps with a global batch size of 128. The loss hyperparameters _λ_ 1 and _λ_ 2 are both set to 0.1, the prune ratio [ _α_ 1 _, α_ 2 _, α_ 3 _, β_ ] set to be 0 _._ 3 _,_ 0 _._ 2 _,_ 0 _._ 2 _,_ 0 _._ 5 and the weighting parameter _ε_ is set to 0.01. Since dropping tokens within the LLM backbone in _π_ 0 [9] would break the KV cache which will slow the speed, we perform token pruning before tokens enter the LLM backbone. For RDT [14], following DART [20], we perform token pruning at the second layer of the DiT block. Other methods maintain complete consistency with their original papers. We collected 50 episodes for the ’Bottle Pick’ task and 100 episodes for the seven other simulator tasks. For the four out-of-domain (OOD) task in RoboTwin2 [32], we collect 50 episodes each. Additionally, we designed 5 realworld experiments, each with 200 episodes, encompassing 

single-arm and dual-arm tasks as shown in Figure 6, with several tasks featuring extensive distractions that distinguish them from simulator environments. For evaluation, we test each simulator task 100 times and each real-world task 20 times. All training was conducted on eight NVIDIA A100 GPUs, and inference was performed on a single NVIDIA RTX 3090 GPU. 


Fig. 6: Task description of real world experiments. 

## _B. Experiment Results_ 

We evaluate the effectiveness of our algorithm in both simulation and real-world environments, and the results of success rate and inference speed in control FPS are shown in Table II and Table I. We select two state-of-the-art methods _π_ 0 [9] and RDT [14] as VLA baseline models, and BFA [15] and one of the best VLM token pruning methods–DART [20] for comparison of pruning. All methods are retrained during post-training. 

Our method achieves significantly higher success rates and faster control frequencies than baselines, with only a slight reduction in speed compared to BFA [15] due to the additional computation of intra-view importance scores alongside inter-view scores. We observe that the DART [20] pruning method tends to perform chaotic and disorganized pruning, preferring to keep only the middle portions while discarding the gripper’s spatial position information. Our method does not suffer from this issue. Moreover, to demonstrate the effectiveness of our method on OOD tasks, we conducted tests on the RoboTwin2 [32] benchmark with cluttered object distractions and unseen environments (varying lighting, backgrounds, and heights) as shown in the Table III. Our method consistently outperformed the baseline, validating its effectiveness on OOD tasks. Furthermore, in real-world environments where redundant information increases, our method still maintains good performance, particularly as our method can effectively enable the model to focus on specific interactive objects rather than distracted objects or background as shown in Figure 9(b). 

TABLE I: Comparison of baseline and BFA++ in RoboTwin. Our method surpasses nearly all baseline methods across various metrics. 

|**Model**|**Hammer Beat **|**Block Handover**|**Bottles Pick **|**Blocks Stack **|**Mug Hang B**|**ottle Adjust **|**Shoe Place **|**Cup Place**|**Mean**|**FPS**|
|---|---|---|---|---|---|---|---|---|---|---|
|_π_0 [9]|0.78|0.52|0.65|0.54|0.07|0.46|0.59|0.36|0.496|6.5 Hz|
|_π_0+DART [20]|0.70|0.53|0.64|0.41|0.08|0.50|0.49|0.30|0.456|9.8 Hz|
|_π_0+BFA [15]|0.80|0.62|0.59|0.60|0.07|0.52|**0.65**|0.34|0.524|11.1 Hz|
|_π_0+BFA++|**0.84**|**0.66**|**0.70**|**0.60**|**0.15**|**0.58**|**0.65**|**0.48**|**0.583**|10.3 Hz|
|RDT [14]|0.83|0.78|0.48|0.15|0.05|0.48|0.61|0.38|0.470|1.0 Hz|
|RDT+DART [20]|0.71|0.70|0.58|0.07|0.03|0.48|0.41|0.24|0.403|1.6 Hz|
|RDT+BFA [15]|0.84|0.80|0.59|**0.22**|0.05|0.42|0.59|0.40|0.489|1.7 Hz|
|RDT+BFA++|**0.89**|**0.82**|**0.80**|0.19|**0.09**|**0.58**|**0.67**|**0.48**|**0.565**|1.5 Hz|


TABLE II: Comparison in real-world environments with success rate and inference speed. Our method demonstrates substantial performance improvements over baseline approaches. 

|**Method**|Bottle<br>Handove|r<br>Grasp<br>Chicken|Slide<br>Bag|Insert<br>Cable<br>|Banana<br>Hard|<sup>**Mean**</sup>|**FPS**|
|---|---|---|---|---|---|---|---|
|_π_0 [9]|0.30|0.45|0.15|0.10|0.35|0.27|5.8 Hz|
|_π_0+DART [20]|0.20|0.50|0.05|0.00|0.20|0.19|8.5 Hz|
|_π_0+BFA [15]|0.45|**0.65**|0.20|0.20|0.40|0.38|10.1 Hz|
|_π_0+BFA++|**0.60**|**0.65**|**0.30 **|**0.30**|**0.55**|**0.48**|9.4 Hz|
|RDT [14]|0.35|0.50|0.05|0.05|0.20|0.23|1.2 Hz|
|RDT+DART [20]|0.25|0.35|0.00|0.00|0.20|0.16|1.8 Hz|
|RDT+BFA [15]|0.40|0.65|0.20|0.15|0.35|0.35|1.8 Hz|
|RDT+BFA++|**0.55**|**0.75**|**0.35 **|**0.20**|**0.45**|**0.46**|1.7 Hz|


TABLE III: Comparison in OOD environments with success rate and inference speed in RoboTwin2. Our method shows impressive improvement. 

|**Method**|Adjust<br>Bottle|Beat<br>Hammer|Handover<br>Block|Open<br>Laptop|<sup>**Mean**</sup>|**FPS**|
|---|---|---|---|---|---|---|
|_π_0 [9]|0.56|0.21|0.08|0.46|0.328|6.4 Hz|
|_π_0+DART [20]|0.40|0.08|0.05|0.30|0.208|10.0 Hz|
|_π_0+BFA [15]|0.59|0.24|0.18|0.46|0.368|11.3 Hz|
|_π_0+BFA++|**0.63**|**0.25**|**0.19**|**0.55**|**0.405**|10.5 Hz|


_C. Analysis_ 

We analyze the tokens from both BFA++ and the baseline to understand why pruning actually improves performance. 

First, as shown in Figure 7, we perform t-SNE [33] visualization on the tokens generated by the baseline and our method on _π_ 0 [9]. We can see that the original tokens from the three views are highly mixed, indicating that the model is processing a lot of redundant information. After BFA++ pruning, tokens from different views are well separated and highly distinct. This shows that input redundancy is almost eliminated, allowing the model to better extract useful information. 

Next, we visualize the Grad-CAM [34] heatmaps produced by the vision encoder for both the baseline ( _π_ 0) and our method ( _π_ 0 + BFA++). As shown in Figure 8, We find that the baseline model shows scattered attention, focusing on global information. After applying our token pruning method, the vision encoder can focus more on important areas, such as the gripper and interacting objects. Unlike typical VLMs, global information in VLA scenarios often includes a lot of irrelevant content. Our method helps the model focus its attention on key interaction regions with more useful information. 


Fig. 7: T-SNE of token with baseline and our BFA++. Tokens from the left view are omitted as they are entirely pruned by BFA++, and BFA++ shows less similar token distributions across views. 


Fig. 8: Grad-Cam heatmaps with baseline and our BFA++. Our method exhibits significantly more concentrated attention on the gripper and interactive objects. 

## _D. Ablation Study_ 

We conduct ablation experiments on our algorithm components using _π_ 0 [9] on four simulation tasks. 

In Table IV, “w/o Hierarchical” means we obtain the final token scores by directly multiplying inter-view importance with intra-view importance, and conduct pruning accordingly. Without hierarchical token pruning, our success rate drops significantly. This is because direct end-to-end ranking tends to select the main view while discarding wrist camera information, similar to using only the main view. “w/o Adaptive Weight” refers to distance weighting not being used. The results show that using distance weighting, which prevents pruning the tokens between objects and grippers, improves our method’s performance in all four tasks. Therefore, our hierarchical token pruning and adaptive weight are both effective. 

Then we conduct experiments without the inter-view 


Fig. 9: The visualization of the final pruned tokens with BFA++, predicted intra-view importance, and inter-view importance. In figures (a) and (b), each image is composed of three views (left, head, right wrist). Figure (a) represents the token importance predicted by Intra-IP, while figure (b) shows the final token retention visualization. Figure (c) illustrates how the inter-view importance predicted by Inter-IP changes throughout the manipulation process shown in the bottom portion. 

TABLE IV: Ablation on components and method of BFA++ with _π_ 0. The results show that all our components are effective and the designed BFA++ pruning structure is superior to alternative methods. 

below 0.5 multiplied by 0.8, which is the best parameter we found through exploration, with other settings identical to BFA++. This approach shows inconsistent speed due to variable prune ratio, making it unsuitable for VLA tasks, and achieves lower success rates than BFA++. 

|**Method**|Block<br>Hammer|Bottle<br>Adjust|Shoe<br>Place|Cup<br>Place|<sup>**Mean**</sup>|**FPS**|aceves|ower success rates tan ++.||
|---|---|---|---|---|---|---|---|---|---|
|w/o Inter-IP|0.76|0.41|0.56|0.50|0.558|10.8 Hz||||
|w/o Intra-IP|0.74|0.51|0.56|0.35|0.540|11.0 Hz|95|Bottles Pick Control Frequency|11|
|w/o Hierarchical|0.73|0.49|0.58|0.46|0.565|10.4 Hz||<br>Hammer Beat Shoe Place||
|w/o Adaptive Weight|0.84|0.53|0.60|0.46|0.608|10.4 Hz|85||10<br>)|
|Adaptive Pooling|0.75|0.48|0.55|0.46|0.560|11.9 Hz|||Hz|
|Random Drop|0.70|0.51|0.52|0.41|0.535|11.5 Hz|75<br>%)||9<br>cy(|
|Online Drop|0.66|0.45|0.50|0.39|0.500|1.3 Hz|te(||en|
|Adaptive Ratio Drop|**0.84**|**0.60**|0.63|0.46|0.633|8.4 Hz|Ra||qu|
|Our BFA++<br>mportance predict|**0.84**<br>or (Int|0.58<br>er-IP)|**0.65**<br>and in|**0.48**<br>tra-vi|**0.638**<br>ew im|10.3 Hz<br>portance|55<br>65<br>Success||7<br>8<br>Control Fre|
|redictor (Intra-IP)|, shown|as “w|/o Inte|r-IP”|and “w|/o Intra-|45|0<br>20<br>30<br>60<br>70<br>85|6|
|P” in Table IV,|using|only|hierarc|hical|pruni|ng with-||Prune Ratio (%)||


importance predictor (Inter-IP) and intra-view importance predictor (Intra-IP), shown as “w/o Inter-IP” and “w/o IntraIP” in Table IV, using only hierarchical pruning without cross-view importance and only using the inter-view importance score to prune. As shown in Table IV, both components enable our model to more accurately identify which tokens to prune. To further validate our method, we compare BFA++ with adaptive pooling [35], random token pruning, and online pooling, which computes intra-view and inter-view importance scores via online annotation. For fair comparison, all methods are applied during both posttraining and inference. Our method significantly outperforms all baselines. We observe that online pruning shows notably lower speed and success rate than the baseline, because online annotation is excessively time-consuming during inference and substantially increases post-training time due to repeated annotations. In contrast, our method effectively backpropagates gradients from both inter-view and intraview perspectives. Finally, we ablate the fixed prune ratio by comparing with adaptive token prune ratios. During twostep pruning, it prunes the number of tokens with scores 

Fig. 10: The ablation of the final prune ratio of BFA++. As the prune ratio increases, the control frequency accelerates, and the success rate first increases and then decreases. Our choice of prune ratio is balanced, as it not only accelerates the process but also maintains a relatively high success rate. 

Next, we conducted an ablation study on the total amount of token pruning by scaling the drop ratio proportionally to assess its effect. As shown in Figure 10, this behavior can be neatly explained by mutual information theory: when the pruning rate is low, both model accuracy and inference speed improve together, because what we remove are mostly redundant or minor tokens that carry little mutual information with the task goal. Dropping them not only reduces computation but also acts as a denoiser, helping the model focus on the truly important bits. However, once the pruning rate exceeds a certain threshold, even as speed continues to improve, accuracy drops sharply. The reason is that pruning begins to 

remove key tokens that have very high mutual information with the correct answer, so performance degrades. 

## V. CONCLUSION 

In this work, we propose BFA++, a dynamic token pruning framework that addresses redundant visual information in multi-view vision–language–action models. Our method introduces two-level importance predictors to identify critical camera views and task-relevant regions, jointly trained with the VLA model using automatically annotated data. Through hierarchical token pruning, BFA++ removes redundant tokens while preserving essential manipulation details. Experiments on the RoboTwin benchmark [26] show that BFA++ achieves 1.5–1.8 _×_ speedup while improving success rates by about 10% on both _π_ 0 [9] and RDT [14], demonstrating that intelligent feature selection can outperform brute-force processing of all inputs. As a post-training approach, BFA++ may face generalization challenges under unseen objects or camera configurations, as the importance score networks are optimized for the training distribution. Future work will focus on improving the robustness of the importance predictors to broader variations in objects and viewpoints. 

## ACKNOWLEDGMENT 

This work was supported in part by the National Key Research and Development Program of China under Grant 2024YFC3308500, the National Science Foundation of China under Grants 92570206 and 62473356, the Beijing Natural Science Foundation under Grants L232028 and L242060, and the Chongqing Industry and Information Technology R&D Program under Grant YJX-2025001001003. 

## REFERENCES 

- [1] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [2] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. Foster, G. Lam, P. Sanketi _et al._ , “Openvla: An open-source vision-language-action model,” _arXiv preprint arXiv:2406.09246_ , 2024. 

- [3] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-languageaction models: Optimizing speed and success,” _arXiv preprint arXiv:2502.19645_ , 2025. 

- [4] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, R. Cheng, C. Shen, Y. Peng, F. Feng _et al._ , “Tinyvla: Towards fast, data-efficient visionlanguage-action models for robotic manipulation,” _arXiv preprint arXiv:2409.12514_ , 2024. 

- [5] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” in _Forty-first International Conference on Machine Learning, ICML 2024, Vienna, Austria, July 21-27, 2024_ . OpenReview.net, 2024. [Online]. Available: https://openreview.net/forum?id=EZcFK8HupF 

- [6] C. Li, J. Wen, Y. Peng, Y. Peng, F. Feng, and Y. Zhu, “Pointvla: Injecting the 3d world into vision-language-action models,” _arXiv preprint arXiv:2503.07511_ , 2025. 

- [7] Y. Yang, Y. Wang, Z. Wen, L. Zhongwei, C. Zou, Z. Zhang, C. Wen, and L. Zhang, “Efficientvla: Training-free acceleration and compression for vision-language-action models,” _arXiv preprint arXiv:2506.10100_ , 2025. 

- [8] H.-T. L. Chiang, Z. Xu, Z. Fu, M. G. Jacob, T. Zhang, T.-W. E. Lee, W. Yu, C. Schenck, D. Rendleman, D. Shah _et al._ , “Mobility vla: Multimodal instruction navigation with long-context vlms and topological graphs,” _arXiv preprint arXiv:2407.07775_ , 2024. 

- [9] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A vision-languageaction flow model for general robot control, 2024,” _URL https://arxiv. org/abs/2410.24164_ . 

- [10] W. Mao, W. Zhong, Z. Jiang, D. Fang, Z. Zhang, Z. Lan, H. Li, F. Jia, T. Wang, H. Fan _et al._ , “Robomatrix: A skill-centric hierarchical framework for scalable robot task planning and execution in openworld,” _arXiv preprint arXiv:2412.00171_ , 2024. 

- [11] K. F. Gbagbe, M. A. Cabrera, A. Alabbas, O. Alyunes, A. Lykov, and D. Tsetserukou, “Bi-vla: Vision-language-action model-based system for bimanual robotic dexterous manipulations,” in _2024 IEEE International Conference on Systems, Man, and Cybernetics (SMC)_ . IEEE, 2024, pp. 2864–2869. 

- [12] J. Liu, H. Chen, P. An, Z. Liu, R. Zhang, C. Gu, X. Li, Z. Guo, S. Chen, M. Liu _et al._ , “Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model,” _arXiv preprint arXiv:2503.10631_ , 2025. 

- [13] X. Zhang, Y. Liu, H. Chang, L. Schramm, and A. Boularias, “Autoregressive action sequence learning for robotic manipulation,” _IEEE Robotics and Automation Letters_ , 2025. 

- [14] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [15] Z. Lan, W. Mao, H. Li, L. Wang, T. Wang, H. Fan, and O. Yoshie, “Bfa: Best-feature-aware fusion for multi-view fine-grained manipulation,” _arXiv preprint arXiv:2502.11161_ , 2025. 

- [16] Y. Li, Y. Meng, Z. Sun, K. Ji, C. Tang, J. Fan, X. Ma, S. Xia, Z. Wang, and W. Zhu, “Sp-vla: A joint model scheduling and token pruning approach for vla model acceleration,” _arXiv preprint arXiv:2506.12723_ , 2025. 

- [17] H. Li, Y. Zuo, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui _et al._ , “Simplevla-rl: Scaling vla training via reinforcement learning,” _arXiv preprint arXiv:2509.09674_ , 2025. 

- [18] J. Zhang, S. Wu, X. Luo, H. Wu, L. Gao, H. T. Shen, and J. Song, “Inspire: Vision-language-action models with intrinsic spatial reasoning,” _arXiv preprint arXiv:2505.13888_ , 2025. 

- [19] Y. Rao, W. Zhao, B. Liu, J. Lu, J. Zhou, and C.-J. Hsieh, “Dynamicvit: Efficient vision transformers with dynamic token sparsification,” _Advances in neural information processing systems_ , vol. 34, pp. 13 937– 13 949, 2021. 

- [20] Z. Wen, Y. Gao, S. Wang, J. Zhang, Q. Zhang, W. Li, C. He, and L. Zhang, “Stop looking for important tokens in multimodal language models: Duplication matters more,” _arXiv preprint arXiv:2502.11494_ , 2025. 

- [21] A. Chandak, L. Antani, M. Taylor, and D. Manocha, “Fastv: Frompoint visibility culling on complex models,” in _Computer Graphics Forum_ , vol. 28, no. 4. Wiley Online Library, 2009, pp. 1237–1246. 

- [22] G. Comanici, E. Bieber, M. Schaekermann _et al._ , “Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities,” _arXiv preprint arXiv:2507.06261_ , 2025. 

- [23] B. Xiao, H. Wu, W. Xu, X. Dai, H. Hu, Y. Lu, M. Zeng, C. Liu, and L. Yuan, “Florence-2: Advancing a unified representation for a variety of vision tasks,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 4818–4829. 

- [24] N. Ravi, V. Gabeur, Y.-T. Hu, R. Hu, C. Ryali, T. Ma, H. Khedr, R. R¨adle, C. Rolland, L. Gustafson _et al._ , “Sam 2: Segment anything in images and videos,” _arXiv preprint arXiv:2408.00714_ , 2024. 

- [25] S. Liu, Z. Zeng, T. Ren, F. Li, H. Zhang, J. Yang, Q. Jiang, C. Li, J. Yang, H. Su _et al._ , “Grounding dino: Marrying dino with grounded pre-training for open-set object detection,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 38–55. 

- [26] Y. Mu, T. Chen, S. Peng, Z. Chen, Z. Gao, Y. Zou, L. Lin, Z. Xie, and P. Luo, “Robotwin: Dual-arm robot benchmark with generative digital twins (early version),” in _European Conference on Computer Vision_ . Springer, 2025, pp. 264–273. 

- [27] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0.5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [28] D. Bolya, C.-Y. Fu, X. Dai, P. Zhang, C. Feichtenhofer, and J. Hoffman, “Token merging: Your vit but faster,” _arXiv preprint arXiv:2210.09461_ , 2022. 

- [29] V. Bhat, Y.-H. Lan, P. Krishnamurthy, R. Karri, and F. Khorrami, “3d cavla: Leveraging depth and 3d context to generalize vision language 

action models for unseen tasks,” _arXiv preprint arXiv:2505.05800_ , 2025. 

- [30] T. Ren, Q. Jiang, S. Liu, Z. Zeng, W. Liu, H. Gao, H. Huang, Z. Ma, X. Jiang, Y. Chen _et al._ , “Grounding dino 1.5: Advance the” edge” of open-set object detection,” _arXiv preprint arXiv:2405.10300_ , 2024. 

- [31] T. Ren, S. Liu, A. Zeng, J. Lin, K. Li, H. Cao, J. Chen, X. Huang, Y. Chen, F. Yan _et al._ , “Grounded sam: Assembling open-world models for diverse visual tasks,” _arXiv preprint arXiv:2401.14159_ , 2024. 

- [32] T. Chen, Z. Chen, B. Chen, Z. Cai, Y. Liu, Z. Li, Q. Liang, X. Lin, Y. Ge, Z. Gu _et al._ , “Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation,” _arXiv preprint arXiv:2506.18088_ , 2025. 

- [33] L. Van der Maaten and G. Hinton, “Visualizing data using t-sne.” _Journal of machine learning research_ , vol. 9, no. 11, 2008. 

- [34] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, “Grad-cam: Visual explanations from deep networks via gradient-based localization,” in _Proceedings of the IEEE international conference on computer vision_ , 2017, pp. 618–626. 

- [35] L. Yao, L. Li, S. Ren, L. Wang, Y. Liu, X. Sun, and L. Hou, “Deco: Decoupling token compression from semantic abstraction in multimodal large language models,” _arXiv preprint arXiv:2405.20985_ , 2024. 

