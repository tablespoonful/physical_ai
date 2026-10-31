---
title: "Real-World Robot Applications of Foundation Models: A Review"
date: "2024-02-08"
authors: "Kento Kawaharazuka; Tatsuya Matsushima; Andrew Gambardella; Jiaxian Guo; Chris Paxton; Andy Zeng"
url: https://arxiv.org/abs/2402.05741
pdf: https://arxiv.org/pdf/2402.05741
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2402.05741)** / [論文ページ](https://arxiv.org/abs/2402.05741)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# REVIEW ARTICLE 

# **Real-World Robot Applications of Foundation Models: A Review** 

Kento Kawaharazuka<sup>a*</sup> , Tatsuya Matsushima<sup>b*</sup> , Andrew Gambardella<sup>b</sup> , Jiaxian Guo<sup>b</sup> , Chris Paxton<sup>c</sup> , and Andy Zeng<sup>d</sup> 

- First two authors equally contributed to this work 

- a Department of Mechano-Informatics, The University of Tokyo, Japan b School of Engineering, The University of Tokyo, Japan 

- c Meta AI Research 

- d Google DeepMind 

### **ARTICLE HISTORY** 

Compiled October 24, 2024 

### **ABSTRACT** 

Recent developments in foundation models, like Large Language Models (LLMs) and Vision-Language Models (VLMs), trained on extensive data, facilitate flexible application across different tasks and modalities. Their impact spans various fields, including healthcare, education, and robotics. This paper provides an overview of the practical application of foundation models in real-world robotics, with a primary emphasis on the replacement of specific components within existing robot systems. The summary encompasses the perspective of input-output relationships in foundation models, as well as their role in perception, motion planning, and control within the field of robotics. This paper concludes with a discussion of future challenges and implications for practical robot applications. 

### **KEYWORDS** 

Foundation Models, Robot Applications, Real-World Scenario 

## **1. Introduction** 

Recent advancements in artificial intelligence have markedly expanded the operational capabilities of robots, enabling them to undertake a diverse range of activities [1–5]. Although initially robots’ deployment was primarily limited to mass production environments [6–11], the applicability of industrial robots has now branched into areas of small-batch and high-variety production, including indoor spaces and disaster sites [12–15]. This proliferation is not merely limited to an increase in environmental diversity; it also extends to an expanded repertoire of tasks, encompassing everyday activities like tidying [16–18], washing [19,20], wiping [21,22], and cooking [23,24]. 

Machine learning has provided a way to meet the needs of such robot systems. However, training each model only on domain-specific data is insufficient for the diverse robots, tasks, and environments. There is a growing need for the development of robots 

Email: `kawaharazuka@jsk.imi.i.u-tokyo.ac.jp` and `matsushima@weblab.t.u-tokyo.ac.jp` This is a preprint of an article whose final and definitive form has been published in ADVANCED ROBOTICS 2024, copyright Taylor & Francis and Robotics Society of Japan, is available online at: `http: //www.tandfonline.com/Article` DOI; `https://doi.org/10.1080/01691864.2024.2408593` . 


**Figure 1.** The structure of this study. In section 2, we overview the characteristics of foundation models and introduce common downstream tasks. In section 3, we categorize studies of applications of foundation models in robotics. In section 4, we introduce prior work on creating foundation models for robotics, so-called robotic foundation models. In section 5, we overview robots, tasks, and environments used for applications of foundation models in robotics. 

that can be applied to various bodies, tasks, and environments using a single, pretrained system or module. 

One solution to this challenge is the introduction of foundation models [25]. Foundation models are models that are trained on large amounts of data and can be easily applied to a wide range of downstream tasks through in-context learning, fine-tuning, or even in a zero-shot manner [26,27]. Prominent examples include Large Language Models (LLMs) like GPT [27] and Vision-Language Models (VLMs) like CLIP [28], where language is a glue to combine various types of modalities. The impact of these foundation models has been remarkable, with several review papers discussing their influence across diverse fields [29–32]. Wang et al. [29] and Zeng et al. [30] have conducted surveys on the application of large language models in robotics, while Firoozi et al. [31] and Hu et al. [32] have conducted surveys on a broader scale, focusing on the application of foundation models in robotics. In this paper, we summarize the applicability of foundation models to real-world robots, aiming to accelerate their adoption in practical robot applications. In comparison to the other survey papers, we provide a summary of how to replace specific components in existing robot systems with foundation models, from the perspective of input-output relationships of the foundation models, as well as perception, motion planning, and control in robotics. 

The structure of this study is shown in Figure 1. In section 2, we will describe the foundation models themselves. In particular, we will classify foundation models in terms of what kind of modalities they use, e.g., vision [33,34], language [35–41] and so on, and what kind of downstream tasks to which they can be applied. In section 3, we will describe how to apply foundation models to robotics based on current applications [2,3,42]. In general, robots need to be equipped with a perception module, a planning module, and a control module. From this perspective, we classify the ways in which one can apply foundation models to real-world robotics into low-level perception, high-level perception, high-level planning, and low-level planning. Additionally, we will explain data augmentation for robotics when training a mapping to directly connect low-level perception and low-level planning. In section 4, we will describe foundation models that include robot embodiment, the robotic foundation model, including discussions about how to make these robotic foundation models in terms of model architecture, dataset, and learning objective. In section 5, we will describe the robots, tasks, and environments where foundation models are used. We classify the 

2 

tasks into navigation, manipulation, navigation with manipulation, locomotion, and communication. Finally, we will discuss future challenges and present our conclusions. 

## **2. Foundation Models** 

The term _foundation model_ was first introduced in [25]. In this survey, we will simply describe the types of foundation models used in robotic applications, as well as downstream tasks, deferring to [25] for a discussion of foundation models themselves. 

In 2012, deep learning gained mainstream attention from the machine learning community with the winning model from the ILSVRC-2012 competition [43]. In 2017, the Transformer model was introduced by [44], leading to significant advancements in the fields of natural language processing (NLP) [45] and computer vision [46]. In 2021, a model that has been trained on a large amount of data and can be easily applied to a wide range of downstream tasks has come to be referred to as a “foundation model” [25]. Foundation models are characterized by three main characteristics: 

- In-context learning 

- Scaling law 

- Homogenization 

_In-context learning_ enables the accomplishment of new tasks with just a few examples, without the need for retraining or fine-tuning. _Scaling laws_ allow for continued performance improvements as data, computational resources, and model sizes are increased. _Homogenization_ allows for certain foundation model architectures to handle diverse modalities in a unified manner. 

In this chapter, we classify foundation models from the perspective of their applicability in robotics. The most critical criterion for robots to leverage foundation models is the choice of which modalities to use. This chapter discusses the types of foundation models and the downstream tasks that they can perform from the perspectives of language, vision, audio, 3D representation, and various other modalities. In the context of utilizing each modality, we further classify foundation models from the perspective of network inputs and outputs. The overview is shown in Figure 2. Note that we do not aim to comprehensively cover foundation models here; our focus remains on addressing differences in modalities and classification of foundation models. 

## **_2.1. Foundation Models for Language_** 

_Large Language Models_ (LLMs) often refer to large deep neural networks trained on vast amounts of data. From the viewpoint of large deep neural networks, Transformers are common architectures for recent LLMs, which may refer to decoder-only autoregressive architectures that consist of multiple Transformer blocks trained to predict the next token. In terms of the data, the datasets for training LLMs are Internet-scale; for example, the pre-training of GPT-3 [47] uses CommonCrawl covering Internet data from years 2016 to 2019, which amounts to 45TB of compressed plain text and 410 billion tokens after filtering. Codex [48] leverages substantial code data from the snapshot of 54 million public software repositories hosted on GitHub in May 2020 to enable code-writing capabilities with LLMs. LLMs are the basis of recent foundation models, which can generalize to diverse domains and combine multiple types of data. The network input and output of LLMs primarily fall into two categories: 

3 


## **Audio-Language Model (ALM)** 

**Figure 2.** The overview of foundation models classified by the modalities such as language, vision, audio, and 3D representation, and by the network input and output. 

## _•_ `Language` _→_ `Language` 

- `Language` _→_ `Latent` 

Regarding `Language` _→_ `Language` , various LLMs have been developed, including GPT-3 [35], LLaMA [40,49], and others. These models can be prompted in order to induce _Chain of Thought (CoT)_ [50,51] which allows them to achieve more complex inference capabilities by going through intermediate reasoning steps while solving a problem. Furthermore, this `language` is not limited to natural language but can also handle various formats such as program code, markup languages (e.g., HTML, XML), and data structures (e.g., JSON, YAML) [48]. In-context learning can also lead to a significant improvement in its performance through the use of examples presented in a few-shot manner. 

As for `Language` _→_ `Latent` , models like BERT [45], RoBERTa [52] have been developed that can transform language into latent space vectors. Also, one can obtain latent space vectors from large language models which can perform `Language` _→_ `Language` conversions, by extracting features from intermediate layers. By projecting into the 

4 

latent space, it becomes possible to measure the distance between two sentences, enabling one to extract similar sentences for tasks such as retrieval. 

Additionally, it is important to highlight the significance of using language models in robotics. There are several advantages to employing language models in robots, with a key benefit being that language models encompass human common sense. This enables robots to autonomously perform tasks such as motion planning and recognition. Moreover, knowledge can be imparted to the robots through in-context learning. However, a major challenge is hallucination. Since language models do not always produce correct outputs, various methods are being developed to ensure reliability. 

## **_2.2. Foundation Models for Vision_** 

The foundation models for images, Large Vision Models (LVM), can mainly be divided into two types based on network input and output: 

- `Vision` _→_ `Latent` 

- `Vision` _→_ `Recognition` 

Regarding `Vision` _→_ `Latent` , various techniques have been developed to project images from diverse situations into some latent space. Representative examples include R3M [3] and VC-1 [53]. These methods are designed to transform image information from various data sources into lower-dimensional vectors, which can be considered as feature extraction of high-level representations. 

As for `Vision` _→_ `Recognition` , in this context, `Recognition` refers to performing tasks such as semantic segmentation, instance segmentation, and bounding box extraction on images. Typically, recognition is based on language labels, and there are not many foundation models that perform these recognitions solely based on image information. Among them, Segment Anything [54] is a model specialized in image segmentation, capable of segmenting not only the entire image but also specific areas specified by points or boxes. More advanced applications like Tracking Anything [55] and Faster Segment Anything [56] have also been developed. It is important to note that `Vision` _→_ `Latent` learning can be self-supervised, making it easy to construct large datasets. However, `Vision` _→_ `Recognition` learning requires manually collecting large amounts of data, making it less scalable. 

Of course, some models perform `Vision` _→_ `Vision` or `Latent` _→_ `Vision` tasks. To effectively utilize these models as foundation models for various tasks, however, conditioning on language is often essential. Therefore, in the following section on Vision and Language, we will introduce examples of such models. 

## **_2.3. Foundation Models for Vision and Language_** 

While individual language or image processing has limited capabilities, combining vision and language allows us to build diverse foundation models. These Vision-Language Models (VLMs) are trained with the Internet-scale massive datasets as well as LLMs. For instance, CLIP [28] is trained on 400 million image-text pair datasets from the Internet. When classifying VLMs from the network input and output, they mainly fall into the following four categories. 

- `Vision + Language` _→_ `Latent` 

- `Vision + Language` _→_ `Language` 

- `Vision + Language` _→_ `Vision` 

5 

## _•_ `Vision + Language` _→_ `Recognition` 

`Vision + Language` _→_ `Latent` involves converting images and text into latent space vectors, which allows one to calculate the similarity between them for downstream tasks such as retrieval. Prominent models include CLIP [28] and GLIP [57]. While CLIP [28] computes correspondences between a single image-text pair, GLIP [57] can calculate correspondences between multiple regions of an image with their text descriptions. 

`Vision + Language` _→_ `Language` enables tasks like image captioning (IC), visual question answering (VQA), and visual entailment (VE). Prominent models include BLIP2 [58], Flamingo [59], OFA [60], and Unified-IO [61]. BLIP2 is dedicated to IC and VQA, whereas OFA and Unified-IO serve as a foundation model capable of VQA, IC, Visual Grounding (VG), Text-to-Image Generation (TIG), and more within a single network. Flamingo supports in-context learning for both vision and language. GPT-4 Vision (GPT-4V) [27] can analyze images that users input into the model and generate the answer as texts, which can apply to IC, VWA, and VE. Extending GPT4V, GPT-4o (omni) is a multimodal model that can reason across audio, vision, and text. 

`Vision + Language` _→_ `Vision` facilitates tasks like image editing and image generation through language. Prominent models include Stable Diffusion [62], DALLE [63], and the previously mentioned OFA [60] and Unified-IO [61]. They incorporate Transformer-based architectures and diffusion architectures into the models. 

`Vision + Language` _→_ `Recognition` enables tasks like semantic segmentation, instance segmentation, and bounding box extraction from images and language. Prominent models include Detic [64], OWL-ViT [65], UniVL [66], LSeg [67], and DinoV2 [68], which are applicable to open-vocabulary recognition. 

The `Vision` category encompasses not only images but also videos. Some approaches involve inputting videos frame by frame into these models and integrating the results, while others like XCLIP [69] and StableVideo [70] directly accept videos as input or produce video outputs. 

## **_2.4. Foundation Models for Audio_** 

By incorporating auditory input into an existing Vision-Language Model, it becomes possible to tackle a wider range of tasks. These Audio-Language Models (ALMs) can be categorized as follows based on network input and output. 

- `Audio + Vision + Language` _→_ `Latent` 

- `Audio + Language` _→_ `Language` 

- `Audio + Vision + Language` _→_ `Audio` 

`Audio + Vision + Language` _→_ `Latent` does not only represent the correspondence between images and language like in CLIP and GLIP, but also encodes sound into latent space vectors, enabling similarity calculations. Prominent models developed for this purpose include CLAP [71] and AudioCLIP [72]. 

`Audio + Language` _→_ `Language` primarily enables Speech-to-Text recognition. Representative models in this category include Whisper [73]. With Whisper [73], it is possible to specify easily confused words and perform in-context learning. 

`Audio + Vision + Language` _→_ `Audio` mainly facilitates Text-to-Speech and audio conversion. Prominent models in this domain include MusicLM [74] and VALLE [75]. VAST [76] is a multi-modal foundation model, which is applicable to video, 

6 

audio, subtitle, and texts. 

## **_2.5. Foundation Models for 3D Representation_** 

Currently, research incorporating 3D representations such as point clouds and 3D meshes as modalities is on the rise. 3D representations are essential for robot operations. Classifying these from network input and output can be summarized as follows: 

- `3D Representation + Vision + Language` _→_ `Latent` 

- `Vision + Language` _→_ `3D Representation` 

- `3D Representation + Vision + Language` _→_ `Recognition` 

`3D Representation + Vision + Language` _→_ `Latent` enables the transformation of 3D representations into latent space vectors, and therefore allows for similarity calculations between latent vectors, like in previous models like CLIP and CLAP. Representative models in this category include ULIP [77] and CLIP-goes-3D [78]. It allows for tasks such as classifying objects of interest based on their 3D shapes, images, or language and using them as features for policy learning. 

`Vision + Language` _→_ `3D Representation` outputs the 3D shapes of objects represented as Point Clouds or 3D Meshes based on images or language input. Prominent models in this category include OmniObject3D [79] and Point-E [80]. These can be useful for tasks like comparing the shape of manipulated objects to reality or viewing them from different angles. Also, TexFusion can output 3D texture with text-guided image diffusion models [81]. 

`3D Representation + Vision + Language` _→_ `Recognition` enables tasks such as segmentation and bounding box extraction in 3D space through language, similar to previous approaches. Representative algorithms include 3D-LLM [82], OpenScene [83], and SpatialVLM [84], which combine 3D representations with LLMs. 

## **_2.6. Foundation Models for Other Modalities_** 

Up until now, we have discussed language, vision, audio, and 3D representations, but in reality it is possible to use various types of sensors. Such sensors include IMUs, heatmaps, object poses, and skeletal movements including gestures. Notable models in this regard include ImageBind [85] and Meta-Transformer [86]. These methods, like CLIP, CLAP, and ULIP, enable similarity calculations, but they simultaneously handle a significantly larger number of modalities. In addition, FoundationPose [87] is a unified foundation model for 6D object pose estimation and tracking, supporting both model-based and model-free setups. There are numerous techniques for dealing with gestures and skeletal movements, such as Human Motion Diffusion Model [88], T2M-GPT [89], and GestureDiffCLIP [90], which generate human motion or gesture through spoken language. 

Finally, it is important to note that there are many models with slightly different input and output configurations beyond what we have discussed here. By determining which modalities are being utilized and what tasks are possible, we can anticipate future application of these models in real-world robotics. 

7 


**Figure 3.** The overview of utilization of foundation models for robots. With foundation models, low-level perception conducts feature extraction or scene recognition, high-level perception conducts reward generation or map construction, high-level planning conducts task planning or code generation, low-level planning conducts footstep generation or command generation, and data augmentation conducts image augmentation or instruction augmentation. 

## **3. Applications of Foundation Models to Robotics** 

In general, the behavior of robots is composed of perception, planning, and control. In this study, we divide perception into two categories: low-level and high-level. Also, we refer to planning and control as high-level planning and low-level planning, respectively. With the addition of data augmentation for learning these components, we categorize the utilization of foundation models for robots into the following five categories. 

- _low-level perception_ 

- _high-level perception_ 

- _high-level planning_ 

- _low-level planning_ 

- _data augmentation_ 

It should be noted that this order of five categories takes into account the typical sequence in robotics: perception, planning, and control. The relationship between these categories is shown in Figure 3. Foundation models for low-level perception include semantic segmentation and bounding box extraction in images or 3D representations, and feature extraction in various modalities. Foundation models for high-level perception involve the transformation and utilization of results obtained from low-level perception into forms such as maps, rewards, and motion constraints. Foundation models for high-level planning execute higher-level abstract task planning, excluding direct control. Foundation models for low-level planning execute lower-level motion control, including joint and end effector control. Foundation models for data augmentation enhance robustness through data augmentation when executing learning that connects low-level perception and low-level planning. 

In practice, various applications are created by combining these five utilization methods. They are mainly categorized into four types as shown in Figure 4. 

- (i) Performing low-level perception and then planning behaviors with high-level planning. 

- (ii) Extracting rewards and motion constraints through low-level perception and high-level perception, and using them for reinforcement learning and trajectory optimization. 

8 


**Figure 4.** The four types of combinations of low-level perception, high-level perception, high-level planning, low-level planning, and data augmentation with foundation models. 

- (iii) Generating maps, scene graphs, and more through low-level perception and highlevel perception, and using them as a basis for task planning. 

- (iv) Robustly conducting end-to-end learning that directly correlates feature extraction from low-level perception and control inputs, using data augmentation. 

It is important to note that there are also research approaches that do not fit within this framework. 

From these perspectives, we select several representative papers and summarize them in Table 1. The details are discussed subsequently. 

**Low-level Perception** : Representative studies utilizing foundation models for lowlevel perception include CLIPort [91] and REFLECT [92]. CLIPort utilizes the semantic information extracted by CLIP’s image and text encoder [28] along with spatial information extracted by Transporter Networks [93] to output pick and place positions, serving as an example of using foundation models for feature extraction in low-level perception. REFLECT combines object detection by MDETR [94], object state recognition by CLIP, scene graph description using depth images and heuristics, sound recognition by AudioCLIP [72], and a summary of the cause of robot failures along with corrective task plans generated by an LLM, serving as an example of using foundation models for scene recognition including explicit object recognition and sound recognition. CLIPort falls under category (iv), and REFLECT falls under category (i) in Figure 4. 

**High-level Perception** : Representative studies utilizing foundation models for high-level perception include VoxPoser [95] and CLIP-Fields [96]. VoxPoser uses an LLM and a VLM to generate affordance maps and constraint maps as programs, and based on these maps, it performs model predictive control, serving as an example of using foundation models for objective function generation and constraint design. A similar case is using LLM or VLM for reward design in reinforcement learning, such as with Eureka [97]. CLIP-Fields utilizes Detic [64], CLIP [28], and SentenceBERT [98] to embed object labels and object image features for each point cloud in 

9 

**Table 1.** Representative studies utilizing foundation models for low-level perception, high-level perception, high-level planning, low-level planning, and data augmentation. 

|Papers|Low-level perception|High-level perception|High-level planning|Low-level planning|Data augmentation|
|---|---|---|---|---|---|
|CLIPort [91]|**feature extraction**|-|-|-|-|
|REFLECT [92]|**scene recognition**|-|task planning|-|-|
|VoxPoser [95]|scene recognition|**objective design**|task planning|-|-|
|CLIP-Fields [96]|feature extraction|**map construction**|-|-|-|
|Tidy-Bot [18]|scene recognition|-|**task planning**|-|-|
|Code as Policies [5]|scene recognition|-|**code generation**|-|-|
|SayTap [100]|-|-|-|**footstep generation**|-|
|General Pattern [101]|-|-|-|**command generation**|-|
|GenAug [102]|-|-|-|-|**image augmentation**|
|DIAL [103]|-|-|-|-|**instruction augmentation**|


space, enabling navigation, serving as an example of using foundation models for map construction. VoxPoser falls under category (ii), and CLIP-Fields falls under category (iii) in Figure 4. 

**High-level Planning** : Representative studies utilizing foundation models for highlevel planning include TidyBot [18] and Code as Policies [5]. TidyBot performs object recognition using ViLD [99] and object classification using CLIP [28]. It then infers where to place those objects, considering learned human preferences in conjunction with an LLM, serving as an example of using foundation models for task planning. Code as Policies generates Python code for pre-defined robot control recognition APIs and control APIs via an LLM, serving as an example of using foundation models for code generation. Both of these cases fall under category (i) in Figure 4. 

**Low-level Planning** : Representative studies utilizing foundation models for lowlevel planning include SayTap [100] and General Pattern Machines [101]. SayTap uses an LLM to output footstep plans and velocity using in-context learning, and then performs reinforcement learning through simulation to obtain joint commands that fulfill these plans, serving as an example of using foundation models for footstep generation. General Pattern Machines utilizes an LLM as a sequence generator for sequence transformation, completion, and improvement, and is used for reinforcement learning in tasks like Cartpole and action completion in manipulation, serving as an example of using foundation models for direct command generation. Both of these cases fall under category (i) in Figure 4, which consists solely of a low-level planner that does not involve perception. 

**Data Augmentation** : Representative studies utilizing foundation models for data augmentation include GenAug [102] and DIAL [103]. GenAug extensively augments images using diffusion models [62] by changing backgrounds, adding distractors, altering object textures, and repositioning different objects to improve the robustness of imitation learning, serving as an example of using foundation models for image data augmentation. DIAL obtains a large number of language instruction examples through LLM and crowdsourcing, fine-tunes CLIP [28] on a large dataset of trajectory data, and extracts multiple appropriate language instructions for imitation learning, serving as an example of using foundation models for instruction augmentation. Both of these cases fall under category (iv) in Figure 4. 

On the other hand, there has been research aiming at creating foundation models for robots that encompass these frameworks, including perception and planning, so-called _Robotic Foundation Models_ . We will provide more details on these in section 4. 

10 

## **_3.1. Low-level Perception_** 

We will describe examples of performing low-level perception with foundation models. As shown in Table 1, its use can mainly be divided into feature extraction and scene recognition. 

## _3.1.1. Low-level Perception for Feature Extraction_ 

Visual pretrained models have often been utilized as strong baselines of feature extraction for perception e.g., ResNet [104] and MoCo [105]. More recently, foundation models, which are trained with more diverse and sometimes multi-modal datasets, are used as pre-trained and general feature extractors, e.g. CLIP [28] and R3M [3]. They are leveraged as either off-the-shelf models or fine-tuned with a dataset of downstream tasks. 

RRL [106] uses a pre-trained ResNet trained with ImageNet [107] (1,000 classes, 1.28M images) to extract features for a reinforcement learning policy with image input. R3M [3] is a visual pre-trained model for robotics trained with Ego4D datasets [108], which consists of egocentric human activity video, with the intention of reducing the domain gap between the source datasets and robot manipulation tasks. R3M is now one of the most commonly used visual pre-trained models; for instance, CACTI [109] uses R3M as a feature extractor for converting camera input to features for imitation learning combined with a ResNet trained with MoCo. Also, CLIP [28] is used in CLIPort [91] to extract language and image embeddings. 

## _3.1.2. Low-level Perception for Scene Recoginition_ 

Foundation models can be used off-the-shelf for common robot vision tasks of robot systems, such as object detection and semantic segmentation. Due to being trained with diverse text-image pair datasets, many of these models can be used in openvocabulary settings without further fine-tuning. For example, Detic [64], SAM [54], OWL-ViT [65], and ViLD [99] are open-vocabulary object detection and segmentation models. ViLD is often combined with CLIP for open-vocabulary object recognition from robot camera observation in table-top manipulation tasks [110] and mobile manipulation tasks [4,18,111]. OFA [60] is a sequence-to-sequence pre-trained vision language model that allows image captioning and visual question answering (VQA), text-to-image generation. 

REFLECT [92] combines object detection with MDETR [94], object state recognition by CLIP [28], and sound recognition by AudioCLIP [72] for a summary of the cause of robot failures. GIRAF [112] utilizes SAM to perform object segmentation on the scene images, and OpenCLIP [113], an open-sourced version of CLIP, for assigning object labels to the segmented images, in combination with supervised gesture detection models. In Kawaharazuka et al. [114], OFA [60] is leveraged to classify the scene as a binary state, e.g. whether a door is open or not, for robot navigation. Similarly, in Kanazawa et al. [115], CLIP is utilized to detect state changes in food ingredients, such as boiling water and melted butter, in the application of cooking robots. 

## **_3.2. High-level Perception_** 

We will describe examples of performing high-level perception with foundation models. As shown in Table 1, its use can mainly be divided into objective design and map construction. 

11 

## _3.2.1. High-level Perception for Objective Design_ 

Foundation models can be utilized for generating goals for downstream planning, generating rewards and costs of the plan, and affordances of controls. 

One of the examples of goal generation for planning with foundation models is DALL-E bot [116], which utilizes a text-conditioned diffusion model for generating goal images for table-top object rearrangement from language instructions. Also, StructDiffusion [117] can offer greater flexibility as it can directly output object placement poses from point cloud observations. Similarly, SuSIE [118] generates subgoals for object manipulation tasks leveraging pre-trained text-conditional image-editing models such as InstructPix2Pix [119]. UniPi [120] generates video using a text-guided video diffusion model with an initial image observation and instruction text, which then can be used in conjunction with a learned inverse model in order to infer actions. 

Similarly, foundation models are used to evaluate states of rewards or costs that can be leveraged with classical planners such as Model Predictive Control (MPC) or learned planners such as reinforcement learning policies. Some algorithms leverage LLMs to generate reward functions from language instructions. In Kwon et al. [121], LLM is leveraged as a proxy of reward functions by providing a few examples or a description of desired behavior. Language to Rewards [122] utilizes LLMs to describe desired robot motion as text from language instruction and then converts it to code reward functions. The reward function is used to optimize robot motion. Dynalang [123] uses an LLM to predict future rewards and utilizes it for model-based reinforcement learning (world models) based on DreamerV3 [124]. ZeST [125] utilizes VLMs to specify goals for robot manipulation tasks in a zero-shot manner. 

Foundation models are also leveraged to learn affordances for manipulation tasks. For example, some works learn affordances for object manipulation from human egocentric video (e.g., EPIC-KITCHENS [126] and Ego4D [108] dataset). RoboAffordances [127] learns a contact heatmap and trajectories from human egocentric videos (EPIC-KITCHENS). Similarly, VIP [128] learns reward functions for object manipulation from the Ego-4D dataset by time contrastive learning and transfers it to real-world robot manipulation settings. LIV [129] extends VIP by learning a multi-modal (language and image) reward function from text-annotated video (EPIC-KITCHENS), which is used to train language-conditional imitation learning policies. Aside from learning 2D visual affordances, VoxPoser [95] represents visual affordances as a 3D Voxel map for motion planning with MPC. 

## _3.2.2. High-level Perception for Map Construction_ 

Vision language models, such as CLIP, are used for extracting semantic information in the mapping, localization, and navigation tasks of mobile robots. LM-Nav [130] uses CLIP as a vision-and-language model for grounding the robot’s visual observations to landmarks in order to create graphs of visual landmarks. CLIP on Wheels [131] adapts open-vocabulary models to language-driven zero-shot object navigation (L-ZSON), the task of navigating an environment and finding specific objects without any prior training. CLIPFields [96] uses CLIP for semantic mapping, embedding the visual features from CLIP into a 3D map using neural rendering [132,133]. The model can retrieve the most similar position between the text input and the semantic map. Similarly, NLMap-Saycan [111] proposes an open-vocabulary queryable semantic representation using CLIP and ViLD [99] to form a semantic map that can be used for navigation with text instructions. AVL-Maps [134] and VL-Maps [135] generate a top-down projection map with the embeddings of text, image, and audio information, which a robot can 

12 

use to navigate to appropriate places. Furthermore, ConceptFusion [136] is engaged in constructing a 3D map that allows queries through images, sound, and text, while OpenFusion [137] is developing a method for performing this process in real-time. Also, ConceptGraphs [138] proposes an open-vocabulary graph-structured representation for 3D scenes, enabling the robot to answer complex scene queries, open-vocabulary pick and place, and traversability estimation. 

## **_3.3. High-level Planning_** 

We will describe examples of performing high-level planning with foundation models. Generating high-level motion planning is one of the most effective use cases of LLMs. As shown in Table 1, its use can mainly be divided into task planning and code generation. 

## _3.3.1. High-level Planning with Task Planning_ 

In Huang et al. [139], next motion plans are generated as language using GPT-3 (causal LLM), the actionable plan is chosen from action set using BERT (Masked LLM), and then the action is executed. SayCan [4] is one of the most well-known papers connecting LLM and robotics. An LLM outputs the scores (log-likelihoods) of the next action candidates from language instruction, which are multiplied by scores from visual affordance, and the action with the highest combined score is chosen as the action to be executed. LM-Nav [130] outputs landmarks using LLM, matches the landmarks and nodes of vision-navigation map, and executes graph search to navigate to the place specified by natural language. Inner Monologue [140] updates a task plan with an LLM using feedback from the current state description. This combines a passive scene description, an active scene description, and success detector. Hulc++ [141] combines a model-based policy guiding the robot to its vicinity with an affordance heatmap using VLM and language instruction, and language-conditioned imitation learning. For long-term task execution, the language instruction is broken down into multiple subtasks with an LLM. PIGINet [142] generates multiple plans using an LLM, scores the feasibility of each plan, and executes the best one. Grounded Decoding [143] is the evolutional version of SayCan, which does not generate the entire sentence but generates tokens successively. LLM-GROP [144] outputs how certain objects are arranged using an LLM. The LLM outputs the symbolic spatial relationship of objects, and then converts it to the geometric spatial relationship whose feasibility levels are evaluated. Finally, the feasibility and efficiency of motion plans are optimized. AVL-Maps [134] and VL-Maps [135] execute motion planning of navigation with an LLM. By combining the subgoals and a map generated with the embeddings of language, image, and audio information, a robot can navigate to appropriate places. Text2Motion [145] outputs the probability of each skill, multiplies it by geometric score, and obtains the best plan by sampling multiple plans iteratively. PET (Plan, Eliminate, and Track) [146] outputs subtasks with an LLM, eliminates unrelated objects from recognition, and tracks the state change in the objects for detecting sub-task completion. In REFLECT [92], a robot summarizes why the action failed and executes replanning. From MDETR [94], CLIP, AudioCLIP, 3D scene graph with depth camera, the current state is described, and the failure can be detected. KITE [147] calculates keypoints in images from language instructions, output actions from an LLM and primitives, and combines them for task execution. In Ren et al. [148], LLM is leveraged to execute a task plan and ask for help using conformal prediction when multiple choices of action exist. In Say- 

13 

Plan [149] a robot navigates by using an LLM and a 3D scene graph. The robot finds objects using a hierarchical 3D scene graph, replanning using a graph simulator and language feedback from failure. In Ichikura et al. [150], a diary is generated using an LLM and VLM for interaction between a human and a robot. It collects image captioning results, voice, and emotion, and summarizes them by using LLM. OK-robot [151] integrates a variety of learned models trained on publicly available data, such as CLIP, Lang-SAM, AnyGrasp [152], and OWL-ViT, to pick and drop objects in real-world environments. 

## _3.3.2. High-level Planner with Code Generation_ 

Socratic models [110] combine VLM, LLM, ALM, and external resources like web search for various applications. For robot experiments, objects are detected by a VLM, code is generated by an LLM, and motion is generated by CLIPort. ProgPrompt [153] outputs Python code with assertions for checking conditions from task examples and current environment information. In Wake et al. [154] and Shirasaka et al. [155], an LLM is leveraged to output JSON files of structured action plans. LLM+P [156] outputs optimal task plans by combining LLMs and PDDL [157]. The task completion rate can be improved by not directly generating language but by generating PDDL codes. In Voyager [158], to acquire new skills for MineDojo, a curriculum is output by an LLM. Feedback from the environment (such as success and failure) is added as prompt, and skill libraries are extended continuously. Source code for new skills are summarized and embedded into a latent space, which allows them to be retrieved later. ChatGPT for Robotics [159] predefines some APIs and generates source code for some motion controls automatically for Habitat [160], AirSim, Tello, and MyCobot. The platform for sharing prompt engineering results, PromptCraft, is open. Statler [161] explores using LLMs to memorize the world. By deciding the next action using an LLM (world-model writer), and by describing the current state after the action (world-model reader), better performance than code-as-policies can be obtained. In Obinata et al. [162], LLM outputs a sequence of subtasks and hierarchical finite state machines are generated to safely operate a robot over long horizons. ViLaIn [163] generates a problem description of PDDL using LLM and VLM. 

## **_3.4. Low-level Planning_** 

There are a few attempts to construct low-level planners by using foundation models. They mainly have two types of output: one is for issuing higher-level commands like footstep plans and end effector positions, and the other is for issuing the lowest-level commands, which are the joint angle commands. 

SayTap [100] generates footstep plans and target velocity for a quadruped robot using a large language model and in-context learning. It acquires policies for converting the obtained footstep plans and velocities into joint angle commands through reinforcement learning, enabling diverse walking patterns. General Pattern Machines [101] uses large language models to perform sequence transformation, completion, and improvement. It can be used for tasks such as reinforcement learning tasks like Cartpole and completing manipulation actions from human demonstrations. Prompt2Walk [164] constructs a planner utilizing LLMs to generate a gait for a quadruped robot, focusing on outputting direct joint angle commands rather than footstep plans. 

14 

## **_3.5. Data Augmentation_** 

Data augmentation is indispensable to train agents which can behave in a variety of scenarios. In particular, the augmentation of images is one of the most important processes for a generalist agent. Generally, the data augmentation of images is executed by rotating, shifting, zooming, and flipping the image, adding noise to the image, and rescaling the pixels. However, if we scale the image of a robot that acts based on the view, the relationship between visual information and behavior will be changed. Therefore, without scaling the image, various changes in the robot view must be prepared. Also, there can be many different language instructions for a robot to accomplish the same task, meaning that the language instructions should be also augmented. To solve these problems, current foundation models can be used efficiently. We introduce several studies that train a generalist agent by augmenting the camera view and language instructions. 

CACTI [109] has improved the accuracy of imitation learning with R3M or pretrained ResNet for various tasks and scenes, through image augmentation by stable diffusion [62]. ROSIE [165] has enhanced the robustness of RT-1 [166] by selecting regions with OWL-ViT [65] and then modifying and augmenting the image using Image Editor [167] and language prompts. GenAug [102] augments images to improve the robustness of imitation learning by using a pre-trained depth-guided text-to-image inpainting model [62] to change the background, add distractors, modify the object’s texture, and place different objects for image augmentation. FoundationPose [87] adapts LLM-aided texture augmentation with diffusion models for a more realistic appearance and strong generalizability. Moo [168] separates the action and object information of language instruction, masks images with object information using OWL-ViT, and generalizes to various objects by removing object information from language instruction, leaving only action information. DIAL [103] is an example of instruction augmentation, which obtains many examples of language instructions through LLM or crowdsourcing, extracts appropriate language instructions using fine-tuned CLIP for trajectory data, and uses them for imitation learning. 

## **4. Progress towards Robotic Foundation Models** 

Aside from studies focusing on leveraging foundation models for robot perception and planning, there are some works aiming to create foundation models for robotics itself, which may be referred to as _robotic foundation models_ . Developing robotic foundation models requires special considerations compared to the robotics domain compared to LLM or VLM. For example, collecting diverse datasets for robotics is more costly than for LLMs and VLMs, which can be easily trained using data collected from the internet, and this difficulty inhibits the scaling up of robotic foundation models. Also, robot systems should handle diversified types of data other than just images or text. In general, the design choices are based on reducing human labor to collect those datasets. 

## **_4.1. Approaches for Robotic Foundation Models_** 

We first categorize robotic foundation models based on their applications. Table 2 shows examples of robotic foundation models. 

15 

**Table 2.** Some examples of representative foundation models trained for robotics. The models can be categorized into three: pre-trained visual representations (PVRs) for robotics, vision language models (VLMs) for robotics, and end-to-end control policies and dynamics models. For the columns of inputs and outputs, Im, S, L, R, and A denote images, robot states, language tokens, rewards, and actions. For the column of architecture, ViT denotes Vision Transformer for vision, and T denotes Transformers. Especially for CNNs, we denote ResNet[104] as CNNR. For the training objectives, CE denotes categorical cross-entropy of discrete tokens, and BC denotes behavioral cloning loss on action space. 

|Model|Inputs|Outputs|Architecture|Objective|
|---|---|---|---|---|
|R3M [3]|Im|Latent|CNNR|Time Contrastive [169]|
|MVP [170,171]|Im|Im,Latent|ViT|MAE [172]|
|PaLM-E [173]|Im,L|L|ViT+T|CE|
|RoboVQA [174]|Im,L|L|ViT+T|CE|
|MT-Opt [175]|Im,S,A|Q-value|CNN|Q-learning|
|BC-Z [176]|Im,L|A|CNNR|Regession (BC)|
|Gato [177]|Im,S,L,A|L,A|CNNR+T|CE|
|RT-1 [166]|Im,L|A|CNN+T|CE (BC)|
|RT-2 [2]|Im,L|A|ViT+T|CE (BC)|
|Q-Transformer [178]|Im,L,A|Q-value|CNN+T|Q-learning|
|RoboCat [179]|Im,S,A|Im,A|CNNR+T|CE|
|TDMs [180]|S,R,A|S,R,A|T|CE|


## _4.1.1. Pre-trained Visual Representations for Robotics_ 

Firstly, pre-trained visual representations (PVRs) [53] for robotics have been developed and utilized. Large visual pretraining models for robotics are developed mainly for feature extraction (low-level perception in section 3.1). For example, RRL [106] utilizes pretrained CNN (ResNet [104]) with ImageNet [107] as a feature extractor for visionbased reinforcement learning. R3M [3] is a ResNet-based visual pretraining model for robot manipulation trained by ego-centric human activity videos (Ego4D [108]) with time contrastive learning [169]. VIP [128] learns features embedding of the observation utilizing time contrastive learning and defines value functions implicitly as the distance on embedding spaces. MVP [170] proposes to learn a visual pre-trained model for imitation learning using Masked Autoencoder (MAE) [172] with Vision Transformer backbones and later applied to real-world settings [171]. VC-1 [53] is a large Vision Transformer-based PVR trained with ImageNet, Ego4D, and robotic datasets of manipulation and navigation. 

## _4.1.2. Vision Language Models for Robotics_ 

The second direction of robotic foundation models is to develop (vision) language models for robotics. PaLM-E [173] is a multimodal language model, which allows multimodal inputs (e.g., images) in addition to text questions, and is trained to answer the questions. The model is an extension of PaLM [36], a large language model with language inputs. The text output (answer) can be utilized for multiple downstream tasks, for example, task and motion planning and visual question answering (VQA) [174]. RoboVQA [174] presents a scalable data collection scheme for visual question answering for robotics in addition to a large and diverse cross-embodiment video-and-text dataset. 

## _4.1.3. End-to-End Control Policies and Dynamics Models_ 

The third direction is to train control policies with large-scale datasets in an end-toend manner. This type of robotic foundation model is sometimes called as **Vision-** 

16 

**Language-Action** (VLA) model. For example, MT-Opt [175] learns a value function (Q-function) of robot manipulation tasks with a large dataset collected with seven robots and 12 tasks, and utilizes it for fast adaptation of novel tasks, ideally in zero-shot transfer if there are sufficient overlaps among tasks. BC-Z [176] learns ResNet-based language-conditional policy from large-scale dataset (more than 25k episodes) of 100 manipulation tasks with 7 DoF manipulators. The dataset is collected semi-autonomously (shared-autonomy) with HG-Dagger [181] to reduce data collection costs; they collect about 11K expert demonstrations first and the rest is collected by deploying the learned policy with the aggregated dataset. VIMA [182] learns an end-to-end visual manipulation policy regarding images in the same way as text tokens; the visual demonstrations and language instructions are tokenized and input to the model, and the model outputs discretized actions. 

**Robotics Transformers** : There is a line of works which is called as “Robotics Transformer” (RT) that learns robot control policies using transformers. RT-1 [166] learns language conditional imitation learning policy with large models (35M parameters). They collected 130k demonstrations with 13 mobile manipulators (taking 17 months) with about 750 language instructions. Recently, there have been several works extending RT-1. For example, Q-Transformer [178] extends RT-1 to offline reinforcement learning settings by learning Q-function considering offline temporal difference backup. RT-2 [2] scales up the model of RT-1 by leveraging Internet-scale visionlanguage models [173,183] and co-finetuning the model with the original dataset and datasets collected with robots (seven skills of RT-1 dataset). The model sizes are with 12B parameters for models based on PaLM-E [2] and 55B for models based on PaLI-X [183]. 

There are several works extending RT-1 and RT-2. For example, RT-Trajectory [184] extend RT-1 architecture to allow human demonstrations of the new target tasks as trajectory sketches, and similarly, RT-Sketch [185] is a goal-conditional policy which incorporates human hand-drawing of the trajectory as inputs. AutoRT [186] integrates LLMs, VLMs, and end-to-end robot control models like RT-1 and RT-2 to enable robots to gather training datasets in novel environments and scale the model itself. SARA-RT [187] proposes up-training, a novel fine-tuning methods for robotics, replacing attention blocks with lightweight ones during training, which enables massive models as RT-2 in robotics with less latency. 

RT-X [1] extends the works of RT-1 and RT-2 in terms of the datasets to train with. They collected datasets of various types of robots, environments, and tasks from more than 20 academic laboratories and trained RT-1 and RT-2 models, which can effectively generalize new robot embodiment and tasks by finetuning. Based on the models in RT-1 and datasets collected in RT-X, Octo [188] proposes the flexible architecture for new modalities of inputs and outputs such as proprioception as input and joint angle as output action. They incorporate diffusion-based policy models [189] as the action head of the model to transform the output token from Transformer models to control actions. 

**Large Models for Learning Dynamics** : Large-scale vision-language-action models are used to model not only robot policy but also the dynamics, which are used for planning. For example, Gato [177] learns control policies of diverse domains, _e.g.,_ Atari [190], DeepMind Control Suite [191], and real-world manipulation tasks [91,147,192,193] of a single model. RoboCat [179] learns dynamics models of diverse control tasks, such as pick-and-place and stacking blocks. TDMs [180] utilizes Transformer-based sequence models as dynamics models, which can be utilized as a zero-shot generalist and a fine-tuned one for control tasks. UniSim [194] is a large- 

17 

scale action-conditional video diffusion models, which can be utilized as simulators of interactions with the real world. 

In the following sections, we categorize the recipes for developing robotic foundation models in terms of model architecture (section 4.2), 

## **_4.2. Model Architectures_** 

Traditionally, the choice of deep learning model is dependent on the modalities of the input of the models; for example, CNNs are used for images and RNNs are used for sequential data such as videos and audio. Recently, as mentioned in section 2, one of the prominent characteristics of modern deep learning network architectures based on Transformers is _homogenization_ , which unifies the methodologies of deep learning for various modalities. Foundation models effectively leverage this feature to enable large-scale multi-modal models that can be shared across various domains. One of the prominent models for multi-modal input is PerceiverIO [195], which generalizes Transformer architecture and scales linearly to the size of inputs and outputs in order to accept various types of inputs such as optical flow and audio as well as texts and images. Perceiver-Actor [196] utilizes PerceiverIO as the model of the imitation leaning policy, which allows voxels from RGB-D camera of the environments and language instructions as input and outputs 6-DoF end effector pose, gripper state, and a binary state indicating motion planner for collision avoidance. 

The multi-modal inputs are fused into a feature vector to input to the model. The simplest choice of the fuse is just a concatenation of the features from different modalities. Recently, FiLM conditioning [197] is a popular choice for conditioning for two different types of features. For example, BC-Z [166,176,198] utilizes FiLM to condition visual input human demonstrations with visual observations. 

Models using transformers require tokenizations of images or actions as well as text. For the image inputs, the inputs are sometimes decomposed into patches and the features of these patches using CNNs [188] or vision transformers [2] are regarded as image tokens. Instead, RT-1 uses CNN (EfficientNet [199]) without patchfying the input images and uses the flattened feature map as visual tokens. TokenLearner [200] is often utilized for reducing dimensions to align dimensions of different modalities. For the case of RT-1 [166], TokenLearner is used to subsample visual tokens to input transformers with text token inputs. Action spaces are often uniformly discretized into bins along with the dimension to align with tokens output by transformers [2,166], while Octo [188] learns to regress the output token to action spaces using diffusion policy [189]. 

## **_4.3. Datasets and Their Collection_** 

Datasets utilized to train robotic foundation models are divided into two groups; namely _action-free datasets_ and _action-conditional datasets_ . 

With regard to action-conditional datasets, many have been released in the context of action-conditional video prediction tasks and offline reinforcement learning tasks. For example, RoboNet [201] contains videos and robot actions of table-top object manipulation tasks and has been utilized in action-conditional video prediction tasks. D4RL [202] is a dataset containing several robot control tasks collected in simulators and has been leveraged as a benchmark of offline reinforcement learning tasks [203– 205]. 

18 

Recently, more diverse and large-scale datasets have been made public and utilized for training end-to-end foundation models. For example, Bridge Data [206,207] contains real-world object manipulation data using a 6-DoF WidowX250 robot arm. Datasets used in RT-1 [166] are publicly released and utilized in subsequent studies [2,178]. The dataset is collected with human experts and a language description of each task is added. RT-X [1] utilizes cross-domain datasets, namely Open X-Embodiement (OXE) datasets, collected with 22 different robots from 21 institutions. The dataset contains more than 1M episodes of 527 skills (160,266 tasks). 

For the ease of collecting expert demonstration datasets with real robots, robot teleoperation systems suitable for collecting datasets have been proposed. For instance, ALOHA [208] is a bimanual teleoperation system with low-cost hardware. Mobile ALOHA [209] incorporates ALOHA system into a mobile robot to enable teleoperation of bimanual mobile manipulator. GELLO [210] proposes a framework for teleoperation of robot arms to collect high-quality datasets with low-cost hardware parts. 

Action-free datasets are relatively easier to collect and transfer among different types of robot morphologies, but, low-level actions cannot be directly obtained from the learned model. Since action-conditional datasets are often dependent on the robot, the action is often generalized (e.g. end-effector pose for object manipulation task). Some studies combine these two groups of datasets for training. The typical type of action-free dataset for a robotic foundation model is a video dataset. For example, Ego4D [108] is a large (3,740 hours) egocentric video dataset of human daily behavior collected across 74 locations. 

## **_4.4. Learning Objectives_** 

In order to train end-to-end robot control models, a simple behavioral cloning (BC) loss on action spaces are often used; for example, BC-Z [176] uses regression loss on action spaces, and RT-1 [166] and RT-2 [2] use categorical cross-entropy loss on discretized action tokens as next token prediction of actions. MT-Opt [175] and Q-Transformer learns value function using TD-Learning as is often with Q-learning in reinforcement learning [211]. However, some recent works like Gato [177] learn to predict the entire trajectory not just the next action or Q-value. There are some works extending the idea of masked prediction models like BERT [45] to robot trajectories such as Unimask [212] and Masked Trajectory Models [213]. By masking tokens in trajectories (observations, actions, rewards, returns, etc.) during training, the various learning objectives on robot trajectories such as behavioral cloning, offline reinforcement learning, and forward dynamics, can be written as the same framework. This formulation can be seen as self-supervised learning on robot trajectories. 

## **5. Robots, Tasks, and Environments** 

From the studies where foundation models are applied, we can know what kind of robots, tasks, and environments are suitable for foundation model-based robotics. In this study, various studies are classified based on the tasks performed by robots. They are primarily classified into four categories: navigation, manipulation, locomotion, and communication. Communication often involves scenarios where robots are not explicitly utilized, and its description is kept to a minimum. Since navigation and manipulation make up the majority of the tasks, we will discuss five tasks, including those four tasks and navigation with manipulation, which deals with both navigation and 

19 

manipulation simultaneously, as shown in Figure 5. Note that, in this section, we handle only tasks and robots that handle the actual robots, not simulation. Additionally, while there have been many studies on robot behavior using language before the advent of foundation models [214,215], we will focus here solely on the current research landscape utilizing these models. 


**Figure 5.** The overview of robots, tasks, and environments used for research with foundation models. 

## **_5.1. Navigation_** 

Research on navigation includes studies that focus on generating maps and those that also involve path planning. Mainly, research focused on map generation includes VL-Maps [135], AVL-Maps [134], CLIP on Wheels [131], ConceptFusion [136], ConceptGraphs [138], and CLIP-Fields [96]. These studies use embeddings of CLIP [28], LSeg [67], AudioCLIP [72], etc. to generate maps and obtain suitable destinations from language instruction. On the other hand, LM-Nav [130] utilizes an LLM and VLM to perform path planning. In efforts to create foundation models for navigation, there are also studies like GNM [216] and ViNT [217]. Additionally, in [159], code generation is conducted for the navigation of the drone Tello. While there is extensive research on map construction indoors, LM-Nav, GNM and ViNT conduct experiments outdoors. Robots such as Clearpath Ridgeback, Clearpath Jackal, Clearpath Warthog, Stretch, HSR, DJI Tello, TurtleBot, Spot, and Unitree are commonly used in these studies. 

## **_5.2. Manipulation_** 

Research on manipulation is the most extensive. Most studies focus on single-arm manipulation and grasping, but there are also studies that deal with dual-arm systems [1,148] and in-hand manipulation [170]. Additionally, the research often takes place in everyday environments, including kitchens and tabletops, although some studies focus on laboratory automation [218]. The tasks covered are primarily pick-andplace, but many studies also report on obstacle avoidance, path planning, and flexible object manipulation. Commonly used robotic platforms include Panda, Kinova Series, UR Series, xarm, EDR, mycobot, KUKA, sawyer, and arms using dynamixel servo motors (WidowX, ViperX, etc.). In terms of end effectors, researchers use not only the robot’s built-in hands but also robotiq hands, allegro hands, and custom soft hands. There are relatively few studies that utilize custom-designed individual arms. 

20 

## **_5.3. Navigation with Manipulation_** 

Research that combines navigation and manipulation is actively conducted. All of this research is conducted indoors and deals with both navigation and pick-and-place grasping, either by combining an LLM and VLM [4,5,18,111,114,140,143,148,149,151,155, 162,219,220], or by simultaneously handling mobile base motion and grasping through the construction of Robotic Foundation Models [2,166,173]. Various robots are used for these purposes, including EDR, single-arm manipulators (e.g. Kinova or Panda) with UGV (e.g. custom mobile platform or Omron mobile platform), Stretch, Fetch, HSR, etc. 

## **_5.4. Locomotion_** 

There is relatively little research on using foundation models for locomotion. This is likely to be due to the difficulty of expressing leg movements in language. Among them, two studies, SayTap [100] and Language to Rewards [122], use foundation models for locomotion. SayTap generates footstep plans, while Language to Rewards generates rewards or constraints for reinforcement learning or model predictive control, by utilizing LLM. Instead of directly handling leg movements, it is common to implicitly adjust leg movements through some abstract layers. Currently, most of the robots under research in the field of locomotion are quadruped robots, such as Unitree, and research on bipedal robots like humans is lacking. 

## **_5.5. Communication_** 

There is a considerable amount of research on communication, but among them, studies involving actual robots, not just devices, for communication are relatively scarce. Here, we introduce interactions between embodied robots and humans involving physical contact through LLMs. Among these studies, Automatic Diary Generation [150,221] stands out for extracting appropriate scenes and imbuing emotions from data collected when robots and humans go for a walk, generating diaries to enhance intimacy with humans. In Cho and Nam [222], diaries are utilized where robots convey their experiences and perspectives to humans as an approach to form social recognition for robots. This diary generation can be considered as a form of high-level perception in our classification. Also, some studies consider human preferences [18,148]. 

## **6. Conclusion and Future Challenges** 

## **_6.1. Conclusion_** 

The application of foundation models to robotics is an exciting and fast-changing field. In this study, we have compiled various studies regarding the real-world robot applications of foundation models. Especially, we focused on how existing robot systems can be replaced by foundational models. First, to apply foundation models to real robots, we categorized them based on the perspective of the input and output modalities and their transformations. Next, we classified these foundation models based on five aspects of their application methodology to real robots: low-level perception, high-level perception, high-level planning, low-level planning, and data augmentation. Then, we categorized the patterns of the combination of these five aspects. Following that, we 

21 

summarized the construction of robotic foundation models, including actions and more, from the perspectives of model architecture, datasets, and learning objectives. Lastly, we summarized the aspects of robots, tasks, and environments that research on the real-world robot applications of foundation models covers. 

Given the rapid development of this field, it is challenging to encompass all the research papers, but it allows us to observe the trends. There are several active directions in current development. One involves the practical application of existing foundational models to robot movements, with a focus on increasing the use of different modalities. Additionally, there is a trend towards constructing robotic foundational models using more extensive data and larger models. The direction also includes building foundational models that generalize across diverse body types and exploring the use of models beyond Transformers, such as Diffusion Models. Furthermore, research on low-level motion control is still relatively scarce, and there is a limited presence of robots thriving in real household and outdoor environments. Expectations for future advancements in these areas remain high. We hope that this study will serve as a guide for future utilization of foundation models. 

## **_6.2. Future Challenges_** 

First, we discuss the real-world robot application of existing foundation models. Various foundation models for mutual conversion between different modalities have been developed, and their application to robots is advancing. However, there are still many modalities that have not been fully utilized. Particularly, depth information, force feedback, inertial sensors, and motion information of humans, objects, and robots are not fully exploited, despite the existence of diverse examples for language, image, and sound information. Additionally, there are issues related to the granularity of skills for motion planning. The hierarchical organization of robot skills, how to structure the skill API at what level of granularity, and the addition of new skills are expected to be significant focus areas in the future. 

Second, we elaborate on the robotic foundation models. While diverse robotic foundation models have been developed, their control frequencies are exceptionally slow. These current models are not suitable for tasks that require fine-grained force control or collaboration with humans. There is room for studies about which action spaces are suitable for these end-to-end control policies and how to reduce safety risks with robotics foundation models. 

Next, we discuss practical robot applications across the entire spectrum. Through various studies, it has been observed that there are few research examples in outdoor settings, and many setups lack reflection of real-world environments, often consisting of toy problems. The use of off-the-shelf robots limits diversity. Furthermore, most setups are primarily based on position control, with few examples utilizing torque control or soft robots. It is anticipated that in the future, robots developed by various research institutions will integrate with foundation models, and there will be an increase in examples of operation in more realistic environments. 

Next, the generalization ability of robots using foundation models to various environments and tasks is a future challenge. Currently, examples of applying foundation models to open-world environments, such as OVMM [220], OK-Robot [151], and GOAT [223], are increasing. We believe this direction represents a significant advancement towards new robots that go beyond the capabilities of traditional robots. 

Lastly, as tasks executed through language instructions become more prevalent, 

22 

quantitative evaluation of performance becomes challenging. Benchmarks such as CALVIN [224] and ARNOLD [225], which perform language instruction tasks in simulators for evaluation, have emerged. Achieving a fair evaluation in the real world, however, is not easy. Additionally, there is a need to contemplate how to evaluate interactions with humans. 

23 

## **References** 

- [1] Open X-Embodiment Collaboration, Abhishek Padalkar, Acorn Pooley, Ajinkya Jain, Alex Bewley, Alex Herzog, Alex Irpan, Alexander Khazatsky, Anant Rai, Anikait Singh, Anthony Brohan, Antonin Raffin, Ayzaan Wahid, Ben BurgessLimerick, Beomjoon Kim, Bernhard Sch¨olkopf, Brian Ichter, Cewu Lu, Charles Xu, Chelsea Finn, Chenfeng Xu, Cheng Chi, Chenguang Huang, Christine Chan, Chuer Pan, Chuyuan Fu, Coline Devin, Danny Driess, Deepak Pathak, Dhruv Shah, Dieter B¨uchler, Dmitry Kalashnikov, Dorsa Sadigh, Edward Johns, Federico Ceola, Fei Xia, Freek Stulp, Gaoyue Zhou, Gaurav S Sukhatme, Gautam Salhotra, Ge Yan, Giulio Schiavi, Hao Su, Hao-Shu Fang, Haochen Shi, Heni Ben Amor, Henrik I Christensen, Hiroki Furuta, Homer Walke, Hongjie Fang, Igor Mordatch, Ilija Radosavovic, Isabel Leal, Jacky Liang, Jaehyung Kim, Jan Schneider, Jasmine Hsu, Jeannette Bohg, Jeffrey Bingham, Jiajun Wu, Jialin Wu, Jianlan Luo, Jiayuan Gu, Jie Tan, Jihoon Oh, Jitendra Malik, Jonathan Tompson, Jonathan Yang, Joseph J Lim, Jo˜ao Silv´erio, Junhyek Han, Kanishka Rao, Karl Pertsch, Karol Hausman, Keegan Go, Keerthana Gopalakrishnan, Ken Goldberg, Kendra Byrne, Kenneth Oslund, Kento Kawaharazuka, Kevin Zhang, Keyvan Majd, Krishan Rana, Krishnan Srinivasan, Lawrence Yunliang Chen, Lerrel Pinto, Liam Tan, Lionel Ott, Lisa Lee, Masayoshi Tomizuka, Maximilian Du, Michael Ahn, Mingtong Zhang, Mingyu Ding, Mohan Kumar Srirama, Mohit Sharma, Moo Jin Kim, Naoaki Kanazawa, Nicklas Hansen, Nicolas Heess, Nikhil J Joshi, Niko Suenderhauf, Norman Di Palo, Nur Muhammad Mahi Shafiullah, Oier Mees, Oliver Kroemer, Pannag R Sanketi, Paul Wohlhart, Peng Xu, Pierre Sermanet, Priya Sundaresan, Quan Vuong, Rafael Rafailov, Ran Tian, Ria Doshi, Roberto Mart´ın-Mart´ın, Russell Mendonca, Rutav Shah, Ryan Hoque, Ryan Julian, Samuel Bustamante, Sean Kirmani, Sergey Levine, Sherry Moore, Shikhar Bahl, Shivin Dass, Shuran Song, Sichun Xu, Siddhant Haldar, Simeon Adebola, Simon Guist, Soroush Nasiriany, Stefan Schaal, Stefan Welker, Stephen Tian, Sudeep Dasari, Suneel Belkhale, Takayuki Osa, Tatsuya Harada, Tatsuya Matsushima, Ted Xiao, Tianhe Yu, Tianli Ding, Todor Davchev, Tony Z Zhao, Travis Armstrong, Trevor Darrell, Vidhi Jain, Vincent Vanhoucke, Wei Zhan, Wenxuan Zhou, Wolfram Burgard, Xi Chen, Xiaolong Wang, Xinghao Zhu, Xuanlin Li, Yao Lu, Yevgen Chebotar, Yifan Zhou, Yifeng Zhu, Ying Xu, Yixuan Wang, Yonatan Bisk, Yoonyoung Cho, Youngwoon Lee, Yuchen Cui, Yueh-hua Wu, Yujin Tang, Yuke Zhu, Yunzhu Li, Yusuke Iwasawa, Yutaka Matsuo, Zhuo Xu, and Zichen Jeff Cui. Open X-Embodiment: Robotic Learning Datasets and RT-X Models. _arXiv preprint arXiv:2310.08864_ , 2023. 

- [2] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, Pete Florence, Chuyuan Fu, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Kehang Han, Karol Hausman, Alex Herzog, Jasmine Hsu, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Isabel Leal, Lisa Lee, Tsang-Wei Edward Lee, Sergey Levine, Yao Lu, Henryk Michalewski, Igor Mordatch, Karl Pertsch, Kanishka Rao, Krista Reymann, Michael Ryoo, Grecia Salazar, Pannag Sanketi, Pierre Sermanet, Jaspiar Singh, Anikait Singh, Radu Soricut, Huong Tran, Vincent Vanhoucke, Quan Vuong, Ayzaan Wahid, Stefan Welker, Paul Wohlhart, Jialin Wu, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Tianhe Yu, and Brianna Zitkovich. RT-2: VisionLanguage-Action Models Transfer Web Knowledge to Robotic Control. In _Pro-_ 

24 

   - _ceedings of The 7th Conference on Robot Learning_ , pages 2165–2183, 2023. 

- [3] Suraj Nair, Aravind Rajeswaran, Vikash Kumar, Chelsea Finn, and Abhinav Gupta. R3M: A Universal Visual Representation for Robot Manipulation. In _6th Annual Conference on Robot Learning_ , 2022. URL `https://openreview. net/forum?id=tGbpgz6yOrI` . 

- [4] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng. Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. In _Proceedings of The 6th Conference on Robot Learning_ , pages 287–318. PMLR, 2022. 

- [5] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as Policies: Language Model Programs for Embodied Control. In _IEEE International Conference on Robotics and Automation_ , 2023. 

- [6] Ruchi Goel and Pooja Gupta. Robotics and industry 4.0. _A Roadmap to Industry 4.0: Smart Production, Sharp Business and Sustainable Development_ , pages 157– 169, 2020. 

- [7] Martin H¨agele, Klas Nilsson, J Norberto Pires, and Rainer Bischoff. Industrial robotics. _Springer handbook of robotics_ , pages 1385–1422, 2016. 

- [8] Naoshi Kondo and K C Ting. Robotics for plant production. _Artificial intelligence review_ , 12:227–243, 1998. 

- [9] Yoram Koren, Yoram Koren, and others. _Robotics for engineers_ , volume 168. McGraw-Hill New York, 1985. 

- [10] Koen De Backer, Timothy DeStefano, Carlo Menon, and Jung Ran Suh. Industrial robotics and the global organisation of production. _OECD_ , 2018. URL `https://www.oecd-ilibrary.org/content/paper/dd98ff58-en` . 

- [11] Guoqiang Ren, Tao Lin, Yibin Ying, Girish Chowdhary, and K C Ting. Agricultural robotics research applicable to poultry production: A review. _Computers and Electronics in Agriculture_ , 169:105216, 2020. 

- [12] Bill Gates. A robot in every home. _Scientific American_ , 296(1):58–65, 2007. [13] Cory D Kidd and Cynthia Breazeal. Robots at home: Understanding longterm human-robot interaction. In _2008 IEEE/RSJ International Conference on Intelligent Robots and Systems_ , pages 3230–3235, 2008. 

- [14] Robin R Murphy, Satoshi Tadokoro, and Alexander Kleiner. Disaster robotics. _Springer handbook of robotics_ , pages 1577–1604, 2016. 

- [15] Jennifer L Burke, Robin R Murphy, Michael D Coovert, and Dawn L Riddle. Moonlight in Miami: Field study of human-robot interaction in the context of an urban search and rescue disaster response training exercise. _Human-Computer Interaction_ , 19(1-2):85–116, 2004. 

- [16] Nichola Abdo, Cyrill Stachniss, Luciano Spinello, and Wolfram Burgard. Robot, organize my shelves! Tidying up objects by predicting user preferences. In _2015 IEEE international conference on robotics and automation (ICRA)_ , pages 1557– 1564, 2015. 

- [17] Tatsuya Matsushima, Yuki Noguchi, Jumpei Arima, Toshiki Aoki, Yuki Okita, 

25 

Yuya Ikeda, Koki Ishimoto, Shohei Taniguchi, Yuki Yamashita, Shoichi Seto, and others. World robot challenge 2020–partner robot: a data-driven approach for room tidying with mobile manipulator. _Advanced Robotics_ , 36(17-18):850–869, 2022. 

- [18] Jimmy Wu, Rika Antonova, Adam Kan, Marion Lepert, Andy Zeng, Shuran Song, Jeannette Bohg, Szymon Rusinkiewicz, and Thomas Funkhouser. TidyBot: Personalized Robot Assistance with Large Language Models. _Autonomous Robots_ , 2023. 

- [19] Emanuela Marchetti, Sophie Grimme, Eva Hornecker, Avgi Kollakidou, and Philipp Graf. Pet-robot or appliance? Care home residents with dementia respond to a zoomorphic floor washing robot. In _Proceedings of the 2022 CHI Conference on Human Factors in Computing Systems_ , pages 1–21, 2022. 

- [20] Nazim Mir-Nasiri, Hudyjaya Siswoyo, and Md Hazrat Ali. Portable autonomous window cleaning robot. _Procedia computer science_ , 133:197–204, 2018. 

- [21] Daniel Leidner, Georg Bartels, Wissam Bejjani, Alin Albu-Sch¨affer, and Michael Beetz. Cognition-enabled robotic wiping: Representation, planning, execution, and interpretation. _Robotics and Autonomous Systems_ , 114:199–216, 2019. 

- [22] Madhura Thosar, Sebastian Zug, Alpha Mary Skaria, and Akshay Jain. A Review of Knowledge Bases for Service Robots in Household Environments. In _AIC_ , pages 98–110, 2018. 

- [23] Mario Bollini, Stefanie Tellex, Tyler Thompson, Nicholas Roy, and Daniela Rus. Interpreting and executing recipes with a cooking robot. In _Experimental Robotics: The 13th International Symposium on Experimental Robotics_ , pages 481–495, 2013. 

- [24] Yuta Sugiura, Daisuke Sakamoto, Anusha Withana, Masahiko Inami, and Takeo Igarashi. Cooking with robots: designing a household system working in open environments. In _Proceedings of the SIGCHI conference on human factors in computing systems_ , pages 2427–2430, 2010. 

- [25] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon, Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Demszky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar Khattab, Pang Wei Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal Ladhak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak Narayanan, Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian Nyarko, Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung Park, Chris Piech, Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher R´e, Dorsa Sadigh, Shiori Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Rohan Taori, Armin W. Thomas, Florian Tram`er, Rose E. Wang, William Wang, Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi 

26 

Zhang, Xikun Zhang, Yuhui Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang. On the Opportunities and Risks of Foundation Models. _arXiv preprint_ , 2021. 

- [26] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Zhiyong Wu, Baobao Chang, Xu Sun, Jingjing Xu, and Zhifang Sui. A survey for in-context learning. _arXiv preprint arXiv:2301.00234_ , 2022. 

- [27] OpenAI. GPT-4 Technical Report. Technical report, 2023. 

- [28] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning Transferable Visual Models From Natural Language Supervision. In _International conference on machine learning_ , pages 8748–8763. PMLR, 2021. 

- [29] Jiaqi Wang, Zihao Wu, Yiwei Li, Hanqi Jiang, Peng Shu, Enze Shi, Huawen Hu, Chong Ma, Yiheng Liu, Xuhui Wang, Yincheng Yao, Xuan Liu, Huaqin Zhao, Zhengliang Liu, Haixing Dai, Lin Zhao, Bao Ge, Xiang Li, Tianming Liu, and Shu Zhang. Large Language Models for Robotics: Opportunities, Challenges, and Perspectives. _arXiv preprint_ , 2024. 

- [30] Fanlong Zeng, Wensheng Gan, Yongheng Wang, Ning Liu, and Philip S Yu. Large Language Models for Robotics: A Survey. _arXiv preprint_ , 2023. 

- [31] Roya Firoozi, Johnathan Tucker, Stephen Tian, Anirudha Majumdar, Jiankai Sun, Weiyu Liu, Yuke Zhu, Shuran Song, Ashish Kapoor, Karol Hausman, Brian Ichter, Danny Driess, Jiajun Wu, Cewu Lu, and Mac Schwager. Foundation Models in Robotics: Applications, Challenges, and the Future. _arXiv preprint_ , 2023. 

- [32] Yafei Hu, Quanting Xie, Vidhi Jain, Jonathan Francis, Jay Patrikar, Nikhil Keetha, Seungchan Kim, Yaqi Xie, Tianyi Zhang, Shibo Zhao, Yu Quan Chong, Chen Wang, Katia Sycara, Matthew Johnson-Roberson, Dhruv Batra, Xiaolong Wang, Sebastian Scherer, Zsolt Kira, Fei Xia, and Yonatan Bisk. Toward General-Purpose Robots via Foundation Models: A Survey and Meta-Analysis. _arXiv preprint_ , 2023. 

- [33] Ling Yang, Zhilong Zhang, Yang Song, Shenda Hong, Runsheng Xu, Yue Zhao, Wentao Zhang, Bin Cui, and Ming-Hsuan Yang. Diffusion models: A comprehensive survey of methods and applications. _ACM Computing Surveys_ , 2022. 

- [34] Lu Yuan, Dongdong Chen, Yi-Ling Chen, Noel Codella, Xiyang Dai, Jianfeng Gao, Houdong Hu, Xuedong Huang, Boxin Li, Chunyuan Li, and others. Florence: A new foundation model for computer vision. _arXiv preprint arXiv:2111.11432_ , 2021. 

- [35] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In _Advances in neural information processing systems 33_ , pages 1877–1901, 2020. 

- [36] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, 

27 

Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. PaLM: Scaling Language Modeling with Pathways. _J. Mach. Learn. Res._ , 24 (240):1–113, 2023. 

- [37] Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona Diab, Xian Li, Xi Victoria Lin, and others. Opt: Open pre-trained transformer language models. _arXiv preprint arXiv:2205.01068_ , 2022. 

- [38] Aohan Zeng, Xiao Liu, Zhengxiao Du, Zihan Wang, Hanyu Lai, Ming Ding, Zhuoyi Yang, Yifan Xu, Wendi Zheng, Xiao Xia, and others. Glm-130b: An open bilingual pre-trained model. _arXiv preprint arXiv:2210.02414_ , 2022. 

- [39] Teven Le Scao, Angela Fan, Christopher Akiki, Ellie Pavlick, Suzana Ili´c, Daniel Hesslow, Roman Castagn´e, Alexandra Sasha Luccioni, Fran¸cois Yvon, Matthias Gall´e, and others. Bloom: A 176b-parameter open-access multilingual language model. _arXiv preprint arXiv:2211.05100_ , 2022. 

- [40] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, and others. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- [41] Rohan Anil, Andrew M Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng Chen, and others. Palm 2 technical report. _arXiv preprint arXiv:2305.10403_ , 2023. 

- [42] Simon Thibault, Rapha¨el Py, Angelo Mattia Gervasi, Romeo Salemme, Eric Koun, Martin L¨ovden, V´eronique Boulenger, Alice C. Roy, and Claudio Brozzoli. Tool use and language share syntactic processes and neural patterns in the basal ganglia. _Science_ , 374(6569), 2021. ISSN 0036-8075. . 

- [43] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E. Hinton. ImageNet classification with deep convolutional neural networks. In _Advances in neural information processing systems_ , volume 60, 2012. 

- [44] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention Is All You Need. In _Proceedings of the 31st International Conference on Neural Information Processing Systems_ , pages 6000–6010, 2017. 

- [45] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In _Proceedings of NAACL-HLT_ , pages 4171–4186, 2019. 

- [46] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, and others. An image is worth 16x16 words: Transformers for image recognition at scale. In _International Conference on Learning Representations_ , 2021. URL `https://openreview.net/forum?id=YicbFdNTTy` . 

- [47] Gwern. GPT-3 Creative Fiction, 2021. URL `https://www.gwern.net/GPT-3` . 

- [48] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, 

28 

Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating Large Language Models Trained on Code. _arXiv preprint_ , 2021. 

- [49] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman Goyal, Eric Hambro, Faisal Azhar, and others. Llama: Open and efficient foundation language models. _arXiv preprint arXiv:2302.13971_ , 2023. 

- [50] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners. _Advances in neural information processing systems_ , 35:22199–22213, 2022. 

- [51] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, and others. Chain-of-thought prompting elicits reasoning in large language models. _Advances in Neural Information Processing Systems_ , 35:24824–24837, 2022. 

- [52] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. RoBERTa: A robustly optimized BERT pretraining approach. _arXiv preprint_ , 2019. ISSN 23318422. 

- [53] Arjun Majumdar, Karmesh Yadav, Sergio Arnaud, Yecheng Jason Ma, Claire Chen, Sneha Silwal, Aryan Jain, Vincent-Pierre Berges, Pieter Abbeel, Jitendra Malik, and others. Where are we in the search for an Artificial Visual Cortex for Embodied Intelligence? In _Workshop on Reincarnating Reinforcement Learning at ICLR 2023_ , 2023. URL `https://openreview.net/forum?id=NJtSbIWmt2T` . 

- [54] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Doll´ar, and Ross Girshick. Segment Anything. _arXiv preprint_ , 2023. 

- [55] Jinyu Yang, Mingqi Gao, Zhe Li, Shang Gao, Fangjing Wang, and Feng Zheng. Track anything: Segment anything meets videos. _arXiv preprint_ , 2023. 

- [56] Chaoning Zhang, Dongshen Han, Yu Qiao, Jung Uk Kim, Sung-Ho Bae, Seungkyu Lee, and Choong Seon Hong. Faster Segment Anything: Towards Lightweight SAM for Mobile Applications. _arXiv preprint_ , 2023. 

- [57] Liunian Harold Li, Pengchuan Zhang, Haotian Zhang, Jianwei Yang, Chunyuan Li, Yiwu Zhong, Lijuan Wang, Lu Yuan, Lei Zhang, Jenq-Neng Hwang, and others. Grounded language-image pre-training. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 10965–10975, 2022. 

- [58] Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. _arXiv preprint arXiv:2301.12597_ , 2023. 

- [59] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda Han, Zhitao Gong, Sina 

29 

Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andrew Brock, Aida Nematzadeh, Sahand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira, Oriol Vinyals, Andrew Zisserman, and Karen Simonyan. Flamingo: a Visual Language Model for Few-Shot Learning. In _Advances in Neural Information Processing Systems_ , pages 23716–23736, 2022. 

- [60] Peng Wang, An Yang, Rui Men, Junyang Lin, Shuai Bai, Zhikang Li, Jianxin Ma, Chang Zhou, Jingren Zhou, and Hongxia Yang. Ofa: Unifying architectures, tasks, and modalities through a simple sequence-to-sequence learning framework. In _International Conference on Machine Learning_ , pages 23318–23340, 2022. 

- [61] Jiasen Lu, Christopher Clark, Rowan Zellers, Roozbeh Mottaghi, and Aniruddha Kembhavi. UNIFIED-IO: A Unified Model for Vision, Language, and Multimodal Tasks. In _The Eleventh International Conference on Learning Representations_ , 2023. URL `https://openreview.net/forum?id=E01k9048soZ` . 

- [62] Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. High-Resolution Image Synthesis with Latent Diffusion Models. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2022. 

- [63] Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. Zero-Shot Text-to-Image Generation. In _International Conference on Machine Learning_ , pages 8821–8831. PMLR, 2021. 

- [64] Xingyi Zhou, Rohit Girdhar, Armand Joulin, Philipp Kr¨ahenb¨uhl, and Ishan Misra. Detecting Twenty-thousand Classes using Image-level Supervision. In _ECCV_ , 2022. 

- [65] Matthias Minderer, Alexey Gritsenko, Austin Stone, Maxim Neumann, Dirk Weissenborn, Alexey Dosovitskiy, Aravindh Mahendran, Anurag Arnab, Mostafa Dehghani, Zhuoran Shen, Xiao Wang, Xiaohua Zhai, Thomas Kipf, and Neil Houlsby. Simple Open-Vocabulary Object Detection with Vision Transformers. In _European Conference on Computer Vision_ , 2022. 

- [66] Tianyi Liu, Zuxuan Wu, Wenhan Xiong, Jingjing Chen, and Yu-Gang Jiang. Unified multimodal pre-training and prompt-based tuning for vision-language understanding and generation. _arXiv preprint arXiv:2112.05587_ , 2021. 

- [67] Boyi Li, Kilian Q Weinberger, Serge Belongie, Vladlen Koltun, and Rene Ranftl. Language-driven Semantic Segmentation. In _International Conference on Learning Representations_ , 2022. URL `https://openreview.net/forum?id= RriDjddCLN` . 

- [68] Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin ElNouby, Mahmoud Assran, Nicolas Ballas, Wojciech Galuba, Russell Howes, PoYao Huang, Shang-Wen Li, Ishan Misra, Michael Rabbat, Vasu Sharma, Gabriel Synnaeve, Hu Xu, Herv´e Jegou, Julien Mairal, Patrick Labatut, Armand Joulin, Piotr Bojanowski, and Meta Ai Research. DINOv2: Learning Robust Visual Features without Supervision. _arXiv preprint_ , 2023. 

- [69] Yiwei Ma, Guohai Xu, Xiaoshuai Sun, Ming Yan, Ji Zhang, and Rongrong Ji. X-clip: End-to-end multi-grained contrastive learning for video-text retrieval. In _Proceedings of the 30th ACM International Conference on Multimedia_ , pages 638–647, 2022. 

- [70] Wenhao Chai, Xun Guo, Gaoang Wang, and Yan Lu. Stablevideo: Text-driven consistency-aware diffusion video editing. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 23040–23050, 2023. 

30 

- [71] Benjamin Elizalde, Soham Deshmukh, Mahmoud Al Ismail, and Huaming Wang. CLAP: Learning Audio Concepts from Natural Language Supervision. In _ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ , pages 1–5, 2023. 

- [72] Andrey Guzhov, Federico Raue, J¨orn Hees, and Andreas Dengel. Audioclip: Extending clip to image, text and audio. In _ICASSP 2022-2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)_ , pages 976–980, 2022. 

