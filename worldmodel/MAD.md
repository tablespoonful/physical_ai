---
title: "MAD: Motion Appearance Decoupling for efficient Driving World Models"
date: "2026-01-14"
authors: "Ahmad Rahimi; Valentin Gerard; Eloi Zablocki; Matthieu Cord; Alexandre Alahi"
url: https://arxiv.org/abs/2601.09452
pdf: https://arxiv.org/pdf/2601.09452
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.09452)** / [論文ページ](https://arxiv.org/abs/2601.09452)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **MAD: Motion Appearance Decoupling for efficient Driving World Models** 

Ahmad Rahimi<sup>_∗_1</sup> Valentin Gerard<sup>_∗_1</sup> ´Eloi Zablocki<sup>2</sup> Matthieu Cord<sup>2</sup><sup>_,_3</sup> Alexandre Alahi<sup>1</sup> 1 Ecole Polythechnique Federal de Lausanne 2 valeo.ai 3 Sorbonne Universit´e first.last@epfl.ch first.last@valeo.com matthieu.cord@sorbonne-universite.fr 

## **Abstract** 

_Recent video diffusion models generate photorealistic, temporally coherent videos, yet they fall short as reliable world models for autonomous driving, where structured motion and physically consistent interactions are essential. Adapting these generalist video models to driving domains has shown promise but typically requires massive domainspecific data and costly fine-tuning. We propose an efficient adaptation framework that converts generalist video diffusion models into controllable driving world models with minimal supervision. The key idea is to decouple_ motion learning _from_ appearance synthesis _. First, the model is adapted to predict structured motion in a simplified form: videos of skeletonized agents and scene elements, focusing learning on physical and social plausibility. Then, the same backbone is reused to synthesize realistic RGB videos conditioned on these motion sequences, effectively “dressing” the motion with texture and lighting. This two-stage process mirrors a reasoning-rendering paradigm: first infer dynamics, then render appearance. Our experiments show this decoupled approach is exceptionally efficient: adapting SVD, we match prior SOTA models with_ **_less than 6% of their compute_** _. Scaling to LTX, our MAD-LTX model outperforms all open-source competitors, and supports a comprehensive suite of text, ego, and object controls. Project page: https://vita-epfl.github.io/MAD-WorldModel/_ 

## **1. Introduction** 

Professional animators do not begin by drawing final, photorealistic frames. They first create an _animatic_ , a sequence of simple, timed-out sketches, to perfect the core of the story: its pacing, composition, and, most critically, its _interactions_ and _motion_ [12]. The final, high-fidelity rendering of light, shadow, and texture is the last, almost mechanical, step. This principle of decoupling a complex creative task into _dynamics_ and _rendering_ is a powerful and fundamental approach. 

We apply this _animator_ principle to the central chal- 


Figure 1. (Top) Our decoupled two-stage pipeline: a Motion Forecaster first generates an abstract intermediate pose representation, which is then used by an Appearance Synthesizer to render the final, photorealistic video. (Bottom) Our method (MAD-LTX) achieves a state-of-the-art quality while requiring a fraction of the training compute budget compared to prior SOTA driving models. 

lenge of creating autonomous driving (AD) world models. Unlike general-purpose video generation models (VGMs), which are trained on large, diverse internet datasets to generate generic videos and primarily excel at visual realism, driving models must _also_ master the physically grounded, multi-agent _dynamics_ of traffic; a task that VGMs fail to capture off the shelf. This reveals the core difficulty: a driving world model must simultaneously master two coupled, complex responsibilities: photorealistic appearance and physical/social dynamics. 

Adapting existing general VGMs to the driving domain is therefore prohibitively expensive. Recent efforts illustrate this: VISTA [10] and GEM [16] consume 25,000 and 50,000 GPU-hours to fine-tune the SVD [6] backbone. More powerful models like Cosmos-Predict [28] are trained from scratch on massive, proprietary datasets, requiring compute resources that place them beyond the reach of most research labs. This high cost of adaptation prevents the AD community from fully leveraging the rapid, ongoing ad- 

1 

vances in general video modeling. 

We therefore propose **MAD** ( **M** otion- **A** ppearance **D** ecoupling), a new methodology for efficiently adapting any general VGM into a controllable driving world model. As illustrated in Fig. 1, we adapt a single VGM backbone to specialize in the two sequential stages of the animator’s workflow, using two lightweight LoRA [19] adapters: 

1. A **Motion Forecaster** masters the _animatic_ stage, learning to generate an abstract, skeletonized video that captures only the scene’s dynamics. This representation does not require new manual labels; we generate it at scale by applying off-the-shelf pose extractors [22, 43] as pseudo-labelers to our video data. 

2. An **Appearance Synthesizer** masters the _rendering_ stage, learning to “dress” this motion by rendering the final photorealistic video conditioned on the abstract skeleton poses. 

By having a _single model_ perform both sequential tasks, our framework is conceptually similar to the ’chain-ofthought’ paradigm, where a model ”reasons” by generating intermediate steps (the motion ”animatic”) before producing the final ”answer” (the rendered video). This singlemodel, two-step approach is further enhanced by a second key principle: maximal reuse of the base model’s learned representations. Instead of engineering new, complex conditioning mechanisms, we project all control signals, including the intermediate poses, the first frame, and even our novel ego-motion representation, into the model’s native visual latent space using its own pre-trained VAE. This allows the model to learn new control tasks while ‘speaking’ a visual language it already understands. 

We validate this framework by creating MAD-SVD and MAD-LTX. As a proof-of-concept, MAD-SVD builds on the SVD backbone and achieves quality competitive with VISTA [10] and GEM [16] while using **less than 6% of their compute and data** . We then scale this methodology to create **MAD-LTX** , an open-source, state-of-the-art driving model building on the LTX backbone. MAD-LTX outperforms all previous open driving models and achieves generation quality comparable to the top-performing, openweight Cosmos Predict 2 [28]. This is accomplished while using only **a fraction of compute and data budget** of competitors, and supporting a combination of text, ego-motion, and object-motion controls. 

**Contributions.** Our main contributions are: 

- A novel methodology that decouples motion forecasting from appearance synthesis, enabling highly efficient adaptation of general VGMs. 

- An efficient adaptation framework that reuses a single backbone with lightweight LoRAs and leverages the model’s native VAE for all conditioning, proving more efficient than standard fine-tuning. 

- **MAD-LTX** , a new open-source, SOTA driving world model (2B & 13B) that is the fastest open-source driving world model and supports a comprehensive suite of text, ego-motion, and object-motion controls. 

## **2. Related Work** 

### **2.1. Driving World Models** 

World models [13] aim to learn action-conditioned dynamics of an environment, predicting plausible futures while capturing underlying physical regularities and agent behaviors that generalize to rare or unseen situations. Beyond future prediction, such models support a wide range of downstream applications, including policy learning [15] where agent can plan inside the learned model rather than in the real environment, representation learning [3, 4] via predictive objectives, and large-scale synthetic data generation [33]. 

In autonomous driving, world models have been instantiated using diverse input parameterizations that reflect different modeling objectives. Semantic BEV and occupancycentric [7, 23, 49] approaches forecast the evolution of road topology, traffic participants, and freespace in a structured mid-level representation aligned with classical planning pipelines. In contrast, LiDAR-based [5, 24] and implicit 4D occupancy-flow models operate directly on dense geometric structure to enable high-fidelity reconstruction. Moving beyond structured ontology-based scene abstractions, video-based driving world models directly generate future ego-centric RGB observations. 

These approaches differ in their sensor assumptions: multi-view methods [18, 34, 44] exploit surround-camera geometry for 3D-consistent scene generation, whereas single-view models [4, 10, 16, 28, 42, 48] operate purely from monocular ego video, offering a critical scalability advantage, as monocular driving video can be collected at scale, even from unconstrained Internet sources [1, 41]. Our work focus on this single-view paradigm, which naturally connects with generalist video generation models literature. 

### **2.2. Generalist Video Generation Models** 

Generalist video generation models [6, 14, 21, 38, 45] are commonly pretrained on large, weakly curated Internetscale video corpora, which endow them with broad visual and temporal priors. 

Despite their impressive visual realism, recent benchmarks [27, 30, 39, 47] show that such models struggle with physical consistency, multi-object dynamics, and causal interactions. They tend to reproduce statistically dominant motion patterns rather than adapting to perturbed environments, causing systematic failures in scenarios requiring agent coordination or physics reasoning. These limitations highlight a gap between generalist video generators 

2 

and the physically grounded world-modeling capabilities needed for reliable driving simulation. 

To compensate for these limitations, several domain adaptation strategies have emerged, each targeting the lack of diverse and physically grounded motion patterns in generalist models. Models trained on weakly curated crowdsourced driving videos [41], such as VISTA [10] and GEM [16], adapt SVD [6] through large-scale fine-tuning on OpenDV [41], requiring substantial computational budgets (approximately 25k and 50k GPU-hours, respectively). Other approaches incorporate synthetic trajectories to enrich multi-object dynamics. ReSim [42] adapts CogVideoX [45] via large-scale, 13k GPU-hour fine-tuning, augmenting training dataset with CARLA [8]-generated trajectories. At the industrial scale, models such as GAIA [18, 34] and Cosmos-Predict [28] circumvent the adaptation bottleneck entirely by training driving-oriented world models from scratch on massive proprietary datasets. 

Together, these efforts underscore that accurately modeling multi-object dynamics remains highly data- and compute-intensive. Our approach aims to reduce this burden by enabling efficient transfer from generalist video generators to driving world models. 

### **2.3. Prior works factorizing motion and appearance** 

Recent findings show that two-stage video generation pipelines, where an intermediate motion representation is predicted before appearance synthesis, improve temporal coherence, especially in sequences exhibiting large motion. In these approaches, two diffusion models are applied sequentially: the first one predicts a coarse motion signal (e.g., an object-level mask video [46], dense pixel-wise motion fields [35], or flow- and depth-based geometric cues [25]), and the second one synthesizes the final video conditioned on this predicted motion representation. We adopt a similar decoupling of motion prediction and appearance synthesis through pose based representation, and show that it enables efficient adaptation to driving scenes with complex, structured multi-agent motion. 

In the driving domain, Epona [48] adopts an autoregressive formulation in which a dedicated trajectory predictor models future ego motion, while a video generator produces the corresponding visual sequence. This coupling stabilizes long-horizon predictions and allows the model to incorporate planning signals. However, because the intermediate motion representation is limited to the ego vehicle, it cannot capture the multi-agent interactions required to fully disentangle motion from appearance in complex driving environments. To the best of our knowledge, we are the first to fully separate multi-agent motion prediction from appearance synthesis in a driving world model. 

A different family of methods focus on appearance-level editing for data augmentation, where visual attributes such 

as weather, illumination, or style are modified while keeping the underlying scene structure fixed. These models [29, 33, 44] condition synthesis on HD-maps, semantic layouts or trajectories extracted from real videos, which provide a static description of geometry and motion. Although this connects to the appearance-synthesis stage of our pipeline, their conditioning structure is extracted rather than predicted, thus placing these methods in an editing task rather than a predictive setting. 

## **3. MAD Method** 

This section first defines the problem formulation and our core design intuition in Sec. 3.1. It follows by describing our intermediate motion representation for driving scenes (Sec. 3.2), then details our methodology for the design and training of the motion forecaster (Sec. 3.3), its optional control signals (Sec. 3.4), and the appearance synthesizer (Sec. 3.5). 

### **3.1. Motivation** 

Generative models, such as diffusion or flow-based models _fθ_ , learn to map a simple prior distribution _N_ (e.g., a Gaussian) to a complex data distribution _X_ . This mapping can be _fθ_ denoted as _N −→X_ . For video generation, unconditional sampling from the video distribution _X_ is of limited use. Practical models are conditioned on a set of control signals C, such as the first frame _I_ or a text prompt _T_ , to guide the _fθ_ synthesis process: _N −→ X_ . 

C 

Driving world models are a specific instance of this setting: they must generate realistic driving scenarios conditioned on high-level ego-vehicle commands. This is particularly challenging as it requires jointly modeling two complex and coupled factors: 1) the dynamic, realistic motion of all actors, and 2) the photorealistic synthesis of pixel-level appearance. Modeling both simultaneously is exceptionally data-intensive and computationally demanding. 

