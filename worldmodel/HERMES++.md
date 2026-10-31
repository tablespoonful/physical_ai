---
title: "HERMES++: Toward a Unified Driving World Model for 3D Scene Understanding and Generation"
date: "2026-04-30"
authors: "Xin Zhou; Dingkang Liang; Xiwu Chen; Feiyang Tan; Dingyuan Zhang; Hengshuang Zhao"
url: https://arxiv.org/abs/2604.28196
pdf: https://arxiv.org/pdf/2604.28196
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2604.28196)** / [論文ページ](https://arxiv.org/abs/2604.28196)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

1 

# HERMES++: Toward a Unified Driving World Model for 3D Scene Understanding and Generation Xin Zhou, Dingkang Liang, Xiwu Chen, Feiyang Tan, Dingyuan Zhang, Hengshuang Zhao, Xiang Bai<sup>�</sup> , Fellow, IEEE 

**_Abstract_ —Driving world models serve as a pivotal technology for autonomous driving by simulating environmental dynamics. However, existing approaches predominantly focus on future scene generation, often overlooking comprehensive 3D scene understanding. Conversely, while Large Language Models (LLMs) demonstrate impressive reasoning capabilities, they lack the capacity to predict future geometric evolution, creating a significant disparity between semantic interpretation and physical simulation. To bridge this gap, we propose HERMES++, a unified driving world model that integrates 3D scene understanding and future geometry prediction within a single framework. Our approach addresses the distinct requirements of these tasks through synergistic designs. First, a BEV representation consolidates multiview spatial information into a structure compatible with LLMs. Second, we introduce LLM-enhanced world queries to facilitate knowledge transfer from the understanding branch. Third, a Current-to-Future Link is designed to bridge the temporal gap, conditioning geometric evolution on semantic context. Finally, to enforce structural integrity, we employ a Joint Geometric Optimization strategy that integrates explicit geometric constraints with implicit latent regularization to align internal representations with geometry-aware priors. Extensive evaluations on multiple benchmarks validate the effectiveness of our method. HERMES++ achieves strong performance, outperforming specialist approaches in both future point cloud prediction and 3D scene understanding tasks. The model and code will be publicly released at https://github.com/H-EmbodVis/HERMESV2.** 

**_Index Terms_ —Driving world model, scene understanding, future point cloud generation.** 

## I. INTRODUCTION 

**D** RIVINGpotential forworldenhancingmodelsenhancingmodels autonomous[1], [2], [3],driving[4] showreliabilitygreat 

potential forworldenhancingmodelsenhancingmodels autonomous[1], driving[4] reliabilitygreat by simulating environmental dynamics. These models enable vehicles to forecast risks and optimize decisions. Existing research primarily focuses on predicting scene evolution, targeting either visual appearance changes [2], [5] or 3D geometric deformations [6], [7]. While the former captures visual texture, the latter, often represented by point clouds [8], [9], [7], [10], preserves explicit geometric relationships between objects and surroundings. Maintaining accurate 3D structure is essential for downstream tasks requiring precise spatial reasoning, making it ideal for describing scene evolution. 

Despite progress in scene generation, a crucial limitation of existing methods is their limited capacity to understand 3D scenes. While capable of predicting plausible future states, 

X. Zhou, D. Liang, D. Zhang and X. Bai are with Huazhong University of Science and Technology. E-mail: (xzhou03, dkliang, xbai)@hust.edu.cn X. Chen, and F. Tan are with Afari Intelligent Drive. 

H. Zhao is with the University of Hong Kong. � Corresponding author. 

they often fail to articulate the semantic context or the causal factors driving the predicted evolution. As shown in Fig. 1(a), while driving world models excel at forecasting environmental changes, they lack the intrinsic mechanisms to answer direct queries (e.g., visual question answering, scene description). This disconnect between prediction and interpretation creates a significant capability gap, as the contextual awareness that is essential for real-world driving remains largely unaddressed by generation-centric architectures. 

Moreover, recent advances in Vision-Language Models (VLMs) [11], [12], [13] have demonstrated remarkable capabilities in general vision tasks by leveraging world knowledge and causal reasoning from large-scale pretraining. When adapted to autonomous driving scenarios [14], [15], [16], these models excel at interpreting complex driving environments, answering queries about traffic participants, generating comprehensive scene descriptions, and reasoning about spatial relationships between entities, as shown in Fig. 1(b). For instance, OmniDrive [14] combines 3D representations with language models for visual question answering, while DriveLM [15] employs graph-based reasoning for scene understanding and planning. However, these language-centric approaches prioritize understanding the current state, lacking the predictive capacity to anticipate how the scene geometry will evolve. This deficiency is critical in safety-critical scenarios where collision avoidance requires anticipating both the present context and future changes. 

Motivated by the complementary strengths and limitations of these two paradigms, we propose that a world model should seamlessly integrate 3D scene understanding with accurate future geometry prediction. Constructing such a cohesive framework requires the careful consideration of two critical aspects. First, a suitable 3D representation is essential for effectively handling both textual understanding and multi-view spatial relationships. This representation must consolidate observations into a structure that preserves geometric interactions while remaining compatible with token-based language models. Second, an interaction mechanism is needed to bridge the gap between understanding and future generation. This ensures that semantic understanding guides geometric evolution and that geometric predictions ground language generation, going beyond multi-task feature sharing. Additionally, ensuring consistency in predicted scene evolutions is challenging, as supervision based solely on future observations often provides only explicit constraints, leading to structural inconsistencies. 

Based on these observations and analyses, in this paper, we propose a unified driving world model that integrates 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

2 


Fig. 1: (a) Previous driving world models focus on generative scene evolution prediction. (b) Large language models for driving are limited to scene understanding. (c) The proposed framework unifies 3D scene understanding and scene evolution generation with the BEV representation. (d) Quantitative comparison with dedicated specialist methods. 

understanding and generation tasks, termed HERMES++, as shown in Fig. 1(c). HERMES++ is built upon a Bird’s-Eye View (BEV) representation that naturally consolidates multiview spatial information while ensuring compatibility with LLMs. For the linking mechanism, we introduce world queries enhanced by the LLM to transfer world knowledge from text understanding to future scene generation. These queries interact with LLM-processed BEV features via a Currentto-Future Link, ensuring that predicted scene evolution is conditioned on both geometric context and semantic reasoning. 

Specifically, the BEV representation mitigates the effects of token length constraints when processing high-resolution multi-view inputs. Instead of directly converting multiple views into tokens, a BEV tokenizer consolidates them in two stages. First, a vision encoder transforms multi-view images into the BEV space using cross-attention, compressing high-dimensional inputs while preserving spatial information. Second, the BEV features are downsampled and flattened into LLM-compatible tokens. This approach reduces redundancy while maintaining geometric relationships in a consistent coordinate system. To strictly enforce geometric consistency in predicted scene evolutions, we further propose a Joint Geometric Optimization strategy. This mechanism integrates explicit geometric constraints on point clouds with implicit geometric regularization on the latent manifold. By aligning representations to geometry-aware priors, our approach ensures structural integrity throughout the generation process. 

Furthermore, we introduce a knowledge transfer mechanism that bridges scene understanding with future evolution prediction. To achieve this, we directly initialize world queries from BEV features before LLM processing. These queries leverage causal attention to aggregate rich world knowledge and semantic context from text tokens. The queries then interact with LLM-encoded BEV features to generate latent representations for future timestamps via a module termed Current-to-Future Link. We further equip this link with two refinements. A Textual Injection integrates text embeddings as conditioning signals, so that semantic information directly modulates the 

generation process. An Ego Modulation adaptively adjusts spatial feature distributions according to future ego-motion, which decouples motion from inherent scene dynamics and ensures controllability across prediction horizons. 

By conducting 3D scene understanding and future scene generation within a single framework, HERMES++ establishes a shared representation that seamlessly accommodates both tasks, offering a holistic perspective on driving environments. This marks a significant step toward a unified driving world model, demonstrating the feasibility of integrated driving understanding and generation. Extensive experiments validate the effectiveness of HERMES++ in both tasks. Notably, our method significantly reduces error by 8.2% compared to the leading method DriveX [17] for challenging 3s point cloud generation. Additionally, for the understanding task, it outperforms the prior specialist baseline Omni-Q [14] by 9.2% on the OmniDrive-nuScenes dataset [14] under the CIDEr metric. 

Overall, this paper presents an early and solid exploration of a unified driving world model. By analyzing the distinct requirements of 3D scene understanding and future geometry evolution prediction, we design key components, including unified representation, world queries, and a Joint Geometric Optimization strategy. We hope this work will establish a foundation for the emerging field of interpretable and predictive autonomous driving systems. Our main contributions are summarized as follows: 

- We propose a unified framework that effectively integrates 3D scene understanding and future geometry prediction. By leveraging a unified representation, our method consolidates multi-view spatial information while maintaining compatibility with LLM processing. 

- We devise a Joint Geometric Optimization strategy to enforce structural integrity in future predictions. This mechanism combines explicit geometric constraints from ground-truth point clouds with implicit geometric regularization on the latent manifold, ensuring that the predicted features align with intrinsic 3D geometry. 

- We introduce LLM-enhanced world queries that facilitate 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

3 

knowledge transfer, allowing semantic reasoning derived from scene understanding to directly guide the generation of future scene evolution. 

- We conduct extensive experiments, demonstrating that HERMES++ achieves strong performance across both generation and understanding, outperforming prior unified baselines and several specialist approaches. These results validate the effectiveness of the unified architecture, offering a new perspective for constructing holistic driving world models. 

This paper is an extended version of our conference paper, published in ICCV 2025 [18], where we make the following new contributions: **1)** We introduce a Joint Geometric Optimization strategy as an implicit geometric regularization on the latent space. The conference version relies solely on explicit point cloud constraints, whereas this strategy constructs geometry-aware representations that facilitate more accurate point cloud decoding and thereby enhance future generation performance. **2)** We further equip the Current-to-Future Link with two refinements. A Textual Injection integrates text embeddings as explicit conditioning signals, so that semantic reasoning from the language model guides the prediction of future scene evolution. An Ego Modulation adaptively adjusts spatial feature distributions, which decouples ego-motion from inherent scene dynamics and improves controllability. **3)** Through these advancements, our model achieves significant performance gains over the conference baseline. Specifically, we observe a 13.7% reduction in generation error and consistent improvements in scene understanding metrics compared with the conference version. **4)** We have made improvements to the quality of the manuscript in various aspects. We extend the evaluations on three additional benchmarks to validate the generalization capabilities. Furthermore, we provide expanded ablation studies and in-depth discussions on the scalability of unified architectures and the intrinsic synergy between understanding and geometric evolution. These analyses not only substantiate our technical contributions but also offer insights into the potential of foundational World Models for interpretable autonomous driving. 

controllability [3], [30], [31]. More recent approaches explore scalable DiT-based architectures [32], [33], [34], autoregressive transformers [35], [36], [37], and multimodal conditioning strategies [38], [31] to improve temporal coherence. On the other hand, other studies focus on generating 3D spatial information to provide geometric representations for autonomous systems. OccWorld [6] targets future occupancy generation and planning using spatial-temporal transformers, which have been adapted to other paradigms, including diffusion [39], [40], rendering [41], [42], [43], and autoregressive transformers [44]. Some approaches propose future point cloud [45], [46], [47], [48] or depth forecasting [49], [50], [51] as world models. Among these, ViDAR [7] uses images to predict future point clouds in a self-supervised manner, while recent methods [32] explore geometry-aware architectures and multiscale temporal modeling to enhance prediction accuracy. 

However, existing driving world models often fail to incorporate an understanding of the driving environment. While capable of predicting future states, they lack the intrinsic ability to interpret or reason about the scenes they generate. Recent research has shifted towards unified models that combine generation and understanding within a single framework [22], [52], [44], [37], [53], yet the exploration of such unified capabilities remains nascent. For example, Doe-1 [22] explores closed-loop autonomous driving with a world model primarily focusing on single-view generation. Epona [37] employs an autoregressive diffusion framework to decouple temporal dynamics from visual generation for consistent long-horizon prediction and planning. FSDrive [54] introduces a visual spatio-temporal Chain-of-Thought to bridge perception and planning by generating future frames with physical constraints. Despite these advances, these methods mostly operate in 2D single-view images or lack dense 3D geometric constraints intertwined with semantic reasoning. 

In this paper, we propose a unified world model that understands driving scenarios and generates future geometric scene evolution, establishing a holistic framework for interpretable and predictive autonomous driving. 

