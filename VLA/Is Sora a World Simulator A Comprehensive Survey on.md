---
title: "Is Sora a World Simulator? A Comprehensive Survey on General World Models and Beyond"
date: "2024-05-06"
authors: "Zheng Zhu; Xiaofeng Wang; Wangbo Zhao; Chen Min; Bohan Li; Nianchen Deng"
url: https://arxiv.org/abs/2405.03520
pdf: https://arxiv.org/pdf/2405.03520
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2405.03520)** / [論文ページ](https://arxiv.org/abs/2405.03520)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

1 

# Is Sora a World Simulator? A Comprehensive Survey on General World Models and Beyond 

Zheng Zhu<sup>_∗_</sup> , Xiaofeng Wang<sup>_∗_</sup> , Wangbo Zhao<sup>_∗_</sup> , Chen Min<sup>_∗_</sup> , Bohan Li<sup>_∗_</sup> , Nianchen Deng<sup>_∗_</sup> , Min Dou<sup>_∗_</sup> , Yuqi Wang<sup>_∗_</sup> , Botian Shi<sup>_†_</sup> , Kai Wang<sup>_†_</sup> , Chi Zhang<sup>_†_</sup> , Yang You<sup>_†_</sup> , Zhaoxiang Zhang<sup>_†_</sup> , Dawei Zhao<sup>_†_</sup> , Liang Xiao<sup>_†_</sup> , Jian Zhao<sup>_†_</sup> , Jiwen Lu<sup>_†_</sup> , Guan Huang<sup>_†_</sup> 

**Abstract** —General world models represent a crucial pathway toward achieving Artificial General Intelligence (AGI), serving as the cornerstone for various applications ranging from virtual environments to decision-making systems. Recently, the emergence of the Sora model has attained significant attention due to its remarkable simulation capabilities, which exhibits an incipient comprehension of physical laws. In this survey, we embark on a comprehensive exploration of the latest advancements in world models. Our analysis navigates through the forefront of generative methodologies in video generation, where world models stand as pivotal constructs facilitating the synthesis of highly realistic visual content. Additionally, we scrutinize the burgeoning field of autonomous-driving world models, meticulously delineating their indispensable role in reshaping transportation and urban mobility. Furthermore, we delve into the intricacies inherent in world models deployed within autonomous agents, shedding light on their profound significance in enabling intelligent interactions within dynamic environmental contexts. At last, we examine challenges and limitations of world models, and discuss their potential future directions. We hope this survey can serve as a foundational reference for the research community and inspire continued innovation. This survey will be regularly updated at: https://github.com/GigaAI-research/General-World-Models-Survey. 

**Index Terms** —World models, Generative models, Video generation, Autonomous driving, Autonomous agents 

✦ 

## **1 INTRODUCTION** 

I development of general world models stands as a funda-N the pursuit of Artificial General Intelligence (AGI), the mental avenue. General world models seek to understand the world through generative processes. Notably, the introduction of the Sora model [1] has garnered significant attention. Its remarkable simulation capabilities not only demonstrate an initial comprehension of physical laws but also highlight the promising advancements in world models. As we stand at the forefront of AI-driven innovation, it is crucial to delve deeper into the realm of world models, unraveling their complexities, evaluating their current developmental stage, and contemplating the potential trajectories they may follow in the future. 

World models predict the future to grow comprehension of the world. This predictive capacity holds immense promise for video generation, autonomous driving, and the development of autonomous agents, which represent three 

- _∗ indicates equal contributions. † indicates corresponding authors._ 

> _• Zheng Zhu and Guan Huang are with GigaAI, Beijing, China. • Xiaofeng Wang, Yuqi Wang and Zhaoxiang Zhang are with Institute of Automation, Chinese Academy of Sciences, Beijing, China._ 

- _Wangbo Zhao, Kai Wang and Yang You are with National University of Singapore, Singapore._ 

- _Bohan Li is with Shanghai Jiao Tong University, Shanghai, China._ 

- _Chen Min is with Institute of Computing Technology, Chinese Academy of Sciences, Beijing, China._ 

- _Nianchen Deng, Min Dou and Botian Shi are with Shanghai Artificial Intelligence Laboratory, Shanghai, China._ 

- _Chi Zhang is with Mach Drive, Beijing, China._ 

- _Dawei Zhao and Liang Xiao are with Defense Innovation Institute, Beijing, China._ 

- _Jian Zhao is with EVOL Lab, Institute of AI, China Telecom, and Northwestern Polytechnical University._ 

- _Jiwen Lu is with Tsinghua University, Beijing, China._ 

mainstream directions of development in world models. As shown in Figure 1, video generation world models encompass the generation and editing of videos to understand and simulate the world, which are valuable for media production and artistic expression. Autonomous driving world models, aided by techniques of video generation, create driving scenarios and learn driving elements and policies from driving videos. This knowledge assists in generating driving actions directly or training driving policy networks, aiding in endto-end autonomous driving. Similarly, agent world models utilize video generation to establish intelligent interactions in dynamic environments. Unlike driving models, they build policy networks applicable to various contexts, either virtual (e.g., programs in games or simulated environments) or physical (e.g., robots). 

Building upon the foundation of comprehensive world modeling, video generation methods unveil physical laws through visual synthesis. Initially, the focus of generative models was primarily on image generation [2], [3], [4], [5], [6], [7], [8], [9], [10] and editing [11], [12], [13], [14], laying the foundation for more sophisticated advancements in synthesizing dynamic visual sequences. Over time, generative models [15], [16], [17], [18], [19], [19], [20], [21], [22], [23] have evolved to not only capture the static attributes of images, but also seamlessly string together sequences of frames. These models have developed some understanding of physics and motion, which represent early and limited forms of general world models [24]. Notably, at the forefront of this evolution stands the Sora model [1]. By harnessing the power of generative techniques, Sora demonstrates a profound ability to generate intricate visual narratives that adhere to the fundamental principles of the physical world. The relationship between generative models and world 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

2 

modeling is symbiotic, with each informing and enriching the other. Generative models can construct vast amounts of data in a controlled environment, which alleviates the need for extensive real-world data collection, particularly beneficial for training AI systems essential in real-world applications. Moreover, the efficacy of generative models critically hinges upon the depth of comprehension provided by world models. It is the comprehensive understanding of underlying environmental dynamics afforded by world models that empowers generative models to produce visually compelling signals of superior quality while adhering to stringent physical constraints. Thereby enhancing their realism and utility in various domains. 

The ability of world models to understand the environment not only enhances video generation quality, but also benefits real-world driving scenarios. By employing predictive techniques to comprehend driving environments, world models are reshaping transportation and urban mobility by anticipating future driving scenarios, thereby enhancing safety and efficiency. World methods, aimed at establishing dynamic models of environments, are crucial in autonomous driving, where precise predictions about the future are essential for safe maneuvering. However, constructing world models for autonomous driving presents unique challenges, primarily due to the sample complexity inherent in real-world driving scenarios. Early methods [25], [26], [27] attempt to address these challenges by reducing the search space and incorporating explicit disentanglement of visual dynamics. Despite progress, a critical limitation lies in the predominant focus on simulation environments. Recent advances have seen autonomous driving world models leverage generative models to tackle real-world scenarios with larger search spaces. GAIA-1 [28] employs a Transformer to predict the next visual token, effectively constructing the driving world model. This approach enables anticipating multiple potential futures based on various prompts, such as weather conditions, scenes, traffic participants, and vehicle actions. Similarly, methods like DriveDreamer [29] and Panacea [30] leverage pre-trained diffusion models to learn driving world models from real-world driving videos. These techniques harness the structured information inherent in driving scenes to controllably generate high-quality driving videos, which can even enhance training for driving perception tasks. DriveDreamer2 [31], based on DriveDreamer, further integrates large language models to enhance the performance of driving world models and user interaction. It enables the generation of controllable driving scene videos solely through natural language input, encompassing even rare scenarios like sudden overtaking maneuvers. Furthermore, Drive-WM [32] demonstrates the feasibility of directly training end-to-end driving using generated driving scene videos, significantly improving endto-end driving performance. By anticipating future scenarios, these models empower vehicles to make informed decisions, ultimately leading to safer and more efficient navigation on the roads. Moreover, this integration not only improves transportation systems’ safety and efficiency but also opens new possibilities for urban planning and design. 

Beyond their established utility in driving scenarios, world models have increasingly become integral to the functioning of autonomous agents, facilitating intelligent 

interactions across a myriad of contexts. For instance, world models in game agents not only augment the gaming experience but also propel the development of sophisticated game algorithms. The Dreamer series [33], [34], [35] exemplify this with its adept use of world models to predict future states within gaming environments. This capability enables game agents to learn in imagination, markedly decreasing the necessary volume of interactions for effective learning. In robotic systems, innovative approaches further underscore the versatility and potential of world models. UniPi [36], for instance, reimagines the decision-making problem in robotics as a text-to-video task. Its policy-asvideo formulation fosters learning and generalization across diverse robot manipulation tasks. Similarly, UniSim [37] introduces a simulator of dynamic interactions through generative modeling, which can then be deployed in realworld scenarios without prior exposure. RoboDreamer [38] pushes the envelope by leveraging world models to propose plans involving combinations of actions and objects, thus solving unprecedented tasks in novel robotic execution environments. The multifaceted applications of world models extend beyond games and robotics. LeCun’s proposal of the Joint-Embedding Predictive Architecture (JEPA) [39] heralds a significant departure from traditional generative models. JEPA learns to map input data to predicted outputs within a higher-level representation space, which enables the model to concentrate on learning more semantic features, enriching its capability for understanding and predicting across various modalities. 

Based on the comprehensive discussions presented above, it is evident that research on world models holds tremendous potential towards achieving AGI and has wide-ranging applications across various domains. Therefore, world models warrant significant attention from both academia and industry, requiring sustained efforts over an extended period. In comparison to recent surveys [40], [41], [42], [43] on world models, our survey offers broader coverage. It not only encompasses generative world models in video generation but also delves into the applications of world models in decision-making systems such as autonomous driving and robotics. We envision this survey to offer valuable insights for newcomers embarking on their journey into this field, while also stimulating critical thinking and discussion among established researchers in the community. 

The main contributions of this survey can be summarized as follows: (1) We present a holistic examination of recent advancements in world model research, encompassing profound philosophical perspectives and detailed discussions. (2) Our analysis delves deeply into the literature surrounding world models for video generation, autonomous driving, and autonomous agents, uncovering their applications in media production, artistic expression, end-to-end driving, games, and robots. (3) We assess the existing challenges and limitations of world models and delve into prospective avenues for future research, with the intention of steering and igniting further progress in world models. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

3 


Fig. 1. This survey focuses on world models for video generation, world models for autonomous driving, and world models for autonomous agents. Video generation world models specialize in conditional video generation and various video editing tasks. These video generation techniques aid in the understanding of complex scenes and decision-making processes in autonomous driving and autonomous agents world models. The applications of these world models are broad, ranging from media production and artistic expression to action prediction in autonomous driving and agent systems. 

## **2 VIDEO GENERATION AS A GENERAL WORLD MODEL** 

The video generation task aims to create various realistic videos, requiring the model to understand and simulate the mechanism in the physical world, which aligns with the objective of building a general world model. In this section, we first introduce the technologies behind the video generation models in Section 2.1. Then, in Section 2.2, we present and review the advanced video generation models emerging in recent years. Finally, we discuss Sora in Section 2.3, which is considered to be the largest breakthrough in video generation. 

### **2.1 Technologies behind Video Generation** 

The concept of video generation contains several different tasks based on the conditions, such as class, text, or image. This survey mainly focuses on the scenario where the text condition is given, known as text-to-video generation. In this section, we first briefly introduce the visual foundation models, which are widely used in generation models. Then, we present the text encoders for extracting text features from the text condition. Finally, we review the evolution of generation techniques. 

### _2.1.1 Visual Foundation Models_ 

The visual foundation models were originally proposed to tackle traditional computer vision tasks, for example, image classification [44], whereas they also inspire the development of generation models. Based on the architecture, they can be roughly categorized into convolution-based models and Transformer-based models, both of which can also be extended to the video data. 

**Convolution-based Models.** The convolution-based models for vision tasks have been fully explored in the last decades. Staring from LeNet [45], AlexNet [46], VGGNet [47], InceptionNet [48], ResNet [49], DenseNet [50] are gradually proposed to tackle the image recogntion problems. These 

models are adopted as a backbone model for other visual tasks [51], [52], [53]. Typically, U-Net [53] builds a U- shape architecture based on a backbone model for image segmentation tasks. The U-shape architecture enables the model can leverage both the low-level and high-level features from the backbone, which significantly improves the pixelwise prediction. Benefiting from the superiority of pixel-wise prediction, the U-shape architecture is also widely used in image generation models [2], [54], [55]. 

**Transformer-based Models.** The Transformer is proposed in [56] for machine translation tasks and applied to vision recognition by ViT [57]. In ViT, images are divided into patches, then projected into tokens and finally processed by a series of multi-head self-attention and multi-layer perceptron blocks. Its ability to capture long-range dependencies in images enables its superiority in image recognition. After that, distillation [58], window-attention [59], and mask image modeling [60], [61] approaches are introduced to improve the training or inference efficiency of vision Transformers. Except for the success in image recognition, Transformerbased models also demonstrate superiority in various visual tasks, such as object detection [62], [63], [64], [65], semantic segmentation [66], [67], [68], and image generation [69], [70], [71]. Thanks to its good scalability property, the Transformerbased model DiT [69] has become the main architecture of Sora. 

**Extension to Video.** The methods mentioned above are mainly designed for image data. Researchers further extend these methods to solve problems in the video domain. Convolution-based models [72], [73], [74], [75], [76], [77], [78] usually introduce 3D convolution layers to building the spatial-temporal relationships in video data. Transformerbased methods [79], [80], [81], [82] extend and improve the multi-head self-attention from spatial-only design to jointly modeling spatial-temporal relationships. These methods also inspire the architecture design of text-to-video generation models, such as [22], [83], [84]. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

4 

### _2.1.2 Text Encoders_ 

The text encoder is adopted to extract the text embedding for a given text prompt in image or video generation. Existing generation methods usually employ the text encoder of a multi-modal model or directly use a language model to conduct the embedding extraction. In the following, we will briefly present representative multi-modal models and language models. 

**Pre-trained Multi-modal Models.** The pre-trained multimodal models, such as [85], [86], [87], align the representation of image and text in the embedding space. It usually consists of an image encoder as well as a text encoder, which naturally can be adapted to inject text information into generation models. CLIP [86] is a typical pre-trained multimodal model, which has been widely used in image/video generation models [2], [3], [6], [18]. It is pre-trained with large-scale image-text pairs through contrastive learning [88] and demonstrates superior performance across various tasks. However, CLIP is pre-trained for image-text alignment instead of comprehending complex text prompts. This drawback may limit the generation performance when the given prompt is long and detailed. 

**Pre-trained Language Models.** The pre-trained language models are usually pre-trained on the large-scale corpus, thus having transferable ability on various downstream language tasks. BERT [89] is an early attempt at language model pretraining, which designed several tasks to push the model learning from unlabeled data. This paradigm also inspires follow-up works, such as RoBERTa [90] and BART [91]. With the increasing model size and enlarging training dataset, the pre-trained models demonstrate surprising abilities, which are usually named as larger language models (LLMs) [92], [93], [94], [95], [96], [97], [98]. T5 [95] and Llama-2 [96] are two widely used LLMs in generation tasks [99], [100], [101], [102] since their superior performance and open avaliablity. The LLMs provide a better understanding of long text prompts than CLIP, thus helping the generation to follow the instructions of humans. 

### _2.1.3 Generation Techniques_ 

In this section, we review the development of generation techniques in recent decades. 

**GAN.** Before the success of diffusion-based methods, GAN introduced in [103] have always been the mainstream methods in image generation. It has a generator _G_ and a discriminator _D_ . The generator _G_ is adapted to generate an output _G_ ( **z** ) from a noised **z** sampled from a Gaussian distribution and the discriminator _D_ is employed to classifier the output is real or fake. 

From the original definition of GAN [103], the generator _G_ and the discriminator _D_ are trained in an adversarial manner. Specifically, we first train the discriminator _D_ . We input real data **x** sampled from a data distribution _p_ data( **x** ) and generated output _G_ ( **z** ) into the discriminator _D_ and it learns to improve the discrimination ability on real and fake samples. This can be formulated as: 

The discriminator _D_ should maximize the loss _ℓD_ . During this process, the parameters in _G_ are frozen. Then, we train the generator _G_ following: 


The generator _G_ is trained to minimize the loss _ℓG_ so that the generated samples can approach the real data. The parameters in _D_ are also not updated during this process. 

Following works apply GAN to various tasks related to image generation, such as style transfer [104], [105], [106], [107], image editing [108], [109], [110], and image inpainting [111], [112]. 

**Diffusion.** Diffusion-based methods have started to dominate image generation since the Denoising Diffusion Probabilistic Model (DDPM) [54], which learns a reverse process to generate an image from a Gaussian distribution _N_ (0 _,_ **_I_** ). It has two processes: the diffusion process (also known as a forward process) and the denoising process (also known as the reverse process). During the diffusion process, we gradually add small Gaussian noise to an image in _T_ timesteps. Given a image **x** 0 from the data distribution, we can obtain **x** _T_ through the cumulative distribution of all previous diffusion processes: 


where 


_T_ and [ _β_ 1 _, β_ 2 _, . . . , βT_ ] denote the diffusion steps and the pre-defined noise schedule, respectively. We can also obtain the output at the _t_ timestep through 


The denoising process is the reverse of the diffusion process, enabling us to obtain images from the Gaussian noise. To achieve this, a denoising model _ϵθ_ learns to predict the noise _ϵt_ added at the timestep _t_ through a simplified loss function, which can be formulated as: 


Then, we can denoise step-by-step through 


where **z** _∼N_ (0 _, I_ ). Although the generation quality of DDPM is satisfactory, its slow generation speed hinders its broader application. Following works attempt to solve this problem by reducing the denoising steps [113], [114], [115], [116], [117] or accelerating the denoising model [118], [119], [120], [121]. 

**Autoregressive Modeling.** Autoregressive modeling has been explored in both language generation methods [92], [93], [94] and image generation tasks [10], [122], [123], [124]. Given a sequence of tokens ( **x** 1 _,_ **x** 2 _, . . . ,_ **x** _K_ ), the probability of the 

_ℓD_ = E **x** _∼p_ data ( **x** )[log _D_ ( **x** )] + E **z** _∼pz_ ( **z** )[log(1 _− D_ ( _G_ ( **z** )))] _._ (1) 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

5 

_k_ -th toeken **x** _k_ only depends on tokens ( **x** 1 _,_ **x** 2 _,_ **x** _k−_ 1). An autoregressive model _pθ_ is trained to maximize the likelihood of the current token, which can be formulated as: 


Recently, LVM [125] scales up the amount of training data to 420 billion tokens and model size to 3 billion parameters, demonstrating an ability for general visual reasoning as well as generation and directing a potential way towards the world model. 

**Masked Modeling.** Masked modeling is first designed for self-supervised learning for language models [89], [90], [126] and image models [60], [61]. Given a sequence of tokens ( **x** 1 _,_ **x** 2 _, . . . ,_ **x** _K_ ), some tokens are randomly masked out. Then, the model is forced to predict the masked tokens and reconstruct the original representation. Noting the ability of image reconstruction of masked modeling, some works [127], [128], [129] directly generate images from mask tokens and find it also generalizes well in video generation tasks [83], [84]. Considering its simplicity and surprising performance, it is also a promising direction for future generation techniques. 

### **2.2 Advanced Video Generation Models** 

In this section, we review the advanced video generation models proposed in recent years. Based on the given conditions ( _e.g_ . example, classes, audios, texts, images, or videos), during generation, video generation tasks can be divided into different categories. Here, we mainly focus on the textto-video method, where the text description is available during generation. These models aim to generate videos that are semantically aligned with given texts while maintaining consistency between different frames. The methods for idea generation with other conditions can be modified from the text-to-image models. 

### _2.2.1 GAN-based Methods_ 

Besides the success of image generation, GAN-based models also achieve remarkable performance for video generation [130], [131], [132], [133], [134], [135], [136]. Here, we select three representative methods and review them briefly. We visualize a general architecture of GAN-based methods from video generation in Figure 4 (a). 

Temporal GANs conditioning on captions (TGANs-C) [130] adopts a text encoder based on LSTM [137] to extract a text embedding. This embedding is then combined with a vector of random noise, which together form the input to the generator. The generator contains a series of spatiotemporal convolutions to generate the frame sequence. Unlike the GANs-based models for image generation in Section 2.1.3, which typically has only one discriminator, TGANs-C designs three discriminators in video, frame, and motion-levels, respectively. Benefiting from these discriminators, the model is capable of producing videos that align with the provided text and akin to authentic video footage. 

Text-Filter conditioning Generative Adversarial Network (TFGAN) [131] adopts the text features extracted from the text encoder to generate a series of filters in different frames. Then, these filters are employed as the convolutional filters in 

the discriminator for each frame generation. This operation enhances the semantic association between the given text and the generated video. 

The StroyGAN [134] aims to generate a sequence of frames based on a multi-sentence paragraph, where each sentence is responsible for one frame. It adopts a story encoder and a context encoder to extract the global representation of the multi-sentence paragraph and sentence for the current frame, respectively. Then, the output from the story encoder and context encoder are combined and input to the generator to generate the current frame. It also employs two discriminators to ensure the frame-level and video-level consistency with the given paragraph. 

### _2.2.2 Diffusion-based Methods_ 

The development of diffusion models for image generation also facilitates the progress in video generation. We select four representative approaches due to their effectiveness or efficiency. We summarize the framework of these methods in Figure 4 (b). 

Imagen Video [19] proposes a cascaded sampling pipeline for video generation. Starting from a base video generation model [138], which generates video with low resolution and low frame rate, the authors cascade spatial and temporal super-resolution models to progressively improve the resolution and frame rate of generated videos. 

Stable video diffusion (SVD) [18] is built upon Stable Diffusion [2] by inserting temporal convolution and attention layers after spatial convolution and attention blocks. To improve the generation performance, the authors propose to disengage the training into three stages: pre-training on text-to-image task, pre-training on text-to-video task, and text-to-video finetuning with high-quality data. It proves the importance of data curation for video diffusion models. 

Latte [139] is an early attempt to apply a Transformerbased model in video generation. The model is built based on DiT [69] and contains extra blocks for spatial-temporal modeling. To ensure the efficiency in generation, the authors explore four efficient designs for spatial and temporal modeling, which is similar to the operations mentioned in Section 2.1.1. The architecture of the Latte is thought to be similar to the design of Sora. 

StreamingT2V [140] divides the text-to-video generation into three steps, enabling to generation of long videos with even more than 1,200 frames. First, it employs pre-trained text-to-video models to generate a short video _e.g_ . with only 16 frames. Then, it extends a video diffusion model with short-term and long-term memory mechanisms to autoregressively generate further frames. Finally, another highresolution video generation model is adopted to enhance generated videos. 

### _2.2.3 Autoregressive Modeling-based Methods_ 

Autoregressive modeling is also a popular technique in video generation [15], [123], [141], [142], [143] . We present its architecture in Figure 4 (c). 

VideoGPT [15] is a representative autoregressive modeling-based method. It first trains a VQ-VAE [144] to encode videos into latent tokens. Then, the authors leverage a GPT-like framework [92] and train the model learning to predict the next token in the latent space. During the 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

6 


Fig. 2. An potential architecture of Sora. This architecture is inspired from [1], [42].1], [42].], [42].42].]. 