Our core intuition is to decouple this joint problem. We first introduce an intermediate motion representation, _M_ , which abstracts away photorealistic appearance to represent only the scene’s underlying motion. We then decompose the generation process into two distinct, more manageable stages: 

1. A **Motion Forecaster** ( _Fθ_ ) generates a future motion representation _M_ from noise, conditioned on motioncentric controls Cmotion (e.g., text, ego-motion, or first _Fθ_ 

RGB frame providing context): _N −−−→_ Cmotion<sup>_M_.</sup> 

2. An **Appearance Synthesizer** ( _Sθ_ ) then renders the final, photorealistic video _X_ , conditioned on the generated motion _M_ and appearance-based controls Cappearance _Sθ_ 

(e.g., the first RGB frame): _N −−−−−−−−→{M,_ Cappearance _}_<sup>_X_.</sup> 

3 


Figure 2. **Training pipeline of our two models.** a) depicts how the pose video is noised in the diffusion process and given as input to the LoRA of the base DiT model, namely _Fθ_ , together with different conditions such as text captions, first frame in RGB and optionally, our visual representation of the ego motion and other objects location. The denoised pose tokens can be decoded back to the generated pose video at inference time. Similarly, b) shows the training scheme for our appearance synthesizer model _Sθ_ , which takes the same text tokens and the visual tokens of the pose video, noised where the token contains skeletons in the “targeted noise injection” block, and denoises RGB video tokens. At inference time, both models are used sequentially, with the generated pose video of the first model being used to control the generation of the second one. 

This two-stage pipeline forms our methodology. A key aspect of our approach is to avoid training _Fθ_ and _Sθ_ from scratch. We argue that large-scale, general video generation models already possess significant latent knowledge of both motion dynamics and visual appearance. We therefore adapt a pre-trained base model to these two specialized tasks by fine-tuning with LoRA [19]. This strategy maximally leverages the base model’s powerful visual priors, drastically reducing the training burden and ensuring our conditioning signals operate within a familiar latent space. 

### **3.2. Intermediate Motion Representation** 

Our intermediate motion representation, _M_ , is designed to isolate the motion dynamics of the scene by abstracting away photorealistic textures. We define _M_ as a “pose video”, a sequence of frames rendered on a black background, depicting the skeletons of dynamic agents (cars, pedestrians) and key static elements (lane lines). Joints and edges are plotted in distinct colors to differentiate agent types. To generate our training data, we extract these poses from real videos using off-the-shelf models [22, 43] to create pseudo-labels. 

As shown in Fig. 3, we explored several representa- 

tions. While HDMaps (3D bounding boxes) are common in classical motion forecasting, they have three drawbacks for our generative setting: 1) They are too abstract, making it difficult for the VGM to realize the bounding box represents a car or pedestrian. Hence the model can not leverage its learned priors, which hurts knowledge transfer. 2) This abstraction gap also burdens the appearance synthesizer, which must learn to correlate simple boxes with complex vehicle appearances. 3) They are not scalable, as they require a full AV perception stack and are limited to small, annotated datasets. In contrast, both panoptic segmentation and our pose representation are highly scalable, as pseudo-labels can be generated for any video. However, as Fig. 3 shows, panoptic segmentation, while pixelaccurate, is largely 2D and struggles to capture 3D orientation or detailed pedestrian articulation. Our pose representation strikes the best balance: it is scalable, 3D-aware, and provides an object-centric structure that aligns well with the priors of VGMs, simplifying both forecasting and synthesis. 

### **3.3. Motion Forecaster** 

Our Motion Forecaster, _Fθ_ , is designed to generate the future pose video _M_ . While standard motion forecasting of- 

4 


