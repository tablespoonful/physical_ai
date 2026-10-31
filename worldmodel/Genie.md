---
title: "Genie: Generative Interactive Environments"
date: "2024-02-23"
authors: "Jake Bruce; Michael Dennis; Ashley Edwards; Jack Parker-Holder; Yuge Shi; Edward Hughes"
venue: "ICML"
url: https://arxiv.org/abs/2402.15391
pdf: https://arxiv.org/pdf/2402.15391
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2402.15391)** / [論文ページ](https://arxiv.org/abs/2402.15391)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。



# **Genie: Generative Interactive Environments** 

**Jake Bruce**<sup>* 1</sup> **Michael Dennis**<sup>* 1</sup> **Ashley Edwards**<sup>* 1</sup> **Jack Parker-Holder**<sup>* 1</sup> **Yuge (Jimmy) Shi**<sup>* 1</sup> **Edward Hughes**<sup>1</sup> **Matthew Lai**<sup>* 1</sup> **Aditi Mavalankar**<sup>1</sup> **Richie Steigerwald**<sup>1</sup> **Chris Apps**<sup>1</sup> **Yusuf Aytar**<sup>1</sup> **Sarah Bechtle**<sup>1</sup> **Feryal Behbahani**<sup>1</sup> **Stephanie Chan**<sup>1</sup> **Nicolas Heess**<sup>1</sup> **Lucy Gonzalez**<sup>1</sup> **Simon Osindero**<sup>1</sup> **Sherjil Ozair**<sup>1</sup> **Scott Reed**<sup>1</sup> **Jingwei Zhang**<sup>1</sup> **Konrad Zolna**<sup>1</sup> **Jeff Clune**<sup>1 2</sup> **Nando de Freitas**<sup>1</sup> **Satinder Singh**<sup>1</sup> **Tim Rockt¨aschel**<sup>* 1</sup> 

## **Abstract** 

We introduce Genie, the first _generative interactive environment_ trained in an unsupervised manner from unlabelled Internet videos. The model can be prompted to generate an endless variety of action-controllable virtual worlds described through text, synthetic images, photographs, and even sketches. At 11B parameters, Genie can be considered a _foundation world model_ . It is comprised of a spatiotemporal video tokenizer, an autoregressive dynamics model, and a simple and scalable latent action model. Genie enables users to act in the generated environments on a frame-by-frame basis _despite training without any ground-truth action labels_ or other domainspecific requirements typically found in the world model literature. Further the resulting learned latent action space facilitates training agents to imitate behaviors from unseen videos, opening the path for training generalist agents of the future. 

## **1. Introduction** 

The last few years have seen an emergence of _generative AI_ , with models capable of generating novel and creative content. Driven by breakthroughs in architectures such as transformers (Vaswani et al., 2017), advances in hardware, and a recent focus on scaling models and datasets, we can now generate coherent, conversational language (Brown et al., 2020; Radford et al., 2018; 2019), as well as crisp and aesthetically pleasing images from a text prompt (Ramesh et al., 2021; 2022; Rombach et al., 2022; Saharia et al., 

> *Equal contribution 1Google DeepMind 2University of British Columbia. Correspondence to: Project Leads: Ashley Edwards _<_ edwardsashley@google.com _>_ , Jack Parker-Holder _<_ jparkerholder@google.com _>_ , Tech Lead: Jake Bruce _<_ jacobbruce@google.com _>_ . 

_Proceedings of the 41_<sup>_st_</sup> _International Conference on Machine Learning_ , Vienna, Austria. PMLR 235, 2024. Copyright 2024 by the author(s). 


Figure 1: **Diverse trajectories** : Genie is a generative model that can be used as an interactive environment. The model can be prompted in various ways, either with a generated image (top) or a hand-drawn sketch (bottom). At each time step, the model takes a user-provided latent action to generate the next frame, producing trajectories with interesting and diverse character actions. 

2022). Early signs indicate video generation will be yet another frontier, with recent results suggesting that such models may also benefit from scale (Blattmann et al., 2023a; Esser et al., 2023; Ho et al., 2022a; Hong et al., 2023). Still, there remains a gulf between the level of interactions and engagement of video generative models and language tools such as ChatGPT, let alone more immersive experiences. 

What if, given a large corpus of videos from the Internet, we could not only train models capable of generating novel images or videos, but entire interactive experiences? In this work we propose _generative interactive environments_ , a new paradigm for generative AI whereby interactive environments can be generated from a single text or image prompt. Our approach, Genie, is trained from a large dataset of over 200,000 hours of publicly available Internet gaming videos and, despite training _without action or text annotations_ , is controllable on a frame-by-frame basis via a learned 

1 

**Generative Interactive Environments** 


Figure 2: **A whole new world** : Genie is capable of converting a variety of different prompts into interactive, playable environments that can be easily created, stepped into, and explored. This is made possible via a latent action interface, learned fully unsupervised from Internet videos. On the right we see a few generated steps for taking two latent actions. See more examples on our website. 

latent action space (see Table 1 for a comparison to other approaches). At 11B parameters, Genie exhibits the properties typically seen in foundation models—it can take an unseen image as a prompt making it possible to create and play entirely imagined virtual worlds (Figures 1 and 2). 

Genie builds upon ideas from state-of-the-art video generation models (Gupta et al., 2023; Villegas et al., 2023), with a core design choice being spatiotemporal (ST) transformers (Xu et al., 2020) which are used in all of our model components. Genie utilizes a novel video tokenizer, and extracts latent actions via a causal action model. Both the video tokens and latent actions are passed to the dynamics model, which autoregressively predicts the next frame using MaskGIT (Chang et al., 2022). We provide a rigorous scaling analysis of our architecture with respect to both batch size and model size, which we vary from 40M to 2.7B parameters. The results show that our architecture scales gracefully with additional computational resources, leading to our final 11B parameter model. We train Genie on a filtered set of 30,000 hours of Internet gameplay videos from hundreds of 2D platformer games, producing a foundation world model for this setting. 

To demonstrate the generality of our approach, we also train a separate model on action-free robot videos from the RT1 dataset (Brohan et al., 2023), learning a generative environment with consistent latent actions. Finally, we show that latent actions learned from Internet videos can be used for inferring policies from unseen action-free videos of simulated reinforcement learning (RL) environments, indicating that Genie may hold the key to unlocking unlimited data for training the next generation of generalist agents (Bauer et al., 2023; Clune, 2019; Open Ended Learning Team et al., 2021; Reed et al., 2022). 

Table 1: **A new class of generative model** : Genie is a novel video and world model that is controllable on a frame-by-frame basis, which requires **only video data** at train time. 

|Model Class|Training Data|Controllability|
|---|---|---|
|World Models|Video + Actions|Frame-level|
|Video Models|Video + Text|Video-level|
|Genie|Video|Frame-level|


## **2. Methodology** 

Genie is a generative interactive environment trained from video-only data. In this section we begin with preliminaries before explaining the main components of our model. 

Several components in the Genie architecture are based on the Vision Transformer (ViT) (Dosovitskiy et al., 2021; Vaswani et al., 2017). Notably, the quadratic memory cost of transformers poses challenges for videos, which can contain up to _O_ (10<sup>4</sup> ) tokens. We thus adopt a memory efficient ST-transformer architecture (inspired by Xu et al. (2020), see Figure 4) across all model components, balancing model capacity with computational constraints. 

Unlike a traditional transformer where every token attends to all others, an ST-transformer contains _L_ spatiotemporal blocks with interleaved spatial and temporal attention layers, followed by a feed-forward layer (FFW) as standard attention blocks. The self-attention in the spatial layer attends over the 1 _× H × W_ tokens within each time step, and in the temporal layer attends over _T ×_ 1 _×_ 1 tokens across the _T_ time steps. Similar to sequence transformers, the temporal layer assumes a causal structure with a causal mask. Crucially, the dominating factor of computation complexity (i.e. the spatial attention layer) in our architecture scales linearly with the number of frames rather than quadratically, making 

2 

**Generative Interactive Environments** 


Figure 3: **Genie model training** : Genie takes in _T_ frames of video as input, tokenizes them into discrete tokens **_z_** via the video tokenizer, and infers the latent actions between each frame **_a_** with the latent action model. Both are then passed to the dynamics model to generate predictions for the next frames in an iterative manner. 

it much more efficient for video generation with consistent dynamics over extended interactions. Further, note that in the ST block, we include only one FFW after both spatial and temporal components, omitting the post-spatial FFW to allow for scaling up other components of the model, which we observe to improve results significantly. 


Figure 4: **ST-transformer architecture** . The architecture is composed of _L_ spatiotemporal blocks, each containing a spatial layer, temporal layer and feed-forward layer. Each color represents a single self-attention map, with the spatial layer attending over the _H × W_ tokens from within a single time step, and temporal the same token from across the _T_ time steps. 

### **2.1. Model Components** 

As shown in Figure 3, our model contains three key components: 1) a **_latent action model_** that infers the latent action **_a_** between each pair of frames and 2) a **_video tokenizer_** that converts raw video frames into discrete tokens **_z_** and 3) a **_dynamics model_** that, given a latent action and past frame tokens, predicts the next frame of the video. The model is trained in two phases following a standard autoregressive video generation pipeline: we train the video tokenizer first, which is used for the dynamics model. We then co-train the latent action model (directly from pixels) and the dynamics model (on video tokens). 

