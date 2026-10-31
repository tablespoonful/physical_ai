---
title: "Dita: Scaling Diffusion Transformer for Generalist Vision-Language-Action Policy"
date: "2025-03-25"
authors: "Zhi Hou; Tianyi Zhang; Yuwen Xiong; Haonan Duan; Hengjun Pu; Ronglei Tong"
venue: "ICCV 2025"
url: https://arxiv.org/abs/2503.19757
pdf: https://arxiv.org/pdf/2503.19757
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.19757)** / [論文ページ](https://arxiv.org/abs/2503.19757)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

This ICCV paper is the Open Access version, provided by the Computer Vision Foundation. Except for this watermark, it is identical to the accepted version; the final published version of the proceedings is available on IEEE Xplore. 

# **Dita: Scaling Diffusion Transformer for Generalist Vision-Language-Action Policy** 


Figure 1. We introduce Dita, an open-source, simple yet effective policy for generalist robotic learning. Pretrained on large-scale crossembodiment datasets, Dita enables 10-shot adaptation to complex, multitask, long-horizon scenarios in novel robot setups. _Particularly, Dita can complete intricate, extended-horizon tasks such as, “close the top drawer, then open the bottom drawer, subsequently place the bowl into the bottom drawer, and finally close the bottom drawer”. Furthermore, Dita demonstrates remarkable robustness against complex object arrangements and even challenging lighting conditions in sophisticated 3D pick-and-rotation tasks._ In this context, the long-horizon demonstration scene serves as the training environment for all tasks. Additionally, Dita seamlessly scales to a wide range of popular simulation benchmarks, achieving state-of-the-art performance across these tasks. 

## **Abstract** 

_While recent vision-language-action models trained on diverse robot datasets exhibit promising generalization capabilities with limited in-domain data, their reliance on compact action heads to predict discretized or continuous actions constrains adaptability to heterogeneous ac-_ 

> *Equal Contribution 

> †Corresponding Author 

_tion spaces. We present Dita, a scalable framework that leverages Transformer architectures to directly denoise continuous action sequences through a unified multimodal diffusion process. Departing from prior methods that condition denoising on fused embeddings via shallow networks, Dita employs in-context conditioning—enabling fine-grained alignment between denoised actions and raw visual tokens from historical observations. This design explicitly models action deltas and environmental nuances._ 

7686 

_By scaling the diffusion action denoiser alongside the Transformer’s scalability, Dita effectively integrates crossembodiment datasets across diverse camera perspectives, observation scenes, tasks, and action spaces. Such synergy enhances robustness against various variances and facilitates the successful execution of long-horizon tasks. Evaluations across extensive benchmarks demonstrate state-ofthe-art or comparative performance in simulation. Notably, Dita achieves robust real-world adaptation to environmental variances and complex long-horizon tasks through 10shot finetuning, using only third-person camera inputs. The architecture establishes a versatile, lightweight and opensource baseline for generalist robot policy learning._ 

## **1. Introduction** 

Conventional robot learning paradigms typically depend on large-scale data collected for specific robots and tasks, yet the acquisition of data for generalized tasks remains both time-intensive and costly due to the inherent limitations of real-world robot hardware. Presently, foundational models in Natural Language Processing and Computer Vision [16, 41, 50–52, 62], pretrained on extensive, diverse, and task-agnostic datasets, have demonstrated remarkable efficacy in addressing downstream tasks either via zero-shot approaches or with minimal task-specific samples. This achievement implies that a universal robotic policy, pretrained on heterogeneous robotic data and finetuned with minimal supervision, could be instrumental in realizing true generalization in the development of visionlanguage-action (VLA) models. Nevertheless, training such policies across expansive cross-embodiment datasets, encompassing diverse sensors, action spaces, tasks, camera views, and environments, remains an open challenge. 

In pursuit of a unified robotic policy, recent studies have directly mapped visual observations and language instructions to actions using expansive VLA models for navigation [65, 66] or manipulation [8, 9, 32, 72], thereby demonstrating zero-shot or few-shot generalization in novel environments. Robot Transformers [8, 9, 54] present policy frameworks based on Transformer architectures, achieving robust generalization by training on the extensive Open X- Embodiment (OXE) Dataset [54]. Furthermore, Octo [72] adopts an autoregressive Transformer design with a diffusion action head, while OpenVLA [32] discretizes the action space and leverages a pretrained visual-language model to construct a VLA model exposed to the OXE Dataset [54]. Nonetheless, despite the promising potential of these VLA models [32, 72] to learn robot policies from vast crossembodiment datasets [54], the intrinsic diversity of robot configurations within these datasets continues to constrain generalization. 

Diffusion policies [17, 30, 61, 83] have demonstrated 


Figure 2. Illustrations of different generalist robot policy architectures. Left head: the common robot Transformer architecture with discretization actions, _e.g_ ., Robot Transformer [8, 9] and OpenVLA [32]. Middle head: the Transformer architecture with diffusion action head which denoises the individual continuous action with a small network condition on each embedding from the causal Transformer, _e.g_ ., Octo [72] and _ω_ 0 [5]. Right head: the proposed Dita architecture that denoises actions inherently in an in-context conditioning style. 

reliable performance in robotic policy learning under the paradigm of single-task imitation learning. Specifically, [18, 72] introduces a generalist policy that denoises actions using a network (MLP/DiT) as diffusion head conditioned on a single embedding from an auto-regressive multimodal Transformer. However, the expansive robot space within large-scale cross-embodiment datasets, encompassing diverse camera views and action spaces, presents a substantial challenge for a tiny diffusion head to effectively denoise continuous actions. Other diffusion policies [30, 61, 72] attempt to integrate historical image observations and instructions into embeddings prior to the denoising process, which might limit the denoising learning. Action anticipation typically relies more on intuitive historical observations rather than on early-fused embeddings. 

In this paper, we introduce Dita, a Diffusion Transformer (DiT) Policy that capitalizes on the Transformer architecture, as demonstrated in prior work [8, 9, 32, 54, 72], thereby ensuring scalability across extensive crossembodiment datasets. The architecture integrates an incontext conditioning mechanism with causal transformer that intrinsically denoises action sequences, thereby enabling direct conditioning of action denoising on image tokens and empowering the model to discern subtle nuances, such as action deltas, within historical visual observations. Our objective is to provide a clean, lightweight (334M parameters), and open-source baseline model for generalist robot policy learning. The model is simple yet effective, achieving state-of-the-art or competitive results on extensive simulation benchmarks, and successfully generalizing to long-horizon tasks in novel environmental configurations—characterized by variations in background, non-target object arrangements, and lighting conditions through finetuning with a mere 10-shot set of real- 

7687 

world samples. Remarkably, this promising performance is achieved exclusively with a single third-person camera input, while the model’s inherent flexibility affords researchers the freedom to integrate additional input modalities (e.g., wrist-camera images, target image predictions, robot state, tactile feedback, etc.) for further investigation. 

## **3. Method** 

In this section, we describe Dita in detail. We begin by detailing the architecture of the model, which is a scalable DiT with in-context conditioning. We then define the training objective for generating multi-modal actions. Finally, we present the data and implementation specifics for the pretraining of our model. 

## **2. Related Work** 

### **3.1. Architecture** 

**Diffusion Policy** Denoising diffusion models [11, 19, 25, 56, 63] have demonstrated remarkable proficiency in both image generation and multi-modal robotic action modeling [12, 14, 17, 30, 39, 42, 61, 74, 75, 77, 83]. Nevertheless, existing diffusion-based manipulation policies predominantly rely on U-Net architectures or shallow crossattention networks designed for single tasks, limiting their scalability to multi-modal applications. Recent generalist models [72, 76] employ VLM embeddings combined with compact MLP diffusers, while others, like RDT [42] and [18], utilize cross-attention Transformers or DiT decoders for bimanual manipulation. In contrast, we propose a scalable DiT with in-context conditioning, which directly processes historical observations through a causal Transformer architecture, thereby providing enhanced expressiveness and generalization capabilities for multi-modal action generation. 

**Generalist Robot Policies** Language-conditioned policies [15, 23, 44, 49, 60, 73, 84] have gained prominence for their adaptability in real-world applications, enabling robots to interpret and execute natural language instructions. Recent advancements in generalist robot policies leverage foundation multi-modal models across both navigation [6, 27, 65, 66, 71, 82] and manipulation [3, 7– 9, 20, 21, 29, 32, 45, 46, 54, 55, 60, 64, 67, 68, 72, 79, 80], with scalable VLA models emerging as a dominant framework [1, 8, 9, 32, 54, 58, 72]. Some approaches incorporate large-scale video backbones trained on internet-scale data [13, 28, 34, 78] to improve temporal visual reasoning. While these methods enhance visual representation learning, our focus is on action generation, where diffusionbased models provide a more expressive alternative. Another crucial factor in generalist policies is the choice of pretrained VLM models for action generation. Unlike recent works [5, 38] that employ PaliGemma [2] to enhance vision-language understanding, we adopt a LLaMA-style causal Transformer for policy learning. This approach is both simple and highly scalable, demonstrating effectiveness across a wide range of benchmarks. Furthermore, by aligning robot actions with language instructions and visual observations in an in-context conditional manner, our method significantly enhances generalization across diverse robotic embodiments. 

**Multi-modal Input Tokenization** . Dita only takes language instructions and third-person camera images as input. The language instructions are tokenized using a frozen CLIP [59] model, while the image observations are first processed by DINOv2 [53] to extract image patch features. Notably, DINOv2 is trained on web data, which differs from robot-specific data. Thus, we jointly optimize the DINOv2 parameters alongside Dita in an end-to-end fashion. To mitigate computational costs, we incorporate a Q-Former [33] with FiLM [57] conditioning to select image features from the DINOv2 patch features based on the instruction context. 

**Action Preprocess** . We represent the end-effector action as a 7D vector, comprising 3 dimensions for the translation vector, 3 dimensions for the rotation vector, and 1 dimension for the gripper position. To align the dimensionality with the image and language tokens, we pad the continuous action vector with zeros to form the action representation. Noise is only introduced into the 7D action vector during the denoising diffusion optimization process. 

**Model Design** . Our core design is the DiT structure [56], which denoises the action chunk with multiple action tokens. This is achieved by conditioning directly on image observations and instruction tokens through an in-context conditioning approach using a causal Transformer. Specifically, we concatenate language tokens, image features, and timestep embeddings at the beginning of the sequence, treating the noisy action in conjunction with the instruction tokens, as illustrated in Figure 3. This design preserves the scalability of Transformer networks and enables denoising to be conditioned directly on image patches, thereby allowing the model to capture nuanced changes in action over historical observations. The model is supervised by the noise introduced into the continuous actions. In other words, we directly apply the diffusion objective in the action chunk space with a large Transformer model, in contrast to the diffusion action head approach [18, 61, 72]. Notably, our proposed Dita presents a versatile and scalable design, adaptable to diverse datasets for both pretraining and finetuning, while achieving promising performance. Furthermore, additional observation tokens and input can be seamlessly integrated into the Transformer architecture. Further details are provided in Appendix A. 

7688 


Figure 3. Our model employs a Transformer-based diffusion architecture, integrating a pretrained CLIP network to extract language instruction tokens. The DinoV2 [53] model encodes image observations, followed by a Q-Former that queries features for each image. The instruction tokens, image features, timestep embeddings, and noised action are concatenated to construct a token sequence, which is then fed into the network to denoise the raw actions. 

### **3.2. Training Objective** 

The denoising network _Eω_ ( _clang, cobs, t,_ **_x_**<sup>_t_</sup> ) is constructed upon a causal Transformer, where _cobs_ represents the image observation, _clang_ denotes the language instruction, and _t →_ 1 _,_ 2 _, . . . , Ttrain_ is the timestep index within the total denoising steps _Ttrain_ . During training, a Gaussian noise vector **_x_**<sup>_t_</sup> _↑N_ ( **0** _,_ **_I_** ) is sampled at each timestep _t_ and added to the action **_a_** to form the noised action token ˆ **_a_** . The network _Eω_ is trained to predict the noise vector **_x_** ˆ, with randomly sampled _t_ . The optimization objective of Dita is to minimize the mean squared error (MSE) loss between **_x_**<sup>_t_</sup> and **_x_** ˆ<sup>_t_</sup> . 

The inference procedure is delineated as follows, _ω_ , _ε_ , and _ϑ_ constitute the noise scheduler [25]. The denoising process is iterated over _Neval_ steps to yield a reliable action. 

**_x_**<sup>_t→_1</sup> = _ω_ ( **_x_**<sup>_t_</sup> _↓ εEω_ ( _clang, cobs, t,_ **_x_**<sup>_t_</sup> ) + _N_ ( **0** _, ϑ_<sup>2</sup> **_I_** )) _._ (1) 

### **3.3. Pretraining Data** 

To evaluate the proposed Dita policy, we select the OXE datasets [32, 54] for model pretraining. We primarily adhere to the method detailed in [32, 72] for dataset selection and weight assignment. Actions are normalized and filtered similar to [54]. 

image observations to predict 16 action chunks. The network is optimized by AdamW [43] for 100,000 steps, with learning rates of 1 _e↓_ 4 for both the causal Transformer and Q-Former, and 1 _e↓_ 5 for DINOv2. Training is conducted with a batch size of 8192 across 32 NVIDIA A100 GPUs, allocating 256 samples per GPU. Additional pretraining configurations are detailed in Appendix A. 

## **4. Simulation Experiments** 

We strive to develop a robust foundational VLA model that is both scalable across diverse simulation benchmarks and adaptive to new complex tasks in unseen robot environments with as few as 10 or even fewer samples. To assess the capabilities of the pretrained model, we conduct evaluations across four simulation benchmarks in this section: 1) SimplerEnv [37] (Google Robot) demonstrates the model’s zero-shot adaptation to simulation environments; 2) LIBERO [40] assesses finetuning adaptability with a single-camera setup; 3) Calvin [47] evaluates longhorizon task performance in novel environments; and 4) ManiSkill2 [22] is re-rendered to illustrate generalization across unseen camera views. Across all four benchmarks, Dita pretrained on OXE datasets _Eω↑OXE_ is evaluated in a zero-shot manner on SimplerEnv, while it is finetuned on the remaining three benchmarks using their respective datasets. 

