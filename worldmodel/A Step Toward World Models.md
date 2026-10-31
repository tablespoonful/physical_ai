---
title: "A Step Toward World Models: A Survey on Robotic Manipulation"
date: "2025-10-31"
authors: "Peng-Fei Zhang; Ying Cheng; Xiaofan Sun; Shijie Wang; Fengling Li; Lei Zhu"
url: https://arxiv.org/abs/2511.02097
pdf: https://arxiv.org/pdf/2511.02097
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.02097)** / [論文ページ](https://arxiv.org/abs/2511.02097)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

1 

# A Step Toward World Models: A Survey on Robotic Manipulation 

Peng-Fei Zhang, Ying Cheng, Xiaofan Sun, Shijie Wang, Fengling Li, Lei Zhu, Heng Tao Shen 

**_Abstract_ —Autonomous agents are increasingly expected to operate in complex, dynamic, and uncertain environments, performing tasks such as manipulation, navigation, and decision-making. Achieving these capabilities requires agents to understand the underlying mechanisms and dynamics of the world, moving beyond reactive control or simple replication of observed states. This motivates the development of world models as internal representations that encode environmental states, capture dynamics, and support prediction, planning, and reasoning. Despite growing interest, the definition, scope, architectures, and essential capabilities of world models remain ambiguous. In this survey, we go beyond prescribing a fixed definition and limiting our scope to methods explicitly labeled as world models. Instead, we examine approaches that exhibit the core capabilities of world models through a review of methods in robotic manipulation. We analyze their roles across perception, prediction, and control, identify key challenges and solutions, and distill the core components, capabilities, and functions that a fully realized world model should possess. Building on this analysis, we aim to motivate further development toward generalizable and practical world models for robotics.** **_This is an initial version of the survey. The content will be expanded and refined in future updates._** 

**_Index Terms_ —World Model; Robotic Manipulation.** 

CONTENTS 

|**I**|**Introdu**|**ction**|1|
|---|---|---|---|
|**II**|**Prelimi**|**naries**|3|
||II-A|What Is the “World” to Be Modeled? .|3|
||II-B|World Models Empowering Robot In-||
|||telligence . . . . . . . . . . . . . . . . .|3|
||II-C|Competing Perspectives on World Models|3|
||II-D|Revisiting Modern AI Models Through||
|||the Lens of World Modeling . . . . . .|3|
|**III**|**Overvi**|**ew of World Models**|5|
||III-A|Paradigms . . . . . . . . . . . . . . . .|5|
||III-B|Architectural Design. . . . . . . . . . .|7|
||III-C|World Observation and Representation .|7|
||III-D|Task Scope . . . . . . . . . . . . . . . .|8|
|**IV**|**Functio**|**ns of World Models**|9|
||IV-A|Decision Support<br>. . . . . . . . . . . .|9|
||IV-B|Training Facilitation . . . . . . . . . . .|11|
|**V**|**Key Te**|**chniques and Notable Challenges**|12|
||V-A|Data Limitations . . . . . . . . . . . . .|12|
||V-B|Perception and Representation<br>. . . . .|13|
||V-C|Long-horizon Reasoning<br>. . . . . . . .|14|


School of Computer Science and Technology, Tongji University. 

|V-D|Spatiotemporal Consistency . . .|. . . .|15|
|---|---|---|---|
|V-E|Generalization . . . . . . . . . .|. . . .|15|
|V-F|Physics-informed Learning . . .|. . . .|16|
|V-G|Memory<br>. . . . . . . . . . . . .|. . . .|16|
|V-H|Other Techniques and Challenges|. . .|17|


|**VI**|**Towards Defining Core Components and Capa-**||
|---|---|---|
|**bilitie**|**s of World Models**|17|
|**VII**|**Dataset**|18|
|**VIII**|**Conclusion and Future research directions**|18|
||VIII-A<br>Conclusion . . . . . . . . . . . . . . . .|18|
||VIII-B<br>Future research directions . . . . . . . .|19|
|**Refer**|**ences**|20|


## I. INTRODUCTION 

“ _If I have seen further, it is by standing on the shoulders of giants_ .” — Isaac Newton 

Autonomous agents are designed to extend human capabilities, assisting in tasks that are dangerous, repetitive, or demand high precision, thereby enhancing productivity across diverse applications. Robots serve as their physically embodied form, aiming to realize seamless interaction with the physical world. Achieving such capabilities requires agents to move beyond reactive control and the mere imitation of observed behaviors, instead developing the ability to model, reason about, and predict environmental dynamics. In this context, world models have emerged as powerful internal representations that enable robots to anticipate future outcomes, plan effectively, and ultimately act intelligently in the real world. Richens _et al._ [1] argue that any agent capable of generalizing to solve multi-step tasks must implicitly learn a predictive model of its environment, e.g., a world model. 

The concept of “world models” in computer science dates back to the 1960s [2], and numerous methods have since been proposed toward more capable models [3], [4], [5], [6], [7], [8], [9], [10], though not all explicitly identify as world models. For example, Wang _et al._ [9], [10], [5], [6], [7], [8] leverage video generation models as a form of world models, which encode extensive world knowledge from largescale training data and can predict future states based current observations and/or actions. LeCun _et al._ [11], [12], [13], [14], [15] emphasizes modeling abstract world state representations, while Zitkovich _et al._ [16], [17], [18] utilize vision-languageaction models (VLA) models that do not explicitly generate future states. The scope of existing methods varies from 2D 

2 


Fig. 1. Conceptual flow of the survey. The survey aims to clarify the motivation behind world modeling, explore its essential scope and development, and illuminate pathways toward more general and capable world models. 

scene prediction to 4D world modeling [19], [20], [21], [22], [23], [24], reflecting different understandings of what it means to model the world. The observation viewpoint of the world includes both third-person (exocentric) [21], [25], [26] and first-person (egocentric) [27], [28] perspectives. 

World models play a critical role in robotic learning in two ways. They allow robots to improve autonomous policies by the internal prediction and simulation of environmental dynamics, future states, and/or action outcomes [29], [12], [13], [14], [30], [21]. They also support scalable policy training and evaluation by generating realistic rollouts and physical interactions [16], [31], [32], [33], [34], [35]. From a functional standpoint, current approaches range from singlepurpose models, such as those for visual planning [30], [36], future-scene generation [37], [33], [38], or action prediction [39], to more integrated systems that couple multiple abilities within a unified framework [40], [27], [41], [42], [43]. 

_These variations indicate that the notion of a world model remains unsettled, with its conceptual, architectural, and functional boundaries not yet clearly defined._ 

Addressing these questions requires standing on the shoulders of prior contributions, carefully analyzing existing methodologies to gain inspiration for elucidating the boundaries of world models. In this survey, rather than hastily defining what constitutes a world model, we provide a comprehensive review of the literature, highlighting their core principles, architectures, and functional roles in enabling intelligent robotic systems. We extend the scope beyond works explicitly labeled as world models, examining their core principles and outlining pathways for constructing practical models that can drive the development of general and adaptive robotic agents. 

This survey is organized around a set of guiding questions designed to provoke thought and provide inspiration. Readers can explore the survey with these questions in mind, using them to provoke thought, gain inspiration, and reflect on the challenges and opportunities in developing world models for robotic manipulation. 

- _What is the world model and its conceptual, architectural, and functional boundaries?_ 

- _How should the world be sensed and presented?_ 

- _What level of model fidelity and coverage is required to reliably support robotic tasks?_ 

- _Is it necessary to learn a world model, given the complexity, resource demands, and potential challenges involved?_ 

- _How far are current world models from fully realized world models?_ 

- _Is human cognition [44], [45] the ultimate goal for world models?_ 

The main contributions of this survey are as follows: 

- **Comprehensive taxonomy of world model architectures.** We provide a systematic categorization of existing designs, including latent space modeling methods, video generation-based models, direct projection based (implicit modeling) methods and other emerging structures. 

- **Functional analysis.** We discuss diverse roles of world models in robotic manipulation, including action prediction and planning, robotic learning, and evaluation, highlighting their contribution to intelligent manipulation. 

- **Capability framework.** We analyze the essential abilities that a world model should possess, such as perception, prediction, imagination, and interaction, aiming to clarify what constitutes a generalizable and capable world model. 

3 

- **Challenges and future directions.** We summarize key challenges, including long-horizon reasoning, physical awareness, and generalization, and discuss potential research directions and solutions toward building practical, real-world models. 

**Related Surveys.** Our survey differs substantially from existing reviews. Several prior surveys have examined world models in robotics, but most focus on specific aspects and provide limited conceptual analysis. For example, Yu _et al._ [46] emphasize video generation, Kong _et al._ [47] cover 3D/4D world modeling, Ai _et al._ [48] study dynamics learning, and Lin _et al._ [49] address physics cognition. Long _et al._ [50] review architectures and functional roles of world models, whereas Zhu _et al._ [51], [52], [53] primarily compile representative works. While these surveys provide valuable overviews, they offer limited discussion of the essential characteristics and functional requirements of comprehensive world models. In contrast, our survey presents a holistic, problem-centered perspective, highlighting key challenges, solution strategies, and future directions for world modeling in robotics. 

**Paper Organization.** The remainder of this paper is organized as follows. Section II introduces the conceptual foundations of world models. Section III provides an overview of current world models, including their learning paradigms, structural designs, representations of the world, and task scopes. Sections IV and V describe the key functions of existing world models and summarize the principal techniques and challenges, respectively. Section VII reviews the major training resources used in world-model research. Section VI then summarizes the fundamental components and capabilities of world models based on this review, followed by Section VIII, which presents conclusions and outlines future research directions. Although this may occasionally lead to some repetition, certain key ideas are revisited throughout the paper to aid understanding and reinforce their conceptual connections. 

## II. PRELIMINARIES 

## _A. What Is the “World” to Be Modeled?_ 

Despite the debate among philosophers about the ultimate nature of the world, the world can be roughly described as a set of entities, each with its own attributes or properties, along with the relationships and interactions that connect them. These attributes, such as shape, size, material, or state, and the connections, can be spatial, causal, functional, or temporal. As a result, objects, agents, and features are not only statically arranged but also evolve and influence one another over time. In order to interact effectively with such a world, an intelligent agent must capture critical information about entities, their properties, and their interactions across spatial and temporal dimensions. Collectively, these entities and interactions form a rich and dynamic environment in which an agent must actively explore, interact, and learn to achieve its goals. This naturally raises the question of what fundamental capabilities underpin an agent’s ability to capture and reason about such complex dynamics, as well as what forms of representation, learning, and interaction are required to model and act within an uncertain and evolving world. 

## _B. World Models Empowering Robot Intelligence_ 

Embodied intelligence refers to a system’s ability to perceive, reason, and learn through direct interaction with its environment. Unlike traditional AI confined to abstract or symbolic domains, embodied intelligence integrates a physical body, sensors, actuators, and computational processes that jointly enable situated perception, reasoning, and action. Intelligent robotic agents serve as the primary physical instantiation of embodied intelligence. They inherently combine perception (via sensors), cognition (for learning and reasoning), and motor control (via actuators) to operate autonomously and acquire knowledge from real-world experience, much like biological organisms. 

However, because intelligent agents perceive only a partial and noisy projection of reality through their sensors, many underlying relationships and causal dependencies remain latent. This limitation makes structured internal representations essential for prediction, planning, and multi-step reasoning. To achieve robust and efficient embodied intelligence, recent research introduces the notion of the “world model”, which serve as internal representations that capture environmental dynamics and common-sense regularities of how the world operates. By internally simulating potential outcomes, world models empower embodied agents to understand their context, anticipate the consequences of actions, and plan complex behaviors before execution, thereby reducing reliance on costly or unsafe real-world trial and error. 

## _C. Competing Perspectives on World Models_ 

Although the concept of the “world model” is prevalent in computer science, its definition remains unsettled, with ongoing debate in the research community regarding its fundamental nature and role in intelligence [80]. A central point of contention concerns its generative capability, as illustrated by NVIDIA [81], who define world models as systems that learn environmental dynamics from multimodal data and generate videos capturing spatial and physical properties. Emphasizing action dependence, Sudhakar _et al._ [37], [40] characterize world models specifically as action-conditioned video generation models, distinguishing them from conventional video prediction. Similarly, Hafner _et al._ [14], [12], [13], [15], [82] identify action-conditioned prediction as a core feature of world models, emphasizing the prediction of latent representations rather than raw observations. Despite these differing perspectives, a common consensus emerges: world models aim to construct internal representations that capture environmental dynamics and action consequences, thereby enabling the prediction of future states. 

## _D. Revisiting Modern AI Models Through the Lens of World Modeling_ 

The rapid progress of large-scale artificial intelligence models has blurred the boundaries between traditional task-specific learning and general world modeling. Although many of these models are not explicitly designed as world models, they exhibit key characteristics of world modelimodelling as 

4 

TABLE I 

A SUMMARY OF REPRESENTATIVE WORLD MODELS. 

- **Prediction Tasks:** _<u>AP</u>_ <u>:</u> Action Prediction, _<u>PL</u>_ <u>:</u> Policy Learning, _<u>VP</u>_ <u>:</u> Visual Planning, _<u>Static</u>_ <u>:</u> Static Visual Prediction, _<u>Action-cond.</u>_ <u>:</u> Action-conditioned Visual Prediction. 

- **Input & Output:** _<u>L</u>_ <u>:</u> Language, _<u>V</u>_ <u>:</u> Video, _<u>A</u>_ <u>:</u> Action, _<u>S</u>_ <u>:</u> State, _<u>I</u>_ <u>:</u> Image, _<u>P</u>_ <u>:</u> Point Cloud, _<u>Tr</u>_ <u>:</u> Trajectory. 

_•_ **Core Components:** _<u>CLIP</u>_ <u>:</u> Contrastive Language-Image Pre-training, _<u>DiT</u>_ <u>:</u> Diffusion Transformer, _<u>IDM</u>_ <u>:</u> Inverse Dynamics Model, _<u>GPT</u>_ <u>:</u> Generative Pretrained Transformer, _<u>LLM</u>_ <u>: Large Language Model,</u> _<u>LSTM</u>_ <u>: Long Short-Term Memory,</u> _<u>RSSM</u>_ <u>: Recurrent State-Space Model,</u> _<u>U-Net</u>_ <u>: U-shaped Convolutional</u> Neural Network, _<u>VAE</u>_ <u>:</u> Variational AutoEncoder, _<u>VDM</u>_ <u>:</u> Video Diffusion Model, _<u>ViT</u>_ <u>:</u> Vision Transformer, _<u>VLM</u>_ <u>:</u> Vision-Language Model, _VQ_ : Vector Quantization, _<u>Ar</u>_ <u>:</u> Autoregressive. 

|**Model**|**Decisio**<br>**AP**<br>**PL**<br>**VP**|**n Support**<br>**Static**<br>**Action-cond.**|**Training Fac**<br>**Data Engine**|**ilitation**<br>**Evaluation**|**Training Data**|**Input**|**Output**|**Core Components**|
|---|---|---|---|---|---|---|---|---|
|PlaNet [29]|✓<br>✓||||V+A|V+A|A|RSSM|
|DreamerV1,V2,V3 [12], [13], [14], [15]|✓<br>✓||||V+A|V+A|A|RSSM|
|PaLM-E [54]|✓||||V+L|V+L|A|LLMs, ViTs|
|OpenVLA [55]|✓||||V+L+A|V+L|A|VLA|
|Plan2Explore [39]|✓<br>✓||||V+A|V+A|A|RSSM|
|FOCUS [25]|✓<br>✓||||V+A|V+A|A|RSSM|
|EgoAgent [27]|✓<br>✓||||V|V+A|A|JEPA|
|GR00T [44]|✓<br>✓||||V+L+A+S|V+L+A+S|A|VLA, VLM|
|THICK [56]|✓<br>✓||||V+A|V+A|A|Hierarchical, RSSM|
|DayDreamer [14]|✓<br>✓||||V+A|V+A|A|RSSM|
|RetryingVisualMPC [30]|✓|✓|||V|I|A|Registration network|
|Genie [20]|✓|✓|||V|I/V|V|VQ-VAE, VQ-VAE|
|GE [57]|✓<br>✓|✓<br>✓|✓||V + L|L+I|V, Ar|VAE, DiT, CLIP|
|GR-2 [58]|✓<br>✓|✓|✓||V|V+L+S|V+A+S, Ar|CLIP, VQGAN, GPT, condition VAE|
|UniSim [19]|✓<br>✓|✓|✓||V+L+A|V+A|V|Stable Diffusion|
|UniPi [59]|✓<br>✓|✓|||V+L|L+I|V|IDM, VDM|
|DiVA [9]|✓<br>✓|✓|||V+L|V+L|V+A|VDM, CLIP, VAE|
|WorldVLA [40]|✓<br>✓|✓|✓||V+L|V+L+A|V+A, Ar|VLA, VQ-GAN|
|iVideoGPT [6]|✓|✓||✓|V+A|V+A|V, Ar|VQ-GAN, GPT|
|DreamVLA [60]|✓<br>✓|✓|||V+L+A+S|V+L+S|A, Ar|CLIP, Masked Autoencoders, LLMs (GPT-2), DiT|
|Seer [61]|✓<br>✓|✓|||V+L+A+S|V+L+S|V+A, Ar|CLIP, ViT, GPT|
|EnerVerse [8]|✓|✓|||V+L+A|V+L|V, Ar|VAE, VDM|
|SayCan [62]|✓||||V+L+A|V+L|A|LLMs|
|FOCUS [25]|✓<br>✓|✓|✓|✓|I+A+S|I+A+S|I+A|RSSM|
|Visual MPC [63]|✓<br>✓|✓|||V+A+S|V+A+S|V+A|LSTM|
|CDNA [36]||✓|||V+A+S|V+A+S|V|LSTM|
|VisualForesight [64]|✓<br>✓|✓|✓|✓|I|V+goal(I/L)|A|LSTM|
|VLP [5]|✓|✓|✓||I+V+L+A|I+L|V+A|VLM, VDM|
|FLIP [65]|✓|✓||✓|V+L|V+L|V|CVAE, DiT, LIV|
|RoboDreamer [66]|✓|✓|✓||V+L|V+L|V|Text Parser, VDM, IDM|
|COMBO [7]|✓|✓|✓|✓|V+L+A|V+A|V+A|VDM, VLM, Tree Search|
|AVID [67]|✓|✓||✓|V+A|V+A|V|VDM, Action Adapter|
|SuSIE [68]|✓<br>✓|✓|||V+L+A|V+L|V+A|Image-Editing Diffusion Model|
|3D-VLA [41]|✓<br>✓|✓<br>✓|||V+L+A+S|V+L|V+A+P|3D-LLM, Stable Diffusion|
|AETHER [23]|✓<br>✓|✓<br>✓|||V|V+A|V|Geometric Encoding, VDM|
|TesserAct [24]|✓<br>✓|✓|✓||V+L+A|V+L|V+A|VDM|
|IRASim [43]|✓<br>✓|✓|✓||V+A|V+Tr|V, Ar|DiT|
|3DFlowAction [69]|✓<br>✓|✓|||V+L|V+L+P|Tr, Ar|VDM, CLIP|
|THICK [56]|✓<br>✓|✓|✓|✓|V+A+S|V+A|V+A+S|Context-Specific RSSM|
|FlowDreamer [21]|✓<br>✓<br>✓|✓|||V+A|V+A|V|i<br>U-Net, Stable Diffusion|
|DREMA [33]|✓|✓|✓||V+A+S|V+S|V+A|Gaussian Splatting|
|AVDC [70]|✓|✓|✓||V+L|V+L|V+Optical Flow+A|U-Net, CLIP-Text, Optical Flow Model|
|GWM [34]|✓|✓<br>✓|✓|✓|V+A|V+A|V|3D Gaussian VAE, DiT|
|Plan2Explore [39]|✓<br>✓||||V|V|A|DM, Dreamer|
|DreamGen [38]||✓|||V|V+L|V|DiT|
|UWM [71]|✓|✓|||V|V+A|V+P|IDM, DiT|
|CLOVER[22]|✓<br>✓<br>✓|✓|||V+L|V+L|V+A|ViTs, CLIP, VDM|
|Pandora [72]||✓|||V+L|V+L|V, Ar|LLM, DynamiCrafter Model|
|PAR [42]||✓|||V+L|V+L+A|V+A, Ar|3D-VAE, Phi Model, DiT, Causal Transformer|
|RoboEnvision [10]|✓|✓|||V+L|V+L|V+A|VLM, DiT|
|HMA[73]||✓|✓||V+L|V+L|V+A|VLMDiT|
|<br>WorldGym [74]||||✓|V+A|V+A|V|, <br>VLM, DiT|
|VideoWorld [75]|✓|✓|||V|V|V+A, Ar|IDM, VQ-VAE, Ar Transformer|
|PlaySlot[26]||✓|||V|V|VAr|IDMRecursiveEncoder-DecoderArTransformer|
|<br>LOReL [76]|✓|✓|||V+L|V+A|, <br>V+A|,  ,  <br>LSTM|
|V-JEPA 2 [77]|✓<br>✓|✓|||V+A|V+A|V+A|JEPA, LLM|
|UP-VLA[78]|✓|✓|||V+L|V+L|V+A+L|VLADecoder|
|<br>CoT-VLA [79]|✓|✓|||V+L|V+L|V+A|, <br>VLA, Decoder|


learning structured representations of reality, reasoning about causality, and predicting or generating plausible future states. Revisiting these modern models through the lens of world modeling provides valuable insights into how intelligence emerges from data, embodiment, and multimodal integration. This perspective helps clarify which components of contemporary architectures, such as large language models (LLMs), vision-language models (VLMs), vision-language-action models (VLAs) and video generation models, implicitly capture aspects of the world and how they contribute to the broader goal of general-purpose world understanding. 

_1) LLM, VLM & VLA_ 