Figure 3. **Comparison of intermediate representations** _M_ **.** HDMaps are abstract and non-scalable. Panoptic segmentation is 3D-blind and struggles with pedestrian details. Our pose-based representation provides a scalable, 3D-aware, and object-centric structure that is ideal for both forecasting and synthesis. 

ten relies on Transformer-based architectures [9, 40], these approaches present several fundamental limitations for our _generative_ world-model task. First, they are typically deterministic, designed to forecast the future states of _existing_ agents, and are incapable of “imagining” new agents entering the scene. Second, they often require a history of multiple observation states, whereas our goal is to generate from a _single_ frame. Finally, such models would need to learn visual context (like the first RGB frame) from scratch, a highly data-intensive process. We therefore bypass these issues by reformulating the task as a _generative_ one, finetuning a pre-trained VGM on our pose videos _M_ . This generative approach not only learns the distribution of plausible driving motions exceptionally fast but also inherently supports the generation of new agents. It also allows us to leverage the VGM’s strong, pre-trained visual priors to understand the first RGB frame, as we detail below. 

A key methodological finding is the importance of operating within the VGM’s “comfort zone”. While the model can technically handle arbitrary inputs, we found that training at its native resolution and frame rate was critical. Downsampling the data (e.g., to reduce FPS or resolution) significantly degraded forecasting quality, as it forced the model to learn new, out-of-distribution motion priors, which requires substantially more data. By respecting the model’s pre-trained priors, we minimize the adaptation cost. 

As illustrated in Fig. 2 panel (a), the forecaster _Fθ_ is trained as a latent diffusion model, conditioned on the initial state of the scene. A core principle of our design is to leverage the base model’s pre-trained VAE for all visual conditioning, eliminating the need for new adapter networks. The forecaster is conditioned on the initial scene state and an optional text prompt, which are integrated into the DiT as follows: 

- **Noisy Latent & First Pose Frame:** The pose video _M_ is 


Figure 4. **Illustration of our visual ego-motion representation** , showing three frames from a car turning left. The ego-camera is surrounded by a static, textured sphere and dust particles. Rotations can be inferred from the background’s apparent motion (moving right), while speed is encoded by the parallax motion of the particles. Blue dots represent the car’s trajectory, and the markings show how the movement between sphere texture and static elements in the background are aligned. 

encoded into latents _z_ = _E_ VAE( _M_ ). These latents _z_ 1 _...T_ are noised according to the base model’s training schedule. To condition on the initial state, the latent features _z_ 0 corresponding to the first pose frame are kept clean (i.e., not noised) and concatenated to the noised sequence. 

- **Text Prompt:** Unlike prior driving models that omit text [10, 16], we retain it for prompt-based motion control. We adopt the base model’s standard text conditioning, encoding prompts with a T5 [32] encoder and integrating them via cross-attention. 

- **First RGB Frame:** While _z_ 0 provides the initial pose, the first RGB frame _I_ 0 contains crucial context (e.g., traffic light state, object presence) that may be lost during pose extraction. We encode _I_ 0 using the VAE and concatenate its latent representation _c_ rgb = _E_ VAE( _I_ 0) to the DiT input sequence as additional context. This cross-modal conditioning is remarkably data and compute efficient, as the VGM backbone already possesses a deep understanding of RGB images from its pre-training. 

### **3.4. Controllable Motion Conditioning** 

A key requirement for a driving world model is controllability. Our framework supports this through the text prompts (as described in Sec. 3.3) and two additional, _conditioning signals_ that are fed to the Motion Forecaster: 

- **Ego-Motion Control:** To control the ego-vehicle, we devise a novel visual representation for its 3D camera pose. We render a video _V_ ego from the ego-camera’s perspective as it moves within a synthetic world. As illustrated in Fig. 4, this world consists of a static sphere with a colored checkerboard texture and static dust particles. Rotations are inferred from the apparent motion of the checkerboard (e.g., the background moves right as the car turns left), while translations are captured by the parallax mo- 

5 

tion of the dust particles. As highlighted by the markings in Fig. 4, the apparent motion of the background texture is designed to closely correspond to the motion of static objects in the real video. We find this visual representation allows the VGM to easily correlate the control input with the expected evolution of the scene. This video is encoded by the VAE, and its latent _c_ ego = _E_ VAE( _V_ ego) is concatenated to the DiT sequence. 

- **Object Movement Control:** To enable fine-grained scenario creation, we introduce an optional control for object motion. We first extract 2D bounding boxes from our pose data and run a tracker to get object trajectories. During training, we randomly select up to 5 tracks, render their bounding box trajectories onto a black background to create a sparse control video _V_ obj, and encode it via the VAE ( _c_ obj = _E_ VAE( _V_ obj)). This sparsity in training mimics the inference-time use case, where a user typically wants to control only a few specific agents. 

### **3.5. Appearance Synthesizer** 

The second stage of our pipeline is the Appearance Synthesizer, _Sθ_ , which is trained to generate the final photorealistic video _X_ . It is conditioned on the first RGB frame _I_ 0, a text prompt _T_ , and the intermediate motion representation _M_ . The text and first-frame conditioning follow the same method as the forecaster model. 

The primary conditioning signal is the pose video _M_ , which is encoded _c_ pose = _E_ VAE( _M_ ) and concatenated to the DiT input. A key challenge arises from the discrepancy between training and inference: during training, the model is conditioned on clean, ground-truth pose videos _M_ gt extracted using pseudo-labelers, but at inference, it receives the predicted _M_ pred from the motion forecaster, which contain artifacts (e.g., blurry or bent lines). 

To bridge this domain gap, we simulate inference-time imperfections during training, as shown in Fig. 2 (b) (targeted noise injection block). We apply a targeted noising strategy to the ground-truth pose latents _c_ pose. This choice is deliberate: we add noise in the _latent space_ because _Fθ_ is a latent diffusion model, and its artifacts (blurriness, bent lines) are more faithfully represented as latent-space noise rather than simple pixel-space noise. Furthermore, we observe that the background generated by _Fθ_ is not noisy. We therefore add Gaussian noise with a random variance _σ ∼ U_ (0 _,_ 0 _._ 3) only to a sparse set of the latent features corresponding to the rendered skeleton parts and keep the black background latents clean. This targeted strategy forces _Sθ_ to become robust to imperfections in the motion structure without corrupting the clean background, which we find improves the quality of the final synthesized video. 

## **4. Experiments** 

This section validates our proposed methodology. We first provide a detailed overview of our datasets, evaluation protocols, and baseline models in Sec. 4.1. We then present Sec. 4.2, a proof-of-concept implementation, MAD-SVD, which demonstrates our method’s efficiency by adapting a general video model to the driving domain. Sec. 4.3 details our primary contribution, MAD-LTX, which scales our approach to a more recent foundation model to achieve stateof-the-art generation quality and controllability. Finally, Sec. 4.4 presents a series of ablation studies that justify our key design choices. 

### **4.1. Experimental Setup** 

**Dataset and Preprocessing:** Our primary dataset, OpenDV [41], consists of 1700 hours of driving footage from YouTube. We preprocess videos to 24fps at a 1056 _×_ 704 resolution. We then extract our intermediate motion representation _M_ by using OpenPifPaf [22] for car and lane poses and DWPose [43] for human poses. We segment the videos into 5-second clips (120 frames) with a 3-second overlap. To improve data quality, we filter out 50% of the clips with the lowest object counts. OpenDV provides distinct training and validation video splits. To create our dataset, we sample 100,000 clips exclusively from the training videos and 5,000 clips exclusively from the validation videos. This ensures no data leakage between our training and validation sets, despite the 3-second overlap in clip extraction. To generate text conditioning _T_ , we use Qwen2.5-VL-32B-Instruct [2] to produce a caption based on the first frame of each clip. We also utilize the Waymo Perception dataset [36], extracting 20-second clips from the front camera, along with the HDMap representation, used for training and evaluating our ablation study. 