### **3.4. Pretraining Details** 

We employ the DDPM diffusion objective [25] with _Ttrain_ = 1000 timesteps for pretraining, while adopting DDIM [69] with _Teval_ = 20 timesteps during zero-shot evaluation to accelerate inference. Based on preliminary experiments reported in ManiSkill2 [22], we utilize 2-frame 

### **4.1. Baselines** 

**Diffusion Action Head** The diffusion head for the action generation _Eω_<sup>_Diff_</sup> _↑s_ [72] is also implemented. Specifically, we employ a three-layer MLP network as the denoising module, conditioned on each action token embedding out- 

7689 

Table 1. Success rate comparison with RT-1-X [8], Octo-Base [72] and OpenVLA-7B [32] on SimplerEnv (both match and variant results of Google Robot [8]). 

|**Method**|**coke**<br>match|**~~c~~an**<br> variant|**move**<br>match|**~~n~~ear**<br> variant|**dra**<br>match|**wer**<br> variant|
|---|---|---|---|---|---|---|
|RT-1-X [8]|56.7%|49.0%|31.7%|32.3%|**59.7%**|29.4%|
|Octo-Base [72]|17.0%|0.6%|4.2%|3.1%|22.7%|1.1%|
|OpenVLA-7B [32]|16.3%|54.5%|46.2%|47.7%|35.6%|17.7%|
|Dita (Ours)|**83.7% **|**85.5%**|**76.0% **|**73.0%**|46.3%|**37.5%**|


