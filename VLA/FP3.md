---
title: "FP3: A 3D Foundation Policy for Robotic Manipulation"
date: "2025-03-11"
authors: "Rujia Yang; Geng Chen; Chuan Wen; Yang Gao"
venue: "ICRA 2026"
url: https://arxiv.org/abs/2503.08950
pdf: https://arxiv.org/pdf/2503.08950
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2503.08950)** / [論文ページ](https://arxiv.org/abs/2503.08950)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# FP3: A 3D Foundation Policy for Robotic Manipulation 

Rujia Yang<sup>*1</sup> , Geng Chen<sup>*2,4</sup><sup>_†_</sup> , Chuan Wen<sup>_‡_1,2,3</sup> , and Yang Gao<sup>_‡_1,2,3</sup> 

> 1IIIS, Tsinghua University, 2Shanghai AI Laboratory, 3Shanghai Qi Zhi Institute, 4UC San Diego 


Fig. 1: **Overview of 3D Foundation Policy (FP3)** , a 1.3B 3D point cloud-based language-visuomotor policy pre-trained on 60k episodes from the DROID dataset [35]. FP3 supports data-efficient fine-tuning for downstream tasks, while demonstrating superior generalizability to unseen environments and novel objects. 

**_Abstract_ —Following its success in natural language processing and computer vision, foundation models that are pre-trained on large-scale multi-task datasets have also shown great potential in robotics. However, most existing robot foundation models rely solely on 2D image observations, ignoring 3D geometric information, which is essential for robots to perceive and reason about the 3D world. In this paper, we introduce FP3, a first** 

> _∗_ denotes equal contribution. _‡_ denotes equal advising. _†_ : work done during the internship at Shanghai AI Laboratory 

**large-scale 3D foundation policy model for robotic manipulation. FP3 builds on a scalable diffusion transformer architecture and is pre-trained on 60k trajectories with point cloud observations. With the model design and diverse pre-training data, FP3 can be efficiently fine-tuned for downstream tasks while exhibiting strong generalization capabilities. Experiments on real robots demonstrate that with only 80 demonstrations, FP3 is able to learn a new task with over 90% success rates in novel environments with unseen objects, significantly surpassing existing robot foundation models. Visualizations and code are available at: FP3.** 

## I. INTRODUCTION 

Learning-based policies have shown great effectiveness in robotic manipulation [6, 80, 12, 75, 36, 3]. However, these learned policies often show limited or even zero generalization capability to unseen scenarios, new objects, and distractors [66]. Additionally, most current methods are trained on single or few tasks[12, 75], requiring a relatively large amount of expert demonstrations (usually about 200 episodes) to learn a new task. In contrast, natural language processing (NLP) and computer vision (CV) have achieved remarkable success in developing foundation models that are trained on largescale data and diverse tasks, enabling them to generalize to arbitrary scenarios in the wild. Therefore, building a similar foundation model in robotic manipulation that can generalize to novel objects, scenes, and tasks becomes a promising topic [36, 39, 3]. 

Towards this goal of policy foundation models, there have been some initial attempts at vision-language-action (VLA) models [80, 36, 3], which build upon the vision-language models (VLM) trained on internet-scale data of vision and language to inherit the commonsense knowledge and finetune the VLMs on large-scale robotics datasets [46, 35]. In the meanwhile, works such as RDT [39] try to scale up diffusion models to build foundation policies. Despite significant progress, their generalizability remains limited when confronted with novel tasks, objects, scenes, and camera views, etc. 

One potential limitation of current policy foundation models is their exclusive reliance on 2D image observations, lacking 3D observation inputs. However, 3D geometric information is significant for perceiving 3D environments and reasoning about spatial relationships [78, 72, 70, 63]. There have been works showing that 3D representations can improve the sample efficiency and generalizability of robotic manipulation policies [54, 70, 33, 72]. Among all the 3D representations such as RGB-D images, point clouds, voxels, and 3D Gaussians [34], point clouds are found to be the most effective [70]. 

In this work, we introduce 3D Foundation Policy (FP3), the first 3D point cloud-based language-visuomotor policy foundation model for robotic manipulation that exhibits strong generalizability and sample efficiency. To extract rich semantic and geometric representation from 3D point cloud observation, FP3 adopts a pre-trained large-scale point cloud encoder Uni3D [77]. We further leverage an encoder-decoder Diffusion Transformer (DiT) architecture to integrate the point cloud representations, language embedding, and proprioception for denoising the actions. 

With the proposed policy architecture, we employ a pretraining&post-training recipe for FP3, mirroring the common practice in large language models (LLMs) [1, 57] where the model is pre-trained on large-scale diverse corpus and finetuned on curated task-specific data to adapt for downstream tasks. We first pre-train FP3 on the large-scale robotic manipulation dataset DROID [35] which contains 76k demonstration 

trajectories or 350h of interaction data from 564 scenes and 86 tasks. We then collect a small amount of high-quality teleoperation data for several tasks and fine-tune FP3. The result indicates that our model can efficiently master a new task with only 80 post-training trajectories and is capable of zeroshot generalization to both novel objects and environments with about 90% success rate. In contrast, strong baselines like DP3 [70] and OpenVLA [36] almost completely fail in this setting. Due to the advantages of 3D representation, FP3 is also robust to background variations, lighting conditions, camera angles, and distractors. Finally, we conduct ablation studies to demonstrate that the 3D representation, data scaling, and model scaling all contribute to the model’s superior performance. 

We summarize our main contributions as follows: 

- 1) We propose a novel diffusion-based 3D robot policy architecture, FP3. 

- 2) We pre-train FP3 on large-scale robotic manipulation data with 3D observation, establishing a 1B-parameter 3D policy foundation model. 

- 3) We collect data on several new tasks and demonstrate the efficient and generalizable fine-tuning of FP3, achieving around 60% in-domain and 80% in-the-wild performance improvement on average over strong baselines with only 2-hour and single-GPU finetuning. 

## II. RELATED WORK 

## _A. Foundation Models in Robotics_ 