**Latent Action Model (LAM)** To achieve controllable video generation, we condition each future frame prediction on the action taken at the previous frame. However, such action labels are rarely available in videos from the Internet and 

action annotation can be costly to obtain. Instead, we learn _latent actions_ in a fully unsupervised manner (see Figure 5). 


Figure 5: **Latent action model** : learns actions _at_ unsupervised from unlabelled video frames. 

First, an encoder takes as inputs all previous frames **_x_** 1: _t_ = ( _x_ 1 _, · · · xt_ ) as well as the next frame _xt_ +1, and outputs a corresponding set of continuous latent actions **_a_** ˜1: _t_ = (˜ _a_ 1 _, · · ·_ ˜ _at_ ). A decoder then takes all previous frames and latent actions as input and predicts the next frame _x_ ˆ _t_ +1. 

To train the model, we leverage a VQ-VAE-based objective van den Oord et al. (2017), which enables us to limit the number of predicted actions to a small discrete set of codes. We limit the vocabulary size _|A|_ of the VQ codebook, i.e. the maximum number of possible latent actions, to a small value to permit human playability and further enforce controllability (we use _|A|_ = 8 in our experiments). As the decoder only has access to the history and latent action, ˜ _at_ should encode the most meaningful changes between the past and the future for the decoder to successfully reconstruct the future frame. 

We found it to be beneficial to use a lightweight decoder to learn the latent actions rather than directly using the dynamics model. Thus the LAM decoder exists only to give the LAM training signal and is not subsequently used at inference time. Indeed, apart from the VQ codebook, the entire LAM is discarded at inference time and replaced with actions from the user. 

We utilize our ST-transformer architecture for the latent action model. The causal mask in the temporal layer allows us to take the entire video **_x_** 1: _T_ as input and generate all latent actions between each frame **_a_** ˜1: _T −_ 1. 

3 

**Generative Interactive Environments** 

**Video Tokenizer** Following prior work (Gupta et al., 2023; Villegas et al., 2023; Yan et al., 2023), we compress videos into discrete tokens to reduce dimensionality and enable higher quality video generation (see Figure 6). We again make use of VQ-VAE, which takes in _T_ frames of video **_x_** 1: _T_ = ( _x_ 1 _, x_ 2 _, · · · , xT_ ) _∈_ R<sup>_T ×H×W ×C_</sup> as input, generating discrete representations for each frame **_z_** 1: _T_ = ( _z_ 1 _, z_ 2 _, · · · , zT_ ) _∈_ I<sup>_T ×D_</sup> , where _D_ is the size of the discrete latent space. The tokenizer is trained using a standard VQ-VQAE objective over the entire video sequence. 


Figure 6: **Video tokenizer** : a VQ-VAE with ST-transformer. 

Unlike prior works that focus on spatial-only compression in the tokenization phase (Gupta et al., 2023; Hong et al., 2022; Wu et al., 2022), we utilize the ST-transformer in both the encoder and decoder to incorporate temporal dynamics in the encodings, which improves the video generation quality. By the causal nature of the ST-transformer, each discrete encoding _zt_ contains information from all previously seen frames of the video **_x_** 1: _t_ . Phenaki (Villegas et al., 2023) also uses a temporal-aware tokenizer, C-ViViT, but this architecture is compute intensive, as the cost grows quadratically with the number of frames—in comparison, our ST-transformer based tokenizer (ST-ViViT) is much more compute efficient with the dominating factor in its cost increasing linearly with the number of frames. 


Figure 7: **Dynamics model** : takes in video tokens and action embeddings, and predicts future masked video tokens. 

**Dynamics Model** The dynamics model is a decoder-only MaskGIT (Chang et al., 2022) transformer (Figure 7). At each time step _t ∈_ [1 _, T_ ], it takes in the tokenized video **_z_** 1: _t−_ 1 and stopgrad latent actions **_a_** ˜1: _t−_ 1 and predicts the next frame tokens _z_ ˆ _t_ . We again utilize an ST-transformer, whose causal structure enables us to use tokens from all ( _T −_ 1) frames **_z_** 1: _T −_ 1 and latent actions **_a_** ˜1: _T −_ 1 as input, and generate predictions for all next frames **_z_** ˆ2: _T_ . The model is trained with a cross-entropy loss between the predicted tokens **_z_** ˆ2: _T_ and ground-truth tokens **_z_** 2: _T_ . At train time we randomly mask the input tokens **_z_** 2: _T −_ 1 according to a Bernoulli distribution masking rate sampled uniformly between 0 _._ 5 and 1. Note that a common practice for training 

world-models, including transformer-based models, is to concatenate the action at time _t_ to the corresponding frame (Micheli et al., 2023; Robine et al., 2023). However, we found that treating the latent actions as _additive embeddings_ for both the latent action and dynamics models helped to improve the controllability of the generations. 

### **2.2. Inference: Action-Controllable Video Generation** 


Figure 8: **Genie Inference** : the prompt frame is tokenized, then combined with the latent action for the corresponding step taken from the user, and passed to the dynamics model for iterative generation. The predicted frame tokens are then decoded back to image space via the tokenizer’s decoder. 

We now describe how to use Genie for action-controllable video generation at inference time (see Figure 8). A player first prompts the model with an image _x_ 1 that serves as the initial frame<sup>1</sup> . The image is tokenized using the video encoder, yielding _z_ 1. The player then specifies a discrete latent action _a_ 1 to take by choosing any integer value within [0 _, |A|_ ). Note that when first interacting with the model, it is unclear how each latent action will impact the next frame generation. However, we found that the meaning of each action remained consistent across different inputs. Hence, interpreting the mapping of latent actions is akin to learning the buttons on a new controller. The dynamics model takes the frame tokens _z_ 1 and corresponding latent action _a_ ˜1, which is obtained by indexing into the VQ codebook with the discrete input _a_ 1, to predict the next frame tokens _z_ 2. This process is repeated to generate the rest of the sequence **_z_** ˆ2: _T_ in an autoregressive manner as actions continue to be passed to the model, while tokens are decoded into video frames **_x_** ˆ2: _T_ with the tokenizer’s decoder. Note that we can re-generate ground truth videos from the dataset by passing the model the starting frame and inferred actions from the video, while also generating completely new videos (or trajectories) by changing the actions. 

## **3. Experimental Results** 

**Datasets** We train Genie on a large-scale dataset collected from publicly available Internet videos of 2D Platformer games (referred to from here on as “Platformers”). We construct the Platformers dataset by filtering publicly available videos for keywords relating to platformers, yielding 55M 16s video clips at 10FPS, with 160x90 resolution. The final 

1The model can be conditioned on a varying number of prompt frames. Here we start from one image as an example. 

4 

**Generative Interactive Environments** 


Figure 9: **Scaling results** . **Left** : Training curves for different model sizes, **Middle** : Final training loss for each model size, averaged over the last 300 updates, **Right** : Final training loss for a 2.3B model with different batch sizes. 

dataset contains 6.8M 16s video clips (30k hours), within an order of magnitude of other popular Internet video datasets (Bain et al., 2021; Wang et al., 2023). More details can be found in Appendix B.1. Unless otherwise specified, results are with a 11B-parameter model trained on this dataset. 

To verify the generality of our method, we also consider the robotics datasets used to train RT1 (Brohan et al., 2023), combining their dataset of _∼_ 130 _k_ robot demonstrations with a separate dataset of simulation data and the 209k episodes of real robot data from prior work (Kalashnikov et al., 2018). Note that we do not use actions from any of these datasets, and simply treat them as videos. For simplicity, from here on we refer to this dataset as “Robotics”. 

effective given the trade-off between reconstruction quality of the tokenizer and downstream performance of video prediction. The latent action model has 300M parameters, uses a patch size of 16 and a codebook with embedding size 32 and 8 unique codes (latent actions). For all modelling components we use a sequence length of 16 frames with an FPS of 10. Further, we employ bfloat16 and QK norm for training our dynamics model, which has been shown to stabilize training at large scale (Dehghani et al., 2023; Henry et al., 2020). At inference time, we perform 25 MaskGIT steps for the sampling of each frame with a temperature of 2 using random sampling. See Appendix C for more details. 

### **3.1. Scaling Results** 

**Metrics** We examine the video generation performance of Genie via two factors, namely **_video fidelity_** , i.e. the quality of video generation, and **_controllability_** , i.e. how much impact the latent actions have in video generation. For video fidelity we use the Frechet Video Distance (FVD), a videolevel metric, which has been shown to have a high level of alignment to human evaluation on video quality (Unterthiner et al., 2019). For controllability, we devise a metric based on peak signal-to-noise ratio (PSNR) which we call ∆ _t_ PSNR, that measures how much the video generations differ when conditioned on latent actions inferred from ground-truth ( _x_ ˆ _t_ ) vs. sampled from a random distribution ( _x_ ˆ<sup>_′_</sup> _t_<sup>):</sup> 