puted by the same causal Transformer architecture (as Middle head illustrated in Figure 2). This approach introduces additional parameters (the extra MLP) compared to Dita. **Octo & OpenVLA** We also reproduce these two opensource VLA models using their released checkpoints, as they employ the same multimodal inputs (language instruction and third-person camera image) as our approach. 

### **4.2. SimplerEnv** 

SimplerEnv [37] is a Real-to-Sim platform designed to evaluate policies learned from real robot data within a simulation environment. In this section, we compare our approach with leading generalist policies, including RT-1-X [8, 54], Octo [72], and OpenVLA [32], under both match and variant scenarios. For a fair comparison, we adhere to the evaluation protocol of SimplerEnv [37], which includes tasks “pick up coke can”, “move an object near to others”, “open drawer”, “close drawer”. 

Table 1 demonstrates that Dita achieves strong generalization performance under zero-shot evaluation across various types of variations, including background, texture, objects, spatial positions, and more. Leveraging the in-context conditioning design, Dita exhibits enhanced robustness, relying solely on third-person view images to detect subtle nuances and generate more reliable actions. The qualitative results are listed in Appendix B.1. 

### **4.3. LIBERO** 

LIBERO [40] is a comprehensive benchmark for knowledge transfer in multitask and lifelong robot learning. It consists of four sub-datasets: LIBERO-SPATIAL, LIBEROOBJECT, LIBERO-GOAL, and LIBERO-100. Notably, LIBERO-100 is further divided into LIBERO-90 and LIBERO-LONG, with the latter featuring 10 long-horizon tasks that encompass diverse object interactions and versatile motor skills. We employ the modified version of LIBERO from OpenVLA [32] as the data source for finetuning and evaluation. 

**Comparisons** . Table 2 demonstrates that Dita outperforms baseline methods on most LIBERO sub-datasets, achieving 

Table 2. Comparison with Diffusion Policy (denoted as DP*, training from scratch) [17], Octo [72], and OpenVLA [32] on LIBERO [40]. Except for Dita results, all other results are sourced from [32]. 