Fig. 3. Chronological overview of video generation models. We present representative models proposed in recent years. Before 2021, GAN-based models dominate video generation. After that, autoregressive modeling-based, diffusion-based, and masked modeling-based models start to emerge and achieve surprising performance. 

inference, a series of tokens is sampled from the latent space and the trained VideoGPT with VQ-VAE decodes it into generated videos. 

GODIVA [141] also generates videos in a similar way while emphasizing reducing the computation complexity of the model. Specifically, the authors propose to replace an original self-attention layer with three sparse self-attention layers, which only are conducted along the temporal, row, and column dimensions of the latent features, respectively. The effectiveness of this disentangling operation is also verified by models mentioned in Section 2.1. 

CogVideo [142] inherits the knowledge from the pretrained autoregressive model CogView2 [145] to reduce the burden of training from scratch. To improve the alignment between the given text and generated video, the authors propose a multi-frame-rate hierarchical generation framework, which first generates key frames in an autoregressive manner and then recursively interpolates frames with bidirectional attentions. 

### _2.2.4 Masked Modeling-based Methods_ 

Masked modeling is also an emerging video generation method. Unlike autoregressive modeling, which suffers from sequential generation, the masked modeling method can decode videos in parallel. We visualize its architecture in Figure 4 (d). 

MAGVIT [83] encodes videos into tokens through a 3D-VQ tokenizer and leverages a masked token modeling paradigm to accelerate the training. Specifically, the target tokens are randomly replaced with conditional tokens and masked tokens during training. Then, a bidirectional Transformer is trained to refine the conditional tokens, predict masked tokens, and reconstruct target tokens. To improve the generation quality, MAGVIT-v2 [84] is introduced to improve the video tokenizer. The authors design a lookupfree quantization method to build the codebook and propose a joint image-video tokenization model, enabling it can tackle image and video generation jointly. After that, VideoPoet [22] integrates MAGVIT-v2 [84] into a large language model to generate videos from various conditioning signals 

Similarly, WorldDreamer [146] also trains to model to reconstruct masked tokens based on those unmasked tokens. To facilitate the training process, they design a spatialtemporal patchwise Transformer, which conducts attention within a spatial-temporal window. It adopts cross-attention layers to inject information of given text descripction into the model. The priority of parallel decoding enables it to achieve much faster video generation than diffusion-based and autoregressive-based methods. 

### _2.2.5 Datasets and Evaluation Metrics_ 

Training a text-to-video generation model requires large-scale video-text pairs. In Table 1, we present serveral popular 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

7 

datasets. These datasets may also be employed to train multi-modal models. Based on the technical report from Sora, the data quality, for example the video-text alginment and the richness of captions, is essential to the generation performance. Hence, we hope more large-scale high quality dataset can be open-sourced, prompting the prosperity of video generation and even the development of world models. 

The metrics adopted to evaulate the video generation performance varies in different papers. Fo example, Latte [139] and VideoGPT [15] measure the performance through Frechet´ Video Distance (FVD) [147]. CLIP similarity (CLIPSim) [141] is also a common evualtion approach. Human evaluation as complementary to these metrics is also widely adopted in existing works. Since evaluation score are highly related to the random seed, it is not easy to conduct fair comparison. Moreover, different mehtods may adopt differnt dataset to evalution performance, which further aggravates this problem. Human preference annotations may be a potential solution for video generation evaluation. Recently, some comprehensive benchmarks [148], [149], [150] are proposed for the comparison fairness. 

### **2.3 Towards World Models: Sora** 

Sora is a closed-source text-to-video generation model developed by OpenAI. Besides being capable of generating a minute of high-fidelity video, it demonstrates some abilities to simulate the real world. It directs a way towards the world model through video generation models. In this section, we briefly introduce the techniques behind Sora. Since Sora is closed-source, all analyses here are mainly based on its technical report [1] and may vary from its real implementation. 

### _2.3.1 Framework_ 

Sora is thought to be a diffusion-based video generation model. It consists of three parts: 1. A compression model that compresses a raw video both temporally and spatially into latent representation and an asymmetrical model that maps the latent representation back to the original video. 2. A Transformer-based diffusion model, similar to DiT [69], which is trained in the latent space. 3. A language model that encoders human instruction into embedding and injects it into the generation model. 

**Compression Model.** The compression model usually contains an encoder and a decoder. The former is adopted to project the video into a low-dimensional latent space, while the latter maps the latent representation back to the video. Based on the technical report [1], the compression model is built based on VAE [151] or VQ-VAE [144]. Since the architecture of the decoder is usually in symmetric to the encoder, we mainly focus on the architecture of the encoder in this review. 

Given a raw video **V** _∈_ R<sup>_T ×H×W ×C_</sup> , the encoder first projects it into a sequence of tokens **x** _∈_ R<sup>_nt×nh×nw×d_</sup> . Based on the methods employed in visual foundation models mentioned in Section 2.1.1, there exist two options: spatialonly compression and spatial-temporal compression. The spatial-only compression only compresses the video along the spatial dimension. It extracts image patches of size _h × w_ for each frame and adopts a 2D convolutional layer to project 

it into **x** _i ∈_ R<sup>_d_</sup> . In this case, we have _nt_ = _T_ , _nh_ = _H/h_ , and _nw_ = _W/w_ . This operation is widely adopted in ViTs [57]. The spatial-temporal compression method compresses the video along both the spatial and temporal dimensions, which provides a larger compression rate. Specifically, it extracts spatial-temporal tubes of size _t × h × w_ from the video and adopts a 3D convolutional layer to project it into an embedding **x** _i ∈_ R<sup>_d_</sup> . Thus, we have _nt_ = _T/t_ , _nh_ = _H/h_ , and _nw_ = _W/w_ . This operation is similar to the tubelet embedding technique in ViViT [79]. 

After the tokenization, the encoder can further process these tokens through Transformer blocks, convolutional blocks, or the combination of them and project them into _z ∈_ R<sup>_n_</sup> _t_<sup>_′×n′_</sup> _h_<sup>_×n′_</sup> _w_<sup>_×d′_</sup> . We present the architecture of the compression model in Figure 2 (a). 

**Generation Model.** Based on the technical report, the generation model is built up on DiT [69]. Since the original DiT is designed for class-to-image generation, two modifications should be conducted on it. First, since the self-attention blocks and MLP blocks in DiT are designed for spatial modeling, extra blocks for temporal modeling should be added. This could be achieved via extending the original selfattention to both spatial and temporal dimensions. Second, the condition is changed from class to text, and blocks to inject the text information should be added. The text-toimage cross-attention block is a potential solution, whose effectiveness has been proven in [100]. Based on this, one layer of the potential architecture can be formulated as: 


where STA and CA denotes the spatial-temporal attention and text-to-image cross attention blocks, respectively. **x**<sup>_g_</sup> _∈_ R<sup>(</sup><sup>_n_</sup> _t_<sup>_g×ng_</sup> _h_<sup>_×ng_</sup> _w_<sup>)</sup><sup>_×dg_</sup> denotes the input of this layer. The text embedding derived from a language model _e.g_ . T5 [95] or a multi-modal model _e.g_ . CLIP [86] is denoted as _c_ . We omit the injection of timestep information for brevity, which can be achieved with adaptive layer norm blocks [152]. We also present the potential architecture in Figure 2 (b). Finally, the generation model is trained to predict noise added to the latent representation _z_ . More details can be found in diffusion techniques mentioned in Section 2.1.3 

### _2.3.2 Training Data_ 

A large challenge to training Sora is collecting large-scale high-quality video-text pairs. Previous works [100], [153] have proven that generation performance is highly dependent on the quality of data. Low-quality data, for example, noisy video-text pairs or too simple video captions, results in generation models with pool instruction following. To tackle this problem, Sora adopts the re-captioning technique proposed in DALL-E 3 [153]. Specifically, a video captioner is trained with high-quality video-text pairs, where the text is well-aligned with the corresponding video and contains diverse and descriptive information. The video captioner could be a video version of multi-modal large language models, like GPT-4V [98], mPLUG [154], or InternVideo [155]. Then, the pre-trained video captioner is employed to 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

8 


Fig. 4. Video generation methods. (a) GAN-based (b) Diffusion-based (c) Autoregressive modeling-based (d) Masked modeling-based. 

generate high-quality captions for the training data of Sora. This simple method effectively improves the data quality. 

During inference, to solve the problem that users may provide too simple prompts, Sora adopts GPT-4 [98] to rewrite the prompts so that they are detailed. This enables Sora to generate high-quality videos. 

### _2.3.3 Towards World Models_ 

Based on the claim from OpenAI, Sora can work as a world simulator, since it can understand the result of an action. For an example from its technical report, Sora generates a video where a painter can leave new strokes along a canvas that persist over time. Another example is that a man can eat a burger and leave bite marks, which denotes that Sora can predict the results of eating. These two examples indicate that Sora can understand the world and predict the results of an action. This capability is well-aligned with the target of world models: understanding the world via predicting the future. Hence, we believe that the techniques behind Sora can further inspire the exloration of world models. 

First, the training and inference strategies improve the performance and efficiency in large generation models. For example, Sora learning from videos with enative aspect ratios, which obviously improve the composition and framing of generated videos. This requires both technical and engineering optimization to enbale efficent training. Generating videos with 1 minute length is a large chalenge and burden for inference server, which still impede releasing Sora to public until now. The OpenAI’s soulution may be valubale for the community of large models. More potential techniues adopted in Sora can be found in [42]. We believe these contritbuons in Sora could also inpire building world models. 

Second, Sora adopts Transformer-based generation with extensive parameters and large-scale training data, resuting in emergent abilities in video generation. This suggests that there also exsiting scaling laws in the visual field and directs a promising way to build large vision models or even world models. 

Finally, Sora emphasize the essentiality of training data for good generation performance once again. Although OpenAI has not disclosed the sources and scale of data used in Sora, some guesses think extensive game videos may be introduced during training. The game videos may contains rich physical information, helping Sora to understanding the physical world. This indicates that the incorporating physical engine may be a potential path towards building world moels. 

## **3 WORLD MODELS FOR AUTONOMOUS DRIVING** 

Driving requires navigating uncertainty. It is crucial to understand the uncertainty inherent in autonomous driving to make safe decisions, where even a minor mistake could have fatal consequences [171]. There are two primary forms of uncertainty: epistemic uncertainty, which stems from a deficit in knowledge or information, and aleatoric uncertainty, which is rooted in the inherent randomness of the real world [172]. To ensure safe driving, it is imperative to leverage past experiences embedded in world models to effectively mitigate both aleatoric and epistemic uncertainty. World models are adept at representing an agent’s spatiotemporal knowledge about its environment through the prediction of future changes [39]. Two primary types of world models exist within autonomous driving aimed at reducing driving uncertainty, i.e., world model for end-toend driving and world model as neural driving simulator. In the simulation environment, methods such as MILE [25] and TrafficBots [173] do not distinguish between epistemic and aleatoric uncertainties and incorporate them into the model based on reinforcement learning, enhancing their capacity for decision-making and future prediction, thereby paving the way to end-to-end autonomous driving. In the real environment, Tesla [174] and methods like GAIA-1 [28] and Copilot4D [175] involve utilizing generative models to construct neural driving simulators that produce 2D or 3D future scenes to enhance predictive capabilities, thus reducing aleatoric uncertainty. Additionally, generating new samples can mitigate epistemic uncertainty regarding rare instances such as corner cases. Figure 5 illustrates these two types of world models in autonomous driving. The neural driving simulator can be further subdivided into two categories: those generating 2D images and those simulating 3D scenes. 

### **3.1 End-to-end Driving** 

In the domain of autonomous driving, the development of world models assumes a crucial role as they strive to construct dynamic representations of environments. Accurate predictions about the future are imperative for ensuring safe maneuvering in contexts. However, constructing world models for autonomous driving poses distinct challenges, mainly originating from the intricate sample complexity in driving scenarios. end-to-end autonomous driving methods [25], [26], [27] strive to tackle these challenges by minimizing the search space and integrating 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

