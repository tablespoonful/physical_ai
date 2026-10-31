---
title: "LARA: Latent Action Representation Alignment for Vision-Language-Action Models"
date: "2026-06-05"
authors: "Mengya Liu; Baoxiong Jia; Jiangyong Huang; Jingze Zhang; Siyuan Huang"
venue: "ICML 2026"
url: https://arxiv.org/abs/2606.07100
pdf: https://arxiv.org/pdf/2606.07100
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2606.07100)** / [論文ページ](https://arxiv.org/abs/2606.07100)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **LARA: Latent Action Representation Alignment for Vision-Language-Action Models** 


_Figure 1._ We present **L** atent **A** ction **R** epresentation **A** lignment (LARA), a simple yet highly effective Vision-Language-Action (VLA) framework that bridges unlabeled video data and action-labeled robot datasets by jointly training a Latent Action Model (LAM) and a diffusion-based VLA model via latent action representation alignment. LARA supports versatile usage as a pre-training method, a post-training enhancement module for pre-trained VLA models, and a latent action refiner for LAM-based VLA models. 

## **Abstract** 

Visual-language action (VLA) models enable robots to predict actions directly from observations and language instructions, but their performance depends on large-scale, high-quality data and is limited by the scarcity of real-world robot action datasets. To facilitate VLA model learning with abundant unlabeled human videos, Latent Action Models (LAM) learn latent action representations from visual dynamics to provide additional supervision for VLA learning. However, LAM and VLA are typically trained separately, leaving LAM ungrounded during VLA training and VLA models constrained by frozen LAM representations. To address these issues, we propose Latent Action Representation Alignment (LARA), a plug-and-play framework that jointly optimizes LAM and VLA via representation alignment. This enables reciprocal benefits where LAMs learn with action trajectories to avoid spu- 

> *Equal contribution †Project lead 1State Key Laboratory of General Artificial Intelligence, BIGAI<sup>2</sup> Peking University. Correspondence to: Baoxiong Jia <baoxiongjia@g.ucla.edu>. 

_Proceedings of the 43_<sup>_𝑟𝑑_</sup> _International Conference on Machine Learning_ , Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s). 

rious visual changes, while VLAs are regularized by forward dynamics learned within LAMs to reduce hallucinations of functionally ineffective trajectories. We demonstrate LARA’s versatility and effectiveness for pre-training, post-training enhancement of pre-trained VLA models, and LAM refinement, achieving an average of ∼10%, ∼5%, and ∼15% improvement over 3 simulation and 1 meticulously designed real-world robotic manipulation benchmarks. The code is publicly available at https://github.com/lmy1001/LARA. 

## **1. Introduction** 

With the rise of Large Vision-Language Models (VLMs), robotic manipulation is shifting from classical task planning and control to learning-based Vision-Language-Action (VLA) models (Kim et al., 2024; Bjorck et al., 2025; Black et al., 2024; Brohan et al., 2022) where actions are predicted directly given visual observation and language instruction. Like other VLMs, VLA performance critically depends on large-scale high-quality data. However, unlike visual datasets, robotic data is difficult and costly to collect, requiring real-world robot interactions, and is hard to generalize across different embodiments. Despite recent efforts to unify and scale robotic datasets (O’Neill et al., 2024; 

1 

**Latent Action Representation Alignment** 

Fang et al., 2023; Bu et al., 2025a), robotic data remains scarce, causing even state-of-the-art VLA models to overfit and struggle to generalize to novel tasks and environments. 

To overcome the robotic data bottleneck, human videos (Goyal et al., 2017; Grauman et al., 2024) have been used as a rich data source due to their scale, accessibility, and diverse task coverage. However, the lack of robot action labels and the large human-robot embodiment gap prevent the direct use of human videos in robot learning. Latent Action Models (LAMs) (Chen et al., 2022; Ye et al., 2024; Chen et al., 2025b) address this challenge by learning to predict future states and compressing visual dynamics into latent action representations as additional VLA data sources. This mechanism is either integrated into VLA models as a pre-training stage before action learning (Bu et al., 2025b) or learned separately to generate pseudo-labels for VLA learning (Ye et al., 2024; Chen et al., 2025b). In both cases, training involves _complex, multi-stage training pipelines with model-specific designs_ . More importantly, as shown in Fig. 2 (left), LAM learning is largely _decoupled_ from VLA learning, leaving LAM ungrounded on accurate action trajectories available during VLA learning and VLA models constrained by frozen LAM representations. 

To this end, we propose **L** atent **A** ction **R** epresentation **A** lignment (LARA), a framework that bridges LAM and VLA learning via representation alignment (Fig. 2 (right)) with the following key insights: 

- For LAM, joint learning with VLA models action trajectories grounds inverse visual dynamics learned to real actions, reducing the learning of spurious visual changes ( _e.g_ ., background, lighting, _etc_ .) from reconstruction. 

- For VLA, LAM regularizes learning by incorporating forward predictions of action effects, reducing hallucinations of kinematically plausible yet functionally incorrect or task-irrelevant action trajectories. 

Drawing inspiration from recent work on representation alignment in diffusion models (Yu et al., 2024; Leng et al., 2025), LARA coordinates LAM and VLA models through a lightweight mechanism compatible with most diffusion-based VLA architectures. Through extensive experiments on simulation and real-world robotic benchmarks, we demonstrate LARA as: (1) **a strong VLA training pipeline** , improving base VLA models by ∼10%, (2) **a powerful post-training enhancement module** for pre-trained VLAs, yielding ∼5% improvement on average, and (3) **an effective method for refining latent action representations** in LAM, boosting based model performance by ∼15% when used as pseudo-labels for downstream VLA learning. Our contributions are as follows: 

- We propose, LARA, a novel and effective framework for jointly improving LAM and VLA model learning via 


_Figure 2._ **Comparison of LAM-based VLA models.** LAMs are commonly used as pseudo labels for VLA learning (left), where as LARA jointly optimizes LAM and VLA model by explicitly aligning their latent representations (right). 

latent action representation alignment. 

- We show LARA’s versatility as a pre-training method, a plug-and-play post-training enhancement module, and a latent action refiner for LAMs. 

- We validate LARA on 3 challenging simulation and 1 real-world robot benchmarks, achieving ∼10%, ∼5%, and ∼15% improvements for full training, post-training enhancement, and LAM refinement, respectively. 

## **2. Related Works** 

**Vision-Language-Action (VLA) Models.** VLA models leverage the reasoning capabilities of VLMs (Karamcheti et al., 2024; Li et al., 2025b; Huang et al., 2024; Gong et al., 2023) to integrate natural language instructions, visual observations, and robot proprioception into a unified control policy. Pioneering works such as RT-1 (Brohan et al., 2022) and Octo (Team et al., 2024) employ a transformer-based policy that integrates diverse data, including robot trajectories across various tasks. RT-2 (Brohan et al., 2024), OpenVLA (Kim et al., 2024), _𝜋_ 0 (Black et al., 2024), and GR00TN1 (Bjorck et al., 2025) adopt a paradigm of large-scale cross-embodiment pre-training followed by task-specific fine-tuning, achieving strong inference performance. Subsequent studies further enhance these models along multiple dimensions, including spatial reasoning (Qu et al., 2025; Zhang et al., 2025b; Zhen et al., 2024; Li et al., 2026), longhorizon planning via Chain-of-Thought (Lin et al., 2025; Zhao et al., 2025), and hierarchical policy systems (Luo et al., 2025; Shi et al., 2025; Huang et al., 2025a; Lee et al., 2025; Li et al., 2025a). Despite these advances, these models are still limited by the scarcity and high cost of labeled robot data (O’Neill et al., 2024) compared to the vast availability of unlabeled video data, revealing a largely untapped opportunity to leverage motion priors inherently embedded in general video corpora. 

2 

**Latent Action Representation Alignment** 

**Latent Action Models (LAM) for VLA Pretraining.** Latent action learning originated in general video domains with approaches such as LAPO (Chen et al., 2022) and Genie (Bruce et al., 2024), inferred latent control signals to model video dynamics. In robotics, LAM is commonly used as an intermediate representation to supervise VLA learning (Ye et al., 2024; Chen et al., 2025b; Bjorck et al., 2025). The subsequent study on LAM improves this paradigm in terms of latent action quality (Nikulin et al., 2025; Liang et al., 2025), data scaling (Chen et al., 2025a), and better integration within VLA models (Bu et al., 2025b). However, these methods generally treat the LAM as a static provider of pseudo-labels or pre-trained weights. This decoupling prevents latent representations from adapting to real robot actions, leaving the gap between visual dynamics and robot motor execution unresolved. 

