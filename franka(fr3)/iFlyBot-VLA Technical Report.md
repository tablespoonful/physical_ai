---
title: "iFlyBot-VLA Technical Report"
date: "2025-11-01"
authors: "Yuan Zhang; Chenyu Xue; Wenjie Xu; Chao Ji; Jiajia wu; Jia Pan"
url: https://arxiv.org/abs/2511.01914
pdf: https://arxiv.org/pdf/2511.01914
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.01914)** / [論文ページ](https://arxiv.org/abs/2511.01914)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**iFlyBot-VLA Technical Report** 


# **Yuan Zhang**<sup>1</sup><sup>_,†_</sup> , **Chenyu Xue**<sup>1</sup><sup>_,†_</sup> , **Wenjie Xu**<sup>1</sup><sup>_,†_</sup> , **Chao Ji**<sup>2</sup> , **Jiajia wu**<sup>1</sup> , **Jia Pan**<sup>1</sup><sup>_,∗_</sup> 

1iFlyTek Reasearch and Development Group, 2LindenBot 

# **Abstract** 

We introduce **iFlyBot-VLA** , a large-scale Vision-Language-Action (VLA) model trained under a novel framework. The main contributions are listed as follows: (1) a **latent action model** thoroughly trained on large-scale human and robotic manipulation videos; (2) a **dual-level action representation framework** that jointly supervises both the Vision-Language Model (VLM) and the action expert during training; (3) a **mixed training strategy** that combines robot trajectory data with general QA and spatial QA datasets, effectively enhancing the 3D perceptual and reasoning capabilities of the VLM backbone. Specifically, the VLM is trained to predict two complementary forms of actions: **latent actions** , derived from our latent action model pretrained on cross-embodiment manipulation data, which capture implicit high-level intentions; and **structured discrete action tokens** , obtained through frequency-domain transformations of continuous control signals, which encode explicit low-level dynamics. This dual supervision aligns the representation spaces of language, vision, and action, enabling the VLM to directly contribute to action generation. Experimental results on the **LIBERO Franka** benchmark demonstrate the superiority of our framework, while real-world evaluations further show that iFlyBot-VLA achieves competitive success rates across diverse and challenging manipulation tasks. Furthermore, we plan to **open-source a portion of our self-constructed dataset** to support future research in the community. 

**Date:** November 5, 2025 

**Correspondence:** `chaoji@iflytek.com, yuanzhang10@iflytek.com` **Project Page:** `https://xuwenjie401.github.io/iFlyBot-VLA.github.io/` 

# **1 Introduction** 

In recent years, with the rapid advancement of Vision-Language Models (VLMs)[1, 4], researchers have begun to envision leveraging their powerful perceptual and reasoning capabilities to accomplish long-horizon and complex robotic manipulation tasks. However, while the autoregressive paradigm has demonstrated impressive performance in complex scene understanding and perception, it faces inherent limitations when dealing with tasks that require precise, continuous control signals—such as predicting joint angles or end-effector poses. Compared with continuous modeling approaches like diffusion or flow-based methods, autoregressive models struggle to generate fine-grained, numerically accurate outputs. 

As a result, most contemporary Vision-Language-Action (VLA) frameworks[6, 10, 12, 23, 29, 39, 40, 49] adopt a hybrid design that integrates a VLM[5, 11] for perception and a diffusion or flow-based action expert for motion generation. This combination provides strong input–output compatibility and leverages the complementary strengths of both components. Nonetheless, a key challenge remains: how to design a training strategy that maximally preserves the VLM’s general perception and reasoning capabilities while enabling the diffusion policy to produce precise, smooth actions. 

† denotes co-first author, * denotes the corresponding author 

On the other hand, imitation learning remains the foundation of most current VLA systems, which rely heavily on high-quality teleoperation datasets [16, 17, 24–28, 34, 37, 46, 48] collected via specialized interfaces. Although recent works have explored alternative data sources such as VR teleoperation [3, 13, 18, 21, 41], handheld devices [14], and human demonstration datasets [15, 19, 20, 22, 33, 44, 45], teleoperated data with consistent morphologies still holds distinct advantages in precision and consistency. While large-scale and diverse manipulation data are crucial for improving generalization across tasks and embodiments, one motivation for integrating VLMs into VLAs is to leverage their broad perceptual and semantic generalization. However, when trained solely on manipulation data, the VLM’s language and reasoning abilities degrade rapidly. Thus, an open challenge remains: how to balance multimodal training so that both the VLM and the action expert can co-evolve—maintaining perception, language understanding, and action generation throughout training. 

Early Vision-Language-Action (VLA) research explored learning manipulation policies via autoregressive Vision-Language Models (VLMs), facing the challenge of discretizing continuous action sequences. OpenVLA [29] normalized continuous actions into 256 discrete bins, but suffered from precision and scalability issues as action chunks grew. FAST [7] addressed this by applying a Discrete Cosine Transform (DCT) [2]–based compression followed by Byte Pair Encoding (BPE) [38], significantly improving learning efficiency and action accuracy. 

Recent approaches learn manipulation knowledge from large-scale videos through latent action representations. LAPA [47] uses a VQ-VAE [43] to discretize latent action increments in unlabeled videos, training a VLA to predict these and fine-tuning on limited robot data for real-world control. UniVLA [9] extends this with a two-stage task-centric framework, introducing task-agnostic and task-specific codebooks for better noise filtering and cross-domain generalization. These studies demonstrate that discretized latent action spaces effectively bridge visual–language perception and fine-grained action generation for scalable manipulation learning. 

In this report, we present **iFlyBot-VLA** , a framework trained in multiple stages using diverse types of data. **iFlyBot-VLA** takes natural language task instructions, multi-view RGB images of the environment, and the robot’s proprioceptive state data as inputs, and outputs _action chunks_ to control a dual-arm robot in an end-to-end manner. Specifically, iFlyBot-VLA builds upon a pretrained Vision-Language Model (VLM) and predicts action chunks through a **flow-matching** mechanism. 

We observe that a randomly initialized flow-based action expert, when trained end-to-end solely on robot trajectory data, can easily degrade the general perceptual ability of the VLM backbone. However, this backbone capability is crucial for the policy’s generalization performance. 

To address the aforementioned challenges, we have made the following contributions: 

- We collect and organize a large-scale, high-quality dataset consisting of single-arm, dual-arm, and human teleoperation videos to train a **latent action model** , thereby obtaining high-level and generalizable latent action representations. 

- Based on the latent action representations and explicit supervision of structured discrete actions, we construct a **dual-level action representation framework** , enabling the joint training of the VLM and the action expert. 

- To preserve the VLM’s general understanding capability and further enhance its embodiment-related spatial perception, we build extensive **general vision-language QA** and **spatial reasoning QA** datasets. These are carefully mixed with robot manipulation data using an optimized ratio, improving the policy’s generalization performance. 

- We design comprehensive comparative experiments on both the **LIBERO benchmark** and **real-world robotic platforms** . The results demonstrate that our proposed framework achieves superior performance across diverse tasks in both simulation and real environments. 

- We will **open-source** our code, along with portions of our teleoperation and VQA datasets, to contribute to the research community. 

2 

# **2 Overview** 

Figure 1 provides an overview of the iFlyBot-VLA model and its overall training pipeline. In this framework, we first construct a manipulation dataset of robot trajectories, which is a weighted combination of three major components: self-collected teleoperation dataset by iFLYTEK, a subset of OXE dataset [35],and a subset of AgiBot-World dataset [8]. 

During the pre-training phase, iFlyBot-VLA also leverages a portion of pure text-based question-answering data to enhance the model’s spatial reasoning and object perception capabilities. This text-only dataset is internally constructed by iFLYTEK and focuses on spatial understanding tasks. 


**Figure 1** The architecture of iFlyBot-VLA consists primarily of a language transformer backbone and an action expert network. The model generates executable robot actions through a combination of explicit and implicit planning. The key–value (KV) cache from the VLM component is passed to the downstream action expert, while the FAST Action Token—which corresponds to the implicit planning process—is not forwarded to the Action Expert 

As mentioned in the Introduction, in order to learn high-level latent action representations from a broader range of manipulation videos—thereby benefiting the learning of downstream numerical action chunks—we first train a more comprehensive codebook via the VQ-VAE pipeline before initiating the VLA training. This codebook serves as the foundation for providing latent action tokens that guide subsequent learning. Our overall training framework is divided into three stages: 

1) **Stage I: Latent Action Training.** We first train a **latent action model** using large-scale, carefully curated human and robotic manipulation videos. Through a VQ-VAE–based architecture, the model learns to extract high-level and generalizable latent action representations from pairs of consecutive frames, providing rich supervision signals that benefit subsequent VLA training. 

