---
title: "Interleave-VLA: Enhancing Robot Manipulation with Image-Text Interleaved Instructions"
date: "2026"
venue: "ICLR 2026 Poster"
url: https://arxiv.org/abs/2505.02152
pdf: https://arxiv.org/pdf/2505.02152
converter: pymupdf4llm
---

> **[PDF を開く](https://arxiv.org/pdf/2505.02152)** / [論文ページ](https://arxiv.org/abs/2505.02152)
>
> PDF から自動変換した本文です。図は含まず、数式と表は崩れている場合があります。

Preprint. 

INTERLEAVE-VLA: ENHANCING ROBOT MANIPULATION WITH INTERLEAVED IMAGE-TEXT INSTRUCTIONS 


Figure 1: **(a)** Our Interleaved X-Embodiment Dataset features diverse, high-quality object-centric images automatically generated from real-world robot demonstrations. **(b)** Interleave-VLA achieves **2** _×_ stronger out-of-domain generalization compared to text-only VLA models in both simulation and real-robot experiments. **(c)** It enables flexible, zero-shot instruction following with cropped images, web photos, and hand-drawn sketches for practical and intuitive human-robot interaction. 

## ABSTRACT 

The rise of foundation models paves the way for generalist robot policies in the physical world. Existing methods relying on text-only instructions often struggle to generalize to unseen scenarios. We argue that interleaved image-text inputs offer richer and less biased context and enable robots to better handle unseen tasks with in-context visual grounding. Building on this insight, we introduce Interleave-VLA, the first robot learning paradigm capable of comprehending interleaved image-text instructions and directly generating continuous action sequences in the physical world. It offers a natural, flexible, and modelagnostic paradigm that extends state-of-the-art vision-language-action (VLA) models with minimal modifications while achieving strong zero-shot generalization. Interleave-VLA also includes an automatic pipeline that converts text instructions from Open X-Embodiment into interleaved image-text instructions, 

> _∗_ Equal contribution 

> _†_ Correspondence Emails: yangxue-2019-sjtu@sjtu.edu.cn, yanjunchi@sjtu.edu.cn, 

> md@cs.unc.edu 

1 

Preprint. 

resulting in a large-scale real-world interleaved embodied dataset with 210k episodes. Comprehensive evaluation in simulation and real world show that Interleave-VLA offers two major benefits: **(1)** improves out-of-domain generalization to unseen objects by 2 _×_ compared to text input baselines, **(2)** supports flexible task interfaces and diverse instructions in a **zero-shot manner** , such as hand-drawn sketches. We attribute Interleave-VLA’s strong zero-shot capability to the use of instruction images, which effectively mitigate hallucinations, and the inclusion of heterogeneous multimodal datasets, enriched with Internet-sourced images, offering potential for scalability. Our website has more information. 

## 1 INTRODUCTION 

The remarkable success of large language models (LLMs) (Achiam et al., 2023; Touvron et al., 2023; Bai et al., 2023; Liu et al., 2024a) and vision-language models (VLMs) (Bai et al., 2025; Team, 2024; Liu et al., 2023a; Chen et al., 2024a; Luo et al., 2025) has established the paradigm of foundation models in the digital world, which are capable of generalizing across a wide range of tasks and domains. Inspired by this progress, the robotic community is actively developing robotic foundation models (Brohan et al., 2023; Kim et al.; O’Neill et al., 2024; Black et al., 2024; Intelligence et al., 2025; Chi et al., 2023) to bring similar generalizability to unseen tasks and scenarios into the physically embodied world. Despite these advances, effective out-of-domain generalization of robotic policies remains a key challenge. We argue that the predominant reliance on text-only instructions in current generalist robotic policies constrains their ability to generalize. Text instructions often prove ambiguous or cumbersome in scenarios where users need to specify goals like “pick up an object like this,” referring to a uniquely shaped or colored item. In contrast, interleaved image-text instructions allow robots to interpret unseen tasks more effectively by providing in-context visual and textual cues, beyond what text instructions alone can convey. 

To develop a general and practical robot policy capable of acting on interleaved image-text instructions in the real world, a straightforward solution is to build upon VLA (Kim et al.; O’Neill et al., 2024; Brohan et al., 2022; 2023; Black et al., 2024; Team et al., 2025) models, which naturally extend VLMs by incorporating action understanding and generation, making them well-suited for robotic tasks. However, current VLA models (Brohan et al., 2023; Kim et al.; Black et al., 2024) remain predominantly trained on text-only instructions—a setting we refer to as the TextVLA paradigm. This limits their ability to benefit from multimodal instruction signals, which have been shown to enhance generalization in vision-language learning (Achiam et al., 2023; Team et al., 2025). This restriction not only reduces instruction flexibility but also prevents these models from leveraging the richer semantics and improved grounding afforded by interleaved multimodal signals. 

To address this limitation, we first build a high-quality interleaved image-text datasets, crucial for training multimodal models. In order to bridge the gap of the lack of image-text interleaved datasets in robotic manipulation, we develop a pipeline to automatically construct interleaved instructions from existing datasets. The proposed pipeline enables automatic and accurate generation of interleaved instructions from real-world dataset Open X-Embodiment (O’Neill et al., 2024). The resulting interleaved dataset contains over 210k episodes and 13 million frames, making it a large-scale, real-world interleaved embodied dataset. This enables training Interleave-VLA with real-world interaction data and diverse visual instruction types. 

We then propose a new paradigm called Interleave-VLA, designed for generating continuous actions from interleaved inputs. As illustrated in Figure 2, Interleave-VLA consists of three key components: **(1)** a lightweight adaptation module that introduces special separator tokens into the tokenizer, enabling existing VLAs to process interleaved inputs without architectural changes, **(2)** a scalable training pipeline that leverages large-scale interleaved embodied datasets while preserving original objectives and hyperparameters, and **(3)** a versatile inference interface that supports both text-only and interleaved instructions, allowing the use of real-world camera crops, web images, or even sketches at test time. This effective design unlocks multimodal instruction-following capabilities for state-of-the-art VLAs in _π_ 0 and can be readily extended to other VLA models, such as OpenVLA (Kim et al.). Experimental results demonstrate that Interleave-VLA significantly surpasses text-only baselines in out-of-domain tasks. The interleaved format enables robust zero-shot generalization to novel objects and user-provided sketches unseen during training. 

2 

Preprint. 

We further investigate the factors behind Interleave-VLA’s superior zero-shot performance relative to Text-VLA. We find that both the scale and heterogeneity of the Interleaved X-Embodiment Dataset contribute to consistent gains in both low- and high-data regimes. We also categorize three recurring forms of attentional hallucination in Text-VLA: _attentional bias_ , _diffused attention_ , and _attention leakage_ , which arise from linguistic ambiguity and distributional biases in text-only instruction interpretation. We summarize our key takeaways below: 

- Generalization failures in VLAs often stem from **attentional hallucinations** , which we summarized as attentional bias, diffused attention, and attention leakage, driven by **(1)** ambiguous contexts and **(2)** training distribution biases (Section 4.1). 

- Interleaved image-text instructions mitigate the hallucination caused by **ambiguous contexts** , providing less-biased in-context visual grounding for better generalization (Figure 5 in Section 4.1). 

- Modality diversity (e.g, interleaved data, web data) alleviates the hallucination from **training distribution biases** , further enhancing generalization. Cross-modal training benefits performance in both interleaved evaluation and text-only evaluation (Section 4.3.3). 

Our core contribution is threefold. **(1)** We introduce Interleave-VLA: a lightweight, transferable paradigm that enhances the generalization capability of current text input VLA models with interleaved image-text instructions. Through comprehensive evaluation, we demonstrate **2** _×_ gains in out-of-domain generalization to novel objects, along with emergent zero-shot capabilities for interpreting diverse visual instructions, such as **hand-drawn sketches** . **(2)** We opensource a large-scale, real-world interleaved embodied dataset with 210k episodes and 13 million frames based on Open X-Embodiment, generated by a fully automated pipeline. **(3)** We provide insights into InterleaveVLA’s effectiveness in mitigating attentional hallucinations commonly observed in Text-VLA. 

## 2 RELATED WORK 

**Interleaved Vision-Language Models.** In the digital domain, recent advances in vision-language models have evolved from handling simple image-text pairs (Liu et al., 2023a; Radford et al., 2021; Li et al., 2023; Fang et al., 2023) to processing arbitrarily interleaved sequences of images and text (Bai et al., 2025; Team, 2024; Chen et al., 2024a; Luo et al., 2025; Xue et al., 2024; Li et al.; Alayrac et al., 2022; Chen et al., 2024b; Jiang et al.). This interleaved format allows models to leverage large-scale multimodal web corpora—such as news articles and blogs—where images and text naturally appear in mixed sequences. Such models have demonstrated improved flexibility and generalization, enabling transfer across diverse tasks and modalities (Li et al.). Despite these successes in the digital world, robotic foundation models in the physical world have yet to fully exploit the benefits of interleaved image-text instructions. Motivated by the progress of interleaved VLMs, we extend this paradigm to the action modality, enabling vision-language-action models to process interleaved instructions. Our results show that multimodal learning with interleaved inputs greatly boosts generalization and displays emergent capabilities in robotic manipulation tasks. 

**Vision Language Action Models.** Vision-language-action (VLA) models have advanced robotic manipulation by enabling policies conditioned on both visual observations and language instructions (Kim et al.; O’Neill et al., 2024; Brohan et al., 2022; 2023; Black et al., 2024; Team et al., 2025; Fang et al., 2025; Wen et al., 2025). Most prior VLA models process single (Kim et al.) or multiple (Brohan et al., 2023; Black et al., 2024) observation images with text-only instructions, with some exploring additional modalities such as 3D (Zhen et al., 2024) and audio (Zhao et al.). Only few existing works, such as VIMA (Jiang et al., 2023), explore the use of interleaved instructions in robotics, evaluating vision-language planning tasks within a high-level 2D action space in simulation. However, they have not investigated the broader benefits of interleaved instructions, such as (1) their advantages over text-only instructions and (2) their applicability to real-world scenarios involving low-level robotic actions. As a result, the practical value of this paradigm remains underexplored due to a lack of real-world datasets and policies capable of handling such input In this work, we make the first step to bridge this gap by proposing Interleave-VLA: a simple, modelagnostic paradigm that extends existing VLA models to support interleaved image-text instructions with minimal modifications. Our comprehensive experiments demonstrate that interleaved instructions substantially improve generalization to unseen objects and environments, and unlock strong zero-shot capabilities for diverse user-provided inputs. This highlights the practical value and scalability of interleaved image-text instructions for real-world robotic manipulation. 

3 

Preprint. 


Figure 2: Overview of the Interleave-VLA paradigm, featuring an extendable adaptation of TextVLA to handle interleaved inputs, scalable training on a constructed large interleaved dataset, and versatile inference that supports a wide range of interleaved instructions. 

3 INTERLEAVE-VLA AND OPEN INTERLEAVED X-EMBODIMENT DATASET 

### 3.1 PROBLEM FORMULATION 

A discrepancy exists between the input modalities of modern Vision-Language Models (VLMs) (Alayrac et al., 2022; Bai et al., 2025; Team, 2024; Xue et al., 2024), which accept arbitrarily interleaved inputs, and most Vision-Language-Action (VLA) models, which typically operate on a single text instruction. We formally define this text-only instruction paradigm as **Text-VLA** . In this work, we propose **Interleave-VLA** , a generalized paradigm that allows a robotic policy to generate actions conditioned on interleaved image-text inputs. This formulation elevates VLA models to the same input flexibility as VLMs, thereby rendering Text-VLA a specialized instance. 

Formally, a policy _πθ_ under the Interleave-VLA paradigm generates an action _at_ at each timestep _t_ by sampling from a distribution conditioned on the state _st_ : _at ∼ πθ_ ( _· | st_ ) where the state is defined as a tuple _st_ = ( _It,_ **q** _t, I_ ). This tuple comprises the current visual observation _It_ (e.g., an image or set of images), the robot’s proprioceptive state **q** _t_ , and an interleaved instruction sequence _I_ . The ordered instruction sequence is represented as _I_ = ( _u_ 1 _, . . . , uM_ ), where each token _uj ∈V_ text _∪V_ img belongs either to the set of text tokens _V_ text or to the set of image tokens _V_ img. Notice that InterleaveVLA can degenerate to special case of standard Text-VLA when all _uj ∈V_ text. 

We show a typical example of a standard text-only instruction and interleaved instruction: 

Text-only: <obs> Place [the blue spoon near microwave] into [silver pot on towel]. Interleaved image-text: <obs> Place [image1 ] into [image2 ]. where <obs> stands for observation image(s), and [image1 ] and [image2 ] are interleaved instruction images. As shown in Figure 1, Interleave-VLA supports more flexible formats. 

### 3.2 INTERLEAVE-VLA PARADIGM 

Outlined in Figure 2, our Interleave-VLA paradigm, designed for generating continuous actions in the real world from interleaved inputs, comprises three core components: **(1)** a straightforward and effective adaptation module, **(2)** a scalable training process tailored for interleaved data, and **(3)** a versatile inference interface that supports interleaved instructions. 

**Adaptation.** Interleave-VLA extends Text-VLA by introducing special separator tokens into the tokenizer of the base VLA model, allowing it to distinguish between image and text tokens. The input processor is updated to support the interleaved format, while the core VLA architecture remains unchanged. This paper focuses on applying Interleave-VLA to _π_ 0 (Black et al., 2024), a state-of-the-art Text-VLA model. Despite its pretrained Paligemma (Beyer et al., 2024) lacking native support for interleaved data, Interleave-VLA enables this capability. Our adaptation is effective in enhancing the zero-shot generalization potential of _π_ 0. Moreover, the simplicity of this adaptator makes it easily applicable to other VLA models, such as OpenVLA (Kim et al.). For further details on our model-agnostic adaptation, see Appendix A. 

**Training.** We train the interleaved-adapted _π_ 0 model using the large-scale interleaved embodied dataset from Section 3.3, without modifying its hyperparameters or flow matching objective. The training process efficiently scales with the dataset size and cross-modal instruction diversity. 

**Inference.** Interleave-VLA paradigm supports both text and interleaved instructions during inference, with interleaved inputs significantly improving generalization to unseen scenarios. Interleaved 

4 

Preprint. 


Figure 3: **Left:** Our open interleaved X-Embodiment dataset features a large number of high-quality cropped images with diversity across objects. **Right:** Interleave dataset generation pipeline: (1) Instruction Parsing: use LLM to extract key objects from language instructions. (2) Open-Vocabulary Detection: use OWLv2 to locate and crop target objects from trajectory frames based on the parsed instruction keywords. (3) Data Quality Verification: use Qwen2.5-VL to verify the detected objects, and if needed, provide keypoints for more precise segmentation using Segment Anything. 

images in prompts offer great versatility, as they can be sourced from diverse sources such as robot camera crops, web images, or hand-drawn sketches, even when the image styles differ from those in the robot’s training data. To simplify interaction with the robot, we also design a user-friendly GUI. 

### 3.3 CONSTRUCTION OF OPEN INTERLEAVED X-EMBODIMENT DATASET 

A large-scale and high-quality pretraining dataset scales up vision-language-action (VLA) (Black et al., 2024; Brohan et al., 2023; Kim et al.) training. However, current real-world datasets only include text instructions and thus do not support Interleave-VLA training. We consequently design a unified pipeline to automatically relabel and generate interleaved data across diverse datasets. 

Our overall dataset generation pipeline consists of three main steps: instruction parsing, openvocabulary detection, and data quality verification, as illustrated in Figure 3. **First** , we use Qwen2.5 (Yang et al., 2024) to extract key objects from language instructions. Unlike rule-based NLP tools like SPaCy (Honnibal, 2017), Qwen2.5 adapts to diverse instruction formats without requiring case-specific rules. It also effectively summarizes lengthy instructions, such as those in datasets like (Shah et al., 2023). **Second** , for open-vocabulary detection, we use the open-vocabulary detector OWLv2 (Minderer et al., 2023) to locate and crop target objects from trajectory frames based on the parsed instruction keywords, achieving 82.6% accuracy. **Finally** , we introduce data quality verification for harder cases where OWLv2 fails: Qwen2.5-VL (Bai et al., 2025) verifies the detected objects, and if needed, provides keypoints for more precise segmentation using Segment Anything (Ravi et al., 2024). This collaborative approach leverages the complementary strengths of VLMs, raising accuracy to 95.6%. Detailed metrics and analysis are provided in Appendix B. 

We release a large-scale interleaved cross-embodiment dataset in the real world, featuring diverse tasks and instructions. This dataset integrates 11 datasets from Open X-Embodiment (O’Neill et al., 2024), including RT-1 (Brohan et al., 2022), Berkeley Autolab UR5 (Chen et al.), IAMLab CMU Pickup Insert (Saxena et al., 2023), Stanford Hydra (Belkhale et al., 2023), UTAustin Sirius (Liu et al., 2023b), Bridge (Walke et al., 2023a), Jaco Play (Dass et al., 2023), UCSD Kitchen (Yan et al., 2023), BC-Z (Jang et al., 2022), Language Table (Lynch et al., 2023), and UTAustin Mutex (Shah et al., 2023). The curated dataset comprises 210k episodes and 13 million frames, spanning 3,500 unique objects and a wide range of task types. To enhance instruction diversity, we augment our dataset by randomly integrating Internet-sourced images alongside the original text instructions. 

## 4 EXPERIMENTS 

In the experiments, our aim is to answer the following research questions: 

(1) How does our Interleave-VLA paradigm compare to conventional Text-VLA paradigm? 

5 

Preprint. 


Figure 4: **Left** : Illustration of generalization settings in SIMPLER. (a) Visual generalization: unseen environments, tablecloths, and lighting conditions. (b) Semantic generalization with novel objects from known categories. (c) Semantic generalization with objects from entirely new categories not seen during training. **Right** : Real-world generalization experiments. In-Domain and out-of-Domain settings in the real world on a FANUC LRMate 200iD/7L robotic arm. 

(2) What are the common failure modes of Text-VLA, and how does Interleave-VLA address them? 

(3) What are the benefits of each stage of Interleave-VLA paradigm’s design? 

### 4.1 SIMULATION COMPARISON WITH TEXT-VLA 

**Task setup.** We use SimplerEnv (Li et al., 2024), a real-to-sim evaluation suite, to efficiently evaluate policies in realistic scenarios. Performances are tested on SimplerEnv-Bridge setup, which uses a WidowX robot configuration compatible with the BridgeData V2 (Walke et al., 2023b). Since SimplerEnv is built for Text-VLA, to enable scalable evaluation of Interleave-VLA models, we extend SimplerEnv with interleaved image–text prompts via automated pipeline (Section 3.3). 

In addition to the four SimplerEnv-Bridge tasks from BridgeData V2, we include ten new tasks for generalization evaluation. Following commonly used Stone et al. (2023), these tasks focus on assessing both _visual generalization_ and _semantic generalization_ . _Visual generalization_ assesses robustness to novel foreground, lighting, and environment backgrounds. _Semantic generalization_ assesses the model’s ability to manipulate in novel scenarios and the presence of diverse distractors. This evaluation is further divided into two sub-categories: **(1)** novel objects from previously seen categories, and **(2)** objects from entirely unseen categories. See left part of Figure 4 for an overview. 

**Baselines.** We evaluate Interleave-VLA against leading Text-VLA models, including RT-1-X (Brohan et al., 2022), Octo (Team et al., 2024), and SoTA _π_ 0 (Black et al., 2024). To directly compare with Text-VLA, we implement Interleave-VLA (Partial) on _π_ 0, which is trained with interleaved inputs but tested with text-only instructions. Finally, we evaluate the full potential of the InterleaveVLA paradigm, where _π_ 0 is both trained and tested using interleaved inputs. Both Interleave-VLA and Text-VLA paradigms are trained on trajectories from BridgeData V2 (Walke et al., 2023a). 

**Results.** In-domain results in Table 1 show that our Interleave-VLA paradigm performs on par with Text-VLA for familiar tasks, demonstrating that interleaved instructions are interpretable thanks to Interleave-VLA training process. For out-of-domain tasks, Interleave-VLA (Partial) already outperforms Text-VLA, benefiting from the multimodal nature of interleaved data, which helps mitigate overfitting. The full Interleave-VLA further enhances generalization, achieving 2 _×_ better performance on semantically out-of-domain tasks. 

**Analysis.** The substantial performance gains of Interleave-VLA (Full) over Text-VLA and Interleave-VLA (Partial) mainly stem from the explicit visual grounding supplied by interleaved instruction images, which reduces a phenomenon we term **attentional hallucination** . To qualitatively illustrate this, we compute the attention scores of target object tokens relative to the tokenized observation in out-of-domain settings. As shown in Figure 5, we identify three primary failure patterns: **(1)** _Attentional Bias_ , where focus is incorrectly allocated to prominent distractor instead of the target object; **(2)** _Diffused Attention_ , characterized by a complete lack of a focal point as attention spreads thinly across the entire scene, suggesting model uncertainty; and **(3)** _Attention Leakage_ , where the model correctly identifies the target but its focus is not tightly contained, scattering onto 

6 

Preprint. 

Table 1: Interleave-VLA and Text-VLA comparison on **SimplerEnv** . **In-Domain** includes 4 tasks following SimplerEnv-Bridge setup. We add 3 **Out-of-Domain** evaluation suites, namely: Visual, Novel Object, and Novel Category corresponding to (a), (b), and (c) respectively on the left of Figure 4. Interleave-VLA (full version) performs better than Text-VLA by over 2 _×_ in out-of-domain semantic generalization tasks. We use **bold** and underline to represent the 1<sup>_st_</sup> and 2<sup>_nd_</sup> highest. 

|**Base Model**|**Parad**|**igm**|**Train/Eval**|**In-Domain**||**Out-of-D**|**omain**|
|---|---|---|---|---|---|---|---|
||||**Modality**||**Visual**|**Novel Object**|**Novel Category**<br>**Avg.**|
|RT-1-X (O’Neill et al., 2024)|Text-|VLA|Text/Text|1.1|0.0|4.0|6.1<br>3.4|
|Octo (Team et al., 2024)|Text-|VLA|Text/Text|17.5|12.6|10.8|8.4<br>10.6|
|_π_0(Black et al., 2024)|Text-<br>|VLA<br>|Text/Text|69.2|71.4|30.2|21.0<br>40.9|
|_π_0(Black et al., 2024)|Interleav<br>(Part|e-VLA<br>ial)|Interleave/Text|**71.9**|69.9|35.1|27.5<br>44.2|
|_π_0(Black et al., 2024)|Interleav<br>(Fu|e-VLA<br>ll)|Interleave/Interleave|71.0|**73.4**|**55.7**|**53.0**<br>**60.7**|
|Zucchini||Stapler|Tape<br>Measure||Tennis|Redbull|Toy<br>Dinosaur|
|**Text-VLA**||||||||
|**AttentionLea**<br>**Interleave**<br>**-**<br>**VLA**|**kage**||**Diffused A**|**ttention**||**Attentio**|**nal Bias**|


Figure 5: Qualitative analysis of Interleave-VLA’s improved performance over the Text-VLA paradigm. In out-of-domain SimplerEnv tasks with unfamiliar objects, Text-VLA displays **attentional hallucination** , which typically manifests in three categories: **(1)** _Attention Leakage_ : the target is partially attended, but focus spills onto irrelevant background or distractor regions; **(2)** _Diffused Attention_ : attention is broadly scattered with no dominant focus, indicating uncertainty about the target; **(3)** _Attentional Bias_ : attention centers on a salient distractor instead of the true target. Interleave-VLA effectively mitigates these issues by leveraging in-context visual cues from interleaved instructions, demonstrating consistent attention on target objects. 

irrelevant background areas. These failures can be attributed to semantic ambiguity in cluttered visual contexts and distributional bias in the training data. For example, **semantic ambiguity** arises when the instruction says “toy dinosaur” but a similarly shaped toy elephant is present, the text-only Text-VLA model often makes an arbitrary choice; **distributional bias** manifests when Text-VLA misidentifies a Red Bull can as a Coca-Cola can because the rare token “redbull” is segmented into “red” + “bull”, causing it to over-attend to “red” and biasing attention toward the familiar red Coca-Cola can. These built-in biases are difficult to address with conventional Text-VLA. In contrast, Interleave-VLA outperforms Text-VLA baselines _by leveraging in-context visual grounding and cross-modality training to reduce attentional hallucinations_ . 

### 4.2 REAL ROBOT COMPARISON 

**Task setup.** We evaluate on a FANUC LRMate 200iD/7L robotic arm equipped with an SMC gripper. Two manipulation tasks are considered: (1) picking up food or fruits, and (2) picking and placing kitchenware. To assess _semantic generalization_ , we follow the SimplerEnv setup. See the right part of Figure 4 for an overview, with additional details in Appendix C.3. 

**Baselines.** All baselines use the same base VLA model _π_ 0, with two following the Interleave-VLA paradigm and one using Text-VLA. Each baseline is finetuned on 20 teleoperated demonstrations per object, collected using a space mouse. Optionally, pretraining is performed on the robot data in Section 3.3, training Text-VLA on text instructions and Interleave-VLA on interleaved instructions. 

**Results.** Table 2 shows that Interleave-VLA achieves **2-3** _×_ higher out-of-domain performance compared to Text-VLA when both are pretrained. Unlike the SimplerEnv experiments, where large-scale BridgeData V2 supports strong performance, the real-robot setup relies on a smaller self-collected dataset. In this low-data regime, directly finetuning _π_ 0 performs poorly (first row). Pretraining 

7 

Preprint. 

Table 2: Comparison of success rates (Succ) and correct object picking rates (Acc) in real-robot experiments. All the baselines use the base VLA model _π_ 0. Interleave-VLA adapted achieves **23** _×_ **higher out-of-domain performance** compared to Text-VLA. “PT” indicates pretraining on our interleaved dataset built in Section 3.3. Notably, although the pretraining dataset does not include FANUC robot arm data, it still enables strong cross-embodiment transfer to FANUC. 

||||||**In-Do**|**main**||||||**Out-of-**|**Domain**|||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Paradigm**|**PT**|pep|per|co|rn|cu|p|**A**|**vg**|be|an|lem|on|**Av**|**g**|
|||_Succ._|_Acc._|_Succ._|_Acc._|_Succ._|_Acc._|_Succ._|_Acc._|_Succ._|_Acc._|_Succ._|_Acc._|_Succ._|_Acc._|
|Interleave-VLA|✗|17|33|0|33|0|33|6|33|0|40|0|33|0|37|
|Text-VLA|✓|58|83|33|**100**|25|**100**|39|94|8|8|17|42|13|25|
|Interleave-VLA|✓|**58**|**100**|**75**|**100**|**67**|**100**|**67**|**100**|**75**|**100**|**67**|**100**|**71**|**100**|
|||pasta<br>_Succ._|server<br>_Acc._|spo<br>_Succ._|on<br>_Acc._|kn<br>_Succ._|ife<br>_Acc._|A<br>_Succ._|vg<br>_Acc._|spat<br>_Succ._|ula<br>_Acc._|black s<br>_Succ._|patula<br>_Acc._|A<br>_Succ._|vg<br>_Acc._|
|Interleave-VLA|✗|33|67|8|58|17|58|19|61|0|67|0|50|0|59|
|Text-VLA|✓|**58**|**83**|**58**|75|**33**|58|**50**|**72**|8|8|33|42|21|25|
|Interleave-VLA|✓|50|67|**58**|**83**|**33**|**58**|47|69|**25**|**100**|**50**|**67**|**38**|**84**|


on the Interleaved X-Embodiment dataset significantly boosts performance through effective crossembodiment transfer, reducing the need for laborious data collection. 

### 4.3 ANALYSIS OF INTERLEAVE-VLA’S GENERALIZATION AND EMERGENT CAPABILITIES 

### 4.3.1 INTERLEAVE-VLA ADAPTATION: EXTENDING TO OTHER VLA MODELS 

The model-agnostic design of Interleave-VLA allows easy adaptation to other VLA models, demonstrating its effectiveness in enhancing manipulation generalization across diverse architectures. To validate this, we extend Interleave-VLA to OpenVLA (Kim et al.), a state-of-the-art VLA model with a distinct architecture and training objective compared to _π_ 0. We evaluate it on VIMABench (Jiang et al., 2023), which includes four levels of manipulation planning tasks involving objects with irregular, cartoon-like shapes and textures. As shown in Figure 6, we compare InterleaveVLA against several end-to-end baselines, including the Text-VLA model OpenVLA and other VIMA-like models such as VIMA-Gato, VIMA-Flamingo, and VIMA-GPT (Jiang et al., 2023). Across all four generalization levels, our general Interleave-VLA paradigm, when directly extended to OpenVLA, achieves the best performance without relying on any task-specific designs. Details on the adaptation and evaluation are provided in Appendices A.2 and C.2. 

### 4.3.2 INTERLEAVE-VLA INFERENCE: FLEXIBILITY AND EMERGENT GENERALIZATION 

The inference interface of Interleave-VLA, which we show effectively reduces attentional hallucination problem, is highly versatile. Interleave-VLA demonstrates strong performance across diverse ways of specifying instructions in VIMA-Bench, including goal image matching and multi-image instruction following. These results demonstrate the flexibility of the Interleave-VLA paradigm, driven by its unified image-text interleaved instructions for general robotic manipulation. 


Figure 6: **VIMA-Bench** results across four generalization levels: L1 (object placement), L2 (novel combination), L3 (novel object), and L4 (novel task). To demonstrate the extendability of our Interleave-VLA paradigm, we apply it to another Text-VLA model, OpenVLA. InterleaveVLA outperforms Text-VLA by 2 2 _×_ across all difficulty levels, further highlighting its superior generalization capabilities with evidence from new task sets and a different base VLA model. 

Building on its versatile inference interface, (novel combination), L3 (novel object), and L4 Interleave-VLA further showcases an emergent (novel task). To demonstrate the extendability capability to interpret instructions in a comof our Interleave-VLA paradigm, we apply it to pletely **zero-shot manner** , directly handling another Text-VLA model, OpenVLA. Interleaveunseen input modalities without any additional VLA outperforms Text-VLA by 2 2 _×_ across all diffinetuning. Table 3 demonstrates the examples ficulty levels, further highlighting its superior genof image instruction types and their corresponderalization capabilities with evidence from new ing high performance. Instructions can be in ditask sets and a different base VLA model. verse formats, including: (1) **Cropped Image Instructions:** Users can directly crop a region from the screen to indicate the target object. (2) **Internet Image Instructions:** Users may supply any image—such as a photo retrieved from the Internet—to represent the desired object. (3) **Hand-Drawn Sketch Instructions:** Users can draw sketches or cartoons about their intentions. 

8 

Preprint. 

Table 3: Interleave-VLA unlocks powerful **zero-shot** generalization to diverse instruction modalities, including hand-drawn sketches, user-cropped images, and Internet photos, **without ever seeing them in training dataset** . The consistently high accuracy demonstrates that Interleave-VLA can robustly interpret and execute visually grounded instructions, showing strong potential for flexible and practical human-robot interaction. 

|**Task**|**Prompt A**|**A Succ. (%)**|**A Acc. (%)**|**Prompt B**|**B Succ. (%)**|**B Acc. (%)**|
|---|---|---|---|---|---|---|
|||58.3|90.0||48.8|86.0|
|||75.8|100||58.8|100|
|||71.7|100||80.8|100|
|||70.0|96.0||73.3|100|
|||69.6|100||76.3|100|
|||75.5|100||71.7|100|


The interleaved instruction format naturally accommodates diverse input types, making human-robot interaction more intuitive by removing the need for users to precisely describe complex objectives with detailed text. This flexibility significantly enhances the model’s ability to generalize, as evidenced by the improvements observed in both in-domain and out-of-domain tasks, where interleaved image-text instructions effectively reduce attentional hallucinations in VLA models. These advancements in Interleave-VLA collectively pave the way for more adaptable robotic systems. 

### 4.3.3 INTERLEAVE-VLA TRAINING: MODALITY AND INSTRUCTION DIVERSITY MATTER 

The most obvious scaling law of Interleave-VLA is dataset size, which is shown in large data domain (Appendix D) and low-data domain (Table 2). Overall, our results underscore the importance of the curated large-scale Interleaved X-Embodiment Dataset (Section 3.3) in fostering robust and generalizable Interleave-VLA. In this section, we delve deeper into the training data and identify two key factors that drive scalability and generalization: **(1)** the modality diversity of the dataset and **(2)** the diversity of prompt images. 

The **diversity of modalities** in training dataset Table 4: Ablation study on prompt image diversity is crucial for achieving robust performance for Interleave _π_ 0 on SimplerEnv. “In-Domain” reVLAs, particularly for out-of-domain genports the average performance on SIMPLER Vieralization. This principle is empirically sual Matching; “Out-of-Domain” averages results demonstrated by comparing the performance of on one unseen instruction from Table 3 and one Interleave-VLA (Partial) and Text-VLA, which unseen object from Figure 4 (left). Combining share an identical architecture (see Table 1). both task-specific and Internet images as prompts _π_ 0 trained with cross-modal, interleaved imageachieves the best overall performance. text instructions achieves absolute improve- **Data In-Domain Out-of-Domain** ments of +2 _._ 5 on familiar in-domain tasks and a more substantial +5 _._ 7 on tasks requiring genInternet Only 59.2 69.1 Task-specific Only 67.5 67.1 eralization to new objects. We attribute this Mixed **71.0 71.7** performance gain to the development of richer multimodal representations by mitigating the model’s tendency to overfit to unimodal text signals (Alayrac et al., 2022). 

**Instruction image diversity** is crucial as well, Table 4 demonstrates that combining Internet images with task-specific images cropped from robot observations yields the best overall performance. Using only Internet images leads to lower in-domain accuracy due to limited task relevance, while relying solely on cropped images improves in-domain results but lacks diversity. Mixing both sources provides complementary advantages, resulting in enhanced accuracy and stronger generalization. 

## 5 CONCLUSION 

Text-only instructions in most robotic policies can be insufficient for unseen scenarios and even causes hallucinations. To address this, we propose Interleave-VLA, a simple and effective paradigm for adapting existing Text-VLA models to process interleaved image-text instructions. To overcome the lack of real-world interleaved datasets, we develop an automatic pipeline that generates a large- 

9 

Preprint. 

scale dataset with 210k episodes and 13 million frames from Open X-Embodiment. With minimal modifications to current VLA models, Interleave-VLA achieves 2 _×_ improvement in generalization across both simulation and real-world experiments. Furthermore, our approach demonstrates strong emergent zero-shot generalization to diverse user instructions never seen during training—including hand-drawn sketches, cropped images, and Internet photos—making it both practical and flexible for real-world robotic applications. 

**Limitations.** While Interleave-VLA demonstrates strong generalization, training with interleaved inputs increases computational demands due to longer image token sequences. Future work could explore compressing image tokens for efficiency and extending VLA models to support interleaved outputs, such as text or images, alongside actions, which recent studies suggest can further enhance performance (Intelligence et al., 2025; Zhao et al., 2025). 

## REFERENCES 

- Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ , 2023. 

- Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc, Arthur Mensch, Katherine Millican, Malcolm Reynolds, et al. Flamingo: a visual language model for few-shot learning. _Advances in neural information processing systems_ , 35:23716– 23736, 2022. 

- Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, et al. Qwen technical report. _arXiv preprint arXiv:2309.16609_ , 2023. 

- Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhaohai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Junyang Lin. Qwen2.5-vl technical report. _arXiv preprint arXiv:2502.13923_ , 2025. 

- Suneel Belkhale, Yuchen Cui, and Dorsa Sadigh. Hydra: Hybrid robot actions for imitation learning. In _7th Annual Conference on Robot Learning_ , 2023. 

- Lucas Beyer, Andreas Steiner, Andr´e Susano Pinto, Alexander Kolesnikov, Xiao Wang, Daniel Salz, Maxim Neumann, Ibrahim Alabdulmohsin, Michael Tschannen, Emanuele Bugliarello, et al. Paligemma: A versatile 3b vlm for transfer. _CoRR_ , 2024. 

- Johan Bjorck, Fernando Casta˜neda, Nikita Cherniadev, Xingye Da, Runyu Ding, Linxi Fan, Yu Fang, Dieter Fox, Fengyuan Hu, Spencer Huang, et al. Gr00t n1: An open foundation model for generalist humanoid robots. _arXiv preprint arXiv:2503.14734_ , 2025. 

- Kevin Black, Noah Brown, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, Lachy Groom, Karol Hausman, Brian Ichter, et al. _π_ 0: A vision-language-action flow model for general robot control. _arXiv preprint arXiv:2410.24164_ , 2024. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, et al. Rt-1: Robotics transformer for real-world control at scale. _arXiv e-prints_ , pp. arXiv–2212, 2022. 

- Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Xi Chen, Krzysztof Choromanski, Tianli Ding, Danny Driess, Avinava Dubey, Chelsea Finn, et al. Rt-2: Vision-language-action models transfer web knowledge to robotic control. _arXiv preprint arXiv:2307.15818_ , 2023. 

- Lawrence Yunliang Chen, Simeon Adebola, and Ken Goldberg. Berkeley UR5 demonstration dataset. https://sites.google.com/view/berkeley-ur5/home. 

- Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong Ye, Hao Tian, Zhaoyang Liu, et al. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling. _arXiv preprint arXiv:2412.05271_ , 2024a. 

10 

Preprint. 

- Zhe Chen, Weiyun Wang, Yue Cao, Yangzhou Liu, Zhangwei Gao, Erfei Cui, Jinguo Zhu, Shenglong Ye, Hao Tian, Zhaoyang Liu, et al. Expanding performance boundaries of open-source multimodal models with model, data, and test-time scaling. _arXiv preprint arXiv:2412.05271_ , 2024b. 

- Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, and Shuran Song. Diffusion policy: Visuomotor policy learning via action diffusion. _The International Journal of Robotics Research_ , pp. 02783649241273668, 2023. 

- Shivin Dass, Jullian Yapeter, Jesse Zhang, Jiahui Zhang, Karl Pertsch, Stefanos Nikolaidis, and Joseph J. Lim. Clvr jaco play dataset, 2023. URL https://github.com/clvrai/clvr_ jaco_play_dataset. 

- Yu Fang, Yue Yang, Xinghao Zhu, Kaiyuan Zheng, Gedas Bertasius, Daniel Szafir, and Mingyu Ding. Rebot: Scaling robot learning with real-to-sim-to-real robotic video synthesis. _arXiv preprint arXiv:2503.14526_ , 2025. 

- Yuxin Fang, Wen Wang, Binhui Xie, Quan Sun, Ledell Wu, Xinggang Wang, Tiejun Huang, Xinlong Wang, and Yue Cao. Eva: Exploring the limits of masked visual representation learning at scale. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , pp. 19358–19369, 2023. 

- Matthew Honnibal. spacy 2: Natural language understanding with bloom embeddings, convolutional neural networks and incremental parsing. _(No Title)_ , 2017. 

- Physical Intelligence, Kevin Black, Noah Brown, James Darpinian, Karan Dhabalia, Danny Driess, Adnan Esmail, Michael Equi, Chelsea Finn, Niccolo Fusai, et al. _π_ 0 _._ 5: a vision-language-action model with open-world generalization. _arXiv preprint arXiv:2504.16054_ , 2025. 

- Eric Jang, Alex Irpan, Mohi Khansari, Daniel Kappler, Frederik Ebert, Corey Lynch, Sergey Levine, and Chelsea Finn. Bc-z: Zero-shot task generalization with robotic imitation learning. In _Conference on Robot Learning_ , pp. 991–1002. PMLR, 2022. 

- Dongfu Jiang, Xuan He, Huaye Zeng, Cong Wei, Max Ku, Qian Liu, and Wenhu Chen. Mantis: Interleaved multi-image instruction tuning. _Transactions on Machine Learning Research_ . 

- Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li FeiFei, Anima Anandkumar, Yuke Zhu, and Linxi Fan. Vima: Robot manipulation with multimodal prompts, 2023. 

- Siddharth Karamcheti, Suraj Nair, Ashwin Balakrishna, Percy Liang, Thomas Kollar, and Dorsa Sadigh. Prismatic vlms: Investigating the design space of visually-conditioned language models. In _Forty-first International Conference on Machine Learning_ , 2024. 

- Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, Ted Xiao, Ashwin Balakrishna, Suraj Nair, Rafael Rafailov, Ethan P Foster, Pannag R Sanketi, Quan Vuong, et al. Openvla: An open-source vision-language-action model. In _8th Annual Conference on Robot Learning_ . 

- Feng Li, Renrui Zhang, Hao Zhang, Yuanhan Zhang, Bo Li, Wei Li, Zejun Ma, and Chunyuan Li. Llava-interleave: Tackling multi-image, video, and 3d in large multimodal models. In _The Thirteenth International Conference on Learning Representations_ . 

- Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi. Blip-2: Bootstrapping language-image pre-training with frozen image encoders and large language models. In _International conference on machine learning_ , pp. 19730–19742. PMLR, 2023. 

- Xuanlin Li, Kyle Hsu, Jiayuan Gu, Karl Pertsch, Oier Mees, Homer Rich Walke, Chuyuan Fu, Ishikaa Lunawat, Isabel Sieh, Sean Kirmani, et al. Evaluating real-world robot manipulation policies in simulation. In _8th Annual Conference on Robot Learning_ , 2024. 

- Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ , 2024a. 

11 

Preprint. 

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning. _Advances in neural information processing systems_ , 36:34892–34916, 2023a. 

- Huihan Liu, Soroush Nasiriany, Lance Zhang, Zhiyao Bao, and Yuke Zhu. Robot learning on the job: Human-in-the-loop autonomy and learning during deployment. In _Robotics: Science and Systems (RSS)_ , 2023b. 

- Songming Liu, Lingxuan Wu, Bangguo Li, Hengkai Tan, Huayu Chen, Zhengyi Wang, Ke Xu, Hang Su, and Jun Zhu. Rdt-1b: a diffusion foundation model for bimanual manipulation. _arXiv preprint arXiv:2410.07864_ , 2024b. 

- Gen Luo, Xue Yang, Wenhan Dou, Zhaokai Wang, Jiawen Liu, Jifeng Dai, Yu Qiao, and Xizhou Zhu. Mono-internvl: Pushing the boundaries of monolithic multimodal large language models with endogenous visual pre-training. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 2025. 

- Corey Lynch, Ayzaan Wahid, Jonathan Tompson, Tianli Ding, James Betker, Robert Baruch, Travis Armstrong, and Pete Florence. Interactive language: Talking to robots in real time. _IEEE Robotics and Automation Letters_ , 2023. 

- Matthias Minderer, Alexey Gritsenko, and Neil Houlsby. Scaling open-vocabulary object detection. _Advances in Neural Information Processing Systems_ , 36:72983–73007, 2023. 

- Abby O’Neill, Abdul Rehman, Abhiram Maddukuri, Abhishek Gupta, Abhishek Padalkar, Abraham Lee, Acorn Pooley, Agrim Gupta, Ajay Mandlekar, Ajinkya Jain, et al. Open x-embodiment: Robotic learning datasets and rt-x models: Open x-embodiment collaboration 0. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ , pp. 6892–6903. IEEE, 2024. 

- Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning transferable visual models from natural language supervision. In _International conference on machine learning_ , pp. 8748–8763. PmLR, 2021. 

- Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman R¨adle, Chloe Rolland, Laura Gustafson, et al. Sam 2: Segment anything in images and videos. _arXiv preprint arXiv:2408.00714_ , 2024. 

- Saumya Saxena, Mohit Sharma, and Oliver Kroemer. Multi-resolution sensing for real-time control with vision-language models. In _7th Annual Conference on Robot Learning_ , 2023. 

- Rutav Shah, Roberto Mart´ın-Mart´ın, and Yuke Zhu. Mutex: Learning unified policies from multimodal task specifications. In _7th Annual Conference on Robot Learning_ , 2023. URL https://openreview.net/forum?id=PwqiqaaEzJ. 

- Lucy Xiaoyang Shi, Zheyuan Hu, Tony Z Zhao, Archit Sharma, Karl Pertsch, Jianlan Luo, Sergey Levine, and Chelsea Finn. Yell at your robot: Improving on-the-fly from language corrections. _CoRR_ , 2024. 

- Austin Stone, Ted Xiao, Yao Lu, Keerthana Gopalakrishnan, Kuang-Huei Lee, Quan Vuong, Paul Wohlhart, Sean Kirmani, Brianna Zitkovich, Fei Xia, et al. Open-world object manipulation using pre-trained vision-language models. In _7th Annual Conference on Robot Learning_ , 2023. 

- Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models. _arXiv preprint arXiv:2405.09818_ , 2024. 

- Gemini Robotics Team, Saminda Abeyruwan, Joshua Ainslie, Jean-Baptiste Alayrac, Montserrat Gonzalez Arenas, Travis Armstrong, Ashwin Balakrishna, Robert Baruch, Maria Bauza, Michiel Blokzijl, et al. Gemini robotics: Bringing ai into the physical world. _arXiv preprint arXiv:2503.20020_ , 2025. 

- Octo Model Team, Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, Sudeep Dasari, Joey Hejna, Tobias Kreiman, Charles Xu, et al. Octo: An open-source generalist robot policy. _arXiv preprint arXiv:2405.12213_ , 2024. 

12 

Preprint. 

- Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ , 2023. 

- Homer Walke, Kevin Black, Abraham Lee, Moo Jin Kim, Max Du, Chongyi Zheng, Tony Zhao, Philippe Hansen-Estruch, Quan Vuong, Andre He, Vivek Myers, Kuan Fang, Chelsea Finn, and Sergey Levine. Bridgedata v2: A dataset for robot learning at scale. In _7th Annual Conference on Robot Learning_ , 2023a. 

- Homer Rich Walke, Kevin Black, Tony Z Zhao, Quan Vuong, Chongyi Zheng, Philippe HansenEstruch, Andre Wang He, Vivek Myers, Moo Jin Kim, Max Du, et al. Bridgedata v2: A dataset for robot learning at scale. In _Conference on Robot Learning_ , pp. 1723–1736. PMLR, 2023b. 

- Junjie Wen, Yichen Zhu, Jinming Li, Minjie Zhu, Zhibin Tang, Kun Wu, Zhiyuan Xu, Ning Liu, Ran Cheng, Chaomin Shen, et al. Tinyvla: Towards fast, data-efficient vision-language-action models for robotic manipulation. _IEEE Robotics and Automation Letters_ , 2025. 

- Le Xue, Manli Shu, Anas Awadalla, Jun Wang, An Yan, Senthil Purushwalkam, Honglu Zhou, Viraj Prabhu, Yutong Dai, Michael S Ryoo, et al. xgen-mm (blip-3): A family of open large multimodal models. _arXiv preprint arXiv:2408.08872_ , 2024. 

- Ge Yan, Kris Wu, and Xiaolong Wang. ucsd kitchens Dataset. August 2023. 

- An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2. 5 technical report. _arXiv preprint arXiv:2412.15115_ , 2024. 

- Qingqing Zhao, Yao Lu, Moo Jin Kim, Zipeng Fu, Zhuoyang Zhang, Yecheng Wu, Zhaoshuo Li, Qianli Ma, Song Han, Chelsea Finn, et al. Cot-vla: Visual chain-of-thought reasoning for visionlanguage-action models. _arXiv preprint arXiv:2503.22020_ , 2025. 

- Wei Zhao, Pengxiang Ding, Zhang Min, Zhefei Gong, Shuanghao Bai, Han Zhao, and Donglin Wang. Vlas: Vision-language-action model with speech instructions for customized robot manipulation. In _The Thirteenth International Conference on Learning Representations_ . 

- Haoyu Zhen, Xiaowen Qiu, Peihao Chen, Jincheng Yang, Xin Yan, Yilun Du, Yining Hong, and Chuang Gan. 3d-vla: A 3d vision-language-action generative world model. In _International Conference on Machine Learning_ , pp. 61229–61245. PMLR, 2024. 

- Allen Zren. open-pi-zero. https://github.com/allenzren/open-pi-zero, 2025. 

13 

Preprint. 

# **Appendix** 

## A INTERLEAVE-VLA IMPLEMENTATION DETAILS 

We extend two state-of-the-art VLA models, _π_ 0 (Black et al., 2024) and OpenVLA (Kim et al.), to develop Interleave-VLA. While VLA models encompass a wide range of architectures (Intelligence et al., 2025; Team et al., 2025; Bjorck et al., 2025; Liu et al., 2024b; Shi et al., 2024; Brohan et al., 2022; 2023; Team et al., 2024; Chi et al., 2023), we focus on those based on VLM backbones due to their inherent ability to process image-text pairs. However, our approach is not restricted to VLM-based methods and can be extended to other sequence modeling approaches for action prediction (Chi et al., 2023; Team et al., 2024; Liu et al., 2024b; Brohan et al., 2022). The key modification involves interleaving image and text embeddings within the input sequence. Investigating the feasibility of this modification for other sequence modeling VLAs is an exciting direction for future research. In this work, we focus on and provide adaptations of Interleave-VLA from _π_ 0 and OpenVLA in the following sections in more detail. 


Figure 7: Comparison of Interleave-VLA and Text-VLA architectures. Interleave-VLA is modelagnostic and requires minimal modifications to existing VLA architectures. The only change is the input format, which allows for interleaved image-text instructions. 

### A.1 INTERLEAVE-VLA ON _π_ 0 

We make minimal architectural changes to the _π_ 0 (Black et al., 2024) model: only the input processor. Specifically, to enable interleaved image-text instructions, we extend its tokenizer vocabulary by introducing special tokens <BOI> (beginning of image) and <EOI> (end of image). These newly added tokens are used to delineate image embeddings within the instruction sequence. Specifically, the input tokens are constructed as follows: 

<BOI> <image>1 ... <image>256 <EOI> <text> <BOI> <image>257 ... <image>512 <EOI> <text> <BOI> <image>513 ... <image>768 <EOI> <text> ... 

Here, each <image> token represents a patch embedding from the visual encoder, and the <BOI> and <EOI> tokens mark the boundaries of each interleaved image segment. This design allows the model to flexibly process multimodal instructions by alternating between image and text tokens within a unified sequence. 

Our Interleave-VLA approach is both _effective_ and _model-agnostic_ , requiring only _minimal modifications_ . Its _effectiveness_ is evidenced by substantial improvements in generalization performance over _π_ 0, achieving 2–3 _×_ gains as shown in Table 1 and Table 2. Interleave-VLA is _model-agnostic_ , seamlessly integrating into existing VLA models without requiring assumptions about the VLM. In Interleave-VLA based on _π_ 0, the VLM backbone Paligemma (Beyer et al., 2024) demonstrates compatibility despite not being pre-trained on Internet-scale interleaved image-text data. Moreover, our approach introduces only _minimal modifications_ , with no architectural changes needed for the underlying VLM backbone. These facts highlight the practicality and broad applicability of Interleave-VLA for advancing multimodal robot learning. 

### A.2 INTERLEAVE-VLA ON OPENVLA 

While architectural changes are not required to the VLM backbone—as demonstrated in our adaptation from _π_ 0—we further investigate whether modifying the backbone architecture affects its ef- 

14 

Preprint. 

fectiveness. Specifically, we replace OpenVLA’s original Prismatic VLM (Karamcheti et al., 2024) backbone with InternVL2.5 (Chen et al., 2024b), which inherently supports the interleaved imagetext format. As shown in Figure 6, our Interleave-VLA adaptation based on OpenVLA continues to function effectively, achieving more than double the performance of the original OpenVLA. This result further highlights the model-agnostic nature of Interleave-VLA and its compatibility with diverse VLA architectures. We have tested on different VLM backbone for OpenVLA in Table 5 and found that changing OpenVLA’s VLM backbone has negligible effect on performance. 

|Method (VLM, Input)|L1|L2|L3|
|---|---|---|---|
|Interleave-VLA (InternVL2.5, Interleaved)|**83.14**|**58.14**|**64.00**|
|OpenVLA (Prismatic, Text)|53.71|23.00|23.86|
|OpenVLA (InternVL2.5, Text)|45.29|24.71|29.71|


Table 5: Comparing Interleave-VLA and OpenVLA with different VLM backbones on VIMABench. 

## B RELIABILITY ANALYSIS OF THE INTERLEAVED DATASET GENERATION PIPELINE 

Figure 8 illustrates the two _complementary_ stages of our generation pipeline: Owlv2 and QwenVL+SAM. Empirical observations indicate that QwenVL+SAM excels at handling openworld objects, such as the green star shown in the top right of the figure. However, it struggles in cluttered scenes or under occlusions, as depicted on the left side of the figure, where Owlv2 demonstrates superior performance. Notably, the combined approach significantly reduces failure rates, although both methods face challenges under severe occlusions or low image resolution. 

To evaluate accuracy, we randomly sampled 200 examples from the generated dataset and verified whether the detected images matched the corresponding text. Each sample may contain multiple key objects, and we considered it a failure if any key object was not detected. The individual error rates for QwenVL+SAM and Owlv2 were 22.1% and 17.4%, respectively, while the combined approach reduced the error rate to just _4.4%_ . These results highlight the effectiveness of integrating these two models to enhance the reliability of the generation pipeline. 


Figure 8: Red: QwenVL+SAM and Yellow: Owlv2. Individual error rates are 22.1% and 17.4%, respectively. The combined error rate is reduced to _4.4%_ . 

15 

Preprint. 

## C EVALUATION DETAILS 

- C.1 EVALUATION ON SIMPLERENV 

### C.1.1 SIMPLERENV EVALUATION TASKS 

Our evaluation on SimplerEnv (Li et al., 2024) includes both In-Domain and Out-of-Domain tasks. The In-Domain tasks follow the original SimplerEnv WidowX BridgeData V2 Visual Matching setup. Since SimplerEnv tasks use text-based instructions, we adapt them into interleaved imagetext instructions using the method described in Section 3.3, based on the first frame of the rollout before the robot arm begins moving. 

In the WidowX BridgeData V2 setup, SimplerEnv does not support generalization tasks (referred to as the Variant Aggregation setup). To overcome this limitation, we introduce a set of challenging Out-of-Domain tasks inspired by the Open Vocabulary manipulation evaluations (Stone et al., 2023). Unlike prior methods that rely on separate VLMs to detect target objects in the scene and inject this information into the robot policy, our Interleave-VLA directly leverages interleaved image-text instruction to perform these tasks without requiring additional modules. These tasks are deliberately designed to be more challenging than the original SimplerEnv tasks, requiring the robot to generalize to novel objects and environments unseen during training on BridgeData V2 (Walke et al., 2023a). 

We describe the 13 tasks (4 In-Domain and 9 Out-of-Domain, as illustrated on the left of Figure 4) used in the SimplerEnv evaluation. The Out-of-Domain tasks are introduced in the order they appear from top left to bottom right, in Figure 4. 

1. **widowx spoon on towel** (In-Domain): This task is part of the original SimplerEnv Visual Matching setting and is included in the BridgeData V2. 

2. **widowx carrot on plate** (In-Domain): Also from the original SimplerEnv Visual Matching setting, this scenario is present in the training data. 

3. **widowx stack cube** (In-Domain): This stacking task is included in the original SimplerEnv Visual Matching setting and present in the training data. 

4. **widowx put eggplant in basket** (In-Domain): This task is part of the original SimplerEnv Visual Matching setting and is present in the training data. 

5. **widowx spoon on towel, unseen environment** (Out-of-Domain, Visual Generalization): The environment overlay is sourced from the RT-1 Dataset (Brohan et al., 2022) and is not seen during Bridge V2 training. The robot must generalize to a novel environment. 

6. **widowx spoon on towel, unseen tablecloth** (Out-of-Domain, Visual Generalization): The tablecloth overlay is a random image from the internet, unseen in Bridge V2 training data, requiring the robot to generalize to new visual backgrounds. 

7. **widowx spoon on towel, unseen lighting** (Out-of-Domain, Visual Generalization): The scene lighting changes dynamically with different colors (RGB) at 5Hz. The robot must generalize to novel and rapidly changing lighting conditions. 

8. **widowx redbull on plate** (Out-of-Domain, Semantic Generalization): This is an unseen object from a known category. While similar cans (e.g., tomato can) appear in training, the Redbull can is new. The robot must use language grounding to identify and manipulate the correct object among distractors (e.g., a Coca-Cola can). 

9. **widowx tennis ball in basket** (Out-of-Domain, Semantic Generalization): This is an unseen object from a known category. While similar balls (e.g., white ball, blue ball) appear in training, the tennis ball is new. The robot must use language grounding to select and manipulate the correct object among distractors (an orange and a ping pong ball). 

10. **widowx zucchini on plate** (Out-of-Domain, Semantic Generalization): This task involves an unseen object from a known category. While a similar zucchini appears only once among 40,000 training episodes, this specific zucchini is entirely novel. The robot must leverage language grounding to accurately identify and manipulate the correct object, distinguishing it from distractors such as a carrot. 

11. **widowx zucchini on saucer dish** (Out-of-Domain, Semantic Generalization): This task introduces a novel zucchini instance and an unfamiliar destination—a saucer dish—both of which 

16 

Preprint. 

are unseen objects from known categories. The robot must ground the instruction to correctly identify the target zucchini and place it onto the saucer, discriminating it from distractors such as a carrot and a regular plate. 

12. **widowx toy dinosaur on towel** (Out-of-Domain, Semantic Generalization): This is a completely unseen category. The robot must use language grounding to identify and manipulate the correct object among distractors (a toy elephant). 

13. **widowx tape measure in basket** (Out-of-Domain, Semantic Generalization): This is a completely unseen category. The robot must use language grounding to identify and manipulate the correct object among distractors (a purple eggplant). 

14. **widowx stapler on paper pile** (Out-of-Domain, Semantic Generalization): This task involves a completely unseen category for both the object and the destination. The robot must leverage language grounding to accurately identify and manipulate the correct object (a stapler) among distractors (e.g., a spatula) and place it onto the unseen destination, the paper pile. 

### C.1.2 SIMPLERENV BASELINES 

Our experiment in Table 1 compares Interleave-VLA (adapted from _π_ 0) with _π_ 0 (Black et al., 2024), RT-1-X (Brohan et al., 2022), and Octo-Base (Team et al., 2024). RT-1-X and Octo models are evaluated using their official checkpoints and code, following the evaluation protocol in the SimplerEnv (Li et al., 2024) repository. For _π_ 0, we use the reimplementation from the GitHub repository (Zren, 2025), which is specifically trained on BridgeData V2 (Walke et al., 2023a) and supports direct evaluation on SimplerEnv. Interleave-VLA is built upon this reimplemented _π_ 0 codebase, with modifications to the input tokens and training on the interleaved BridgeData V2, using the interleaved dataset construction pipeline described in Section 3.3. To further highlight the benefits of large-scale, diverse, cross-embodiment data, we also co-train Interleave-VLA with our curated Open Interleaved X-Embodiment Dataset, as detailed in Section 3.3. 

Both Interleave-VLA (including the co-trained variant) and _π_ 0 models were trained with a learning rate of 5e-5, a global batch size of 1024, for approximately 30 epochs. The model input consists of a single observation image (no history), interleaved image-text instruction tokens, one proprioceptive token (no history), and four action tokens. Training takes roughly 2 days on 4 _×_ H100 GPUs with a per device batch size of 16. Actions and proprioception across the diverse datasets are normalized to the 7D format: xyz position, Euler orientation, and gripper state, with all values scaled to the range [ _−_ 1 _,_ 1]. 

The results presented in Table 1 reflect the best performance across checkpoints. Notably, performance can vary significantly between checkpoints, even among those that appear mostly converged. This variability is particularly pronounced for challenging tasks requiring precise manipulation, such as ”widowx stack cube”. These observations align with findings reported in the _π_ 0 reimplementation GitHub repository (Zren, 2025). 

### C.1.3 SIMPLERENV EVALUATION RESULTS 

Table 6 provides detailed generalization results for the top-performing models: _π_ 0, Interleave-VLA (adapted from _π_ 0), and Interleave-VLA co-trained, as reported in Table 1. Interleave-VLA consistently surpasses _π_ 0 across all Out-of-Domain generalization tasks, demonstrating the effectiveness of multimodal learning from interleaved image-text data for both visual and semantic generalization. The co-trained Interleave-VLA model achieves further improvements, especially on semantic generalization tasks such as “RedBull on Plate,” where similar RedBull cans are present in the RT-1 dataset for the Google robot. This highlights positive cross-embodiment task transfer to the WidowX robot. Overall, these results show that training with large-scale, diverse robot data enhances model generalization to novel tasks and robot embodiments, supporting our approach of curating the Open Interleaved X-Embodiment Dataset. 

Note that the Unseen Environment setting is omitted for the Interleave-VLA co-trained model because the scene overlay is sourced from the RT-1 Google Robot dataset, which is included in the co-train data. As a result, the model tends to generate actions intended for the Google Robot. During evaluation, however, the robot used is WidowX, leading to a mismatch in embodiment and causing the model to produce incorrect actions. 

17 

Preprint. 

Table 6: Detailed evaluation results on 9 Out-of-Domain generalization tasks based on SimplerEnv. Success rates (%) are reported for _π_ 0, Interleave-VLA (adapted from _π_ 0), and Interleave-VLA cotrained with our Open Interleaved X-Embodiment Dataset, covering both visual and semantic generalization. Generalization results confirm that Interleave-VLA outperforms _π_ 0 across all tasks, with further cross-embodiment improvements from co-training. 

||Visu|al Generalizati|on|||Se|mantic Generali|zation|||
|---|---|---|---|---|---|---|---|---|---|---|
||Unseen|Unseen|Unseen|Redbull|Tennis Ball|Zucchini|Toy Dinosaur|Tape Measure|Stapler on||
|Model|Tablecloth|Environment|Lighting|on Plate|in Basket|on Plate|<br>on Towel|<br>in Basket|<br>Paper Pile|Average|
|_π_0|78.0|77.0|59.2|0.0|30.0|50.0|24.0|1.0|38.0|39.7|
|Interleave-VLA|**80.0**|**79.0**|**61.3**|**35.0**|**73.0**|**83.0**|**39.0**|**53.0**|**70.0**|**63.4**|


### C.2 EVALUATION ON VIMA-BENCH 

### C.2.1 VIMA-BENCH EVALUATION TASKS 

We evaluate performance on the majority of VIMA-Bench tasks, but excluding those requiring historical memory. Memory-dependent tasks are omitted because Interleave-VLA, like common VLA models (Kim et al.; O’Neill et al., 2024; Brohan et al., 2022; 2023; Black et al., 2024; Team et al., 2025; Fang et al., 2025; Wen et al., 2025), is designed for memory-independent, first-order Markov settings. In general, common VLA models characterize the conditional distribution _p_ ( **A** _t|_ **o** _t_ ), where **A** _t_ = [ **a** _t,_ **a** _t_ +1 _, . . . ,_ **a** _t_ + _H−_ 1] represents a sequence of future actions, and **o** _t_ denotes the current observation (comprising multiple RGB images, a language command, and the robot’s proprioceptive state). Extending VLAs to handle historical memory in interleaved instruction scenarios remains an interesting direction for future work. 

VIMA-Bench employs interleaved image-text instructions for task specification. To evaluate textinstructed VLA models, we transform these interleaved instructions into text-only instructions by utilizing the shape and texture names provided in the VIMA-Bench codebase. For example: 

VIMA-Bench Instruction: Put the into the . Transformed Instruction: Put the rainbow triangle into the blue square. 

### C.2.2 VIMA-BENCH BASELINES 

We evaluate Interleave-VLA (adapted from OpenVLA) against several baselines: OpenVLA (Kim et al.), VIMA-Gato (Jiang et al., 2023), VIMA-Flamingo (Jiang et al., 2023), and VIMA-GPT (Jiang et al., 2023). All models are trained on the same dataset generated using an oracle model, which has access to the exact 2D poses of all objects in the scene. This dataset generation process is provided by VIMA. For OpenVLA, the training data consists of text-instructed samples. Both InterleaveVLA and OpenVLA are trained on an equivalent amount of the generated VIMA dataset using the following training hyperparameters: a constant learning rate of 2e-5 and a global batch size of 128. This comparison demonstrates the effectiveness of Interleave-VLA in improving generalization performance over existing VLA models. The results for VIMA-Gato, VIMA-Flamingo, and VIMAGPT are taken from the original VIMA paper (Jiang et al., 2023) and serve as additional benchmarks. These models, adapted by the VIMA team, serve as benchmarks to assess the progression of VLA models from earlier architectures like Gato, Flamingo, and GPT to the more advanced OpenVLA. 

### C.2.3 VIMA-BENCH EVALUATION RESULTS 

The detailed results for the memory-independent VIMA-Bench tasks are presented in Table 7. The results demonstrate that Interleave-VLA benefits significantly from interleaved image-text instructions, which enhance its ability to identify and manipulate the correct object by 2 _×_ . This approach proves more effective than relying solely on text descriptions to distinguish objects with the desired texture and shape among distractors. 

18 

Preprint. 

Table 7: Detailed VIMA-Bench results for L1, L2, and L3 level generalization evaluations. Interleave-VLA generally outperforms other VLA models and improves the generalization capacity of OpenVLA (Kim et al.) by over 2 _×_ . 

||**VI**|**MA-Be**|**nch L1**||||||
|---|---|---|---|---|---|---|---|---|
|Model Name|task1|task2|task3|task4|task7|task11|task15|AVG|
|OpenVLA (Kim et al.)|83|70|78|4|**92**|0|49|53.71|
|Interleave-VLA|**87**|**82**|81|54|82|**100**|**96**|**83.14**|
|VIMA-Gato|79|68|**91**|**57**|74|61|83|73.29|
|VIMA-Flamingo|56|58|63|48|62|66|40|56.14|
|VIMA-GPT|62|57|41|55|54|77|41|55.29|
||**VI**<br>|**MA-Be**<br>|**nch L2**<br>||||||
|OpenVLA (Kim et al.)|18|20|68|2|31|0|22|23.00|
|Interleave-VLA|36|32|75|44|26|**100**|**94**|58.14|
|VIMA-Gato|**56.5**|**53.5**|**88**|**55.5**|53|63|81.5|**64.43**|
|VIMA-Flamingo|51|52.5|61.5|49.5|**55.5**|82|42|56.29|
|VIMA-GPT|52|52|49.5|54.5|51|76.5|43|54.07|
||**VI**|**MA-Be**|**nch L3**||||||
|OpenVLA (Kim et al.)|27|36|61|3|26|0|14|23.86|
|Interleave-VLA|**52**|55|81|53|46|**98**|**63**|**64.00**|
|VIMA-Gato (Jiang et al., 2023)|51|**58**|**84.5**|**56.5**|49|65|52|59.43|
|VIMA-Flamingo (Jiang et al., 2023)|49|50|66.5|47|50|66|30.5|51.29|
|VIMA-GPT (Jiang et al., 2023)|**52**|51|55|49.5|**50.5**|82|37|53.86|


- C.3 EVALUATION ON REAL ROBOT 

### C.3.1 REAL ROBOT EVALUATION TASKS 

We evaluate on two distinct manipulation tasks: Lift and Pick&Place, corresponding to the first and second rows of results shown in Table 2. Visual illustrations of these tasks are shown on the right side of Figure 4. The tasks are designed to be challenging, requiring the robot to generalize to novel objects not seen during training. We describe these tasks in more detail. 

The Lift task includes: 

1. **Lift pepper** (In-Domain): 20 demonstrations collected with varied object arrangements and positions. 

2. **Lift cup** (In-Domain): 20 demonstrations collected with varied object arrangements and positions. 

3. **Lift corn** (In-Domain): 20 demonstrations collected with varied object arrangements and positions. 

4. **Lift lemon** (Out-of-Domain, Semantic Generalization): The target is an unseen object, as lemons are not included in the collected demonstrations. Although the lemon category appears in the pretraining data, it appears with different textures, robots, and environments. VLA models must utilize language grounding to accurately identify and lift the target lemon among two distractor items. 

5. **Lift bean** (Out-of-Domain, Semantic Generalization): The target belongs to a completely unseen category, as beans are absent from both the collected demonstrations and the pretraining dataset. VLA models must rely on language grounding to correctly identify and lift the target bean among two distractor items. 

6. **Lift spoon** (Out-of-Domain, Semantic Generalization): The target is an unseen object from a known category, as the demonstrations do not include this specific spoon. While the spoon category appears in the pretraining data, it is represented with different textures, robots, and environ- 

19 

Preprint. 

ments. VLA models must leverage language grounding to accurately identify and lift the target spoon among two distractor items. 

The Pick&Place task includes: 

1. **Pick up kitchen cutter and place into the pot** (In-Domain): 20 demonstrations collected with varied object arrangements and positions. 

2. **Pick up ladle and place into the pot** (In-Domain): 20 demonstrations collected with varied object arrangements and positions. 

3. **Pick up pasta server and place into the pot** (In-Domain): 20 demonstrations collected with varied object arrangements and positions. 

4. **Pick up the white and blue spatula and place it into the pot** (Out-of-Domain, Semantic Generalization): The target is an unseen object from a known category. The demonstrations do not include any spatula. While the spatula category appears in the pretraining data, it is shown with different textures, robots, and environments. VLA models must utilize language grounding to accurately identify and manipulate the target spatula among two distractor kitchenware items. 

5. **Pick up the black and white spatula and place it into the pot** (Out-of-Domain, Semantic Generalization): Similar to the previous task, but the target spatula is black and white. The robot must leverage language grounding to correctly identify and manipulate the target spatula among two distractor kitchenware items. 

### C.3.2 REAL ROBOT BASELINES 

We compare Interleave-VLA (adapted from _π_ 0) with pretraining against the following baselines: _π_ 0 with pretraining and Interleave-VLA without pretraining. The pretraining dataset is a subset of our curated Open Interleaved X-Embodiment Dataset, as described in Section 3.3. Interleave-VLA w/ PT is pretrained on this dataset and subsequently fine-tuned on the collected demonstrations from the FANUC robot arm before evaluation. For _π_ 0 w/ PT, the same pretraining and fine-tuning protocol is applied, except the dataset is not interleaved. This setup allows for a direct comparison to evaluate the benefits of interleaved image-text instructions for generalization. The Interleave-VLA w/o PT is trained exclusively on the collected FANUC demonstrations, without exposure to the Open Interleaved X-Embodiment Dataset, enabling us to assess the impact of large-scale, diverse pretraining on performance. All models are fine-tuned with a learning rate of 5e-5, a global batch size of 128, and evaluated across several checkpoints to mitigate the performance variability noted in Appendix C.1.2. 

### C.3.3 REAL ROBOT EVALUATION RESULTS 

Tables 8 and 9 present the detailed evaluation results for the Lift and Pick&Place tasks, respectively. Interleave-VLA, adapted from _π_ 0, is compared against _π_ 0 and Interleave-VLA without pretraining (w/o PT). In generalization tasks, Interleave-VLA consistently outperforms _π_ 0 in semantic generalization by 2 _×_ , highlighting the effectiveness of multimodal learning from interleaved imagetext data. The results further demonstrate that pretraining on the Open Interleaved X-Embodiment Dataset significantly enhances performance across all tasks. For small-scale datasets (60 demonstrations in total per task), pretraining on the Open Interleaved X-Embodiment Dataset proves essential for achieving strong performance, as cross-embodiment pretraining enables the model to learn more robust representations and generalize effectively, even to the FANUC robot, which is not included in the pretraining data. 

## D SCALABILITY OF INTERLEAVE-VLA WITH THE OPEN INTERLEAVED X-EMBODIMENT DATASET 

The Open Interleaved X-Embodiment Dataset, detailed in Section 3.3, empowers Interleave-VLA to scale efficiently with increasing data. This section demonstrates the scalability of Interleave-VLA through pretraining and co-training strategies in varying data regimes. 

**Pretraining for Low-Data Regimes:** As shown in Table 2, pretraining on the curated Open Interleaved X-Embodiment Dataset is essential for achieving strong performance on real robot tasks. 

20 

Preprint. 

Table 8: Detailed evaluation of the ”Lift task”. We conduct 12 trials for each object and report both the number of successful trials (# Succ) and the number of trials where the correct object is manipulated (# Acc). 

|Category|Task|# Trials|Interleave-VLA w/ PT<br># Succ / # Acc|Interleave-VLA w/o PT<br># Succ / # Acc|_π_0w/ PT<br># Succ / # Acc|
|---|---|---|---|---|---|
|In-Domain|pepper|12|7/12|2/4|7/10|
|In-Domain|corn|12|9/12|0/4|4/12|
|In-Domain|cup|12|8/12|0/4|3/12|
|Out-of-Domain|spoon|12|9/11|0/2|9/11|
|Out-of-Domain|bean|12|9/12|0/4|1/1|
|Out-of-Domain|lemon|12|8/12|0/4|2/5|
|||Mean Success / Accuracy Rate|69.4 % / 98.6 %|2.8 % / 30.6 %|36.1 % / 70.8 %|


Table 9: Detailed evaluation on ”Pick&Place task”. We conduct 12 trials for each object and report both the number of successful trials (# Succ) and the number of trials where the correct object is manipulated (# Acc). 

|Category|Task|# Trials|Interleave-VLA w/ PT<br># Succ / # Acc|Interleave-VLA w/o PT<br># Succ / # Acc|_π_0w/ PT<br># Succ / # Acc|
|---|---|---|---|---|---|
|In-Domain|pasta server|12|6/8|4/8|7/10|
|In-Domain|spoon|12|7/10|1/7|7/9|
|In-Domain|knife|12|4/7|2/7|4/12|
|Out-of-Domain|spatula|12|3/8|0/8|1/1|
|Out-of-Domain|black spatula|12|6/8|0/6|4/5|
|||Mean Success / Accuracy Rate|43.3 % / 68.3 %|11.7 % / 60 %|38.3 % / 61.7 %|


This is particularly important due to the limited size of the FANUC dataset, which contains only 60 demonstrations per task. Pretraining on the significantly larger and more diverse Open Interleaved X-Embodiment Dataset enables Interleave-VLA to learn robust representations that generalize effectively to the FANUC robot, even though it is not included in the pretraining data. 

**Co-Training for High-Data Regimes:** Co-training with additional datasets from the Open Interleaved X-Embodiment Dataset further enhances performance in semantic generalization tasks. While the Bridge Dataset V2 is already extensive and diverse, making substantial improvements challenging, co-training yields additional gains in semantic generalization. This demonstrates that interleaved training facilitates cross-embodiment skill transfer. Detailed results are presented in Table 10. 

Table 10: Scalability of Interleave-VLA through co-training on the Open Interleaved X-Embodiment Dataset, evaluated under the **SimplerEnv** Out-of-Domain setting. Incorporating datasets beyond Bridge Data V2 in the Open Interleaved X-Embodiment Dataset further improves performance in semantic generalization tasks. The **bold** and <u>underlined</u> values represent the highest and secondhighest scores, respectively. 

|**Base Model**|**Paradigm**|Co-trained|Visual|Novel Object|Novel Category|Avg.|
|---|---|---|---|---|---|---|
|_π_0(Black et al., 2024)|Interleave-VLA|✗|**73.4**|63.7|53.0|63.4|
|_π_0(Black et al., 2024)|Interleave-VLA|✓|71.5|**70.7**|**57.3**|**66.5**|


## E TASK FLEXIBILITY AND EMERGENT GENERALIZATION DETAILS 

To highlight the task flexibility and emergent generalization capabilities of Interleave-VLA when faced with unseen instructions, we leverage the interleaved image-text interface to evaluate its performance across diverse user input styles during deployment. The Interleave-VLA model used in this evaluation is directly taken from the SimplerEnv evaluation suite (Table 1 and Table 6) without any additional fine-tuning. A summary of Interleave-VLA’s performance statistics is presented in Table 3. 

Below, we describe the three tasks and their corresponding prompts in the order they appear in Table 3: 

21 

Preprint. 

1. **Place** **_{_ eggplant, carrot** **_}_ on the plate** . Two types of instructions are provided. The first row includes a hand-drawn sketch of an eggplant and a carrot, created by a human on-the-fly. The second row features a sketch-style image of an eggplant and a carrot sourced from the Internet. 

2. **Place** **_{_ green, yellow** **_}_ block on the towel** . Two types of instructions are included. The first row contains a hand-drawn sketch of a green and yellow block, created by a human on-the-fly. The second row features random images representing a green and yellow block, sourced from the Internet. 

3. **Place** **_{_ block, spoon** **_}_ on the towel** . Two types of instructions are used. The first row includes a hand-drawn sketch of a block and a spoon, created by a human on-the-fly. The second row features cropped images of the desired target objects, captured from a screen by a human on-thefly. 

Interleave-VLA demonstrates remarkable emergent generalization capabilities, even when faced with diverse instruction styles such as Internet images, object crops (from a familiar input style but with unseen images), and sketches (a completely novel input style not encountered during training). These emergent capabilities go beyond the typical generalization to novel objects and environments evaluated in prior VLA models (Black et al., 2024; Kim et al.). They highlight Interleave-VLA’s adaptability to new tasks and instruction formats, showcasing its practical flexibility in processing diverse multimodal inputs. 

## F OPEN INTERLEAVED X-EMBODIMENT DATASET DETAILS 

The Open Interleaved X-Embodiment Dataset, curated as described in Section 3.3 for training Interleave-VLA, integrates data from 11 sources within the Open X-Embodiment Dataset. To ensure coherent training and facilitate cross-embodiment transfer, the action space across all datasets is standardized to a unified 7D pose format: xyz position, Euler orientation, and gripper state. This normalization adheres to practices established in recent VLA research (Kim et al.; Black et al., 2024; Team et al., 2024). Our dataset features an extensive variety of over 3500 diverse object categories, as depicted on the left of Figure 3. Additionally, Figure 9 highlights the wide range of skills encompassed within the dataset and provides a detailed breakdown of its composition and partitioning. 


Figure 9: **Left:** Our Open Interleaved X-Embodiment Dataset is diverse in skills. **Right:** Composition of open data sources in our curated Open Interleaved X-Embodiment Dataset. 

22 