The strong reasoning capabilities and next-token prediction mechanism of LLMs make them natural foundations for constructing world models, as they capture sequential dependencies, causal relationships, and abstract dynamics. When equipped with auxiliary modules such as value functions [62] or modality-specific encoders [72], [54], [60], LLMs 

can achieve a more comprehensive understanding of the environment. Moving beyond the language-centric paradigm, VLMs focus on the joint modeling of multiple modalities, providing a perceptually grounded understanding of the world [83], [84]. Furthermore, an increasing number of studies have explored augmenting VLMs with low-level action-generation capabilities, thereby transforming them into VLA [16], [85], [44] that bridge perception, reasoning, and control. In addition to action generation, there are also many work that enable additional visual prediction [78], [79]. 

From the above discussion, the designs and functions of LLMs, VLMs, and VLAs align with the spirit of world models, as they aim to represent and reason about world dynamics. Therefore, these models should not be excluded from the broader conceptual scope of world modeling. However, solely relying on LLMs, VLMs, or VLAs often constrains a system’s capacity for long-horizon prediction, reasoning, and imagination, all of which are essential for modeling dynamic and 

5 


Fig. 2. A visualization of an agent [11], where the world model predicts possible future world states as a function of imagined actions sequences proposed by the actor. 

interactive environments. Recent studies have thus begun to integrate these models into architectures that explicitly function as world models, such as the JEPA framework [27], Dreamerstyle frameworks [86], positioning them as core mechanisms for capturing temporal and causal dynamics. 

## _2) Video Generation Models_ 

Video generation models primarily aim to produce visually realistic and temporally coherent sequences, which implicitly rely on learning the underlying dynamics of the environment. They can operate on diverse modalities, including language, visual data, and action inputs, allowing them to access environmental context and imagine future scenes. These characteristics position video generation models as a form of world modeling. Indeed, many recent world models adopt video generation as their core mechanism [5], [6], [7], enabling the prediction of future states encompassing observations, actions, and environmental changes. However, most video generation models focus on observation-level prediction and may suffer from issues such as a lack of interpretable internal representations and limited causal understanding of the world. 

## Implications for Modern AI Models 

Viewing LLMs, VLMs, VLAs, and video generation models through the lens of world modeling reveals the shared objective across modern AI paradigms: constructing internal representations that capture the structure and dynamics of the world. This perspective reframes world modeling not as a separate task, but as the underlying principle driving the integration of perception, reasoning, and action in intelligent systems. 

## III. OVERVIEW OF WORLD MODELS 

_“What we observe is not nature itself, but nature exposed to our method of questioning.”_ 

— Werner Heisenberg 

## _A. Paradigms_ 

Building on the previous review of current models, contemporary architectures for capturing world dynamics can be broadly stratified along a methodological spectrum: implicit world modeling (e.g., LLMs, VLMs, and VLAs) [27], [87], [41], [85], latent dynamics modeling [14], [12], [13], [15], and video generation paradigms [6], [5], [7], [67], each targeting distinct representational granularities and predictive mechanisms. 

## _1) Implicit World Modeling_ 

Implicit World Modeling refers to the paradigm in which an agent learns to map sensory inputs (e.g., vision and language) directly to actions without constructing an explicit, disentangled representation of the environment’s states or dynamics. Representative models include LLMs, VLMs, and VLAs, which offer distinct advantages in semantic grounding, generalization, and interpretability [62], [72], [54], [60], [84]. An illustration of these models is shown in Fig. 3. At the same time, these models can be integrated into broader worldmodeling architectures to capture temporal dependencies and enable long-horizon prediction [16], [85], [44]. Detailed discussions are provided in Sections II-D1 and IV-A1. 

## _2) Latent Dynamics Modeling_ 

Latent dynamics models typically encode high-dimensional observations into compact latent states through a variational autoencoder or encoder network, and employ recurrent or transformation modules (e.g., RNNs or Transformers) to predict the temporal evolution of these latent representations [12], [13], [14], [15]. This architecture is characterized by latentspace imagination and task-oriented optimization over visual granularity, facilitating long-horizon learning by forecasting future states without the need for pixel-level reconstruction. **Recurrent State-Space Model (RSSM)** [29] resembles the structure of a partially observable Markov decision process. Its learning framework consists of three main components: an encoder, a decoder, and a dynamics model. The encoder network fuses sensory inputs (observations) _o_ together into the stochastic representations _z_ . The dynamics model learns to predict the sequence of stochastic representations by using its recurrent state _s_ . The decoder reconstructs sensory inputs to provide a rich signal for learning representations and enables human inspection of model predictions, but is not needed while learning behaviors from latent rollouts. Specifically, at time step _t_ , let the image observation be _ot_ , the action vectors _at_ and the reward _rt_ . RSSM can be formulated as the generative process of the images and rewards conditioned a hidden state sequence _st_ : 


**PlaNet** [29] first demonstrates the effectiveness of learning dynamics in a latent space. The **Dreamer** family of models (a visualization is shown in Fig. 3) [12], [13], [14], [15] further verify this paradigm and establish a representative framework 

6 


Fig. 3. An overview of world models. Implicit world models map observations and instructions directly to actions without explicitly modeling environmental dynamics. Latent-dynamics world models capture the evolution of environment dynamics within a latent space, while video-generation-based world models predict future visual scenes. 

that reduces reliance on real-world data by performing imagination directly in latent space. Dreamer enables policy learning through imagined trajectories without continuous interaction with the environment, allowing agents to simulate multi-step consequences of actions and generalize to new states, objects, and environments. 

While sharing the objective of learning predictive worldstate representations, **Joint-Embedding Predictive Architecture (JEPA)** [11], [27] and RSSM diverge fundamentally in their learning mechanisms. RSSM relies on generative reconstruction of observations to model latent dynamics, whereas JEPA (a visualization is shown in Fig. 3) employs selfsupervised predictive coding in embedding spaces, directly forecasting future state representations without decoding to raw sensory inputs. This paradigm eliminates the computational cost of pixel-level reconstruction but necessitates powerful hierarchical encoders to compress sufficient environmental information into abstract embeddings. As a result, it introduces an implicit information bottleneck that demands careful architectural balancing to preserve task-relevant features. Under the JEPA framework, Assran _et al._ [77] combine pretrained video models with an action-conditioned predictor to autoregressively predict future states and actions. 

The **MuZero** series [88], [89], [90] represent another form of latent-dynamics-based world modeling. Instead of modeling the complete environment dynamics, MuZero predicts only future quantities directly relevant to planning, such as rewards, 

values, and policies, given the complexity of real-world environments, and employs a tree-based search algorithm [91] to select optimal actions. 

## _3) Video Generation_ 

Video-based generative models are powerful tools for capturing environmental dynamics and predicting future scenes. These models operate directly on high-dimensional raw observations, such as RGB images, depth maps, or force fields, treating the environment as a sequence of frames [6], [23], [19], [20], [92], [72], [93], [66], [94]. By generating future scenes, they can support a wide range of applications, including simulation, action prediction, and visual planning [63], [64], [6], [7], [67]. Moreover, they can leverage large-scale pre-training to enhance generalization and improve sample efficiency [67], [23], [67], [9], [38]. Depending on the input modality, world models can be constructed using actionconditioned video prediction models [6], text-to-video models [5], [19], [38], [66], or trajectory-to-video models [43], [58]. 

There are several architectural families of video-based world models. Diffusion-based world models generate videos by progressively denoising random noise through multiple iterative steps. Representative examples include U-Net-based models [95], [70] and diffusion transformer (DiT)-based architectures [25], [96], [43], [97], [10]. Autoregressive world models, in contrast, predict the next token or frame conditioned on previously generated ones, effectively modeling temporal dependencies in the sequence [57], [6], [72], [8], [26], [20], 

7 

[58]. Other architectures include variational autoencoder-based models [20] and convolutional LSTMs [63], [64]. 

Autoregressive-based world models generate each step conditioned on previous outputs, allowing them to predict sequences of arbitrary length and making them well-suited for long-horizon predictions. However, they often suffer from error accumulation over extended sequences [10] and may struggle to represent highly multi-modal distributions. In contrast, diffusion-based models generate samples through an iterative denoising process, enabling them to model complex, multimodal distributions and produce globally coherent sequences. This iterative refinement also makes diffusion models more robust to individual prediction errors, resulting in better performance on tasks requiring long-horizon consistency or highquality generative outputs. On the downside, diffusion models are computationally intensive and slower during inference, and adapting them to sequential prediction requires careful conditioning. Overall, autoregressive world models tend to excel in scenarios demanding speed and accurate short-term predictions. In contrast, diffusion models are more suitable for tasks such as long-horizon prediction, where maintaining global coherence is crucial. 

Compared with implicit and latent-space world models, video generation models provide more detailed visual predictions but at a higher computational cost, lower generation speed and sample efficiency. In addition, action predictions are only proved to be align with visual future generation [73], as visual data contains relevant information to actions. 

## _B. Architectural Design_ 

## _1) Flat Architecture_ 

Most current methods adopt flat architectures [21], [25], [26], [20], [92], [72], [93], [66], which face critical limitations. They lack structured representations of the environment, resulting in poor handling of multi-scale dynamics, limited longhorizon prediction, error accumulation, and reduced generalization. Specifically, in robotic manipulation, placing fragile objects requires the robot to react instantly to unexpected slips while simultaneously planning the sequence of pickand-place actions to achieve the overall goal. Many tasks further involve long-term objectives that must be completed through sequential subgoals and temporally extended actions. For example, assembling a piece of furniture requires picking up components, aligning and attaching them correctly, and tightening screws for each part. Moreover, operating at a single level of abstraction causes small prediction errors to compound over time, degrading performance in long-horizon tasks. Finally, flat architectures fail to extract high-level abstractions, limiting transferability across tasks and environments. 

## _2) Hierarchical Architecture_ 

Several studies have begun to explore and design hierarchical world models. In this scheme, lower-level modules handle intermediate reactions and short-term predictions, while higher-level components are responsible for long-term planning and abstraction. Lecun _et al._ [11] hypothesize a hierarchical JEPA architecture, where low-level and highlevel representations are learned for short- and long-term 

predictions, respectively. Gumbsch _et al._ [56] propose an RSSM-based hierarchical world model, where the low-level module captures immediate dynamics for reactive control, and the high-level module models abstract temporal patterns for strategic planning. Bj¨orck _et al._ [44] introduce a dualsystem architecture in which System 2 interprets the environment and task goals, while System 1 generates continuous motor commands in real time. Similarly, Wang _et al._ [45] design a dual-level world model consisting of an RSSM-based System 1 (RSSM-S1) and a logic-integrated neural network System 2 (LINN-S2). The inter-system feedback mechanism ensures that predicted sequences comply with domain-specific logical rules: LINN-S2 constrains RSSM-S1’s predictions, while RSSM-S1 updates LINN-S2 based on new observations, enabling dynamic adaptation. Wang _et al._ [98] further employ System 2 for value-guided high-level planning by estimating state-action values and selecting optimal actions, while System 1 executes real-time motions via cascaded action denoising. Despite their advantages, hierarchical architectures introduce greater model complexity, higher computational cost, and increased training difficulty. Determining which goals or subtasks should be handled by high-level versus low-level modules remains challenging, as does designing appropriate architectures and preparing suitable training datasets. Moreover, maintaining effective information flow and coordination between layers is essential for stable and coherent performance. Consequently, developing hierarchical world models requires substantial effort in architecture design, goal decomposition, dataset construction, and inter-layer coordination. 

## Implications for World Model Paradigms and Architectures 

World models can take diverse forms depending on the specific approach and task, but their fundamental objective remains the same: to model environmental dynamics and predict future states. Their design must balance efficiency, long-horizon reasoning, generalization across tasks, and the integration of multimodal inputs. To capture both short-term reactions and long-term planning, hierarchical architectures are often adopted. However, such designs introduce additional challenges, including greater complexity, higher computational cost, difficult goal decomposition, demanding dataset preparation, and the need for effective interlayer coordination. 

## _C. World Observation and Representation_ 

## _1) Dimensionality of the World_ 

In designing world models, the dimensionality of the environment is critical in shaping a model’s ability to capture spatial structures, temporal evolution, and causal dynamics. 

Some works operate purely in 2D pixel space [19], [20], [92], [72], [93], [66], capturing visual appearance and shortterm dynamics but ignoring the real-world geometry. While 2D pixel-space models [19] capturing visual appearance and shortterm dynamics but lacking geometric awareness of real-world 

8 

structure. This limitation motivates the development of 3Daware architectures. To incorporate geometric understanding of the 3D world, Bu _et al._ [22], [70], [7] construct world models based on RGB-D data, while others extract richer 3D cues such as scene flow [21], motion fields [69] and 3D point clouds with associated language descriptions [41], enabling more comprehensive modeling of 3D world dynamics. Additionally, Lu _et al._ [34] leverage 3D Gaussian Splatting, Diffusion Transformers, and 3D Gaussian Variational Autoencoder to extract 3D representations from RGB observations. Zhang _et al._ [60] incorporate depth estimation to enhance the understanding of 3D worlds. In addition to geometric structure, temporal dynamics are incorporated to construct 4D world models that jointly capture spatial and temporal evolution. For example, Zhu _et al._ [23] synthesize 4D data from RGB-D videos by estimating depth and camera pose. Zhen _et al._ [24] leverage the pre-trained 3D VAE [99] to encode RGB, depth, and normal videos and sum them together. Huang _et al._ [8] employ 4D Gaussian splatting to model spatiotemporal dynamics in robotic environments. 

## _2) Observation Viewpoint of the World_ 

Robots acquire skills by observing and imitating humans or other agents in their environment. Depending on the observation viewpoint, world models for robot learning can be categorized into third-person (exocentric) [21], [25], [26] and first-person (egocentric) [27], [28] perspectives. Many existing methods learn from exocentric perspectives, capturing skills from an external viewpoint [21], [25], [26]. However, exocentric observations do not fully align with how humans perceive the world. This has motivated the development of egocentric world models. For example, Chen _et al._ [27] observe a continuous loop of human interactions, in which humans perceive egocentric observations and take 3D actions repeatedly. They model interactions as sequences of “stateaction-state-action” tokens, processed using a causal attention mechanism. Zhang _et al._ [7] focus on multi-agent planning, inferring other agents’ actions from world states estimated via partial egocentric observations. 

Grauman _et al._ [28] argue that egocentric and exocentric viewpoints are complementary. Learning through egocentric viewpoints allows robots to better understand hand-object interactions and the attention mechanism of the camera wearer, while exocentric perspectives provide information about the surrounding environment and whole-body poses. 

_3) Representation of the World_ 

A central aspect of world models lies in how the environment is represented, which directly influences their ability to reason about dynamics, predict future states, and generalize across tasks. World representations can be broadly categorized into scene-centric, object-centric, and flow-centric approaches. In scene-centric representations, the environment is encoded as a single holistic latent, typically learned directly from pixels or raw sensory inputs [29], [12], [13], [15], [100]. While video generation tasks aim to maximize the visual fidelity of predicted sequences, robotic manipulation often does not require the full visual detail. Irrelevant elements such as the background or parts of the robot arm can be ignored. This motivates the use of object-centric representations, which 