2) **Stage II: Foundational Pre-training.** The goal of this stage is to build a foundational model with broad spatial perception, object recognition, and generalization capabilities, without specializing in any particular downstream task. The resulting model can follow natural-language commands, execute instruction-driven actions, and recognize both object categories and their spatial relations. 

3) **Stage III: Task-specific Post-training.** For more complex and dexterous operations, we conduct a secondstage post-training process using high-quality, self-collected datasets to adapt the model to specific downstream tasks. iFlyBot-VLA employs large-scale, high-fidelity post-training strategies for sophisticated robotic skills such as cloth folding, manipulation in cluttered scenes, and grasp-and-place tasks involving irregular objects. This stage relies on larger datasets to achieve high-precision control and robust adaptability. 

The next chapter provides a detailed explanation of the iFlyBot-VLA model architecture. The model builds upon the Qwen2.5-VL (3B) [4] vision-language backbone. By further training on the hybrid dataset—comprising both spatial question-answering data and robot manipulation data—the vision-language model is enhanced to understand and generate action-related responses. 

3 

To transform Qwen2.5-VL into a vision-language-action (VLA) model capable of generating continuous action trajectories, a downstream Action Expert Module is introduced. This module is based on Flow-Matching Diffusion Transformer [36] architecture, which performs denoising via flow-matching techniques using the KV-features extracted from the vision-language model. The design and implementation of this component are described in detail in the following section. 

It is worth noting that iFlyBot-VLA adopts Qwen2.5-VL primarily due to its superior performance and deployment flexibility. In principle, the same framework can be adapted to any vision-language backbone with minimal modification. 

# **3 iFlyBot-VLA Model** 

The architecture of iFlyBot-VLA consists primarily of a language transformer backbone and an action expert network. The model generates executable robot actions through a combination of explicit and implicit planning. The key–value (KV) cache from the VLM component is passed to the downstream action expert, while the FAST Action Token—which corresponds to the implicit planning process—is not forwarded to the Action Expert. 

The **iFlyBot-VLA** model is an end-to-end **Vision-Language-Action (VLA)** model denoted as _πθ_ . It controls a dual-arm robot by generating an **action block** of length _k_ , represented as _at_ = _at_ : _t_ + _k_ . The generation of this action block primarily depends on three inputs: the language instruction _l_ , the visual observation _ot_ obtained from sensors, and the current robot state _st_ , formulated as 1: 


The model mainly consists of a language transformer backbone and an action expert network, which together generate executable robot actions _at_ through explicit and implicit planning. The supervision for latent action tokens is provided by an expert network based on the visual changes across future frames, while the discretized action tokens are obtained by an action token encoder that encodes a sliding window of future actions. In practice, we assign these action tokens to the unused token IDs within the VLM tokenizer to ensure seamless integration with the language modeling framework. 

## **3.1 latent action model** 