## _B. Large Language Models for Driving_ 

## II. RELATED WORK 

## _A. World Models for Driving_ 

Driving world models [19] have garnered considerable attention in autonomous driving due to their ability to learn comprehensive environmental representations and predict future evolution based on action sequences. By simulating the dynamics of the driving environment, these models provide essential support for downstream tasks such as risk assessment and motion planning. Current research primarily focuses on generation tasks operating in either 2D [20], [21], [22] or 3D [23], [24] spaces. 

Most pioneering 2D world models perform video generation for driving scenarios. GAIA-1 [5] introduced a learned simulator based on an autoregressive model. Subsequent works further leverage large-scale data [25], [26], [27] and advanced pre-training techniques to enhance generation quality regarding consistency [28], [29], resolution [2], [26], and 

Large Language Models (LLMs) and Vision-Language Models (VLMs) have achieved significant success by leveraging extensive world knowledge and causal reasoning capabilities derived from large-scale pretraining [55], [56], [57], [58], [59]. In the realm of autonomous driving, these models effectively bridge the gap between raw sensory data and semantic understanding, enabling the interpretation of complex traffic scenarios, reasoning about agent behaviors, and generating natural language explanations. Such capabilities are crucial for developing reliable autonomous systems capable of handling diverse driving situations. 

Recent research has adapted LLMs and VLMs to various driving tasks. For scene understanding, DriveGPT4 [16] employs a VLM to generate driving commands alongside natural language justifications based on front-view observations. DriveLM [15] introduces scene graphs to facilitate structured reasoning and end-to-end driving via graph-based visual question 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

4 

answering. Similarly, OmniDrive [14] integrates 3D spatial representations with VLMs using a Q-Former, establishing a comprehensive benchmark for multi-task driving comprehension. To enhance spatial-temporal modeling, ELM [60] proposes pre-training strategies tailored specifically for embodied scenarios. Beyond perception and reasoning, VisionLanguage-Action (VLA) models have emerged to directly link perception with control [61], [62], [63], [64]. For example, ORION [65] performs a differentiable connection between reasoning and action space. Despite these advances, existing methods primarily rely on the LLM to understand the current state, often lacking the capacity to predict the future geometric evolution of the surrounding environment. 

In this paper, we bridge this gap by enabling LLMs to comprehend the present driving scenario and predict its future evolution. Rather than treating these as isolated tasks, we establish dedicated mechanisms that allow semantic reasoning from language understanding to guide geometric prediction. This design empowers the model to leverage world knowledge for generating structurally coherent future scenes, creating a framework that seamlessly integrates scene comprehension with accurate prediction. 

## III. PRELIMINARIES 

This section briefly reviews driving world models and the Bird’s-Eye View representation as preliminaries. 

**Driving world models** aim to learn a general representation of the driving environment by forecasting the future dynamics of a scene [19], [20], [18], [6], [7]. The core objective is to predict future states based on current observations and planned actions, enabling the model to capture the underlying data distribution of real-world driving scenarios. 

Formally, given an observation _Ot_ at time _t_ and an action _At_ , a driving world model predicts the subsequent observation _Ot_ +1. This process typically involves three components: 


where _E_ : _O →Z_ is an encoder that maps observations to latent representations, _M_ : _Z×A →Z_ is the predicting model that transitions the latent state forward in time conditioned on an action, and _D_ : _Z →O_ is a decoder that reconstructs the observation from the predicted latent state. The latent space _Z_ serves as a compact representation that captures essential scene information while filtering out irrelevant details. While _Ot_ can vary across modalities (e.g., RGB images, LiDAR), this work focuses on multi-view images as input and point clouds as output, leveraging the latter’s ability to preserve 3D geometric structures, which are essential for spatial reasoning. Two further considerations support this choice of output modality. First, point clouds are directly measured by the LiDAR sensor and require no additional annotation, so the geometric supervision scales easily to larger amounts of data, whereas 3D occupancy must be constructed by aggregating sequential scans and, in its semantic form, additionally requires pervoxel categories. Second, point clouds can be decoded from the predicted representation by a lightweight differentiable renderer, whereas generating plausible future images relies on 

the strong priors of large pre-trained generative models, which would obscure the contribution of the unified representation studied in this work. We further note that this choice is not a restriction of the architecture, since the world queries and the Current-to-Future Link (Sec. IV-B) operate on latent features and are agnostic to the output modality. 

**Bird’s-Eye View (BEV)** has emerged as a foundational spatial representation for autonomous driving, offering a natural coordinate system for multi-view fusion and spatial reasoning [27], [66], [67], [68]. Unlike perspective views, which are prone to occlusion and scale ambiguity, BEV preserves geometric relationships in a top-down logical space. 

Given multi-view images _{Ii}_<sup>_N_</sup> _i_ =1<sup>from</sup><sup>_N_multi-viewcam-</sup> eras, the BEV representation is defined as a feature map **F** BEV _∈_ R<sup>_H×W ×C_</sup> , where _H×W_ represents the spatial resolution and _C_ denotes the feature dimension. The transformation from perspective view to 3D BEV space requires lifting image features to 3D spatial locations. Following modern approaches like the BEVFormer series [69], [70], we employ learnable grid queries **Q** BEV _∈_ R<sup>_H×W ×C_</sup> positioned at predefined grid locations in BEV space. For each query at spatial location ( _x, y_ ), the corresponding BEV feature is computed through spatial cross-attention: 


where DA( _·_ ) denotes multi-scale deformable cross-attention that aggregates features from the _i_ -th camera feature map **F** _i_ around the projected reference point _πi_ ( _x, y, z_ ) with learned sampling offsets and attention weights. _H_ is a set of predefined height anchors, and _πi_ ( _·_ ) maps a 3D location to the image plane using camera intrinsics and extrinsics. 

By encoding geometry, the BEV representation effectively unifies visual semantics with spatial structure. Its natural integration of visual semantics and geometric structure makes BEV well-suited for both scene understanding and generation. We thus leverage it as the core substrate to bridge scene understanding and future evolution prediction within a shared geometric space. 

## IV. METHOD 

Fig. 2 illustrates the overall framework of HERMES++, which seamlessly integrates language-based reasoning with geometric generation. The pipeline begins by transforming multi-view images into the BEV representation, which is subsequently compressed into visual tokens compatible with the large language model. These tokens, concatenated with user instructions and learnable world queries, are processed by the LLM to generate textual responses while aggregating semantic context into the queries. Following this, the Currentto-Future Link propagates the encoded BEV features to future timestamps, conditioned on the enriched queries, text embeddings, and ego-motion. Finally, a shared Render reconstructs point clouds from the predicted features. To strictly enforce structural integrity, we employ a Joint Geometric Optimization strategy that integrates explicit geometric constraints on reconstructed point clouds with implicit geometric 

5 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 


Fig. 2: Pipeline of HERMES++. Flattened BEV tokens, instructions, and world queries are input to the LLM to generate text and semantic contexts. The Current-to-Future Link propagates the encoded BEV to future states, conditioned on both textual semantics and world queries. The shared Render then predicts the evolution of the point cloud. During training, a Joint Geometric Optimization strategy ensures structural integrity by combining explicit geometric constraints on rendered outputs with implicit geometric regularization on latent features using a frozen geometry extractor. 

regularization on the latent manifold. Through this unified pipeline, HERMES++ effectively bridges the gap between perception and prediction, leveraging world knowledge to directly guide future scene evolution. Compared with the conference version [18], the visual tokenizer and Render in Sec. IV-A and the world queries in Sec. IV-B are inherited. The Joint Geometric Optimization strategy in Sec. IV-C is newly introduced, together with the Textual Injection and Ego Modulation that refine the Current-to-Future Link in Sec. IV-B3, and the training objectives in Sec. IV-D are extended accordingly. 

## _A. Visual Tokenizer and BEV-to-Point Render_ 

To address the spatial discontinuity inherent in multi-view inputs and the token constraints of LLMs, we adopt the BEV representation, which naturally preserves geometric structural integrity while enabling efficient compression for language interaction. Specifically, a visual tokenizer is used for feature encoding and a differentiable Render for geometric decoding. 

For feature encoding, we employ a BEV-based visual tokenizer to preserve geometric spatial relationships across views while providing semantically rich inputs for the LLM. Given multi-view images _{It_<sup>_i}N_</sup> _i_ =1<sup>attime</sup><sup>_t_from</sup><sup>_N_cameras,the</sup> tokenizer operates in two stages. First, we encode the multiview images using a vision encoder [71], [72] to extract multi- 

scale perspective features. These features are then transformed into a BEV representation **F**<sup>bev</sup> _t ∈_ R<sup>_w×h×c_</sup> via spatial crossattention [70]. This process effectively captures both semantic and geometric information in the BEV space, where _w_ and _h_ denote the spatial dimensions of the BEV grid, and _c_ represents the feature channels. Because the raw BEV features contain a large number of tokens that exceed the length limits of most LLMs [73], we apply a downsampling module composed of strided convolutions and pooling. This reduces the spatial resolution by a factor of 4 while expanding the channel dimension to preserve information, yielding **F**<sup>down</sup> _t ∈_ R _<u>w</u>_ 4<sup>_×_</sup><sup>_<u>h</u>_</sup> 4<sup>_×_4</sup><sup>_c_</sup> . Finally, we flatten and project the compressed feature through a linear layer for LLM processing, following established practices in vision-language models [11], [74]: 


where _L_ BEV = _<u>w</u>_ 4<sup>_×_</sup><sup>_<u>h</u>_</sup> 4<sup>isthenumberofBEVtokens,</sup><sup>_C_is</sup> the hidden dimension of the LLM, and Flatten( _·_ ) reshapes the spatial dimensions into token sequences. This tokenization balances spatial detail preservation with computational efficiency. To complement this encoding process and recover 3D geometry from BEV spaces, we introduce a differentiable BEV-to-Point Render _R_ . This module operates on either the compressed BEV feature **F**<sup>down</sup> _t_ or the LLM-processed BEV 

6 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

feature **B** _t_ (after out-projection from the LLM dimension). To generate 3D geometry from 2D BEV features, we first upsample the input to its original spatial resolution using nearest neighbor interpolation and convolutional layers. As BEV features lack height information, we expand them into a volumetric representation by reshaping along the height dimension. A series of 3D convolutional layers then refines this representation to produce **V**<sup>ˆ</sup> _t ∈_ R<sup>_w×h×z×c′_</sup> , where _z_ denotes the number of discrete height levels, and _c_<sup>_′_</sup> is the output dimension encoding the 3D scene structure. 

Following established neural rendering techniques [75], [76], [77], we model the scene geometry as an implicit signed distance function (SDF) field. For each LiDAR ray **r** _k_ emitted from the center **o** along direction **t** _k_ , we discretize it into _n_ sample points **p** _i_ = **o** + _di_ **t** _k_ with increasing depths 0 _≤ d_ 1 _< d_ 2 _< · · · < dn_ . For each point, we retrieve the local feature **f** _i_ from **V**<sup>ˆ</sup> _t_ via trilinear interpolation and predict the SDF value _si_ using a shallow MLP _ϕ_ SDF, i.e., _si_ = _ϕ_ SDF( **p** _i,_ **f** _i_ ). With the predicted SDF values, the rendered depth for ray **r** _k_ is computed as a weighted sum: 


where _wi_ represents the weight derived from transmittance _Ti_ =<sup>�</sup><sup>_i_</sup> _j_<sup>_−_</sup> =1<sup>1(1</sup><sup>_−αj_)andopacity</sup><sup>_αi_.Theopacityiscomputed</sup> from the SDF gradients as: 


where _στ_ ( _x_ ) = (1 + _e_<sup>_−τx_</sup> )<sup>_−_1</sup> is the sigmoid with a learnable parameter _τ_ . The final point cloud _Pt_ = _{_ **p** _k}_<sup>_K_</sup> _k_ =1<sup>isobtained</sup> by converting the rendered depths back to 3D coordinates. 

## _B. Unification of Understanding and Generation_ 

This subsection details the unification mechanism that seamlessly integrates scene understanding and future evolution prediction within HERMES++. The central challenge lies in establishing knowledge transfer from language-based reasoning to geometric prediction, thereby enabling the world knowledge acquired during understanding to guide future generation. We address this through two key designs: world queries that aggregate semantic information, and a Current-to-Future Link that leverages both geometric and textual conditioning for temporal evolution modeling. 