focus on task-relevant entities and their interactions [25], [33], [26], [69], [18]. Flow-centric representations, in contrast, are designed to capture the motion dynamics of the environment, emphasizing temporal change and spatial displacement [65]. 

Implications for World Observation and Representation 

The world is inherently structured, requiring models to consider multiple dimensions in order to capture spatial and temporal dynamics, and to select appropriate observation viewpoints and representations according to task requirements. Each strategy provides distinct advantages, and effectively combining their complementary strengths while maintaining computational efficiency remains a central challenge. 

## _D. Task Scope_ 

World models can also be categorized based on their task coverage. Some studies focus on single-task objectives, such as future-scene prediction [37], [36], [33], [38], [30], or planning and action prediction [39]. 

In contrast, an increasing number of studies aim to support multiple tasks simultaneously, thereby enhancing the generality and applicability of world models. For instance, Cheang _et al._ [58], [66], [5], [65] generate videos for futurescene prediction and accordingly infer corresponding actions. Other works pursue simultaneous action prediction and worldscene forecasting [40], [27], [41], [42]. Beyond dual-task integration, several approaches extend world models to even broader capabilities. For instance, Bruce _et al._ [20] propose interactive video generation that supports environment prediction and imitation learning, and utilize a latent action model to infer policies from unseen, action-free videos. Liao _et al._ [57] introduce a unified framework for embodied video generation, policy learning, and simulation. Lu _et al._ [34] learn 3D world representations for future-state prediction, imitation learning, and simulator through video generation. Zhu _et al._ [43] develop an action-conditioned world model supporting trajectory-conditioned video generation, policy evaluation, and planning. Similarly, Huang _et al._ [8] achieve multi-view video generation, robotic action prediction, and a data flywheel mechanism for sim-to-real adaptation. 

**Would Foundation Models.** When discussing task scope, the notion of “foundation world models” becomes essential. These approaches aim to generalize across diverse tasks through large-scale training, paving the way for world models that act as universal backbones for robotics. One line of research achieves this through large-scale pretraining followed by taskspecific fine-tuning [34], [6], [96], [58], [101]. In particular, Mazzaglia _et al._ [101] integrate a foundation VLM with a generative world model to enhance multimodal generalization. Other works directly pursue large-scale end-to-end training to build general-purpose world models [20], [40]. 

9 

## Implications for the Task Scope 

The task scope directly shapes the capabilities and practical functions of a world model. Single-task models can achieve high performance but offer limited generalization, whereas multi-task models support diverse tasks at the cost of efficiency and potential taskspecific performance. The choice between single-task and multi-task world models depends on task complexity, generalization requirements, available data, computational resources, and modularity, with multitask models often preferred for flexible and reusable robotic systems. 

## IV. FUNCTIONS OF WORLD MODELS 

World models play a central role in modern robotics by providing an internal predictive understanding of the environment. They enable robots to reason about future states, anticipate the consequences of actions, and perform evaluations, which are particularly valuable in real-world settings where interactions are costly, risky, or time-consuming. By modeling environmental dynamics, world models form the foundation for autonomous, adaptable, and efficient robotic systems. In robotic manipulation, world models serve two complementary functions: decision support, by predicting future scenes, actions and planning, and training facilitation, by generating data or acting as learned simulators. These roles are often closely related. For example, a world model used as a simulator can simultaneously generate training data and assist decision making [34], [57]. By combining these functionalities, world models provide a comprehensive framework that enables robots to act intelligently, learn efficiently, and adapt to complex and dynamic environments. Additional details are provided in Table I, which complements the following discussion. 

## _A. Decision Support_ 

- _1) Implicit World Models for Action Prediction and Planning_ 

This line of work explores world models that enable action prediction and planning without explicitly modeling state transitions or world dynamics. These approaches typically leverage the strong reasoning and next-token prediction capabilities of Large Language Models (LLMs), Vision-Language Models (VLMs), and Vision-Language-Action (VLA) models. Since LLMs lack direct access to environmental or robotic states, auxiliary components are often incorporated to provide grounding. For example, Ahn _et al._ [62] introduce affordance functions to evaluate the feasibility of skills for completing a target task. Xiang _et al._ [72], [54] employ encoders to process environmental information, while Zhang _et al._ [60] integrate multimodal tokens including states, images, and text to enhance reasoning and generalization. Zhang _et al._ [17] further combine 2D and 3D encoders to process RGB images and 3D point clouds, capturing complementary spatial cues for richer world understanding. Hong _et al._ [18] extend this paradigm by incorporating additional sensory modalities such 

as vision, audio, tactile, and thermal inputs to achieve a more comprehensive understanding of the environment. 

Conventional LLMs are language-centric and typically treat visual and other sensory information as auxiliary inputs. VLMs extend this paradigm by jointly learning aligned visual and linguistic representations, enabling grounded perceptual understanding of the world [83]. Zhang _et al._ [84] further leverage VLMs to generate candidate action sequences, which are evaluated using a lightweight action-conditioned video prediction model to forecast future scenes. The predicted outcomes are then assessed by the VLM to select the final action. An increasing number of studies extend VLMs to VLA by equipping them with low-level action generation capabilities. For instance, Zitkovich _et al._ [16] represent robot actions as a form of language, effectively bridging perception and control through textual grounding. Zhen _et al._ [41] employ a 3D-based LLM [85] to represent and predict 3D world states and generate actions, incorporating a diffusion model to synthesize future scenes. Inspired by the dual-process theory of human cognition [102], Bj¨orck _et al._ [44] design a dualsystem architecture in which a VLM serves as the reasoning module (System 2) and a Diffusion Transformer functions as the action module (System 1), with both components jointly optimized for coordinated reasoning and actuation. Zhou _et al._ [103] preserve the reasoning capability of VLMs while introducing a Mixture-of-Experts to alleviate conflicts between multimodal understanding and robotic manipulation in the parameter space. Kim _et al._ [55] train their model on a large corpus of real-world robot demonstrations, enabling efficient adaptation to new robotic platforms through parameterefficient fine-tuning. 

To further enhance long-horizon prediction, reasoning, and imagination, several methods integrate large language or multimodal models into other world model architectures, where they serve as core components. For instance, Chen _et al._ [27] employ the open-source LLM, i.e., InternLM [87], to predict future states from egocentric observations as a fundamental element of the JEPA framework. Similarly, Vision-Language Models [101] and Video-Language Models [86] have been incorporated into Dreamer-style architectures for low-level dynamics modeling, where they extract high-level semantic knowledge of the world to guide prediction. 

Notably, LLMs, VLMs, and VLAs can also act as explicit world models that predict future scenes [78], [60], [79] or world knowledge [60]. We will elaborate them in Section IV-A3. 

- _2) Latent Dynamics Modeling for Action Prediction and Planning_ 

This line of research focuses on modeling the temporal evolution of environment dynamics within a latent space, facilitating efficient action prediction, planning and future imagination. Operating in a compact latent space requires fewer environment interactions and reduces computational cost compared to pixel-based modeling. Hafner _et al._ [29], [12], [13], [14], [15] introduce online planning in latent space through the Recurrent State-Space Model (RSSM), which learns to reconstruct input observations [29]. The Dreamer series [12], [13], [14], [15] introduces latent imagination, 

10 

allowing agents to predict and plan over latent trajectories instead of pixels for more efficient and stable policy learning. Specifically, DreamerV1 [12] learns long-horizon behaviors from images by jointly predicting actions and state values, greatly improving sample efficiency. DreamerV2 [13] extends this framework to discrete environments by introducing binary latent variables, achieving human-level performance on the Atari benchmark. DreamerV3 [15], [100] further improves scalability and generative capacity through techniques such as symlog normalization for reward stabilization, refined KL balancing, and enhanced replay buffers. Sekar _et al._ [39] enhance generalization to downstream tasks through selfsupervised learning without task-specific rewards, while Wu _et al._ [14] deploy Dreamer in the real world without simulators. Gumbsch _et al._ [56] introduce context-sensitive dynamics via a context-specific RSSM and hierarchical architecture to improve scalability and long-horizon prediction. Ferraro _et al._ [25] develop object-centric world models for improved interaction reasoning. 

Under the JEPA framework, Chen _et al._ [27] capture causal and temporal dependencies by organizing states and actions into an interleaved sequence, integrating future state prediction and action generation within a unified transformer architecture. Building on this, Assran _et al._ [77] leverage pre-trained video encoders optimized with a masked denoising objective as the core of JEPA, enabling self-supervised learning through an action-conditioned predictor that autoregressively forecasts future states and actions. Incorporating other potential world models, such as LLMs and VLMs, have been introduced in Section IV-A1. 

There are also approaches that couple Model Predictive Control (MPC) with learned world models, where the predictive model is used to simulate future trajectories and select optimal actions in a receding-horizon manner. For example, Hansen _et al._ [104] learn task-specific latent dynamics models using temporal-difference objectives and apply them for efficient online Model Predictive Control. Hansen _et al._ [105] further improve generalization across diverse embodiments and action spaces by learning an implicit, control-centric dynamics model. 

_3) Vision-based Action Prediction and Planning_ 

Vision-based methods enable robots to predict future observations from sensory inputs, allowing them to plan actions in complex and unstructured environments. By simulating sequences of visual outcomes, robots can evaluate longhorizon behaviors, integrate multiple modalities (e.g., vision, language, and control), and generalize to novel tasks without task-specific retraining. This predictive capability makes visual imagination a key component of goal-directed and adaptive robotic decision-making. In particular, action-conditioned multi-frame prediction serves as a crucial element of prediction and planning, allowing robots to mentally simulate the outcomes of different actions before selecting the optimal one for a given task. According to the task formulation, existing approaches can be broadly classified into vision-conditioned and language-conditioned goal representations. 

**Vision-Conditioned Goals.** Finn _et al._ [36] learn to predict motion dynamics that remain consistent across visual 

appearances, aiming to enable long-range, action-conditioned video prediction and generalization to unseen objects. Ebert _et al._ [30], [64] improve long-horizon prediction by using an image registration–based cost function that continuously corrects errors during execution, achieving closed-loop visual planning. Bu _et al._ [22] further extend this idea with textconditioned video generation to synthesize depth- and flowconsistent sub-goal images. A feedback mechanism then selects sub-goals and generates corresponding actions based on visual error evaluation, bridging visual planning and policy learning. 

Imagining the future does not inherently produce actions. To enable action predictions, Finn _et al._ [63], [30], [64] incorporate visual prediction models with model-predictive control (MPC) to select the best action (sequence). Bu _et al._ [22] use an error-measurement strategy to select the best subgoal images and an MLP that is train with an Inverse Dynamics objective to decode the corresponding actions. 

**Language-Conditioned Goals.** In [36], [63], [30], [64], task specifications are provided as goal images, which are often difficult to obtain and prone to over- or under-specification. To address this limitation, a growing line of research leverages language as a more flexible, compact, and general medium for specifying tasks. However, translating language instructions into precise, actionable representations grounded in the robot’s observations remains challenging due to the misalignment between linguistic descriptions and visual perception. To bridge this gap, Nair _et al._ [76] use action-conditioned video prediction to simulate future scenes under different action sequences and learn a language-conditioned reward function from crowd-sourced descriptions to measure task completion. The best sequence is selected to maximize the reward. Zhang _et al._ [78] take advantage of the semantic knowledge and reasoning abilities of VLA and incorporate a decoder into VLA to enable future scene predictions and action generation. Zhou _et al._ [66] parse language instructions into compositional primitives to capture spatial object relations and generalize to novel commands, while also supporting multimodal task inputs such as goal images and sketches. Zhang _et al._ [60] enhance reasoning and generalization by introducing additional dream queries that capture historical information and predict dynamic regions, depth, and semantic maps using foundation models such as DINOv2 [106] and SAM [107]. 

**Diverse Goals.** Some works leverage diverse goal conditions to improve task understanding and completion. For instance, Wang _et al._ [9] develop a language–gesture-conditioned video generation model to disambiguate task specifications and integrate a behavior-cloning policy that unifies visual plan generation and manipulation. Du _et al._ [59] incorporate observed images as additional context in each frame-denoising step to synthesize video plans and employ an inverse-dynamics model to infer the corresponding action sequences. Zhao _et al._ [79] introduce visual chain-of-thought reasoning into VLA models by autoregressively generating sub-goal images alongside language instructions, enabling temporal planning and improving reasoning capability. 

**Action Inference.** A key advantage of vision–based action prediction is that it does not rely on large-scale action- 

11 

labeled data. They can be pre-trained on large-scale video data and infer actions by training a simple action extractor using small amounts of action data. Techniques for action extraction include the inverse dynamics model [108], [59], [66], a transformer encoder-decoder architecture [9]. Zhang _et al._ [7] use vision language models to propose actions, and a tree search to find the best plan. However, video predictions would contain irrelevant information to the target tasks or actions to execute such as background and robot arm. To handle this, Zhi _et al._ [69] extract 3D Flow from video data and learn 3D optical flow as a representation of object motions to guide action planning. Zhang _et al._ [60] propose dynamic region-based forecasting, which leverages optical flow prediction model [109], [110] to identify dynamic regions within the scene, enabling the model to concentrate on areas of motion that are critical for task execution instead of redundant frame reconstruction. Agarwal _et al._ [96] leverage large-scale pre-training on both image and post-training for robotic manipulation, including instructionbased video prediction and action-based next-frame prediction. 3D positional embeddings, including 3D factorized Rotary Position Embedding and absolute positional embedding for relative positions and absolute coordinates respectively, are adopted to capture spatial and temporal information. Actions are predicted through an action embedder MLP. Tian _et al._ [61] propose an end-to-end Predictive Inverse Dynamics Models, which learn actions and visual futures synergistically to enhance the simulation and action predictions ability. [111] predict both future frames and robot actions within joint latent denoising process, which support planning and acting in a closed-loop manner. 

**Visual Fidelity vs. Action Prediction.** Guo _et al._ [21] hypothesize that models trained solely with frame-prediction losses tend to emphasize visual appearance fidelity while underestimating accurate dynamics modeling. This highlights the need for approaches that explicitly separate dynamics learning from visual rendering. To address this, FlowDreamer adopts a two-stage framework that first predicts environment dynamics and then renders corresponding visual observations. 

## _B. Training Facilitation_ 

World models can act both as data engines, generating synthetic trajectories that support imitation learning and reinforcement learning, and as evaluation modules that provide internal reward estimation or predictive feedback. Because many models combine these roles, it is difficult to assign them to a single category. Accordingly, when discussing each role, we introduce their complementary functions in parallel to highlight this overlap. 

## _1) Data Engine_ 

Large-scale human teleoperation datasets have greatly advanced robot learning [16], [31], [32], [112], [44], [35]. However, collecting such data is labor-intensive and limits coverage across diverse environments and tasks. Vision-based world models, particularly video world models, offer an alternative by learning environment dynamics and generating synthetic data. These models can be broadly divided, according to whether they are conditioned on actions, into static video generation models [38], which predict general future scenes, and 

action-conditioned video generation models, which simulate how actions change the environment. Beyond data generation, video-based world models increasingly support diverse tasks such as planning, policy learning, and action prediction, which will be reflected in the following content. 

Specifically, Du _et al._ [59] target to enable visual world imagination, action planning and generating video demonstration for training by learning a text-conditioned video generation model. Wu _et al._ [6] train a large-scale video world model to generate accurate and realistic simulated experiences, enabling video prediction, visual planning, and policy training. Jang _et al._ [38] propose to leverage video world models [97] to generate robot video data. They first fine-tune video world models on a target robot to capture the embodiment-specific dynamics and kinematics and prompt the model with to initial frames and language instruction to generate corresponding data. Pseudo-action labels are generated by means of either a latent action model [113] or an inverse dynamics model [114]. Lu _et al._ [34] leverage 3D-GS reconstruction with Diffusion Transformers to effectively model 3D dynamics, which can promote future scenes generation to support imitation learning and reinforcement learning. Ye _et al._ [115] synthesize data from diverse perspectives to introduce variations in texture, illumination, viewpoints, physical properties, task diversity, and interaction patterns. Their approach includes: (i) re-rendering real trajectories with diverse visual content, (ii) generating viewpoint-consistent multi-camera scenes with pose adjustments, and (iii) synthesizing embodied interaction sequences, such as converting first-person human videos into robot-centric demonstrations. To ensure realism and avoid hallucination artifacts, the authors further leverage a set of quality assessment metrics that evaluate geometric consistency [116], multiview consistency [116], text–scene alignment [117], and physical plausibility [117]. When constructing world models for training data generation, it is unrealistic to expect any training distribution to encompass all possible configurations of the world. To handle this, Barcellona _et al._ [33] construct a compositional world model to generate novel demonstration data for training by combining Gaussian Splatting [118] and physics simulators. Equivariant transformation is leveraged to augment data, which modify both observations and the corresponding action sequences to ensure semantical consistency. Wang _et al._ [119] present a video-based world model capable of predicting future visual observations conditioned on VLAgenerated actions. A VLM-guided instant reflector serves as a reward function that quantifies task completion through the semantic alignment between the predicted trajectory and the textual instruction. 

Despite recent progress, existing methods continue to face challenges in generating diverse and counterfactual data that remain physically plausible, thereby limiting the quality and diversity of synthetic datasets [44]. 

## _2) Evaluation_ 

Traditionally, robot control policies have been developed and evaluated using handcrafted physics simulators [120], [121], [122]. However, such simulators rely on simplified or manually engineered dynamics, which struggle to capture complex real-world phenomena, particularly high-DoF inter- 

12 

actions, deformable objects, and other non-rigid or contactrich scenarios [123], [124], [125]. Consequently, the resulting discrepancies between simulated and real environments, commonly referred to as the sim-to-real gap, have significantly hindered the deployment and generalization of robotic policies in practice [126], [127]. To handle this, world models potentially emerge as a scalable, reproducible, and informative tool, which reduce reliance on trial-and-error in the real world. Compared to other filed such as autonomous driving [128] and navigation [129], simulated evaluation of robotic manipulation remains difficult because of the highly varied and dynamic interactions that arise between the agent and its environment. Li _et al._ [130] leverage a video generative world model [97] to produce videos based on action representations from a policy network. A success detector [131] is then used to evaluate task completion from the generated videos and corresponding text prompts. Quevedo _et al._ [74] evaluate robot polices by means of Monte Carlo rollouts in the world model and take a vision-language model, i.e., GPT-4o [132], as the reward model. He _et al._ [133] introduce a framelevel control and a motion-reinforced training to improve action-following ability and temporal, dynamic consistency, enhancing the dynamic prediction and action responsiveness of world simulator. More valuable transitions are discovered for policy learning. Zhu _et al._ [43] construct a frame-level, action-conditioned video world model based on a Diffusion Transformer, enabling scalable policy evaluation, planning, and future-scene generation. Liao _et al._ [57] take an actionconditioned video generator as the core to model the spatial, temporal, and semantic regularities of real-world interactions that are fundamental to robotic manipulation. The base world model can support future scene generation, action predictions, data engine and closed-loop policy evaluation. Wang _et al._ [73] promote the versatility of video world models for policy evaluation, visual simulation, synthetic data generation by perform training on heterogeneous actions data with a shared spatial-temporal transformer. 