To learn latent actions in a self-supervised manner, we train a **latent action model** with an encoder–decoder structure, which serves as the expert network, as shown in Fig. 2. 

The encoder consists of both spatial and temporal Transformers, taking as input a set of current image frames _ot_ and future frames _ot_ + _k_ spaced by _k_ , and outputs the latent action _ct_ . To ensure sufficient motion variation between frames, the interval between the two frames is fixed at 1 second, and the corresponding frame gap _k_ is determined according to the frame rate of each dataset. 

The decoder, which contains only a spatial Transformer, takes the latent action _ct_ and the image frame _ot_ as inputs to reconstruct the future frame _ot_ + _H_ . 

The latent action quantization model is trained based on the **VQ-VAE objective** , discretizing the continuous encoded features by retrieving the nearest quantized representation from the codebook, which facilitates the VLM’s learning of _zt_ by 2: 


The size of the codebook _|C|_ is set to 32, and 8 discrete codes are retrieved at each step. During reproduction of the VQ-VAE training, we encountered a gradient collapse issue. To address this, we adopt the **NSVQ algorithm** [42], which replaces the original VQ’s Straight-Through Estimator (STE) with a noise-based approximation. Specifically, it substitutes the quantization error between the discrete output and the encoder output with the product of this error and a unit noise vector, thereby preventing gradient collapse by 3: 


4 

where _w_ follows a standard Gaussian distribution. 

Additionally, during the decoding process, we apply a **stop-gradient** operation to the current frame, forcing the model to rely on the latent action _ct_ for decoding the future frame. The supervision loss is defined as the mean squared error (MSE) between the reconstructed and target images. 


**Figure 2** Architecture of the latent action token encoding expert network 

## **3.2 Discrete Action Token Encoding** 

The discrete action tokens in the iFlyBot-VLA model are encoded by an _action token encoder_ based on the action window _at_ composed of multiple future action frames. Specifically, we adopt the _Fast Action Token_ method [7] to encode _at_ . 

It is worth noting that, on one hand, the discrete action tokens share a high degree of similarity with the downstream action outputs generated by the action expert, which may lead to overfitting if their corresponding features are directly provided to the expert, thereby reducing the model’s generalization ability. On the other hand, the number of discrete action tokens is relatively large, which can significantly increase inference time and reduce efficiency when generating them in real-time. 

Therefore, in this work, the discrete action tokens are used **only to supervise the VLM (Vision-Language Model) component** to implicitly encourage the model to learn action-related semantics and to assist in implicit action planning. During both training and inference, the corresponding features of the discrete action tokens are not utilized. In contrast, the **latent action tokens** are constructed from a more compact latent action space, whose features are used for downstream action planning. This design enhances the quality of robot action generation while maintaining high inference efficiency. 

## **3.3 VLA Model Architecture** 

The iFlyBot-VLA model _πθ_ consists of two main components: (1) a **Transformer-based vision-language backbone** for embedding multimodal states, and (2) a **Diffusion Transformer expert network** for generating continuous robot actions. 

In the language Transformer backbone, we adopt a standard _decoder-only_ vision-language model (VLM) framework. The image encoder embeds visual observations from the robot’s onboard cameras into the same feature space as the language tokens. In addition to conventional vision-language inputs, iFlyBot-VLA introduces **robot-specific inputs** , namely the robot’s proprioceptive state. In practice, we insert a placeholder token for the state input, which is later replaced by the feature obtained from passing the actual state values through a fully connected layer. During training, the VLM is supervised to predict two sequences: a set of _latent action tokens_ and a set of _discrete action tokens_ . The latent action tokens assist in the planning and generation of the action block _at_ , while the discrete tokens guide the VLM in learning spatially grounded, action-related semantics. 

The downstream action expert network is a **Diffusion Transformer** . During inference, the VLM outputs KV caches at every layer, which are fed into the action expert to provide necessary visual-linguistic context and planning information. Only the KV caches corresponding to the _latent action tokens_ are retained, while those 

5 

related to the discrete action tokens are excluded. The KV caches of latent action tokens are preserved because they provide a highly compressed representation of actions, effectively supporting downstream planning. In contrast, discrete action tokens are excluded since their large quantity would slow down inference and reduce overall efficiency. 

For modeling continuous actions, iFlyBot-VLA adopts the **flow-matching** approach [30, 32] to represent continuous action distributions. This method is particularly suitable for high-frequency manipulation tasks. In implementation, the downstream expert network takes as input the robot state, the current timestep, and a **noised action** composed of the target action window, timestep, and Gaussian noise. Together with the expert’s features, the model predicts the denoising direction from the noised action toward the true action. The corresponding loss is defined as: 


Here, _t_ denotes the robot’s timestep and _τ ∈_ [0 _,_ 1] represents the flow-matching time variable. During training, Gaussian noise _ϵ ∼N_ (0 _,_ 1) is sampled, and the noised action is constructed as _A_<sup>_τ_</sup> _t_<sup>=</sup><sup>_τAt_+ (1</sup><sup>_−τ_)</sup><sup>_ϵ_.The</sup> network output _πθ_ ( _A_<sup>_τ_</sup> _t_<sup>_, l, ot, st_)istrainedtomatchthedenoisingvectorfield</sup><sup>_π_(</sup><sup>_Aτ_</sup> _t_<sup>_|At_) =</sup><sup>_ϵ −At_.Theaction</sup> expert module adopts a **fully bidirectional attention mask** , ensuring that all action tokens within the same window can attend to each other, allowing parallel denoising across the action window. This design both promotes temporal continuity between actions and improves generation efficiency. During training, the flow-matching timestep _τ_ is sampled from a Beta distribution that assigns higher weights to smaller (noisier) timesteps. 

## **3.4 Inference Process** 