Similar to the cases in natural language processing and computer vision, foundation models have already been widely used in multiple aspects of robotics, including representation learning [44, 42, 64, 67], high-level task planning [7, 24], training-free robotic manipulation [28, 26, 27], etc. In this work, we concentrate on policy foundation models in robotics, which also often refer to multi-task ”generalist” robot policies [6, 80, 36, 58, 39, 3] trained on large-scale robot datasets [46, 60, 35, 17]. A significant subset of policy foundation models consists of autoregressive vision-language-action (VLA) models like RT-2 [80] and OpenVLA [36], which directly fine-tune pre-trained large vision-language models to predict actions by treating discretized actions as language tokens. Recently, RDT [39] scales up a diffusion transformer [47] to build a foundation model for bimanual manipulation. Another recent work _π_ 0 [3] investigates the combination of a pre-trained VLM backbone with diffusion (flow matching [38]) models for robot control. Our work is most similar to RDT in terms of architecture, as both build upon diffusion transformers, but there are key differences, such as conditioning blocks. RDT employs cross attention blocks, while we opt for adaLN blocks [47, 15] for stabilizing training. 

In addition to architecture, a key difference between these approaches and FP3 is the observation modality. Unlike these works, which all take 2D image observation as input, our work utilizes 3D point cloud observations to enhance the perception of 3D geometric information and reasoning about 

spatial relationships, introducing the first policy foundation model with 3D representations to our knowledge. 

## _B. Robotic Manipulation with 3D representations_ 

Compared to 2D images, 3D representations such as RGBD images, point clouds, and voxels contain richer geometric information and have thus been widely used in robotic manipulation [54, 70, 19]. Kite [56] directly leverages the RGB-D observation for semantic manipulation. Other works [11, 68, 70, 61] reconstruct point clouds from RGB-D images and process them using a point cloud encoder for manipulation. Voxelizing the point clouds for perception is also a viable solution [30, 54, 25]. Another set of works[18, 65, 33, 72, 73] lifts 2D image features to 3D space to benefit from both semantic and geometric information. There have also been attempts in combining implicit or explicit 3D reconstruction (NeRF [43], 3D gaussians [34]) with robotic manipulation [69, 29, 14, 76, 41]. In this work, we choose the point cloud as the 3D representation as it is found to be more effective than other representations in DP3 [70]. 

Despite the differences in representation, all the aforementioned methods consist of small networks trained on a limited number of tasks. FP3 differs from these works in several ways: it is a foundation model trained on a large multi-task dataset, it scales up the point cloud encoder to 300M parameters and the whole network to 1.3B parameters, and it supports efficient and generalizable fine-tuning for new tasks. 

## _C. Diffusion models in Robotics_ 

Diffusion models have achieved great success in image generation [21, 55, 53] and video generation [22, 4, 8, 20] by modeling complex high-dimensional continuous distributions through progressive denoising. Due to their remarkable expressiveness, diffusion models have also been applied across various fields in robotics, including reinforcement learning [62, 2, 10], imitation learning [12, 70, 52, 39, 58, 3], and motion planning [31, 59, 9]. Our work focuses on “Diffusion Policies” [12], which refers to methods that directly employ conditional diffusion models as visuomotor policy models for imitation learning. Most closely related to our work is RDT [39], a diffusion foundation model for manipulation. A key distinction between our work and RDT is that our FP3 model leverages 3D point cloud representations to achieve improved data efficiency and generalizability. 

## III. METHOD 

We introduce the 3D Foundation Policy (FP3) model for generalist robotic manipulation, achieving high data efficiency and generalization capability. FP3 is a 1.3B encoder-decoder transformer network following a two-stage pre-training and post-training recipe. We first provide the detailed architecture and key design decisions of FP3 in Section III-A. Then we describe the pre-training and post-training procedures in Section III-B and Section III-C, respectively. 

## _A. FP3 model_ 

At its core, FP3 is a diffusion-based policy model similar to [12, 39]. It takes the 3D point cloud observation, language, and robot proprioceptive state as input and predicts action chunks of future actions. Formally, we formalize the problem of language-conditioned visuomotor control as modeling the distribution _p_ ( _At|ot_ ), where **o** _t_ = [ **P**<sup>1</sup> _t_<sup>_, ...,_</sup><sup>**P**</sup><sup>_n_</sup> _t_<sup>_, ℓt,_</sup><sup>**q**</sup><sup>_t_] is the ob-</sup> servation at time _t_ including point cloud observation **P**<sup>_i_</sup> _t_<sup>from</sup> the _i_<sup>_th_</sup> camera (including historical observation), language instruction _ℓt_ and proprioceptive information **q** _t_ and _At_ = [ _at, at_ +1 _, ..., at_ + _H−_ 1] denotes the predicted action chunk. We train a denoising diffusion probabilistic model (DDPM) [21] to approximate the conditional distribution and use the denoising diffusion implicit model (DDIM) [55] method to accelerate inference. 

Now we describe the detailed structure of FP3 model, including the encoding of multi-modal inputs and the transformer-based encoder-decoder architecture. 

**Encoding of multi-modal inputs.** To process the multimodal input, we encode the input signals into a unified token space with the same dimensions as follows: 

- **Point cloud observations** contain rich semantic and geometric information and are found to be more suitable for policy learning compared to other 3D representations [70]. Therefore, we consider using point cloud as the 3D representation in FP3. Current point cloud-based robot policies [70, 61, 73] typically use sparse point cloud and small networks such as PointNet++ [49] and PointNeXt [50] to encode the points into embeddings. However, pre-trained large-scale foundation vision encoders have demonstrated a performance advantage over small encoders in image-based policies [13, 37]. Consequently, we increase the number of input points to 4000 for each view and employ a 300M-parameter point cloud encoder Uni3D ViT [77] that is pre-trained to align the 3D point cloud features with the image-text aligned features to obtain the point cloud embeddings. For the third-personview and the wrist-view point clouds, we use separate encoders since their point distributions might be greatly different. Following [37], we choose to fine-tune the weights of Uni3D ViTs during policy training. 

- **Language instructions** are simply encoded with a CLIP [51] model to align with Uni3D. The weights are fixed during training since the language embeddings are already well-trained. 

- **Low-dimensional inputs** including robot proprioceptive state and noise levels are processed with two-layer MLPs, respectively. 

