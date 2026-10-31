---
title: "Align-Then-stEer: Adapting the Vision-Language Action Models through Unified Latent Guidance"
date: "2025-09-02"
authors: "Yang Zhang; Chenwei Wang; Ouyang Lu; Yuan Zhao; Yunfei Ge; Zhenglong Sun"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2509.02055
pdf: https://arxiv.org/pdf/2509.02055
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2509.02055)** / [論文ページ](https://arxiv.org/abs/2509.02055)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **Align-Then-stEer: Adapting the Vision-Language Action Models through Unified Latent Guidance** 

**Yang Zhang**<sup>1</sup><sup>_,_2</sup><sup>_†_</sup> , **Chenwei Wang**<sup>1</sup><sup>_,_3</sup><sup>_†_</sup> , **Ouyang Lu**<sup>1</sup><sup>_,_4</sup><sup>_†_</sup> , **Yuan Zhao**<sup>1</sup> , **Yunfei Ge**<sup>1</sup> , **Zhenglong Sun**<sup>3</sup> , **Xiu Li**<sup>2</sup> , **Chi Zhang**<sup>1</sup> , **Chenjia Bai**<sup>1</sup><sup>_∗_</sup> , **Xuelong Li**<sup>1</sup><sup>_∗_</sup> 

> 1Institute of Artificial Intelligence, China Telecom, 2Tsinghua University, 3The Chinese University of Hong Kong, Shenzhen,<sup>4</sup> Northwestern Polytechnical University 

> _†_ Equal Contributions *Corresponding Authors 

Vision-Language-Action (VLA) models pre-trained on large, diverse datasets show remarkable potential for general-purpose robotic manipulation. However, a primary bottleneck remains in adapting these models to downstream tasks, especially when the robot’s embodiment or the task itself differs from the pre-training data. This discrepancy leads to a significant mismatch in action distributions, demanding extensive data and compute for effective fine-tuning. To address this challenge, we introduce **Align-ThenstEer ( ATE )** , a novel, data-efficient, and plug-and-play adaptation framework. ATE first aligns disparate action spaces by constructing a unified latent space, where a variational autoencoder constrained by reverse KL divergence embeds adaptation actions into modes of the pre-training action latent distribution. Subsequently, it steers the diffusion- or flow-based VLA’s generation process during fine-tuning via a guidance mechanism that pushes the model’s output distribution towards the target domain. We conduct extensive experiments on cross-embodiment and cross-task manipulation in both simulation and real world. Compared to direct fine-tuning of representative VLAs, our method improves the average multi-task success rate by up to **9.8%** in simulation and achieves a striking **32% success rate gain** in a real-world cross-embodiment setting. Our work presents a general and lightweight solution that greatly enhances the practicality of deploying VLA models to new robotic platforms and tasks. 

**Date:** September 2, 2025 **Project:** https://align-then-steer.github.io/ **Code:** https://github.com/TeleHuman/Align-Then-Steer **Correspondence to:** Chenjia Bai (baicj@chinatelecom.cn) 


### **1 Introduction** 

Vision-Language Action models (VLAs) (Brohan et al., 2022; Zitkovich et al., 2023; Kim et al., 2024; Black et al., 2024) have emerged as a powerful solution to empower general-purpose robotic manipulation with broad generalization in tasks and environments. Inspired by the success in scaling data and parameters of Large Language Models (LLMs) and Visual-Language Models (VLMs), the VLA models extend the pre-trained VLM models (Li et al., 2023; Driess et al., 2023; Beyer et al., 2024; Wang et al., 2024) by integrating an action expert module to generate low-level actions, thereby inheriting the common knowledge, semantic reasoning, and instruction-following capabilities of VLMs to facilitate policy learning. Specifically, a representative training recipe for VLA typically consists of two phases: a (i) _pre-training phase_ : pretrain the entire VLA model that contains a strong VLM and an action expert on a large corpus containing cross-embodiment datasets (Jang et al., 2021; Collaboration et al., 2023; Khazatsky et al., 2024), which spans diverse robots and tasks to learn a general visuomotor prior at scale, and an (ii) _adaptation phase_ : fine-tune the VLA model on a narrowly curated dataset tailored to a particular robot platform and associated tasks, aiming to enhance the manipulation abilities in specific downstream domains. 

Though the two-phase paradigm is efficient, it becomes challenging when downstream domains adopt embodiments differing from those in pre-training. For instance, the datasets for pre-training mainly employ various single-arm robots, while the target embodiment might instead utilize dual-arm platform or humanoid robots. 

1 


**Figure 1** We present ATE, a plug-and-play adaptation framework for pre-trained Vision-Language-Action (VLA) models. Unlike prior methods that directly fine-tune VLAs, ATE aligns disparate action spaces into a unified latent representation and steers the VLA’ s generation via guidance, enabling data-efficient cross-task and cross-embodiment adaptation. This framework is evaluated in simulation on RoboTwin and ManiSkill benchmarks, as well as on a real-world dual-arm RealMan 7-DoF robot, demonstrating strong generalization, bimanual dexterous coordination, and minute-level long-horizon manipulation, achieving substantial gains in multi-task success rates. 

Since VLAs rely on imitation learning that is closely tied to action labels, the discrepancy in adaptation arises as the action spaces and, correspondingly, the action distributions are significantly different from those in the pretraining dataset, often necessitating extensive data collection for the new embodiment. Furthermore, even with the same robot platform, differences in tasks and deployment setup also lead to significant mismatches in the action distributions of the two phases. Recent approaches try to develop adaptation techniques by reducing the training cost at the parameter level (Kim et al., 2024; Zhang et al., 2025b), or by exploring different design decisions (Kim et al., 2025; Pertsch et al., 2025). However, they often struggle to address discrepancies in task distributions and overlook the embodiment mismatches that are significantly more challenging to resolve. As a consequence, efficient adaptation becomes the primary bottleneck for specific robot deployments in target domains. This motivates the central question of this paper: how can we achieve _VLA adaptation for both cross-embodiment and cross-task scenarios under a limited data regime?_ 

To this end, we propose a data-efficient adaptation method, named **Align-Then-stEer( ATE )** , for cross-embodiment and cross-task VLA adaptation by explicitly mitigating action-distribution mismatch via a two-stage strategy. In the first stage, we construct a unified latent action space to bridge the domain gap between embodiments and tasks involved during pre-training and the adaptation phases. It is achieved by training a standard Variational Autoencoder (VAE) on the pre-training action-labeled dataset to obtain a latent prior, followed by learning a smaller VAE on limited adaptation data with a reverse KL divergence constraint toward the learned pre-trained latent distribution. Thanks to the mode-seeking behavior of reverse KL divergence, this encourages the encoded latent of the target embodiment’s actions to be embedded into a specific mode of the learned prior, yielding a unified and hierarchically structured latent space. In the second stage, inspired by classifier-guided diffusion models (Dhariwal and Nichol, 2021; Bansal et al., 2023), we design a guidance function grounded in the shared latent space that can be seamlessly integrated into the training objective 

2 

of diffusion- or flow-based VLAs. This classifier guidance steers the output distribution of the pre-trained VLA toward that of the target embodiment and task, enabling faster and precise adaptation under limited data. Notably, our method requires no modification to the original VLA architecture and introduces only negligible overhead, i.e., adaptation is highly efficiently achieved by training two separate lightweight VAEs. An overview of our method is given in Fig. 1. 

Our key contributions are summarized as follows: 

- We propose a novel alignment strategy to bridge the action-distribution gap between pre-training and adaptation. By leveraging the mode-seeking behavior of reverse KL, our method constructs a unified, structured latent space that embeds target actions into modes of the pre-training latent distribution. 

- We introduce a classifier-guidance mechanism that operates within this unified latent space to explicitly steer the VLA’s output distribution. This enables precise and rapid adaptation to new embodiments and tasks, without requiring additional data. 

- The proposed ATE framework is model-agnostic and plug-and-play, seamlessly integrating with various diffusion- or flow-based VLAs without modifying their architecture and with negligible computational overhead. 

- We validate our method across different embodiments and tasks in both simulated and real-world manipulation settings. The result demonstrates consistent improvements over baselines that rely on direct supervised fine-tuning, highlighting our approach’s superior adaptation efficiency. 

### **2 Related Works** 

**Vision-Language-Action Models.** The long-term objective of robotic manipulation is to develop general-purpose models that can adapt to diverse embodiments and tasks. Vision-Language-Action models (VLAs) is currently a mainstream approach that builds upon the perception and language understanding capabilities of pretrained VLMs and introduces an additional action prediction module. Leveraging massive datasets of robotic demonstrations for joint pretraining, these models can process language instructions, visual observations, and proprioceptive input to generate continuous action sequences that interact with the physical environment to accomplish complex real-world tasks. Early representative works such as Octo and RT-1 (Brohan et al., 2022; Team et al., 2024) trained Transformer-based policies from scratch on large-scale robotic datasets, while RT-2 and OpenVLA (Zitkovich et al., 2023; Kim et al., 2024) further utilized pre-trained VLMs (e.g., PaLI-X, Prismatic) (Chen et al., 2023a; Anschütz and Le Bras, 2023) and fine-tuned them on robot datasets (e.g., OXE) (Collaboration et al., 2023) via action discretization, achieving improved capabilities by inheriting the knowledge of VLMs. Subsequent methods such as RDT-1B, H-RDT, DexVLA, DiVLA, DexGraspVLA, Dita, and etc. (Liu et al., 2024; Bi et al., 2025; Wen et al., 2025a,c; Zhong et al., 2025; Hou et al., 2025) adopt diffusion-based architectures to represent the multimodality in robot data. Recently, a new generation of VLA models—such as π0, GROOT, π0.5, SmolVLA, and TinyVLA (Black et al., 2024; NVIDIA, 2025; Intelligence et al., 2025; Shukor et al., 2025; Wen et al., 2025b) adopt a dual system compositional architecture that incorporates a generative action expert based on diffusion or flow matching (Liu et al., 2023a; Lipman et al., 2023) to produce continuous action sequences, significantly improving the prediction accuracy and physical executability. However, they mostly focus on architectures and objectives in the pre-training phase, while we aim to improve the efficiency for cross-embodiment and cross-task adaptation on pretrained VLAs. 

**Policy Adaptation of VLAs.** Despite the promise of VLAs for general-purpose robot manipulation, current approaches still suffer from high fine-tuning costs for embodiment and task mismatches. Several approaches construct latent action representation for different data sources (Ye et al., 2025; Bu et al., 2025; NVIDIA, 2025), perform Kinematics retargeting or eigengrasps (Bauer et al., 2025; Yuan et al., 2025), or manually design a physically interpretable action space for different robot platforms (Liu et al., 2024; Zheng et al., 2025), while they cannot easily adapt to different robot platforms since the target action distribution can be significantly different from the original one. RoboOS adopts advanced architectures by building skill library and shared action space for different embodiments, while is require complex module construction and coupling. Other works improve the adaptation efficiency of VLAs by caching visual tokens and selectively updating task-relevant ones (Xu et al., 2025), compressing high-frequency action sequences into low-frequency tokens 

3 

via discrete cosine transform (Pertsch et al., 2025), adopting LoRA-based update (Wen et al., 2025b), or performing dynamic layer activation for distillation (Zhang et al., 2025a). However, theses methods are often restricted to auto-regressive manner and overlook the diffusion and flow-matching architectures. Meanwhile, solely increasing the training efficiency is still limited in cross-embodiment adaptation as the domain gap would be hard to bridge via direct tuning. In contrast, we take a novel perspective by using mode seeking property of VAEs to bridge the gap of action distributions in pre-train and adaptation, and also employ latent guidance that are seamless compatible for diffusion and flow-matching VLAs. More discussion on the recent works of constructing unified action spaces to enhance the ability of VLAs are provided in the Appendix A. 

### **3 Preliminaries** 

**Training objective of VLAs.** The training of VLA models typically contains two stages: (i) obtain an initial policy via pre-training the model on a cross-embodiment action-labeled dataset _D_ pretrain, where we denote the set of embodiments included in it as _M_ pretrain = _{E_ 1 _, E_ 2 _, . . . , En}_ ; (ii) finetune the policy on a narrow but high-quality dataset _D_ adaptation collected from the target embodiment _E_ target for downstream applications. Formally, the optimization objective of the VLA policy _πθ_ is to maximize the log-likelihood of an action chunk **a** _t_ : _t_ + _h_ given an observation **o** _t_ and a language-format task instruction _l_ sampled from the dataset, which can be formulated as follows: 


where **o** _t_ contain single-view or multi-view RGB observations **I**<sup>1</sup> _t_<sup>_,_</sup><sup>**I**2</sup> _t_<sup>_, . . . ,_</sup><sup>**I**</sup><sup>_n_</sup> _t_<sup>,andtheproprioceptivestate</sup><sup>**q**</sup><sup>_t_</sup> usually describes the joint position and angle of the robot. 

**Diffusion Models and Flow Matching.** Diffusion models (Sohl-Dickstein et al., 2015; Ho et al., 2020; Song et al., 2021) are generative models where data generation is modeled as a denoising process. Consider a forward diffusion process that gradually adds Gaussian noise to samples **x** 0 _∼ q_ ( **x** 0) over _T_ steps and produces a sequence of noisy samples **x** 1 _, . . . ,_ **x** _T_ that satisfies _q_ ( **x** 1: _T |_ **x** 0) =<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_q_(</sup><sup>**x**</sup><sup>_i|_</sup><sup>**x**</sup><sup>_i−_1)and</sup><sup>_q_(</sup><sup>**x**</sup><sup>_t|_</sup><sup>**x**</sup><sup>_t−_1) =</sup> _N_ ( **x** _t_ ;<sup>_~~√~~_</sup> _<u>αt</u>_ **<u>x</u>** _t−_ 1 _,_ (1 _− αt_ ) _I_ ), where _{αt ∈_ (0 _,_ 1) _}_<sup>_T_</sup> _t_ =1<sup>isapredefinednoisescheduler.Thedenoisingdiffusion</sup> model reverses the above process to approximate the data distribution _pθ_ ( **x** 0) which is parameterized as _pθ_ ( **x** 0) = � _p_ ( **x** 0: _T_ ) _d_ **x** 1: _T_ = � _p_ ( **x** _T_ )<sup>�</sup><sup>_T_</sup> _t_ =1<sup>_pθ_(</sup><sup>**x**</sup><sup>_t−_1</sup><sup>_|_</sup><sup>**x**</sup><sup>_t_)</sup><sup>_d_</sup><sup>**x**1:</sup><sup>_T_.</sup> By minimizing the following denoising loss function introduced by Ho et al. (2020), 


we can get a noise prediction network _ϵθ_ ( **x** _t, t_ ) to perform the reverse diffusion process - it begins by sampling **x** _T ∼N_ (0 _, I_ ), and then iteratively applies the update 


where _ϵk ∼N_ (0 _, I_ ), and _σk_ is a function of _k_ and depends on the noise scheduler. 

Beyond denoising diffusion, flow matching is another generative modeling framework that implements data generation as a probability path from a known source distribution to the data target distribution (Lipman et al., 2023; Liu et al., 2023b; Lipman et al., 2024). Assuming the source sample and target sample are denoted as **x** 1 and **x** 0 respectively, and flow matching timesteps are denoted as _τ ∈_ [0 _,_ 1]. By instantiating the path as a linear-Gaussian path given by **x** _τ ∼N_ ( _τ_ **x** 0 _,_ (1 _− τ_ ) _I_ ), flow matching operates by first sampling noise from a standard Gaussian and then processes this noise through a deterministic process to produce a sample from the target distribution, similar to the denoising process. The flow _vθ_ that maintains the probability path is typically trained via optimizing a simple conditional flow matching loss function, 


In robotic manipulation, there can be dozens of possible actions **a** _t_ to accomplish the task given the same language instruction _l_ and observation. Motivated by the capability of diffusion models and flow matching on 

4 


**Figure 2 The overview of ATE framework.** (a) In the first stage, we construct a unified action space to bridge the embodiment gap in pretraining and adaptation stages by utilizing the mode-seeking behavior of asymmetric VAEs. (b) In the second stage, we integrate classifier guidance in diffusion and flow-based VLAs to steer the pretrained policy towards the target action distribution with specific robot platforms. 

providing high-precision continuous representation and modeling multi-modal distribution, recent VLAs (Black et al., 2024; Liu et al., 2024; Intelligence et al., 2025; Bjorck et al., 2025) have incorporated diffusion-based or flow-based action prediction to boost performance. 

**Problem Setting.** In this work, we assume access to a pre-trained diffusion-based or flow-based policy, which can be either a VLA model or Vision-Action model like Diffusion Policy (Chi et al., 2023). Our goal is to adapt the pretrained model in _D_ pretrain to a specific embodiment _E_ target given an adaptation dataset _D_ adaptation, where _E_ target is not be involved in pre-training, i.e., _E_ target _∈M/_ pretrain. In addition, the tasks contain in _D_ adaptation can also be significantly different from that in pre-training. For clarity, we use the superscript _k_ to denote the diffusion or flow-matching timestep, and the subscript _t_ to denote the trajectory timestep. 

### **4 Methodology** 

The proposed ATE algorithm mainly consists of two stages: (i) we extract a unified action latent space to compactly encompass the actions of different embodiments, thus bridging the domain gap between the embodiments in the pre-training and adaptation phase (details in Section 4.1); (ii) then, we design a guidance 

5 

function grounded in the unified latent space and leverage the resulting classifier guidance to explicitly steer the fine-tuning towards our desired data distribution during adaptation (details in Section 4.2). Fig. 2 provides an overview of our entire procedure. 

#### **4.1 Alignment through Unified Action Latent Space** 

A pre-trained VLA acquires a general visuomotor prior by modeling the distribution _p_ ( **a** ¯ _t_ : _t_ + _H−_ 1 _|_ **o** _t, l_ ), where the action chunk **a** ¯ _t_ : _t_ + _H−_ 1 of length _H_ , observation **o** _t_ and language instruction _l_ are sampled from the pre-training data _D_ pretrain. Such a prior effectively captures the action distribution _pD_ pretrain( **a** ¯ _t_ : _t_ + _H−_ 1) from the pre-training embodiments _M_ pretrain. However, due to the inherent differences in degrees of freedom (DoFs) and physical representation (e.g., joint angles, end-effector poses, and joint torques), the raw action-labeled data from the target embodiment _E_ target can vary significantly from the action generated by the pre-trained VLA. This leads to a substantial **domain gap** that hinders efficient adaptation. To bridge this gap, we employ two distinct Variational Autoencoders (VAEs) to encode the fundamentally disparate pre-training and adaptation action data into a single, unified, and compact action latent space. 

**Learning Pre-training Action Latent.** We construct a pre-training action-VAE _V_ pretrain := _{_ **E** _ϕ,_ **D** _ϕ}_ to compress all possible action chunks in the pre-training data into a low-dimensional latent space _Z_ , which consists of a Transformer encoder **E** _ϕ_ and a Transformer decoder **D** _ϕ_ . The encoder takes an action chunk **a** ¯ _t_ : _t_ + _H−_ 1 of length _H_ as input, and outputs the parameters of a Gaussian distribution _qϕ_ ( _z|_ **a** ¯ _t_ : _t_ + _H−_ 1) to represent the action latent. Then we use the reparameterization trick to sample a latent vector _z ∈_ R<sup>_d_</sup> . Inspired by prior work on motion sequence VAEs (Petrovich et al., 2021; Chen et al., 2023b), we similarly prepend two learnable tokens, _µ_ token and Σtoken, to the input. The corresponding outputs from the encoder are then used to convert fixed-length action chunks into a single, chunk-level latent representation. The decoder, built upon a Transformer decoder with a cross-attention mechanism, takes _H_ zero embeddings as a query and the latent vector _z_ as key and value, and generates a reconstructed action chunk of length _H_ . 

We instantiate _V_ pretrain as an InfoVAE (Zhao et al., 2017) rather than a vanilla VAE (Kingma and Welling, 2013). Formally, it is optimized by maximizing the log-likelihood term together with a KL regularization term towards the fixed latent prior distribution and a mutual information maximization term that encourages high mutual information between **a** ¯ _t_ : _t_ + _H−_ 1 and _z_ . The objective can be simplified as, 


where _V_ pretrain is parameterized by _ϕ_ , _pD_ ( **a** ¯ _t_ : _t_ + _H−_ 1) is an abbreviation for _pD_ pretrain( **a** ¯ _t_ : _t_ + _H−_ 1), and _α_ and _λ_ are hyperparameters that control penalty strength. The latent prior _p_ ( _z_ ) is set as a unit Gaussian _N_ (0 _, I_ ). 

**Embedding Adaptation Action Latent into Pre-training Action Latent Space.** With the pre-training action VAE _V_ pretrain, we can obtain the learned action latent distribution _qϕ_ ( _z_ ) by marginalizing over all action chunks in _D_ pretrain. To create a unified action latent space, we train a separate adaptation action VAE _V_ adaptation := _{_ **E** _ψ,_ **D** _ψ}_ which is parameterized as _ψ_ , with a KL regularization towards the learned pre-training action latent distribution. Denoting the action chunk of length _L_ in the adaptation data as **a** ˜ _t_ : _t_ + _L−_ 1, the learning objective of _V_ adaptation is written as follows, 


where _pD_ ( **a** ˜ _t_ : _t_ + _L−_ 1) is an abbreviation for _pD_ ( **a** ˜ _t_ : _t_ + _L−_ 1) _pD_ adaptation( **a** ˜ _t_ : _t_ + _L−_ 1). The adaptation action VAE has the same architecture and variant as the pre-training VAE. Minimizing the reverse KL divergence _D_ KL( _qψ_ ( _z|_ **a** ˜ _t_ : _t_ + _L−_ 1) _∥qϕ_ ( _z_ )) instead of _D_ KL( _qϕ∥qψ_ ) ensures that the learned adaptation action latent distribution is mode-seeking (Bishop and Nasrabadi, 2006). Therefore, this effectively embeds the adaptation latent distribution _qψ_ ( _z_ ) into one mode of the pre-trained action latent distribution _qϕ_ ( _z_ ), yielding a unified and compact latent space _Z_ . 

**Implementation Details.** The purpose of using two VAEs is to bridge the distribution gap of the output action chunks between the pre-trained VLA and the adaptation data. Thus, the pre-training VAE _V_ pretrain uses 

6 

the same action chunk length _H_ as in the pre-training phase, while the adaptation action VAE _V_ adaptation adopts the action chunk length _L_ used in the adaptation phase. Following the guidelines of Zhao et al. (2017), we replace the last KL term in both Eq. (5) and Eq. (6) with Maximum-Mean Discrepancy (Li et al., 2015; Dziugaite et al., 2015) for more tractable optimization. The learned pre-training action latent distribution _qϕ_ ( _z_ ) in Eq. (6) is approximated as _N_ ( _µϕ,_ Σ _ϕ_ ), where _µϕ_ and Σ _ϕ_ are calculated over all sampled pre-training action latents. A detailed algorithm for training both VAEs is provided in Alg. 1. 

#### **4.2 Classifier Guidance for Steering Adaptation** 

To facilitate efficient adaptation of a pre-trained diffusion or flow-based VLA, we introduce the classifier guidance (Dhariwal and Nichol, 2021) to explicitly steer the fine-tuning process. The core idea is to design a guidance function that measures the discrepancy between the generated actions and the target action distribution within the unified latent space _Z_ , and then use the gradient of this function to guide the policy update. This approach enables highly efficient adaptation without requiring additional data budget. In the following, we first introduce the formulation of classifier guidance in diffusion and flow-based VLAs; then we detail the guidance function according to the learned latent action space. 

**ClassifierGuidanceinDiffusion-basedVLAs.** Note that the action latent _z_ is only determined by the action chunk **a** _t_ : _t_ + _h_ , i.e., independent of the observation **o** _t_ and language instruction _l_ . As the conditioning label we use for guidance is based solely on the latent _z_ , we thus omit these conditions and treat it as an unconditional diffusion model _πθ_ ( _·_ ) := _pθ_ ( _·_ ) for notational simplicity. A diffusion model typically predicts the noise _ϵθ_ ( **a**<sup>_k_</sup> _t_ : _t_ + _h_<sup>_, k_)</sup> that corrupts an initial action chunk **a**<sup>0</sup> _t_ : _t_ + _h_<sup>toanoisyversion</sup><sup>**a**</sup><sup>_k_</sup> _t_ : _t_ + _h_<sup>.AccordingtoLuo(2022),byTweedie’s</sup> Formula, it can be used to derive a score function, 


To generate a desired action chunk conditioned on a label _y_ , we have to sample from the conditional distribution _pθ_ ( **a**<sup>_k_</sup> _t_ : _t_ + _h_<sup>_|y_).UsingBayes’rule,thescorefunctionforthisconditionaldistributionis:</sup> 


By substituting the score function in Eq. (7), we obtain a calibrated noise prediction _ϵ_ ˆ that incorporates the guidance gradient _g_ = _∇_ **a** _kt_ : _t_ + _h_<sup>log</sup><sup>_p_(</sup><sup>_y|_</sup><sup>**a**</sup> _t_<sup>_k_</sup> : _t_ + _h_<sup>),whichcorrespondstothescoreofthejointdistributionofthe</sup> action chunk and the conditioning label, as 


where we delay the discussion of the exact expression of _g_ subsequently. By incorporating this modified noise prediction into the original denoising objective, we explicitly steer the fine-tuning stage of the VLA. The final objective is reformulated as, 


where _λ_ is a guidance scale that modulates the influence of the guidance. 

**Classifier Guidance in Flow-based VLAs.** Similarly, for those VLAs that model the generation of action chunks with Flow Matching framework, we also provide an updated objective that directly incorporates the classifier guidance into the learning of the flow. As proven by Lipman et al. (2024), supposing a velocity field _vθ_ is an instance of linear Gaussian flows **x**<sup>_τ_</sup> = _τ_ **x**<sup>1</sup> + (1 _− τ_ ) **x**<sup>0</sup> where _q_ ( **x**<sup>1</sup> ) is the target data distribution and _p_ ( **x**<sup>0</sup> ) = _N_ (0 _, I_ ) is the source distribution, the transformation between marginal velocity fields and score function for unconditional distributions satisfies 


7 

We refer readers to Lipman et al. (2024) for a detailed proof. Similarly, when we condition the velocity field _vθ_ ( **a**<sup>_τ_</sup> _t_ : _t_ + _h_<sup>_|y_)onalabel</sup><sup>_y_,wehave</sup> 


The final objective for fine-tuning the pre-trained velocity field _vθ_ is thus rewritten as, 


where _λ_ is the guidance scale. 

**Designing a Guidance Function for Efficient Adaptation.** The goal of fine-tuning a pre-trained VLA is to fit the action distribution of the adaptation data. Despite the inherent heterogeneity of actions from different embodiments, we can effectively measure a valid discrepancy between them by leveraging the unified and compact action latent space _Z_ , established in Section 4.1. To facilitate efficient adaptation, we design a guidance function that measures how closely an intermediate action chunk during the denoising process, **a** ˆ<sup>_k_</sup> _t_ : _t_ + _h_<sup>,</sup> aligns with the ground truth action chunk, **a**<sup>0</sup> _t_ : _t_ + _h_<sup>,fromtheadaptationdata.InspiredbyCarvalhoetal.</sup> (2023); Liang et al. (2025), we formulate the classifier induced by such a guidance function as an energy-based model, 


where **E** _ψ_ is the encoder of the adaptation action VAE and _Zψ_ is a normalizing constant dependent on _ψ_ . Then the classifier guidance _g_ can be easily calculated via, 


where we use **E** _ψ_ to encode both noisy actions and clean actions. One may ask whether the encoder **E** _ψ_ can robustly encode noisy action chunks. As identified by Zhao et al. (2017), the vanilla VAE (Kingma and Welling, 2013) suffers from issues such as posterior collapse and inaccurate amortized latent inference, while the InfoVAE effectively addresses these limitations, making it an appropriate alternative for our deliberately designed guidance function. Since the guidance relies on the ground truth action chunk, which is not available during VLA inference, we incorporate this guidance explicitly into the training objective, as shown in Eqs. (9) and (12). During training, we use the noisy action chunk **a**<sup>_k_</sup> _t_ : _t_ + _h_<sup>corruptedfromitsgroundtruth</sup><sup>**a**0</sup> _t_ : _t_ + _h_<sup>asa</sup> reliable substitute for the corresponding intermediate action chunk during the denoising process. 

This gradient guidance _g_ allows us to explicitly calibrate the transitions at any noise level _k_ , pushing the VLA’s output consistently towards a latent representation that reduces the distance to the target distribution throughout the whole denoising process. As shown in Fig. 2, our method not only steers the pre-trained VLA towards the adaptation data, but also constrains its output to remain within the unified action latent space which happens to be a specific mode of the pre-training action latent space. By preventing the VLA from deviating far from this structured latent manifold, our method also implicitly helps preserve valuable visuomotor prior knowledge acquired during pre-training. Detailed algorithmic descriptions for how we steer the adaptation of diffusion-based/flow-based VLAs are provided in Algs. 2 and 3. 

### **5 Experiments** 

To demonstrate the efficiency of ATE in facilitating the adaptation process across embodiments and tasks, we evaluate our approach in both simulated and real-world settings. Through extensive experiments, our aim is to answer the following key questions: **_Q_ 1** : How efficiently does ATE facilitate the VLA’s adaptation 

8 

under cross-task and cross-embodiment regimes? (Section 5.2) **_Q_ 2** : To what extent does ATE enhance the generalization of the fine-tuned VLA against diverse perturbations, such as variations in object placement, lighting conditions, and visual distractors? (Section 5.3) **_Q_ 3** : How critical is our proposed aligned and structured action latent space to achieving efficient cross-embodiment and cross-task adaptation? (Section 5.4) 

#### **5.1 Experimental Setup** 

To demonstrate the efficiency of ATE in facilitating the adaptation process across embodiments and tasks, we evaluate our approach in both simulated and real-world settings. 

**Experimental Environment.** For simulation, we conduct experiments on two recently released benchmarks: **RoboTwin 1.0** (Mu et al., 2025) and **ManiSkill3** (Tao et al., 2024). RoboTwin 1.0 provides 17 diverse singleand dual-arm manipulation tasks (e.g., tool adjustment, dual-bottle picking) that are largely absent from mainstream VLA pretraining datasets (Open X-Embodiment, Droid, and etc.). ManiSkill3 instead focuses on contact-rich single-arm manipulation (e.g., cube pushing, cube picking), emphasizing precise low-level control. Together, these benchmarks allow us to evaluate ATE under both bimanual and contact-rich regimes, directly addressing **_Q_ 1** regarding cross-task efficient adaptation. 

For real-world experiments, we deploy policies trained using ATE on a dual-arm **RealMan** robot, where each arm has 7 DoF—distinct from the 6-DoF single-arm embodiments predominantly used in mainstream VLA pretraining datasets (e.g., RDT, _π_ 0). We design **four long-horizon dual-arm tasks** requiring precise insertion and tight collaboration, along with an additional **tool-use task** (details are provided in Appendix B). These tasks are particularly challenging for current VLA models, as they require bimanual coordination, tool interaction, and long-horizon reasoning capabilities that remain challenging for existing VLAs. This setting provides a strong testbed to evaluate how efficiently ATE facilitates adaptation across both task and embodiment shifts ( **_Q_ 1** ) and to probe robustness under real-world perturbations such as object placement, lighting, and visual distractors ( **_Q_ 2** ). We refer the detail of real-robot setup in Appendix C. 

**Baselines.** Since ATE is designed to be plug-and-play, it can be directly applied to existing diffusion- and flow matching–based architectures. We benchmark it on three representative models. For diffusion-based models, we include the **Diffusion Policy (DP)** , a foundational diffusion architecture; and **RDT-1B** (Liu et al., 2024), a diffusion-based VLA tailored for bimanual manipulation that leverages a scalable transformer and a physically interpretable unified action space for transferable across robot embodiments. For flow matching–based models, we include **_π_ 0**<sup>1</sup> (Black et al., 2024), a generalist policy built on pre-trained vision-language models, supporting multi-task and multi-embodiment manipulation with strong instruction-following and efficient adaptation ability. Together, these baselines represent the leading paradigms of robotic foundation models, allowing us to evaluate how our aligned and structured action latent space contributes to efficient adaptation ( **_Q_ 3** ). **Note that in all cases, the baseline comparison is against direct fine-tuning of these architectures without our method.** 

**Implementation.** Our implementation consists of two main components. 

Firstly, we adopt a two-step Info-VAE training scheme to learn structured latent representations over action chunks, which facilitates efficient guidance during downstream policy adaptation. With only robot action data required, the action-latent learning is lightweight while capturing informative latent structure. In step-1, the training of VAE is performed on large-scale VLA pretraining datasets, aiming to capture transferable latent structure across diverse robot platforms and tasks. The model uses a latent dimension of 512 and is trained with a mutual information term to encourage informative latent variables and alignment between pretraining and downstream action spaces. The training of step-1 typically takes around 12 hours. Then, step-2 fine-tuning is conducted on small sets of domain-specific data, further aligning the action distribution of the target domain to the latent space. This step is extremely fast, taking less than 0.5 hours. 

> • **Step 1 (General latent learning):** We perform general representation learning on large-scale datasets, which is used in the pretraining stage of VLAs. The datasets for training VAEs in this stage include DROID, Kuka, ALOHA, and selected subsets of Open X-Embodiment, aiming to capture transferable latent structure across diverse robot platforms and tasks. 

> 1Here we adopt the implementation of _π_ 0 from Huggingface Lerobot Community (https://github.com/huggingface/lerobot) across all experiments. 

9 

- **Step 2 (Domain-specific latent tuning):** We finetune the pre-trained VAEs with only a small set of data from the target domains (i.e., RoboTwin-1.0, ManiSkill3, and Real-robot setup) that have specific embodiments and tasks. Specifically, we use 100 trajectories per task for RDT-based models, and 50 trajectories for _π_ 0- and DP-based models. 

**Table 1** Info-VAE training configuration across stages and policy types. 

|**Policy**|**Dataset Source**|**Episodes**|**Epochs**|
|---|---|---|---|
||**Step 1**|||
|DP|RoboTwin 1.0: 5 tasks|50/task|1000|
|RDT|Open X-Embodiment (subset), DROID, Kuka, ALOHA<br>|3000|1000|
|_π_0|Open X-Embodiment (subset), DROID|3000|1000|
||**Step 2**|||
|DP|RoboTwin 1.0: 1 task|50/task|200|
|RDT|RoboTwin 1.0: 17 tasks, ManiSkill3: 2 tasks|100/task|200|
|_π_0|RoboTwin 1.0: 17 tasks, Real-World: 4 long-horizon tasks|50/task|200|


Secondly, the pretrained Info-VAE is used to provide structured latent information for a lightweight guidance module, which facilitates efficient adaptation of diffusion- or flow-matching–based VLAs. During policy fine-tuning, the guidance module leverages the Info-VAE latent space to measure the discrepancy between predicted and target actions and applies gradient signals to steer the policy updates toward the target distribution. The Info-VAE parameters are frozen, with guidance enhanced via random latent perturbations and dynamically scaled according to the current generation step. A tunable parameter controls the overall strength of the guidance, allowing a flexible trade-off between adaptation efficiency and stability. This approach enables rapid adaptation without requiring additional data, and integration into existing VLA training pipelines is straightforward and computationally lightweight. Full algorithmic details, including the latent-space guidance formulation, are provided in the Appendix E. 

#### **5.2 Main Results** 

To answer **_Q_ 1** , we first evaluate the proposed ATE method in simulation using two representative benchmarks: RoboTwin 1.0 and ManiSkill3. Task success rate is used as the performance metric to compare our method with baseline models, including RDT, _π_ 0, and DP. The results demonstrate that our method consistently enhances performance across tasks and architectures, particularly under limited data conditions. 

**Simulation Results on RoboTwin 1.0.** We evaluate both RDT and _π_ 0 on 17 manipulation tasks from the RoboTwin 1.0 benchmark, with results summarized in Table 2. Our ATE variants significantly outperform the original models, achieving average success rate improvements of +10% for RDT and +9% for _π_ 0, with gains exceeding +30% on challenging tasks such as _put apple cabinet_ and _empty cup place_ . In addition to higher final performance, our method demonstrates improved sample efficiency, surpassing the RDT baseline at just 70k steps compared to 90k. Fig. 3 illustrates the performance of both the DP baseline and the ATE variant in in-distribution and out-of-distribution settings. Overall, our method consistently improves success rates and accelerates convergence, with particularly large gains on tasks where the baseline struggles. Examining the training curves at 100, 200, and 300 epochs shows that our method reaches higher success rates earlier and maintains strong performance on the most challenging tasks. For out-of-distribution settings such as _dual bottles pick easy_ and _shoe place_ , the ATE variant consistently surpasses the baseline, with the success rate in _shoe place_ nearly doubling at 100 epochs. Similar trends are observed in in-distribution settings, such as _put apple cabinet_ and _empty cup place_ . The performance gain can be attributed to two key advantages of our algorithm: (i) the unified action latent space, which compactly represents actions of different embodiments and tasks, and bridges the domain gap between pre-training and adaptation; and (ii) the latent space guidance, which explicitly steers fine-tuning towards the target action distribution, which ensures efficient adaptation while preserving valuable visuomotor priors, resulting in both faster convergence and higher final success rates. 

**Simulation Results on ManiSkill3.** The effectiveness of the proposed approach is further validated on the ManiSkill3 benchmark using RDT as the policy backbone. This simulator emphasizes contact-rich manipulation and offers a diverse suite of single-arm tasks. As shown in Table 3, the success rates on two representative 

10 

**Table 2** The comparison of task success rates on RoboTwin 1.0 benchmark 

|||Me|thod||
|---|---|---|---|---|
|Task|||||
||RDT-1B<br>(Liu et al., 2024)|**RDT-1B + ATE**<br>(Ours)|_π_0<br>(Black et al., 2024)|**_π_0 + ATE**<br>(Ours)|
|Block Hammer Beat|52%|**71%**(_↑_19)|38%|**44%**(_↑_6)|
|Block Handover|69%|**91%**(_↑_22)|80%|**92%**(_↑_12)|
|Blocks Stack (Easy)|10%|**31%**(_↑_21)|30%|**50%**(_↑_20)|
|Blocks Stack (Hard)|1%|**7%**(_↑_6)|**8%**|7%(_↓_1)|
|Bottle Adjust|**53%**|37%(_↓_16)|39%|**45%**(_↑_6)|
|Container Place|34%|**55%**(_↑_21)|56%|**59%**(_↑_3)|
|Diverse Bottles Pick|18%|**24%**(_↑_6)|20%|**40%**(_↑_20)|
|Dual Bottles Pick (Easy)|76%|**87%**(_↑_11)|48%|**85%**(_↑_37)|
|Dual Bottles Pick (Hard)|39%|**58%**(_↑_19)|52%|**55%**(_↑_3)|
|Dual Shoes Place|6%|**9%**(_↑_3)|22%|**24%**(_↑_2)|
|Empty Cup Place|22%|**61%**(_↑_39)|32%|**36 %**(_↑_4)|
|Mug Hanging (Easy)|6%|6%|11%|**27%**(_↑_16)|
|Mug Hanging (Hard)|1%|1%|4%|4%|
|Pick Apple Messy|35%|**39%**(_↑_4)|**18%**|11%(_↓_7)|
|Put Apple Cabinet|20%|**45%**(_↑_25)|34%|**55%**(_↑_21)|
|Shoe Place|**44%**|43%(_↓_1)|52%|**58%**(_↑_6)|
|Tool Adjust|**54%**|42%(_↓_12)|**70%**|69%(_↓_1)|
|**Average**|31.8%|**41.6%**(_↑_9.8)|36.1%|**44.8%**(_↑_8.7)|


**Figure 3** Evaluation of DP baseline with and without ATE across (a) Out-of-distribution tasks and (b) In-distribution tasks. Incorporating ATE consistently improves success rates and accelerates convergence, with the most significant gains observed on challenging tasks where baseline performance is low. 

tasks demonstrate consistent improvements with the ATE adaptation method, indicating strong generalization even in highly dynamic simulated environments. 

**Table 3** Task success rates on ManiSkill3 benchmark. 

**Real-World Results.** To further address **_Q_ 1** in terms of efficient cross-task and cross-embodiment adaptation, we conduct real-world experiments on a dual-arm RealMan robot, with each arm having 7 DoF and equipped with Agibot OminiPicker single-DoF grippers. To be specific, we design four representative manipulation tasks for our experiments. For each of the four tasks, we collect 160 

|**Task**|**RDT-1B**|**RDT-1B + ATE(Ours)**|
|---|---|---|
|Push Cube|65.2%|**78.4%**(_↑_13.2)|
|Pick Cube|7.6%|**14.8%**(_↑_7.2)|
|**Average**|36.4%|**46.6%**(_↑_10.2)|


demonstration trajectories, with the detailed experimental setups and data collection procedures provided in Appendix C and Appendix H. The training process adopts a batch size of 48 for 120k steps, and success rates are measured at 60k, 90k, and 120k steps to assess both convergence speed and final performance. The experiments focus on long-horizon manipulation sequences, each lasting over one minute and requiring precise coordination between arms and objects, thus providing a strong testbed to validate ATE for efficient cross-task 

11 


**Figure 4** Real-world evaluation on physical robot experiments. Top panel reports success rates across four tasks and overall average, comparing ATE with the baseline π0. Bottom panel shows full execution trajectories of four representative tasks, covering long-horizon, single-arm, and dual-arm scenarios. 

and cross-embodiment adaptation. The definitions of the four tasks are as follows. 

- **Cook Bun:** The right gripper grasps a bun from the right plate and places it on the left plate, while the left gripper lifts the lid and places it aside. The left gripper then picks a bun from the left plate and places it into the steamer, and finally returns the lid to the steamer. 

- **Pick Bun:** The left gripper lifts the lid temporarily, grasps the bun farthest from the camera inside the steamer, and places it on the left plate. The lid is then returned to the steamer. 

- **Make Sandwich:** The left gripper retrieves one toasted bread slice from the toaster and transfers it to the right gripper, which places it on the left plate. The right gripper then adds the patty, lettuce, and top bread slice handed from the left gripper. 

- **Use Toaster:** The left gripper picks up the farther bread slice and passes it to the right gripper for toaster insertion. The remaining slice is inserted similarly, followed by pressing the toaster button. 

These tasks involve minute-scale operations that require bimanual collaboration, posing challenges especially with limited adaptation data. The evaluation is run on a single NVIDIA 4090 at 20 Hz, and each task is evaluated over 20 trials, where ‘success’ is defined as completing the long-horizon sequence, including coordinated object manipulation and placement. Initial object positions are randomly sampled within a radius of 3.5 cm. For the _Use Toaster_ task, we adopt a graded success metric: fully inserting a bread slice counts as 1.0, tilted insertion as 0.25, and partial insertion as 0.5. 

Figure 4 visualizes success rates across tasks at different training steps. Our method significantly accelerates learning, achieving higher success rates with fewer training steps. For example, in _Cook Bun_ , the success rate increases to 100% in 90k steps, while the baseline only reaches 15%. In the single-arm _Pick Bun_ task, ATE reaches 50% success at 90k steps and 70% at 120k. For dual-arm tasks ( _Make Sandwich_ and _Use Toaster_ ), ATE consistently improves performance across all checkpoints. On average across all tasks, the baseline achieves 16.7% overall success, while ATE reaches 58.1% at 120k steps, demonstrating substantial improvement in both final performance and convergence speed. The largest gains are observed in long-horizon tasks like _Pick Bun_ , where proper sequencing and coordination are crucial. 

In real-world evaluation, we also observe manifest improvements in motion quality. Due to action-space alignment, ATE can generate smoother trajectories compared to the baseline, which often shows abrupt movements and collisions. This is particularly evident in _Cook Bun_ and _Pick Bun_ , where the baseline applies excessive force to the steamer lid. In contrast, ATE modulates force appropriately, allowing the robot to 

12 


**Figure 5** Real-world generalization settings. For the Spatial Generalization experiment, we vary the initial positions of manipulated objects. For the Visual Distractors experiment, we randomly place unseen items (e.g., fruits) in the scene. For the human disturbance experiment, we intervene at key execution points by resetting already completed sub-tasks. 

pause and reposition as needed. Here, we use the _Cook Bun_ task as a representative example, with all related 6-dimensional force data and analyses provided in AppendixG. 

_Discussion._ In general, simulation and real-world experiments consistently demonstrate that ATE facilitates efficient cross-task and cross-embodiment adaptation. Across RoboTwin 1.0 and ManiSkill3 benchmarks, ATE improves final success rates, accelerates convergence, and enhances sample efficiency compared to baseline policies. Real-world evaluations on the dual-arm RealMan robot further confirm these advantages, with ATE achieving higher success rates, smoother trajectories, and better long-horizon coordination. These results indicate that leveraging a unified action latent space together with latent-space guidance allows the policy to quickly adapt to new tasks and embodiments while preserving pre-trained visuomotor knowledge, effectively addressing **_Q_ 1** . 

#### **5.3 Generalization Ability Analysis** 

To answer **_Q_ 2** , we evaluate the robustness and generalization of ATE under diverse real-world perturbations, including variations in illumination, visual distractions, object morphology, clutter, and human disturbances. Each experiment is evaluated over 5 trials, with success defined as completing the full manipulation sequence. The experimental setups for all perturbations, except for the illumination variation, are illustrated in Fig. 5. 

**Varying Illumination.** We alter the lighting conditions while keeping the color temperature fixed at 5800 K. The illumination levels are set to low, high, and flicker around the optimal value. As shown in Table 4, ATE consistently outperform the baseline, particularly under extreme or flickering illumination, where the baseline often failed. This indicates that ATE is robust to lighting intensity variations, maintaining task performance even under conditions not seen during training. 

**Spatial Generalization.** To further examine position generalization, we extend the randomized initial placement experiments beyond the original 20 trials. The objects are displaced within a larger radius of approximately 6.5 cm, with five trials conducted at each boundary position (up, down, left, right) as well as at the initial location. For the _Pick Bun_ and _Cook Bun_ tasks, the buns were moved accordingly, while for the _Make Sandwich_ task, the meat slices and lettuce were repositioned. Table 5 shows that ATE achieved success rates of 40%, 60%, and 40% on _Cook Bun_ , _Pick Bun_ , and _Make Sandwich_ , respectively. These results demonstrate 

13 

ATE’ s ability to adapt to larger spatial shifts, highlighting efficient position generalization across diverse manipulation tasks. 

**Visual Distractor.** We introduce irrelevant objects that are not present in the dataset, such as scattered fruits, puzzle pieces, and trays, to place on the table as visual distractions. Table 5 shows that ATE outperformed the baseline in all tasks, with success rates of 40% for _Cook Bun_ , 80% for _Pick Bun_ , and 40% for _Make Sandwich_ . This suggests that ATE effectively focuses on task-relevant objects while ignoring irrelevant clutter, demonstrating strong visual generalization. 

**Human Disturbance.** During the task, when the robotic arm successfully grasped a bun or other objects, a human quickly interfered—for example, removing a bun from the gripper or repositioning ingredients—forcing the policy to reattempt. Table 5 shows that ATE retained 0% success on _Cook Bun_ , 40% on _Pick Bun_ , and 60% on _Make Sandwich_ , whereas the baseline largely failed. These results highlight ATE’s robustness to sudden external interventions, suggesting that the policy can recover from unexpected disturbances and adapt its behavior accordingly. 

**Table 4** Success rates (%) under different illumination settings (5 trials each). 

|**Method**|**Cook Bun**|**Pick Bun**|**Make Sandwich**|
|---|---|---|---|
|Low Illumination Condition||||
|ATE|60%|40%|40%|
|Baseline|0%|0%|40%|
|High Illumination Condition<br>ATE|60%|40%|60%|
|Baseline|0%|0%|40%|
|Flickering Illumination Condition<br>ATE|20%|0%|20%|
|Baseline|0%|0%|20%|


**Table 5** Success rates (%) under different generalization challenges (5 trials each). 

|**Challenge**|**Co**<br>**ATE**|**ok Bun**<br>**Baseline**|**Pi**<br>**ATE**|**ck Bun**<br>**Baseline**|**Make**<br>**ATE**|**Sandwich**<br>**Baseline**|
|---|---|---|---|---|---|---|
|Visual Distractor|40%|20%|80%|20%|40%|40%|
|Spatial Generalization|40%|0%|60%|40%|40%|20%|
|Human Disturbance|0%|0%|40%|0%|60%|40%|


_Discussion_ Overall, across all generalization experiments—including varying illumination, visual distractors, spatial shifts, human disturbances, and object morphology/clutter variations—ATE consistently outperforms the baseline. These results directly address **_Q_ 2** , showing that ATE enhances the robustness of the VLA against diverse real-world perturbations. The strong generalization arises because our method constrains the policy within the structured latent space learned during pre-training, which effectively preserves pre-trained visuomotor priors while allowing adaptation to new environmental variations. By maintaining behavior within this latent manifold, ATE enables the policy to recover from unexpected disturbances, focus on task-relevant features, and adapt to unseen object configurations, demonstrating reliable performance under conditions not encountered during training. 

#### **5.4 Ablation Study** 

To answer **_Q_ 3** , we study the impact of the aligned and structured action latent space on cross-embodiment and cross-task adaptation. We compare our two-stage Info-VAE, which embeds adaptation actions into a mode of the pre-trained latent manifold, against a single-stage VAE trained directly on task-specific data, using both _π_ 0 and Diffusion Policy backbones. As shown in Figure 6, the two-stage approach consistently outperforms the single-stage baseline, achieving higher final success rates, especially on long-horizon or challenging tasks. By 

14 


**Figure 6** Ablation study on the effect of two-stage Info-VAE training. We compare the proposed two-stage Info-VAE with a single-stage VAE trained only on task-specific datasets, using both _π_ 0 and Diffusion Policy backbones. For the Diffusion Policy results, we evaluate both in-distribution (†) and out-of-distribution generalization settings (‡). 

constraining adaptation actions within the structured latent space, our method effectively reduces the domain gap between pre-training and target embodiments, while preserving valuable pre-trained visuomotor priors. These results confirm that the aligned latent space is critical for efficient adaptation, enabling downstream policies to rapidly leverage prior knowledge and generalize across different tasks and robotic platforms. 

### **6 Conclusion** 

In this work, we present ATE , a lightweight and data-efficient framework for adapting VLAs to new embodiments and tasks. By unifying disparate action spaces and steering the pre-trained model via classifier guidance, our method effectively bridges the action distribution gap between pre-training and downstream adaptation. The experimental results on representative VLA architectures, including DP, RDT, and _π_ 0 verify the widely applicability of our adaptation method. The cross-task adaptation experiments on RoboTwin and ManiSkill benchmarks show that ATE consistently outperforms baselines. By constructing complex bimanual collaboration tasks in a new robot platform, we observe ATE obtains significantly better performance than standard adaptation methods, especially for spatial, visual, and disturbance generalization settings. 

Our results highlight the practicality and scalability of ATE, offering a plug-and-play solution that seamlessly integrates with diffusion- and flow-based VLAs without altering their architectures. Looking ahead, we envision that this alignment-and-guidance paradigm can serve as a foundation for fine-tuning generalist robot policies at scale, enabling efficient adaptation to new robotic platforms and diverse tasks. 

15 

### **References** 

- Johannes Anschütz and Arthur-César Le Bras. Prismatic dieudonné theory. In _Forum of Mathematics, Pi_ , volume 11, page e2. Cambridge University Press, 2023. 

- Arpit Bansal, Hong-Min Chu, Avi Schwarzschild, Soumyadip Sengupta, Micah Goldblum, Jonas Geiping, and Tom Goldstein. Universal guidance for diffusion models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 843–852, 2023. 

- Erik Bauer, Elvis Nava, and Robert K Katzschmann. Latent action diffusion for cross-embodiment manipulation. _arXiv preprint arXiv:2506.14608_ , 2025. 

- Lucas Beyer, Andreas Steiner, André Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _arXiv preprint arXiv:2407.07726_ , 2024. 

- Hongzhe Bi, Lingxuan Wu, Tianwei Lin, Hengkai Tan, Zhizhong Su, Hang Su, and Jun Zhu. H-rdt: Human manipulation enhanced bimanual robotic manipulation, 2025. URL https://embodiedfoundation.github.io/hrdt. 

- Christopher M Bishop and Nasser M Nasrabadi. _Pattern recognition and machine learning_ , volume 4. Springer, 2006. 

- Johan Bjorck, Fernando Castañeda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Learning to act anywhere with task-centric latent actions. _arXiv preprint arXiv:2502.14420_ , 2025. 

- Joao Carvalho, An T Le, Mark Baierl, Dorothea Koert, and Jan Peters. Motion planning diffusion: Learning and planning of robot motions with diffusion models. In _2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 1916–1923. IEEE, 2023. 

- Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, et al. Pali-x: On scaling up a multilingual vision and language model. _arXiv preprint arXiv:2305.18565_ , 2023a. 

- Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, and Gang Yu. Executing your commands via motion diffusion in latent space. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18000–18010, 2023b. 

- Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2023. 

- Open X-Embodiment Collaboration, Abby O’Neill, Abdul Rehman, Abhinav Gupta, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, Albert Tung, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anchit Gupta, Andrew Wang, Andrey Kolobov, Anikait Singh, Animesh Garg, Aniruddha Kembhavi, Annie Xie, Anthony Brohan, Antonin Raffin, Archit Sharma, Arefeh Yavary, Arhan Jain, Ashwin Balakrishna, Ayzaan Wahid, Ben Burgess-Limerick, Beomjoon Kim, Bernhard Schölkopf, Blake Wulfe, Brian Ichter, Cewu Lu, Charles Xu, Charlotte Le, Chelsea Finn, Chen Wang, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Christopher Agia, Chuer Pan, Chuyuan Fu, Coline Devin, Danfei Xu, Daniel Morton, Danny Driess, Daphne Chen, Deepak Pathak, Dhruv Shah, Dieter Büchler, Dinesh Jayaraman, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Ethan Foster, Fangchen Liu, Federico Ceola, Fei Xia, Feiyu Zhao, Felipe Vieira Frujeri, Freek Stulp, Gaoyue Zhou, Gaurav S. Sukhatme, Gautam Salhotra, Ge Yan, Gilbert Feng, Giulio Schiavi, Glen Berseth, Gregory Kahn, Guangwen Yang, Guanzhi Wang, Hao Su, Hao-Shu Fang, Haochen Shi, Henghui Bao, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homanga Bharadhwaj, Homer Walke, Hongjie Fang, Huy Ha, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jad Abou-Chakra, Jaehyung Kim, Jaimyn Drake, Jan Peters, Jan Schneider, Jasmine Hsu, Jay Vakil, Jeannette Bohg, Jeffrey Bingham, 

16 

Jeffrey Wu, Jensen Gao, Jiaheng Hu, Jiajun Wu, Jialin Wu, Jiankai Sun, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jimmy Wu, Jingpei Lu, Jingyun Yang, Jitendra Malik, João Silvério, Joey Hejna, Jonathan Booher, Jonathan Tompson, Jonathan Yang, Jordi Salvador, Joseph J. Lim, Junhyek Han, Kaiyuan Wang, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Black, Kevin Lin, Kevin Zhang, Kiana Ehsani, Kiran Lekkala, Kirsty Ellis, Krishan Rana, Krishnan Srinivasan, Kuan Fang, Kunal Pratap Singh, Kuo-Hao Zeng, Kyle Hatch, Kyle Hsu, Laurent Itti, Lawrence Yunliang Chen, Lerrel Pinto, Li Fei-Fei, Liam Tan, Linxi "Jim" Fan, Lionel Ott, Lisa Lee, Luca Weihs, Magnum Chen, Marion Lepert, Marius Memmel, Masayoshi Tomizuka, Masha Itkina, Mateo Guaman Castro, Max Spero, Maximilian Du, Michael Ahn, Michael C. Yip, Mingtong Zhang, Mingyu Ding, Minho Heo, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Muhammad Zubair Irshad, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Ning Liu, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Osbert Bastani, Pannag R Sanketi, Patrick "Tree" Miller, Patrick Yin, Paul Wohlhart, Peng Xu, Peter David Fagan, Peter Mitrano, Pierre Sermanet, Pieter Abbeel, Priya Sundaresan, Qiuyu Chen, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart’in-Mart’in, Rohan Baijal, Rosario Scalise, Rose Hendrix, Roy Lin, Runjia Qian, Ruohan Zhang, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Shan Lin, Sherry Moore, Shikhar Bahl, Shivin Dass, Shubham Sonawani, Shubham Tulsiani, Shuran Song, Sichun Xu, Siddhant Haldar, Siddharth Karamcheti, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Subramanian Ramamoorthy, Sudeep Dasari, Suneel Belkhale, Sungjae Park, Suraj Nair, Suvir Mirchandani, Takayuki Osa, Tanmay Gupta, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Thomas Kollar, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z. Zhao, Travis Armstrong, Trevor Darrell, Trinity Chung, Vidhi Jain, Vikash Kumar, Vincent Vanhoucke, Vitor Guizilini, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiangyu Chen, Xiaolong Wang, Xinghao Zhu, Xinyang Geng, Xiyuan Liu, Xu Liangwei, Xuanlin Li, Yansong Pang, Yao Lu, Yecheng Jason Ma, Yejin Kim, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Yilin Wu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yongqiang Dou, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yue Cao, Yueh-Hua Wu, Yujin Tang, Yuke Zhu, Yunchu Zhang, Yunfan Jiang, Yunshuang Li, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zehan Ma, Zhuo Xu, Zichen Jeff Cui, Zichen Zhang, Zipeng Fu, and Zipeng Lin. Open X-Embodiment: Robotic learning datasets and RT-X models. https://arxiv.org/abs/2310.08864, 2023. 

- Prafulla Dhariwal and Alexander Nichol. Diffusion models beat gans on image synthesis. _Advances in neural information processing systems_ , 34:8780–8794, 2021. 

- Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: An embodied multimodal language model. In _International Conference on Machine Learning_ , pages 8469–8488. PMLR, 2023. 

- Gintare Karolina Dziugaite, Daniel M Roy, and Zoubin Ghahramani. Training generative neural networks via maximum mean discrepancy optimization. In _Proceedings of the Thirty-First Conference on Uncertainty in Artificial Intelligence_ , pages 258–267, 2015. 

- Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 

- Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, et al. Dita: Scaling diffusion transformer for generalist vision-language-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. BC-z: Zero-shot task generalization with robotic imitation learning. In _5th Annual Conference on Robot Learning_ , 2021. URL https://openreview.net/forum?id=8kbp23tSGYv. 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. OpenVLA: An open-source vision-language-action model. In _8th Annual Conference on Robot Learning_ , 2024. URL https://openreview.net/forum?id=ZMnD6QZAE6. 

17 

Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

Diederik P Kingma and Max Welling. Auto-encoding variational bayes. _arXiv preprint arXiv:1312.6114_ , 2013. 

- Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pages 19730–19742. PMLR, 2023. 

- Yujia Li, Kevin Swersky, and Rich Zemel. Generative moment matching networks. In _International conference on machine learning_ , pages 1718–1727. PMLR, 2015. 

- Zhixuan Liang, Yao Mu, Yixiao Wang, Tianxing Chen, Wenqi Shao, Wei Zhan, Masayoshi Tomizuka, Ping Luo, and Mingyu Ding. Dexhanddiff: Interaction-aware diffusion planning for adaptive dexterous manipulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 1745–1755, 2025. 

- Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matthew Le. Flow matching for generative modeling. In _The Eleventh International Conference on Learning Representations_ , 2023. URL https: //openreview.net/forum?id=PqvMRDCJT9t. 

- Yaron Lipman, Marton Havasi, Peter Holderrieth, Neta Shaul, Matt Le, Brian Karrer, Ricky TQ Chen, David Lopez-Paz, Heli Ben-Hamu, and Itai Gat. Flow matching guide and code. _arXiv preprint arXiv:2412.06264_ , 2024. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024. 

- Xingchao Liu, Chengyue Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In _The Eleventh International Conference on Learning Representations_ , 2023a. URL https: //openreview.net/forum?id=XVjTT1nw5z. 

- Xingchao Liu, Chengyue Gong, and qiang liu. Flow straight and fast: Learning to generate and transfer data with rectified flow. In _The Eleventh International Conference on Learning Representations_ , 2023b. URL https: //openreview.net/forum?id=XVjTT1nw5z. 

- Calvin Luo. Understanding diffusion models: A unified perspective. _arXiv preprint arXiv:2208.11970_ , 2022. 

- Yao Mu, Tianxing Chen, Zanxin Chen, Shijia Peng, Zhiqian Lan, Zeyu Gao, Zhixuan Liang, Qiaojun Yu, Yude Zou, Mingkun Xu, et al. Robotwin: Dual-arm robot benchmark with generative digital twins. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 27649–27660, 2025. 

NVIDIA. Gr00t n1: An open foundation model for generalist humanoid robots, 2025. 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. _arXiv preprint arXiv:2501.09747_ , 2025. 

- Mathis Petrovich, Michael J Black, and Gül Varol. Action-conditioned 3d human motion synthesis with transformer vae. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 10985–10995, 2021. 

- Mustafa Shukor, Dana Aubakirova, Francesco Capuano, Pepijn Kooijmans, Steven Palma, Adil Zouitine, Michel Aractingi, Caroline Pascal, Martino Russi, Andres Marafioti, et al. Smolvla: A vision-language-action model for affordable and efficient robotics. _arXiv preprint arXiv:2506.01844_ , 2025. 

- Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli. Deep unsupervised learning using nonequilibrium thermodynamics. In _International conference on machine learning_ , pages 2256–2265. pmlr, 2015. 

- Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Scorebased generative modeling through stochastic differential equations. In _International Conference on Learning Representations_ , 2021. URL https://openreview.net/forum?id=PxTIG12RRHS. 

- Stone Tao, Fanbo Xiang, Arth Shukla, Yuzhe Qin, Xander Hinrichsen, Xiaodi Yuan, Chen Bao, Xinsong Lin, Yulin Liu, Tse-kai Chan, et al. Maniskill3: Gpu parallelized robotics simulation and rendering for generalizable embodied ai. _arXiv preprint arXiv:2410.00425_ , 2024. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

18 

- Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution. _arXiv preprint arXiv:2409.12191_ , 2024. 

- Junjie Wen, Yichen Zhu, Jinming Li, Zhibin Tang, Chaomin Shen, and Feifei Feng. Dexvla: Vision-language model with plug-in diffusion expert for general robot control. _arXiv preprint arXiv:2502.05855_ , 2025a. 

- Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025b. 

- Junjie Wen, Yichen Zhu, Minjie Zhu, Zhibin Tang, Jinming Li, Zhongyi Zhou, Xiaoyu Liu, Chaomin Shen, Yaxin Peng, and Feifei Feng. Diffusionvla: Scaling robot foundation models via unified diffusion and autoregression. In _Forty-second International Conference on Machine Learning_ , 2025c. 

- Siyu Xu, Yunke Wang, Chenghao Xia, Dihao Zhu, Tao Huang, and Chang Xu. Vla-cache: Towards efficient visionlanguage-action model via adaptive token caching in robotic manipulation. _arXiv preprint arXiv:2502.02175_ , 2025. 

- Seonghyeon Ye, Joel Jang, Byeongguk Jeon, Se June Joo, Jianwei Yang, Baolin Peng, Ajay Mandlekar, Reuben Tan, Yu-Wei Chao, Bill Yuchen Lin, Lars Liden, Kimin Lee, Jianfeng Gao, Luke Zettlemoyer, Dieter Fox, and Minjoon Seo. Latent action pretraining from videos. In _International Conference on Learning Representations_ , 2025. 

- Haoqi Yuan, Bohan Zhou, Yuhui Fu, and Zongqing Lu. Cross-embodiment dexterous grasping with reinforcement learning. In _The Thirteenth International Conference on Learning Representations_ , 2025. URL https://openreview. net/forum?id=twIPSx9qHn. 

- Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025a. 

- Rongyu Zhang, Menghang Dong, Yuan Zhang, Liang Heng, Xiaowei Chi, Gaole Dai, Li Du, Yuan Du, and Shanghang Zhang. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. _arXiv preprint arXiv:2503.20384_ , 2025b. 

- Shengjia Zhao, Jiaming Song, and Stefano Ermon. Infovae: Information maximizing variational autoencoders. _arXiv preprint arXiv:1706.02262_ , 2017. 

- Jinliang Zheng, Jianxiong Li, Dongxiu Liu, Yinan Zheng, Zhihao Wang, Zhonghong Ou, Yu Liu, Jingjing Liu, Ya-Qin Zhang, and Xianyuan Zhan. Universal actions for enhanced embodied foundation models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22508–22519, 2025. 

- Yifan Zhong, Xuchuan Huang, Ruochong Li, Ceyao Zhang, Yitao Liang, Yaodong Yang, and Yuanpei Chen. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. _arXiv preprint arXiv:2502.20900_ , 2025. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 

19 

### **A Additional Related Works** 

**Constructing Unified Action Space.** Establishing a shared discrete token dictionary to discretize continuous robotic actions is a common approach for mapping heterogeneous actions into a shared space (Brohan et al., 2022; Zitkovich et al., 2023; Kim et al., 2024; Pertsch et al., 2025). Furthermore, UniVLA (Bu et al., 2025) leveraged a Vector-Quantized VAE to extract task-centric latent actions from massive cross-embodiment videos for VLA pre-training and post-training. Similarly, UniACT (Zheng et al., 2025) also learned a discrete atomic behavior codebook from large-scale robotic data to form a universal discrete latent action representation. However, these methods primarily focus on establishing a universal latent representation for actions across different embodiments, failing to resolve the significant distribution discrepancy that persists between pre-training and adaptation data within the latent space. In contrast, we approach this issue from the perspective of bridging the distribution gap. Our method constructs a unified action space by first encoding the pre-training actions to form a base latent distribution, and subsequently embedding the adaptation actions into the modes of this pre-training action distribution, which results in a structured latent space. While Bauer et al. (2025) combined separate VAEs with contrastive learning to map different embodiment-specific instances of the same action into a shared latent space, their method’s heavy reliance on a hand motion retargeting system to generate these instances makes it challenging to apply in common VLA pre-training and post-training recipe. 

### **B Additional Real-World Experiments: Tool Use** 

#### **B.1 Experimental Setup** 

To validate our method on the tool-use VLA challenge, we collected an additional 80 trajectories and designed the **Make Yogurt Bowl** task. This task requires using both a _shovel_ and a _spoon_ for precise ingredient manipulation. 

**Data.** 80 high-quality trajectories are collected for this task, covering variations in initial object placement. 

**Platform.** All experiments are conducted on a dual-arm **RealMan** robot, where each arm has 7 DoF and is equipped with Agibot OminiPicker single-DoF grippers. The left arm handles the spatula, and the right arm handles the spoon. 

**Training.** Models are trained for 120k steps on 8 NVIDIA A100 GPUs with a batch size of 12 per GPU. Execution runs at 20 Hz on a single NVIDIA 4090. 

**Task Description.** Use the right gripper to pick up the shovel, scoop out the nuts and oats, and then pour yogurt into the bowl. During the process, use the left gripper to stir with a spoon. 


**Table 6** Success rate (%). 

|**Task**|**Baseline**|**ATE(Ours)**|
|---|---|---|
|Make Yogurt Bowl|15%|25%|


**Figure 7** Experimental setup for the _Make Yogurt Bowl_ task. The dual-arm robot manipulates ingredients using a spatula (right hand) and a spoon (left hand), demonstrating precise coordination. Key objects are highlighted. 

20 


**#1: Pick up the shovel with the right gripper. Scoop the nuts using the shovel. #2: Scoop the oats using the shovel. #3: Pick up the yogurt bottle with the right gripper. #4: Pick up the spoon with the left gripper. #5: Pour the yogurt into the bowl while stirring with the spoon in the left gripper. #6: Place the yogurt bottle back in its original position.** 

**Figure 8** Real-world execution of the Make Yogurt Bowl task. 

#### **B.2 Results.** 

For the _Make Yogurt Bowl_ task, the robot must perform highly coordinated dual-arm manipulation: the right gripper picks up a spatula to scoop nuts and oats and pour yogurt into the bowl, while the left gripper continuously stirs the mixture with a spoon. This task requires precise control of multiple tools simultaneously, careful timing to avoid spillage, and maintaining proper spatial relationships between ingredients and utensils. Such multi-tool coordination represents a challenging test for vision-language-action policies, as small deviations can lead to task failure. 

As shown in Table 6, our ATE method achieves a success rate of 25%, outperforming the baseline at 15%, with each method tested over 20 trials. This improvement highlights ATE’s ability to leverage pre-trained latent representations and structured visuomotor priors, enabling more reliable tool handling and fine-grained manipulation. The results indicate that ATE effectively captures the dependencies between dual-arm actions and tool interactions, allowing it to generalize across subtle variations in object positions and motions, whereas the baseline struggles with the complexity of simultaneous tool use. 

#### **B.3 Visual Distractor Generalization** 

To evaluate visual distractor robustness, unexpected objects (e.g., extra fruit pieces, small puzzles) are randomly placed on the table. The robot must complete the task while ignoring these unexpected items. Success is defined as correctly completing all phases with proper tool use. Each experiment is repeated 5 times, and the results are summarized in Table 7. 

### **C Experimental Setup** 

#### **C.1 Fast Adaptation in RoboTwin/Maniskill** 

Each model is trained and evaluated across a range of manipulation tasks using the specified number of demonstrations. All experiments are conducted using multi-GPU training setups. 

_RoboTwin 1.0 Benchmark_ RoboTwin 1.0 is adopted as the core evaluation benchmark. As a generative digital twin framework tailored for dual-arm tasks, RoboTwin 1.0 integrates 3D generative models and large 

21 


**Table 7** Success rate (%) under Visual Distractors. 

|**Task**|**Baseline**|**ATE(Ours)**|
|---|---|---|
|Make Yogurt Bowl|0%|20%|


**Figure 9** Experimental setup of the _Make Yogurt Bowl_ task under visual distractors. Additional irrelevant objects (e.g., fruit pieces) are placed on the table, while the dual-arm robot must focus on manipulating the spoon and spatula to complete the task. 

language models to synthesize diverse object-centric scenes along with spatially grounded robot code. A total of 17 tasks are selected, spanning both single-arm and dual-arm manipulation scenarios (e.g., tool adjustment, dual-bottle picking). 

_ManiSkill3 Benchmark_ In addition, we use ManiSkill3, a fast, GPU-parallelized simulator designed for contact-rich single-arm manipulation. We evaluate our method on 2 representative tasks such as push cube and pick cube, which emphasize physical contact and fine-grained control. 

**Simulation Training Configuration.** We summarize the training settings for each policy in Table 8. 

**Table 8** Training configurations for different policy models and environments. BS/GPU denotes batch size per GPU. 

|**Policy**|**Benchmark**|**BS/GPU**|**GPUs**|**Training Duration**|**Dataset Size**|
|---|---|---|---|---|---|
|RDT|RoboTwin 1.0 (17 tasks, , multi-task)|16|4 A100|100k steps|100/task|
||ManiSkill3 (2 tasks, multi-task)|12|2 A100|100k steps|100/task|
|_π_0 (PyTorch)|RoboTwin 1.0 (17 tasks, multi-task)|12|4 A100|60k steps|50/task|
|DP|RoboTwin 1.0 (5-task pretrain)|128|1 A100|2000 epochs|50/task|
||RoboTwin 1.0 (Finetune)|128|1 A100|300 epochs|50/task|


**Diffusion Policy Evaluation.** To assess the effectiveness of our proposed ATE training strategy, we perform evaluations under both in-distribution and out-of-distribution settings using Diffusion Policy as the backbone model: 

- **Pretraining:** A base model is trained on a fixed set of 5 RoboTwin 1.0 tasks. 

- **Evaluation:** 

   - _In-distribution setting:_ We fine-tune and evaluate the model on a subset of the same tasks used in pretraining to assess in-distribution task adaptation. 

   - _Out-of-distribution setting:_ We fine-tune and evaluate the model on novel RoboTwin 1.0 tasks that were not part of the pretraining set, measuring generalization to unseen tasks. 

This setup allows us to verify whether our ATE policy fine-tuning improves generalization and adaptation performance across both familiar and novel tasks. 

22 

#### **C.2 Fast Adaptation to Dual Realman Arms in Real World** 

**Data.** We collect 160 high-quality trajectories for each of the four representative long-horizon manipulation tasks ( _Cook Bun, Pick Bun, Make Sandwich, Use Toaster_ ), each lasting over one minute and requiring precise bimanual coordination between arms and objects. 

**Platform and Vision Setup.** All experiments are conducted on a dual-arm **RealMan** robot, where each arm has 7 DoF and is equipped with Agibot OminiPicker single-DoF grippers. The visual system consists of a main overhead camera (Intel RealSense L515, RGB only, 960×540, 30 Hz, automatic exposure) and two wrist-mounted cameras (Intel RealSense D405, RGB only, 960×540, 30 Hz, automatic exposure) to capture the workspace from multiple perspectives. 

**Training.** Models are trained for 120k steps using 8 NVIDIA A100 GPUs, with a batch size of 12 per GPU. 

**Task Setup.** The key objects involved in the four representative long-horizon manipulation tasks are illustrated in Figure 10. 


**Figure 10** Key objects involved in the four representative long-horizon manipulation tasks. 

#### **C.3 Generalization Ability Evaluation on Dual Realman Arms** 

This section provides essential details to reproduce the generalization experiments in Section 5.3, focusing on illumination settings. 

_Illumination Settings_ We used a set of controllable studio lamps to vary lighting conditions. All lamps have a fixed color temperature of 5800 K. All illumination settings are illustrated in Figure 11. 

- **Lamp:** COB studio fill light 

- **Low Illumination:** 25 lux 

- **High Illumination:** 65 lux 

- **Flickering Illumination:** alternating between 0 and 45 lux, flicker frequency 2 Hz 

_Notes:_ All experiments were conducted under the same camera configuration to ensure consistent observation inputs for the policy. 

### **D Training Hyperparameters** 

We summarize the key hyperparameter settings used for both stages of our method, including (i) Learning the Unified Action Latent Space, and (ii) Steering Efficient Adaptation with Latent Guidance. 

23 


**Figure 11** Illustration of the illumination setup under three conditions: low (25 lux), high (65 lux), and flickering (alternating between 0 and 45 lux at 2 Hz). 

**Table 9** Hyperparameters for Info-VAE pretraining. 

|**Hyperparameter**|**Value**|
|---|---|
|Latent dimension|512|
|Temporal input length|64 (RDT), 50 (_π_0), 14 (DP)|
|Input dimensionality|128 (RDT), 32 (_π_0), 14 (DP)|
|Optimizer|Adam|
|Learning rate|1_×_10<sup>_−_4</sup>|
|Weight decay|1_×_10<sup>_−_4</sup>|
|Batch size|64|


**Table 10** Task-specific fine-tuning (RoboTwin). 

|**Hyperparameter**|**RDT**|_π_0|**DP**|
|---|---|---|---|
|Chunk size|64|50|8|
|Batch size|64|24|128|
|Learning rate|1.0e-4|2.5e-5|1.0e-4|
|Training duration|100k steps|60k steps|300 epochs|


_Other platforms._ For ManiSkill and Real Robot experiments, we use the following task-specific fine-tuning settings: 

- **ManiSkill (simulator):** Chunk size 64 (RDT), 24 batch size, learning rate 1.0e-4, training duration 100k steps. 

- **Real Robot (physical):** Chunk size 20 ( _π_ 0), batch size 48, learning rate 2.5e-5, training duration 120k steps. 

24 

### **E Algorithmic Description of ATE** 

**Algorithm 1** Stage 1: Learning the Unified Action Latent Space 

**Input:** Pre-training dataset- _D_ pretrain, Adaptation dataset _D_ adaptation, Pre-training action VAE _ϕ_ , Adaptation action VAE _ψ_ , Number of epochs _N_ // Learn the pre-training action VAE **for** epoch = 1 to _N_ **do** Sample a batch of actions _{_ **a**<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _H−_ 1<sup>_}_</sup> _i_<sup>_n_</sup> =1<sup>from</sup><sup>_D_pretrain</sup> Update pre-training action VAE _ϕ_ via maximizing _L_ ( _ϕ_ ; _D_ pretrain) in Eq. (5) **end for** // Calculate the pre-training action latent distribution Initialize the running mean _µϕ_ and variance Σ _ϕ_ of the pre-trained action latent distribution _qϕ_ ( _z_ ) **for** all possible sample **a** _t_ : _t_ + _H−_ 1 in **do** Encode the latent _z_ of the action chunk **a** _t_ : _t_ + _H−_ 1 via _ϕ_ Update the running mean _µϕ_ and variance Σ _ϕ_ **end for** // Learn the adaptation action VAE **for** epoch = 1 to _N_ **do** Sample a batch of actions _{_ **a**<sup>(</sup> _t_ :<sup>_i_</sup> _t_<sup>)</sup> + _L−_ 1<sup>_}_</sup> _i_<sup>_n_</sup> =1<sup>from</sup><sup>_D_adaptation</sup> Update pre-training action VAE _ψ_ via maximizing _L_ ( _ψ_ ; _D_ adaptation _, ϕ_ ) in Eq. (6) **end for** 

**Algorithm 2** Stage 2: Steering Adaptation of **Flow-based VLAs** with Latent Guidance 

**Input:** Flow-based VLA _vθ_ , Adaptation dataset _D_ adaptation, Adaptation action encoder **E** _ψ_ , Guidance scale _λ_ , Learning rate _η_ **repeat** Sample an observation-language-action pair ( **o** _t, l,_ **a** _t_ : _t_ + _L−_ 1) _∼ pD_ adaptation( _·_ ) Sample _ϵ ∼N_ (0 _, I_ ) _, τ ∼U_ ([0 _,_ 1]) Corrupt clean action chunk **a**<sup>_τ_</sup> _t_ : _t_ + _L−_ 1<sup>=</sup><sup>_τ_</sup><sup>**a**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_L−_1 + (1</sup><sup>_−τ_)</sup><sup>_ϵ_</sup> // Compute the guidance Get the latents _z_ ˆ = **E** _ψ_ ( **a**<sup>_τ_</sup> _t_ : _t_ + _L−_ 1<sup>)</sup><sup>_, z_=</sup><sup>**E**</sup><sup>_ψ_(</sup><sup>**a**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_L−_1)ofnoisyactionchunkandcleanactionchunk</sup> Obtain the latent guidance _g_ = _−∇_ **a**<sup>_τ_</sup> _t_ : _t_ + _L−_ 1<sup>_∥z −z_ˆ</sup><sup>_∥_2</sup> // Steer the fine-tuning Get the ground truth velocity _vt_ = **a** _t_ : _t_ + _L−_ 1 _− ϵ_ Update the VLA via _θ_ = _θ − η∇θ∥_ [ _vθ_ ( **a**<sup>_τ_</sup> _t_ : _t_ + _L−_ 1<sup>;</sup><sup>_τ,_</sup><sup>**o**</sup><sup>_t, l_) +</sup><sup><u>1</u></sup><sup>_−_</sup> _τ_<sup>_<u>τ</u>λg_]</sup><sup>_−vt∥_2</sup> **until** Converged 

25 

**Algorithm 3** Stage 2: Steering Adaptation of **Diffusion-based VLAs** with Latent Guidance 

**Input:** Diffusion-based VLA _ϵθ_ , Adaptation dataset _D_ adaptation, Adaptation action encoder **E** _ψ_ , Guidance scale _λ_ , Learning rate _η_ **repeat** Sample an observation-language-action pair ( **o** _t, l,_ **a** _t_ : _t_ + _L−_ 1) _∼ pD_ adaptation( _·_ ) Sample _ϵ ∼N_ (0 _, I_ ) _, k ∼U_ ( _{_ 1 _,_ 2 _, . . . , T }_ ) Corrupt clean action chunk **a**<sup>_k_</sup> _t_ : _t_ + _L−_ 1<sup>=</sup><sup>_~~√~~_</sup> _<u>α</u>_ <u>¯</u> _k_ **<u>a</u>** _t_ : _t_ + _L−_ 1 +<sup>_~~√~~_</sup> 1 _− α_ ¯ _kϵ_ // Compute the guidance Get the latents _z_ ˆ = **E** _ψ_ ( **a**<sup>_k_</sup> _t_ : _t_ + _L−_ 1<sup>)</sup><sup>_, z_=</sup><sup>**E**</sup><sup>_ψ_(</sup><sup>**a**</sup><sup>_t_:</sup><sup>_t_+</sup><sup>_L−_1)ofnoisyactionchunkandcleanactionchunk</sup> Obtain the latent guidance _g_ = _−∇_ **a** _kt_ : _t_ + _L−_ 1<sup>_∥z −z_ˆ</sup><sup>_∥_2</sup> // Steer the fine-tuning Get the ground truth velocity _vt_ = **a** _t_ : _t_ + _L−_ 1 _− ϵ_ Update the VLA via _θ_ = _θ − η∇θ∥_ [ _ϵθ_ ( **a**<sup>_k_</sup> _t_ : _t_ + _L−_ 1<sup>;</sup><sup>_k,_</sup><sup>**o**</sup><sup>_t, l_)</sup><sup>_−_</sup><sup>_~~√~~_</sup> 1 _− α_ ¯ _kλg_ ] _− ϵ∥_<sup>2</sup> **until** Converged 

### **F Hardware Details** 

We present the dual-arm platform constructed and utilized in this work. Two identical Realman RM75-6s robotic arms are mounted on a white lifting desk using four G-type fixtures. At their end-effectors, we fixed the OminiPicker grippers developed by AGIBOT together with RealSense-D405 short-range depth cameras. Both grippers communicate with the workstation through USB-to-serial protocols. In addition to the two cameras mounted on the robotic arm end-effectors, we also strategically positioned one RealSense-L515 high-precision depth camera on a tripod, positioned appropriately behind the arms to capture a complementary global view. All three cameras are directly connected to our workstation via USB 3.2 interfaces. The two robotic arms are connected to the same local area network as the workstation and communicate using the Ethernet-based SDK provided by Realman. An overview of the hardware setup is illustrated in Figure 12, while the corresponding hardware specifications are listed in Table 11 for reference. 


**Figure 12** Hardware feature. The wrist-mounted camera is the RealSense D405 model, with an optimal operating range of 7cm – 50cm, while the exterior camera is the RealSense L515 model, with an optimal operating range of 0.25m – 9m. The two robotic arms are of exactly the same model rather than mirror versions. 

26 

|Parameter|Value (%)|
|---|---|
|DoF|8 × 2 = 16|
|Arm weight|7.9 × 2 = 15.8 kg|
|Arm Payload|5000g|
|Arm reach|638.5mm|
|Arm Repeatability|0.05mm|
|Joint motion range|J1 _±_ 178°, J2 _±_ 130°, J3 _±_ 178°, J4 _±_ 135°, J5 _±_ 178°, J6 _±_ 128°, J7 _±_ 360°|
|Gripper range|120mm|
|Gripper weight|0.43kg|
|Gripper Payload|1.5kg|
|Gripper max force|30N|


**Table 11** Technical specifications. In this table, the term arm refers to the Realman RM75-6s model, while gripper refers to the Ominipicker developed by AGIBOT. 

## **G The Hidden Advantage of ATE : Safer and Smoother Manipulation** 


**(a)** 6-axis force data during a single Cook Bun task using the direct fine-tuned _π_ 0 model. 

**(b)** 6-axis force data during a single Cook Bun task using the _π_ 0 model fine-tuned with ATE . 

**Figure 13 Six-axis force comparison during the** **_Cook Bun_ task.** (a) Using the direct fine-tuned _π_ 0 model, the force signals exhibit instability and less structured patterns. (b) Using the _π_ 0 model fine-tuned with ATE, the force signals are smoother and more consistent, indicating improved robustness and better adaptation to the target embodiment. 

While our primary objective was to facilitate data-efficient adaptation by bridging the action distribution gap, our experiments revealed **a valuable and unanticipated benefit** : superior motion smoothness and more stable force control. We validate this finding through a detailed analysis of six-axis force measurements. The term six-axis force refers to forces and torques expressed in the coordinate frame rigidly attached to the target object: the three force components are along the positive directions of the coordinate axes, while the remaining three correspond to torques around these axes. 

When performing the cook bun task with the direct fine-tuned policy _π_ 0, we observed that the robot arm frequently exerts excessive force while placing the steam lid back on the steamer, which often led to deformation of the steamer. By contrast, when the same action was executed by the fine-tuned policy _π_ 0 with ATE, the deformation of the steamer was significantly mitigated. 

To quantitatively substantiate this observation, we used the built-in six-axis force sensor integrated into the robot’s end-effector to collect data during task execution. As shown in Figure 13a and Figure 13b, we selected the force component along the x-axis as the primary evaluation criterion. This is because we confirmed that, when placing the lid, the force transmitted from the lid to the gripper is aligned with the x-axis direction. The data presented in the figure are relative measures, obtained by subtracting the sensor readings at the initial pose from the raw sensor values. 

From the figures, it can be observed that the force curve of ATE exhibits fewer sharp fluctuations compared to that of the baseline and remains at a smaller overall magnitude. More specifically, across four representative 

27 

peaks and valleys, the baseline policy demonstrates a tendency to apply excessive and unnecessary downward force during the bun-grasping and lid-placing actions. 

This finding suggests that by constraining the fine-tuning process within the pre-training action latent space, our method implicitly guides the policy toward safer and more robust physical interactions. 

### **H Real-world Data Collection Details** 

In this section, we provide a detailed description of how our dataset is collected. As illustrated in Figure 14b, our real-world tasks involve bimanual simultaneous actions. If we were to rely on traditional single-operator teleoperation, accomplishing such tasks would impose excessive demands on the operator. To address this challenge, we adopt a dual-operator collaborative teleoperation approach for data collection. 


**(a)** Dual-arm collaborative teleoperation. 

**(b)** Bimanual task involves simultaneous actions. 

**Figure 14** The setup of real-robot data collection. (a) The overview of how we implement dual-arm data Collection. During teleoperation, the operator holds Joycon with the hand which not cared about by our program. (b) An example that requires both hands to perform logically disparate tasks, simultaneously occurs in the _use toaster_ task. 

In the dual-operator teleoperation setup, each operator is first equipped with a separate Vision Pro headset, both of which are connected to the same local area network. We then employ the open-source project TrackingStreamer to extract hand-keypoint estimations from the Vision Pro devices and stream them to our workstation. Note that in the wrist pose estimated by Vision Pro, the attached coordinate frame on the wrist differs in orientation from the coordinate frame defined on the Realman robotic arm. To ensure consistency, we apply a right-multiplication with a predefined rotation matrix _T_ rotation to the wrist frame, so that when both the wrist and the robotic arm are in their initial poses, the directions of their coordinate frames are aligned. 

After both operators place their corresponding hands (which control the robotic arms) in the initial positions and press the initialization button, the program immediately records the wrist estimation from Vision Pro at that moment, and treats it as the initialization matrix for the current data collection session. Next, we assume the existence of a transformation matrix, such that left-multiplying the initialization matrix with _T_ transform maps it to the robotic arm coordinate system, perfectly aligning it with the initial pose of the end-effector . By right-multiplying both sides of this equation with the inverse of the initialization matrix, we can solve for _T_ transform 

_T_ transform = _T_ ee_init( _T_ vision_init _T_ rotation)<sup>_−_1</sup> 

where _T_ ee_init denotes the initial pose of the end effector in the robot coordinate system, and _T_ vision_init denotes the wrist pose estimated by Vision Pro at the time of initialization. For every subsequent step, Vision Pro’s wrist estimation is first multiplied by the right _T_ rotation and then by the left _T_ transform. This way, the motion and orientation of the hand can be directly mapped into the robotic arm coordinate system, 

28 

representing the desired end effector pose. By employing this mapping approach for teleoperation, it is only necessary to know the initial poses of the robotic arm and the initial pose of the interface to be used as the teleoperation reference. Moreover, under the requirements of our experiments, this method enables a clear separation of the two different robotic arms, thereby facilitating the realization of dual operator teleoperation. Next, we utilized the Pinocchio library to solve the inverse kinematics to get the joint angles, which are then transmitted directly to the robot for execution. Beyond using Vision Pro as our primary sensing hardware, we integrate Nintendo Joy-Con devices: operators can use the Joy-Cons to control the gripper’s open and close actions, thereby completely eliminating potential misrecognition issues since we use vision-based solutions. Additionally, Joy-Cons serve as auxiliary controllers to notify the operator of code errors, quickly set the robot arms, and confirm dataset recording, among other functions. 

The advantages of employing dual operator teleoperation can be outlined as follows. First, tasks requiring both arms to perform different actions simultaneously can be executed effortlessly, enabling the policy which fine-tuned on our dataset to demonstrate superhuman multitasking capabilities. Second, when one arm is idle, its wrist-mounted camera can be aimed at the other working arm, thereby providing three distinct visual perspectives for the active robotic arm. Third, operators are granted greater freedom of movement: they can walk around to achieve larger control ranges for their respective arms without worrying about the state of the other arm. Furthermore, since the two operators’ hands are spatially separated, the visual occlusion problem in HandOver-type tasks is naturally resolved. Finally, each of the operator only needs to master half of the skill set, which accelerates skill transfer when switching to new tasks and reduces operator workload. 

29 