9 

TABLE 1 

Datasets for video generation. ASR: Automatic speech recognition. This table is reported by [156] 

|**Dataset**<br>**Year**|**Text**|**Domain**<br>|#**Video**|**Avg**|**Video len**|**Avg text len**|**Resolution**|
|---|---|---|---|---|---|---|---|
|MSVD [157]<br>2011<br>LSMDC [158]<br>2015<br>MSR-VTT [159]<br>2016<br>DiDeMo [160]<br>2017|Manual Caption<br>Manual Caption<br>Manual Caption<br>Manual Caption|Open<br>Movie<br>Open<br>Flickr|1970<br>118K<br>10K<br>27K|9.7s<br>4.8s<br>15.0s<br>6.9s|5.3hr<br>158hr<br>40hr<br>87hr|8.7 words<br>7.0 words<br>9.3 words<br>8.0 words|-<br>1080p<br>240p<br>-|
|ActivityNet [161]<br>2017|Manual Caption|Action|100K|36.0s|849hr|13.5 words|-|
|YouCook2 [162]<br>2018|Manual Caption|Cooking|14K|19.6s|176hr|8.8 words|-|
|VATEX [163]<br>2019|Manual Caption|Open|41K|10s|115hr|15.2 words|-|
|HowTo100M [164]<br>2019|ASR|Open|136M|3.6s|134.5Khr|4.0 words|240p|
|ACAV [165]<br>2021|ASR|Open|100M|10.0s|277.7Khr|-|-|
|YT-Temporal-180M [166]<br>2021|ASR|Open|180M|-|-|-|-|
|HD-VILA-100M [167]<br>2021|ASR|Open|103M|13.4s|371.5Khr|32.5 words|720p|
|WebVid-10M [168]<br>2021|Manual Caption|Open|10M|18.0s|50Khr|12.0 words|-|
|Vimeo25M [169]<br>2023|Automatic Caption|Open|25M|4.5s|-|10.0 words|-|
|InternVid [170]<br>2023|Automatic Caption|Open|234M|11.7s|760.3Khr|17.6 words|720P|
|Panda-70M [156]<br>2024|Automatic Caption|Open|70.8M|8.5s|166.8Khr|13.2 words|720p|
|<br>|||||||●<br>**Cosmos**|
|●<br>**End-to-End Driving**||||||●<br>**DrivingDojo**|**GAIA-2**<br>●|
|●**Neural Driving Simulator (2D)**|||●|**SubjectDr**|**ive**<br>|●<br>**DriveWorld**|●<br>**DIO**|
|●**Neural Driving Simulator (3D)**|||●|**Think2Dri**<br>|**ve**<br>|**LAW**<br>●|**PreWorld**<br>●|
||||●|**DriveDre**|**amer-2**<br>|●**GEM**|●<br>**DiST-4D**|
|**TrafficBots**<br>●<br>**Iso-Dream**<br>●|**Driving**<br>**Diffusion**<br>●|**Panacea**<br>●<br>**Drive-WM**<br>●|●<br>|**GenAD**||●**DriveDreamer4**|●**UMGen**<br>**D**|
|**DriveDreamer**<br>●<br>**MILE**<br>●|**ADrive-I**<br>●|**WoVoGe**<br>●|●<br><br>|**Vista**||●**ReconDreamer**|●**MaskGWM**|
|**GAIA-1**<br>●<br>**SEM2**<br>●|**Copilot4D**<br>●|●<br><br>|●<br><br>|**LidarDM**||●**UniScene**|●**Raw2Drive**|
|**UniWorld**<br>●<br>**Tesla**<br>**World Model**<br>●|**MUVO**<br>●|**OccWorl**<br><br>**ViDAR**<br>●|●<br>|**MagicDri**|**ve3D**<br>|●<br>**GaussianWorld**|●<br>**AdaWM**|
|2023<br>2023.9<br>20|2023.<br>23.11|12|2024.5||2024.12||2025|


Fig. 5. Timeline of World Models in Autonomous Driving. End-to-end driving and neural driving simulator (both 2D and 3D) approaches are emerging since 2023. 

TABLE 2 

Summary of end-to-end driving methods based on world models. Img, Act, Seg, and Dest stand for images, action, segmentation, and destination, respectively. 

|**Method**|**Type**|**Core Structure**|**Reward**|**Input**|**Output**|**Simulator**|
|---|---|---|---|---|---|---|
|Iso-Dream [26]|Reinforcement Learning|RSSM [176]|✓|Img, Act|Img, Act|CARLA v1|
|MILE [25]|Imitation Learning|PGM [151]|_×_|Img, Act|Img, Act, BEV Seg|CARLA v1|
|SEM2 [27]|Reinforcement Learning|RSSM [176]|✓|Img, Act|Img, Mask|CARLA v1|
|TrafficBots [173]|Reinforcement Learning|CVAE [177]|✓|Static Map, Traffic Lights, Act|Act, Dest|CARLA v1|
|Think2Drive [178]|Reinforcement Learning|RSSM [176]|✓|Box, HD-Map, Traffic Lights|Act|CARLA v2|


explicit disentanglement of visual dynamics on the CARLA simulator [179]. The comparison of existing end-to-end driving methods based on world models is illustrated in Table 2. 

Iso-Dream [26] introduces a Model-Based Reinforcement Learning (MBRL) framework, aimed at effectively disentangling and utilizing controllable and noncontrollable state transitions via reinforcement learning. Furthermore, Iso-Dream optimizes the agent’s behavior based on the separated latent imaginations of world models. In detail, Iso-Dream projects non-controllable states into the future to estimate state values and links them with the current controllable state. Iso-Dream enhances the agent’s long-horizon 

decision-making capabilities, exemplified in scenarios like autonomous vehicles proactively evade potential hazards by anticipating the movements of surrounding vehicles. 

Iso-Dream learns the world model by mapping the 2D image in front view to control signals, which is not suitable for autonomous driving in 3D space. To address this issue, MILE [25] integrates the world model with imitation learning in 3D space, i.e., Bird’s Eye View (BEV) space. MILE uses 3D geometry as an inductive bias and creates a latent space from expert driving videos. The training occurs using an offline dataset of urban driving, devoid of any necessity for online engagement with the scene. In performance, it surpasses prior cutting-edge methods 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

10 

by a significant 31% margin in driving score on CARLA, even when operating in entirely new town and weather conditions. Moreover, MILE demonstrates its capability to execute intricate driving maneuvers solely based on plans generated through imaginative processes. 

Similar to MILE, SEM2 [27] also constructs a world model in 3D space. SEM2 employs a novel approach by incorporating a latent filter to isolate crucial task-specific features and then utilizes these features to reconstruct a semantic mask. Additionally, it utilizes a multi-source sampler during training, which merges standard data with various corner case data within a single batch, effectively ensuring a balanced data distribution. Specifically, SEM2 takes camera and LiDAR as inputs, encoding them into a latent state with deterministic and stochastic variables. The initial latent state is subsequently employed to regenerate the observation. Following this, the latent semantic filter isolates driving-relevant features from the latent state, reconstructs the semantic mask, and predicts the reward. Extensive experiment conducted on the CARLA simulator showcases SEM2’s adeptness in sample efficiency and robustness to variations in input permutations. 

TrafficBots [173], another end-to-end driving method based on world model, places emphasis on forecasting the actions of individual agents within a given scenario. By factoring in the destination of each agent, TrafficBots utilizes a Conditional Variational Autoencoder (CVAE) [177] to imbue individual agents with unique characteristics, enabling action anticipation from a BEV perspective. TrafficBots offers quicker operational speeds and scalability to handle larger numbers of agents. Experiments carried out on the Waymo dataset illustrate TrafficBots’ capacity to emulate realistic multi-agent behaviors and attain promising results in motion prediction tasks. 

The above methods [25], [26], [27], [173] were experimented in CARLA v1, but inherently face challenges regarding data inefficiency in CARLA v2. CARLA v2 offers a more quasi-realistic testbed. Addressing the complexities of CARLA v2 scenarios, Think2Drive [178], a model-based reinforcement learning method for autonomous driving, encourages the planner to _think_ within the learned latent space. This approach significantly enhances training efficiency by utilizing a low-dimensional state space and leveraging parallel computing of tensors. Think2Drive achieves expertlevel proficiency on CARLA v2 simulator after a mere 3-day training period utilizing a single A6000 GPU. Furthermore, Think2Drive introduces the CornerCase Repository, a novel benchmark designed to assess driving models across diverse scenarios. 

Despite the advancements seen in world models for endto-end driving using reinforcement learning, a significant limitation remains: its primary emphasis on simulation environments. Next, we will delve into research on world models for autonomous driving in real-world scenarios. 

### **3.2 Neural Driving Simulator** 

High-quality data serves as the bedrock for training deep learning models. While text and image data are readily available at low costs, acquiring data in the realm of autonomous driving poses challenges owing to factors such 

as spatio-temporal complexities and concerns regarding privacy. This is particularly true for addressing long-tail targets that directly impact realistic driving safety. World models are pivotal for understanding and simulating the complex physical world [28]. Some recent endeavors have introduced diffusion models [54] into the domain of autonomous driving to build world models as neural simulators to generate requisite autonomous 2D driving videos [28], [29], [180], [181]. Additionally, some methods employ world models to generate 3D occupancy grids or LiDAR point clouds depicting future scenes [175], [182], [183], [184]. Table 3 provides an overview of these neural driving simulator methods based on world models. 

### _3.2.1 2D Scene Generation_ 

World models for driving video generation entail tackling two pivotal challenges: _Consistency_ and _Controllability_ . Consistency is crucial for maintaining temporal and cross-view coherence between generated images, whereas controllability ensures that generated images align with corresponding annotations [30]. The comparison of exiting 2D driving video generation methods based on world models are shown in Table 4. 

GAIA-1 [28] is a cutting-edge generative world model designed to produce lifelike driving videos, offering precise manipulation of both ego-vehicle actions and environmental elements. GAIA-1 tackles the challenge of world modeling by leveraging video, text, and action inputs as sequences of tokens, predicting subsequent tokens in an unsupervised way. Its structure comprises two main elements: the world model and the video diffusion decoder. The world model, boasting 6.5 billion parameters, underwent a 15-day training period utilizing 64 NVIDIA A100s, while the video decoder, with 2.6 billion parameters, was trained for the same duration using 32 NVIDIA A100s. The world model meticulously examines the elements and dynamics within the scene, whereas the diffusion decoder transforms latent representations into high-fidelity videos imbued with intricate realism. GAIA1’s training corpus comprises 4,700 hours of driving videos collected in London, spanning from 2019 to 2023. Notably, GAIA-1 demonstrates an understanding of 3D geometry and can capture the complex interactions induced by road irregularities. Furthermore, GAIA-1 adheres to similar scaling laws observed in Large Language Models (LLMs). With its learned representations and control over scene elements, GAIA-1 opens new possibilities for enhancing embodied intelligence. 

While GAIA-1 can generate realistic autonomous driving scene videos, its controllability is limited to using only text and action as conditions for video generation, whereas autonomous driving tasks require adherence to structured traffic constraints. DriveDreamer [29], which excels in controllable driving video generation, seamlessly aligns with text prompts and structured traffic constraints, including HD-Map and 3D box data. The training pipeline of DriveDreamer comprises two stages: initially, DriveDreamer is trained with traffic structural information as intermediate conditions, significantly improving sampling efficiency. In the subsequent stage, the world model is developed through video prediction, where driving actions are iteratively utilized to update future traffic structural conditions. This 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

11 

TABLE 3 

Summary of model structure for neural driving simulator based on world models in autonomous driving. Img, Act, PC, Traj, Occ, HD, Flow, Lay, Obj, Seq, and Arg2 stand for images, action, point cloud, trajectory, occupancy, HD-Map, optical flow, layout, objects, sequence, and Argoverse2, respectively. 

|**Task**|**Method**|**Data Source**|**Architecture**|**Encoder**|**Decoder**|**Input**|**Output**|
|---|---|---|---|---|---|---|---|
|2D|GAIA-1 [28]<br>DriveDreamer [29]<br>DrivingDiffusion [186]<br>ADriver-I [187]<br>Panacea [30]<br>Drive-WM [32]<br>WoVoGen [188]<br>DriveDreamer-2 [31]<br>GenAD [180]<br>SubjectDrive [181]|Wayve [28]<br>nuScenes [185]<br>nuScenes [185]<br>nuScenes [185]<br>nuScenes [185]<br>nuScenes [185]<br>nuScenes [185]<br>nuScenes [185]<br>OpenDV-2K [180], nuScenes [185]<br>nuScenes [185]|GPT<br>Diffusion<br>Diffusion<br>Diffusion<br>Diffusion<br>Diffusion<br>Diffusion<br>Diffusion<br>Diffusion<br>Diffusion|VQ-VAE<br>VAE<br>Diffusion Encoder<br>CLIP-ViT<br>Diffusion Encoder<br>VAE<br>4D Volume Encoder<br>VAE<br>Diffusion Encoder<br>Diffusion Encoder|Video Diffusion Decoder<br>Task Specific Decoder<br>Diffusion Decoder<br>Video Diffusion Decoder<br>Diffusion Decoder<br>VAE Decoder<br>Diffusion Decoder<br>Video Decoder<br>Diffusion Decoder<br>Diffusion Decoder|Img, Text, Act<br>Img, Act, Box, Text<br>Img, Flow, Text, 3D Lay<br>Img, Act<br>Img, Text, BEV Seq<br>Img, Act<br>Img, Text, HD, Occ, Obj<br>Img, HD, Traj, Box, Text<br>Img, Text, Act<br>Img, Subject|Img<br>Img, Act<br>Img<br>Img, Act<br>Img<br>Img, Traj<br>Img, HD, Occ<br>Img<br>Img<br>Img|
|3D|UniWorld [189]<br>Copilot4D [175]<br>MUVO [182]<br>OccWorld [192]<br>ViDAR [183]<br>LidarDM [193]<br>DriveWorld [184]|nuScenes [185]<br>nuScenes [185], KITTI [190], Arg2 [191]<br>CARLA v1 [179]<br>nuScenes [185]<br>nuScenes [185]<br>KITTI-360 [194], Waymo [195]<br>nuScenes [185], OpenScene [196]|Transformer<br>Diffusion<br>GRU<br>GPT<br>Transformer<br>Diffusion<br>Transformer|BEV Encoder<br>VQ-VAE<br>SensorFusion<br>VQ-VAE<br>BEV Encoder<br>Diffusion Encoder<br>BEV Encoder|Task Specific Decoder<br>VQ-VAE Decoder<br>Task Specific Decoder<br>VQ-VAE Decoder<br>Latent Render<br>Diffusion Decoder<br>Task Specific Decoder|Img<br>PC, Act<br>Img, PC, Act<br>Occ, Ego Poses<br>Img, Ego Poses<br>Img, Traffic Lay<br>Img, Act, Ego Poses|Img, Occ<br>PC<br>Img, Act, Occ<br>Occ, Ego Poses<br>PC<br>PC<br>Occ, Act|


TABLE 4 

Comparison of FVD and FID metrics with 2D driving video generation methods based on world models on the validation set of the nuScenes dataset. 

|**Method**|**Multi-View**|**Multi-Frame**|**FVD**_↓_|**FID**_↓_|
|---|---|---|---|---|
|DriveDreamer [29]||✓|452.0|52.6|
|DriveDreamer [29]|✓|✓|340.8|14.9|
|ADriver-I [187]||✓|97.0|5.5|
|WoVoGen [188]|✓|✓|418.0|27.6|
|DrivingDiffusion [186]|✓|✓|332.0|15.8|
|Panacea [30]|✓|✓|139.0|17.0|
|SubjectDrive [181]|✓|✓|124.0|16.0|
|GenAD-nus [180]|✓|✓|244.0|15.4|
|GenAD-OpenDV [180]|✓|✓|184.0|15.4|
|<br>Drive-WM [32]|✓|✓|122.7|15.8|
|DriveDreamer-2 [31]|✓|✓|55.7|11.2|


enables DriveDreamer to anticipate variations in the driving environment based on different driving strategies. Through extensive experiments on the challenging nuScenes [185] benchmark, DriveDreamer is confirmed to enable precise and controllable video generation, representing the structural constraints of real-world traffic situations. 

To further bolster the consistency and controllability of generated multi-view videos, DriveDreamer-2 [31] is introduced as an evolution of the DriveDreamer framework. DriveDreamer-2 integrates a LLM to augment the controllability of video generation. Initially, DriveDreamer2 integrates an LLM interface to interpret user queries and translate them into agent trajectories. Subsequently, it generates an HD-Map in accordance with traffic regulations based on these trajectories. Additionally, DriveDreamer-2 proposes the unified multi-miew model to improve temporal and spatial consistency to generate multi-view videos. 

Different from DriveDreamer-2 with LLM, ADriver-I [187] leverages Multimodal Large Language Models (MLLMs) to enhance the controllability of generating driving scene videos. Inspired by the interleaved document approach in MLLMs, ADriver-I introduces interleaved vision-action pairs to establish a standardized format for visual features and their associated control signals. These vision-action pairs are utilized as inputs, and ADriver-I forecasts the control signal of the present frame in an autoregressive manner. ADriver-I continues this iterative process with the predicted next frame, 

enabling it to achieve autonomous driving in the synthesized environment. Its performance is rigorously assessed through extensive experimentation on datasets such as nuScenes [185] and sizable proprietary datasets. 

