---
title: "Do World Action Models Generalize Better than VLAs? A Robustness Study"
date: "2026-03-23"
authors: "Zhanguang Zhang; Zhiyuan Li; Behnam Rahmati; Rui Heng Yang; Yintao Ma; Amir Rasouli"
url: https://arxiv.org/abs/2603.22078
pdf: https://arxiv.org/pdf/2603.22078
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2603.22078)** / [論文ページ](https://arxiv.org/abs/2603.22078)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# DO WORLD ACTION MODELS GENERALIZE BETTER THAN VLAS? A ROBUSTNESS STUDY 

Zhanguang Zhang<sup>1</sup> , Zhiyuan Li<sup>_∗_1</sup><sup>_,_2</sup> , Behnam Rahmati<sup>_†_1</sup> , Rui Heng Yang<sup>1</sup> , Yintao Ma<sup>1</sup> , Amir Rasouli<sup>1</sup> 

Sajjad Pakdamansavoji<sup>1</sup> , Yangzheng Wu<sup>1</sup> , Lingfeng Zhang<sup>1</sup> , Tongtong Cao<sup>1</sup> , Feng Wen<sup>1</sup> 

Xinyu Wang<sup>1</sup> , Xingyue Quan<sup>1</sup> and Yingxue Zhang<sup>1</sup><sup>_∗_</sup> 

1Huawei Technologies 2University of Toronto 

## **ABSTRACT** 

Robot action planning in the real world is challenging as it requires not only understanding the current state of the environment but also predicting how it will evolve in response to actions. Vision-languageaction (VLA), which repurpose large-scale vision-language models for robot action generation using action experts, have achieved notable success across a variety of robotic tasks. Nevertheless, their performance remains constrained by the scope of their training data, exhibiting limited generalization to unseen scenarios and vulnerability to diverse contextual perturbations. More recently, world models have been revisited as an alternative to VLAs. These models, referred to as world action models (WAMs), are built upon world models that are trained on large corpora of video data to predict future visual states. With minor adaptations, their latent representation can be decoded into robot actions. It has been suggested that their explicit dynamic prediction capacity, combined with spatiotemporal priors acquired from web-scale video pre-training, enables WAMs to generalize more effectively than VLAs. In this paper, we conduct a comparative study of prominent state-of-the-art VLA policies and recently released WAMs. We evaluate their performance on the LIBERO-Plus and RoboTwin 2.0-Plus benchmarks under various visual and language perturbations. Our results show that WAMs achieve strong robustness, with LingBot-VA reaching 74.2% success rate on RoboTwin 2.0-Plus and Cosmos-Policy achieving 82.2% on LIBERO-Plus. While VLAs such as _π_ 0 _._ 5 can achieve comparable robustness on certain tasks, they typically require extensive training with diverse robotic datasets and varied learning objectives. Hybrid approaches that partially incorporate video-based dynamic learning exhibit intermediate robustness, highlighting the importance of how video priors are integrated. Overall, our findings shed light on critical insights into the strengths of WAMs relative to VLAs, as well as the remaining challenges for real-world deployment. The evaluation code for the RoboTwin2.0-Plus benchmark is available at: https://robot-robustness.github.io/RoboTwin2.0-Plus/ 

## **1 Introduction** 

Robot motion planning in real-world environments—whether for navigation, manipulation, or locomotion—remains highly challenging. A key difficulty arises from the diversity and uncertainty of real-world settings, which makes it hard for robot policies to anticipate the consequences of their actions. Recently, vision–language–action (VLA) policies [Black et al., 2025a, Kim et al., 2025] have emerged as a new paradigm compared to traditional motion planning approaches [Elbanhawi and Simic, 2014]. By leveraging foundation models trained on large-scale vision and language data, VLA policies have demonstrated strong performance across a wide range of robotic tasks, including navigation [Xu et al., 2024], manipulation [Zheng et al., 2026], and locomotion [Jiang et al., 2026]. 

Despite their strong performance, VLAs exhibit several notable limitations, including limited generalization ability [Ma et al., 2026] and a lack of robustness to distractions and cluttered environments [Rasouli et al., 2026]. In essence, they often lack a fundamental understanding of the physical world that is necessary for consistent planning across 

> _∗_ Corresponding to {zhanguang.zhang, yingxue.zhang}@huawei.com 

> _†_ work done during internship at Huawei Canada 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

diverse environments. To address this issue, recent work has begun incorporating world models into robotic policies. Traditionally, world models have been used primarily as simulators for model training and evaluation [Cutler et al., 2015, Ha and Schmidhuber, 2018a, Hafner et al., 2020]. More recently, they have been increasingly integrated into robot policies—including VLAs—in a variety of ways, such as auxiliary training objectives [Chen et al., 2025b, Cen et al., 2025], planning modules [Yin et al., 2025, Gao et al., 2025], or guidance mechanisms for flow-based policies [Du and Song, 2025, Huang et al., 2025, Chen et al., 2026]. Building on this trend, new approaches go a step further by proposing the use of world models directly as control policies [Kim et al., 2026, Goswami et al., 2025b, Liao et al., 2025, Li et al., 2026b, Ye et al., 2026b], where the model’s latent representations are decoded into actions. 

Given the many similarities between foundation models and world models, there is ongoing debate about the primary advantages of world models and whether their explicit use in planning is necessary, since foundation-based robot policies may already implicitly model the world dynamics. To investigate this question, we conduct a comparative study of state-of-the-art VLA policies and world action models (WAMs), aiming to highlight their differences under a range of contextual perturbations. More specifically, we leverage two enhanced manipulation benchmarks to evaluate the robustness of policy models: **LIBERO-Plus** [Fei et al., 2025], which introduces seven types of perturbations to single-arm manipulation tasks, and **RoboTwin 2.0-Plus** , an in-house benchmark that follows a similar perturbation protocol in the two-arm Aloha-Agilex setup of RoboTwin 2.0 [Chen et al., 2025a]. 

Our findings reveal that WAMs generally demonstrate strong robustness to noise, lighting and layout perturbations in both single-arm and bimanual settings. This robustness is believed to be at least partially attributable to the spatiotemporal priors inherited from their world model backbones. While classic VLAs like _π_ 0 _._ 5 [Black et al., 2025a], as well as hybrid approaches like MOTUS [Bi et al., 2025] and VLA-JEPA [Sun et al., 2026], can achieve comparable or even superior robustness, they often require carefully curated and diverse datasets and/or explicit dynamic prediction objectives during the embodied pre-training phase. In contrast, the simplicity of the embodied pre-training phase represents a key advantage of WAMs over classic VLAs. However, the high inference overhead of WAMs remains a major challenge that limits their deployment in real-world robotic systems, with a single inference step being at least 4.8 times slower than _π_ 0 _._ 5. Recent GigaWorld-Policy [Ye et al., 2026a] and Fast-WAM [Yuan et al., 2026] mitigate this issue by generating actions only at inference time, while jointly predicting future visual state or conditioning state prediction on actions during training. In our evaluation, Fast-WAM achieves performance on RoboTwin 2.0-Plus that is essentially on par with the state-of-the-art IDM-based WAM (LingBot-VA), but its robustness on LIBERO-Plus collapses sharply when the training data lacks diversity, suggesting that joint-denoising designs may rely more heavily on training-data diversity for generalization than IDM-style designs that explicitly condition action on a predicted future state. Their inference latency also remains substantial compared to the _π_ -series, posing challenges for smooth real-world deployment. Further research is needed to more efficiently exploit the dynamic priors of world-model backbones and improve both training and inference efficiency. 

## **2 Related Works** 

### **2.1 Vision Language Action (VLAs)** 

Recent progress in robot foundation models has focused on integrating perception, language understanding, and control within unified multimodal architectures. A central direction in this line of work is the development of vision–language–action (VLA) models that connect high-level semantic reasoning with low-level robot execution. Early work such as PaLM-E [Driess et al., 2023] demonstrates that large language models can be adapted to embodied settings by representing visual observations and robot states as additional tokens in a transformer. This formulation shows that knowledge learned from internet-scale data can support downstream robotic manipulation and long-horizon tasks when paired with action prediction. Building on this paradigm, a series of works explored large-scale end-to-end VLA policies trained on robot demonstrations. RT-1 and RT-2 [Brohan et al., 2023, Zitkovich et al., 2023] introduced transformer policies that map visual observations and language instructions directly to robot actions, showing that large multi-task datasets enable generalization across manipulation behaviors. RT-H [Belkhale et al., 2024] further explored hierarchical policy structures that improve data efficiency and long-horizon execution. In parallel, the _π_ 0 series [Black et al., 2025b] studied scaling behavior in VLA policies, emphasizing the role of action representation and dataset diversity in enabling robust multi-task generalization. 

A second line of work emphasizes data-centric scaling and cross-embodiment generalization. Octo [Octo Model Team et al., 2024], trained on the Open X-Embodiment dataset [O’Neill et al., 2024], demonstrated that a single policy can learn from heterogeneous datasets spanning multiple robots and tasks. OpenVLA [Kim et al., 2025] further advanced this direction by providing an open-source VLA implementation built on pretrained multimodal encoders, highlighting the importance of reproducible pipelines and shared datasets for scaling robot foundation models. More recent research has focused on improving reasoning and adaptation within VLA architectures. CoT-VLA [Zhao et al., 

2 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

2025b] introduces visual chain-of-thought reasoning by predicting intermediate visual goals before generating actions, improving long-horizon task performance. ChatVLA-2 [Zhou et al., 2025] explores integrating open-world reasoning capabilities from pretrained vision–language models into robotic policies. Meanwhile, X-VLA [Zheng et al., 2026] investigates scalable cross-embodiment learning through embodiment-specific soft prompts, and SimpleVLA-RL [Li et al., 2026a] demonstrates that reinforcement learning applied after imitation pre-training can significantly improve robustness and long-horizon execution. 

### **2.2 World Model in Robotics** 

World models learn the internal representation of the world and can predict future visual states conditioned on actions. Although the concept has long been studied [Craik, 1967, Sandage, 1988, Ha and Schmidhuber, 2018b], it has recently experienced a surge in interest and has been applied across a wide range of applications, including image retrieval [Tang et al., 2025], autonomous driving [Hassan et al., 2025, Zhao et al., 2025a], medical imaging [Yue et al., 2025, Yang et al., 2025a], face generation [Zheng et al., 2025], and robotics locomotion [Hao et al., 2025, Wang et al., 2025], navigation [Bar et al., 2025, Yao et al., 2025], object manipulation [Zhen et al., 2025]. 

In the context of robotics, world models have been used in several ways, including as simulators for training and evaluation [Shang et al., 2025], as auxiliary modules to boost planning policies [Yin et al., 2025], or as policies themselves after certain adaptations [Goswami et al., 2025a]. Below we provide a brief review of each of these categories. 

### **2.2.1 World Models as Learned Simulators** 

In robotics and embodied AI, world models are most operationally useful when treated as **learned simulators** : actionconditioned generative models that produce counterfactual futures for decision-making. Rather than focusing on perceptual reconstruction or open-ended generation, this view treats the model as a computational substrate for control, where imagined rollouts must remain action-grounded, decision-relevant, and stable under closed-loop distribution shift [Ha and Schmidhuber, 2018b, Hafner et al., 2019, 2020]. Importantly, simulation does not need to occur in pixel space. Latent dynamics models—such as recurrent state-space models and predictive state representations—enable compact rollouts as long as task-relevant structure is preserved [Littman and Sutton, 2001]. This shift from reconstruction fidelity toward control-aligned prediction exposes a key tension: improvements in likelihood or visual fidelity do not necessarily translate to better planning or policy learning, especially under long-horizon drift or objective mismatch [Lambert et al., 2020, Soh and Lim, 2026]. 

Learned simulators are used in two main ways. First, they support explicit planning, where policies optimize actions by querying the model at test time. Latent planners such as PlaNet, PETS, and MBPO perform model predictive control with varying strategies to mitigate model error [Hafner et al., 2019, Chua et al., 2018, Janner et al., 2019]. More recently, V-JEPA 2-AC enables planning from image goals in latent space after large-scale pre-training on video data [Assran et al., 2025]. H-WM further explores hierarchical planning by coupling symbolic task-level prediction with visual state prediction, using intermediate subgoals to guide long-horizon robotic task and motion planning [Chen et al., 2026]. Video-based and foundation-scale simulators extend this idea to high-dimensional observations, enabling goal-directed planning from images or large-scale video pre-training [Finn and Levine, 2017, Ebert et al., 2018]. NVIDIA presents Cosmos-Predict2.5 as a multimodal world-generation model designed to support robotics planning and large-scale synthetic rollouts [NVIDIA, 2025, NVIDIA et al., 2025]. Second, world models enable imaginationbased policy optimization, where policies are trained directly on simulated trajectories, as in World Models, Dreamer, and its successors [Ha and Schmidhuber, 2018a, Hafner et al., 2020, 2023]. Hybrid approaches such as TD-MPC combine short-horizon model rollouts with value bootstrapping to limit compounding error while retaining sample efficiency [Hansen et al., 2022, 2024]. Across these paradigms, the simulator’s value lies less in perceptual realism and more in producing predictions that are reliable for control. 

In visual navigation, world models are increasingly used to support tasks such as image-goal navigation. The Navigation World Model (NWM) [Bar et al., 2025] enables goal-conditioned navigation by using a Model Predictive Control (MPC) [Kouvaritakis and Cannon, 2016] framework to simulate and evaluate candidate trajectories. Building on this idea, a lightweight one-step world model [Shen et al., 2026] employs a 3D U-Net with spatial–temporal attention to predict future observations, improving robustness and efficiency in multi-modal goal navigation tasks. More recently, MindJourney [Yang et al., 2025b] leverages world models for test-time scaling to enhance a vision–language model’s understanding of 3D dynamics. 

3 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 1: **Summary of world action models (WAMs)** . **MOT** : mixture-of-transformers, indicating that separate transformer backbones are used for video and action streams, with cross-modal interactions facilitated via attention at each layer. Note that the released LingBot-VA model adopts a unified transformer for both modalities, instead of the mixture-of-transformer architecture described in the paper. **Pretrain Free** : the method does not require task-agnostic embodied pre-training. **Causal Pred.** : action prediction is conditioned on the generated visual state, or vice versa. **AR Gen.** : auto-regressive generation. 

|**Model**|**#Params**|**Backbone**|**MOT**|**Pretrain**<br>**Free**|**Causal**<br>**Pred.**|**AR Gen.**|
|---|---|---|---|---|---|---|
|VPP<br>[Hu et al., 2025]|1.5B|Stable Video<br>Diffusion (SVD)|✗|✗|✓|✗|
|GE-Act<br>[Liao et al., 2025]|2.2B|LTX-Video-2B|✓|✗|✗|✓|
|Cosmos-Policy<br>[Kim et al., 2026]|2B|Cosmos-Predict2-2B|✗|✓|✗|✗|
|LingBot-VA<br>[Li et al., 2026b]|5.3B|Wan2.2-5B|✓?|✗|✓|✓|
|DreamZero<br>[Ye et al., 2026b]|14B|Wan2.1-14B|✗|✗|✗|✓|
|GigaWorld-Policy<br>[Ye et al., 2026a]|>5B|Wan2.2-5B|✗|✗|✓|✗|
|Fast-WAM<br>[Yuan et al., 2026]|6B|Wan2.2-5B|✓|✓|✗|✗|


### **2.2.2 World Models as Auxiliary Tasks** 

In this scheme, world knowledge is acquired by augmenting the policy with predictive capacities. This is achieved by introducing auxiliary prediction tasks [Chen et al., 2025b, Cen et al., 2025, Zhang et al., 2025, Sun et al., 2026, Wang et al., 2026] or by co-training the policy with a predictive model [Wang et al., 2026, Li et al., 2025]. In Chen et al. [2025b], a GPT-like architecture is proposed in which video content is converted into latent motion tokens that are incorporated with the text and the initial image observation. The model is first pre-trained to predict future video tokens and then finetuned with an action head to generate motions. WorldVLA [Cen et al., 2025] enhances the VLA policy by adding image prediction component to generate future scenes given the observation and current action. DreamVLA [Zhang et al., 2025] augments the policy with three auxiliary predictive tasks: semantic, depth and dynamic prediction. In Sun et al. [2026], the authors employ a teacher–student training framework in which a predictive video encoder generates dynamic targets from future visual states, while the VLM backbone produces latent action representations using only the current observation. These two latent representations are then mapped and combined to form future states, which are learned through an alignment loss. The authors of Wang et al. [2026] achieve multitasking by using interleaved representations that combine discrete vision, language, and action tokens as input. Unified World Model [Zhu et al., 2025] integrates action and video diffusion processes within a unified transformer architecture, with independent diffusion timesteps governing each modality. Following this scheme, the model can learn a forward dynamics, an inverse dynamics, and a video generator. MOTUS [Bi et al., 2025] introduces a Mixture-of-Transformers (MoT) architecture that unifies video and action generation, enabling training across five tasks with diverse data types. The model in Li et al. [2025] learns a policy by decoupling video-action decoding. Via a masking operation in video and action space, the model is induced to forward and inverse dynamics, as well as planning capability. For the navigation task. UniWM Dong et al. [2025] integrates prediction and control within a unified multimodal framework, first predicting actions and then autoregressively reconstructing future visual observations, with the reconstruction loss serving as an auxiliary supervision for action prediction. 

### **2.2.3 World Action Models (WAMs)** 

Despite the success of the VLAs aforementioned, they are mostly finetuned from VLM backbone models pretrained with an auto-regressive next-token prediction objective. While this language-centric pre-training enables models to capture high-level visual semantics, it often neglects the perception and prediction of fine-grained world dynamics that are essential for precise robotic control. With recent advances in action-conditioned video generation, a growing body of research has begun to explore adapting video generation models for policy learning [Bi et al., 2025, Hu et al., 2025, Kim et al., 2026, Li et al., 2026b, Ye et al., 2026b,a, Yuan et al., 2026]. Video Prediction Policy (VPP) by Hu et al. [2025] is among the earliest efforts to repurpose a video generation backbone for robot action generation. Specifically, a video 

4 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

diffusion model is first pretrained on text-guided video prediction task, and then further adapted to generate robot actions with a diffusion policy head conditioned on visual features encoded by the video model. Empirical results show that the video pre-training stage is crucial for the observed performance improvements. Building on this paradigm, mimicvideo [Pai et al., 2025] leverages a language-conditioned video generation model (i.e., Cosmos-Predict2-2B [Agarwal et al., 2025], while retaining the same two-stage training scheme. It introduces a flow matching-based action decoder that is trained from scratch and serves as an inverse dynamic model (IDM). GE-Act [Liao et al., 2025], built on the Genie Envisioner (GE) platform, follows a similar strategy. Leveraging a pretrained video diffusion model backbone (i.e., LTX-Video-2B), it introduces a lightweight, flow-matching action decoder which maps video model encoded latent features to robot action trajectories. Despite the success of mimic-video and GE-Act, training an additional action decoder from scratch can disrupt the latent space learned by the video model and incurs extra training cost. Instead, Cosmos-policy [Kim et al., 2026] minimally adapts the diffusion process of the video generation model Cosmos-Predict2, encoding the robot state, future image and value estimates directly as latent frames. With these lightweight architectural modifications, the model is finetuned under joint training objectives for policy, world model and value prediction. The resulting model supports both direct policy generation and model-based planning through its predicted future state and value estimates. LingBot-VA [Li et al., 2026b] and DreamZero [Ye et al., 2026b] enhance causal reasoning capacity of video-based policy model by unifying future visual state prediction and action inference within an interleaved sequence and autoregressively generating future predictions conditioned on previous step’s outputs. This formulation enables efficient KV-cache memory integration while enforcing causal consistency—both of which are crucial for long-horizon robotic tasks. While using different video generation backbones, both methods address the challenge of slow inference of video models for robot control. To improve real-time performance, they accelerate inference through techniques such as asynchronous inference pipeline and partial video denoising, among other optimizations. 

GigaWorld-Policy [Ye et al., 2026a] and Fast-WAM [Yuan et al., 2026] aim to mitigate the slow inference time of WAMs by treating video generation as optional at test time. GigaWorld-Policy conditions future visual state prediction on actions, whereas Fast-WAM jointly generate both modalities. Both designs enable test-time action prediction without explicitly generating visual state, as required in other IDM-based approaches (e.g., LingBot-VA), thereby significantly reducing the inference latency. However, the reported inference latencies of GigaWorld-Policy (360 ms) and Fast-WAM (190 ms) remain substantially higher than that of _π_ 0 [Black et al., 2025b] on a consumer-level device (73 ms), leaving considerable room for improvement. Beyond inference speed, Fast-WAM also demonstrates great data efficiency in both simulation and real-world tasks by requiring only task-specific finetuning, without costly embodied pre-training on large-scale task-agnostic data. As shown in our evaluation (Table 3), Fast-WAM is essentially on par with the state-of-the-art LingBot-VA on RoboTwin 2.0, despite the absence of embodied pre-training—further substantiating the data efficiency of the WAM paradigm. 

The key characteristics of recent WAMs are summarized in Table 1. We only consider the methods that leverage a pretrained world model backbone for robot action generation, with minimal or no architecture modifications. Consequently, MOTUS is excluded from this list: although it adopts a pretrained Wan2.2-5B for video generation, it relies on an additional VLM for action generation rather than the world model backbone itself. Typically, lightweight modifications are introduced to the video backbones to encode robot joint state and produce robot actions. While some approaches (e.g., Cosmos-Policy, GigaWorld-Policy) employ a unified transformer backbone for both video and action streams, others such as GE-Act and Fast-WAM adopt mixture-of-transformers (MOT) architectures, using a smaller, dedicated transformer for action modeling. Regarding training objectives, WAM models are typically trained to predict future visual state and actions, and in most cases require embodied pre-training on large-scale robot data. The design of causal attention also varies across methods. For instance, LingBot-VA conditions action generation on predicted visual state, whereas Cosmos-Policy and DreamZero jointly denoise both modalities. In contrast, GigaWorld-Policy conditions video generation on actions. Autoregressive generation is employed in GE-Act, LingBot-VA and DreamZero to condition prediction on historical context, improving temporal consistency and inference efficiency. 

### **2.3 Differences between WAMs and VLAs** 

WAMs differ from VLAs in their backbone model choices, training strategies, and prediction schemes. While WAMs leverage video generation models pretrained for video synthesis, VLAs are typically built upon VLM backbones pretrained for next-token prediction. The training datasets used by several influential VLAs, WAMs, and hybrid approaches are summarized in Table 2. In terms of notation, the training scheme is divided into two phases: **taskagnostic embodied pre-training** and **task-specific finetuning** . The embodied pre-training may be followed by a separate post-training stage, as in the case of _π_ 0 _._ 5 [Black et al., 2025a]. During the embodied pre-training stage, WAMs are commonly trained to jointly predict future visual states and actions using robot manipulation data. In contrast, VLAs are typically trained either for next-token prediction or action diffusion, often using not only robot data but also multi-modal web data and human videos in some cases [Black et al., 2025a, Bu et al., 2025]. In terms of 

5 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 2: **Training data of VLAs and WAMs across different training stages. Training stages** : <mark>Embodied Pre-training , Embodied Post-training , Task-specif</mark> i <mark>c Finetuning .</mark> **PT** : filtered data for embodied posttraining. 

|**Model**|**Semantic Understanding**<br>**& Spatial Grounding**|**General Video**<br>|**Robot Data**|**Task-specific Data**|
|---|---|---|---|---|
|||_VLAs_|||
|_π_0|-|-|Cross-embodiment (>10k h)|Trajectories (5–100 h)|
|OpenVLA-OFT|-|-|Cross-embodiment (970k)|Trajectories (20–300)|
|X-VLA|-|-|Cross-embodiment (288k)|Trajectories (50)|
|_π_0_._5|High-level planning|-|Mobile manipulation (400 h)|Trajectories (1–20 h)|
||Web data-VQA||Multi-env. tabletop||
||Web data-captioning||Cross-embodiment||
||Web data-grounding||Mobile manipulation (PT)||
||High-level planning (PT)<br>Verbal instruction<br>Web data (PT)||Multi-env. tabletop (PT)||
|||_VLA + WM_|||
|VLA-JEPA|-|Human Ego (220k)|Single-embodiment (76k)|Trajectories (100)|
|MOTUS|-|Human Ego (231k)|Cross-embodiment (781k)|Trajectories (100)|
||||Cross-embodiment (781k)<br>Task-agnostic data (1k)||
|||_WAMs_|||
|Cosmos-Policy|-|-<br>|-|Trajectories (185)|
|DreamZero|-|-|Single-embodiment (500 h)|Trajectories (12–40 h)|
|GE-Act|-|-|Single-embodiment (3k h)|Trajectories (1 h)|
|LingBot-VA|-|-|Cross-embodiment (16k h)|Trajectories (50)|
|GigaWorld-Policy|-|Human Ego (4.5k h)|Cross-embodiment (6.7k h)|Trajectories (50)|
|Fast-WAM|-|-<br>|-|Trajectories (60 h)|


prediction schemes, VLAs typically map current state _ht_ directly to the action _at_ via _pθ_ ( _at|ht_ ). In contrast, WAMs either jointly predict the future visual state _ht_ +1 and action _at_ via _pϕ_ ( _ht_ +1 _, at|ht_ ) or first predict the future visual state and then condition action generation on the predicted state, analogous to an inverse dynamic model (IDM), as _pϕ_ ( _ht_ +1 _|ht_ ) _· gψ_ ( _at|ht, ht_ +1). In a less common causal formulation, GigaWorld-Policy predicts the action first, then generates future visual state conditioned on the action. 

The pre-training stage of video generation backbones such as Cosmos-Predict2 involves future visual state prediction—specifically the _pϕ_ ( _ht_ +1 _| ht_ ) component—trained on diverse internet-scale video data covering natural dynamics, hand motion, driving, etc. This video pre-training objective enhances the model’s ability to capture general physical dynamics and to predict fine-grained spatiotemporal state transitions. Given this prior physical knowledge, the embodied pre-training phase of WAMs can primarily focus on establishing general action prediction, _gψ_ ( _at | ht, ht_ +1), which is a relatively easier learning problem. Prior work suggests that agents capable of generalizing to multi-step goal-directed tasks must effectively learn predictive structure in the environment [Richens et al., 2025]. In contrast, the backbones of VLAs—VLMs—are typically trained on static image-text data and therefore often lack fine-grained dynamic prediction capability. As a result, VLAs generally require more diverse geometric grounding, video data, and robotic data during embodied pre-training to implicitly acquire models of world dynamics. 

6 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 


Figure 1: **Examples of perturbations on RoboTwin 2.0-Plus tasks.** Definition of notations (N1, L1, etc.) can be found in Section A 

## **3 Experiments** 

### **3.1 Datasets** 

To systematically compare the robustness of world action models (WAMs) and vision-language-action (VLA) models under diverse perturbation factors, we propose the **RoboTwin 2.0-Plus** benchmark, constructed upon RoboTwin 2.0 [Chen et al., 2025a] and following the perturbation protocol of LIBERO-Plus [Fei et al., 2025] with minor parameter adjustments. Specifically, perturbations are applied along the following axes: (1) _Camera_ , altering the viewpoint pose of the third-person camera; (2) _Robot_ , varying the initial joint configuration; (3) _Language_ , paraphrasing or altering task instructions; (4) _Light_ , modifying illumination intensity, shadow direction, and color temperature; (5) _Background_ , changing table and scene textures; (6) _Noise_ , applying photometric distortions to input images; and (7) _Layout_ , introducing task-irrelevant distractive objects into the workspace. This benchmark is designed to facilitate evaluation of WAMs and VLAs that provide open-source checkpoints trained on RoboTwin 2.0. Further details are provided in Section A. In addition, we also evaluate existing approaches on the open-sourced **LIBERO-Plus** benchmark Fei et al. [2025]. 

LIBERO-Plus and RoboTwin 2.0-Plus differ substantially in their underlying environments, as summarized in Table 8. The primary distinction lies in their observation and action spaces. LIBERO-Plus employs a 7-DoF Franka Panda robot equipped with two cameras—one third-person view and one wrist-mounted—both operating at a resolution of 256 _×_ 256. In contrast, RoboTwin 2.0-Plus features a dual-arm bimanual system based on the Aloha-Agilex platform, with three cameras: a head-mounted third-person view and two wrist-mounted cameras, each capturing images at 320 _×_ 240 resolution. These differences in embodiment, sensing configuration, and action space make the two benchmarks complementary. LIBERO-Plus primarily evaluates single-arm dexterity under perturbations, whereas RoboTwin 2.0-Plus focuses on the robustness of bimanual coordination. 

### **3.2 Evaluation Methods** 

We conduct comprehensive evaluation of VLAs and WAMs for which publicly available checkpoints exist. On RoboTwin 2.0-Plus, We evaluate X-VLA [Zheng et al., 2026], MOTUS [Bi et al., 2025] and LingBot-VA [Li et al., 2026b] using their released checkpoints finetuned on the original RoboTwin 2.0 dataset. Due to the known performance gap between the JAX and PyTorch implementations of the _π_ -series models—also reported in Bi et al. [2025] and Li et al. [2026b]—and the absence of a JAX version of _π_ 0 _._ 5, we finetuned the JAX implementation of _π_ 0 _._ 5 on the RoboTwin 2.0 dataset. The model is finetuned from the pretrained _π_ 0 _._ 5 checkpoint on the full 27.5k RoboTwin 2.0 training data for 60k gradient steps using the openpi framework’s recommended configuration: AdamW optimizer ( _β_ 1=0 _._ 9, _β_ 2=0 _._ 95, gradient clipping at 1.0), cosine decay learning rate schedule (peak 2 _._ 5 _×_ 10<sup>_−_5</sup> , decaying to 2 _._ 5 _×_ 10<sup>_−_6</sup> ), batch size 64, with delta joint actions. More model checkpoints are publicly available for LIBERO, and some of them have been evaluated on LIBERO-Plus. We report the results of a diverse set of VLAs and WAMs, including classic VLAs from the _π_ 0-series [Black et al., 2025b,a] (JAX version); approaches that incorporate world modeling as auxiliary tasks, such 

7 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 3: **RoboTwin 2.0-Plus evaluation results** . The _Original_ column reports the success rate of each method evaluated in the original RoboTwin 2.0 _Easy_ setting. For a fair comparison, all methods use a single unified model across all tasks. The best result in each column is highlighted in **bold** , while second-best result is underlined. **Lang.** : Language. **BG** : Background. 

|Model|Original|Camera|Robot|Lang.|Light|BG|Noise|Layout|Total|
|---|---|---|---|---|---|---|---|---|---|
|||||_VLAs_||||||
|_π_0_._5|78.4|**45.6**|27.6|74.4|49.6|71.7|64.9|56.8|58.6|
|X-VLA|65.6|23.2|65.2|64.4|63.1|58.6|49.7|34.8|53.1|
|||||_VLA + WM_||||||
|MOTUS|87.0|21.6|**85.0**|83.2|84.6|84.4|43.1|82.8|71.5|
|||||_WAMs_||||||
|LingBot-VA|**92.1**|28.9|36.2|**87.3**|**89.0**|**91.3**|**80.9**|**87.9**|**74.2**|
|Fast-WAM|91.2|30.4|53.2|86.7|88.8|90.0|76.4|83.2|72.7|


as VLA-JEPA [Sun et al., 2026]; and recent WAMs including GE-Act [Liao et al., 2025] and Cosmos-Policy [Kim et al., 2026]. A detailed comparison of these models is presented in Section C. 

Although DreamZero [Ye et al., 2026b] is included in our WAM taxonomy (Table 1), we exclude it from the benchmark evaluation for three reasons. First, its released checkpoint is trained on a proprietary cross-embodiment dataset and cannot be directly applied to LIBERO or RoboTwin 2.0 without re-training. Second, re-training is prohibitively expensive, as the model is built on the Wan2.1-14B video generation backbone—the largest among all WAMs surveyed—and its autoregressive interleaved training procedure demands substantial GPU resources. Third, the inference pipeline requires a warm-up phase exceeding 15 minutes, making benchmark-scale evaluation across thousands of rollout episodes impractical. The checkpoint of GigaWorld-Policy is also not yet publicly available; we therefore include it in the architectural comparison but exclude it from the quantitative evaluation. Fast-WAM [Yuan et al., 2026], which was previously unreleased, has since become available and is included in our evaluation: we use the `robotwin_uncond_3cam_384` checkpoint for RoboTwin 2.0-Plus (finetuned on the standard 27.5k clean + domain-randomized demonstrations) and a LIBERO checkpoint trained on clean demonstrations only. This training-data asymmetry between the two Fast-WAM checkpoints is intentional and revisited in **RQ 2** , as it offers a useful natural experiment on the role of task-specific data diversity. 

### **3.3 Results** 

We aim to address the following research questions through our experiments and analysis: 

- **RQ 1.** Are WAM-based policies robust to perturbations? 

- **RQ 2.** Is the performance advantage of WAMs consistent across different perturbation types? 

- **RQ 3.** How to explain the performance differences between VLAs and WAMs? 

- **RQ 4.** What are the runtime characteristics of WAMs and how do they compare to those of VLAs? 

Our key findings addressing the aforementioned questions are summarized below. 

### **RQ 1.** Are WAM-based policies robust to perturbations? 

Recent WAM studies have reported superior performance over VLAs in both simulation and real robot experiments Kim et al. [2026], Bi et al. [2025], Li et al. [2026b]. In particular, WAMs demonstrate stronger scene and task generalization, largely attributed to the spatiotemporal priors inherited from the video pre-training. We adopt RoboTwin 2.0-Plus and LIBERO-Plus described in prior session to rigorously evaluate the robustness of policy models under diverse perturbation conditions. As shown in Table 3, LinBot-VA achieves the SOTA success rate of 92.1% on the original RoboTwin 2.0 benchmark and consistently exhibits great robustness to various perturbations. It ranks first in five out of seven perturbation categories and achieves an overall success rate of 74.2%, which is significantly higher than 58.6% by _π_ 0 _._ 5 and 72.7% of the second-best method Fast-WAM. Several representative cases are illustrated in Figure 2. While _π_ 0 _._ 5 struggles with visual perturbations such as noise, light and cluttered layout, LingBot-VA performs effectively under these conditions, demonstrating greater robustness. The results of LIBERO-Plus further corroborate the robustness advantage of WAMs on a second benchmark. Cosmos-Policy achieves an impressive 98.5% success rate on the original 

8 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 


Figure 2: **Case studies on RoboTwin 2.0-Plus.** We present three representative cases comparing _π_ 0 _._ 5 and LingBot-VA. Keyframes are shown sequentially from left to right. **(a)** _Task:_ beat block with hammer. _Perturbation:_ noise (N3). _Result: π_ 0 _._ 5 collides with the hammer and fails to complete the task. **(b)** _Task:_ handover block. _Perturbation:_ layout. _Result: π_ 0 _._ 5 collides with the red block during approach, leading to failure. **(c)** _Task:_ rank RGB blocks. _Perturbation:_ lighting (L1–L4 mix). _Result: π_ 0 _._ 5 fails to grasp the first red block due to misalignment and does not recover. LingBotVA success in all three cases shown. 

LIBERO benchmark and maintains an 82.2% overall success rate with all perturbations introduced in LIBERO-Plus. GE-Act follows closely, attaining an 80.3% success rate on LIBERO-Plus. Despite the high sensitivity of most VLAs to perturbations, _π_ 0 _._ 5 delivers strong and consistent performance, achieving the highest overall success rate of 85.7%. 

Furthermore, Fast-WAM—the only WAM in our evaluation that requires no embodied pre-training—achieves an overall success rate of 72.7% on RoboTwin 2.0-Plus (Table 3), placing it second only to LingBot-VA and ahead of MOTUS. This indicates that the spatiotemporal priors of the video backbone alone—without any large-scale embodied pretraining—can yield WAM-level robustness, provided the task-specific training data is sufficiently diverse, a condition we examine more carefully in **RQ 2** . 

Notably, several models occupy a middle ground between pure VLAs and WAMs, and their behavior sheds light on how video priors are integrated, not merely whether they are present. MOTUS incorporates a pretrained video generation backbone (Wan2.2-5B) but routes action generation through a separate VLM expert rather than the video model itself. On RoboTwin 2.0-Plus as shown in Table 3, MOTUS achieves the highest robot initial-state robustness (85.0%) and the third-best overall score (71.5%), suggesting that incorporation of the additional video backbone and jointly training with dynamic prediction enhances the robustness of the learned policy. VLA-JEPA, on the other hand, augments a standard VLM backbone (Qwen3-VL-2B) with a future-state prediction objective trained on human videos, effectively injecting video-like temporal priors into the VLA framework. Its competitive performance on LIBERO-Plus (77.9% in total) indicates that even partial incorporation of spatiotemporal learning can meaningfully improve robustness, though it still falls short of dedicated WAMs that natively operate in the video latent space. 

### **RQ 2.** Is the performance advantage of WAMs consistent across different perturbation types? 

The behavior of WAMs varies across different types of perturbations. As shown in Table 3, LingBot-VA consistently demonstrates strong robustness to visually based perturbations. In particular, it maintains strong performance under light (89.0%), noise (80.9%), and layout (87.9%) perturbations, while facing challenges in scenarios involving variations in camera viewpoint and the robot’s initial state. A similar trend is observed in the LIBERO-Plus results shown in Table 4, where Cosmos-Policy and GE-Act demonstrate high robustness in light, noise and layout perturbations. Visualizations of predictions by Cosmos-Predict, shown in Figure 3, indicate that the future images predicted by Cosmos-policy remain highly accurate under varying noise and light conditions. Notably, when the input image is corrupted by noise, Cosmos-policy is able to effectively denoise the moving robotic arm in its predictions. This capacity is likely attributable to its pre-training on web-scale videos containing dynamic objects. However, the predictions exhibit severe spatial distortions and inconsistent color schemes under certain background perturbation—probably due to the uncommon 

9 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 4: **LIBERO-Plus evaluation results** . The _Original_ column denotes results on the standard LIBERO benchmark. The results of _π_ 0, _π_ 0-FAST, Openvla-OFT-m, UniVLA, RIPT-VLA are sourced from Fei et al. [2025]. The results reported for HoloBrain0-GD [Lin et al., 2026] and ABot-M0 [Yang et al., 2026] are taken from their respective papers. The remaining models are evaluated using their official repositories and publicly released checkpoints. Specifically, _π_ 0(rerun) and _π_ 0 _._ 5 are evaluated using their JAX implementations. The best result in each column is highlighted in **bold** , while second-best result is underlined. **Lang.** : Language. **BG** : Background. 

|Model|Original|Camera|Robot|Lang.|Light|BG|Noise|Layout|Total|
|---|---|---|---|---|---|---|---|---|---|
|||||_VLAs_||||||
|_π_0|94.2|13.8|6.0|58.8|85.0|81.4|79.0|68.9|53.6|
|_π_0(rerun)|91.3|61.0|40.8|63.5|89.3|84.1|80.1|76.4|69.4|
|_π_0-FAST|85.5|65.1|21.6|61.0|73.2|73.2|74.4|68.8|61.6|
|_π_0_._5|96.9|75.4|77.5|85.6|**96.9**|94.6|89.7|**85.7**|**85.7**|
|Openvla-OFT_m|97.6|55.6|21.7|81.0|92.7|91.0|78.6|68.7|67.9|
|UniVLA|95.2|1.8|46.2|69.6|69.0|81.0|21.2|31.9|42.9|
|RIPT-VLA|97.5|55.2|31.2|77.6|88.4|91.6|73.5|74.2|68.4|
|X-VLA|98.1|23.4|**89.7**|75.7|88.2|**96.0**|62.7|71.8|71.4|
|HoloBrain0-GD|96.7|65.5|58.2|78.7|88.1|90.3|66.9|79.5|74.0|
|ABot-M0|**98.6**|60.4|67.9|86.4|96.2|91.6|86.4|82.6|80.5|
||||_V_|_LA + WM_||||||
|VLA-JEPA|97.2|64.2|67.7|**88.1**|91.8|93.4|65.8|83.9|77.9|
|||||_WAMs_||||||
|GE-Act|94.4|60.7|77.0|77.4|95.8|86.0|90.9|80.2|80.3|
|Cosmos-Policy|98.5|**75.8**|63.3|81.7|96.5|88.9|**92.7**|82.2|82.2|
|Fast-WAM|97.6|16.4|44.5|68.9|78.2|53.7|37.7|60.7|51.5|


background patterns. This degradation in the quality of predicted future images will likely lead to inaccurate action generation. 

Fast-WAM further provides a particularly clean natural experiment on the role of task-specific training-data diversity. On RoboTwin 2.0-Plus, where the released checkpoint was finetuned on the standard 27.5k clean + domain-randomized demonstrations, Fast-WAM is highly robust: 91.2% on the original benchmark and 72.7% averaged across perturbations (Table 3)—a drop of only _∼_ 18 points. On LIBERO-Plus, where the same architecture was trained on clean demonstrations only, the model achieves 97.6% on the original benchmark but degrades sharply under nearly every perturbation type (camera 16.4%, background 53.7%, noise 37.7%; Table 4), corresponding to an overall _∼_ 46-point drop. Since the architecture and video backbone are identical across the two checkpoints, the contrast isolates the contribution of training-data diversity: the spatiotemporal priors of the video backbone are necessary but not sufficient for robustness, and task-specific training-data diversity remains a critical lever even when the backbone is video-pretrained. Comparing across architectures, this also suggests that Fast-WAM—which jointly denoises state and action without explicitly conditioning the latter on a predicted future state—may be more dependent on training-data diversity to acquire generalization than IDM-style WAMs such as LingBot-VA, where the explicit state-to-action causal coupling provides an additional architectural prior for robustness. Overall, this is consistent with our broader finding that robustness emerges from the _integration_ of dynamic priors with diverse training data rather than from the presence of either alone. 

### **RQ 3.** How to explain the performance differences between VLAs and WAMs? 

As discussed in Section 2.3, WAMs differ from VLAs in both backbone selection and the subsequent training strategy for robot policy generation. Unlike VLAs, which typically leverage VLM backbones, WAMs build upon video diffusion models pretrained on web-scale video generation tasks. Exposure to diverse and temporally rich video data in video backbone enables WAMs to capture fine-grained visual dynamics and temporal dependencies without requiring extensive training for policy generation. As shown in Table 2, WAMs such as Cosmos-policy require only lightweight finetuning on downstream tasks while maintaining strong robustness under various visual perturbations. In contrast, the backbone models of VLAs are primarily trained on static image-text data and lack explicit priors over visual dynamics, which can limit their ability to adapt to new scenes and tasks. To achieve robustness comparable to WAMs, VLAs typically require additional training on diverse dynamic visual data. For instance, _π_ 0 _._ 5 achieves strong cross-scene generalization and robustness to visual perturbations by incorporating diverse robotic data and web data into its training pipeline. Similarly, hybrid methods such as VLA-JEPA and MOTUS with strong robustness also incorporate human 

10 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 


Figure 3: **Illustrations of future images predicted by Cosmos-policy.** Ground-truth and predicted images under three types of perturbations (noise, lighting, and background variations) in LIBERO-Plus are shown. GT: the ground truth. Pred.: the predictions generated by Cosmos-policy. 

video data in their training pipeline. Overall, the spatiotemporal priors inherited from video generation backbones substantially simplifies the training process of WAMs and reduce their reliance on diverse visual data. This advantage is particularly valuable in settings where data availability is limited. 

Table 5: **Runtime Speed Comparison.** The inference times of all models are evaluated using the same device. LingBotVA(RW): real-world setting with three denoising steps for state and five for action. LingBot-VA(RT): RoboTwin 2.0 setting with 25 denoising steps for state and 50 for action. 

||_π_0_._5|X-VLA|Fast-<br>WAM<sup>_∗_</sup>|GE-Act|Cosmos-<br>Policy|LingBot-<br>VA(RW)|MOTUS|LingBot-<br>VA(RT)|
|---|---|---|---|---|---|---|---|---|
|Action chunk size|50|30|32|36|16|32|16|32|
|Inference_t_(wall<br>clock)|63 ms|195 ms|190 ms|300 ms|390 ms|480 ms|1175 ms|5230 ms|
|Inference_t_(w.r.t.<br>|1.0|3.1_×_|3.0_×_|4.8_×_|6.2_×_|7.6_×_|18.6_×_|83.0_×_|
|_π_0_._5)|||||||||


> _<u>∗</u>_ Fast-WAM latency is reported by Yuan et al. [2026] on their hardware and is not re-measured on our device. 

**RQ 4.** What are the runtime characteristics of WAMs and how do they compare to those of VLAs? 

A major limitation of WAMs is their slower runtime compared to VLAs, primarily due to the computational overhead of the future-state diffusion process. As summarized in Table 5, the inference cost of WAMs varies considerably depending on architecture choices. Among VLAs, _π_ 0 _._ 5 achieves the fastest inference at 63 ms per chunk, while X-VLA takes 195 ms per inference. In contrast, MOTUS and WAMs are consistently slower, requiring at least 4.8 _×_ runtime per inference compared to _π_ 0 _._ 5. A critical factor that largely determines the speed of WAMs is the number of denoising steps for state and action, with state denoising typically dominating the runtime. For example, GE-Act requires only one denoising step for state and ten for action, whereas Cosmos-Policy performs five steps for both. MOTUS, in contrast, uses ten denoising steps for both state and action. LingBot-VA adopts different configurations depending on the setting: for real-world deployment, it uses three denoising steps for state and five for action, while for RoboTwin 2.0, it employs 25 and 50 steps, respectively, which explains its significantly longer inference time (5.2 seconds per inference). Runtime speed of WAMs is also affected by other factors, including backbone size (2B–5.3B parameters), generation strategy (joint denoising vs. separate action decoding), and whether autoregressive generation is employed. By omitting visual state generation at test time, Fast-WAM achieves the lowest inference latency among WAMs in our comparison (190 ms; Table 5), but is still 3.0 _×_ slower than _π_ 0 _._ 5. Further efforts are still needed to improve the inference efficiency of WAMs. 

11 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

## **4 Conclusion** 

We presented a systematic comparative study of world action models (WAMs) and vision-language-action models (VLAs), evaluating their robustness under diverse visual and language perturbations across two complementary benchmarks: RoboTwin 2.0-Plus and LIBERO-Plus. Our findings reveal that WAMs, by leveraging spatiotemporal priors from video generation backbones, consistently demonstrate strong robustness to noise, lighting, and layout perturbations—a pattern that holds across both single-arm (LIBERO) and bimanual (RoboTwin) settings. However, camera viewpoint and robot initial-state perturbations remain challenging for WAMs, indicating that video priors offer limited benefit when the geometric configuration of the scene is altered. Among VLAs, _π_ 0 _._ 5 achieves competitive or superior robustness by incorporating diverse robotic and web data during training, suggesting that data diversity can compensate for the absence of explicit world modeling. Hybrid approaches such as MOTUS and VLA-JEPA, which partially integrate video-based temporal learning, exhibit robustness profiles that fall between pure VLAs and WAMs, highlighting that the manner in which video priors are incorporated matters as much as their presence. 

Our analysis also reveals that inference speed remains a major challenge for WAMs, primarily driven by the visual state denoising process. While faster methods such as GE-Act requires only a single denoising step, the slowest model, LingBot-VA, requires up to 25 steps on the RoboTwin dataset. Compared to _π_ 0 _._ 5, the evaluated WAMs are at least 4.8 times slower per inference. This underscores a key practical challenge for WAMs and highlights the need for further research to improve their inference efficiency, enabling deployment in scenarios that require rapid response time or real-time interaction with dynamic environments. Recent approaches, such as Fast-WAM, have sought to accelerate inference by co-training visual state and action prediction and omitting state generation at test time. In our evaluation, Fast-WAM achieves competitive robustness on RoboTwin 2.0-Plus (72.7% overall, second only to LingBot-VA) without any embodied pre-training, demonstrating the data efficiency of the WAM paradigm. However, when restricted to clean training demonstrations on LIBERO, Fast-WAM’s robustness collapses (51.5% overall vs. 97.6% on the original benchmark), reinforcing that the WAM video prior is necessary but not sufficient—task-specific training-data diversity remains essential. A substantial latency gap also remains relative to _π_ 0 _._ 5 ( _∼_ 3 _×_ ) in real-world deployment, indicating room for further optimization. 

12 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

## **References** 

- Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model platform for physical ai. _arXiv preprint arXiv:2501.03575_ , 2025. 

- Mahmoud Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili, Matthew Muckley, Ammar Rizvi, Claire Roberts, Koustuv Sinha, Artem Zholus, Sergio Arnaud, Abha Gejji, Ada Martin, Francois Robert Hogan, Daniel Dugas, Piotr Bojanowski, Vasil Khalidov, Patrick Labatut, Francisco Massa, Marc Szafraniec, Kapil Krishnakumar, Yong Li, Xiaodong Ma, Sarath Chandar, Franziska Meier, Yann LeCun, Michael Rabbat, and Nicolas Ballas. V-jepa 2: Self-supervised video models enable understanding, prediction and planning. _arXiv preprint arXiv:2506.09985_ , 2025. URL `https://arxiv.org/abs/2506.09985` . 

- Amir Bar, Gaoyue Zhou, Danny Tran, Trevor Darrell, and Yann LeCun. Navigation world models. In _Proceedings of the Computer Vision and Pattern Recognition Conference_ , pages 15791–15801, 2025. 

- Suneel Belkhale, Tianli Ding, Ted Xiao, Pierre Sermanet, Quan Vuong, Jonathan Tompson, Yevgen Chebotar, Debidatta Dwibedi, and Dorsa Sadigh. Rt-h: Action hierarchies using language. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2024. 

- Hongzhe Bi, Hengkai Tan, Shenghao Xie, Zeyuan Wang, Shuhe Huang, Haitian Liu, Ruowen Zhao, Yao Feng, Chendong Xiang, Yinze Rong, et al. Motus: A unified latent action world model. _arXiv preprint arXiv:2512.13030_ , 2025. 

- Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Robert Equi, Chelsea Finn, Niccolo Fusai, Manuel Y. Galliker, Dibya Ghosh, Lachy Groom, Karol Hausman, brian ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Devin LeBlanc, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Allen Z. Ren, Lucy Xiaoyang Shi, Laura Smith, Jost Tobias Springenberg, Kyle Stachowicz, James Tanner, Quan Vuong, Homer Walke, Anna Walling, Haohuan Wang, Lili Yu, and Ury Zhilinsky. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. In _Proceedings of The 9th Conference on Robot Learning_ , 2025a. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, Szymon Jakubczak, Tim Jones, Liyiming Ke, Sergey Levine, Adrian Li-Bell, Mohith Mothukuri, Suraj Nair, Karl Pertsch, Lucy Xiaoyang Shi, James Tanner, Quan Vuong, Anna Walling, Haohuan Wang, and Ury Zhilinsky. _π_ 0: A vision-language-action flow model for general robot control. In _Proceedings of Robotics: Science and Systems (RSS)_ , 2025b. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Tomas Jackson, Sally Jesmonth, Nikhil J. Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Kuang-Huei Lee, Sergey Levine, Yao Lu, Utsav Malla, Deeksha Manjunath, Igor Mordatch, Ofir Nachum, Carolina Parada, Jodilyn Peralta, Emily Perez, Karl Pertsch, Jornell Quiambao, Kanishka Rao, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Kevin Sayed, Jaspiar Singh, Sumedh Sontakke, Austin Stone, Clayton Tan, Huong Tran, Vincent Vanhoucke, Steve Vega, Quan Vuong, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. Rt-1: Robotics transformer for real-world control at scale. In _Proceedings of Robotics: Science and Systems (RSS)_ , Daegu, Republic of Korea, July 2023. doi: 10.15607/RSS.2023.XIX.025. 

- Qingwen Bu, Yanting Yang, Jisong Cai, Shenyuan Gao, Guanghui Ren, Maoqing Yao, Ping Luo, and Hongyang Li. Learning to Act Anywhere with Task-centric Latent Actions. In _Proceedings of Robotics: Science and Systems_ , LosAngeles, CA, USA, June 2025. doi: 10.15607/RSS.2025.XXI.014. 

- Jun Cen, Chaohui Yu, Hangjie Yuan, Yuming Jiang, Siteng Huang, Jiayan Guo, Xin Li, Yibing Song, Hao Luo, Fan Wang, et al. Worldvla: Towards autoregressive action world model. _arXiv preprint arXiv:2506.21539_ , 2025. 

- Tianxing Chen, Zanxin Chen, Baijun Chen, Zijian Cai, Yibin Liu, Zixuan Li, Qiwei Liang, Xianliang Lin, Yiheng Ge, Zhenyu Gu, et al. Robotwin 2.0: A scalable data generator and benchmark with strong domain randomization for robust bimanual robotic manipulation. _arXiv preprint arXiv:2506.18088_ , 2025a. 

- Wenyuan Chen, Jinbang Huang, Oscar Pang, Zhiyuan Li, Xiao Hu, Lingfeng Zhang, Zhanguang Zhang, Mark Coates, Tongtong Cao, Xingyue Quan, and Zhang Yingxue. H-wm: Robotic task and motion planning guided by hierarchical world model. _arXiv preprint arXiv:2602.11291_ , 2026. 

- Yi Chen, Yuying Ge, Weiliang Tang, Yizhuo Li, Yixiao Ge, Mingyu Ding, Ying Shan, and Xihui Liu. Moto: Latent motion token as the bridging language for learning robot manipulation from videos. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , pages 19752–19763, October 2025b. 

13 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

- Kurtland Chua, Roberto Calandra, Rowan McAllister, and Sergey Levine. Deep reinforcement learning in a handful of trials using probabilistic dynamics models. _arXiv preprint arXiv:1805.12114_ , 2018. URL `https://arxiv.org/ abs/1805.12114` . NeurIPS 2018 (PETS). 

- Kenneth James Williams Craik. _The nature of explanation_ , volume 445. Cambrdige University Press, 1967. 

- Mark Cutler, Thomas J Walsh, and Jonathan P How. Real-world reinforcement learning via multifidelity simulators. _IEEE Transactions on Robotics_ , 31(3):655–671, 2015. 

- Yifei Dong, Fengyi Wu, Guangyu Chen, Zhi-Qi Cheng, Qiyu Hu, Yuxuan Zhou, Jingdong Sun, Jun-Yan He, Qi Dai, and Alexander G Hauptmann. Unified world models: Memory-augmented planning and foresight for visual navigation. _arXiv preprint arXiv:2510.08713_ , 2025. 

- Danny Driess, Fei Xia, Mehdi SM Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, et al. Palm-e: an embodied multimodal language model. In _Proceedings of the 40th International Conference on Machine Learning_ , pages 8469–8488, 2023. 

- Max Du and Shuran Song. Dynaguide: Steering diffusion polices with active dynamic guidance. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL `https://openreview.net/forum? id=XOw7Yf8qN3` . 

- Frederik Ebert, Chelsea Finn, Sudeep Dasari, Annie Xie, Alex Lee, and Sergey Levine. Visual foresight: Modelbased deep reinforcement learning for vision-based robotic control. _arXiv preprint arXiv:1812.00568_ , 2018. URL `https://arxiv.org/abs/1812.00568` . 

- Mohamed Elbanhawi and Milan Simic. Sampling-based robot motion planning: A review. _Ieee access_ , 2:56–77, 2014. 

- Senyu Fei, Siyin Wang, Junhao Shi, Zihao Dai, Jikun Cai, Pengfang Qian, Li Ji, Xinzhe He, Shiduo Zhang, Zhaoye Fei, Jinlan Fu, Jingjing Gong, and Xipeng Qiu. Libero-plus: In-depth robustness analysis of vision-language-action models. _arXiv preprint arXiv:2510.13626_ , 2025. 

- Chelsea Finn and Sergey Levine. Deep visual foresight for planning robot motion. _arXiv preprint arXiv:1610.00696_ , 2017. URL `https://arxiv.org/abs/1610.00696` . ICRA 2017. 

- Shenyuan Gao, Siyuan Zhou, Yilun Du, Jun Zhang, and Chuang Gan. Adaworld: Learning adaptable world models with latent actions. In _Forty-second International Conference on Machine Learning_ , 2025. URL `https://openreview. net/forum?id=QQegZj99sk` . 

- Raktim Gautam Goswami, Prashanth Krishnamurthy, Yann LeCun, and Farshad Khorrami. Osvi-wm: One-shot visual imitation for unseen tasks using world-model-guided trajectory generation. In _NeurIPS_ , 2025a. 

- Raktim Gautam Goswami, Prashanth Krishnamurthy, Yann LeCun, and Farshad Khorrami. OSVI-WM: One-shot visual imitation for unseen tasks using world-model-guided trajectory generation. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025b. URL `https://openreview.net/forum?id=eXO6g7BmOA` . 

- David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018a. URL `https://arxiv. org/abs/1803.10122` . 

- David Ha and Jürgen Schmidhuber. World models. _arXiv preprint arXiv:1803.10122_ , 2018b. 

- Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson. Learning latent dynamics for planning from pixels. In _Proceedings of the 36th International Conference on Machine Learning (ICML)_ , 2019. URL `https://proceedings.mlr.press/v97/hafner19a.html` . 

- Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mohammad Norouzi. Dream to control: Learning behaviors by latent imagination. In _International Conference on Learning Representations (ICLR)_ , 2020. URL `https: //openreview.net/forum?id=S1lOTC4tDS` . 

- Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv:2301.04104_ , 2023. URL `https://arxiv.org/abs/2301.04104` . DreamerV3 (arXiv). 

- Nicklas Hansen, Xiaolong Wang, and Hao Su. Temporal difference learning for model predictive control. In _Proceedings of the 39th International Conference on Machine Learning (ICML)_ , 2022. URL `https://proceedings.mlr. press/v162/hansen22a.html` . 

- Nicklas Hansen, Hao Su, and Xiaolong Wang. Td-mpc2: Scalable, robust world models for continuous control. _arXiv preprint arXiv:2310.16828_ , 2024. URL `https://arxiv.org/abs/2310.16828` . ICLR 2024. 

- Chenjie Hao, Weyl Lu, Yifan Xu, and Yubei Chen. Neural motion simulator pushing the limit of world models in reinforcement learning. In _CVPR_ , 2025. 

14 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

- Mariam Hassan, Sebastian Stapf, Ahmad Rahimi, Pedro M. B. Rezende, Yasaman Haghighi, David Brüggemann, Isinsu Katircioglu, Lin Zhang, Xiaoran Chen, Suman Saha, Marco Cannici, Elie Aljalbout, Botao Ye, Xi Wang, Aram Davtyan, Mathieu Salzmann, Davide Scaramuzza, Marc Pollefeys, Paolo Favaro, and Alexandre Alahi. Gem: A generalizable ego-vision multimodal world model for fine-grained ego-motion, object dynamics, and scene composition control. In _CVPR_ , 2025. 

- Yucheng Hu, Yanjiang Guo, Pengchao Wang, Xiaoyu Chen, Yen-Jen Wang, Jianke Zhang, Koushil Sreenath, Chaochao Lu, and Jianyu Chen. Video prediction policy: A generalist robot policy with predictive visual representations. In _Forty-second International Conference on Machine Learning_ , 2025. URL `https://openreview.net/forum?id= c0dhw1du33` . 

- Yuhang Huang, Jiazhao Zhang, Shilong Zou, Xinwang Liu, Ruizhen Hu, and Kai Xu. Ladi-WM: A latent diffusionbased world model for predictive manipulation. In _9th Annual Conference on Robot Learning_ , 2025. URL `https://openreview.net/forum?id=o2w2iiMyEU` . 

- Michael Janner, Justin Fu, Marvin Zhang, and Sergey Levine. When to trust your model: Model-based policy optimization. _arXiv preprint arXiv:1906.08253_ , 2019. URL `https://arxiv.org/abs/1906.08253` . NeurIPS 2019. 

- Haoran Jiang, Jin Chen, Qingwen Bu, Li Chen, Modi Shi, Yanjie Zhang, Delong Li, Chuanzhe Suo, wang chuang, zhihui peng, and Hongyang Li. WholebodyVLA: Towards unified latent VLA for whole-body loco-manipulation control. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL `https://openreview.net/ forum?id=OCJmVjyzN7` . 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, Thomas Kollar, Benjamin Burchfiel, Russ Tedrake, Dorsa Sadigh, Sergey Levine, Percy Liang, and Chelsea Finn. Openvla: An open-source vision-language-action model. In _CoRL_ , 2025. 

- Moo Jin Kim, Yihuai Gao, Tsung-Yi Lin, Yen-Chen Lin, Yunhao Ge, Grace Lam, Percy Liang, Shuran Song, Ming-Yu Liu, Chelsea Finn, and Jinwei Gu. Cosmos policy: Fine-tuning video models for visuomotor control and planning. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL `https: //openreview.net/forum?id=wPEIStHxYH` . 

- Basil Kouvaritakis and Mark Cannon. Model predictive control. _Switzerland: Springer International Publishing_ , 38 (13-56):7, 2016. 

- Nathan Lambert, Brandon Amos, Omry Yadan, and Roberto Calandra. Objective mismatch in model-based reinforcement learning. _arXiv preprint arXiv:2002.04523_ , 2020. URL `https://arxiv.org/abs/2002.04523` . Published in L4DC 2020. 

- Haozhan Li, Yuxin Zuo, Jiale Yu, et al. Simplevla-rl: Scaling vla training via reinforcement learning. In _International Conference on Learning Representations (ICLR)_ , 2026a. 

- Lin Li, Qihang Zhang, Yiming Luo, Shuai Yang, Ruilin Wang, Fei Han, Mingrui Yu, Zelin Gao, Nan Xue, Xing Zhu, et al. Causal world modeling for robot control. _arXiv preprint arXiv:2601.21998_ , 2026b. 

- Shuang Li, Yihuai Gao, Dorsa Sadigh, and Shuran Song. Unified video action model. _arXiv preprint arXiv:2503.00200_ , 2025. 

- Yue Liao, Pengfei Zhou, Siyuan Huang, Donglin Yang, Shengcong Chen, Yuxin Jiang, Yue Hu, Jingbin Cai, Si Liu, Jianlan Luo, et al. Genie envisioner: A unified world foundation platform for robotic manipulation. _arXiv preprint arXiv:2508.05635_ , 2025. 

- Xuewu Lin, Tianwei Lin, Yun Du, Hongyu Xie, Yiwei Jin, Jiawei Li, Shijie Wu, Qingze Wang, Mengdi Li, Mengao Zhao, et al. Holobrain-0 technical report. _arXiv preprint arXiv:2602.12062_ , 2026. 

- Michael L. Littman and Richard S. Sutton. Predictive representations of state. _Advances in Neural Information Processing Systems_ , 14, 2001. URL `https://papers.nips.cc/paper_files/paper/2001/hash/ 1e4d36177d71bbb3558e43af9577d70e-Abstract.html` . 

- Guoqing Ma, Siheng Wang, Zeyu Zhang, Shan Yu, and Hao Tang. Generalvla: Generalizable vision-language-action models with knowledge-guided trajectory planning. _arXiv preprint arXiv:2602.04315_ , 2026. 

- NVIDIA. Nvidia cosmos. Product / documentation page, 2025. URL `https://www.nvidia.com/en-us/ai/ cosmos/` . 

- NVIDIA, Arslan Ali, Junjie Bai, Maciej Bala, Yogesh Balaji, Aaron Blakeman, Tiffany Cai, Jiaxin Cao, Tianshi Cao, Elizabeth Cha, Yu-Wei Chao, Prithvijit Chattopadhyay, Mike Chen, Yongxin Chen, Yu Chen, Shuai Cheng, Yin Cui, Jenna Diamond, Yifan Ding, Jiaojiao Fan, Linxi Fan, Liang Feng, Francesco Ferroni, Sanja Fidler, Xiao Fu, Ruiyuan Gao, Yunhao Ge, Jinwei Gu, Aryaman Gupta, Siddharth Gururani, Imad El Hanafi, Ali Hassani, Zekun Hao, Jacob 

15 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Huffman, Joel Jang, Pooya Jannaty, Jan Kautz, Grace Lam, Xuan Li, Zhaoshuo Li, Maosheng Liao, Chen-Hsuan Lin, Tsung-Yi Lin, Yen-Chen Lin, Huan Ling, Ming-Yu Liu, Xian Liu, Yifan Lu, Alice Luo, Qianli Ma, Hanzi Mao, Kaichun Mo, Seungjun Nah, Yashraj Narang, Abhijeet Panaskar, Lindsey Pavao, Trung Pham, Morteza Ramezanali, Fitsum Reda, Scott Reed, Xuanchi Ren, Haonan Shao, Yue Shen, Stella Shi, Shuran Song, Bartosz Stefaniak, Shangkun Sun, Shitao Tang, Sameena Tasmeen, Lyne Tchapmi, Wei-Cheng Tseng, Jibin Varghese, Andrew Z. Wang, Hao Wang, Haoxiang Wang, Heng Wang, Ting-Chun Wang, Fangyin Wei, Jiashu Xu, Dinghao Yang, Xiaodong Yang, Haotian Ye, Seonghyeon Ye, Xiaohui Zeng, Jing Zhang, Qinsheng Zhang, Kaiwen Zheng, Andrew Zhu, and Yuke Zhu. World simulation with video foundation models for physical ai. _arXiv preprint arXiv:2511.00062_ , 2025. URL `https://arxiv.org/abs/2511.00062` . 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Lawrence Yunliang Chen, Pannag Sanketi, Quan Vuong, Ted Xiao, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. In _Proceedings of Robotics: Science and Systems_ , Delft, Netherlands, 2024. 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 6892–6903. IEEE, 2024. 

- Jonas Pai, Liam Achenbach, Victoriano Montesinos, Benedek Forrai, Oier Mees, and Elvis Nava. mimic-video: Video-action models for generalizable robot control beyond vlas. _arXiv preprint 2512.15692_ , 2025. 

- Amir Rasouli, Montgomery Alban, Sajjad Pakdamansavoji, Zhiyuan Li, Zhanguang Zhang, Aaron Wu, and Xuan Zhao. Distracted robot: How visual clutter undermine robotic manipulation. In _ICRA_ , 2026. 

- Jonathan Richens, David Abel, Alexis Bellot, and Tom Everitt. General agents contain world models. _arXiv preprint arXiv:2506.01622_ , 2025. 

- Allan Sandage. Observational tests of world models. _Annual Review of Astronomy and Astrophysics_ , 26:561–630, 1988. 

- Yu Shang, Xin Zhang, Yinzhou Tang, Lei Jin, Chen Gao, Wei Wu, and Yong Li. Roboscape: Physics-informed embodied world model. In _NeurIPS_ , 2025. 

- Wangtian Shen, Ziyang Meng, Jinming Ma, Mingliang Zhou, and Diyun Xiang. An efficient and multi-modal navigation system with one-step world model. _arXiv preprint arXiv:2601.12277_ , 2026. 

- Harold Soh and Eugene Lim. Action hallucination in generative visual-language-action models. _arXiv preprint arXiv:2602.06339_ , 2026. URL `https://arxiv.org/abs/2602.06339` . 

- Jingwen Sun, Wenyao Zhang, Zekun Qi, Shaojie Ren, Zezhi Liu, Hanxin Zhu, Guangzhong Sun, Xin Jin, and Zhibo Chen. Vla-jepa: Enhancing vision-language-action model with latent world model. _arXiv preprint arXiv:2602.10098_ , 2026. 

- Yuanmin Tang, Jing Yu, Keke Gai, Jiamin Zhuang, Gang Xiong, Gaopeng Gou, and Qi Wu. Missing target-relevant information prediction with world model for accurate zero-shot composed image retrieval. In _CVPR_ , 2025. 

- Qi Wang, Zhipeng Zhang, Baao Xie, Xin Jin, Yunbo Wang, Shiyu Wang, Liaomo Zheng, Xiaokang Yang, and Wenjun Zeng. Disentangled world models: Learning to transfer semantic knowledge from distracting videos for reinforcement learning. In _ICCV_ , 2025. 

- Yuqi Wang, Xinghang Li, Wenxuan Wang, Junbo Zhang, Yingyan Li, Yuntao Chen, Xinlong Wang, and Zhaoxiang Zhang. Unified vision-language-action model. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL `https://openreview.net/forum?id=PklMD8PwUy` . 

- Zhuo Xu, Hao-Tien Lewis Chiang, Zipeng Fu, Mithun George Jacob, Tingnan Zhang, Tsang-Wei Edward Lee, Wenhao Yu, Connor Schenck, David Rendleman, Dhruv Shah, et al. Mobility vla: Multimodal instruction navigation with long-context vlms and topological graphs. In _8th Annual Conference on Robot Learning_ , 2024. 

- Yandan Yang, Shuang Zeng, Tong Lin, Xinyuan Chang, Dekang Qi, Junjin Xiao, Haoyun Liu, Ronghan Chen, Yuzhi Chen, Dongjie Huo, et al. Abot-m0: Vla foundation model for robotic manipulation with action manifold learning. _arXiv preprint arXiv:2602.11236_ , 2026. 

- Yijun Yang, Zhao-Yang Wang, Qiuping Liu, Shuwen Sun, Kang Wang, Rama Chellappa, Zongwei Zhou, Alan Yuille, Lei Zhu, Yu-Dong Zhang, et al. Medical world model. In _ICCV_ , 2025a. 

- Yuncong Yang, Jiageng Liu, Zheyuan Zhang, Siyuan Zhou, Reuben Tan, Jianwei Yang, Yilun Du, and Chuang Gan. Mindjourney: Test-time scaling with world models for spatial reasoning. _arXiv preprint arXiv:2507.12508_ , 2025b. 

- Xuan Yao, Junyu Gao, and Changsheng Xu. Navmorph: A self-evolving world model for vision-and-language navigation in continuous environments. In _ICCV_ , 2025. 

16 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

- Angen Ye, Boyuan Wang, Chaojun Ni, Guan Huang, Guosheng Zhao, Hao Li, Hengtao Li, Jie Li, Jindi Lv, Jingyu Liu, et al. Gigaworld-policy: An efficient action-centered world–action model. _arXiv preprint arXiv:2603.17240_ , 2026a. 

- Seonghyeon Ye, Yunhao Ge, Kaiyuan Zheng, Shenyuan Gao, Sihyun Yu, George Kurian, Suneel Indupuru, You Liang Tan, Chuning Zhu, Jiannan Xiang, Ayaan Malik, Kyungmin Lee, William Liang, Nadun Ranawaka, Jiasheng Gu, Yinzhen Xu, Guanzhi Wang, Fengyuan Hu, Avnish Narayan, Johan Bjorck, Jing Wang, Gwanghyun Kim, Dantong Niu, Ruijie Zheng, Yuqi Xie, Jimmy Wu, Qi Wang, Ryan Julian, Danfei Xu, Yilun Du, Yevgen Chebotar, Scott Reed, Jan Kautz, Yuke Zhu, Linxi "Jim" Fan, and Joel Jang. World action models are zero-shot policies, 2026b. URL `https://arxiv.org/abs/2602.15922` . 

- Tenny Yin, Zhiting Mei, Tao Sun, Ola Sho, Anirudha Majumdar, Emily Zhou, Jeremy Bao, Miyu Yamane, and Lihan Zha. WoMAP: World models for embodied open-vocabulary object localization. In _9th Annual Conference on Robot Learning_ , 2025. URL `https://openreview.net/forum?id=KXzkAje2uQ` . 

- Tianyuan Yuan, Zibin Dong, Yicheng Liu, and Hang Zhao. Fast-wam: Do world action models need test-time future imagination? _arXiv preprint arXiv:2603.16666_ , 2026. 

- Yang Yue, Yulin Wang, Haojun Jiang, Pan Liu, Shiji Song, and Gao Huang. Echoworld: Learning motion-aware world models for echocardiography probe guidance. In _CVPR_ , 2025. 

- Wenyao Zhang, Hongsi Liu, Zekun Qi, Yunnan Wang, XinQiang Yu, Jiazhao Zhang, Runpei Dong, Jiawei He, He Wang, Zhizheng Zhang, Li Yi, Wenjun Zeng, and Xin Jin. DreamVLA: A vision-language-action model dreamed with comprehensive world knowledge. In _The Thirty-ninth Annual Conference on Neural Information Processing Systems_ , 2025. URL `https://openreview.net/forum?id=PK07eretkF` . 

- Guosheng Zhao, Chaojun Ni, Xiaofeng Wang, Zheng Zhu, Xueyang Zhang, Yida Wang, Guan Huang, Xinze Chen, Boyuan Wang, Youyi Zhang, Wenjun Mei, and Xingang Wang. Drivedreamer4d: World models are effective data machines for 4d driving scene representation. In _CVPR_ , 2025a. 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, et al. Cot-vla: Visual chain-of-thought reasoning for vision-language-action models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2025b. 

- Haoyu Zhen, Qiao Sun, Hongxin Zhang, Junyan Li, Siyuan Zhou, Yilun Du, and Chuang Gan. Learning 4d embodied world models. In _ICCV_ , 2025. 

- Jinliang Zheng, Jianxiong Li, Zhihao Wang, Dongxiu Liu, Xirui Kang, Yuchun Feng, Yinan Zheng, Jiayin Zou, Yilun Chen, Jia Zeng, Tai Wang, Ya-Qin Zhang, Jingjing Liu, and Xianyuan Zhan. X-VLA: Soft-prompted transformer as scalable cross-embodiment vision-language-action model. In _The Fourteenth International Conference on Learning Representations_ , 2026. URL `https://openreview.net/forum?id=kt51kZH4aG` . 

- Yu Zheng, Boyang Gong, Fanye Kong, Yueqi Duan, Bingyao Yu, Wenzhao Zheng, Lei Chen, Jiwen Lu, and Jie Zhou. Learning counterfactually decoupled attention for open-world model attribution. In _ICCV_ , 2025. 

- Zhongyi Zhou, Yichen Zhu, Xiaoyu Liu, et al. Chatvla-2: Vision-language-action model with open-world reasoning. In _Advances in Neural Information Processing Systems (NeurIPS)_ , 2025. 

- Chuning Zhu, Raymond Yu, Siyuan Feng, Benjamin Burchfiel, Paarth Shah, and Abhishek Gupta. Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets. _arXiv preprint arXiv:2504.02792_ , 2025. 

- Brianna Zitkovich, Tianhe Yu, Sichun Xu, Peng Xu, Ted Xiao, Fei Xia, Jialin Wu, Paul Wohlhart, Stefan Welker, Ayzaan Wahid, Quan Vuong, Vincent Vanhoucke, Huong Tran, Radu Soricut, Anikait Singh, Jaspiar Singh, Pierre Sermanet, Pannag Sanketi, Grecia Salazar, Michael Ryoo, Krista Reymann, Kanishka Rao, Karl Pertsch, Igor Mordatch, Henryk Michalewski, Yao Lu, Sergey Levine, Edward Tsang-Wei Lee, Lisa Lee, Isabel Leal, Yuheng Kuang, Dmitry Kalashnikov, Ryan Julian, Nikhil Joshi, Alex Irpan, Brian Ichter, Jasmine Hsu, Alexander Herzog, Karol Hausman, Kehang Han, Keerthana Gopalakrishnan, Montserrat Gonzalez Arenas, Chuyuan Fu, Pete Florence, Chelsea Finn, Avinava Dubey, Danny Driess, Tianli Ding, Krzysztof Choromanski, Xi Chen, Yevgen Chebotar, Justice Carbajal, Noah Brown, and Anthony Brohan. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , volume 229 of _Proceedings of Machine Learning Research_ , pages 2165–2183. PMLR, 2023. 

17 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

## **Appendix** 

## **A RoboTwin 2.0-Plus Benchmark** 

To systematically evaluate the robustness of world action models under controlled perturbations, we extend the RoboTwin 2.0 [Chen et al., 2025a] benchmark with LIBERO-Plus-style [Fei et al., 2025] perturbation categories. We call this extended benchmark **RoboTwin 2.0-Plus** . It covers **7 perturbation dimensions** and **21 sub-dimensions** , applied to all 50 RoboTwin 2.0 dual-arm tasks. 

### **A.1 Perturbation Taxonomy** 

Table 6 enumerates all 21 sub-dimensions. Each sub-dimension is individually configurable via YAML flags, enabling both combined and ablation-style evaluation. 

### **A.2 Evaluation Protocol** 

A full RoboTwin 2.0-Plus evaluation requires **8 configs** per task: 1 clean baseline + 7 perturbation branches (Table 7). Each branch activates exactly one perturbation dimension while keeping all others at their default (clean) values, isolating the effect of each dimension on policy performance. Each config runs 50 episodes per task. 

### **A.3 Sub-dimension Details** 

**Sensor Noise (N1–N5).** One of five noise types is applied per episode, cycled deterministically by episode index: **N1** motion blur (oriented Gaussian kernel), **N2** Gaussian blur (isotropic), **N3** zoom blur (multi-scale warp accumulation around the image center), **N4** fog (homogeneous white fog with exponential transmittance), and **N5** glass blur (random pixel displacement with iterative Gaussian smoothing). Noise severity is sampled uniformly in [2 _,_ 3] per episode. All corruptions are applied to RGB observations at render time for both head and wrist cameras. 

**Lighting. L1** (diffuse color): a strong per-channel RGB tint _∈_ [0 _._ 0 _,_ 3 _._ 5] is sampled and applied to all directional and point light sources; always active. **L2** (direction): the primary directional light is re-oriented via spherical coordinates ( _θ_ , _ϕ_ ), with a 35% chance of dramatic side-lighting ( _θ ∈_ [68<sup>_◦_</sup> _,_ 82<sup>_◦_</sup> ]); activated jointly with **L4** (shadows): directional light shadow casting is toggled on/off (50% per episode). **L3** (specular): specular strength _∈_ [0 _._ 3 _,_ 6 _._ 0] and shininess _∈_ [10 _,_ 250] are applied to all scene actor materials (50% chance per episode). 

**Camera Viewpoints.** Applied to the head camera only. **C1** (distance): viewing distance is scaled by a factor _∈_ [0 _._ 85 _,_ 1 _._ 0]. **C2** (spherical position): azimuth and elevation are perturbed by up to _±_ 10<sup>_◦_</sup> with _±_ 10% distance variation; disabled by default in the evaluation config but can be enabled via a YAML flag for ablation. **C3** (orientation): yaw, pitch, and roll are independently perturbed in [0<sup>_◦_</sup> _,_ 5<sup>_◦_</sup> ] with random sign. 

**Robot Initial States.** Gaussian noise with std = 0 _._ 1 rad (clipped to _±_ 0 _._ 225 rad per joint) is added to the home joint angles of both arms. Additionally, each gripper is set to an extreme position (0.05 or 0.95) with probability 0.25. 

**Background. B1** (scene theme): in addition to the upstream texture swap, a random per-channel RGB multiplier _∈_ [0 _._ 4 _,_ 1 _._ 8] is applied to the wall color, and the floor receives an independent random color. **B2** (surface appearance): the table material is randomized with metallic _∈_ [0 _._ 0 _,_ 0 _._ 8], roughness _∈_ [0 _._ 05 _,_ 0 _._ 95], and a per-channel color tint _∈_ [0 _._ 4 _,_ 1 _._ 8]. 

**Objects Layout. O1** (distractor objects): the number of task-irrelevant objects placed on the table is sampled uniformly from [3 _,_ 15] per episode, replacing the upstream fixed count of 10. **O2** (target pose): after scene initialization, task-relevant objects receive Gaussian position noise ( _σ_ = 2 cm in _x_ and _y_ ; _z_ unchanged) and uniform yaw rotation up to _±_ 15<sup>_◦_</sup> . 

**Language Instructions.** 2,500 pre-generated instruction variants (50 tasks _×_ 50 variants) are stored as JSON files. In the combined config, each episode samples one variant: **R1** (distraction, _∼_ 30%) wraps the original instruction in irrelevant conversational context; **R2** (common-sense rewording, _∼_ 50%) replaces object names with functional descriptions and uses verb synonyms; **R3** (reasoning chain, _∼_ 20%) rewrites the imperative instruction as a goal-state or outcome description. Individual R2-only and R3-only configs are provided for ablation studies. 

18 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 6: **RoboTwin 2.0-Plus perturbation taxonomy.** All 21 sub-dimensions across 7 LIBERO-Plus dimensions, with implementation-level parameter details. 

|**Dimension**|**Code**|**Sub-dimension**|**Implementation Details**|
|---|---|---|---|
||N1|Motion blur|Gaussian kernel (_r ∈_[3_,_15],_σ ∈_[1_,_8]), rotated by ran-<br>dom angle_∈_[_−_30<sup>_◦_</sup>_,_30<sup>_◦_</sup>]|
|Sensor Noise|N2|Gaussian blur|Isotropic Gaussian (_σ ∈_[1_,_10])<br>|
||N3|Zoom blur|Multi-scale warp accumulation (_s ∈_[1_._0_,_1_._56], step _∈_<br>[0_._01_,_0_._03])<br>|
||N4|Fog|Homogeneous white fog with transmittance_e_<sup>_−αd_ </sup>(_α ∈_<br>[0_._3_,_1_._5],_d_=3)|
||N5|Glass blur|Pixel displacement (_δ ∈_[1_,_5] px) + Gaussian (_σ ∈_<br>[0_._5_,_2_._5]), 1–3 iterations|
||L1|Diffuse color|Per-channel RGB tint_∈_[0_._0_,_3_._5]applied to all directional<br>d i lih l|
|Light Conditions|L2|Direction|an pont gts (aways on)<br>Spherical re-sampling: _θ ∈_[8<sup>_◦_</sup>_,_82<sup>_◦_</sup>],_ϕ ∈_[0_,_2_π_]; 35%<br>chance of dramatic side lighting (_θ ∈_[68<sup>_◦_</sup>_,_82<sup>_◦_</sup>]). Linked<br>with L4|
||L3|Specular|Material specular strength _∈_<br>[0_._3_,_6_._0], shininess _∈_<br>[10_,_250]; applied to all scene actors (50% chance per<br>episode)|
||L4|Shadows|Directional light shadow on/off (50% chance);<br>co-<br>activated with L2|
||C1|Distance|Distance scaling _∈_[0_._85_,_1_._0]_×_ original (head camera<br>|
|Camera Viewpoints|C2<br>C3|Spherical position<br>Orientation|only)<br>Azimuth/elevation perturbation (_±_10<sup>_◦_</sup>) +_±_10%distance<br>variation (disabled by default)<br>Yaw/pitch/roll each_∈_[0<sup>_◦_</sup>_,_5<sup>_◦_</sup>]with random sign|
|Robot Init States|–|Joint perturbation|Gaussian noise (std = 0_._1rad, clip _±_0_._225rad) on all<br>joints of both arms; gripper set to extreme (0.05 or 0.95)<br>with_p_=0_._25|
|Background Textures|B1<br>B2|Scene theme<br>Surface appearance|Wall + floor RGB color tint, per-channel multiplier _∈_<br>[0_._4_,_1_._8]; combined with upstream texture swap<br>Table material:<br>metallic _∈_<br>[0_._0_,_0_._8], roughness _∈_<br>[0_._05_,_0_._95], per-channel color tint_∈_[0_._4_,_1_._8]|
|Objects Layout|O1|Distractor objects|Variable count per episode (3–15 objects, vs. fixed 10 in<br>upstream)|
||O2|Target pose|Position: Gaussian noise (_σ_=2cm, x/y only); orientation:<br>uniform yaw_±_15<sup>_◦_</sup>|
|Language Instructions|R1|Distraction|Irrelevant conversational wrapping (_∼_30%of combined<br>episodes)|
||R2|Common-sense rewording|Object names_→_functional descriptions, verb synonyms<br>(_∼_50%)|
||R3|Reasoning chain|Imperative_→_goal-state / outcome description (_∼_20%)|
|_Total: 7 dimensions, 21_|_sub-dime_|_nsions implemented; 20/21 a_|_ctive by default (C2 disabled to avoid instability)_|


## **B Benchmark comparison** 

19 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 7: **RoboTwin-Plus evaluation configs.** The 8 required configs for a complete robustness evaluation. 

|**#**|**Config**|**Perturbation**|**Active Sub-dims**|
|---|---|---|---|
|0|`demo_clean`|None (clean baseline)|–|
|1|`demo_vision_noise`|Sensor Noise|N1–N5 (cycled)|
|2|`demo_light`|Lighting|L1 (always) + L2/L3/L4 (stochastic)|
|3|`demo_camera`|Camera Viewpoints|C1 + C3 (C2 disabled by default)|
|4|`demo_robot_state`|Robot Initial State|Joint noise + gripper extremes|
|5|`demo_background_plus`|Background|B1 (texture + color tint) + B2|
|6|`demo_objects_plus`|Objects Layout|O1 (variable count) + O2 (pose)|
|7|`demo_language_plus`|Language|R1 + R2 + R3 (combined)|


Table 8: **Benchmark comparison** between LIBERO-Plus and RoboTwin 2.0-Plus. 

|Aspect|LIBERO-Plus|RoboTwin 2.0-Plus|
|---|---|---|
|Simulator|MuJoCo (robosuite)|SAPIEN (ManiSkill3)|
|Robot|Franka Panda (7-DoF)|Aloha-AgileX (14-DoF)|
|Arms|Single arm|Dual arm (bimanual)|
|Cameras|2 (third-person + wrist)|3 (head + 2 wrist)|
|Image resolution|256_×_256|320_×_240|
|Native action space|7-dim delta EEF|14-dim joint positions|
|Control mode|OSC (delta EE pose)|Joint position control|
|Control frequency|10 Hz|25–30 Hz|
|Base tasks|40 (4 suites_×_10)|50 collaborative tasks|
|Training demos|50 per task|50 clean + 500 randomized|
|Total trajectories|22,400|27,500|
|Distractor objects|416|731 (147 categories)|


## **C Comparison of Evaluated Models** 

Table 9: **Model setup comparison.** Action representation, dimensionality, chunk size, and control frequency for each evaluated model. Entries marked with “–” indicate values inherited from the base model or not explicitly specified. Unless noted, models on LIBERO follow the native axis-angle rotation convention. 

|Model|Action Repr.|Dim|Chunk|Freq|
|---|---|---|---|---|
|_VLA Models_|||||
|Pi0|Delta EEF|7|50|50 Hz|
|Pi0-FAST|Delta EEF (FAST tokenized)|7|50|15–50 Hz|
|Pi0.5|Absolute EEF / joints|18–19|50|50 Hz|
|OpenVLA-OFT|Delta EEF|7|8|3–10 Hz|
|UniVLA|Delta EEF (DCT tokenized)|7|10|–|
|RIPT-VLA|Delta EEF (inherited)|7|8|–|
|xVLA|Absolute EEF (6D rot.)|10/20|32|–|
|VLA-JEPA|Delta EEF|7|7|–|
|MOTUS|Latent (optical flow)|14|48|30 Hz|
|_World Action Mo_|_dels_||||
|GE-Act|Absolute EEF (Euler)|7/14|54|30 Hz|
|Cosmos-Policy|Latent-frame + native|7/14|16|–|
|LingBot-VA|Absolute EEF (quat.) + joints|30|4|50 Hz|


We evaluate both VLA models and WAMs. The action representation and control details of each model are summarized in Table 9. On the VLA side, **Pi0** Black et al. [2025b] and **Pi0-FAST** use delta end-effector control with axis-angle rotation and generate 50-step action chunks via flow matching and FAST tokenization, respectively. **Pi0.5** [Black et al., 2025a] extends Pi0 to predict absolute target poses with 50-step chunks at 50 Hz, and supports both end-effector and joint-space control depending on the platform. **OpenVLA-OFT** [Kim et al., 2025] follows the native 7-dim delta end-effector convention on LIBERO with an action chunk size of 8, and **RIPT-VLA** inherits its action space from 

20 

**Do World Action Models Generalize Better than VLAs? A Robustness Study** 

Table 10: Detailed LIBERO-Plus results for each task suite. **Lang.** : Language. **BG** : Background. The Fast-WAM LIBERO checkpoint was trained on clean demonstrations only, whereas its RoboTwin checkpoint was trained on clean + domain-randomized demonstrations (cf. **RQ 2** ). 

|Category|Model|Camera|Robot|Lang.|Light|BG|Noise|Layout|Total|
|---|---|---|---|---|---|---|---|---|---|
||_π_0|70.7|49.1|67.9|92.8|95.0|87.7|94.0|78.6|
||_π_0_._5|76.9|85.4|90.3|97.6|95.3|91.7|97.7|90.3|
||X-VLA|24.5|91.4|82.1|100.0|100.0|63.5|93.8|77.7|
|Spatial|VLA-JEPA|74.2|71.7|96.1|97.9|99.6|77.8|95.3|86.9|
||GE-Act|72.3|75.7|90.8|100.0|89.1|97.7|89.6|87.5|
||Cosmos-policy|81.1|59.7|88.2|89.0|91.1|98.0|99.2|86.6|
||Fast-WAM|14.4|44.0|69.5|87.3|69.8|35.0|60.5|54.4|
||_π_0|80.1|31.9|75.4|94.3|85.9|87.9|76.2|74.7|
||_π_0_._5|91.4|70.6|92.4|98.7|98.0|95.5|88.6|90.0|
||X-VLA|19.7|97.2|90.7|92.6|98.4|51.4|55.6|69.3|
|Object|VLA-JEPA|69.2|57.8|90.8|100.0|100.0|75.1|87.3|81.0|
||GE-Act|81.3|83.4|83.6|98.3|94.8|97.2|79.7|87.7|
||Cosmos-policy|88.4|61.6|81.9|100.0|96.4|94.3|87.1|86.2|
||Fast-WAM|25.3|64.1|96.3|97.9|77.8|63.7|73.0|71.2|
||_π_0|56.6|43.3|43.2|90.3|84.7|82.8|59.8|63.4|
||_π_0_._5|80.1|80.2|71.5|98.6|92.9|94.2|71.1|82.7|
||X-VLA|27.2|90.2|58.8|95.7|97.9|67.5|61.2|68.7|
|Goal|VLA-JEPA|72.3|73.1|75.3|89.9|94.3|69.9|68.7|76.3|
||GE-Act|52.5|71.9|46.3|93.9|87.2|83.4|68.9|70.0|
||Cosmos-policy|75.7|64.1|67.6|99.6|95.0|91.6|56.2|76.4|
||Fast-WAM|8.1|24.7|49.8|75.3|44.5|23.7|48.0|39.2|
||_π_0|38.7|39.9|69.7|79.2|72.3|64.6|77.6|61.3|
||_π_0_._5|54.2|74.8|89.8|92.7|92.7|78.8|87.2|79.9|
||X-VLA|22.2|79.9|71.3|95.6|94.5|68.2|76.6|69.9|
|Long|VLA-JEPA|42.5|68.5|90.9|78.4|81.3|44.3|86.2|67.9|
||GE-Act|38.9|77.1|91.4|90.5|74.4|86.0|84.6|76.6|
||Cosmos-policy|59.2|67.4|89.8|97.4|74.7|88.0|91.7|80.2|
||Fast-WAM|17.7|45.3|60.1|52.2|22.8|28.5|61.2|41.1|


the OpenVLA-OFT base model. **UniVLA** tokenizes native actions via DCT (FAST tokenizer) with a chunk size of 10 on LIBERO. **xVLA** [Zheng et al., 2026] is notable for employing a unified absolute end-effector representation with 6D rotation across all benchmarks, outputting 10-dim per arm (padded to 20-dim for dual-arm), with a chunk size of 32. **VLA-JEPA** [Sun et al., 2026] predicts delta end-effector actions with axis-angle rotation using a conditional flow-matching action head and a prediction horizon of 7 steps. 

On the WAM side, **Cosmos-Policy** [Kim et al., 2026] encodes actions as latent frames within its video diffusion process, using the native 7-dim action space on LIBERO with a chunk size of 16. **GE-Act** [Liao et al., 2025] predicts absolute end-effector poses with Euler angle rotation and generates 54-step action trajectories via a lightweight flow-matching decoder at 30 Hz. **MOTUS** [Bi et al., 2025] takes a fundamentally different approach by operating in a learned 14-dimensional latent action space derived from optical flow, which is mapped to robot-specific commands during fine-tuning, with a chunk size of 48 at 30 Hz. **LingBot-VA** [Li et al., 2026b] uses a 30-dimensional representation combining absolute end-effector poses (with quaternion rotation) and joint angles for both arms, with a compact chunk size of 4 at 50 Hz. 

### **C.1 Detailed LIBERO-Plus Results** 

21 

