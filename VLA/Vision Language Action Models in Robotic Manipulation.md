---
title: "Vision Language Action Models in Robotic Manipulation: A Systematic Review"
date: "2025-07-14"
authors: "Muhayy Ud Din; Waseem Akram; Lyes Saad Saoud; Jan Rosell; Irfan Hussain"
url: https://arxiv.org/abs/2507.10672
pdf: https://arxiv.org/pdf/2507.10672
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2507.10672)** / [論文ページ](https://arxiv.org/abs/2507.10672)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Vision Language Action Models in Robotic Manipulation: A Systematic Review 

# Muhayy Ud Din<sup>_a_</sup> , Waseem Akram<sup>_a_</sup> , Lyes Saad Saoud<sup>_a_</sup> , Jan Rosell<sup>_b_</sup> and Irfan Hussain*<sup>_a_</sup> 

_aKhalifa University Center for Autonomous Robotic Systems (KUCARS) Khalifa University United Arab Emirates. bInstitute of Industrial and Control Engineering (IOC) Universitat Politecnica de Catalunya Spain._ 

|A R T I C L E I N F O|A B S T R A C T|
|---|---|
|_Keywords_:|Vision Language Action (VLA) models represent a transformative shift in robotics, with the aim|
|Vision language models|of unifying visual perception, natural language understanding, and embodied control within a single|
|Robotic and embodied control<br>Foundation models<br>Language-conditioned manipulation and<br>control|learning framework. This review presents a comprehensive and forward-looking synthesis of the VLA<br>paradigm, with a particular emphasis on robotic manipulation and instruction-driven autonomy. We<br>comprehensively analyze 102 VLA models, 26 foundational datasets, and 12 simulation platforms that<br>collectively shape the development and evaluation of VLAs models. These models are categorized<br>into key architectural paradigms, each reflecting distinct strategies for integrating vision, language,<br>and control in robotic systems. Foundational datasets are evaluated using a novel criterion based<br>on task complexity, variety of modalities, and dataset scale, allowing a comparative analysis of<br>their suitability for generalist policy learning. We introduce a two-dimensional characterization<br>framework that organizes these datasets based on semantic richness and multimodal alignment,<br>showing underexplored regions in the current data landscape. Simulation environments are evaluated<br>for their effectiveness in generating large-scale data, as well as their ability to facilitate transfer<br>from simulation to real-world settings and the variety of supported tasks. Using both academic<br>and industrial contributions, we recognize ongoing challenges and outline strategic directions such<br>as scalable pretraining protocols, modular architectural design, and robust multimodal alignment<br>strategies. This review serves as both a technical reference and a conceptual roadmap for advancing<br>embodiment and robotic control, providing insights that span from dataset generation to real world<br>deployment of generalist robotic agents. For reference, a public repository summarizing VLA models,<br>datasets, and simulators can be found at:https://github.com/Muhayyuddin/VLAs|


|**Conten**|**ts**|**8**<br>**Challenges and Future Directions**<br>**21**|
|---|---|---|
|||8.1<br>Architectural Challenges . . . . . . . . . .<br>21|
|**1**<br>**Intr**|**oduction**|**1**<br>8.2<br>Dataset Challenges . . . . . . . . . . . . .<br>21|
|||8.3<br>Simulation Challenges<br>. . . . . . . . . . .<br>22|
|**2**<br>**Lite**|**rature Search and Selection Criteria**|**3**<br>8.4<br>Future Directions . . . . . . . . . . . . . .<br>22|
|**3**<br>**Back**|**ground Concepts**|**4**<br>**9**<br>**Conclusion**<br>**23**|
|3.1|Transformer . . . . . . . . . . . . . . . .|.<br>4|
|3.2|Vision Transformers<br>. . . . . . . . . . .|.<br>5<br>**1Itdti**|
|3.3|Large Language Models<br>. . . . . . . . .|.<br>5<br>**. nroucon**|
|3.4|Vision Language Models . . . . . . . . .|.<br>6<br>The integration of vision, language, and action into<br>a unified framework has emerged as a paradigm-shifting|
|**4**<br>**Visi**|**on Language Action Models**|**6**<br>approach in robotics and embodied artificial intelligence.|
|4.1|VLA Architecture . . . . . . . . . . . . .|.<br>6<br>Traditionally, robotic systems that depend on task-specific|
|4.2|State-of-the-Art VLA Models. . . . . . .|.<br>7<br>programming struggle in dynamic and unstructured envi-|
|4.3|Architectural Trends<br>. . . . . . . . . . .|.<br>7<br>ronments. In contrast, VLA models aim to utilize the gen-<br>eralization capabilities of large-scale foundation models to|
|**5**<br>**VLA**|**Training Datasets**|**14**<br>enable robotic systems that can understand instructions in|
|5.1|Dataset Format . . . . . . . . . . . . . .|.<br>14<br>natural language, perceive their surroundings, and perform|
|5.2|Major VLA Datasets<br>. . . . . . . . . . .|.<br>14<br>complex tasks autonomously (Brohan et al.,2022;Ahn et al.,|
|5.3|Benchamrk VLA Datasets<br>. . . . . . . .|.<br>16<br>2022;Jiang et al.,2022;Team et al.,2024). The fundamental|
|5.4|Benchmarking Analysis . . . . . . . . . .|.<br>17<br>concept of this paradigm is transformer architecture, which|
|**6**<br>**Sim**|**ulation Tools**|**17**<br>has transformed natural language processing and vision with<br>self-attention mechanisms and large-scale pretraining. Mod-|
|**7**<br>**App**<br>7.1<br>7.2|**lications and Evaluation of VLAs**<br>Application Domains . . . . . . . . . . . <br>VLA Model Selection and Evaluation<br>. .|**19**<br> .<br>19<br> .<br>19<br>els like GPT (Brown et al., 2020), BERT (Devlin et al.,<br>2018), ViT (Dosovitskiy et al., 2020), and CLIP (Radford<br>et al.,2021) demonstrate that massive datasets and parameter<br>scales can produce remarkable generalizability and robust-|
|∗corre<br>ORCI|sponding author: irfan.hussain@ku.ac.ae<br>D(s):|ness. These insights have led to new architectures that fuse<br>iidlibilliihih|


The integration of vision, language, and action into a unified framework has emerged as a paradigm-shifting approach in robotics and embodied artificial intelligence. Traditionally, robotic systems that depend on task-specific programming struggle in dynamic and unstructured environments. In contrast, VLA models aim to utilize the generalization capabilities of large-scale foundation models to enable robotic systems that can understand instructions in natural language, perceive their surroundings, and perform complex tasks autonomously (Brohan et al., 2022; Ahn et al., 2022; Jiang et al., 2022; Team et al., 2024). The fundamental concept of this paradigm is transformer architecture, which has transformed natural language processing and vision with self-attention mechanisms and large-scale pretraining. Models like GPT (Brown et al., 2020), BERT (Devlin et al., 2018), ViT (Dosovitskiy et al., 2020), and CLIP (Radford et al., 2021) demonstrate that massive datasets and parameter scales can produce remarkable generalizability and robustness. These insights have led to new architectures that fuse vision and language into robotics control policies, which step forward towards generalist agents such as RT-1 (Brohan 

Page 1 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 1:** VLA models, datasets, and contributing institutions from 2022 to 2025. The top row presents major VLA models introduced each year, alongside their associated institutions (logos within red boxes). The bottom row displays key datasets used to train and evaluate these models, grouped by release year. The figure highlights the increasing scale and diversity of datasets and institutional involvement, with contributions from academic (e.g., CMU, CNRS, UC, Peking Uni) and industrial labs (e.g., Google, NVIDIA, Microsoft). This timeline highlights the rapid advancements in VLA research. 

et al., 2022), SayCan (Ahn et al., 2022), VIMA (Jiang et al., 2022), and Octo (Team et al., 2024). The trend of developing such models is continuously growing as depicted in Fig 1. 

The development of effective VLA models is fundamentally dependent on the availability of large-scale, diverse, and multi-model datasets, together with realistic simulation platforms. These elements are essential for training models that can robustly understand language instructions, perceive visual environments, and generate meaningful action sequences. For instance, the _Open X-Embodiment_ (Collaboration et al., 2025) dataset unifies data from 22 robot embodiments and more than 500 tasks using a shared action space. It enables the pre-training of foundation models like RT-1-X, significantly enhancing cross-robot generalization. Similarly, the _DROID_ dataset (Khazatsky, 2024) uses internet-scale data, combining human-annotated language with robotic video demonstrations for scenes with complex manipulations. These datasets significantly advance the data ecosystem for training and benchmarking VLAs. Comprehensive datasets enable the learning of diverse tasks in both household and industrial contexts. These datasets offer rich annotations, including demonstration trajectories, object state transitions, and diverse natural language prompts. However, real-world data collection is labor-intensive, expensive, and limited in diversity, which highlights the importance of simulation. 

Simulation environments allow data generation to be scaled across a wide range of settings, object types, lighting conditions, and agent embodiments. Platforms such as _Habitat_ (Savva et al., 2019), _Isaac Gym_ (Makoviychuk et al., 2021), and _RoboSuite_ (Zhu et al., 2020) offer programmable and photorealistic environments with physics-based interactions, facilitating both imitation and reinforcement learning paradigms. More recently, tools such as _iGibson_ (Xia 

et al., 2020) and _AI2-THOR_ (Kolve et al., 2017) have added support for human-centric indoor environments with naturalistic object arrangements, enhancing semantic realism. Simulation also enables automatic generation of multimodal annotations, such as action trajectories, object states, and natural language instructions that are crucial to align visual, linguistic, and motor modalities. Recent efforts also emphasize the importance of synthetic language generation aligned with task semantics (e.g., VLN-CE (Krantz et al., 2020), ALFRED (Shridhar et al., 2020)) to ensure linguistic diversity and instruction complexity. The integration of simulation and large-scale synthetic datasets is therefore crucial for building VLA systems that are robust, scalable, and applicable to real-world deployment. 

Since the field matures at a rapid pace, numerous architectures, datasets, and frameworks are being proposed in a fast order. Despite the growing body of research, there remains a gap in the literature for a comprehensive and systematic synthesis that organizes and categorizes the architectural foundations, benchmark datasets, simulation platforms, and evaluation protocols that collectively shape the current VLA landscape. It is critically needed to contextualize the state-of-the-art and identify emerging patterns, limitations, and opportunities. This study will serve as both a technical reference and a conceptual roadmap to accelerate research in embodied foundation models and generalist robotic intelligence. 

**_Contributions:_** 

This systematic review makes the following key contributions to the field of VLA models in robotics: 

- _Structured taxonomy of VLA architectures:_ We present a detailed classification of VLA model architectures, organizing them into key categories according to their 

Page 2 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 2:** Overview of the skeleton of the paper, highlighting the main sections and their interrelated subtopics. 

distinct methods for integrating perception, natural language understanding, and embodied control. 

- _A novel quantitative benchmarking for VLA datasets:_ We introduce a novel quantitative framework designed to systematically benchmark VLA datasets, using metrics that are empirically adjusted for task complexity (task) and modality richness (mod). This benchmarking approach generates a two-dimensional graph (Fig. 10) that efficiently represents current datasets, allowing us to pinpoint significant gaps, particularly the lack of datasets that combine very high levels of task complexity with comprehensive multimodelities. 

- _In-depth review of simulation platforms:_ We review the most critical simulation platforms used in VLA research, focusing on their distinct sensory modalities, applications and their essential role in facilitating large-scale and reproducible VLA experiments and data generation. 

- _Identification of challenges and future roadmap:_ We identify persistent challenges facing VLA model development and articulate a clear roadmap for future research directions, emphasizing key areas such as architectural modularity, scalable data generation strategies, advancing dynamic simulation through differentiable contact modeling, and unified languagegrounding APIs to enable robust and scalable realworld deployment. 

The rest of the paper is organized as illustrated in Fig. 2. Sec. 2 outlines the literature search and selection criteria used to collect the most relevant and representative VLA systems. Sec. 3 introduces core background concepts including 

transformers, vision transformers, large-language models, and vision-language models, which collectively form the foundation of modern VLA architectures. Sec. 4 presents an in-depth review of VLA model architectures, highlights state-of-the-art systems, and identifies common architectural trends. Sec. 5 lists and analyzes the main training datasets, discussing dataset formats, benchmarking protocols, and evaluation metrics. Sec. 6 reviews the simulation platforms and tools used for training and testing VLA agents. Sec. 7 outlines practical application domains, describes the criteria used for selecting representative VLA models for comparison, and details evaluation protocols and key findings. Sec. 8 discusses key challenges and future directions, categorizing them into architectural, dataset, and simulation challenges, and outlines open problems and opportunities for future research. Finally, Sec. 9 summarizes the conclusions and offers a roadmap for advancing VLA-driven robotic autonomy. 

# **2. Literature Search and Selection Criteria** 

We conducted an extensive search through IEEE Xplore, Elsevier, Springer Nature, MDPI, Wiley, and arXiv to identify work on VLA models, VLA datasets, and simulation tools for robotic simulation and data generation. To capture each aspect, we developed sets of keywords; for _VLA models_ : "vision language action" OR VLA OR (vision AND language AND action) OR Vision Language Models for Robotic manipulation" "Multimodal Robotic Control", "Vision-Language Grounding", "Visuomotor Transformer", "End-to-End Robot Learning". The keywords for _Training datasets_ are "VLA dataset" OR "manipulation dataset" OR "embodied AI dataset for manipulation". Finally for _Simulation tools_ : "simulator for robotic manipulation" OR "embodied AI data-generation simulator" OR "robotic manipulation simulator" OR "realistic dynamic simulation for robotic manipulation" We applied the following inclusion criteria to identify original research: 1) Proposes or evaluates a VLA model, a VLA dataset, or a simulator for robotic manipulation or manipulation data generation. 2) Presents a novel model, dataset, or a new simulator. 

To ensure comprehensive coverage, we complement traditional database searches with conversational queries in a large-language model (e.g. GPT), using targeted prompts per thematic area. For _VLA models_ , we asked GPT to "List vision-language-action models published between 2022 and 2025," "List end-to-end transformer-based VLA architectures", "List VLA methods that use diffusion-based action decoders", "List modular fusion framework VLA models". For datasets, prompts included "List of VLA datasets released between 2022 and 2025", "List manipulation datasets used for VLM training" and "List embodied AI datasets for robotics" and "List of well-known manipulation datasets". For simulation tools, we queried "List simulators for robotic manipulation data generation," "List simulation environments for embodied AI dataset creation," "List robotic manipulation dataset generation simulators" and "List robotic dynamic simulators". We then merged these lists with our 

Page 3 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 3:** Annual VLA models and foundational VLA datasets count from 2022 to 2025. Green bars indicate the number of new VLA model introduced each year, while purple bars represent the number of novel dataset releases. The data illustrate a rapid acceleration in model development, particularly in 2025, alongside steady growth in dataset creation to support training and evaluation of these models. 

database results, removed duplicates, and performed manual validation to arrive at the final set of models, datasets, and simulators included in this review. 

We also included arXiv e-prints (https://arxiv.org/) in our search because the field of VLAs has recently begun to mature, and most breakthroughs and novel architectures have appeared as preprints in recent times. Fig. 3 shows the VLA (in green) and dataset (in purple) counts per year used in this work. We thoroughly examined the preprints and included only those that make substantial contributions to the field. The integration of preprints ensures that we capture the very latest models, datasets, and simulation tools as soon as they emerge, giving a more accurate and up-todate picture of this rapidly evolving field. 

# **3. Background Concepts** 

This section outlines the core architectures behind VLA models. We start with the transformer, a model that has transformed both language and vision tasks. We then cover Vision Transformers (ViTs), which apply self-attention to image patches for visual feature extraction. The subsequent category comprises Large Language Models (LLMs), which are transformer-based models trained on large text datasets that perform reasoning, instruction following, and zeroshot tasks. Finally, we will provide an overview of vision language models (VLMs), which fuse visual and textual data through cross-modal attention to ground instructions in robotic actions. These components form the backbone of modern VLA architectures, detailed in the following subsections. 

## **3.1. Transformer** 

Transformers are a class of deep learning architectures introduced by Vaswani et al. (Vaswani et al., 2017), these models have revolutionized the fields of natural language processing and computer vision by enabling greater parallelization and scalability in sequence modeling, i.e. in the processing and learning of patterns from sequences of data. 

The core of Transformers lie in the _self-attention mechanism_ , detailed below, which let each token in a sequence weigh and combine information from all other tokens to build a contextaware representation. 

The Transformer architecture (depicted in Fig 4) comprises three differentiated parts: the embedding layer, the encoder stack, and the decoder stack, which includes the final output projection and softmax layer. They are detailed in the following subsections, after presenting the _self-attention mechanism_ . 

### **_3.1.1. Self-Attention_** 

The self-attention mechanism allows each token in a sequence to attend to all other tokens when computing its representation. To achieve this, the model first transforms each input token into three distinct vector representations: queries ( _𝑄_ ), keys ( _𝐾_ ), and values ( _𝑉_ ). These vectors are obtained through learned linear projections of the input embeddings and serve different roles in the attention computation: the _query_ represents what the current token is looking for, the _key_ indicates what information each token provides, and the _value_ contains the actual content to be shared. By comparing queries to keys, the model determines attention weights, which are then used to aggregate the values into a new context-aware representation for each token. 

This process is formalized by the _scaled dot-product attention_ mechanism, which computes the dot <u>product</u> between queries and keys, scales the result by ~~√~~ _𝑑𝑘_ (where _𝑑𝑘_ is the dimension of the keys), applies a softmax function to obtain attention weights, and finally combines these weights with the values to produce the output: _<u>𝑄𝐾</u>_<sup>_⊤_</sup> Attention( _𝑄, 𝐾, 𝑉_ ) = softmax _𝑉_ (1) ( ~~√~~ _𝑑𝑘_ ) 

Building upon this mechanism, _multi-head attention_ extends the model’s capacity by enabling it to attend to information from multiple representation subspaces simultaneously. Instead of computing attention once with a single set of projection matrices, the model uses _ℎ_ parallel attention layers, or _heads_ , each with its own learned weight matrices _𝑊𝑖_<sup>_𝑄_,</sup> _𝑊𝑖_<sup>_𝐾_,and</sup><sup>_𝑊_</sup> _𝑖_<sup>_𝑉_.Thesematricesindependentlyprojectthe</sup> input into _ℎ_ different subspaces, allowing each head to focus on different aspects of the input relationships: 


The outputs from all heads are concatenated and passed through a final linear projection using _𝑊_<sup>_𝑂_</sup> to produce the result of the multi-head attention module. 

### **_3.1.2. Embeddings_** 

Embedding refers to continuous vector representations that map discrete inputs such as words, image patches, or action tokens into a dense latent space. In Transformer architectures, embeddings serve as the foundational interface between symbolic input (for example, textual instructions) and differentiable computation. Input embeddings enable the 

Page 4 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 4:** An overview of the Transformer architecture highlighting the encoder-decoder structure and the internal mechanism of multi-head attention. The encoder processes input embeddings through layers of multi-head attention, normalization, and feedforward networks. The decoder mirrors this with additional masked attention layers and incorporates encoder outputs for contextual decoding. The magnified view illustrates the scaled dot-product attention and how multiple attention heads are concatenated and linearly transformed to form the final multi-head attention output. The image is adapted from (Vaswani et al., 2017) 

model to process structured data in a unified format, while output embeddings decode latent representations into action or token spaces. Since the Transformer architecture lacks recurrence, a set of sinusoidal positional encodings is added to the input embeddings to provide information about the order of elements in a sequence. These learned representations capture semantic, spatial, or temporal relationships that are essential for generalization and reasoning in multimodal tasks (Vaswani et al., 2017; Dosovitskiy et al., 2021; Press and Wolf, 2017). 

### **_3.1.3. Encoder_** 

The encoder stack consists of _𝑁_ identical layers, where each layer has a multi-head self-attention mechanism followed by a position-wise feedforward network. Both sublayers are equipped with residual connections (which add the input of a sub-layer to its output to help preserve information and ease optimization) and layer normalization (which normalizes activations to improve training stability). In the first layer, the input embeddings provide the queries, keys, and values. In deeper layers, these are derived from the output of the preceding layer. 


**Figure 5:** Architecture of the ViT. The input image is divided into fixed-size non-overlapping patches which are flattened and linearly projected into embedding vectors. A learnable classification (CLS) token is prepended to the sequence of patch embeddings (shown in darker blue). Positional embeddings are added to retain spatial information before feeding the sequence into a standard Transformer encoder. The output of the CLS token is passed through an MLP head to produce the final class prediction. The image is adpated from (Dosovitskiy et al., 2021) 

### **_3.1.4. Decoder_** 

The decoder stack also consists of _𝑀_ identical layers, but with a slightly different architecture. Each layer contains three sub-layers: a masked multi-head self-attention layer, a multi-head encoder-decoder attention layer, and a feedforward network. The masked self-attention prevents a position from attending to subsequent tokens, ensuring that the model generates output in an autoregressive manner. The encoderdecoder attention enables the decoder to query the encoder’s outputs, integrating source information into the generation process. Like the encoder, each sub-layer in the decoder is followed by residual connections and layer normalization. 

The final output of the decoder is passed through a linear transformation and a softmax function to produce a probability distribution over all possible output tokens, enabling the model to predict the next token in the target sequence one step at a time. 

## **3.2. Vision Transformers** 

The Vision Transformer extends the Transformer architecture to visual domains by treating image patches as input tokens (Dosovitskiy et al., 2020). As shown in Fig 5, an image is split into a sequence of non-overlapping patches, each of which is linearly projected into a fixed-dimensional embedding. These embeddings are then augmented with learnable positional encodings and passed through a standard Transformer encoder. A classification token is appended, and its final representation is used for prediction through a multi-layer perceptron head (MLP). ViTs achieve competitive performance on benchmarks like ImageNet (Deng et al., 2009), highlighting the power of attention in learning global visual representations. 

## **3.3. Large Language Models** 

LLMs are transformer architectures (Fig. 4) trained on large-scale text data. These models are typically classified 

Page 5 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 6:** Architecture of a VLM for image captioning and semantic understanding. Visual input is processed by a visual encoder to extract patch-based embeddings. In parallel, a text prompt (e.g., "Describe the image") is tokenized and embedded. These embeddings are fused and jointly processed through a Transformer-based encoder-decoder architecture. The model outputs a natural language caption that describes the semantic content of the image, enabling tasks such as captioning, question answering, and visual grounding. the image is adapted from (Xiao et al., 2024) 

into three architectural types: _encoder-only_ , _decoder-only_ , and _encoder-decoder_ . Each structure is optimized for different types of task in natural language processing and robotics applications. 

_Encoder-only_ models, such as BERT, RoBERTa, and DeBERTa, utilize bidirectional self-attention mechanisms to learn deep contextual relationships from both the left and right of a token (Ghojogh et al., 2024; Zayyanu et al., 2024). These models are trained using masked language modeling (MLM) objectives and are well-suited for text classification, semantic similarity, and question answering. Their strength lies in representing sentence-level meaning rather than in generating sequential text. 

_Decoder-only_ models, such as GPT-3, GPT-4, PaLM, and LLaMA, operate sequentially by predicting the next token in a sequence based only on previous tokens (Ghojogh et al., 2024). This unidirectional architecture is optimized for text generation, dialogue, summarization, and other openended generative tasks. 

_Encoder-decoder_ models, also known as sequence-tosequence architectures, such as T5, BART, and the original Transformer, include an encoder to represent the input and a decoder to produce the output (Liu et al., 2021; Brandišauskas et al., 2023; Ghojogh et al., 2024). These are ideal for tasks where full input processing is required before output generation, including machine translation, summarization, and code generation. Recent applications in robotics also use encoder-decoder models for instruction grounding and language-conditioned action planning. 

## **3.4. Vision Language Models** 

VLMs use the synergy between computer vision and natural language processing to perform tasks such as image captioning, visual question answering, cross-modal retrieval, and instruction grounding. Like LLMs, they are built on the 

Transformer architecture, using either dual encoders (e.g., CLIP), unified encoder-decoder frameworks (e.g., BLIP, Flamingo), or sequence-to-sequence stacks. During training, they typically align visual and textual inputs using objectives such as contrastive learning (matching image-text pairs), masked modeling (predicting masked tokens or regions), or learning to generate captions from images. 

Fig. 6 illustrates a typical VLM designed for image captioning using a transformer-based encoder-decoder architecture. The process begins with an input image, which is divided into patches and embedded via a _visual encoder_ , such as a (ViT) (Mishra et al., 2024; Lam et al., 2023). A language prompt, e.g., "Describe the image", is also tokenized and embedded, either directly or via lightweight text guidance. The visual tokens and prompt embeddings are passed through a _Transformer encoder-decoder_ stack. The encoder captures spatial and semantic relationships from the image, while the decoder generates output tokens autoregressively. This allows the model to produce a fluent and contextually accurate caption, as shown in Fig. 6. This architecture enables semantic-level reasoning over visual input and has shown strong performance on benchmark datasets such as Flickr8k and Flickr30k (Mishra et al., 2024; Abdel-Hamid et al., 2024). 

Recent studies have demonstrated improved caption quality through the use of advanced modules or architectural variants within the encoder-decoder stack, such as Swin Transformers, T5-based decoders, or GPT-based language models, depending on the design (Lam et al., 2023; Mishra et al., 2024; Fouad et al., 2024). These approaches are widely used in robotic perception systems where visual scene understanding must be paired with natural language generation or instruction. 

# **4. Vision Language Action Models** 

VLA models represent a new frontier in robotic intelligence, enabling robots to perceive visual environments, understand natural language instructions, and execute grounded actions accordingly. These models bridge the semantic gap between multimodal inputs, such as images, sensor data, human commands, and low-level robotic control. VLA architectures are particularly relevant for unstructured and dynamic environments, where traditional rule-based programming is infeasible. They empower robots to generalize tasks such as object manipulation, navigation, and interaction by using deep learning, representation alignment, and sequential decision making (Wang et al., 2024a; Guruprasad et al., 2024; Wang et al., 2024d). 

## **4.1. VLA Architecture** 

The VLA architecture illustrated in Fig. 7 represents an end-to-end framework that is a representative of the leading VLA systems such as; RT-2 (Zitkovich et al., 2023), OpenVLA (Driess et al., 2024), CLIP-RT (Kang et al., 2025), Octo (Team et al., 2024), and RT-1 (Brohan et al., 2022), all of which employ transformer-based vision and language backbones fused through cross-modal attention. 

Page 6 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 7:** Architecture of a VLA system for robotic manipulation. The model processes three inputs: an image of the scene, a natural language instruction, and the robot’s internal state. These are encoded respectively through visual, text, and state encoders. The resulting embeddings are passed to an LLM that fuses multimodal information and generates a semantic representation of the intended task. This representation, along with robot state features, is processed by an Action Decoder implemented as a diffusion transformer to generate a trajectory that accomplishes the commanded task. 

The architecture unifies three parallel encoder streams: visual, linguistic, and proprioceptive, into a single transmission diffusion backbone that directly generates control commands. First, a transformer-based _Visual Encoder_ (e.g. ViT (Dosovitskiy et al., 2020), DINOv2 (Caron et al., 2021)) processes raw RGB (depth/semantic) images of the workspace and produces a sequence of fixed-length feature tokens. In parallel, a pre-trained _Language Encoder_ (for example, PaLM (Chowdhery et al., 2022) or LLaMA (Touvron et al., 2023)) tokenizes and embeds natural language instructions, whether high-level goals (e.g., "Put bowl, apple, and banana on plate.") or detailed stepwise instructions, in the same _𝑑_ -dimensional space. Similarly, _State Encoder_ embeds the proprioceptive and kinematic state of the robot (joint angles, pose of the end effector, gripper status) through an MLP or small transformer into additional tokens, allowing the model to reason about reachability, collision avoidance, and feedback correction. 

All tokens are concatenated and passed into a transformerbased model that produces _action embeddings_ . This model may implement either a diffusion policy, using a _Diffusion Transformer_ that iteratively denoises a noisy latent trajectory (e.g., as in Diffusion Policy (Chi et al., 2023a) or VLAFlow (Black et al., 2024b)), or a direct policy, which predicts the embeddings in a single pass without diffusion. At inference time, the action embeddings are converted into continuous control signals, such as end-effector velocities or joint torques, either through a lightweight output head or by completing the full diffusion sampling process. In some implementations, the embeddings can also be decoded into imagined next-frame images, enabling an "imagineand-verify" loop for closed-loop execution. 

Models such as OpenVLA and Octo further incorporate proprioceptive tokens, while several systems (e.g., PerAct (Shridhar et al., 2022b), Helix (Team, 2025a)) support real-time feedback loops for continual correction. The rapid 

evolution and plug-and-play modularity of these architectures, where one can swap in a stronger ViT, a larger language model, or a more expressive diffusion sampler are driving to a new direction of instruction-driven autonomy for generalist robotic systems. 

## **4.2. State-of-the-Art VLA Models** 

Table 1 is organized to provide a brief yet thorough overview of over a hundred VLA models related to robotic manipulation and instruction-driven autonomy. The first two columns detail the name and year of publication of each model. The next two columns _End-to-End_ and _Component Focused_ flag whether a model learns a direct mapping from raw visual and language input to control commands or instead concentrates on developing individual building blocks (for example, a better vision backbone or a more effective action sampler). The _Main Contributions_ column then summarizes each work’s core innovation, whether it introduced a novel fusion architecture, demonstrated a new training paradigm, or achieved state-of-the-art performance on a benchmark. 

Each VLA model is based on four essential components: the training dataset, which provides foundational real-world task demonstrations or simulated episodes; the vision encoder, responsible for converting raw images or depth data into detailed feature maps; the language encoder, which maps instructions or annotations into a shared latent space; and the action decoder, which integrates these multimodal embeddings to produce the actual robot instructions, whether they are joint trajectories, discrete tokens, or overarching motion primitives. In Table 1, the final column specifies which dataset each model was trained on, which vision backbone it uses (e.g. CLIP-ViT, ResNet, EfficientNet), which text encoder it employs (e.g. T5, LLaMA, CLIP text), and what kind of action decoder it relies upon (e.g. Transformer head, diffusion policy, CVAE sampler), making it straightforward to compare how different architectures assemble these building blocks. 

## **4.3. Architectural Trends** 

Fig. 8 presents a comprehensive taxonomy of VLA model components, structured around three interconnected modules: vision encoders, language encoders, and action decoders. Within the vision encoder family, several prominent approaches exist. CLIP and SigLIP-based encoders are popular for their strong visual-text alignment through contrastive learning and are utilized in models such as CLIPort, RevLA, and Edge VLA. Other ViT variants such as DINOv2 and Qwen2 VIT, are used in models like Gato, Octo, HybridVLA, and Chain-of-Affordance for their ability to model long-range spatial dependencies and high-level visual semantics. CNN-based encoders such as ResNet and EfficientNet appear in models like CLIPort, ACT, RT-1, and QUAR-VLA. 

Page 7 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

Table 1: Comprehensive survey of VLA models developed for robotic manipulation and instruction-driven autonomy. The table lists each model’s name, publication year, indicates whether it operates in an end-to-end fashion (mapping raw visual and language inputs directly to actions) or focuses on individual components (vision, language, or action modules), and summarizes its main technical contributions. The final column details the primary training datasets and core model components-including vision encoders, language encoders, and action decoders used by each method. 

|**Model Name**|**End-to-**<br>**End**|**Componen**<br>**Focused**|**t**<br>**Main Contributions**|**Training Dataset and Model Components**|
|---|---|---|---|---|
|CLIPort (Shrid-<br>har et al.,2022a)|✔|✔|Pioneered the semantic grounding of visuomotor<br>policies by integrating CLIP features into dense<br>transport maps for precise pick-and-place.|Dataset: Self-collected visuomotor demos; Vision Encoder: CLIP-<br>ResNet50 + Transporter-ResNet; Language Encoder: CLIP text en-<br>coder; Action Decoder: LingUNet|
|RT-1<br>(Brohan<br>et al.,2022)|✔|✔|Introduced a discretized action transformer for<br>scalable multi-task kitchen manipulation.|Dataset: Self-collected RT-1-Kitchen; Vision Encoder: EfficientNet<br>CNN; Language Encoder: Universal Sentence Encoder; Action De-<br>coder: Discretized action transformer head|
|Gato (Reed et al.,<br>2022)|✔|✔|Demonstrated a unified tokenization scheme<br>across vision, language, and control tasks,<br>achieving zero-shot transfer across domains.|Dataset: Self-collected multi-domain tasks; Vision Encoder: custom<br>ViT; Language Encoder: Sentence Piece tokenizer; Action Decoder:<br>Autoregressive Transformer|
|VIMA<br>(Jiang<br>et al.,2022)|✔|✔|Handled six distinct vision-language grounding<br>tasks via a prompt-based multimodal policy.|Dataset: VIMA self-collected; Vision Encoder: Mask R-CNN; Lan-<br>guage Encoder: T5-base; Action Decoder: Transformer policy head|
|PerAct (Shridhar<br>et al.,2023)|✔|✘|Uses voxel-based representation with language<br>conditioning for high-precision manipulation;<br>operates directly on point cloud voxels.|Dataset: RLBench; Vision Encoder: Perceiver Transformer + voxel<br>grid encoder; Language Encoder: CLIP text encoder; Action De-<br>coder: Transformer voxel policy head|
|SayCan<br>(Ahn<br>et al.,2022)|✘|✔|Combines language model planning with value<br>function grounding in the real world; interprets<br>high-level goals into executable robot actions.|Dataset: Self-collected everyday manipulation demos; Vision En-<br>coder: none; Language Encoder: PaLM; Action Decoder: Value-<br>conditioned execution module|
|RoboAgent<br>(Bharadhwaj<br>et al.,2023)|✔|✘|MT-ACT: multi-task transformer policy with<br>semantically augmented CVAE encoding and<br>action-chunking for strong real-world general-<br>ization.|Dataset: RoboSet teleop demos; Vision Encoder: Multi-view CNN<br>encoder; Language Encoder: Semantic transformer encoder; Action<br>Decoder: CVAE + Chunked trajectory predictor|
|RT-Trajectory<br>(Gu et al.,2023)|✔|✘|Conditioned policies on user-sketched trajecto-<br>ries to improve generalization to novel layouts<br>and paths.|Dataset: RT-1 dataset; Vision Encoder: EfficientNet-B3; Language<br>Encoder: None; Action Decoder: Sketch-conditioned behavioral<br>cloning policy|
|ACT (Zhao et al.,<br>2023)|✔|✔|Applied temporal ensembling to achieve smooth<br>bimanual manipulation with 0.1 mm precision.|Dataset: self-collected demos on ALOHA; Vision Encoder: ResNet-<br>18; Language Encoder: none ; Action Decoder: CVAE-Transformer<br>head|
|RT-2 (Zitkovich<br>et al.,2023)|✔|✔|First large VLA co-finetuned on Internet VQA<br>and robot data, unlocking emergent multi-robot<br>zero-shot capabilities.|Dataset: Internet VQA + RT-1-Kitchen; Vision Encoder: PaLI-<br>X/PaLM-E ViT; Language Encoder: PaLI-X/PaLM-E text encoder;<br>Action Decoder: Symbol-tuning transformer|
|VoxPoser<br>(Huang<br>et<br>al.,<br>2023)|✔|✔|Achieved zero-shot constraint-aware motion<br>planning by composing a frozen VLM and LLM<br>without additional training.|Dataset: Self-collected motion demos+RLBench; Vision Encoder:<br>OWL-ViT; Language Encoder: GPT-4; Action Decoder: MPC op-<br>timizer|
|CLIP-RT (Kang<br>et al.,2024)|✘|✔|Contrastive policy using CLIP vision and text<br>encoders to select language-based motion primi-<br>tives, enabling fast learning and robust zero-shot<br>transfer for table-top manipulation.|Dataset: OXE; Vision Encoder: CLIP image encoder (ViT-H-14);<br>Language Encoder: CLIP text encoder; Action Decoder: Cosine<br>similarity head over text-embedded motion primitives.|
|Diffusion Policy<br>(Chi<br>et<br>al.,<br>2023a)|✔|✔|Introduced diffusion-based policy modeling for<br>multimodal visuomotor action distributions.|Dataset: Self-collected demos; Vision Encoder: ResNet-18; Lan-<br>guage Encoder: None; Action Decoder: diffusion policy network|
|Octo<br>(Team<br>et al.,2024)|✔|✔|First generalist diffusion policy trained on 4 M+<br>trajectories across 22 robot platforms, demon-<br>strating broad transfer.|Dataset: Open X-Embodiment; Vision Encoder: CNN encoder ;<br>Language Encoder: T5-base; Action Decoder: Diffusion Transformer<br>head|
|VLATest (Wang<br>et al.,2024c)|✘|✔|Automated framework for large-scale VLA<br>model testing, revealing robustness gaps and<br>guiding improvements in manipulation.|Dataset: none ; Vision Encoder: that used in (e.g., OpenVLA,RT-<br>1,Octo); Language Encoder: that used in (e.g., OpenVLA,RT-<br>1,Octo); Action Decoder: that used in (e.g., OpenVLA,RT-1,Octo)|
|NaVILA (Cheng<br>et al.,2024)|✔|✘|Hierarchical planning yields 88% real-world<br>navigation<br>success<br>for<br>legged<br>robots<br>via<br>language-conditioned topological control.|Dataset: Self-collected Real-world legged robot demos; Vision En-<br>coder: VILA Vision Encoder ; Language Encoder: VILA LLM;<br>Action Decoder: Topological graph planner + RL policy for joint<br>commands|
|RoboNurse-<br>VLA (Li et al.,<br>2024c)|✔|✘|Real-time voice-to-action pipeline for surgical<br>instrument handover, robust to unseen tools in<br>dynamic scenes.|Dataset: Self-collected Surgical handover videos + voice prompts;<br>Vision Encoder: SAM2 ; Language Encoder: LLaMA-2; Action<br>Decoder: token-based action decoder|
|Mobility<br>VLA|✔|✘|Multimodal instruction navigation with topolog-|Dataset: MINT instruction tours; Vision Encoder: Gemini 1.5 Pro|
|(Chiang<br>et<br>al.,<br>2024)|||ical mapping for robust long-range mobility.|based (ViT); Language Encoder: Gemini 1.5 Pro based text encoder;<br>Action Decoder: Topological graph-based planner|
|RevLA<br>(Dey<br>et al.,2024)|✔|✘|Domain adaptation adapters to improve the gen-<br>eralization of robotic foundation models across<br>visual domains.|Dataset: Open X-Embodiment (OXE); Vision Encoder: DINO-v2<br>+ SigLIP; Language Encoder: LLama-7B; Action Decoder: Llama<br>head, outputs 7 discrete action tokens|


_<mark>continue</mark>_ 

Page 8 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

|**Model Name**|**End-to-**<br>**End**|**Compone**<br>**Focused**|**nt**<br>**Main Contribution**|**Training Dataset and Model Components**|
|---|---|---|---|---|
|Uni-NaVid<br>(Zhang<br>et<br>al.,<br>2024b)|✔|✘|Video-based VLA unifying embodied naviga-<br>tion tasks across multiple benchmarks.|Dataset: Room-to-Room (R2R) + REVERIE; Vision Encoder: EVA-<br>CLIP; Language Encoder: Vicuna-7B; Action Decoder: Vicuna-7B<br>head (4 discrete action tokens)|
|RDT-1B<br>(Liu<br>et al.,2024b)|✔|✔|1.2B-parameter diffusion foundation model ex-<br>celling at bimanual manipulation and zero-shot<br>generalization.|Dataset: self-collected 6K ALOHA episodes; Vision Encoder:<br>SigLIP ; Language Encoder: T5-XXL ; Action Decoder: Diffusion<br>Transformer + MLP decoder|
|RoboMamba<br>(Liu<br>et<br>al.,<br>2024a)|✔|✘|Mamba-based unified VLA with linear-time in-<br>ference for real-time robotic reasoning.|Dataset: SAPIEN sim benchmarks + real-world demos; Vision En-<br>coder: Mamba VLM visual backbone; Language Encoder: Mamba<br>VLM text backbone; Action Decoder: MLP policy head for SE(3)<br>pose predicting|
|Chain-of-<br>Affordance<br>(Li<br>et al.,2024a)|✘|✔|Sequential affordance reasoning for spatial plan-<br>ning, achieving SOTA on LIBERO dataset.|Dataset: LIBERO + real/sim manipulation tasks; Vision Encoder:<br>Qwen2-VL; Language Encoder: Qwen2-VL; Action Decoder: Dif-<br>fusion policy head|
|Edge<br>VLA<br>(Budzianowski<br>et al.,2024)|✔|✔|Lightweight, edge-optimized VLA for low-<br>power real-time inference.|Dataset: OXE + Bridge robotics set; Vision Encoder: SigLIP<br>+ DINOV2; Language Encoder: Qwen2; Action Decoder: Non-<br>autoregressive control head|
|OpenVLA (Kim<br>et al.,2024)|✔|✔|LORA-fine-tuned open-source VLA achieving<br>efficient transfer and high success.|Dataset: OXE + DROID robot data; Vision Encoder: DINOv2 +<br>SigLIP; Language Encoder: Llama 2; Action Decoder: Llama 2<br>output head (predicts discretized action tokens as output)|
|CogACT<br>(Li<br>et al.,2024b)|✔|✔|Componentized diffusion action transformer,<br>+59.1% success over OpenVLA with specialized<br>adaptation.|<br>Dataset: OXE subset + real trials; Vision Encoder: DINOv2 +<br>SigLIP; Language Encoder: LLaMA-2; Action Decoder: Diffusion<br>Transformer head|
|ShowUI-2B (Lin<br>et al.,2024)|✔|✔|GUI/web navigation via screenshot grounding<br>and efficient token selection.|Dataset: 256 K GUI instruction demos; Vision Encoder: Qwen2-VL-<br>2B ViT; Language Encoder: Qwen2-VL-2B LLM; Action Decoder:<br>Qwen2-VL-2B output head (GUI actions as tokens)|
|Pi-0 (Black et al.,<br>2024a)|✔|✘|General robot control flow model for high-<br>frequency, open-world tasks.|<br>Dataset: Extended OXE called Pi-Cross-Embodiment; Vision<br>Encoder: PaliGemma (SigLIP); Language Encoder: PaliGemma<br>(Gemma-2B); Action Decoder: diffusion-based Flow matching ac-<br>tion expert head|
|HiRT<br>(Zhang<br>et al.,2024a)|✔|✔|Hierarchical planning/control separation, dou-<br>bling execution speed and improving dynamic<br>task success.|Dataset: Self collected Real-world data; Vision Encoder: Instruct-<br>BLIP; Language Encoder: LLaMA-2; Action Decoder: Latent-<br>conditioned policy head (MLP)|
|A3VLM (Huang<br>et al.,2024)|✘|✔|Learns articulation-aware affordance grounding<br>purely from RGB video, generalizing to unseen<br>object joints.|Dataset: PartNet-Mobility; Vision Encoder: CLIP, DINOv2, Q-<br>Former (fused); Language Encoder: LLaMA2; Action Decoder: Pa-<br>rameterized primitive motion generator|
|SVLR (Samson<br>et al.,2024)|✘|✔|Modular "segment-to-action" pipeline using vi-<br>sual prompt retrieval for on-device policy execu-<br>tion.|Dataset: Self-collected visual prompts; Vision Encoder: Mini In-<br>ternVL; Language Encoder: Phi-3mini4k; Action Decoder: Script-<br>based action binder|
|Bi-VLA<br>(Gbagbe et al.,<br>2024)|✘|✔|Dual-arm<br>instruction-to-action<br>planner<br>grounded in recipe demonstrations, achieving<br>83.4 % real-world task success.|Dataset: Visual-recipe demos; Vision Encoder: Qwen-VL; Language<br>Encoder: Starling-LM; Action Decoder: Python trajectory generator|
|QUAR-VLA<br>(Ding<br>et<br>al.,<br>2024)|✔|✘|Quadruped-specific VLA with adaptive gait and<br>body command mapping, strong sim-to-real<br>transfer.|Dataset: QUART locomotion + manipulation; Vision Encoder:<br>EfficientNet-B3; Language Encoder: FiLM / VLM tokenizer; Action<br>Decoder: Transformer decoder (discrete tokens)|
|3D-VLA<br>(Zhen<br>et al.,2024)|✔|✔|Integrates 3D generative diffusion heads for<br>world<br>reconstruction,<br>enabling<br>planning<br>in<br>RGB+D and point-cloud spaces.|Dataset: 3D-language-action pairs; Vision Encoder: 3D-aware trans-<br>former; Language Encoder: 3D-LLM; Action Decoder: Multi-head<br>diffusion planner|
|RoboMM<br>(Yan<br>et al.,2024)|✔|✔|<br>MIM-based multimodal decoder unifying 3D<br>perception and language for spatially aligned<br>policy fusion.|f<br>Dataset: RoboData (CALVIN, Meta-World); Vision Encoder: Multi-<br>view CLIP + occupancy network; Language Encoder: Flamingo-<br>style fusion module; Action Decoder: Multimodal MLP/attention<br>decoder|
|FAST<br>(Pertsch<br>et al.,2025)|✔|✔|Frequency-space action tokenization for up to 15<br>times faster inference on general robot control.|Dataset: DROID; Vision Encoder: PaliGemma (SigLIP); Language<br>Encoder: PaliGemma (Gemma-2B); Action Decoder: FAST token<br>generator|
|OpenVLA-OFT<br>(Kim<br>et<br>al.,<br>2025)|✔|✔|Optimized fine-tuning of OpenVLA with paral-<br>lel chunked decoding, achieving 97.1 % success<br>on LIBERO dataset and 26 time speed-up.|Dataset: LIBERO; Vision Encoder: SigLIP + DINOv2; Language<br>Encoder: LLaMA-27B; Action Decoder: Llama 2 Parallel chunking<br>head|
|CoVLA<br>(Arai<br>et al.,2025)|✔|✘|<br>VLA model for autonomous driving, trained on<br>richly annotated scene data for robust planning.|Dataset: Large-scale driving videos + annotations; Vision Encoder:<br>CLIP ViT; Language Encoder: LLaMA-2; Action Decoder: Trajec-<br>tory prediction module|
|ORION<br>(Fu<br>et al.,2025)|✔|✘|Holistic end-to-end driving VLA aligning se-<br>mantic understanding with generative trajectory<br>control.|<br>Dataset: E2E driving benchmark; Vision Encoder: EVA-02-L (Trans-<br>former); Language Encoder: Vicuna v1.5 (LoRA); Action Decoder:<br>Generative planner head|
|UAV-VLA<br>|✔|✘|Zero-shot aerial mission VLA combining satel-<br>|Dataset: Satellite + UAV flight logs; Vision Encoder: Molmo-7B-D<br>|
|(Sautenkov<br>et al.,2025)|||lite and UAV imagery for scalable instruction-<br>driven flight planning.|(CLIP); Language Encoder: GPT-3; Action Decoder: Transformer-<br>based path planner|


_<mark>continue</mark>_ 

Page 9 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

|**Model Name**|**End-to-**<br>**End**|**Componen**<br>**Focused**|**t**<br>**Main Contribution**|**Training Dataset and Model Components**|
|---|---|---|---|---|
|Combat<br>VLA<br>(Chen<br>et<br>al.,<br>2025a)|✔|✘|Ultra-fast tactical reasoning in 3D ARPG en-<br>vironments, achieving 50 times faster inference<br>and human-level success.|Dataset: 3D ARPG combat logs; Vision Encoder: Qwen2.5-VL-3B;<br>Language Encoder: Qwen2.5-VL-3B; Action Decoder: LLM-based<br>planner head|
|HybridVLA (Liu<br>et al.,2025)|✔|✘|Adaptive ensemble decoding that combines dif-<br>fusion and autoregressive policies for robust<br>multi-task generalization.|Dataset: RT-X trajectories + synthetic task fusion; Vision Encoder:<br>CLIP ViT + DINOV2; Language Encoder: LLaMA-2; Action De-<br>coder: Diffusion policy head|
|NORA<br>(Hung<br>et al.,2025)|✔|✘|<br>Low-overhead VLA with integrated visual rea-<br>soning and FAST token decoding for real-time<br>performance.|f<br>Dataset: OXE; Vision Encoder: Qwen-2.5-VL; Language Encoder:<br>Qwen-2.5-VL; Action Decoder: FAST tokenizer head|
|SpatialVLA (Qu<br>et al.,2025)|✔|✘|3D spatial encoding and adaptive action dis-<br>cretization to improve cross-robot manipulation<br>generality.|Dataset: OXE; Vision Encoder: SigLIP; Language Encoder:<br>PaliGemma (Gemma-2B); Action Decoder: Adaptive action grid<br>head|
|MoLe-VLA<br>(Zhang<br>et<br>al.,<br>2025e)|✔|✘|Selective layer activation in a multi-stage ViT<br>yields 5.6 time faster inference and +8% task<br>success.|Dataset: RLBench + real-world trials; Vision Encoder: DINOv2,<br>SigLIP; Language Encoder: LLaMA-2; Action Decoder: Diffusion<br>head|
|JARVIS-VLA<br>(Li et al.,2025b)|✔|✘|Open-world instruction following in 3D games<br>via keyboard/mouse action prediction.|Dataset: Minecraft gameplay demos; Vision Encoder: ViT (in<br>Llava-Next/Qwen2-VL); Language Encoder: Llava-Next/Qwen2-VL<br>(transformer LLMs); Action Decoder: Key/mouse control head|
|UP-VLA (Zhang<br>et al2025d)|✔|✘|Precise 3D spatial reasoning, achieving +33 %<br>success on the CALVIN benchmark|Dataset: CALVIN; Vision Encoder: CLIP-ViT; Language Encoder:<br>Phi-15 Action Decoder: MLP olic head|
|., <br>Shake-VLA|✔|✔|.<br>Modular bimanual VLA achieving 100% success|.;    py<br>Dataset: Cocktail mixing demos; Vision Encoder: YOLOv8, Easy-|
|(Khan<br>et<br>al.,<br>2025)|||<br>on cluttered cocktail-mixing tasks.|OCR; Language Encoder: GPT-4o,Whisper-1; Action Decoder: Bi-<br>manual arm controller|
|MORE<br>(Zhao<br>et al.,2025a)|✘|✘|Scalable Mixture of Expert (MoE) enhanced RL<br>framework for quadruped multi-task learning.|Dataset: Quadruped navigation/manipulation demos; Vision En-<br>coder: CLIP-like; Language Encoder: Fuyu 8B ; Action Decoder:<br>Mixture-of-Experts + LoRA adapter|
|DexGraspVLA<br>(Zhong<br>et<br>al.,<br>2025)|✔|✘|Diffusion-based dexterous grasping with≥90%<br>zero-shot success across diverse objects.|<br>Dataset: Self-collected Dexterous grasp data; Vision Encoder: DI-<br>NOv2; Language Encoder: Qwen-VL, Qwen2.5-VL; Action De-<br>coder: Diffusion policy head|
|DexVLA<br>(Wen<br>et al.,2025)|✔|✘|Cross-embodiment diffusion expert enabling<br>rapid adaptation without per-task tuning.|Dataset: OXE, RLBench; Vision Encoder: Qwen2-VL (ViT),<br>ResNet-50; Language Encoder:Qwen2-VL,DistilBERT; Action De-<br>coder: Diffusion Transformer head|
|Humanoid-VLA<br>(Ding<br>et<br>al.,<br>2025)|✔|✘|Hierarchical VLA for full-body humanoid con-<br>trol, integrating perception and latent action<br>planning.|f<br>Dataset: Self-collected humanoid robot episodes; Vision Encoder:<br>Video Visual Encoder,Cross-Attention; Language Encoder: Llama3-<br>70B; Action Decoder: Token-based Motion Decoder + RL Whole-<br>Body Ctrlr|
|ObjectVLA<br>(Zhu<br>et<br>al.,<br>2025a)|✔|✘|End-to-end<br>open-world<br>object<br>manipulation<br>without task-specific data.|<br>Dataset: RoboSpatial manipulation episodes; Vision Encoder: Di-<br>noX, DiVLA VLM; Language Encoder: DiVLA (LLM backbone);<br>Action Decoder: Object-centric diffusion controller head|
|Gemini Robotics<br>(Team,2025b)|✔|✔|General-purpose VLA built on the Gemini<br>2.0 foundation, enabling long-horizon dexterous<br>manipulation across diverse robot embodiments<br>with zero-shot adaptability.|f<br>Dataset: Self-collected ALOHA2 demos + web-scale VL Dataset;<br>Vision Encoder: Gemini 2.0 vision component; Language Encoder:<br>Gemini 2.0 language component; Action Decoder: Local zero-shot<br>policy head|
|ECoT (Zawalski<br>et al.,2025)|✔|✔|<br>Embodied chain-of-thought planning for inter-<br>pretable, stepwise VLA control.|<br>Dataset: Bridge v2 ; Vision Encoder: SigLIP, DINOv2; Language En-<br>coder: LLaMA-2 7B; Action Decoder: Autoregressive VLA decoder<br>with CoT module|
|OTTER (Huang<br>et al.,2025a)|✔|✔|Zero-shot generalization via a frozen CLIP back-<br>bone and causal transformer action decoding.|Dataset: LIBERO; Vision Encoder: Frozen CLIP ViT; Language<br>Encoder: CLIP text encoder; Action Decoder: Causal transformer<br>delta-trajectory head|
|_𝜋_-0.5<br>(Black<br>et al.,2025)|✔|✔|Hierarchical VLA co-trained on real robot demos<br>and web-scale vision-language data for robust<br>household task generalization.|<br>Dataset: self-collected 400h robot teleop + web VL dataset; Vision<br>Encoder: SigLIP; Language Encoder: Gemma (2B/2.6B); Action<br>Decoder: Flow Matching Head|
|OneTwoVLA|✔|✔|<br>Unified reasoning-acting framework that dynam-|<br>Dataset:Self-collected16Kreasoning-augmentedrobotepisodes;|
|(Lin et al.,2025)|||i<br>ically toggles between planning and control via<br>decision tokens.|<br>Vision Encoder: same as pi-0 vla; Language Encoder:same as pi-0<br>vla; Action Decoder: Diffusion policy head|
|Helix<br>(Team,<br>2025a)|✔|✔|First 200 Hz VLA for full humanoid control<br>on embedded systems, enabling zero-shot task<br>transfer.|f<br>Dataset: self-collected 200Hz teleop + sim logs; Vision Encoder:<br>Pretrained VLM ; Language Encoder: Pretrained VLM ; Action<br>Decoder: Fast transformer policy|
|Gii Rbi|✔|✔|OdiiidifGiiVLA|<br>D Slflld ALOHA2  fh di d Vi|
|emn ootcs<br>|||n-evce optmze varant o emn ,<br>|ataset: e-coecte  + ew-sot aaptaton emos; -<br>|
|On-Device<br>(Parada<br>and<br>Team2025)|||delivering low-latency dual-arm and humanoid<br>control on embedded hardware.|sion Encoder: Gemini SDK vision module; Language Encoder: Gem-<br>ini SDK language module; Action Decoder: On-device optimized<br>policy head|
|, <br>OE-VLA (Zhao|✔|✔|Curriculum-tuned LLaVA backbone with inter-|<br>Dataset: CALVIN; Vision Encoder: SigLIP-400M ViT; Language|
|et al.,2025c)|||leaved multimodal prompting for improved gen-<br>eralization across vision-language-action tasks.|Encoder: Qwen-1.5 language module; Action Decoder: MLP token<br>generator|
|SmolVLA<br><br><br>|✔|✔|Ultra-lightweight VLA trained on community-<br>|Dataset: 22.9K community episodes; Vision Encoder: SigLIP (VLM-<br>|
|(Shukor<br>et<br>al.,<br>2025)|||contributed robot demonstrations, capable of<br>real-time inference on CPU.|2) visual backbone; Language Encoder: SmolVLM2 text backbone;<br>Action Decoder: Chunked flow-matching head|


_<mark>continue</mark>_ 

Page 10 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

|**Model Name**|**End-to-**<br>**End**|**Componen**<br>**Focused**|**t**<br>**Main Contribution**|**Training Dataset and Model Components**|
|---|---|---|---|---|
|EF-VLA<br>(authors,2025)|✔|✔|Early fusion of fine-grained CLIP visual tokens<br>into the language-action pipeline, boosting zero-<br>shot generalization.|Dataset: Self-collected real and simulated tasks; Vision Encoder:<br>Frozen CLIP ViT; Language Encoder: Frozen CLIP text encoder;<br>Action Decoder: causal transformer|
|PD-VLA<br>(Song<br>et al.,2025b)|✔|✘|First parallel decoding method with action<br>chunking for VLA, achieving a 2.52 times speed-<br>up without sacrificing control fidelity.|Dataset: Chunked trajectory demonstrations; Vision Encoder: CLIP-<br>ViT-Large-Patch14-336 (LLaVA); Language Encoder: Vicuna-7B-<br>v1.5 (LLaVA); Action Decoder: Fixed-point token predictor|
|LeVERB<br>(Xue<br>et al.,2025)|✔|✔|Dual-process latent VLA for whole-body hu-<br>manoid control, achieving 58.5 % success on<br>sim-to-real humanoid demos.|Dataset: sim-to-real humanoid demos; Vision Encoder: SigLIP ViT;<br>Language Encoder: SigLIP text encoder; Action Decoder: Latent<br>CVAE verb + transformer policy|
|TLA (Hao et al.,<br>2025)|✔|✔|First language-grounded tactile-action model for<br>high-precision contact tasks, with 85 % success<br>on peg-in-hole task.|Dataset: TLA Data; Vision Encoder: ViT (Qwen2-VL); Language<br>Encoder: Qwen2-VL; Action Decoder: MultimodalΔ_𝑥_∕Δ_𝑦_∕Δ_𝑧_pre-<br>dictor|
|Interleave-VLA<br>(Fan et al.,2025)|✔|✔|Model-agnostic wrapper enabling interleaved<br>image-text instruction processing..|Dataset: Interleave-VLA data; Vision Encoder: Any base VLM (e.g.,<br>OpenVLA); Language Encoder: Any LLM (e.g., Pi-0); Action De-<br>coder: Minimal interleaved-processing module|
|iRe-VLA<br>(Guo<br>et al.,2025)|✔|✔|Iterative RL and supervised fine-tuning pipeline<br>for robust control and rapid generalization across<br>embodiments.|Dataset: Franka-Kitchen, real Panda robot demos; Vision Encoder:<br>BLIP-2 (pre-trained VLM); Language Encoder: BLIP-2; Action De-<br>coder: MLP action head after token learner|
|TraceVLA<br>(Zheng<br>et<br>al.,<br>2025b)|✔|✔|Visual trace prompting to incorporate spatio-<br>temporal cues, boosting task success by 3.5 time<br>over OpenVLA.|Dataset: OXE + 150K trace-annotated demos; Vision Encoder: Phi-<br>3-Vision with trace overlay; Language Encoder: Phi-3 LLM; Action<br>Decoder: Quantized delta-motion tokens|
|OpenDrive VLA<br>(Zhu<br>et<br>al.,<br>2025b)|✔|✘|End-to-end driving VLA with semantic scene<br>alignment and temporal abstraction for robust<br>trajectory planning.|Dataset: Autonomous driving QA/planning benchmarks; Vision<br>Encoder: ResNet-101 + Query Transformers; Language Encoder:<br>Qwen2.5-Instruct (LLM); Action Decoder: Ego-vehicle action au-<br>toregressor|
|V-JEPA 2 (Ass-<br>ran et al.,2025)|✔|✘|Dual-stream self-supervised video JEPA en-<br>abling predictive planning in vision-language-<br>action tasks.|Dataset: Droid video data; Vision Encoder: ViT (self-supervised)<br>; Language Encoder: LLM for QA/alignment; Action Decoder:<br>Action-conditioned transformer predictor head|
|Knowledge<br>Insulating VLA<br>(Driess<br>et<br>al.,<br>2025)|✔|✘|Implements insulation layers between vision-<br>language and action modules, accelerating train-<br>ing and inference while maintaining generaliza-<br>tion.|Dataset: Multi-domain VL datasets; Vision Encoder: PaliGemma<br>(SigLIP); Language Encoder: PaliGemma (Gemma-2B) encoder;<br>Action Decoder: Diffusion Modular policy head|
|GR00T<br>N1<br>(Bjorck<br>et<br>al.,<br>2025)|✔|✘|Self-collected<br>Diffusion-based<br>foundation<br>model enabling unified humanoid control with<br>policy tokenization.|Dataset: Multi-modal humanoid demonstrations; Vision Encoder:<br>SigLIP-2 ViT (Eagle-2 VLM); Language Encoder: SmolLM2 (Eagle-<br>2 VLM); Action Decoder: Generative diffusion transformer based<br>planner|
|AgiBot<br>World<br>Colosseo<br>(Bu<br>et al.,2025)|✔|✘|Integrates multiple embodied datasets into a uni-<br>fied platform for scalable training and evaluation<br>of VLA models.|Dataset: AgiBot World Data; Vision Encoder: PaliGemma (SigLIP);<br>Language Encoder: PaliGemma (Gemma-2B); Action Decoder: La-<br>tent action planner + policy head|
|Hi<br>Robot<br>(Shi<br>et al.,2025)|✔|✘|Hierarchical separation of planning and control<br>for open-ended instruction following in complex<br>environments.|Dataset: Self-collected Instruction-following data; Vision En-<br>coder: PaliGemma-3B (SigLIP); Language Encoder: PaliGemma-3B<br>(Gemma-2B); Action Decoder: Flow-Matching Action Expert|
|EnerVerse|✔|✘|World-model LLM for predictive future-space|Dataset: self-collected Synthetic task fusion data; Vision En-|
|(Huang<br>et<br>al.,<br>2025b)|||modeling, enabling long-horizon manipulation<br>planning.|coder:Pretrained VAE + Diffusion Generator; Language Encoder:<br>Tokenized instruction prompt; Action Decoder: Diffusion Policy<br>Head|
|FLaRe (Hu et al.,<br>2024)|✔|✘|Large-scale RL fine-tuning framework generat-<br>ing robust, adaptive robot policies across do-<br>mains.|Dataset: Multi-domain RL demonstrations; Vision Encoder: DinoV2;<br>Language Encoder: Transformer policy (language tokens); Action<br>Decoder: RL policy head|
|Beyond<br>Sight<br>(Jones<br>et<br>al.,<br>2025)|✔|✘|Fuses<br>heterogeneous<br>sensor<br>modalities<br>via<br>language-grounded attention to improve VLA<br>generalization.|Dataset: self-collected Multi-sensor data; Vision Encoder: Multi-<br>modal ViT; Language Encoder: Transformer (shared, task language<br>input); Action Decoder: Transformer action head|
|GeoManip (Tang<br>et al.,2025)|✔|✘|Encodes geometric constraints as model inter-<br>faces, enhancing robustness and precision in ma-<br>nipulation.|Dataset: Self-collected Simulated geometry tasks; Vision Encoder:<br>VLM (GPT-4o) + Grounding-DINO; Language Encoder: GPT-4o;<br>Action Decoder: Constraint solver head|
|Universal<br>Actions<br>(Zheng<br>et al.,2025a)|✔|✘|Defines a universal action dictionary to stan-<br>dardize policy transfer and improve cross-task<br>adaptability.|Dataset: Self-collected Cross-domain manipulation demos; Vision<br>Encoder: Shared VLM (LLaVA-OneVion-0.5B); Language Encoder:<br>LLaVA; Action Decoder: Unified action tokenizer head|
|RoboHorizon|✔|✘|LLM-enhanced multi-view environment model-|i<br>Dataset:Self-collectedMulti-viewrobottrajectoriesVisionEn-|
|(Chen<br>et<br>al.,<br>2025c)|||<br>ing for robust long-horizon task planning.|;  <br>coder: Multi-view transformer (ViT); Language Encoder: GP-<br>TâĂŘbased planner; Action Decoder: DreamerV2 Actor-Critic RL<br>Head|
|SAM2Act (Fang<br>et al.,2025)|✔|✘|Utilizes SAM-based segmentation prompts with<br>memory-augmented VLA for improved object-<br>centric manipulation.|Dataset: SAM-labeled manipulation tasks; Vision Encoder: SAM2<br>segmentation encoder; Language Encoder: CLIP text encoder; Ac-<br>tion Decoder: Memory-augmented policy head|
|LMM<br>Planner<br><br>|✔|✘|Merges LMM-based strategic planning with 3D<br>|Dataset: skill library demos; Vision Encoder: DINO (2D semantics)<br>|
|Integration<br>(Li<br>et al.,2025d)|||skill policies for generalizable manipulation.|+ PointNext (3D); Language Encoder: CLIP Language Encoder;<br>Action Decoder:3D Transformer head|


_<mark>continue</mark>_ 

Page 11 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

|**Model Name**|**End-to-**<br>**End**|**Componen**<br>**Focused**|**t**<br>**Main Contribution**|**Training Dataset and Model Components**|
|---|---|---|---|---|
|VLA-Cache (Xu<br>et al.,2025)|✔|✘|Introduces token-caching to reuse computation<br>across time steps, boosting inference efficiency.|Dataset: LIBERO; Vision Encoder: CLIP ViT; Language Encoder:<br>LLaMA-2; Action Decoder: Cached inference head|
|Forethought<br>VLA (Wu et al.,<br>2025)|✔|✘|Aligns latent vision and action spaces for<br>foresight-driven policy steering.|Dataset: Self-collected Latent alignment demonstrations; Vision En-<br>coder: Phi-3 Vision; Language Encoder: LLama; Language; Action<br>Decoder: Diffusion policy|
|GRAPE (Zhang<br>et al.,2024c)|✔|✘|Preference-guided policy adaptation via person-<br>alized feedback alignment.|Dataset: Self-collected Preference-labeled demos; Vision Encoder:<br>Dinov2; Language Encoder: LLaMA-2; Action Decoder: Autore-<br>gressive transformer head|
|HAMSTER<br>(Li<br>et al.,2025c)|✔|✘|Hierarchical skill decomposition to sequence<br>multi-step manipulation actions.|Dataset: Self-collected Decomposed manipulation tasks; Vision En-<br>coder: VILA-1.5-13B; Language Encoder: VILA-1.5-13B; Action<br>Decoder: Robotic View Transformer Skill execution head|
|TempoRep VLA<br>(Myers<br>et<br>al.,<br>2025)|✔|✘|Use successor representation temporal encoding<br>for compositional action planning.|Dataset: Self-collected Temporal demonstration sequences; Vision<br>Encoder: ResNet-34 CNN; Language Encoder: retrained transformer<br>(CLIP-style); Action Decoder: MLP (3x256) head on ResNet feature|
|ConRFT<br>(Chen<br>et al.,2025b)|✔|✘|Applies consistency regularized fine-tuning with<br>reinforcement for stable policy learning.|Dataset: Self-collected data for fine-tuning; Vision Encoder: same<br>as in octo; Language Encoder:same as in octo; Action Decoder:<br>Reinforced policy head|
|RoboBERT|✔|✘|Unified multimodal Transformer for end-to-|Dataset: Self-collected Multi-domain robot demos; Vision Encoder:|
|(Wang<br>et<br>al.,<br>2025)|||end vision-language-action manipulation, pre-<br>trained on diverse robot and language data.|CLIP ViT; Language Encoder: BERT-base; Action Decoder: CNN-<br>based Diffusion Policy Head|
|Diffusion<br>Transformer<br>Policy<br>(Hou<br>et al.,2024a)|✔|✘|Adapts diffusion-based transformer architectures<br>to VLA policy learning, enabling robust multi-<br>modal action sampling.|Dataset: LIBERO + CALVIN; Vision Encoder: DINOv2; Language<br>Encoder: CLIP Text Encoder; Action Decoder: Diffusion generator<br>head|
|GEVRM (Zhang<br>et al.,2025b)|✔|✘|Generative video modeling of goal-oriented<br>tasks to enhance planning for visual manipula-<br>tion.|Dataset: CALVIN; Vision Encoder: ResNet-34; Language Encoder:<br>T5 Encoder; Action Decoder: Diffusion Policy|
|SoFar (Qi et al.,<br>2025)|✔|✘|Introduces successor-feature orientation repre-<br>sentations bridging spatial reasoning and robotic<br>manipulation.|Dataset: Self-collected Orientation task demonstrations; Vision En-<br>coder: Florence-2 (ViT-style), SAM; Language Encoder: CLIP Text<br>Encode; Action Decoder: VLM (e.g., LLaVA or GPT-4o) for 6D goal<br>pose, then motion planner|
|ARM4R<br>(Niu<br>et al.,2025)|✔|✘|Auto-regressive 4D transition model for predict-<br>ing and planning manipulator trajectories.|Dataset: 76K videos from the Epic-Kitchens100 dataset ; Vision<br>Encoder: ViT-Base; Language Encoder: CLIP text encoder; Action<br>Decoder: 2-layer MLP|
|Magma<br>(Yang<br>et al.,2025)|✔|✘|Foundation multimodal agent model unifying<br>vision, language, and action domains for end-to-<br>end control.|Dataset: Self-collected Multimodal interaction dataset; Vision<br>Encoder: ConvNeXt-XXlarge; Language Encoder: LLaMA-3-8B<br>(decoder-only LLM); Action Decoder: Decoder-Only LLM Head<br>(LLaMA-3-8B)|
|An Atomic Skill<br>Library (Li et al.,<br>2025a)|✔|✘|Constructs an atomic skill library for modular,<br>data-efficient composition of robotic actions.|Dataset: Self-collected Skill primitive demonstrations; Vision En-<br>coder: Prismatic VLM (scene description.), DINO-X (obj detection),<br>SAM-2 (segmentation); Language Encoder: Prismatic, GPT-4 (for<br>planning); Action Decoder: Skill executor module|
|VLAS<br>(Zhao<br>et al.,2025b)|✔|✘|Integrates speech-based LLM guidance for cus-<br>tomizable voice-driven vision-language-action<br>control.|Dataset: Speech-guided robot demos; Vision Encoder: CLIP ViT;<br>Language Encoder: Vicuna (LLaMA-7B/13B); Action Decoder: Vi-<br>cuna as an Autoregressive Action Decoder|
|ChatVLA (Zhou<br>et al.,2025)|✔|✔|Unified conversational VLA enabling natural-<br>language and vision-driven interactive robot<br>control with real-time multimodal feedback.|Dataset: Interactive human-robot demos; Vision Encoder: ViT +<br>LoRA; Language Encoder: Qwen2-VL-2B (LLM); Action Decoder:<br>mixture-of-expert action head, as in DiVLA)|
|RoboBrain<br>(Ji<br>et al.,2025)|✔|✘|Knowledge-grounded policy brain that maps ab-<br>stract high-level plans to concrete multimodal<br>actions across diverse tasks.|Dataset: Multi-domain robot and plan data; Vision Encoder: SigLIPr;<br>Language Encoder: Qwen2.5-7B-Instruct (decoder-only LLM); Ac-<br>tion Decoder: LoRA adapters for skill|
|SafeVLA|✔|✘|Safety-aware VLA integrating constraint feed-|Dataset: Safety-scenario demonstrations; Vision Encoder: Modu-|
|(Zhang<br>et<br>al.,<br>2025a)|||back through safe RL to ensure collision-free,<br>reliable manipulation.|lar (DINOv2, SigLIP, CLIP); Language Encoder: LLM (model-<br>agnostic, e.g., T5, LLaMA, Qwen); Action Decoder: Safety-<br>constraint policy head|
|CognitiveDrone<br>(Lykov<br>et<br>al.,<br>2025)|✔|✘|Embodied cognitive reasoning VLA for UAVs,<br>combining vision-language understanding with<br>autonomous flight planning.|<br>Dataset: UAV mission logs; Vision Encoder: OpenVLA visual en-<br>coder (ViT-style) ; Language Encoder: OpenVLAâĂŹs language<br>encoder; Action Decoder: Transformer policy head|
|Diffusion-VLA|✔|✔|Multimodal VLA framework unifying vision-|Dataset: Multi-embodiment manipulation suites; Vision Encoder:|
|(Wen<br>et<br>al.,<br>2024)|||language reasoning with diffusion-based policy<br>for robust, generalizable manipulation across di-<br>verse robot embodiments.|SigLIP; Language Encoder: Qwen2-VL (2B/7B/72B); Action De-<br>coder: Latent diffusion policy head + MLP|


Page 12 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 8:** This mind map presents the principal classes of vision encoders, language encoders, and action decoders employed in state-of-the-art VLA models. Only those encoder and decoder classes that are utilized by at least three different models are visualized, highlighting prevailing architectural trends across the VLA literature. The taxonomy categorizes representative models under each component family based on their dominant backbone; for example, ViT variants (such as; CLIP, SigLIP, DINOv2) and CNNs for vision encoding, LLaMA/Vicuna, T5-base, Qwen, and GPT-based models for language encoding, and diffusion or autoregressive transformers, MLP, and general Token predictors for action decoding. It should be noted that some models are listed under multiple encoder categories due to hybrid or fused architecture designs. For instance, models such as HybridVLA, OpenVLA, and DexGraspVLA appear under both SigLIP and DINOv2, as they integrate features from both backbones to enhance visual grounding and downstream task performance. This fusion-based design supports improved generalization, multi-view robustness, and more flexible multimodal alignment. 

Language encoders show similar architectural diversity. LLaMA and Vicuna-based language encoders are widely used in models such as RevLA, OpenVLA, and HybridVLA for instruction understanding and zero-shot reasoning. T5style models appear in VIMA, Octo, and FLARE, offering flexible encoder-decoder structures for sequence generation. GPT-based and Qwen-based encoders, such as those used in VoxPoser, Edge VLA, and DexVLA, balance generalization and compact deployment. Gemma-2B language encoders are found in Pi-0 and FAST, while specialized solutions like CLIP Text encoders are used in CLIPort and PerAct for minimal alignment tasks. 

In action decoders, diffusion-based transformers are a leading choice for models like Octo, HybridVLA, and DexGraspVLA, as they offer fine-grained, temporally smooth control via iterative denoising. Autoregressive Transformer heads, such as those in Gato, OpenDrive VLA, and GRAPE, generate action sequences step-by-step, optimizing real-time responsiveness. Several models including VoxPoser, LMM Planner Integration, and FLARE embed Model Predictive Control or specialized planning heads to support decisionmaking in dynamic tasks. MLP or token predictor heads are used in OpenVLA, TraceVLA, and RoboMamba for efficient low-level control. 

Page 13 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 9:** Schematic of the unified VLA training data format. Visual observations, language instructions, and action/control signals are grouped into episode directories and serialized into standardized storage formats (JSON, TFRecord, and HDF5), enabling efficient and scalable data loading for end-to-end model training. 

Our evaluation of VLA architectures shows a wide variety of algorithms in each core component. For the vision encoder, the majority of models used CLIP and SigLIPbased ViT backbones to extract rich, semantically aligned visual features. In the language domain, the LLaMA family (including LLaMA-2 and its larger variants) is most commonly used, appearing in several models as the primary text encoder. When it comes to action decoding, diffusion-based Transformer heads are the most popular choice with their ability to model complex, multimodal action distributions. On the data side, while many teams rely on privately collected manipulation demonstrations, the publicly available Open X-Embodiment dataset is the most commonly used. 

# **5. VLA Training Datasets** 

The foundation of VLA models lies in high quality, diverse training datasets. These datasets are crucial as they expose models in the complete range of real and simulated environments, ensuring a tight alignment of visual elements, natural language instructions, and control (James et al., 2020). These datasets allow VLAs to learn complex crossmodal correlations, such as how language complexities (e.g., ’gently place’) affect motion smoothness without relying on manually prepared heuristics. We first introduce the unified dataset schema that underlies the VLA training pipelines, then survey the most influential public datasets, and finally apply a comprehensive benchmarking strategy to assess the scale, modality coverage, and complexity of each dataset. 

## **5.1. Dataset Format** 

Structured overview of the general dataset format commonly used in VLA training pipelines. is illustrated in 

Fig. 9. It highlights the systematic organization of multimodal data into three primary streams: visual, language, and action/control, which collectively facilitate the training and evaluation of VLA models. 

The _Visual Streams_ comprise raw RGB frames, video snippets, and optionally, depth maps and segmentation masks. These visual inputs provide essential spatial and contextual data to perception modules in VLA architectures. Typically, the data in this stream is stored in standard image or video formats like JPEG or PNG for individual frames and MP4 or similar formats for video snippets. 

The _Language Streams_ incorporate natural-language instructions or dialogues alongside tokenization metadata (such as token offset). These textual annotations are essential for instructing and conditioning robotic actions and are commonly stored in lightweight, structured formats such as JSON or plain text files. The presence of tokenization metadata facilitates efficient textual processing, enabling direct integration with transformer-based language models. 

The _Action/Control Labels_ include discrete action tokens (e.g. categorical commands like "move forward" or "turn left") and continuous control vectors representing joint positions or end-effector trajectories. These action labels provide explicit supervision signals for model output and are typically stored as NumPy arrays or encoded within structured data containers. 

All three modality streams are systematically integrated into standardized episode-level directories (e.g., episode/), where visual data reside in subdirectories such as rgb/ and depth/, accompanied by lang.json, actions.npy, and states.npy. Each episode folder can then be serialized in formats like: _JSON_ for lightweight, human-readable metadata; _TFRecord_ / _TF-Example_ for high-throughput, sharded training; or _HDF5_ for efficient random access to synchronized frames, actions, and state arrays, enabling balance readability, I/O performance, and scalability in their training pipelines. 

## **5.2. Major VLA Datasets** 

Table 2 summarizes the progress of VLA datasets, highlighting how each dataset advances autonomy by varying in scale, modality, and task complexity. Early collections such as EmbodiedQA and R2R focus on discrete decision making in constrained environments, offering simple state-action mappings suitable for evaluating baseline policy architectures (e.g., PACMAN, Speaker-Follower). As we move into 2020-2022, datasets like ALFRED, RLBench, and CALVIN introduce longer-horizon tasks and richer sensory streams combining RGB, depth, proprioception, and natural language instructions to stress test hierarchical planning and subgoal decomposition methods (e.g., C2F-ARM, VIMA, RT-2). These mid-generation datasets bridge the gap between symbolic planners and end-to-end learning, enabling comparative analyses of model-based control versus learned policies under simulated dynamics. 

Page 14 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

Table 2: Overview of main VLA datasets used in robotic manipulation and embodied AI research. For each dataset, we list the release year, dataset size, distinctive characteristics, and the data storage format. 

|**Dataset**<br>EbdidAD  l|**Size**|**Distinctive Characteristics**|**Data Format**|
|---|---|---|---|
|moeQ (as et a.,<br>2018)|5,000+ QA episodes across<br>750+ 3D scenes|Goal-directed visual question answering<br>in House3D with object and room diver-<br>sity|JSON-formatted question-answer pairs, egocentric RGB<br>frame sequences, and agent trajectories|
|R2R (Anderson et al.,2018)|7,189 unique paths with 21,567<br>natural language instructions|Real-world vision-language navigation us-<br>ing Matterport3D with path diversity and<br>crowd-sourced instructions|JSON files with instructions and navigation paths;<br>panoramic JPEG frames and viewpoint graph metadata|
|ALFRED (Shridhar et al.,<br>2020)|8,055<br>expert<br>demonstrations<br>with 25,743 language directives|Language-conditioned household manip-<br>ulation tasks in AI2-THOR 2.0 across 120<br>indoor scenes|Per-demonstration folders with egocentric RGB frames,<br>ground-truth interaction masks, and language annotations;<br>metadata and action/state sequences in JSON format|
|RLBench (James et al.,2020)|Expert demonstrations avail-<br>able for 100 vision-based ma-<br>nipulation tasks|Large-scale few-shot and imitation learn-<br>ing benchmark in PyRep simulation|Pickled demos include joint_positions, camera_images,<br>task_description, and proprioceptive states.|
|CVDN (NDH) (Thomason<br>et al.,2019)|7,415 navigation-from-dialog-<br>history instances from 2,050 di-<br>alogs|Vision-and-Dialog Navigation benchmark<br>requiring agents to act based on dialog<br>history|JSON annotations with dialog turns, navigation paths,<br>image features, and speaker roles|
|TEACh (Padmakumar et al.,<br>2021)|3,047<br>successful<br>two-agent<br>gameplay sessions|Multiturn dialog-driven household task<br>completion in AI2-THOR|JSON transcripts aligned to visual frames, with egocentric<br>RGB, object masks, action logs, and benchmark CSV<br>splits|
|DialFRED (Gao et al.,2022a)|53,000+ human-annotated QA<br>pairs across 34,000+ tasks|Dialogue-enabled embodied instruction<br>following on augmented ALFRED sub-<br>goals|Per-taskdialogue.jsonwith human and oracle QAs, action<br>traces, subgoal templates, and frame alignment|
|Ego4D (Grauman et al.,2022)|3,670 h of first-person video|Large-scale, real-world egocentric dataset<br>with diverse scenarios and modalities|MP4 video clips; JSON-based narrations and annotations;<br>HDF5/LMDB indices; multilingual narration files.|
|CALVIN (Mees et al.,2022)|5,000+ demonstrations|Long-horizon,<br>language-conditioned<br>robotic manipulation tasks|HDF5 archives with synchronized RGB-D frames, propri-<br>oception, action sequences, and natural language instruc-<br>tions.|
|DROID (Khazatsky,2024)<br>O|76k<br>demonstrations;<br>564<br>scenes, 86 tasks|High-diversity<br>language-conditioned<br>robot manipulation|RLDS-formatted RGB-D data, stereo video, camera cali-<br>brations, language annotations, and robot state/action logs.|
|pen<br>X-Embodiment (Collaboration<br>et al.,2025)|1M+ trajectories, 500+ skills,<br>22 robot types|Large-scale,<br>multi-embodiment,<br>multi-<br>skill manipulation dataset|Sharded TFRecords with RGB/depth frames, language<br>instructions, action vectors; YAML metadata and RLDS<br>format.|
|RoboSpatial (Song et al.,<br>2025a)|1M images, 5K 3D scans, 3M<br>spatial QA pairs|2D-3D paired spatial reasoning dataset|RGB images, 3D scans, and relational graph annotations<br>in support of spatial understanding benchmarks.|
|CoVLA (Arai et al.,2024)|83.3 h real-world driving video,<br>6M frames|Time-aligned<br>vision-language-action<br>dataset|Synchronized RGB video, GPS/IMU-based trajectories,<br>and auto-generated captions using rule-based and VLM<br>methods.|
|TLA (Hao et al.,2025)<br>|30K contact-rich peg-in-hole<br>demonstrations|Tactile-language-action alignment for pre-<br>cise insertion and assembly|ROS bag files with synchronized camera/, tactile/,<br>lang.json, andtrajectory.csvrecordings.|
|BridgeData V2 (Walke et al.,<br>2023)|60,096<br>trajectories<br>(50,365<br>teleoperated; 9,731 scripted)|Multi-skill<br>goal-<br>and<br>language-<br>conditioned manipulation dataset|TFRecords with RGB images, natural language instruc-<br>tions, and continuous 7-DoF action vectors; includes both<br>human and scripted demonstrations.|
|LIBERO (Liu et al.,2023)|130 tasks: 10 spatial, 10 object,<br>10 goal, 100 lifelong|Lifelong VLA benchmark for procedural<br>and declarative knowledge transfer|<br>JSON and Parquet files with RGB images, language in-<br>structions, action trajectories, and structured metadata.|
|Kaiwu (Jiang et al.,2025)|1M<br>multimodal<br>robotic<br>episodes|Real-world, multi-embodiment dataset for<br>dexterous manipulation with natural lan-<br>guage commands|Per-episode HDF5 files with synchronized RGB, depth,<br>3D skeletons, tactile, EMG, gaze, IMU, audio, language,<br>and motion capture data.|
|PLAICraft (He et al.,2025)|10,000 + hours of multiplayer<br>Minecraft gameplay across 5<br>modalities|<br>Open-ended<br>multiplayer<br>interaction<br>with<br>emergent<br>task<br>structures<br>and<br>voice-aligned social play|<br>JSON-encoded multimodal streams (RGB, audio, key-<br>board, mouse) with millisecond alignment|
|AgiBot World (Bu et al.,2025)|1M+ multimodal dual-arm tra-<br>jectories|<br>Open-source platform for long-horizon<br>eneralist olic learnin|ROS-based: RGB-D, fisheye, tactile, proprioception, lan-<br>uae error annotations and dexterous control los|
|Robo360 (Liang et al.,2023)|2K+ real trajectories, 86 cali-<br>brated views, 100+ diverse ob-<br>jects|g py g<br>Multimodal dataset for dynamic NeRF,<br>imitation learning, and control|gg,  ,    g.<br>Synchronized RGB videos, depth maps, audio, robot pro-<br>prioception, and control signals per frame.|
|REASSEMBLE (Sliwowski<br>et al.,2025)|4,551 contact-rich demonstra-<br>tions, 17 objects, 781 minutes|Multimodal<br>(RGB,<br>audio,<br>event,<br>force/torque, proprioception)|Synchronized multistream recordings from RGB cameras,<br>event camera, microphones, force/torque sensors, and pro-<br>prioceptive signals, collected during haptically teleop-<br>erated assembly and disassembly tasks based on NIST<br>benchmark boards.|
|RoboCerebra (Han et al.,2025)|100K long-horizon trajectories<br>across 1K+ tasks|System-2-level reasoning and generaliza-<br>tion in real-world-scale settings|Structured plan logs, visual transitions, failure anno-<br>tations, and dense subtask labels from human-verified<br>demonstrations and multi-stage task generation.|
|IRef-VLA (Zhang et al.,<br>2025c)|11.5K rooms, 7.6M spatial rela-<br>tions, 4.7M instructions|Imperfect referential grounding in 3D in-<br>door scenes|<br>Per-room scene graphs, free-space maps, and affordance<br>annotations with synthetic and imperfect language queries.|
|Interleave-VLA (Fan et al.,<br>2025)|210K episodes (13M frames)|Interleaved<br>vision-language<br>instruction<br>execution|Mixed-format episodes with images, sketch overlays, and<br>text prompts aligned with action sequences.|
|RoboMM (Yan et al.,2024)|30K simulated episodes + 5K<br>real-world trials|Multimodal fusion of vision, language,<br>proprioception and touch|<br>HDF5 per episode with<br>rgb/,<br>depth/,<br>tactile.csv,<br>instructions.jsonandactionsequence.json.|
|ARIO (Wang et al.,2024b)|<br>50K simulated episodes + 5K<br>real-world trials|,<br>Contact-rich manipulation with tactile, au-<br>dio, andproprioceptive feedback|,_<br>Per-episode HDF5 archives withrgb/,depth/,tactile.csv,<br>instructions.json, andaction_sequence.json.|


Page 15 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

From 2023 onward, the field shifts to truly multimodal control challenges. Datasets such as DROID and Open X- Embodiment embed synchronized RGBD, language, and multi-skill trajectories, facilitating evaluation of sensor fusion strategies and real-time feedback controllers. Largescale egocentric corpora like Ego4D and CoVLA offer real-world visual streams that drive research on robust perception-action loops under unpredictable dynamics. Recent contact-rich datasets such as ARIO, TLA, RoboMM, and REASSEMBLE integrate high-frequency haptic and force/torque feedback alongside vision and language, enabling fine-grained impedance control and hybrid modelpredictive schemes for deformable-object manipulation. Highly multimodal and large-scale datasets such as Kaiwu, PLAICraft, AgiBot World, and Robo360 support openended, long-horizon, and real-world tasks with diverse sensor suites including tactile, audio, proprioceptive, and multiview data. By standardizing annotation formats (HDF5 bundles, ROS bags, TFRecords) and pairing each collection with representative baselines (e.g., SayCan, HapticBERT, MMFusionNet), Table 2 provides a detailed overview of these datasets across a continuum of task complexity, modality richness, and real-world fidelity. 

where _𝛼𝑖 >_ 0 for _𝑖_ = 1 _,_ … _,_ 4 are weights that normalize each term to commensurate scales and can be tuned to reflect the emphasis on action length, skill diversity, sequential structure, or language complexity. For our benchmark, we set all weights equal to one. 

Modality richness, captured by the score mod, integrates four factors reflecting the scope and quality of sensory input: 

- Number of distinct modalities ( _𝑀_ ), Such as vision, depth, haptics, and language. 

- 1 

- • Mean quality _𝑄_ = _𝑀_ ∑ _𝑀𝑖_ =1<sup>_𝑄𝑚_</sup> _𝑖_<sup>,Where</sup><sup>_𝑄𝑚_</sup> _𝑖_<sup>for</sup><sup>_𝑖_=</sup> 1 _,_ … _, 𝑀_ are the modality-specific quality scores. _𝑄𝑚𝑖_ can be determined by expert annotation, automated signal-to-noise ratio analysis, or based on dataset documentation and previous benchmark studies. For this work, we use a mixture of empirical review and published specifications to assign scores in the range [0 _._ 6 _,_ 0 _._ 95], reflecting the typical range of public datasets. 

- Fidelity of temporal alignment across modalities ( _𝐴_ ), Measures how tightly modalities are synchronized (e.g., frame-accurate vision-language pairing), with _𝐴_ ∈[0 _,_ 1]. 

## **5.3. Benchamrk VLA Datasets** 

In order to benchmark, we map each major VLA dataset onto a two-dimensional plane spanned by task complexity and modality richness, illustrated in Fig. 10. The x-axis captures how challenging each dataset’s manipulation tasks are, ranging from simple single-step actions to long-horizon, multiskill sequences. The y-axis shows the modality richness, from minimal (dual modalities: text and image) to comprehensive (up to seven modalities including audio, video, robot proprioception, control, depth, haptics, and language). 

To quantify these dimensions systematically, we assign scalar scores to each dataset reflecting their task complexity and modality richness. Task complexity, denoted as task, incorporates: 

- Average number of low-level actions per episode ( _𝑇_ ). This captures how many primitive control commands are grouped together in a typical task (e.g., grasp, lift, move). 

- Number of distinct high-level skills ( _𝑆_ ). This enumerates different semantic subtasks (e.g., open drawer, pick object). 

- Degree of sequential task dependency ( _𝐷_ ). This denotes the fraction of tasks that require strict ordering of subtasks; _𝐷_ ∈[0 _,_ 1]. 

- Linguistic abstraction level ( _𝐿_ ). Quantifies the average linguistic complexity (e.g., vocabulary size or syntactic depth) of the instruction set; _𝐿_ ∈ ℝ<sup>+</sup> . 

These attributes are integrated via the following weighted model: 

- Presence of reasoning-critical modalities ( _𝑅_ ): Such as object masks or scene graphs that enable higher-level reasoning, _𝑅_ ∈{0 _,_ 1}. 

This scoring mechanism is formalized as: 


where modality sensitivity weights _𝛽𝑖 >_ 0 for _𝑖_ = 1 _,_ … _,_ 4 tune the relative importance of modality count, signal quality, temporal alignment, and reasoning-enabled annotations. For our benchmark, we set all weights equal to one. 

Finally, to allow direct comparison across heterogeneous benchmarks, both raw scores are normalized. Task complexity to a standardized [1 _,_ 5] scale and modality richness to a [2 _,_ 5] scale. This mapping ensures interpretability: datasets with the lowest complexity or modality richness receive a score of 1 or 2 ("Very Low"/"Minimal") and the highest receive 5 ("Very High"/"Comprehensive"), with intermediate values reflecting proportional positioning. The bubble size then encodes the relative dataset scale (e.g., number of episodes or hours), providing an at-a-glance summary of both range and comprehensiveness across the leading VLA benchmarks. 

The resulting visualization effectively categorizes datasets, while it also highlights critical gaps in current benchmark, offering notably the underrepresented region combining highly complex tasks with extensive multimodal integration. This gap underscores a promising direction for future dataset development aimed at advancing truly generalist robotic agents capable of complex, real-world perception and planning. 

- task() = _𝛼_ 1 log(1 + _𝑇_ ) + _𝛼_ 2 _𝑆_ + _𝛼_ 3 _𝐷_ + _𝛼_ 4 _𝐿,_ (4) 

Page 16 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 


**Figure 10:** Benchmarking VLA Datasets by Task Complexity and Modality Richness. Each bubble represents a VLA dataset, positioned according to its normalized task-complexity score (x-axis) and its modality-richness score (y-axis). The bubble area is proportional to the dataset scale that is number of annotated episodes or interactions. The script to generate the plot can be found here:https://github.com/Muhayyuddin/VLAs 

## **5.4. Benchmarking Analysis** 

Fig. 10 shows that most current VLA benchmarks are concentrated within a task complexity range from very low to high on the x-axis and span from minimal to rich modality along the y-axis. Early navigation and QA datasets like EmbodiedQA, R2R, and RoboSpatial are characterized by their very low complexity and minimal modality, reflecting simple, discrete decision-making in constrained environments. In contrast, mid-generation collections such as RLBench, TEACh, Ego4D, CVDN, and RoboCerebra, tend to feature low to moderate complexity with moderate modality richness, often focused on navigation, imitation, or basic manipulation tasks involving a limited number of modalities. 

As the field evolves, datasets such as ALFRED, DialFRED, CoVLA, Interleave-VLA, RoboData, and REASSEMBLE have moved into the medium-complexity, richmodality region by incorporating additional sensory streams like depth, language, and proprioceptive signals, enabling more sophisticated evaluation of policy learning and multistep planning. In particular, a small subset of datasets, including Iref-VLA, Robo360, TLA, CALVIN, and Open X- Embodiment, simultaneously achieve high task complexity and rich modality, each with a particular focus. Robo360 on multiview real-robot visual fidelity, Iref-VLA on referential grounding in 3D scenes, TLA on tactile-language-action alignment for contact-rich assembly, CALVIN on longhorizon language-conditioned robotic manipulation, and Open X-Embodiment on multirobot, multiskill demonstrations at scale. 

The only dataset positioned at the extreme of both axes is Kaiwu, which achieves very high task complexity alongside the most comprehensive modality richness, integrating vision, depth, language, proprioception, haptics, and additional streams. Meanwhile, AgiBot World stands out in the very high complexity quadrant while exhibiting just moderate modality diversity, emphasizing large-scale, longhorizon dual-arm tasks rather than maximal sensor integration. This disparity highlights a critical gap: current VLA benchmarks do not yet fully integrate the challenges of longhorizon, multi-skill control with exhaustive multimodal input (vision, depth, language, proprioception, haptics, audio, and scene graphs). Without such datasets, the development of robust and generalist robotic agents remains limited. Future efforts should therefore focus on the upper right quadrant of the landscape, creating new VLA benchmarks that maximize both task difficulty and multimodal diversity to accelerate progress toward general-purpose embodied intelligence. 

# **6. Simulation Tools** 

Simulation environments have become essential for VLA research, offering scalable, repeatable, and extensively annotated data at orders of magnitude greater than what is feasible in the physical world. Modern platforms such as AI2-THOR, Habitat, and NVIDIA Isaac Sim provide high-precision physics, realistic rendering, and customizable multimodal sensors ranging from RGBD cameras, force/torque and tactile probes, to proprioceptive encoders 

Page 17 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

**Table 3** 

Overview of simulation platforms commonly used for generating and evaluating VLA datasets. The table summarizes each simulator’s supported sensory modalities, primary use cases, core capabilities, and the datasets that rely on them. These tools span diverse domains such as photorealistic indoor navigation, dexterous manipulation, and large-scale reinforcement learning, with varying degrees of physics realism. 

|**Simulator**<br>|**Modalities**|**Use Cases**|**Capabilities**|**Datasets**|
|---|---|---|---|---|
|AI2-THOR (Kolve<br>et al., 2017) **[link]**<br>|RGB,<br>depth,<br>semantic/instance<br>segmentation,<br>object<br>states|Embodied navigation, object<br>manipulation|Photorealistic indoor scenes;<br>procedural scene generation;<br>physics-based object/agent in-<br>teraction; built-in interaction<br>APIs; language and task inte-<br>gration|ALFRED<br>(Shridhar<br>et<br>al.,<br>2020), TEACh (Padmakumar<br>et al., 2021), DialFRED (Gao<br>et al., 2022b)|
|Habitat (Savva et al.,<br>2019) **[link]**<br>NVIDIAIsaac|RGB, depth, semantic seg-<br>mentation, agent pose|Vision-language<br>navigation,<br>embodied<br>QA,<br>point-goal<br>navigation|Photorealistic,<br>high-<br>performance<br>rendering;<br>large-scale 3D scene support;<br>modular<br>sensor<br>and<br>agent<br>APIs|R2R (Anderson et al., 2018),<br>CVDN<br>(Thomason<br>et<br>al.,<br>2019),<br>EmbodiedQA<br>(Das<br>et al., 2018)|
|<br>Sim (NVIDIA<br>Corporation) **[link]**<br>|RGB,<br>depth,<br>LiDAR,<br>semantic/instance<br>segmentation,<br>bounding<br>boxes, point clouds, physics<br>states, force/torque, event<br>camera|RL<br>&<br>control,<br>sim-to-real<br>transfer,<br>synthetic<br>dataset<br>generation,<br>embodied<br>AI,<br>multi-robot simulation, digital<br>twin, warehouse & industrial<br>robotics|Physically accurate PhysX dy-<br>namics; RTX-accelerated pho-<br>torealistic rendering; procedu-<br>ral scene generation; domain<br>randomization; noise models;<br>ROS/ROS2 and Python API;<br>cloud deployment|Open X-Embodiment (Collab-<br>oration et al., 2025), Isaac<br>Gym, RLBench, custom syn-<br>thetic datasets|
|Gazebo (Koenig and<br>Howard, 2004) **[link]**|RGB, depth, LiDAR, IMU,<br>joint states, force/torque,<br>contact, GPS|Control<br>algorithm<br>development,<br>multirobot<br>coordination,<br>sim-to-real<br>transfer, embodied navigation<br>and manipulation|Open-source;<br>plugin-based<br>extensibility;<br>realistic<br>multi-<br>physics engines; ROS1/ROS2<br>integration;<br>multi-robot,<br>multi-sensor support|RoboSpatial<br>(Song<br>et<br>al.,<br>2025a),|
|PyBullet (Coumans<br>and Bai, 2016) **[link]**<br>|RGB, depth, contact forces,<br>joint states|RL, robotic manipulation pro-<br>totyping, physics-based simu-<br>lation|Real-time<br>physics;<br>Python<br>API;<br>cross-platform;<br>easy<br>scripting;<br>supports<br>robotics<br>and VR|QUAR-VLA<br>(Chen<br>et<br>al.,<br>2024),<br>various<br>custom<br>RL/manipulation datasets|
|CoppeliaSim (Rohmer<br>et al., 2013) **[link]**|RGB, depth, joint states,<br>force/torque sensors, prox-<br>imity sensors|Multi-robot coordination, task<br>scripting, manipulation, edu-<br>cation|Multiple built-in physics en-<br>gines; remote APIs (Python,<br>ROS, C++); graphical scene<br>editor; flexible scripting|RLBench (James et al., 2020),<br>CALVIN (Mees et al., 2022)|
|Webots (Michel,<br>2004) **[link]**<br>Unity|RGB, depth, sound, GPS,<br>proximity, IMU, lidar, joint<br>states|Mobile navigation, multi-robot<br>and swarm robotics, manipula-<br>tion, education|Cross-platform; extensive sen-<br>sor and actuator models; GUI<br>scenario/world design; ROS in-<br>tegration; physics-based simu-<br>lation|AgiBot World (Bu et al.,2025)|
|ML-Agents (Juliani<br>et al., 2018) **[link]**|RGB,<br>depth,<br>raycasts,<br>physics states|Reinforcement<br>&<br>imitation<br>learning, interactive tasks|Unity<br>engine<br>visual<br>fidelity;<br>Python/C# APIs; curriculum<br>learning|Used in custom RL and nav-<br>igation datasets (e.g., Obsta-<br>cle Tower, RoomNav, Mini-<br>World);|
|MuJoCo (Todorov<br>et al., 2012) **[link]**|Joint<br>positions,<br>contact<br>forces, kinematics, RGB|Continuous control, dynamics<br>learning, RL research|High-speed simulation; accu-<br>rate contact and soft body<br>modeling; analytic gradients|Meta-World (Yu et al., 2020),<br>RoboSuite (Zhu et al., 2020),<br>custom RL benchmarks|
|iGibson (Xia et al.,<br>2020) **[link]**|RGB, depth, semantic & in-<br>stance masks, object poses,<br>contact forces|Interactive navigation, manip-<br>ulation, semantic reasoning|Photorealistic dynamic scenes;<br>real-world<br>scene<br>reconstruc-<br>tions; interactive objects and<br>agents|iGibson<br>v1/v2<br>(Xia<br>et<br>al.,<br>2020)|
|UniSim (Yang et al.,<br>2023) **[link]**|RGB,<br>depth,<br>propriocep-<br>tion, haptics, audio|Multi-modal dataset genera-<br>tion, multi-agent coordination,<br>manipulation, navigation|Unified multi-sensor API; scal-<br>able cloud-native simulation;<br>plugin-based extensibility; sup-<br>port for real and simulated sen-<br>sor data|UniSim-VLA<br>(Yang<br>et<br>al.,<br>2023)|
|SAPIEN (Xiang et al.,<br>2020) **[link]**|RGB, depth, segmentation<br>masks, contact forces, artic-<br>ulated object states|Deformable<br>and<br>articulated<br>object manipulation, semantic<br>reasoning, dexterous grasping|High-fidelity<br>GPU-based<br>physics;<br>real-time<br>dynamic<br>simulation;<br>Python<br>API;<br>large-scale articulated object<br>library|DexGraspNet (Wang et al.,<br>2023), TLA (Hao et al., 2025)|


and language interfaces all configurable at fine temporal resolutions. Using procedural scene generation, randomized object properties, and scripted agent behaviors, simulators enable the automated synthesis of hundreds of thousands of trajectories, complete with ground truth annotations 

for object poses, semantic maps, action sequences, and natural language instructions. Crucially, built-in toolkits for scenario scripting and domain randomization facilitate systematic studies of generalization under varied lighting, object geometries, and task orders, while lightweight GPU 

Page 18 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

accelerated backends support rapid iteration of new dataset designs. Together, this ecosystem of VLA simulators accelerates the co-development of control algorithms and benchmark datasets, ensuring that advances in multimodal perception, language grounding, and closed-loop planning can be evaluated and refined in a controlled, reproducible framework before deployment on real robotic platforms. 

Table 3 summarizes the current state-of-the-art simulation platforms used for the generation of VLA datasets. The table lists four essential aspects for each simulator: the _Modalities_ of sensors it offers, the main _Use Cases_ it supports, its fundamental technical _Capabilities_ , and the representative _Datasets_ that are based on it. This unified view allows researchers to directly compare engines based on their multi-modal sensor suite, physics accuracy, scalability, and integration with language and control APIs. 

In the first column, platforms such as AI2-THOR and Habitat provide photorealistic RGB, depth, and semantic streams, making them ideal for embodied navigation and visual question answering benchmarks (e.g., ALFRED, R2R, EmbodiedQA, CVDN). Middle entries like NVIDIA Isaac Sim and Gazebo deliver advanced LiDAR, IMU, force/torque, and multi-robot support crucial for large-scale reinforcement learning, sim-to-real transfer, and multi-agent coordination, as in Open X-Embodiment and RoboSpatial. Contact-rich simulators including PyBullet, CoppeliaSim, MuJoCo, and SAPIEN enable precise force, torque, and haptic feedback, powering dexterous manipulation datasets such as DexGraspNet, CALVIN, and TLA. Emerging platforms (Unity ML-Agents, RoboSuite, IsaacGym, UniSim) highlight capabilities such as GPU-parallel rollout, cloudnative simulation, and unified multi-sensor APIs, enabling the creation of next-generation VLA datasets with millions of diverse trajectories spanning vision, language, touch, and audio. The table provides an essential reference by mapping these four aspects across fifteen simulators: it assists in choosing the optimal backend for dataset generation, clarifies the trade-offs between rendering quality and processing speed, and identifies gaps where enhancements in simulator features could facilitate more detailed VLA benchmarks. 

# **7. Applications and Evaluation of VLAs** 

## **7.1. Application Domains** 

The Table 4 organizes VLA models into six broad application domains. These application domains are explained below. 

The _Manipulation and Task Generalization_ domain covers models that unify visual perception and language instructions into a single control policy for diverse objectlevel tasks from simple grasping and placement to complex assembly with a focus on maintaining adaptability to novel objects, configurations, and robot models with limited retraining. In _Autonomous Mobility_ domain, models convert high-level language goals into safe, efficient navigation plans for wheeled, legged, or aerial platforms. They combine scene understanding (identifying landmarks, obstacles, and 

waypoints) with motion planning to follow verbal or written navigation instructions. 

In _Human Assistance and Interaction_ application area, agents interpret human commands and contexts to perform collaborative tasks, handling tools, manipulating domestic objects on request, or automating GUI workflows via multi-turn dialogues, prioritizing responsiveness and safety when working alongside people. The _Robotic Platforms_ category focuses on models for controllers specialized to specific hardware (quadrupeds, humanoids, custom arms), integrating platform-aware perception and action modules that respect each robot’s kinematics, dynamics, and sensor capabilities. _Virtual Environments_ includes purely softwarebased agents that automate GUIs, play video games, or act as benchmarking frameworks. This domain highlights how VLA techniques are generalized beyond physical robots in simulated or desktop settings. _Edge and Low-Power Deployment_ focuses on lightweight architectures optimized for immediate inference on CPUs or embedded processors, demonstrating that successful VLA integration can function within limited computational and energy constraints. 

## **7.2. VLA Model Selection and Evaluation** 

Since manipulation and task generalization remain the dominant challenges in VLA research, we selected ten models that best exemplify high manipulation skill and broad task generalization. These models were chosen according to: (1) the breadth of task coverage, including the ability to handle unseen problems, (2) zero-shot or few-shot generalization to new embodiments and environments, (3) robust real-robot validation, (4) architectural novelty in fusion or decoding mechanisms, and (5) computational practicality regarding inference speed and resource usage. 

Our evaluation framework employs three standardized metrics that are success rate, zero-shot generalization, and real-robot validation to enable direct comparisons across VLA architectures. Table 5 summarizes ten representative models, listing each model’s name and its primary benchmark dataset. The _Success Rate_ column categorizes average task completion as High (≥ 90 %), Medium (70-90 %), or Low (< 70 %). _Zero-Shot Capability_ is estimated High for ≥ 80 % success on unseen tasks, Medium for 50-80 %, and Low for < 50 %. Finally, _Real-Robot Deployment_ indicates whether a model has been validated on physical hardware (Yes) or remains simulation only (No). This uniform metric framework allows for direct comparison between architectures and datasets. 

RT-2 demonstrates this balance by co-finetuning on internet-scale VQA data and robot trajectories to achieve zero-shot transfer across dozens of tasks on multiple robots. Pi-0 shows that a lightweight 3B-parameter model can operate at over 200 Hz while generalizing to new tasks and robots. CLIPort introduced dense semantic grounding using CLIP-enhanced transport maps, setting state-of-the-art results on diverse tabletop manipulation tasks. VIMA demonstrated that a single, prompt-based, multimodal policy could perform six grounding tasks, including pushing, grasping, 

Page 19 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

**Table 4** 

Categorization of VLA Models by Application. 

|**Application**|**VLA Models**|
|---|---|
|**Manipulation and Task Generalization**|CLIPort; RT-1; Gato; VIMA; RoboAgent; RT-Trajectory; RT-2; Pi-0; OpenVLA; OpenVLA-OFT; Tiny<br>VLA; DexVLA; OneTwoVLA; RDT-1B; Shake-VLA; DexGraspVLA; Bi-VLA; MoLe-VLA; TLA; ACT;<br>GeoManip; LMM Planner Integration; Online RL VLA; SAM2Act; VoxPoser; Diffusion Policy; Octo;<br>Chain-of-Affordance; CogACT; ECoT; OTTER; Gemini Robotics; V-JEPA 2; Knowledge Insulating VLA<br>Models; AgiBot World Colosseo; Fine-Tuning VLA Models; Hi Robot; EnerVerse; FLaRe; Beyond Sight;<br>Universal Actions; RoboHorizon; VLA-Cache; Forethought VLA; GRAPE; HAMSTER; TempoRep VLA;<br>ConRFT; RoboBERT; Diffusion Transformer Policy; GEVRM; SoFar; ARM4R; Magma; An Atomic Skill<br>Library; VLAS; SafeVLA; iRe-VLA; TraceVLA; RevLA; RoboMamba; A3VLM; SVLR; 3D-VLA; HybridVLA;<br>SpatialVLA; OE-VLA; EF-VLA; RoboBrain; PerAct; SayCan; CLIP-RT; VLATest; HiRT; A3VLM; SVLR;<br>Bi-VLA; QUAR-VLA; 3D-VLA; RoboMM; Shake-VLA; MORE; DexGraspVLA; DexVLA; Humanoid-VLA;<br>ObjectVLA; Gemini Robotics; ECoT; OTTER; _𝜋_-0.5; OneTwoVLA; Helix; OE-VLA; SmolVLA; EF-VLA;<br>PD-VLA; LeVERB; TLA; Interleave-VLA; iRe-VLA; TraceVLA; VLATest; OpenVLA-OFT; Edge VLA;<br>CoVLA; RoboMM; RoboBERT; Diffusion Transformer Policy; GEVRM; SoFar; ARM4R; Magma; An<br>Atomic Skill Library; VLAS; ChatVLA; RoboBrain; SafeVLA; Diffusion-VLA|
|**Autonomous Mobility**|NaVILA; Mobility VLA; Uni-NaVid; COVLA; OpenDrive VLA; ORION; UAV-VLA; CognitiveDrone|
|**Human Assistance and Interaction**|RoboNurse-VLA; ObjectVLA; RoboMM; Interleave-VLA; ChatVLA|
|**Robotic Platforms**|QUAR-VLA; MORE; LeVERB; Humanoid-VLA; GR00T N1; Helix|
|**Virtual Environments**|ShowUI-2B; Combat VLA; JARVIS-VLA; VLATest|
|**Edge and Low-Power Deployment**|Edge VLA; SmolVLA; Gemini Robotics On-Device; FAST (Pi-0 Fast); NORA; PD-VLA|


**Table 5** 

Table summarizes the evaluation of ten leading VLA models selected based on manipulation capabilities and task generalization. 

|**Model**|**Benchmark Datasets**|**Success**<br>**Rate**|**Zero-Shot**|**Real-**<br>**Robot**|**Notable Results**|
|---|---|---|---|---|---|
|RT-2|Open X-Embodiment, BridgeData<br>V2|High|High|✔|Outperforms RT-1 and SayCan on gener-<br>alization and zero-shot; strong multi-robot,<br>internet-pretrained transfer.|
|Octo|RLBench, Open X-Embodiment|Medium|Medium|✔|First<br>diffusion-based<br>generalist<br>trained<br>on<br>4M+ trajectories across 22 robots; robust sim-<br>to-real.|
|OpenVLA|Open X-Embodiment, DROID|Medium|Medium|✔|LoRA fine-tuned, open-source VLA; competi-<br>tive success with minimal tuning.|
|Gato|Internal multi-task dataset|Medium|Medium|✔|Unified<br>policy<br>for<br>vision,<br>language,<br>and<br>robotics; real-robot zero-shot transfer.|
|Pi-0|Pi-Cross-Embodiment|Medium|Medium|✔|200Hz+ low-latency control; generalizes to<br>new embodiments and setups.|
|DexVLA|RT-X, RLBench|Medium|Medium|✔|Plug-in diffusion experts; cross-embodiment<br>adaptation without fine-tuning.|
|CLIPort|Ravens pick-and-place suite|Medium|Low|✔|CLIP-based dense transport achieves state-of-<br>the-art on tabletop tasks.|
|RoboAgent|RoboSet|High|High|✔|CVAE action-chunking, semantic augmenta-<br>tion; strong real-world generalization.|
|VIMA|VIMA dataset|Medium|Medium|✔|Prompt-based multimodal transformer; com-<br>positional generalization, real-robot demos.|
|TLA|TLA benchmark|Medium|High|✔|First language-tactile VLA; achieves 85%+<br>success on contact-rich tasks.|


and stacking, all within a unified model and with real-robot demos. RoboAgent advances action decomposition and semantic augmentation for real-world manipulation, achieving high success in real kitchen settings. OpenVLA offers a LoRA-tuned, open-source alternative to RT-2, matching competitive performance with lower tuning overhead and real-robot support. Octo introduced the use of diffusionbased policies at scale, training on over 4 million trajectories across 22 robot platforms and achieving robust sim-to-real transfer. DexVLA uses plug-in diffusion experts to rapidly adapt across different embodiments without task-specific fine-tuning. TLA introduces the first language-tactile model, reaching over 85% success in challenging tasks that involve a lot of contact. Gato established a unified token-based policy 

that spans vision, language, and robotic control, with strong zero-shot transfer on real robots. 

Together, these models illustrate two main trajectories in the VLA field. On the one hand are large generalist architectures such as RT-2, Octo, Gato, and OpenVLA which use massive transformer-based backbones and diffusion decoders trained on millions of diverse trajectories. These excel in broad zero-shot generalization and are effective in many tasks and robots. On the other hand, modular and task-specialized systems, such as DexVLA, CLIPort, TLA, and RoboAgent, use targeted modules (e.g., objectcentric ViTs, tactile encoders, LoRA adapters, and semantic augmentation) to enhance robustness and data efficiency for specific manipulation skills. This division demonstrates that while scaling and pretraining bring broad generalization, 

Page 20 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

specialized pipelines remain critical for bridging sim-to-real gaps and achieving high-precision real-world performance. 

# **8. Challenges and Future Directions** 

This section presents open challenges and future directions essential to advancing VLA models. We categorize these into three interconnected domains: Architectural Challenges, Dataset Challenges, and Simulation Challenges. Addressing these challenges will be essential to develop robust and generalizable robotic autonomy. 

## **8.1. Architectural Challenges** 

VLA models rely on a unified Transformer backbone to process high-resolution images or video frames alongside natural-language instructions and output platform-specific action commands. This end-to-end approach exposes several core architectural challenges that arise from the heterogeneity, scale, and physical diversity inherent to robotic control. 

_1. Tokenization and Vocabulary Alignment:_ VLA models must process heterogeneous inputs including natural language, image patches, and continuous robot states, however standard techniques such as byte-pair encoding (BPE) for text and fixed patch embeddings for vision often fail to capture the complexities of visual and proprioceptive signals. This misalignment results in inconsistent token distributions and degraded cross-modal attention. To address this, recent approaches have introduced unified tokenization schemes. Perceiver IO uses shared latent arrays for multimodal fusion (Jaegle et al., 2022), BLIP-2 introduces a Q-former to dynamically select vision tokens compatible with language models (Li et al., 2023), and adapter-based quantization layers allow flexible discretization within each modality stream (Pfeiffer et al., 2020). Despite these advances, several key challenges remain, such as efficiently encoding highdimensional sensor streams without information loss, dynamically adapting vocabularies in the presence of noise or novel configurations, achieving low-latency token generation on resource-constrained platforms, and designing interpretable token spaces to support transparent and reliable cross-modal reasoning. 

_2. Modality Fusion:_ Simply concatenating visual and linguistic features or applying basic cross-attention often fails to align the distinct statistical properties of pixellevel and word-level representations, resulting in weak visual grounding. Recent advances adopt an "align-thenfuse" paradigm to strengthen cross-modal representations. For instance, align-before-fusing employs momentum-based contrastive learning to pre-align vision and language modalities (Li et al., 2022), and VLMo introduces multimodal expert layers within Transformer blocks to adaptively balance contributions from each stream (Wang et al., 2022). Despite these gains, key challenges remain: effectively fusing asynchronous sensory streams like haptics or audio; incorporating additional modalities such as force/torque signals; dynamically reweighting modality importance under 

domain shift (e.g., lighting changes or ambiguous language); improving interpretability of cross-attention layers for debugging; and enabling low-latency, resource efficient fusion for deployment on embedded robotic platforms. 

_3. Generalization Across Embodiments:_ Fixed action vocabularies and rigid kinematic bindings severely limit the ability of VLA models to transfer across different robot models. Recent approaches address this by conditioning action generation on robot-specific descriptors or learned affordance models. For example, PaLM-E encodes explicit hardware embeddings to adapt vision-language reasoning to new platforms (Driess et al., 2023), while RT-2 freezes its visionlanguage planning module and delegates embodiment/modelspecific control to a lightweight action adapter. More recent efforts, such as DexVLA, go further by enabling plug-andplay cross-embodiment adaptation using diffusion-based expert modules trained across diverse kinematic structures. Despite these advances, zero-shot generalization to entirely novel robot models, payload distributions, or joint limits continues to degrade without fine-tuning. Moreover, simto-real transfer remains unstable under noisy sensor readings and unexpected dynamics, and generating smooth, compliant trajectories that adapt to varying torque, speed, and stiffness profiles across platforms remains an open and critical challenge. 

_4. Manipulator Motion Smoothness:_ Although many VLA models emphasize the prediction of discrete action tokens, they often neglect the quality of continuous motion trajectories, which are essential for smooth, safe and precise manipulation. Recent approaches such as Diffusion Policy (Chi et al., 2023b) reformulate visuomotor control as a conditional denoising process, enabling the generation of temporally coherent action sequences. Based on this, the diffusion transformer policy (Hou et al., 2024b) integrates large transformer architectures directly into the diffusion framework, achieving improved stability and generalization across diverse robotic platforms. However, several challenges remain unresolved: achieving real-time inference with latencysensitive diffusion models, ensuring robust collision avoidance under sensor noise and dynamic uncertainty, maintaining a balance between trajectory smoothness and fast reactivity to changing goals, coupling diffusion-based controllers with high-level language planners. 

## **8.2. Dataset Challenges** 

Comprehensive, varied, and well-organized datasets form the basis for developing VLA models. However, current data sets exhibit several significant limitations that obstruct the path toward robust, general-purpose VLA models. 

_1. Task Diversity:_ Current datasets are highly specialized, focusing on narrow, short-horizon tasks. For instance, ALFRED and CALVIN emphasize pick-and-place operations, while R2R focuses on navigation and finding pathways 

Page 21 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

guided by language. However, few datasets integrate longhorizon task planning that combines spatial reasoning, navigation, and fine-grained object manipulation in open-ended, multi-scene environments. This fragmentation restrains the training of agents capable of seamlessly switching between locomotion and manipulation tasks in realistic household or industrial scenarios. 

_2. Modality Imbalance:_ Most VLA datasets primarily offer RGB images and textual annotations, often excluding critical sensor modalities such as depth maps, force/torque signals, tactile feedback, or proprioceptive data. When these streams are present, they are frequently captured at inconsistent sampling rates or resolutions. This lack of highquality, synchronized multimodal data significantly limits the development of models that can perform robust sensor fusion despite environmental uncertainty. 

_3. Annotation Quality and Cost:_ Obtaining accurate labels such as 6-DoF object poses, frame-aligned multi-sensor data, or detailed natural language explanations is resource intensive and time-consuming, requiring either detailed manual annotation or unreliable semi-automated pipelines. Although simulated environments can provide perfect annotations at scale, domain gaps in appearance, physics, and interaction fidelity often degrade sim-to-real transfer. Meanwhile, current self-supervised and auto-labeling methods remain unreliable across diverse task domains. 

_4. Realism and Scale:_ Real-world datasets like Open X- Embodiment offer high fidelity data with authentic sensor noise and physical interactions, but are constrained by the cost and time of robot data collection, typically producing only hundreds of hours of recordings. In contrast, simulation platforms can generate millions of trajectories efficiently but struggle to replicate complex real-world dynamics, such as material deformation, lighting variability, or occlusion effects. This trade-off between realism and scalability remains a fundamental bottleneck in the development of models that generalize beyond laboratory conditions. 

Addressing these limitations will require coordinated efforts to build long-horizon, cross-domain benchmarks; gather richly synchronized multimodal datasets; reduce annotation costs through self-supervision and automation; and bridge the realism-scale divide via hybrid simulation-real data pipelines. These advances are essential to equip future VLA models with the robustness and adaptability needed for deployment in real-world environments. 

## **8.3. Simulation Challenges** 

Simulators provide scalable, controllable environments for generating training data for VLA models. However, several critical limitations must be addressed to ensure that simulated performance reliably transfers to real-world deployment. 

_1. Physics Accuracy and Contact Modeling:_ Popular physics engines such as MuJoCo, PyBullet, and NVIDIA 

Isaac Sim simplify physical interactions by relying on basic Coulomb friction models and point-contact approximations. Although this enables stable and fast simulation, it fails to capture essential dynamics such as soft-body deformation, variable surface friction, and joint compliance. As a result, policies trained in simulation often perform poorly in the real world, leading to issues like object slip, unexpected torque spikes, or unstable contact behavior. 

_2. Visual Realism and Throughput Trade-offs:_ Highfidelity simulation platforms such as AI2-THOR, Habitat, and Unity ML-Agents provide photorealistic rendering and diverse assets, making them ideal for vision-heavy tasks. However, this comes at the cost of low frame rates and high GPU demand, limiting their suitability for large-scale reinforcement learning or self-supervised pretraining. In contrast, lightweight renderers support high-throughput simulation but suffer from domain gaps in texture, lighting, and occlusion realism, reducing the effectiveness of domainrandomized policies during real-world deployment. 

_3. Lack of Built-in Language Grounding APIs:_ Most simulators do not provide native support for grounding natural language commands into agent behaviors. This forces to create custom annotation pipelines such as those used in ALFRED or TEACh that align textual instructions with actions and scene representations. These efforts introduce significant development overhead, restrict reproducibility, and lead to fragmented and non-standardized data formats. 

_4. Multi-Robot and Agent Support Capabilities:_ Support for multiple robots varies widely across simulators. Some platforms like Isaac Sim and Gazebo offer flexible import of arbitrary robot descriptions via URDF or SDF formats, facilitating multi-robot coordination and benchmarking. Others, like Webots and RoboSuite, are optimized for specific robot families, limiting generalization and reusability. This inconsistency complicates cross-platform pretraining and impairs reproducibility across hardware setups. 

Overcoming these challenges requires advancing contactrich physics modeling, optimizing rendering pipelines for both fidelity and throughput, developing standardized language grounding interfaces, and unifying multi-agent simulation support. These improvements are essential to create simulation platforms that can produce realistic, scalable, and transferable datasets for training generalizable VLA models. 

## **8.4. Future Directions** 

To advance the next generation of VLA models, future systems should incorporate learnable, modality-aware tokenizers-such as vector-quantized VAEs or neural dictionaries to jointly discretize continuous sensor streams like proprioception and force/torque alongside visual and textual inputs. Dynamic fusion blocks (e.g., gating networks, mixture-of-experts, or conditional attention) can reweight each modality based on task demands, improving flexibility and robustness. For scaling long video or text sequences, hierarchical architectures are recommended, where 

Page 22 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

lightweight CNN or RNN frontends downsample highframe-rate inputs before passing them to sparse Transformer layers for efficient long-range modeling. Additionally, integrating diffusion-based trajectory generators with differentiable safety and collision-avoidance filters can produce smooth, compliant motions that align tightly with high-level task planning. 

On the dataset side, procedural task grammars embedded in simulators can automatically generate long-horizon, open-ended scenarios that interleave navigation and finegrained manipulation. To support sensor fusion, standardized multimodal capture pipelines should be adopted to synchronize RGB-D, tactile, force/torque, audio, and language streams at compatible sampling rates, with missing modalities augmented through cross-modal synthesis (e.g., monocular depth estimation). Annotation burdens can be reduced through self-supervised or weakly supervised techniques, including unsupervised segmentation, visionlanguage co-training, and active learning, to automatically extract object masks, 6-DoF trajectories, and language explanations. Hybrid synthetic-real pipelines, using neural rendering and physics-aware domain randomization, can bridge the realism-scale gap, ensuring that large-scale simulated data generalize better to physical environments. 

In simulation platforms, physics fidelity should be improved through differentiable, multi-scale contact models that blend classical solvers with data-driven calibration to better handle soft-body deformation, friction variability, and compliance. Hybrid rendering pipelines that combine highthroughput rasterization for general frames with neural or ray-traced rendering for key scenes can deliver realism without compromising speed. A simulator-agnostic language grounding API should be established to map natural language instructions directly to scene graphs and agent behaviors. Finally, to enable broad generalization, simulators must support multi-robot and multi-agent scenarios, with autoimport of URDF/SDF models and shared simulation protocols, allowing for consistent policy pretraining across heterogeneous robot platforms. 

# **9. Conclusion** 

VLA models are transforming the operational scope of robotic agents by tightly coupling perception, language, and action through integrated learning strategies. This review has systematically organized the current VLA landscape across four key dimensions: architectural design, dataset ecosystems, simulation platforms, and evaluation methodologies. The analysis reveals a rapid evolution toward multimodal, instruction conditioned agents capable of generalizing across tasks, embodiments, and environments. While significant progress has been made, the field continues to face critical challenges in achieving scalable pretraining, reliable transfer from simulation to physical environments, and 

transparent decision making in safety critical contexts. Addressing these limitations will require advancements in composable learning systems, data efficient adaptation strategies, and standardized procedures for benchmarking and deployment. The future of VLA research lies in bridging foundational models with real world applications, enabling agents that can reason, act, and adapt in complex, open ended settings. This review contributes to that trajectory by synthesizing core architectural principles, learning paradigms, and deployment infrastructures, while outlining open problems that can shape the development of the next generation of vision language grounded robotic intelligence. 

# **Declaration** 

Declaration of generative AI and AI-assisted technologies in the writing process. 

During the preparation of this work the author(s) used ChatGPT in order to refine the English and to search the names of the VLA models. After using this tool/service, the author(s) reviewed and edited the content as needed and take(s) full responsibility for the content of the publication. 

# **References** 

Abdel-Hamid, A., Mahmoud, K., et al., 2024. Image captioning transformers: A comprehensive review. Artificial Intelligence Review doi:10. 1007/s10462-024-10560-w. early access. 

- Ahn, M., Brohan, A., Brown, N., et al., 2022. Do as i can, not as i say: Grounding language in robotic affordances. arXiv preprint arXiv:2204.01691 . 

- Anderson, P., Wu, Q., Teney, D., Bruce, J., Johnson, M., SÃĳnderhauf, N., Reid, I., Gould, S., van den Hengel, A., 2018. Vision-and-language navigation: Interpreting visually-grounded navigation instructions in real environments, in: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 

- Arai, H., Miwa, K., Sasaki, K., Watanabe, K., Yamaguchi, Y., Aoki, S., Yamamoto, I., 2025. Covla: Comprehensive vision-language-action dataset for autonomous driving. 2025 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), IEEE , 1933–1943. 

