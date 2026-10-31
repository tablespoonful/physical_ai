---
title: "FlowDreamer: A RGB-D World Model with Flow-based Motion Representations for Robot Manipulation"
date: "2025-05-15"
authors: "Jun Guo; Xiaojian Ma; Yikai Wang; Min Yang; Huaping Liu; Qing Li"
url: https://arxiv.org/abs/2505.10075
pdf: https://arxiv.org/pdf/2505.10075
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.10075)** / [論文ページ](https://arxiv.org/abs/2505.10075)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **FlowDreamer: A RGB-D** **<mark>World</mark> Model with Flow-based Motion Representations for Robot Manipulation** 

Jun Guo<sup>*,1,2</sup> , Xiaojian Ma<sup>*,#,1</sup> , Yikai Wang<sup>*,3</sup> , Min Yang<sup>1,4</sup> , Huaping Liu<sup>#,2</sup> , Qing Li<sup>#,1</sup> 

> 1State Key La <mark>boratory</mark> of General Artificial Intelligence (BIGAI) 

2Department of Computer Science and Technology, Tsinghua University 

3School of Artificial Intelligence, Beijing Normal University 

4School of Artificial Intelligence and Automation, Huazhong University of Science and Technology 

> *Equ <mark>al Contr</mark> ibution #Corresponding Author https://sharinka0715.github.io/FlowDreamer/ 

## **Abstract** 

_This paper investigates training better visual world models for robot manipulation,_ i.e _., models that can predict future visual observations by conditioning on past frames and robot actions. Specifically, we consider world models that operate on RGB-D frames (RGB-D world models). As opposed to canonical approaches that handle dynamics prediction mostly implicitly and reconcile it with visual rendering in a single model, we introduce FlowDreamer, which adopts 3D scene flow as explicit motion representations. FlowDreamer first predicts 3D scene flow from past frame and action conditions with a U-Net, and then a diffusion model will predict the future frame utilizing the scene flow. FlowDreamer is trained end-to-end despite its modularized nature. We conduct experiments on 4 different benchmarks, covering both video prediction and visual planning tasks. The results demonstrate that FlowDreamer achieves better performance compared to other baseline RGB-D world models by 7% on semantic similarity, 11% on pixel quality, and 6% on success rate in various robot manipulation domains._ 

## **1. Introduction** 

We study developing better visual world models for robot manipulation tasks. In robotics, a visual world model [24] needs to perform the following steps: 1) **dynamics prediction** : predict the future motion given the current sensory observations (about robot and environment states) and robot action; and 2) **visual rendering** : render the visual observations after the motion happens. A visual world model captures the underlying world dynamics and can be used as a learnable simulator to help produce and evaluate motion plans of robot manipulators in company with model-based 


Figure 1. **Proposed RGB-D world model with flow-based motion representations.** FlowDreamer adopts a two-stage prediction framework, which explicitly predict scene flow as motion representations. FlowDreamer achieves better results on future frame prediction and visual planning tasks in various robot manipulation domains. 

planning algorithms [63, 87, 94, 98]. The use of visual world models alleviates the need for precise scene modeling and simulation [14, 37], making it a promising research direction. In this paper, we specifically focus on world models that operate on RGB-D frames (RGB-D world models), which are commonly adopted sensory observations in robot manipulation tasks. 

Existing visual world models have undergone rapid development in recent years. Starting from early approaches that utilize recurrent neural networks (RNNs) [18, 25– 27, 29, 39], powerful diffusion-based generative models [7, 19, 32, 64, 70, 71] have gain popularity in recent world models [1, 2, 40, 59]. However, regardless of the architectures of these models, they mostly reconcile the two aforementioned steps (dynamics prediction and visual rendering) 

1 

in a single model. These design choices not only reduce the model’s transparency but also, as our later experiments show, impair its future prediction performance. We hypothesize that models trained solely with frame prediction loss tend to prioritize improving the fidelity of rendered visual appearances while placing less emphasis on accurate dynamics prediction. This highlights the importance of exploring methods that explicitly model dynamics prediction. 

To this end, we propose FlowDreamer, a RGB-D world model that explicitly models dynamics prediction to enhance the predictive capability of world models. FlowDreamer adopts a two-stage framework to predict the environment dynamics and render the visual observations separately. Specifically, FlowDreamer introduces explicit modeling of 3D dynamics by leveraging 3D scene flow [82], which is a versatile representation that describes the motion of objects within a scene. In the first stage, a scene flow prediction module independently predicts the dynamic changes induced by given actions. This module is trained with a scene flow prediction loss to ensure robust supervision of the scene dynamics, thereby endowing the world model with an enhanced understanding of dynamics in 3D space. In the second stage, we employ a conditional diffusion model [32, 71] that predicts the next visual observation based on the current observation and the motion information provided by the scene flow prediction module. Despite its modularized nature, our model can be trained in an endto-end fashion. 

We validate the effectiveness of our method on multiple benchmarks commonly used in robotic manipulation. On action-conditioned benchmarks ( _e.g_ ., RT-1 [6], Language Table [51]), our approach achieves better visual performance comparable to normal RGB-D world models, with a 7% increase in semantic similarity and 11% on pixel quality. Evaluations on VP<sup>2</sup> visual planning benchmark [77] with RoboDesk [41] and Robosuite [99] tasks reveal a 6% increase in the success rate in manipulation tasks. 

In summary, our main contributions are as follows: 

1. We propose FlowDreamer, a two-stage RGB-D world model with dynamics and visual prediction module, which can be trained in an end-to-end fashion despite its modularized nature. 

2. We introduce a scene flow prediction module that adopts 3D scene flow on RGB-D space as a general motion representation to supervise dynamics prediction and enhance dynamics modeling. 

3. We perform comprehensive evaluations across several benchmarks, demonstrating the efficacy of our approach in both visual performance and visual planning tasks. 

## **2. Related Work** 

### **2.1. Generative World Models in Robotics** 

World models [24], also known as dynamic models, refer to techniques that predict the future state based on current observations and given conditions. In robotics, control strategies can leverage the generative capability of these models for planning, learning, or reducing the cost associated with interactions in the real environment. A world model typically requires the robot’s current observation in the form of latent states, sensor measurements, or visual information as input and produces future observations while also potentially predicting higher-level information such as rewards, values, or subsequent actions. 

Existing work in this domain can be broadly categorized into two types, namely _control-based_ world models and _instruction-based_ world models. In _control-based_ world models [20, 21, 63, 87, 94, 98], the conditioning inputs are robot control signals, including joint forces or velocities, end-effector positions, or movement commands. These models can serve as simulators for the environment and facilitate approaches such as model-based reinforcement learning [18, 25–27, 39, 66, 73, 74, 88] and model predictive control [28, 29]. Many studies [2, 8, 40, 53, 54, 58, 59, 79] have also trained world models within games with players’ interaction signals as input, employing neural networks as the game engine. In contrast, _instruction-based_ world models [1, 4, 16, 17, 34, 43, 47, 94, 97] take task-related instructions, _e.g_ ., task identifiers or natural language descriptions, as conditions to generate a sequence of future states or actions. This approach not only envisions future world states but also simulates the execution of policies, thereby allowing inverse dynamics to derive robot control parameters from observations [4, 43] or enabling fine-tuning into a vision-language-action (VLA) model [11, 16, 17, 96]. This paper proposes a _control-based_ world model that uses robot actions as conditions and employs scene flow as an intermediate representation to simulate and predict environmental dynamics, ultimately generating images that are interpretable by human observers. 

