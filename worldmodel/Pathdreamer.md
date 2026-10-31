---
title: "Pathdreamer: A World Model for Indoor Navigation"
date: "2021-05-18"
authors: "Jing Yu Koh; Honglak Lee; Yinfei Yang; Jason Baldridge; Peter Anderson"
url: https://arxiv.org/abs/2105.08756
pdf: https://arxiv.org/pdf/2105.08756
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2105.08756)** / [論文ページ](https://arxiv.org/abs/2105.08756)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Pathdreamer: A World Model for Indoor Navigation** 

Jing Yu Koh<sup>1</sup> 

Honglak Lee<sup>2</sup> 

Yinfei Yang<sup>1</sup> Jason Baldridge<sup>1</sup> Peter Anderson<sup>1</sup> 

1Google Research 

2University of Michigan 

# **Abstract** 

_People navigating in unfamiliar buildings take advantage of myriad visual, spatial and semantic cues to efficiently achieve their navigation goals. Towards equipping computational agents with similar capabilities, we introduce Pathdreamer, a visual world model for agents navigating in novel indoor environments. Given one or more previous visual observations, Pathdreamer generates plausible high-resolution_ 360<sup>_◦_</sup> _visual observations (RGB, semantic segmentation and depth) for viewpoints that have not been visited, in buildings not seen during training. In regions of high uncertainty (e.g. predicting around corners, imagining the contents of an unseen room), Pathdreamer can predict diverse scenes, allowing an agent to sample multiple realistic outcomes for a given trajectory. We demonstrate that Pathdreamer encodes useful and accessible visual, spatial and semantic knowledge about human environments by using it in the downstream task of Vision-and-Language Navigation (VLN). Specifically, we show that planning ahead with Pathdreamer brings about half the benefit of looking ahead at actual observations from unobserved parts of the environment. We hope that Pathdreamer will help unlock model-based approaches to challenging embodied navigation tasks such as navigating to specified objects and VLN._ 

# **1. Introduction** 

World models [23], or models of environments [72], are an appealing way to represent an agent’s knowledge about its surroundings. An agent with a world model can predict its future by ‘imagining’ the consequences of a series of proposed actions. This capability can be used for samplingbased planning [16, 57], learning policies directly from the model (i.e., learning in a dream) [17, 23, 64, 25], and for counterfactual reasoning [6]. Model-based approaches such as these also typically improve the sample efficiency of deep reinforcement learning [72, 62]. However, world models that generate high-dimensional visual observations (i.e., images) have typically been restricted to relatively simple environments, such as Atari games [62] and tabletops [16]. 

Our goal is to develop a generic visual world model for agents navigating in indoor environments. Specifically, 


Figure 1: Generating photorealistic 360<sup>_◦_</sup> visual observations from an imagined 6.3m trajectory in a previously unseen building. Observations also include depth and segmentations (not shown here). 

given one or more previous observations and a proposed navigation action sequence, we aim to generate plausible high-resolution visual observations for viewpoints that have not been visited, and do so in buildings not seen during training. Beyond applications in video editing and content creation, solving this problem would unlock model-based methods for many embodied AI tasks, including navigating to objects [5], instruction-guided navigation [3, 66, 40] and dialog-guided navigation [74, 26]. For example, an agent asked to find a certain type of object in a novel building, e.g. ‘ _find a chair_ ’, could perform mental simulations using the world model to identify navigation trajectories that are most likely to include chair observations – without moving. 

Building such a model is challenging. It requires synthesizing completions of partially visible objects, using as few as one previous observation. This is akin to novel view synthesis from a single image [19, 80], but with potentially unbounded viewpoint changes. There is also the related but considerably more extreme challenge of predicting around corners. For example, as shown in Fig. 1, any future navigation trajectory passing the entrance of an unseen room requires the model to plausibly imagine the entire contents 

1 

of that room (we dub this the _room reveal_ problem). This requires generalizing from the visual, spatial and semantic structure of previously explored environments—which in our case are photo-realistic 3D captures of real indoor spaces in the Matterport3D dataset [7]. A third problem is temporal consistency: predictions of unseen building regions should ideally be stochastic (capturing the full distribution of possible outcomes), but revisited regions should be rendered in a consistent manner to previous observations. 

Towards this goal, we introduce Pathdreamer. Given one or more visual observations (consisting of RGB, depth and semantic segmentation for panoramas) of an indoor scene, Pathdreamer synthesizes high-resolution visual observations (RGB, depth and semantic segmentations) along a specified trajectory through future viewpoints, using a hierarchical two-stage approach. Pathdreamer’s first stage, Structure Generator, generates depth and semantic segmentations. Inspired by video prediction [11], these outputs are conditioned on a latent noise tensor capturing the stochastic information about the next observation (such as the layout of an unseen room) that cannot be predicted deterministically. The second stage’s Image Generator renders the depth and semantic segmentations as realistic RGB images using modified Multi-SPADE blocks [63, 51]. To maintain long-term consistency in the generated observations, both stages use back-projected 3D point cloud representations which are re-projected into image space for context [51]. 

Pathdreamer can generate plausible views for unseen indoor scenes under large viewpoint changes (see Figure 1), while also addressing the _room reveal_ problem – in this case correctly hypothesizing that the unseen room revealed at position 2 will most likely resemble a kitchen. Empirically, using the Matterport3D dataset [7] and 360<sup>_◦_</sup> observations, we evaluate both stages of our model against prior work and reasonable baselines and ablations. We find that the hierarchical structure of the model is essential for predicting over large viewpoint changes, that maintaining both RGB and semantic context is required, and that prediction quality degrades gradually when we evaluate with trajectory rollouts of up to 13m (with viewpoints 2.25m apart on average). 

Encouraged by these results, we investigate whether Pathdreamer’s RGB predictions can improve performance on a downstream task: Vision-and-Language Navigation (VLN), using the R2R dataset [3]. VLN requires agents to interpret and execute natural language navigation instructions in a photorealistic 3D environment. A robust finding from previous research is that performance improves dramatically when agents can look ahead at unobserved parts of the environment while following an instruction [50]. We show that replacing look-ahead observations with Pathdreamer predictions maintains around half of the gains, a finding we expect to have significant implications for VLN research. In summary, our main contributions include: 

- Proposing the study of visual world models for generic indoor environments and defining evaluation protocols and baselines for future work. 

- Pathdreamer, a stochastic hierarchical visual world model combining multiple, independent threads of previous work on video prediction [11], semantic image synthesis [63] and video-to-video synthesis [51]. 

- Extensive experiments characterizing the performance of Pathdreamer and demonstrating improved results on the downstream VLN task [3]. 

# **2. Related Work** 

**Video Prediction** Our work is closely related to the task of video prediction, which aims to predict the future frames of a video sequence. While some video prediction methods predict RGB video frames directly [76, 1, 41, 44], many others use hierarchical models to first predict an intermediate representation (such as semantic segmentation) [47, 35, 77, 82, 42], which improves the fidelity of long-term predictions [42]. Several approaches have also incorporated 3D point cloud representations, using projective camera geometry to explicitly infer aspects of the next frame [75, 51, 43]. Inspired by this work, we adopt and combine both the hierarchical two-stage approach and 3D point cloud representations. Further, since our interest is in action-conditional world models, we provide a trajectory of future viewpoints to the model rather than assuming a constant frame rate and modeling camera motion implicitly, which is more typical in video generation [44, 42]. 

**Action-Conditional Video Prediction** Conditional video prediction to improve agent reasoning and planning has been explored in several tasks. This includes video prediction for Atari games conditioned on control inputs [60, 10, 62, 25] and 3D game environments like Doom [23]. In robotics, action-conditional video prediction has been investigated for object pushing in tabletop settings to improve generalization to novel objects [15, 16, 14]. This work has been restricted to simple environments and low-resolution images, such as 64 _×_ 64 images of objects in a wooden box. To the best of our knowledge, we are the first to investigate action-conditional video prediction in building-scale environments with high-resolution (1024 _×_ 512) images. 

**World Models and Navigation Priors** World models [23] are an appealing way to summarize and distill knowledge about complex, high-dimensional environments. However, world models can differ in their outputs. While Pathdreamer predicts visual observations, there is also a vast literature on world models that predict compact latent representations of future states [38, 24, 25] or other taskspecific measurements [13] or rewards [61]. This includes recent work attempting to learn statistical regularities and other priors for indoor navigation—for example, by min- 

2 

ing spatial co-occurrences from real estate video tours [8], learning to predict top-down belief maps over room characteristics [58], or learning to reconstruct house floor plans using audio and visual cues from a short video sequence [65]. In contrast to these approaches, we focus on explicitly predicting visual observations (i.e., pixels) which are generic, human-interpretable, and apply to a wide variety of downstream tasks and applications. Further, recent work identifies a close correlation between image prediction accuracy and downstream task performance in model-based RL [4]. 

**Embodied Navigation Agents** High-quality 3D environment datasets such as Matterport3D [7], StreetLearn [56, 53], Gibson [81] and Replica [71] have triggered intense interest in developing embodied agents that act in realistic human environments [2]. Tasks of interest include ObjectNav [5] (navigating to an instance of a particular kind of object), and Vision-and-Language Navigation (VLN) [3], in which agents must navigate according to natural language instructions. Variations of VLN include indoor navigation [3, 33, 66, 40], street-level navigation [9, 53], visionand-dialog navigation [59, 74, 26], VLN in continuous environments [39], and more. Notwithstanding considerable exploration of pretraining strategies [46, 27, 50, 87], data augmentation approaches [20, 21, 73], agent architectures and loss functions [86, 48, 49], existing work in this space considers only model-free approaches. Our aim is to unlock model-based approaches to these tasks, using a visual world model to encode prior commonsense knowledge about human environments and thereby relieve the burden on the agent to learn these regularities. Underscoring the potential of this direction, we note that using the ground-truth environment for planning with beam search typically improves VLN success rates on the R2R dataset by 17-19% [20, 73]. 

**Novel View Synthesis** We position our work with respect to novel view synthesis [19, 37, 29, 18, 70, 85, 54]. Methods for representing 3D scenes include point cloud representations [80], layered depth images [12], and mesh representations [68]. Recently, neural radiance fields (NeRF) [55, 52, 83] achieved impressive results by capturing volume density and color implicitly with a neural network. NeRF models synthesize very high quality 3D scenes, but a significant drawback for our purposes is that they require a large number of input views to render a single scene (e.g., 20–62 images per scene in [55]). More importantly, these models are typically trained to represent a single scene, and do not yet generalize well to unseen environments. In contrast, our problem demands generalization to unseen environments, using as little as one previous observation. 

# **3. Pathdreamer** 

Pathdreamer is a world model that generates highresolution visual observations from a trajectory of future 

viewpoints in buildings it has never observed. The input to Pathdreamer is a sequence of previous observations consisting of RGB images _I_ 1: _t−_ 1, semantic segmentation images _s_ 1: _t−_ 1, and depth images _d_ 1: _t−_ 1 (where the depth and segmentations could be ground-truth or estimates from a model). We assume that a corresponding sequence of camera poses _T_ 1: _t−_ 1 is available from an odometry system, and that the camera intrinsics are known or estimated. Our goal is to generate realistic RGB, semantic segmentation and depth images for a trajectory of future poses _Tt, Tt_ +1 _, . . . , TT_ , which may be provided up front or iteratively by some agent interacting with the returned observations. Note that we generate depth and segmentation because these modalities are useful in many downstream tasks. We assume that the future trajectory may traverse unseen areas of the environment, requiring the model to not only in-fill minor object dis-occlusions, but also to imagine entire room reveals (Figure 1). 

Figure 2 shows our proposed hierarchical two-stage model for addressing this challenge. It uses a latent noise tensor _zt_ to capture the stochastic information about the next observation (e.g. the layout of an unseen room) that cannot be predicted deterministically. Given a sampled noise tensor _zt_ , the first stage (Structure Generator) generates a new depth image _d_<sup>ˆ</sup> _t_ and segmentation image _s_ ˆ _t_ to provide a plausible high-level semantic representation of the scene, using as context the previous semantic and depth images _s_ 1: _t−_ 1, _d_ 1: _t−_ 1. In the second stage (Image Generator), the predicted semantic and depth images _s_ ˆ _t_ , _d_<sup>ˆ</sup> _t_ are rendered into a realistic RGB image _I_<sup>ˆ</sup> _t_ using previous RGB images _I_ 1: _t−_ 1 as context. In each stage, context is provided by accumulating previous observations as a 3D point cloud which is re-projected into 2D using _Tt_ . 

## **3.1. Structure Generator: Segmentation & Depth** 

Pathdreamer’s first stage is the Structure Generator, a stochastic encoder-decoder network for generating diverse, plausible segmentation and depth images. Like [51], to provide the previous observation context, we first back-project the previous segmentations _s_ 1: _t−_ 1 into a unified 3D semantic point cloud using the depth images _d_ 1: _t−_ 1 and camera poses _T_ 1: _t−_ 1. We then re-project this point cloud back into pixel space usingguidance images _s T′tt_<sup>,</sup> to create sparse segmentation and depth<sup>_d_</sup> _′t_<sup>which reflect the current pose.</sup> mantic guidance imagethe depth guidance imageThe input to the encoder is a one-hot encoding of the se- _s′t d_<sup>_∈_</sup> _′t_<sup>_∈_R</sup><sup>_W_R</sup><sup>_×WH ××HC×_, concatenated with1.The architecture</sup> of the encoder-decoder model is based on RedNet [34] – a ResNet-50 [28] architecture designed for indoor RGB-D semantic segmentation. RedNet uses transposed convolutions for upsampling in the decoder and skip connections between the encoder and decoder to preserve spatial information. Since the input contains a segmentation image, and segmentation classes differ across datasets, the encoder- 

3 


Figure 2: Pathdreamer model architecture at step _t_ . Given a history of visual observations (RGB, depth and semantics) and a trajectory of future viewpoints, the Structure Generator conditions on a sampled noise tensor before generating semantic and depth outputs to provide a high-level structural representation of the scene. Realistic RGB images are synthesized by the Image Generator in the second stage. 

decoder is not pretrained. We introduce the latent spatial noise tensor _zt ∈_ R<sup>_H′×W ′×_32</sup> into the model by concatenating it with the feature map between the encoder and the decoder. The final output of the encoder-decoder model is a segmentation image ˆ _st_ and a depth image _d_<sup>ˆ</sup> _t_ , with segmentation predictions generated by a _C_ -way softmax and depth outputs normalized in the range (0 _,_ 1) and generated via a sigmoid function. At each step during inference, the segmentation prediction _s_ ˆ _t_ is back-projected and added to the point cloud to assist prediction in future timesteps. 

To generate the noise tensor _zt_ , we take inspiration from SVG _pψ_ ( _zt|_ [ _s_ 11 _′t_<sup>_, d_</sup> ] _′t_ and<sup>).Intuitively,</sup> learn a conditional<sup>thereare</sup> prior<sup>many</sup> noise<sup>possible</sup> distribution<sup>scenes</sup> that may be generated for an unseen building region. We would like _zt_ to carry the stochastic information about the next observation that the deterministic encoder cannot capture, and we would like for the decoder to make good use of that information. During training, we encourage the first outcomedistributionby _p_ using _ψ_ ( _zt|s_ a _′t_<sup>_, d_</sup> KL-divergence _′t_<sup>)tobeclose</sup> loss<sup>tothe</sup> to force<sup>posterior</sup> the prior<sup>dis-</sup> tribution _φ_ ( _zt|st, dt_ ) which is conditioned on the groundtruth segmentation and depth images. We encourage the second outcome by providing the decoder with sampled _zt_ values from the posterior distribution _qφ_ (conditioned on the ground-truth outputs) during training. During inference, the latent noise _zt_ is sampled from the prior distribution _pψ_ and the posterior distribution _qφ_ is not used. Both distributions are modeled using 3-layer CNNs that take their input from the encoder and output two channels representing _µ_ and _σ_ to parameterize a multivariate Gaussian distribution _N_ ( _µ, σ_ ). As shown in Figure 3, the noise is useful in encoding diverse, plausible representations of unseen regions. 

Overall, the Structure Generator is trained to minimize a joint loss consisting of a cross-entropy loss _L_ ce for semantic predictions, a mean absolute error term for depth predic- 

tions, and the KL-divergence term for the noise tensor: 


where _λ_ ce, _λ_ d, and _λ_ KL are weights determined by a grid search. We set these to 1, 100, and 0.5 respectively. 

## **3.2. Image Generator: RGB** 

The Image Generator is an image-to-image translation GAN [22, 78] that converts the semantic and depth predictions ˆ _st_ , _d_<sup>ˆ</sup> _t_ from the first stage into a realistic RGB image _I_<sup>ˆ</sup> _t_ . Our model architecture is based on SPADE blocks [63] that use spatially-adaptive normalization layers to insert context into multiple layers of the network. As with our Structure Generator, we maintain an accumulating 3D point cloud containing all previous image observations. This provides a sparse RGB guidance image _It_<sup>_′_when re-projected.Similar</sup> to Multi-SPADE [51], we insert two SPADE normalization layers into each residual block: one conditioned on the concatenated semantic and depth inputs [ˆ _st, d_<sup>ˆ</sup> _t_ ], and one conditioned on the RGB guidance image _It_<sup>_′_.The sparsity of the</sup> RGB guidance image is handled by applying partial convolutions [45]. In total Image Generator consists of 7 MultiSPADE blocks, preceded by a single convolution block. 

Following SPADE [63], the model is trained with the GAN hinge loss, feature matching loss [78], and perceptual loss [36] from a pretrained VGG-19 [69] model. During training, the generator is provided with the ground-truth segmentation image _st_ and ground-truth depth image _dt_ . Our discriminator architecture is based on PatchGAN [32], and takes as input the concatenation of the ground-truth image _It_ or generated image _I_<sup>ˆ</sup> _t_ , the ground-truth depth image _dt_ and the ground-truth semantic image _st_ . The losses for 

4 


Figure 3: When predicting around corners, the Structure Generator can sample diverse and semantically plausible scene layouts which are closely reflected in the RGB output of the Image Generator, shown here for two guidance image inputs (left columns; unseen areas are indicated by solid black regions). Each example shows three alternative _room reveals_ and the groundtruth. In the bottom example, the model considers various completions for a bedroom but fails to anticipate the groundtruth’s matching lamp on the opposite side of the bed. 

the generator _G_ and the discriminator _D_ are: 


where _xt_ = ( _st, dt, It_<sup>_′_) denotes the complete set of inputs to</sup> the generator, _φ_<sup>(</sup><sup>_i_)</sup> denotes the output of the _i_<sup>th</sup> layer of the pretrained VGG-19 model, _D_<sup>(</sup><sup>_i_)</sup> denotes the output of the discriminator’s _i_ -th layer (conditioning inputs _st, dt_ to the discriminator have been dropped to save space). Like the Structure Generator, the Image Generator is not pretrained. 

## **3.3. Training and Inference** 

**Dataset** For training and evaluation we use Matterport3D [7], a dataset of 10.8k RGB-D images from 90 building-scale indoor environments. For each environment, Matterport3D also includes a textured 3D mesh which is annotated with 40 semantic classes of objects and building components. To align with downstream VLN tasks, in all experiments the RGB, depth and semantic images are 360<sup>_◦_</sup> panoramas in equirectangular format. 

**Trajectories** To train Pathdreamer, we sampled 400k trajectories from the Matterport3D training environments. To define feasible trajectories, we used the navigation graphs from the Room-to-Room (R2R) dataset [3], in which nodes correspond to panoramic image locations, and edges define 

navigable state transitions. For each trajectory 5–8 panoramas were sampled, choosing the starting node and the edge transitions uniformly at random. On average the viewpoints in these trajectories are 2m apart. Training with relatively large viewpoint changes is desirable, since the model learns to synthesize observations with large viewpoint changes in a single step (without the need to incur the computational cost of generating intervening frames). However, this does not preclude Pathdreamer from generating smooth video outputs at high frame rates<sup>1</sup> . 

**Training** The first and second stages of the model are trained separately. For the Image Generator, we use the Matterport3D RGB panoramas as training targets at 1024 _×_ 512 resolution. We use the Habitat simulator [67] to render ground-truth depth and semantic training inputs and stitch these into equirectangular panoramas. We perform data augmentation by randomly cropping and horizontally rolling the RGB panoramas, which we found essential due to the limited number of panoramas available. 

To train the Structure Generator, we again used Habitat to render depth and semantic images. Since this stage does not require aligned RGB images for training, in this case we performed data augmentation by perturbing the viewpoint coordinates with a random Gaussian noise vector drawn from _N_ (0 _,_ 0 _._ 2m) independently along each 3D axis. The Structure Generator was trained with equirectangular panoramas at 512 _×_ 256 resolution. 

**Inference** To avoid heading discontinuities during inference, we use circular padding on the image x-axis for both the Structure Generator and the Image Generator. 

> 1See https://youtu.be/StklIENGqs0 for our video generation results. 

5 


Figure 4: Example full prediction sequence beginning with one observation (depth, semantics, RGB) as context and generating observations for 3 new viewpoints traversing a corridor. At 2.3m the model completes a room reveal, imagining a kitchen-like space. After 8.6m the model’s predictions degrade. More examples are provided in the supplementary. 

The 512 _×_ 256 resolution semantic and depth outputs of the Structure Generator are upsampled to 1024 _×_ 512 using nearest neighbor interpolation before they are passed to the Image Generator. In quantitative experiments, we set the Structure Generator noise tensor _zt_ to the mean of the prior. 

# **4. Experiments** 

For evaluation we use the paths from the Val-Seen and Val-Unseen splits of the R2R dataset [3]. Val-Seen contains 340 trajectories from environments in the Matterport3D training split. Val-Unseen contains 783 trajectories in Matterport3D environments not seen in training. Since R2R trajectories contain 5-7 panoramas and at least 1 previous observation is given as context, we report evaluations over 1–6 steps, representing predictions over trajectory rollouts of around 2–13m (panoramas are 2.25m apart on average). See Figure 4 for an example rollout over 8.6m. We characterize the performance of Pathdreamer in comparison to baselines, ablations and in the context of the downstream task of Vision-and-Language Navigation (VLN). 

## **4.1. Pathdreamer Results** 

**Semantic Generation** A key feature of our approach is the ability to generate semantic segmentation and depth outputs, in addition to RGB. We evaluate the generated semantic segmentation images using mean Intersection-OverUnion (mIOU) and report results for: 

- **Nearest Neighbor** : A baseline without any learned components, using nearest-neighbor interpolation to fill holes in the projected semantic guidance image _s_<sup>_′_</sup> _t_<sup>.</sup> 

   - _t_<sup>.</sup> 

- **Ours (Teacher Forcing)** : Structure Generator trained using the ground truth semantic and depth images as the previous observation at every time step. 

- **Ours (Recurrent)** : Structure Generator trained while feeding back its own semantic and depth predictions as 

previous observations for the next step prediction. This reduces train-test mismatch and may allow the model to compensate for errors when doing longer roll-outs. We also tried training the hierarchical convolutional LSTM from [42], but found that it frequently collapsed to a single class prediction. We attribute this to the large viewpoint changes and heavy occlusion in the training sequences; we believe this can be more effectively modeled with point cloud geometry than with a geometry-unaware LSTM. 

As illustrated in Table 1, Pathdreamer performs far better than the Nearest Neighbor baseline regardless of the number of steps in the rollout or the number of previous observations used as context. As expected, performance in seen environments is higher than unseen. Perhaps surprisingly, in Figure 5a we show that Recurrent training improves results during longer rollouts in the training environments (ValSeen), but this does not improve results on Val-Unseen, perhaps indicating that the error compensation learned by the Image Generator does not easily generalize. 

In addition to accurate predictions, we also want generated results to be _diverse_ . Figure 3 shows that our model can generate diverse semantic scenes by interpolating the noise tensor _zt_ , and that the RGB outputs closely reflect the generated semantic image. This allows us to generate multiple plausible alternatives for the same navigation trajectory. 

**RGB Generation** To evaluate the quality of RGB panoramas generated by the Image Generator, we compute the Fr´echet Inception Distance (FID) [30] between generated and real images for each step in the paths. We report results using the semantic images generated by the Structure Generator as inputs (i.e., our full model). To quantify the potential for uplift with better Structure Generators, we also report results using ground truth semantic segmentations as input. We compare to two ablated versions of our model: 

6 


(a) Semantic segmentation mean-IOU ( _↑_ ). **[TF]:** Teacher Forcing. **[Rec]:** Recurrent. 

(b) RGB generation FID ( _↓_ ). **[GT]** : Ground truth semantic inputs. **[SG]** : Structure Generator predictions. 

Figure 5: Pathdreamer semantic segmentation mean-IOU (above) and RGB generation FID (below). Results are shown for Val-Seen (left) and Val-Unseen (right). Confidence intervals indicate the range of outcomes with 1, 2 or 3 previous observations as context. 

|||**Val**|**-Seen**|**Val-**|**Unseen**|
|---|---|---|---|---|---|
|**Model**|**Context**|1 Step|1–6 Steps|1 Step|1–6 Steps|
|Nearest Neighbor|1|59.5|32.0|59.1|30.6|
|Ours (Teacher Forcing)|1|**84.9**|59.2|**78.3**|50.8|
|Ours (Recurrent)|1|84.7|**65.9**|77.5|**50.9**|
|Nearest Neighbor|2|57.4|35.2|56.5|33.8|
|Ours (Teacher Forcing)|2|**85.4**|64.6|**77.4**|55.5|
|Ours (Recurrent)|2|85.1|**70.2**|76.6|**55.7**|
|Nearest Neighbor|3|57.4|38.7|56.1|37.7|
|Ours (Teacher Forcing)|3|**85.1**|68.5|**77.3**|60.4|
|Ours (Recurrent)|3|84.6|**72.7**|76.8|**60.8**|


Table 1: Mean-IOU ( _↑_ ) for generated semantic segmentations with varying context and prediction steps. 

- **No Semantics** : The semantic and depth inputs _st_ , _dt_ are removed from the Multi-SPADE blocks. 

- **SPADE** : An ablation of the RGB inputs to the model, comprising the previous RGB image _It−_ 1 and the reprojected RGB guidance image _It_<sup>_′_.Thesemanticim-</sup> age _st_ replaces _It−_ 1 as input to the model and the _It_<sup>_′_in-</sup> put layers are removed from the Multi-SPADE blocks, making this effectively the SPADE model [63]. 

As shown in Table 2, SPADE performs the best in ValSeen, indicating that the model has the capacity to mem- 

|||**I**|**npu**|**ts**|**Val**|**-Seen**|**Val-**|**Unseen**|
|---|---|---|---|---|---|---|---|---|
|**Model**|**Contex**|**t**Obs|Sem|RGB|1 Step|1–6 Steps|1 Step|1–6 Steps|
|No Semantics|1|-||✓|34.1|81.7|35.2|90.8|
|SPADE|1|GT|✓||**23.3**|**24.9**|47.3|50.3|
|Ours|1|GT|✓|✓|24.1|31.3|**32.4**|**39.9**|
|Ours|1|SG|✓|✓|26.2|41.7|34.8|70.4|
|No Semantics|2|-||✓|34.0|69.0|39.5|78.6|
|SPADE|2|GT|✓||**22.8**|**25.3**|52.3|51.2|
|Ours|2|GT|✓|✓|23.5|31.2|**35.3**|**39.9**|
|Ours|2|SG|✓|✓|25.8|38.4|38.2|61.0|
|No Semantics|3|-||✓|35.6|60.4|41.9|67.5|
|SPADE|3|GT|✓||**23.1**|**26.2**|52.8|50.7|
|Ours|3|GT|✓|✓|23.2|31.7|**35.5**|**39.2**|
|Ours|3|SG|✓|✓|25.6|36.7|38.5|52.9|


Table 2: FID scores ( _↓_ ) for generated RGB images with varying context and prediction steps, using either ground truth semantics (GT) or Structure Generator predictions (SG) as input. 

orize the training environments. In this case, RGB inputs are not necessary. However, our model performs noticeably better in Val-Unseen, highlighting the importance of maintaining RGB context in unseen environments (which is our focus). Performance degrades significantly in the No Semantics setting in both Val-Seen and Val-Unseen. We observed that without semantic inputs, the model is unable to generate meaningful images over longer horizons, which validates our two-stage hierarchical approach. These results are reflected in the FID scores, as well as qualitatively (Figure 6); Image Generator’s outputs are significantly crisper, especially over longer horizons. Due to the benefit of guidance images, the Image Generator’s textures are also generally better matched with the unseen environment, while SPADE tends to wash out textures, usually creating images of a standard style. Figure 5b plots performance for every setting step-by-step. FID of the Image Generator improves substantially when using ground truth semantics, particularly for longer rollouts, highlighting the potential to benefit from improvements to the Structure Generator. 

## **4.2. VLN Results** 

Finally, we evaluate whether predictions from Pathdreamer can improve performance on a downstream visual navigation task. We focus on Vision-and-Language Navigation (VLN) using the R2R dataset [3]. Because reaching the navigation goal requires successfully grounding natural language instructions to visual observations, this provides a challenging task-based assessment of prediction quality. 

In our inference setting, at each step while moving through the environment we use a baseline VLN agent based on [79] to generate a large number of possible future trajectories using beam search. We then rank these alternative trajectories using an instruction-trajectory compatibility model [84] to assess which trajectory best matches the 

7 


Figure 6: Visual comparison of ablated Image Generator outputs on Val-Unseen with _ground truth_ segmentation and depth. Both RGB and semantic context are important for best performance. 

instruction. The agent then executes the first action from the top-ranked trajectory before repeating the process. We consider three different planning horizons, with future trajectories containing 1, 2 or 3 forward steps. 

The instruction-trajectory compatibility model is a dualencoder that separately encodes textual instructions and trajectories (encoded using visual observations and path geometry) into a shared latent space. To improve performance on incomplete paths, we introduce truncated paths into the original contrastive training scheme proposed in [84]. The compatibility model is trained using only ground truth observations. However, during inference, RGB observations for future steps are drawn from three different sources: 

- **Ground truth** : RGB observations from the actual environment, i.e., look-ahead observations. 

- **Pathdreamer** : RGB predictions from our model. 

- **Repeated pano** : A simple baseline in which the most recent RGB observation is repeated in future steps. 

- **Blank pano** : A simple baseline in which blank images are provided as future observations. 

Note that in all cases the geometry of the future trajectories is determined by the ground truth R2R navigation graphs. In Table 3, we report Val-Unseen results for this experiment using standard metrics for VLN: navigation error (NE), success rate (SR), shortest path length (SPL), normalized Dynamic Time Warping (nDTW) [31], and success weighted by normalized Dynamic Time Warping (sDTW) [31]. 

Consistent with prior work [20, 73], we find that looking ahead using ground truth visual observations provides a robust performance boost, e.g., success rate increases from 44.6% with 1 planning step (top panel) to 59.3% with 3 planning steps (bottom panel). At the other extreme, the Repeated pano baseline is weak, with a success rate of just 

**Observations Plan Steps NE** _↓_ **SR** _↑_ **SPL** _↑_ **nDTW** _↑_ **sDTW** _↑_ 

|Repeated pano|1|6.75|35.7|33.8|52.0|31.2|
|---|---|---|---|---|---|---|
|Blank pano|1|7.29|35.9|33.7|50.9|31.5|
|Pathdreamer|1|6.55|39.9|38.3|54.6|35.2|
|Ground truth|1|5.80|44.6|42.7|58.9|39.4|
|Repeated pano|2|6.76|36.8|34.0|51.8|31.7|
|Blank pano|2|6.65|40.0|37.2|53.3|34.8|
|Pathdreamer|2|5.8|46.5|43.9|59.1|41.2|
|Ground truth|2|4.95|54.3|51.3|64.9|48.3|
|Repeated pano|3|6.25|40.6|37.7|55.6|35.2|
|Blank pano|3|6.48|41.9|38.8|54.2|36.1|
|Pathdreamer|3|5.32|50.4|47.3|61.8|44.4|
|Ground truth|3|4.44|59.3|55.8|67.9|52.7|


Table 3: VLN Val-Unseen results using an instructiontrajectory compatibility model to rank alternative future trajectories with planning horizons of 1, 2 or 3 steps. 

35.7% with 1 planning step (top row). The Blank pano baseline is similar, with a success rate of 35.9%. This is not surprising: these baselines deny the compatibility model any useful visual representation of the next action, which is crucial to performance [20, 73]. However, increasing the planning horizon does improve performance even for the Repeated/Blank pano baselines, since the compatibility model is able to compare the geometry of alternative future trajectories. Finally, we observe that using Pathdreamer’s visual observations closes about half the gap between the Repeated pano baseline and the ground truth observations, e.g., 50.4% success with Pathdreamer vs. 40.6% and 59.3% respectively for the others. We conclude that using Pathdreamer as a visual world model can improve performance on downstream tasks, although existing agents still rely on using a navigation graph to define the feasible action space at each step. Pathdreamer is complementary to current SOTA model-based approaches, and a combination would likely lead to further boosts in VLN performance, which is worth investigating in future work. 

# **5. Conclusion** 

Pathdreamer is a stochastic hierarchical visual world model that can synthesize realistic and diverse 360<sup>_◦_</sup> panoramic images for unseen trajectories in real buildings. As a visual world model, Pathdreamer also shows strong promise in improving performance on downstream tasks, which we show with VLN. Most notably, we show that Pathdreamer captures around half the benefit of looking ahead at actual observations from the environment. The efficacy of Pathdreamer in the VLN task may be attributed to its ability to model fundamental constraints in the real world, and thus relieve agents from having to learn the geometry and visual and semantic structure of buildings. Applying Pathdreamer to other embodied navigation tasks such as Object-Nav [5], VLN-CE [39] and street-level navigation [9, 53] are natural directions for future work. 

8 

# **References** 

- [1] Sandra Aigner and Marco K¨orner. Futuregan: Anticipating the future frames of video sequences using spatiotemporal 3d convolutions in progressively growing gans. _arXiv preprint arXiv:1810.01325_ , 2018. 2 

- [2] Peter Anderson, Angel Chang, Devendra Singh Chaplot, Alexey Dosovitskiy, Saurabh Gupta, Vladlen Koltun, Jana Kosecka, Jitendra Malik, Roozbeh Mottaghi, Manolis Savva, and Amir R. Zamir. On evaluation of embodied navigation agents. _arXiv preprint arXiv:1807.06757_ , 2018. 3 

- [3] Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko S¨underhauf, Ian Reid, Stephen Gould, and Anton van den Hengel. Vision-and-language navigation: Interpreting visually-grounded navigation instructions in real environments. In _CVPR_ , pages 3674–3683, 2018. 1, 2, 3, 5, 6, 7 

- [4] Mohammad Babaeizadeh, Mohammad Taghi Saffar, Danijar Hafner, Harini Kannan, Chelsea Finn, Sergey Levine, and Dumitru Erhan. Models, pixels, and rewards: Evaluating design trade-offs in visual model-based reinforcement learning. _arXiv preprint arXiv:2012.04603_ , 2020. 3 

- [5] Dhruv Batra, Aaron Gokaslan, Aniruddha Kembhavi, Oleksandr Maksymets, Roozbeh Mottaghi, Manolis Savva, Alexander Toshev, and Erik Wijmans. Objectnav revisited: On evaluation of embodied agents navigating to objects. _arXiv preprint arXiv:2006.13171_ , 2020. 1, 3, 8 

- [6] Lars Buesing, Theophane Weber, Yori Zwols, Sebastien Racaniere, Arthur Guez, Jean-Baptiste Lespiau, and Nicolas Heess. Woulda, coulda, shoulda: Counterfactually-guided policy search. In _ICLR_ , 2019. 1 

- [7] Angel Chang, Angela Dai, Thomas Funkhouser, Maciej Halber, Matthias Niessner, Manolis Savva, Shuran Song, Andy Zeng, and Yinda Zhang. Matterport3d: Learning from RGBD data in indoor environments. _International Conference on 3D Vision (3DV)_ , 2017. 2, 3, 5 

- [8] Matthew Chang, Arjun Gupta, and Saurabh Gupta. Semantic visual navigation by watching youtube videos. _NeurIPS_ , 2020. 3 

- [9] Howard Chen, Alane Suhr, Dipendra Misra, Noah Snavely, and Yoav Artzi. Touchdown: Natural language navigation and spatial reasoning in visual street environments. In _CVPR_ , 2019. 3, 8 

- [10] Silvia Chiappa, S´ebastien Racaniere, Daan Wierstra, and Shakir Mohamed. Recurrent environment simulators. _ICLR_ , 2017. 2 

- [11] Emily Denton and Rob Fergus. Stochastic video generation with a learned prior. 2018. 2, 4 

- [12] Helisa Dhamo, Keisuke Tateno, Iro Laina, Nassir Navab, and Federico Tombari. Peeking behind objects: Layered depth prediction from a single image. _Pattern Recognition Letters_ , 125:333–340, 2019. 3 

- [13] Alexey Dosovitskiy and Vladlen Koltun. Learning to act by predicting the future. In _ICLR_ , 2017. 2 

- [14] Frederik Ebert, Chelsea Finn, Alex X Lee, and Sergey Levine. Self-supervised visual planning with temporal skip connections. _Conference on Robot Learning (CoRL)_ , 2017. 2 

- [15] Chelsea Finn, Ian Goodfellow, and Sergey Levine. Unsupervised learning for physical interaction through video prediction. In _NeurIPS_ , pages 64–72, 2016. 2 

- [16] Chelsea Finn and Sergey Levine. Deep visual foresight for planning robot motion. In _ICRA_ , pages 2786–2793. IEEE, 2017. 1, 2 

- [17] Chelsea Finn, Xin Yu Tan, Yan Duan, Trevor Darrell, Sergey Levine, and Pieter Abbeel. Deep spatial autoencoders for visuomotor learning. In _ICRA_ , pages 512–519. IEEE, 2016. 1 

- [18] John Flynn, Michael Broxton, Paul Debevec, Matthew DuVall, Graham Fyffe, Ryan Overbeck, Noah Snavely, and Richard Tucker. Deepview: View synthesis with learned gradient descent. In _CVPR_ , pages 2367–2376, 2019. 3 

- [19] John Flynn, Ivan Neulander, James Philbin, and Noah Snavely. Deepstereo: Learning to predict new views from the world’s imagery. In _CVPR_ , 2016. 1, 3 

- [20] Daniel Fried, Ronghang Hu, Volkan Cirik, Anna Rohrbach, Jacob Andreas, Louis-Philippe Morency, Taylor BergKirkpatrick, Kate Saenko, Dan Klein, and Trevor Darrell. Speaker-follower models for vision-and-language navigation. _NeurIPS_ , 2018. 3, 8 

- [21] Tsu-Jui Fu, Xin Eric Wang, Matthew F Peterson, Scott T Grafton, Miguel P Eckstein, and William Yang Wang. Counterfactual vision-and-language navigation via adversarial path sampler. In _ECCV_ , pages 71–86, 2020. 3 

- [22] Ian J Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial networks. _NeurIPS_ , 2014. 4 

- [23] David Ha and J¨urgen Schmidhuber. World models. _NeurIPS_ , 2018. 1, 2 

- [24] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. _ICLR_ , 2019. 2 

- [25] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _arXiv preprint arXiv:2010.02193_ , 2020. 1, 2 

- [26] Meera Hahn, Jacob Krantz, Dhruv Batra, Devi Parikh, James M. Rehg, Stefan Lee, and Peter Anderson. Where are you? localization from embodied dialog. 2020. 1, 3 

- [27] Weituo Hao, Chunyuan Li, Xiujun Li, Lawrence Carin, and Jianfeng Gao. Towards learning a generic agent for visionand-language navigation via pre-training. In _CVPR_ , June 2020. 3 

- [28] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In _CVPR_ , pages 770–778, 2016. 3 

- [29] Phlipp Henzler, Volker Rasche, Timo Ropinski, and Tobias Ritschel. Single-image tomography: 3d volumes from 2d cranial x-rays. In _Computer Graphics Forum_ , volume 37, pages 377–388. Wiley Online Library, 2018. 3 

- [30] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. GANs trained by a two time-scale update rule converge to a local nash equilibrium. In _NeurIPS_ , 2017. 6 

9 

- [31] Gabriel Ilharco, Vihan Jain, Alexander Ku, Eugene Ie, and Jason Baldridge. General evaluation for instruction conditioned navigation using dynamic time warping. _NeurIPS Workshop on Visually Grounded Interaction and Language (ViGIL)_ , 2019. 8 

- [32] Phillip Isola, Jun-Yan Zhu, Tinghui Zhou, and Alexei A Efros. Image-to-image translation with conditional adversarial networks. _CVPR_ , 2017. 4 

- [33] Vihan Jain, Gabriel Magalhaes, Alexander Ku, Ashish Vaswani, Eugene Ie, and Jason Baldridge. Stay on the path: Instruction fidelity in vision-and-language navigation. 2019. 3 

- [34] Jindong Jiang, Lunan Zheng, Fei Luo, and Zhijun Zhang. Rednet: Residual encoder-decoder network for indoor rgbd semantic segmentation. _arXiv preprint arXiv:1806.01054_ , 2018. 3 

- [35] Xiaojie Jin, Huaxin Xiao, Xiaohui Shen, Jimei Yang, Zhe Lin, Yunpeng Chen, Zequn Jie, Jiashi Feng, and Shuicheng Yan. Predicting scene parsing and motion dynamics in the future. In _NeurIPS_ , pages 6915–6924, 2017. 2 

- [36] Justin Johnson, Alexandre Alahi, and Li Fei-Fei. Perceptual losses for real-time style transfer and super-resolution. In _ECCV_ , pages 694–711, 2016. 4 

- [37] Abhishek Kar, Christian H¨ane, and Jitendra Malik. Learning a multi-view stereo machine. In _NeurIPS_ , pages 365–376, 2017. 3 

- [38] Maximilian Karl, Maximilian Soelch, Justin Bayer, and Patrick Van der Smagt. Deep variational bayes filters: Unsupervised learning of state space models from raw data. _ICLR_ , 2017. 2 

- [39] Jacob Krantz, Erik Wijmans, Arjun Majundar, Dhruv Batra, and Stefan Lee. Beyond the nav-graph: Vision and language navigation in continuous environments. In _ECCV_ , 2020. 3, 8 

- [40] Alexander Ku, Peter Anderson, Roma Patel, Eugene Ie, and Jason Baldridge. Room-across-room: Multilingual visionand-language navigation with dense spatiotemporal grounding. _EMNLP_ , 2020. 1, 3 

- [41] Yong-Hoon Kwon and Min-Gyu Park. Predicting future frames using retrospective cycle gan. In _CVPR_ , pages 1811– 1820, 2019. 2 

- [42] Wonkwang Lee, Whie Jung, Han Zhang, Ting Chen, Jing Yu Koh, Thomas Huang, Hyungsuk Yoon, Honglak Lee, and Seunghoon Hong. Revisiting hierarchical approach for persistent long-term video prediction. In _ICLR_ , 2021. 2, 6 

- [43] Zuoyue Li, Zhaopeng Cui, and Martin R Oswald. Streetview panoramic video synthesis from a single satellite image. _arXiv preprint arXiv:2012.06628_ , 2020. 2 

- [44] Andrew Liu, Richard Tucker, Varun Jampani, Ameesh Makadia, Noah Snavely, and Angjoo Kanazawa. Infinite nature: Perpetual view generation of natural scenes from a single image. _arXiv preprint arXiv:2012.09855_ , 2020. 2 

- [45] Guilin Liu, Fitsum A Reda, Kevin J Shih, Ting-Chun Wang, Andrew Tao, and Bryan Catanzaro. Image inpainting for irregular holes using partial convolutions. In _ECCV_ , pages 85–100, 2018. 4 

- [46] Jiasen Lu, Dhruv Batra, Devi Parikh, and Stefan Lee. Vilbert: Pretraining task-agnostic visiolinguistic representations for vision-and-language tasks. In _NeurIPS_ , pages 13–23, 2019. 3 

- [47] Pauline Luc, Natalia Neverova, Camille Couprie, Jakob Verbeek, and Yann LeCun. Predicting deeper into the future of semantic segmentation. In _ICCV_ , pages 648–657, 2017. 2 

- [48] Chih-Yao Ma, Jiasen Lu, Zuxuan Wu, Ghassan AlRegib, Zsolt Kira, Richard Socher, and Caiming Xiong. Selfmonitoring navigation agent via auxiliary progress estimation. _ICLR_ , 2019. 3 

- [49] Chih-Yao Ma, Zuxuan Wu, Ghassan AlRegib, Caiming Xiong, and Zsolt Kira. The regretful agent: Heuristic-aided navigation through progress estimation. In _CVPR_ , pages 6732–6740, 2019. 3 

- [50] Arjun Majumdar, Ayush Shrivastava, Stefan Lee, Peter Anderson, Devi Parikh, and Dhruv Batra. Improving visionand-language navigation with image-text pairs from the web. _ECCV_ , 2020. 2, 3 

- [51] Arun Mallya, Ting-Chun Wang, Karan Sapra, and MingYu Liu. World-consistent video-to-video synthesis. _ECCV_ , 2020. 2, 3, 4 

- [52] Ricardo Martin-Brualla, Noha Radwan, Mehdi S. M. Sajjadi, Jonathan T. Barron, Alexey Dosovitskiy, and Daniel Duckworth. NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections. In _CVPR_ , 2021. 3 

- [53] Harsh Mehta, Yoav Artzi, Jason Baldridge, Eugene Ie, and Piotr Mirowski. Retouchdown: Adding touchdown to streetlearn as a shareable resource for language grounding tasks in street view. _EMNLP Workshop on Spatial Language Understanding (SpLU)_ , 2020. 3, 8 

- [54] Ben Mildenhall, Pratul P Srinivasan, Rodrigo Ortiz-Cayon, Nima Khademi Kalantari, Ravi Ramamoorthi, Ren Ng, and Abhishek Kar. Local light field fusion: Practical view synthesis with prescriptive sampling guidelines. _ACM Transactions on Graphics (TOG)_ , 38(4):1–14, 2019. 3 

- [55] Ben Mildenhall, Pratul P Srinivasan, Matthew Tancik, Jonathan T Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis. _ECCV_ , 2020. 3 

- [56] Piotr Mirowski, Andras Banki-Horvath, Keith Anderson, Denis Teplyashin, Karl Moritz Hermann, Mateusz Malinowski, Matthew Koichi Grimes, Karen Simonyan, Koray Kavukcuoglu, Andrew Zisserman, et al. The streetlearn environment and dataset. _arXiv preprint arXiv:1903.01292_ , 2019. 3 

- [57] Anusha Nagabandi, Gregory Kahn, Ronald S Fearing, and Sergey Levine. Neural network dynamics for model-based deep reinforcement learning with model-free fine-tuning. In _ICRA_ , pages 7559–7566. IEEE, 2018. 1 

- [58] Medhini Narasimhan, Erik Wijmans, Xinlei Chen, Trevor Darrell, Dhruv Batra, Devi Parikh, and Amanpreet Singh. Seeing the un-scene: Learning amodal semantic maps for room navigation. In _ECCV_ , pages 513–529. Springer, 2020. 3 

- [59] Khanh Nguyen and Hal Daum´e III. Help, anna! visual navigation with natural multimodal assistance via retrospective curiosity-encouraging imitation learning. _EMNLP_ , 2019. 3 

10 

- [60] Junhyuk Oh, Xiaoxiao Guo, Honglak Lee, Richard L Lewis, and Satinder Singh. Action-conditional video prediction using deep networks in atari games. In _NeurIPS_ , pages 2863– 2871, 2015. 2 

- [61] Junhyuk Oh, Satinder Singh, and Honglak Lee. Value prediction network. In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, _NeurIPS_ , 2017. 2 

- [62] Blazej Osinski, Chelsea Finn, Dumitru Erhan, George Tucker, Henryk Michalewski, Konrad Czechowski, Lukasz Mieczyslaw Kaiser, Mohammad Babaeizadeh, Piotr Kozakowski, Piotr Milos, Roy H Campbell, Afroz Mohiuddin, Ryan Sepassi, and Sergey Levine. Model-based reinforcement learning for atari. In _ICLR_ , 2020. 1, 2 

- [63] Taesung Park, Ming-Yu Liu, Ting-Chun Wang, and Jun-Yan Zhu. Semantic image synthesis with spatially-adaptive normalization. In _CVPR_ , pages 2337–2346, 2019. 2, 4, 7 

- [64] Aj Piergiovanni, Alan Wu, and Michael S Ryoo. Learning real-world robot policies by dreaming. In _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 7680–7687. IEEE, 2019. 1 

- [65] Senthil Purushwalkam, Sebastian Vicenc Amengual Gari, Vamsi Krishna Ithapu, Carl Schissler, Philip Robinson, Abhinav Gupta, and Kristen Grauman. Audio-visual floorplan reconstruction. _arXiv preprint arXiv:2012.15470_ , 2020. 3 

- [66] Yuankai Qi, Qi Wu, Peter Anderson, Xin Wang, William Yang Wang, Chunhua Shen, and Anton van den Hengel. Reverie: Remote embodied visual referring expression in real indoor environments. In _CVPR_ , 2020. 1, 3 

- [67] Manolis Savva, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, Vladlen Koltun, Jitendra Malik, Devi Parikh, and Dhruv Batra. Habitat: A Platform for Embodied AI Research. In _ICCV_ , 2019. 5 

- [68] Meng-Li Shih, Shih-Yang Su, Johannes Kopf, and Jia-Bin Huang. 3d photography using context-aware layered depth inpainting. In _CVPR_ , June 2020. 3 

- [69] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. _ICLR_ , 2015. 4 

- [70] Pratul P Srinivasan, Richard Tucker, Jonathan T Barron, Ravi Ramamoorthi, Ren Ng, and Noah Snavely. Pushing the boundaries of view extrapolation with multiplane images. In _CVPR_ , pages 175–184, 2019. 3 

- [71] Julian Straub, Thomas Whelan, Lingni Ma, Yufan Chen, Erik Wijmans, Simon Green, Jakob J. Engel, Raul Mur-Artal, Carl Ren, Shobhit Verma, Anton Clarkson, Mingfei Yan, Brian Budge, Yajie Yan, Xiaqing Pan, June Yon, Yuyang Zou, Kimberly Leon, Nigel Carter, Jesus Briales, Tyler Gillingham, Elias Mueggler, Luis Pesqueira, Manolis Savva, Dhruv Batra, Hauke M. Strasdat, Renzo De Nardi, Michael Goesele, Steven Lovegrove, and Richard Newcombe. The Replica dataset: A digital replica of indoor spaces. _arXiv preprint arXiv:1906.05797_ , 2019. 3 

- [72] Richard S. Sutton and Andrew G. Barto. _Reinforcement Learning: An Introduction_ . A Bradford Book, Cambridge, MA, USA, 2018. 1 

- [73] Hao Tan, Licheng Yu, and Mohit Bansal. Learning to navigate unseen environments: Back translation with environmental dropout. In _Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)_ , pages 2610–2621, 2019. 3, 8 