- Arai, H., Miwa, K., Sasaki, K., Yamaguchi, Y., Watanabe, K., Aoki, S., Yamamoto, I., 2024. Covla: Comprehensive vision-languageaction dataset for autonomous driving URL: https://arxiv.org/abs/ 2408.10845, arXiv:2408.10845. 

- Assran, M., Bardes, A., Fan, D., Garrido, Q., Howes, R., Muckley, M., Rizvi, A., Roberts, C., Sinha, K., Zholus, A., et al., 2025. V-jepa 2: Selfsupervised video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985 . 

- authors, A., 2025. Ef-vla: Vision-language-action models with aligned vision language features for better generalization. Under review at ICLR 2025 URL: https://openreview.net/forum?id=8512. preprint under double-blind review. 

- Bharadhwaj, H., Pore, N., Liang, J., Singh, J., Rao, K., Zeng, A., Gopalakrishnan, K., 2023. Roboagent: Generalist robot agent with semantic and temporal understanding. arXiv preprint arXiv:2310.08560 URL: https://robopen.github.io/media/roboagent.pdf. 

- Bjorck, J., Castañeda, F., Cherniadev, N., Da, X., Ding, R., Fan, L., Fang, Y., Fox, D., Hu, F., Huang, S., et al., 2025. Gr00t n1: An open foundation model for generalist humanoid robots. arXiv preprint arXiv:2503.14734 