### ∆ _t_ PSNR = PSNR( _xt,_ ˆ _xt_ ) _−_ PSNR( _xt,_ ˆ _x_<sup>_′_</sup> _t_<sup>)</sup><sup>_,_</sup> 

where _xt_ denotes the ground-truth frame at time _t_ , _x_ ˆ _t_ denotes the frame from latent actions **_a_** ˜1: _t_ inferred from ground-truth frames, and _x_ ˆ<sup>_′_</sup> _t_<sup>the same frame generated from</sup> a sequence of latent actions randomly sampled from a categorical distribution. As such, the greater ∆ _t_ PSNR is, the more the video generated from random latent actions differs from ground-truth, which indicates a higher level of controllability from the latent actions. For all experiments we report ∆ _t_ PSNR with _t_ = 4. 

**Training Details** Our video tokenizer uses 200M parameters, a patch size of 4 and a codebook with embedding size 32 and 1024 unique codes, which we found to be the most 

In this section, we investigate the scaling behavior of our model. To this end, we conduct studies that explore the impact of both model size and batch size. See Appendix D for more details on architecture and compute usage. 

**Scaling Model Size** Given a fixed video tokenizer and action model architecture, we train a series of dynamics models ranging from 40M to 2.7B parameters. Figure 9 shows our architecture scales gracefully with model parameters, with each increase in size corresponding to a consistent decrease in the final training loss. This is a strong indication that our approach benefits from scaling, which we exploit with our main Genie model. 

**Scaling Batch Size** We also investigate the effect of scaling the batch size, considering a 2.3B model with batch sizes of 128, 256, and 448, equating to 1.9M, 3.8M and 6.6M tokens. As shown in Figure 9, increasing the batch size leads to a similarly favorable gain in terms of model performance. 

**Genie Model** It is clear that increasing both model size and batch size helps improve model performance. As a result, for our final model, we train a 10.1B dynamics model with a batch size of 512, for a total of 125k steps, using 256 TPUv5p. When combined with the tokenizer and action model this brings the total to 10.7B parameters, trained on 942B tokens, which we refer to as the Genie model. 

5 

**Generative Interactive Environments** 


Figure 10: **Playing from Image Prompts** : We can prompt Genie with images generated by text-to-image models, hand-drawn sketches or real-world photos. In each case we show the prompt frame and a second frame after taking one of the latent actions four consecutive times. In each case we see clear character movement, despite some of the images being visually distinct from the dataset. 

### **3.2. Qualitative Results** 

We now present qualitative results from the Genie model. We showcase a 11B parameter model trained on the Platformers dataset and a smaller 1.3B model trained on the Robotics dataset. Our model generates high-quality, controllable videos across diverse domains. Notably, we qualitatively evaluate our Platformers-trained model using _only out-of-distribution (OOD) image prompts_ , including those generated from text-to-image models, hand-drawn sketches, and even real-world photos. The ability to generalize to such significantly OOD inputs underscores the robustness of our approach and the value of training on large-scale data, which would not have been feasible with real actions as input. 

**Platformers-trained model** Figure 10 showcases examples of our model’s generations prompted from OOD images, including (top row) images generated from Imagen2 (Ho et al., 2022a; van den Oord et al.), (second row) hand-drawn sketches and (bottom row) real-world photos. Genie enables bringing these imagined worlds to life, as we see gamelike behaviour when interacting with each example. We showcase more generations in Appendix A, additionally highlighting the consistency of the latent actions. 

Another emergent capability of our model is its ability to understand 3D scenes and emulate parallax, which is commonly seen in platformer games. In Figure 11 we show an image generated by Imagen2, where taking a latent action 


Figure 11: **Emulating parallax** , a common feature in platformer games. From this initial frame generated by a text-to-image model, the **foreground** moves more than the **near** and **far** middle ground, while the **background** moves only slightly. 

moves the foreground at a different rate to the background (as indicated by the length of different colored arrows). 

**Robotics-trained model** We trained a 2.5B-parameter model on the Robotics dataset using the same hyperparameters found to be best on Platformers, achieving an FVD of 82.7 on the test split. As shown in Figure 17, this model successfully learns distinct and consistent actions from video data, requiring neither text nor action labels (as in e.g. Yang et al. (2023)). Notably, our model learns not only the controls of the robotic arm but also the interactions and deformations of various objects (Figure 12). We believe this shows our approach presents a path to using larger video datasets from the Internet to create a foundational world model for robotics, with low-level controllable simulation that could be used for a variety of applications. 

6 

**Generative Interactive Environments** 


Figure 12: **Learning to simulate deformable objects** : we show frames from a ten step trajectory in the model, taking the same action. Genie is capable of learning the physical properties of objects such as bags of chips. 


Figure 13: **Controllable, consistent latent actions in Robotics** : trajectories beginning from three different starting frames from our Robotics dataset. Each column shows the resulting frame from taking the same latent action five times. Despite training without action labels, not only are the same actions consistent across varied prompt frames, but also have semantic meaning: _down_ , _up_ and _left_ . 

### **3.3. Training Agents** 


Figure 14: **Playing from RL environments** : Genie can generate diverse trajectories given an image of an unseen RL environment. 

We believe Genie could one day be used as a foundation world model for training generalist agents. In fact, in Figure 14 we show that the model can be used for generating diverse trajectories in unseen RL environments. We further investigate if latent actions learnt from Internet videos can be used for imitating behaviors from unseen videos. We use a frozen LAM to label a sequence of expert videos from a target environment with discrete latent actions and then train a policy that predicts the likelihood of the expert taking 

a latent action given an observation. We then use a small dataset with expert ground-truth actions for mapping latent to real actions (see Appendix E for more details). 

We evaluate in both hard and easy settings of a procedurally generated 2D-platformer environment, CoinRun (Cobbe et al., 2020), and compare against an oracle behavioral cloning (BC) model that has access to expert actions as an upper bound, and a random agent as a lower bound (Figure 15). Notably, the LAM-based policy achieves the same score as the oracle and adapts given as few as 200 expert samples, despite almost certainly never seeing CoinRun before. This provides evidence that the learnt latent actions are consistent, as the mapping from latent to real contains no information about the current observation. 


Figure 15: **BC results** . Mean percentage of levels solved out of 100 samples, averaged over 5 seeds with 95% confidence intervals. 

### **3.4. Ablation Studies** 

**Design choices for latent action model** In designing our latent action model, we carefully considered the type of input to use. While we ultimately chose to use the original images (pixels), we thoroughly evaluated this choice against the alternative of using tokenized images (replacing x with z in Figure 5). We refer to this alternative approach as the “token-input” model (see Table 2). While this model achieved a slightly lower FVD score on the Platformers dataset, it did not maintain this advantage on the Robotics dataset. More importantly, in both environments, the tokeninput model exhibited worse controllability (as measured by ∆ _t_ PSNR). This suggests that some information about video dynamics and movement might have been lost during tokenization, and as a result it is beneficial for the latent 

7 

**Generative Interactive Environments** 

action model to take in raw videos as input. 

Table 2: **Latent action model input ablation** . We see that Genie achieves higher controllability. 

||Dataset|#Params|FVD (_↓_)|∆_t_PSNR(_↑_)|
|---|---|---|---|---|
|Token-input|Platformers|2.3B|**38.8**|1.33|
|Pixel-input (**Genie**)|Platformers|2.5B|40.1|**1.91**|
|Token-input|Robotics|1B|257.8|1.65|
|Pixel-input (**Genie**)|Robotics|1B|**136.4**|**2.07**|


**Tokenizer architecture ablations** We compare the performance of three choices of tokenizers, including 1) (spatialonly) ViT, 2) (spatial-temporal) ST-ViViT and 3) (spatialtemporal) C-ViViT (Table 3). For comparison we use similar number of parameters for all tokenizers, with patch size 10, batch size 128 and sequence length 16. We then train the same dynamics and latent action model on these three different tokenizers, and report their FVD as well as ∆ _t_ PSNR. 

Table 3: **Tokenizer architecture ablation** : Our ST-ViViT architecture results in the best performing tokenizer. 

||#Params|Memory|FVD (_↓_)|∆_t_PSNR(_↑_)|
|---|---|---|---|---|
|ViT|230M|0.3GB|114.5|1.39|
|C-ViViT (Villegas et al.,2023)|225M|1.6GB|272.7|1.37|
|**ST-ViViT (ours)**|205M|0.9GB|**81.4**|**1.66**|


Our proposed ST-ViViT architecture provides both improved video generation (FVD) and ∆ _t_ PSNR, for a reasonable trade-off in memory, as compared to to C-ViViT and the spatial-only ViT. This demonstrates its ability to generate videos of high fidelity and controllability, respectively. While C-ViViT employs a full space-time attention mechanism, resulting in significantly higher memory consumption compared to the other two architectures at the same parameter count, this does not translate to improved performance. In fact, C-ViViT exhibits a tendency towards overfitting, necessitating strong regularization during training, which might explain its considerably lower performance. 

