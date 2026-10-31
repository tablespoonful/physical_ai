---
title: "RoboAgent: Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action Chunking"
date: "2023-09-05"
authors: "Homanga Bharadhwaj; Jay Vakil; Mohit Sharma; Abhinav Gupta; Shubham Tulsiani; Vikash Kumar"
url: https://arxiv.org/abs/2309.01918
pdf: https://arxiv.org/pdf/2309.01918
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2309.01918)** / [論文ページ](https://arxiv.org/abs/2309.01918)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **RoboAgent: Generalization and Efficiency in Robot Manipulation via Semantic Augmentations and Action Chunking** 

**Homanga Bharadhwaj**<sup>_∗,_1</sup><sup>_,_2</sup> **Jay Vakil**<sup>_∗,_2</sup> **Mohit Sharma**<sup>_∗,_1</sup> 

**Abhinav Gupta**<sup>1</sup> **Shubham Tulsiani**<sup>1</sup> 

**Vikash Kumar**<sup>1</sup><sup>_,_2</sup> 

1 **Carnegie Mellon University,** 2 **FAIR-MetaAI** 

`https://robopen.github.io/` � 


Figure 1: A glimpse of the diverse manipulation capabilities of _RoboAgent_ – a single agent capable of 12 manipulation skills across 38 tasks encompassing 6 activities. For videos, visit: `robopen.github.io/` � 

**Abstract:** The grand aim of having a single robot that can manipulate arbitrary objects in diverse settings is at odds with the paucity of robotics datasets. Acquiring and growing such datasets is strenuous due to manual efforts, operational costs, and safety challenges. A path toward such an universal agent would require a structured framework capable of wide generalization but trained within a reasonable data budget. In this paper, we develop an efficient system ( _RoboAgent_ ) for training universal agents capable of multi-task manipulation skills using (a) _semantic augmentations_ that can rapidly multiply existing datasets and (b) _action representations_ that can extract performant policies with small yet diverse multimodal datasets without overfitting. In addition, reliable task conditioning and an expressive policy architecture enable our agent to exhibit a diverse repertoire of skills in novel situations specified using language commands. Using merely 7500 

> _∗_ authors contributed equally 

demonstrations, we are able to train a single agent capable of 12 unique skills, and demonstrate its generalization over 38 tasks spread across common daily activities in diverse kitchen scenes. On average, _RoboAgent_ outperforms prior methods by over 40% in unseen situations while being more sample efficient and being amenable to capability improvements and extensions through fine-tuning. 

## **1 Introduction** 

Training a robot manipulator with multiple skills requires exposure to diverse experiences and the ability to acquire skills from a diverse data corpus. To collect such a multi-skill data corpus in the real world requires substantial effort and suffers from high operational costs and safety challenges. Given the expense, efficiency in robot learning paradigms is necessary for real-world training and deployment. While there are recent efforts in scaling real-world robotic datasets despite these challenges [1, 2, 3], efficiency seems to be overlooked in the attempts to scale [4, 5, 6, 7]. 

With the acknowledgment that robot learning will generally benefit as the scale of the robotics dataset grows, the focus of our work is on investigating generalization in developing capable agents under a _given data budget_ . We restrict ourselves to a dataset with 7,500 robot manipulation trajectories (an order of magnitude less than related works [5]) containing a diverse collection of manipulation skills across different tasks. As a robot under deployment in real environments like homes, hospitals, etc., will always find itself in unseen scenarios, we set out to develop the most capable agent with an emphasis on its _ability to generalize to novel situations within this data budget_ . 

At first sight, wide generalization with a data budget seems like wishful thinking - while it’s possible to provide large representation capabilities to the agent’s policy, scaling without data diversity will likely lead to overfitting and no generalization. Our insight is twofold: (1) We ensure sufficient coverage of different skills in different scenarios in a dataset (of 7500 trajectories) we collect through teleoperation. The collected dataset is diversified offline, at no extra human/robot cost, via semantic augmentations [8, 9, 10] to aid generalization in novel situations. (2) We train a languageconditioned manipulation policy with **MT-ACT** – multi-task action-chunking transformers capable of handling the multi-modal data distribution. The architecture leverages the fact that robot movements are temporally correlated, by predicting action chunks [11] instead of per-step actions, leading to smoother behaviors and mitigation of covariate shift commonly observed in the low data imitation learning regime. 

Overall, we emphasize that the data efficiency lessons we present are _general_ and will help in achieving generalizable agents independent of the available data budget. Building on these insights, we make the following contributions: 

- We present an efficient method MT-ACT designed to recover **generalist agents on a data budget** . MT-ACT leverages data multiplication via semantic augmentations and action representations to drive efficiency gains in low-data settings. 

- MT-ACT’s architecture can effectively ingest multi-modal trajectory data to recover _RoboAgent_ – a single policy that can perform a diverse set of tasks through language instructions. Through extensive real-world experiments, we show _RoboAgent_ is **capable of exhibiting 12 manipulation skills** . 

- We perform extensive generalization studies to demonstrate that MT-ACT is 40 % more performant than alternatives, exhibits much **superior generalization to diverse novel scenarios** , and is amenable to **improvements and extensions during deployment through fine-tuning** . 

- We meticulously recorded all the data collected during the course of the project which we are opensourcing as part of `RoboSet` - one of the **largest open-source robotics dataset** on commodity hardware. It contains high-quality human teleOp trajectories spanning a balanced distribution of 12 skills across 38 tasks in diverse kitchen scenes. 

2 


Figure 2: Two stage framework: [Left] **Semantic augmentation** stage diversifies the robot data offline using inpainting augmentations at no extra human/robot cost. [Right] **Policy learning** stage trains languageconditioned policy using MT-ACT – multi-task action-chunking transformers – which leverages efficient action representations for ingesting multi-modal multi-task data into a single multi-skill multi-task policy. 

## **2 Related Work** 

**Frameworks for Scaling Robot Learning.** Given the cost of supervision in robot learning, selfsupervised learning [12, 13, 14] methods leveraging large unlabeled datasets have been a dominant paradigm in efforts towards building general-purpose agents. Large-scale simulations [15, 16, 17, 18] have also been leveraged with the hope of learning a general multi-task policy for diverse tasks [19, 20, 21, 22, 23, 24] first and then transferring it to the real world via sim2real[25, 26, 27, 28]. However, many existing multi-task RL works focus on narrow domains in simulation [22, 29], and those in the real-world show limited generalization and task diversity [30, 9]. While other works [19, 20, 31] focus on multi-task settings in diverse scenarios, they restrict to evaluating trained policies mostly in simulation. By contrast, our work focuses on a large, diverse set of real-world manipulation tasks. Recently, many works have used imitation learning with large-scale real-world robot tele-operation datasets of high quality [2, 3, 32, 1, 33, 34] . While early works collect limited real-world data [3, 33], more recent approaches [1, 5, 7] collect much larger datasets. In fact, [5] gathers, possibly, the largest dataset ( _≈_ 130 _K_ demonstrations) outside bin and place settings and shows impressive generalization with skills learned using this data. Our work is similar in spirit, _i.e._ , we focus on real-world manipulation tasks and aim to learn a multi-task policy using _limited_ realworld demonstrations. However, unlike [1], we avoid toy environment setups and focus on realistic real-world kitchen setups with clutter and multiple feasible tasks in a scene. Additionally, our agents exhibit a much greater diversity of skills than [5, 7, 28] while being trained only on 7.5k trajectories, as opposed to 135k in [5]. Importantly, we collect our data with commodity hardware (see Figure 6) and are making it readily available to robotic researchers worldwide. 

**Alternate Data Sources in Robotics.** Recent successes of large-scale self-supervised approaches within both language and vision communities have showcased the advantage of large-scale data. Many recent works propose using pre-trained visual representations trained primarily on non-robot datasets [35, 36], for learning control policies [37, 38, 26, 39, 40]. Most of these works focus on single-task settings [37, 38, 41, 42], or in simulated robot environments [26, 39]. Given the inherently large cost of collecting real-world robotics datasets, many works have focused on using alternate data sources such as language [43, 44, 45, 46], human videos [47, 48, 49, 50, 51, 52, 53, 54], and generative augmentations [55, 56, 9, 8, 10]. Our work is most similar to the latter set of works, some of which use diffusion models to generate augmentations for data collected in the real world. However, unlike some prior works [9, 8] our approach is fully automatic. We do not need segmentation masks [9] or object meshes [8] for generating augmentation data. Overall, our work is most similar to [10] which adapts a pre-trained open-world object detection model [57] for generating 

3 

Table 1: Open-source real-world manipulation dataset landscape: `RoboSet` (ours) `https:// robopen.github.io/roboset/` is one of the largest open-source robotics datasets. It contains high-quality demonstration, including human tele-operation, trajectories spanning a balanced distribution of 12 skills across 38 tasks in diverse kitchen scenes. 

||**Trajectories**|**Tasks**|**Skills**|**Scenes**|**Source**|
|---|---|---|---|---|---|
|`RoboSet`**(MT-ACT)**|7,500|38|12|10|TeleOp|
|`RoboSet`**(kitchen)**|30,050|38|12|10|TeleOp|
|`RoboSet`**(bin)**|70,000|10|4|1|Heuristics|
|`RoboSet`**(full)**|98,050|48|12|11|TeleOp+Heuristics|
|BridgeData [1]|33,200|72|8|10|TeleOp|
|BC-Z [6]|25,000|100|9|N/A|TeleOp|
|RoboTurk [3]|2,100|N/A|3|1|TeleOp|
|Amazon Pick-Place [60]|100,000|N/A|1|1|Heuristics|
|RoboNet [2]|162,000|N/A|2|7|Heuristics|
|BAIR Pushing [61]|N/A|N/A|1|1|Heuristics|


segmentations that are used with text-guided diffusion models to generate augmentations. However, our approach does not require any further fine-tuning of a separate module for open-vocabulary segmentation and language grounding. More importantly, we further investigate scaling laws with respect to semantic data augmentations to demonstrate the favorable impact of augmentations in aiding test-time generalization to unseen scenarios. 

## **3 MT-ACT: Multi-Task Action Chunking Transformer** 

To learn generalizable manipulation policies, it is essential for robots to be exposed to rich and diverse experiences, encompassing a wide range of skills and contextual variations. However, operational costs and real-world challenges in collecting such extensive datasets pose a practical limit on their overall size. Our goal is to address these limitations by developing _a paradigm that can learn effective multi-task agents under a limited data budget_ . Our approach consists of two stages (Figure 2): 

**Semantic Augmentation** – the first stage multiplies the pre-collected dataset by creating a diverse collection of semantic augmentations over the existing robot’s experiences. These semantic augmentations recreate a particular robot demonstration into several demonstrations, each with a different semantic context (objects, textures, backgrounds, etc), at no extra robot or human cost. Such data diversification incorporates real-world semantic priors into the multi-task manipulation agents preparing them to account for out-of-distribution scenarios they might encounter during deployment. 

**Policy Learning** – the second stage learns robust skills from limited skill data, adapting design choices from previously limited single-task settings to the context of large-scale generalization in multi-task multi-scene manipulation tasks with diverse skills. We develop MT-ACT – a languageconditioned novel policy architecture to train robust agents capable of recovering multiple skills from multi-modal datasets. To model the diverse multi-modal multi-task augmented datasets, we employ a Conditional Variational Autoencoder (CVAE) [58] to identify action distribution modes. This enables us to fit a high-capacity Transformer [59] conditioned on the CVAE encodings, effectively capturing the variations and dependencies in the augmented dataset. Our policy also leverages the fact that robot movements are temporally correlated. Predicting action chunks [11] instead of per-step actions, leads to smoother behaviors and mitigation of covariance shift commonly observed in the low data imitation learning regime. Next, we outline the individual components of our method in detail. 

### **3.1 Dataset (** `RoboSet` **)** 

Training a general agent capable of robustly exhibiting a diverse repertoire of skills in novel scenes and tasks needs exposure to experiences matching this diversity. To align with our goal of building 

4 

a data-efficient robot learning paradigm, we restrict ourselves to a frozen pre-collected small but diverse dataset – `RoboSet` (MT-ACT). In order to capture behavioral diversity, we ensure sufficient coverage over different core skills, where each skill if defined as a temporally correlated sequence of actions that lead to plausible change in an object’s pose. Example skills include _closing/opening_ articulated objects, _sliding_ , _wiping_ . Each skill is instantiated across a set of objects. We refer to such (skill, object) combinations as a **task** . Our tasks are instantiated in different kitchen scenes, visually illustrated in Appendix A. Instead of a random collection of tasks, we structure groups of tasks as belonging to be part of a household **activity** , such that they can be executed in sequence to obtain a meaningful outcome, such as cleaning a kitchen. Further details on the different skills, tasks and activities in `RoboSet` are provided in Appendix A.1. 


Figure 3: `RoboSet` (MT-ACT) contains a diverse set of 12 non-trivial manipulation skills (beyond picking/pushing, including articulated object manipulation and object re-orientation) expressed across 38 tasks across multiple scenes. In the figure, we mark the skill distribution of our dataset in terms of % of trajectories with a certain skill. The number on top represents the number of trajectories corresponding to the skill used to train RoboAgent. 

`RoboSet(MT-ACT)` – the dataset we used for this project consists of 7,500 trajectories (Table 1)<sup>1</sup> collected using human teleoperation. The dataset involves 12 skills expressed across multiple tasks and scenes. Figure 3 shows the distribution of skills over our dataset. While the commonly used pick-place skills cover 40% of the dataset, we also include contact-rich skills such as ( _Wipe_ , _Cap_ ) as well as skills involving articulated objects ( _Flap-Open_ , _Flap-Close_ ). We collect the overall dataset across four different physical setups. Each setup is instantiated with various everyday objects to create a kitchen scene. We frequently vary each set up with different variations of objects, thereby exposing each skill to multiple target objects and scene instantiations. We provide a glimpse of the overall setup and a subset of objects used in Figure 6, and data composition details in section 4. 

In Table 1, we compare our dataset with existing _open-source_ robot manipulation datasets. Compared to prior open-source real-world datasets, `RoboSet` presents a greater number and diversity of skills and scene variations. `RoboSet` is one of the largest publically released dataset with commodity robots collected in the real-world setup. Finally, despite our data diversity, `RoboSet(MT-ACT)` used for training our agents is still much smaller in size in comparison to other recent papers that use _proprietary_ robotic hardware, e.g. RT1 which has 135K trajectories [5], or those that rely on simulation [28]. 

### **3.2 Data Augmentation** 

Generally useful robot manipulation systems will need to be able to deal with out-of-distribution scenarios (e.g. different homes and offices). Since any dataset of a practical size will have a limited diversity of objects and scenes (due to physical access and operational constraints) compared to what agents will encounter during deployment. To enable test-time generalization to the unseen scenarios, we develop a _fully automatic_ offline process to multiply the dataset. 

> 1Note that the entire `RoboSet` is much larger and much more diverse. _RoboAgent_ is trained on `RoboSet` (MT-ACT) – a subset consisting of 7500 trajectories 

5 


Figure 4: Illustration of the data augmentations that we develop to rapidly multiply limited robot datasets with diverse semantic scene variations. In (a) we show the scene around the robot and the interaction object changing. In (b), we show the interaction object itself changing while preserving the rest of the scene. 

Given an initial dataset of robot behaviors, we multiply the dataset by creating multiple semantic variations of the dataset while preserving the _robot behavior_ within each trajectory. These semantic variations are created by applying augmentations per frame within the trajectory. Augmentations are created by inpainting a part of the image frame introducing new objects and scene variations. The inpainting locations are specified by a mask and are informed by a text prompt. As opposed to [9, 8, 10] needing manual masks, object templates, etc., our approach is fully automatic. We use the SegmentAnything model [62] to automatically detect semantic boundaries in the scene to create augmentation masks. We apply augmentations separately to the object under manipulation and the rest of the environment respecting the object and robot boundaries. See subsection A.2 for additional details. We emphasize that our approach toward semantic augmentation is fully automatic and offline. It takes advantage of and is also well poised to continually benefit from rapidly advancing progress in segmentation and in-painting models [62, 63]. Akin to fields of natural language processing and computer vision, by distilling semantic real-world priors present in internet images/videos into robotics datasets, it provides robot learning a scalable mechanism to benefit from internet-scale data at no extra cost to humans/robots. 

### **3.3 MT-ACT Architecture** 

Scaling up dataset diversity as well as network capacity constitutes the two fundamental requirements to improve generalization in machine learning paradigms. In the field of robot learning, the need for generalization remains at large as both of the aforementioned generation requirements are hard to meet under real-world constraints. Safety and operational costs challenge the availability of diverse datasets, and the need for fast real-time control loops restricts the inference time needed to avail large models. Recovery of a generalizable robot manipulation policy under a practical data budget available in robotics demands an efficient policy architecture. In scenarios that have sufficient coverage within the training data, we want the policy to stay close to nominal behaviors (efficient imitation). The policy also needs to be effective to new variations (effective generalization) and contexts (efficient task conditioning) that are unseen during training . In addition, we want the policies to exhibit temporally correlated smooth behaviors accomplishing tasks with minimal errors and safety violations. 

Our policy architecture – MT-ACT is designed to be a Transformer model [59] of sufficient capacity that can handle multi-modal multi-task robot datasets. In order to capture multi-modal data, following prior works [11] we incorporate a CVAE [58] that encodes action sequences into latent _style_ embeddings _z_ . The decoder of the CVAE is the Transformer policy that conditions on the latents _z_ . This formulation of expressing the policy as a generative model helps in effectively fitting to the multi-modal teleop data, without ignoring regions of a trajectory crucial for precision, which are also likely to be more stochastic. In order to model multi-task data, we incorporate a pre-trained language encoder [65] that learns an embedding _T_ of a particular task description. To mitigate issues of com- 

6 


Figure 5: Policy architecture for MT-ACT . We use a CVAE that learns latent encodings _z_ for action sequences to implicitly identify different _modes_ in the data. A transformer takes as input a latent code, language embedding of the task, and image embeddings from four camera views, to autoregressively output an action sequence _at_ : _t_ + _H_ for chunk size _H_ . On the right, we shows details for the FiLM layer [64] that we use for language-conditioning. 

pounding error and to achieve smooth temporally correlated robot motions, at each time-step, we predict actions _H_ steps in the future and execute them through temporal-aggregation of overlapping actions predicted for a particular time-step [11]. To improve effectiveness towards scene variations and robustness towards occlusions in clutter, we provide the policy with four different views of the workspace through four cameras. 

At time-step _t_ , the transformer encoder takes four camera views , _o_<sup>1:4</sup> _t_<sup>, the joint pose of the robot</sup><sup>_jt_,</sup> the style embedding from the CVAE _z_ , and the language embedding _T_ . We use a FiLM-based conditioning [64, 5], in order to ensure that the image tokens are able to reliably focus on the language instruction, such that the policy doesn’t get confused about the task when multiple tasks are possible in a scene. The encoded tokens go to the decoder of the Transformer policy with fixed position embeddings, which finally outputs the next action chunk ( _H_ actions) for the current time-step. For execution, we average over all overlapping actions predicted for the current time-step (As _H >_ 1, the action chunks overlap), and execute the resulting averaged action. 

## **4 Experimental Design** 

Through experiments, we want to understand the following research questions 

- How does MT-ACT perform, quantitatively and qualitatively, on a large set of vision-based robotic manipulation tasks? How does it generalize to new tasks, objects, and environments? 

- Does data augmentation improve robustness to noise/distractors? 

- Does data augmentation improve policy generalization (i.e. scenes with new target objects)? 

- Does the policy architecture of MT-ACT enable efficient learning with high performance? 

- Does action chunking help with temporally consistent trajectories, achieving higher success? 

To answer these research questions we instantiate our framework in the real world using commodity hardware and objects commonly used in everyday kitchens. Next, we outline the system and dataset used to investigate our questions and then describe the different generalization axes for evaluation. 

**Robot hardware.** Figure 6 shows our robot environment, called _RoboPen_ that consists of a kitchen setup with everyday objects, a Franka Emika Panda arm with a two-finger Robotiq gripper fitted with Festo Adaptive Fingers<sup>2</sup> , three fixed cameras (top, left, right), and a wrist camera mounted above the end-effector. The four Realsense D455 camera views provide complementary perspectives of the workspace, and we utilize all of them for robust policy learning. 

> 2 `https://robotiq.com/products/2f85-140-adaptive-robot-gripper` and `https://www. festo.com/us/en/p/adaptive-gripper-finger-id_DHAS_GF/` 

7 

**Data collection.** Our robot manipulation dataset for the experiments consists of 7,500 trajectories, collected through tele-operation by a human operator, over a period of two months. We collect all the data across four different physical setups with different kitchen-like environments with a Franka Emika [66]. Each setup also sporadically changes its scene by swapping new objects and backgrounds. The teleoperation stack is based on [67] and uses VR-controllers. The dataset comprises of diverse manipulation skills like opening/closing drawers, pouring, pushing, dragging, picking, placing, etc. across several everyday objects. Figure 3 shows the distribution of skills in the dataset. Additional details regarding the dataset, along with sample trajectories, and a link to the entire dataset are in the project website� linked with the paper. We are publicly releasing this dataset, as part of RoboSet – a large multi-skill robotics dataset described in subsection 3.1. To our knowledge, this is one of the largest open-source robot manipulation datasets with the most commonly used non-proprietary robot hardware (Franka Panda [66]) containing diverse real-world behaviors beyond pick and place. 


Figure 6: A zoomed-out view of the robot environment, showing all four cameras in the scene (in colored squares) that provide complementary views of the scene and a glimpse of the diverse set of objects in the dataset, used for all our experiments. The objects range from articulated objects like drawers and ovens, to smaller rigid objects like french press, bowls, and deformable objects like towels. 


Figure 7: Visualization of different generalization axes, evaluating effectiveness with lighting variations and smaller scene changes such as object poses (L1), robustness to significant scene variations (L2), generalization to unseen tasks (L3). _Bottom-Left:_ Results for commonly used L1-generalization. _Bottom-Right:_ Multi-Task (universal policy) results for different levels of generalization. See 9 for L4-generalization results. 

**Generalization Axes.** Following prior work [5, 6, 20], we define each _task_ to consist of a particular language command like _‘pick a cube of butter from the drawer on the left’_ that defines an object to 

8 

be interacted with (butter), a skill to be executed (pick), and some context (drawer on the left). Each activity consists of a collection of 4-5 closely tasks that can be executed in sequence. Table 2 lists the different activities used in our work. We refer to the policy trained over all the activities to be the _universal policy_ , and those trained only over one activity to be an _activity policy_ . We consider evaluations in terms of different levels of generalization, illustrated visually for a scene in Fig. 7: **L1(Effectiveness)** : Generalization of the agent to variations in object positions and orientations, and in lighting conditions. **L2 (Robustness):** New background, different distractor object variations, and unseen distractor objects introduced in the scene. **L3 (Generalization):** New tasks never seen before, including new object-skill combinations. **L4 (Strong Generalization):** New kitchen never seen before (see Figure 9 Left). 

## **5 Experiments** 

Through detailed real-world robot manipulation experiments, we evaluate the proposed framework for sample efficiency, and generalization of the agent to diverse scenes. 

**Baselines.** We compare multiple baselines that use visual policy learning for robotics. _Single Task Agents_ : We compare ACT-based policies [11] trained for individual tasks, and evaluated on the respective tasks. These policies don’t need to generalize across tasks and scene, and represent an approximate _oracle_ performance per task. _Visual Imitation Learning (VIL)_ : We compare with regular language-conditioned multi-task visual imitation learning. _CACTI_ [9]: This baseline is a prior framework for multi-task learning that also uses some scene augmentations for generalization. _RT1_ [5]: We re-implement a baseline RT1-like agent. _BeT_ [68]: We modify the Behavior Transformer architecture with language conditioning and train it in a multi-task manner. 

Next, we present results and analysis from our large-scale real-world experiments that attempt to understand the research questions presented in section 4. 

### **5.1 Multi-Task Real-World Results** 

**Performance.** Figure 7 (Left-Bottom) compares our proposed MT-ACT policies against commonly used imitation learning architectures. In this figure (Figure 7 Left-Bottom) we only plot results for _L1-generalization_ since this is the standard setting most other imitation learning algorithms use. We observe that all approaches that only model next-step actions (instead of sub-trajectories) exhibit weaker performance. Among these approaches, we find that action-clustering-based approaches (BeT [68]) for multi-task settings, perform significantly worse. We believe this happens because naive clustering in very diverse action distributions may not result in clusters that generalize across diverse skills. Additionally, since we are operating under a data budget, we observe that RT1-like approaches that require a lot of data do not perform well in the low data regime. By contrast, our MT-ACT policy which uses action-chunking and CVAE to model multi-modal sub-trajectories significantly outperforms all baselines. 

**Generalization and Robustness.** Figure 7 (Bottom-Right) shows the results for all methods across multiple levels of generalization ( **L1** , **L2** , and **L3** ). Recall that these levels of generalization include diverse table backgrounds, distractors ( **L2** ) and novel skill-object combinations ( **L3** ). From Figure 7 (Bottom-Right) we see that by virtue of semantic augmentations and action representations, MT-ACT significantly outperforms all the baselines we consider. More interestingly, we see that semantic augmentations have less effect for L1-generalization ( _≈_ 30% relative), they provide a _much more_ significant improvement for both L2-generalization ( _≈_ 100% relative) and L3-generalization ( _≈_ 400% relative). Since semantic augmentations affect both scenes (backgrounds and distractor objects) as well as target objects being manipulated they provide useful support for the policy to achieve increasing levels of generalization. 

Additionally, in Figure 8 we also separately report generalization results for each activity separately. From Figure 8 we see that each our proposed semantic augmentations positively affect each activity’s performance. Interestingly, we find that for 

9 


Figure 8: Results for MT-ACT, its ablated variant without semantic augmentations, and baselines, for different activities, with L1, L2, L3 levels of generalization. Each activity consists of 4-5 tasks, and the results average over the tasks in an activity. The results show that semantic augmentations significantly improve performance of MT-ACT over the baselines. In addition, even without augmentations, the MT-ACT policy achieves much higher success rates compared to the baselines. 

some of the harder activities (Making-Tea, Stowing-Bowl, Heating Soup) the relative improvement in performance due to semantic augmentations is much larger. Overall, our results show that traditional visual imitation learning (without any augmentations), i.e., VIL and RT1 trained on our relatively small dataset, completely fail for L3 and L2, indicating a lack of generalization to unseen scenarios, due to data paucity. Finally, we also test our policy on a completely new kitchen with novel objects, arrangements, distractors, i.e., L4 generalization. Figure 9 (Left) visualizes this new kitchen environment. We evaluate all methods in this new kitchen for 3 tasks. Figure 9 (Right) shows the results for each method on this new environment. Specifically, we obtain an average success rate of 25% for MT-ACT (and 0 for all the other baseFigure 9: Only MT-ACT policies perform lines). We see that MT-ACT without semantic augmentatasks in a completely new kitchen environtions also fails completely on this new environment thus ment (L4). indicating the benefits of our approach for zero-shot adaptation. 

### **5.2 Ablation** 

We ablate the different design choices we make in our proposed architecture. 

**Task Specification using FiLM conditioning.** For language conditioned multi-task policy, as described in section 3.3, we use a FiLM based conditioning [64] for the language embedding of task descriptions [69]. Here, we compare this design choice with a simple concatenation-based conditioning of the language embeddings with image tokens for the policy. In Fig. 10 (Left) we show results for this ablation study averaged over all activities, and we observe a 5-10% drop in performance of the version of MT-ACT without FiLM conditioning. 

**Chunk Size for Action Representations.** Here we train variants of MT-ACT with different chunk sizes 10, 20, 40. In Fig. 10 ((Middle-Left), we see that a chunk size of 20 performs the best, with a 0- 5% drop in performance with chunk size 10. In addition, large chunk size 40 performs significantly worse with more than 20% drop in performance indicating the inability of the policy to correct errors as the chunks grow in size. 

10 


Figure 10: We shows results of the different ablation studies and analysis in section 5.2, showing the benefits of FiLM conditioning, the effect of varying chunk sizes in the predictions, the number of augmentations per frame for multiplying the dataset, and the feasibility of fine-tuning MT-ACT for improved deployment. 

**Number of augmentations per frame.** We ablate the number of augmentations per frame, to see if more augmentations help MT-ACT in learning a more performant policy. From Fig. 10 (MiddleRight), we see that the number of augmentations per frame is strongly correlated with overall performance gains. Thanks to the real-world semantic priors injected via data augmentation, the gains are more notable for L2 and L3 levels where out-of-domain generalization is required from the policy. 

**Robustness analysis.** We perform several robustness analyses of the universal MT-ACT agent, by manually perturbing the scene during evaluation, and also introduce system failures like blocking the views from one, two, or three cameras. On average, we find that the policy is robust to these strong active variations, and can solve the specified task in about 70% of the 20 evaluations we run for this analysis. Videos showing these results are in the project website. 

**Plasticity.** Here, we evaluate the feasibility of adding additional capabilities to the universal MT-ACT agent, without requiring significant re-training. We take the trained agent (on 38 tasks) and fine-tune on (1 _/_ 10)<sup>th</sup> of the original data combined with data for a new held-out task (placing toast in toaster oven). The new task has 50 trajectories, multiplied with 4 augmentations per frame, for a total of 250 trajectories. Fig. 10 (Right) shows that the fine-tuned agent is able to learn this new task, without significantly deteriorating in performance on the previous 6 activities. Also, it achieves slightly better L2, L3 performance than a single-task policy trained only on augmented data of the new task, indicating efficient data re-use. 

## **6 Discussion and Limitations** 

We developed a framework for sample-efficient and generalizable multi-task robot manipulation in the real world. Our framework is based on rapidly multiplying a small robotics dataset through semantic scene augmentations, and training a multi-task language-conditioned policy that can ingest the diverse multi-modal data obtained through augmentations. We combine and adapt several design choices like action chunking and temporal aggregation proposed in the context of single-task policies, and show that they yield significant boosts in performance even in the multi-task settings we consider. 

Finally, we release one of the largest robot manipulation datasets to date involving over 12 skills in kitchen environments which we hope will facilitate further research in developing robot manipulation systems with diverse real-world generalization. An important limitation of our work is that all the tasks consist of individual skills, and an interesting direction for future work would be to develop approaches for composing skills automatically for solving long-horizon tasks. Another limitation is that we do not explore the axes of language generalization, and use language embeddings from pre-trained encoders as is, without any modifications. Future work could investigate better language conditioning that is more flexibly adaptable to changes in task descriptions. 

11 

## **Acknowledgements** 

We acknowledge various contributions, large and small, from the entire Embodied AI team at Meta. The project has also significantly benefitted from brainstorming sessions from – Aravind Rajeswaran, Chris Paxton, Tony Zhao, Abhishek Gupta, and individual contributions from Giri Anantharaman, Leonid Shamis, Tingfan Wu, Priyam Parashar, Chandler Meadows, Sahir Gomez, and Liyiming Ke. We thank Gaoyue Zhou, Raunaq Bhirangi, Sudeep Dasari , Yufei Ye, Mustafa Mukadam, Shikhar Bahl, Mandi Zhao, Wenxuan Zhou, Jason Ma, and Unnat Jain for helpful discussions at different stages of the project. 

## **References** 

- [1] F. Ebert, Y. Yang, K. Schmeckpeper, B. Bucher, G. Georgakis, K. Daniilidis, C. Finn, and S. Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. 

- [2] S. Dasari, F. Ebert, S. Tian, S. Nair, B. Bucher, K. Schmeckpeper, S. Singh, S. Levine, and C. Finn. Robonet: Large-scale multi-robot learning. In _Conference on Robot Learning_ , pages 885–897. PMLR, 2020. 

- [3] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, J. Gao, J. Emmons, A. Gupta, E. Orbay, et al. Roboturk: A crowdsourcing platform for robotic skill learning through imitation. In _Conference on Robot Learning_ , pages 879–893. PMLR, 2018. 

- [4] D. Kalashnikov, J. Varley, Y. Chebotar, B. Swanson, R. Jonschkowski, C. Finn, S. Levine, and K. Hausman. Mt-opt: Continuous multi-task robotic reinforcement learning at scale. _arXiv preprint arXiv:2104.08212_ , 2021. 

- [5] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [6] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 

- [7] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke, et al. Qt-opt: Scalable deep reinforcement learning for visionbased robotic manipulation. _arXiv preprint arXiv:1806.10293_ , 2018. 

- [8] Z. Chen, S. Kiami, A. Gupta, and V. Kumar. Genaug: Retargeting behaviors to unseen situations via generative augmentation. _arXiv preprint arXiv:2302.06671_ , 2023. 

- [9] Z. Mandi, H. Bharadhwaj, V. Moens, S. Song, A. Rajeswaran, and V. Kumar. Cacti: A framework for scalable multi-task multi-scene visual imitation learning. _arXiv preprint arXiv:2212.05711_ , 2022. 

- [10] T. Yu, T. Xiao, A. Stone, J. Tompson, A. Brohan, S. Wang, J. Singh, C. Tan, J. Peralta, B. Ichter, et al. Scaling robot learning with semantically imagined experience. _arXiv preprint arXiv:2302.11550_ , 2023. 

- [11] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [12] L. Pinto and A. Gupta. Learning to push by grasping: Using multiple tasks for effective learning. In _2017 IEEE international conference on robotics and automation (ICRA)_ , pages 2161–2168. IEEE, 2017. 

- [13] C. Lynch, M. Khansari, T. Xiao, V. Kumar, J. Tompson, S. Levine, and P. Sermanet. Learning latent plans from play. In _Conference on robot learning_ , pages 1113–1132. PMLR, 2020. 

12 

- [14] L. Berscheid, T. R¨uhr, and T. Kr¨oger. Improving data efficiency of self-supervised learning for robotic grasping. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 2125–2131. IEEE, 2019. 

- [15] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning. In _Conference on robot learning_ , pages 1094–1100. PMLR, 2020. 

- [16] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019–3026, 2020. 

- [17] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mazhar, et al. Orbit: A unified simulation framework for interactive robot learning environments. _IEEE Robotics and Automation Letters_ , 2023. 

- [18] Y. Zhu, J. Wong, A. Mandlekar, R. Mart´ın-Mart´ın, A. Joshi, S. Nasiriany, and Y. Zhu. robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv:2009.12293_ , 2020. 

- [19] S. Reed, K. Zolna, E. Parisotto, S. G. Colmenarejo, A. Novikov, G. Barth-Maron, M. Gimenez, Y. Sulsky, J. Kay, J. T. Springenberg, et al. A generalist agent. _arXiv preprint arXiv:2205.06175_ , 2022. 

- [20] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. Fei-Fei, A. Anandkumar, Y. Zhu, and L. Fan. Vima: General robot manipulation with multimodal prompts. _arXiv preprint arXiv:2210.03094_ , 2022. 

- [21] J. Schrittwieser, I. Antonoglou, T. Hubert, K. Simonyan, L. Sifre, S. Schmitt, A. Guez, E. Lockhart, D. Hassabis, T. Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 588(7839):604–609, 2020. 

- [22] L. Espeholt, H. Soyer, R. Munos, K. Simonyan, V. Mnih, T. Ward, Y. Doron, V. Firoiu, T. Harley, I. Dunning, et al. Impala: Scalable distributed deep-rl with importance weighted actor-learner architectures. _arXiv preprint arXiv:1802.01561_ , 2018. 

- [23] S. Sodhani, A. Zhang, and J. Pineau. Multi-task reinforcement learning with context-based representations. In _International Conference on Machine Learning_ , pages 9767–9779. PMLR, 2021. 

- [24] L. Kaiser, M. Babaeizadeh, P. Milos, B. Osinski, R. H. Campbell, K. Czechowski, D. Erhan, C. Finn, P. Kozakowski, S. Levine, et al. Model-based reinforcement learning for atari. _arXiv preprint arXiv:1903.00374_ , 2019. 

- [25] J. Tobin, R. Fong, A. Ray, J. Schneider, W. Zaremba, and P. Abbeel. Domain randomization for transferring deep neural networks from simulation to the real world. In _2017 IEEE/RSJ international conference on intelligent robots and systems (IROS)_ , pages 23–30. IEEE, 2017. 

- [26] M. Shridhar, L. Manuelli, and D. Fox. Cliport: What and where pathways for robotic manipulation. In _Conference on Robot Learning_ , pages 894–906. PMLR, 2022. 

- [27] A. Handa, A. Allshire, V. Makoviychuk, A. Petrenko, R. Singh, J. Liu, D. Makoviichuk, K. Van Wyk, A. Zhurkevich, B. Sundaralingam, et al. Dextreme: Transfer of agile in-hand manipulation from simulation to reality. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 5977–5984. IEEE, 2023. 

- [28] K. Bousmalis, G. Vezzani, D. Rao, C. Devin, A. X. Lee, M. Bauza, T. Davchev, Y. Zhou, A. Gupta, A. Raju, et al. Robocat: A self-improving foundation agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ , 2023. 

13 

- [29] H. F. Song, A. Abdolmaleki, J. T. Springenberg, A. Clark, H. Soyer, J. W. Rae, S. Noury, A. Ahuja, S. Liu, D. Tirumala, et al. V-mpo: On-policy maximum a posteriori policy optimization for discrete and continuous control. _arXiv preprint arXiv:1909.12238_ , 2019. 

- [30] A. Gupta, J. Yu, T. Z. Zhao, V. Kumar, A. Rovinsky, K. Xu, T. Devlin, and S. Levine. Resetfree reinforcement learning via multi-task learning: Learning dexterous manipulation behaviors without human intervention. In _2021 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6664–6671. IEEE, 2021. 

- [31] T. Yu, S. Kumar, A. Gupta, S. Levine, K. Hausman, and C. Finn. Gradient surgery for multitask learning. _Advances in Neural Information Processing Systems_ , 33:5824–5836, 2020. 

- [32] A. Mandlekar, D. Xu, J. Wong, S. Nasiriany, C. Wang, R. Kulkarni, L. Fei-Fei, S. Savarese, Y. Zhu, and R. Mart´ın-Mart´ın. What matters in learning from offline human demonstrations for robot manipulation. In _Conference on Robot Learning_ , pages 1678–1690. PMLR, 2022. 

- [33] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pages 991–1002. PMLR, 2022. 

- [34] S. Dasari, J. Wang, J. Hong, S. Bahl, Y. Lin, A. Wang, A. Thankaraj, K. Chahal, B. Calli, S. Gupta, et al. Rb2: Robotic manipulation benchmarking with a twist. _arXiv preprint arXiv:2203.08098_ , 2022. 

- [35] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18995–19012, 2022. 

- [36] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei. Imagenet: A large-scale hierarchical image database. In _2009 IEEE conference on computer vision and pattern recognition_ , pages 248–255. Ieee, 2009. 

- [37] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta. R3m: A universal visual representation for robot manipulation. _arXiv preprint arXiv:2203.12601_ , 2022. 

- [38] S. Parisi, A. Rajeswaran, S. Purushwalkam, and A. Gupta. The unsurprising effectiveness of pre-trained vision models for control. _arXiv preprint arXiv:2203.03580_ , 2022. 

- [39] A. Majumdar, K. Yadav, S. Arnaud, Y. J. Ma, C. Chen, S. Silwal, A. Jain, V.-P. Berges, P. Abbeel, J. Malik, et al. Where are we in the search for an artificial visual cortex for embodied intelligence? _arXiv preprint arXiv:2303.18240_ , 2023. 

- [40] R. Shah and V. Kumar. Rrl: Resnet as representation for reinforcement learning. _arXiv preprint arXiv:2107.03380_ , 2021. 

- [41] M. Sharma, C. Fantacci, Y. Zhou, S. Koppula, N. Heess, J. Scholz, and Y. Aytar. Lossless adaptation of pretrained vision models for robotic manipulation. In _The Eleventh International Conference on Learning Representations_ . 

- [42] N. Hansen, Z. Yuan, Y. Ze, T. Mu, A. Rajeswaran, H. Su, H. Xu, and X. Wang. On pretraining for visuo-motor control: Revisiting a learning-from-scratch baseline. _arXiv preprint arXiv:2212.05749_ , 2022. 

- [43] S. Tellex, T. Kollar, S. Dickerson, M. Walter, A. Banerjee, S. Teller, and N. Roy. Understanding natural language commands for robotic navigation and mobile manipulation. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 25, pages 1507–1514, 2011. 

- [44] C. Lynch and P. Sermanet. Language conditioned imitation learning over unstructured data. _arXiv preprint arXiv:2005.07648_ , 2020. 

14 

- [45] S. Stepputtis, J. Campbell, M. Phielipp, S. Lee, C. Baral, and H. Ben Amor. Languageconditioned imitation learning for robot manipulation tasks. _Advances in Neural Information Processing Systems_ , 33:13139–13150, 2020. 

- [46] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, R. Julian, et al. Do as i can, not as i say: Grounding language in robotic affordances. In _Conference on Robot Learning_ , pages 287–318. PMLR, 2023. 

- [47] A. Nguyen, D. Kanoulas, L. Muratore, D. G. Caldwell, and N. G. Tsagarakis. Translating videos to commands for robotic manipulation with deep recurrent neural networks. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3782–3788. IEEE, 2018. 

- [48] H. Bharadhwaj, A. Gupta, and S. Tulsiani. Visual affordance prediction for guiding robot exploration. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [49] Y. Zhou, Y. Aytar, and K. Bousmalis. Manipulator-independent representations for visual imitation. _arXiv preprint arXiv:2103.09016_ , 2021. 

- [50] L. Shao, T. Migimatsu, Q. Zhang, K. Yang, and J. Bohg. Concept2robot: Learning manipulation concepts from instructions and human demonstrations. _The International Journal of Robotics Research_ , 40(12-14):1419–1434, 2021. 

- [51] K. Shaw, S. Bahl, and D. Pathak. Videodex: Learning dexterity from internet videos. In _Conference on Robot Learning_ , pages 654–665. PMLR, 2023. 

- [52] H. Bharadhwaj, A. Gupta, S. Tulsiani, and V. Kumar. Zero-shot robot manipulation from passive human videos. _arXiv preprint arXiv:2302.02011_ , 2023. 

- [53] S. Bahl, A. Gupta, and D. Pathak. Human-to-robot imitation in the wild. _arXiv preprint arXiv:2207.09450_ , 2022. 

- [54] S. Bahl, R. Mendonca, L. Chen, U. Jain, and D. Pathak. Affordances from human videos as a versatile representation for robotics. _arXiv preprint arXiv:2304.08488_ , 2023. 

- [55] K. Rao, C. Harris, A. Irpan, S. Levine, J. Ibarz, and M. Khansari. Rl-cyclegan: Reinforcement learning aware simulation-to-real. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 11157–11166, 2020. 

- [56] I. Kapelyukh, V. Vosylius, and E. Johns. Dall-e-bot: Introducing web-scale diffusion models to robotics. _arXiv preprint arXiv:2210.02438_ , 2022. 

- [57] M. Minderer, A. Gritsenko, A. Stone, M. Neumann, D. Weissenborn, A. Dosovitskiy, A. Mahendran, A. Arnab, M. Dehghani, Z. Shen, et al. Simple open-vocabulary object detection with vision transformers. _arXiv preprint arXiv:2205.06230_ , 2022. 

- [58] D. P. Kingma and M. Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- [59] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- [60] C. Mitash, F. Wang, S. Lu, V. Terhuja, T. Garaas, F. Polido, and M. Nambi. Armbench: An object-centric benchmark dataset for robotic manipulation. _arXiv preprint arXiv:2303.16382_ , 2023. 

- [61] F. Ebert, C. Finn, A. X. Lee, and S. Levine. Self-supervised visual planning with temporal skip connections. _CoRL_ , 12:16, 2017. 

15 

- [62] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo, et al. Segment anything. _arXiv preprint arXiv:2304.02643_ , 2023. 

- [63] J. Yang, M. Gao, Z. Li, S. Gao, F. Wang, and F. Zheng. Track anything: Segment anything meets videos. _arXiv preprint arXiv:2304.11968_ , 2023. 

- [64] E. Perez, F. Strub, H. De Vries, V. Dumoulin, and A. Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 32, 2018. 

- [65] S. Y. Gadre, M. Wortsman, G. Ilharco, L. Schmidt, and S. Song. Clip on wheels: Zero-shot object navigation as object localization and exploration. _arXiv preprint arXiv:2203.10421_ , 2022. 

- [66] S. Haddadin, S. Parusel, L. Johannsmeier, S. Golz, S. Gabl, F. Walch, M. Sabaghian, C. J¨ahne, L. Hausperger, and S. Haddadin. The franka emika robot: A reference platform for robotics research and education. _IEEE Robotics & Automation Magazine_ , 29(2):46–64, 2022. 

- [67] V. Kumar and E. Todorov. Mujoco haptix: A virtual reality system for hand manipulation. In _2015 IEEE-RAS 15th International Conference on Humanoid Robots (Humanoids)_ , pages 657–663. IEEE, 2015. 

- [68] N. M. M. Shafiullah, Z. J. Cui, A. Altanzaya, and L. Pinto. Behavior transformers: Cloning _k_ modes with one stone. _arXiv preprint arXiv:2206.11251_ , 2022. 

- [69] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. _arXiv preprint arXiv:1810.04805_ , 2018. 

16 

|Heat Soup|Serve Soup|Baking Prep|Making Tea|Cleaning Up|Stow Bowl|
|---|---|---|---|---|---|
|Flap-Open Oven|Flap-Open Oven|Slide-Open Drawer|Uncap Lid|Pick Lid|Slide-Open Drawer|
|Pick Bowl|Pick Bowl|Pick Butter|Place Lid|Cap Lid|Pick Bowl|
|Slide-In Bowl|Slide-Out Bowl|place Butter|Pick Tea|Slide-Close Drawer|Place Bowl|
|Flap-Close Oven|Flap-Close Oven|Slide-Close Drawer|Place Tea<br>Pick Lid|Flap-Close Oven<br>Pick Towel|Slide-Close Drawer|


Table 2: List of activities (Top Row) and the associated tasks for each activity. 

## **A Dataset details** 

MT-ACT uses 7,500 human teleoperated demonstrations from the _RoboSet_ dataset<sup>3</sup> . MT-ACT dataset consisted of RGB and depth frames from four camera views (right, left, top, and wrist) as shown in figure 6, Franka joint positions and velocities, end-effector/gripper position and velocities, controls applied to the Franka joints and end-effector/gripper, and the time-steps (40 steps). 

The data was collected using an Oculus Quest 2 controller on a kitchen table-top setup at 5Hz and saved in HDF5 format. Rollouts from the data are shown in Figure 11 as well as in `https: //robopen.github.io/roboset/` . 

### **A.1 Dataset Terminology** 

**Skill** Different works in robotics often assign different meanings when they refer to “skills”. In our work, we refer to a skill when the robot performs a similar motion across different object instances (both shape and size). For instance, pick, place, open, close objects are considered as different skills. Since our dataset contains articulated objects if the “open” skill with multiple objects results in different motion we classify them as different skills. For instance, “Open Drawer” requires interacting with a prismatic joint while “Open Oven” interacts with a revolute joint. Hence, we classify these as separate skills. Our definition is broadly similar to some previous works [5]. We use 12 skills in RoboSet – _Slide-Open, Slide-Close, Flap-Open, Flap-Close, Cap, Uncap, Pick, Place, Wipe, Plunge, Slide-in, Slide-out_ . 

**Task:** We define each instantiation of our skill with a particular object class as a different task. For instance, “Pick Mug” and “Pick Butter” correspond to the same “Pick” skill but are two different tasks. 

**Activity:** A general robot agent will eventually need to perform a sequence of tasks, e.g. make tea. We refer to such sequence of tasks as _activities_ . Table 2 lists the activities used in our work as well as tasks corresponding to each activity. Our final aim is to train a _single_ robot agent to perform all activities. 

**Policies:** We train and compare different policies in our work. We classify these policies into _singletask_ policy, _multi-task (single-activity)_ and _multi-task (universal)_ policies. As each name suggests, single-task policies are trained on specific tasks. Multi-Task (single-activity) policies are trained on all tasks belonging to an activity. Finally, Multi-Task (universal) policies are trained on all tasks and activities. Our final _RoboAgent_ is trained as a Multi-Task (universal) policy. 

### **A.2 Details on Semantic Augmentations** 

We enable two different types of scene augmentations for multiplying data, for enabling generalization to different scenes with novel distractors, and to scenes with different objects for interaction: 

> • **Augmenting interaction object:** Given the joint angle of the robot in a frame of a trajectory, we use forward kinematics to recover the robot mask as well as the end-effector position of the robot. 

> 3The full RoboSet is much more diverse and consists of 9,500 teleoperated demonstrations, 20,500 kinesthetic demonstrations in various kitchen and table-top settings. In addition, it contains about 70,000 trajectories in bin settings collected through heuristics 

17 


Figure 11: Sample task demonstrations in the `RoboSet` (visualizing four views horizontally, and five timesteps vertically), used for training. 

We use the end-effector location to prompt SegmentAnything [62] for obtaining a mask of the object being interacted with. We then inpaint the region of the object being interacted with, based on a text prompt, and keep it consistent across time by tracking with TrackAnything [63]. 

- **Augmenting background:** We use SegmentAnything [62] to randomly choose a set of objects in the background that do not overlap with the robot mask, and the mask of the object being interacted with, and inpaint the scene based on the resulting overall mask over all the objects identified by SegmentAnything. 

Note that our augmentation approaches are all automatic and do not require any manual effort in specifying masks or object meshes etc. This is in contrast to prior works that require manual specification of a fixed mask per trajectory [9], and those that require templates of object textures and meshes [8]. In addition, unlike [10], we do not require training any further modules for identifying objects through open-vocabulary detection that relies on language grounding. 

## **B Train and Evaluation Details** 

In this section we present training and evaluation details both for our methods and the baselines. 

### **B.1 Robot Environment and Evaluation Details** 

The robot environments for evaluation consist of table-top kitchen setups with diverse real objects in the scene. There are 4 cameras providing complementary views of the workspace. The robot is a Franka Emika Panda arm operated with joint position control, with an action space dimension of 8 (7 joint positions, 1 dimension for end-effector open/close). The robot arm has a two-finger gripper, and a wrist camera. The robot is operated at a frequency of 5Hz. 

### **B.2 Hyper-parameters for MT-ACT and baselines** 

Here we provide hyper-parameter details of the policy architecture. We train all policies for 2000 epochs. For the overall MT-ACT agent, trained on the augmented dataset, this takes about 48 hours on a single 2080Ti GPU with a batch size of 8. 

18 


Figure 12: Qualitative results of rollouts for L2 and L3 levels of generalization, showing tasks _open drawer_ and _pick a slab of butter_ . For L2 we introduce different distractors in the scene, and change the background tiles. For L3, in addition to changes in L2 we introduce different task objects, for example by replacing a slab of butter with a piece of watermelon, or a banana. 

Table 3: Hyper-parameters for MT-ACT 

Table 4: Hyper-parameters for RT-1 [5] 

|**Name**|**Value**|**Name**|**Value**|
|---|---|---|---|
|learning rate<br>batch size<br>fdfd i|1e-5<br>8<br>3200|learning rate<br>discrete action tokens|1e-4<br>256|
|eeorwar sze<br>Attention heads|8|batch size|64|
|<br>chunk size<br>dropout|20<br>0.1|feedforward size<br>Attention heads<br>dt|1024<br>8<br>01|
|Transformer encoder layers|4|ropou<br>Tf l|.<br>6|
|Transformer decoder layers|7|ransormer ayers<br>L Ebddi i|384|
|Language Embedding size|384|anguage meng sze||


For our baseline implementations we did a hyperparameter search for relevant parameters. For each baseline implementation we try to adapt them from their officially released code. Specificially, for RT1 [5] we use `https://github.com/google-research/robotics_transformer` for reference. On the other hand, for BET [68] we use `https://github.com/notmahi/bet` . To provide language conditioning for both baselines we use similar FiLM [64] implementation as our approach. 

For hyper-parameters we use 3 different discrete action sizes – 64, 256 and 512, we vary the learning rates from (1 _e−_ 3 _,_ 1 _e−_ 4). We use the AdamW optimizer with a weight decay range in (1 _e−_ 2 _,_ 1 _e−_ 3 _,_ 1 _e −_ 4). Our RT-1 transformer uses 6 layers with 8 parallel attention heads and each head with size 64. Each transformer uses a feedforward layer with intermediate sie of 1024. On the other hand for [68] we experiment with 3 different action cluster sizes – 64, 256 and 512. We use a similar transformer implementation for BET as RT-1. Finally, for real-world evaluation we use the hyper-parameters with lowest validation loss. 

## **C Additional Results** 

In this section, we present some additional results. First, we present results and discuss how well our multi-task policy performs when compared to single-task policies. Figure 13 compares singletask policy performance against two sets of multi-task policies for the _Heat Soup_ activity. For the first multi-task Single-Activity policy (MT Single-Activity) we only train it across all tasks within the same activity. For the latter multi-task universal multi-activity policy (MT-Universal) we train it across all tasks in all activities. From Figure 13 we see that for most tasks _MT Single-Activity_ is able to outperform single task policies. Additionally, single-task policies are able to perform well on most tasks ( _≈_ 80%) except the more challenging constrained manipulation tasks (slide-in-bowl) ( _≈_ 20%). Finally, we also observe that MT-Single-Activity can outperform MT-Universal for most tasks. This happens because the universal agent is trained to perform a much larger variety of tasks. Given the very large variety of skills (Figure 3), such multi-task training can result in some negative 

19 


Figure 13: Single-Task vs Multi-Task comparison for Heat Soup activity. Multi-Task (Single Activity) represents a multi-task policy trained on only 4 tasks in Heat-Soup activity. 

transfer compared to training on a narrowly defined skills. We believe these reduced multi-task results present useful avenues for future research. Finally, in Table 5 we show results for all tasks in all activities using our single universal policy. From the below table, we see that the universal policy is able to perform well on most tasks except the more challenging tasks such as grasping small deformable objects (Pick Tea: 40%, Pick Lid: 50%). 

|**Heat Soup**|Success|**Serve Soup**|Success|**Baking Prep**|Success|
|---|---|---|---|---|---|
|Flap-Open Oven|80%|Flap-Open Oven|90%|Slide-Open Drawer|70%|
|Pick Bowl|60%|Pick Bowl|50%|Pick Butter|70%|
|Slide-In Bowl|70%|Slide-Out Bowl|80%|place Butter|90%|
|Flap-Close Oven|50%|Flap-Close Oven|80%|Slide-Close Drawer|90%|
|**Making Tea**|Success|**Cleaning Up**|Success|**Stow Bowl**|Success|
|Uncap Lid|80%|Pick Lid|70%|Slide-Open Drawer|70%|
|Place Lid|90%|Cap Lid|100%|Pick Bowl|70%|
|Pick Tea|40%|Slide-Close Drawer|90%|Place Bowl|80%|
|Place Tea|60%|Flap-Close Oven|80%|Slide-Close Drawer|80%|
|Pick Lid|50%|Pick Towel|90%|||
|Cap Lid|70%|Wipe Counter|90%|||


Table 5: Results for different tasks using the learned **universal policy** . 

20 