ADriver-I is limited to generating single-view videos. To generate multi-view videos as DriveDreamer-2, Panacea [30] and DrivingDiffusion [186] are proposed. Panacea [30] is an innovative video generation system designed specifically for panoramic and controllable driving scene synthesis. It operates in two stages: initially crafting realistic multi-view driving scene images, then expanding these images along the temporal axis to create video sequences. For panoramic video generation, Panacea introduces decomposed 4D attention, enhancing both multi-view and temporal coherence. Additionally, Panacea utilizes ControlNet to incorporate BEV sequences. Beyond these fundamental features, Panacea maintains flexibility by enabling manipulation of global scene attributes through textual descriptions, including weather, time, and scene details, providing a user-friendly interface for generating specific samples. DrivingDiffusion [186] also presents a multi-stage approach for generating multi-view videos. It involves several crucial stages: multi-view singleframe image generation, shared single-view video generation across multiple cameras, and post-processing capable of handling extended video generation. It also introduces local prompts to improve the quality of images effectively. Subsequent to the generation process, post-processing is employed to enhance the coherence among different views in subsequent frames. Additionally, it utilizes a temporal sliding window algorithm to prolong the video duration. 

The objective of the above methods is to generate realistic driving scenario videos given certain conditions. DriveWM [32] takes this a step further by utilizing predicted future scene videos for end-to-end planning applications to enhance driving safety. Drive-WM introduces multi-view and temporal modeling to generate multi-view frames. To improve multi-view consistency, Drive-WM proposes factorizing the joint modeling to predict intermediate views conditioned on adjacent views, significantly enhancing consistency between views. Drive-WM also introduces a simple yet effective unified condition interface, enabling flexible utilization of diverse conditions such as images, text, 3D layouts, and actions, thereby simplifying conditional 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

12 

generation. Furthermore, by leveraging the multi-view world model, Drive-WM explores end-to-end planning applications to enhance autonomous driving safety. Specifically, at each time step, Drive-WM utilizes the world model to generate predicted future scenarios for trajectory candidates sampled from the planner. These futures are evaluated using an imagebased reward function, and the optimal trajectory is selected to extend the planning tree. Testing on real-world driving datasets validates Drive-WM’s capability to produce toptier, cohesive, and manageable multi-view driving videos, thereby unlocking avenues for real-world simulations and safe planning. 

Control signals like bounding boxes or HD-Maps provide a sparse representation of the driving scene. WoVoGen [188] enhances diffusion-based generative models by introducing a 4D world volume. Initially, WoVoGen builds a 4D world volume by merging a reference scene with a forthcoming vehicle control sequence. This volume then guides the generation of multi-view imagery. Within this 4D structure, each voxel is enriched with LiDAR semantic labels obtained via the fusion of multi-frame point clouds, enhancing the depth and complexity of environmental comprehension. 

SubjectDrive [181] has undertaken further research to explore the effects of increasing the scale of generated videos on the performance of perception models in autonomous driving. Through their investigations, they have demonstrated the efficacy of scaling generative data production in continuously enhancing autonomous driving applications. It has pinpointed the pivotal significance of enhancing data diversity in efficiently expanding generative data production. Consequently, SubjectDrive has developed an innovative model incorporating a subject control mechanism. 

The above methods for generating driving videos have largely been studied on relatively small datasets like nuScenes [185]. GAIA-1 [28] was trained on a dataset of 4,700 hours, but the training dataset is not publicly available. Recently, GenAD [180] has released the largest multimodal video dataset for autonomous driving, OpenDV2K, exceeding the scale of the widely used nuScenes dataset by a multiplier of 374. OpenDV-2K contains 2,059 hours of video content accompanied by textual annotations, drawn from a combination of 1,747 hours sourced from YouTube and an additional 312 hours gathered from public datasets. Addressing common challenges such as causal confusion and handling large motions, GenAD utilizes causal temporal attention and decoupled spatial attention mechanisms to effectively capture the rapid spatio-temporal fluctuations present in highly dynamic driving environments. This architecture allows GenAD to generalize across diverse scenarios in a zero-shot way. This acquired understanding is further substantiated through the application of its learned knowledge to driving challenges, including planning and simulation tasks. 

### _3.2.2 3D Scene Generation_ 

In addition to generating 2D videos for autonomous driving through world modeling, some methods delve into utilizing world models to produce 3D LiDAR point clouds or 3D occupancy grids. 

Copilot4D [175] presents an innovative approach to world modeling by first tokenizing LiDAR point cloud 

observations with VQ-VAE [144], then predicting future LiDAR point clouds via discrete diffusion. To efficiently decode and denoise tokens in parallel, Copilot4D modifies the masked generative image Transformer to fit within the discrete diffusion framework with slight adjustments, yielding significant improvements. When utilized for training world models based on LiDAR point cloud observations, Copilot4D achieves a remarkable reduction of over 65% in Chamfer distance for point cloud forecasting at 1s prediction and over 50% at 3s prediction across datasets such as nuScenes [185], Argoverse2 [191], and KITTI Odometry [190]. 

Copilot4D utilizes unannotated LiDAR data to construct its world model, while OccWorld [192] delves into the 3D occupancy space for the representation of 3D scenes. OccWorld initiates its approach by employing a VQ-VAE [144] to refine high-level concepts and derive discrete 3D semantic occupancy scene tokens in a self-supervised manner. Subsequently, it customizes the GPT [94] architecture, introducing a spatial-temporal generative Transformer to forecast scene tokens and ego tokens. Through these advancements, OccWorld achieves significant results in 4D occupancy forecasting and planning. 

Copilot4D and OccWorld employ past LiDAR or 3D occupancy frames to generate future 3D scenes, whereas MUVO [182] adopts a more comprehensive strategy by leveraging raw camera and LiDAR data as input. MUVO aims to acquire a sensor-agnostic geometric representation of the environment and predicts future scenes in the forms of RGB images, 3D occupancy grids, and LiDAR point clouds. Initially, MUVO undertakes image and LiDAR point cloud processing, encoding, and fusion utilizing a Transformer-based architecture. Subsequently, it inputs the latent representations of the sensor data into a transition model to establish a probabilistic model of the current state. Concurrently, MUVO forecasts the probabilistic model of future states and generates samples from it. 

While Copilot4D, OccWorld, and MUVO generate 3D scenes without control, LidarDM [193] excels in producing layout-aware LiDAR videos. LidarDM employs latent diffusion models to generate the 3D scene, integrating dynamic actors to establish the underlying 4D world, and subsequently generating realistic sensory observations within this virtual environment. Beginning with the input traffic layout at time _t_ = 0, LidarDM initiates the generation process by creating actors and the static scene. Subsequently, LidarDM generates the motion of the actors and the ego-car, composing the underlying 4D world. Finally, a generative- and physicsbased simulation is utilized to produce realistic 4D sensor data. The LiDAR videos generated by LidarDM are realistic, layout-aware, physically plausible, and temporally coherent. They demonstrate a minimal domain gap when tested with perception modules trained on real data. 

As an abstract spatio-temporal representation of reality, the world model possesses the capability to predict future states based on the present. The training mechanism of world models holds promise in establishing a foundational pre-trained model for autonomous driving. UniWorld [189], ViDAR [183], and DriveWorld [184] delve into the exploration of 4D pre-training based on world models, aiming to enhance various downstream tasks of autonomous driving, such as perception, prediction, and planning. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

13 

UniWorld [189] introduces the concept of predicting future 3D occupancy as a pre-text task for autonomous driving, leveraging extensive unlabeled image-LiDAR pairs for 4D pre-training. It takes multi-view images as inputs, generating feature maps in a unified BEV space [197]. These BEV representations are then utilized by a world model head to predict the occupancy of future frames. UniWorld demonstrates improvements in intersection over union for tasks like semantic scene completion and motion prediction compared to 3D pre-training methods [198], [199]. 

While UniWorld has demonstrated the effectiveness of 4D pre-training based on world models for autonomous driving, it predicts future scenes by adding a simple occupancy head. ViDAR [183] proposes latent rendering operator with differentiable ray-casting for future scene prediction. ViDAR consists of three main components: history encoder, latent rendering operator, and future decoder. The history encoder embeds visual sequences into BEV space. Subsequently, these BEV features undergo processing by the latent rendering operator, which significantly bolsters downstream performance. The future decoder, functioning as an autoregressive Transformer, utilizes historical BEV features to iteratively forecast future LiDAR point clouds for various timestamps. 

To enhance 4D pre-training for autonomous driving by better capturing spatio-temporal dynamics, DriveWorld [184] takes a further step by separately addressing temporal and spatial information. DriveWorld introduces the memory state-space model to reduce uncertainty within autonomous driving across both spatial and temporal dimensions. Firstly, to tackle aleatoric uncertainty, DriveWorld proposes the dynamic memory bank module, which learns temporalaware latent dynamics to predict future scenes. Secondly, to mitigate epistemic uncertainty, DriveWorld introduces the static scene propagation module, which learns spatialaware latent statics to provide comprehensive scene context. Moreover, DriveWorld introduces the task prompt, utilizing semantic cues as guidance to dynamically adjust the feature extraction process for various driving tasks. 

## **4 WORLD MODELS FOR AUTONOMOUS AGENTS** 

In artificial intelligence, an autonomous agent refers to a system that can perceive its surrounding environment through sensors (such as cameras) and act upon it through actuators to achieve specific goals [200]. These agents can be physical, like robots, or virtual, such as software programs that perform tasks in digital environments. 

Given a goal, agents need to plan a sequence of actions. There are already many successful algorithms for dynamic planning in known environments. In most cases, however, the environment is complex and stochastic, making it difficult to model by human experience explicitly. Therefore, this field’s core topic is how agents learn to plan in an unknown and complex environment. One way to solve this problem is to have the agent accumulate experience and learn behaviors directly from the interaction with the environment, without modeling the state changes of the environment (the so-called model-free reinforcement learning). While this solution is simple and flexible, the learning process relies on many interactions with the environment, which may be extremely expensive, even unacceptable. 

World Models [201] is the first work that introduces the concept of the world model in the field of reinforcement learning, modeling knowledge about the world from the agent’s experience and gaining the ability to predict the future. This work demonstrates that even a simple RNN model can capture the dynamics of the environment and support the agent to learn and evolve policies in this model. This learning paradigm is referred to as _learning in imagination_ [33]. With world models, the cost of trials and failures can be greatly reduced [202]. 

In this section, we introduce the world models for autonomous agents. We first describe the general framework of a world model-based agent, including the key components and the model structures widely used in world model-based agents in Section 4.1. Then, we introduce the agents serving a variety of tasks, such as game agents and robotics, in Section 4.2. Finally, we present the benchmarks that are commonly used to evaluate the performance of world model-based agents. 

### **4.1 General Framework of an Agent based on World Model** 

Most works implement world model-based agents under a basic framework originating from robotics. In the framework, the world model is the core component. To model and predict the surrounding environment, pioneers proposed several effective structures, which are widely used in later works. In this section, we describe in detail the key components of the framework and the widely used structures of world models. 

### _4.1.1 Key Components_ 

From the view of software engineering, an agent system can be decomposed into four components [203]: **Sensor** Sensors are the interface between an agent and its environment, providing the raw (or interpreted) information the robot needs to understand its current context and make decisions. Perception of the environment encompasses multiple modalities, including vision through cameras, audition through microphones, touch through touch sensors, etc. Among these modalities, vision is critical. Most research uses vision as the only way for agents to perceive the environment. **Actor.** Actors are the mechanisms through which an agent exerts influence or effectuates changes in its environment. They are the output devices that allow the agent to perform actions, such as motors for movement, robotic arms for manipulation, and communication interfaces for interaction with other systems or humans. The actions taken by the agent are determined by the decisions made within its planning system and are executed through the actuators. **Planning.** Planning is the cognitive process that enables the autonomous agent to determine a sequence of actions that will lead to achieving its goals. It involves analyzing the current state of the environment as perceived by the sensors, defining the desired end state, and selecting the most appropriate actions to bridge the gap between the current and desired states. The planning component must consider the agent’s capabilities, constraints, and the potential consequences of its actions. Effective planning allows the agent to act purposefully and adaptively, optimizing its behavior to achieve its objectives efficiently and effectively. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

14 

|●RSSM-based<br>●Diffusion-based||●Dr.G|||
|---|---|---|---|---|
|●JEPA-based<br>●LLM-based||●SWIM|●SafeDreamer||
|●Robot DreamPolicy<br>●Others<br>●Transformer-based||●DreamerV3<br>●HarmonyDream<br>●DayDreamer<br>●TWM|●Genie<br>●V-JEPA<br>●RoboDreamer<br>●UniSim|●RoboScape<br>●V-JEPA 2|
|●World Models|●DreamerPro|●STORM|●DIAMOND|●FlowDreamer|
|●PathDreamer<br>●SimPLe|●DreamingV2|●MC-JEPA|●This&That|●PEVA|
|●DreamerV2<br>●Plan2Explore|●TransDreamer|●A-JEPA|●GameNGen|●TesserAct|
|●LEXA<br>●DreamerV1|●IRIS|●I-JEPA|●NWM|●WorldVLA|
|●Dreaming<br>●PlaNet|●JEPA|●UniPi|●iVideoGPT|●UAV|
|Before 2021<br>2021<br>2|022<br>2|023<br>2|024<br>2|025|


Fig. 6. Chronological overview of video generation model. We present the world model-based autonomous agents proposed in recent years. The colors show different structures of world models. The RSSM dominated these efforts while the Transformer, JEPA, and diffusion are gaining more and more attention from 2022. 

**World Model.** A world model is an internal representation of the surrounding environment. This model is crucial for the agent’s ability to understand the context in which it operates, predict the outcomes of its actions, and make informed decisions. The world model interacts with the other three components through _tell_ and _ask_ interfaces [203]. That is to say, it receives information from other components to update its state and also responds to queries from other components. A robust world model can reasonably predict the future state when told with current perceptions and actions, thereby guiding the planning component to make wiser decisions. 

### _4.1.2 Widely-used Model Structure_ 

A world model’s key ability is predicting the environment’s future state. Given the inherent randomness in most environments, predictions should maintain a balance between determinism and uncertainty. Many researches have been conducted on this problem, proposing a variety of model structures. Figure 6 shows the works in this field. Among these works, the most widely-used structures are RSSM [176], [202], [204], [205], JEPA [39], [206], [207], [208], [209], and Transformer-based models [146], [210], [211], [212], [213]. **Recurrent State Space Model.** The Recurrent State Space Model (RSSM) is the core structure of the Dreamer series. RSSM aims to facilitate prediction in latent spaces. It learns a dynamic model of the environment from pixel observations and selects actions by planning in the encoded latent space. By decomposing the latent state into stochastic and deterministic parts, this model considers both deterministic and stochastic factors of the environment. Due to its exceptional performance in continuous control tasks for robots, many subsequent works have expanded upon its foundation. **Joint-Embedding Predictive Architecture.** The JointEmbedding Predictive Architecture (JEPA) is proposed in a paper by LeCun [39] that laid out a conceptual framework for future autonomous machine intelligence architecture. It learns the mapping from input data to predicted output. 

This model is different from traditional generative models as it does not directly generate pixel-level output, but makes predictions in a higher-level representation space, allowing the model to focus on learning more semantic features. Another core idea of JEPA is to train the network through self-supervised learning so that it can predict missing or hidden parts in the input data. Through self-supervised learning, models can be pre-trained on a large number of unlabeled data and then fine-tuned on downstream tasks, thereby improving their performance on a variety of visual [206], [208], [209] and non-visual tasks [207]. 

**Transformer-based World Models.** The Transformer [56] originates from the natural language processing task. It operates on the principle of the attention mechanism, which enables the model to simultaneously focus on different parts of the input data. Transformers have been proven to be more effective than Recurrent Neural Networks (RNNs) in many domains that require long-term dependencies and direct memory access for memory-based reasoning [214], thus gaining increasing attention in the field of reinforcement learning in recent years. Since 2022, multiple works have attempted to construct world models based on the Transformer and its variants [211], [212], [215], achieving better performance than the RSSM model on some complex memory interaction tasks [210]. Among them, Google’s Genie [213] has attracted considerable attention. This work constructs a generative interactive environment based on the ST-Transformer [216], trained through self-supervised learning from a vast collection of unlabeled internet video data. Genie demonstrates a new paradigm for manipulable world models, offering a glimpse into the immense potential for the future development of world models. 

### **4.2 Agents for Different Tasks** 

Many researchers have explored the application of agents in various fields and tasks, such as gaming, robotics, navigation, 

15 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

task planning, etc. Among the most widely studied tasks are games and robotics. 

### _4.2.1 Game Agent_ 

Getting AI systems to learn to play games has been an interesting topic for a long time. The research on game agents not only improves the game experience but more importantly, helps people develop more advanced algorithms and models. 

With the introduction of the Arcade Learning Environment (ALE) [217], Atari games have gained a lot of emphasis as a benchmark for reinforcement learning. The Atari collection includes more than 500 games, covering a wide variety of game types and challenges, making it ideal for evaluating the capabilities of reinforcement learning algorithms. Many studies have shown that reinforcement learning can make agents play games at a level comparable to that of human players [218], [219], [220], [221]. However, most of them require a huge amount of interaction steps with the environment. World models can predict future states of the environment, allowing agents to learn in imagination, thus significantly reducing the number of interactions required for learning. 

RES [222] is an RNN-based environment simulator that can predict the subsequent state of the environment based on a series of actions and corresponding environmental observations. Based on this capability, SimPLe [223] designs a novel stochastic video prediction model, which achieves significant improvement in sample efficiency. Under the constraint of 100K interactions, SimPLe has a much better performance in Atari games compared to previous modelfree reinforcement learning methods. 

DreamerV2 [34] trains a game agent based on the RSSM model [176]. Unlike previous approaches that use continuous latent representations, DreamerV2 uses discrete categorical variables. This discretization method enables the model to capture the dynamic changes in the environment more accurately. DreamerV2 further uses the actor-critic algorithm to learn the behaviors purely from imagined sequences generated by the world model and achieves performance comparable to human players on the Atari 200M benchmark [224]. 