**Encoder-decoder structure.** Since Diffusion Transformers have shown great scalability in image generation [47, 16] and policy learning [79, 15], we adopt the transformer architecture and scale it up for FP3. To better fuse the point cloud, language, and proprioceptive state embeddings, we utilize a Transformer Encoder-Decoder architecture similar to [75, 74, 52, 15]. Specifically, FP3 first feeds all the embeddings into 


Fig. 2: **FP3 architecture.** Each camera view’s point cloud observation **P**<sup>_i_</sup> _t_<sup>(withhistorylengthoftwo)isencodedwitha</sup> Uni3D ViT-L [77] encoder. The language instruction _ℓt_ is embedded with a frozen CLIP [51] model. The Transformer encoder fuses multi-modal input embeddings to latent tokens, while the Transformer decoder takes in the noise actions and leverages adaLN [47, 5, 32] blocks to integrate the latent tokens generated by the encoder, predicting denoised action chunks. 

a transformer encoder, producing a sequence of informative latent tokens. 

The diffusion denoiser of FP3 is a Transformer decoder that denoises the action chunks from noise with temporal causal masking following [79]. To infuse the latent tokens with multimodal information into the denoiser, FP3 adopts the adaptive Layer-Norm (adaLN) module for conditioning, which has been found to be essential for implementing diffusion training in image generation [47, 16] and policy learning [79, 15]. 

## _B. Pre-training_ 

**Pre-training data.** To build a 3D policy foundation model, we need to train our model on large-scale 3D robotic manipulation datasets. However, most existing large-scale robot datasets such as the Open X-Embodiment dataset (OXE, [46]) are mainly 2D-only. Thus, in this work, we pre-train FP3 with the DROID dataset [35], which includes 86 tasks and 76k demonstrations and provides depth observation data. We finally use 60k demonstrations from DROID to pre-train FP3. 

**Data pre-processing.** While DROID uses three cameras for data collection, we only use two of them including one thirdview camera and one wrist-view camera in FP3 for convenience. We use the RGB image and the depth map to recover the 3D point cloud for each camera and transform the two point clouds to the same world frame. As we only care about the operated object, we cropped the points outside a 1-meter box to remove redundant points. Further, we downsample each point cloud by farthest point sampling (FPS, [48]) to 4000 points to facilitate model training while retaining sufficient information. We preserve the color channels of each point to enable further experiments conditioned on colors. 

**Pre-training details.** Following prior works [36, 37] which found that freezing pre-trained vision encoders may harm the policy performance, we fine-tune the Uni3D ViT encoder during pre-training. We also randomly drop some points during 

training for augmentation, and the dropout rate is randomly selected from 0 to 0.8. 

We use the AdamW optimizer [40] with a cosine learning rate schedule. The weight decay is set to 0.1, and gradient clipping is set to 1.0. The FP3 base model is pre-trained for 3M steps with a batch size of 128 using 8 NVIDIA A800 GPUs, which takes about 48 hours. Fine-tuning the same model on a single NVIDIA A800 GPU takes approximately 2 hours and can be further sped up with multi-GPU training. 

To handle the partial observation, we stack 2 frames as input, including 1 step observation history, to compensate for the missing dynamic information of the robot. 

## _C. Post-training_ 

After obtaining the pre-trained base model, we further employ a post-training process using a small amount of highquality data to adapt the model to certain tasks, which aligns with most modern LLM practice [1, 57]. Different from the fine-tuning settings adopted in most existing robot foundation models in which they focus on either fine-tuning the model to adapt to new robot setups [36, 58] or learning new tasks in a fixed environment [39, 3], our goal is to fine-tune our model to _solve specific tasks on any object, in any environment_ . 

To achieve this goal, we further collect data for each downstream task in our robot setup. Taking the lesson from Lin et al. [37], we aim to enhance the diversity of environments and objects rather than merely increasing the number of demonstrations in the same scenario. Specifically, for each task, we collect 10 teleoperation demonstrations in each of 8 environments using 8 unique objects, i.e., 80 demonstrations in total. We then fine-tune the base model on this data using the parameter-efficient fine-tuning strategy LoRA [23]. Thanks to the effective initialization from pre-training, this small amount of fine-tuning data enables zero-shot deployment to novel environments and objects. We will discuss the tasks and results in detail in Section IV. 

## IV. EXPERIMENTS 

We conduct experiments on real robots for four downstream tasks to investigate the following questions: 

- 1) Can FP3 be efficiently fine-tuned for new tasks? 

- 2) How well does the fine-tuned FP3 generalize to unseen objects and scenes compared to the existing imitation learning (foundation) policies? 

- 3) How robust is FP3 to the environment perturbations, such as lighting, camera views, distractors, _etc._ ? 

- 4) Can FP3 correctly execute the corresponding tasks following the language instruction? 

## _A. Experimental Setups_ 

**Real robot setup.** As we pre-train our FP3 model on the DROID dataset, we also build a real robot setup similar to DROID for evaluating downstream tasks. This setup features a Franka Emika Panda robot arm equipped with a Robotiq gripper, mounted on a movable desk. For point cloud observation, we utilize one ZED mini camera in wrist view and one ZED 2 camera in third-person view. To collect data, we employ a Meta Quest 2 VR headset to teleoperate the robot. We record the absolute Cartesian Space Control as the action space for policy training and deployment. More details are provided in the Appendix. 


Fig. 3: **Task illustrations.** We evaluate our model on four downstream tasks: Fold Towel, Clean Table, Stand up Cup, and Pour Water. 

**Tasks.** We choose four downstream tasks to evaluate our model and the baselines: 

- Fold Towel: Fold a long towel from right to left on a flat surface. 

- Clean Table: Pick up a crumpled piece of paper and put it in the bucket. 

- Stand up Cup: Stand a cup lying on a flat surface upright. 

- Pour Water: Pick up a water bottle, pour the water from the water bottle into a cup, then place the water bottle on a coaster. 

Figure 3 illustrates the process of these four tasks. Further details are provided in the Appendix. **Baselines.** In order to comprehensively evaluate FP3, we carefully select three baselines: 

- Diffusion Policy (DP) [12]: a classic diffusion-based imitation learning policy with 2D image observation. 

- DP3 [70]: an alternative version of DP which changes the 2D image observation to 3D point cloud and designs a lightweight encoder to encode the point cloud. 