Escontrela _et al._ [134] train an autoregressive transformerbased video prediction model and use the next-token likelihoods of the frozen model as a general **reward** function across diverse tasks. 

## Implications for Functions of World models 

World models advance robotic learning by providing a unified predictive core that supports both decisionmaking and training. This highlights their growing importance and motivates efforts to build foundational world models capable of supporting diverse downstream tasks. However, differing objectives, such as pixel-level video generation and action-centric prediction, impose competing requirements on representations, suggesting that a single model must carefully balance fidelity, controllability, and task relevance. 

## V. KEY TECHNIQUES AND NOTABLE CHALLENGES 

This section summarizes the key techniques that drive the development of world models and discusses the major 

challenges that remain in achieving general, scalable, and robust modeling. Some techniques and concepts are revisited across subsections to emphasize their central importance. 

## _A. Data Limitations_ 

World models require large amounts of data and supervision to learn generalizable representations of world dynamics and support diverse tasks. However, collecting real-world robotic data is labor-intensive and costly, and the available data are often heterogeneous in format and modality. To overcome these limitations, a variety of strategies have been proposed. 

_1) Training Data Scarcity_ 

_a) Leveraging Pre-trained Models_ 

Given the limited availability of training data, many approaches leverage existing pre-trained models. For example, Xiang _et al._ [72] bypass the need for training from scratch by integrating a pre-trained LLM and a pre-trained video model, requiring only lightweight fine-tuning. Zhu _et al._ [43] initialize IRASim with the pre-trained weights of OpenSora [93] to expedite training. Similarly, Sudhakar _et al._ [37] leverage a pre-trained diffusion model, while Wang _et al._ [9] utilize Stable Video Diffusion, fine-tuned with robotic videos to adapt to the robotics domain. Song _et al._ [42] further exploit the world knowledge embedded in pre-trained autoregressive video generation models such as NOVA [135]. 

_b) Incorporating Auxiliary Data Sources_ 

Some works tackle the shortage of robot data by using other available sources, such as human manipulation datasets. For instance, Zhi _et al._ [69] use both human and robot manipulation videos for training. However, these datasets often contain cluttered backgrounds and similar-looking objects. To address this, they apply optical flow constraints to make the learned representation embodiment-agnostic. Sudhakar _et al._ [37] leverage an automatic hand segmentation method to obtain agent-agnostic data for robot learning. Others resort to more diverse data. For example, Yang _et al._ [19] leverage diverse kinds of data, including objects, scenes, actions, motions, language, and motor control, and convert all actions into a common format. 

_c) Synthetic Data Generation_ 

Instead of relying on real-world data, Deng _et al._ [136] synthesize large-scale action data to train their model. To address the scarcity of 4D data, the Aether team [23] generate RGB-D synthetic videos and develop a robust camera-pose annotation pipeline to reconstruct full 4D dynamics. Similarly, Zhen _et al._ [24] build a 4D embodied video dataset that combines synthetic data with ground-truth depth, normal information and real-world data with estimated depth and normal maps obtained from off-the-shelf estimators. 

## _2) Heterogeneous Action Data_ 

World models should be able to understand different forms of actions and embodiments to ensure their real-world applications. A basic strategy is to utilize diverse datasets for training. However, the inherent cross-domain and cross-embodiment nature of datasets lead to heterogeneous actions data, including action spaces, action frequencies, and action horizon. For example, diverse embodiment (e.g., different degrees of freedom 

13 

across robotic arms) and control interface (end effector (EEF) position for arms) would lead to actions of different forms. To handle this, Zheng _et al._ [137] learn to capture their shared structural features to obtain the generic atomic behaviors by means of vision language models. Similarly, Zheng _et al._ [73] lean a share latent space for actions by decoupling observation and actions. More strategies can borrow from relevant fields [138], [139], [140]. 

## Implications for Data Limitations 

The scarcity of data can be alleviated by leveraging external datasets or pre-trained base models from other sources. The key challenge lies in bridging the gap between the source and target domains. Furthermore, it is desirable to uncover the underlying knowledge through supervised learning. 

## _3) Action Label Missing_ 

Action-labeled data, which are essential for learning actionconditioned future predictions [19], are particularly scarce in real-world settings. 

## _a) Self-supervised Learning_ 

Finn _et al._ [36], [63] propose to learn pixel-level motion in a self-supervised manner, while Ebert _et al._ [30], [64] leverage image-to-image registration between consecutive video frames to capture dynamics without explicit action labels. However, goal image-based learning presents several drawbacks: such goals are inconvenient for humans to specify, may overconstrain the desired behavior (leading to sparse rewards), or under-specify task-relevant information for non-goal-reaching tasks. 

## _b) Action Label Extraction_ 

Another approach to handling missing action labels is to infer them directly from unlabeled videos. More specifically, Bruce _et al._ [20], [141] employ latent action autoencoders to extract latent actions in a self-supervised manner. In their studies, Bruce _et al._ [20] sample actions uniformly, while Gao _et al._ [141] introduce biased action sampling to encourage broader exploration and enable action reuse across contexts. Jiang _et al._ [38] extract pseudo-actions using either a latent action model [113] or an inverse dynamics model (IDM) [114]. Du _et al._ [59], [75], [26], [70] learn from unlabeled videos by training inverse dynamics models to infer actions or their embeddings. Ren _et al._ [75] further integrate an inverse dynamics module into a latent dynamics model to leverage rich temporal representations, improving the temporal consistency of predicted actions. Villar _et al._ [26] predict latent actions from object-centric representations. 

## _c) Other Strategies_ 

Some works aim to leverage **pre-trained video models** . For instance, Rigter _et al._ [67] adapt a pre-trained video diffusion model for action-conditioned world modeling by training a lightweight adapter, which is then fine-tuned on a small set of domain-specific, action-labeled videos. Black _et al._ [68] similarly employ a pre-trained image-editing diffusion model to support video-based world modeling. In addition, Zhu _et al._ [71] design a **unified world model** that integrates the action and video diffusion processes within a unified transformer architecture using separate diffusion timesteps. This can enable learning from action-free video data. Ko _et al._ [70] utilize **optical flow** extracted from videos, thereby circumventing the need for explicit action labels. 

## _B. Perception and Representation_ 

Perception lies at the heart of robotic world models, enabling systems to interpret task instructions and transform raw sensory inputs into meaningful representations. These representations allow robots to understand structured environments and, in turn, predict, react, and plan effectively. 

## _1) Inputs_ 

**Language.** Task instructions are usually given in language. Many methods use pretrained models such as CLIP [22], [70], [142], [61], Phi [143], [42], or conditional VAEs [42] to extract semantic representations from the instructions. 

**Visual data.** Similarly, visual inputs are often processed using pre-trained visual encoders. For example, Tian _et al._ [61] leverage pre-trained Vision Transformers (ViTs) [144] to process image observations. Wu _et al._ [6] employ a conditional VQGAN that encodes only task-relevant dynamic information, such as the position and pose of moving objects, to reduce temporal redundancy across frames. An autoregressive, GPTlike transformer is then used to generate the next tokens, which are decoded into future frames. 

**Action data.** Actions are sometimes represented as integer values, which lack the contextual richness. This limitation can prevent world models from accurately capturing the intended meaning behind actions. To address this, He _et al._ [133] propose representing actions through language templates that explicitly encode their semantic meaning. In many cases, actions are instead expressed in natural language, as noted above. While this enables richer semantic representations, it also introduces challenges, such as instruction-following ambiguity, which are discussed in Section V-B2a. 

**Diverse data inputs.** Robots need to gain a structured understanding of the world by jointly considering diverse sensory inputs. To achieve this, Song _et al._ [42] embed images and robot actions into a unified physical space, enabling the model to capture the sequential evolution of both the robot and its environment. Hong _et al._ [18] incorporate visual, auditory, tactile, and thermal modalities, projecting them into a shared feature space where a language model generates subsequent states and action tokens. 

_2) Challenges_ 

## _a) Instruction Understanding and Following_ 

Instructions convey task goals and can take various forms, including linguistic directives (natural language or structured text), visual cues (sketches, images, or demonstration videos), and others. Compared to image-based goals, textual descriptions provide a more abstract, compositional, and flexible way of specifying objectives, enabling better generalization, clearer intent communication, and more efficient human–robot 

14 

interaction. Many recent works express target goals through text descriptions [59]. Ideally, language instructions should clearly describe the task and remain easily interpretable by the model. However, real-world scenarios often involve ambiguous or novel instructions, making effective interpretation and grounding critical for successful task execution. **Ambiguous Instructions.** In real-world scenarios, language instructions are often ambiguous (e.g., “put this near here” [9]). To resolve such ambiguity, Wang _et al._ [9] use pointing gestures, interpreted through 2D gripper and object tracking, as an additional instruction modality. 

**New Instructions.** World models are constrained to make predictions based on language instructions similar to those encountered during training, limiting their ability to generalize to novel commands. To solve this problem, Xiang _et al._ [72] curate a large and diverse set of action-state sequences from re-captioned videos and simulations, and fine-tune world models on this data to improve instruction interpretation and generalize to novel commands and tasks. Li _et al._ [66] employ a text parser to decompose language instructions into primitives, separating actions and spatial relationships. This decomposition allows the model to flexibly recombine these components and generalize to previously unseen combinations of instructions. However, decomposing instructions into primitives can ignore their interrelationships. To address this, Li _et al._ [145] represent each instruction as an action tree, capturing the hierarchical structure among primitives to better model task organization. 

_b) Raw Pixels Modeling vs. Concept Abstraction_ 

Some studies suggest that humans make predictions based on abstract concepts rather than raw pixels [27]. Instead of converting images into discrete tokens [19], [6], Chen _et al._ [27] use learnable convolutional layers to project images into continuous semantic embeddings. Song _et al._ [42] adopt an open-source 3D variational autoencoder (Open-Sora [93]) to obtain video representations. In contrast, another line of work operates directly in pixel space. For instance, Ko _et al._ [70] adapt a U-Net-based image diffusion model with factorized spatial–temporal convolutions [146] to jointly capture spatial and temporal information. 

_c) Task-irrelevant Issues_ 

Visual data often contain information irrelevant to the task, and models such as Vision Transformers (ViTs) may produce hundreds of features per image, affecting both efficiency and effectiveness. To address this, Tian _et al._ [61] extract taskrelevant features using a perceiver resampler [147]. Ren _et al._ [75] learn compact visual representations that preserve finegrained temporal dynamics through a causal encoder–decoder structure and quantization with a discrete codebook [148]. 

_d) Spatiotemporal Awareness_ 

Understanding the world requires modeling how spatial structures evolve over time. To this end, several works design architectures that explicitly capture spatial and temporal dependencies. Tian _et al._ [61] enhance token representations with learnable positional embeddings at each timestep to capture temporal information. Bruce _et al._ [20] develop a spatiotemporal transformer composed of multiple spatiotemporal blocks to model spatial–temporal relationships in dynamic scenes. Ko _et_ 

_al._ [70] adopt factorized spatiotemporal convolutions following the design of [95]. Zhang _et al._ [60] extract spatiotemporal patch representations using a masked autoencoder [144]. Other studies incorporate additional cues to better understand the three-dimensional structure of the environment. For example, Zhang _et al._ [60] estimate depth information using depth estimation techniques [149] to enhance 3D spatial understanding. When encoding multi-view inputs, Liao _et al._ [57] augment each token with 2D rotary positional embeddings, view-specific learnable embeddings, and timestep encodings to promote spatiotemporal alignment while preserving viewpointspecific distinctions. 

## Implications for Perception 

World models should process and integrate diverse sensory inputs to build a coherent understanding of real-world dynamics. While current models primarily rely on vision and language, incorporating additional modalities such as tactile and proprioceptive sensing is crucial for achieving comprehensive perception in complex environments. It is also important to consider which information to perceive and how to model its spatial and temporal structure. 

## _C. Long-horizon Reasoning_ 

Many robotic tasks require coherent long-horizon reasoning, where achieving the final objective depends on executing a temporally consistent sequence of actions over extended time scales. Existing methods are limited in long-horizon predictions [76], [4], [29], [13], [15]. For example, Ha _et al._ [4], [29], [13], [15] predefine temporal horizons to guide planning in their world models. In terms of video generation, existing methods still suffer from limited length (short-horizon future video) [65]. For example, Ko _et al._ [70] predicts a fixed number (eight) of future frames with U-Net based diffusion model [146]. Bruce _et al._ [20] can only memorize 16 frames and cannot produce consistent predictions. For autoregressive models, small prediction errors compound sequentially, leading to substantial inaccuracies in long-horizon forecasts. 

## _1) Closed-loop Learning_ 

A line of work enabling long-term planning/predictions by learning through interaction with feedback and adjusting their behaviour accordingly [5], [22] . For example, Ebert _et al._ [30], [64] utilize image-to-image registration between predicted video frames and both the start and the goal images with the average length of the warping vectors as a cost function. The model would continue to retry until the task is completed. Du _et al._ [5] proposes a recursive planning framework comprising action proposal, video rollout generation, and evaluation. Vision–language models (VLMs) are used to propose potential next actions, while video generation models simulate multiple possible future rollouts. The resulting trajectories are then evaluated by the VLMs to select the optimal action. Du _et al._ [57] design a neural simulator that predicts future visuals, enabling policy models to interact within a consistent 

15 

environment. A sparse memory mechanism is leveraged to further enhance the consistency over the time. 

## _2) Subgoals_ 

Pre-trained models possess a vast repository of commonsense and procedural knowledge that can be leveraged to decompose a high-level goal, often specified in natural language (e.g., ”make a cup of coffee”), into a logical sequence of concrete sub-goals or skills. Bu _et al._ [22] propose to promote long-horizon manipulation tasks by decomposing the goal into sub-goals and handling error accumulations by designing a real-time feedback mechanism. Yang _et al._ [10] leverage VLM to produce sub-goals and utilize coarse and fine video diffusion models to generate long-horizon videos. Chen _et al._ [150] utilizes an LLM to generate a multi-stage plan and design a LLM-based dense reward generator for sub-tasks, providing crucial guidance for long-horizon planning. 

## _3) Hierarchical Structures_ 

Bu _et al._ [56] propose hierarchical world models with Adaptive Temporal Abstractions that separate the modeling of dynamics into high-level and low-level latent states. The low-level model captures fine-grained, short-term dynamics for immediate reactions, while the high-level model abstracts over longer temporal horizons to represent extended dependencies and long-term goals. By dynamically adapting the temporal granularity of the high-level latent states, the model can efficiently plan and predict over long horizons while maintaining accurate short-term predictions through the low-level module. 

## _4) More Strategies._ 

Driess _et al._ [54] provide a goal image in addition to language instructions. Du _et al._ [5] propose to take advantage of long-horizon inference of VLMs and the low-level visual dynamic modelling ability of text-to-video models to handle long-horizon visual planning. A tree search over the space of possible video sequences to find proper long-horizon plans. Ren _et al._ [75] lean compact representations for the visual world that preserve the detailed temporal dynamics by means of causal encoder-decoder and quantization with a discrete codebook [148]. 

## _D. Spatiotemporal Consistency_ 

Spatiotemporal consistency plays a vital role in ensuring coherent and physically plausible predictions of future states. It guarantees that the model preserves object continuity, motion smoothness, and causal relationships across time, enabling stable video simulation and reliable dynamics forecasting. 

## _1) Data Perspective_ 

In conditional video synthesis, Du _et al._ [59] incorporate the observed image as additional context when denoising each frame. Specifically, it adapts a temporal super-resolution diffusion architecture by tiling the conditioned visual observation across all timesteps. Each intermediate noisy frame is concatenated with the observed image throughout sampling, providing a strong spatial anchor that enforces consistent environmental states across time. Ko _et al._ [70] concatenates the initial condition frame with all subsequent frames, providing a stable reference that preserves both the spatial layout and temporal evolution of the environment throughout the sequence. Zhen _et_ 

_al._ [24] refine depth maps using normal integration to enhance spatial consistency. Optical flow is then calculated to ensure depth coherence across frames, maintaining consistent scene geometry over time. 

## _2) Model Perspective_ 

Yang _et al._ [10] noted that in autoregressive predictions, standard spatiotemporal attention in video diffusion models degrades frame consistency due to limited long-range context. To address this, the temporal attention layers are replaced with 3D full attention layers, enabling computation of attention across all spatiotemporal tokens and better modeling of large motions. Additionally, the spatial attention layers are modified by reinjecting the VAE features of the first frame and computing cross-attention with the spatial tokens of the query features, further enhancing frame coherence. 

## _3) Memory Mechanism_ 

Memory mechanisms preserve historical information, enabling the coherent evolution of spatial and temporal patterns over time. For example, Liao _et al._ [57] design a sparse memory mechanism to provide long-term historical context, improving spatiotemporal consistency and task relevance. More information can refer to Section V-G. 

## _E. Generalization_ 

Robots are expected to operate robustly in complex and novel environments, interacting with unfamiliar objects and performing tasks beyond their training distribution. 

## _1) Data Scaling_ 

An intuitive and effective strategy to enhance generalization is to scale the diversity and volume of training data. For example, Cheang _et al._ [58] increase the number of pretraining videos from 0.8 million in [151] to 38 million. Assran _et al._ [77] expand the dataset from 2 million used by [152] to 22 million videos. Wang _et al._ [73] expand each of the 40 datasets by increasing trajectories from 10 up to 10<sup>6</sup> . Cheang _et al._ [153] train the model with web-scale visionlanguage data, human trajectory data and robot trajectory data. Kevin _et al._ [154] leverage diverse mobile manipulator data, diverse multi-environment non-mobile robot data, crossembodiment laboratory data, high-level subtask prediction, and multi-modal web data. Cheang _et al._ [33], [58] investigate **data augmentation** strategies to enhance generalization. In [33], object rotation and roto-translation are applied. Cheang _et al._ [58] generate novel scenes by injecting objects using a diffusion model [155] and/or altering backgrounds with the Segment Anything Model (SAM) [107]. A video generation model [107] is subsequently employed to synthesize videos that preserve the original robot motions from the inpainted frames. Liao _et al._ [57] augment the dataset with a diverse set of failure cases, including erroneous executions, incomplete behaviors, and suboptimal control trajectories—collected from both human teleoperation and real-world robotic deployments. One problem of data scaling is that it is unlikely to collect all data for each tasks. At the same time, how to balance different data tasks is also challenging. Moreover, performance gains by scaling data is also limited for consistent performance improvements. 