- Black, K., Brown, N., Darpinian, J., Dhabalia, K., Driess, D., Esmail, A., Equi, M., et al., 2025. _𝜋_ -0.5:: A vision-language-action model with open-world generalization. arXiv preprint arXiv:2504.16054 URL: https://arxiv.org/abs/2504.16054. 

Page 23 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al., 2024a. Pi-0: A visionlanguage-action flow model for general robot control. arXiv preprint arXiv:2410.24164 . 

- Black, K., Brown, N., Driess, D., Esmail, A., Equi, M., Finn, C., Fusai, N., Groom, L., Hausman, K., Ichter, B., et al., 2024b. _𝑝𝑖_ _0: A visionlanguage-action flow model for general robot control. arXiv preprint arXiv:2410.24164 . 

- Brandišauskas, M., Å¡ukauskas, M., Krizhanovsky, A., 2023. Seq2code: Encoder-decoder model for program synthesis. Procedia Computer Science 222, 1441–1450. doi:10.1016/j.procs.2023.11.306. 

- Brohan, A., Brown, N., Carbajal, J., Chebotar, Y., Dabis, J., Finn, C., Gopalakrishnan, K., Hausman, K., Herzog, A., Hsu, J., et al., 2022. Rt1: Robotics transformer for real-world control at scale. arXiv preprint arXiv:2212.06817 . 