IRIS [215] is one of the pioneers that apply Transformer [56] in the world model. The agent learns its skill in a world model based on the autoregressive Transformer. As pointed out by Robine et al. [212], the autoregressive Transformer can model more complex dependencies by allowing the world model to directly access previous states, while previous works can only view a compressed recurrent state. IRIS shows that the Transformer architecture is more efficient in sampling, outperforming humans in the Atari100k benchmark [223] by only two hours of gameplay. 

TWM [212] proposes a Transformer-XL [225]-based world model. Transformer-XL solves the problem of capturing long-distance dependencies in language modeling tasks by introducing the segment-level recurrence mechanism to extend the length of context. TWM migrates this capability into the world model, enabling the capture of long-term dependencies between the states of the environment. To run more efficiently, TWM further trains a model-free agent in the latent imagination, avoiding a full inference of the world model in runtime. 

STORM [211] sets a new record in no-resorting-tolookahead-search methods on Atari100k benchmark [223] by stochastic Transformer. Inspired by the fact that introducing random noise into the world model helps enhance the robustness and reduce cumulative errors in autoregressive predictions, STORM employs a categorical variational autoencoder [151], which inherently has a stochastic nature. 

Genie [213] is a novel generative environment developed by the DeepMind team. It learns the ability to generate interactive 2D worlds by unsupervised learning from many internet videos without labels. The most attractive point is that it can not only generate an entirely new virtual environment based on image or text prompts but also predict coherent video sequences of that environment frame by frame based on user input actions. Genie enhances the efficiency of virtual content creation as well as provides a rich interactive learning platform for the training of future AI agents. Although the current video quality and frame rate still need improvement, it has already demonstrated the immense potential of generative AI in building future virtual worlds. 

### _4.2.2 Robotics_ 

Getting an agent to learn to manipulate a robot is a long-term challenge. Agents are desired to plan autonomously, make decisions, and control actuators (e.g., robotic arms and legs) to complete complex interactions with the physical world. Common basic tasks include walking, running, jumping, grasping, carrying, and placing objects. Some of the more complicated tasks require a combination of several basic tasks, such as taking a specific item out of a drawer or making a cup of coffee. 

One difference between a robot and a game agent is that the goal of the robot is to interact with the real environment, which not only makes the environment dynamics more complex and stochastic but also greatly increases the cost of interacting with the environment during the training process. Therefore, it is particularly important to reduce the number of interaction steps with the environment and enhance sampling efficiency in such scenarios. In addition, the control of the actuators is in a continuous action space, which is also very different from the discrete action space in the game environment. 

Previous works of model-based planning [226], [227], [228] learn low-dimensional environment dynamics by assuming that access to the underlying state and the reward function is available. But in complex environments, this assumption is often untenable. Hafner et al. [176] suggested learning the environment dynamics from pixels and planning in latent spaces. They proposed RSSM, which is the base of the later Dreamer-like world models. They achieved similar performance to the state-of-art model-free methods within less than 1/100 episodes on six continuous control tasks of DeepMind Control Suite (DMC) [229], which proves that learning latent dynamics of the environments in the image domain is a promising approach. 

However, PlaNet [176] learns the behaviors by online planning, i.e., considering only rewards within a fixed imagination horizon, which brings shortsighted behaviors. To solve this problem, Hafner et al. further proposed DreamerV1 [33], an agent that learns long-horizon behaviors purely from 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

16 

the imagination of the RSSM-based world model. Predicting in latent space is memory efficient, thus allowing imagine thousands of trajectories in parallel. DreamerV1 uses a novel actor-critic algorithm to learn behaviors beyond the horizon. The evaluation performed on visual control tasks of DMC shows that DreamerV1 exceeds previous model-based and model-free approaches in data efficiency, computation time, and final performance. 

SafeDreamer [230] aims to address safe reinforcement learning, especially in complex scenarios such as visiononly tasks. SafeDreamer employs an online safety-reward planning algorithm for planning within world models to meet the constraints of vision-based tasks. It also combines Lagrangian methods with online and background planning within world models to balance long-term rewards and costs. SafeDreamer demonstrates nearly zero-cost performance across low-dimensional and visual input tasks and outperforms other reinforcement learning methods in the SafetyGymnasium benchmark [231], showcasing its effectiveness in balancing performance and safety in reinforcement learning tasks. 

The above works only learn and evaluate their performance in simple simulation environments, while the real environments often contain task-unrelated visual distractions such as complex backgrounds and varying lights. RSSM learns the world model by reconstructing image observations, making it very sensitive to visual distractions in images and difficult to capture small but important content. Therefore, based on DreamerV1 [33], Dreaming [232] avoids the autoencoding process by directly imagining and planning in the latent space, and trains the world model by contrastive learning, which does not rely on pixel-level reconstruction loss, so that the method is robust to visual distractions in the environment. DreamingV2 [205] further explores how to apply contrastive learning to the discrete latent space of DreamerV2 [34]. Experimental results on 5 simulated robot tasks with 3D space and photorealistic rendering show that DreamingV2 can effectively handle complex visual observations, and the performance is significantly better than that of DreamerV2. 

Similar efforts are made by DreamerPro [204] and Dr.G [233], both of which use a reconstruction-free approach to address the visual sensitivity issue of RSSM. The difference is that DreamerPro uses the prototype learning method to train the prediction of the world model in the latent space, which avoids the expensive computation caused by the large batch size required for contrast learning. Dr.G, on the other hand, uses a self-supervised method of double-contrast learning to replace the reconstruction loss in DreamerV1 [33]. Both are evaluated in environments from DMC synthesized with complex background videos, verifying their robustness to visual distractions. 

Besides those works involving simulated environments only, some works are trying to train a robot in the real world. The most difficult thing is that interaction with the real world is expensive or even dangerous. Thus the ability of _training in imagination_ is especially important in such scenarios. RobotDreamPolicy [234] learns a world model first and then learns the policy in the world model to reduce the interactions with the real environment. During the training of the world model, the robot executes random actions 

in the environment, collecting pairs of the image before action, action, and the image after action as the training data. DayDreamer [202] applies DreamerV2 [34] to 4 real robots and directly trains the model online in real environments. The authors found in experiments that the Dreamer model is capable of online learning in the real world, and can master a skill in a very short time. These works provide strong evidence that the sample efficiency of the world model can help robots learn various skills efficiently with fewer interactions. 

### _4.2.3 Diverse Environments and Tasks_ 

Besides game and robotic tasks, some research works have looked at other tasks such as navigation. PathDreamer [235] applies the idea of world model to indoor navigation tasks. The world model is used to enhance environmental awareness and predictive planning. Given one or more previous observations, PathDreamer can predict plausible panoramic images of the future, even for unseen rooms or regions behind corners. Furthermore, PathDreamer innovatively uses 3D point clouds for environment representation, which significantly improves navigation success. 

The JEPA series of work applies the architecture proposed by LeCun [39] to a variety of modal understanding and prediction tasks. I-JEPA [206] is a non-generative self-supervised learning method that learns highly semantic visual representations by predicting the representations of different target blocks within the same image from a single context block. A-JEPA [207] proposes a self-supervised learning method based on audio spectrograms, which effectively applies the successfully masked modeling principle from the visual domain to audio. A context encoder is used to predict and align the representations of different target blocks from the same audio spectrogram. MC-JEPA [208] is a self-supervised learning method that simultaneously learns video content features and motion features through JEPA, using a shared encoder to improve the accuracy of motion estimation and enrich the content features to include motion information. V-JEPA [209] extends I-JEPA to feature prediction in videos. It presents a suite of vision models that are exclusively trained based on the objective of feature prediction. These models are developed without relying on supervisory signals such as pre-trained image encoders, negative examples, text, and reconstruction techniques. 

Other research efforts aim to study agents suitable for diverse tasks. DreamerV3 [35] is a universal algorithm that realizes cross-domain learning with fixed hyperparameters by signal amplitude transformation and robust normalization. The authors evaluated multiple benchmark sets from Atari games, high/low dimensional continuous control tasks, survival tasks, spatial and temporal reasoning tasks, etc. The results show that DreamerV3 can master different domains only by relying on the same set of hyperparameters, and its performance is even better than some specialized algorithms designed for specific domains. DreamerV3 is also the first agent to successfully collect diamonds from scratch in Minecraft without providing any human experience. 

Plan2Explore [236] proposes a self-supervised two-stage learning process. In the first stage, the agent explores the environment in a self-supervised manner, gathers information about the environment, and summarizes past experiences 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

17 

in the form of a parametric world model. It is worth noting that no reward information is provided to the agent during this phase, and the exploration is performed by the agent autonomously. Then the agent learns behaviors in the trained world model for specific tasks. This stage can be done with little or no interaction with the environment. The two-stage learning process allows the agent to obtain a more universal world model, making the agent learn downstream tasks more efficiently. 

SWIM [237] aims to solve the learning of complex and general skills in the real world. SWIM claims that an agent must utilize internet-scale human video data to understand rich interactions carried out by humans and gain meaningful affordances. To this end, SWIM proposes a high-level, structured, human-centric action space that is applicable for both humans and robots. The world model is first trained from a large dataset containing around 50K egocentric videos. Then the world model is finetuned with robot data to fit the robot domain. After that, behaviors for specified tasks can be learned in the trained world model using the standard cross-entropy method [238]. With the help of human action videos, SWIM achieves about two times higher success than prior approaches while requiring less than 30 minutes of real-world interaction data. 

HarmonyDream [239] identifies the world model as a multi-task model consisting of observation modeling tasks and reward modeling tasks. HarmonyDream argues that traditional world modeling methods, which tend to focus on observation modeling, can become difficult and inefficient due to the complexity of the environment and the limited capacity of the model. HarmonyDream maintains a balance between observation modeling and reward modeling by automatically adjusting the loss coefficient, which can be adapted to different types of tasks and avoid complicated hyperparameter adjustments. 

RoboDreamer [38] learns compositional world models to enhance robotic imagination. It decomposes the video generation process and leverages the inherent compositionality of natural language. In this way, it can synthesize video plans of unseen combinations of objects and actions. RoboDreamer dissects language instructions into a set of primitives, which then serve as distinct conditions for a set of models to generate videos. This method not only demonstrates strong zero-shot generalization capabilities but also shows promising results in multimodal-instructional video generation and deployment on robotic manipulation tasks. 

UniSim [37] is a generative simulator for real-world interactions. UniSim contains a unified generative framework taking action as input that integrates diverse datasets across different modulations. With this approach, UniSim can simulate the visual outcomes of both high-level instructions and low-level controls. UniSim can be utilized for various applications, such as controllable game content creation and the training of embodied agents in simulated environments, which can be directly deployed in the real world. 

### **4.3 Commonly Used Benchmarks** 

A variety of benchmarks are used to measure the performance of game agents and robotics. The evaluation method 

TABLE 5 

Human-normalized scores (HNS in %) of world-model-based agents on 26 games in the Atari100k benchmark [223]. The highest score of each row is bolded. 

||SimPLe<br>[223]|DreamerV3<br>[35]|IRIS<br>[215]|TWM<br>[212]|STORM<br>[211]|Harmony<br>Dreamer<br>[239]|DIAMOND<br>[**?**]|
|---|---|---|---|---|---|---|---|
|Alien|5.6|10.6|2.8|6.5|**11.0**|9.6|7.5|
|Amidar|4.0|7.8|8.0|6.8|11.6|7.9|**12.8**|
|Assault|58.7|93.1|250.6|88.6|111.4|150.2|**251.0**|
|Asterix|11.1|8.7|7.8|10.9|9.9|11.2|**42.1**|
|BankHeist|2.7|85.9|5.3|61.2|84.8|**142.8**|0.7|
|BattleZone|4.8|28.4|30.8|7.8|32.1|**40.5**|6.7|
|Boxing|64.2|649.2|583.3|645.0|665.8|665.8|**723.3**|
|Breakout|51.0|101.7|284.7|63.5|49.7|178.1|**454.2**|
|Chopper.|2.6|-5.9|11.5|13.5|**16.4**|10.6|8.5|
|CrazyClimber|206.8|345.0|193.8|243.7|223.5|287.3|**352.9**|
|DemonAttack|3.1|8.3|**103.5**|10.9|0.7|2.8|7.5|
|Freeway|56.4|0.0|105.1|82.1|**114.9**|0.0|112.5|
|Frostbite|4.0|19.8|4.5|**33.0**|29.3|14.4|4.9|
|Gopher|15.7|161.1|91.8|65.8|370.4|**593.3**|261.7|
|Hero|5.5|34.0|20.2|20.9|33.6|**41.4**|15.4|
|Jamesbond|26.1|151.9|158.4|121.8|**175.3**|105.2|145.5|
|Kangaroo|0.0|135.6|26.4|39.8|139.3|169.8|**178.7**|
|Krull|56.8|579.3|470.1|445.1|638.4|576.7|**656.9**|
|KungFuMaster|65.0|94.1|95.7|108.1|**115.3**|97.9|82.1|
|MsPacman|17.6|15.3|10.4|19.3|**35.6**|20.7|24.8|
|Pong|94.9|109.6|100.0|111.9|89.8|112.5|**116.4**|
|PrivateEye|0.0|1.2|0.1|0.1|**11.2**|4.2|0.1|
|Qbert|8.5|24.4|4.4|23.8|**32.8**|28.4|32.6|
|RoadRunner|71.9|198.6|122.6|116.1|224.1|186.8|**263.8**|
|Seaquest|1.5|1.3|1.4|**1.7**|1.1|1.4|1.1|
|UpNDown|25.2|63.9|27.0|**138.4**|66.8|92.7|29.8|
|Avg. HNS|33.2|112.4|104.6|95.6|126.7|136.6|**145.9**|


TABLE 6 

The performance (Episode Return) of some world-model-based agents in different robot tasks. This table is reported by Okada et al. [205]. Episode Return is defined as the sum of all rewards earned by the agent in a full episode. The highest value of each row is bolded. 

||Dreamer<br>[33]|DreamerV2<br>[34]|Dreaming<br>[232]|DreamingV2<br>[205]|DreamerPro<br>[204]|
|---|---|---|---|---|---|
|3D Robot-arm tasks f|rom Dreami|ng [232] and R|oboSuite [240]|||
|UR5-reach|701±223|704±222|752±1178|**776**±194|668±252|
|Lift|134±46|165±126|174±107|**327**±150|138±64|
|Door|154±32|190±126|319±173|**383**±143|111±110|
|PegInHole|354±47|376±59|353±50|**436**±26|327±43|
|Difficult pole-swingu<br>|i p tasks from<br>|i    DMC [229]<br>||||
|Acrobot-swingup|382±147|309±131|359±111|**470**±129|-|
|Cartpole-two-poles|256±65|248±103|273±53|**308**±55|-|
|3D robot tasks from<br>|DMC [229]<br>|||||
|Quadruped-walk|242±120|350±89|379±189|**492**±127|-|
|Quadruped-run|269±114|352±68|339±128|**385**±91|-|
|Reach-duplo|5±11|149±62|145±61|**199**±43|87±76|
|2D robot tasks from|DMC [229]|||||
|Cheetah-run|776±120|**811**±75|542±132|768±24|-|
|Walker-walk|906±70|**951**±28|518±76|857±115|-|
|Reacher-easy|658±429|923±215|**947**±100|924±210|-|
|Reacher-hard|247±392|175±340|**743**±346|598±447|-|
|Finger-turn-easy|665±430|498±469|**842**±286|434±469|-|
|Finger-turn-hard|533±426|600±417|**858**±210|484±434|-|


is usually to test the completion of several specific tasks or the rewards obtained by the agent after a limited amount of interactive learning in a specific environment. 

Atari100k [223] is the most commonly used benchmark for game agents, which uses a subset of 26 Atari games from the Arcade Learning Environment [217]. For each game, the agent is allowed to collect up to 100K interactions. With 4 frames per interaction, this is equivalent to 400K frames or 114 minutes (at 60FPS). To normalize the scores across different games, a metric called Normalized Human Score (NHS) [224] is proposed, which is defined as: 


Where _score_ human is the score achieved by the professional human player and _score_ random is the score achieved by an 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

18 

agent using purely random policy. This metric evaluates the performance of agents compared to the professional human player. Table 5 collects the performance reported by the world model-based game agents mentioned in this survey. Overall, recent methods have been able to outperform human players in about half of these 26 games with a constraint of only 100K interactions, and in some games, several times over. At the same time, in other games such as Alien, Amidar, and Seaquest, they perform much worse than human players. This may be because the environment dynamics of these games are more complex, and 100K interactions are not enough for the agent to have a full understanding of the environment. On the other hand, low-quality images make some important elements easily ignored by imagereconstruction-based algorithms, resulting in an incorrect understanding of the environment. 

For robotic tasks, there are several benchmarks adopted for different tasks and environments. DMC [229] is the most commonly used benchmark for robot learning. It contains a virtual environment that supports research into how agents learn complex physical tasks. This environment offers a diverse set of control tasks, from simple object moving to complex manipulator operations, as well as navigation tasks in 3D space. These tasks are built on top of the MuJoCo physics engine [241]. It also supports high-dimensional observing spaces, including pixel-level visual inputs, which makes it suitable for studying vision-driven reinforcement learning algorithms. To increase the visual diversity, DMC Remaster [242] extends DMC with seven types of visual factors, including the ground texture, the background, the color of robot, the color of target, the specular property, the camera position, and the light, thus presents a greater challenge to the visual robustness of the algorithm. 

Another common benchmark is RoboSuite [240]. It is a robot learning simulation framework powered by MuJoCo physics engine that provides a standardized benchmark environment for robot learning research. The RoboSuite includes a variety of robot models, grippers, controller modes, and a standardized set of benchmark tasks. In addition, it supports generating new environments programmatically with a modular API design that allows researchers the flexibility to design new robotic simulation environments. 