**Representation Alignment.** The idea of leveraging good representations for regularizing modeling has proven to be effective for a diverse range of tasks, VLM learning (Jain et al., 2025), 3D understanding (Huang et al., 2025b), as well as image generation (Ye et al., 2024; Leng et al., 2025; Ma et al., 2025; Yao et al., 2025). Despite similar ideas having been explored on VLA learning (Zheng et al., 2025; Kachaev et al., 2025) by aligning the VLA model with diverse frozen visual-language features, we argue that the alignment target should essentially be an updatable action representation to allow the latent action space to coevolve with VLA learning. In fact, we show that, similar to REPA (Ye et al., 2024) in image generation, this can be easily achieved by a bidirectional representation alignment loss between intermediate features of the diffusion VLA and LAM latent actions. 

## **3. Background** 

**Diffusion-based VLA Models** Flow-based VLA models map visual observations and natural language instructions to robot action trajectories using VLMs and flow-based generative models. At timestep _𝑡_ , the VLM model VLM _𝜃_ extracts task-related vision-language tokens **f** _𝑡_<sup>vl= VLM</sup><sup>_𝜃_(</sup><sup>_𝑰𝑡, 𝑳_) from</sup> the instruction _𝑳_ and observation _𝑰𝑡_ . Combined with robot proprioceptive state **s** _𝑡_ , these form the conditioning input **c** _𝑡_ = { **s** _𝑡 ,_ **f** _𝑡_<sup>vl}foractiongeneration.Thediffusion-based</sup> action generation model then generates an action chunk with _𝐶_ steps _𝑨𝑡_ = **a** _𝑡_ : _𝑡_ + _𝐶_ via flow matching. Specifically, given the flow timestep _𝜏_ ∈[0 _,_ 1] and the sampling noise _𝝐_ ∼N ( **0** _, 𝑰_ ), the model optimizes: 


where _𝑨𝑡_<sup>_𝜏_=</sup><sup>_𝜏𝑨𝑡_+(1−</sup><sup>_𝜏_)</sup><sup>_𝝐_isthenoisedaction.This</sup> objective trains the velocity field network _𝑣 𝜃_ to predict denoising directions at each flow timestep (Lipman et al., 2022). With this velocity field, we can generate actions from 

random noise _𝑨𝑡_<sup>0∼N (</sup><sup>**0**</sup><sup>_, 𝑰_)by integrating</sup><sup>_𝑣𝜃_from</sup><sup>_𝜏_=0</sup> to _𝜏_ = 1 via the forward Euler rule: 


where _𝐾_ is the number of integration steps controlling the approximation accuracy. 

**Latent Action Model (LAM)** Given the scarcity of actionlabeled robotic data, prior works have explored leveraging unlabeled human and robot interaction videos for robotic action learning (Chen et al., 2022; Ye et al., 2024; Chen et al., 2025b). These methods employ a LAM that encodes transitions between current visual observations _𝑰𝑡_ and future observation _𝑰𝑡_ + _𝐶_ into discrete latent actions. Specifically, the LAM consists of three components: 

- (1) _Inverse Dynamic Model (IDM)_ **z** _𝑡_ = IDM _𝜑_ ( _𝑰𝑡 , 𝑰𝑡_ + _𝐶_ ) predicts continuous latent action **z** _𝑡_ capturing implicit dynamics between current and future observations. 

- (2) _Vector Quantizer_ **z** _𝑡_<sup>_𝑞_= Quant</sup><sup>_𝜑_(</sup><sup>**z**</sup><sup>_𝑡_), that discretizes the</sup> latent into a codebook token **z** _𝑡_<sup>_𝑞_∈{</sup><sup>**z**1</sup> _𝜑_<sup>_,_· · ·</sup><sup>_,_</sup><sup>**z**</sup><sup>_𝐾_</sup> _𝜑_<sup>}codebook</sup> following VQ-VAE (Van Den Oord et al., 2017). 

- (3) _Forward Dynamic Model (FDM) 𝑰_<sup>ˆ</sup> _𝑡_ + _𝐶_ = FDM _𝜑_ ( _𝑰𝑡 ,_ **z** _𝑡_<sup>_𝑞_),</sup> that reconstructs the future observation conditioned on the current observation and the quantized latent action. 

The full pipeline is trained end-to-end with the VQVAE (Van Den Oord et al., 2017) objective: 


where sg[·] denotes the stop-gradient operation and _𝛽_ balances the commitment loss (Van Den Oord et al., 2017). Most LAM-based VLA models (Ye et al., 2024; Chen et al., 2025b;a) follow a two-stage protocol: first pre-training the LAM on unlabeled data, then leveraging it to guide VLA training with labeled data. As illustrated in Fig. 2 (left), the standard approach treats latent action tokens **z** _𝑡_<sup>_𝑞_as ad-</sup> ditional supervision, where the VLA model is trained to predict both the latent action **z**<sup>_𝑡_</sup> _𝑞_<sup>andtheactuallow-level</sup> actions _𝑨𝑡_ . While this design facilitates model training, it potentially risks constraining the quality of the learned action representations to the fidelity of the pseudo labels produced by the LAM given similar limitation observed in the image generation domain (Leng et al., 2025). 

## **4. Method** 

As discussed in Sec. 1 and Sec. 3, LAM and flow-based action models represent complementary aspects of robot control but operate in isolation without leveraging each other’s modeling on state transition (effect) and action commands (cause). To this end, we propose LARA ( **L** atent **A** ction **R** epresentation **A** lignment) to enable joint optimization of both models via a simple and effective latent action repre- 

3 


_Figure 3._ **Method overview.** We begin with LAM (left), where an Inverse Dynamic Model (IDM) learns a latent action **z** _𝑡_ from consecutive image frames, and a Forward Dynamic Model (FDM) learns to reconstruct the subsequent frame conditioned on the preceding frame and the quantized latent action **z** _𝑡_<sup>_𝑞_.We then conduct Latent Action Representation Alignment (LARA) training on a diffusion-based VLA</sup> model, where LARA explicitly aligns the latent action **z** _𝑡_ with intermediate features of the Diffusion Transformer (DiT), thereby jointly optimizing the LAM and VLA model in an end-to-end manner. 

sentation alignment mechanism. We provide an overview of LARA in Fig. 3. 

### **4.1. Latent Action Representation Alignment (LARA)** 

**Latent Action Representation Alignment** Recent work in image generation (Yu et al., 2024; Leng et al., 2025), has demonstrated that aligning diffusion model intermediate features with pre-trained representations like DINOv2 (Oquab et al., 2023) improves generation quality. We adopt this principle for action generation by treating the flow-matching model _𝑣 𝜃_ ( _𝑨𝑡_<sup>_𝜏,_</sup><sup>**c**</sup><sup>_𝑡_) from Eq. (1) as an encoder-decoder struc-</sup> ture _𝐸 𝜃_ ◦ _𝐷 𝜃_ within its architecture: 


where the encoder _𝐸 𝜃_ extracts an intermediate latent representation **h** _𝑡_<sup>_𝜃_,which the decoder</sup><sup>_𝐷𝜃_uses to predict the</sup> target velocity **v** _𝑡_ = _𝑨𝑡_ − _𝝐_ . In practice, when implemented as a DiT (Peebles & Xie, 2023), the representation **h** _𝑡_<sup>_𝜃_corre-</sup> sponds to the latent features between DiT layers. Drawing inspiration from image diffusion methods like REPA (Yu et al., 2024), we introduce a representation alignment objective for action learning. Given a frozen pre-trained action representation embedding **y**<sup>pretrain</sup> _𝑡_ , we optimize: 


where _𝑓𝜓_ (·) is a learnable projection head that adapts between the pre-trained action representation space and the diffusion feature space. Different from prior works (Zheng et al., 2025) that leverage frozen action embeddings, we leverage the online LAM latent actions **z**<sup>frozen</sup> _𝑡_ from Eq. (3) as **y**<sup>pretrain</sup> _𝑡_ and propose the joint training of the LAM and 

action diffusion models. Specifically, we replace the frozen representation **y**<sup>pretrain</sup> _𝑡_ with the online LAM latent action: 


where **z** _𝑡_<sup>_𝜑_=</sup><sup>**z**</sup><sup>_𝑡_is the online continuous latent action before</sup> quantization in the LAM. This alignment loss is combined with both the flow-matching objective and the LAM reconstruction objective to form the full LARA objective: 