- Brown, T.B., Mann, B., Ryder, N., et al., 2020. Language models are fewshot learners. Advances in Neural Information Processing Systems 33, 1877–1901. 

- Bu, Q., Cai, J., Chen, L., Cui, X., Ding, Y., Feng, S., Gao, S., He, X., Hu, X., Huang, X., et al., 2025. Agibot world colosseo: A large-scale manipulation platform for scalable and intelligent embodied systems. arXiv preprint arXiv:2503.06669 . 

- Budzianowski, P., Maa, W., Freed, M., Mo, J., Xie, A., Tipnis, V., Bolte, B., 2024. Edgevla: Efficient vision-language-action models. environments 20, 3. 

- Caron, M., Touvron, H., Cord, M., Douze, M., Massa, F., Sablayrolles, A., Jégou, H., 2021. Emerging properties in self-supervised vision transformers, in: ICCV. 

- Chen, P., Bu, P., Wang, Y., Wang, X., Wang, Z., Guo, J., Zhao, Y., Zhu, Q., Song, J., Yang, S., et al., 2025a. Combatvla: An efficient visionlanguage-action model for combat tasks in 3d action role-playing games. arXiv preprint arXiv:2503.09527 . 

- Chen, X., et al., 2024. Quar-vla: A vision-language-action model for quadruped robots. arXiv preprint arXiv:2310.08532 . 