Other benchmarks for robotic tasks include Meta-World [243] which contains 50 distinct robotic manipulation tasks for meta-RL and multi-task learning, RLBench [244] which contains 100 unique, hand-designed tasks, covering everything from simple goal-reaching and door opening to more complex multi-stage tasks. 

Due to the choice of different tasks and interaction constraints in different works, the results of robotic research works are difficult to align. DreamingV2 [205] evaluates a relatively complete set of these works, which covers discrete/continuous latent space and with/without image reconstruction. We refer to their evaluation results in this survey, which are presented in Table 6. The experiment analyzes the impact of two factors, the discreteness or continuity of the latent space and the presence or absence of image reconstruction, on the learning effectiveness of the agent. 

## **5 DISCUSSION** 

Despite the recent surge in research on general world models [201], [213] and specific applications in areas like autonomous driving [28], [29], [32], [175], [180], [184], [187], [188], [192] and robotics [33], [34], [35], [202], numerous challenges and opportunities await further exploration. In this section, we delve into the intricate challenges faced by general world models and their current technical constraint, alongside envisioning potential future directions for their development. Additionally, we explore the unique challenges and promising avenues in the fields of autonomous driving and autonomous agents. Furthermore, we reflect on the ethical and safety considerations arising from the deployment of these models. 

### **5.1 General World Models** 

General world models aim to represent and simulate a wide range of situations and interactions, like those encountered in the real world. Recent advancements in generative models have greatly improved video generation quality. Notably, Sora can create high-definition videos up to one minute in length, closely mimicking the physical world, showing great potential for general world models. However, it’s crucial to address existing issues and challenges for future progress. 

### _5.1.1 Challenges_ 

Video generation is not synonymous with world models. While video generation may serve as one manifestation of world models, it does not fully address the core challenges inherent to world models. We will discuss several challenges that we deem important for world models in the following. **Causal Reasoning.** As a predictive model, the essence of world modeling lies in its capacity for reasoning. The model should be capable of inferring outcomes of decisions never encountered before, rather than solely making predictions within known data distributions. As discussed in [245] and illustrated in Figure 7, we expect world models to possess the ability of counterfactual reasoning, whereby outcomes are inferred through rational imagining. This ability is inherently human but remains a challenging task for current AI systems. For example, imagine an autonomous vehicle facing a sudden traffic accident or a robot in a new environment. A world model with counterfactual reasoning can simulate different actions they could take, predict outcomes, and choose the safest response—even in new situations. This would significantly improve autonomous systems’ decisionmaking, helping them handle new and complex scenarios. **Physical Laws.** Although Sora’s video generation is impressive, it’s argued to fall short as a world model because it doesn’t fully comply with physical laws. Realism, seen in Sora’s videos, isn’t the same as reality, which demands strict obedience to physical laws like gravity, light interaction, and fluid dynamics. While Sora has improved in modeling movement, including pedestrians and rigid body movements [23], it still struggles with accurately simulating fluids and complex physical phenomena. Training Sora with just video-text pairs isn’t enough to grasp these complexities. Understanding physical laws often requires specific observations, suggesting that combining Sora with physics-driven simulators could be beneficial. Although these simulators 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

19 


Fig. 7. The three level hierarchy of intelligence [245]. World models are expected to conduct counterfactual reasoning. 

might not achieve Sora’s level of realism, they correctly follow physical properties. 

**Generalization.** Generalization capability is a crucial aspect of world models, emphasizing not only data interpolation but, more importantly, data extrapolation. For instance, in autonomous driving, real-life accidents or abnormal driving behaviors are rare occurrences. Therefore, can the learned world model imagine these rare driving events? This requires the model to move beyond simply memorizing the training data and instead develop a robust understanding of the underlying principles governing driving dynamics and road scenarios. By extrapolating from known data and simulating a wide range of potential situations, the world model can better prepare autonomous vehicles to navigate safely in the real world, even in unfamiliar or unexpected circumstances. **Computational Efficiency.** Efficiency in video generation is currently a significant limitation. To maintain consistency in video generation, autoregressive methods are often employed, leading to a considerable increase in generation time. Based on the news and anaylysis in the internet, Sora may take over about one hour to generate a video with one minute length. Although a series of distillation-based methods [114], [246] have emerged in image generation, yielding significant acceleration in performance, research in the field of video generation remains limited. 

**Evaluation System.** Current world models are predominantly based on generative model research, with evaluation metrics primarily focusing on the quality of generation, such as FID [247] and FVD [147]. Additionally, there are some works proposing more comprehensive evaluation benchmarks, such as CLIPScore [248], T2VScore [249], VBench [150], EvalCrafter [148], PEEKABOO [250], and others. However, generation metrics alone cannot reflect the predictive rationality of world models. This highlights the need for human-centric evaluation [41], which measures whether the generated videos meet users’ expectations or align with human reasoning. By incorporating human feedback, evaluations become more comprehensive, considering realism, coherence, and relevance. This approach also offers insights into real-world utility, guiding further development and refinement for practical applications. 

### _5.1.2 Future Perspectives_ 

Despite the acclaimed success of recent world model studies, and considering some of the core challenges we discussed before, we believe that future research on world models can step further in the following directions. 

**3D World Simulator.** Video generation has advanced significantly in simulating various aspects of the world, but the world exists fundamentally in three dimensions. Therefore, future world models should possess the capability to predict and comprehend 3D spatial environments. This involves not only capturing the visual appearance of objects and scenes but also encoding their spatial relationships, depth information, and volumetric properties. Extending world models into three-dimensional space can enable more immersive and realistic simulations, facilitating applications in virtual reality [251], augmented reality, robotics, and autonomous systems. Moreover, 3D world models can enhance the ability to interpret and interact with the physical world. 

**World Models for Embodied Intelligence.** World models for embodied intelligence [252] involve creating comprehensive representations of the environment that an agent interacts with. This implies that world models can serve as simulators to train embodied agents’ decision-making processes, as demonstrated by Drive-WM’s [32] preliminary attempts in the field of autonomous driving. Moreover, integration with embodied intelligence enriches their direct interaction with the environment, significantly enhancing machines’ understanding of and adaptability to the physical world. 

### **5.2 World Models for Autonomous Driving** 

While extensive research has been conducted on world models in autonomous driving, the current state of world models remains rudimentary compared to the comprehensive mental world models possessed by a skilled human driver. Significant challenges persist in areas like action controllability, 3D consistency, and overcoming data limitations. Nevertheless, we hold firm in the belief that the foundational model for autonomous driving will be based on world models, enabling effective interaction and comprehensive understanding of the physical world. 

### _5.2.1 Challenges_ 

**Action Controllability.** In the realm of autonomous driving, the emphasis is on action-conditioned generation rather than text-conditioned video generation. While this area has garnered attention, only a handful of studies have delved into it. For instance, GAIA-1 [28] and DriveDreamer [29] focus on steering and throttle conditioning, while DriveWM [32] utilizes planning trajectories for better integration with end-to-end driving systems. However, achieving finegrained control over actions remains highly challenging. For instance, when attempting to control a vehicle to perform unconventional maneuvers such as high-speed turns or U- turns, the quality of generation noticeably deteriorates. This limitation is also influenced by the distribution of normal data. Actions, being continuous variables, pose difficulty in learning their latent space representations from limited data samples. Current methods are only capable of achieving coarse motion control, emphasizing the considerable gap that still exists towards achieving fine-grained control. 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

20 

**3D Consistency.** 3D consistency is crucial for autonomous driving. Although current video generation techniques may appear realistic, ensuring their 3D consistency is challenging, thus compromising the reliability of world model generation. However, if the world model is to be truly applied, the ability to consistently generate 3D spaces must be further improved. While the Sora team believes that scaling up can enable models to learn 3D consistency from videos, this implicit learning approach is obviously less secure for autonomous driving. Given the abundance of sensors in autonomous vehicles, world models can extend beyond mere video generation. For instance, conditioning on point clouds or occupancy grids can significantly enhance 3D consistency. **Data Limitations.** Data plays a crucial role in training foundation models. Unlike the readily available image and text data on the internet, autonomous driving encounters significant challenges in data collection, making world model construction exceedingly difficult. Firstly, autonomous driving data collection differs substantially from human learning due to fixed sensor positions. Humans learn about the world’s physics through passive observation and active interaction, while autonomous vehicles lack this flexibility. Understanding the consequences of the ego-agent’s actions on the environment is vital for reasoning about interactions. However, such data is often scarce or hard to obtain, presenting a significant challenge in world model construction. Secondly, privacy concerns and commercial competition often deter automotive companies from sharing their autonomous driving data. This not only limits the scale of available data but also restricts its diversity. Lastly, data collection typically exhibits a long-tail distribution, emphasizing the importance of rare scenarios that are nonetheless crucial for autonomous driving. Therefore, the efficient selection of such data remains a challenging and unresolved issue. While GenAD [180] has explored training world models using internet data, the effectiveness remains preliminary. Addressing these data limitation issues will facilitate research on autonomous driving world models. 

### _5.2.2 Future Perspectives_ 

**End-to-end Foundation Driving Models.** The world model is crucial for building the end-to-end foundation model for autonomous driving. As a simulator of the real world, it can not only provide high-quality data but also enable a closedloop training environment for decision-making. Although the driving domain is more restricted compared to general scenarios, it involves rich interactions and an understanding of spatial and temporal information, which are currently lacking in text-based video generation models. Currently, the world model for autonomous driving is still far from achieving this goal. The best model, GAIA-1 [28], is trained on 4,700 hours video data, akin to GPT predicting the next token. However, with a model size of 9B, it still falls far short compared to large language models. However, the shift towards big data-driven autonomous driving is undoubtedly an inevitable trend. Models will increasingly comprehend reality and grasp the rules and techniques of driving from data, rather than relying solely on manually designed rules. In this regard, Tesla’s FSD beta 12.3 has demonstrated amazing driving capabilities, offering a glimpse of hope for the future end-to-end foundation model of driving. 

**Real-world Driving Simulators.** While many end-to-end autonomous driving methods are under research in the CARLA simulator, the inherent disparities between simulated and real-world environments present significant challenges. This highlights the necessity of constructing more realistic real-world driving simulations in the future. Leveraging the robust predictive capabilities of world models, we can create even more realistic driving simulators that extend beyond mere video generation. Such simulators must also focus on aspects like scene layout control, lighting control, and object manipulation. Furthermore, world models can be seamlessly integrated with previous simulation [253] efforts based on MVS [254], [255], NeRF [256], and 3D Gaussian Splatting [257], thereby enhancing the scene generalization capabilities of existing methods. By utilizing more realistic driving simulators for model training, it can greatly facilitate the deployment of autonomous driving systems that perform reliably in practical settings [258]. 

### **5.3 World Models for Autonomous Agents** 

Autonomous agents encompass both physical robots in the real world and intelligent agents in digital environments. World models have the capability to simulate not only the intricate complexities of the physical world but also the nuances of digital environments. From the perspective of autonomous agents, world models present some new challenges and opportunities. 

### _5.3.1 Challenges_ 

**Understand the Environment Dynamics.** Agents need to understand their environments to function effectively. For physical robots, this means grappling with the complex and often uncertain dynamics of the physical world, a task made difficult by limited observations and the probabilistic nature of real-world changes. Unlike robots, humans navigate this complexity well thanks to multisensory perception, genetic knowledge, and the ability to learn from experience and share knowledge. To enhance an agent’s understanding of its environment, we can draw inspiration from human capabilities in three ways: First, by enhancing multimodal perception, allowing agents to gather more comprehensive information through integrated models that encompass vision, sound, and touch. Examples of this approach include the development of large language models like GPT-4V [98] and Gemini [259]. Second, leveraging extensive internet data for unsupervised learning can aid agents in acquiring fundamental cognitive abilities. Lastly, advancing and disseminating sophisticated knowledge through systems like LeCun’s multi-level knowledge induction [39] facilitates agents in rapidly attaining a deeper understanding of their environment. 

**Task Generalization.** Agents in real-world applications frequently encounter a range of diverse tasks, necessitating world models that can not only handle familiar tasks but also generalize effectively to novel, unseen ones. This task generalization capability is crucial for agents, yet current robots still face significant challenges in this regard. The majority of robots today are specialized models, tailored to perform specific functions such as sweeping, transporting, cooking, and the like, limiting their adaptability and versatility in handling a wider range of tasks. This implies that 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

21 

learning world models cannot solely rely on imitation and generation; rather, it is essential to abstract common sense from diverse tasks. Such common sense enables agents to migrate and comprehend different tasks more easily. Mere reliance on big data learning is an inefficient and poorly generalizable approach. This is analogous to the concept of meta-learning, where meta-learning methods train agents to learn how to learn, enabling them to quickly adapt to new tasks. Additionally, multi-task learning frameworks empower agents to train on multiple tasks simultaneously, identifying and leveraging the commonalities between them. 

### _5.3.2 Future Perspectives_ 

**Knowledge Injection through Large Language Model.** LLM has demonstrated astonishing comprehension abilities over the past two years. Through the language learning, the model has acquired a certain amount of knowledge about the world. Leveraging this accumulated knowledge, the LLM can serve as a prior for world models, enabling the model to learn different tasks more efficiently. Just like humans, world models initially envision scenarios based on their preexisting knowledge and subsequently refine their understanding through feedback obtained from the actual environment. We believe that the integration of world models with large language models represents one of the promising directions for future development. 

**Real-world Application.** While the Dreamer series of algorithms [33], [34], [35] has shown promise in learning from limited interaction through planning within simulated environments and gaming scenarios, their application in realworld robotics remains largely unexplored [202]. However, the transition from simulation to reality is an inevitable direction for future research. The real world introduces additional uncertainties, including observation errors and control precision, making it crucial to investigate the effectiveness of world models for physical robots in real-world settings. 

### **5.4 Ethical and Safety Concerns** 

The main concerns surrounding tools like Sora revolve around their safety and ethical impacts. 

**Model Accountability.** As a powerful predictive model, ensuring the reliability of world model predictions is a critical concern. Accountability measures are indispensable to validate the accuracy and fairness of model outputs, particularly considering their potential impact on decisionmaking processes. For instance, in autonomous driving, the reliability of world model predictions is essential for ensuring safety. Moreover, accountability measures should also address issues of fairness, ensuring that world models do not exhibit biases [260] that could disproportionately impact certain groups or communities. 

**Disinformation.** Hyper-realistic videos generated by visual generative AI present an alarming threat, particularly in their potential to create emotionally manipulative content that spreads misinformation, especially during critical events like elections. The proliferation of fabricated videos depicting politicians in fictitious scenarios significantly distorts public opinion. Furthermore, this misinformation seeps into education, making it harder to distinguish reality from falsehood. Tackling this issue demands collaborative action from 

governments, technology firms, media organizations, and civil society to establish a reliable information dissemination system. 

**Data Privacy.** The abundance of data undoubtedly propels the rapid development of large foundation models, but it also raises concerns about privacy protection. In a recent study [261], mainstream large language models like GPT-4, Llama-2, and Claude-2 were used to infer specific privacy datasets. It was found that these large models could automatically deduce various real privacy data hidden within the text content analyzed from users’ texts alone. Compared to textual data, the internet holds a vast amount of video data and continues to update daily, which requires even more attention to privacy concerns. Especially for large-scale models used in video generation, it is essential to disclose the sources of training videos to prevent personal privacy data from being unknowingly used for training. Additionally, corresponding laws and policies should be established to clarify the protection and requirements of personal privacy data. 

## **6 CONCLUSION** 

In this survey, we conduct a comprehensive review of general world models, underlining their pivotal importance in the pursuit of AGI and their fundamental applications across a myriad of domains, from immersive virtual environments to sophisticated decision-making systems. Through our examination, the emergence of the Sora model is highlighted for its unparalleled simulation capabilities and nascent understanding of physical principles, marking a significant milestone in the evolution of world models. We delve deeply into the current innovations, with a particular focus on the application of world models for video generation, autonomous driving, and the operation of autonomous agents. Despite the progress and promising prospects, we also critically evaluate the challenges and limitations facing current world model methodologies, contemplating their complexity, ethical considerations, and scalability. This comprehensive review not only showcases the current state and potential of world models but also illuminates the path toward their future development and application. We hope this survey can inspire the community toward novel solutions, thereby broadening the horizon for world models and their applications in shaping the future of AGI. 

## **REFERENCES** 

- [1] T. Brooks _et al._ , “Video generation models as world simulators,” 2024. [Online]. Available: https://openai.com/ research/video-generation-models-as-world-simulators 

- [2] R. Rombach _et al._ , “High-resolution image synthesis with latent diffusion models,” in _CVPR_ , 2022. 

- [3] D. Podell _et al._ , “Sdxl: Improving latent diffusion models for high-resolution image synthesis,” _arXiv preprint arXiv:2307.01952_ , 2023. 

- [4] S. Gu _et al._ , “Vector quantized diffusion model for text-to-image synthesis,” in _CVPR_ , 2022. 

- [5] M. Ding _et al._ , “Cogview: Mastering text-to-image generation via transformers,” _NeurIPS_ , 2021. 

- [6] A. Ramesh _et al._ , “Hierarchical text-conditional image generation with clip latents,” _arXiv preprint arXiv:2204.06125_ , 2022. 

- [7] A. Nichol _et al._ , “Glide: Towards photorealistic image generation and editing with text-guided diffusion models,” _arXiv preprint arXiv:2112.10741_ , 2021. 

22 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

- [8] F. Bao _et al._ , “One transformer fits all distributions in multi-modal diffusion at scale,” in _ICML_ , 2023. 

- [9] J. Yu _et al._ , “Scaling autoregressive models for content-rich text-toimage generation,” _arXiv preprint arXiv:2206.10789_ , 2022. 

- [10] M. Chen _et al._ , “Generative pretraining from pixels,” in _ICML_ , 2020. 

