---
title: "DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos"
date: "2026"
venue: "ICML 2026"
url: https://proceedings.mlr.press/v306/gao26q.html
pdf: https://raw.githubusercontent.com/mlresearch/v306/main/assets/gao26q/gao26q.pdf
converter: pymupdf4llm
---

> **[PDF を開く](https://raw.githubusercontent.com/mlresearch/v306/main/assets/gao26q/gao26q.pdf)** / [論文ページ](https://proceedings.mlr.press/v306/gao26q.html)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

**Shenyuan Gao**<sup>* 1 2</sup> **William Liang**<sup>* 1 3</sup> **Kaiyuan Zheng**<sup>1 4</sup> **Ayaan Malik**<sup>1 5</sup> **Seonghyeon Ye**<sup>1 6</sup> **Sihyun Yu**<sup>6</sup> **Wei-Cheng Tseng**<sup>1 7</sup> **Yuzhu Dong**<sup>1</sup> **Kaichun Mo**<sup>1</sup> **Chen-Hsuan Lin**<sup>1</sup> **Jiannan Xiang**<sup>8</sup> **Yuqi Xie**<sup>1</sup> **Ruijie Zheng**<sup>1</sup> **Dantong Niu**<sup>1 3</sup> **Pooya Jannaty**<sup>1</sup> **Jinwei Gu**<sup>1</sup> **Jun Zhang**<sup>2</sup> **Jitendra Malik**<sup>3</sup> **Pieter Abbeel**<sup>3</sup> **Ming-Yu Liu**<sup>1</sup> **Yuke Zhu**<sup>1 9</sup> **Joel Jang**<sup>1</sup> **Linxi Fan**<sup>1</sup> 

dreamdojo-world.github.io 

## **Abstract** 

## **1. Introduction** 

Being able to simulate the outcomes of actions in varied environments will revolutionize the development of generalist agents at scale. However, modeling these world dynamics, especially for dexterous robotics tasks, poses significant challenges due to limited data coverage and scarce action labels. As an endeavor towards this end, we introduce DreamDojo, a generalist world model that learns diverse interactions and dexterous controls from 44k hours of egocentric human videos. Our data mixture represents the largest video dataset to date for world model pretraining, spanning a wide range of daily scenarios with diverse objects and skills. To address the scarcity of action labels, we introduce continuous latent actions as unified proxy actions, enhancing interaction knowledge transfer from unlabeled videos. After post-training on small-scale target robot data, DreamDojo demonstrates a strong understanding of physics and precise action controllability. We also devise a distillation pipeline that accelerates DreamDojo to a real-time speed of 10.93 FPS and further improves consistency to the context. Our work enables several important applications based on generative world models, including live teleoperation, policy evaluation, and model-based planning. Systematic evaluation on multiple challenging out-of-distribution (OOD) benchmarks verifies the significance of our method for simulating open-world, contact-rich tasks, paving the way for general-purpose robot world models. 

> *Equal contribution 1NVIDIA 2HKUST 3UC Berkeley<sup>4</sup> University of Washington<sup>5</sup> Stanford University<sup>6</sup> KAIST 7University of Toronto 8UC San Diego 9UT Austin. Correspondence to: Shenyuan Gao _<_ sygao@connect.ust.hk _>_ . 

_Proceedings of the 43_<sup>_rd_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

World models, which predict futures based on actions, have emerged as a pivotal component in the development of generalist robots (Sutton, 1991; LeCun, 2022; Hu et al., 2023b; Richens et al., 2025). Recent advances in video generation (Ali et al., 2025; Wan et al., 2025) have ushered in a new era of video world models, in which future states are represented as video frames (Parker-Holder & Fruchter, 2025; Russell et al., 2025; Sun et al., 2025b). However, current world models primarily plateau at discrete controls, while the high-dimensional action spaces for contact-rich robot tasks have yet to make similar progress. Unlike game and driving domains, robot data often has limited coverage due to hardware divergence and collection cost. The nearly infinite variety of real-world environments can easily exceed the distribution of the available robot data. Additionally, existing datasets predominantly consist of expert demonstrations, lacking the stochasticity in intentions necessary for learning strong action controllability. As a result, existing world models remain confined to simulating observed setups and are often unresponsive to counterfactual actions, constraining their applicability for diverse scenarios and complex tasks. 

In this work, we introduce **DreamDojo** , a generalist world model for open-world dexterous robot tasks. Unlike previous methods that typically rely on teleoperation data, we exploit _human videos_ for pretraining. Despite the embodiment gap, the underlying physics during interactions is largely consistent between humans and robots, enabling effective knowledge transfer. Therefore, we curate the _largest_ egocentric human video dataset to date, **DreamDojo-HV** (Human Videos), which comprises 44k hours of video sequences, surpassing the datasets used in prior works by several orders of magnitude. In addition to its scale, DreamDojo-HV incorporates an exceptionally diverse range of activities, encompassing approximately 96 _×_ more skills and 2,000 _×_ more scenes than the most diverse public datasets for robot learning (Khazatsky et al., 2024; Bu et al., 2025a). This provides us with a rich corpus for learning physics and 

1 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

### dynamics about different kinds of interactions. 

Nevertheless, fine-grained action labels are much scarcer than raw videos when scaling up. Naively training on passive videos overlooks the causality between video observations and actions, leading to inferior knowledge transfer for action-conditioned world simulation. Moreover, converting various action formats into a unified one entails inevitable engineering effort. To address these challenges, we introduce _continuous latent actions_ (Gao et al., 2025) as unified proxy actions for all videos. The proposed latent action model can extract semantically meaningful actions between frames in a self-supervised manner, ensuring effective transfer of both physics and controllability as the data scales to the internet level. Through rigorous designs of model architecture and training recipe, DreamDojo is able to acquire a comprehensive understanding of physics, achieving plausible simulations across diverse environments and finegrained controllability over continuous robot actions. 

To achieve real-time prediction without visual degradation, we further introduce a distillation pipeline following the Self Forcing paradigm (Huang et al., 2025b). Our distillation also enhances the long-horizon consistency by efficiently modeling a short temporal context. The resulting model can autoregressively predict future frames at a resolution of 640 _×_ 480 at 10.93 FPS for an arbitrary horizon, significantly reducing the cost for various downstream applications such as live teleoperation and model-based planning. 

In summary, our main contributions include: (1) **A largescale video dataset** , DreamDojo-HV, that accumulates 44k hours of egocentric experiences from a wide spectrum of daily activities. To the best of our knowledge, this is the _largest_ and most diverse data corpus to date for world model learning. (2) **A generalist world model** for general-purpose robots. By scaling up human videos and introducing continuous latent actions as unified proxy, we present DreamDojo, the _first_ world model of its kind that shows zero-shot generalization to unseen objects and novel environments. (3) **A distillation pipeline** that enables efficient autoregressive prediction and improves context consistency. The final model can be interacted with for more than 1 minute in real time without degradation. (4) **Multiple downstream applications** highlight the potential of DreamDojo in performing live teleoperation, policy evaluation, model-based planning, _etc_ ., accelerating the development of robot policies. 

where _p_ : _S × A →_ ∆( _S_ ) is the transition distribution. In this paper, the term “world model” refers specifically to this category unless otherwise stated. 

**Cosmos-Predict2.5 model.** We establish our world model on the pretrained Cosmos-Predict2.5 model (Ali et al., 2025), a latent video diffusion model that predicts future frames with text and conditional frame inputs. The CosmosPredict2.5 model operates in the continuous latent space produced by WAN2.1 tokenizer (Wan et al., 2025). It injects language and timestep conditions into each DiT block (Peebles & Xie, 2023). The text embedding is processed by cross-attention layers, while the timestep information is first encoded by sinusoidal embeddings, projected by a lightweight MLP, and then used by adaptive layer normalization for dynamic modulations (scale, shift, gate) (Ali et al., 2025). The whole network is trained using flow matching loss (Lipman et al., 2022) for its simplicity and effectiveness. Specifically, given the noise corrupted video latent **x** _t_ at timestep _t_ , the flow matching loss minimizes the prediction error with the ground-truth velocity **v** _t_ : 


where **v** _t_ is a difference between the noise **_ϵ_** and the clean sample **x** ( _i.e_ ., **v** _t_ = **_ϵ_** _−_ **x** ), **c** denotes any conditions ( _e.g_ ., text, conditional frames, and actions for world models), and **u** ( _·_ ; _θ_ ) represents the denoiser parametrized by _θ_ . 

## **3. Approach** 

### **3.1. Overview** 

In this section, we first introduce the features of our dataset in Section 3.2, and then describe the architecture of DreamDojo and its training recipe in Section 3.3. Our whole training procedure consists of three phases: (1) **Pretraining from human videos.** At this stage, we curate three egocentric human datasets for pretraining: In-lab, EgoDex, and DreamDojo-HV. Continuous latent actions are introduced as conditions for all videos. (2) **Post-training on target robots.** To adapt DreamDojo to different embodiments, we reset the action conditioning layer and learn the new action space through finetuning. The post-training can be conducted on a target robot dataset collected from limited scenarios. (3) **Distillation.** Once DreamDojo has learned the target action space, a distillation process can be applied to improve real-time interactivity and context consistency. 

## **2. Preliminary** 

**Interactive world model.** The objective of an interactive world model is to infer future states based on actions. Formally, given an action _a ∈A_ , the interactive world model acts as a state transition function that samples the next state: 


### **3.2. DreamDojo-HV Dataset** 

Existing robot world models are primarily limited to indistribution settings and fall short in generalizing to unseen interactions with new objects (Team et al., 2025; Zhang et al., 2025a). In essence, this limitation arises because most datasets only cover a relatively narrow distribution with 

2 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 1._ **DreamDojo overview.** DreamDojo acquires comprehensive physical knowledge from large-scale human datasets by utilizing latent actions as unified labels. After post-training and distillation on the target robots, our model can predict the future world in real time with continuous action controls. DreamDojo can robustly generalize to various objects and environments, facilitating large-scale policy evaluation without real-world deployment. It also enables live teleoperation and online model-based planning. 


_Figure 2._ **Distribution analysis of DreamDojo-HV. (a)** Distribution of the scenarios and random examples from the most frequent categories. **(b)** [Left]: Distribution of subtask numbers within each video. Most videos involve long-horizon tasks that require multiple interactions to accomplish. [Right]: Representative skills in DreamDojo-HV and their frequencies. Our dataset covers a wide range of interaction types beyond pick-and-place. **(c)** Visualization of skill verbs and object names based on their frequency of occurrence in language annotations. 

3 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

_Table 1._ **Scale and diversity comparison to existing large-scale datasets used by previous world models.** Our curated data mixture excels in both scale and diversity, encompassing 15 _×_ longer duration, 96 _×_ more skills, and 2,000 _×_ more scenes than the previously largest dataset for world model training.<sup>_†_</sup> Estimated by GPT based on the global language annotation of each video clip. 

|Dataset|Type|Prior Works|# Hour|# Trajectory|# Skill|# Scene|
|---|---|---|---|---|---|---|
|RT-1|Robot|IRASim, UniSim|900|130k|8|2|
|BridgeData V2|Robot|IRASim, UniSim,<br>WorldGym, WMPE|130|60.1k|13|24|
|Language-Table|Robot|IRASim, UniSim, HMA|2.7k|442k|-|-|
|RoboNet|Robot|iVideoGPT, IRASim|-|162k|-|10|
|DROID|Robot|Ctrl-World, UWM|350|76k|86|564|
|AgiBot-World|Robot|EnerVerse-AC|2.9k|1,000k|87|106|
|Nymeria|Human|PEVA, EgoTwin,<br>EgoControl|300|1.2k|-|50|
|In-lab|Human|-|55|13.9k|35|1|
|EgoDex|Human|-|829|30k|194<br>|5|
|DreamDojo-HV|Human|-|43,827|1,135k|6,015<sup>_†_</sup><br>|1,135k|
|**Our Mixture**|Human|-|44,711|1,179k|_≥_6,015<sup>_†_</sup>|_≥_1,135k|


limited verbs, objects, and environments, thereby restricting the breadth of interaction patterns. As a result, training on these datasets often fails to preserve the model’s abilities when extending to out-of-distribution scenarios. 

To address this limitation, one might consider increasing the scale of real robot data. However, this may not be the most efficient approach to encompass all potential interaction types, as each new trajectory involves costly teleoperation. On the other hand, human videos, which can be captured during daily activities, emerge as a promising axis to empower robot learning (Zheng et al., 2025; Kareer et al., 2025; Ye et al., 2025b; Chen et al., 2025a) . Inspired by these studies, we scale up human videos as a pioneering step for world model pretraining. Our human data comes from three sources: (1) **In-lab** is collected in our tabletop settings at our laboratory to validate our core designs. The collectors are wearing Manus gloves with Vive Ultimate Tracker to capture precise hand poses, which can be readily retargeted to the GR-1 robot actions. It contains several new objects and new verbs that are unseen in our default robot training dataset. (2) **EgoDex** (Hoque et al., 2025) is a public dexterous human manipulation dataset with egocentric views recorded by Apple Vision Pro. It has 829 hours of egocentric videos with high-precision 3D hand and finger poses collected at the time of recording. It also contains a variety of everyday household objects. We include it to our data suite to enrich object variety. (3) **DreamDojo-HV** is a large-scale in-house dataset collected through crowdsourcing. It features a wide spectrum of loco-manipulation skills and extremely diverse environments, such as household, industrial, retail, educational, and administrative (see Figure 2 for the distribution), which significantly increases the scale and diversity of our data corpus. Each episode is annotated with a text that describes the task being performed. 

As shown in Table 1, our final dataset comprises a total of 44,711 hours, making it the largest human interaction dataset to date for world model pretraining. It includes more 

than 9,869 unique scenes, 6,015 unique tasks, and 43,237 unique objects, representing the majority of interactions in daily activities. Its scale and diversity also provide thorough coverage of various action distributions and increase the stochasticity of the future, thereby enhancing the controllability of actions. In Section 4.3, we demonstrate that increasing the data scale and diversity continues to enhance model performance across all benchmarks. 

### **3.3. DreamDojo Generalist World Model** 

### 3.3.1. MODEL ARCHITECTURE 

Unlike conventional video generators (Wan et al., 2025; Ali et al., 2025), world models are distinct in their prioritization on action controllability (Yang et al., 2024b; 2025a; Huang et al., 2025a). Different from interactive games with discrete inputs (Parker-Holder et al., 2024), achieving genuine controllability for robot actions presents more challenges due to its high dimensionality and contact-rich nature. 

To realize precise action following, we propose two improvements based on the original architecture. First, instead of using the absolute robot joint poses, we transform them into relative actions by rebaselining the inputs with the pose at the beginning of each latent frame ( _i.e_ ., every 4 timesteps). Since relative actions are often concentrated in a narrower space shared across various trajectories, this significantly reduces modeling complexity, thereby enhancing generalization to continuous and compositional robot actions. 

Second, since the consequences of interactions strictly follow causality, observing future actions does not aid predictions at the current timestep but rather increases irrelevant noise. Therefore, instead of sending the entire relative action trajectory as a global condition for all latent frames, we inject actions into the latent frames as chunks (Huang et al., 2025a; Zhu et al., 2025b; Guo et al., 2025b). Specifically, since the temporal compression ratio of the WAN2.1 tokenizer (Wan et al., 2025) is 4 ( _i.e_ ., video latent _x_<sup>_i_</sup> cor- 

4 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 3._ **Latent action model.** [Left]: The information bottleneck design of our latent action model enforces action disentanglement, producing a continuous latent vector that represents actions between frames. [Right]: We retrieve and group the frame pairs from different datasets that share the most similar latent actions. The embodiments are performing the same actions despite the significant differences in context. 

responds to 4 frames _f_<sup>_i_:</sup><sup>_i_+4</sup> in the pixel space, _x_<sup>_i_+1</sup> corresponds to _f_<sup>_i_+4:</sup><sup>_i_+8</sup> , and so on), we concatenate 4 consecutive actions _a_<sup>_t_:</sup><sup>_t_+4</sup> as a chunk and send them to the corresponding latent frame together. This strong prior can greatly mitigate the causality confusion, thereby improving learning efficiency and ultimately enhancing controllability. We show the effects of these two designs above on both expert and counterfactual trajectories in Section D.8. 

### 3.3.2. PRETRAINING FROM HUMAN VIDEOS 

**Latent action as proxy action.** While our data suite includes comprehensive real-world activities, it does not come with fine-grained action annotations. To inherit the rich knowledge from this unlabeled dataset, one straightforward solution is to pretrain the model by passively predicting future frames. In our experiments, we found that this simple approach can transfer certain physical knowledge from human videos, resulting in more physically plausible modeling for unseen objects. Nevertheless, since world models must learn the consequences of actions, relying solely on actionless videos may lead to an inadequate understanding of the causality, ultimately resulting in inferior interactivity when adapting to the target robots. 

To address the inefficient knowledge transfer caused by absence of action labels, it is crucial to derive pseudo labels from pixels that describe the current actions. While offthe-shelf models like HaMeR (Pavlakos et al., 2024) can extract hand poses at scale, these models struggle to represent actions beyond the hands ( _e.g_ ., arm movements and locomotions) and often face challenges in inferring hand positions in heavy occlusions. In addition, they primarily focus on low-level features of the human hands, which may hinder effective knowledge transfer to the target robot when there is a significant embodiment gap. 

On the other hand, latent actions (Bruce et al., 2024; Ye et al., 2025b; Gao et al., 2025), which extract action in- 

formation purely from videos in a self-supervised manner and provide consistent action interpretation across embodiments, have gained increasing attention recently. Inspired by (Gao et al., 2025), we adopt continuous latent actions due to their superiority in cross-embodiment generalization and efficient adaptability. We establish a latent action model as a VAE (Kingma & Welling, 2013) using the spatiotemporal Transformer architecture (Bruce et al., 2024). It has an information bottleneck design that can automatically disentangle the most critical action information from the context. Specifically, unlike the standard VAE, our VAE encoder takes two consecutive frames _f_<sup>_t_:</sup><sup>_t_+1</sup> , extracts spatiotemporal features, and projects the global features to a low-dimensional embedding ˆ _at_ . The VAE decoder receives this embedding along with the former frame _f_<sup>_t_</sup> , aggregates the information and predicts the subsequent frame _f_<sup>_t_+1</sup> . The entire VAE is supervised by the reconstruction loss of the later frame and the KL divergence. The compactness of the embedding and the regularization term together create an information bottleneck. To reconstruct the later frame, the model has to disentangle and compress the most critical motions between frames. 


In egocentric human videos, we found that this embedding particularly captures the human actions and can be transferred across embodiments (see Figure 3). Ultimately, we are able to utilize latent actions as unified proxy labels for world models. During pretraining, we condition each latent frame on the chunked latent actions. Concretely, after extracting latent actions from consecutive frames, we project them using a lightweight MLP to match the dimensions of the timestep embeddings. The last layer of the action MLP is initialized with zeros to avoid perturbing the pretrained model state at the beginning of training (Zhang et al., 2023), which we empirically found leads to improved physics. The projected embeddings are added with the timestep embeddings and then fed into the adaptive layer normalization within each DiT block. 

**Training objective.** As mentioned in Section 2, CosmosPredict2.5 employs the standard flow matching loss (Equation (2)) as its training objective. However, this individual supervision of each frame overlooks the temporal correlation between video frames, which could provide a more direct signal for learning object dynamics and action following. Inspired by previous studies (Wang et al., 2024b; Gao et al., 2024; Yang et al., 2025a), we modify Equation (2) to a new loss that aims to match the ground-truth temporal transitions. Let **z** _t_ = **u** ( **x** _t, t,_ **c** ; _θ_ ) represent the predicted velocity, then the proposed temporal consistency loss can 

5 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

be expressed as: 


Here, _K_ is the total length of the video latent, [ _z_<sup>1</sup> _, z_<sup>2</sup> _, . . . , z_<sup>_k_</sup> ] and [ _v_<sup>1</sup> _, v_<sup>2</sup> _, . . . , v_<sup>_k_</sup> ] are frames in **z** _t_ and **v** _t_ , respectively. In practice, we found that this loss term not only accelerates the learning of action controllability but also effectively enhances object completeness and reduces artifacts. Therefore, our final training objective becomes: 


where _λ >_ 0 is a trade-off coefficient to balance the optimization. We use _λ_ = 0 _._ 1 in our experiments. 

### 3.3.3. POST-TRAINING ON TARGET ROBOTS 

While learning from human videos exposes the model to a wide range of physics interactions, we still require a posttraining stage on the target robot data to adapt our model for downstream applications. To achieve this, we flatten the ground-truth actions of the target robot into a sequence and project the entire sequence through the action MLP. To match the target action space, we reinitialize the first layer of the action MLP and fully finetune it along with all other pretrained weights. Thanks to strong pretraining, the target robot dataset can be collected in limited domains at a small scale while still achieving zero-shot generalization after finetuning. The continuity of our latent action space also ensures better adaptation results compared to other variants (Gao et al., 2025). 

### 3.3.4. DISTILLATION 

In order to unlock capabilities like live teleoperation and online model-based planning, our world model must run autoregressively in real time (Huang, 2025). However, existing video diffusion models are often limited in achieving this due to (1) their bidirectional attention architecture, which defines a fixed horizon length, and (2) a large number of denoising timesteps ( _e.g_ ., 50), which severely hampers inference speed. 

Thus, we introduce an additional distillation stage that converts the foundation DreamDojo model into an autoregressive, few-step diffusion model. We build on the process introduced by Self Forcing (Huang et al., 2025b), which uses two training stages to distill teacher _G_ teacher to student _G_ student. We construct _G_ student with the same architecture and model weights of _G_ teacher, with the exception of the bidirectional attention mechanism, which is replaced with causal attention, and the timestep schedule, which is shortened to a few steps ( _e.g_ ., 4). In the first “warmup” stage, 

we regress student predictions to match ODE solutions generated by our teacher and train via teacher forcing, _i.e_ ., its context consists of latents generated by the teacher. Afterwards, in the second “distillation” stage, we construct the student context with its own previously-generated latents, and supervise with a distribution matching loss (Yin et al., 2024b) based on the KL divergence between real (teacher) and fake (student) distributions. To compute its gradient, we use real and fake models _s_ real and _s_ fake, 


where _z ∼N_ (0 _, I_ ) is noise, _xt_ is produced via forward diffusion with _G_ student starting at _z_ , and _s_ real is estimated by _G_ teacher whereas _s_ fake is estimated by a model trained on the predictions of _G_ student. 

This process minimizes the train-test distribution mismatch, as the student is trained to generate from its previous outputs. To mitigate degradation over long horizons, we also propose to have the student generate more frames than the horizon of the teacher, simulating longer student rollouts and thus further minimizing the train-test discrepancy. 

## **4. Experiments** 

In this section, we conduct extensive experiments to demonstrate DreamDojo’s strengths. Specifically, we aim to answer the following questions: (1) Compared to actionless pretraining, can latent actions enable more effective transfer from human videos? (Section 4.2) (2) Can more diverse data help generalize to new types of physical interaction and scenarios? (Section 4.3 and Section D.6) (3) Can our architectural design and training objective improve the action-conditioned prediction? (Section D.8) (4) Can our distillation pipeline accelerate and stabilize long-horizon interactions? (Section 4.4) (5) Can DreamDojo empower downstream applications, including policy evaluation, testtime search, and live teleoperation? (Section 4.5) 

### **4.1. Benchmark Construction** 

To demonstrate the effectiveness of our method, we conduct the first systematic evaluation that emphasizes out-ofdistribution scenarios and counterfactual actions. To be specific, we mirror the diverse and novel interactions in the three human datasets and construct three corresponding evaluation sets using the Fourier GR-1 humanoid robot: (1) **In-lab Eval** , (2) **EgoDex Eval** , (3) **DreamDojo-HV Eval** . We make every effort to replicate the objects observed in the human videos, allowing our robots to perform the same interactions that reflect similar underlying physics. We also collect a (4) **Counterfactual Eval** set that focuses on counterfactual actions not present in current robot learn- 

6 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

ing datasets, such as patting a toy or reaching toward an object but missing it. To assess DreamDojo’s generalization to diverse environmental changes, we further employ Gemini 2.5 Flash Image ( _a.k.a_ . Nano Banana) (Comanici et al., 2025) to edit the backgrounds of EgoDex Eval and DreamDojo-HV Eval to replicate typical observations in the original datasets. This results in (5) **EgoDex-novel Eval** and (6) **DreamDojo-HV-novel Eval** , with each consisting of 25 samples. A glimpse of the samples from our benchmarks is provided in Figure 7. 

### **4.2. Effects of Different Action Conditions** 

We conduct experiments on both In-lab Eval and EgoDex Eval. To demonstrate the efficacy of the proposed latent action conditioning, we compare our method with three representative baselines: (1) **Without pretraining.** In this setup, the model is initialized from Cosmos-Predict2.5 directly for post-training without observing the human videos. (2) **Action-free pretraining.** In this baseline, we pretrain the world model on unlabeled videos as passive future prediction. The pretrained model is then used for post-training. (3) **Ground-truth action conditioning.** In this baseline, we pretrain the world model with ground-truth action conditioning. This is an ideal setting, where additional equipment is required to obtain high-quality action labels. Specifically, on the In-lab dataset, we condition our model on retargeted GR-1 actions captured by Manus gloves with a Vive Ultimate Tracker, which are mapped to the real GR-1 action specifications for each degree of freedom. The EgoDex dataset utilizes Apple Vision Pro to capture hand poses, which are subsequently transformed into MANO (Romero et al., 2022) by ourselves as conditions during pretraining. 

All compared methods are pretrained for 50k steps on the corresponding human datasets and post-trained for 25k steps on the in-distribution GR-1 dataset. The post-trained models are evaluated on In-lab Eval and EgoDex Eval, which contain novel objects and actions not present in the GR-1 training dataset. The results are reported in Table 3. While pretraining on human videos through action-free video prediction brings marginal benefits, introducing latent actions significantly narrows the gap to the ideal scenario where ground-truth action labels are available. We also provide the PSNR curves throughout the post-training stage in the Appendix. Pretraining with latent actions can reach a much higher upper bound than action-free pretraining and without pretraining. Note that, though MANO actions can also be extracted from videos (Pavlakos et al., 2024), it is likely not as precise as using the Apple Vision Pro to derive the MANO labels in Table 3. Hence, we choose latent actions as unified proxy actions for all human videos during pretraining. 

### **4.3. Effects of Different Data Mixtures** 

We also conduct a dataset ablation to validate the benefits of increasing data diversity. Specifically, we pretrain our model on different data combinations for 50k steps, and then post-train on the GR-1 dataset for 25k steps. Unlike our final models, the sampling ratio is uniform across each dataset for the model variants in this ablation study. We evaluate the post-trained models on In-lab Eval, EgoDex Eval, and DreamDojo-HV Eval, which contain unseen object interactions, as well as on Counterfactual Eval, which features counterfactual actions. From the results in Table 2, increasing data diversity not only improves physics modeling but also enhances the controllability for out-of-distribution actions. We also conduct human preference study for unseen scenarios. See the Appendix for evaluation results. 

### **4.4. Benefits of Distillation** 

To unlock real-time inference, we distill the GR-1 posttrained variant of DreamDojo-2B using the same GR-1 dataset. Stress testing the capabilities of this distillation process, we run both the teacher and student models on GR-1 Long Eval, generating 600 frames (1 minute) of longhorizon, multi-stage tasks. As seen in Table 4, our student model, despite being few-step and autoregressive, achieves performance close to that of the teacher while running at nearly 4 _×_ faster when benchmarked on H100 GPUs. In addition, the autoregressive architecture of our student offers two extra advantages. First, since the student generates each latent frame autoregressively, it enables real-time streaming, which we demonstrate in Section 4.5 is crucial for multiple downstream applications. Second, different from the teacher that is conditioned on a single initial frame, the distilled model can naturally incorporate multiple frames as context, resulting in superior robustness to occlusions and camera shifts. See our Appendix for qualitative samples and the analysis of the generalization ability after distillation. 

### **4.5. Downstream Applications** 

**Policy evaluation.** One of the most straightforward application of world models is for policy evaluation (Li et al., 2025d; Quevedo et al., 2025; Zbinden et al., 2025; Tseng et al., 2025; Team et al., 2025). In this work, we choose AgiBot fruit packing as a typical long-horizon task to verify whether DreamDojo can perform policy evaluation accurately. We train a single-view state-free variant of GR00T N1.5 (Bjorck et al., 2025) on the fruit packing dataset. We also post-train DreamDojo-2B on the same AgiBot dataset. Afterwards, we deploy different checkpoints from training to collect closed-loop rollouts in the real world. More implementation details are provided in the Appendix. 

Following WorldEval (Li et al., 2025d) and SIMPLER (Li 

7 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

_Table 2._ **Effects of using different data mixture.** Adding more human datasets to pretraining consistently improves the performance for both out-of-distribution scenarios and counterfactual actions, highlighting the the potential of our approach. 

|**Pretrained Model**|<br>|**In-lab Eval**<br>|<br>|**E**<br>|**goDex Ev**<br>|**al**<br>|**Drea**<br>|**mDojo-HV**<br>|**Eval**<br>|**Coun**<br>|**terfactual**<br>|**Eval**<br>|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|Cosmos-Predict2.5|20.576|0.774|0.222|19.952|0.787|0.219|18.274|0.754|0.236|20.472|0.802|0.190|
|Data Mixture|||||||||||||
|In-lab|20.913|0.776|0.219|20.267|0.785|0.218|18.621|0.754|0.233|20.755|0.796|0.187|
|In-lab+EgoDex|20.972|0.778|0.216|20.334|0.791|0.215|18.706|0.762|0.230|20.797|0.796|0.188|
|In-|21.016|0.781|0.215|20.414|0.790|0.216|18.724|0.759|0.232|20.852|0.799|0.188|
|lab+EgoDex+DreamDojo-<br>HV|||||||||||||
|DreamDojo-2B|21.114|0.774|0.222|20.411|0.775|0.226|18.813|0.747|0.238|20.907|0.787|0.192|
|DreamDojo-14B|21.413|0.788|0.208|20.525|0.787|0.213|18.924|0.751|0.228|21.087|0.793|0.185|


_Table 3._ **Effects of different action conditioning methods.** Latent action conditioning performs on par with the ideal settings in simulation quality and is the most scalable in use. We denote retargeted action and MANO in gray because they represent ideal collection setups when additional action capture devices are equipped. 


_Figure 4._ **Real vs. DreamDojo success rates.** 

|**Method**||**In-lab Eval**||
|---|---|---|---|
||PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|w/o pretrain|20.576|0.774|0.222|
|action-free|20.797|0.773|0.222|
|latent action|20.913|0.776|0.219|
|retargeted action|20.960|0.773|0.219|
|**Mthd**||**EgoDex Eva**|**l**|
|**eo**|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|w/o pretrain|19.952|0.787|0.219|
|action-free|19.924|0.783|0.222|
|latent action|20.344|0.790|0.214|
|MANO|20.474|0.795|0.211|


_Table 4._ **Results of our distillation pipeline.** Our distilled model is capable of real-time inference (10.93 FPS) with minor degradation in long-horizon rollouts and performance close to that of the teacher. 

|**Mthd**||**GR-1 Long Eval**||
|---|---|---|---|
|**eo**|PSNR_↑_|SSIM_↑_<br>LPIPS_↓_|FPS_↑_|
|Teacher|14.086|0.442<br>0.412|2.72|
|Student|13.146|0.379<br>0.485|10.93|


_Figure 5._ **Model-based planning results.** 

et al., 2024), we utilize Pearson correlation coefficient to quantify linear agreement between real-world and DreamDojo’s success rates and Mean Maximum Rank Violation (MMRV) to measure the rank consistency between these two. Figure 4 shows that DreamDojo’s success rate has a strong linear correlation with real-world success rate (Pearson _r_ =0.995) and maintains a highly consistent ranking (MMRV=0.003), indicating that DreamDojo is able to serve as a reliable simulator for policy evaluation. 

**Model-based planning.** Being able to simulate future outcomes conditioned on actions allows model-based planning that can strengthen and correct the policies at test time (Qi et al., 2025). In this paper, we adopt a simple algorithm for model-based planning. Specifically, similar to the policy evaluation experiment above, we setup 10 AgiBot fruit packing scenes as our touchstone. We ensemble 5 model checkpoints from training to generate action proposals that 

8 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

exhibit sufficient variance at inference time. These action proposals are sent to DreamDojo to predict future video trajectories. Subsequently, the best proposal is selected by an external value model that takes a short video clip as input and is executed by the robot. The implementation details of the value model are provided in the Appendix. 

To ensure execution efficiency, we batch all the action inputs and process them using the distilled DreamDojo-2B. While our world model will introduce additional latency, it will also significantly improve the overall performance. The results are presented in Figure 5. With the help of DreamDojo, the policies can anticipate the outcomes of their predictions in advance and adaptively select the most promising mode for execution, improving the success rate by 5.33% over the best model checkpoint. Compared to uniformly sampling from all policy proposals, applying model-based planning with DreamDojo yields nearly a 13% increase in success rate. These results highlight the huge promise of DreamDojo for online policy steering. 

**Live teleoperation.** We can also provide action conditions by connecting the teleoperative devices used for robot data collection to DreamDojo. To verify this, we deploy DreamDojo-2B on a local desktop equipped with a 5090 GPU and connect a PICO VR controller to capture the upperbody action inputs for the G1 robot. As a result, we found that we could directly teleoperate the virtual robot at realtime speed. An example is shown in Figure 6. For live teleoperation videos, please visit our website. 

## **5. Conclusion** 

In this paper, we introduce DreamDojo, a generalist world model that can simulate dexterous robotics tasks and generalize to unseen scenarios. Our model is pretrained on largescale human datasets that encompass a wide variety of daily interactions. To further enhance knowledge transfer and action controllability, continuous latent actions are introduced as proxy actions for all videos. We further introduce a distillation pipeline that enables stable long-horizon interactions at real-time speed. Extensive evaluations underscore the significance of DreamDojo, demonstrating improved physics understanding and action following in out-of-distribution scenarios, a positive correlation with real-world evaluations, and real-time interactivity for live teleoperation and testtime policy steering. We hope our effort can pave the way for general-purpose robot world models. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of machine intelligence. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here. 

## **References** 

- Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., Cao, J., Cao, T., Cha, E., Chao, Y.-W., et al. World Simulation with Video Foundation Models for Physical AI. _arXiv preprint arXiv:2511.00062_ , 2025. 

- Alonso, E., Jelley, A., Micheli, V., Kanervisto, A., Storkey, A. J., Pearce, T., and Fleuret, F. Diffusion for World Modeling: Visual Details Matter in Atari. In _NeurIPS_ , 2024. 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. _arXiv preprint arXiv:2506.09985_ , 2025. 

- Bai, Y., Tran, D., Bar, A., LeCun, Y., Darrell, T., and Malik, J. Whole-Body Conditioned Egocentric Video Prediction. _arXiv preprint arXiv:2506.21552_ , 2025. 

- Bar, A., Zhou, G., Tran, D., Darrell, T., and LeCun, Y. Navigation World Models. In _CVPR_ , 2025. 

- Bi, H., Wu, L., Lin, T., Tan, H., Su, Z., Su, H., and Zhu, J. H-RDT: Human Manipulation Enhanced Bimanual Robotic Manipulation. In _AAAI_ , 2025. 

- Bjorck, J., Castaneda,˜ F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. GR00T N1: An Open Foundation Model for Generalist Humanoid Robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _π_ 0: A Vision-Language-Action Flow Model for General Robot Control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. RT-1: Robotics Transformer for Real-World Control at Scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Bruce, J., Dennis, M. D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al. Genie: Generative Interactive Environments. In _ICML_ , 2024. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. AgiBot World Colosseo: A Large-scale Manipulation Platform for Scalable and Intelligent Embodied Systems. _arXiv preprint arXiv:2503.06669_ , 2025a. 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. UniVLA: Learning to Act Anywhere with Task-centric Latent Actions. In _RSS_ , 2025b. 

9 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

- Chen, B., Zhang, T., Geng, H., Song, K., Zhang, C., Li, P., Freeman, W. T., Malik, J., Abbeel, P., Tedrake, R., et al. Large Video Planner Enables Generalizable Robot Control. _arXiv preprint arXiv:2512.15840_ , 2025a. 

- Chen, X., Guo, J., He, T., Zhang, C., Zhang, P., Yang, D. C., Zhao, L., and Bian, J. IGOR: Image-GOal Representations are the Atomic Control Units for Foundation Models in Embodied AI. _arXiv preprint arXiv:2411.00785_ , 2024. 

- Chen, X., Wei, H., Zhang, P., Zhang, C., Wang, K., Guo, Y., Yang, R., Wang, Y., Xiao, X., Zhao, L., et al. villa-X: Enhancing Latent Action Modeling in Vision-LanguageAction Models. _arXiv preprint arXiv:2507.23682_ , 2025b. 

- Comanici, G., Bieber, E., Schaekermann, M., Pasupat, I., Sachdeva, N., Dhillon, I., Blistein, M., Ram, O., Zhang, D., Rosen, E., et al. Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities. _arXiv preprint arXiv:2507.06261_ , 2025. 

- Cui, J., Wu, J., Li, M., Yang, T., Li, X., Wang, R., Bai, A., Ban, Y., and Hsieh, C.-J. Self-Forcing++: Towards Minute-Scale High-Quality Video Generation. _arXiv preprint arXiv:2510.02283_ , 2025. 

- Dasari, S., Ebert, F., Tian, S., Nair, S., Bucher, B., Schmeckpeper, K., Singh, S., Levine, S., and Finn, C. RoboNet: Large-Scale Multi-Robot Learning. _arXiv preprint arXiv:1910.11215_ , 2019. 

- Du, M. and Song, S. DynaGuide: Steering Diffusion Polices with Active Dynamic Guidance. In _NeurIPS_ , 2025. 

- Gao, S., Yang, J., Chen, L., Chitta, K., Qiu, Y., Geiger, A., Zhang, J., and Li, H. Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability. In _NeurIPS_ , 2024. 

- Gao, S., Zhou, S., Du, Y., Zhang, J., and Gan, C. AdaWorld: Learning Adaptable World Models with Latent Actions. In _ICML_ , 2025. 

- Garrido, Q., Nagarajan, T., Terver, B., Ballas, N., LeCun, Y., and Rabbat, M. Learning Latent Action World Models In The Wild. _arXiv preprint arXiv:2601.05230_ , 2026. 

- Goswami, R. G., Bar, A., Fan, D., Yang, T.-Y., Zhou, G., Krishnamurthy, P., Rabbat, M., Khorrami, F., and LeCun, Y. World Models Can Leverage Human Videos for Dexterous Manipulation. _arXiv preprint arXiv:2512.13644_ , 2025. 

- Guo, J., Ye, Y., He, T., Wu, H., Jiang, Y., Pearce, T., and Bian, J. MineWorld: A Real-Time and Open-Source Interactive World Model on Minecraft. _arXiv preprint arXiv:2504.08388_ , 2025a. 

- Guo, Y., Shi, L. X., Chen, J., and Finn, C. Ctrl-World: A Controllable Generative World Model for Robot Manipulation. _arXiv preprint arXiv:2510.10125_ , 2025b. 

- Ha, D. and Schmidhuber, J. Recurrent World Models Facilitate Policy Evolution. In _NeurIPS_ , 2018. 

- Hafner, D., Pasukonis, J., Ba, J., and Lillicrap, T. Mastering Diverse Domains through World Models. _Nature_ , 2025a. 

- Hafner, D., Yan, W., and Lillicrap, T. Training Agents Inside of Scalable World Models. _arXiv preprint arXiv:2509.24527_ , 2025b. 

- Ho, D., Monas, J., Ren, J., and Yu, C. 1X World Model: Evaluating Bits, not Atoms, 2025. URL https://www. 1x.tech/1x-world-model.pdf. 

- Ho, J. and Salimans, T. Classifier-Free Diffusion Guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 

- Hong, Y., Mei, Y., Ge, C., Xu, Y., Zhou, Y., Bi, S., HoldGeoffroy, Y., Roberts, M., Fisher, M., Shechtman, E., et al. RELIC: Interactive Video World Model with LongHorizon Memory. _arXiv preprint arXiv:2512.04040_ , 2025. 

- Hoque, R., Huang, P., Yoon, D. J., Sivapurapu, M., and Zhang, J. EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video. _arXiv preprint arXiv:2505.11709_ , 2025. 

- Hore, A. and Ziou, D. Image Quality Metrics: PSNR vs. SSIM. In _ICPR_ , 2010. 

- Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., and Corrado, G. GAIA-1: A Generative World Model for Autonomous Driving. _arXiv preprint arXiv:2309.17080_ , 2023a. 

- Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., Chen, W., et al. LoRA: Low-Rank Adaptation of Large Language Models. In _ICLR_ , 2022. 

- Hu, Y., Xie, Q., Jain, V., Francis, J., Patrikar, J., Keetha, N., Kim, S., Xie, Y., Zhang, T., Fang, H.-S., et al. Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis. _arXiv preprint arXiv:2312.08782_ , 2023b. 

- Huang, S., Wu, J., Zhou, Q., Miao, S., and Long, M. Vid2World: Crafting Video Diffusion Models to Interactive World Models. _arXiv preprint arXiv:2505.14357_ , 2025a. 

- Huang, X. Towards Video World Models, 2025. URL https://www.xunhuang.me/blogs/world_ model.html. 

10 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

- Huang, X., Li, Z., He, G., Zhou, M., and Shechtman, E. Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion. In _NeurIPS_ , 2025b. 

- Jain, A. K., Mohta, V., Kim, S., Bhardwaj, A., Ren, J., Feng, Y., Choudhury, S., and Swamy, G. A Smooth Sea Never Made a Skilled SAILOR: Robust Imitation via Learning to Search. In _NeurIPS_ , 2025. 

- Jang, J., Ye, S., Lin, Z., Xiang, J., Bjorck, J., Fang, Y., Hu, F., Huang, S., Kundalia, K., Lin, Y.-C., et al. DreamGen: Unlocking Generalization in Robot Learning through Video World Models. In _CoRL_ , 2025. 

- Jiang, Y., Chen, S., Huang, S., Chen, L., Zhou, P., Liao, Y., He, X., Liu, C., Li, H., Yao, M., et al. EnerVerseAC: Envisioning Embodied Environments with Action Condition. _arXiv preprint arXiv:2505.09723_ , 2025a. 

- Jiang, Z., Liu, K., Qin, Y., Tian, S., Zheng, Y., Zhou, M., Yu, C., Li, H., and Zhao, D. World4RL: Diffusion World Models for Policy Refinement with Reinforcement Learning for Robotic Manipulation. _arXiv preprint arXiv:2509.19080_ , 2025b. 

- Kanervisto, A., Bignell, D., Wen, L. Y., Grayson, M., Georgescu, R., Valcarcel Macua, S., Tan, S. Z., Rashid, T., Pearce, T., Cao, Y., et al. World and Human Action Models Towards Gameplay Ideation. _Nature_ , 2025. 

- Kareer, S., Pertsch, K., Darpinian, J., Hoffman, J., Xu, D., Levine, S., Finn, C., and Nair, S. Emergence of Human to Robot Transfer in Vision-Language-Action Models. _arXiv preprint arXiv:2512.22414_ , 2025. 

- Khazatsky, A., Pertsch, K., Nair, S., Balakrishna, A., Dasari, S., Karamcheti, S., Nasiriany, S., Srirama, M. K., Chen, L. Y., Ellis, K., et al. DROID: A Large-Scale InThe-Wild Robot Manipulation Dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Kim, S. W., Zhou, Y., Philion, J., Torralba, A., and Fidler, S. Learning to Simulate Dynamic Environments with GameGAN. In _CVPR_ , 2020. 

- Kim, S. W., Philion, J., Torralba, A., and Fidler, S. DriveGAN: Towards a Controllable High-Quality Neural Simulation. In _CVPR_ , 2021. 

- Kingma, D. P. and Welling, M. Auto-Encoding Variational Bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- Kong, L., Yang, W., Mei, J., Liu, Y., Liang, A., Zhu, D., Lu, D., Yin, W., Hu, X., Jia, M., et al. 3D and 4D World Modeling: A Survey. _arXiv preprint arXiv:2509.07996_ , 2025. 

- LeCun, Y. A Path Towards Autonomous Machine Intelligence. _Open Review_ , 2022. 

- Li, H., Ding, P., Suo, R., Wang, Y., Ge, Z., Zang, D., Yu, K., Sun, M., Zhang, H., Wang, D., et al. VLA-RFT: Vision-Language-Action Reinforcement Fine-tuning with Verified Rewards in World Simulators. _arXiv preprint arXiv:2510.00406_ , 2025a. 

- Li, Q., Deng, Y., Liang, Y., Luo, L., Zhou, L., Yao, C., Zeng, L., Feng, Z., Liang, H., Xu, S., et al. Scalable VisionLanguage-Action Model Pretraining for Robotic Manipulation with Real-Life Human Activity Videos. _arXiv preprint arXiv:2510.21571_ , 2025b. 

- Li, S., Gao, Y., Sadigh, D., and Song, S. Unified Video Action Model. In _RSS_ , 2025c. 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating Real-World Robot Manipulation Policies in Simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 

- Li, Y., Zhu, Y., Wen, J., Shen, C., and Xu, Y. WorldEval: World Model as Real-World Robot Policies Evaluator. _arXiv preprint arXiv:2505.19017_ , 2025d. 

- Liang, A., Czempin, P., Hong, M., Zhou, Y., Biyik, E., and Tu, S. CLAM: Continuous Latent Action Models for Robot Learning from Unlabeled Demonstrations. _arXiv preprint arXiv:2505.04999_ , 2025. 

- Lin, S., Yang, C., He, H., Jiang, J., Ren, Y., Xia, X., Zhao, Y., Xiao, X., and Jiang, L. Autoregressive Adversarial PostTraining for Real-Time Interactive Video Generation. In _NeurIPS_ , 2025. 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow Matching for Generative Modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Liu, K., Hu, W., Xu, J., Shan, Y., and Lu, S. Rolling Forcing: Autoregressive Long Video Diffusion in Real Time. _arXiv preprint arXiv:2509.25161_ , 2025a. 

- Liu, M., Shu, J., Chen, H., Li, Z., Zhao, C., Yang, J., Gao, S., Chen, H., and Shen, C. StaMo: Unsupervised Learning of Generalizable Robot Motion from Compact State Representation. _arXiv preprint arXiv:2510.05057_ , 2025b. 

- Liu, V., Adeniji, A., Zhan, H., Haldar, S., Bhirangi, R., Abbeel, P., and Pinto, L. EgoZero: Robot Learning from Smart Glasses. _arXiv preprint arXiv:2505.20290_ , 2025c. 

- Loshchilov, I. and Hutter, F. Decoupled Weight Decay Regularization. In _ICLR_ , 2019. 

- Luo, H., Feng, Y., Zhang, W., Zheng, S., Wang, Y., Yuan, H., Liu, J., Xu, C., Jin, Q., and Lu, Z. Being-H0: VisionLanguage-Action Pretraining from Large-Scale Human Videos. _arXiv preprint arXiv:2507.15597_ , 2025. 

11 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

- Lynch, C., Wahid, A., Tompson, J., Ding, T., Betker, J., Baruch, R., Armstrong, T., and Florence, P. Interactive Language: Talking to Robots in Real Time. _RA-L_ , 2023. 

   - Romero, J., Tzionas, D., and Black, M. J. Embodied Hands: Modeling and Capturing Hands and Bodies Together. _arXiv preprint arXiv:2201.02610_ , 2022. 

   - Russell, L., Hu, A., Bertoni, L., Fedoseev, G., Shotton, J., Arani, E., and Corrado, G. GAIA-2: A Controllable Multi-View Generative World Model for Autonomous Driving. _arXiv preprint arXiv:2503.20523_ , 2025. 

- Ma, L., Ye, Y., Hong, F., Guzov, V., Jiang, Y., Postyeni, R., Pesqueira, L., Gamino, A., Baiyya, V., Kim, H. J., et al. Nymeria: A Massive Collection of Multimodal Egocentric Daily Motion in the Wild. In _ECCV_ , 2024. 

   - Schmidt, D. and Jiang, M. Learning to Act without Actions. In _ICLR_ , 2024. 

- Mendonca, R., Bahl, S., and Pathak, D. Structured World Models from Human Videos. In _RSS_ , 2023. 

   - Seo, Y., Lee, K., James, S. L., and Abbeel, P. Reinforcement Learning with Action-Free Pre-Training from Videos. In _ICML_ , 2022. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., El-Nouby, A., et al. DINOv2: Learning Robust Visual Features without Supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

   - Shin, J., Li, Z., Zhang, R., Zhu, J.-Y., Park, J., Shechtman, E., and Huang, X. MotionStream: Real-Time Video Generation with Interactive Motion Controls. _arXiv preprint arXiv:2511.01266_ , 2025. 

- Pallotta, E., Azar, S. M., Doorenbos, L., Ozsoy, S., Iqbal, U., and Gall, J. EgoControl: Controllable Egocentric Video Generation via 3D Full-Body Poses. _arXiv preprint arXiv:2511.18173_ , 2025. 

   - Sun, W., Wei, F., Zhao, J., Chen, X., Chen, Z., Zhang, H., Zhang, J., and Lu, Y. From Virtual Games to Real-World Play. _arXiv preprint arXiv:2506.18901_ , 2025a. 

- Parker-Holder, J. and Fruchter, S. Genie 3: A New Frontier for World Models, 2025. URL https: //deepmind.google/discover/blog/ 

   - Sun, W., Zhang, H., Wang, H., Wu, J., Wang, Z., Wang, Z., Wang, Y., Zhang, J., Wang, T., and Guo, C. World- 

   - . Play: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling. _arXiv preprint arXiv:2512.14614_ , 2025b. 

- genie-3-a-new-frontier-for-world-models/. 

- Parker-Holder, J., Ball, P., Bruce, J., Dasagi, V., Holsheimer, K., Kaplanis, C., Moufarek, A., Scully, G., Shar, J., Shi, J., et al. Genie 2: A Large-Scale Foundation World Model, 2024. URL https: //deepmind.google/discover/blog/ 

   - Sutton, R. S. Dyna, an Integrated Architecture for Learning, Planning, and Reacting. _ACM Sigart Bulletin_ , 1991. 

- genie-2-a-large-scale-foundation-world-model/Team, . 

   - Team, G.. R., Devin, C., Du, Y., Dwibedi, D., Gao, R., Jindal, A., Kipf, T., Kirmani, S., Liu, F., Majumdar, A., et al. Evaluating Gemini Robotics Policies in a Veo World Simulator. _arXiv preprint arXiv:2512.10675_ , 2025. 

- Pavlakos, G., Shan, D., Radosavovic, I., Kanazawa, A., Fouhey, D., and Malik, J. Reconstructing Hands in 3D with Transformers. In _CVPR_ , 2024. 

   - Team, R., Gao, Z., Wang, Q., Zeng, Y., Zhu, J., Cheng, K. L., Li, Y., Wang, H., Xu, Y., Ma, S., et al. Advancing OpenSource World Models. _arXiv preprint arXiv:2601.20540_ , 2026. 

- Peebles, W. S. and Xie, S. Scalable Diffusion Models with Transformers. In _ICCV_ , 2023. 

- Qi, H., Yin, H., Zhu, A., Du, Y., and Yang, H. Strengthening Generative Robot Policies through Predictive World Modeling. _arXiv preprint arXiv:2502.00622_ , 2025. 

   - Tseng, W.-C., Gu, J., Zhang, Q., Mao, H., Liu, M.Y., Shkurti, F., and Yen-Chen, L. Scalable Policy Evaluation with Video World Models. _arXiv preprint arXiv:2511.11520_ , 2025. 

- Qiu, R.-Z., Yang, S., Cheng, X., Chawla, C., Li, J., He, T., Yan, G., Yoon, D. J., Hoque, R., Paulsen, L., et al. Humanoid Policy ˜ Human Policy. In _CoRL_ , 2025. 

   - Valevski, D., Leviathan, Y., Arar, M., and Fruchter, S. Diffusion Models are Real-Time Game Engines. In _ICLR_ , 2025. 

- Quevedo, J., Liang, P., and Yang, S. Evaluating Robot Policies in a World Model. _arXiv preprint arXiv:2506.00613_ , 2025. 

   - Walke, H. R., Black, K., Zhao, T. Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A. W., Myers, V., Kim, M. J., Du, M., et al. BridgeData V2: A Dataset for Robot Learning at Scale. In _CoRL_ , 2023. 

- Richens, J., Everitt, T., and Abel, D. General Agents Need World Models. In _ICML_ , 2025. 

12 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

- Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.-W., Chen, D., Yu, F., Zhao, H., Yang, J., et al. Wan: Open and Advanced Large-Scale Video Generative Models. _arXiv preprint arXiv:2503.20314_ , 2025. 

- Wang, C., Shi, H., Wang, W., Zhang, R., Fei-Fei, L., and Liu, C. K. DexCap: Scalable and Portable Mocap Data Collection System for Dexterous Manipulation. In _RSS_ , 2024a. 

- Wang, L., Zhao, K., Liu, C., and Chen, X. Learning Real-World Action-Video Dynamics with Heterogeneous Masked Autoregression. _arXiv preprint arXiv:2502.04296_ , 2025a. 

- Wang, X., Zhang, S., Yuan, H., Qing, Z., Gong, B., Zhang, Y., Shen, Y., Gao, C., and Sang, N. A Recipe for Scaling up Text-to-Video Generation with Text-free Videos. In _CVPR_ , 2024b. 

- Wang, Y., Wen, C., Guo, H., Peng, S., Qin, M., Bao, H., Zhou, X., and Hu, R. Precise Action-to-Video Generation Through Visual Action Prompts. In _ICCV_ , 2025b. 

- Wang, Y., Zhang, F., Zhan, D.-C., Zhao, L., Wang, K., and Bian, J. Co-Evolving Latent Action World Models. _arXiv preprint arXiv:2510.26433_ , 2025c. 

- Weng, W., Feng, R., Wang, Y., Dai, Q., Wang, C., Yin, D., Zhao, Z., Qiu, K., Bao, J., Yuan, Y., et al. ART-V: Auto-Regressive Text-to-Video Generation with Diffusion Models. In _CVPR_ , 2024. 

- Wiedemer, T., Li, Y., Vicol, P., Gu, S. S., Matarese, N., Swersky, K., Kim, B., Jaini, P., and Geirhos, R. Video Models are Zero-Shot Learners and Reasoners. _arXiv preprint arXiv:2509.20328_ , 2025. 

- Wu, J., Ma, H., Deng, C., and Long, M. Pre-Training Contextualized World Models with In-the-Wild Videos for Reinforcement Learning. In _NeurIPS_ , 2023. 

- Wu, J., Yin, S., Feng, N., He, X., Li, D., Hao, J., and Long, M. iVideoGPT: Interactive VideoGPTs are Scalable World Models. In _NeurIPS_ , 2024. 

- Wu, Y., Tian, R., Swamy, G., and Bajcsy, A. From Foresight to Forethought: VLM-in-the-Loop Policy Steering via Latent Alignment. In _RSS_ , 2025. 

- Xiao, J., Yang, Y., Chang, X., Chen, R., Xiong, F., Xu, M., Zheng, W.-S., and Zhang, Q. World-Env: Leveraging World Model as a Virtual Environment for VLA PostTraining. _arXiv preprint arXiv:2509.24948_ , 2025. 

- Xiu, J., Hong, F., Li, Y., Li, M., Wang, W., Han, S., Pan, L., and Liu, Z. EgoTwin: Dreaming Body and View in First Person. _arXiv preprint arXiv:2508.13013_ , 2025. 

- Yadav, Y., Zhou, Z., Wagenmaker, A., Pertsch, K., and Levine, S. Robust Finetuning of Vision-Language-Action Robot Policies via Parameter Merging. _arXiv preprint arXiv:2512.08333_ , 2025. 

- Yang, J., Gao, S., Qiu, Y., Chen, L., Li, T., Dai, B., Chitta, K., Wu, P., Zeng, J., Luo, P., et al. Generalized Predictive Model for Autonomous Driving. In _CVPR_ , 2024a. 

- Yang, J., Chitta, K., Gao, S., Chen, L., Shao, Y., Jia, X., Li, H., Geiger, A., Yue, X., and Chen, L. ReSim: Reliable World Simulation for Autonomous Driving. In _NeurIPS_ , 2025a. 

- Yang, J., Shi, Y., Zhu, H., Liu, M., Ma, K., Wang, Y., Wu, G., He, T., and Wang, L. CoMo: Learning Continuous Latent Motion from Internet Videos for Scalable Robot Learning. _arXiv preprint arXiv:2505.17006_ , 2025b. 

- Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., and Abbeel, P. Learning Interactive Real-World Simulators. In _ICLR_ , 2024b. 

- Yang, R., Yu, Q., Wu, Y., Yan, R., Li, B., Cheng, A.-C., Zou, X., Fang, Y., Cheng, X., Qiu, R.-Z., et al. EgoVLA: Learning Vision-Language-Action Models from Egocentric Human Videos. _arXiv preprint arXiv:2507.12440_ , 2025c. 

- Yang, S., Walker, J., Parker-Holder, J., Du, Y., Bruce, J., Barreto, A., Abbeel, P., and Schuurmans, D. Video as the New Language for Real-World Decision Making. In _ICML_ , 2024c. 

- Ye, D., Zhou, F., Lv, J., Ma, J., Zhang, J., Lv, J., Li, J., Deng, M., Yang, M., Fu, Q., et al. Yan: Foundational Interactive Video Generation. _arXiv preprint arXiv:2508.08601_ , 2025a. 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent Action Pretraining from Videos. In _ICLR_ , 2025b. 

- Yin, T., Gharbi, M., Park, T., Zhang, R., Shechtman, E., Durand, F., and Freeman, B. Improved Distribution Matching Distillation for Fast Image Synthesis. In _NeurIPS_ , 2024a. 

- Yin, T., Gharbi, M., Zhang, R., Shechtman, E., Durand, F., Freeman, W. T., and Park, T. One-Step Diffusion with Distribution Matching Distillation. In _CVPR_ , 2024b. 

- Yin, T., Zhang, Q., Zhang, R., Freeman, W. T., Durand, F., Shechtman, E., and Huang, X. From Slow Bidirectional to Fast Causal Video Generators. In _CVPR_ , 2025. 

- Yu, J., Qin, Y., Che, H., Liu, Q., Wang, X., Wan, P., Zhang, D., Gai, K., Chen, H., and Liu, X. A Survey of Interactive Generative Video. _arXiv preprint arXiv:2504.21853_ , 2025. 

13 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

- Zbinden, L., Nelson, N., Chen, J.-T., Chen, X., Woong, J., Azizian, M., Krieger, A., Huver, S., et al. CosmosSurg-dVRK: World Foundation Model-based Automated Online Evaluation of Surgical Robot Policy Learning. _arXiv preprint arXiv:2510.16240_ , 2025. 

- Zhang, J., Huang, Z., Gu, C., Ma, Z., and Zhang, L. Reinforcing Action Policies by Prophesying. _arXiv preprint arXiv:2511.20633_ , 2025a. 

- Zhang, K., Mei, Y., Xu, J., and Patel, V. M. Endless World: Real-Time 3D-Aware Long Video Generation. _arXiv preprint arXiv:2512.12430_ , 2025b. 

- Zhang, L., Rao, A., and Agrawala, M. Adding Conditional Control to Text-to-Image Diffusion Models. In _ICCV_ , 2023. 

- Zhang, L., Kan, M., Shan, S., and Chen, X. PreLAR: World Model Pre-Training with Learnable Action Representation. In _ECCV_ , 2024. 

- Zhang, R., Isola, P., Efros, A. A., Shechtman, E., and Wang, O. The Unreasonable Effectiveness of Deep Features as a Perceptual Metric. In _CVPR_ , 2018. 

- Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., Jang, J., Kundalia, K., Lin, Z., Magne, L., et al. FLARE: Robot Learning with Implicit World Modeling. In _CoRL_ , 2025. 

- Zhou, G., Pan, H., LeCun, Y., and Pinto, L. DINO-WM: World Models on Pre-Trained Visual Features Enable Zero-Shot Planning. In _ICML_ , 2025. 

- Zhu, C., Yu, R., Feng, S., Burchfiel, B., Shah, P., and Gupta, A. Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets. In _RSS_ , 2025a. 

- Zhu, F., Wu, H., Guo, S., Liu, Y., Cheang, C., and Kong, T. IRASim: A Fine-Grained World Model for Robot Manipulation. In _ICCV_ , 2025b. 

- Zhu, F., Yan, Z., Hong, Z., Shou, Q., Ma, X., and Guo, S. WMPO: World Model-based Policy Optimization for Vision-Language-Action Models. _arXiv preprint arXiv:2511.09515_ , 2025c. 

14 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

## **A. Limitations** 

While DreamDojo demonstrates significant improvements over the baseline, it is by no means perfect when simulating uncommon actions, such as slapping and fast waving. Additionally, when conducting policy evaluation, the absolute success rates in DreamDojo are often higher than their real counterparts, indicating a limitation in accurately generating nuanced failures. Future work should explore how to cover broader action distribution, _e.g_ ., using policy rollouts (Zhu et al., 2025c; Ho et al., 2025). We also believe that there remains significant space for improving inference speed through engineering optimizations (Hong et al., 2025; Parker-Holder & Fruchter, 2025; Team et al., 2026). In addition, it does not naturally support multi-view simulation, which is crucial for state-of-the-art policies (Bjorck et al., 2025; Black et al., 2024). Moreover, how to retain the pretrained knowledge as much as possible has not been studied in depth. Future work could explore other fine-tuning strategies (Hu et al., 2022; Yadav et al., 2025) to achieve better post-training performance on the target embodiment. 

## **B. Experiment Details** 

**Training and inference.** The latent action model is a 700M spatiotemporal Transformer (Bruce et al., 2024) that is trained for 400k steps with a total batch size of 256. The dimension of the latent action is 32. The model has 24 encoder blocks for latent action extraction and 24 decoder blocks for forward dynamics prediction. It is trained on a data mixture of the three human video datasets, as well as our in-house robot datasets, including Unitree G1, Fourier GR-1, AgiBot, and YAM. The original videos are temporally downsampled by a random factor of _{_ 1 _,_ 2 _,_ 3 _,_ 4 _}_ to capture various kinds of motions. The video frames are center cropped and resized to a fixed resolution of 240 _×_ 320. The _β_ in Equation (3) is set to 10<sup>_−_6</sup> to achieve a good trade-off between representation capacity and transferability for post-training. We employ the AdamW (Loshchilov & Hutter, 2019) with a weight decay of 0.01 and a constant learning rate of 2 _._ 5 _×_ 10<sup>_−_5</sup> to train the latent action model from scratch. 

The world model is initialized from Cosmos-Predict2.5 (Ali et al., 2025) and pretrained on the mixture of our In-lab, EgoDex, and DreamDojo-HV datasets, with a sampling ratio of 1:2:10, respectively. The video frames are center cropped and resized to a fixed resolution of 640 _×_ 480, and then clipped into sequences with a length of 13 for pretraining. The text condition is fixed as an empty prompt. We present two variants of DreamDojo: a 2B model and a 14B model. Both models are pretrained for 140k steps with an effective batch size of 1024 using 256 H100 GPUs. We use AdamW (Loshchilov & Hutter, 2019) with a weight decay of 0.1, and set the learning rate to 1 _._ 6 _×_ 10<sup>_−_4</sup> . An exponential moving average (EMA) is maintained throughout the training and used to generate all our results. 

In the post-training stage, the videos of the target embodiment ( _e.g_ ., G1, GR-1, AgiBot) are sampled at roughly 10 Hz to capture sufficient motions. The video clips are then organized as sequences with a length of 13. The first frame serves as the condition frame, and the raw actions are processed as relative actions with a length of 12. The world model is finetuned with all weights updated using a similar hyperparameter setting as in the pretraining stage. By default, post-training is conducted with 128 H100 GPUs for 50k steps with a batch size of 512. 

The distillation stage initializes the autoregressive student model with the weights of the teacher, while replacing bidirectional attention with causal attention over a sliding window size of 12 frames. First, for the warmup stage, we generate 10k ODE trajectories and train for 10k iterations. Next, for the distillation step, we have the student randomly generate between 13 and 49 frames during training, and compute loss on the last 13 generated frames. We run this distillation step for 3k iterations. All distillation is conducted on 64 H100 GPUs, using a batch size of 256 for the warmup stage and 64 for the distillation stage. 

During inference, the teacher model utilizes 35 denoising steps for generation, while the distilled model reduces this number to 4 steps. Classifier-free guidance (Ho & Salimans, 2022) is disabled as we empirically found it brings limited benefits. 

**Evaluation protocol.** To quantify the model performance on our evaluation sets, we use PSNR (Hore & Ziou, 2010), SSIM (Hore & Ziou, 2010), and LPIPS (Zhang et al., 2018) as three main automatic metrics. When evaluating the models without distillation, we generate 100 future videos over three rounds by autoregressively resetting the condition frame with the last prediction to make the discrepancies between different variants more discriminative, resulting in 100 samples with 49 frames for most of our evaluations. We choose Fourier GR-1 as a representative target embodiment for most ablative studies. 

Since the ground-truth videos are unavailable for EgoDex-novel Eval and DreamDojo-HV-novel Eval, we design a human 

15 

#### **DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 6._ **Live teleoperation.** We can teleoperate a virtual G1 robot using the PICO VR controller in real time. 


_Figure 7._ **Benchmark visualization.** We rigorously construct six evaluation benchmarks that reflect the diverse scenarios and actions present in human datasets, while being out-of-distribution for the robot training datasets. 

preference evaluation protocol following recent advances (Gao et al., 2024; Wan et al., 2025; Yin et al., 2025). Specifically, we make a web UI and invite 12 volunteers to judge side-by-side video pairs from physics correctness of object interactions and action following compared to the ground-truth video. For physics correctness, they are suggested to focus on object permanence, shape consistency, and contact causality. For action following, we encourage the evaluators to pay more attention to the pose of the robots and allow for a “tie”. We also provide evaluation examples beforehand to justify the key factors the evaluators should focus on. The order of the videos in each pair will be randomly switched to avoid bias, and we average all win rates against the anchor model to obtain the final results. Figure 8 shows our web UI for our human preference evaluation, allowing the evaluators to assess physics correctness and action following intuitively. 

**Policy evaluation details.** We set up 20 different scenes for the fruit packing tasks, covering various combinations of multiple fruits (pear, mango, banana, and starfruit) located in different places on the table. The success rate is determined by the number of fruits successfully picked up from the table and placed into the bag, with 5 fruits designated as 100% success. For each scene, we collect an approximately 80-second rollout in the real world and simulate the entire rollout with the post-trained DreamDojo-2B using the same initial frame. The generated rollouts are scored by human evaluators based on consistent criteria as the real world. The final success rate is averaged across all 20 scenes for both real-world and DreamDojo. 

16 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 8._ **Web UI for human preference evaluation.** To intuitively compare physics correctness and action controls, we devise a web UI that can display the ground-truth video alongside two videos generated by two different models simultaneously. The order of the generated videos will be randomly switched to avoid any potential bias. 

## **C. Related Work** 

**World model.** World models can simulate world transitions in response to actions, which have been proven critical for developing intelligent agents (Ha & Schmidhuber, 2018; Hafner et al., 2025a; Alonso et al., 2024; Richens et al., 2025). Building upon advances in generative models, a surge of works have developed high-quality video world models for simulating interactive games (Yu et al., 2025; Kim et al., 2020; Alonso et al., 2024; Guo et al., 2025a; Parker-Holder et al., 2024; Parker-Holder & Fruchter, 2025; Ye et al., 2025a; Sun et al., 2025a; Kanervisto et al., 2025; Hafner et al., 2025b) and autonomous driving (Kong et al., 2025; Kim et al., 2021; Hu et al., 2023a; Russell et al., 2025; Yang et al., 2024a; Bar et al., 2025). Motivated by successes in these domains, recent works have also introduced video generative models to simulate robot manipulation tasks (Wu et al., 2024; Wang et al., 2025a; Li et al., 2025c; Zhu et al., 2025a; Jiang et al., 2025a; Guo et al., 2025b), which hold great promise for scalable policy evaluation (Li et al., 2025d; Quevedo et al., 2025; Zbinden et al., 2025; Tseng et al., 2025; Team et al., 2025), reinforcement learning (Yang et al., 2024b; Xiao et al., 2025; Li et al., 2025a; Jiang et al., 2025b; Zhu et al., 2025c; Zhang et al., 2025a), and policy steering (Zhou et al., 2025; Assran et al., 2025; Jain et al., 2025; Du & Song, 2025; Wu et al., 2025; Qi et al., 2025). However, existing models are typically trained and evaluated in in-distribution settings, leaving it unclear whether these models can truly facilitate planning in unseen scenarios. 

Another thread of research focuses on world model pretraining from internet-scale videos to improve downstream performances (Seo et al., 2022; Mendonca et al., 2023; Wu et al., 2023; Zhang et al., 2024). More related to ours, VAP (Wang et al., 2025b) utilizes 2D skeletons to unify action conditions from different robots and hands for joint training. AdaWorld (Gao et al., 2025) and the follow-up works (Wang et al., 2025c; Garrido et al., 2026) propose pretraining a world model with latent actions to enhance transferability. Additionally, DexWM (Goswami et al., 2025) leverages human videos to help generalization to unseen dexterous manipulation skills. However, they primarily focus on tabletop datasets in laboratory setups and demonstrate inferior visual quality compared to recent advancements. In contrast, we introduce the first generalist world model for dexterous manipulation, which exhibits strong generalization in simulating diverse out-of-distribution manipulation skills across multiple embodiments. 

**Latent action.** Internet-scale video is an intriguing source for sparking emergent abilities (Yang et al., 2024c; Wiedemer 

17 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

et al., 2025), but the unavailability of action labels could significantly hinder learning efficiency. To address this issue, latent actions have recently been proposed as a promising approach for learning from unlabeled videos (Schmidt & Jiang, 2024; Ye et al., 2025b; Jang et al., 2025; Bu et al., 2025b;a). Besides serving as supervision for policy learning, latent actions can also be utilized as a control interface for world models (Bruce et al., 2024; Chen et al., 2024; Gao et al., 2025; Wang et al., 2025c; Garrido et al., 2026). Several works have also demonstrated the effectiveness of continuous latent actions (Gao et al., 2025; Liang et al., 2025; Yang et al., 2025b; Liu et al., 2025b). Inspired by these explorations, we extract latent actions as a unified proxy for our generalist world model and investigate how this approach can promote robust generalization when interacting with unseen objects after adapting to new embodiments. 

**Autoregressive video generation.** Autoregressive video generation offers the finest granularity and flexibility for interaction (Weng et al., 2024), which is well-suited for action-conditioned world modeling (Valevski et al., 2025; Bruce et al., 2024; Gao et al., 2025; Huang, 2025). To accelerate inference speed, previous methods (Yin et al., 2025; Lin et al., 2025) distill the bidirectional model into an autoregressive student model that only requires fewer steps to generate videos of comparable quality. More recently, Self Forcing and its follow-ups (Huang et al., 2025b; Liu et al., 2025a; Cui et al., 2025; Shin et al., 2025; Zhang et al., 2025b) further reduce long-term drift by mirroring the inference process during training. Building upon these techniques, we present a distillation pipeline that significantly boosts inference speed to real-time levels while ensuring the final model is aware of historical context. This makes our distilled model readily applicable to various downstream tasks, such as performing long-horizon dexterous teleoperation in real time. 

## **D. Additional Results** 

### **D.1. Effects of Our Data Mixtures** 

In addition to the quantitative evaluations, we demonstrate the effectiveness of human data pretraining through visualizations. The samples in Figure 9 verify that incorporating human data pretraining is essential for precise physics modeling of objects not captured by the robot dataset. 

### **D.2. Comparison with Prior Robot World Models** 

To contextualize DreamDojo against the state-of-the-art robot world model, we additionally post-train Ctrl-World (Guo et al., 2025b) using its official configuration and compare it against DreamDojo-2B on all four evaluation sets. As shown in Table 5, DreamDojo-2B surpasses Ctrl-World by a large margin across all evaluation sets in both PSNR and SSIM, demonstrating that the proposed human video pretraining recipe yields substantially better generalization than prior dedicated robot world models. 

_Table 5._ **Comparison with Ctrl-World.** DreamDojo-2B consistently outperforms the prior state-of-the-art Ctrl-World across all four evaluation sets. 

|**Mthd**|**I**|**n-lab Ev**|**al**|**E**|**goDex Ev**|**al**|**Drea**|**mDojo-H**|**V Eval**|**Coun**|**terfactua**|**l Eval**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**eo**|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|Ctrl-World|20.075|0.719|0.215|19.637|0.735|0.205|17.920|0.694|0.231|19.391|0.736|0.216|
|DreamDojo-2B|21.114|0.774|0.222|20.411|0.775|0.226|18.813|0.747|0.238|20.907|0.787|0.192|


### **D.3. Effects of Including Failure Rollouts in Post-Training** 

A key limitation of training only on expert demonstrations is that the model may not learn to simulate nuanced failure trajectories. To examine whether incorporating policy rollouts at the post-training stage helps, we post-train two variants of DreamDojo on the bimanual YAM dataset: one variant uses 35 hours of demonstration data, while the other combines the 35 hours of demonstration data with 5 hours of policy rollouts (of which approximately 5 _/_ 6 are failures). Both variants are trained for 20k steps, and the mixture ratio of demonstration to rollout is 2:1 in the second variant. We then evaluate the PSNR of both variants on a held-out demonstration set (Success) and a held-out failure rollout set (Failure). As shown in Table 6, including failure rollouts in post-training yields a small but consistent gain on the success set, and a much larger gain on the failure set, indicating that the model becomes substantially better at simulating unsuccessful trajectories without sacrificing simulation quality on successful ones. 

18 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

_Table 6._ **Effects of including failure rollouts in post-training.** Mixing a small amount of policy rollouts into post-training substantially improves the simulation of failure trajectories, with no degradation on successful ones. 

|**Eval Set**|w/o rollout|w/ rollout|
|---|---|---|
|Success|21.522|21.547|
|Failure|20.656|22.220|


### **D.4. Sensitivity to Post-Training Data Scale** 

To understand how the amount of post-training data interacts with our human video pretraining, we vary the GR-1 posttraining data scale and finetune two variants for 15k steps each: one initialized from our pretrained DreamDojo, and the other from Cosmos-Predict2.5 without our human video pretraining. Both variants are evaluated on the In-Lab Eval set using PSNR. As shown in Table 7, models with our pretraining outperform those without across all scales. Notably, our pretraining makes the model significantly less sensitive to the size of the post-training dataset; in contrast, the variant without our pretraining performs noticeably worse at 8h, suggesting an overfitting tendency on small post-training corpora. This indicates that our human video pretraining substantially reduces the post-training data requirement for adapting to a new embodiment. 

_Table 7._ **Sensitivity to post-training data scale.** Our pretraining consistently outperforms training without pretraining and makes the model robust to small post-training corpora. 

|**Data Scale**|w/o pretrain|w/ pretrain|
|---|---|---|
|8h|18.889|21.261|
|44h|19.081|21.175|
|88h|19.074|21.109|


### **D.5. Pretraining Benefits Propagating to Downstream Planning** 

To verify whether the benefits of our human video pretraining can propagate to downstream applications, we additionally distill a model post-trained from Cosmos-Predict2.5 on AgiBot fruit packing (i.e., without our human video pretraining) and compare it against our distilled DreamDojo-2B under the model-based planning setup in Section 4.5. We also include a baseline that uniformly samples from the policy action proposals without any world-model-based selection. As shown in Table 8, both world models help over the unified sampling baseline (37%), but the model with our pretraining is substantially better at selecting the correct actions, achieving a 70% success rate compared to 43% for the variant without pretraining. This indicates that the generalization benefits acquired from large-scale human videos translate directly into better downstream planning performance. 

_Table 8._ **Pretraining benefits in model-based planning.** Our human video pretraining propagates to substantially higher downstream success rates in model-based planning on AgiBot fruit packing. 

|unified sampling|w/o pretrain|w/ pretrain|
|---|---|---|
|37%|43%|70%|


### **D.6. Generalization to Unseen Scenarios** 

To benchmark the generalization ability in unseen scenarios, we generate video samples using the two final models, DreamDojo-2B and DreamDojo-14B, and conduct evaluations with Cosmos-Predict2.5 without human video pretraining. All models are post-trained for 30k steps. After post-training, we ask 12 volunteers to evaluate three model pairs: DreamDojo2B _vs_ . Cosmos-Predict2.5, DreamDojo-14B _vs_ . Cosmos-Predict2.5, and DreamDojo-14B _vs_ . DreamDojo-2B. The evaluation is conducted on 50 samples from EgoDex-novel Eval and DreamDojo-HV-novel Eval. The results in Table 9 show that our DreamDojo-2B surpass the original Cosmos-Predict2.5 in both physics correctness and action following by a non-trivial margin, while DreamDojo-14B exhibits a clear advantage over DreamDojo-2B in both axes due to its large capacity. 

### **D.7. Effects of Our Model Designs** 

We provide qualitative comparisons of the results from different model designs as outlined in Table 10. Both relative actions and chunked injection significantly enhance simulation quality, underscoring their importance for achieving precise action 

19 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

_Table 9._ **Human preference evaluation in diverse out-of-distribution scenarios.** DreamDojo outperforms the pretrained CosmosPredict2.5 by a non-trivial margin. Our DreamDojo-14B demonstrates the most competitive performance in both physics correctness and action following. 

|**Metric**|DreamDojo-2B_>_|DreamDojo-14B_>_|DreamDojo-14B_>_|
|---|---|---|---|
||Cosmos-Predict2.5|Cosmos-Predict2.5|DreamDojo-2B|
|Physics Correctness|62.50%|73.50%|72.50%|
|Action Following|63.45%|72.55%|65.53%|


_Table 10._ **Ablations of architecture and loss designs.** Our design choices can effectively enhance the simulation quality of both expert and counterfactual trajectories. 

||**Modifications**|||**GR-1 Val**||**Cou**|**nterfactual**|**Eval**|
|---|---|---|---|---|---|---|---|---|
|relative|chunked|temporal|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
||||16.199|0.557|0.315|19.448|0.768|0.211|
|✓|||16.522|0.576|0.304|19.482|0.772|0.212|
|✓|✓||17.626|0.620|0.267|20.783|0.790|0.193|
|✓|✓|✓|17.630|0.622|0.266|20.980|0.796|0.189|


_Table 11._ **Generalization ability after distillation.** DreamDojo shows consistently better generalization than the baseline. 

|**Method**|**I**|**n-lab Eva**|**l**|**E**|**goDex Ev**|**al**|**Drea**|**mDojo-HV**|**Eval**|**Coun**|**terfactual**|**Eval**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|PSNR_↑_|SSIM_↑_|LPIPS_↓_|
|w/o pretrain|20.304|0.770|0.230|19.119|0.762|0.240|17.869|0.736|0.259|19.782|0.758|0.232|
|w/ pretrain|20.733|0.782|0.220|19.313|0.765|0.235|18.195|0.740|0.254|19.891|0.746|0.234|


controllability. Additionally, the proposed temporal consistency loss further reinforces the modeling quality of objects. 

### **D.8. Ablations of Our Design Choices** 

To efficiently verify the effectiveness of our architectural design and training objective, we finetune Cosmos-Predict2.5 for 30k steps only on the GR-1 training dataset. The finetuned models are then evaluated on a held-out GR-1 validation set with expert demonstrations and the Counterfactual Eval set. Starting with the simple Cosmos-Predict2.5 base architecture, we gradually apply our modifications: relative action transformation, chunked action injection, and the temporal consistency loss. The evaluation results are shown in Table 10. Both relative actions and chunked injection can significantly improve simulation quality, indicating their importance for achieving precise action controllability. The proposed temporal consistency loss further improves performance on both benchmarks, demonstrating its effectiveness in enhancing action following and object modeling. In Figure 10, we also provide qualitative comparisons for these variants. 

### **D.9. Benefits of Distillation** 

We ablate the choice of teacher model in Table 11, evaluating the distillation results of a teacher pretrained on human videos versus one without pretraining (Cosmos-Predict2.5). Across all four evaluation datasets, we observe that the former significantly outperforms the latter. This suggests that the benefits of generalization achieved through our human video pre-training are preserved after distillation, resulting in student models that also excel in unseen scenarios. 

We compare the 1-minute videos generated by the teacher model and the student model in Figure 11. DreamDojo can continuously predict long-horizon rollouts in real time with strong stability and action following. 

In Figure 12, we also visualize representative samples that illustrate the superior consistency of the student model. The distilled DreamDojo can recover objects from occlusions by modeling a short context, whereas the teacher model is unable to achieve this due to its single-frame conditioning. 

### **D.10. DreamDojo-HV Samples** 

To assist a better understanding of the DreamDojo-HV dataset, we visualize more data samples in Figure 13, highlighting its extensive coverage of interaction types and scenarios. 

### **D.11. PSNR Curves in Post-Training** 

We visualize how the PSNR scores will evolve during post-training. From Figure 14, we notice that pretraining with latent actions can reach a much higher upper bound than action-free pretraining and without pretraining, especially on EgoDex 

20 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 9._ **Qualitative comparison of human data pretraining effects.** Through pretraining on diverse human interaction data, DreamDojo acquires a generalizable understanding of general physics, resulting in more realistic simulation for objects that are unseen in the target robot dataset. 

21 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 10._ **Qualitative comparison of our design choices.** Applying all our techniques results in the best capabilities for object modeling and action following. 

22 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 

Eval. 

### **D.12. Value Model** 

To automatically judge the value of the predicted futures, we train an external model based on the DINOv2 (Oquab et al., 2023) architecture. Our value model takes a video clip consisting of 4 frames as input. The DINOv2 backbone is frozen and independently extracts image features from each frame. The features from all frames are then processed by a value prediction module with global attention. The value prediction module is trained to estimate the number of time steps remaining until each subtask boundary, which is defined as the keyframe between consecutive subtask language annotations. The ground-truth value is normalized by the maximum subtask interval in the dataset. For each generated video, the value estimation is performed as a sliding window with a stride of 1. The final value of the current video is defined as the average of all clips from the start to the dip before the estimated value increases. The action proposal with the lowest value ( _i.e_ ., closest to subtask completion) will be selected for real-world execution. A visualization of the accuracy of our value model is shown in Figure 15. 

23 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 11._ **Long-horizon rollouts for 1 minute.** Note that the teacher model generates videos in a chunk-wise manner and operates at a speed (2.72 FPS) that is 4 _×_ slower than that of the student model (10.93 FPS). 

24 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 12._ **The advantage of student context.** The student model exhibits better consistency in handling occlusions and camera shifts, while the teacher model has no way to ensure that due to the missing context. 

25 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 13._ **Diversity of DreamDojo-HV.** We visualize more samples from the curated DreamDojo-HV dataset, which encompasses extremely diverse actions and tool-using scenarios. 

26 

**DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos** 


_Figure 14._ **Post-training PSNR curves using different action conditioning.** Latent action conditioning can achieve comparable performance as high-quality action labels obtained using extra devices. On EgoDex Eval, our approach can also reach a much higher upper bound compared to action-free pretraining and without pretraining. 


_Figure 15._ **Value model estimation.** We visualize the estimated value and the ground-truth value of two representative episodes. Our value model reliably estimates the number of steps remaining to complete the current subtask. 

27 