- Chen, Y., Tian, S., Liu, S., Zhou, Y., Li, H., Zhao, D., 2025b. Conrft: A reinforced fine-tuning method for vla models via consistency policy. arXiv preprint arXiv:2502.05450 . 

- Chen, Z., Huo, J., Chen, Y., Gao, Y., 2025c. Robohorizon: An llm-assisted multi-view world model for long-horizon robotic manipulation. arXiv preprint arXiv:2501.06605 . 

- Cheng, A., Ji, Y., Yang, Z., Gongye, Z., Zou, X., Kautz, J., BÄśyÄśk, E., Yin, H., Liu, S., Wang, X., 2024. Navila: Legged robot vision-languageaction model for navigation. arXiv preprint arXiv:2412.04453 . 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S., 2023a. Diffusion policy: Visuomotor policy learning via action diffusion. The International Journal of Robotics Research 02783649241273668. 

- Chi, C., Xu, Z., Feng, S., Cousineau, E., Du, Y., Burchfiel, B., Tedrake, R., Song, S., 2023b. Diffusion policy: Visuomotor policy learning via action diffusion. arXiv preprint arXiv:2303.04137 . 

- Chiang, H., Xu, Z., Fu, Z., Jacob, M., Zhang, T., Lee, T., Yu, W., Schenck, C., Rendleman, D., Shah, D., et al., 2024. Mobility vla: Multimodal instruction navigation with long-context vims and topological graphs. arXiv preprint arXiv:2407.07775 . 