- [11] L. Zhang _et al._ , “Adding conditional control to text-to-image diffusion models,” 2023. 

- [12] Y. Li _et al._ , “Gligen: Open-set grounded text-to-image generation,” in _ICCV_ , 2023. 

- [13] C. Mou _et al._ , “T2i-adapter: Learning adapters to dig out more controllable ability for text-to-image diffusion models,” in _AAAI_ , 2024. 

- [14] L. Huang _et al._ , “Composer: Creative and controllable image synthesis with composable conditions,” _arXiv preprint arXiv:2302.09778_ , 2023. 

- [15] W. Yan _et al._ , “Videogpt: Video generation using vq-vae and transformers,” _arXiv preprint arXiv:2104.10157_ , 2021. 

- [16] R. Girdhar _et al._ , “Emu video: Factorizing text-to-video generation by explicit image conditioning,” _arXiv preprint arXiv:2311.10709_ , 2023. 

- [17] Y. Zeng _et al._ , “Make pixels dance: High-dynamic video generation,” _arXiv preprint arXiv:2311.10982_ , 2023. 

- [18] A. Blattmann _et al._ , “Stable video diffusion: Scaling latent video diffusion models to large datasets,” _arXiv preprint arXiv:2311.15127_ , 2023. 

- [19] J. Ho _et al._ , “Imagen video: High definition video generation with diffusion models,” _arXiv preprint arXiv:2210.02303_ , 2022. 

- [20] A. Gupta _et al._ , “Photorealistic video generation with diffusion models,” _arXiv preprint arXiv:2312.06662_ , 2023. 

- [21] A. Blattmann _et al._ , “Align your latents: High-resolution video synthesis with latent diffusion models,” in _CVPR_ , 2023. 

- [22] D. Kondratyuk _et al._ , “Videopoet: A large language model for zero-shot video generation,” _arXiv preprint arXiv:2312.14125_ , 2023. 

- [23] P. Esser _et al._ , “Structure and content-guided video synthesis with diffusion models,” in _ICCV_ , 2023. 

- [24] A. Germanidis, “Introducing general world models,” 2023. [Online]. Available: https://research.runwayml.com/ introducing-general-world-models 

- [25] A. Hu _et al._ , “Model-based imitation learning for urban driving,” _NeurIPS_ , 2022. 

- [26] M. Pan _et al._ , “Iso-dream: Isolating and leveraging noncontrollable visual dynamics in world models,” _NeurIPS_ , 2022. 

- [27] Z. Gao _et al._ , “Enhance sample efficiency and robustness of endto-end urban autonomous driving via semantic masked world model,” _arXiv preprint arXiv:2210.04017_ , 2022. 

- [28] A. Hu _et al._ , “Gaia-1: A generative world model for autonomous driving,” _arXiv preprint arXiv:2309.17080_ , 2023. 

- [29] X. Wang _et al._ , “Drivedreamer: Towards real-world-driven world models for autonomous driving,” _arXiv preprint arXiv:2309.09777_ , 2023. 

- [30] Y. Wen _et al._ , “Panacea: Panoramic and controllable video generation for autonomous driving,” _arXiv preprint arXiv:2311.16813_ , 2023. 

- [31] G. Zhao _et al._ , “Drivedreamer-2: Llm-enhanced world models for diverse driving video generation,” _arXiv preprint arXiv:2403.06845_ , 2024. 

- [32] Y. Wang _et al._ , “Driving into the future: Multiview visual forecasting and planning with world model for autonomous driving,” _arXiv preprint arXiv:2311.17918_ , 2023. 

- [33] D. Hafner _et al._ , “Dream to control: Learning behaviors by latent imagination,” in _ICLR_ , 2020. 

- [34] ——, “Mastering atari with discrete world models,” in _ICLR_ , 2021. [35] ——, “Mastering diverse domains through world models,” 2023. [36] Y. Du _et al._ , “Learning universal policies via text-guided video generation,” _NeurIPS_ , 2024. 

- [37] S. Yang _et al._ , “Learning interactive real-world simulators,” in _ICLR_ , 2024. 

- [38] S. Zhou _et al._ , “Robodreamer: Learning compositional world models for robot imagination,” 2024. 

- [39] Y. LeCun _et al._ , “A path towards autonomous machine intelligence version 0.9.2, 2022-06-27,” 2022. [Online]. Available: https://api.semanticscholar.org/CorpusID:251881108 

- [40] Y. Guan _et al._ , “World models for autonomous driving: An initial survey,” _arXiv preprint arXiv:2403.02622_ , 2024. 

- [41] J. Cho _et al._ , “Sora as an agi world model? a complete survey on text-to-video generation,” _arXiv preprint arXiv:2403.05131_ , 2024. 

- [42] Y. Liu _et al._ , “Sora: A review on background, technology, limitations, and opportunities of large vision models,” _arXiv preprint arXiv:2402.17177_ , 2024. 

- [43] R. Sun _et al._ , “From sora what we can see: A survey of text-to-video generation.” 

- [44] J. Deng _et al._ , “Imagenet: A large-scale hierarchical image database,” in _CVPR_ , 2009. 

- [45] Y. LeCun _et al._ , “Gradient-based learning applied to document recognition,” _Proceedings of the IEEE_ , 1998. 

- [46] A. Krizhevsky _et al._ , “Imagenet classification with deep convolutional neural networks,” _NeurIPS_ , vol. 25, 2012. 

- [47] K. Simonyan _et al._ , “Very deep convolutional networks for largescale image recognition,” _arXiv preprint arXiv:1409.1556_ , 2014. 

- [48] C. Szegedy _et al._ , “Going deeper with convolutions,” in _CVPR_ , 2015. 

- [49] K. He _et al._ , “Deep residual learning for image recognition,” in _CVPR_ , 2016. 

- [50] G. Huang _et al._ , “Densely connected convolutional networks,” in _CVPR_ , 2017. 

- [51] S. Ren _et al._ , “Faster r-cnn: Towards real-time object detection with region proposal networks,” _NeurIPS_ , 2015. 

- [52] K. He _et al._ , “Mask r-cnn,” in _ICCV_ , 2017. [53] O. Ronneberger _et al._ , “U-net: Convolutional networks for biomedical image segmentation,” in _MICCAI_ , 2015. 

- [54] J. Ho _et al._ , “Denoising diffusion probabilistic models,” _NeurIPS_ , 2020. 

- [55] P. Dhariwal _et al._ , “Diffusion models beat gans on image synthesis,” _NeurIPS_ , 2021. 

- [56] A. Vaswani _et al._ , “Attention is all you need,” _NeurIPS_ , 2017. [57] A. Dosovitskiy _et al._ , “An image is worth 16x16 words: Transformers for image recognition at scale,” _arXiv preprint arXiv:2010.11929_ , 2020. 

- [58] H. Touvron _et al._ , “Training data-efficient image transformers & distillation through attention,” in _ICML_ , 2021. 

- [59] Z. Liu _et al._ , “Swin transformer: Hierarchical vision transformer using shifted windows,” in _ICCV_ , 2021. 

- [60] H. Bao _et al._ , “Beit: Bert pre-training of image transformers,” _arXiv preprint arXiv:2106.08254_ , 2021. 

- [61] K. He _et al._ , “Masked autoencoders are scalable vision learners,” in _CVPR_ , 2022. 

- [62] N. Carion _et al._ , “End-to-end object detection with transformers,” in _ECCV_ , 2020. 

- [63] X. Zhu _et al._ , “Deformable detr: Deformable transformers for end-to-end object detection,” _arXiv preprint arXiv:2010.04159_ , 2020. 

- [64] Z. Yao _et al._ , “Efficient detr: improving end-to-end object detector with dense prior,” _arXiv preprint arXiv:2104.01318_ , 2021. 

- [65] H. Zhang _et al._ , “Dino: Detr with improved denoising anchor boxes for end-to-end object detection,” _arXiv preprint arXiv:2203.03605_ , 2022. 

- [66] E. Xie _et al._ , “Segformer: Simple and efficient design for semantic segmentation with transformers,” _NeurIPS_ , 2021. 

- [67] R. Strudel _et al._ , “Segmenter: Transformer for semantic segmentation,” in _ICCV_ , 2021. 

- [68] S. Zheng _et al._ , “Rethinking semantic segmentation from a sequence-to-sequence perspective with transformers,” in _CVPR_ , 2021. 

- [69] W. Peebles _et al._ , “Scalable diffusion models with transformers,” in _ICCV_ , 2023. 

- [70] F. Bao _et al._ , “All are worth words: A vit backbone for diffusion models,” in _CVPR_ , 2023. 

- [71] A. Hatamizadeh _et al._ , “Diffit: Diffusion vision transformers for image generation,” _arXiv preprint arXiv:2312.02139_ , 2023. 

- [72] S. Ji _et al._ , “3d convolutional neural networks for human action recognition,” _TPAMI_ , 2012. 

- [73] D. Tran _et al._ , “Learning spatiotemporal features with 3d convolutional networks,” in _ICCV_ , 2015. 

- [74] J. Carreira _et al._ , “Quo vadis, action recognition? a new model and the kinetics dataset,” in _CVPR_ , 2017. 

- [75] D. Tran _et al._ , “Convnet architecture search for spatiotemporal feature learning,” _arXiv preprint arXiv:1708.05038_ , 2017. 

- [76] C. Feichtenhofer _et al._ , “Slowfast networks for video recognition,” in _ICCV_ , 2019. 

- [77] C. Feichtenhofer, “X3d: Expanding architectures for efficient video recognition,” in _CVPR_ , 2020. 

- [78] C. Yang _et al._ , “Temporal pyramid network for action recognition,” in _CVPR_ , 2020. 

- [79] A. Arnab _et al._ , “Vivit: A video vision transformer,” in _ICCV_ , 2021. 

23 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

- [80] G. Bertasius _et al._ , “Is space-time attention all you need for video understanding?” in _ICML_ , 2021. 

- [81] K. Li _et al._ , “Uniformer: Unified transformer for efficient spatiotemporal representation learning,” _arXiv preprint arXiv:2201.04676_ , 2022. 

- [82] Z. Liu _et al._ , “Video swin transformer,” in _CVPR_ , 2022. [83] L. Yu _et al._ , “Magvit: Masked generative video transformer,” in _CVPR_ , 2023. 

- [84] ——, “Language model beats diffusion–tokenizer is key to visual generation,” _arXiv preprint arXiv:2310.05737_ , 2023. 

- [85] J. Li _et al._ , “Align before fuse: Vision and language representation learning with momentum distillation,” _NeurIPS_ , 2021. 

- [86] A. Radford _et al._ , “Learning transferable visual models from natural language supervision,” in _ICML_ , 2021. 

- [87] J. Li _et al._ , “Blip: Bootstrapping language-image pre-training for unified vision-language understanding and generation,” in _ICML_ , 2022. 

- [88] A. Jaiswal _et al._ , “A survey on contrastive self-supervised learning,” _Technologies_ , 2020. 

- [89] J. Devlin _et al._ , “Bert: Pre-training of deep bidirectional transformers for language understanding,” _arXiv preprint arXiv:1810.04805_ , 2018. 

- [90] Y. Liu _et al._ , “Roberta: A robustly optimized bert pretraining approach,” _arXiv preprint arXiv:1907.11692_ , 2019. 

- [91] M. Lewis _et al._ , “Bart: Denoising sequence-to-sequence pretraining for natural language generation, translation, and comprehension,” _arXiv preprint arXiv:1910.13461_ , 2019. 

- [92] A. Radford _et al._ , “Improving language understanding by generative pre-training,” 2018. 

- [93] ——, “Language models are unsupervised multitask learners,” _OpenAI blog_ , 2019. 

- [94] T. Brown _et al._ , “Language models are few-shot learners,” _NeurIPS_ , 2020. 

- [95] C. Raffel _et al._ , “Exploring the limits of transfer learning with a unified text-to-text transformer,” _JMLR_ , 2020. 

- [96] H. Touvron _et al._ , “Llama: Open and efficient foundation language models,” _arXiv preprint arXiv:2302.13971_ , 2023. 

- [97] ——, “Llama 2: Open foundation and fine-tuned chat models,” _arXiv preprint arXiv:2307.09288_ , 2023. 

- [98] J. Achiam _et al._ , “Gpt-4 technical report,” _arXiv preprint arXiv:2303.08774_ , 2023. 

- [99] X. Hu _et al._ , “Ella: Equip diffusion models with llm for enhanced semantic alignment,” _arXiv preprint arXiv:2403.05135_ , 2024. 

- [100] J. Chen _et al._ , “Pixart-alpha: Fast training of diffusion transformer for photorealistic text-to-image synthesis,” _arXiv preprint arXiv:2310.00426_ , 2023. 

- [101] C. Saharia _et al._ , “Photorealistic text-to-image diffusion models with deep language understanding,” _NeurIPS_ , 2022. 

- [102] W. Wu _et al._ , “Paragraph-to-image generation with informationenriched diffusion model,” _arXiv preprint arXiv:2311.14284_ , 2023. 

- [103] I. Goodfellow _et al._ , “Generative adversarial nets,” _NeurIPS_ , 2014. [104] J.-Y. Zhu _et al._ , “Unpaired image-to-image translation using cycleconsistent adversarial networks,” in _ICCV_ , 2017. 

- [105] T. Karras _et al._ , “A style-based generator architecture for generative adversarial networks,” in _CVPR_ , 2019. 

- [106] O. Patashnik _et al._ , “Styleclip: Text-driven manipulation of stylegan imagery,” in _ICCV_ , 2021. 

- [107] A. Brock _et al._ , “Large scale gan training for high fidelity natural image synthesis,” _arXiv preprint arXiv:1809.11096_ , 2018. 

- [108] J. Zhu _et al._ , “In-domain gan inversion for real image editing,” in _ECCV_ , 2020. 

- [109] T. Wang _et al._ , “High-fidelity gan inversion for image attribute editing,” in _CVPR_ , 2022. 

- [110] G. Perarnau _et al._ , “Invertible conditional gans for image editing,” _arXiv preprint arXiv:1611.06355_ , 2016. 

- [111] H. Liu _et al._ , “Pd-gan: Probabilistic diverse gan for image inpainting,” in _CVPR_ , 2021. 

- [112] U. Demir _et al._ , “Patch-based image inpainting with generative adversarial networks,” _arXiv preprint arXiv:1803.07422_ , 2018. 

- [113] J. Song _et al._ , “Denoising diffusion implicit models,” _arXiv preprint arXiv:2010.02502_ , 2020. 

- [114] S. Luo _et al._ , “Latent consistency models: Synthesizing highresolution images with few-step inference,” _arXiv preprint arXiv:2310.04378_ , 2023. 

- [115] T. Salimans _et al._ , “Progressive distillation for fast sampling of diffusion models,” _arXiv preprint arXiv:2202.00512_ , 2022. 

- [116] H. Zheng _et al._ , “Fast sampling of diffusion models via operator learning,” in _ICML_ , 2023. 

- [117] Y. Song _et al._ , “Consistency models,” _arXiv preprint arXiv:2303.01469_ , 2023. 

- [118] Z. Pan _et al._ , “T-stitch: Accelerating sampling in pre-trained diffusion models with trajectory stitching,” _arXiv preprint arXiv:2402.14167_ , 2024. 

- [119] Y. Shang _et al._ , “Post-training quantization on diffusion models,” in _CVPR_ , 2023. 

- [120] G. Fang _et al._ , “Structural pruning for diffusion models,” _NeurIPS_ , 2024. 

- [121] X. Ma _et al._ , “Deepcache: Accelerating diffusion models for free,” _arXiv preprint arXiv:2312.00858_ , 2023. 

- [122] Y. Yu _et al._ , “Diverse image inpainting with bidirectional and autoregressive transformers,” in _ACM ICM_ , 2021. 

- [123] J. Yu _et al._ , “Scaling autoregressive models for content-rich text-toimage generation,” _arXiv preprint arXiv:2206.10789_ , 2022. 

- [124] D. Lee _et al._ , “Autoregressive image generation using residual quantization,” in _CVPR_ , 2022. 

- [125] Y. Bai _et al._ , “Sequential modeling enables scalable learning for large vision models,” _arXiv preprint arXiv:2312.00785_ , 2023. 

- [126] X. Jiao _et al._ , “Tinybert: Distilling bert for natural language understanding,” _arXiv preprint arXiv:1909.10351_ , 2019. 

- [127] H. Chang _et al._ , “Maskgit: Masked generative image transformer,” in _CVPR_ , 2022. 

- [128] T. Li _et al._ , “Mage: Masked generative encoder to unify representation learning and image synthesis,” in _CVPR_ , 2023. 

- [129] ——, “Self-conditioned image generation via generating representations,” _arXiv preprint arXiv:2312.03701_ , 2023. 

- [130] Y. Pan _et al._ , “To create what you tell: Generating videos from captions,” in _ACM ICM_ , 2017. 

- [131] Y. Balaji _et al._ , “Conditional gan with discriminative filter generation for text-to-video synthesis.” in _IJCAI_ , 2019. 

- [132] B. Li, “Word-level fine-grained story visualization,” in _ECCV_ , 2022. 

- [133] Y. Li _et al._ , “Video generation from text,” in _AAAI_ , 2018. 

- [134] ——, “Storygan: A sequential conditional gan for story visualization,” in _CVPR_ , 2019. 

- [135] D. Kim _et al._ , “Tivgan: Text to image to video generation with step-by-step evolutionary generator,” _IEEE Access_ , 2020. 

- [136] K. Deng _et al._ , “Irc-gan: Introspective recurrent convolutional gan for text-to-video generation.” in _IJCAI_ , 2019. 

- [137] S. Hochreiter _et al._ , “Long short-term memory,” _Neural computation_ , 1997. 

- [138] J. Ho _et al._ , “Video diffusion models,” _NeurIPS_ , 2022. 

