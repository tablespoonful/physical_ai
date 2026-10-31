---
title: "MoReFlow: Motion Retargeting Learning through Unsupervised Flow Matching"
date: "2025-09-29"
authors: "Wontaek Kim; Tianyu Li; Sehoon Ha"
venue: "Submitted to ICLR 2026"
url: https://arxiv.org/abs/2509.25600
pdf: https://arxiv.org/pdf/2509.25600
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.25600)** / [論文ページ](https://arxiv.org/abs/2509.25600)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Arxiv Version 

# MOREFLOW: MOTION RETARGETING LEARNING THROUGH UNSUPERVISED FLOW MATCHING 

**Wontaek Kim, Tianyu Li**<sup>*****</sup> **, Sehoon Ha**<sup>*****</sup> 

Georgia Institute of Technology Atlanta, GA 30332, USA _{_ wkim345,tli471,sehoonha _}_ @gatech.edu 

## ABSTRACT 

Motion retargeting holds a premise of offering a larger set of motion data for characters and robots with different morphologies. Many prior works have approached this problem via either handcrafted constraints or paired motion datasets, limiting their applicability to humanoid characters or narrow behaviors such as locomotion. Moreover, they often assume a fixed notion of retargeting, overlooking domainspecific objectives like style preservation in animation or task-space alignment in robotics. In this work, we propose **MoReFlow** , Motion Retargeting via Flow Matching, an unsupervised framework that learns correspondences between characters’ motion embedding spaces. Our method consists of two stages. First, we train tokenized motion embeddings for each character using a VQ-VAE, yielding compact latent representations. Then, we employ flow matching with conditional coupling to align the latent spaces across characters, which simultaneously learns conditioned and unconditioned matching to achieve robust but flexible retargeting. Once trained, **MoReFlow** enables flexible and reversible retargeting without requiring paired data. Experiments demonstrate that **MoReFlow** produces highquality motions across diverse characters and tasks, offering improved controllability, generalization, and motion realism compared to the baselines. 

## 1 INTRODUCTION 

Motion retargeting has been the fundamental problem of adapting motions performed by one actor to another with different morphology, such as transferring a human motion sequence to a virtual avatar or a humanoid robot. It holds the premise of an enriched dataset for virtual characters or robots by reducing the cost of content creation in animation and gaming, enabling robots to learn practical skills from human demonstrations, and supporting cross-actor motion analysis in biomechanics. Despite its diverse applications, the central challenge remains the same: establishing a reliable correspondence between the motion spaces of different characters while respecting different kinematic and dynamic capabilities. 

Motion retargeting has been studied with diverse approaches, such as optimization methods with handcrafted constraints (Zakka, 2025; Choi & Ko, 2000), reinforcement learning (Reda et al., 2023), and learning-based mappings between characters (Villegas et al., 2021). However, most methods remain restricted to the same human morphologies (Aberman et al., 2020; Aigerman et al., 2022). While some recent works tackle motion retargeting between heterogeneous morphologies, such as human-to-quadruped (Li et al., 2024b;a), they are often limited to locomotion tasks. Moreover, existing approaches typically assume a fixed notion of retargeting. In practice, the objective of the retargeting may vary: motion retargeting in animation often means joint-space alignment to preserve style, while robotics applications may require task-space alignment to achieve functional goals. These limitations call for a more general and adaptable retargeting framework. 

In this work, we propose **MoReFlow** , Motion Retargeting via Flow Matching, an unsupervised framework for learning motion retargeting across heterogeneous characters. Specifically, **MoReFlow** formulates the retargeting problem as constructing a correspondence between the motion spaces of two characters using Flow Matching. The framework consists of two stages: pretraining a motion tokenizer and learning motion correspondence via codebook flow. In the first stage, we 

1 

Arxiv Version 


Figure 1: **MoReFlow** enables diverse source motions to be retargeted across different target characters with controllable outcomes. The source motions include both dynamic whole-body movements and fine-grained manipulation tasks. The target characters range from smaller humanoid robots to morphologically distinct platforms such as Spot. Our framework can generate multiple retargeted variations to accommodate different user preferences. 

train tokenized motion embeddings for each character using a VQ-VAE (Van Den Oord et al., 2017), which yields a compact motion representation together with a motion encoder and decoder. In the second stage, **MoReFlow** employs guided flow matching to establish correspondences between the latent spaces of different characters. At inference, the source character’s motion is encoded into a latent vector, translated into the target character’s latent vector through the learned flow, and then reconstructed by the target character’s decoder. Our unsupervised framework employs conditional coupling to handle large unpaired datasets, where it guides the flow to minimize geodesic distances in the feature space between samples. 

We conduct extensive experiments covering humanoid and non-humanoid robots to validate our framework. Our main results show that **MoReFlow** can retarget diverse dynamic human motions—including locomotion, sports, and gestural actions—to new characters such as the smaller Booster T1 humanoid and the Spot quadruped with a manipulator (Figure 1). The retargeted motions not only preserve the style and semantics of the source but also adapt naturally to the target morphology. Furthermore, our framework enables condition-dependent control, producing multiple valid outcomes from the same source motion depending on whether the alignment is defined in local or world coordinates in real time. Compared to the baseline methods, **MoReFlow** achieves better motion quality while offering a higher degree of controllability in cross-morphology retargeting. Finally, our ablation studies analyze the effects of various factors, such as different embedding designs and motion dataset volume. 

In summary, our contributions are as follows: 

- We introduce **MoReFlow** , a novel unsupervised framework for cross-morphology motion retargeting that leverages flow matching in tokenized motion spaces. It enables retargeting without paired data and supports reversible and modular mappings between characters. 

- We show that the proposed framework can generate different motion retargeting results under various conditions, such as local style alignment or world-frame task alignment, which offer users interactive, fine-grained control. 

- We validate the effectiveness of the proposed approach through extensive experiments. The results demonstrate that **MoReFlow** achieves controllable, high-quality motion retargeting that preserves semantic intent and outperforms baseline methods in both motion fidelity and controllability. 

2 

Arxiv Version 

## 2 RELATED WORK 

### 2.1 MOTION RETARGETING 

Motion retargeting methods can be broadly divided into two categories: _homo-morphology_ methods, where source and target share the same skeletal topology but differ in proportions or geometry, and _cross-morphology_ methods, where source and target differ fundamentally in skeletal structure. 

**Homomorphology Motion Retargeting.** Early learning-based approaches such as Neural Kinematic Networks (NKN) (Villegas et al., 2018) and Skeleton-Aware Networks (Aberman et al., 2020) pioneered unsupervised retargeting by incorporating kinematic layers and graph-structured features. Subsequent work extended these ideas to improve realism and robustness, for example through residual perception modules (Zhang et al., 2023b), contact- and geometry-aware constraints (Villegas et al., 2021), or correspondence-free streaming models for online transfer (Rekik et al., 2024). More recent studies leverage skeleton-agnostic embeddings and canonical templates to generalize across characters (Lee et al., 2023; Zhang et al., 2024), while generative approaches such as diffusion and collision-aware frameworks further enhance plausibility (Cao et al., 2025; Martinelli et al., 2024). In robotics, optimization-based methods such as MINK (Zakka, 2025) provide inverse-kinematics baselines for retargeting motions from human datasets to humanoid robots like NAO, Atlas, and Valkyrie. 

**Cross-Morphology Motion Retargeting.** Retargeting across characters with different skeletal structures requires bridging more substantial morphological gaps. Adversarial correspondence embedding (ACE) (Li et al., 2023), phase-manifold alignment (Li et al., 2024a), and reinforcement learning frameworks such as CrossLoco (Li et al., 2024b) have been proposed to transfer human motions to quadrupeds and robots. Broader frameworks such as BuddyImitation (Li et al., 2025) extend retargeting to interaction skills by modeling relational dynamics. Other studies address human-toquadruped transfer via imitation learning or hierarchical controllers (Kim et al., 2022; Yoon et al., 2024), while optimization-based approaches such as differentiable optimal control (DOC) exploit model predictive control for legged robots (Grandia et al., 2023). Unsupervised latent alignment methods (Yan et al., 2023; Mourot et al., 2023) and generative approaches (Cao et al., 2025) further demonstrate the diversity of strategies for handling structural mismatches in cross-embodiment motion retargeting. 

### 2.2 FLOW MATCHING AND GENERATIVE FLOWS 

Flow matching has recently emerged as a powerful alternative to diffusion models for generative modeling. Unlike diffusion, which relies on stochastic denoising processes, flow matching trains continuous normalizing flows by regressing vector fields along probability paths, offering both simulation-free training and efficient sampling (Lipman et al., 2022). The method has since been applied across a wide range of modalities, including image and video generation, audio synthesis, and text modeling (Lipman et al., 2024), with theoretical analyses highlighting its equivalence to Gaussian diffusion processes (Gao et al., 2024). More recently, flow matching has been adapted to motion domains. Hu et al. (2023) introduced Motion Flow Matching for efficient human motion generation and editing, while Cuba et al. (2025) extended the framework with conditional targetpredictive flows to reduce temporal jitter in text-to-motion tasks. These works highlight the versatility of flow matching and motivate its use in our framework, where efficient and controllable latent-space alignment is central to motion retargeting. 

## 3 MOTION RETARGETING VIA FLOW MATCHING 

Our framework, **MoReFlow** addresses motion retargeting by learning a correspondence between the motion spaces of different characters in an unsupervised manner. An overview of the method is presented in Figure 2. The method consists of two main stages. In the first stage, we construct compact motion embeddings for each character using a vector-quantized variational autoencoder (VQ-VAE). This tokenized representation provides a discrete latent space that captures motion patterns while discarding low-level redundancy. In the second stage, we employ flow matching to learn a transformation between the latent spaces of different characters. By combining these two stages, 

3 

Arxiv Version 


Figure 2: Overview of the proposed MoReFlow framework. Each character (C<sup>src</sup> and C<sup>tgt</sup> ) has a pretrained VQ-VAE tokenizer consisting of an encoder, a decoder, and a codebook. A source motion is first encoded and quantized into tokens from the source codebook. The flow matching model then maps the token distribution from the source codebook to the target codebook, optionally conditioned on task requirements, such as local style alignment or world-frame alignment. The retargeted motion is reconstructed using the pretrained target decoder. 

**MoReFlow** enables flexible motion retargeting across characters with different morphologies. Once trained, the framework supports diverse retargeting outcomes under different conditions, such as local style preservation or task-space alignment, and can also perform retargeting in reverse without requiring additional models. 

### 3.1 PRETRAINED MOTION TOKENIZER 

Directly performing motion retargeting in raw trajectory space is difficult because motion sequences are high-dimensional and redundant. To simplify the problem, we construct a compact tokenized representation of motion using a VQ-VAE inspired by T2M-GPT (Zhang et al., 2023a). Each input motion frame is represented as _xt_ = [ _pt_ ; _rt_ ; _vt_<sup>root</sup> ] where _pt_ and _rt_ denote joint positions and rotations, and _vt_<sup>root</sup> denotes the root velocity at frame _t_ . Instead of encoding single frames, we partition the sequence into overlapping motion chunks of length _H_ . Each chunk _xt_ : _t_ + _H−_ 1 = _{xt, . . . , xt_ + _H−_ 1 _}_ is processed by an encoder _Eθ_ that produces a latent feature 


The latent vector is quantized using a codebook _E_ = _{e_ 1 _, . . . , eK}_ of _K_ embeddings. Each _zt_ is replaced by its nearest entry and the decoder _Dϕ_ reconstructs the motion chunk from quantized tokens: 


The model is trained with the standard VQ-VAE objective that consists of three terms: reconstruction loss _L_ rec, codebook loss _L_ code and commitment loss _L_ commit: 


where sg[ _·_ ] denotes the stop-gradient operator and _β_ is a weighting coefficient. This process yields a sequence of motion tokens that capture essential spatiotemporal patterns while discarding redundancy. This discrete latent representation provides a compact and structured space that simplifies learning correspondences across characters via flow matching. For each character, we train an individual set of an encoder, a decoder and a codebook. 

### 3.2 MOTION RETARGETING VIA CODEBOOK FLOW 

Once motion embeddings are obtained, we perform retargeting entirely in the latent space of motion tokens. Given a source motion _x_<sup>src</sup> _t_ : _t_ + _H−_ 1<sup>, the pretrained encoder first maps it into a latent represen-</sup> 

4 

Arxiv Version 

tation _z_<sup>src</sup> = _Eθ_<sup>src(</sup><sup>_x_src</sup> _t_ : _t_ + _H−_ 1<sup>).Each latent vector is then quantized by selecting its nearest codebook</sup> entry from the source character’s codebook _E_<sup>src</sup> as defined in Equation 2. 

We treat each quantized motion token _z_ ˆ<sup>src</sup> as a categorical distribution over source tokens. The retargeting model _fψ_ , parameterized by flow matching, is conditioned on an one hot vector control signal _c_ that specifies the retargeting objective. It defines a time-dependent velocity field _vψ_ ( _·, q, c_ ) that transports the distribution to the target token space. At inference time, the process starts from the source distribution _p_<sup>src</sup> at _q_ = 0 and integrates the following ODE until _q_ = 1: 


Numerical integration produces the final distribution _p_ 1 _≈ p_<sup>tgt</sup> . From this, the most likely token sequence ˜ _z_<sup>tgt</sup> is extracted and decoded by the pretrained target decoder to yield the retargeted motion: 


Condition-dependent motion retargeting is crucial in practice. For example, when aligning motion style in animation, the condition _c_ may specify local-frame style alignment so that the target reproduces the same movement pattern regardless of global trajectory. In contrast, motion retargeting for robotic manipulation or navigation tasks may require condition to specify world-frame alignment to ensure that end-effectors or base trajectories match global objectives. To support multiconditioned motion retargeting, **MoReFlow** employs classifier-free guidance (Ho & Salimans, 2022) to strengthen the influence of conditions without requiring explicit external classifiers. During inference, the velocity field is evaluated both with and without the condition _c_ , and the two predictions are interpolated: 


where _γ_ is the guidance scale. This strategy allows users to smoothly control the strength of condition signals, enabling flexible trade-offs between different motion retargeting preferences. 

### 3.3 LEARNING MOTION RETARGETING VIA UNSUPERVISED FLOW MATCHING 

Training the retargeting model _fψ_ is challenging because we do not assume access to paired motion datasets across characters. To address this, we combine flow matching with condition-dependent feature regularization. 

We consider the distributions _z_<sup>src</sup> and _z_<sup>tgt</sup> over the source and target codebooks. Flow matching defines an interpolating distribution _pt_ between _z_<sup>src</sup> and _z_<sup>tgt</sup> by setting the velocity _z_ ˙ as _z_<sup>tgt</sup> _− z_<sup>src</sup> , and the model learns a velocity field _vψ_ to match the probability flow Lipman et al. (2024): 


To guide alignment toward meaningful retargeting outcomes, we define a feature extractor Φ( _·, c_ ) that computes condition-specific descriptors from a motion sequence, where the details of the feature functions are provided in A.4. The feature loss compares the extracted features of the source motion _x_<sup>src</sup> and the retargeted motion _x_ ˆ<sup>tgt</sup> : 


This formulation remains flexible across diverse conditioning schemes without committing to fixed feature types. 

Following the classifier-free guidance paradigm, during training we randomly drop the condition _c_ (with probability _p_ mask), replacing it with a null condition ∅. This allows the model to learn both unconditional and conditional velocity fields, enabling stronger control during inference via interpolation (Zheng et al., 2023). The final objective combines the flow matching loss and the condition-dependent feature loss with a weighting variable _α_ : 


Because we do not assume a paired dataset, which is less feasible for large-scale motion retargeting, we require a mechanism to guide the learning process of flow matching. We employ multi-sample 

5 

Arxiv Version 

condition couplings, where each source motion can be associated with multiple target motions depending on the conditions. At the beginning of each iteration, we sample a condition, including the null condition, and a batch of motions from both the source and target domains. We then compute pairwise couplings across the batch according to the specified condition metrics to update the correspondence between source–target pairs. This multi-sample coupling strategy produces richer and more diverse training signals while preventing overfitting to arbitrary one-to-one pairings A.3. 

## 4 EXPERIMENT 

In this section, we evaluate **MoReFlow** through a comprehensive set of experiments. We begin by presenting our main results, which demonstrate that MoReFlow can retarget diverse dynamic human motions to both humanoid and quadrupedal robots with high motion quality, semantic alignment, and condition-dependent controllability. Next, we quantitatively compare our approach against several baseline methods, showing that **MoReFlow** achieves superior performance in cross-morphology motion retargeting while offering greater flexibility. Finally, we conduct a series of ablation studies to analyze the impact of key design choices such as embedding structure, motion dataset volume. 

### 4.1 EXPERIMENT SETUP 

We train and evaluate on the AMASS dataset (Mahmood et al., 2019), using a total of 482 clips corresponding to about 2,747 seconds or 82,410 frames. For **locomotion/lower-body** motions, we use 117 human source clips and 258 target-domain clips to cover a broad range of speeds and headings. For **arm/upper-body** motions, we use 105 human source clips and 310 target-domain clips to span diverse end-effector paths. The characters for source and target include an SMPL-humanoid (human), a half-sized SMPL-humanoid (half-human), the Booster T1 robot (T1) (Booster Robotics), and the Spot quadruped (Spot) (Boston Dynamics, 2019). 

### 4.2 IMPLEMENTATION DETAILS 

**Tokenization.** We train a separate motion VQ-VAE tokenizer for each character, which converts 32frame motion windows (=1 second) into compact token sequences. After normalizing each clip using the dataset-level mean and standard deviation, we extract all valid 32-frame windows for training and evaluation. VQ-VAE consists of a temporal convolutional encoder–decoder with configurable depth and width, which is combined with an EMA-reset quantizer (Williams et al., 2020). For SMPL humanoids and the Booster T1 robot, we use a codebook size of 512 _×_ 512, while for the Spot quadruped we use 256 _×_ 256. Temporal downsampling by a factor of 4 reduces each 32frame window to a short latent sequence of 8 tokens, which serves as the basis for retargeting. Codebook sequences are generated in batches for efficiency. For training, we use the AdamW optimizer (Loshchilov & Hutter, 2017) with betas [0.9, 0.99], a batch size of 128, and an exponential moving average constant _µ_ = 0 _._ 99. The Motion VQ-VAEs are trained with a learning-rate warm-up of 1K iterations at 2e-4, followed by 100K iterations at 1e-5. 

**Flow Matching.** Our Discrete-Flow-Transformer maps source tokens to target tokens conditioned on task features. It employs token embeddings, sinusoidal positional encoding, and separate time/condition MLP embeddings, followed by a Transformer encoder (Vaswani et al., 2017). The encoder is configured with 512-dimensional token embeddings, 6 encoder layers _×_ 8 self-attention heads, a 2048-dimensional feedforward sublayer, a dropout rate of 0 _._ 1, and a maximum sequence length of 8 tokens. The encoder output is connected to a linear prediction head over the target vocabulary. We use the same AdamW optimizer with a learning rate of 1e-4 and betas [0.9, 0.99] for a total 200K iterations with a 1K warm-up using the cosine LR scheduler (Loshchilov & Hutter, 2016), and the weight decay is 1e-2. The coupling batch size is set to _k_ = 512. 

All experiments run on a single RTX 4090 with an Intel i9-13900K (24 cores). Training the motion VQ-VAEs takes less than 1 hour per character, and training the discrete flow retargeter takes 8 hours approximately. 

### 4.3 MAIN RESULTS 

We first present the main results of **MoReFlow** . Our framework successfully retargets a wide range of dynamic human motions, including locomotion, jumping, tennis and golf swings, and boxing, 

6 

Arxiv Version 

onto the half human, T1, and Spot robots. For example, human walking motions following geometric trajectories are retargeted to all three characters, producing smooth and physically consistent executions. In addition, **MoReFlow** transfers challenging upper-body and whole-body motions with physical realism, demonstrating its ability to handle a broad spectrum of dynamic motions. 

A key advantage of **MoReFlow** is its controllability. Unlike traditional methods that typically produce a fixed retargeted motion for a given condition, our framework allows users to specify alignment conditions and thereby generate different outcomes. For example, the same human walking motion can be retargeted onto a smaller half-human or T1 in different ways, such as preserving the original style or aligning the global trajectory through faster walking or running (Figure 1, 1st column). In fact, task-space alignment can also induce drastically different behaviors, such as T1 jumping to match human height, T1 jumping more dynamically to follow a human leap, or a human crawling to match the lower height of Spot. For upper-body gestures, **MoReFlow** allows users to toggle the mapping of left, right, or both arms for T1 waving, or to direct the mapping to either a manipulator or a front leg for Spot boxing (Figure 1, 2nd column). Even in a book-retrieval scenario involving full-body motions, T1 can either stylistically imitate the human in the local frame or match task-space alignment by adjusting shoulder angles and reaching a higher shelf (Figure 1, 3rd column). Such controllability makes **MoReFlow** broadly applicable across domains where users may prioritize either stylistic fidelity or task effectiveness. 

Another advantage of **MoReFlow** lies in its ability to support chain-of-retargeting, which enables motion transfer between characters that do not share a direct mapping. Because the flow formulation is reversible, motions can be transferred modularly through intermediate characters. For example, we demonstrate the transfer of a quadruped robot’s hand-waving motion to the Booster T1 robot’s left and right hands by first retargeting the motion back to the human domain, and then mapping it onto the new robot. 

### 4.4 BASELINE COMPARISON 

To further validate the effectiveness of **MoReFlow** , we compare it against several baseline methods. The evaluation includes both qualitative visualizations and quantitative metrics that measure motion quality and controllability. 

To select baselines, we focus on cross-embodiment motion retargeting algorithms in an unsupervised setting. In this domain, we select two representative approaches: **Walk-the-Dog (WtD)** (Li et al., 2024a) and **ACE** (Li et al., 2023). **WtD** introduces a vector-quantized periodic autoencoder to learn a shared phase manifold across different characters, enabling alignment in both timing and semantics. It also learns a shared latent codebook for both source and target characters to cluster semantically similar motions. In contrast, our **MoReFlow** framework trains separate codebooks for each character and establishes correspondences between them through a learned flow field, which provides greater flexibility and modularity. On the other hand, **ACE** adopts a two-stage paradigm similar to ours: it first trains a motion prior, then learns a retargeting networks. However, **ACE** learns the retargeting function in a single step using a GAN-based adversarial objective. It also builds the motion prior using a motion VAE, whereas **MoReFlow** employs a VQ-VAE to obtain a tokenized latent representation. For all baselines, we follow the implementations provided in the original papers, with minor adaptations to ensure compatibility with our experimental setup. 

For quantitative evaluation, we employ the following metrics: 

- **FID** : computes the Fr´echet Inception Distance between the feature distributions of source and retargeted motions, assessing overall distributional similarity. Lower FID values signify that the retargeted motion more closely resemble the source motion. 

- **Diversity (DIV)** : measures the variability of retargeted motions across different sequences, capturing the expressiveness of the model. 

- **Alignment (ALI)** : measures feature-level consistency between the source and retargeted motions by computing differences in extracted features. 

- **Naturalness (NAT)** : assesses whether the generated motions are physically plausible. We identify unnatural frames, such as those exhibiting foot sliding, foot penetration, or joint vibration, and report the percentage of natural frames as the score. 

7 

Arxiv Version 

|Method|FI|D_↓_|DI|V_↑_|AL|I_↑_|NAT|(%)_↑_|
|---|---|---|---|---|---|---|---|---|
||Loco.|Upper.|Loco.|Upper.|Loco.|Upper.|Loco.|Upper.|
|WtD|42.4|75.0|0.45|0.40|0.84|0.56|87.2|82.2|
|ACE|51.7|60.8|0.56|0.51|0.79|0.75|80.8|84.1|
|**MoReFlow**|**33.1**|**38.9**|**0.68**|**0.63**|**0.85**|**0.79**|**89.6**|**92.9**|


Table 1: Comparison of MoReFlow against baseline methods on Locomotion (Loco.) and Upperbody retargeting tasks. 

In summary, _FID_ and _NAT_ primarily evaluate motion quality in terms of realism and physical plausibility, whereas _DIV_ and _ALI_ predominantly assess controllability, capturing expressive diversity and semantic consistency under fixed conditions. 

A summary of the results is presented in Table 1. Overall, our results show that **MoReFlow** consistently outperforms the baseline methods in both motion quality and controllability. Compared to **WtD** , our approach does not rely on an internal periodic structure to guide motion generation. While **WtD** ’s design enforces smooth periodic behaviors, it limits the ability to encode the full diversity of character motions. **WtD** performs well on periodic locomotion by aligning timing with a shared phase–codebook and frequency scaling, but it degrades markedly on non-periodic upper-body motions. For example, in lifting a box, **WtD** under-represents the amplitude and timing of elbow extension–flexion, leading to insufficient reach and frequent over/undershoot during the hold phase. In contrast, our method leverages character-specific codebooks connected through flow matching, which allows for more expressive movements. This is evident in our results, where **MoReFlow** achieves higher _Diversity_ and stronger _Alignment_ scores than **WtD** . 

When compared to **ACE** , **MoReFlow** also demonstrates clear advantages. **ACE** constructs its motion prior using a MotionVAE, which can suffer from posterior collapse, causing the generated motion to depend primarily on the character’s previous pose rather than the source motion. In addition, **ACE** performs retargeting as a single-step GAN-based mapping, which often produces unstable results. By contrast, **MoReFlow** generates retargeted motions gradually through the flow matching process, yielding smoother transitions and greater stability. With world-frame alignment on a half-sized SMPL-humanoid, **ACE** ’s prior-state dependency delays step-length and velocity adaptation, leading to increased toe slip, whereas **MoReFlow** promptly adjusts these parameters via condition-guided vector fields, reducing slip. On Spot with a manipulator for tennis swinging, **ACE** ’s single-step discriminator causes wrist jitter and impact undershoot, while **MoReFlow** integrated flow through peak velocity, deceleration, and stop improves impact stability. This design directly contributes to **MoReFlow** achieving lower _FID_ and higher _NAT_ scores than **ACE** , as the generated motions better preserve semantic intent while avoiding artifacts such as foot sliding or joint vibration. 

For locomotion, **WtD** ’s phase manifold and frequency-scaled matching perform well in capturing periodic timing and semantics ( _ALI_ ), but its shallow decoder and shared codebook limit distributional _FID_ and _DIV_ scores. For upper-body tasks, which are less periodic, both **WtD** and **ACE** exhibit reduced naturalness ( _NAT_ )— **WtD** due to phase bias and **ACE** due to adversarial instability. In contrast, **MoReFlow** ’s character-specific codebooks and continuous flows preserve semantics while mitigating artifacts, resulting in lower _FID_ and higher _NAT_ . 

### 4.5 ABLATION STUDY 

To further understand the design choices in **MoReFlow** , we conduct a series of ablation studies. These experiments examine how the latent representation, window size (chunk size), and couplinhg batch size affect retargeting quality and controllability. By comparing different configurations, we provide insight into why our final configuration achieves both high-quality and flexible motion retargeting. 

**Latent space design.** We first analyze the role of the latent space in motion retargeting. In this experiment, we compare three configurations: (1) retargeting directly in trajectory space without using a latent embedding, (2) retargeting in a continuous latent space without quantization, and (3) our proposed design using a VQ-VAE tokenized latent space. The results show that retargeting without a latent space suffers from unstable training and poor motion quality, as the high dimensionality of 

8 

Arxiv Version 

trajectories makes alignment difficult. The continuous latent variant improves stability, which result _FID_ value lower (53.3) and _NAT_ higher as **ACE** , 81.8%. But still produces motions with degraded diversity and alignment. In contrast, our discrete tokenized latent space provides compact and expressive motion representations, yielding the best performance across FID, Diversity, and Alignment metrics 1. 

**Window size.** The window size controls the temporal context seen by both the tokenizer and our Discrete-Flow-Transformer. Smaller windows emphasize local kinematics but may truncate non-periodic transients; larger windows capture longer dependencies, but increase token-sequence length and matching ambiguity unless the tokenizer’s temporal downsampling and the DiscreteFlow-Transformer’s maximum sequence length are co-tuned. Empirically, 32 frames worked best with nearest-neighbor (Euclidean) coupling driven by root-velocity features (local, short-horizon signals), while 64 frames benefited optimal transport (cosine) coupling in pattern space (longer temporal templates). With nearest-neighbor coupling, 32 frames yields the best semantic controllability with competitive realism, yields the highest _DIV, ALI_ values as Table 1, whereas with optimal transport, 64 frames improves realism ( _NAT_ 91.1%) and stability at a slight diversity cost ( _ALI_ goes down to 0.83). These settings balanced expressivity and stable couplings without exceeding the flow matching sequence budget. See Appendix A.3 for the per-step coupling procedure. 

**Coupling batch size.** Coupling is computed within each mini-batch: increasing the number of samples per step yields a denser bipartite candidate set, improving one-to-one pairing quality and reducing variance of the training signal; however, both cost and noise sensitivity grow with batch size, especially for transport-based coupling. We found a clear “sweet spot”: 512 for nearest-neighbor coupling, which offers sufficient candidate coverage without oversmoothing, and 256 for optimal transport coupling, which captures adequate structure while avoiding heavy, noisy transport in very large batches). Beyond these points, we observed diminishing returns and sporadic instability. When coupling batch size grows to the sweet spot, we observe diminishing returns and mild degradation in _NAT_ with higher training variance. 

