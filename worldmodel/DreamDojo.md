---
title: "DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos"
date: "2026-02-06"
authors: "Shenyuan Gao; William Liang; Kaiyuan Zheng; Ayaan Malik; Seonghyeon Ye; Sihyun Yu"
venue: "ICML"
url: https://arxiv.org/abs/2602.06949
pdf: https://arxiv.org/pdf/2602.06949
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2602.06949)** / [論文ページ](https://arxiv.org/abs/2602.06949)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

_2026-2-9_ 


# **DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

**Shenyuan Gao**<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> **William Liang**<sup>1</sup><sup>_,_3</sup><sup>_†_</sup> **Kaiyuan Zheng**<sup>1</sup><sup>_,_4</sup><sup>_*_</sup> **Ayaan Malik**<sup>1</sup><sup>_,_5</sup><sup>_*_</sup> **Seonghyeon Ye**<sup>1</sup><sup>_,_6</sup> **Sihyun Yu**<sup>6</sup> **Wei-Cheng Tseng**<sup>1</sup><sup>_,_7</sup> **Yuzhu Dong**<sup>1</sup> **Kaichun Mo**<sup>1</sup> **Chen-Hsuan Lin**<sup>1</sup> **Qianli Ma**<sup>1</sup> **Seungjun Nah**<sup>1</sup> **Loic Magne**<sup>1</sup> **Jiannan Xiang**<sup>8</sup> **Yuqi Xie**<sup>1</sup> **Ruijie Zheng**<sup>1</sup> **Dantong Niu**<sup>1</sup><sup>_,_3</sup> **You Liang Tan**<sup>1</sup> **K.R. Zentner**<sup>1</sup> **George Kurian**<sup>1</sup> **Suneel Indupuru**<sup>1</sup> **Pooya Jannaty**<sup>1</sup> **Jinwei Gu**<sup>1</sup> **Jun Zhang**<sup>2</sup> **Jitendra Malik**<sup>3</sup> **Pieter Abbeel**<sup>3</sup> **Ming-Yu Liu**<sup>1</sup> **Yuke Zhu**<sup>1</sup><sup>_,_9</sup><sup>_‡_</sup> **Joel Jang**<sup>1</sup><sup>_‡_</sup> **Linxi “Jim” Fan**<sup>1</sup><sup>_‡_</sup> 1NVIDIA 2HKUST 3UC Berkeley 4UW 5Stanford 6KAIST 7UofT 8UCSD 9UT Austin _†_ Co-First Authors _*_ Core Contributors _‡_ Project Leads `dreamdojo-world.github.io` 


## **Abstract** 

**Being able to simulate the outcomes of actions in varied environments will revolutionize the development of generalist agents at scale. However, modeling these world dynamics, especially for dexterous robotics tasks, poses significant challenges due to limited data coverage and scarce action labels. As an endeavor towards this end, we introduce DreamDojo, a foundation world model that learns diverse interactions and dexterous controls from 44k hours of egocentric human videos. Our data mixture represents the largest video dataset to date for world model pretraining, spanning a wide range of daily scenarios with diverse objects and skills. To address the scarcity of action labels, we introduce continuous latent actions as unified proxy actions, enhancing interaction knowledge transfer from unlabeled videos. After posttraining on small-scale target robot data, DreamDojo demonstrates a strong understanding of physics and precise action controllability. We also devise a distillation pipeline that accelerates DreamDojo to a real-time speed of 10.81 FPS and further improves context consistency. Our work enables several important applications based on generative world models, including live teleoperation, policy evaluation, and model-based planning. Systematic evaluation on multiple challenging out-of-distribution (OOD) benchmarks verifies the significance of our method for simulating open-world, contact-rich tasks, paving the way for general-purpose robot world models.** 

© 2026 NVIDIA. All rights reserved. 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

## **1. Introduction** 

World models, which predict futures based on actions, have emerged as a key component in the development of generalist robots (Hu et al., 2023; LeCun, 2022; Richens et al., 2025; Sutton, 1991). Recent advances in video generation (Ali et al., 2025; Wan et al., 2025) have driven video world models, in which future states are represented as video frames (Ball et al., 2025; Russell et al., 2025; Sun et al., 2025). However, they primarily plateau at discrete controls, while the high-dimensional action spaces for contact-rich robot tasks have yet to make similar progress. Unlike game and driving data, robot data often has limited coverage due to hardware variability and collection cost. The nearly infinite variety of real-world environments can easily exceed the distribution of available robot data. Additionally, existing datasets predominantly consist of expert demonstrations, lacking the stochasticity in intentions necessary for learning strong action controllability. As a result, existing video world models remain confined to simulating observed setups and are often unresponsive to counterfactual actions, constraining their applicability for diverse scenarios and complex tasks. 

In this work, we introduce **DreamDojo** , a foundation world model for open-world dexterous robot tasks. Unlike previous methods that typically rely on teleoperation data, we exploit _human videos_ for pretraining. Despite the embodiment gap, the underlying physics during interactions is largely consistent between humans and robots, enabling effective knowledge transfer. Therefore, we curate the _largest_ egocentric human video dataset to date, **DreamDojo-HV** (Human Videos), which comprises 44k hours of video sequences, surpassing the datasets used in prior works by several orders of magnitude. In addition to its scale, DreamDojo-HV incorporates an exceptionally diverse range of activities, encompassing approximately 96 _×_ more skills and 2,000 _×_ more scenes than the most diverse public datasets for robot learning (Bu et al., 2025; Khazatsky et al., 2024). This provides us with a rich corpus for learning physics and dynamics about diverse interactions. 

Nevertheless, fine-grained action labels are much scarcer than raw videos at scale. Naively training on passive videos overlooks the causality between video observations and actions, leading to inferior knowledge transfer for action-conditioned world simulation. Moreover, converting various action formats into a unified one entails inevitable engineering effort. To address these challenges, we introduce _continuous latent actions_ (Gao et al., 2025) as unified proxy actions for all videos. The proposed latent action model can extract semantically meaningful actions between frames in a self-supervised manner, ensuring effective transfer of both physics and controllability as the data scales to the internet level. Through rigorous designs of model architecture and training recipe, DreamDojo is able to acquire a comprehensive understanding of physics, achieving plausible simulations across diverse environments and fine-grained controllability over continuous robot actions. 

To achieve real-time prediction without visual degradation, we further introduce a distillation pipeline following the Self Forcing paradigm (Huang et al., 2025). Our distillation also enhances the long-horizon consistency by efficiently modeling a short temporal context. The resulting model can autoregressively predict future frames at a resolution of 640 _×_ 480 at 10.81 FPS for an arbitrary horizon, significantly reducing the cost for various downstream applications such as live teleoperation and model-based planning. 

In summary, our main contributions include: 

- **A large-scale video dataset** , DreamDojo-HV, that accumulates 44k hours of egocentric experiences from a wide spectrum of daily activities. To the best of our knowledge, this is the _largest_ and most diverse data corpus to date for world model learning. 

- **A foundation world model** for general-purpose robots. By scaling up human videos and introducing continuous latent actions as unified proxy, we present DreamDojo, the _first_ world model of its kind that shows zero-shot generalization to unseen objects and novel environments. 

- **A distillation pipeline** that enables efficient autoregressive prediction and improves context consistency. The final model can be interacted with for more than 1 minute in real time without degradation. 

- **Multiple downstream applications** highlight the potential of DreamDojo in performing live teleoperation, policy evaluation, model-based planning, _etc_ ., accelerating the development of robot policies. 

2 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 1: **DreamDojo overview.** DreamDojo acquires comprehensive physical knowledge from large-scale human datasets by utilizing latent actions as unified labels. After post-training and distillation on the target robots, our model can predict the future world in real time with continuous action controls. DreamDojo can robustly generalize to various objects and environments, facilitating large-scale policy evaluation without real-world deployment. It also enables live teleoperation and online model-based planning. 

## **2. Preliminary** 

**Interactive world model.** The objective of an interactive world model is to infer future states based on actions. Formally, given an action _𝑎 ∈𝒜_ , the interactive world model acts as a state transition function that samples the next state: 


where _𝑝_ : _𝒮× 𝒜→_ ∆( _𝒮_ ) is the transition distribution. In this paper, the term “world model” refers specifically to this category unless otherwise stated. 

**Cosmos-Predict2.5 model.** We establish our world model on the pretrained Cosmos-Predict2.5 model (Ali et al., 2025), a latent video diffusion model that predicts future frames with text and conditional frame inputs. The Cosmos-Predict2.5 model operates in the continuous latent space produced by WAN2.2 tokenizer (Wan et al., 2025). It injects language and timestep conditions into each DiT block (Peebles and Xie, 2023). The text embedding is processed by cross-attention layers, while the timestep information is first encoded by sinusoidal embeddings, projected by a lightweight MLP, and then used by adaptive layer normalization for dynamic modulations (scale, shift, gate) (Ali et al., 2025). The whole network is trained using flow matching loss (Lipman et al., 2022). Specifically, given the noise corrupted video latent **x** _𝑡_ at timestep _𝑡_ , the flow matching loss minimizes the prediction error with the ground-truth velocity **v** _𝑡_ : 


where **v** _𝑡_ is a difference between the noise **_𝜖_** and the clean sample **x** ( _i.e_ ., **v** _𝑡_ = **_𝜖_** _−_ **x** ), **c** denotes any conditions ( _e.g_ ., text, conditional frames, and actions for world models), and **u** ( _·_ ; _𝜃_ ) is the denoiser parametrized by _𝜃_ . 

## **3. Approach** 

### **3.1. Overview** 

In this section, we first introduce the features of our dataset in Sec. 3.2, and then describe the architecture of DreamDojo and its training recipe in Sec. 3.3. Our whole training procedure consists of three phases: 

3 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 2: **Distribution analysis of DreamDojo-HV. (a)** Distribution of the scenarios and random examples from the most frequent categories. **(b)** [Left]: Distribution of subtask numbers within each video. Most videos involve long-horizon tasks that require multiple interactions to accomplish. [Right]: Representative skills in DreamDojo-HV and their frequencies. Our dataset covers a wide range of interaction types beyond pick-and-place. **(c)** Visualization of skill verbs and object names based on their frequency of occurrence in language annotations. 

1. **Pretraining from human videos.** At this stage, we curate three egocentric human datasets for pretraining: In-lab, EgoDex, and DreamDojo-HV. Continuous latent actions are introduced as conditions for all videos. 

2. **Post-training on target robots.** To adapt DreamDojo to different embodiments, we reset the action conditioning layer and learn the new action space through finetuning. The post-training can be conducted on a target robot dataset collected from limited scenarios. 

3. **Distillation.** Once DreamDojo has learned the target action space, a distillation process can be applied to improve real-time interactivity and context consistency. 

### **3.2. DreamDojo-HV Dataset** 

Existing robot world models are primarily limited to in-distribution settings and fall short in generalizing to unseen interactions with new objects (Team et al., 2025; Zhang et al., 2025). In essence, this limitation arises because most datasets only cover a relatively narrow distribution with limited verbs, objects, and environments, thereby restricting the breadth of interaction patterns. As a result, training on these datasets often fails to preserve the model’s abilities when extending to out-of-distribution scenarios. 

To address this limitation, one might consider increasing the scale of real robot data. However, this may not be the most efficient approach to encompass all potential interaction types, as each new trajectory involves costly teleoperation. On the other hand, human videos, which can be captured during daily activities, emerge as a promising axis to empower robot learning (Bi et al., 2025; Chen et al., 2025,; Kareer et al., 2025; Li et al., 2025; Liu et al., 2025; Luo et al., 2025; Qiu et al., 2025; Wang et al., 2024; Yang et al., 2025; Ye et al., 2025; Zheng et al., 2025). Inspired by these studies, we scale up human videos as a pioneering step for world model pretraining. Our human data comes from three sources: 

1. **In-lab** is collected in our tabletop settings at our laboratory to validate our core designs. The collectors are wearing Manus gloves with Vive Ultimate Tracker to capture precise hand poses, which can be readily 

4 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

|Dataset|Type|Prior Works|# Hour|# Trajectory|# Skill|# Scene|
|---|---|---|---|---|---|---|
|RT-1|Robot|IRASim, UniSim|900|130k|8|2|
|BridgeData V2|Robot|IRASim, UniSim,<br>WorldGym, WMPE|130|60.1k|13|24|
|Language-Table|Robot|IRASim, UniSim,<br>HMA|2.7k|442k|-|-|
|RoboNet|Robot|iVideoGPT, IRASim|-|162k|-|10|
|DROID|Robot|Ctrl-World, UWM|350|76k|86|564|
|AgiBot-World|Robot|EnerVerse-AC|2.9k|1,000k|87|106|
|Nymeria|Human|PEVA, EgoTwin,<br>EgoControl|300|1.2k|-|50|
|In-lab|Human|-|55|13.9k|35|1|
|EgoDex|Human|-|829|30k|194|5|
|DreamDojo-HV|Human|-|43,827|1,135k|6,015<sup>_†_</sup>|1,135k|
|**Our Mixture**|Human|-|44,711|1,179k|_≥_6,015<sup>_†_</sup>|_≥_1,135k|


Table 1: **Scale and diversity comparison to existing large-scale datasets used by previous world models.** Our curated data mixture excels in both scale and diversity, encompassing 15 _×_ longer duration, 96 _×_ more skills, and 2,000 _×_ more scenes than the previously largest dataset for world model training.<sup>_†_</sup> Estimated by GPT based on the global language annotation of each video clip. 

retargeted to the GR-1 robot actions. It contains several new objects and new verbs that are unseen in our default robot training dataset. 

2. **EgoDex** (Hoque et al., 2025) is a public dexterous human manipulation dataset with egocentric views recorded by Apple Vision Pro. It has 829 hours of egocentric videos with high-precision 3D hand and finger poses collected at the time of recording. It also contains a variety of everyday household objects. We include it to our data suite to enrich object variety. 

3. **DreamDojo-HV** is a large-scale in-house dataset collected through crowdsourcing. It features a wide spectrum of loco-manipulation skills and extremely diverse environments, such as household, industrial, retail, educational, and administrative (see Fig. 2 for the distribution), which significantly increases the scale and diversity of our data corpus. Each episode is annotated with a text that describes the task being performed. 

As shown in Tab. 1, our final dataset comprises a total of 44,711 hours, making it the largest human interaction dataset to date for world model pretraining. It includes more than 9,869 unique scenes, 6,015 unique tasks, and 43,237 unique objects, representing the majority of interactions in daily activities. Its scale and diversity also provide thorough coverage of various action distributions and increase the stochasticity of the future, thereby enhancing the controllability of actions. In Sec. 4.3, we demonstrate that increasing the data scale and diversity continues to enhance model performance across all benchmarks. 

### **3.3. DreamDojo Foundation World Model** 

#### **3.3.1. Model Architecture** 

Unlike conventional video generators (Ali et al., 2025; Wan et al., 2025), world models are distinct in their prioritization on action controllability (Huang et al., 2025; Yang et al., 2025, 2024). Different from interactive games with discrete inputs (Parker-Holder et al., 2024), achieving genuine controllability for robot actions presents more challenges due to its high dimensionality and contact-rich nature. 

To realize precise action following, we propose two improvements based on the original architecture. First, instead of using the absolute robot joint poses, we transform them into relative actions by rebaselining the inputs with the pose at the beginning of each latent frame ( _i.e_ ., every 4 timesteps). Since relative actions are often concentrated in a narrower space shared across various trajectories, this significantly reduces modeling complexity, thereby enhancing generalization to continuous and compositional robot actions. 

5 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 3: **Latent action model.** [Left]: The information bottleneck design of our latent action model enforces action disentanglement, producing a continuous latent vector that represents actions between frames. [Right]: We retrieve and group the frame pairs from different datasets that share the most similar latent actions. The embodiments are performing the same actions despite the significant differences in context. 

Second, since the consequences of interactions strictly follow causality, observing future actions does not aid predictions at the current timestep but rather increases irrelevant noise. Therefore, instead of sending the entire relative action trajectory as a global condition for all latent frames, we inject actions into the latent frames as chunks (Guo et al., 2025; Huang et al., 2025; Zhu et al., 2025). Specifically, since the temporal compression ratio of the WAN2.2 tokenizer (Wan et al., 2025) is 4 ( _i.e_ ., video latent _𝑥_<sup>_𝑖_</sup> corresponds to 4 frames _𝑓_<sup>_𝑖_:</sup><sup>_𝑖_+4</sup> in the pixel space, _𝑥_<sup>_𝑖_+1</sup> corresponds to _𝑓_<sup>_𝑖_+4:</sup><sup>_𝑖_+8</sup> , and so on), we concatenate 4 consecutive actions _𝑎_<sup>_𝑡_:</sup><sup>_𝑡_+4</sup> as a chunk and send them to the corresponding latent frame together. This strong prior can greatly mitigate the causality confusion, thereby improving learning efficiency and ultimately enhancing controllability. We show the effects of these two designs above on both expert and counterfactual trajectories in Sec. 4.5. 

#### **3.3.2. Pretraining from Human Videos** 

**Latent action as proxy action.** While our data suite includes comprehensive real-world activities, it does not come with fine-grained action annotations. To inherit the rich knowledge from this unlabeled dataset, one straightforward solution is to pretrain the model by passively predicting future frames. In our experiments, we found that this simple approach can transfer certain physical knowledge from human videos, resulting in more physically plausible modeling for unseen objects. Nevertheless, since world models must learn the consequences of actions, relying solely on actionless videos may lead to an inadequate understanding of the causality, ultimately resulting in inferior interactivity when adapting to the target robots. 

To address the inefficient knowledge transfer caused by absence of action labels, it is crucial to derive pseudo labels from pixels that describe the current actions. While off-the-shelf models like HaMeR (Pavlakos et al., 2024) can extract hand poses at scale, these models struggle to represent actions beyond the hands ( _e.g_ ., arm movements and locomotions) and often face challenges in inferring hand positions in heavy occlusions and camera movements. In addition, they primarily focus on low-level features of the human hands, which may hinder effective knowledge transfer to the target robot when there is a significant embodiment gap. 

On the other hand, latent actions (Bruce et al., 2024; Gao et al., 2025; Ye et al., 2025), which extract action information purely from videos in a self-supervised manner and provide consistent action interpretation across embodiments, have gained increasing attention recently. Inspired by (Gao et al., 2025), we adopt continuous 

6 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

latent actions due to their superiority in cross-embodiment generalization and efficient adaptability. We establish a latent action model as a VAE (Kingma and Welling, 2013) using the spatiotemporal Transformer architecture (Bruce et al., 2024). It has an information bottleneck design that can automatically disentangle the most critical action information from the context. Specifically, unlike the standard VAE, our VAE encoder takes two consecutive frames _𝑓_<sup>_𝑡_:</sup><sup>_𝑡_+1</sup> , extracts spatiotemporal features, and projects the global features to a low-dimensional embedding _𝑎_ ˆ _𝑡_ . The VAE decoder receives this embedding along with the former frame _𝑓_<sup>_𝑡_</sup> , aggregates the information and predicts the subsequent frame _𝑓_<sup>_𝑡_+1</sup> . The entire VAE is supervised by the reconstruction loss of the later frame and the KL divergence. The compactness of the embedding and the regularization term together create an information bottleneck. To reconstruct the later frame, the model has to disentangle and compress the most critical motions between frames. 


In egocentric human videos, we found that this embedding particularly captures the human actions and can be transferred across embodiments (see Fig. 3). Ultimately, we are able to utilize latent actions as unified proxy labels for world models. During pretraining, we condition each latent frame on the chunked latent actions. Concretely, after extracting latent actions from consecutive frames, we project them using a lightweight MLP to match the dimensions of the timestep embeddings. The last layer of the action MLP is initialized with zeros to avoid perturbing the pretrained model state at the beginning of training (Zhang et al., 2023), which we empirically found leads to improved physics. The projected embeddings are added with the timestep embeddings and then fed into the adaptive layer normalization within each DiT block. 

**Training objective.** As mentioned in Sec. 2, Cosmos-Predict2.5 employs the standard flow matching loss (Eq. (2)) as its training objective. However, this individual supervision of each frame overlooks the temporal correlation between video frames, which could provide a more direct signal for learning object dynamics and action following. Inspired by previous studies (Gao et al., 2024; Wang et al., 2024; Yang et al., 2025), we modify Eq. (2) to a new loss that aims to match the ground-truth temporal transitions. Let **z** _𝑡_ = **u** ( **x** _𝑡, 𝑡,_ **c** ; _𝜃_ ) represent the predicted velocity, then the proposed temporal consistency loss can be expressed as: 


Here, _𝐾_ is the total length of the video latent, [ _𝑧_<sup>1</sup> _, 𝑧_<sup>2</sup> _, . . . , 𝑧_<sup>_𝑘_</sup> ] and [ _𝑣_<sup>1</sup> _, 𝑣_<sup>2</sup> _, . . . , 𝑣_<sup>_𝑘_</sup> ] are frames in **z** _𝑡_ and **v** _𝑡_ , respectively. In practice, we found that this loss term not only accelerates the learning of action controllability but also effectively enhances object completeness and reduces artifacts. Therefore, our final training objective becomes: 


where _𝜆>_ 0 is a trade-off coefficient to balance the optimization. We use _𝜆_ = 0 _._ 1 in our experiments. 

#### **3.3.3. Post-Training on Target Robots** 

Although learning from human videos exposes the model to a wide range of physics interactions, we still require a post-training stage on the target robot data to adapt our model for downstream applications. To achieve this, we flatten the ground-truth actions of the target robot into a sequence and project the entire sequence through the action MLP. To match the target action space, we reinitialize the first layer of the action MLP and fully finetune it along with all other pretrained weights. Thanks to strong pretraining, the target robot dataset can be collected in limited domains at a small scale while still achieving zero-shot generalization after finetuning. The continuity of our latent action space also ensures better adaptation results compared to other variants (Gao et al., 2025). 

7 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

#### **3.3.4. Distillation** 

In order to unlock capabilities like live teleoperation and online model-based planning, our world model must be able to run autoregressively in real time (Huang, 2025). However, existing video diffusion models are often limited in achieving this due to (1) their bidirectional attention architecture, which defines a fixed horizon length, and (2) a large number of denoising timesteps ( _e.g_ ., 50), which severely hampers inference speed. 

Thus, we introduce an additional distillation stage that converts the foundation DreamDojo model into an autoregressive, few-step diffusion model. We build on the process introduced by Self Forcing (Huang et al., 2025), which uses two training stages to distill teacher _𝐺_ teacher to student _𝐺_ student. We construct _𝐺_ student with the same architecture and model weights of _𝐺_ teacher, with the exception of the bidirectional attention mechanism, which is replaced with causal attention, and the timestep schedule, which is shortened to a few steps ( _e.g_ ., 4). 

**Warmup stage.** In the first “warmup” stage, we regress student predictions to match ODE solutions generated by our teacher, 


where _𝑥_ 0 is from the teacher’s ODE trajectory. In this stage, the student generates via teacher forcing, _i.e_ ., its context consists of latents generated by the teacher. 

**Distillation stage.** Afterwards, in the second “distillation” stage, we construct the student context with its own previously-generated latents, instead of continuing teacher forcing from the first stage. This aligns the training distribution with what the model will receive at inference time, thereby reducing compounding error. To supervise this stage, we guide the student distribution toward the teacher via a distribution matching loss (Yin et al., 2024) based on the Kullback-Leibler (KL) divergence between real (teacher) and fake (student) distributions, 


Computing the loss in this form is intractable, but we can directly compute its gradient, using real and fake diffusion models _𝑠_ real and _𝑠_ fake to estimate the score, 


where _𝑧 ∼𝒩_ (0 _, 𝐼_ ) is noise, _𝑥𝑡_ is produced via forward diffusion with _𝐺_ student starting at _𝑧_ , and _𝑠_ real is estimated by _𝐺_ teacher whereas _𝑠_ fake is estimated by a model trained on the predictions of _𝐺_ student. 

This process minimizes the train-test distribution mismatch, as the student is trained to generate from its previous outputs. However, despite this alignment, generation quality can still degrade over long horizons. To improve robustness against compounding errors, we propose to have the student generate _𝑁_<sup>_′_</sup> _> 𝑁_ frames, where _𝑁_ represents the horizon of the teacher. This simulates longer student rollouts, thus further minimizing the train-test discrepancy. To supervise the student’s prediction, we randomly select a window of size _𝑁_ , which receives gradients via the _ℒ_ distill loss (Eq. (8)). 

## **4. Experiments** 

In this section, we conduct extensive experiments to demonstrate DreamDojo’s strengths. Specifically, we aim to answer the following questions: (1) Compared to actionless pretraining, can latent actions enable more effective transfer from human videos? (Sec. 4.2) (2) Can more diverse data help generalize to new types of physical interaction and scenarios? (Sec. 4.3 and Sec. 4.4) (3) Can our architectural design and training objective improve the action-conditioned prediction? (Sec. 4.5) (4) Can our distillation pipeline accelerate and stabilize long-horizon interactions? (Sec. 4.6) (5) How can we apply DreamDojo in downstream applications to facilitate robot learning? (Sec. 4.7) 

8 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 4: **Benchmark visualization.** We rigorously construct six evaluation benchmarks that reflect the diverse scenarios and actions present in human datasets, while being out-of-distribution for the robot training datasets. 

### **4.1. Experimental Setup** 

**Training and inference.** The latent action model is a 700M spatiotemporal Transformer (Bruce et al., 2024) that is trained for 400k steps with a total batch size of 256. The dimension of the latent action is 32. The model has 24 encoder blocks for latent action extraction and 24 decoder blocks for forward dynamics prediction. It is trained on a data mixture of the three human video datasets, as well as our in-house robot datasets, including Unitree G1, Fourier GR-1, AgiBot, and YAM. The original videos are temporally downsampled by a random factor of _{_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ to capture various kinds of motions. The video frames are center cropped and resized to a fixed resolution of 320 _×_ 240. The _𝛽_ in Eq. (3) is set to 10<sup>_−_6</sup> to achieve a good trade-off between representation capacity and transferability for post-training. We employ the AdamW (Loshchilov and Hutter, 2019) with a weight decay of 0.01 and a constant learning rate of 2 _._ 5 _×_ 10<sup>_−_5</sup> to train the latent action model from scratch. 

The world model is initialized from Cosmos-Predict2.5 (Ali et al., 2025) and pretrained on the mixture of our In-lab, EgoDex, and DreamDojo-HV datasets, with a sampling ratio of 1:2:10, respectively. The video frames are center cropped and resized to a fixed resolution of 640 _×_ 480, and then clipped into sequences with a length of 13 for pretraining. The text condition is fixed as an empty prompt. We present two variants of DreamDojo: a 2B model and a 14B model. Both models are pretrained for 140k steps with an effective batch size of 1024 using 256 NVIDIA H100 GPUs. We use AdamW (Loshchilov and Hutter, 2019) with a weight decay of 0.1, and set the learning rate to 1 _._ 6 _×_ 10<sup>_−_4</sup> . An exponential moving average (EMA) is maintained throughout the training and used to generate all our results. 

In the post-training stage, the videos of the target embodiment ( _e.g_ ., G1, GR-1, AgiBot) are sampled at roughly 10 Hz to capture feasible motions. The video clips are then organized as sequences with a length of 13. The first frame serves as the condition frame, and the raw actions are processed as relative actions with a length of 12. The world model is finetuned with all weights updated using a similar hyperparameter setting as in the pretraining stage. By default, post-training is conducted with 128 NVIDIA H100 GPUs for 50k steps with a batch size of 512. 

9 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

|**Method**||**In-lab Eval**||**Method**|**E**|**goDex Eva**|**l**|
|---|---|---|---|---|---|---|---|
||PSNR_↑_|SSIM_↑_|LPIPS_↓_||PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|w/o pretrain|20.576|0.774|0.222|w/o pretrain|19.952|0.787|0.219|
|action-free|20.797|0.773|0.222|action-free|19.924|0.783|0.222|
|latent action|**20.913**|**0.776**|**0.219**|latent action|**20.344**|**0.790**|**0.214**|
|retargeted action|20.960|0.773|0.219|MANO|20.474|0.795|0.211|


Table 2: **Effects of different action conditioning methods.** Latent action conditioning performs on par with the ideal settings in simulation quality and is the most scalable in use. We denote retargeted action and MANO in gray because they represent ideal collection setups when additional action capture devices are equipped. The best results are marked with **bold** , and the second best results are underlined. 

The distillation stage initializes the autoregressive student model with the weights of the teacher, while replacing bidirectional attention with causal attention over a sliding window size of 12 frames. First, for the warmup stage, we generate 10k ODE trajectories and train for 10k iterations. Next, for the distillation step, we have the student randomly generate between 13 and 49 frames during training, and compute loss on the last 13 generated frames. We run this distillation step for 3k iterations. All distillation is conducted on 64 NVIDIA H100 GPUs, using a batch size of 256 for the warmup stage and 64 for the distillation stage. 

During inference, the teacher model utilizes 35 denoising steps for generation, while the distilled model reduces this number to 4 steps. Classifier-free guidance (Ho and Salimans, 2022) is disabled as we empirically found it brought limited benefits. 

**Benchmark construction.** To demonstrate the effectiveness of our method, we conduct a systematic evaluation that emphasizes out-of-distribution scenarios and counterfactual actions. To be specific, we mirror the diverse and novel interactions in the three human datasets and construct three corresponding evaluation sets using the Fourier GR-1 humanoid robot: (1) **In-lab Eval** , (2) **EgoDex Eval** , (3) **DreamDojo-HV Eval** . We make every effort to replicate the objects observed in the human videos, allowing our robots to perform the same interactions that reflect similar underlying physics. We also collect a (4) **Counterfactual Eval** set that focuses on counterfactual actions not present in current robot learning datasets, such as patting a toy or reaching toward an object but missing it. To assess DreamDojo’s generalization to diverse environmental changes, we further employ Gemini 2.5 Flash Image ( _a.k.a_ . Nano Banana) (Comanici et al., 2025) to edit the backgrounds of EgoDex Eval and DreamDojo-HV Eval to replicate typical observations in the original datasets. This results in (5) **EgoDex-novel Eval** and (6) **DreamDojo-HV-novel Eval** , with each consisting of 25 samples. A glimpse of the samples from our benchmarks is provided in Fig. 4. 

**Evaluation protocol.** To quantify the model performance on our evaluation sets, we use PSNR (Hore and Ziou, 2010), SSIM (Hore and Ziou, 2010), and LPIPS (Zhang et al., 2018) as our three main automatic metrics. When evaluating the models without distillation, we generate 100 future videos over three rounds by autoregressively resetting the condition frame with the last prediction to make the discrepancies between different variants more discriminative, resulting in 100 samples with 49 frames for most of our evaluations. We choose Fourier GR-1 as a representative target embodiment for most ablative studies. 

Since the ground-truth videos are unavailable for EgoDex-novel Eval and DreamDojo-HV-novel Eval, we design a human preference evaluation protocol following recent advances (Gao et al., 2024; Wan et al., 2025; Yin et al., 2025). Specifically, we make a web UI and invite 12 volunteers to judge side-by-side video pairs from physics correctness of object interactions and action following compared to the ground-truth video. For physics correctness, they are suggested to focus on object permanence, shape consistency, and contact causality. For action following, we encourage the evaluators to pay more attention to the pose of the robots and allow for a “tie”. We also provide evaluation examples beforehand to justify the key factors the evaluators should focus on. The order of the videos in each pair will be randomly switched to avoid bias, and we average all win rates 

10 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

|**Pretrained Model**|**I**|**n-lab Eva**|**l**|**E**|**goDex Eva**|**l**|**Dream**|**Dojo-HV**|**Eval**|**Count**|**erfactual**|**Eval**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|Cosmos-Predict2.5|20.576|0.774|0.222|19.952|0.787|0.219|18.274|0.754|0.236|20.472|0.802|0.190|
|Data Mixture|||||||||||||
|In-lab|20.913|0.776|0.219|20.267|0.785|0.218|18.621|0.754|0.233|20.755|0.796|0.187|
|In-lab+EgoDex|20.972|0.778|0.216|20.334|**0.791**|0.215|18.706|**0.762**|0.230|20.797|0.796|0.188|
|In-lab+EgoDex+DreamDojo-HV|21.016|0.781|0.215|20.414|0.790|0.216|18.724|0.759|0.232|20.852|**0.799**|0.188|
|DreamDojo-2B|21.114|0.774|0.222|20.411|0.775|0.226|18.813|0.747|0.238|20.907|0.787|0.192|
|DreamDojo-14B|**21.413**|**0.788**|**0.208**|**20.525**|0.787|**0.213**|**18.924**|0.751|**0.228**|**21.087**|0.793|**0.185**|


Table 3: **Effects of using different data mixtures.** Adding more human datasets to pretraining consistently improves the performance for both out-of-distribution scenarios and counterfactual actions, highlighting the the potential of our approach. The best results are marked with **bold** , and the second best results are underlined. 

against the anchor model to obtain the final results. More details can be found in the Appendix. 

### **4.2. Effects of Different Action Conditions** 

We conduct experiments on both In-lab Eval and EgoDex Eval. To demonstrate the efficacy of the proposed latent action conditioning, we compare our method with three representative baselines: 

1. **Without pretraining.** In this setup, the model is initialized from Cosmos-Predict2.5 directly for posttraining without observing the human videos. 

2. **Action-free pretraining.** In this baseline, we pretrain the world model on unlabeled videos as passive future prediction. The pretrained model is then used for post-training. 

3. **Ground-truth action conditioning.** In this baseline, we pretrain the world model with ground-truth action conditioning. This is an ideal setting, where additional equipment is required to obtain high-quality action labels. Specifically, on the In-lab dataset, we condition our model on retargeted GR-1 actions captured by Manus gloves with a Vive Ultimate Tracker, which are mapped to the real GR-1 action specifications for each degree of freedom. The EgoDex dataset utilizes Apple Vision Pro to capture hand poses, which are subsequently transformed into MANO (Romero et al., 2022) by ourselves as conditions during pretraining. 

All compared methods are pretrained for 50k steps on the corresponding human datasets and post-trained for 25k steps on the in-distribution GR-1 dataset. The post-trained models are evaluated on In-lab Eval and EgoDex Eval, which contain novel objects and actions not present in the GR-1 training dataset. The results are reported in Tab. 2. While pretraining on human videos through action-free video prediction brings marginal benefits, introducing latent actions significantly narrows the gap to the ideal scenario where ground-truth action labels are available. We also provide the PSNR curves throughout the post-training stage in the Appendix. Pretraining with latent actions can reach a much higher upper bound than action-free pretraining and without pretraining. Note that, although MANO actions can also be extracted from videos (Pavlakos et al., 2024), it is likely not as precise as using the Apple Vision Pro to derive the MANO labels in Tab. 2. Hence, we choose latent actions as unified proxy actions for all human videos during pretraining. 

### **4.3. Effects of Different Data Mixtures** 

We also conduct a dataset ablation to validate the benefits of increasing data diversity. Specifically, we pretrain our model on different data combinations for 50k steps, and then post-train on the GR-1 dataset for 25k steps. Unlike our final models, the sampling ratio is uniform across each dataset for the model variants in this ablation study. We evaluate the post-trained models on In-lab Eval, EgoDex Eval, and DreamDojo-HV Eval, which contain unseen object interactions, as well as on Counterfactual Eval, which features counterfactual actions. From the results in Tab. 3, increasing data diversity not only improves physics modeling but also enhances the controllability for out-of-distribution actions. 

11 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

|**Metric**|DreamDojo-2B ><br>Cosmos-Predict2.5|DreamDojo-14B ><br>Cosmos-Predict2.5|DreamDojo-14B ><br>DreamDojo-2B|
|---|---|---|---|
|Physics Correctness|62.50%|73.50%|72.50%|
|Action Following|63.45%|72.55%|65.53%|


Table 4: **Human preference evaluation in diverse out-of-distribution scenarios.** DreamDojo outperforms the pretrained Cosmos-Predict2.5 by a non-trivial margin. Our DreamDojo-14B demonstrates the most competitive performance in both physics correctness and action following. 

||**Modifications**|**i**||**GR-1 Val**||**Coun**|**terfactual**|**Eval**|
|---|---|---|---|---|---|---|---|---|
|relative|chunked|temporal|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
||||16.199|0.557|0.315|19.448|0.768|0.211|
|✓|||16.522|0.576|0.304|19.482|0.772|0.212|
|✓|✓||17.626|0.620|0.267|20.783|0.790|0.193|
|✓|✓|✓|**17.630**|**0.622**|**0.266**|**20.980**|**0.796**|**0.189**|


Table 5: **Ablations of architecture and loss designs.** Our design choices can effectively enhance the simulation quality of both expert and counterfactual trajectories. 

### **4.4. Generalization to Unseen Scenarios** 

To benchmark the generalization ability in unseen scenarios, we generate video samples using the two final models, DreamDojo-2B and DreamDojo-14B, and conduct evaluations with Cosmos-Predict2.5 without human video pretraining. All models are post-trained for 30k steps. After post-training, we ask 12 volunteers to evaluate three model pairs: DreamDojo-2B _vs_ . Cosmos-Predict2.5, DreamDojo-14B _vs_ . Cosmos-Predict2.5, and DreamDojo-14B _vs_ . DreamDojo-2B. The evaluation is conducted on 50 samples from EgoDex-novel Eval and DreamDojo-HV-novel Eval. The results in Tab. 4 show that our DreamDojo-2B surpass the original CosmosPredict2.5 in both physics correctness and action following by a non-trivial margin, while DreamDojo-14B exhibits a clear advantage over DreamDojo-2B in both axes due to its large capacity. 

### **4.5. Ablations of Our Design Choices** 

To efficiently verify the effectiveness of our architectural design and training objective, we finetune CosmosPredict2.5 for 30k steps only on the GR-1 training dataset. The finetuned models are then evaluated on a held-out GR-1 validation set with expert demonstrations and the Counterfactual Eval set. Starting with the simple CosmosPredict2.5 base architecture, we gradually apply our modifications: relative action transformation, chunked action injection, and the temporal consistency loss. The evaluation results are shown in Tab. 5. Both relative actions and chunked injection can significantly improve simulation quality, indicating their importance for achieving precise action controllability. The proposed temporal consistency loss further improves performance on both benchmarks, demonstrating its effectiveness in enhancing action following and object modeling. In the Appendix, we also provide qualitative comparisons for these variants. 

### **4.6. Benefits of Distillation** 

To unlock real-time inference, we distill the GR-1 post-trained variant of DreamDojo-2B using the same GR-1 dataset. Stress testing the capabilities of this distillation process, we run both the teacher and student models on GR-1 Long Eval, generating 600 frames (1 minute) of long-horizon, multi-stage tasks. As seen in Tab. 6, our student model, despite being few-step and autoregressive, achieves performance close to that of the teacher while running nearly 4 _×_ faster on a single NVIDIA H100 GPU. In addition, the autoregressive architecture of our student offers two extra advantages. First, since the student generates each latent frame autoregressively, it enables real-time streaming, which we demonstrate in Sec. 4.7 is crucial for multiple downstream applications. Second, unlike the teacher that is conditioned on a single initial frame, the distilled model can naturally incorporate multiple frames as context, resulting in superior robustness to occlusions and camera shifts. See our Appendix for qualitative samples. 

12 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

|**Mthd**|**G**|**R-1 Long Eva**|**l**||**Interactivity**||
|---|---|---|---|---|---|---|
|**eo**|PSNR_↑_|SSIM_↑_|LPIPS_↓_|FPS_↑_|predict len_↓_|context len_↑_|
|Teacher|14.086|0.442|0.412|2.72|12|1|
|Student|13.146|0.379|0.485|10.81|4|12|


Table 6: **Results of our distillation pipeline.** Our distilled model is significantly faster, able to inference at real-time 10.81 FPS with minor degradation in long-horizon rollouts and performance close to that of the teacher. The autoregressive causal prediction of the student model also provides finer granularity for interaction and better context awareness. 

|**Method**|**I**<br>PSNR_↑_|**n-lab Eva**<br>SSIM_↑_|**l**<br>LPIPS_↓_|**E**<br>PSNR_↑_|**goDex Ev**<br>SSIM_↑_|**al**<br>LPIPS_↓_|**Drea**<br>PSNR_↑_|**mDojo-HV**<br>SSIM_↑_|**Eval**<br>LPIPS_↓_|**Coun**<br>PSNR_↑_|**terfactua**<br>SSIM_↑_|**l Eval**<br>LPIPS_↓_|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|w/o pretrain|20.304|0.770|0.230|19.119|0.762|0.240|17.869|0.736|0.259|19.782|0.758|0.232|
|w/ pretrain|20.733|0.782|0.220|19.313|0.765|0.235|18.195|0.740|0.254|19.891|0.746|0.234|


Table 7: **Generalization ability after distillation.** Thanks to our strong pretraining, DreamDojo shows consistently better generalization than the baseline after distillation. 

Lastly, we ablate the choice of teacher model in Tab. 7, evaluating the distillation results of a teacher pretrained on human videos versus one without pretraining (Cosmos-Predict2.5). Across all four evaluation datasets, we observe that the former significantly outperforms the latter. This suggests that the benefits of generalization achieved through our human video pre-training are preserved after distillation, resulting in student models that also excel in unseen scenarios. 

### **4.7. Downstream Applications** 

**Policy evaluation.** One of the most straightforward application of world models is for policy evaluation (Li et al., 2025; Quevedo et al., 2025; Team et al., 2025; Tseng et al., 2025; Zbinden et al., 2025). In this work, we choose AgiBot fruit packing as a typical long-horizon task to verify whether DreamDojo can perform policy evaluation accurately. We train a single-view state-free variant of GR00T N1.5 (Bjorck et al., 2025) on the fruit packing dataset. We also post-train DreamDojo-2B on the same AgiBot dataset. Afterwards, we deploy different checkpoints from training to collect closed-loop rollouts in the real world. 

We set up 20 different scenes for the fruit packing tasks, covering various combinations of multiple fruits (pear, mango, banana, and starfruit) located in different places on the table. The success rate is determined by the number of fruits successfully picked up from the table and placed into the bag, with 5 fruits designated as 100% success. For each scene, we collect an approximately 80-second rollout in the real world and simulate the entire rollout with the post-trained DreamDojo-2B using the same initial frame. The generated rollouts are scored by human evaluators based on consistent criteria as the real world. The final success rate is averaged across all 20 scenes for both real-world and DreamDojo. 

Following WorldEval (Li et al., 2025) and SIMPLER (Li et al., 2024), we utilize Pearson correlation coefficient to quantify linear agreement between real-world and DreamDojo’s success rates and Mean Maximum Rank Violation (MMRV) to measure the rank consistency between these two. Fig. 5a shows that DreamDojo’s success rate has a strong linear correlation with real-world success rate (Pearson _𝑟_ =0.995) and maintains a highly consistent ranking (MMRV=0.003), indicating that DreamDojo is able to serve as a reliable simulator for policy evaluation. 

**Model-based planning.** Being able to simulate future outcomes conditioned on actions allows model-based planning that can strengthen and correct the policies at test time (Qi et al., 2025). In this paper, we adopt a simple algorithm for model-based planning. Specifically, similar to the policy evaluation experiment above, we setup 10 AgiBot fruit packing scenes as our touchstone. We ensemble 5 model checkpoints from training to generate action proposals that exhibit sufficient variance at inference time. These action proposals are sent 

13 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 5: **Downstream applications.** We show evidences that can be readily applied to benefit robot learning in policy evaluation without requiring real-world deployment, as well as for test-time model-based planning. 


Figure 6: **Live teleoperation.** We can teleoperate a virtual G1 robot using the PICO VR controller in real time. 

to DreamDojo to predict future video trajectories. To ensure execution efficiency, we batch all the action inputs and process them using the distilled DreamDojo-2B. Subsequently, the best proposal is selected by an external value model that takes a short video clip as input and is executed by the robot. The implementation details of the value model are provided in the Appendix. 

We experiment with two different groups of checkpoints. The results are presented in Fig. 5b. While our world model will introduce additional latency, it will also significantly improve the overall performance. With the help of DreamDojo, the policies can anticipate the outcomes of their predictions in advance and adaptively select the most promising mode for execution. For the policy group that has a larger performance variance, our approach improves the success rate by 17% over the best model checkpoint. Compared to uniformly sampling from all policy proposals, applying model-based planning with DreamDojo yields nearly a 2 _×_ increase in success rate. Another policy group, which mainly consists of converged checkpoints, yields a smaller yet still nearly a 2 _×_ increase in success rate. These results highlight the huge promise of DreamDojo for online policy steering. Based on the observation that ensembling models with greater variance has a higher probability of improvement, we anticipate that using policies from more diverse architectures (Cao et al., 2025) may further boost performance gains. 

**Live teleoperation.** We can also provide action conditions by connecting the teleoperation devices used for robot data collection to DreamDojo. To verify this, we deploy DreamDojo-2B on a local desktop equipped with an NVIDIA RTX 5090 GPU and connect a PICO VR controller to capture the upper-body action inputs for the G1 robot. As a result, we found that we could directly teleoperate the virtual robot at real-time speed. An example is shown in Fig. 6. For live teleoperation videos, please visit our website. 

14 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

## **5. Conclusion** 

In this paper, we introduce DreamDojo, a foundation world model that can simulate dexterous robotics tasks and generalize to unseen scenarios. Our model is pretrained on large-scale human datasets that encompass a wide variety of daily interactions. To further enhance knowledge transfer and action controllability, continuous latent actions are introduced as proxy actions for all videos. We further introduce a distillation pipeline that enables stable long-horizon interactions at real-time speed. Extensive evaluations underscore the significance of DreamDojo, demonstrating improved physics understanding and action following in out-of-distribution scenarios, a positive correlation with real-world evaluations, and real-time interactivity for live teleoperation and test-time policy steering. We hope our effort can pave the way for general-purpose robot world models. 

**Limitations.** While DreamDojo demonstrates significant improvements over the baseline, it is by no means perfect when simulating uncommon actions, such as slapping and fast waving. Additionally, when conducting policy evaluation, the absolute success rates in DreamDojo are often higher than their real counterparts, indicating a limitation in accurately generating nuanced failures. Future work should explore how to cover broader action distribution, _e.g_ ., using policy rollouts (Ho et al., 2025; Zhu et al., 2025). We also believe that there remains significant space for improving inference speed through engineering optimizations (Ball et al., 2025; Hong et al., 2025; Team et al., 2026; Ye et al., 2026). In addition, our model does not naturally support multi-view simulation, which is crucial for state-of-the-art policies (Bjorck et al., 2025; Black et al., 2024). Moreover, how to retain the pretrained knowledge as much as possible has not been studied in depth. Future work could explore other fine-tuning strategies (Hu et al., 2022; Yadav et al., 2025) to achieve better post-training performance on the target embodiment. 

15 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

## **A. Acknowledgement** 

We would like to thank Fernando Castaneda, Yunhao Ge, Sally Huynh, Yen-Chen Lin, Alec Nagal, Connor Pedersen, Shreya Raj, Yinzhen Xu, and the rest of the members of the GEAR Team for their invaluable support and feedback throughout this project. We also appreciate all the anonymous participants who contributed to the human evaluation. 

## **B. Related Work** 

**World model.** World models can simulate world transitions in response to actions, which have been proven critical for developing intelligent agents (Alonso et al., 2024; Ha and Schmidhuber, 2018; Hafner et al., 2025; Richens et al., 2025). Building upon advances in generative models, a surge of works have developed highquality video world models for simulating interactive games (Alonso et al., 2024; Ball et al., 2025; Guo et al., 2025; Hafner et al., 2025; Kanervisto et al., 2025; Kim et al., 2020; Parker-Holder et al., 2024; Sun et al., 2025; Ye et al., 2025; Yu et al., 2025) and autonomous driving (Bar et al., 2025; Hu et al., 2023; Kim et al., 2021; Kong et al., 2025; Russell et al., 2025; Yang et al., 2024). Motivated by successes in these domains, recent works have also introduced video generative models to simulate robot manipulation tasks (Guo et al., 2025; Jiang et al., 2025; Li et al., 2025; Wang et al., 2025; Wu et al., 2024; Zhu et al., 2025), which hold great promise for scalable policy evaluation (Li et al., 2025; Quevedo et al., 2025; Team et al., 2025; Tseng et al., 2025; Zbinden et al., 2025), reinforcement learning (Jiang et al., 2025; Li et al., 2025; Xiao et al., 2025; Yang et al., 2024; Zhang et al., 2025; Zhu et al., 2025), and policy steering (Assran et al., 2025; Du and Song, 2025; Jain et al., 2025; Qi et al., 2025; Wu et al., 2025; Zhou et al., 2025). However, existing models are typically trained and evaluated in in-distribution settings, leaving it unclear whether these models can truly facilitate planning in unseen scenarios. 

Another thread of research focuses on world model pretraining from internet-scale videos to improve downstream performance (Mendonca et al., 2023; Seo et al., 2022; Wu et al., 2023; Zhang et al., 2024). Our work is more related to works such as VAP (Wang et al., 2025) which utilizes 2D skeletons to unify action conditions from different robots and hands for joint training, as well as AdaWorld (Gao et al., 2025) and the follow-up works (Garrido et al., 2026; Wang et al., 2025) which propose pretraining a world model with latent actions to enhance transferability. Additionally, DexWM (Goswami et al., 2025) leverages human videos to help generalization to unseen dexterous manipulation skills. However, they primarily focus on tabletop datasets in laboratory setups and demonstrate inferior visual quality compared to recent advancements. In contrast, we introduce the first foundation world model for dexterous manipulation, which exhibits strong generalization in simulating diverse out-of-distribution manipulation skills across multiple embodiments. 

**Latent action.** Internet-scale video is an intriguing source for sparking emergent abilities (Wiedemer et al., 2025; Yang et al., 2024), but the unavailability of action labels could significantly hinder learning efficiency. To address this issue, latent actions have recently been proposed as a promising approach for learning from unlabeled videos (Bu et al., 2025; Jang et al., 2025; Schmidt and Jiang, 2024; Ye et al., 2025; Zhang et al., 2025). Besides serving as supervision for policy learning, latent actions can also be utilized as a control interface for world models (Bruce et al., 2024; Chen et al., 2024; Gao et al., 2025; Garrido et al., 2026; Wang et al., 2025). Several works have also demonstrated the effectiveness of continuous latent actions (Gao et al., 2025; Liang et al., 2025; Liu et al., 2025; Yang et al., 2025). Inspired by these explorations, we extract latent actions as a unified proxy for our foundation world model and investigate how this approach can promote robust generalization when interacting with unseen objects after adapting to new embodiments. 

**Autoregressive video generation.** Autoregressive video generation offers the finest granularity and flexibility for interaction (Weng et al., 2024), which is well-suited for action-conditioned world modeling (Bruce et al., 2024; Gao et al., 2025; Huang, 2025; Valevski et al., 2025). To accelerate inference speed, previous methods (Lin et al., 2025; Yin et al., 2025) distill the bidirectional model into an autoregressive student model that only 

16 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 7: **Web UI for human preference evaluation.** To intuitively compare physics correctness and action controls, we devise a web UI that can display the ground-truth video alongside two videos generated by two different models simultaneously. The order of the generated videos will be randomly switched to avoid any potential bias. 

requires fewer steps to generate videos of comparable quality. More recently, Self Forcing and its follow-ups (Cui et al., 2025; Huang et al., 2025; Liu et al., 2025; Shin et al., 2025; Zhang et al., 2025) further reduce longterm drift by mirroring the inference process during training. Building upon these techniques, we present a distillation pipeline that significantly boosts inference speed to real-time levels while ensuring the final model is aware of historical context. This makes our distilled model readily applicable to various downstream tasks, such as performing long-horizon dexterous teleoperation in real time. 

## **C. Human Preference Evaluation** 

Fig. 7 shows our web UI for our human preference evaluation, allowing the evaluators to assess physics correctness and action following intuitively. 

## **D. Additional Visualizations** 

### **D.1. Effects of Our Data Mixtures** 

In addition to the quantitative evaluations, we demonstrate the effectiveness of human data pretraining through visualizations. The samples in Fig. 8 verify that incorporating human data pretraining is essential for precise physics modeling of objects not captured by the robot dataset. 

### **D.2. Effects of Our Model Designs** 

We provide qualitative comparisons of the results from different model designs as outlined in Tab. 5. Both relative actions and chunked injection significantly enhance simulation quality, underscoring their importance for achieving precise action controllability. Additionally, the proposed temporal consistency loss further reinforces 

17 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 8: **Qualitative comparison of human data pretraining effects.** Through pretraining on diverse human interaction data, DreamDojo acquires a generalizable understanding of general physics, resulting in more realistic simulation for objects that are unseen in the target robot dataset. 

the modeling quality of objects. 

### **D.3. Benefits of Distillation** 

We compare the 1-minute videos generated by the teacher model and the student model in Fig. 10. DreamDojo can continuously predict long-horizon rollouts in real time with strong stability and action following. 

In Fig. 11, we also visualize representative samples that illustrate the superior consistency of the student model. The distilled DreamDojo can recover objects from occlusions by modeling a short context, whereas the teacher model is unable to achieve this due to its single-frame conditioning. 

### **D.4. DreamDojo-HV Samples** 

To assist a better understanding of the DreamDojo-HV dataset, we visualize more data samples in Fig. 12, highlighting its extensive coverage of interaction types and scenarios. 

18 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 9: **Qualitative comparison of our design choices.** Applying all our techniques results in the best capabilities for object modeling and action following. 

19 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

### **D.5. PSNR Curves in Post-Training** 

We visualize how the PSNR scores will evolve during post-training. Fig. 13 shows that pretraining with latent actions can reach a much higher upper bound than action-free pretraining and without pretraining, especially on EgoDex Eval. 

### **D.6. Value Model** 

To automatically judge the value of the predicted futures, we train an external model based on the DINOv2 (Oquab et al., 2023) architecture. Our value model takes a video clip consisting of 4 frames as input. The DINOv2 backbone is frozen and independently extracts image features from each frame. The features from all frames are then processed by a value prediction module with global attention. The value prediction module is trained to estimate the number of time steps remaining until each subtask boundary, which is defined as the keyframe between consecutive subtask language annotations. The ground-truth value is normalized by the maximum subtask interval in the dataset. For each generated video, the value estimation is performed as a sliding window with a stride of 1. The final value of the current video is defined as the average of all clips from the start to the dip before the estimated value increases. The action proposal with the lowest value ( _i.e_ ., closest to subtask completion) will be selected for real-world execution. A visualization of the accuracy of our value model is shown in Fig. 14. 

20 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 10: **Long-horizon rollouts for 1 minute.** Note that the teacher model generates videos in a chunk-wise manner and operates at a speed (2.72 FPS) that is 4 _×_ slower than that of the student model (10.81 FPS). 

21 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 11: **The advantage of student context.** The student model exhibits better consistency in handling occlusions and camera shifts, while the teacher model has no way to ensure that due to the missing context. 

22 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 12: **Diversity of DreamDojo-HV.** We visualize more samples from the curated DreamDojo-HV dataset, which encompasses extremely diverse actions and tool-using scenarios. 

23 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 


Figure 13: **Post-training PSNR curves using different action conditioning.** Latent action conditioning can achieve comparable performance as high-quality action labels obtained using extra devices. On EgoDex Eval, our approach can also reach a much higher upper bound compared to action-free pretraining and without pretraining. 


Figure 14: **Value model estimation.** We visualize the estimated value and the ground-truth value of two representative episodes. Our value model reliably estimates the number of steps remaining to complete the current subtask. 

24 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

## **References** 

- [1] Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Aaron Blakeman, Tiffany Cai, Jiaxin Cao, Tianshi Cao, Elizabeth Cha, Yu-Wei Chao, et al. World Simulation with Video Foundation Models for Physical AI. _arXiv preprint arXiv:2511.00062_ , 2025. 2, 3, 5, 9 

- [2] Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storkey, Tim Pearce, and François Fleuret. Diffusion for World Modeling: Visual Details Matter in Atari. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 16 

- [3] Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, et al. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. _arXiv preprint arXiv:2506.09985_ , 2025. 16 

- [4] Yutong Bai, Danny Tran, Amir Bar, Yann LeCun, Trevor Darrell, and Jitendra Malik. Whole-Body Conditioned Egocentric Video Prediction. _arXiv preprint arXiv:2506.21552_ , 2025. 

- [5] Philip Ball, Jakob Bauer, Frank Belletti, Bethanie Brownfield, Ariel Ephrat, Shlomi Fruchter, Agrim Gupta, Kristian Holsheimer, Aleksander Holynski, Jiri Hron, et al. Genie 3: A New Frontier for World Models, 2025. URL `https://deepmind.google/discover/blog/ genie-3-a-new-frontier-for-world-models/` . 2, 15, 16 

- [6] Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation World Models. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 16 

- [7] Hongzhe Bi, Lingxuan Wu, Tianwei Lin, Hengkai Tan, Zhizhong Su, Hang Su, and Jun Zhu. H-RDT: Human Manipulation Enhanced Bimanual Robotic Manipulation. In _Proc. of the Conf. on Artificial Intelligence (AAAI)_ , 2025. 4 

- [8] Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. _arXiv preprint arXiv:2503.14734_ , 2025. 13, 15 

- [9] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _𝜋_ 0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ , 2024. 15 

- [10] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. RT-1: Robotics Transformer for Real-World Control at Scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- [11] Jake Bruce, Michael Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative Interactive Environments. In _Proc. of the International Conf. on Machine learning (ICML)_ , 2024. 6, 7, 9, 16 

- [12] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems. _arXiv preprint arXiv:2503.06669_ , 2025. 2 

- [13] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. UniVLA: Learning to Act Anywhere with Task-centric Latent Actions. In _Proc. Robotics: Science and Systems (RSS)_ , 2025. 16 

- [14] Jiahang Cao, Yize Huang, Hanzhong Guo, Rui Zhang, Mu Nan, Weijian Mai, Jiaxu Wang, Hao Cheng, Jingkai Sun, Gang Han, et al. Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-Time Distribution-Level Composition. _arXiv preprint arXiv:2510.01068_ , 2025. 14 

25 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [15] Boyuan Chen, Tianyuan Zhang, Haoran Geng, Kiwhan Song, Caiyi Zhang, Peihao Li, William Freeman, Jitendra Malik, Pieter Abbeel, Russ Tedrake, et al. Large Video Planner Enables Generalizable Robot Control. _arXiv preprint arXiv:2512.15840_ , 2025. 4 

- [16] Xiaoyu Chen, Junliang Guo, Tianyu He, Chuheng Zhang, Pushi Zhang, Derek Cathera Yang, Li Zhao, and Jiang Bian. IGOR: Image-GOal Representations are the Atomic Control Units for Foundation Models in Embodied AI. _arXiv preprint arXiv:2411.00785_ , 2024. 16 

- [17] Xiaoyu Chen, Hangxing Wei, Pushi Zhang, Chuheng Zhang, Kaixin Wang, Yanjiang Guo, Rushuai Yang, Yucen Wang, Xinquan Xiao, Li Zhao, et al. villa-X: Enhancing Latent Action Modeling in Vision-LanguageAction Models. _arXiv preprint arXiv:2507.23682_ , 2025. 4 

- [18] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 10 

- [19] Justin Cui, Jie Wu, Ming Li, Tao Yang, Xiaojie Li, Rui Wang, Andrew Bai, Yuanhao Ban, and ChoJui Hsieh. Self-Forcing++: Towards Minute-Scale High-Quality Video Generation. _arXiv preprint arXiv:2510.02283_ , 2025. 17 

- [20] Sudeep Dasari, Frederik Ebert, Stephen Tian, Suraj Nair, Bernadette Bucher, Karl Schmeckpeper, Siddharth Singh, Sergey Levine, and Chelsea Finn. RoboNet: Large-Scale Multi-Robot Learning. _arXiv preprint arXiv:1910.11215_ , 2019. 

- [21] Maximilian Du and Shuran Song. DynaGuide: Steering Diffusion Polices with Active Dynamic Guidance. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 16 

- [22] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 7, 10 

- [23] Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, and Chuang Gan. AdaWorld: Learning Adaptable World Models with Latent Actions. In _Proc. of the International Conf. on Machine learning (ICML)_ , 2025. 2, 6, 7, 16 

- [24] Quentin Garrido, Tushar Nagarajan, Basile Terver, Nicolas Ballas, Yann LeCun, and Michael Rabbat. Learning Latent Action World Models In The Wild. _arXiv preprint arXiv:2601.05230_ , 2026. 16 

- [25] Raktim Gautam Goswami, Amir Bar, David Fan, Tsung-Yen Yang, Gaoyue Zhou, Prashanth Krishnamurthy, Michael Rabbat, Farshad Khorrami, and Yann LeCun. World Models Can Leverage Human Videos for Dexterous Manipulation. _arXiv preprint arXiv:2512.13644_ , 2025. 16 

- [26] Junliang Guo, Yang Ye, Tianyu He, Haoyu Wu, Yushu Jiang, Tim Pearce, and Jiang Bian. MineWorld: A Real-Time and Open-Source Interactive World Model on Minecraft. _arXiv preprint arXiv:2504.08388_ , 2025. 16 

- [27] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-World: A Controllable Generative World Model for Robot Manipulation. _arXiv preprint arXiv:2510.10125_ , 2025. 6, 16 

- [28] David Ha and Jürgen Schmidhuber. Recurrent World Models Facilitate Policy Evolution. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2018. 16 

- [29] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering Diverse Domains through World Models. _Nature_ , 2025. 16 

26 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [30] Danijar Hafner, Wilson Yan, and Timothy Lillicrap. Training Agents Inside of Scalable World Models. _arXiv preprint arXiv:2509.24527_ , 2025. 16 

- [31] Daniel Ho, Jack Monas, Juntao Ren, and Christina Yu. 1X World Model: Evaluating Bits, not Atoms, 2025. URL `https://www.1x.tech/1x-world-model.pdf` . 15 

- [32] Jonathan Ho and Tim Salimans. Classifier-Free Diffusion Guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 10 

- [33] Yicong Hong, Yiqun Mei, Chongjian Ge, Yiran Xu, Yang Zhou, Sai Bi, Yannick Hold-Geoffroy, Mike Roberts, Matthew Fisher, Eli Shechtman, et al. RELIC: Interactive Video World Model with Long-Horizon Memory. _arXiv preprint arXiv:2512.04040_ , 2025. 15 

- [34] Ryan Hoque, Peide Huang, David Yoon, Mouli Sivapurapu, and Jian Zhang. EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video. _arXiv preprint arXiv:2505.11709_ , 2025. 5 

- [35] Alain Hore and Djemel Ziou. Image Quality Metrics: PSNR vs. SSIM. In _Proc. of the International Conf. on Pattern Recognition (ICPR)_ , 2010. 10 

- [36] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. GAIA-1: A Generative World Model for Autonomous Driving. _arXiv preprint arXiv:2309.17080_ , 2023. 16 

- [37] Edward Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. LoRA: Low-Rank Adaptation of Large Language Models. In _Proc. of the International Conf. on Learning Representations (ICLR)_ , 2022. 15 

- [38] Yafei Hu, Quanting Xie, Vidhi Jain, Jonathan Francis, Jay Patrikar, Nikhil Keetha, Seungchan Kim, Yaqi Xie, Tianyi Zhang, Hao-Shu Fang, et al. Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis. _arXiv preprint arXiv:2312.08782_ , 2023. 2 

- [39] Siqiao Huang, Jialong Wu, Qixing Zhou, Shangchen Miao, and Mingsheng Long. Vid2World: Crafting Video Diffusion Models to Interactive World Models. _arXiv preprint arXiv:2505.14357_ , 2025. 5, 6 

- [40] Xun Huang. Towards Video World Models, 2025. URL `https://www.xunhuang.me/blogs/world_ model.html` . 8, 16 

- [41] Xun Huang, Zhengqi Li, Guande He, Mingyuan Zhou, and Eli Shechtman. Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 2, 8, 17 

- [42] Arnav Kumar Jain, Vibhakar Mohta, Subin Kim, Atiksh Bhardwaj, Juntao Ren, Yunhai Feng, Sanjiban Choudhury, and Gokul Swamy. A Smooth Sea Never Made a Skilled SAILOR: Robust Imitation via Learning to Search. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 16 

- [43] Joel Jang, Seonghyeon Ye, Zongyu Lin, Jiannan Xiang, Johan Bjorck, Yu Fang, Fengyuan Hu, Spencer Huang, Kaushil Kundalia, Yen-Chen Lin, et al. DreamGen: Unlocking Generalization in Robot Learning through Video World Models. In _Proc. Conf. on Robot Learning (CoRL)_ , 2025. 16 

- [44] Yuxin Jiang, Shengcong Chen, Siyuan Huang, Liliang Chen, Pengfei Zhou, Yue Liao, Xindong He, Chiming Liu, Hongsheng Li, Maoqing Yao, et al. EnerVerse-AC: Envisioning Embodied Environments with Action Condition. _arXiv preprint arXiv:2505.09723_ , 2025. 16 

- [45] Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Dongbin Zhao. World4RL: Diffusion World Models for Policy Refinement with Reinforcement Learning for Robotic Manipulation. _arXiv preprint arXiv:2509.19080_ , 2025. 16 

27 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [46] Anssi Kanervisto, Dave Bignell, Linda Yilin Wen, Martin Grayson, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Tabish Rashid, Tim Pearce, Yuhan Cao, et al. World and Human Action Models Towards Gameplay Ideation. _Nature_ , 2025. 16 

- [47] Simar Kareer, Karl Pertsch, James Darpinian, Judy Hoffman, Danfei Xu, Sergey Levine, Chelsea Finn, and Suraj Nair. Emergence of Human to Robot Transfer in Vision-Language-Action Models. _arXiv preprint arXiv:2512.22414_ , 2025. 4 

- [48] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. DROID: A LargeScale In-The-Wild Robot Manipulation Dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 2 

- [49] Seung Wook Kim, Yuhao Zhou, Jonah Philion, Antonio Torralba, and Sanja Fidler. Learning to Simulate Dynamic Environments with GameGAN. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2020. 16 

- [50] Seung Wook Kim, Jonah Philion, Antonio Torralba, and Sanja Fidler. DriveGAN: Towards a Controllable High-Quality Neural Simulation. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2021. 16 

- [51] Diederik Kingma and Max Welling. Auto-Encoding Variational Bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 7 

- [52] Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu, Wei Yin, Xiaotao Hu, Mingkai Jia, et al. 3D and 4D World Modeling: A Survey. _arXiv preprint arXiv:2509.07996_ , 2025. 16 

- [53] Yann LeCun. A Path Towards Autonomous Machine Intelligence. _Open Review_ , 2022. 2 

- [54] Hengtao Li, Pengxiang Ding, Runze Suo, Yihao Wang, Zirui Ge, Dongyuan Zang, Kexian Yu, Mingyang Sun, Hongyin Zhang, Donglin Wang, et al. VLA-RFT: Vision-Language-Action Reinforcement Fine-tuning with Verified Rewards in World Simulators. _arXiv preprint arXiv:2510.00406_ , 2025. 16 

- [55] Qixiu Li, Yu Deng, Yaobo Liang, Lin Luo, Lei Zhou, Chengtang Yao, Lingqi Zeng, Zhiyuan Feng, Huizhi Liang, Sicheng Xu, et al. Scalable Vision-Language-Action Model Pretraining for Robotic Manipulation with Real-Life Human Activity Videos. _arXiv preprint arXiv:2510.21571_ , 2025. 4 

- [56] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified Video Action Model. In _Proc. Robotics: Science and Systems (RSS)_ , 2025. 16 

- [57] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating Real-World Robot Manipulation Policies in Simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 13 

- [58] Yaxuan Li, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. WorldEval: World Model as Real-World Robot Policies Evaluator. _arXiv preprint arXiv:2505.19017_ , 2025. 13, 16 

- [59] Anthony Liang, Pavel Czempin, Matthew Hong, Yutai Zhou, Erdem Biyik, and Stephen Tu. CLAM: Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations. _arXiv preprint arXiv:2505.04999_ , 2025. 16 

- [60] Shanchuan Lin, Ceyuan Yang, Hao He, Jianwen Jiang, Yuxi Ren, Xin Xia, Yang Zhao, Xuefeng Xiao, and Lu Jiang. Autoregressive Adversarial Post-Training for Real-Time Interactive Video Generation. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 16 

28 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [61] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow Matching for Generative Modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 3 

- [62] Kunhao Liu, Wenbo Hu, Jiale Xu, Ying Shan, and Shijian Lu. Rolling Forcing: Autoregressive Long Video Diffusion in Real Time. _arXiv preprint arXiv:2509.25161_ , 2025. 17 

- [63] Mingyu Liu, Jiuhe Shu, Hui Chen, Zeju Li, Canyu Zhao, Jiange Yang, Shenyuan Gao, Hao Chen, and Chunhua Shen. StaMo: Unsupervised Learning of Generalizable Robot Motion from Compact State Representation. _arXiv preprint arXiv:2510.05057_ , 2025. 16 

- [64] Vincent Liu, Ademi Adeniji, Haotian Zhan, Siddhant Haldar, Raunaq Bhirangi, Pieter Abbeel, and Lerrel Pinto. EgoZero: Robot Learning from Smart Glasses. _arXiv preprint arXiv:2505.20290_ , 2025. 4 

- [65] Ilya Loshchilov and Frank Hutter. Decoupled Weight Decay Regularization. In _Proc. of the International Conf. on Learning Representations (ICLR)_ , 2019. 9 

- [66] Hao Luo, Yicheng Feng, Wanpeng Zhang, Sipeng Zheng, Ye Wang, Haoqi Yuan, Jiazheng Liu, Chaoyi Xu, Qin Jin, and Zongqing Lu. Being-H0: Vision-Language-Action Pretraining from Large-Scale Human Videos. _arXiv preprint arXiv:2507.15597_ , 2025. 4 

- [67] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive Language: Talking to Robots in Real Time. _IEEE Robotics and Automation Letters (RA-L)_ , 2023. 

- [68] Lingni Ma, Yuting Ye, Fangzhou Hong, Vladimir Guzov, Yifeng Jiang, Rowan Postyeni, Luis Pesqueira, Alexander Gamino, Vijay Baiyya, Hyo Jin Kim, et al. Nymeria: A Massive Collection of Multimodal Egocentric Daily Motion in the Wild. In _Proc. of the European Conf. on Computer Vision (ECCV)_ , 2024. 

- [69] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured World Models from Human Videos. In _Proc. Robotics: Science and Systems (RSS)_ , 2023. 16 

- [70] Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. DINOv2: Learning Robust Visual Features without Supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 20 

- [71] Enrico Pallotta, Sina Mokhtarzadeh Azar, Lars Doorenbos, Serdar Ozsoy, Umar Iqbal, and Juergen Gall. EgoControl: Controllable Egocentric Video Generation via 3D Full-Body Poses. _arXiv preprint arXiv:2511.18173_ , 2025. 

- [72] Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, et al. Genie 2: A Large-Scale Foundation World Model, 2024. URL `https://deepmind.google/discover/blog/ genie-2-a-large-scale-foundation-world-model/` . 5, 16 

- [73] Georgios Pavlakos, Dandan Shan, Ilija Radosavovic, Angjoo Kanazawa, David Fouhey, and Jitendra Malik. Reconstructing Hands in 3D with Transformers. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 6, 11 

- [74] William Peebles and Saining Xie. Scalable Diffusion Models with Transformers. In _Proc. of the IEEE International Conf. on Computer Vision (ICCV)_ , 2023. 3 

- [75] Han Qi, Haocheng Yin, Aris Zhu, Yilun Du, and Heng Yang. Strengthening Generative Robot Policies through Predictive World Modeling. _arXiv preprint arXiv:2502.00622_ , 2025. 13, 16 

29 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [76] Ri-Zhao Qiu, Shiqi Yang, Xuxin Cheng, Chaitanya Chawla, Jialong Li, Tairan He, Ge Yan, David Yoon, Ryan Hoque, Lars Paulsen, et al. Humanoid Policy ˜ Human Policy. In _Proc. Conf. on Robot Learning (CoRL)_ , 2025. 4 

- [77] Julian Quevedo, Percy Liang, and Sherry Yang. Evaluating Robot Policies in a World Model. _arXiv preprint arXiv:2506.00613_ , 2025. 13, 16 

- [78] Jonathan Richens, Tom Everitt, and David Abel. General Agents Need World Models. In _Proc. of the International Conf. on Machine learning (ICML)_ , 2025. 2, 16 

- [79] Javier Romero, Dimitrios Tzionas, and Michael J Black. Embodied Hands: Modeling and Capturing Hands and Bodies Together. _arXiv preprint arXiv:2201.02610_ , 2022. 11 

- [80] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. GAIA-2: A Controllable Multi-View Generative World Model for Autonomous Driving. _arXiv preprint arXiv:2503.20523_ , 2025. 2, 16 

- [81] Dominik Schmidt and Minqi Jiang. Learning to Act without Actions. In _Proc. of the International Conf. on Learning Representations (ICLR)_ , 2024. 16 

- [82] Younggyo Seo, Kimin Lee, Stephen James, and Pieter Abbeel. Reinforcement Learning with Action-Free Pre-Training from Videos. In _Proc. of the International Conf. on Machine learning (ICML)_ , 2022. 16 

- [83] Joonghyuk Shin, Zhengqi Li, Richard Zhang, Jun-Yan Zhu, Jaesik Park, Eli Shechtman, and Xun Huang. MotionStream: Real-Time Video Generation with Interactive Motion Controls. _arXiv preprint arXiv:2511.01266_ , 2025. 17 

- [84] Wenqiang Sun, Fangyun Wei, Jinjing Zhao, Xi Chen, Zilong Chen, Hongyang Zhang, Jun Zhang, and Yan Lu. From Virtual Games to Real-World Play. _arXiv preprint arXiv:2506.18901_ , 2025. 16 

- [85] Wenqiang Sun, Haiyu Zhang, Haoyuan Wang, Junta Wu, Zehan Wang, Zhenwei Wang, Yunhong Wang, Jun Zhang, Tengfei Wang, and Chunchao Guo. WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling. _arXiv preprint arXiv:2512.14614_ , 2025. 2 

- [86] Richard S Sutton. Dyna, an Integrated Architecture for Learning, Planning, and Reacting. _ACM Sigart Bulletin_ , 1991. 2 

- [87] Gemini Robotics Team, Coline Devin, Yilun Du, Debidatta Dwibedi, Ruiqi Gao, Abhishek Jindal, Thomas Kipf, Sean Kirmani, Fangchen Liu, Anirudha Majumdar, et al. Evaluating Gemini Robotics Policies in a Veo World Simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 4, 13, 16 

- [88] Robbyant Team, Zelin Gao, Qiuyu Wang, Yanhong Zeng, Jiapeng Zhu, Ka Leong Cheng, Yixuan Li, Hanlin Wang, Yinghao Xu, Shuailei Ma, et al. Advancing Open-Source World Models. _arXiv preprint arXiv:2601.20540_ , 2026. 15 

- [89] Wei-Cheng Tseng, Jinwei Gu, Qinsheng Zhang, Hanzi Mao, Ming-Yu Liu, Florian Shkurti, and Lin Yen-Chen. Scalable Policy Evaluation with Video World Models. _arXiv preprint arXiv:2511.11520_ , 2025. 13, 16 

- [90] Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion Models are Real-Time Game Engines. In _Proc. of the International Conf. on Learning Representations (ICLR)_ , 2025. 16 

- [91] Homer Rich Walke, Kevin Black, Tony Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. BridgeData V2: A Dataset for Robot Learning at Scale. In _Proc. Conf. on Robot Learning (CoRL)_ , 2023. 

30 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [92] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, et al. Wan: Open and Advanced Large-Scale Video Generative Models. _arXiv preprint arXiv:2503.20314_ , 2025. 2, 3, 5, 6, 10 

- [93] Chen Wang, Haochen Shi, Weizhuo Wang, Ruohan Zhang, Li Fei-Fei, and C Karen Liu. DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation. In _Proc. Robotics: Science and Systems (RSS)_ , 2024. 4 

- [94] Lirui Wang, Kevin Zhao, Chaoqi Liu, and Xinlei Chen. Learning Real-World Action-Video Dynamics with Heterogeneous Masked Autoregression. _arXiv preprint arXiv:2502.04296_ , 2025. 16 

- [95] Xiang Wang, Shiwei Zhang, Hangjie Yuan, Zhiwu Qing, Biao Gong, Yingya Zhang, Yujun Shen, Changxin Gao, and Nong Sang. A Recipe for Scaling up Text-to-Video Generation with Text-free Videos. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 7 

- [96] Yuang Wang, Chao Wen, Haoyu Guo, Sida Peng, Minghan Qin, Hujun Bao, Xiaowei Zhou, and Ruizhen Hu. Precise Action-to-Video Generation Through Visual Action Prompts. In _Proc. of the IEEE International Conf. on Computer Vision (ICCV)_ , 2025. 16 

- [97] Yucen Wang, Fengming Zhang, De-Chuan Zhan, Li Zhao, Kaixin Wang, and Jiang Bian. Co-Evolving Latent Action World Models. _arXiv preprint arXiv:2510.26433_ , 2025. 16 

- [98] Wenming Weng, Ruoyu Feng, Yanhui Wang, Qi Dai, Chunyu Wang, Dacheng Yin, Zhiyuan Zhao, Kai Qiu, Jianmin Bao, Yuhui Yuan, et al. ART-V: Auto-Regressive Text-to-Video Generation with Diffusion Models. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 16 

- [99] Thaddäus Wiedemer, Yuxuan Li, Paul Vicol, Shixiang Shane Gu, Nick Matarese, Kevin Swersky, Been Kim, Priyank Jaini, and Robert Geirhos. Video Models are Zero-Shot Learners and Reasoners. _arXiv preprint arXiv:2509.20328_ , 2025. 16 

- [100] Jialong Wu, Haoyu Ma, Chaoyi Deng, and Mingsheng Long. Pre-Training Contextualized World Models with In-the-Wild Videos for Reinforcement Learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2023. 16 

- [101] Jialong Wu, Shaofeng Yin, Ningya Feng, Xu He, Dong Li, Jianye Hao, and Mingsheng Long. iVideoGPT: Interactive VideoGPTs are Scalable World Models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 16 

- [102] Yilin Wu, Ran Tian, Gokul Swamy, and Andrea Bajcsy. From Foresight to Forethought: VLM-in-the-Loop Policy Steering via Latent Alignment. In _Proc. Robotics: Science and Systems (RSS)_ , 2025. 16 

- [103] Junjin Xiao, Yandan Yang, Xinyuan Chang, Ronghan Chen, Feng Xiong, Mu Xu, Wei-Shi Zheng, and Qing Zhang. World-Env: Leveraging World Model as a Virtual Environment for VLA Post-Training. _arXiv preprint arXiv:2509.24948_ , 2025. 16 

- [104] Jingqiao Xiu, Fangzhou Hong, Yicong Li, Mengze Li, Wentao Wang, Sirui Han, Liang Pan, and Ziwei Liu. EgoTwin: Dreaming Body and View in First Person. _arXiv preprint arXiv:2508.13013_ , 2025. 

- [105] Yajat Yadav, Zhiyuan Zhou, Andrew Wagenmaker, Karl Pertsch, and Sergey Levine. Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging. _arXiv preprint arXiv:2512.08333_ , 2025. 15 

- [106] Jiange Yang, Yansong Shi, Haoyi Zhu, Mingyu Liu, Kaijing Ma, Yating Wang, Gangshan Wu, Tong He, and Limin Wang. CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning. _arXiv preprint arXiv:2505.17006_ , 2025. 16 

31 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [107] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping Luo, et al. Generalized Predictive Model for Autonomous Driving. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 16 

- [108] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. ReSim: Reliable World Simulation for Autonomous Driving. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 5, 7 

- [109] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning Interactive Real-World Simulators. In _Proc. of the International Conf. on Learning Representations (ICLR)_ , 2024. 5, 16 

- [110] Ruihan Yang, Qinxi Yu, Yecheng Wu, Rui Yan, Borui Li, An-Chieh Cheng, Xueyan Zou, Yunhao Fang, Xuxin Cheng, Ri-Zhao Qiu, et al. EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos. _arXiv preprint arXiv:2507.12440_ , 2025. 4 

- [111] Sherry Yang, Jacob Walker, Jack Parker-Holder, Yilun Du, Jake Bruce, Andre Barreto, Pieter Abbeel, and Dale Schuurmans. Video as the New Language for Real-World Decision Making. In _Proc. of the International Conf. on Machine learning (ICML)_ , 2024. 16 

- [112] Deheng Ye, Fangyun Zhou, Jiacheng Lv, Jianqi Ma, Jun Zhang, Junyan Lv, Junyou Li, Minwen Deng, Mingyu Yang, Qiang Fu, et al. Yan: Foundational Interactive Video Generation. _arXiv preprint arXiv:2508.08601_ , 2025. 16 

- [113] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent Action Pretraining from Videos. In _Proc. of the International Conf. on Learning Representations (ICLR)_ , 2025. 4, 6, 16 

- [114] Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, et al. DreamZero: World Action Models Are Zero-Shot Policies, 2026. URL `https://dreamzero0.github.io/` . 15 

- [115] Tianwei Yin, Michaël Gharbi, Taesung Park, Richard Zhang, Eli Shechtman, Fredo Durand, and Bill Freeman. Improved Distribution Matching Distillation for Fast Image Synthesis. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 

- [116] Tianwei Yin, Michaël Gharbi, Richard Zhang, Eli Shechtman, Fredo Durand, William Freeman, and Taesung Park. One-Step Diffusion with Distribution Matching Distillation. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 8 

- [117] Tianwei Yin, Qiang Zhang, Richard Zhang, William Freeman, Fredo Durand, Eli Shechtman, and Xun Huang. From Slow Bidirectional to Fast Causal Video Generators. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 10, 16 

- [118] Jiwen Yu, Yiran Qin, Haoxuan Che, Quande Liu, Xintao Wang, Pengfei Wan, Di Zhang, Kun Gai, Hao Chen, and Xihui Liu. A Survey of Interactive Generative Video. _arXiv preprint arXiv:2504.21853_ , 2025. 16 

- [119] Lukas Zbinden, Nigel Nelson, Juo-Tung Chen, Xinhao Chen, Ji Woong, Mahdi Azizian, Axel Krieger, Sean Huver, et al. Cosmos-Surg-dVRK: World Foundation Model-based Automated Online Evaluation of Surgical Robot Policy Learning. _arXiv preprint arXiv:2510.16240_ , 2025. 13, 16 

- [120] Chuheng Zhang, Tim Pearce, Pushi Zhang, Kaixin Wang, Xiaoyu Chen, Wei Shen, Li Zhao, and Jiang Bian. What Do Latent Action Models Actually Learn? In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 16 

32 

DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos 

- [121] Jiahui Zhang, Ze Huang, Chun Gu, Zipei Ma, and Li Zhang. Reinforcing Action Policies by Prophesying. _arXiv preprint arXiv:2511.20633_ , 2025. 4, 16 

- [122] Ke Zhang, Yiqun Mei, Jiacong Xu, and Vishal M Patel. Endless World: Real-Time 3D-Aware Long Video Generation. _arXiv preprint arXiv:2512.12430_ , 2025. 17 

- [123] Lixuan Zhang, Meina Kan, Shiguang Shan, and Xilin Chen. PreLAR: World Model Pre-Training with Learnable Action Representation. In _Proc. of the European Conf. on Computer Vision (ECCV)_ , 2024. 16 

- [124] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding Conditional Control to Text-to-Image Diffusion Models. In _Proc. of the IEEE International Conf. on Computer Vision (ICCV)_ , 2023. 7 

- [125] Richard Zhang, Phillip Isola, Alexei Efros, Eli Shechtman, and Oliver Wang. The Unreasonable Effectiveness of Deep Features as a Perceptual Metric. In _Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR)_ , 2018. 10 

- [126] Ruijie Zheng, Jing Wang, Scott Reed, Johan Bjorck, Yu Fang, Fengyuan Hu, Joel Jang, Kaushil Kundalia, Zongyu Lin, Loic Magne, et al. FLARE: Robot Learning with Implicit World Modeling. In _Proc. Conf. on Robot Learning (CoRL)_ , 2025. 4 

- [127] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. DINO-WM: World Models on Pre-Trained Visual Features Enable Zero-Shot Planning. In _Proc. of the International Conf. on Machine learning (ICML)_ , 2025. 16 

- [128] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets. In _Proc. Robotics: Science and Systems (RSS)_ , 2025. 16 

- [129] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. IRASim: A Fine-Grained World Model for Robot Manipulation. In _Proc. of the IEEE International Conf. on Computer Vision (ICCV)_ , 2025. 6 

- [130] Fangqi Zhu, Zhengyang Yan, Zicong Hong, Quanxin Shou, Xiao Ma, and Song Guo. WMPO: World Model-based Policy Optimization for Vision-Language-Action Models. _arXiv preprint arXiv:2511.09515_ , 2025. 15, 16 

33 