- [139] X. Ma _et al._ , “Latte: Latent diffusion transformer for video generation,” _arXiv preprint arXiv:2401.03048_ , 2024. 

- [140] R. Henschel _et al._ , “Streamingt2v: Consistent, dynamic, and extendable long video generation from text,” _arXiv preprint arXiv:2403.14773_ , 2024. 

- [141] C. Wu _et al._ , “Godiva: Generating open-domain videos from natural descriptions,” _arXiv preprint arXiv:2104.14806_ , 2021. 

- [142] W. Hong _et al._ , “Cogvideo: Large-scale pretraining for text-to-video generation via transformers,” _arXiv preprint arXiv:2205.15868_ , 2022. 

- [143] A. Maharana _et al._ , “Storydall-e: Adapting pretrained text-toimage transformers for story continuation,” in _ECCV_ , 2022. 

- [144] A. Van Den Oord _et al._ , “Neural discrete representation learning,” _NeurIPS_ , 2017. 

- [145] M. Ding _et al._ , “Cogview2: Faster and better text-to-image generation via hierarchical transformers,” _NeurIPS_ , 2022. 

- [146] X. Wang _et al._ , “Worlddreamer: Towards general world models for video generation via predicting masked tokens,” 2024. 

- [147] T. Unterthiner _et al._ , “Towards accurate generative models of video: A new metric & challenges,” _arXiv preprint arXiv:1812.01717_ , 2018. 

- [148] Y. Liu _et al._ , “Evalcrafter: Benchmarking and evaluating large video generation models,” _arXiv preprint arXiv:2310.11440_ , 2023. 

- [149] ——, “Fetv: A benchmark for fine-grained evaluation of opendomain text-to-video generation,” _NeurIPS_ , 2024. 

- [150] Z. Huang _et al._ , “Vbench: Comprehensive benchmark suite for video generative models,” _arXiv preprint arXiv:2311.17982_ , 2023. 

- [151] D. P. Kingma _et al._ , “Auto-encoding variational bayes,” _arXiv preprint arXiv:1312.6114_ , 2013. 

- [152] E. Perez _et al._ , “Film: Visual reasoning with a general conditioning layer,” in _AAAI_ , 2018. 

- [153] J. Betker _et al._ , “Improving image generation with better captions,” _Computer Science_ , 2023. 

24 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

- [154] H. Xu _et al._ , “mplug-2: A modularized multi-modal foundation model across text, image and video,” in _ICML_ , 2023. 

- [155] Y. Wang _et al._ , “Internvideo2: Scaling video foundation models for multimodal video understanding,” _arXiv preprint arXiv:2403.15377_ , 2024. 

- [156] T.-S. Chen _et al._ , “Panda-70m: Captioning 70m videos with multiple cross-modality teachers,” _arXiv preprint arXiv:2402.19479_ , 2024. 

- [157] D. Chen _et al._ , “Collecting highly parallel data for paraphrase evaluation,” in _ACL_ , 2011. 

- [158] A. Rohrbach _et al._ , “A dataset for movie description,” in _CVPR_ , 2015. 

- [159] J. Xu _et al._ , “Msr-vtt: A large video description dataset for bridging video and language,” in _CVPR_ , 2016. 

- [160] L. Anne Hendricks _et al._ , “Localizing moments in video with natural language,” in _ICCV_ , 2017. 

- [161] F. Caba Heilbron _et al._ , “Activitynet: A large-scale video benchmark for human activity understanding,” in _CVPR_ , 2015. 

- [162] L. Zhou _et al._ , “Towards automatic learning of procedures from web instructional videos,” in _AAAI_ , 2018. 

- [163] X. Wang _et al._ , “Vatex: A large-scale, high-quality multilingual dataset for video-and-language research,” in _ICCV_ , 2019. 

- [164] A. Miech _et al._ , “Howto100m: Learning a text-video embedding by watching hundred million narrated video clips,” in _ICCV_ , 2019. 

- [165] S. Lee _et al._ , “Acav100m: Automatic curation of large-scale datasets for audio-visual video representation learning,” in _ICCV_ , 2021. 

- [166] R. Zellers _et al._ , “Merlot: Multimodal neural script knowledge models,” _NeurIPS_ , 2021. 

- [167] H. Xue _et al._ , “Advancing high-resolution video-language representation with large-scale video transcriptions,” in _CVPR_ , 2022. 

- [168] M. Bain _et al._ , “Frozen in time: A joint video and image encoder for end-to-end retrieval,” in _ICCV_ , 2021. 

- [169] Y. Wang _et al._ , “Lavie: High-quality video generation with cascaded latent diffusion models,” _arXiv preprint arXiv:2309.15103_ , 2023. 

- [170] ——, “Internvid: A large-scale video-text dataset for multimodal understanding and generation,” _arXiv preprint arXiv:2307.06942_ , 2023. 

- [171] A. Hu, “Neural world models for computer vision,” Ph.D. dissertation, University of Cambridge, 2022. 

- [172] C. R. Fox _et al._ , “Distinguishing two dimensions of uncertainty,” _SSRN Electronic Journal_ , 2011. 

- [173] Z. Zhang _et al._ , “Trafficbots: Towards world models for autonomous driving simulation and motion prediction,” in _ICRA_ , 2023. 

- [174] W. M. of Tesla, “[online],” http://https://www.https://www. youtube.com/watch?v=svgGsnBkl <u>o.</u> 

- [175] L. Zhang _et al._ , “Copilot4d: Learning unsupervised world models for autonomous driving via discrete diffusion,” in _ICLR_ , 2024. 

- [176] D. Hafner _et al._ , “Learning latent dynamics for planning from pixels,” in _ICML_ , 2019. 

- [177] K. Sohn _et al._ , “Learning structured output representation using deep conditional generative models,” _NeurIPS_ , 2015. 

- [178] Q. Li _et al._ , “Think2drive: Efficient reinforcement learning by thinking in latent world model for quasi-realistic autonomous driving (in carla-v2),” _arXiv preprint arXiv:2402.16720_ , 2024. 

- [179] A. Dosovitskiy _et al._ , “Carla: An open urban driving simulator,” in _CoRL_ , 2017. 

- [180] J. Yang _et al._ , “Generalized predictive model for autonomous driving,” _arXiv preprint arXiv:2403.09630_ , 2024. 

- [181] B. Huang _et al._ , “Subjectdrive: Scaling generative data in autonomous driving via subject control,” _arXiv preprint arXiv:2403.19438_ , 2024. 

- [182] D. Bogdoll _et al._ , “Muvo: A multimodal generative world model for autonomous driving with geometric representations,” _arXiv preprint arXiv:2311.11762_ , 2023. 

- [183] Z. Yang _et al._ , “Visual point cloud forecasting enables scalable autonomous driving,” in _CVPR_ , 2024. 

- [184] C. Min _et al._ , “Driveworld: 4d pre-trained scene understanding via world models for autonomous driving,” in _CVPR_ , 2024. 

- [185] H. Caesar _et al._ , “nuscenes: A multimodal dataset for autonomous driving,” in _CVPR_ , 2020. 

- [186] X. Li _et al._ , “Drivingdiffusion: Layout-guided multi-view driving scene video generation with latent diffusion model,” _arXiv preprint arXiv:2310.07771_ , 2023. 

- [187] F. Jia _et al._ , “Adriver-i: A general world model for autonomous driving,” _arXiv preprint arXiv:2311.13549_ , 2023. 

- [188] J. Lu _et al._ , “Wovogen: World volume-aware diffusion for controllable multi-camera driving scene generation,” _arXiv preprint arXiv:2312.02934_ , 2023. 

- [189] C. Min _et al._ , “Uniworld: Autonomous driving pre-training via world models,” _arXiv preprint arXiv:2308.07234_ , 2023. 

- [190] A. Geiger _et al._ , “Are we ready for autonomous driving? the kitti vision benchmark suite,” in _CVPR_ , 2012. 

- [191] B. Wilson _et al._ , “Argoverse 2: Next generation datasets for self-driving perception and forecasting,” _arXiv preprint arXiv:2301.00493_ , 2023. 

- [192] W. Zheng _et al._ , “Occworld: Learning a 3d occupancy world model for autonomous driving,” _arXiv preprint arXiv:2311.16038_ , 2023. 

- [193] V. Zyrianov _et al._ , “Lidardm: Generative lidar simulation in a generated world,” _arXiv preprint arXiv:2404.02903_ , 2024. 

- [194] Y. Liao _et al._ , “Kitti-360: A novel dataset and benchmarks for urban scene understanding in 2d and 3d,” _TPAMI_ , 2022. 

- [195] P. Sun _et al._ , “Scalability in perception for autonomous driving: Waymo open dataset,” in _CVPR_ , 2020. 

- [196] O. Contributors, “Openscene: The largest up-to-date 3d occupancy prediction benchmark in autonomous driving,” https://github. com/OpenDriveLab/OpenScene, 2023. 

- [197] Z. Wang _et al._ , “Sts: Surround-view temporal stereo for multi-view 3d detection,” _arXiv preprint arXiv:2208.10145_ , 2022. 

- [198] C. Min _et al._ , “Multi-camera unified pre-training via 3d scene reconstruction,” _RAL_ , 2024. 

- [199] ——, “Occupancy-mae: Self-supervised pre-training large-scale lidar point clouds with masked occupancy autoencoders,” _IEEE Transactions on Intelligent Vehicles_ , 2023. 

- [200] S. Franklin _et al._ , “Is it an agent, or just a program?: A taxonomy for autonomous agents,” in _Intelligent Agents III Agent Theories, Architectures, and Languages_ , 1997. 

- [201] D. Ha _et al._ , “Recurrent world models facilitate policy evolution,” in _NeurIPS_ , 2018. 

- [202] P. Wu _et al._ , “Daydreamer: World models for physical robot learning,” in _CoRL_ , 2023. 

- [203] R. Sakagami _et al._ , “Robotic world models—conceptualization, review, and engineering best practices,” _Frontiers in Robotics and AI_ , 2023. 

- [204] F. Deng _et al._ , “Dreamerpro: Reconstruction-free model-based reinforcement learning with prototypical representations,” in _ICML_ , 2022. 

- [205] M. Okada _et al._ , “Dreamingv2: Reinforcement learning with discrete world models without reconstruction,” in _IROS_ , 2022. 

- [206] M. Assran _et al._ , “Self-supervised learning from images with a joint-embedding predictive architecture,” in _CVPR_ , 2023. 

- [207] Z. Fei _et al._ , “A-jepa: Joint-embedding predictive architecture can listen,” 2024. 

- [208] A. Bardes _et al._ , “Mc-jepa: A joint-embedding predictive architecture for self-supervised learning of motion and content features,” 2023. 

- [209] ——, “Revisiting feature prediction for learning visual representations from video,” 2024. 

- [210] C. Chen _et al._ , “Transdreamer: Reinforcement learning with transformer world models,” 2022. 

- [211] W. Zhang _et al._ , “Storm: Efficient stochastic transformer based world models for reinforcement learning,” in _NeurIPS_ , 2023. 

- [212] J. Robine _et al._ , “Transformer-based world models are happy with 100k interactions,” in _ICLR_ , 2023. 

- [213] J. Bruce _et al._ , “Genie: Generative interactive environments,” 2024. [214] A. Banino _et al._ , “MEMO: A deep network for flexible combination of episodic memories,” in _ICLR_ , 2020. 

- [215] V. Micheli _et al._ , “Transformers are sample-efficient world models,” in _ICLR_ , 2023. 

- [216] M. Xu _et al._ , “Spatial-temporal transformer networks for traffic flow forecasting,” 2021. 

- [217] M. G. Bellemare _et al._ , “The arcade learning environment: An evaluation platform for general agents,” _J. Artif. Int. Res._ , 2013. 

- [218] J. Schulman _et al._ , “Proximal policy optimization algorithms,” 2017. 

- [219] M. Hessel _et al._ , “Rainbow: combining improvements in deep reinforcement learning,” in _AAAI_ , 2018. 

- [220] L. Espeholt _et al._ , “IMPALA: Scalable distributed deep-RL with importance weighted actor-learner architectures,” in _ICML_ , 2018. 

- [221] M. Laskin _et al._ , “CURL: Contrastive unsupervised representations for reinforcement learning,” in _ICML_ , 2020. 

- [222] S. Chiappa _et al._ , “Recurrent environment simulators,” in _ICLR_ , 2017. 

25 

IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE, VOL. XX, NO. XX, XXX 2025 

- [223] L. Kaiser _et al._ , “Model based reinforcement learning for atari,” in _ICLR_ , 2020. 

- [224] V. Mnih _et al._ , “Human-level control through deep reinforcement learning,” _Nature_ , 2015. 

- [225] Z. Dai _et al._ , “Transformer-XL: Attentive language models beyond a fixed-length context,” in _ACL_ , 2019. 

- [226] M. P. Deisenroth _et al._ , “Pilco: a model-based and data-efficient approach to policy search,” in _ICML_ , 2011. 

- [227] Y. Gal _et al._ , “Improving PILCO with Bayesian neural network dynamics models,” in _Data-Efficient Machine Learning workshop, ICML_ , 2016. 

- [228] M. Henaff _et al._ , “Model-based planning with discrete and continuous actions,” 2018. 

- [229] Y. Tassa _et al._ , “Deepmind control suite,” 2018. 

- [230] W. Huang _et al._ , “Safedreamer: Safe reinforcement learning with world models,” in _ICLR_ , 2024. 

- [231] J. Ji _et al._ , “Safety gymnasium: A unified safe reinforcement learning benchmark,” in _NeurIPS_ , 2023. 

- [232] M. Okada _et al._ , “Dreaming: Model-based reinforcement learning by latent imagination without reconstruction,” in _ICRA_ , 2021. 

- [233] J. Ha _et al._ , “Dream to generalize: Zero-shot model-based reinforcement learning for unseen visual distractions,” _AAAI_ , 2023. 

- [234] A. Piergiovanni _et al._ , “Learning real-world robot policies by dreaming,” in _IROS_ , 2019. 

- [235] J. Y. Koh _et al._ , “Pathdreamer: A world model for indoor navigation,” in _ICCV_ , 2021. 

- [236] R. Sekar _et al._ , “Planning to explore via self-supervised world models,” in _ICML_ , 2020. 

- [237] R. Mendonca _et al._ , “Structured World Models from Human Videos,” in _RSS_ , 2023. 

- [238] R. Rubinstein, “The Cross-Entropy method for combinatorial and continuous optimization,” _Methodology And Computing In Applied Probability_ , 1999. 

- [239] H. Ma _et al._ , “Harmonydream: Task harmonization inside world models,” 2024. 

- [240] Y. Zhu _et al._ , “robosuite: A modular simulation framework and benchmark for robot learning,” 2022. 

- [241] E. Todorov _et al._ , “Mujoco: A physics engine for model-based control,” in _ICIRS_ , 2012. 

- [242] J. Grigsby _et al._ , “Measuring visual generalization in continuous control from pixels,” 2020. 

- [243] T. Yu _et al._ , “Meta-world: A benchmark and evaluation for multitask and meta reinforcement learning,” in _CoRL_ , 2020. 

- [244] S. James _et al._ , “Rlbench: The robot learning benchmark & learning environment,” _RAL_ , 2020. 

- [245] J. Pearl _et al._ , _The book of why: the new science of cause and effect_ . Basic books, 2018. 

- [246] J. Chen _et al._ , “Pixart- _{\_ delta _}_ : Fast and controllable image generation with latent consistency models,” _arXiv preprint arXiv:2401.05252_ , 2024. 

- [247] M. Heusel _et al._ , “Gans trained by a two time-scale update rule converge to a local nash equilibrium,” _NeurIPS_ , 2017. 

- [248] J. Hessel _et al._ , “Clipscore: A reference-free evaluation metric for image captioning,” _arXiv preprint arXiv:2104.08718_ , 2021. 

- [249] J. Z. Wu _et al._ , “Towards a better metric for text-to-video generation,” _arXiv preprint arXiv:2401.07781_ , 2024. 

- [250] Y. Jain _et al._ , “Peekaboo: Interactive video generation via maskeddiffusion,” _arXiv preprint arXiv:2312.07509_ , 2023. 

- [251] L.-H. Lee _et al._ , “All one needs to know about metaverse: A complete survey on technological singularity, virtual ecosystem, and research agenda,” _arXiv preprint arXiv:2110.05352_ , 2021. 

- [252] S. H. Vemprala _et al._ , “Chatgpt for robotics: Design principles and model abilities,” _IEEE Access_ , 2024. 

- [253] Z. Yang _et al._ , “Unisim: A neural closed-loop sensor simulator,” in _CVPR_ , 2023. 

- [254] Z. Wei _et al._ , “Aa-rmvsnet: Adaptive aggregation recurrent multiview stereo network,” in _ICCV_ , 2021, pp. 6187–6196. 

- [255] ——, “Bidirectional hybrid lstm based recurrent neural network for multi-view stereo,” _TVCG_ , 2022. 

- [256] B. Mildenhall _et al._ , “Nerf: Representing scenes as neural radiance fields for view synthesis,” _Communications of the ACM_ , 2021. 

- [257] B. Kerbl _et al._ , “3d gaussian splatting for real-time radiance field rendering,” _ToG_ , 2023. 

- [258] Q. Zhu _et al._ , “Deep learning for multi-view stereo via plane sweep: A survey,” _arXiv preprint arXiv:2106.15328_ , 2021. 

- [259] G. Team _et al._ , “Gemini: a family of highly capable multimodal models,” _arXiv preprint arXiv:2312.11805_ , 2023. 

- [260] M. Zhou _et al._ , “Bias in generative ai,” _arXiv preprint arXiv:2403.02726_ , 2024. 

- [261] R. Staab _et al._ , “Beyond memorization: Violating privacy via inference with large language models,” _arXiv preprint arXiv:2310.07298_ , 2023. 