_1)_ **_Language-based Scene Understanding_** _:_ The LLM serves as the central reasoning engine, processing multiview observations encoded as BEV features **F** _t_ (Eq. 3) and responding to user instructions about the driving scenario. User instructions are tokenized into text tokens **T** _∈_ R<sup>_L_text</sup><sup>_×C_</sup> using the LLM’s vocabulary, where _L_ text is the text length. These sequences are concatenated and processed by the LLM, enabling the model to interpret the driving scene through next-token prediction. This process not only serves the immediate queryanswering task but also enriches the internal representations with semantic knowledge essential for future prediction. 

_2)_ **_World Queries for Knowledge Transfer_** _:_ To enable knowledge transfer from understanding to generation, we introduce world queries that interact directly with the LLM’s processing pipeline and act as temporal semantic carriers. Unlike conventional approaches that employ separate branches for task-specific processing, our world queries are injected into the input sequence, acting as latent placeholders that aggregate semantic information from both visual and textual contexts. 

Specifically, we initialize ∆ _t_ groups of world queries, with each group containing _n_ tokens corresponding to a distinct future time step. This initialization leverages adaptive max pooling over the compressed BEV features **F**<sup>down</sup> _t_ to extract salient spatial information, yielding the base spatial queries **Q** _∈_ R<sup>_n×_4</sup><sup>_c_</sup> , where 4 _c_ represents the channel dimension. To enable controllable future generation conditioned on egovehicle trajectories, we process the ego-motion parameters for each future frame using an MLP to generate high-dimensional motion embeddings **e** _t_ + _i ∈_ R<sup>1</sup><sup>_×_4</sup><sup>_c_</sup> . These embeddings are then broadcasted and added to the base spatial queries. Furthermore, learnable frame embeddings **FE** _∈_ R<sup>∆</sup><sup>_t×_4</sup><sup>_c_</sup> are introduced to encode the temporal order. The final world queries **Q**<sup>_w_</sup> _∈_ R<sup>(∆</sup><sup>_t×n_)</sup><sup>_×C_</sup> are constructed by concatenating these temporally conditioned representations and projecting them to the hidden dimension of the language model using a shared linear layer _ϕ_ : 


where _⊕_ denotes element-wise addition with broadcasting across the spatial query and temporal dimensions accordingly. 

We argue that our world queries facilitate knowledge transfer in two ways. First, the causal attention mechanism allows world queries to access all preceding tokens, effectively aggregating specific semantic context from current BEV observations and textual instructions. Second, the language model contains rich intrinsic world knowledge during large-scale pre-training. By processing queries, the model infuses them with world knowledge and causal priors. Thus, the resulting enriched queries **Q**<sup>_w_</sup> _ϵ_<sup>encapsulatebothcontext-specificdetails</sup> and generalized world knowledge, serving as priors for the subsequent geometric forecasting task. 

_3)_ **_Current-to-Future Link_** _:_ While the world queries capture semantic information from the understanding process, they provide only a sparse representation of future scenes with _n_ queries per time point. To generate dense future BEV features, we introduce a Current-to-Future Link that propagates spatial information from the current encoded BEV **B** _t_ to future time points, conditioned on both world queries and text embeddings. We further refine this link with two designs, a Textual Injection and an Ego Modulation, which condition the propagation on semantic context and on the planned ego-motion, respectively. 

The Textual Injection incorporates semantic context into the generation process. Specifically, we extract text embeddings **T** ˆ _∈_ R<sup>_k×C_</sup> from the LLM-processed text tokens via average pooling and linear projection, where _k_ is the number of pooled tokens and _C_ is the LLM dimension. For each future time step _i ∈{_ 1 _, . . . ,_ ∆ _t}_ , let **Q**<sup>_w_</sup> _ϵ,i_<sup>denotethecorrespondingworld</sup> 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

7 

queries. The link consists of several stacked blocks, each containing cross-attention, self-attention, and feed-forward layers. The cross-attention layer aggregates information from both world queries and text: 


where **X**<sup>(</sup><sup>_l_)</sup> represents the input features (initialized as **B** _t_ ), and the concatenation [ **Q**<sup>_w_</sup> _ϵ,i_<sup>;</sup><sup>**T**ˆ]servesastheKeyandValue.This</sup> formulation enables the model to jointly attend to geometric context from world queries and semantic guidance from text, explicitly directing the spatial evolution. 

To ensure the predicted scene aligns with planned trajectories, we further apply an Ego Modulation (EM) that adapts feature distributions based on future ego-motion. Specifically, the ego-motion for time point _t_ + _i_ is encoded through an MLP with a Tanh activation to produce modulation parameters _γ_ and _β_ for self-attention and feed-forward layers: 


where _⊙_ denotes element-wise multiplication, and the modulation vectors are zero-initialized at the initial period of training to maintain stability. This modulation adaptively adjusts spatial representations based on driving maneuvers. Notably, EM is applied only to self-attention and feed-forward branches, preserving the cross-attention’s focus on semantic aggregation. 

Finally, the processed features are reshaped and upsampled to future BEV representations _{_ **B** _t_ + _i}_<sup>∆</sup> _i_ =1<sup>_t_,whicharesubse-</sup> quently used by the shared Render to generate corresponding future point cloud evolutions _{Pt_ + _i}_<sup>∆</sup> _i_ =1<sup>_t_.</sup> 

The Current-to-Future Link thus serves as a bridge between understanding and generation, enabling world knowledge from language reasoning to inform geometric prediction while maintaining controllability through ego-motion conditioning. This architecture enables the model to generate future scenes that are both semantically consistent with the current context and geometrically aligned with the vehicle’s behavior. 

## _C. Joint Geometric Optimization Strategy_ 

We observe that relying solely on rendering-based supervision often results in structural ambiguity in the latent representation, as it fails to capture intricate geometric structures and foreground objects. To address this, we propose a Joint Geometric Optimization strategy that imposes constraints on both the observational and latent levels. This mechanism integrates explicit geometric constraints derived from ground-truth point clouds with implicit regularization to internal representations. 

**Explicit Geometric Constraints.** At the observational level, we supervise the generated point clouds to ensure geometric integrity. We employ a simple _L_ 1 loss on the rendered depths to minimize the discrepancy between the predicted and ground-truth geometry. The rendering loss is formulated as: 


where _d_ ( **r** _k_ ) and _d_<sup>˜</sup> ( **r** _k_ ) denote the ground-truth and predicted depths for ray **r** _k_ , _λi_ is the loss weight for frame _t_ + _i_ , and _Ni_ 

is the number of rays. This explicit constraint ensures that the decoded point clouds align with the physical measurements. 

**Implicit Geometric Regularization.** Complementary to explicit constraints, we introduce an implicit regularization for the latent manifold. This strategy aligns the predicted features with geometry-aware representations, thereby guiding the model to encode intrinsic 3D structures. Specifically, this process leverages a geometric feature extractor to derive latent priors, which are then enforced on the predicted features via two complementary alignment objectives. 

To obtain the geometry-aware priors, we utilize a selfsupervised point cloud reconstruction network as the geometric feature extractor. This network comprises a sparse 3D convolutional encoder paired with the differentiable Render _R_ . During a pre-training stage, we voxelize the groundtruth point cloud _Pt_ , extract features using the extractor, and subsequently render them to reconstruct the input point cloud. This self-supervision enables the capture of spatially meaningful representations. In the main training phase, the Geometric Feature Extractor functions as a frozen encoder to produce the target geometry-aware features **V** _t ∈_ R<sup>_w×h×z×c′_</sup> . 

We align the predicted volumetric features **V**<sup>ˆ</sup> _t_ with the frozen geometry-aware features **V** _t_ using two objectives that capture both local correspondence and global structural patterns. First, to enforce element-wise consistency, we employ a cosine similarity loss: 


where ( _i, j, k_ ) indexes the voxel grid. Second, we introduce a Gram loss to measure feature correlations for global consistency. We pool the features along orthogonal spatial axes to obtain projected maps **V** _t_<sup>_HW_</sup> , **V** _t_<sup>_HZ_</sup> , and **V** _t_<sup>_W Z_</sup> . For a perspective _d ∈{HW, HZ, WZ}_ , the spatial Gram matrix is formulated as: 


where _Nd_ is the spatial tokens length in perspective _d_ . This matrix captures pairwise correlations across spatial locations. The Gram loss minimizes the discrepancy between the Gram matrices of the predicted and geometry-aware features: 


where **G**<sup>ˆ</sup><sup>_d_</sup> _t_<sup>and</sup><sup>**G**</sup><sup>_d_</sup> _t_<sup>are computed from</sup><sup>**V**ˆ</sup><sup>_t_and</sup><sup>**V**</sup><sup>_t_, respectively.</sup> _∥· ∥F_ denotes the Frobenius norm. 

Since the geometry extractor is used only for training-time regularization and is discarded at inference, it introduces no additional inference-time cost. 

## _D. Training Objectives_ 

The training of HERMES++ is governed by a composite objective function that jointly optimizes language understanding, geometric rendering, and structural alignment. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

8 

To enable scene understanding, we employ next-token prediction following the standard autoregressive language modeling objective: 


where _P_ ( _·|·_ ) represents the conditional probability modeled by the LLM parameters **Θ** , **F** _t_ is the flattened BEV feature, and **T** _i_ denotes the _i_ -th text token. To supervise future point cloud generation, we utilize the proposed Joint Geometric Optimization strategy. This objective integrates the explicit geometric constraints (Eq. 9) with the implicit geometric regularization (Eq. 10 and Eq. 12): 


Finally, the overall objective is the summation of the understanding and generation losses: 


## V. EXPERIMENTAL SETUP 

## _A. Datasets and Evaluation Metric_ 

We conduct comprehensive experiments on four datasets, and additionally use NuInteract for vision-language alignment. **NuScenes Dataset** [78] serves as the primary benchmark for geometric representation learning and unified training. In our experiments, we utilize the multi-view images as inputs and synchronized point clouds as ground truth. Following prior work [7], [18], we evaluate the consistency of predicted future scenes using the bidirectional Chamfer Distance (CD). The evaluation is restricted to a Region of Interest (ROI) defined by _x, y ∈_ [ _−_ 51 _._ 2m _,_ 51 _._ 2m] and _z ∈_ [ _−_ 3m _,_ 5m]. 

**OmniDrive-nuScenes Dataset** [14] is utilized for the refinement phase and unified instruction tuning. It enriches the original NuScenes dataset with high-quality scene descriptions and visual question-answering (QA) pairs, requiring the model to reason about complex object interactions and traffic contexts. To assess scene understanding capabilities, we evaluate the quality of textual responses on the validation set. We report CIDEr [79] for consensus, METEOR [80] for semantic alignment, and ROUGE-L [81] for structural similarity, following the official evaluation. 

**NuScenes-QA Dataset** [82] is a large-scale visual question answering benchmark, comprising _∼_ 460k QA pairs. It leverages 3D detection annotations to construct scene graphs, evaluating the model’s ability to interpret complex driving environments and reason about spatial relationships. We report the standard top-1 accuracy to quantify performance on this multi-view visual question-answering task. 

**DriveLM Dataset** [15] introduces Graph Visual Question Answering to mimic human-like reasoning in driving. Constructed on selected NuScenes keyframes, it interconnects perception, prediction, and planning questions via logical dependencies. The rich logical chain annotations assess the depth of the reasoning and its capability to align scene understanding with action planning. We report the hybrid metrics calculated by the official test server. 

TABLE I: Training details of HERMES++. The ‘/’ in Stage 1 and Stage 2 indicates the settings for the two sub-phases. 

|Config|Stage 1|Stage 2|Stage 3|
|---|---|---|---|
|Optimizer|AdamW|AdamW|AdamW|
|Learning Rate|2e-4|2e-4/4e-4|4e-4|
|Training Epochs|12/6|3/6|36|
|Learning Rate Scheduler|Cosine|Cosine|Cosine|
|Total Batch Size|32|128|128|


**NuInteract Dataset** [83] is a large-scale language-based driving dataset containing _∼_ 1.5M diverse annotations, including dense captions for individual images and scenes. We utilize NuInteract to establish an initial alignment between BEV visual features and the LLM’s semantic space, effectively mitigating data scarcity in vision-language pre-training. 

## _B. Implementation Details_ 