## 5 LIMITATIONS 

A key limitation of our current framework is that motion retargeting is performed in a one-to-one manner, where a flow model is trained specifically for each source–target character pair. This design simplifies the learning problem and allows us to achieve high-quality results, but it prevents the framework from directly generalizing to many-to-many retargeting. Although retargeting between arbitrary characters can in principle be achieved by chaining intermediate mappings, this strategy introduces inefficiency: the computational cost grows with the number of intermediate characters, and accumulated errors along the chain may degrade motion fidelity. Moreover, such chaining assumes that a suitable path of characters exists between the source and target, which is not guaranteed in practice. Extending **MoReFlow** toward a unified framework that enables flexible one-to-many or any-to-any retargeting, while maintaining scalability and motion quality, is an important direction for future work. 

## 6 CONCLUSION 

In this work, we introduced MoReFlow, an unsupervised framework for cross-morphology motion retargeting based on flow matching in tokenized motion spaces. By combining character-specific VQ-VAE embeddings with condition-dependent flow models, our approach enables controllable and reversible motion transfer across a wide range of characters without requiring paired data. Extensive experiments demonstrate that MoReFlow not only achieves high-quality retargeting results across humanoid and quadrupedal robots but also offers explicit controllability to adapt motions to different alignment requirements. Compared to prior baselines, our framework delivers superior motion fidelity, diversity, and naturalness while providing deeper engineering insights through ablation studies. We believe MoReFlow establishes a scalable foundation for generalizable cross-character motion retargeting, and future work will explore extending the framework to many-to-many retargeting and real-world robot deployment. 