### **2.2. Dynamics Modeling** 

Most existing world models are trained in an end-to-end manner with supervising signals to directly predict future states without explicitly modeling the dynamical processes. Explicit modeling of the dynamics underlying environmental state changes can enhance the interpretability of the world model and improve prediction accuracy. In the field of video generation, there are several works [22, 30, 52, 57, 69] that model the motion between frames to better control and enhance the performance of video generation models. Early works [10, 56, 91] employed SE(3) transformations as an intermediate representation of object mo- 

2 


Figure 2. **Overview of FlowDreamer.** At stage 1, FlowDreamer receives the RGB-D frame and the robot action as input to explicitly predict the scene flow as motion representations. At stage 2, FlowDreamer leverages a denoising U-Net to generate high-resolution nextstep future observation via diffusion. 

### **3.1. Background: Latent Diffusion Models** 

tion. This approach is limited to rigid bodies and requires the world model to possess object-centric awareness, which requires extra segmentations of training data. An alternative representation is _flow_ [43, 90], which is referred to as optical flow [33, 50] in 2D images and as scene flow [82] in 3D space. Flow is defined as the displacement of every point in the observation space from one timestep to the next, which provides a universal and flexible means to represent various forms of motion, including non-rigid objects. In order to extract flow information from the training sequences of world models, flow estimation methods are employed to compute the displacement between adjacent frames. In the 2D domain, numerous methods, including both traditional [5, 9, 33, 50] and deep learningbased [15, 35, 44, 62, 67, 68, 72, 75, 92] approaches, have been developed to estimate optical flow. In 3D space, several deep learning methods [38, 42, 48, 49, 81, 89] have shown promise in estimating scene flow, while the task remains generally more challenging. Our approach utilizes 3D scene flow in the RGB-D space as the representation of motion, which can be obtained by integrating optical flow from consecutive frames with the corresponding depth information. 

Diffusion models [32, 70, 71] progressively transform data into noise through a forward diffusion process and then learn to reverse this process to generate high-quality samples. Latent diffusion models [64] extend this framework by performing the diffusion process in a lower-dimensional latent space rather than directly in the pixel space. By leveraging a learned encoder [80] to project data into a compact latent representation, latent diffusion models achieve significant improvements in computational efficiency and scalability while still maintaining high fidelity in the generated samples. In the forward process, small amounts of Gaussian noise are incrementally added to the data, gradually destroying its structure, which can be formatted by 


where **z**<sup>_k_</sup> is the noised latent, _β_<sup>_k_</sup> is a variance schedule controlling the noise level, both at _k_ -th denoising step. The reverse process can be modeled by a neural network _ϵθ_ which aims to progressively denoise the sample, recovering **z**<sup>0</sup> from **z**<sup>_k_</sup> (which is approximately Gaussian): 

## **3. FlowDreamer: A RGB-D World Model** 

In this section, we illustrate the framework of our FlowDreamer. Fig. 2 depicts the overall framework of our method. FlowDreamer is a two-stage action-conditioned RGB-D world model, which receives the current RGB-D observation ( _It, Dt_ ) and the robot action **a** _t_ as the input and predicts the future RGB observations _It_ +1. At stage 1, we start from an RGB-D observation image and a robot action, predicting the 3D scene flow _ft→t_ +1 between the current and the next frame (Sec. 3.2). At stage 2, we apply a diffusion denoising network condition on the RGB-D image ( _It, Dt_ ) and the predicted scene flow _f_<sup>ˆ</sup> _t→t_ +1 to generate the observation _It_ +1 at the next timestep from a random noise _ϵt_ +1 (Sec. 3.3). 


During training, we sample a timestep _t ∈_ [1 _, K_ ] and add a Gaussian noise _ϵ_<sup>_k_</sup> _∼N_ (0 _,_ **I** ) to the clean sample **z**<sup>0</sup> by **z**<sup>_k_</sup> = _~~√~~ α_ ¯<sup>_k_</sup> **z**<sup>0</sup> + _~~√~~_ 1 _− α_ ¯<sup>_k_</sup> _ϵ_<sup>_k_</sup> , and the model is optimized to predict the added noise _ϵ_<sup>_k_</sup> , resulting in a simplified loss function: 


In the inference phase, we can generate **z**<sup>0</sup> by starting from a sample **z**<sup>_K_</sup> drawn from a standard Gaussian distribution, and the model iteratively computes **z**<sup>_k−_1</sup> from **z**<sup>_k_</sup> : 


3 

where _ε ∼N_ (0 _,_ **I** ) and _σ_<sup>_k_</sup> is an appropriately chosen noise scale. In practice, we can accelerate the generation process by setting _σ_<sup>_k_</sup> = 0 and use a sub-sequence of [1 _, . . . , K_ ] to reduce the forward steps [71]. 

### **3.2. Dynamics Prediction** 

Different from end-to-end world models, FlowDreamer applies a dynamics prediction module to explicitly predict the transition between consecutive frames. In robot manipulation tasks, we hope to find an intermediate representation as auxiliary information to depict the dynamics of the robot and objects. Innovated by [43, 90, 91], we choose 3D scene flow as the intermediate representation, which is general and versatile and can be collected by various flow estimation networks. In point clouds, scene flow is generally defined by the displacement of point coordinates. We can easily project an RGB-D image into point cloud space with camera intrinsics, where 2D pixels in the image with shape ( _H, W_ ) are converted to _H × W_ points in 3D space. We denote _K_ as the camera intrinsic matrix, ( _u, v_ ) as the horizontal and vertical index of pixels, and _D_ as the depth map. Then, the pixel coordinates in camera coordinate space ( _x, y, z_ ) can be calculated by: 


Assume the point in 3D space has a coordinate ( _x, y, z_ ) at timestep _t_ and ( _x_<sup>_′_</sup> _, y_<sup>_′_</sup> _, z_<sup>_′_</sup> ) at timestep _t_ + 1, the 3D scene flow is defined as follows: 


As pixels at the same index between consecutive frames do not always represent the same 3D point, the vital challenge to get the scene flow is to find the correspondence between frames. For simulation data, we directly obtain the scene flow from the simulator backend according to the rigid transformations of every object. For real-world data, we can apply an off-the-shelf 3D scene flow estimator named RAFT-3D [76] to estimate the scene flow. If the real-world data has no depth information, we can estimate the depth by a pretrained video depth estimator [12]. The detailed scene flow obtainment pipeline are introduced in Appendix B. 

