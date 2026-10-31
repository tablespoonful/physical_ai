---
title: "Cross-Embodiment Robot Foundation World Models with Latent Actions"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/huang26bv.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/huang26bv/huang26bv.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/huang26bv/huang26bv.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/huang26bv.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Cross-Embodiment Robot Foundation World Models with Latent Actions** 

**Huang Huang**<sup>1 2</sup> **Sriram Yenamandra**<sup>1 2</sup> **Arjun Majumdar**<sup>2</sup> **Elie Aljalbout**<sup>2</sup> **Tushar Nagarajan**<sup>2</sup> **Tsung-Yen Yang**<sup>2</sup> **Akshara Rai**<sup>2</sup> **Michael Rabbat**<sup>2</sup> **Li Fei-Fei**<sup>1</sup> **Jiajun Wu**<sup>1</sup> **Tingfan Wu**<sup>2</sup> **Franziska Meier**<sup>2</sup> 

## **Abstract** 

The diversity of robot embodiments and action spaces makes it challenging to build robot world models that generalize across different embodiments. We introduce the Latent ActionConditioned Robot World Model (LAC-WM), which operates within a learned unified latent action space shared across diverse embodiments. This unified action space improves the world model’s performance when adapted to previously unseen robot embodiments. We compare LACWM with an Explicit Action-Conditioned World Model (EAC-WM), which conditions on explicit motion labels. Our results shows that explicit action conditioning leads to disjoint action representations across embodiments, limiting downstream performance when adapting to new robots. We evaluate both models on dexterous manipulation tasks and a modified LIBERO benchmark. LAC-WM improves downstream performance over EAC-WM by up to 46.7% on dexterous manipulation and 11.7% on LIBERO. Crucially, the unified latent action space allows LAC-WM’s downstream performance to scale positively with the number of embodiments used during pretraining. In contrast, the disjoint action space in EACWM leads to decreased performance as the number of pretraining embodiments increases. These results highlights the importance of a unified action space for efficient cross-embodiment learning, addressing a key challenge in robotics. 

## **1. Introduction** 

Robot action-conditioned video generation models, or _robot world models_ , offer a complementary approach to robot policies based on imitation learning, allowing robots to predict 

> 1Department of Computer Science, Stanford University, US 

> 2Work partially done while at Meta FAIR Robotics. Correspondence to: Huang Huang _<_ ravenh@stanford.edu _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

future states and evaluate planned actions before execution, improving planning and decision-making. However, a fundamental and persistent challenge in robotics is the vast and evolving diversity of robot embodiments. Robots differ widely in their physical structure, sensors and actuators, and control strategies, and new embodiments are constantly emerging. This creates a critical need for robot world models that can efficiently learn from cross-embodiment data (Zheng et al., 2025; Liu et al., 2025; Zheng et al., 2026; Doshi et al., 2024; Bu et al., 2025b) and adapt quickly to previously unseen robot forms. 

We propose learning a unified latent action space that aligns action representations across different embodiments, including both human and different robot agents. This latent space abstracts away embodiment-specific details while preserving task-relevant information, enabling the model to integrate heterogeneous data during pretraining. We show that such a unified latent space will empower the world model to learn more efficiently across embodiments during pretraining and adapt quickly to unseen embodiments through finetuning, laying the groundwork for a truly generalizable foundational world model for robotics. Latent action spaces have primarily been explored for extracting action representations from unlabeled video data (Ye et al., 2025; Chen et al., 2024). However, most robotic datasets come with action annotations, and advances in human pose estimation provide scalable motion information, including detailed hand poses and camera movements. This enables learning action spaces directly from motion data. Despite this, there is a lack of comparative analysis for action embedding alignment across different embodiments between representations derived directly from motion data and those learned through latent action models. We hypothesize that training action encoders solely on motion data leads to disjoint latent spaces for different embodiments (Figure 2), which limits cross-embodiment knowledge transfer and degrades generalization performance on unseen embodiments. 

We focus on learning a foundational robot world model that learns efficiently from cross-embodiment data during pretraining and adapts quickly to unseen embodiments through finetuning. Specifically, we investigate two key research questions: (1) _Do latent action models better unify crossembodiment action representations compared to explicit_ 

1 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 


**Figure 1. LAC-WM Architecture** . During pretraining (yellow area), the inverse dynamics model (IDM) encodes cross-embodiment image observations into a unified latent action space, as the condition for the forward dynamics model (FDM). A motion decoder translates the latent actions into motion labels, including delta human hand poses, robot end-effector actions, and camera motion. During finetuning (green area), an action projector encodes raw robot actions of unseen embodiments into the pre-trained unified latent action space. 

_action labels?_ and (2) _Does a unified action space enhance cross-embodiment robot world model learning compared to a disjoint latent space?_ We propose the Latent Action Conditioned Robot World Model (LAC-WM), which predicts future observations conditioned on a unified latent action space. LAC-WM consists of four components: an inverse dynamics model (IDM), an forward dynamics model (FDM), a motion decoder and an action projector, as in Figure 1. The IDM encodes pairs of consecutive image observations into latent actions, which condition the FDM to predict the next frame. The motion decoder, following Nikulin et al. (2025), decodes latent actions back into explicit motion labels. The IDM and FDM are trained jointly on datasets combining human manipulation videos and robot data. Since future observations, required by the IDM, are unavailable at inference time, we train an action projector that maps explicit actions into the latent action space (Gao et al., 2025), enabling the world model to directly consume action inputs. 

We evaluate LAC-WM in a cross-embodiment transfer setting, where the model is pretrained on multiple embodiments and fine-tuned on a previously unseen robot using an action projector. We compare against an explicit actionconditioned world model (EAC-WM), which directly encodes motion information into action latents. Our results show that LAC-WM produces higher-quality future predictions than EAC-WM and improves task success rate by up to 46.7% on dexterous manipulation. We further validate LAC-WM on a modified LIBERO benchmark with unseen object and location variants, where it improves the average success rate from 82.4% to 92.0% over EAC-WM. Moreover, LAC-WM exhibits positive scaling in downstream planning performance as the number of pretraining embodiments increases, whereas EAC-WM shows the opposite trend, likely due to its disjoint latent space, which hinders effective cross-embodiment learning. 

## **2. Related Work** 

**World Models in Robotics.** World models (WMs) have emerged as a way to achieve controllable video generation (Bruce et al., 2024; Zhang et al., 2025; Li et al., 2025; Po et al., 2025; Yang et al., 2024; Valevski et al., 2025; Yu et al., 2025). Robotic world models serve as scalable and explainable compliments to imitation learning based policies. Prior work has explored training navigation world models (Hu et al., 2023; Bar et al., 2025; Gao et al., 2024; Hassan et al., 2025) with well-defined action spaces (e.g., velocity). Robot manipulation world models involve diverse action spaces due to differences in robot morphologies, and as a result, they typically rely on action-free video prediction during pretraining (Gupta et al., 2022; Wu et al., 2024; Assran et al., 2025), or use text or video conditioning (Agarwal et al., 2025), adding action conditioning only during finetuning (Gupta et al., 2022; Wu et al., 2024; Agarwal et al., 2025; Assran et al., 2025). Zhu et al. (2025) incorporate action conditioning for a single robot embodiment but do not evaluate cross-embodiment transfer. In contrast, LACWM directly tackles the challenge of heterogeneous action spaces with a unified latent action space, enabling efficient cross-embodiment learning and better generalization. 

**Latent Action Modeling.** Latent Action Models (LAM) have emerged as a promising approach to learn action representations from large-scale unlabeled data. Prior work has explored LAMs for training _latent action_ policies for game environments (Schmidt & Jiang, 2024), and finetuning expert-level policies from these, with limited labels. Other works have explored LAMs for robot manipulation, by extracting latent actions from large-scale unlabeled human videos as labels to fine-tune vision-language models, and subsequently vision-language-action (VLA) models (Ye et al., 2025; Chen et al., 2025; Bu et al., 2025b; Jang et al., 2025; Cui et al., 2024; Kim et al., 2025). Liang et al. (2025); 

2 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

Nikulin et al. (2025) introduced an auxiliary motion decoding loss which aligns latent actions with explicit control actions, to encourage the latent space to capture actionable content. Zhang et al. (2026) explores various best practices for training LAMs. LAC-WM also uses a motion decoding loss and learns a continuous latent action space. Instead of focusing on policy learning as in prior work, we learn a unified latent action space from cross embodiment labeled datasets, for building robot world foundation models. 