**Evaluation Metrics:** We report FID [17] and FVD [37] in the Appendix (Sec. 6.2) for completeness. However, as noted by recent works [11], we find these metrics correlate poorly with perceptual quality and motion realism in complex driving scenarios. Our primary evaluation is a human study, where participants were shown videos generated from 100 random scenes from the OpenDV [41] validation set. In a pairwise “A/B” test, users were asked to choose which video (from two models, starting from the same initial frame) was superior in: 1) general quality, 2) motion realism, and 3) visual quality. This study collects preference scores across 14 model comparisons. We share a screenshot of the website we developed to collect human preferences in the Supplementary Material (Sec. 7). 

6 


Figure 5. **Human preference study comparing MAD-LTX against competing models.** Bars show how often each model is preferred in head-to-head comparisons. ‘*’ denotes proprietary models which use private datasets and significant computational resources. 


Figure 6. **Human preference study comparing MAD-SVD against Vista [10] and GEM [16],** which are all based on the save SVD [6] backbone, while MAD-SVD uses only 6% of Vista and 3% of GEM’s computation budget. Bars show how often each model is preferred in head-to-head comparisons, which demonstrate that MAD-SVD is able to reach performance of Vista, and get close to GEM’s performance only with a fraction of their compute budget. 

**Training Details:** Both the Motion Forecaster ( _Fθ_ ) and Appearance Synthesizer ( _Sθ_ ) are initialized from the same base video model (SVD [6] or LTX [14]) and fine-tuned using LoRA [19]. We use the AdamW [26] optimizer with a learning rate of 2 _×_ 10<sup>_−_4</sup> and a batch size of 32. The motion forecaster _Fθ_ is trained for 9,000 steps on 139 hours of driving video from OpenDV. The appearance synthesizer _Sθ_ is subsequently trained for 5,000 steps. All experiments are conducted on 32 GH200 GPUs. Total fine-tuning for our LTX-based model takes 128 GPU hours for the 2B size and 700 GPU hours for 13B size, and 1500 GPU hours for our SVD-based model. Full training hyperparameters and details are listed in Appendix (Sec. 8). 

**Baselines:** We apply our methodology to two base models, SVD [6] and LTX [14] to create a driving-specific model, “MAD-SVD” and “MAD-LTX”, respectively. We compare our MAD-SVD against existing SVD-based driving models: **VISTA** [10] and **GEM** [16]. We also compare against our state-of-the-art models, the MAD-LTX, with the **Cosmos** [28] suite, a state-of-the-art model with two versions: _Predict 1_ (7B, 14B), for which a paper and weights are available, and _Predict 2_ (2B, 14B), which is a more powerful model with open weights. Since no LTX-based 

driving models exist for comparison, we establish our own key baseline, Fine-tuned LTX. This model is a LoRA finetune of the LTX model on our OpenDV dataset for the same compute budget as our MAD-LTX, trained end-to-end without our two-stage decoupling. This provides a rigorous, ‘apples-to-apples’ comparison to validate our method’s efficacy. 

### **4.2. Proof-of-Concept: MAD-SVD** 

To first validate our method’s efficiency, we implement MAD-SVD by adapting the Stable Video Diffusion (SVD) [6] model. We fine-tune two separate LoRAs from the SVD backbone: a Motion Forecaster ( _Fθ_ ) to generate 25 frames of pose video _M_ , and an Appearance Synthesizer ( _Sθ_ ) to render the final video _X_ . 

As shown in Fig. 6, we compare MAD-SVD to SVD [6], VISTA [10] and GEM [16], two state-of-the-art driving models also based on SVD. The results are highly encouraging: MAD-SVD achieves competitive generation quality while using a fraction of the resources. Notably, compared to VISTA, our method requires over **12** _×_ **less data** (139 hrs vs. 1,700) and **16** _×_ **less compute** (1500 GPUhrs vs. 25,000). This experiment serves as a strong proofof-concept, demonstrating that our decoupled methodology enables efficient adaptation of general video models into specialized world models, bypassing the need for massive, domain-specific training. 

### **4.3. Scaling to State-of-the-Art: MAD-LTX** 

Having validated our method’s efficiency, we now apply it to the large-scale LTX foundation model to create our stateof-the-art driving world model, MAD-LTX. We create and evaluate models at both 2B and 13B scales. 

**Evaluation of Generation Quality.** As established in Sec. 4.1, we find that standard metrics like FID and FVD correlate poorly with perceptual quality in this domain (see Sec. 6.2). We therefore rely on our large-scale human preference study as the primary measure of generation quality. 

The results of our human study, presented in Fig. 5, lead to three key conclusions: 

7 

1. **MAD-LTX outperforms all previous open-source driving models.** At both model scales, MAD-LTX is significantly preferred over SOTA driving models like GEM [16], VISTA [10], and the proprietary model Cosmos Predict 1 [28]. 

2. **Our method is superior to naive fine-tuning.** MADLTX is strongly preferred over our _Fine-tuned LTX_ baseline (29 pref. vs. 16 for 2B and 33 pref. vs. 15). This result is critical, as it confirms that our decoupled, twostage methodology is the primary driver of quality, not just the LTX backbone or the training data. 

3. **MAD-LTX is competitive with closed-source SOTA.** Our open-source MAD-LTX-13B model achieves generation quality nearly on par with the closed-source Cosmos Predict 2 (14B), while being trained with a fraction of the data and compute, and being significantly faster at inference time. 

**Evaluation of Open-Loop Motion Planning** To specifically evaluate the planning capabilities enabled by our Motion Forecaster, we conduct an evaluation designed to isolate the model’s open-loop planning ability. We generate 6 unconditional videos (k=6) for each of the 1,500 validation clips. We then use MapAnything [20] to extract the ego-vehicle trajectory from both the ground-truth and generated videos. Tab. 1 reports the minimum Average Displacement Error (minADE@6) and the Average Pairwise Distance (APD@6) over a 5-second horizon. 

1. **MAD-LTX achieves superior planning accuracy.** Our model consistently yields the lowest minADE6, outperforming the Base LTX and our standard Fine-tuned LTX baseline across both scales. This performance gain demonstrates that by modeling in the intermediate pose representation space, the Motion Forecaster captures realistic scene interactions and long-term dynamics more effectively than baselines operating directly in video space. 

2. **MAD-LTX is less prone to mode collapse.** We observe that standard fine-tuning significantly degrades diversity of predicted trajectories, with APD6 lower by 37.8% comparing to MAD-LTX for the 13B size and causing a 40% degradation in minADE6. We believe this is caused by the well-known phenomenon of memorization in diffusion models, which is especially likely to occur when large models are fine-tuned on small datasets. While direct video fine-tuning hurts model diversity, MADLTX avoids this by predicting motion in an abstract pose space. Because this representation removes visual textures and cues, the model is forced to learn the underlying movement rather than spurious correlations ( _e.g_ ., always stopping when observing an ambulance, or turning left when seeing a pedestrian wearing pink). 

Table 1. **Open-loop motion planning evaluation** on OpenDV [41] over a 5s horizon. We evaluate planning accuracy (minADE6, _↓_ in meters) and trajectory diversity (APD6, _↑_ in cm). Our MADLTX model achieves the best accuracy while maintaining high diversity. 

|Model|**2B**Mod|el|**13B**Mo|del|
|---|---|---|---|---|
||minADE6 _↓_|APD6 _↑_|minADE6 _↓_|APD6 _↑_|
|Base LTX [14]|5.42|**102.96**|4.14|**101.46**|
|Fine-tuned LTX|5.28 (+2.6%)|68.20|5.83(-40%)|63.06|
|MAD-LTX (ours)|**4.88 (+10%)**|76.21|**3.64 (+12%)**|101.45|


Table 2. **Human preference (%) for ablations on noise strategy and intermediate representation.** Each value shows the preference for our final MAD-LTX-2B model when compared head-tohead against the variant in the row. 

|Ablated Model<br>Human|Pref. for MAD-LTX-2B (%)_↑_|
|---|---|
||(Our model is better)|
|MAD-LTX 2B w/o noise|62%|
|MAD-LTX 2B (Panoptic Seg.)|74%|
|MAD-LTX 2B (HDMap)|78%|


### **4.4. Ablation Studies** 