- [73] Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever. Robust speech recognition via large-scale weak supervision. In _International Conference on Machine Learning_ , pages 28492–28518, 2023. 

- [74] Andrea Agostinelli, Timo I Denk, Zal´an Borsos, Jesse Engel, Mauro Verzetti, Antoine Caillon, Qingqing Huang, Aren Jansen, Adam Roberts, Marco Tagliasacchi, and others. MusicLM: Generating music from text. _arXiv preprint_ , 2023. 

- [75] Chengyi Wang, Sanyuan Chen, Yu Wu, Ziqiang Zhang, Long Zhou, Shujie Liu, Zhuo Chen, Yanqing Liu, Huaming Wang, Jinyu Li, and others. Neural codec language models are zero-shot text to speech synthesizers. _arXiv preprint_ , 2023. 

- [76] Sihan Chen, Handong Li, Qunbo Wang, Zijia Zhao, Mingzhen Sun, Xinxin Zhu, and Jing Liu. Vast: A vision-audio-subtitle-text omni-modality foundation model and dataset. _Advances in Neural Information Processing Systems_ , 36, 2024. 

- [77] Le Xue, Mingfei Gao, Chen Xing, Roberto Mart´ın-Mart´ın, Jiajun Wu, Caiming Xiong, Ran Xu, Juan Carlos Niebles, and Silvio Savarese. ULIP: Learning a unified representation of language, images, and point clouds for 3D understanding. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 1179–1189, 2023. 