L( _𝜃, 𝜑, 𝜓_ ) = LACT ( _𝜃_ ) + _𝑤_ 1LLARA ( _𝜃, 𝜑, 𝜓_ ) + _𝑤_ 2LLAM ( _𝜑_ ) _,_ (7) 

where _𝑤_ 1 and _𝑤_ 2 are loss balancing hyperparameters. 

- **Bi-directional Regularization Effect** Notably, LARA induces complementary regularization effects on both the LAM and the action diffusion model: 

- (1) _Inverse Dynamics Regularization for LAM_ : By aligning LAM latent actions with action policy representations, we constrain the action latent space to emphasize controlrelevant visual changes rather than nuisance variations ( _e.g_ ., lighting, shadows) which are irrelevant for action execution. This alignment suppresses these spurious factors arising from purely visual dynamics learning and encourages **z** _𝑡_ to encode only causal features necessary for predicting actions, resulting in a more action-centric LAM latent space. 

- (2) _Forward Dynamics Grounding for Action Diffusion_ : Standard behavior cloning-based action generation largely reduces to pattern matching from observations to actions, without explicitly modeling the physical consequences of actions. By anchoring intermediate action-DiT representations to the forward-predictive latent actions learned by the LAM, we inject an explicit notion of future state 

4 

**Latent Action Representation Alignment** 

evolution into the action diffusion policy. This grounding biases the action model toward representations consistent with plausible future world states, mitigating the prediction of kinematically hallucinated trajectories ( _i.e_ ., physically plausible but non-effect actions), and ensuring that generated actions respect environment dynamics. 

### **4.2. Training and Application of LARA** 

**Model Design** For the LAM model, we adopt the latent action model design from Moto-GPT (Chen et al., 2025b), modeling the IDM and FDM using ViT-based encoderdecoder architectures and a latent codebook size of 128. For the diffusion VLA model, we use a standard crossattention DiT backbone following prior works (Liu et al., 2024; Bjorck et al., 2025). Vision-language features are extracted using a frozen Eagle-2 (Li et al., 2025b) VLM with learnable adapters. To accommodate for diverse robot embodiments, we follow GR00T-N1 (Bjorck et al., 2025) and employ embodiment-specific MLP encoders that map heterogeneous proprioceptive state sapces into a shared embedding space before feeding them into the DiT. LARA at the second-to-last _𝐿_ − 2 layer of the DiT. We provide additional implementation and training details in Sec. A.1. 

- **LARA Training Pipeline** We train both the LAM and the action diffusion models with the following three stages: 

- (1) _LAM Pre-training_ : We train the LAM on large-scale unlabeled video data, including both robot data and internet videos using the LAM objective as in Eq. (3). This establishes a general purpose latent action space capturing visual dynamics across diverse scenarios. 

- (2) _LARA Joint Pre-Training_ : Taking the reconstruction pretrained LAM from stage 1, we train the action diffusion model on robot demonstration data with action labels, applying the full LARA objective in Eq. (7) and updating the action DiT and LAM jointly. This stage incorporates diverse robot embodiments to learn better embodimentagnostic action representations. 

- (3) _LARA Joint Post-Training_ : We fine-tune all models from stage 2 on target-task demonstrations for the deployment embodiment with task-specific data. This follows the standard VLA pre-training and post-training paradigm. 

**Applications of LARA** As the representation-level alignment in LARA enables flexible integration with diverse pretrained LAMs and action diffusion models without architectural modifications, we demonstrate two representative applications of LARA on pre-trained models: 

- (1) _LARA Post-training Enhancement_ , where LARA is applied as a modular post-training procedure to an existing pre-trained diffusion-based VLA model using a pretrained LAM for representation alignment. 

- (2) _LARA for Latent Action Refinement_ , where the LARA- 

pretrained LAM provides improved structured latent action tokens that can be directly used as pseudo-labels in latent action-based frameworks such as LAPA (Ye et al., 2024) and Moto-GPT (Chen et al., 2025b). 

Both usage modes rely on post-training-scale data and are empirically evaluated in Sec. 5 to show their effectiveness. 

## **5. Experiments** 

In this section, we validate the efficacy of LARA by addressing the research questions below in the following sections: 

- (1) How does LARA compare to existing VLA models across diverse robotic menchmarks? 

- (2) To what extent does LARA improve existing models as a post-training refinement module for VLAs and as a latent action refiner for LAMs? 

- (3) How well does LARA generalize to novel tasks and robot embodiments, and which factors are critical for effective LARA training? 

### **5.1. Experimental Settings** 

**General Experimental Settings** To ensure fair comparison with existing VLA models that vary widely in pretraining data scale and sources, we evaluate LARA under two distinct experimental settings.: 

- _OXE-Constrained Comparison_ : All models are pretrained exclusively on datasets within the scope of Open-X-Embodiment (OXE) (O’Neill et al., 2024) (see in Sec. A.3) and optionally post-trained on the target evaluation datasets. This setting offers a clean experimental setting to reveal the effect of specific model design. 

- _Unconstrained Comparison_ : We put no constraints on model design and pre-training datasets. This setting aims to reveal the true performance limit of designed models compared with state-of-the-art models. 

**Evaluation Setup** For evaluation, we assess model performance on three existing simulation benchmarks: 

- _LIBERO_ (Liu et al., 2023): We follow common posttraining and evaluation protocols (Bu et al., 2025b) and report model success rates on _LIBERO-Spatial_ , _LIBEROObject_ , _LIBERO-Goal_ , and _LIBERO-Long_ . 

- _SIMPLER-ENV_ (Li et al., 2024): We follow established post-training and evaluation protocols from villa-X (Chen et al., 2025a) and report model success rates on three task categories, including _Pick Coke Can_ , _Object Movement_ , and _Open & Close Drawer_ . 

- _GR1-Sim-24(30)_ (Bjorck et al., 2025): We follow GR00TN1 (Bjorck et al., 2025) and select the post-training setting with 30 demos for model training and report model success rates on the 24 tasks available. 

5 

**Latent Action Representation Alignment** 

_Table 1._ **Benchmark Evaluations** . We show the performance of LARA variants against existing models under the _OXE-Constrained_ and _Unconstrained_ settings. For GR00T-N1.6-LARA, we post-train GR00T-N1.6 with an OXE-pretrained LAM using LARA. 

||||_LIBERO_||||_SIMPL_|_ER-ENV_||
|---|---|---|---|---|---|---|---|---|---|
|Methods||||||||||
||Spatial|Object|Goal|Long|Average|Pick|Move|Drawer|Average|
|_OXE-Constrained Comparison_||||||||||
|OpenVLA (Kim et al.,2024)|84.7|88.4|79.2|53.7|76.5|16.3|46.2|35.6|32.7|
|Octo (Team et al.,2024)|78.9|85.7|84.6|51.1|75.1|17.0|4.2|22.7|14.6|
|Moto-GPT (Chen et al.,2025b)|-|-|-|-|-|74.0|60.4|**43.1**|61.4|
|LAPA (Ye et al.,2024)|73.8|74.6|58.8|55.4|65.7|-|-|-|-|
|LARA (_DiT-only_)|84.5|90.0|86.5|76.5|84.4|62.3|**84.0**|21.0|55.8|
|LARA (_full_)|**88.0**|**92.0**|**88.5**|**86.0**|**88.6**|**82.3**|83.7|29.5|**65.2**|
|_LARA Improvement_|+4.1%|+2.2%|+2.3%|+12.4%|+5.0%|+32.1%|-0.4%|+40.5%|+16.8%|
|_Unconstrained Comparison_||||||||||
|SpatialVLA (Qu et al.,2025)|88.2|89.9|78.6|55.5|78.1|88.0|72.7|41.8|70.7|
|CoT-VLA (Zhao et al.,2025)|87.5|91.6|87.6|69.0|81.1|-|-|-|-|
|_𝜋_0-FAST (Pertsch et al.,2025)|96.4|96.8|88.6|60.2|85.5|75.3|67.5|42.9|61.9|
|UniVLA (Bu et al.,2025b)|96.5|96.8|95.6|92.0|95.2|-|-|-|-|
|TraceVLA (Zheng et al.,2024)|-|-|-|-|-|45.0|63.8|63.1|57.3|
|Magma (Yang et al.,2025)|-|-|-|-|-|75.0|53.0|58.9|62.3|
|villa-X (Chen et al.,2025a)|**97.5**|97.0|91.5|74.5|90.1|**98.7**|75.0|**59.3**|77.7|
|DreamVLA (Zhang et al.,2025a)|**97.5**|94.0|89.5|89.5|92.6|-|-|-|-|
|GR00T-N1.6 (Bjorck et al.,2025)|**97.5**|96.0|95.5|91.0|95.0|97.3|87.0|52.3|78.9|
|GR00T-N1.6-LARA|96.5|**97.5**|**96.0**|**92.5**|**95.6**|98.0|**89.0**|52.8|**79.9**|
|_LARA Post-train Improvement_|-1.0%|+1.6%|+0.5%|+1.6%|+0.6%|+0.7%|+2.3%|+1.0%|+1.3%|