- OpenVLA [36]: a most widely-used image-based VisionLanguage-Action (VLA) model. 

These three baselines each represent a small 2D policy, a small 3D policy, and a large 2D foundational policy. For DP and DP3, we add a language-conditioning module in the same manner as FP3 to fuse language instructions. 

**Metrics.** We report the success rate as our metric. Results in Table I are averaged over 20 evaluation trials. 

## _B. Efficient and generalizable fine-tuning for new tasks_ 

We first evaluate FP3’s capability to learn new tasks efficiently. We collect only 10 demonstrations per environmentobject pair for 8 pairs to obtain 80 demonstrations in total for each task. For DP and DP3, we use the demonstrations to train the policies, while for OpenVLA and our FP3, we follow the pre-training and post-training recipe to fine-tune the base models for each task. Additionally, we train FP3 from scratch to validate the necessity of pre-training. 

For each task, we not only evaluate all the policies in four in-domain environments with seen objects, but also deploy them zero-shot in four out-of-domain environments with unseen objects, which is a huge challenge for the model’s generalizability. 

**In-domain Performance.** Results in Table I show that in in-domain experiments, with only 10 demonstrations per scene, DP and DP3 can somewhat handle easier tasks, even though the success rate is below 50% in most cases; however, they almost completely fail in the more difficult task Pour Water. And OpenVLA struggles to perform any task, likely due to the lack of action chunking. In contrast, thanks to pre-training and 3D representation, FP3 efficiently learns all tasks with a success rate exceeding 90%. Qualitatively, we find that the failures of all baseline algorithms are mainly due to issues in the details, such as not being precise enough when attempting to grasp objects, which causes the object to be pushed away, or the bottle opening being off-center when pouring water, etc. In contrast, due to its large number of parameters and extensive pre-training, our FP3 policy can better predict complex target actions. The actions predicted by the FP3 policy are significantly smoother and more precise, leading to a notably higher success rate compared to the strong baselines. 

**In-the-Wild Performance.** We further move the robot arm to novel environments and evaluate the policies with unseen objects. In this challenging setting, we observe that all baseline policies without pre-training, including FP3-Scratch, often fail to recognize the target objects, resulting in near-zero performance as shown in Figure 4. In contrast, FP3 rarely encounters such situations and consistently performs well in all scenarios and tasks, achieving an average success rate of over 80%, which devastates all the baselines. We attribute the superior performance to our large-scale pre-training, as the pre-training data encompasses a wide variety of scenes 

TABLE I: **Post-training Evaluation.** We fine-tune FP3 and baseline methods on 80 demonstrations from 8 environments and evaluate them on four in-domain environments with seen objects and four in-the-wild environments with unseen objects, conducting 5 trials for each. FP3 significantly outperforms other policies both in domain and in the wild. 

||Fold|Towel|Clean|Table|Stand|up Cup|Pour|Water|Ave|rage|
|---|---|---|---|---|---|---|---|---|---|---|
||In-domain|In-the-wild|In-domain|In-the-wild|In-domain|In-the-wild|In-domain|In-the-wild|In-domain|In-the-wild|
|DP|20|0|75|5|45|0|5|0|36.25|1.25|
|DP3|20|0|25|10|45|0|0|0|22.50|2.50|
|OpenVLA|5|0|15|5|15|10|0|0|7.50|3.75|
|FP3-Scratch|35|5|35|0|15|0|35|0|30.00|1.25|
|FP3 (**ours**)|**90**|**85**|**100**|**95**|**95**|**75**|**95**|**75**|**95.00**|**82.50**|


and objects, greatly enhancing the robustness of the policy. Furthermore, the point cloud observation is also a crucial factor, enabling better capture of geometric information, which is essential for cross-domain generalization. 

**Failure Analysis of Baselines.** It is worth noting that in all cases, OpenVLA performs poorly, with the primary failure modes being its tendency to get stuck at specific positions and its inability to interact accurately with objects. The issue of getting stuck may stem from OpenVLA’s lack of action chunking and observation history. The failure to interact precisely might be because OpenVLA uses only third-personview observation, which offers a restricted field of view. 

Another interesting issue is the policy’s response after an initial failure attempt. Sometimes, the policy fails in its first attempt, as seen in the Clean Table task where it fails to grasp the crumpled paper and ends up grabbing nothing. In such cases, we observe that only OpenVLA and FP3 make reasonable subsequent attempts, while DP, DP3, and FP3Scratch tend to get stuck and simply wobble around the area after failure, unable to have a try again. This phenomenon happens probably because the fine-tuning data is limited, thus the policies without pre-training can fall into an out-of-distribution state after the first failure, and hence fail to output reasonable behaviors. Conversely, Large-scale pre-training with diverse tasks and objects in FP3 addresses this issue. 

## _C. More experiments on generalization_ 

Having demonstrated the efficient adaptation to new tasks and remarkable generalizability to novel objects and environments of FP3, we conduct more comprehensive experiments on FP3’s generalizability to different environments and robot setups using the Clean Table task. Figure 5 demonstrates the results and visualizations. 

**Generalization to different object appearances, backgrounds, and lighting conditions.** Conventional image-based policy networks are sensitive to visual variations. Therefore, we systematically alter one aspect of the in-domain environment: object appearance, background texture, or lighting condition, to evaluate the policies. The results indicate that the image-based DP experiences a performance decline compared to the in-domain results, particularly with modified color and background. In contrast, DP3’s performance in lighting and object color generalization remains stable, as it eliminates the 

color channels and relies solely on point positions. However, it is still limited by in-domain performance. With the benefits of pre-training initialization and 3D geometry understanding, FP3 surpasses the baselines. Qualitatively, DP and DP3 occasionally struggle to accurately recognize objects or estimate their positions, while FP3 consistently performs well. 

**Generalization to new camera views.** Camera view variations have also been a major challenge for image-based policies. Therefore, we adjust the camera view by approximately 30 degrees from the training data to evaluate the robustness of the policies. Once again, DP completely fails in this scenario, and DP3 is constrained by its in-domain performance, while FP3 maintains its high performance since the point cloud is consistently converted to the same coordinates as long as the camera is properly calibrated. 

