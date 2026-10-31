---
title: "ChronoDreamer: Action-Conditioned World Model as an Online Simulator for Robotic Planning"
date: "2025-12-21"
authors: "Zhenhao Zhou; Dan Negrut"
url: https://arxiv.org/abs/2512.18619
pdf: https://arxiv.org/pdf/2512.18619
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2512.18619)** / [論文ページ](https://arxiv.org/abs/2512.18619)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# ChronoDreamer: Action-Conditioned World Model as an Online Simulator for Robotic Planning 

Zhenhao Zhou, Dan Negrut<sup>1</sup> 

> 1University of Wisconsin–Madison `zzhou292@wisc.edu, negrut@wisc.edu` 

## **Abstract** 

We present ChronoDreamer, an action-conditioned world model for contact-rich robotic manipulation. Given a history of egocentric RGB frames, contact maps, actions, and joint states, ChronoDreamer predicts future video frames, contact distributions, and joint angles via a spatial-temporal transformer trained with MaskGITstyle masked prediction. Contact is encoded as depthweighted Gaussian splat images that render 3D forces into a camera-aligned format suitable for vision backbones. At inference, predicted rollouts are evaluated by a vision-language model that reasons about collision likelihood, enabling rejection sampling of unsafe actions before execution. We train and evaluate on DreamerBench, a simulation dataset generated with Project Chrono that provides synchronized RGB, contact splat, proprioception, and physics annotations across rigid and deformable object scenarios. Qualitative results demonstrate that the model preserves spatial coherence during non-contact motion and generates plausible contact predictions, while the LLM-based judge distinguishes collision from noncollision trajectories. 

## **1 Introduction** 

Robots operating in contact-rich environments require trajectory planning that respects both task objectives and collision constraints. Classical approaches rely on explicit geometric models and physics simulators, but high-fidelity simulation is often too slow for online replanning, and sim-to-real gaps persist even with careful calibration. Learned world models offer a complementary path: by predicting future states conditioned on actions, they enable planning by imagination at speeds compatible with real-time control. However, most video prediction models focus on visual plausibility and neglect the physical quantities—contact forces, friction modes, joint states—that determine whether a trajectory is safe. 

This work addresses the gap between video generation and contact-aware planning. We introduce ChronoDreamer, an action-conditioned world model that jointly 

predicts future RGB frames, contact maps, and joint angles. The model operates on discrete visual tokens from a pretrained encoder and uses a spatial-temporal transformer with factorized attention to maintain tractable complexity over long horizons. Contact is represented as a camera-aligned image via depth-weighted Gaussian splats, encoding force magnitude and direction in a form directly consumable by vision backbones. At inference time, predicted rollouts are passed to a vision-language model that reasons about collision likelihood, enabling rejection sampling of unsafe actions before execution. 

#### **Contributions.** 

- A contact encoding scheme that renders 3D contact forces as depth-weighted Gaussian splat images aligned with the robot’s egocentric camera, providing dense contact supervision in an image-native format. 

- ChronoDreamer, a spatial-temporal transformer world model that predicts video tokens, contact tokens, and joint angles jointly via MaskGIT-style masked prediction with factorized vocabulary. 

- Integration of world-model rollouts with an LLMbased collision judge that reasons over predicted frames and contact maps to filter unsafe action candidates online. 

- Evaluation on DreamerBench, a multi-scenario dataset with rigid and deformable objects, demonstrating spatial coherence preservation and contactevent prediction. 

## **2 Background and Motivation** 

State-of-the-art text- and image-conditioned video generators now produce photorealistic textures and intricate geometry, yet they still violate basic mechanics: objects interpenetrate, trajectories defy gravity, and energy appears or vanishes. For robotics, scientific visualization, or simulation-aware media, these failures are structural rather than aesthetic, and they motivate returning to the 

1 

world-model viewpoint in which a generator maintains an internal state and transition dynamics coherent enough to support imagination and planning. Classic systems such as World Models, PlaNet, and Dreamer—and large-scale successors like Genie—demonstrated that long-horizon behavior hinges on latent dynamics that stay faithful to first principles [1]. Reframing modern video generation through this lens suggests that perceptual fidelity must be paired with state updates governed by constraints resembling Newtonian, and more broadly physical, laws. 

One route to lawful dynamics is to make physically plausible motion the default attractor via architectural bias. PhyDNet and PhyLoNet introduce dual pathways that disentangle a PDE-inspired “physics” cell from a residual appearance branch; the former evolves smooth, conservative dynamics, while the latter handles nuisance visual factors [2]. Even though these designs predate diffusion models, the lesson transfers: inserting lightweight, physics-structured latent updates between denoising steps or constraining attention flows to respect locality regularizes temporal evolution, cuts down implausible transitions, and keeps the latent state easier to plan in—much like traditional world-model agents that rely on carefully structured transition models instead of unconstrained recurrence. 

Another strand delegates state evolution to a mechanistic simulator and reserves the generator for photorealistic rendering. PhysGen exemplifies a staged pipeline in which geometry and material parameters are inferred from a single image and user command, a rigid-body simulator propagates contact-rich dynamics, and a diffusion renderer produces temporally consistent imagery guided by the simulated motion [3]. Variants insert deformable or continuum solvers, or periodically project denoising intermediates back onto the simulator’s feasible set, tightening constraints while preserving generative diversity. From the world-model perspective, these simulator-inthe-loop systems externally scaffold the transition model: a trusted dynamical engine maintains or corrects the latent state, whereas the generator focuses on appearance. Design choices revolve around the governing simulator class, how tightly it couples to the denoiser, and how physical parameters are estimated or adapted over time, but even simple staged interfaces yield large reductions in violations while preserving user control. 

A complementary approach relies on multimodal language and vision-language models to supply symbolic reasoning about forces, contacts, and constraints before or during sampling. DiffPhy parses a prompt to extract entities and qualitative dynamics, then guides a diffusion model to honor that physical “plan”; VideoREPA distills relational understanding from recognition models into text-to-video generators so that high-level commonsense physics is baked into the latent transitions without embedding a full simulator [4]. Viewed through world modeling, the reasoner acts as a high-level dynamics prior that proposes coarse motion plans which the generator 

follows, yielding more globally plausible rollouts while retaining the coverage of large video backbones. Because symbolic reasoning can hallucinate, practical systems pair it with lightweight validators or occasional simulator hints, but the amortized planning cost makes this path attractive when prompts describe qualitative effects that are difficult to capture with explicit simulation alone. 

Finally, physics can be enforced through training-free guidance signals that nudge the denoiser away from violations without modifying the base model. Recent work constructs counterfactual prompts that deliberately break physics and uses synchronized, decoupled guidance to push samples away from those modes, improving gravity and contact behavior without finetuning [5]. Related frame-level control techniques inject depth, sketch, or keyframe cues during denoising; when those cues are replaced by physics-violation critics such as penetration detectors or anti-gravity classifiers, the same machinery becomes a soft controller on the sampler’s transition dynamics [6]. By training lightweight critics or distilling simulator judgments into differentiable surrogates, one can retrofit powerful pretrained generators with practical physics correctors, combining the engineering pragmatism of plug-and-play guidance with the rigor of simulator or reasoning-based constraints. 

## **3 Method** 

### **3.1 Contact Encoding via DepthWeighted Gaussian Splats** 

A central design choice in DreamerBench is to represent contact as a camera-centric image rather than as a sparse list of contact points. Existing work explores several alternatives. Neural Contact Fields represent contact as a continuous probability field over 3D space conditioned on tactile inputs, enabling estimation of complex extrinsic contact patches from visuotactile signals [7]. Vision-only approaches such as Im2Contact recover dense contact maps from RGB observations by learning a pixel-wise contact likelihood without explicit access to forces or tactile measurements [8]. Large-scale visuotactile datasets including FreeTacMan encode contact as image-like tactile fields synchronized with external views for contactrich manipulation [9]. More recently, DyTact models dynamic contacts using 2D Gaussian surfels attached to articulated meshes, rasterized into time-varying contact fields [10]. These lines of work suggest that contact fields expressed in an image-like domain are a convenient interface for modern vision backbones and world models. 

In DreamerBench, each simulation step produces a _contact splat_ image that aggregates all active contacts into a single RGB frame aligned with a reference camera. For each contact _i_ , we log a 3D contact position **p** _i ∈_ R<sup>3</sup> and a contact force **f** _i ∈_ R<sup>3</sup> . Given a camera with world-frame position **c** _∈_ R<sup>3</sup> and rotation **R** _cw ∈_ SO(3) (rotation from 

2 

world to camera), the camera-frame coordinates of the contact point are 


We interpret _Xi_ as depth along the camera forward axis (with _Xi >_ 0 in front of the camera) and apply nearplane clipping by discarding contacts with _Xi < X_ min or clipping line segments to the plane _X_ = _X_ min to avoid numerical instabilities in the projection. 

Projection to the discrete image plane uses a pinhole model with intrinsics ( _fx, fy, cx, cy_ ): 


followed by rounding to the nearest pixel center ( _u_ ˜ _i,_ ˜ _vi_ ) _∈_ Z<sup>2</sup> . To encode force _direction_ in the image plane, the implementation also projects a second point displaced along the force vector, 


with a scale _si_ chosen as an affine or quantile-based function of the force magnitude _∥_ **f** _i∥_ . The displacement between the two projections in pixel space, 


defines a 2D direction vector. After normalization **d** ˆ _i_ = ∆ **d** _i/∥_ ∆ **d** _i∥_ , the two components are mapped from [ _−_ 1 _,_ 1] to [0 _,_ 1] and stored in the green and blue channels, respectively: 

cropped to a finite window of radius _O_ ( _ri_ ). To encourage nearer contacts to dominate farther ones, the kernel is multiplied by a depth-dependent weight 


with a tunable depth scale _τ_ depth _>_ 0. The total weight for contact _i_ at pixel ( _u, v_ ) is then 


Let **c** _i_ = ( _Ri, Gi, Bi_ )<sup>_⊤_</sup> denote the per-contact color vector. The image is assembled by weighted accumulation over all contacts, followed by a per-pixel normalization: 


Here **I** ( _u, v_ ) _∈_ [0 _,_ 1]<sup>3</sup> is the final contact splat image at the given time step. The normalized averaging behaves like a soft z-buffer over Gaussian “surfels”: overlapping contributions are blended rather than summed unboundedly, and nearer contacts are given higher effective weight through _wi_<sup>depth</sup> . The resulting image compactly encodes contact spatial footprint, approximate pressure (via red intensity and kernel size), and projected force direction (via green–blue hue) in a form directly consumable by convolutional networks or video-tokenization modules. 

### **3.2 World Model Architecture** 


The red channel encodes a clipped and normalized force magnitude, 


so that _Ri_ saturates for very large contact forces. 

Each contact is then rendered as an isotropic Gaussian kernel centered at ( _u_ ˜ _i,_ ˜ _vi_ ), with a radius that depends on the normalized magnitude _mi/m_ max. Specifically, we define a radius _ri_ through 


with a shaping exponent _γ ≥_ 1 and bounds 0 _< r_ min _≤ r_ max. The corresponding Gaussian kernel over integer pixel offsets ( _δu, δv_ ) is 


This section describes ChronoDreamer, a spatialtemporal transformer architecture for action-conditioned video prediction that operates on discrete latent representations obtained through finite-scalar quantization. The model employs a MaskGIT-style training objective for next-frame prediction and jointly predicts future video frames, contact maps, and joint angles conditioned on historical observations and action sequences. 

#### **3.2.1 Architecture Overview** 

Figure 1 depicts the data pipeline. Raw RGB frames and contact splat images at 256 _×_ 256 resolution are tokenized by the Cosmos DI8 _×_ 8 encoder via finite-scalar quantization, yielding 32 _×_ 32 discrete token grids per frame. These tokens, along with continuous action commands and joint angle observations, are loaded via memorymapped I/O and passed to the spatial-temporal dynamics model, which outputs predicted video tokens, contact tokens, and regressed joint angles. 

The architecture comprises four components. The _video encoder_ (Nvidia Cosmos Tokenizer) maps _H × W_ RGB 

3 


Figure 1: Data pipeline. Cosmos encoder tokenizes RGB and contact frames into 32 _×_ 32 grids. The dynamics model outputs factorized video/contact logits and joint angles. 

**Convolutional Feature Extraction** The encoder employs a hierarchical convolutional architecture with residual blocks. Given an input image **x** , the encoder first applies an initial convolution: 


where _C_ base = 128 is the base channel dimension. 

The encoder consists of _N_ blocks = 5 stages with channel multipliers (1 _,_ 1 _,_ 2 _,_ 2 _,_ 4). At each stage _i_ , the feature map passes through _N_ res = 2 residual blocks: 


where the residual function _F_ res is defined as: 


with GN( _·_ ) denoting group normalization with 32 groups and _σ_ ( _·_ ) the Swish activation function: 


Spatial downsampling is performed between stages using strided convolutions: 


The final encoder output is obtained through: 


frames to _h × w_ discrete token grids with vocabulary size _V_ = 65 _,_ 536 via finite-scalar quantization. The _spatialtemporal transformer_ consists of _L_ blocks, each containing factorized spatial and temporal self-attention followed by a feed-forward network. The _MaskGIT module_ performs masked token prediction with iterative unmasking governed by a cosine schedule. The _video decoder_ reconstructs RGB frames from quantized latents; separate linear heads project to contact map logits and joint angle outputs. 

Throughout this section, we denote the batch size by _B_ , temporal sequence length by _T_ , input frame dimensions by _H × W_ , latent token grid dimensions by _h × w_ (with _S_ = _h × w_ spatial tokens per frame), model hidden dimension by _D_ , number of attention heads by _Nh_ , vocabulary size by _V_ , and number of transformer layers by _L_ . 

#### **3.2.2 Video Encoder: Nvidia Cosmos Tokenizer with Finite-Scalar Quantization** 

**Encoder Architecture** The video encoder transforms input RGB frames **x** _∈_ R<sup>3</sup><sup>_×H×W_</sup> into discrete latent tokens **z** _∈{_ 0 _,_ 1 _, . . . , V −_ 1 _}_<sup>_h×w_</sup> . The encoding process comprises two stages: continuous feature extraction and lookup-free quantization. 

where _C_ = 6 is the number of continuous latent channels (before quantization) and **h** mid denotes the output of additional mid-block residual layers. The encoder architecture includes a 2-level Haar wavelet transform applied to the input for initial downsampling (factor of 4). 

**Finite-Scalar Quantization (FSQ)** Finite-Scalar Quantization (FSQ) is a non-learned discrete quantization method that maps continuous latent channels to discrete token indices. For each of the _C_ = 6 continuous latent channels, FSQ independently quantizes values to a fixed set of discrete levels. The resulting token indices range over _V ≈_ 65 _,_ 536 distinct values, allowing the encoder to represent rich visual information without maintaining explicit learnable codebooks. 

During decoding, given a token index, FSQ internally de-quantizes to recover the original continuous latent representation. 

**Quantization and Token Index Computation.** FSQ operates on the _C_ = 6 continuous latent channels independently. Each channel is mapped to a discrete level, and the combination of all _C_ channels produces a single token index in the range [0 _, V −_ 1] where _V ≈_ 65 _,_ 536. The quantization is deterministic (non-learned) and fully differentiable. 

4 

**Entropy Regularization.** To encourage codebook utilization, an entropy loss is applied: 


where _H_ sample is the average per-sample entropy and _H_ batch is the entropy of the batch-averaged token distribution. The coefficients _α_ sample = _α_ batch = 1 _._ 0 balance sample-level minimization (encouraging deterministic assignments) and batch-level maximization (encouraging uniform codebook usage). 

**Token Factorization** For large vocabulary sizes, token embeddings are factorized to reduce parameter count. Given _V_ = 2<sup>18</sup> and a factorization into _K_ = 2 subvocabularies, each token index _z_ is decomposed: 


where _Vf_ = _~~√~~ V_ = 512 is the factored vocabulary size, and _z_ 0 _, z_ 1 _∈{_ 0 _, . . . , Vf −_ 1 _}_ . The token embedding is computed as the sum of factored embeddings: 


where **E** 0 _,_ **E** 1 _∈_ R<sup>_Vf ×D_</sup> are learnable embedding matrices. 

_Joint Angle Embedding._ Joint angles are similarly projected: 


where **W** _j ∈_ R<sup>_D×Nj_</sup> . 

_Combined Control Token._ The action and joint angle embeddings are combined additively to form a single control token per frame: 


This combined control token is prepended to the video tokens for each frame, yielding an augmented sequence: 


The full input tensor has shape ( _B, T, S_ + 1 _, D_ ), where the first position in the spatial dimension corresponds to the control token. 

**Positional Encoding** Learnable positional embeddings encode both temporal and spatial positions: 


The positional embedding is added to the input representation: 


#### **3.2.3 Input Representation and Conditioning** 

#### **3.2.4 Spatial-Temporal Transformer Decoder** 

**Input Modalities** The model receives four input modalities: _history video tokens_ **Z** hist _∈{_ 0 _, . . . , V }_<sup>_Th×S_</sup> , discrete tokens for _Th_ history frames with _S_ = _h × w_ spatial tokens per frame; _history actions_ **a** hist _∈_ R<sup>_Th×_3</sup> , continuous vectors encoding commanded velocities; _future actions_ **a** fut _∈_ R<sup>_Tf ×_3</sup> , action vectors for frames to be predicted; and _history joint angles_ **_θ_** hist _∈_ R<sup>_Th×Nj_</sup> with _Nj_ = 4 joint channels. 

**Embedding Strategy** _Video Token Embedding._ Video tokens are embedded using the factorized embedding scheme: 


A special mask token embedding **e** mask _∈_ R<sup>_D_</sup> is used for tokens that are masked during training: 


_Action Embedding._ Actions are projected to the model dimension through a linear layer followed by layer normalization: 


**Architecture Overview** Figure 2 details the transformer internals. The ST-Transformer decoder comprises _L_ = 24 identical blocks, each applying factorized spatial and temporal attention followed by a feedforward network. This factorization reduces complexity from _O_ ( _T_<sup>2</sup> _S_<sup>2</sup> ) for joint spatiotemporal attention to _O_ ( _TS_<sup>2</sup> + _T_<sup>2</sup> _S_ ). 

**ST-Block Structure** Each ST-Block contains three sub-layers applied in sequence: spatial self-attention across all _S_ + 1 tokens within each frame, temporal selfattention across all _T_ frames for each spatial position, and a position-wise feed-forward network. 

_Spatial Self-Attention._ Given input **X** _∈_ R<sup>_B×T ×_(</sup><sup>_S_+1)</sup><sup>_×D_</sup> , spatial attention operates independently on each frame. The input is first reshaped to ( _BT, S_ + 1 _, D_ ): 


Standard multi-head self-attention is applied: 


In spatial attention, the control token (at position 0) attends to and is attended by all video tokens (positions 1 to _S_ ), enabling action-video interaction within each frame. 

5 

_Temporal Self-Attention with Causal Masking._ For temporal attention, the tensor is reshaped to ( _B_ ( _S_ + 1) _, T, D_ ): 

**X** temporal = reshape( **X**<sup>_′_</sup> spatial<sup>_,_(</sup><sup>_B_(</sup><sup>_S_+ 1)</sup><sup>_, T, D_))</sup> (33) Causal self-attention is applied with a lower-triangular attention mask: 

**X**<sup>_′_</sup> temporal<sup>=</sup><sup>**X**temporal+CausalSelfAttn(</sup><sup>**X**temporal)(34)</sup> 

The causal mask ensures that tokens at time _t_ can only attend to tokens at times _≤ t_ : 


**Self-Attention Mechanism** The self-attention operation computes queries, keys, and values through linear projections: 


Multi-head attention splits these into _Nh_ = 8 heads with dimension _dk_ = _D/Nh_ = 32: 


The heads are concatenated and projected: 

MultiHead( **X** ) = Concat(head1 _, . . . ,_ head _Nh_ ) **W** _O_ (40) 

_QK-Normalization._ Layer normalization is applied to queries and keys before computing attention scores: 


This stabilizes training, particularly for large models. _µP Scaling._ When using maximal update parameterization <u>(</u> _<u>µ</u>_ P), attention logits are scaled by 8 _/dk_ instead of 1 _/_<sup>_~~√~~_</sup> _dk_ : 


This ensures consistent training dynamics across model widths. 

**Feed-Forward Network** The feed-forward network consists of two linear transformations with GELU activation: 

FFN( **x** ) = **W** 2 _·_ Dropout (GELU( **W** 1 **x** + **b** 1))+ **b** 2 (44) 

The hidden dimension is _D_ ff = 4 _D_ = 1024 (controlled by mlp_ratio = 4 _._ 0). 

The complete ST-Block forward pass is: 


**Attention Pattern Analysis** Spatial attention is bidirectional within each frame: the control token **C** _t_ attends to all video tokens _{_ **x** _t,_ 1 _, . . . ,_ **x** _t,S}_ , and each video token **x** _t,s_ attends to both the control token and all other video tokens in frame _t_ . No causal mask is applied. 

Temporal attention enforces causality across frames. Each position attends only to the same position at earlier times: the control token at time _t_ aggregates _{_ **C** 0 _, . . . ,_ **C** _t}_ ; the video token at position _s_ and time _t_ attends to _{_ **x** 0 _,s, . . . ,_ **x** _t,s}_ . The causal mask prevents information flow from future frames. 

#### **3.2.5 MaskGIT: Masked Generative Image Transformer** 

**Training Objective** The model is trained using a masked language modeling objective adapted for visual tokens. During training, a subset of future frame tokens is masked, and the model predicts the original tokens. 

**Masking Strategy** Given a sequence of _T_ frames, the first _Th_ frames serve as context (history), and the remaining _Tf_ = _T −Th_ frames are candidates for masking. For each training sample, a corruption strategy is applied: 

_Case 1: Standard MLM Masking._ With probability 1 _− ρ_ non-mlm, the model applies per-frame masking. For each frame _t >_ 0, a mask probability _pt_ is sampled from a cosine schedule: 


Each spatial position ( _h, w_ ) is then independently masked with probability _pt_ : 


_Case 2: Autoregressive-Style Masking._ With prob= ability _ρ_ non-mlm 0 _._ 5, the model instead applies autoregressive-style masking. A boundary frame _t_<sup>_∗_</sup> _∼_ Uniform _{Th, . . . , T −_ 1 _}_ is sampled; frames _{_ 0 _, . . . , t_<sup>_∗_</sup> _−_ 1 _}_ remain fully unmasked while frames _{t_<sup>_∗_</sup> _, . . . , T −_ 1 _}_ undergo progressive corruption with increasing noise. 

**Random Token Corruption** Prior to masking, tokens may be randomly corrupted: 


where _r_ = 0 _._ 2 is the maximum corruption rate and _u ∼_ Uniform(0 _,_ 1) is sampled per batch. 

**Loss Computation** _Video Token Prediction Loss._ The model outputs logits for each factored vocabulary: 


6 

These are reshaped to ( _K, Vf_ ) and cross-entropy loss is computed for each factored vocabulary: 


where _M_ is the set of masked positions. 

_Contact Prediction Loss._ A separate output head predicts contact maps: 


The contact loss uses the same factorized cross-entropy: 


_Joint Angle Prediction Loss._ Joint angles are predicted from the control token embedding: 


where **C**<sup>_′_</sup> _t_<sup>isthecontroltokenoutputfromthetrans-</sup> former. 

_Confidence Estimation._ For factorized tokens, confidence is the product of probabilities across vocabularies: 


Two unmasking modes are implemented: _greedy_ selects tokens with highest confidence; _random_ samples uniformly and is applied during training to mitigate exposure bias. 

#### **3.2.6 Video Decoder** 

**Decoder Architecture** The decoder mirrors the encoder, mapping quantized latents to RGB images. Given quantized features **e** ˆ _∈{−_ 1 _,_ +1 _}_<sup>_Cz×h×w_</sup> , an initial 3 _×_ 3 convolution projects to _C_ base _·_ 4 channels, followed by mid-block residual layers. Upsampling stages apply residual blocks with channel multipliers (4 _,_ 2 _,_ 2 _,_ 1 _,_ 1) in reverse order. The output projection applies group normalization and Swish activation before a 3 _×_ 3 convolution produces three RGB channels. 

The joint loss is mean squared error over future frames: 


_Total Loss._ The total training loss is: 


with _λ_ contact = 2 _._ 0 and _λ_ joint = 1 _._ 0. 

**Inference: Iterative Decoding** During inference, future frames are generated autoregressively, with each frame decoded using iterative parallel decoding. 

_Autoregressive Frame Generation._ For each future frame _t ∈{Th, . . . , T −_ 1 _}_ , the model initializes all tokens as mask tokens, applies MaskGIT iterative decoding for _N_ steps iterations, and then uses the predicted tokens as context for subsequent frames. 

_MaskGIT Iterative Decoding._ Within each frame, tokens are unmasked iteratively using a cosine schedule: 

#### **Algorithm 1** MaskGIT Decoding for Frame _t_ 

|1:|Initialize: **z**<sup>(0)</sup><br>_t_<br>_←_**z**mask (all positions masked)|
|---|---|
|2:|**for** _i_= 0 to _N_steps_−_1 **do**<br>|
|3:|Compute logits: **_ℓ_**=_fθ_(**z**_<t,_**z**<sup>(</sup><sup>_i_)</sup><br>_t _<sup>_,_</sup><sup>**a**</sup><sup>_,_</sup><sup>**_θ_**)</sup>|
|4:|Sample tokens: ˆ**z**_t ∼_Categorical(softmax(**_ℓ_**_/τ_))<br>|
|5:|Compute confidences: _cs_ = <sup>�</sup><br>_k _<sup>_p_(ˆ</sup><sup>_z_(</sup><sup>_k_)</sup><br>_t,s _<sup>_|_</sup><sup>**_ℓ_**)</sup><br>|
|6:|Compute mask ratio: _γ_ = cos( <sup>_π_</sup><br>2 <sup>_·_</sup><br>_i_+1<br>_N_steps <sup>)</sup>|
|7:|Number to mask: _n_=_⌈γ · S⌉_|
|8:|Select _n_ positions with lowest confidence to remain<br>masked<br>|
|9:|Update: **z**<sup>(</sup><sup>_i_+1)</sup><br>_t_<br>, keeping high-confidence predictions|
|10: <br>11:|**end for**<br> **return z**<br>(_N_steps)<br>_t_|


**Upsampling Operation** Spatial resolution is increased using depth-to-space (pixel shuffle) operations: 

Upsample( **h** ) = DepthToSpace(Conv3 _×_ 3( **h** ; 4 _C_ ) _,_ block_size = 2) (59) This rearranges a tensor of shape ( _B,_ 4 _C, H, W_ ) to ( _B, C,_ 2 _H,_ 2 _W_ ). 

**Token-to-Latent Mapping** Given predicted token indices _z ∈{_ 0 _, . . . , V −_ 1 _}_ , the decoder recovers the continuous latent representation via the inverse FSQ dequantization operation. This produces a tensor **e** _∈_ R<sup>_C×h×w_</sup> with _C_ = 6 channels, which is then passed to the decoder network for image reconstruction. The inverse Haar wavelet transform is applied during decoding to upsample the spatial resolution by a factor of 4. 

**Factorization Strategy** For computational efficiency during training and inference, token indices are factorized into _K_ = 2 factors, each with vocabulary size _Vf_ = 256, such that _Vf_<sup>_K_</sup> = 65 _,_ 536 _≈ V_ . This reduces the output logit dimension from _V_ to _K · Vf_ and enables parallel prediction across factors. 

#### **3.2.7 Model Output Specification** 

**Forward Pass Outputs** During training, the forward pass returns the total loss _L_ and its components _L_ video, _L_ contact, _L_ joint, along with token-level accuracies on masked positions. The full logit tensor of shape ( _B, K · Vf , T, H, W_ ) is retained for downstream analysis. 

7 

**Generation Outputs** At inference, `generate()` returns predicted video token indices of shape ( _B, T · H · W_ ). Optional outputs include contact map tokens ( _B, Tf , H, W_ ), predicted joint angles ( _B, Tf , Nj_ ), and factored logits for uncertainty quantification. 

#### **3.2.8 Model Configuration** 

**Default Hyperparameters** The model uses _L_ = 24 transformer layers with hidden dimension _D_ = 256, _Nh_ = 8 attention heads (head dimension _dk_ = 32), FFN hidden dimension _D_ ff = 1024, temporal sequence length _T_ = 16, and spatial sequence length _S_ = 1024 (32 _×_ 32 tokens per frame). The image vocabulary size is _V_ = 65536, factorized into _K_ = 2 sub-vocabularies of size _Vf_ = 256 each. Joint angle inputs have _Nj_ = 4 channels. 

**Computational Complexity** Per ST-Block, spatial attention requires _O_ ( _BT_ ( _S_ +1)<sup>2</sup> _D_ ) operations while temporal attention requires _O_ ( _B_ ( _S_ +1) _T_<sup>2</sup> _D_ ) operations. For _L_ layers, the total complexity is: 


With default parameters ( _T_ = 16, _S_ = 1024, _D_ = 256, _L_ = 24), this is approximately _O_ (10<sup>11</sup> ) operations per forward pass for batch size 1. 

_Parameter Count._ The model contains approximately: 

Params _≈ L·_ (12 _D_<sup>2</sup> +8 _D_<sup>2</sup> )+ _Vf ·K ·D_ + _T ·_ ( _S_ +1) _·D_ (61) yielding roughly 30-50M parameters depending on configuration. 

### **3.3 Online World Model Evaluation in the Planning Loop** 

#### **3.3.1 Coupling ChronoDreamer in Eval Simulation** 

During each evaluation cycle, ChronoDreamer aggregates a short history of camera frames, robot states, and executed actions, then feeds these sequences into the world model to predict next-step RGB observations and contact maps. The predicted futures, alongside the tiled history, are passed to an LLM judge that reasons about collision risk. 

The planner samples candidate actions and submits them to this LLM gate synchronously each world-model period; any action flagged as unsafe is resampled, up to a fixed maximum of three attempts. If all sampled actions are rejected, the controller falls back to a conservative retreat—commanding an upward ( _−Z_ ) motion—to clear the workspace before continuing. 

#### **3.3.2 LLM Collision Judge** 

The following prompt template elicits collision assessments from the LLM: 

```
LLM_PROMPT_TEMPLATE="""Doyouthinkthereisacollision
happeningbetweenthemanipulatorandanyoftheobjectsonthe
table?Thecameraismountedonthearmofthemanipulator.
Youareastrictcollisionverifier.
Youwillbeshown:
```

- `(1) History RGB frames (prompt)` 

- `(2) Predicted future RGB frames (generated)` 

```
(3)Predictedcontactmap(generated)–WARNING:thisisnoisy
andoftenhasfalsepositives.
TASK
```

```
Decideifacollisionhappensbetweenthemanipulator/gripper
andANYtableobject.
```

```
DEFINITION
```

```
Outputcollision_likely=trueONLYifBOTHaretrue:
```

```
(A)InthepredictedfutureRGBframes,thegripper/manipulator
makesphysicallyplausiblecontactwithanobject(notjust
overlapsin2D).
```

```
(B)AtleastoneofthefollowingisvisibleinRGB:
```

```
(B1)Theobjectmoves/rotates/shiftsrelativetothetable
```

```
(displacement)comparedtoitsposeinthelastpromptframe.
```

```
(B2)Theobjectdeforms/deflects/compressesatthecontactpoint
(commonforchains/FEA/deformables),evenifitsbaseposedoes
nottranslate.
```

- `(B3) There is sustained pushing/pressing contact across multiple future frames with no visible gap, even if the object is constrained/heavy and does not translate.` 

- `IMPORTANT RULES (to reduce false positives)` 

```
-DoNOTclaimcollisionbasedonlyonthecontactmap.The
contactmapcanbewrong.
```

- `If the gripper crosses over an object in the image in 2D but` 

- `there is a visible gap/clearance (no sustained contact), this is NOT a collision.` 

- `If you cannot clearly see contact evidence in the predicted` 

- `RGB frames (displacement, deformation/deflection, or sustained pressing contact), set collision_likely=false.` 

- `Lack of object translation does NOT imply "no collision" when` 

- `the object is constrained/heavy or deformable. In those cases, look for deformation/deflection or sustained pressing contact.` 

```
-Iftheyellowtableseemsbecomingsmaller,thislikelymeans
thearm/cameraisliftingupward;liftingmakescollisionless
likely.Prefercollision_likely=falseunlessthereisclear
contactevidence.
```

- `Only give high confidence (` _>_ `= 0.85) when contact evidence is` 

- `obvious and sustained across multiple future frames.` 

- `If evidence is ambiguous or blurred, set` 

- `collision_likely=false and confidence` _<_ `= 0.5. FEW-SHOT EXAMPLES (read carefully)` 

- `Example 1 (NO collision: high clearance pass-over) Predicted frames show the gripper moving "over" a block in 2D, but the block’s pose does not change relative to the table. Even if the contact map lights up near the block, answer:` 

```
{"collision_likely":false,"confidence":0.3,
"first_collision_frame":0,"explanation":"Gripperpasses
above/nearobject;novisibledisplacementinRGB."}
Example2(NOcollision:apparentmotionfromcamera
ego-motion)
```

```
Cameramoveswiththearm;objectsmayappeartoshiftslightly
duetoviewpointchanges.Iftheobjectremainsfixedrelative
totableedges/markersandthereisnoclearpush/impact,
answer:
```

```
{"collision_likely":false,"confidence":0.4,
"first_collision_frame":0,"explanation":"Noclearobject
displacement;apparentchangeslikelyfromcameramotion."}
Example3(YEScollision:clearpush)
```

```
Grippercontactsablockandtheblocktranslates/rotatesina
sustainedwayacrossmultiplefutureframes.Answer:
```

```
{"collision_likely":true,"confidence":0.9,
```

```
"first_collision_frame":1,"explanation":"Contactwith
sustainedobjectdisplacementvisibleinRGB."}
Example4(YEScollision:constrained/heavy/deformableobject)
```

```
Thegripperpressesintoachain/beam/deformableobjectandyou
canseebending/compression/deflectionatthecontactpoint,
eveniftheobjectdoesnottranslate.Answer:
{"collision_likely":true,"confidence":0.85,
```

```
"first_collision_frame":1,"explanation":"Sustainedpressing
contactwithvisibledeformation/deflectioninRGB."}
Inputs:
```

```
-Image1:historyRGBframes(prompt)
-Image2:predictedfutureRGBframes(generated)
-Image3:predictedfuturecontactmap(generated)
ReturnJSONonlywiththefollowingschema:
{
```

```
"collision_likely":true/false,
"confidence":0.0-1.0,
"first_collision_frame":0-7,
"explanation":"..."
}
"""
```

8 

Each episode (trajectory) is represented as 


## **4 Experiments** 

We evaluate on _DreamerBench_ , a simulator-generated dataset targeting frictional, contact-rich tabletop dynamics [11]. It complements DMControl [12], ALE [13], D4RL [14], RLBench [15], Open X-Embodiment [16], DrivingDojo [17], and WorldPrediction [18] by exposing dense contact supervision. 

### **4.1 Trajectory Generation and State Logging** 

Trajectories are generated using Project Chrono, configured as a multi-physics engine with rigid and (optionally) flexible bodies, Coulomb friction, and penalty-based or constraint-based contact handling. At a fixed simulation time step ∆ _t_ , the underlying continuous-time dynamics can be interpreted as a hybrid ODE/DAE system with a non-smooth right-hand side; DreamerBench records a discretized version of these dynamics suited for sequence modeling. 

At each simulation step _t_ , a state tuple 


is logged, together with a low-level action _at_ and, optionally, a task reward _rt_ , where: 

- _o_<sup>rgb</sup> _t_ collects RGB images from one or more cameras (e.g., ego and side views), at a resolution suitable for vector-quantized autoencoders. 

- _o_<sup>contact</sup> _t_ is a “contact splat” image: a workspacealigned grid that encodes the spatial footprint and magnitude of contact (e.g., approximated contact pressure). 

- _qt, q_ ˙ _t_ are robot joint positions and velocities, forming a proprioceptive observation channel. 

- _ft_<sup>contact</sup> aggregates per-contact 3D normal and tangential forces (either per contact point or grouped per body), corresponding to impulses in non-smooth mechanics discretized over ∆ _t_ . 

- _µt_ denotes scalar or per-body friction coefficients used by the contact model (e.g., static and kinetic coefficients ( _µ_ s _, µ_ k)), enabling variation of friction regimes. 

- _ct_ is a discrete contact-mode flag (no contact, sticking, sliding, separating), which can be interpreted as a latent discrete state in a hybrid latent variable model. 

with horizon _T_ chosen so that objects undergo multiple contact mode transitions (impact, stick–slip, rolling, and settling). This setting is suitable for evaluating longhorizon rollout stability of world models under hybrid dynamics. Episodes last 300–600 steps to capture multiple stick–slip transitions. 

### **4.2 Simulation Scenarios** 

Each scenario— `flashlight-box` , `flashlight-coca` , `waterbottle-coca` , and `fea-flashlight` —provides synchronized RGB views, contact splat images, proprioception, low-level actions, and physics annotations (forces, friction coefficients, mode flags), and vector-quantized latents are pre-computed so that token-based models avoid repeated encoding. The domains are deliberately non-smooth: transition kernels switch whenever contacts appear or disappear, friction regimes change, or rolling transitions to sticking. Table 1 illustrates the four scenarios with example RGB and contact-splat images. 

**File organization and pre-computed latents.** On disk, DreamerBench is organized into scenario-specific archives (e.g., `flashlight_box_00.zip` ), each containing multiple episodes and auxiliary files: 

- arrays for RGB and contact-splat images, proprioception, actions, and physics annotations; 

- pre-computed discrete visual tokens **z** _t ∈{_ 0 _, . . . , K −_ 1 _}_<sup>_S_</sup> for RGB and contact streams, obtained from a vector-quantized autoencoder and stored in binary files (e.g., `video.bin` , `contact_splat.bin` ); 

- metadata (JSON) describing token grid size _S_ , codebook size _K_ , frame count, frame rate, and segmentation into episodes. 

This layout is compatible with common training stacks (PyTorch, JAX) that either stream episodes as variablelength sequences or treat the dataset as a concatenated sequence with associated _segment IDs_ . “Contact splat” images are generated with the encoder in Section 3.1 and stored alongside tokenized latents **z** _t_ plus metadata for streaming. 

### **4.3 Stochastic Joystick Excitation via an Ornstein–Uhlenbeck Process** 

To generate temporally correlated yet nontrivial endeffector motion for data collection, and to excite rich contact behaviors, the joystick command channel in _DreamerBench_ is driven by an Ornstein–Uhlenbeck (OU) process. The OU process is a stationary Gaussian Markov process originally introduced as a mean-reverting model 

9 

Table 1: Simulation scenarios in DreamerBench with example RGB and contact-splat images. 

|Scenario|Description|Ego camera|Side camera 0|Contact-splat<br>image|
|---|---|---|---|---|
|`flashlight box`|Tool interacting with a box on a planar<br>surface with sliding and pushing.||||
|`flashlight coca`|Tool interacting with a tall cylindrical<br>container with sliding and rolling contact.||||
|`waterbottle coca`|Bottle–cylinder interaction with combined<br>sliding and rolling along the table.||||
|`fea flashlight`|Four tetrahedron-defined FEA beams and<br>two standing flashlights represented as<br>rigid bodies.||||


for Brownian velocity fluctuations [19]. In continuous time, a _d_ -dimensional OU process _Xt ∈_ R<sup>_d_</sup> satisfies the Langevin-type stochastic differential equation 


where _θ >_ 0 is the mean-reversion rate, _µ ∈_ R<sup>_d_</sup> is the long-term mean, _σ >_ 0 is the diffusion scale, and _Wt_ is _d_ - dimensional standard Brownian motion. The process has an exponential autocorrelation function with correlation time _τc_ = 1 _/θ_ and a Gaussian stationary distribution; efficient numerical schemes for OU trajectories and related functionals are standard in the SDE literature [20]. 

OU noise is widely used in continuous-control reinforcement learning as a model of colored action noise, in particular to drive exploration in physical systems with inertia without introducing unrealistically high-frequency jitter [21, 22]. Here, the same construction is used not for exploration during learning, but to synthesize joysticklike excitation that repeatedly engages contact, sliding, and rolling during data collection. We instantiate a threedimensional OU process 


representing a latent control signal over Cartesian directions ( _x, y, z_ ) in the workspace of the robot arm. 

The implementation mirrors an Euler–Maruyama discretization of (64) with time step ∆ _t_ , 


After each update (66), the process state is postprocessed before being interpreted as a joystick command. First, a minimum-magnitude constraint is applied: letting _mk_ = _∥Xk∥_ 2 and denoting a threshold _m_ min _>_ 0, the state is rescaled according to 


where _v_ is a random unit vector. This step enforces a lower bound on the norm of _Xk_ while preserving the 

10 

current direction whenever possible, avoiding extended intervals of near-zero actuation. 

Next, each component is passed through a deadzone and mapped to a Cartesian increment. For component _X_<sup>(</sup><sup>_i_)</sup> _k_<sup>,athreshold</sup><sup>_ε >_0isapplied:</sup> 


and the resulting vector updates the end-effector position: 

where _v_ scale is a scalar step size and Π _P_ denotes component-wise clipping to a predefined axis-aligned workspace box _P_ . The updated target position _pk_ +1 is then passed to an inverse kinematics solver, which produces joint angles applied to the robot at the control rate. 

Overall, the joystick control law in _DreamerBench_ can be viewed as an OU-driven colored-noise excitation filtered through a norm constraint, a deadzone nonlinearity, and a constrained kinematic integrator. This construction yields temporally coherent, reproducible stochastic motion that systematically excites contact-rich interactions while avoiding degenerate trajectories with negligible motion, and it admits straightforward ablations (e.g., modifying _τc_ or replacing OU noise with i.i.d. Gaussian noise) for future studies. This colored-noise excitation consistently drives sliding, rolling, and intermittent sticking without degenerating into near-static trajectories. 

## **5 Results** 

### **5.1 Ablations Studies** 

We are actively working on ablation studies to understand the scaling and the of the performance of different network sizes with number of tasks trained on. We will report the results here soon. Due to very limited compute resources, we have not been able to run these experiments yet. 

### **5.2 Qualitative Analysis** 

A qualitative analysis has been conducted by human to gain understanding on the model performance after training for 4 epochs using the following parameters. 

We have noticed the spatial and object coherence, the objects’ relative positions on the table, can be preserved easily by the model, across multiple scenarios, when contact has not happened. Examples have been provided in Figure 3. The spatial coherence is a combination of camera rendering and positioning, lower level inverse kinematic controller, and multibody dynamics physics. 

Figures 4a and 4b show cases in which a contact happens between the end-effector and an object on the table. The model is able to predict the contact event and generate corresponding contact splat frames. However, the 

predicted video and camera frames tend to show artifacts and blurriness after contact happens, and certain spatial coherence is lost. This behavior is quite consistent cross multiple scenarios, tasks, and given prompts. This might be an indication that the current DreamerBench dataset does not contain enought contact-rich data, as indeed due to the natural of action sampling and simulation setup, contact events take a relatively small portion of the entire dataset. 

## **6 Discussion** 

Qualitatively, the trained world model is capable of deducing possible collision in most cases. We have noticed prompt engineering is the key to guide llm to generate correct collision flags. An example correct reasoning case is shown below, Gemma-3-27b-it from Google Gemini family is used for the example rasoning: 

Figure 5a and Figure 5b show two consecutive action sampling at the same time stamp, this example case shows the action sampling associated with attempt 0, in Figure 5a, with an llm reasoning giving a collision confidence of 0.95, would result in a collision. Then, the system moved on to perform a resampling and the world model predicted the rollout in attempt 1, with the generated frame and contact, the world model predicted a collision confidence of 0.3, decided the action sampling is categorized as safe. In this example case, in Figure 5a, the world model correctly identified a collision case where the manipulator pushes the deformable object towards the edge of the table. The generated frames depict the movement of the deformable object being pushed by the manipulator. In Figure 5b, the world model recognized a non-collision case where the manipulator lifts up and moves away from both the table and the deformable object. The generated frames effectively illustrate this movement. 

The llm reasonings for both of these attempts are shown below: 

For attempt 0 (Collision Case) - Response: 

```
Attempt0(CollisionCase)-GeminiResponse:
{
"collision_likely":true,
"confidence":0.95,
"first_collision_frame":4,
"explanation":"Thegrippervisiblycontactsthesmall
cylindricalobjectandpushesittotherightacrossmultiple
futureframes.CleardisplacementisvisibleintheRGB
images."
}
```

```
Model:gemma-3-27b-it
PromptTokenCount:760(TEXT)+774(IMAGE)=1534total
TotalTokenCount:1534
ResponseID:r8FEaceAGsG-_uMPrtOugQc
```

For attempt 1 (Non-Collision Case) - Response: 

11 

```
Attempt1(Non-CollisionCase)-GeminiResponse:
{
```

```
"collision_likely":false,
"confidence":0.3,
"first_collision_frame":0,
"explanation":"Gripperapproachesobjectbutnovisible
displacementoftheobjectisobservedinthepredictedRGB
frames.Apparentchangescouldbeduetocameramotion."
}
```

```
Model:gemma-3-27b-it
PromptTokenCount:760(TEXT)+774(IMAGE)=1534total
TotalTokenCount:1534
ResponseID:ysFEaaOaL7iv_uMP2PX-yAg
```

## **7 Future Work** 

The current version of ChronoDreamer shows good generalization across multiple different scenarios and tasks. So far, only random excitation has been used for simulation evaluation, we reported qualitative success to prevent potential collision in a random OU action sampling setting. In the future, we plan to integrate ChronoDreamer with a model predictive controller (MPC) or VLA to perform closed-loop control for specific tasks, such as reaching a target position while avoiding collisions with objects. Based on the current results using a small network, world model has already shown its capability for hazard prevention and can potentially increase controller success rate. 


Figure 2: ST-Transformer architecture. Control tokens (action + joint embeddings) are concatenated with video tokens and processed by _N_ axial ST-Blocks. Three output heads: joint regression (MSE), contact tokens, and video tokens (factorized CE). 

12 


Figure 3: Spatial coherence in non-contact scenarios ( `fea_flashlight` ). Row 1: prompt; Rows 2–3: predicted RGB; Rows 4–5: predicted contact splat. Time progresses left to right. 


Figure 4: Predictions during contact events. Layout as in Fig. 3. Post-contact frames exhibit increased blurriness. 


(a) Collision detected (conf. 0.95): manipulator pushes object toward table edge. 


(b) No collision (conf. 0.3): manipulator lifts away from table. 

Figure 5: Consecutive action samples at the same timestep. LLM judge rejects attempt 0, accepts attempt 1. 

13 

## **References** 

- [1] Ha, D., and Schmidhuber, J., 2018. World models. 

- [2] Le Guen, V., and Thome, N., 2020. “Disentangling physical dynamics from unknown factors for unsupervised video prediction”. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 11474–11484. 

- [3] Liu, S., Ren, Z., Gupta, S., and Wang, S., 2024. “Physgen: Rigid-body physics-grounded image-tovideo generation”. In European Conference on Computer Vision (ECCV). OpenAccess version. 

- [4] Zhang, K., Xiao, C., Xu, J., Mei, Y., and Patel, V. M., 2025. Think before you diffuse: Infusing physical rules into video diffusion. 

- [5] Hao, Y., Chen, C., Mian, A. S., Xu, C., and Liu, D., 2025. Enhancing physical plausibility in video generation by reasoning the implausibility. 

- [6] Jang, S., Ki, T., Jo, J., Yoon, J., Kim, S. Y., Lin, Z., and Hwang, S. J., 2025. Frame guidance: Trainingfree guidance for frame-level control in video diffusion models, June. 

- [7] Higuera, C., Dong, S., Boots, B., and Mukadam, M., 2022. “Neural contact fields: Tracking extrinsic contact with tactile sensing”. _arXiv preprint arXiv:2210.09297_ . 

- [8] Kim, L., Li, Y., Posa, M., and Jayaraman, D., 2023. “Im2contact: Vision-based contact localization without touch or force sensing”. In Proceedings of The 7th Conference on Robot Learning, Vol. 229 of _Proceedings of Machine Learning Research_ , PMLR, pp. 1533– 1546. 

- [9] Wu, L., Yu, C., Ren, J., Chen, L., Huang, R., Gu, G., and Li, H., 2025. “Freetacman: Robot-free visuo-tactile data collection system for contact-rich manipulation”. _arXiv preprint arXiv:2506.01941_ . 

   - [13] Bellemare, M. G., Naddaf, Y., Veness, J., and Bowling, M., 2013. “The arcade learning environment: An evaluation platform for general agents”. _Journal of Artificial Intelligence Research,_ **47** , pp. 253–279. 

   - [14] Fu, J., Kumar, A., Nachum, O., Tucker, G., and Levine, S., 2020. “D4RL: Datasets for deep datadriven reinforcement learning”. _arXiv preprint arXiv:2004.07219_ . 

   - [15] James, S., Ma, Z., Arrojo, D. R., and Davison, A. J., 2020. “RLBench: The robot learning benchmark & learning environment”. _IEEE Robotics and Automation Letters,_ **5** (2), pp. 3019–3026. 

   - [16] Open X-Embodiment Collaboration, 2023. “Open x-embodiment: Robotic learning datasets and RT-X models”. _arXiv preprint arXiv:2310.08864_ . 

   - [17] Wang, Y., et al., 2024. “DrivingDojo dataset: Advancing interactive and knowledge-enriched driving world models”. _arXiv preprint arXiv:2410.10738_ . 

   - [18] Chen, D., Chung, W., Bang, Y., Ji, Z., and Fung, P., 2025. “Worldprediction: A benchmark for highlevel world modeling and long-horizon procedural planning”. _arXiv preprint arXiv:2506.04363_ . 

   - [19] Uhlenbeck, G. E., and Ornstein, L. S., 1930. “On the theory of the brownian motion”. _Physical Review,_ **36** (5), pp. 823–841. 

   - [20] Gillespie, D. T., 1996. “Exact numerical simulation of the ornstein–uhlenbeck process and its integral”. _Physical Review E,_ **54** (2), pp. 2084–2091. 

   - [21] Lillicrap, T. P., Hunt, J. J., Pritzel, A., Heess, N., Erez, T., Tassa, Y., Silver, D., and Wierstra, D., 2015. “Continuous control with deep reinforcement learning”. _arXiv preprint arXiv:1509.02971_ . 

   - [22] Hollenstein, J., Auddy, S., Saveriano, M., Renaudo, E., and Piater, J., 2022. “Action noise in off-policy deep reinforcement learning: Impact on exploration and performance”. _Transactions on Machine Learning Research_ . Available at arXiv:2206.03787. 

- [10] Cong, X., Xing, A., Pokhariya, C., Fu, R., and Sridhar, S., 2025. “Dytact: Capturing dynamic contacts in hand-object manipulation”. _arXiv preprint arXiv:2506.03103_ . 

- [11] Zhou, J., 2025. Dreamerbench: Dataset for evaluating world models under frictional, contact-rich dynamics. `https://huggingface.co/datasets/ zzhou292/DreamerBench` . Accessed: 2025-11-27. 

- [12] Tassa, Y., Doron, Y., Muldal, A., Erez, T., Li, Y., de Las Casas, D., Budden, D., Abdolmaleki, A., Merel, J., Lefrancq, A., Lillicrap, T., and Riedmiller, M., 2018. “Deepmind control suite”. _arXiv preprint arXiv:1801.00690_ . 

14 