We apply a dynamics prediction module to predict the 3D scene flow from time _t_ to _t_ + 1, given the RGB-D observation ( _It, Dt_ ) and the robot action **a** _t_ . The backbone of our dynamics prediction model is a conditional U-Net [65], and the robot action is integrated with the feature map via cross-attention [86]. The loss function _L_ flow is defined as the mean square error (MSE) between the module output _f_ ˆ _t→t_ +1 and the estimated scene flow _ft→t_ +1: 


### **3.3. Future Generation** 

After getting the predicted scene flow, we can further predict future observations through a generative model. We choose Latent Diffusion Models as our future generation model, as it has shown outstanding capability in image generation [19, 64]. In FlowDreamer, we fine-tune the pretrained Stable Diffusion [64] to build our future generation module, which we denote as _ϵθ_ . The input of the generation module contains the current RGB-D observation ( _It, Dt_ ), the robot action **a** _t_ , and the predicted 3D scene flow _f_<sup>ˆ</sup> _t→t_ +1, and the output of the module is the next RGB observation _It_ +1. In order to generate high-resolution observations, following previous works [63, 98], we use the pre-trained variational autoencoder in Stable Diffusion [64] to compress the RGB observation _It_ into latent space **z** _t_ . The module output **z** _t_ +1 is also in latent space and can be decoded to image space by the pretrained decoder. Depth map _Dt_ and the scene flow _f_<sup>ˆ</sup> _t→t_ +1 are firstly downsampled to the same shape of **z** _t_ by several convolutional layers, and then channel-wise concatenated with **z** _t_ as the input of the diffusion model: 


where _k_ is the diffusion step, and _z_<sup>_k_</sup> is the latent to be denoised. We do not directly predict the depth map _Dt_ +1, as the decoder of the diffusion model is not specially designed for metric depths. To autoregressively imagine the future, we leverage a pre-trained depth estimation model [93] with a simple DPT [61] head to predict the metric depth _Dt_ +1 from _It_ +1. 

In summary, our FlowDreamer trains the dynamics prediction module and the denoising U-Net jointly, and the overall loss function is: 


where _L_ diff and _L_ flow are defined in Eqn. 3 and Eqn. 7, and _α_ is a coefficient to control the weight of the two objectives. 

## **4. Experiments** 

In this section, we conduct extensive experiments in four different benchmarks to verify the performance of FlowDreamer. We aim to answer three questions: 

1. Is FlowDreamer effective on video prediction compared 

   - with other RGB-D world models? (Sec. 4.1) 

4 

Table 1. **Video prediction results on the SimplerEnv RT-1 benchmark.** We categorize the metrics into three groups: semantic similarity, pixel similarity, and media quality. **Bold** numbers indicate the best results, and underlined numbers indicate the second best results. 

|**Method**|**Semantic**|**Similarity**|**Pi**|**xel Similari**|**ty**|**Media**|**Quality**|
|---|---|---|---|---|---|---|---|
||DINOv2 L2↓|CLIP score↑|PSNR↑|SSIM↑|LPIPS↓|FID↓|FVD↓|
|Vanilla|12.5936|0.8999|20.5925|0.7831|0.1304|71.8069|365.0697|
|MinkNet|12.1569|0.9038|20.5804|0.7942|0.1252|57.9706|325.3416|
|SepTrain|11.4512|0.9131|21.2289|0.8135|0.1097|45.3967|**245.9106**|
|FlowDreamer|**10.9922**|**0.9189**|**21.7562**|**0.8196**|**0.0993**|**43.5807**|268.3853|


Table 2. **Video prediction results on the Language Table benchmark.** We categorize the metrics into three groups: semantic similarity, pixel similarity, and media quality. **Bold** numbers indicate the best results, and underlined numbers indicate the second best results. 

|**Method**|**Semantic**<br>DINOv2 L2↓|**Similarity**<br>CLIP score↑|**Pi**<br>PSNR↑|**xel Similarit**<br>SSIM↑|**y**<br>LPIPS↓|**Media Q**<br>FID↓|**uality**<br>FVD↓|
|---|---|---|---|---|---|---|---|
|Vanilla|10.7294|0.9473|25.6762|0.9273|0.0627|26.6415|110.4629|
|MinkNet|10.0136|0.9614|25.1973|0.9228|0.0642|33.5479|88.3917|
|SepTrain|10.2514|0.9507|25.9785|0.9278|0.0571|21.2822|87.3121|
|Ours|**9.3899**|**0.9688**|**26.8907**|**0.9401**|**0.0476**|**20.0259**|**66.9215**|


2. Can FlowDreamer facilitate model predictive control for robot manipulation tasks? (Sec. 4.2) 

3. How does the predicted scene flow in FlowDreamer contribute to the future prediction? (Sec. 4.3) 

### **4.1. Video Prediction** 

To evaluate the future generation performance of FlowDreamer, we conduct the video prediction experiments, which require the world model to generate a full trajectory given the first frame of the video and the action trajectory. By comparing the similarity between predicted frames and ground truth frames, we can verify the future prediction capability of world models. 

**Datasets.** We conduct video prediction experiments on RT1 [6] and Language Table [51] benchmarks to evaluate the methods. As the real-world data do not contain the depth information, we collect training and inference trajectories from the simulator. For RT-1 environment, we use SimplerEnv [46] as the simulator. For the Language Table environment, we use the official simulation environment. Collected trajectories are split into training, validation, and test sets without overlap. Experiments on real-world data are reported in Appendix C. 

**Baselines.** To evaluate the performance of FlowDreamer compared to other RGB-D world models, we design three different baselines: _Vanilla_ , _MinkNet_ , and _SepTrain_ . See detailed implementation in Appendix A. 

- _Vanilla_ is a single-stage RGB-D diffusion model, which receives current RGB-D observations as input and predicts RGB images at the next timestep. We compare it with our FlowDreamer to measure the contribution of the 

dynamics prediction module. 

- _MinkNet_ is a two-stage world model that replaces the backbone of the dynamics prediction module from U-Net to MinkowskiNet [13], a 4D sparse convolutional network for point clouds. We compare it with our FlowDreamer to demonstrate the effectiveness of the RGB-D representation. 

- _SepTrain_ is a two-stage world model, which trains the dynamics prediction module and the Denoising U-Net separately. We compare it with our FlowDreamer to evaluate the performance of end-to-end training. 

**Metrics.** To evaluate the video prediction performance, we use PSNR [36], SSIM [85], LPIPS [95], FID [31], and FVD [78] as the assessment metrics, and additionally calculate the latent L2 distance extracted by DINOv2 (denoted as DINOv2 L2) and the latent cosine similarity extract by CLIP (denoted as CLIP score) to estimate the semantic similarity. PSNR measures the distance between the predicted video and the ground-truth video in the pixel space, and SSIM evaluates the structural similarity between frames. LPIPS, FID, and FVD are model-based evaluation metrics that compare frames in latent feature space. LPIPS measures the distance in different feature spaces, while FID and FVD measure the distribution disparity between generated and ground-truth images or videos. DINOv2 and CLIP are large-scale pretrained models via unsupervised learning, which could robustly extract the semantic feature from the images. We assume that DINOv2 and CLIP feature distance could reflect the environment state information more than image quality metrics. 