## **4. Related Work** 

**World models** Generative interactive environments can be considered a class of _World Models_ (Ha & Schmidhuber, 2018; Oh et al., 2015), which enable next-frame prediction that is conditioned on action inputs (Bamford & Lucas, 2020; Chiappa et al., 2017; Hafner et al., 2020; 2021; Kim et al., 2020; 2021; Micheli et al., 2023; Nunes et al., 2020; Pan et al., 2022; Robine et al., 2023). Such models can be useful for training agents, as they can be used for learning policies without direct environment experience at agent training time. However, learning the models themselves typically requires action-conditioned data obtained directly from the environment. In contrast, our approach seeks to learn a world model in an unsupervised fashion from videos alone. Recently, there has been renewed emphasis on scaling 

world models. GAIA-1 (Hu et al., 2023) and UniSim (Yang et al., 2023) learn world models for autonomous driving and robotic manipulation respectively. These approaches require both text and action labels, while we focus on training from video-only data from publicly available Internet videos. 

**Video models** Our work is related to _video models_ , which typically condition on initial frames (or text) and predict the remaining frames in a video (Blattmann et al., 2023b; Clark et al., 2019; Finn et al., 2016; Ho et al., 2022a;b; Hoppe¨ et al., 2022; Kalchbrenner et al., 2017; Le Moing et al., 2021; Lotter et al., 2017; Luc et al., 2020; Singer et al., 2023; Walker et al., 2021; Yan et al., 2021). Our approach most resembles recent transformer based models such as Phenaki (Villegas et al., 2023), TECO (Yan et al., 2023) and MaskViT (Gupta et al., 2023), as we use MaskGIT (Chang et al., 2022) and an ST-Transformer (Xu et al., 2020) over tokenized images. While video models are becoming increasingly controllable (e.g. (Huang et al., 2022)), we seek a more agentic goal and explicitly learn a _latent action space_ directly from data, allowing users or agents to “play” the model using latent action-conditioned predictions. 

**Playable Video Generation** Genie generalizes beyond Playable Video Generation (PVG) (Menapace et al., 2021), where latent actions are used for controlling world models learnt directly from videos (Menapace et al., 2021; 2022). In contrast to Genie, PVG and related works (Davtyan & Favaro, 2022) consider domain-specific static examples, rather than generating entirely new environments via prompting. Thus, scaling beyond this setting required nontrivial architectural changes, dropping inductive biases in exchange for a general method. 

**Environment generation** Our work is also related to _Procedural Content Generation_ (PCG, see for example Risi & Togelius, 2020a;b) where machine learning has proven highly effective for generating game levels (Summerville et al., 2018), recently via language models that directly write game code (Sudhakaran et al., 2023; Todd et al., 2023). Language models themselves can also be considered to be interactive environments (Wong et al., 2023), albeit lacking a visual component. By contrast in our setting the levels can be learnt and generated directly from pixels, which enables us to utilize the diversity of Internet video data. Other related works have aimed to learn game level components from videos, but require domain-specific knowledge and thus could be difficult to scale (Guzdial & Riedl, 2016; Guzdial et al., 2017). 

**Training agents with latent actions** Prior works have used latent actions for imitation from observation (Edwards et al., 2019), planning (Rybkin* et al., 2019) and pre-training RL agents (Schmidt & Jiang, 2024; Ye et al., 2022). These approaches have similar objectives to our latent action model, though have not been applied at scale. VPT (Baker et al., 

8 

**Generative Interactive Environments** 

2022) is a recent approach that uses an inverse dynamics model learnt from human-provided action labeled data, to label Internet-scale videos with actions that can then be used for training a policy. We showed, in contrast, that we can use _latent_ actions learnt from Internet videos to infer policies for arbitrary environments, avoiding the need for ground-truth actions that are costly and may not generalize. 

## **5. Conclusion and Future Work** 

We proposed Genie, a new form of generative AI that enables anyone, even children, to dream up, create, and step into generated worlds as we can with human-designed simulated environments. We demonstrated that Genie can be prompted to generate a diverse set of interactive and controllable environments despite training from video-only data. 

There are clear improvements that can be made to the model. Genie inherits some of the weaknesses of other autoregressive transformer models, and can hallucinate unrealistic futures. And while we have made progress with spatiotemporal representations, we are still limited to 16 frames of memory which makes it challenging to get consistent environments over long horizons. Finally, Genie currently operates around 1FPS and requires future advances to achieve an efficient frame rate for interaction. 

Still, we believe Genie opens up vast potential for future research. Given its generality, the model could be trained from an even larger proportion of Internet videos to simulate diverse, realistic, and imagined environments. Furthermore, we only briefly touched upon the capabilities of using Genie for training agents, but given that the lack of rich and diverse environments is one of the key limitations in RL, we could unlock new paths to creating more generally capable agents. 

## **Impact Statement** 

**Societal Impact** Genie could enable a large amount of people to generate their own game-like experiences. This could be positive for those who wish to express their creativity in a new way, for example children who could design and step into their own imagined worlds. We also recognize that with significant advances, it will be critical to explore the possibilities of using this technology to amplify existing human game generation and creativity—and empowering relevant industries to utilize Genie to enable their next generation of playable world development. 

**Training Data and Weights** : We have chosen not to release the trained model checkpoints, the model’s training dataset, or examples from that data to accompany this paper or the website. We would like to have the opportunity to further engage with the research (and video game) community and to ensure that any future such releases are respectful, safe 

and responsible. 

**Reproducibility** : We understand that it may be challenging for researchers with fewer computational to reproduce our main results. In order to mitigate this issue, we describe a smaller scale, fully reproducible example in Appendix F that can run on a single mid-range TPU (or GPU). Given that many design choices translate between the two settings, we believe this will make it possible for the broader community to investigate future architectural improvements as well as additional research directions resulting from our work. 

## **Acknowledgements** 

We thank Mateusz Malinowski, Philip Ball and Louis Kirsch for reviewing a draft of our paper; Cassidy Hardin, David Bridson, Eric Lau, Lars Lowe Sjoesund, Lucas Smaira and Bernardo Avila Pires for help with our Platformers dataset; Ruben Villegas for valuable discussions on our video model training and evaluation; and Adrian Bolton, Rushil Mistry, Hannah Openshaw, Zoubin Ghahramani, Raia Hadsell, Koray Kavukcuoglu, Daan Wierstra, Doina Precup and Ed Hirst for strategic advice and guidance. We make use of the DeepMind Jax ecosystem (Babuschkin et al., 2010) and specifically thank Andy Brock for building the internal framework we used for our model training and Arthur Brussee who provided an initial interface that enabled us to “play” our models. Finally, thank you to Seneca and Caspian Clune for their creative sketches, potentially making them the youngest ever game designers. 

## **References** 

- Babuschkin, I., Baumli, K., Bell, A., Bhupatiraju, S., Bruce, J., Buchlovsky, P., Budden, D., Cai, T., Clark, A., Danihelka, I., et al. The deepmind jax ecosystem, 2020. _URL http://github. com/deepmind_ , 2010. 

- Bain, M., Nagrani, A., Varol, G., and Zisserman, A. Frozen in time: A joint video and image encoder for end-to-end retrieval. In _2021 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pp. 1708–1718, Los Alamitos, CA, USA, oct 2021. IEEE Computer Society. doi: 10.1109/ICCV48922.2021.00175. 

- Baker, B., Akkaya, I., Zhokov, P., Huizinga, J., Tang, J., Ecoffet, A., Houghton, B., Sampedro, R., and Clune, J. Video pretraining (vpt): Learning to act by watching unlabeled online videos. _Advances in Neural Information Processing Systems_ , 35:24639– 24654, 2022. 

- Bamford, C. and Lucas, S. M. Neural game engine: Accurate learning ofgeneralizable forward models from pixels. In _Conference on Games_ , 2020. 

- Bauer, J., Baumli, K., Behbahani, F., Bhoopchand, A., BradleySchmieg, N., Chang, M., Clay, N., Collister, A., Dasagi, V., Gonzalez, L., Gregor, K., Hughes, E., Kashem, S., Loks-Thompson, M., Openshaw, H., Parker-Holder, J., Pathak, S., Perez-Nieves, N., Rakicevic, N., Rocktaschel, T., Schroecker, Y., Singh, S.,¨ Sygnowski, J., Tuyls, K., York, S., Zacherl, A., and Zhang, 

9 

**Generative Interactive Environments** 

- L. M. Human-timescale adaptation in an open-ended task space. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 1887–1935. PMLR, 23–29 Jul 2023. 

- Blattmann, A., Dockhorn, T., Kulal, S., Mendelevitch, D., Kilian, M., Lorenz, D., Levi, Y., English, Z., Voleti, V., Letts, A., Jampani, V., and Rombach, R. Stable video diffusion: Scaling latent video diffusion models to large datasets, 2023a. 