The BEV-based tokenizer utilizes an OpenCLIP ConvNeXtL backbone [72], [71] for visual feature extraction. Both the visual tokenizer and the Render are initialized from scratch. For the language component, we adopt the pre-trained weights of InternVL2 [12], [74]. The visual tokenizer [70] encodes the scene into a 180 _×_ 180 BEV grid with a channel dimension of 256. In the BEV-to-Point Render, the height dimension _z_ and output channel _c_<sup>_′_</sup> are both set to 32. The model forecasts scene evolution over a horizon of ∆ _t_ = 3 seconds. Regarding the training objective, we empirically set the framewise generation weights to _λi_ = 1+0 _._ 5 _× i_ for _i ∈{_ 0 _, · · · ,_ 3 _}_ to emphasize long-term prediction accuracy. 

The training process proceeds in three progressive stages, as summarized in Tab. I. First, to establish reliable geometric representations, we conduct a geometry-aware pre-training where the sparse 3D encoder [84] is trained via self-supervised point cloud reconstruction and subsequently frozen as a static prior. We then pre-train the tokenizer and Render to lift 2D observations into 3D space by reconstructing current point clouds from multi-view images, supervised by _L_ render and _L_ cos. Subsequently, we bridge the visual and linguistic modalities through alignment and refinement phases while maintaining implicit regularization. We initially train only the LLM projectors using a masking-based augmentation strategy (stitching captions with unmasked views) to mitigate data scarcity, which expands the image-text pairs by 7 _×_ to _∼_ 200K. This is followed by a refinement phase where all parameters are unfrozen (applying LoRA [85] to the LLM) using dense captions from NuInteract [83] and scene descriptions from OmniDrive-nuScenes [14]. Finally, we integrate the Currentto-Future Link to conduct scene understanding and predict future evolution. The model is jointly trained on nuScenes keyframes, descriptions, and conversation annotations, guided by Joint Geometric Optimization using both _L_ gram and _L_ cos. 

## VI. RESULTS AND ANALYSIS 

In this section, we conduct comprehensive experiments to validate the effectiveness of HERMES++. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

9 

TABLE II: The comparison of HERMES++ and understanding/generation specialist models. L/C/T refers to LiDAR/camera/text, respectively. ‘Aux. Sup.’ denotes auxiliary supervision (e.g., 3D object detection, lane detection). We report METEOR, ROUGE, and CIDEr for understanding tasks, and Chamfer Distance for 0–3s on the OmniDrive-nuScenes [14] validation set. 

|Method|Reference|# LLM Params|Modality|Aux. Sup.||Gene|ration|||Understanding||
|---|---|---|---|---|---|---|---|---|---|---|---|
||||||0s _↓_|1s _↓_|2s _↓_|3s _↓_|METEOR _↑_|ROUGE _↑_|CIDEr _↑_|
||||_Onl_|_y Generation_||||||||
|SPFNet [86]|CoRL 21|-|L_→_L|-|-|2.24|-|2.50||||
|S2Net [46]|ECCV 22|-|L_→_L|-|-|1.70|-|2.06||||
|4D-Occ [47]|CVPR 23|-|L_→_L|-|-|1.13|1.53|2.11||Unsupported||
|ViDAR [7]|CVPR 24|-|C_→_L|-|-|1.12|1.38|1.73||||
|DriveX [17]|ICCV 25|-|C_→_L|-|-|**0.66**|0.86|1.10||||
||||_Only _|_Understanding_||||||||
|LLaVA-OV [87]|TMLR 25|7B|C_→_T|-|||||-|0.221|0.284|
|Omni-L [14]|CVPR 25|7B|C_→_T|3D Box, Lane|||||0.376|0.321|0.732|
|Omni-Q [14]|CVPR 25|7B|C_→_T|3D Box, Lane|||d||0.380|0.326|0.686|
|OmniDrive-2D [14]|CVPR 25|7B|C_→_T|3D Box, Lane||Unsup|porte||0.383|0.325|0.671|
|OmniDrive-BEV [14]|CVPR 25|7B|C_→_T|3D Box, Lane|||||0.356|0.278|0.595|
|ORION [65]|ICCV 25|7B|C_→_T|3D Box, Lane|||||0.354|0.306|0.635|
|||_Ui_|_nified Unders_|_tanding and Gene_|_ration_|||||||
|HERMES [18] (conference version)|ICCV 25|1.8B|C_→_T&L|-|0.59|0.78|0.95|1.17|0.384|0.327|0.741|
|HERMES++ (**ours**)|-|1.8B|C_→_T&L|-|0.53|0.71|0.86|1.01|0.385|0.327|0.749|
|HERMES++ (**ours**)|-|3.8B|C_→_T&L|-|**0.51**|0.68|**0.82**|**0.97**|**0.389**|**0.331**|**0.772**|


## _A. Unification of Understanding and Generation_ 

In this subsection, we present a comprehensive evaluation of HERMES++ on the NuScenes and OmniDrive-nuScenes benchmarks. We compare our framework against three categories of baselines: 1) Generation specialists; 2) Understanding specialists; and 3) Our conference version. Tab. II details the quantitative comparisons, from which we draw the following observations: 

**1) HERMES++ significantly advances 3s future scene generation compared to dedicated specialists.** The quantitative results in Tab. II demonstrate that our method achieves superior geometric prediction accuracy. Compared to leading generation methods such as 4D-Occ [47] and ViDAR [7], HERMES++ achieves better performance with only currentframe observations. Specifically, we reduce the CD at the 3s horizon by 41.6% compared to ViDAR. Even against the recently proposed DriveX [17], our method maintains an advantage, achieving a reduction of 0.09 in CD at the 3s horizon. By employing multiple groups of world queries to inject conditional context for future BEV states, our model effectively leverages semantic information to achieve more precise scene evolution prediction. 

**2) HERMES++ achieves highly competitive understanding capabilities without auxiliary supervision.** In the domain of 3D scene understanding, HERMES++ consistently outperforms specialist models while maintaining high data efficiency. As demonstrated in OmniDrive [14], incorporating auxiliary supervision (e.g., 3D object detection and lane detection) enhances the model’s semantic capabilities. However, as indicated in Tab. II, HERMES++ attains superior performance solely through the BEV representation and standard instruction tuning, without incorporating any detection or mapbased supervision. Specifically, we outperform Omni-L and OmniDrive-2D by 2.3% and 11.6% on the CIDEr metric, respectively, with consistent gains in METEOR and ROUGE scores. We attribute this improvement to the geometric prop- 

erties of the BEV representation and the proposed task interaction mechanisms. Baselines such as Omni-Q and ORION typically utilize sparse queries (e.g., via Q-Former3D [88]) to extract scene information. While effective, these approaches often benefit from auxiliary supervision to guide feature learning, compensating for the limited geometric context captured by sparse observations. In contrast, HERMES++ utilizes BEV, which inherently preserves rich semantic information and geometric interaction, allowing the model to learn effective scene representations without external guidance. 

Furthermore, we systematically compared HERMES++with our conference version [18]. While the conference version already achieves highly competitive results, HERMES++ establishes a new state-of-the-art across both tasks. As shown in Tab. II, these upgrades yield a 13.7% reduction in 3s generation error alongside improvements in understanding metrics, demonstrating the effectiveness of the deeper task interaction enabled by the newly introduced technical improvements. 

Moreover, our framework benefits from model scaling. Increasing the LLM parameters to 3.8B yields improvements across both domains, further reducing the generation error to 0.97 and boosting the CIDEr score to 0.772. This positive correlation indicates that our unified modeling approach effectively internalizes spatial-semantic representations to interpret complex driving scenes, thereby bridging the gap between geometric perception and linguistic understanding. 

## _B. Qualitative Evaluation_ 

Fig. 3 presents qualitative results from HERMES++. As highlighted by the green text, the model demonstrates strong scene understanding capabilities. Notably, it is able to identify fine-grained cues such as the “Shaw Foundation Alumni House” on signage and infer that the scene is likely located on a campus. This suggests that our BEV representation preserves sufficient granularity for fine-grained semantic reasoning, overcoming the resolution limitations often attributed 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

10 


Fig. 3: Qualitative results of HERMES++. The **green text** highlights the accurate responses to user instructions. The **red circles** track the geometric evolution of other objects in the predicted point clouds. 

to compressed features. Regarding scene evolution, the red circles track the precise geometric progression of other objects, maintaining high structural integrity consistent with the ground truth. This alignment between textual interpretation and physical trajectories validates the effectiveness of our framework in bridging semantic understanding with geometric simulation. 

## _C. Analysis and Ablation Study_ 

The following experiments are conducted on the NuScenes dataset. Unless specified, all the ablation experiments are performed using 25% of the training data. 

_1)_ **_Analysis of BEV Input Representation_** _:_ We first investigate the BEV input representation, focusing on its superiority over direct multi-view inputs and on how spatial resolution balances geometry information with computational efficiency. 

**Effectiveness of the BEV Input.** To demonstrate the effectiveness of BEV representations as a unified interface, we compare our approach against a strong multi-view baseline where CLIP-encoded image features are directly input into the LLM. To ensure comparable information capacity, image features are resized to 2,532 tokens, a token budget comparable to that of our BEV input. The LLM, BEVFormer, and render head (without up/downsampling layers) then process these features for scene understanding and future prediction. 

Quantitative results in Fig. 4 reveal that while both methods achieve highly competitive scene understanding performance with only 0.001 METEOR difference, they diverge significantly in generation tasks. Our BEV approach significantly outperforms the multi-view baseline, reducing the Chamfer Distance at 3s by _∼_ 32%. We attribute this to the spatial structural collapse of flattened image tokens during LLM processing, which hinders accurate 3D geometry recovery while retaining rich semantics. As shown in the qualitative case in Fig. 4, the multi-view baseline hallucinates a left turn due to misleading road markings, whereas our BEV representation, preserving spatial topology, correctly predicts a straight trajectory. This highlights BEV features as a superior, unified representation that effectively balances semantics with the geometric structural prior required for accurate forecasting. 

**Inference Cost of the BEV Input.** We further profile the inference cost of the two input interfaces. Both variants are measured on a single A100 under the same setting, with bf16 autocast enabled in the vision path. Since they share the same image backbone and are given comparable token budgets, the BEVFormer and the downsampling layer account for the entire runtime difference. Tab. III shows that the attention over BEV grids is not a dominant cost: the BEVFormer and the 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

11 


Fig. 4: Qualitative case and comparison between Multi-view-based and BEV-based inputs. While both methods yield comparable scene understanding performance (see METEOR scores), the multi-view baseline suffers from spatial structural collapse. 

TABLE III: Latency of the vision path before the LLM and the resulting token cost for the two input interfaces. Vision path total covers the image backbone and the feature-to-token stage. All values are measured on one A100 under bf16 and averaged over repeated samples. 

|Stage|Multi-view<br>as LLM input|BEV<br>as LLM input|
|---|---|---|
|Image backbone, 6 cams 1600_×_928|112.1 ms|112.1 ms|
|Feature to LLM tokens|0.9 ms|60.2 ms|
|# LLM visual tokens|2,532|2,025|
|LLM prefill|19.2 ms|15.8 ms|
|Vision path total|_∼_113 ms|_∼_172 ms|


downsampling layer add about 60 ms, which brings the vision path before the LLM from about 113 ms to about 172 ms, while the token budget and the prefill of the two interfaces remain comparable. This cost is incurred once per frame and is independent of the length of the generated answer and of the number of predicted future frames. We regard it as an acceptable price for an interface that accommodates spatial geometry and semantics at the same time, which is what yields the substantial gain in geometric accuracy reported above. 

**Impact of BEV Representation Scales.** We further evaluate the impact of BEV spatial resolution, which entails a trade-off between geometric consistency and the tokenprocessing capacity of LLMs. As shown in Tab. IV, we compare downsampling strategies ( _×_ 4 _, ×_ 8) against directly learning coarse features (‘Direct Query’). The ‘Downsample ( _×_ 4)’ yields the best trade-off between generation and understanding, achieving the lowest CD at 0–3s and a CIDEr score of 0.720. Notably, downsampling from a fine-grained feature map significantly surpasses direct coarse querying. Specifically, the ‘Downsample ( _×_ 4)’ strategy reduces the CD at 3s from 2.012 to 1.436, representing a 26.8% improvement. This result indicates that capturing detailed geometric information at a high resolution prior to compression is essential for 

TABLE IV: Ablation on downsampling scales for the BEV. M., R., and C. are METEOR, ROUGE, and CIDEr, respectively. 

|BEVConfiguration||Gener|ation||Un|derstand|ing|
|---|---|---|---|---|---|---|---|
|i|0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|Downsample (_×_8)|0.827|1.084|1.410|1.781|0.370|0.314|0.681|
|Downsample (_×_4)|0.588|0.879|1.146|1.436|0.378|0.322|0.720|
|Direct Query (_×_4)|0.769|1.211|1.615|2.012|0.378|0.322|0.723|