- [78] Deepti Hegde, Jeya Maria Jose Valanarasu, and Vishal Patel. Clip goes 3d: Leveraging prompt tuning for language grounded 3d recognition. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 2028– 2038, 2023. 

- [79] Tong Wu, Jiarui Zhang, Xiao Fu, Yuxin Wang, Jiawei Ren, Liang Pan, Wayne Wu, Lei Yang, Jiaqi Wang, Chen Qian, and others. Omniobject3d: Largevocabulary 3d object dataset for realistic perception, reconstruction and generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 803–814, 2023. 

- [80] Alex Nichol, Heewoo Jun, Prafulla Dhariwal, Pamela Mishkin, and Mark Chen. Point-e: A system for generating 3d point clouds from complex prompts. _arXiv preprint arXiv:2212.08751_ , 2022. 

- [81] Tianshi Cao, Karsten Kreis, Sanja Fidler, Nicholas Sharp, and Kangxue Yin. Texfusion: Synthesizing 3d textures with text-guided image diffusion models. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 4169–4181, 2023. 

- [82] Yining Hong, Haoyu Zhen, Peihao Chen, Shuhong Zheng, Yilun Du, Zhenfang Chen, and Chuang Gan. 3D-LLM: Injecting the 3d world into large language models. _arXiv preprint_ , 2023. 

