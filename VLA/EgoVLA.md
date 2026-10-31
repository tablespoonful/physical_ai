---
title: "EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos"
date: "2025-07-16"
authors: "Ruihan Yang; Qinxi Yu; Yecheng Wu; Rui Yan; Borui Li; An-Chieh Cheng"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2507.12440
pdf: https://arxiv.org/pdf/2507.12440
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.12440)** / [論文ページ](https://arxiv.org/abs/2507.12440)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **_EgoVLA_ : Learning Vision-Language-Action Models from Egocentric Human Videos** 

**Ruihan Yang**<sup>1</sup><sup>_∗_</sup> **, Qinxi Yu**<sup>2</sup><sup>_∗_</sup> **, Yecheng Wu**<sup>3</sup><sup>_,_4</sup> **, Rui Yan**<sup>1</sup> **, Borui Li**<sup>1</sup> **, An-Chieh Cheng**<sup>1</sup> **, Xueyan Zou**<sup>1</sup> , **Yunhao Fang**<sup>1</sup> , **Xuxin Cheng**<sup>1</sup> , **Ri-Zhao Qiu**<sup>1</sup> , **Hongxu Yin**<sup>4</sup> , **Sifei Liu**<sup>4</sup> , **Song Han**<sup>3</sup><sup>_,_4</sup> , **Yao Lu**<sup>4</sup> , **Xiaolong Wang**<sup>1</sup> 1UC San Diego 2UIUC 3MIT 4 NVIDIA 


Figure 1: **_EgoVLA_ .** Our vision-language-action model learns manipulation skills from egocentric human videos and transfers them to a bimanual humanoid robot. The top row illustrates the diverse manipulation behaviors demonstrated by humans in the video dataset, while the bottom row shows the robot performing egocentric dexterous manipulation based on the learned skills. 

**Abstract:** Real robot data collection for imitation learning has led to significant advances in robotic manipulation. However, the requirement for robot hardware in the process fundamentally constrains the scale of the data. In this paper, we explore training Vision-Language-Action (VLA) models using egocentric human videos. The benefit of using human videos is not only for their scale but more importantly for the richness of scenes and tasks. With a VLA trained on human video that predicts human wrist and hand actions, we can perform Inverse Kinematics and retargeting to convert the human actions to robot actions. We finetune the model using a few robot manipulation demonstrations to obtain the robot policy, namely _EgoVLA_ . We propose a simulation benchmark called _Ego Humanoid Manipulation Benchmark_ , where we design diverse bimanual manipulation tasks with demonstrations. We fine-tune and evaluate _EgoVLA_ with _Ego Humanoid Manipulation Benchmark_ and show significant improvements over baselines and ablate the importance of human data.Videos can be found on our website: `https://rchalyang.github.io/EgoVLA/` 

### **1 Introduction** 

There has been a vast advancement in robotic manipulation in the last few years, thanks to large-scale real robot data collection [1, 2]. Compared to approaches that leverage simulation, directly performing supervised learning with real robot data avoids the Sim2Real domain gap and easily increases the task complexity. To efficiently collect complex robot manipulation data, multiple teleoperation tools with joint mapping [3, 4, 5], exoskeleton [6, 7, 8], and VR devices [9, 10, 11] are proposed. While this is encouraging, the requirement of a robot and an expert operator fundamentally constrains the scale of the data to be collected. 

How about learning manipulation from human videos? If we consider human as a special format of robot, there are 8 billion robots continuously operating across the world in all the environments 


Figure 2: **_EgoVLA_** takes visual history, language instruction, and action query token as input. The latent features are converted to human action with the action head. We use the wrist pose and MANO hand parameter[18] as human action space. 

that we would like robots to operate in. Recent work on Hand-Object Interaction prediction [12] has shown promising results in forecasting long-term human intention on manipulation. If we are able to leverage such human data to train a robot policy, it easily scales up not only the number of training data, but more importantly the diversity of tasks and scenes. It allows training on scenes where the current robot might not easily fit in or tasks that are even challenging for teleoperation. 

Our key observation is: The difference between human action and robot action spaces might not be that large, and it can be approximated by a few geometric transforms. Instead of training a Robot Vision-Language-Action (VLA) model on robot data [13, 14, 15, 16], we propose to train a Human Egocentric VLA ( _EgoVLA_ ) on human data. Specifically, given a few frames of visual observation language instruction, and current hand pose as input, the VLA will predict human actions in a few steps in the future. The action space includes the human wrist and hand joint angles. This human action space can be converted to a robot action space by converting wrist location to end-effector location through Inverse Kinematics and converting human hand joints to robot hand joints through retargeting. Thus the Human VLA is inherently already a robot policy, except the inputs are human hand images and there is still error in action outputs. We can correct this by further fine-tuning the VLA with a few robot demonstrations collected by teleoperation. In this way, we do not require large-scale robot data for training. 

To benchmark robotic manipulation, we propose a new humanoid bimanual manipulation benchmark based on NVIDIA IsaacSim[17], namely _Ego Humanoid Manipulation Benchmark_ . In this benchmark, we provide 12 tasks including simple tasks that perform atomic actions and longhorizon tasks that combine multiple atomic actions. We collect 100 demonstrations per task and evaluate models using the benchmark. In our experiments, we first train our _EgoVLA_ on our EgoCentric Human Manipulation dataset and fine-tune on the humanoid manipulation demonstration collected for specific tasks. In our simulation benchmark, our _EgoVLA_ outperforms different specialist and generalist baselines in both short-horizon and long-horizon tasks and achieves better generalization across visual observation and spatial locations. 

### **2 Related Work** 

**Dexterous Manipulation:** Research in dexterous manipulation has progressed from control-based methods [19, 20, 21, 22, 23, 24, 25] to learning-driven approaches [26, 27]. While early work emphasized precision, generalization across diverse scenarios remained limited. Learning-based methods introduced pose vector generation [28, 29, 30], intermediate representations [31, 32], and contact maps [33, 34], but large-scale dexterous manipulation remains an open challenge. Recent efforts leverage egocentric human videos for training task-specific policies [35, 36]. In contrast, we aim to develop generalist manipulation models directly from egocentric human demonstrations. 

**Vision-Language-Action (VLA):** Vision-Language Models (VLMs)[37, 38, 39] have shown strong generalization across multimodal tasks[40, 41, 42, 43, 44]. Building on this, Vision-Language- 

2 

Action Models (VLAs)[16, 14, 45, 13, 15, 46] fine-tune VLMs with large-scale robot data, enabling perception-action integration. However, VLA training is data-intensive, often requiring extensive teleoperation[47, 48] or scripted execution [49, 50]. OpenVLA [14] and Octo [13] leverage crowdsourced robot datasets [1] but face scalability bottlenecks. We propose an alternative: learning policies from human egocentric videos, augmented by small-scale target-domain fine-tuning. 

**Egocentric Vision:** Egocentric vision research [51, 52, 53] traditionally faced limitations in data scale and diversity. Recent datasets [54, 55] improve coverage but focus on activities beyond current robotic capabilities. Simpler datasets [56, 57] capture everyday interactions but lack pose annotations. We address this by curating a targeted mixture of datasets and introducing an Egocentric Human Video Dataset (Section 3.1) optimized for dexterous manipulation learning. 

**Learning from In-the-Wild Video:** Several works [58, 59] propose extracting affordances or interaction cues from in-the-wild videos. Motivated by egocentric vision, recent studies [60, 61, 62, 63, 64, 65, 66] pretrain representations using human videos, showing ~~<u><mark>positive transfer.</mark></u>~~ ~~<mark>However, most</mark>~~ focus on unsupervised learning without leveraging fine-grained han ~~<mark>d or wrist pose information. Our</mark>~~ work instead uses high-quality egocentric data within the VLA fra ~~<mark>mework to directly improve dex-</mark>~~ terous policy learning, capitalizing on advances in wearable hand-t ~~<mark>racking tech</mark> nologies.~~ 

### **3 Learning Manipulation Skills from Ego-centric Human Videos** 

In this section, we describe the construction of our egocentric human manipulation dataset, the training of _EgoVLA_ on this dataset, bridging the embodiment gap between humans and humanoid robots, and the deployment of _EgoVLA_ for manipulation tasks. 

#### **3.1 Ego-Centric Human Manipulation Dataset** 


Following insights from language model and vision-language model training, Human Video Dataset Split we emphasize the importance of dataset structure in driving model perfor13% mance. We construct a large-scale human egocentric manipulation dataset 23% focused on skill-rich video sequences with accompanying pose annotations. 25% The combined dataset contains egocentric RGB observations, wrist poses, hand poses, and camera poses. Our dataset integrates sequences from four 39% sources with their relative proportions shown in Fig. 3: **HOI4D** consists of 4,000 videos capturing one-handed manipulations such as pick-and-place, reTACO HoloAssist orientation, and articulated object interaction. **HOT3D** provides 833 minutes HOI4D HOT3D of video interacting with 33 rigid objects, with precise 3D hand and camera Figure 3: **Human** pose annotations. **HoloAssist** offers 166 hours of recordings of complex tasks **Data** such as battery replacement, furniture assembly, and machine setup. Although its hand pose annotations are noisier, it captures rich bimanual interactions. To avoid overrepresentation of HoloAssist, which has noisier labels, we uniformly sampled 1/10 of it to balance tasks and sources. **TACO** includes 2,317 motion sequences covering 151 tool-action-object triplets. 

**Data Processing:** Egocentric videos introduce challenges for learning due to continuous camera motion. To mitigate this, we use world-frame camera poses to project future wrist positions into the current camera frame, ensuring consistent supervision. Training samples are generated by sampling RGB observations at 3 FPS, balancing computational efficiency and temporal continuity. In total, our dataset comprises approximately 500,000 image-action pairs across diverse manipulation tasks. 

#### **3.2** **_EgoVLA_ Model** 

We build _EgoVLA_ on top of a vision-language model to leverage strong visual and semantic reasoning. Specifically, we use _NVILA-2B_ [67] as the backbone for its robust vision-language understanding and compact size, enabling both intention inference and efficient fine-tuning. As shown in Fig.2, _EgoVLA_ takes as input current and historical egocentric visual observations, language instructions, action query tokens, and human proprioception. These inputs are encoded by the VLM backbone and further processed by an action head to predict future human or robot actions. 

3 


Figure 4: **Unified Action Space:** MANO hand parameters are used as a shared action space for humans and robots. For robot hands, during training, optimized mano parameters produce the same fingertip position as the robot hand fingertip. A small MLP maps predicted finger tip positions to joint commands during deployment. 

Visual Observations consists of six RGB frames: the current observation and five preceding frames, sampled at 0 _._ 2sec intervals, covering a 1sec history. Each frame has a resolution of 384 _×_ 384. Language Instructions describe the immediate desired behavior. This design focuses the model on skill execution rather than high-level planning, ensuring a clear mapping between language input and predicted actions. Human Proprioception State includes wrist translations/rotations, and hand pose parameters. These are processed through MLPs before being passed to the action head. 

Each predicted action includes the wrist pose (3D translation and rotation in rot6D representation [68] in the camera frame) and hand joint angles, represented using the top 15 PCA components of the MANO hand model [18]. _EgoVLA_ is trained to regress future wrist poses in the camera frame and hand joint parameters. The objective is: _L_ = _λ_ wrist trans _L_ wrist trans + _λ_ wrist rot _L_ wrist rot + _λ_ joint _L_ joint. _L_ wrist trans and _L_ joint are L2 losses for wrist translation and hand joint angle regression. _L_ wrist rot is a rotation loss for rot6D[68] wrist orientation. _λ_ joint _, λ_ wrist trans _, λ_ wrist rot are weighting coefficients. Full loss details are provided in the Supplementary Materials. 

**Action Head & Action Query Tokens:** The action head is a transformer (300M) consisting of six encoder layers, each with a hidden size of 1536. It takes as input the human (or robot) proprioception state and the latent embeddings corresponding to the action query tokens, and predicts a sequence _At_ = [ _at, at_ +1 _, . . . , at_ + _H_ ] over a 1-second horizon (30 future steps at 30 Hz) for both hands. We use the last _H_ = 30 word IDs from the vocabulary as action query tokens. 

**Training Details:** We first pretrain _EgoVLA_ on our Ego-Centric Human Manipulation Dataset for 20 epochs. This is followed by 115 epochs of post-training on robot demonstration data, where the learning rate is reduced after 100 epochs. During training, the full model, including the visual encoder, is fine-tuned.Further training configurations are detailed in the Supplementary Materials. 

#### **3.3 Transferring** **_EgoVLA_ to Humanoid Robot** 

Humans and humanoid robots share a similar manipulation framework using two arms and hands. However, directly transferring _EgoVLA_ to humanoid robots is challenging due to differences in camera pose, hand morphology, and visual appearance. To enable the deployment, we fine-tune _EgoVLA_ using a small set of robot demonstrations, leveraging a unified action space as in Fig. 4 and we provide more details regarding the Humanoid Robot data in Sec. 4 

**Retargeting robot data to human representation:** To fine-tune on robot data, we first align the robot’s action space with the human representation. For end-effector poses, 3D transformations align the robot and human coordinate systems. Aligning hand configurations is more complex: we estimate MANO [18] parameters that best approximate the robot hand’s actuation by minimizing the discrepancy between predicted and observed fingertip positions: minimize _L_ ( **Θ** ) = **Θ** 

51 �5 _i_ =1<sup>SmoothL1(</sup><sup>**J**pred(</sup><sup>**Θ**)</sup><sup>_i,_</sup><sup>**J**obs</sup><sup>_,i_)where</sup><sup>**Θ**</sup><sup>_∈_R15aretheMANOhandparameters,</sup><sup>**J**pred(</sup><sup>**Θ**)</sup> are fingertip positions computed via MANO forward kinematics, and **J** obs _∈_ R<sup>5</sup><sup>_×_3</sup> are the observed robot fingertip positions. This unified action space enables direct fine-tuning of _EgoVLA_ on robot demonstrations without requiring additional architectural changes or reinitialization. 

4 


Figure 5: **Task Visualization.** All simulated tasks with predicted wrist trajs from _EgoVLA_ . 

**Mapping human hand to robot hand:** At inference time, the wrist and hand poses predicted by _EgoVLA_ are mapped to the robot’s actuators, as illustrated in Fig. 4 (bottom row). Wrist poses are first converted into robot end-effector poses through 3D transformations, and the corresponding arm joint angles are solved via inverse kinematics (IK). For hand actuation, we use the MANO model to calculate 3D hand keypoints from the predicted MANO parameters. A lightweight MLP then predicts the robot’s hand joint commands given 3D hand keypoints. This MLP is trained on robot demonstrations where hand actuations are retargeted into human hand representations. This mapping achieves a mean fingertip position error of 5 _×_ 10<sup>_−_5</sup> _,_ m. Furthermore, replaying raw demonstrations through this retargeting pipeline preserves task validity, indicating that the small errors introduced during retargeting do not significantly affect control performance. Additional implementation details are provided in the Supplementary Materials. 

### **4** **_Ego Humanoid Manipulation Benchmark_** 

Beyond data scarcity, a major challenge in learning-based robotics is the lack of scalable, robust, and reproducible evaluation. Real-world evaluation is often costly, time-consuming, and raises concerns around safety and reproducibility—barriers that disproportionately affect resource-constrained settings such as academic labs. Recent work [69] has shown that simulation-based evaluations are highly correlated with real-world performance, supporting their use as a reliable proxy. To enable consistent benchmarking of humanoid manipulation, we introduce the _Ego Humanoid Manipulation Benchmark_ , built using NVIDIA Isaac Lab [70]. _Ego Humanoid Manipulation Benchmark_ is not designed for direct sim-to-real transfer. Instead, we leverage simulation, similar to LIBERO [71] and SIMPLER [69]—as a controlled and reproducible testbed for evaluating manipulation policies. Our simulated platform features the Unitree H1 [72] humanoid robot with two Inspire dexterous hands [73], and includes 12 manipulation tasks spanning both **Short Horizon** atomic actions (Push-Box, Flip-Mug, Pour-Balls, Close-Drawer, Open-Drawer, Open-Laptop, Stack-Can) and **Long-Horizon** , multi-stage skills (Sort-Cans, Insert-Cans, Unload-Cans, Insert-And-Unload-Cans, Stack-Can-Into-Drawer), as shown in Fig. 5. 

**Observation & Action Space:** Our benchmark provides robot joint positions, end-effector poses, contact forces, and egocentric RGB-D visual input for observations. While _EgoVLA_ uses only egocentric vision, end-effector poses, hand joint actuation, and task descriptions, additional modalities are available for future research. The robot is controlled via end-effector control for arms and PD joint control for hands. Each hand has 12 DoFs (6 active, 6 mimic joints). The final 36-dimensional action space combines arm inverse kinematics with direct hand actuation. Control frequency is 30 Hz. We also provide per-step success indicators and sub-task completion flags for every task. Definitions and success metrics for each sub-task are detailed in the supplementary materials. 

**Diverse Visual Background:** Simulation allows full control over visual conditions. We includes 5 room textures (Room 1–5) and 5 table textures (Table 1–5), generating 25 distinct visual background combinations for robust generalization evaluation. 

**Demonstrations:** To support imitation learning, we provide expert demonstrations collected via OpenTelevision [10] using the Meta Quest 3. Demonstrations are collected using Room 1, 2, or 3, with Table 1 fixed. For each task, we collect 100 successful demonstrations, with episode lengths ranging from 100 to 500 frames depending on task complexity. 

5 


Figure 6: **Visual Instruction Following.** Top: original HOI4D samples with corresponding language instructions. Red lines indicate ground-truth human wrist trajectories, and green lines denote predictions. Bottom: results with modified instructions while keeping the same visual input. _EgoVLA_ adjusts predicted trajectories appropriately according to the new instructions, demonstrating its understanding of language and environment. 

Table 1: **Evaluation on Short-Horizon Tasks on Seen/Unseen Visual Configurations** 

||Stack-Can|Push|-Box<br>Open-|Drawer Close-|Drawer|Flip-|Mug|Pour|-Balls|Open-Laptop|M|ean|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Method|SR_↑_PSR_↑_|SR_↑_|PSR_↑_SR_↑_|PSR_↑_<br>SR_↑_|PSR_↑_|SR_↑_|PSR_↑_|SR_↑_|PSR_↑_|SR_↑_<br>PSR_↑_|SR_↑_|PSR_↑_|
||||See  i|n Visual Config|iuration||||||||
|ACT [5]|22.22 22.22|11.11|85.19 18.52|66.67<br>48.15|96.30|7.40|7.40|3.70|77.78|62.96<br>62.96|24.87|59.79|
|EgoVLA-NoPretrain [38]|55.56 55.56|51.85|75.93 59.26|77.78 100.00|100.00|3.70|3.70|85.19|93.83|96.30<br>96.30|64.55|71.87|
|_EgoVLA_ (50%)<br>**_EgoVLA_**|44.44 44.44 <br>77.78<br>77.78|33.33 <br>70.37|66.67 22.22 <br>83.33<br>59.26|61.73 100.00 <br>81.48<br>100.00|100.00 <br>100.00|22.22 <br>59.26|22.22 <br>59.26|77.78 <br>77.78|92.59 <br>92.59|37.04<br>44.44 <br>100.00<br>100.00|48.15 <br><br>77.78|61.73<br>84.92|
||||Unse  i|en Visual Confi|iguration|i|||||||
|ACT [5]|9.09 10.61|18.18|87.88 24.24|71.97<br>63.64|96.97|0.00|0.00|6.06|59.09|53.03<br>53.03|24.89|54.22|
|EgoVLA-NoPretrain [38]|57.58 57.58|69.70|82.58 46.15|71.28<br>86.36|89.90|4.69|4.69|46.03|79.37|48.48<br>53.03|51.28|62.63|
|**_EgoVLA_**|62.12<br>62.12|75.76|84.85<br>50.00|75.25<br>98.48|98.48|30.77|30.77|83.33|94.44|83.33<br>87.88|69.11|76.26|


### **5 Experiments** 

#### **5.1 Human Manipulation Modeling** 

Before directly evaluating robotic manipulation performance, we first assess how well _EgoVLA_ models human hand motion after training on the Human Ego-Centric Manipulation Dataset. Quantitatively, the average future prediction error for the human wrist translation is approximately 8 _,_ cm. When projected onto the 2D image plane, the normalized error is around 0 _._ 13, comparable to stateof-the-art results reported in HOI-forecast [74]. To further examine whether _EgoVLA_ captures environmental context and follows language instructions, we sample examples from the HOI4D evaluation set, modifying the original language prompts while keeping the visual inputs unchanged. As shown in the third column of Fig. 6, when the instruction changes from _Put it in the drawer_ to _Take it out of the drawer_ , the predicted hand trajectories shift from moving into the drawer to moving toward the cabinet surface. Similarly, in the second column, altering the instruction from _Put something in it_ to _Open and close the door_ results in trajectories shifting from placing objects inside the safe to interacting with the safe’s door. These results demonstrate that _EgoVLA_ not only accurately models human motion, but also learns the underlying semantic intent behind the actions. 

#### **5.2 Humanoid Robot Evaluation** 

We evaluate the manipulation performance of different models using two metrics: _Success Rate (SR)_ , measuring overall task success, and _Progress Rate (PSR)_ , defined as the average number of completed subtasks relative to the total subtasks in a long-horizon task. 

**Baselines:** We compare _EgoVLA_ against two baselines: (1) _EgoVLA-NoPretrain_ , which fine-tunes the pre-trained VLM on robot demonstrations without human video pretraining; (2) _ACT_ , which trains a separate specialist transformer for each task individually. For ACT, we adopt the recommended training settings. 

**Evaluation Setup:** We assess model performance under two settings: **Seen** , where visual backgrounds are identical to those encountered during training, and **Unseen** , where backgrounds are entirely novel. To promote robustness, object positions are **randomized** at the start of each roll- 

6 

Table 2: **Evaluation on Long-Horizon Tasks on Seen/Unseen Visual Configurations** . 

||Insert-An|d-Unload-C|ans Stack-Ca|n-Into-Drawer<br>Sort|-Cans|Unloa|d-Cans|Insert-Cans|M|ean|
|---|---|---|---|---|---|---|---|---|---|---|
|Method|SR_↑_|PSR_↑_|SR_↑_|PSR_↑_<br>SR_↑_|PSR_↑_|SR_↑_|PSR_↑_|SR_↑_PSR_↑_|SR_↑_|PSR_↑_|
||||Seen Vis i|ual Configuration|||||||
|ACT [5]|0.00|11.11|11.11|37.04<br>0.00|28.63|0.00|35.80|0.00 19.75|2.22|26.47|
|EgoVLA-NoPretrain [38]|7.41|45.93|0.00|18.52<br>51.85|79.63|62.96|75.00|11.11 55.56|26.67|54.93|
|_EgoVLA_ (50%)|0.00|28.15|29.63|57.41<br>0.00|33.33|0.00|30.56|7.41 49.07|7.41|39.70|
|**_EgoVLA_**|44.44|77.04|40.74|75.93<br>55.56|88.89|66.67|83.33|22.22<br>78.70|45.93|80.78|
||||Unseen V i|isual Configuration|||||||
|ACT [5]|0.00|7.95|1.52|33.84<br>0.00|20.71|1.52|33.83|0.00 21.21|0.61|23.51|
|EgoVLA-NoPretrain [38]|0.00|29.09|0.00|20.08<br>15.15|45.83|34.85|55.68|6.06 30.30|11.21|36.20|
|**_EgoVLA_**|31.82|76.97|28.79|60.98<br>18.18|68.94|50.00|75.76|15.15<br>62.88|28.79|69.11|


out, with placement constrained to regions not seen during training. Detailed specifications for background splits and object randomization ranges (up to 20cm _×_ 20cm) are provided in the supplementary materials. For **Seen** backgrounds, each model is evaluated with 27 rollouts per task: nine episodes for each of three backgrounds. For **Unseen** backgrounds, each model is evaluated with 66 rollouts per task: three episodes for each of 22 unseen backgrounds. 

We use simulation to ensure reproducible and robust evaluation, but the method itself is modalityagnostic and can learn effectively from any high-quality teleoperated demonstrations, whether collected in simulation or the real world. 

**_EgoVLA_ Requires Robot Data Post-training:** While _EgoVLA_ is pretrained on egocentric human videos using a unified action space, zero-shot deployment on humanoid robots without fine-tuning on robot data results in 0% success across all tasks. This failure stems from appearance, perception, and kinematic mismatches between humans and robots. Even for tasks seen during pretraining (e.g., _Pouring Balls_ ), execution fails without robot-specific adaptation, highlighting the need for post-training on in-domain robot data. 

**Ego-centric Human Pretraining Improves In-Domain Performance:** We first evaluate models on **Seen** visual backgrounds. As shown in Table 1 and Table 2, _EgoVLA_ consistently outperforms the _EgoVLA-NoPretrain_ baseline across both short- and long-horizon tasks. Gains are especially pronounced on tasks requiring fine-grained manipulation, such as _Stack-Cans_ , _Sort-Cans_ , _InsertAnd-Unload-Cans_ , and _Flip-Mugs_ . We attribute this to the human pretraining phase, during which _EgoVLA_ learns general manipulation skills involving ”hands” independent of embodiment (human or robot). In contrast, _EgoVLA-NoPretrain_ learns solely from robot demonstrations without such transferable priors. Moreover, the performance gap between _EgoVLA_ and _EgoVLA-NoPretrain_ is larger for long-horizon tasks, achieving approximately 20% higher success rates. Compared to the specialist _ACT_ baselines, generalist models ( _EgoVLA_ and _EgoVLA-NoPretrain_ ) perform substantially better on both short- and long-horizon tasks. This is likely because specialist models must simultaneously learn low-level manipulation and long-horizon planning from scratch, whereas generalist models leverage shared low-level skills across tasks. 

**Ego-centric Human Pretraining Enhances Out-of-Domain Generalization:** As shown in Table 1, _EgoVLA_ maintains strong generalization in short-horizon tasks on **Unseen** visual backgrounds, with only a minor drop in mean success rate, whereas _EgoVLA-NoPretrain_ exhibits a substantial 23% decline. For long-horizon tasks, as shown in Table 2, _EgoVLA_ achieves around 30% success on unseen backgrounds. Although success rates decline compared to seen environments, the progress rate remains similar, suggesting that failures primarily occur at the final stages of task execution rather than early subgoals. This demonstrates that pretraining on egocentric human videos significantly improves _EgoVLA_ ’s ability to generalize to novel environments. 

**Ablation Study — Robot Data Scale:** To analyze the contributions of human video pretraining and robot demonstration fine-tuning, we train a variant of _EgoVLA_ using only 50% of the robot demonstrations, denoted as _EgoVLA (50%)_ . As shown in Table 1 and Table 2, while _EgoVLA (50%)_ can still complete some tasks, its overall success rate drops substantially, particularly on long-horizon tasks (from 45.93% to 7.41%). These results suggest that, although pretraining on egocentric hu- 

7 


Figure 7: **Data Mixture Ablation.** _EgoVLA_ pretrained on different mixtures of human egocentric datasets, evaluated on **Unseen** visual backgrounds for short-horizon tasks. Greater diversity consistently improves generalization performance. 


Figure 8: **Spatial Distribution.** Success rate and progress of _EgoVLA_ under **Unseen** visual backgrounds, visualized across object spawning positions. The model maintains strong performance across a wide area, with higher success in regions commonly associated with effective bimanual manipulation. 


Figure 9: **Robot Trajectories (left to right).** In the top row, the robot inserts two cans into the tray and unloads them, and in the bottom row, the robot puts the can over the saucer and closes the drawer. 

man videos significantly improves both in-domain performance and generalization, _EgoVLA_ still requires a moderate amount of task-specific robot demonstrations to achieve strong performance. 

**Ablation Study - Pretrain Data Mixture:** To further assess the impact of pretraining data composition, we pretrain _EgoVLA_ using different data mixtures, as shown in Fig. 7. Results show that increasing the scale and diversity of human pretraining data consistently improves downstream performance, with both average Success Rate (SR) and Progress Rate (PSR) increasing across tasks. Notably, despite noisy hand annotations in HoloAssist, missing language labels in HOT3D, and limited visual diversity in TACO, we still observe positive transfer, highlighting the robustness of our approach to dataset imperfections. 

**Performance of** **_EgoVLA_ Conditioned on Object Spawning Positions:** Beyond generalization to diverse visual backgrounds, we further analyze model performance conditioned on object spawning positions. As shown in Fig. 8, we visualize the success rate under _Unseen_ visual backgrounds for short-horizon tasks and the average progress for long-horizon tasks. For short-horizon tasks, we observe that success rates are higher when objects are placed closer to the center of the randomized region. For long-horizon tasks, two distinct high-probability regions emerge. We hypothesize that this arises because many long-horizon tasks involve bimanual operations, with each peak corresponding to successful interactions using either the left or right hand. 

**Trajectory Visualization:** To complement quantitative evaluation, we visualize policy rollouts for long-horizon tasks in Fig. 9. We display the sequence of visual observations alongside the predicted wrist trajectories produced by _EgoVLA_ . For clarity, only the future wrist positions are visualized. Despite training with only 100 demonstrations per task, _EgoVLA_ successfully executes diverse long-horizon tasks while demonstrating strong spatial and visual generalization. Additional trajectory visualizations are provided in the supplementary materials. 

### **6 Conclusion** 

In this work, we present _EgoVLA_ , a vision-language-action model trained on egocentric human videos for dexterous manipulation. _EgoVLA_ is developed through pretraining a vision-language model on large-scale human egocentric manipulation dataset, and fine-tuning on a small set of robot demonstrations. To enable transfer across embodiments, we introduce a unified action space that aligns human and robot hand representations. Experimental results demonstrate that human video pretraining enables _EgoVLA_ to learn a generalist manipulation policy, achieving strong performance across diverse tasks with limited robot data, with strong generalization ability. 

8 

### **7 Limitation** 

Our pretraining framework requires human data with hand and wrist pose annotations, which may limit data availability. However, the increasing accessibility of high-fidelity AR/VR devices (e.g., Quest 3, Vision Pro, Aria Glasses) is expected to ease this constraint. Additionally, although _EgoVLA_ is pretrained with a unified action space, it cannot be directly deployed for manipulation without further fine-tuning on a moderate amount of robot data. Future work may explore improving zero-shot transferability through more embodiment-agnostic pretraining. 

### **References** 

- [1] Q. Vuong, S. Levine, H. R. Walke, K. Pertsch, and A. S. et al. Open x-embodiment: Robotic learning datasets and RT-x models. In _CoRL_ , 2023. 1, 3 

- [2] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, P. D. Fagan, J. Hejna, M. Itkina, M. Lepert, Y. J. Ma, P. T. Miller, J. Wu, S. Belkhale, S. Dass, H. Ha, A. Jain, A. Lee, Y. Lee, M. Memmel, S. Park, I. Radosavovic, K. Wang, A. Zhan, K. Black, C. Chi, K. B. Hatch, S. Lin, J. Lu, J. Mercat, A. Rehman, P. R. Sanketi, A. Sharma, C. Simpson, Q. Vuong, H. R. Walke, B. Wulfe, T. Xiao, J. H. Yang, A. Yavary, T. Z. Zhao, C. Agia, R. Baijal, M. G. Castro, D. Chen, Q. Chen, T. Chung, J. Drake, E. P. Foster, J. Gao, D. A. Herrera, M. Heo, K. Hsu, J. Hu, D. Jackson, C. Le, Y. Li, K. Lin, R. Lin, Z. Ma, A. Maddukuri, S. Mirchandani, D. Morton, T. Nguyen, A. O’Neill, R. Scalise, D. Seale, V. Son, S. Tian, E. Tran, A. E. Wang, Y. Wu, A. Xie, J. Yang, P. Yin, Y. Zhang, O. Bastani, G. Berseth, J. Bohg, K. Goldberg, A. Gupta, A. Gupta, D. Jayaraman, J. J. Lim, J. Malik, R. Mart´ın-Mart´ın, S. Ramamoorthy, D. Sadigh, S. Song, J. Wu, M. C. Yip, Y. Zhu, T. Kollar, S. Levine, and C. Finn. Droid: A large-scale in-the-wild robot manipulation dataset. 2024. 1 

- [3] A. Iyer, Z. Peng, Y. Dai, I. Guzey, S. Haldar, S. Chintala, and L. Pinto. Open teach: A versatile teleoperation system for robotic manipulation. _arXiv preprint arXiv:2403.07870_ , 2024. 1 

- [4] S. Dass, W. Ai, Y. Jiang, S. Singh, J. Hu, R. Zhang, P. Stone, B. Abbatematteo, and R. MartinMartin. Telemoma: A modular and versatile teleoperation system for mobile manipulation. _arXiv preprint arXiv:2403.07869_ , 2024. 1 

- [5] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _RSS_ , 2023. 1, 6, 7, 18 

- [6] L. Zhao, T. Yang, Y. Yang, and P. Yu. A wearable upper limb exoskeleton for intuitive teleoperation of anthropomorphic manipulators. _Machines_ , 11(4):441, 2023. 1 

- [7] H. Fang, H.-S. Fang, Y. Wang, J. Ren, J. Chen, R. Zhang, W. Wang, and C. Lu. Airexo: Lowcost exoskeletons for learning whole-arm manipulation in the wild. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 15031–15038. IEEE, 2024. 1 

- [8] S. Yang, M. Liu, Y. Qin, D. Runyu, L. Jialong, X. Cheng, R. Yang, S. Yi, and X. Wang. Ace: A cross-platfrom visual-exoskeletons for low-cost dexterous teleoperation. _arXiv preprint arXiv:240_ , 2024. 1 

- [9] A. Naceri, D. Mazzanti, J. Bimbo, Y. T. Tefera, D. Prattichizzo, D. G. Caldwell, L. S. Mattos, and N. Deshpande. The vicarios virtual reality interface for remote robotic teleoperation: Teleporting for intuitive tele-manipulation. _Journal of Intelligent & Robotic Systems_ , 101: 1–16, 2021. 1 

- [10] X. Cheng, J. Li, S. Yang, G. Yang, and X. Wang. Open-television: Teleoperation with immersive active visual feedback. _arXiv preprint arXiv:2407.01512_ , 2024. 1, 5 

9 

- [11] R. Ding, Y. Qin, J. Zhu, C. Jia, S. Yang, R. Yang, X. Qi, and X. Wang. Bunny-visionpro: Realtime bimanual dexterous teleoperation for imitation learning. 2024. URL `https://arxiv. org/abs/2407.03162` . 1 

- [12] J. Tian, L. Yang, R. Ji, Y. Ma, L. Xu, J. Yu, Y. Shi, and J. Wang. Gaze-guided hand-object interaction synthesis: Benchmark and method. _arXiv preprint arXiv:2403.16169_ , 2024. 2 

- [13] Octo Model Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, C. Xu, J. Luo, T. Kreiman, Y. Tan, L. Y. Chen, P. Sanketi, Q. Vuong, T. Xiao, D. Sadigh, C. Finn, and S. Levine. Octo: An open-source generalist robot policy. In _RSS_ , 2024. 2, 3 

- [14] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn. OpenVLA: An open-source vision-language-action model. In _CoRL_ , 2024. 2, 3 

- [15] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint_ , 2024. 2, 3 

- [16] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint_ , 2023. 2, 3 

- [17] NVIDIA. Isaac sim: Advanced simulation for robotics development, 2024. Accessed: Jun 2024. 2 

- [18] J. Romero, D. Tzionas, and M. J. Black. Embodied hands: Modeling and capturing hands and bodies together. _ACM Transactions on Graphics, (Proc. SIGGRAPH Asia)_ , 36(6), Nov. 2017. 2, 4, 15, 18 

- [19] A. Rodriguez, M. T. Mason, and S. Ferry. From caging to grasping. _IJRR_ , 2012. 2 

- [20] C. Rosales, R. Su´arez, M. Gabiccini, and A. Bicchi. On the synthesis of feasible and prehensile robotic grasps. In _ICRA_ , 2012. 2 

- [21] D. Prattichizzo, M. Malvezzi, M. Gabiccini, and A. Bicchi. On the manipulability ellipsoids of underactuated robotic hands with compliance. _RAS_ , 2012. 2 

- [22] J. Ponce, S. Sullivan, J.-D. Boissonnat, and J.-P. Merlet. On characterizing and computing three-and four-finger force-closure grasps of polyhedral objects. In _ICRA_ , 1993. 2 

- [23] J. Ponce, S. Sullivan, A. Sudsang, J.-D. Boissonnat, and J.-P. Merlet. On computing four-finger equilibrium and force-closure grasps of polyhedral objects. _IJRR_ , 1997. 2 

- [24] Y. Zheng and C.-M. Chew. Distance between a point and a convex cone in _n_ -dimensional space: Computation and applications. _T-RO_ , 2009. 2 

- [25] H. Dai, A. Majumdar, and R. Tedrake. Synthesis and optimization of force closure grasps via sequential semidefinite programming. _ISRR_ , 2018. 2 

- [26] O. M. Andrychowicz, B. Baker, M. Chociej, R. Jozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray, et al. Learning dexterous in-hand manipulation. _IJRR_ , 2020. 2 

- [27] A. Nagabandi, K. Konolige, S. Levine, and V. Kumar. Deep dynamics models for learning dexterous manipulation. In _CoRL_ , 2020. 2 

- [28] H. Jiang, S. Liu, J. Wang, and X. Wang. Hand-object contact consistency reasoning for human grasps generation. In _ICCV_ , 2021. 2 

10 

- [29] E. Corona, A. Pumarola, G. Alenya, F. Moreno-Noguer, and G. Rogez. Ganhand: Predicting human grasp affordances in multi-object scenes. In _CVPR_ , 2020. 2 

- [30] L. Yang, X. Zhan, K. Li, W. Xu, J. Li, and C. Lu. Cpf: Learning a contact potential field to model the hand-object interaction. In _ICCV_ , 2021. 2 

- [31] L. Shao, F. Ferreira, M. Jorda, V. Nambiar, J. Luo, E. Solowjow, J. A. Ojea, O. Khatib, and J. Bohg. Unigrasp: Learning a unified model to grasp with multifingered robotic hands. _RA-L_ , 2020. 2 

- [32] A. Wu, M. Guo, and C. K. Liu. Learning diverse and physically feasible dexterous grasps with generative model and bilevel optimization. _CoRL_ , 2022. 2 

- [33] S. Brahmbhatt, A. Handa, J. Hays, and D. Fox. Contactgrasp: Functional multi-finger grasp synthesis from contact. In _IROS_ , 2019. 2 

- [34] D. Turpin, L. Wang, E. Heiden, Y.-C. Chen, M. Macklin, S. Tsogkas, S. Dickinson, and A. Garg. Grasp’d: Differentiable contact-rich grasp synthesis for multi-fingered hands. In _ECCV_ , 2022. 2 

- [35] R.-Z. Qiu, S. Yang, X. Cheng, C. Chawla, J. Li, T. He, G. Yan, D. J. Yoon, R. Hoque, L. Paulsen, G. Yang, J. Zhang, S. Yi, G. Shi, and X. Wang. Humanoid policy human policy, 2025. URL `https://arxiv.org/abs/2503.13441` . 2 

- [36] S. Kareer, D. Patel, R. Punamiya, P. Mathur, S. Cheng, C. Wang, J. Hoffman, and D. Xu. Egomimic: Scaling imitation learning via egocentric video, 2024. URL `https://arxiv. org/abs/2410.24221` . 2 

- [37] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al. Gpt-4 technical report. _arXiv preprint_ , 2023. 2 

- [38] J. Lin, H. Yin, W. Ping, P. Molchanov, M. Shoeybi, and S. Han. Vila: On pre-training for visual language models. In _CVPR_ , 2024. 2, 6, 7 

- [39] S. Tong, E. Brown, P. Wu, S. Woo, M. Middepogu, S. C. Akula, J. Yang, S. Yang, A. Iyer, X. Pan, et al. Cambrian-1: A fully open, vision-centric exploration of multimodal llms. _arXiv preprint_ , 2024. 2 

- [40] S. Pratt, I. Covert, R. Liu, and A. Farhadi. What does a platypus look like? generating customized prompts for zero-shot image classification. In _ICCV_ , 2023. 2 

- [41] Y. Alaluf, E. Richardson, S. Tulyakov, K. Aberman, and D. Cohen-Or. Myvlm: Personalizing vlms for user-specific queries. In _ECCV_ , 2025. 2 

- [42] W. Kuo, Y. Cui, X. Gu, A. Piergiovanni, and A. Angelova. Open-vocabulary object detection upon frozen vision and language models. In _ICLR_ , 2023. 2 

- [43] D.-A. Huang, S. Liao, S. Radhakrishnan, H. Yin, P. Molchanov, Z. Yu, and J. Kautz. Lita: Language instructed temporal-localization assistant. In _ECCV_ , 2025. 2 

- [44] T. Lv, Y. Huang, J. Chen, Y. Zhao, Y. Jia, L. Cui, S. Ma, Y. Chang, S. Huang, W. Wang, et al. Kosmos-2.5: A multimodal literate model. _arXiv preprint_ , 2023. 2 

- [45] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, R. Cheng, C. Shen, Y. Peng, F. Feng, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _arXiv preprint_ , 2024. 3 

11 

- [46] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL `https://arxiv.org/abs/2504.16054` . 3 

- [47] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, J. Gao, J. Emmons, A. Gupta, E. Orbay, et al. Roboturk: A crowdsourcing platform for robotic skill learning through imitation. In _CoRL_ , 2018. 3 

- [48] A. Mandlekar, S. Nasiriany, B. Wen, I. Akinola, Y. Narang, L. Fan, Y. Zhu, and D. Fox. Mimicgen: A data generation system for scalable robot learning using human demonstrations. In _CoRL_ , 2023. 3 

- [49] S. Dasari, F. Ebert, S. Tian, S. Nair, B. Bucher, K. Schmeckpeper, S. Singh, S. Levine, and C. Finn. Robonet: Large-scale multi-robot learning. In _CoRL_ , 2019. 3 

- [50] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke, et al. Scalable deep reinforcement learning for vision-based robotic manipulation. In _CoRL_ , 2018. 3 

- [51] D. Damen, H. Doughty, G. M. Farinella, A. Furnari, E. Kazakos, J. Ma, D. Moltisanti, J. Munro, T. Perrett, W. Price, et al. Rescaling egocentric vision: Collection, pipeline and challenges for epic-kitchens-100. _IJCV_ , 2022. 3 

- [52] G. A. Sigurdsson, A. K. Gupta, C. Schmid, A. Farhadi, and A. Karteek. Actor and observer: Joint modeling of first and third-person videos. In _CVPR_ , 2018. 3 

- [53] Y. Li, Z. Ye, and J. M. Rehg. Delving into egocentric actions. In _CVPR_ , 2015. 3 

- [54] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In _CVPR_ , 2022. 3 

- [55] K. Grauman, A. Westbury, L. Torresani, K. Kitani, J. Malik, T. Afouras, K. Ashutosh, V. Baiyya, S. Bansal, B. Boote, et al. Ego-exo4d: Understanding skilled human activity from first-and third-person perspectives. In _CVPR_ , 2024. 3 

- [56] F. Mahdisoltani, G. Berger, W. Gharbieh, D. Fleet, and R. Memisevic. On the effectiveness of task granularity for transfer learning. _arXiv preprint_ , 2018. 3 

- [57] D. Damen, H. Doughty, G. M. Farinella, S. Fidler, A. Furnari, E. Kazakos, D. Moltisanti, J. Munro, T. Perrett, W. Price, et al. Scaling egocentric vision: The epic-kitchens dataset. In _ECCV_ , 2018. 3 

- [58] S. Bahl, R. Mendonca, L. Chen, U. Jain, and D. Pathak. Affordances from human videos as a versatile representation for robotics. 2023. 3 

- [59] C. Wen, X. Lin, J. So, K. Chen, Q. Dou, Y. Gao, and P. Abbeel. Any-point trajectory modeling for policy learning, 2023. 3 

- [60] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta. R3m: A universal visual representation for robot manipulation, 2022. URL `https://arxiv.org/abs/2203.12601` . 3 

- [61] A. Majumdar, K. Yadav, S. Arnaud, Y. J. Ma, C. Chen, S. Silwal, A. Jain, V.-P. Berges, T. Wu, J. Vakil, P. Abbeel, J. Malik, D. Batra, Y. Lin, O. Maksymets, A. Rajeswaran, and F. Meier. Where are we in the search for an artificial visual cortex for embodied intelligence? In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. URL `https://openreview.net/forum?id=6qLzQeFGio` . 3 

12 

- [62] S. Karamcheti, S. Nair, A. S. Chen, T. Kollar, C. Finn, D. Sadigh, and P. Liang. Languagedriven representation learning for robotics. In _Robotics: Science and Systems (RSS)_ , 2023. 3 

- [63] J. Yang, B. Liu, J. Fu, B. Pan, G. Wu, and L. Wang. Spatiotemporal predictive pre-training for robotic motor control, 2024. URL `https://arxiv.org/abs/2403.05304` . 3 

- [64] J. Zeng, Q. Bu, B. Wang, W. Xia, L. Chen, H. Dong, H. Song, D. Wang, D. Hu, P. Luo, et al. Learning manipulation by predicting interaction. _arXiv preprint arXiv:2406.00439_ , 2024. 3 

- [65] S. Ye, J. Jang, B. Jeon, S. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin, L. Liden, K. Lee, J. Gao, L. Zettlemoyer, D. Fox, and M. Seo. Latent action pretraining from videos, 2024. URL `https://arxiv.org/abs/2410.11758` . 3 

- [66] W. Lirui, C. Xinlei, Z. Jialiang, and H. Kaiming. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. In _Neurips_ , 2024. 3 

- [67] Z. Liu, L. Zhu, B. Shi, Z. Zhang, Y. Lou, S. Yang, H. Xi, S. Cao, Y. Gu, D. Li, X. Li, Y. Fang, Y. Chen, C.-Y. Hsieh, D.-A. Huang, A.-C. Cheng, V. Nath, J. Hu, S. Liu, R. Krishna, D. Xu, X. Wang, P. Molchanov, J. Kautz, H. Yin, S. Han, and Y. Lu. Nvila: Efficient frontier visual language models, 2025. URL `https://arxiv.org/abs/2412.04468` . 3 

- [68] Y. Zhou, C. Barnes, J. Lu, J. Yang, and H. Li. On the continuity of rotation representations in neural networks, 2020. URL `https://arxiv.org/abs/1812.07035` . 4, 17 

- [69] X. Li, K. Hsu, J. Gu, K. Pertsch, O. Mees, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, S. Levine, J. Wu, C. Finn, H. Su, Q. Vuong, and T. Xiao. Evaluating real-world robot manipulation policies in simulation, 2024. URL `https://arxiv.org/abs/2405.05941` . 5 

- [70] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mazhar, A. Mandlekar, B. Babich, G. State, M. Hutter, and A. Garg. Orbit: A unified simulation framework for interactive robot learning environments. _IEEE Robotics and Automation Letters_ , 8(6):3740–3747, 2023. doi:10.1109/LRA.2023.3270034. 5 

- [71] B. Liu, Y. Zhu, C. Gao, Y. Feng, Q. Liu, Y. Zhu, and P. Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning, 2023. URL `https://arxiv.org/abs/2306. 03310` . 5 

- [72] U. Robotics. H1, 2024. Accessed: Sep 2024. 5 

- [73] I. Robots. The dexterous hands, 2024. Accessed: Jul 2024. 5 

- [74] S. Liu, S. Tripathi, S. Majumdar, and X. Wang. Joint hand motion and interaction hotspots prediction from egocentric videos. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 6 

- [75] X. Wang, T. Kwon, M. Rad, B. Pan, I. Chakraborty, S. Andrist, D. Bohus, A. Feniello, B. Tekin, F. V. Frujeri, N. Joshi, and M. Pollefeys. Holoassist: an egocentric human interaction dataset for interactive ai assistants in the real world. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 20270–20281, October 2023. 15, 16 

- [76] Y. Liu, Y. Liu, C. Jiang, K. Lyu, W. Wan, H. Shen, B. Liang, Z. Fu, H. Wang, and L. Yi. Hoi4d: A 4d egocentric dataset for category-level human-object interaction. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 21013–21022, June 2022. 15, 16, 18, 19, 22 

- [77] Y. Liu, H. Yang, X. Si, L. Liu, Z. Li, Y. Zhang, Y. Liu, and L. Yi. Taco: Benchmarking generalizable bimanual tool-action-object understanding. _arXiv preprint arXiv:2401.08399_ , 2024. 15, 16 

13 

- [78] P. Banerjee, S. Shkodrani, P. Moulon, S. Hampali, F. Zhang, J. Fountain, E. Miller, S. Basol, R. Newcombe, R. Wang, J. J. Engel, and T. Hodan. Introducing hot3d: An egocentric dataset for 3d hand and object tracking. _arXiv preprint arXiv:2406.09598_ , 2024. 15, 18 

- [79] M. Oquab, T. Darcet, T. Moutakanni, H. V. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, R. Howes, P.-Y. Huang, H. Xu, V. Sharma, S.-W. Li, W. Galuba, M. Rabbat, M. Assran, N. Ballas, G. Synnaeve, I. Misra, H. Jegou, J. Mairal, P. Labatut, A. Joulin, and P. Bojanowski. Dinov2: Learning robust visual features without supervision, 2023. 17 

- [80] T. Darcet, M. Oquab, J. Mairal, and P. Bojanowski. Vision transformers need registers, 2023. 17 

- [81] NVIDIA. Nvidia omniverse: A platform for virtual collaboration and real-time simulation, 2024. Accessed: Jun 2024. 22 

14 

## **Appendix** 

### **1 Dataset Details** 

**Language Label:** The combined dataset includes ego-centric RGB visual observations, wrist poses, hand poses, and camera poses. Notably, HoloAssist, TACO and HOI4D provide specific language labels for each video clip, while HOT3D lacks language annotations. To maintain consistency across datasets, we include placeholder language instructions for HOT3D. 

**MANO Shape Parameters:** To streamline the problem, we use the average human hand shape provided by MANO [18], focusing on manipulation skills learning from human demonstrations. 

**Hand Pose Parameters:** For ego-centric video dataset (HoloAssist[75]) that utilize hand model other than MANO[18], we retarget the provided hand poses to the MANO [18] representation, ensuring unified modeling. 

Section 3.1 presents an overview of our Ego-Centric Human Video Dataset. Here, we provide a detailed visualization of the task distribution for HOI4D [76] and HoloAssist [75], as shown in Fig. 10. The task distribution for HOT3D[78] is not visualized, as task labels are not provided for its sequences. 

For HOI4D [76], we show the task descriptions across all sequences, while for HoloAssist [75] and TACO [77], we illustrate the verbs from the action descriptions. To enhance clarity, a logarithmic scale is applied to the frequency distributions for both datasets. As shown in Fig. 10, all datasets provide ego-centric human video across diverse tasks. 

15 


Figure 10: **Human Video Distribution.** We visualize the human video task distribution over all HOI4D [76], HoloAssist [75] and TACO [77] sequences. 

16 

### **2 Training Details** 

#### **2.1** **_EgoVLA_ Training Details** 

We provide detailed training configurations to ensure the faithful reproduction of our results. All models were trained using 32 A100 GPUs. 

**Training Objectives:** Our full training objective is defined as follows: 

_L_ = _λ_ wrist trans _L_ wrist trans + _λ_ wrist rot _L_ wrist rot + _λ_ joint _L_ joint 

where _L_ wrist trans = _∥_ **T** pred _−_ **T** gt _∥_ 2<sup>2isL2lossforwristtranslationregression.</sup><sup>**T**predisthepre-</sup> dicted wrist translation in the camera frame, and **P** gt is the ground-truth wrist translation. _L_ wrist rot = _∥_ **R** pred _−_ **R** gt _∥_ 2<sup>2istherotationlossforwristrotationpredictionwhere</sup><sup>**R**predisthepredictedwrist</sup> rotation in the camera frame, and **R** gt is the ground-truth wrist rotation. Our model predicts rotation in rot6d[68], and we convert the predicted rotation to rotation matrix before compute the loss. _L_ joint = _∥_ **Θ** pred _−_ **Θ** gt _∥_ 2<sup>2isL2lossforhandjointangleregression,where</sup><sup>**Θ**predarethepredicted</sup> MANO parameters, and **Θ** gt are the ground-truth MANO parameters. _λ_ joint _, λ_ wrist trans _, λ_ wrist rot are weights to balance different terms. 

We use the following hyperparameters for training on our ego-centric human video dataset and during fine-tuning with robot demonstrations (as in Table 3). 

Table 3: Hyper Parameters for Pretraining on Human Videos 

|Hyper Parameter Name|Pretraining<br>On Human Video Data|Post-Training<br>On Robot Demonstrations|
|---|---|---|
|Epoch|20|115|
|Batch Size|16 * 8 * 4|16 * 8 * 4|
|Learing Rate (LR)|1e-4|2e-5 (2e-6 after 100epochs)|
|LR Scheduling|Cosine|Constant|
|Action Head Hidden Size|1536|1536|
|Action Head Transformer Layers|6|6|
|_λ_wrist trans|20.0|20.0|
|_λ_wrist rot|5.0|5.0|
|_λ_joint|5.0|5.0|


#### **2.2 ACT Training Details** 

All ACT models were trained using 3 NVIDIA RTX A4000. To obtain a more thorough assessment of performance on ACT, we trained ACT policies for each task with new settings. We replace the visual backbone with DinoV2 [79][80]. Rather than padding episodes with the last frame, we modified the dataloader to randomly select an episode and a segment from the dataset. We set action chunk size to 64 for short horizon task Close-Drawer and 128 for the others. We use the following hyperparameters for training ACT models(as in Table 4). 

Table 4: Hyper Parameters for ACT models 

|Name|Value|
|---|---|
|Epoch|50000|
|Batch Size|50|
|Learing Rate|1e-4|
|Backbone|DinoV2|
|Transformer Hidden Dimension|512|
|Encoder Layer|4|
|Decoder Layer|7|
|Number of Heads|8|


17 

### **3 Detailed Action Formulation** 

#### **3.1 Inference** 

As described in Section 3, our _EgoVLA_ generates _H_ = 30 actions per timestep at a frequency of 30 Hz, predicting actions for a 1-second future window. When deployed on the humanoid robot in simulation, the policy operates at 30 Hz. To enhance the smoothness of the robot’s behavior and incorporate long-term planning capabilities, we employ action-chunking as described in ALOHA [5]. For smoothing, we use a parameter value of 0.8. 

#### **3.2 Detailed MANO Hand Parameterization** 

The MANO hand model [18] includes 15 ball joints with 45 degrees of freedom (DOFs). However, the human hand lacks this level of flexibility. To address this, MANO provides a low-rank representation using PCA. Consistent with HOI4D [76] and HOT3D [78], we adopt the first 15 principal components of the PCA representation for hand pose parameterization, effectively representing the action space in a compact yet expressive form. 

#### **3.3 Retargeting during deployment** 

To ensure consistency between training and inference, we train a compact MLP for retargeting. Specifically, this retargeting MLP takes as input the 3D fingertip positions in the wrist frame of both hands and outputs the actuation values for all degrees of freedom (DOFs) of both hands. 

The retargeting MLP is a four-layer neural network with hidden layer sizes of [64, 128, 64]. Its training data is derived from the process of converting robot demonstrations into human hand representations, as detailed in Sec.3. By employing this retargeting MLP, we not only achieve consistent retargeting results across training and inference but also enhance inference speed. 

Table 5: Hyper Parameters for Retargeting MLP 

|Name|Value|
|---|---|
|Epoch|2000|
|Batch Size|2048|
|Learing Rate|0.001|


18 

### **4 Human Prediction Visualization** 

In addition to the instruction-following results presented in Sec.5, this section provides additional visualizations of human trajectory predictions. We showcase the predicted future hand trajectories alongside the ground truth trajectories in Fig. 11. As illustrated, our _EgoVLA_ produces accurate and consistent predictions across diverse scenes, object instances, and tasks. All these human videos are never seen by the model during training. 

In Fig. 11a, the hand trajectory shows the approach to the knife, followed by lifting it and cutting the apple. Fig.11b and Fig.11c depict clear hand movements along the door’s rotational axis during operation. In Fig. 11g, our model accurately predicts the placement position within the drawer. Lastly, in Fig.11d and Fig.11e, the predictions remain consistent across different kettle instances, indicating the model’s ability to understand the shared semantics of similar objects. 


Figure 11: **Human Trajectory Prediction** : The green dotted lines are the future human hand trajectories predicted by our _EgoVLA_ and the red dotted lines are the ground-truth future human hand trajectories. All sequences are from our evaluation set built upon HOI4D [76] dataset. The language sequence descriptions are also provided as captions for each sequence. 

19 

### **5 Policy Trajectories Visualization** 

In addition to the policy trajectories discussed in Sec.5, this section provides additional visualizations of policy rollouts for various tasks. We present short-horizon task trajectories in Fig.12 and Fig.12. These figures highlight our model’s ability to perform fundamental manipulation skills, including: Pushing: Illustrated in Fig. 12b. Grasping and Placing: Shown in Fig. 12d. 

In Fig. 13, our model demonstrates its capacity to integrate these atomic skills from short-horizon tasks to solve diverse long-horizon tasks using a single generalist policy. For example: In Fig. 13d, the policy successfully executes a long-horizon task involving picking up a can, stacking the on the saucer and closing the drawer. In Fig. 13e, the policy achieves a sequence of actions to sort four different cans. This involves picking up each can and placing it in the correct container consecutively, demonstrating the model’s accuracy and consistency in long-horizon tasks. 


Figure 12: **Robot Trajectories for Short-Horizon Tasks** . We visualize the policy trajectories for short-horizon tasks in our _Ego Humanoid Manipulation Benchmark_ . The green dotted lines are the future robot hand trajectories predicted by our _EgoVLA_ . 

20 


Figure 13: **Robot Trajectories for Long-Horizon Tasks.** We visualize the policy trajectories for long-horizon tasks in our _Ego Humanoid Manipulation Benchmark_ . The green dotted lines are the future robot hand trajectories predicted by our _EgoVLA_ . 

21 

### **6 Humanoid Manipulation Benchmark Details** 

#### **6.1 Assets** 

The asset library combines models from NVIDIA Omniverse [81] and 3D-scanned meshes from HOI4D [76], with modifications (e.g., added handles) to improve manipulability. We also fine-tune physics parameters to ensure realistic interactions while maintaining simulation efficiency. 

#### **6.2 Detailed Task Lists and Language Instruction for Every Task** 

- **Pour-Balls** : ”Pour balls in cup into bowl” 

- **Push-Box** : ”Push box to the marker” 

- **Close-Drawer** : ”Close the opened drawer” 

- **Open-Drawer** : ”Open the closed drawer” 

- **Flip-Mug** : ”Flip the mug” 

- **Open-Laptop** : ”Open the laptop” 

- **Stack-Can** : ”Put can on the saucer” 

- **Sort-Cans** : ”Put sprite cans to the left box, and orange cans to the right box” 

- **Insert-Cans** : ”Insert cans into the boxes” 

- **Insert-And-Unload-Cans** : ”Insert the right can into the slot and insert the left can into the slot, unload the right cans and then unload the left cans” 

- **Unload-Cans** : ”Unload the right cans and then unload the left cans” 

- **Stack-Can-Into-Drawer** : ”Put can on the saucer, and Close the drawer” 

#### **6.3 Object Randomization Range Visualization** 

We provide the visualization for range of object randomization. Objects are randomized within a rectangle. The visualization of object at upper left and bottom right corners is shown in Fig. 14. 

#### **6.4 Environment Background Visualization** 

We provide a visualization of the diverse background of the environments. In total, we include 5 rooms and 5 tables, which can be combined in various configurations. The visualization of rooms and tables is shown in Fig. 15. 

#### **6.5 Training & Evaluation Visual Configuration Visualization** 

We provide a visualization of the training and evaluation visual configuration. As shown in Fig. 16 and discussed in the main paper, we collect and train our models with three visual configurations and evaluate models on 22 unseen visual configurations. 

#### **6.6 Simulation Details and Success & Subtask definitions** 

To maintain a control frequency of 30 Hz, the simulation decimation and render interval are set based on the time step (dt), calculated as: 

simulation decimation = render interval = 

1 

30 _∗ dt_ 

For each environment, the detailed physics parameters and task definitions are provided below: 

- **Push-Box** 

**–** Physics Parameters: 

22 


Figure 14: **Object Randomization Range** 


Figure 15: **Diverse Environment Background** : we included 5 different rooms and 5 different tables resulting 25 different visual configurations 

23 


Figure 16: **Training & Evaluation Configuration** 

      - <sup>Physics simulation time-step in seconds (</sup><sup>_dt_):</sup> 1201 

      - <sup>Box contact offset (in meters):0.02</sup> 

   - Task Definition: 

      - <sup>Final task success if distance between box and goal marker is smaller than 0.08.</sup> 

      - <sup>Subtask reach success if distance between end effector(EE) and box is smaller than</sup> 0.13. 

- **Flip-Mug** 

   - Physics Parameters: 

      - <sup>dt:</sup> 2401 

      - <sup>Mug collision approximation:SDF Mesh</sup> 

      - <sup>Mug contact offset:0.002</sup> 

   - Task Definition: 

      - <sup>Finaltasksuccessifzunitvector(unitvectorinworldframepointingupwards)</sup> transformed by mug frame has z value greater than 0.5. 

      - <sup>Subtask reach success if distance between EE and mug is smaller than 0.12.</sup> 

- **Pour-Balls** 

   - Physics Parameters: 

      - <sup>dt:</sup> 2401 

      - <sup>Mug collision approximation:SDF Mesh</sup> 

      - <sup>Mug contact offset:0.002</sup> 

      - <sup>Ball contact offset:0.002</sup> 

   - Task Definition: 

      - <sup>Final task success if at least 3 balls are within the mug</sup> 

      - <sup>Subtask reach success if distance between EE and bottle is smaller than 0.12.</sup> 

      - <sup>Subtask lift success if height of bottle increases by at least 0.06.</sup> 

- **Sort-Cans** 

   - Physics Parameters: 

      - <sup>dt:</sup> 1201 

      - <sup>Can collision approximation:Convex hull</sup> 

      - <sup>Mug contact offset:0.0015</sup> 

24 

   - <sup>Container collision approximation:Convex Decomposition</sup> 

   - <sup>Container contact offset:0.0015</sup> 

- Task Definition: 

   - <sup>Final task success if both Sprite cans are inside the left container and both Fanta</sup> cans are inside the right container 

   - <sup>Subtask reaches success if the distance between EE and can is smaller than 0.12.</sup> Value of subtask reach represents the number of cans that satisfy the condition. 

   - <sup>Subtaskliftsuccessifheightofthecanincreasesbyatleast0.06.Valueofthe</sup> subtask lift represents the number of cans that satisfy the condition. 

   - <sup>Subtask sort represents the number of cans that are inside the correct container.</sup> 

#### • **Insert-Cans** 

- Physics Parameters: 

<u>1</u> 

   - <sup>dt:</sup> 1201 

   - <sup>Can collision approximation:Convex hull</sup> 

   - <sup>Can contact offset:0.0015</sup> 

   - <sup>Container collision approximation:SDF Mesh</sup> 

   - <sup>Container contact offset:0.002</sup> 

- Task Definition: 

   - <sup>Final task success if cans x,y coordinates are within the container and the z value</sup> is smaller than the threshold for inserted cans (1.065) 

   - <sup>Subtask reaches success if the distance between EE and can is smaller than 0.12.</sup> Value of subtask reach represents the number of cans that satisfy the condition. 

   - <sup>Subtaskliftsuccessifheightofthecanincreasesbyatleast0.06.Valueofthe</sup> subtask lift represents the number of cans that satisfy the condition. 

   - <sup>Subtask insert represents the number of cans that are inserted.</sup> 

#### • **Unload-Cans** 

   - Physics Parameters: 

      - <sup>dt:</sup> 1201 

      - <sup>Can collision approximation:Convex hull</sup> 

      - <sup>Can contact offset:0.0015</sup> 

      - <sup>Container collision approximation:SDF Mesh</sup> 

      - <sup>Container contact offset:0.002</sup> 

   - Task Definition: 

      - <sup>Final task success if cans x,y coordinates are not within the container, and can is</sup> standing upwards on the table (same calculation as Flip-Mug), and height of can is greater than table surface 

      - <sup>Subtask reach success if distance between EE and can is smaller than 0.12.Value</sup> of subtask reach represents the number of cans that satisfy the condition. 

      - <sup>Subtask lift success if height of can increases by at least 0.06.Value of subtask lift</sup> represents the number of cans that satisfy the condition. 

      - <sup>Subtask unload represents the number of cans that are unloaded.</sup> 

- **Insert-And-Unload-Cans** 

   - Physics Parameters: 

      - <sup>dt:</sup> 

<u>1</u> 

      - 120 

   - <sup>Can collision approximation:Convex hull</sup> 

   - <sup>Can contact offset:0.0015</sup> 

   - <sup>Container collision approximation:SDF Mesh</sup> 

   - <sup>Container contact offset:0.002</sup> 

- Task Definition: 

25 

      - <sup>Final task success if cans are inserted first then unloaded</sup> 

      - <sup>Subtask reach success if distance between EE and can is smaller than 0.12.Value</sup> of subtask reach represents the number of cans that satisfy the condition. 

      - <sup>Subtask lift success if height of can increases by at least 0.06.Value of subtask lift</sup> represents the number of cans that satisfy the condition. 

      - <sup>Subtask insert represents the number of cans that are inserted.</sup> 

      - <sup>Subtask unload represents the number of cans that are unloaded.</sup> 

- **Close-Drawer** 

   - Physics Parameters: 

      - <sup>dt:</sup> <u>1</u> 

240 

      - <sup>Drawer body collision approximation:Convex Decomposition</sup> 

      - <sup>Drawer door collision approximation:SDF Mesh</sup> 

      - <sup>Drawer contact offset:0.01</sup> 

   - Task Definition: 

      - <sup>Final task success if drawer is fully closed</sup> 

      - <sup>Subtask reach success if distance between EE and handle on drawer door is smaller</sup> than 0.12 

      - <sup>Subtask move-door success if drawer is closed at least 10% of its joint range</sup> 

- **Open-Drawer** 

   - Physics Parameters: 

      - <sup>dt:</sup> <u>1</u> 

240 

      - <sup>Drawer body collision approximation:Convex Decomposition</sup> 

      - <sup>Drawer door collision approximation:SDF Mesh</sup> 

      - <sup>Drawer contact offset:0.01</sup> 

   - Task Definition: 

      - <sup>Final task success if drawer is fully open</sup> 

      - <sup>Subtask reach success if distance between EE and handle on drawer door is smaller</sup> than 0.12 

      - <sup>Subtask move-door success if drawer is open at least 10% of its joint range</sup> 

- **Stack-Can** 

   - Physics Parameters: 

      - <sup>dt:</sup> 

         - <u>1</u> 

         - 120 

      - <sup>Can collision approximation:Convex hull</sup> 

      - <sup>Can contact offset:0.0015</sup> 

      - <sup>Plate collision approximation:Convex Decomposition</sup> 

      - <sup>Plate contact offset:auto computed</sup> 

   - Task Definition: 

      - <sup>Final task success if horizontal distance (calculated using x,y coordinates) between</sup> can and plate is smaller than radius of plate and difference in z values is smaller than 0.02 

      - <sup>Subtask place success if horizontal distance (calculated using x,y coordinates) be-</sup> tween can and plate is smaller than radius of plate and difference in z values is smaller than 0.05 

- **Stack-Can-Into-Drawer** 

   - Physics Parameters: 

      - <sup>dt:</sup> 2401 

      - <sup>Can collision approximation:Convex hull</sup> 

      - <sup>Can contact offset:0.0015</sup> 

26 

- <sup>Plate collision approximation:Convex Decomposition</sup> 

- <sup>Plate contact offset:auto computed</sup> 

- <sup>Drawer body collision approximation:Convex Decomposition</sup> 

- <sup>Drawer door collision approximation:SDF Mesh</sup> 

- <sup>Drawer contact offset:0.01</sup> 

* 

   - Task Definition: 

      - <sup>Final task success if horizontal distance (calculated using x,y coordinates) between</sup> can and plate is smaller than radius of plate, difference in z values is smaller than 0.02, and drawer is close. 

      - <sup>Subtaskreach</sup> ~~d~~ rawer success if distance between left EE and drawer handle is smaller than 0.12. 

      - <sup>Subtaskreach</sup> ~~c~~ an success if distance between right EE and can is smaller than 0.12. 

      - <sup>Subtask lift success if height of can increases by at least 0.06.</sup> 

- **Open-Laptop** 

   - Physics Parameters: 

         - <u>1</u> 

      - <sup>dt:</sup> 1201 

      - <sup>Laptop body collision approximation:Convex Hull</sup> 

      - <sup>Laptop lid collision approximation:Convex Hull</sup> 

      - <sup>Laptop lid contact offset:auto computed</sup> 

   - Task Definition: 

      - <sup>Final task success if laptop is open by at least 70% of its joint range.</sup> 

      - <sup>Subtask move</sup> ~~l~~ id ~~s~~ uccess if laptop is open by at least 15% of its joint range. 

For robot hands, collision approximation for each link is Convex Decomposition, and contact offset is 0.005. 

27 