**Latent Action World Models.** Bruce et al. (2024); Ren et al. (2025) introduce a latent action model (LAM) paired with a world model, trained on datasets that include robot data. However, their approach does not involve cross-embodiment pretraining across diverse embodiments, nor does the world model support conditioning on raw robot actions at inference time. Chen et al. (2024) train LAMs with data augmentation to regularize latent actions that feed into a foundation policy and world models for robotic manipulation. However, they focus on action-free video pretraining and do not demonstrate adaptation to unseen robot embodiments. Gao et al. (2025) demonstrate that a pretrained latent actionconditioned world model can be adapted for robot manipulation by projecting raw action signals into the latent action space. But they also focus on action-free video pretraining and lack comparisons with robot world models trained using explicit action labels. In contrast, we leverages labeled cross-embodiment data for robot world model training and investigate the comparison between a learned latent action space and directly encoding the motion labels. We show a unified latent action space benefits cross-embodiment learning with better downstream robot planning performance, particularly when adapting to unseen embodiments. 

## **3. Method** 

LAC-WM is pretrained on cross-embodiment datasets and finetuned to adapt to previously unseen robot embodiments. The overall framework is in Figure 1. During pretraining (left, yellow), LAC-WM consists of an inverse dynamics model (IDM), a forward dynamics model (FDM), and a motion decoder (MD). The IDM encodes image observations into a latent action, which conditions the FDM to predict the next image latent. The MD decodes latent actions into explicit motion labels. The image prediction and motion decoding losses jointly supervise all modules. During finetuning (right, green), an action projector maps raw robot actions of an unseen robot embodiment into the latent action space, enabling the pretrained FDM to generate rollouts conditioned on embodiment-specific actions. 

### **3.1. Latent Action Conditioned Robot World Model** 

Given a video demonstration with _T_ frames _{O_ 1 _, ..., OT }_ and corresponding motion information _{a_ 1 _, ..., aT }_ , LAC- 

WM works as follows. 

**Latent Action Modeling with an IDM and FDM** RGB observations _Ot_ are mapped into visual embeddings _xt_ using a visual encoder (V-JEPA-2 (Assran et al., 2025)). The IDM takes as input two consecutive embeddings _xt_ and _xt_ +1 to encode latent action _zt_ such that _zt_ = IDM( _xt, xt_ +1). The IDM uses _M_ causal attention layers to produce contextualized representations of _xt_ and _xt_ +1, followed by _N_ cross-attention layers that transform a learned query token _qt_ into latent actions _zt_ by cross-attending to the contextualized representations. The FDM processes _xt_ and _zt_ using _L_ blocks composed of self-attention on _xt_ , self-attention on _zt_ , and cross-attention from _xt_ to _zt_ , to predict the next visual embedding _x_ ˆ _t_ +1, such that _x_ ˆ _t_ +1 = FDM( _xt, zt_ ). 

**Cross-Augmentation Inputs** Since the IDM is partially supervised by the image latent prediction loss, it may encode future information directly into _zt_ as a shortcut. To mitigate this, we adopt a cross-augmentation training scheme, similar to (Chen et al., 2024). Given observations _Ot_ and _Ot_ +1, we apply independent augmentations _A_ 1 and _A_ 2 to obtain two augmented embedding pairs: ( _x_<sup>1</sup> _t_<sup>_, x_1</sup> _t_ +1<sup>)</sup> and ( _x_<sup>2</sup> _t_<sup>_, x_2</sup> _t_ +1<sup>).</sup> One pair is used by IDM to generate _zt_<sup>1=IDM(</sup><sup>_x_1</sup> _t_<sup>_, x_1</sup> _t_ +1<sup>),whilethe other isused by FDM to</sup> predict _x_ ˆ<sup>2</sup> _t_ +1<sup>= FDM(</sup><sup>_x_</sup> _t_<sup>2</sup><sup>_, z_</sup> _t_<sup>1).The image latent prediction</sup> loss is given by: 


**Motion Decoder** While prior work mitigates shortcut solutions in LAM training by using quantization or lowdimensional latent spaces (Chen et al., 2024; Ye et al., 2025), such constraints limit representational capacity. Instead, LAC-WM uses continuous latent actions and mitigates shortcuts through an auxiliary motion decoding loss (Nikulin et al., 2025; Liang et al., 2025). The motion decoder (MD) reconstructs ground-truth motions **a** _t_ from latent actions _zt_ , conditioned on the current observation to enable viewpointdependent predictions. Specifically, _zt_ serves as a query in a cross-attention module over visual tokens extracted from the current frame. To reduce computation, the visual tokens are downsampled via a 2D convolutional layer. The resulting cross-attended features are fed into an MLP to produce motion outputs, such that ˆ **a** _t_ = MD( _xt, zt_ ). The decoder is trained using a mean squared error loss: 


The overall training loss combines the self-supervised image latent prediction loss and supervised motion decoding loss using weighting coefficients _λ_ recon and _λ_ motion as follows: 


3 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 


**Figure 2. UMAP visualization of 7,000 action embeddings** from three datasets: Droid (red), Agibot (green), and Egodex (blue). **1** : Embeddings from separate Explicit Action Encoders (EAE), which are distinctly separated by embodiment. **2** : Embeddings from a shared EAE (EAE*), still showing dataset-level separation. **3** : Embeddings from IDM without the motion decoder, where Agibot and Egodex cluster together but separate from Droid. **4** : Embeddings from the IDM, showing strong cross-dataset alignment. The IDM, FDM, and MD are trained end-to-end. Once trained, we keep the FDM and add an action projector for finetuning to adapt to an unseen embodiment. 

### **3.2. Adapting to Unseen Robot Embodiments** 

The latent action model requires future observations, which are unavailable during inference. Prior works address this by training a policy conditioned on current observations to generate latent actions (Ye et al., 2025; Chen et al., 2024). However, this approach does not support planning with a raw-action-conditioned world model. Instead, we learn an _action projector_ (Figure 1, right) that maps explicit raw actions into the latent action space (Gao et al., 2025). We use a two-layer MLP that takes the action **a** _t_ as input and outputs the corresponding latent action _zt_ . To adapt to an unseen robot embodiment, we initialize an action projector and finetune the pre-trained LAC-WM in three stages. First, we fine-tune the IDM and FDM of LAC-WM end-to-end using LoRA (Hu et al., 2022) with rank 2. Second, we freeze the FDM and train the action projector from scratch to map explicit actions into the latent space. Third, we jointly finetune the projector and FDM end-to-end using LoRA with rank 2. At inference time, we use only the action projector and FDM to perform action-conditioned imagined rollouts. 

## **4. Experiments** 

### **4.1. Baseline** 

We use a robot world model with explicit action encoders as our baseline. Specifically, we adopt the same FDM architecture but generate action conditioning by directly encoding 

explicit motions, such as robot end-effector (EE) actions or delta human hand poses into action embeddings. Since different embodiments have distinct action spaces, we employ separate action encoders for each embodiment, following common practice in multi-embodiment learning (NVIDIA et al., 2025b). Each action encoder shares the same architecture as the action projector in LAC-WM, taking only the explicit action as input and outputting the corresponding action embedding. To adapt to unseen embodiments, we train a new action encoder from scratch and fine-tune the FDM using LoRA with rank 2. We denote this model, consisting of explicit action encoders (EAE) and the FDM, as the explicit action conditioned robot world model (EAC-WM). 

### **4.2. Model Pretraining** 

**Datasets** We conduct pretraining on three datasets: EgoDex (Hoque et al., 2025), Agibot (Bu et al., 2025a), and Droid (Khazatsky et al., 2024). Agibot features a bimanual humanoid robot and Droid consists of a single Franka arm with a Robotiq gripper. EgoDex is a dataset of humans manipulating different objects in a tabletop environment. The datasets provide camera extrinsic information corresponding to egocentric head cameras for EgoDex and Agibot and third-person view cameras for Droid. Additionally, we have robot end-effector action labels for Agibot and Droid and human hand poses annotations for EgoDex. For each dataset, we chunk the actions into 5-step sequences to down-sample the observation frequency, which we found in practice improves world model learning. We sample 50,000 trajectories from each dataset. The action space includes changes in end-effector poses and camera poses. More details about the dataset action space is in Section A.1. 

**Parameters** Both EAC-WM and LAC-WM are trained for 80,000 iterations with a batch size of 512. Both models employ an action embedding dimension of 64. For both models, we use a pretrained V-JEPA2 (Assran et al., 2025) RGB tokenizer for image encoding, which is frozen during the model pre-training and fine-tuning. We use a custom V-JEPA2 RGB decoder to decode the predicted image embeddings into RGB image space as in Section A.3. More training details are in Section A.4. 