**Results.** Table 1 and 2 shows the quantitative results on 

5 


Figure 3. **Qualitative results on the SimplerEnv RT-1 and Language Table benchmark.** We show the predicted frames and the scene flows except for _Vanilla_ , where only RGB frames are being predicted. The R, G, and B channel values in the flow visualization represent the components of the 3D scene flow along the _x_ , _y_ , and _z_ directions, respectively, normalized by the maximum value of the scene flow. 

RT-1 and Language Table benchmarks. We can observe that our FlowDreamer achieves the best performance on most of the metrics, including semantic similarity, pixel similarity, and media quality. The results demonstrate the effectiveness of our FlowDreamer. The _SepTrain_ model achieves the second-best performance at most of the metrics, and the performance is very similar to our FlowDreamer. This indicates that end-to-end training is generally a better approach, while the contribution is less than that of other components. We notice that _Vanilla_ and _MinkNet_ have similar performances, though _MinkNet_ has a similar two-stage framework and a dynamics prediction module. From the qualitative results (Fig. 3), we can see the scene flow predicted by _MinkNet_ has low quality. The color of the predicted flows is similar to the ground truth flows, which shows that the direction of flows is generally correct. However, the flow predicted by _MinkNet_ cannot distinguish the moving parts and the stationary parts, thus not providing efficient guidance to the downstream diffusion model. Moreover, we observe 

from Fig. 3 that all predictions have a similar visual quality, but our FlowDreamer outperforms other models in environment states. This lies in the additional dynamics prediction module, which can explicitly predict the environment transition, thus resulting in more accurate future predictions. 

### **4.2. Visual Planning** 

We further evaluate our FlowDreamer on visual planning tasks to show how FlowDreamer makes a difference in robot manipulation tasks. In visual planning tasks, the policy interacts with environments to minimize the difference between the observation and the goal image. For world models without any action output, model predictive control (MPC) [18, 20] methods can be applied to evaluate the performance. 

**Datasets.** We choose VP<sup>2</sup> [77] as our visual planning benchmark. VP<sup>2</sup> is a control-centric benchmark that evaluates video prediction models by visual MPC methods. The environment contains four Robosuite [99] and seven Ro- 

6 


Figure 4. **Visual planning results on the VP**<sup>2</sup> **benchmark.** We report the mean and the min/max performance of different methods over multiple runs with different random seeds. On the right, “Average” means the average success rate over all reported tasks. 


Figure 5. **Qualitative results on the Robodesk and Robosuite dataset.** The trajectory comes from the validation set, which is split from the original training trajectories and is not used for training. For our method, we show the predicted RGB images and scene flows. 

boDesk [41] tasks. We run our experiments with 4 seeds on RoboDesk tasks and 3 seeds with Robosuite tasks, which keeps same with other VP<sup>2</sup> experiments. 

**Baselines.** We compare the visual planning performance with a single-stage RGB-D diffusion world model (denoted as _Vanilla_ ). Moreover, following iVideoGPT [87], we choose all video generation models provided by VP<sup>2</sup> paper as our baselines, including FitVid [3], SVG’ [83], MCVD [84], Struct-VRNN [55], and MaskViT [23]. We also compare our performance with iVideoGPT itself. 

**Metrics.** Following iVideoGPT [87], we report the mini- 

mum, maximum, and average success rate of our method between different random seeds. The reported baseline results are provided by previous works [77, 87], and we additionally report our performance in the same setting. For Robosuite push tasks, a cost below 0.05 is considered a success. 

**Results.** Fig. 4 shows the visual MPC results on the VP<sup>2</sup> benchmark. From the results, we found that our FlowDreamer always performs better than the _Vanilla_ model, which implies that our proposed framework works well on visual planning tasks. For other video prediction models, 

7 


Figure 6. **The qualitative results when flows are reversed.** With reversed (therefore incorrect) scene flow, the diffusion model in FlowDreamer can only utilize action condition, leading to worse performances on future frame prediction. 


Figure 7. **The correlation between the flow prediction error and image assessment metrics.** We show the scatter plots of SSIM (higher is better), LPIPS (lower is better), DINOv2 L2 (lower is better), and CLIP score (higher is better) vs. flow error and report the correlation coefficients. 

|_r_||PSNR|SSIM|LPIPS|DINOv2|CLIP|
|---|---|---|---|---|---|---|
|Flow|Error|-0.6704|-0.8239|0.6072|0.1821|-0.3058|


Table 3. **The correlation coefficient** _r_ **between the flow prediction error and image assessment metrics.** _r >_ 0 indicates a positive correlation and _r <_ 0 indicates a negative correlation. 

of historical context. In Robosuite tasks, objects would have velocity after being pushed by the robot arm, which cannot be reflected by a single RGB-D image. Those objects without attachment to the robot arm have scene flows, which could be misleading in prediction. 

### **4.3. Additional Analysis on Flow Prediction** 

In this section, we conduct further analysis to figure out the effect of the predicted flow. We first reverse the direction of input flows at stage 2 while the robot action remains unchanged. Fig. 6 visualizes the resulting prediction. We can observe that the robot did not really take contrary actions due to the action input at stage 2, while its performance becomes worse and cannot lead to the goal state. This result shows that the scene flow predicted at stage 1 provides auxiliary information to better generate the future. 

Then, we calculate the correlation between the flow prediction error and other image assessment metrics. Table 3 shows the correlation coefficient _r_ between flow prediction error and other metrics, and Fig. 7 shows the scatter plot for SSIM, LPIPS, DINOv2 L2, and CLIP score. We notice that the flow error has a high correlation with PSNR and SSIM and a reasonable correlation with LPIPS, which demonstrates the effectiveness of the predicted flow in video prediction. For DINOv2 L2 and CLIP scores, the correlations are weak, where we infer that the semantic metrics extracted by DINOv2 and CLIP do not tell the relatively minor prediction error from the ground truth well. 

## **5. Conclusion** 

FlowDreamer achieves a comparable performance on the average metric, while all video prediction baselines have a context of two frames. Our FlowDreamer performs best on some tasks, _e.g_ ., Green button and Upright block, while it fails on other tasks, _e.g_ ., Open slide. We hypothesize that the failure lies in that the visual reward cannot always point to the correct trajectory, which is also revealed by [87]. Fig. 5 shows the qualitative results on VP<sup>2</sup> benchmark tasks. Our model can predict the flow and the goal accurately on RoboDesk tasks, while it is hard to predict precise flow on Robosuite push tasks. We assume the reason lies in the lack 