We conduct two ablation studies using human preference to validate our primary design choices for the MAD-LTX-2B model. 

**Noise Addition to Appearance Synthesizer.** To bridge the domain gap between clean ground-truth poses ( _M_ gt) at training and the potentially imperfect predicted poses ( _M_ pred) at inference, we introduce a targeted noising strategy to the _Sθ_ ’s conditioning, as detailed in our methodology. Tab. 2 compares our full model against a variant trained “w/o noise.” The strong human preference for our model confirms that this strategy is critical for stabilizing generation and improving the sharpness of the final video. 

**Intermediate Representation (** _M_ **).** A key design choice is the intermediate representation _M_ , as discussed in Sec. 3.2. It must be abstract enough for _Fθ_ to forecast, yet descriptive enough for _Sθ_ to render. We test two alternatives: 1) **Panoptic Segmentation** (with tracking) and 2) **HDMap** (3D bounding boxes with road lanes). The human study in Tab. 2 confirms our pose-based representation is most effective. Our hypothesis is that this strikes an optimal balance: segmentation is pixel-aligned (good for _Sθ_ ) but loses 3D orientation (bad for _Fθ_ ), while HDMaps are 3D-aware (good for _Fθ_ ) but not pixel-aligned (bad for _Sθ_ ). Skeleton poses capture the best of both. 

8 

## **Conclusion** 

We introduced MAD, a novel methodology for efficiently adapting general-purpose video foundation models into high-fidelity, controllable driving world models. By decoupling structured motion learning from appearance synthesis, our framework efficiently converts generalist models into controllable driving world models, bypassing the prohibitive compute and data costs of traditional fine-tuning. Our decoupled adaptation is orders of magnitude more efficient than prior work. When scaled, our MAD-LTX model outperforms open-source competitors and achieves generation quality comparable to top-tier proprietary models (Cosmos Predict 2) with a significantly faster inference speed. 

Our work presents a highly efficient paradigm for creating specialized, controllable world models from general video generation models. Model weights, code and data collected during our user study will be open sourced. We hope this work will contribute to reduce the latency between architectural progress in video generation models and their subsequent adoption for driving specialized world models. 

## **Acknowledgments** 

This work was supported as part of the Swiss AI Initiative by a grant from the Swiss National Supercomputing Centre (CSCS) under project ID a144 on Alps. It has also been supported by Hasler Foundation under the Responsible AI program, Swiss National Science Foundation (SNSF) through the project Grant:10003100, chair VISA DEEP (ANR-20CHIA-0022), Cluster PostGenAI@Paris (ANR-23-IACL0007, FRANCE 2030), and Valeo. We also thank the participants who took part in the human evaluation for their time and insights. 

## **References** 

- [1] Md Shadab Alam, Marieke Martens, Olena Bazilinska, and Pavlo Bazilinskyy. Understanding global pedestrian behaviour in 565 cities with dashcam videos on youtube. Technical report, 2025. 2 

- [2] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 6, 1 

- [3] Adrien Bardes, Quentin Garrido, Jean Ponce, Xinlei Chen, Michael Rabbat, Yann LeCun, Mahmoud Assran, and Nicolas Ballas. Revisiting feature prediction for learning visual representations from video, 2024. 2 

- [4] Florent Bartoccioni, Elias Ramzi, Victor Besnier, Shashanka Venkataramanan, Tuan-Hung Vu, Yihong Xu, Loick Chambon, Spyros Gidaris, Serkan Odabas, David Hurych, Renaud 

Marlet, Alexandre Boulch, Mickael Chen, Eloi<sup>´</sup> Zablocki, Andrei Bursuc, Eduardo Valle, and Matthieu Cord. Vavim and vavam: Autonomous driving through video generative modeling, 2025. 2 

- [5] Hengwei Bian, Lingdong Kong, Haozhe Xie, Liang Pan, Yu Qiao, and Ziwei Liu. Dynamiccity: Large-scale 4d occupancy generation from dynamic scenes, 2025. 2 

- [6] Andreas Blattmann, Tim Dockhorn, Sumith Kulal, Daniel Mendelevitch, Maciej Kilian, Dominik Lorenz, Yam Levi, Zion English, Vikram Voleti, Adam Letts, Varun Jampani, and Robin Rombach. Stable video diffusion: Scaling latent video diffusion models to large datasets. _CoRR_ , abs/2311.15127, 2023. 1, 2, 3, 7 

- [7] Junliang Chen, Huaiyuan Xu, Yi Wang, and Lap-Pui Chau. Occprophet: Pushing efficiency frontier of camera-only 4d occupancy forecasting with observer-forecaster-refiner framework, 2025. 2 

- [8] Alexey Dosovitskiy, German Ros, Felipe Codevilla, Antonio Lopez, and Vladlen Koltun. Carla: An open urban driving simulator, 2017. 3 

- [9] Lan Feng, Mohammadhossein Bahari, Kaouther Messaoud Ben Amor, Eloi Zablocki, Matthieu Cord, and Alexan-<sup>´</sup> dre Alahi. Unitraj: A unified framework for scalable vehicle trajectory prediction. In _ECCV_ , 2024. 5 

- [10] Shenyuan Gao, Jiazhi Yang, Li Chen, Kashyap Chitta, Yihang Qiu, Andreas Geiger, Jun Zhang, and Hongyang Li. Vista: A generalizable driving world model with high fidelity and versatile controllability. In _Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024_ , 2024. 1, 2, 3, 5, 7, 8 

- [11] Songwei Ge, Aniruddha Mahapatra, Gaurav Parmar, JunYan Zhu, and Jia-Bin Huang. On the content bias in fr´echet video distance. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 6, 2 

- [12] Francis Glebas. _Directing the story: professional storytelling and storyboarding techniques for live action and animation_ . Routledge, 2012. 1 

- [13] David Ha and J¨urgen Schmidhuber. World models. 2018. 2 

- [14] Yoav HaCohen, Nisan Chiprut, Benny Brazowski, Daniel Shalem, Dudu Moshe, Eitan Richardson, Eran Levin, Guy Shiran, Nir Zabari, Ori Gordon, Poriya Panet, Sapir Weissbuch, Victor Kulikov, Yaki Bitterman, Zeev Melumian, and Ofir Bibi. Ltx-video: Realtime video latent diffusion. _CoRR_ , abs/2501.00103, 2025. 2, 7, 8 

- [15] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination, 2020. 2 

- [16] Mariam Hassan, Sebastian Stapf, Ahmad Rahimi, Pedro M. B. Rezende, Yasaman Haghighi, David Br¨uggemann, Isinsu Katircioglu, Lin Zhang, Xiaoran Chen, Suman Saha, Marco Cannici, Elie Aljalbout, Botao Ye, Xi Wang, Aram Davtyan, Mathieu Salzmann, Davide Scaramuzza, Marc Pollefeys, Paolo Favaro, and Alexandre Alahi. GEM: A generalizable ego-vision multimodal world model for fine- 

9 

grained ego-motion, object dynamics, and scene composition control. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2025, Nashville, TN, USA, June 11-15, 2025_ , pages 22404–22415. Computer Vision Foundation / IEEE, 2025. 1, 2, 3, 5, 7, 8 

- [17] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium. In _Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA_ , pages 6626–6637, 2017. 6, 2 

- [18] Anthony Hu, Lloyd Russell, Hudson Yeo, Zak Murez, George Fedoseev, Alex Kendall, Jamie Shotton, and Gianluca Corrado. Gaia-1: A generative world model for autonomous driving, 2023. 2, 3 

- [19] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan AllenZhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. In _The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ . OpenReview.net, 2022. 2, 4, 7 