TABLE V: Ablation on the Joint Geometric Optimization strategy. M., R., and C. indicate METEOR, ROUGE, and CIDEr, respectively. 

|_L_|_L_||Gene|ration||U|nderstandi|ng|
|---|---|---|---|---|---|---|---|---|
|cos|gram|0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|-|-|0.656|0.967|1.270|1.637|0.379|0.322|0.722|
|✓|-|0.594|0.890|1.161|1.441|0.378|0.321|0.717|
|-|✓|0.608|0.920|1.218|1.544|0.378|0.321|0.717|
|✓|✓|0.588|0.879|1.146|1.436|0.378|0.322|0.720|


preserving structural integrity, whereas direct coarse querying results in irretrievable information loss. In contrast, excessive downsampling ( _×_ 8) creates an information bottleneck, degrading the CD at 3s to 1.781 and dropping the CIDEr to 0.681, confirming that sufficient spatial resolution is critical for both precise future prediction and semantic understanding. 

_2)_ **_Analysis of Joint Geometric Optimization_** _:_ We then investigate the impact of the proposed Joint Geometric Optimization strategy. As in Tab. V, depending exclusively on explicit geometric constraints yields a suboptimal CD of 1.637 at the 3s horizon. Incorporating implicit geometric regularization with _L_ cos significantly enhances performance, reducing the CD to 1.441. This indicates that enforcing voxel-wise feature consistency with geometry-aware priors is essential for accurate structure generation. Furthermore, only employing _L_ gram also provides a noticeable improvement (CD of 1.544). We attribute this to the ability of the Gram matrix to capture 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

12 


Fig. 5: Visualization of internal representations. (a) Features learned with only explicit geometric constraints. (b) The corresponding ground-truth point cloud. (c) Predicted features learned with the Joint Geometric Optimization strategy. 

global structural patterns and internal feature correlations, serving as a complement to the spatially strict Cosine loss. The integration of both implicit geometric regularizers yields superior performance (CD of 1.436), demonstrating a synergistic effect in which joint constraints on local feature consistency and global structural coherence encourage plausible 3D representations while maintaining understanding performance. 

To further validate the geometric regularization effect, we visualize the learned BEV features and demonstrate the effectiveness of our Joint Geometric Optimization strategy. As shown in Fig. 5(a), relying on explicit geometric constraints inevitably leads to depth ambiguity. This manifests as conspicuous ray-shaped artifacts extending along camera projection lines and an abnormally high response concentration at the ego-center, which overshadows the scene’s essential geometric structure. In contrast, the proposed Joint Geometric Optimization strategy imposes explicit constraints on the output while implicitly regularizing the latent manifold. As shown in Fig. 5(c), this approach effectively suppresses projection artifacts and the central bias, yielding spatially compact features that strictly adhere to the intrinsic geometry presented in the point cloud (Fig. 5(b)). This confirms that the joint mechanism guides the model to learn a cleaner, structurally faithful latent space rather than overfitting to perspective camera views. 

_3)_ **_Analysis of Current-to-Future Link_** _:_ We perform a progressive ablation study to validate our Current-to-Future Link in Tab. VI. The ‘w/o Link’ entirely removes the Link module, attempting to predict the future by directly copying **B** _t_ and adding future ego-motion states. This naive propagation fails to model the dynamic evolution of the environment, resulting in a severe performance drop with a 3s CD of 2.377 and a CIDEr drop to 0.433. Introducing the Simple Link, consisting of 3 vanilla attention layers, resolves this bottleneck and drastically reduces the 3s CD to 1.542. 

TABLE VI: Ablation on Current-to-Future Link. M., R., and C. indicate METEOR, ROUGE, and CIDEr, respectively. 

|Modules||Gener|ation||Un|derstandi|ng|
|---|---|---|---|---|---|---|---|
||0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|w/o Link|0.891|1.368|1.877|2.377|0.290|0.263|0.433|
|w/ Simple Link|0.609|0.919|1.207|1.542|0.378|0.322|0.718|
|+ Textual Injection|0.602|0.907|1.205|1.506|0.376|0.321|0.717|
|+ Ego Modulation|0.597|0.895|1.165|1.442|0.377|0.320|0.711|
|+ More blocks|**0.588**|**0.879**|**1.146**|**1.436**|**0.378**|**0.322**|**0.720**|


TABLE VII: Ablation on interaction of tasks. M., R., and C. indicate METEOR, ROUGE, and CIDEr, respectively. 

|Under.|Gen.||Gene|ration||Un|derstandi|ng|
|---|---|---|---|---|---|---|---|---|
|||0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|✓|-|-|-|-|-|0.379|0.322|0.726|
|-|✓|0.599|0.885|1.157|1.434|-|-|-|
|Separated|unification|0.600|0.981|1.296|1.634|0.376|0.320|0.703|
|✓|✓|**0.588**|**0.879**|**1.146**|**1.436**|**0.378**|**0.322**|**0.720**|


Incorporating Textual Injection reduces the CD to 1.506, suggesting that semantic abstractions and world knowledge derived from the understanding branch provide crucial context for geometric generation, effectively conditioning future prediction on linguistic priors. Another pronounced improvement is achieved by introducing the Ego Modulation, which further lowers the CD to 1.442. This module injects the egovehicle’s kinematic states into the feature modulation process. It is pivotal for decoupling the ego-motion from the scene’s inherent dynamics, thereby preventing the misinterpretation of static background shifts as object motion. Finally, scaling up the network depth from 3 to 6 achieves the best CD of 1.436 and boosts the CIDEr score to 0.720. This indicates that sufficient model capacity is required to capture the highly non-linear temporal evolution of complex driving scenarios. At the same time, the parallel improvement in understanding metrics suggests a positive interaction between the two tasks. Compared with the implicit geometric regularization, which reduces the 3s CD from 1.637 to 1.436 (Tab. V), the gains of the Textual Injection and the Ego Modulation are smaller but consistent across horizons. 

_4)_ **_Analysis of task interaction_** _:_ We then analyze the interaction between future generation and scene understanding to validate the necessity of the proposed framework. 

**Impact of Task Unification.** Tab. VII evaluates the influence of joint training compared to single-task specialists. The ‘Separated unification’ baseline, where tasks share the visual tokenizer but operate without deep interaction, yields suboptimal performance with a CD of 1.634 at 3 seconds and a CIDEr score of 0.703. In contrast, our framework significantly improves these metrics to 1.436 and 0.720, respectively. This demonstrates that the proposed unified modeling is effective. Specifically, the semantic context guides geometric evolution, while geometric constraints provide physical grounding for language reasoning. Thus, the joint model achieves performance comparable to specialized single-task models without requiring separate architectures. 

**Impact of World Queries Integration Strategy.** We further 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

13 

TABLE VIII: Ablation on world queries integration. M., R., and C. indicate METEOR, ROUGE, and CIDEr, respectively. 


analyze the integration of world queries **Q**<sup>_w_</sup> with the LLM. We compare three settings as shown in Tab. VIII. The baseline (a), i.e., separated unification, which relies solely on Textual Injection for task unification, yields a suboptimal CD of 1.634. Setting (b) introduces **Q**<sup>_w_</sup> to aggregate BEV features but bypasses the LLM reasoning process. While this improves the CD to 1.526 by enhancing feature extraction, the lack of deep semantic interaction limits its potential. Our proposed method (c), which processes **Q**<sup>_w_</sup> directly through the LLM, achieves the best performance with a CD of 1.436 and a CIDEr score of 0.720. This improvement indicates that the LLM effectively encodes semantic information into the **Q**<sup>_w_</sup> , which serves as a critical guide for future geometric prediction. Furthermore, since the world queries participate in the forward pass, the gradients from the generation objective backpropagate to refine the LLM, thereby improving the text understanding capability. 

_5)_ **_Analysis of Hyperparameters and Configurations_** _:_ Finally, we systematically investigate the impact of specific network hyperparameters and configurations, including the query initialization strategy, the number of world queries, and the temporal prediction horizon. 

**Impact of Initialization of World Queries.** We first investigate the strategy for initializing world queries to validate the necessity of perceptual anchoring. As shown in Tab. IXa, we first introduce a ‘Random Init’ baseline where queries are learned as independent parameters. This setting yields a suboptimal CD of 1.448 at 3s. In contrast, initializing queries directly from BEV features consistently improves performance. This confirms that anchoring world queries to the current perceptual state establishes a direct channel between input features and future predictions, facilitating effective gradient flow and semantic alignment. Among the BEV-based strategies, we compare parametric methods (e.g., Attention Pooling, Cross Attention) with heuristic ones (e.g., Average Pooling, Max Pooling). Notably, the simple Max Pooling strategy achieves the best overall performance (CD 1.436), surpassing the more complex Cross Attention mechanism. We attribute this to the inherent sparsity of BEV representations, where Max Pooling effectively captures the most salient features within the grid (e.g., object occupancy) while ignoring 

TABLE IX: Ablation on hyperparameters and configurations. M., R., and C. indicate METEOR, ROUGE, and CIDEr. 

(a) Ablation on the source of world queries 

|Method||Gener|ation||U|nderstandi|ng|
|---|---|---|---|---|---|---|---|
||0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|Random Init|0.598|0.883|1.161|1.448|0.378|0.321|0.714|
|Attn. Pool|0.595|0.892|1.152|1.438|0.377|0.321|0.716|
|Cross Attn.|0.603|0.892|1.155|1.442|0.378|0.322|0.719|
|Avg. Pool|0.597|0.883|1.153|1.444|0.378|0.321|0.713|
|Max Pool|0.588|0.879|1.146|1.436|0.378|0.322|0.720|


(b) Ablation on the number of world queries 

|_n_||||Gen|eration||||Underst|anding||
|---|---|---|---|---|---|---|---|---|---|---|---|
|||0s _↓_||1s _↓_|2s _↓_||3s _↓_|M. _↑_|R.|_↑_|C. _↑_|
|0||0.598||0.910|1.17|3|1.478|0.377|0.3|21|0.716|
|1||0.593||0.888|1.14|6|1.419|0.377|0.3|21|0.712|
|2||0.599||0.884|1.14|8|1.431|0.377|0.3|21|0.717|
|4||0.588||0.879|1.14|6|1.436|0.378|0.3|22|0.720|
|8<br>) A<br>on<br>ith|bl<br>up<br> gr|0.594<br>ation <br>to 10<br>ound|on <br>s.<br> tru|0.889<br> genera<br>The 10s<br>th at th|1.15<br>tion len<br>colum<br>at hori|2<br>gth. <br>n is<br>zon.|1.430<br> The last <br>averaged|0.378<br> row <br>over|0.3<br>extend<br>valida|21<br>s the s<br>tion sc|0.719<br>uperv<br>enario|
||Se|cond|||G|enerati|on||Un|derstan|ding|
|0|1|2|3|0s _↓_|1s _↓_|2s _↓_|3s _↓_|10s _↓_|M. _↑_|R. _↑_|C. _↑_|
|✓|✓|-|-|0.550|0.835|-|-|-|0.380|0.322|0.723|
|✓|✓|✓|-|0.575|0.851|1.147|-|-|0.378|0.322|0.718|
|-|✓|✓|✓|-|0.933|1.189|1.476|-|0.378|0.321|0.716|
|✓|-|-|✓|0.584|-|-|1.677|-|0.379|0.322|0.723|
|✓|✓|✓|✓|0.588|0.879|1.146|1.436|-|0.378|0.322|0.720|
|Ext|end|ed to 1|0s|0.704|1.608|2.476|3.139|4.579|0.376|0.323|0.718|


(c) Ablation on generation length. The last row extends the supervision up to 10s. The 10s column is averaged over validation scenarios with ground truth at that horizon. 

background noise. Average Pooling dilutes these signals, and parametric methods may face optimization challenges due to limited training data. 

**Impact of Number of World Queries.** We further analyze the quantity _n_ of world queries **Q**<sup>_w_</sup> _∈_ R<sup>(∆</sup><sup>_t×n_)</sup><sup>_×C_</sup> , which serve as an information bridge between temporal BEV features and the LLM. As shown in Tab. IXb, _n_ = 0 relies solely on Textual Injection within the Current-to-Future Link, which yields a suboptimal CD of 1.478 at the 3s horizon. Introducing world queries establishes a dedicated geometricsemantic bridge to guide future generation. Specifically, setting _n_ = 4 reduces the 3s CD by 0.04 while elevating the CIDEr metric to 0.720. This validates the effectiveness of the queries in aggregating semantic context from BEV observations and textual instructions. Further increasing _n_ to 8 causes slight regressions in 0–2s generation. Thus, we adopt _n_ =4 as the default configuration to balance computational efficiency with representational capacity. 