We introduce FlowDreamer, an action-conditioned RGB-D world model with flow-based motion representations. FlowDreamer leverages 3D scene flow as a versatile motion representation and applies a separate dynamics prediction module to learn environment dynamics from scene flow. Despite its modularized nature, FlowDreamer can be jointly trained in an end-to-end manner. Experiments on 4 different benchmarks, including video prediction and visual planning, demonstrate the superiority of our FlowDreamer compared to other RGB-D world models. Limitations and future directions can be found in the Appendix. 

8 

## **References** 

- [1] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 1, 2 

- [2] Eloi Alonso, Adam Jelley, Vincent Micheli, Anssi Kanervisto, Amos Storkey, Tim Pearce, and Franc¸ois Fleuret. Diffusion for world modeling: Visual details matter in atari. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 1, 2 

- [3] Mohammad Babaeizadeh, Mohammad Taghi Saffar, Suraj Nair, Sergey Levine, Chelsea Finn, and Dumitru Erhan. Fitvid: Overfitting in pixel-level video prediction. _arXiv preprint arXiv:2106.13195_ , 2021. 7 

- [4] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Rich Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pre-trained image-editing diffusion models. In _International Conference on Learning Representations (ICLR)_ , 2024. 2 

- [5] Michael J Black and Padmanabhan Anandan. A framework for the robust estimation of optical flow. In _International Conference on Computer Vision (ICCV)_ , 1993. 3 

- [6] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 2, 5, 13 

- [7] Tim Brooks, Bill Peebles, Connor Holmes, Will DePue, Yufei Guo, Li Jing, David Schnurr, Joe Taylor, Troy Luhman, Eric Luhman, Clarence Ng, Ricky Wang, and Aditya Ramesh. Video generation models as world simulators, 2024. 1 

- [8] Jake Bruce, Michael D Dennis, Ashley Edwards, Jack Parker-Holder, Yuge Shi, Edward Hughes, Matthew Lai, Aditi Mavalankar, Richie Steigerwald, Chris Apps, et al. Genie: Generative interactive environments. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

- [9] Andr´es Bruhn, Joachim Weickert, and Christoph Schn¨orr. Lucas/kanade meets horn/schunck: Combining local and global optic flow methods. _International Journal of Computer Vision (IJCV)_ , 2005. 3 

- [10] Arunkumar Byravan and Dieter Fox. Se3-nets: Learning rigid body motion using deep neural networks. In _International Conference on Robotics and Automation (ICRA)_ , 2017. 2 

- [11] Chi-Lam Cheang, Guangzeng Chen, Ya Jing, Tao Kong, Hang Li, Yifeng Li, Yuxiao Liu, Hongtao Wu, Jiafeng Xu, Yichu Yang, et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arXiv preprint arXiv:2410.06158_ , 2024. 2 

- [12] Sili Chen, Hengkai Guo, Shengnan Zhu, Feihu Zhang, Zilong Huang, Jiashi Feng, and Bingyi Kang. Video depth anything: Consistent depth estimation for super-long videos. _arXiv preprint arXiv:2501.12375_ , 2025. 4, 14 

- [13] Christopher Choy, JunYoung Gwak, and Silvio Savarese. 4d spatio-temporal convnets: Minkowski convolutional neural 

networks. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 5, 13 

- [14] Tianyuan Dai, Josiah Wong, Yunfan Jiang, Chen Wang, Cem Gokmen, Ruohan Zhang, Jiajun Wu, and Li Fei-Fei. Automated creation of digital cousins for robust policy learning. _arXiv preprint arXiv:2410.07408_ , 2024. 1 

- [15] Alexey Dosovitskiy, Philipp Fischer, Eddy Ilg, Philip Hausser, Caner Hazirbas, Vladimir Golkov, Patrick Van Der Smagt, Daniel Cremers, and Thomas Brox. Flownet: Learning optical flow with convolutional networks. In _International Conference on Computer Vision (ICCV)_ , 2015. 3 

- [16] Yilun Du, Sherry Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Josh Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning universal policies via text-guided video generation. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 2 

- [17] Yilun Du, Sherry Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Pierre Sermanet, Tianhe Yu, Pieter Abbeel, Joshua B Tenenbaum, Leslie Pack Kaelbling, et al. Video language planning. In _International Conference on Learning Representations (ICLR)_ , 2024. 2 

- [18] Frederik Ebert, Chelsea Finn, Sudeep Dasari, Annie Xie, Alex Lee, and Sergey Levine. Visual foresight: Model-based deep reinforcement learning for vision-based robotic control. _arXiv preprint arXiv:1812.00568_ , 2018. 1, 2, 6 

- [19] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas M¨uller, Harry Saini, Yam Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers for high-resolution image synthesis. In _International Conference on Machine Learning (ICML)_ , 2024. 1, 4 

- [20] Chelsea Finn and Sergey Levine. Deep visual foresight for planning robot motion. In _International Conference on Robotics and Automation (ICRA)_ , 2017. 2, 6 

- [21] Chelsea Finn, Ian Goodfellow, and Sergey Levine. Unsupervised learning for physical interaction through video prediction. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2016. 2 

- [22] Daniel Geng, Charles Herrmann, Junhwa Hur, Forrester Cole, Serena Zhang, Tobias Pfaff, Tatiana Lopez-Guevara, Carl Doersch, Yusuf Aytar, Michael Rubinstein, et al. Motion prompting: Controlling video generation with motion trajectories. _arXiv preprint arXiv:2412.02700_ , 2024. 2 

- [23] Agrim Gupta, Stephen Tian, Yunzhi Zhang, Jiajun Wu, Roberto Mart´ın-Mart´ın, and Li Fei-Fei. Maskvit: Masked visual pre-training for video prediction. In _International Conference on Learning Representations (ICLR)_ , 2023. 7 

- [24] David Ha and J¨urgen Schmidhuber. Recurrent world models facilitate policy evolution. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2018. 1, 2 

- [25] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. 1, 2 

- [26] Danijar Hafner, Timothy P Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. In _International Conference on Learning Representations (ICLR)_ , 2021. 

9 

- [27] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 1, 2 

- [28] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2023. 2 

- [29] Nmenicklas A Hansen, Hao Su, and Xiaolong Wang. Temporal difference learning for model predictive control. In _International Conference on Machine Learning (ICML)_ , 2022. 1, 2 

- [30] Zekun Hao, Xun Huang, and Serge Belongie. Controllable video generation with sparse trajectories. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2018. 2 

- [31] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 5 

- [32] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2020. 1, 2, 3 

- [33] Berthold KP Horn and Brian G Schunck. Determining optical flow. _Artificial intelligence_ , 1981. 3 

- [34] Siyuan Huang, Liliang Chen, Pengfei Zhou, Shengcong Chen, Zhengkai Jiang, Yue Hu, Peng Gao, Hongsheng Li, Maoqing Yao, and Guanghui Ren. Enerverse: Envisioning embodied future space for robotics manipulation. _arXiv preprint arXiv:2501.01895_ , 2025. 2 