9 

Arxiv Version 

## REFERENCES 

- Kfir Aberman, Peizhuo Li, Olga Sorkine-Hornung, Dani Lischinski, and Daniel Cohen-Or. Skeleton-aware networks for deep motion retargeting. In _ACM Transactions on Graphics (TOG)_ , volume 39, pp. 62, 2020. URL https://arxiv.org/abs/2005.05732. 

- Noam Aigerman, Kunal Gupta, Vladimir G Kim, Siddhartha Chaudhuri, Jun Saito, and Thibault Groueix. Neural jacobian fields: Learning intrinsic mappings of arbitrary meshes. _arXiv preprint arXiv:2205.02904_ , 2022. 

- Booster Robotics. Booster t1. https://www.boosterobotics.com/booster-t1/. Accessed: 2025-09-23. 

- Boston Dynamics. Spot® - the agile mobile robot. https://www.bostondynamics.com/ products/spot, 2019. Accessed: 2025-09-23. 

- Zhefeng Cao, Ben Liu, Sen Li, Wei Zhang, and Hua Chen. G-dream: Graph-conditioned diffusion retargeting across multiple embodiments. _arXiv preprint arXiv:2505.20857_ , 2025. 

- Kwang-Jin Choi and Hyeong-Seok Ko. Online motion retargetting. _The Journal of Visualization and Computer Animation_ , 11(5):223–235, 2000. 