- [74] Jesse Thomason, Michael Murray, Maya Cakmak, and Luke Zettlemoyer. Vision-and-dialog navigation. In _Conference on Robot Learning (CoRL)_ , pages 394–406. PMLR, 2020. 1, 3 

- [75] Suhani Vora, Reza Mahjourian, Soeren Pirk, and Anelia Angelova. Future semantic segmentation leveraging 3d information. _ECCV 3D Reconstruction meets Semantics Workshop_ , 2018. 2 

- [76] Jacob Walker, Abhinav Gupta, and Martial Hebert. Patch to the future: Unsupervised visual prediction. In _CVPR_ , pages 3302–3309, 2014. 2 

- [77] Ting-Chun Wang, Ming-Yu Liu, Jun-Yan Zhu, Guilin Liu, Andrew Tao, Jan Kautz, and Bryan Catanzaro. Video-tovideo synthesis. _NeurIPS_ , 2018. 2 

- [78] Ting-Chun Wang, Ming-Yu Liu, Jun-Yan Zhu, Andrew Tao, Jan Kautz, and Bryan Catanzaro. High-resolution image synthesis and semantic manipulation with conditional gans. In _CVPR_ , pages 8798–8807, 2018. 4 

- [79] Xin Wang, Qiuyuan Huang, Asli Celikyilmaz, Jianfeng Gao, Dinghan Shen, Yuan-Fang Wang, William Yang Wang, and Lei Zhang. Reinforced cross-modal matching and selfsupervised imitation learning for vision-language navigation. In _CVPR_ , pages 6629–6638, 2019. 7 