|**Method**|**SPATIAL**|**OBJECT**|**GOAL LONG**|**Averge**|
|---|---|---|---|---|
|DP*[17]|78.3%|92.5%|68.3% 50.5%|72.4%|
|Octo [72]|78.9%|85.7%|84.6% 51.1%|75.1%|
|OpenVLA [32]|**84.9%**|88.4%|79.2% 53.7%|76.5%|
|Dita(Ours)|84.2%|**96.3%**|**85.4% 63.8%**|**82.4%**|
|Dita w/ wrist|**97.4%**|94.8%|**93.2% 83.6%**|92.3%|


an overall increase in average success rate by nearly 6%. Notably, Dita exhibits a 10% improvement on LIBEROLONG, highlighting its strong potential for tackling longhorizon tasks. 

### **4.4. CALVIN** 

CALVIN [47] is an open-source simulated benchmark designed for learning long-horizon, language-conditioned tasks. It consists of four distinct scenes (A, B, C, and D) and introduces the ABC _↔_ D evaluation protocol, where models are trained on environments A, B, and C and evaluated on environment D. The benchmark aims to solve up to 1,000 unique task sequences, each comprising five distinct subtasks. The primary evaluation metric is the success sequence length, which measures the ability to complete five consecutive subtasks within a sequence. To assess the longhorizon generalization of Dita, we adopt the ABC _↔_ D setting while only utilizing static RGB images as perception inputs. Additionally, we also implement a diffusion policy baseline _Eω_<sup>_Diff_</sup> _↑s_ by introducing a three-layer MLP diffusion head, further demonstrating the effectiveness of Dita’s incontext conditioning mechanism. 

**Comparisons** . Table 3 presents a comparative analysis of prior approaches and the proposed Dita on CALVIN. Without whistles and bells, the proposed Dita achieves comparable performance among methods relying solely on a single RGB camera for observation. Noticeably, only 1% of the trajectories were labeled with text in Calvin [47]. The rest are unstructured play data collected by untrained users, with no information for downstream tasks. _Dita does not utilize the play data which provides external trajectory data compared to the labeled data, while GR-MG uses it for training the policy._ Remarkably, GHIL-Glue [4, 24], which builds upon SuSIE [4] with further finetuned generative models [10, 81], results in significantly larger models. Furthermore, Dita surpasses its non-pretrained variant by a margin of 1.23, underscoring its superior transferability. In contrast, employing diffusion head underperforms Dita by 0.45 points with similar pretrained weights, highlighting the 

7690 

Table 3. The comparisons with state-of-the-art approaches on Calvin (ABC _→_ D) with the metrics of success rate and average success length. The abbreviations denote different input modalities: S-RGB for Static RGB, G-RGB for Gripper RGB, S-RGBD for Static RGBD, G-RGBD for Gripper RGB-D, P for proprioceptive arm position, and Cam for camera parameters. 

|**Mthd**|**It**||**No. Inst**|**ructions i**|**n a Row(1 **|**000 chain**|**s)**|
|---|---|---|---|---|---|---|---|
|**eo**|**npu**|1|2|3|4|5|Avg.Len.|
|RoboFlamingo [36]|S-RGB,G-RGB|82.4%|61.9%|46.6%|33.1%|23.5%|2.47|
|GR-1 [78]|S-RGB,G-RGB,P|85.4%|71.2%|59.6%|49.7%|40.1%|3.06|
|3D Diffuser [30]|S-RGBD,G-RGBD,P,Cam|92.2%|78.7%|63.9%|51.2%|41.2%|3.27|
|GR-MG[34]|S-RGBD,G-RGBD,P|**96.8%**|**89.3%**|**81.5%**|**72.7**%|**64.4**%|**4.04**|
|SuSIE [4]|S-RGB|87.0%|69.0%|49.0%|38.0%|26.0%|2.69|
|GHIL-Glue[4,24]|S-RGB|**95.2%**|**88.5%**|**73.2%**|**62.5%**|**49.8%**|**3.69**|
|_E_<sup>_Diff_</sup><br>_ω→s_<br>w/o Pretrain|S-RGB|75.5%|44.8%|25.0%|15.0%|7.5%|1.68|
|_E_<sup>_Diff_</sup><br>_ω→s_|S-RGB|94.3%|77.5%|62.0%|48.3%|34.0%|3.16|
|Ours w/o Pretrain|S-RGB|89.5%|63.3%|39.8%|27.3%|18.5%|2.38|
|Ours|S-RGB|**94.5%**|**82.5%**|**72.8%**|**61.3%**|**50.0%**|**3.61**|


efficacy of Dita’s in-context conditioning mechanism. The results illustrate that Dita excels at discerning subtle visual nuances in long-horizon tasks and generalizes proficiently across diverse environments, effectively transferring knowledge from extensive, real-world pretraining datasets to the CALVIN benchmark. 

### **4.5. ManiSkill2** 

ManiSkill2 [22], the next generation of the SAPIEN ManiSkill benchmark [48], serves as a widely recognized platform for assessing the generalized manipulation capabilities of embodied models. It encompasses 20 distinct manipulation task families and over 4M demonstration frames across various configurations. Leveraging ManiSkill2, we establish a _novel camera view generalization_ benchmark to evaluate the effectivenes of Dita. 

**Setup** . To construct the benchmark, we select 5 tasks (PickCube-v0, StackCube-v0, PickSingleYCB-v0, PickClutterYCB-v0, PickSingleEGAD-v0) from ManiSkill2 and create a camera pool comprising 300K random cameras. More details are provided in Appendix. We also implement RT-1 [8] style baseline model _Eω_<sup>_Disc_</sup> _↑s_<sup>with an ar-</sup> chitecture similar to ours for comparison. Unlikely, we discretize each action dimension into 256 bins [8] and utilize a Transformer network to predict the corresponding bin indices. 