During inference, iFlyBot-VLA generates actions starting from random Gaussian noise _A_<sup>0</sup> _t_<sup>_∼N_(0</sup><sup>_,_1)and</sup> integrates the learned vector field from _τ_ = 0 to _τ_ = 1 to obtain the final action sequence. Specifically, a discrete forward Euler integration is performed as 5: 


where _σ_ is the integration step size. In practice, a five-step integration is used, i.e., _σ_ = 0 _._ 2. During inference, the VLM’s KV cache needs to be computed only once, regardless of the number of integration steps, ensuring efficient and stable action generation. 

# **4 Training Strategy** 

## **4.1 Data Preparation** 

Our latent action network does not rely on textual inputs, allowing for more diverse data usage. On one hand, we incorporate large-scale human manipulation datasets. The inclusion of these datasets enhances the generalization ability of the model, enabling it to handle complex manipulation scenarios and diverse tasks. On the other hand, the latent action network _F_ is trained using both single-arm and dual-arm robotic datasets. These datasets correspond to various robotic operation settings and motion types, enabling the expert model to effectively capture action dynamics across both single-arm and dual-arm robotic contexts. 

Our latent action network does incorporate large-scale human manipulation datasets including HoloAssist [45], Ego4D [20], EgoDex [22], HOI4D [33], Something-Something V2 [19], and EgoVid [44], and using both single-arm and dual-arm robotic datasets, including OXE [35], AgiBot [8], RoboMind [46], and Galaxea [24], as show in fig 3. 

During the training of iFlyBot-VLA, the datasets used include: (1) an internally constructed **VQA dataset focuses on spatial understanding** developed by iFLYTEK, (2) a subset of the publicly available **OXE** [35] dataset containing a wide range of robotic manipulation tasks under diverse scenarios and robot embodiments, (3) a subset of the publicly released **AgiBot-World** [8] dataset from AgiBot featuring dual-arm robotic operations, and (4) a **self-collected dataset** from iFLYTEK, which includes various dual-arm manipulation tasks such 

6 


**Figure 3** The data used for training the latent action token encoding expert network 

as tabletop pick-and-place, cloth folding, and grasping irregular or soft objects across multiple real-world environments. 

The self-collected iFLYTEK dataset was gathered using **26 dual-arm robots** configured in two different setups. It contains three primary categories of tasks: 

- **Cloth Folding:** Includes five types of T-shirts and three types of shorts. For each type, 190 trajectories were collected, each averaging 4.5 minutes, totaling approximately 110 hours of data. 

- **General Pick and Place:** Includes 30 categories of grasped objects, with 400 trajectories per category, each averaging 27 seconds, totaling around 90 hours of data. 

- **Long-Horizon Parcel Sorting** : The goal is to handle flexible packages of varying sizes and flip them so that the label side faces upward. A total of 2,752 trajectories were collected, each averaging 61 seconds, resulting in approximately 47 hours of data. 

Both the folding and grasping datasets are planned to be released publicly in the future. 

The training of iFlyBot-VLA consists of two stages. In the **first pre-training stage** , we use the full text-based spatial QA dataset, the OXE and AgiBot open-source datasets, and the complete self-collected dual-arm manipulation dataset from iFLYTEK, which covers diverse scenes and tasks. In the **second fine-tuning stage** , the model is trained on task-specific datasets to adapt to particular robot actions. The data distribution ratio for pre-training is illustrated in Fig. 4. 

## **4.2 Training Strategy** 

In the **first-stage pre-training** , the full dataset—including the general spatial QA data—is utilized. For the QA data, iFlyBot-VLA employs special marker tokens. All action outputs for these samples are set to zero, and the action loss is not computed. Additionally, no gradient is propagated through the action expert module for these samples. 

7 


**Figure 4 Overview of our dataset.** The pretraining mixture consists of subsets of OXE, AgiBot_World, self-collected manipulation data, and VQA data. The left figure shows the proportion of different datasets in the pretraining mixture, while the right figure illustrates the composition of QA datasets during the pretraining stage. 

For robotic manipulation data, since the action expert is randomly initialized, the end-to-end training gradients will cause significant interference to the pre-trained VLM. This interferes with the preservation and learning of the VLM’s capabilities. iFlyBot-VLA truncates the gradient flow from the action expert to the vision-language backbone. 

In the **second-stage fine-tuning** , after pre-training, the vision-language backbone already possesses strong possesses strong capabilities in embodied perception, reasoning, and implicit action feature extraction. The focus of fine-tuning is therefore on enabling the action expert to learn robot-specific control dynamics and foster better interaction between upstream and downstream modules. During this stage, gradient propagation from the action expert to the vision-language backbone is enabled, because the gradients of the action experts in the randomly initialized Diffusion Transformer structure will undermine the capabilities of the pre-trained VLM component. Moreover, while the pre-trained VLM already possesses strong capabilities in embodied perception, reasoning, and implicit action feature extraction, the action expert still needs further adaptation to downstream tasks, iFlyBot-VLA for each batch of actions applies **multi-sample noise perturbations** —sampling different noisy versions of the same action sequence—to perform denoising and backpropagation jointly. This strategy accelerates training and enhances the stability of the action expert. 

Throughout all training stages, iFlyBot-VLA pads both action and state vectors to a **20-dimensional space** , where the first 10 dimensions correspond to the left arm and the latter 10 to the right arm. For single-arm datasets, during the first-stage training, the action data are randomly assigned to either the left or right arm to maintain consistency in input dimensionality. 

# **5 Experiments** 

To systematically evaluate the performance of iFlyBot-VLA and the effectiveness of its individual components, we conducted experiments in both simulated and real-world environments. The iFlyBot-VLA model was first tested in the **LIBERO simulator** [31], where it was compared with several existing methods to validate its performance. In addition, ablation studies were performed within LIBERO to examine the respective contributions of explicit and implicit planning to the overall model performance. 