- Manolo Canales Cuba, Vin´ıcius do Carmo Mel´ıcio, and Jo˜ao Paulo Gois. Flowmotion: Targetpredictive conditional flow matching for jitter-reduced text-driven human motion generation. _Computers & Graphics_ , pp. 104374, 2025. 

- Ruiqi Gao, Emiel Hoogeboom, Jonathan Heek, Valentin De Bortoli, Kevin P. Murphy, and Tim Salimans. Diffusion meets flow matching: Two sides of the same coin. 2024. URL https: //diffusionflow.github.io/. 

- Ruben Grandia et al. Differentiable optimal control for legged robots. In _Robotics: Science and Systems (RSS)_ , 2023. URL https://la.disneyresearch.com/wp-content/ uploads/DOC_paper.pdf. 

- Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ , 2022. 

- Vincent Tao Hu, Wenzhe Yin, Pingchuan Ma, Yunlu Chen, Basura Fernando, Yuki M Asano, Efstratios Gavves, Pascal Mettes, Bjorn Ommer, and Cees GM Snoek. Motion flow matching for human motion synthesis and editing. _arXiv preprint arXiv:2312.08895_ , 2023. 

- Sunwoo Kim et al. Human motion control of quadrupedal robots using deep reinforcement learning. In _Robotics: Science and Systems (RSS)_ , 2022. URL https://arxiv.org/abs/2204. 13336. 