16 

## _2) Use of Pretrained Models_ 

Many methods aim to enhance generalization by leveraging the generative capabilities of video models. For example, Zhu _et al._ [23] combine video generation with geometric-aware learning to improve synthetic-to-real generalization across unseen viewpoints and support multiple downstream tasks. Zhen _et al._ [24] fine-tune a video generation model on RGB, depth, and normal videos to encode detailed shape, configuration, and temporal dynamics, enabling generalization to unseen scenes, objects, and cross-domain scenarios. The generalization capabilities of large language models, such as videolanguage models [86] and vision-language models [101], can be leveraged to enhance world models. By extracting highlevel knowledge about the environment, these models facilitate more effective low-level dynamics modeling. 

## _3) Instructions Decomposing_ 

Another generation issue comes from unseen instructions. To handle this, Zhou _et al._ [66] enhance the ability to unseen instructions by decomposing each spatial relation phrase into a set of compositional components with the pre-trained parser [156] and the rule-based approach. Detailed information can refer to Section V-B2a. 

## _4) Invariant Representations_ 

Generalization can be significantly improved by learning invariant representations to superficial or task-irrelevant changes in the environment. For example, Pang _et al._ [157] model learns to explicitly decompose visual observations into a viewinvariant representation, which is used for the control policy, and a view-dependent representation. This decoupling makes the resulting policy robust to changes in camera viewpoint, a common source of failure in visuomotor control. Similarly, the Martinez _et al._ [158] framework learns a transferable communicative context between two agents, which enables zeroshot adaptation to entirely unseen sparse-reward environments by decoupling the representation learning from the control problem. Wu _et al._ [159] disentangle the modeling of context and dynamics by introducing a context encoder, enabling the model to capture shared knowledge for predictions. 

## _5) Task-relevant Information Focused_ 

Video data often contain irrelevant data to the actions such as background and robot arm, which would limited the generalization ability of the learned world models. To handle this, [69] propose to object-centric world models, which concentrated on object movements via the optical flow predictions that is independent of embodiment. Finn _et al._ [36] propose to explicitly model and predict motion that are relatively invariant to the object appearance, enabling longrange predictions and generalize to unseen objects. 

## _6) Other Strategies_ 

Black _et al._ [68] use a pretrained image-editing model to generate subgoals from language commands and current observations, enabling low-level controllers to act and generalize to novel objects and scenarios. Self-supervised learning without task-specific rewards that can enhancing generalization abilities into different tasks [39]. 

## _F. Physics-informed Learning_ 

Existing world models struggle to generate physically consistent videos because they lack an inherent understanding of physics, often producing unrealistic dynamics and implausible event sequences. Simply scaling up training data or model size is insufficient to capture the underlying physical laws [160]. To address this challenge, several approaches have been proposed. For example, Yang _et al._ [161] introduce a two-stage image-to-video generation framework that explicitly incorporates physics through vision- and language-informed physical priors. Team _et al._ [23] estimate depth and camera pose directly from videos, facilitating physics-informed learning and enabling world models to infer and predict physically consistent dynamics. Peper _et al._ [162] argue that advancing from physics-informed to physics-interpretable world models requires rethinking model design, and propose four guiding principles: organizing latent spaces by physical intent, encoding invariant and equivariant environmental representations, integrating multiple supervision signals, and partitioning generative outputs to improve both scalability and verifiability. 

## Implications for Generalization and Physics-informed World Modeling 

While large-scale training improves the predictive, and generative abilities of world models, handling complex environments requires going beyond simple replication of observations. World models must capture the underlying physical and causal mechanisms of the world, enabling them to generate and predict consistent dynamics across diverse and unseen scenarios. 

## _G. Memory_ 

Memory mechanisms enable world models to store and retrieve relevant past information, supporting hidden-state disambiguation and long-horizon reasoning. For example, LeCun _et al._ [11] incorporate a memory module that maintains past, current, and predicted world states along with intrinsic costs, allowing retrieval of contextual information for reasoning and training. Huang _et al._ [8] propose a sparse contextual memory mechanism that preserves essential prior information throughout the generation process in a non-redundant manner, theoretically enabling the generation of sequences of arbitrary length. Zhou _et al._ [163] employ a 3D feature-map memory to maintain temporal consistency during sequence generation. **Memory Efficiency.** Standard transformer blocks apply multihead self-attention to all tokens in the input token sequence, resulting in quadratic computation cost. Zhu _et al._ [43] leverage the memory-efficient spatial-temporal attention mechanism to reduce the computation cost. Liao _et al._ [57] randomly sampled parse memory frames from prior video history to augment temporal diversity to improve representational invariance, and use low-frame-rate video sequence for fine-tuning frames. 

17 

## _H. Other Techniques and Challenges_ 

## _1) Video Fidelity_ 

To achieve high-fidelity video generation, several methods leverage powerful generative models. For instance, Ko _et al._ [70] employ an image diffusion model based on a U-Net with factorized spatiotemporal convolutions as the fundamental building block. Guo _et al._ [21] utilize the pre-trained variational autoencoder from Stable Diffusion [164]. Souvcek _et al._ [165] propose to make use of a variety of action and final state prompts. 

## _2) Closed-loop Learning_ 

Closed-loop learning enables agents to actively refine their internal world models by observing and responding to realtime feedback from the environment. This continuous perception–action cycle grounds learning in physical reality, enhances generalization, and allows adaptive correction. Driess _et al._ [54] update observations based on the actions executed, which are then fed into VLMs to enable the robot to correct or reorganize its plan in response to environmental changes and task progress. Bu _et al._ [22] design a feedback mechanism that is based on the element-wise discrepancy measure between current and goal state embeddings. Zhi _et al._ [69], estimate the location of the moving objects, depth prediction, 3D optical flow by input into GPT-4o to verify alignment with given instructions, enabling closed-loop planning. 

_3) Reasoning_ 

Reasoning enables a robot to interpret sensory input and translate it into purposeful actions rather than reactive responses. Zhou _et al._ [60] enhance the reasoning and genrealization ability by incorporating context information and predicting dynamic regions, depth map, semantic knowledge by means of foundation models, e.g., DINOv2 [106] and SAM [107]. Ye _et al._ [115] introduce an Embodied Chain-ofThought as an intermediate reasoning representation, enabling more structured and interpretable decision-making in embodied tasks. Ye _et al._ [115] [79] generates a sub-goal image that represents the robot’s planned state in pixel space, and then conditions its action on both the current observation and the generated subgoal image. 

_4) Sim-to-real Gap_ 

The substantial gap between synthetic and real-world data limits the transferability and real-world performance of robotic systems. To handle this, Huang _et al._ [8] propose combining the generative model with 4D Gaussian Splatting, forming a self-reinforcing data loop to reduce the sim-to-real gap. 

_5) 3D Robotics World Prediction_ 

General-purpose video generation models neglect the substantial gap between their representation space and the threedimensional, temporally interconnected robotics environment, thereby hindering accurate action policy prediction. For example, Wen _et al._ [166] focuses on 2D image prediction before action generation. To handle this, Huang _et al._ [8] propose Free Anchor Views, a multi-view video representation offering flexible, task-adaptive perspectives to address challenges like motion ambiguity and environmental constraints. 

_6) Fine-grained Robot-object Interaction_ 

Robots are expected to perform precise manipulation, which requires world models to support fine-grained robot-object 


Fig. 4. Potential Core Components and Capabilities of World Models. 

interactions. To achieve this, Zhu _et al._ [43] design a novel frame-level action-conditioning module to achieve precise action-frame alignment. He _et al._ [133] adopt two different pre-trained video generative models as the base models, and introduce a minimalist yet powerful add-on action-conditioned module that improves frame-level action awareness while maintaining architectural flexibility. 

_7) Multi-agent Operation_ 

Certain tasks necessitate coordinated operation among multiple robots to achieve successful completion. To this end, Zhang _et al._ [7] factorize the joint actions of different agents as a set of text prompt and leverage composable video diffusion models to learn world dynamics and make predictions. An agent-dependent loss is imposed to let the model focus on the related pixel, where the loss coefficient matrix is based on each agent’s reachable region. 

## _8) Error Propagation_ 

In autoregressive models, subsequent actions are generated based on previous predictions, leading to error propagation over time. To handle this, Cen _et al._ [40] propose an attention mask strategy that selectively masks prior actions during the generation of the current action. It enables both future imagination and action generation. 

## VI. TOWARDS DEFINING CORE COMPONENTS AND CAPABILITIES OF WORLD MODELS 

From our survey of current approaches, we summarize some potential key components and capabilities that a world model should possess. Future research may identify additional dimensions necessary for comprehensive world modeling. 

- 1) **Comprehensive Multimodal Perception.** World models should be capable of perceiving and integrating information across all available modalities, such as vision, language, action, touch, force, and proprioception, along with the spatial and temporal structures. By jointly modeling these modalities and dimensions, they can construct a unified and dynamic understanding of the environment that facilitate decision-making and support robot training. 

18 

- 2) **Interactivity.** World models should engage dynamically with their environments, not merely by passively observing or predicting changes, but by modeling how actions influence future states. Such action-conditioned dynamics enable agents to simulate interactions, evaluate potential outcomes, and plan behaviors grounded in causal understanding of the world. 

- 3) **Imagination.** Imagination enables world models to simulate and evaluate possible futures, allowing agents to learn, plan, and reason without external interaction. 

- 4) **Long-horizon Reasoning.** It enables world models to anticipate distant consequences of actions, plan multi-step behaviors, and optimize long-term outcomes rather than short-term rewards. 

- 5) **Spatiotemporal Reasoning.** World models should reason about spatial and temporal relationships among entities to understand and predict dynamic changes in the environment. 

- 6) **Counterfactual Reasoning.** This enables world models to imagine alternative futures under different actions, allowing agents to evaluate possible outcomes and select the most effective course of action. 

- 7) **Abstract Reasoning.** The world is immensely complex, and world models cannot capture every detail. Therefore, they must extract and represent the underlying principles and basic mechanisms that govern the world’s dynamics. 

- 8) **High-fidelity Prediction.** World models should generate accurate and detailed predictions of future states or observations, maintaining spatial, temporal, and physical consistency to ensure reliable simulation and planning. 

- 9) **Physics Awareness.** World models should maintain consistency with physical principles, enabling them to generate dynamically plausible predictions that support safe and reliable robotic interaction. 

- 10) **Generalization Ability.** To operate effectively in complex real-world settings, world models must generalize beyond their training distributions, adapting to new tasks, objects, and domains. 

- 11) **Causality.** World models should understand relationship between actions (causes) and their effects (outcomes) in the world. This causal understanding enables agents to predict how interventions will change future states, distinguish correlation from true influence, and generalize their behavior to unseen situations by reasoning about cause–effect mechanisms rather than memorized patterns. 

- 12) **Memory.** It enables world models to store and recall past experiences, ensuring temporal consistency and coherent predictions. In addition, world models should be able to access and integrate external information, thereby supporting richer reasoning, long-term planning, and adaptability—analogous to the role of retrieval-augmented generation (RAG) in language models. 

- 13) **Collaboration Ability.** World models should support both inter-agent and intra-agent coordination by reasoning about the behaviors, goals, and intentions of others and managing cooperation among multiple effectors (e.g., multi-arm systems). 

## VII. DATASET 

There are abundant datasets that facilitate robot learning, including general robotic manipulation datasets [179], [30], [173], [175], [176], [181], [136], [183], dual-arm robotic manipulation datasets [112], human manipulation datasets [168], [170], [165], [172], [58], [41], combinations of robotic & human manipulation [41], egocentric datasets [169], [28], [171], 3D & 4D datasets [24], [41], [181], [69], [169], [28], [174], [177], [18], [178], [180], multi-view datasets [18], [28], [183] and panoramic-view datasets [177]. A detailed information can be found in Table. II. 

Recent efforts in world models for robotic manipulation have leveraged large and diverse datasets, often combining multiple sources, to enable generalization across tasks and environments. For example, Yang _et al._ [19] construct a large-scale natural dataset combining simulated executions and renderings [174], [175], real robot data [176], human activity videos [169], [171], [170], 3D panorama scans [177], and internet text-image data (i.e., LAION-400M [185]). Bruce _et al._ [20] combine the RT-1 dataset [167] with real robot grasping data [186]. Wu _et al._ [6] train the world model based on the combination of the Open X-Embodiment (OXE) dataset [178] and the Something-Something v2 trajectory dataset [170]. Bruce _et al._ [58] employ a pretraining and fine-tuning strategy. In the pretraining stage, a combination of human demonstration datasets such as Howto100M [168], Ego4D [169], Something-Something V2 [170], EPIC-KITCHENS [171], Kinetics-700 [172], and robot datasets [167], [173]. Fine-tuning data includes 105 table-top tasks via teleoperation covering eight skills (e.g., pick, place). Data augmentations are performed to add new objects or change backgrounds by means of a diffusion model [155] and the Segment Anything Model (SAM) [107], as well as a video generation model [187] to synthesize new videos. Du _et al._ [59] curate an internet-scale pretraining dataset consisting of 14 million video-text pairs, 60 million image-text pairs [188], LAION400M [185], and a smaller real-world robotic dataset [176]. Huang _et al._ [8] construct multi-anchor view video datasets using public sources including RT-1 [167], Taco-Play [189], ManiSkill [180], BridgeData V2 [173], LanguageTable [175], and RoboTurk [181], augmented with Isaac Sim simulations [190]. [24] construct a 4D embodied video dataset based on previous datasets [182], [167], [173], [170] by measuring depth and normal information. 

VIII. CONCLUSION AND FUTURE RESEARCH DIRECTIONS 

## _A. Conclusion_ 

This survey provides a comprehensive evaluation of current approaches to world modeling, examining their relevance for robotic manipulation, underlying architectures, functionalities, key challenges, and proposed solutions. By synthesizing these findings, we offer insights into the nature of fully realized world models and outline the efforts required to advance the field. Our goal is to provide readers with a solid foundation and guide future research directions in world modeling. 

19 

TABLE II 

A SUMMARY OF REPRESENTATIVE DATASETS. _<u>H</u>_ : HOUR, _Manip_ : MANIPULATION, _<u>Env.</u>_ : ENVIRONMENTS, _Traj._ : TRAJECTORIES. 

|**Dataset**|**Env.**|**Data Type**|**Dataset Size**|**Actor**|**Task/Skill/Content**|**Notes**|
|---|---|---|---|---|---|---|
|Robotic Pushing [30]|Laboratory|Video, Gripper Pose|59k|Robotic Arm|Push|-|
|RT-1 [167]|Office, Kitchen|Video|_∼_130k|Robot|744 Tasks, e.g., Pick, Move|-|
|Howto100M [168]<br>|12 Env., e.g., Home, Garden<br>|Video, Annotation<br>|136M<br>|Human|23k Tasks, e.g., Cook, Mark<br>l|-<br>|
|Ego4D [169]|Dailylife, Outdoor, Indoor|Video, Annotation, Audio|3,670 H|Human|Diverse Tasks, e.g., flip, lift|4D, Egocentric|
|Ego-Exo4D [28]|123 Natural Scenes|Video, Audio, 3D Point Cloud, Annotation|221.26 H Videos, 79M+ 3D Body Poses|Human|43 Tasks, 689 Keysteps|Multi-view, 4D, Egocentric, Exocentric|
|ManiFlow-110k [69]|-|Optical Flow|110k|Robot, Human|Object Movement|3D|
|Something-Something V2 [170]|Human-object Interaction|Video|108+K|Human|12 Tasks, e.g., Pour, Drop|-|
|EPIC-KITCHENS [171]|Kitchen|Video, Action Narrations|432 Sequences/55 H|Human|323 Tasks, e.g., Cook, Clean|Egocentric|
|Kinetics-700 [172]|Kitchen|Video|650K|Human|700 Tasks, e.g., Pour, Walk||
|Bridgedata v2 [173]|24 Env., e.g., Kitchens, Tabletops|video|60.1K Traj.|Robot|13 Tasks, e.g., Sweep|-|
|GR-2 [58]|Table-top|Video|40K Traj.,|Human|Diverse tasks/skills, e.g., Pick, Place|-|
|HM3D [174]|Photorealistic Indoor|RGB-D Video|1K Scenes|-|-|3D|
|LanguageTable [175]|Simulated & Real-world Tabletop|Video|600k Traj.|Robot, end-effector|Diverse tasks/skills, e.g., Push, Separate|-|
|Bridge Data [176]|Toy & Real Kitchens, Toy Sinks|Video|7.2K Trajec.|Robot|71 Tasks, e.g., Flip, Put|-|
|Matterport3D [177]|Building-scale Scenes|RGB-D Images|194K+|Tripod-mounted Cameras|-|Panoramic-view|
|Multisensory-Universe [18]|Indoor Scenes|Images, Audio, Tactile, etc|500k|Robot|67 Robotic Manip. tasks|3D, Multi-view|
|Open X-Embodiment [178]|311 Scenes, e.g., Household|Video, Depth, 3D Information|1M+ Traj.|Robot|527 Skills/160266 Tasks, e.g., Pick, Move|3D|
|DROID [179]|52 Buildings/564 Scenes|RGB Video, Depth, Proprioception, Instructions|76k Traj., 350 H|Robot|86 Tasks|-|
|ManiSkill [180]|Simulation|RGB/RGB-D Video, 3D Point Clouds, Proprioception|4M+ Frames, 2K+ Object Mdels|Robot|20 Manip. Tasks|3D|
|RoboTurk [181]|Tabletop|RGB & Depth Images, Robot Sensor Data|2K+ Demonstration Frames, 111.25 H|Robot Arms|Object Search, Tower Creation, Laundry Layout|3D, Long-horizon Object Manip.|
|AgiBot-World-Beta [112]|106 Scenes|Traj.|1M+ Traj., 2.9K H|Robot Arms|217 Tasks, 87 Skills|Dual-arm, Dexterous hands, Collaboration|
|3D-EIT [41]|Simulation|Images, 3D Point Cloud, Annotation|2M|Robot, Human|Robot Manip., Human-object Interaction|3D|
|TesserAct [24]|Synthetic & Real Scenes|RGB, Depth, Normal videos|285K|Robot Arms|Robotic Manip.|4D, Based on [182], [167], [173], [170]|
|SynGrasp-1B [136]|Tabletop, Simulation|Image|1B Frames, 10K+ Objects|Robot|Grasp|-|
|RH20T-P [183]|Tabletop, etc|Video|38k|Robot|67 Robotic Manip. Tasks|Primitive-level, Multi-view|
|RoboNet [184]|Diverse ENV., e.g., arena|Video, Traj.|15M Video Frame, 62K Traj.|Robot Arm and Gripper|Manip. Tasks, e.g., push and pick-and-place|-|
|GenHowTo [165]|Kitchens, etc|Image Triplets|200k|Human|Manip., e.g., Cut Tasks|-|