- [80] Olivia Wiles, Georgia Gkioxari, Richard Szeliski, and Justin Johnson. Synsin: End-to-end view synthesis from a single image. In _CVPR_ , pages 7467–7477, 2020. 1, 3 

- [81] Fei Xia, Amir R. Zamir, Zhi-Yang He, Alexander Sax, Jitendra Malik, and Silvio Savarese. Gibson env: real-world perception for embodied agents. In _CVPR_ . IEEE, 2018. 3 

- [82] Jingwei Xu, Bingbing Ni, Zefan Li, Shuo Cheng, and Xiaokang Yang. Structure preserving video prediction. In _CVPR_ , pages 1460–1469, 2018. 2 

- [83] Alex Yu, Vickie Ye, Matthew Tancik, and Angjoo Kanazawa. pixelnerf: Neural radiance fields from one or few images. _arXiv preprint arXiv:2012.02190_ , 2020. 3 

- [84] Ming Zhao, Peter Anderson, Vihan Jain, Su Wang, Alex Ku, Jason Baldridge, and Eugene Ie. On the evaluation of visionand-language navigation instructions. In _Conference of the European Chapter of the Association for Computational Linguistics (EACL)_ , 2021. 7, 8 

- [85] Tinghui Zhou, Richard Tucker, John Flynn, Graham Fyffe, and Noah Snavely. Stereo magnification: Learning view synthesis using multiplane images. _SIGGRAPH_ , 2018. 3 