**Comparisons** . Table 4 compares the proposed method with the discretization action head and the diffusion action head. The experiments demonstrate that Dita outperforms the _Eω_<sup>_Disc_</sup> _↑s_<sup>in large-scale, novel camera view scenarios.Ad-</sup> ditionally, Dita shows superior performance on more complex tasks and outperforms _Eω_<sup>_Diff_</sup> _↑s_ by 20% in the PickSingleYCB task and by 12% in the PickClutterYCB task. The results highlight that Dita offers better scalability on large, diverse datasets, while also achieving enhanced camera view generalization. 

Table 4. Comparison of our model with two baseline methods (discretization and diffusion head) on ManiSkill2 success rate. The abbreviations denote the task names: S-YCB for PickSingleYCB, C-YCB for PickClutterYCB, EGAD for PickSingleEGAD. 

|**Method**|**Avg.**|**PickC StackC S-YCB**|**C-YCB**|**EGAD**|
|---|---|---|---|---|
|_E_<sup>_Disc_</sup><br>_ω→s_<br>|30.2%|41.0% 33.0% 22.0%|1.0%|54.0%|
|_E_<sup>_Diff_</sup><br>_ω→s_|58.6%|**86.0%** 76.0% 37.0%|24.0%|70.0%|
|Dita (ours)|**65.8%**|79.0% **80.0% 62.0% **|**36.0% **|**72.0%**|


### **4.6. Ablation Study** 

In this section, we conduct an ablation study on key factors in the model architecture design, including observation length, trajectory length, and denoising steps. 

**Observation length.** The length of historical observation images significantly impacts performance. As shown in Table 5, success rate drops sharply when the observation length is increased to 3. This could be due to the increased difficulty in model convergence, as the number of corresponding image tokens also rises. Additionally, we observe that using 2-frame observations enhances performance, particularly when the prediction horizon is extended. When the trajectory length is 32, Dita with 2-frame observations achieves superior performance. We argue that 2-frame observations strike an optimal balance, providing sufficient visual distinction between objects in the workspace and the robot states. 

**Trajectory length.** Trajectory length is the sum length of observation and action prediction chunks, which is also a critical factor influencing performance. Table 5 shows that performance improves as trajectory length increases. Notably, the performance of more complex tasks, such as PickClutterYCB, increases substantially with longer trajectory lengths, while simpler tasks, like PickCube, maintain high 

7691 