- Chowdhery, A., Narang, S., Devlin, J., Bosma, M., Mishra, G., Roberts, A., Barham, P., Chung, H.W., Sutton, C., Sepassi, R., Gehrmann, S., Elsen, E., Patrick, D., Mishkin, P., 2022. Palm: Scaling language modeling with pathways. arXiv preprint arXiv:2204.02311 . 

- Collaboration, E., O’Neill, A., Rehman, A., Gupta, A., Maddukuri, A., Gupta, A., Padalkar, A., Lee, A., et al., A.P., 2025. Open x-embodiment: Robotic learning datasets and rt-x models. URL: https://arxiv.org/abs/ 2310.08864, arXiv:2310.08864. 

- Coumans, E., Bai, Y., 2016. Pybullet, a python module for physics simulation for robotics, games and machine learning. https://pybullet.org. 

- Das, A., Datta, S., Gkioxari, G., Lee, S., Parikh, D., Batra, D., 2018. Embodied question answering, in: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR). 

- Deng, J., Dong, W., Socher, R., Li, L.J., Li, K., Fei-Fei, L., 2009. Imagenet: A large-scale hierarchical image database. 2009 IEEE Conference on Computer Vision and Pattern Recognition (CVPR) , 248–255URL: https://doi.org/10.1109/CVPR.2009.5206848, doi:10. 1109/CVPR.2009.5206848. 