- [86] Fengda Zhu, Yi Zhu, Xiaojun Chang, and Xiaodan Liang. Vision-language navigation with self-supervised auxiliary reasoning tasks. In _CVPR_ , pages 10012–10022, 2020. 3 

- [87] Wanrong Zhu, Xin Wang, Tsu-Jui Fu, An Yan, Pradyumna Narayana, Kazoo Sone, Sugato Basu, and William Yang Wang. Multimodal text style transfer for outdoor vision-andlanguage navigation. _EACL_ , 2021. 3 

11 

# **A. Qualitative Results** 

## **A.1. Val-Unseen Results** 

We present additional qualitative results generated by the Pathdreamer model, on the Val-Unseen split of the R2R dataset. These environments are not seen by the model during training, and act as a test of the generalization ability of Pathdreamer. Figure 7 presents cherry-picked examples of Pathdreamer generated sequences and Figure 8 presents randomly chosen examples. 

## **A.2. Val-Seen Results** 

The Val-Seen split contains novel navigation trajectories for environments seen in the training split. As described in the main paper, the Structure Generator and Image Generator models perform significantly better on Val-Seen, since they can memorize the training environments with less generalization required. We observe that generation results maintain high fidelity even at large distances from the location of the input observation. Figure 9 presents cherrypicked examples and Figure 10 presents random examples. 