### **4.3. Model Finetuning** 

As described in Section 3.2, we finetune models to adapt to an unseen embodiment. We use a bimanual Franka robot setup equipped with Allegro hands, denoted as BFA. 

**Dataset** We consider a dataset consisting of 22 tasks of picking up different objects from a counter and placing it at a desired location in different scenes. The training dataset consists of 7,265 trajectories collected in the RoboCasa simulator (Nasiriany et al., 2024), covering common kitchen object categories (e.g., apple, bell pepper, ketchup), and 

4 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 


**Figure 3. Cross-embodiment action transfer results** : The left panels illustrate robot-to-human transfer, while the right panels show human-to-robot transfer. The first row presents reference videos. Rows 2–4 display FDM generated videos using embeddings from EAE, IDM without MD, and IDM, respectively. Blue dotted lines trace end-effector trajectories from the references and are aligned across generated videos except for initial positions. IDM embeddings yield trajectories that closely match the references, whereas the other methods exhibit inaccurate motion patterns and visual artifacts (highlighted by red circles). 

includes both successful and failed attempts. The trajectories only use the right robot arm. Thus, the action space is 25D, consisting 16 joint dimensions for the robot-hand, 3 dimensions for end-effector position, and 6 dimensions for rotation. Egocentric visual observations are captured using a head camera. As in Section 4.2, actions are chunked into 5-step sequences, reducing the observation frequency. More details are in Section A.2. 

**Finetuning Parameters** We finetune the LAC-WM and EAC-WM models on the BFA dataset using a batch size of 256 for a total of 60k iterations. For LAC-WM, fine-tuning follows the multi-stage procedure outlined in Section 3.2, with 20k iterations for Stage 1, 5k for Stage 2, and 35k for Stage 3. For EAC-WM, we follow the procedure in Section 4.1 and fine-tune for 60k iterations in a single stage. We found that directly fine-tuning EAC-WM in one stage yields better downstream performance than using the multi-stage approach, as shown in Section A.5. 

## **5. Latent Action Analysis** 

This section addresses the first research question of _Do latent action models better unify cross-embodiment action representations compared to explicit action labels?_ Specifically, we visualize the latent action space and qualitatively evaluate the action transfer between different embodiments. 

