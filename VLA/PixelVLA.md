---
title: "PixelVLA: Advancing Pixel-level Understanding in Vision-Language-Action Model"
date: "2025-11-03"
authors: "Wenqi Liang; Gan Sun; Yao He; Jiahua Dong; Suyan Dai; Ivan Laptev"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2511.01571
pdf: https://arxiv.org/pdf/2511.01571
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2511.01571)** / [論文ページ](https://arxiv.org/abs/2511.01571)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Published as a conference paper at ICLR 2026 

# PIXELVLA: ADVANCING PIXEL-LEVEL UNDERSTANDING IN VISION-LANGUAGE-ACTION MODEL 

**Wenqi Liang**<sup>1</sup><sup>_,_2</sup> **, Gan Sun**<sup>2</sup><sup>_†_</sup> **, Yao He**<sup>2</sup> **, Jiahua Dong**<sup>3</sup> **, Suyan Dai**<sup>2</sup> **, Ivan Laptev**<sup>3</sup> **, Salman Khan**<sup>3</sup><sup>_,_4</sup> , **Yang Cong**<sup>2</sup> 

- 1 University of Trento 

- 2 School of Automation Science and Engineering, South China University of Technology 

- 3 Mohamed bin Zayed University of Artificial Intelligence 

- 4 Australian National University 

- _{_ liangwenqi0123, sungan1412, heyao0293, dongjiahua1995, congyang81 _}_ @gmail.com, _{_ ivan.laptev, salman.khan _}_ @mbzuai.ac.ae _†_ Corresponding Author 


Figure 1: We introduce PixelVLA, a vision–language–action (VLA) model designed for pixel-level reasoning and multimodal prompting. Unlike prior VLA models (a), which primarily rely on imagelevel understanding for manipulation and depend solely on textual instructions, PixelVLA (b) advances beyond these limitations by enabling fine-grained pixel-level comprehension and supporting both textual and visual prompts. This paradigm effectively enhances spatial precision and expands human–robot interaction, leading to superior performance (c) compared to baseline methods. 

## ABSTRACT 

Vision-Language-Action models (VLAs) are emerging as powerful tools for learning generalizable visuomotor control policies. However, current VLAs are mostly trained on large-scale image–text–action data and remain limited in two key ways: (i) they struggle with pixel-level scene understanding, and (ii) they rely heavily on textual prompts, which reduces their flexibility in real-world settings. To address these challenges, we introduce PixelVLA, the first VLA model designed to support both pixel-level reasoning and multimodal prompting with text and visual inputs. Our approach is built on a new visuomotor instruction tuning framework that integrates a multiscale pixel-aware encoder with a visual promptaware encoder. To train PixelVLA effectively, we further propose a two-stage automated annotation pipeline that generates Pixel-160K, a large-scale dataset with pixel-level annotations derived from existing robot data. Experiments on three standard VLA benchmarks and two VLA model variants show that PixelVLA improves manipulation success rates by 10 _._ 1% _∼_ 28 _._ 7% over OpenVLA, while requiring only 1 _._ 5% of its pretraining cost. These results demonstrate that PixelVLA can be integrated into existing VLAs to enable more accurate, efficient, and versatile robot control in complex environments. Project page: https://wenqiliang.github.io/PixelVLA/. 

1 

Published as a conference paper at ICLR 2026 

## 1 INTRODUCTION 

Traditional robotic policy learning methods (Brohan et al. (2022); Liang et al. (2024); Chi et al. (2023); Dong et al. (2026)) rely heavily on task-specific demonstration datasets (James et al. (2020); Liu et al. (2023a)), which limits their ability to generalize to out-of-distribution (OOD) tasks. In contrast, vision-language-action models (VLAs) (Brohan et al. (2023); Kim et al. (2024); Black et al. (2024)) leverage large-scale robot datasets together with pre-trained vision-language models (VLMs), achieving stronger generalization and instruction-following capabilities. For example, RT2 (Brohan et al. (2023)) integrates internet-scale VLMs with robotic control, enabling semantic reasoning and manipulation of novel objects. Similarly, OpenVLA (Kim et al. (2024)) leverages Prismatic VLM (Karamcheti et al. (2024)) as backbone to conduct large-scale training on the OXE dataset (O’Neill et al. (2024)), leading to significant improvement in OOD generalization. 

Despite recent progress, as shown in Fig. 1 (a), most VLAs (Kim et al. (2024); Han et al. (2026); Shi et al. (2025)) inherit from VLMs that process observations only at the image level, lacking fine-grained pixel-level understanding. This gap limits spatial reasoning and weakens OOD generalization. In contrast, pixel-level comprehension has already been successfully validated in VLMs (Ren et al. (2024); Zhang et al. (2024b)) and enables precise object perception and richer spatial awareness, which are key for robust manipulation in diverse environments. The second limitation lies in prompting. Most VLAs depend solely on textual instructions, which overlook subtle visual cues and constrain spatial awareness (Ranasinghe et al. (2024)) and multimodal human–robot interaction (Jiang et al. (2023); Zheng et al. (2024); Li et al. (2026)). To explore visual prompting in VLAs, TraceVLA (Zheng et al. (2024)) improves spatial-temporal awareness with visual traces, and LLaRA (Li et al. (2025b)) encodes object locations within textual prompts to enhance regionlevel understanding. Nevertheless, these approaches still face challenges in achieving fine-grained pixel-level understanding and effectively integrating diverse multimodal prompts ( _e.g._ , points, lines, regions, masks) (Wu et al. (2024b); Dong et al. (2024)). 

Inspired by the successful visual instruction tuning in VLMs (Liu et al. (2023b); Karamcheti et al. (2024)), we introduce a novel visuomotor instruction tuning framework to train our VLA models. This framework is designed to significantly enhance the pixel-level understanding capabilities of VLAs and empower them to effectively process multimodal visuomotor control prompts. However, current robotic datasets (O’Neill et al. (2024); Khazatsky et al. (2024)) lack multimodal prompts and pixel-level annotations. Meanwhile, directly employing existing VLMs and open-set segmentation models (Karamcheti et al. (2024); Liu et al. (2024a)) to extract visual prompts and pixel-level annotations proves to be ineffective. This is due to a significant domain gap between their pre-training data and robotic data, as well as the cluttered and low-quality nature of robotic images. 

To tackle the above challenges, as presented in Fig. 1 (b), we introduce PixelVLA in this paper, the first vision-language-action model that achieves both **pixel-level understanding** and **multimodal prompting** . The model architecture of PixelVLA comprises a pre-trained VLMs as backbone, a visual prompt-aware encoder, a multiscale pixel-aware encoder and a continuous action decoder. Specifically, in PixelVLA, we introduce a lightweight visual prompt-aware encoder to process the diverse visual prompts ( _e.g._ , points, lines, regions, masks). Subsequently, a novel multiscale pixelaware encoder is designed to generate pixel-aware embeddings to inject pixel-level understanding into VLAs. Furthermore, we develop a continuous action representation decoder that leverages pixel-level understanding to capture fine-grained action details based on the hidden states of VLMs. 

To address the challenge of synthesizing high-quality multimodal prompts and pixel-level annotations from cluttered, low-quality robot observations, we propose a two-stage automated annotation pipeline to create a pixel-annotated visuomotor instruction tuning dataset, namely **Pixel-160K** . Concretely, our two-stage automated annotation pipeline comprises a gripper-aware region proposal stage followed by a multimodal object segmentation stage. In the first stage, a video segmentation model is employed to localize the robot gripper and generate preliminary region proposals for target objects. Subsequently, the second stage leverages a large language model (LLM) and an open-vocabulary segmentation model to predict pixel-level annotations and produce multimodal prompts from these region proposals. Thereafter, we train PixelVLA using the proposed visuomotor instruction tuning framework, which incorporates a continuous action training stage and a pixel-level understanding enhancement stage. To evaluate the effectiveness of PixelVLA, we integrate its architecture and visuomotor instruction-tuning procedure into two widely adopted VLAs: 

2 

Published as a conference paper at ICLR 2026 

OpenVLA (O’Neill et al. (2024)) and _π_ 0 (Black et al. (2024)). Extensive evaluations on three VLA benchmarks demonstrate that PixelVLA advances current VLAs to achieve superior performance in zero-shot manipulation tasks and adaptation to new robot setups, while requiring only 1 _._ 5% of the pretraining computation of OpenVLA. 

The main contributions of this paper are listed below: 

- We present PixelVLA, a novel vision-language-action model enabling pixel-level understanding while supporting both textual and visual prompts. In PixelVLA, we introduce a lightweight visual prompt-aware encoder to process diverse visual prompts, a novel multiscale pixel-aware encoder for pixel-level understanding injection, and a continuous action decoder to generate robotic action. 

- We design a novel two-stage automated annotation pipeline to effectively create a pixellevel visuomotor instruction tuning dataset from the publicly available robot datasets, called Pixel-160K, where the pipeline comprises the gripper-aware region proposal stage and the multimodal object segmentation stage. 

- We introduce a novel visuomotor instruction tuning framework for training PixelVLA, comprising a continuous action training stage and a pixel-level understanding enhancement stage. Extensive evaluations on three benchmarks and two VLA model variants show that PixelVLA improves performance of current VLAs with relatively low training cost. 

## 2 RELATED WORK 

**Vision-Language-Action Models** . Vision-language-action models (VLAs) (Team et al. (2025); Brohan et al. (2023); Black et al. (2024); Ding et al. (2024); Fan et al. (2025)) have propelled robotic manipulation forward by endowing robots with the ability to understand and execute language-based instructions in diverse visual environments. Trained on numerous robot episodes, OpenVLA (Kim et al. (2024)) enables zero-shot control and adaptation for various robots. Building on the foundational capabilities of OpenVLA, various approaches have been proposed to advance robotic manipulation, such as SpatialVLA (Qu et al. (2025)) and ECoT (Zawalski et al. (2024)). Most prior VLAs focus on innovations in visual processing for robotic manipulation, such as introducing visual chain-of-thought (CoT) reasoning mechanisms for visual planning (Zhao et al. (2025)). Nevertheless, they primarily process visual information at the image level, lacking the ability to perform detailed pixel-level visual processing required for precise robotic manipulation. 

**Visual Prompting in VLMs** . Visual prompting methods (Zhang et al. (2023); Ren et al. (2024); Wu et al. (2024a); Zhang et al. (2024b)) have recently emerged as a complementary paradigm to textual prompting, allowing models to accept more fine-grained supervision in the form of region-level (Guo et al. (2024)) and even pixel-level instructions (Ma et al. (2024); Rasheed et al. (2024)) over multimodal inputs. Shikra (Chen et al. (2023)) extends MLLMs with a simple vision–encoder–LLM architecture that treats spatial coordinates as natural language tokens. Ferret (You et al. (2023)) enhances region-level grounding in MLLMs through a hybrid region representation and a spatial-aware visual sampler that supports diverse region inputs, while Ferret-v2 (Zhang et al. (2024a)) further introduces any-resolution grounding and multi-granularity visual encoding, leading to improved fine-grained visual understanding and localization over prior MLLMs. LocVLM (Ranasinghe et al. (2024)) proposes an image-space coordinate–based instruction fine-tuning framework for MLLMs that explores coordinate representations and spatial objectives to inject spatial awareness. However, despite these advances, robust pixel-level understanding in VLA frameworks remains challenging, especially when aligning fine-grained spatial cues with continuous, high-precision action control. 

**Visual Instruction Tuning in VLAs** . Visual Instruction Tuning (Zhu et al. (2023); Liu et al. (2023b); Rasheed et al. (2024)) is generally divided into two steps, which are modality alignment and instruction optimization, respectively. This strategy also serves as the core paradigm for realizing multimodal capabilities in VLAs (Li et al. (2025b), Zheng et al. (2024); Zawalski et al. (2024)). For example, TraceVLA (Zheng et al. (2024)) introduces visual trace prompting to enhance spatial-temporal awareness in VLAs. In contrast, LLaRA (Li et al. (2025b)) reformulates the robot action policy as visuo-textual conversations through visuomotor instruction tuning and RoVI (Li et al. (2025c)) develops an object-centric visual instruction paradigm with symbolic sketches. However, to address various visuomotor control challenges, adapting visual instruction tuning for VLAs remains a major constraint. 

3 

Published as a conference paper at ICLR 2026 


Figure 2: Overview of the PixelVLA architecture. The model integrates three novel components: (1) a _visual prompt-aware encoder_ for processing input diverse visual prompts; (2) a _multiscale pixelaware encoder_ that injects pixel-level information into token embeddings; and (3) a _continuous action decoder_ to predict 7D robot actions. PixelVLA enhances fine-grained pixel-level spatial understanding and multimodal prompt responsiveness, enabling more precise manipulation policies in visually complex scenarios. 

## 3 PROBLEM DEFINITION: VISUOMOTOR INSTRUCTION TUNING 

Inspired by the effectiveness of visual instruction tuning in VLMs (Liu et al. (2023b); Rasheed et al. (2024); Wu et al. (2024a); Kang et al. (2025); Li et al. (2025a)), we aim to adapt a similar process for VLAs to tackle diverse visuomotor control challenges ( _e.g._ , various multimodal prompts) and achieve pixel-level understanding. Similar to LLaRA (Li et al. (2025b)), we formalize this paradigm as Visuomotor Instruction Tuning. Specifically, following OpenVLA (Kim et al. (2024)), given a series of image observations **X** = _{_ **x**<sup>_t_</sup> _∈_ R<sup>_H×W ×_3</sup> _}_<sup>_T_</sup> _t_ =1<sup>andalanguageinstruction</sup><sup>**L**,theVLA</sup> model _Fθ_ ( _·_ ) can generate a series of robotic actions **A** = _{_ **a**<sup>_t_</sup> _∈_ R<sup>7</sup> _}_<sup>_T_</sup> _t_ =1<sup>,</sup><sup>_i.e._,</sup><sup>**a**</sup><sup>_t_=</sup><sup>_Fθ_(</sup><sup>**x**</sup><sup>_t,_</sup><sup>**L**).</sup> For an episode of length _T_ , the likelihood of successfully completing the task through an action sequence **A** can be calculated as: 


where _T_ denotes the length of timestep in an episode, _θ_ represents the parameters of VLA model _Fθ_ ( _·_ ) and _pθ_ denotes the likelihood of generating action **a**<sup>_t_</sup> by the VLA model _Fθ_ ( _·_ ). However, this robotic action generation process fails to accommodate various visual prompts and achieve fine-grained pixel-level understanding. To address these challenges, we here introduce a novel visuomotor instruction tuning framework that reformulates robotic action generation as **a**<sup>_t_</sup> = _Fθ_ ( **x**<sup>_t_</sup> _,_ **p**<sup>_t_</sup> _,_ **L** _,_ **V** ) and reformulate the likelihood in Eq. (1) for an episode of length _T_ as: 


where **P** = _{_ **p**<sup>_t_</sup> _∈_ R<sup>_H×W_</sup> _}_<sup>_T_</sup> _t_ =1<sup>,</sup><sup>**p**</sup><sup>_t_represents the pixel-aware mask input, and</sup><sup>**V**denotes the diverse</sup> visual prompts ( _e.g._ , points, lines, regions, masks). 

## 4 THE PROPOSED METHOD 

As illustrated in Fig. 2, we present the architecture of the proposed PixelVLA to achieve pixellevel understanding and accommodate both textual and visual prompts. Specifically, PixelVLA integrates a novel multiscale pixel-aware encoder (Sec. 4.1) that infuses pixel-level understanding into VLAs through tokenized representations, a visual prompt-aware encoder for handling diverse visual prompts (Sec. 4.1), and a continuous action decoder (Sec. 4.1) for accurate robotic action 

4 

Published as a conference paper at ICLR 2026 

prediction. In addition, an automated annotation generation pipeline and a pixel-annotated visuomotor instruction tuning dataset Pixel-160K are presented in Sec. 4.2. Subsequently, we introduce the proposed visuomotor instruction tuning procedure for training PixelVLA in Sec. 4.3. 

### 4.1 PIXELVLA ARCHITECTURE 

Current VLAs (Black et al. (2024); Kim et al. (2024); Wang et al. (2026b;a)) are typically pretrained on large-scale image-instruction-action robotic datasets (O’Neill et al. (2024); Wu et al. (2024c)). Architecturally built upon VLMs, these models process single or multi-view images along with textual instructions. However, this foundation inherently restricts their ability to achieve pixellevel understanding or respond to detailed visual prompts, resulting in constraining VLAs for spatial comprehension and object perception. 

To address these architectural constraints, as illustrated in Fig. 2, we present a novel VLA model, namely PixelVLA. Specifically, PixelVLA integrates four main parts: (1) a **vision encoder** and **MLP projector** for visual embedding extraction, (2) a **visual prompt-aware encoder** and a **multiscale pixel-aware encoder** for accommodating visual prompts and pixel-level understanding injection, (3) a **LLM backbone** and (4) a **continuous action decoder** for non-discrete robot action prediction. Following OpenVLA (Kim et al. (2024)), we preliminarily build our PixelVLA on Prismatic-7B VLM (Karamcheti et al. (2024)), where a Llama 2-7B (Touvron et al. (2023)) is employed as LLM backbone. The vision encoder of PixelVLA consists of pre-trained DinoV2 (Oquab et al. (2023)) and SigLIP (Zhai et al. (2023)) models, and a lightweight 2-layer MLP projector is utilized to map the output features of the vision encoder into the input space of LLM. 

**Multiscale Pixel-aware Encoder** . To extract pixel-level information from multiscale image features and encode the spatial positional information of visual prompts, we propose a multiscale pixel-aware encoder designed to generate both pixel-aware embeddings and prompt-aware embeddings. Specifically, as described in Eq. (2), for each training sample _{_ **x**<sup>0</sup> _,_ **p**<sup>0</sup> _,_ **L**<sup>0</sup> _,_ **V**<sup>0</sup> _}_ drawn from Pixel-160K, PixelVLA first encodes the image observation **x**<sup>0</sup> _∈_ R<sup>_H×W ×_3</sup> with the SigLIP vision encoder to obtain multi-level visual features **F**<sup>0</sup> _v_<sup>=</sup><sup>_{_</sup><sup>**f**0</sup> _v_<sup>_,i_</sup> _∈_ R<sup>_Hi×Wi×Di_</sup> _}_<sup>_L_</sup> _i_ =1<sup>,where</sup><sup>_L_denotes the number of</sup> selected feature levels. As illustrated in Fig. 2 (a), the multiscale pixel-aware encoder leverages the features **F**<sup>0</sup> _v_<sup>andapixel-awaremaskinput</sup><sup>**p**0</sup><sup>_∈_R</sup><sup>_H×W_tocomputethepixel-awareembed-</sup> dings **E**<sup>0</sup> _p_<sup>_∈_R</sup><sup>_Np×D_.Here,</sup><sup>_Np_is the length of pixel-aware embeddings and</sup><sup>_D_denotes the feature</sup> dimension of LLM. Specifically, the pixel-aware embeddings **E**<sup>0</sup> _p_<sup>can be computed as follows:</sup> 


where MLP( _·_ ) is a multilayer perceptron (MLP) layer and Γ<sup>_i_</sup> ( _·_ ) denotes the linear projection in the _i_ -th linear projector. Supervised by the action prediction loss, PixelVLA learns to associate the pixel-level information encoded in these pixel-aware embeddings **E**<sup>0</sup> _p_<sup>with action generation, thereby</sup> enhancing the VLA backbone with pixel-level understanding. 

**Visual Prompt-aware Encoder** . As shown in Fig. 2(b), we adopt a lightweight prompt encoder similar to that in SAM (Kirillov et al. (2023)) and integrate it into PixelVLA as the visual prompting encoder. Concretely, the user-provided prompts **V**<sup>0</sup> _∈_ R<sup>_H×W_</sup> are first converted into continuous positional embeddings based on their normalized image coordinates, and then combined with learned prompt-type embeddings to produce prompt features **F**<sup>0</sup> _s_<sup>_∈_R</sup><sup>_Ns×Ds_,where</sup><sup>_Ns_istheembedding</sup> length and _Ds_ is the feature dimension. These features **F**<sup>0</sup> _s_<sup>arefurthertransformedbyanMLPto</sup> obtain the final prompt-aware embeddings **E**<sup>0</sup> _s_<sup>_∈_R</sup><sup>_Ns×D_.Since each embedding is explicitly tied to</sup> a specific location or region in the image via its coordinate-based positional embedding, the spatial positional information of the visual prompts is preserved throughout the encoding process. 

**Continuous Action Decoder** . Most existing VLA models (Kim et al. (2024); Zheng et al. (2024); Li et al. (2024b)) adapt autoregressive generation to predict sequential action tokens based on the pre-trained VLM backbone. In contrast, following _π_ 0 (Black et al. (2024)), we develop a continuous action decoder that directly predicts continuous action representations, leveraging pixel-level understanding to capture fine-grained action details. Specifically, as illustrated in Fig. 2 (b), the hidden states **F**<sup>_t_</sup> _∈_ R<sup>_Ns×D_</sup> from the last layer of LLM backbone are sequentially processed by a linear projector, _Nr_ ResNet blocks and a MLP projector to obtain the actions **A** _∈_ R<sup>_Nc×_7</sup> . Here, 

5 

Published as a conference paper at ICLR 2026 


Figure 3: Overview of the Pixel-160K Dataset. 

_Ns_ denotes the sequence length of the LLM backbone, while _Nc_ represents the chunk size used in action chunking (Zhao et al. (2023)). In this way, we can effectively preserve the pixel-level understanding learned by the pre-trained VLM backbone while enabling the continuous action decoder to incorporate these features directly into the continuous action prediction. The resulting continuous actions are then used to compute an L1 regression loss that supervises the training process. 

### 4.2 VISUOMOTOR TUNING DATA GENERATION 

In this section, we introduce Pixel-160K as shown in Fig. 3, a visuomotor instruction tuning dataset comprising image-text-action triplets with visual prompts and mask annotations, containing approximately 160K manipulation episodes to encourage VLAs for fine-grained pixel-level understanding. Specifically, to address the challenge of cluttered and low-quality robot observations in robot datasets, we propose an automated annotation pipeline containing a gripper-aware region proposal stage and a multimodal object segmentation stage. This pipeline enables the effective generation of visual prompts and mask annotations for each episode using the publicly available Fractal dataset (Brohan et al. (2022)) and Bridge v2 dataset (Walke et al. (2023)). 

**Gripper-aware Region Proposal Stage** . Given a sequence of observations _{_ **x**<sup>1</sup> _η_<sup>_,_</sup><sup>**x**2</sup> _η_<sup>_, . . . ,_</sup><sup>**x**</sup> _η_<sup>_Nη}_</sup> from the _η_ -th episode, the first gripper-close state in the episode as _Gη ∈{_ 1 _,_ 2 _, . . . , Nη}_ and the corresponding observation as **x**<sup>_G_</sup> _η_<sup>_η_</sup> _∈{_ **x**<sup>1</sup> _η_<sup>_,_</sup><sup>**x**2</sup> _η_<sup>_, . . . ,_</sup><sup>**x**</sup> _η_<sup>_Nη}_.</sup> Here, _Nη_ represents the length of the _η_ -th episode. Sequentially, we can select a series of gripper-close state observations _{_ **x**<sup>_G_</sup> 1<sup>1</sup><sup>_,_</sup><sup>**x**</sup> 2<sup>_G_2</sup><sup>_, . . . ,_</sup><sup>**x**</sup> _N_<sup>_GNe_</sup> _e_<sup>_}_from the whole dataset, where</sup><sup>_Ne_denotes the number of total episodes in the</sup> dataset. Furthermore, we assume _{_ **x**<sup>_G_</sup> 1<sup>1</sup><sup>_,_</sup><sup>**x**</sup><sup>_G_</sup> 2<sup>2</sup><sup>_, . . . ,_</sup><sup>**x**</sup><sup>_G_</sup> _N_<sup>_Ne_</sup> _e_<sup>_}_as a discrete video and apply SAM 2 (Ravi</sup> et al. (2024)) to generate _Ne_ gripper masks. Then, we compute the minimal axis-aligned bounding boxes enclosing these masks, uniformly enlarge each by a fixed margin to capture local context and reduce detection noise, and take the resulting boxes as the _Ne_ region proposals _{_ **R** 1 _,_ **R** 2 _, . . . ,_ **R** _Ne }_ . Here, **R** _η ∈_ R<sup>4</sup> is the proposal for the _η_ -th episode. In this way, the region proposals can be leveraged to accurately capture object from cluttered and low-quality robot observations. 

**Multimodal Object Segmentation Stage** . Given a manipulation instruction such as “ _Put the Eggplant in Yellow Basket_ ”, we employ Llama 2–7B to reason over the instruction and extract the textual description of the target object to be manipulated, _e.g._ , “ _Eggplant_ ”. For the _η_ -th episode, we then provide the target object text along with the region proposal _{_ **R** _η}_ into an open-vocabulary object detector Grounding DINO (Liu et al. (2024a)) and SAM (Kirillov et al. (2023)). These models detect all relevant object instances, generate their mask annotations, and associate them with the corresponding language expressions from the target object text. We then filter the predictions based on their confidence scores, retaining only the mask annotations within the bounding box that has the highest box-confidence. Sequentially, we derive visual prompts from the object masks by randomly sampling points within the mask, generating random lines inside the object region, and extracting external bounding boxes through mask contour detection. 

Finally, we apply the proposed two-stage automated annotation pipeline to the publicly available Fractal dataset (Brohan et al. (2022)) and Bridge v2 dataset (Walke et al. (2023)). We first au- 

6 

Published as a conference paper at ICLR 2026 

Table 1: SimplerEnv (Li et al. (2024c)) simulation evaluation results in terms of the average success rate for the Google Robot setup. VM denotes Visual Matching and VA is Variant Aggregation. ■ and ■ denote tuning-based methods applied to the pretrained weights of OpenVLA and _π_ 0, respectively. 

|Mthd|Pick Co|ke Can|Move|Near|Open/Clo|se Drawer|**Ave**|**rage**|
|---|---|---|---|---|---|---|---|---|
|eos|VM|VA|VM|VA|VM|VA|VM|VA|
|RT-1-X (O’Neill et al.(2024))|56.7|49.0|31.7|32.3|59.7|29.4|49.4|36.9|
|Octo-Base (Team et al.(2024))|17.0|0.6|4.2|3.1|22.7|1.1|14.6|1.6|
|HPT (Wang et al.(2024))|56.0|–|60.0|–|24.0|–|46.7|–|
|RoboVLMs (Liu et al.(2025))|72.7|68.3|66.3|56.0|26.8|8.5|56.3|46.3|
|Dita (Hou et al.(2025))|83.7|85.5|76.0|73.0|46.3|37.5|68.7|65.3|
|SpatialVLA (Qu et al.(2025))|81.0|89.5|69.6|71.7|59.3|36.2|71.9|68.8|
|OpenVLA (Kim et al.(2024))|16.3|54.5|46.2|47.7|35.6|17.7|32.7|40.0|
|OpenVLA-SFT|17.5|51.9|44.6|42.3|32.8|16.8|31.6|38.6|
|TraceVLA (Zheng et al.(2024))|28.0|60.0|53.7|56.4|**57.0**|**31.0**|46.2|49.1|
|**PixelVLA**|**81.7**|**72.7**|**60.1**|**57.7**|42.3|20.0|**61.4**|**50.1**|
|_π_0 (Black et al.(2024))|72.7|75.2|65.3|**63.7**|38.3|25.6|58.8|54.8|
|_π_0-SFT|70.8|72.1|64.2|61.3|36.8|28.3|57.3|53.9|
|**PixelVLA**-_π_0|**80.7**|**76.8**|**67.7**|62.0|**41.3**|**30.8**|**63.3**|**56.5**|


tomatically discard samples with failed mask generation ( _e.g._ , empty or invalid masks) using a simple script, and then the authors rapidly inspect the remaining samples to remove those with clearly incorrect masks. In total, this process filters out approximately 19.2% of the generated samples. The resulting dataset, Pixel-160K, contains 160K robot manipulation episodes and 6.5M image–text–action triplets with visual prompts and mask annotations. 

### 4.3 VISUOMOTOR INSTRUCTION TUNING PROCEDURE 

To advance fine-grained pixel-level understanding in VLAs, we propose a novel visuomotor instruction tuning procedure, consisting of a continuous action training stage and a pixel-level understanding enhancement stage. Concretely, the first continuous action training stage enables the VLA model to acquire robust continuous action representations from a large mixture of image–text–action datasets. In the second stage, pixel-level understanding is explicitly enhanced by adapting the pretrained model on Pixel-160K dataset through LoRA adaptation (Hu et al. (2022); Li et al. (2025d)). The following sections elaborate on the key designs of this two-stage training strategy. 

**Continuous Action Training Stage** . Before training, we initialize the vision encoder, the MLP projector, and the LLM backbone in PixelVLA with the pretrained weights of VLAs (Kim et al. (2024); Black et al. (2024)), which has been trained on the large-scale mixture dataset OXE (O’Neill et al. (2024)). In addition, during this stage, the visual prompt-aware encoder and the multiscale pixelaware encoder of PixelVLA are removed, while all other modules except the continuous action decoder are frozen to preserve the general manipulation knowledge learned in the pretrained VLAs. To directly map the final hidden states of the last layer of LLM to continuous action values, we follow (Zhao et al. (2023); Kim et al. (2025)) to implement L1 regression to align predicted actions generated by the proposed continuous action decoder with the ground-truth actions. Unlike OpenVLA, which represents actions as discrete tokens by normalizing each action dimension to [ _−_ 1 _,_ +1] and uniformly discretizing it into 256 bins, PixelVLA directly predicts continuous action values, thereby avoiding the loss of fine-grained action details introduced by discretization. Furthermore, during this stage, we train PixelVLA on a mixture of Fractal dataset and Bridge v2 dataset. 

**Pixel-level Understanding Enhancement Stage** . Originally, most existing visuomotor instruction tuning methods (Li et al. (2025b); Kim et al. (2025); Yang et al. (2025)) focus on image-level understanding. In contrast, at this stage, to enhance pixel-level understanding of PixelVLA, we employ LoRA adaptation to efficiently fine-tune PixelVLA’s LLM backbone on Pixel-160K dataset, while jointly training the visual prompt-aware encoder along with the multiscale pixel-aware encoder. Meanwhile, the continuous action decoder is optimized while the remaining PixelVLA modules remain frozen. Furthermore, we adopt the same L1 regression loss and continuous action representation strategy as those employed in the continuous action training stage. At each training step, given 

7 

Published as a conference paper at ICLR 2026 

Table 2: Evaluation results from the SimplerEnv simulation for the WidowX robot. Gra. denotes the average grasp success rate, and Suc. is the overall task completion success rate. 

|Methods|Put S<br>|poon<br>|Put C<br>|arrot<br>|Stack<br>|Blocks<br>|Put Eg<br>|gplant<br>|**Ave**<br>|**rage**<br>|
|---|---|---|---|---|---|---|---|---|---|---|
||Gra.|Suc.|Gra.|Suc.|Gra.|Suc.|Gra.|Suc.|Gra.|Suc.|
|RT-1-X (O’Neill et al.(2024))|16.7|0.0|20.8|4.2|8.3|0.0|0.0|0.0|11.5|1.1|
|Octo-Base (Team et al.(2024))|34.7|12.5|52.8|8.3|31.9|0.0|66.7|43.1|46.5|16.0|
|Octo-Small (Team et al.(2024))|77.8|47.2|27.8|9.7|40.3|4.2|87.5|56.9|58.4|29.5|
|RoboVLMs (Liu et al.(2025))|37.5|20.8|33.3|25.0|8.3|8.3|0.0|0.0|19.8|13.5|
|SpatialVLA (Qu et al.(2025))|25.0|20.8|41.7|20.8|58.3|25.0|79.2|70.8|51.1|34.4|
|OpenVLA (Kim et al.(2024))|4.1|0.0|33.3|0.0|12.5|0.0|8.3|4.1|14.6|1.0|
|OpenVLA-SFT|8.4|0.0|35.1|12.8|10.5|0.0|16.5|8.4|17.6|5.3|
|**PixelVLA**|20.8|4.2|**37.5**|**20.8**|16.6|0.0|79.2|41.7|38.5|16.7|
|_π_0 (Black et al.(2024))|45.8|29.1|25.0|0.0|50.0|16.6|**91.6**|**62.5**|53.1|27.1|
|_π_0-SFT|45.3|26.8|28.6|4.2|52.3|18.6|88.5|59.6|53.7|27.3|
|**PixelVLA-**_π_0|**51.7**|**32.4**|28.7|16.7|**56.8**|**21.7**|83.3|61.7|**55.1**|**33.8**|


a mini-batch _{_ **x**<sup>_i_</sup> _,_ **p**<sup>_i_</sup> _,_ **a**<sup>_i_</sup> _,_ **L**<sup>_i_</sup> _,_ **V**<sup>_i_</sup> _}_<sup>_B_</sup> _i_ =1<sup>sampled from the Pixel-160K dataset, the forward process at a</sup> single timestep of this stage can then be formulated as follows: 


where _C_ ( _·_ ) refers to the continuous action decoder and _H_ represents the LLM backbone of PixelVLA. In addition, _B_ denotes the mini-batch size and _∥· ∥_ 1 is the L1 norm used for regression. Notably, **E**<sup>_i_</sup> _v_<sup>_,_</sup><sup>**E**</sup><sup>_i_</sup> _l_<sup>_,_</sup><sup>**E**</sup> _o_<sup>_i,_</sup><sup>**E**</sup><sup>_i_</sup> _s_<sup>correspondtothevisualembeddingsproducedbythevisionencoderand</sup> the MLP projector, the language embeddings from the LLM tokenizer, the pixel-aware embeddings and the prompt-aware embeddings, respectively. 

## 5 EXPERIMENTS 

We conduct experiments to investigate how PixelVLA leverages pixel-level understanding and multimodal prompts to enhance the performance of current VLAs in both in-domain and out-of-domain adaptation. To achieve this objective, we develop three experimental paradigms: (1) zero-shot object manipulation comparisons for out-of-domain generalization (Sec. 5.2), (2) adaptation to new robot setups to evaluate in-domain robustness (Sec. 5.3), and (3) a series of ablation studies to quantify the contribution of each individual module within PixelVLA (Sec. 5.4). 

### 5.1 EXPERIMENTAL SETUP 

**Evaluation tasks** . We conduct all experiments on three simulation benchmarks, _i.e._ , SimplerEnvGoogle Robot (Li et al. (2024c)), SimplerEnv-WidowX (Li et al. (2024c)) and LIBERO (Liu et al. (2023a)). SimplerEnv (Li et al. (2024c)) is an open-source simulation suite that facilitates reproducible and scalable evaluation of robot manipulation policies by explicitly addressing visual and dynamic gaps between simulation and real hardware. In light of this, we conduct zero-shot object manipulation comparisons on SimplerEnv. In addition, following OpenVLA (Kim et al. (2024)), we evaluate performance of new robot adaptation across four task suites within LIBERO (Liu et al. (2023a)), _i.e._ , LIBERO-Spatial, LIBERO-Object, LIBERO-Goal and LIBERO-Long. 

**Implementation Details** . To evaluate the effectiveness of PixelVLA, we apply its architecture and the proposed visuomotor instruction-tuning procedure to two widely-used VLAs, OpenVLA (Kim et al. (2024)) and _π_ 0 (Black et al. (2024)). Regarding the training data, PixelVLA is trained in two stages: the first stage utilizes real-robot demonstrations from the Fractal dataset (Brohan et al. (2022)) and Bridge v2 dataset (Walke et al. (2023)), while the second stage employs 160K realrobot demonstrations from the proposed Pixel-160K dataset. For input robot observations across all datasets, PixelVLA is conditioned solely on a single third-person camera view and processes images at a resolution of 224×224 pixels. In all training stages, we set action chunk size to 8 for 

8 

Published as a conference paper at ICLR 2026 

Table 3: LIBERO Simulation Benchmark Results. We report the success rates of each method across four task suites. Models including Octo, OpenVLA, TraceVLA, Dita, SpatialVLA and PixelVLA are adapted through fine-tuning. R. represents the success rate ranking in each task suite. 

|Methods|Spat<br>Suc.(_↑_)|ial<br> R.(_↓_)|Obj<br> Suc.(_↑_)|ect<br> R.(_↓_)|Go<br> Suc.(_↑_)|al<br> R.(_↓_)|Lon<br> Suc.(_↑_)|g<br> R.(_↓_)|**Average**|
|---|---|---|---|---|---|---|---|---|---|
|Diffusion Policy (Chi et al.(2023))|78.3|8|92.5|2|68.3|7|50.5|7|72.4|
|Octo (Team et al.(2024))|78.9|7|85.7|7|84.6|4|51.1|6|75.1|
|CoT-VLA (Zhao et al.(2025))|87.5|3|91.6|3|**87.6**|1|69.0|2|81.1|
|Dita (Hou et al.(2025))|84.2|6|**96.3**|1|85.4|3|63.8|3|82.4|
|SpatialVLA (Qu et al.(2025))|88.2|2|89.9|5|78.6|6|55.5|4|78.1|
|OpenVLA (Kim et al.(2024))|84.7|4|88.4|6|79.2|5|53.7|5|76.5|
|TraceVLA (Zheng et al.(2024))|84.6|5|89.9|5|78.6|6|55.5|4|78.1|
|**PixelVLA**|**88.5**|1|90.0|4|85.8|2|**82.6**|1|**86.7**|


the continuous action decoder, _i.e._ , the predicted action **a**<sup>**t**</sup> _∈_ R<sup>8</sup><sup>_×_7</sup> . The first training stage involves training PixelVLA for 100k steps with a batch size of 32 and a learning rate of 5 _×_ 10<sup>_−_4</sup> . Notably, in light of the effectiveness action expert in _π_ 0, we omit the first training stage when adapting PixelVLA on _π_ 0. During the second training stage, we fine-tune the LLM backbone of PixelVLA using LoRA adaptation with a rank _r_ = 32. This stage is trained for 200k steps with a batch size of 32 and a learning rate of 1 _×_ 10<sup>_−_3</sup> . In addition, to adapt PixelVLA to the LIBERO benchmark (Liu et al. (2023a)), we fine-tune the pre-trained model for 150K steps on each task suite using LoRA adaptation with rank _r_ = 32, a batch size of 32, and a learning rate of 5 _×_ 10<sup>_−_4</sup> . In addition to the two baseline VLAs, OpenVLA (Kim et al. (2024)) and _π_ 0 (Black et al. (2024)), we compare the performance of PixelVLA against other state-of-the-art VLAs, such as RT-1 (Brohan et al. (2022)), HPT (Wang et al. (2024)), Octo (Team et al. (2024)), TraceVLA (Zheng et al. (2024)), RoboVLMs (Liu et al. (2025)), Dita (Hou et al. (2025)) and SpatialVLA (Qu et al. (2025)). To further ensure fairness, we additionally fine-tune _π_ 0 and OpenVLA on the Fractal and Bridge datasets, obtaining baselines denoted as _π_ 0-SFT and OpenVLA-SFT. 

### 5.2 ZERO-SHOT OBJECT MANIPULATION COMPARISONS 

This subsection evaluates the zero-shot manipulation performance of our model against baseline VLAs across multiple Base Setup (a) Camera Orientations task categories and robot platforms. As shown in Tab. 1, on the Google Robot setup PixelVLA achieves an average VM (b) LightingChange (c) BackgroundChange score of 61.4 and VA score of 50.1, surpassing OpenVLA by <u>28.7/10.1</u> and OpenVLA-SFT by 29.8/11 ~~<u>.</u>~~ ~~<u><mark>5</mark></u>~~ in VM/VA, respectively. These results indicate a (d) Distractor (e) Table Texture strong capability in both pixel-level unInitial States Figure 4: Performance comparison of OpenVLA, derstanding and adaptation to textual and TraceVLA and PixelVLA performance across varivisual prompts in out-of-domain adaptaous environmental variations on SimplerEnv-Google tion. Notably, as shown in Fig. 4, PixRobot setup: camera orientations, lighting, backelVLA outperforms TraceVLA and Openground, distractors, and table texture. VLA across various environmental variations, highlighting the effectiveness of the proposed visuomotor instruction tuning procedure in addressing out-of-domain generalization. 

Similar trends are observed on the WidowX robot setup in Tab 2, where PixelVLA- _π_ 0 achieves an average grasp score of 55.1 and success score of 16.7, outperforming the baseline _π_ 0 by 2.0 and 6.7, respectively, and surpassing RoboVLM by 35.3 and 18.2. The results strongly affirm that PixelVLA’s architectural innovations including its multiscale pixel-aware encoder and integration of visual prompts, significantly enhance its zero-shot perceptual and operational capabilities. Furthermore, the significant improvements of PixelVLA and PixelVLA- _π_ 0 over the baselines OpenVLA 

9 

Published as a conference paper at ICLR 2026 

and _π_ 0 demonstrate that incorporating the finer-grained pixel-level spatial comprehension into existing VLAs enables more effective adaptation to unseen objects. 

### 5.3 NEW ROBOT SETUPS ADAPTATION COMPARISONS 

To evaluate the adaptability of PixelVLA to novel robotic setups and task configurations, we employ the proposed automated annotation pipeline to process the LIBERO benchmark training data (Liu et al. (2023a)), yielding the LIBERO-Pixel dataset. Subsequently, as summarized in Tab. 3, PixelVLA achieves state-of-the-art performance with an average success rate of 86.7 across all tasks, significantly surpassing strong baselines. In addition, As shown in Tab. 3, PixelVLA outperforms OpenVLA across all four LIBERO task suites, with particularly large gains on LIBERO-Long. We attribute this to the Continuous Action Decoder: action chunking helps the policy capture longerrange temporal dependencies (Liu et al. (2024b)), while continuous action prediction mitigates compounding discretization errors (Black et al. (2024)) over long-horizon manipulation. These superior results demonstrate the enhanced adaptability of PixelVLA to new robotic setups, highlighting the effectiveness of pixel-level visual understanding and continuous action representation in PixelVLA. Notably, PixelVLA achieves significant performance in the LIBERO-Long setup, demonstrating its effectiveness in long-range manipulation. 

### 5.4 ABLATION STUDIES 

This subsection evaluates the effectiveness of individual components in PixelVLA on SimplerEnv-Google Robot in terms of Variant Aggregation. As shown in Tab. 4, we use OpenVLA as the baseline model. Here, Baseline+FT refers to fine-tuning OpenVLA directly on a mixture of Fractal dataset and Bridge v2 dataset. In addition, Baseline+FT+CAT indicates training OpenVLA with the proposed continuous action training stage using a contin- 

Table 4: Quantitative ablation studies on Variant Aggregation for the Google Robot setup, evaluated in the SimplerEnv simulation environment (Li et al. <u>(2024c)).</u> 

|Methods|Pick<br>Coke Can|Move <br>Near|Open/Close<br>Drawer|**Average**|
|---|---|---|---|---|
|Baseline|54.5|47.7|17.7|40.0|
|+FT|51.9|42.3|16.8|37.0|
|+FT+CAT|61.3|52.3|17.7|43.8|
|+FT+PUE|71.1|54.7|**21.3**|48.0|
|**PixelVLA**|**72.7**|**57.7**|20.0|**50.1**|


uous action decoder, while Baseline+FT+PUE denotes fine-tuning OpenVLA with the proposed pixel-level understanding enhancement stage on the Pixel-160 dataset. 

As presented in Tab. 4, incorporating the continuous action training stage (Baseline+FT+CAT) improves the average score of 3.8% compared to Baseline, highlighting the benefits of the proposed continuous action decoder. Further enhancement with pixel-level understanding (Baseline+FT+PUE) yields a more substantial gain of 8.0%. Compared to the single-stage Baseline+FT+PUE, PixelVLA adds a continuous action training stage, and this two-stage scheme leads to a slight drop on Open/Close Drawer, due to the catastrophic forgetting (Li et al. (2024a)) in joint two-stage optimization and the high difficulty and sensitivity of this task. Ultimately, PixelVLA outperforms Baseline+FT+CAT by 6.3%. This progressive improvement validates the effectiveness of both pixel-level understanding and multimodal prompts in advancing generalization capabilities. 

## 6 CONCLUSION 

This paper proposes PixelVLA, a vision-language-action (VLA) model, to address the limitations of existing VLAs, such as insufficient pixel-level understanding and over-reliance on textual prompts. PixelVLA integrates a multiscale pixel-aware encoder to inject pixel-level understanding, a continuous action decoder for generating accurate robotic actions, and a lightweight visual prompt-aware encoder to support both textual and visual prompts. In addition, a two-stage automated annotation pipeline is designed to construct the Pixel-160K dataset containing 160K manipulation episodes. To advance fine-grained pixel-level understanding in VLAs, we propose a novel two-stage visuomotor instruction tuning framework to train PixelVLA, requiring only 1.5% of the pretraining cost of OpenVLA. Expensive evaluations on three VLA benchmarks show that PixelVLA can be integrated into existing VLAs to achieve a 10 _._ 1% _∼_ 28 _._ 7% improvement in manipulation success rate, effectively enhancing the spatial comprehension and complex environment adaptability of VLAs. 

10 

Published as a conference paper at ICLR 2026 

### ACKNOWLEDGMENTS 

This work is supported by the National Key Research and Development Program of China (2023YFB4704800) and National Nature Science Foundation of China under Grant (62225310,62273333), and the Fundamental Research Funds for the Central Universities (2025ZYGXZR032, 2024ZYGXZR024). 

## REFERENCES 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv preprint arXiv:2212.06817_ , 2022. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. In _arXiv preprint arXiv:2307.15818_ , 2023. 

- Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, and Rui Zhao. Shikra: Unleashing multimodal llm’s referential dialogue magic. _arXiv preprint arXiv:2306.15195_ , 2023. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Pengxiang Ding, Han Zhao, Wenjie Zhang, Wenxuan Song, Min Zhang, Siteng Huang, Ningxi Yang, and Donglin Wang. Quar-vla: Vision-language-action model for quadruped robots. In _ECCV_ , pp. 352–367. Springer, 2024. 

- Jiahua Dong, Wenqi Liang, Hongliu Li, Duzhen Zhang, Meng Cao, Henghui Ding, Salman H Khan, and Fahad Shahbaz Khan. How to continually adapt text-to-image diffusion models for flexible customization? _NeurIPS_ , 37:130057–130083, 2024. 

- Jiahua Dong, Qi Lyu, Baichen Liu, Xudong Wang, Wenqi Liang, Duzhen Zhang, Jiahang Tu, Hongliu Li, Hanbin Zhao, Henghui Ding, Yulun Zhang, Zhi Han, Nicu Sebe, Fahad Shahbaz Khan, Salman Khan, Mubarak Shah, Philip Torr, Ming-Hsuan Yang, and Dacheng Tao. Learning to model the world: A survey of world models in artificial intelligence. _TechRxiv_ , 2026. 

- Cunxin Fan, Xiaosong Jia, Yihang Sun, Yixiao Wang, Jianglan Wei, Ziyang Gong, Xiangyu Zhao, Masayoshi Tomizuka, Xue Yang, Junchi Yan, et al. Interleave-vla: Enhancing robot manipulation with interleaved image-text instructions. _arXiv preprint arXiv:2505.02152_ , 2025. 

- Qiushan Guo, Shalini De Mello, Hongxu Yin, Wonmin Byeon, Ka Chun Cheung, Yizhou Yu, Ping Luo, and Sifei Liu. Regiongpt: Towards region understanding vision language model. In _CVPR_ , pp. 13796–13806, 2024. 

- Zebin Han, Xudong Wang, Baichen Liu, Qi Lyu, Zhenduo Shang, Jiahua Dong, Lianqing Liu, and Zhi Han. Seqwalker: Sequential-horizon vision-and-language navigation with hierarchical planning. _arXiv preprint arXiv:2601.04699_ , 2026. 

- Zhi Hou, Tianyi Zhang, Yuwen Xiong, Haonan Duan, Hengjun Pu, Ronglei Tong, Chengyang Zhao, Xizhou Zhu, Yu Qiao, Jifeng Dai, et al. Dita: Scaling diffusion transformer for generalist visionlanguage-action policy. _arXiv preprint arXiv:2503.19757_ , 2025. 

- Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. Lora: Low-rank adaptation of large language models. _ICLR_ , 1(2):3, 2022. 

- Stephen James, Zicong Ma, David Rovick Arrojo, and Andrew J Davison. Rlbench: The robot learning benchmark & learning environment. _IEEE Robotics and Automation Letters_ , 5(2):3019– 3026, 2020. 

11 

Published as a conference paper at ICLR 2026 

- Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li FeiFei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. Vima: robot manipulation with multimodal prompts. In _ICML_ , pp. 14975–15022, 2023. 

- Zhaolu Kang, Junhao Gong, Jiaxu Yan, Wanke Xia, Yian Wang, Ziwen Wang, Huaxuan Ding, Zhuo Cheng, Wenhao Cao, Zhiyuan Feng, et al. Hssbench: Benchmarking humanities and social sciences ability for multimodal large language models. _arXiv preprint arXiv:2506.03922_ , 2025. 

- Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _ICML_ , 2024. 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. _arXiv preprint arXiv:2403.12945_ , 2024. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. _arXiv preprint arXiv:2406.09246_ , 2024. 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. _arXiv preprint arXiv:2502.19645_ , 2025. 

- Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In _ICCV_ , pp. 4015–4026, 2023. 

- Hongyu Li, Liang Ding, Meng Fang, and Dacheng Tao. Revisiting catastrophic forgetting in large language model tuning. _arXiv preprint arXiv:2406.04836_ , 2024a. 

- Junxian Li, Di Zhang, Xunzhi Wang, Zeying Hao, Jingdi Lei, Qian Tan, Cai Zhou, Wei Liu, Yaotian Yang, Xinrui Xiong, et al. Chemvlm: Exploring the power of multimodal large language models in chemistry area. In _AAAI_ , pp. 415–423, 2025a. 

- Xiang Li, Cristina Mata, Jongwoo Park, Kumara Kahatapitiya, Yoo Sung Jang, Jinghuan Shang, Kanchana Ranasinghe, Ryan Burgert, Mu Cai, Yong Jae Lee, and Michael S. Ryoo. Llara: Supercharging robot learning data for vision-language policy. In _ICLR_ , 2025b. 

- Xiaoqi Li, Mingxu Zhang, Yiran Geng, Haoran Geng, Yuxing Long, Yan Shen, Renrui Zhang, Jiaming Liu, and Hao Dong. Manipllm: Embodied multimodal large language model for objectcentric robotic manipulation. In _CVPR_ , pp. 18061–18070, 2024b. 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. _arXiv preprint arXiv:2405.05941_ , 2024c. 

- Yanbang Li, Ziyang Gong, Haoyang Li, Xiaoqi Huang, Haolan Kang, Guangping Bai, and Xianzheng Ma. Robotic visual instruction. In _CVPR_ , pp. 12155–12165, 2025c. 

- Yuqi Li, Junhao Dong, Chuanguang Yang, Shiping Wen, Piotr Koniusz, Tingwen Huang, Yingli Tian, and Yew-Soon Ong. Mmt-ard: Multimodal multi-teacher adversarial distillation for robust vision-language models. _arXiv preprint arXiv:2511.17448_ , 2025d. 

- Yuqi Li, Siwei Meng, Chuanguang Yang, Weilun Feng, Junming Liu, Zhulin An, Yikai Wang, and Yingli Tian. A comprehensive survey of interaction techniques in 3d scene generation. _Authorea Preprints_ , 2026. 

- Wenqi Liang, Gan Sun, Yao He, Yu Ren, Jiahua Dong, and Yang Cong. Never-ending behaviorcloning agent for robotic manipulation. _arXiv preprint arXiv:2403.00336_ , 2024. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. _NeurIPS_ , 36:44776–44791, 2023a. 

12 

Published as a conference paper at ICLR 2026 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _NeurIPS_ , 36:34892–34916, 2023b. 

- Huaping Liu, Xinghang Li, Peiyan Li, Minghuan Liu, Dong Wang, Jirong Liu, Bingyi Kang, Xiao Ma, Tao Kong, and Hanbo Zhang. Towards generalist robot policies: What matters in building vision-language-action models. _arXiv preprint arXiv:2412.14058_ , 2025. 

- Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Qing Jiang, Chunyuan Li, Jianwei Yang, Hang Su, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. In _ECCV_ , pp. 38–55. Springer, 2024a. 

- Yuejiang Liu, Jubayer Ibn Hamid, Annie Xie, Yoonho Lee, Maximilian Du, and Chelsea Finn. Bidirectional decoding: Improving action chunking via closed-loop resampling. _arXiv preprint arXiv:2408.17355_ , 2024b. 

- Chuofan Ma, Yi Jiang, Jiannan Wu, Zehuan Yuan, and Xiaojuan Qi. Groma: Localized visual tokenization for grounding multimodal large language models. In _ECCV_ , pp. 417–435. Springer, 2024. 

- Maxime Oquab, Timoth´ee Darcet, Th´eo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. _arXiv preprint arXiv:2304.07193_ , 2023. 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _ICRA_ , pp. 6892–6903. IEEE, 2024. 

- Delin Qu, Haoming Song, Qizhi Chen, Yuanqi Yao, Xinyi Ye, Yan Ding, Zhigang Wang, JiaYuan Gu, Bin Zhao, Dong Wang, et al. Spatialvla: Exploring spatial representations for visuallanguage-action model. _arXiv preprint arXiv:2501.15830_ , 2025. 

- Kanchana Ranasinghe, Satya Narayan Shukla, Omid Poursaeed, Michael S Ryoo, and Tsung-Yu Lin. Learning to localize objects improves spatial reasoning in visual-llms. In _CVPR_ , pp. 12977– 12987, 2024. 

- Hanoona Rasheed, Muhammad Maaz, Sahal Shaji, Abdelrahman Shaker, Salman Khan, Hisham Cholakkal, Rao M Anwer, Eric Xing, Ming-Hsuan Yang, and Fahad S Khan. Glamm: Pixel grounding large multimodal model. In _CVPR_ , pp. 13009–13018, 2024. 

- Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman R¨adle, Chloe Rolland, Laura Gustafson, et al. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ , 2024. 

- Zhongwei Ren, Zhicheng Huang, Yunchao Wei, Yao Zhao, Dongmei Fu, Jiashi Feng, and Xiaojie Jin. Pixellm: Pixel reasoning with large multimodal model. In _CVPR_ , pp. 26374–26383, 2024. 

- Hao Shi, Bin Xie, Yingfei Liu, Lin Sun, Fengrong Liu, Tiancai Wang, Erjin Zhou, Haoqiang Fan, Xiangyu Zhang, and Gao Huang. Memoryvla: Perceptual-cognitive memory in vision-languageaction models for robotic manipulation. _arXiv preprint arXiv:2508.19236_ , 2025. 

- Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

13 

Published as a conference paper at ICLR 2026 

- Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe HansenEstruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _CoRL_ , pp. 1723–1736. PMLR, 2023. 

- Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. _NeurIPS_ , 37:124420–124450, 2024. 

- Xudong Wang, Jiahua Dong, Baichen Liu, Qi Lyu, Lianqing Liu, and Zhi Han. Lifelong embodied navigation learning. In _ICLR_ , 2026a. 

- Xudong Wang, Gan Li, Zhiyu Liu, Yao Wang, Lianqing Liu, and Zhi Han. All-day multi-scenes lifelong vision-and-language navigation with tucker adaptation. In _ICLR_ , 2026b. 

- Jiannan Wu, Muyan Zhong, Sen Xing, Zeqiang Lai, Zhaoyang Liu, Zhe Chen, Wenhai Wang, Xizhou Zhu, Lewei Lu, Tong Lu, et al. Visionllm v2: An end-to-end generalist multimodal large language model for hundreds of vision-language tasks. _NeurIPS_ , 37:69925–69975, 2024a. 

- Junda Wu, Zhehao Zhang, Yu Xia, Xintong Li, Zhaoyang Xia, Aaron Chang, Tong Yu, Sungchul Kim, Ryan A Rossi, Ruiyi Zhang, et al. Visual prompting in multimodal large language models: A survey. _arXiv preprint arXiv:2409.15310_ , 2024b. 

- Kun Wu, Chengkai Hou, Jiaming Liu, Zhengping Che, Xiaozhu Ju, Zhuqin Yang, Meng Li, Yinuo Zhao, Zhiyuan Xu, Guang Yang, et al. Robomind: Benchmark on multi-embodiment intelligence normative data for robot manipulation. _arXiv preprint arXiv:2412.13877_ , 2024c. 

- Shuai Yang, Hao Li, Yilun Chen, Bin Wang, Yang Tian, Tai Wang, Hanqing Wang, Feng Zhao, Yiyi Liao, and Jiangmiao Pang. Instructvla: Vision-language-action instruction tuning from understanding to manipulation. _arXiv preprint arXiv:2507.17520_ , 2025. 

- Haoxuan You, Haotian Zhang, Zhe Gan, Xianzhi Du, Bowen Zhang, Zirui Wang, Liangliang Cao, Shih-Fu Chang, and Yinfei Yang. Ferret: Refer and ground anything anywhere at any granularity. _arXiv preprint arXiv:2310.07704_ , 2023. 

- Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. _arXiv preprint arXiv:2407.08693_ , 2024. 

- Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. Sigmoid loss for language image pre-training. In _ICCV_ , pp. 11975–11986, 2023. 

- Ao Zhang, Hao Fei, Yuan Yao, Wei Ji, Li Li, Zhiyuan Liu, and Tat-Seng Chua. Vpgtrans: Transfer visual prompt generator across llms. _NeurIPS_ , 36:20299–20319, 2023. 

- Haotian Zhang, Haoxuan You, Philipp Dufter, Bowen Zhang, Chen Chen, Hong-You Chen, Tsu-Jui Fu, William Yang Wang, Shih-Fu Chang, Zhe Gan, et al. Ferret-v2: An improved baseline for referring and grounding with large language models. _arXiv preprint arXiv:2404.07973_ , 2024a. 

- Tao Zhang, Xiangtai Li, Hao Fei, Haobo Yuan, Shengqiong Wu, Shunping Ji, Chen Change Loy, and Shuicheng Yan. Omg-llava: Bridging image-level, object-level, pixel-level reasoning and understanding. _NeurIPS_ , 37:71737–71767, 2024b. 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for visionlanguage-action models. In _CVPR_ , pp. 1702–1713, 2025. 

- Tony Z Zhao, Vikash Kumar, Sergey Levine, and Chelsea Finn. Learning fine-grained bimanual manipulation with low-cost hardware. _arXiv preprint arXiv:2304.13705_ , 2023. 

- Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daum´e III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. _arXiv preprint arXiv:2412.10345_ , 2024. 

- Deyao Zhu, Jun Chen, Xiaoqian Shen, Xiang Li, and Mohamed Elhoseiny. Minigpt-4: Enhancing vision-language understanding with advanced large language models. _arXiv preprint arXiv:2304.10592_ , 2023. 

14 

Published as a conference paper at ICLR 2026 

## A APPENDIX 

This supplemental material introduces additional details not mentioned in the main paper. Overall, it mainly includes the following aspects: 

- **(1)** Details of Pixel-160K dataset in Sec. A.1. 

- **(2)** More experiment setup in Sec. A.2. 

- **(3)** More implementation details in Sec. A.3. 

- **(4)** More qualitative comaprisons in Sec. A.4. 

- **(5)** Limitations in Sec. A.5. 


Figure 5: The episode example in our Pixel-160K dataset. 

### A.1 PIXEL-160K DATASET 

This section provides a detailed description of the Pixel-160K dataset and the proposed automated annotation pipeline. In contrast to existing robot datasets composed of image-level and text instructions, Pixel-160K offers fine-grained pixel-level annotations and supports both textual and visual prompts, aiming to train VLAs for more precise pixel-level spatial understanding and diversified human–robot interaction. Pixel-160K comprises 160K robot manipulation episodes and 6.5M image–text–action triplets enriched with visual prompts and mask annotations. Specifically, for the _i_ -th episode **E** _i_ in Pixel-160K dataset, **E** _i_ = _{_ **X** _i,_ **A** _i,_ **P** _i,_ **L** _i,_ **V** _i}_ , where **X** _i_ = _{_ **x**<sup>_t_</sup> _i_<sup>_}_</sup> _t_<sup>_T_</sup> =1<sup>,</sup> **P** _i_ = _{_ **p**<sup>_t_</sup> _i_<sup>_}_</sup> _t_<sup>_T_</sup> =1<sup>,</sup><sup>**A**</sup><sup>_i_=</sup><sup>_{_</sup><sup>**a**</sup><sup>_t_</sup> _i_<sup>_}_</sup> _t_<sup>_T_</sup> =1<sup>.</sup> As shown in Fig. 5, to effectively inject the pixel-level annotations and visual masks, we reformulate the textual instruction– _What should the robot do to {</instruction>}_ as _What should the robot do to {</instruction>}, refer to {</annotations>} {</visual prompts>}_ . Here, _<_ / _· >_ a placeholder and is subsequently replaced with the language embeddings, the pixel-aware embeddings and the prompt-aware embeddings. 

As illustrated in Fig. 6(a), the proposed automated annotation pipeline consists of two sequential stages: (a) Gripper-aware Region Proposal Stage and (b) Multimodal Object Segmentation Stage. The gripper-aware region proposal stage consists of four steps: 

**1. Gripper-close State Extraction** : For each manipulation episode, we parse the robotic state sequence ∆ _x,_ ∆ _θ,_ ∆Grip. Frames in which the gripper state ∆Grip = 1 are identified as gripperclose states, indicating that the gripper is interacting with an object. The first frame in each episode is selected as the key observation **x**<sup>_G_</sup> _η_<sup>_η_, representing the earliest moment of potential object contact.</sup> 

> <sup>_G_</sup> _η_<sup>_η_, representing the earliest moment of potential object contact.</sup> 

**2. Discrete Video Composition** : We collect the gripper-close observations from all episodes, _i.e._ , _{_ **x**<sup>_G_</sup> 1<sup>1</sup><sup>_,_</sup><sup>**x**</sup><sup>_G_</sup> 2<sup>2</sup><sup>_, . . . ,_</sup><sup>**x**</sup> _N_<sup>_GNe_</sup> _e_<sup>_}_, where</sup><sup>_Ne_is the total number of episodes.These frames are then organized</sup> 

15 

Published as a conference paper at ICLR 2026 


Figure 6: The proposed automated annotation pipeline for generating visual prompts and mask annotations at scale for a given robot dataset, consisting of a gripper-aware region proposal stage and a multimodal object segmentation stage. 

into a discrete video set that captures diverse gripper-object interaction states across the dataset, providing compact yet informative cues for region localization. 

**3. Gripper Detection** : To precisely localize the gripper within the selected frames, we apply SAM 2 (Ravi et al. (2024)). The model segments the gripper region from each observation, producing bounding boxes tightly enclosing the gripper. These gripper regions serve as reliable anchors, as the manipulated objects typically appear adjacent to or in contact with the gripper. 

**4. Region Proposals Generation** : Finally, we crop the localized gripper regions from the initial observations to form region proposals **R** 1 _,_ **R** 2 _, . . . ,_ **R** _Ne_ , with each **R** _η ∈_ R<sup>4</sup> denoting a bounding box for the _η_ -th episode. These proposals effectively filter out irrelevant background clutter and highlight the object-relevant areas, thereby facilitating accurate segmentation in the subsequent multimodal object segmentation stage. 

As illustrated in Fig. 6(b), the multimodal object segmentation stage consists of two steps: 

**5. Target Object Reasoning** : Given a manipulation instruction, such as “Pick the vessel and place it on the blue cloth” or “Move the red fork to the left side of the stove”, we employ a large language model (LLM) to parse the instruction and extract the target object to be manipulated. The LLM identifies the first object the robot needs to grasp and outputs its textual description ( _e.g._ , “vessel” or “the red fork”). This reasoning step transforms natural-language task instructions into precise object queries, enabling alignment between language and perception. 

**6. Annotations Generation** : For the _η_ -th episode, we feed the target object text together with the region proposal **R** _η_ into an open-vocabulary detection and segmentation pipeline comprising Grounding DINO (Liu et al. (2024a)) and SAM (Kirillov et al. (2023)). Grounding DINO detects candidate object bounding boxes conditioned on the target object text, grounding the language query into specific image regions. Subsequently, SAM refines these detections by generating pixel-level segmentation masks for the grounded boxes. The outputs include bounding boxes, segmentation masks, and text-object alignments. We then filter the results by selecting the mask with the highest confidence score within the region proposal, discarding low-confidence or irrelevant detections. Finally, from the retained object mask, we derive visual prompts by: randomly sampling points inside the mask, generating random lines within the object area, and extracting external bounding boxes via contour detection. 

### A.2 EXPERIMENT SETUP 

**Evaluation tasks** . As shown in Fig. 7, we conduct all experiments on three simulation benchmarks, _i.e._ , SimplerEnv-Google Robot (Li et al. (2024c)), SimplerEnv-WidowX (Li et al. (2024c)) and LIBERO (Liu et al. (2023a)). Specifically, SimplerEnv Li et al. (2024c) is an open-source simulation suite designed for reproducible and scalable evaluation of robot manipulation policies. It explicitly 

16 

Published as a conference paper at ICLR 2026 


Figure 7: Experimental Setup Overview. We evaluate PixelVLA on three simulation benchmarks: SimpleEnv-WidowX with WidowX robot, SimpleEnv-Google Robot with Google robot, and LIBERO with Franka. 

addresses the visual and dynamic gaps between simulation and real hardware, enabling more faithful assessments of policy generalization. SimplerEnv provides two complementary evaluation settings: Visual Matching (VM), which minimizes visual appearance discrepancies to improve the correlation between simulation and real-world performance; and Variant Aggregation (VA), which, inspired by domain randomization, introduces diverse visual perturbations and aggregates results across multiple randomized environments to obtain more robust performance estimates. Building on these capabilities, we perform zero-shot object manipulation experiments on SimplerEnv to benchmark the effectiveness of our approach. 

As shown in Fig. 7, LIBERO (Liu et al. (2023a)) is a comprehensive benchmark suite designed to evaluate continual adaptation and generalization in robot manipulation. It consists of multiple task suites that focus on different aspects of knowledge transfer: LIBERO-Spatial, which requires learning new spatial relationships between identical objects; LIBERO-Object, which involves recognizing and manipulating novel object types; and LIBERO-Goal, which evaluates the ability to adapt to new task goals given the same objects and spatial layouts. Additionally, LIBERO-Long extends the challenge to long-horizon tasks, testing a robot’s capacity for compositional reasoning and extended action planning. Together, these task suites provide a systematic framework for studying declarative knowledge (spatial and object-level) and knowledge (goal-oriented behaviors) in robot learning. 

### A.3 IMPLEMENTATION DETAILS 

**Training** . In the first stage of continuous action training, we initialize PixelVLA’s vision encoder, MLP projector, and LLM backbone with pretrained weights from VLAs (Kim et al. (2024); Black et al. (2024)), which were trained on the large-scale OXE dataset (O’Neill et al. (2024)). To focus on learning continuous action mappings, the visual prompt-aware encoder and the multiscale pixelaware encoder are removed, while all other modules except the continuous action decoder are frozen to preserve general manipulation knowledge. The continuous action decoder maps the final hidden states of the LLM to continuous action values. We use L1 regression (Zhao et al. (2023); Kim et al. (2025)) to align the predicted actions with ground-truth actions. Each continuous action dimension is uniformly discretized into 256 bins and normalized to [ _−_ 1 _,_ +1] for fine-grained prediction. The input observation consists of a single third-person camera view resized to 224 _×_ 224 pixels. Actions are predicted in chunks of 8 timesteps, with **a**<sup>**t**</sup> _∈_ R<sup>8</sup><sup>_×_7</sup> . During this stage, PixelVLA is trained on a mixture of Fractal (Brohan et al. (2022)) and Bridge v2 (Walke et al. (2023)) datasets. Training runs for 100k steps with a batch size of 32 and a learning rate of 5 _×_ 10<sup>_−_4</sup> . This stage is omitted when adapting PixelVLA to _π_ 0 due to the effectiveness of its pretrained action expert. 

In Pixel-level Understanding Enhancement Stage, PixelVLA is fine-tuned for pixel-level understanding using the Pixel-160K dataset. The visual prompt-aware encoder and multiscale pixel-aware encoder are jointly trained, while LoRA adaptation is applied to the LLM backbone (rank _r_ = 32). All other modules remain frozen except the continuous action decoder, which is optimized using L1 regression, following the same continuous action representation as in the first stage. Input observations are a single third-person camera view resized to 224 _×_ 224 pixels. Actions are predicted in chunks of 8 timesteps, **a**<sup>**t**</sup> _∈_ R<sup>8</sup><sup>_×_7</sup> . Training runs for 200k steps with a batch size of 32 and a 

17 

Published as a conference paper at ICLR 2026 

Table 5: SimplerEnv (Li et al. (2024c)) simulation evaluation results in terms of the average success rate for the Google Robot setup. VM denotes Visual Matching and VA is Variant Aggregation. ■ denotes tuning-based methods applied to the pretrained weights of OpenVLA. 

||Methods|Horizontal|Pick Co<br> Vertical|ke Can<br> Standing|**Average**|Move Near<br>**Average**|Ope<br>Open|n/Close<br> Close|Drawer<br> **Average**|**Average**|
|---|---|---|---|---|---|---|---|---|---|---|
||RT-1-X (O’Neill et al.(2024))|82.0|33.0|55.0|56.7|31.7|29.6|89.1|59.7|53.4|
||Octo-Base (Team et al.(2024))|21.0|21.0|9.0|17.0|4.2|0.9|44.4|22.7|16.8|
|VM|HPT (Wang et al.(2024))|–|–|–|56.0|60.0|–|–|24.0|46.0|
||RoboVLMs (Liu et al.(2025))|85.0|43.0|90.0|72.7|66.3|28.7|25.0|26.8|56.3|
||SpatialVLA (Qu et al.(2025))|70.0|82.0|91.0|81.0|69.6|49.1|69.4|59.3|71.9|
||OpenVLA (Kim et al.(2024))|27.0|3.0|19.0|16.3|46.2|19.4|51.8|35.6|27.7|
||TraceVLA (Zheng et al.(2024))|–|–|–|28.0|53.7|–|–|57.0|42.0|
||**PixelVLA**|90.9|63.6|90.9|81.7|60.1|25.3|59.3|42.3|65.0|
||RT-1-X (O’Neill et al.(2024))|56.9|20.4|69.8|49.0|32.3|6.9|51.9|29.4|39.6|
||Octo-Base (Team et al.(2024))|0.5|0.0|1.3|0.6|3.1|0.0|2.1|1.1|1.1|
|VA|HPT (Wang et al.(2024))|–|–|60.0|–|–|–|–|–|–|
||RoboVLMs (Liu et al.(2025))|77.8|48.0|79.1|68.3|56.0|1.6|15.3|8.5|46.3|
||SpatialVLA (Qu et al.(2025))|93.3|83.1|92.0|89.5|71.7|23.3|49.2|36.2|68.8|
||OpenVLA (Kim et al.(2024))|71.1|27.1|65.3|54.5|47.7|15.8|19.5|17.7|39.8|
||TraceVLA (Zheng et al.(2024))|–|–|–|60.0|56.4|–|–|31.0|45.0|
||**PixelVLA**|81.8|54.5|81.8|72.7|57.7|22.8|16.4|20.0|52.6|


learning rate of 1 _×_ 10<sup>_−_3</sup> , enhancing PixelVLA’s ability to localize and manipulate target objects at the pixel level. 

**Inference** . During inference, the user only needs to provide a semantic instruction along with visual prompts in the initial observation. Subsequently, we incorporate FastSAM to predict the mask annotation of the target object based on the given visual prompts. This introduces an additional computational overhead of approximately 1% of the overall model inference cost, resulting in a negligible impact on inference efficiency. 

### A.4 QUALITATIVE COMPARISONS 

As shown in Tab. 5, this section presents the evaluation results of the simpler environment on the Google Robotics benchmark, which includes tasks such as Coke can manipulation (horizontal, vertical and standing picking) and drawer operations (open and close). PixelVLA demonstrates exceptional performance, achieving an average VM score of 65.0, significantly outperforming OpenVLA (27.7) and TraceVLA (42.0). In the VA category, PixelVLA achieves an average score of 52.6, again surpassing OpenVLA (39.8) and TraceVLA (45.0). These results indicate that PixelVLA outperforms its counterparts in both pixel-level understanding and the adaptation to visual prompts, showcasing a remarkable capacity for generalist manipulation across the evaluated tasks. The significant margins in performance metrics underscore the effectiveness of the proposed method in addressing out-of-domain generalization challenges. 

### A.5 LIMITATIONS 

Although PixelVLA substantially improves VLA performance through pixel-level understanding and tailored visual prompts, it remains limited in handling richer input modalities (e.g., 3D perception) and more advanced forms of visual prompting, such as precise trajectory guidance, referenceimage prompts, pose-conditioned prompts, or compositional prompt sequences. In addition, while PixelVLA is extensively validated across three simulated benchmarks, we expect that real-world robot experiments would further strengthen its contributions. We regard these extensions as important directions for future work. 

18 