- [83] Songyou Peng, Kyle Genova, Chiyu Jiang, Andrea Tagliasacchi, Marc Pollefeys, Thomas Funkhouser, and others. Openscene: 3d scene understanding with open vocabularies. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 815–824, 2023. 

- [84] Boyuan Chen, Zhuo Xu, Sean Kirmani, Danny Driess, Pete Florence, Brian Ichter, Dorsa Sadigh, Leonidas Guibas, and Fei Xia. SpatialVLM: Endowing 

31 

Vision-Language Models with Spatial Reasoning Capabilities. _arXiv preprint_ , 2024. 

- [85] Rohit Girdhar, Alaaeldin El-Nouby, Zhuang Liu, Mannat Singh, Kalyan Vasudev Alwala, Armand Joulin, and Ishan Misra. Imagebind: One embedding space to bind them all. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 15180–15190, 2023. 

- [86] Yiyuan Zhang, Kaixiong Gong, Kaipeng Zhang, Hongsheng Li, Yu Qiao, Wanli Ouyang, and Xiangyu Yue. Meta-transformer: A unified framework for multimodal learning. _arXiv preprint_ , 2023. 

- [87] Bowen Wen, Wei Yang, Jan Kautz, and Stan Birchfield Nvidia. FoundationPose: Unified 6D Pose Estimation and Tracking of Novel Objects. _arXiv preprint_ , 2023. 

