---
title: "A Survey on Vision-Language-Action Models for Embodied AI"
date: "2024-05-23"
authors: "Yueen Ma; Zixing Song; Yuzheng Zhuang; Jianye Hao; Irwin King"
url: https://arxiv.org/abs/2405.14093
pdf: https://arxiv.org/pdf/2405.14093
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2405.14093)** / [論文ページ](https://arxiv.org/abs/2405.14093)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

1 

# A Survey on Vision-Language-Action Models for Embodied AI 

Yueen Ma, Zixing Song, Yuzheng Zhuang, Jianye Hao, Irwin King, _Fellow, IEEE_ 

**_Abstract_ —Embodied AI is widely recognized as a cornerstone of artificial general intelligence (AGI) because it involves controlling embodied agents to perform tasks in the physical world. Building on the success of large language models (LLMs) and vision-language models (VLMs), a new category of multimodal models—referred to as vision-language-action (VLA) models— has emerged to address language-conditioned robotic tasks in embodied AI by leveraging their distinct ability to generate actions. The recent proliferation of VLAs necessitates a comprehensive survey to capture the rapidly evolving landscape. To this end, we present the first survey on VLAs for embodied AI. This work provides a detailed taxonomy of VLAs, organized into three major lines of research. The first line focuses on individual components of VLAs. The second line is dedicated to developing VLA-based control policies adept at predicting low-level actions. The third line comprises high-level task planners capable of decomposing long-horizon tasks into a sequence of subtasks, thereby guiding VLAs to follow more general user instructions. Furthermore, we provide an extensive summary of relevant resources, including datasets, simulators, and benchmarks. Finally, we discuss the challenges facing VLAs and outline promising future directions in embodied AI. A curated repository associated with this survey is available at: https://github.com/yueen-ma/Awesome-VLA** 

**_Index Terms_ —Embodied AI, large language model (LLM), multimodality, robotics, vision-language-action (VLA) model, world model** 

## I. INTRODUCTION 

Vision-language-action (VLA) models are a class of multimodal models within the field of embodied AI, designed to process information from three modalities: vision, language, and action. Unlike conversational AI, embodied AI requires controlling physical embodiments that interact with the environment, and robotics is the most prominent domain of embodied AI. In language-conditioned robotic tasks, the policy must possess the capability to understand language instructions, visually perceive the environment, and generate appropriate actions, necessitating the multimodal capabilities of VLAs. The term was recently coined by RT-2 [1]. Compared with earlier deep reinforcement learning (RL) approaches, 

This article has been published in IEEE Transactions on Neural Networks and Learning Systems. This is the author’s version and may not fully reflect the final typeset publication. The final published version can be found via Digital Object Identifier (DOI): 10.1109/TNNLS.2025.3650584 

Yueen Ma and Irwin King are with the Chinese University of Hong Kong, Hong Kong, China (e-mail: yema21@cse.cuhk.edu.hk; king@cse.cuhk.edu.hk; corresponding author: Irwin King). 

Zixing Song is with the University of Bristol, Bristol BS8 1QU, U.K. (email: zixing.song@bristol.ac.uk). 

Yuzheng Zhuang and Jianye Hao are with Huawei Noah’s Ark Laboratory, Shenzhen 518000, China (e-mail: zhuangyuzheng@huawei.com; haojianye@huawei.com). 


Fig. 1. General architecture of VLA models. Three representative methods for action prediction are shown. Related components are presented in dashed boxes. 

VLAs offer superior versatility, dexterity, and generalizability in complex environments. As a result, they are well-suited not only for controlled settings like factories but also for everyday tasks in household environments. 

Early developments in deep learning primarily consisted of unimodal models. In computer vision (CV), models like AlexNet [2] showcased the potential of artificial neural networks (ANNs). Recurrent neural networks laid the groundwork for numerous natural language processing (NLP) models, but NLP has seen a transition in recent years, with Transformers [3] taking precedence. The deep Q-network (DQN) [4] demonstrated that ANNs can successfully tackle RL problems. Leveraging advancements of unimodal models across diverse machine learning fields, multimodal models now address a wide range of tasks, such as visual question answering (VQA), image captioning, and text-to-video generation. 

Conventional robot policies based on RL have largely focused on addressing a limited set of tasks within controlled environments, such as item grasping [5]. However, there is a growing need for more versatile multitask policies, akin to recent trends in large language models (LLMs) and visionlanguage models (VLMs). Developing a multitask policy is challenging, as it requires learning a broader set of skills and adapting to diverse environments. Furthermore, specifying tasks via language instructions offers a more intuitive user-robot interface, which necessitates the development of language-conditioned robot policies. 

Built upon the success of large VLMs, VLA models have demonstrated their potential in addressing these challenges, as illustrated in Fig. 1. Similar to VLMs, VLAs utilize vision foundation models as vision encoders to obtain pretrained 

2162-237X © 2025 IEEE. All rights reserved, including rights for text and data mining, and training of artificial intelligence and similar technologies. Personal use is permitted, but republication/redistribution requires IEEE permission. See https://www.ieee.org/publications/rights/index.html for more information. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

2 


Fig. 2. (a) Venn diagram that outlines the main concepts in embodied AI discussed in this article. (b) Timelines that trace the evolution from unimodal models to VLA models. 

visual representations (PVRs) of the current environmental state, such as object class, pose, and geometry. VLAs encode instructions using the token embeddings of their LLMs and employ various strategies to align vision and language embeddings, including approaches like Flamingo [6], BLIP-2 [7], and LLaVA [8]. By finetuning on robot data, the LLM can function as a decoder to predict actions and perform languageconditioned robotic tasks. These cross-disciplinary innovations drive the advancement of VLAs in embodied AI—a critical building block for AGI. 

VLAs are closely related to three lines of work, as depicted by the timelines in Fig. 2(b) and the taxonomy in Fig. 3. Some approaches focus on individual components of VLAs (see Section III-A), such as PVRs, dynamics learning, world models, and reasoning. Meanwhile, a substantial body of research is dedicated to low-level control policies (see Section III-B). In this category, language instructions and visual observations are fed into the control policy, which then generates low-level actions—such as translation and rotation— thereby rendering VLAs an ideal choice for control policies. In contrast, another category of models serves as high-level task planners responsible for task decomposition (see Section IV). These models break down long-horizon tasks into a sequence of subtasks that, in turn, guide VLAs toward the overall goal, as illustrated in Fig. 4. Most current robotic systems adopt such a hierarchical framework [9], [10], [11] because the high-level task planner can leverage models with high capacity while the low-level control policy can focus on speed and precision, similar to hierarchical RL. 

To provide a more comprehensive overview of current progress in embodied AI, we propose a generalized definition of “VLA,” as illustrated by the Venn diagram in Fig. 2(a). We define a VLA as any model capable of processing multimodal inputs from vision and language to produce robot actions that accomplish embodied tasks, typically following the architecture in Fig. 1. The original concept of VLA referred to a model that adapts VLMs to robotic tasks [1]. Analogous to the distinction between LLMs and more general language models, we designate the original VLAs as “Large VLAs” (LVLAs) because they are based on LLMs or large VLMs. 

## _A. Related Work_ 

To the best of our knowledge, this survey is the first to review the recent progress of VLA models, a rapidly emerg- 

ing research area. Previous surveys have investigated other facets of embodied AI. Firoozi et al. [12] comprehensively summarized foundation models in robotics up to 2023, while Wang et al. [13] focused on LLMs in robotics. Hu et al. [14] examined more recent vision, language, and robotic foundation models for general-purpose robots. Kawaharazuka et al. [15] concentrated on real-world robot applications. In contrast, our work emphasizes VLA models, thereby complementing and extending the existing literature on embodied AI. 

## _B. Contributions_ 

To the best of our knowledge, this article is the first comprehensive survey of emerging VLA models in the field of embodied AI. 

- 1) _Comprehensive Review:_ We present a thorough review of emerging VLA models in embodied AI, covering various aspects including components, architectures, training objectives, and robotic tasks. 

- 2) _Taxonomy:_ We introduce a taxonomy of VLAs based on the hierarchical framework of current robotic systems, comprising two hierarchies: a low-level control policy and a high-level task planner. Control policies execute low-level actions based on specified language commands and the perceived environment. Task planners provide guidance to control policies by decomposing long-horizon tasks into subtasks. We also discuss various essential components of VLAs. 

- 3) _Resources:_ We summarize the necessary resources for training and evaluating VLAs, including recent datasets and benchmarks in real-world or simulated environments. We also discuss various approaches to address current challenges, such as data scarcity and inconsistency. 

- 4) _Future Directions:_ We outline current challenges and promising future opportunities in the field, such as safety, foundation models, and real-world deployment. 

## II. BACKGROUND 

Embodied AI is a unique form of artificial intelligence that actively interacts with the physical environment. This sets it apart from other AI models, such as conversational AI, which primarily handles textual conversations, or generative AI models that focus on tasks like text-to-video generation. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

3 


Fig. 3. Taxonomy of VLA models. The organization of this survey follows this taxonomy. 

Embodied AI encompasses a broad spectrum of embodiments, including smart appliances, smart glasses, autonomous vehicles, and more. Among them all, robots stand out as one of the most prominent embodiments. 

Robot learning is also usually framed as an RL problem, represented as a Markov decision process (MDP) consisting of states ( _s_ ), actions ( _a_ ), and rewards ( _r_ ). An MDP trajectory is denoted by _τ_ = ( _s_ 1 _, a_ 1 _, r_ 1 _, . . . , sT , aT , rT_ ). In certain scenarios, robotic tasks may also be viewed as partially observable Markov decision processes (POMDPs) due to incomplete observations. The primary objective of RL is to train a policy capable of generating optimal actions for the current state _π_ ( _at|st_ ). Various methods, such as TD learning and policy gradients, can be employed to achieve this. However, in cases where defining the reward function proves challenging, imitation learning is utilized to directly model the action distribution within trajectories devoid of rewards _τ_ = ( _s_ 1 _, a_ 1 _, . . . , sT , aT_ ). Furthermore, many multitask robot models employ language as instructions _p_ to determine which task or skill to execute, leading to the development of language-conditioned robot policies _π_ ( _at|p, s≤t, a<t_ ). 

III. VISION-LANGUAGE-ACTION MODELS 

## _A. Components of VLA_ 

A body of work focuses on individual components of VLA models, drawing on successes in CV, NLP, and RL. We introduce them through the lens of embodied AI. 

_1) Reinforcement Learning:_ RL laid the foundation for embodied AI and continues to help advance VLAs. DQN first demonstrated learning policies directly from high-dimensional pixel inputs, underscoring the need for greater model capacity in end-to-end RL. RL trajectories—sequences of states, actions, and rewards—naturally align with sequence modeling problems, making them well-suited to Transformer architectures. Pioneering efforts in this direction include Decision Transformer (DT) [16] and Trajectory Transformer (TT) [17]. Gato [18] further extended this paradigm to a multimodal, multitask, multiembodiment setting. _π_ 0<sup>_∗_</sup> _._ 6<sup>[19] employs RL for</sup> VLAs to learn from experience. 

Furthermore, a synergy has emerged between RL and LLMs, benefiting embodied AI in multiple ways. RL from human feedback (RLHF) aligns LLMs with human preferences and has also been applied to robot learning. SEED [20] utilizes RLHF alongside skill-based RL to address the sparse reward issue and to improve safety via human evaluation. Conversely, LLMs also enable novel RL methods. Reflexion [21] proposes a verbal RL framework that replaces weight updates in RL models with linguistic feedback, making it naturally applicable to embodied decision-making where planning also occurs in language form. Eureka [22] shows that LLMs can design reward functions for embodied agents that outperform expert human-engineered ones. As LLMs evolve, this synergy accelerates progress in RL and embodied AI. 

_2) Pretrained Visual Representations:_ The effectiveness of the vision encoder directly influences the performance of VLAs, as it provides crucial information regarding the current state _st_ , such as object categories, positions, and affordances. Consequently, numerous methods are devoted to improving the quality of PVRs. Their technical details are compared in Table I. 

CLIP [23] has gained widespread adoption as a vision encoder in robotic models. The training objective of CLIP is to identify the correct text-image pair among all possible combinations in a given batch. CLIP is pretrained on the WIT dataset, comprising 400 million image-text pairs. This largescale training allows CLIP to develop a rich understanding of the relationship between visual and textual information. 

R3M [24] proposes two main pretraining objectives: time contrastive learning (CL) and video-language alignment. The objective of time contrastive learning is to minimize the distance between temporally proximal video frames while simultaneously increasing the separation between temporally distant ones. This objective aims to create PVRs that capture the temporal relationships within the video sequence. On the other hand, video-language alignment aims to learn whether a video corresponds to a language instruction. This objective enriches the semantic relevance embedded in the PVRs. VIP [25] also capitalizes on video temporal relationships. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

4 

Table I 

PVRS. V: VISION. L: LANGUAGE. CL: CONTRASTIVE LEARNING. **SIM** / **REAL** : SIMULATED/REAL-WORLD. **MANI** / **NAVI** : MANIPULATION/NAVIGATION. FOR SIMPLICITY, WE ONLY SHOW THE MAIN PART OF THE OBJECTIVE EQUATION, OMITTING ELEMENTS SUCH AS TEMPERATURE, AUXILIARY LOSS. _S_ ( _·_ ) DENOTES A SIMILARITY MEASURE 

|**Model**|**Network**|**Type**|**Objective**|**Notations**|**Robotic Tasks**|
|---|---|---|---|---|---|
|CLIP [23]|ViT-B|VL-CL|�_N_<br>_i_=1 <sup>_−_log</sup><br>exp(_S_(_xi,yi_))<br>�_N_<br>_j_=1 <sup>exp(</sup><sup>_S_(</sup><sup>_xi,yj_))</sup><br>|(_xi, yi_): image-text pair|(Used by CLIPort [29], EmbCLIP [30],<br>and CoW [31])|
|R3M [24]|ResNet-50|Time-CL|�<br>_i,j,k _<sup>_−_log</sup><br>exp(_S_(_xi,xj_))<br>exp(_S_(_xi,xj_))+exp(_S_(_xi,xk_))|_xi_: video frame at time _i_; _i < j < k_|**Sim-Mani**: Meta-World, Franka Kitchen,<br>Adroit|
|MVP [26]|ViT-B/L|MAE|�<br>_i∈M_ <sup>MSE (</sup><sup>_xi, f_mae(</sup><sup>_x/∈M_))</sup><br>|_xi_: image patch; _M_: masked set|**Real-Mani** (xArm7): pick, reach block,<br>push cube, close fridge|
|VIP [25]|ResNet-50|Time-CL|�<br>_τ _<sup>_−_log</sup><br>exp(_S_(_x_0_,xT_))<br>�<br>_i,j_ <sup>exp(</sup><sup>_S_(</sup><sup>_xi,xT_ )</sup><sup>_−γS_(</sup><sup>_xj,xT_ ))</sup>|_xi_: video frame at time _i_; 0_≤i < j < T_;<br>_γ_: discount factor; _τ_: trajectory|**Real-Mani** (Franka): pick and place, close<br>drawer, push bottle, fold towel|
|VC-1 [32]|ViT-L|MAE, CL|(A combination of previous works, including<br>CLIP, R3M, MVP, and VIP.)||**Sim-Mani**: Meta-World, Adroit, DMC,<br>TriFinger, Habitat 2.0; **Sim-Navi**: Habitat|
|Voltron [33]|ViT-S/B|MAE,<br>Lang-Gen|�<br>_i∈M_ <sup>MSE (</sup><sup>_xi, f_mae(</sup><sup>_x/∈M, y_));</sup><br>�_N_<br>_i_=1 <sup>_−_log</sup><sup>_P_ (</sup><sup>_yi | x, y<i_)</sup>|_xi_: image patch; _M_: masked set;<br>_y_: language instruction|**Sim-Mani**: Franka Kitchen;<br>**Real-Mani** (Franka): custom study desk|
|RPT [28]|ViT|MAE|�<br>_i∈M_ <sup>MSE (</sup><sup>_xi, f_mae(</sup><sup>_x/∈M, y, z, . . ._ ))</sup>|_x, y, z_: three distinct modalities; _M_:<br>masked set|**Real-Mani** (Franka): stack, pick, pick<br>from bin|
|DINOv2<br>[34]|ViT|Self-<br>distillation|�<br>_x_<br>�<br>_x_<sup>_′̸_</sup>=_x _<sup>_H_(</sup><sup>_Pt_(</sup><sup>_x_)</sup><sup>_, Ps_(</sup><sup>_x′_))</sup>|_x, x_<sup>_′_</sup>: image views; _H_(): cross-entropy;<br>_Pt, Ps_: teacher, student|(Used by OpenVLA [35], ReKep [36])|
|I-JEPA [37]|ViT|JEPA|�<br>_i∈M_ <sup>MSE (</sup><sup>_f′_(</sup><sup>_xi_)</sup><sup>_, g_(</sup><sup>_f_(</sup><sup>_x/∈M_)))</sup>|_xi_: image block; _M_: target set; _f, f_<sup>_′_</sup>:<br>encoder, EMA encoder; _g_: predictor||
|Theia [38]|ViT-T/S/B|Distillation|(Distillation of vision foundation models:<br>ViT, CLIP, SAM, DINOv2, Depth-Anything.)||**Sim-Mani&Navi**: CortexBench (VC-1);<br>**Real-Mani**: pick, place, open door/drawer|


MVP [26] applies a masked autoencoder (MAE) from computer vision to robotic datasets. The MAE involves masking out a portion of input patches to a ViT model and training it to reconstruct the corrupted patches. This approach closely resembles the masked language modeling technique used in BERT [27] and falls within the purview of self-supervised training. RPT [28] is pretrained with a focus not only on reconstructing visual inputs but also on robotic actions and proprioceptive states. 

Voltron [33] introduces a pretraining objective by incorporating language conditioning and language generation into the MAE objective. Employing an encoder-decoder Transformer structure, the model alternates between language-conditioned masked image reconstruction and language generation from masked images. This enhances the alignment between language and vision modalities. 

VC-1 [32] conducts an in-depth examination of prior PVRs and introduces an enhanced PVR model by systematically exploring optimal ViT configurations across diverse datasets. In addition, they perform a comprehensive comparative analysis of their model against previous methods on various manipulation and navigation datasets, shedding light on the critical factors that contribute to the improvement of PVRs. Another study [39] also compares previous PVRs obtained under supervised learning or self-supervised learning. 

DINOv2 [34] proposes a new self-supervised training paradigm for PVRs that achieves performance beyond that of MAE. It employs a self-distillation framework in which the teacher and student networks receive different views of the same image and match their encoded representations. The student network is updated via gradient descent, while the teacher network is maintained as the exponential moving average of the student network. 

I-JEPA [37] is motivated by the joint-embedding predictive architectures proposed by LeCun [40]. It constructs a “primitive” internal world model by comparing the embeddings of patches. Unlike DINO, which uses cropped images, I-JEPA 

employs masked patches. Moreover, it differs from MAE because it is a nongenerative approach. 

Theia [38] proposes distilling various vision foundation models into a single model. By fusing diverse visual information, such as segmentation, depth, and semantics, it outperforms previous PVRs while requiring less data and a smaller model size. 

_3) Video Representations:_ Videos are simple sequences of images and can be represented by concatenating the usual PVRs of each frame. However, their multiview nature enables a variety of unique representation techniques beyond those mentioned above, such as time CL and MAE. NeRF can be extracted from videos and contains rich 3D information for robot learning, as exemplified by F3RM [41], and 3DLLM [42]. The recent 3D Gaussian Splatting (3D-GS) [43], [44] surpasses NeRF in visual quality and rendering speed. In addition, many videos contain audio, which can provide important cues for robot policies [45]. 

_4) Dynamics Learning:_ Dynamics learning encompasses objectives aimed at endowing the model _f_ ( _·_ ) with an understanding of forward or inverse dynamics. Forward dynamics involves predicting the subsequent state resulting from a given action, whereas inverse dynamics entails determining the action required to transition from a previous state to a known subsequent state: 


Some approaches also frame these objectives as reordering problems for shuffled state sequences. Some forward dynamics methods closely resemble the image or video prediction pretraining used in PVRs. We compare them in Table II. 

Vi-PRoM [46] presents three distinct pretraining objectives. The first involves a contrastive self-supervised learning objective designed to distinguish between different videos. The remaining two objectives are centered around supervised learning tasks: temporal dynamics learning, aimed at recovering 

5 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

Table II 

DYNAMICS LEARNING METHODS FOR VLAS. _f_ ( _·_ ) IS THE DYNAMICS MODEL. FWD, INV: FORWARD & INVERSE DYNAMICS 

|**Model**|**Vision Encoder**|**Type**|**Objective**|**Notations**|**Robotic Tasks**|
|---|---|---|---|---|---|
|Vi-PRoM [46]|ResNet|Temporal dynamics|�_T_<br>_t_=1 <sup>CE(</sup><sup>_t, f_(</sup><sup>_s′_</sup><br>_t_<sup>))</sup><br>|_s_<sup>_′_</sup><br>_t_<sup>: frame in shuffled</sup><br>seq.; _f_(_·_) predicts<br>original frame index|**Sim-Mani**: Meta-World, Franka<br>Kitchen; **Real-Mani**: open & close<br>drawer/door|
|MaskDP [47]|ViT (MAE)|MAE (implicit fwd<br>& inv dynamics)|�_T_<br>_t_=1 <sup>MSE (</sup><sup>_xt, f_mask(</sup><sup>_τ ′_))</sup><br>|_xt ∈{st, at}_; _τ _<sup>_′_</sup>:<br>masked sequence|**Sim**: DeepMind Control Suite|
|MIDAS [48]|ViT, Mask R-CNN|Inverse dynamics|�_T −_1<br>_t_=1 <sup>_−_log</sup><sup>_P_ (</sup><sup>_at | f_inv(</sup><sup>_s_1:</sup><sup>_T_ ))</sup><br>|_s_1:_T_ : full state seq.|**Sim-Mani**: VIMA-Bench|
|SMART [49]|CNN|Forward & inverse<br>dynamics|�_T −_1<br>_t_=1<br>�<br>MSE (_st_+1_, f_fwd(_st, at_))<br>+ MSE (_at, f_inv(_st, st_+1))<br>�<br>+ <sup>�</sup>MSE(_at, f_mask(_τ _<sup>_′_</sup>))<br>|_st_, _at_: state, action; _τ _<sup>_′_</sup>:<br>masked sequence|**Sim**: DeepMind Control Suite|
|PACT [50]|ResNet-18, PointNet|Forward dynamics|�_T −_1<br>_t_=1 <sup>MSE (</sup><sup>_st_+1</sup><sup>_, f_fwd(</sup><sup>_st, at_))</sup>|_st_, _at_: state, action|**Sim-Navi**: Habitat; **Real-Navi**<br>(MuSHR vehicle)|
|VPT [51]|ResNet|Inverse dynamics|�_T_<br>_t_=1 <sup>_−_log</sup><sup>_P_ (</sup><sup>_at | f_inv(</sup><sup>_s_1:</sup><sup>_T_ ))</sup><br>|_st_, _at_: state, action|**Sim**: Minecraft|
|GR-1 [52]|ViT (MAE)|Forward dynamics|�_T −_1<br>_t_=1 <sup>MSE (</sup><sup>_st_+1</sup><sup>_, f_fwd(</sup><sup>_st, at_))</sup>|_st_, _at_: state, action|**Sim-Mani**: CALVIN|


shuffled video frames, and image classification employing pseudo labels. Through a comprehensive comparison with preceding pretraining methods, Vi-PRoM demonstrates its effectiveness for behavior cloning (BC) and PPO. 

MIDAS [48] introduces an inverse dynamics prediction task as part of its pretraining. The objective is to train the model to predict actions from observations, formulated as a motion-following task. This approach enhances the model’s understanding of the transition dynamics of the environment. 

SMART [49] presents a pretraining scheme encompassing three distinct objectives: forward dynamics prediction, inverse dynamics prediction, and randomly masked hindsight control. The forward dynamics prediction task involves predicting the next latent state, while the inverse dynamics prediction task entails predicting the previous action. In the case of hindsight control, the entire control sequence is provided as input, with some actions masked, and the model is trained to recover these masked actions. The incorporation of the first two dynamics prediction tasks facilitates capturing local and short-term dynamics, while the third task is designed to capture global and long-term temporal dependencies. 

MaskDP [47] features the masked decision prediction task, wherein both state and action tokens are masked for reconstruction. This masked modeling task is specifically crafted to equip the model with an understanding of both forward and inverse dynamics. Notably, in contrast to preceding masked modeling approaches like BERT or MAE, MaskDP can be applied directly to downstream tasks in a zero-shot manner. 

PACT [50] introduces a pretraining objective aimed at modeling state-action transitions. It receives sequences of states and actions as input, and predicts each state and action token autoregressively. This pretrained model serves as a dynamics model, which can then be finetuned for various downstream tasks such as localization, mapping, and navigation. 

VPT [51] proposes a video pretraining method that harnesses unlabeled internet data to pretrain a foundation model for the game of Minecraft. The approach begins by training an inverse dynamics model using a limited amount of labeled data, which is then utilized to label internet videos. Subsequently, this newly auto-labeled data is employed to train the VPT foundation model through BC. This methodology follows semi-supervised imitation learning. As a result of this process, the model demonstrates human-level performance across a 

multitude of tasks. 

GR-1 [52] introduces video prediction pretraining tailored for a GPT-style model. The ability to anticipate future frames aligns with forward dynamics learning, contributing to more accurate action prediction. 

_5) World Models:_ A world model _P_ ( _·_ ) encodes commonsense knowledge about the world and predicts the future state for a given action [40]: 


It enables model-based control and planning for embodied agents, as they can search for an optimal action sequence in imaginary space before executing any real actions. Although forward dynamics learning also attempts to predict the next state, it is usually treated as a pretraining task or an auxiliary loss to enhance the action decoder for the primary robotics tasks, rather than serving as a standalone module. In addition, new embodied experiences can be sampled from visual world models that explicitly generate images or videos of future states. 

Dreamer [53] employs three primary modules to construct a latent dynamics model: a representation model, responsible for encoding images into latent states; a transition model, which captures transitions between latent states; and a reward model, predicting the reward associated with a given state. Under the actor-critic framework, Dreamer utilizes an action model and a value model to learn behavior through imagination by propagating analytic gradients through the learned dynamics. Building upon this foundation, DreamerV2 [54] introduces a discrete latent state space along with an improved objective. DreamerV3 [55] extends its focus to a broader range of domains with fixed hyperparameters. DayDreamer [56] applies this method to physical robots performing real-world tasks. 

IRIS [57] employs a GPT-like autoregressive Transformer as the foundation of its world model, with a VQ-VAE serving as the vision encoder. Subsequently, a policy is trained using imagined trajectories, which are unrolled from a real observation by the world model. TWM [58] also investigates the application of Transformers in building world models. 

_6) LLM-Induced World Models:_ LLMs encompass a wealth of commonsense knowledge about the world, prompting many approaches to leverage that knowledge for improving VLAs. 

6 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

DECKARD [59] prompts an LLM to generate abstract world models (AWMs) represented as directed acyclic graphs [60], [61], specifically tailored for the task of item crafting in Minecraft. DECKARD iterates between two phases: in the Dream phase, it samples a subgoal guided by AWM; in the Wake phase, DECKARD executes the subgoal and updates the AWM through interactions with the game. This guided approach enables DECKARD to achieve markedly faster item crafting compared with baselines lacking such guidance. 

LLM-DM [62] uses an LLM to construct world models in planning domain definition language (PDDL)—a capability that LLM+P [63] did not achieve, as its PDDL world model was hand-crafted. The LLM also acts as an interface, mediating between the generated PDDL model and corrective feedback from syntactic validators and human experts. Finally, the PDDL world model serves as a symbolic simulator, enabling plan generation. 

RAP [64] repurposes an LLM to act as both a policy that predicts actions and a world model that provides the state transition distribution. Unlike previous chain-of-thought (CoT) prompting methods, RAP incorporates Monte Carlo tree search (MCTS) to enable structured planning, allowing the LLM to build a reasoning tree incrementally. This reasoning strategy helps RAP find a high-reward path that balances exploration and exploitation. Tree-Planner [65] improves efficiency by prompting the LLM only once to generate diverse paths within an action tree. 

LLM-MCTS [66] extends the problem setting to POMDPs. As a world model, the LLM generates the initial belief of the current state; as a policy, it serves as a heuristic to guide action selection. By leveraging its commonsense knowledge, the LLM reduces the search space of MCTS, thereby improving search efficiency. 

_7) Visual World Models:_ Unlike LLM-induced world models, which are in textual form, visual world models generate images, videos, or 3D scenes of future states—aligning more closely with the physical world. They can further be utilized to generate new trajectories. This direction has been gaining increasing attention since Sora demonstrated world-simulation capabilities [67], as investigated by a dedicated survey [68]. 

Genie [69] introduces a new class of generative models, termed generative interactive environments. It consists of three main components: a spatiotemporal video tokenizer, an autoregressive dynamics model, and a latent action model. After being trained on unlabeled videos in an unsupervised manner, Genie allows users to interact with the generative environment on a frame-by-frame basis. Consequently, Genie establishes a foundation world model. 

3D-VLA [70] proposes a 3D world model capable of goal generation. It processes visual inputs, such as images, depth maps, and point clouds, and then generates a goal state— either as an image or a point cloud—using diffusion models in response to the user’s query. The generated goal state can subsequently be used to guide robot control. 

UniSim [71] builds a generative model based on real-world interaction videos. It is capable of simulating visual outcomes for both high-level and low-level actions, which can then be leveraged as new experiences for training embodied agents. 

E2WM [72] even treats existing simulators as world models to collect embodied experiences via MCTS. 

_8) Reasoning:_ Reasoning has become a key capability of LLMs, as demonstrated by chain-of-thought (CoT) methods [73], [74]. In embodied AI, researchers are exploring how to leverage CoT reasoning to refine the decision-making process. 

Reasoning is naturally compatible with high-level task planning, as both often occur in the language domain. ThinkBot [75] applies CoT to recover missing action descriptions in sparse human instructions, thereby enhancing instruction coherence and boosting success rates in difficult tasks. ReAct [76] interleaves reasoning traces and actions, where CoT can help create action plans, inject commonsense knowledge, and handle exceptions, ultimately improving embodied decision-making. RAT [77] integrates CoT with retrievalaugmented generation (RAG) to mitigate hallucinations and thus improve embodied planning. Tree-Planner [65] employs a tree-of-thoughts approach for task planning. 

Another paradigm involves equipping low-level control policies with reasoning capabilities, as pioneered by ECoT [78]. This method trains OpenVLA [35] to conduct embodied CoT reasoning about plans, subtasks, motions, and visual features, before predicting low-level actions. By relying on this multistep reasoning rather than the “muscle memory” of VLAs, it improves success rates on challenging generalization tasks without requiring additional robot data. CoT-VLA [79] introduces visual CoT reasoning for VLAs. 

_9) Policy Steering:_ Policy steering can enhance VLA performance at test-time without the need for expensive retraining. V-GPS [80] re-ranks generated actions based on a learned value function, while RoboMonkey [81] employs a VLMbased verifier to select the optimal action from a sampled set. _10) Strengths and Limitations:_ 

_a) PVRs:_ Although time CL with videos and text-guided pretraining methods, such as CLIP, provide image-level information, they lack the pixel-level details offered by MAEbased self-supervised learning methods. Pixel-level information contains rich details—including segmentation masks, object positions, and depth estimation—that are generally more useful for robot manipulation tasks requiring high precision, as demonstrated by VC-1’s comparison [32]. DINOv2 learns both pixel- and image-level features by combining masked image modeling with a momentum encoder and multicrop augmentation, with benefits on downstream robotic tasks evidenced by OpenVLA [35]. I-JEPA focuses on patches in the representation space and, as a result, captures low-level image features more effectively than view-invariance methods such as DINO. Theia distills various off-the-shelf vision foundation models into a single model that surpasses isolated individual models, as demonstrated by comprehensive evaluations against most existing PVRs in robot learning [38]. 

_b) Forward & Inverse Dynamics:_ Forward dynamics learning is generally more challenging than inverse dynamics learning because predicting future states is more complex than predicting past actions. Consequently, the difficulty of forward dynamics often leads to greater performance improvements, as demonstrated in SMART. However, inverse dynamics models 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

7 


Fig. 4. Illustration of a hierarchical robot policy. The high-level task planner decomposes the user instruction into subtasks, which are then executed step by step by the low-level control policy. 

can be used to generate action labels for datasets that contain only states, such as raw robot manipulation videos. 

_c) World Models & Reasoning:_ Although both world models and reasoning methods can be applied to low-level control policies and high-level task planners, current approaches remain distinct. World models are predominantly used to interact with control policies because they excel at generating the immediate next state given low-level actions. In contrast, CoT-based reasoning methods focus on task planning since they express thought chains in text, making them wellsuited for refining text-based task plans. 

## _B. Low-Level Control Policies_ 

Through the integration of an action decoder with perception modules, such as vision encoders and language encoders, a VLA model _πθ_ with parameters _θ_ is formed as a control policy to execute language instructions _p_ : 


It can also be referred to as a low-level policy, low-level controller, or action primitive. The diversity among VLAs arises from individual modules and overall architectures. The general architecture is shown in Fig. 1. This section explores various approaches to designing low-level control policies. Table III summarizes their technical details. 

_1) Non-Transformer Control Policies:_ Prior to the adoption of Transformer models, early control policies for languageconditioned robotic tasks varied significantly in architecture. 

CLIPort [29] integrates CLIP with the Transporter network, creating a two-stream architecture. The CLIP vision encoder extracts “semantic” information from the RGB image, while the Transporter network extracts “spatial” information from the RGB-D image. The CLIP sentence encoder encodes the language instruction and guides the output _SE_ (2) action, consisting of paired pick and place end-effector poses. It represents an early demonstration of language-conditioned pick-and-place capabilities. 

BC-Z [82] processes two types of task instructions: a language instruction or a human demonstration video. The environment is presented to the model in the form of an RGB image. Then the instruction embedding and the image embedding are combined through the FiLM layer, culminating in the generation of actions. This conditional policy is asserted to exhibit zero-shot task generalization to unseen tasks. 

MCIL [83] represents a pioneering robot policy that integrates free-form natural language conditioning. This is in contrast to earlier approaches that typically rely on conditions in the form of task IDs or goal images. MCIL introduces the capability to leverage unlabeled and unstructured demonstration data. This is achieved by training the policy to follow either image or language goals, with a small fraction of the training dataset consisting of paired image and language goals. 

HULC [84] introduces several techniques aimed at enhancing robot learning architectures. These include a hierarchical decomposition of robot learning, a multimodal Transformer, and discrete latent plans. The Transformer learns high-level behaviors, hierarchically dividing low-level local policies and the global plan. In addition, HULC incorporates a visuolingual semantic alignment loss based on CL to align VL modalities. HULC++ [85] further integrates a self-supervised affordance model. This model guides HULC to the actionable region specified by a language instruction, enabling it to fulfill tasks within this designated area. 

UniPi [86] treats the decision-making problem as a textconditioned video generation problem. To predict actions, UniPi generates a video based on a given text instruction, and actions are extracted from the frames of the video through inverse dynamics. This innovative policy-as-video formulation offers several advantages, including enhanced generalization across diverse robot tasks and the potential for knowledge transfer from internet videos to real robots. 

_2) Transformer-Based Control Policies:_ Since the introduction of Transformers, control policies have converged to similar Transformer-based architectures. 

Interactive language [88] presents a robotic system wherein the low-level control policy can be guided in real-time by human instructions conveyed through language, enabling the completion of long-horizon rearrangement tasks. The efficacy of such language-based guidance is primarily attributed to the utilization of a meticulously collected dataset containing diverse language instructions, which surpasses previous datasets by an order of magnitude in scale. 

Hiveformer [89] places significant emphasis on leveraging multiview scene observations and maintaining the full observation history for a language-conditioned policy. This approach represents an advancement over previous systems, such as CLIPort and BC-Z, that only use the current observation. Notably, Hiveformer stands out as one of the early adopters 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

8 

Table III 

VLAS THAT SERVE AS LOW-LEVEL CONTROL POLICIES. ♢ INDICATES LARGE VLAS. CLOSELY RELATED (NON-VLA MODELS) ARE INCLUDED IN BRACKETS. THE REMAINING ARE GENERALIZED VLAS. CONT/DISC: CONTINUOUS/DISCRETE ACTION. TFM: TRANSFORMER. XATTN: CROSS-ATTENTION. CONCAT: CONCATENATION. QUANT.: QUANTIZATION. _p_ / _s_ : PROMPT/STATE VISION ENCODER. [SC]: SELF-COLLECT DATA 

|**Model**|**Vision**<br>**Encoder**|**Language**<br>**Encoder / VLM**|**Action De-**<br>**coder/Head**|**Architecture**|**Training**<br>**Objectives**|**Training**<br>**Datasets**|**Environments, Embodiments, Tasks, and**<br>**Skills**|
|---|---|---|---|---|---|---|---|
|CLIPort [29]|CLIP-ResNet50,<br>TtRNt|CLIP-GPT|LingUNet|Hadamard|BC (_SE_(2))|[SC]|**Sim**: Ravens|
|MCIL [83]|ransporer-ese<br>Custom-CNN|USE|RNN|LMP|MCIL|Play-LMP, [SC]|**Sim**: 3D Playroom environment|
|HULC [84], [85]<br>Lanuaecosts[87]|MCIL CNN<br>CLIP-ViTUNet|Sentence-BERT<br>CLIP-GPT|RNN<br>STORM|LMP<br>Concat|MCIL<br>MLE(costma)|CALVIN data<br>[SC]|**Sim**: CALVIN<br>**Sim**&**Real**(Franka):icklace|
|gg  <br>Interactive Language<br>[88]|, <br>ResNet|CLIP-GPT|TFM|Xattn|p<br>BC (cont)|[SC: Language-<br>Table]|p, p<br>**Sim** & **Real** (xArm6): rearrangement|
|Hiveformer [89]<br>PerAct [90]|UNet<br>3D CNN|CLIP-GPT<br>CLIP-GPT|TFM, UNet<br>PerceiverIO|Concat<br>Concat|BC (cont)<br>3D affordance|RLBench data<br>RLBench data,<br>[SC]|**Sim**: RLBench<br>**Sim**: RLBench; **Real** (Franka): pick, place,<br>stackopendrawersweepinsertpegetc.|
|Act3D [91]|CLIP-ResNet50|CLIP-GPT|TFM|Xattn|3D affordance<br>(l)|RLBench data,<br>[SC]|,  , ,  , <br>**Sim**: RLBench; **Real** (Franka): reach target,<br>itkt|
|RVT [92],<br>RVT2[93]|CLIP-ResNet50|CLIP-GPT|TFM|Concat|voxe<br>2D affordance<br>(tt3D)|RLBench data,<br>[SC]|wpe, sac, ec.<br>**Sim**: RLBench; **Real** (Franka): stack, press,<br>l|
|- <br>RoboPoint [94]|ViT-L/14|Vicuna-V1.5<br>||Concat|projec o <br>2D affordance<br>|[SC]|pace<br>**Real** (Franka): pick, place|
|Gato [18]|ViT|13B<br>Sent.Piece|TFM|Concat|(project to 3D)<br>BC (cont & disc)|[SC]|**Sim** & **Real** (Sawyer): RGB-stacking|
|(RoboCat) [95]|VQ-GAN (_p, s_)||TFM|Quant.|BC, observation<br>prediction|Self-<br>improvement|**Sim** & **Real** (Sawyer, Franka, KUKA):<br>stackingbuildingliftinginsertionremoval|
|VIMA [96]<br>|ViT, Mask R-CNN<br>|T5<br>|TFM<br>|Xattn<br>|BC (_SE_(2))<br>|[SC:VIMA-Data]<br>|, , , , <br>**Sim** (Ravens): VIMA-Bench<br>|
|BC-Z [82]<br>RT-1 [97]|ResNet18 (_p, s_)<br>EfficientNet|USE<br>USE|MLP<br>TFM|FiLM<br>FiLM|BC (cont)<br>BC (disc)|[SC]<br>[SC: Fractal]|**Real** (EDR): pick-place/wipe/drag, grasp, push<br>**Real** (EDR): pick-place, move, knock|
|MOO [96]|OWL-ViT (_p_),<br>EfficientNet(_s_)|USE|TFM|FiLM|BC (disc)|[SC]|**Real** (EDR): pick, move near, knock, place<br>uprightplaceinto|
|Q-Transformer [98]|i <br>EfficientNet|USE|TFM|FiLM|TD error|Fractal, Auto-<br>ll|,  <br>**Sim**: pick; **Real** (EDR): pick, place, open/close<br>d|
|(RT-Trajectory) [99]|EfficientNet||TFM||BC (disc)|coect<br>[SC]|rawer, move near<br>**Real** (EDR): pick, place, fold towel, swivel<br>chairetc|
|(ACT) [100]|ResNet18||CVAE-TFM||BC (cont, action<br>|[SC] with<br>|, .<br>**Sim**: transfer cube, bimanual insertion; **Real**<br>|
|RoboAgent / MT-<br>ACT [101]|CNN||CVAE-TFM|FiLM|chunking)<br>BC (cont, action<br>chunking)|ALOHA<br>RoboSet|(ViperX, WidowX): slot battery, open cup, etc<br>**Real** (Franka): pick, place, open/close drawers,<br>pour, push, drag, etc.|
|RoboFlamingo [102]|CLIP-ViT-L/14|LLaMA, MPT,<br>GPT-NeoX|LSTM, TFM|Xattn|BC (cont)|CALVIN data|**Sim**: CALVIN|
|RbUniVi[103]|UVFrmr|(Mdldi|nfllRb|lmin)|BC(nt)|CALVINdt|**Sim**CALVIN|
|ooew <br>DRVLA104|oe<br>M|oe es<br>ldifllR|oows oo<br>Fli|ago|co<br>BC|aa<br>CALVINd|: <br>**Si**CALVIN|
|ee- []<br>Instruct2Act [105]|(o<br>CLIP, SAM|e esgn oows o<br>ChatGPT|oamngo++)<br>Robot APIs|Tool-Use|(cont)|ata|**m**: <br>**Sim** (Ravens): VIMA-Bench|
|VoxPoser [106]|ViLD, MDETR,|GPT-4|MPC|Tool-Use|||**Sim**: Sapien; **Real** (Franka): move&avoid, set|
|UniPi [86]|OWL-ViT, SAM<br>Imagen video|T5-XXL|CNN|Xattn|Inverse dynamics|[SC:PF], Ravens,<br>BrideV1|table, close drawer, open bottle, sweep trash<br>**Sim**: Painting Factory (PF), Ravens|
|(Diffusion Policy)<br>|ResNet18||UNet, TFM||DDPM|g<br>[SC]|**Sim**: Robomimic, Franka Kitchen, etc; **Real**<br>l|
|[107]<br>(DP3) [108]|DP3 Encoder|(Model desig|n follows Diffusi|on Policy)|DDIM|[SC]|(UR5, Franka): push-T, flip mug, pour sauce<br>**Sim**: (72 tasks); **Real** (Franka, Allegro hand):<br>lldlidill|
|SUDD [109]|ResNet18|CLIP-GPT|UNet, TFM|Concat|DDPM|Lang-guided<br>datageneration|ro-up, umpng, r, pour<br>**Sim**: MuJoCo; **Real** (UR5e): pick, place|
|Octo [110]|CNN|T5-base|TFM|Concat|DDPM|<br>OXE|**Real**: BridgeV2, CMU Baking, Stanford<br>CoffeeBerkelePeInsertetc|
|3D Diffuser Actor<br>||(Model design follow|s Act3D)||DDPM|RLBench,<br>|, y g , .<br>**Sim**: RLBench, CALVIN; **Real** (Franka): put,<br>|
|[111]<br>MDT [112]|CLIP-ViT-B/16 (_p_),<br>|CLIP-GPT|DiT|Concat|DDIM|CALVIN, [SC]<br>CALVIN,<br>|open, close, stack, etc.<br>**Sim**: CALVIN, LIBERO; **Real** (Franka): pick,<br>|
|RDT-1B [113]|Voltron/ResNet18 (_s_)<br>SigLIP|T5-XXL|DiT|Xattn|DDPM|LIBERO, [SC]<br>(Aggregated<br>Datasets)|push, open, close, etc.<br>**Real** (ALOHA dual-arm): wash, pour, fold,<br>etc|
|RT-2 [1] ♢|ViT-4B, ViT-22B|PaLI-X, PaLM-E|Symbol-<br>ti|Concat|BC (disc), Co-<br>fiti|Fractal, VQA|.<br>**Sim**: Language-Table; **Real**: RT-1 evaluation<br>tk|
|RT-H [114] ♢<br>||(Model design follo<br>|unng<br>ws RT-2)<br>||ine-unng<br>BC (disc)<br>|Diverse+Kitchen<br>|ass<br>**Real**: Diverse+Kitchen eval tasks<br>|
|RT-X [115] ♢<br>OpenVLA [35] ♢|DINOv2, SigLIP|(Models from RT-1 a<br>Prismatic-7B|nd RT-2)<br>Symbol-<br>tuning|Concat|BC (disc)<br>BC (disc)|[SC: OXE]<br>OXE, DROID|**Real**: BridgeV2, RT-1 evaluation tasks, etc.<br>**Real**: BridgeV2, RT-1 evaluation tasks,<br>Franka-TabletopDROIDetc.|
|OpenVLA-OFT<br>[116]♢|(Im|proves OpenVLA with|OFT recipe)||BC (cont, parallel<br>decodew/chunk)|LIBERO, [SC]|, , <br>**Sim**: LIBERO; **Real** (ALOHA setup): fold,<br>scoopput|
|<br>TraceVLA [117] ♢|(Model design fo|llows OpenVLA, addi|ng visual trace|prompting)|.<br>BC (disc)|BridgeV2,<br>FtlSC|, <br>**Sim**: SimplerEnv; **Real** (WidowX): pick, push,<br>fldi|
|_π_0 [118] ♢|SigLIP|PaliGemma|Action<br>|Concat|Flow matching|raca, []<br>OXE, [SC: _π_-<br>|o, swpe<br>**Real** (general robot control): sweep, open,<br>|
|RoboMamba [119] ♢|CLIP-ViT|Mamba|expert<br>MLP|Concat|BC (cont)|cross-embod.]<br>[SC]|pack, etc.<br>**Sim**: Sapien; **Real** (Franka): open door/box,<br>|
|SpatialVLA [120] ♢|SigLIP, Ego3D<br>iidi|PaliGemma 2|MLP|Concat|BC (Adaptive<br>Aiid|OXE, BridgeV2,<br>l2|staple<br>**Sim**: SimplerEnv, LIBERO; **Real** (WidowX):<br>ikllh|
|TinyVLA [121] ♢|Poston Encong<br>ViT|Pythia|Diffusion<br>|Concat|cton Grs)<br>DDPM|Fracta, RH0T<br>OXE, [SC]|pc, pace, cose, pus<br>**Sim**: MetaWorld; **Real** (Franka, UR5): place,<br>l|
|CogACT [122] ♢|DINOv2, SigLIP|LLaMA 2|Policy<br>DiT|Concat|DDIM|OXE, [SC]|stack, flip mug, close drawer, open box<br>**Sim**: SimplerEnv; **Real** (Realman, Franka):<br>|
|DexVLA [123] ♢|ViT, ResNet-50|Qwen2-VL 2B,<br>|ScaleDP|Concat|DDPM|[SC]|pick, place, stack, open/close oven<br>**Real** (Franka, UR5e, AgileX): pick, fold shirt,<br>|
|HybridVLA [124] ♢|DINOv2, SigLIP,<br>CLIP|DistilBERT,<br>LLaMA 2, Phi-2|MLP|Concat|DDIM|OXE, DROID|bus table, pour<br>**Sim**: RLBench; **Real** (Franka, AgileX): pick-<br>laceouroendrawerfoldetc|
|LAPA [125] ♢|C-ViViT, VQ-GAN|LWM-Chat-1M|MLP|Concat|LAPA|OXE, BridgeV2,<br>SomethinV2|p, p, p , , .<br>**Sim**: Language-Table, SimplerEnv; **Real**<br>(Franka)ickcoerithtoelknockoer|
|WorldVLA [126] ♢|VQ-GAN|Chameleon|TFM|Quant.|BC (disc, chunk.),<br>|g <br>LIBERO,<br>|: p, v w w,  v<br>**Sim**: LIBERO|
|UniVLA[127]♢|MoVQ|Emu3|TFM|Quant|world model<br>BC(discchunk)|OpenVLA data<br>(Simbenchmark|**Sim**:CALVINLIBEROSimplerEnv|
|||||.|, .,<br>world model|<br>data)|, ,|


IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

9 

of Transformer architecture as its policy backbone. 

Gato [18] proposes a model that can play Atari games, caption images, and stack blocks, all with a single set of model parameters. This achievement is facilitated by a unified tokenization scheme, harmonizing the input and output across diverse tasks and domains. Consequently, Gato enables the simultaneous training of different tasks. Astra [128] optimizes this architecture via trajectory attention. 

RoboCat [95] proposes a self-improvement process designed to enable an agent to rapidly adapt to new tasks with as few as 100 demonstrations. This self-improvement process iteratively finetunes the model and self-generates new data with the finetuned model. Built upon the Gato model, RoboCat incorporates the VQ-GAN image encoder. During training, RoboCat predicts not only the next action but also future observations. The effectiveness of the self-improvement process is demonstrated through comprehensive experiments conducted in both simulated and real-world environments under multitask and multiembodiment settings. 

RT-1 [97], developed by the same team as BC-Z, shares similarities with BC-Z but introduces some key distinctions. Notably, RT-1 employs a vision encoder based on the more efficient EfficientNet, departing from BC-Z’s use of ResNet. However, RT-1 does not use video as a task instruction. In addition, RT-1 replaces the MLP action decoder in BC-Z with a Transformer decoder, producing discretized actions. This modification enables RT-1 to attend to past images, enhancing its performance compared with BC-Z. 

Q-Transformer [98] extends RT-1 by introducing autoregressive Q-functions. In contrast to RT-1, which learns expert trajectories through imitation learning, Q-Transformer adopts Q-learning methods. Alongside the TD error objective of Q- learning, a conservative regularizer is incorporated to ensure that the maximum value action remains in-distribution. This approach allows Q-Transformer to leverage not only successful demonstrations but also failed trajectories for learning. 

RT-Trajectory [99] adopts trajectory sketches as policy conditions instead of relying on language conditions or goal conditions. These trajectory sketches consist of curves that delineate the intended trajectory for the robot end-effector to follow. They can be manually specified through a graphical user interface, extracted from human demonstration videos, or generated by foundation models. RT-Trajectory’s policy is built upon the backbone of RT-1 and trained to control the robot arm to accurately follow the trajectory sketches. This approach facilitates generalization to novel objects, tasks, and skills, as trajectories from various tasks are transferable. 

ACT [100] builds a conditional VAE policy with action chunking, requiring the policy to predict a sequence of actions rather than a single one. During inference, the action sequence is averaged using a method called temporal ensembling. RoboAgent [101] extends ACT via MT-ACT, demonstrating that action chunking improves temporal consistency. It also introduces an inpainting-based semantic augmentation method. 

RoboFlamingo [102] adapts the OpenFlamingo VLM to a robot policy by attaching an LSTM-based policy head. This demonstrates that pretrained VLMs can be effectively transferred to language-conditioned robotic manipulation tasks. 

A recent trend in LLMs is equipping them with tool-use capabilities by generating code that calls tools via APIs [129]. Instruct2Act [105] follows this paradigm by integrating vision and action tools, enabling LLMs to perform robotic tasks. 

_3) Control Policies for Multimodal Instructions:_ Multimodal instruction enables new ways to specify tasks, such as through demonstrations, by naming novel objects, or by pointing with a finger or mouse click. 

VIMA [130] places a significant emphasis on multimodal prompts and the generalization capabilities of models. By incorporating multimodal prompts, more specific and intricate tasks can be formulated compared with pure text prompts. VIMA introduces six main types of tasks: object manipulation, visual goal reaching, novel concept grounding, one-shot video imitation, visual constraint satisfaction, and visual reasoning. These tasks are often challenging or even infeasible to express using only language prompts. VIMA-Bench has been developed to evaluate across four generalizability levels: placement, novel combinatorial, novel object, and novel task. 

MOO [96] extends RT-1 to handle multimodal prompts. Leveraging the backbone of RT-1, it incorporates OWL-ViT to localize target objects specified by the prompt. By expanding the RT-1 dataset with new objects and additional prompt images, MOO enhances the generalization capabilities of RT1. This extension also facilitates new methods of specifying target objects, such as pointing with a finger and clicking on graphical user interfaces. 

_4) Control Policies with 3D Vision:_ In our 3D world, it is reasonable to assume that 3D vision provides richer information than 2D images. 

Point clouds are a common representation for 3D visual inputs due to their straightforward derivation from RGB-D inputs, as demonstrated by both DP3 [108] and 3D Diffuser Actor [111]. Voxels have likewise been extensively studied. VER [131] proposes voxelizing multiview images into 3D cells in a coarse-to-fine manner, enhancing performance in visionlanguage navigation tasks. PerAct [90] facilitates efficient task learning with only a few demonstrations by leveraging voxel representations in both the observation and action spaces. The input comprises voxel maps reconstructed from multiview RGB-D images, while the output corresponds to the best voxel for guiding the gripper’s movement. RoboUniView [103] improves performance by injecting 3D information from multiperspective images through a novel UVFormer vision encoder, which is pretrained on a 3D occupancy task. 

In contrast, Act3D [91] introduces a continuous resolution 3D feature field, with adaptive resolutions based on the current task, addressing the computational cost of voxelization. RVT, RVT-2 [92], [93] propose re-rendering images from virtual views of the scene point cloud and using these images as inputs, rather than directly relying on 3D inputs. 

_5) Diffusion-Based Control Policies:_ Diffusion-based action generation leverages the success of diffusion models in the field of CV. 

Diffusion Policy [107] formulates a robot policy as a DDPM. This approach incorporates a variety of techniques, including receding horizon control, visual conditioning, and the time-series diffusion Transformer. The effectiveness of this 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

10 


Fig. 5. Representative architectures of VLA models. Some correspond to the “Architecture” column in Table III. _⊙_ : Hadamard product. _⊕_ : Concatenation. 

diffusion-based visuomotor policy is underscored by its proficiency in multimodal action distributions, high-dimensional action spaces, and training stability. 

SUDD [109] presents a framework where an LLM guides data ~~g~~ eneration, and subsequently, the filtered datas ~~et~~ is distilled <u>into</u> a <u>visuo-linguo-motor</u> policy. This framework achieves language-guided data generation by <u>composing</u> an LLM with a suite of primitive robot utilities, such as grasp samplers and motion planners. It then extends Diffusion Policy by incorporating language-based conditioning for multitask learning and facilitates the distillation of the filtered dataset. 

Octo [110] introduces a Transformer-based diffusion policy characterized by a modular open-framework design, allowing for the flexible integration of different task definition encoders, observation encoders, and action decoders with the <u>Octo</u> Transformer. Being among the first to utilize the OXE dataset [115], Octo demonstrates positive transfer and generalizability across diverse robots and tasks. 

MDT [112] builds a variant of the DiT model from CV for the action prediction head. Originally proposed as a Transformer-based diffusion model, DiT replaced the classical U-Net architecture in image generation. Coupled with two auxiliary objectives—masked generative foresight and contrastive latent alignment—MDT similarly demonstrates better performance than prior U-Net-based diffusion models. 

RDT-1B [113] is a diffusion-based foundation model for bimanual manipulation, also built on DiT. It addresses data scarcity by introducing a physically interpretable unified action format across various robots, enabling pretraining on heterogeneous multirobot datasets with over 1M trajectories. This allows RDT to scale up to 1.2B parameters and demonstrate zero-shot generalization. 

_6) Diffusion-Based Control Policies with 3D Vision:_ Several works have proposed combining 3D vision with diffusionbased policies. DP3 [108] introduces 3D point cloud inputs to a diffusion policy. Similarly, 3D Diffuser Actor [111] shares the core idea of DP3 but differs in model architecture by combining Act3D with Diffusion Policy. 3D-MoE [132] 

explores an efficient mixture-of-experts architecture with DiTbased action diffusion using a rectified flow framework. 

_7) Control Policies for Motion Planning:_ Motion planning involves decomposing movement tasks into discrete waypoints while satisfying constraints such as obstacle avoidance and kinematic limits. 

The _language costs_ framework [87] presents a novel approa ~~ch~~ to r ~~ob~~ ot correction using natural language for humanin-the-loop control. This method leverages predicted cost maps generated from human instructions, which are then utilized by the motion planner to compute the optimal path. This framework enables users to correct goals, specify preferences, or recover from errors through intuitive language commands. 

VoxPoser [106] employs an LLM and a VLM to create 3D voxel maps that represent affordances and constraints. It leverages the programming capability of LLMs and the perception capability of VLMs. The LLM translates language instructions into executable code, invoking the VLM to obtain object coordinates. Based on the composed affordance and constraint maps, VoxPoser employs model predictive control to generate a feasible trajectory for the robot arm’s end-effector. Notably, VoxPoser does not require any training, as it directly connects LLMs and VLMs for motion planning. 

RoboTAP [133] breaks down demonstrations into stages marked by the opening and closing of the gripper. In each stage, RoboTAP uses the TAPIR algorithm to detect active points that track the relevant object from the source to the target pose. These tracked points are then used by a visual servoing controller to guide the robot. A motion plan is created by chaining these stages together, enabling few-shot visual imitation. 

_8) Control Policies with Point-Based Actions:_ Recent research has explored leveraging the capabilities of VLMs to select or predict point-based actions—a cost-effective alternative to building full VLAs. 

PIVOT [134] casts robotics tasks as a VQA problem, leveraging VLMs to select the best robot action from a set of visual proposals. Visual proposals are annotated in the form 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

11 

of keypoints on images. The VLM is iteratively prompted to refine them until the best option is identified. 

RoboPoint [94] finetunes a VLM on the task of spatial affordance prediction, in which the model outputs 2D points indicating where to act on the image. These affordance points are subsequently projected into 3D space using depth maps, forming the predicted robot action. 

ReKep [36] introduces constraint functions that map 3D keypoints in the scene to a numerical cost. Robotics manipulation tasks can be represented as a sequence of these constraints, which are generated by large vision models and VLMs. Consequently, robot actions can be obtained by solving the resulting constrained optimization problem. 

_9) Large VLA:_ Large VLA is equivalent to the original VLA definition proposed by RT-2 [1], as illustrated in Fig. 2(a). This terminology is analogous to the distinction between LLMs and general language models, or between large VLMs and general VLMs. 

RT-2 [1] leverages the capabilities of large multimodal models for robotics tasks, building upon architectures like PaLI-X and PaLM-E (see the architecture in Fig. 5(e)). The approach introduces a co-fine-tuning strategy, jointly training the model on Internet-scale VQA data and robot data. This training scheme enhances the model’s generalizability and enables emergent capabilities. 

RT-H [114] introduces an action hierarchy that includes an intermediate prediction layer of language motions, situated between language instructions and low-level actions (translation and rotation). This additional layer facilitates improved data sharing across different tasks. For example, both the language instructions “pick” and “pour” may involve the language motion “move the arm up”. Moreover, this action hierarchy enables users to specify corrections to recover from failures, from which the model can subsequently learn. 

RT-X [115] builds upon the previous RT-1 and RT-2 models. These models are retrained using a newly introduced opensource dataset named open X-embodiment (OXE), which is orders of magnitude larger than previous datasets. The resulting models, RT-1-X and RT-2-X, both outperform their original versions. 

OpenVLA [35] was later developed as an open-source counterpart to RT-2-X. It additionally explored efficient finetuning methods, including LoRA and model quantization. OpenVLAOFT [116] applies an Optimized Fine-Tuning (OFT) recipe for improved efficiency and performance. TraceVLA [117] finetunes OpenVLA to enable visual trace prompting, enhancing the model’s spatial-temporal awareness. 

_π_ 0 [118] proposes a flow-matching architecture for transforming VLMs into VLAs. By incorporating an additional action expert based on the mixture-of-experts framework (see the architecture in Fig. 5(f)), it effectively inherits the Internetscale knowledge of the base VLM while extending its capabilities to address robotic tasks. 

RoboMamba [119] replaces the computationally expensive Transformer architecture with a Mamba state space model featuring linear inference complexity, thereby achieving efficient robotic reasoning and action capabilities. 

SpatialVLA [120] introduces Ego3D position encoding for injecting 3D information and represents actions with adaptive action grids for enhanced generalizability and robustness. 

LAPA [125] devises the first unsupervised pretraining method for VLAs based on latent actions [69]. This approach employs a three-stage process to learn from Internet-scale unlabeled videos. First, a VQ-VAE framework is pretrained to extract quantized latent actions between image frames. Next, a VLA model is pretrained to predict these latent actions. Finally, the model is finetuned using only a small robotic dataset to map the latent actions to actual robot actions. 

The integration of LVLAs with diffusion has also been gaining popularity. TinyVLA [121] leverages Diffusion Policy, while CogACT [122] utilizes a DiT action diffusion module. DexVLA [123] proposes embodied curriculum learning to progressively train a diffusion action expert, incorporating substep reasoning for decomposing long-horizon tasks. HybridVLA [124] integrates diffusion with the autoregressive paradigm to fully leverage VLMs’ reasoning capabilities. 

GR00T N1 [135] introduces a dual-system architecture to build a robot foundation model for humanoid robots (see the architecture in Fig. 5(g)). Its VLM-based System 2 processes image observations and language instructions at 10 Hz, while System 1 is a diffusion module that generates closed-loop motor actions in real time (120 Hz). 

NORA-1.5 [136] unifies a VLA with a world model through reward-guided post-training. Genie Envisioner [137] is a world foundation platform that integrates a world model and a VLA within a single video-generative framework. See the general architecture in Fig. 5(h). 

Visual autoregressive (VAR) modeling [138] with quantized visual tokens demonstrates improved performance over diffusion models in image generation. This suggests that the three modalities of VLAs can be unified under the autoregressive paradigm [139]. WorldVLA [126] and UniVLA [127] advance this direction by integrating VLAs with world models (see the architecture in Fig. 5(i)). They quantize multimodal data into discrete tokens, forming a shared vocabulary of quantized multimodal tokens. Consequently, all modalities can be modeled autoregressively, enabling not only action and text generation but also image generation, thereby constituting a world model. _10) Strengths and Limitations:_ 

_a) Architectures:_ Representative VLA architectures are illustrated in Fig. 5. FiLM is used in RT-1, and thus its followup models inherit this mechanism. While cross-attention may offer superior performance with smaller model sizes, concatenation is simpler to implement and can achieve comparable results with larger models [130]. Quantization unifies multimodal tokens into a shared vocabulary, thus enabling integration with world models. The tool-use paradigm of LLMs can also be applied to robotic tasks. 

_b) Action Types and Their Training Objectives:_ Most low-level control policies predict actions for the end-effector pose while abstracting away the motion planning module that produces more fine-grained motions. While this abstraction facilitates better generalization to different embodiments, it also imposes limitations on dexterity. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

12 

Table IV 

HIGH-LEVEL TASK PLANNERS 

|**Model**|**Vision**<br>**Model**|**Language Model /**<br>**VLM**|**Low-level Control**<br>**Policy**|**Architecture**|**Require**<br>**Training**|**Environments, Embodiments, Tasks, and**<br>**Skills**|
|---|---|---|---|---|---|---|
|PaLM-E [11]|ViT, OSRT|PaLM|Interactive Language,<br>RT-1|Concat|✓|**Sim**: TAMP; **Sim&Real-Mani**: Language-<br>Table; **Real**: SayCan setup|
|EmbodiedGPT [140]|EVA ViT-G/14|LLaMA-7B|MLP|Xattn|✓|**Sim-Mani**: Franka Kitchen, Meta-World|
|LEO [141]|ConvNeXt, PointNet++|Vicuna-7B|MLP|Concat|✓|**Sim-Mani**: CLIPort task subset; **Sim-Navi**:<br>Habitat-web|
|3D-LLM [42]|CLIP, 3D-CLR,<br>ConceptFusion|Flamingo, BLIP-2|DD-PPO|Concat|✓|**Sim-Navi**: Habitat|
|ShapeLLM [142]|ReCon++|LLaMA||Concat|✓|3D MM-Vet Benchmark|
|SayCan [10]||PaLM, FLAN|BC-Z, MT-Opt||✗|**Real-Navi&Mani** (EDR): office kitchen|
|Translated _⟨_LM_⟩_[143]<br>||GPT-3, Codex|||✗|**Sim**: VirtualHome|
|(SL)<sup>3</sup> [144]||T5-small|seq2seq||✓|**Sim-Navi**: ALFRED|
|Inner Monologue [9]|MDETR, CLIP|InstructGPT, PaLM|CLIPort, heuristics,<br>SayCan policies|Language|✗|**Sim&Real-Mani**: Tabletop Rearrangement;<br>**Real-Navi&Mani**: Kitchen Mobile Mani.|
|LLM-Planner [145]|HLSM object detector|GPT-3|HLSM|Language|✓|**Sim-Navi**: ALFRED|
|LID [146]|CNN|GPT-2||Lang., Embed|✓|**Sim**: VirtualHome|
|SMs [147]|CLIP, ViLD|GPT-3, RoBERTa|CLIPort|Lang., Code|✗|**Sim-Mani**: pick, place|
|ProgPrompt [148]|ViLD|GPT-3|API|Code|✗|**Sim**: VirtualHome|
|ChatGPT for Robotics<br>[149]|YOLOv8|ChatGPT|API|Code|✗|**Real-Navi**: drone flight; **Sim-Navi**: AirSim,<br>Habitat|
|CaP [150]|ViLD, MDETR|GPT-3, Codex|API|Code|✗|**Sim-Mani** & **Sim-Navi**: pick, place, etc.|
|DEPS [151]|CLIP|ChatGPT|MC-Controller, Steve-1|Code|✗|**Sim**: Minecraft|
|ConceptGraphs [152]|SAM, CLIP, LLaVA|GPT-4|API|Code (JSON)|✗|**Sim**: AI2-THOR; **Real** (Spot Arm): pick-place|


The BC objective is used in imitation learning, with different variants for different action types. The BC objective for continuous actions can be written as 


where MSE( _·_ ) stands for mean squared error, _at_ is the action annotation from expert demonstrations, and ˆ _at_ is the predicted action. 

Discrete actions are achieved by dividing the action value range into a fixed number of bins. Their BC objective is 


where CE( _·_ ) stands for cross-entropy loss. The BC objective for _SE_ (2) actions is 


The DDPM objective in diffusion-based control policies is 


where _a_<sup>_k_</sup> _t_<sup>istheaction</sup><sup>_at_corruptedbyrandomnoise</sup><sup>_εk_at</sup> diffusion iteration _k_ , and _εθ_ is the noise prediction network, i.e., the VLA model. 

While discrete action has demonstrated superior performance in RT-1 [97], Octo [110] argues that it leads to early grasping issues. _SE_ (2) actions require the model to predict only the pick pose and the place pose of the end-effector, which are sufficient for many tabletop manipulation tasks. However, more complex tasks—such as “pouring water into a cup”—may require additional DoFs, thereby necessitating _SE_ (3) actions [36]. Although point-based actions can be coarse-grained, they are more easily obtained from VLMs in a zero-shot manner. 

_c) RT Series:_ RT-1 [97] inspired a series of “Robotic Transformer” models. The Transformer backbone surpasses previous RNN backbones by harnessing the higher capacity of Transformers to absorb larger robot datasets. Preceding RT1 was BC-Z, which solely utilized MLP layers for action prediction. Subsequent to RT-1, several works emerged to introduce new capabilities. MOO adapted RT-1 to accommodate multimodal prompts. RT-Trajectory enabled RT-1 to process trajectory sketches as prompts. Q-Transformer utilized Q-learning to train RT-1. RT-2, based on ViT and LLM, introduced a completely different architecture from RT-1. RT-X retrained RT-1 and RT-2 with a significantly larger dataset, resulting in improved performance. Based on RT2, RT-H [114] introduced action hierarchies for better data sharing. 

_d) LVLA vs. Generalized VLA:_ While LVLAs can greatly enhance instruction-following abilities because they can better parse user intentions, concerns arise regarding their training cost and deployment speed. Slow inference speed, in particular, can significantly impact performance in dynamic environments, as changes in the environment may occur during inference. Therefore, several methods have been proposed to improve efficiency. TinyVLA [121] focuses on inference speed and data efficiency through a smaller VLM and diffusion head for robot action. DeeR-VLA [104] proposes only partially activating the model via early-exit dynamic inference. 

_e) Scaling Laws:_ As in LLMs, scaling laws have also been observed in robotics [153], [154], revealing the importance of model size, dataset size, and the diversity of environments and objects. Further research in this area can guide the development of VLAs with robust in-the-wild generalization capabilities. 


A high-level task planner _πϕ_ aims to decompose a complex task _ℓ_ into a sequence of subtasks **p** ˆ = [ _p_ 1 _, p_ 2 _, . . . , pN_ ] (i.e., a 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

13 

task plan), where each _pi_ serves as an instruction to low-level control policies _πθ_ : 


This process is sometimes referred to as task or subgoal decomposition and is closely related to task and motion planning (TAMP) and embodied decision making. When equipped with task planners, VLAs can complete more complex, longhorizon tasks, as illustrated in Fig. 4. Details are summarized in Table IV. Ideally, task plans should also incorporate optimal scheduling for these subtasks. 

## _A. Monolithic Task Planners_ 

A single LLM or multimodal LLM (MLLM) can typically generate task plans by employing a tailored framework or through finetuning on embodied datasets. We refer to these as _monolithic_ models. 

_1) End-to-End Task Planners:_ Similar to LVLAs, task planners can be implemented as end-to-end MLLMs, leveraging their Internet-scale knowledge for task planning. 

PaLM-E [11] integrates ViT and PaLM to create an embodied MLLM capable of performing high-level embodied reasoning tasks. Based on perceived images and high-level language instructions, PaLM-E generates a text plan that serves as instructions for low-level robotic policies. In a mobile manipulation environment, the generated plan is mapped to executable low-level instructions using SayCan [10]. As the low-level policy executes actions, PaLM-E can also replan based on changes in the environment. With PaLM as its backbone, PaLM-E can handle standard VQA tasks along with additional embodied VQA tasks. 

EmbodiedGPT [140] introduces the embodied-former, which outputs task-relevant instance-level features. This is achieved by incorporating vision encoder embeddings and embodied planning information provided by an LLM. These instance features serve to inform the low-level policy about the immediate next action to take. 

_2) End-to-End Task Planners with 3D Vision:_ Some task planners also explore the use of 3D vision. Because the majority of current MLLMs deal with images as visual inputs, they require architectural changes to incorporate 3D visual inputs. Consequently, they are usually end-to-end models. 

LEO [141] uses a two-stage training strategy to integrate a point cloud encoder with an LLM: the first stage focuses on 3D vision-language alignment, followed by the second stage of 3D vision-language-action instruction tuning. LEO performs well not only in 3D question-answering tasks but also in manipulation, navigation, and task planning. 

3D-LLM [42] injects 3D information into LLMs and empowers them to perform 3D tasks, such as 3D-assisted dialog and navigation, using features from point clouds, gradSLAM, and neural voxel fields. MultiPLY [155] is an object-centric embodied LLM that incorporates even more modalities, including audio, tactile, and thermal. 

ShapeLLM [142] is built on the novel 3D vision encoder ReCon++, which distills knowledge from multiview image and text teacher models, along with a point cloud MAE. 


Fig. 6. Different approaches to connect LLM to multimodal modules in modular task planners. 

By integrating ReCon++ with LLaMA, ShapeLLM improves embodied interaction performance on their newly proposed 3D benchmark, 3D MM-Vet. 

_3) Groun_ _~~ded Task~~ Planners:_ Grounded task planning involves generating high-level actions while considering whether they can be executed by low-level control policies. 

SayCan [10] is a framework designed to integrate highlevel LLM planners with low-level control policies. In this framework, the LLM planner accepts a user’s high-level instruction and “says” what the most probable next low-level skill is, a concept referred to as _task-grounding_ . The low-level policy provides the value function as the affordance function, determining the probability that the policy “can” complete the skill, known as _world-grounding_ . By considering both the LLM’s plan and the affordances, the framework selects the optimal skill for the current state. 

Translated _⟨_ LM _⟩_ [143] employs a two-step process to translate high-level instructions into executable actions. Initially, a pretrained causal LLM is utilized for _plan generation_ , breaking down the high-level instruction into the next action, expressed as a free-form language phrase. Then, as this phrase may not directly map to VirtualHome actions, a pretrained masked LLM is employed for _action translation_ . This step involves calculating the similarity between the generated action phrase and the admissible VirtualHome actions. The translated action is appended to the plan, and the updated plan is fed back into the LLM to generate the next action phrase. This twostep process is repeated until a complete plan is formed. A “re-prompting” strategy [156] is further proposed to generate corrective actions when the agent encounters precondition errors. 

(SL)<sup>3</sup> [144] is a learning algorithm that alternates between three steps: segmentation, labeling, and parameter update. In the segmentation step, high-level subtasks are aligned with low-level actions; subtask descriptions are then inferred in the labeling step; and finally, the network parameters are updated. This approach enables a hierarchical policy to discover reusable skills with sparse natural language annotations. 

## _B. Modular Task Planners_ 

Finetuning end-to-end models on embodied data can be expensive; therefore, some approaches adopt a modular design by assembling off-the-shelf LLMs and VLMs into task planners. These approaches can also be viewed as following the tool-use architecture [129]. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

14 

_1) Language-Based Task Planners:_ Language-based approaches use natural language descriptions as the medium for exchanging multimodal information, as shown in Fig. 6(a). 

Inner monologue [9] sits between high-level commands and low-level policies to enable closed-loop control planning. It employs an LLM to generate language instructions for lowlevel policies and dynamically updates these instructions based on the received feedback. The feedback encompasses various sources: success feedback, object and scene feedback, and human feedback. As the feedback is communicated to the LLM in a textual format, no additional training is required for the LLM. A similar approach is used in ReAct [76]. 

LLM-Planner [145] introduces a novel approach to constructing a hierarchical policy comprising a high-level planner and a low-level planner. The high-level planner harnesses the capabilities of an LLM to generate natural language plans, while the low-level planner translates each subgoal within the plan into primitive actions. While sharing similarities with previous methods in its overall architecture, LLM-Planner distinguishes itself by incorporating a re-planning mechanism, enabling the robot to “get unstuck”. 

LID [146] introduces a novel data collection procedure termed active data gathering (ADG). A key aspect of ADG is hindsight relabeling, which reassigns labels to unsuccessful trajectories, effectively maximizing the utilization of data irrespective of trajectory success. By converting all environmental inputs into textual descriptions, the proposed language-modelbased policy gains enhanced combinatorial generalization. 

Socratic models (SMs) [147] present a unique framework wherein diverse pretrained models are effectively composed without the need for finetuning. The framework relies on a key mechanism called multimodal-informed prompting, which facilitates information exchange among models with varied multimodal capabilities. The idea is to utilize multimodal models to convert non-language inputs into language descriptions, effectively unifying different modalities within the language space. Beyond excelling in conventional multimodal tasks, SMs showcase their versatility in robot perception and planning. In addition to natural language plans, task plans can also be represented in the form of pseudocode. 

_2) Code-Based Task Planners:_ Code-based task planners leverage the coding ability of LLMs to generate task plans in the form of executable programs. Object detectors, VLMs, and control policies can be invoked via APIs, as shown in Fig. 6(b). 

ProgPrompt [148] introduces a novel task-planning approach by prompting LLMs with program-like specifications detailing available actions and objects. This enables LLMs to generate high-level plans for household tasks in a few-shot manner. Environmental feedback can be incorporated through assertions within the program. 

ChatGPT for robotics [149] takes advantage of the programming ability of ChatGPT to facilitate “user on the loop” control, a departure from the conventional “engineer in the loop” methodology. The procedure includes several steps. First, a list of APIs is defined, such as an object-detection API, a grasp API, and a move API. Second, a prompt is constructed for ChatGPT, specifying the environment, API functionality, 

Table V 

EMBODIED DATASETS. PER RT-X, SKILLS CORRESPOND TO VERBS, AND TASKS ARE DIFFERENT COMBINATIONS OF VERBS AND OBJECTS. _∗_ DATASET COLLECTED IN SIMULATION RATHER THAN THE REAL WORLD. SOME DATASETS ARE CONTINUALLY UPDATED, AND WE INCLUDE ONLY THE ORIGINAL VERSION. TABLE ADAPTED FROM [158], [159] 

|**Dataset**|**Skills **|**Tasks **|**Scene**|**s Episodes **|**Collection**|**Obs.**|**Instruction**|**Robots**|
|---|---|---|---|---|---|---|---|---|
|MIME [160]|12|20|1|8.3K|Human teleop.|RGBD|Demo|Baxter|
|_∗_RoboTurk [161]|2|3|1|2.1K|Human teleop.|RGB||Sawyer|
|RoboNet [162]|||10|162K|Script|RGB|Goal image|(7 robots)|
|MT-Opt [163]|2|12|1|800K|Script, RL|RGB|Task ID|(7 robots)|
|BC-Z [82]|3|100|1|25.9K|Human teleop.|RGB|Lang, demo|EDR|
|Fractal [97]|12|700+|2|130K|Human teleop.|RGB|Lang|EDR|
|MOO [96]|5|||59.1K|Human teleop.|RGB|Multimodal|EDR|
|_∗_VIMA [130]|17||1|650K|Script|RGB|Multimodal|UR5|
|RoboSet [164]|12|38|11|98.5K|Human, script|RGBD|Lang|Franka|
|BridgeV2 [165]|13||24|60.1K|Human, script|RGB(D)|Lang|WidowX|
|RH20T [158]|42|147|7|110K+|Human teleop.|RGBD|Lang|(4 robots)|
|DROID [159]|86||564|76K|Human teleop.|RGBD|Lang|Franka|
|OXE [115]|527|160K|311|1M+|Aggregate data|RGBD|Lang|(22 robots)|


and task goal. Third, ChatGPT is iteratively prompted to write code utilizing the defined APIs to execute the task, provided access to simulation and user feedback for evaluating code quality and safety. Finally, the ChatGPT-generated code is executed. In this procedure, ChatGPT serves as a high-level task planner, and actions are generated through function calls to corresponding low-level APIs. 

Code as policies (CaP) [150] also leverages the codewriting capability of LLMs. It employs GPT-3 or Codex to generate policy code, which, in turn, invokes perception modules and control APIs. CaP exhibits proficiency in spatialgeometric reasoning, generalization to new instructions, and parameterization for low-level control primitives. By leveraging the multimodal capabilities of GPT-4V, COME-robot [157] eliminates the need for perception APIs required by CaP. This opens up possibilities for open-ended reasoning and adaptive planning within a closed-loop framework, enabling capabilities such as failure recovery and free-form instruction following. 

DEPS [151] stands for “describe, explain, plan, and select.” This approach employs an LLM to generate plans and explain failures based on feedback descriptions collected from the environment—a process referred to as “self-explanation,” which aids in replanning. In addition, DEPS introduces a trainable goal selector to choose among parallel candidate subgoals based on how easily they can be achieved, a crucial aspect often overlooked by other high-level task planners. 

ConceptGraphs [152] introduces a method to convert observation sequences into open-vocabulary 3D scene graphs. Objects are extracted from RGB images using 2D segmentation models, and VLMs are employed to caption objects and establish inter-object relations, resulting in the construction of a 3D scene graph. This graph can then be translated into a text description (JSON), providing LLMs with rich semantic and spatial relationships between entities for task planning. 

## _C. Strengths and Limitations_ 

_Monolithic_ task planners that utilize grounded task planning focus on generating executable plans. End-to-end models share an architecture similar to most LVLAs and can be finetuned on specialized embodied data to achieve better performance. However, the training costs of such large models are often substantial. In contrast, _modular_ task planners are more readily 

15 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

Table VI 

SIMULATORS AND SIMULATED BENCHMARKS. CONTROL: CONTINUOUS CONTROL TASKS. D, S, A, N: DEPTH, SEGMENTATION, AUDIO, NORMAL. FORCE: SIMULATED CONTACT FORCE BETWEEN END-EFFECTOR AND ITEM. PD: PRE-DEFINED. TABLE ADAPTED FROM [166], [167] 

|**Name**|**Scenes**<br>**/Rooms**|**Objects**<br>**/Cat**|**UI**|**Physics**<br>**Engine**|**Task**|**Observation**|**Action**|**Agent**|**Description**|**Related**|
|---|---|---|---|---|---|---|---|---|---|---|
|Gibson [168]|572/-|||Pybullet|Navi|RGB, D, N, S|||Navi only||
|iGibson [167], [169],<br>[170]|15/108|152/5|Mouse,<br>VR|Pybullet|Navi, Mani|RGB, D, S, N,<br>Flow, LiDAR|Force|TurtleBot v2,<br>LoCoBot, etc.|VR, Continuous Extended States.<br>Versions: 0.5, 1.0, 2.0|Benchmarks: BEHAVIOR-100<br>[166], BEHAVIOR-1K [171]|
|SAPIEN [172]||2346/-|Code|PhysX|Navi, Mani|RGB, D, S|Force|Franka|Articulation, Ray Tracing|VoxPoser. Benchmark: SIMPLER<br>[173]|
|AI2-THOR [174]|-/120|118/118|Mouse|Unity|Navi, Mani|RGB, D, S, A|Force, PD|ManipulaTHOR,<br>LoCoBot, etc.|Object States, Task Planning.<br>Versions: [175], [176]|Benchmarks: ALFRED, RoPOR<br>[177]|
|VirtualHome [178]|7/-|-/509|Lang|Unity|Navi, Mani|RGB, D, S|Force, PD|Human|Object States, Task Planning|LID, Translated〈LM〉, ProgPrompt|
|TDW [179]|15/120|112/50|VR|Unity,<br>Flex|Navi, Mani|RGB, D, S, A|Force|Fetch, Sawyer,<br>Baxter|Audio, Fluids||
|RLBench [180]|1/-|28/28|Code|V-REP|Mani|RGB, D, S|Force|Franka|Tiered Task Difficulty|Hiveformer, PerAct|
|Meta-World [181]|1/-|80/7|Code|MuJoCo|Mani|Pose|Force|Sawyer|Meta-RL|R3M, VC-1, Vi-PRoM,<br>EmbodiedGPT|
|CALVIN [182]|4/-|7/5||Pybullet|Mani|RGB, D|Force|Franka|Long-horizon Lang-cond tasks|GR-1, HULC, RoboFlamingo|
|Franka Kitchen [183]|1/-|10/6|VR|MuJoCo|Mani|Pose|Force|Franka|Extended by R3M with RGB|R3M, Voltron, Vi-PRoM,<br>Diffusion Policy, EmbodiedGPT|
|Habitat [184], [185]|(Matterp|ort + Gibson)|Mouse|Bullet|Navi|RGB, D, S, A|Force|Fetch, Franka,<br>AlienGO|Fast, Navi only. Versions: 1.0,<br>2.0, Rearrangement [186]|VC-1, PACT; Benchmark:<br>OVMM [187]|
|ALFRED [188]|-/120|84/84||Unity|Navi, Mani|RGB, D, S|PD|Human|Diverse long-horizon tasks|(SL)<sup>3</sup>, LLM-Planner|
|DMC [189]|1/-|4/4|Code|MuJoCo|Control|RGB, D|Force||Continuous RL|VC-1, SMART|
|OpenAI Gym [190]|1/-|4/4|Code|MuJoCo|Control|RGB|Force||Single agent RL environments||
|Genesis [191]|(Rigid, d<br>liquid, et|eformable,<br>c.)|Code|(Custom)|Navi, Mani|RGB, D, S, N|Force|Franka, Unitree,<br>etc.|High-speed comprehensive<br>physics simulation||


deployable because they leverage off-the-shelf LLMs and VLMs. Language-based task planners offer the advantage of seamless integration of LLMs and VLMs, as they are designed to operate in the natural language space. However, they often require extra steps to align the generated task plans with language instructions that are admissible to low-level control policies. Conversely, while code-based task planners may require manually wrapping VLMs and control policies within APIs and preparing clear documentation in advance, they enable code debugging and provide greater controllability. Ultimately, their performance remains constrained by the programming capabilities of the underlying models. 

## V. DATASETS AND BENCHMARKS 

## _A. Real-World Robot Datasets & Benchmarks_ 

Embodied AI faces significant data scarcity issues because real-world robot data are not as readily available as language data. Collecting real-world robot datasets poses multiple challenges. First, the process is impeded by the cost and time required to procure robotic equipment, set up environments, and gather expert data through dedicated policies or human teleoperation. Second, the diverse types and configurations of robots introduce inconsistencies in factors such as sensory data, control modes, and gripper types. Finally, accurately capturing 6D object poses and reproducing setups remain elusive. We summarize recent embodied datasets in Table V. In addition, real-world benchmarks are further complicated by the need for human evaluation. 

causes of this gap are multifaceted, encompassing unrealistic rendering quality, inaccuracies in physics simulations, and domain shifts characterized by object properties and robot motion planners. For instance, simulating non-rigid entities such as deformable objects or liquids presents significant difficulties. Moreover, importing new objects into simulators requires considerable effort, often involving techniques such as 3D scanning and mesh editing. Despite these hurdles, simulated environments provide automated evaluation metrics that aid researchers in consistently evaluating robotic models. Many benchmarks are based on simulators because they can precisely reproduce the experimental setup and yield fair comparisons of different models. Another technique, known as real-to-sim, can improve simulation fidelity, recreate failure cases, or facilitate digital twins. 

## _C. Automated Dataset Collection_ 

Several approaches advocate for automated dataset collection. RoboGen [192] employs a generative simulation paradigm that proposes interesting skills, simulates corresponding environments, and selects optimal learning approaches to train policies for acquiring those skills. AutoRT [193] functions as a robot orchestrator driven by LLMs, generating tasks, filtering them by affordance, and utilizing either autonomous policies or human teleoperators to collect and evaluate data. DIAL [194] focuses on augmenting language instructions in existing datasets using VLMs. RoboPoint [94] generates scenes procedurally with randomized 3D layouts, objects, and camera viewpoints. 

## _B. Simulators, Simulated Robot Datasets & Benchmarks_ 

Many researchers resort to simulated environments to circumvent real-world obstacles and scale the data collection process. We compare simulators and simulated benchmarks in Table VI. Nevertheless, this strategy presents its own challenges, chief among which is the sim-to-real gap. This discrepancy arises when models trained on simulated data exhibit poor performance during real-world deployment. The 

## _D. Human Datasets_ 

An alternative strategy to address data scarcity in realworld settings is to leverage human data. Human behavior offers plentiful guidance for robot policies due to its dexterity and diversity [195]. However, this strategy also comes with inherent limitations. Capturing and transferring human hand and body motions to robot embodiments is difficult. Moreover, the inconsistency in human data poses a hurdle, as some 

16 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

Table VII 

EMBODIED QUESTION ANSWERING BENCHMARKS. EXPLORE: ACTIVE EXPLORATION 

|**Benchmark**|**QA Pairs**|**Scenes**|**Source**|**Answer Type**|**Collection**|**Explore**|**Metrics**|
|---|---|---|---|---|---|---|---|
|EQA [203]|5K|750 envs|House3D simulator|Answer set (172 answers)|Template|✓|Accuracy|
|IQUAD [204]|75K|30 rooms|AI2-THOR|Multiple choice|Template|✓|Accuracy|
|MT-EQA [205]|19.3K|588 envs|House3D simulator|Binary answer|Template|✓|Accuracy|
|MP3D-EQA [206]|1,136|83 envs|MatterPort3D|Answer set (53 answers)|Template|✓|Accuracy|
|EgoVQA [207]|600|16 videos|IU Multi-view|Multiple choice (1 out of 5)|Human annotators|✗|Accuracy|
|EgoTaskQA [208]|40K|2K videos|LEMMA dataset|Open answer, binary verification|Human annotators & template|✗|Accuracy|
|EQA-MX [209]|8.2M|750K images|CAESAR simulator|Answer set|Question templates, answer set|✗|Accuracy|
|OpenEQA [210]|557 + 1079|180 envs|HM3D + ScanNet|Open answer|Human annotators|✗|LLM Score|


data are egocentric while others are captured from thirdperson perspectives. In addition, filtering human data to extract useful information can be labor-intensive. These obstacles underscore the complexities involved in incorporating human data into robot learning processes. UMI [196] proposes a method to mitigate these issues using hand-held grippers. For a more comprehensive comparison of human datasets, we refer interested readers to [197]. 

## _E. Task Planning Benchmarks_ 

EgoPlan-Bench [198] focuses on benchmarking real-world task planning with human annotations. PlanBench [199], [200] comprehensively assesses various aspects of task planning ability, such as cost optimality, plan verification, and replanning. LoTa-Bench [201] directly evaluates task planning by executing the generated plans in simulators and calculating success rates. Embodied agent interface (EAI) [202] argues that this approach fails to pinpoint issues in LLMs. By formalizing the input-output of LLM-based modules for decisionmaking tasks, EAI enables more fine-grained metrics beyond success rates. 

## _F. Embodied Question Answering (EQA) Benchmarks_ 

EQA benchmarks, as summarized in Table VII, do not directly evaluate robotic tasks like manipulation and navigation, but instead target other relevant abilities for embodied AI, such as spatial reasoning, physics understanding, and world knowledge. EQA is akin to traditional VQA benchmarks, but differs in that the agent can actively explore the environment before providing an answer. EmbodiedQA [203] and IQUAD [204] were among the first works to introduce this type of benchmark. MT-EQA [205] focuses on complex questions involving multiple targets. MP3D-EQA [206] converts previous RGB inputs to point clouds, testing 3D perception capabilities. Active exploration requires access to a simulator, thereby restricting the ability to utilize real-world data. EgoVQA [207] shifts the focus of VQA to egocentric videos. EgoTaskQA [208] emphasizes spatial, temporal, and causal relationship reasoning. EQA-MX [209] investigates multimodal expressions (MXs), including regular verbal utterances and nonverbal gestures like eye gaze and pointing. OpenEQA [210] evaluates seven main categories, including functional reasoning and world knowledge. 

## VI. CHALLENGES AND FUTURE DIRECTIONS 

_a) Safety First:_ Safety is paramount in robotics, as robots interact directly with the physical world. Ensuring the 

safety of robotic systems requires the integration of real-world commonsense. This involves the incorporation of robust safety guardrails, risk assessment frameworks, and human-robot interaction protocols. RLHF and “evaluation without execution” can also significantly lower safety risks [20]. Interpretability and explainability of VLA decision-making processes are also crucial for enhancing robot safety through error diagnosis and troubleshooting. 

_b) Datasets & Benchmarks:_ In addition to the issues discussed in Section V, comprehensive benchmarks that cover a wide range of skills, objects, embodiments, and environments remain to be developed. Moreover, metrics beyond the success rate are needed for a fine-grained diagnosis of issues in VLA models, as highlighted by EAI [202] for LLMs. 

_c) Foundation Models & Generalization:_ VLA foundation models or robotic foundation models (RFMs) for embodied AI remain an open research topic primarily due to the diversity in embodiments, environments, and tasks. Many have made significant progress [113], [118], but still lack generalization capability on par with LLMs in NLP. Attaining such a level of generalization is very challenging, as it requires the development of many core AGI capabilities. 

_d) Multimodality:_ VLAs inherit many challenges associated with multimodal models, such as obtaining useful embeddings and aligning different modalities. Current approaches, like ImageBind [211] and LanguageBind [212], align different modalities to the image or language embedding space, respectively. Within a unified embedding space, MLLMs can accommodate diverse modalities and become more general. However, whether focusing on embeddings alone is sufficient remains under debate. Although beyond the scope of VLAs, other modalities—such as audio [45], haptics [213], and gaze [214]—have proven useful for certain embodied AI applications. For instance, modeling human gaze data using an additional gaze network [215] or incorporating it via an auxiliary loss [216] has been shown to enhance the performance of the primary policy network. These approaches demonstrate that RL policies can benefit from human-like visual attention, as human gaze often reveals the most salient locations in the environment [217]. While incorporating additional modalities is often advantageous, it inevitably introduces extra complexity into the model design. 

_e) Framework for Long-Horizon Tasks:_ The hierarchical framework is currently the most practical approach for longhorizon tasks. However, it increases system complexity and potential points of failure. Frequent task execution failures can trigger replanning, which can cause significant latency. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

17 

Moreover, monolithic task planners share similar architectures with LVLAs, so employing two large models can be redundant and may hinder scalability. In addition, although modular task planners typically do not require training, they are not plugand-play: language-based models may generate subtasks that control policies cannot execute, whereas code-based models require modules to be prewrapped in APIs manually. Therefore, developing a unified framework that directly translates long-horizon tasks into low-level control signals in an end-toend fashion is worth exploring. 

_f) Real-Time Responsiveness:_ Unlike conversational AI, many robotic applications require real-time decision-making to respond to dynamic environments. If inference time cannot keep pace with environmental changes, the model may generate obsolete actions repeatedly. However, current VLA models—especially LVLAs and task planners—face a tradeoff between speed and capacity. Novel mechanisms are thus needed to strike an optimal balance. 

_g) Multiagent Systems:_ Cooperative multiagent systems offer benefits such as distributed perception and collaborative fault recovery. However, they also face challenges, including effective communication, coordinated dispatching, and fleet heterogeneity. In certain scenarios, individual agents may have conflicting goals, which further increases complexity. 

_h) Ethical and Societal Implications:_ Robotics has always raised various ethical, societal, and legal concerns. These include risks related to privacy, job displacement, decisionmaking bias, and the impact on social norms and human relationships. 

_i) Applications:_ Most current VLAs focus on household or industrial settings, but a wider range of applications is possible, such as virtual assistants, autonomous vehicles, and agricultural robots. Various embodiments may also call for specialized VLAs, including dexterous hands, drones, quadruped robots, and humanoid robots. One particularly important field is healthcare, encompassing surgical robots [218] and care robots [219]. Healthcare demands higher safety and privacy standards and may necessitate novel techniques such as human-in-the-loop (HITL) control and federated learning. Moreover, due to the significant domain gap, specialized vision models might be needed for medical images. 

## VII. CONCLUSION 

VLA models hold immense promise for enabling embodied agents to interact with the physical world and fulfill user instructions. This article is the first survey to review LVLAs alongside generalized VLAs. Our taxonomy provides a highlevel overview of three main lines of research: key components, control policies, and task planners. We meticulously analyze and compare their technical details, including model architectures, training strategies, and individual modules. In addition, we highlight essential resources for training and evaluating VLAs, such as datasets, simulators, and benchmarks. We hope this survey captures the rapidly evolving landscape of embodied AI and inspires future research. 

## ACKNOWLEDGMENTS 

This work was supported by the Research Grants Council of the Hong Kong Special Administrative Region, China, CUHK 2300246 (RGC C1043-24G), CUHK 7010870, and CUHK 6906061. 

## REFERENCES 

- [1] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, X. Chen, K. Choromanski, T. Ding, D. Driess, A. Dubey, C. Finn, P. Florence, C. Fu, M. G. Arenas, K. Gopalakrishnan, K. Han, K. Hausman, A. Herzog, J. Hsu, B. Ichter, A. Irpan, N. J. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, L. Lee, T. E. Lee, S. Levine, Y. Lu, H. Michalewski, I. Mordatch, K. Pertsch, K. Rao, K. Reymann, M. S. Ryoo, G. Salazar, P. Sanketi, P. Sermanet, J. Singh, A. Singh, R. Soricut, H. T. Tran, V. Vanhoucke, Q. Vuong, A. Wahid, S. Welker, P. Wohlhart, J. Wu, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich, “RT-2: visionlanguage-action models transfer web knowledge to robotic control,” _CoRR_ , vol. abs/2307.15818, 2023. 

- [2] A. Krizhevsky, I. Sutskever, and G. E. Hinton, “Imagenet classification with deep convolutional neural networks,” in _NIPS_ , 2012, pp. 1106– 1114. 

- [3] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention is all you need,” in _NIPS_ , 2017, pp. 5998–6008. 

- [4] V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. A. Riedmiller, A. Fidjeland, G. Ostrovski, S. Petersen, C. Beattie, A. Sadik, I. Antonoglou, H. King, D. Kumaran, D. Wierstra, S. Legg, and D. Hassabis, “Human-level control through deep reinforcement learning,” _Nat._ , vol. 518, no. 7540, pp. 529–533, 2015. 

- [5] S. Levine, P. Pastor, A. Krizhevsky, and D. Quillen, “Learning handeye coordination for robotic grasping with large-scale data collection,” in _ISER_ , ser. Springer Proceedings in Advanced Robotics, vol. 1. Springer, 2016, pp. 173–184. 

- [6] J. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds, R. Ring, E. Rutherford, S. Cabi, T. Han, Z. Gong, S. Samangooei, M. Monteiro, J. L. Menick, S. Borgeaud, A. Brock, A. Nematzadeh, S. Sharifzadeh, M. Binkowski, R. Barreira, O. Vinyals, A. Zisserman, and K. Simonyan, “Flamingo: a visual language model for few-shot learning,” in _NeurIPS_ , 2022. 

- [7] J. Li, D. Li, S. Savarese, and S. C. H. Hoi, “BLIP-2: bootstrapping language-image pre-training with frozen image encoders and large language models,” in _ICML_ , vol. 202. PMLR, 2023, pp. 19 730– 19 742. 

- [8] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” _CoRR_ , vol. abs/2304.08485, 2023. 

- [9] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar, P. Sermanet, T. Jackson, N. Brown, L. Luu, S. Levine, K. Hausman, and B. Ichter, “Inner monologue: Embodied reasoning through planning with language models,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 1769–1782. 

- [10] B. Ichter, A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, R. Julian, D. Kalashnikov, S. Levine, Y. Lu, C. Parada, K. Rao, P. Sermanet, A. Toshev, V. Vanhoucke, F. Xia, T. Xiao, P. Xu, M. Yan, N. Brown, M. Ahn, O. Cortes, N. Sievers, C. Tan, S. Xu, D. Reyes, J. Rettinghouse, J. Quiambao, P. Pastor, L. Luu, K. Lee, Y. Kuang, S. Jesmonth, N. J. Joshi, K. Jeffrey, R. J. Ruano, J. Hsu, K. Gopalakrishnan, B. David, A. Zeng, and C. K. Fu, “Do as I can, not as I say: Grounding language in robotic affordances,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 287–318. 

- [11] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, W. Huang, Y. Chebotar, P. Sermanet, D. Duckworth, S. Levine, V. Vanhoucke, K. Hausman, M. Toussaint, K. Greff, A. Zeng, I. Mordatch, and P. Florence, “Palm-e: An embodied multimodal language model,” in _ICML_ , vol. 202. PMLR, 2023, pp. 8469–8488. 

- [12] R. Firoozi, J. Tucker, S. Tian, A. Majumdar, J. Sun, W. Liu, Y. Zhu, S. Song, A. Kapoor, K. Hausman, B. Ichter, D. Driess, J. Wu, C. Lu, and M. Schwager, “Foundation models in robotics: Applications, challenges, and the future,” _CoRR_ , vol. abs/2312.07843, 2023. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

18 

- [13] J. Wang, Z. Wu, Y. Li, H. Jiang, P. Shu, E. Shi, H. Hu, C. Ma, Y. Liu, X. Wang, Y. Yao, X. Liu, H. Zhao, Z. Liu, H. Dai, L. Zhao, B. Ge, X. Li, T. Liu, and S. Zhang, “Large language models for robotics: Opportunities, challenges, and perspectives,” _CoRR_ , vol. abs/2401.04334, 2024. 

- [14] Y. Hu, Q. Xie, V. Jain, J. Francis, J. Patrikar, N. V. Keetha, S. Kim, Y. Xie, T. Zhang, S. Zhao, Y. Q. Chong, C. Wang, K. P. Sycara, M. Johnson-Roberson, D. Batra, X. Wang, S. A. Scherer, Z. Kira, F. Xia, and Y. Bisk, “Toward general-purpose robots via foundation models: A survey and meta-analysis,” _CoRR_ , vol. abs/2312.08782, 2023. 

- [15] K. Kawaharazuka, T. Matsushima, A. Gambardella, J. Guo, C. Paxton, and A. Zeng, “Real-world robot applications of foundation models: a review,” _Adv. Robotics_ , vol. 38, no. 18, pp. 1232–1254, 2024. 

- [16] L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch, “Decision transformer: Reinforcement learning via sequence modeling,” in _NeurIPS_ , 2021, pp. 15 084–15 097. 

- [17] M. Janner, Q. Li, and S. Levine, “Offline reinforcement learning as one big sequence modeling problem,” in _NeurIPS_ , 2021, pp. 1273–1286. 

- [18] S. E. Reed, K. Zolna, E. Parisotto, S. G. Colmenarejo, A. Novikov, G. Barth-Maron, M. Gimenez, Y. Sulsky, J. Kay, J. T. Springenberg, T. Eccles, J. Bruce, A. Razavi, A. Edwards, N. Heess, Y. Chen, R. Hadsell, O. Vinyals, M. Bordbar, and N. de Freitas, “A generalist agent,” _Trans. Mach. Learn. Res._ , vol. 2022, 2022. 

- [19] A. A. Physical Intelligence and, R. Aniceto, A. Balakrishna, K. Black, K. Conley, G. Connors, J. Darpinian, K. Dhabalia, J. DiCarlo, D. Driess, M. Equi, A. Esmail, Y. Fang, C. Finn, C. Glossop, T. Godden, I. Goryachev, L. Groom, H. Hancock, K. Hausman, G. Hussein, B. Ichter, S. Jakubczak, R. Jen, T. Jones, B. Katz, L. Ke, C. Kuchi, M. Lamb, D. LeBlanc, S. Levine, A. Li-Bell, Y. Lu, V. Mano, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, C. Sharma, L. X. Shi, L. Smith, J. T. Springenberg, K. Stachowicz, W. Stoeckle, A. Swerdlow, J. Tanner, M. Torne, Q. Vuong, A. Walling, H. Wang, B. Williams, S. Yoo, L. Yu, U. Zhilinsky, and Z. Zhou, “ _π_<sup>*</sup> 0.6: a VLA that learns, from experience,” _CoRR_ , vol. abs/2511.14759, 2025. 

- [20] A. Hiranaka, M. Hwang, S. Lee, C. Wang, L. Fei-Fei, J. Wu, and R. Zhang, “Primitive skill-based robot learning from human evaluative feedback,” in _IROS_ , 2023, pp. 7817–7824. 

- [21] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, “Reflexion: language agents with verbal reinforcement learning,” in _NeurIPS_ , 2023. 

- [22] Y. J. Ma, W. Liang, G. Wang, D. Huang, O. Bastani, D. Jayaraman, Y. Zhu, L. Fan, and A. Anandkumar, “Eureka: Human-level reward design via coding large language models,” in _ICLR_ , 2024. 

- [23] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, “Learning transferable visual models from natural language supervision,” in _ICML_ , vol. 139. PMLR, 2021, pp. 8748–8763. 

- [24] S. Nair, A. Rajeswaran, V. Kumar, C. Finn, and A. Gupta, “R3M: A universal visual representation for robot manipulation,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 892–909. 

- [25] Y. J. Ma, S. Sodhani, D. Jayaraman, O. Bastani, V. Kumar, and A. Zhang, “VIP: towards universal visual reward and representation via value-implicit pre-training,” in _ICLR_ , 2023. 

- [26] I. Radosavovic, T. Xiao, S. James, P. Abbeel, J. Malik, and T. Darrell, “Real-world robot learning with masked visual pre-training,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 416–426. 

- [27] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: pre-training of deep bidirectional transformers for language understanding,” in _NAACL-HLT (1)_ . Association for Computational Linguistics, 2019, pp. 4171–4186. 

- [28] I. Radosavovic, B. Shi, L. Fu, K. Goldberg, T. Darrell, and J. Malik, “Robot learning with sensorimotor pre-training,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 683–693. 

- [29] M. Shridhar, L. Manuelli, and D. Fox, “Cliport: What and where pathways for robotic manipulation,” in _CoRL_ , vol. 164. PMLR, 2021, pp. 894–906. 

- [30] A. Khandelwal, L. Weihs, R. Mottaghi, and A. Kembhavi, “Simple but effective: CLIP embeddings for embodied AI,” in _CVPR_ . IEEE, 2022, pp. 14 809–14 818. 

- [31] S. Y. Gadre, M. Wortsman, G. Ilharco, L. Schmidt, and S. Song, “Cows on pasture: Baselines and benchmarks for language-driven zero-shot object navigation,” in _CVPR_ . IEEE, 2023, pp. 23 171–23 181. 

- [32] A. Majumdar, K. Yadav, S. Arnaud, Y. J. Ma, C. Chen, S. Silwal, A. Jain, V. Berges, T. Wu, J. Vakil, P. Abbeel, J. Malik, D. Batra, 

Y. Lin, O. Maksymets, A. Rajeswaran, and F. Meier, “Where are we in the search for an artificial visual cortex for embodied intelligence?” in _NeurIPS_ , 2023. 

- [33] S. Karamcheti, S. Nair, A. S. Chen, T. Kollar, C. Finn, D. Sadigh, and P. Liang, “Language-driven representation learning for robotics,” in _RSS_ , 2023. 

- [34] M. Oquab, T. Darcet, T. Moutakanni, H. V. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, M. Assran, N. Ballas, W. Galuba, R. Howes, P. Huang, S. Li, I. Misra, M. Rabbat, V. Sharma, G. Synnaeve, H. Xu, H. J´egou, J. Mairal, P. Labatut, A. Joulin, and P. Bojanowski, “Dinov2: Learning robust visual features without supervision,” _Trans. Mach. Learn. Res._ , vol. 2024, 2024. 

- [35] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, G. Lam, P. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” _CoRR_ , vol. abs/2406.09246, 2024. 

- [36] W. Huang, C. Wang, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation,” _CoRR_ , vol. abs/2409.01652, 2024. 

- [37] M. Assran, Q. Duval, I. Misra, P. Bojanowski, P. Vincent, M. G. Rabbat, Y. LeCun, and N. Ballas, “Self-supervised learning from images with a joint-embedding predictive architecture,” in _CVPR_ . IEEE, 2023, pp. 15 619–15 629. 

- [38] J. Shang, K. Schmeckpeper, B. B. May, M. V. Minniti, T. Kelestemur, D. Watkins, and L. Herlant, “Theia: Distilling diverse vision foundation models for robot learning,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 724–748. 

- [39] S. Parisi, A. Rajeswaran, S. Purushwalkam, and A. Gupta, “The unsurprising effectiveness of pre-trained vision models for control,” in _ICML_ , vol. 162. PMLR, 2022, pp. 17 359–17 371. 

- [40] Y. LeCun, “A path towards autonomous machine intelligence,” 2022. [Online]. Available: https://openreview.net/pdf?id=BZ5a1r-kVsf 

- [41] W. Shen, G. Yang, A. Yu, J. Wong, L. P. Kaelbling, and P. Isola, “Distilled feature fields enable few-shot language-guided manipulation,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 405–424. 

- [42] Y. Hong, H. Zhen, P. Chen, S. Zheng, Y. Du, Z. Chen, and C. Gan, “3dllm: Injecting the 3d world into large language models,” in _NeurIPS_ , 2023. 

- [43] B. Kerbl, G. Kopanas, T. Leimk¨uhler, and G. Drettakis, “3d gaussian splatting for real-time radiance field rendering,” _ACM Trans. Graph._ , vol. 42, no. 4, pp. 139:1–139:14, 2023. 

- [44] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, “Langsplat: 3d language gaussian splatting,” in _CVPR_ . IEEE, 2024, pp. 20 051– 20 060. 

- [45] A. Thankaraj and L. Pinto, “That sounds right: Auditory selfsupervision for dynamic robot manipulation,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 1036–1049. 

- [46] Y. Jing, X. Zhu, X. Liu, Q. Sima, T. Yang, Y. Feng, and T. Kong, “Exploring visual pre-training for robot manipulation: Datasets, models and methods,” in _IROS_ , 2023, pp. 11 390–11 395. 

- [47] F. Liu, H. Liu, A. Grover, and P. Abbeel, “Masked autoencoding for scalable and generalizable decision making,” in _NeurIPS_ , 2022. 

- [48] J. Li, Q. Gao, M. Johnston, X. Gao, X. He, H. Shi, S. Shakiah, R. Ghanadan, and W. Y. Wang, “Mastering robot manipulation with multimodal prompts through pretraining and multi-task fine-tuning,” in _ICML_ , 2024. 

- [49] Y. Sun, S. Ma, R. Madaan, R. Bonatti, F. Huang, and A. Kapoor, “SMART: self-supervised multi-task pretraining with control transformers,” in _ICLR_ , 2023. 

- [50] R. Bonatti, S. Vemprala, S. Ma, F. Frujeri, S. Chen, and A. Kapoor, “PACT: perception-action causal transformer for autoregressive robotics pre-training,” in _IROS_ , 2023, pp. 3621–3627. 

- [51] B. Baker, I. Akkaya, P. Zhokhov, J. Huizinga, J. Tang, A. Ecoffet, B. Houghton, R. Sampedro, and J. Clune, “Video pretraining (VPT): learning to act by watching unlabeled online videos,” in _NeurIPS_ , 2022. 

- [52] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _ICLR_ , 2024. 

- [53] D. Hafner, T. P. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _ICLR_ , 2020. 

- [54] D. Hafner, T. P. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” in _ICLR_ , 2021. 

- [55] D. Hafner, J. Pasukonis, J. Ba, and T. P. Lillicrap, “Mastering diverse domains through world models,” _CoRR_ , vol. abs/2301.04104, 2023. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

19 

- [56] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 2226–2240. 

- [57] V. Micheli, E. Alonso, and F. Fleuret, “Transformers are sampleefficient world models,” in _ICLR_ , 2023. 

- [58] J. Robine, M. H¨oftmann, T. Uelwer, and S. Harmeling, “Transformerbased world models are happy with 100k interactions,” in _ICLR_ , 2023. 

- [59] K. Nottingham, P. Ammanabrolu, A. Suhr, Y. Choi, H. Hajishirzi, S. Singh, and R. Fox, “Do embodied agents dream of pixelated sheep: Embodied decision making using language guided world modelling,” in _ICML_ , vol. 202. PMLR, 2023, pp. 26 311–26 325. 

- [60] Z. Song, Y. Zhang, and I. King, “No change, no gain: Empowering graph neural networks with expected model change maximization for active learning,” in _NeurIPS_ , 2023. 

- [61] Y. Ma, Z. Song, X. Hu, J. Li, Y. Zhang, and I. King, “Graph component contrastive learning for concept relatedness estimation,” in _AAAI_ . AAAI Press, 2023, pp. 13 362–13 370. 

- [62] L. Guan, K. Valmeekam, S. Sreedharan, and S. Kambhampati, “Leveraging pre-trained large language models to construct and utilize world models for model-based task planning,” in _NeurIPS_ , 2023. 

- [63] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone, “LLM+P: empowering large language models with optimal planning proficiency,” _CoRR_ , vol. abs/2304.11477, 2023. 

- [64] S. Hao, Y. Gu, H. Ma, J. J. Hong, Z. Wang, D. Z. Wang, and Z. Hu, “Reasoning with language model is planning with world model,” in _EMNLP_ , 2023, pp. 8154–8173. 

- [65] M. Hu, Y. Mu, X. Yu, M. Ding, S. Wu, W. Shao, Q. Chen, B. Wang, Y. Qiao, and P. Luo, “Tree-planner: Efficient close-loop task planning with large language models,” in _ICLR_ , 2024. 

- [66] Z. Zhao, W. S. Lee, and D. Hsu, “Large language models as commonsense knowledge for large-scale task planning,” in _NeurIPS_ , 2023. 

- [67] OpenAI. (2024) Video generation models as world simulators. [Online]. Available: https://openai.com/index/ video-generation-models-as-world-simulators/ 

- [68] Z. Zhu, X. Wang, W. Zhao, C. Min, N. Deng, M. Dou, Y. Wang, B. Shi, K. Wang, C. Zhang, Y. You, Z. Zhang, D. Zhao, L. Xiao, J. Zhao, J. Lu, and G. Huang, “Is sora a world simulator? A comprehensive survey on general world models and beyond,” _CoRR_ , vol. abs/2405.03520, 2024. 

- [69] J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps, Y. Aytar, S. Bechtle, F. M. P. Behbahani, S. C. Y. Chan, N. Heess, L. Gonzalez, S. Osindero, S. Ozair, S. E. Reed, J. Zhang, K. Zolna, J. Clune, N. de Freitas, S. Singh, and T. Rockt¨aschel, “Genie: Generative interactive environments,” in _ICML_ , 2024. 

- [70] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: A 3d vision-language-action generative world model,” in _ICML_ , 2024. 

- [71] S. Yang, Y. Du, S. K. S. Ghasemipour, J. Tompson, L. P. Kaelbling, D. Schuurmans, and P. Abbeel, “Learning interactive real-world simulators,” in _ICLR_ , 2024. 

- [72] J. Xiang, T. Tao, Y. Gu, T. Shu, Z. Wang, Z. Yang, and Z. Hu, “Language models meet world models: Embodied experiences enhance language models,” in _NeurIPS_ , 2023. 

- [73] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa, “Large language models are zero-shot reasoners,” in _NeurIPS_ , 2022. 

- [74] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou, “Chain-of-thought prompting elicits reasoning in large language models,” in _NeurIPS_ , 2022. 

- [75] G. Lu, Z. Wang, C. Liu, J. Lu, and Y. Tang, “Thinkbot: Embodied instruction following with thought chain reasoning,” _CoRR_ , vol. abs/2312.07062, 2023. 

- [76] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, and Y. Cao, “React: Synergizing reasoning and acting in language models,” in _ICLR_ , 2023. 

- [77] Z. Wang, A. Liu, H. Lin, J. Li, X. Ma, and Y. Liang, “RAT: retrieval augmented thoughts elicit context-aware reasoning in long-horizon generation,” _CoRR_ , vol. abs/2403.05313, 2024. 

- [78] M. Zawalski, W. Chen, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” _CoRR_ , vol. abs/2407.08693, 2024. 

- [79] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn, A. Handa, T. Lin, G. Wetzstein, M. Liu, and D. Xiang, “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _CVPR_ , 2025, pp. 1702–1713. 

- [80] M. Nakamoto, O. Mees, A. Kumar, and S. Levine, “Steering your generalists: Improving robotic foundation models via value guidance,” 

in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 4996–5013. 

- [81] J. Kwok, C. Agia, R. Sinha, M. Foutter, S. Li, I. Stoica, A. Mirhoseini, and M. Pavone, “Robomonkey: Scaling test-time sampling and verification for vision-language-action models,” _CoRR_ , vol. abs/2506.17811, 2025. 

- [82] E. Jang, A. Irpan, M. Khansari, D. Kappler, F. Ebert, C. Lynch, S. Levine, and C. Finn, “BC-Z: zero-shot task generalization with robotic imitation learning,” in _CoRL_ , vol. 164. PMLR, 2021, pp. 991–1002. 

- [83] C. Lynch and P. Sermanet, “Language conditioned imitation learning over unstructured data,” in _RSS_ , 2021. 

- [84] O. Mees, L. Hermann, and W. Burgard, “What matters in language conditioned robotic imitation learning over unstructured data,” _IEEE Robotics Autom. Lett._ , vol. 7, no. 4, pp. 11 205–11 212, 2022. 

- [85] O. Mees, J. Borja-Diaz, and W. Burgard, “Grounding language with visual affordances over unstructured data,” in _ICRA_ . IEEE, 2023, pp. 11 576–11 582. 

- [86] Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel, “Learning universal policies via text-guided video generation,” in _NeurIPS_ , 2023. 

- [87] P. Sharma, B. Sundaralingam, V. Blukis, C. Paxton, T. Hermans, A. Torralba, J. Andreas, and D. Fox, “Correcting robot plans with natural language feedback,” in _RSS_ , 2022. 

- [88] C. Lynch, A. Wahid, J. Tompson, T. Ding, J. Betker, R. Baruch, T. Armstrong, and P. Florence, “Interactive language: Talking to robots in real time,” _CoRR_ , vol. abs/2210.06407, 2022. 

- [89] P. Guhur, S. Chen, R. G. Pinel, M. Tapaswi, I. Laptev, and C. Schmid, “Instruction-driven history-aware policies for robotic manipulations,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 175–187. 

- [90] M. Shridhar, L. Manuelli, and D. Fox, “Perceiver-actor: A multi-task transformer for robotic manipulation,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 785–799. 

- [91] T. Gervet, Z. Xian, N. Gkanatsios, and K. Fragkiadaki, “Act3d: 3d feature field transformers for multi-task robotic manipulation,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 3949–3965. 

- [92] A. Goyal, J. Xu, Y. Guo, V. Blukis, Y. Chao, and D. Fox, “RVT: robotic view transformer for 3d object manipulation,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 694–710. 

- [93] A. Goyal, V. Blukis, J. Xu, Y. Guo, Y. Chao, and D. Fox, “RVT-2: learning precise manipulation from few demonstrations,” _CoRR_ , vol. abs/2406.08545, 2024. 

- [94] W. Yuan, J. Duan, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox, “Robopoint: A vision-language model for spatial affordance prediction for robotics,” _CoRR_ , vol. abs/2406.10721, 2024. 

- [95] K. Bousmalis, G. Vezzani, D. Rao, C. Devin, A. X. Lee, M. Bauz´a, T. Davchev, Y. Zhou, A. Gupta, A. Raju, A. Laurens, C. Fantacci, V. Dalibard, M. Zambelli, M. F. Martins, R. Pevceviciute, M. Blokzijl, M. Denil, N. Batchelor, T. Lampe, E. Parisotto, K. Zolna, S. E. Reed, S. G. Colmenarejo, J. Scholz, A. Abdolmaleki, O. Groth, J. Regli, O. Sushkov, T. Roth¨orl, J. E. Chen, Y. Aytar, D. Barker, J. Ortiz, M. A. Riedmiller, J. T. Springenberg, R. Hadsell, F. Nori, and N. Heess, “Robocat: A self-improving foundation agent for robotic manipulation,” _CoRR_ , vol. abs/2306.11706, 2023. 

- [96] A. Stone, T. Xiao, Y. Lu, K. Gopalakrishnan, K. Lee, Q. Vuong, P. Wohlhart, B. Zitkovich, F. Xia, C. Finn, and K. Hausman, “Openworld object manipulation using pre-trained vision-language models,” _CoRR_ , vol. abs/2303.00905, 2023. 

- [97] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu, J. Ibarz, B. Ichter, A. Irpan, T. Jackson, S. Jesmonth, N. J. Joshi, R. Julian, D. Kalashnikov, Y. Kuang, I. Leal, K. Lee, S. Levine, Y. Lu, U. Malla, D. Manjunath, I. Mordatch, O. Nachum, C. Parada, J. Peralta, E. Perez, K. Pertsch, J. Quiambao, K. Rao, M. S. Ryoo, G. Salazar, P. R. Sanketi, K. Sayed, J. Singh, S. Sontakke, A. Stone, C. Tan, H. T. Tran, V. Vanhoucke, S. Vega, Q. Vuong, F. Xia, T. Xiao, P. Xu, S. Xu, T. Yu, and B. Zitkovich, “RT-1: robotics transformer for real-world control at scale,” in _RSS_ , 2023. 

- [98] Y. Chebotar, Q. Vuong, A. Irpan, K. Hausman, F. Xia, Y. Lu, A. Kumar, T. Yu, A. Herzog, K. Pertsch, K. Gopalakrishnan, J. Ibarz, O. Nachum, S. Sontakke, G. Salazar, H. T. Tran, J. Peralta, C. Tan, D. Manjunath, J. Singh, B. Zitkovich, T. Jackson, K. Rao, C. Finn, and S. Levine, “Qtransformer: Scalable offline reinforcement learning via autoregressive q-functions,” _CoRR_ , vol. abs/2309.10150, 2023. 

- [99] J. Gu, S. Kirmani, P. Wohlhart, Y. Lu, M. G. Arenas, K. Rao, W. Yu, C. Fu, K. Gopalakrishnan, Z. Xu, P. Sundaresan, P. Xu, 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

20 

H. Su, K. Hausman, C. Finn, Q. Vuong, and T. Xiao, “Rt-trajectory: Robotic task generalization via hindsight trajectory sketches,” _CoRR_ , vol. abs/2311.01977, 2023. 

- [100] T. Z. Zhao, V. Kumar, S. Levine, and C. Finn, “Learning fine-grained bimanual manipulation with low-cost hardware,” in _RSS_ , 2023. 

- [101] H. Bharadhwaj, J. Vakil, M. Sharma, A. Gupta, S. Tulsiani, and V. Kumar, “Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking,” in _ICRA_ . IEEE, 2024, pp. 4788–4795. 

- [102] X. Li, M. Liu, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, H. Li, and T. Kong, “Vision-language foundation models as effective robot imitators,” _CoRR_ , vol. abs/2311.01378, 2023. 

- [103] F. Liu, F. Yan, L. Zheng, C. Feng, Y. Huang, and L. Ma, “Robouniview: Visual-language model with unified view representation for robotic manipulaiton,” _CoRR_ , vol. abs/2406.18977, 2024. 

- [104] Y. Yue, Y. Wang, B. Kang, Y. Han, S. Wang, S. Song, J. Feng, and G. Huang, “Deer-vla: Dynamic inference of multimodal large language models for efficient robot execution,” in _NeurIPS_ , 2024. 

- [105] S. Huang, Z. Jiang, H. Dong, Y. Qiao, P. Gao, and H. Li, “Instruct2act: Mapping multi-modality instructions to robotic actions with large language model,” _CoRR_ , vol. abs/2305.11176, 2023. 

- [106] W. Huang, C. Wang, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language models,” _CoRR_ , vol. abs/2307.05973, 2023. 

- [107] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” in _RSS_ , 2023. 

- [108] Y. Ze, G. Zhang, K. Zhang, C. Hu, M. Wang, and H. Xu, “3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations,” in _RSS_ , 2024. 

- [109] H. Ha, P. Florence, and S. Song, “Scaling up and distilling down: Language-guided robot skill acquisition,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 3766–3777. 

- [110] D. Ghosh, H. R. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu, J. Luo, Y. L. Tan, L. Y. Chen, Q. Vuong, T. Xiao, P. R. Sanketi, D. Sadigh, C. Finn, and S. Levine, “Octo: An open-source generalist robot policy,” in _RSS_ , 2024. 

- [111] T. Ke, N. Gkanatsios, and K. Fragkiadaki, “3d diffuser actor: Policy diffusion with 3d scene representations,” _CoRR_ , vol. abs/2402.10885, 2024. 

- [112] M. Reuss, O.<sup>¨</sup> E. Yagmurlu, F. Wenzel, and R. Lioutikov, “Multimodal diffusion transformer: Learning versatile behavior from multimodal goals,” _CoRR_ , vol. abs/2407.05996, 2024. 

- [113] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” _arXiv preprint arXiv:2410.07864_ , 2024. 

- [114] S. Belkhale, T. Ding, T. Xiao, P. Sermanet, Q. Vuong, J. Tompson, Y. Chebotar, D. Dwibedi, and D. Sadigh, “RT-H: action hierarchies using language,” _CoRR_ , vol. abs/2403.01823, 2024. 

- [115] O. X. Collaboration, A. Padalkar, A. Pooley, A. Jain, A. Bewley, A. Herzog, A. Irpan, A. Khazatsky, A. Raj, A. Singh, A. Brohan, A. Raffin, A. Wahid, B. Burgess-Limerick, B. Kim, B. Sch¨olkopf, B. Ichter, C. Lu, C. Xu, C. Finn, C. Xu, C. Chi, C. Huang, C. Chan, C. Pan, C. Fu, C. Devin, D. Driess, D. Pathak, D. Shah, D. B¨uchler, D. Kalashnikov, D. Sadigh, E. Johns, F. Ceola, F. Xia, F. Stulp, G. Zhou, G. S. Sukhatme, G. Salhotra, G. Yan, G. Schiavi, G. Kahn, H. Su, H. Fang, H. Shi, H. B. Amor, H. I. Christensen, H. Furuta, H. Walke, H. Fang, I. Mordatch, I. Radosavovic, and et al., “Open x- embodiment: Robotic learning datasets and RT-X models,” _CoRR_ , vol. abs/2310.08864, 2023. 

- [116] M. J. Kim, C. Finn, and P. Liang, “Fine-tuning vision-language-action models: Optimizing speed and success,” _CoRR_ , vol. abs/2502.19645, 2025. 

- [117] R. Zheng, Y. Liang, S. Huang, J. Gao, H. D. III, A. Kolobov, F. Huang, and J. Yang, “Tracevla: Visual trace prompting enhances spatialtemporal awareness for generalist robotic policies,” in _ICLR_ , 2025. 

- [118] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky, “ _π_ 0: A vision-language-action flow model for general robot control,” _CoRR_ , vol. abs/2410.24164, 2024. 

- [119] J. Liu, M. Liu, Z. Wang, P. An, X. Li, K. Zhou, S. Yang, R. Zhang, Y. Guo, and S. Zhang, “Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation,” in _NeurIPS_ , 2024. 

- [120] D. Qu, H. Song, Q. Chen, Y. Yao, X. Ye, Y. Ding, Z. Wang, J. Gu, B. Zhao, D. Wang, and X. Li, “Spatialvla: Exploring spatial representations for visual-language-action model,” _CoRR_ , vol. abs/2501.15830, 2025. 

- [121] J. Wen, Y. Zhu, J. Li, M. Zhu, K. Wu, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang, “Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation,” _CoRR_ , vol. abs/2409.12514, 2024. 

- [122] Q. Li, Y. Liang, Z. Wang, L. Luo, X. Chen, M. Liao, F. Wei, Y. Deng, S. Xu, Y. Zhang, X. Wang, B. Liu, J. Fu, J. Bao, D. Chen, Y. Shi, J. Yang, and B. Guo, “Cogact: A foundational vision-language-action model for synergizing cognition and action in robotic manipulation,” _CoRR_ , vol. abs/2411.19650, 2024. 

- [123] J. Wen, Y. Zhu, J. Li, Z. Tang, C. Shen, and F. Feng, “Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control,” _CoRR_ , vol. abs/2502.05855, 2025. 

- [124] J. Liu, H. Chen, P. An, Z. Liu, R. Zhang, C. Gu, X. Li, Z. Guo, S. Chen, M. Liu, C. Hou, M. Zhao, K. alex Zhou, P. Heng, and S. Zhang, “Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model,” _CoRR_ , vol. abs/2503.10631, 2025. 

- [125] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y. Chao, B. Y. Lin, L. Liden, K. Lee, J. Gao, L. Zettlemoyer, D. Fox, and M. Seo, “Latent action pretraining from videos,” in _ICLR_ , 2025. 

- [126] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang, D. Zhao, and H. Chen, “Worldvla: Towards autoregressive action world model,” _CoRR_ , vol. abs/2506.21539, 2025. 

- [127] Y. Wang, X. Li, W. Wang, J. Zhang, Y. Li, Y. Chen, X. Wang, and Z. Zhang, “Unified vision-language-action model,” _CoRR_ , vol. abs/2506.19850, 2025. 

- [128] Y. Ma, D. Chi, S. Wu, Y. Liu, Y. Zhuang, and I. King, “Astra: Efficient transformer architecture and contrastive dynamics learning for embodied instruction following,” in _EMNLP_ , 2025. 

- [129] C. Qu, S. Dai, X. Wei, H. Cai, S. Wang, D. Yin, J. Xu, and J. Wen, “Tool learning with large language models: a survey,” _Frontiers Comput. Sci._ , vol. 19, no. 8, p. 198343, 2025. 

- [130] Y. Jiang, A. Gupta, Z. Zhang, G. Wang, Y. Dou, Y. Chen, L. FeiFei, A. Anandkumar, Y. Zhu, and L. Fan, “VIMA: general robot manipulation with multimodal prompts,” _CoRR_ , vol. abs/2210.03094, 2022. 

- [131] R. Liu, W. Wang, and Y. Yang, “Volumetric environment representation for vision-language navigation,” in _CVPR_ . IEEE, 2024, pp. 16 317– 16 328. 

- [132] Y. Ma and I. King, “3d-moe: A mixture-of-experts multi-modal LLM for 3d vision and pose diffusion via rectified flow,” _CoRR_ , vol. abs/2501.16698, 2025. 

- [133] M. Vecer´ık, C. Doersch, Y. Yang, T. Davchev, Y. Aytar, G. Zhou, R. Hadsell, L. Agapito, and J. Scholz, “Robotap: Tracking arbitrary points for few-shot visual imitation,” in _ICRA_ . IEEE, 2024, pp. 5397– 5403. 

- [134] S. Nasiriany, F. Xia, W. Yu, T. Xiao, J. Liang, I. Dasgupta, A. Xie, D. Driess, A. Wahid, Z. Xu, Q. Vuong, T. Zhang, T. E. Lee, K. Lee, P. Xu, S. Kirmani, Y. Zhu, A. Zeng, K. Hausman, N. Heess, C. Finn, S. Levine, and B. Ichter, “PIVOT: iterative visual prompting elicits actionable knowledge for vlms,” in _ICML_ , 2024. 

- [135] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, Linxi, Y. Fang, D. Fox, F. Hu, S. Huang, J. Jang, Z. Jiang, J. Kautz, K. Kundalia, L. Lao, Z. Li, Z. Lin, K. Lin, G. Liu, E. LLontop, L. Magne, A. Mandlekar, A. Narayan, S. Nasiriany, S. Reed, Y. L. Tan, G. Wang, Z. Wang, J. Wang, Q. Wang, J. Xiang, Y. Xie, Y. Xu, Z. Xu, S. Ye, Z. Yu, A. Zhang, H. Zhang, Y. Zhao, R. Zheng, and Y. Zhu, “GR00T N1: an open foundation model for generalist humanoid robots,” _CoRR_ , vol. abs/2503.14734, 2025. 

- [136] N. M. Chia-Yu Hung and, H. Deng, L. Renhang, Y. Ang, A. Zadeh, C. Li, D. Herremans, Z. Wang, and S. Poria, “NORA-1.5: A visionlanguage-action model trained using world model-, and action-based preference rewards,” _CoRR_ , vol. abs/2511.14659, 2025. 

- [137] P. Z. Yue Liao and, S. Huang, D. Yang, S. Chen, Y. Jiang, H. Yue, J. Cai, S. Liu, J. Luo, L. Chen, S. Yan, M. Yao, and G. Ren, “Genie envisioner: A unified world foundation platform for robotic, manipulation,” _CoRR_ , vol. abs/2508.05635, 2025. 

- [138] K. Tian, Y. Jiang, Z. Yuan, B. Peng, and L. Wang, “Visual autoregressive modeling: Scalable image generation via next-scale prediction,” in _NeurIPS_ , 2024. 

- [139] X. Zhuang, Y. Xie, Y. Deng, L. Liang, J. Ru, Y. Yin, and Y. Zou, “VARGPT: unified understanding and generation in a visual autoregres- 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

21 

sive multimodal large language model,” _CoRR_ , vol. abs/2501.12327, 2025. 

- [140] Y. Mu, Q. Zhang, M. Hu, W. Wang, M. Ding, J. Jin, B. Wang, J. Dai, Y. Qiao, and P. Luo, “Embodiedgpt: Vision-language pre-training via embodied chain of thought,” _CoRR_ , vol. abs/2305.15021, 2023. 

- [141] J. Huang, S. Yong, X. Ma, X. Linghu, P. Li, Y. Wang, Q. Li, S. Zhu, B. Jia, and S. Huang, “An embodied generalist agent in 3d world,” in _ICML_ , 2024. 

- [142] Z. Qi, R. Dong, S. Zhang, H. Geng, C. Han, Z. Ge, L. Yi, and K. Ma, “Shapellm: Universal 3d object understanding for embodied interaction,” in _ECCV (43)_ , ser. Lecture Notes in Computer Science, vol. 15101. Springer, 2024, pp. 214–238. 

- [143] W. Huang, P. Abbeel, D. Pathak, and I. Mordatch, “Language models as zero-shot planners: Extracting actionable knowledge for embodied agents,” in _ICML_ , vol. 162. PMLR, 2022, pp. 9118–9147. 

- [144] P. Sharma, A. Torralba, and J. Andreas, “Skill induction and planning with latent language,” in _ACL (1)_ , 2022, pp. 1713–1726. 

- [145] C. H. Song, B. M. Sadler, J. Wu, W. Chao, C. Washington, and Y. Su, “Llm-planner: Few-shot grounded planning for embodied agents with large language models,” in _ICCV_ . IEEE, 2023, pp. 2986–2997. 

- [146] S. Li, X. Puig, C. Paxton, Y. Du, C. Wang, L. Fan, T. Chen, D. Huang, E. Aky¨urek, A. Anandkumar, J. Andreas, I. Mordatch, A. Torralba, and Y. Zhu, “Pre-trained language models for interactive decision-making,” in _NeurIPS_ , 2022. 

- [147] A. Zeng, M. Attarian, B. Ichter, K. M. Choromanski, A. Wong, S. Welker, F. Tombari, A. Purohit, M. S. Ryoo, V. Sindhwani, J. Lee, V. Vanhoucke, and P. Florence, “Socratic models: Composing zero-shot multimodal reasoning with language,” in _ICLR_ , 2023. 

- [148] I. Singh, V. Blukis, A. Mousavian, A. Goyal, D. Xu, J. Tremblay, D. Fox, J. Thomason, and A. Garg, “Progprompt: Generating situated robot task plans using large language models,” in _ICRA_ . IEEE, 2023, pp. 11 523–11 530. 

- [149] S. Vemprala, R. Bonatti, A. Bucker, and A. Kapoor, “Chatgpt for robotics: Design principles and model abilities,” _CoRR_ , vol. abs/2306.17582, 2023. 

- [150] J. Liang, W. Huang, F. Xia, P. Xu, K. Hausman, B. Ichter, P. Florence, and A. Zeng, “Code as policies: Language model programs for embodied control,” in _ICRA_ . IEEE, 2023, pp. 9493–9500. 

- [151] Z. Wang, S. Cai, A. Liu, X. Ma, and Y. Liang, “Describe, explain, plan and select: Interactive planning with large language models enables open-world multi-task agents,” _CoRR_ , vol. abs/2302.01560, 2023. 

- [152] Q. Gu, A. Kuwajerwala, S. Morin, K. M. Jatavallabhula, B. Sen, A. Agarwal, C. Rivera, W. Paul, K. Ellis, R. Chellappa, C. Gan, C. M. de Melo, J. B. Tenenbaum, A. Torralba, F. Shkurti, and L. Paull, “Conceptgraphs: Open-vocabulary 3d scene graphs for perception and planning,” _CoRR_ , vol. abs/2309.16650, 2023. 

- [153] F. Lin, Y. Hu, P. Sheng, C. Wen, J. You, and Y. Gao, “Data scaling laws in imitation learning for robotic manipulation,” in _ICLR_ , 2025. 

- [154] T. Pearce, T. Rashid, D. Bignell, R. Georgescu, S. Devlin, and K. Hofmann, “Scaling laws for pre-training agents and world models,” in _ICML_ , 2025. 

- [155] Y. Hong, Z. Zheng, P. Chen, Y. Wang, J. Li, and C. Gan, “Multiply: A multisensory object-centric embodied large language model in 3d world,” in _CVPR_ . IEEE, 2024, pp. 26 396–26 406. 

- [156] S. S. Raman, V. Cohen, E. Rosen, I. Idrees, D. Paulius, and S. Tellex, “Planning with large language models via corrective re-prompting,” _CoRR_ , vol. abs/2211.09935, 2022. 

- [157] P. Zhi, Z. Zhang, M. Han, Z. Zhang, Z. Li, Z. Jiao, B. Jia, and S. Huang, “Closed-loop open-vocabulary mobile manipulation with GPT-4V,” _CoRR_ , vol. abs/2404.10220, 2024. 

- [158] H. Fang, H. Fang, Z. Tang, J. Liu, C. Wang, J. Wang, H. Zhu, and C. Lu, “RH20T: A comprehensive robotic dataset for learning diverse skills in one-shot,” in _ICRA_ . IEEE, 2024, pp. 653–660. 

- [159] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis, P. D. Fagan, J. Hejna, M. Itkina, M. Lepert, Y. J. Ma, P. T. Miller, J. Wu, S. Belkhale, S. Dass, H. Ha, A. Jain, A. Lee, Y. Lee, M. Memmel, S. Park, I. Radosavovic, K. Wang, A. Zhan, K. Black, C. Chi, K. B. Hatch, S. Lin, J. Lu, J. Mercat, A. Rehman, P. R. Sanketi, A. Sharma, C. Simpson, Q. Vuong, H. R. Walke, B. Wulfe, T. Xiao, J. H. Yang, A. Yavary, T. Z. Zhao, C. Agia, R. Baijal, M. G. Castro, D. Chen, Q. Chen, T. Chung, J. Drake, E. P. Foster, and et al., “DROID: A large-scale in-the-wild robot manipulation dataset,” _CoRR_ , vol. abs/2403.12945, 2024. 

- [160] P. Sharma, L. Mohan, L. Pinto, and A. Gupta, “Multiple interactions made easy (MIME): large scale demonstrations data for imitation,” in _CoRL_ , vol. 87. PMLR, 2018, pp. 906–915. 

- [161] A. Mandlekar, Y. Zhu, A. Garg, J. Booher, M. Spero, A. Tung, J. Gao, J. Emmons, A. Gupta, E. Orbay, S. Savarese, and L. Fei-Fei, “ROBOTURK: A crowdsourcing platform for robotic skill learning through imitation,” in _CoRL_ , vol. 87. PMLR, 2018, pp. 879–893. 

- [162] S. Dasari, F. Ebert, S. Tian, S. Nair, B. Bucher, K. Schmeckpeper, S. Singh, S. Levine, and C. Finn, “Robonet: Large-scale multi-robot learning,” in _CoRL_ , vol. 100. PMLR, 2019, pp. 885–897. 

- [163] D. Kalashnikov, J. Varley, Y. Chebotar, B. Swanson, R. Jonschkowski, C. Finn, S. Levine, and K. Hausman, “Mt-opt: Continuous multi-task robotic reinforcement learning at scale,” _CoRR_ , vol. abs/2104.08212, 2021. 

- [164] V. Kumar, R. M. Shah, G. Zhou, V. Moens, V. Caggiano, A. Gupta, and A. Rajeswaran, “Robohive: A unified framework for robot learning,” in _NeurIPS_ , 2023. 

- [165] F. Ebert, Y. Yang, K. Schmeckpeper, B. Bucher, G. Georgakis, K. Daniilidis, C. Finn, and S. Levine, “Bridge data: Boosting generalization of robotic skills with cross-domain datasets,” in _RSS_ , 2022. 

- [166] S. Srivastava, C. Li, M. Lingelbach, R. Mart´ın-Mart´ın, F. Xia, K. E. Vainio, Z. Lian, C. Gokmen, S. Buch, C. K. Liu, S. Savarese, H. Gweon, J. Wu, and L. Fei-Fei, “BEHAVIOR: benchmark for everyday household activities in virtual, interactive, and ecological environments,” in _CoRL_ , vol. 164. PMLR, 2021, pp. 477–490. 

- [167] C. Li, F. Xia, R. Mart´ın-Mart´ın, M. Lingelbach, S. Srivastava, B. Shen, K. E. Vainio, C. Gokmen, G. Dharan, T. Jain, A. Kurenkov, C. K. Liu, H. Gweon, J. Wu, L. Fei-Fei, and S. Savarese, “igibson 2.0: Objectcentric simulation for robot learning of everyday household tasks,” in _CoRL_ , vol. 164. PMLR, 2021, pp. 455–465. 

- [168] F. Xia, A. R. Zamir, Z. He, A. Sax, J. Malik, and S. Savarese, “Gibson env: Real-world perception for embodied agents,” in _CVPR_ . Computer Vision Foundation / IEEE Computer Society, 2018, pp. 9068–9079. 

- [169] F. Xia, W. B. Shen, C. Li, P. Kasimbeg, M. Tchapmi, A. Toshev, R. Mart´ın-Mart´ın, and S. Savarese, “Interactive gibson benchmark: A benchmark for interactive navigation in cluttered environments,” _IEEE Robotics Autom. Lett._ , vol. 5, no. 2, pp. 713–720, 2020. 

- [170] B. Shen, F. Xia, C. Li, R. Mart´ın-Mart´ın, L. Fan, G. Wang, C. P´erezD’Arpino, S. Buch, S. Srivastava, L. Tchapmi, M. Tchapmi, K. Vainio, J. Wong, L. Fei-Fei, and S. Savarese, “igibson 1.0: A simulation environment for interactive tasks in large realistic scenes,” in _IROS_ . IEEE, 2021, pp. 7520–7527. 

- [171] C. Li, R. Zhang, J. Wong, C. Gokmen, S. Srivastava, R. Mart´ın-Mart´ın, C. Wang, G. Levine, W. Ai, B. Martinez, H. Yin, M. Lingelbach, M. Hwang, A. Hiranaka, S. Garlanka, A. Aydin, S. Lee, J. Sun, M. Anvari, M. Sharma, D. Bansal, S. Hunter, K. Kim, A. Lou, C. R. Matthews, I. Villa-Renteria, J. H. Tang, C. Tang, F. Xia, Y. Li, S. Savarese, H. Gweon, C. K. Liu, J. Wu, and L. Fei-Fei, “BEHAVIOR1K: A human-centered, embodied AI benchmark with 1, 000 everyday activities and realistic simulation,” _CoRR_ , vol. abs/2403.09227, 2024. 

- [172] F. Xiang, Y. Qin, K. Mo, Y. Xia, H. Zhu, F. Liu, M. Liu, H. Jiang, Y. Yuan, H. Wang, L. Yi, A. X. Chang, L. J. Guibas, and H. Su, “SAPIEN: A simulated part-based interactive environment,” in _CVPR_ . Computer Vision Foundation / IEEE, 2020, pp. 11 094–11 104. 

- [173] X. Li, K. Hsu, J. Gu, K. Pertsch, O. Mees, H. R. Walke, C. Fu, I. Lunawat, I. Sieh, S. Kirmani, S. Levine, J. Wu, C. Finn, H. Su, Q. Vuong, and T. Xiao, “Evaluating real-world robot manipulation policies in simulation,” _CoRR_ , vol. abs/2405.05941, 2024. 

- [174] E. Kolve, R. Mottaghi, D. Gordon, Y. Zhu, A. Gupta, and A. Farhadi, “AI2-THOR: an interactive 3d environment for visual AI,” _CoRR_ , vol. abs/1712.05474, 2017. 

- [175] K. Ehsani, W. Han, A. Herrasti, E. VanderBilt, L. Weihs, E. Kolve, A. Kembhavi, and R. Mottaghi, “Manipulathor: A framework for visual object manipulation,” in _CVPR_ . Computer Vision Foundation / IEEE, 2021, pp. 4497–4506. 

- [176] L. Weihs, M. Deitke, A. Kembhavi, and R. Mottaghi, “Visual room rearrangement,” in _CVPR_ . Computer Vision Foundation / IEEE, 2021, pp. 5922–5931. 

- [177] K. Mirakhor, S. Ghosh, D. Das, and B. Bhowmick, “Task planning for visual room rearrangement under partial observability,” in _ICLR_ , 2024. 

- [178] X. Puig, K. Ra, M. Boben, J. Li, T. Wang, S. Fidler, and A. Torralba, “Virtualhome: Simulating household activities via programs,” in _2018 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2018, Salt Lake City, UT, USA, June 18-22, 2018_ . Computer Vision Foundation / IEEE Computer Society, 2018, pp. 8494–8502. 

- [179] C. Gan, J. Schwartz, S. Alter, D. Mrowca, M. Schrimpf, J. Traer, J. D. Freitas, J. Kubilius, A. Bhandwaldar, N. Haber, M. Sano, K. Kim, E. Wang, M. Lingelbach, A. Curtis, K. T. Feigelis, D. Bear, D. Gutfreund, D. D. Cox, A. Torralba, J. J. DiCarlo, J. Tenenbaum, J. H. McDermott, and D. Yamins, “Threedworld: A platform for 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

22 

interactive multi-modal physical simulation,” in _NeurIPS Datasets and Benchmarks_ , 2021. 

- [180] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics Autom. Lett._ , vol. 5, no. 2, pp. 3019–3026, 2020. 

- [181] T. Yu, D. Quillen, Z. He, R. Julian, K. Hausman, C. Finn, and S. Levine, “Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning,” in _CoRL_ , vol. 100. PMLR, 2019, pp. 1094– 1100. 

- [182] O. Mees, L. Hermann, E. Rosete-Beas, and W. Burgard, “CALVIN: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks,” _IEEE Robotics Autom. Lett._ , vol. 7, no. 3, pp. 7327–7334, 2022. 

- [183] A. Gupta, V. Kumar, C. Lynch, S. Levine, and K. Hausman, “Relay policy learning: Solving long-horizon tasks via imitation and reinforcement learning,” in _CoRL_ , vol. 100. PMLR, 2019, pp. 1025–1037. 

- [184] M. Savva, J. Malik, D. Parikh, D. Batra, A. Kadian, O. Maksymets, Y. Zhao, E. Wijmans, B. Jain, J. Straub, J. Liu, and V. Koltun, “Habitat: A platform for embodied AI research,” in _ICCV_ . IEEE, 2019, pp. 9338–9346. 

- [185] A. Szot, A. Clegg, E. Undersander, E. Wijmans, Y. Zhao, J. M. Turner, N. Maestre, M. Mukadam, D. S. Chaplot, O. Maksymets, A. Gokaslan, V. Vondrus, S. Dharur, F. Meier, W. Galuba, A. X. Chang, Z. Kira, V. Koltun, J. Malik, M. Savva, and D. Batra, “Habitat 2.0: Training home assistants to rearrange their habitat,” in _NeurIPS_ , 2021, pp. 251– 266. 

- [186] D. Batra, A. X. Chang, S. Chernova, A. J. Davison, J. Deng, V. Koltun, S. Levine, J. Malik, I. Mordatch, R. Mottaghi, M. Savva, and H. Su, “Rearrangement: A challenge for embodied AI,” _CoRR_ , vol. abs/2011.01975, 2020. 

- [187] S. Yenamandra, A. Ramachandran, K. Yadav, A. S. Wang, M. Khanna, T. Gervet, T. Yang, V. Jain, A. Clegg, J. M. Turner, Z. Kira, M. Savva, A. X. Chang, D. S. Chaplot, D. Batra, R. Mottaghi, Y. Bisk, and C. Paxton, “Homerobot: Open-vocabulary mobile manipulation,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 1975–2011. 

- [188] M. Shridhar, J. Thomason, D. Gordon, Y. Bisk, W. Han, R. Mottaghi, L. Zettlemoyer, and D. Fox, “ALFRED: A benchmark for interpreting grounded instructions for everyday tasks,” in _CVPR_ . Computer Vision Foundation / IEEE, 2020, pp. 10 737–10 746. 

- [189] Y. Tassa, Y. Doron, A. Muldal, T. Erez, Y. Li, D. de Las Casas, D. Budden, A. Abdolmaleki, J. Merel, A. Lefrancq, T. P. Lillicrap, and M. A. Riedmiller, “Deepmind control suite,” _CoRR_ , vol. abs/1801.00690, 2018. 

- [190] G. Brockman, V. Cheung, L. Pettersson, J. Schneider, J. Schulman, J. Tang, and W. Zaremba, “Openai gym,” _CoRR_ , vol. abs/1606.01540, 2016. 

- [191] Genesis-Team, “Genesis: A universal and generative physics engine for robotics and beyond,” December 2024. [Online]. Available: https://github.com/Genesis-Embodied-AI/Genesis 

- [192] Y. Wang, Z. Xian, F. Chen, T. Wang, Y. Wang, K. Fragkiadaki, Z. Erickson, D. Held, and C. Gan, “Robogen: Towards unleashing infinite data for automated robot learning via generative simulation,” in _ICML_ , 2024. 

- [193] M. Ahn, D. Dwibedi, C. Finn, M. G. Arenas, K. Gopalakrishnan, K. Hausman, B. Ichter, A. Irpan, N. J. Joshi, R. Julian, S. Kirmani, I. Leal, T. E. Lee, S. Levine, Y. Lu, S. Maddineni, K. Rao, D. Sadigh, P. Sanketi, P. Sermanet, Q. Vuong, S. Welker, F. Xia, T. Xiao, P. Xu, S. Xu, and Z. Xu, “Autort: Embodied foundation models for large scale orchestration of robotic agents,” _CoRR_ , vol. abs/2401.12963, 2024. 

- [194] T. Xiao, H. Chan, P. Sermanet, A. Wahid, A. Brohan, K. Hausman, S. Levine, and J. Tompson, “Robotic skill acquisition via instruction augmentation with vision-language models,” in _RSS_ , 2023. 

- [195] Y. Ma, D. Chi, J. Li, K. Song, Y. Zhuang, and I. King, “VOLTA: improving generative diversity by variational mutual information maximizing autoencoder,” in _NAACL-HLT (Findings)_ , 2024. 

- [196] C. Chi, Z. Xu, C. Pan, E. Cousineau, B. Burchfiel, S. Feng, R. Tedrake, and S. Song, “Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots,” in _RSS_ , 2024. 

- [197] G. Moon, S. Saito, W. Xu, R. Joshi, J. Buffalini, H. Bellan, N. Rosen, J. Richardson, M. Mize, P. de Bree, T. Simon, B. Peng, S. Garg, K. McPhail, and T. Shiratori, “A dataset of relighted 3d interacting hands,” in _NeurIPS_ , 2023. 

- [198] Y. Chen, Y. Ge, Y. Ge, M. Ding, B. Li, R. Wang, R. Xu, Y. Shan, and X. Liu, “Egoplan-bench: Benchmarking egocentric embodied planning with multimodal large language models,” _CoRR_ , vol. abs/2312.06722, 2023. 

- [199] K. Valmeekam, M. Marquez, A. O. Hernandez, S. Sreedharan, and S. Kambhampati, “Planbench: An extensible benchmark for evaluating large language models on planning and reasoning about change,” in _NeurIPS_ , 2023. 

- [200] K. Valmeekam, M. Marquez, S. Sreedharan, and S. Kambhampati, “On the planning abilities of large language models - A critical investigation,” in _NeurIPS_ , 2023. 

- [201] J. Choi, Y. Yoon, H. Ong, J. Kim, and M. Jang, “Lota-bench: Benchmarking language-oriented task planners for embodied agents,” _CoRR_ , vol. abs/2402.08178, 2024. 

- [202] M. Li, S. Zhao, Q. Wang, K. Wang, Y. Zhou, S. Srivastava, C. Gokmen, T. Lee, L. E. Li, R. Zhang, W. Liu, P. Liang, L. Fei-Fei, J. Mao, and J. Wu, “Embodied agent interface: Benchmarking llms for embodied decision making,” in _NeurIPS_ , 2024. 

- [203] A. Das, S. Datta, G. Gkioxari, S. Lee, D. Parikh, and D. Batra, “Embodied question answering,” in _CVPR_ . Computer Vision Foundation / IEEE Computer Society, 2018, pp. 1–10. 

- [204] D. Gordon, A. Kembhavi, M. Rastegari, J. Redmon, D. Fox, and A. Farhadi, “IQA: visual question answering in interactive environments,” in _CVPR_ . Computer Vision Foundation / IEEE Computer Society, 2018, pp. 4089–4098. 

- [205] L. Yu, X. Chen, G. Gkioxari, M. Bansal, T. L. Berg, and D. Batra, “Multi-target embodied question answering,” in _CVPR_ . Computer Vision Foundation / IEEE, 2019, pp. 6309–6318. 

- [206] E. Wijmans, S. Datta, O. Maksymets, A. Das, G. Gkioxari, S. Lee, I. Essa, D. Parikh, and D. Batra, “Embodied question answering in photorealistic environments with point cloud perception,” in _CVPR_ . Computer Vision Foundation / IEEE, 2019, pp. 6659–6668. 

- [207] C. Fan, “Egovqa - an egocentric video question answering benchmark dataset,” in _ICCV Workshops_ . IEEE, 2019, pp. 4359–4366. 

- [208] B. Jia, T. Lei, S. Zhu, and S. Huang, “Egotaskqa: Understanding human tasks in egocentric videos,” in _NeurIPS_ , 2022. 

- [209] M. M. Islam, A. Gladstone, R. Islam, and T. Iqbal, “EQA-MX: embodied question answering using multimodal expression,” in _ICLR_ , 2024. 

- [210] A. Majumdar, A. Ajay, X. Zhang, P. Putta, S. Yenamandra, M. Henaff, S. Silwal, P. Mcvay, O. Maksymets, S. Arnaud, K. Yadav, Q. Li, B. Newman, M. Sharma, V. Berges, S. Zhang, P. Agrawal, Y. Bisk, D. Batra, M. Kalakrishnan, F. Meier, C. Paxton, S. Sax, and A. Rajeswaran, “OpenEQA: Embodied Question Answering in the Era of Foundation Models,” in _CVPR_ , 2024. 

- [211] R. Girdhar, A. El-Nouby, Z. Liu, M. Singh, K. V. Alwala, A. Joulin, and I. Misra, “Imagebind one embedding space to bind them all,” in _CVPR_ . IEEE, 2023, pp. 15 180–15 190. 

- [212] B. Zhu, B. Lin, M. Ning, Y. Yan, J. Cui, H. Wang, Y. Pang, W. Jiang, J. Zhang, Z. Li, C. Zhang, Z. Li, W. Liu, and L. Yuan, “Languagebind: Extending video-language pretraining to n-modality by language-based semantic alignment,” in _ICLR_ , 2024. 

- [213] I. G¨uzey, B. Evans, S. Chintala, and L. Pinto, “Dexterity from touch: Self-supervised pre-training of tactile representations with robotic play,” in _CoRL_ , vol. 229. PMLR, 2023, pp. 3142–3166. 

- [214] R. Zhang, A. Saran, B. Liu, Y. Zhu, S. Guo, S. Niekum, D. Ballard, and M. Hayhoe, “Human gaze assisted artificial intelligence: A review,” in _IJCAI-20_ , 7 2020, pp. 4951–4958, survey track. 

- [215] R. Zhang, Z. Liu, L. Zhang, J. A. Whritner, K. S. Muller, M. M. Hayhoe, and D. H. Ballard, “AGIL: learning attention from human for visuomotor tasks,” in _ECCV (11)_ , vol. 11215. Springer, 2018, pp. 692–707. 

- [216] A. Saran, R. Zhang, E. S. Short, and S. Niekum, “Efficiently guiding imitation learning agents with human gaze,” in _AAMAS_ . ACM, 2021, pp. 1109–1117. 

- [217] S. Guo, R. Zhang, B. Liu, Y. Zhu, D. H. Ballard, M. M. Hayhoe, and P. Stone, “Machine versus human attention in deep reinforcement learning tasks,” in _NeurIPS_ , 2021, pp. 25 370–25 385. 

- [218] H. M. Le, T. N. Do, and S. J. Phee, “A survey on actuators-driven surgical robots,” _Sensors and Actuators A-physical_ , vol. 247, pp. 323– 354, 2016. 

- [219] M. S. Laursen, J. S. Pedersen, S. A. Just, T. R. Savarimuthu, B. Blomholt, J. K. H. Andersen, and P. J. Vinholt, “Factors facilitating the acceptance of diagnostic robots in healthcare: A survey,” in _ICHI_ . IEEE, 2022, pp. 442–448. 

- [220] K. He, X. Zhang, S. Ren, and J. Sun, “Deep residual learning for image recognition,” in _CVPR_ . IEEE Computer Society, 2016, pp. 770–778. 

- [221] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, J. Uszkoreit, and N. Houlsby, “An image is worth 16x16 words: Transformers for image recognition at scale,” in _ICLR_ , 2021. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

23 

- [222] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W. Lo, P. Doll´ar, and R. B. Girshick, “Segment anything,” _CoRR_ , vol. abs/2304.02643, 2023. 

- [223] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” _Neural Comput._ , vol. 9, no. 8, pp. 1735–1780, 1997. 

- [224] K. Cho, B. van Merrienboer, C¸ . G¨ulc¸ehre, D. Bahdanau, F. Bougares, H. Schwenk, and Y. Bengio, “Learning phrase representations using RNN encoder-decoder for statistical machine translation,” in _EMNLP_ . ACL, 2014, pp. 1724–1734. 

- [225] OpenAI. (2023) Introducing chatgpt. [Online]. Available: https: //openai.com/blog/chatgpt 

- [226] D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. van den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam, M. Lanctot, S. Dieleman, D. Grewe, J. Nham, N. Kalchbrenner, I. Sutskever, T. P. Lillicrap, M. Leach, K. Kavukcuoglu, T. Graepel, and D. Hassabis, “Mastering the game of go with deep neural networks and tree search,” _Nat._ , vol. 529, no. 7587, pp. 484–489, 2016. 

- [227] J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov, “Proximal policy optimization algorithms,” _CoRR_ , vol. abs/1707.06347, 2017. 

- [228] OpenAI, M. Andrychowicz, B. Baker, M. Chociej, R. J´ozefowicz, B. McGrew, J. Pachocki, A. Petron, M. Plappert, G. Powell, A. Ray, J. Schneider, S. Sidor, J. Tobin, P. Welinder, L. Weng, and W. Zaremba, “Learning dexterous in-hand manipulation,” _CoRR_ , vol. abs/1808.00177, 2018. 

- [229] R. Rafailov, A. Sharma, E. Mitchell, C. D. Manning, S. Ermon, and C. Finn, “Direct preference optimization: Your language model is secretly a reward model,” in _NeurIPS_ , 2023. 

- [230] X. Chen, H. Fang, T. Lin, R. Vedantam, S. Gupta, P. Doll´ar, and C. L. Zitnick, “Microsoft COCO captions: Data collection and evaluation server,” _CoRR_ , vol. abs/1504.00325, 2015. 

- [231] S. Antol, A. Agrawal, J. Lu, M. Mitchell, D. Batra, C. L. Zitnick, and D. Parikh, “VQA: visual question answering,” in _ICCV_ . IEEE Computer Society, 2015, pp. 2425–2433. 

- [232] L. Yu, P. Poirson, S. Yang, A. C. Berg, and T. L. Berg, “Modeling context in referring expressions,” in _ECCV (2)_ , ser. Lecture Notes in Computer Science, vol. 9906. Springer, 2016, pp. 69–85. 

- [233] O. Vinyals, A. Toshev, S. Bengio, and D. Erhan, “Show and tell: A neural image caption generator,” in _CVPR_ . IEEE Computer Society, 2015, pp. 3156–3164. 

- [234] A. Radford, K. Narasimhan, T. Salimans, and I. Sutskever, “Improving language understanding by generative pre-training,” _OpenAI blog_ , 2018. 

- [235] J. Lu, D. Batra, D. Parikh, and S. Lee, “Vilbert: Pretraining taskagnostic visiolinguistic representations for vision-and-language tasks,” in _NeurIPS_ , 2019, pp. 13–23. 

- [236] A. Khan, A. Sohail, U. Zahoora, and A. S. Qureshi, “A survey of the recent architectures of deep convolutional neural networks,” _Artif. Intell. Rev._ , vol. 53, no. 8, pp. 5455–5516, 2020. 

- [237] S. H. Khan, M. Naseer, M. Hayat, S. W. Zamir, F. S. Khan, and M. Shah, “Transformers in vision: A survey,” _ACM Comput. Surv._ , vol. 54, no. 10s, pp. 200:1–200:41, 2022. 

- [238] Y. LeCun, B. E. Boser, J. S. Denker, D. Henderson, R. E. Howard, W. E. Hubbard, and L. D. Jackel, “Backpropagation applied to handwritten zip code recognition,” _Neural Comput._ , vol. 1, no. 4, pp. 541–551, 1989. 

- [239] K. Simonyan and A. Zisserman, “Very deep convolutional networks for large-scale image recognition,” in _ICLR_ , 2015. 

- [240] C. Szegedy, W. Liu, Y. Jia, P. Sermanet, S. E. Reed, D. Anguelov, D. Erhan, V. Vanhoucke, and A. Rabinovich, “Going deeper with convolutions,” in _CVPR_ . IEEE Computer Society, 2015, pp. 1–9. 

- [241] C. Szegedy, S. Ioffe, V. Vanhoucke, and A. A. Alemi, “Inception-v4, inception-resnet and the impact of residual connections on learning,” in _AAAI_ . AAAI Press, 2017, pp. 4278–4284. 

- [242] S. Xie, R. B. Girshick, P. Doll´ar, Z. Tu, and K. He, “Aggregated residual transformations for deep neural networks,” in _CVPR_ . IEEE Computer Society, 2017, pp. 5987–5995. 

- [243] J. Hu, L. Shen, and G. Sun, “Squeeze-and-excitation networks,” in _CVPR_ . Computer Vision Foundation / IEEE Computer Society, 2018, pp. 7132–7141. 

- [244] M. Tan and Q. V. Le, “Efficientnet: Rethinking model scaling for convolutional neural networks,” in _ICML_ , vol. 97. PMLR, 2019, pp. 6105–6114. 

- [245] R. B. Girshick, J. Donahue, T. Darrell, and J. Malik, “Rich feature hierarchies for accurate object detection and semantic segmentation,” in _CVPR_ . IEEE Computer Society, 2014, pp. 580–587. 

- [246] R. B. Girshick, “Fast R-CNN,” in _ICCV_ . IEEE Computer Society, 2015, pp. 1440–1448. 

- [247] S. Ren, K. He, R. B. Girshick, and J. Sun, “Faster R-CNN: towards real-time object detection with region proposal networks,” in _NIPS_ , 2015, pp. 91–99. 

- [248] K. He, G. Gkioxari, P. Doll´ar, and R. B. Girshick, “Mask R-CNN,” in _ICCV_ . IEEE Computer Society, 2017, pp. 2980–2988. 

- [249] J. Redmon, S. K. Divvala, R. B. Girshick, and A. Farhadi, “You only look once: Unified, real-time object detection,” in _CVPR_ . IEEE Computer Society, 2016, pp. 779–788. 

- [250] T. Lin, P. Doll´ar, R. B. Girshick, K. He, B. Hariharan, and S. J. Belongie, “Feature pyramid networks for object detection,” in _CVPR_ . IEEE Computer Society, 2017, pp. 936–944. 

- [251] T. Lin, P. Goyal, R. B. Girshick, K. He, and P. Doll´ar, “Focal loss for dense object detection,” in _ICCV_ . IEEE Computer Society, 2017, pp. 2999–3007. 

- [252] P. Anderson, X. He, C. Buehler, D. Teney, M. Johnson, S. Gould, and L. Zhang, “Bottom-up and top-down attention for image captioning and visual question answering,” in _CVPR_ . Computer Vision Foundation / IEEE Computer Society, 2018, pp. 6077–6086. 

- [253] J. Long, E. Shelhamer, and T. Darrell, “Fully convolutional networks for semantic segmentation,” in _CVPR_ . IEEE Computer Society, 2015, pp. 3431–3440. 

- [254] V. Badrinarayanan, A. Kendall, and R. Cipolla, “Segnet: A deep convolutional encoder-decoder architecture for image segmentation,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 39, no. 12, pp. 2481– 2495, 2017. 

- [255] O. Ronneberger, P. Fischer, and T. Brox, “U-net: Convolutional networks for biomedical image segmentation,” in _MICCAI (3)_ , ser. Lecture Notes in Computer Science, vol. 9351. Springer, 2015, pp. 234–241. 

- [256] N. Carion, F. Massa, G. Synnaeve, N. Usunier, A. Kirillov, and S. Zagoruyko, “End-to-end object detection with transformers,” in _ECCV (1)_ , ser. Lecture Notes in Computer Science, vol. 12346. Springer, 2020, pp. 213–229. 

- [257] R. Strudel, R. G. Pinel, I. Laptev, and C. Schmid, “Segmenter: Transformer for semantic segmentation,” in _ICCV_ . IEEE, 2021, pp. 7242–7252. 

- [258] A. Ioannidou, E. Chatzilari, S. Nikolopoulos, and I. Kompatsiaris, “Deep learning advances in computer vision with 3d data: A survey,” _ACM Comput. Surv._ , vol. 50, no. 2, pp. 20:1–20:38, 2017. 

- [259] E. Ahmed, A. Saint, A. E. R. Shabayek, K. Cherenkova, R. Das, G. Gusev, D. Aouada, and B. E. Ottersten, “Deep learning advances on different 3d data representations: A survey,” _CoRR_ , vol. abs/1808.01462, 2018. 

- [260] Y. Guo, H. Wang, Q. Hu, H. Liu, L. Liu, and M. Bennamoun, “Deep learning for 3d point clouds: A survey,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 43, no. 12, pp. 4338–4364, 2021. 

- [261] C. R. Qi, H. Su, M. Nießner, A. Dai, M. Yan, and L. J. Guibas, “Volumetric and multi-view cnns for object classification on 3d data,” in _CVPR_ . IEEE Computer Society, 2016, pp. 5648–5656. 

- [262] Y. Feng, Y. Feng, H. You, X. Zhao, and Y. Gao, “Meshnet: Mesh neural network for 3d shape representation,” in _AAAI_ . AAAI Press, 2019, pp. 8279–8286. 

- [263] D. W. Otter, J. R. Medina, and J. K. Kalita, “A survey of the usages of deep learning for natural language processing,” _IEEE Trans. Neural Networks Learn. Syst._ , vol. 32, no. 2, pp. 604–624, 2021. 

- [264] P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, “Pretrain, prompt, and predict: A systematic survey of prompting methods in natural language processing,” _ACM Comput. Surv._ , vol. 55, no. 9, pp. 195:1–195:35, 2023. 

- [265] Y. Bengio, R. Ducharme, and P. Vincent, “A neural probabilistic language model,” in _NIPS_ . MIT Press, 2000, pp. 932–938. 

- [266] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and J. Dean, “Distributed representations of words and phrases and their compositionality,” in _NIPS_ , 2013, pp. 3111–3119. 

- [267] T. Mikolov, K. Chen, G. Corrado, and J. Dean, “Efficient estimation of word representations in vector space,” in _ICLR (Workshop Poster)_ , 2013. 

- [268] J. Pennington, R. Socher, and C. D. Manning, “Glove: Global vectors for word representation,” in _EMNLP_ . ACL, 2014, pp. 1532–1543. 

- [269] J. L. Elman, “Finding structure in time,” _Cogn. Sci._ , vol. 14, no. 2, pp. 179–211, 1990. 

- [270] D. Bahdanau, K. Cho, and Y. Bengio, “Neural machine translation by jointly learning to align and translate,” in _ICLR_ , 2015. 

- [271] Z. Huang, W. Xu, and K. Yu, “Bidirectional LSTM-CRF models for sequence tagging,” _CoRR_ , vol. abs/1508.01991, 2015. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

24 

- [272] M. E. Peters, M. Neumann, M. Iyyer, M. Gardner, C. Clark, K. Lee, and L. Zettlemoyer, “Deep contextualized word representations,” in _NAACL-HLT_ . Association for Computational Linguistics, 2018, pp. 2227–2237. 

- [273] J. Howard and S. Ruder, “Universal language model fine-tuning for text classification,” in _ACL (1)_ . Association for Computational Linguistics, 2018, pp. 328–339. 

- [274] Y. Kim, “Convolutional neural networks for sentence classification,” in _EMNLP_ . ACL, 2014, pp. 1746–1751. 

- [275] X. Zhang, J. J. Zhao, and Y. LeCun, “Character-level convolutional networks for text classification,” in _NIPS_ , 2015, pp. 649–657. 

- [276] X. Ma and E. H. Hovy, “End-to-end sequence labeling via bidirectional lstm-cnns-crf,” in _ACL (1)_ . The Association for Computer Linguistics, 2016. 

- [277] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever _et al._ , “Language models are unsupervised multitask learners,” _OpenAI blog_ , vol. 1, no. 8, p. 9, 2019. 

- [278] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell _et al._ , “Language models are few-shot learners,” _arXiv preprint arXiv:2005.14165_ , 2020. 

- [279] OpenAI, “GPT-4 technical report,” _CoRR_ , vol. abs/2303.08774, 2023. 

- [280] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis, L. Zettlemoyer, and V. Stoyanov, “Roberta: A robustly optimized BERT pretraining approach,” _CoRR_ , vol. abs/1907.11692, 2019. 

- [281] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut, “ALBERT: A lite BERT for self-supervised learning of language representations,” in _ICLR_ , 2020. 

- [282] K. Clark, M. Luong, Q. V. Le, and C. D. Manning, “ELECTRA: pre-training text encoders as discriminators rather than generators,” in _ICLR_ , 2020. 

- [283] Z. Yang, Z. Dai, Y. Yang, J. G. Carbonell, R. Salakhutdinov, and Q. V. Le, “Xlnet: Generalized autoregressive pretraining for language understanding,” in _NeurIPS_ , 2019, pp. 5754–5764. 

- [284] S. Zhang, S. Roller, N. Goyal, M. Artetxe, M. Chen, S. Chen, C. Dewan, M. T. Diab, X. Li, X. V. Lin, T. Mihaylov, M. Ott, S. Shleifer, K. Shuster, D. Simig, P. S. Koura, A. Sridhar, T. Wang, and L. Zettlemoyer, “OPT: open pre-trained transformer language models,” _CoRR_ , vol. abs/2205.01068, 2022. 

- [285] M. Lewis, Y. Liu, N. Goyal, M. Ghazvininejad, A. Mohamed, O. Levy, V. Stoyanov, and L. Zettlemoyer, “BART: denoising sequence-tosequence pre-training for natural language generation, translation, and comprehension,” in _ACL_ . Association for Computational Linguistics, 2020, pp. 7871–7880. 

- [286] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning with a unified text-to-text transformer,” _J. Mach. Learn. Res._ , vol. 21, pp. 140:1–140:67, 2020. 

- [287] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, P. Schuh, K. Shi, S. Tsvyashchenko, J. Maynez, A. Rao, P. Barnes, Y. Tay, N. Shazeer, V. Prabhakaran, E. Reif, N. Du, B. Hutchinson, R. Pope, J. Bradbury, J. Austin, M. Isard, G. Gur-Ari, P. Yin, T. Duke, A. Levskaya, S. Ghemawat, S. Dev, H. Michalewski, X. Garcia, V. Misra, K. Robinson, L. Fedus, D. Zhou, D. Ippolito, D. Luan, H. Lim, B. Zoph, A. Spiridonov, R. Sepassi, D. Dohan, S. Agrawal, M. Omernick, A. M. Dai, T. S. Pillai, M. Pellat, A. Lewkowycz, E. Moreira, R. Child, O. Polozov, K. Lee, Z. Zhou, X. Wang, B. Saeta, M. Diaz, O. Firat, M. Catasta, J. Wei, K. Meier-Hellstern, D. Eck, J. Dean, S. Petrov, and N. Fiedel, “Palm: Scaling language modeling with pathways,” _J. Mach. Learn. Res._ , vol. 24, pp. 240:1–240:113, 2023. 

- [288] R. Anil, A. M. Dai, O. Firat, M. Johnson, D. Lepikhin, A. Passos, S. Shakeri, E. Taropa, P. Bailey, Z. Chen, E. Chu, J. H. Clark, L. E. Shafey, Y. Huang, K. Meier-Hellstern, G. Mishra, E. Moreira, M. Omernick, K. Robinson, S. Ruder, Y. Tay, K. Xiao, Y. Xu, Y. Zhang, G. H. Abrego,<sup>´</sup> J. Ahn, J. Austin, P. Barham, J. A. Botha, J. Bradbury, S. Brahma, K. Brooks, M. Catasta, Y. Cheng, C. Cherry, C. A. Choquette-Choo, A. Chowdhery, C. Crepy, S. Dave, M. Dehghani, S. Dev, J. Devlin, M. D´ıaz, N. Du, E. Dyer, V. Feinberg, F. Feng, V. Fienber, M. Freitag, X. Garcia, S. Gehrmann, L. Gonzalez, and et al., “Palm 2 technical report,” _CoRR_ , vol. abs/2305.10403, 2023. 

- [289] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M. Lachaux, T. Lacroix, B. Rozi`ere, N. Goyal, E. Hambro, F. Azhar, A. Rodriguez, A. Joulin, E. Grave, and G. Lample, “Llama: Open and efficient foundation language models,” _CoRR_ , vol. abs/2302.13971, 2023. 

- [290] H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. Bikel, L. Blecher, C. Canton-Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, 

   - J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. Hartshorn, S. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura, M. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. E. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom, “Llama 2: Open foundation and fine-tuned chat models,” _CoRR_ , vol. abs/2307.09288, 2023. 

- [291] Baidu. (2023) Introducing ernie 3.5: Baidu’s knowledge-enhanced foundation model takes a giant leap forward. [Online]. Available: http://research.baidu.com/Blog/index-view?id=185 

- [292] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano, J. Leike, and R. Lowe, “Training language models to follow instructions with human feedback,” in _NeurIPS_ , 2022. 

- [293] J. Wei, M. Bosma, V. Y. Zhao, K. Guu, A. W. Yu, B. Lester, N. Du, A. M. Dai, and Q. V. Le, “Finetuned language models are zero-shot learners,” in _ICLR_ , 2022. 

- [294] H. W. Chung, L. Hou, S. Longpre, B. Zoph, Y. Tay, W. Fedus, E. Li, X. Wang, M. Dehghani, S. Brahma, A. Webson, S. S. Gu, Z. Dai, M. Suzgun, X. Chen, A. Chowdhery, S. Narang, G. Mishra, A. Yu, V. Y. Zhao, Y. Huang, A. M. Dai, H. Yu, S. Petrov, E. H. Chi, J. Dean, J. Devlin, A. Roberts, D. Zhou, Q. V. Le, and J. Wei, “Scaling instruction-finetuned language models,” _CoRR_ , vol. abs/2210.11416, 2022. 

- [295] R. Taori, I. Gulrajani, T. Zhang, Y. Dubois, X. Li, C. Guestrin, P. Liang, and T. B. Hashimoto, “Stanford alpaca: An instruction-following llama model,” https://github.com/tatsu-lab/stanford <u>alpaca,</u> 2023. 

- [296] W.-L. Chiang, Z. Li, Z. Lin, Y. Sheng, Z. Wu, H. Zhang, L. Zheng, S. Zhuang, Y. Zhuang, J. E. Gonzalez, I. Stoica, and E. P. Xing, “Vicuna: An open-source chatbot impressing gpt-4 with 90%* chatgpt quality,” March 2023. [Online]. Available: https://lmsys.org/blog/2023-03-30-vicuna/ 

- [297] Y. Li, “Deep reinforcement learning: An overview,” _CoRR_ , vol. abs/1701.07274, 2017. 

- [298] K. Arulkumaran, M. P. Deisenroth, M. Brundage, and A. A. Bharath, “A brief survey of deep reinforcement learning,” _CoRR_ , vol. abs/1708.05866, 2017. 

- [299] W. Li, H. Luo, Z. Lin, C. Zhang, Z. Lu, and D. Ye, “A survey on transformers in reinforcement learning,” _CoRR_ , vol. abs/2301.03044, 2023. 

- [300] H. van Hasselt, A. Guez, and D. Silver, “Deep reinforcement learning with double q-learning,” in _AAAI_ . AAAI Press, 2016, pp. 2094–2100. 

- [301] M. Andrychowicz, D. Crow, A. Ray, J. Schneider, R. Fong, P. Welinder, B. McGrew, J. Tobin, P. Abbeel, and W. Zaremba, “Hindsight experience replay,” in _NIPS_ , 2017, pp. 5048–5058. 

- [302] S. Fujimoto, D. Meger, and D. Precup, “Off-policy deep reinforcement learning without exploration,” in _ICML_ , vol. 97. PMLR, 2019, pp. 2052–2062. 

- [303] A. Kumar, J. Fu, M. Soh, G. Tucker, and S. Levine, “Stabilizing offpolicy q-learning via bootstrapping error reduction,” in _NeurIPS_ , 2019, pp. 11 761–11 771. 

- [304] A. Kumar, A. Zhou, G. Tucker, and S. Levine, “Conservative q-learning for offline reinforcement learning,” in _NeurIPS_ , 2020. 

- [305] S. Levine and V. Koltun, “Guided policy search,” in _ICML (3)_ , ser. JMLR Workshop and Conference Proceedings, vol. 28. JMLR.org, 2013, pp. 1–9. 

- [306] D. Silver, G. Lever, N. Heess, T. Degris, D. Wierstra, and M. A. Riedmiller, “Deterministic policy gradient algorithms,” in _ICML_ , ser. JMLR Workshop and Conference Proceedings, vol. 32. JMLR.org, 2014, pp. 387–395. 

- [307] T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and D. Wierstra, “Continuous control with deep reinforcement learning,” in _ICLR (Poster)_ , 2016. 

- [308] V. Mnih, A. P. Badia, M. Mirza, A. Graves, T. P. Lillicrap, T. Harley, D. Silver, and K. Kavukcuoglu, “Asynchronous methods for deep reinforcement learning,” in _ICML_ , ser. JMLR Workshop and Conference Proceedings, vol. 48. JMLR.org, 2016, pp. 1928–1937. 

- [309] S. Gu, T. P. Lillicrap, I. Sutskever, and S. Levine, “Continuous deep q-learning with model-based acceleration,” in _ICML_ , ser. JMLR Workshop and Conference Proceedings, vol. 48. JMLR.org, 2016, pp. 2829–2838. 

25 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

- [310] T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, “Soft actor-critic: Offpolicy maximum entropy deep reinforcement learning with a stochastic actor,” in _ICML_ , vol. 80. PMLR, 2018, pp. 1856–1865. 

- [311] J. Schulman, S. Levine, P. Abbeel, M. I. Jordan, and P. Moritz, “Trust region policy optimization,” in _ICML_ , ser. JMLR Workshop and Conference Proceedings, vol. 37. JMLR.org, 2015, pp. 1889–1897. 

- [312] J. Schulman, P. Moritz, S. Levine, M. I. Jordan, and P. Abbeel, “High-dimensional continuous control using generalized advantage estimation,” in _ICLR (Poster)_ , 2016. 

- [313] J. Ho and S. Ermon, “Generative adversarial imitation learning,” in _NIPS_ , 2016, pp. 4565–4573. 

- [314] L. Pinto, J. Davidson, R. Sukthankar, and A. Gupta, “Robust adversarial reinforcement learning,” in _ICML_ , vol. 70. PMLR, 2017, pp. 2817– 2826. 

- [315] P. F. Christiano, J. Leike, T. B. Brown, M. Martic, S. Legg, and D. Amodei, “Deep reinforcement learning from human preferences,” in _NIPS_ , 2017, pp. 4299–4307. 

- [316] A. S. Vezhnevets, S. Osindero, T. Schaul, N. Heess, M. Jaderberg, D. Silver, and K. Kavukcuoglu, “Feudal networks for hierarchical reinforcement learning,” in _ICML_ , vol. 70. PMLR, 2017, pp. 3540– 3549. 

- [317] S. Levine, C. Finn, T. Darrell, and P. Abbeel, “End-to-end training of deep visuomotor policies,” _J. Mach. Learn. Res._ , vol. 17, pp. 39:1– 39:40, 2016. 

- [318] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke, and S. Levine, “Qt-opt: Scalable deep reinforcement learning for vision-based robotic manipulation,” _CoRR_ , vol. abs/1806.10293, 2018. 

- [319] OpenAI, I. Akkaya, M. Andrychowicz, M. Chociej, M. Litwin, B. McGrew, A. Petron, A. Paino, M. Plappert, G. Powell, R. Ribas, J. Schneider, N. Tezak, J. Tworek, P. Welinder, L. Weng, Q. Yuan, W. Zaremba, and L. Zhang, “Solving rubik’s cube with a robot hand,” _CoRR_ , vol. abs/1910.07113, 2019. 

- [320] F. Scarselli, M. Gori, A. C. Tsoi, M. Hagenbuchner, and G. Monfardini, “The graph neural network model,” _IEEE Trans. Neural Networks_ , vol. 20, no. 1, pp. 61–80, 2009. 

- [321] Z. Wu, S. Pan, F. Chen, G. Long, C. Zhang, and P. S. Yu, “A comprehensive survey on graph neural networks,” _IEEE Trans. Neural Networks Learn. Syst._ , vol. 32, no. 1, pp. 4–24, 2021. 

- [322] J. Bruna, W. Zaremba, A. Szlam, and Y. LeCun, “Spectral networks and locally connected networks on graphs,” in _ICLR_ , 2014. 

- [323] M. Defferrard, X. Bresson, and P. Vandergheynst, “Convolutional neural networks on graphs with fast localized spectral filtering,” in _NIPS_ , 2016, pp. 3837–3845. 

- [324] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” in _ICLR (Poster)_ , 2017. 

- [325] A. Micheli, “Neural network for graphs: A contextual constructive approach,” _IEEE Trans. Neural Networks_ , vol. 20, no. 3, pp. 498–511, 2009. 

- [326] J. Gilmer, S. S. Schoenholz, P. F. Riley, O. Vinyals, and G. E. Dahl, “Neural message passing for quantum chemistry,” in _ICML_ , vol. 70. PMLR, 2017, pp. 1263–1272. 

- [327] K. Xu, W. Hu, J. Leskovec, and S. Jegelka, “How powerful are graph neural networks?” in _ICLR_ , 2019. 

- [328] W. L. Hamilton, Z. Ying, and J. Leskovec, “Inductive representation learning on large graphs,” in _NIPS_ , 2017, pp. 1024–1034. 

- [329] P. Velickovic, G. Cucurull, A. Casanova, A. Romero, P. Li`o, and Y. Bengio, “Graph attention networks,” in _ICLR (Poster)_ , 2018. 

- [330] S. Cao, W. Lu, and Q. Xu, “Deep neural networks for learning graph representations,” in _AAAI_ . AAAI Press, 2016, pp. 1145–1152. 

- [331] T. N. Kipf and M. Welling, “Variational graph auto-encoders,” _CoRR_ , vol. abs/1611.07308, 2016. 

- [332] Y. Seo, M. Defferrard, P. Vandergheynst, and X. Bresson, “Structured sequence modeling with graph convolutional recurrent networks,” in _ICONIP (1)_ , ser. Lecture Notes in Computer Science, vol. 11301. Springer, 2018, pp. 362–373. 

- [333] W. Du, H. Zhang, Y. Du, Q. Meng, W. Chen, N. Zheng, B. Shao, and T. Liu, “SE(3) equivariant graph neural networks with complete local frames,” in _ICML_ , vol. 162. PMLR, 2022, pp. 5583–5608. 

- [334] V. G. Satorras, E. Hoogeboom, and M. Welling, “E(n) equivariant graph neural networks,” in _ICML_ , vol. 139. PMLR, 2021, pp. 9323–9332. 

- [335] Y. Rong, Y. Bian, T. Xu, W. Xie, Y. Wei, W. Huang, and J. Huang, “Self-supervised graph transformer on large-scale molecular data,” in _NeurIPS_ , 2020. 

- [336] F. Fuchs, D. E. Worrall, V. Fischer, and M. Welling, “Se(3)transformers: 3d roto-translation equivariant attention networks,” in _NeurIPS_ , 2020. 

- [337] R. Krishna, Y. Zhu, O. Groth, J. Johnson, K. Hata, J. Kravitz, S. Chen, Y. Kalantidis, L. Li, D. A. Shamma, M. S. Bernstein, and L. Fei-Fei, “Visual genome: Connecting language and vision using crowdsourced dense image annotations,” _Int. J. Comput. Vis._ , vol. 123, no. 1, pp. 32–73, 2017. 

- [338] L. Wu, Y. Chen, K. Shen, X. Guo, H. Gao, S. Li, J. Pei, and B. Long, “Graph neural networks for natural language processing: A survey,” _Found. Trends Mach. Learn._ , vol. 16, no. 2, pp. 119–328, 2023. 

- [339] D. Ghosal, N. Majumder, S. Poria, N. Chhaya, and A. F. Gelbukh, “Dialoguegcn: A graph convolutional neural network for emotion recognition in conversation,” in _EMNLP/IJCNLP (1)_ . Association for Computational Linguistics, 2019, pp. 154–164. 

- [340] W. Zhong, J. Xu, D. Tang, Z. Xu, N. Duan, M. Zhou, J. Wang, and J. Yin, “Reasoning over semantic-level graph for fact checking,” in _ACL_ . Association for Computational Linguistics, 2020, pp. 6170– 6180. 

- [341] L. Wang, Y. Li, O.<sup>¨</sup> Aslan, and O. Vinyals, “Wikigraphs: A wikipedia text - knowledge graph paired dataset,” _CoRR_ , vol. abs/2107.09556, 2021. 

- [342] J. Tang, J. Zhang, L. Yao, J. Li, L. Zhang, and Z. Su, “Arnetminer: extraction and mining of academic social networks,” in _KDD_ . ACM, 2008, pp. 990–998. 

- [343] H. Tan and M. Bansal, “LXMERT: learning cross-modality encoder representations from transformers,” in _EMNLP/IJCNLP (1)_ . Association for Computational Linguistics, 2019, pp. 5099–5110. 

- [344] L. H. Li, M. Yatskar, D. Yin, C. Hsieh, and K. Chang, “Visualbert: A simple and performant baseline for vision and language,” _CoRR_ , vol. abs/1908.03557, 2019. 

- [345] W. Su, X. Zhu, Y. Cao, B. Li, L. Lu, F. Wei, and J. Dai, “VL-BERT: pre-training of generic visual-linguistic representations,” in _ICLR_ , 2020. 

- [346] Y. Chen, L. Li, L. Yu, A. E. Kholy, F. Ahmed, Z. Gan, Y. Cheng, and J. Liu, “UNITER: universal image-text representation learning,” in _ECCV (30)_ , ser. Lecture Notes in Computer Science, vol. 12375. Springer, 2020, pp. 104–120. 

- [347] W. Kim, B. Son, and I. Kim, “Vilt: Vision-and-language transformer without convolution or region supervision,” in _ICML_ , vol. 139. PMLR, 2021, pp. 5583–5594. 

- [348] Z. Wang, J. Yu, A. W. Yu, Z. Dai, Y. Tsvetkov, and Y. Cao, “Simvlm: Simple visual language model pretraining with weak supervision,” in _ICLR_ , 2022. 

- [349] Z. Dai, H. Liu, Q. V. Le, and M. Tan, “Coatnet: Marrying convolution and attention for all data sizes,” in _NeurIPS_ , 2021, pp. 3965–3977. 

- [350] J. Wang, Z. Yang, X. Hu, L. Li, K. Lin, Z. Gan, Z. Liu, C. Liu, and L. Wang, “GIT: A generative image-to-text transformer for vision and language,” _Trans. Mach. Learn. Res._ , vol. 2022, 2022. 

- [351] L. Yuan, D. Chen, Y. Chen, N. Codella, X. Dai, J. Gao, H. Hu, X. Huang, B. Li, C. Li, C. Liu, M. Liu, Z. Liu, Y. Lu, Y. Shi, L. Wang, J. Wang, B. Xiao, Z. Xiao, J. Yang, M. Zeng, L. Zhou, and P. Zhang, “Florence: A new foundation model for computer vision,” _CoRR_ , vol. abs/2111.11432, 2021. 

- [352] W. Wang, H. Bao, L. Dong, J. Bjorck, Z. Peng, Q. Liu, K. Aggarwal, O. K. Mohammed, S. Singhal, S. Som, and F. Wei, “Image as a foreign language: BEIT pretraining for vision and vision-language tasks,” in _CVPR_ . IEEE, 2023, pp. 19 175–19 186. 

- [353] L. Yao, R. Huang, L. Hou, G. Lu, M. Niu, H. Xu, X. Liang, Z. Li, X. Jiang, and C. Xu, “FILIP: fine-grained interactive language-image pre-training,” in _ICLR_ , 2022. 

- [354] C. Jia, Y. Yang, Y. Xia, Y. Chen, Z. Parekh, H. Pham, Q. V. Le, Y. Sung, Z. Li, and T. Duerig, “Scaling up visual and vision-language representation learning with noisy text supervision,” in _ICML_ , vol. 139. PMLR, 2021, pp. 4904–4916. 

- [355] Q. Xie, M. Luong, E. H. Hovy, and Q. V. Le, “Self-training with noisy student improves imagenet classification,” in _CVPR_ . Computer Vision Foundation / IEEE, 2020, pp. 10 684–10 695. 

- [356] J. Li, R. R. Selvaraju, A. Gotmare, S. R. Joty, C. Xiong, and S. C. Hoi, “Align before fuse: Vision and language representation learning with momentum distillation,” in _NeurIPS_ , 2021, pp. 9694–9705. 

- [357] A. Singh, R. Hu, V. Goswami, G. Couairon, W. Galuba, M. Rohrbach, and D. Kiela, “FLAVA: A foundational language and vision alignment model,” in _CVPR_ . IEEE, 2022, pp. 15 617–15 629. 

- [358] Z. Liu, Y. Lin, Y. Cao, H. Hu, Y. Wei, Z. Zhang, S. Lin, and B. Guo, “Swin transformer: Hierarchical vision transformer using shifted windows,” in _ICCV_ . IEEE, 2021, pp. 9992–10 002. 

- [359] H. Wu, B. Xiao, N. Codella, M. Liu, X. Dai, L. Yuan, and L. Zhang, “Cvt: Introducing convolutions to vision transformers,” in _ICCV_ . IEEE, 2021, pp. 22–31. 

26 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

- [360] A. Brock, S. De, S. L. Smith, and K. Simonyan, “High-performance large-scale image recognition without normalization,” in _ICML_ , vol. 139. PMLR, 2021, pp. 1059–1071. 

- [361] J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, E. Rutherford, D. de Las Casas, L. A. Hendricks, J. Welbl, A. Clark, T. Hennigan, E. Noland, K. Millican, G. van den Driessche, B. Damoc, A. Guy, S. Osindero, K. Simonyan, E. Elsen, J. W. Rae, O. Vinyals, and L. Sifre, “Training compute-optimal large language models,” _CoRR_ , vol. abs/2203.15556, 2022. 

- [362] Y. Fang, W. Wang, B. Xie, Q. Sun, L. Wu, X. Wang, T. Huang, X. Wang, and Y. Cao, “EVA: exploring the limits of masked visual representation learning at scale,” in _CVPR_ . IEEE, 2023, pp. 19 358– 19 369. 

- [363] X. Chen, X. Wang, S. Changpinyo, A. J. Piergiovanni, P. Padlewski, D. Salz, S. Goodman, A. Grycner, B. Mustafa, L. Beyer, A. Kolesnikov, J. Puigcerver, N. Ding, K. Rong, H. Akbari, G. Mishra, L. Xue, A. V. Thapliyal, J. Bradbury, and W. Kuo, “Pali: A jointly-scaled multilingual language-image model,” in _ICLR_ , 2023. 

- [364] L. Xue, N. Constant, A. Roberts, M. Kale, R. Al-Rfou, A. Siddhant, A. Barua, and C. Raffel, “mt5: A massively multilingual pre-trained text-to-text transformer,” in _NAACL-HLT_ . Association for Computational Linguistics, 2021, pp. 483–498. 

- [365] X. Chen, J. Djolonga, P. Padlewski, B. Mustafa, S. Changpinyo, J. Wu, C. R. Ruiz, S. Goodman, X. Wang, Y. Tay, S. Shakeri, M. Dehghani, D. Salz, M. Lucic, M. Tschannen, A. Nagrani, H. Hu, M. Joshi, B. Pang, C. Montgomery, P. Pietrzyk, M. Ritter, A. J. Piergiovanni, M. Minderer, F. Pavetic, A. Waters, G. Li, I. Alabdulmohsin, L. Beyer, J. Amelot, K. Lee, A. P. Steiner, Y. Li, D. Keysers, A. Arnab, Y. Xu, K. Rong, A. Kolesnikov, M. Seyedhosseini, A. Angelova, X. Zhai, N. Houlsby, and R. Soricut, “Pali-x: On scaling up a multilingual vision and language model,” _CoRR_ , vol. abs/2305.18565, 2023. 

- [366] M. Dehghani, J. Djolonga, B. Mustafa, P. Padlewski, J. Heek, J. Gilmer, A. Steiner, M. Caron, R. Geirhos, I. Alabdulmohsin, R. Jenatton, L. Beyer, M. Tschannen, A. Arnab, X. Wang, C. Riquelme, M. Minderer, J. Puigcerver, U. Evci, M. Kumar, S. van Steenkiste, G. F. Elsayed, A. Mahendran, F. Yu, A. Oliver, F. Huot, J. Bastings, M. P. Collier, A. A. Gritsenko, V. Birodkar, C. Vasconcelos, Y. Tay, T. Mensink, A. Kolesnikov, F. Pavetic, D. Tran, T. Kipf, M. Lucic, X. Zhai, D. Keysers, J. Harmsen, and N. Houlsby, “Scaling vision transformers to 22 billion parameters,” _CoRR_ , vol. abs/2302.05442, 2023. 

- [367] Y. Tay, M. Dehghani, V. Q. Tran, X. Garcia, J. Wei, X. Wang, H. W. Chung, D. Bahri, T. Schuster, H. S. Zheng, D. Zhou, N. Houlsby, and D. Metzler, “UL2: unifying language learning paradigms,” in _ICLR_ , 2023. 

- [368] R. Zhang, J. Han, A. Zhou, X. Hu, S. Yan, P. Lu, H. Li, P. Gao, and Y. Qiao, “Llama-adapter: Efficient fine-tuning of language models with zero-init attention,” _CoRR_ , vol. abs/2303.16199, 2023. 

- [369] P. Gao, J. Han, R. Zhang, Z. Lin, S. Geng, A. Zhou, W. Zhang, P. Lu, C. He, X. Yue, H. Li, and Y. Qiao, “Llama-adapter V2: parameterefficient visual instruction model,” _CoRR_ , vol. abs/2304.15010, 2023. 

- [370] S. Huang, L. Dong, W. Wang, Y. Hao, S. Singhal, S. Ma, T. Lv, L. Cui, O. K. Mohammed, B. Patra, Q. Liu, K. Aggarwal, Z. Chi, J. Bjorck, V. Chaudhary, S. Som, X. Song, and F. Wei, “Language is not all you need: Aligning perception with language models,” _CoRR_ , vol. abs/2302.14045, 2023. 

- [371] Z. Peng, W. Wang, L. Dong, Y. Hao, S. Huang, S. Ma, and F. Wei, “Kosmos-2: Grounding multimodal large language models to the world,” _CoRR_ , vol. abs/2306.14824, 2023. 

- [372] H. Wang, S. Ma, S. Huang, L. Dong, W. Wang, Z. Peng, Y. Wu, P. Bajaj, S. Singhal, A. Benhaim, B. Patra, Z. Liu, V. Chaudhary, X. Song, and F. Wei, “Foundation transformers,” _CoRR_ , vol. abs/2210.06423, 2022. 

- [373] W. Dai, J. Li, D. Li, A. M. H. Tiong, J. Zhao, W. Wang, B. Li, P. Fung, and S. C. H. Hoi, “Instructblip: Towards general-purpose visionlanguage models with instruction tuning,” _CoRR_ , vol. abs/2305.06500, 2023. 

- [374] D. Zhu, J. Chen, X. Shen, X. Li, and M. Elhoseiny, “Minigpt-4: Enhancing vision-language understanding with advanced large language models,” _CoRR_ , vol. abs/2304.10592, 2023. 

- [375] H. Zhang, X. Li, and L. Bing, “Video-llama: An instruction-tuned audio-visual language model for video understanding,” _CoRR_ , vol. abs/2306.02858, 2023. 

- [376] Y. Su, T. Lan, H. Li, J. Xu, Y. Wang, and D. Cai, “Pandagpt: One model to instruction-follow them all,” _CoRR_ , vol. abs/2305.16355, 2023. 

- [377] K. Li, Y. He, Y. Wang, Y. Li, W. Wang, P. Luo, Y. Wang, L. Wang, and Y. Qiao, “Videochat: Chat-centric video understanding,” _CoRR_ , vol. abs/2305.06355, 2023. 

- [378] S. contributors. (2023) Stablelm: Stability ai language models. [Online]. Available: https://github.com/stability-AI/stableLM 

- [379] L. Zhao, E. Yu, Z. Ge, J. Yang, H. Wei, H. Zhou, J. Sun, Y. Peng, R. Dong, C. Han, and X. Zhang, “Chatspot: Bootstrapping multimodal llms via precise referring instruction tuning,” _CoRR_ , vol. abs/2307.09474, 2023. 

- [380] Q. Ye, H. Xu, G. Xu, J. Ye, M. Yan, Y. Zhou, J. Wang, A. Hu, P. Shi, Y. Shi, C. Li, Y. Xu, H. Chen, J. Tian, Q. Qi, J. Zhang, and F. Huang, “mplug-owl: Modularization empowers large language models with multimodality,” _CoRR_ , vol. abs/2304.14178, 2023. 

- [381] Q. Ye, H. Xu, J. Ye, M. Yan, A. Hu, H. Liu, Q. Qian, J. Zhang, F. Huang, and J. Zhou, “mplug-owl2: Revolutionizing multi-modal large language model with modality collaboration,” _CoRR_ , vol. abs/2311.04257, 2023. 

- [382] C. Xu, D. Guo, N. Duan, and J. J. McAuley, “Baize: An opensource chat model with parameter-efficient tuning on self-chat data,” in _EMNLP_ . Association for Computational Linguistics, 2023, pp. 6268–6278. 

- [383] C. Wu, S. Yin, W. Qi, X. Wang, Z. Tang, and N. Duan, “Visual chatgpt: Talking, drawing and editing with visual foundation models,” _CoRR_ , vol. abs/2303.04671, 2023. 

- [384] F. Chen, M. Han, H. Zhao, Q. Zhang, J. Shi, S. Xu, and B. Xu, “XLLM: bootstrapping advanced large language models by treating multimodalities as foreign languages,” _CoRR_ , vol. abs/2305.04160, 2023. 

- [385] X. Zhai, A. Kolesnikov, N. Houlsby, and L. Beyer, “Scaling vision transformers,” in _CVPR_ . IEEE, 2022, pp. 1204–1213. 

- [386] Z. Du, Y. Qian, X. Liu, M. Ding, J. Qiu, Z. Yang, and J. Tang, “GLM: general language model pretraining with autoregressive blank infilling,” in _ACL (1)_ . Association for Computational Linguistics, 2022, pp. 320– 335. 

- [387] F. Chen, D. Zhang, M. Han, X. Chen, J. Shi, S. Xu, and B. Xu, “VLP: A survey on vision-language pre-training,” _Int. J. Autom. Comput._ , vol. 20, no. 1, pp. 38–56, 2023. 

- [388] P. Xu, X. Zhu, and D. A. Clifton, “Multimodal learning with transformers: A survey,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 45, no. 10, pp. 12 113–12 132, 2023. 

- [389] X. Wang, G. Chen, G. Qian, P. Gao, X. Wei, Y. Wang, Y. Tian, and W. Gao, “Large-scale multi-modal pre-trained models: A comprehensive survey,” _Mach. Intell. Res._ , vol. 20, no. 4, pp. 447–482, 2023. 

- [390] J. Zhang, J. Huang, S. Jin, and S. Lu, “Vision-language models for vision tasks: A survey,” _CoRR_ , vol. abs/2304.00685, 2023. 

- [391] C. Sun, A. Myers, C. Vondrick, K. Murphy, and C. Schmid, “Videobert: A joint model for video and language representation learning,” in _ICCV_ . IEEE, 2019, pp. 7463–7472. 

- [392] H. Bao, W. Wang, L. Dong, Q. Liu, O. K. Mohammed, K. Aggarwal, S. Som, S. Piao, and F. Wei, “Vlmo: Unified vision-language pretraining with mixture-of-modality-experts,” in _NeurIPS_ , 2022. 

- [393] X. Zhai, X. Wang, B. Mustafa, A. Steiner, D. Keysers, A. Kolesnikov, and L. Beyer, “Lit: Zero-shot transfer with locked-image text tuning,” in _CVPR_ . IEEE, 2022, pp. 18 102–18 112. 

- [394] M. Tsimpoukelli, J. Menick, S. Cabi, S. M. A. Eslami, O. Vinyals, and F. Hill, “Multimodal few-shot learning with frozen language models,” in _NeurIPS_ , 2021, pp. 200–212. 

- [395] J. Yu, Z. Wang, V. Vasudevan, L. Yeung, M. Seyedhosseini, and Y. Wu, “Coca: Contrastive captioners are image-text foundation models,” _Trans. Mach. Learn. Res._ , vol. 2022, 2022. 

- [396] P. Wang, A. Yang, R. Men, J. Lin, S. Bai, Z. Li, J. Ma, C. Zhou, J. Zhou, and H. Yang, “OFA: unifying architectures, tasks, and modalities through a simple sequence-to-sequence learning framework,” in _ICML_ , vol. 162. PMLR, 2022, pp. 23 318–23 340. 

- [397] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen, “Lora: Low-rank adaptation of large language models,” in _ICLR_ , 2022. 

- [398] P. Esser, R. Rombach, and B. Ommer, “Taming transformers for highresolution image synthesis,” in _CVPR_ . Computer Vision Foundation / IEEE, 2021, pp. 12 873–12 883. 

- [399] C. Zheng, T. Vuong, J. Cai, and D. Phung, “Movq: Modulating quantized vectors for high-fidelity image generation,” in _NeurIPS_ , 2022. 

- [400] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, “Sigmoid loss for language image pre-training,” in _ICCV_ . IEEE, 2023, pp. 11 941– 11 952. 

- [401] X. Gu, T. Lin, W. Kuo, and Y. Cui, “Open-vocabulary object detection via vision and language knowledge distillation,” in _ICLR_ , 2022. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

27 

- [402] A. Kamath, M. Singh, Y. LeCun, G. Synnaeve, I. Misra, and N. Carion, “MDETR - modulated detection for end-to-end multi-modal understanding,” in _ICCV_ . IEEE, 2021, pp. 1760–1770. 

- [403] V. Blukis, C. Paxton, D. Fox, A. Garg, and Y. Artzi, “A persistent spatial semantic representation for high-level natural language instruction execution,” in _CoRL_ , vol. 164. PMLR, 2021, pp. 706–717. 

- [404] K. He, X. Chen, S. Xie, Y. Li, P. Doll´ar, and R. B. Girshick, “Masked autoencoders are scalable vision learners,” in _CVPR_ . IEEE, 2022, pp. 15 979–15 988. 

- [405] M. Minderer, A. A. Gritsenko, A. Stone, M. Neumann, D. Weissenborn, A. Dosovitskiy, A. Mahendran, A. Arnab, M. Dehghani, Z. Shen, X. Wang, X. Zhai, T. Kipf, and N. Houlsby, “Simple open-vocabulary object detection with vision transformers,” _CoRR_ , vol. abs/2205.06230, 2022. 

- [406] Z. Liu, H. Mao, C. Wu, C. Feichtenhofer, T. Darrell, and S. Xie, “A convnet for the 2020s,” in _CVPR_ . IEEE, 2022, pp. 11 966–11 976. 

- [407] J. Ho, W. Chan, C. Saharia, J. Whang, R. Gao, A. A. Gritsenko, D. P. Kingma, B. Poole, M. Norouzi, D. J. Fleet, and T. Salimans, “Imagen video: High definition video generation with diffusion models,” _CoRR_ , vol. abs/2210.02303, 2022. 

- [408] R. Villegas, M. Babaeizadeh, P. Kindermans, H. Moraldo, H. Zhang, M. T. Saffar, S. Castro, J. Kunze, and D. Erhan, “Phenaki: Variable length video generation from open domain textual descriptions,” in _ICLR_ . OpenReview.net, 2023. 

- [409] M. S. M. Sajjadi, D. Duckworth, A. Mahendran, S. van Steenkiste, F. Pavetic, M. Lucic, L. J. Guibas, K. Greff, and T. Kipf, “Object scene representation transformer,” in _NeurIPS_ , 2022. 

- [410] C. R. Qi, H. Su, K. Mo, and L. J. Guibas, “Pointnet: Deep learning on point sets for 3d classification and segmentation,” in _CVPR_ . IEEE Computer Society, 2017, pp. 77–85. 

- [411] C. R. Qi, L. Yi, H. Su, and L. J. Guibas, “Pointnet++: Deep hierarchical feature learning on point sets in a metric space,” in _NIPS_ , 2017, pp. 5099–5108. 

- [412] Y. Hong, C. Lin, Y. Du, Z. Chen, J. B. Tenenbaum, and C. Gan, “3d concept learning and reasoning from multi-view images,” in _CVPR_ . IEEE, 2023, pp. 9202–9212. 

- [413] K. M. Jatavallabhula, A. Kuwajerwala, Q. Gu, M. Omama, G. Iyer, S. Saryazdi, T. Chen, A. Maalouf, S. Li, N. V. Keetha, A. Tewari, J. B. Tenenbaum, C. M. de Melo, K. M. Krishna, L. Paull, F. Shkurti, and A. Torralba, “Conceptfusion: Open-set multimodal 3d mapping,” in _RSS_ , 2023. 

- [414] N. Reimers and I. Gurevych, “Sentence-bert: Sentence embeddings using siamese bert-networks,” in _EMNLP/IJCNLP (1)_ . Association for Computational Linguistics, 2019, pp. 3980–3990. 

- [415] V. Sanh, L. Debut, J. Chaumond, and T. Wolf, “Distilbert, a distilled version of BERT: smaller, faster, cheaper and lighter,” _CoRR_ , vol. abs/1910.01108, 2019. 

- [416] M. N. Team. (2023) Introducing mpt-7b: A new standard for opensource, commercially usable llms. Accessed: 2023-05-05. [Online]. Available: www.mosaicml.com/blog/mpt-7b 

- [417] A. Awadalla, I. Gao, J. Gardner, J. Hessel, Y. Hanafy, W. Zhu, K. Marathe, Y. Bitton, S. Y. Gadre, S. Sagawa, J. Jitsev, S. Kornblith, P. W. Koh, G. Ilharco, M. Wortsman, and L. Schmidt, “Openflamingo: An open-source framework for training large autoregressive visionlanguage models,” _CoRR_ , vol. abs/2308.01390, 2023. 

- [418] S. Biderman, H. Schoelkopf, Q. G. Anthony, H. Bradley, K. O’Brien, E. Hallahan, M. A. Khan, S. Purohit, U. S. Prashanth, E. Raff, A. Skowron, L. Sutawika, and O. van der Wal, “Pythia: A suite for analyzing large language models across training and scaling,” in _ICML_ , vol. 202. PMLR, 2023, pp. 2397–2430. 

- [419] M. Javaheripi, S. Bubeck, M. Abdin, J. Aneja, S. Bubeck, C. C. T. Mendes, W. Chen, A. Del Giorno, R. Eldan, S. Gopi _et al._ , “Phi-2: The surprising power of small language models,” _Microsoft Research Blog_ , 2023. 

- [420] S. Black, S. Biderman, E. Hallahan, Q. Anthony, L. Gao, L. Golding, H. He, C. Leahy, K. McDonell, J. Phang, M. Pieler, U. S. Prashanth, S. Purohit, L. Reynolds, J. Tow, B. Wang, and S. Weinbach, “Gptneox-20b: An open-source autoregressive language model,” _CoRR_ , vol. abs/2204.06745, 2022. 

- [421] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, 

   - A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba, “Evaluating large language models trained on code,” _CoRR_ , vol. abs/2107.03374, 2021. 

- [422] S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh, “Prismatic vlms: Investigating the design space of visuallyconditioned language models,” in _ICML_ , 2024. 

- [423] L. Beyer, A. Steiner, A. S. Pinto, A. Kolesnikov, X. Wang, D. Salz, M. Neumann, I. Alabdulmohsin, M. Tschannen, E. Bugliarello, T. Unterthiner, D. Keysers, S. Koppula, F. Liu, A. Grycner, A. A. Gritsenko, N. Houlsby, M. Kumar, K. Rong, J. Eisenschlos, R. Kabra, M. Bauer, M. Bosnjak, X. Chen, M. Minderer, P. Voigtlaender, I. Bica, I. Balazevic, J. Puigcerver, P. Papalampidi, O. J. H´enaff, X. Xiong, R. Soricut, J. Harmsen, and X. Zhai, “Paligemma: A versatile 3b VLM for transfer,” _CoRR_ , vol. abs/2407.07726, 2024. 

- [424] A. Steiner, A. S. Pinto, M. Tschannen, D. Keysers, X. Wang, Y. Bitton, A. A. Gritsenko, M. Minderer, A. Sherbondy, S. Long, S. Qin, R. R. Ingle, E. Bugliarello, S. Kazemzadeh, T. Mesnard, I. Alabdulmohsin, L. Beyer, and X. Zhai, “Paligemma 2: A family of versatile vlms for transfer,” _CoRR_ , vol. abs/2412.03555, 2024. 

- [425] Chameleon-Team, “Chameleon: Mixed-modal early-fusion foundation models,” _CoRR_ , vol. abs/2405.09818, 2024. 

- [426] X. Wang, X. Zhang, Z. Luo, Q. Sun, Y. Cui, J. Wang, F. Zhang, Y. Wang, Z. Li, Q. Yu, Y. Zhao, Y. Ao, X. Min, T. Li, B. Wu, B. Zhao, B. Zhang, L. Wang, G. Liu, Z. He, X. Yang, J. Liu, Y. Lin, T. Huang, and Z. Wang, “Emu3: Next-token prediction is all you need,” _CoRR_ , vol. abs/2409.18869, 2024. 

- [427] H. Liu, W. Yan, M. Zaharia, and P. Abbeel, “World model on millionlength video and language with blockwise ringattention,” in _ICLR_ . OpenReview.net, 2025. 

- [428] D. K. Misra, A. Bennett, V. Blukis, E. Niklasson, M. Shatkhin, and Y. Artzi, “Mapping instructions to actions in 3d environments with visual goal prediction,” in _EMNLP_ , 2018, pp. 2667–2678. 

- [429] C. Lynch, M. Khansari, T. Xiao, V. Kumar, J. Tompson, S. Levine, and P. Sermanet, “Learning latent plans from play,” in _CoRL_ , vol. 100. PMLR, 2019, pp. 1113–1132. 

- [430] M. Bhardwaj, B. Sundaralingam, A. Mousavian, N. D. Ratliff, D. Fox, F. Ramos, and B. Boots, “STORM: an integrated framework for fast joint-space model-predictive control for reactive manipulation,” in _CoRL_ , vol. 164. PMLR, 2021, pp. 750–759. 

- [431] A. Jaegle, S. Borgeaud, J. Alayrac, C. Doersch, C. Ionescu, D. Ding, S. Koppula, D. Zoran, A. Brock, E. Shelhamer, O. J. H´enaff, M. M. Botvinick, A. Zisserman, O. Vinyals, and J. Carreira, “Perceiver IO: A general architecture for structured inputs & outputs,” in _ICLR_ , 2022. 

- [432] E. Wijmans, A. Kadian, A. Morcos, S. Lee, I. Essa, D. Parikh, M. Savva, and D. Batra, “DD-PPO: learning near-perfect pointgoal navigators from 2.5 billion frames,” in _ICLR_ , 2020. 

- [433] M. Zhu, Y. Zhu, J. Li, J. Wen, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang, “Scaling diffusion policy in transformer to 1 billion parameters for robotic manipulation,” _CoRR_ , vol. abs/2409.14411, 2024. 

- [434] J. W. Wei, L. Hou, A. K. Lampinen, X. Chen, D. Huang, Y. Tay, X. Chen, Y. Lu, D. Zhou, T. Ma, and Q. V. Le, “Symbol tuning improves in-context learning in language models,” _CoRR_ , vol. abs/2305.08298, 2023. 

- [435] W. Peebles and S. Xie, “Scalable diffusion models with transformers,” in _ICCV_ . IEEE, 2023, pp. 4172–4182. 

- [436] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” in _NeurIPS_ , 2020. 

- [437] Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole, “Score-based generative modeling through stochastic differential equations,” in _ICLR_ , 2021. 

- [438] A. Zeng, P. Florence, J. Tompson, S. Welker, J. Chien, M. Attarian, T. Armstrong, I. Krasin, D. Duong, V. Sindhwani, and J. Lee, “Transporter networks: Rearranging the visual world for robotic manipulation,” in _CoRL_ , vol. 155. PMLR, 2020, pp. 726–747. 

- [439] R. Goyal, S. E. Kahou, V. Michalski, J. Materzynska, S. Westphal, H. Kim, V. Haenel, I. Fr¨und, P. Yianilos, M. Mueller-Freitag, F. Hoppe, C. Thurau, I. Bax, and R. Memisevic, “The ”something something” video database for learning and evaluating visual common sense,” in _ICCV_ . IEEE Computer Society, 2017, pp. 5843–5851. 

- [440] X. Lin, J. So, S. Mahalingam, F. Liu, and P. Abbeel, “Spawnnet: Learning generalizable visuomotor skills from pre-trained networks,” _CoRR_ , vol. abs/2307.03567, 2023. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

28 

- [441] S. P. Arunachalam, I. G¨uzey, S. Chintala, and L. Pinto, “Holo-dex: Teaching dexterity with immersive mixed reality,” in _ICRA_ . IEEE, 2023, pp. 5962–5969. 

- [442] N. M. M. Shafiullah, A. Rai, H. Etukuru, Y. Liu, I. Misra, S. Chintala, and L. Pinto, “On bringing robots home,” _CoRR_ , vol. abs/2311.16098, 2023. 

- [443] Y. Seo, D. Hafner, H. Liu, F. Liu, S. James, K. Lee, and P. Abbeel, “Masked world models for visual control,” in _CoRL_ , vol. 205. PMLR, 2022, pp. 1332–1344. 

- [444] R. Mendonca, S. Bahl, and D. Pathak, “Structured world models from human videos,” in _RSS_ , 2023. 

- [445] M. Pan, X. Zhu, Y. Wang, and X. Yang, “Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models,” in _NeurIPS_ , 2022. 

- [446] Z. Dai, Z. Yang, Y. Yang, J. G. Carbonell, Q. V. Le, and R. Salakhutdinov, “Transformer-xl: Attentive language models beyond a fixed-length context,” in _ACL (1)_ . Association for Computational Linguistics, 2019, pp. 2978–2988. 

- [447] A. Avetisyan, C. Xie, H. Howard-Jenkins, T. Yang, S. Aroudj, S. Patra, F. Zhang, D. P. Frost, L. Holland, C. Orme, J. Engel, E. Miller, R. A. Newcombe, and V. Balntas, “Scenescript: Reconstructing scenes with an autoregressive structured language model,” _CoRR_ , vol. abs/2403.13064, 2024. 

- [448] N. M. Shafiullah, Z. J. Cui, A. Altanzaya, and L. Pinto, “Behavior transformers: Cloning $k$ modes with one stone,” in _NeurIPS_ , 2022. 

- [449] Z. J. Cui, Y. Wang, N. M. M. Shafiullah, and L. Pinto, “From play to policy: Conditional behavior generation from uncurated robot data,” in _ICLR_ , 2023. 

- [450] S. Lee, Y. Wang, H. Etukuru, H. J. Kim, N. M. M. Shafiullah, and L. Pinto, “Behavior generation with latent actions,” in _ICML_ , 2024. 

- [451] R. Sapkota, Y. Cao, K. I. Roumeliotis, and M. Karkee, “Visionlanguage-action models: Concepts, progress, applications and challenges,” _CoRR_ , vol. abs/2505.04769, 2025. 

- [452] Y. Zhong, F. Bai, S. Cai, X. Huang, Z. Chen, X. Zhang, Y. Wang, S. Guo, T. Guan, K. N. Lui, Z. Qi, Y. Liang, Y. Chen, and Y. Yang, “A survey on vision-language-action models: An action tokenization perspective,” _CoRR_ , vol. abs/2507.01925, 2025. 

- [453] M. U. Din, W. Akram, L. S. Saoud, J. Rosell, and I. Hussain, “Vision language action models in robotic manipulation: A systematic review,” _CoRR_ , vol. abs/2507.10672, 2025. 

- [454] D. Zhang, J. Sun, C. Hu, X. Wu, Z. Yuan, R. Zhou, F. Shen, and Q. Zhou, “Pure vision language action (VLA) models: A comprehensive survey,” _CoRR_ , vol. abs/2509.19012, 2025. 

- [455] S. Li, Y. Chen, L. Dong, S. Liu, D. Lan, L. Yu, and Z. Pang, “Transferring vision-language-action models to industry applications: Architectures, performance, and challenges,” _CoRR_ , vol. abs/2509.23121, 2025. 

- [456] K. Kawaharazuka, J. Oh, J. Yamada, I. Posner, and Y. Zhu, “Visionlanguage-action models for robotics: A review towards real-world applications,” _IEEE Access_ , vol. 13, pp. 162 467–162 504, 2025. 

- [457] Z. Yu, B. Wang, P. Zeng, H. Zhang, J. Zhang, L. Gao, J. Song, N. Sebe, and H. T. Shen, “A survey on efficient vision-language-action models,” _CoRR_ , vol. abs/2510.24795, 2025. 

- [458] S. Poria, N. Majumder, C. Hung, A. A. Bagherzadeh, C. Li, K. Kwok, Z. Wang, C. Tan, J. Wu, and D. Hsu, “10 open challenges steering the future of vision-language-action models,” _CoRR_ , vol. abs/2511.05936, 2025. 

- [459] C. Xu, S. Zhang, Y. Liu, B. Sun, W. Chen, B. Xu, Q. Liu, J. Wang, S. Wang, S. Luo, J. Peters, A. V. Vasilakos, S. Zafeiriou, and J. Deng, “An anatomy of vision-language-action models: From modules to milestones and challenges,” _CoRR_ , vol. abs/2512.11362, 2025. 

- [460] H. Deng, Z. Wu, H. Liu, W. Guo, Y. Xue, Z. Shan, C. Zhang, B. Jia, Y. Ling, G. Lu, and Z. Wang, “A survey on reinforcement learning of vision-language-action models for robotic manipulation,” _TechRxiv_ , 2025, preprint. 

- [461] T. Hu, X. Liu, S. Wang, Y. Zhu, A. Liang, L. Kong, G. Zhao, Z. Gong, J. Cen, Z. Huang, X. Hao, L. Li, H. Song, X. Li, J. Ma, S. Shen, J. Zhu, D. Tao, Z. Liu, and J. Liang, “Vision-language-action models for autonomous driving: Past, present, and future,” _CoRR_ , vol. abs/2512.16760, 2025. 

- [462] X. Li, C. Mata, J. Park, K. Kahatapitiya, Y. S. Jang, J. Shang, K. Ranasinghe, R. D. Burgert, M. Cai, Y. J. Lee, and M. S. Ryoo, “Llara: Supercharging robot learning data for vision-language policy,” in _ICLR_ . OpenReview.net, 2025. 

- [463] K. Pertsch, K. Stachowicz, B. Ichter, D. Driess, S. Nair, Q. Vuong, O. Mees, C. Finn, and S. Levine, “FAST: efficient action tokenization for vision-language-action models,” _CoRR_ , vol. abs/2501.09747, 2025. 

- [464] P. Intelligence, K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, M. Y. Galliker, D. Ghosh, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, D. LeBlanc, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, A. Z. Ren, L. X. Shi, L. M. Smith, J. T. Springenberg, K. Stachowicz, J. Tanner, Q. Vuong, H. Walke, A. Walling, H. Wang, L. Yu, and U. Zhilinsky, “ _π_ 0.5: a vision-language-action model with open-world generalization,” _CoRR_ , vol. abs/2504.16054, 2025. 

- [465] Z. Xu, H. L. Chiang, Z. Fu, M. G. Jacob, T. Zhang, T. E. Lee, W. Yu, C. Schenck, D. Rendleman, D. Shah, F. Xia, J. Hsu, J. Hoech, P. Florence, S. Kirmani, S. Singh, V. Sindhwani, C. Parada, C. Finn, P. Xu, S. Levine, and J. Tan, “Mobility VLA: multimodal instruction navigation with long-context vlms and topological graphs,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 3866–3887. 

- [466] P. Ding, J. Ma, X. Tong, B. Zou, X. Luo, Y. Fan, T. Wang, H. Lu, P. Mo, J. Liu, Y. Wang, H. Zhou, W. Feng, J. Liu, S. Huang, and D. Wang, “Humanoid-vla: Towards universal humanoid control with visual integration,” _CoRR_ , vol. abs/2502.14795, 2025. 

- [467] P. Ding, H. Zhao, W. Zhang, W. Song, M. Zhang, S. Huang, N. Yang, and D. Wang, “QUAR-VLA: vision-language-action model for quadruped robots,” in _ECCV (5)_ , ser. Lecture Notes in Computer Science, vol. 15063. Springer, 2024, pp. 352–367. 

- [468] X. Tong, P. Ding, D. Wang, W. Zhang, C. Cui, M. Sun, Y. Fan, H. Zhao, H. Zhang, Y. Dang, S. Huang, and S. Lyu, “Quart-online: Latency-free large multimodal language model for quadruped robot learning,” _CoRR_ , vol. abs/2412.15576, 2024. 

- [469] H. Zhao, W. Song, D. Wang, X. Tong, P. Ding, X. Cheng, and Z. Ge, “More: Unlocking scalability in reinforcement learning for quadruped vision-language-action models,” _CoRR_ , vol. abs/2503.08007, 2025. 

- [470] Y. Zhong, X. Huang, R. Li, C. Zhang, Y. Liang, Y. Yang, and Y. Chen, “Dexgraspvla: A vision-language-action framework towards general dexterous grasping,” _CoRR_ , vol. abs/2502.20900, 2025. 

- [471] Y. Cui, Y. Zhang, L. Tao, Y. Li, X. Yi, and Z. Li, “End-to-end dexterous arm-hand VLA policies via shared autonomy: VR teleoperation augmented by autonomous hand VLA policy for efficient data collection,” _CoRR_ , vol. abs/2511.00139, 2025. 

- [472] NVIDIA, “Alpamayo-r1: Bridging reasoning and action prediction for generalizable autonomous driving in the long tail,” _CoRR_ , vol. abs/2511.00088, 2025. 

- [473] H. Arai, K. Miwa, K. Sasaki, K. Watanabe, Y. Yamaguchi, S. Aoki, and I. Yamamoto, “Covla: Comprehensive vision-language-action dataset for autonomous driving,” in _WACV_ . IEEE, 2025, pp. 1933–1943. 

- [474] Y. Li, S. Shang, W. Liu, B. Zhan, H. Wang, Y. Wang, Y. Chen, X. Wang, Y. An, C. Tang, L. Hou, L. Fan, and Z. Zhang, “Drivevla-w0: World models amplify data scaling law in autonomous driving,” _CoRR_ , vol. abs/2510.12796, 2025. 

- [475] J. Hwang, R. Xu, H. Lin, W. Hung, J. Ji, K. Choi, D. Huang, T. He, P. Covington, B. Sapp, Y. Zhou, J. Guo, D. Anguelov, and M. Tan, “EMMA: end-to-end multimodal model for autonomous driving,” _Trans. Mach. Learn. Res._ , vol. 2025, 2025. 

- [476] P. Chen, P. Bu, Y. Wang, X. Wang, Z. Wang, J. Guo, Y. Zhao, Q. Zhu, J. Song, S. Yang, J. Wang, and B. Zheng, “Combatvla: An efficient vision-language-action model for combat tasks in 3d action role-playing games,” _CoRR_ , vol. abs/2503.09527, 2025. 

- [477] M. Li, Z. Wang, K. He, X. Ma, and Y. Liang, “JARVIS-VLA: posttraining large-scale vision language models to play visual games with keyboards and mouse,” in _ACL (Findings)_ . Association for Computational Linguistics, 2025, pp. 17 878–17 899. 

- [478] N. G. Tsung-Wei Ke and and K. Fragkiadaki, “3d diffuser actor: Policy diffusion with 3d scene representations,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 1949–1974. 

- [479] X. Li, L. Heng, J. Liu, Y. Shen, C. Gu, Z. Liu, H. Chen, N. Han, R. Zhang, H. Tang, S. Zhang, and H. Dong, “3ds-vla,” _arXiv preprint_ , 2025. 

- [480] Y. C. Jiahui Zhang and, Y. Xu, Z. Huang, Y. Zhou, Y. Yuan, X. Cai, G. Huang, X. Quan, H. Xu, and L. Zhang, “4d-vla: Spatiotemporal vision-language-action pretraining with cross-scene, calibration,” _CoRR_ , vol. abs/2506.22242, 2025. 

- [481] M. A. Kohei Sendai and, T. Matsushima, Y. Matsuo, and Y. Iwasawa, “Leave no observation behind: Real-time correction for VLA action, chunks,” _CoRR_ , vol. abs/2509.23224, 2025. 

- [482] H. C. Siyuan Huang and, Y. Liu, Y. Zhu, H. Dong, A. Boularias, P. Gao, and H. Li, “A3VLM: actionable articulation-aware vision language model,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 1675–1690. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

29 

- [483] K. K. Minho Park and, J. Hyung, H. Jang, H. Jin, J. Yun, H. Lee, and J. Choo, “ACG: action coherence guidance for flow-based VLA models,” _CoRR_ , vol. abs/2510.22201, 2025. 

- [484] T. W. Wencheng Ye and, L. Zhu, F. Li, and G. Yang, “Actdistill: General action-guided self-derived distillation for efficient, vision-languageaction models,” _CoRR_ , vol. abs/2511.18082, 2025. 

- [485] H. G. Yuntao Dai and, T. Wang, Q. Cheng, Y. Zheng, Z. Qiu, L. Gong, W. Lou, and X. Zhou, “Actionflow: A pipelined action acceleration for vision language, models on edge,” _CoRR_ , vol. abs/2512.20276, 2025. 

- [486] Y. L. Weijie Shen and, Y. Wu, Z. Liang, S. Gu, D. Wang, T. Nian, L. Xu, Y. Qin, J. Pang, X. Guan, X. Yang, and Y. Mu, “Expertise need not monopolize: Action-specialized mixture of experts, for visionlanguage-action learning,” _CoRR_ , vol. abs/2510.14300, 2025. 

- [487] Y. C. Xiaohuan Pei and, S. Xu, Y. Wang, Y. Shi, and C. Xu, “Action-aware dynamic pruning for efficient vision-language-action, manipulation,” _CoRR_ , vol. abs/2509.22093, 2025. 

- [488] Z. W. Siyu Xu and, Y. Wang, C. Xia, T. Huang, and C. Xu, “Affordance field intervention: Enabling vlas to escape memory traps, in robotic manipulation,” _CoRR_ , vol. abs/2512.07472, 2025. 

- [489] Z. Y. Yizheng Zhang and, J. Lai, C. Lu, and L. Han, “Agentworld: An interactive simulation platform for scene construction, and mobile robotic manipulation,” _CoRR_ , vol. abs/2508.07770, 2025. 

- [490] H. Q. Irmak Guzey and, J. Urain, C. Wang, J. Yin, K. Bodduluri, M. Lambeta, L. Pinto, A. Rai, J. Malik, T. Wu, A. Sharma, and H. Bharadhwaj, “Dexterity from smart lenses: Multi-fingered robot manipulation with, in-the-wild human demonstrations,” _CoRR_ , vol. abs/2511.16661, 2025. 

- [491] B. L. Wenxin Zheng and, B. Xu, E. Feng, J. Gu, and H. Chen, “Leveraging os-level primitives for robotic action management,” _CoRR_ , vol. abs/2508.10259, 2025. 

- [492] Z. W. Yiyang Huang and, Z. Wan, Y. Tian, H. Xu, Y. Han, and Y. Gan, “ANNIE: be careful of your robots,” _CoRR_ , vol. abs/2509.03383, 2025. 

- [493] S. C. Yuhua Jiang and, Y. Ding, F. Gao, and B. Qi, “Asyncvla: Asynchronous flow matching for vision-language-action models,” _CoRR_ , vol. abs/2511.14148, 2025. 

- [494] C. W. Yang Zhang and, O. Lu, Y. Zhao, Y. Ge, Z. S. 0001, X. L. 0001, C. Z. 0012, C. Bai, and X. L. 0001, “Align-then-steer: Adapting the vision-language action models through unified latent guidance,” 2025. [Online]. Available: https://dblp.org/rec/journals/corr/abs-2509-02055 

- [495] J. T. Zhenlong Yuan and, J. Luo, R. Chen, C. Qian, L. Sun, X. Chu, Y. Cai, D. Zhang, and S. Li, “Autodrive-r<sup>2</sup> : Incentivizing reasoning and self-reflection, capacity for VLA model in autonomous driving,” _CoRR_ , vol. abs/2509.01944, 2025. 

- [496] Y. X. Hanshi Wang and, Z. Xu, J. Gao, Y. Liu, W. Hu, K. Wang, and Z. Zhang, “Autoprune: Each complexity deserves a pruning policy,” _CoRR_ , vol. abs/2509.23931, 2025. 

- [497] T. C. Zewei Zhou and, S. Z. Zhao, Y. Zhang, Z. Huang, B. Zhou, and J. Ma, “Autovla: A vision-language-action model for end-to-end autonomous, driving with adaptive reasoning and reinforcement finetuning,” _CoRR_ , vol. abs/2506.13757, 2025. 

- [498] J. L. Lei Xiao and, J. Gao, F. Ye, Y. Jin, J. Qian, J. Zhang, Y. Wu, and X. Yu, “Ava-vla: Improving vision-language-action models with active visual attention,” 2025. [Online]. Available: https://dblp.org/rec/journals/corr/abs-2511-18960 

- [499] L. L. Harris Song and, “Avi: Action from volumetric inference,” _CoRR_ , vol. abs/2510.21746, 2025. 

- [500] G. T. Xueyang Zhou and, G. Zhang, H. Wang, P. Zhou, and L. Sun, “Badvla: Towards backdoor attacks on vision-language-action models, via objective-decoupled optimization,” _CoRR_ , vol. abs/2505.16640, 2025. 

- [501] Z. Z. Kechun Xu and, A. Chen, S. Zhao, Q. Huang, Y. Yang, H. Lu, R. Xiong, M. Tomizuka, and Y. Wang, “Seeing to act, prompting to specify: A bayesian factorization of, vision language action policy,” _CoRR_ , vol. abs/2512.11218, 2025. 

- [502] Y. F. Hao Luo and, W. Zhang, S. Zheng, Y. Wang, H. Yuan, J. Liu, C. Xu, Q. Jin, and Z. Lu, “Being-h0: Vision-language-action pretraining from large-scale human, videos,” _CoRR_ , vol. abs/2507.15597, 2025. 

- [503] J. F. Yanbo Mao and, R. Zhang, H. Xie, and M. Yao, “Beyond success: Refining elegant robot manipulation from mixed-quality, data via justin-time intervention,” _CoRR_ , vol. abs/2511.22555, 2025. 

- [504] M. A. C. Koffivi Fid`ele Gbagbe and, A. Alabbas, O. Alyunes, A. Lykov, and D. Tsetserukou, “Bi-vla: Vision-language-action model-based system for bimanual robotic, dexterous manipulations,” in _SMC_ . IEEE, 2024, pp. 2864–2869. 

- [505] T. B. Masato Kobayashi and, “Bi-vla: Bilateral control-based imitation learning via vision-language, fusion for action generation,” _CoRR_ , vol. abs/2509.18865, 2025. 

- [506] Y. C. Peiyan Li and, H. Wu, X. Ma, X. Wu, Y. Huang, L. Wang, T. Kong, and T. Tan, “Bridgevla: Input-output alignment for efficient 3d manipulation learning, with vision-language models,” _CoRR_ , vol. abs/2506.07961, 2025. 

- [507] A. Z. R. Asher J. Hancock and and A. Majumdar, “Run-time observation interventions make vision-language-action models, more visually robust,” in _ICRA_ . IEEE, 2025, pp. 9499–9506. 

- [508] Y. Y. Xiuxiu Qi and, J. Cao, L. Bai, C. Fan, C. Cao, and H. Wang, “Continuous vision-language-action co-learning with semantic-physical, alignment for behavioral cloning,” _CoRR_ , vol. abs/2511.14396, 2025. 

- [509] Y. Z. Zhongyi Zhou and, J. Wen, C. Shen, and Y. Xu, “Chatvla-2: Vision-language-action model with open-world embodied reasoning, from pretrained knowledge,” _CoRR_ , vol. abs/2505.21906, 2025. 

- [510] R. Y. Zijian An and, Y. Feng, and L. Zhou, “CLAW: A visionlanguage-action framework for weight-aware robotic, grasping,” _CoRR_ , vol. abs/2509.14143, 2025. 

- [511] J. K. Gi-Cheon Kang and, K. Shim, J. K. Lee, and B. Zhang, “CLIP-RT: learning language-conditioned robotic policies from natural, language supervision,” _CoRR_ , vol. abs/2411.00508, 2024. 

- [512] Q. Y. Zeyuan Chen and, Y. Chen, T. Wu, J. Zhang, Z. Ding, J. Li, Y. Yang, and H. Dong, “Clutterdexgrasp: A sim-to-real system for general dexterous grasping, in cluttered scenes,” _CoRR_ , vol. abs/2506.14317, 2025. 

- [513] F. S. Dapeng Zhang and, R. Zhao, Y. Chen, P. Zhi, C. Li, R. Zhou, and Q. Zhou, “Coc-vla: Delving into adversarial domain transfer for explainable, autonomous driving via chain-of-causality visual-languageaction model,” _CoRR_ , vol. abs/2511.19914, 2025. 

- [514] R. Z. Wei Li and, R. Shao, J. He, and L. Nie, “Cogvla: Cognitionaligned vision-language-action model via instruction-driven, routing & sparsification,” _CoRR_ , vol. abs/2508.21046, 2025. 

- [515] X. C. Qihang Peng and, C. Yang, S. Shi, and H. Li, “Colavla: Leveraging cognitive latent reasoning for hierarchical parallel, trajectory planning in autonomous driving,” _CoRR_ , vol. abs/2512.22939, 2025. 

- [516] S. T. Yuhui Chen and, S. Liu, Y. Zhou, H. Li, and D. Zhao, “Conrft: A reinforced fine-tuning method for VLA models via consistency, policy,” _CoRR_ , vol. abs/2502.05450, 2025. 

- [517] Y. W. Puhao Li and, Z. Xi, W. Li, Y. Huang, Z. Zhang, Y. Chen, J. Wang, S. Zhu, T. Liu, and S. Huang, “Controlvla: Few-shot objectcentric adaptation for pre-trained vision-language-action, models,” _CoRR_ , vol. abs/2506.16211, 2025. 

- [518] W. K. Tian Nian and, Y. Mu, T. Chen, S. Zhu, and B. Hu, “Control your robot: A unified system for robot control and policy, deployment,” _CoRR_ , vol. abs/2509.23823, 2025. 

- [519] Y. C. Shiyu Fang and, H. Liang, C. Lv, P. Hang, and J. Sun, “Corevla: A dual-stage end-to-end autonomous driving framework for, long-tail scenarios via collect-and-refine,” _CoRR_ , vol. abs/2509.15968, 2025. 

- [520] T. Y. Zhaohui Wang and and H. Tang, “Cot4ad: A vision-languageaction model with explicit chain-of-thought, reasoning for autonomous driving,” _CoRR_ , vol. abs/2511.22532, 2025. 

- [521] W. D. Zhenghao ”Mark” Peng and, Y. You, Y. Chen, W. Luo, T. Tian, Y. Cao, A. Sharma, D. Xu, B. Ivanovic, B. Li, B. Zhou, Y. Wang, and M. Pavone, “Counterfactual VLA: self-reflective vision-languageaction model, with adaptive reasoning,” _CoRR_ , vol. abs/2512.24426, 2025. 

- [522] O. H. Daniel San Jos´e Pro and, R. R¨omer, M. D¨osch, M. Schuck, and A. P. Schoellig, “CRISP - compliant ROS2 controllers for learning-based manipulation, policies and teleoperation,” _CoRR_ , vol. abs/2509.06819, 2025. 

- [523] H. L. Yi-Lin Wei and, Y. Lin, P. Wang, Z. Liang, G. Liu, and W. Zheng, “Cyclemanip: Enabling cyclic task manipulation via effective historical, perception and understanding,” _CoRR_ , vol. abs/2512.01022, 2025. 

- [524] H. L. Changyeon Kim and, Y. Seo, K. Lee, and Y. Zhu, “DEAS: detached value learning with action sequence for scalable, offline RL,” _CoRR_ , vol. abs/2510.07730, 2025. 

- [525] L. H. Haibo Hu and, N. Guan, and C. J. Xue, “Deead: Dynamic early exit of vision-language action for efficient, autonomous driving,” _CoRR_ , vol. abs/2511.20720, 2025. 

- [526] Y. L. Cheng Yin and, W. Xu, S. Tam, X. Zeng, Z. Liu, and Z. Yin, “Deepthinkvla: Enhancing reasoning capability of vision-languageaction, models,” _CoRR_ , vol. abs/2511.15669, 2025. 

- [527] S. Wu, Y. Ji, Q. Li, Z. Zhang, Q. He, W. Xie, G. Zhang, B. Bayramli, Y. Ding, and H. Lu, “Dejavu: Towards experience feedback learning for embodied intelligence,” _arXiv preprint_ , 2025. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

30 

- [528] Y. L. Tianyuan Yuan and, C. Lu, Z. Chen, T. Jiang, and H. Zhao, “Depthvla: Enhancing vision-language-action models with depthaware, spatial reasoning,” _CoRR_ , vol. abs/2510.13375, 2025. 

- [529] E. Z. Bin Xie and, F. Jia, H. Shi, H. Fan, H. Zhang, H. Li, J. Sun, J. Bin, J. Huang, K. Liu, K. Liu, K. Gu, L. Sun, M. Zhang, P. Han, R. Hao, R. Zhang, S. Huang, S. Xie, T. Wang, T. Liu, W. Tang, W. Zhu, Y. Chen, Y. Liu, Y. Zhou, Y. Liu, Y. Zhao, Y. Ma, Y. Wei, Y. Chen, Z. Chen, Z. Li, Z. Wu, Z. Zhang, Z. Liu, Z. Yan, and Z. Zhang, “Dexbotic: Opensource vision-language-action toolbox,” _CoRR_ , vol. abs/2510.23511, 2025. 

- [530] Z. X. Cheng Chi and, S. Feng, E. Cousineau, Y. Du, B. Burchfiel, R. Tedrake, and S. Song, “Diffusion policy: Visuomotor policy learning via action diffusion,” _Int. J. Robotics Res._ , vol. 44, no. 10-11, pp. 1684– 1704, 2025. 

- [531] M. Z. Junjie Wen and, Y. Zhu, Z. Tang, J. Li, Z. Zhou, C. Li, X. Liu, Y. Peng, C. Shen, and F. Feng, “Diffusion-vla: Scaling robot foundation models via unified diffusion, and autoregression,” _CoRR_ , vol. abs/2412.03293, 2024. 

- [532] A. J. Yu Gao and, Y. Wang, J. Wang, H. Jiang, Z. Sun, Y. Heng, W. Shuo, H. Zhao, and H. Sun, “Diffvla++: Bridging cognitive reasoning and end-to-end driving through, metric-guided alignment,” _CoRR_ , vol. abs/2510.17148, 2025. 

- [533] R. Liang, Y. Zheng, K. Zheng, T. Tan, J. Li, L. Mao, Z. Wang, G. Chen, H. Ye, J. Liu, J. Wang, and X. Zhan, “Dichotomous diffusion policy optimization,” _arXiv preprint_ , 2025. 

- [534] Z. F. Rushuai Yang and, T. Zhang, K. Wang, C. Zhang, L. Zhao, X. Su, Y. Chen, and J. Bian, “Discover, learn, and reinforce: Scaling visionlanguage-action pretraining, with diverse rl-generated trajectories,” _CoRR_ , vol. abs/2511.19528, 2025. 

- [535] M. K. Nikita Kachaev and, D. Zelezetsky, A. K. Kovalev, and A. I. Panov, “Don’t blind your VLA: aligning visual representations for OOD, generalization,” _CoRR_ , vol. abs/2510.25616, 2025. 

- [536] J. K. ByungOk Han and and J. Jang, “A dual process VLA: efficient robotic manipulation leveraging VLM,” _CoRR_ , vol. abs/2410.15549, 2024. 

- [537] Z. Z. Guo Ye and, X. Zhao, S. Wu, H. Lu, S. Lu, and H. Liu, “Learning to feel the future: Dreamtacvla for contact-rich manipulation,” _CoRR_ , vol. abs/2512.23864, 2025. 

- [538] H. L. Wenyao Zhang and, Z. Qi, Y. Wang, X. Yu, J. Zhang, R. Dong, J. He, H. Wang, Z. Zhang, L. Yi, W. Zeng, and X. Jin, “Dreamvla: A vision-language-action model dreamed with comprehensive, world knowledge,” _CoRR_ , vol. abs/2507.04447, 2025. 

- [539] S. G. Jiacheng Ye and, J. Gao, J. Fan, S. Wu, W. Bi, H. Bai, L. Shang, and L. Kong, “Dream-vl & dream-vla: Open vision-language and vision-language-action, models with diffusion language model backbone,” _CoRR_ , vol. abs/2512.22615, 2025. 

- [540] Z. L. Zhen Fang and, J. Liu, H. Chen, Y. Zeng, S. Huang, Z. Chen, L. Chen, S. Zhang, and F. Zhao, “Dualvla: Building a generalizable embodied agent via partial decoupling, of reasoning and action,” _CoRR_ , vol. abs/2511.22134, 2025. 

- [541] H. Z. Teqiang Zou and, Y. Nong, Y. Li, K. Liu, H. Yang, X. Ling, X. Li, and L. Ma, “Asynchronous fast-slow vision-language-action policies for whole-body, robotic manipulation,” _CoRR_ , vol. abs/2512.20188, 2025. 

- [542] M. Z. Junjie Wen and, J. Liu, Z. Liu, Y. Yang, L. Zhang, S. Zhang, Y. Zhu, and Y. Xu, “dvla: Diffusion vision-language-action model with multimodal chain-of-thought,” _CoRR_ , vol. abs/2509.25681, 2025. 

- [543] Y. H. Travis Davies and, A. Gladstone, Y. Liu, X. Chen, H. Ji, H. Liu, and L. Hu, “Ebt-policy: Energy unlocks emergent physical reasoning capabilities,” _CoRR_ , vol. abs/2510.27545, 2025. 

- [544] W. C. Michal Zawalski and, K. Pertsch, O. Mees, C. Finn, and S. Levine, “Robotic control via embodied chain-of-thought reasoning,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 3157–3181. 

- [545] S. B. William Chen and, S. Mirchandani, O. Mees, D. Driess, K. Pertsch, and S. Levine, “Training strategies for efficient embodied reasoning,” _CoRR_ , vol. abs/2505.08243, 2025. 

- [546] Y. W. Yantai Yang and, Z. Wen, L. Zhongwei, C. Zou, Z. Zhang, C. Wen, and L. Zhang, “Efficientvla: Training-free acceleration and compression for vision-language-action, models,” _CoRR_ , vol. abs/2506.10100, 2025. 

- [547] M. Z. S. Binjie Zhang and, “Ego-centric predictive model conditioned on hand trajectories,” _CoRR_ , vol. abs/2508.19852, 2025. 

- [548] R. C. Zefu Lin and, C. Hanning, X. Wang, J. Xu, X. Jin, C. Wenbo, H. Zhou, L. Fan, W. Li, and Z. Zhang, “Embodiedcoder: Parameterized embodied mobile manipulation via modern, coding model,” _CoRR_ , vol. abs/2510.06207, 2025. 

- [549] T. H. Nhat Chung and, T. Nguyen, H. Le, F. Bumgarner, D. M. H. Nguyen, K. Vo, K. Yamazaki, C. Rainwater, T. Kieu, A. Nguyen, and N. Le, “Rethinking progression of memory state in robotic manipulation: An, object-centric perspective,” _CoRR_ , vol. abs/2511.11478, 2025. 

- [550] X. W. Zhehao Dong and, Z. Zhu, Y. Wang, Y. Wang, Y. Zhou, B. Wang, C. Ni, R. Ouyang, W. Qin, X. Chen, Y. Ye, and G. Huang, “EMMA: generalizing real-world robot manipulation via generative, visual transfer,” _CoRR_ , vol. abs/2509.22407, 2025. 

- [551] P. H. Qi Sun and, P. T. Deep, V. Toh, U. Tan, D. Ghosal, and S. Poria, “Emma-x: An embodied multimodal action model with grounded chain of, thought and look-ahead spatial reasoning,” in _ACL (1)_ . Association for Computational Linguistics, 2025, pp. 14 199–14 214. 

- [552] L. B. Chikit Ng and, G. Wang, Y. Wang, H. Gao, K. Yuan, C. Jin, T. Zeng, and H. Ren, “Endovla: Dual-phase vision-languageaction model for autonomous tracking, in endoscopy,” _CoRR_ , vol. abs/2505.15206, 2025. 

- [553] H. S. Delin Qu and, Q. Chen, Z. Chen, X. Gao, X. Ye, Q. Lv, M. Shi, G. Ren, C. Ruan, M. Yao, H. Yang, J. Bao, B. Zhao, and D. Wang, “Embodiedonevision: Interleaved vision-text-action pretraining for, general robot control,” _CoRR_ , vol. abs/2508.21112, 2025. 

- [554] S. W. Yi Liu and, D. Wei, X. Cai, L. Zhong, J. Yang, G. Ren, J. Zhang, M. Yao, C. Li, X. He, L. Chen, and J. Luo, “Unified embodied VLM reasoning with robotic action via autoregressive, discretized pretraining,” _CoRR_ , vol. abs/2512.24125, 2025. 

- [555] G. W. Chang Nie and, Z. Lie, and H. Wang, “ERMV: editing 4d robotic multi-view images to enhance embodied agents,” _CoRR_ , vol. abs/2507.17462, 2025. 

- [556] Y. P. Chengmeng Li and, “Embodiment transfer learning for visionlanguage-action models,” _CoRR_ , vol. abs/2511.01224, 2025. 

- [557] A. M. Samarth Chopra and, B. Carnovale, E. Sokolson, R. Kubendran, and S. Dickerson, “Everydayvla: A vision-language-action model for affordable robotic, manipulation,” _CoRR_ , vol. abs/2511.05397, 2025. 

- [558] Y. Z. Tao Lin and, Y. Du, J. Zhang, J. Liu, Y. Chen, E. Gu, Z. Liu, H. Cai, Y. Zou, L. Zou, Z. Zhou, G. Li, and B. Zhao, “Evo-1: Lightweight vision-language-action model with preserved semantic, alignment,” _CoRR_ , vol. abs/2511.04555, 2025. 

- [559] Y. A. Shahram Najam Syed and, A. Jakobsson, and J. Ichnowski, “Expres-vla: Specializing vision-language-action models through experience, replay and retrieval,” _CoRR_ , vol. abs/2511.06202, 2025. 

- [560] Y. H. Jiashu Yang and, Y. Xie, N. Guo, and W. Lian, “Look, zoom, understand: The robotic eyeball for embodied perception,” _CoRR_ , vol. abs/2511.15279, 2025. 

- [561] W. K. Qi Lv and, H. Li, J. Zeng, Z. Qiu, D. Qu, H. Song, Q. Chen, X. Deng, and J. Pang, “F1: A vision-language-action model bridging understanding and, generation to actions,” _CoRR_ , vol. abs/2509.06951, 2025. 

- [562] J. D. Zijun Lin and, H. Fang, D. Fox, R. Krishna, C. Tan, and B. Wen, “Failsafe: Reasoning and recovery from failures in vision-languageaction, models,” _CoRR_ , vol. abs/2510.01642, 2025. 

- [563] Q. Z. Jiajun Cao and, P. Jia, X. Zhao, B. Lan, X. Zhang, X. Wei, S. Chen, Z. Li, Y. Wang, L. Li, X. Liu, M. Lu, and S. Zhang, “Fastdrivevla: Efficient end-to-end driving via plug-and-play reconstructionbased, token pruning,” _CoRR_ , vol. abs/2507.23318, 2025. 

- [564] H. Chen, J. Liu, C. Gu, Z. Liu, R. Zhang, X. Li, and X. He, “Fast-inslow: A dual-system vla model unifying fast manipulation within slow reasoning,” _arXiv preprint_ , 2025. 

- [565] J. W. Ruijie Zheng and, S. Reed, J. Bjorck, Y. Fang, F. Hu, J. Jang, K. Kundalia, Z. Lin, L. Magne, A. Narayan, Y. L. Tan, G. Wang, Q. Wang, J. Xiang, Y. Xu, S. Ye, J. Kautz, F. Huang, Y. Zhu, and L. Fan, “FLARE: robot learning with implicit world modeling,” _CoRR_ , vol. abs/2505.15659, 2025. 

- [566] H. Z. Moritz Reuss and, M. R¨uhle, ¨O. E. Yagmurlu, F. Otto, and R. Lioutikov, “FLOWER: democratizing generalist robot policies with efficient vision-language-action, flow policies,” _CoRR_ , vol. abs/2509.04996, 2025. 

- [567] Z. Zhong, H. Yan, J. Li, X. Liu, X. Gong, T. Zhang, W. Song, J. Chen, X. Zheng, H. Wang, and H. Li, “Flowvla: Visual chain of thought-based motion reasoning for vision-language-action models,” _arXiv preprint_ , 2025. 

- [568] H. L. Jiawen Yu and, Q. Yu, J. Ren, C. Hao, H. Ding, G. Huang, G. Huang, Y. Song, P. Cai, C. Lu, and W. Zhang, “Forcevla: Enhancing VLA models with a force-aware moe for contact-rich, manipulation,” _CoRR_ , vol. abs/2505.22159, 2025. 

- [569] S. L. Yanjia Huang and, S. Liu, Q. Xu, M. Wu, X. Gao, and Z. Tu, “Forge-tree: Diffusion-forcing tree search for long-horizon robot manipulation,” _CoRR_ , vol. abs/2510.21744, 2025. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

31 

- [570] Z. D. Yifan Yang and, T. Xie, F. Cao, P. Shen, P. Song, P. Jin, G. Sun, S. Xu, Y. You, and J. Liu, “FPC-VLA: A vision-language-action framework with a supervisor, for failure prediction and correction,” _CoRR_ , vol. abs/2509.04018, 2025. 

- [571] J. L. Xin Wang and, Z. Weng, Y. Wang, Y. Gao, T. Pang, C. Du, Y. Teng, Y. Wang, Z. Wu, X. Ma, and Y. Jiang, “Freezevla: Actionfreezing attacks against vision-language-action, models,” _CoRR_ , vol. abs/2509.19870, 2025. 

- [572] Q. Z. Weiqi Li and, R. Zhai, L. Lin, and G. Wang, “VLA models are more generalizable than you think: Revisiting physical, and spatial modeling,” _CoRR_ , vol. abs/2512.02902, 2025. 

- [573] T. Y. Tao Jiang and, Y. Liu, C. Lu, J. Cui, X. Liu, S. Cheng, J. Gao, H. Xu, and H. Zhao, “Galaxea open-world dataset and G0 dual-system VLA model,” _CoRR_ , vol. abs/2509.00576, 2025. 

- [574] H. N. Arjun Vaithilingam Sudhakar and, M. Reymond, M. Liu, J. Rajendran, and S. Chandar, “A generalist hanabi agent,” in _ICLR_ . OpenReview.net, 2025. 

- [575] G. A. Team, “Gen-0: Embodied foundation models that scale with physical interaction,” _arXiv preprint_ , 2025. 

- [576] M. M. Ali Abouzeid and, Z. Sun, and D. Song, “Geoaware-vla: Implicit geometry aware vision-language-action model,” _CoRR_ , vol. abs/2509.14117, 2025. 

- [577] H. Z. Wenxuan Song and, P. Ding, C. Cui, S. Lyu, Y. Fan, and D. Wang, “Germ: A generalist robotic model with mixture-of-experts for quadruped, robot,” in _IROS_ . IEEE, 2024, pp. 11 879–11 886. 

- [578] P. D. Hongyin Zhang and, S. Lyu, Y. Peng, and D. Wang, “GEVRM: goal-expressive video generation model for robust visual, manipulation,” in _ICLR_ . OpenReview.net, 2025. 

- [579] L. G. Shunlei Li and, J. Wang, C. Che, X. Xiao, J. Cao, Y. Hu, and H. R. Karimi, “Information-theoretic graph fusion with visionlanguage-action model, for policy reasoning and dual robotic control,” _CoRR_ , vol. abs/2508.05342, 2025. 

- [580] M. C. Minghao Guo and, J. Tao, R. Xu, Y. Yan, X. Liang, I. Laptev, and X. Chang, “Glad: Geometric latent distillation for vision-languageaction models,” _CoRR_ , vol. abs/2512.09619, 2025. 

- [581] J. Jabbour, D.-K. Kim, M. Smith, J. Patrikar, R. Ghosal, Y. Wang, A. Agha, V. J. Reddi, and S. Omidshafiei, “Dont run with scissors,” _arXiv preprint_ , 2025. 

- [582] A. A. Gemini Robotics Team and, S. Abeyruwan, J. Ainslie, J. Alayrac, M. G. Arenas, A. Balakrishna, N. Batchelor, A. Bewley, J. T. Bingham, M. Bloesch, K. Bousmalis, P. Brakel, A. Brohan, T. Buschmann, A. Byravan, S. Cabi, K. Caluwaerts, F. Casarini, C. Chan, O. Chang, L. Chappellet-Volpini, J. E. Chen, X. Chen, H. L. Chiang, K. Choromanski, A. Collister, D. B. D’Ambrosio, S. Dasari, T. Davchev, M. K. Dave, C. Devin, N. D. Palo, T. Ding, C. Doersch, A. Dostmohamed, Y. Du, D. Dwibedi, S. T. Egambaram, M. Elabd, T. Erez, X. Fang, C. Fantacci, C. Fong, E. Frey, C. Fu, R. Gao, M. Giustina, K. Gopalakrishnan, L. Graesser, O. Groth, A. Gupta, R. Hafner, S. Hansen, L. Hasenclever, S. Haves, N. Heess, B. Hernaez, A. Hofer, J. Hsu, L. Huang, S. H. Huang, A. Iscen, M. G. Jacob, D. Jain, S. Jesmonth, A. Jindal, R. Julian, D. Kalashnikov, M. E. Karagozler, S. Karp, M. Kecman, J. C. Kew, D. Kim, F. Kim, J. Kim, T. Kipf, S. Kirmani, K. Konyushkova, L. Y. Ku, Y. Kuang, T. Lampe, A. Laurens, T. A. Le, I. Leal, A. X. Lee, T. E. Lee, G. Lever, J. Liang, L. Lin, F. Liu, S. Long, C. Lu, S. Maddineni, A. Majumdar, K. Maninis, A. Marmon, S. Martinez, A. H. Michaely, and N. Milonopoulos, “Gemini robotics 1.5: Pushing the frontier of generalist robots with, advanced embodied reasoning, thinking, and motion transfer,” _CoRR_ , vol. abs/2510.03342, 2025. 

- [583] K. Z. Zijian Zhang and, Z. Chen, J. Jang, Y. Li, C. Wang, M. Ding, D. Fox, and H. Yao, “GRAPE: generalizing robot policy via preference alignment,” _CoRR_ , vol. abs/2411.19309, 2024. 

- [584] M. C. Helong Huang and, K. Tan, X. Quan, G. Huang, and H. Zhang, “Graphcot-vla: A 3d spatial-aware reasoning vision-language-action, model for robotic manipulation with ambiguous instructions,” _CoRR_ , vol. abs/2508.07650, 2025. 

- [585] M. Y. Shengliang Deng and, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, H. Cui, Z. Zhang, and H. Wang, “Graspvla: a grasping foundation model pre-trained on billion-scale, synthetic action data,” _CoRR_ , vol. abs/2505.03233, 2025. 

- [586] Z. F. Ma¨elic Neau and, P. E. Santos, A. Bosser, and C. Buche, “Graspvla: Graph-based symbolic action representation for long-horizon, planning with VLA policies,” _CoRR_ , vol. abs/2511.04357, 2025. 

- [587] G. C. Ruoshi Wen and, Z. Cui, M. Du, Y. Gou, Z. Han, L. Huang, M. Lei, Y. Li, Z. Li, W. Liu, Y. Liu, X. Ma, H. Niu, Y. Ouyang, Z. Ren, H. Shi, W. Xu, H. Zhang, J. Zhang, X. Zhang, L. Zheng, W. Zhong, 

   - Y. Zhou, Z. Zhu, and H. Li, “Gr-dexter technical report,” _CoRR_ , vol. abs/2512.24210, 2025. 

- [588] X. M. Yunfei Li and, J. Xu, Y. Cui, Z. Cui, Z. Han, L. Huang, T. Kong, Y. Liu, H. Niu, W. Peng, J. Qiao, Z. Ren, H. Shi, Z. Su, J. Tian, Y. Xiao, S. Zhang, L. Zheng, H. Li, and Y. Wu, “GR-RL: going dexterous and precise for long-horizon robotic manipulation,” _CoRR_ , vol. abs/2512.01801, 2025. 

- [589] Y. D. Yi Li and, J. Zhang, J. Jang, M. Memmel, C. R. Garrett, F. Ramos, D. Fox, A. Li, A. Gupta, and A. Goyal, “HAMSTER: hierarchical action models for open-world robot manipulation,” in _ICLR_ . OpenReview.net, 2025. 

- [590] FIGURE, “Helix: A vision-language-action model for generalist humanoid control,” _arXiv preprint_ , 2025. 

- [591] P. D. Minghui Lin and, S. Wang, Z. Zhuang, Y. Liu, X. Tong, W. Song, S. Lyu, S. Huang, and D. Wang, “Hif-vla: Hindsight, insight and foresight through motion representation, for vision-language-action models,” _CoRR_ , vol. abs/2512.09928, 2025. 

- [592] B. L. Zhiying Du and, Y. Liang, Y. Shen, H. Cao, X. Zheng, Z. Feng, Z. Wu, J. Yang, and Y. Jiang, “Himoe-vla: Hierarchical mixture-ofexperts for generalist vision-language-action, policies,” _CoRR_ , vol. abs/2512.05693, 2025. 

- [593] R. Z. Guanxing Lu and, H. Lin, H. Zhang, and Y. Tang, “Human-inthe-loop online rejection sampling for robotic manipulation,” _CoRR_ , vol. abs/2510.26406, 2025. 

- [594] B. I. Lucy Xiaoyang Shi and, M. R. Equi, L. Ke, K. Pertsch, Q. Vuong, J. Tanner, A. Walling, H. Wang, N. Fusai, A. Li-Bell, D. Driess, L. Groom, S. Levine, and C. Finn, “Hi robot: Open-ended instruction following with hierarchical vision-language-action, models,” in _ICML_ . OpenReview.net, 2025. 

- [595] Y. G. Jianke Zhang and, X. Chen, Y. Wang, Y. Hu, C. Shi, and J. Chen, “Hirt: Enhancing robotic control with hierarchical robot transformers,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 933–946. 

- [596] Y. Z. Xinyu Xu and, Y. Li, L. Han, and C. Lu, “Humanvla: Towards vision-language directed object rearrangement by, physical humanoid,” in _NeurIPS_ , 2024. 

- [597] C. X. Yuan Zhang and, W. Xu, C. Ji, J. Wu, and J. Pan, “iflybot-vla technical report,” _CoRR_ , vol. abs/2511.01914, 2025. 

- [598] W. G. Dekun Lu and and K. Jia, “Imaginationpolicy: Towards generalizable, precise and reliable end-to-end, policy for robotic manipulation,” _CoRR_ , vol. abs/2509.20841, 2025. 

- [599] H. G. Haohan Chi and, Z. Liu, J. Liu, C. Liu, J. Li, K. Yang, Y. Yu, Z. Wang, W. Li, L. Wang, X. Hu, H. Sun, H. Zhao, and H. Zhao, “Impromptu VLA: open weights and open data for driving visionlanguage-action, models,” _CoRR_ , vol. abs/2505.23757, 2025. 

- [600] Z. S. Ulas Berk Karli and and T. Fitzgerald, “INSIGHT: inference-time sequence introspection for generating help, triggers in vision-languageaction models,” _CoRR_ , vol. abs/2510.01389, 2025. 

- [601] H. L. Shuai Yang and, Y. Chen, B. Wang, Y. Tian, T. Wang, H. Wang, F. Zhao, Y. Liao, and J. Pang, “Instructvla: Vision-language-action instruction tuning from understanding, to manipulation,” _CoRR_ , vol. abs/2507.17520, 2025. 

- [602] K. G. Yandu Chen and, Y. Wen, Y. Zhao, T. Wang, and L. Nie, “Intentionvla: Generalizable and efficient embodied intention reasoning, for human-robot interaction,” _CoRR_ , vol. abs/2510.07778, 2025. 

- [603] B. M. Nan Sun and, Y. Li, C. Wang, D. Guo, and H. Liu, “Transforming monolithic foundation models into embodied multi-agent, architectures for human-robot collaboration,” _CoRR_ , vol. abs/2512.00797, 2025. 

- [604] Y. C. Xinyi Chen and, Y. Fu, N. Gao, J. Jia, W. Jin, H. Li, Y. Mu, J. Pang, Y. Qiao, Y. Tian, B. Wang, B. Wang, F. Wang, H. Wang, T. Wang, Z. Wang, X. Wei, C. Wu, S. Yang, J. Ye, J. Yu, J. Zeng, J. Zhang, J. Zhang, S. Zhang, F. Zheng, B. Zhou, and Y. Zhu, “Internvla-m1: A spatially guided vision-language-action framework, for generalist robot policy,” _CoRR_ , vol. abs/2510.13778, 2025. 

- [605] J. Z. Yanjiang Guo and, X. Chen, X. Ji, Y. Wang, Y. Hu, and J. Chen, “Improving vision-language-action model with online reinforcement learning,” in _ICRA_ . IEEE, 2025, pp. 15 665–15 672. 

- [606] Y. G. Anqing Jiang and, Y. Wang, Z. Sun, S. Wang, Y. Heng, H. Sun, S. Tang, L. Zhu, J. Chai, J. Wang, Z. Gu, H. Jiang, and L. Sun, “IRL-VLA: training an vision-language-action policy via reward world, model,” _CoRR_ , vol. abs/2508.06571, 2025. 

- [607] W. Xu, L. Zhuang, and L. Shan, “Kv-efficient vla: A method to speed up vision language models with rnn-gated chunked kv cache,” _arXiv preprint_ , 2025. 

- [608] X. G. Zuolei Li and, X. Wang, and J. Fu, “Latbot: Distilling universal latent actions for vision-language-action, models,” _CoRR_ , vol. abs/2511.23034, 2025. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

32 

- [609] Y. N. Bahey Tharwat and, A. Abouzeid, and I. Reid, “Latent action pretraining through world modeling,” _CoRR_ , vol. abs/2509.18428, 2025. 

- [610] K. C. Shuhan Tan and, Y. Chen, R. Tian, Y. You, Y. Wang, W. Luo, Y. Cao, P. Kr¨ahenb¨uhl, M. Pavone, and B. Ivanovic, “Latent chain-of-thought world modeling for end-to-end driving,” _CoRR_ , vol. abs/2512.10226, 2025. 

- [611] W. C. Ameesh Shah and, A. Godbole, F. Mora, S. A. Seshia, and S. Levine, “Learning affordances at inference-time for vision-languageaction, models,” _CoRR_ , vol. abs/2510.19752, 2025. 

- [612] K. D. G. Justin Williams and, R. George, and M. Sarkar, “Lite VLA: efficient vision-language-action control on cpu-bound, edge robots,” _CoRR_ , vol. abs/2511.05642, 2025. 

- [613] J. S. Yi Yang and, S. Kou, Y. Wang, and Z. Deng, “Lohovla: A unified vision-language-action model for long-horizon, embodied tasks,” _CoRR_ , vol. abs/2506.00411, 2025. 

- [614] X. G. Xiaofan Wang and, J. Fu, Z. Li, D. Fortier, G. Mullins, A. Kolobov, and B. Guo, “Lola: Long horizon latent action learning for general robot manipulation,” _CoRR_ , vol. abs/2512.20166, 2025. 

- [615] P. D. Yiguo Fan and, S. Bai, X. Tong, Y. Zhu, H. Lu, F. Dai, W. Zhao, Y. Liu, S. Huang, Z. Fan, B. Chen, and D. Wang, “Long-vla: Unleashing long-horizon capability of vision language action, model for robot manipulation,” _CoRR_ , vol. abs/2508.19958, 2025. 

- [616] T. Z. Boyuan Chen and, H. Geng, K. Song, C. Zhang, P. Li, W. T. Freeman, J. Malik, P. Abbeel, R. Tedrake, V. Sitzmann, and Y. Du, “Large video planner enables generalizable robot control,” _CoRR_ , vol. abs/2512.15840, 2025. 

- [617] K. G. Yi Yang and, Y. Wen, H. Li, Y. Zhao, T. Wang, and X. Liu, “Maniagent: An agentic framework for general robotic manipulation,” _CoRR_ , vol. abs/2510.11660, 2025. 

- [618] X. L. Yi Yang and, Y. Chen, J. Song, Y. Wang, Z. Xiao, J. Su, Y. Qiaoben, P. Liu, and Z. Deng, “Mantis: A versatile visionlanguage-action model with disentangled, visual foresight,” _CoRR_ , vol. abs/2511.16175, 2025. 

- [619] J. L. Chenyang Gu and, H. Chen, R. Huang, Q. Wuwu, Z. Liu, X. Li, Y. Li, R. Zhang, P. Jia, P. Heng, and S. Zhang, “Manualvla: A unified VLA model for chain-of-thought manual generation, and robotic manipulation,” _CoRR_ , vol. abs/2512.02013, 2025. 

- [620] W. G. Runhao Li and, Z. Wu, C. Wang, H. Deng, Z. Weng, Y. Tan, and Z. Wang, “MAP-VLA: memory-augmented prompting for vision-language-action model, in robotic manipulation,” _CoRR_ , vol. abs/2511.09516, 2025. 

- [621] J. Z. Zhihao Zhan and, L. Zhang, Q. Lv, H. Liu, J. Zhang, W. Li, Z. Chen, T. Chen, K. Wang, L. Lin, and G. Wang, “ _E_ 0: Enhancing generalization and fine-grained, control in VLA models via continuized discrete diffusion,” _CoRR_ , vol. abs/2511.21542, 2025. 

- [622] ¨O. E. Y. Moritz Reuss and, F. Wenzel, and R. Lioutikov, “Multimodal diffusion transformer: Learning versatile behavior from, multimodal goals,” in _Robotics: Science and Systems_ , 2024. 

- [623] J. P. Ajay Sridhar and, S. Sharma, and C. Finn, “Memer: Scaling up memory for robot control via experience retrieval,” _CoRR_ , vol. abs/2510.20328, 2025. 

- [624] B. X. Hao Shi and, Y. Liu, L. Sun, F. Liu, T. Wang, E. Zhou, H. Fan, X. Zhang, and G. Huang, “Memoryvla: Perceptual-cognitive memory in vision-language-action models, for robotic manipulation,” _CoRR_ , vol. abs/2508.19236, 2025. 

- [625] Z. Y. Chen Li and, H. Zhang, F. Chen, C. Zhu, A. Bolimera, and M. Savvides, “Metavla: Unified meta co-training for efficient embodied adaption,” _CoRR_ , vol. abs/2510.05580, 2025. 

- [626] D. K. Suhyeok Jang and, C. Kim, Y. Kim, and J. Shin, “Verifierfree test-time sampling for vision language action models,” _CoRR_ , vol. abs/2510.05681, 2025. 

- [627] I. Z. Haoyun Li and, R. Ouyang, X. Wang, Z. Zhu, Z. Yang, Z. Zhang, B. Wang, C. Ni, W. Qin, X. Chen, Y. Ye, G. Huang, Z. Song, and X. Wang, “Mimicdreamer: Aligning human and robot demonstrations for scalable, VLA training,” _CoRR_ , vol. abs/2509.22199, 2025. 

- [628] D. Z. Haoyu Fu and, Z. Zhao, J. Cui, H. Xie, B. Wang, G. Chen, D. Liang, and X. Bai, “Minddrive: A vision-language-action model for autonomous driving, via online reinforcement learning,” _CoRR_ , vol. abs/2512.13636, 2025. 

- [629] S. X. Peijun Tang and, B. Sun, B. Huang, K. Luo, H. Yang, W. Jin, and J. Wang, “Mind to hand: Purposeful robotic control via embodied reasoning,” _CoRR_ , vol. abs/2512.08580, 2025. 

- [630] X. W. Zhenhan Yin and, J. Jiang, K. Deng, P. Chen, S. Li, C. Liu, X. Xu, J. Song, L. Gao, and H. T. Shen, “Mivla: Towards generalizable vision-language-action model with human-robot, mutual imitation pretraining,” _CoRR_ , vol. abs/2512.15411, 2025. 

- [631] J. L. Zhuoyang Liu and, J. Xu, N. Han, C. Gu, H. Chen, K. Zhou, R. Zhang, K. Hsieh, K. Wu, Z. Che, J. Tang, and S. Zhang, “MLA: A multisensory language-action model for multimodal understanding, and forecasting in robotic manipulation,” _CoRR_ , vol. abs/2509.26642, 2025. 

- [632] X. C. Haotian Liang and, B. Wang, M. Chen, Y. Liu, Y. Zhang, Z. Chen, T. Yang, Y. Chen, J. Pang, D. Liu, X. Yang, Y. Mu, W. Shao, and P. Luo, “MM-ACT: learn from multimodal parallel generation to act,” _CoRR_ , vol. abs/2512.00975, 2025. 

- [633] G. W. Dong Jing and, J. Liu, W. Tang, Z. Sun, Y. Yao, Z. Wei, Y. Liu, Z. Lu, and M. Ding, “Mixture of horizons in action chunking,” _CoRR_ , vol. abs/2511.19433, 2025. 

- [634] N. S. Dmytro Kuzmenko and, “Moira: Modular instruction routing architecture for multi-task robotics,” _CoRR_ , vol. abs/2507.01843, 2025. 

- [635] M. X. Chengshu Li and, A. Bahety, H. Yin, Y. Jiang, H. Huang, J. Wong, S. Garlanka, C. Gokmen, R. Zhang, W. Liu, J. Wu, R. Mart´ınMart´ın, and L. Fei-Fei, “Momagen: Generating demonstrations under soft and hard constraints, for multi-step bimanual mobile manipulation,” _CoRR_ , vol. abs/2510.18316, 2025. 

- [636] Y. Z. Zhenyu Wu and, X. Xu, Z. Wang, and H. Yan, “Momanipvla: Transferring vision-language-action models for general, mobile manipulation,” in _CVPR_ . Computer Vision Foundation / IEEE, 2025, pp. 1714–1723. 

- [637] Y. W. Shuo Wang and, W. Li, Y. Wang, M. Chen, K. Wang, Z. Su, X. Cai, Y. Jin, D. Li, and Z. Fan, “Monodream: Monocular vision-language navigation with panoramic dreaming,” _CoRR_ , vol. abs/2508.02549, 2025. 

- [638] T. X. Austin Stone and, Y. Lu, K. Gopalakrishnan, K. Lee, Q. Vuong, P. Wohlhart, S. Kirmani, B. Zitkovich, F. Xia, C. Finn, and K. Hausman, “Open-world object manipulation using pre-trained vision-language models,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 229. PMLR, 2023, pp. 3397–3417. 

- [639] W. S. Han Zhao and, D. Wang, X. Tong, P. Ding, X. Cheng, and Z. Ge, “More: Unlocking scalability in reinforcement learning for quadruped, vision-language-action models,” in _ICRA_ . IEEE, 2025, pp. 11 212– 11 218. 

- [640] R. Z. Chengbo Yuan and, M. Liu, Y. Hu, S. Wang, L. Yi, C. Wen, S. Zhang, and Y. Gao, “Motiontrans: Human VR data enable motion-level learning for robotic, manipulation policies,” _CoRR_ , vol. abs/2509.17759, 2025. 

- [641] A. M. Zhenyu Wu and, X. Xu, H. Yin, Y. Liang, Z. Wang, J. Lu, and H. Yan, “Moto: A zero-shot plug-in interaction-aware navigation for general, mobile manipulation,” _CoRR_ , vol. abs/2509.01658, 2025. 

- [642] J. Z. Alexander Spiridonov and, N. Nikolov, L. V. Gool, and D. P. Paudel, “Generalist robot manipulation beyond action labeled data,” _CoRR_ , vol. abs/2509.19958, 2025. 

- [643] H. T. Hongzhe Bi and, S. Xie, Z. Wang, S. Huang, H. Liu, R. Zhao, Y. Feng, C. Xiang, Y. Rong, H. Zhao, H. Liu, Z. Su, L. Ma, H. Su, and J. Zhu, “Motus: A unified latent action world model,” _CoRR_ , vol. abs/2512.13030, 2025. 

- [644] X. S. Pu Zhao and, Z. Kong, Y. Shen, S. Chang, A. Akbari, T. Rupprecht, L. Lu, E. Nan, C. Yang, Y. He, W. Shi, X. Xu, Y. Huang, W. Jiang, W. Wang, Y. Chen, Y. He, and Y. Wang, “Open-source multimodal moxin models with moxin-vlm and moxin-vla,” _CoRR_ , vol. abs/2512.22208, 2025. 

- [645] F. J. Peilong Han and, M. Zhang, Y. Qiu, H. Tang, Y. Zheng, T. Wang, and J. Hao, “MUVLA: learning to explore object navigation via map understanding,” _CoRR_ , vol. abs/2509.25966, 2025. 

- [646] Y. J. An-Chieh Cheng and, Z. Yang, X. Zou, J. Kautz, E. Biyik, H. Yin, S. Liu, and X. Wang, “Navila: Legged robot vision-language-action model for navigation,” _CoRR_ , vol. abs/2412.04453, 2024. 

- [647] M. P. Sajjad Pakdamansavoji and, A. Sigal, Z. Li, R. H. Yang, and A. Rasouli, “Improving robotic manipulation robustness via NICE scene surgery,” _CoRR_ , vol. abs/2511.22777, 2025. 

- [648] L. Magne, A. Awadalla, G. Wang, Y. Xu, J. Belofsky, F. Hu, J. Kim, L. Schmidt, G. Gkioxari, J. Kautz, Y. Yue, Y. Choi, Y. Zhu, and L. J. Fan, “Nitrogen: An open foundation model for generalist gaming agents,” _arXiv preprint_ , 2026. 

- [649] D. D. Rokas Bendikas and, M. Peschl, S. Haresh, and P. Mazzaglia, “Focusing on what matters: Object-agent-centric tokenization for vision, language action models,” _CoRR_ , vol. abs/2509.23655, 2025. 

- [650] T. H. Khoa Vo and, Y. Ikebe, T. Pham, N. Chung, M. N. Vu, D. N. H. Minh, A. Nguyen, A. Gunderman, C. Rainwater, and N. Le, “Clutterresistant vision-language-action models through object-centric, and geometry grounding,” _CoRR_ , vol. abs/2512.22519, 2025. 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

33 

- [651] S. Y. Julong Wei and, P. Li, Q. Hu, Z. Gan, and W. Ding, “Occllama: An occupancy-language-action generative world model for, autonomous driving,” _CoRR_ , vol. abs/2409.03272, 2024. 

- [652] L. K. Ruixun Liu and, D. Li, and H. Zhao, “Occvla: Vision-languageaction model with implicit 3d occupancy supervision,” _CoRR_ , vol. abs/2509.05578, 2025. 

- [653] H. D. Tianyi Zhang and, H. Hao, Y. Qiao, J. Dai, and Z. Hou, “Grounding actions in camera space: Observation-centric vision-languageaction, policy,” _CoRR_ , vol. abs/2508.13103, 2025. 

- [654] S. C. Zihao Wang and, Z. Mu, H. Lin, C. Zhang, X. Liu, Q. Li, A. Liu, X. S. Ma, and Y. Liang, “Omnijarvis: Unified vision-languageaction tokenization enables open-world, instruction following agents,” in _NeurIPS_ , 2024. 

- [655] Q. N. Pei Liu and, X. Lu, H. Liu, W. Ma, D. She, P. Jia, X. Lang, and J. Ma, “Omnireason: A temporal-guided vision-language-action framework for, autonomous driving,” _CoRR_ , vol. abs/2509.00789, 2025. 

- [656] C. C. Huaihai Lyu and, S. Xie, P. Wang, X. Chen, S. Zhang, and C. Xu, “Omnisat: Compact action token, faster auto regression,” _CoRR_ , vol. abs/2510.09667, 2025. 

- [657] C. G. Noriaki Hirose and, D. Shah, and S. Levine, “Omnivla: An omnimodal vision-language-action model for robot navigation,” _CoRR_ , vol. abs/2509.19480, 2025. 

- [658] R. N. Fanqi Lin and, Y. Hu, J. You, J. Zhao, and Y. Gao, “Onetwovla: A unified vision-language-action model with adaptive, reasoning,” _CoRR_ , vol. abs/2505.11917, 2025. 

- [659] M. L. Zihao Wang and, K. He, X. Wang, Z. Mu, A. Liu, and Y. Liang, “Openha: A series of open-source hierarchical agentic models in minecraft,” _CoRR_ , vol. abs/2509.13347, 2025. 

- [660] K. P. Moo Jin Kim and, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong, T. Kollar, B. Burchfiel, R. Tedrake, D. Sadigh, S. Levine, P. Liang, and C. Finn, “Openvla: An open-source vision-language-action model,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 2679–2713. 

- [661] F. L. Huang Huang and, L. Fu, T. Wu, M. Mukadam, J. Malik, K. Goldberg, and P. Abbeel, “OTTER: A vision-language-action model with text-aware visual feature, extraction,” in _ICML_ . OpenReview.net, 2025. 

- [662] S. L. Xiaopeng Lin and, B. Yu, R. Yang, C. Wu, Y. Miao, Y. Jin, Y. Shi, C. Huang, B. Cheng, and K. Chen, “Physbrain: Human egocentric data as a bridge from vision language, models to physical intelligence,” _CoRR_ , vol. abs/2512.16793, 2025. 

- [663] J. L. Zhihao Wang and, J. Zheng, W. Zhang, D. Liu, Y. Zheng, H. Niu, J. Yu, and X. Zhan, “Physiagent: An embodied agent framework in physical world,” _CoRR_ , vol. abs/2509.24524, 2025. 

- [664] K. Chen, Z. Liu, T. Zhang, Z. Guo, S. Xu, H. Lin, H. Zang, Q. Zhang, Z. Yu, G. Fan, T. Huang, Y. Wang, and C. Yu, “ _π_ rl: Online RL fine-tuning for flow-based vision-language-action models,” _CoRR_ , vol. abs/2510.25889, 2025. 

- [665] G. S. Wenqi Liang and, Y. He, J. Dong, S. Dai, I. Laptev, S. H. Khan, and Y. Cong, “Pixelvla: Advancing pixel-level understanding in visionlanguage-action, model,” _CoRR_ , vol. abs/2511.01571, 2025. 

- [666] E. L. H. Yi Zhang and, K. Chao, N. Petrovic, Y. Song, C. Wu, and A. Knoll, “A unified perception-language-action framework for adaptive autonomous, driving,” _CoRR_ , vol. abs/2507.23540, 2025. 

- [667] J. Z. Hang Yu and, Y. Liu, K. Li, C. Ma, D. Zhang, Y. Hu, G. Chen, J. Xie, J. Guo, J. Zhao, and Y. Gao, “Point what you mean: Visually grounded instruction policy,” _CoRR_ , vol. abs/2512.18933, 2025. 

- [668] X. W. Ziwen Li and, H. Zhang, R. Chen, R. Lin, X. He, H. Huang, Y. Guo, F. Karray, T. Liu, and M. Gong, “Posa-vla: Enhancing action generation via pose-conditioned anchor, attention,” _CoRR_ , vol. abs/2512.03724, 2025. 

- [669] Z. H. Jiahui Zhang and, C. Gu, Z. Ma, and L. Zhang, “Reinforcing action policies by prophesying,” _CoRR_ , vol. abs/2511.20633, 2025. 

- [670] H. K. Seongmin Park and, W. Jeon, J. Yang, B. Jeon, Y. Oh, and J. Choi, “Quantization-aware imitation-learning for resource-efficient robotic, control,” _CoRR_ , vol. abs/2412.01034, 2024. 

- [671] Y. C. Yixuan Li and, M. Zhou, and H. Li, “Qdepth-vla: Quantized depth prediction as auxiliary supervision for, vision-language-action models,” _CoRR_ , vol. abs/2510.14836, 2025. 

- [672] Q. V. Yevgen Chebotar and, K. Hausman, F. Xia, Y. Lu, A. Irpan, A. Kumar, T. Yu, A. Herzog, K. Pertsch, K. Gopalakrishnan, J. Ibarz, O. Nachum, S. A. Sontakke, G. Salazar, H. T. Tran, J. Peralta, C. Tan, D. Manjunath, J. Singh, B. Zitkovich, T. Jackson, K. Rao, C. Finn, and S. Levine, “Q-transformer: Scalable offline reinforcement learning 

   - via autoregressive, q-functions,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 229. PMLR, 2023, pp. 3909–3928. 

- [673] P. D. Xinyang Tong and, Y. Fan, D. Wang, W. Zhang, C. Cui, M. Sun, H. Zhao, H. Zhang, Y. Dang, S. Huang, and S. Lyu, “Quart-online: Latency-free multimodal large language model for quadruped, robot learning,” in _ICRA_ . IEEE, 2025, pp. 9533–9539. 

- [674] L. F. Justin Yu and, H. Huang, K. El-Refai, R. A. Ambrus, R. Cheng, M. Z. Irshad, and K. Goldberg, “Real2render2real: Scaling robot data without dynamics simulation or, robot hardware,” _CoRR_ , vol. abs/2505.09601, 2025. 

- [675] L. W. Songming Liu and, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “RDT-1B: a diffusion foundation model for bimanual manipulation,” in _ICLR_ . OpenReview.net, 2025. 

- [676] Z. Y. Dapeng Zhang and, Z. Chen, C. Liao, Y. Chen, F. Shen, Q. Zhou, and T. Chua, “Reasoning-vla: A fast and general vision-language-action reasoning, model for autonomous driving,” _CoRR_ , vol. abs/2511.19912, 2025. 

- [677] Y. Z. Pengxiang Li and, Y. Wang, H. Wang, H. Zhao, J. Liu, X. Zhan, K. Zhan, and X. Lang, “Discrete diffusion for reflective vision-language-action models in, autonomous driving,” _CoRR_ , vol. abs/2509.20109, 2025. 

- [678] S. D. Kaustubh Sridhar and, D. Jayaraman, and I. Lee, “REGENT: A retrieval-augmented generalist agent that can act in-context, in new environments,” in _ICLR_ . OpenReview.net, 2025. 

- [679] C. W. Wenlong Huang and, Y. Li, R. Zhang, and L. Fei-Fei, “Rekep: Spatio-temporal reasoning of relational keypoint constraints, for robotic manipulation,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 4573–4602. 

- [680] Z. Z. Yajat Yadav and, A. Wagenmaker, K. Pertsch, and S. Levine, “Robust finetuning of vision-language-action robot policies via parameter, merging,” _CoRR_ , vol. abs/2512.08333, 2025. 

- [681] T. C. Jiyeon Koo and, H. Kang, E. Pyo, T. G. Oh, T. Kim, and A. J. Choi, “Retovla: Reusing register tokens for spatial reasoning in visionlanguage-action, models,” _CoRR_ , vol. abs/2509.21243, 2025. 

- [682] J. Z. Sombit Dey and, N. Nikolov, L. V. Gool, and D. P. Paudel, “Revla: Reverting visual domain limitation of robotic foundation models,” in _ICRA_ . IEEE, 2025, pp. 8679–8686. 

- [683] S. D. Kaustubh Sridhar and, D. Jayaraman, and I. Lee, “RICL: adding in-context adaptability to pre-trained vision-language-action, models,” _CoRR_ , vol. abs/2508.02062, 2025. 

- [684] G. V. Konstantinos Bousmalis and, D. Rao, C. M. Devin, A. X. Lee, M. B. Villalonga, T. Davchev, Y. Zhou, A. Gupta, A. Raju, A. Laurens, C. Fantacci, V. Dalibard, M. Zambelli, M. F. Martins, R. Pevceviciute, M. Blokzijl, M. Denil, N. Batchelor, T. Lampe, E. Parisotto, K. Zolna, S. E. Reed, S. G. Colmenarejo, J. Scholz, A. Abdolmaleki, O. Groth, J. Regli, O. Sushkov, T. Roth¨orl, J. E. Chen, Y. Aytar, D. Barker, J. Ortiz, M. A. Riedmiller, J. T. Springenberg, R. Hadsell, F. Nori, and N. Heess, “Robocat: A self-improving generalist agent for robotic manipulation,” _Trans. Mach. Learn. Res._ , vol. 2024, 2024. 

- [685] C. Y. Zongzheng Zhang and, H. Xu, M. Liao, X. Qi, H. Gao, Z. Wang, and H. Zhao, “Robochemist: Long-horizon and safety-compliant robotic chemical experimentation,” _CoRR_ , vol. abs/2509.08820, 2025. 

- [686] H. L. Qingwen Bu and, L. Chen, J. Cai, J. Zeng, H. Cui, M. Yao, and Y. Qiao, “Towards synergistic, generalized, and efficient dual-system for robotic, manipulation,” _CoRR_ , vol. abs/2410.08001, 2024. 

- [687] M. L. Xinghang Li and, H. Zhang, C. Yu, J. Xu, H. Wu, C. Cheang, Y. Jing, W. Zhang, H. Liu, H. Li, and T. Kong, “Vision-language foundation models as effective robot imitators,” in _ICLR_ . OpenReview.net, 2024. 

- [688] W. Z. Weixin Mao and, Z. Jiang, D. Fang, Z. Zhang, Z. Lan, F. Jia, T. Wang, H. Fan, and O. Yoshie, “Robomatrix: A skill-centric hierarchical framework for scalable, robot task planning and execution in open-world,” _CoRR_ , vol. abs/2412.00171, 2024. 

- [689] H. X. Weifan Guan and, C. Zhang, A. Li, Q. Hu, and J. Cheng, “Roboneuron: A modular framework linking foundation models and ROS, for embodied AI,” _CoRR_ , vol. abs/2512.10394, 2025. 

- [690] J. W. Shunlei Li and, R. Dai, W. Ma, W. Y. Ng, Y. Hu, and Z. Li, “Robonurse-vla: Robotic scrub nurse system based on vision-languageaction, model,” in _IROS_ . IEEE, 2025, pp. 3986–3993. 

- [691] J. F. Siyin Wang and, F. Liu, X. He, H. Wu, J. Shi, K. Huang, Z. Fei, J. Gong, Z. Wu, Y. Jiang, S. Ng, T. Chua, and X. Qiu, “Roboomni: Proactive robot manipulation in omni-modal context,” _CoRR_ , vol. abs/2510.23763, 2025. 

- [692] C. C. Huajie Tan and, X. Chen, Y. Ji, Z. Zhao, X. Hao, Y. Lyu, M. Cao, J. Zhao, H. Lyu, E. Zhou, N. Chen, Y. Fu, C. Peng, W. Guo, D. Liang, Z. Chen, M. Lyu, C. He, Y. Ao, Y. Lin, P. Wang, Z. Wang, and S. Zhang, “Roboos-next: A unified memory-based framework for 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

34 

lifelong, scalable, and robust multi-robot collaboration,” _CoRR_ , vol. abs/2510.26536, 2025. 

- [693] J. D. Wentao Yuan and, V. Blukis, W. Pumacay, R. Krishna, A. Murali, A. Mousavian, and D. Fox, “Robopoint: A vision-language model for spatial affordance prediction, in robotics,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 270. PMLR, 2024, pp. 4005–4020. 

- [694] C. Y. Boshi An and and R. K. Katzschmann, “Robotic assistant: Completing collaborative tasks with dexterous vision-language-action, models,” _CoRR_ , vol. abs/2510.25713, 2025. 

- [695] P. L. Xinghang Li and, M. Liu, D. Wang, J. Liu, B. Kang, X. Ma, T. Kong, H. Zhang, and H. Liu, “Towards generalist robot policies: What matters in building vision-language-action, models,” _CoRR_ , vol. abs/2412.14058, 2024. 

- [696] Z. W. Jianing Guo and, C. Tu, Y. Ma, X. Kong, Z. Liu, J. Ji, S. Zhang, Y. Chen, K. Chen, Q. Dou, Y. Yang, X. Liu, H. Zhao, W. Lv, and S. Li, “On robustness of vision-language-action model against multi-modal, perturbations,” _CoRR_ , vol. abs/2510.00037, 2025. 

- [697] L. L. Mingtong Dai and, Y. Bai, Y. Liu, Z. Wang, R. SU, C. Chen, L. Lin, and X. Wu, “Rover: Robot reward model as test-time verifier for vision-language-action, model,” _CoRR_ , vol. abs/2510.10975, 2025. 

- [698] W. B. Tobias J¨ulg and and F. Walter, “Refined policy distillation: From VLA generalists to RL experts,” in _IROS_ . IEEE, 2025, pp. 11 677– 11 684. 

- [699] J. L. Taeyoung Kim and, M. Koo, D. Kim, K. Lee, C. Kim, Y. Seo, and J. Shin, “Contrastive representation regularization for vision-languageaction, models,” _CoRR_ , vol. abs/2510.01711, 2025. 

- [700] T. Y. Brianna Zitkovich and, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, Q. Vuong, V. Vanhoucke, H. T. Tran, R. Soricut, A. Singh, J. Singh, P. Sermanet, P. R. Sanketi, G. Salazar, M. S. Ryoo, K. Reymann, K. Rao, K. Pertsch, I. Mordatch, H. Michalewski, Y. Lu, S. Levine, L. Lee, T. E. Lee, I. Leal, Y. Kuang, D. Kalashnikov, R. Julian, N. J. Joshi, A. Irpan, B. Ichter, J. Hsu, A. Herzog, K. Hausman, K. Gopalakrishnan, C. Fu, P. Florence, C. Finn, K. A. Dubey, D. Driess, T. Ding, K. M. Choromanski, X. Chen, Y. Chebotar, J. Carbajal, N. Brown, A. Brohan, M. G. Arenas, and K. Han, “RT-2: vision-language-action models transfer web knowledge to robotic, control,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 229. PMLR, 2023, pp. 2165–2183. 

- [701] S. K. Soroush Nasiriany and, T. Ding, L. Smith, Y. Zhu, D. Driess, D. Sadigh, and T. Xiao, “Rt-affordance: Affordances are versatile intermediate representations, for robot manipulation,” in _ICRA_ . IEEE, 2025, pp. 8249–8257. 

- [702] T. D. Suneel Belkhale and, T. Xiao, P. Sermanet, Q. Vuong, J. Tompson, Y. Chebotar, D. Dwibedi, and D. Sadigh, “RT-H: action hierarchies using language,” in _Robotics: Science and Systems_ , 2024. 

- [703] J. W. K. Samuel Schmidgall and, A. Kuntz, A. E. Ghazi, and A. Krieger, “General-purpose foundation models for increased autonomy in robot-assisted, surgery,” _Nat. Mac. Intell._ , vol. 6, no. 11, pp. 1275–1283, 2024. 

- [704] S. K. Jiayuan Gu and, P. Wohlhart, Y. Lu, M. G. Arenas, K. Rao, W. Yu, C. Fu, K. Gopalakrishnan, Z. Xu, P. Sundaresan, P. Xu, H. Su, K. Hausman, C. Finn, Q. Vuong, and T. Xiao, “Rt-trajectory: Robotic task generalization via hindsight trajectory, sketches,” in _ICLR_ . OpenReview.net, 2024. 

- [705] A. R. Abby O’Neill and, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain, A. Tung, A. Bewley, A. Herzog, A. Irpan, A. Khazatsky, A. Rai, A. Gupta, A. E. Wang, A. Singh, A. Garg, A. Kembhavi, A. Xie, A. Brohan, A. Raffin, A. Sharma, A. Yavary, A. Jain, A. Balakrishna, A. Wahid, B. BurgessLimerick, B. Kim, B. Sch¨olkopf, B. Wulfe, B. Ichter, C. Lu, C. Xu, C. Le, C. Finn, C. Wang, C. Xu, C. Chi, C. Huang, C. Chan, C. Agia, C. Pan, C. Fu, C. Devin, D. Xu, D. Morton, D. Driess, D. Chen, D. Pathak, D. Shah, D. B¨uchler, D. Jayaraman, D. Kalashnikov, D. Sadigh, E. Johns, E. P. Foster, F. Liu, F. Ceola, F. Xia, F. Zhao, F. Stulp, G. Zhou, G. S. Sukhatme, G. Salhotra, G. Yan, G. Feng, G. Schiavi, G. Berseth, G. Kahn, G. Wang, H. Su, H. Fang, H. Shi, H. Bao, H. B. Amor, H. I. Christensen, H. Furuta, H. Walke, H. Fang, H. Ha, I. Mordatch, I. Radosavovic, I. Leal, J. Liang, J. Abou-Chakra, J. Kim, J. Drake, J. Peters, J. Schneider, J. Hsu, J. Bohg, J. T. Bingham, J. Wu, J. Gao, J. Hu, J. Wu, J. Wu, J. Sun, J. Luo, J. Gu, J. Tan, J. Oh, J. Wu, J. Lu, J. Yang, J. Malik, J. Silv´erio, J. Hejna, J. Booher, J. Tompson, J. Yang, J. Salvador, J. J. Lim, J. Han, K. Wang, K. Rao, K. Pertsch, K. Hausman, K. Go, K. Gopalakrishnan, K. Goldberg, K. Byrne, K. Oslund, K. Kawaharazuka, K. Black, K. Lin, K. Zhang, K. Ehsani, K. Lekkala, K. Ellis, K. Rana, K. Srinivasan, K. Fang, K. P. Singh, K. Zeng, K. Hatch, K. Hsu, L. Itti, L. Y. Chen, L. Pinto, L. FeiFei, L. Tan, L. J. Fan, L. Ott, L. Lee, L. Weihs, M. Chen, M. Lepert, 

   - M. Memmel, M. Tomizuka, M. Itkina, M. G. Castro, M. Spero, M. Du, M. Ahn, M. C. Yip, M. Zhang, M. Ding, M. Heo, M. K. Srirama, M. Sharma, M. J. Kim, N. Kanazawa, N. Hansen, N. Heess, N. J. Joshi, N. S¨underhauf, N. Liu, N. D. Palo, N. M. M. Shafiullah, O. Mees, O. Kroemer, O. Bastani, P. R. Sanketi, P. T. Miller, P. Yin, P. Wohlhart, P. Xu, P. D. Fagan, P. Mitrano, P. Sermanet, P. Abbeel, P. Sundaresan, Q. Chen, Q. Vuong, R. Rafailov, R. Tian, R. Doshi, R. Mart´ın-Mart´ın, R. Baijal, R. Scalise, R. Hendrix, R. Lin, R. Qian, R. Zhang, R. Mendonca, R. Shah, R. Hoque, R. Julian, S. BustamanteGomez, S. Kirmani, S. Levine, S. Lin, S. Moore, S. Bahl, S. Dass, S. D. Sonawani, S. Song, S. Xu, S. Haldar, S. Karamcheti, S. Adebola, S. Guist, S. Nasiriany, S. Schaal, S. Welker, S. Tian, S. Ramamoorthy, S. Dasari, S. Belkhale, S. Park, S. Nair, S. Mirchandani, T. Osa, T. Gupta, T. Harada, T. Matsushima, T. Xiao, T. Kollar, T. Yu, T. Ding, T. Davchev, T. Z. Zhao, T. Armstrong, T. Darrell, T. Chung, V. Jain, V. Vanhoucke, W. Zhan, W. Zhou, W. Burgard, X. Chen, X. Wang, X. Zhu, X. Geng, X. Liu, L. Xu, X. Li, Y. Lu, Y. J. Ma, Y. Kim, Y. Chebotar, Y. Zhou, Y. Zhu, Y. Wu, Y. Xu, Y. Wang, Y. Bisk, Y. Cho, Y. Lee, Y. Cui, Y. Cao, Y. Wu, Y. Tang, Y. Zhu, Y. Zhang, Y. Jiang, Y. Li, Y. Li, Y. Iwasawa, Y. Matsuo, Z. Ma, Z. Xu, Z. J. Cui, Z. Zhang, and Z. Lin, “Open x-embodiment: Robotic learning datasets and RT-X models : Open, x-embodiment collaboration,” in _ICRA_ . IEEE, 2024, pp. 6892–6903. 

- [706] V. B. Ankit Goyal and, J. Xu, Y. Guo, Y. Chao, and D. Fox, “RVT-2: learning precise manipulation from few demonstrations,” in _Robotics: Science and Systems_ , 2024. 

- [707] S. H. Yuming Jiang and, S. Xue, Y. Zhao, J. Cen, S. Leng, K. Li, J. Guo, K. Wang, M. Chen, F. Wang, D. Zhao, and X. Li, “Rynnvla-001: Using human demonstrations to improve robot manipulation,” _CoRR_ , vol. abs/2509.15212, 2025. 

- [708] S. H. Jun Cen and, Y. Yuan, K. Li, H. Yuan, C. Yu, Y. Jiang, J. Guo, X. Li, H. Luo, F. Wang, D. Zhao, and H. Chen, “Rynnvla-002: A unified vision-language-action and world model,” _CoRR_ , vol. abs/2511.17502, 2025. 

- [709] B. Zhang, Y. Zhang, J. Ji, Y. Lei, J. Dai, Y. Chen, and Y. Yang, “Safevla: Towards safety alignment of vision-language-action model via constrained learning,” _arXiv preprint_ , 2025. 

- [710] K. C. Isabel Leal and, D. Jain, A. Dubey, J. Varley, M. S. Ryoo, Y. Lu, F. Liu, V. Sindhwani, Q. Vuong, T. Sarl´os, K. Oslund, K. Hausman, and K. Rao, “SARA-RT: scaling up robotics transformers with selfadaptive robust, attention,” in _ICRA_ . IEEE, 2024, pp. 6920–6927. 

- [711] Y. Z. Minjie Zhu and, J. Li, J. Wen, Z. Xu, N. Liu, R. Cheng, C. Shen, Y. Peng, F. Feng, and J. Tang, “Scaling diffusion policy in transformer to 1 billion parameters for, robotic manipulation,” in _ICRA_ . IEEE, 2025, pp. 10 838–10 845. 

- [712] C. Li, J. Liu, G. Wang, X. Li, S. Chen, L. Heng, C. Xiong, J. Ge, R. Zhang, K. Zhou, and S. Zhang, “A self-correcting vision-languageaction model for fast and slow system manipulation,” _arXiv preprint_ , 2024. 

- [713] A. L. Yilin Wu and, T. Hermans, F. Ramos, A. Bajcsy, and C. P´erezD’Arpino, “Do what you say: Steering vision-language-action models via runtime, reasoning-action alignment verification,” _CoRR_ , vol. abs/2510.16281, 2025. 

- [714] J. Z. Beichen Wang and, S. Dong, I. Fang, and C. Feng, “VLM see, robot do: Human demo video to robot action plan via vision, language model,” in _IROS_ . IEEE, 2025, pp. 17 215–17 222. 

- [715] Z. A. Ran Yang and, L. Zhou, and Y. Feng, “Seqvla: Sequential task execution for long-horizon manipulation with, completion-aware vision-language-action model,” _CoRR_ , vol. abs/2509.14138, 2025. 

- [716] L. L. Kevin Qinghong Lin and, D. Gao, Z. Yang, S. Wu, Z. Bai, S. W. Lei, L. Wang, and M. Z. Shou, “Showui: One vision-language-action model for GUI visual agent,” in _CVPR_ . Computer Vision Foundation / IEEE, 2025, pp. 19 498–19 508. 

- [717] L. Wang, “Sigma: The key for vision-language-action models toward telepathic, alignment,” _CoRR_ , vol. abs/2512.00783, 2025. 

- [718] Y. Z. Haozhan Li and, J. Yu, Y. Zhang, Z. Yang, K. Zhang, X. Zhu, Y. Zhang, T. Chen, G. Cui, D. Wang, D. Luo, Y. Fan, Y. Sun, J. Zeng, J. Pang, S. Zhang, Y. Wang, Y. Mu, B. Zhou, and N. Ding, “Simplevlarl: Scaling VLA training via reinforcement learning,” _CoRR_ , vol. abs/2509.09674, 2025. 

- [719] H. S. Ayudh Saxena and, S. Routray, R. R. Shah, and E. Pahwa, “SITCOM: scaling inference-time compute for vlas,” _CoRR_ , vol. abs/2510.04041, 2025. 

- [720] D. A. Mustafa Shukor and, F. Capuano, P. Kooijmans, S. Palma, A. Zouitine, M. Aractingi, C. Pascal, M. Russi, A. Marafioti, S. Alibert, M. Cord, T. Wolf, and R. Cad`ene, “Smolvla: A vision-language- 

35 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

action model for affordable and efficient, robotics,” _CoRR_ , vol. abs/2506.01844, 2025. 

- [721] W. X. Jianping Jiang and, Z. Lin, H. Zhang, T. Ren, Y. Gao, Z. Lin, Z. Cai, L. Yang, and Z. Liu, “SOLAMI: social vision-language-action modeling for immersive interaction, with 3d autonomous characters,” in _CVPR_ . Computer Vision Foundation / IEEE, 2025, pp. 26 887– 26 898. 

- [722] W. S. Fuhao Li and, H. Zhao, J. Wang, P. Ding, D. Wang, L. Zeng, and H. Li, “Spatial forcing: Implicit spatial representation alignment for vision-language-action, model,” _CoRR_ , vol. abs/2510.12276, 2025. 

- [723] J. X. Hanzhen Wang and, J. Pan, Y. Zhou, and G. Dai, “Specprunevla: Accelerating vision-language-action models via action-aware, selfspeculative pruning,” _CoRR_ , vol. abs/2509.05614, 2025. 

- [724] R. Y. Songsheng Wang and, Z. Yuan, C. Yu, F. Gao, Y. Wang, and D. F. Wong, “Spec-vla: Speculative decoding for vision-languageaction models with, relaxed acceptance,” _CoRR_ , vol. abs/2507.22424, 2025. 

- [725] Y. L. Hengyu Fang and, Y. Du, L. Du, and H. Yang, “SQAP-VLA: A synergistic quantization-aware pruning framework for, high-performance vision-language-action models,” _CoRR_ , vol. abs/2509.09090, 2025. 

- [726] Y. Y. Zhejia Cai and, X. Chang, S. Liang, R. Chen, F. Xiong, M. Xu, and R. Huang, “Seeing space and motion: Enhancing latent actions with spatial and, dynamic awareness for VLA,” _CoRR_ , vol. abs/2509.26251, 2025. 

- [727] G. Z. Feng Xu and, X. Kong, T. Fu, D. F. N. Gordon, X. An, and B. Busam, “STARE-VLA: progressive stage-aware reinforcement for fine-tuning, vision-language-action models,” _CoRR_ , vol. abs/2512.05107, 2025. 

- [728] M. Y. Shengliang Deng and, Y. Zheng, J. Su, W. Zhang, X. Zhao, H. Cui, Z. Zhang, and H. Wang, “Stereovla: Enhancing vision-language-action models with stereo vision,” _CoRR_ , vol. abs/2512.21970, 2025. 

- [729] J. Z. Wenjun Lin and, K. Cai, and K. Wang, “STORM: searchguided generative world models for robotic manipulation,” _CoRR_ , vol. abs/2512.18477, 2025. 

- [730] P. G. Yufan He and, M. Xu, Z. Li, A. Myronenko, D. Imans, B. Liu, D. Yang, M. Gu, Y. Ji, Y. Jin, R. Zhao, B. Shen, and D. Xu, “Surgworld: Learning surgical robot policies from videos via world, modeling,” _CoRR_ , vol. abs/2512.23162, 2025. 

- [731] C. C. Chaojun Ni and, X. Wang, Z. Zhu, W. Zheng, B. Wang, T. Chen, G. Zhao, H. Li, Z. Dong, Q. Zhang, Y. Ye, Y. Wang, G. Huang, and W. Mei, “Swiftvla: Unlocking spatiotemporal dynamics for lightweight VLA, models at minimal overhead,” _CoRR_ , vol. abs/2512.00903, 2025. 

- [732] X. Z. Zonghuan Xu and, X. Ma, and Y. Jiang, “Tabvla: Targeted backdoor attacks on vision-language-action models,” _CoRR_ , vol. abs/2510.10932, 2025. 

- [733] S. M. Jonas Geiping and, N. Jain, J. Kirchenbauer, S. Singh, B. R. Bartoldson, B. Kailkhura, A. Bhatele, and T. Goldstein, “Scaling up test-time compute with latent reasoning: A recurrent, depth approach,” _CoRR_ , vol. abs/2502.05171, 2025. 

- [734] H. Z. Shuaijun Wang and, D. Xiang, and Y. You, “Tacrefinenet: Tactileonly grasp refinement between arbitrary in-hand, object poses,” _CoRR_ , vol. abs/2509.25746, 2025. 

- [735] S. W. Jialei Huang and, F. Lin, Y. Hu, C. Wen, and Y. Gao, “Tactilevla: Unlocking vision-language-action model’s physical knowledge, for tactile generalization,” _CoRR_ , vol. abs/2507.09160, 2025. 

- [736] H. X. Zongzheng Zhang and, Z. Yang, C. Yue, Z. Lin, H. Gao, Z. Wang, and H. Zhao, “TA-VLA: elucidating the design space of torque-aware vision-language-action, models,” _CoRR_ , vol. abs/2509.07962, 2025. 

- [737] C. Huang, Y. Wu, M. Chen, Y. F. Wang, and F. Yang, “Thinkact: Visionlanguage-action reasoning via reinforced visual latent planning,” _CoRR_ , vol. abs/2507.16815, 2025. 

- [738] Z. W. Guanxing Lu and, C. Liu, J. Lu, and Y. Tang, “Thinkbot: Embodied instruction following with thought chain reasoning,” in _ICLR_ . OpenReview.net, 2025. 

- [739] J. Z. Shaoan Wang and, M. Li, J. Liu, A. Li, K. Wu, F. Zhong, J. Yu, Z. Zhang, and H. Wang, “Trackvla: Embodied visual tracking in the wild,” _CoRR_ , vol. abs/2505.23189, 2025. 

- [740] P. D. Jiacheng Liu and, Q. Zhou, Y. Wu, D. Huang, Z. Peng, W. Xiao, W. Zhang, L. Yang, C. Lu, and D. Wang, “Trajbooster: Boosting humanoid whole-body manipulation via trajectory-centric, learning,” _CoRR_ , vol. abs/2509.11839, 2025. 

- [741] Y. G. Zhenyang Liu and, S. Zheng, X. Xue, and Y. Fu, “Trivla: A triple-system-based unified vision-language-action model, for general robot control,” _CoRR_ , vol. abs/2507.01424, 2025. 

- [742] Y. Bai, Z. Wang, Y. Liu, K. Luo, Y. Wen, M. Dai, W. Chen, Z. Chen, L. Liu, G. Li, and L. Lin, “Learning to see and act: Task-aware virtual view exploration for robotic manipulation,” _arXiv preprint_ , 2025. 

- [743] W. S. Jiayi Chen and, P. Ding, Z. Zhou, H. Zhao, F. Tang, D. Wang, and H. Li, “Unified diffusion VLA: vision-language-action model via joint discrete, denoising diffusion process,” _CoRR_ , vol. abs/2511.01718, 2025. 

- [744] Y. Z. Zhangyuan Wang and, Y. Yan, X. Tian, X. Shao, M. Li, W. Li, G. Su, W. Cui, and D. Fan, “Underwatervla: Dual-brain visionlanguage-action architecture for, autonomous underwater navigation,” _CoRR_ , vol. abs/2509.22441, 2025. 

- [745] Y. H. Jianke Zhang and, Y. Guo, X. Chen, Y. Liu, W. Chen, C. Lu, and J. Chen, “Unicod: Enhancing robot policy via unified continuous and discrete, representation learning,” _CoRR_ , vol. abs/2510.10642, 2025. 

- [746] C. C. Jiasen Lu and, S. Lee, Z. Zhang, S. Khosla, R. Marten, D. Hoiem, and A. Kembhavi, “Unified-io 2: Scaling autoregressive multimodal models with vision, language, audio, and action,” in _CVPR_ . IEEE, 2024, pp. 26 429–26 445. 

- [747] K. W. Jiazhao Zhang and, S. Wang, M. Li, H. Liu, S. Wei, Z. Wang, Z. Zhang, and H. Wang, “Uni-navid: A video-based vision-languageaction model for unifying, embodied navigation tasks,” _CoRR_ , vol. abs/2412.06224, 2024. 

- [748] Z. L. Hao Lu and, G. Jiang, Y. Luo, S. Chen, Y. Zhang, and Y. Chen, “Uniugp: Unifying understanding, generation, and planing for end-toend, autonomous driving,” _CoRR_ , vol. abs/2512.09864, 2025. 

- [749] Y. Y. Hui Lu and, Y. Yang, C. Yi, Q. Zhang, B. Shen, A. C. Kot, and X. Jiang, “When robots obey the patch: Universal transferable patch attacks on, vision-language-action models,” _CoRR_ , vol. abs/2511.21192, 2025. 

- [750] Y. G. Jianke Zhang and, Y. Hu, X. Chen, X. Zhu, and J. Chen, “UPVLA: A unified understanding and prediction model for embodied, agent,” in _ICML_ . OpenReview.net, 2025. 

- [751] Z. W. Anqi Li and, J. Zhang, M. Li, Y. Qi, Z. Chen, Z. Zhang, and H. Wang, “Urbanvla: A vision-language-action model for urban micromobility,” _CoRR_ , vol. abs/2510.23576, 2025. 

- [752] Z. W. Junwen Gu and, P. Si, S. Qiu, Y. Feng, L. Sun, L. Luo, L. Yu, J. Wang, and Z. Wu, “USIM and U0: A vision-language-action dataset and model for, general underwater robots,” _CoRR_ , vol. abs/2510.07869, 2025. 

- [753] R. Y. Chuning Zhu and, S. Feng, B. Burchfiel, P. Shah, and A. Gupta, “Unified world models: Coupling video and action diffusion for pretraining, on large robotic datasets,” _CoRR_ , vol. abs/2504.02792, 2025. 

- [754] L. A. Jonas Pai and, V. Montesinos, B. Forrai, O. Mees, and E. Nava, “mimic-video: Video-action models for generalizable robot control beyond, vlas,” _CoRR_ , vol. abs/2512.15692, 2025. 

- [755] J. L. Yueru Jia and, S. Liu, R. Zhou, W. Yu, Y. Yan, X. Chi, Y. Guo, B. Shi, and S. Zhang, “Video2act: A dual-system video diffusion policy with robotic spatio-motional, modeling,” _CoRR_ , vol. abs/2512.03044, 2025. 

- [756] F. W. Yichao Shen and, Z. Du, Y. Liang, Y. Lu, J. Yang, N. Zheng, and B. Guo, “Videovla: Video generators can be generalizable robot manipulators,” _CoRR_ , vol. abs/2512.06963, 2025. 

- [757] J. Y. Jeongeun Park and, B. Jeon, J. Park, J. Shin, N. Cho, K. Lee, S. Yun, and S. Choi, “Hierarchical vision language action model using success and failure, demonstrations,” _CoRR_ , vol. abs/2512.03913, 2025. 

- [758] M. W. Guangyan Chen and, Q. Shao, Z. Zhou, W. Mao, T. Cui, M. Zhu, Y. Deng, L. Yang, Z. Zhang, Y. Yang, H. Chen, and Y. Yue, “See once, then act: Vision-language-action model with task learning, from oneshot video demonstrations,” _CoRR_ , vol. abs/2512.07582, 2025. 

- [759] H. H. Ankit Goyal and, X. Yang, V. Blukis, and F. Ramos, “VLA0: building state-of-the-art vlas with zero modification,” _CoRR_ , vol. abs/2510.13054, 2025. 

- [760] C. M. Hanyu Zhou and and G. H. Lee, “VLA-4D: embedding 4d awareness into vision-language-action models, for spatiotemporally coherent robotic manipulation,” _CoRR_ , vol. abs/2511.17199, 2025. 

- [761] P. D. Yihao Wang and, L. Li, C. Cui, Z. Ge, X. Tong, W. Song, H. Zhao, W. Zhao, P. Hou, S. Huang, Y. Tang, W. Wang, R. Zhang, J. Liu, and D. Wang, “Vla-adapter: An effective paradigm for tiny-scale visionlanguage-action, model,” _CoRR_ , vol. abs/2509.09372, 2025. 

- [762] M. Z. Yuze Wu and, X. Li, Y. Du, Y. Fan, W. Li, Z. Han, X. Zhou, and F. Gao, “VLA-AN: an efficient and onboard vision-language-action framework, for aerial navigation in complex environments,” _CoRR_ , vol. abs/2512.15258, 2025. 

- [763] Y. W. Siyu Xu and, C. Xia, D. Zhu, T. Huang, and C. Xu, “Vlacache: Towards efficient vision-language-action model via adaptive, token caching in robotic manipulation,” _CoRR_ , vol. abs/2502.02175, 2025. 

36 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

- [764] Y. X. Yuping Yan and, Y. Zhang, L. Lyu, H. Wang, and Y. Jin, “When alignment fails: Multimodal adversarial attacks on vision-languageaction, models,” _CoRR_ , vol. abs/2511.16203, 2025. 

- [765] Z. L. Chongkai Gao and, Z. Chi, J. Huang, X. Fei, Y. Hou, Y. Zhang, Y. Lin, Z. Fang, Z. Jiang, and L. Shao, “VLA-OS: structuring and dissecting planning representations and, paradigms in vision-languageaction models,” _CoRR_ , vol. abs/2506.17561, 2025. 

- [766] J. L. Zhuo Li and, Z. Dong, T. Teng, Q. Rouxel, D. G. Caldwell, and F. Chen, “Towards deploying VLA without fine-tuning: Plug-andplay inference-time, VLA policy steering via embodied evolutionary diffusion,” _CoRR_ , vol. abs/2511.14178, 2025. 

and J. Tang, “XR-1: towards versatile vision-language-action models via learning, unified vision-motion representations,” _CoRR_ , vol. abs/2511.02776, 2025. 

   - [786] J. L. Jinliang Zheng and, Z. Wang, D. Liu, X. Kang, Y. Feng, Y. Zheng, J. Zou, Y. Chen, J. Zeng, Y. Zhang, J. Pang, J. Liu, T. Wang, and X. Zhan, “X-VLA: soft-prompted transformer as scalable cross-embodiment vision-language-action, model,” _CoRR_ , vol. abs/2510.10274, 2025. 

- [767] Y. C. Ziyan Liu and, H. Cai, T. Lin, S. Yang, Z. Liu, and B. Zhao, “Vlapruner: Temporal-aware dual-level visual token pruning for efficient, vision-language-action inference,” _CoRR_ , vol. abs/2511.16449, 2025. 

- [768] O. G. Y. Cyrus Neary and, A. Kuramshin, O. Aslan, and G. Berseth, “Improving pre-trained vision-language-action policies with modelbased, search,” _CoRR_ , vol. abs/2508.12211, 2025. 

- [769] S. M. Hyunki Seong and, H. Ahn, J. Kang, and D. H. Shim, “Vla-r: Vision-language action retrieval toward open-world end-to-end autonomous driving,” 2025. [Online]. Available: https: //dblp.org/rec/journals/corr/abs-2511-12405 

- [770] Z. Z. Angen Ye and, B. Wang, X. Wang, D. Zhang, and Z. Zhu, “Vlar1: Enhancing reasoning in vision-language-action models,” 2025. [Online]. Available: https://dblp.org/rec/journals/corr/abs-2510-01623 

- [771] L. Z. Yongsheng Zhao and, B. Cheng, G. Yao, X. Wen, and H. Gao, “VLA-RAIL: A real-time asynchronous inference linker for VLA, models and robots,” _CoRR_ , vol. abs/2512.24673, 2025. 

- [772] P. D. Hengtao Li and, R. Suo, Y. Wang, Z. Ge, D. Zang, K. Yu, M. Sun, H. Zhang, D. Wang, and W. Su, “VLA-RFT: vision-language-action reinforcement fine-tuning with verified, rewards in world simulators,” _CoRR_ , vol. abs/2510.00406, 2025. 

- [773] P. D. Wei Zhao and, M. Zhang, Z. Gong, S. Bai, H. Zhao, and D. Wang, “VLAS: vision-language-action model with speech instructions for, customized robot manipulation,” in _ICLR_ . OpenReview.net, 2025. 

- [774] T. Z. Ganlin Yang and, H. Hao, W. Wang, Y. Liu, D. Wang, G. Chen, Z. Cai, J. Chen, W. Su, W. Zhou, Y. Qiao, J. Dai, J. Pang, G. Luo, W. Wang, Y. Mu, and Z. Hou, “Vlaser: Vision-language-action model with synergistic embodied reasoning,” _CoRR_ , vol. abs/2510.11027, 2025. 

- [775] Y. S. Jiaming Tang and, Y. Zhao, S. Yang, Y. Lin, Z. Zhang, J. Hou, Y. Lu, Z. Liu, and S. Han, “VLASH: real-time vlas via future-stateaware asynchronous inference,” _CoRR_ , vol. abs/2512.01031, 2025. 

- [776] X. W. Asher J. Hancock and, L. Zha, O. Russakovsky, and A. Majumdar, “Actions as language: Fine-tuning vlms into vlas without catastrophic, forgetting,” _CoRR_ , vol. abs/2509.22195, 2025. 

- [777] M. W. Guangyan Chen and, T. Cui, Y. Mu, H. Lu, T. Zhou, Z. Peng, M. Hu, H. Li, L. Yuan, Y. Yang, and Y. Yue, “Vlmimic: Vision language models are visual imitation learner for fine-grained, actions,” in _NeurIPS_ , 2024. 

- [778] C. W. Wenlong Huang and, R. Zhang, Y. Li, J. Wu, and L. Fei-Fei, “Voxposer: Composable 3d value maps for robotic manipulation with language, models,” in _CoRL_ , ser. Proceedings of Machine Learning Research, vol. 229. PMLR, 2023, pp. 540–562. 

- [779] M. W. Mingjie Xu and, Y. Zhao, J. C. L. Li, and W. Ou, “Llavaspacesgg: Visual instruct tuning for open-vocabulary scene graph, generation with enhanced spatial relations,” in _WACV_ . IEEE, 2025, pp. 6362–6372. 

- [780] J. C. Yifang Xu and, F. Cai, Z. Zhu, H. Shang, S. Luan, M. Xu, N. Zhang, Y. Li, J. Cai, and S. Zhu, “Wam-flow: Parallel coarse-to-fine motion planning via discrete flow, matching for autonomous driving,” _CoRR_ , vol. abs/2512.06112, 2025. 

- [781] J. C. Haoran Jiang and, Q. Bu, L. Chen, M. Shi, Y. Zhang, D. Li, C. Suo, C. Wang, Z. Peng, and H. Li, “Wholebodyvla: Towards unified latent VLA for whole-body loco-manipulation, control,” _CoRR_ , vol. abs/2512.11047, 2025. 

- [782] Z. Y. Fangqi Zhu and, Z. Hong, Q. Shou, X. Ma, and S. Guo, “WMPO: world model-based policy optimization for vision-languageaction, models,” _CoRR_ , vol. abs/2511.09515, 2025. 

- [783] X. C. Zezhong Qian and, Y. Li, S. Wang, Z. Qin, X. Ju, S. Han, and S. Zhang, “Wristworld: Generating wrist-views via 4d world models for robotic, manipulation,” _CoRR_ , vol. abs/2510.07313, 2025. 

- [784] H. C. Pei Yang and, Y. Song, and M. Z. Shou, “X-humanoid: Robotize human videos to generate humanoid videos at scale,” _CoRR_ , vol. abs/2512.04537, 2025. 

- [785] K. W. Shichao Fan and, Z. Che, X. Wang, D. Wu, F. Liao, N. Liu, Y. Zhang, Z. Zhao, Z. Xu, M. Li, Q. Liu, S. Zhang, M. Wan, 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

37 

## APPENDIX 

## _A. Background_ 

_1) Unimodal Models:_ Vision-language-action models integrate three modalities, often relying on existing unimodal models. The transition from convolutional neural networks (e.g., ResNet [220]) to visual Transformers (e.g., ViT [221], SAM [222]) in computer vision has facilitated the development of vision foundation models (VFMs). In natural language processing, the evolution from recurrent neural networks (e.g., LSTM [223], GRU [224]) to Transformers [3] initially led to the pretrain-finetune paradigm (e.g., BERT [27], ChatGPT [225]), followed by the recent success of prompt tuning driven by large language models. Reinforcement learning (e.g., DQN [4], AlphaGo [226], PPO [227], Dactyl [228]) has also witnessed a shift towards employing Transformers to model the Markov Decision Process as autoregressive sequential data. DPO [229] directly trains LLMs on human preferences, simplifying RLHF. 

_2) Vision-Language Models:_ Vision-language tasks, encompassing image captioning [230], visual question answering [231], visual grounding [232], require the fusion of computer vision and natural language processing models. Early efforts, such as Show and Tell [233], leveraged the success of early CNNs and RNNs. The advent of high-capacity language models, including BERT [27] and GPT [234], ushered in a new era of Transformer-based VLMs. One of the pioneering self-supervised pretraining methods is ViLBERT [235], while CLIP [23] popularized contrastive pretraining approaches for multimodal alignment. The recent emergence of large language models has driven the development of multimodal LLMs (MLLMs) or large multimodal models (LMMs), which achieve state-of-the-art performance on multimodal instruction-following tasks. Representative MLLMs include Flamingo [6], BLIP-2 [7], and LLaVA [8]. VLMs share a close relationship with VLAs, as the multimodal architectures of VLMs can be readily adopted for VLAs. Additionally, VLMs can function as high-level task planners if they possess sufficient reasoning capabilities. 

## _B. Background (Extended Version): Unimodal Models_ 

Vision-language-action models involve three modalities, and consequently, many VLAs depend on existing unimodal models for processing inputs from different modalities. Therefore, it is crucial to summarize representative developments in unimodal models, as they often serve as integral components in VLAs. Specifically, for the vision modality, we collect models designed for image classification, object detection, and image segmentation, as these tasks are particularly relevant for robotic learning. Natural language processing models play a crucial role in enabling VLAs to understand language instructions or generate language responses. Reinforcement learning is a foundational component for obtaining optimal policies, facilitating the generation of appropriate actions in a given environment and condition. A brief timeline of the development of unimodal models is depicted in Figure 7. Additionally, Figure 8 highlights the progressive increase in model size within these fields. 

_1) Computer Vision:_ Computer vision witnessed the inception of modern neural networks. In robotics, object classification models can be used to inform a policy about which objects are of interest, and models for object detection or image segmentation can help precisely locate objects. Therefore, we mainly summarize approaches for these tasks, but numerous excellent surveys on visual models, ranging from convolutional neural networks (CNNs) [236] to Transformers [237], offer more detailed insights. Interested readers are directed to these surveys for a more comprehensive introduction. Here, we will briefly touch upon some of the key developments in the field of computer vision. 

_a) Convolutional Neural Network:_ Early developments in computer vision (CV) were primarily focused on the image classification task. LeNet [238] was among the first convolutional neural networks, designed for identifying handwritten digits in zip codes. In 2012, AlexNet [2] emerged as a breakthrough by winning the ImageNet challenge, showcasing the potential of neural networks. VGG [239] demonstrated the benefits of increasing the depth of CNNs. GoogLeNet [240], also known as Inception-V1, introduced the concept of blocks. ResNet [220] introduced skip connections or residual connections. Inception-ResNet [241], as the name suggests, combines residual connects and inception blocks. ResNeXt [242] explored the concept of split, transform, and merge. SENet [243] introduces the squeeze-and-excitation blocks, utilizing a type of attention mechanism. EfficientNet [244] studied the width, depth, and resolution of CNN models with “compound scaling,” highlighting the trade-off between efficiency and performance. 

Alongside image classification, object detection became an integral component in many applications. Building upon the success of image classification backbone networks, a series of works optimized region-based methods: R-CNN [245], Fast R-CNN [246], Faster R-CNN [247], and Mask R-CNN [248]. Grid-based methods like YOLO [249] are also widely adopted. Bottom-up, top-down is also a popular strategy, employed by FPN [250], RetinaNet [251], BUTD [252], etc. In scenarios requiring more detailed and precise object detection, image segmentation aims to determine the exact outline of objects. Many popular models adopt an “encoder-decoder” architecture, where the encoder understands both the global and local context of the image, and the decoder produces a segmentation map based on this context information. Representative works following this idea include FCN [253], SegNet [254], Mask R-CNN [248], and U-Net [255]. 

_b) Vision Transformer:_ Convolutional neural networks (CNNs) have historically been the foundation of computer vision models. However, the landscape shifted with the introduction of the Transformer architecture in the seminal work by [3]. This paradigm shift was initiated by ViT [221]. It revolutionizes image processing by breaking down images into 16-by-16 pixel patches, treating each as a token akin to those in NLP; leveraging a BERT-like model, ViT encodes these patches and has exhibited superior performance over many traditional CNN models in image classification tasks. 

The transformative power of the Transformer extends beyond classification. DETR [256] employs an encoder-decoder 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

38 


Fig. 7. A brief timeline of pivotal unimodal models leading to the development of vision-language-action models, organized by their publication years. Details can be found in Appendix:B. 

Transformer architecture to tackle object detection. The encoder processes the input image, and its output embeddings are fed into the decoder through cross-attention. Notably, DETR introduces learnable object queries to the decoder, facilitating the extraction of crucial object-wise information from the encoder’s output. Venturing into image segmentation, Segmenter [257] was the first to utilize Transformer on this task. The Segment Anything model (SAM) [222] achieves remarkable milestones in promptable segmentation, zero-shot performance, and versatile architecture, further underlining the transformative impact of Vision Transformer models in various computer vision domains. 

_c) Vision in 3D:_ Aside from the most common RGB data, other types of visual inputs are widely used [258], [259]. In robotics, depth maps are useful since they provide essential 3D information that is not explicitly stored in RGB images. Depth maps can be captured with Microsoft Kinect<sup>1</sup> or Intel RealSense<sup>2</sup> or recovered from pure RGB images. Point clouds [260] are also popular visual input types due to the widespread adoption of LiDARs and 3D scanners; depth maps can be easily converted to point clouds. Volumetric data [261], such as voxels or octrees, is usually more information-rich than depth 

> 1https://azure.microsoft.com/en-us/products/kinect-dk/ 

> 2https://www.intelrealsense.com 

maps and is suitable for representing rigid objects. Despite the widespread use of 3D meshes as the default data format in computer graphics, their irregular nature poses challenges for neural networks [262]. 

_2) Natural Language Processing:_ Natural Language Processing (NLP) plays a pivotal role in VLA, serving as a vital component for understanding user instructions or even generating appropriate textual responses. The recent surge in NLP owes much to the success of Transformer models [3]. In the landscape of contemporary NLP, there is a noticeable shift towards implicit learning of language syntax and semantics, a departure from the previous paradigms. To provide context, this subsection will commence with a concise overview of fundamental yet enduring concepts before delving into the noteworthy advancements in contemporary NLP. For an indepth exploration of the progress in the NLP domain, readers are directed to comprehensive surveys by [263] and [264], which meticulously review the trajectory of advancements in NLP. 

_a) Early Developments:_ The field of NLP, which was more frequently referred to as Computational Linguistics (CL) in the early days, tries to solve various tasks regarding to natural language. In CL, natural languages used to be processed in a hierarchical way: word, syntax, and semantics. Firstly, on the 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

39 


Fig. 8. The growing scale of unimodal models over the years. _∗_ GPT-4’s model size is estimated since it has not been officially disclosed. 

word level, many aspects need to be accounted for, including morphology, lexicology, phonology, etc. This leads to problems like tokenization, lemmatization, stemming, semantic relations, word sense disambiguation, and Zipf’s Law problem. Then, in terms of syntax, natural language, in contrast to formal language, has much less restricted grammar and thus is more challenging to parse: in the Chomsky hierarchy, natural language is generally considered to follow context-sensitive grammar, while programming languages are covered under context-free grammar. Syntactic parsing includes tasks such as part-of-speech tagging, constituency parsing, dependency parsing, and named entity recognition. Finally, to understand the semantics of a sentence in written language or an utterance in spoken language, the following tasks were studied: semantic role labeling, frame semantic parsing, abstract meaning representation, logical form parsing, etc. 

_b) Recurrent Neural Network & Convolutional Neural Network:_ In the initial stages of NLP, rudimentary models relied on simple feed-forward neural networks to tackle various tasks [265]. After the introduction of word embeddings like word2vec [266], [267] and GloVe [268], NLP techniques embraced recurrent neural networks (RNNs) [269], such as LSTM [223], GRU [224], RNNsearch [270], LSTM-CRF [271], etc. Examples of representative RNNs in NLP include ELMo [272] and ULMFiT [273]. While RNNs played a significant role, alternative models utilizing convolutional neural networks also emerged. WordCNN [274] employed CNNs at the word level, with word2vec features serving as input to the CNNs. Another 

approach, CharCNN [275], focused on modeling language at the character level with CNN. Subsequent research [276] highlighted that character-level CNNs excel at capturing word morphology, and their combination with a word-level LSTM backbone can significantly enhance performance. 

_c) Transformer & Large Language Model:_ The groundbreaking Transformer model, introduced by [3], revolutionized natural language processing through the introduction of the self-attention mechanism, inspiring a cascade of subsequent works. BERT [27] leverages the Transformer encoder stack, excelling in natural language understanding. On the other hand, the GPT family [234], [277], [278], [279] is built upon Transformer decoder blocks, showcasing prowess in natural language generation tasks. A line of work strives to refine the original BERT, including RoBERTa [280], ALBERT [281], ELECTRA [282]. Simultaneously, a parallel line of research following the GPT paradigm has given rise to models like XLNet [283], OPT [284]. BART [285], an encoder-decoder Transformer, distinguishes itself through pretraining using the denoising sequence-to-sequence task. Meanwhile, T5 [286] introduces modifications to the original Transformer, maintaining the encoder-decoder architecture. T5 unifies various NLP tasks through a shared text-to-text format, exhibiting enhanced performance in transfer learning. These diverse models collectively showcase the versatility and ongoing evolution within the NLP landscape. 

Over the past few years, there has been a remarkable expansion in the size of language models, driven by the 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

40 

scalability of the Transformer architecture. This trend has given rise to a series of large language models (LLMs) that have demonstrated breakthrough performance and capabilities not achievable with smaller models. A landmark model in this evolution is ChatGPT [225], which has sparked considerable interest and inspired a series of works in this domain, such as GPT-4 [279], PaLM [287], PaLM-2 [288], LLaMA [289], LLaMA 2 [290], ERNIE 3.5 [291]. Notably, LLaMA stands out as one of the few open-source LLMs, fostering interesting developments. The introduction of “instructiontuning” has allowed efficient finetuning of a pretrained LLM to become an instruction-following model. This technique is popularized by InstructGPT [292] and FLAN [293], [294]. Recent advancements in instruction-following models include Alpaca [295], employing self-instruction, and Vicuna [296], leveraging conversations from ShareGPT. As LLMs grow in scale and power, there is a shift away from the need for finetuning on downstream tasks. With appropriate prompts, LLMs can produce accurate outputs without task-specific training, a paradigm known as _prompt engineering_ . This approach differs from the traditional _pretrain-finetune_ paradigm. DPO [229] introduces a method to train LLMs directly on human preferences without requiring explicit reward modeling or reinforcement learning, simplifying upon previous RLHF methods. 

_3) Reinforcement Learning:_ Reinforcement learning (RL) seeks to acquire a policy capable of taking optimal actions based on observations of the environment. Numerous visionlanguage-action models are constructed based on paradigms such as imitation learning or Temporal Difference (TD) learning within RL. Many challenges faced in the development of robotic policies can be effectively addressed through insights gained from the field of RL. Consequently, delving into RL methods presents a valuable avenue for enhancing robotic learning. For a deeper exploration of RL methods, readers can refer to more comprehensive reviews provided by [297], [298], and [299]. 

_a) Deep Reinforcement Learning:_ The advent of deep reinforcement learning can be attributed to the success of pioneering models, Deep Q-Network [4] and AlphaGo [226]. Deep learning, with its ability to provide low-dimensional representations, proved instrumental in overcoming traditional computational and memory complexity challenges in reinforcement learning. In recent years, a multitude of valuefunction-based approaches have surfaced. Double DQN (DDQN) [300] addresses the action value overestimation issue of DQN. Hindsight experience replay (HER) [301] focuses on the sparse reward issue. Batch-Constrained deep Q-learning (BCQ) [302] presents an approach aimed at enhancing offpolicy learning by constraining the action space. BEAR [303] endeavors to alleviate instability arising from bootstrapping errors in off-policy RL. [304] introduces conservative Q- learning (CQL) to address the overestimation of values by standard off-policy RL methods. 

Another paradigm within reinforcement learning is policy search, encompassing methods such as policy gradient and actor-critic techniques. These approaches aim to combat persistent challenges, including instability, slow convergence, and 

data inefficiency. Guided policy search (GPS) [305] learns a policy with importance sampling guided by another controller toward a local optimum. Deterministic policy gradient (DPG) [306], deep deterministic policy gradient (DDPG) [307], and asynchronous advantage actor-critic (A3C) [308] improve efficiency without compromising stability. Normalized advantage functions (NAF) [309] are a continuous variant of Q-learning, allowing for Q-learning with experience replay. Soft actorcritic (Soft AC) [310] takes advantage of the maximum entropy RL framework to lower sample complexity and improve convergence properties. Trust region policy optimization (TRPO) [311] and proximal policy optimization (PPO) [227] utilize trust region methods to stabilize policy gradients, with PPO additionally incorporating a truncated generalized advantage estimation (GAE) [312]. 

Beyond these, various other RL methodologies exist, such as imitation learning and hierarchical reinforcement learning. Generative adversarial imitation learning (GAIL) [313] is an imitation learning method that uses a generative adversarial framework to discriminate expert trajectories against generated trajectories. Robust adversarial reinforcement learning (RARL) [314] incorporates adversarial agents to enhance generalization. RLHF [315] utilizes human preferences without access to the reward function. FeUdal Networks (FuN) [316] introduce a hierarchical reinforcement learning architecture featuring a Manager module and a Worker module. 

_b) Robotics:_ In the field of RL, robotics stands out as one of the most prevalent and impactful applications. A noteworthy contribution to this field is E2E-DVP [317]. This pioneering model represents one of the first end-to-end solutions for robotic control. Its neural network is designed to take raw images as input and generate motor torques as output. [5] curated a substantial real-world dataset and developed a CNN that predicts grasps based on monocular input images. Building upon these foundations, QT-Opt [318] further expands the dataset and model scale, introducing closed-loop control capabilities to enhance robotic control systems. Then Dreamer [53] addresses long-horizon tasks. OpenAI also developed a dexterous robot hand that can solve the Rubik’s cube [228], [319]. 

_4) Graph:_ Graph is ubiquitous in many scenarios, such as social networks, molecule structures, 3D object meshes, etc. Even images and text can be modeled as a 2D grid and a linear graph (path graph), respectively. To process graphstructured data, recurrent graph neural networks [320] were first introduced, which were later optimized by convolutional graph neural networks. The review of graph neural networks (GNN) [321] can be referred to for more in-depth details. 

Convolutional graph neural networks can be generally divided into two categories: spectral-based and spatial-based. Spectral-based convolutional GNNs draw inspiration from graph signal processing, which provides theoretical support for the design of the networks. However, spatial-based convolutional GNNs have an advantage in terms of their efficiency and flexibility. Spectral CNN [322] is one of the first convolutional GNNs, but it is not robust to changes in graph structure and has a high computational cost. ChebNet [323] and GCN [324] significantly reduced the cost: ChebNet used an approximation 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

41 

based on Chebyshev polynomials, and GCN is its first-order approximation. Neural Network for Graphs (NN4G) [325] is the first spatial network. MPNN [326] introduced a general framework of spatial-based networks under which most existing GNNs can be covered. But the drawback of MPNN is that it does not embed graph structure information, which is later solved by GIN [327]. GraphSage [328] improves efficiency by sampling a fixed number of neighbors. Graph Attention Network (GAT) [329] incorporates the attention mechanism. 

Besides recurrent and convolutional graph neural networks, there are graph autoencoders [330], [331] and spatial-temporal graph neural networks [332]. Equivariant message passing networks are recently introduced to handle 3D graphs, including E(n)- and SE(3)- Equivariant GNN [333], [334]. Graph Transformer models make use of the power of Transformers to process graph data. There are already over 20 such graph Transformer models, such as GROVER [335] and SE(3)Transformers [336]. 

_a) Graph and Vision:_ Graph structures also exist in some computer vision tasks. Scene graph [337] can be used to express object relationships in most visual inputs. In addition to detecting objects in an image, scene graph generation necessitates the understanding of the relationships between detected objects. For example, a model needs to detect a person and a cup, and then understand that the person is holding the cup, which is the relationship between the two objects. Knowledge graphs often contain visual illustrations, such as WikiData. Those graphs can be helpful in downstream computer vision tasks. 

_b) Graph and Language:_ Graph structures are ubiquitous in language data [338]. Word-level graphs include dependency graphs, constituency graphs, AMR graphs, etc. Word-level means each node of those graphs corresponds to a word in the original text. These graphs can be used to explicitly represent the syntax or semantics of the raw sentence. Sentencelevel graphs can be useful in dialog tracking [339], fact checking [340], etc. Document-level graphs include knowledge graphs [341], citation graphs [342], etc. They can be used in document-level tasks, such as document retrieval, document clustering, etc. Different types of language graphs are often processed using the aforementioned GNNs to facilitate downstream tasks. 

_C. Background (Extended Version): Vision-Language Models_ 

Comprehensive surveys on VLMs exist, covering early BERT-based VLMs [387], [388] (Section C1), as well as more recent VLMs with contrastive pretraining [389], [390] (Section C2). Given the rapid evolution of this field and the emergence of new VLMs based on large language models, commonly known as large multimodal models (LMMs), we also compile the latest developments of LMMs (Section C3). To compare the most representative VLMs, we include their specifications in Table VIII. 

_1) Self-Supervised Pretraining:_ The evolution of the Transformer architecture to accommodate various modalities has given rise to robust multimodal Transformer models. Initial VLMs based on BERT can be broadly categorized into two 

types: single-stream and multi-stream [387]. Single-stream models employ a single stack of Transformer blocks to process both visual and linguistic inputs, whereas multistream models utilize a separate Transformer stack for each modality, with Transformer cross-attention layers exchanging multimodal information. To enhance alignment among modalities, these models incorporate various pretraining tasks aimed at absorbing knowledge from out-of-domain data. ViLBERT [235] stands as the pioneer in this line of work, featuring a multi-stream Transformer architecture. Text input undergoes standard processing in the language Transformer; image input is first processed using Faster R-CNN, and the output embeddings of all objects are then passed into the vision stream. The two Transformer outputs—language embeddings and vision embeddings—are combined using a novel coattention Transformer layer. VL-BERT [345] adopts a singlestream multimodal Transformer, simply concatenating vision and language tokens into a single input sequence. VideoBERT [391] adapts mulitmodal Transformer models to video inputs. UNITER [346] proposes the word-region alignment loss to explicitly align word with image regions. ViLT [347] uses ViTstyle [221] image patch projection to embed images, deviating from previous region or grid features. 

SimVLM [348] opts for a streamlined approach, relying solely on a single prefix language modeling objective to reduce training costs. VLMo [392] and BEiT-3 [352] both introduce mixture-of-modality-experts Transformers to effectively handle multimodal inputs. 

_2) Contrastive Pretraining:_ Vision-language pretraining in the initial series of BERT-based VLMs has evolved, with refinements such as curating larger-scale pretraining datasets, leveraging multimodal contrastive learning, and exploring specialized multimodal architectures. CLIP [23] is one of the earliest attempts in vision-language contrastive pretraining. By contrastive pretraining on a large-scale image-text pair dataset, CLIP exhibits the capability to be transferred to downstream tasks in a zero-shot fashion. In the same line of work, other few-/zero-shot learners have emerged. FILIP [353] concentrates on finer-grained multimodal interactions with a token-wise contrastive objective. ALIGN [354] focuses on learning from noisy datasets collected without filtering and post-processing. “Locked-image Tuning” (LiT) [393] posits that only training the text model while freezing the image model yields the best results on new tasks. In Frozen [394], the pretrained language model is frozen and a vision encoder is trained to produce image embeddings as a part of language model prompts, exemplifying an instance of prompt tuning. 

Unlike the two-tower frameworks of CLIP, FILIP, and ALIGN, which solely train unimodal encoders (image encoder and text encoder), ALBEF [356] additionally incorporates training a multimodal encoder on top of the unimodal encoders, with FLAVA [357] sharing a similar idea. In contrast to contrastive pretraining methods, CoCa [395] seeks to amalgamate the strengths of CLIP’s contrastive learning and SimVLM’s generative objective. Florence [351] generalizes representations from coarse, scene-level to fine, object-level, expands from images to videos, and encompasses modalities beyond RGB channels. OFA [396] draws inspiration from T5 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

42 

Table VIII 

VISION-LANGUAGE MODELS. IN THE “OBJECTIVE” COLUMN: “MLM”: MASKED LANGUAGE MODELING. “MVM”: MASKED VISION MODELING, RECONSTRUCTING MASKED IMAGE REGIONS. “VLM”: BINARY CLASSIFICATION OF WHETHER VISION AND LANGUAGE INPUTS MATCH. “LM”: AUTOREGRESSIVE LANGUAGE MODELING. “VLCL”: VISION-LANGUAGE CONTRASTIVE LEARNING. WE ONLY INCLUDE REPRESENTATIVE MULTIMODAL DATASETS DUE TO LIMITED SPACE. “MM” INCLUDES MULTIMODAL TASKS SUCH AS VISUAL QUESTION ANSWERING, IMAGE CAPTIONING, AND VISION-LANGUAGE RETRIEVAL. “VISION” REPRESENTS COMPUTER VISION TASKS, SUCH AS IMAGE CLASSIFICATION. “LANGUAGE” REPRESENTS NATURAL LANGUAGE PROCESSING TASKS 

|**Model**|**Vision Encoder**<br>**Name**|**Params**|**Language En**<br>**Name**|**coder**<br>**Params**|**VL-Fusion**|**Objectives**|**Datasets**|**Tasks**|
|---|---|---|---|---|---|---|---|---|
|ViLBERT [235]|Faster R-CNN [247],<br>[252]|44M|Dual-stream<br>BERT-base [27]|221M|Dual-stream|MLM, MVM,<br>VLM|COCO, VG|MM|
|LXMERT [343]|Faster R-CNN [247],<br>[252]|44M|Dual-stream<br>BERT-base [27]|183M|Dual-stream|MLM, MVM,<br>VLM, VQA|COCO, VG, VQA, GQA, VGQA|MM|
|VisualBERT [344]|Faster R-CNN [247],<br>[252]|60M|BERT-base [27]|110M|Single-stream|MLM, VLM|COCO|MM|
|ervised<br>VL-BERT [345]|Faster R-CNN [247],<br>[252]|44M|BERT-base [27]|110M|Single-stream|MLM, MVM|CC|MM|
|Self-sup<br>UNITER [346]|Faster R-CNN [247],<br>[252]|44M|BERT-base/<br>BERT-large [27]|86M/<br>303M|Single-stream|MLM, VLM,<br>MVM, WRA|COCO, VG, SBU, CC|MM|
|ViLT [347]|Linear projection [221]|2.4M|BERT-base [27]|85M|Single-stream|MLM, VLM|COCO, VG, SBU, CC|MM|
|SimVLM [348]|ViT/CoAtNet-huge<br>(shared encoder) [349]|632M|Shared encoder|632M|Single-stream|PrefixLM|ALIGN dataset|MM|
|GIT [350]|Florence [351]|637M|Transformer [3]|60M|Single-stream|LM|COCO, VG, SBU, CC, etc.|MM|
|BEiT-3 [352]|V-FFN<br>(+Shared Attn)|692M<br>(+317M)|L-FFN<br>(+Shared Attn)|692M<br>(+317M)|Modality experts|MLM, VLM|COCO, VG, SBU, CC|MM, Vision|
|CLIP [23]|ViT [221]|428M|GPT-2 [277]|63M|Two-tower|VLCL|WTI|Vision|
|FILIP [353]|ViT-L/14 [221]|428M|GPT [277]|117M|Two-tower|VLCL|FILIP300M (Self-collect)|MM, Vision|
|tive<br>ALIGN [354]|EfficientNet-L2 [355]|480M|BERT-large [27]|336M|Two-tower|VLCL|ALIGN dataset (Self-collect)|MM, Vision|
|ontras<br>ALBEF [356]|ViT-B/16 [221]|87M|BERT-base [27]|85M|Dual-stream|MLM, VLM,<br>VLCL|COCO, VG, CC, SBU|MM|
|C<br>FLAVA [357]|ViT-B/16 [221]|87M|RoBERTa-base<br>[280]|125M|Dual-stream|MLM, MVM,<br>VLM, VLCL|COCO, VG, CC, SBU, etc.<br>(PMD)|MM, Vision,<br>Language|
|Florence [351]|Hierarchical Vision<br>Transformers [358], [359]|637M|RoBERTa [280]|125M|Two-tower|VLCL|FLD-900M (Self-collect)|Vision|
|Flamingo [6]|NFNet-F6 [360]|438M|Chinchilla [361]|70B|Dual-stream|LM|M3W, ALIGN dataset, LTIP, VTP|MM|
|BLIP-2 [7]|CLIP ViT-L/14 [23],<br>EVA ViT-G/14 [362]<br>+ Q-Former|428M,<br>1B|OPT [284]<br>Flan-T5 [294]|6.7B<br>3B/11B|Single-stream|BLIP, LM|COCO, VG, CC, SBU, LAION|MM|
|PaLI [363]|ViT-e [363]|4B|mT5-XXL [364]|13B|Single-stream|Mixed|WebLI, etc|MM|
|PaLI-X [365]|ViT-22B [366]|22B|UL2 [367]|32B|Single-stream|Mixed|WebLI, etc|MM|
|LLaMA-Adapter<br>[368]|CLIP ViT-B/16 [23]|87M|LLaMA [289]|7B|Single-stream|LM|Self-instruct|Instruction-<br>following|
|LLaMA-Adapter-V2<br>[369]|CLIP ViT-L/14 [23]|428M|LLaMA [289]|7B|Single-stream|LM|GPT-4-LLM, COCO, ShareGPT|Instruction-<br>following|
|el<br>Kosmos-1 [370],<br>Kosmos-2 [371]|CLIP ViT-L/14 [23]|428M|Magneto [372]|1.3B|Single-stream|LM|LAION, COYO, CC; Unnatural<br>Instructions, FLANv2|Instruction-<br>following<br>(Kosmos-2|
|l Mod||||||||w/ grounding,<br>referring)|
|ltimoda<br>InstructBLIP [373]|EVA ViT-G/14 [362]|1B|Flan-T5 [294]<br>Vicuna [296]|3B/11B<br>7B/13B|Single-stream|BLIP, LM|COCO, VQA, LLaVA-Instruct-<br>150K, etc. (26 datasets)|Instruction-<br>following|
|rge Mu<br>LLaVA [8]|CLIP ViT-L/14 [23]|428M|LLaMA [289]|13B|Single-stream|LM|CC, (FT: GPT-assisted Visual<br>Instruction Data Generation)|Instruction-<br>following|
|La<br>MiniGPT-4 [374]|EVA ViT-G/14 [362]<br>+ Q-Former [7]|1B|Vicuna [296]<br>LLaMA2 [290]|7B/13B<br>7B|Single-stream|LM|CC, SBU, LAION (FT: SC)|Instruction-<br>following|
|Video-LLaMA [375]|EVA ViT-G/14 [362]<br>+ Q-Former [7]|1B|LLaMA [289]|7B/13B|Single-stream|BLIP, LM|CC595k|Instruction-<br>following|
|PandaGPT [376]|ImageBind ViT-H [211]|632M|Vicuna [296]|13B|Single-stream|LM|(FT: LLaVA data, MiniGPT-4<br>data)|Instruction-<br>following|
|VideoChat [377]|EVA ViT-G/14 [362]<br>+ Q-Former [7]|1B|StableVicuna<br>[378]|13B|Single-stream|LM|COCO, VG, CC, SBU (FT: SC,<br>MiniGPT-4, LLaVA data)|Instruction-<br>following|
|ChatSpot [379]|CLIP ViT-L/14 [23]|428M|Vicuna [296]|7B|Single-stream|LM|MGVLID, RegionChat|Instruction-<br>following, Vision|
|mPLUG-Owl [380],<br>mPLUG-Owl2 [381]|CLIP ViT-L/14 [23]<br>+ Visual Abstractor|428M|LLaMA [289]|7B|Single-stream|LM|LAION, COYO, CC, COCO (FT:<br>Alpaca, Vicuna, Baize [382] data)|Instruction-<br>following|
|Visual ChatGPT<br>[383]|(22 different models)|-|ChatGPT [225]|-|Prompt Manager|-|Add image understanding and gene|ration to ChatGPT|
|X-LLM [384]|ViT-G [385] + Q-Former<br>[7] + Adapter|1.8B|ChatGLM [386]|6B|Single-stream|Three-stage<br>training|MiniGPT-4 data, AISHELL-2,<br>ActivityNet, VSDial-CN (SC)|Instruction-<br>following|


IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

43 

[286] and proposes unifying diverse unimodal and multimodal tasks under a sequence-to-sequence learning framework. _3) Large Multimodal Model:_ Large language models (LLMs) encapsulate extensive knowledge, and efforts have been made to transfer this knowledge to multimodal tasks. Given the resource-intensive nature of finetuning entire LLMs on multimodal tasks due to their large size, various techniques have been explored to effectively connect frozen LLMs with vision encoders, enabling the combined model to acquire multimodal capabilities. Flamingo [6] connects a pretrained vision encoder, NFNet [360], and a large language model, Chinchilla [361], by inserting trainable gated cross-attention layers while keeping the rest of the model frozen. BLIP-2 [7] introduces Q- Former, bootstrapping vision-language representation learning first from a frozen CLIP ViT [23] and then from a frozen LLM, OPT [284] or Flan-T5 [294]. PaLI [363] and PaLIX [365] investigate the advantages of jointly scaling up the vision and language components using large-scale multilingual image-text data. 

Similar to developments in NLP, instruction-following has become a crucial aspect of VLMs, prompting the exploration of various multimodal instruction-tuning methods. LLaMAAdapter [368], [369] employs a parameter-efficient finetuning (PEFT) technique, enabling LLaMA [289] to process visual inputs. Kosmos-1 [370] introduces a less restrictive input format that accommodates interleaved image and text. Its Magneto LLM [372] serves as a “general-purpose interface” for docking with perception modules [23]. Kosmos-2 [371] adds additional grounding and referring capabilities. InstructBLIP [373] achieves instruction-following using an instruction-aware Q-Former based on BLIP-2’s Q-Former [7]. Comparable to Kosmos-2, ChatSpot [379] excels at following precise referring instructions, utilizing CLIP ViT [23] and Vicuna [296]. X-LLM [384] converts multimodality data into LLM inputs using X2L interfaces and treats them as foreign languages, where the X2L interface is inspired by the Q- Former from BLIP-2 [7]. mPLUG-Owl [380], [381] introduces a two-stage training paradigm that establishes a connection between a pretrained LLM with a visual encoder and a visual abstractor, thereby endowing LLMs with multimodality abilities. Visual ChatGPT [383] proposes a prompt manager that manages the interaction between ChatGPT and 22 visual foundation models, with the goal of equipping ChatGPT with the capability to understand and generate images. 

Rather than employing intricate mechanisms to connect components for different modalities, both LLaVA [8] and MiniGPT-4 [374] propose connecting vision encoders with LLMs through a single linear layer. LLaVA adopts a two-stage instruction-tuning approach, pretraining the CLIP ViT vision encoder [23] in the first stage and finetuning the linear layer and the LLaMA LLM [289] in the second stage. In contrast, MiniGPT-4 freezes both the vision encoder (BLIP-2’s ViT + Q-Former [7]) and the Vicuna LLM [296], only training the linear layer. Following MiniGPT-4, Video-LLaMA [375] handles videos by incorporating two branches for video and audio, each comprising a video/audio encoder and a BLIP-2-style Q-Former [7]. PandaGPT [376] leverages ImageBind [211] to encode vision/text/audio/depth/thermal/IMU data, feeding 

them to the Vicuna model [296] also through a linear layer. PandaGPT diverges from MiniGPT-4 by using LoRA [397] to train Vicuna alongside the linear layer. 

## _D. Supplementary Related Work_ 

Due to page limitations, we were unable to provide citations for all the mentioned models in the main text. Here is a list of supplementary related works: 

## Computer Vision: 

- Mask R-CNN [248] 

- YOLOv8 [249] 

- EfficientNet [244] 

- UNet [255] 

- VQ-GAN [398] 

- MoVQ [399] 

- SigLIP [400] 

- ViLD [401] 

- MDETR [402] 

- HLSM object detector [403] 

- ResNet [220] 

- ViT, ViT-B, ViT-L [26], [221] 

- MAE [404] 

- ViT-22B [366] 

- EVA ViT-G/14 [362] 

- OWL-ViT [405] 

- ConvNeXt [406] 

- SAM [222] 

- Imagen video [407] 

- C-ViViT [408] 

- OSRT [409] 

- PointNet [410] 

- PointNet++ [411] 

- 3D-CLR [412] 

- ConceptFusion [413] 

## Natural Language Processing, LLM, VLM: 

- Long Short-Term Memory (LSTM) [223] 

- Transformer [3] 

- Sentence-BERT / Sent.-BERT [414] 

- DistilBERT [415] 

- T5-small, T5-base, T5-XXL [286] 

- LLaMA [289] 

- LLaMA 2 [290] 

- Vicuna-V1.5 13B [296] 

- MPT [416] 

- FLAN [293] 

- Flamingo [6], [417] 

- Pythia [418] 

- Phi-2 [419] 

- GPT-NeoX [420] 

- Codex [421] 

- InstructGPT [376] 

- ChatGPT [225] 

- GPT-2 [277] 

- GPT-3 [278] 

- GPT-4 [279] 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

44 

- PaLI-X [365] 

- Prismatic-7B VLM [422] 

- PaliGemma [423] 

- PaliGemma 2 [424] 

- Chameleon [425] 

- Emu3 [426] 

- LWM-Chat-1M [427] 

- LLaMA-Adapter [368] 

Action Modules: 

- LingUNet [428] 

- Latent Motor Plans (LMP) [429] 

- STORM [430] 

- PerceiverIO [431] 

- DD-PPO [432] 

- ScaleDP [433] 

- Symbol-tuning [434] 

- DiT [435] 

## Others: 

- DDPM [436] 

- DDIM [437] 

- Ravens [438] 

- RLBench [180] 

- Something V2: Something-something V2 [439] 

Abbreviations: 

- TFM: Transformer 

- MCIL: multicontext imitation learning 

- MLE: maximum likelihood estimation 

- MPC: model predictive control 

- CVAE: conditional variational autoencoder 

- EDR: Everyday Robots 

## _E. Additional VLA-Related Work_ 

We include additional VLA-related work that could not be included in the main text due to the page limit. 

_1) Components of VLA: Pretraining:_ Value-Implicit Pretraining (VIP) [25] capitalizes on the temporal sequences present in videos, distinguishing itself from R3M [24] by attracting both the initial and target frames while simultaneously repelling successive frames. This objective aims to capture long-range temporal relationships and uphold local smoothness. While their own experiments demonstrate superior performance compared to R3M in specific tasks, subsequent research presents conflicting findings through more comprehensive evaluations [32]. 

SpawnNet [440] utilizes a two-stream architecture incorporating adapter layers to fuse features from both a pretrained vision encoder and features learned from scratch. This innovative approach eliminates the necessity of training the pretrained vision encoders while surpassing the performance of parameter-efficient finetuning (PEFT) methods, as evidenced by experimental results in robot manipulation tasks. 

Holo-Dex [441] proposes learning low-dimensional representations for visual policies using self-supervised learning (SSL). In Dobb _·_ E [442], SSL is also explored for 3D visual 

inputs, through a method termed “Home Pretrained Representations,” using data collected from 22 homes in NYC. The authors extend SSL-pretrained representations beyond visual inputs. AuRL [45] introduces learning dynamic behaviors from audio, an often-overlooked yet important information source. Additionally, visual inputs were found to be insufficient for multi-fingered robotic hands, leading to T-Dex [213], a tactilebased dexterous policy. 

_2) Components of VLA: World Models:_ Masked World Model (MWM) [443] innovates by modifying the vision encoder of DreamerV2 to a hybrid composition of convolutional neural network and vision Transformer. In training this novel Convolutional-ViT vision encoder, MWM draws inspiration from the approach proposed in MAE [404]. Through the incorporation of an auxiliary reward prediction loss, the resulting learned latent dynamics model exhibits a notable performance improvement across various visual robotic tasks. 

SWIM [444] advocates for the use of human videos in training a world model due to the availability of large-scale human-centric data. However, acknowledging the substantial gap between human and robot data, SWIM addresses this disparity by grounding actions in visual affordance maps. This approach involves inferring target poses based on the affordance maps, facilitating an effective transfer of knowledge from human data to enhance robot control. 

Iso-Dream [445] introduces two key enhancements to the Dreamer framework. The first enhancement focuses on optimizing inverse dynamics by decoupling controllable and noncontrollable dynamics. The second enhancement involves optimizing agent behavior based on the decoupled latent imaginations. This approach is particularly advantageous, as the noncontrollable state transition branch can be rolled out independently of actions, yielding benefits for long-horizon decision-making processes. 

Transformer-based World Model (TWM) [58] shares the same motivation as Dreamer but adopts a different approach by constructing a world model based on the Transformer-XL architecture [446]. This Transformer-based world model trains a model-free agent in latent imagination by generating new trajectories. Additionally, TWM suggests a modification to the balanced KL divergence loss from DreamerV2 and introduces a novel thresholded entropy loss tailored for the advantage actor-critic framework. 

SceneScript [447] introduces a set of structured language commands that can define an entire scene, specifying the layout and objects. This language-based scene representation distinguishes itself from previous methods—such as meshes, voxel grids, point clouds, or radiance fields—by generating scenes in an autoregressive, token-based fashion. It achieves competitive results against state-of-the-art methods in layout estimation and object detection. 

_3) Components of VLA: Imitation Learning:_ BeT [448], an imitation learning variant of the Trajectory Transformer, addresses the noisy and multimodal nature of non-expert human demonstration data by using k-means-based action discretization coupled with continuous action correction. C-BeT [449] extends BeT by adding a target frame or demonstration as the goal specification. VQ-BeT [450] further improves 

45 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

BeT by incorporating vector quantization instead of k-means, enabling better modeling of long-range actions. 

_4) Subsequent Surveys on VLA:_ Since the initial release of this survey was made public, the field of embodied AI has experienced a proliferation of VLA models, leading to the emergence of several related surveys [451], [452], [453], [454], [455], [456], [457], [458], [459], [460], [461]. 

_5) Latest Developments of VLA:_ LLaRA [462] introduces a data-centric method that uses a Vision-Language Model to automatically relabel existing robot demonstration videos with rich, descriptive language, significantly boosting the performance of downstream vision-language policies. 

_π_ 0 [118] undergoes further enhancements, including FAST [463] and _π_ 0 _._ 5 [464]. FAST is a novel robot action tokenization method designed to prioritize dexterous skills. _π_ 0 _._ 5 pushes the boundaries of in-the-wild generalization by incorporating cotraining with diverse data sources. 

Mobility VLA [465] proposes a hierarchical policy that integrates the commonsense reasoning capabilities of VLMs with a topological-graph-based low-level navigation policy. 

While many VLAs focus primarily on robotic arms, recent advancements have extended their application to more complex embodiments, including humanoid and quadruped robots. 

## Humanoid Robot: 

- GR00T N1 [135] 

- Humanoid-VLA [466] 

- Quadruped Robot: 

- QUAR-VLA [467] 

- QUART-Online [468] 

- MoRE [469] 

## Dexterous Hand: 

- DexGraspVLA [470] 

- DexGrasp-VLA [471] 

## Autonomous Vehicle: 

- Alpamayo-R1 [472] 

- CoVLA [473] 

- DriveVLA-W0 [474] 

- EMMA [475] 

Additionally, some VLAs are designed to function as virtual assistants capable of taking actions within operating systems, video games, and other environments. Notable examples include: 

- CombatVLA [476] 

- JARVIS-VLA [477] 

“robotics”. This pipeline yielded approximately 400 VLArelated papers. Acknowledging the potential for automated errors, we welcome feedback and requests for corrections regarding the included data. 

Abbreviations of institutes appearing in Figure 9: 

- **AI2** : Allen Institute for AI 

- **AIBD** : Advanced Institute of Big Data 

- **ANU** : Australian National University 

- **AgiBot** : AgiBot Research 

- **Alexandria Univ.** : Alexandria University 

- **Alibaba** : Alibaba Group, DAMO Academy 

- **Anyverse** : Anyverse Intelligence 

- **BAAI** : Beijing Academy of Artificial Intelligence 

- **BACFBC** : Innovation Center for Future Blockchain and Privacy Computing, Beijing 

- **BIGAI** : State Key Lab of General Artificial Intelligence 

- **BIT** : Beijing Institute of Technology 

- **BJUT** : Beijing University of Technology 

- **BKLSISMI** : Beijing Key Laboratory of Super Intelligent Security of Multi-Modal Information 

- **BNU** : Beijing Normal University 

- **BUAA** : Beihang University 

- **BUPT** : Beijing University of Posts and Telecommunications 

- **Bosch** : Bosch Center for Artificial Intelligence, Bosch Corporate Research, Bosch Mobility Solutions, Bosch Research 

- **Bretagne** : Bretagne INP - ENIB 

- **ByteDance** : ByteDance Research, ByteDance Seed 

- **CAS** : Chinese Academy of Sciences 

- **CAU** : Clark Atlanta University 

- **CMU** : Carnegie Mellon University 

- **CNRS** : CNRS IRL 2010 CROSSING 

- **CSU** : Central South University 

- **CUHK** : The Chinese University of Hong Kong 

- **CUHK(SZ)** : The Chinese University of Hong Kong (Shenzhen) 

- **CWRU** : Case Western Reserve University 

- **Caltech** : California Institute of Technology 

- **Cambridge** : Cambridge University 

- **China Mobile** : China Mobile Information Technology Co., Ltd., 

- **China Telecom** : China Telecom 

- **CityU** : City University of Hong Kong 

- **Cognitive AI** : Cognitive AI Lab 

- **Columbia** : Columbia University 

- **DSO** : DSO National Laboratories 

- **DUT** : Dalian University of Technology 

We utilize various charts to visualize key aspects of VLA developments from 2020 to 2025, including Figure 9, Figure 10, Figure 11, and Figure 12. To supplement the VLAs discussed in the main text, we employed a hybrid approach combining automated scripting and manual searching to retrieve VLA-related papers published between January 2020 and December 2025. We queried the keywords “VLA”, “Visionlanguage-action”, and “Vision language action”, filtering false positives based on their relevance to “embodied AI” and 

- **Didi Chuxing** : Didi Chuxing 

- **Drexel** : Drexel University 

- **Duke** : Duke University 

- **ECNU** : East China Normal University 

- **EIT** : Eastern Institute of Technology 

- **EKUT** : University of T¨ubingen 

- **ENS** : Ecole<sup>´</sup> Normale Sup´erieure 

- **ER** : Everyday Robots 

- **ETH** : ETH Zurich 

46 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

- **EdUHK** : The Education University of Hong Kong 

- **Fudan** : Fudan University 

- **GDUT** : Guangdong University of Technology 

- **Gachon Univ.** : Gachon University 

- **Galaxea** : Galaxea AI 

- **Georgia Tech** : Georgia Institute of Technology 

- **Google** : Google, Google DeepMind, Robotics at Google, Google Research, Brain Team, Gemini Robotics Team 

- **HBUT** : Hebei University of Technology 

- **HIT** : Harbin Institute of Technology 

- **HIT(SZ)** : Harbin Institute of Technology (Shenzhen) 

- **HKU** : The University of Hong Kong 

- **HKUST** : Hong Kong University of Science and Technology 

- **HKUST(GZ)** : Hong Kong University of Science and Technology (Guangzhou) 

- **HUST** : Huazhong University of Science and Technology 

- **Hanyang Univ.** : Hanyang University 

- **Harvard** : Harvard University 

- **Horizon** : Horizon Robotics 

- **Huawei** : Huawei Technologies, Huawei Noah’s Ark Lab 

- **HuggingFace** : Hugging Face 

- **Hyundai** : Hyundai Motor Company 

- **IC** : Imperial College London 

- **IEIT** : IEIT SYSTEMS Co., Ltd. 

- **IIIT-H** : IIIT Hyderabad 

- **IIT** : Istituto Italiano di Tecnologia 

- **IMT** : IMT Atlantique 

- **Infinigence** : Infinigence AI 

- **JHU** : Johns Hopkins University 

- **JLU** : Jilin University 

- **KAIST** : KAIST AI 

- **KIT** : Karlsruhe Institute of Technology 

- **Kobe Univ.** : Kobe University 

- **Korea Univ.** : Korea University 

- **LZU** : Lanzhou University 

- **Lehigh Univ.** : Lehigh University 

- **LiAuto** : LiAuto Inc. 

- **LimX** : LimX Dynamics 

- **Logos** : Logos Robotics 

- **Lumina** : Lumina Group 

- **Lumos** : Lumos Robotics 

- **MBZUAI** : Mohamed bin Zayed University of Artificial Intelligence 

- **MEGVII** : MEGVII Technology 

- **MIPT** : IAI MIPT 

- **MIT** : Massachusetts Institute of Technology 

- **MMLab** : MMLab @ CUHK, MMLab @ HKU 

- **Macalester** : Macalester College 

- **Meta** : Meta AI, FAIR-MetaAI, Meta Reality Labs 

- **Microsoft** : Microsoft Research, Microsoft Research Asia, Microsoft Zurich 

- **Midea** : Midea Group 

- **Mila** : Mila — Quebec AI Institute 

- **Monash Univ.** : Monash University 

- **Moxin** : Moxin (Huzhou) Technology Co., Ltd. 

- **NAVER** : NAVER AI Lab 

- **NEU** : Northeastern University 

- **NJU** : Nanjing University 

- **NJUPT** : Nanjing University of Posts and Telecommunications 

- **NKU** : Nankai University 

- **NPU** : Northwestern Polytechnical University 

- **NTU** : Nanyang Technological University 

- **NUS** : National University of Singapore 

- **NVIDIA** : NVIDIA Research 

- **NWU** : Northwestern University 

- **NYU** : New York University 

- **NaUKMA** : National University of Kyiv-Mohyla Academy 

- **Noematrix** : Noematrix Intelligence 

- **OXE Team** : Open X-Embodiment Collaboration 

- **OpenHelix** : OpenHelix Team 

- **PCL** : Peng Cheng Laboratory 

- **PI** : Physical Intelligence 

- **PKU** : Peking University 

- **PSL** : PSL Research University 

- **Penn State** : Pennsylvania State University 

- **Pitt** : University of Pittsburgh 

- **PolyU** : The Hong Kong Polytechnic University 

- **Princeton** : Princeton University 

- **QMUL** : Queen Mary University of London 

- **Qi Zhi** : Shanghai Qi Zhi Institute, Shanghai Qizhi Institute 

- **Qualcomm** : Qualcomm AI Research 

- **RU** : Rutgers University 

- **RUC** : Renmin University of China 

- **SBU** : Stony Brook University 

- **SCUT** : South China University of Technology 

- **SH AI Lab** : Shanghai AI Laboratory 

- **SHU** : Shanghai University 

- **SII** : Shanghai Innovation Institute 

- **SJTU** : Shanghai Jiao Tong University 

- **SKKU** : Sungkyunkwan University 

- **SNU** : Seoul National University 

- **STU** : ShanghaiTech University 

- **SUST** : Southern University of Science and Technology 

- **SUTD** : Singapore University of Technology and Design 

- **SYSU** : Sun Yat-sen University 

- **SZU** : Shenzhen University 

- **Sea AI** : Sea AI Lab 

- **SenseTime** : SenseTime Research 

- **Siemens** : Siemens Corporation 

- **Simplexity** : Simplexity Robotics 

- **Sofia Univ.** : Sofia University “St. Kliment Ohridski” 

- **Sony** : Sony Interactive Entertainment, Sony Research 

- **Sorbonne Univ.** : Sorbonne University 

- **Spirit** : Spirit AI 

- **Stanford** : Stanford University 

- **Syracuse** : Syracuse University 

- **T-Stone** : T-Stone Robotics Institute 

- **TJU** : Tianjin University 

- **TUM** : Technical University of Munich 

- **Taiwan Univ.** : National Taiwan University 

- **Tencent** : Tencent Inc., Tencent Robotics X, Wechat AI 

- **Tongji** : Tongji University 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

47 

- **Toyota** : Toyota Research Institute 

- **Tsinghua** : Tsinghua University 

- **Turing** : Turing Inc. 

- _•_ **U of U** : University of Utah 

- **UATX** : The University of Austin at Texas 

- **UAlberta** : University of Alberta 

- **UArizona** : University of Arizona 

- **UArkansas** : University of Arkansas 

- **UBC** : The University of British Columbia 

- **UCAS** : University of Chinese Academy of Sciences 

- **UCB** : University of California, Berkeley 

- **UCL** : University College London 

- **UCLA** : University of California, Los Angeles 

- **UCSD** : University of California San Diego 

Xiaomi EV, Xiaomi Robotics 

   - **Yale** : Yale University 

   - **Yinwang** : Yinwang Intelligent Technology Co., Ltd. 

   - **Yuandao** : Yuandao AI 

   - **ZGCA** : Zhongguancun Academy 

   - **ZGCI** : Zhongguancun Institute of Artificial Intelligence 

   - **ZJU** : Zhejiang University 

   - **ZZU** : Zhengzhou University 

   - **ZhiCheng** : ZhiCheng AI 

   - **Zhongke Huiling** : Beijing Zhongke Huiling Robot Technology Co 

   - **iFlyTek** : iFlyTek Research and Development Group 

   - **mimic** : mimic robotics 

   - **valeo** : valeo.ai 

- **UCSI** : UCSI University 

- **UCSP** : Universidad Cat´olica San Pablo 

- **UChicago** : University of Chicago 

- **UESTC** : University of Electronic Science and Technology of China 

- **UIC** : University of Illinois Chicago 

- **UIUC** : University of Illinois Urbana-Champaign 

- **UM** : University of Macau 

- **UMD** : University of Maryland, College Park 

- **UMU** : Ume˚a University 

- **UNSW** : University of New South Wales 

- **UOsaka** : The University of Osaka 

- **UPenn** : University of Pennsylvania 

- **UQ** : University of Queensland 

- **USC** : University of Southern California 

- **USST** : University of Shanghai for Science and Technology 

- **USTC** : University of Science and Technology of China 

- **USYD** : The University of Sydney 

- **UT Austin** : The University of Texas at Austin 

- **UT Dallas** : University of Texas at Dallas 

- **UTN** : University of Technology Nuremberg 

- **UTS** : University of Technology Sydney 

- **UTokyo** : The University of Tokyo 

- **UW** : University of Washington 

- **UWarsaw** : University of Warsaw 

- **UW–Madison** : University of Wisconsin-Madison 

- **UdeM** : Universit´e de Montr´eal 

- **Uni Freiburg** : University of Freiburg 

- **UofT** : University of Toronto 

- **VT** : Virginia Tech 

- **VinUni** : VinUniversity 

- **WHU** : Wuhan University 

- **WMU** : Wenzhou Medical University 

- **Waseda** : Waseda University 

- **Westlake Univ.** : Westlake University 

- **X-Era** : X-Era AI Lab 

- **X-Humanoid** : Beijing Innovation Center of Humanoid Robotics 

- **XDU** : Xidian University 

- **XJTU** : Xi’an Jiaotong University 

- **XMU** : Xiamen University Malaysia 

- **XPeng** : XPeng Motors 

- **Xiaomi** : Beijing Xiaomi Robot Technology Co., Ltd., 

List of VLAs appearing in Figure 9: 

- 3D Diffuser Actor [478] 

- 3DS-VLA [479] 

- 4D-VLA [480] 

- A2C2 [481] 

- A3VLM [482] 

- ACG [483] 

- ACT [100] 

- Act3D [91] 

- ActDistill [484] 

- ActionFlow [485] 

- AdaMoE [486] 

- ADP [487] 

- AFI [488] 

- AgentWorld [489] 

- AINA [490] 

- Alpamayo-R1 [472] 

- AMS [491] 

- ANNIE [492] 

- AsyncVLA [493] 

- ATE [494] 

- AutoDrive-R2 [495] 

- AutoPrune [496] 

- AutoVLA [497] 

- AVA-VLA [498] 

- Avi [499] 

- BadVLA [500] 

- BayesVLA [501] 

- BC-Z [82] 

- Being-H0 [502] 

- Beyond Success [503] 

- Bi-VLA [504] 

- Bi-VLA 2025 [505] 

- BridgeVLA [506] 

- BYOVLA [507] 

- CCoL [508] 

- ChatVLA-2 [509] 

- CLAW [510] 

- CLIPort [29] 

- CLIP-RT [511] 

- ClutterDexGrasp [512] 

- CoC-VLA [513] 

- CogACT [122] 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

48 

- CogVLA [514] _•_ FAST [463] 

- _•_ ColaVLA [515] _•_ FastDriveVLA [563] _•_ CombatVLA [476] _•_ Fast-in-Slow [564] _•_ ConRFT [516] _•_ FLARE [565] _•_ ControlVLA [517] _•_ FLOWER [566] _•_ Control Your Robot [518] _•_ FlowVLA [567] _•_ CoReVLA [519] _•_ ForceVLA [568] _•_ CoT4AD [520] _•_ FORGE-Tree [569] _•_ CoT-VLA [79] _•_ FPC-VLA [570] _•_ Counterfactual VLA [521] _•_ FreezeVLA [571] _•_ CoVLA [473] _•_ FTM, FLA [572] _•_ CRISP [522] _•_ G0 [573] _•_ CycleManip [523] _•_ Gato [574] _•_ DEAS [524] _•_ GEN-0 [575] _•_ DeeAD [525] _•_ Genie Envisioner [137] _•_ DeepThinkVLA [526] _•_ GeoAware-VLA [576] _•_ DeeR-VLA [104] _•_ GeRM [577] _•_ Dejavu [527] _•_ GEVRM [578] _•_ DepthVLA [528] _•_ GF-VLA [579] _•_ Dexbotic [529] _•_ GLaD [580] _•_ DexGrasp-VLA [471] _•_ GLUESTICK [581] _•_ DexGraspVLA [470] _•_ GR00T N1 [135] _•_ DexVLA [123] _•_ GR 1.5 [582] _•_ Diffusion Policy [530] _•_ GRAPE [583] _•_ Diffusion-VLA [531] _•_ GraphCoT-VLA [584] _•_ DiffVLA [532] _•_ GraspVLA [585] _•_ DIPOLE [533] _•_ GraSP-VLA [586] _•_ DLR [534] _•_ GR-Dexter [587] _•_ Don’t Blind Your VLA [535] _•_ GR-RL [588] _•_ DP3 [108] _•_ HAMSTER [589] _•_ DP-VLA [536] _•_ Helix [590] _•_ DreamTacVLA [537] _•_ HiF-VLA [591] _•_ DreamVLA [538] _•_ HiMoE-VLA [592] _•_ Dream-VLA [539] _•_ Hi-ORS [593] _•_ DriveVLA-W0 [474] _•_ Hi Robot [594] _•_ DualVLA [540] _•_ HiRT [595] _•_ DuoCore-FS [541] _•_ Hiveformer [89] _•_ dVLA [542] _•_ HULC [84] _•_ EBT-Policy [543] _•_ HULC++ [85] _•_ ECoT [544] _•_ Humanoid-VLA [466] _•_ ECoT-Lite [545] _•_ HumanVLA [596] _•_ EfficientVLA [546] _•_ HybridVLA [124] _•_ Ego-PM [547] _•_ iFlyBot-VLA [597] _•_ EmbodiedCoder [548] _•_ ImaginationPolicy [598] _•_ Embodied-SlotSSM [549] _•_ Impromptu VLA [599] _•_ EMMA [550] _•_ INSIGHT [600] _•_ Emma-X [551] _•_ Instruct2Act [105] _•_ EndoVLA [552] _•_ InstructVLA [601] _•_ EO-1 [553] _•_ IntentionVLA [602] _•_ ERIQ [554] _•_ InteractGen [603] _•_ ERMV [555] _•_ Interactive Language [88] _•_ ET-VLA [556] _•_ InternVLA-M1 [604] _•_ EveryDayVLA [557] _•_ iRe-VLA [605] _•_ Evo-1 [558] _•_ IRL-VLA [606] _•_ ExpReS-VLA [559] _•_ JARVIS-VLA [477] _•_ EyeVLA [560] _•_ KV-Efficient VLA [607] _•_ F1 [561] _•_ Language costs [87] _•_ FailSafe [562] _•_ LAPA [125] 

   - LAPA [125] 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

49 

- LatBot [608] 

- _•_ LAWM [609] _•_ LCDrive [610] _•_ LITEN [611] _•_ Lite VLA [612] _•_ LLaRA [462] _•_ LoHoVLA [613] _•_ LoLA [614] _•_ Long-VLA [615] _•_ LVP [616] _•_ ManiAgent [617] _•_ Mantis [618] _•_ ManualVLA [619] _•_ MAP-VLA [620] _• E_ 0 [621] _•_ MCIL [84] _•_ MDT [622] _•_ MemER [623] _•_ MemoryVLA [624] _•_ MetaVLA [625] _•_ MG-Select [626] _•_ MimicDreamer [627] _•_ MindDrive [628] _•_ Mind to Hand [629] _•_ MiVLA [630] _•_ MLA [631] _•_ MM-ACT [632] _•_ Mobility VLA [465] _•_ MoH [633] _•_ MoIRA [634] _•_ MoMaGen [635] _•_ MoManipVLA [636] _•_ MonoDream [637] _•_ MOO [638] _•_ MoRE [639] _•_ MotionTrans [640] _•_ MoTo [641] _•_ MotoVLA [642] _•_ Motus [643] _•_ Moxin-VLA [644] _•_ MT-ACT [101] _•_ MUVLA [645] _•_ NaVILA [646] 

- NICE [647] 

- _•_ NitroGen [648] _•_ NORA-1.5 [136] _•_ Oat-VLA [649] _•_ OBEYED-VLA [650] _•_ OccLLaMA [651] _•_ OccVLA [652] _•_ Octo [110] _•_ OC-VLA [653] _•_ OmniJARVIS [654] _•_ OmniReason [655] _•_ OmniSAT [656] _•_ OmniVLA [657] _•_ OneTwoVLA [658] _•_ OpenHA [659] 

- OpenVLA [660] 

- _•_ OpenVLA-OFT [116] _•_ OTTER [661] _•_ PerAct [90] _•_ PhysBrain [662] _•_ PhysiAgent [663] _• π_ 0 [118] _• π_ 0 _._ 5 [464] _• π_ 0<sup>_∗_</sup> _._ 6<sup>[19]</sup> _• π_ RL [664] _•_ PIVOT [134] _•_ PixelVLA [665] _•_ PLA [666] _•_ Point-VLA [667] _•_ PosA-VLA [668] _•_ Prophet [669] _•_ QAIL+QBC [670] _•_ QDepth-VLA [671] _•_ Q-Transformer [672] _•_ QUART-Online [673] _•_ QUAR-VLA [467] _•_ R2R2R [674] _•_ RDT-1B [675] _•_ Reasoning-VLA [676] _•_ ReflectDrive [677] _•_ REGENT [678] _•_ ReKep [679] _•_ RETAIN [680] _•_ RetoVLA [681] _•_ ReVLA [682] _•_ RICL [683] _•_ RoboCat [684] _•_ RoboChemist [685] _•_ RoboDual [686] _•_ RoboFlamingo [687] _•_ RoboMamba [119] _•_ RoboMatrix [688] _•_ RoboMonkey [81] _•_ RoboNeuron [689] _•_ RoboNurse-VLA [690] _•_ RoboOmni [691] _•_ RoboOS-NeXT [692] _•_ RoboPoint [693] _•_ RoboTAP [133] _•_ Robotic Assistant [694] _•_ RoboUniView [103] _•_ RoboVLMs [695] _•_ RobustVLA [696] _•_ RoVer [697] 

- RPD [698] 

- RS-CL [699] 

- RT-1 [97] 

- RT-2 [700] 

- _•_ RT-A [701] 

- RT-H [702] 

- RT-RAS [703] 

- _•_ RT-Trajectory [704] 

- RT-X [705] 

50 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 

- RVT [92] _•_ V-GPS [80] 

- _•_ RVT-2 [706] _•_ Video2Act [755] _•_ RynnVLA-001 [707] _•_ VideoVLA [756] _•_ RynnVLA-002 [708] _•_ VIMA [130] _•_ SafeVLA [709] _•_ VINE [757] _•_ SARA-RT [710] _•_ ViVLA [758] _•_ ScaleDP [711] _•_ VLA-0 [759] _•_ SC-VLA [712] _•_ VLA-4D [760] _•_ SEAL [713] _•_ VLA-Adapter [761] _•_ SeeDo [714] _•_ VLA-AN [762] _•_ SeqVLA [715] _•_ VLA-Cache [763] _•_ ShowUI [716] _•_ VLA-Fool [764] _•_ Sigma [717] _•_ VLA-OS [765] _•_ SimpleVLA-RL [718] _•_ VLA-Pilot [766] _•_ SITCOM [719] _•_ VLA-Pruner [767] _•_ SmolVLA [720] _•_ VLAPS [768] _•_ SOLAMI [721] _•_ VLA-R [769] _•_ Spatial Forcing [722] _•_ VLA-R1 [770] _•_ SpatialVLA [120] _•_ VLA-RAIL [771] _•_ SpecPrune-VLA [723] _•_ VLA-RFT [772] _•_ Spec-VLA [724] _•_ VLAS [773] _•_ SQAP-VLA [725] _•_ Vlaser [774] _•_ SSM-VLA [726] _•_ VLASH [775] _•_ STARE-VLA [727] _•_ VLM2VLA [776] _•_ StereoVLA [728] _•_ VLMimic [777] _•_ STORM [729] _•_ VoxPoser [778] _•_ SUDD [109] _•_ VST [779] _•_ SurgWorld [730] _•_ WAM-Flow [780] _•_ SwiftVLA [731] _•_ WholeBodyVLA _•_ TabVLA [732] _•_ WMPO [782] _•_ TACO [733] _•_ WorldVLA [126] _•_ TacRefineNet [734] _•_ WristWorld [783] _•_ Tactile-VLA [735] _•_ X-Humanoid [784] _•_ TA-VLA [736] _•_ XR-1 [785] _•_ ThinkAct [737] _•_ X-VLA [786] _•_ ThinkBot [738] _•_ TinyVLA [121] _6) Beyond VLA: •_ TraceVLA [117] standard VLA architectures _•_ TrackVLA [739] _•_ **VLA + World** _•_ TrajBooster [740] with world models. _•_ Transporter Networks [438] **–** WorldVLA [126] 

- _•_ TriVLA [741] **–** UniVLA [127] 

- _•_ TVVE [742] **–** NORA-1.5 [136] 

- _•_ UD-VLA [743] **–** RynnVLA-002 

- _•_ UnderwaterVLA [744] **–** Motus [643] 

- _•_ UniCoD [745] _•_ **PLA, MLA:** 

- _•_ Unified-IO 2 [746] beyond vision. 

- _•_ Uni-NaVid [747] **–** Perception-Language-Action 

- _•_ UniPi [86] [666] 

- _•_ UniUGP [748] **–** Multisensory 

- _•_ UniVLA [127] _•_ UPA-RFAS [749] _•_ **VAM:** Video-Action _•_ UP-VLA [750] tics and dynamics _•_ UrbanVLA [751] more efficient _•_ USIM & U0 [752] **–** mimic-video _•_ UWM [753] _•_ VAM [754] 

   - VST [779] 

   - _•_ WAM-Flow [780] _•_ WholeBodyVLA [781] _•_ WMPO [782] 

   - _6) Beyond VLA:_ Recent research has expanded beyond 

   - standard VLA architectures in several key directions: 

   - **VLA + World Model:** Architectures that unify VLAs with world models. 

      - WorldVLA [126] 

      - NORA-1.5 [136] 

      - RynnVLA-002 [708] 

      - **–** Motus [643] 

   - **PLA, MLA:** Models incorporating perception modalities beyond vision. 

      - Perception-Language-Action framework (PLA) [666] 

      - Multisensory Language–Action model (MLA) [631] 

   - **VAM:** Video-Action Models that jointly capture semantics and dynamics during video pretraining, enabling more efficient post-training for low-level robot control. 

      - mimic-video (VAM) [754] 

- VER [131] 

51 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 


Fig. 9. Timeline of VLA models from 2020 to 2025. Bracketed numbers indicate the publication count for the corresponding year or institute. 

52 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 


Fig. 10. Visualization of the VLA research landscape. 

53 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 


Fig. 11. Quantitative analysis of VLA development trends. 

54 

IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS 


Fig. 12. VLA research output and impact by institution. 