## **A.3. Noise Interpolation** 

As described in the main paper, the Structure Generator is able to generate alternative, diverse, _room reveals_ for a given scene. In areas without guidance pixels (i.e., in areas of the environment not seen from a previous view), interpolating over different noise vectors produces diverse and plausible outcomes. Figure 11 presents cherry-picked examples of Pathdreamer sequences when conditioned on different noise vectors. Figure 12 contains additional examples of randomly selected sequences conditioned on random noise vectors. 

# **B. Generated Videos** 

In addition to image generation, Pathdreamer is capable of generating continuous video sequences, simply by sequencing generated images with small viewpoint changes. We provide videos displaying Pathdreamer generated results for several unseen environments. We also compare Pathdreamer’s rendering quality using multiple observations to the output of the Habitat simulator using meshbased rendering, illustrating a favorable comparison in quality. We refer readers to the YouTube link<sup>2</sup> for the video results. 

that is used as input at each step is the ground-truth previous observation. During the teacher forcing stage, the number of ground truth context frames used for a path of length _L_ is decayed uniformly from _L −_ 1 to 1. After 30 epochs, we switch to the recurrent setting in which the model’s previous prediction is used as the previous observation at each step during the rollout (similar to our setup at inference time). We use the Adam optimizer with parameters _β_ 1 = 0 _._ 9 and _β_ 2 = 0 _._ 999. We apply a learning rate which starts at 1 _e_<sup>_−_4</sup> and warms up to 2 _e_<sup>_−_4</sup> uniformly over 10 epochs. 