## _B. Future research directions_ 

From our survey of current approaches and analysis of the core components and capabilities of world models, it is evident that present models fall short of accurately representing realworld phenomena. The limitations and the set of expected capabilities define promising directions for future research. To provide additional context, we also discuss several significant research directions. 

**More Diverse Modalities.** The real world contains diverse forms of information, and no single sensory modality can capture its full complexity. This motivates world models capable of perceiving and integrating multiple modalities, including vision, language, action, touch, force, and proprioception, along with their interactions. Early progress has been made in this direction. For example, Hong _et al._ [18] introduce the Multisensory-Universe dataset, which features interactive scenes enriched with tactile, audio, and temperature signals, generated with the assistance of ChatGPT [191]. 

**Hierarchical World Models.** Hierarchical systems play a critical role in building effective world models, as they allow agents to reason across multiple layers of abstraction. However, designing hierarchical models is inherently challenging: separating low-level and high-level dynamics is difficult, and coordinating interactions across layers adds further complexity. While existing studies primarily emphasize model design [56], [11], [45], [80], their validation in complex real-world environments remains limited. 

**Causality** is a fundamental principle for understanding and modeling the world, describing how events or factors influence outcomes and enabling reasoning about future consequences. It is the key to the world model and agents to allow them to interact with the world, which is inline with the human cognition. Richens _et al._ [192] indicate that learning a causal model is the key to ensure the generalization ability to new domains. Wang _et al._ [193], [194] learn a causal dynamics model by removing unnecessary dependencies for tasks, which however are constrained to specific tasks. Gupta _et al._ [195] argue that conventional theory-driven approaches to causal modeling, such as those in [196], [197], are insufficient for world models that aim for generalizable understanding. These methods rely on predefined variables and case-specific 

theoretical properties. In the real world, sensory inputs are complex, often unstructured, and key theoretical properties, such as identifiability, may not hold. 

**Resource-Constrained Deployment.** Current world models, particularly those based on video generation, are computationally intensive and contain hundreds of millions of parameters, which limits their feasibility for real-world robotic deployment and on-device inference. To enable practical applications, designing lightweight and efficient world models has become increasingly important. Quantization and model compression techniques offer promising directions for reducing memory and computational costs, and have been extensively explored in related domains [198], [199], [200], [201], providing both direct solutions and inspiration for future lightweight world model architectures. 

**Fairness and Security.** As world models become integral to embodied agents and decision-making systems, ensuring their ethical alignment and fairness is critical. Unlike conventional vision or language models, world models directly influence how autonomous agents perceive, reason, and act within real environments, which amplifies the consequences of biased or unsafe representations. To handle this, emerging research explores bias auditing, fairness-aware training, and safetyconstrained learning objectives to prevent harmful behaviors and unintended policy generalization. 

Furthermore, deep models are known to be vulnerable to adversarial attacks, which can compromise performance by introducing imperceptible perturbations to inputs [202], [203], modifying model parameters [204], [205], or even exploiting hardware-level weaknesses [206], [207]. These vulnerabilities raise serious concerns regarding the security and reliability of world models, especially when deployed in safety-critical domains. To date, systematic studies on the robustness and security of world models remain limited, underscoring an urgent need for dedicated research into adversarial resilience, trustworthy deployment, and secure model adaptation. 

**Evaluation Protocols.** Current evaluation practices for world models are fragmented and only loosely aligned with their intended capabilities, often relying on task-specific or proxy metrics and partial human validation [57]. There is a pressing need for standardized benchmarks and unified evaluation frameworks that can comprehensively assess world model 

20 

competence across multiple dimensions, including visual fidelity, policy success, causal consistency, physical plausibility, generalization, and long-horizon reasoning. 

**Beyond Human Intelligence.** Insights from human cognition have profoundly influenced the design of robotic and world modeling systems [11], [56], [44], [45]. However, the completeness of the world extends beyond human cognition, which is bounded by partial observation, finite memory, limited attention, and inherent heuristic biases. World models are therefore expected to transcend human cognitive bounds, providing a deeper and more systematic understanding of complex environments. 

## **Structured and Abstract World Understanding.** 

“ _Truth is ever to be found in simplicity, and not in the multiplicity and confusion of things_ .” — Isaac Newton 

The ultimate goal of world models is to capture underlying regularities and structured abstractions, rather than memorizing every detail of a complex environment. This focus on essential structure is key for enabling world models to generalize across diverse environments. 

## REFERENCES 

- [1] J. Richens, T. Everitt, and D. Abel, “General agents need world models,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [2] M. MINSKY, “A framework for representing knowledge,” _The psychology of computer vision_ , pp. 211–277, 1975. 

- [3] J. Schmidhuber, “On learning to think: Algorithmic information theory for novel combinations of reinforcement learning controllers and recurrent neural world models,” _arXiv preprint arXiv:1511.09249_ , 2015. 

- [4] D. Ha and J. Schmidhuber, “World models,” _arXiv preprint arXiv:1803.10122_ , 2018. 

- [5] Y. Du, M. Yang, P. Florence, F. Xia, A. Wahid, B. Ichter, P. Sermanet, T. Yu, P. Abbeel, J. B. Tenenbaum _et al._ , “Video language planning,” _arXiv preprint arXiv:2310.10625_ , 2023. 

- [6] J. Wu, S. Yin, N. Feng, X. He, D. Li, J. Hao, and M. Long, “ivideogpt: Interactive videogpts are scalable world models,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 68 082–68 119, 2024. 

- [7] H. Zhang, Z. Wang, Q. Lyu, Z. Zhang, S. Chen, T. Shu, B. Dariush, K. Lee, Y. Du, and C. Gan, “Combo: Compositional world models for embodied multi-agent cooperation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [8] S. Huang, L. Chen, P. Zhou, S. Chen, Z. Jiang, Y. Hu, Y. Liao, P. Gao, H. Li, M. Yao _et al._ , “Enerverse: Envisioning embodied future space for robotics manipulation,” _arXiv preprint arXiv:2501.01895_ , 2025. 

- [9] B. Wang, N. Sridhar, C. Feng, M. Van der Merwe, A. Fishman, N. Fazeli, and J. J. Park, “This&that: Language-gesture controlled video generation for robot planning,” in _2025 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2025, pp. 12 842–12 849. 

- [10] L. Yang, Y. Bai, G. Eskandar, F. Shen, M. Altillawi, D. Chen, S. Majumder, Z. Liu, G. Kutyniok, and A. Valada, “Roboenvision: A longhorizon video generation model for multi-task robot manipulation,” _arXiv preprint arXiv:2506.22007_ , 2025. 

- [11] Y. LeCun, “A path towards autonomous machine intelligence,” _Open Review_ , vol. 62, no. 1, pp. 1–62, 2022. 

- [12] D. Hafner, T. Lillicrap, J. Ba, and M. Norouzi, “Dream to control: Learning behaviors by latent imagination,” in _International Conference on Learning Representations_ , 2019. 

- [13] D. Hafner, T. P. Lillicrap, M. Norouzi, and J. Ba, “Mastering atari with discrete world models,” in _International Conference on Learning Representations_ , 2021. 

- [14] P. Wu, A. Escontrela, D. Hafner, P. Abbeel, and K. Goldberg, “Daydreamer: World models for physical robot learning,” in _Conference on robot learning_ . PMLR, 2023, pp. 2226–2240. 

- [15] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse domains through world models,” _arXiv preprint arXiv:2301.04104_ , 2023. 

- [16] B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid _et al._ , “Rt-2: Vision-language-action models transfer web knowledge to robotic control,” in _Conference on Robot Learning_ . PMLR, 2023, pp. 2165–2183. 

- [17] J. Huang, S. Yong, X. Ma, X. Linghu, P. Li, Y. Wang, Q. Li, S.C. Zhu, B. Jia, and S. Huang, “An embodied generalist agent in 3d world,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 20 413–20 451. 

- [18] Y. Hong, Z. Zheng, P. Chen, Y. Wang, J. Li, and C. Gan, “Multiply: A multisensory object-centric embodied large language model in 3d world,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 26 406–26 416. 

- [19] M. Yang, Y. Du, K. Ghasemipour, J. Tompson, D. Schuurmans, and P. Abbeel, “Learning interactive real-world simulators,” _arXiv preprint arXiv:2310.06114_ , vol. 1, no. 2, p. 6, 2023. 

- [20] J. Bruce, M. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps _et al._ , “Genie: generative interactive environments,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 4603–4623. 

- [21] J. Guo, X. Ma, Y. Wang, M. Yang, H. Liu, and Q. Li, “Flowdreamer: A rgb-d world model with flow-based motion representations for robot manipulation,” _arXiv preprint arXiv:2505.10075_ , 2025. 

- [22] Q. Bu, J. Zeng, L. Chen, Y. Yang, G. Zhou, J. Yan, P. Luo, H. Cui, Y. Ma, and H. Li, “Closed-loop visuomotor control with generative expectation for robotic manipulation,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 139 002–139 029, 2024. 

- [23] H. Zhu, Y. Wang, J. Zhou, W. Chang, Y. Zhou, Z. Li, J. Chen, C. Shen, J. Pang _et al._ , “Aether: Geometric-aware unified world modeling,” in _ICCV_ , 2025. 

- [24] H. Zhen, Q. Sun, H. Zhang, J. Li, S. Zhou, Y. Du, and C. Gan, “Tesseract: learning 4d embodied world models,” _arXiv preprint arXiv:2504.20995_ , 2025. 

- [25] S. Ferraro, P. Mazzaglia, T. Verbelen, and B. Dhoedt, “Focus: objectcentric world models for robotic manipulation,” _Frontiers in Neurorobotics_ , vol. 19, p. 1585386, 2025. 

- [26] A. Villar-Corrales and S. Behnke, “Playslot: Learning inverse latent dynamics for controllable object-centric video prediction and planning,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [27] L. Chen, Y. Wang, S. Tang, Q. Ma, T. He, W. Ouyang, X. Zhou, H. Bao, and S. Peng, “Egoagent: A joint predictive agent model in egocentric worlds,” _arXiv preprint arXiv:2502.05857_ , 2025. 

- [28] K. Grauman, A. Westbury, L. Torresani, K. Kitani, J. Malik, T. Afouras, K. Ashutosh, V. Baiyya, S. Bansal, B. Boote _et al._ , “Ego-exo4d: Understanding skilled human activity from first-and third-person perspectives,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 19 383–19 400. 

- [29] D. Hafner, T. Lillicrap, I. Fischer, R. Villegas, D. Ha, H. Lee, and J. Davidson, “Learning latent dynamics for planning from pixels,” in _International conference on machine learning_ , 2019, pp. 2555–2565. 

- [30] F. Ebert, S. Dasari, A. X. Lee, S. Levine, and C. Finn, “Robustness via retrying: Closed-loop robotic manipulation with self-supervised learning,” in _Conference on robot learning_ . PMLR, 2018, pp. 983– 993. 

- [31] K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter _et al._ , “ _π_ 0: A visionlanguage-action flow model for general robot control,” _arXiv preprint arXiv:2410.24164_ , 2024. 

- [32] G. R. Team, S. Abeyruwan, J. Ainslie, J.-B. Alayrac, M. G. Arenas, T. Armstrong, A. Balakrishna, R. Baruch, M. Bauza, M. Blokzijl _et al._ , “Gemini robotics: Bringing ai into the physical world,” _arXiv preprint arXiv:2503.20020_ , 2025. 

- [33] L. Barcellona, A. Zadaianchuk, D. Allegro, S. Papa, S. Ghidoni, and E. Gavves, “Dream to manipulate: Compositional world models empowering robot imitation learning with imagination,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [34] G. Lu, B. Jia, P. Li, Y. Chen, Z. Wang, Y. Tang, and S. Huang, “Gwm: Towards scalable gaussian world models for robotic manipulation,” _arXiv preprint arXiv:2508.17600_ , 2025. 

- [35] S. Liu, L. Wu, B. Li, H. Tan, H. Chen, Z. Wang, K. Xu, H. Su, and J. Zhu, “Rdt-1b: a diffusion foundation model for bimanual manipulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [36] C. Finn, I. Goodfellow, and S. Levine, “Unsupervised learning for physical interaction through video prediction,” in _Proceedings of the 30th International Conference on Neural Information Processing Systems_ , 2016, pp. 64–72. 

21 

- [37] S. Sudhakar, R. Liu, B. V. Hoorick, C. Vondrick, and R. Zemel, “Controlling the world by sleight of hand,” in _European Conference on Computer Vision_ . Springer, 2024, pp. 414–430. 

- [38] J. Jang, S. Ye, Z. Lin, J. Xiang, J. Bjorck, Y. Fang, F. Hu, S. Huang, K. Kundalia, Y.-C. Lin _et al._ , “Dreamgen: Unlocking generalization in robot learning through video world models,” _arXiv preprint arXiv:2505.12705_ , 2025. 

- [39] R. Sekar, O. Rybkin, K. Daniilidis, P. Abbeel, D. Hafner, and D. Pathak, “Planning to explore via self-supervised world models,” in _International conference on machine learning_ , 2020, pp. 8583–8592. 

- [40] J. Cen, C. Yu, H. Yuan, Y. Jiang, S. Huang, J. Guo, X. Li, Y. Song, H. Luo, F. Wang _et al._ , “Worldvla: Towards autoregressive action world model,” _arXiv preprint arXiv:2506.21539_ , 2025. 

- [41] H. Zhen, X. Qiu, P. Chen, J. Yang, X. Yan, Y. Du, Y. Hong, and C. Gan, “3d-vla: a 3d vision-language-action generative world model,” in _Proceedings of the 41st International Conference on Machine Learning_ , 2024, pp. 61 229–61 245. 

- [42] Z. Song, S. Qin, T. Chen, L. Lin, and G. Wang, “Physical autoregressive model for robotic manipulation without action pretraining,” _arXiv preprint arXiv:2508.09822_ , 2025. 

- [43] F. Zhu, H. Wu, S. Guo, Y. Liu, C. Cheang, and T. Kong, “Irasim: Learning interactive real-robot action simulators,” in _ICCV_ , 2025. 

- [44] J. Bjorck, F. Casta˜neda, N. Cherniadev, X. Da, R. Ding, L. Fan, Y. Fang, D. Fox, F. Hu, S. Huang _et al._ , “Gr00t n1: An open foundation model for generalist humanoid robots,” _arXiv preprint arXiv:2503.14734_ , 2025. 

- [45] L. Wang, R. Shelim, W. Saad, and N. Ramakrishnan, “Dmwm: Dual-mind world model with long-term imagination,” _arXiv preprint arXiv:2502.07591_ , 2025. 

- [46] J. Yu, Y. Qin, H. Che, Q. Liu, X. Wang, P. Wan, D. Zhang, K. Gai, H. Chen, and X. Liu, “A survey of interactive generative video,” _arXiv preprint arXiv:2504.21853_ , 2025. 

- [47] L. Kong, W. Yang, J. Mei, Y. Liu, A. Liang, D. Zhu, D. Lu, W. Yin, X. Hu, M. Jia _et al._ , “3d and 4d world modeling: A survey,” _arXiv preprint arXiv:2509.07996_ , 2025. 

- [48] B. Ai, S. Tian, H. Shi, Y. Wang, T. Pfaff, C. Tan, H. I. Christensen, H. Su, J. Wu, and Y. Li, “A review of learning-based dynamics models for robotic manipulation,” _Science Robotics_ , vol. 10, no. 106, p. eadt1497, 2025. 

- [49] M. Lin, X. Wang, Y. Wang, S. Wang, F. Dai, P. Ding, C. Wang, Z. Zuo, N. Sang, S. Huang _et al._ , “Exploring the evolution of physics cognition in video generation: A survey,” _arXiv preprint arXiv:2503.21765_ , 2025. 

- [50] X. Long, Q. Zhao, K. Zhang, Z. Zhang, D. Wang, Y. Liu, Z. Shu, Y. Lu, S. Wang, X. Wei _et al._ , “A survey: Learning embodied intelligence from physical simulators and world models,” _arXiv preprint arXiv:2507.00917_ , 2025. 

- [51] Z. Zhu, X. Wang, W. Zhao, C. Min, N. Deng, M. Dou, Y. Wang, B. Shi, K. Wang, C. Zhang _et al._ , “Is sora a world simulator? a comprehensive survey on general world models and beyond,” _arXiv preprint arXiv:2405.03520_ , 2024. 

- [52] W. Liang, R. Zhou, Y. Ma, B. Zhang, S. Li, Y. Liao, and P. Kuang, “Large model empowered embodied ai: A survey on decision-making and embodied learning,” _arXiv preprint arXiv:2508.10399_ , 2025. 

- [53] J. Ding, Y. Zhang, Y. Shang, Y. Zhang, Z. Zong, J. Feng, Y. Yuan, H. Su, N. Li, N. Sukiennik _et al._ , “Understanding world or predicting future? a comprehensive survey of world models,” _ACM Computing Surveys_ , vol. 58, no. 3, pp. 1–38, 2025. 

- [54] D. Driess, F. Xia, M. S. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu _et al._ , “Palm-e: an embodied multimodal language model,” in _Proceedings of the 40th International Conference on Machine Learning_ , 2023, pp. 8469–8488. 

- [55] M. J. Kim, K. Pertsch, S. Karamcheti, T. Xiao, A. Balakrishna, S. Nair, R. Rafailov, E. P. Foster, P. R. Sanketi, Q. Vuong _et al._ , “Openvla: An open-source vision-language-action model,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 2679–2713. 

- [56] C. Gumbsch, N. Sajid, G. Martius, and M. V. Butz, “Learning hierarchical world models with adaptive temporal abstractions from discrete latent dynamics,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [57] Y. Liao, P. Zhou, S. Huang, D. Yang, S. Chen, Y. Jiang, Y. Hu, J. Cai, S. Liu, J. Luo _et al._ , “Genie envisioner: A unified world foundation platform for robotic manipulation,” _arXiv preprint arXiv:2508.05635_ , 2025. 