Additionally, we meticulously design a real-world robot manipulation benchmark for model performance testing: 

- _G1-Real(50)_ : In _G1-Real(50)_ , we deploy models on a realworld Unitree G1 humanoid robot and test task performance on two composite tasks: (1) _“Pick Green Tomate and Place in Green Basket”_ , and (2) _“Grasp Bottle and Pour to Cup”_ . During post-training, we provide 50 realrobot manipulation demonstrations for each task. During evaluation, we model success rates on both sub-task ( _e.g_ ., grasp first then pour) and full-task execution over 50 trials. We provide a visualization of this task in Fig. 4 and additional details for real-robot setup in Sec. C. 

### **5.2. LARA for Full VLA Training** 

**Experimental Setup** We evaluate the efficacy of LARA as a full VLA framework, encompassing both pre-training and post-training stages under the _OXE-constrained Comparison_ setting. Specifically, we provide two LARA variants under this setting with training details in Sec. A.2: 

- LARA ( _DiT-only_ ): We pre-train a vanilla DiT model described in Sec. 4.2 directly on OXE data without representation alignment and then post-train on target datasets. 

- LARA ( _full_ ): We train the full LARA model by first pre-training the LAM model on OXE data with only reconstruction loss. This LAM is used for LARA joint pretraining on OXE-data and post-training on target datasets with an DiT initialized from scratch. 

**Results & Analyses** As detailed in the top section of Tab. 1, LARA consistently outperforms existing VLA frameworks when pre-trained on OXE data, achieving a 12% and 4% overall improvements over the best baselines on _LIBERO_ and _SIMPLER-ENV_ , respectively. This includes state-of-the-art LAM-based VLA models like MotoGPT (Chen et al., 2025b) and LAPA (Ye et al., 2024). Additionally, compared to the vanilla DiT baseline, LARA (DiT-only), the full LARA pipeline reaches around 5% and 15% on LIBERO and SIMPLER, respectively, validating the effectiveness of LARA as a general and superior VLA model learning paradigm. Remarkably, despite using only OXE-data for pre-training, LARA outperforms several large-scale pre-trained models in the _Unconstrained Comparison_ setting, including _𝜋_ 0-FAST (Pertsch et al., 2025), Magma (Yang et al., 2025), and SpatialVLA (Qu et al., 2025), demonstrating its potential as a data-efficient VLA framework. 

### **5.3. LARA for Post-training Enhancement** 

**Experimental Setup** We evaluate LARA as a plugand-play post-training enhancement module for existing diffusion-based VLA models under the _Unconstrained Comparison_ setting. Due to computational constraints, we select GR00T-N1.6 (Bjorck et al., 2025) as our baselines given their strong performance on a wide range of tasks. Specifically, we create the LARA enhanced model, GR00T-N1.6LARA, by applying the full LARA objective to jointly 

6 

**Latent Action Representation Alignment** 

_Table 2._ **Quantitative results on GR1 Simulation and G1 Real-World Evaluation.** We report success rates for the _GR1-Sim-24(30)_ benchmark (24 bimanual simulation tasks, fine-tuned on 30 demonstrations per task following (Bjorck et al., 2025)) and the _G1-Real(50)_ suite. The real-world evaluation is conducted on the Unitree G1 humanoid across two multi-stage tasks ( _Pick-n-Place_ , _Grasp-n-Pour_ ), averaging performance over 50 trials per task. 

|Mthd|_GR1-Sim-24_|_G1-Re_|_al Pick-_|_n-Place_|_G_|_1-Real Gra_|_sp-n-Pour_|_G1-Real_|
|---|---|---|---|---|---|---|---|---|
|eos|Avg.|Pick|Place|Full|Grasp-Left|Grasp-Righ|t<br>Pour<br>Full|Avg.|
|_OXE-Constrained Comparison_|||||||||
|LARA (_DiT-only_)|6.4|74.0|78.4|58.0|58.0|78.0|93.1<br>54.0|56.0|
|LARA (_full_)|11.4|90.0|88.9|80.0|80.0|**84.0**|**100.0**<br>**68.0**|74.0|
|_LARA Improvement_|+78.1%|+21.6%|+13.4%|+37.9%|+37.9%|+7.7%|+7.4%<br>+25.9%|+32.1%|
|_Unconstrained Comparison_<br>GR00T-N1.6 (Bjorck et al.,2025)|47.0|90.0|84.4|76.0|78.0|80.0|87.2<br>**68.0**|72.0|
|GR00T-N1.6-LARA|**48.5**|**92.0**|**91.3**|**84.0**|**86.0**|76.0|94.4<br>**68.0**|**76.0**|
|_LARA Post-train Improvement_|+3.2%|+2.2%|+8.2%|+10.5%|+10.3%|-4.0%|+7.2%<br>+0.0%|+5.56%|
|GR1 Can to Drawer||Pick||Place|Grasp|-Left|Grasp-Right|Pour|


_Figure 4._ **Task Visualization of** **_GR1-Sim-24(30)_ and** **_G1-Real(50)_ .** We illustrate a representative bimanual task from the _GR1-Sim-24(30)_ simulation suite (left) alongside the two real-world tasks evaluated on the G1 humanoid: _Pick-n-Place_ and _Grasp-an-Pour_ (right). For a detailed frame-by-frame breakdown of the _G1-Real(50)_ execution, please refer to Fig. S.4. 

train the pre-trained GR00T-N1.6 model with an LAM (pre-trained on OXE with reconstruction loss only) on the post-training data respectively. We provide training details in Sec. A.2. In addition to the experiments conducted on GR00T-N1.6, we further apply LARA to the _𝜋_ 0 _._ 5 (Black et al., 2025) model during post-training to validate its effectiveness across different backbone architectures. Additional experimental setups and results are provided in Sec. B.1. 

**Results & Analyses** As shown in the bottom section of Tab. 1 and bottom section of Tab. 2, our LARA enhanced model consistently outperforms existing models on all benchmarks. Notably, even when applied only in the post-training stage, adding LARA substantially improves performance over the vanilla GR00T-N1.6 model and the _𝜋_ 0 _._ 5 model (see in Tab. S.3), achieving state-of-the-art performance. Compared to implicit world modeling models like DreamVLA (Zhang et al., 2025a) and UniVLA (Bu et al., 2025b) that require full model re-training, LARA post-training enhancement is significantly more efficient while achieving better performance. Moreover, since the GR-1 and G1 embodiments in Tab. 2 were not available during LAM pre-training, the performance gains demonstrate that such alignment can be efficiently achieved during only the post-training stage, further validating the data-efficiency as discussed in Sec. 5.2. 

on _GR1-Sim-24(30)_ and _G1-Real(50)_ following the _OXEConstrained Comparison_ setting. As both datasets involve embodiments absent from OXE and limited demonstration data, this experiment tests the adaptability and generalizability of LARA for new embodiments and tasks. We provide additional training details in Sec. A.2. 

**Results & Analyses** As shown in the top section of Tab. 2, we observe a tremendous performance improvement of LARA when adapting models pre-trained on OXE to novel embodiments and tasks, achieving over ∼30% performance improvements on average. This demonstrates that LARA learns embodiment-agnostic action representations from visual semantics which supports fast adaptation to novel embodiments and tasks rather than overfitting to embodimentspecific patterns, enabling stronger generalization capabilities. Nevertheless, a noticeable gap remains when compared to large-scale pre-trained models that have already seen the GR-1 and G1 embodiments, highlighting the importance of extensive pre-training. Even so, under limited demonstration settings, LARA still outperforms the vanilla GR00TN1.6 baseline on _G1-Real(50)_ , indicating strong potential when combined with larger-scale pre-training. Due to computational constraints, we leave the full-scale pre-training on all available open-source datasets to future work. 

### **5.5. LARA for Latent Action Refinement** 

### **5.4. LARA for Fast Adaptation and Generalization** 

**Experimental Setup** To further validate the dataefficiency and generalizability of LARA, we evaluate models by pre-training only on OXE data and post-training 