- Blattmann, A., Rombach, R., Ling, H., Dockhorn, T., Kim, S. W., Fidler, S., and Kreis, K. Align your latents: Highresolution video synthesis with latent diffusion models. _2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 22563–22575, 2023b. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., Ibarz, J., Ichter, B., Irpan, A., Jackson, T., Jesmonth, S., Joshi, N. J., Julian, R., Kalashnikov, D., Kuang, Y., Leal, I., Lee, K.H., Levine, S., Lu, Y., Malla, U., Manjunath, D., Mordatch, I., Nachum, O., Parada, C., Peralta, J., Perez, E., Pertsch, K., Quiambao, J., Rao, K., Ryoo, M., Salazar, G., Sanketi, P., Sayed, K., Singh, J., Sontakke, S., Stone, A., Tan, C., Tran, H., Vanhoucke, V., Vega, S., Vuong, Q., Xia, F., Xiao, T., Xu, P., Xu, S., Yu, T., and Zitkovich, B. Rt-1: Robotics transformer for real-world control at scale. In _Robotics: Science and Systems_ , 2023. 

- Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al. Language models are few-shot learners. _Advances in neural information processing systems_ , 33:1877–1901, 2020. 

- Chang, H., Zhang, H., Jiang, L., Liu, C., and Freeman, W. T. Maskgit: Masked generative image transformer. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 11315–11325, June 2022. 

- Chiappa, S., Racaniere, S., Wierstra, D., and Mohamed, S. Recurrent environment simulators. In _International Conference on Learning Representations_ , 2017. 

- Clark, A., Donahue, J., and Simonyan, K. Efficient video generation on complex datasets. _CoRR_ , abs/1907.06571, 2019. URL http://arxiv.org/abs/1907.06571. 

- Clune, J. Ai-gas: Ai-generating algorithms, an alternate paradigm for producing general artificial intelligence. _arXiv preprint arXiv:1905.10985_ , 2019. 

- Cobbe, K., Hesse, C., Hilton, J., and Schulman, J. Leveraging procedural generation to benchmark reinforcement learning. In _Proceedings of the 37th International Conference on Machine Learning_ , pp. 2048–2056, 2020. 

- Davtyan, A. and Favaro, P. Controllable video generation through global and local motion dynamics. In Avidan, S., Brostow, G., Cisse, M., Farinella, G. M., and Hassner, T. (eds.),´ _Computer Vision – ECCV 2022_ , pp. 68–84, Cham, 2022. Springer Nature Switzerland. ISBN 978-3-031-19790-1. 

- Dehghani, M., Djolonga, J., Mustafa, B., Padlewski, P., Heek, J., Gilmer, J., Steiner, A. P., Caron, M., Geirhos, R., Alabdulmohsin, I., Jenatton, R., Beyer, L., Tschannen, M., Arnab, A., 

Wang, X., Riquelme Ruiz, C., Minderer, M., Puigcerver, J., Evci, U., Kumar, M., Steenkiste, S. V., Elsayed, G. F., Mahendran, A., Yu, F., Oliver, A., Huot, F., Bastings, J., Collier, M., Gritsenko, A. A., Birodkar, V., Vasconcelos, C. N., Tay, Y., Mensink, T., Kolesnikov, A., Pavetic, F., Tran, D., Kipf, T., Lucic, M., Zhai, X., Keysers, D., Harmsen, J. J., and Houlsby, N. Scaling vision transformers to 22 billion parameters. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 7480–7512. PMLR, 23–29 Jul 2023. 

- Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., and Houlsby, N. An image is worth 16x16 words: Transformers for image recognition at scale. In _International Conference on Learning Representations_ , 2021. URL https://openreview.net/forum? id=YicbFdNTTy. 

- Edwards, A., Sahni, H., Schroecker, Y., and Isbell, C. Imitating latent policies from observation. In _International conference on machine learning_ , pp. 1755–1763. PMLR, 2019. 

- Esser, P., Chiu, J., Atighehchian, P., Granskog, J., and Germanidis, A. Structure and content-guided video synthesis with diffusion models. In _2023 IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

- Finn, C., Goodfellow, I., and Levine, S. Unsupervised learning for physical interaction through video prediction. In _Proceedings of the 30th International Conference on Neural Information Processing Systems_ , NIPS’16, pp. 64–72, Red Hook, NY, USA, 2016. Curran Associates Inc. ISBN 9781510838819. 

- Gupta, A., Tian, S., Zhang, Y., Wu, J., Mart´ın-Mart´ın, R., and Fei-Fei, L. Maskvit: Masked visual pre-training for video prediction. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Guzdial, M. and Riedl, M. Game level generation from gameplay videos. In _Proceedings of the AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment_ , volume 12, pp. 44–50, 2016. 

- Guzdial, M., Li, B., and Riedl, M. O. Game engine learning from video. In _IJCAI_ , pp. 3707–3713, 2017. 

- Ha, D. and Schmidhuber, J. Recurrent world models facilitate policy evolution. In _Proceedings of the 32Nd International Conference on Neural Information Processing Systems_ , NeurIPS’18, pp. 2455–2467, 2018. 

- Hafner, D., Lillicrap, T., Ba, J., and Norouzi, M. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations_ , 2020. 

- Hafner, D., Lillicrap, T. P., Norouzi, M., and Ba, J. Mastering atari with discrete world models. In _International Conference on Learning Representations_ , 2021. 

- He, K., Zhang, X., Ren, S., and Sun, J. Deep residual learning for image recognition. In _2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 770–778, 2016. doi: 10.1109/CVPR.2016.90. 

10 

**Generative Interactive Environments** 

- Henry, A., Dachapally, P. R., Pawar, S. S., and Chen, Y. Query-key normalization for transformers. In _Findings of the Association for Computational Linguistics: EMNLP 2020_ , pp. 4246–4253, Online, November 2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.findings-emnlp.379. 

- Ho, J., Chan, W., Saharia, C., Whang, J., Gao, R., Gritsenko, A., Kingma, D. P., Poole, B., Norouzi, M., Fleet, D. J., and Salimans, T. Imagen video: High definition video generation with diffusion models, 2022a. 

- Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M., and Fleet, D. J. Video diffusion models. In Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and Oh, A. (eds.), _Advances in Neural Information Processing Systems_ , volume 35, pp. 8633– 8646. Curran Associates, Inc., 2022b. 

- Hong, W., Ding, M., Zheng, W., Liu, X., and Tang, J. Cogvideo: Large-scale pretraining for text-to-video generation via transformers. _arXiv preprint arXiv:2205.15868_ , 2022. 

- Hong, W., Ding, M., Zheng, W., Liu, X., and Tang, J. Cogvideo: Large-scale pretraining for text-to-video generation via transformers. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https://openreview.net/ forum?id=rB6TpjAuSRy. 

- Hoppe, T., Mehrjou, A., Bauer, S., Nielsen, D., and Dittadi, A.¨ Diffusion models for video prediction and infilling. _Transactions on Machine Learning Research_ , 2022. ISSN 2835-8856. 

- Hu, A., Russell, L., Yeo, H., Murez, Z., Fedoseev, G., Kendall, A., Shotton, J., and Corrado, G. Gaia-1: A generative world model for autonomous driving, 2023. 

- Huang, J., Jin, Y., Yi, K. M., and Sigal, L. Layered controllable video generation. In _Computer Vision – ECCV 2022: 17th European Conference, Tel Aviv, Israel, October 23–27, 2022, Proceedings, Part XVI_ , pp. 546–564, Berlin, Heidelberg, 2022. Springer-Verlag. ISBN 978-3-031-19786-4. 

- Jouppi, N. P., Yoon, D. H., Kurian, G., Li, S., Patil, N., Laudon, J., Young, C., and Patterson, D. A domain-specific supercomputer for training deep neural networks. _Communications of the ACM_ , 63(7):67–78, 2020. 

- Kalashnikov, D., Irpan, A., Pastor, P., Ibarz, J., Herzog, A., Jang, E., Quillen, D., Holly, E., Kalakrishnan, M., Vanhoucke, V., et al. Qt-opt: Scalable deep reinforcement learning for visionbased robotic manipulation. _arXiv preprint arXiv:1806.10293_ , 2018. 

- Kalchbrenner, N., van den Oord, A., Simonyan, K., Danihelka, I., Vinyals, O., Graves, A., and Kavukcuoglu, K. Video pixel networks. In Precup, D. and Teh, Y. W. (eds.), _Proceedings of the 34th International Conference on Machine Learning_ , volume 70 of _Proceedings of Machine Learning Research_ , pp. 1771–1779. PMLR, 06–11 Aug 2017. URL https://proceedings. mlr.press/v70/kalchbrenner17a.html. 

- Kapturowski, S., Ostrovski, G., Quan, J., Munos, R., and Dabney, W. Recurrent experience replay in distributed reinforcement learning. In _International conference on learning representations_ , 2018. 

- Kim, S. W., Zhou, Y., Philion, J., Torralba, A., and Fidler, S. Learning to simulate dynamic environments with gamegan. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2020. 