**Image Generator** This model was trained with a batch size of 128 over 500 epochs. We use the Adam optimizer with parameters _β_ 1 = 0 _._ 5 and _β_ 2 = 0 _._ 999, and a learning rate of 2 _e_<sup>_−_4</sup> for both the generator and the discriminator. During training, the discriminator is trained for 2 steps for each generator training step. Following standard practice, at inference time we applied an exponential moving average (EMA) to the generator weights with 0.999 decay. For the choice of loss weights, we set _λ_ GAN = 1, _λ_ VGG = 0 _._ 07, and _λ_ FM = 0. We found experimentally that excluding the feature matching loss speeds up training throughput and did not have a significant effect on the results. 

**Evaluation Details** We compute the FID score<sup>3</sup> using 10,000 random samples for each prediction sequence step. As the R2R validation sets contain 783 and 340 sequences for Val-Unseen and Val-Seen respectively, we perform data augmentation with random horizontal roll and flips to acquire 10,000 samples. 

We run evaluation every 2000 training steps, and select the best checkpoint on the Val-Seen and Val-Unseen set for reporting results for the respective split. We note that training time is generally significantly longer on Val-Seen as compared to Val-Unseen. Due to the benefit of overfitting on the training set for Val-Seen, performance continues to improve on even as generalization performance on ValUnseen deteriorates. 