**Generalization to distractors.** We also try putting random distractors around the target object to assess the robustness of these policies. In such settings, we find that the policies may attempt to grasp interfering objects. This issue occurs in all methods, including FP3, yet FP3’s performance remains the highest and most stable. 

## _D. Instruction following_ 

Since FP3 is a language-conditioned visuomotor policy, it’s also important to evaluate its capability to execute tasks following the language command. Hence we fine-tune FP3 and the baselines in a multi-task setting using data from all tasks and evaluate them by providing different language instructions in the same initial state. Figure 6 demonstrates that FP3 can execute tasks according to different language commands within the same starting context, while the baseline methods either fail to complete the task or are disrupted by the target objects of other tasks. 

## _E. Ablations_ 

We finally do ablation studies on the observation choice, model size, and pre-training data size. We consider the following variants of FP3: 

- FP3-Base reduces the transformer size of both the encoder and decoder in FP3 from ViT-Large to ViT-Base, decreasing the total parameters from 1.3B to 365M. 

- FP3-Base-30k further reduces the pre-training data of FP3-Base from 60k to 30k demonstrations. 


Fig. 4: **Visualizations of post-training environments and in-the-wild evaluations.** The green boxes represent successful steps, while the red boxes represent failed ones. FP3 generalize well to all unseen environments and new objects, while Diffusion Policy often fails to recognize the target object or misses the target position. 


Fig. 5: **Generalization evaluation.** We evaluate FP3 and baseline policies on a diverse set of tasks, covering different axes of generalization, including lighting, camera view, distractor, object and background. FP3 achieves outstanding performance in all generalization evaluation settings. 


Fig. 6: **Instruction following evaluation.** We evaluate FP3 and baseline policies in the same initial state with different language instructions. FP3 can perfectly follow the instructions to execute the correct tasks rather than simply memorize the training distribution. 

- FP3-Base-Image converts the point cloud observations to image observations on FP3-Base and employs a DINOv2 [45] model to encode the images. 

- FP3-Scratch is the FP3 model trained from scratch without any pre-training. 

Table II presents the results of each variant on the Clean Table task. FP3-Scratch exhibits poor performance both in domain and in the wild, indicating the importance of pretraining. FP3-Base-Image’s performance aligns with FP3-Base in domain, but there is a huge performance drop in the wild, highlighting the effectiveness of 3D point cloud representation. FP3-Base and FP3-Base-30k demonstrate similar performance, both lower than our final FP3. More challenging tasks and additional data points are likely required to draw more definitive conclusions about the precise scaling law of pre-training. 

TABLE II: **Ablation study.** We achieve the best performance when using 3D point cloud input, a larger model, and largerscale pre-training data. 

|||Clean|Table|
|---|---|---|---|
||In-domain||In-the-wild|
|FP3-Scratch|35||0|
|FP3-Base-Image|90||55|
|FP3-Base|95||90|
|FP3-Base-30k|95||90|
|FP3 (**ours**)|**100**||**95**|


## V. LIMITATIONS 

While FP3 shows strong performance as a policy foundation model, it still has several limitations. One limitation is that although FP3 enables efficient and generalizable downstream fine-tuning, the base model exhibits limited zero-shot performance. One possible reason is that the pre-training dataset DROID is still not large enough compared to other 2D robotics datasets like OXE. Future work can consider collecting larger 3D robotics datasets for pre-training. Another limitation is that FP3 incorporates language conditioning through a simple CLIP embedding, which is insufficient to represent complicated and dynamic information. Combining diffusion-based FP3 with VLM to build a VLA model like _π_ 0 [3] seems a promising future direction. Additionally, FP3 does not leverage the robust pre-trained 2D vision encoders like DINOV2 [45] and SigLIP [71]. There is huge potential in merging 3D point cloud features with 2D image features or lifting the 2D features to 3D space. We leave these explorations for future work. 

## VI. CONCLUSION 

In this work, we present the 3D Foundation Policy (FP3), a large-scale Diffusion Transformer-based policy with 3D point cloud input. We pre-train FP3 on 60k episodes of robotic manipulation data and subsequently fine-tune it for downstream tasks. Through extensive experiments, we demonstrate that FP3 serves as an outstanding policy initialization for dataefficient and generalizable fine-tuning for new tasks. With only 80 demonstrations, FP3 can learn a new task with over 90% 

success rates in novel environments with unseen objects, significantly outperforming existing robot policies. We hope that our work will pave the way for more exciting advancements in robot foundation models utilizing 3D representations. 

## VII. ACKNOWLEDGMENT 

This work is supported by the National Natural Science Foundation of China (62176135), National Key R&D Program of China (2022ZD0161700), Shanghai Qi Zhi Institute Innovation Program SQZ202306 and the Tsinghua University Dushi Program. 

We would like to express our gratitude to Tong Zhang and Yingdong Hu for their help with the robot hardware setup.. We also appreciate the insightful discussions and feedback from Jiacheng You, Shengjie Wang and Chengbo Yuan. 

## REFERENCES 

- [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. <u>arXiv preprint arXiv:2303.08774,</u> 2023. 

- [2] Anurag Ajay, Yilun Du, Abhi Gupta, Joshua B Tenenbaum, Tommi S Jaakkola, and Pulkit Agrawal. Is conditional generative modeling all you need for decision making? In <u>The Eleventh International Conference on Learning Representations.</u> 

- [3] Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A visionlanguage-action flow model for general robot control. <u>arXiv preprint arXiv:2410.24164,</u> 2024. 

- [4] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, et al. Stable video diffusion: Scaling latent video diffusion models to large datasets. <u>arXiv preprint arXiv:2311.15127, 2023.</u> 

- [5] Andrew Brock, Jeff Donahue, and Karen Simonyan. Large scale gan training for high fidelity natural image synthesis. In <u>International Conference on Learning Representations,</u> 2018. 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. <u>arXiv preprint arXiv:2212.06817,</u> 2022. 

- [7] Anthony Brohan, Yevgen Chebotar, Chelsea Finn, Karol Hausman, Alexander Herzog, Daniel Ho, Julian Ibarz, Alex Irpan, Eric Jang, Ryan Julian, et al. Do as i can, not as i say: Grounding language in robotic affordances. In <u>Conference on robot learning, pages 287–318. PMLR,</u> 2023. 

- [8] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, Clarence Ng, Ricky Wang, and Aditya Ramesh. Video generation models as world 

simulators. 2024. URL https://openai.com/research/ video-generation-models-as-world-simulators. 

- [9] J. Carvalho, A.T. Le, M. Baierl, D. Koert, and J. Peters. Motion planning diffusion: Learning and planning of robot motions with diffusion models. In <u>IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS),</u> 2023. 