In real-world scenarios, iFlyBot-VLA was tested across three distinct task settings: (1) complex tabletop pickand-place, (2) manipulation of irregularly shaped and deformable objects, and (3) cloth folding. The results demonstrate that iFlyBot-VLA achieves strong stability and generalization across diverse and challenging tasks, effectively learning robust policies capable of handling long-horizon and fine-grained manipulation. 

## **5.1 Results in the LIBERO Simulator** 

The **LIBERO benchmark** (see Fig. 5) consists of four task suites designed to evaluate learning approaches in robotic manipulation. In this work, we focus on **supervised fine-tuning within target task suites** , using 

8 

imitation learning combined with _flow-matching denoising_ to train policies on successful demonstration trajectories, and then assess their performance. 


**Figure 5** Task suites in the LIBERO dataset. 

As illustrated in Fig. 5, LIBERO includes four task suites, each containing 10 tasks with 10 demonstrations per task: 

1. **LIBERO-Spatial:** Tasks require spatial reasoning, such as accurately placing a bowl based on inferred geometric relationships, evaluating the model’s ability in spatial and geometric reasoning. 

2. **LIBERO-Object:** The scene layout remains fixed while object categories vary, testing the model’s generalization to new object instances. 

3. **LIBERO-Goal:** Object and scene layouts are fixed, but task goals differ, evaluating goal-directed adaptability and reasoning. 

4. **LIBERO-Long:** Long-horizon tasks composed of multiple sub-goals, diverse objects, layouts, and task sequences, testing the model’s ability to plan and execute multi-step manipulation. 

During training, we follow the **OpenVLA** data preprocessing pipeline by removing all failed demonstrations. iFlyBot-VLA was trained for **70,000 steps** on the LIBERO-Long suite and **50,000 steps** on the remaining suites, with a global batch size of 64 and an action window size of 7 for both training and inference. Only third-person camera images and textual task instructions were used as inputs. Importantly, none of the LIBERO samples overlapped with those used in pre-training or latent action model training, ensuring a stringent test of the model’s generalization ability. 

The comparison baselines include three representative models, among which **OpenVLA** and _π_ 0 are most closely related to our method: 

- **LAPA** [47]: An unsupervised framework that learns latent actions from unlabelled human videos. 

- **OpenVLA** [29]: A vision-language-action model trained on large-scale and diverse datasets such as OpenX to achieve general-purpose robot policy learning. 

- _π_ 0 [6]: A vision-language-action model that generates continuous actions via an action expert trained on OpenX and self-collected robot data, then fine-tuned for downstream tasks. 

The experimental results are shown in Fig. 6. 

In this experiment, iFlyBot-VLA achieved an **average accuracy of 93.8%** across LIBERO tasks, outperforming the best existing VLA model, _π_ 0 (86%), and significantly surpassing OpenVLA (76.5%). iFlyBot-VLA achieved state-of-the-art performance in all task suites except LIBERO-Goal, where it still reached 93%, nearly matching _π_ 0’s 95%. These results demonstrate that iFlyBot-VLA achieves strong and consistent performance within the LIBERO simulator, with clear improvements over previous action-window-based approaches. 

9 


**Figure 6** Comparison of iFlyBot-VLA and representative VLA models on the LIBERO simulator dataset. 

## **5.2 Ablation Study in LIBERO** 

To further investigate the roles of explicit and implicit planning, an ablation study was conducted in the LIBERO simulator. The results are presented in Fig. 7. 


**Figure 7** Ablation results showing the effect of different components of iFlyBot-VLA in the LIBERO simulator. 

The full iFlyBot-VLA model achieved the best overall performance. Compared to the version without the Fast module ( _w/o Fast_ ), which achieved 87.8% success, the full model improved by 6%. Compared to the version without the LAM module ( _w/o LAM_ ), which achieved 90.3%, the full model improved by 3.5%. When both Fast and LAM modules were removed ( _w/o Fast and LAM_ ), success dropped to 73%, yielding a 20.8% improvement when both were included. These results clearly demonstrate that both explicit and implicit planning mechanisms contribute positively to task execution, particularly for long-horizon manipulation tasks, where their combined effect is most pronounced. 

10 

## **5.3 Real-World Experiments** 

Our real-world experiments consist of three main parts: 

- General Pick-and-Place Tasks: We evaluate iFlyBot-VLA’s performance when facing unseen objects, lighting variations, and novel scenes. 

- Long-Horizon Manipulation Tasks: We measure the overall task success rate and the step-by-step completion accuracy of iFlyBot-VLA in extended manipulation sequences. 

- Dexterous Dual-Arm Manipulation: We assess the model’s performance in tasks that require precise and coordinated control of both robotic arms. 

To enable direct comparison with state-of-the-art models, we fine-tuned _π_ 0 following the official instructions from its GitHub repository, using our self-collected data. 

For the real-world general pick and place experiments, we collected 175 hours of pick-and-place data using our robotic platform and teleoperation interface. The dataset includes approximately 32,000 robot trajectories covering 30 different objects. We standardized the language command input as “put A into B”, where A represents the object to be picked and B denotes the target container. 

For the baseline model _π_ 0, we finetuned it directly on the robot trajectory data following its official training pipeline. For iFlyBot-VLA, we adopted a different strategy — combining spatial-QA data with robot trajectory data, and leveraging both latent action labels and FAST labels during training. 

### **5.3.1 Genaral Pick and Place** 