**Experimental Setup** To verify the reciprocal enhancement LARA provides to the LAM model, we investigate whether the alignment process improves the quality of the latent action representations for downstream tasks. We utilize 

7 

**Latent Action Representation Alignment** 

_Table 3._ **LAM and LARA-LAM Comparison in SIMPLER Evaluation.** 

|Methods|Pick Object|Move Near|Open Drawer|Close Drawer|Pick Coke Can|Avg.|
|---|---|---|---|---|---|---|
|LAM|36.3|61.0|25.7|38.0|53.0|42.8|
|LARA-LAM|**41.0**|**63.7**|**29.3**|**53.7**|**59.7**|**49.5**|
|_LARA-LAM Improvement_|+12.9%|+4.4%|+14.0%|+41.3%|+12.6%|+15.7%|


_Figure 6._ **Ablation Study on LARA Design.** We report success rates on _LIBERO-Long_ , the most challenging subset of LIBERO benchmark. 

_Figure 5._ **Attention Map Visualization for LAM and LARA-LAM.** We show attention heat maps between latent actions and image patches from LAM (up) and LARA-LAM (below) respectively, higher attention regions are marked in red. 

### **5.6. Ablation Study** 

the Moto-GPT (Chen et al., 2025b) framework as a controlled testbed, leveraging its reliance on LAM-generated latent action tokens for VLA supervision. Specifically, Moto-GPT employs a two-stage curriculum, where an initial LAM-only training phase supervise VLA models exclusively by pseudo-labels from LAMs, followed by a joint training phase that combines latent action supervisions with ground-truth action supervisions. We conduct a direct comparison of LAMs by training two distinct Moto-GPT models on the OXE Fractal dataset from scratch and testing on the _SIMPLER-ENV_ benchmark, utilizing latent tokens from a vanilla LAM and a LARA-aligned LAM (LARA-LAM) both trained on OXE data, respectively. We provide additional training details in Sec. D. 

To validate our design choices, we conduct ablations on the _LIBERO-Long_ benchmark using the _Unconstrained_ GR00TN1.6-LARA pipeline following the protocol of _LIBEROLong_ Evaluation in Sec. 5.3. 

**Alignment Depth.** We first investigate the optimal depth for injecting the LARA alignment loss in GR00T-N1.6 model. Given the DiT layers **L** , We evaluate alignment performance at various depths (specifically layers {4 _,_ 8 _,_ **L** - 2 _,_ **L** }). As shown in Fig. 6, the earlier layers lack sufficient semantic abstraction, while the final layers are too specialized. Consequently, we select the **L** − 2 layer as the optimal insertion point, offering the balance between high-level semantics and actionable motion. 

**Quantitative & Qualitative Analyses** As shown in Tab. 3, LARA-LAM outperforms the baseline LAM across all tasks, yielding an average success rate improvement of 15.7%. Given that our controlled training protocol isolates representation quality as the sole variable, these performance gains are directly attributable to the superior structure of the LARA-refined latent space. This empirically confirms that the alignment objective is bi-directional: it does not merely transfer knowledge from LAM to Policy, but establishes a reciprocal cycle where action supervision actively refines the LAM into a more robust, action-centric manifold. To qualitatively validate this refinement, we visualize the attention map between latent action tokens and patch embeddings in both models. As illustrated in Fig. 5, the LARA-LAM attention maps demonstrate a significantly sharper focus on the robot’s end-effector and interaction targets, whereas the baseline frequently attends to background distractors. This visual evidence corroborates that LARA functions as an effective inverse dynamics regularizer, suppressing visual noise to prioritize task-relevant motion features. 

Notably, this result does not imply that **L** − 2 is universally optimal across different backbone architectures. To further examine the effect of backbone architecture on alignment depth, we additionally evaluate LARA on the _𝜋_ 0 _._ 5 model, with details provided in Sec. B.1. The results show that, for _𝜋_ 0 _._ 5, applying alignment at the final layer achieves the best performance, whereas applying alignment at layer **L** − 2 leads to degraded performance. These findings suggest that the optimal alignment depth is architecture-dependent. Nevertheless, our empirical results indicate a consistent principle: LARA alignment is generally more effective in deeper layers close to the action prediction head, rather than in early layers with limited semantic abstraction. 

**Joint Optimization vs. Frozen LAM.** We further analyze the impact of jointly optimizing LAM alongside the flowbased VLA model, versus using a frozen LAM as a fixed supervision target, both aligning at DiT **L** − 2 layer. Results in Fig. 6 demonstrate that the joint optimization strategy 

8 

**Latent Action Representation Alignment** 

outperforms the frozen baseline. This empirical evidence supports our core thesis: the bidirectional information flow, where the policy informs the LAM and vice versa, is critical for maximizing performance. Additional analyses of the loss design and ablations on the loss weights _𝑤_ 1 and _𝑤_ 2 are provided in Sec. B.2. The ablation results demonstrate that, beyond the joint training strategy, the specific loss design also plays a crucial role. Moreover, the loss weights must be chosen carefully, as excessively large values may cause either the LARA alignment loss or the LAM loss to dominate the optimization process, resulting in performance degradation. 

## **6. Conclusion** 

In this work, we introduced LARA ( **L** atent **A** ction **R** epresentation **A** lignment), a novel framework designed to co-align the latent action space with the policy’s internal representations, overcoming the scarcity of robot action data. This alignment unlocks a critical reciprocal benefit: the LAM is grounded by real action trajectories, and the VLA is regularized by the LAM’s forward dynamics priors. We demonstrated the versatility of LARA across multiple paradigms, including pre-training from scratch, posttraining enhancement, and latent space refinement based on extensive experimental results. While our experiments were conducted on subsets of the OXE dataset due to computational constraints, the robust gains observed even in this data-limited regime, highlight the scalability of our approach. We hope this study serves as a foundational guide for future research into the end-to-end co-training of world models and policies, unlocking the full potential of internetscale video data for generalist robot learning. 

## **Impact Statement** 

This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none of which we feel must be specifically highlighted here. 

## **References** 

- Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 1, 2, 3, 5, 6, 7, 12 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al. _𝜋_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 1, 2 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M. R., Finn, C., Fusai, N., Galliker, M. Y., et al. _𝜋_ 0 _._ 5: a vision-language-action model with open-world generalization. In _9th Annual Conference on Robot Learning_ , 2025. 7, 13 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 1, 2, 16 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Chen, X., Choromanski, K., Ding, T., Driess, D., Dubey, A., Finn, C., et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control, 2023. _URL https://arxiv. org/abs/2307.15818_ , 2024. 2 

- Bruce, J., Dennis, M. D., Edwards, A., Parker-Holder, J., Shi, Y., Hughes, E., Lai, M., Mavalankar, A., Steigerwald, R., Apps, C., et al. Genie: Generative interactive environments. In _International Conference on Machine Learning (ICML)_ , 2024. 3 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. _arXiv preprint arXiv:2503.06669_ , 2025a. 2 

- Bu, Q., Yang, Y., Cai, J., Gao, S., Ren, G., Yao, M., Luo, P., and Li, H. Univla: Learning to act anywhere with taskcentric latent actions. In _Robotics: Science and Systems (RSS)_ , 2025b. 2, 3, 5, 6, 7 

- Chen, X., Ghadirzadeh, A., Yu, T., Wang, J., Gao, A. Y., Li, W., Bin, L., Finn, C., and Zhang, C. Lapo: Latent-variable advantage-weighted policy optimization for offline reinforcement learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2022. 2, 3 

- Chen, X., Wei, H., Zhang, P., Zhang, C., Wang, K., Guo, Y., Yang, R., Wang, Y., Xiao, X., Zhao, L., et al. Villax: enhancing latent action modeling in vision-languageaction models. _arXiv preprint arXiv:2507.23682_ , 2025a. 3, 5, 6 

- Chen, Y., Ge, Y., Li, Y., Ge, Y., Ding, M., Shan, Y., and Liu, X. Moto: Latent motion token as the bridging language for robot manipulation. In _International Conference on Computer Vision (ICCV)_ , 2025b. 2, 3, 5, 6, 8, 12, 16 

- Fang, H.-S., Fang, H., Tang, Z., Liu, J., Wang, C., Wang, J., Zhu, H., and Lu, C. Rh20t: A comprehensive robotic dataset for learning diverse skills in one-shot. _arXiv preprint arXiv:2307.00595_ , 2023. 2 

9 

**Latent Action Representation Alignment** 