- [10] Huayu Chen, Cheng Lu, Chengyang Ying, Hang Su, and Jun Zhu. Offline reinforcement learning via highfidelity generative behavior modeling. In <u>The Eleventh International Conference on Learning Representations.</u> 

- [11] Shizhe Chen, Ricardo Garcia Pinel, Cordelia Schmid, and Ivan Laptev. Polarnet: 3d point clouds for languageguided robotic manipulation. In <u>Conference on Robot Learning,</u> pages 1761–1781. PMLR, 2023. 

- [12] Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. <u>The International Journal of Robotics Research,</u> page 02783649241273668, 2023. 

- [13] Cheng Chi, Zhenjia Xu, Chuer Pan, Eric Cousineau, Benjamin Burchfiel, Siyuan Feng, Russ Tedrake, and Shuran Song. Universal manipulation interface: In-thewild robot teaching without in-the-wild robots. <u>arXiv preprint arXiv:2402.10329,</u> 2024. 

- [14] Qiyu Dai, Yan Zhu, Yiran Geng, Ciyu Ruan, Jiazhao Zhang, and He Wang. Graspnerf: Multiview-based 6- dof grasp detection for transparent and specular objects using generalizable nerf. In <u>2023 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 1757–1763. IEEE, 2023. 

- [15] Sudeep Dasari, Oier Mees, Sebastian Zhao, Mohan Kumar Srirama, and Sergey Levine. The ingredients for robotic diffusion transformers. <u>arXiv preprint arXiv:2410.10088,</u> 2024. 

- [16] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas M¨uller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for high-resolution image synthesis. In <u>Forty-first International Conference on Machine Learning,</u> 2024. 

- [17] Hao-Shu Fang, Hongjie Fang, Zhenyu Tang, Jirong Liu, Junbo Wang, Haoyi Zhu, and Cewu Lu. Rh20t: A robotic dataset for learning diverse skills in one-shot. In <u>RSS 2023 Workshop on Learning for Task and Motion Planning,</u> 2023. 

- [18] Theophile Gervet, Zhou Xian, Nikolaos Gkanatsios, and Katerina Fragkiadaki. Act3d: 3d feature field transformers for multi-task robotic manipulation. In <u>7th Annual Conference on Robot Learning,</u> 2023. 

- [19] Ankit Goyal, Jie Xu, Yijie Guo, Valts Blukis, Yu-Wei Chao, and Dieter Fox. Rvt: Robotic view transformer for 3d object manipulation. In <u>Conference on Robot Learning,</u> pages 694–710. PMLR, 2023. 

- [20] Xianfan Gu, Chuan Wen, Weirui Ye, Jiaming Song, and Yang Gao. Seer: Language instructed video prediction 

with latent diffusion models. In <u>The Twelfth International Conference on Learning Representations,</u> 2024. URL https://openreview.net/forum?id=qHGgNyQk31. 

- [21] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. <u>Advances in neural information processing systems,</u> 33:6840–6851, 2020. 

- [22] Jonathan Ho, Tim Salimans, Alexey Gritsenko, William Chan, Mohammad Norouzi, and David J Fleet. Video diffusion models. <u>Advances in Neural Information Processing Systems,</u> 35:8633–8646, 2022. 

- [23] Edward J Hu, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. In <u>International Conference on Learning Representations,</u> . 

- [24] Yingdong Hu, Fanqi Lin, Tong Zhang, Li Yi, and Yang Gao. Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning. In <u>First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024,</u> . 

- [25] Haojie Huang, Owen Howell, Xupeng Zhu, Dian Wang, Robin Walters, and Robert Platt. Fourier transporter: Biequivariant robotic manipulation in 3d. <u>arXiv preprint arXiv:2401.12046,</u> 2024. 

- [26] Haoxu Huang, Fanqi Lin, Yingdong Hu, Shengjie Wang, and Yang Gao. Copa: General robotic manipulation through spatial constraints of parts with foundation models. In <u>First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024,</u> . 

- [27] Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. In <u>8th Annual Conference on Robot Learning,</u> . 

- [28] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li Fei-Fei. Voxposer: Composable 3d value maps for robotic manipulation with language models. In <u>Conference on Robot Learning,</u> pages 540– 562. PMLR, 2023. 

- [29] Jeffrey Ichnowski, Yahav Avigal, Justin Kerr, and Ken Goldberg. Dex-nerf: Using a neural radiance field to grasp transparent objects. In <u>5th Annual Conference on Robot Learning.</u> 

- [30] Stephen James, Kentaro Wada, Tristan Laidlow, and Andrew J Davison. Coarse-to-fine q-attention: Efficient learning for visual robotic manipulation via discretisation. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 13739–</u> 13748, 2022. 

- [31] Michael Janner, Yilun Du, Joshua Tenenbaum, and Sergey Levine. Planning with diffusion for flexible behavior synthesis. In <u>International Conference on Machine Learning,</u> pages 9902–9915. PMLR, 2022. 

- [32] Tero Karras, Samuli Laine, and Timo Aila. A stylebased generator architecture for generative adversarial networks. <u>IEEE Transactions on Pattern Analysis and Machine Intelligence,</u> 43(12):4217–4228, 2021. 

- [33] Tsung-Wei Ke, Nikolaos Gkanatsios, and Katerina 

Fragkiadaki. 3d diffuser actor: Policy diffusion with 3d scene representations. In <u>First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024.</u> 

- [34] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. <u>ACM Trans. Graph., 42(4):139–</u> 1, 2023. 

- [35] Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. <u>CoRR,</u> 2024. 

- [36] Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. <u>arXiv preprint arXiv:2406.09246,</u> 2024. 

- [37] Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data scaling laws in imitation learning for robotic manipulation. <u>arXiv preprint arXiv:2410.18647,</u> 2024. 

- [38] Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In <u>The Eleventh International Conference on Learning Representations.</u> 