Our evaluation was conducted under four different configurations. The **Basic** setting refers to test scenes and objects that also appear in the training data, with moderate and stable illumination. The **Unseen Objects** setting uses test objects that were not present in the training set but belong to the same semantic categories as seen objects, sharing similar noun descriptions in the language prompts. For example, an “Ultraman toy” not seen during training but belonging to the category “toy,” or an “Ice Red Tea” unseen during training but belonging to the category “beverage.” The detailed object categories are shown in Fig. 8(a), where the left column lists seen objects and the right column lists unseen ones. The **Light Illumination Variation** setting keeps the same scenes and objects as the training set but introduces continuously changing light conditions, including extreme illumination levels not observed during training, as illustrated in Fig. 8(b). The **Unseen Scenes** configuration tests the model on entirely different tabletop and environmental settings from those in the training set. While the training environment used square tables and cloth-covered surfaces, the test environments include alternative layouts such as factory conveyor setups and household scenes, as shown in Fig. 8(c). 

For each configuration, we evaluated 24 seen object categories or 14 unseen object categories, performing 20 pick-and-place attempts for each. The results are presented in Fig. 9. 

From the experimental results, iFlyBot-VLA achieved success rates of **96.25%** , **96.04%** , **88.21%** , and **93.57%** in the Basic, Light Illumination Variation, Unseen Objects, and Unseen Scenes configurations, respectively. These results are slightly higher than those of the baseline model, which achieved **94.79%** , **92.71%** , **81.67%** , and **87.91%** under the same conditions. The improvements demonstrate that our proposed framework effectively enhances the model’s generalization capability across varying lighting, object, and environmental conditions. 

### **5.3.2 Long-Horizon Manipulation Task** 

We collected data for a “ **parcel sorting** ” task in a simulated factory conveyor-line environment, a long-horizon dual-arm manipulation task involving deformable packages, as illustrated in Fig. 10. To complete the full sorting process, the robot must: (1) grasp a flexible package, (2) determine whether the package orientation requires flipping, and if so, perform a coordinated dual-arm flipping motion, (3) place and push the package into the designated target area, and (4) repeat steps (1)–(3) until all packages on the table are sorted. Using the prompt _“If the label is face-up, flip the package and put it in the basket”_ , we collected approximately **47 hours** of data, corresponding to around **2,752 trajectories** . 

11 


**Figure 8 Experiment Settings of Generalizable Pick-and-Place.** (a) Examples of seen and unseen objects — left: seen, right: unseen. (b) Illustration of varying illumination conditions. (c) Demonstration of grasping experiments in different scenes. 

12 


**Figure 9 Experiment Results of General Pick-and-Place.** Success rate of our policy and baseline. 


**Figure 10 Experiment Results of Long-Horizon Manipulation Tasks.** (a) Detailed steps of parcel sorting. (b) Results of our policy and baseline. 

Since the packages are soft and easily deformable, after the right arm places one corner of the package, its orientation may not be perfectly face-up. Therefore, we adopted two evaluation criteria: 

- **Strict:** All packages must reach the correct target area, and their orientations must be correct immediately after the first placement by the right arm. 

- **Allow Correction:** All packages must reach the correct target area, but if orientation errors occur after the right arm’s placement, up to two correction attempts are permitted. 

We conducted 40 repeated trials, each involving three packages (two requiring flipping). The results show that under the **Allow Correction** criterion, iFlyBot-VLA achieved a **7.5% higher success rate** than the baseline, highlighting the effectiveness of our dual-arm coordination and implicit planning strategies in handling deformable and long-horizon manipulation tasks. 

### **5.3.3 Challenging and Dexterous Dual-Arm Manipulation Task** 

The **folding** task poses significant challenges for VLA models, as it requires both high-precision manipulation (e.g., grasping the correct corners of clothing) and robust policy control to handle the highly variable states of deformable objects. Previous studies have achieved success in folding already flattened clothes in real-world 

13 


**Figure 11 Detailed Description of the Clothes Folding Task** (a) Initial state of the clothes. (b) Challenging actions involved in "flattening" 

14 


**Figure 12 We defined a step-by-step evaluation protocol and summarized the corresponding results as follows:** (a) Step Definition for the Folding Task. (b) Completion rate of each step. 

settings. However, when garments appear in arbitrary configurations—such as crumpled or twisted states—on the table, as shown in Fig. 11(a), the task becomes substantially more difficult. 

First, identifying the appropriate corner points to grasp from random configurations is highly challenging. Second, flattening the garment involves intricate sub-steps such as _“flick flattening”_ —which demands precise control over speed and acceleration, as shown in Fig. 11(b) (left)—and _“drag flattening”_ along the table edge, which requires accurate perception of the garment’s state and key feature points, as shown in Fig. 11(b)(right). 

During testing, we observed that the success of the “ **flick flattening** ” motion depends heavily on the chunk-wise optimization strategy in the inference code. To ensure a fair comparison with baselines (e.g., _π_ 0), we used the original inference code without modification and instead adopted the “ **drag-flattening** ” method. It is worth noting that although we did not employ the **flick-flattening** strategy, the combination of our model and the optimized inference policy achieved approximately 90% success rate on this single step, as demonstrated in the video available on our project homepage. For this setup, we collected data on **8 clothing types** (5 T-shirts and 3 pairs of shorts), totaling approximately **110 hours** of demonstrations, with around **200 trajectories per clothing type** . 

Given the complexity of this task, we report not only the overall success rate but also the success rate for each step to provide a more detailed comparison. Since locating the correct grasping points often requires multiple attempts, we imposed a **3-minute time limit** for each full execution. The detailed results are presented in Fig. 12(b), where the x-axis corresponds to the steps illustrated in Fig. 12(a). Note that since the flattening step may require multiple repetitions, when no overall time constraint is imposed, allowing sufficient time for corner-point searching and flattening enables iFlyBot-VLA to achieve nearly 90% task success rate. 

# **6 Limitation and Conclusion** 