Table 5. Ablation on ManiSkill2 about the observation length (# obs) and the trajectory length (# traj). 

|**# obs**|**# traj**|**All**|**PickC StackC**|**S-YCB**|**C-YCB**|**EGAD**|
|---|---|---|---|---|---|---|
|2|2|40.8%|68.0% 54.0%|33.0%|9.0%|40.0%|
|2|4|51.6%|81.0% 69.0%|44.0%|11.0%|53.0%|
|2|8|62.4%|**89.0**% 78.0%|54.0%|25.0%|66.0%|
|2|16|65.6%|83.0% **80.0**%|**70.0**%|25.0%|70.0%|
|2|32|**65.8**%|79.0% **80.0**%|62.0%|**36.0**%|**72.0**%|
|1|32|61.6%|78.0% 76.0%|64.0%|24.0%|66.0%|
|1|1|51.0%|79.0% 66.0%|42.0%|19.0%|49.0%|
|3|3|35.4%|54.0% 49.0%|27.0%|5.0%|42.0%|


Figure 4. The experimental platform consists of Franka Emika Panda robot arm, Robotiq 2F-85 gripper and RealSense D435i positioned in third-person view. 

performance once the trajectory length exceeds 4. Long trajectory length significantly boosts performance, as this optimization allows the model to better anticipate the target object’s position and gain awareness of more future states. 

## **5. Real-Robot Experiments** 

Few-shot real-world robot adaptation is a critical metric for evaluating the effectiveness of a generalist policy in practical applications. For real-robot experiments, We employ 10-shot finetuning to assess the model’s adaptability in complex, long-horizon, multi-modal tasks within unseen robot environments. 

### **5.1. Real-Robot Task Finetuning** 

**Setup.** To deploy the Dita model, as shown in Figure 4, the robot setup consists of a 7-DoF tabletop Franka Emika Panda robot arm and a Robotiq 2F-85 gripper. A RealSense D435i RGB-D camera, positioned approximately 1.5m away from the robot in a third-person view, captures RGB scenes with cluttered background at each inference timestep. Robot control is managed from a desktop computer running ROS, communicating with the model-deploy 

server with 1 NVIDIA A100 GPU. The system is operating under control frequency of 3Hz. Given the data domain gap between our robot platform and the pretrain dataset, we primarily evaluate Dita on 10-shot generalization for the following challenging tasks relevant to current VLA approaches: 

- **Pick & Place** . Two pick-and-place tasks with target object banana and kiwifruit are evaluated. 10 samples are collected for each task, with position variances introduced during evaluation to assess generalization performance. 

- **Pour** . We design two pouring tasks to evaluate the complex rotation finetuning: “pour the coffee beans into the bowl”, and “pour the water from the teapot into the cup”. 

- **Stack** . We design two stacking tasks for long-horizon pick-and-place: stacking three bowls and stacking three Russian dolls. 

- **Pick & Rotation** . These skills combine two tasks: “pick the banana and insert it into the small pen container” and “open the flip-top door box and then pick up the small cube”. 

- **Pull & Push** . We design the task “open/close the drawer” to evaluate pull and push abilities of our models. 

- **Long-Horizon Tasks.** We further devise several longhorizon tasks (more than 3 steps), including “Pick up the bowl within the drawer and pour the coffee beans into the outside bowl”, “pick up the racket and hit the ball into the goal”, “open the top drawer, then pick the cube into the drawer, and finally close the drawer”, “close the top drawer, then open the bottom drawer and put the bowl into the drawer, and finally close the drawer” and “open the box and move the green cube into the box then close the box”, to demonstrate the long-horizon manipulation ability of Dita (detailed in demo videos in Supplementary Materials). 

The diffusion policy [17] has demonstrated strong capabilities in learning to mimic single tasks. Therefore, in addition to Octo and OpenVLA, we design a multimodal diffusion policy baseline based on a causal Transformer for comparison, which incorporates a similar diffusion head as described in Section 4.1. 

**Optimization.** We finetune the Dita on the aforementioned multiple manipulation tasks, with data collected on the same platform, using LoRA [26] for fair comparison and AdamW for 20,000 steps with image augmentations. The number of timesteps is set to 100 for DDPM [25], and the batch size of 512. 

**10-shot Finetuning.** We directly use the model pretrained on OXE datasets to evaluate 10-shot finetuning generalization for real-robot experiments. To ensure consistency with OpenVLA [32], we finetune the network with one observation and one-step prediction. We compare the proposed method with OpenVLA [32] and Octo-base [72] models. Overall, Dita achieves a 63.8% success rate on two-step 

7692 


Figure 5. Quantitative results in real-robot experiments. Each task is manually divided into two sequential steps, except for the last two single-step tasks. In each stacked bar, the light-colored region represents the model’s success rate in the first stage, while the dark-colored region indicates the contribution of second-stage success to the overall success rate. A larger proportion of the dark-colored region signifies a stronger capability of the model in completing long-horizon tasks. Since the open/close drawer tasks are single-step, they are excluded from the calculation of the average success rate. 


Figure 6. Qualitative comparison in real-robot experiments. Failures are highlighted with red circles. For a direct comparison, we initialize the layout consistently across all methods. 

tasks, with the second stage contributing nearly half, as shown in Figure 5. Dita consistently outperforms both Octo and OpenVLA, demonstrating superior performance on all complex tasks. For long-horizon tasks, OpenVLA effectively completes the first task but fails to handle the longhorizon task, such as completely misunderstanding the insert operation. In contrast, Octo performs better with rotation tasks and approaches the second step of the task more effectively. Supplementary materials provide extensive qualitative comparisons. 

**Variance Robustness.** To evaluate the robustness of Dita, we further validate its performance under different variances, including background changes, non-target object arrangements and lighting conditions. As illustrated in Figure 1, it is surprising to find that Dita not only excels in completing complex long-horizon tasks but also demonstrates resilience to a wide range of variations. 

### **5.2. Qualitative Comparison** 

Figure 6 presents a comparison between Dita, diffusion head baseline, Octo [72], and OpenVLA [32] as evaluated in real-robot experiments under 10-shot finetuning setting. According to the visualized comparison, those baseline methods usually fail to grasp the correct position under the 10-shot setting, _e.g_ ., “fail to insert the gap of the box”, “grasp when the gripper is not in the correct grasping position (the hand of cup or teapot)”. Meanwhile, the baseline methods, _e.g_ ., the second raw (pouring water) in Figure 6, sometimes misunderstand the lifting action and get stuck after grasp. In contrast, Dita is able to effectively complete all the complex tasks with extreme 3D rotations. 

## **6. Conclusion** 

We present Dita, an architecture for generalist robot learning that leverages a Transformer-based diffusion model to denoise continuous action sequences through an in-context conditioning mechanism. By harnessing the scalability of Transformers, Dita effectively models diverse robot behaviors across extensive cross-embodiment datasets, enabling robust generalization across multiple simulation benchmarks within a unified framework. Additionally, Dita demonstrates strong few-shot adaptation capabilities, successfully transferring to novel real-world robot setups and long-horizon tasks with minimal in-domain samples. Notably, the model is clean, lightweight, and open-source, and its promising performance—achieved exclusively with a single third-person camera input—underscores its potential as a scalable and flexible solution for generalist policies. 

7693 

## **7. Acknowledgment** 

This work is supported by National Key RD Program of China (NO. 2022ZD0160201). 

## **References** 

- [1] Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quon Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. _arXiv preprint arXiv:2403.01823_ , 2024. 3 

- [2] Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 3 

- [3] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 4788–4795. IEEE, 2024. 3, 5 

- [4] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained imageediting diffusion models. _arXiv preprint arXiv:2310.10639_ , 2023. 5, 6 

- [5] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _pi_ 0: A vision-languageaction flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 2, 3 

- [6] Denis Blessing, Onur Celik, Xiaogang Jia, Moritz Reuss, Maximilian Li, Rudolf Lioutikov, and Gerhard Neumann. Information maximizing curriculum: A curriculum-based approach for learning versatile skills. _Advances in Neural Information Processing Systems_ , 36, 2024. 3 

- [7] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, et al. Robocat: A selfimproving foundation agent for robotic manipulation. _arXiv preprint arXiv:2306.11706_ , 2023. 3 

- [8] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2, 3, 5, 6 

- [9] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 2, 3, 4 

- [10] Tim Brooks, Aleksander Holynski, and Alexei A Efros. Instructpix2pix: Learning to follow image editing instructions. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18392–18402, 2023. 5 

- [11] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, Clarence Ng, Ricky Wang, and Aditya Ramesh. Video generation models as world simulators. 2024. 3 

- [12] Jiahang Cao, Qiang Zhang, Jingkai Sun, Jiaxu Wang, Hao Cheng, Yulin Li, Jun Ma, Yecheng Shao, Wen Zhao, Gang Han, et al. Mamba policy: Towards efficient 3d diffusion policy with hybrid selective state models. _arXiv preprint arXiv:2409.07163_ , 2024. 3 

- [13] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 3 

- [14] Boyuan Chen, Diego Marti Monso, Yilun Du, Max Simchowitz, Russ Tedrake, and Vincent Sitzmann. Diffusion forcing: Next-token prediction meets full-sequence diffusion. _arXiv preprint arXiv:2407.01392_ , 2024. 3, 5 

- [15] Lili Chen, Shikhar Bahl, and Deepak Pathak. Playfusion: Skill acquisition via diffusion from language-annotated play. In _Conference on Robot Learning_ , pages 2012–2029. PMLR, 2023. 3 

- [16] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, et al. Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 24185–24198, 2024. 2 

- [17] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 2, 3, 5, 7 

- [18] Sudeep Dasari, Oier Mees, Sebastian Zhao, Mohan Kumar Srirama, and Sergey Levine. The ingredients for robotic diffusion transformers. _arXiv preprint arXiv:2410.10088_ , 2024. 2, 3 

- [19] Prafulla Dhariwal and Alexander Nichol. Diffusion models beat gans on image synthesis. _Advances in neural information processing systems_ , 34:8780–8794, 2021. 3 

- [20] Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palme: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 3 

- [21] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A robotic dataset for learning diverse skills in one-shot. In _RSS 2023 Workshop on Learning for Task and Motion Planning_ , 2023. 3 

- [22] Jiayuan Gu, Fanbo Xiang, Xuanlin Li, Zhan Ling, Xiqiang Liu, Tongzhou Mu, Yihe Tang, Stone Tao, Xinyue Wei, Yunchao Yao, et al. Maniskill2: A unified benchmark for generalizable manipulation skills. _arXiv preprint arXiv:2302.04659_ , 2023. 4, 6, 2 

- [23] Huy Ha, Pete Florence, and Shuran Song. Scaling up and distilling down: Language-guided robot skill acquisition. In 

7694 

_Conference on Robot Learning_ , pages 3766–3777. PMLR, 2023. 3 

- [24] Kyle B Hatch, Ashwin Balakrishna, Oier Mees, Suraj Nair, Seohong Park, Blake Wulfe, Masha Itkina, Benjamin Eysenbach, Sergey Levine, Thomas Kollar, et al. Ghil-glue: Hierarchical control with filtered subgoal images. _arXiv preprint arXiv:2410.20018_ , 2024. 5, 6 

- [25] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 3, 4, 7 

- [26] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_ , 2021. 7 

- [27] Jiangyong Huang, Silong Yong, Xiaojian Ma, Xiongkun Linghu, Puhao Li, Yan Wang, Qing Li, Song-Chun Zhu, Baoxiong Jia, and Siyuan Huang. An embodied generalist agent in 3d world. _arXiv preprint arXiv:2311.12871_ , 2023. 3 

- [28] Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Peng Gao, Hongsheng Li, Maoqing Yao, and Guanghui Ren. Enerverse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 3 

- [29] Siddharth Karamcheti, Suraj Nair, Annie S Chen, Thomas Kollar, Chelsea Finn, Dorsa Sadigh, and Percy Liang. Language-driven representation learning for robotics. _arXiv preprint arXiv:2302.12766_ , 2023. 3 

- [30] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina Fragkiadaki. 3d diffuser actor: Policy diffusion with 3d scene representations. _arXiv preprint arXiv:2402.10885_ , 2024. 2, 3, 6 

- [31] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 1 

- [32] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 2, 3, 4, 5, 7, 8 

- [33] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pages 19730– 19742. PMLR, 2023. 3 

- [34] Peiyan Li, Hongtao Wu, Yan Huang, Chilam Cheang, Liang Wang, and Tao Kong. Gr-mg: Leveraging partiallyannotated data via multi-modal goal-conditioned policy. _IEEE Robotics and Automation Letters_ , 2025. 3, 6 

- [35] Tianhong Li, Yonglong Tian, He Li, Mingyang Deng, and Kaiming He. Autoregressive image generation without vector quantization. _arXiv preprint arXiv:2406.11838_ , 2024. 5 

- [36] Xinghang Li, Minghuan Liu, Hanbo Zhang, Cunjun Yu, Jie Xu, Hongtao Wu, Chilam Cheang, Ya Jing, Weinan Zhang, 

   - Huaping Liu, et al. Vision-language foundation models as effective robot imitators. _arXiv preprint arXiv:2311.01378_ , 2023. 6 

- [37] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, Sergey Levine, Jiajun Wu, Chelsea Finn, Hao Su, Quan Vuong, and Ted Xiao. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 4, 5 

- [38] Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, Hanbo Zhang, and Huaping Liu. Towards generalist robot policies: What matters in building vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2024. 3 

- [39] Zhixuan Liang, Yao Mu, Hengbo Ma, Masayoshi Tomizuka, Mingyu Ding, and Ping Luo. Skilldiffuser: Interpretable hierarchical planning via skill abstractions in diffusion-based task execution. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 16467– 16476, 2024. 3 

- [40] Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _Advances in Neural Information Processing Systems_ , 36, 2024. 4, 5, 2 

- [41] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning, 2023. 2 

- [42] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 3 

- [43] I Loshchilov. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 4 

- [44] Corey Lynch and Pierre Sermanet. Language conditioned imitation learning over unstructured data. _arXiv preprint arXiv:2005.07648_ , 2020. 3 

- [45] Corey Lynch, Mohi Khansari, Ted Xiao, Vikash Kumar, Jonathan Tompson, Sergey Levine, and Pierre Sermanet. Learning latent plans from play. In _Conference on robot learning_ , pages 1113–1132. PMLR, 2020. 3 

- [46] Oier Mees, Lukas Hermann, and Wolfram Burgard. What matters in language conditioned robotic imitation learning over unstructured data. _IEEE Robotics and Automation Letters_ , 7(4):11205–11212, 2022. 3 

- [47] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for languageconditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3): 7327–7334, 2022. 4, 5 