- [39] Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. <u>arXiv preprint arXiv:2410.07864,</u> 2024. 

- [40] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In <u>International Conference on Learning Representations.</u> 

- [41] Guanxing Lu, Shiyi Zhang, Ziwei Wang, Changliu Liu, Jiwen Lu, and Yansong Tang. Manigaussian: Dynamic gaussian splatting for multi-task robotic manipulation. In <u>European Conference on Computer Vision,</u> pages 349– 366. Springer, 2024. 

- [42] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. Vip: Towards universal visual reward and representation via value-implicit pre-training. In <u>The Eleventh International Conference on Learning Representations.</u> 

- [43] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. <u>Communications of the ACM, 65(1):99–</u> 106, 2021. 

- [44] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3m: A universal visual representation for robot manipulation. In <u>6th Annual Conference on Robot Learning.</u> 

- [45] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy V Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel HAZIZA, Francisco Massa, Alaaeldin 

El-Nouby, et al. Dinov2: Learning robust visual features without supervision. <u>Transactions on Machine Learning Research.</u> 

- [46] Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 6892–6903. IEEE, 2024. 

- [47] William Peebles and Saining Xie. Scalable diffusion models with transformers. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision,</u> pages 4195–4205, 2023. 

- [48] Charles R Qi, Hao Su, Kaichun Mo, and Leonidas J Guibas. Pointnet: Deep learning on point sets for 3d classification and segmentation. In <u>Proceedings of the IEEE conference on computer vision and pattern recognition,</u> pages 652–660, 2017. 

- [49] Charles Ruizhongtai Qi, Li Yi, Hao Su, and Leonidas J Guibas. Pointnet++: Deep hierarchical feature learning on point sets in a metric space. <u>Advances in neural information processing systems,</u> 30, 2017. 

- [50] Guocheng Qian, Yuchen Li, Houwen Peng, Jinjie Mai, Hasan Hammoud, Mohamed Elhoseiny, and Bernard Ghanem. Pointnext: Revisiting pointnet++ with improved training and scaling strategies. <u>Advances in neural information processing systems,</u> 35:23192–23204, 2022. 

- [51] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In <u>International conference on machine learning,</u> pages 8748–8763. PMLR, 2021. 

- [52] Moritz Reuss, Omer<sup><u>¨</u></sup> Erdinc¸ Ya˘gmurlu, Fabian Wenzel, and Rudolf Lioutikov. Multimodal diffusion transformer: Learning versatile behavior from multimodal goals. In <u>First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024,</u> 2024. 

- [53] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In <u>Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,</u> pages 10684–10695, 2022. 

- [54] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-actor: A multi-task transformer for robotic manipulation. In <u>Conference on Robot Learning, pages 785–</u> 799. PMLR, 2023. 

- [55] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. In <u>International Conference on Learning Representations.</u> 

- [56] Priya Sundaresan, Suneel Belkhale, Dorsa Sadigh, and Jeannette Bohg. Kite: Keypoint-conditioned policies for semantic manipulation. In <u>Conference on Robot Learning,</u> pages 1006–1021. PMLR, 2023. 

- [57] Gemini Team, Rohan Anil, Sebastian Borgeaud, Yonghui 

Wu, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, et al. Gemini: a family of highly capable multimodal models. <u>arXiv preprint arXiv:2312.11805,</u> 2023. 

- [58] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. <u>arXiv preprint arXiv:2405.12213,</u> 2024. 

- [59] Julen Urain, Niklas Funk, Jan Peters, and Georgia Chalvatzaki. Se (3)-diffusionfields: Learning smooth cost functions for joint grasp and motion optimization through diffusion. In <u>2023 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 5923–5930. IEEE, 2023. 

- [60] Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In <u>Conference on Robot Learning,</u> pages 1723– 1736. PMLR, 2023. 

- [61] Chenxi Wang, Hongjie Fang, Hao-Shu Fang, and Cewu Lu. Rise: 3d perception makes real-world robot imitation simple and effective. In <u>ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation,</u> . 

- [62] Zhendong Wang, Jonathan J Hunt, and Mingyuan Zhou. Diffusion policies as an expressive policy class for offline reinforcement learning. In <u>The Eleventh International Conference on Learning Representations,</u> . 

- [63] Chuan Wen, Dinesh Jayaraman, and Yang Gao. Can transformers capture spatial relations between objects? In <u>The Twelfth International Conference on Learning Representations,</u> 2023. 

- [64] Chuan Wen, Xingyu Lin, John Ian Reyes So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point Trajectory Modeling for Policy Learning. In <u>Proceedings of Robotics: Science and Systems,</u> Delft, Netherlands, July 2024. doi: 10.15607/RSS.2024.XX.092. 

- [65] Zhou Xian, Nikolaos Gkanatsios, Theophile Gervet, Tsung-Wei Ke, and Katerina Fragkiadaki. Chaineddiffuser: Unifying trajectory diffusion and keypose prediction for robotic manipulation. In <u>7th Annual Conference on Robot Learning,</u> 2023. 

- [66] Annie Xie, Lisa Lee, Ted Xiao, and Chelsea Finn. Decomposing the generalization gap in imitation learning for visual robotic manipulation. In <u>2024 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 3153–3160. IEEE, 2024. 

- [67] Chengbo Yuan, Chuan Wen, Tong Zhang, and Yang Gao. General flow as foundation affordance for scalable robot learning. In <u>8th Annual Conference on Robot Learning,</u> 2024. URL https://openreview.net/forum?id=nmEt0ci8hi. 

- [68] Wentao Yuan, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. M2t2: Multi-task masked transformer for object-centric pick and place. In <u>7th Annual Conference on Robot Learning.</u> 

- [69] Yanjie Ze, Ge Yan, Yueh-Hua Wu, Annabella Macaluso, Yuying Ge, Jianglong Ye, Nicklas Hansen, Li Erran Li, and Xiaolong Wang. Gnfactor: Multi-task real robot learning with generalizable neural feature fields. In <u>Conference on Robot Learning,</u> pages 284–301. PMLR, 2023. 