**Limitation.** Although our model demonstrates outstanding performance in complex environments and longhorizon tasks, certain limitations remain. On one hand, despite the strong generalization capability of **iFlyBot-VLA** , it can still fail when following novel instructions involving unseen concepts or objects, and it faces challenges in grasping objects with shapes it has never encountered before. In future work, we plan to enhance the model’s ability to handle entirely new scenarios by scaling up the model, expanding the training dataset, and incorporating richer spatial representations.On the other hand, similar to all imitation learning approaches, **iFlyBot-VLA** may struggle to maintain performance or recover effectively when encountering 

15 

out-of-distribution inputs during inference. Therefore, in future research, we aim to integrate reinforcement learning (RL) mechanisms to further improve the model’s generalization ability and robustness in dexterous manipulation tasks, ultimately surpassing the inherent limitations of imitation learning and achieving stronger performance across more complex scenarios. 

**Conclusions.** In this report, we introduced **iFlyBot-VLA** — a powerful **Vision-Language-Action (VLA)** model capable of generating action commands for controlling dual-arm mobile robots. We conducted an in-depth investigation of the model architecture and proposed a novel **explicit + implicit action planning framework** , which significantly improves model performance while introducing only a minimal increase in inference time. 

Comprehensive experiments were conducted both in the **LIBERO simulator** and in real-world environments. The results demonstrate that iFlyBot-VLA excels in several key aspects: it generalizes effectively to unseen objects and environments, and exhibits remarkable robustness and reliability in executing both long-horizon and fine-grained manipulation tasks. 

We believe that iFlyBot-VLA lays a solid foundation for the development of **general-purpose robotic systems** capable of assisting humans in a wide variety of everyday tasks, and that it contributes to advancing the field of general robotic intelligence. 

16 

# **References** 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv <u>preprint</u> arXiv:2303.08774, 2023. 

- [2] Nasir Ahmed, T_ Natarajan, and Kamisetty R Rao. Discrete cosine transform. IEEE transactions on Computers, 100(1):90–93, 2006. 

- [3] Sridhar Pandian Arunachalam, Irmak Güzey, Soumith Chintala, and Lerrel Pinto. Holo-dex: Teaching dexterity with immersive mixed reality. arXiv <u>preprint</u> arXiv:2210.06463, 2022. 

- [4] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. arXiv <u>preprint</u> arXiv:2502.13923, 2025. 

- [5] Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. arXiv <u>preprint</u> arXiv:2407.07726, 2024. 

- [6] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. arXiv <u>preprint</u> arXiv:2410.24164, 2024. 

- [7] Kevin Black, Manuel Y Galliker, and Sergey Levine. Real-time execution of action chunking flow policies. arXiv <u>preprint</u> arXiv:2506.07339, 2025. 

- [8] Qingwen Bu, Jisong Cai, Li Chen, Xiuqi Cui, Yan Ding, Siyuan Feng, Shenyuan Gao, Xindong He, Xuan Hu, Xu Huang, et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. arXiv <u>preprint</u> arXiv:2503.06669, 2025. 

- [9] Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Univla: Learning to act anywhere with task-centric latent actions. arXiv <u>preprint</u> arXiv:2505.06111, 2025. 

- [10] Chilam Cheang, Sijin Chen, Zhongren Cui, Yingdong Hu, Liqun Huang, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Xiao Ma, et al. Gr-3 technical report. arXiv <u>preprint</u> arXiv:2507.15493, 2025. 

- [11] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. arXiv <u>preprint</u> arXiv:2305.18565, 2023. 

- [12] Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, et al. Internvla-m1: A spatially guided vision-language-action framework for generalist robot policy. arXiv <u>preprint</u> arXiv:2510.13778, 2025. 

- [13] Xuxin Cheng, Jialong Li, Shiqi Yang, Ge Yang, and Xiaolong Wang. Open-television: Teleoperation with immersive active visual feedback. arXiv <u>preprint</u> arXiv:2407.01512, 2024. 

- [14] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-the-wild robot teaching without in-the-wild robots. arXiv <u>preprint</u> arXiv:2402.10329, 2024. 

- [15] Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Sanja Fidler, Antonino Furnari, Evangelos Kazakos, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will Price, et al. Scaling egocentric vision: The epic-kitchens dataset. In Proceedings of the European conference on computer vision <u>(ECCV),</u> pages 720–736, 2018. 

- [16] Amaury Depierre, Emmanuel Dellandréa, and Liming Chen. Jacquard: A large scale dataset for robotic grasp detection. In 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems <u>(IROS),</u> pages 3511–3516. IEEE, 2018. 

- [17] Clemens Eppner, Arsalan Mousavian, and Dieter Fox. Acronym: A large-scale grasp dataset based on simulation. In 2021 IEEE International Conference on Robotics and Automation <u>(ICRA),</u> pages 6222–6227. IEEE, 2021. 

- [18] Abraham George, Alison Bartsch, and Amir Barati Farimani. Openvr: Teleoperation for manipulation. SoftwareX, 29:102054, 2025. 

- [19] Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska, Susanne Westphal, Heuna Kim, Valentin Haenel, Ingo Fruend, Peter Yianilos, Moritz Mueller-Freitag, et al. The" something something" video 

17 

database for learning and evaluating visual common sense. In Proceedings of the IEEE international conference on computer vision, pages 5842–5850, 2017. 

- [20] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, et al. Ego4d: Around the world in 3,000 hours of egocentric video. In Proceedings of the IEEE/CVF conference on computer vision and <u>pattern</u> recognition, pages 18995–19012, 2022. 

- [21] Tairan He, Zhengyi Luo, Xialin He, Wenli Xiao, Chong Zhang, Weinan Zhang, Kris Kitani, Changliu Liu, and Guanya Shi. Omnih2o: Universal and dexterous human-to-humanoid whole-body teleoperation and learning. arXiv <u>preprint</u> arXiv:2406.08858, 2024. 

- [22] Ryan Hoque, Peide Huang, David J Yoon, Mouli Sivapurapu, and Jian Zhang. Egodex: Learning dexterous manipulation from large-scale egocentric video. arXiv <u>preprint</u> arXiv:2505.11709, 2025. 