- Gong, R., Huang, J., Zhao, Y., Geng, H., Gao, X., Wu, Q., Ai, W., Zhou, Z., Terzopoulos, D., Zhu, S.-C., et al. Arnold: A benchmark for language-grounded task learning with continuous states in realistic 3d scenes. In _International Conference on Computer Vision (ICCV)_ , 2023. 2 

- Goyal, R., Ebrahimi Kahou, S., Michalski, V., Materzynska, J., Westphal, S., Kim, H., Haenel, V., Fruend, I., Yianilos, P., Mueller-Freitag, M., et al. The" something something" video database for learning and evaluating visual common sense. In _Proceedings of the IEEE international conference on computer vision_ , pp. 5842–5850, 2017. 2 

- Grauman, K., Westbury, A., Torresani, L., Kitani, K., Malik, J., Afouras, T., Ashutosh, K., Baiyya, V., Bansal, S., Boote, B., et al. Ego-exo4d: Understanding skilled human activity from first-and third-person perspectives. In _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2024. 2 

- He, K., Chen, X., Xie, S., Li, Y., Dollár, P., and Girshick, R. Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 16000–16009, 2022. 12 

- Huang, C.-P., Wu, Y.-H., Chen, M.-H., Wang, Y.-C. F., and Yang, F.-E. Thinkact: Vision-language-action reasoning via reinforced visual latent planning. _arXiv preprint arXiv:2507.16815_ , 2025a. 2 

- Huang, J., Yong, S., Ma, X., Linghu, X., Li, P., Wang, Y., Li, Q., Zhu, S.-C., Jia, B., and Huang, S. An embodied generalist agent in 3d world. In _International Conference on Machine Learning (ICML)_ , 2024. 2 

- Huang, X., Wu, J., Xie, Q., and Han, K. 3drs: Mllms need 3d-aware representation supervision for scene understanding. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025b. 3 

- Jain, J., Yang, Z., Shi, H., Gao, J., and Yang, J. Elevating visual perception in multimodal llms with visual embedding distillation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. 3 

- Kachaev, N., Kolosov, M., Zelezetsky, D., Kovalev, A. K., and Panov, A. I. Don’t blind your vla: Aligning visual representations for ood generalization. _arXiv preprint arXiv:2510.25616_ , 2025. 3 

- Karamcheti, S., Nair, S., Balakrishna, A., Liang, P., Kollar, T., and Sadigh, D. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 2 

- Kim, M. J., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al. Openvla: An open-source vision-languageaction model. _arXiv preprint arXiv:2406.09246_ , 2024. 1, 2, 6 

- Lee, J., Duan, J., Fang, H., Deng, Y., Liu, S., Li, B., Fang, B., Zhang, J., Wang, Y. R., Lee, S., et al. Molmoact: Action reasoning models that can reason in space. _arXiv preprint arXiv:2508.07917_ , 2025. 2 

- Leng, X., Singh, J., Hou, Y., Xing, Z., Xie, S., and Zheng, L. Repa-e: Unlocking vae for end-to-end tuning with latent diffusion transformers. _arXiv preprint arXiv:2504.10483_ , 2025. 2, 3, 4 

- Li, C., Wen, J., Peng, Y., Peng, Y., and Zhu, Y. Pointvla: Injecting the 3d world into vision-language-action models. _IEEE Robotics and Automation Letters_ , 11(3):2506–2513, 2026. 2 

- Li, W., Zhang, R., Shao, R., He, J., and Nie, L. Cogvla: Cognition-aligned vision-language-action model via instruction-driven routing & sparsification. _arXiv preprint arXiv:2508.21046_ , 2025a. 2 

- Li, X., Hsu, K., Gu, J., Pertsch, K., Mees, O., Walke, H. R., Fu, C., Lunawat, I., Sieh, I., Kirmani, S., et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024. 5 

- Li, Z., Chen, G., Liu, S., Wang, S., VS, V., Ji, Y., Lan, S., Zhang, H., Zhao, Y., Radhakrishnan, S., et al. Eagle 2: Building post-training data strategies from scratch for frontier vision-language models. _arXiv preprint arXiv:2501.14818_ , 2025b. 2, 5, 12 

- Liang, A., Czempin, P., Hong, M., Zhou, Y., Biyik, E., and Tu, S. Clam: Continuous latent action models for robot learning from unlabeled demonstrations. _arXiv preprint arXiv:2505.04999_ , 2025. 3 

- Lin, F., Nai, R., Hu, Y., You, J., Zhao, J., and Gao, Y. Onetwovla: A unified vision-language-action model with adaptive reasoning. _arXiv preprint arXiv:2505.11917_ , 2025. 2 

- Lipman, Y., Chen, R. T., Ben-Hamu, H., Nickel, M., and Le, M. Flow matching for generative modeling. _arXiv preprint arXiv:2210.02747_ , 2022. 3 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., and Stone, P. Libero: Benchmarking knowledge transfer for lifelong robot learning. In _Advances in Neural Information Processing Systems Datasets and Benchmarks Track (NeurIPS Datasets and Benchmarks)_ , 2023. 5 

10 

**Latent Action Representation Alignment** 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., and Zhu, J. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 5 

- Luo, H., Feng, Y., Zhang, W., Zheng, S., Wang, Y., Yuan, H., Liu, J., Xu, C., Jin, Q., and Lu, Z. Being-h0: vision-language-action pretraining from large-scale human videos. _arXiv preprint arXiv:2507.15597_ , 2025. 2 

- Ma, C., Jiang, Y., Wu, J., Yang, J., Yu, X., Yuan, Z., Peng, B., and Qi, X. Unitok: A unified tokenizer for visual generation and understanding. _arXiv preprint arXiv:2502.20321_ , 2025. 3 

- Nikulin, A., Zisman, I., Tarasov, D., Lyubaykin, N., Polubarov, A., Kiselev, I., and Kurenkov, V. Latent action learning requires supervision in the presence of distractors. _arXiv preprint arXiv:2502.00379_ , 2025. 3 

- Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V., Fernandez, P., Haziza, D., Massa, F., ElNouby, A., et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 4 

- O’Neill, A., Rehman, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., Pooley, A., Gupta, A., Mandlekar, A., Jain, A., et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _International Conference on Robotics and Automation (ICRA)_ , 2024. 1, 2, 5, 12, 13, 16 

- Peebles, W. and Xie, S. Scalable diffusion models with transformers. In _International Conference on Computer Vision (ICCV)_ , 2023. 4 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., and Levine, S. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 6 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al. Spatialvla: Exploring spatial representations for visual-language-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 2, 6 

- Shi, L. X., Ichter, B., Equi, M., Ke, L., Pertsch, K., Vuong, Q., Tanner, J., Walling, A., Wang, H., Fusai, N., et al. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. _arXiv preprint arXiv:2502.19417_ , 2025. 2 

- Team, O. M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 2, 6 

- Van Den Oord, A., Vinyals, O., et al. Neural discrete representation learning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2017. 3, 12 

- Yang, J., Tan, R., Wu, Q., Zheng, R., Peng, B., Liang, Y., Gu, Y., Cai, M., Ye, S., Jang, J., et al. Magma: A foundation model for multimodal ai agents. In _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 6 

- Yao, T., Li, Y., Pan, Y., Qiu, Z., and Mei, T. Denoising token prediction in masked autoregressive models. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pp. 18024–18033, 2025. 3 

- Ye, S., Jang, J., Jeon, B., Joo, S., Yang, J., Peng, B., Mandlekar, A., Tan, R., Chao, Y.-W., Lin, B. Y., et al. Latent action pretraining from videos. _arXiv preprint arXiv:2410.11758_ , 2024. 2, 3, 5, 6 

- Yu, S., Kwak, S., Jang, H., Jeong, J., Huang, J., Shin, J., and Xie, S. Representation alignment for generation: Training diffusion transformers is easier than you think. _arXiv preprint arXiv:2410.06940_ , 2024. 2, 4 

- Zhang, W., Liu, H., Qi, Z., Wang, Y., Yu, X., Zhang, J., Dong, R., He, J., Lu, F., Wang, H., et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arXiv preprint arXiv:2507.04447_ , 2025a. 6, 7 

- Zhang, W., Wang, Y., Luo, H., Yuan, H., Feng, Y., Zheng, S., Jin, Q., and Lu, Z. Dig-flow: Discrepancy-guided flow matching for robust vla models. _arXiv preprint arXiv:2512.01715_ , 2025b. 2 

- Zhao, Q., Lu, Y., Kim, M. J., Fu, Z., Zhang, Z., Wu, Y., Li, Z., Ma, Q., Han, S., Finn, C., et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025. 2, 6 