- [70] Yanjie Ze, Gu Zhang, Kangning Zhang, Chenyuan Hu, Muhan Wang, and Huazhe Xu. 3d diffusion policy: Generalizable visuomotor policy learning via simple 3d representations. In <u>ICRA 2024 Workshop on 3D Visual Representations for Robot Manipulation,</u> 2024. 

- [71] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pretraining. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision,</u> pages 11975–11986, 2023. 

- [72] Tong Zhang, Yingdong Hu, Hanchen Cui, Hang Zhao, and Yang Gao. A universal semantic-geometric representation for robotic manipulation. In <u>Conference on Robot Learning,</u> pages 3342–3363. PMLR, 2023. 

- [73] Tong Zhang, Yingdong Hu, Jiacheng You, and Yang Gao. Leveraging locality to boost sample efficiency in robotic manipulation. <u>arXiv preprint arXiv:2406.10615,</u> 2024. 

- [74] Tony Z Zhao, Jonathan Tompson, Danny Driess, Pete Florence, Seyed Kamyar Seyed Ghasemipour, Chelsea Finn, and Ayzaan Wahid. Aloha unleashed: A simple recipe for robot dexterity. In <u>8th Annual Conference on Robot Learning.</u> 

- [75] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. <u>arXiv preprint arXiv:2304.13705,</u> 2023. 

- [76] Yuhang Zheng, Xiangyu Chen, Yupeng Zheng, Songen Gu, Runyi Yang, Bu Jin, Pengfei Li, Chengliang Zhong, Zengmao Wang, Lina Liu, et al. Gaussiangrasper: 3d language gaussian splatting for open-vocabulary robotic grasping. <u>arXiv preprint arXiv:2403.09637,</u> 2024. 

- [77] Junsheng Zhou, Jinsheng Wang, Baorui Ma, Yu-Shen Liu, Tiejun Huang, and Xinlong Wang. Uni3d: Exploring unified 3d representation at scale. In <u>The Twelfth International Conference on Learning Representations.</u> 

- [78] Haoyi Zhu, Yating Wang, Di Huang, Weicai Ye, Wanli Ouyang, and Tong He. Point cloud matters: Rethinking the impact of different observation spaces on robot learning. <u>arXiv preprint arXiv:2402.02500,</u> 2024. 

- [79] Minjie Zhu, Yichen Zhu, Jinming Li, Junjie Wen, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, Yaxin Peng, Feifei Feng, et al. Scaling diffusion policy in transformer to 1 billion parameters for robotic manipulation. <u>arXiv preprint arXiv:2409.14411,</u> 2024. 

- [80] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-languageaction models transfer web knowledge to robotic control. In <u>Conference on Robot Learning,</u> pages 2165–2183. PMLR, 2023. 

APPENDIX 

## _A. Environment Visualization_ 

For all four tasks, we collect post-training data in 8 environments and evaluate the policies in 4 in-domain environments and 4 unseen environments. We visualize all the scenes in Figure 7. 

## _B. Object Visualization_ 

Similar to the scenes, we have 8 training objects and 4 unseen objects for each task. All the objects are visualized in Figure 8. 

We list the training hyperparameters for pre-training and fine-tuning in Table III and Table IV. We train all models on 8 NVIDIA A800 GPUs. 

TABLE III: **Pre-training Hyperparameters.** 

|Hyperparameter|Value|
|---|---|
|Image observation horizon|2|
|Proprioception observation horizon|2|
|Action prediction horizon|16|
|Action execution horizon|8|
|Pointcloud down sample number|4000|
|Optimizer|AdamW|
|Learning rate|1e-4|
|Learning rate schedule|cosine|
|Weight decay|0.1|
|Gradient clipping|1.0|
|Batch size|128|
|Inference denoising iterations|16|


TABLE IV: **Fine-tuning Hyperparameters.** 

|Hyperparameter|Value|
|---|---|
|LoRA rank|32|
|LoRA alpha|16|
|Image observation horizon|2|
|Proprioception observation horizon|2|
|Action prediction horizon|16|
|Action execution horizon|8|
|Pointcloud down sample number|4000|
|Optimizer|AdamW|
|Learning rate|1e-6|
|Learning rate schedule<br>|cosine|
|Weight decay|0.1|
|Gradient clipping|1.0|
|Batch size|128|
|Inference denoising iterations|16|


- Fold Towel: The robot is required to complete two steps: first, grasping the right edge of the towel, and second, folding the towel to the left. The towel’s center position is randomly varied, and its orientation is randomly rotated within ±30 degrees. The towels have different colors, textures, and materials, but they are prefolded into approximately rectangular shapes of similar size. 

- Clean Table: The robot is required to complete two steps: first, grasping the spitball on the surface, and second, moving it just above the trash bin and dropping it into the bin. The positions of the spitball and the trash bin are randomly placed. The trash bins have different colors and textures, and their sizes vary to some extent. 

- Stand up Cup: The robot is required to complete two steps: first, it inserts the gripper into the cup’s opening and grasps the cup, and second, it lifts and stands the cup upright. The cup’s placement is random, with its orientation varying within the 180-degree range where the opening faces the robotic arm. 

- Pour Water: The robot performs three sequential actions: initially, it grasps a drink bottle; subsequently, it pours water into a mug; and finally, it places the bottle on a coaster. The position of the mug is randomly varied. The relative positions are also randomized, but the water bottle is always approximately to the left of the cup, while the coaster is approximately to the right of the cup. The water bottle, cup, and coaster vary in color, material, and size. 

As Figure 9 shows, we basically setup the robot following the DROID. We use a Franka Emika Panda robot arm equipped with a Robotiq gripper, mounted on a movable lifting desk. For point cloud observation, we use one ZED mini camera and one ZED 2 camera. The ZED 2 provides third-person perspective images, fixed on a movable lifting desk, while the ZED mini provides wrist perspective images, fixed on the camera’s end effector. For data collection, we use a Meta Quest2 VR glass to teleoperate the robot with a control frequency of 15Hz. All policy evaluations are performed on an RTX 3090 GPU (24GB VRAM). And everything is powered by a mobile power supply (EcoFlow DELTA 2 Max). 


Fig. 9: hardware setup. 


Fig. 7: **Scenes visualization** of 8 post-training scenes and 4 unseen scenes for evaluation. 


Fig. 8: **Object Visualization** of 8 training objects and 4 unseen objects for each task. 