- Sunmin Lee, Taeho Kang, Jungnam Park, Jehee Lee, and Jungdam Won. Same: Skeleton-agnostic motion embedding for character animation. In _SIGGRAPH Asia 2023 Conference Papers_ , pp. 1–11, 2023. 

- Peizhuo Li, Sebastian Starke, Yuting Ye, and Olga Sorkine-Hornung. Walkthedog: Crossmorphology motion alignment via phase manifolds. In _SIGGRAPH, Technical Papers_ , 2024a. doi: 10.1145/3641519.3657508. 

- Tianyu Li, Jungdam Won, Alexander Clegg, Jeonghwan Kim, Akshara Rai, and Sehoon Ha. Ace: Adversarial correspondence embedding for cross morphology motion retargeting from human to nonhuman characters. In _SIGGRAPH Asia 2023 Conference Papers_ , pp. 1–11, 2023. 

- Tianyu Li, Hyunyoung Jung, Matthew Gombolay, Yong Kwon Cho, and Sehoon Ha. Crossloco: Human motion driven control of legged robots via guided unsupervised reinforcement learning. In _International Conference on Learning Representations (ICLR)_ , 2024b. URL https://proceedings.iclr.cc/paper_files/paper/ 2024/file/cce0df2e85795d81e417fc74c9cc29ec-Paper-Conference.pdf. 