- [35] Zhaoyang Huang, Xiaoyu Shi, Chao Zhang, Qiang Wang, Ka Chun Cheung, Hongwei Qin, Jifeng Dai, and Hongsheng Li. Flowformer: A transformer architecture for optical flow. In _European Conference on Computer Vision (ECCV)_ , 2022. 3 

- [36] Quan Huynh-Thu and Mohammed Ghanbari. Scope of validity of psnr in image/video quality assessment. _Electronics letters_ , 2008. 5 

- [37] Zhenyu Jiang, Cheng-Chun Hsu, and Yuke Zhu. Ditto: Building digital twins of articulated objects from interaction. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 5616–5626, 2022. 1 

- [38] Philipp Jund, Chris Sweeney, Nichola Abdo, Zhifeng Chen, and Jonathon Shlens. Scalable scene flow from point clouds in the real world. _IEEE Robotics and Automation Letters (RA-L)_ , 2021. 3 

- [39] Łukasz Kaiser, Mohammad Babaeizadeh, Piotr Miłos, Bła˙zej Osi´nski, Roy H Campbell, Konrad Czechowski, Dumitru Erhan, Chelsea Finn, Piotr Kozakowski, Sergey Levine, et al. Model based reinforcement learning for atari. In _International Conference on Learning Representations (ICLR)_ , 2020. 1, 2 

- [40] Anssi Kanervisto, Dave Bignell, Linda Yilin Wen, Martin Grayson, Raluca Georgescu, Sergio Valcarcel Macua, Shan Zheng Tan, Tabish Rashid, Tim Pearce, Yuhan Cao, Abdelhak Lemkhenter, Chentian Jiang, Gavin Costello, Gunshi Gupta, Marko Tot, Shu Ishida, Tarun Gupta, Udit Arora, Ryen W. White, Sam Devlin, Cecily Morrison, and 

Katja Hofmann. World and human action models towards gameplay ideation. _Nature_ , 2025. 1, 2 

- [41] Harini Kannan, Danijar Hafner, Chelsea Finn, and Dumitru Erhan. Robodesk: A multi-task reinforcement learning benchmark, 2021. 2, 7 

- [42] Ishan Khatri, Kyle Vedder, Neehar Peri, Deva Ramanan, and James Hays. I can’t believe it’s not scene flow! In _European Conference on Computer Vision (ECCV)_ , 2024. 3 

- [43] Po-Chen Ko, Jiayuan Mao, Yilun Du, Shao-Hua Sun, and Joshua B Tenenbaum. Learning to act from actionless videos through dense correspondences. In _International Conference on Learning Representations (ICLR)_ , 2023. 2, 3, 4 

- [44] Guillaume Le Moing, Jean Ponce, and Cordelia Schmid. Dense optical tracking: connecting the dots. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 3 

- [45] Qixiu Li, Yaobo Liang, Zeyu Wang, Lin Luo, Xi Chen, Mozheng Liao, Fangyun Wei, Yu Deng, Sicheng Xu, Yizhong Zhang, et al. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. _arXiv preprint arXiv:2411.19650_ , 2024. 13 

- [46] Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 5, 13 

- [47] Jessy Lin, Yuqing Du, Olivia Watkins, Danijar Hafner, Pieter Abbeel, Dan Klein, and Anca Dragan. Learning to model the world with language. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

- [48] Yancong Lin and Holger Caesar. Icp-flow: Lidar scene flow estimation with icp. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 3 

- [49] Xingyu Liu, Charles R Qi, and Leonidas J Guibas. Flownet3d: Learning scene flow in 3d point clouds. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2019. 3 

- [50] Bruce D Lucas and Takeo Kanade. An iterative image registration technique with an application to stereo vision. In _International Joint Conference on Artificial Intelligence (IJCAI)_ , 1981. 3 

- [51] Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters (RA-L)_ , 2023. 2, 5 

- [52] Aniruddha Mahapatra and Kuldeep Kulkarni. Controllable animation of fluid elements in still images. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 2 

- [53] Vincent Micheli, Eloi Alonso, and Franc¸ois Fleuret. Transformers are sample-efficient world models. In _International Conference on Learning Representations (ICLR)_ , 2023. 2 

- [54] Vincent Micheli, Eloi Alonso, and Franc¸ois Fleuret. Efficient world models with context-aware tokenization. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

10 

- [55] Matthias Minderer, Chen Sun, Ruben Villegas, Forrester Cole, Kevin P Murphy, and Honglak Lee. Unsupervised learning of object structure and dynamics from videos. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. 7 

- [56] Iman Nematollahi, Erick Rosete-Beas, Seyed Mahdi B Azad, Raghu Rajan, Frank Hutter, and Wolfram Burgard. T3vip: Transformation-based 3d video prediction. In _International Conference on Intelligent Robots and Systems (IROS)_ , 2022. 2 

- [57] Haomiao Ni, Changhao Shi, Kai Li, Sharon X Huang, and Martin Renqiang Min. Conditional image-to-video generation with latent flow diffusion models. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 2 

- [58] Junhyuk Oh, Xiaoxiao Guo, Honglak Lee, Richard L Lewis, and Satinder Singh. Action-conditional video prediction using deep networks in atari games. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2015. 2 

- [59] Jack Parker-Holder, Philip Ball, Jake Bruce, Vibhavari Dasagi, Kristian Holsheimer, Christos Kaplanis, Alexandre Moufarek, Guy Scully, Jeremy Shar, Jimmy Shi, Stephen Spencer, Jessica Yung, Michael Dennis, Sultan Kenjeyev, Shangbang Long, Vlad Mnih, Harris Chan, Maxime Gazeau, Bonnie Li, Fabio Pardo, Luyu Wang, Lei Zhang, Frederic Besse, Tim Harley, Anna Mitenkova, Jane Wang, Jeff Clune, Demis Hassabis, Raia Hadsell, Adrian Bolton, Satinder Singh, and Tim Rockt¨aschel. Genie 2: A large-scale foundation world model, 2024. 1, 2 

- [60] Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In _AAAI Conference on Artificial Intelligence (AAAI)_ , 2018. 13 

- [61] Ren´e Ranftl, Alexey Bochkovskiy, and Vladlen Koltun. Vision transformers for dense prediction. In _International Conference on Computer Vision (ICCV)_ , 2021. 4 

- [62] Anurag Ranjan and Michael J Black. Optical flow estimation using a spatial pyramid network. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2017. 3 

- [63] Marc Rigter, Tarun Gupta, Agrin Hilmkil, and Chao Ma. Avid: Adapting video diffusion models to world models. _arXiv preprint arXiv:2410.12822_ , 2024. 1, 2, 4 

- [64] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2022. 1, 3, 4, 13 

- [65] Olaf Ronneberger, Philipp Fischer, and Thomas Brox. U- net: Convolutional networks for biomedical image segmentation. In _Medical image computing and computer-assisted intervention (MICCAI)_ , 2015. 4 

- [66] Julian Schrittwieser, Ioannis Antonoglou, Thomas Hubert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, et al. Mastering atari, go, chess and shogi by planning with a learned model. _Nature_ , 2020. 2 