**Impact of Generation Horizon.** Tab. IXc presents the impact of prediction horizon length on model performance. While shorter horizons such as 0–1s yield a lower CD of 0.550 due to reduced uncertainty, modeling long-term evolution is essential for comprehensive scene understanding. We observe that temporal continuity is critical. For instance, the discontinuous setting of 0s and 3s results in a sharp degradation in CD from 3s to 1.677, indicating that intermediate states serve as necessary bridges for reasoning about future dynamics. Similarly, excluding the current state (1–3s) hampers performance 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

14 

TABLE X: VQA results on NuScenes-QA dataset [82]. 

|Method|Reference|Modality|Acc. (%) _↑_|
|---|---|---|---|
|LLaVA [11]|NeurIPS 23|Camera|47.4|
|BEVDet+BUTD [82]|AAAI 24|Camera|57.0|
|BEVDet+MCAN [82]|AAAI 24|Camera|57.9|
|CenterPoint+BUTD [82]|AAAI 24|LiDAR|58.1|
|CenterPoint+MCAN [82]|AAAI 24|LiDAR|59.5|
|LiDAR-LLM [89]|AAAI 25|LiDAR|48.6|
|Omni-Q [14]|CVPR 25|Camera|59.2|
|OpenDriveVLA-7B [90]|AAAI 26|Camera|58.2|
|HERMES++|-|Camera|**61.3**|


TABLE XI: The results on driving with language leaderboard [15], where ‘Acc.’, ‘GPT’, and ‘FS’ indicate Accuracy, GPT-score, and Final Score, respectively. 

|Method|Reference|Acc. _↑_|GPT _↑_|Match _↑_|FS _↑_|
|---|---|---|---|---|---|
|DriveLM [15]|ECCV 24|0.65|0.53|0.28|0.50|
|Team NVIDIA [91]|CVPRW 24|0.78|0.60|-|0.59|
|MMFM<br>AD [91]|CVPRW 24|0.67|0.64|-|0.57|
|Omni-Q [14]|CVPR 25|0.78|**0.64**|0.37|0.58|
|FSDrive [54]|NeurIPS 25|0.72|0.63|0.39|0.57|
|HERMES++|-|**0.83**|0.61|**0.43**|**0.59**|


as the model lacks the initial geometric reference. Our default setting of 0–3s strikes an optimal balance, maintaining longterm prediction with a CD of 1.436 while preserving high semantic understanding capabilities. 

As shown in the last row of Tab. IXc, extending the supervised horizon to 10 seconds maintains understanding metrics but degrades predicted geometry. The CD at 3s increases from 1.436 to 3.139, reaching 4.579 at 10s. This degradation primarily affects the predicted future rather than the current frame, suggesting long-horizon targets are weakly determined. We attribute this behavior to the weak determinacy of long-horizon targets. Within 10s, the ego vehicle often travels beyond the evaluation range, making the geometry largely unobservable from the current frame. The inconsistent gradients from long-horizon supervision interfere with nearhorizon objectives, causing a slight degradation in 1-3 second accuracy despite unchanged supervision. This indicates that a metric-based protocol is most reliable within the observable range, justifying our 3-second horizon for main experiments. Reliable long-horizon geometry prediction requires a larger observable context or an evaluation protocol accounting for unobserved regions, which warrants future research. 

## _D. Generalization to Additional Tasks_ 

_1)_ **_Understanding Capability on Other Datasets_** _:_ To further evaluate the generalization capability of HERMES++ in diverse driving scenarios, we extend our evaluation to two popular benchmarks: NuScenes-QA [82], which focuses on 3D spatial perception statistics, and DriveLM [15], which emphasizes graph-based reasoning. 

As shown in Tab. X, HERMES++ achieves state-of-theart performance with an accuracy of 61.3%. Generalist 2D VLMs such as LLaVA [11] struggle on this benchmark, largely due to their lack of 3D spatial modeling. In contrast, modular approaches that combine 3D detectors with QA heads, such as CenterPoint+MCAN [82], perform significantly 

TABLE XII: Comparison of the motion planning in nuScenes [78] validation set. 

|Method|Reference||L2 (|m) _↓_||C|ollisio|n (%|) _↓_|
|---|---|---|---|---|---|---|---|---|---|
|||1s|2s|3s|Avg.|1s|2s|3s|Avg.|
|Ego-MLP [93]|arXiv 23|0.15|0.32|0.59|0.35|0.00|0.27|0.85|0.37|
|BEV-Planner [94]|CVPR 24|0.30|0.52|0.83|0.55|0.10|0.37|1.30|0.59|
|BEV-Planner++ [94]|CVPR 24|0.16|0.32|0.57|0.35|0.00|0.29|0.73|0.34|
|ST-P3 [95]|ECCV 22|1.33|2.11|2.90|2.11|0.23|0.62|1.27|0.71|
|UniAD [96]|CVPR 23|0.20|0.42|0.75|0.46|0.02|0.25|0.84|0.37|
|VAD-Base [97]|ICCV 23|0.17|0.34|0.60|0.37|0.04|0.27|0.67|0.33|
|OmniDrive [14]|CVPR 25|0.40|0.80|1.32|0.84|0.04|0.46|2.32|0.94|
|OmniDrive++ [14]|CVPR 25|0.14|0.29|0.55|0.33|0.00|0.13|0.78|0.30|
|Doe-1 [22]|arXiv 24|0.50|1.18|2.11|1.26|0.04|0.37|1.19|0.53|
|Epona [37]|ICCV 25|0.61|1.17|1.98|1.25|0.01|0.22|0.85|0.36|
|ORION [65]|ICCV 25|0.17|0.31|0.55|0.34|0.05|0.25|0.80|0.37|
|HERMES++|-|0.16|0.33|0.62|0.37|0.00|0.16|0.72|0.29|


better. Notably, HERMES++ outperforms the camera-based SOTA Omni-Q [14] by 2.1% and effectively surpasses the LiDAR-based specialist CenterPoint+MCAN, which scores 59.5%. This result demonstrates that the BEV representation effectively encodes rich geometric information comparable to LiDAR, providing robust spatial grounding for visual question answering without relying on depth sensors during inference. 

We further evaluate the reasoning capability of HERMES++ on the DriveLM benchmark, which demands integrated reasoning across perception, prediction, and planning. As shown in Tab. XI, HERMES++ achieves a highly competitive Final Score (FS) of 0.59, matching the challenge winner Team NVIDIA and outperforming strong baselines like OmniQ [14] and FSDrive [54]. Notably, as shown in Fig. 1(d), our method achieves a prediction accuracy of 0.83, surpassing Omni-Q (0.78) by 5%. Furthermore, HERMES++ attains a leading score of 0.43 in the ‘Match’ metric without auxiliary detection supervision [92], validating the advantage of the 3D representation. By enforcing geometric consistency through the generation branch, the model inherently encodes precise spatial semantics, enabling it to ground its reasoning in a 3D scene rather than relying solely on language priors. 

_2)_ **_Motion Planning_** _:_ To further evaluate the generalization capability of our learned unification model, we extend HERMES++ to the open-loop motion planning task on the nuScenes validation set. Specifically, we append a lightweight MLP head to the world queries **Q**<sup>_w_</sup> to hierarchically regress future trajectories, which subsequently serve as conditions for generating future point clouds. It is worth emphasizing that our model is trained solely with text instructions and future geometric supervision. As shown in Tab. XII, HERMES++ achieves highly competitive performance with an average L2 error of 0.37m and a collision rate of 0.29%. Compared to the recent leading method ORION, HERMES++ achieves a 0.08% lower collision rate while maintaining a comparable L2 error. Furthermore, our method substantially improves over OmniDrive and surpasses OmniDrive++ in average collision rate. These results demonstrate that by optimizing for future scene generation under textual guidance, HERMES++ effectively internalizes world knowledge and actionable driving dynamics, enabling planning potential even without perception supervision. 

15 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

TABLE XIII: Comparison of different LLMs. M., R., and C. indicate METEOR, ROUGE, and CIDEr, respectively. (a) Comparison across different LLM series. 

|Model||Gene|ration||U|nderstandi|ng|
|---|---|---|---|---|---|---|---|
||0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|Llama-3.2 [99]|0.617|0.936|1.227|1.533|0.377|0.319|0.700|
|Qwen3 [98]|0.614|0.910|1.198|1.521|0.374|0.317|0.696|
|InternVL2 [74]|**0.588**|**0.879**|**1.146**|**1.436**|**0.378**|**0.322**|**0.720**|
|(b) Comparis|on acro|ss mod|el scale|s on In|ternVL|2 series|[74].|


|Model||Gener|ation||U|nderstandi|ng|
|---|---|---|---|---|---|---|---|
||0s _↓_|1s _↓_|2s _↓_|3s _↓_|M. _↑_|R. _↑_|C. _↑_|
|0.8B|0.601|0.890|1.150|1.434|0.376|0.319|0.708|
|1.8B|0.588|0.879|1.146|1.436|0.378|0.322|0.720|
|3.8B|**0.557**|**0.768**|**0.991**|**1.255**|**0.383**|**0.325**|**0.742**|


_3)_ **_Generalization to Different LLMs_** _:_ To verify the universality of HERMES++, we conduct experiments across various LLM architectures and scales using 25% of the training data. 

**Effect of Model Architecture.** We first evaluate the adaptability of our method by integrating three representative LLMs with comparable parameter counts [74], [98], [99]. As shown in Tab. XIIIa, our framework consistently achieves promising performance across all architectures, demonstrating its generalization capability. InternVL2 yields superior results in both generation and understanding metrics (e.g., achieving the lowest prediction error at 3s). We attribute this to its reliable vision-language alignment, which effectively adapts to our BEV-based tokenization strategy. 

**Impact of Model Scale.** We further investigate the scalability of our approach using the InternVL2 series. Tab. XIIIb reveals a clear positive correlation between model size and performance. As the number of parameters increases, the model achieves significant gains in both future prediction and scene understanding. Specifically, the 3.8B model outperforms the 0.8B variant by 12.5% for the 3s prediction error. We argue that our framework effectively leverages the richer world knowledge and stronger reasoning capabilities inherent in larger language models. This indicates that our method is highly scalable and has the potential for further performance gains as foundation models become increasingly powerful. 

## VII. CONCLUSION 

In this paper, we present HERMES++, a unified driving world model that integrates 3D scene understanding and future geometry prediction. By leveraging the BEV representation, we effectively consolidate multi-view visual information into a format compatible with LLMs. To facilitate interaction between semantic reasoning and geometric evolution, we introduce LLM-enhanced world queries to enable knowledge transfer. These queries then interact with LLM-encoded BEV features to generate latent representations for future timestamps via a Current-to-Future Link. To further ensure the structural consistency of predicted futures, we devise a Joint Geometric Optimization strategy that integrates explicit geometric constraints with implicit latent regularization to align 

internal representations with geometry-aware priors. Extensive evaluations validate the effectiveness of our approach. HERMES++ achieves strong performance, outperforming specialists in both generation and understanding tasks. We hope this work establishes a solid foundation for future research in interpretable and predictive driving systems. 

**Limitation and future work.** While this work presents a solid exploration toward a unified driving world model, how to leverage the semantic priors encapsulated in pre-trained multimodal large models for BEV input requires further investigation. Additionally, extending the generation to broader output modalities, such as future images and 3D occupancy, presents an interesting direction for comprehensive scene simulation. **Acknowledgment.** This work was supported by the NSFC (62225603, 62441615, and 623B2038). 

## REFERENCES 

- [1] L. Chen, P. Wu, K. Chitta, B. Jaeger, A. Geiger, and H. Li, “End-toend autonomous driving: Challenges and frontiers,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 46, no. 12, pp. 10 164–10 183, 2024. 

- [2] S. Gao, J. Yang, L. Chen, K. Chitta, Y. Qiu, A. Geiger, J. Zhang, and H. Li, “Vista: A generalizable driving world model with high fidelity and versatile controllability,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2024, pp. 91 560–91 596. 

- [3] G. Zhao, X. Wang, Z. Zhu, X. Chen, G. Huang, X. Bao, and X. Wang, “Drivedreamer-2: Llm-enhanced world models for diverse driving video generation,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 39, no. 10, 2025, pp. 10 412–10 420. 