- Kim, S. W., Philion, J., Torralba, A., and Fidler, S. Drivegan: Towards a controllable high-quality neural simulation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 5820–5829, June 2021. 

- Le Moing, G., Ponce, J., and Schmid, C. Ccvs: Context-aware controllable video synthesis. In Ranzato, M., Beygelzimer, A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.), _Advances in Neural Information Processing Systems_ , volume 34, pp. 14042– 14055. Curran Associates, Inc., 2021. 

- Lotter, W., Kreiman, G., and Cox, D. Deep predictive coding networks for video prediction and unsupervised learning. In _International Conference on Learning Representations_ , 2017. URL https://openreview.net/forum?id=B1ewdt9xe. 

- Luc, P., Clark, A., Dieleman, S., de Las Casas, D., Doron, Y., Cassirer, A., and Simonyan, K. Transformation-based adversarial video prediction on large-scale data. _CoRR_ , abs/2003.04035, 2020. 

- Menapace, W., Lathuiliere,` S., Tulyakov, S., Siarohin, A., and Ricci, E. Playable video generation. In _IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2021, virtual, June 19-25, 2021_ , pp. 10061–10070. Computer Vision Foundation / IEEE, 2021. 

- Menapace, W., Lathuiliere,` S., Siarohin, A., Theobalt, C., Tulyakov, S., Golyanik, V., and Ricci, E. Playable environments: Video manipulation in space and time. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022. 

- Micheli, V., Alonso, E., and Fleuret, F. Transformers are sampleefficient world models. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Nunes, M. S., Dehban, A., Moreno, P., and Santos-Victor, J. Action-conditioned benchmarking of robotic video prediction models: a comparative study. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 8316–8322, 2020. doi: 10.1109/ICRA40945.2020.9196839. 

- Oh, J., Guo, X., Lee, H., Lewis, R., and Singh, S. Actionconditional video prediction using deep networks in atari games. In _Proceedings of the 28th International Conference on Neural Information Processing Systems - Volume 2_ , NIPS’15, pp. 2863–2871, Cambridge, MA, USA, 2015. MIT Press. 

- Open Ended Learning Team, Stooke, A., Mahajan, A., Barros, C., Deck, C., Bauer, J., Sygnowski, J., Trebacz, M., Jaderberg, M., Mathieu, M., McAleese, N., Bradley-Schmieg, N., Wong, N., Porcel, N., Raileanu, R., Hughes-Fitt, S., Dalibard, V., and Czarnecki, W. M. Open-ended learning leads to generally capable agents. _CoRR_ , abs/2107.12808, 2021. 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., El-Nouby, A., et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Pan, M., Zhu, X., Wang, Y., and Yang, X. Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models. In Koyejo, S., Mohamed, S., Agarwal, A., Belgrave, D., Cho, K., and Oh, A. (eds.), _Advances in Neural Information Processing Systems_ , volume 35, pp. 23178–23191. Curran Associates, Inc., 2022. 

11 

**Generative Interactive Environments** 

- Radford, A., Narasimhan, K., Salimans, T., and Sutskever, I. Improving language understanding by generative pre-training. 2018. 

- Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al. Language models are unsupervised multitask learners. _OpenAI blog_ , 1(8):9, 2019. 

- Rajbhandari, S., Rasley, J., Ruwase, O., and He, Y. Zero: Memory optimizations toward training trillion parameter models. In _SC20: International Conference for High Performance Computing, Networking, Storage and Analysis_ , pp. 1–16. IEEE, 2020. 

- Ramesh, A., Pavlov, M., Goh, G., Gray, S., Voss, C., Radford, A., Chen, M., and Sutskever, I. Zero-shot text-to-image generation. In Meila, M. and Zhang, T. (eds.), _Proceedings of the 38th International Conference on Machine Learning_ , volume 139 of _Proceedings of Machine Learning Research_ , pp. 8821–8831. PMLR, 18–24 Jul 2021. 

- Ramesh, A., Dhariwal, P., Nichol, A., Chu, C., and Chen, M. Hierarchical text-conditional image generation with clip latents, 2022. 

- Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S. G., Novikov, A., Barth-maron, G., Gimenez, M., Sulsky, Y., Kay, J., Sprin-´ genberg, J. T., Eccles, T., Bruce, J., Razavi, A., Edwards, A., Heess, N., Chen, Y., Hadsell, R., Vinyals, O., Bordbar, M., and de Freitas, N. A generalist agent. _Transactions on Machine Learning Research_ , 2022. ISSN 2835-8856. Featured Certification, Outstanding Certification. 

- Risi, S. and Togelius, J. Increasing generality in machine learning through procedural content generation. _Nature Machine Intelligence_ , 2, 08 2020a. doi: 10.1038/s42256-020-0208-z. 

- Risi, S. and Togelius, J. Procedural content generation: From automatically generating game levels to increasing generality in machine learning. _Nature_ , 2020b. 

- Robine, J., Hoftmann,¨ M., Uelwer, T., and Harmeling, S. Transformer-based world models are happy with 100k interactions. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P., and Ommer, B. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , pp. 10684–10695, June 2022. 

- Rybkin*, O., Pertsch*, K., Derpanis, K. G., Daniilidis, K., and Jaegle, A. Learning what you can do before doing anything. In _International Conference on Learning Representations_ , 2019. 

- Saharia, C., Chan, W., Saxena, S., Li, L., Whang, J., Denton, E., Ghasemipour, S. K. S., Gontijo-Lopes, R., Ayan, B. K., Salimans, T., Ho, J., Fleet, D. J., and Norouzi, M. Photorealistic text-to-image diffusion models with deep language understanding. In Oh, A. H., Agarwal, A., Belgrave, D., and Cho, K. (eds.), _Advances in Neural Information Processing Systems_ , 2022. 

- Schmidt, D. and Jiang, M. Learning to act without actions. In _The Twelfth International Conference on Learning Representations_ , 2024. 

- Shoeybi, M., Patwary, M., Puri, R., LeGresley, P., Casper, J., and Catanzaro, B. Megatron-lm: Training multi-billion parameter language models using model parallelism. _CoRR_ , abs/1909.08053, 2019. URL http://arxiv.org/abs/ 1909.08053. 

- Singer, U., Polyak, A., Hayes, T., Yin, X., An, J., Zhang, S., Hu, Q., Yang, H., Ashual, O., Gafni, O., Parikh, D., Gupta, S., and Taigman, Y. Make-a-video: Text-to-video generation without text-video data. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- Sudhakaran, S., Gonzalez-Duque,´ M., Glanois, C., Freiberger, M., Najarro, E., and Risi, S. Prompt-guided level generation. In _Proceedings of the Companion Conference on Genetic and Evolutionary Computation_ , pp. 179–182, 2023. 

- Summerville, A., Snodgrass, S., Guzdial, M., Holmgard,˚ C., Hoover, A. K., Isaksen, A., Nealen, A., and Togelius, J. Procedural content generation via machine learning (PCGML). _IEEE Trans. Games_ , 10(3):257–270, 2018. 

- Todd, G., Earle, S., Nasir, M. U., Green, M. C., and Togelius, J. Level generation through large language models. In _Proceedings of the 18th International Conference on the Foundations of Digital Games_ , pp. 1–8, 2023. 

- Torabi, F., Warnell, G., and Stone, P. Behavioral cloning from observation. _arXiv preprint arXiv:1805.01954_ , 2018. 

- Unterthiner, T., van Steenkiste, S., Kurach, K., Marinier, R., Michalski, M., and Gelly, S. FVD: A new metric for video generation, 2019. 

- van den Oord, A., Razavi, A., Uria, B., C¸ aglar˘ Unl<sup>¨</sup> u,¨ Nash, C., Wolff, C., Durkan, C., Ding, D., Gorny,´ D., Gladchenko, E., Riedel, F., Qi, H., Kelly, J., Bauer, J., Donahue, J., Zhang, J., Malinowski, M., Binkowski,´ M., Luc, P., Riachi, R., Strudel, R., Sander Dieleman, T. P. I., Ganin, Y., and EatonRosen., Z. Imagen 2. URL https://deepmind.google/ technologies/imagen-2/. 

- van den Oord, A., Vinyals, O., and Kavukcuoglu, K. Neural discrete representation learning. In _Proceedings of the 31st International Conference on Neural Information Processing Systems_ , NIPS’17, pp. 6309–6318, Red Hook, NY, USA, 2017. Curran Associates Inc. ISBN 9781510860964. 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., and Polosukhin, I. Attention is all you need. In _Advances in Neural Information Processing Systems_ , pp. 5998–6008, 2017. 

- Villegas, R., Babaeizadeh, M., Kindermans, P.-J., Moraldo, H., Zhang, H., Saffar, M. T., Castro, S., Kunze, J., and Erhan, D. Phenaki: Variable length video generation from open domain textual descriptions. In _International Conference on Learning Representations_ , 2023. 

- Walker, J. C., Razavi, A., and van den Oord, A. Predicting video with _{_ vqvae _}_ , 2021. 