- Zhen, H., Qiu, X., Chen, P., Yang, J., Yan, X., Du, Y., Hong, Y., and Gan, C. 3d-vla: A 3d vision-language-action generative world model. _arXiv preprint arXiv:2403.09631_ , 2024. 2 

- Zheng, R., Liang, Y., Huang, S., Gao, J., Daumé III, H., Kolobov, A., Huang, F., and Yang, J. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 6 

- Zheng, R., Wang, J., Reed, S., Bjorck, J., Fang, Y., Hu, F., Jang, J., Kundalia, K., Lin, Z., Magne, L., et al. Flare: Robot learning with implicit world modeling. _arXiv preprint arXiv:2505.15659_ , 2025. 3, 4 

11 

**Latent Action Representation Alignment** 

## **A. Training Details** 

### **A.1. Model Implementation** 

**Latent Action Model (LAM) Implementation** We adopt the architectural design from Moto-GPT (Chen et al., 2025b) for our Latent Action Model. The process operates in four stages: 

- **Visual Encoding:** The current frame _𝐼𝑡_ and the target future frame _𝐼𝑡_ + _𝐶_ are processed by a frozen, pre-trained ViT (He et al., 2022) encoder to extract patch embeddings. These embeddings are concatenated to form a unified visual feature sequence. 

- **Motion Extraction (M-Former):** These features are input to the "M-Former," a 4-layer transformer encoder equipped with 8 learnable query embeddings. The M-Former utilizes self-attention to distill the visual changes into a continuous latent representation _𝑧𝑡_ . 

- **Quantization:** The output query features are discretized using a Vector Quantization (VQ) codebook with a vocabulary size of 128, resulting in discrete latent motion tokens _𝑧𝑡_<sup>_𝑞_.</sup> 

- **Reconstruction:** Finally, the quantized tokens _𝑧𝑡_<sup>_𝑞_are fed into a decoder—comprising a 12-layer ViT (He et al., 2022)</sup> with a hidden size of 768—to reconstruct the future frame _𝐼𝑡_ + _𝐶_ . 

**Flow-based VLA Implementation** We employ Eagle-2 (Li et al., 2025b) as the vision-language backbone to process visual observations and task instructions. While the core VLM weights remain frozen, we introduce a trainable self-attention adapter to refine the VLM embeddings before they condition the diffusion process. To handle diverse robot morphologies, the action policy utilizes embodiment-specific MLP encoders. These encoders project proprioceptive states and noisy actions into a shared latent embedding space. The diffusion process is modeled by a Diffusion Transformer (DiT) comprising _𝐿_ = 16 layers, featuring alternating self-attention and cross-attention blocks (conditioned on VLM embeddings). To support scalability across diverse hardware, we instantiate the model with a capacity for up to 64 distinct embodiment IDs. We set the maximum action dimension to 32 and the state dimension to 64, using padding to accommodate the varying degrees of freedom found in diverse manipulation datasets. 

We list the implementation details of each component in Tab. S.1. 

### **A.2. Model Training** 

**Training Details:** We train the LAM on subsets of the OXE dataset (O’Neill et al., 2024), with the temporal stride ( _𝐶_ = 5) to learn the latent action every 5 frames with standard VQ-VAE (Van Den Oord et al., 2017) objective. The model is trained for 350k steps on 4 NVIDIA A100 GPUs with a global batch size of 512. We utilize the AdamW optimizer with a peak learning rate of 1 × 10<sup>−4</sup> and a cosine decay schedule (weight decay 1 × 10<sup>−5</sup> ). For further architectural specifics, we refer readers to (Chen et al., 2025b). 

**LARA (** **_DiT-only_ ) Training** For the baseline diffusion training, we optimize the flow-matching objective defined in Eq. (1). To predict continuous action, we usually predict the action chunk **A** _𝑡_ : _𝑡_ + _𝐶_ . We set _𝐶_ = 16. We train on the subset of the OXE dataset containing valid action labels. The action prediction horizon is set to 16. The model is trained for 200k steps on 4 NVIDIA A100 GPUs with a global batch size of 384. We use the AdamW optimizer with a peak learning rate of 1 × 10<sup>−4</sup> , a cosine decay schedule, and a weight decay of 1 × 10<sup>−5</sup> . 

**LARA (** **_full_ ) Joint Training** For the full LARA framework, we optimize the joint objective in Eq. (7). The LARA loss is implemented between _𝑧𝑡_ extracted from ( _𝐼𝑡 , 𝐼𝑡_ + _𝐶_ ), with _𝐶_ = 16, and aligned with _𝐿_ − 2 layer of hidden states _ℎ𝑡_<sup>_𝜃_.Crucially,</sup> to ensure temporal consistency, we select the hidden state token corresponding to the final timestep of the action chunk ( _𝑡_ + _𝐶_ ) for alignment. This constraint forces the policy’s representation of the completed action trajectory ( **A** _𝑡_ : _𝑡_ + _𝐶_ ) to match the visual effect predicted by the LAM. Based on empirical tuning, we set the loss balancing weights to _𝑤_ 1 = 0 _._ 01 and _𝑤_ 2 = 0 _._ 01. All other optimization hyperparameters (batch size, learning rate, optimizer) remain identical to the _DiT-only_ configuration to ensure a fair comparison. 

**GR00T-N1.6-LARA Post-training.** In the _Unconstrained_ setting, we initialize the model with the public GR00TN1.6 (Bjorck et al., 2025) checkpoint (pre-trained on large-scale data) and perform joint optimization using the protocol described above. We maintain the weights _𝑤_ 1 = 0 _._ 01 and _𝑤_ 2 = 0 _._ 01. The model is fine-tuned on target robot demonstrations 

12 

**Latent Action Representation Alignment** 

_Table S.1._ **Implementation Details of LAM and Diffusion-based VLA Policy with LARA.** 

|Component|Parameter|Value|
|---|---|---|
|_LAM_|||
|ViT Encoder|-|Pretrained ViT|
|M-Former|num_queries<br>num_layers|8<br>4|
|ViT Decoder|num_layers<br>num_heads|12<br>12|
|VQ Codebook|num_codes|128|
|_VLA Policy_|||
|VLM|-|Frozen Eagle v2|
|Adapter|Self-Attn<br>Layer Norm|1<br>1|
|Action Encoder|MLP|1|
|Action Decoder|MLP|1|
|State Encoder|MLP|1|
|Diffusion Model|DiT|16|
|Projector|MLP|1|
|Alignment Depth|DiT Layer|L-2|
|-|Max Num Embodiments|64|
|-|Max State Dim|64|
|-|Max Action Dim|32|


for approximately 20k steps, with the exception of the _GR1-Sim-24(30)_ benchmark, which is trained for 50k steps due to higher task complexity. We use a learning rate of 1 × 10<sup>−4</sup> and a global batch size of 384 on 4 NVIDIA A100 GPUs. This post-training setup is consistent across LARA ( _full_ ), LARA ( _DiT-only_ ), and the GR00T-N1.6 baseline. 

We summarize the training hyperparameters in Tab. S.2. 

### **A.3. Training Dataset** 

We curate a targeted subset of the Open XEmbodiment (OXE) dataset (O’Neill et al., 2024), specifically filtering for trajectories featuring single-arm end-effector control. The detailed composition and distribution of these subsets are visualized in Fig. S.1. To tailor the data for distinct learning objectives, we employ different temporal strides ( _𝐶_ ). For LAM pre-training, we set a shorter horizon of _𝐶_ = 5 to capture fine-grained visual motion dynamics. Conversely, for the VLA policy training, we extend the horizon to _𝐶_ = 16 to match the length of the predicted action chunks. To address the variance in dataset sizes within OXE, we adopt a balanced sampling strategy where each subset is sampled with equal probability, preventing the model from overfitting to dominant data sources. 

## **B. Additional Experimental Results** 

### **B.1. Joint LARA Post-training with** _𝜋_ 0 _._ 5 

To further validate the effectiveness of LARA as a plug-and-play module, we integrate LARA with the pretrained _𝜋_ 0 _._ 5 (Black et al., 2025) model. We post-train _𝜋_ 0 _._ 5-LARA on the LIBERO dataset for 20k steps, following the post-training recipe of _𝜋_ 0 _._ 5. The LARA alignment loss is applied to the final layer, _e.g_ ., layer **L** , of the _𝜋_ 0 _._ 5 backbone, immediately before the action decoder. We use loss weights _𝑤_ 1 = 0 _._ 01 and _𝑤_ 2 = 0 _._ 01. Additionally, we evaluate applying the alignment loss at layer **L** − 2, with results reported in Tab. S.3. 