- [88] Guy Tevet, Sigal Raab, Brian Gordon, Yoni Shafir, Daniel Cohen-or, and Amit Haim Bermano. Human Motion Diffusion Model. In _The Eleventh International Conference on Learning Representations_ , 2023. 

- [89] Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Shaoli Huang, Yong Zhang, Hongwei Zhao, Hongtao Lu, and Xi Shen. T2M-GPT: Generating Human Motion from Textual Descriptions with Discrete Representations. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2023. 

- [90] Tenglong Ao, Zeyi Zhang, and Libin Liu. GestureDiffuCLIP: Gesture Diffusion Model with CLIP Latents. _ACM Trans. Graph._ , 42(4). 

- [91] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. CLIPort: What and Where Pathways for Robotic Manipulation. In _Proceedings of the 5th Conference on Robot Learning (CoRL)_ , 2021. 

- [92] Zeyi Liu, Arpit Bahety, and Shuran Song. REFLECT: Summarizing Robot Experiences for FaiLure Explanation and CorrecTion Examples in the RoboFail Benchmark. In _Conference on Robot Learning (CoRL)_ , 2023. URL `https: //roboreflect.github.io/` . 

- [93] Andy Zeng, Pete Florence, Jonathan Tompson, Stefan Welker, Jonathan Chien, Maria Attarian, Travis Armstrong, Ivan Krasin, Dan Duong, Ayzaan Wahid, Vikas Sindhwani, and Johnny Lee. Transporter Networks: Rearranging the Visual World for Robotic Manipulation. In _Conference on Robot Learning (CoRL)_ , 2020. 

