---
title: "From Seeing to Doing: Bridging Reasoning and Decision for Robotic Manipulation"
date: "2025-05-13"
authors: "Yifu Yuan; Haiqin Cui; Yibin Chen; Zibin Dong; Fei Ni; Longxin Kou"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2505.08548
pdf: https://arxiv.org/pdf/2505.08548
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.08548)** / [論文ページ](https://arxiv.org/abs/2505.08548)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

# **From Seeing to Doing: Bridging Reasoning and Decision for Robotic Manipulation** 

**Yifu Yuan**<sup>**1**</sup> , **Haiqin Cui**<sup>**1,†**</sup> , **Yibin Chen**<sup>**1,†**</sup> , **Zibin Dong**<sup>**1**</sup> , **Fei Ni**<sup>**1**</sup> , **Longxin Kou**<sup>**1**</sup> , **Jinyi Liu**<sup>**1**</sup> , **Pengyi Li**<sup>**1**</sup> , **Yan Zheng**<sup>**1**</sup> , **Jianye Hao**<sup>**1**</sup> 

1Tianjin University 

†Equal Contribution 

Corresponding author(s): Jianye Hao; Email jianye.hao@tju.edu.cn 

Achieving generalization in robotic manipulation remains a critical challenge, particularly for unseen scenarios and novel tasks. Current Vision-Language-Action (VLA) models, while building on top of general Vision-Language Models (VLMs), still fall short of achieving robust zero-shot performance due to the scarcity and heterogeneity prevalent in embodied datasets. To address these limitations, we propose **FSD** ( _From Seeing to Doing_ ), a novel vision-language model that generates intermediate representations through spatial relationship reasoning, providing fine-grained guidance for robotic manipulation. Our approach combines a hierarchical data construction pipeline for training with a self-consistency mechanism that aligns spatial coordinates with visual signals. Through extensive experiments, we comprehensively validated FSD’s capabilities in both “ _seeing_ ” and “ _doing_ ”, achieving outstanding performance across 8 benchmarks for general spatial reasoning and embodied reference abilities, as well as on our proposed more challenging benchmark **VABench** . We also verified zero-shot capabilities in robot manipulation, demonstrating significant performance improvements over baseline methods in both SimplerEnv and real robot settings. Experimental results show that FSD achieves 40.6% success rate in SimplerEnv and 72% success rate across 8 real-world tasks, outperforming the strongest baseline by 30%. More visualizations and datasets are available on website. 

� **Projects:** https://embodied-fsd.github.io/ Codehttps://github.com/pickxiguapi/Embodied-FSD Datasetshttps://huggingface.co/collections/IffYuan/fsd � **Contact:** yuanyf@tju.edu.cn **Published as a conference paper at ICLR 2026** 


## **1 Introduction** 

A driving force behind robotics research is the pursuit of generalization: creating agents capable of versatile action across diverse robotic platforms, extending beyond familiar tasks, objects, and environments while adapting to dynamic visual inputs. Current approaches Kim et al. (2024); Brohan et al. (2023) leverage pretrained Vision-Language Models (VLMs) and transform them into Vision-Language-Action Models (VLAs) using large-scale embodied datasets. This enables systems to interpret natural language instructions and generate robotic manipulation actions Black et al. (2024). The intention is to capitalize on the generalization capabilities of VLMs pre-trained on internet-scale data, with the hope that resulting VLAs will adapt to novel scenarios involving unseen objects and tasks. However, empirical evidence Zheng et al. (2024); Zawalski et al. (2024); Liu et al. (2024d) demonstrates that directly applying the generalization power of VLMs falls short of achieving strong zero-shot performance on completely novel tasks. 

1 


**Figure 1 Overview of FSD** . FSD unlocks visual aids reasoning and generation through Spatial Relationship Focused CoT, demonstrating exceptional generalization capabilities that enable zero-shot robot manipulation and achieving remarkable performance across multiple benchmarks. 

We attribute the limited generalization in VLA-based systems to _scarcity_ and _heterogeneity_ of datasets. Robotics data remains limited compared to language and vision datasets, preventing similar scaling laws Kaplan et al. (2020); Lin et al. (2024a). Despite growth in embodied datasets O’Neill et al. (2023), their insufficient coverage and diversity prevent robust zero-shot generalization. Additionally, robotic embodiment heterogeneity Wang et al. (2024) causes significant variation in VLA outputs, making endto-end supervised learning from vision and language to diverse action outputs a potentially unrealistic path toward generalization. 

We present a novel pipeline addressing generalization challenges in robotic manipulation. Our approach leverages VLMs’ visual understanding capabilities, augmented with step-by-step reasoning to extract unified mid-level structural representations independent of robot embodiment. This representation is key to generalizing learning across diverse physical interactions and dynamic behaviors. Specifically, this mid-level representation includes spatial affordance boxes/points and visual traces, each represented as marked coordinates within visual images. These visual aids provide expressive yet compact spatial information that enables effective reasoning and decisions, overcoming both scarcity and heterogeneity limitations. We introduce **FSD** ( **_F_** _rom_ **_S_** _eeing to_ **_D_** _oing_ ), a model that generates visual intermediate representations through spatial reasoning (figure 1). FSD comprises three key components: (1) Spatial Relationship-Focused Visual Chain-of-Thought ( **SrCoT** ), which conducts multi-step reasoning anchored by object coordinates and spatial relationships, treating visual aid generation as a reasoning process; (2) A hierarchical data construction pipeline combining large-scale embodied datasets with common sense data, establishing a weak-to-strong capability enhancement training process; and (3) A self-consistency mechanism that aligns understanding and generation by binding spatial coordinates with specific visual signals. To evaluate the accuracy and generalization ability of visual aids generated in complex scenes, we also manually annotated 300 images from both real-world and simulation tasks across various scenarios, 

2 

forming a **V** isual **A** ids Generation Benchmark ( **VABench** ). Through carefully crafted training and evaluation methods, FSD can achieve precise generation of visual aids in different scenarios, then the robot follows spatial affordances and visual traces through simple planning methods to complete action execution. 

FSD generalizes effectively to new instructions, and scenes through enhanced reasoning abilities. Our contributions include: (1) A novel paradigm bridging VLM reasoning with embodied decisions via visual aids; (2) The SrCoT method enabling multi-step reasoning for visual aid generation and guiding zero-shot manipulation; (3) Our weak-to-strong spatial reasoning and visual aids datasets, along with VABench, a manually annotated challenging benchmark for visual aids generation; (4) Superior performance across 8 benchmarks in spatial reasoning, free space reference, and visual aids generation, with zero-shot deployment achieving 40.6% success in SimplerEnv and 72% in 8 real-world tasks, outperforming RoboPoint baseline by 30%. 

## **2 Related Work** 

**Spatial Understanding and Reasoning with VLMs** Spatial understanding and reasoning Liu et al. (2023b); Song et al. (2024); Du et al. (2024); Liao et al. (2024); Ray et al. (2024) require VLMs to infer spatial information beyond 2D RGB images, a capability crucial for embodied AI applications such as navigation Song et al. (2024); Hong et al. (2023); Li et al. (2024b) and manipulation Yuan et al. (2024b). Recent advances include SpatialVLM Chen et al. (2024), which explicitly incorporates spatial primitives and coordinate systems to enhance geometric reasoning capabilities. Similarly, SpatialRGPT Cheng et al. (2024) and SpatialBot Cai et al. (2024) improve spatial capabilities through more precise spatial relationship modeling. FSD specifically targets embodied manipulation scenarios by enhancing spatial reasoning capabilities through novel SrCoT mechanisms and sophisticated self-consistency alignment techniques. 

**Visual Chain-of-thought Reasoning** The integration of Chain-of-thought (CoT) Wei et al. (2022) and its variants Zhang et al. (2022); Yao et al. (2023b, 2024) has significantly enhanced LLM reasoning abilities through structured step-by-step processes. For the multimodal reasoning challenge, researchers have developed various CoT approaches Mitra et al. (2024); Zheng et al. (2023a); Yao et al. (2023a); Wu et al. (2025) that establish appropriate reasoning anchors and extend reasoning pathways. Shikra Chen et al. (2023) improves referential expression by incorporating specific visual regions into the reasoning process, while VoCoT Li et al. (2024e) extends visually-grounded reasoning chains. VisualCoT Shao et al. (2024) provides a comprehensive benchmark validating CoT effectiveness in multi-hop image reasoning tasks. EmbodiedCoT Zawalski et al. (2024) pioneered CoT application in embodied AI by enhancing intermediate reasoning through fine-tuning OpenVLA Kim et al. (2024). In contrast, FSD uniquely integrates visual-spatial reasoning using spatial relationship graphs as reasoning anchors. 

**Visual Aids Empowered Robotic Manipulation** Extracting embodiment-agnostic visual aids to enhance training efficiency has emerged as a promising paradigm in robotic manipulation. Numerous studies Bharadhwaj et al. (2024); Wen et al. (2023); Xu et al. (2024); Zheng et al. (2024); Yuan et al. (2024a) have explored robotic policy learning based on visual traces, though most remain confined to specific tasks with cross-embodiment applicability. LLaRVA Niu et al. (2024) advances this field by predicting visual traces to better align visual and action spaces for robot learning, compiling an impressive large visual trace dataset, yet struggles to generalize to novel downstream tasks without task-specific fine-tuning. Spatial affordance represents another effective visual aid, with several works Yuan et al. (2024b); Mo et al. (2021); Qin et al. (2020); Song et al. (2024); Ji et al. (2025); Yang et al. (2025); Li et al. (2025) demonstrating its utility in robotic manipulation tasks. Our key insight is that the scarcity 

3 

of embodied data fundamentally limits purely data-driven visual aid prediction approaches, impeding zero-shot generalization to unseen scenarios. Therefore, we employ a reasoning-driven paradigm to activate general spatial abilities and enhance generalization. 

## **3 Bridging Reasoning and Decision through Visual Aids Generation** 

To harness VLMs’ visual perception capabilities for cross-domain generalization, we introduce **FSD** ( _From Seeing to Doing_ )—a model exhibiting robust spatial reasoning and generation abilities. We first establish visual aids through spatial affordances and visual traces, then develop Spatial Relationship-Focused CoT (SrCoT), which leverages object-centric coordinates and their spatial relationships as reasoning anchors. Supporting this approach requires precise spatial understanding and complex instructionfollowing capabilities to generate coordinate representations. We implement a progressive weak-to-strong data construction pipeline across five capability levels, complemented by a self-consistency alignment mechanism that enhances understanding and generation abilities. 

### **3.1 Definition of Visual Aids** 

As shown in figure 2, FSD utilizes three visual aids of increasing complexity, all defined within normalized image coordinates **_𝑥_** = ( _𝑝_ , _𝑞_ ) _∈_ [0, 1000]<sup>2</sup> _⊂_ **R**<sup>2</sup> : **Spatial affordance boxes** _ℬ_ = [ _𝑥_ 1, _𝑦_ 1, _𝑥_ 2, _𝑦_ 2] define target regions for object placement. For instructions like " _Put the sushi into the silver pot_ ," the model must infer coordinates for unmarked free space—beyond standard detector capabilities. **Spatial affordance points** _𝒫_ = _{_ ( _𝑥𝑖_ , _𝑦𝑖_ ) _| 𝑖_ = 1, 2, ..., _𝑛}_ provide more precise and flexible placement with reduced redun- 


**Figure 2** Diagrams of Visual Aid Types 

dancy. **Object-centric visual traces** **_𝜏_** = _{_ **_𝑥_** _𝑡 | 𝑡_ = 1, 2, ..., _𝑇 }_ represent ordered coordinate sequences that describe manipulation trajectories, where _𝑇_ denotes the sequence length. These traces enable complex instruction execution, cross-embodiment transfer, and collision avoidance. We implement these representations in 2D rather than 3D due to limited high-quality 3D data availability Zhang et al. (2024). Our object-centric rather than agent-centric visual aids approach effectively circumvents the limitations of heterogeneous embodied data while leveraging general visual datasets without robots, thus enabling robust generalization to novel scenarios and tasks. 

### **3.2 Spatial Relationship-Focused Visual Chain-of-thought** 

To enable VLMs to generate spatial visual aids, a direct approach is supervised fine-tuning Niu et al. (2024); Yuan et al. (2024b); Li et al. (2024c); Zawalski et al. (2024) using these aids as a new action space or employing generative models Shridhar et al. (2024); Xu et al. (2024). However, the heterogeneity and scarcity of embodied datasets limit this method. Directly aligning RGB images with coordinate points is challenging and prone to overfitting, hindering generalization. _How can we stimulate VLMs’ spatial reasoning abilities to guide the generation rather than merely relying on extensive demonstrations?_ Inspired by human cognition (figure 3 (Top)), when executing tasks like "putting broccoli into a pot," humans first locate relevant objects, then plan movement paths based on relative positions while considering feasibility and obstacles. During this process, humans construct reasoning chains, repeatedly referencing object positions and establishing spatial relationships. 

4 


**Figure 3** Inspired by the process of human reasoning, FSD uses a spatial relationship graph as an anchor to derive a visual chain-of-thought reasoning process for visual trace generation. 

Based on these considerations, we introduce Spatial Relationship-Focused Visual Chain-of-thought (SrCoT). This approach guides VLMs to generate visual aids through structured reasoning based on spatial relationship graphs. SrCoT consists of two essential phases: 1 **Description** : We generate object-centric region captions establishing a task-relevant spatial relationship graph where nodes represent objects with their coordinates and edges denote relative relationships (above, below, left, right, etc.). 2 **Reasoning** : Using the spatial relationship graph as anchor points, we determine start and end coordinates through object references and free space reasoning, then iteratively derive intermediate points with explicit logical connections between steps. Thus, we prescribe a templated reasoning path for VLMs, enabling FSD to perform analogical reasoning in the spatial domain. While VLMs struggle to directly map future actions to image coordinates, our method leverages known object relationships as reference points for multi-hop analysis, simplifying the reasoning process. figure 3 (Bottom) demonstrates a complete reasoning sequence. This step-by-step SrCoT approach, though powerful, fundamentally depends on precise spatial understanding capabilities. To improve the stability and reliability of reasoning paths and reduce model hallucinations, SrCoT requires the model to generate coordinates in a specified format and bind them to objects while performing object-centric reasoning Wang et al. (2025); Li et al. (2024e). We use _<ref>_ to mark objects, and _<point>_ and _<box>_ to mark points and boxes, respectively, ensuring that each object is strictly bound to its corresponding coordinates. This explicit visual-spatial coordinate alignment enhances the FSD ’s understanding of the spatial positions and relationships of objects. All coordinates are treated as text and are discretized as integers normalized between 0 and 999. 

### **3.3 Weak-to-Strong Capability Dataset Construction Pipeline** 

The SrCoT mechanism demands enhanced capabilities from VLMs, including precise reference grounding, spatial understanding, and complex instruction-following capabilities (directly predicting future point trajectories) where mainstream VLMs Liu et al. (2024c); Lin et al. (2024b); Ray et al. (2024); Du et al. (2024) show limitations. Consequently, we designed a weak-to-strong data construction pipeline to progressively develop these abilities. 

**FSD encompasses five hierarchical capability levels:** 1 **Region Grounding** enables robots to focus on key objects in scenes. Although grounding capabilities have been broadly integrated into current 

5 


**Figure 4** FSD screens data from large-scale embodied datasets, generates ground truth spatial relationship graph. We finally collected 300K data for 10+ embodiments with 5-level capabilities. 

VLMs Chen et al. (2023); You et al. (2023), understanding various small objects and complex scenes for embodied tasks is still limited; 2 **Spatial Relationship** understanding establishes prerequisite knowledge for spatial reasoning, forming the anchor points for SrCoT; 3 **Spatial Reasoning** builds upon these foundations to perform multi-hop analysis of object positions and relationships; and finally, 4 **Spatial Affordance Generation** and 5 **Visual Trace Generation** create actionable spatial guidance. Notably, SrCoT functions as a general visual-spatial reasoning mechanism applicable beyond visual traces to diverse spatial reasoning tasks. Through hierarchical spatial capability training, we enhance VLMs’ general spatial reasoning abilities, extending well beyond just embodied domains. 

**Automatic Dataset Construction:** We leveraged extensive robot data from BridgeDataV2 Walke et al. (2023), RT-X O’Neill et al. (2023), and Droid Khazatsky et al. (2024) to construct FSD’s training dataset. Inspired by SpatialVLM Chen et al. (2024) and SpatialRGPT Cheng et al. (2024), our automated data construction pipeline created 300K Supervised Fine-Tuning (SFT) data across numerous formats. After filtering demonstrations with unclear instructions, we used GPT4o Hurst et al. (2024) to nominate task-relevant objects while excluding out-of-range or overly complex items. We then built around objects using GroundedSam Ren et al. (2024) for bounding boxes and segmentation masks ( **Level** 1 dataset). For spatial relationship labels, we reconstructed 3D semantic scene graphs using Metric3Dv2 Hu et al. (2024) for depth estimation, along with WildCamera Zhu et al. (2024) and PerspectiveFields Jin et al. (2023) for camera parameters. This enabled 2D-3D mapping and spatial relationship graph construction. ( **Level** 2 dataset). We only generate relative depth sorting data to infer positional relationships, so the accuracy requirement is not high. To improve data quality, in particular, we selected objects with a relative depth gap of 20% for subsequent generation. Afterward, we randomly sample spatial relationship graphs to construct spatial reasoning QA. We provide image captions, object coordinates, and relationships as a context for GPT4o to create complex QAs ( **Level** 3 Dataset). 

A core aspect of the FSD dataset is the visual aids generation. We employ a simple method with successful human demonstrations from embodied datasets and infer the process from the results. Spatial affordance represents the designated completion area for manipulation tasks. To create spatial affordance labels ( **Level** 4 Dataset), we extract the manipulated object’s final position from the terminal frame, combine it with reference object positioning, calculate the precise affordance region, and re-render this information onto the initial frame. For visual trace generation ( **Level** 5 Dataset), we employ a two-stage approach: first applying self-supervised keypoint extraction Huang et al. (2024) to identify grasp points 

6 

on manipulated objects, then utilizing Cotracker Karaev et al. (2024) to capture temporal dynamics from human demonstrations, subsequently projecting these trajectories onto the initial frame. Throughout this process, we employed strict rule-based filters and continually validated our approach against manually annotated test sets, iteratively refining our filtering criteria based on empirical feedback to ensure the resulting dataset met our quality requirements. The dataset presentation, data filtering process, and prompts used to generate the data are provided in section A. 

### **3.4 Self-Consistent Alignment for Spatial Understanding and Generation** 

High-quality SFT datasets enable VLMs to generate visual aids Yuan et al. (2024b), yet these models struggle to understand the physical meaning of such annotations since coordinate spaces never appeared in pretraining data. The alignment between image coordinates and actual spatial positions presents a significant challenge. Therefore, we propose a self-consistency mechanism to further align FSD capabilities in spatial understanding and generation. We frame generation tasks inversely as understanding problems: if the forward task requires inferring visual trace **_𝜏_** from an image _𝑋𝑣_ and task instruction _𝑋𝑞_ , i.e. ( _𝑋𝑣_ , _𝑋𝑞_ ) _→_ **_𝜏_** , we construct the inverse task of predicting possible instructions given an image and visual traces ( _𝑋𝑣_ , **_𝜏_** ) _→ 𝑋𝑞_ . This bidirectional approach helps the model comprehend spatial coordinates’ meanings and aligns coordinate space with image-text modalities, unifying visual aids as both understanding and generation signals while enhancing FSD spatial reasoning capabilities. 

## **4 Training and Action Execution of FSD** 

**Training:** We follow the instruction tuning pipeline proposed by LLaVA-1.5 Liu et al. (2023c, 2024c). As shown in figure 1, FSD’s architecture comprises an image encoder (CLIP-ViT-L-336px Gao et al. (2024)), a linear projector, a language tokenizer, and a LLM (Vicuna-13B Zheng et al. (2023b)). The image encoder processes images into tokens. These visual tokens are then projected into the same embedding space as language tokens through a two-layer linear projector. Only the projector and LLM weights are updated during fine-tuning while the vision encoder and tokenizer remain frozen. We built upon ASMv2 Wang et al. (2025) as our foundation, which already incorporates basic relation conversation and reference grounding capabilities. The training process of FSD is divided into two stages: **General Spatial Reasoning Enhancement** : Using data from levels 1-3, we focus on improving the model’s embodied spatial reasoning capabilities. Following Yuan et al. (2024b) and Brohan et al. (2023), we discovered that an appropriate data mixture is crucial for downstream performance. Joint training with mixed robotic and internet data ensures the model retains knowledge acquired during pre-training. Consequently, our instruction tuning utilizes a diverse 1.4M sample mixture including general visual question answering (VQA) data. This comprehensive training ensures FSD maintains robust general spatial knowledge while developing embodied capabilities. **Visual Aids Generation and Understanding** : Using data from levels 4-5 with the self-consistency mechanism, we specifically train visual aids generation and understanding abilities. FSD predicts a fixed set of 8 points for simplification when generating spatial visual traces. Additional training details and the summary of mixture datasets are provided in section B. 

**Action Execution:** FSD can reason from initial or intermediate task steps, freely selecting needed visual aids. When using bounding boxes, we sample the center as the target point; with affordance points, we directly sample one point. For visual trace execution, we first generate 2D visual traces **_𝜏_** and obtain preliminary depth information from depth cameras. Following the pinhole camera model, we employ depth-based back-projection to map these to 3D space, yielding **_𝜏_**<sup>3</sup><sup>_𝑑_</sup> = _{_ **_𝑥_**<sup>3</sup> _𝑡_<sup>_𝑑_</sup> _| 𝑡_ = 1, 2, ..., _𝑇 }_ . Next, based on the spatial position of the first point **_𝑥_** 1, we query GraspNet’s Fang et al. (2020) grasp candidates _𝐺_ to match the nearest grasp pose _𝐺_<sup>_*_</sup> . For relatively fixed scenes, we may also use predetermined 

7 

**Table 1** Performance comparison on 5 spatial reasoning benchmarks. **Bold** and underlined values show best and second-best performance among open-source models. 

|||**C**|**VBench**|||||**CRPE**|||**S**|**AT**|||**BLINK**|||**EmbSp**|**Rank**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Count|2DRel|3DDep|3DDis|Avg.|Exist.|Subj.|Pred.|Obj.|Avg.|Val|Real|Count|MV|RelDepth|SpRel|Avg.|Test||
|_Closed-source model_|_s_|||||||||||||||||||
|GPT-4V|62.4|71.1|79.8|68.3|70.4|90.6|76.7|65.1|68.5|75.2|44.8|50.7|60.8|55.6|59.7|72.7|62.2|36.1|-|
|GPT-4o|65.9|85.5|87.8|78.2|79.4|93.3|81.9|71.8|73.6|80.2|49.4|57.5|49.2|60.2|74.2|69.2|63.2|49.1|-|
|_Open-source models_||||||||||||||||||||
|LLaVA-1.5-13B|58.2|46.6|53.0|47.8|51.4|88.7|57.4|54.2|55.2|63.9|51.4|41.6|45.0|41.4|53.2|69.9|52.4|35.1|4.8|
|SAT-Dynamic-13B|61.5|**89.7**|80.7|73.0|76.2|87.5|60.6|57.6|65.2|67.7|**87.7**|54.9|35.8|44.4|**73.4**|66.4|55.0|51.3|2.8|
|RoboPoint-13B|56.5|77.2|81.5|57.7|68.2|93.2|66.3|62.4|**70.9**|73.2|53.3|46.6|48.3|44.4|62.1|65.7|55.1|51.4|2.8|
|ASMv2-13B|58.9|68.9|68.9|68.9|66.4|92.1|69.2|59.0|65.3|71.4|63.9|46.7|59.2|44.4|56.5|65.0|56.3|57.4|3.1|
|FSD-13B|**62.4**|86.5|**88.0**|**86.7**|**80.9**|**94.0**|**75.2**|**65.1**|70.4|**76.2**|73.2|**63.3**|**60.0**|**46.6**|70.2|**78.3**|**63.8**|**63.3**|**1.3**|


grasp poses. Subsequently, we optimize the path trajectory using gradient descent-based interpolation, generating complete motion trajectories in SE(3) space, enabling the robotic arm to follow the 3D visual trajectory. When using only spatial affordance, we utilize CuRobo Sundaralingam et al. (2023) as the motion planner to determine execution trajectories _𝑇_ based on the target position _𝒫_ . More details are provided in section C. Unlike methods such as LLARVA Niu et al. (2024) and EmbodiedCOT Zawalski et al. (2024) which also utilize visual auxiliary aids, FSD transforms prediction tasks into reasoning tasks, better leveraging visual-spatial common knowledge without requiring scenario-specific fine-tuning. 

## **5 Visual Aids Generation Benchmark** 

Few datasets exist for evaluating visual aid generation, Where2Place Yuan et al. (2024b) provides 100 real-world images from homes and offices but is limited to direct and simple language instructions. And no benchmarks for trajectory prediction. To address this gap, we propose the **V** isual **A** ids Generation Benchmark ( **VABench** ). we manually annotated 300 problems from real-world and simulation datasets (OXE O’Neill et al. (2023), BridgeData Walke et al. (2023), Droid Khazatsky et al. (2024) and Libero Liu et al. (2023a)), requiring models to infer visual aids given only natural language instructions similar to everyday human commands. For spatial affordance ( _VABench-Point_ ), we measure the proportion of points falling within target regions. For models that only output bounding boxes, we sample uniformly within boxes. For visual trace ( _VABench-VisualTrace_ ), we compute MAE and RMSE between ground truth **_𝜏_** = _<u>{</u>_ **_𝑥_** _𝑡_ _<u>|</u> 𝑡_ = 1, 2, ..., _𝑇 }_ and predictions **_𝜏_** ˆ = _{_ ˆ **_𝑥_** _𝑡 | 𝑡_ = 1, 2, ..., _𝑇_<sup>ˆ</sup> _}_ : MAE = _𝑇_ <u>1</u> ∑︀ _𝑇𝑡_ =1<sup>_‖_</sup><sup>**_𝑥_**</sup><sup>_𝑡−_</sup><sup>**_𝑥_**ˆ</sup><sup>_𝑡‖_,</sup> RMSE = ~~√~~ _𝑇_ <u>1 ∑</u> _𝑇𝑡_ ︀ =1<sup>_‖_</sup><sup>**_𝑥_**</sup><sup>_𝑡−_</sup><sup>**_𝑥_**ˆ</sup><sup>_𝑡‖_2.We interpolate when trajectory lengths differ and normalize coordinates</sup> to a 1000×1000 space for consistent evaluation. Since multiple valid solutions exist for each instruction, we simulated human evaluation standards by establishing detailed assessment criteria and added metrics with MLLM-based qualitative scoring (1-10) of visualized trajectories, named GPT Score. We provide detailed dataset information and evaluation procedures in section D. 

## **6 Experiments** 

We evaluated FSD across two dimensions: **_Seeing_** and **_Doing_** . For _Seeing_ , we tested its general spatial reasoning and visual aids generation capabilities. For _Doing_ , we conducted zero-shot manipulation experiments in both SimplerEnv Li et al. (2024d) simulation and real-world xArm robotic platforms to assess its practical generalization performance. 

8 


**Figure 5** FSD directly generates visual aids based on task instructions for novel tasks and scenarios. _1st_ row: affordance bounding boxes; _2nd_ row: affordance points; _3rd_ and _4th_ rows: visual traces. 

**Table 2** Performance comparison on object/free space reference benchmarks. The best results are highlighted. 

|**Benchmark**|**GPT-4o**|**SpaceLLaVA**|**LLaVA-NeXT-34B**|**SpatialBot-3B**|**ASMv2-13B**|**RoboBrain-7B**|**RoboPoint-13B**|**FSD-13B**|
|---|---|---|---|---|---|---|---|---|
|RoboRefIt|15.3|21.3|19.9|23.6|48.4|10.1|49.8|**56.7**|
|Where2Place|29.1|11.8|15.0|15.0|22.0|16.6|**46.0**|45.8|


### **6.1 Evaluation of Spatial Understanding and Reasoning Capabilities** 

**Benchmarks and Baselines.** _General Spatial Reasoning Capabilities:_ We evaluated general spatial reasoning capabilities using five popular benchmarks: CVBench Tong et al. (2024), BLINK Fu et al. (2024), CRPE Wang et al. (2025), SAT Ray et al. (2024), and EmbSpatial-Bench Du et al. (2024). These benchmarks encompass 15 subtasks measuring various spatial competencies. We included two leading closed-source models: GPT-4o and GPT-4V as performance reference. Subsequently, we conducted comparative analyses against other open-source spatial enhanced MLLMs, including LLaVA-1.5 Liu et al. (2023c), SAT-Dynamic Ray et al. (2024), RoboPoint Yuan et al. (2024b), and ASMv2 Wang et al. (2025), all with 13B parameters. _Object and Free Region Reference Capabilities:_ We assessed embodied spatial capabilities using the RoboRefIt Lu et al. (2023) and Where2Place Yuan et al. (2024b) benchmarks. We compared mainstream closed-source models and MLLM for enhancing spatial abilities (SpatialBot Cai et al. (2024), SpaceLLaVA Chen et al. (2024), and RoboBrain Ji et al. (2025)). We used the proportion of predicted points within specified regions as the accuracy metric. For models without point output support, we asked models to output bounding boxes of target regions, then sampled evenly within these bounding boxes. _Spatial Visual Aids Capabilities:_ We utilized our VABench to evaluate the capabilities. We found few models with this capability for Visual Trace prediction, so we also trained an end-toend prediction baseline model using a pre-trained DINOv2 Oquab et al. (2023) encoder coupled with transformer Vaswani et al. (2017) architecture to predict visual trajectories, trained on the same visual trajectory data, named _DINOv2 Predictor_ . We conducted this comparison to demonstrate the advantages of our reasoning-based FSD approach. More experimental details are provided in App. E. 

9 

**Table 3 Performance comparison on VABench.** The best results are highlighted in bold. 

|**(a)**<br>VABench|-Point|**(b)**|VABench-Vi|sualTrace||
|---|---|---|---|---|---|
|**Model**|**Accuracy**_↑_|||||
|||**Model**|**RMSE**_↓_|**MAE**_↓_|**LLM Score**_↑_|
|GPT4o<br>ASMv2|9.30<br>1007|GPT4o|136.13|113.53|4.37|
|RoboPoint|.<br>1909|DINOv2 Predictor|128.32|117.49|4.01|
|RoboBrain|.<br>700|RoboBrain|121.6|103.8|4.5|
|FSD|.<br>**6182**|FSD|**78.26**|**63.44**|**6.21**|
|w/o SrCoT|**.**<br>2621|w/o SrCoT|99.53|80.06|5.07|
|<br>w/o Alignment|.<br>55.92|w/o Alignment|80.48|66.80|5.92|


**Figure 6 Example of the FSD Reasoning Process** FSD performs point-by-point reasoning and localization, ultimately generating a feasible visual trace. 

**FSD exhibits superior general spatial reasoning capabilities.** As shown in table 1, FSD achieves a leading average rank of 1.3 across 15 tasks from spatial benchmarks, significantly outperforming other 13B open-source models and rivaling the closed-source GPT-4o. The model particularly excels in 3D depth perception (88.0%), distance estimation (86.7%), and spatial relationship understanding (78.3%). These results validate our data-centric approach for building robust spatial reasoning, a critical foundation for advanced embodied intelligence. 

**FSD excels in object reference and free space localization.** The results in table 2 demonstrate FSD’s ability to accurately identify objects and free spaces from language instructions. For object reference (RoboRefIt), FSD achieves 56.7% accuracy, surpassing both GPT-4o (15.3%) and specialist models like RoboPoint (49.8%) by significant margins. On the more challenging free space reference task (Where2Place), FSD performs competitively with RoboPoint while substantially outperforming other models. This improvement stems from enhanced spatial understanding through our SrCoT mechanism. See App. F for more visualizations. 

**FSD demonstrates breakthrough performance in visual aid generation.** As shown in table 3, FSD significantly outperforms all baselines in generating precise spatial affordances and visual traces. Specifically, FSD achieves 61.82% accuracy on VABench-P, over 3x higher than RoboPoint (19.09%) and attains significantly lower error rates with a better LLM Score on VABench-V. Ablation studies validate the critical contributions of both SrCoT and self-consistency alignment, confirming that our reasoning-based approach enables more accurate predictions than purely data-driven methods. A detailed comparison with RoboBrain Ji et al. (2025) is available in App. I. 

**Visualization of visual aids generated by FSD** . We visualize the visual aids generated by FSD in figure 5, showcasing its effective adaptation to diverse scenes, perspectives, and tasks. figure 6 illustrates how the CoT reasoning guides the generation process. Additional visualizations and complete output examples 

10 

**Table 4 SimplerEnv Evaluation on WidowX Robot.** Each task is tested 24 episodes. Most of the results for end-to-end VLAs are sourced from Chen et al. (2025), while the results for the remaining models are reproduced in accordance with the official code. 

|Type|Model|Put Spoon<br>on Towel|Put Carrot<br>on Plate|Stack Green Block<br>on Yellow Block|Put Eggplant<br>in Yellow Basket|Avg|
|---|---|---|---|---|---|---|
||OctoTeam et al.(2024)|41.7|8.2|0.0|56.7|26.7|
|Edtd|_𝜋_0 Black et al.(2024)|29.1|0.0|16.6|62.5|27.1|
|n-o-en<br>VLA|_𝜋_0-fastPertsch et al.(2025)|29.1|21.9|10.8|66.6|**48.3**|
||OpenVLAKim et al.(2024)|4.2|0.0|0.0|16.7|5.2|
||OpenVLA-OFTKim et al.(2025)|34.2|30.0|30.0|**72.5**|41.8|
|Modular VLA|MOKALiu et al.(2024a)|**45.8**|41.6|**33.3**|12.5|33.3|
|Affordance|RoboPointYuan et al.(2024b)|16.7|20.8|8.3|25.0|17.7|
|VLA|FSD|41.6|**50.0**|**33.3**|37.5|40.6|


are available in App. F. 

### **6.2 Evaluation of the Decision Capability** 


**Figure 7** Real-world robotic manipulation tasks performed by an xArm 6 robot (left) and performance comparison of FSD against baseline models GPT-4o, MOKA, and RoboPoint (right). 

**SimplerEnv Evaluation.** To assess the zero-shot generalization capability of FSD, we deployed this approach on the WidowX robotic arm and conducted experiments using SimplerEnv Li et al. (2024d). Since end-to-end VLA methods require fine-tuning, for fair comparison, we ensured that all end-to-end baseline methods were trained using the BridgeData Walke et al. (2023) dataset and evaluated under the same settings. We benchmarked mainstream VLAs, including end-to-end models (Octo, the _𝜋_ 0 series, OpenVLA), the modular-based method MOKA Liu et al. (2024a), and the affordance-based RoboPoint Yuan et al. (2024b). As shown in table 4, although the latest end-to-end VLAs (such as _𝜋_ 0-fast and OpenVLAOFT) perform well in this limited generalization scenario, FSD still achieves an average success rate of 40.6%, significantly outperforming standard zero-shot baselines such as RoboPoint (17.7%). Without dedicated fine-tuning, end-to-end VLAs may suffer from severe performance breakdowns (with success rates approaching zero) when faced with substantial variations in backgrounds and instructions. In contrast, FSD demonstrates robust zero-shot generalization. Therefore, we suggest that an important direction for future research is to explore closed-loop policy VLAs explicitly guided by visual trajectories, in order to combine robust planning capabilities with precise execution abilities. 

11 

**Real World Robot Evaluation** As shown in figure 7, we conducted zero-shot tests with FSD on an xArm 6 robot across 8 tabletop manipulation tasks. The setup included an Intel RealSense L515 LiDAR camera. To test the capabilities of different visual aids, we used visual trace for the sponge and folding tasks, while affordance points were used for other tasks. We compared against GPT-4o, MOKA, and RoboPoint baselines. Robopoint often makes incorrect predictions in tasks involving spatial understanding. The primary cause of MOKA failures stems from the cascading errors of multiple submodules. Under zero-shot conditions, FSD achieved 72% success rate, outperforming the strongest baseline by more than 30%. Notably, FSD successfully completed complex tasks with visual trace generation, e.g. towel folding, which was beyond baseline capabilities. Full results are presented in figure 7. We refer to App. G for detailed setup and visualization. 


**Figure 8 Qualitative results on challenging manipulation scenarios** . We evaluate FSD on a contact-rich task (Top: Wiping the whiteboard) and an articulated object task (Bottom: Opening the drawer). The leftmost column visualizes the visual trace generated by FSD, followed by key frames of the real-world execution. 

**Qualitative Experiments on Challenging Tasks** We conducted a preliminary exploration and attempted to assess FSD’s capability in handling scenarios that require continuous contact and kinematic understanding. We introduced two new challenging tasks: “Wiping the whiteboard” and “opening the drawer.” As shown in figure 8, FSD was able to infer the visual traces required for these tasks. For the contact-rich whiteboard task, the model generated a smooth wiping trajectory across the surface. For the articulated drawer task, the model successfully predicted the arc trajectory needed to pull the handle. Although the downstream action controller requires further adjustment and optimization for these more challenging tasks, these qualitative results verify the potential of FSD to bridge perception and complex control. 

**Table 5** Real-world Execution Time 

**Real World Execution Latency** We evaluated FSD’s execution **Table 5** Real-world Execution Time latency against the end-to-end OpenVLA and modular MOKA **Model Sponge Cucumber** pipelines, with results reported in table 5. FSD achieves the lowOpenVLA (FT) 23s 12s est latency due to its single-pass, single-model architecture that MOKA 28s 18s **FSD 14s 10s** generates the entire visual trace in a zero-shot manner. This approach avoids both the costly fine-tuning and step-by-step inference required by OpenVLA and the system overhead of a multi-component pipeline like MOKA. FSD thus effectively balances powerful zero-shot manipulation capabilities with practical, low real-world latency. We primarily use open-loop control, but FSD can also be integrated into a hierarchical learning-based pipeline, using its visual trace to guide and improve closed-loop control. See App. **??** for more details. 

|**Model**|**Sponge**|**Cucumber**|
|---|---|---|
|OpenVLA (FT)|23s|12s|
|MOKA|28s|18s|
|**FSD**|**14s**|**10s**|


## **7 Conclusion** 

In this paper, we introduced FSD ( _From Seeing to Doing_ ), bridging visual reasoning and robotic manipulation through intermediate spatial representations. Our approach overcomes the critical challenges of scarcity and heterogeneity through three key innovations: a Spatial Relationship-Focused Visual Chain- 

12 


**Figure 9 Visualization of FSD executing tasks** . The first six rows are real-world experiments, and the last four rows are from SIMPLEREnv. 

of-Thought for multi-step reasoning, a hierarchical weak-to-strong data pipeline, and a self-consistency mechanism to align spatial coordinates with visual signals. Experiments demonstrate FSD’s superior performance across multiple spatial reasoning and visual aid benchmarks. In zero-shot robotic deployment, 

13 


You are currently a robot performing robotic manipulation tasks. The task instruction is: place coke can into middle drawer. Use 2D points to mark the manipulated object-centric waypoints to guide the robot to successfully complete the task. Image Input Visual Visual **Trace Gener** ation ation 

##### <Description> 

The image shows a <ref>coke can</ref><box>[[424, 309, 550, 391]]</box> placed on top of a cabinet. The cabinet has an open <ref>middle drawer</ref><box>[[231, 427, 798, 898]]</box>. </Description> <Reasoning> 

To move the coke can into the middle drawer, start by identifying the initial position of the coke can at <point>[[493, 343]]</point>. First, lift the coke can slightly upwards to clear the edge of the cabinet, moving to <point>[[490, 302]]</point>.Next, lower the coke can towards the middle drawer, passing through <point>[[490, 396]]</point> and <point>[[490, 465]]</point>. Continue lowering it into the drawer, reaching <point>[[493, 533]]</point>. Finally, place the coke can in the middle drawer at the final position <box>[[477, 674, 575, 741]]</box>, ending the trace at <point>[[524, 705]]</point>. </Reasoning> <Answer> The visual trace for placing the coke can into the middle drawer is <point>[[493, 343], [490, 302], [490, 396], [490, 465], [493, 533], [505, 602], [515, 677], [524, 705]]</point>. </Answer> 

**Figure 10** An example and visualization of FSD for generating visual trace. 


You are currently a robot performing robotic manipulation tasks.” Your task instruction: Place the spoon on top of the towel. Observe the image, use 2D points and bounding box to mark the target location. In your answer, use <box>[[x1, y1, x2, y2]]</box> to present the bounding box of the target region and use <point>[[x1, y1], [x2, y2], ...]</point> to mark the points of the free space. Image Input Bbox Generation Point Generation 

<Description> 

The image shows a <ref>red spoon</ref><box>[[476, 533, 751, 622]]</box> placed next to a <ref>orange towel</ref><box>[[163, 329, 384, 488]]</box>. In the middle, there is a metal bowl, and to the left of the bowl, there is a yellow chicken leg. </Description> <Reasoning> 

The task is to place the red spoon at <point>[[488, 576]]</point> on top of the green towel at <box>[[163, 329, 384, 488]]</box>. The current position of the spoon is above the towel, so it needs to be moved to overlap with the towel's position <box>[[163, 329, 384, 488]]</box>. </Reasoning> <Answer> To complete the task, the target position for the red spoon is <box>[[166, 371, 418, 435]]</box>. The new position can also be roughly defined by the following several free points <point>[[201, 402], [204, 402], [204, 404], [202, 402], [204, 405], [206, 405], [206, 404], [204, 405]]</point>, which outline the position of the red spoon after it is placed on the orange towel. </Answer> 

**Figure 11** An example and visualization of FSD for generating affordance box and points. 

FSD achieved an impressive 72% success rate across diverse tasks, outperforming baselines by 30%. We acknowledge limitations, such as the reliance on 2D trajectory generation and constraints from training data quality. More limitations and future works are in App.J. 

14 

## **Acknowledgement** 

This work is supported by the National Natural Science Foundation of China (Grant Nos. 62422605, 62533021) and the National Natural Science Foundation of China Youth Student Basic Research Project (Grant No. 625B2128). Yifu Yuan is also supported by the Young Science and Technology Scientists Sponsorship Program by CAST - Doctoral Student Special Plan. This work is also supported by the National Natural Science Foundation of China (Grant No. 92370132) and the National Key Research and Development Program of China (Grant No. 2024YFE0210900). Pengyi Li is supported by the Basic Research Project (Grant No. 624B2101). We would like to thank Zhongwen Xu, Liang Wang, Shuyang Gu, and Han Hu for their participation in the discussions of this paper and for providing valuable insights. In addition, we would especially like to thank Yiyang Huang for the constructive suggestions on improving the figures in the manuscript. 

## **Ethics Statement** 

This paper is dedicated to advancing the field of robotic manipulation towards the creation of more effective and versatile robotic assistants. Our research strictly adheres to responsible practices and aligns with the ICLR Code of Ethics. All training data was sourced from large-scale, open-access robotics datasets, with all assets utilized in full compliance with their original licensing and terms of service. We recognize that while the intended applications of this research are positive, the long-term societal impacts of increasing robotic autonomy warrant careful consideration. 

## **Reproducibility Statement** 

To promote transparency and reproducibility within the scientific community, we provide detailed training parameters and resources in the appendix. The complete code for both training and inference has been uploaded to an gitHub repository: https://github.com/pickxiguapi/Embodied-FSD. We have made datasets and model checkpoints publicly available. 

## **References** 

- Homanga Bharadhwaj, Roozbeh Mottaghi, Abhinav Gupta, and Shubham Tulsiani. Track2act: Predicting point tracks from internet videos enables generalizable robot manipulation. <u>arXiv preprint arXiv:2405.01527, 2024.</u> 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _𝜋_ 0: A vision-language-action flow model for general robot control. <u>arXiv preprint arXiv:2410.24164, 2024.</u> 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. <u>arXiv preprint arXiv:2307.15818, 2023.</u> 

- Wenxiao Cai, Iaroslav Ponomarenko, Jianhao Yuan, Xiaoqi Li, Wankou Yang, Hao Dong, and Bo Zhao. Spatialbot: Precise spatial understanding with vision language models. <u>arXiv preprint arXiv:2406.13642, 2024.</u> 

- Boyuan Chen, Zhuo Xu, Sean Kirmani, Brain Ichter, Dorsa Sadigh, Leonidas Guibas, and Fei Xia. Spatialvlm: Endowing vision-language models with spatial reasoning capabilities. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14455–14465, 2024.</u> 

- Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang, Feng Zhu, and Rui Zhao. Shikra: Unleashing multimodal llm’s referential dialogue magic. <u>arXiv preprint arXiv:2306.15195, 2023.</u> 

15 

- Xinyi Chen, Yilun Chen, Yanwei Fu, Ning Gao, Jiaya Jia, Weiyang Jin, Hao Li, Yao Mu, Jiangmiao Pang, Yu Qiao, Yang Tian, Bin Wang, Bolun Wang, Fangjing Wang, Hanqing Wang, Tai Wang, Ziqin Wang, Xueyuan Wei, Chao Wu, Shuai Yang, Jinhui Ye, Junqiu Yu, Jia Zeng, Jingjing Zhang, Jinyu Zhang, Shi Zhang, Feng Zheng, Bowen Zhou, and Yangkun Zhu. Internvla-m1: A spatially guided vision-language-action framework for generalist robot policy, 2025. URL https://arxiv.org/abs/2510.13778. 

- An-Chieh Cheng, Hongxu Yin, Yang Fu, Qiushan Guo, Ruihan Yang, Jan Kautz, Xiaolong Wang, and Sifei Liu. Spatialrgpt: Grounded spatial reasoning in vision language model. <u>arXiv preprint arXiv:2406.01584, 2024.</u> 

- Mengfei Du, Binhao Wu, Zejun Li, Xuanjing Huang, and Zhongyu Wei. Embspatial-bench: Benchmarking spatial understanding for embodied tasks with large vision-language models. <u>arXiv preprint arXiv:2406.05756, 2024.</u> 

- Hao-Shu Fang, Chenxi Wang, Minghao Gou, and Cewu Lu. Graspnet-1billion: A large-scale benchmark for general object grasping. In <u>Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages</u> 11444–11453, 2020. 

- Xingyu Fu, Yushi Hu, Bangzheng Li, Yu Feng, Haoyu Wang, Xudong Lin, Dan Roth, Noah A Smith, Wei-Chiu Ma, and Ranjay Krishna. Blink: Multimodal large language models can see but not perceive. In <u>European Conference on Computer Vision, pages 148–166. Springer, 2024.</u> 

- Peng Gao, Shijie Geng, Renrui Zhang, Teli Ma, Rongyao Fang, Yongfeng Zhang, Hongsheng Li, and Yu Qiao. Clip-adapter: Better vision-language models with feature adapters. <u>International Journal of Computer Vision,</u> 132(2):581–595, 2024. 

- Richard Hartley and Andrew Zisserman. <u>Multiple View Geometry in Computer Vision.</u> Cambridge University Press, 2nd edition, 2004. ISBN 0521540518. 

- Yining Hong, Haoyu Zhen, Peihao Chen, Shuhong Zheng, Yilun Du, Zhenfang Chen, and Chuang Gan. 3d-llm: Injecting the 3d world into large language models. <u>Advances in Neural Information Processing Systems,</u> 36: 20482–20494, 2023. 

- Mu Hu, Wei Yin, Chi Zhang, Zhipeng Cai, Xiaoxiao Long, Hao Chen, Kaixuan Wang, Gang Yu, Chunhua Shen, and Shaojie Shen. Metric3d v2: A versatile monocular geometric foundation model for zero-shot metric depth and surface normal estimation. <u>arXiv preprint arXiv:2404.15506, 2024.</u> 

- Wenlong Huang, Chen Wang, Yunzhu Li, Ruohan Zhang, and Li Fei-Fei. Rekep: Spatio-temporal reasoning of relational keypoint constraints for robotic manipulation. <u>arXiv preprint arXiv:2409.01652, 2024.</u> 

- Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. Gpt-4o system card. <u>arXiv preprint arXiv:2410.21276, 2024.</u> 

- Yuheng Ji, Huajie Tan, Jiayu Shi, Xiaoshuai Hao, Yuan Zhang, Hengyuan Zhang, Pengwei Wang, Mengdi Zhao, Yao Mu, Pengju An, Xinda Xue, Qinghang Su, Huaihai Lyu, Xiaolong Zheng, Jiaming Liu, Zhongyuan Wang, and Shanghang Zhang. Robobrain: A unified brain model for robotic manipulation from abstract to concrete. <u>arXiv preprint arXiv:2502.21257, 2025.</u> 

- Linyi Jin, Jianming Zhang, Yannick Hold-Geoffroy, Oliver Wang, Kevin Blackburn-Matzen, Matthew Sticha, and David F Fouhey. Perspective fields for single image camera calibration. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 17307–17316, 2023.</u> 

- Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. <u>arXiv preprint arXiv:2001.08361,</u> 2020. 

- Nikita Karaev, Iurii Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian Rupprecht. Cotracker3: Simpler and better point tracking by pseudo-labelling real videos. <u>arXiv preprint arXiv:2410.11831,</u> 2024. 

- Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. <u>arXiv preprint arXiv:2403.12945, 2024.</u> 

16 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan Foster, Grace Lam, Pannag Sanketi, et al. Openvla: An open-source vision-language-action model. <u>arXiv preprint arXiv:2406.09246, 2024.</u> 

- Moo Jin Kim, Chelsea Finn, and Percy Liang. Fine-tuning vision-language-action models: Optimizing speed and success. <u>arXiv preprint arXiv:2502.19645, 2025.</u> 

- Bo Li, Yuanhan Zhang, Dong Guo, Renrui Zhang, Feng Li, Hao Zhang, Kaichen Zhang, Peiyuan Zhang, Yanwei Li, Ziwei Liu, et al. Llava-onevision: Easy visual task transfer. <u>arXiv preprint arXiv:2408.03326, 2024a.</u> 

- Chengzu Li, Caiqi Zhang, Han Zhou, Nigel Collier, Anna Korhonen, and Ivan Vulić. Topviewrs: Vision-language models as top-view spatial reasoners. <u>arXiv preprint arXiv:2406.02537, 2024b.</u> 

- Xiang Li, Cristina Mata, Jongwoo Park, Kumara Kahatapitiya, Yoo Sung Jang, Jinghuan Shang, Kanchana Ranasinghe, Ryan Burgert, Mu Cai, Yong Jae Lee, et al. Llara: Supercharging robot learning data for vision-language policy. <u>arXiv preprint arXiv:2406.20095, 2024c.</u> 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. <u>arXiv preprint arXiv:2405.05941, 2024d.</u> 

- Yi Li, Yuquan Deng, Jesse Zhang, Joel Jang, Marius Memmel, Raymond Yu, Caelan Reed Garrett, Fabio Ramos, Dieter Fox, Anqi Li, et al. Hamster: Hierarchical action models for open-world robot manipulation. <u>arXiv preprint arXiv:2502.05485, 2025.</u> 

- Zejun Li, Ruipu Luo, Jiwen Zhang, Minghui Qiu, and Zhongyu Wei. Vocot: Unleashing visually grounded multi-step reasoning in large multi-modal models. <u>arXiv preprint arXiv:2405.16919, 2024e.</u> 

- Yuan-Hong Liao, Rafid Mahmood, Sanja Fidler, and David Acuna. Reasoning paths with reference objects elicit quantitative spatial reasoning in large vision-language models. <u>arXiv preprint arXiv:2409.09788, 2024.</u> 

- Fanqi Lin, Yingdong Hu, Pingyue Sheng, Chuan Wen, Jiacheng You, and Yang Gao. Data scaling laws in imitation learning for robotic manipulation. <u>arXiv preprint arXiv:2410.18647, 2024a.</u> 

- Ji Lin, Hongxu Yin, Wei Ping, Pavlo Molchanov, Mohammad Shoeybi, and Song Han. Vila: On pre-training for visual language models. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,</u> pages 26689–26699, 2024b. 

- Bo Liu, Yifeng Zhu, Chongkai Gao, Yihao Feng, Qiang Liu, Yuke Zhu, and Peter Stone. Libero: Benchmarking knowledge transfer for lifelong robot learning. <u>Advances in Neural Information Processing Systems, 36:44776–</u> 44791, 2023a. 

- Fangchen Liu, Kuan Fang, Pieter Abbeel, and Sergey Levine. Moka: Open-vocabulary robotic manipulation through mark-based visual prompting. In <u>First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024, 2024a.</u> 

- Fangyu Liu, Guy Emerson, and Nigel Collier. Visual spatial reasoning. <u>Transactions of the Association for Computational Linguistics, 11:635–651, 2023b.</u> 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Improved baselines with visual instruction tuning. <u>arXiv preprint arXiv:2310.03744, 2023c.</u> 

- Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee. Llava-next: Improved reasoning, ocr, and world knowledge, 2024b. URL https://llava-vl.github.io/blog/2024-01-30-llava-next/. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. <u>Advances in neural information processing systems, 36, 2024c.</u> 

- Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, et al. Grounding dino: Marrying dino with grounded pre-training for open-set object detection. <u>arXiv preprint arXiv:2303.05499, 2023d.</u> 

17 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. <u>arXiv preprint arXiv:2410.07864, 2024d.</u> 

- Yuhao Lu, Yixuan Fan, Beixing Deng, Fangfu Liu, Yali Li, and Shengjin Wang. Vl-grasp: a 6-dof interactive grasp policy for language-oriented objects in cluttered indoor scenes. In <u>2023 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 976–983. IEEE, 2023.</u> 

- Chancharik Mitra, Brandon Huang, Trevor Darrell, and Roei Herzig. Compositional chain-of-thought prompting for large multimodal models. In <u>Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 14420–14431, 2024.</u> 

- Kaichun Mo, Leonidas J Guibas, Mustafa Mukadam, Abhinav Gupta, and Shubham Tulsiani. Where2act: From pixels to actions for articulated 3d objects. In <u>Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 6813–6823, 2021.</u> 

- Dantong Niu, Yuvan Sharma, Giscard Biamby, Jerome Quenum, Yutong Bai, Baifeng Shi, Trevor Darrell, and Roei Herzig. Llarva: Vision-action instruction tuning enhances robot learning. <u>arXiv preprint arXiv:2406.11815,</u> 2024. 

- Jake O’Neill, Abraham Arthurs, Fábio Avila Belbute-Peres, Julian Balaguer, Sarah Bechtle, Gemma Bidoia, Kyle Burden, Erwin Chang, Sheila Chen, Todor Davchev, et al. Open x-embodiment: Robotic learning datasets and rt-x models. <u>arXiv preprint arXiv:2310.08864, 2023.</u> 

- Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. <u>arXiv preprint arXiv:2304.07193, 2023.</u> 

- Karl Pertsch, Kyle Stachowicz, Brian Ichter, Danny Driess, Suraj Nair, Quan Vuong, Oier Mees, Chelsea Finn, and Sergey Levine. Fast: Efficient action tokenization for vision-language-action models. <u>arXiv preprint arXiv:2501.09747, 2025.</u> 

- Zengyi Qin, Kuan Fang, Yuke Zhu, Li Fei-Fei, and Silvio Savarese. Keto: Learning keypoint representations for tool manipulation. In <u>2020 IEEE International Conference on Robotics and Automation (ICRA), pages 7278–7285.</u> IEEE, 2020. 

- Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. <u>Journal of Machine Learning Research, 21:1–67, 2020.</u> URL https://jmlr.org/papers/v21/20-074.html. 

- Arijit Ray, Jiafei Duan, Reuben Tan, Dina Bashkirova, Rose Hendrix, Kiana Ehsani, Aniruddha Kembhavi, Bryan A Plummer, Ranjay Krishna, Kuo-Hao Zeng, et al. Sat: Spatial aptitude training for multimodal language models. <u>arXiv preprint arXiv:2412.07755, 2024.</u> 

- Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kunchang Li, He Cao, Jiayu Chen, Xinyu Huang, Yukang Chen, Feng Yan, et al. Grounded sam: Assembling open-world models for diverse visual tasks. <u>arXiv preprint arXiv:2401.14159, 2024.</u> 

- Hao Shao, Shengju Qian, Han Xiao, Guanglu Song, Zhuofan Zong, Letian Wang, Yu Liu, and Hongsheng Li. Visual cot: Advancing multi-modal language models with a comprehensive dataset and benchmark for chain-of-thought reasoning. In <u>The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2024.</u> 

- Mohit Shridhar, Yat Long Lo, and Stephen James. Generative image as action models. <u>arXiv preprint arXiv:2407.07875, 2024.</u> 

- Chan Hee Song, Valts Blukis, Jonathan Tremblay, Stephen Tyree, Yu Su, and Stan Birchfield. Robospatial: Teaching spatial understanding to 2d and 3d vision-language models for robotics. <u>arXiv preprint arXiv:2411.16537, 2024.</u> 

- Balakumar Sundaralingam, Siva Kumar Sastry Hari, Adam Fishman, Caelan Garrett, Karl Van Wyk, Valts Blukis, Alexander Millane, Helen Oleynikova, Ankur Handa, Fabio Ramos, et al. Curobo: Parallelized collision-free 

18 

robot motion generation. In <u>2023 IEEE International Conference on Robotics and Automation (ICRA),</u> pages 8112–8119. IEEE, 2023. 

- Octo Team, RT-X Team, Anthony Brohan, Noah Brown, Lauren Chen, Michael Cheng, Krzysztof Choromanski, Eamonn Cullina, Gabe Dalal, Chelsea Fu, Florian Golemo, et al. Octo: An open-source generalist robot policy. <u>arXiv preprint arXiv:2403.10164, 2024.</u> 

- Shengbang Tong, Ellis Brown, Penghao Wu, Sanghyun Woo, Manoj Middepogu, Sai Charitha Akula, Jihan Yang, Shusheng Yang, Adithya Iyer, Xichen Pan, Austin Wang, Rob Fergus, Yann LeCun, and Saining Xie. Cambrian-1: A fully open, vision-centric exploration of multimodal llms, 2024. 

- Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. <u>Advances in neural information processing systems, 30, 2017.</u> 

- Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe Hansen-Estruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In <u>Conference on Robot Learning, pages 1723–1736. PMLR, 2023.</u> 

- Lirui Wang, Xinlei Chen, Jialiang Zhao, and Kaiming He. Scaling proprioceptive-visual learning with heterogeneous pre-trained transformers. <u>arXiv preprint arXiv:2409.20537, 2024.</u> 

- Weiyun Wang, Yiming Ren, Haowen Luo, Tiantong Li, Chenxiang Yan, Zhe Chen, Wenhai Wang, Qingyun Li, Lewei Lu, Xizhou Zhu, et al. The all-seeing project v2: Towards general relation comprehension of the open world. In <u>European Conference on Computer Vision, pages 471–490. Springer, 2025.</u> 

- Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. Chainof-thought prompting elicits reasoning in large language models. <u>Advances in neural information processing systems, 35:24824–24837, 2022.</u> 

- Chuan Wen, Xingyu Lin, John So, Kai Chen, Qi Dou, Yang Gao, and Pieter Abbeel. Any-point trajectory modeling for policy learning. <u>arXiv preprint arXiv:2401.00025, 2023.</u> 

- Yixuan Wu, Yizhou Wang, Shixiang Tang, Wenhao Wu, Tong He, Wanli Ouyang, Philip Torr, and Jian Wu. Dettoolchain: A new prompting paradigm to unleash detection ability of mllm. In <u>European Conference on Computer Vision, pages 164–182. Springer, 2025.</u> 

- Mengda Xu, Zhenjia Xu, Yinghao Xu, Cheng Chi, Gordon Wetzstein, Manuela Veloso, and Shuran Song. Flow as the cross-domain manipulation interface. <u>arXiv preprint arXiv:2407.15208, 2024.</u> 

- Jianwei Yang, Reuben Tan, Qianhui Wu, Ruijie Zheng, Baolin Peng, Yongyuan Liang, Yu Gu, Mu Cai, Seonghyeon Ye, Joel Jang, et al. Magma: A foundation model for multimodal ai agents. <u>arXiv preprint arXiv:2502.13130,</u> 2025. 

- Fanglong Yao, Changyuan Tian, Jintao Liu, Zequn Zhang, Qing Liu, Li Jin, Shuchao Li, Xiaoyu Li, and Xian Sun. Thinking like an expert: Multimodal hypergraph-of-thought (hot) reasoning to boost foundation modals. <u>arXiv preprint arXiv:2308.06207, 2023a.</u> 

- Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. Tree of thoughts: Deliberate problem solving with large language models. <u>Advances in Neural Information Processing Systems, 36, 2024.</u> 

- Yao Yao, Zuchao Li, and Hai Zhao. Beyond chain-of-thought, effective graph-of-thought reasoning in language models. <u>arXiv preprint arXiv:2305.16582, 2023b.</u> 

- Haoxuan You, Haotian Zhang, Zhe Gan, Xianzhi Du, Bowen Zhang, Zirui Wang, Liangliang Cao, Shih-Fu Chang, and Yinfei Yang. Ferret: Refer and ground anything anywhere at any granularity. <u>arXiv preprint arXiv:2310.07704,</u> 2023. 

- Chengbo Yuan, Chuan Wen, Tong Zhang, and Yang Gao. General flow as foundation affordance for scalable robot learning. <u>arXiv preprint arXiv:2401.11439, 2024a.</u> 

19 

- Wentao Yuan, Jiafei Duan, Valts Blukis, Wilbert Pumacay, Ranjay Krishna, Adithyavairavan Murali, Arsalan Mousavian, and Dieter Fox. Robopoint: A vision-language model for spatial affordance prediction for robotics. <u>arXiv preprint arXiv:2406.10721, 2024b.</u> 

- Michał Zawalski, William Chen, Karl Pertsch, Oier Mees, Chelsea Finn, and Sergey Levine. Robotic control via embodied chain-of-thought reasoning. <u>arXiv preprint arXiv:2407.08693, 2024.</u> 

- Tianle Zhang, Dongjiang Li, Yihang Li, Zecui Zeng, Lin Zhao, Lei Sun, Yue Chen, Xuelong Wei, Yibing Zhan, Lusong Li, et al. Empowering embodied manipulation: A bimanual-mobile robot manipulation dataset for household tasks. <u>arXiv preprint arXiv:2405.18860, 2024.</u> 

- Zhuosheng Zhang, Aston Zhang, Mu Li, and Alex Smola. Automatic chain of thought prompting in large language models. <u>arXiv preprint arXiv:2210.03493, 2022.</u> 

- Ge Zheng, Bin Yang, Jiajin Tang, Hong-Yu Zhou, and Sibei Yang. Ddcot: Duty-distinct chain-of-thought prompting for multimodal reasoning in language models. <u>Advances in Neural Information Processing Systems, 36:5168–</u> 5191, 2023a. 

- Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and chatbot arena. <u>Advances in Neural Information Processing Systems, 36:46595–46623, 2023b.</u> 

- Ruijie Zheng, Yongyuan Liang, Shuaiyi Huang, Jianfeng Gao, Hal Daumé III, Andrey Kolobov, Furong Huang, and Jianwei Yang. Tracevla: Visual trace prompting enhances spatial-temporal awareness for generalist robotic policies. <u>arXiv preprint arXiv:2412.10345, 2024.</u> 

- Shengjie Zhu, Abhinav Kumar, Masa Hu, and Xiaoming Liu. Tame a wild camera: in-the-wild monocular camera calibration. <u>Advances in Neural Information Processing Systems, 36, 2024.</u> 

20 

## **Appendix** 

## **A Weak-to-Strong Dataset Construction** 

**Region Grounding Dataset Generation** Regional grounding enables robots to focus on key objects within a scene. In embodied AI, robots need to concentrate on task-relevant local scenes in the image according to task instructions and be able to accurately locate objects. In Level 1 of our dataset, we integrate grounding with captioning, aiming for the agent to provide positional information when describing images. Unlike traditional image captioning, objects in embodied scenes are often cluttered, and we only seek to extract captions for task-relevant regions, avoiding redundant information. We prompt GPT-4o to exclude task-irrelevant regions based on task instructions and generate both image captions and the corresponding object names. Subsequently, we use Grounding DINO Liu et al. (2023d) to capture the locations of various objects in the image and embed them into the caption sentences, forming captions with object location information. Below is an example from the dataset: 

Level 1: Region Grounding 

**Human:** `Give a short and clear explanation of the subsequent image.` **GPT:** `A <ref>robotic arm</ref><box>[[338, 126, 994, 861]]</box> is positioned above a <ref>blue bottle</ref><box>[[257, 201, 381, 413]]</box>, with a <ref>grey toy</ref><box>[[391, 413, 538, 518]]</box> to the left and a <ref>green oval object</ref><box>[[592, 481, 702, 601]]</box> to the right on a wooden table.` 

**Spatial Relationship Dataset Generation** To accurately infer object spatial relationships from RGB images, a multi-stage pipeline is employed: encompassing object detection, instance segmentation, 2D-to-3D mapping, and subsequent relationship calculation. 

Initially, for pre-identified objects of interest within the scene, GroundedSAM Ren et al. (2024) is utilized to perform instance segmentation, yielding precise object masks. Subsequently, the 2D RGB information is elevated to a 3D spatial representation. This transformation begins with leveraging PerspectiveFields Jin et al. (2023) to estimate the Z-axis orientation, serving as a coarse approximation for camera extrinsics. Concurrently, the WildCamera Zhu et al. (2024) model is employed to estimate intrinsic camera parameters, including focal length and resolution. Metric3Dv2 Hu et al. (2024) is then used for robust depth estimation. By integrating the RGB image, estimated depth image, and computed camera intrinsics and extrinsics, the 2D RGB image is transformed into a 3D point cloud. Given the prior object segmentation, the specific 3D spatial position and size of each individual object can be precisely derived from the generated point cloud. These comprehensive 3D data then enable the calculation of relative spatial relationships between objects, which are subsequently exported as a spatial relationship graph. We present the 2D RGB-D images before transformation and the visualized point clouds after transformation in figure 12. 

It is important to note that for inferring spatial relationships, only relative depth sorting data is generated, which means stringent accuracy requirements for absolute depth are relaxed. To further enhance data quality, particularly for robust relationship inference, objects exhibiting a relative depth gap of at least 20% are preferentially selected for subsequent generation. An example from the dataset: 

21 


Point clouds after instance segmentation 

Depth Image 

RGB Image 

**Figure 12** RGB-D images before transformation and the visualized point clouds after transformation. 

Level 2: Spatial Relationship 

```
Human:Tellmeabouttheitemsinyourviewandtheirrelationshipsto
eachother.Answerthequestionwithscenegraph.
GPT:<ref>frontleftburner</ref><box>[[597,422,817,596]]</box>
ispositioned<pred>totherightof</pred><box>[[597,422,
817,596]]</box><box>[[171,275,446,409]]</box><ref>metal
pot</ref><box>[[171,275,446,409]]</box>.<ref>metal
pot</ref><box>[[171,275,446,409]]</box>appears<pred>tothe
leftof</pred><box>[[171,275,446,409]]</box><box>[[431,474,715,
608]]</box><ref>greenspatula</ref><box>[[431,474,715,608]]</box>.
<ref>metalpot</ref><box>[[171,275,446,409]]</box>canbeseen
<pred>totheleftof</pred><box>[[171,275,446,409]]</box><box>[[519,
408,600,490]]</box><ref>orangecheeseslice</ref><box>[[519,408,
600,490]]</box>.
```

**Spatial Reasoning QA Generation** After generating the spatial relation diagrams, we can easily create various template questions for spatial reasoning Cheng et al. (2024); Du et al. (2024), such as: _How are [A] and [B] positioned in relation to each other in the image? or From your perspective, which object in the image is at the shortest distance?_ In addition to template-based QA, we also combine task instructions, existing spatial information, and images to query GPT-4o, thereby generating more diverse multi-turn dialogues to enhance the model’s generalization ability in spatial reasoning. 

**Spatial Affordance and Visual Trace Dataset Generation** Next, we provide a detailed description of how to extract the required controllable points/boxes and visual trajectories from the embodied dataset like BridgeData Walke et al. (2023), RT-X O’Neill et al. (2023) and Droid Khazatsky et al. (2024). Our methodology for extracting visual aids, specifically Affordance Boxes, Affordance Points, and Visual Traces, involves a multi-stage process leveraging state-of-the-art vision models. We also incorporate a rigorous data validation procedure to ensure high-quality output. 

First, we acquire the initial and final frames of the video sequence. To determine the Affordance Box, we utilize GroundingDINO Liu et al. (2023d) and GroundedSam Ren et al. (2024) to detect the mask of the `manipulated_object` in the final frame. The bounding box of this detected object in the final frame defines the Affordance Box, representing the ultimate spatial location of the manipulated object. Subsequently, we extract Affordance Points. This involves performing an erosion operation on the mask of the `manipulated_object` obtained from the final frame. Erosion reduces the mask’s area, facilitating 

22 

the sampling of points that are more central or internal to the object, thereby mitigating the risk of sampling edge points. From this eroded mask, we uniformly sample 8 points, which constitute the Affordance Points. For Visual Trace extraction, we begin by detecting the mask of the `manipulated_object` in the first frame. From this mask, we sample 3 points, which serve as the initial query points for the CoTracker Karaev et al. (2024) model. Selecting multiple points enhances the robustness of trajectory tracking. The processed video sequence and these sampled points are then fed into the CoTracker model, which outputs the predicted trajectory for each query point across every frame of the video sequence. We calculate the total distance of each trajectory and select the longest trajectory as the representative trajectory for the `manipulated_object` . This chosen trajectory is then subjected to cubic spline interpolation for smoothing. Finally, 8 equidistant points are uniformly sampled from the smoothed trajectory, forming the Visual Trace. 

A critical aspect of this process is addressing potential prediction errors from the pre-trained visual models, such as incorrect object identification or incomplete tracking of object motion. To mitigate these issues, we implement stringent rule-based filtering using hyperparameters like size thresholds and trajectory length thresholds. Before annotating each dataset, we iteratively adjust these rules and conduct manual inspections on 100 examples. Only when the accuracy of these filtered results surpasses 95% do we deem the filtering rules robust enough to proceed with the full data generation pipeline. This meticulous validation process ensures the high quality of the generated data. 

Following the generation of these visual aids, we also pre-generate the thinking processes for Chainof-Thought (CoT) reasoning. We input templates, questions, and answers into GPT-4o, querying it to complete the thinking process. The complete query prompt is constructed accordingly: 

23 

#### Prompt and In-context Example for Completing Thinking Process 

```
YouareanAIvisualassistantthatcananalyzeasingleimage.
Youreceiveoneimageandcorrespondingcaption,taskinstruction,
manipulatedobjectinthetaskandtargetplacetofinishthetask,
andboundingboxpositionandrelativepositionoftheseobjects.
Also,youreceivetheanswerofpointsandbbox.Now,youneedto
generatea<Description>...</Description>,<Reasoning>...</Reasoning>,
<Answer>...</Answer>format.
<Description>First,usingtheprovidedcaption,taskinstruction,
describethescene.Ifthereareerrorsinthecaption,pleaseignore
themanddonotpointthemoutinyourdescription.Insteadofdirectly
mentioningtheboundingboxcoordinates,utilizethisdatatoexplain
thesceneusingnaturallanguagewithitsboundingboxintheformat
like"<ref>object</ref><box>[[x1,y1,x2,y2]]</box>".Whenmentioning
thepredicatebetweentwoobjects,youshouldmentionitintheformat
like"<pred>predicate</pred><box>[[x1,y1,x2,y2]]</box><box>[[x3,
y3,x4,y4]]</box>",where"<box>[[x1,y1,x2,y2]]</box>"denotes
theboundingboxcoordinatesofthesubjectand"<box>[[x3,y3,
x4,y4]]</box>"denotestheboundingboxcoordinatesoftheobject.
</Description>
<Reasoning>Accordingtothetaskinstructionandtheanswerofpoints
andbbox,provideachain-of-thought,logicalexplanationoftheproblem.
</Reasoning>
<Answer>Statethefinalboundingboxanswerandpointanswerinaclear
anddirectformathere.Boundingboxanswerisintheformatlike
"<box>[[x1,y1,x2,y2]]</box>".Pointanswerisintheformatlike
"<point>[[x1,y1],[x2,y2],[x3,y3],...]</point>".</Answer>
Hereisanexample:
Caption:7upcanisonthetablebesidethebowl,drawerisopen.
Taskinstruction:place7upcanintotopdrawer
Manipulatedobject:7upcan<box>[[686,174,788,357]]</box>
Targetplace:topdrawer<box>[[135,411,852,920]]</box>Current
Relation:(7upcan,[686,174,788,357],topdrawer,[135,411,852,
920],above)
BoundingBoxAnswer:[569,553,651,679]
PointAnswer:[[603,609],[593,637],[596,643],[615,596],[612,
593],[590,637],[603,606],[615,631]]
```

```
<Description>Thescenedescribesa<ref>7upcan</ref><box>[[686,
174,788,357]]</box>thatispositionedonatable.Itissituated
<pred>above</pred><box>[[686,174,788,357]]</box><box>[[135,411,852,
920]]</box>the<ref>topdrawer</ref><box>[[135,411,852,920]]</box>
whichisopen.</Description><Reasoning>The7upcanisabovethe
topdrawernowandshouldbeplacedintothetopdrawer.Sothe
targetpositionofthe7upcanmightbesimilartothepositionofthe
drawer’sinterior.</Reasoning><Answer>Tocompletethetask,the
targetpositionis<box>[[569,553,651,679]]</box>.Thenewposition
canalsoberoughlydefinedbythefollowingseveralfreepoints
<point>[[603,609],[593,637],[596,643],[615,596],[612,593],[590,
637],[603,606],[615,631]]</point>,whichcanoutlinethepositionof
the7upcanafteritisplacedinthetopdrawer.</Answer>
```

24 

Next, we present two examples from the dataset: one involves generating Affordance Boxes/Points (Level 4), and the other involves generating visual trace (Level 5). We consider Affordance Points as samples within the box; thus, generating the box first and then the points is a refinement process from coarse to fine granularity. Therefore, both types are generated for each data, and one can choose which to use as needed. In the task of generating visual trace, since we performed equidistant interpolation in advance, the visual trace in the dataset is fixed at 8 points. Consequently, models trained on such a dataset will also generate 8 points as the visual trace. 

Level 4: Spatial Affordance Box/Points Generation 

```
Human:"Youarecurrentlyarobotperformingroboticmanipulationtasks.
Yourtaskinstruction:Movedthecantotheleftsideofthegreen
cloth.Observetheimage,use2Dpointsandboundingboxtomarkthe
targetlocationwherethemanipulatedobjectwillbemoved.Inyour
answer,use<box>[[x1,y1,x2,y2]]</box>topresenttheboundingboxof
thetargetregion,anduse<point>[[x1,y1],[x2,y2],...]</point>to
markthepointsofthefreespace."
```

```
GPT:"<Description>
Theimageshowsa<ref>whitesoupcan</ref><box>[[544,177,
700,368]]</box>positionedtotherightofa<ref>green
towel</ref><box>[[244,389,664,676]]</box>onatable.Asmallbowl
containingayellowobjectandabrushisnexttothetowel.
</Description>
<Reasoning>
Thetaskistomovethewhitesoupcantotheleftsideofthegreen
towel.Currently,thecanistotherightofthetowel,soitneedsto
berepositionedtotheleftofthetowel’scurrentlocation.
</Reasoning>
<Answer>
Thetargetpositionforthewhitesoupcanis<box>[[250,181,400,
392]]</box>.Thenewpositioncanalsoberoughlydefinedbythe
followingpoints:<point>[[346,248],[302,365],[377,251],[330,
295],[357,291],[354,362],[329,355],[312,352]]</point>.
</Answer>"
```

25 

#### Level 5: Visual Trace Generation 

```
Human:"Youarecurrentlyarobotperformingroboticmanipulation
tasks.Yourtaskinstruction:putthegreenspatulainthesilverpot.
Observetheimage,use2Dpointstomarkthemanipulatedobject-centric
waypointstoguidetherobottomanipulatetheobject.Typically,the
waypointsconsistofanorderedsequenceofeight2Dpoints.Theformat
is<point>[[x1,y1],[x2,y2],...]</point>."
```

### `GPT: "<Description>` 

```
Theimageshowsa<ref>greenspatula</ref><box>[[762,536,856,
711]]</box>positionedtotherightofanorangetowelonatable.A
<ref>silverpot</ref><box>[[0,723,242,872]]</box>islocatedabovea
roboticarm.Otherobjects,suchasagraycanandamushroom,arealso
presentinthescene.
```

```
</Description>
<Reasoning>
```

```
Tomovethegreenspatulaintothesilverpot,startbyidentifyingthe
initialpositionofthespatulaat<point>[[802,613]]</point>.First,
liftthespatulaupwardstoclearthetable,movingto<point>[[774,
501]]</point>.Then,moveithorizontallytowardstheleft,passing
through<point>[[685,394]]</point>.Finally,lowerthespatulainto
thesilverpot,endingat<point>[[657,401]]</point>withinthetarget
boundingbox<box>[[225,529,407,640]]</box>.
```

```
</Reasoning>
```

```
<Answer>
```

```
Thevisualtraceforplacingthegreenspatulaintothesilverpotis
<point>[[802,613],[780,582],[774,501],[744,465],[685,394],[657,
349],[668,354],[657,401]]</point>.
</Answer>"
```

## **B Training Details and Datasets** 

The training of FSD is a two-stage process, building upon the LLaVA Liu et al. (2024b) architecture through continued fine-tuning of ASMv2 Wang et al. (2025). In order to train a VLM with powerful spatiotemporal reasoning abilities that can also generate visual aids, we leveraged a comprehensive dataset of approximately 1.4M samples from various sources. _Note:_ The position coordinate format used by FSD normalizes the image coordinates to a range of 0-999 after padding the image to a square shape. For all datasets mentioned below, the coordinates have been pre-processed in this manner. 

**Stage 1: Spatial Reasoning Enhancement** The primary goal of the first stage is to enhance the model’s spatial reasoning capabilities. This dataset is primarily composed of two parts: common-sense image QA and conversations data and spatial reasoning data. The inclusion of GeneralQA is crucial for FSD to maintain broad instruction-following abilities after fine-tuning. First, we selected some datasets and randomly sampled around 838k data from LLaVA-665k and ASMv2-4M instruction-following data. Next, we incorporated approximately 295k samples of spatial reasoning data from the LLaVA-OneVision Li et al. (2024a), RoboPoint Yuan et al. (2024b), SpatialBot Cai et al. (2024) and SAT Ray et al. (2024) training 

26 

datasets. Finally, the first three levels of FSD’s collected embodied spatial reasoning datasets (250k samples) were also integrated into this training phase. A summary of the datasets used can be found in table 6. 

**Stage 2: Visual Aids Generation and Understanding** We specifically focused on training for visual aids generation. Here, "generation" refers to generating visual aids based on a given question, while "understanding" represents its inverse problem. We excluded some inverse problems with ambiguous semantics. The final total amount of data used is shown in table 6. 

**Training Configuration** We used exactly the same hyperparameters in both stages of training. We utilized a global batch size of 128 and the AdamW optimizer, configured with _𝛽_ 1 = 0.9, _𝛽_ 2 = 0.999, and a weight decay coefficient of 0. The learning rate was set to 2 _×_ 10<sup>_−_5</sup> . Both training stages employ a linear warmup for the first 3% of training steps, followed by a cosine decay strategy to a minimum learning rate of 0. We simultaneously train both the vision-language connector and the language model. The image resolution was set to 336 _×_ 336, and the visual encoder remained frozen throughout the entire training process. In the first phase, we train for 1 epoch on the complete dataset, while in the second phase, we train for 3 epochs. The FSD model has approximately 13B trainable parameters and we conducted training using 8 A100 40G GPUs, with Stage 1 requiring approximately 72 hours and Stage 2 requiring 8 hours. 

## **C Details of Action Execution** 

When utilizing FSD for robotic manipulation tasks, we can select from various visual aids. As described in figure 2, these include **spatial affordance boxes** ( _ℬ_ ), **spatial affordance points** ( _𝒫_ ), and **object-centric visual traces** ( **_𝜏_** ). The choice of visual aids dictates the subsequent motion planning strategy. 

**Motion Planning with Spatial Affordances** For spatial affordance boxes ( _ℬ_ ), the target point for manipulation is derived by sampling the center of the box. In the case of spatial affordance points ( _𝒫_ ), a point is directly sampled. When relying on spatial affordance information, whether from boxes or points, we employ CuRobo Sundaralingam et al. (2023) as our motion planner. CuRobo is responsible for generating collision-free paths that guide the robot’s end-effector to the inferred target affordance point. 

**Motion Planning with Object-Centric Visual Traces** When leveraging object-centric visual traces ( **_𝜏_** ), the process involves mapping 2D visual traces into 3D space and then interpolating these discrete points to form a complete motion trajectory in SE(3) space. The detailed procedure is as follows: 

We directly acquire 2D keypoint information, denoted as _𝑘𝑖_ = ( _𝑢𝑖_ , _𝑣𝑖_ ) _∈_ **R**<sup>2</sup> , where _𝑢𝑖_ and _𝑣𝑖_ represent the x and y coordinates of the _𝑖_ -th point in the image, for _𝑖 ∈_ [1, _𝑇_ ]. Initial depth information, _𝑑𝑖 ∈_ **R** , is obtained from a depth camera. Using the Pinhole camera model Hartley and Zisserman (2004), we can transform these 2D keypoints into 3D Cartesian coordinates _𝑃𝑖_ = ( _𝑥𝑖_ , _𝑦𝑖_ , _𝑧𝑖_ ) _∈_ **R**<sup>3</sup> via: 


Here, _𝑠𝑖_ is the normalized depth, calculated as _𝑠𝑖_ = _𝑑𝑖_ / `depth_scale` . The intrinsic camera parameters, _𝑓𝑥_ , _𝑓𝑦_ , _𝑐𝑥_ , _𝑐𝑦_ , and the depth scaling factor, `depth_scale` , are all camera-specific. 

However, a naive use of the raw depth values _𝑑𝑖_ obtained from the depth camera often results in trajectories that closely hug the object’s surface, which is undesirable for robust robot manipulation. To address this, we formulate an optimization problem to address it. We fix the depth values for the start and end 

27 

points of the path ( _𝑑_ 1 and _𝑑𝑇_ ) and optimize the intermediate depth values _𝑑_ 2: _𝑇 −_ 1 to minimize the total Euclidean distance between consecutive points in Cartesian space. 

The objective function for this optimization is: 


where _𝑑_ ( _𝑃𝑖_ , _𝑃𝑖_ +1) represents the Euclidean distance between points _𝑃𝑖_ and _𝑃𝑖_ +1. We employ a gradient descent method from `scipy` library to optimize this objective function. This refined approach allows for more robust and practical robot motion planning by addressing the limitations of raw depth data and providing a structured framework for integrating various visual aids. 

## **D Details of Visual Aids Generation Benchmark** 

To address the gap in evaluating visual assistance signal generation, we established **VABench** , a comprehensive benchmark. VABench comprises two distinct tasks: **VABench-Point** and **VABench-VisualTrace** , each featuring 300 meticulously hand-annotated questions. These tasks require models to infer visual auxiliary information solely from natural language instructions, mimicking everyday human commands. 

For **VABench-Point** , we provide ground truth bounding boxes for each question. The model’s performance is then assessed by calculating the proportion of predicted points that fall within the target region. For models that only output bounding boxes, we explored two scoring methods: Intersection Over Union (IOU) and uniformly sampling points within the predicted box. We ultimately opted for the latter approach, as the physical interaction between a robotic arm and an object in real-world tasks is fundamentally determined by specific point coordinates. For **VABench-VisualTrace** , we provide ground truth trajectories consisting of eight points. When the predicted trajectory length deviates from the ground truth, we employ interpolation to align their lengths. To ensure consistent evaluation across varying image resolutions, all coordinates are uniformly normalized to a range of 0 to 1000. Subsequently, we employ a combination of Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and **GPT Score** to comprehensively evaluate performance. 

Here, we detail the design philosophy and evaluation procedure of the GPT Score. Given that multiple valid solutions can exist for each task instruction, relying solely on trajectory similarity to the ground truth as a scoring criterion can be one-sided. Therefore, we established detailed evaluation criteria to simulate realistic human assessment. Based on these rules, we introduced a visualized trajectory scoring method leveraging Multimodal Large Language Models (MLLMs), termed **GPT-score** . 

Specifically, we designed an evaluation prompt to guide GPT-4.1 in assessing predicted object manipulation trajectories based on both task instructions and visual inputs. The prompt provides clear instructions and criteria, positioning the model as an expert evaluator in robotic manipulation and visual reasoning. Each evaluation instance consists of a task instruction and an accompanying image that visualizes the predicted trajectory, where a red circle indicates the start point and a blue diamond marks the end point. The model is instructed to assess the trajectory according to three key criteria: (1) task alignment and success, determining whether the predicted path correctly fulfills the instruction by starting and ending in appropriate locations; (2) feasibility, evaluating the physical plausibility and smoothness of the motion; and (3) obstacle avoidance, considering whether the trajectory avoids potential collisions. The prompt emphasizes that completing the task correctly is the most important factor; any major deviation in goal achievement results in a low score, even if the trajectory appears smooth or feasible. Then, the model returns a structured response consisting of a numerical score from 1 to 10, along with a concise 

28 

explanation. Scores are interpreted based on task success and quality: low scores (1–4) indicate failure to accomplish the task, mid-range scores (6–8) reflect successful but imperfect trajectories, and high scores (9–10) are reserved for trajectories that are both accurate and high-quality. This scoring scheme allows for nuanced, human-like evaluation that integrates both semantic understanding and visual reasoning. By leveraging this multimodal prompt framework, GPT-score enables a robust and interpretable evaluation process that aligns closely with human judgment, overcoming the limitations of purely geometric or distance-based metrics. The complete prompt is presented as follows: 

29 

#### Complete Prompt for GPT Score Metrics 

You are an expert evaluator in robotic manipulation and visual reasoning. Your job is to assess the quality of predicted trajectories based on task instructions and visual inputs. 

You are given: 

- A task instruction describing an object manipulation task. 

- An image showing a predicted trajectory. 

#### **Note:** 

- In the image, the red circle indicates the start point, and the blue diamond indicates the end 

- point. 

- The trajectory represents the predicted movement path of the manipulated object, not the robot or end-effector. 

- You should **evaluate the predicted trajectory as a proposed motion for the object that is supposed to be moved**, based on the task instruction — **not based on the static positions of objects in the image**. The objects have not actually moved. 

#### **Evaluation Criteria (listed in order of importance):** 

1. **Task Alignment and Success (most important)** - Does the trajectory clearly and accurately fulfill the task instruction? - **The trajectory must start at the correct location and end at a target position that aligns with the task goal.** - Large deviations in the starting or ending point (e.g., wrong object, wrong destination, or stopping short of the goal) should result in a low score, even if the rest of the trajectory is smooth. - If the task is not accomplished (due to incorrect goal interpretation or spatial execution), the score should be low regardless of other qualities. 

2. **Feasibility** - Is the movement physically plausible, smooth, and continuous? - Are there any unrealistic discontinuities, sharp turns, or impossible transitions? - Even if the movement is feasible, it should not receive a high score if the task is not completed. 

3. **Obstacle Avoidance / Safety** - Does the trajectory reasonably avoid collisions with surrounding objects? - Minor risks may be tolerated if the task is completed successfully, but major or clear collisions should reduce the score. 

#### **Scoring Guideline:** 

- If the task is **not accomplished**, or if the start or end point is significantly incorrect, the score should typically be **4 or below**. 

- If the task is completed but the trajectory has issues (e.g., roughness, minor risk of collision), a score in the **6–8** range is appropriate. 

- A **score of 9–10** should be given only when the trajectory clearly completes the task, with good start/end accuracy, smooth motion, and reasonable safety. 

Based on these criteria, provide a single overall score from 1 (very poor) to 10 (excellent), reflecting how well the task is accomplished. 

Respond strictly in the following format: Score: <1-10> Explanation: <brief justification> 

The task instruction is: {task_instruction} 

Please give your response. 

30 

**Table 6** Details of the training data for FSD 

|**Stage**|**Task**|**Datasets**|**Samples**|**Data Sources**|
|---|---|---|---|---|
||GeneralQA<br>(Caption,<br>VQA,<br>OCR, RegionVQA, Conversation,<br>Grounding, Text)|ShareGPT4V, VQAv2, OCR-VQA,<br>Visual7W,<br>ST-VQA,<br>RefCO-<br>CO/+/g, VG, AS-Core, AS-V2,<br>TextVQA, Visual7W|838k|LLaVA<br>Liu<br>et<br>al.<br>(2024b),<br>ASMv2Wang et al.(2025)|
|Stage 1|General Spatial Reasoning|KITTI, 2D3DS, ObjectRef, Re-<br>gionRef, VSR, CLEVR, CLEVR-<br>Math, SUPER-CLEVR, RAVEN|295k|SpatialBot Cai et al. (2024),<br>RoboPointYuan et al.(2024b),<br>SAT Ray et al. (2024), LLaVA-<br>OneVisionLi et al.(2024a)|
||Embodied Spatial Reasoning|FSD Level 1 (145k),<br>Level<br>2 (86k) and Level 3 (19k)|250k|FSD|
||Spatial Affordance Generation<br>& Understanding|FSD Level 4 (24k)|24k|FSD|
|Stage 2|Visual Trace Generation & Un-<br>derstanding|FSD Level 5 (26k)|26k|FSD|


## **E Details of Benchmarks and Baselines** 

For **general spatial reasoning tasks** , the answers are typically multiple-choice questions with clear options. However, some spatial reasoning models show reduced instruction-following ability after fine-tuning, preventing them from directly outputting the correct option. To address this, we use a **lenient matching rule** , considering an answer correct if it includes either the correct content or the corresponding option. 

For **object/region reference tasks** , we carefully fine-tuned and used a tailored prompt for each model. Most models, such as GPT-4o and ASMV2 Wang et al. (2025), cannot directly output specific points. Similar to the validation process for RoboPoint Yuan et al. (2024b), we also found that using in-context learning to specify point output formats resulted in worse performance compared to directly outputting bounding boxes. Therefore, for these models, we instructed them to output bounding boxes directly. From these bounding boxes, we either uniformly sampled nine points or took the midpoint. Then, we calculated the proportion of points within the specified region to determine the final average accuracy. 

For the **VABench-VisualTrace task** , due to a lack of strong baselines, we developed an additional Transformer-based prediction model, trained from scratch using the same data, which we named **DINOv2 Predictor** . In the DINOv2 Predictor, the visual encoder uses a pre-trained DINOv2 Oquab et al. (2023), encoding images to output a (196, 768) feature vector. The language encoder uses a pre-trained T5Base Raffel et al. (2020), outputting (32, 768). These are concatenated with learnable embeddings (8, 768) and passed through a Transformer encoder base. The output of the learnable embeddings is then read and passed through a linear layer to predict eight points. During training, we keep the language encoder fully frozen and train the visual encoder along with the other remaining parameters. 

## **F More Visualizations and Examples** 

We present the prediction results of FSD on Where2place Yuan et al. (2024b), Roborefit Lu et al. (2023), and VABench in figure 13, figure 14, and figure 15, respectively. 

31 


**Figure 13 Visualization of visual aids generated by FSD in the Where2Place benchmark.** 

## **G Real World Experiment Results** 

In our real-world desktop manipulation tasks, we used an xArm 6 robotic arm for evaluation. This setup included an Intel RealSense L515 LiDAR camera and a force-torque sensor on the xArm to enable compliance control, which improved interaction with the environment. A computer running Ubuntu 24.04 and equipped with an NVIDIA GTX 1660 was directly connected to the arm and camera to execute low-level control policies. Notably, a single RealSense L515 depth camera was sufficient for task completion, especially when performing visual trace execution. This approach eliminated the need for object segmentation and 3D mapping; instead, we directly mapped 2D visual trajectories to 3D for execution, with no strict requirements on depth information accuracy. Demonstrations are available in figure 9 and on our website. 

## **H Prompt for Using FSD Model** 

Generate Spatial Affordance Points & Bounding Box 

You are currently a robot performing robotic manipulation tasks. Your task instruction: { `Task Instruction` } . Observe the image, use 2D points and bounding box to mark the target location where the manipulated object will be moved. In your answer, use <box>[[x1, y1, x2, y2]]</box> to present the bounding box of the target region, and use <point>[[x1, y1], [x2, y2], ...]</point> to mark the points of the free space. 

32 


**Figure 14 Visualization of visual aids generated by FSD in the RoboRefit benchmark.** 

#### Generate Visual Trace 

You are currently a robot performing robotic manipulation tasks. Your task instruction: { `Task Instruction` }. Observe the image, use 2D points to mark the manipulated object-centric waypoints to guide the robot to manipulate the object.Typically, the waypoints consists of an ordered sequence of eight 2D points. The format is <point>[[x1, y1], [x2, y2], ...]</point>. 

## **I Comparison of FSD and RoboBrain** 

Both FSD and RoboBrain Ji et al. (2025) have the capability to generate visual trace. However, RoboBrain tends to produce agent-centric visual trace, whereas FSD generates object-centric visual trace. FSD adopts a task-centric design principle, allowing it to perform effectively even in more heterogeneous ontological scenarios, including those that completely lack robotic arms in the image, thus exhibiting stronger generalizability. Due to the differences in the methods of generating visual trace, we conducted several sets of visual trajectory visualizations for qualitative analysis, as shown in figure 16. Under the same zero-shot setting, the visual trace generated by FSD has higher accuracy compared to those generated by RoboBrain, confirming that FSD’s reasoning-based pipeline possesses greater generalizability when facing unknown tasks. 

33 

## **J Future Works** 

We have made preliminary attempts to use visual aids as intermediate states in FSD, achieving promising results in object/target/region reference and actual manipulation task execution. Future work can focus on the following aspects to further enhance the applicability of this paradigm: 1. **Task Decomposition for Complex and Long-Horizon Instructions:** The current version of FSD primarily targets clear and explicit language instructions. When dealing with long-horizon tasks or ambiguous/complex instructions, the model needs to decompose them into atomic, executable sub-tasks. We believe that decomposing instructions into a sequence of visual aids to guide each sub-task execution is a promising avenue. 2. **Downstream Execution and Visual-Aid-Guided Control:** Currently, FSD relies mainly on training-free motion planning methods for downstream execution. In extremely complex or dynamic scenarios, this may lead to a bottleneck in success rates. A potential improvement is to use the generated visual aids as explicit guidance for downstream VLA models, replacing language-conditioned training. Several preliminary studies Zheng et al. (2024); Bharadhwaj et al. (2024); Li et al. (2025) have shown that, for robotic manipulation tasks, affordance and visual trajectories provide more effective guidance than language prompts. 3. **Extending from 2D to 3D Visual Aids:** At present, FSD focuses on predicting 2D visual aids, similar to the representation used in Referring Expression Comprehension (REC) and related tasks, which leverages the general visual understanding and reasoning capabilities of VLMs. However, as task and scene complexity increases, predicting 3D visual traces may prove to be a more effective solution, and we identify this as an important direction for future research. 

34 


**Figure 15 Visualization of visual aids generated by FSD in the VABench benchmark.** FSD can generate three types of visual aids based on task instructions for novel tasks and scenarios. 1st-2nd row: visual trace; 3rd-4th row: affordance points; 5th-6th rows: affordance bounding box. 

35 


**Figure 16 Comparison of generated visual traces between FSD and RoboBrain.** 

36 