- [58] C.-L. Cheang, G. Chen, Y. Jing, T. Kong, H. Li, Y. Li, Y. Liu, H. Wu, J. Xu, Y. Yang _et al._ , “Gr-2: A generative video-language-action model with web-scale knowledge for robot manipulation,” _arXiv preprint arXiv:2410.06158_ , 2024. 

- [59] Y. Du, S. Yang, B. Dai, H. Dai, O. Nachum, J. Tenenbaum, D. Schuurmans, and P. Abbeel, “Learning universal policies via text-guided video generation,” _Advances in neural information processing systems_ , vol. 36, pp. 9156–9172, 2023. 

- [60] W. Zhang, H. Liu, Z. Qi, Y. Wang, X. Yu, J. Zhang, R. Dong, J. He, H. Wang, Z. Zhang _et al._ , “Dreamvla: a vision-language-action model dreamed with comprehensive world knowledge,” _arXiv preprint arXiv:2507.04447_ , 2025. 

- [61] Y. Tian, S. Yang, J. Zeng, P. Wang, D. Lin, H. Dong, and J. Pang, “Predictive inverse dynamics models are scalable learners for robotic manipulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [62] M. Ahn, A. Brohan, N. Brown, Y. Chebotar, O. Cortes, B. David, C. Finn, C. Fu, K. Gopalakrishnan, K. Hausman _et al._ , “Do as i can, not as i say: Grounding language in robotic affordances,” _arXiv preprint arXiv:2204.01691_ , 2022. 

- [63] C. Finn and S. Levine, “Deep visual foresight for planning robotic motion,” in _2017 IEEE international conference on robotics and automation_ . IEEE, 2017, pp. 2786–2793. 

- [64] F. Ebert, C. Finn, S. Dasari, A. Xie, A. Lee, and S. Levine, “Visual foresight: Model-based deep reinforcement learning for vision-based robotic control,” _arXiv preprint arXiv:1812.00568_ , 2018. 

- [65] C. Gao, H. Zhang, Z. Xu, C. Zhehao, and L. Shao, “Flip: Flow-centric generative planning as general-purpose manipulation world model,” in _The Thirteenth International Conference on Learning Representations_ , 2024. 

- [66] S. Zhou, Y. Du, J. Chen, Y. Li, D.-Y. Yeung, and C. Gan, “Robodreamer: Learning compositional world models for robot imagination,” in _International Conference on Machine Learning_ . PMLR, 2024, pp. 61 885–61 896. 

- [67] M. Rigter, T. Gupta, A. Hilmkil, and C. Ma, “Avid: Adapting video diffusion models to world models,” in _Reinforcement Learning Conference_ , 2025. 

- [68] K. Black, M. Nakamoto, P. Atreya, H. R. Walke, C. Finn, A. Kumar, and S. Levine, “Zero-shot robotic manipulation with pre-trained imageediting diffusion models,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [69] H. Zhi, P. Chen, S. Zhou, Y. Dong, Q. Wu, L. Han, and M. Tan, “3dflowaction: Learning cross-embodiment manipulation from 3d flow world model,” _arXiv preprint arXiv:2506.06199_ , 2025. 

- [70] P.-C. Ko, J. Mao, Y. Du, S.-H. Sun, and J. B. Tenenbaum, “Learning to act from actionless videos through dense correspondences,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [71] C. Zhu, R. Yu, S. Feng, B. Burchfiel, P. Shah, and A. Gupta, “Unified world models: Coupling video and action diffusion for pretraining on large robotic datasets,” _arXiv preprint arXiv:2504.02792_ , 2025. 

- [72] J. Xiang, G. Liu, Y. Gu, Q. Gao, Y. Ning, Y. Zha, Z. Feng, T. Tao, S. Hao, Y. Shi _et al._ , “Pandora: Towards general world model with natural language actions and video states,” _arXiv preprint arXiv:2406.09455_ , 2024. 

- [73] L. Wang, K. Zhao, C. Liu, and X. Chen, “Learning real-world actionvideo dynamics with heterogeneous masked autoregression,” _arXiv preprint arXiv:2502.04296_ , 2025. 

- [74] J. Quevedo, P. Liang, and S. Yang, “Evaluating robot policies in a world model,” _arXiv preprint arXiv:2506.00613_ , 2025. 

- [75] Z. Ren, Y. Wei, X. Guo, Y. Zhao, B. Kang, J. Feng, and X. Jin, “Videoworld: Exploring knowledge learning from unlabeled videos,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 29 029–29 039. 

- [76] S. Nair, E. Mitchell, K. Chen, S. Savarese, C. Finn _et al._ , “Learning language-conditioned robot behavior from offline data and crowdsourced annotation,” in _Conference on Robot Learning_ . PMLR, 2022, pp. 1303–1315. 

- [77] M. Assran, A. Bardes, D. Fan, Q. Garrido, R. Howes, M. Muckley, A. Rizvi, C. Roberts, K. Sinha, A. Zholus _et al._ , “V-jepa 2: Selfsupervised video models enable understanding, prediction and planning,” _arXiv preprint arXiv:2506.09985_ , 2025. 

- [78] J. Zhang, Y. Guo, Y. Hu, X. Chen, X. Zhu, and J. Chen, “Up-vla: A unified understanding and prediction model for embodied agent,” _ICML_ , 2025. 

- [79] Q. Zhao, Y. Lu, M. J. Kim, Z. Fu, Z. Zhang, Y. Wu, Z. Li, Q. Ma, S. Han, C. Finn _et al._ , “Cot-vla: Visual chain-of-thought reasoning for vision-language-action models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 1702–1713. 

- [80] E. Xing, M. Deng, J. Hou, and Z. Hu, “Critiques of world models,” _arXiv preprint arXiv:2507.05169_ , 2025. 

22 

- [81] NVIDIA. (2025) World models. [Online]. Available: https://www. nvidia.com/en-au/glossary/world-models 

- [82] D. Chen, T. Moutakanni, W. Chung, Y. Bang, Z. Ji, A. Bolourchi, and P. Fung, “Planning with reasoning using vision language world model,” _arXiv preprint arXiv:2509.02722_ , 2025. 

- [83] Y. Hu, F. Lin, T. Zhang, L. Yi, and Y. Gao, “Look before you leap: Unveiling the power of gpt-4v in robotic vision-language planning,” _arXiv preprint arXiv:2311.17842_ , 2023. 

- [84] W. Zhao, J. Chen, Z. Meng, D. Mao, R. Song, and W. Zhang, “Vlmpc: Vision-language model predictive control for robotic manipulation,” _arXiv preprint arXiv:2407.09829_ , 2024. 

- [85] Y. Hong, H. Zhen, P. Chen, S. Zheng, Y. Du, Z. Chen, and C. Gan, “3d-llm: Injecting the 3d world into large language models,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 20 482–20 494, 2023. 

- [86] Y. Wang, R. Yu, S. Wan, L. Gan, and D.-C. Zhan, “Founder: Grounding foundation models in world models for open-ended embodied decision making,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [87] I. Team, “Internlm: A multilingual language model with progressively enhanced capabilities,” 2023. 

- [88] J. Schrittwieser, I. Antonoglou, T. Hubert, K. Simonyan, L. Sifre, S. Schmitt, A. Guez, E. Lockhart, D. Hassabis, T. Graepel _et al._ , “Mastering atari, go, chess and shogi by planning with a learned model,” _Nature_ , vol. 588, no. 7839, pp. 604–609, 2020. 

- [89] W. Ye, S. Liu, T. Kurutach, P. Abbeel, and Y. Gao, “Mastering atari games with limited data,” _Advances in neural information processing systems_ , vol. 34, pp. 25 476–25 488, 2021. 

- [90] S. Wang, S. Liu, W. Ye, J. You, and Y. Gao, “Efficientzero v2: Mastering discrete and continuous control with limited data,” _arXiv preprint arXiv:2403.00564_ , 2024. 

- [91] D. Silver, T. Hubert, J. Schrittwieser, I. Antonoglou, M. Lai, A. Guez, M. Lanctot, L. Sifre, D. Kumaran, T. Graepel _et al._ , “A general reinforcement learning algorithm that masters chess, shogi, and go through self-play,” _Science_ , vol. 362, no. 6419, pp. 1140–1144, 2018. 

- [92] T. Brooks, B. Peebles, C. Holmes, W. DePue, Y. Guo, L. Jing, D. Schnurr, J. Taylor, T. Luhman, E. Luhman _et al._ , “Video generation models as world simulators,” _OpenAI Blog_ , vol. 1, no. 8, p. 1, 2024. 

- [93] Z. Zheng, X. Peng, T. Yang, C. Shen, S. Li, H. Liu, Y. Zhou, T. Li, and Y. You, “Open-sora: Democratizing efficient video production for all,” _arXiv preprint arXiv:2412.20404_ , 2024. 

- [94] M. Q. Ali, A. Sridhar, S. Matiana, A. Wong, and M. Al-Sharman, “Humanoid world models: Open world foundation models for humanoid robotics,” _arXiv preprint arXiv:2506.01182_ , 2025. 

- [95] J. Ho, T. Salimans, A. Gritsenko, W. Chan, M. Norouzi, and D. J. Fleet, “Video diffusion models,” _Advances in neural information processing systems_ , vol. 35, pp. 8633–8646, 2022. 

- [96] N. Agarwal, A. Ali, M. Bala, Y. Balaji, E. Barker, T. Cai, P. Chattopadhyay, Y. Chen, Y. Cui, Y. Ding _et al._ , “Cosmos world foundation model platform for physical ai,” _arXiv preprint arXiv:2501.03575_ , 2025. 

- [97] T. Wan, A. Wang, B. Ai, B. Wen, C. Mao, C.-W. Xie, D. Chen, F. Yu, H. Zhao, J. Yang _et al._ , “Wan: Open and advanced large-scale video generative models,” _arXiv preprint arXiv:2503.20314_ , 2025. 

- [98] H. Song, D. Qu, Y. Yao, Q. Chen, Q. Lv, Y. Tang, M. Shi, G. Ren, M. Yao, B. Zhao _et al._ , “Hume: Introducing system-2 thinking in visual-language-action model,” _arXiv preprint arXiv:2505.21432_ , 2025. 

- [99] D. P. Kingma and M. Welling, “Auto-encoding variational bayes,” _arXiv preprint arXiv:1312.6114_ , 2013. 

- [100] D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap, “Mastering diverse control tasks through world models,” _Nature_ , pp. 1–7, 2025. 

- [101] P. Mazzaglia, T. Verbelen, B. Dhoedt, A. Courville, and S. Rajeswar, “Genrl: Multimodal-foundation world models for generalization in embodied agents,” _Advances in neural information processing systems_ , vol. 37, pp. 27 529–27 555, 2024. 

- [102] D. Kahneman, _Thinking, fast and slow_ . macmillan, 2011. [103] Z. Zhou, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Vision-languageaction model with open-world embodied reasoning from pretrained knowledge,” _arXiv preprint arXiv:2505.21906_ , 2025. 

- [104] N. A. Hansen, H. Su, and X. Wang, “Temporal difference learning for model predictive control,” in _International Conference on Machine Learning_ , 2022, pp. 8387–8406. 

- [105] N. Hansen, H. Su, and X. Wang, “Td-mpc2: Scalable, robust world models for continuous control,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [106] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby _et al._ , “Dinov2: 

Learning robust visual features without supervision,” _Transactions on Machine Learning Research Journal_ , pp. 1–31, 2024. 

- [107] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo _et al._ , “Segment anything,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2023, pp. 4015–4026. 

- [108] J. Liang, P. Tokmakov, R. Liu, S. Sudhakar, P. Shah, R. Ambrus, and C. Vondrick, “Video generators are robot policies,” _arXiv preprint arXiv:2508.00795_ , 2025. 

- [109] N. Karaev, I. Rocco, B. Graham, N. Neverova, A. Vedaldi, and C. Rupprecht, “Cotracker: It is better to track together,” in _European conference on computer vision_ . Springer, 2024, pp. 18–35. 

- [110] N. Karaev, I. Makarov, J. Wang, N. Neverova, A. Vedaldi, and C. Rupprecht, “Cotracker3: Simpler and better point tracking by pseudolabelling real videos,” _arXiv preprint arXiv:2410.11831_ , 2024. 

- [111] Y. Guo, Y. Hu, J. Zhang, Y.-J. Wang, X. Chen, C. Lu, and J. Chen, “Prediction with action: Visual policy learning via joint denoising process,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 112 386–112 410, 2024. 

- [112] Q. Bu, J. Cai, L. Chen, X. Cui, Y. Ding, S. Feng, S. Gao, X. He, X. Hu, X. Huang _et al._ , “Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems,” _arXiv preprint arXiv:2503.06669_ , 2025. 

- [113] S. Ye, J. Jang, B. Jeon, S. J. Joo, J. Yang, B. Peng, A. Mandlekar, R. Tan, Y.-W. Chao, B. Y. Lin _et al._ , “Latent action pretraining from videos,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [114] B. Baker, I. Akkaya, P. Zhokov, J. Huizinga, J. Tang, A. Ecoffet, B. Houghton, R. Sampedro, and J. Clune, “Video pretraining (vpt): Learning to act by watching unlabeled online videos,” _Advances in Neural Information Processing Systems_ , vol. 35, pp. 24 639–24 654, 2022. 

- [115] Y. Angen, “Gigabrain-0: A world model-powered vision-languageaction model,” _arXiv:2510.19430_ , 2025. 

- [116] L. Liu, X. Wang, G. Zhao, K. Li, W. Qin, J. Qiu, Z. Zhu, G. Huang, and Z. Su, “Robotransfer: Geometry-consistent video diffusion for robotic visual policy transfer,” _arXiv preprint arXiv:2505.23171_ , 2025. 

- [117] A. Azzolini, J. Bai, H. Brandon, J. Cao, P. Chattopadhyay, H. Chen, J. Chu, Y. Cui, J. Diamond, Y. Ding _et al._ , “Cosmos-reason1: From physical common sense to embodied reasoning,” _arXiv preprint arXiv:2503.15558_ , 2025. 

- [118] B. Kerbl, G. Kopanas, T. Leimk¨uhler, and G. Drettakis, “3d gaussian splatting for real-time radiance field rendering.” _ACM Trans. Graph._ , vol. 42, no. 4, p. 1–14, 2023. 

- [119] J. Xiao, Y. Yang, X. Chang, R. Chen, F. Xiong, M. Xu, W.-S. Zheng, and Q. Zhang, “World-env: Leveraging world model as a virtual environment for vla post-training,” _arXiv preprint arXiv:2509.24948_ , 2025. 

- [120] E. Todorov, T. Erez, and Y. Tassa, “Mujoco: A physics engine for model-based control,” in _2012 IEEE/RSJ international conference on intelligent robots and systems_ . IEEE, 2012, pp. 5026–5033. 

- [121] T. Erez, Y. Tassa, and E. Todorov, “Simulation tools for model-based robotics: Comparison of bullet, havok, mujoco, ode and physx,” in _2015 IEEE international conference on robotics and automation (ICRA)_ . IEEE, 2015, pp. 4397–4404. 

- [122] R. Tedrake _et al._ , “Drake: Model-based design and verification for robotics,” 2019. 

- [123] N. S¨underhauf, O. Brock, W. Scheirer, R. Hadsell, D. Fox, J. Leitner, B. Upcroft, P. Abbeel, W. Burgard, M. Milford _et al._ , “The limits and potentials of deep learning for robotics,” _The International journal of robotics research_ , vol. 37, no. 4-5, pp. 405–420, 2018. 

- [124] A. Afzal, D. S. Katz, C. L. Goues, and C. S. Timperley, “A study on the challenges of using robotics simulators for testing,” _arXiv preprint arXiv:2004.07368_ , 2020. 

- [125] H. Choi, C. Crump, C. Duriez, A. Elmquist, G. Hager, D. Han, F. Hearl, J. Hodgins, A. Jain, F. Leve _et al._ , “On the use of simulation in robotics: Opportunities, challenges, and suggestions for moving forward,” _Proceedings of the National Academy of Sciences_ , vol. 118, no. 1, p. e1907856118, 2021. 

- [126] G. Dulac-Arnold, D. Mankowitz, and T. Hester, “Challenges of realworld reinforcement learning,” _arXiv preprint arXiv:1904.12901_ , 2019. 

- [127] W. Zhao, J. P. Queralta, and T. Westerlund, “Sim-to-real transfer in deep reinforcement learning for robotics: a survey,” in _2020 IEEE symposium series on computational intelligence (SSCI)_ . IEEE, 2020, pp. 737–744. 

- [128] A. Dosovitskiy, G. Ros, F. Codevilla, A. Lopez, and V. Koltun, “Carla: An open urban driving simulator,” in _Conference on robot learning_ , 2017, pp. 1–16. 

23 

- [129] M. Deitke, W. Han, A. Herrasti, A. Kembhavi, E. Kolve, R. Mottaghi, J. Salvador, D. Schwenk, E. VanderBilt, M. Wallingford _et al._ , “Robothor: An open simulation-to-real embodied ai platform,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2020, pp. 3164–3174. 

- [130] Y. Li, Y. Zhu, J. Wen, C. Shen, and Y. Xu, “Worldeval: World model as real-world robot policies evaluator,” _arXiv preprint arXiv:2505.19017_ , 2025. 

- [131] G. Team, R. Anil, S. Borgeaud, J.-B. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican _et al._ , “Gemini: a family of highly capable multimodal models,” _arXiv preprint arXiv:2312.11805_ , 2023. 

- [132] A. Hurst, A. Lerer, A. P. Goucher, A. Perelman, A. Ramesh, A. Clark, A. Ostrow, A. Welihinda, A. Hayes, A. Radford _et al._ , “Gpt-4o system card,” _arXiv preprint arXiv:2410.21276_ , 2024. 

- [133] H. He, Y. Zhang, L. Lin, Z. Xu, and L. Pan, “Pre-trained video generative models as world simulators,” _arXiv preprint arXiv:2502.07825_ , 2025. 

- [134] A. Escontrela, A. Adeniji, W. Yan, A. Jain, X. B. Peng, K. Goldberg, Y. Lee, D. Hafner, and P. Abbeel, “Video prediction models as rewards for reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 68 760–68 783, 2023. 