- [20] Nikhil Keetha, Norman M¨uller, Johannes Sch¨onberger, Lorenzo Porzi, Yuchen Zhang, Tobias Fischer, Arno Knapitsch, Duncan Zauss, Ethan Weber, Nelson Antunes, Jonathon Luiten, Manuel Lopez-Antequera, Samuel Rota Bul`o, Christian Richardt, Deva Ramanan, Sebastian Scherer, and Peter Kontschieder. MapAnything: Universal feedforward metric 3D reconstruction, 2025. arXiv preprint arXiv:2509.13414. 8, 1 

- [21] Weijie Kong, Qi Tian, Zijian Zhang, Rox Min, Zuozhuo Dai, Jin Zhou, Jiangfeng Xiong, Xin Li, Bo Wu, Jianwei Zhang, Kathrina Wu, Qin Lin, Junkun Yuan, Yanxin Long, Aladdin Wang, Andong Wang, Changlin Li, Duojun Huang, Fang Yang, Hao Tan, Hongmei Wang, Jacob Song, Jiawang Bai, Jianbing Wu, Jinbao Xue, Joey Wang, Kai Wang, Mengyang Liu, Pengyu Li, Shuai Li, Weiyan Wang, Wenqing Yu, Xinchi Deng, Yang Li, Yi Chen, Yutao Cui, Yuanbo Peng, Zhentao Yu, Zhiyu He, Zhiyong Xu, Zixiang Zhou, Zunnan Xu, Yangyu Tao, Qinglin Lu, Songtao Liu, Dax Zhou, Hongfa Wang, Yong Yang, Di Wang, Yuhong Liu, Jie Jiang, and Caesar Zhong. Hunyuanvideo: A systematic framework for large video generative models, 2025. 2 

- [22] Sven Kreiss, Lorenzo Bertoni, and Alexandre Alahi. Openpifpaf: Composite fields for semantic keypoint detection and spatio-temporal association. _IEEE Trans. Intell. Transp. Syst._ , 23(8):13498–13511, 2022. 2, 4, 6, 1 

- [23] Bohan Li, Jiazhe Guo, Hongsi Liu, Yingshuang Zou, Yikang Ding, Xiwu Chen, Hu Zhu, Feiyang Tan, Chi Zhang, Tiancai Wang, Shuchang Zhou, Li Zhang, Xiaojuan Qi, Hao Zhao, Mu Yang, Wenjun Zeng, and Xin Jin. Uniscene: Unified occupancy-centric driving scene generation, 2025. 2 

- [24] Ao Liang, Youquan Liu, Yu Yang, Dongyue Lu, Linfeng Li, Lingdong Kong, Huaici Zhao, and Wei Tsang Ooi. Learning to generate 4d lidar sequences, 2025. 2 

- [25] Jingyun Liang, Yuchen Fan, Kai Zhang, Radu Timofte, Luc Van Gool, and Rakesh Ranjan. Movideo: Motion-aware video generation with diffusion models, 2024. 3 

- [26] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net, 2019. 7 

- [27] Saman Motamed, Laura Culp, Kevin Swersky, Priyank Jaini, and Robert Geirhos. Do generative video models understand physical principles?, 2025. 2 

- [28] NVIDIA, :, Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, Daniel Dworakowski, Jiaojiao Fan, Michele Fenzi, Francesco Ferroni, Sanja Fidler, Dieter Fox, Songwei Ge, Yunhao Ge, Jinwei Gu, Siddharth Gururani, Ethan He, Jiahui Huang, Jacob Huffman, Pooya Jannaty, Jingyi Jin, Seung Wook Kim, Gergely Kl´ar, Grace Lam, Shiyi Lan, Laura Leal-Taixe, Anqi Li, Zhaoshuo Li, Chen-Hsuan Lin, Tsung-Yi Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Alice Luo, Qianli Ma, Hanzi Mao, Kaichun Mo, Arsalan Mousavian, Seungjun Nah, Sriharsha Niverty, David Page, Despoina Paschalidou, Zeeshan Patel, Lindsey Pavao, Morteza Ramezanali, Fitsum Reda, Xiaowei Ren, Vasanth Rao Naik Sabavat, Ed Schmerling, Stella Shi, Bartosz Stefaniak, Shitao Tang, Lyne Tchapmi, Przemek Tredak, WeiCheng Tseng, Jibin Varghese, Hao Wang, Haoxiang Wang, Heng Wang, Ting-Chun Wang, Fangyin Wei, Xinyue Wei, Jay Zhangjie Wu, Jiashu Xu, Wei Yang, Lin Yen-Chen, Xiaohui Zeng, Yu Zeng, Jing Zhang, Qinsheng Zhang, Yuxuan Zhang, Qingqing Zhao, and Artur Zolkowski. Cosmos world foundation model platform for physical ai, 2025. 1, 2, 3, 7, 8 

- [29] NVIDIA, :, Hassan Abu Alhaija, Jose Alvarez, Maciej Bala, Tiffany Cai, Tianshi Cao, Liz Cha, Joshua Chen, Mike Chen, Francesco Ferroni, Sanja Fidler, Dieter Fox, Yunhao Ge, Jinwei Gu, Ali Hassani, Michael Isaev, Pooya Jannaty, Shiyi Lan, Tobias Lasser, Huan Ling, Ming-Yu Liu, Xian Liu, Yifan Lu, Alice Luo, Qianli Ma, Hanzi Mao, Fabio Ramos, Xuanchi Ren, Tianchang Shen, Xinglong Sun, Shitao Tang, Ting-Chun Wang, Jay Wu, Jiashu Xu, Stella Xu, Kevin Xie, Yuchong Ye, Xiaodong Yang, Xiaohui Zeng, and Yu Zeng. Cosmos-transfer1: Conditional world generation with adaptive multimodal control, 2025. 3 

- [30] Yiran Qin, Zhelun Shi, Jiwen Yu, Xijun Wang, Enshen Zhou, Lijun Li, Zhenfei Yin, Xihui Liu, Lu Sheng, Jing Shao, Lei Bai, Wanli Ouyang, and Ruimao Zhang. Worldsimbench: Towards video generation models as world simulators, 2024. 

2 

- [31] Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tianyi Tang, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report, 2025. 1 

- [32] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a 

10 

   - unified text-to-text transformer. _Journal of Machine Learning Research_ , 21(140):1–67, 2020. 5 

- [33] Xuanchi Ren, Yifan Lu, Tianshi Cao, Ruiyuan Gao, Shengyu Huang, Amirmojtaba Sabour, Tianchang Shen, Tobias Pfaff, Jay Zhangjie Wu, Runjian Chen, Seung Wook Kim, Jun Gao, Laura Leal-Taixe, Mike Chen, Sanja Fidler, and Huan Ling. Cosmos-drive-dreams: Scalable synthetic driving data generation with world foundation models, 2025. 2, 3 

- [34] Lloyd Russell, Anthony Hu, Lorenzo Bertoni, George Fedoseev, Jamie Shotton, Elahe Arani, and Gianluca Corrado. Gaia-2: A controllable multi-view generative world model for autonomous driving, 2025. 2, 3 

- [35] Xiaoyu Shi, Zhaoyang Huang, Fu-Yun Wang, Weikang Bian, Dasong Li, Yi Zhang, Manyuan Zhang, Ka Chun Cheung, Simon See, Hongwei Qin, Jifeng Dai, and Hongsheng Li. Motion-i2v: Consistent and controllable image-to-video generation with explicit motion modeling, 2024. 3 

- [36] Pei Sun, Henrik Kretzschmar, Xerxes Dotiwalla, Aurelien Chouard, Vijaysai Patnaik, Paul Tsui, James Guo, Yin Zhou, Yuning Chai, Benjamin Caine, Vijay Vasudevan, Wei Han, Jiquan Ngiam, Hang Zhao, Aleksei Timofeev, Scott Ettinger, Maxim Krivokon, Amy Gao, Aditya Joshi, Yu Zhang, Jonathon Shlens, Zhifeng Chen, and Dragomir Anguelov. Scalability in perception for autonomous driving: Waymo open dataset. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2020. 6, 1 

- [37] Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Rapha¨el Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _CoRR_ , abs/1812.01717, 2018. 6, 2 

- [38] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, Jianyuan Zeng, Jiayu Wang, Jingfeng Zhang, Jingren Zhou, Jinkai Wang, Jixuan Chen, Kai Zhu, Kang Zhao, Keyu Yan, Lianghua Huang, Mengyang Feng, Ningyi Zhang, Pandeng Li, Pingyu Wu, Ruihang Chu, Ruili Feng, Shiwei Zhang, Siyang Sun, Tao Fang, Tianxing Wang, Tianyi Gui, Tingyu Weng, Tong Shen, Wei Lin, Wei Wang, Wei Wang, Wenmeng Zhou, Wente Wang, Wenting Shen, Wenyuan Yu, Xianzhong Shi, Xiaoming Huang, Xin Xu, Yan Kou, Yangyu Lv, Yifei Li, Yijing Liu, Yiming Wang, Yingya Zhang, Yitong Huang, Yong Li, You Wu, Yu Liu, Yulin Pan, Yun Zheng, Yuntao Hong, Yupeng Shi, Yutong Feng, Zeyinzi Jiang, Zhen Han, Zhi-Fan Wu, and Ziyu Liu. Wan: Open and advanced large-scale video generative models, 2025. 2 

Luo, Jun Zhang, Andreas Geiger, Yu Qiao, and Hongyang Li. Generalized predictive model for autonomous driving. In _IEEE/CVF Conference on Computer Vision and Pattern Recognition, CVPR 2024, Seattle, WA, USA, June 16-22, 2024_ , pages 14662–14672. IEEE, 2024. 2, 3, 6, 8 

   - [42] Jiazhi Yang, Kashyap Chitta, Shenyuan Gao, Long Chen, Yuqian Shao, Xiaosong Jia, Hongyang Li, Andreas Geiger, Xiangyu Yue, and Li Chen. Resim: Reliable world simulation for autonomous driving, 2025. 2, 3 

   - [43] Zhendong Yang, Ailing Zeng, Chun Yuan, and Yu Li. Effective whole-body pose estimation with two-stages distillation. In _IEEE/CVF International Conference on Computer Vision, ICCV 2023 - Workshops, Paris, France, October 2-6, 2023_ , pages 4212–4222. IEEE, 2023. 2, 4, 6 

   - [44] Zhuoran Yang, Xi Guo, Chenjing Ding, Chiyu Wang, Wei Wu, and Yanyong Zhang. Instadrive: Instance-aware driving world models for realistic and consistent video generation. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 25410–25420, 2025. 2, 3 

   - [45] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, Da Yin, Yuxuan Zhang, Weihan Wang, Yean Cheng, Bin Xu, Xiaotao Gu, Yuxiao Dong, and Jie Tang. Cogvideox: Text-to-video diffusion models with an expert transformer, 2025. 2, 3 

   - [46] Guy Yariv, Yuval Kirstain, Amit Zohar, Shelly Sheynin, Yaniv Taigman, Yossi Adi, Sagie Benaim, and Adam Polyak. Through-the-mask: Mask-based motion trajectories for image-to-video generation, 2025. 3 

   - [47] Chenyu Zhang, Daniil Cherniavskii, Antonios Tragoudaras, Antonios Vozikis, Thijmen Nijdam, Derck W. E. Prinzhorn, Mark Bodracska, Nicu Sebe, Andrii Zadaianchuk, and Efstratios Gavves. Morpheus: Benchmarking physical reasoning of video generative models with real physical experiments, 2025. 2 

   - [48] Kaiwen Zhang, Zhenyu Tang, Xiaotao Hu, Xingang Pan, Xiaoyang Guo, Yuan Liu, Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, Xun Cao, and Wei Yin. Epona: Autoregressive diffusion world model for autonomous driving, 2025. 2, 3 

   - [49] Sicheng Zuo, Wenzhao Zheng, Yuanhui Huang, Jie Zhou, and Jiwen Lu. Gaussianworld: Gaussian world model for streaming 3d occupancy prediction, 2024. 2 

- [39] Zeqing Wang, Xinyu Wei, Bairui Li, Zhen Guo, Jinrui Zhang, Hongyang Wei, Keze Wang, and Lei Zhang. Videoverse: How far is your t2v generator from a world model?, 2025. 2 

- [40] Yihong Xu, Eloi<sup>´</sup> Zablocki, Alexandre Boulch, Gilles Puy, Micka¨el Chen, Florent Bartoccioni, Nermin Samet, Oriane Sim´eoni, Spyros Gidaris, Tuan-Hung Vu, Andrei Bursuc, Eduardo Valle, Renaud Marlet, and Matthieu Cord. Valeo4cast: A modular approach to end-to-end forecasting. In _ECCV Workshop_ , 2024. 5 

- [41] Jiazhi Yang, Shenyuan Gao, Yihang Qiu, Li Chen, Tianyu Li, Bo Dai, Kashyap Chitta, Penghao Wu, Jia Zeng, Ping 

11 

# **MAD: Motion Appearance Decoupling for efficient Driving World Models** 

# Supplementary Material 


Figure 7. Inference Speed vs. Perceptual Quality. We report the inference time measured on a single GH200 GPU. Performance is quantified using the ELO score computed from our human preference study. **Our MAD-LTX models achieve up to 3.6× faster inference than competitive models of comparable size and performance** 

## **5. Inference Speed** 

We report the inference latency for 5 seconds video generation in figure 7 on a single NVIDIA GH200 GPU. We exclude functionalities that require additional model loading (making the inference slower) like upsampling or model offloading for Cosmos baselines. All tests use the default resolution and generated frame count specified by each respective model, for models that generate short segments, multiple rollouts are used to reach the 5-second duration used in our evaluation. 

Direct measurements for Cosmos-Predict2 on the GH200 were not available. We report its A100 inference time as 41 minutes (14B) and 11 minutes (2B). The A100 inference speed is rescaled to the GH200 for Predict2 using a conversion ratio computed from other baselines. **Our MAD-LTX models achieve up to 3.6× faster inference than competitive models of comparable size and performance** 

## **6. Additional Experiments** 

### **6.1. Evaluation of Control Capabilities** 

We evaluate the fidelity of our model’s three primary control axes: **ego trajectory control, object control, and textual control** . Experiments are conducted on a subset of N=800 video clips (5 seconds each) from the Waymo Open Dataset. As shown in Tab. 3, we adopt the evaluation protocol from [16] and use our unconditional models (‘MADLTX-uncond’) as a reference baseline to demonstrate the effectiveness of our conditioning signals. The specific eval- 

Table 3. Evaluation of control fidelity. We evaluate each control type over 800 generated samples from Waymo Open Dataset [36]. ‘MAD-LTX-uncond’ (our models without any control inputs) serves as reference baselines to measure the effectiveness of the conditioning. **MAD-LTX effectively supports all three distinct control modalities** 

|Model|Ego_↓_|Obj_↑_|Tex<br>**Action**|t_↑_<br>**Object**|
|---|---|---|---|---|
|MAD-LTX-2B-uncond|5.2|0.40|38.8%|42.1%|
|MAD-LTX-2B (ours)|**1.4**|**0.51**|**40.8%**|**45.6%**|
|MAD-LTX-13B-uncond|3.4|0.45|39.2%|44.6%|
|MAD-LTX-13B (ours)|**1.5**|**0.55**|**43.9%**|**49.1%**|


uation metrics for each modality are defined as follows: 

**Ego-Motion Control.** We condition the generation on Ground Truth (GT) ego-camera poses from the Waymo Open Dataset. To measure fidelity, we extract the realized ego-trajectory from both the GT video and the generated video using MapAnything [20]. We report the **Average Displacement Error (ADE)** between these two extracted trajectories as the primary metric. 

**Object Control.** We utilize OpenPifPaf [22] to detect and track a single target object in the GT video. We condition the generation on the single object extracted location from the GT video. For evaluation, we run OpenPifPaf [22] on the generated video to locate the corresponding object. We report the **Intersection over Union (IoU)** between the conditioned GT box and the detected box in the generated frame. If the target object fails to appear in the generated video, an IoU of 0 is assigned. 

**Text Control.** We employ an automated Visual Question Answering (VQA) pipeline to assess text adherence across two distinct categories: **Action** (dynamics/maneuvers) and **Object** (entity presence). We use **Qwen2.5** [31] to extract semantic elements from the input prompt and reformulate them into a binary verification question tailored to the specific category—for example, _Is the ego car turning left?”_ for textual action control, and _Is a cyclist entering the video?”_ for textual object control. We then feed the generated video and this question into the Vision-Language Model **Qwen2.5-VL** [2] to obtain a Yes” or No” prediction. We report the **Success Rate** (percentage of “Yes” answers) for each category. 

**Control Results** As detailed in Table 3, we observe consistent quantitative improvements across all metrics and model 

1 

sizes when comparing the conditioned MAD-LTX models against their unconditional counterparts. The performance gap is most significant in **Ego-Motion Control amd Object control** . This is expected: while the unconditional model typically forecasts a _plausible_ future object/ego trajectory (representing one valid mode of the motion distribution), it is penalized for deviating from the specific Ground Truth realization. The conditioned model, however, effectively utilizes the control signal to lock onto the correct mode. For **Textual Control** , the improvements are consistently positive but less significant. We attribute this to the unconditional model being trained on static captions (describing the first frame), which yields a high starting score, while VLM noise limits the measured gain. These results confirm that—consistent across both parameter scales— **MAD-LTX effectively supports all three distinct control modalities.** 

### **6.2. Standard video quality metrics (FID/FVD)** 

We report in table 4 the Fr´echet Inception Distance [17] (FID) and Fr´echet Video Distance [37] (FVD) for the Base LTX [14] model, the standard fine-tuned baseline (Finetuned LTX), and our proposed MAD-LTX across both 2B and 13B parameter scales. 

All metrics were computed on the OpenDV [41] test set using N=5,000 generated samples per method. As shown in Table 1, while we report these metrics for completeness, we observe—consistent with recent literature[11] —that **FID and FVD scores do not strictly correlate with human perceptual preference in this domain.** 

Table 4. **Standard video quality metric on the OpenDV test set.** We report FID and FVD metrics computed using _N_ = 5 _,_ 000 samples. Consistent with prior work[11], **we observe that these distribution based metrics do not necessarily correlate with human perceptual preference.** 

|**Model Size**|**Method**|**FID**_↓_|**FVD**_↓_|
|---|---|---|---|
||Base LTX|4.06|**64.40**|
|2B|Fine-tuned LTX|**2.66**|67.17|
||MAD-LTX (Ours)|3.72|92.79|
||Base LTX|2.21|**56.15**|
|13B|Fine-tuned LTX|**1.94**|69.56|
||MAD-LTX (Ours)|2.39|59.61|


Figure 8. **User Study Interface:** We employ a side-byside pairwise comparison protocol to evaluate generation performance. Participants are asked to rate their preference between two anonymized videos across three specific criteria: General Quality, Motion Quality and Realistic Dynamics, and Visual Quality. For each criterion, annotators select from a 5-point scale ranging from ”Strong Preference” or ”Preference” for a specific model, to ”No Preference.” 

To ensure high-quality feedback, the participant pool consisted exclusively of domain experts—computer vision researchers specializing in autonomous driving. 

For each baseline, we generated _N_ = 100 video samples (5 seconds duration). In every comparison, annotators were presented with two anonymized videos and asked to rate their preference (Strongly Prefer, Prefer, or No Preference) based on the following specific prompts: 

- **General Quality:** _“Overall which video do you prefer? In other words which video is harder to distinguish from real video?”_ (Results reported in Figure 5 of the main manuscript). 

- **Motion Quality and Realistic Dynamics:** _“Which video has more realistic, fluid and coherent motion, and is physically and socially plausible? Stopping suddenly without reason, collisions between objects, or cars driving in wrong direction are example of poor motion quality.”_ 

- **Visual Quality:** _“Which video has better clarity, fewer artifacts, and more pleasing visual? Blurry object, change of color or shape over time, and visual distortions are example of poor visual quality.”_ 

### **7.2. Additional results** 

## **7. Human Evaluation** 

### **7.1. Protocol** 

We conducted a blinded pairwise comparison study hosted on a custom Hugging Face interface. The specific layout of the pairwise comparison interface is illustrated in fugure 8. 

In this section, we report the detailed results for **Motion Quality** and **Visual Quality** . 

The detailed pairwise win rates for Motion Quality and Visual Quality are presented in figures 9, 10, 11 and 12. We observe that user preferences on these two axes strongly correlate with the General Quality results reported in the 

2 


Figure 9. **Motion Realism Preference (MAD-LTX 2B).** Human preference evaluation specific on motion plausibility (e.g., fluidity, absence of collisions/sudden stops). ‘*’ denotes proprietary mod- els which use private datasets and significant computational resource **MAD-LTX-2B outperforms all open-source models, ranking second only to the proprietary Cosmos-Predict2.** 


Figure 10. **Visual Quality Preference (MAD-LTX 2B).** Human preference evaluation specific on visual quality (e.g., temporal consistency, distortions). ‘*’ denotes proprietary models which use private datasets and significant computational resources. **MAD-LTX-2B outperforms all open-source models, ranking second only to the proprietary Cosmos-Predict2.** 


Figure 11. **Motion Realism Preference (MAD-LTX 13B).** Human preference evaluation specific on motion plausibility (e.g., fluidity, absence of collisions/sudden stops). ‘*’ denotes proprietary models which use private datasets and significant computational resources. **MAD-LTX-13B outperforms all open-source models, ranking second only to the proprietary CosmosPredict2.** 

main manuscript. Consistent across both the 2B and 13B parameter scales, **MAD-LTX outperforms all evaluated open-source baselines in terms of both motion realism and visual fidelity.** In alignment with the global preference trends, the proprietary Cosmos-Predict2 is the only model that retains a higher preference rate than our method on both criteria. 


Figure 12. **Visual Quality Preference (MAD-LTX 13B).** Human preference evaluation specific on visual quality (e.g., temporal consistency, distortions). ‘*’ denotes proprietary models which use private datasets and significant computational resources. **MAD-LTX-13B outperforms all open-source models, ranking second only to the proprietary Cosmos-Predict2.** 

## **8. Additional Hyperparameters** 

We share a comprehensive list of all the hyper parameters we used for training our Motion Forecaster and our Motion Synthesizer in Tab. 5. All codes with the corresponding config files will be released for reproducibility. 

Table 5. LTX Training Hyperparameters 

|**Category**|**Parameter**|**Value**|**Description**|
|---|---|---|---|
|**Model Strategy**|Model Source|LTX<br>~~2~~B<br>~~0~~.9.6<br>~~D~~EVandLTX<br>~~1~~3B<br>~~0~~97<br>~~D~~EV|Base 2B parameter model and 13B param-<br>eter model.|
||Training Mode|lora|Low-Rank Adaptation fine-tuning.|
||Precision|bf16|Brain Floating Point 16 mixed precision.|
|**LoRA Config**|Rank (_r_)|512|High rank for high expressivity.|
||Alpha (_α_)|512|Scaling factor (1:1 ratio with rank).|
||Targets|q, k, v, out, ff|Applies to Attention and Feed-Forward<br>blocks.|
|**Optimization**|Learning Rate|2_×_10<sup>_−_4</sup>|Step size for the optimizer.|
||Optimizer|adamw|Standard AdamW optimizer.|
||Batch Size|32|Small batch size due to VRAM constraints.|
||||But used 32 GPUs, so an effective batch<br>size of 32.|
||Scheduler|linear|Linear learning rate decay.|


## **9. Limitations and Future Work** 

While our intermediate motion representation has proved to be useful, it currently omits contextual driving signalization for precise prediction, such as traffic light states or traffic signs. Furthermore, we observed that while the overall pseudo-labeling strategy was successful, the generated lane keypoints are inherently noisy, hindering accurate road layout modeling. An ablation showed that replacing these with road segmentation masks could offer a more robust structural representation. For future work, we will focus on incorporating these driving elements and exploring segmentation-based road representations. 

Beyond the driving domain, the core MAD principle could be extended to other areas for which pose is a natural representation, such as human-centric video generation, an area where industry currently focuses on extensive training over large datasets, and to ego-view object manipulation for robotics, which directly relates to the world model problematics. 

3 

