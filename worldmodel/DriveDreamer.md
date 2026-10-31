---
title: "DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving"
date: "2023-09-18"
authors: "Xiaofeng Wang; Zheng Zhu; Guan Huang; Xinze Chen; Jiagang Zhu; Jiwen Lu"
url: https://arxiv.org/abs/2309.09777
pdf: https://arxiv.org/pdf/2309.09777
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2309.09777)** / [論文ページ](https://arxiv.org/abs/2309.09777)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving** 

Xiaofeng Wang<sup>*1</sup> Zheng Zhu<sup>*1�</sup> Guan Huang<sup>1,2</sup> Xinze Chen<sup>1</sup> Jiagang Zhu<sup>1</sup> Jiwen Lu<sup>2</sup> 1GigaAI 2Tsinghua University 

Project Page: https://drivedreamer.github.io 


Figure 1. _DriveDreamer_ demonstrates a comprehensive understanding of driving scenarios. It excels in controllable driving video generation, aligning seamlessly with text prompts and structured traffic constraints. _DriveDreamer_ can also interact with the driving scene and predict different future driving videos, based on input actions. Furthermore, _DriveDreamer_ extends its utility to anticipate future actions. 

## **Abstract** 

_World models, especially in autonomous driving, are trending and drawing extensive attention due to their capacity for comprehending driving environments. The established world model holds immense potential for the generation of high-quality driving videos, and driving policies for safe maneuvering. However, a critical limitation_ 

_in relevant research lies in its predominant focus on gaming environments or simulated settings, thereby lacking the representation of real-world driving scenarios. Therefore, we introduce DriveDreamer, a pioneering world model entirely derived from real-world driving scenarios. Regarding that modeling the world in intricate driving scenes entails an overwhelming search space, we propose harnessing the_ 

1 

_powerful diffusion model to construct a comprehensive representation of the complex environment. Furthermore, we introduce a two-stage training pipeline. In the initial phase, DriveDreamer acquires a deep understanding of structured traffic constraints, while the subsequent stage equips it with the ability to anticipate future states. The proposed DriveDreamer is the first world model established from realworld driving scenarios. We instantiate DriveDreamer on the challenging nuScenes benchmark, and extensive experiments verify that DriveDreamer empowers precise, controllable video generation that faithfully captures the structural constraints of real-world traffic scenarios. Additionally, DriveDreamer enables the generation of realistic and reasonable driving policies, opening avenues for interaction and practical applications._ 

## **1. Introduction** 

Spurred by insights from AGI (Artificial General Intelligence) and the principles of embodied AI, a profound transformation in autonomous driving is underway. Autonomous vehicles rely on sophisticated systems that engage with and comprehend the real driving world. At the heart of this evolution is the integration of world models [15,17–19]. World models hold great promise for generating diverse and realistic driving videos, encompassing even long-tail scenarios, which can be utilized to train various driving perception approaches. Furthermore, the predictive capabilities in world models facilitate end-to-end driving, ushering in a new era of autonomous driving experiences. 

Deriving latent dynamics of world models from visual signals was initially introduced in video prediction [8, 11, 19]. By extrapolating from observed visual sequences, video prediction methods can infer future states of the environment, effectively modeling how objects and entities within a scene will evolve over time. However, modeling the intricate driving scenarios in pixel space is challenging due to the large sampling space [5, 7]. To alleviate this problem, recent research endeavors have sought innovative strategies to enhance sampling efficiency. ISO-Dream [52] explicitly disentangles visual dynamics into controllable and uncontrollable states. MILE [29] strategically incorporates world modeling within the Bird’s Eye View (BEV) semantic segmentation space, complementing world modeling with imitation learning. SEM2 [13] further extends the Dreamer framework into BEV segmentation maps, utilizing Reinforce Learning (RL) for training. Despite the progress witnessed in world models, a critical limitation in relevant research lies in its predominant focus on simulation environments. 

In this paper, we propose _DriveDreamer_ , which pioneers the construction of comprehensive world models from real driving videos and human driver behaviors. Considering the 

intricate nature of modeling real-world driving scenes, we introduce the Autonomous-driving Diffusion Model ( _AutoDM_ ), which empowers the ability to create a comprehensive representation of the complex driving environment. We propose a two-stage training pipeline. In the first stage, we train _Auto-DM_ by incorporating traffic structural information as intermediate conditions, which significantly enhances sampling efficiency. Consequently, _Auto-DM_ exhibits remarkable capabilities in comprehending real-world driving scenes, particularly concerning the dynamic foreground objects and the static background. In the secondstage training, we establish the world model through video prediction. Specifically, driving actions are employed to iteratively update future traffic structural conditions, which enables _DriveDreamer_ to anticipate variations in the driving environment based on different driving strategies. Moreover, _DriveDreamer_ extends its predictive prowess to foresee forthcoming driving policies, drawing from historical observations and _Auto-DM_ features. Thus creating a executable, and predictable driving world model. 

The main contributions of this paper can be summarized as follows: (1) We introduce _DriveDreamer_ , which is the first world model derived from real-world driving scenarios. _DriveDreamer_ can jointly enable the generation of high-quality driving videos and reasonable driving policies. (2) To enhance the comprehension of real-world driving scenes and expedite the world model convergence, we introduce the Autonomous-driving Diffusion Model and a two-stage training pipeline. The first-stage training enables the comprehension of traffic structural information, and the second-stage video prediction training empowers the predictive capacity. (3) _DriveDreamer_ can controllably generate driving scene videos that are highly aligned with traffic constraints (see Fig. 1), enhancing the training of driving perception methods (e.g., 3D detection). Besides, _DriveDreamer_ can generate future driving policies based on historical observations and _Auto-DM_ features. Notably, _DriveDreamer_ achieves promising planning results in open-loop assessments on the nuScenes dataset. 

## **2. Related Work** 

### **2.1. Diffusion Model** 

Diffusion models represent a family of probabilistic generative models that progressively introduce noise to data and subsequently learn to reverse this process for the purpose of generating samples [73]. These models have recently garnered significant attention due to their exceptional performance in various applications, setting new benchmarks in image synthesis [1, 14, 49, 55, 57], video generation [21, 23, 35, 60, 67, 74], and 3D content generation [6, 43, 53, 69]. To enhance the controllable generation capability, ControlNet [76], GLIGEN [42], T2I-Adapter [48] 

2 

and Composer [32] have been introduced to utilize various control inputs, including depth maps, segmentation maps, canny edges, and sketches. Concurrently, BEVControl [72], MagicDrive [12] and DrivingDiffuson [41] incorporate layout conditions to enhance image generation. The fundamental essence of diffusion-based generative models lies in their capacity to comprehend and understand the intricacies of the world. Harnessing the power of these diffusion models, _DriveDreamer_ seeks to comprehend the complex realm of autonomous-driving scenarios. 

### **2.2. Video Generation** 

Video generation and video prediction are effective approaches to understanding the visual world. In the realm of video generation, several standard architectures have been employed, including Variational Autoencoders (VAEs) [8,28], auto-regressive models [34,56,61,70], flowbased models [40], and Generative Adversarial Networks (GANs) [46, 58, 62, 65]. Recently, the burgeoning diffusion models [9, 24, 25, 49, 50, 57] have also been extended to the domain of video generation. Video diffusion models [21, 23, 35, 60, 67, 74] exhibit higher-quality video generation capabilities, producing realistic frames and transitions between frames while offering enhanced controllability. They accommodate various input control conditions such as text, canny, sketch, semantic maps, and depth maps. 

Video prediction models represent a specialized form of video generation models, sharing numerous similarities. In particular, video prediction involves anticipating future video changes based on historical video observations [8, 11, 19, 27, 64]. DriveGAN [36] establishes associations between driving actions and pixels, predicting future driving videos by specifying future driving policies. In contrast, _DriveDreamer_ incorporates structured traffic conditions, text prompts, and driving actions as inputs, empowering precise, realistic video and action generation that are faithfully aligned with real-world driving scenarios. 

### **2.3. World Models** 

World models have been extensively explored in modelbased imitation learning, demonstrating remarkable success in various applications [15–20, 37, 44, 59, 71]. These approaches typically leverage Variational Autoencoders (VAE) [39] and Long Short-Term Memory (LSTM) [26] to model transition dynamics and rendering functionality. World methods target at establishing dynamic models of environments, enabling agents to be predictive of the future. This aspect is of paramount importance in autonomous driving, where precise predictions about the future are essential for safe maneuvering. However, constructing world models in autonomous driving presents unique challenges, primarily due to the high sample complexity inherent in realworld driving tasks [5]. To address these problems, ISO- 


Figure 2. Two-stage training pipeline of _DriveDreamer_ . 

Dream [52] introduces an explicit disentanglement of visual dynamics into controllable and uncontrollable states. MILE [29] strategically incorporates world modeling within the BEV semantic segmentation space, enhancing world modeling through imitation learning. SEM2 [13] extends the Dreamer framework into BEV segmentation maps, employing reinforcement learning for training. Despite the progress witnessed in world models, a critical limitation in relevant research lies in its predominant focus on simulation environments. The transition to real-world driving scenarios remains an under-explored frontier. 

## **3. DriveDreamer** 

The overall framework of _DriveDreamer_ is depicted in Fig 3. The framework begins with an initial reference frame _I_ 0 and its corresponding road structural information ( _i.e_ ., HDMap _H_ 0 and 3D box _B_ 0). Within this context, _DriveDreamer_ leverages the proposed _ActionFormer_ to predict forthcoming road structural features in the latent space. These predicted features serve as conditions and are provided to _Auto-DM_ , which generates future driving videos. Simultaneously, the utilization of text prompts allows for dynamic adjustments to the driving scenario style ( _e.g_ ., weather and time of the day). Moreover, _DriveDreamer_ incorporates historical action information and the multi-scale latent features extracted from _Auto-DM_ , which are combined to generate reasonable future driving actions. In essence, _DriveDreamer_ offers a comprehensive framework that seamlessly integrates multi-modal inputs to generate future driving videos and driving policies, thereby advancing the capabilities of autonomous-driving systems. 

Regarding the extensive search space of establishing world models in real-world driving scenarios, we introduce a two-stage training strategy for _DriveDreamer_ . This strategy is designed to significantly enhance sampling efficiency and expedite model convergence. The two-stage training is 

3 


Figure 3. Overall framework of _DriveDreamer_ . The framework initiates with reference frame _I_ 0 and road structural information (i.e., HDMap _H_ 0 and 3D box _B_ 0). _DriveDreamer_ employs the _ActionFormer_ to predict future road structural features, which serve as conditions provided to _Auto-DM_ , generating future driving videos _I_<sup>ˆ</sup> _i_<sup>_N_</sup> =0<sup>_−_1.Additionally, text prompts enable dynamic scenario style adjustments.The</sup> model integrates past driving actions and multi-scale features from _Auto-DM_ to generate plausible future driving actions _A_<sup>ˆ</sup><sup>_N_</sup> _i_ =<sup>+</sup> _N_<sup>_M_.</sup> 

illustrated in Fig. 2. There are two steps in the first-stage training. Step 1 involves utilizing the single-frame structured condition, which guides _DriveDreamer_ to generate driving scene image, facilitating its comprehension of structural traffic constraints. Step 2 extends its understanding into video generation. The second-stage training enables _DriveDreamer_ to interact with the environment and predict future states effectively. This phase takes an initial frame image along with its corresponding structured information as input. Simultaneously, sequential driving actions are provided, with the model expected to generate future driving videos and future driving actions. In the following sections, we delve into the specifics of the model architecture and training pipelines. 

### **3.1. First-stage Training** 

**_Auto-DM_ .** In _DriveDreamer_ , we introduce _Auto-DM_ , to model and comprehend driving scenarios from real-world driving videos. It is noted that comprehending driving scenes solely from pixel space presents challenges due to extensive search space in real-world driving scenarios. To mitigate this, we explicitly incorporate structured traffic information as conditional inputs. 

The overall structure of _Auto-DM_ is illustrated in Fig. 4, where traffic conditions are projected onto the image plane, generating HDMap conditions _{Hi}_<sup>_N_</sup> _i_ =0<sup>_−_1</sup> _∈R_<sup>_N×H×W ×_3</sup> , and 3D boxes conditions _{Bi}_<sup>_N_</sup> _i_ =0<sup>_−_1</sup> _∈R_<sup>_N×NB×_16</sup> , along with the box categories _{Ci}_<sup>_N_</sup> _i_ =0<sup>_−_1</sup> _∈R_<sup>_N×NB_</sup> ( _N_ is the 

number of video frames, and _NB_ is the predefined maximum box numbers with zero padded). In this following, unless specified, the subscript _i_ is omitted for readability. To enable controllability, the spatially aligned conditions _H_ are encoded by convolution layers and then concatenated with _Zt_ , where _{Zt}_<sup>_N_</sup> _i_ =0<sup>_−_1are noisy latent features generated</sup> by the forward diffusion process [57]. For position conditions ( _i.e_ ., 3D boxes) that are not spatially aligned with _Zt_ , we first aggregate position embeddings _H_<sup>_p_</sup> : 


where _Fa_ is MLP layers, _Ce_ is CLIP [54] embed box categories features, Fourier( _·_ ) is Fourier embedding [47], and [ _·_ ] is the concatenation operation. Then _gated self-attention_ [42] is leveraged to integrate position embeddings _H_<sup>_p_</sup> with visual signals _v_ from the original UNet features [57]: 


where _η_ is a learnable parameter, _Fs_ is self-attention, and TS( _·_ ) is the token selection operation that considers visual tokens only [42]. 

To further empower _Auto-DM_ with comprehension of driving dynamics, we introduce temporal attention layers _Ft_ to enhance frame coherence in the generated videos: 


where we first reshape the visual signal _v_ from _R_<sup>_N×C×H×W_</sup> to _R_<sup>_C×NHW_</sup> . The shape transformation 

4 


Figure 4. Overall structure of the _Auto-DM_ . _Auto-DM_ takes three types of control conditions as inputs. Spatially aligned conditions ( _i.e_ ., HDMap _Hi_<sup>_N_</sup> =0<sup>_−_1), are concatenated with noise images and fed into the diffusion steps.Position conditions, represented by 3D boxes</sup> _Bi_<sup>_N_</sup> =0<sup>_−_1and their labels, are flattened and utilized in the gated self-attention.Text prompts are incorporated into diffusion steps using cross-</sup> attention, influencing the style of the generated driving video. Temporal attention layers are employed to ensure the consistency of the generated video frames. The diffusion steps estimate noise and generate loss with the input noise to optimize _Auto-DM_ . 

facilitates the frame-wise self-attention layers _Fs_ to learn inter-frame dynamics. _T_ pose denotes temporal position embeddings that are encoded by sinusoidal function [2]. Finally, we restore the visual signal to its original dimensions, thus ensuring the feature integrity. Notably, the same architecture can be extended to generate multi-view images (see Fig. 6), where the _Fs_ solely attends to neighbor views. Additionally, a stack of frame-wise attention and view-wise attention contributes to multi-view video generation (see supplement for more details). 

Furthermore, cross-attention layers [57] are utilized to facilitate feature interactions between text inputs and visual signals, empowering text descriptions to influence driving scene attributes such as weather and time of day. In the next, we will elaborate on the first-stage training pipeline, which involves two steps. 

**Step 1 training.** The _Auto-DM_ incorporates input solely from a single frame of structured traffic conditions, coupled with supervision from a single-frame image. For structured traffic conditions, HDMaps and 3D boxes are obtained either from human annotations or pertained perception methods ( _e.g_ ., LAV [4], BEVerse [77], UniAD [31]). Then threechannel HDMaps (lane boundary, lane divider, and pedestrian crossing) and eight-corner 3D boxes are projected onto the image plane to generate corresponding conditions. Notably, during step 1 training, temporal attention layers are omitted, which enables the network to focus exclusively on learning the traffic structural constraints, expediting the convergence of the training process. 

**Step 2 training.** The _Auto-DM_ incorporates input from 

multiple frames of structured traffic conditions and is supervised using driving videos. In contrast to step 1, learning from videos allows _Auto-DM_ to gain a deeper understanding of the intricate motion transitions in driving scenarios. Building upon the pretrained models established in step 1, step 2 incorporates temporal attention layers into the model architecture. These additional parameters enable the _AutoDM_ to focus on the temporal dynamics present in the input data, further enhancing its ability to capture and interpret the nuanced temporal aspects of driving scenes. 

In step 1 and step 2 training, the proposed _Auto-DM_ is trained using the same noise schedule as the underlying image model [57]. Specifically, the forward process gradually adds noise _ϵ_ to the latent feature _Z_ 0, resulting in the noisy latent feature _ZT_ . Then we train _ϵϕ_ to predict the noise we added, and the trainable parameters _ϕ_ are optimized via: 


where _ϕ_ denotes the trainable parameters involved in the gated self-attention, temporal attention, and cross-attention layers, and time step _t_ is uniformly sampled from [1 _, T_ ]. 

### **3.2. Second-stage Training** 

Based on the first-stage training, _DriveDreamer_ has obtained comprehension of the structured traffic information. However, the desired world model should also be predictive of the future and can interact with the environment. Therefore, we embark on the second phase of our approach. In this phase, we leverage the video prediction task to establish 

5 


Figure 5. Overall structure of _ActionFormer_ . The initial structural conditions _H_ 0 and _B_ 0 are first encoded and flattened into a 1D latent space. These latent features are then concatenated and processed through self-attention and MLP layers, generating the hidden state. Cross-attention layers establish associations between hidden states and driving actions. Gated Recurrent Units (GRUs) are employed to iteratively predict future hidden states. These predicted hidden states are further concatenated with action features and decoded into future traffic structural conditions to be fed into _Auto-DM_ . 

the driving world model. Specifically, the video prediction task entails providing an initial observation _I_ 0 _, H_ 0 _, B_ 0, as well as driving actions _{Ai}_<sup>_T_</sup> _i_ =0<sup>_−_1, with the desired outcome</sup> being the future driving videos _{Ii}_<sup>_T_</sup> _i_ =1<sup>,and future driving</sup> actions _{Ai}_<sup>_T_</sup> _i_ =<sup>+</sup> _T_<sup>_N_.</sup> 

**_ActionFormer_ .** Recall that the trained _Auto-DM_ can generate driving videos _{Ii}_<sup>_T_</sup> _i_ =0<sup>based on sequential structured</sup> information _{Hi}_<sup>_T_</sup> _i_ =0<sup>_, {Bi}T_</sup> _i_ =0<sup>.However, in the video pre-</sup> diction task, future traffic structural conditions beyond the present timestamp is unavailable. To address this challenge, we introduce the _ActionFormer_ , which leverages driving actions _{Ai}_<sup>_T_</sup> _i_ =0<sup>_−_1to iteratively predict future structural condi-</sup> tions. The overall architecture of _ActionFormer_ is in Fig. 5. Firstly the initial structural conditions _H_ 0 _, B_ 0 are encoded and flattened into 1D latent space. The latent features are concatenated and aggregated by self-attention and MLP layers to generate the hidden state **h** 0. Subsequently, crossattention layers _Fca_ are utilized to construct associations between hidden states and driving actions. Then latent variable **s** _t_ is parameterized as: 


where _µθ, σθ_ are layers to learn Gaussian parameters. To predict future hidden states, we employ Gated Recurrent 


These hidden states are concatenated with action features and are decoded into future traffic structural conditions. It’s noted that the _Actionformer_ forecasts future traffic conditions at the feature level, which mitigates noise interference at the pixel level, resulting in more robust predictions. Besides the traffic structural conditions generated by _Actionformer_ and the text prompt condition, we process the reference image condition _I_ 0 similar to [2]. Based on the above conditions, we extend _Auto-DM_ to jointly generate future driving videos _{Ii}_<sup>_T_</sup> _i_ =1<sup>anddrivingactions</sup><sup>_{Ai}T_</sup> _i_ =<sup>+</sup> _T_<sup>_N_.We</sup> formalize this process as a generative probabilistic model, where the joint probability can be factorized as: 


where 


_p_ ( _AT_ : _T_ + _N |_ **h** 0: _T ,_ **s** 0: _T −_ 1 _, A_ 0: _T −_ 1 _, I_ 0) _._ 

6 

Considering updating hidden states _p_ ( **h** _t |_ **h** _t−_ 1 _,_ **s** _t−_ 1) is a deterministic process (Eq. 6), only latent variables **s** _t_ are needed to be inferred to maximize the marginal likelihood of observation _p_ ( _I_ 1: _T , AT_ : _T_ + _N_ ). Therefore, variational distribution _q_ vd is introduced to conduct variational inference: 


Note that the posterior and prior matching [29] is not included, as we empirically find the simplified variational lower bound produces similar plausible results. In Eq. 10, the video prediction and action prediction parts can be modeled by Gaussian distributions _N_ ( _G_ ( **h** 0: _T , A_ 0: _T −_ 1 _, I_ 0) _,_ **I** ) and Laplace distribution Laplace( _π_ ( **h** 0: _T , A_ 0: _T −_ 1 _, I_ 0) _,_ 1). Therefore, we employ mean-squared error and _L_ 1 loss to optimize the video prediction training. _G_ , _π_ are learnable layers involved in _ActionFormer_ , _Auto-DM_ , video decoder ( _i.e_ ., VAE decoder) and action decoder. For action prediction details, we first pool multi-scale UNet features from _Auto-DM_ . The pooled features are concatenated with historical action features, which are then decoded by MLP layers to generate future driving actions. 

Based on the two-stage training, _DriveDreamer_ has acquired a comprehensive understanding of the driving world, encompassing the structural constraints of traffic, predictions of future driving states, and interaction with the established world model. 

## **4. Experiment** 

### **4.1. Experiment Details** 

**Dataset.** The training data is sourced from the real-world driving dataset nuScenes [3], comprising a total of 700 training videos and 150 validation videos. Each video includes _∼_ 20 seconds of footage captured by six surroundview cameras. The videos have a frame rate of 12Hz, resulting in _∼_ 1M video frames available for training. During the first-stage training, we utilize the nuScenes-devkit [51] to acquire HDMap annotations (lane boundary, lane divider, and pedestrian crossing) corresponding to 12Hz frames, which are then projected onto the image plane. Considering the nuScenes dataset only provides 2Hz 3D bounding box annotations, we supplement this with 12Hz bounding 

box annotations from [68]. In the second-stage training, we employ the yaw angle and velocity of the ego-car as the driving action inputs. Besides, we extract scene description information ( _e.g_ ., weather and time) from the nuScenes annotation, which serves as text conditions. 

**Training.** The proposed _Auto-DM_ is built upon Stable Diffusion v1.4 [57], whose original parameters are frozen. In step 1 of first-stage training, our model is trained for 40 epochs with a batch size of 16. In step 2, _Auto-DM_ is trained for 10 epochs with a batch size of 1, with video frame length _N_ = 32, and spatial size of 448 _×_ 256. During second-stage video prediction training, our model predicts 16 frame driving videos _I_ 1:16 and 16 future driving actions _I_ 17:32, and the model is trained for 10 epochs on a batch size of 1. All the experiments are conducted on A800 GPUs, and we use the AdamW optimizer [38] with a learning rate 5 _×_ 10<sup>_−_5</sup> . **Evaluation.** We conducted a comprehensive evaluation of the proposed _DriveDreamer_ , employing both qualitative and quantitative assessments. We utilized frame-wise Fr´echet Inception Distance (FID) [22] and Fr´echet Video Distance (FVD) [63] to evaluate the generation quality, where the evaluated image is resized to 448 _×_ 256. Besides, to verify the generated images enhance the training of driving perception methods, _DriveDreamer_ is evaluated through 3D object detection, with FCOS3D [66] and BEVFusion [45] as baseline methods. Furthermore, we test the performance of driving policy generation. Following the settings in [30], we evaluate output driving trajectories for future 3 seconds. 

### **4.2. Controllable Driving Video Generation** 

The proposed _DriveDreamer_ exhibits a profound comprehension of driving scenarios, capable of controllably generating diverse driving videos. In this subsection, we first demonstrate that, based on first-stage training, _DriveDreamer_ can generate diverse driving videos under structured traffic conditions. Besides, we verify that the generated images can enhance the training of driving perception methods. Furthermore, _DriveDreamer_ showcases its versatility by responding to different input actions, allowing for the control of the vehicle’s trajectory and consequently generating diverse driving videos. 

As shown in Fig. 1 and Fig 6, _DriveDreamer_ exhibits proficiency in producing images and videos that adhere meticulously to structured traffic conditions (more visualizations are in supplement). Significantly, we can also manipulate the text prompt to induce variations in the generated videos, encompassing changes in weather and time of day. To further validate the generation quality, we extract 4K traffic conditions (from the nuScenes training set) to generate driving images. The generated images are combined with real images for training the 3D detection task. Results in Tab. 1 indicate that training with our synthetic 

7 


Figure 6. Visualizations of generated multi-view images, where the generation conditions (HDMaps, 3D boxes) are from nuScenes validation set. Regions highlighted by red rectangles and yellow circles indicate that the generated images share multi-view consistency and are aligned with ground truth conditions. 

|Methods|Resolution|Data|mAP(_↑_)|NDS(_↑_)|
|---|---|---|---|---|
|FCOS3D [66]|1600_×_900|w/o synthetic data|30.2|38.1|
|FCOS3D [66]|1600_×_900|w 4K synthetic data|**30.9**(+0.7)|**38.3**(+0.2)|
|BEVFusion [45]|704_×_256|w/o synthetic data|32.8|37.6|
|BEVFusion [45]|704_×_256|w 4K synthetic data|**35.8**(+3.0)|**39.5**(+1.9)|


Table 1. Performance of synthetic data augmentation on training 3D object detection. 

data significantly enhances the performance of 3D detection. Specifically, compared with training without synthetic data, the mAP metrics of FCOS3D and BEVFusion are improved by 0.7 and 3.0. 

In addition to the utilization of structured traffic conditions for generating driving videos, _DriveDreamer_ exhibits the capability to diversify the generated driving videos by adapting to different driving actions. As depicted in Fig. 1 (more visualizations are in supplement), starting from an initial frame paired with its corresponding structural information, _DriveDreamer_ can generate distinct videos based on various driving actions, such as videos depicting left and right turns. In summary, _DriveDreamer_ excels in producing a wide spectrum of driving scene videos, characterized by both high controllability and diversity. Thus, _DriveDreamer_ holds promise for training autonomous-driving systems across a wide range of tasks, encompassing even corner cases and long-tail scenarios. 

In the quantitative experiment, we extract ego-car driving actions from the nuScenes validation set as conditions to generate driving videos. For comparison, we train DriveGAN [36] on the nuScenes dataset, employing the same training settings as those used for _Drivedreamer_ . Besides, we train _Drivedreamer_ without _ActionFormer_ as a baseline 

|Methods|1st-stage train<br>(_Auto-DM_)|2nd-stage train<br>(_ActionFormer_)|FID (_↓_)|FVD (_↓_)|
|---|---|---|---|---|
|DriveGAN [36]|-|-|27.8|390.8|
|_DriveDreamer_|||15.9|363.3|
|_DriveDreamer_|✓||15.3|349.6|
|_DriveDreamer_|✓|✓|**14.9**|**340.8**|


Table 2. Comparison of generation quality on nuScenes validation. 

(specifically, the action features are directly concatenated with the zero-padded structured traffic conditions). The results are presented in Tab. 2, where we evaluate the quality of generated videos. Notably, our approach without firststage training achieves superior FID and FVD scores compared to DriveGAN. This observation underscores the effectiveness of leveraging a powerful diffusion model in visually comprehending driving scenarios. Furthermore, our findings reveal that _Drivedreamer_ after first-stage training, exhibits an improved understanding of the structured information within driving scenes, resulting in higher-quality video generation. Lastly, we observe that the proposed _ActionFormer_ effectively leverages the traffic structural information knowledge acquired during the first-stage training. Compared to the _concatenation_ baseline approach, the _ActionFormer_ iteratively updates future structured information based on input actions, which further enhances the quality of generated videos. 

### **4.3. Driving Action Generation** 

In addition to its capacity for generating highly controllable driving videos, _DriveDreamer_ demonstrates the ability to predict reasonable driving actions. As depicted in 

8 

|Method|Visual Info.|Action Info.|_L_2 Avg. (m)|Col. Avg. (%)|
|---|---|---|---|---|
|ST-P3 [30]|✓||2.11|0.71|
|UniAD [31]|✓||1.65|0.31|
|AD-MLP [75]||✓|**0.29**|0.19|
|VAD [33]|✓|✓|0.37|**0.14**|
|_DriveDreamer_|✓|✓|**0.29**|0.15|


Table 3. Open-loop planning performance on nuScenes validation set. The evaluation settings are the same as ST-P3 [30]. 

Fig. 1, provided with an initial frame condition and past driving actions, _DriveDreamer_ can generate future driving actions that align with real-world scenarios . Furthermore, we conduct a quantitative assessment of the prediction accuracy. Specifically, MLP layers [75] are utilized to encode past driving action information. Additionally, multi-scale UNet features are pooled as visual cues. The two modality features are then concatenated to learn future driving trajectories (more implementation details are in supplement). The results of open-loop evaluation on the nuScenes dataset are presented in Tab. 3. Remarkably, the average _L_ 2 trajectory error of _DriveDreamer_ is merely 0.29m, surpassing the performance of the multi-modality method VAD [33]. In addition, _DriveDreamer_ relatively decreases the average collision rate reported in [75] by 21%, confirming that the visual features learned by _DriveDreamer_ contribute to end-to-end autonomous driving, thereby enhancing driving safety. 

## **5. Discussion and Conclusion** 

_DriveDreamer_ represents a significant advancement in the field of world modeling, particularly in the context of autonomous driving. By focusing on real-world driving scenarios and harnessing the power of the diffusion model, _DriveDreamer_ has demonstrated its ability to comprehend complex environments, generate high-quality driving videos, and formulate realistic driving policies. While prior research primarily concentrated on gaming or simulated environments, _DriveDreamer_ extends the boundaries of world modeling to encompass the intricacies of actual driving conditions. _DriveDreamer_ paves the way for future research in autonomous driving, emphasizing the importance of real-world representation for more accurate modeling and decision-making in this critical domain. 

## **References** 

- [1] Fan Bao, Shen Nie, Kaiwen Xue, Chongxuan Li, Shi Pu, Yaole Wang, Gang Yue, Yue Cao, Hang Su, and Jun Zhu. One transformer fits all distributions in multi-modal diffusion at scale. _arXiv preprint arXiv:2303.06555_ , 2023. 2 

- [2] Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis. Align your latents: High-resolution video synthesis with latent diffusion models. In _CVPR_ , 2023. 5, 6 

- [3] Holger Caesar, Varun Bankiti, Alex H. Lang, Sourabh Vora, Venice Erin Liong, Qiang Xu, Anush Krishnan, Yu Pan, Giancarlo Baldan, and Oscar Beijbom. nuscenes: A multimodal dataset for autonomous driving. _CVPR_ , 2019. 7, 12 

- [4] Dian Chen and Philipp Kr¨ahenb¨uhl. Learning from all vehicles. In _CVPR_ , 2022. 5 

- [5] Li Chen, Penghao Wu, Kashyap Chitta, Bernhard Jaeger, Andreas Geiger, and Hongyang Li. End-to-end autonomous driving: Challenges and frontiers. _arXiv preprint arXiv:2306.16927_ , 2023. 2, 3 

- [6] Rui Chen, Yongwei Chen, Ningxin Jiao, and Kui Jia. Fantasia3d: Disentangling geometry and appearance for high-quality text-to-3d content creation. _arXiv preprint arXiv:2303.13873_ , 2023. 2 

- [7] Felipe Codevilla, Eder Santana, Antonio M L´opez, and Adrien Gaidon. Exploring the limitations of behavior cloning for autonomous driving. In _CVPR_ , 2019. 2 

- [8] Emily Denton and Rob Fergus. Stochastic video generation with a learned prior. In _ICML_ , 2018. 2, 3 

- [9] Prafulla Dhariwal and Alexander Nichol. Diffusion models beat gans on image synthesis. _NeurIPS_ , 2021. 3 

- [10] Stefan Elfwing, Eiji Uchibe, and Kenji Doya. Sigmoidweighted linear units for neural network function approximation in reinforcement learning. _Neural networks_ , 2018. 12 

- [11] Jean-Yves Franceschi, Edouard Delasalles, Micka¨el Chen, Sylvain Lamprier, and Patrick Gallinari. Stochastic latent residual video prediction. In _ICML_ , 2020. 2, 3 

- [12] Ruiyuan Gao, Kai Chen, Enze Xie, Lanqing Hong, Zhenguo Li, Dit-Yan Yeung, and Qiang Xu. Magicdrive: Street view generation with diverse 3d geometry control. _arXiv preprint arXiv:2310.02601_ , 2023. 3 

- [13] Zeyu Gao, Yao Mu, Ruoyan Shen, Chen Chen, Yangang Ren, Jianyu Chen, Shengbo Eben Li, Ping Luo, and Yanfeng Lu. Enhance sample efficiency and robustness of end-to-end urban autonomous driving via semantic masked world model. _arXiv preprint arXiv:2210.04017_ , 2022. 2, 3 

- [14] Shuyang Gu, Dong Chen, Jianmin Bao, Fang Wen, Bo Zhang, Dongdong Chen, Lu Yuan, and Baining Guo. Vector quantized diffusion model for text-to-image synthesis. In _CVPR_ , 2022. 2 

- [15] David Ha and J¨urgen Schmidhuber. Recurrent world models facilitate policy evolution. _NeurIPS_ , 2018. 2, 3 

- [16] Danijar Hafner, Kuang-Huei Lee, Ian Fischer, and Pieter Abbeel. Deep hierarchical planning from pixels. _NeurIPS_ , 2022. 3 

- [17] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _arXiv preprint arXiv:1912.01603_ , 2019. 2, 3 

- [18] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 2, 3 

- [19] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 2, 3 

9 

- [20] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. 3 

- [21] William Harvey, Saeid Naderiparizi, Vaden Masrani, Christian Weilbach, and Frank Wood. Flexible diffusion modeling of long videos. _NeurIPS_ , 2022. 2, 3 

- [22] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. _NeurIPS_ , 2017. 7 

- [23] Jonathan Ho, William Chan, Chitwan Saharia, Jay Whang, Ruiqi Gao, Alexey Gritsenko, Diederik P Kingma, Ben Poole, Mohammad Norouzi, David J Fleet, et al. Imagen video: High definition video generation with diffusion models. _arXiv preprint arXiv:2210.02303_ , 2022. 2, 3 

- [24] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _NeurIPS_ , 2020. 3 

- [25] Jonathan Ho, Chitwan Saharia, William Chan, David J Fleet, Mohammad Norouzi, and Tim Salimans. Cascaded diffusion models for high fidelity image generation. _JMLR_ , 2022. 3 

- [26] Sepp Hochreiter and J¨urgen Schmidhuber. Long short-term memory. _Neural computation_ , 1997. 3 

- [27] Tobias H¨oppe, Arash Mehrjou, Stefan Bauer, Didrik Nielsen, and Andrea Dittadi. Diffusion models for video prediction and infilling. _arXiv preprint arXiv:2206.07696_ , 2022. 3 

- [28] Jun-Ting Hsieh, Bingbin Liu, De-An Huang, Li F Fei-Fei, and Juan Carlos Niebles. Learning to decompose and disentangle representations for video prediction. _NeurIPS_ , 2018. 3 

- [29] Anthony Hu, Gianluca Corrado, Nicolas Griffiths, Zachary Murez, Corina Gurau, Hudson Yeo, Alex Kendall, Roberto Cipolla, and Jamie Shotton. Model-based imitation learning for urban driving. _NeurIPS_ , 2022. 2, 3, 7 

- [30] Shengchao Hu, Li Chen, Penghao Wu, Hongyang Li, Junchi Yan, and Dacheng Tao. St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning. In _ECCV_ , 2022. 7, 9 

- [31] Yihan Hu, Jiazhi Yang, Li Chen, Keyu Li, Chonghao Sima, Xizhou Zhu, Siqi Chai, Senyao Du, Tianwei Lin, Wenhai Wang, Lewei Lu, Xiaosong Jia, Qiang Liu, Jifeng Dai, Yu Qiao, and Hongyang Li. Planning-oriented autonomous driving. In _CVPR_ , 2023. 5, 9 

- [32] Lianghua Huang, Di Chen, Yu Liu, Yujun Shen, Deli Zhao, and Jingren Zhou. Composer: Creative and controllable image synthesis with composable conditions. _arXiv preprint arXiv:2302.09778_ , 2023. 3 

- [33] Bo Jiang, Shaoyu Chen, Qing Xu, Bencheng Liao, Jiajie Chen, Helong Zhou, Qian Zhang, Wenyu Liu, Chang Huang, and Xinggang Wang. Vad: Vectorized scene representation for efficient autonomous driving. _arXiv preprint arXiv:2303.12077_ , 2023. 9 

- [34] Nal Kalchbrenner, A¨aron Oord, Karen Simonyan, Ivo Danihelka, Oriol Vinyals, Alex Graves, and Koray Kavukcuoglu. Video pixel networks. In _ICML_ , 2017. 3 

- [35] Levon Khachatryan, Andranik Movsisyan, Vahram Tadevosyan, Roberto Henschel, Zhangyang Wang, Shant 

Navasardyan, and Humphrey Shi. Text2video-zero: Text-toimage diffusion models are zero-shot video generators. _arXiv preprint arXiv:2303.13439_ , 2023. 2, 3 

- [36] Seung Wook Kim, Jonah Philion, Antonio Torralba, and Sanja Fidler. Drivegan: Towards a controllable high-quality neural simulation. In _CVPR_ , 2021. 3, 8 

- [37] Seung Wook Kim, Yuhao Zhou, Jonah Philion, Antonio Torralba, and Sanja Fidler. Learning to simulate dynamic environments with gamegan. In _CVPR_ , 2020. 3 

- [38] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ , 2014. 7 

- [39] Diederik P Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 3 

- [40] Manoj Kumar, Mohammad Babaeizadeh, Dumitru Erhan, Chelsea Finn, Sergey Levine, Laurent Dinh, and Durk Kingma. Videoflow: A flow-based generative model for video. _arXiv preprint arXiv:1903.01434_ , 2019. 3 

- [41] Xiaofan Li, Yifu Zhang, and Xiaoqing Ye. Drivingdiffusion: Layout-guided multi-view driving scene video generation with latent diffusion model. _arXiv preprint arXiv:2310.07771_ , 2023. 3 

- [42] Yuheng Li, Haotian Liu, Qingyang Wu, Fangzhou Mu, Jianwei Yang, Jianfeng Gao, Chunyuan Li, and Yong Jae Lee. Gligen: Open-set grounded text-to-image generation. In _CVPR_ , 2023. 2, 4 

- [43] Chen-Hsuan Lin, Jun Gao, Luming Tang, Towaki Takikawa, Xiaohui Zeng, Xun Huang, Karsten Kreis, Sanja Fidler, Ming-Yu Liu, and Tsung-Yi Lin. Magic3d: High-resolution text-to-3d content creation. In _CVPR_ , 2023. 2 

- [44] Jessy Lin, Yuqing Du, Olivia Watkins, Danijar Hafner, Pieter Abbeel, Dan Klein, and Anca Dragan. Learning to model the world with language. _arXiv preprint arXiv:2308.01399_ , 2023. 3 

- [45] Zhijian Liu, Haotian Tang, Alexander Amini, Xinyu Yang, Huizi Mao, Daniela L Rus, and Song Han. Bevfusion: Multitask multi-sensor fusion with unified bird’s-eye view representation. In _ICRA_ , 2023. 7, 8, 13 

- [46] Michael Mathieu, Camille Couprie, and Yann LeCun. Deep multi-scale video prediction beyond mean square error. _arXiv preprint arXiv:1511.05440_ , 2015. 3 

- [47] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 2021. 4, 12 

- [48] Chong Mou, Xintao Wang, Liangbin Xie, Jian Zhang, Zhongang Qi, Ying Shan, and Xiaohu Qie. T2i-adapter: Learning adapters to dig out more controllable ability for text-to-image diffusion models. _arXiv preprint arXiv:2302.08453_ , 2023. 2 

- [49] Alex Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela Mishkin, Bob McGrew, Ilya Sutskever, and Mark Chen. Glide: Towards photorealistic image generation and editing with text-guided diffusion models. _arXiv preprint arXiv:2112.10741_ , 2021. 2, 3 

- [50] Alexander Quinn Nichol and Prafulla Dhariwal. Improved denoising diffusion probabilistic models. In _ICML_ , 2021. 3 

10 

- [51] nuScenes Contributors. The devkit of the nuscenes dataset. https : / / github . com / nutonomy / nuscenes - devkit, 2019. 7 

- [52] Minting Pan, Xiangming Zhu, Yunbo Wang, and Xiaokang Yang. Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. _NeurIPS_ , 2022. 2, 3 

- [53] Ben Poole, Ajay Jain, Jonathan T Barron, and Ben Mildenhall. Dreamfusion: Text-to-3d using 2d diffusion. _arXiv preprint arXiv:2209.14988_ , 2022. 2 

- [54] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _ICML_ . 4 

- [55] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. Hierarchical text-conditional image generation with clip latents. _arXiv preprint arXiv:2204.06125_ , 2022. 2 

- [56] MarcAurelio Ranzato, Arthur Szlam, Joan Bruna, Michael Mathieu, Ronan Collobert, and Sumit Chopra. Video (language) modeling: a baseline for generative models of natural videos. _arXiv preprint arXiv:1412.6604_ , 2014. 3 

- [57] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _CVPR_ , 2022. 2, 3, 4, 5, 7 

- [58] Masaki Saito, Eiichi Matsumoto, and Shunta Saito. Temporal generative adversarial nets with singular value clipping. In _ICCV_ , 2017. 3 

- [59] Younggyo Seo, Danijar Hafner, Hao Liu, Fangchen Liu, Stephen James, Kimin Lee, and Pieter Abbeel. Masked world models for visual control. In _CoRL_ , 2023. 3 

- [60] Uriel Singer, Adam Polyak, Thomas Hayes, Xi Yin, Jie An, Songyang Zhang, Qiyuan Hu, Harry Yang, Oron Ashual, Oran Gafni, et al. Make-a-video: Text-to-video generation without text-video data. _arXiv preprint arXiv:2209.14792_ , 2022. 2, 3 

- [61] Nitish Srivastava, Elman Mansimov, and Ruslan Salakhudinov. Unsupervised learning of video representations using lstms. In _ICML_ , 2015. 3 

- [62] Sergey Tulyakov, Ming-Yu Liu, Xiaodong Yang, and Jan Kautz. Mocogan: Decomposing motion and content for video generation. In _CVPR_ , 2018. 3 

   - [67] Xiang Wang, Hangjie Yuan, Shiwei Zhang, Dayou Chen, Jiuniu Wang, Yingya Zhang, Yujun Shen, Deli Zhao, and Jingren Zhou. Videocomposer: Compositional video synthesis with motion controllability. _arXiv preprint arXiv:2306.02018_ , 2023. 2, 3 

   - [68] Xiaofeng Wang, Zheng Zhu, Yunpeng Zhang, Guan Huang, Yun Ye, Wenbo Xu, Ziwei Chen, and Xingang Wang. Are we ready for vision-centric driving streaming perception? the asap benchmark. In _CVPR_ , 2023. 7 

   - [69] Zhengyi Wang, Cheng Lu, Yikai Wang, Fan Bao, Chongxuan Li, Hang Su, and Jun Zhu. Prolificdreamer: High-fidelity and diverse text-to-3d generation with variational score distillation. _arXiv preprint arXiv:2305.16213_ , 2023. 2 

   - [70] Dirk Weissenborn, Oscar T¨ackstr¨om, and Jakob Uszkoreit. Scaling autoregressive video models. _arXiv preprint arXiv:1906.02634_ , 2019. 3 

   - [71] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _CoRL_ , 2023. 3 

   - [72] Kairui Yang, Enhui Ma, Jibin Peng, Qing Guo, Di Lin, and Kaicheng Yu. Bevcontrol: Accurately controlling streetview elements with multi-perspective consistency via bev sketch layout. _arXiv preprint arXiv:2308.01661_ , 2023. 3 

   - [73] Ling Yang, Zhilong Zhang, Yang Song, Shenda Hong, Runsheng Xu, Yue Zhao, Yingxia Shao, Wentao Zhang, Bin Cui, and Ming-Hsuan Yang. Diffusion models: A comprehensive survey of methods and applications. _arXiv preprint arXiv:2209.00796_ , 2022. 2 

   - [74] Ruihan Yang, Prakhar Srivastava, and Stephan Mandt. Diffusion probabilistic modeling for video generation. _arXiv preprint arXiv:2203.09481_ , 2022. 2, 3 

   - [75] Jiang-Tian Zhai, Ze Feng, Jihao Du, Yongqiang Mao, JiangJiang Liu, Zichang Tan, Yifu Zhang, Xiaoqing Ye, and Jingdong Wang. Rethinking the open-loop evaluation of endto-end autonomous driving in nuscenes. _arXiv preprint arXiv:2305.10430_ , 2023. 9, 12 

   - [76] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models, 2023. 2 

   - [77] Yunpeng Zhang, Zheng Zhu, Wenzhao Zheng, Junjie Huang, Guan Huang, Jie Zhou, and Jiwen Lu. Beverse: Unified perception and prediction in birds-eye-view for vision-centric autonomous driving. _arXiv preprint arXiv:2205.09743_ , 2022. 5 

- [63] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arXiv preprint arXiv:1812.01717_ , 2018. 7 

- [64] Vikram Voleti, Alexia Jolicoeur-Martineau, and Chris Pal. Mcvd-masked conditional video diffusion for prediction, generation, and interpolation. _NeurIPS_ , 2022. 3 

- [65] Carl Vondrick, Hamed Pirsiavash, and Antonio Torralba. Generating videos with scene dynamics. _NeurIPS_ , 29, 2016. 3 

- [66] Tai Wang, Xinge Zhu, Jiangmiao Pang, and Dahua Lin. Fcos3d: Fully convolutional one-stage monocular 3d object detection. In _CVPR_ , 2021. 7, 8, 13 

11 

In the supplement materials, we first elaborate on the implementation details of _DriveDreamer_ , including model architecture and synthetic data training details. Then, we present additional visualization results. 

## **6. Implementation Details** 

**Condition encoders.** In _DriveDreamer_ , diverse encoders are employed to embed different condition inputs, including the reference image, HDMap, 3D box, and action. The detailed architectures of these encoders are listed in Table 4. For spatially aligned conditions, such as the reference image _I ∈R_<sup>_H×W ×_3</sup> and HDMap _H ∈R_<sup>_H×W ×_3</sup> , a stack of 2D convolution layers is utilized to perform downsampling, ensuring the final output dimensions align with those of the diffusion noise. For unstructured conditions like the 3D box _B ∈R_<sup>_N×NB×_16</sup> and action _A ∈R_<sup>_N×_2</sup> , Multilayer Perceptron (MLP) layers are employed for encoding features. 

|Conditions|Layer Description|Output Size|
|---|---|---|
|Ref. Img. (Step A)|Conv2D,4_×_4, S4|_H/_4_× W/_4_×_4|
|Ref. Img. (Step B)|Conv2D,4_×_4, S4|_H/_16_× W/_16_×_4|
|Ref. Img. (StepC)|Conv2D,4_×_4,S4|_H/_64_× W/_64_×_8|
|HDMap (Step A)|Conv2D,4_×_4, S4|_H/_4_× W/_4_×_4|
|HDMap (Step B)|Conv2D,4_×_4, S4|_H/_16_× W/_16_×_4|
|HDMap (StepC)|Conv2D,4_×_4,S4|_H/_64_× W/_64_×_8|
|3D Box (Step A)|FourierEmbedder [47]|_N × NB ×_256|
|3D Box (Step B)|MLP|_N × NB ×_512|
|3D Box(StepC)|MLP|_N × NB ×_768|
|Action (Step A)|MLP|_N ×_32|
|Action (Step B)|MLP|_N ×_128|


Table 4. Encoder architecture details, where S denotes stride, and each convolution layer and MLP layer are followed by _Sigmoid Linear Units_ [10]. 

**Multi-view generation.** The framework of _DriveDreamer_ can be easily extended to multi-view image/video generation. The model architecture comparison between video generation, multi-view image generation and multi-view video generation are shown in Fig. 7. For multi-view image generation, the model framework is the same as that of video generation, except that the frame-vise attention layers are replaced with view-wise attention layers. Besides, the view-wise attention layers construct associations solely between adjacent views. For multi-view video generation, view-wise attention layers and frame-wise attention layers are stacked to process diffusion latent features, which results in view-consistent and frame-consistent videos (see Fig. 8). 

**Action prediction architecture.** For action prediction, the multi-modal features are first concatenated: 

CONCAT( _F_ p( _U_ 0) _, F_ p( _U_ 1) _, F_ p( _U_ 2) _, F_ p( _U_ 3) _, Af_ ) _,_ (11) 


Figure 7. Model architecture comparison between video generation, multi-view image generation and multi-view video generation. 

= where _F_ p is the average pooling operation, _Ui_ ( _i_ 0 _,_ 1 _,_ 2 _,_ 3) are multi-scale UNet features, and _Af_ is the encoded driving action (i.e., velocity and yaw angle) features. Then we use MLP layers [75] to learn future driving actions. For trajectory prediction evaluation, following [75], _Af_ is additionally extracted from high-level command, accelerate and past trajectories, and we use the same action feature encoder of [75]. 

**Synthetic data training.** We leverage data generated by _DriveDreamer_ to augment the training of 3D detection tasks. Specifically, _DriveDreamer_ is fine-tuned with higher-resolution images, where the training data is from nuScenes [3]. Consequently, _DriveDreamer_ can generate high-fidelity images with a resolution of 768 _×_ 448. Then the generated images are resized to the original resolution of 1600 _×_ 900, which can be utilized to train various offthe-shelf 3D detectors. During the training process, we randomly select 4000 samples (3D boxes and HDMap) from the nuScenes training set, which are employed to generate multi-view images. These synthetic data are mixed with the original training set to train 3D detectors. In the ex- 

12 


Figure 8. Visualizations of the generated multi-view video. Regions highlighted by red circles indicate that the generated videos are viewconsistent and frame-consistent. 

periment, we train each baseline (i.e., FCOS3D [66] and BEVFusion [45]) for 12 epochs. The results presented in Tab. 1 demonstrate that our approach significantly improves the performance of downstream tasks. 

## **7. Visualizations** 

As shown in Fig. 9, _DriveDreamer_ exhibits significant proficiency in producing a diverse range of driving scene videos that adhere meticulously to structured traffic conditions, comprising elements such as HDMaps and 3D boxes. Significantly, we can also manipulate the text prompt to induce variations in the generated videos, encompassing changes in weather and time of day. This heightened adaptability contributes substantially to the multifaceted nature of the generated video outputs. In addition to the utilization of structured traffic conditions for generating driving videos, 

_DriveDreamer_ exhibits the capability to diversify the generated driving videos by adapting to different driving actions. As depicted in Fig. 10, starting from an initial frame paired with its corresponding structural information, _DriveDreamer_ can generate distinct videos based on various driving actions, such as videos depicting left and right turns. Apart from its capacity for generating highly controllable driving videos, _DriveDreamer_ demonstrates the ability to predict reasonable driving actions. As depicted in Fig. 11, provided with an initial frame condition and past driving actions, _DriveDreamer_ can generate future driving actions that align with real-world scenarios. Comparative analysis of the generated actions against corresponding ground truth videos reveals that _DriveDreamer_ consistently predicts sensible driving actions, even in complex situations such as intersections, obeying traffic lights, and executing turns. 

13 


Figure 9. Driving video generation with structured traffic conditions (HDMaps and 3D boxes), where text prompts are utilized to adjust driving scenario style ( _e.g_ ., weather and time of the day). 

14 


Figure 10. Future driving video generation with driving actions interaction, where different driving actions ( _e.g_ . turn left, turn right) can produce corresponding driving videos. 


Figure 11. Visualization of the predicted future driving actions, along with the corresponding ground truth driving video. 

15 