- Wang, Y., He, Y., Li, Y., Li, K., Yu, J., Ma, X., Chen, X., Wang, Y., Luo, P., Liu, Z., Wang, Y., Wang, L., and Qiao, Y. Internvid: A large-scale video-text dataset for multimodal understanding and generation, 2023. 

12 

**Generative Interactive Environments** 

- Wong, L., Grand, G., Lew, A. K., Goodman, N. D., Mansinghka, V. K., Andreas, J., and Tenenbaum, J. B. From word models to world models: Translating from natural language to the probabilistic language of thought, 2023. 

- Wu, C., Liang, J., Ji, L., Yang, F., Fang, Y., Jiang, D., and Duan, N. Nuwa:¨ Visual synthesis pre-training for neural visual world creation. In _European conference on computer vision_ , pp. 720– 736. Springer, 2022. 

- Xu, M., Dai, W., Liu, C., Gao, X., Lin, W., Qi, G.-J., and Xiong, H. Spatial-temporal transformer networks for traffic flow forecasting. _arXiv preprint arXiv:2001.02908_ , 2020. 

- Yan, W., Zhang, Y., Abbeel, P., and Srinivas, A. Videogpt: Video generation using vq-vae and transformers, 2021. 

- Yan, W., Hafner, D., James, S., and Abbeel, P. Temporally consistent transformers for video generation. In Krause, A., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pp. 39062–39098. PMLR, 23–29 Jul 2023. 

- Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., and Abbeel, P. Learning interactive real-world simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 

- Ye, W., Zhang, Y., Abbeel, P., and Gao, Y. Become a proficient player with limited data through watching pure videos. In _The Eleventh International Conference on Learning Representations_ , 2022. 

13 

**Generative Interactive Environments** 

## **Author Contributions** 

We list authors alphabetically by last name. Please direct all correspondence to project leads: Ashley Edwards (edwardsashley@google.com) and Jack Parker-Holder (jparkerholder@google.com) and tech lead: Jake Bruce (jacobbruce@google.com). 

### **Core Contributors** 

- **Jake Bruce** : project leadership, video tokenizer research, action model research, dynamics model research, scaling, model demo, infrastructure 

- **Michael Dennis** : dynamics model research, scaling, metrics, model demo, infrastructure 

- **Ashley Edwards** : genie concept, project leadership, action model research, agent training, model demo 

- **Edward Hughes** : dynamics model research, infrastructure 

- **Matthew Lai** : dataset curation, infrastructure 

- **Aditi Mavalankar** : action model research, metrics, agent training 

- **Jack Parker-Holder** : genie concept, project leadership, dynamics model research, scaling, dataset curation 

- **Yuge (Jimmy) Shi** : video tokenizer research, dynamics model research, dataset curation, metrics 

- **Richie Steigerwald** : dataset curation, metrics 

### **Partial Contributors and Advisors** 

- **Chris Apps** : project management 

- **Yusuf Aytar** : technical advice 

- **Sarah Bechtle** : technical advice 

- **Feryal Behbahani** : strategic advice 

- **Stephanie Chan** : technical advice 

- **Jeff Clune** : technical advice, strategic advice 

- **Lucy Gonzalez** : project management 

- **Nicolas Heess** : strategic advice 

- **Simon Osindero** : technical advice 

- **Sherjil Ozair** : technical advice 

- **Scott Reed** : technical advice 

- **Jingwei Zhang** : technical advice 

- **Konrad Zolna** : scaling, technical advice 

### **Sponsors** 

- **Nando de Freitas** : strategic advice 

- **Tim Rockt¨aschel** : genie concept, project leadership 

- **Satinder Singh** : strategic advice 

14 

**Generative Interactive Environments** 

## **A. More Example Trajectories** 


Figure 16: **More example trajectories** : the model is prompted with either hand-drawn sketches, images generated from text-to-image generative models or realistic photos. Actions that drive the dynamics of the trajectory are provided by human input. 

15 


Figure 17: **Controllable, consistent latent actions in Platformers** : trajectories beginning from four different starting frames from our Platformers dataset. Each column shows the resulting frame from taking the same latent action five times. Despite training without action labels, not only are the same actions consistent across varied prompt frames, but also have semantic meaning: _left_ , _right_ , _jump_ , and _no-op_ . 

## **B. Dataset** 

### **B.1. Platformers Dataset** 

**Initial Dataset** We generated a dataset by filtering publicly available Internet videos, using the following criteria: 

- The title contains keywords relating to 2D platformer games. 

- The title or description must contain an action word, such as “speedrun” or “playthrough”. 

- The title must not contain negating words such as “movie” or “unboxing”. 

We then split each video into 16s clips at 10 FPS, which corresponds to 160 frames per clip. Our resulting dataset contains 55M videos, which totals around 244k hours. When selecting keywords, we manually spot checked results to check that they typically produced 2D platformer gameplay videos which are not outnumbered by other sorts of videos which happen to share similar keywords. 

**Filter Pipeline** We noticed that many of the videos in the dataset were of poor quality, impacting our model performance. We propose a scalable approach to systematically filter the data, using a learned classifier as in (Baker et al., 2022). First, we define high quality videos as those that display clear gameplay and do not contain distractor items such as menu screen or streamer faces. We then filter this data as follows: 

1. Our team hand labelled 10k videos, with roughly ten hours of total human effort. The labels ranged from 5 (best) to 1 (worst) quality. 

16 

**Generative Interactive Environments** 

2. We trained a 11M parameter ResNet18 (He et al., 2016) with binary classification where we deleted all entries rated 2-4 and classified 5 as good and 1 as bad. 

3. We then apply a decision rule based on model prediction and confidence to determine whether to keep the video. 

Consistent to findings in prior work Baker et al. (2022); Oquab et al. (2023), having high quality data outweighs the quantity of data – even though the curated datasaet is only just over 10% the size of the original dataset, the model trained on the curated dataset outperforms in terms of FVD, see Table 4. Our final dataset is 6.8M videos for a total of over 30k hours. 

Table 4: Effect of dataset curation. 

||#Params|FVD (_↓_)|
|---|---|---|
|Original dataset (55M videos)|580M|61.4|
|Curated dataset (6.8M videos)|580M|**54.8**|


## **C. Training details** 

### **C.1. Latent Action Model Training** 

We found a benefit from increasing the number of codes (i.e. number of actions), at the cost of reduced playability for human and AI agents. 

Table 5: Platformers action model hyperparameters 

|Component|Parameter|Value|
|---|---|---|
|Encoder|num<br>~~l~~ayers|20|
||d<br>~~m~~odel|1024|
||num<br>~~h~~eads|16|
|Decoder|num<br>~~l~~ayers|20|
||d<br>~~m~~odel|1024|
||num<br>~~h~~eads|16|
|Codebook|num<br>~~c~~odes|8|
||patch<br>~~s~~ize|16|
||latent<br>~~d~~im|32|


Note that the model inputs are normalized between 0 and 1 and the final outputs of the decoder are placed through a sigmoid. 

### **C.2. Video Tokenizer Training** 

Here we describe our video tokenizer training. We found it more effective to scale our decoder than the encoder, and a marginal gain from increasing batch size (see Table 6). 

Table 6: Tokenizer batch size scaling hyperparameters. 

|batch<br>~~s~~ize|training hardware|FLOPs|PSNR|
|---|---|---|---|
|64|64 TPUv2|4_._22_×_10<sup>20</sup>|35.7|
|384|64 TPUv3|2_._57_×_10<sup>21</sup>|36.5|


17 

**Generative Interactive Environments** 

Table 7: Platformers video tokenizer hyperparameters. 

|Component|Parameter|Value|
|---|---|---|
|Encoder|num<br>~~l~~ayers<br>d<br>~~m~~odel<br>num<br>~~h~~eads<br>k/q<br>~~s~~ize|12<br>512<br>8<br>64|
|Decoder|num<br>~~l~~ayers<br>d<br>~~m~~odel|20<br>1024|
||num<br>~~h~~eads|16|
||k/q<br>~~s~~ize|64|
|Codebook|num<br>~~c~~odes|1024|
||patch<br>~~s~~ize|4|
||latent<br>~~d~~im|32|


We train our video tokenizer for 300k steps using the AdamW optimizer, with cosine decay, using the hyperparameters in Table 8. 

Table 8: Video tokenizer optimizer hyperparameters 

|Parameter|Value|
|---|---|
|max<br>~~l~~r|3e-4|
|min<br>~~l~~r|3e-4|
|_β_1|0.9|
|_β_2|0.9|
|weight<br>~~d~~ecay|1e-4|
|warmup<br>~~s~~teps|10k|


### **C.3. Dynamics Model Training** 

Table 9: Dynamics model optimizer hyperparameters 

|Parameter|Value|
|---|---|
|max<br>~~l~~r|3e-5|
|min<br>~~l~~r|3e-6|
|_β_1|0.9|
|_β_2|0.9|
|weight<br>~~d~~ecay|1e-4|
|warmup<br>~~s~~teps|5k|