- [67] Xiaoyu Shi, Zhaoyang Huang, Weikang Bian, Dasong Li, Manyuan Zhang, Ka Chun Cheung, Simon See, Hongwei Qin, Jifeng Dai, and Hongsheng Li. Videoflow: Exploiting temporal cues for multi-frame optical flow estimation. In _International Conference on Computer Vision (ICCV)_ , 2023. 3 

- [68] Xiaoyu Shi, Zhaoyang Huang, Dasong Li, Manyuan Zhang, Ka Chun Cheung, Simon See, Hongwei Qin, Jifeng Dai, and Hongsheng Li. Flowformer++: Masked cost volume autoencoding for pretraining optical flow estimation. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023. 3 

- [69] Xiaoyu Shi, Zhaoyang Huang, Fu-Yun Wang, Weikang Bian, Dasong Li, Yi Zhang, Manyuan Zhang, Ka Chun Cheung, Simon See, Hongwei Qin, et al. Motion-i2v: Consistent and controllable image-to-video generation with explicit motion modeling. In _ACM SIGGRAPH Conference Proceedings_ , 2024. 2 

- [70] Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli. Deep unsupervised learning using nonequilibrium thermodynamics. In _International Conference on Machine Learning (ICML)_ , 2015. 1, 3 

- [71] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models. _arXiv preprint arXiv:2010.02502_ , 2020. 1, 2, 3, 4 

- [72] Deqing Sun, Xiaodong Yang, Ming-Yu Liu, and Jan Kautz. Pwc-net: Cnns for optical flow using pyramid, warping, and cost volume. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pages 8934–8943, 2018. 3 

- [73] Ruixiang Sun, Hongyu Zang, Xin Li, and Riashat Islam. Learning latent dynamic robust representations for world models. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

- [74] Richard S Sutton. Dyna, an integrated architecture for learning, planning, and reacting. _ACM Sigart Bulletin_ , 1991. 2 

- [75] Zachary Teed and Jia Deng. Raft: Recurrent all-pairs field transforms for optical flow. In _European Conference on Computer Vision (ECCV)_ , 2020. 3, 14 

- [76] Zachary Teed and Jia Deng. Raft-3d: Scene flow using rigidmotion embeddings. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2021. 4, 14 

- [77] Stephen Tian, Chelsea Finn, and Jiajun Wu. A controlcentric benchmark for video prediction. In _International Conference on Learning Representations (ICLR)_ , 2023. 2, 6, 7, 13 

- [78] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 5 

- [79] Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion models are real-time game engines. _arXiv preprint arXiv:2408.14837_ , 2024. 2 

- [80] Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 3 

- [81] Kyle Vedder, Neehar Peri, Nathaniel Eliot Chodosh, Ishan Khatri, ERIC EATON, Dinesh Jayaraman, Yang Liu, Deva 

11 

Ramanan, and James Hays. Zeroflow: Scalable scene flow via distillation. In _International Conference on Learning Representations (ICLR)_ , 2024. 3 

- [82] Sundar Vedula, Simon Baker, Peter Rander, Robert Collins, and Takeo Kanade. Three-dimensional scene flow. In _International Conference on Computer Vision (ICCV)_ , 1999. 2, 3 

- [83] Ruben Villegas, Arkanath Pathak, Harini Kannan, Dumitru Erhan, Quoc V Le, and Honglak Lee. High fidelity video prediction with large stochastic recurrent neural networks. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2019. 7 

- [84] Vikram Voleti, Alexia Jolicoeur-Martineau, and Chris Pal. Mcvd-masked conditional video diffusion for prediction, generation, and interpolation. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 7 

- [85] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. Image quality assessment: from error visibility to structural similarity. _Transactions on Image Processing (TIP)_ , 2004. 5 

- [86] A Waswani, N Shazeer, N Parmar, J Uszkoreit, L Jones, A Gomez, L Kaiser, and I Polosukhin. Attention is all you need. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 4 

   - [95] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2018. 5 

   - [96] Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3dvla: A 3d vision-language-action generative world model. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

   - [97] Siyuan Zhou, Yilun Du, Jiaben Chen, YANDONG LI, DitYan Yeung, and Chuang Gan. Robodreamer: Learning compositional world models for robot imagination. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

   - [98] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: Learning interactive realrobot action simulators. _arXiv preprint arXiv:2406.14540_ , 2024. 1, 2, 4, 13 

   - [99] Yuke Zhu, Josiah Wong, Ajay Mandlekar, Roberto Mart´ınMart´ın, Abhishek Joshi, Soroush Nasiriany, and Yifeng Zhu. robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv:2009.12293_ , 2020. 2, 6 

- [87] Jialong Wu, Shaofeng Yin, Ningya Feng, Xu He, Dong Li, Jianye Hao, and Mingsheng Long. ivideogpt: Interactive videogpts are scalable world models. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2024. 1, 2, 7, 8 

- [88] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on Robot Learning (CoRL)_ , 2022. 2 

- [89] Yuxi Xiao, Qianqian Wang, Shangzhan Zhang, Nan Xue, Sida Peng, Yujun Shen, and Xiaowei Zhou. Spatialtracker: Tracking any 2d pixels in 3d space. In _The IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 3 

- [90] Mengda Xu, Zhenjia Xu, Yinghao Xu, Cheng Chi, Gordon Wetzstein, Manuela Veloso, and Shuran Song. Flow as the cross-domain manipulation interface. In _Conference on Robot Learning (CoRL)_ , 2024. 3, 4 

- [91] Zhenjia Xu, Zhanpeng He, Jiajun Wu, and Shuran Song. Learning 3d dynamic scene representations for robot manipulation. In _Conference on Robot Learning (CoRL)_ , 2020. 2, 4 

- [92] Gengshan Yang and Deva Ramanan. Volumetric correspondence networks for optical flow. _Advances in Neural Information Processing Systems (NeurIPS)_ , 32, 2019. 3 

- [93] Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao, Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao. Depth anything v2. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 4, 14 

- [94] Sherry Yang, Yilun Du, Seyed Kamyar Seyed Ghasemipour, Jonathan Tompson, Leslie Pack Kaelbling, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. In _International Conference on Learning Representations (ICLR)_ , 2024. 1, 2 

12 

## **A. Implementation Details** 