- Devlin, J., Chang, M.W., Lee, K., Toutanova, K., 2018. Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805 . 

- Dey, S., Zaech, J., Nikolov, N., Van Gool, L., Paudel, D., 2024. Revla: Reverting visual domain limitation of robotic foundation models. arXiv preprint arXiv:2409.15250 . 

- Ding, P., Ma, J., Tong, X., Zou, B., Luo, X., Fan, Y., Wang, T., Lu, H., Mo, P., Liu, J., et al., 2025. Humanoid-vla: Towards universal humanoid control with visual integration. arXiv preprint arXiv:2502.14795 . 

- Ding, P., Zhao, H., Zhang, W., Song, W., Zhang, M., Huang, S., Yang, N., Wang, D., 2024. Quar-vla: Vision-language-action model for quadruped robots. European Conference on Computer Vision, Springer , 352–367. 

- Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., Houlsby, N., 2021. An image is worth 16x16 words: Transformers for image recognition at scale, in: International Conference on Learning Representations (ICLR). URL: https://arxiv.org/abs/2010. 11929. 

- Dosovitskiy, A., Beyer, L., Kolesnikov, A., et al., 2020. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929 . 

- Driess, D., Ruiz, N., Goyal, K., Chebotar, Y., Irpan, A., Ailon, X., Levine, S., Finn, C., 2023. Palm-e: An embodied multimodal language model. arXiv preprint arXiv:2303.03378 . 

- Driess, D., Springenberg, J.T., Ichter, B., Yu, L., Li-Bell, A., Pertsch, K., Ren, A.Z., Walke, H., Vuong, Q., Shi, L.X., et al., 2025. Knowledge insulating vision-language-action models: Train fast, run fast, generalize better. arXiv preprint arXiv:2505.23705 . 

- Driess, D., et al., 2024. Openvla: Open-source vision-language-action models for robotics. arXiv preprint arXiv:2406.09246 . 

- Fan, C., Jia, X., Sun, Y., Wang, Y., Wei, J., Gong, Z., Zhao, X., Tomizuka, M., Yang, X., Yan, J., Ding, M., 2025. Interleave-vla: Enhancing robot manipulation with interleaved image-text instructions. arXiv preprint arXiv:2406.07000 URL: https://arxiv.org/abs/2406.07000. 

- Fang, H., Grotz, M., Pumacay, W., Wang, Y.R., Fox, D., Krishna, R., Duan, J., 2025. Sam2act: Integrating visual foundation model with a memory architecture for robotic manipulation. arXiv preprint arXiv:2501.18564 

- Fouad, S., et al., 2024. Image captioning using deep learning: A comprehensive review and future perspectives. Multimedia Tools and Applications doi:10.1007/s11042-024-17234-3. 

- Fu, H., Zhang, D., Zhao, Z., Cui, J., Liang, D., Zhang, C., Zhang, D., Xie, H., Wang, B., Bai, X., 2025. Orion: A holistic end-to-end autonomous driving framework by vision-language instructed action generation. arXiv preprint arXiv:2503.19755 . 

- Gao, X., Gao, Q., Gong, R., Lin, K., Thattai, G., Sukhatme, G.S., 2022a. DialFRED: Dialogue-Enabled Agents for Embodied Instruction Following. IEEE Robotics and Automation Letters 7, 10049–10056. doi:10. 1109/LRA.2022.3193254. 

- Gao, X., Gao, Q., Gong, R., Lin, K., Thattai, G., Sukhatme, G.S., 2022b. Dialfred: Dialogue-enabled agents for embodied instruction following. IEEE Robotics and Automation Letters 7, 10049âĂŞ10056. URL: http: //dx.doi.org/10.1109/LRA.2022.3193254, doi:10.1109/lra.2022.3193254. 

- Gbagbe, K.F., Cabrera, M.A., Alabbas, A., Alyunes, O., Lykov, A., Tsetserukou, D., 2024. Bi-vla: Vision-language-action model-based system for bimanual robotic dexterous manipulations. arXiv preprint arXiv:2405.06039 URL: https://arxiv.org/abs/2405.06039. 

- Ghojogh, B., Ghodsi, A., Karray, F., Crowley, M., 2024. Attention mechanism in machine learning: A survey. arXiv preprint arXiv:2402.05310 URL: https://arxiv.org/abs/2402.05310. 

- Grauman, K., Westbury, A., Byrne, E., Chavis, Z., Furnari, A., et al., R.G., 2022. Ego4d: Around the world in 3,000 hours of egocentric video URL: https://arxiv.org/abs/2110.07058, arXiv:2110.07058. 

Page 24 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

- Gu, J., Kirmani, S., Wohlhart, P., Lu, Y., Arenas, M.G., Rao, K., Yu, W., Fu, C., Gopalakrishnan, K., Xu, Z., et al., 2023. Robotic task generalization via hindsight trajectory sketches. arXiv preprint arXiv:2311.01977 URL: https://arxiv.org/abs/2311.01977. 

- Guo, Y., Zhang, J., Chen, X., Ji, X., Wang, Y.J., Hu, Y., Chen, J., 2025. irevla: Improving vision-language-action model with online reinforcement learning. arXiv preprint arXiv:2501.16664 URL: https://arxiv.org/ abs/2501.16664. 

- Guruprasad, P., Sikka, H., Song, J., Wang, Y., Liang, P.P., 2024. Benchmarking vision, language, & action models on robotic learning tasks. arXiv preprint arXiv:2411.05821 . 

- Han, S., Qiu, B., Liao, Y., Huang, S., Gao, C., Yan, S., Liu, S., 2025. Robocerebra: A large-scale benchmark for long-horizon robotic manipulation evaluation. arXiv preprint arXiv:2506.06677 . 

- Hao, P., Zhang, C., Li, D., Cao, X., Hao, X., Cui, S., Wang, S., 2025. Tla: Tactile-language-action model for contact-rich manipulation. arXiv preprint arXiv:2503.08548 URL: https://arxiv.org/abs/2503.08548. 

- He, Y., Weilbach, C.D., Wojciechowska, M.E., Zhang, Y., Wood, F., 2025. Plaicraft: Large-scale time-aligned vision-speech-action dataset for embodied ai. URL: https://arxiv.org/abs/2505.12707, arXiv:2505.12707. 

- Hou, Z., Zhang, T., Xiong, Y., Pu, H., Zhao, C., Tong, R., Qiao, Y., Dai, J., Chen, Y., 2024a. Diffusion transformer policy. arXiv preprint arXiv:2410.15959 . 

- Hou, Z., Zhang, T., Xiong, Y., Pu, H., Zhao, C., Tong, R., Qiao, Y., Dai, J., Chen, Y., 2024b. Diffusion transformer policy: Scaling diffusion transformer for generalist visionâĂŞlanguageâĂŞaction learning. arXiv preprint arXiv:2410.15959 . 

- Hu, J., Hendrix, R., Farhadi, A., Kembhavi, A., Martín-Martín, R., Stone, P., Zeng, K.H., Ehsani, K., 2024. Flare: Achieving masterful and adaptive robot policies with large-scale reinforcement learning fine-tuning. arXiv preprint arXiv:2409.16578 . 

- Huang, H., Liu, F., Fu, L., Wu, T., Mukadam, M., Malik, J., Goldberg, K., Abbeel, P., 2025a. Otter: A vision-language-action model with textaware visual feature extraction. arXiv preprint arXiv:2503.03734 URL: https://arxiv.org/abs/2503.03734. 

- Huang, S., Chang, H., Liu, Y., Zhu, Y., Dong, H., Boularias, A., Gao, P., Li, H., 2024. A3vlm: Actionable articulation-aware vision language model, in: Proceedings of the 8th Conference on Robot Learning (CoRL). URL: https://arxiv.org/abs/2405.06039. 

- Huang, S., Chen, L., Zhou, P., Chen, S., Jiang, Z., Hu, Y., Liao, Y., Gao, P., Li, H., Yao, M., et al., 2025b. Enerverse: Envisioning embodied future space for robotics manipulation. arXiv preprint arXiv:2501.01895 . 

- Huang, W., Wang, C., Zhang, R., Li, Y., Wu, J., Fei-Fei, L., 2023. Voxposer: Composable 3d value maps for robotic manipulation with language models. arXiv preprint arXiv:2307.05973 . 

- Hung, C., Sun, Q., Hong, P., Zadeh, A., Li, C., Tan, U., Majumder, N., Poria, S., et al., 2025. Nora: A small open-sourced generalist vision language action model for embodied tasks. arXiv preprint arXiv:2504.19854 . 

- Jaegle, A., Gimeno, N., Brock, A., Zisserman, A., Carreira, J., Vinyals, O., Verdegaal, R., Pessoa, P., Nowozin, S., 2022. Perceiver IO: A general architecture for structured inputs & outputs, in: International Conference on Learning Representations (ICLR). 

- James, S., Ma, Z., Arrojo, D.R., Davison, A.J., 2020. Rlbench: The robot learning benchmark & learning environment. IEEE Robotics and Automation Letters 5, 3019–3026. doi:10.1109/LRA.2020.2972831. 

- Ji, Y., Tan, H., Shi, J., Hao, X., Zhang, Y., Zhang, H., Wang, P., Zhao, M., Mu, Y., An, P., et al., 2025. Robobrain: A unified brain model for robotic manipulation from abstract to concrete, in: Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 1724–1734. 

- Jiang, S., Li, H., Ren, R., Zhou, Y., Wang, Z., He, B., 2025. Kaiwu: A multimodal manipulation dataset and framework for robot learning and human-robot interaction. URL: https://arxiv.org/abs/2503.05231, arXiv:2503.05231. 

- Jiang, Y., Gupta, A., Zhang, Z., et al., 2022. Vima: General robot manipulation with multimodal prompts. arXiv preprint arXiv:2210.03094 . 

- Jones, J., Mees, O., Sferrazza, C., Stachowicz, K., Abbeel, P., Levine, S., 2025. Beyond sight: Finetuning generalist robot policies with heterogeneous sensors via language grounding. arXiv preprint arXiv:2501.04693 . 

- Juliani, A., Berges, V., Teng, E., Gao, Y., Henry, H., Mattar, M., Lange, D., 2018. Unity: A general platform for intelligent agents, in: Proceedings of the 1st Annual Conference on Robot Learning (CoRL), pp. 49–60. 

- Kang, G.C., Kim, J., Shim, K., Lee, J.K., Zhang, B.T., 2024. Clip-rt: Learning language-conditioned robotic policies from natural language supervision. arXiv preprint arXiv:2411.00508 . 

- Kang, G.C., Kim, J., Shim, K., Lee, J.K., Zhang, B.T., 2025. Clip-rt: Learning language-conditioned robotic policies from natural language supervision, in: Proceedings of Robotics: Science and Systems (RSS). 

- Khan, M., Asfaw, S., Iarchuk, D., Cabrera, M., Moreno, L., Tokmurziyev, I., Tsetserukou, D., 2025. Shake-vla: Vision-language-action model-based system for bimanual robotic manipulations and liquid mixing. arXiv preprint arXiv:2501.06919 . 

- Khazatsky, A.e.a., 2024. Droid: A large-scale in-the-wild robot manipulation dataset, in: Robotics: Science and Systems (RSS). URL: https: //droid-dataset.github.io/. 

- Kim, M., Finn, C., Liang, P., 2025. Fine-tuning vision-languageaction models: Optimizing speed and success. arXiv preprint arXiv:2502.19645 . 

- Kim, M., Pertsch, K., Karamcheti, S., Xiao, T., Balakrishna, A., Nair, S., Rafailov, R., Foster, E., Lam, G., Sanketi, P., et al., 2024. Openvla: An open-source vision-language-action model. arXiv preprint arXiv:2406.09246 . 

- Koenig, N., Howard, A., 2004. Design and use paradigms for gazebo, an open-source multi-robot simulator, in: 2004 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), IEEE. pp. 2149– 2154. 

- Kolve, E., Mottaghi, R., Han, W., Randhavane, T., Zheng, X., Li, Y., Gupta, A., Farhadi, A., 2017. AI2-THOR: An interactive 3d environment for visual ai, in: Proceedings of the 1st Annual Conference on Robot Learning (CoRL). URL: https://ai2thor.allenai.org. 

- Krantz, J., Wijmans, E., Mukhopadhyay, A., Lee, S., Chernova, S., Batra, D., 2020. Beyond the nav-graph: Vision-and-language navigation in continuous environments, in: Proceedings of the European Conference on Computer Vision (ECCV), Springer. pp. 104–120. URL: https: //arxiv.org/abs/2004.07787, doi:10.1007/978-3-030-58568-6_7. 

- Lam, C., Wang, X., Lu, X., Yao, Y., Yang, M.H., 2023. Deep learning with vision transformers: A survey. IEEE Transactions on Pattern Analysis and Machine Intelligence 45, 13101–13124. doi:10.1109/TPAMI.2023. 3241477. 

- Li, D., Peng, B., Li, C., Qiao, N., Zheng, Q., Sun, L., Qin, Y., Li, B., Luan, Y., Wu, B., et al., 2025a. An atomic skill library construction method for data-efficient embodied manipulation. arXiv preprint arXiv:2501.15068 

- Li, J., Li, X., Li, X., Huang, J., Zhang, J., Wang, L., Dou, Q., Ling, H., 2022. Align before fuse: Vision and language representation learning with momentum distillation, in: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 18713–18723. 

- Li, J., Peng, E.A., Wang, C., Liu, J., Feichtenhofer, C., 2023. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models, in: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pp. 10965–10975. 

- Li, J., Zhu, Y., Tang, Z., Wen, J., Zhu, M., Liu, X., Li, C., Cheng, R., Peng, Y., Feng, F., 2024a. Improving vision-language-action models via chainof-affordance. arXiv preprint arXiv:2412.20451 . 

- Li, M., Wang, Z., He, K., Ma, X., Liang, Y., 2025b. Jarvis-vla: Post-training large-scale vision language models to play visual games with keyboards and mouse. arXiv preprint arXiv:2503.16365 . 

- Li, Q., Liang, Y., Wang, Z., Luo, L., Chen, X., Liao, M., Wei, F., Deng, Y., Xu, S., Zhang, Y., et al., 2024b. Cogact: A foundational visionlanguage-action model for synergizing cognition and action in robotic manipulation. arXiv preprint arXiv:2411.19650 . 

- Li, S., Wang, J., Dai, R., Ma, W., Ng, W., Hu, Y., Li, Z., 2024c. Robonursevla: Robotic scrub nurse system based on vision-language-action model. arXiv preprint arXiv:2409.19590 . 

- Li, Y., Deng, Y., Zhang, J., Jang, J., Memmel, M., Yu, R., Garrett, C.R., Ramos, F., Fox, D., Li, A., et al., 2025c. Hamster: Hierarchical action models for open-world robot manipulation. arXiv preprint arXiv:2502.05485 . 

Page 25 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

- Li, Y., Yan, G., Macaluso, A., Ji, M., Zou, X., Wang, X., 2025d. Integrating lmm planners and 3d skill policies for generalizable manipulation. arXiv preprint arXiv:2501.18733 . 

- Liang, L., Bian, L., Xiao, C., et al., 2023. Robo360: A 3d omnispective multi-material robotic manipulation dataset. arXiv preprint arXiv:2312.06686 . 

- Lin, F., Nai, R., Hu, Y., You, J., Zhao, J., Gao, Y., 2025. Onetwovla: A unified vision-language-action model with adaptive reasoning. arXiv preprint arXiv:2505.11917 URL: https://arxiv.org/abs/2505.11917. 

- Lin, K., Li, L., Gao, D., Yang, Z., Wu, S., Bai, Z., Lei, W., Wang, L., Shou, M., 2024. Showui: One vision-language-action model for gui visual agent. arXiv preprint arXiv:2411.17465 . 

- Liu, B., Zhu, Y., Gao, C., Feng, Y., Liu, Q., Zhu, Y., Stone, P., 2023. Libero: Benchmarking knowledge transfer for lifelong robot learning. Advances in Neural Information Processing Systems 36, 44776–44791. 

- Liu, J., Chen, H., An, P., Liu, Z., Zhang, R., Gu, C., Li, X., Guo, Z., Chen, S., Liu, M., et al., 2025. Hybridvla: Collaborative diffusion and autoregression in a unified vision-language-action model. arXiv preprint arXiv:2503.10631 . 

- Liu, J., Liu, M., Wang, Z., An, P., Li, X., Zhou, K., Yang, S., Zhang, R., Guo, Y., Zhang, S., 2024a. Robomamba: Efficient vision-language-action model for robotic reasoning and manipulation. Advances in Neural Information Processing Systems 37, 40085–40110. 

- Liu, S., Wu, L., Li, B., Tan, H., Chen, H., Wang, Z., Xu, K., Su, H., Zhu, J., 2024b. Rdt-1b: a diffusion foundation model for bimanual manipulation. arXiv preprint arXiv:2410.07864 . 