- [48] Tongzhou Mu, Zhan Ling, Fanbo Xiang, Derek Yang, Xuanlin Li, Stone Tao, Zhiao Huang, Zhiwei Jia, and Hao Su. Maniskill: Generalizable manipulation skill benchmark with large-scale demonstrations. _arXiv preprint arXiv:2107.14483_ , 2021. 6, 2 

- [49] Vivek Myers, Andre Wang He, Kuan Fang, Homer Rich Walke, Philippe Hansen-Estruch, Ching-An Cheng, Mihai Jalobeanu, Andrey Kolobov, Anca Dragan, and Sergey Levine. Goal representations for instruction following: A 

7695 

semi-supervised language interface to control. In _Conference on Robot Learning_ , pages 3894–3908. PMLR, 2023. 3 

- [50] OpenAI. Dall·e: Creating images from text, 2021. 2 

- [51] OpenAI. Chatgpt, 2022. 

- [52] OpenAI. Gpt-4: Multimodal capabilities, 2023. 2 

- [53] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 3, 4 

- [54] Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, Anthony Brohan, et al. Open x- embodiment: Robotic learning datasets and rt-x models. _arXiv preprint arXiv:2310.08864_ , 2023. 2, 3, 4, 5 

- [55] Tim Pearce, Tabish Rashid, Anssi Kanervisto, Dave Bignell, Mingfei Sun, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Ida Momennejad, Katja Hofmann, et al. Imitating human behaviour with diffusion models. _arXiv preprint arXiv:2301.10677_ , 2023. 3 