# **C. Implementation Details** 

**Structure Generator** We trained this model with a batch size of 64, over 50 epochs. For the first 30 epochs the model is trained with teacher forcing, i.e., the previous observation 

> 2https://youtu.be/StklIENGqs0 

> 3We used https://github.com/mseitzer/pytorch-fid for computing results. 

12 


Figure 7: Selected examples of predicted sequences from the Val-Unseen split using one ground truth observation as context. 

13 


Figure 8: Randomly selected prediction sequences from the Val-Unseen split using one ground truth observation as context. 

14 


Figure 9: Selected examples of predicted sequences from the Val-Seen split using one ground truth observation as context. 

15 


Figure 10: Random prediction sequences from the Val-Seen split using one ground truth observation as context. 

16 


(a) Several plausible scene layouts are predicted for the unknown region of the image on the right (indicated in black in the guidance inputs). Notably, Pathdreamer is able to synthesize a complete set of a bed, cushion, and chair in the second example (noise vector _z_ 2). 


(c) Several varying but plausible scenes are considered by Pathdreamer: (1) a window with curtains open at the side, (2) a window covered by curtains, and (3) a large floor to ceiling window on the right of the room. 

Figure 11: Diverse and semantically plausible predictions can be sampled for scenes containing previously unseen regions. Shown here are several selected examples, each consisting of three alternative room reveals and the corresponding ground truth (from Val-Unseen). 

17 


(c) This example contains stairs leading to a hallway, which is correctly predicted by the model. Several potential layouts are synthesized, although none of them fully synthesize the entire door frame present in the ground truth example. 

Figure 12: Random examples of generation results when sampled with different noise vectors. 

18 