- [94] Aishwarya Kamath, Mannat Singh, Yann LeCun, Gabriel Synnaeve, Ishan Misra, and Nicolas Carion. Mdetr-modulated detection for end-to-end multi-modal understanding. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , pages 1780–1790, 2021. 

- [95] Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, and Li FeiFei. VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models. _arXiv preprint_ , 2023. 

- [96] Nur Muhammad Mahi Shafiullah, Chris Paxton, Lerrel Pinto, Soumith Chintala, and Arthur Szlam. CLIP-Fields: Weakly Supervised Semantic Fields for Robotic Memory. In _Robotics: Science and Systems_ , 2023. 

- [97] Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Eureka: Human-Level Reward Design via Coding Large Language Models. _arXiv preprint arXiv:2310.12931_ , 2023. 

- [98] Nils Reimers and Iryna Gurevych. Sentence-bert: Sentence embeddings using siamese bert-networks. _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)_ , pages 3982–3992, 2019. URL 

32 

- `https://aclanthology.org/D19-1410` . 

- [99] Xiuye Gu, Tsung-Yi Lin, Weicheng Kuo, and Yin Cui. Open-vocabulary Object Detection via Vision and Language Knowledge Distillation. In _International Conference on Learning Representations_ , 2022. 

- [100] Yujin Tang, Wenhao Yu, Jie Tan, Heiga Zen, Aleksandra Faust, and Tatsuya Harada. SayTap: Language to Quadrupedal Locomotion. In _7th Annual Conference on Robot Learning_ , 2023. URL `https://openreview.net/forum?id= 7TYeO2XVqI` . 

- [101] Suvir Mirchandani, Fei Xia, Pete Florence, Brian Ichter, Danny Driess, Montserrat Gonzalez Arenas, Kanishka Rao, Dorsa Sadigh, and Andy Zeng. Large Language Models as General Pattern Machines. In _Proceedings of the 7th Conference on Robot Learning (CoRL)_ , 2023. 

- [102] Zoey Chen, Sho Kiami, Abhishek Gupta, and Vikash Kumar. GenAug: Retargeting behaviors to unseen situations via Generative Augmentation. In _Robotics: Science and Systems_ , 2023. 

- [103] Ted Xiao, Harris Chan, Pierre Sermanet, Ayzaan Wahid, Anthony Brohan, Karol Hausman, Sergey Levine, and Jonathan Tompson. Robotic skill acquisition via instruction augmentation with vision-language models. In _Robotics: Science and Systems_ , 2023. 

- [104] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep Residual Learning for Image Recognition. In _Proceedings of the IEEE conference on Computer Vision and Pattern Recognition_ , pages 770–778, 2016. 

- [105] Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick. Momentum contrast for unsupervised visual representation learning. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9729– 9738, 2020. 

- [106] Rutav Shah and Vikash Kumar. RRL: Resnet as representation for Reinforcement Learning. In _International Conference on Machine Learning_ . PMLR, 2021. 

- [107] Jia Deng, Wei Dong, R. Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. ImageNet: A large-scale hierarchical image database. In _2009 IEEE Conference on Computer Vision and Pattern Recognition_ , pages 248–255, 2009. 

- [108] Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu, Miguel Martin, Tushar Nagarajan, Ilija Radosavovic, Santhosh Kumar Ramakrishnan, Fiona Ryan, Jayant Sharma, Michael Wray, Mengmeng Xu, Eric Zhongcong Xu, Chen Zhao, Siddhant Bansal, Dhruv Batra, Vincent Cartillier, Sean Crane, Tien Do, Morrie Doulaty, Akshay Erapalli, Christoph Feichtenhofer, Adriano Fragomeni, Qichen Fu, Abrham Gebreselasie, Cristina Gonzalez, James Hillis, Xuhua Huang, Yifei Huang, Wenqi Jia, Weslie Khoo, Jachym Kolar, Satwik Kottur, Anurag Kumar, Federico Landini, Chao Li, Yanghao Li, Zhenqiang Li, Karttikeya Mangalam, Raghava Modhugu, Jonathan Munro, Tullie Murrell, Takumi Nishiyasu, Will Price, Paola Ruiz Puentes, Merey Ramazanova, Leda Sari, Kiran Somasundaram, Audrey Southerland, Yusuke Sugano, Ruijie Tao, Minh Vo, Yuchen Wang, Xindi Wu, Takuma Yagi, Ziwei Zhao, Yunyi Zhu, Pablo Arbelaez, David Crandall, Dima Damen, Giovanni Maria Farinella, Christian Fuegen, Bernard Ghanem, Vamsi Krishna Ithapu, C. V. Jawahar, Hanbyul Joo, Kris Kitani, Haizhou Li, Richard Newcombe, Aude Oliva, Hyun Soo Park, James M. Rehg, Yoichi Sato, Jianbo Shi, Mike Zheng Shou, Antonio Torralba, Lorenzo Torresani, Mingfei Yan, and Jitendra Malik. Ego4D: Around the World in 3,000 Hours of Egocentric Video. In _IEEE/CVF Conference on Computer_ 

33 

_Vision and Pattern Recognition (CVPR)_ , pages 18995–19012, 2022. 

- [109] Zhao Mandi, Homanga Bharadhwaj, Vincent Moens, Shuran Song, Aravind Rajeswaran, and Vikash Kumar. CACTI: A Framework for Scalable Multi-Task Multi-Scene Visual Imitation Learning. In _CoRL 2022 Workshop on Pre-training Robot Learning_ , 2022. URL `https://openreview.net/forum?id=dRHW9-QFj9` . 

- [110] Andy Zeng, Maria Attarian, Brian Ichter, Krzysztof Choromanski, Adrian Wong, Stefan Welker, Federico Tombari, Aveek Purohit, Michael Ryoo, Vikas Sindhwani, Johnny Lee, Vincent Vanhoucke, and Pete Florence. Socratic Models: Composing Zero-Shot Multimodal Reasoning with Language. In _International Conference on Learning Representations_ , 2023. 

- [111] Boyuan Chen, Fei Xia, Brian Ichter, Kanishka Rao, Keerthana Gopalakrishnan, Michael S. Ryoo, Austin Stone, and Daniel Kappler. Open-vocabulary Queryable Scene Representations for Real World Planning. In _International Conference on Robotics and Automation_ , 2023. 

- [112] Li-Heng Lin, Yuchen Cui, Yilun Hao, Fei Xia, and Dorsa Sadigh. GestureInformed Robot Assistance via Foundation Models. In _7th Annual Conference on Robot Learning_ , 2023. URL `https://openreview.net/forum?id=Ffn8Z4Q-zU` . 

- [113] Gabriel Ilharco, Mitchell Wortsman, Ross Wightman, Cade Gordon, Nicholas Carlini, Rohan Taori, Achal Dave, Vaishaal Shankar, Hongseok Namkoong, John Miller, Hannaneh Hajishirzi, Ali Farhadi, and Ludwig Schmidt. OpenCLIP, 2021. URL `https://doi.org/10.5281/zenodo.5143773` . 

- [114] Kento Kawaharazuka, Yoshiki Obinata, Naoaki Kanazawa, Kei Okada, and Masayuki Inaba. VQA-based Robotic State Recognition Optimized with Genetic Algorithm. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 8306–8311, 2023. 

- [115] Naoaki Kanazawa, Kento Kawaharazuka, Yoshiki Obinata, Kei Okada, and Masayuki Inaba. Recognition of Heat-Induced Food State Changes by TimeSeries Use of Vision-Language Model for Cooking Robot. _arXiv preprint arXiv:2309.01528_ , 2023. 