- Liu, X., Chen, W., Chen, Y., Chen, Y.S., Wang, W.Y., 2021. Pre-train or prompt? exploring the encoder-decoder framework for zero-shot learning. arXiv preprint arXiv:2104.08691 URL: https://arxiv.org/ abs/2104.08691. 

- Lykov, A., Serpiva, V., Khan, M.H., Sautenkov, O., Myshlyaev, A., Tadevosyan, G., Yaqoot, Y., Tsetserukou, D., 2025. Cognitivedrone: A vla model and evaluation benchmark for real-time cognitive task solving and reasoning in uavs. arXiv preprint arXiv:2503.01378 . 

- Makoviychuk, V., Wawrzyniak, L., Rathod, Y., Allshire, A., Handa, A., Müller, J., Widmaier, F., Leal-Taixé, L., Makadia, A., Leutenegger, S., 2021. Isaac gym: High performance gpu based physics simulation for robot learning. arXiv preprint arXiv:2108.10470 URL: https://arxiv. org/abs/2108.10470. 

- Mees, O., Hermann, L., Rosete-Beas, E., Burgard, W., 2022. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. URL: https://arxiv.org/abs/2112.03227, arXiv:2112.03227. 

- Michel, O., 2004. Webots: Professional mobile robot simulation, in: 2004 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), IEEE. pp. 4020–4025. 

- Mishra, A., Mishra, A., Singh, G., et al., 2024. Image transformers: A survey. ACM Computing Surveys In press. 

- Myers, V., Zheng, B.C., Dragan, A., Fang, K., Levine, S., 2025. Temporal representation alignment: Successor features enable emergent compositionality in robot instruction following temporal representation alignment. arXiv preprint arXiv:2502.05454 . 

- Niu, D., Sharma, Y., Xue, H., Biamby, G., Zhang, J., Ji, Z., Darrell, T., Herzig, R., 2025. Pre-training auto-regressive robotic models with 4d representations. arXiv preprint arXiv:2502.13142 . 

- NVIDIA Corporation, . NVIDIA Isaac Sim. https://developer.nvidia. com/isaac-sim. Accessed: 2025-05-18. 

- Padmakumar, A., Thomason, J., Shrivastava, A., Lange, P., Narayan-Chen, A., Gella, S., Piramuthu, R., Tur, G., Hakkani-Tur, D., 2021. Teach: Task-driven embodied agents that chat. URL: https://arxiv.org/abs/ 2110.00534, arXiv:2110.00534. 

- Parada, C., Team, G.R., 2025. Gemini robotics on-device brings ai to local robotic devices. DeepMind Blog. Available at: https://deepmind.google/discover/blog/gemini-robotics-on-devicebrings-ai-to-local-robotic-devices/. 

- Pertsch, K., Stachowicz, K., Ichter, B., Driess, D., Nair, S., Vuong, Q., Mees, O., Finn, C., Levine, S., 2025. Fast: Efficient action tokenization for vision-language-action models. arXiv preprint arXiv:2501.09747 . 

- Pfeiffer, J., Vulic, I., Gurevych, I., 2020. Adapterfusion: Non-destructive task composition for transfer learning, in: Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 4875–4884. 

- Press, O., Wolf, L., 2017. Using the output embedding to improve language models, in: Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics (EACL), pp. 157–163. URL: https://arxiv.org/abs/1608.05859. 

- Qi, Z., Zhang, W., Ding, Y., Dong, R., Yu, X., Li, J., Xu, L., Li, B., He, X., Fan, G., et al., 2025. Sofar: Language-grounded orientation bridges spatial reasoning and object manipulation. arXiv preprint arXiv:2502.13143 . 

- Qu, D., Song, H., Chen, Q., Yao, Y., Ye, X., Ding, Y., Wang, Z., Gu, J., Zhao, B., Wang, D., et al., 2025. Spatialvla: Exploring spatial representations for visual-language-action model. arXiv preprint arXiv:2501.15830 . 

- Radford, A., Kim, J.W., Hallacy, C., et al., 2021. Learning transferable visual models from natural language supervision. arXiv preprint arXiv:2103.00020 . 

- Reed, S., Zolna, K., Parisotto, E., Colmenarejo, S., Novikov, A., BarthMaron, G., Gimenez, M., Sulsky, Y., Kay, J., Springenberg, J., et al., 2022. A generalist agent. arXiv preprint arXiv:2205.06175 . 

- Rohmer, E., Singh, S.P., Freese, M., 2013. V-rep: A versatile and scalable robot simulation framework, in: 2013 IEEE/RSJ international conference on intelligent robots and systems, IEEE. pp. 1321–1326. 

- Samson, M., Muraccioli, B., Kanehiro, F., 2024. Scalable, trainingfree visual language robotics: A modular multi-model framework for consumer-grade gpus. arXiv preprint arXiv:2502.01071 URL: https: //arxiv.org/abs/2502.01071. 

- Sautenkov, O., Yaqoot, Y., Lykov, A., Mustafa, M., Tadevosyan, G., Akhmetkazy, A., Cabrera, M., Martynov, M., Karaf, S., Tsetserukou, D., 2025. Uav-vla: Vision-language-action system for large scale aerial mission generation. arXiv preprint arXiv:2501.05014 . 

- Savva, M., Chang, A.X., Dosovitskiy, A., et al., 2019. Habitat: A platform for embodied ai research. Proceedings of the IEEE/CVF International Conference on Computer Vision , 9339–9347. 

- Shi, L.X., Ichter, B., Equi, M., Ke, L., Pertsch, K., Vuong, Q., Tanner, J., Walling, A., Wang, H., Fusai, N., et al., 2025. Hi robot: Open-ended instruction following with hierarchical vision-language-action models. arXiv preprint arXiv:2502.19417 . 

- Shridhar, M., Manuelli, L., Fox, D., 2022a. Cliport: What and where pathways for robotic manipulation. Conference on robot learning, PMLR , 894–906. 

- Shridhar, M., Manuelli, L., Fox, D., 2022b. Perceiver-actor: A multi-task transformer for robotic manipulation, in: Conference on Robot Learning (CoRL). URL: https://peract.github.io/paper/peract_corl2022.pdf. 

- Shridhar, M., Manuelli, L., Fox, D., 2023. Perceiver-actor: A multi-task transformer for robotic manipulation, in: Conference on Robot Learning, PMLR. pp. 785–799. 

- Shridhar, M., Thomason, J., Gordon, D., Bisk, Y., Han, W., Mottaghi, R., Zettlemoyer, L., Fox, D., 2020. ALFRED: a benchmark for interpreting grounded instructions for everyday tasks, in: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR). URL: https://arxiv.org/abs/1912.01734. 

- Shukor, M., Aubakirova, D., Capuano, F., Kooijmans, P., Palma, S., Zouitine, A., et al., 2025. Smolvla: A vision-language-action model for affordable and efficient robotics. arXiv preprint arXiv:2506.01844 URL: https://arxiv.org/abs/2506.01844. 

- Sliwowski, D., Jadav, S., Stanovcic, S., Orbik, J., Heidersberger, J., Lee, D., 2025. Reassemble: A multimodal dataset for contact-rich robotic assembly and disassembly. arXiv preprint arXiv:2502.05086 . 

- Song, C.H., Blukis, V., Tremblay, J., Tyree, S., Su, Y., Birchfield, S., 2025a. Robospatial: Teaching spatial understanding to 2d and 3d visionlanguage models for robotics. URL: https://arxiv.org/abs/2411.16537, arXiv:2411.16537. 

- Song, W., Chen, J., Ding, P., Zhao, H., Zhao, W., Zhong, Z., Ge, Z., Ma, J., Li, H., 2025b. Accelerating vision-language-action model integrated with action chunking via parallel decoding. arXiv preprint arXiv:2503.02310 . 

Page 26 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

- Tang, W., Pan, J.H., Liu, Y.H., Tomizuka, M., Li, L.E., Fu, C.W., Ding, M., 2025. Geomanip: Geometric constraints as general interfaces for robot manipulation. arXiv preprint arXiv:2501.09783 . 

- Team, F.A., 2025a. Helix: A vision-language-action model for generalist humanoid control. Available at: https://www.figure.ai/news/helix. 

- Team, G.R., 2025b. Gemini robotics: Bringing ai into the physical world. arXiv preprint arXiv:2503.20020 URL: https://arxiv.org/abs/2503. 20020. 

- Team, O.M., Ghosh, D., Walke, H., Pertsch, K., Black, K., Mees, O., Dasari, S., Hejna, J., Kreiman, T., Xu, C., et al., 2024. Octo: An open-source generalist robot policy. arXiv preprint arXiv:2405.12213 . 

- Thomason, J., Murray, M., Cakmak, M., Zettlemoyer, L., 2019. Visionand-dialog navigation. URL: https://arxiv.org/abs/1907.04957, arXiv:1907.04957. 

- Todorov, E., Erez, T., Tassa, Y., 2012. Mujoco: A physics engine for modelbased control, in: 2012 IEEE/RSJ international conference on intelligent robots and systems, IEEE. pp. 5026–5033. 

- Touvron, H., Martin, T., Stone, L., Albert, A., Almahairi, A., Laradji, I., Aqaj, Y., Baratin, A., Lee, S., Verde, Z., Kaplanyan, A., Azar, M., Gelly, S., Joulin, A., 2023. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971 . 

- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Å., Polosukhin, I., 2017. Attention is all you need, in: Advances in Neural Information Processing Systems (NeurIPS), pp. 5998–6008. URL: https://arxiv.org/abs/1706.03762. 

- Walke, H.R., Black, K., Zhao, T.Z., Vuong, Q., Zheng, C., Hansen-Estruch, P., He, A.W., Myers, V., Kim, M.J., Du, M., et al., 2023. Bridgedata v2: A dataset for robot learning at scale, in: Conference on Robot Learning, PMLR. pp. 1723–1736. 

- Wang, L., Zhang, H., Zhao, Y., Liu, Z., Bian, J., Yu, H., Xu, C., Lau, R., Wang, S., 2022. Vlmo: Unified vision-language pre-training with mixture-of-modality-experts, in: ACM International Conference on Multimedia (MM). 

- Wang, R., Zhang, J., Chen, J., Xu, Y., Li, P., Liu, T., Wang, H., 2023. Dexgraspnet: A large-scale robotic dexterous grasp dataset for general objects based on simulation, in: 2023 IEEE International Conference on Robotics and Automation (ICRA), IEEE. pp. 11359–11366. 

- Wang, S., Shan, J., Zhang, J., Gao, H., Han, H., Chen, Y., Wei, K., Zhang, C., Wong, K., Zhao, J., et al., 2025. Robobert: An end-to-end multimodal robotic manipulation model. arXiv preprint arXiv:2502.07837 . 

- Wang, T., Han, C., Liang, J.C., Yang, W., Liu, D., Zhang, L.X., Wang, Q., Luo, J., Tang, R., 2024a. Exploring the adversarial vulnerabilities of vision-language-action models in robotics. arXiv preprint arXiv:2411.13587 . 

- Wang, Z., Zheng, H., Nie, Y., Xu, W., Wang, Q., Ye, H., Li, Z., Zhang, K., Cheng, X., Dong, W., Cai, C., Lin, L., Zheng, F., Liang, X., 2024b. All robots in one: A new standard and unified dataset for versatile, generalâĂŚpurpose embodied agents. arXiv preprint arXiv:2408.10899 URL: https://arxiv.org/abs/2408.10899. 

- Wang, Z., Zhou, Z., Song, J., Huang, Y., Shu, Z., Ma, L., 2024c. Towards testing and evaluating vision-language-action models for robotic manipulation: An empirical study. arXiv preprint arXiv:2409.12894 . 

- Wang, Z., Zhou, Z., et al., 2024d. Ladev: A language-driven testing and evaluation platform for vision-language-action models in robotic manipulation. arXiv preprint arXiv:2410.05191 . 

- Wen, J., Zhu, M., Zhu, Y., Tang, Z., Li, J., Zhou, Z., Li, C., Liu, X., Peng, Y., Shen, C., Feng, F., 2024. Diffusion-vla: Generalizable and interpretable robot foundation model via self-generated reasoning. arXiv preprint arXiv:2412.03293 Accepted by ICML 2025. 

- Wen, J., Zhu, Y., Li, J., Tang, Z., Shen, C., Feng, F., 2025. Dexvla: Visionlanguage model with plug-in diffusion expert for general robot control. arXiv preprint arXiv:2502.05855 . 

- Wu, Y., Tian, R., Swamy, G., Bajcsy, A., 2025. From foresight to forethought: Vlm-in-the-loop policy steering via latent alignment. arXiv preprint arXiv:2502.01828 . 

- Xia, F., Li, C., Martín-Martín, R., Litany, O., Zamir, A.R., Savarese, S., 2020. Interactive gibson benchmark: A benchmark for interactive navigation in cluttered environments, in: Proceedings of the IEEE/RSJ 

International Conference on Intelligent Robots and Systems (IROS), pp. 5891–5898. URL: https://arxiv.org/abs/2002.10322, doi:10.1109/ IROS45743.2020.9341201. 

- Xiang, F., Qin, Y., Mo, K., Xia, Y., Zhu, H., Liu, F., Liu, M., Jiang, H., Yuan, Y., Wang, H., et al., 2020. Sapien: A simulated part-based interactive environment, in: Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 11097–11107. 

- Xiao, B., Wu, H., Xu, W., Dai, X., Hu, H., Lu, Y., Zeng, M., Liu, C., Yuan, L., 2024. Florence-2: Advancing a unified representation for a variety of vision tasks, in: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 4818–4829. 

- Xu, S., Wang, Y., Xia, C., Zhu, D., Huang, T., Xu, C., 2025. Vla-cache: Towards efficient vision-language-action model via adaptive token caching in robotic manipulation. arXiv preprint arXiv:2502.02175 . 

- Xue, H., Huang, X., Niu, D., Liao, Q., Kragerud, T., Gravdahl, J.T., Peng, X.B., Shi, G., Darrell, T., Sreenath, K., Sastry, S., 2025. Leverb: Humanoid whole-body control with latent vision-language instruction. arXiv preprint arXiv:2506.13751 URL: https://arxiv.org/abs/2506. 13751. 

- Yan, F., Liu, F., Zheng, L., Zhong, Y., Huang, Y., Guan, Z., Feng, C., Ma, L., 2024. Robomm: All-in-one multimodal large model for robotic manipulation. arXiv preprint arXiv:2412.07215 URL: https://arxiv. org/abs/2412.07215. 

- Yang, J., Tan, R., Wu, Q., Zheng, R., Peng, B., Liang, Y., Gu, Y., Cai, M., Ye, S., Jang, J., et al., 2025. Magma: A foundation model for multimodal ai agents, in: Proceedings of the Computer Vision and Pattern Recognition Conference, pp. 14203–14214. 

- Yang, M., Du, Y., Ghasemipour, K., Tompson, J., Schuurmans, D., Abbeel, P., 2023. Learning interactive real-world simulators. arXiv preprint arXiv:2310.06114 1, 6. 

- Yu, T., Quillen, D., He, Z., Julian, R., Hausman, K., Finn, C., Levine, S., 2020. Meta-world: A benchmark and evaluation for multi-task and meta reinforcement learning, in: Conference on robot learning, PMLR. pp. 1094–1100. 

- Zawalski, M., Chen, W., Pertsch, K., Mees, O., Finn, C., Levine, S., 2025. Robotic control via embodied chain-of-thought reasoning. arXiv preprint arXiv:2407.08693 URL: https://arxiv.org/abs/2407.08693. 

- Zayyanu, M., Usman, B.T., Muda, Z., Salim, N.A., Mohamed, A., Abubakar, A.Y., Al-Obeidat, F., Malik, M.A., 2024. Revolutionising natural language processing with transformers: A survey. Information Processing & Management 61, 103528. doi:10.1016/j.ipm.2023.103528. 

- Zhang, B., Zhang, Y., Ji, J., Lei, Y., Dai, J., Chen, Y., Yang, Y., 2025a. Safevla: Towards safety alignment of vision-language-action model via safe reinforcement learning. arXiv e-prints , arXiv–2503. 

- Zhang, H., Ding, P., Lyu, S., Peng, Y., Wang, D., 2025b. Gevrm: Goalexpressive video generation model for robust visual manipulation. arXiv preprint arXiv:2502.09268 . 

- Zhang, H., Zantout, N., Kachana, P., Zhang, J., Wang, W., 2025c. Iref-vla: A benchmark for interactive referential grounding with imperfect language in 3d scenes. arXiv preprint arXiv:2503.17406 . 

- Zhang, J., Guo, Y., Chen, X., Wang, Y.J., Hu, Y., Shi, C., Chen, J., 2024a. Hirt: Enhancing robotic control with hierarchical robot transformers, in: Proceedings of the 8th Conference on Robot Learning (CoRL). URL: https://arxiv.org/abs/2410.05273. 

- Zhang, J., Guo, Y., Hu, Y., Chen, X., Zhu, X., Chen, J., 2025d. Up-vla: A unified understanding and prediction model for embodied agent. arXiv preprint arXiv:2501.18867 . 

- Zhang, J., Wang, K., Wang, S., Li, M., Liu, H., Wei, S., Wang, Z., Zhang, Z., Wang, H., 2024b. Uni-navid: A video-based vision-languageaction model for unifying embodied navigation tasks. arXiv preprint arXiv:2412.06224 . 

- Zhang, R., Dong, M., Zhang, Y., Heng, L., Chi, X., Dai, G., Du, L., Wang, D., Du, Y., Zhang, S., 2025e. Mole-vla: Dynamic layer-skipping vision language action model via mixture-of-layers for efficient robot manipulation. arXiv preprint arXiv:2503.20384 . 

- Zhang, Z., Zheng, K., Chen, Z., Jang, J., Li, Y., Han, S., Wang, C., Ding, M., Fox, D., Yao, H., 2024c. Grape: Generalizing robot policy via preference alignment. arXiv preprint arXiv:2411.19309 . 

Page 27 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

Vision Language Action Models a Review 

- Zhao, H., Song, W., Wang, D., Tong, X., Ding, P., Cheng, X., Ge, Z., 2025a. More: Unlocking scalability in reinforcement learning for quadruped vision-language-action models. arXiv preprint arXiv:2503.08007 . 

- Zhao, T., Kumar, V., Levine, S., Finn, C., 2023. Learning finegrained bimanual manipulation with low-cost hardware. arXiv preprint arXiv:2304.13705 . 

- Zhao, W., Ding, P., Zhang, M., Gong, Z., Bai, S., Zhao, H., Wang, D., 2025b. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. arXiv preprint arXiv:2502.13508 . 

- Zhao, W., Li, G., Gong, Z., Ding, P., Zhao, H., Wang, D., 2025c. Unveiling the potential of vision-language-action models with open-ended multimodal instructions. arXiv preprint arXiv:2505.11214 URL: https: //arxiv.org/abs/2505.11214. 

- Zhen, H., Qiu, X., Chen, P., Yang, J., Yan, X., Du, Y., Hong, Y., Gan, C., 2024. 3d-vla: A 3d vision-language-action generative world model. arXiv preprint arXiv:2403.09631 URL: https://arxiv.org/abs/2403. 09631. 

- Zheng, J., Li, J., Liu, D., Zheng, Y., Wang, Z., Ou, Z., Liu, Y., Liu, J., Zhang, Y.Q., Zhan, X., 2025a. Universal actions for enhanced embodied foundation models. arXiv preprint arXiv:2501.10105 . 

- Zheng, R., Liang, Y., Huang, S., Gao, J., III, H.D., Kolobov, A., Huang, F., Yang, J., 2025b. Tracevla: Visual trace prompting enhances spatialtemporal awareness for generalist robotic policies, in: International 

- Conference on Learning Representations (ICLR). URL: https://arxiv. org/abs/2412.10345. 

- Zhong, Y., Huang, X., Li, R., Zhang, C., Liang, Y., Yang, Y., Chen, Y., 2025. Dexgraspvla: A vision-language-action framework towards general dexterous grasping. arXiv preprint arXiv:2502.20900 . 

- Zhou, Z., Zhu, Y., Zhu, M., Wen, J., Liu, N., Xu, Z., Meng, W., Cheng, R., Peng, Y., Shen, C., et al., 2025. Chatvla: Unified multimodal understanding and robot control with vision-language-action model. arXiv preprint arXiv:2502.14420 . 

- Zhu, M., Zhu, Y., Li, J., Zhou, Z., Wen, J., Liu, X., Shen, C., Peng, Y., Feng, F., 2025a. Objectvla: End-to-end open-world object manipulation without demonstration. arXiv preprint arXiv:2502.19250 . 

- Zhu, T., Zhang, H., Zhou, Y., Yu, W., Wang, Y., Ma, L., Xu, H., 2025b. Opendrive-vla: Generalist vision-language-action agent for autonomous driving. arXiv preprint arXiv:2505.01871 URL: https://arxiv.org/abs/ 2505.01871. 

- Zhu, Y., Gupta, A., Ebert, F., et al., 2020. robosuite: A modular simulation framework and benchmark for robot learning. arXiv preprint arXiv:2009.12293 . 

- Zitkovich, B., Yu, T., Xu, S., Xu, P., Xiao, T., Xia, F., Wu, J., Wohlhart, P., Welker, S., Wahid, A., et al., 2023. Rt-2: Vision-language-action models transfer web knowledge to robotic control. Conference on Robot Learning, PMLR , 2165–2183. 

Page 28 of 28 

Muhayy Ud Din et al.: _Preprint submitted to Elsevier_ 