## **D. Scaling Experiments Details** 

In this section we provide more details on the architecture as well as compute budget for the scaling experiments. 

**Scaling model size** For all models we use a batch size of 256. We train all models for 200k steps, thus use a total of 750B training tokens for each run. All runs make use of batch parallelism and stage-3 ZeRO sharding (Rajbhandari et al., 2020), while our larger models also make use of tensor parallelism (Shoeybi et al., 2019). For this experiment we make use of TPUv2 and TPUv3 (Jouppi et al., 2020). See Table 10 for more details. 

18 

**Generative Interactive Environments** 

Table 10: Model size scaling architectures and compute usage. All models were trained for 200k steps with a batch size of 256, equating to 750B tokens. 

|Parameters|num<br>~~l~~ayers|num<br>~~h~~eads|d<br>~~m~~odel|k/q size|training hardware|training time|FLOPs|
|---|---|---|---|---|---|---|---|
|41M|18|8|512|64|64 TPUv2|3 days|2_._05_×_10<sup>20</sup>|
|96M|16|16|768|64|64 TPUv2|6 days|3_._58_×_10<sup>20</sup>|
|192M|20|18|1024|64|64 TPUv2|9 days|6_._4_×_10<sup>20</sup>|
|404M|21|12|1536|128|64 TPUv2|18 days|1_._2_×_10<sup>21</sup>|
|811M|20|20|2048|128|128 TPUv3|7 days|2_._2_×_10<sup>21</sup>|
|1.6B|28|22|2560|128|128 TPUv3|12 days|4_._04_×_10<sup>21</sup>|
|2.7B|36|22|3072|128|256 TPUv3|16 days|6_._91_×_10<sup>21</sup>|


**Scaling batch size** All models use the same architecture with 2.3B parameters, as shown in Table 11, and train for 200k steps. The only difference between the three runs is hardware—the 128, 256 and 448 batch size models train on 64 TPUv3, 128 TPUv3 and 64 TPUv5p respectively. 

Table 11: Batch size scaling hyperparameters. All models use the following architecture for 200k steps, differing only in batch size. 

|Parameters<br>num<br>~~l~~ayers|num<br>~~h~~eads|d<br>~~m~~odel|k/q size|
|---|---|---|---|
|2.3B<br>34|20|2560|128|


**Genie Model** The parameter count, model architecture as well as compute usage of the dynamics model for the final Genie model is listed in Table 12. We train a 10.1B dynamics model with a batch size of 512, for a total of 125k steps using 256 TPUv5. 

Table 12: Genie dynamics model hyperparameters. 

|Parameters<br>num<br>~~l~~ayers|num<br>~~h~~eads|d<br>~~m~~odel|k/q size|FLOPs|
|---|---|---|---|---|
|10.1B<br>48|36|5120|128|6_._6_×_10<sup>22</sup>|


## **E. Behavioral Cloning Details** 

In this section we provide more details about our behavioral cloning experiments. We train within the Procgen CoinRun environment (Cobbe et al., 2020) and evaluate in a held out test set. We assume we have a dataset of expert sequences in this environment from an agent trained with R2D2 (Kapturowski et al., 2018). We then train an agent to imitate from this data. Notably, the oracle agent has access to the corresponding ground-truth expert actions. We now discuss how we can utilize a pre-trained LAM to infer the actions taken. 

### **E.1. Genie LAM** 

In order to train an agent to imitate from unseen videos, we can use a frozen LAM from a Genie model trained on Internet videos. Given an expert sequence _⟨xt, xt_ +1 _⟩_ we extract the corresponding latent action label _at ← LAM_ ( _xt, xt_ +1). We then train a policy _π_ ( _at|xt_ ) to predict the likelihood of the expert taking latent action _at_ given observation _xt_ . Note that this procedure is similar to prior works that learn from videos (Baker et al., 2022; Torabi et al., 2018). However, these approaches use ground-truth actions for labeling videos whereas we utilize latent actions learnt completely offline. 

During inference, we must map latent actions emitted by the policy to real actions. To do this, we utilize a small set of action-labeled expert sequences. Given an expert sequence _⟨xt, ut, xt_ +1 _⟩_ (we denote _ut_ for ground-truth actions to avoid confusion with predicted latent actions), we use the LAM to obtain a latent action _at_ and fill a dictionary _D_ consisting of mapped latents to a list of corresponding real actions. In summary, given an observation _xt_ from the environment, we can obtain the most likely latent action as _at ∼ π_ ( _st_ ), and then take the corresponding real action as _ut ∼ D_ [ _at_ ]. 

Note that other works have used data extracted from the agent’s policy to obtain a mapping from latent to real actions (Edwards et al., 2019; Ye et al., 2022), but we found using expert data enabled us to better evaluate the quality of the learnt policy. As shown in the main text, the agent was capable of adapting with as few as 200 expert labels. 

19 

**Generative Interactive Environments** 

### **E.2. Architecture** 

We train a transformer as the policy for both the oracle and latent BC agents. We utilize our proposed ST-ViViT architecture for encoding the frames **_x_** 1: _t_ = ( _x_ 1 _, · · · xt_ ) . All previous actions are placed through a one-hot and then combined with the corresponding frame encoding as an additive embedding. We use a sequence length of 4 during both training and inference and a batch size of 16. 

Both the oracle and Genie LAM are trained with a cross-entropy loss where targets are either real or latent actions, respectively. During inference, we obtain the final prediction by sampling from the predicted logits. Note we found the oracle agent performed better when we randomly sampled actions 10% of the time. 

Table 13: BC model optimizer hyperparameters 

|Parameter|Value|
|---|---|
|max<br>~~l~~r|3e-5|
|min<br>~~l~~r|3e-6|
|_β_1|0.9|
|_β_2|0.96|
|weight<br>~~d~~ecay|1e-4<br>|
|warmup<br>~~s~~teps|5k|


Table 14: BC policy hyperparameters 

|Component|Parameter|Value|
|---|---|---|
|Encoder|num<br>~~l~~ayers|12|
||d<br>~~m~~odel|512|
||patch<br>~~s~~ize|4|
|Policy|linear<br>~~l~~ayer|512|


## **F. Reproducible Case Study** 

In this section we describe a self-contained, fully reproducible case study that can be trained with a single mid range TPU/GPU in under a week. 

### **F.1. Data Collection** 

First we need to collect the data to train our model. We use the CoinRun environment from the Procgen benchmark (Cobbe et al., 2020) since it has thousands of visually diverse levels with fairly simple platformer-like dynamics. Using the “hard” mode, we collect data using a random policy with no action repeats. We sample level seeds between zero and 10,000 and collect 1,000 timesteps for each level, for a total of 10M transitions. 

### **F.2. Video Tokenizer Training** 

Our video tokenizer for CoinRun follows the same setup as described in Section 2.1, trained with the optimizer configuration as in Section C.2. The primary difference in this example is we use smaller model sizes (see Table 15), and then use a batch size of 48 sequences, of length 16, for a total of 768 images per batch. This is sufficient to fit in a single TPU with 16G memory. The model is trained for three days using a single TPU which is sufficient to complete 300k steps. 

20 

**Generative Interactive Environments** 

Table 15: CoinRun video tokenizer hyperparameters 

|Component|Parameter|Value|
|---|---|---|
|Encoder|num<br>~~l~~ayers<br>d<br>~~m~~odel|8<br>512|
||num<br>~~h~~eads|8|
|Decoder|num<br>~~l~~ayers|8|
||d<br>~~m~~odel|512|
||num<br>~~h~~eads|8|
|Codebook|num<br>~~c~~odes<br>patch<br>~~s~~ize|1024<br>4|
||latent<br>~~d~~im|32|


### **F.3. Dynamics + Latent Action Model Training** 

Once we have trained the video tokenizer we can then jointly train the latent action and dynamics models. Once again we seek to fit our model training inside 16G memory, so we use a batch size of 36 sequences consisting of 16 frames each, for a total of 576 images. We train both the latent action model and dynamics model in parallel, using the setup described above (see: Section C.1 for the latent action model and Section C.3 for the dynamics model). 

We train both the latent action and dynamics models in parallel for 200k steps, using the optimizer hyperparameters in Table 9. 

Table 16: CoinRun action model hyperparameters 

|Component|Parameter|Value|
|---|---|---|
|Encoder|num<br>~~l~~ayers|8|
||d<br>~~m~~odel|512|
||num<br>~~h~~eads|8|
|Decoder|num<br>~~l~~ayers|8|
||d<br>~~m~~odel|512|
||num<br>~~h~~eads|8|
|Codebook|num<br>~~c~~odes|6|
||latent<br>~~d~~im|32|


Table 17: CoinRun dynamics model hyperparameters 

|Component|Parameter|Value|
|---|---|---|
|Architecture|num<br>~~l~~ayers|12|
||d<br>~~m~~odel|512|
||num<br>~~l~~ayers|8|
|Sampling|temperature|1.0|
||maskgit<br>~~s~~teps|25|


21 