- [116] Ivan Kapelyukh, Vitalis Vosylius, and Edward Johns. DALL-E-Bot: Introducing Web-Scale Diffusion Models to Robotics. _IEEE Robotics and Automation Letters (RA-L)_ , 2023. 

- [117] Weiyu Liu, Yilun Du, Tucker Hermans, Sonia Chernova, and Chris Paxton. StructDiffusion: Language-Guided Creation of Physically-Valid Structures using Unseen Objects. In _RSS 2023_ , 2023. 

- [118] Kevin Black, Mitsuhiko Nakamoto, Pranav Atreya, Homer Walke, Chelsea Finn, Aviral Kumar, and Sergey Levine. Zero-Shot Robotic Manipulation with Pretrained Image-Editing Diffusion Models. _arXiv preprint arXiv:2310.10639_ , 2023. 

- [119] Tim Brooks, Aleksander Holynski, and Alexei A Efros. Instructpix2pix: Learning to follow image editing instructions. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18392–18402, 2023. 

- [120] Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, and Pieter Abbeel. Learning Universal Policies via Text-Guided Video Generation. _arXiv preprint_ , 2023. 

- [121] Minae Kwon, Sang Michael Xie, Kalesha Bullard, and Dorsa Sadigh. Reward Design with Language Models. In _International Conference on Learning Representations_ , 2023. 

- [122] Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, Brian Ichter, Ted Xiao, Peng Xu, Andy Zeng, Tingnan 

34 

- Zhang, Nicolas Heess, Dorsa Sadigh, Jie Tan, Yuval Tassa, and Fei Xia. Language to Rewards for Robotic Skill Synthesis. _7th Annual Conference on Robot Learning_ , 2023. URL `https://openreview.net/forum?id=SgTPdyehXMA` . 

- [123] Jessy Lin, Yuqing Du, Olivia Watkins, Danijar Hafner, Pieter Abbeel, Dan Klein, and Anca Dragan. Learning to Model the World with Language. _arXiv preprint_ , 2023. 

- [124] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering Diverse Domains through World Models. _arXiv preprint_ , 2023. 

- [125] Yuchen Cui, Scott Niekum, Abhinav Gupta, Vikash Kumar, and Aravind Rajeswaran. Can Foundation Models Perform Zero-Shot Task Specification For Robot Manipulation? In _Learning for Dynamics and Control Conference_ , pages 893–905, 2022. 

- [126] Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Antonino Furnari, Evangelos Kazakos, Jian Ma, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will Price, and Michael Wray. Rescaling Egocentric Vision: Collection, Pipeline and Challenges for EPIC-KITCHENS-100. _International Journal of Computer Vision_ , 130(1):33–55, 2022. ISSN 0920-5691. . 

- [127] Shikhar Bahl, Russell Mendonca, Lili Chen, Unnat Jain, and Deepak Pathak. Affordances from Human Videos as a Versatile Representation for Robotics. In _CVPR_ , 2023. 

- [128] Yecheng Jason Ma, Shagun Sodhani, Dinesh Jayaraman, Osbert Bastani, Vikash Kumar, and Amy Zhang. VIP: Towards Universal Visual Reward and Representation via Value-Implicit Pre-Training. In _International Conference on Learning Representations_ , 2023. 

- [129] Yecheng Jason Ma, William Liang, Vaidehi Som, Vikash Kumar, Amy Zhang, Osbert Bastani, and Dinesh Jayaraman. LIV: Language-Image Representations and Rewards for Robotic Control. In _International Conference on Machine Learning_ , 2023. 

- [130] Dhruv Shah, Blazej Osinski, Brian Ichter, and Sergey Levine. LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action. In _6th Annual Conference on Robot Learning_ , 2022. 

- [131] Samir Yitzhak Gadre, Mitchell Wortsman, Gabriel Ilharco, Ludwig Schmidt, and Shuran Song. Clip on wheels: Zero-shot object navigation as object localization and exploration. _arXiv preprint arXiv:2203.10421_ , 3(4):7, 2022. 

- [132] Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis. In _ECCV_ , volume 12346 LNCS, 2020. . 

- [133] Thomas M¨uller, Alex Evans, Christoph Schied, and Alexander Keller. Instant neural graphics primitives with a multiresolution hash encoding. _ACM Transactions on Graphics_ , 41(4):1–15, 2022. 

- [134] Chenguang Huang, Oier Mees, Andy Zeng, and Wolfram Burgard. Audio Visual Language Maps for Robot Navigation. In _International Symposium on Experimental Robotics (ISER)_ , 2023. 

- [135] Chenguang Huang, Oier Mees, Andy Zeng, and Wolfram Burgard. Visual Language Maps for Robot Navigation. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [136] Krishna Murthy Jatavallabhula, Alihusein Kuwajerwala, Qiao Gu, Mohd Omama, Tao Chen, Alaa Maalouf, Shuang Li, Ganesh Subramanian Iyer, Nikhil Varma Keetha, Ayush Tewari, Joshua B Tenenbaum, Celso M de Melo, Madhava Krishna, Liam Paull, Florian Shkurti, and Antonio Torralba. Concept- 

35 

- Fusion: Open-set Multimodal 3D Mapping. In _Robotics: Science and Systems (RSS) 2023_ , 2023. 

- [137] Kashu Yamazaki, Taisei Hanyu, Khoa Vo, Thang Pham, Minh Tran, Gianfranco Doretto, Anh Nguyen, and Ngan Le. Open-Fusion: Real-time Open-Vocabulary 3D Mapping and Queryable Scene Representation. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2024. 

- [138] Qiao Gu, Alihusein Kuwajerwala, Krishna Murthy Jatavallabhula, Bipasha Sen, Aditya Agarwal, Corban Rivera, William Paul, Rama Chellappa, Chuang Gan, Celso M de Melo, Joshua B Tenenbaum, Antonio Torralba, Florian Shkurti, and Liam Paull. ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning. In _2nd Workshop on Language and Robot Learning: Language as Grounding_ , 2023. URL `https://openreview.net/forum?id=QVbHQ33R0x` . 

- [139] Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot planners: Extracting actionable knowledge for embodied agents. In _International Conference on Machine Learning_ , pages 9118–9147, 2022. 

- [140] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, and Karol Hausman. Inner Monologue: Embodied Reasoning through Planning with Language Models. In _Conference on Robot Learning_ , 2022. 

- [141] Oier Mees, Jessica Borja-Diaz, and Wolfram Burgard. Grounding Language with Visual Affordances over Unstructured Data. In _IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [142] Zhutian Yang, Caelan Reed Garrett, Tom´as Lozano-P´erez, Leslie Kaelbling, and Dieter Fox. Sequence-Based Plan Feasibility Prediction for Efficient Task and Motion Planning. In _Robotics: Science and Systems_ , 2023. 

- [143] Wenlong Huang, Fei Xia, Dhruv Shah, Danny Driess, Andy Zeng, Yao Lu, Pete Florence, Igor Mordatch, Sergey Levine, Karol Hausman, and Brian Ichter. Grounded Decoding: Guiding Text Generation with Grounded Models for Robot Control. In _Thirty-seventh Conference on Neural Information Processing Systems_ , 2023. URL `https://openreview.net/forum?id=JCCi58IUsh` . 

- [144] Yan Ding, Xiaohan Zhang, Chris Paxton, and Shiqi Zhang. Task and Motion Planning with Large Language Models for Object Rearrangement. _arXiv preprint_ , 2023. 

- [145] Kevin Lin, Christopher Agia, Toki Migimatsu, Marco Pavone, and Jeannette Bohg. Text2Motion: From Natural Language Instructions to Feasible Plans. _ICRA 2023 Workshop Pretraining4Robotics_ , 2023. 

- [146] Yue Wu, So Yeon Min, Yonatan Bisk, Ruslan Salakhutdinov, Amos Azaria, Yuanzhi Li, Tom Mitchell, and Shrimai Prabhumoye. Plan, Eliminate, and Track – Language Models are Good Teachers for Embodied Agents. _arXiv preprint_ , 2023. 

- [147] Priya Sundaresan, Suneel Belkhale, Dorsa Sadigh, and Jeannette Bohg. KITE: Keypoint-Conditioned Policies for Semantic Manipulation. In _7th Annual Conference on Robot Learning_ , 2023. URL `https://openreview.net/forum?id= veGdf4L4Xz` . 

- [148] Allen Z. Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, Fei Xia, Jake Varley, Zhenjia Xu, Dorsa Sadigh, Andy Zeng, and Anirudha Majumdar. Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners. In _Conference on_ 

36 

_Robot Learning (CoRL)_ , 2023. 

- [149] Krishan Rana, Jesse Haviland, Sourav Garg, Jad Abou-Chakra, Ian Reid, and Niko Suenderhauf. SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Task Planning. In _7th Annual Conference on Robot Learning_ , 2023. URL `https://openreview.net/forum?id=wMpOMO0Ss7a` . 

- [150] Aiko Ichikura, Kento Kawaharazuka, Yoshiki Obinata, Kei Okada, and Masayuki Inaba. A method for Selecting Scenes and Emotion-based Descriptions for a Robot’s Diary. In _IEEE RO-MAN_ , 2023. 

- [151] Peiqi Liu, Yaswanth Orru, Chris Paxton, Nur Muhammad Mahi Shafiullah, and Lerrel Pinto. OK-Robot: What Really Matters in Integrating Open-Knowledge Models for Robotics. _arXiv preprint arXiv:2401.12202_ , 2024. 

- [152] Hao-Shu Fang, Chenxi Wang, Hongjie Fang, Minghao Gou, Jirong Liu, Hengxu Yan, Wenhai Liu, Yichen Xie, and Cewu Lu. AnyGrasp: Robust and Efficient Grasp Perception in Spatial and Temporal Domains. _IEEE Transactions on Robotics (T-RO)_ , 2023. 

- [153] Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. ProgPrompt: Generating Situated Robot Task Plans using Large Language Models. In _2023 IEEE International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [154] Naoki Wake, Atsushi Kanehira, Kazuhiro Sasabuchi, Jun Takamatsu, and Katsushi Ikeuchi. Chatgpt empowered long-step robot control in various environments: A case application. _arXiv preprint_ , 2023. 

- [155] Mimo Shirasaka, Tatsuya Matsushima, Soshi Tsunashima, Yuya Ikeda, Aoi Horo, So Ikoma, Chikaha Tsuji, Hikaru Wada, Tsunekazu Omija, Dai Komukai, et al. Self-recovery prompting: Promptable general purpose service robot system with foundation models and self-recovery. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 17395–17402. IEEE, 2024. 

- [156] Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu, Shiqi Zhang, Joydeep Biswas, and Peter Stone. LLM+P: Empowering Large Language Models with Optimal Planning Proficiency. _arXiv preprint_ , 2023. 

- [157] Constructions Aeronautiques, Adele Howe, Craig Knoblock, I S I Drew McDermott, Ashwin Ram, Manuela Veloso, Daniel Weld, David Wilkins SRI, Anthony Barrett, Dave Christianson, and others. PDDL - the planning domain definition language. _Technical Report, Tech. Rep._ , 1998. 

- [158] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An Open-Ended Embodied Agent with Large Language Models. _arXiv preprint arXiv:2305.16291_ , 2023. 

- [159] Sai Vemprala, Rogerio Bonatti, Arthur Bucker, and Ashish Kapoor. ChatGPT for Robotics: Design Principles and Model Abilities. _arXiv preprint_ , 2023. 

- [160] Xavier Puig, Eric Undersander, Andrew Szot, Mikael Dallaire Cote, Tsung-Yen Yang, Ruslan Partsey, Ruta Desai, Alexander William Clegg, Michal Hlavac, So Yeon Min, and others. Habitat 3.0: A Co-Habitat for Humans, Avatars and Robots. _arXiv preprint arXiv:2310.13724_ , 2023. 

- [161] Takuma Yoneda, Jiading Fang, Peng Li, Huanyu Zhang, Tianchong Jiang, Shengjie Lin, Ben Picker, David Yunis, Hongyuan Mei, and Matthew R. Walter. Statler: State-Maintaining Language Models for Embodied Reasoning. _arXiv preprint_ , 2023. 

- [162] Yoshiki Obinata, Naoaki Kanazawa, Kento Kawaharazuka, Iori Yanokura, Soonhyo Kim, Kei Okada, and Masayuki Inaba. Foundation Model based Open 

37 

Vocabulary Task Planning and Executive System for General Purpose Service Robots. _arXiv preprint_ , 2023. 

- [163] Keisuke Shirai, Cristian C Beltran-Hernandez, Masashi Hamaya, Atsushi Hashimoto, Shohei Tanaka, Kento Kawaharazuka, Kazutoshi Tanaka, Yoshitaka Ushiku, and Shinsuke Mori. Vision-Language Interpreter for Robot Task Planning. _arXiv preprint arXiv:2311.00967_ , 2023. 

- [164] Yen-Jen Wang, Bike Zhang, Jianyu Chen, and Koushil Sreenath. Prompt a Robot to Walk with Large Language Models. _arXiv preprint_ , 2023. 

- [165] Tianhe Yu, Ted Xiao, Austin Stone, Jonathan Tompson, Anthony Brohan, Su Wang, Jaspiar Singh, Clayton Tan, Dee M, Jodilyn Peralta, Brian Ichter, Karol Hausman, and Fei Xia. Scaling Robot Learning with Semantically Imagined Experience. In _arXiv preprint arXiv:2302.11550_ , 2023. 

- [166] Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, and others. Rt-1: Robotics transformer for real-world control at scale. In _Proceedings of Robotics: Science and Systems_ , 2023. 

- [167] Su Wang, Chitwan Saharia, Ceslee Montgomery, Jordi Pont-Tuset, Shai Noy, Stefano Pellegrini, Yasumasa Onoe, Sarah Laszlo, David J Fleet, Radu Soricut, and others. Imagen editor and editbench: Advancing and evaluating text-guided image inpainting. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , pages 18359–18369, 2023. 

- [168] Austin Stone, Ted Xiao, Yao Lu, Keerthana Gopalakrishnan, Kuang-Huei Lee, Quan Vuong, Paul Wohlhart, Sean Kirmani, Brianna Zitkovich, Fei Xia, Chelsea Finn, and Karol Hausman. Open-World Object Manipulation using Pre-Trained Vision-Language Models. _arXiv preprint_ , 2023. 

- [169] Pierre Sermanet, Corey Lynch, Yevgen Chebotar, Jasmine Hsu, Eric Jang, Stefan Schaal, Sergey Levine, and Google Brain. Time-contrastive networks: Self-supervised learning from video. In _2018 IEEE international conference on robotics and automation (ICRA)_ , pages 1134–1141. IEEE, 2018. 

- [170] Tete Xiao, Ilija Radosavovic, Trevor Darrell, and Jitendra Malik. Masked visual pre-training for motor control. _arXiv preprint arXiv:2203.06173_ , 2022. 

- [171] Ilija Radosavovic, Tete Xiao, Stephen James, Pieter Abbeel, Jitendra Malik, and Trevor Darrell. Real-World Robot Learning with Masked Visual Pre-training. In _6th Annual Conference on Robot Learning_ , 2022. URL `https://openreview. net/forum?id=KWCZfuqshd` . 

- [172] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Doll´ar, and Ross Girshick. Masked autoencoders are scalable vision learners. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 16000– 16009, 2022. 

- [173] Danny Driess, Fei Xia, Mehdi S M Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, and others. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv:2303.03378_ , 2023. 