**UMAP Visualization** We analyze the action embeddings generated by both the IDM in the pretrained LAC-WM and the explicit action encoder (EAE) in pretrained EAC-WM by sampling 7,000 data points from the validation splits of the three pre-training datasets. Visualized with UMAP (Figure 2), the latent action embeddings produced by the IDM cluster closely across all three datasets, suggesting they occupy a unified action space (panel 4). In contrast, the embeddings from the EAE are clearly separated by dataset, indicating that explicit actions do not share a common latent representation (panel 1). Since EAC-WM uses a separate EAE for each embodiment, we additionally train a variant with a single shared EAE across all embodiments, denoted as EAE*. EAE* still produces disjoint dataset-specific action embeddings ((panel 2), showing that the separation is not due to different EAE initializations. Interestingly, when the IDM is trained without the motion decoder, the embeddings from Agibot and Egodex form a joint cluster, distinct from that of Droid (panel 3). We hypothesize this occurs because both Agibot and Egodex are based on egocentric views, resulting in more similar visual distributions. Extracting latent actions purely from visual observations may lack the task-relevant grounding provided by motion data, potentially resulting in latent representations that encode primarily perceptual features. This can lead to disjoint latent action spaces when faced with varying visual distributions. 

5 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

**Action Latent Transfer** We demonstrate the transferability of latent action embeddings across different embodiments by conditioning the FDM on observations from one embodiment while using action embeddings derived from another embodiment. Given an 8-frame reference video, we extract latent action embeddings by passing the video frames through the IDM. For comparison, the explicit actions are encoded using the EAE from EAC-WM, producing explicit action embeddings. Qualitative results in Figure 3 show transfers between robot (Agibot) and human motions. 

As shown in Figure 3, the learned latent action space enables video generation that captures semantically consistent and similar movements across different embodiments. Specifically, the latent action encodes the end-effector motion direction in image space. As illustrated in the left column of Figure 3, the same latent action prompts both the robot’s right end-effector and the human’s right hand to move rightward and upward. In contrast, EAE embeddings fail to transfer effectively, producing nearly static posess of human hands and robot grippers. This aligns with our UMAP visualization, where separated action embeddings from different embodiments lead to out-of-distribution conditioning when mixing embodiments. Videos generated with IDM embeddings trained without the MD exhibit artifacts like duplicated hands and floating objects (red circles). These artifacts suggest that the latent embeddings may have learned the shortcut solution of encoding perceptual features such as optical flow when not grounded by motion labels. Conversely, action embeddings from IDM trained with MD result in no residual artifacts from the source embodiment, indicating that these embeddings effectively capture embodiment-invariant motion representations. 

To summarize, the UMAP visualization and action transfer results suggest that _latent action models do better unify action representations across diverse embodiments than directly using action labels on heterogeneous datasets_ . Moreover, incorporating a motion decoding loss further enhances the coherence of the latent action space. To further study the physical meaning of the latent actions, we also conduct PCA analysis on the latent action embeddings in Section A.7. 

## **6. Robot Task Evaluation** 

This section studies the world model performance when adapting to a previously unseen embodiment. 

### **6.1. Action-conditioned Imagined Roll-out** 

We quantitatively evaluate action conditioned image generation performance of the world models by predicting eight future frames based on an initial observation and an action sequence, as in Figure 6. For evaluation, we use the held out BFA splits to test generalization to (1) unseen instances of 

|Eval Split|Model|PSNR_↑_|LPIPS_↓_|FID_↓_|FVD_↓_|
|---|---|---|---|---|---|
|Unseen|EAC-WM-S|22.212|0.077|10.648|42.257|
|It|EAC-WM|24.252|0.057|9.312|30.349|
|nsances|LAC-WM|**27.484**|**0.037**|**8.439**|**23.213**|
||EAC-WM-S|22.062|0.081|10.642|40.477|
|Unseen<br>Cti|EAC-WM|24.091|0.060|9.144|29.702|
|aegores|LAC-WM|**27.333**|**0.040**|**8.509**|**24.456**|


**Table 1. Action conditioned imagined roll-out performance** . Image and video quality metrics are reported across evaluation splits on unseen instances and unseen categories. LAC-WM performs the best compared to models trained from scratch (EAC-WM-S) or pretrained with explicit actions (EAC-WM). 

objects within known categories (Unseen Instances) and (2) three entirely unseen object categories: donut, lime, and banana (Unseen Categories). We compare two variants of EAC-WM: EAC-WM-S, trained from scratch on BFA, and EAC-WM, which is first pretrained on three datasets (EgoDex, Agibot, and Droid), then finetuned on BFA. LAC-WM is pretrained then finetuned as in Section 4.3. All models take in raw robot actions, which is encoded into action embeddings through the explicit action encoders of EAC-WM or the action projector of LAC-WM. We report image quality metrics (PSNR, FID, LPIPS) and a video quality metric (FVD), computed over 512 randomly sampled windows per split ( Table 1). LAC-WM performs the best, followed by EAC-WM, while EAC-WM-S performs worst, highlighting the importance of pretraining with a unified action space for effective adaptation. 

### **6.2. Robot Planning with Action Selection** 

We investigate the second research question of _whether a unified action space enhance cross-embodiment learning of the world model and downstream robot task performance_ , especially when adapted to an unseen embodiment, by using the world model to select actions for completing the task. 

**Problem Setup** As in Section 4.3, we consider the task of picking up an object from a counter and placing it back using the right arm of the BFA setup. We evaluate generalization to both Unseen Instances and Unseen Categories. We consider 22 unseen instances from 22 seen categories and 3 unseen categories. For each evaluation episode, we assume access to one demonstration trajectory for sampling a subgoal image every _p_ timesteps, resulting in a sequence of subgoal sets the robot must achieve to complete the task. For each subgoal, we sample _N_ candidate action sequences of length _p_ . Given the current observation, the robot uses the world model to roll out predictions of future observations conditioned on action embeddings from action projector encoding each action sequence. The action sequence whose final predicted image is closest to the subgoal image is selected for execution, based on _l_ 2 distance between the predicted final image embedding and the subgoal image embedding. We then move on to the next 

6 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

subgoal, repeating this process until the episode ends. An example of this rollout selection process is illustrated in Figure 7. In practice, to mitigate noise in the image embedding space, we select the top- _k_ action sequences with the closest final predicted images to the subgoal, and execute the average of these _k_ sequences. 

**Metrics** Given the difficulty of this dexterous manipulation task, we evaluate performance using multiple metrics. Task Success Rate (S.R.) indicates whether the object was successfully lifted and placed back on the counter by the end of the episode. We also measure intermediate progress: Success Rate of Contact (S.R.C.), which indicates if the robot contacted the object, and Success Rate of Lifting (S.R.L.), which indicates if the object was lifted without touching the counter. To assess how closely the robot follows the subgoals, we compute the embedding distance between each subgoal image and the corresponding achieved image at each rollout step. We report the average embedding distance across all subgoals ( _δf_ ), and for the final goal ( _δfg_ ). 

**Action Selection from VLA Samples** Instead of performing random action sequence sampling, which is inefficient for action optimization, especially for a difficult dexterous manipulation task, we explore sampling from alternative priors. With recent advancements in VLAs, we investigate whether world models can complement VLA by guiding action selection over VLA-generated candidates. Specifically, we leverage an off-the-shelf VLA model trained on the BFA dataset, which generates actions via a diffusion head conditioned on current observations, language instructions, and robot state. While we use the VLA with architecture specified in Section A.6, other VLA models with action sampling head can also be used. At test time, we generate diverse candidate actions by injecting different noise seeds into the flow-matching process, producing _N_ =500 candidate sequences, each of length _p_ =100. These sequences typically correspond to 4–5 subgoals per episode, resulting in a 20-step rollout for the world models. We use _k_ = 3 to select the top 3 action sequences to calculate the average action sequence for execution, as described before. 

We benchmark our world-model–guided action selection against two VLA-only baselines: **VLA-random** , which executes a single randomly sampled action sequence, and **VLA-mean** , which averages across all _N_ candidates. For action selection, we consider three world models: EACWM-S, EAC-WM, and LAC-WM. Each model is tested over 100 episodes per evaluation split across all tasks, with 3 random seeds per experiment. Results in Table 2 show that action selection guided by LAC-WM significantly outperforms the VLA-only baselines, particularly on the S.R.L and S.R metrics. Notably, LAC-WM achieves a **29.0% higher S.R.** than the strongest VLA baseline, a **22.2% improvement over EAC-WM-S** , and a **46.7% improvement** 


**Figure 4.** We show the image latent embedding distance _δf_ (left) and _δfg_ (middle) and task success rate S.R. (right), for LAC-WM (blue) and EAC-WM (orange) pre-trained with different number of embodiments. The x axis shows the number of embodiments and dataset size used in pre-training, from left to right of the x axis, the model is trained with Egodex only, Egodex and Agibot, and Egodex, Agibot and Droid dataset. 


**Figure 5.** Experiments of scaling number of embodiments or data samples. The first two points shows the scaling from two embodiments (Egodex and Droid) to three embodiments (Egodex, Droid and Agibot) with same amount of trajectories, while the last two points shows the scaling from 24k trajectories to 150k trajectories across three embodiments. 

**over EAC-WM** , averaged across splits. An example rollout is shown in Figure 8, where LAC-WM successfully grasped and lifted the object while both EAC-WM-S and EAC-WM fails to lift the object, indicating LAC-WM is better at capturing fine-grained details of the robot hand posture and learning more accurate dynamics. While EAC-WM-S offers slight improvements over the VLA baselines, EACWM underperforms compared to both VLA-only methods and EAC-WM-S, indicating its limited ability to reliably predict long-horizon futures. This is likely due to its disjoint action space limiting cross-embodiment pretraining and downstream performance. This contrast highlights the advantage of LAC-WM ’s unified action space in facilitating effective adaptation to unseen embodiments. Despite LAC-WM ’s gains, overall S.R. remains low, reflecting the difficulty of this dexterous manipulation task. Additionally, we report the metric _δf_ , which measures how effectively a method reaches the subgoal state, a lower _δf_ indicates better subgoal alignment. LAC-WM achieves lower _δf_ values than EAC-WM, suggesting more accurate subgoal reaching. However, since subgoal images are not used by VLA-only methods, they may attempt to reach different subgoal states. Therefore, both _δf_ and _δfg_ serve as reference metrics rather than definitive performance indicators for those baselines. 

**Scaling Law with Number of Embodiments and Data** 

We investigate the performance of world models as we scale the number of embodiments used in pre-training. Specifically, we pretrain both LAC-WM and EAC-WM on three 

7 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

|**Val Set**|**Model**|_δf ↓_|_δfg ↓_|S.R.C_↑_|S.R.L_↑_|**S.R.**_↑_|
|---|---|---|---|---|---|---|
||VLA-mean|26.49_±_0.06|27.07_±_0.02|0.84_±_0.04|0.56_±_0.00|0.20_±_0.03|
|Unseen|VLA-random|26.52_±_0.06|27.23_±_0.12|0.82_±_0.03|0.55_±_0.03|0.18_±_0.03|
|Instances|EAC-WM-S|26.74_±_0.34|27.38_±_0.35|0.84_±_0.02|0.58_±_0.04|0.19_±_0.04|
||EAC-WM|26.79_±_0.26|27.37_±_0.27|0.84_±_0.01|0.56_±_0.04|0.16_±_0.04|
||LAC-WM|**26.29**_±_0.15|**26.87**_±_0.13|**0.86**_±_0.03|**0.60**_±_0.03|**0.25**_±_0.03|
||VLA-mean|26.94_±_0.09|27.86_±_0.17|0.84_±_0.04|0.49_±_0.04|0.14_±_0.03|
|Unseen|VLA-random|26.93_±_0.06|27.77_±_0.07|0.80_±_0.01|0.48_±_0.01|0.12_±_0.02|
|Categories|EAC-WM-S|27.16_±_0.39|28.00_±_0.41|0.84_±_0.02|0.49_±_0.07|0.17_±_0.03|
||EAC-WM|27.19_±_0.28|28.03_±_0.27|0.82_±_0.01|0.49_±_0.04|0.14_±_0.04|
||LAC-WM|**26.73**_±_0.09|**27.58**_±_0.11|**0.85**_±_0.02|**0.56**_±_0.02|**0.18**_±_0.02|
||VLA-mean|26.72_±_0.08|27.46_±_0.09|0.84_±_0.04|0.53_±_0.02|0.17_±_0.03|
|Ar|VLA-random|26.72_±_0.06|27.50_±_0.09|0.81_±_0.02|0.52_±_0.02|0.15_±_0.02|
|veage|EAC-WM-S|26.95_±_0.37|27.69_±_0.38|0.84_±_0.02|0.54_±_0.05|0.18_±_0.03|
||EAC-WM|26.99_±_0.27|27.70_±_0.27|0.83_±_0.01|0.52_±_0.04|0.15_±_0.04|
||LAC-WM|**26.50**_±_0.12|**27.22**_±_0.12|**0.85**_±_0.03|**0.58**_±_0.02|**0.22**_±_0.02|


**Table 2. Robot planning performance** of a VLA with action selection using a world model (EAC-WM-S, EAC-WM, LAC-WM) versus without action selection (VLA-mean, VLA-random). Mean and standard deviation across three seeds are shown. 

subsets: (1) Egodex only, (2) Egodex and Agibot, and (3) Egodex, Agibot, and Droid. For each dataset, we use 50,000 samples, so models pretrained on more embodiments are exposed to proportionally larger amounts of data. Then we fine-tune the models on BFA and use them for VLA action selection. We report the S.R., _δf_ and _δfg_ for each fine-tuned model. Results averaged over 3 seeds are shown in Figure 4. Interestingly, LAC-WM ’s downstream planning performance improves as the number of pre-training embodiments increases, while EAC-WM shows the opposite trend with decreased S.R. and increased or nearly unchanged _δf_ and _δfg_ . We hypothesize this is because as the number of embodiment increases, the action embedding space become more disjoint for EAC-WM, making the model harder to learn from cross embodiment datasets, and less effective at adapting to the new BFA embodiment. These results highlight that a unified action space is critical for cross-embodiment pre-training. 

We further investigate how performance scales with either the number of embodiments or the amount of pretraining data in Figure 5. The first two points in the plot correspond to settings where the total number of samples is fixed while increasing the number of embodiments. The last two points correspond to fixed embodiments while increasing the dataset size. In both scenarios, LAC-WM exhibits consistent performance improvements as either embodiments or samples increase. In contrast, EAC-WM performance degrades when adding more embodiments, and only improves when additional data comes from the same embodiment. These results suggest that EAC-WM cannot efficiently leverage heterogeneous action spaces, further highlighting the advantage of learning a unified latent action representation. 

**Ablating Motion Decoding and Cross-Augmentation In-** 

|**Model**|_δf ↓_|_δfg ↓_|_S.R.C ↑_|_S.R.L↑_|**S**_._**R**_.↑_|
|---|---|---|---|---|---|
|LAC-WM-MD-CA|26.98|27.80|0.83|0.46|0.13|
|LAC-WM|**26.73**|**27.58**|**0.85**|**0.56**|**0.18**|


**Table 3. Ablation study of motion decoding loss and crossaugmentation inputs on the validation set of unseen categories.** 

**puts** We analyze the effect of motion decoding and crossaugmentation inputs for downstream robot planning by comparing LAC-WM with LAC-WM-MD-CA, a variant trained without the motion decoding loss or cross-augmentation, on the Unseen Categories validation split. As shown in Table 3 (3 seeds), LAC-WM achieves a 38% higher success rate, suggesting that both motion decoding and crossaugmentation are crucial for learning latent actions that encode physically meaningful control information. 

In summary, the superior performance of LAC-WM over EAC-WM indicates that _conditioning a world model on a unified action space enhances cross-embodiment learning and improves adaptation to unseen embodiments for robot action planning compared to using a disjoint latent space_ . 

**Effectiveness of LAC-WM with Different Vision Encoders.** We further evaluate the robustness of LAC-WM with a different vision tokenizer. We replace the vision encoder/decoder with the pretrained Cosmos-0.1-TokenizerCI8x8 (NVIDIA et al., 2025a), and pretrain both LAC-WM and EAC-WM using the same data and hyperparameters as in Section 4.2. We then finetune the pretrained world models on LIBERO (Liu et al., 2023) to test whether the benefits of LAC-WM transfer to a different simulation benchmark. Note that the Franka arm with Franka gripper in the LIBERO enviroment is a slightly different embodiment compared to the Franka arm with a Robotiq gripper in the Droid dataset. 

For finetuning, we replay trajectories from LIBERO-10, 

8 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

|Task|VLA-random|VLA-mean|EAC-WM|LAC-WM|
|---|---|---|---|---|
|book|0.76|0.76|0.80|**0.92**|
|white bowl|0.76|0.92|0.92|**0.96**|
|wine bottle|0.72|0.84|0.84|**0.96**|
|alphabet soup|0.80|0.72|0.80|**0.88**|
|salad dressing|0.68|0.84|0.76|**0.88**|
|Average|0.744|0.816|0.824|**0.920**|


**Table 4. Success rate on five unseen LIBERO tasks over 125 total episodes** . All methods share the same _π_ 0 _._ 5 VLA backbone, sampling 20 candidate 50-step action chunks. 

LIBERO-Goal, LIBERO-Object, and LIBERO-Spatial at 256 _×_ 256 resolution, yielding 2,000 trajectories. We additionally collect 200 rollout trajectories by executing a pretrained _π_ 0 _._ 5 (Intelligence et al., 2025) policy on four LIBERO-Object tasks with large initial-pose perturbations, producing 110 successes and 90 failures. This exposes the world models to both success and failure rollouts. Both LAC-WM and EAC-WM are finetuned on the resulting 2,200 trajectories using the protocol in Section 4.3. 

Since the original LIBERO benchmark is close to saturated, we evaluate on five unseen LIBERO-Object task variants. Three tasks require placing unseen objects, namely book, white bowl, and wine bottle, into the basket, while two tasks place alphabet soup and salad dressing at unseen initial locations. For each task, we collect one human demonstration and sample frames every 40 steps as goal images. We evaluate each method over 25 rollouts with randomized initial states per task, for 125 episodes in total. 

We finetune _π_ 0 _._ 5 on LIBERO to predict 50-step action chunks, as the VLA policy. At inference time, we sample 20 candidate chunks with diffusion noise scale 2.0. For each candidate, the world model rolls out eight 5-step visual predictions, corresponding to 40 execution steps. We select the chunk whose final predicted frame has the smallest latent distance to the goal image, and execute its first 25 steps. We compare LAC-WM against EAC-WM and two VLA-only baselines: VLA-random and VLA-mean. 

As shown in Table 4, LAC-WM achieves the best performance on all five unseen tasks, improving the average success rate from 82.4% with EAC-WM to 92.0%, a 9.6point absolute gain. It also improves over VLA-mean by 10.4 points and VLA-random by 17.6 points. In contrast, EAC-WM performs similarly to VLA-mean, suggesting that explicit-action-conditioned prediction provides limited benefit for ranking candidate chunks in this setting. These results show that LAC-WM remains effective with a different vision encoder and transfers robustly to LIBERO. 

## **7. Conclusion and Limitations** 

In this work, we investigate foundational robot world model learning using a cross-embodiment dataset. We compare LAC-WM, a world model conditioned on latent actions, 

with EAC-WM, which relies on explicit action labels. Our results demonstrate that latent-action-conditioned models learn more unified representations across diverse embodiments, and that LAC-WM-guided planning significantly outperforms EAC-WM. Notably, we find that the downstream performance of LAC-WM scales positively with the number of embodiments used during pretraining, whereas EAC-WM exhibits the opposite trend. These findings highlight the effectiveness of a unified latent action space in addressing the challenges of cross-embodiment generalization and heterogeneous action spaces in robotics. 

The pretraining datasets include motion labels, which is an intentional design choice. It enables a direct comparison with world models trained under explicit action supervision, allowing us to isolate the benefits of a unified latent action space. Our auxiliary motion decoding loss promotes coherence in the latent action representations without constraining the framework to labeled data. As a result, the proposed approach is compatible with, and likely to benefit from, large-scale label-free video pretraining. Future work will explore leveraging such unlabeled data to further enhance generalization and transfer capabilities in robotic world models. Despite the substantial performance gains achieved by LAC-WM, absolute task success remains limited for the dexterous manipulation benchmark, reflecting the difficulty of dexterous manipulation in unseen settings. Improving performance through stronger VLA policies and more robust planning is an important direction. In addition, future work will include real-world data collection and hardware validation to evaluate LAC-WM in physical environments. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of robot world model learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

## **References** 

- Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Bar, A., Zhou, G., Tran, D., Darrell, T., and LeCun, Y. Navigation world models. In _Proceedings of the Computer_ 

9 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

- _Vision and Pattern Recognition Conference_ , pp. 15791– 15801, 2025. 

- Bruce, J., Dennis, M. D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Huang, X., Jiang, S., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025a. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with taskcentric latent actions, 2025b. URL https://arxiv. org/abs/2505.06111. 

- Chen, X., Guo, J., He, T., Zhang, C., Zhang, P., Yang, D. C., Zhao, L., and Bian, J. Igor: Image-goal representations are the atomic control units for foundation models in embodied ai, 2024. URL https://arxiv.org/abs/ 2411.00785. 

- Chen, Y., Ge, Y., Tang, W., Li, Y., Ge, Y., Ding, M., Shan, Y., and Liu, X. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 19752–19763, 2025. 

- Cui, Z. J., Pan, H., Iyer, A., Haldar, S., and Pinto, L. Dynamo: In-domain dynamics pretraining for visuo-motor control. _Advances in Neural Information Processing Systems_ , 37:33933–33961, 2024. 

- Doshi, R., Walke, H. R., Mees, O., Dasari, S., and Levine, S. Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation. In _CoRL_ , pp. 496–512, 2024. URL https://proceedings. mlr.press/v270/doshi25a.html. 

- Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., and Li, H. Vista: A generalizable driving world model with high fidelity and versatile controllability. _Advances in Neural Information Processing Systems_ , 37: 91560–91596, 2024. 

- Gao, S., Zhou, S., Du, Y., Zhang, J., and Gan, C. Adaworld: Learning adaptable world models with latent actions, 2025. URL https://arxiv.org/abs/ 2503.18938. 

- Gupta, A., Tian, S., Zhang, Y., Wu, J., Mart´ın-Mart´ın, R., and Fei-Fei, L. Maskvit: Masked visual pre-training for video prediction, 2022. URL https://arxiv.org/ abs/2206.11894. 

- Hassan, M., Stapf, S., Rahimi, A., Rezende, P., Haghighi, Y., Bruggemann, D., Katircioglu, I., Zhang, L., Chen, X.,¨ Saha, S., et al. Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pp. 22404–22415, 2025. 

- Hoque, R., Huang, P., Yoon, D. J., Sivapurapu, M., and Zhang, J. Egodex: Learning dexterous manipulation from large-scale egocentric video, 2025. URL https: //arxiv.org/abs/2505.11709. 

- Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., and Corrado, G. Gaia-1: A generative world model for autonomous driving. _arXiv preprint arXiv:2309.17080_ , 2023. 

- Hu, E. J., yelong shen, Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., and Chen, W. LoRA: Low-rank adaptation of large language models. In _International Conference on Learning Representations_ , 2022. URL https: //openreview.net/forum?id=nZeVKeeFYf9. 

- Intelligence, P., Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Galliker, M. Y., Ghosh, D., Groom, L., Hausman, K., Ichter, B., Jakubczak, S., Jones, T., Ke, L., LeBlanc, D., Levine, S., Li-Bell, A., Mothukuri, M., Nair, S., Pertsch, K., Ren, A. Z., Shi, L. X., Smith, L., Springenberg, J. T., Stachowicz, K., Tanner, J., Vuong, Q., Walke, H., Walling, A., Wang, H., Yu, L., and Zhilinsky, U. _π_ 0 _._ 5: a vision-language-action model with open-world generalization, 2025. URL https: //arxiv.org/abs/2504.16054. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., Magne, L., Mandlekar, A., Narayan, A., Tan, Y. L., Wang, G., Wang, J., Wang, Q., Xu, Y., Zeng, X., Zheng, K., Zheng, R., Liu, M.-Y., Zettlemoyer, L., Fox, D., Kautz, J., Reed, S., Zhu, Y., and Fan, L. Dreamgen: Unlocking generalization in robot learning through video world models, 2025. URL https://arxiv.org/abs/2505.12705. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., Fagan, P. D., Hejna, J., Itkina, M., Lepert, M., Ma, Y. J., Miller, P. T., Wu, J., Belkhale, S., Dass, S., Ha, H., Jain, A., Lee, A., Lee, Y., Memmel, M., Park, S., Radosavovic, I., Wang, K., Zhan, A., Black, K., Chi, C., Hatch, K. B., Lin, S., Lu, J., Mercat, J., Rehman, A., Sanketi, P. R., Sharma, A., Simpson, C., Vuong, Q., Walke, H. R., Wulfe, B., Xiao, T., Yang, J. H., Yavary, A., Zhao, T. Z., Agia, C., Baijal, R., Castro, M. G., Chen, D., Chen, Q., Chung, T., Drake, J., Foster, E. P., Gao, J., Herrera, 

10 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

- D. A., Heo, M., Hsu, K., Hu, J., Jackson, D., Le, C., Li, Y., Lin, X., Ma, Z., Maddukuri, A., Mirchandani, S., Morton, D., Nguyen, T. K., O’Neill, A., Scalise, R., Seale, D., Son, V., Tian, S., Tran, E., Wang, A. E., Wu, Y., Xie, A., Yang, J., Yin, P., Zhang, Y., Bastani, O., Berseth, G., Bohg, J., Goldberg, K., Gupta, A., Gupta, A., Jayaraman, D., Lim, J. J., Malik, J., Mart´ın-Mart´ın, R., Ramamoorthy, S., Sadigh, D., Song, S., Wu, J., Yip, M. C., Zhu, Y., Kollar, T., Levine, S., and Finn, C. DROID: A large-scale in-the-wild robot manipulation dataset. In _RSS 2024 Workshop: Data Generation for Robotics_ , 2024. URL https: //openreview.net/forum?id=Ml2pTYLNLi. 

- Kim, H., Kang, J., Kang, H., Cho, M., Kim, S. J., and Lee, Y. Uniskill: Imitating human videos via cross-embodiment skill representations. In _9th Annual Conference on Robot Learning_ , 2025. URL https://openreview.net/ forum?id=EgSDP6AOF1. 

- Li, J., Tang, J., Xu, Z., Wu, L., Zhou, Y., Shao, S., Yu, T., Cao, Z., and Lu, Q. Hunyuan-gamecraft: High-dynamic interactive game video generation with hybrid history condition. _arXiv preprint arXiv:2506.17201_ , 2025. 

- Liang, A., Czempin, P., Hong, M., Zhou, Y., Biyik, E., and Tu, S. Clam: Continuous latent action models for robot learning from unlabeled demonstrations. _arXiv preprint arXiv:2505.04999_ , 2025. 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., qiang liu, Zhu, Y., and Stone, P. LIBERO: Benchmarking knowledge transfer for lifelong robot learning. In _Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2023. URL https: //openreview.net/forum?id=xzEtNSuDJk. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. RDT-1b: a diffusion foundation model for bimanual manipulation. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum? id=yAzN4tz7oI. 

- Mandlekar, A., Nasiriany, S., Wen, B., Akinola, I., Narang, Y., Fan, L., Zhu, Y., and Fox, D. Mimicgen: A data generation system for scalable robot learning using human demonstrations. In _7th Annual Conference on Robot Learning_ , 2023. 

- Nasiriany, S., Maddukuri, A., Zhang, L., Parikh, A., Lo, A., Joshi, A., Mandlekar, A., and Zhu, Y. Robocasa: Largescale simulation of everyday tasks for generalist robots. In _RSS 2024 Workshop: Data Generation for Robotics_ , 2024. URL https://openreview.net/forum? id=mHxHdTaRLa. 

- Nikulin, A., Zisman, I., Tarasov, D., Lyubaykin, N., Polubarov, A., Kiselev, I., and Kurenkov, V. Latent action learning requires supervision in the presence of distractors, 2025. URL https://arxiv.org/abs/2502. 00379. 

- NVIDIA, :, Agarwal, N., Ali, A., Bala, M., Balaji, Y., Barker, E., Cai, T., Chattopadhyay, P., Chen, Y., Cui, Y., Ding, Y., Dworakowski, D., Fan, J., Fenzi, M., Ferroni, F., Fidler, S., Fox, D., Ge, S., Ge, Y., Gu, J., Gururani, S., He, E., Huang, J., Huffman, J., Jannaty, P., Jin, J., Kim, S. W., Klar,´ G., Lam, G., Lan, S., LealTaixe, L., Li, A., Li, Z., Lin, C.-H., Lin, T.-Y., Ling, H., Liu, M.-Y., Liu, X., Luo, A., Ma, Q., Mao, H., Mo, K., Mousavian, A., Nah, S., Niverty, S., Page, D., Paschalidou, D., Patel, Z., Pavao, L., Ramezanali, M., Reda, F., Ren, X., Sabavat, V. R. N., Schmerling, E., Shi, S., Stefaniak, B., Tang, S., Tchapmi, L., Tredak, P., Tseng, W.C., Varghese, J., Wang, H., Wang, H., Wang, H., Wang, T.-C., Wei, F., Wei, X., Wu, J. Z., Xu, J., Yang, W., Yen-Chen, L., Zeng, X., Zeng, Y., Zhang, J., Zhang, Q., Zhang, Y., Zhao, Q., and Zolkowski, A. Cosmos world foundation model platform for physical ai, 2025a. URL https://arxiv.org/abs/2501.03575. 

- NVIDIA, :, Bjorck, J., Castaneda, F., Cherniadev, N., Da,˜ X., Ding, R., Fan, L. J., Fang, Y., Fox, D., Hu, F., Huang, S., Jang, J., Jiang, Z., Kautz, J., Kundalia, K., Lao, L., Li, Z., Lin, Z., Lin, K., Liu, G., Llontop, E., Magne, L., Mandlekar, A., Narayan, A., Nasiriany, S., Reed, S., Tan, Y. L., Wang, G., Wang, Z., Wang, J., Wang, Q., Xiang, J., Xie, Y., Xu, Y., Xu, Z., Ye, S., Yu, Z., Zhang, A., Zhang, H., Zhao, Y., Zheng, R., and Zhu, Y. Gr00t n1: An open foundation model for generalist humanoid robots, 2025b. URL https://arxiv.org/abs/2503.14734. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H. V., Szafraniec, M., Khalidov, V., Fernandez, P., HAZIZA, D., Massa, F., El-Nouby, A., Assran, M., Ballas, N., Galuba, W., Howes, R., Huang, P.-Y., Li, S.-W., Misra, I., Rabbat, M., Sharma, V., Synnaeve, G., Xu, H., Jegou, H., Mairal, J., Labatut, P., Joulin, A., and Bojanowski, P. DINOv2: Learning robust visual features without supervision. _Transactions on Machine Learning Research_ , 2024. ISSN 2835-8856. URL https:// openreview.net/forum?id=a68SUt6zFt. Featured Certification. 

- Po, R., Nitzan, Y., Zhang, R., Chen, B., Dao, T., Shechtman, E., Wetzstein, G., and Huang, X. Long-context state-space video world models, 2025. URL https: //arxiv.org/abs/2505.20171. 

- Ren, Z., Wei, Y., Guo, X., Zhao, Y., Kang, B., Feng, J., and Jin, X. Videoworld: Exploring knowledge learning from unlabeled videos. In _Proceedings of the Computer Vision_ 

11 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

- _and Pattern Recognition Conference_ , pp. 29029–29039, 2025. 

- Schmidt, D. and Jiang, M. Learning to act without actions. In _The Twelfth International Conference on Learning Representations_ , 2024. URL https://openreview. net/forum?id=rvUq3cxpDF. 

- Valevski, D., Leviathan, Y., Arar, M., and Fruchter, S. Diffusion models are real-time game engines. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum? id=P8pqeEkn1H. 

   - Zheng, J., Li, J., Wang, Z., Liu, D., Kang, X., Feng, Y., Zheng, Y., Zou, J., Chen, Y., Zeng, J., Wang, T., Zhang, Y.-Q., Liu, J., and Zhan, X. X-VLA: Soft-prompted transformer as scalable cross-embodiment vision-languageaction model. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL https: //openreview.net/forum?id=kt51kZH4aG. 

   - Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., and Kong, T. Irasim: A fine-grained world model for robot manipulation, 2025. URL https://arxiv.org/abs/2406. 14540. 

- Wu, J., Yin, S., Feng, N., He, X., Li, D., HAO, J., and Long, M. ivideoGPT: Interactive videoGPTs are scalable world models. In _The Thirty-eighth Annual Conference on Neural Information Processing Systems_ , 2024. URL https: //openreview.net/forum?id=4TENzBftZR. 

- Yang, S., Du, Y., Ghasemipour, S. K. S., Tompson, J., Kaelbling, L. P., Schuurmans, D., and Abbeel, P. Learning interactive real-world simulators. In _The Twelfth International Conference on Learning Representations_ , 2024. URL https://openreview.net/forum? id=sFyTZEqmUY. 

- Ye, S., Jang, J., Jeon, B., Joo, S. J., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., Liden, L., Lee, K., Gao, J., Zettlemoyer, L., Fox, D., and Seo, M. Latent action pretraining from videos. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview.net/forum? id=VYOe2eBQeh. 

- Yu, J., Qin, Y., Wang, X., Wan, P., Zhang, D., and Liu, X. Gamefactory: Creating new games with generative interactive videos. _arXiv preprint arXiv:2501.08325_ , 2025. 

- Zhang, C., Pearce, T., Zhang, P., Wang, K., Chen, X., Shen, W., Zhao, L., and Bian, J. What do latent action models actually learn? In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2026. URL https://openreview.net/forum? id=DQMjemrVhe. 

- Zhang, Y., Peng, C., Wang, B., Wang, P., Zhu, Q., Kang, F., Jiang, B., Gao, Z., Li, E., Liu, Y., et al. Matrixgame: Interactive world foundation model. _arXiv preprint arXiv:2506.18701_ , 2025. 

- Zheng, J., Li, J., Liu, D., Zheng, Y., Wang, Z., Ou, Z., Liu, Y., Liu, J., Zhang, Y.-Q., and Zhan, X. Universal actions for enhanced embodied foundation models, 2025. URL https://arxiv.org/abs/2501.10105. 

12 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

## **A. Appendix** 

### **A.1. Pretraining Dataset Details** 

We conduct pretraining on three datasets: EgoDex (Hoque et al., 2025), Agibot (Bu et al., 2025a), and Droid (Khazatsky et al., 2024). The action space includes changes in end-effector poses and camera poses. The end-effector pose combines the wrist pose with additional dimensions for gripper or hand articulation. Each wrist pose is represented as a nine-dimensional vector containing three dimensions for translation and six for rotation. The camera pose follows the same nine-dimensional format. In Agibot, the end-effector pose has twenty dimensions total, ten per hand, with each consisting of the nine-dimensional wrist pose plus one dimension for the gripper state. In Droid, it is ten-dimensional for a single arm with the same structure. In EgoDex, the end-effector pose includes the nine-dimensional wrist pose plus sixty dimensions representing finger positions, corresponding to twenty keypoints in three-dimensional space, for a total of 138 dimensions for both hands. Camera motion is represented as a nine-dimensional change in pose for EgoDex and Agibot. For Droid, it is set to zero because the third-person camera remains fixed during each episode. The end-effector pose and camera motion vectors are concatenated as input to EAC-WM. For the motion decoder of LAC-WM, the latent action vector is divided evenly: the first half decodes the end-effector pose, and the second half decodes the camera pose. 


**Figure 6. Example of action conditioned imagined roll-out from the world models** . The top row displays the ground truth video, while the subsequent rows show action-conditioned imagined rollouts from EAC-WM-S, EAC-WM, and LAC-WM. While LAC-WM accurately predicts future observations, both EAC-WM-S and EAC-WM exhibit overshooting robot actions, highlighted by red circles, where the robot arm moves excessively. This suggests that LAC-WM better captures the robot dynamics. 

### **A.2. BFA Dataset** 

We use MimicGen (Mandlekar et al., 2023) along with RoboCasa simulator to produce large-scale synthetic pick and place datasets given 10 teleoperation trajectories. The teleoperators are instructed to pick up the object and place it either to the left or right of the initial position of the object with minimum of 0.1 meter movement. The data consists of 22 grasping 

13 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 


**Figure 7. Examples of action selection rollout** . The leftmost image shows the initial observation, and the rightmost image depicts the goal state. Numbers in the top-left corner indicate time steps. In this example, three action sequences are sampled and rolled out by the world model, producing eight future predictions. The action sequence whose predicted final image has the smallest embedding distance ( _δfg_ ) to the goal image is selected for execution. Here, the action sequence in the top row is chosen. 

object categories, resulting a total of 7,265 success and failure trajectories, with 20% of them being success trajectories. The robot consists of two franka arms mounted on the mobile platform. See Figure 6 for the examples of the dataset. 

### **A.3. Image decoder** 

To reconstruct pixels from V-JEPA2 (Assran et al., 2025) embeddings, we train a custom Vision Transformer–based decoder. We first pretrain this decoder to reconstruct images from DROID and then finetune it on the BFA dataset. The decoder projects the input embeddings (16 _×_ 16 tokens, each of dimension 1408 for a 256 _×_ 256 image) to a 1024-dimensional decoder space, followed by 12 self-attention layers with 32 attention heads each. The resulting features are then linearly mapped back to pixel space to reconstruct the output frames. We train the decoder using a standard mean-squared error (MSE) loss. 

### **A.4. Model Training and Inference** 

**Model Parameters** The details of our model parameters can be found in Table 5. 

|Hyperparameter|Value|
|---|---|
|Image Tokenizer|V-JEPA 2 (1B)|
|Action Projector|1,550,528|
|Image Decoder|153,845,952|
|IDM:||
|# Attention Blocks|4|
|# Attention Heads|16|
|# Latent Dimension|512|
|# Parameter|46,939,968|
|FDM:||
|# Attention Blocks|8|
|# Attention Heads|16|
|# Latent Dimension|512|
|# Parameter|93,844,480|


**Table 5.** Hyperparameters for LAC-WM model architecture. 

**Pretraining parameters** We pre-train both LAC-WM and EAC-WM for 80,000 iterations. For both models, we remove the temporal attention in the FDM for the first 60,000 iterations, to encourage strong conditioning on actions (Chen et al., 2024). The final 20,000 iterations fine-tune the model with additional temporal attentions in FDM using a temporal horizon of 8. 

14 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 

|**Val Set**|**Model**|_δf ↓_|_δfg ↓_|S.R.C_↑_|S.R.L_↑_|S.R_↑_|
|---|---|---|---|---|---|---|
||EAC-WM-S|25.00_±_0.04|26.53_±_0.06|0.59_±_0.03|0.22_±_0.02|0.11_±_0.02|
||EAC-WM-TFT|25.05_±_0.01|26.49_±_0.10|0.54_±_0.03|0.15_±_0.06|0.09_±_0.02|
|U|EAC-WM|25.03_±_0.04|26.53_±_0.12|0.61_±_0.03|0.21_±_0.02|0.11_±_0.01|
|nseen<br>I|LAC-WM-DFT|24.82_±_0.08|26.32_±_0.20|0.61_±_0.03|0.19_±_0.02|0.07_±_0.01|
|nstance|LAC-WM-(2,3)|24.88_±_0.04|26.51_±_0.08|0.54_±_0.09|0.21_±_0.01|0.09_±_0.01|
||LAC-WM-(1,2)|24.90_±_0.09|26.37_±_0.12|0.59_±_0.07|0.21_±_0.05|0.09_±_0.06|
||LAC-WM|**24.60**_±_0.07|**26.16**_±_0.19|**0.65**_±_0.06|**0.27**_±_0.06|**0.12**_±_0.02|
||EAC-WM-S|25.75_±_0.04|27.46_±_0.07|0.56_±_0.02|0.08_±_0.03|0.03_±_0.03|
||EAC-WM-TFT|25.68_±_0.06|27.39_±_0.11|0.54_±_0.00|0.13_±_0.05|0.07_±_0.01|
|U|EAC-WM|25.68_±_0.15|27.50_±_0.09|0.54_±_0.07|0.16_±_0.04|0.08_±_0.02|
|nseen<br>Ci|LAC-WM-DFT|25.57_±_0.04|27.35_±_0.05|0.53_±_0.08|0.19_±_0.01|0.09_±_0.02|
|ategores|LAC-WM-(2,3)|25.78_±_0.18|27.48_±_0.28|0.51_±_0.09|**0.21**_±_0.05|0.06_±_0.04|
||LAC-WM-(1,2)|25.65_±_0.09|27.43_±_0.09|0.48_±_0.07|0.09_±_0.01|0.03_±_0.02|
||LAC-WM|**25.39**_±_0.02|**27.21**_±_0.09|**0.61**_±_0.01|0.18_±_0.03|**0.10**_±_0.02|
||EAC-WM-S|25.38_±_0.04|26.99_±_0.06|0.55_±_0.03|0.15_±_0.03|0.07_±_0.03|
||EAC-WM-TFT|25.36_±_0.04|26.94_±_0.11|0.54_±_0.02|0.14_±_0.06|0.08_±_0.02|
||EAC-WM|25.36_±_0.10|27.01_±_0.10|0.58_±_0.05|0.18_±_0.03|0.09_±_0.02|
|Average|LAC-WM-DFT|25.19_±_0.06|26.83_±_0.12|0.57_±_0.05|0.19_±_0.02|0.08_±_0.02|
||LAC-WM-(2,3)|25.33_±_0.11|26.99_±_0.18|0.52_±_0.09|0.21_±_0.03|0.07_±_0.03|
||LAC-WM-(1,2)|25.27_±_0.09|26.90_±_0.11|0.54_±_0.07|0.15_±_0.03|0.06_±_0.04|
||LAC-WM|**24.50**_±_0.04|**26.68**_±_0.14|**0.61**_±_0.03|**0.22**_±_0.05|**0.11**_±_0.02|


**Table 6.** Robot planning performance for different methods using action selection from the training dataset. 

The training costs around 4 days on 64 H200 GPUs. 

**Model Inference** On an NVIDIA L40S GPU, the inference time is approximately 0.1 seconds for a batch size of 10 when predicting 8 future frames at 256×256 resolution. 

### **A.5. Action Selection from Training Dataset** 

To avoid potential bias introduced in VLA generated samples, we use action sequences sampled from the training dataset described in Section 4.3 to evaluate LAC-WM and EAC-WM under various fine-tuning strategies. 

We set _N_ =500, _p_ =30, and _k_ =5. This yields a sequence of 12-15 subgoals per episode. Since actions are chunked into 5-step segments for world model rollouts, this results in a 6-frame rollout per sequence. We execute all 30 actions in the selected sequence. We evaluate each model on 50 episodes for both splits. Each episode is repeated three times using different random seeds, and we report the averaged results in Table 6. We compare the performance of EAC-WM-S, EAC-WM, and LAC-WM. 

The results in Table 6 demonstrate that world-model–based action selection enables effective planning for dexterous manipulation. While the overall task success rate (S.R.) remains low due to the inherent difficulty of the task, models leveraging pretraining and fine-tuning (LAC-WM, EAC-WM) outperform the model trained from scratch (EAC-WM-S) on both evaluation splits. Notably, for the Unseen Categories split, LAC-WM achieves a final success rate of 10%, three times higher than EAC-WM-S. Pretraining also improves intermediate metrics: both the object contact rate (S.R.C.) and the object lifting rate (S.R.L.) increase, and the robot reaches states closer to the subgoal images, as indicated by lower image embedding distances ( _δf_ and _δfg_ ). Overall, LAC-WM achieves the best performance across all metrics, with significantly reduced embedding distances and higher task success rates. 

We further evaluate different fine-tuning strategies for both EAC-WM and LAC-WM, as summarized in Table 6. **EACWM-TFT** adopts a two-stage fine-tuning process: (1) fine-tuning the action encoder while freezing the FDM, followed by (2) end-to-end fine-tuning of both modules using LoRA (rank 2). **LAC-WM-DFT** performs end-to-end training of the action projector from scratch and fine-tuning of FDM using LoRA (rank 2). **LAC-WM-(2,3)** first trains an action projector from scratch with the FDM frozen, then jointly fine-tunes the action projector and FDM end-to-end using LoRA (rank 2). **LAC-WM-(1,2)** first fine-tunes the IDM and FDM of LAC-WM end-to-end using LoRA (rank 2), followed by training an action projector from scratch and end-to-end fine-tuning of the FDM using LoRA (rank 2). EAC-WM and LAC-WM are fine-tuned as in Section 4.3. 

15 

#### **Cross-Embodiment Robot Foundation World Models with Latent Actions** 


**Figure 8. Example roll-out of executing actions from a pre-trained VLA.** From top to bottom, the figure shows rollouts for: executing the mean of all sampled actions (VLA-mean), a random sampled action (VLA-random), and actions selected using EAC-WM-S, EAC-WM, and LAC-WM from the VLA samples. The task is to pick up the object and place it back on the counter. While LAC-WM successfully selects actions to complete the task, the other methods fail to grasp and lift the object. 

### **A.6. Vision-Language Action Model for Dexterous Manipulation** 

Here we give details of the VLA model for dexterous manipulation used in our experiments on world-model guided VLA action selection. The model processes vision and language inputs and generates action trajectories in a single forward pass. The architecture comprises the following key components: 

- Visual Encoder: RGB images captured from the robot’s onboard camera are processed using a pre-trained DINOv2 (Oquab et al., 2024) vision transformer. This encoder extracts high-level visual features, providing rich contextual information about the environment. The visual encoder is kept frozen during policy training. 

- Language Encoder: Task instructions, provided as natural language commands or tokenized text, are embedded using a pretrained language encoder. This allows the policy to flexibly condition its behavior on diverse language inputs. The language embeddings are kept frozen during policy training. 

- Proprioception and Action Encoders: The robot’s proprioceptive states (end-effector positions and finger joint angles) are encoded using transformer-based encoders, trained from scratch. These encoders capture the robot’s internal state, which is critical for precise control. The input dimension is 25, consisting of a 9-dimensional end-effector pose, and 16 finger joint angles. 

- Transformer Trunk: Encoded representations from all modalities (vision, language, proprioception, and previous actions) are fused using a 3-layer transformer trunk. This component, trained from scratch, enables effective cross-modal integration and reasoning. 

- Action Decoder (Diffusion Head): The fused multi-modal representation is decoded into action trajectories using a diffusion-based model head. Action space is future end-effector pose and finger joint angles, also 25 dimensional, predicted over an action horizon of 100. The diffusion head is trained with a diffusion loss, allowing the policy to model the distribution over possible future actions and generate diverse, high-quality action sequences. 

The policy predicts action sequences with a horizon length of 100 steps at a control frequency of 15Hz. We deploy the whole action chunk before replanning. The policy is trained with 2000 successful demonstrations of the robot picking and placing different objects. 

16 

**Cross-Embodiment Robot Foundation World Models with Latent Actions** 


**Figure 9. Latent Action PCA Analysis** . The representative examples from each of the cluster show that latent action in each cluster corresponds to semantically meaningful actions (e.g. opening and closing gripper, moving left and right) across different embodiments. 

### **A.7. Latent Action PCA Analysis** 

To further study the physical meaning of the latent actions, we conduct PCA analysis on the latent action embeddings. Specifically, we obtain the PCA vectors on the latent action sequences (of length 4) extracted from all pretraining datasets (AgiBot, Droid and EgoDex). By projecting these high-dimensional latents onto the first two principal components, we visualize structure of the latent action space and perfrom K-means clustering (K=4) to identify distinct action clusters. For each cluster, we select representative samples from each dataset that are closest to the cluster centroid. We then visualize the start and end images of the video sequence that produced these representative latent action sequences, as shown in Figure 9. The representative examples per cluster demonstrate that the learned latent actions capture consistent and meaningful motion patterns across different embodiments. 

17 