- [56] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4195–4205, 2023. 3 

- [57] Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , 2018. 3 

- [58] Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 3 

- [59] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 3 

- [60] Moritz Reuss, Maximilian Li, Xiaogang Jia, and Rudolf Lioutikov. Goal-conditioned imitation learning using scorebased diffusion policies. _arXiv preprint arXiv:2304.02532_ , 2023. 3 

- [61] Moritz Reuss, Omer<sup>¨</sup> Erdinc¸ Ya˘gmurlu, Fabian Wenzel, and Rudolf Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. In _First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024_ , 2024. 2, 3, 5 

- [62] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Tim Schmidt. Stable diffusion: Highresolution image synthesis with latent diffusion models, 2021. 2, 5 

- [63] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10684–10695, 2022. 3 

- [64] Paul Maria Scheikl, Nicolas Schreiber, Christoph Haas, Niklas Freymuth, Gerhard Neumann, Rudolf Lioutikov, and Franziska Mathis-Ullrich. Movement primitive diffusion: Learning gentle robotic manipulation of deformable objects. _IEEE Robotics and Automation Letters_ , 2024. 3 

- [65] Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. Gnm: A general navigation model to drive any robot. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 7226–7233. IEEE, 2023. 2, 3 

- [66] Dhruv Shah, Ajay Sridhar, Nitish Dashora, Kyle Stachowicz, Kevin Black, Noriaki Hirose, and Sergey Levine. Vint: A foundation model for visual navigation. _arXiv preprint arXiv:2306.14846_ , 2023. 2, 3 

- [67] Rutav Shah, Roberto Mart´ın-Mart´ın, and Yuke Zhu. Mutex: Learning unified policies from multimodal task specifications. _arXiv preprint arXiv:2309.14320_ , 2023. 3 

- [68] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiveractor: A multi-task transformer for robotic manipulation. In _Conference on Robot Learning_ , pages 785–799. PMLR, 2023. 3 

- [69] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 4 

- [70] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. 2023. 5 

- [71] Ajay Sridhar, Dhruv Shah, Catherine Glossop, and Sergey Levine. Nomad: Goal masked diffusion policies for navigation and exploration. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 63–70. IEEE, 2024. 3 

- [72] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2, 3, 4, 5, 7, 8 

- [73] Yang Tian, Sizhe Yang, Jia Zeng, Ping Wang, Dahua Lin, Hao Dong, and Jiangmiao Pang. Predictive inverse dynamics models are scalable learners for robotic manipulation. _arXiv preprint arXiv:2412.15109_ , 2024. 3 

- [74] Yixiao Wang, Yifei Zhang, Mingxiao Huo, Ran Tian, Xiang Zhang, Yichen Xie, Chenfeng Xu, Pengliang Ji, Wei Zhan, Mingyu Ding, et al. Sparse diffusion policy: A sparse, reusable, and flexible policy for robot learning. _arXiv preprint arXiv:2407.01531_ , 2024. 3 

- [75] Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, et al. One-step diffusion policy: Fast visuomotor policies via diffusion distillation. _arXiv preprint arXiv:2410.21257_ , 2024. 3 

- [76] Junjie Wen, Minjie Zhu, Yichen Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Chengmeng Li, Xiaoyu Liu, Yaxin Peng, Chaomin Shen, et al. Diffusion-vla: Scaling robot foundation models via unified diffusion and autoregression. _arXiv preprint arXiv:2412.03293_ , 2024. 3 

- [77] Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with 

7696 

plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025. 3 

- [78] Hongtao Wu, Ya Jing, Chilam Cheang, Guangzeng Chen, Jiafeng Xu, Xinghang Li, Minghuan Liu, Hang Li, and Tao Kong. Unleashing large-scale video generative pretraining for visual robot manipulation. _arXiv preprint arXiv:2312.13139_ , 2023. 3, 6 

- [79] Zhou Xian, Nikolaos Gkanatsios, Theophile Gervet, and Katerina Fragkiadaki. Unifying diffusion models with action detection transformers for multi-task robotic manipulation. In _7th Annual Conference on Robot Learning_ , page 5, 2023. 3 

- [80] Ted Xiao, Harris Chan, Pierre Sermanet, Ayzaan Wahid, Anthony Brohan, Karol Hausman, Sergey Levine, and Jonathan Tompson. Robotic skill acquisition via instruction augmentation with vision-language models. _arXiv preprint arXiv:2211.11736_ , 2022. 3 

- [81] Jinbo Xing, Menghan Xia, Yong Zhang, Haoxin Chen, Wangbo Yu, Hanyuan Liu, Gongye Liu, Xintao Wang, Ying Shan, and Tien-Tsin Wong. Dynamicrafter: Animating open-domain images with video diffusion priors. In _European Conference on Computer Vision_ , pages 399–417. Springer, 2024. 5 

- [82] Jonathan Yang, Catherine Glossop, Arjun Bhorkar, Dhruv Shah, Quan Vuong, Chelsea Finn, Dorsa Sadigh, and Sergey Levine. Pushing the limits of cross-embodiment learning for manipulation and navigation. _arXiv preprint arXiv:2402.19432_ , 2024. 3 

- [83] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In _ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation_ , 2024. 2, 3 

- [84] Edwin Zhang, Yujie Lu, William Wang, and Amy Zhang. Language control diffusion: Efficiently scaling through space, time, and tasks. _arXiv preprint arXiv:2210.15629_ , 2022. 3 

- [85] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 5 

7697 

