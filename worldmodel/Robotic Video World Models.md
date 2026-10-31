---
title: "Robotic Video World Models: A Survey of Applications, Research Challenges, Future Directions"
date: "2026-01-12"
authors: "Zhiting Mei; Tenny Yin; Ola Shorinwa; Apurva Badithela; Zhonghe Zheng; Joseph Bruno"
url: https://arxiv.org/abs/2601.07823
pdf: https://arxiv.org/pdf/2601.07823
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2601.07823)** / [論文ページ](https://arxiv.org/abs/2601.07823)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

**Robotic Video World Models: A Survey of Applications, Research Challenges, Future Directions** 

**Zhiting Mei**<sup>1</sup><sup>_∗_</sup> , **Tenny Yin**<sup>1</sup><sup>_∗_</sup> , **Ola Shorinwa**<sup>1</sup><sup>_∗_</sup> , **Apurva Badithela**<sup>1</sup> , **Zhonghe Zheng**<sup>1</sup> , **Joseph Bruno**<sup>2</sup> , **Madison Bland**<sup>1</sup> , **Lihan Zha**<sup>1</sup> , **Asher Hancock**<sup>1</sup> , **Jaime Fern´andez Fisac**<sup>1</sup> , **Philip Dames**<sup>2</sup> , **Anirudha Majumdar**<sup>1</sup> 

> 1Princeton University, 2Temple University 

- _∗_ Equal contribution. 

Video world models have emerged as promising candidates for high-fidelity world models, offering the potential to synthesize high-quality videos capturing fine-grained interactions between agents and their environments conditioned on multi-modal user inputs. Their impressive capabilities address many of the long-standing challenges faced by physics-based simulators, driving broad adoption in many problem domains, e.g., robotics. For example, video models can generate photorealistic, physically consistent deformable-body simulation without making prohibitive simplifying assumptions, which is a major bottleneck in physics-based simulation. Moreover, video models can serve as foundation world models that capture the dynamics of the world in a fine-grained and expressive way. They thus overcome the limited expressiveness of language-only abstractions in describing intricate physical interactions. However, despite their potential, video models still generate physics-violating future predictions, often manifesting as hallucinations. In this survey, we provide a review of video models and their applications as embodied world models in robotics, including efficient data generation and policy learning, dynamics and rewards modeling in reinforcement learning, policy evaluation, and visual planning. Further, we highlight important challenges hindering the trustworthy integration of video models, such as poor instruction following, hallucinations like violations of physics, and unsafe content generation, in addition to fundamental limitations such as significant data curation, training, and inference costs. We present potential future directions to address these open research challenges to motivate research and ultimately facilitate broader applications, especially in safety-critical settings. We provide a curated bibliography at `https://github.com/irom-princeton/awesome-robotics-video-world-model-papers` . 

**Keywords: Video Generation Models, World Modeling, Visual Planning, Policy Learning and Evaluation** 

**Bibliography: github.com/irom-princeton/awesome-robotics-video-world-model-papers** 


**Figure 1 Overview.** As embodied world models, video models offer immense potential in high-fidelity future prediction, overcoming some of the most notable challenges faced by classical physics-based simulators. These capabilities drive state-of-the-art advances in generalist robot policy learning, policy evaluation, and visual planning. 

1 

# **1 Introduction** 

Recent breakthroughs in generative modeling, such as diffusion and flow-matching [1, 2], have enabled high-fidelity controllable video synthesis conditioned on user inputs such as text prompts, robot actions, and video frames. By training on internet-scale data, state-of-the-art (SOTA) video models learn to create rich videos that capture aesthetic and dynamic (motion) effects (e.g., with cinematic lighting, camera motion, and physical interaction between agents), driving widespread applications in video editing and content creation [3–11]. As a result, these models have been increasingly integrated into robotics, e.g., in robot data generation, visual planning, policy learning, and policy evaluation [12–17], drawing upon their impressive zero-shot generalization capabilities [18]. In this survey, we provide a review of video models, highlighting their capabilities, applications in robotics, and limitations. 

The advent of large vision-language models (VLMs/LLMs) [19–21] has significantly transformed the state of the art in many problem domains (e.g., natural language processing, computer vision, robotics, etc.) due to their remarkable language generation and commonsense reasoning capabilities. Through pretraining on internet-scale data, LLMs learn broad foundational knowledge required to solve a wide range of tasks, which has resulted in their emergence as impressive zero-shot AI models. For example, VLMs function as the backbones of SOTA vision-language-action robot policies [22–24], which enable robots to perform diverse tasks with a single (unified) policy in place of multiple task-specific policies. Despite these impressive capabilities, language models face some important limitations. First, language-only abstractions lack the expressiveness required to efficiently capture the intricate interaction processes inherent in the physical world. For example, consider the task of creating a concise fine-grained description of the contact interactions between a robot’s gripper and a target deformable object, e.g., a cloth. Such a task is immensely challenging due to the high density of information and the limited capacity of language. Second, language-centric modeling fails to accurately model the spatial and temporal dependencies between real-world phenomena (events) that are crucial to comprehensively understanding the physical world. Although physics-based simulators offer visual world modeling capabilities, their practical effectiveness is limited by a number of fundamental challenges. Particularly, physics-based simulation generally requires restrictive simplifying assumptions that hinder the visual and physical fidelity of their predictions. For example, physics engines require expensive asset curation procedures to minimize the sim-to-real gap and struggle to accurately simulate deformable bodies with complex morphology and dynamics. Video generation models offer a path towards overcoming these limitations by serving as photorealistic, physically consistent spatiotemporal models of the world. These capabilities, alongside their long-term potential, have catalyzed the adoption of video models across various robotics applications. 

In robotics, video models have been increasingly adopted as embodied world models [25–28]. High-fidelity world modeling establishes a trustworthy foundation for efficient evaluation of robot policies [16, 17, 29, 30]. Traditionally, _policy evaluation_ has necessitated setting up real-world robot stations for online policy roll-outs, which is notably expensive given the pertinent hardware and labor cost. Video models can circumvent this bottleneck without compromising the reliability of evaluation results. Additionally, video models can provide high-fidelity dynamics and rewards predictions for training robot policies using reinforcement learning [31–34], while also enabling _cost-effective robot data generation_ in imitation learning. While data scaling has proven to be a critical recipe for advancing the performance of SOTA robot policies [23, 35], collecting expert demonstration data is incredibly expensive, posing a significant limitation. Video models can facilitate scalable data generation without relying on human supervision, addressing this pressing challenge. The expert demonstrations from video models can also be directly applied to a robot through motion retargeting [36–38]. Beyond generating successful task demonstrations, video models can synthesize failure video trajectories that endow robot policies with corrective behaviors for more robustness. Further, the generated data can be optimized through _visual planning_ to compute more optimal robot trajectories [14, 15, 39–42]. 

Although video models provide valuable capabilities, their integration into robotics faces notable limitations. Like LLMs, video models tend to hallucinate, generating videos that are physically unrealistic, e.g., with objects appearing/disappearing or deforming in ways that violate physics [43–46]. Video models also struggle to follow user instructions [47, 48], especially in long-duration video generation tasks [49–51]. Further, significant data curation, training, and inference costs and the lack of adequate content safeguards in video generation remain critical challenges [52, 53], hindering broader adoption in robotics. Addressing these challenges constitutes a 

2 

crucial roadmap for future work, ultimately enabling video models to realize their full potential. 

This survey provides an extensive overview of video models, identifying prevailing model architectures, key applications in robotics, and major challenges. We highlight four prominent applications of video models as embodied world models in robotics, including: (i) robot data generation and action prediction in imitation learning, (ii) dynamics and rewards modeling in reinforcement learning, (iii) policy evaluation, and (iv) visual planning, as illustrated in Figure 1. Furthermore, we outline important open research challenges impeding trustworthy applications of video models in robotics and present important directions for future research to address these problems. 

**Comparison to Existing Surveys.** Prior survey papers have covered video generation models broadly, particularly video diffusion models, identifying the prevailing model architectures [54, 55], techniques for controllable video generation [56], core applications in video generation, video editing, and video understanding [57]. Other surveys [58–61] provide a broad discussion of world models, presenting a valuable review of research across a wide range of model architectures, such as recurrent neural networks, transformers, language models, and scene reconstruction models, e.g., Gaussian Splatting. Prior work also highlights the unified framework for information representation and task formulation provided by video models [62] and discuss the progression in the capabilities of video models, through a primarily historical lens, along with potential future capabilities [63]. Although relevant for broader understanding, these existing surveys lack a comprehensive review of generative video models as world models in robotics [58–61] or an extensive discussion of specific applications, associated challenges, and future directions of generative video models in robotics [54–57, 63]. In contrast, our survey provides an exhaustive discussion of video generation models in robotics, especially in robot manipulation, which has not been considered by existing surveys unlike areas such as autonomous driving [64–67]. 

**Research Methodology.** We surveyed the literature for papers related to video generation with particular emphasis on applications to robotics, checking online sources, paper references, and individual suggestions. We considered all publicly accessible papers up to December 2025, aggregating them in a local database. To identify more relevant references, we categorized these papers into foundational methods such as diffusion modeling/flow-matching; application-centric solutions, e.g., in robot policy learning, planning, and policy evaluation; and benchmarks and datasets, including evaluation metrics. Given the broad range of papers on the foundations of video generation, we limit our discussion to seminal papers, along with significant papers introducing new ideas that have been widely adopted by other papers discussed in this survey. In contrast, we include all papers focused on applications of video models to robotics in this survey, especially those where video generation plays a critical role. Likewise, we include all representative video generation benchmark and dataset papers, given their significance to future research. To facilitate further research, we provide a curated bibliography at `https://github.com/irom-princeton/awesome-robotics-video-world-model-papers` . 

**Taxonomy.** We categorize existing literature around its practical applications, framing these domains as the primary vectors of impact for video world models in robotics. This functional taxonomy yields three core contributions. First, it contextualizes state-of-the-art world-modeling methodologies within fundamental robotic paradigms—specifically policy learning, evaluation, and visual planning, thereby rendering the field accessible to a multidisciplinary audience. Second, it systemically identifies the inherent boundaries of current frameworks, illustrating how video-driven approaches can mitigate these limitations. Finally, this taxonomy charts the critical open challenges remaining in the field, detailing the barriers to achieving physics-aligned future prediction, thereby offering a strategic roadmap to guide future research. 

**Organization.** We discuss the organization of this survey, as summarized in Figure 2. In Section 2, we provide an overview of important concepts that are crucial to understanding generative video modeling. We begin with a discussion of learned world models, highlighting the evolution of these models from (latent) state-based representations to high-fidelity video-based representations. Further, we review diffusion/flow-matching-based modeling highlighting the core principles behind their success. In Section 3, we present major applications of video models in robotics, encompassing robot data generation and action prediction in imitation learning, dynamics and rewards modeling in reinforcement learning, policy evaluation, and visual planning. In Section 4, we highlight useful metrics and benchmarks for evaluating video models. Subsequently, we identify open research challenges in Section 5 and suggest directions for future research. We conclude the survey in Section 6. 

3 


**Figure 2 Organization.** The organization of this survey, including background material, taxonomy of robotics applications, evaluation metrics and benchmarks, and open challenges and directions for future research. 

4 

# **2 Background** 

In this section, we provide relevant background concepts that are essential to understanding the material presented in this survey. We begin with a brief introduction of world models, followed by an overview of video models. Specifically, we categorize video models broadly into non-diffusion-based video models and diffusion/flow-matching-based video models. State-of-the-art video models generally utilize diffusion or flow-matching for high-fidelity video synthesis. As a result, we provide a more comprehensive discussion of these models. 

## **2.1 Learned World Models** 

Many robotics algorithms require a model of the robot’s environment to efficiently learn policies that are effective in the real-world, especially when real-world interactions are prohibitively costly or unsafe. For example, reinforcement learning (RL) methods [137, 138] generally require a large number of interactions between an agent and its environment to learn useful behaviors, which is typically expensive in the real-world. World models enable scalable data collection for training these policies with little to no real-world interaction. At their core, world models predict the evolution of the environment of an agent due to interactions. Traditionally, physics-based simulators [139, 140] have been utilized as world models for predicting the dynamical effects of a robot’s actions. However, physics-based simulators typically utilize simplified physics engines that approximate physical laws for computational feasibility, introducing inductive biases that limit their realism, e.g., in simulating non-rigid objects. Importantly, these approximations often contribute to the sim-to-real gap in robotics, impeding successful transfer of simulation-trained robot policies to the real-world. Moreover, robot manipulation tasks have become increasingly complex, exacerbating these challenges. 

Learned world models [141, 142] have emerged as an effective solution to these challenges. We can broadly classify learned world models into two categories: _Markovian state-based_ world models and _video_ world models. 

**Markovian State-Based World Models.** A state refers to a description of the environment of an agent at a given time step, which could include its RGB observations, proprioception, or latent embeddings of these observations at past and current time steps. Markovian state-based world models assume that the future evolution of the agent’s environment only depends on the agent’s state _st_ at the current time step _t_ and its action _at_ , which represents either a physical action or a latent action. Markovian state-based world models are trained to predict the future state _st_ +1, given the current state _st_ and action _at_ : _st_ +1 _∼ pη_ ( _st_ +1 _|st, at_ ) _,_ where _pη_ represents the dynamics predictor with parameters _η_ . These world models generally operate in latent space and are composed of an encoder for embedding observations into a latent space, dynamics predictor, and rewards predictor, given by: 

Encoder: _st ∼Eγ_ ( _st|ot_ ) _,_ Dynamics: _s_ ˆ _t_ +1 _∼ pη_ (ˆ _st_ +1 _|st, at_ ) _,_ Rewards: _r_ ˆ _t_ +1 _∼ pζ_ (ˆ _rt_ +1 _|s_ ˆ _t_ +1) _,_ (1) 

with parameters _γ_ and _ζ_ for the encoder and rewards predictor, respectively. 

Prior work [68, 69, 143–146] has largely parameterized the dynamics predictor _pη_ using recurrent neural networks (RNNs) or recurrent state-space models (RSSMs). However, more recent works employ transformers [70] and diffusion in pixel space [147–149] or latent space [150, 151] for more expressive dynamics prediction. In general, world models [70, 74, 75, 88, 143, 152, 153] are trained to minimize the error between the predicted and ground-truth next state, either in latent space or reconstructed pixel space using the mean-squared error (MSE) loss function [70, 147] or the Kullback-Leibler (KL) divergence loss [68]. We refer interested readers to [58] for a detailed review of these models. 

**Video World Models.** To model the world, video models learn spatiotemporal mappings that capture the evolution of an environment over space and time, without explicitly modeling a Markovian state, in contrast to Markovian state-based world models. In general, video models apply non-linear transformations to the patches or pixels of a video frame to propagate the environment dynamics. Early research in video prediction applied spatial transformations to pixels to generate future frames [154, 155]. However, these transformations capture only local perturbations of the frames, limiting their expressiveness in more complex video generation, e.g., with dynamic backgrounds. Other methods [71, 156] extend generative adversarial networks (GANs) 

5 


**Figure 3 Diffusion Video Model Architectures.** Diffusion/Flow-matching has emerged as the dominant model architecture for training photorealistic controllable video models that can be steered using text, image, and other conditioning inputs. These models broadly utilize diffusion transformers (DiTs) or U-Nets to learn important interpendencies across space and time within a compact latent space. 

[157] to video prediction for higher video fidelity. However, the susceptibility of GANs to mode collapse limits their ability to model diverse potential video evolution paths. 

Subsequent work [72, 73, 158–160] uses variational inference via variational autoencoders [161] to learn a latent distribution over pixels, explicitly encoding the stochasticity in video prediction within the latent distribution. Given the success of transformers in language modeling, the work in [162] introduces the video transformer, achieving higher-quality video generation through autoregressive predictions. However, powerful autoregressive decoders introduce the challenge of latent collapse, where the learned model fails to efficiently use the latent space. Vector-quantized variational autoencoders (VQ-VAEs) [10, 11, 28, 73, 159, 163, 164] address this issue by quantizing the latent representations into discrete codes in a codebook. VQ-VAEs are typically pre-trained on large-scale image and video datasets with a reconstruction objective on compact per-frame latent embeddings achieved through spatial and temporal compression. 

Despite the resulting performance gains, these video models lack the ability to capture complex interactions within an environment, limiting their applications. These limitations have been addressed by diffusion and flow-based matching, enabling video models to learn highly expressive representations of the physical world. We provide a detailed discussion of these video models in the subsequent subsections, along with a brief overview of joint-embedding predictive architectures, which seek to learn world models from video data without predicting pixel-level visual details. 

## **2.2 Diffusion/Flow-Matching Video Models** 

The emergence of diffusion modeling [1] and flow-matching [2] has transformed the SOTA in image and video generation [165, 166], achieving high-fidelity video generation that capture fine-grained realistic and cinematic effects. Given the similarity between diffusion modeling and flow-matching, we limit our discussion to diffusion models for simplicity. We refer readers to [2] for a more detailed presentation of flow-matching. Diffusion models [1, 167] have gained prominence as a powerful formulation for generative models that synthesize data by modeling an iterative denoising process. Given data **x** 0 _∼ q_ ( **x** 0), the _forward process_ (also called the diffusion process) progressively corrupts clean data **x** 0 with Gaussian noise over _T_ time steps under some noise schedule _{βt}_<sup>_T_</sup> _t_ =1<sup>,givenby:</sup><sup>_q_(</sup><sup>**x**</sup><sup>_t|_</sup><sup>**x**</sup><sup>_t−_1) =</sup><sup>_N_</sup> � **x** _t_ ;<sup>_~~√~~_</sup> 1 _− βt_ **x** _t−_ 1 _, βt_ **I** � _._ Conversely, the _reverse process_ iteratively removes the noise added to the images in the forward process. These transitions are supervised via a noise-based or velocity-based loss function [1], given by: _L_ **_ϵ_** = E **x** 0 _,t,_ **_ϵ_** and _L_ **_v_** = E **x** 0 _,t,_ **_v_** _t_ , � _∥_ **_ϵ_** _−_ **_ϵ_** _θ_ ( **x** _t, t_ ) _∥_<sup>2�</sup> � _∥_ **_v_** _t −_ **_v_** _θ_ ( **x** _t, t_ ) _∥_<sup>2�</sup> respectively. 

Early diffusion models [76] operate directly in the pixel space, which is prohibitively expensive at high 

6 

resolutions. To overcome this limitation, recent approaches adopt a latent diffusion paradigm, where observations are first compressed into a lower-dimensional latent space using a variational autoencoder (VAE) [10, 11, 77, 168, 169] or pretrained encoders [170] prior to the diffusion process. Diffusion models are broadly parameterized using U-Nets [171, 172] or transformers [173, 174]. Early works on video diffusion [76, 77, 133, 175] extend 2D U-Nets to the spatiotemporal domain by lifting 2D convolutions to 3D or by introducing temporal attention modules to jointly model spatial and temporal dependencies. More recent work [173, 174] replace the traditional U-Net backbone with a diffusion transformers (DiT), leveraging the expressivity of self-attention mechanisms. This design trades the U-Net’s inductive biases toward locality and translation equivariance for a more flexible capacity to model long-range dependencies and higherorder semantic relationships, which are important in temporally-coherent long-video generation, an essential requirement in robotics. Consequently, SOTA video models [5, 7, 9, 10, 174] utilize DiT-based architectures. 

Although inherently unconditional, diffusion models must be conditioned on tasks or robot actions for applications to robotics, which is achieved through classifier-based and classifier-free guidance. Classifier-based guidance [165] trains a classifier that learns to predict an attribute (label) _y_ from a noisy sample _xt_ , denoted as _pϕ_ ( _y | xt_ ), which provides a steering mechanism at inference time. To circumvent the high computation costs and training instability associated with this approach, classifier-free guidance [176–180] trains a joint conditional and unconditional model which is steered towards desirable outputs via a modulated conditioning signal. 

Conditioning is typically achieved through channel concatenation, cross-attention, or adaptive normalization. While channel concatenation enforces spatially-aligned interactions by augmenting the inputs or latent representations along the channel dimension, cross-attention captures primarily semantic, non-spatial interactions between intermediate video features (queries) and the conditioning signal (keys and values) [181], e.g., with text inputs. In contrast, adaptive normalization methods such as AdaLN or FiLM [182, 183] provide global attribute control (e.g., target frame rate or motion intensity) through scale and shift modulation of normalization layers. These mechanisms are directly employed in text-to-video (T2V) generation [184, 185] via cross-attention, image-to-video (I2V) generation [77, 177] with frame-level input concatenation and text-video cross-attention, and action-conditioned (AC) motion/trajectory-guided generation [11, 16, 17, 30, 186–188] using coordinate maps, optical flow fields, keypoint heatmaps, applied forces, or robot joint/end-effector positions. 

## **2.3 Video Joint-Embedding Predictive Architecture Models** 

Here, we discuss methods based on joint-embedding predictive architectures (JEPAs) [78, 79, 81] that learn world models from internet-scale videos for future prediction, video understanding, and planning in latent space. In contrast to diffusion/flow-matching video models, which prioritize photorealistic video generation, video JEPA models [79, 81] seek to learn effective latent representations through self-supervised training on video data. JEPAs build on contrastive learning approaches that identify salient characteristic features of (image) inputs to distinguish between similar and dissimilar (image) pairs, where similar examples are typically generated via data augmentation, e.g., through cropping, resizing, color distortions, or noise injection. These augmented inputs are mapped to latent embeddings using a learned model, which is trained using the exp(sim( _zi,zj_ <u>)</u> _<u>/τ</u>_ <u>)</u> InfoNCE loss function: _Li,j_ = _−_ log <u>�2</u> _kN_ =1<sup>1</sup><sup>_k̸_=</sup><sup>_i_exp(sim(</sup><sup>_zi,zk_)</sup><sup>_/τ_)</sup><sup>_,_wheresim(</sup><sup>_·_)correspondstothenormalizeddot</sup> product of the two vectors, given a positive image pair ( _xi, xj_ ) from a dataset of _N_ image pairs. 

To minimize the risk of representation collapse often associated with contrastive learning, JEPA utilizes an asymmetric architecture for embedding input images, comprising a student encoder, a target encoder, and a predictor. Video joint-embedding predictive architecture (V-JEPA) models [79, 81] build upon this foundation for video generation, predicting spatially and temporally masked features within the latent space. By making predictions within the latent space as opposed to pixel space, the model is encouraged to predict higher-level representations rather than pixel-level information [80]. This abstract understanding allows the model to build an internal world model, enabling it to also make predictions about future states and plan without task-specific training or reward, which is often unavailable in robotics. For conditional video generation, the model is trained with the loss function: min _θ,ϕ,_ ∆ _y ||Pϕ_ (∆ _y, Eθ_ ( _x_ )) _−_ sg( _Eθ_ ¯( _y_ )) _||_ 1 _,_ , with future latent embeddings from the predictor network _Pϕ_ and frame embeddings from the encoder _Eθ_ and exponentially-moving variant _Eθ_ ¯ at the current timestep, where sg( _·_ ) denotes the stop-gradient operator. After _Eθ_ has been trained, it can be 

7 


**Figure 4 Video Models for Embodied World Modeling.** Video models provide high-quality representations of the physical world, which could be implicit (e.g., latent and video representations) or explicit (e.g., point clouds and Gaussian Splatting models). 

frozen and used to train a transition model with additional action-labeled trajectory data [81]. Although JEPA models are more robust to collapse, they can still be prone to representation collapse [189], although they are more robust compared to prior approaches. Regularizers [190, 191] have been shown to help prevent posterior collapse, but are difficult to tune and interpret [189]. 

# **3 Applications of Video Models in Robotics** 

In this section, we explore applications of video models as high-fidelity world models in robotics. World models capture the evolution of an environment under the effects of actions applied by an agent. However, modeling physical interactions is extremely challenging, given the stochastic nature of dynamical interactions, which is often not fully described by simplified physical laws. Although early world models [69, 143] effectively learn high-level scene dynamics, they struggle with modeling intricate dynamical changes, especially with high-fidelity. Notably, in fine-grained interaction tasks in robotics, such as dexterous manipulation, these models often fail to predict the effect of subtle changes in robot actions that have significant impacts on the success of such tasks. For high-fidelity world modeling, these models generally require lots of training data centered around such dynamical events for effective supervision, which is often difficult to collect in many practical applications. More traditional physics-based simulators function as world models; however, their capabilities are often limited by restrictive assumptions built on simplified object models and dynamics models. For example, physics-based simulators typically struggle with deformable-body simulations, which require higher-fidelity dynamics model. Importantly, these assumptions contribute to the sim-to-real gap faced by physics-based simulators, e.g., through the use of primitive object shapes, appearance and visual conditions. Recent work in robotics seeks to address these limitations by leveraging video models as _embodied world models_ . 

Video models offer a promising path to high-fidelity physical world simulation, without a prohibitive demand for large-scale action-labeled datasets. Recent approaches [8, 25, 26, 192, 193] fine-tune pre-trained video models to autoregressively synthesize 4D scene representations, generating new future frames conditioned on past generated ones. Based on their underlying scene representations, video world models can be classified into two categories, based on the maintained scene representation, namely: _implicit_ and _explicit_ video world models, as illustrated in Figure 4. 

**Implicit video world models.** In implicit video world models, the 3D scene representation is encoded exclusively within the video model, without any external representation. As such, visualization of the evolving scene can only be achieved by generating videos from the video model. Implicit representations 

8 

circumvent the rigid inductive biases common in alternative approaches, yielding superior generalization with fewer assumptions while eliminating the need for auxiliary sensor-based supervision, such as depth maps. Recent works extensively leverage this flexibility for more versatile video generation across both scene-centric [188, 192, 194] and object-centric [195] paradigms, often incorporating fine-grained language steering [25] via causal attention and diffusion forcing [124]. Within these frameworks, conditioning modalities diverge: whereas some approaches [192] rely solely on text prompts, others [25, 26, 154, 194, 196, 197] fine-tune pre-trained models on control-centric robot datasets (e.g., Bridge [198], DROID [199]) to achieve action-conditioned synthesis. Nonetheless, lacking structural constraints, these implicit methods demand substantially more training data to internalize underlying physical laws. 

**Explicit video world models.** In contrast to implicit approaches, explicit video world models ground future predictions in a concrete 3D/4D spatial representation derived from multi-view frames or geometric depth maps, modalities that are often unavailable in real-world settings. To circumvent this data scarcity, recent explicit frameworks [26, 27] leverage cost-effective alternatives, such as simulation data, to scale training on multi-view video data conditioned on text and image inputs. However, synthesized multi-view frames typically yield a sparse representation of the physical world that may prove insufficient for fine-grained robotic manipulation. For finer spatial granularity, contemporary methods integrate structural graphics primitives, utilizing dense 3D Gaussian Splatting fields [200], camera ray map back-projection [193], or volumetric voxel grids [201]. 

Given their growing capabilities, video models enable a broad range of downstream robotics applications, including: (i) efficient data generation and action prediction in imitation learning, (ii) expressive dynamics and reward modeling in reinforcement learning, (iii) scalable policy evaluation, and (iv) visual planning for model predictive control. 

## **3.1 Cost-Effective Data Generation and Action Prediction in Imitation Learning** 

In recent years, impressive research advances in robotics have been driven by imitation learning on large-scale expert demonstrations, circumventing the well-documented challenges associated with explicitly modeling dynamical interactions between robots and their environments. For example, SOTA vision-language-action (VLA) models [23, 24, 202, 203] have demonstrated remarkable capabilities in generalist language-conditioned robot manipulation, exhibiting strong task and environment generalization and robust recovery behaviors in the presence of disturbances. Scaling these foundation models—both in parameter size and training data volume—has proven essential to realizing such performance leaps, mirroring the scaling paradigms that underscored the success of large language models. However, the immense time and labor costs associated with collecting large-scale, high-quality expert demonstrations pose a critical bottleneck to further advancement. To address this challenge, recent work [12, 83, 107, 204–206] employs video models as cost-effective data generators of expert demonstrations, bypassing the overhead of human-supervised data collection. Concurrently, recent research has explored the use of video models as policy backbones in imitation learning, seeking to harness the synergies between dynamics prediction and policy learning to ground proposed robot actions. Table 1 summarizes related methods. 

**Video Models as Data Generators.** For scalable data generation, existing methods fine-tune pre-trained video models, such as Cosmos Predict [213] and Wan [10], on robot datasets for adaptation to robot embodiments and environments. However, the expressiveness of text-conditioned and image-conditioned video models is often too limited to capture the diversity of the training data required to train generalizable robot policies. Subsequent research on controllable video models [107, 179, 214, 215] seek to overcome this limitation through finer control of camera and object motion in generated videos, given an input text, image, keypoints, or trajectory vectors, describing spatial changes in the scene temporally. Some methods [206] further decompose the task into a set of subtasks for generating keyframes, which serve as conditioning inputs to generate videos for longer-horizon tasks. Other methods [204] train video models for effective cross-embodiment transfer, generating robot videos and extracting corresponding actions from models trained human video data. The resulting action-annotated data is used for policy learning, e.g., with VLA models [12, 213], or directly applied to a robot [36, 37, 216]. These methods typically recover robot actions from generated videos using an end-to-end approach or a modular approach. While modular approaches offer superior generalization, they are inherently prone to compounding errors across sequential stages, a limitation that end-to-end paradigms 

9 

**Table 1** Representative Video Models in Robot Data Generation and Policy Learning 

|Application|Method|Backbone|Architecture|Input Modality|Robot-Agnostic|
|---|---|---|---|---|---|
||DreamGen [12]|Wan 2.1 [10]|DiT|I2V|✗(GR1, Franka, SO-100)|
|IDM-Based Data|VPP [207]|SVD [77]|U-Net|I2V|✗(OpenX)|
|Generation|ARDuP [208]|SD [168]|U-Net|I2V|✗(Bridge)|
||Vidar [205]|Wan 2.2 [10]|DiT|I2V|✗(Aloha, AgiBot)|
||LuciBot [83]|KLING [4]|DiT|I2V|✗(N/A)|
|MtiRtti|AVDC [38]|ADM-G [165]|U-Net|I2V|✗(Sawyer, Bridge, Franka)|
|oon eargeng|VideoAgent [85]|ADM-G [165]|U-Net|I2V|✗(Sawyer, Bridge)|
||Dreamitate [86]|SVD [77]|U-Net|I2V|✗(xArm, UR5)|
||UVA [87]|Scratch|DiT|I2V|✗(ARX X5)|
||UWM [209]|Scratch|DiT|I2V|✗(DROID)|
|PliBkb|UniVLA [210]|Emu3 [211]|DiT|I2V|✗(AgileX)|
|ocy acone|Video Policy [212]|SVD [77]|U-Net|I2V|✗(DROID)|
||LVP [41]|Scratch|DiT|I2V|✗(N/A)|
||Mimic-Video [42]|Cosmos-Predict2 [11]|DiT|I2V|✗(Franka)|


effectively circumvent. Figure 5 illustrates these approaches, contrasting the two distinct action prediction paradigms. 

_End-to-end_ methods typically utilize latent action models (LAMs) or inverse-dynamics models (IDMs) to estimate actions from videos. LAMs [120, 121, 217] infer actions that explain the transition between a pair of video frames in latent space without the need for ground-truth actions, which often resides in a different action space. To learn latent actions without supervision, existing methods train an encoder-decoder model with a reconstruction-based loss function, typically implemented in latent space. The encoder takes in a pair of frames and outputs a latent action, which is passed into the decoder to recover the future frame. SOTA LAMs use VQ-VAEs as the model architecture for the encoder and decoder, given the superior tradeoff offered by VQ-VAEs in terms of expressiveness and training efficiency. Given the non-equivalence between the action space of the ground-truth and latent actions, LAMs often require a subsequent fine-tuning stage at deployment time to align the ground-truth and latent action spaces using a small set of action-labeled data. Unlike LAMs, IDMs [122, 123, 218] learn to predict actions from videos in a supervised fashion from action-labeled video data. Recent methods parameterize the video-to-action mapping using an encoder-decoder model trained with a diffusion objective. Although the need for ground-truth action labels poses a challenge to IDMs, IDMs do not require a fine-tuning stage, enabling zero-shot deployment in policy learning, either through direct action regression [12, 207] or video-based active-region localization [205, 208]. 

Broadly, _modular_ approaches [82–84] estimate the target object’s pose in each video frame, utilizing learned pose trackers [219, 220], monocular depth estimators [221], optical flow predictors [38], or CAD models [86] for 3D object pose estimation. The resulting object trajectory is subsequently retargeted (i.e., applied) to the robot, under the assumption that a fixed rigid transformation exists between the object’s reference point and the robot’s end-effector. By taking advantage of low-level control routines, these methods can be deployed zero-shot without the need for a separate fine-tuning stage for aligning the action spaces between training and deployment. 

**Video Models as Policy Backbones.** Unified video-action methods employ video models as policy backbones, co-training robot policies to jointly predict videos and actions conditioned on a language instruction and initial observation. While most unified video-action methods [87, 209, 222, 223] utilize a VLA architecture for these policies, more recent work [41, 42, 212] directly adapts pre-trained video models for joint video and action generation using autoregressive transformer architectures [87, 222–224], typically with diffusion-based supervision [88, 209, 210, 212, 225]. By jointly modeling future frame prediction and action estimation, these policies exploit the causal relationship between a robot’s actions and subsequent environmental states, enabling effective inference-time optimization toward a desired goal. Furthermore, these unified architectures inherently support diverse downstream tasks, such as modeling forward and inverse kinematics. While pre-trained policy backbones instill robust physical priors that enhance out-of-distribution generalization, they can be challenging to fine-tune effectively compared to models trained from scratch. 

10 


**Figure 5 Video Models for Data Generation.** Generative video models provide a scalable pathway for high-fidelity data generation, enabling cost-effective robot policy learning. Robot actions can be extracted from videos through modular approaches using end-effector pose tracking or end-to-end approaches, such as inverse-dynamics methods. 

## **3.2 Dynamics and Rewards Modeling in Reinforcement Learning** 

Although imitation learning provides a more sample-efficient training pipeline than reinforcement learning (RL), the resulting policies notoriously fail to generalize outside the training data distribution. RL mitigates these generalization bottlenecks; however, it requires well-defined dynamics models and reward functions, both of which are notoriously difficult to hand-engineer in complex physical domains. Further, due to its low sample efficiency, RL requires large amounts of training data to achieve the same level of performance as imitation-learned policies. To address these limitations, recent research explore video models as expressive backbones for dynamics and rewards modeling, as summarized in Table 2 

Whereas earlier works utilized recurrent state-space models [226] or image diffusion frameworks [227] for dynamics prediction, more recent approaches leverage video diffusion models, which yield higher-fidelity and more physically consistent rollouts. This training paradigm typically begins with a pre-training phase for textconditioned video generation, followed by a post-training phase on action-aligned trajectories to achieve precise action-space alignment [31]. Once aligned, these video world models can be directly deployed as dynamics and reward predictors during reinforcement learning (RL) policy fine-tuning [90]. Alternatively, reward signals can be derived by evaluating the generated video frames with vision-language models (VLMs) [32], or computed natively via video prediction likelihood [33] and conditional entropy metrics [34]. Although VLMs offer superior generalization capabilities, they are susceptible to hallucinations that can introduce misleading signals, thereby impeding the learning process. 

## **3.3 Scalable Policy Evaluation** 

Beyond policy learning, video models offer a path towards reliable policy evaluation that is reproducible across different environments and task settings. Real-world evaluation of robot manipulation policies is notably challenging due to the significant inherent hardware and labor costs, especially for generalist robot policies, which typically require evaluation across a combinatorial number of operating environments. For example, each hardware trial requires human monitoring to reset the environment, observe the policy rollout, and record success scores, which is typically expensive. While hardware evaluation is the gold-standard, policy evaluation 

11 

**Table 2** Representative Video Models in Dynamics and Rewards Modeling in Reinforcement Learning 

|Application|Method|Backbone|Architecture|Input Modality|Robot-Agnostic|
|---|---|---|---|---|---|
|DiPditi|World-Env [32]|Scratch|U-Net|AC-I2V|✗(Franka)|
|ynamcs recon|GVM2A [90]|ADM-G [165]|U-Net|AC-I2V|✗(Franka, Sawyer)|
|RdPditi|VIPER [33]|VideoGPT [164]|VQ-GAN|I2V|✗(RL-Bench)|
|ewar recon|Diffusion Reward [34]|VQ-Diffusion [228]|VQ-GAN|I2V|✗(Sawyer)|
|Dynamics & Reward Prediction|Dreamer 4 [31]|Scratch|DiT|AC-I2V|✗(Bridge)|


**Table 3** Representative Video Models in Policy Evaluation 

|Method|Backbone|Architecture|Input Modality|History-conditioned|Robot-Agnostic|
|---|---|---|---|---|---|
|IRASim [92]|Scratch|DiT|AC-I2V|✓|✗(RT-1, Bridge)|
|WorldEval [91]|Wan 2.1 [10]|DiT|AC-I2V|✗|✗(AgileX)|
|WorldGym [16]|Scratch|DiT|AC-I2V|✗|✗(Bridge)|
|Ctrl-World [17]|SVD [77]|U-Net|AC-I2V|✓|✓(N/A)|
|Cosmos-Eval [93]|Cosmos-Predict2 [11]|DiT|AC-I2V|✓|✗(Bridge)|
|Veo-Robotics [30]|Veo 2 [229]|DiT|AC-I2V|✗|✗(ALOHA 2)|


via physics-based simulation is the best available alternative, especially with recent improvements in visual fidelity, system identification, and careful tuning of material properties. However, physics-based simulation demands substantial initialization overhead, as each real-world environment must be manually reconstructed. This process requires the meticulous tuning of numerous parameters, such as asset lighting and material surface properties, to mitigate the sim-to-real gap. In contrast, video models [230–232] offer a higher-fidelity, more scalable framework for policy evaluation, modeling intricate robot-environment interactions that are challenging for physics-based simulators, e.g., in deformable-body simulation. 

We survey a growing body of research on methodologies for video-model-based policy evaluation, spanning diverse techniques for policy comparison and the estimation of real-world success rates, as summarized in Table 3. These studies demonstrate that video world models can serve as high-fidelity verification tools prior to real-world deployment. Specifically, real-world success rates can be quantified by executing the policy in closed-loop simulations with a video model, conditioned on initial observation samples and task instructions [16, 17, 26, 29, 30, 91–93]. To improve the quality and consistency of video generation, some architectures [91] condition the video model on the latent action representation in the policy, instead of conditioning on the robot’s physical actions [16, 17]. Moreover, several architectures incorporate multi-view image conditioning to reduce hallucinations [17], effectively leveraging the multi-camera configurations typically deployed in robotic manipulation setups. To further mitigate prediction errors that accumulate over long rollouts, existing methods incorporate history during video generation, conditioning future video frames not only on the current observation but also on past observations. The history may consist of all frames within a fixed window length [16, 29, 92] or a sparsely sampled subset of past frames [17, 26]. Moreover, augmenting observations with corresponding robot joint poses has been shown to improve frame-level action controllability [17]. 

Each rollout is scored according to a rubric to quantify success (e.g., Bernoulli score, partial credit) on task completion and instruction following, and the scores of individual rollouts are aggregated into empirical success rates. To assess the accuracy of video models in policy evaluation, existing approaches [17, 30, 93] use metrics such as the Pearson correlation coefficient and the Mean Maximum Rank Violation (MMRV). The Pearson correlation coefficient measures the strength of the linear relationship between predicted and real-world success rates — a high correlation is achieved when policies with high real-world success rates also exhibit high success rates in video model evaluations, and policies with low real success rates similarly have low video model success rates. In contrast, rank violation captures ranking inconsistencies between policy pairs, weighting each violation by the absolute difference in real-world success rates. The MMRV score is computed as the average across policies of their maximum rank violations. Although the predicted and real-world success rates do not always match, the evaluation results provide valuable insights for ranking the relative performance of policies, which is essential in improving robot policies in subsequent design and 

12 

**Table 4** Representative Video Models in Visual Planning 

|Method|Backbone|Architecture|Input Modality|History-Conditioned|Search|
|---|---|---|---|---|---|
|Visual MPC [39]|Scratch|RNN|AC-I2V|✗|Sampling|
|FLIP [15]|Scratch|DiT|I2V|✓|Tree Search|
|VLP [14]|Scrtach|U-Net|I2V|✗|Sampling|
|MindJourney [94]|Wan 2.2 [10]|DiT|AC-I2V|✗|Tree Search|
|SuSIE [96]|InstructPix2Pix [233]|U-Net|I2I|✗|Greedy|
|NovaFlow [13]|Wan [10]|DiT|I2V|✗|Greedy|


### training stages. 

Furthermore, video models can also be used to assess the robustness and safety of robot policies, particularly in out-of-distribution conditions [16, 30]. Such out-of-distribution scenarios can be rapidly constructed via image editing [30], e.g., to alter the background or add novel objects and distractors. This pipeline enables the use of video models to consistently predict performance degradation along different axes of generalization. Additionally, the pipeline can be readily interfaced with a VLM to generate safety-critical scenes and tasks for testing whether the policy executes semantically or physically unsafe behavior. Additionally, for accurate predictions across successful and failure scenarios, existing methods [29, 92, 93] incorporate failure data when training video models to avoid a bias towards always predicting success, which we discuss further in Section 5.9. 

## **3.4 Visual Planning for Model Predictive Control** 

Robot planning offers a compelling alternative to imitation learning, facilitating robust out-of-distribution generalization beyond the support of the training dataset. However, the design of high-fidelity models that closely predict the scene dynamics often proves prohibitively challenging. To address these drawbacks, recent work has explored utilizing video models in _visual planning_ , defined as the problem of synthesizing a sequence of images or video frames that show the steps necessary to complete a task specified by a language instruction and an initial observation. By leveraging the extensive diversity of the training data encoded by video models, these methods circumvent the need for large-scale expert demonstrations or explicit dynamics models to solve a broad range of robot tasks. 

Visual planning methods [234] generally optimize the generated video plans using sampling-based trajectory optimization methods, such as the gradient-free cross-entropy method, or gradient-based methods, e.g., gradient descent or Levenberg-Marquardt optimizers. The optimization routine is often embedded within a model predictive control (MPC) framework, facilitating the incorporation of new observations during planning via sensor feedback. Video-model-based visual planning methods can utilize _action-guided_ or _action-free_ approaches to create feasible robot trajectories, as outlined in Table 4. 

**Action-Guided Visual Planning.** Action-guided visual planning methods utilize a three-step approach: first, generating action proposals; second, synthesizing video trajectories using video models as dynamics prediction modules conditioned on these proposals; and third, evaluating the resulting trajectories against a predefined objective function. Broadly, the action proposals are typically generated by sampling-based approaches [39], learned approaches [15], or VLMs [14, 94]. Sampling-based approaches [39] primarily employ the cross-entropy method with subsequent optimization of the generated frames based on photometric/Euclidean error signals with respect to user-provided goal images or keypoints. Other approaches extend this framework by generating action proposals via learned models, such as autoencoders [15], VLMs [14, 94], or auxiliary video models [95], and subsequently scoring the candidate trajectories using either the proposal network itself or an external evaluation model [235]. 

**Action-Free Visual Planning.** In contrast, action-free visual planning methods bypass action proposal generation entirely, synthesizing future video plans directly from text-conditioned video models and utilizing the resulting frames as visual subgoals. For low-level execution, existing frameworks train goal-conditioned policies to derive robot actions from these image subgoals (e.g., via behavior cloning [96]) or employ IDMs to map current observations and subgoals directly to control actions [40, 236]. Alternatively, object pose 

13 

trajectories can be extracted from the generated videos [13] and refined through least-squares optimization prior to motion retargeting. 

# **4 Evaluating Video Models** 

In this section, we present standard metrics and benchmarks for evaluating video models across different dimensions, including perceptual quality, physical consistency, and semantic alignment with the input prompts. 

## **4.1 Metrics for Evaluating Video Models** 

To assess video generation quality in accordance with human judgment, various metrics are needed to evaluate video models on visual quality, temporal coherence, diversity of generation, and physical commonsense. Although many traditional image quality metrics [97, 98, 237] exist, these metrics do not assess temporal consistency of generated videos. To address this limitation, recent work [101, 101] has introduced video-specific metrics that measure video quality both spatially and temporally. Additionally, application-focused metrics are equally important. For example, in policy evaluation, the usefulness of an action-conditioned video model depends on how well it can predict policy success rate, and in policy learning, whether the generated demonstration data results in higher-performance policies [12]. Here, we discuss frame-level metrics and spatiotemporal consistency metrics. 

**Frame-level Metrics.** Traditional frame-level metrics from computer vision can be used to assess video generation quality, such as the peak signal-to-noise ratio (PSNR) [97] and structural similarity index (SSIM) [98]. Unlike PSNR, which is inversely proportional to the mean squared error of the pixel values, SSIM assesses image quality on luminance, contrast, and structure, which is more indicative of perceived similarity. Pixel-based metrics often fail to capture higher-order image structures that align with human perceptual judgments [98], which might be better represented in the learned feature spaces of deep models. For instance, the CLIP similarity score uses the cosine similarity between images in the embedding space [100] to assess semantic alignment between a pair of images. For generative models, the inception score [238] assesses if the model confidently generates diverse, yet semantically meaningful images by computing the expected KL-divergence between the predicted class distribution and the marginal distribution of all generated images. However, the inception score does not use real samples, depends on a fixed label space, and is not suited for image generation without a target object. The Fr´echet Inception Distance (FID) [239] addresses these challenges by computing the Wasserstein-2 distance between multi-dimensional Gaussian distributions over the real and generated feature embeddings. Likewise, the Learned Perceptual Image Patch Similarity (LPIPS) [99] is a similarity score on feature embeddings from several layers of a deep image recognition network, which has been shown to be comparable to human judgments. Furthermore, recent work [237] has demonstrated that these perceptual metrics can be learned to further align with human judgments. 

**Spatiotemporal Metrics.** While frame-level metrics focus on visual representation at any given video frame, assessing the temporal coherence of videos is also important for evaluating video generation quality. The Fr´echet Video Distance (FVD) [101] accomplishes this by extending the Fr´echet Inception Distance temporally to video representations that capture motion features across frames as well as the quality of images per frame. Instead of assuming a Gaussian representation for the features, the Kernel Video Distance (KVD) [101] uses a kernel-based metric (maximum mean discrepancy), to capture higher-order variations. The Fr´echet Video Motion Distance (FVMD) computes the Fr´echet distance on motion features by extracting keypoints that can be tracked across multiple frames and computing their velocities and accelerations. Prior work has also employed optical flow [10, 102, 240] to assess temporal coherence and VLMs [12, 44] to evaluate physical consistency of generated videos. 

## **4.2 Benchmarks for Evaluating Video Models** 

Despite their impressive capabilities, video models tend to generate videos that violate specific desired qualities, such as physical consistency, even when these videos are of high visual quality. Prior work [48, 241, 242] has introduced benchmarks to assess the performance of video models across different criteria, spanning visual quality, dynamic consistency, and instruction following. By evaluating video models across many dimensions, 

14 

these benchmarks highlight critical areas for future research, in addition to identifying SOTA video models. Generally, existing benchmarks demonstrate that video models fail to follow physical laws, even after scaling these models, although their aesthetic quality and temporal consistency tend to improve with scale. While many existing benchmarks evaluate the overall quality or physical consistency of generated videos from video models, only a few benchmarks assess the safety of generated videos. These safety benchmarks [52, 53] provide an extensive evaluation of the safety of video models, demonstrating their tendency to generate illegal or unethical videos that violate their safety guidelines. In the subsequent discussion, we present benchmarks that examine the overall quality of video models broadly and those that focus on evaluating physical commonsense. 

**Broad Benchmarks.** WorldModelBench [48] introduces a benchmark to evaluate the instruction following and physics adherence capabilities of video models, identifying physically inconsistent changes in the sizes of objects, which violate the law of mass conservation. Further, EvalCrafter [103] evaluates the quality of generated videos in terms of their aesthetic and motion quality as well as temporal consistency and text-to-video alignment. While visual quality is assessed using DOVER [243], motion quality is evaluated using action recognition methods, which are based on the activity classes in the Kinetics 400 dataset [244]. Temporal consistency and text-to-video alignment are measured using optical flow and CLIP, respectively. EvalCrafter shows that its evaluation criteria are well-aligned with human preferences. EWMBench [245] also evaluates video models along similar axes but uses the cosine-similarity metric with DINOv2 [246] embeddings to measure visual consistency. Furthermore, VBench [104] examines the performance of video models across sixteen fine-grained criteria, such as background consistency, subject consistency, and temporal flickering, in addition to aesthetic and semantic quality and instruction following. Like other benchmarks, VBench demonstrates that the results of each video model on each criterion is highly correlated with human preferences. Likewise, PAI-Bench [242] compares video models based on the temporal consistency, motion smoothness, and aesthetic quality of their generated videos. Beyond measuring overall video consistency, T2V-CompBench [105] evaluates object attribute consistency, such as color, shape, and texture, along with action consistency in generated videos. Similarly, WorldSimBench [47] assesses the physical consistency of motion, particularly the perception of a sense of depth, and changes in the velocity of objects in different media such as air and water. 

**Physical Commonsense.** Other benchmarks focus primarily on evaluating the physical commonsense of video models [43, 109]. For example, Physics-IQ [43] assesses video models’ understanding of the laws of physics, such as those on optics, thermodynamics, magnetism and fluid dynamics, revealing that contemporary models lack a foundational grasp of physical laws. Likewise, PhyGenBench [45] measures the commensense knowledge of video models on 27 physical laws, including gravity, sublimation, solubility, and friction, across 160 prompts. VideoPhy [44] evaluates models along analogous axes, placing a stronger emphasis on complex object interactions. Notably, VP<sup>2</sup> [106] examines the alignment of video models with physical laws in the task of visual planning, demonstrating that strong performance on perceptual metrics is generally not indicative of alignment with physical consistency. Further, VP<sup>2</sup> [106] shows that although scaling the model size and training dataset improves performance, the resulting gains plateau relatively quickly. 

## **4.3 Horizon of Video Model Evaluation** 

A unified framework for evaluating video models remains lacking, especially in the context of robotics applications. Existing metrics for evaluating video models generally assess either the perceptual quality [97, 98, 239] of their generated videos or their semantic consistency [100, 246]. While visual quality may be prioritized in content generation, physical consistency and predictive accuracy are more critical in robotics [106]. For example, robotics applications demand high-fidelity video generation to ensure consistency between predicted success rates and real-world success rates in policy evaluation and to mitigate compounding errors in downstream control applications. Given the lack of suitable metrics, researchers often resort to surrogate measures based on the downstream application, e.g., correlation between real and predicted policy success rates by video models, to approximate the performance of the video models [17]. Additionally, many works rely on human judgment to evaluate video model performance [107], which is qualitative, costly, and subject to bias. Designing effective evaluation metrics is critical in assessing the performance of video models, especially along the axes of physical, temporal, and semantic consistency. 

**Physical Consistency.** Physical consistency constitutes the most critical axis of evaluation for the successful integration of video models into robotics workflows. To serve as viable substitutes for physics-based simulators, 

15 

generative video models must yield future predictions that adhere to fundamental physical laws. However, current architectures remain limited by non-causal dynamical artifacts, such as objects appearing or disappearing spontaneously, or morphing without external interaction or environmental triggers. Existing evaluation metrics fail to sufficiently capture this physical alignment due to their systemic bias toward surface-level perceptual fidelity. Furthermore, while VLMs can offer coarse feedback on consistency, they are prone to hallucinations that compromise evaluation reliability. Consequently, physical violations persist as a core vulnerability of SOTA video models, underscoring the urgent need for benchmarks that directly assess physically grounded video generation. Promising directions include video understanding methods that track cross-frame agent and object dynamics to systematically quantify physical anomalies, thereby providing the granular feedback necessary to guide the development of next-generation, physically consistent world models. This architectural progress will, in turn, accelerate the deployment of video models as high-fidelity data generators, robust predictors of policy success, and trustworthy visual planners. 

**Temporal Consistency.** Maintaining temporal coherence remains a formidable challenge for video models, particularly during the long-horizon generation tasks crucial for robotic control. Although traditional visual fidelity metrics, such as SSIM and PSNR, offer coarse indicators of temporal consistency, their efficacy is strictly bounded to scenarios characterized by low per-frame pixel velocities. Conversely, robotics applications demand high-fidelity kinematic alignment across frames to support precise closed-loop control in visual planning and fine-grained policy rollouts. Current evaluation suites fail to probe temporal consistency at this granular level. For instance, existing frameworks typically measure temporal quality via optical flow or cross-frame feature similarity using learned encoders like DINO or CLIP, which operate at a semantic granularity too coarse to isolate fine-grained temporal artifacts. These limitations necessitate the design of more expressive benchmarks to systematically track and accelerate research progress. 

**Semantic Consistency.** Video models occasionally generate content that is misaligned with the input prompt—a drawback that is particularly pronounced in image-and-text-conditioned generation. This semantic misalignment is highly consequential in data augmentation and visual planning, where the synthesized rollouts are treated as ground-truth data for training policies or for direct execution. Such discrepancies compromise safety and risk catastrophic real-world failures, underscoring the critical nature of this evaluation axis. Current verification methods primarily rely on CLIP to assess text-to-video semantic consistency; however, CLIP’s underlying contrastive framework effectively behaves as a bag-of-words model, rendering it insensitive to complex syntactic relationships and spatial compositionality in rich generation tasks. While VLMs offer finer-grained semantic probing, their propensity to hallucinate compromises their reliability in automated evaluation pipelines. Promising alternatives include task-understanding frameworks that explicitly verify the logical alignment between user-specified conditioning inputs and downstream video outputs. 

# **5 Open Challenges and Future Directions** 

We identify open research challenges in robotics applications of video models and highlight directions for future research to address these challenges. We note that solutions to these challenges apply broadly beyond robotics, which could motivate novel applications of video models. 

## **5.1 Hallucinations and Violations of Physics** 

Despite their impressive capabilities, video models often hallucinate, generating implausible video frames that are temporally inconsistent or misaligned with physical reality. In T2V generation, recent works [46, 247, 248] have explored different types of hallucinations, including vanishing subject, omission error, numeric variability, visual incongruity, and subject dysmorphia [247], and have proposed hallucination detectors. In robotics, the challenge of hallucination is especially important, given the critical role of accurate future prediction in policy evaluation and visual planning, among other application areas. Recent works have found that using multi-view frame inputs and particularly including a wrist camera view reduces hallucinations [17]. However, augmented conditioning inputs have limited effect on mitigating the violation of physics. Specifically, video models typically fail to follow the laws of physics governing object motion and interactions [108, 111]. Prior work [43, 44, 48] has demonstrated that generated videos from these models violate fundamental principles, such as Newton’s law of motion, conservation of energy and mass, and gravitational effects, revealing a lack of 

16 

understanding of these laws. Further, these models tend to mimic the closest training example when presented with a task at inference, limiting their generalization to new (unseen) tasks. In this setting, video models exhibit a propensity to prioritize transferring the color, size, velocity, and shape of objects in the training dataset to the objects in the new task, in that particular order [43, 109]. 

Further, existing work [44, 45] shows that video models struggle with generating physically-realistic solid-solid interactions, demonstrating that video models do not understand the material properties of objects, the law of conservation of momentum, and the impenetrability of objects. Video models also show a fundamental lack of understanding of fluid mechanics and conservation of mass [43], generating unrealistic videos of liquid flows, e.g., pouring a drink into a cup without a corresponding change in the volume of liquid in the cup. However, generating physically realistic data is crucial in robotics, such as in robot learning where the generated data serves as expert demonstrations for training a policy, highlighting the need to impart physical understanding to video models. Moreover, prompt engineering and scaling techniques do not adequately resolve this challenge, suggesting that novel architectures and training techniques are required to address this problem. Next, we discuss potential directions for future research to improve the physical consistency of videos generated by video models. 

**Future Directions.** Physical realism of generated videos from video models is essential in applications requiring trustworthy video generation, such as policy evaluation, planning, and policy learning, underscoring the importance of research on hallucination mitigation. To improve the physical consistency of generated videos, prior work [249–252] has explored integrating physics-based priors and physics-based simulation with video generation. Hamiltonian and Lagrangian approaches [249, 250] train models to predict the dynamics of system based on Hamiltonian or Lagrangian mechanics. By encoding the laws of physics as priors in the training process, the resulting models tend to adhere better to the physical laws. Other methods employ simulation engines to enforce physical laws. For example, PhysGen [251] extracts object segmentation masks and physical properties using VLMs and computes feasible trajectories for the annotated objects using rigid-body dynamics equations. Subsequently, the trajectories are applied to corresponding pixels for video generation. However, the resulting video often contains artifacts, which degrades its fidelity. PhysGen uses a video diffusion model to edit these artifacts to generate higher-quality videos [253]. Likewise, WonderPlay [252] constructs a 3D scene representation from the conditioning inputs and estimates the physical properties of objects in the scene using a VLM. The scene and objects’ physical properties are passed into a physics-based simulator, which computes a coarse trajectory conditioned on applied forces. The coarse trajectory from the simulator serve as conditioning inputs for a video model to generate future frames. Other methods [110] have utilized LLMs to refine video models’ input prompts to provide comprehensive descriptions of physical attributes and interactions to improve the physical accuracy of generated videos. Although these methods improve physical alignment, they do not eliminate violations of the laws of physics. Specifically, LLMs/VLMs are prone to hallucinations [254], which limits the effectiveness of the aforementioned methods. Moreover, these methods rely on ad-hoc solutions, negatively impacting their generality and ease of implementation. We believe a promising future direction will be to explore efficient techniques for natively endowing video models with a fundamental understanding of physical laws, which might necessitate the design of novel training techniques and model architectures [255] that enforce physical laws. 

Additionally, improving the ability of video models to understand feasible interaction modes could be critical to mitigating hallucinations. Prior work has explored identifying and localizing functional interaction cues from videos, e.g., how humans interact with objects and environments, which is referred to as affordance-based video understanding [256, 257]. Existing methods [258–261] localize interaction regions in videos and embed these cues into a latent space to predict the evolution of contact regions (hotspots) across future video frames. The resulting affordance maps [262–265] can serve as conditioning (guidance) signals in video synthesis to improve the physical consistency of generated videos. Developing effective strategies for incorporating these signals during video generation is an important area for future work. 

## **5.2 Uncertainty Quantification** 

Uncertainty quantification (UQ) techniques are widely utilized with traditional deep neural networks to examine the trustworthiness of these difficult-to-interpret models. While the rapid development of LLMs has led to increased research in UQ of large generative models to address severe hallucinations (see [266] 

17 

for a review of LLM UQ methods), UQ methods for image and video generation models remain largely underexplored. Meanwhile, extending existing UQ methods to video generation models faces significant challenges due to the complexity of spatial and temporal relationships. For example, generative video modeling fails to satisfy the central assumptions of standard Bayesian UQ methods, such as the assumption of independent, identically distributed samples, given the correlation between frames across multiple timesteps. Additionally, the significant computational cost associated with video generation impedes the application of ensemble-based UQ methods. Importantly, existing video models lack the ability to express or verbalize their confidence. As a result, inference-time UQ methods, e.g., black-box LLM UQ methods, cannot be directly applied to video models. 

**Future Directions.** A few recent works have explored UQ techniques for controllable video generation, including text-conditioned and action-conditioned models. S-QUBED [46] quantifies uncertainty of T2V generation in the semantic space. However, this method only estimates task-level confidence on video generation. On the other hand, _C_<sup>3</sup> [111] trains video models for simultaneous video generation and uncertainty quantification in latent space. Specifically, _C_<sup>3</sup> enables video models to predict the uncertainty associated with each subpatch of the generated video, providing dense confidence estimates spatially and temporally. In general, these methods are only guaranteed to provide calibrated uncertainty estimates within the distribution of the training dataset, limiting their effectiveness in out-of-distribution use-cases. A promising direction for future work will be to explore more cost-effective methods for uncertainty quantification with provable guarantees both within and beyond the training distribution. 

## **5.3 Instruction Following** 

Like early language models [267], text-conditioned video models struggle with following user instructions specified in the input prompts [44, 47], which poses a significant limitation. Although these models are generally trained with guidance for alignment with the conditioning inputs, existing guidance mechanisms do not provide sufficient supervision to produce videos consistent with the input prompt. In general, SOTA video models often fail to complete the specified task due to their inability to extract and transfer the intended action from the conditioning input to the specified actor (agent). Prior work [48] has shown that video models are generally able to correctly generate videos containing the agents stated in the input prompt but only partially follow the specified action and in some cases, completely fail to incorporate the specified action into the generated video. 

Furthermore, video models typically fail to generate high-quality text (annotations) in videos [103], even in videos with otherwise high-fidelity components. This limitation becomes especially conspicuous when the input prompt specifically requests text annotations. Further, camera motion control via input prompts remains a major challenge for video models [103, 245]. Even when asked to generate videos with a static camera viewpoint without panning, video models tend to mimic their training videos, which often contain camera motion, resulting in non-adherence to the input prompt. 

These challenges limit robotics applications in data generation and policy learning, among others. For example, many robot data generation methods operate under the assumption of a static camera position for accurate 3D pose estimation of the robot’s end-effector pose through back-projection. Violation of this assumption results in inaccurate goal poses for tracking, degrading the robot’s task performance. Likewise, failure to generate videos that correctly follow the actions specified by the input prompt leads to training data corruption, limiting the effectiveness of imitation learning, which relies on high-quality (expert) demonstrations. 

**Future Directions.** Recent work [112–114] has explored improving the instruction-following capability of video models through multimodal conditioning. ViMi [112] interleaves language and images into a single instruction prompt, which is passed into a VLM to extract a conditional embedding for video generation. Similarly, Aid [113] uses a VLM to predict the states of future video frames, which are fused with the text instruction to generate a conditional embedding for video synthesis. Other approaches [115, 116] enable fine-grained multimodal user inputs to more strongly guide video models in the generation process. With InteractiveVideo [115], users can control the content of generated videos through image, text, and trajectory prompts, describing the desired motion of different elements of the video scene. Similarly, ATI [116] enables localized control of deformations using keypoints and motion paths. Some other methods [117] have examined 

18 

instruction fine-tuning using preference-based reward models to train video models that are better at following user instructions. The aforementioned approaches generally rely on VLMs or other learned models that are susceptible to hallucinations, limiting their practical effectiveness. To address this challenge, a promising research direction will be to explore intrinsic methods for improving task understanding and instruction following, e.g., through inference-time “reasoning” over the generated video patches and frames, similar to the approach used in reasoning language models [19, 268]. 

## **5.4 Evaluating Video Models** 

As established in Section 4.3, robust evaluation metrics and standardized benchmarks for video world models remain notably deficient. To address these limitations, this section outlines several promising research directions aimed at bridging this methodological gap. 

**Future Directions.** Prior works have developed benchmarks for evaluating video generation in terms of alignment with downstream task performance [47, 106]. However, the environment complexity and visual quality of these benchmarks are fundamentally limited by the simulators. Recent works have explored benchmarking and evaluating T2V generation without ground-truth videos along many axes, such as overall video quality, text-to-video alignment, motion quality, and temporal consistency [103]. To evaluate the quality of video models as embodied world models, WorldModelBench [48] trains a VLM-based judge to assess video models in terms of instruction following, physics adherence, and commonsense. In general, these benchmarks still lack the ability to assess video generation quality in fine-grained robot manipulation tasks. A promising direction for future research will be to explore robotics-centric benchmarks and multi-dimensional metrics for quantitative, efficient, and task-relevant video model evaluation. Further, future research on evaluation pipelines that compare the physical consistency of generated videos based on the corresponding motion in the associated 3D scene reconstructions will be important. 

## **5.5 Safe Content Generation** 

Many video models lack adequate safety guardrails, impeding their integration into many real-world applications. Prior work [52, 53] has demonstrated the propensity of video models to generate unsafe content, containing crime, offensive activities, violence, or misinformation, which could hinder adoption in sensitive applications. Despite the importance of safety, only a few papers [118] have explored methods for improving the safety of video models. Addressing this challenge is essential to driving broader applications in robotics. 

**Future Directions.** Enforcing the safety of video models is particularly challenging, given the broad diversity of unsafe video content. For tractability, prior work has utilized model guardrails to prevent the generation of potentially harmful content. While there is extensive literature on safeguarding LLMs [269], analogous techniques for video generation models are far less developed. Recent work (e.g., SAFEWatch [52]) introduces a mechanism for enforcing user-specified safety policies during video generation. However, these methods are task-specific which limits their amenability to more general applications, underscoring the need for more versatile safety guardrails. Additionally, there is a growing need for safety benchmarks for video models. Existing benchmarks [52, 53] evaluate video models on a limited range of criteria, e.g., crimes, hate content, privacy violations, and abusive content; however, a broader evaluation of safety is required for real-world use-cases in robotics. Developing more effective safety guardrails and introducing more comprehensive safety benchmarks will be critical to improving the overall safety of video models in video synthesis. 

## **5.6 Safe Robot Interaction** 

Beyond safe video synthesis, robots must interact safely with other objects and agents in their environments. Safety in robotics can be broadly classified into two categories: (i) physical safety, which involves avoiding all forms of collisions; and (ii) semantic safety, which involves avoiding situations deemed potentially harmful by common-sense knowledge, such as tossing sharp objects at other agents. These forms of safety have been underexplored in robotics applications of video models. However, the success of many robotics tasks depends significantly on satisfying these safety constraints, e.g., in visual planning. 

19 

**Future Directions.** As embodied world models, video models enable robots to assess the safety of proposed actions without executing these actions in the real-world, which is critical to preserving the safety of robots, other agents, and their environments. To detect safety violations, some existing methods [30] generate video predictions from robot action proposals using video models. Other prior work [74, 270] perform robot safety filtering directly in the latent space of world models to predict failures and preempt their occurrence. Likewise, existing methods [119, 271] quantify uncertainty in the latent space to guard against unseen out-of-distribution (OOD) hazards and other user-specified constraint violations. While these works make notable steps toward safe robot control, they have primarily been limited to Markovian state-based world models. Extending these ideas to the spatiotemporal latent spaces of video world models remains a challenge, constituting a important direction for future research. Moreover, generalization beyond the training distribution remains a core challenge in long-tail or safety-critical scenarios because world models are inherently limited by the distribution of their training data. 

## **5.7 Action Estimation** 

SOTA imitation-learned robot policies require high-quality data [199, 272, 273], which is often expensive to collect in the real-world. Although video generation models can address this challenge, the video generated by these models typically do not contain action-labeled frames, which is essential in learning robot policies. Some methods have explored estimating robot actions from videos; however, these methods [120] typically fail to achieve the high level of accuracy required in imitation learning in fine-grained tasks, hindering the effectiveness of current solutions that integrate video models in policy learning frameworks. We discuss a few limitations of latent action models and inverse-dynamics models, the two main approaches for action estimation from robot videos. 

Latent action models [120, 121] estimate robot actions between a pair of video frames in a (discrete) latent space, defined by a fixed set of action codes (primitives). The expressiveness of the learned latent actions is strongly influenced by the size of the latent codebook. Scaling the size of the latent codebook is challenging in practice due to the significant training instabilities and higher compute cost associated with training latent action models with larger codebooks. Further, latent actions are generally difficult to interpret, which makes data curation and analysis more challenging. Additional real-world data is also required to fine-tune latent action models to predict actions that are compatible with physical robots. Inverse-dynamics models [122, 123] suffer from similar challenges and require lots of training data to sufficiently cover the space of robot actions. Like other imitation-learned models, inverse-dynamics models exhibit limited generalization outside of the training distribution, hindering real-world applications. 

**Future Directions.** For better interpretability, recent work [8] utilizes small latent codebooks, which facilitate mapping each latent action to interpretable conditioning inputs. However, this approach fails to scale to more complex robotics tasks which require larger codebooks to effectively learn latent actions. Exploring model architectures that induce interpretable latent actions, without compromising the expressiveness of the latent action space, will be critical to advancing the adoption of video models in robot policy learning. Likewise, the development of robust training procedures for latent action models will be essential to their generalization in robotics. Additionally, semi-supervised training techniques could enable efficient training of generalizable inverse-dynamics models with only a few human annotations, constituting a promising area for future work. 

## **5.8 Long-Horizon Video Generation** 

To serve as effective world models in robotics tasks, video models must predict sufficiently long future horizons that match the duration of robotic tasks, which are often minutes long. However, SOTA video models are limited to generating videos of only a few seconds in duration. For example, Veo 3.1 [9] generates 8-second long videos while Wan 2.5 [10] generates 10-second long videos. These durations are not long enough for informed decision-making in many robotics problems, such as visual planning. Current video generation pipelines require extending multiple short clips to create longer-duration videos; however, this approach often introduces artifacts that degrade the temporal coherence and physical consistency of the resulting videos. While SOTA video models excel in short-duration video generation tasks, scaling these models to longer horizons for robotics tasks remains an open challenge. 

20 

**Future Directions.** Several architectures attempt to address video consistency over long horizons. Broadly, these methods use frame compression, sampling schedule optimizations, or hierarchical frameworks to enable long video generation. For example, MALT [49] encodes past segments into a compact latent memory vector to facilitate autoregressive generation; however, this approach remains susceptible to error accumulation [274]. FramePack [50] mitigates drift by compressing frame contexts based on importance and establishing early endpoints to anchor the generation process. TTTVideo [125] and LaCT [126] utilize test-time training (TTT) to dynamically encode history into model weights or neural hidden states during inference. However, the quality of the generated videos degrades as video length increases. To improve video fidelity, Long-Context Tuning (LCT) [51] expands the context window to maintain dense attention across multi-shot scenes but is limited by the quadratic cost of self-attention, which imposes a computational ceiling on the maximum generation length. In contrast to these approaches, Mixture of Contexts (MoC) [275] circumvents compressing history entirely by recasting generation as an information retrieval task via a sparse attention routing mechanism. Diffusion Forcing [124] offers an alternative solution by training models to denoise tokens with independent noise levels, enabling variable-horizon generation that empirically improves stability in policy rollouts. On the other hand, NUWA-XL [276] utilizes a hierarchical “diffusion-over-diffusion” structure, where a global model generates sparse keyframes and local models recursively fill the intermediate gaps. Despite these improvements, existing methods still struggle to generate minutes-long videos, impeding the their effectiveness in real-world applications. A promising direction for future work will be to design efficient techniques for extending the context window of video models without a prohibitive increase in computation cost for long-video generation. 

## **5.9 Data Curation Costs** 

High-quality data is essential to training video models that are capable of synthesizing high-fidelity, physicallyconsistent videos across diverse tasks. Beyond video quality, diversity of the training data strongly influences the fidelity of generated videos [127, 134], especially for text-conditioned or action-conditioned video models, which require extensive data coverage for desirable results. Although large volumes of videos exist on the internet, many of these videos lack good visual quality and descriptive text annotations, posing a challenge. Specifically, many existing datasets, such as WebVideo-10M [277] and Panda-70M [128], have focused on scale rather than quality, aggregating tens of millions of videos along with their captions. As a result, these datasets suffer from inaccurate, non-descriptive video captions, blurry videos, and rapid shot changes between temporally-inconsistent clips, which negatively impact training. SOTA methods [10, 11, 127, 134] typically rely on expensive data preprocessing pipelines to identify good-quality video data for training. This pipeline consists of three broad stages: (i) video splitting, (ii) video filtering, and (iii) video annotation. At the video splitting stage, candidate video data is temporally segmented into short continuous clips using classical shot detection tools. Videos that are too short are removed at this stage. The resulting clips are then processed by video filters using metrics that assess the visual quality, text quality, motion smoothness and jitter, among others, often with learned models. Subsequently, many methods [11, 134] utilize VLMs [128, 278, 279] for annotating the processed videos, pairing text descriptions with the video data for supervising video models. The VLMs are typically fine-tuned for higher-quality video captioning. This pipeline typically requires human supervision, increasing data curation costs. 

**Future Directions.** Recent video datasets, e.g., VidGen-1M [129] and OpenVid-1M [130], have explored different pre-processing techniques to filter videos using well-defined quality scores before training. These quality scores evaluate the aesthetics, temporal consistency, motion fidelity, and caption descriptiveness, identifying video clips that are more likely to be natural without unrealistic motion. Although these datasets generally provide higher-quality training data, their relatively small size impedes strong zero-shot generalization. Consequently, many SOTA video models [9–11] utilize proprietary curated datasets with dense annotations by VLMs and humans to ensure high quality control. However, VLMs are prone to hallucinations, and human-annotated data collection is expensive, posing significant challenges in high-fidelity video data collection. Exploring strategies for grounding VLMs to minimize the risk of hallucinations is a promising area for future work. Likewise, developing novel-view synthesis techniques to efficiently scale data collection to new scenes from a small set of high-quality videos will be essential to reducing the costs of data curation. Further, more accurate methods for splitting and filtering videos will be critical to curating highly diverse datasets with good temporal and spatial consistency, e.g., [131]. In robotics, high-fidelity future prediction in both successful and unsuccessful task rollout or demonstrations is essential for video models to serve as good proxies for real-world 

21 

environments. Notably, failure demonstrations are important to train video models that faithfully execute actions output by the policy. Recent studies suggest that incorporating failure data from autonomous policy rollouts is critical for training world models that exhibit action controllability [29, 92, 93]. Without such data, generated videos can exhibit an optimistic bias toward success, e.g., via hallucinations that reposition objects for easier grasping or over-estimate grasp feasibility, which could result in real-world failures [29]. 

## **5.10 Training and Inference Costs** 

SOTA video models require large amounts of compute resources for training and inference. Although the true cost of training video models is often confidential especially for closed-source models, the most cost-effective SOTA open-source video models require hundreds of thousands of dollars to train—e.g., $200k for OpenSora 2.0 [134]. Video models typically have billions of parameters, which is a major contributing factor to their significant training costs. Although latent diffusion [133] reduces the number of parameters required by these models, the corresponding reduction in training costs is often not sufficient. As a result, research on training video models has broadly remained limited to large research groups with deep budgets. Moreover, recent developments such as classifier-free guidance [165, 176] for fine-grained input-conditioning introduce additional computational overhead. Reducing training and inference costs is critical to advancing broader applications of video models in robotics. 

Additionally, high-fidelity video models [7, 9–11] are often limited by significantly slow inference speeds. For example, Veo 3 [9] generates about 12 video frames per second on an NVIDIA A100 GPU. Although sufficient in some use cases, the slow inference time presents an important challenge in many robotics applications, such as visual planning, where closed-loop execution requires real-time feedback to the planner for robustness. Existing video model planners often take a few seconds to generate feasible action trajectories for a single episode [132], which is not fast enough for real-time operation. 

**Future Directions.** For faster training and inference, recent work [31, 134] has explored spatial and temporal compression techniques to reduce the number of costly attention operations during video generation. Dreamer 4 [31] applies temporal attention sparsely to every fourth video frame by decoupling spatial and temporal attention. Similarly, OpenSora uses deep compression autoencoders [280] to downsample input tokens at greater ratios to speed up inference by an order of magnitude. Likewise, Wan [10] employs a feature cache mechanism to enable chunk-based video synthesis while preserving temporal continuity. Some other methods utilize shortcut models [135] for finer control over the number of sampling steps required for video generation without any significant degradation in video quality. Like shortcut models, consistency models [136, 281] enable efficient video diffusion using a single-step denoising process. Other video models utilize more classical speed optimization techniques for faster inference, e.g., quantization [282] and model distillation [283]. Further research on these topics is required to improve inference speeds for real-time applications. 

# **6 Conclusion** 

This survey reviews video models and their applications as embodied world models in robotics, identifying prevailing model architectures, conditioning modalities, and key capabilities of video models. Specifically, we categorize existing robotics applications into four broad classes: robot data generation and action prediction in imitation learning, dynamics and rewards modeling in reinforcement learning, policy evaluation, and visual planning. We emphasize that these applications are underpinned by the remarkable ability of video models to learn fine-grained spatiotemporal relationships that govern the evolution of the state of real-world environments, which is essential for physically consistent future predictions. Furthermore, we identify critical open research challenges and propose directions for future research, seeking to motivate broader applications of video models. 

22 

# **Acknowledgments** 

Asher J. Hancock was supported by the National Science Foundation Graduate Research Fellowship Program under Grant No. DGE-2146755. Apurva Badithela is supported by the Presidential Postdoctoral Research Fellowship at Princeton University. The authors were partially supported by the NSF CAREER Award #2044149, #2107048, the Office of Naval Research (N00014-23-1-2148), the Sloan Fellowship, and Apple Inc. Any views, opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and should not be interpreted as reflecting the views, policies or position, either expressed or implied, of Apple Inc. 

# **References** 

- [1] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. _Advances in neural information processing systems_ , 33:6840–6851, 2020. 2, 4, 6 

- [2] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, and Matt Le. Flow matching for generative modeling, 2023. URL `https://arxiv.org/abs/2210.02747` . 2, 4, 6 

- [3] Xiaowen Li, Haolan Xue, Peiran Ren, and Liefeng Bo. Diffueraser: A diffusion model for video inpainting. _arxiv:2501.10018_ , 2025. 2 

- [4] Kuaishou Technology. Kling AI: Next-generation AI creative studio. `https://ir.kuaishou.com/news-releases/ news-release-details/kling-ai-launches-25-turbo-video-model-industry-leading` , June 2024. 10 

- [5] Runway. Introducing Gen-3 Alpha: A New Frontier for Video Generation. `https://runwayml.com/research/ introducing-gen-3-alpha` , jun 2024. 7 

- [6] Luma Labs. Dream Machine: New Freedoms of Imagination. `https://lumalabs.ai/dream-machine` , June 2024. 

- [7] Tim Brooks et al. Video generation models as world simulators. _OpenAI Blog_ , 1(8):1, 2024. 4, 7, 22 

- [8] Google DeepMind. Genie 3: A New Frontier for World Models. Google DeepMind Blog, aug 2025. URL `https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/` . 4, 8, 20 

- [9] DeepMind. Veo-3: A text-to-video generation system with audio. Technical Report Tech Report, DeepMind / Google, 2025. 4, 7, 20, 21, 22 

- [10] Team Wan. Wan: Open and advanced large-scale video generative models. _arxiv:2503.20314_ , 2025. 4, 6, 7, 9, 10, 12, 13, 14, 20, 21, 22 

- [11] Niket Agarwal et al. Cosmos world foundation model platform for physical ai. _arXiv:2501.03575_ , 2025. 2, 4, 6, 7, 10, 12, 21, 22 

- [12] Joel Jang et al. Dreamgen: Unlocking generalization in robot learning through video world models. _arxiv:2505.12705_ , 2025. 2, 4, 9, 10, 14 

- [13] Hongyu Li, Lingfeng Sun, Yafei Hu, Duy Ta, Jennifer Barry, George Konidaris, and Jiahui Fu. Novaflow: Zero-shot manipulation via actionable flow from generated videos. _arxiv:2510.08568_ , 2025. 4, 13, 14 

- [14] Yilun Du, Mengjiao Yang, Pete Florence, Fei Xia, Ayzaan Wahid, Brian Ichter, Pierre Sermanet, Tianhe Yu, Pieter Abbeel, Joshua B. Tenenbaum, Leslie Kaelbling, Andy Zeng, and Jonathan Tompson. Video language planning, 2023. URL `https://arxiv.org/abs/2310.10625` . 2, 4, 13 

- [15] Chongkai Gao, Haozhuo Zhang, Zhixuan Xu, Zhehao Cai, and Lin Shao. Flip: Flow-centric generative planning as general-purpose manipulation world model. _arxiv:2412.08261_ , 2024. 2, 4, 13 

- [16] Julian Quevedo, Ansh Kumar Sharma, Yixiang Sun, Varad Suryavanshi, Percy Liang, and Sherry Yang. Worldgym: World model as an environment for policy evaluation, 2025. URL `https://arxiv.org/abs/2506.00613` . 2, 4, 7, 12, 13 

- [17] Yanjiang Guo, Lucy Xiaoyang Shi, Jianyu Chen, and Chelsea Finn. Ctrl-world: A controllable generative world model for robot manipulation. _arxiv:2510.10125_ , 2025. 2, 4, 7, 12, 15, 16 

- [18] Thadd¨aus Wiedemer et al. Video models are zero-shot learners and reasoners, 2025. URL `https://arxiv.org/ abs/2509.20328` . 2 

23 

- [19] DeepSeek-AI. DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, 2025. 2, 19 

- [20] OpenAI. GPT-5 and the new era of work. `https://openai.com/index/gpt-5-new-era-of-work/` , August 2025. 

- [21] Demis Hassabis, Koray Kavukcuoglu, and on behalf of the Gemini team. A new era of intelligence with Gemini 3. `https://blog.google/products/gemini/gemini-3/` , nov 2025. Blog Post. 2 

- [22] Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Conference on Robot Learning_ , pages 2165–2183. PMLR, 2023. 2 

- [23] Physical Intelligence. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arxiv:2504.16054_ , 2025. 2, 9 

- [24] Gemini Robotics Team. Gemini robotics: Bringing ai into the physical world. _arxiv:2503.20020_ , 2025. 2, 9 

- [25] Siqiao Huang, Jialong Wu, Qixing Zhou, Shangchen Miao, and Mingsheng Long. Vid2world: Crafting video diffusion models to interactive world models. _arxiv:2505.14357_ , 2025. 2, 8, 9 

- [26] Siyuan Huang et al. Enerverse: Envisioning embodied future space for robotics manipulation. _arxiv:2501.01895_ , 2025. 8, 9, 12 

- [27] Yue Liao et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arxiv:2508.05635_ , 2025. 9 

- [28] Jake Bruce et al. Genie: Generative interactive environments. In _Forty-first International Conference on Machine Learning_ , 2024. 2, 6 

- [29] 1X World Model Team. 1x world model: Evaluating bits, not atoms. Technical report, 1X, 2025. 2, 4, 12, 13, 22 

- [30] Gemini Robotics Team. Evaluating Gemini robotics policies in a veo world simulator, 2025. URL `https: //arxiv.org/abs/2512.10675` . 2, 4, 7, 12, 13, 20 

- [31] Danijar Hafner, Wilson Yan, and Timothy Lillicrap. Training agents inside of scalable world models. _arxiv:2509.24527_ , 2025. 2, 4, 11, 12, 22 

- [32] Junjin Xiao, Yandan Yang, Xinyuan Chang, Ronghan Chen, Feng Xiong, Mu Xu, Wei-Shi Zheng, and Qing Zhang. World-env: Leveraging world model as a virtual environment for vla post-training. _arxiv:2509.24948_ , 2025. 4, 11, 12 

- [33] Alejandro Escontrela et al. Video prediction models as rewards for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:68760–68783, 2023. 4, 11, 12 

- [34] Tao Huang, Guangqi Jiang, Yanjie Ze, and Huazhe Xu. Diffusion reward: Learning rewards via conditional video diffusion. In _European Conference on Computer Vision_ , pages 478–495. Springer, 2024. 2, 4, 11, 12 

- [35] Generalist AI. GEN-0 / Embodied Foundation Models That Scale with Physical Interaction. `https:// generalistai.com/blog/nov-04-2025-GEN-0` , November 2025. 2 

- [36] Anurag Ajay et al. Compositional foundation models for hierarchical planning. _Advances in Neural Information Processing Systems_ , 36:22304–22325, 2023. 2, 9 

- [37] Zhengtong Xu, Qiang Qiu, and Yu She. Vilp: Imitation learning with latent video planning. _IEEE Robotics and Automation Letters_ , 2025. 9 

- [38] Po-Chen Ko et al. Learning to act from actionless videos through dense correspondences. _arxiv:2310.08576_ , 2023. 2, 10 

- [39] Frederik Ebert, Chelsea Finn, Sudeep Dasari, Annie Xie, Alex Lee, and Sergey Levine. Visual foresight: Model-based deep reinforcement learning for vision-based robotic control. _arxiv:1812.00568_ , 2018. 2, 4, 13 

- [40] Qingwen Bu et al. Closed-loop visuomotor control with generative expectation for robotic manipulation. _Advances in Neural Information Processing Systems_ , 37:139002–139029, 2024. 4, 13 

- [41] Boyuan Chen, Tianyuan Zhang, Haoran Geng, Kiwhan Song, Caiyi Zhang, Peihao Li, William T. Freeman, Jitendra Malik, Pieter Abbeel, Russ Tedrake, Vincent Sitzmann, and Yilun Du. Large video planner enables generalizable robot control, 2025. URL `https://arxiv.org/abs/2512.15840` . 10 

24 

- [42] Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond vlas, 2025. URL `https://arxiv.org/abs/2512.15692` . 2, 10 

- [43] Saman Motamed, Laura Culp, Kevin Swersky, Priyank Jaini, and Robert Geirhos. Do generative video models understand physical principles?, 2025. URL `https://arxiv.org/abs/2501.09038` . 2, 4, 15, 16, 17 

- [44] Hritik Bansal, Zongyu Lin, Tianyi Xie, Zeshun Zong, Michal Yarom, Yonatan Bitton, Chenfanfu Jiang, Yizhou Sun, Kai-Wei Chang, and Aditya Grover. Videophy: Evaluating physical commonsense for video generation. _arxiv:2406.03520_ , 2024. 4, 14, 15, 16, 17, 18 

- [45] Fanqing Meng et al. Towards world simulator: Crafting physical commonsense-based benchmark for video generation. _arxiv:2410.05363_ , 2024. 4, 15, 17 

- [46] Zhiting Mei, Ola Shorinwa, and Anirudha Majumdar. How confident are video models? Empowering video models to express their uncertainty. _arxiv:2510.02571_ , 2025. 2, 4, 16, 18 

- [47] Yiran Qin et al. Worldsimbench: Towards video generation models as world simulators. _arxiv:2410.18072_ , 2024. 2, 4, 15, 18, 19 

- [48] Dacheng Li et al. Worldmodelbench: Judging video generation models as world models. _arxiv:2502.20694_ , 2025. 2, 4, 14, 15, 16, 18, 19 

- [49] Sihyun Yu, Meera Hahn, Dan Kondratyuk, Jinwoo Shin, Agrim Gupta, Jos´e Lezama, Irfan Essa, David Ross, and Jonathan Huang. Malt diffusion: Memory-augmented latent transformers for any-length video generation. _arxiv:2502.12632_ , 2025. 2, 4, 21 

- [50] Lvmin Zhang and Maneesh Agrawala. Packing input frame context in next-frame prediction models for video generation. _arxiv:2504.12626_ , 2025. 4, 21 

- [51] Yuwei Guo, Ceyuan Yang, Ziyan Yang, Zhibei Ma, Zhijie Lin, Zhenheng Yang, Dahua Lin, and Lu Jiang. Long context tuning for video generation. _arxiv:2503.10589_ , 2025. 2, 4, 21 

- [52] Zhaorun Chen, Francesco Pinto, Minzhou Pan, and Bo Li. Safewatch: An efficient safety-policy following video guardrail model with transparent explanations, 2024. URL `https://arxiv.org/abs/2412.06878` . 2, 4, 15, 19 

- [53] Yibo Miao, Yifan Zhu, Yinpeng Dong, Lijia Yu, Jun Zhu, and Xiao-Shan Gao. T2vsafetybench: Evaluating the safety of text-to-video generative models, 2024. URL `https://arxiv.org/abs/2407.05965` . 2, 4, 15, 19 

- [54] Andrew Melnik, Michal Ljubljanac, Cong Lu, Qi Yan, Weiming Ren, and Helge Ritter. Video diffusion models: A survey. _arxiv:2405.03150_ , 2024. 3 

- [55] Jiwen Yu, Yiran Qin, Haoxuan Che, Quande Liu, Xintao Wang, Pengfei Wan, Di Zhang, Kun Gai, Hao Chen, and Xihui Liu. A survey of interactive generative video. _arxiv:2504.21853_ , 2025. 3 

- [56] Yue Ma et al. Controllable video generation: A survey. _arxiv:2507.16869_ , 2025. 3 

- [57] Zhen Xing, Qijun Feng, Haoran Chen, Qi Dai, Han Hu, Hang Xu, Zuxuan Wu, and Yu-Gang Jiang. A survey on video diffusion models. _ACM Computing Surveys_ , 57(2):1–42, 2024. 3 

- [58] Xinqing Li, Xin He, Le Zhang, and Yun Liu. A comprehensive survey on world models for embodied ai. _arxiv:2510.16732_ , 2025. 3, 5 

- [59] Jingtao Ding et al. Understanding world or predicting future? a comprehensive survey of world models. _ACM Computing Surveys_ , 58(3):1–38, 2025. 

- [60] Lingdong Kong, Wesley Yang, Jianbiao Mei, Youquan Liu, Ao Liang, Dekai Zhu, Dongyue Lu, Wei Yin, Xiaotao Hu, Mingkai Jia, et al. 3d and 4d world modeling: A survey. _arxiv:2509.07996_ , 2025. 

- [61] Kun Zhang et al. Generative artificial intelligence in robotic manipulation: A survey. _arxiv:2503.03464_ , 2025. 3 

- [62] Sherry Yang, Jacob Walker, Jack Parker-Holder, Yilun Du, Jake Bruce, Andre Barreto, Pieter Abbeel, and Dale Schuurmans. Video as the new language for real-world decision making, 2024. URL `https://arxiv.org/abs/ 2402.17139` . 3 

- [63] Jingtong Yue, Ziqi Huang, Zhaoxi Chen, Xintao Wang, Pengfei Wan, and Ziwei Liu. Simulating the visual world with artificial intelligence: A roadmap, 2025. URL `https://arxiv.org/abs/2511.08585` . 3 

- [64] Zheng Zhu et al. Is sora a world simulator? a comprehensive survey on general world models and beyond. _arxiv:2405.03520_ , 2024. 3 

25 

- [65] Yanchen Guan et al. World models for autonomous driving: An initial survey. _IEEE Transactions on Intelligent Vehicles_ , 2024. 

- [66] Tuo Feng, Wenguan Wang, and Yi Yang. A survey of world models for autonomous driving. _arxiv:2501.11260_ , 2025. 

- [67] Yingyan Li, Shuyao Shang, Weisong Liu, Bing Zhan, Haochen Wang, Yuqi Wang, Yuntao Chen, Xiaoman Wang, Yasong An, Chufeng Tang, et al. Drivevla-w0: World models amplify data scaling law in autonomous driving. _arxiv:2510.12796_ , 2025. 3 

- [68] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arxiv:2301.04104_ , 2023. 4, 5 

- [69] Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arxiv:2310.16828_ , 2023. 4, 5, 8 

- [70] Gaoyue Zhou, Hengkai Pan, Yann LeCun, and Lerrel Pinto. Dino-wm: World models on pre-trained visual features enable zero-shot planning. _arxiv:2411.04983_ , 2024. 4, 5 

- [71] Carl Vondrick et al. Generating videos with scene dynamics. _Advances in neural information processing systems_ , 29, 2016. 4, 5 

- [72] Mohammad Babaeizadeh, Chelsea Finn, Dumitru Erhan, Roy H Campbell, and Sergey Levine. Stochastic variational video prediction. _arXiv:1710.11252_ , 2017. 4, 6 

- [73] Jialong Wu et al. ivideogpt: Interactive videogpts are scalable world models. _Advances in Neural Information Processing Systems_ , 37:68082–68119, 2024. 4, 6 

- [74] Kensuke Nakamura, Lasse Peters, and Andrea Bajcsy. Generalizing safety beyond collision-avoidance via latent-space reachability analysis, 2025. URL `https://arxiv.org/abs/2502.00935` . 4, 5, 20 

- [75] Tenny Yin et al. Womap: World models for embodied open-vocabulary object localization. In _RSS 2025 Workshop: Mobile Manipulation_ , 2025. 4, 5 

- [76] Jonathan Ho et al. Video diffusion models. _Advances in neural information processing systems_ , 35:8633–8646, 2022. 4, 6, 7 

- [77] Andreas Blattmann et al. Stable video diffusion: Scaling latent video diffusion models to large datasets, 2023. URL `https://arxiv.org/abs/2311.15127` . 4, 7, 10, 12 

- [78] Mahmoud Assran et al. Self-supervised learning from images with a joint-embedding predictive architecture. In _Proc. of the IEEE/CVF CVPR_ , pages 15619–15629, 2023. 4, 7 

- [79] Adrien Bardes et al. Revisiting feature prediction for learning visual representations from video. _arxiv:2404.08471_ , 2024. 4, 7 

- [80] Quentin Garrido, Nicolas Ballas, Mahmoud Assran, Adrien Bardes, Laurent Najman, Michael Rabbat, Emmanuel Dupoux, and Yann LeCun. Intuitive physics understanding emerges from self-supervised pretraining on natural videos, 2025. URL `https://arxiv.org/abs/2502.11831` . 4, 7 

- [81] Mido Assran et al. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv:2506.09985_ , 2025. 4, 7, 8 

- [82] Shivansh Patel, Shraddhaa Mohan, Hanlin Mai, Unnat Jain, Svetlana Lazebnik, and Yunzhu Li. Robotic manipulation by imitating generated videos without physical demonstrations. _arxiv:2507.00990_ , 2025. 4, 10 

- [83] Xiaowen Qiu et al. Lucibot: Automated robot policy learning from generated videos. _arxiv:2503.09871_ , 2025. 4, 9, 10 

- [84] Homanga Bharadhwaj et al. Gen2act: Human video generation in novel scenarios enables generalizable robot manipulation. _arxiv:2409.16283_ , 2024. 4, 10 

- [85] Achint Soni, Sreyas Venkataraman, Abhranil Chandra, Sebastian Fischmeister, Percy Liang, Bo Dai, and Sherry Yang. Videoagent: Self-improving video generation. _arxiv:2410.10076_ , 2024. 4, 10 

- [86] Junbang Liang et al. Dreamitate: Real-world visuomotor policy learning via video generation. _arxiv:2406.16862_ , 2024. 4, 10 

- [87] Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arxiv:2503.00200_ , 2025. 4, 10 

26 

- [88] Wenyao Zhang et al. Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge. _arxiv:2507.04447_ , 2025. 4, 5, 10 

- [89] Yuxin Jiang et al. Enerverse-ac: Envisioning embodied environments with action condition. _arxiv:2505.09723_ , 2025. 4 

- [90] Yunhao Luo and Yilun Du. Grounding video models to actions through goal conditioned exploration. _arxiv:2411.07223_ , 2024. 4, 11, 12 

- [91] Yaxuan Li, Yichen Zhu, Junjie Wen, Chaomin Shen, and Yi Xu. Worldeval: World model as real-world robot policies evaluator. _arxiv:2505.19017_ , 2025. 4, 12 

- [92] Fangqi Zhu, Hongtao Wu, Song Guo, Yuxiao Liu, Chilam Cheang, and Tao Kong. Irasim: Learning interactive real-robot action simulators. _arxiv:2406.14540_ , 2024. 4, 12, 13, 22 

- [93] Wei-Cheng Tseng, Jinwei Gu, Qinsheng Zhang, Hanzi Mao, Ming-Yu Liu, Florian Shkurti, and Lin Yen-Chen. Scalable policy evaluation with video world models. _arxiv:2511.11520_ , 2025. 4, 12, 13, 22 

- [94] Yuncong Yang et al. Mindjourney: Test-time scaling with world models for spatial reasoning. _arxiv:2507.12508_ , 2025. 4, 13 

- [95] Jun Cen, Chenfei Wu, Xiao Liu, Shengming Yin, Yixuan Pei, Jinglong Yang, Qifeng Chen, Nan Duan, and Jianguo Zhang. Using left and right brains together: Towards vision and language planning. _arxiv:2402.10534_ , 2024. 4, 13 

- [96] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-shot robotic manipulation with pretrained image-editing diffusion models. _arxiv:2310.10639_ , 2023. 4, 13 

- [97] Alain Hor´e and Djemel Ziou. Image quality metrics: Psnr vs. ssim. In _2010 20th International Conference on Pattern Recognition_ , pages 2366–2369, 2010. 4, 14, 15 

- [98] Zhou Wang, Alan C Bovik, Hamid R Sheikh, and Eero P Simoncelli. Image quality assessment: from error visibility to structural similarity. _IEEE transactions on image processing_ , 13(4):600–612, 2004. 4, 14, 15 

- [99] Richard Zhang, Phillip Isola, et al. The unreasonable effectiveness of deep features as a perceptual metric. In _Proc. of the IEEE conference on computer vision and pattern recognition_ , pages 586–595, 2018. 4, 14 

- [100] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pages 8748–8763. PmLR, 2021. 4, 14, 15 

- [101] Thomas Unterthiner, Sjoerd Van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, and Sylvain Gelly. Towards accurate generative models of video: A new metric & challenges. _arxiv:1812.01717_ , 2018. 4, 14 

- [102] James J Gibson. The perception of the visual world. _The American Journal of Psychology_ , 64(3):440, 1951. 4, 14 

- [103] Yaofang Liu et al. Evalcrafter: Benchmarking and evaluating large video generation models. In _Proc. of the IEEE/CVF Conference on CVPR_ , pages 22139–22149, 2024. 4, 15, 18, 19 

- [104] Ziqi Huang, Yinan He, Jiashuo Yu, et al. Vbench: Comprehensive benchmark suite for video generative models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 21807–21818, 2024. 4, 15 

- [105] Kaiyue Sun, Kaiyi Huang, Xian Liu, Yue Wu, Zihan Xu, Zhenguo Li, and Xihui Liu. T2v-compbench: A comprehensive benchmark for compositional text-to-video generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 8406–8416, 2025. 4, 15 

- [106] Stephen Tian, Chelsea Finn, and Jiajun Wu. A control-centric benchmark for video prediction. _arxiv:2304.13723_ , 2023. 4, 15, 19 

- [107] Boyang Wang et al. This&that: Language-gesture controlled video generation for robot planning. In _2025 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 12842–12849. IEEE, 2025. 4, 9, 15 

- [108] Minghui Lin, Xiang Wang, Yishan Wang, Shu Wang, Fengqi Dai, Pengxiang Ding, Cunxiang Wang, Zhengrong Zuo, Nong Sang, Siteng Huang, et al. Exploring the evolution of physics cognition in video generation: A survey. _arxiv:2503.21765_ , 2025. 4, 16 

27 

- [109] Bingyi Kang, Yang Yue, Rui Lu, Zhijie Lin, Yang Zhao, Kaixin Wang, Gao Huang, and Jiashi Feng. How far is video generation from world model: A physical law perspective. _arxiv:2411.02385_ , 2024. 4, 15, 17 

- [110] Ke Zhang, Cihan Xiao, Yiqun Mei, Jiacong Xu, and Vishal M. Patel. Think before you diffuse: Llms-guided physics-aware video generation, 2025. URL `https://arxiv.org/abs/2505.21653` . 4, 17 

- [111] Zhiting Mei, Tenny Yin, Micah Baker, Ola Shorinwa, and Anirudha Majumdar. World models that know when they don’t know: Controllable video generation with calibrated uncertainty. _arxiv:2512.05927_ , 2025. 4, 16, 18 

- [112] Yuwei Fang, Willi Menapace, Aliaksandr Siarohin, Tsai-Shien Chen, Kuan-Chieh Wang, Ivan Skorokhodov, Graham Neubig, and Sergey Tulyakov. Vimi: Grounding video generation through multi-modal instruction. In _Proc. of the 2024 Conference on Empirical Methods in NLP_ , pages 4444–4456, 2024. 4, 18 

- [113] Zhen Xing, Qi Dai, Zejia Weng, Zuxuan Wu, and Yu-Gang Jiang. Aid: Adapting image2video diffusion models for instruction-guided video prediction. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 21243–21253, 2025. 4, 18 

- [114] Jialu Li, Shoubin Yu, Han Lin, Jaemin Cho, Jaehong Yoon, and Mohit Bansal. Training-free guidance in text-to-video generation via multimodal planning and structured noise initialization, 2025. URL `https: //arxiv.org/abs/2504.08641` . 4, 18 

- [115] Yiyuan Zhang, Yuhao Kang, Zhixin Zhang, Xiaohan Ding, Sanyuan Zhao, and Xiangyu Yue. Interactivevideo: User-centric controllable video generation with synergistic multimodal instructions, 2024. URL `https://arxiv. org/abs/2402.03040` . 4, 18 

- [116] Angtian Wang, Haibin Huang, Jacob Zhiyuan Fang, Yiding Yang, and Chongyang Ma. Ati: Any trajectory instruction for controllable video generation, 2025. URL `https://arxiv.org/abs/2505.22944` . 4, 18 

- [117] Hangjie Yuan, Shiwei Zhang, Xiang Wang, Yujie Wei, Tao Feng, Yining Pan, Yingya Zhang, Ziwei Liu, Samuel Albanie, and Dong Ni. Instructvideo: Instructing video diffusion models with human feedback. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 6463–6474, 2024. 4, 18 

- [118] Jaehong Yoon, Shoubin Yu, Vaidehi Patil, Huaxiu Yao, and Mohit Bansal. Safree: Training-free and adaptive guard for safe text-to-image and video generation, 2025. URL `https://arxiv.org/abs/2410.12761` . 4, 19 

- [119] Junwon Seo, Kensuke Nakamura, and Andrea Bajcsy. Uncertainty-aware latent safety filters for avoiding out-of-distribution failures, 2025. URL `https://arxiv.org/abs/2505.00779` . 4, 20 

- [120] Seonghyeon Ye et al. Latent action pretraining from videos. In _The Thirteenth International Conference on Learning Representations_ , 2024. 4, 10, 20 

- [121] Xiaoyu Chen et al. Villa-x: enhancing latent action modeling in vision-language-action models. _arxiv:2507.23682_ , 2025. 4, 10, 20 

- [122] Deepak Pathak, Parsa Mahmoudieh, Guanghao Luo, Pulkit Agrawal, Dian Chen, Yide Shentu, Evan Shelhamer, Jitendra Malik, Alexei A Efros, and Trevor Darrell. Zero-shot visual imitation. In _Proceedings of the IEEE conference on computer vision and pattern recognition workshops_ , pages 2050–2053, 2018. 4, 10, 20 

- [123] Hengkai Tan, Yao Feng, Xinyi Mao, Shuhe Huang, Guodong Liu, Zhongkai Hao, Hang Su, and Jun Zhu. Anypos: Automated task-agnostic actions for bimanual manipulation. _arxiv:2507.12768_ , 2025. 4, 10, 20 

- [124] Boyuan Chen et al. Diffusion forcing: Next-token prediction meets full-sequence diffusion. In _Advances in Neural Information Processing Systems_ , volume 37, pages 24081–24125. Curran Associates, Inc., 2024. 4, 9, 21 

- [125] Karan Dalal, Daniel Koceja, Jiarui Xu, Yue Zhao, Shihao Han, Ka Chun Cheung, Jan Kautz, Yejin Choi, Yu Sun, and Xiaolong Wang. One-minute video generation with test-time training. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 17702–17711, 2025. 4, 21 

- [126] Tianyuan Zhang, Sai Bi, Yicong Hong, Kai Zhang, Fujun Luan, Songlin Yang, Kalyan Sunkavalli, William T Freeman, and Hao Tan. Test-time training done right. _arxiv:2505.23884_ , 2025. 4, 21 

- [127] Zhuoyi Yang et al. Cogvideox: Text-to-video diffusion models with an expert transformer. _arxiv:2408.06072_ , 2024. 4, 21 

- [128] Tsai-Shien Chen et al. Panda-70m: Captioning 70m videos with multiple cross-modality teachers. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13320–13331, 2024. 4, 21 

- [129] Zhiyu Tan, Xiaomeng Yang, Luozheng Qin, and Hao Li. Vidgen-1m: A large-scale dataset for text-to-video generation. _arxiv:2408.02629_ , 2024. 4, 21 

28 

- [130] Kepan Nan, Rui Xie, Penghao Zhou, Tiehan Fan, Zhenheng Yang, Zhijie Chen, Xiang Li, Jian Yang, and Ying Tai. Openvid-1m: A large-scale high-quality dataset for text-to-video generation. _arxiv:2407.02371_ , 2024. 4, 21 

- [131] Qiuheng Wang, Yukai Shi, Jiarong Ou, Rui Chen, Ke Lin, Jiahao Wang, Boyuan Jiang, Haotian Yang, Mingwu Zheng, Xin Tao, et al. Koala-36m: A large-scale video dataset improving consistency between fine-grained conditions and video content. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 8428–8437, 2025. 4, 21 

- [132] Po-Chen Ko, Jiayuan Mao, Yu-Hsiang Fu, Hsien-Jeng Yeh, Chu-Rong Chen, Wei-Chiu Ma, Yilun Du, and Shao-Hua Sun. Implicit state estimation via video replanning, 2025. URL `https://arxiv.org/abs/2510.17315` . 4, 22 

- [133] Andreas Blattmann et al. Align your latents: High-resolution video synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 22563–22575, 2023. 4, 7, 22 

- [134] Xiangyu Peng et al. Open-sora 2.0: Training a commercial-level video generation model in 200 k. _arxiv:2503.09642_ , 2025. 4, 21, 22 

- [135] Kevin Frans, Danijar Hafner, Sergey Levine, and Pieter Abbeel. One step diffusion via shortcut models. _arXiv:2410.12557_ , 2024. 4, 22 

- [136] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever. Consistency models. In _International Conference on Machine Learning_ , pages 32211–32252. PMLR, 2023. 4, 22 

- [137] Aravind Rajeswaran, Vikash Kumar, Abhishek Gupta, Giulia Vezzani, John Schulman, Emanuel Todorov, and Sergey Levine. Learning complex dexterous manipulation with deep reinforcement learning and demonstrations. _arxiv:1709.10087_ , 2017. 5 

- [138] Jan Matas, Stephen James, and Andrew J Davison. Sim-to-real reinforcement learning for deformable object manipulation. In _Conference on Robot Learning_ , pages 734–743. PMLR, 2018. 5 

- [139] Emanuel Todorov, Tom Erez, and Yuval Tassa. Mujoco: A physics engine for model-based control. In _2012 IEEE/RSJ international conference on intelligent robots and systems_ , pages 5026–5033. IEEE, 2012. 5 

- [140] Erwin Coumans and Yunfei Bai. Pybullet, a python module for physics simulation for games, robotics and machine learning, 2016. 5 

- [141] David Ha and J¨urgen Schmidhuber. Recurrent world models facilitate policy evolution. _Advances in neural information processing systems_ , 31, 2018. 5 

- [142] David Ha and J¨urgen Schmidhuber. World models. _arxiv:1803.10122_ , 2(3), 2018. 5 

- [143] Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination, 2020. URL `https://arxiv.org/abs/1912.01603` . 5, 8 

- [144] Danijar Hafner, Timothy Lillicrap, Mohammad Norouzi, and Jimmy Ba. Mastering atari with discrete world models. _arxiv:2010.02193_ , 2020. 

- [145] Russell Mendonca, Shikhar Bahl, and Deepak Pathak. Structured world models from human videos. _arxiv:2308.10901_ , 2023. 

- [146] Jialong Wu, Haoyu Ma, Chaoyi Deng, and Mingsheng Long. Pre-training contextualized world models with inthe-wild videos for reinforcement learning. _Advances in Neural Information Processing Systems_ , 36:39719–39743, 2023. 5 

- [147] Eloi Alonso et al. Diffusion for world modeling: Visual details matter in atari. _Advances in Neural Information Processing Systems_ , 37:58757–58791, 2024. 5 

- [148] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning interactive real-world simulators. _arxiv:2310.06114_ , 1(2):6, 2023. 

- [149] Zihan Ding, Amy Zhang, Yuandong Tian, and Qinqing Zheng. Diffusion world model: Future modeling beyond step-by-step rollout for offline reinforcement learning. _arxiv:2402.03570_ , 2024. 5 

- [150] Yuhang Huang, Jiazhao Zhang, Shilong Zou, XInwang Liu, Ruizhen Hu, and Kai Xu. Ladi-wm: A latent diffusion-based world model for predictive manipulation. _arxiv:2505.11528_ , 2025. 5 

29 

- [151] Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 15791–15801, 2025. 5 

- [152] Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg. Daydreamer: World models for physical robot learning. In _Conference on robot learning_ , pages 2226–2240. PMLR, 2023. 5 

- [153] Akshay L Chandra, Iman Nematollahi, Chenguang Huang, Tim Welschehold, Wolfram Burgard, and Abhinav Valada. Diwa: Diffusion policy adaptation with world models. _arxiv:2508.03645_ , 2025. 5 

- [154] Chelsea Finn, Ian Goodfellow, and Sergey Levine. Unsupervised learning for physical interaction through video prediction. _Advances in neural information processing systems_ , 29, 2016. 5, 9 

- [155] Xu Jia, Bert De Brabandere, Tinne Tuytelaars, and Luc V Gool. Dynamic filter networks. _Neural information processing systems_ , 29, 2016. 5 

- [156] Aidan Clark, Jeff Donahue, and Karen Simonyan. Adversarial video generation on complex datasets. _arxiv:1907.06571_ , 2019. 5 

- [157] Ian J Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial nets. _Advances in neural information processing systems_ , 27, 2014. 6 

- [158] Alex X Lee et al. Stochastic adversarial video prediction. _arxiv:1804.01523_ , 2018. 6 

- [159] Jacob Walker, Ali Razavi, and A¨aron van den Oord. Predicting video with vqvae. _arxiv:2103.01950_ , 2021. 6 

- [160] Mohammad Babaeizadeh et al. Fitvid: Overfitting in pixel-level video prediction. _arxiv:2106.13195_ , 2021. 6 

- [161] Diederik P Kingma and Max Welling. Auto-encoding variational bayes. _arxiv:1312.6114_ , 2013. 6 

- [162] Dirk Weissenborn, Oscar T¨ackstr¨om, and Jakob Uszkoreit. Scaling autoregressive video models. _arxiv:1906.02634_ , 2019. 6 

- [163] Aaron Van Den Oord et al. Neural discrete representation learning. _Neural information processing systems_ , 30, 2017. 6 

- [164] Wilson Yan, Yunzhi Zhang, Pieter Abbeel, and Aravind Srinivas. Videogpt: Video generation using vq-vae and transformers, 2021. URL `https://arxiv.org/abs/2104.10157` . 6, 12 

- [165] Prafulla Dhariwal and Alexander Nichol. Diffusion models beat gans on image synthesis. _Advances in neural information processing systems_ , 34:8780–8794, 2021. 6, 7, 10, 12, 22 

- [166] Zhifeng Kong, Wei Ping, Jiaji Huang, Kexin Zhao, and Bryan Catanzaro. Diffwave: A versatile diffusion model for audio synthesis. _arxiv:2009.09761_ , 2020. 6 

- [167] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising diffusion implicit models, 2022. URL `https: //arxiv.org/abs/2010.02502` . 6 

- [168] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-resolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10684–10695, 2022. 7, 10 

- [169] Weijie Kong, Qi Tian, Zijian Zhang, et al. Hunyuanvideo: A systematic framework for large video generative models, 2025. URL `https://arxiv.org/abs/2412.03603` . 7 

- [170] Federico Baldassarre et al. Back to the features: Dino as a foundation for video world models. _arxiv:2507.19468_ , 2025. 7 

- [171] Olaf Ronneberger, Philipp Fischer, and Thomas Brox. U-net: Convolutional networks for biomedical image segmentation. In _International Conference on Medical image computing and computer-assisted intervention_ , pages 234–241. Springer, 2015. 7 

- [172] Ozg¨un<sup>¨</sup> C¸i¸cek, Ahmed Abdulkadir, Soeren S Lienkamp, Thomas Brox, and Olaf Ronneberger. 3d u-net: learning dense volumetric segmentation from sparse annotation. In _International conference on medical image computing and computer-assisted intervention_ , pages 424–432. Springer, 2016. 7 

- [173] William Peebles and Saining Xie. Scalable diffusion models with transformers. In _Proc. of the IEEE/CVF international conference on computer vision_ , pages 4195–4205, 2023. 7 

30 

- [174] Shoufa Chen, Mengmeng Xu, Jiawei Ren, Yuren Cong, Sen He, Yanping Xie, Animesh Sinha, Ping Luo, Tao Xiang, and Juan-Manuel Perez-Rua. Gentron: Diffusion transformers for image and video generation. In _Proc. of the IEEE/CVF Conference on CVPR_ , pages 6441–6451, 2024. 7 

- [175] Jay Zhangjie Wu et al. Tune-a-video: One-shot tuning of image diffusion models for text-to-video generation. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 7623–7633, 2023. 7 

- [176] Jonathan Ho and Tim Salimans. Classifier-free diffusion guidance. _arxiv:2207.12598_ , 2022. 7, 22 

- [177] Jinbo Xing, Menghan Xia, Yong Zhang, Haoxin Chen, Wangbo Yu, Hanyuan Liu, Gongye Liu, Xintao Wang, Ying Shan, and Tien-Tsin Wong. Dynamicrafter: Animating open-domain images with video diffusion priors. In _European Conference on Computer Vision_ , pages 399–417. Springer, 2024. 7 

- [178] Shengming Yin, Chenfei Wu, Jian Liang, Jie Shi, Houqiang Li, Gong Ming, and Nan Duan. Dragnuwa: Finegrained control in video generation by integrating text, image, and trajectory, 2023. URL `https://arxiv.org/ abs/2308.08089` . 

- [179] Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li, Tianshui Chen, Menghan Xia, Ping Luo, and Ying Shan. Motionctrl: A unified and flexible motion controller for video generation. In _ACM SIGGRAPH 2024 Conference Papers_ , pages 1–11, 2024. 9 

- [180] Yuwei Guo, Ceyuan Yang, Anyi Rao, Zhengyang Liang, Yaohui Wang, Yu Qiao, Maneesh Agrawala, Dahua Lin, and Bo Dai. Animatediff: Animate your personalized text-to-image diffusion models without specific tuning, 2024. URL `https://arxiv.org/abs/2307.04725` . 7 

- [181] Bingyan Liu, Chengyu Wang, Tingfeng Cao, Kui Jia, and Jun Huang. Towards understanding cross and self-attention in stable diffusion for text-guided image editing, 2024. URL `https://arxiv.org/abs/2403.03431` . 7 

- [182] Ethan Perez, Florian Strub, Harm de Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer, 2017. URL `https://arxiv.org/abs/1709.07871` . 7 

- [183] Jingjing Xu, Xu Sun, Zhiyuan Zhang, Guangxiang Zhao, and Junyang Lin. Understanding and improving layer normalization, 2019. URL `https://arxiv.org/abs/1911.07013` . 7 

- [184] Jonathan Ho et al. Imagen video: High definition video generation with diffusion models. _arxiv:2210.02303_ , 2022. 7 

- [185] Uriel Singer et al. Make-a-video: Text-to-video generation without text-video data. _arxiv:2209.14792_ , 2022. 7 

- [186] Nate Gillman, Charles Herrmann, Michael Freeman, Daksh Aggarwal, Evan Luo, Deqing Sun, and Chen Sun. Force prompting: Video generation models can learn and generalize physics-based control signals, 2025. URL `https://arxiv.org/abs/2505.19386` . 7 

- [187] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding conditional control to text-to-image diffusion models, 2023. 

- [188] Seungwook Kim, Seunghyeon Lee, and Minsu Cho. Freeaction: Training-free techniques for enhanced fidelity of trajectory-to-video generation. _arxiv:2509.24241_ , 2025. 7, 9 

- [189] Eric Xing, Mingkai Deng, Jinyu Hou, and Zhiting Hu. Critiques of world models, 2025. URL `https://arxiv. org/abs/2507.05169` . 8 

- [190] Randall Balestriero and Yann LeCun. Lejepa: Provable and scalable self-supervised learning without the heuristics, 2025. 8 

- [191] Adrien Bardes, Jean Ponce, and Yann LeCun. Vicreg: Variance-invariance-covariance regularization for selfsupervised learning, 2022. 8 

- [192] Jiannan Xiang et al. Pandora: Towards general world model with natural language actions and video states. _arxiv:2406.09455_ , 2024. 8, 9 

- [193] Aether Team et al. Aether: Geometric-aware unified world modeling. _arxiv:2503.18945_ , 2025. 8, 9 

- [194] Zezhong Qian, Xiaowei Chi, Yuming Li, Shizun Wang, Zhiyuan Qin, Xiaozhu Ju, Sirui Han, and Shanghang Zhang. Wristworld: Generating wrist-views via 4d world models for robotic manipulation. _arxiv:2510.07313_ , 2025. 9 

31 

- [195] Angel Villar-Corrales and Sven Behnke. Playslot: Learning inverse latent dynamics for controllable object-centric video prediction and planning. _arxiv:2502.07600_ , 2025. 9 

- [196] Calvin Luo, Zilai Zeng, Yilun Du, and Chen Sun. Solving new tasks by adapting internet video knowledge. _arxiv:2504.15369_ , 2025. 9 

- [197] Hongxiang Zhao, Xingchen Liu, Mutian Xu, Yiming Hao, Weikai Chen, and Xiaoguang Han. Taste-rob: Advancing video generation of task-oriented hand-object interaction for generalizable robotic manipulation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 27683–27693, 2025. 9 

   - Taste-rob: 

- [198] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. _arxiv:2109.13396_ , 2021. 9 

- [199] Alexander Khazatsky et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arxiv:2403.12945_ , 2024. URL `https://arxiv.org/abs/2403.12945` . 9, 20 

- [200] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler, and George Drettakis. 3d gaussian splatting for real-time radiance field rendering. _ACM Trans. Graph._ , 42(4):139–1, 2023. 9 

- [201] Siyuan Zhou et al. Learning 3d persistent embodied world models. _arxiv:2505.05495_ , 2025. 9 

- [202] Jason Lee et al. Molmoact: Action reasoning models that can reason in space. _arxiv:2508.07917_ , 2025. 9 

- [203] Asher J Hancock, Xindi Wu, Lihan Zha, Olga Russakovsky, and Anirudha Majumdar. Actions as language: Fine-tuning vlms into vlas without catastrophic forgetting. _arxiv:2509.22195_ , 2025. 9 

- [204] Sicheng Xie, Haidong Cao, Zejia Weng, Zhen Xing, Haoran Chen, Shiwei Shen, Jiaqi Leng, Zuxuan Wu, and Yu-Gang Jiang. Human2robot: Learning robot actions from paired human-robot videos. _arxiv:2502.16587_ , 2025. 9 

- [205] Yao Feng, Hengkai Tan, Xinyi Mao, Chendong Xiang, Guodong Liu, Shuhe Huang, Hang Su, and Jun Zhu. Vidar: Embodied video diffusion model for generalist manipulation. _arxiv:2507.12898_ , 2025. 10 

- [206] Liudi Yang, Yang Bai, George Eskandar, Fengyi Shen, Mohammad Altillawi, Dong Chen, Soumajit Majumder, Ziyuan Liu, Gitta Kutyniok, and Abhinav Valada. Roboenvision: A long-horizon video generation model for multi-task robot manipulation. _arXiv:2506.22007_ , 2025. 9 

- [207] Yucheng Hu et al. Video prediction policy: A generalist robot policy with predictive visual representations. _arxiv:2412.14803_ , 2024. 10 

- [208] Shuaiyi Huang et al. Ardup: Active region video diffusion for universal policies. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pages 8465–8472. IEEE, 2024. 10 

- [209] Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arxiv:2504.02792_ , 2025. 10 

- [210] Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. _arxiv:2506.19850_ , 2025. 10 

- [211] Xinlong Wang, Xiaosong Zhang, Zhengxiong Luo, Quan Sun, Yufeng Cui, Jinsheng Wang, Fan Zhang, Yueze Wang, Zhen Li, Qiying Yu, et al. Emu3: Next-token prediction is all you need. _arXiv preprint arXiv:2409.18869_ , 2024. 10 

- [212] Junbang Liang, Pavel Tokmakov, Ruoshi Liu, Sruthi Sudhakar, Paarth Shah, Rares Ambrus, and Carl Vondrick. Video generators are robot policies, 2025. URL `https://arxiv.org/abs/2508.00795` . 10 

- [213] NVIDIA Research. World Simulation With Video Foundation Models for Physical AI. _NVIDIA Research Publication_ , September 2025. 9 

- [214] Zhenghao Zhang, Junchao Liao, Menghao Li, Zuozhuo Dai, Bingxue Qiu, Siyu Zhu, Long Qin, and Weizhi Wang. Tora: Trajectory-oriented diffusion transformer for video generation. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 2063–2073, 2025. 9 

- [215] Xiao Fu, Xintao Wang, Xian Liu, Jianhong Bai, Runsen Xu, Pengfei Wan, Di Zhang, and Dahua Lin. Learning video generation for robotic manipulation with collaborative trajectory control. _arxiv:2506.01943_ , 2025. 9 

- [216] Hongyin Zhang, Pengxiang Ding, Shangke Lyu, Ying Peng, and Donglin Wang. Gevrm: Goal-expressive video generation model for robust visual manipulation. _arxiv:2502.09268_ , 2025. 9 

32 

- [217] Dominik Schmidt and Minqi Jiang. Learning to act without actions. In _The Twelfth International Conference on Learning Representations_ , 2024. 10 

- [218] Pulkit Agrawal, Ashvin V Nair, Pieter Abbeel, Jitendra Malik, and Sergey Levine. Learning to poke by poking: Experiential learning of intuitive physics. _Advances in neural information processing systems_ , 29, 2016. 10 

- [219] Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield. Foundationpose: Unified 6d pose estimation and tracking of novel objects. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 17868–17879, 2024. 10 

- [220] Yann Labb´e, Lucas Manuelli, Arsalan Mousavian, Stephen Tyree, Stan Birchfield, Jonathan Tremblay, Justin Carpentier, Mathieu Aubry, Dieter Fox, and Josef Sivic. Megapose: 6d pose estimation of novel objects via render & compare. _arxiv:2212.06870_ , 2022. 10 

- [221] Bingxin Ke, Dominik Narnhofer, Shengyu Huang, Lei Ke, Torben Peters, Katerina Fragkiadaki, Anton Obukhov, and Konrad Schindler. Video depth without video models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 7233–7243, 2025. 10 

- [222] Ilija Radosavovic, Baifeng Shi, Letian Fu, Ken Goldberg, Trevor Darrell, and Jitendra Malik. Robot learning with sensorimotor pre-training. In _Conference on Robot Learning_ , pages 683–693. PMLR, 2023. 10 

- [223] Chi-Lam Cheang et al. Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation. _arxiv:2410.06158_ , 2024. 10 

- [224] Hongtao Wu et al. Unleashing large-scale video generative pre-training for visual robot manipulation. _arxiv:2312.13139_ , 2023. 10 

- [225] Yanjiang Guo, Yucheng Hu, Jianke Zhang, Yen-Jen Wang, Xiaoyu Chen, Chaochao Lu, and Jianyu Chen. Prediction with action: Visual policy learning via joint denoising process. _Advances in Neural Information Processing Systems_ , 37:112386–112410, 2024. 10 

- [226] Younggyo Seo, Kimin Lee, Stephen L James, and Pieter Abbeel. Reinforcement learning with action-free pre-training from videos. In _International Conference on Machine Learning_ , pages 19561–19579. PMLR, 2022. 11 

- [227] Zhennan Jiang, Kai Liu, Yuxin Qin, Shuai Tian, Yupeng Zheng, Mingcai Zhou, Chao Yu, Haoran Li, and Dongbin Zhao. World4rl: Diffusion world models for policy refinement with reinforcement learning for robotic manipulation. _arxiv:2509.19080_ , 2025. 11 

- [228] Shuyang Gu, Dong Chen, Jianmin Bao, Fang Wen, Bo Zhang, Dongdong Chen, Lu Yuan, and Baining Guo. Vector quantized diffusion model for text-to-image synthesis. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 10696–10706, 2022. 12 

- [229] Google DeepMind. State-of-the-art video and image generation with Veo 2 and Imagen 3. Google Official Blog, December 2024. URL `https://blog.google/innovation-and-ai/models-and-research/google-labs/ video-image-generation-update-december-2024/` . 12 

- [230] Xuanlin Li et al. Evaluating real-world robot manipulation policies in simulation. _arxiv:2405.05941_ , 2024. 12 

- [231] Kaifeng Zhang et al. Real-to-sim robot policy evaluation with gaussian splatting simulation of soft-body interactions. _arxiv:2511.04665_ , 2025. 

- [232] Arhan others Jain. Polaris: Scalable real-to-sim evaluations for generalist robot policies. _arxiv:2512.16881_ , 2025. 12 

- [233] Tim Brooks, Aleksander Holynski, and Alexei A Efros. Instructpix2pix: Learning to follow image editing instructions. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 18392–18402, 2023. 13 

- [234] Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, and Chuang Gan. Adaworld: Learning adaptable world models with latent actions. _arxiv:2503.18938_ , 2025. 13 

- [235] Yecheng Jason Ma, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. Liv: Language-image representations and rewards for robotic control. In _International Conference on Machine Learning_ , pages 23301–23320. PMLR, 2023. 13 

- [236] Yilun Du et al. Learning universal policies via text-guided video generation. _Advances in neural information processing systems_ , 36:9156–9172, 2023. 13 

33 

- [237] Stephanie Fu, Netanel Tamir, Shobhita Sundaram, Lucy Chai, Richard Zhang, Tali Dekel, and Phillip Isola. Dreamsim: Learning new dimensions of human visual similarity using synthetic data, 2023. URL `https: //arxiv.org/abs/2306.09344` . 14 

- [238] Tim Salimans, Ian Goodfellow, Wojciech Zaremba, Vicki Cheung, Alec Radford, and Xi Chen. Improved techniques for training gans. _Advances in neural information processing systems_ , 29, 2016. 14 

- [239] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. Gans trained by a two time-scale update rule converge to a local nash equilibrium, 2018. URL `https://arxiv.org/abs/1706.08500` . 14, 15 

- [240] K Manasa and Sumohana S Channappayya. An optical flow-based full reference video quality assessment algorithm. _IEEE Transactions on Image Processing_ , 25(6):2480–2492, 2016. 14 

- [241] Xiaowei Chi, Chun-Kai Fan, Hengyuan Zhang, Xingqun Qi, Rongyu Zhang, et al. Eva: An embodied world model for future video anticipation. _arxiv:2410.15461_ , 2024. 14 

- [242] Fengzhe Zhou, Jiannan Huang, Jialuo Li, Deva Ramanan, and Humphrey Shi. Physical ai bench: A comprehensive benchmark for physical ai generation and understanding, 2025. URL `https://github.com/SHI-Labs/ physical-ai-bench` . 14, 15 

- [243] Haoning Wu, Erli Zhang, Liang Liao, Chaofeng Chen, Jingwen Hou, et al. Exploring video quality assessment on user generated contents from aesthetic and technical perspectives. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 20144–20154, 2023. 15 

- [244] Will Kay, Joao Carreira, Karen Simonyan, Brian Zhang, Chloe Hillier, Sudheendra Vijayanarasimhan, Fabio Viola, Tim Green, Trevor Back, Paul Natsev, Mustafa Suleyman, and Andrew Zisserman. The kinetics human action video dataset, 2017. URL `https://arxiv.org/abs/1705.06950` . 15 

- [245] Hu Yue, Siyuan Huang, Yue Liao, Shengcong Chen, Pengfei Zhou, Liliang Chen, Maoqing Yao, and Guanghui Ren. Ewmbench: Evaluating scene, motion, and semantic quality in embodied world models. _arxiv:2505.09694_ , 2025. 15, 18 

- [246] Meta AI Research. Dinov2: Learning robust visual features without supervision, 2024. URL `https://arxiv. org/abs/2304.07193` . 15 

- [247] Vipula Rawte, Sarthak Jain, Aarush Sinha, Garv Kaushik, Aman Bansal, et al. Vibe: A text-to-video benchmark for evaluating hallucination in large multimodal models. In _Proceedings of the 5th Workshop on Trustworthy NLP (TrustNLP 2025)_ , pages 232–246, 2025. 16 

- [248] Zhixuan Chu, Lei Zhang, Yichen Sun, Siqiao Xue, Zhibo Wang, Zhan Qin, and Kui Ren. Sora detector: A unified hallucination detection for large text-to-video models. _arxiv:2405.04180_ , 2024. 16 

- [249] Samuel Greydanus, Misko Dzamba, and Jason Yosinski. Hamiltonian neural networks. _Neural information processing systems_ , 32, 2019. 17 

- [250] Christine Allen-Blanchette, Sushant Veer, Anirudha Majumdar, and Naomi Ehrich Leonard. Lagnetvip: A lagrangian neural network for video prediction, 2020. URL `https://arxiv.org/abs/2010.12932` . 17 

- [251] Shaowei Liu, Zhongzheng Ren, Saurabh Gupta, and Shenlong Wang. Physgen: Rigid-body physics-grounded image-to-video generation. In _European Conference on Computer Vision (ECCV)_ , 2024. 17 

- [252] Zizhang Li, Hong-Xing Yu, Wei Liu, Yin Yang, Charles Herrmann, Gordon Wetzstein, and Jiajun Wu. Wonderplay: Dynamic 3d scene generation from a single image and actions, 2025. URL `https://arxiv.org/abs/2505.18151` . 17 

- [253] Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu, and Stefano Ermon. Sdedit: Guided image synthesis and editing with stochastic differential equations. _arxiv:2108.01073_ , 2021. 17 

- [254] Hanchao Liu, Wenyuan Xue, Yifei Chen, Dapeng Chen, Xiutian Zhao, Ke Wang, Liping Hou, Rongjun Li, and Wei Peng. A survey on hallucination in large vision-language models. _arxiv:2402.00253_ , 2024. 17 

- [255] George Em Karniadakis, Ioannis G Kevrekidis, Lu Lu, Paris Perdikaris, Sifan Wang, and Liu Yang. Physicsinformed machine learning. _Nature Reviews Physics_ , 3(6):422–440, 2021. 17 

- [256] Zecheng Yu, Yifei Huang, Ryosuke Furuta, Takuma Yagi, Yusuke Goutsu, and Yoichi Sato. Fine-grained affordance annotation for egocentric hand-object interaction videos. In _Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision_ , pages 2155–2163, 2023. 17 

34 

- [257] Yong-Lu Li, Hongwei Fan, Zuoyu Qiu, Yiming Dou, Liang Xu, Hao-Shu Fang, Peiyang Guo, Haisheng Su, Dongliang Wang, Wei Wu, et al. Discovering a variety of objects in spatio-temporal human-object interactions. _arxiv:2211.07501_ , 2022. 17 

- [258] Kuan Fang, Te-Lin Wu, Daniel Yang, Silvio Savarese, and Joseph J. Lim. Demo2vec: Reasoning object affordances from online videos. In _2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 2139–2147, 2018. doi: 10.1109/CVPR.2018.00228. 17 

- [259] Tushar Nagarajan, Christoph Feichtenhofer, and Kristen Grauman. Grounded human-object interaction hotspots from video. In _2019 IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 8687–8696, 2019. doi: 10.1109/ICCV.2019.00878. 

- [260] Shaowei Liu, Subarna Tripathi, Somdeb Majumdar, and Xiaolong Wang. Joint hand motion and interaction hotspots prediction from egocentric videos. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 3282–3292, 2022. 

- [261] Lorenzo Mur-Labadia, Jose J Guerrero, and Ruben Martinez-Cantin. Multi-label affordance mapping from egocentric vision. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 5238–5249, 2023. 17 

- [262] Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from human videos as a versatile representation for robotics. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 13778–13790, 2023. 17 

- [263] Yuanchen Ju, Kaizhe Hu, Guowei Zhang, Gu Zhang, Mingrun Jiang, and Huazhe Xu. Robo-abc: Affordance generalization beyond categories via semantic correspondence for robot manipulation. In _European Conference on Computer Vision_ , pages 222–239. Springer, 2024. 

- [264] Gen Li, Nikolaos Tsagkas, Jifei Song, Ruaridh Mon-Williams, Sethu Vijayakumar, Kun Shao, and Laura SevillaLara. Learning precise affordances from egocentric videos for robotic manipulation. In _Proc. of the IEEE/CVF International Conference on Computer Vision_ , pages 10581–10591, 2025. 

- [265] Miao Liu, Siyu Tang, Yin Li, and James M Rehg. Forecasting human-object interaction: joint prediction of motor attention and actions in first person video. In _European conference on computer vision_ , pages 704–721. Springer, 2020. 17 

- [266] Ola Shorinwa, Zhiting Mei, Justin Lidard, Allen Z Ren, and Anirudha Majumdar. A survey on uncertainty quantification of large language models: Taxonomy, open research challenges, and future directions. _ACM Computing Surveys_ , 2025. 17 

- [267] Long Ouyang et al. Training language models to follow instructions with human feedback. _Advances in neural information processing systems_ , 35:27730–27744, 2022. 18 

- [268] Zhiting Mei, Christina Zhang, Tenny Yin, Justin Lidard, Ola Shorinwa, and Anirudha Majumdar. Reasoning about uncertainty: Do reasoning models know when they don’t know?, 2025. URL `https://arxiv.org/abs/2506.18183` . 19 

- [269] Anthropic. Training a helpful and harmless assistant with reinforcement learning from human feedback, 2022. 19 

- [270] Kai-Chieh Hsu, Haimin Hu, and Jaime F. Fisac. The safety filter: A unified view of safety-critical control in autonomous systems. _Annual Review of Control, Robotics, and Autonomous Systems_ , 7(Volume 7, 2024): 47–72, 2024. ISSN 2573-5144. doi: https://doi.org/10.1146/annurev-control-071723-102940. URL `https: //www.annualreviews.org/content/journals/10.1146/annurev-control-071723-102940` . 20 

- [271] Sankalp Agrawal, Junwon Seo, Kensuke Nakamura, Ran Tian, and Andrea Bajcsy. Anysafe: Adapting latent safety filters at runtime via safety constraint parameterization in the latent space, 2025. URL `https://arxiv. org/abs/2509.19555` . 20 

- [272] Homer Rich Walke et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pages 1723–1736. PMLR, 2023. 20 

- [273] Open X-Embodiment Collaboration. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 20 

- [274] Jing Wang, Fengzhuo Zhang, Xiaoli Li, Vincent YF Tan, Tianyu Pang, Chao Du, Aixin Sun, and Zhuoran Yang. Error analyses of auto-regressive video diffusion models: A unified framework. _arxiv:2503.10704_ , 2025. 21 

35 

- [275] Shengqu Cai, Ceyuan Yang, Lvmin Zhang, Yuwei Guo, Junfei Xiao, Ziyan Yang, Yinghao Xu, Zhenheng Yang, Alan Yuille, Leonidas Guibas, et al. Mixture of contexts for long video generation. _arxiv:2508.21058_ , 2025. 21 

- [276] Shengming Yin, Chenfei Wu, Huan Yang, Jianfeng Wang, Xiaodong Wang, Minheng Ni, Zhengyuan Yang, Linjie Li, Shuguang Liu, Fan Yang, et al. Nuwa-xl: Diffusion over diffusion for extremely long video generation. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 1309–1320, 2023. 21 

- [277] Max Bain, Arsha Nagrani, G¨ul Varol, and Andrew Zisserman. Frozen in time: A joint video and image encoder for end-to-end retrieval. In _Proceedings of the IEEE/CVF international conference on computer vision_ , pages 1728–1738, 2021. 21 

- [278] Yuanhan Zhang, Jinming Wu, Wei Li, Bo Li, Zejun Ma, Ziwei Liu, and Chunyuan Li. Video instruction tuning with synthetic data. _arxiv:2410.02713_ , 2024. 21 

- [279] Ji Lin, Hongxu Yin, Wei Ping, Pavlo Molchanov, Mohammad Shoeybi, and Song Han. Vila: On pre-training for visual language models. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 26689–26699, 2024. 21 

- [280] Junyu Chen, Han Cai, Junsong Chen, Enze Xie, Shang Yang, Haotian Tang, Muyang Li, Yao Lu, and Song Han. Deep compression autoencoder for efficient high-resolution diffusion models, 2025. URL `https: //arxiv.org/abs/2410.10733` . 22 

- [281] Ruili Feng, Han Zhang, Zhantao Yang, Jie Xiao, Zhilei Shu, Zhiheng Liu, Andy Zheng, Yukun Huang, Yu Liu, and Hongyang Zhang. The matrix: Infinite-horizon world generation with real-time moving control. _arxiv:2412.03568_ , 2024. 22 

- [282] Tianchen Zhao, Tongcheng Fang, Haofeng Huang, et al. Vidit-q: Efficient and accurate quantization of diffusion transformers for image and video generation, 2025. URL `https://arxiv.org/abs/2406.02540` . 22 

- [283] Tianwei Yin, Qiang Zhang, Richard Zhang, William T Freeman, Fredo Durand, Eli Shechtman, and Xun Huang. From slow bidirectional to fast autoregressive video diffusion models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 22963–22974, 2025. 22 

36 