10 

Arxiv Version 

- Tianyu Li, Hengbo Ma, Sehoon Ha, and Kwonjoon Lee. Learning physical interaction skills from human demonstrations. _arXiv preprint arXiv:2507.20445_ , 2025. 

- Yaron Lipman, Ricky TQ Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 

- Yaron Lipman, Marton Havasi, Peter Holderrieth, Neta Shaul, Matt Le, Brian Karrer, Ricky TQ Chen, David Lopez-Paz, Heli Ben-Hamu, and Itai Gat. Flow matching guide and code. _arXiv preprint arXiv:2412.06264_ , 2024. 

- Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. _arXiv preprint arXiv:1608.03983_ , 2016. 

- Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint arXiv:1711.05101_ , 2017. 

- Naureen Mahmood, Nima Ghorbani, Nikolaus F. Troje, Gerard Pons-Moll, and Michael J. Black. AMASS: Archive of motion capture as surface shapes. In _International Conference on Computer Vision_ , pp. 5442–5451, October 2019. 

- Francesco Martinelli et al. Collision-aware motion retargeting across skeletons. In _ACM Transactions on Graphics (TOG)_ , 2024. URL https://dl.acm.org/doi/10.1145/3681758. 3698007. 

- Lucas Mourot, Ludovic Hoyet, Florent Le Clerc, and Pierre Hellier. Humot: Topology-agnostic motion retargeting via transformers. _arXiv preprint arXiv:2305.18897_ , 2023. URL https: //arxiv.org/abs/2305.18897. 

- Daniele Reda, Jungdam Won, Yuting Ye, Michiel Van De Panne, and Alexander Winkler. Physicsbased motion retargeting from sparse inputs. _Proceedings of the ACM on Computer Graphics and Interactive Techniques_ , 6(3):1–19, 2023. 