**Details of the dynamics prediction module.** Our FlowDreamer utilizes a conditional 2D U-Net with 4 downsample and upsample layers as the dynamics prediction module. The action condition is integrated with image features via cross-attention, which is similar to Stable Diffusion. We also design a conditional MinkowskiNet [13] as a point-cloud-based baseline. The structure of the conditional MinkowskiNet is modified from MinkUNet34B in the official repository, where we replace the batch normalization layers in the basic blocks with Feature-wise Linear Modulation (FiLM) [60] layers to introduce action condition. **Training and inference details.** We conduct all our experiments on an NVIDIA A800 cluster. Each model is trained on 8 GPUs in parallel, with a batch size of 16 per GPU. The denoising U-Net and the image encoder/decoder are loaded from Stable Diffusion 2.1 [64]. We only finetune the parameters of the denoising network yet freeze the weight of the encoder and decoder. All models are trained for 60k steps with a constant learning rate of 1e-4. We use AdamW optimizer for training, and we use a mixed precision with FP16 and FP32 supported by Pytorch-Lightning. For diffusion models, we utilize a PNDM scheduler with 20 sampling steps during inference. We notice that increasing sampling steps more than 20 cannot improve the accuracy of future prediction yet is more time-consuming. The output resolution is relevant to the dataset, which will be reported in the next section. 

## **B. Data Collection** 

In the main paper, we conduct experiments on 4 different simulation environments. To train world models on these environments, we need to collect feasible trajectories and calculate the ground truth 3D scene flow. Also, we conduct experiments on RT-1 real dataset, where we estimate the depth and the scene flow through depth estimators and flow estimators. Table 4 shows the dataset statistics in detail. This section will introduce the data collection pipeline. 

|Dataset|Resolution|Episode|Sample|
|---|---|---|---|
|RT-1 SimplerEnv|320_×_256|25,000|758,015|
|Language Table|512_×_288|36,000|1,447,805|
|RoboDesk|320_×_320|35,000|1,190,000|
|Robosuite|256_×_256|50,000|1,749,825|
|RT-1 Real|320_×_256|86,403|3,638,016|


Table 4. **Dataset statistics.** An “episode” refers to a complete trajectory where the robot completes a task. A “sample” refers to a frame pair at timestep _t_ and _t_ + 1 with a robot action **a** _t_ . 

**Trajectory collection.** For the RT-1 SimplerEnv environment, we choose 5 tasks implemented by Sim- 

plerEnv [46]: _pick_ _~~c~~ oke_ _~~c~~ an, pick_ _~~o~~ bject, move_ _~~n~~ ear, open_ _~~d~~ rawer, close_ _~~d~~ rawer_ , and generate 5k trajectories for each task. The action trajectory is generated by CogACT [45], a foundational vision-language-action model. We only sample successful trajectories and discard failed trajectories. For the Language Table environment, we generate trajectories by the RRT* oracle policy provided in the official repositories. The task instruction format is “ _push {block A} to {block B}_ ”. For RoboDesk and Robosuite tasks, we use the trajectories provided by VP<sup>2</sup> benchmark [77]. We load the provided initial states and actions into the simulator to collect RGB-D and flow information. Note that the observation of RoboDesk is a resized and cropped image from the original observation, which would affect the flow calculation. Our world model trains and predicts based on the original observation and crops the predicted observation to calculate the visual planning reward. The RT-1 real-world dataset is provided by the original paper [6], and we choose the preprocessed version by IRASim [98]. 

**Scene flow obtainment.** For all simulation environments, we can extract the ground truth scene flow from the simulator. Specifically, all objects in the simulator are rigid bodies or articulated objects, whose _pose_ at each timestep _t_ could be represented by a 4 _×_ 4 homogeneous transformation matrix _Tt_ . Therefore, we can calculate the position of a point at timestep _t_ + 1, with the position at timestep _t_ and the corresponding pose matrices: 


where **x** _t_ and **x** _t_ +1 are 3D point coordinates at timestep _t_ and _t_ + 1. Then the scene flow can be calculated by _ft→t_ +1 = **x** _t_ +1 _−_ **x** _t_ . 


Figure 8. **Scene flow obtainment pipeline on the real-world dataset.** The consistent metric depth is estimated by Video Depth Anything and Depth Anything v2, and the 3D scene flow is estimated by RAFT-3D and refined by RAFT. 

For RT-1 real world datasets, as there is no ground truth depth or pose matrix, we apply some depth estima- 

13 

Table 5. **Video prediction results on RT-1 real-world dataset.** We categorize the metrics into three groups: semantic similarity, pixel similarity, and media quality. **Bold** numbers indicate the best results. 

|**Method**|**Semantic**|**Similarity**|**Pi**|**xel Similari**|**ty**|**Media**|**Quality**|
|---|---|---|---|---|---|---|---|
||DINOv2 L2↓|CLIP score↑|PSNR↑|SSIM↑|LPIPS↓|FID↓|FVD↓|
|Vanilla|15.6659|0.8618|17.9724|0.5401|0.1882|13.1636|195.3965|
|Ours|**15.5710**|**0.8687**|**18.6574**|**0.5532**|**0.1764**|**10.4547**|**191.3314**|


tion model: Depth Anything v2 [93] and Video Depth Anything [12] to estimate the metric depth, and utilize some flow estimation model: RAFT [75] and RAFT-3D [76] to estimate the 3D scene flow. The pipeline is illustrated in Fig. 8. Specifically, we first obtain the relative depths using Video Depth Anything, which can produce spatially and temporally coherent depths across frames. To get metric depths, we utilize Depth Anything V2 to estimate the metric depths and align the two depth maps by computing scale and shift parameters. Next, we input the aligned metric depth along with the RGB image into RAFT-3D to obtain frame-paired 3D scene flows and use the estimation result of RAFT to refine the scene flow by producing a flow mask. 

only relies on current observations and actions, just aiming to demonstrate the effectiveness of explicit dynamics modeling. Finally, the inference of the diffusion model is relatively slow due to the progressive denoising framework, while diffusion models could achieve outstanding visual performance. Future works could explore a better tradeoff between inference time and prediction performance. 

## **C. Extended Experimental Results** 

In this section, we conduct real-world experiments to evaluate the feasibility of our pipeline. We conduct video prediction experiments on the real-world RT-1 robot manipulation dataset. The RT-1 real-world dataset contains more tasks, lighting conditions, and camera positions, making it a much harder task than on the simulation data. As there is no ground truth depth or scene flow, we leverage the estimation results as the training target. We compare FlowDreamer with the single-stage _Vanilla_ world model. 

Table 5 shows the performance of video prediction. FlowDreamer still performs better than _Vanilla_ , while the discrepancy becomes lower than simulation data. From the qualitative examples (see Fig. 9), we could see that the ground truth scene flows estimated by RAFT-3D are not accurate, which would introduce noise into the training target. Our FlowDreamer is affected by inaccurate supervision and produces inaccurate flow predictions. However, our performance still outperforms _Vanilla_ , as _Vanilla_ cannot even keep the consistency of the background during generation. 

## **D. Limitations and Future Works** 

While FlowDreamer has made progress, there are some limitations that could be improved by future works. First, our training data mainly come from simulation, as most of the robotic data are monocular RGB videos. Next, we did not consider any context or history in FlowDreamer, though adding more context does not conflict with our methodology. We provide a simple version of FlowDreamer that 

14 


Figure 9. **Qualitative results on the RT-1 real world dataset.** The depth is estimated by Depth Anything v2, and the flow in “GT” are estimated by RAFT-3D, making it a harder scenario. 

15 