- [174] Pierre Sermanet, Tianli Ding, Jeffrey Zhao, Fei Xia, Debidatta Dwibedi, Keerthana Gopalakrishnan, Christine Chan, Gabriel Dulac-Arnold, Sharath Maddineni, Nikhil J Joshi, Pete Florence, Wei Han, Robert Baruch, Yao Lu, Suvir Mirchandani, Peng Xu, Pannag Sanketi, Karol Hausman, Izhak Shafran, Brian Ichter, and Yuan Cao. RoboVQA: Multimodal Long-Horizon Reasoning for Robotics. In _2nd Workshop on Language and Robot Learning: Language as Grounding_ , 2023. URL `https://openreview.net/forum?id=z3zBluGh1L` . 

38 

- [175] Dmitry Kalashnikov, Jacob Varley, Yevgen Chebotar, Benjamin Swanson, Rico Jonschkowski, Chelsea Finn, Sergey Levine, and Karol Hausman. Scaling Up Multi-Task Robotic Reinforcement Learning. _5th Annual Conference on Robot Learning_ , 2021. URL `https://openreview.net/forum?id=p9Pe-l9MMEq` . 

- [176] Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. BC-Z: Zero-Shot Task Generalization with Robotic Imitation Learning. In _5th Annual Conference on Robot Learning_ , 2021. URL `https://openreview.net/forum?id=8kbp23tSGYv` . 

- [177] Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay, Jost Tobias Springenberg, and others. A generalist agent. _Transactions on Machine Learning Research_ , 2022. URL `https://openreview.net/forum?id= 1ikK0kHjvj` . 

- [178] Yevgen Chebotar, Quan Vuong, Karol Hausman, Fei Xia, Yao Lu, Alex Irpan, Aviral Kumar, Tianhe Yu, Alexander Herzog, Karl Pertsch, Keerthana Gopalakrishnan, Julian Ibarz, Ofir Nachum, Sumedh Anand Sontakke, Grecia Salazar, Huong T Tran, Jodilyn Peralta, Clayton Tan, Deeksha Manjunath, Jaspiar Singh, Brianna Zitkovich, Tomas Jackson, Kanishka Rao, Chelsea Finn, and Sergey Levine. Q-Transformer: Scalable Offline Reinforcement Learning via Autoregressive Q-Functions. In _7th Annual Conference on Robot Learning_ , 2023. 

- [179] Konstantinos Bousmalis, Giulia Vezzani, Dushyant Rao, Coline Devin, Alex X Lee, Maria Bauza, Todor Davchev, Yuxiang Zhou, Agrim Gupta, Akhil Raju, and others. RoboCat: A Self-Improving Foundation Agent for Robotic Manipulation. _arXiv preprint arXiv:2306.11706_ , 2023. 

- [180] Ingmar Schubert, Jingwei Zhang, Jake Bruce, Sarah Bechtle, Emilio Parisotto, Martin Riedmiller, Jost Tobias Springenberg, Arunkumar Byravan, Leonard Hasenclever, and Nicolas Heess. A Generalist Dynamics Model for Control. _arXiv preprint arXiv:2305.10912_ , 2023. 

- [181] Michael Kelly, Chelsea Sidrane, Katherine Driggs-Campbell, and Mykel J Kochenderfer. Hg-dagger: Interactive imitation learning with human experts. In _2019 International Conference on Robotics and Automation (ICRA)_ , pages 8077–8083, 2019. 

- [182] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. VIMA: Robot Manipulation with Multimodal Prompts. In _Fortieth International Conference on Machine Learning_ , 2023. 

- [183] Xi Chen, Josip Djolonga, Piotr Padlewski, Basil Mustafa, Soravit Changpinyo, Jialin Wu, Carlos Riquelme Ruiz, Sebastian Goodman, Xiao Wang, Yi Tay, and others. PaLI-X: On Scaling up a Multilingual Vision and Language Model. _arXiv preprint arXiv:2305.18565_ , 2023. 

- [184] Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, and others. RT-Trajectory: Robotic Task Generalization via Hindsight Trajectory Sketches. _arXiv preprint arXiv:2311.01977_ , 2023. 

- [185] Anonymous. RT-sketch: Goal-conditioned imitation learning from hand-drawn sketches, 2024. URL `https://openreview.net/forum?id=YxvmODVWny` . 

- [186] Michael Ahn, Debidatta Dwibedi, Chelsea Finn, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Karol Hausman, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, et al. Autort: Embodied foundation models for large scale orchestration of robotic agents. _arXiv preprint arXiv:2401.12963_ , 2024. 

39 

- [187] Isabel Leal, Krzysztof Choromanski, Deepali Jain, Avinava Dubey, Jake Varley, Michael Ryoo, Yao Lu, Frederick Liu, Vikas Sindhwani, Quan Vuong, et al. Sarart: Scaling up robotics transformers with self-adaptive robust attention. _arXiv preprint arXiv:2312.01990_ , 2023. 

- [188] Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Charles Xu, Jianlan Luo, Tobias Kreiman, You Liang Tan, Dorsa Sadigh, Chelsea Finn, and Sergey Levine. Octo: An open-source generalist robot policy. `https://octo-models.github.io` , 2023. 

- [189] Cheng Chi, Siyuan Feng, Yilun Du, Zhenjia Xu, Eric Cousineau, Benjamin Burchfiel, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _arXiv preprint arXiv:2303.04137_ , 2023. 

- [190] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A. Rusu, Joel Veness, Marc G. Bellemare, Alex Graves, Martin Riedmiller, Andreas K. Fidjeland, Georg Ostrovski, Stig Petersen, Charles Beattie, Amir Sadik, Ioannis Antonoglou, Helen King, Dharshan Kumaran, Daan Wierstra, Shane Legg, and Demis Hassabis. Human-level control through deep reinforcement learning. _Nature_ , 518(7540):529–533, 2015. 

- [191] Yuval Tassa, Yotam Doron, Alistair Muldal, Tom Erez, Yazhe Li, Diego de Las Casas, David Budden, Abbas Abdolmaleki, Josh Merel, Andrew Lefrancq, and others. Deepmind control suite. _arXiv preprint arXiv:1801.00690_ , 2018. 

- [192] Zhenglin Geng, Chen Cao, and Sergey Tulyakov. 3D Guided Fine-Grained Face Manipulation. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pages 9821–9830, 2019. 

- [193] Shixiang Gu, Ethan Holly, Timothy Lillicrap, and Sergey Levine. Deep Reinforcement Learning for Robotic Manipulation. In _2017 IEEE international conference on robotics and automation (ICRA)_ , pages 3389–3396, 2017. 

- [194] Mengjiao Yang, Yilun Du, Kamyar Ghasemipour, Jonathan Tompson, Dale Schuurmans, and Pieter Abbeel. Learning Interactive Real-World Simulators. _arXiv preprint arXiv:2310.06114_ , 2023. 

- [195] Andrew Jaegle, Sebastian Borgeaud, Jean-Baptiste Alayrac, Carl Doersch, Catalin Ionescu, David Ding, Skanda Koppula, Daniel Zoran, Andrew Brock, Evan Shelhamer, and others. Perceiver io: A general architecture for structured inputs & outputs. In _International Conference on Learning Representations_ , 2022. URL `https://openreview.net/forum?id=fILj7WpI-g` . 

- [196] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation. In _6th Annual Conference on Robot Learning_ , 2022. URL `https://openreview.net/forum?id=PS_eCS_WCvD` . 

- [197] Ethan Perez, Florian Strub, Harm De Vries, Vincent Dumoulin, and Aaron Courville. Film: Visual reasoning with a general conditioning layer. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 32, 2018. 

- [198] Homanga Bharadhwaj, Jay Vakil, Mohit Sharma, Abhinav Gupta, Shubham Tulsiani, and Vikash Kumar. Roboagent: Generalization and efficiency in robot manipulation via semantic augmentations and action chunking. _arXiv preprint arXiv:2309.01918_ , 2023. 

- [199] Mingxing Tan and Quoc Le. Efficientnet: Rethinking model scaling for convolutional neural networks. In _International conference on machine learning_ , pages 6105–6114. PMLR, 2019. 

- [200] Michael Ryoo, A J Piergiovanni, Anurag Arnab, Mostafa Dehghani, and Anelia Angelova. Tokenlearner: Adaptive space-time tokenization for videos. _Advances in Neural Information Processing Systems_ , 34:12786–12797, 2021. 

40 

- [201] Sudeep Dasari, Frederik Ebert, Stephen Tian, Suraj Nair, Bernadette Bucher, Karl Schmeckpeper, Siddharth Singh, Sergey Levine, and Chelsea Finn. Robonet: Large-scale multi-robot learning. In _Conference on Robot Learning (CoRL)_ , 2019. 

- [202] Justin Fu, Aviral Kumar, Ofir Nachum, George Tucker, and Sergey Levine. D4rl: Datasets for deep data-driven reinforcement learning. _arXiv preprint arXiv:2004.07219_ , 2020. 

- [203] Aviral Kumar, Aurick Zhou, George Tucker, and Sergey Levine. Conservative q-learning for offline reinforcement learning. _Advances in Neural Information Processing Systems_ , 33:1179–1191, 2020. 

- [204] Tianhe Yu, Garrett Thomas, Lantao Yu, Stefano Ermon, James Y Zou, Sergey Levine, Chelsea Finn, and Tengyu Ma. Mopo: Model-based offline policy optimization. _Advances in Neural Information Processing Systems_ , 33:14129–14142, 2020. 

- [205] Tatsuya Matsushima, Hiroki Furuta, Yutaka Matsuo, Ofir Nachum, and Shixiang Gu. Deployment-efficient reinforcement learning via model-based offline optimization. In _International Conference on Learning Representations_ , 2021. URL `https://openreview.net/forum?id=3hGNqpI4WS` . 

- [206] Frederik Ebert, Yanlai Yang, Karl Schmeckpeper, Bernadette Bucher, Georgios Georgakis, Kostas Daniilidis, Chelsea Finn, and Sergey Levine. Bridge data: Boosting generalization of robotic skills with cross-domain datasets. In _Robotics: Science and Systems_ , 2022. 

- [207] Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, and others. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning (CoRL)_ , 2023. 

- [208] Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- [209] Zipeng Fu, Tony Z Zhao, and Chelsea Finn. Mobile ALOHA: Learning bimanual mobile manipulation with low-cost whole-body teleoperation. _arXiv preprint arXiv:2401.02117_ , 2024. 

- [210] Philipp Wu, Yide Shentu, Zhongke Yi, Xingyu Lin, and Pieter Abbeel. GELLO: A general, low-cost, and intuitive teleoperation framework for robot manipulators. _arXiv preprint arXiv:2309.13037_ , 2023. 

- [211] Richard S Sutton and Andrew G Barto. _Reinforcement learning: An introduction_ . 2018. 

- [212] Micah Carroll, Orr Paradise, Jessy Lin, Raluca Georgescu, Mingfei Sun, David Bignell, Stephanie Milani, Katja Hofmann, Matthew Hausknecht, Anca Dragan, and others. Uni [mask]: Unified inference in sequential decision problems. _Advances in neural information processing systems_ , 35:35365–35378, 2022. 

- [213] Philipp Wu, Arjun Majumdar, Kevin Stone, Yixin Lin, Igor Mordatch, Pieter Abbeel, and Aravind Rajeswaran. Masked Trajectory Models for Prediction, Representation, and Control. In _Proceedings of the 40th International Conference on Machine Learning_ , volume 202 of _Proceedings of Machine Learning Research_ , pages 37607–37623. PMLR, 1 2023. 

- [214] Jun Hatori, Yuta Kikuchi, Sosuke Kobayashi, Kuniyuki Takahashi, Yuta Tsuboi, Yuya Unno, Wilson Ko, and Jethro Tan. Interactively picking real-world objects with unconstrained spoken language instructions. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , pages 3774–3781. IEEE, 2018. 

41 

- [215] Tadahiro Taniguchi, Takayuki Nagai, Tomoaki Nakamura, Naoto Iwahashi, Tetsuya Ogata, and Hideki Asoh. Symbol emergence in robotics: a survey. _Advanced Robotics_ , 30(11-12):706–728, 2016. 

- [216] Dhruv Shah, Ajay Sridhar, Arjun Bhorkar, Noriaki Hirose, and Sergey Levine. GNM: A General Navigation Model to Drive Any Robot. In _International Conference on Robotics and Automation (ICRA)_ , 2023. 

- [217] Dhruv Shah, Ajay Sridhar, Nitish Dashora, Kyle Stachowicz, Kevin Black, Noriaki Hirose, and Sergey Levine. ViNT: A Foundation Model for Visual Navigation. In _7th Annual Conference on Robot Learning_ , 2023. 

- [218] Naruki Yoshikawa, Marta Skreta, Kourosh Darvish, Sebastian Arellano-Rubach, Zhi Ji, Lasse Bjørn Kristensen, Andrew Zou Li, Yuchi Zhao, Haoping Xu, Artur Kuramshin, and others. Large language models for chemistry robotics. _Autonomous Robots_ , 47:1057–1086, 2023. 

- [219] Kento Kawaharazuka, Yoshiki Obinata, Naoaki Kanazawa, Kei Okada, and Masayuki Inaba. Robotic Applications of Pre-Trained Vision-Language Models to Various Recognition Behaviors. _arXiv preprint arXiv:2303.05674_ , 2023. 

- [220] Sriram Yenamandra, Arun Ramachandran, Karmesh Yadav, Austin S Wang, Mukul Khanna, Theophile Gervet, Tsung-Yen Yang, Vidhi Jain, Alexander Clegg, John M Turner, Zsolt Kira, Manolis Savva, Angel X Chang, Devendra Singh Chaplot, Dhruv Batra, Roozbeh Mottaghi, Yonatan Bisk, and Chris Paxton. HomeRobot: Open-Vocabulary Mobile Manipulation. In _7th Annual Conference on Robot Learning_ , 2023. URL `https://openreview.net/forum? id=b-cto-fetlz` . 

- [221] Aiko Ichikura, Kento Kawaharazuka, Yoshiki Obinata, Koki Shinjo, Kei Okada, and Masayuki Inaba. Automatic Diary Generation System including Information on Joint Experiences between Humans and Robots. _arXiv preprint arXiv:2309.01948_ , 2023. 

- [222] Hyungjun Cho and Tek-Jin Nam. The story of Beau: Exploring the potential of generative diaries in shaping social perceptions of robots. _International Journal of Design_ , 17(1):1–15, 2023. 

- [223] Matthew Chang, Theophile Gervet, Mukul Khanna, Sriram Yenamandra, Dhruv Shah, So Yeon Min, Kavit Shah, Chris Paxton, Saurabh Gupta, Dhruv Batra, and others. Goat: Go to any thing. _arXiv preprint arXiv:2311.06430_ , 2023. 

- [224] Oier Mees, Lukas Hermann, Erick Rosete-Beas, and Wolfram Burgard. Calvin: A benchmark for language-conditioned policy learning for long-horizon robot manipulation tasks. _IEEE Robotics and Automation Letters_ , 7(3):7327–7334, 2022. 

- [225] Ran Gong, Jiangyong Huang, Yizhou Zhao, Haoran Geng, Xiaofeng Gao, Qingyang Wu, Wensi Ai, Ziheng Zhou, Demetri Terzopoulos, Song-Chun Zhu, and others. ARNOLD: A Benchmark for Language-Grounded Task Learning With Continuous States in Realistic 3D Scenes. In _Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)_ , 2023. 

42 