- Rim Rekik, Mathieu Marsot, Anne-H´el`ene Olivier, Jean-S´ebastien Franco, and Stefanie Wuhrer. Correspondence-free online human motion retargeting. In _2024 International Conference on 3D Vision (3DV)_ , pp. 707–716. IEEE, 2024. 

- Aaron Van Den Oord, Oriol Vinyals, et al. Neural discrete representation learning. _Advances in neural information processing systems_ , 30, 2017. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. _Advances in neural information processing systems_ , 30, 2017. 

- Ruben Villegas, Jimei Yang, Seunghoon Hong, Xunyu Lin, and Honglak Lee. Learning to generate long-term future via hierarchical prediction. In _Proceedings of the 35th International Conference on Machine Learning_ , 2018. URL https://arxiv.org/abs/1804.05653. 

- Ruben Villegas, Duygu Ceylan, Aaron Hertzmann, Jimei Yang, and Jun Saito. Contact-aware retargeting of skinned motion. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pp. 9720–9729, 2021. 

- Will Williams, Sam Ringer, Tom Ash, David MacLeod, Jamie Dougherty, and John Hughes. Hierarchical quantized autoencoders. _Advances in Neural Information Processing Systems_ , 33:4524– 4535, 2020. 

- Xinchen Yan, Benjamin Mascaro, and Seungbae Lee. Imitationnet: Unsupervised human-to-robot motion retargeting. _arXiv preprint arXiv:2309.05310_ , 2023. URL https://arxiv.org/ abs/2309.05310. 

- Seonghun Yoon, Sungjoon Kang, Minhyuk Kim, Sungjoon Ahn, Stelian Coros, and Sung-Hee Choi. Spatio-temporal motion retargeting for quadruped robots. _arXiv preprint arXiv:2404.11557_ , 2024. URL https://arxiv.org/abs/2404.11557. 

11 

Arxiv Version 

- Kevin Zakka. Mink: Python inverse kinematics based on MuJoCo, May 2025. URL https: //github.com/kevinzakka/mink. 

- J Zhang, Y Zhang, X Cun, S Huang, Y Zhang, H Zhao, H Lu, and X Shen. T2m-gpt: Generating human motion from textual descriptions with discrete representations. arxiv 2023. _arXiv preprint arXiv:2301.06052_ , 2023a. 

- Jiaxu Zhang, Zhigang Tu, Junwu Weng, Junsong Yuan, and Bo Du. A modular neural motion retargeting system decoupling skeleton and shape perception. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 46(10):6889–6904, 2024. 

- Yang Zhang, Zhiwen Deng, Zhigang Pan, and He Wang. Skinned motion retargeting with residual perception of motion semantics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2023b. URL https://openaccess.thecvf.com/ content/CVPR2023/papers/Zhang_Skinned_Motion_Retargeting_With_ Residual_Perception_of_Motion_Semantics__CVPR_2023_paper.pdf. 

- Qinqing Zheng, Matt Le, Neta Shaul, Yaron Lipman, Aditya Grover, and Ricky TQ Chen. Guided flows for generative modeling and decision making. _arXiv preprint arXiv:2311.13443_ , 2023. 

12 

Arxiv Version 

## A TRAINING HYPERPARAMETERS 

A.1 VQ-VAE (TOKENIZER) PER CHARACTER 

Table 2 

|**Group**|**Param**|**Value**|
|---|---|---|
|Data|window<br>~~s~~ize|32|
||batch<br>~~s~~ize|128|
||num<br>~~w~~orkers|4|
|Optimization|total<br>~~i~~ter|100,000|
||warmup<br>~~i~~ter|1,000|
||lr|2e-4|
||optimizer|AdamW|
||betas|(0.9, 0.99)|
||weight<br>~~d~~ecay|0.0|
||lr<br>~~s~~cheduler|[50k, 100k]|
||scheduler_γ_|0.05|
|Loss|recons<br>~~l~~oss<br>commit_β_|l1<br>~~s~~mooth<br>0.02|
|Quantizer|quantizer|ema<br>~~r~~eset|
||_µ_|0.99|
||beta|1.0|
||nb<br>~~c~~ode|512|
|Humanoids|code<br>~~d~~im|512|
|(SMPL,<br>half,|width/depth|512 / 3|
|Booster T1)|down<br>~~t~~ / stride<br>~~t~~|2 / 2|
||out<br>~~e~~mb<br>~~w~~idth|512|
||nb<br>~~c~~ode|256|
||code<br>~~d~~im|256|
|Spot quadruped|width/depth|256 / 3|
||down<br>~~t~~ / stride<br>~~t~~|2 / 2|
||out<br>~~e~~mb<br>~~w~~idth|256|
|Misc|activation / norm<br>seed|relu / none<br>123|


Table 2: VQ-VAE tokenizer hyperparameters per character family. 

A.2 FLOW MATCHING RETARGETER 

Table 3 

13 

Arxiv Version 

|**Group**|**Param**|**Value**|
|---|---|---|
|Discrete tokens|vocab<br>~~s~~ize<br>max<br>~~s~~eq<br>~~l~~en|_= target_ nb<br>~~c~~ode<br>8|
|Transformer|d<br>~~m~~odel<br>n<br>~~l~~ayers<br>n<br>~~h~~ead<br>d<br>~~f~~f<br>dropout<br>activation<br>pos. encoding<br>batch<br>~~f~~irst|512<br>6<br>8<br>2048<br>0.1<br>GELU<br>sinusoidal<br>True|
|Cond/Time embed|time<br>~~e~~mbed<br>cond<br>~~e~~mbed<br>cond<br>~~d~~im|2-layer MLP, SiLU<br>2-layer MLP, SiLU<br>derived|
|Data|window<br>~~s~~ize<br>coupling<br>~~b~~atch<br>~~s~~ize<br>num<br>~~w~~orkers|32 (default)<br>512 (NN) / 256 (OT)<br>4|
|Optimization|total<br>~~i~~ter<br>lr<br>scheduler|200,000<br>1e-4<br>CosineAnnealingLR|
|Loss|_L_FM|1.0|
||_L_feat|0.2|


Table 3: Flow Matching hyperparameters and Transformer configuration. 

### A.3 MULTI-SAMPLE CONDITION COUPLING 

- **Algorithm 1** Pseudocode of Multi-Sample Condition Coupling **Require:** Pretrained source tokenizer _E_<sup>_src_</sup> , Pretrained target tokenizer _E_<sup>_tgt_</sup> **Require:** Source motion dataset _Dsrc_ , Target motion dataset _Dtgt_ **Require:** Set of conditions _C_ (including null condition _∅_ ) **Require:** Condition-specific feature extractor Φ( _·, c_ ) 1: **Initialize:** Flow model parameters _ψ_ 2: **for** each training iteration **do** 3: // 1. Sample a condition and motion batches 4: Sample a condition _c ∼C_ 5: Sample a source motion batch _Bsrc_ = _{x_<sup>_src_</sup> _i }_<sup>_k_</sup> _i_ =1<sup>_∼Dsrc_</sup> 6: Sample a target motion batch _Btgt_ = _{x_<sup>_tgt_</sup> _j_<sup>_}_</sup> _j_<sup>_k_</sup> =1<sup>_∼Dtgt_</sup> 7: 8: // 2. Compute condition-specific features for coupling 9: Compute source features _{Fi_<sup>_src_</sup> _←_ Φ( _x_<sup>_src_</sup> _i , c_ ) _}_<sup>_k_</sup> _i_ =1 

- 10: Compute target features _{Fj_<sup>_tgt_</sup> _←_ Φ( _x_<sup>_tgt_</sup> _j_<sup>_, c_)</sup><sup>_}_</sup> _j_<sup>_k_</sup> =1 11: 12: // 3. Find correspondences by computing pairwise couplings 13: Compute a cost matrix _M_ where _Mij_ = distance( _Fi_<sup>_src_</sup> _, Fj_<sup>_tgt_</sup> ) 14: Find an optimal permutation _π_ = argmin _σ_ � _ki_ =1<sup>_Mi,σ_(</sup><sup>_i_)</sup> 15: 16: // 4. Form pseudo-pairs and update the flow model 17: Create pseudo-pairs _P_ = _{_ ( _x_<sup>_src_</sup> _i , x_<sup>_tgt_</sup> _π_ ( _i_ )<sup>)</sup><sup>_}_</sup> _i_<sup>_k_</sup> =1 18: Obtain latent codes for pairs: _zi_<sup>_src_</sup> _← E_<sup>_src_</sup> ( _x_<sup>_src_</sup> _i_ ), _zπ_<sup>_tgt_</sup> ( _i_ )<sup>_←Etgt_(</sup><sup>_xtgt_</sup> _π_ ( _i_ )<sup>)</sup> 19: Compute loss _Ltotal_ using _{_ ( _zi_<sup>_src_</sup> _, zπ_<sup>_tgt_</sup> ( _i_ )<sup>)</sup><sup>_}_</sup> _i_<sup>_k_</sup> =1<sup>and condition</sup><sup>_c_(from Eq. 13)</sup> 20: Update parameters: _ψ ←_ update( _ψ, ∇ψLtotal_ ) 

14 

Arxiv Version 

A.4 DETAILS OF CONDITIONS 

**Notation.** Let ∆ _t_ = 1 _/_ FPS, _Rt ∈ SO_ (3) be the world-frame root orientation at time _t_ , and _p_<sup>root</sup> _t ∈_ R<sup>3</sup> the world-frame root (pelvis) position. For any world-frame vector _x_<sup>world</sup> _t_ , the rootaligned local coordinate is 


Let _pt_ ( _j_ ) _∈_ R<sup>3</sup> denote the world-frame position of joint/end-effector _j_ . Given a window of length _T_ (e.g., _T_ =32), define the window average as 


**1. Root velocity condition (world-frame measurements)** Combine root linear and angular velocities expressed in the _root-aligned_ frame (values retain physical units). 


_2D planar variant (optional)._ If needed for planar walking: 


**2. Local end-effector position condition (only limb-length normalization)** Use _root-aligned relative_ EE positions. For an EE set _J_ , each with an anchor _aj_ (e.g., shoulder for wrist/elbow), define 


where _ℓaj →j >_ 0 is the limb length (measured at rest or averaged), and _ε_ is a small constant for numerical stability. 


_Arm-specific example (anchor = shoulder)._ 


When we want to make different conditions for each part of character body, _c_<sup>arm-local</sup> _t_ can be concatenated by different combinations of left or right or multiple body parts. 

15 

Arxiv Version 

**3. World XYZ end-effector position condition (absolute)** Use absolute world-frame EE positions without any dataset or scale normalization: 


**4. World XY root position condition (path control)** Use the root world-frame planar position. Remove an initial offset (for relative pathing) but do _not_ normalize: 


**5. World Z (root height) condition (absolute)** Use the root world-frame height directly: 


### **Notation addendum** 

- <sup>**�**</sup> : feature-wise concatenation along the channel/feature axis (we use<sup>�</sup> as “concat,” not as a direct-sum operator). 

- log( _·_ ) on _SO_ (3): matrix logarithm mapping a rotation to a skew-symmetric element in so(3). 

- vee( _·_ ): the _∨_ -operator so(3) _→_ R<sup>3</sup> that converts a skew-symmetric matrix to its axial vector (inverse of the hat map). 

- wrap( _·_ ): angle wrapping to ( _−π, π_ ] (used for yaw increments). 

- _ψt_ : root yaw angle at time _t_ ; ( **v** _t_ ) _x,y_ and ( _·_ ) _z_ denote planar and vertical components respectively. 

- _J_ : the chosen set of end-effectors/joints used for a condition (e.g., _{_ wrist, elbow _}_ ); _aj_ is the anchor joint for _j_ (e.g., shoulder for arm). 

- _ℓaj →j_ : limb length from anchor _aj_ to end-effector _j_ (measured in a rest pose or as an average over the dataset); _ε >_ 0 is a small constant for numerical stability. 

- _t_ 0: the reference frame index used for offset removal in world-XY paths (typically the start of the current window, i.e., _t_ 0= _t_ ). 

**Notes.** Local (anchor-relative) features are made approximately scale-invariant by limb-length normalization, which is desirable for upper-limb control. World-frame conditions intentionally keep their physical magnitudes, preserving absolute task constraints such as global positions, heights, and true velocities. All conditions are aggregated to window-level features via Φ<sup>(</sup> _t_ :<sup>_·_</sup> _T_<sup>)tomatchthe</sup> windowed formulation used in Sec. 3.3. 

16 