- [23] Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. arXiv <u>preprint</u> arXiv:2504.16054, 2025. 

- [24] Tao Jiang, Tianyuan Yuan, Yicheng Liu, Chenhao Lu, Jianning Cui, Xiao Liu, Shuiqi Cheng, Jiyang Gao, Huazhe Xu, and Hang Zhao. Galaxea open-world dataset and g0 dual-system vla model. arXiv <u>preprint</u> arXiv:2509.00576, 2025. 

- [25] Yun Jiang, Stephen Moseson, and Ashutosh Saxena. Efficient grasping from rgbd images: Learning using a new rectangle representation. In 2011 IEEE International conference on robotics and automation, pages 3304–3311. IEEE, 2011. 

- [26] Dmitry Kalashnikov, Alex Irpan, Peter Pastor, Julian Ibarz, Alexander Herzog, Eric Jang, Deirdre Quillen, Ethan Holly, Mrinal Kalakrishnan, Vincent Vanhoucke, et al. Scalable deep reinforcement learning for vision-based robotic manipulation. In Conference on robot learning, pages 651–673. PMLR, 2018. 

- [27] Daniel Kappler, Jeannette Bohg, and Stefan Schaal. Leveraging big data for grasp planning. In 2015 IEEE international conference on robotics and automation <u>(ICRA),</u> pages 4304–4311. IEEE, 2015. 

- [28] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. arXiv <u>preprint</u> arXiv:2403.12945, 2024. 

- [29] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. arXiv <u>preprint</u> arXiv:2406.09246, 2024. 

- [30] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. arXiv <u>preprint</u> arXiv:2210.02747, 2022. 

- [31] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. Advances in Neural Information Processing Systems, 36:44776– 44791, 2023. 

- [32] Qiang Liu. Rectified flow: A marginal preserving approach to optimal transport. arXiv <u>preprint</u> arXiv:2209.14577, 2022. 

- [33] Yunze Liu, Yun Liu, Che Jiang, Kangbo Lyu, Weikang Wan, Hao Shen, Boqiang Liang, Zhoujie Fu, He Wang, and Li Yi. Hoi4d: A 4d egocentric dataset for category-level human-object interaction. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 21013–21022, 2022. 

- [34] Jeffrey Mahler, Jacky Liang, Sherdil Niyaz, Michael Laskey, Richard Doan, Xinyu Liu, Juan Aparicio Ojea, and Ken Goldberg. Dex-net 2.0: Deep learning to plan robust grasps with synthetic point clouds and analytic grasp metrics. arXiv <u>preprint</u> arXiv:1703.09312, 2017. 

- [35] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In 2024 IEEE International Conference on Robotics and Automation <u>(ICRA),</u> pages 6892–6903. IEEE, 2024. 

18 

- [36] William Peebles and Saining Xie. Scalable diffusion models with transformers. In Proceedings of the IEEE/CVF international conference on computer vision, pages 4195–4205, 2023. 

- [37] Lerrel Pinto and Abhinav Gupta. Supersizing self-supervision: Learning to grasp from 50k tries and 700 robot hours. In 2016 IEEE international conference on robotics and automation <u>(ICRA),</u> pages 3406–3413. IEEE, 2016. 

- [38] Yusuxke Shibata, Takuya Kida, Shuichi Fukamachi, Masayuki Takeda, Ayumi Shinohara, Takeshi Shinohara, and Setsuo Arikawa. Byte pair encoding: A text compression scheme that accelerates pattern matching. 1999. 

- [39] Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. arXiv <u>preprint</u> arXiv:2503.20020, 2025. 

- [40] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. arXiv <u>preprint</u> arXiv:2405.12213, 2024. 

- [41] Ievgenii A Tsokalo, David Kuss, Ievgen Kharabet, Frank HP Fitzek, and Martin Reisslein. Remote robot control with human-in-the-loop over long distances using digital twins. In 2019 IEEE Global Communications Conference <u>(GLOBECOM),</u> pages 1–6. IEEE, 2019. 

- [42] Mohammad Hassan Vali and Tom Bäckström. Nsvq: Noise substitution in vector quantization for machine learning. IEEE Access, 10:13598–13610, 2022. doi: 10.1109/ACCESS.2022.3147670. 

- [43] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. Advances in neural information <u>processing</u> systems, 30, 2017. 

- [44] Xiaofeng Wang, Kang Zhao, Feng Liu, Jiayu Wang, Guosheng Zhao, Xiaoyi Bao, Zheng Zhu, Yingya Zhang, and Xingang Wang. Egovid-5m: A large-scale video-action dataset for egocentric video generation. arXiv <u>preprint</u> arXiv:2411.08380, 2024. 

- [45] Xin Wang, Taein Kwon, Mahdi Rad, Bowen Pan, Ishani Chakraborty, Sean Andrist, Dan Bohus, Ashley Feniello, Bugra Tekin, Felipe Vieira Frujeri, et al. Holoassist: an egocentric human interaction dataset for interactive ai assistants in the real world. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 20270–20281, 2023. 

- [46] Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. arXiv <u>preprint</u> arXiv:2412.13877, 2024. 

- [47] Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Sejune Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, et al. Latent action pretraining from videos. arXiv <u>preprint</u> arXiv:2410.11758, 2024. 

- [48] Xinghao Zhu, Ran Tian, Chenfeng Xu, Mingxiao Huo, Wei Zhan, Masayoshi Tomizuka, and Mingyu Ding. Fanuc manipulation: A dataset for learning-based manipulation with fanuc mate 200id robot. `https://sites.google. com/berkeley.edu/fanuc-manipulation` , 2023. 

- [49] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In Conference on Robot Learning, pages 2165–2183. PMLR, 2023. 

19 