As shown in Tab. S.3, LARA consistently improves upon the already strong performance of the base model across the LIBERO benchmark. Moreover, the optimal alignment depth depends on the backbone architecture and must be chosen carefully. While the exact optimal layer index varies across architectures, our empirical findings suggest a consistent 

13 

**Latent Action Representation Alignment** 

_Table S.2._ **Training Hyperparameters for models.** 


_Figure S.1._ **Training Data Distribution.** Visualization of the dataset mixtures used for both LAM pre-training and LARA policy training. 

_Table S.3._ **Comparison of** _𝜋_ 0 _._ 5 **and** _𝜋_ 0 _._ 5 **-LARA in LIBERO.** 

|Methods|Spatial|Object|Goal|Long|Average|
|---|---|---|---|---|---|
|_𝜋_0_._5|98.8|98.0|98.2|92.4|96.9|
|_𝜋_0_._5-LARA (L-2 layer)|97.0|99.0|87.5|83.5|91.2|
|_𝜋_0_._5-LARA (L layer)|**99.0**|**98.5**|**99.0**|**94.5**|**97.8**|
|_LAM Improvement_|+0.2%|+0.5%|+0.8%|+2.1%|+0.9%|


principle: alignment is more effective in deeper layers close to the action prediction head. 

### **B.2. Loss Designs and Weights Ablation** 

We further ablate the use of the LARA loss and the LAM loss to verify the importance of the loss design. The experimental setup follows the ablation study in Appendix 5.6. Specifically, we evaluate GR00T-N1.6-LARA on the LIBERO-Long dataset. In addition, we conduct an ablation study on the loss weights, varying them from 0.0001 to 1.0. The results are presented in Fig. S.2. 

As shown in Fig. S.2, joint training with both the LARA loss and the LAM loss achieves the best performance. The LARA loss is essential, as it regularizes the feature space and enables the policy and the LAM to mutually enhance each other, thereby achieving the strongest performance. For the loss-weight ablation, the optimal setting is _𝑤_ 1 = 0 _._ 01 and _𝑤_ 2 = 0 _._ 02. In contrast, larger weights, such as 0.1 or 1.0, degrade action prediction accuracy, as the LARA alignment loss and the LAM loss begin to dominate model training. Unless otherwise specified, we use weights of 0.01 across all tasks and settings. 

14 

**Latent Action Representation Alignment** 

_Figure S.2._ **Loss Designs and Weights Ablation.** We evaluate various weights and the two regularization losses in the LIBERO-Long dataset. 

|_.._ **oss esgns an egts**<br>te various weights and the two <br>in the LIBERO-Long dataset.|**aton.** e<br>regularization|Ego-view camera<br>(Realsense D455)<br>14-DoF Humanoid Robot Bimanual Arms<br>(Unitree G1)<br>2-DoF Head Motor|
|---|---|---|
|Methods|Long|6DF Rbi Hd × 2|
|_𝑤_1 =0_._0001&_𝑤_2 =0_._0001<br>_𝑤_1 =0_._001&_𝑤_2 =0_._001<br>_𝑤_1 =0_._01&_𝑤_2 =0_._01<br>_𝑤_1 =0_._1&_𝑤_2 =0_._1<br>_𝑤_1 =1_._0&_𝑤_2 =1_._0|91.5<br>91.0<br>**92.5**<br>89.5<br>86.5|-o ootc an<br>(Inspire Robots RH56DFTP)|
|w/oL_𝐿𝐴𝑅𝐴_<br>w/oL_𝐿𝐴𝑀_|88.0<br>89.5<br>_Figure S.3._ <br>|**Real-world setup with the Unitree G1 humano**<br>|


_Figure S.3._ **Real-world setup with the Unitree G1 humanoid.** The robot is equipped with Inspire Hands and a 2-DoF actuated head mounting an Intel RealSense D455 RGB camera for first-person observations. 

## **C. Details on Real World Experiments** 

**Hardware.** All real-world experiments are conducted on a Unitree G1 humanoid equipped with Inspire Hands and a actuated head for camera reorientation (shown in Fig. S.3). To increase the first-person field of view (FoV), we use the head-mounted Intel RealSense D455 to capture RGB observations. 

**Control Interface.** All policy operates on a 28-dimensional state and outputs a 28-dimensional action. The controlled DoFs consist of 14 upper-body arm DoFs (7 DoFs per arm), 12 hand DoFs (6 DoFs per hand), and 2 head DoFs (yaw and pitch). During experiments, the robot is suspended by a gantry crane for safety and stability. 

**Data collection.** We collect real-world VLA training data by teleoperating the G1 using Apple Vision Pro. We consider two manipulation tasks: (i) pick-and-place and (ii) pouring. For each task, we collect 50 demonstrations (examples shown in Fig. S.4). For both tasks, the object poses are randomized within a 10 cm × 10 cm region. 

**Tasks Evaluation Metrics.** For the two tasks, each task is evaluated over 50 trials. The inference denoising step is 4, and the action horizon is 8. 

**(1) Single-Arm Pick-and-Place.** _Instruction: "Pick the Green Tomato and Place in the Green Basket."_ This task evaluates the sim-to-real transfer capability of LARA ( _full_ ) when trained only on OXE data, compared to the GR00T-N1.6 baseline which benefits from large-scale pre-training (see in Tab. 2). Success is decomposed into stages: 

- **Pick (SRPick):** The robot successfully grasps and lifts the tomato (e.g., Frame 4 in Fig. S.4). 

- **Full (SRFull):** The tomato is successfully placed into the target basket (e.g., Frame 5). 

- **Place (SRPlace):** We define the conditional success rate for the placement phase (SRPlace) as the probability of success given a successful pick: 


**(2) Bimanual Pouring.** _Instruction: "Grasp the Bottle and Pour to the Cup."_ This task serves as a challenging benchmark for bimanual coordination, with varying embodiment gap, task gap compared with our training dataset. Success is tracked for each effector: 

- **Grasp-Left (SRGL):** The left hand successfully grasps the cup (e.g., Frame 4). 

- **Grasp-Right (SRGR):** The right hand successfully grasps the bottle ( _e.g_ ., Frame 5). 

- **Full (SRFull):** Liquid (or proxy object) is successfully poured from the bottle to the cup (e.g., Frame 6). 

- **Pour (SRPour):** Since the pouring action requires the successful execution of both grasps, we define the conditional success rate for pouring (SRPour) as: 


_Note: We assume independence between the grasp success probabilities for the normalization factor._ 

15 


_Figure S.4._ Visualization of real-world tasks. 

## **D. LARA-LAM for Latent Action Refinement** 

**Moto-GPT Vanilla Pipeline.** The vanilla SIMPLER pipeline in Moto-GPT (Chen et al., 2025b) consists of three stages: (1) latent tokenizer pre-training, which utilizes a subset of Open-X-Embodiment (O’Neill et al., 2024) including 109k real- world trajectory video covering various embodiments; (2) Moto-GPT pre-training, which utilizes the same Open-XEmbodiment subset to supervise the VLA model **only** with latent action tokens; and (3) Moto-GPT co-fine-tuning, which additionally uses 73k expert trajectories with action labels from RT-1 (Brohan et al., 2022), the loss in Stage-3 contains both the latent action tokens prediction loss and the real action prediction loss. The evaluation on SIMPLER includes three tasks based on the Google-Robot embodiment: Pick Coke Can, Move Near, and Open/Close Drawer. 

**Our implementation.** We directly begin with our pre-trained LAM while skipping the first stage of Moto-GPT. We then proceed to perform Moto-GPT stage-2 and stage-3 training with our pre-trained LAM. Notably, for training efficiency, in this experiment we use a smaller dataset (OXE Fractal dataset) for Moto-GPT stage-2 pre-training, and stage-3 co-fine-tuning. We compare the following two variants: 

- **LAM.** We directly use our stage-1 pre-trained LAM to guide the Moto-GPT stage-2 pre-training, and then continue to perform Moto-GPT stage-3 co-fine-tuning in OXE Fractal dataset. 

- **LARA-LAM.** We use our trained LARA-LAM for the training of Moto-GPT stage-2 and stage-3 in OXE Fractal dataset. In contrast to the vanilla LAM, the LARA-LAM undergoes an extra LARA _joint pre-training_ stage to verify whether LARA joint pre-training yields better latent action representation. 

16 