- [135] H. Deng, T. Pan, H. Diao, Z. Luo, Y. Cui, H. Lu, S. Shan, Y. Qi, and X. Wang, “Autoregressive video generation without vector quantization,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [136] S. Deng, M. Yan, S. Wei, H. Ma, Y. Yang, J. Chen, Z. Zhang, T. Yang, X. Zhang, H. Cui _et al._ , “Graspvla: a grasping foundation model pre-trained on billion-scale synthetic action data,” _arXiv preprint arXiv:2505.03233_ , 2025. 

- [137] J. Zheng, J. Li, D. Liu, Y. Zheng, Z. Wang, Z. Ou, Y. Liu, J. Liu, Y.-Q. Zhang, and X. Zhan, “Universal actions for enhanced embodied foundation models,” in _Proceedings of the Computer Vision and Pattern Recognition Conference_ , 2025, pp. 22 508–22 519. 

- [138] R. Doshi, H. R. Walke, O. Mees, S. Dasari, and S. Levine, “Scaling cross-embodied learning: One policy for manipulation, navigation, locomotion and aviation,” in _Conference on Robot Learning_ . PMLR, 2025, pp. 496–512. 

- [139] O. M. Team, D. Ghosh, H. Walke, K. Pertsch, K. Black, O. Mees, S. Dasari, J. Hejna, T. Kreiman, C. Xu _et al._ , “Octo: An open-source generalist robot policy,” _arXiv preprint arXiv:2405.12213_ , 2024. 

- [140] L. Wang, X. Chen, J. Zhao, and K. He, “Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers,” _Advances in neural information processing systems_ , vol. 37, pp. 124 420–124 450, 2024. 

- [141] S. Gao, S. Zhou, Y. Du, J. Zhang, and C. Gan, “Adaworld: Learning adaptable world models with latent actions,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [142] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International conference on machine learning_ . PmLR, 2021, pp. 8748–8763. 

- [143] M. Javaheripi, S. Bubeck, M. Abdin, J. Aneja, S. Bubeck, C. C. T. Mendes, W. Chen, A. Del Giorno, R. Eldan, S. Gopi _et al._ , “Phi-2: The surprising power of small language models,” _Microsoft Research Blog_ , vol. 1, no. 3, p. 3, 2023. 

- [144] K. He, X. Chen, S. Xie, Y. Li, P. Doll´ar, and R. Girshick, “Masked autoencoders are scalable vision learners,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 16 000–16 009. 

- [145] Y. Li, X. Wei, X. Chi, Y. Li, Z. Zhao, H. Wang, N. Ma, M. Lu, and S. Zhang, “Manipdreamer: Boosting robotic manipulation world model with action tree and visual guidance,” _arXiv preprint arXiv:2504.16464_ , 2025. 

- [146] P. Dhariwal and A. Nichol, “Diffusion models beat gans on image synthesis,” _Advances in neural information processing systems_ , vol. 34, pp. 8780–8794, 2021. 

- [147] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds _et al._ , “Flamingo: a visual language model for few-shot learning,” _Advances in neural information processing systems_ , vol. 35, pp. 23 716–23 736, 2022. 

- [148] F. Mentzer, D. Minnen, E. Agustsson, and M. Tschannen, “Finite scalar quantization: Vq-vae made simple,” in _The Twelfth International Conference on Learning Representations_ , 2025. 

- [149] L. Yang, B. Kang, Z. Huang, X. Xu, J. Feng, and H. Zhao, “Depth anything: Unleashing the power of large-scale unlabeled data,” in 

   - _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2024, pp. 10 371–10 381. 

- [150] Z. Chen, J. Huo, Y. Chen, and Y. Gao, “Robohorizon: An llm-assisted multi-view world model for long-horizon robotic manipulation,” _arXiv preprint arXiv:2501.06605_ , 2025. 

- [151] H. Wu, Y. Jing, C. Cheang, G. Chen, J. Xu, X. Li, M. Liu, H. Li, and T. Kong, “Unleashing large-scale video generative pre-training for visual robot manipulation,” in _The Twelfth International Conference on Learning Representations_ , 2024. 

- [152] A. Bardes, Q. Garrido, J. Ponce, X. Chen, M. Rabbat, Y. LeCun, M. Assran, and N. Ballas, “Revisiting feature prediction for learning visual representations from video,” _arXiv preprint arXiv:2404.08471_ , 2024. 

- [153] C. Cheang, S. Chen, Z. Cui, Y. Hu, L. Huang, T. Kong, H. Li, Y. Li, Y. Liu, X. Ma _et al._ , “Gr-3 technical report,” _arXiv preprint arXiv:2507.15493_ , 2025. 

- [154] K. Black, N. Brown, J. Darpinian, K. Dhabalia, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai _et al._ , “ _π_ 0 _._ 5: a vision-language-action model with open-world generalization,” _arXiv preprint arXiv:2504.16054_ , 2025. 

- [155] J. Ho, A. Jain, and P. Abbeel, “Denoising diffusion probabilistic models,” _Advances in neural information processing systems_ , vol. 33, pp. 6840–6851, 2020. 

- [156] N. Kitaev, S. Cao, and D. Klein, “Multilingual constituency parsing with self-attention and pre-training,” in _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , 2019, pp. 3499–3505. 

- [157] J.-C. Pang, N. Tang, K. Li, Y. Tang, X.-Q. Cai, Z.-Y. Zhang, G. Niu, M. Sugiyama, and Y. Yu, “Learning view-invariant world models for visual robotic manipulation,” in _The Thirteenth International Conference on Learning Representations_ , 2025. 

- [158] F. Martinez-Lopez, T. Li, Y. Lu, and J. Chen, “In-context reinforcement learning via communicative world models,” _arXiv preprint arXiv:2508.06659_ , 2025. 

- [159] J. Wu, H. Ma, C. Deng, and M. Long, “Pre-training contextualized world models with in-the-wild videos for reinforcement learning,” _Advances in Neural Information Processing Systems_ , vol. 36, pp. 39 719–39 743, 2023. 

- [160] B. Kang, Y. Yue, R. Lu, Z. Lin, Y. Zhao, K. Wang, G. Huang, and J. Feng, “How far is video generation from world model: A physical law perspective,” in _Forty-second International Conference on Machine Learning_ , 2025. 

- [161] X. Yang, B. Li, Y. Zhang, Z. Yin, L. Bai, L. Ma, Z. Wang, J. Cai, T.-T. Wong, H. Lu _et al._ , “Vlipp: Towards physically plausible video generation with vision and language informed physical prior,” _arXiv preprint arXiv:2503.23368_ , 2025. 

- [162] J. Peper, Z. Mao, Y. Geng, S. Pan, and I. Ruchkin, “Four principles for physically interpretable world models,” _arXiv preprint arXiv:2503.02143_ , 2025. 

- [163] S. Zhou, Y. Du, Y. Yang, L. Han, P. Chen, D.-Y. Yeung, and C. Gan, “Learning 3d persistent embodied world models,” _arXiv preprint arXiv:2505.05495_ , 2025. 

- [164] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, “High-resolution image synthesis with latent diffusion models,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 10 684–10 695. 

- [165] T. Souˇcek, D. Damen, M. Wray, I. Laptev, and J. Sivic, “Genhowto: Learning to generate actions and state transformations from instructional videos,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 6561–6571. 

- [166] Y. Wen, J. Lin, Y. Zhu, J. Han, H. Xu, S. Zhao, and X. Liang, “Vidman: Exploiting implicit dynamics from video diffusion model for effective robot manipulation,” _Advances in Neural Information Processing Systems_ , vol. 37, pp. 41 051–41 075, 2024. 

- [167] A. Brohan, N. Brown, J. Carbajal, Y. Chebotar, J. Dabis, C. Finn, K. Gopalakrishnan, K. Hausman, A. Herzog, J. Hsu _et al._ , “Rt-1: Robotics transformer for real-world control at scale,” _Robotics: Science and Systems_ , 2023. 

- [168] A. Miech, D. Zhukov, J.-B. Alayrac, M. Tapaswi, I. Laptev, and J. Sivic, “Howto100m: Learning a text-video embedding by watching hundred million narrated video clips,” in _Proceedings of the IEEE/CVF international conference on computer vision_ , 2019, pp. 2630–2640. 

- [169] K. Grauman, A. Westbury, E. Byrne, Z. Chavis, A. Furnari, R. Girdhar, J. Hamburger, H. Jiang, M. Liu, X. Liu _et al._ , “Ego4d: Around the world in 3,000 hours of egocentric video,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2022, pp. 18 995–19 012. 

24 

- [170] R. Goyal, S. Ebrahimi Kahou, V. Michalski, J. Materzynska, S. Westphal, H. Kim, V. Haenel, I. Fruend, P. Yianilos, M. Mueller-Freitag _et al._ , “The” something something” video database for learning and evaluating visual common sense,” in _Proceedings of the IEEE international conference on computer vision_ , 2017, pp. 5842–5850. 

- [171] D. Damen, H. Doughty, G. M. Farinella, S. Fidler, A. Furnari, E. Kazakos, D. Moltisanti, J. Munro, T. Perrett, W. Price _et al._ , “Scaling egocentric vision: The epic-kitchens dataset,” in _Proceedings of the European conference on computer vision (ECCV)_ , 2018, pp. 720–736. 

- [172] J. Carreira, E. Noland, C. Hillier, and A. Zisserman, “A short note on the kinetics-700 human action dataset,” _arXiv preprint arXiv:1907.06987_ , 2019. 

- [173] H. R. Walke, K. Black, T. Z. Zhao, Q. Vuong, C. Zheng, P. HansenEstruch, A. W. He, V. Myers, M. J. Kim, M. Du _et al._ , “Bridgedata v2: A dataset for robot learning at scale,” in _Conference on Robot Learning_ , 2023, pp. 1723–1736. 

- [174] S. K. Ramakrishnan, A. Gokaslan, E. Wijmans, O. Maksymets, A. Clegg, J. M. Turner, E. Undersander, W. Galuba, A. Westbury, A. X. Chang _et al._ , “Habitat-matterport 3d dataset (hm3d): 1000 largescale 3d environments for embodied ai,” in _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ , 2021. 

- [175] C. Lynch, A. Wahid, J. Tompson, T. Ding, J. Betker, R. Baruch, T. Armstrong, and P. Florence, “Interactive language: Talking to robots in real time,” _IEEE Robotics and Automation Letters_ , 2023. 

- [176] F. Ebert, Y. Yang, K. Schmeckpeper, B. Bucher, G. Georgakis, K. Daniilidis, C. Finn, and S. Levine, “Bridge data: Boosting generalization of robotic skills with cross-domain datasets,” _arXiv preprint arXiv:2109.13396_ , 2021. 

- [177] A. Chang, A. Dai, T. Funkhouser, M. Halber, M. Niebner, M. Savva, S. Song, A. Zeng, and Y. Zhang, “Matterport3d: Learning from rgb-d data in indoor environments,” in _2017 International Conference on 3D Vision (3DV)_ . IEEE Computer Society, 2017, pp. 667–676. 

- [178] A. O’Neill, A. Rehman, A. Maddukuri, A. Gupta, A. Padalkar, A. Lee, A. Pooley, A. Gupta, A. Mandlekar, A. Jain _et al._ , “Open x-embodiment: Robotic learning datasets and rt-x models: Open x- embodiment collaboration 0,” in _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2024, pp. 6892–6903. 

- [179] A. Khazatsky, K. Pertsch, S. Nair, A. Balakrishna, S. Dasari, S. Karamcheti, S. Nasiriany, M. K. Srirama, L. Y. Chen, K. Ellis _et al._ , “Droid: A large-scale in-the-wild robot manipulation dataset,” _arXiv preprint arXiv:2403.12945_ , 2024. 

- [180] J. Gu, F. Xiang, X. Li, Z. Ling, X. Liu, T. Mu, Y. Tang, S. Tao, X. Wei, Y. Yao _et al._ , “Maniskill2: A unified benchmark for generalizable manipulation skills,” in _The Eleventh International Conference on Learning Representations_ , 2023. 

- [181] A. Mandlekar, J. Booher, M. Spero, A. Tung, A. Gupta, Y. Zhu, A. Garg, S. Savarese, and L. Fei-Fei, “Scaling robot supervision to hundreds of hours with roboturk: Robotic manipulation dataset through human reasoning and dexterity,” in _2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2019, pp. 1048–1055. 

- [182] S. James, Z. Ma, D. R. Arrojo, and A. J. Davison, “Rlbench: The robot learning benchmark & learning environment,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3019–3026, 2020. 

- [183] Z. Chen, Z. Shi, X. Lu, L. He, S. Qian, Z. Yin, W. Ouyang, J. Shao, Y. Qiao, C. Lu _et al._ , “Rh20t-p: A primitive-level robotic manipulation dataset towards composable generalization agents in real-world scenarios,” in _NeurIPS 2024 Workshop on Open-World Agents_ , 2024. 

- [184] S. Dasari, F. Ebert, S. Tian, S. Nair, B. Bucher, K. Schmeckpeper, S. Singh, S. Levine, and C. Finn, “Robonet: Large-scale multi-robot learning,” in _Conference on Robot Learning_ , 2020, pp. 885–897. 

   - [189] E. Rosete-Beas, O. Mees, G. Kalweit, J. Boedecker, and W. Burgard, “Latent plans for task-agnostic offline reinforcement learning,” in _Conference on Robot Learning_ , 2023, pp. 1838–1849. 

   - [190] M. Mittal, C. Yu, Q. Yu, J. Liu, N. Rudin, D. Hoeller, J. L. Yuan, R. Singh, Y. Guo, H. Mazhar _et al._ , “Orbit: A unified simulation framework for interactive robot learning environments,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 6, pp. 3740–3747, 2023. 

   - [191] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

   - [192] J. Richens and T. Everitt, “Robust agents learn causal world models,” _arXiv preprint arXiv:2402.10877_ , 2024. 

   - [193] Z. Wang, X. Xiao, Z. Xu, Y. Zhu, and P. Stone, “Causal dynamics learning for task-independent state abstraction,” in _International Conference on Machine Learning_ , 2022, pp. 23 151–23 180. 

   - [194] M. Tomar, A. Zhang, R. Calandra, M. E. Taylor, and J. Pineau, “Modelinvariant state abstractions for model-based reinforcement learning,” _arXiv preprint arXiv:2102.09850_ , 2021. 

   - [195] T. Gupta, W. Gong, C. Ma, N. Pawlowski, A. Hilmkil, M. Scetbon, M. Rigter, A. Famoti, A. J. Llorens, J. Gao _et al._ , “The essential role of causality in foundation world models for embodied ai,” _arXiv preprint arXiv:2402.06665_ , 2024. 

   - [196] E. A. Stuart, “Matching methods for causal inference: A review and a look forward,” _Statistical science: a review journal of the Institute of Mathematical Statistics_ , vol. 25, no. 1, p. 1, 2010. 

   - [197] V. Chernozhukov, D. Chetverikov, M. Demirer, E. Duflo, C. Hansen, W. Newey, and J. Robins, “Double/debiased machine learning for treatment and structural parameters,” _The Econometrics Journal_ , pp. C1–C68, 2018. 

   - [198] A. Polino, R. Pascanu, and D. Alistarh, “Model compression via distillation and quantization,” in _International Conference on Learning Representations_ , 2018. 

   - [199] A. Gholami, S. Kim, Z. Dong, Z. Yao, M. W. Mahoney, and K. Keutzer, “A survey of quantization methods for efficient neural network inference,” in _Low-power computer vision_ . Chapman and Hall/CRC, 2022, pp. 291–326. 

   - [200] Y. Shang, Z. Yuan, B. Xie, B. Wu, and Y. Yan, “Post-training quantization on diffusion models,” in _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2023, pp. 1972–1981. 

   - [201] Y. Li, T. Chen, P.-F. Zhang, and H. Yin, “Lightweight self-attentive sequential recommendation,” in _Proceedings of the 30th ACM international conference on information & knowledge management_ , 2021, pp. 967–977. 

   - [202] C. Szegedy, W. Zaremba, I. Sutskever, J. Bruna, D. Erhan, I. Goodfellow, and R. Fergus, “Intriguing properties of neural networks,” _arXiv preprint arXiv:1312.6199_ , 2013. 

   - [203] P.-F. Zhang, Z. Huang, and G. Bai, “Universal adversarial perturbations for vision-language pre-trained models,” in _Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval_ , 2024, pp. 862–871. 

   - [204] J. Ren, Y. Zhou, J. Jin, L. Lyu, and D. Yan, “Dimension-independent certified neural network watermarks via mollifier smoothing,” in _ICML_ . PMLR, 2023, pp. 28 976–29 008. 

   - [205] N. Park and S. Kim, “Blurs behave like ensembles: Spatial smoothings to improve accuracy, uncertainty, and robustness,” in _ICML_ , 2022, pp. 17 390–17 419. 

   - [206] L. Cojocar, J. Kim, M. Patel, L. Tsai, S. Saroiu, A. Wolman, and O. Mutlu, “Are we susceptible to rowhammer? an end-to-end methodology for cloud providers,” in _SP_ , 2020, pp. 712–728. 

   - [207] P. Jattke, M. Wipfli, F. Solt, M. Marazzi, M. B¨olcskei, and K. Razavi, “ _{_ ZenHammer _}_ : Rowhammer attacks on _{_ AMD _}_ zen-based platforms,” in _USENIX Security_ , 2024, pp. 1615–1633. 

- [185] C. Schuhmann, R. Vencu, R. Beaumont, R. Kaczmarczyk, C. Mullis, A. Katta, T. Coombes, J. Jitsev, and A. Komatsuzaki, “Laion-400m: Open dataset of clip-filtered 400 million image-text pairs,” _arXiv preprint arXiv:2111.02114_ , 2021. 

- [186] D. Kalashnikov, A. Irpan, P. Pastor, J. Ibarz, A. Herzog, E. Jang, D. Quillen, E. Holly, M. Kalakrishnan, V. Vanhoucke _et al._ , “Scalable deep reinforcement learning for vision-based robotic manipulation,” in _Conference on robot learning_ , 2018, pp. 651–673. 

- [187] X. Ma, Y. Wang, X. Chen, G. Jia, Z. Liu, Y.-F. Li, C. Chen, and Y. Qiao, “Latte: Latent diffusion transformer for video generation,” _Transactions on Machine Learning Research_ , 2025. 

- [188] J. Ho, W. Chan, C. Saharia, J. Whang, R. Gao, A. Gritsenko, D. P. Kingma, B. Poole, M. Norouzi, D. J. Fleet _et al._ , “Imagen video: High definition video generation with diffusion models,” _arXiv preprint arXiv:2210.02303_ , 2022. 