- [4] S. Tu, X. Zhou, D. Liang, X. Jiang, Y. Zhang, X. Li, and X. Bai, “The role of world models in shaping autonomous driving: A comprehensive survey,” _Frontiers of Computer Science_ , 2026. 

- [5] A. Hu, L. Russell, H. Yeo, Z. Murez, G. Fedoseev, A. Kendall, J. Shotton, and G. Corrado, “Gaia-1: A generative world model for autonomous driving,” _arXiv preprint arXiv:2309.17080_ , 2023. 

- [6] W. Zheng, W. Chen, Y. Huang, B. Zhang, Y. Duan, and J. Lu, “Occworld: Learning a 3d occupancy world model for autonomous driving,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 55–72. 

- [7] Z. Yang, L. Chen, Y. Sun, and H. Li, “Visual point cloud forecasting enables scalable autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 14 673–14 684. 

- [8] J. Hou, Z. Liu, D. Liang, Z. Zou, X. Ye, and X. Bai, “Query-based temporal fusion with explicit motion for 3d object detection,” in _Proc. Adv. Neural Inf. Process. Syst._ , vol. 36, 2023, pp. 75 782–75 797. 

- [9] J. Li, Z. Liu, J. Hou, and D. Liang, “Dds3d: Dense pseudo-labels with dynamic threshold for semi-supervised 3d object detection,” in _Proc. IEEE Int. Conf. Robotics Automation_ , 2023, pp. 9245–9252. 

- [10] D. Liang, T. Feng, X. Zhou, Y. Zhang, Z. Zou, and X. Bai, “Parameterefficient fine-tuning in spectral domain for point cloud learning,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 47, no. 12, pp. 10 949–10 966, 2025. 

- [11] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” in _Proc. Adv. Neural Inf. Process. Syst._ , vol. 36, 2023, pp. 34 892–34 916. 

- [12] Z. Chen, J. Wu, W. Wang, W. Su, G. Chen, S. Xing, M. Zhong, Q. Zhang, X. Zhu, L. Lu _et al._ , “Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 24 185–24 198. 

- [13] Z. Li, B. Yang, Q. Liu, Z. Ma, S. Zhang, J. Yang, Y. Sun, Y. Liu, and X. Bai, “Monkey: Image resolution and text label are important things for large multi-modal models,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 26 763–26 773. 

- [14] S. Wang, Z. Yu, X. Jiang, S. Lan, M. Shi, N. Chang, J. Kautz, Y. Li, and J. M. Alvarez, “Omnidrive: A holistic vision-language dataset for autonomous driving with counterfactual reasoning,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2025, pp. 22 442–22 452. 

- [15] C. Sima, K. Renz, K. Chitta, L. Chen, H. Zhang, C. Xie, J. Beißwenger, P. Luo, A. Geiger, and H. Li, “Drivelm: Driving with graph visual question answering,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 256– 274. 

16 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

- [16] Z. Xu, Y. Zhang, E. Xie, Z. Zhao, Y. Guo, K.-Y. K. Wong, Z. Li, and H. Zhao, “Drivegpt4: Interpretable end-to-end autonomous driving via large language model,” _IEEE Robotics and Automation Letters_ , pp. 8186–8193, 2024. 

- [17] C. Shi, S. Shi, K. Sheng, B. Zhang, and L. Jiang, “Drivex: Omni scene modeling for learning generalizable world knowledge in autonomous driving,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2025, pp. 28 599–28 609. 

- [18] X. Zhou, D. Liang, S. Tu, X. Chen, Y. Ding, D. Zhang, F. Tan, H. Zhao, and X. Bai, “Hermes: A unified self-driving world model for simultaneous 3d scene understanding and generation,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2025, pp. 27 817–27 827. 

- [19] D. Ha and J. Schmidhuber, “Recurrent world models facilitate policy evolution,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2018. 

- [20] X. Wang, Z. Zhu, G. Huang, X. Chen, J. Zhu, and J. Lu, “Drivedreamer: Towards real-world-drive world models for autonomous driving,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 55–72. 

- [21] E. Ma, L. Zhou, T. Tang, Z. Zhang, D. Han, J. Jiang, K. Zhan, P. Jia, X. Lang, H. Sun _et al._ , “Unleashing generalization of end-toend autonomous driving with controllable long video generation,” _arXiv preprint arXiv:2406.01349_ , 2024. 

- [22] W. Zheng, Z. Xia, Y. Huang, S. Zuo, J. Zhou, and J. Lu, “Doe-1: Closed-loop autonomous driving with large world model,” _arXiv preprint arXiv:2412.09627_ , 2024. 

- [23] C. Min, D. Zhao, L. Xiao, J. Zhao, X. Xu, Z. Zhu, L. Jin, J. Li, Y. Guo, J. Xing _et al._ , “Driveworld: 4d pre-trained scene understanding via world models for autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 15 522–15 533. 

- [24] J. Ma, X. Chen, J. Huang, J. Xu, Z. Luo, J. Xu, W. Gu, R. Ai, and H. Wang, “Cam4docc: Benchmark for camera-only 4d occupancy forecasting in autonomous driving applications,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 21 486–21 495. 

- [25] J. Yang, S. Gao, Y. Qiu, L. Chen, T. Li, B. Dai, K. Chitta, P. Wu, J. Zeng, P. Luo _et al._ , “Generalized predictive model for autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 14 662–14 672. 

- [26] F. Jia, W. Mao, Y. Liu, Y. Zhao, Y. Wen, C. Zhang, X. Zhang, and T. Wang, “Adriver-i: A general world model for autonomous driving,” _arXiv preprint arXiv:2311.13549_ , 2023. 

- [27] Y. Zhang, S. Gong, K. Xiong, X. Ye, X. Li, X. Tan, F. Wang, J. Huang, H. Wu, and H. Wang, “Bevworld: A multimodal world simulator for autonomous driving via scene-level bev latents,” _arXiv preprint arXiv:2407.05679_ , 2024. 

- [28] Y. Wang, J. He, L. Fan, H. Li, Y. Chen, and Z. Zhang, “Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 14 749–14 759. 

- [29] R. Gao, K. Chen, E. Xie, L. Hong, Z. Li, D.-Y. Yeung, and Q. Xu, “Magicdrive: Street view generation with diverse 3d geometry control,” in _Proc. Int. Conf. Learn. Representations_ , 2024. 

- [30] Y. Wen, Y. Zhao, Y. Liu, F. Jia, Y. Wang, C. Luo, C. Zhang, T. Wang, X. Sun, and X. Zhang, “Panacea: Panoramic and controllable video generation for autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 6902–6912. 

- [31] X. Li, Y. Zhang, and X. Ye, “Drivingdiffusion: layout-guided multi-view driving scenarios video generation with latent diffusion model,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 469–485. 

- [32] B. Li, J. Guo, H. Liu, Y. Zou, Y. Ding, X. Chen, H. Zhu, F. Tan, C. Zhang, T. Wang _et al._ , “Uniscene: Unified occupancy-centric driving scene generation,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2025, pp. 11 971–11 981. 

- [33] J. Ni, Y. Guo, Y. Liu, R. Chen, L. Lu, and Z. Wu, “Maskgwm: A generalizable driving world model with video mask reconstruction,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2025, pp. 22 381– 22 391. 

- [34] J. Lu, Z. Huang, Z. Yang, J. Zhang, and L. Zhang, “Wovogen: World volume-aware diffusion for controllable multi-camera driving scene generation,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 329–345. 

- [35] Y. Chen, Y. Wang, and Z. Zhang, “Drivinggpt: Unifying driving world modeling and planning with multi-modal autoregressive transformers,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2025, pp. 26 890–26 900. 

- [36] X. Hu, M. Jia, X. Guo, Q. Zhang, X.-x. Long, and W. Yin, “Drivingworld: Constructing world model for autonomous driving via video gpt,” in _Proc. Int. Conf. Pattern Recognit._ Springer, 2026, pp. 276–291. 

- [37] K. Zhang, Z. Tang, X. Hu, X. Pan, X. Guo, Y. Liu, J. Huang, L. Yuan, Q. Zhang, X.-X. Long _et al._ , “Epona: Autoregressive diffusion world model for autonomous driving,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2025, pp. 27 220–27 230. 

- [38] G. Zhao, C. Ni, X. Wang, Z. Zhu, X. Zhang, Y. Wang, G. Huang, X. Chen, B. Wang, Y. Zhang _et al._ , “Drivedreamer4d: World models are effective data machines for 4d driving scene representation,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2025, pp. 12 015–12 026. 

- [39] L. Wang, W. Zheng, Y. Ren, H. Jiang, Z. Cui, H. Yu, and J. Lu, “Occsora: 4d occupancy generation models as world simulators for autonomous driving,” _arXiv preprint arXiv:2405.20337_ , 2024. 

- [40] S. Gu, W. Yin, B. Jin, X. Guo, J. Wang, H. Li, Q. Zhang, and X. Long, “Dome: Taming diffusion model into high-fidelity controllable occupancy world model,” _arXiv preprint arXiv:2410.10429_ , 2024. 

- [41] B. Agro, Q. Sykora, S. Casas, T. Gilles, and R. Urtasun, “Uno: Unsupervised occupancy fields for perception and forecasting,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 14 487–14 496. 

- [42] Z. Huang, J. Zhang, and E. Ohn-Bar, “Neural volumetric world models for autonomous driving,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 195–213. 

- [43] Z. Yan, W. Dong, Y. Shao, Y. Lu, H. Liu, J. Liu, H. Wang, Z. Wang, Y. Wang, F. Remondino _et al._ , “Renderworld: World model with selfsupervised 3d label,” in _Proc. IEEE Int. Conf. Robotics Automation_ , 2025, pp. 6063–6070. 

- [44] J. Wei, S. Yuan, P. Li, Q. Hu, Z. Gan, and W. Ding, “Occllama: An occupancy-language-action generative world model for autonomous driving,” _arXiv preprint arXiv:2409.03272_ , 2024. 

- [45] V. Zyrianov, H. Che, Z. Liu, and S. Wang, “Lidardm: Generative lidar simulation in a generated world,” in _Proc. IEEE Int. Conf. Robotics Automation_ , 2025, pp. 6055–6062. 

- [46] X. Weng, J. Nan, K.-H. Lee, R. McAllister, A. Gaidon, N. Rhinehart, and K. M. Kitani, “S2net: Stochastic sequential pointcloud forecasting,” in _Proc. Eur. Conf. Comput. Vis._ , 2022, pp. 549–564. 

- [47] T. Khurana, P. Hu, D. Held, and D. Ramanan, “Point cloud forecasting as a proxy for 4d occupancy forecasting,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2023, pp. 1116–1124. 

- [48] L. Zhang, Y. Xiong, Z. Yang, S. Casas, R. Hu, and R. Urtasun, “Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion,” in _Proc. Int. Conf. Learn. Representations_ , 2024. 

- [49] M. Hassan, S. Stapf, A. Rahimi, P. Rezende, Y. Haghighi, D. Br¨uggemann, I. Katircioglu, L. Zhang, X. Chen, S. Saha _et al._ , “Gem: A generalizable ego-vision multimodal world model for finegrained ego-motion, object dynamics, and scene composition control,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2025, pp. 22 404– 22 415. 

- [50] J. Guo, Y. Ding, X. Chen, S. Chen, B. Li, Y. Zou, X. Lyu, F. Tan, X. Qi, Z. Li _et al._ , “Dist-4d: Disentangled spatiotemporal diffusion with metric depth for 4d driving scene generation,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2025, pp. 27 231–27 241. 

- [51] D. Liang, D. Zhang, X. Zhou, S. Tu, T. Feng, X. Li, Y. Zhang, M. Du, X. Tan, and X. Bai, “Unifuture: A 4d driving world model for future generation and perception,” in _Proc. IEEE Int. Conf. Robotics Automation_ , 2026. 

- [52] T. Xu, H. Lu, X. Yan, Y. Cai, B. Liu, and Y. Chen, “Occ-llm: Enhancing autonomous driving with occupancy-based large language models,” _arXiv preprint arXiv:2502.06419_ , 2025. 

- [53] H. Lu, Z. Liu, G. Jiang, Y. Luo, S. Chen, Y. Zhang, and Y.-C. Chen, “Uniugp: Unifying understanding, generation, and planing for end-toend autonomous driving,” _arXiv preprint arXiv:2512.09864_ , 2025. 

- [54] S. Zeng, X. Chang, M. Xie, X. Liu, Y. Bai, Z. Pan, M. Xu, and X. Wei, “Futuresightdrive: Thinking visually with spatio-temporal cot for autonomous driving,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2025. 

- [55] J. Wu, M. Zhong, S. Xing, Z. Lai, Z. Liu, Z. Chen, W. Wang, X. Zhu, L. Lu, T. Lu _et al._ , “Visionllm v2: An end-to-end generalist multimodal large language model for hundreds of vision-language tasks,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2024, pp. 69 925–69 975. 

- [56] Z. Zhang, Y. Ma, E. Zhang, and X. Bai, “Psalm: Pixelwise segmentation with large multi-modal model,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 74–91. 

- [57] R. Dong, C. Han, Y. Peng, Z. Qi, Z. Ge, J. Yang, L. Zhao, J. Sun, H. Zhou, H. Wei _et al._ , “Dreamllm: Synergistic multimodal comprehension and creation,” in _Proc. Int. Conf. Learn. Representations_ , 2024. 

- [58] J. H. Cho, B. Ivanovic, Y. Cao, E. Schmerling, Y. Wang, X. Weng, B. Li, Y. You, P. Kraehenbuehl, Y. Wang _et al._ , “Language-image models with 3d understanding,” in _Proc. Int. Conf. Learn. Representations_ , 2025. 

- [59] H. Fu, D. Zhang, Z. Zhao, J. Cui, H. Xie, B. Wang, G. Chen, H. Ye, D. Liang, and X. Bai, “Minddrive: A vision-language-action model for autonomous driving via online reinforcement learning,” in _Proc. Eur. Conf. Comput. Vis._ , 2026, pp. 503–522. 

JOURNAL OF L<sup>A</sup> TEX CLASS FILES, VOL. 18, NO. 9, SEPTEMBER 2020 

17 

- [60] Y. Zhou, L. Huang, Q. Bu, J. Zeng, T. Li, H. Qiu, H. Zhu, M. Guo, Y. Qiao, and H. Li, “Embodied understanding of driving scenarios,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 129–148. 

- [61] E. Cui, W. Wang, Z. Li, J. Xie, H. Zou, H. Deng, G. Luo, L. Lu, X. Zhu, and J. Dai, “Drivemlm: aligning multi-modal large language models with behavioral planning states for autonomous driving,” _Visual Intelligence_ , vol. 3, no. 1, p. 22, 2025. 

- [62] J.-J. Hwang, R. Xu, H. Lin, W.-C. Hung, J. Ji, K. Choi, D. Huang, T. He, P. Covington, B. Sapp _et al._ , “Emma: End-to-end multimodal model for autonomous driving,” _Trans. on Mach. Learn. Research_ , 2025. 

- [63] X. Tian, J. Gu, B. Li, Y. Liu, Y. Wang, Z. Zhao, K. Zhan, P. Jia, X. Lang, and H. Zhao, “Drivevlm: The convergence of autonomous driving and large vision-language models,” in _Conf. on robot learn._ , 2025, pp. 4698– 4726. 

- [64] H. Shao, Y. Hu, L. Wang, G. Song, S. L. Waslander, Y. Liu, and H. Li, “Lmdrive: Closed-loop end-to-end driving with large language models,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 15 120– 15 130. 

- [65] H. Fu, D. Zhang, Z. Zhao, J. Cui, D. Liang, C. Zhang, D. Zhang, H. Xie, B. Wang, and X. Bai, “Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2025, pp. 24 823–24 834. 

- [66] Y. Li, Z. Ge, G. Yu, J. Yang, Z. Wang, Y. Shi, J. Sun, and Z. Li, “Bevdepth: Acquisition of reliable depth for multi-view 3d object detection,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 37, no. 2, 2023, pp. 1477–1485. 

- [67] Z. Liu, H. Tang, A. Amini, X. Yang, H. Mao, D. L. Rus, and S. Han, “Bevfusion: Multi-task multi-sensor fusion with unified bird’s-eye view representation,” in _Proc. IEEE Int. Conf. Robotics Automation_ , 2023, pp. 2774–2781. 

- [68] H. Li, C. Sima, J. Dai, W. Wang, L. Lu, H. Wang, J. Zeng, Z. Li, J. Yang, H. Deng _et al._ , “Delving into the devils of bird’s-eye-view perception: A review, evaluation and recipe,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 46, no. 4, pp. 2151–2170, 2024. 

- [69] Z. Li, W. Wang, H. Li, E. Xie, C. Sima, T. Lu, Y. Qiao, and J. Dai, “Bevformer: Learning bird’s-eye-view representation from multi-camera images via spatiotemporal transformers,” in _Proc. Eur. Conf. Comput. Vis._ , 2022, pp. 1–18. 

- [70] C. Yang, Y. Chen, H. Tian, C. Tao, X. Zhu, Z. Zhang, G. Huang, H. Li, Y. Qiao, L. Lu _et al._ , “Bevformer v2: Adapting modern image backbones to bird’s-eye-view recognition via perspective supervision,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2023, pp. 17 830– 17 839. 

- [71] M. Cherti, R. Beaumont, R. Wightman, M. Wortsman, G. Ilharco, C. Gordon, C. Schuhmann, L. Schmidt, and J. Jitsev, “Reproducible scaling laws for contrastive language-image learning,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2023, pp. 2818–2829. 

- [72] Z. Liu, H. Mao, C.-Y. Wu, C. Feichtenhofer, T. Darrell, and S. Xie, “A convnet for the 2020s,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2022, pp. 11 976–11 986. 

- [73] D. Zhang, D. Liang, Z. Tan, X. Ye, C. Zhang, J. Wang, and X. Bai, “Make your vit-based multi-view 3d detectors faster via token compression,” in _Proc. Eur. Conf. Comput. Vis._ , 2024, pp. 56–72. 

- [74] Z. Chen, W. Wang, H. Tian, S. Ye, Z. Gao, E. Cui, W. Tong, K. Hu, J. Luo, Z. Ma _et al._ , “How far are we to gpt-4v? closing the gap to commercial multimodal models with open-source suites,” _Science China Information Sciences_ , vol. 67, no. 12, p. 220101, 2024. 

- [75] H. Yang, S. Zhang, D. Huang, X. Wu, H. Zhu, T. He, S. Tang, H. Zhao, Q. Qiu, B. Lin _et al._ , “Unipad: A universal pre-training paradigm for autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 15 238–15 250. 

- [76] H. Zhu, H. Yang, X. Wu, D. Huang, S. Zhang, X. He, H. Zhao, C. Shen, Y. Qiao, T. He _et al._ , “Ponderv2: Improved 3d representation with a universal pre-training paradigm,” _IEEE Trans. Pattern Anal. Mach. Intell._ , vol. 47, no. 8, pp. 6550–6565, 2025. 

- [77] P. Wang, L. Liu, Y. Liu, C. Theobalt, T. Komura, and W. Wang, “Neus: Learning neural implicit surfaces by volume rendering for multi-view reconstruction,” in _Proc. Adv. Neural Inf. Process. Syst._ , 2021, pp. 27 171–27 183. 

   - [80] S. Banerjee and A. Lavie, “Meteor: An automatic metric for mt evaluation with improved correlation with human judgments,” in _Proc. Annual Meeting of the Association for Computational Linguistics Workshop_ , 2005. 

   - [81] C.-Y. Lin, “Rouge: A package for automatic evaluation of summaries,” in _Proc. Annual Meeting of the Association for Computational Linguistics Workshop_ , 2004. 

   - [82] T. Qian, J. Chen, L. Zhuo, Y. Jiao, and Y.-G. Jiang, “Nuscenes-qa: A multi-modal visual question answering benchmark for autonomous driving scenario,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 38, no. 5, 2024, pp. 4542–4550. 

   - [83] Z. Zhao, H. Fu, D. Liang, X. Zhou, D. Zhang, H. Xie, B. Wang, and X. Bai, “Extending large vision-language model for diverse interactive tasks in autonomous driving,” _IEEE Trans. Image Process._ , vol. 35, pp. 8558–8573, 2026. 

   - [84] Y. Yan, Y. Mao, and B. Li, “Second: Sparsely embedded convolutional detection,” _Sensors_ , vol. 18, no. 10, p. 3337, 2018. 

   - [85] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen, “Lora: Low-rank adaptation of large language models,” in _Proc. Int. Conf. Learn. Representations_ , 2022. 

   - [86] X. Weng, J. Wang, S. Levine, K. Kitani, and N. Rhinehart, “Inverting the pose forecasting pipeline with spf2: Sequential pointcloud forecasting for sequential pose forecasting,” in _Conf. on robot learn._ , 2021, pp. 11– 20. 

   - [87] B. Li, Y. Zhang, D. Guo, R. Zhang, F. Li, H. Zhang, K. Zhang, P. Zhang, Y. Li, Z. Liu _et al._ , “Llava-onevision: Easy visual task transfer,” _Trans. on Mach. Learn. Research_ , 2025. 

   - [88] J. Li, D. Li, S. Savarese, and S. Hoi, “Blip-2: Bootstrapping languageimage pre-training with frozen image encoders and large language models,” in _Proc. Int. Conf. Mach. Learn._ , 2023, pp. 19 730–19 742. 

   - [89] S. Yang, J. Liu, R. Zhang, M. Pan, Z. Guo, X. Li, Z. Chen, P. Gao, H. Li, Y. Guo _et al._ , “Lidar-llm: Exploring the potential of large language models for 3d lidar understanding,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 39, no. 9, 2025, pp. 9247–9255. 

   - [90] X. Zhou, X. Han, F. Yang, Y. Ma, V. Tresp, and A. Knoll, “Opendrivevla: Towards end-to-end autonomous driving with large vision language action model,” in _Proc. AAAI Conf. Artif. Intell._ , 2026, pp. 13 782– 13 790. 

   - [91] OpenDriveLab, “CVPR 2024 autonomous driving challenge: Driving with language,” https://opendrivelab.com/challenge2024/#driving <u>with</u> language, 2024. 

   - [92] S. Wang, Y. Liu, T. Wang, Y. Li, and X. Zhang, “Exploring objectcentric temporal modeling for efficient multi-view 3d object detection,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2023, pp. 3621–3631. 

   - [93] J.-T. Zhai, Z. Feng, J. Du, Y. Mao, J.-J. Liu, Z. Tan, Y. Zhang, X. Ye, and J. Wang, “Rethinking the open-loop evaluation of end-toend autonomous driving in nuscenes,” _arXiv preprint arXiv:2305.10430_ , 2023. 

   - [94] Z. Li, Z. Yu, S. Lan, J. Li, J. Kautz, T. Lu, and J. M. Alvarez, “Is ego status all you need for open-loop end-to-end autonomous driving?” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2024, pp. 14 864– 14 873. 

   - [95] S. Hu, L. Chen, P. Wu, H. Li, J. Yan, and D. Tao, “St-p3: End-to-end vision-based autonomous driving via spatial-temporal feature learning,” in _Proc. Eur. Conf. Comput. Vis._ , 2022, pp. 533–549. 

   - [96] Y. Hu, J. Yang, L. Chen, K. Li, C. Sima, X. Zhu, S. Chai, S. Du, T. Lin, W. Wang _et al._ , “Planning-oriented autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2023, pp. 17 853–17 862. 

   - [97] B. Jiang, S. Chen, Q. Xu, B. Liao, J. Chen, H. Zhou, Q. Zhang, W. Liu, C. Huang, and X. Wang, “Vad: Vectorized scene representation for efficient autonomous driving,” in _Proc. IEEE Int. Conf. Comput. Vis._ , 2023, pp. 8340–8350. 

   - [98] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv _et al._ , “Qwen3 technical report,” _arXiv preprint arXiv:2505.09388_ , 2025. 

   - [99] Meta AI, “Llama 3.2: Revolutionizing edge ai and vision with open, customizable models,” https://ai.meta.com/blog/ llama-3-2-connect-2024-vision-edge-mobile-devices, 2024. 

- [78] H. Caesar, V. Bankiti, A. H. Lang, S. Vora, V. E. Liong, Q. Xu, A. Krishnan, Y. Pan, G. Baldan, and O. Beijbom, “nuscenes: A multimodal dataset for autonomous driving,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2020, pp. 11 621–11 631. 

- [79] R. Vedantam, C. Lawrence Zitnick, and D. Parikh, “Cider: Consensusbased image description evaluation,” in _Proc. IEEE Conf. Comput. Vis. Pattern Recognit._ , 2015, pp. 4566–4575. 

